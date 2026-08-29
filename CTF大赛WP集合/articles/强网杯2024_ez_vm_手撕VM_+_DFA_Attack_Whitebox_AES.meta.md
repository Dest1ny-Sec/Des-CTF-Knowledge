---
title: 强网杯2024 ez_vm 手撕VM + DFA Attack Whitebox AES
contest: 强网杯2024
year: 2024
difficulty: hard
vuln_type: reverse
tags: [手撕VM, 自定义VM, tzcnt指令, push_8/16/32/64, 白盒AES, DFA, Differential_Fault_Analysis, 故障分析, 字节码格式, 0x08开头格式, chal.exe, 3766323862633565, 魔改TEA, Inline_hook, 寄存器vm]
attack_chain: 静态分析chal.exe → switch+tzcnt指令调度发现自定义VM → 0x08 0x20 0x00格式字节码 → push_8/16/32/64/pop_64/pop_32/mov reg imm/mov reg [reg]等指令集还原 → 提取AES密钥用白盒+DFA差分故障分析 → 验证密钥解魔改TEA得flag
key_payload: switch+tzcnt VM调度 + 字节码0x08 0x20格式 + DFA故障分析 + 白盒AES
one_liner: 强网杯2024 ez_vm:手撕Windows自定义VM字节码(0x08+寄存器+操作)+白盒AES DFA差分故障分析。
lesson: 自定义VM逆向:switch+tzcnt指令调度;白盒AES密钥提取可用DFA差分故障分析(注入fault观察密文差分推key);字节码格式常见0x08开头+reg+操作;Windows x64程序用push_8/16/32/64/pop_64/pop_32/mov reg,[reg];魔改TEA delta非0x9E3779B9。
quality: high
---
