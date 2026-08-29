---
title: D3CTF 2023 REVERSE
contest: D3CTF
year: 2023
difficulty: hard
vuln_type: reverse
tags: [nand-vm, rc4, pyd, bindiff, syscall-hooking, kernel-module, fork-pipe, z3]
attack_chain:
  - D3SKY: RC4 解密 opcode 还原 NAND VM
  - 条件断点提取 opcode 操作
  - 识别 XOR 比较模式
  - Z3 约束求解
  - D3RC4: 反编译 fork+pipe 子进程
  - 模拟递归 get_key
  - 还原 RC4 key
  - Z3 解密
  - D3RECOVER: Bindiff 合并 pyd 符号
  - XOR+add 还原
  - D3SYSCALL: 内核模块劫持 syscall_table
  - 翻译 rax 调度
key_payload: RC4 加密 opcode + NAND VM + fork/pipe 子进程 + syscall hook
one_liner: D3CTF 2023 四道逆向 WP 合集，NAND-VM / fork-pipe 套娃 / pyd Bindiff / syscall 劫持 VM。
lesson: 当 IDA/Ghidra 看到 "mov byte 一坨"、自定义 syscall、fork/pipe 套娃时，要立刻反应过来这是 VM 套娃。
quality: high
---

D3CTF 2023 四道逆向高质量 WP 集。

**D3SKY — NAND VM (32 位)**
TLS 回调改 RC4 密钥为 `YunZhiJun`，解密 74 字节 opcode（37 输入 + 37 密文）。主函数是 NAND VM：`op[p2] = ~(op[p0] & op[p1])`，所有运算（XOR/AND/OR）都用 NAND 复合。ida 条件断点抓 opcode：取 `op_addr = 0x5B4018`，打印 `op[p2] = ~(op[p0] & op[p1]) (op[p2] = ~(%d & %d))`。Z3 解 `input[i] ^ input[(i+1) % 37] ^ input[(i+2) % 37] ^ input[(i+3) % 37] == enc[i]`。flag = `A_Sin91e_InS7rUcti0N_ViRTua1_M4chin3~`。

**D3RC4 — Fork/Pipe 套娃 (64 位)**
`main` 返回 fake flag，真解密在 `_fini_array` 里的 `father()` 函数。父进程 pipe + fork 多次，递归把"奇数下标数据"写管道、"偶数下标"累加 p1 计数。子进程 `child(ffd)` 读 buf 第一个值再 fork，调 RC4 解密特定字节。`get_key(arr)` 模拟递归：取 arr[0] 加入 key，剩余 arr[i] % arr[0] != 0 的元素递归。Z3 + 复现 RC4 流程还原。最终 key = `We1c0m3_t0_d^3ctf\x03\x05\x07\x0b\x11\x13\x17\x1d\x1f`，flag = `getting_primes_with_pipes_is_awesome`。

**D3RECOVER — pyd Bindiff 还原 (64 位)**
无符号 pyd + 有符号 pyd 配套出题，Bindiff 合并后定位 `_pyx_pf_14d3recover_ver2_2check`。逻辑：`in[i] = input[i] ^ 0x23`，然后 `in[i] = ((in[i] + in[i+2]) & 0xFF) ^ 0x54` 跑 30 轮。Z3 解得 `flag{y0U_RE_Ma5t3r_0f_R3vocery!}`。

**D3SYSCALL — syscall 劫持 VM (64 位)**
main 函数前一坨"运行于主函数之前的函数"动态加载内核模块 `my_module`，从 kallsyms 拿 `sys_call_table`，写自定义操作：`v4[0x14F] = mov; v4[0x150] = ALU; v4[0x151] = push; v4[0x152] = pop; v4[0x153] = reset; v4[0x154] = check`。主程序调一坨 syscall 触发 VM。`strace -e raw=all` 抓所有 syscall 还原 rax/rdx/rsi/rdi 调度参数，翻译为 Python 助记符，Z3 求解。整题出题人公开了 https://github.com/4nsw3r123/d3syscall。
