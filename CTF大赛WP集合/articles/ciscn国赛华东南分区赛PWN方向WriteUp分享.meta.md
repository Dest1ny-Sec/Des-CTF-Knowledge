---
title: ciscn 国赛华东南分区赛 PWN 方向 WriteUp 分享
contest: CISCN
year: 2023
difficulty: hard
vuln_type: pwn_unknown
tags: [ciscn, glibc-2.35, safe-linking, uaf, seccomp, vm-escape, srop]
attack_chain:
  - 栈劫持到 bss 段二次 ROP
  - 填满 tcache 触发 unsorted bin 残留
  - UAF 读 + XOR 解密还原 libc/heap
  - double-free + tcache fd 异或
  - _IO_list_all 劫持
  - SigreturnFrame 跳到 ORW
key_payload: glibc 2.35 safe-linking 异或 + _IO_list_all 攻击 + ORW 链
one_liner: CISCN 2023 华东南分区赛 7 道 PWN 复盘，覆盖栈劫持/UAF/Seccomp/SVM 多种高阶技巧。
lesson: glibc 2.35 引入的 safe-linking 异或 + _rtld_global 攻击面让 house of banana 复活；栈劫持到 bss 段做二次 ROP 是有限溢出时唯一出路。
quality: high
---

CISCN 2023 创新实践能力赛华东南分区赛 PWN 方向 7 道高质量 WP：login / notepad / dbgnote / houmt / MaskNote / ezroom / svm。

**login** — 无 Canary 无 PIE，仅 0x10 栈溢出。解题套路：第一次 read 栈溢出劫持 rbp 到 bss 段；第二次 read 借助 main 函数尾的固定写入代码段，向高地址 bss 段再写一次；二次 leave_ret 跳到 system 弹 shell。难点是 ROP 调用 puts 泄 libc 时栈空间不够，解决方案是栈劫持到 bss 段靠后位置。

**notepad** — 保护全开的 glibc 2.35 菜单。Erase 函数只清 size 不置空指针 → UAF。填满 tcache 触发 unsorted bin 残留 → 泄 libc/heap。Rewrite 要求 size 非零但 Erase 已清零 → 配合可写 0x10 字节清零实现 double free。tcache fd 需异或 (addr>>12) 绕过 safe-linking。最终劫持 _IO_list_all 走 _IO_wfile_jumps 攻击面。

**dbgnote** — 两处溢出：命令字符串 2 字节全局变量溢出 + index 1 字节栈溢出。注册了 abort 信号 handler 以 `dbg` 参数重启程序，进入调试功能任意地址读写。利用 `++--++--` 泄栈地址最后 2 字节 → 栈上布置 LD_DEBUG=all → 改 envp 指针最后 2 字节指向 LD_DEBUG=all → 触发 abort → 重启时 libc 打印调试信息泄 libc → 劫持 exit_handlers 拿 shell。

**houmt** — UAF + 异或加密的 show 函数。show 输出第 k 字节与 k+1 字节和 0xf0-1-k 字节的异或结果；由于高位为 0，从后往前两两异或即可还原。利用 glibc 缺陷：释放到 tcache 时只检查 key 字段，不检查 next chunk 的 size/prev_inuse。house of banana + SigreturnFrame 走 ORW 链。

**MaskNote** — sprintf 格式化串漏洞（Mask 由用户控制），可写 0x80 字节到栈上。

**ezroom** — 二叉排序树 + exchange 移动节点。指针未置 0 → UAF。check 函数只检测 int16_t 二字节 → 两个 chunk 地址差 0x10000 即可绕过。2.35 任意地址读写走 house of banana。

**svm** — 自定义指令集 VM，no relro 无 PIE。init_array 函数删 tmp/log.txt 后用 O_CREAT 重建；指令执行结果经 snprintf 格式化后 printf + write 到 log.txt。可控 code 缓冲区在栈上 0x640 大小。
