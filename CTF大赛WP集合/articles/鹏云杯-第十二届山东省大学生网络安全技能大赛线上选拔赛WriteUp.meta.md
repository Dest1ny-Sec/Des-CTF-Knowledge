---
title: 鹏云杯 第十二届山东省大学生网络安全技能大赛 WriteUp
contest: 鹏云杯
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags: [maze-game, boss-affect, byte-XOR, ror-rotation, swap-reverse, RSA-power-4, continued-fraction, lattice-attack, Shandong-CTF]
attack_chain:
  - Reverse game 迷宫: wasd 控制 + 4 个 boss 影响 enc + 固定 key
  - byte_4020[i] += 4 + byte_4060[i] ^ byte_4020[i] = flag{Th1s_1s_My_S1mpl3_Fl4g_f0r_CTF}
  - Reverse error: 3 轮加密 + 逻辑左移 round+1 位 + 奇数反转偶数相邻交换
  - key = [0x1a,0x2b,0x3c,0x4d,0x5e,0x6f,0x70,0x81,0x92,0xa3,0xb4,0xc5,0xd6,0xe7,0xf8,0x09]
  - enc[i] = ror(enc[i], round+1) ^ key[i % 16]
  - Crypto 4 阶 RSA: n = p^4 * q^4 (p, q 256-bit), phi = (p^4-1)(q^4-1)
  - d 是 230-bit 素数, e = inverse(d, phi)
  - 用连分数 (continued fraction) 攻击恢复 p, q
  - 4 阶 RSA 不像标准 RSA, phi 多项式展开要小心
key_payload: 'byte_4020[i] += 4 + XOR + ror(enc[i], round+1) ^ key + 连分数 4 阶 RSA'
one_liner: 鹏云杯 4 题：迷宫 game 字节 XOR + 3 轮 ror+swap 加密 + 4 阶 RSA 连分数攻击。
lesson: 迷宫 + boss 影响 enc 是 CTF 出题常用套路；4 阶 RSA 分解需要连分数 + phi 多项式。
quality: high
---

# 鹏云杯 第十二届山东省大学生网络安全技能大赛 WriteUp

**来源**: ctfiot.com ID 271997
**赛事**: 鹏云杯 第十二届山东省大学生网络安全技能大赛 - 网络安全技术爱好者 - 线上选拔赛

## 1. Reverse - game (迷宫)

### 题目
- IDA 分析是迷宫游戏
- wasd 控制，遇 Boss 进入 game() 函数
- 4 个 Boss 影响 enc
- 终点调用 print_flag()

### 解法
```python
byte_4020 = [0x22, 0xc6, 0x39, 0x8e, 0xdc, 0x0b, 0x59, 0x4c, 0xfa, 0xa3,
             0x05, 0x86, 0xcf, 0x3d, 0xb7, 0x1d, 0x63, 0xac, 0x2e, 0xef,
             0x44, 0x97, 0x5c, 0x7b, 0xd2, 0x08, 0x89, 0xb9, 0x36, 0xc9,
             0x4a, 0x13, 0x9c, 0xde, 0x29, 0x6c, 0xf7, 0x53, 0x82]

byte_4060 = [0x40, 0xa6, 0x5c, 0xf5, 0x9b, 0x4b, 0x38, 0x36, 0x9b, 0xc6,
             0x7d, 0xef, 0xb7, 0x1e, 0xd9, 0x11, 0x14, 0xc3, 0x6d, 0x92,
             0x26, 0xff, 0x3f, 0x08, 0xb7, 0x60, 0xe6, 0xd8, 0x5e, 0x92,
             0x01, 0x62, 0xd4, 0xbd, 0x60, 0x11, 0x81, 0x32, 0xfb]

for i in range(len(byte_4020)):
    byte_4020[i] += 4

flag = ''
for i in range(39):
    c = byte_4060[i] ^ byte_4020[i]
    flag += chr(c) if 0x20 <= c <= 0x7E else '.'
print(flag)
# flag{Th1s_1s_My_S1mpl3_Fl4g_f0r_CTF}
```

## 2. Reverse - error (ror + swap)

### 加密
- 3 轮
- 逻辑左移 `round+1` 位
- 奇数轮: 反转数组
- 偶数轮: 相邻元素交换
- 16 字节 key XOR

### 解密
```python
def ror(b, s):
    s %= 8
    return ((b >> s) | (b << (8 - s))) & 0xFF

enc = list(bytes.fromhex('d2e7f6d2f17123532dd8996ec04d94a6912dafd6f1b37c1d264d43a91d804d63542ef89b'))
key = [0x1a,0x2b,0x3c,0x4d,0x5e,0x6f,0x70,0x81,0x92,0xa3,0xb4,0xc5,0xd6,0xe7,0xf8,0x09]

for round in range(2, -1, -1):
    if round % 2:
        enc = enc[::-1]
    else:
        for j in range(0, len(enc) - 1, 2):
            enc[j], enc[j+1] = enc[j+1], enc[j]
    for i in range(len(enc)):
        enc[i] = ror(enc[i], round + 1) ^ key[i % len(key)]
print(''.join(chr(x) for x in enc))
```

## 3. Crypto - 4 阶 RSA

### 题目
```python
nbit = 256
p = getPrime(int(nbit))
q = getPrime(int(nbit))
n = p * q
t = 4
phi = (p**4 - 1) * (q**4 - 1)
d = getPrime(int(0.9*nbit))
e = inverse(d, phi)
c = pow(bytes_to_long(flag), e, n)
```

### 攻击
- `n = p^4 × q^4` 形式
- `phi = (p^4-1)(q^4-1)`
- 用连分数 (continued fraction) 攻击恢复 p, q
- `cf(a, b)` 辗转相除生成连分数
- `convs()` 把连分数展开为 (num, den) 候选解

```python
def cf(a, b):
    r = []
    while b:
        r.append(a // b)
        a, b = b, a - b * (a // b)
    return r

def convs(cf):
    res = []
    for i in range(len(cf)):
        num, den = 1, 0
        for q in cf[i::-1]:
            num, den = q * num + den, num
        res.append((num, den))
    return res
```

## 评价
鹏云杯 4 题：迷宫游戏 + ror/swap 加密 + 4 阶 RSA + 数据研判 SQL。考察多技能融合。
