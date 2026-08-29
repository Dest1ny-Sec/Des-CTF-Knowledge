---
title: 第九届御网杯网络安全大赛校级选拔赛题解
contest: 第九届御网杯
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [御网杯校选, MISC, XOR爆破, jpg分离zip, LSB, base64+base58+rot13, ASCII转换]
attack_chain: 1.ez_xor:爆破i XOR a[j]→flag→2.光隙:jpg分离zip爆破密码+hex+base64→3.折叠图纸:直接搜flag→4.ez_picture:lsb→解压→base64→5.easy_misc:ascii+base64+base58+rot13
key_payload: "XOR爆破;i in 0-255;jpg分离zip爆破密码;LSB解密码;base64+base58+rot13"
one_liner: 第九届御网杯校选MISC：XOR爆破+jpg分离zip+LSB+base64/58/rot13
lesson: MISC常考：XOR爆破+图片分离+LSB+多重编码
quality: low
---

# 第九届御网杯网络安全大赛校级选拔赛题解

**赛事**：第九届御网杯校级选拔赛（2024）

**MISC 5题**：

**1. ez_xor**：
```python
a = [0x5f, 0x55, 0x58, 0x5e, 0x42, 0x71, 0x7a, 0x6d, 0x7f,
     0x48, 0x4e, 0x5c, 0x78, 0x6a, 0x7d, 0x08, 0x01, 0x0b, 0x44]
for i in range(256):
    flag = ""
    for j in range(len(a)):
        flag = flag + chr(i ^ a[j])
    print(flag)
```

**2. 光隙中的寄生密钥**：
- jpg中分离出zip
- 爆破zip密码
- hex + base64 解密

**3. 被折叠的显影图纸**：
- 直接搜索 flag

**4. ez_picture**：
- LSB 拿到密码
- 解压图片
- 图片内有 base64 加密字符 → 解密

**5. easy_misc**：
- 转ascii → base64 → base58
- 最后 rot13 或 凯撒13

**质量评估**：低（多题基本介绍）
