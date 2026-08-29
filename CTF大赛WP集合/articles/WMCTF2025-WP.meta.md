---
title: WMCTF 2025 WP (XMCVE-Polaris, 星盟安全团队)
contest: WMCTF 2025
year: 2025
difficulty: hard
vuln_type: web_unknown
tags: [bpf_array, map_free_overwrite, array_of_map_spray, task_struct_arbitrary_rw, kernel_ret2usr, 32d_lattice, bkz22_submod, mt19937_624_brute, pdfminer_pickle_rce, gzip_polyglot, shellcode_in_pdf, split_master]
attack_chain: BPF:write_cmd 0x159*2=0x2b2 越界淹下一个 bpf_array 前 2 字节→map_lookup_elem=map_free→堆喷 array_of_map→read_cmd 泄 ops 前 4 字节→内核基地址→劫持 index_mask/max_entries/value_size 越界改 task_struct 提权 / LFSR:32 元子集和 BKZ-22 + split_master 重组 6 段 512 bit → 32 维 LLL + 10 维格爆破 / pdfminer:CMapDB._load_data pickle.loads + gzip 双成员 polyglot (pickle + PDF) / Flask MT19937:收集 624 个 getrandbits(32) 恢复内部状态预测 key2
key_payload: 0x150+0x159*2=0x402 bpf 越界 / split_master(B_decimal, segment_bits) / MT19937Predictor.setrandbits(val, 32) / pickle.dumps(Exploit()) + gzip 双成员
one_liner: WMCTF 2025 星盟安全团队 XMCVE-Polaris 第 6 名杂烩 WP，BPF 内核利用 + LFSR 子集和 + pdfminer pickle RCE + Flask MT19937 状态恢复，多题型覆盖。
lesson: gzip 双成员 polyglot 是 PDF+pickle 联动 RCE 的经典技巧；MT19937 收集 624 个 32-bit 输出即可恢复内部状态。
quality: high
---
