---
title: [HITCTF 2022] re3 – debug_maze 详细 Writeup
contest: HITCTF 2022
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [windows_reverse, antidebug_isdebuggerpresent, call_5_flower, getprocaddress_via_sm3, tls_callback, child_debugger_debug_only_this_process, int3_exception_vm, excep_breakpoint, excep_access_violation, pusha_popa_vm, custom_exception_handler]
attack_chain: Win32 控制台 + IsDebuggerPresent + call $+5 花指令 + mul eax 两次 + PEB 找 kernel32.dll + GetProcAddress 模拟 (SM3 哈希) → TLS 回调修改字符串 + dec_xored 异或 (第 1 字节往后 ^ 第 0 字节) → 子进程 DEBUG_ONLY_THIS_PROCESS 调试父进程 + EXCEPTION_BREAKPOINT/EXCEPTION_ACCESS_VIOLATION 双异常分发 + int 3 trap 触发 → ecx/eax/ebx 三寄存器 VM pusha/popa 包裹 → 模拟执行 jnz/push/pop/mul/add/addn/store/load/cmp/jmp 11 条指令 → HITCTF2022{4311254395e7d3cf0b372d95b58325674d6117}
key_payload: call $+5; mul eax; cmp eax, 51h / sub_401D10 XOR 自解密 / DEBUG_ONLY_THIS_PROCESS / int 3 trap / excep_breakpoint: case 1=jnz 2=push 4=pop 8=correct 0x10=mul 0x20=wrong / excep_access_violation: 1=add 2=addn 4=store 8=load 0x10=cmp 0x20=jmp
one_liner: HITCTF 2022 re3 debug_maze 逆向：IsDebuggerPresent 抗反调试 + call $+5 花指令 + PEB 找 kernel32 + SM3 模拟 GetProcAddress + TLS 异或解密 + 子进程调试 + int 3 trap 三寄存器 VM 模拟。
lesson: call $+5 是经典花指令，"执行 mul 一次" 配合 PEB 找 kernel32 是 2022 流行 Win 抗反调试组合；EXCEPTION_BREAKPOINT/EXCEPTION_ACCESS_VIOLATION 双异常分发做 VM 是 2022 re3/anti-RE 标配。
quality: high
---
