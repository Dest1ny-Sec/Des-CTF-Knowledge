---
title: 鹏城杯2023 Writeup –Polaris战队
contest: 鹏城杯 2023
year: 2023
difficulty: hard
vuln_type: pwn_unknown
tags: [6502-cpu-emu, custom-vm, tcache-dup, FSOP, off-by-one, heap-overlap, rust-reverse, rc4-decrypt, glob-fuzz, tera-ssti, php-deserialize]
attack_chain:
- 6502 CPU模拟器: get_mem/write_mem+IZX寻址模式,LDX/LDA/STA/ADC指令组合写shellcode
- silent: read溢出0x100字节+栈迁移到bss+爆破write+_start重复执行+汇编shellcode open/read/write
- babyheap: readn off-by-one构造chunk overlap+tcache劫持stdout泄露栈+栈劫持ROP
- Auto_Coffee_machine: re(idx)密码bypass后edit越界改stdout+libc泄露+__free_hook劫持
- Bad PE: RC4 th3k3y! 解密节区释放可执行程序
- web1: PHP反序列化Hacker+__get+finish->hacker()链触发
- web2: glob://backdoor_*.php爆破32字符后门+title[]=.php/data[]=<?php system("cat /f*")双参数覆盖
- Tera: tera模板引擎{%%}块标签绕表达式注入+__tera_context查看上下文
key_payload: 6502 LDX/LDA/ADC/STA字节码组合
one_liner: 鹏城杯2023 Polaris战队WP,PWN4题(6502模拟器+silent栈迁移+babyheap FSOP+咖啡机)+RE2题(Rust猜数字+RC4 PE节区)+WEB3题(反序列化+glob爆破+tera SSTI)。
lesson: 6502/ARM等异构CPU模拟器PWN题的关键是识别寻址模式(IZX)+指令集,栈迁移爆破write是2023年新热点,Rust逆向需要从unsafe块开始跟,tera模板{%%}块是常见SSTI绕表达式方式。
quality: high
---

## 题目列表

PWN(4): 6502 / silent / babyheap / Auto_Coffee_machine
RE(2): 安全编程(Rust猜数字) / Bad PE (RC4节区解密)
WEB(3): web1(反序列化) / web2(glob爆破) / Tera(SSTI)

## 关键考点

### 6502 CPU模拟器PWN
- get_mem(unsigned __int16 a1): 解析地址,mem_ptr + a1 (0-255) / mem_ptr + a1 - 256 + 256 (256-511) / mem_ptr + a1 - 65018 + 512 (0xFFFA-0xFFFF) / mem_ptr + a1 - 512 + 518 (其他)
- IZX寻址:cpu_fetch两次+offset索引
- payload使用p8(162)=LDX,p8(161)=LDA,p8(134)=STX,p8(129)=STA,p8(101)=ADC
- 写shellcode:`/bin/sh0`字符串

### silent: 栈迁移爆破write
- init_seccomp+alarm(30)+read(0, buf, 0x100)溢出
- 爆破write 1/4096成功率
- 栈迁移到0x603000-0x100,然后用_start重启到bss留libc地址
- 再次栈迁移到0x601000+0x1288+read堆地址+随机地址
- 命中后用libc的read/write做ORW shellcode
- shellcode:`mov eax, 0x67616c66; push rax; mov rdi, rsp; xor eax, eax; mov esi, eax; mov al, 2; syscall ; open + read + write`

### babyheap: readn off-by-one
- glibc 2.38+菜单:add(0x400-0x500)+edit(可越界1字节)+show+delete
- menu()先malloc(0x10)再printf+free泄露堆地址
- 构造chunk overlap(0x408+0x4f8堆叠)→delete(1)→add(0x418)+add(0x4e8)→delete(1)→add(0x500)→show(0)泄露libc
- tcache劫持stdout:edit(0)用`(heap_addr+0x2c0)>>0xc ^ (libc+0x1ff7a0)`作为chunk地址xor保护
- 篡改stdout为`0x00000000fbad3887` + write_base/read_base相等到libc+0x206258泄露栈地址
- 再次tcache dup到栈-0x128,栈劫持ROP

### Auto_Coffee_machine: 越界改stdout
- 菜单:1.buy 2.show 3.默认,re(idx)输入密码bypass:`p64(0x6e7770207473756a) + p64(0x746920)` (just win it)
- ed(idx, of, data)越界写edit
- 改stdout vtable到0x405e20+泄露libc+__free_hook=system+写"/bin/sh"

### Bad PE: RC4解密节区
- 异或释放另一可执行程序
- 关键Key:`th3k3y!`
- 完整RC4 KSA+PRGA恢复节区内容

### web2: glob爆破后门
- 32字符backdoor_xxxxxx.php
- list=['1'..'9','0','q'..'p','a'..'m']
- payload:`glob://backdoor_`+tmp+`*.php`
- 命中后`backdoor_00fbc51dcdf9eef767597fd26119a894.php?username=11&title[]=.php&data[]=<?php system("cat /f*")`

### Tera: tera模板SSTI
- tera模板引擎不能用`{{...}}`表达式(被过滤)
- 改用`{%...%}`块标签
- `__tera_context`查看上下文
- 模板:`{% set x = __tera_context %}{{x}}`或`{% if ... %}`

## 实战价值
- 异构CPU模拟器PWN:6502/RISC-V/ARM模拟器都是CTF热点
- 栈迁移爆破write/seccomp ORW的组合是2023-2024新趋势
- Rust逆向需要找unsafe块作为切入点
- tera模板{%%}块绕过表达式注入是2024-2025新攻击面
