---
title: 2025 KCTF 第十题《涅磐，亦是新生》设计思路及解析（VHDL GHDL + AES-256-CTR）
contest: 2025 KCTF
year: 2025
difficulty: hard
vuln_type: [reverse, hardware]
tags: [KCTF 2025 第十题 涅磐亦是新生, VHDL 硬件设计, GHDL 仿真器, AES-256-CTR, vcd 波形图, 关键字符串抹除, Frida Hook 定位关键比较, ghdl 源码逆向, 跨领域 VHDL+密码学, 嘉然今天吃什么战队 k1ee]
attack_chain:
  - 入口函数 sub_140001010 → sub_1400721F0 → sub_140081F40 → sub_140071D12 → sub_140071BA4
  - 特征字符串 "GRT is not consistent with the flags used for your design"
  - 修改 ghdl 源码，定位 vcd 三个相关函数指针
  - vcd 导出波形图 → 找关键比较位置
  - 抹除关键字符串增加识别难度
  - Frida Hook 定位关键比较
  - AES-256-CTR 解密 → xor → flag
key_payload: "Run_Through_Longjump(sub_140071B50) < 0 → 错误路径"
one_liner: 2025 KCTF 第十题 涅磐新生：VHDL 硬件设计 + GHDL 仿真器 + AES-256-CTR 加密 + 波形图分析 + Frida Hook；跨领域 VHDL+密码学综合。
lesson: VHDL/GHDL 编译后的二进制是少见的逆向题类型，ghdl 源码+波形图+字符串抹除是常见反分析手段；Frida Hook + AES-256-CTR 密文比对定位关键比较是最简路径。
quality: high
---

# 2025 KCTF 第十题《涅磐，亦是新生》设计思路及解析

## KCTF 评委团队点评

> 本题巧妙利用 VHDL 硬件设计语言与 GHDL 仿真环境，将 AES-256-CTR 加密流程隐藏在编译后的原生代码中，逆向难度适中。题目通过抹除关键字符串增加识别难度，但通过动态分析（如 Frida Hook）可定位关键比较逻辑。解题需结合硬件仿真特性（如波形分析思路）与密码学知识，最终通过异或操作还原 Flag，考察了逆向工程中的环境搭建、动态调试和跨领域学习能力。

## 设计思路

出题人：k1ee（嘉然今天吃什么战队）

关键点在于分析 ghdl 源码，修改程序体，找到时机设置 vcd 这三个相关函数指针即可。则可寻找方法设置使用 vcd 功能导出波形图，就可以找到关键位置并进行逆向了。

## 赛题解析（论坛会员 tacesrever 提供）

### 入口函数链

```
start → sub_140001010 → sub_1400721F0 → sub_140081F40 → sub_140071D12 → sub_140071BA4
```

### 关键反编译

```c
__int64 sub_140071BA4() {
    __int64 v0; // rax
    char v1; // dl
    __int64 result; // rax
    char *v3; // [rsp+20h] [rbp-18h] BYREF
    void *v4; // [rsp+28h] [rbp-10h]

    v0 = stdout();
    sub_140077F00(v0);
    v1 = sub_140057150();
    result = 0LL;
    if (!v1) {
        if (a08it[3] != 'T' || a08it[2] != 'i') {
            v3 = "GRT is not consistent with the flags used for your designerror during elaboration";
            v4 = &unk_1400CE8F8;
            sub_140078292(&v3);
        }
        sub_140076562();
        sub_140062D32();
        sub_14006DFCE();
        if (Flag_Stats) sub_14007F8E6();
        if ((int)Run_Through_Longjump(sub_140071B50) < 0) {
            v3 = "error during elaboration";
            ...
        }
    }
}
```

## 解题关键

1. **ghdl 源码分析**：VHDL 编译后二进制 → 找 vcd 三个函数指针
2. **vcd 波形图**：导出波形图找关键比较位置
3. **字符串抹除**：识别关键字符串"GRT is not consistent..."等
4. **Frida Hook**：动态 Hook 关键比较函数
5. **AES-256-CTR 解密**：VHDL 内嵌 AES-256-CTR 加密流程
6. **xor 操作还原**：最终异或操作还原 flag
