---
title: 绿城杯-WriteUp
contest: 绿城杯
year: 2021
difficulty: medium
vuln_type: pwn_unknown
tags: [off-by-one, uaf-double-free, tcache-poisoning, libc-2.23, one-gadget, ROP, ORW, git-leak, eval-system, false-file-read]
attack_chain:
- Web warmup:git信息泄露+SQL注入+eval(system("tac pages/flag.php"))+payload:?link_page=23') or eval(system("tac pages/flag.php"));#
- Pwn null:off by one+libc-2.23 uaf+tcache攻击+__free_hook=system
- Pwn ezuaf:double free泄漏cfree后三位+mallochook确定libc 2.23+one_gadget 0x45226
- Pwn GreentownNote:uaf+堆重叠+tcache bin+__free_hook+open/read/write ORW
- Web ezphp:phpggc+SQL注入(时间盲注)+AES-CBC解密+RSA低位爆破
- Web easy_seri:PHP反序列化
key_payload: eval(system("tac pages/flag.php")) + one_gadget 0x45226
one_liner: 绿城杯WriteUp多方向,Web(warmup ezphp easy_seri)+Pwn(null off-by-one+ezuaf double-free+GreentownNote uaf ORW)。
lesson: 绿城杯是glibc-2.23时代典型off-by-one+tcache攻击;git信息泄露在Web题中是常见入口;时间盲注+1字节+快速爆破是密码攻击的实用技术。
quality: high
---

## 题目列表

Web(4): warmup / ezphp / easy_seri / 另一个
Pwn(3): null / ezuaf / GreentownNote / W

## 关键考点

### Web warmup
- git信息泄露
- payload:`?link_page=23') or eval(system("tac pages/flag.php"));%23`

### Pwn null (off-by-one)
- libc-2.23-0ubuntu11.2_amd64.so
- 经典off-by-one(2.23版本) → 0x71→0x91→0xa1 fake chunk
- tcache poisoning:edit(0)覆盖fd到__free_hook-0x10
- 两次add后__free_hook=system
- add(3,0x20,'/bin/sh\x00') + delete(3) = /bin/sh

### Pwn ezuaf (double-free)
- 远程double free泄漏cfree后三位
- mallochook地址通过libcdatabase确定libc 2.23
- 攻击one_gadget:og = [0x45226, 0x4527a, 0xf0364, 0xf1207]
- add(0x10)触发one_gadget

### Pwn GreentownNote (uaf ORW)
- libc-2.27
- 4次free+show泄堆地址
- add重叠+tcache bin攻击
- __free_hook改rop链
- open/read/write ORW三件套(0x2155f+0x23e6a+0x1b96+pop_rdi+pop_rsi+pop_rdx)

### Web ezphp
- phpggc反序列化工具
- SQL注入+时间盲注
- AES-CBC解密
- RSA低位爆破(factor分解+低位/高位拼接)

## 实战价值
- glibc-2.23时代的off-by-one+tcache是经典堆利用入门
- double free+mallochook确定libc版本是2021年CTF高频技巧
- git信息泄露(/.git/)在Web入门题是常见入口
- __free_hook+rop ORW是Heap+ORW的标准组合
- one_gadget是libc-2.23+的最简洁提权方式
