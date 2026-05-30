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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773370926-wxsync-2026-03-b43b026b510a10007cbf0d0512852e63.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773370928-wxsync-2026-03-e18d81a959dbac0acdcbe43a05cf7fe1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773370930-wxsync-2026-03-94a7085d875d07294b46244f047eef2a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773370931-wxsync-2026-03-350a6a1721982687072562cf7b7d2c91.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773370933-wxsync-2026-03-93c68f58412c92faf26159a3f4fbf8fd.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773370934-wxsync-2026-03-d63b56dc1984347d2f5eab2090dde6ac.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773370936-wxsync-2026-03-2259dc981ca9233e262d6b3f2a9b7a77.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773370937-wxsync-2026-03-6dde9712c6d54f9088aa5935e82260cc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773370940-wxsync-2026-03-6b6fc0852a0f12ac1b3d66725a8062ae.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773370941-wxsync-2026-03-7655c007c8f64305284c8a34abe913f4.png)