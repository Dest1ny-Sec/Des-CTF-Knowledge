---
title: 数据安全积分争夺赛西区WP - 2.31 UAF+RC4魔改+表替换
contest: 数据安全积分争夺赛西区
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [libc-2.31_UAF, __free_hook+one_gadget, 0x508+0x38, RC4魔改, 0xd3异或, 自解密shellcode, mprotect_RWX, 表替换208EC37FD94165AB, libc-2.31, phtml上传, 数据安全, 数据加密]
attack_chain: 数据安全3:phtml上传绕过后翻文件 → 数据安全5:libc-2.31 UAF 0x508泄露libc + 0x38 tcache编辑__free_hook=one_gadget 0xe3b01 → 数据安全7:自解密shellcode(XOR 0xd3)+魔改RC4(key="103906d6c9429372"+init+4常数+t=box[i]+box[j]+15)+字典208EC37FD94165AB表替换得原文
key_payload: libc-2.31 UAF + __free_hook+one_gadget 0xe3b01 + RC4魔改+4常数+15 + 表替换
one_liner: 数据安全积分争夺赛西区WP:libc-2.31 UAF+RC4魔改+表替换。
lesson: libc-2.31 UAF经典:0x508 chunk进unsorted bin+0x38 tcache+__free_hook劫持;one_gadget 0xe3b01;自解密shellcode用XOR+RC4特征调试;RC4魔改init+4常数+exchange t=box[i]+box[j]+15;表替换208EC37FD94165AB→0123456789abcdef字典逆替换。
quality: high
---
