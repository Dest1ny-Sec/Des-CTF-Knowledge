---
title: 2024 第四届"网鼎杯"朱雀组 writeup（SMC XOR 0x42 + base24 + VMP 壳）
contest: 2024 第四届网鼎杯
year: 2024
difficulty: medium
vuln_type: [reverse, misc_unknown, crypto_unknown]
tags: [Re1 SMC XOR 0x42, idapython PatchByte, base24 自定义码表 24 字符, decode_base24 libnum.n2s, Re2 VMP 壳, svchost.exe 字符串大法, 异或解密 + 注入 svchost, 断点 check 先运行再瞬间断点绕过]
attack_chain:
  - Re1: SMC 自解密 0x600 字节 XOR 0x42，idapython PatchByte
  - Re2: VMP 加壳，字符串搜 svchost.exe + 异或解密关键函数
  - base24 码表 "4836CR7F9TXGQVWYB2JPHKDM" 24 字符，密文 4FKMKYP497G87QXHBTRJKCGM63XXCC8CDQX39TQPYFY
  - libnum.n2s 转换 + 反转 [::-1]
key_payload: "PatchByte(start+i, (Byte(start+i)+0x42)&0xff)"
one_liner: 第四届网鼎杯朱雀组 Reverse 三题：SMC XOR 0x42 + base24 自定义码表解码 + VMP 壳 svchost.exe 字符串大法。
lesson: SMC 自解密常见手法是 idapython PatchByte 跑一遍；base24/36 等自定义码表要把密文每个字符先查表得索引再按位权累加；VMP 壳直接字符串大法 + 异或解密关键函数最快。
quality: high
---

# 2024 第四届"网鼎杯"朱雀组

## Re1：SMC XOR 0x42

```python
start = 0x140003000
for i in range(0x600):
    PatchByte(start+i, (Byte(start+i)+0x42) & 0xff)
```
idapython 把 0x140003000 起 0x600 字节每个 +0x42 还原 SMC 自解密代码。

## Re2：base24 自定义码表

```python
base24_code_table = "4836CR7F9TXGQVWYB2JPHKDM"
ciphertext = "4FKMKYP497G87QXHBTRJKCGM63XXCC8CDQX39TQPYFY"
def decode_base24(ciphertext, code_table):
    temp = [code_table.index(char) for char in ciphertext if char in code_table]
    num = 0
    for i, value in enumerate(temp):
        num += value * (24 ** (len(temp) - i - 1))
    decoded_bytes = libnum.n2s(num)
    return decoded_bytes.decode('utf-8', errors='ignore')
print(decode_base24(ciphertext, base24_code_table)[::-1])
```
24 字符码表按位权 24^i 累加，再 `n2s` 转字节，`[::-1]` 反转出 flag。

## Re2：VMP 壳

VMP 加壳难脱 → 直接字符串大法搜 `svchost.exe`，发现异或解密关键函数，配合勒索病毒等字符串判断是 svchost 注入型。  
**断点 check 绕过**：先运行程序，触发解密后再瞬间断点。
