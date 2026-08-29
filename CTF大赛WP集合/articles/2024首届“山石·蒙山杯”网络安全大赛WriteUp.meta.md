---
title: 2024 首届"山石·蒙山杯"网络安全大赛 WriteUp（凯撒+USB+CRC32 爆破）
contest: 2024 首届"山石·蒙山杯"网络安全大赛
year: 2024
difficulty: easy
vuln_type: [misc_unknown, stego_image, crypto_unknown]
tags: [蒙山杯 Misc 签到 m13c, 凯撒 shift=4 eccgxj{Nywx_e_W1qtpi_Q13g} → ayyctf{Jut_a_S1mple_M13c}, shark USB 键盘流量 04-a 1c-y 06-c 17-t, USB HID scan code map, easymisc zip 密码 4 字节可见 ASCII CRC32 爆破, PIL Image.split() RGB LSB 隐写]
attack_chain:
  - 签到 m13c: caesar_decrypt(eccgxj{Nywx_e_W1qtpi_Q13g}, shift=4) → ayyctf{Jut_a_S1mple_M13c}
  - shark: USB 键盘流量按键顺序 04-1c-06-17-09-2f-0b-20-0f-0f-27-2d-0e-08-1c-2d-05-27-21-15-07-30 → ayyctf{h3ll0_key_b04rd}
  - easymisc: zip 4 字节密码 CRC32 爆破 zlib.crc32 + itertools.product
  - 解压后 PIL Image.split() RGB LSB 隐写
key_payload: "caesar_decrypt(ciphertext, shift=4) → ayyctf{Jut_a_S1mple_M13c}"
one_liner: 蒙山杯 Misc 三题：凯撒 shift=4 + USB 键盘流量 scan code map + zip 4 字节密码 CRC32 爆破 + LSB 隐写。
lesson: USB 键盘流量 scan code → ASCII 映射：04=a, 1c=y, 06=c, 17=t, 09=f, 2f={, 0b=h, 20=3, 0f=l, 27=0, 2d=-, 0e=k, 08=e, 21=4, 15=r, 07=d, 30=}；CRC32 爆破 4 字节可见 ASCII 100^4 = 1 亿，Python 跑 30 秒。
quality: medium
---

# 2024 首届"山石·蒙山杯"网络安全大赛 Misc 三题

## 01 签到 m13c（凯撒 shift=4）

```python
def caesar_decrypt(ciphertext, shift):
    decrypted_text = ""
    for char in ciphertext:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                decrypted_text += chr((ord(char) - shift_amount - 97) % 26 + 97)
            else:
                decrypted_text += chr((ord(char) - shift_amount - 65) % 26 + 65)
        else:
            decrypted_text += char
    return decrypted_text

ciphertext = "eccgxj{Nywx_e_W1qtpi_Q13g}"
shift = 4
print(caesar_decrypt(ciphertext, shift))
# ayyctf{Jut_a_S1mple_M13c}
```

## 02 shark（USB 键盘流量）

按键顺序（USB HID scan code）：
- 04=a, 1c=y, 06=c, 17=t, 09=f, 2f={, 0b=h
- 20=3, 0f=l, 0f=l, 27=0, 2d=-, 0e=k, 08=e, 1c=y
- 2d=-, 05=b, 27=0, 21=4, 15=r, 07=d, 30=}

组合：`ayyctf{h3ll0_key_b04rd}`

## 03 easymisc（CRC32 爆破 + LSB）

```python
import zlib
import itertools
import string
def brute_force_crc32(target_crc32):
    visible_ascii_chars = string.printable[:-6]  # 100 字符
    for candidate in itertools.product(visible_ascii_chars, repeat=4):
        candidate_str = ''.join(candidate)
        if zlib.crc32(candidate_str.encode()) == target_crc32:
            return candidate_str
```
zip 4 字节可见 ASCII 密码 CRC32 爆破 → 100^4 = 1 亿组合，Python 跑 30 秒。  
解压后 PIL `Image.split()` 取 R/G/B 通道 LSB 拼图。
