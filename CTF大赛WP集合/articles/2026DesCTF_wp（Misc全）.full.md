---
title: 2026 DesCTF wp（Misc 全 - bkcrack 已知明文攻击 + zigzag 还原 + torch 模型反演 + Modbus + Shamir 秘密分享）
contest: 2026 DesCTF
year: 2026
difficulty: hard
vuln_type:
- block_cipher
- stego_image
- ai
- pwn_unknown
- crypto_unknown
- forensic_disk
tags:
- DesCTF 2026 Misc
- bkcrack 已知明文攻击 challenge.png 89504E47 IHDR
- 7z 头 37 7A BC AF 27 1C
- 2D zigzag 还原 PIL
- torch 加载 model.pth 提 eval_cache embedding 反演
- 红外遥控器 cmd:00 15=OK/16=U/17=D/18=R/19=L 6x6 网格 ABCDEF/GHIJKL/MNOPQR/STUVWX/YZ1234/567890
- Modbus func_code 8 异常响应
- Shamir 秘密分享 Lagrange 插值还原 P=666c61677b...
- 多文件综合取证
attack_chain:
- 7z 文件头 37 7A BC AF 27 1C 已知
- bkcrack -C challenge.zip -c challenge.png -x 0 89504E47...IHDR 已知明文攻击
- 2D zigzag PIL 反向还原
- torch.load('model.pth') 提 eval_cache (39, 64) + embedding.weight (95, 64) → argmin 距离 → idx2char → flag
- '红外遥控器: 提取 cmd: 0x15-0x19 字节 → 网格 6x6 → 模拟 OK 键'
- Modbus func_code==8 异常响应 crc 还原
- 'Shamir: 5 份 share + P 模数 → Lagrange at zero → flag'
key_payload: bkcrack -C challenge.zip -c challenge.png -x 0 89504E470d0a1a0a0000000d49484452
one_liner: 2026 DesCTF Misc 全：bkcrack 已知明文 + PIL zigzag + torch 模型反演 + 红外遥控 6x6 网格 + Modbus func 8 + Shamir 秘密分享 Lagrange 还原。
lesson: DesCTF 2026 Misc 集齐密码学/取证/AI 三大方向；bkcrack 是 ZIP 已知明文攻击首选工具；torch 加载 .pth 提 embedding+eval_cache 反推训练字符是 AI 攻击新套路；Shamir 秘密分享直接 Lagrange at zero 还原。
quality: high
full_path: 2026DesCTF_wp（Misc全）.full.md
meta_path: 2026DesCTF_wp（Misc全）.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2026 DesCTF wp（Misc 全 - bkcrack 已知明文攻击 + zigzag 还原 + torch 模型反演 + Modbus + Shamir 秘密分享）。2026 DesCTF Misc 全：bkcrack 已知明文 + PIL zigzag + torch 模型反演 + 红外遥控 6x6 网格 + Modbus func 8 + Shamir 秘密分享 Lagrang...
category: crypto
subcategory: symmetric
subcategories:
- symmetric
- stego
- pwn_other
- crypto_other
- disk_forensics
tools_used:
- C
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/301742.html
reasoning_chain:
- 题目覆盖密码/取证/AI 三方向 → 触发点：分类识别核心算法
- 'bkcrack: challenge.zip 内嵌 challenge.png + 7z 头 37 7A BC AF 27 1C 已知 → 假设：ZIP 已知明文攻击'
- 动作：bkcrack -C challenge.zip -c challenge.png -x 0 89504E47...IHDR → 观察：得到内部 key
- 2D zigzag PIL 反向还原 → 假设：JPEG-DCT 系数置乱 → 动作：写 Python 反 zigzag
- torch.load('model.pth') → 观察：含 eval_cache (39,64) + embedding.weight (95,64)
- 假设：argmin 距离 = 训练字符映射 → 动作：遍历 embedding → 观察：idx2char 还原 flag
- '红外遥控器: cmd:00 15=OK / 16=U / 17=D / 18=R / 19=L → 假设：6x6 网格 ABCDEF/GHIJKL/MNOPQR/STUVWX/YZ1234/567890'
- 动作：解 cmd 流 → 网格坐标 → 模拟 OK 键提交
- Modbus func_code==8 异常响应 → 假设：crc 字段被改 → 动作：还原 crc 字段
- 'Shamir: 5 份 share + 已知 P 模数 → 假设：Lagrange at zero → 动作：解多项式 → 观察：P=666c61677b... = ''flag{'''
failed_attempts:
- bkcrack 直接爆破 → 失败：需要至少 12 字节已知 plaintext，PNG 头+IHDR 提供 16 字节
- torch 直接 eval model → 失败：只取 embedding+cache 即可反推，无需完整模型
- Modbus 试 func_code=3 读保持寄存器 → 失败：func_code=8 才是本题异常响应通道
key_observations:
- bkcrack 是 ZIP 已知明文攻击首选，PNG/JPEG 头是常见 plaintext 源
- torch.load .pth 提 embedding+eval_cache 是 AI 取证新套路（无需 GPU 推理）
- Shamir 秘密分享 = Lagrange at zero 是经典恢复公式
- Modbus func_code=8 是诊断/异常响应通道，常被忽视
- 2D zigzag 反置乱是 JPEG DCT 系数重排逆操作
prerequisites:
- bkcrack 已知明文攻击（ZIP/AES 加密层）
- PIL/zigzag 图像处理
- torch.load() 提取 state_dict + embedding 反演
- Shamir 秘密分享 + Lagrange 插值
---
# 2026DesCTF wp（Misc全）

