---
title: TUCTF 2024 Writeup
contest: TUCTF
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [rot13, custom-image-format, crc8-checksum, wifi-aircrack, embrava-bello]
attack_chain:
- S = "reingvbaonetr" 字符 chr(ord(s) - 0x61 + 0x54) = rot13
- TU Image Program: 自定义 TIMG 格式 (4 byte header + width/height + RUBY tag)
- 三通道 DATR/DATG/DATB + 每行 crc8 校验和
- img.getpixel([j,i])[0] R 通道
- timg_to_jpg 解码脚本：struct.unpack('>I', data[8:12]) width
- airodump-ng + aircrack-ng 爆破 WiFi (D8:3A:DD:07:AA:5A)
- aircrack-ng -w /usr/share/wordlists/rockyou.txt
key_payload: rot13("reingvbaonetr")
one_liner: TUCTF 2024 4 题：rot13 + TIMG 自定义图像格式 + WiFi aircrack 爆破。
lesson: rot13 加密的字符串仅偏移 0x54 位 (chr(ord(c) - 0x61 + 0x54))；自研图像格式常带 crc8 行校验。
quality: medium
---
# TUCTF 2024 Writeup (4 题)

## 1. Reverse - 字符串
```python
S = "reingvbaonetr"
for s in S:
    tmp = ord(s) - 0x61
    print(chr(tmp + 0x54), end="")
```
- 字符减 0x61 加 0x54 = rot13
- "reingvbaonetr" → "ervatobnagre" 

## 2. Reverse - TU Image Program
自定义 TIMG 格式：
```python
# Header
write = [b'\x54', b'\x49', b'\x4D', b'\x47', b'\x00', b'\x01', b'\x00', b'\x02']
# width(4) + height(4) + 'RUBY'(4)
for x in w.to_bytes(4): write.append(x.to_bytes(1))
for y in h.to_bytes(4): write.append(y.to_bytes(1))
write += [b'R', b'U', b'B', b'Y']

# 三通道 DATR / DATG / DATB
for i in range(h):
    dat = [b'D', b'A', b'T', 'R']  # 实际按 R/G/B 循环
    for j in range(w):
        dat.append(img.getpixel([j,i])[0].to_bytes(1))  # R 通道
    dat.append(getCheck(dat[4:]))  # crc8
    for wa in dat: write.append(wa)
# ... G 通道 + B 通道 + DATE 结束
```

解码：
```python
def timg_to_jpg(timg_file, output_file):
    with open(timg_file, "rb") as f:
        data = f.read()
    if data[:4] != b'TIMG': raise ValueError("Invalid TIMG")
    width = int.from_bytes(data[8:12], "big")
    height = int.from_bytes(data[12:16], "big")
    if data[16:20] != b'RUBY': raise ValueError("Invalid RUBY")
    
    r_channel = np.zeros((height, width), dtype=np.uint8)
    g_channel = np.zeros((height, width), dtype=np.uint8)
    b_channel = np.zeros((height, width), dtype=np.uint8)
    
    offset = 20
    for color, channel in zip([b'DATR', b'DATG', b'DATB'], [r_channel, g_channel, b_channel]):
        for i in range(height):
            if data[offset:offset+4] != color: raise ValueError(f"Missing {color}")
            offset += 4
            for j in range(width):
                channel[i, j] = data[offset]
                offset += 1
            offset += 1  # checksum
    
    rgb_array = np.stack((r_channel, g_channel, b_channel), axis=2)
    img = Image.fromarray(rgb_array, "RGB")
    img.save(output_file, "JPEG")
```

## 3. Forensic - WiFi
```bash
airodump-ng -r dump-05.cap
aircrack-ng -w /usr/share/wordlists/rockyou.txt -b D8:3A:DD:07:AA:5A dump-05.cap
```

## 4. Misc - Misc
(未给出详细 flag)
