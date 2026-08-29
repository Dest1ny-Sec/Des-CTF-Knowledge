---
title: 2024 KCTF 大赛 - 第九题《第一次接触》设计思路及解析
contest: KCTF大赛
year: 2024
difficulty: hard
vuln_type: [reverse, misc_math]
tags: [三段序列号, 四皇后问题, 反调试改乘数, 内存布局凑0x39, md5爆破, strncmp前8位]
attack_chain: 输入序列号必须 27 位（不是 24 也不是 30）→ 3 段各 9 位 → part1 头 8 位 = "hellocat" 不提第 9 位 → part2 "20211205" 反转 "50211202" * 3 = 150633606 但反调试把 3 改成 2 → 所以 part2 前面要再加 1 位 '0' → part3 "a3b1c4d29" 四皇后问题坐标 + 第 9 位 '9' 覆盖 g_serial3_verify 0x10000000 后的 0x39 → 唯一解 hellocatx202112050a3b1c4d29 → md5 校验 40d511825ecbc207eb6ef9a7b1c6e34b
key_payload: hellocatx202112050a3b1c4d29 ; md5 = 40d511825ecbc207eb6ef9a7b1c6e34b ; g_serial3_verify = 0x10000039 ; 50211202 * 3 = 150633606 ; num3_531008 = 2（反调试改）
one_liner: 27 位序列号 + 三段校验 + 四皇后 + 反调试改乘数 + md5 爆破。
lesson: 序列号长度必须是 3 倍数 + 第 9 位覆盖隔壁变量的内存布局是 KCTF 老套路。
quality: high
---
# 2024 KCTF 大赛 - 第九题《第一次接触》设计思路及解析

**出题战队**：laughlaugh
**解题战队**：tacesrever（一血 hzqmwne 用时 1h20m55s）

## 设计思路

**序列号结构**

```
hellocat x | 20211205 0 | a3b1c4d2 9
    ↑9位        ↑9位          ↑9位
```

序列号共 27 位，平均分成 3 段，**每段 9 位**（不是 8 位！这是出题人埋的第一个坑）。

**第一段 part1**

```c
BOOL verify1_45C360(char *part1) {
    to_lower_455816(part1);
    return strncmp(part1, "hellocat", 8u) == 0;  // 只比 8 位
}
```

`strncmp(part1, "hellocat", 8)` → 第 9 位不限（a-z 0-9 范围即可）。

**第二段 part2**

```c
BOOL verify2_45C400(char *part2) {
    reverse(part2);
    v3 = 0;
    for (i = 0; i < strlen(part2); i++) v3 += part2[i] - '0';
    return v3 == num13_531004 && num3_531008 * parseint(part2) == 150633606;
}
```

- `reverse("20211205") = "50211202"` → 数字和 38（每位相加）
- `parseint("50211202") * num3 = 150633606` → 50211202 * 3 = 150633606
- 但有**无声反调试**会把 `num3` 从 3 改成 2 → 必须前面再加 1 位让乘法等式成立
- 唯一解：`0` + `20211205` = `020211205`

**第三段 part3**

```c
BOOL verify3_45C500(char *part3) {
    strcpy(&gpart3_531E94, part3);
    dword_531E9C |= 0x10000000;          // 初始 0x10000000
    if (gpart3[0] >= gpart3[2]) dword |= 0x88;
    if (gpart3[2] >= gpart3[4]) dword |= 0x90;
    if (gpart3[4] >= gpart3[6]) dword |= 0xa0;
    if (!sub_458232(gpart3_0))  dword = 1;  // 全错时清 0x10
    if (!sub_458232(gpart3_2))  dword ^= 0x08;
    if (!sub_458232(gpart3_4))  dword ^= 0x10;
    if (!sub_458232(gpart3_6))  dword ^= 0x20;
    return dword == 0x10000039;
}
```

`g_serial3[8]` 与 `g_serial3_verify`（4 字节 int）内存相邻：
```
低地址 g_serial3          高地址 g_serial3_verify
[0] [1] [2] [3] [4] [5] [6] [7] | [byte0] [byte1] [byte2] [byte3]
                              ←  0x39   0x00   0x00   0x10
```

- 4 皇后坐标 `a3 b1 c4 d2` 全部正确 → dword = 0x10000000（缺 0x39）
- 4 皇后坐标全部错 → dword = 0x39（缺 0x10）
- 唯一解：让 part3 第 9 位 = `'9'`，覆盖低地址字节为 0x39

**4 皇后问题（4x4 国际象棋）**

- 解 1：`a3b1c4d2`（列行）
- 解 2：`a2b4c1d3`

最终序列号 = `hellocatx202112050a3b1c4d29`（x=第 9 位穷举 26+10=36 种）

**爆破脚本**

```python
from Crypto.Hash import MD5
serial = bytearray(b'hellocat.202112050')
target_md5 = "40d511825ecbc207eb6ef9a7b1c6e34b"
chars = b"abcdefghijklmnopqrstuvwxyz0123456789"

for i in range(36):
    serial[8] = chars[i]
    for j in range(4*4*4*4):
        n = j % 4;       r = b'a' + chr(ord('1')+n).encode()
        n = (j//4) & 3;  r += b'b' + chr(ord('1')+n).encode()
        n = (j//16) & 3; r += b'c' + chr(ord('1')+n).encode()
        n = (j//64) & 3; r += b'd' + chr(ord('1')+n).encode()
        r += b'9'
        if MD5.new(serial+r).hexdigest() == target_md5:
            print(serial+r)
            exit(0)

# bytearray(b'hellocatx202112050a3b1c4d29')
```

**反调试明细**

| 位置 | 行为 |
|------|------|
| 入口 `__CheckForDebuggerJustMyCode` | IDA/调试器检测 |
| `num3_531008` 隐式改 | 3 → 2（无声反调试） |
| 字符白名单 | `[a-z0-9]`，超范围直接 WRONG |