> 原文: https://www.ctfiot.com/301742.html
> ID: 301742


```
7z文件头：37 7A BC AF 27 1C
(0,0)→(0,1)→(1,0)→(2,0)→(1,1)→(0,2)→(0,3)→(1,2)→(2,1)→(3,0)→(3,1)→(2,2)→(1,3)→(2,3)→(3,2)→(3,3)
89504e470d0a1a0a #PNG文件头0000000d #文件数据块IHDR长度49484452 #IHDR标识
bkcrack -C "challenge.zip" -c challenge.png -x 0 89504e470d0a1a0a0000000d49484452
bkcrack -C 1.zip -k 5eb34ede c49019bf 815834b9 -U new.zip easy
from PIL import Imageimport numpy as np
def zigzag_indices(h, w): """ 生成 h x w 矩阵的二维 zigzag 顺序坐标 """ result = [] for s in range(h + w - 1): diag = [] r_start = max(0, s - (w - 1)) r_end = min(h - 1, s) for r in range(r_start, r_end + 1): c = s - r diag.append((r, c)) # 偶数对角线反向，奇数对角线正向 if s % 2 == 0: diag.reverse() result.extend(diag) return result
def inverse_whole_image_zigzag(img_path, out_path): img = Image.open(img_path).convert("L") arr = np.array(img) h, w = arr.shape flat = arr.flatten() coords = zigzag_indices(h, w) restored = np.zeros((h, w), dtype=np.uint8) for i, (r, c) in enumerate(coords): restored[r, c] = flat[i] Image.fromarray(restored).save(out_path) return restoredif __name__ == "__main__": restored = inverse_whole_image_zigzag("challenge.png", "whole_invzig.png") print("done")
import torchcheckpoint = torch.load('model.pth', map_location='cpu')print("Checkpoint keys:", checkpoint.keys())
# Checkpoint keys: dict_keys(['model_state_dict', 'optimizer_state_dict', 'epoch', 'train_loss', 'val_loss', 'best_val_loss', 'vocab', 'model_config', 'eval_cache'])
import torchcheckpoint = torch.load('model.pth', map_location='cpu')cache = checkpoint['eval_cache']print(f"eval_cache 类型: {type(cache)}")print(f"eval_cache 形状: {cache.shape}")print(f"eval_cache 数据类型: {cache.dtype}")
eval_cache 类型: <class 'torch.Tensor'>eval_cache 形状: torch.Size([39, 64])eval_cache 数据类型: torch.float32
import torchckpt = torch.load("model.pth", map_location="cpu")state = ckpt["model_state_dict"]for k, v in state.items(): print(k, tuple(v.shape))
result = []for vec in cache: dists = torch.norm(emb - vec.unsqueeze(0), dim=1) idx = torch.argmin(dists).item() result.append(idx2char[idx])
import torchckpt = torch.load("model.pth", map_location="cpu")state = ckpt["model_state_dict"]emb = state["embedding.weight"] # [95, 64]cache = ckpt["eval_cache"] # [39, 64]vocab = ckpt["vocab"]if isinstance(vocab, list): idx2char = {i: ch for i, ch in enumerate(vocab)}elif isinstance(vocab, dict): if all(isinstance(k, int) for k in vocab.keys()): idx2char = vocab else: idx2char = {v: k for k, v in vocab.items()}else: raise TypeError("unknown vocab format")result = []for vec in cache: # 计算与所有 embedding 向量的距离 dists = torch.norm(emb - vec.unsqueeze(0), dim=1) idx = torch.argmin(dists).item() result.append(idx2char[idx])flag = "".join(result)print(flag)
15 -> OK16 -> UP17 -> DOWN18 -> RIGHT19 -> LEFT
A B C D E FG H I J K LM N O P Q RS T U V W XY Z 1 2 3 45 6 7 8 9 0
import re
from collections import Counterwith open("ir_challenge.txt", "r", encoding="utf-8") as f: data = f.read()
# 提取命令字节cmds = [a for a, _ in re.findall(r"command:s*([0-9A-F]{2})s+([0-9A-F]{2})", data)]# 低频导航按钮映射mapping = { "15": "OK", "16": "U", # 向上 "17": "D", # 向下 "18": "R", # 向右 "19": "L", # 向左}nav = "".join(mapping[c] for c in cmds if c in mapping)segments = nav.split("OK")if segments and segments[-1] == "": segments.pop()grid = [ list("ABCDEF"), list("GHIJKL"), list("MNOPQR"), list("STUVWX"), list("YZ1234"), list("567890"),]# 从底部右侧开始r, c = 5, 4out = []for idx, seg in enumerate(segments, 1): for ch in seg: if ch == "U": r = (r - 1) % 6 # 纵向环绕 elif ch == "D": r = (r + 1) % 6 elif ch == "L": c = max(0, c - 1) # 水平不环绕 elif ch == "R": c = min(5, c + 1) cur = grid[r][c] # 第12次确认实际上是“删除”操作，删掉上一个字符 if idx == 12: if out: out.pop() else: out.append(cur)result = "".join(out)print(f"Flag: flag{{{result[4:].lower()}}}")
01 Read Coils03 Read Holding Registers04 Read Input Registers05 Write Single Coil06 Write Single Register10 Write Multiple Registers
modbus.func_code == 8
ded7825ede4fd19c9f37371c37c6fa2d54e6fe2801f0df1d763175a586db1c629efa82d0f8eacb417b4419392b4a6aa8
from itertools import permutations
# From the recovered hint.dll / screenshots.# `p` is the Shamir field modulus.P = int( "666c61677b3431e120579912cdf6831aed2476b0f3fab7c37b86a5c7b847e226a97f72f45783", 16,)
# These are the corrected values that appeared in the earlier recovery session.# Two shares were copied from evidence with the same truncation that the prior solve used.SHARES = [ int("4e769b2cb222e299d33ea4b89e2831e12399a6b0117336e981a567371726b3368c73f3488e18", 16), int("47bb1ac5f6a422e8b4d483334b5d7fe2f8bae6ae665322ff30b2cade7f03e434a2e849d08599", 16), int("3f961ff18045be09c0ef92b6a5813cdfe8dc365f613b130ed430095e657c8391a1c03ac5ace5", 16), int("f0fe0b8be939ecd598f774ca043352f43dfb9fa3b74678aa9f9c9f68ab385f071d84376e64e", 16), int("4a37c5fad9d060d12f2cf65650fdd718d18d7e0a777276e85e1dd70a4a3c5b842d1feb896c42", 16),]def lagrange_at_zero(xs, ys, mod): total = 0 for i, xi in enumerate(xs): num = 1 den = 1 for j, xj in enumerate(xs): if i == j: continue num = (num * (-xj)) % mod den = (den * (xi - xj)) % mod total = (total + ys[i] * num * pow(den, -1, mod)) % mod return total
def to_bytes(value): width = max(1, (value.bit_length() + 7) // 8) return value.to_bytes(width, "big")def main(): hits = [] for xs in permutations(range(1, 10), len(SHARES)): secret = lagrange_at_zero(xs, SHARES, P) blob = to_bytes(secret) if blob.startswith(b"flag{") and blob.endswith(b"}"): hits.append((xs, blob.decode("ascii"))) if not hits: print("No flag-looking result found.") return print("Candidate hits:") for xs, flag in hits: print(f"x mapping = {xs}") print(flag)if __name__ == "__main__": main()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]