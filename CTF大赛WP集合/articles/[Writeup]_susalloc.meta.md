---
title: [Writeup] susalloc (backdoor-infoseciitr 2024)
contest: Backdoor-infoseciitr 2024
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags: [custom_heap_susalloc, items_data_ptrs_array, set_value_relative_offset, fast_bin_fake_chunk, cout_target_overwrite, libc_leak_via_cout, malloc_hook_overwrite_one_gadget, canary_disabled, pwn_custom_heap]
attack_chain: set_value offset 负数 0xffffffe0 任意写一字节 → malloc(0x10)+malloc(0x200)+free(0x200) unsorted bin → set_value(0, -32, 0xf0) size 覆盖 → padding 48 字节 | 触发 puts 泄 binary 0x104f0 (unsorted_bin 起始) → 多次 malloc 0x10 堆布局 + free 链到 fast_bins[2] - 0x20 → forged chunk 改 next_ptr = cout 0x100f0 → 触发 puts 泄 libc → fix cout → 改 __malloc_hook 0x30+0x20 = -0x50 偏移 → one_gadget 0xe3b01 → malloc(0x20) 触发
key_payload: set_value(idx, off, val) / off = -32 (0xffffffe0) 任意写 / forged_chunk = b'A'*16 + p64(0xf0)+p64(0x40)+p64(0x40)+p64(0x2)+p64(0x0)+p64(fast_bins-0x20) / libc_leak = read(7).split(b'|')[1] / __malloc_hook-0x30-0x20 触发
one_liner: Backdoor-infoseciitr 2024 susalloc 逆向 + 利用：自定义堆实现 + set_value 相对偏移 0xffffffe0 单字节写 + fast_bin 伪造 chunk 链接 cout + __malloc_hook 写 one_gadget 0xe3b01。
lesson: set_value(offset, value) 函数是 CTF 相对地址任意写的核心；自定义堆利用要先识别"items_data_ptrs + fast_bins + unsorted_bin"三件套偏移布局。
quality: high
---
