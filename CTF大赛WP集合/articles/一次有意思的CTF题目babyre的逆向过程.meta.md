---
title: 一次有意思的CTF题目 babyre 的逆向过程
contest: 个人赛
year: 2022
difficulty: hard
vuln_type: reverse
tags: [S-box, custom-cipher, IAT-hook, IsDebuggerPresent, virtualprotect, memcmp, anti-debug, Sangfor]
attack_chain: 1. 32 字节 flag 输入 → sub_401920 初始化 + IsDebuggerPresent 检测 + 有调试器时异或 i/2. sub_4017A0 加密 + sub_401400 memcmp vs unk_405000 32 字节/3. sub_401430 + sub_401280 16 轮计算 v8 v9 + 与 0xC7296F5E/0xD2F4B2A9 异或/4. IAT hook IsDebuggerPresent：遍历 PE 导入表 → VirtualProtect 改 RWX → 改 dword_40514C/5. 逆推 sub_401280_re 还原 flag = Sangfor{855908672599db85b370dcb}
key_payload: flag = Sangfor{855908672599db85b370dcb}  v5 = 0x68546749  v6 = 0x79685365
one_liner: babyre Windows 逆向，IAT hook IsDebuggerPresent 抗调试 + 自定义 S-box 加密 + 16 轮 XOR 计算。
lesson: 自定义 S-box 加密需要逆推 sub_401280；IAT hook 抗调试是 anti-debug 经典；VirtualProtect 改导入表绕过；32 字节 flag 输入验证。
quality: high
---

# 一次有意思的CTF题目 babyre 的逆向过程

## 概览
Windows 32 位逆向题，flag 长度 32 字节，含 anti-debug + 自定义 S-box 加密。

## main 函数
```c
int main() {
    HMODULE v3;
    int v5 = 0x68546749;
    int v6 = 0x79685365;
    char v7 = 0, v8 = 0, v9 = 0;
    sub_401C30("please input the flag:");
    sub_401C70("%s", g_flag, 33);
    v3 = GetModuleHandleA(0);
    sub_401920(v3);
    if (IsDebuggerPresent()) {
        for (i = 0; i < 32; ++i)
            g_flag[i] ^= i;
    }
    sub_4017A0(g_flag, 32, &v5, 8);
    if (sub_401400(v3))
        sub_401C30("nsuccess!");
    else
        sub_401C30("nfailed!");
}
```

## 关键函数
- `sub_401400`: `return memcmp(g_flag, &unk_405000, 0x20u) == 0;`
- 目标密文: `E8 B2 BE C7 24 2A 8C B1 2B 7A B8 36 17 78 34 91 7E 52 45 2A 6A FD E9 E4 94 CD 84 7A 79 D5 54 1E`

## IAT Hook 抗调试
```c
for (i = (_DWORD *)((char *)v5 + *(_DWORD *)((char *)v5 + *((_DWORD *)v5 + 15) + 128)); *i; i += 5) {
    v1 = (int)v5 + *i;
    v3 = (int)v5 + i[4];
    for (j = 0; *(_DWORD *)(v3 + 4 * j); ++j) {
        v2 = strcmp((const char *)v5 + *(_DWORD *)(v1 + 4 * j) + 2, "IsDebuggerPresent");
        if (!v2) {
            VirtualProtect((LPVOID)(v3 + 4 * j), 4u, 0x40u, &flOldProtect);
            *(_DWORD *)(v3 + 4 * j) = dword_40514C;
            VirtualProtect((LPVOID)(v3 + 4 * j), 4u, flOldProtect, &flOldProtect);
        }
    }
}
```

## 加密函数 sub_401280
```c
int sub_401280(int a1, int *a2, int *a3) {
    int v3, v4, v5, v6, v8, v9;
    v9 = *a2;
    v8 = *a3;
    for (i = 0; i < 16; ++i) {
        v3 = *(_DWORD *)(a1 + 4 * i) ^ v9;
        v9 = v8 ^ sub_4011D0(a1, v3);
        v8 = v3;
    }
    v4 = v9;
    v5 = v8;
    v6 = *(_DWORD *)(a1 + 64) ^ v4;
    *a2 = *(_DWORD *)(a1 + 68) ^ v5;
    *a3 = v6;
}
```

## flag
**Sangfor{855908672599db85b370dcb}**

## 经验提炼
- 自定义 S-box 加密需要逆推 sub_401280
- IAT hook 抗调试是 anti-debug 经典
- VirtualProtect 改导入表绕过
- 32 字节 flag 输入验证
- 16 轮循环 XOR + S-box 查询
- v5/v6 作为密钥
- 调试器检测时循环异或 0-31
- Windows PE 导入表遍历公式: `*((_DWORD *)v5 + 15) + 128`
- strcmp 找 "IsDebuggerPresent" 函数名
- 0xC7296F5E / 0xD2F4B2A9 是常量
