---
title: 2016 腾讯游戏安全技术竞赛题 PC 第一题
contest: 2016 腾讯游戏安全技术竞赛
year: 2016
difficulty: medium
vuln_type: [reverse, crypto_oracle]
tags: [腾讯游戏安全, GS Lab, MFC, GetDlgItem, base64-码表替换, 自定义加密, 加密函数, 注册机, OD, esp-trace, user32]
attack_chain: ["PE 工具看导入表：GetWindowTextA / DrawTextA / SetWindowTextA / TextOutA 等", "MFC 程序 GetDlgItem 消息循环拿控件文本（不是 GetDlgItemTextA）", "用户名长度 6-20 位，序列号长度 27 位", "encrystUsernameFirst 加密用户名：循环 16 次 (username[edx] * 0x1339E7E - &data) * edi，存到 data[0x14]", "encrystUsernameSecond 第二轮加密", "base64 自定义码表编码", "if (a&&b&&c&&d&&e) success else fail — 多个 jne 都得跳过去", "注册失败时 eax=0，成功时 eax=1", "用户名 'helloworld' 序列号 'VASdBcsKGhNDMRwPXv85%61MNQR'（最后字符 Q/R/S/T 都行）"]
key_payload: "序列号 = base64_encode(custom_table, encrypt2(encrypt1(username)))"
one_liner: 腾讯 GS Lab MFC 注册机：用户名 + 二次加密 + 自定义 base64 码表
lesson: MFC GetDlgItem 是经典消息循环；base64 码表替换是入门加密；多 jne 串联是判断结构
quality: high
---

# 2016 腾讯游戏安全技术竞赛题 PC 第一题

原文 https://www.ctfiot.com/44316.html

## 结论
- 用户名 → encrystFirst → encrystSecond → base64 编码
- 64 个字符的 base64 码表是**自定义**的

## 工具
- OD (OllyDbg)
- PE 工具
- IDA Pro（分析用）

## 还原

### MFC 文本获取
```c
// GetDlgItem 不是 GetDlgItemTextA
// 用消息循环取控件句柄
GetDlgItem(hwndDlg, IDC_USERNAME);
// 后面用 WM_GETTEXT 消息循环
```

### 用户名长度 6-20
### 序列号长度 27
### 用户名加密（第一轮）
```c
void encrystUsernameFirst(string username) {
    unsigned char data[0x14];
    memset(data, 0, 0x14);
    int eax = 0;
    int ebp = 0x1339E7E;
    int esp = (int)&data - 0x88;
    int edx = (int)&data;
    int ecx = 0;
    int edi = username.length();
    int* esi = 0;
    ebp = ebp - edx;
    while (ecx < 0x10) {
        eax = ecx;
        edx = eax % edi;
        esi = (int*)&data[ecx];
        ecx++;
        eax = username[edx];
        edx = (int)esi + ebp;
        eax = eax * edx;
        eax = eax * edi;
        (*esi) += eax;
    }
}
```

### 验证
- 输入 `helloworld`（10 字符）→ 加密 → 序列号 `VASdBcsKGhNDMRwPXv85%61MNQR`
- 最后字符 Q/R/S/T 均可（长度非 4 倍数，'*' 填充）

### 成功条件
```c
if (a && b && c && d && e) success;  // 多个 jne 都得跳
else fail;  // xor eax, eax
```

## 教学价值
- **MFC GetDlgItem** 是 Win32 经典消息循环
- **base64 码表替换** 是入门级加密
- **多 jne 串联** 是常见判断结构
- **OD ESP 栈追踪** 是 reverse 入门
- **GS Lab** 是腾讯游戏安全实验室（gslab.qq.com）

## 工具
- OD (OllyDbg)
- PE 工具
- IDA Pro
- WinHex

## flag / 序列号
- 用户名 `helloworld` → 序列号 `VASdBcsKGhNDMRwPXv85%61MNQR`（或末位 Q/R/S/T）
