---
title: [LitCTF 2023] enbase64
contest: LitCTF 2023
year: 2023
difficulty: medium
vuln_type: crypto_rsa
tags: [custom_base64_table, permutation_v3_array, base64_48_iteration_shuffle, gets_33_flag, basecheck_verify, table_recovery, base64_decode_perm_inverse, ctf_reverse, low_quality_text]
attack_chain: IDA 反汇编 Source[61] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" + v5 = "9+/" + qmemcpy 后 56 字符 → gets(Str) 长度 33 → base64(Source, Str, Str1) → basecheck(Str1) 验证 → v3[65] permutation 数组迭代 48 次生成新 Source 表 → 还原 permutation 求 inverse → 查表逆 base64 解 flag
key_payload: Source = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" / v3[]={16,34,56,7,46,2,10,44,...,29} 64 元素 permutation / 48 次迭代 for i=0..47 for j=0..63 Source[j]=Destination[v3[j]]
one_liner: LitCTF 2023 enbase64 自定义 Base64 字符表 + 64 元素 permutation 数组迭代 48 次洗牌 + basecheck 验证，flag 长度 33，需逆 48 次 permutation 求原表后查表解。
lesson: 自定义 Base64 表逆向关键是"还原 permutation 数组 + 求逆映射 + 查表逆编码"；48 次迭代是 anti-brute-force 但对小型 permutation 仍可符号化求逆。
quality: low
---
