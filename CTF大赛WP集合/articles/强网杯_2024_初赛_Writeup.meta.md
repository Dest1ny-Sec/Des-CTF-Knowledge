---
title: 强网杯 2024 初赛 Writeup - S1uM4i
contest: 强网杯 2024 初赛
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [Pwn堆溢出, libc泄露, off_by_null, 魔术Gadgets, _Unwind_RaiseException, expect_number, RC4+字节交换+多层XOR, mips_emu, 自生成代码, 字节序转换, 0x23000 mmap, 魔改S盒, 异或, stack_ov, ARC4, t<<7, 16*v3, S1uM4i]
attack_chain: Pwn chat_with_me:堆溢出+off-by-null改size+魔术Gadgets劫持__free_hook或栈迁移到_Unwind_RaiseException → Pwn expect_number:发送二进制01串构造输入+爆破text base+栈溢出跳_Unwind_RaiseException → Re mips:emu中0x23000 mmap位置定位解密函数+异或验证输入 → Re remem:字节序转换+20字符分5个u32+64位无符号整数运算+自生成代码调试
key_payload: _Unwind_RaiseException栈迁移 + 魔术Gadgets劫持free_hook + RC4 swap+XOR多层 + 0x23000 mmap
one_liner: 强网杯2024初赛 S1uM4i全方向:Pwn堆溢出_Unwind_RaiseException+魔术Gadgets+RC4/异或mips_remem逆向。
lesson: Pwn利用_Unwind_RaiseException(0x4C60偏移)+魔术Gadgets(libc-2.35+0x58740 system)绕过stack check;expect_number爆破text base+栈溢出跳_Unwind_RaiseException;逆向mips_emu中0x23000 mmap位置定位解密函数;remem需自生成代码调试+字节序转换+64位无符号整数运算;RC4(b'6105t3')+swap字节+多层XOR+自实现S盒(t<<7|>>1)+16*((32*v3|v3>>3)^0xAD)。
quality: high
---
