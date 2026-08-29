---
title: 看雪2023 KCTF年度赛 | 第六题·至暗时刻-设计思路及解析
contest: 看雪2023 KCTF年度赛
year: 2023
difficulty: medium
vuln_type: reverse
tags: [数独, TLS回调反调试, IsDebuggerPresent, NtQueryInformationProcess 0x7, CheckRemoteDebuggerPresent, syscall下断点, 字符串异或解密, kctf拼接]
attack_chain: patch掉TLS回调IsDebuggerPresent/NtQueryInformationProcess 0x7→patch CheckRemoteDebuggerPresent→input头尾拼接字符串+kctf头→异或解密明文→sub_7FF61D223529/sub_7FF61D222E4E/sub_7FF61D222A8E三函数→sub_7FF61D222A10核心syscall下断点查看参数
key_payload: "TLS回调反调试;IsDebuggerPresent跳转patch;NtQueryInformationProcess 0x7;CheckRemoteDebuggerPresent;syscall下断点查寄存器;头部3201382652D139C0E22132DF...尾部6771165753...;kctf"
one_liner: KCTF2023年度赛Q6《至暗时刻》数独+3层反调试+syscall系统调用断点查参数
lesson: TLS回调+CheckRemoteDebuggerPresent多层反调试；syscall下断点查寄存器参数
quality: high
---

# 看雪2023 KCTF年度赛 | 第六题·至暗时刻-设计思路及解析

**赛事**：看雪2023 KCTF年度赛 Q6《至暗时刻》

**难度**：11队破解

**题目设计**：
- 涉及数独（9x9含-1的初始+完整解）
- 字符串异或解密
- 3层反调试
- syscall系统调用

**赛题解析**：

**Step 1：过反调试**

**TLS回调1**：IsDebuggerPresent
- 跳转patch掉 → 改为jmp
- 不管结果如何都不进入if

**TLS回调2**：NtQueryInformationProcess 0x7
- 功能码0x7查调试器信息
- if跳转改为jmp

**Step 2：sub_7FF61D221450 反调试**
- CheckRemoteDebuggerPresent
- 跳转改jmp绕过

**Step 3：字符串处理**
- 内置字符串异或解密
- 头尾拼接字符串：
  - 头部：`3201382652D139C0E22132DF1BC2212EA0991650A229B36436823D0B13D51E6`
  - 尾部：`677116575313142309154604431859253431473963507533496829080645035455771774602058076430276921790210013736267644383505517280`
  - 最头部再拼：`kctf`

**Step 4：3个相似函数**
- sub_7FF61D223529
- sub_7FF61D222E4E
- sub_7FF61D222A8E
- 都很类似

**Step 5：核心函数sub_7FF61D222A10**
- 函数指针处理 + syscall系统调用
- **syscall下断点** → 根据syscall函数原型查看寄存器参数

**题中包含数独**（部分解）：
```
{8, -1, -1, -1, -1, -1, -1, -1, -1},
{-1, -1, 3, 6, -1, -1, -1, -1, -1},
{-1, 7, -1, -1, 9, -1, 2, -1, -1},
{-1, 5, -1, -1, -1, 7, -1, -1, -1},
{-1, -1, -1, -1, 4, 5, 7, -1, -1},
{-1, -1, -1, 1, -1, -1, -1, 3, -1},
{-1, -1, 1, -1, -1, -1, -1, 6, 8},
{-1, -1, 8, 5, -1, -1, -1, 1, -1},
{-1, 9, -1, -1, -1, -1, 4, -1, -1}
```

**完整数独解**：
```
{8, 1, 2, 7, 5, 3, 6, 4, 9},
{9, 4, 3, 6, 8, 2, 1, 7, 5},
{6, 7, 5, 4, 9, 1, 2, 8, 3},
{1, 5, 4, 2, 3, 7, 8, 9, 6},
{3, 6, 9, 8, 4, 5, 7, 2, 1},
{2, 8, 7, 1, 6, 9, 5, 3, 4},
{5, 2, 1, 9, 7, 4, 3, 6, 8},
{4, 3, 8, 5, 2, 6, 9, 1, 7},
{7, 9, 6, 3, 1, 8, 4, 5, 2}
```

**核心技术**：
- 3层反调试：TLS IsDebuggerPresent + NtQueryInformationProcess 0x7 + CheckRemoteDebuggerPresent
- 字符串异或解密
- syscall下断点 + 寄存器参数
- 数独完整解
- kctf字符串头

**质量评估**：高（3层反调试 + syscall断点 + 完整数独解）
