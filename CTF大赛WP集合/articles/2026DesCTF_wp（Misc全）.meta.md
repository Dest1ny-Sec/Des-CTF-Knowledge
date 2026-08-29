---
title: 2026 DesCTF wp（Misc 全 - bkcrack 已知明文攻击 + zigzag 还原 + torch 模型反演 + Modbus + Shamir 秘密分享）
contest: 2026 DesCTF
year: 2026
difficulty: hard
vuln_type: [block_cipher, stego_image, ai, pwn_unknown, crypto_unknown, forensic_disk]
tags: [DesCTF 2026 Misc, bkcrack 已知明文攻击 challenge.png 89504E47 IHDR, 7z 头 37 7A BC AF 27 1C, 2D zigzag 还原 PIL, torch 加载 model.pth 提 eval_cache embedding 反演, 红外遥控器 cmd:00 15=OK/16=U/17=D/18=R/19=L 6x6 网格 ABCDEF/GHIJKL/MNOPQR/STUVWX/YZ1234/567890, Modbus func_code 8 异常响应, Shamir 秘密分享 Lagrange 插值还原 P=666c61677b..., 多文件综合取证]
attack_chain:
  - 7z 文件头 37 7A BC AF 27 1C 已知
  - bkcrack -C challenge.zip -c challenge.png -x 0 89504E47...IHDR 已知明文攻击
  - 2D zigzag PIL 反向还原
  - torch.load('model.pth') 提 eval_cache (39, 64) + embedding.weight (95, 64) → argmin 距离 → idx2char → flag
  - 红外遥控器: 提取 cmd: 0x15-0x19 字节 → 网格 6x6 → 模拟 OK 键
  - Modbus func_code==8 异常响应 crc 还原
  - Shamir: 5 份 share + P 模数 → Lagrange at zero → flag
key_payload: "bkcrack -C challenge.zip -c challenge.png -x 0 89504E470d0a1a0a0000000d49484452"
one_liner: 2026 DesCTF Misc 全：bkcrack 已知明文 + PIL zigzag + torch 模型反演 + 红外遥控 6x6 网格 + Modbus func 8 + Shamir 秘密分享 Lagrange 还原。
lesson: DesCTF 2026 Misc 集齐密码学/取证/AI 三大方向；bkcrack 是 ZIP 已知明文攻击首选工具；torch 加载 .pth 提 embedding+eval_cache 反推训练字符是 AI 攻击新套路；Shamir 秘密分享直接 Lagrange at zero 还原。
quality: high
---

# 2026 DesCTF wp（Misc 全）

## 1. bkcrack 已知明文攻击 challenge.zip

```bash
# 7z 文件头: 37 7A BC AF 27 1C
# PNG 文件头: 89504E470D0A1A0A
# 已知 challenge.png 偏移 0 是 PNG 头
bkcrack -C challenge.zip -c challenge.png -x 0 89504E470D0A1A0A0000000D49484452
# 1.zip: 5eb34ede c49019bf 815834b9
bkcrack -C 1.zip -k 5eb34ede c49019bf 815834b9 -U new.zip easy
```

## 2. 2D zigzag 还原

```python
from PIL import Image
import numpy as np

def zigzag_indices(h, w):
    result = []
    for s in range(h + w - 1):
        diag = []
        r_start = max(0, s - (w - 1))
        r_end = min(h - 1, s)
        for r in range(r_start, r_end + 1):
            c = s - r
            diag.append((r, c))
        if s % 2 == 0:
            diag.reverse()
        result.extend(diag)
    return result

def inverse_whole_image_zigzag(img_path, out_path):
    img = Image.open(img_path).convert("L")
    arr = np.array(img)
    h, w = arr.shape
    flat = arr.flatten()
    coords = zigzag_indices(h, w)
    restored = np.zeros((h, w), dtype=np.uint8)
    for i, (r, c) in enumerate(coords):
        restored[r, c] = flat[i]
    Image.fromarray(restored).save(out_path)
    return restored
```

## 3. torch 模型反演

```python
import torch
ckpt = torch.load("model.pth", map_location="cpu")
state = ckpt["model_state_dict"]
emb = state["embedding.weight"]    # [95, 64]
cache = ckpt["eval_cache"]          # [39, 64]
vocab = ckpt["vocab"]               # list[95] 或 dict

if isinstance(vocab, list):
    idx2char = {i: ch for i, ch in enumerate(vocab)}
elif isinstance(vocab, dict):
    if all(isinstance(k, int) for k in vocab.keys()):
        idx2char = vocab
    else:
        idx2char = {v: k for k, v in vocab.items()}

result = []
for vec in cache:
    dists = torch.norm(emb - vec.unsqueeze(0), dim=1)
    idx = torch.argmin(dists).item()
    result.append(idx2char[idx])
flag = "".join(result)
print(flag)
```

## 4. 红外遥控 6x6 网格

```python
# 红外命令字节 0x15-0x19 映射导航
mapping = {"15": "OK", "16": "U", "17": "D", "18": "R", "19": "L"}
nav = "".join(mapping[c] for c in cmds if c in mapping)
segments = nav.split("OK")
grid = [
    list("ABCDEF"), list("GHIJKL"), list("MNOPQR"),
    list("STUVWX"), list("YZ1234"), list("567890"),
]
# 从底部右侧开始
r, c = 5, 4
out = []
for idx, seg in enumerate(segments, 1):
    for ch in seg:
        if ch == "U": r = (r - 1) % 6
        elif ch == "D": r = (r + 1) % 6
        elif ch == "L": c = max(0, c - 1)
        elif ch == "R": c = min(5, c + 1)
        cur = grid[r][c]
        if idx == 12:  # 第 12 次确认 = 删除
            if out: out.pop()
        else:
            out.append(cur)
result = "".join(out)
print(f"Flag: flag{{{result[4:].lower()}}}")
```

## 5. Modbus func_code 8 异常响应

```python
# Modbus func_code == 8 异常响应 + 提取 crc
# ded7825ede4fd19c9f37371c37c6fa2d54e6fe2801f0df1d763175a586db1c629efa82d0f8eacb417b4419392b4a6aa8
```

## 6. Shamir 秘密分享（Lagrange 插值）

```python
from itertools import permutations

P = int("666c61677b3431e120579912cdf6831aed2476b0f3fab7c37b86a5c7b847e226a97f72f45783", 16)
SHARES = [int("4e769b2cb222e299d33ea4b89e2831e12399a6b0117336e981a567371726b3368c73f3488e18", 16), ...]

def lagrange_at_zero(xs, ys, mod):
    total = 0
    for i, xi in enumerate(xs):
        num, den = 1, 1
        for j, xj in enumerate(xs):
            if i == j: continue
            num = (num * (-xj)) % mod
            den = (den * (xi - xj)) % mod
        total = (total + ys[i] * num * pow(den, -1, mod)) % mod
    return total

def to_bytes(value):
    width = max(1, (value.bit_length() + 7) // 8)
    return value.to_bytes(width, "big")

for xs in permutations(range(1, 10), len(SHARES)):
    secret = lagrange_at_zero(xs, SHARES, P)
    blob = to_bytes(secret)
    if blob.startswith(b"flag{") and blob.endswith(b"}"):
        print(blob.decode("ascii"))
```
P 模数 = `0x666c61677b...` 以 `flag{41` 开头。
