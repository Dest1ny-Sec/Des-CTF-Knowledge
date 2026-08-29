---
title: 解析2025强网拟态Stack
contest: 强网拟态 2025 Stack
year: 2025
difficulty: hard
vuln_type: pwn_unknown
tags: [SROP, sigreturn, stack-pivot, mprotect, BSS, syscall, openat, sendfile, No-PIE, No-canary]
attack_chain:
- 题目描述:"I don't need libc, and I guess you don't need it either" 不需要libc
- 环境:No PIE+No canary+NX enabled+Full RELRO
- 关键gadgets:
  - 0x40140e: syscall ; ret
  - 0x40121d: pop rbp ; ret
  - 0x4013b7: leave ; ret (栈迁移)
- 思路:SROP (Sigreturn Oriented Programming)
- 步骤:
  1. 泄露栈地址:printf("Hello, %s!") 后0x10字节填充
  2. 栈溢出0x60+8(rbp)+8(ret)→read到BSS段
  3. 在BSS段构造SROP frame
  4. syscall 15 (rt_sigreturn) 恢复所有寄存器
  5. 调用mprotect(bss, 0x100, 7) 修改BSS段为RWX
  6. 在BSS段执行shellcode
  7. shellcode: openat(-100, '/flag') + sendfile(1, 'rax', 0, 0x50)
- read返回字节数:15→触发rt_sigreturn
- BSS页对齐:0x404000
key_payload: SROP + mprotect(bss, 0x100, 7) + shellcode(openat+sendfile)
one_liner: 强网拟态2025 Stack SROP+栈迁移+shellcode,No-PIE+No-canary+NX+Full RELRO,泄露栈+栈迁移到BSS+SROP调用mprotect(7=PROT_READ|WRITE|EXEC)+shellcode(openat/sendfile读flag)。
lesson: SROP是绕过NX+Full RELRO+无libc环境的终极武器,关键是构造SigreturnFrame+read返回15触发rt_sigreturn;mprotect+BSS段是NX保护绕过的标准组合;openat+sendfile是Linux文件读取的稳定syscall。
quality: high
---

## 题目列表

1道PWN:Stack (SROP)

## 关键考点

### 环境
- 64位ELF, No PIE, No canary, NX enabled, Full RELRO
- 题目描述:"I don't need libc, and I guess you don't need it either"
- 附件:libc.so.6 + ld-linux-x86-64.so.2

### 关键gadgets
- 0x40140e: syscall ; ret
- 0x40121d: pop rbp ; ret
- 0x4013b7: leave ; ret (栈迁移gadget)

### SROP原理
- Linux信号处理:收到信号→内核保存所有寄存器到栈(sigcontext)
- rt_sigreturn系统调用:信号处理完成后恢复所有寄存器
- 利用:伪造sigcontext→rt_sigreturn→内核恢复伪造寄存器
- 可以控制所有寄存器(rax/rdi/rsi/rdx/rsp/rip)
- 只需要一个syscall指令

### 攻击步骤
1. 泄露栈地址:printf("Hello, %s!") + 0x10填充
2. 栈溢出0x60字节+覆盖saved rbp为bss+0x800+覆盖ret为0x4013d4(read内部)
3. 第二次read到BSS段
4. 构造SROP frame + mprotect(bss, 0x100, 7)
5. read 15字节触发rt_sigreturn(rax=15)
6. mprotect修改BSS为RWX
7. shellcode: openat + sendfile

### SROP Frame
```python
sigframe = SigreturnFrame()
sigframe.rax = 0xa  # sys_mprotect
sigframe.rdi = bss  # addr
sigframe.rsi = 0x100  # len
sigframe.rdx = 7  # prot=PROT_READ|WRITE|EXEC
sigframe.rsp = 0x404910  # new stack
sigframe.rip = 0x40140e  # syscall
```

### shellcode
```python
sc = shellcraft.openat(-100, '/flag')
sc += shellcraft.sendfile(1, 'rax', 0, 0x50)
```

### 关键技术
- mprotect(7) = PROT_READ|PROT_WRITE|PROT_EXEC = RWX
- openat(-100, '/flag', ...) = AT_FDCWD相对当前工作目录
- sendfile(1, rax, 0, 0x50) = 内核空间传输,无需用户空间
- BSS页对齐:(addr >> 12) << 12
- read返回15:触发rt_sigreturn (syscall 15)

### 利用链
```
栈溢出 → 栈迁移到BSS → 构造SROP frame → read 15字节触发rt_sigreturn → mprotect(bss, RWX) → 执行shellcode(openat+sendfile) → flag
```

## 实战价值
- SROP是绕过NX+Full RELRO+无libc环境的终极武器
- 关键是构造SigreturnFrame+read返回15触发rt_sigreturn
- mprotect+BSS段是NX保护绕过的标准组合
- openat+sendfile是Linux文件读取的稳定syscall
- SigreturnFrame(pwntools)封装好,直接设置rax/rdi/rsi/rdx/rsp/rip即可
