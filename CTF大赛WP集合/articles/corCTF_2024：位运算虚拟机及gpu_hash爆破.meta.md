---
title: corCTF 2024：位运算虚拟机及 gpu hash 爆破
contest: corCTF
year: 2024
difficulty: hard
vuln_type: reverse
tags: [bit-vm, hasher, gpu-bruteforce, numba, cuda, 2060]
attack_chain:
  - 0x1290~0xED853 mov byte 提取位运算
  - 输入按位拆分到字节数组
  - 32 次写入识别 5 种运算 (add/and/or/xor/circular-shift)
  - 反编译 C 代码
  - numba + CUDA 7 分半跑完
  - 还原 flag
key_payload: 位运算 VM 模拟 32 位整型 + GPU 加速 hash 爆破
one_liner: corCTF 2024 逆向题，把位运算 VM 反编译为 32 位整型运算后用 GPU 跑 hash 爆破。
lesson: 当反编译工具 IDA/Ghidra 因一坨 mov byte 失败时，先识别"位运算 VM 模拟整型"模式，再反编译为 C/C++。
quality: high
---

corCTF 2024 FizzBuzz101 出题，背景：电脑被 Crowdstrike 干掉，恢复密钥被自己写的 hasher 挡住。

**初步分析**

binary 在 0x1290~0xED853 区间有一坨 `mov byte ptr [rax+x], 1/0` 指令，导致 IDA F5 main 函数失败。规律：
- 0x1290~0x136F：`mov byte [rax+x], 1`，x ∈ [0x120, 0x13F]
- 0x1370~0x16EF：`mov byte [rax+x], 0`，x ∈ [0xFA0, 0x101F]
- 0x16F0~0x1E6E：or 运算模板
- 0x1E6F~0x566E：常量赋值 (0 或 1)
- 0x566F~0x57EE：and 运算
- 0x57EF~0x59CE：xor 运算
- 0x59CF~0x5BAE：and 运算

**核心洞察**：变量按位拆分到字节，整个 0x1290~0xED854 是位运算 VM，模拟 32 位整型加/与/或/异或/循环位移 5 种运算。

**main 逻辑**

输入校验：`corctf{` 头 + `}` 尾 + `s[8]==s[17]` + `s[9]==s[11]` + `s[7]==s[16]+1` + `s[14]==s[16]+4`，把 `s[7:18]` 按位拆分到 `v3[0x940:0x998]`，最后 4 个 DWORD 要 == `0x14353CE419C603BA`。

**反编译**

每 32 次连续对非寄存器字节的写入是一次 32 位整型运算。识别方法：往数组中插入随机数据，32 次写入后取出结果，判断符合 5 种运算中的哪一种。

**GPU 爆破**

输入 11 字符(a[0]..a[10])，a[1]=a[10]、a[2]=a[4]、a[0]=a[9]+1、a[7]=a[9]+4 → 实际只需 7 字符。Python numba 调用 CUDA，笔记本 RTX 2060 跑 7 分半。坑：把逻辑都扔进核函数、别用数组(慢)、拆成单独变量。

作者是看雪论坛 `wx_御史神风`。
