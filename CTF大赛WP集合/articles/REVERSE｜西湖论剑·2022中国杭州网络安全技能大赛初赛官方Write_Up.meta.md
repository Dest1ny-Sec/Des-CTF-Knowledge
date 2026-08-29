---
title: REVERSE - 西湖论剑 2022 中国杭州网络安全技能大赛初赛官方 Write Up
contest: 西湖论剑 2022 中国杭州网络安全技能大赛 初赛
year: 2023
difficulty: high
vuln_type: misc_unknown
tags: [reverse, atexit-hook, iat-hook, base8, sha1, rc4, ebpf, uprobe, uretprobe, vma-vt, tea, mode-switch-32-64]
attack_chain:
  - 一 BabyRE: atexit 数组 6 函数顺序调用 sub_401170→1230→12b0→main→1670→15c0→14e0
  - sub_4012b0 替换 GetLastError IAT 地址为 sub_4019d0
  - flag 48 字符 = 6 位 base8 + 36 位 base8 + 6 位 base8
  - 自实现 Base8Encode/Base8Decode 字母表 0-7
  - 自实现 SHA1 (W[80] + H0..H4)
  - 双重爆破: 前 6 位 base8+sha1 验证 + 后 6 位 rc4 验证
  - 二 Berkeley: ELF64 去符号 + 数据段嵌入 BPF ELF
  - Shift+E 提取 BPF bytecode + LLVM-objdump -D 反汇编
  - ghidra eBPF 插件 + LBB0_1/LBB0_2 反编译
  - uprobe 段处理 flag + uretprobe 段二次处理 + check
  - 用户层 sub_63EA 是假 flag，真 flag 在 eBPF 段
  - 三 Dual personality: Win10 32 位 + 64 位混合代码
  - 多次 call far 切换 32/64 位 + 切换 64 后代码段改了 main
  - dump 0x4011d0/0x401200/0x401290 字节码 64 位 IDA 重分析
  - flag 32 字节 = 8 DWORD 累加 + 4 QWORD ROL 12/34/56/14 + 4 DWORD key 派生
  - 四 EasyVT: Guest.exe + EasyVT.sys 驱动
  - 启动 VT (vmxon/vmptrld/vmclear/vmptrst/vmwrite) + VMCS 设置
  - VM-Exit Handler switch case 处理不同退出码 (cpuid/rdmsr/wrmsr/xsetbv...)
  - 实际为 TEA delta=0xc95d6abf + RC4 算法 + 多次参数赋值混淆
key_payload: check1="162304651523346214431471150310701503207116032063140334661543446114434066142304661563446615430464" + check2 sha1
one_liner: 西湖论剑 2022 Reverse 官方 WP：BabyRE IAT hook + base8/sha1/rc4 三段爆破、Berkeley ELF 嵌入 eBPF uprobe/uretprobe、Dual personality 32/64 模式切换、EasyVT VT 驱动 VM-Exit Handler。
lesson: atexit 数组存储执行顺序是 Windows Reverse 入门挖法；ELF 数据段嵌入 BPF ELF 是逆向高阶技术；Win10 32/64 模式 call far 切换是反调试常见；VT VMCS Exit Handler 分析需配合 Intel SDM 卷 3 附录 C。
quality: high
---
