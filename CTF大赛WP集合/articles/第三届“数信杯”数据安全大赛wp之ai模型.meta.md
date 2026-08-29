---
title: 第三届"数信杯"数据安全大赛wp之ai模型
contest: 第三届数信杯数据安全大赛
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags: [数信杯, AI模型, MultimodalMLP, 3层MLP, R通道mod10, LSB隐写, PyTorch, 27字符flag, stego]
attack_chain: 取图片左上角前20个像素R值→R mod 10得到20维特征→MultimodalMLP模型推理(20→64→32→27)→输出27个数值取整→chr()转为flag
key_payload: "MultimodalMLP:fc1=Linear(20,64) fc2=Linear(64,32) fc3=Linear(32,27) ReLU;R mod 10得20维特征;round(v.item())取整转ASCII;27字符flag"
one_liner: 第三届数信杯AI模型：图片R通道mod10提取20维特征+3层MLP推理+27字符flag
lesson: AI隐写赛=特征提取(R通道mod10)+轻量MLP推理(3层Linear+ReLU)+输出转ASCII
quality: high
---

# 第三届"数信杯"数据安全大赛wp之ai模型

**赛事**：第三届数信杯数据安全大赛（2025）

**题目**：Multimodal Steganography（多模态隐写）

**隐写规则**：
1. 图片的红色(R)通道隐藏了模型输入特征
2. 取图片左上角前20个像素的R值，计算R值 mod 10 得到20维特征
3. 20维特征输入 multimodal_model.pth 模型
4. 输出的数值取整即为 flag 的 ASCII 码
5. ASCII转字符得完整flag

**模型结构**（3层MLP + ReLU）：
```python
class MultimodalMLP(nn.Module):
    def __init__(self):
        super(MultimodalMLP, self).__init__()
        self.fc1 = nn.Linear(20, 64)   # 输入层
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 32)   # 隐藏层
        self.fc3 = nn.Linear(32, 27)   # 输出层（对应27字符flag）
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x
```

**完整解题脚本**：
```python
import torch
import torch.nn as nn
from PIL import Image

class MultimodalMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(20, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 27)
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def extract_features(image_path):
    img = Image.open(image_path).convert("RGB")
    features = []
    for y in range(20):  # 第1列前20行
        r, g, b = img.getpixel((0, y))  # x=0, y=0-19
        r_mod10 = r % 10
        features.append(r_mod10)
    return torch.tensor(features, dtype=torch.float32).unsqueeze(0)

def solve_ctf(model_path, image_path):
    # 1. 提取图片特征
    features = extract_features(image_path)
    # 2. 加载模型推理
    model = MultimodalMLP()
    state_dict = torch.load(model_path, map_location='cpu')
    model.load_state_dict(state_dict)
    model.eval()
    with torch.no_grad():
        output = model(features)
    # 3. 输出转ASCII码
    ascii_codes = [round(v.item()) for v in output[0]]
    flag = ''.join(chr(code) for code in ascii_codes)
    return features, ascii_codes, flag
```

**关键修正**：
- "左上角前20个像素"应理解为 **第1列(x=0)的前20个像素(y=0-19)**
- 不是前20个总像素
- R值取模10 (mod 10) 限定特征范围 [0, 9]

**核心技术**：
- PIL Image.getpixel提取RGB
- R通道 mod 10 特征提取
- PyTorch加载.pth模型
- model.eval() + torch.no_grad()推理
- round()取整 → chr()转ASCII

**质量评估**：高（完整MLP逆向 + 特征提取 + flag恢复）
