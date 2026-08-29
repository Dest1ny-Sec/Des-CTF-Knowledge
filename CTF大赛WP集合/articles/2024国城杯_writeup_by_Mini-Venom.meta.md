---
title: 2024 国城杯 writeup by Mini-Venom
contest: 国城杯
year: 2024
difficulty: medium
vuln_type: [stego_image, stego_traffic, crypto_unknown, misc_unknown, reverse]
tags: [.264 视频隐写, np.random seed 爆破, DataMatrix 二维码, PGP wordlist 编码, shiro 反序列化, AES-ECB, AES key=oursecret]
attack_chain: 1. Tr4ffIc_w1th_Ste90: password.pacpng → 追踪 UDP 流 → hex 还原 → 改后缀 .264 → VLC 拿压缩包密码 → 解压 → 乱序图片 (np.random.shuffle 行列) → 爆破 seed → DataMatrix 二维码 → 在线扫码 → PGP wordlist 解密 / 2. Just_F0r3n51Cs: 流量包导图 → 拼接还原 → base64 → oursecret is D0g3xGC → AES-ECB 解密
key_payload: np.random.seed(seed) ; np.random.shuffle(row_indices) ; np.argsort 还原 ; PGP wordlist 'crumpled' = '44' ; AES-ECB key='oursecret is D0g3xGC' ; shiro 默认 key
one_liner: UDP .264 视频 + seed 爆破乱序图 + PGP 词表 + AES-ECB。
lesson: PGP 词表每个 2 字母/词对应 0x00-0xFF 字节；np.random.shuffle 行列只需 argsort 还原。
quality: high
---
# 2024 国城杯 writeup by Mini-Venom

## 1. Tr4ffIc_w1th_Ste90

### 步骤 1: UDP 流量还原 .264 视频

```bash
tshark -r password.pacpng -Y "udp" -T fields -e data
# 复制原始 hex → Cyberchef 转 → 改后缀 .264
vlc flag.264
# 看视频帧得压缩包密码：!t15tH3^pAs5W#RD*f0RFL@9
```

### 步骤 2: 解压后图像乱序还原

```python
import numpy as np
import cv2
import os
import sys

def decode(input_image, output_dir, seed_range):
    to_recover = cv2.imread(input_image, cv2.IMREAD_GRAYSCALE)
    to_recover_array = np.asarray(to_recover)
    for seed in seed_range:
        np.random.seed(seed)
        row_indices = list(range(to_recover_array.shape[0]))
        col_indices = list(range(to_recover_array.shape[1]))
        np.random.shuffle(row_indices)
        np.random.shuffle(col_indices)
        row_reverse = np.argsort(row_indices)
        col_reverse = np.argsort(col_indices)
        recovered_image = to_recover_array[row_reverse, :]
        recovered_image = recovered_image[:, col_reverse]
        cv2.imwrite(f"{output_dir}/recovered_seed_{seed}.png", recovered_image)

# python decode.py encoded.png ./recovered_images 0-1000
```

`np.random.shuffle` 行列 → `np.argsort` 还原 → 爆破 seed。

### 步骤 3: DataMatrix 扫码

在线扫码得：
```
5ebe4614-5544-4c1a-a7d4-d8240c8196e2
dc23c630-04bd-4801-8b70-2f5bb69246a2
b7b7fa4a-b602-43ca-801d-01f763d1f679
```

### 步骤 4: PGP 词表解码

```
crumpled chairlift freedom chisel island dashboard crucial kickoff crucial chairlift drifter classroom highchair cranky clamshell edict drainage fallout clamshell chatter chairlift goldfish chopper eyetooth endow chairlift edict eyetooth deadbolt fallout egghead chisel eyetooth cranky crucial deadbolt chatter chisel egghead chisel crumpled eyetooth clamshell deadbolt chatter chopper eyetooth classroom chairlift fallout drainage klaxon
```

```python
aaa = [
    ["00", "aardvark", "adroitness"],
    ...
    ["44", "crumpled", "designing"],
    ...
    ["FF", "Zulu", "Yucatan"]
]
def tihuan(s):
    for i in aaa:
        s = s.replace(i[1], i[0])
        s = s.replace(i[2], i[0])
    return s
bbb = tihuan(_string)  # "44 30 67 33 0C 47 43 7B..."
ccc = bbb.split(" ")
ddd = ""
for i in ccc: ddd += chr(int(i, 16))
print(ddd)
# D0g3xGC{C0N9rA7ULa710n5_Y0U_HaV3_ACH13V3D_7H15_90aL}
```

## 2. Just_F0r3n51Cs

```python
# 流量包 → 导出图片 (5ebe4614-5544-4c1a-a7d4-d8240c8196e2)
# 找到 base64: oursecret is D0g3xGC
# AES-ECB key=oursecret is D0g3xGC
# 解密得到密文
# 环境变量提示 flag2 位置
# C:\Users\D0g3xGC\flag4.zip 解 enc_png → Python 脚本还原
```

**Shiro 反序列化** + AES-ECB key 复用。
