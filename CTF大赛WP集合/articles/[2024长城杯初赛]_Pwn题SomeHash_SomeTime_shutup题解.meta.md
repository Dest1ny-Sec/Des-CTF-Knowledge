---
title: [2024 长城杯初赛] Pwn 题 SomeHash SomeTime shutup 题解
contest: 2024 长城杯初赛
year: 2024
difficulty: hard
vuln_type: fmt_string
tags: [fmt_string_pwn, stack_leak_libc, hn_arb_write, rop_pop_rdi_binsh_system, house_of_minho, fake_io_list_all_wfile_jumps, custom_shellcode_rop, open_read_write_flag, double_arb_write_loop]
attack_chain: SomeHash:name 长度 -0x98 + b"xxx>%6$p->%19$p->%21$p-" 泄 stack/libc/elf_base → cnt 变量 %hn 写大值 0x100 → 多次 %23$hn 写 stack_target → %53$hhn 单字节 6 次写 pop_rdi+ret+/bin/sh+system → SomeTime:循环 add/free 0x30-0x70+0xa0-0xf0 切割 unsorted bin 残余 → add 0x70 覆盖 size=0x5e1 fake chunk → add 0x100 + show 泄 libc → 多次 free 触发 _IO_list_all 攻击 + house of minho fake_file_addr → shutup:open/read/write flag shellcode 拼接 ROP
key_payload: payload = b"xxx>%6$p->%19$p->%21$p-" / cnt 偏移 0x5078 写 0x100 / %23$hn + %53$hhn 双写 / system @ libc+0x50d60 / fake_file_addr = heap_addr + 0x7f0 / shellcode = open+read+write flag
one_liner: 2024 长城杯初赛 3 道 Pwn：SomeHash fmt-string 栈泄露 + %hn 任意地址写 ROP + SomeTime 堆菜单 house_of_minho _IO_list_all 攻击 + shutup 自定义 shellcode+ROP 读 flag。
lesson: fmt-string 多次 %hn 写 stack 后用 %hhn 单字节写是经典的"64 位地址任意写"模板；house_of_minho 利用 0x70+ 小于等于 0x80 触发 _IO_list_all 攻击是 2024 新型 _IO 攻击。
quality: high
---
