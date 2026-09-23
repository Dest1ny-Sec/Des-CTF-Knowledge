---
title: 第三届"数信杯"数据安全大赛wp之ai模型
contest: 第三届数信杯数据安全大赛
year: 2025
difficulty: medium
vuln_type: stego
tags:
- 数信杯
- AI模型
- MultimodalMLP
- 3层MLP
- R通道mod10
- LSB隐写
- PyTorch
- 27字符flag
- stego
attack_chain: 取图片左上角前20个像素R值→R mod 10得到20维特征→MultimodalMLP模型推理(20→64→32→27)→输出27个数值取整→chr()转为flag
key_payload: MultimodalMLP:fc1=Linear(20,64) fc2=Linear(64,32) fc3=Linear(32,27) ReLU;R mod 10得20维特征;round(v.item())取整转ASCII;27字符flag
one_liner: 第三届数信杯AI模型：图片R通道mod10提取20维特征+3层MLP推理+27字符flag
lesson: AI隐写赛=特征提取(R通道mod10)+轻量MLP推理(3层Linear+ReLU)+输出转ASCII
quality: high
full_path: 第三届“数信杯”数据安全大赛wp之ai模型.full.md
meta_path: 第三届“数信杯”数据安全大赛wp之ai模型.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: 第三届"数信杯"数据安全大赛wp之ai模型。第三届数信杯AI模型：图片R通道mod10提取20维特征+3层MLP推理+27字符flag。经验：AI隐写赛=特征提取(R通道mod10)+轻量MLP推理(3层Linear+ReLU)+输出转ASCII
category: misc
subcategory: misc_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/295618.html
reasoning_chain:
- 触发点：题目给图片+ multimodal_model.pth 3 层 MLP→假设：图片 R 通道隐写
- 动作：取左上角 20 个像素 R 值 → R mod 10 → 20 维特征→观察：得到特征向量
- 假设：模型结构 fc1(20→64)+fc2(64→32)+fc3(32→27)+ReLU→动作：torch.load state_dict→观察：模型加载成功
- 动作：特征输入 model.eval() + no_grad→观察：27 维输出
- 假设：round(v.item()) 取整→chr 转 ASCII→动作：批量 round→chr→观察：拼成 27 字符 flag
failed_attempts:
- 试图把整张图片送进模型 → 失败：模型输入是 20 维不是图像
- 试图 R/G/B 三通道都取 → 失败：题目只提 R 通道
- 试图 sigmoid 激活 → 失败：模型没有最后一层激活
key_observations:
- AI 隐写赛标准套路：R 通道 mod 10 → MLP 推理 → 输出 ASCII 取整
- 3 层 MLP (Linear+ReLU) 是轻量 CTF 模型固定模式
- torch.load + load_state_dict + model.eval() + no_grad 是推理标准 4 步
- round(v.item()) 是把浮点输出转整数的关键
prerequisites:
- PyTorch 模型加载与推理
- PIL Image 像素访问
- MLP 模型结构理解(Linear+ReLU)
- ASCII 编码与 chr/int 转换
---
# 第三届“数信杯”数据安全大赛wp之ai模型

> 原文: https://www.ctfiot.com/295618.html
> ID: 295618

题干

隐写规则提示：1. 图片的红色（R）通道中隐藏了模型输入特征；2. 取图片左上角前20个像素的R值，计算 R值 mod 10 得到20维特征；3. 20维特征输入multimodal_model.pth模型后，输出的数值取整即为flag的ASCII码；4. ASCII码转换为字符即可得到完整flag。
模型提示：- 模型为轻量全连接神经网络（MLP），仅含3层线性层+ReLU激活。

#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""CTF题目解题脚本 - Multimodal Steganography题目文件:    - secret_image.png: 包含隐藏特征的图片    - multimodal_model.pth: 训练好的神经网络模型    - stego_hint.txt: 解题提示文件解题方法:    1. 取图片左上角前20个像素的R值，计算R值mod10得到20维特征    2. 将20维特征输入MLP模型(3层线性层+ReLU)    3. 模型输出27个数值，取整后转为ASCII码    4. ASCII码转换为字符得到完整flag"""import torchimport torch.nn as nnfrom PIL import Imageclass MultimodalMLP(nn.Module):    """    题目中的MLP模型结构    - fc1: Linear(20, 64)  输入层: 20维特征 → 64维隐藏层    - fc2: Linear(64, 32)  隐藏层: 64维 → 32维    - fc3: Linear(32, 27)  输出层: 32维 → 27维(对应27个字符的flag)    - 每层线性后接ReLU激活    """    def __init__(self):        super(MultimodalMLP, self).__init__()        self.fc1 = nn.Linear(20, 64)        self.relu = nn.ReLU()        self.fc2 = nn.Linear(64, 32)        self.fc3 = nn.Linear(32, 27)    def forward(self, x):        x = self.relu(self.fc1(x))        x = self.relu(self.fc2(x))        x = self.fc3(x)        return xdef extract_features(image_path):    """    从图片中提取20维特征    修正：取第1列(x=0)前20行像素(y从0到19)的R值，计算R值mod10    注意：stego_hint.txt中的"左上角前20个像素"应理解为第1列的前20个像素    """    img = Image.open(image_path).convert("RGB")    features = []    for y in range(20):  # 取第1列的前20行        r, g, b = img.getpixel((0, y))  # x=0, y从0到19        r_mod10 = r % 10        features.append(r_mod10)    return torch.tensor(features, dtype=torch.float32).unsqueeze(0)def solve_ctf(model_path, image_path):    """    主解题函数    """    # 步骤1: 提取图片特征    features = extract_features(image_path)    # 步骤2: 加载模型并推理    model = MultimodalMLP()    state_dict = torch.load(model_path, map_location='cpu')    model.load_state_dict(state_dict)    model.eval()    with torch.no_grad():        output = model(features)    # 步骤3: 输出转ASCII码    ascii_codes = [round(v.item()) for v in output[0]]    flag = ''.join(chr(code) for code in ascii_codes)    return features, ascii_codes, flagif __name__ == "__main__":    MODEL_PATH = "../0512/multimodal_model.pth"    IMAGE_PATH = "../0512/secret_image.png"    print("=" * 70)    print(" " * 15 + "CTF题目解题 - Multimodal Steganography")    print("=" * 70)    try:        features, ascii_codes, flag = solve_ctf(MODEL_PATH, IMAGE_PATH)        print("n[步骤1] 特征提取")        print(f"  图片第1列前20个像素R值mod10: {list(features[0].numpy())}")        print("n[步骤2] 模型推理")        print(f"  模型结构: fc1(20→64) + ReLU + fc2(64→32) + ReLU + fc3(32→27)")        print(f"  输入特征维度: {features.shape}")        print(f"  输出向量: {ascii_codes}")        print("n[步骤3] ASCII解码")        print(f"  ASCII码: {ascii_codes}")        print(f"  对应字符: {[chr(c) for c in ascii_codes]}")        print("n" + "=" * 70)        print(f"  ✅ FLAG: {flag}")        print("=" * 70)    
except FileNotFoundError as e:        print(f"❌ 文件未找到: {e}")    
except Exception as e:        print(f"❌ 错误: {e}")        import traceback        traceback.print_exc()

运行结果：


```
隐写规则提示：1. 图片的红色（R）通道中隐藏了模型输入特征；2. 取图片左上角前20个像素的R值，计算 R值 mod 10 得到20维特征；3. 20维特征输入multimodal_model.pth模型后，输出的数值取整即为flag的ASCII码；4. ASCII码转换为字符即可得到完整flag。
模型提示：- 模型为轻量全连接神经网络（MLP），仅含3层线性层+ReLU激活。
#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""CTF题目解题脚本 - Multimodal Steganography题目文件:    - secret_image.png: 包含隐藏特征的图片    - multimodal_model.pth: 训练好的神经网络模型    - stego_hint.txt: 解题提示文件解题方法:    1. 取图片左上角前20个像素的R值，计算R值mod10得到20维特征    2. 将20维特征输入MLP模型(3层线性层+ReLU)    3. 模型输出27个数值，取整后转为ASCII码    4. ASCII码转换为字符得到完整flag"""import torchimport torch.nn as nnfrom PIL import Imageclass MultimodalMLP(nn.Module):    """    题目中的MLP模型结构    - fc1: Linear(20, 64)  输入层: 20维特征 → 64维隐藏层    - fc2: Linear(64, 32)  隐藏层: 64维 → 32维    - fc3: Linear(32, 27)  输出层: 32维 → 27维(对应27个字符的flag)    - 每层线性后接ReLU激活    """    def __init__(self):        super(MultimodalMLP, self).__init__()        self.fc1 = nn.Linear(20, 64)        self.relu = nn.ReLU()        self.fc2 = nn.Linear(64, 32)        self.fc3 = nn.Linear(32, 27)    def forward(self, x):        x = self.relu(self.fc1(x))        x = self.relu(self.fc2(x))        x = self.fc3(x)        return xdef extract_features(image_path):    """    从图片中提取20维特征    修正：取第1列(x=0)前20行像素(y从0到19)的R值，计算R值mod10    注意：stego_hint.txt中的"左上角前20个像素"应理解为第1列的前20个像素    """    img = Image.open(image_path).convert("RGB")    features = []    for y in range(20):  # 取第1列的前20行        r, g, b = img.getpixel((0, y))  # x=0, y从0到19        r_mod10 = r % 10        features.append(r_mod10)    return torch.tensor(features, dtype=torch.float32).unsqueeze(0)def solve_ctf(model_path, image_path):    """    主解题函数    """    # 步骤1: 提取图片特征    features = extract_features(image_path)    # 步骤2: 加载模型并推理    model = MultimodalMLP()    state_dict = torch.load(model_path, map_location='cpu')    model.load_state_dict(state_dict)    model.eval()    with torch.no_grad():        output = model(features)    # 步骤3: 输出转ASCII码    ascii_codes = [round(v.item()) for v in output[0]]    flag = ''.join(chr(code) for code in ascii_codes)    return features, ascii_codes, flagif __name__ == "__main__":    MODEL_PATH = "../0512/multimodal_model.pth"    IMAGE_PATH = "../0512/secret_image.png"    print("=" * 70)    print(" " * 15 + "CTF题目解题 - Multimodal Steganography")    print("=" * 70)    try:        features, ascii_codes, flag = solve_ctf(MODEL_PATH, IMAGE_PATH)        print("n[步骤1] 特征提取")        print(f"  图片第1列前20个像素R值mod10: {list(features[0].numpy())}")        print("n[步骤2] 模型推理")        print(f"  模型结构: fc1(20→64) + ReLU + fc2(64→32) + ReLU + fc3(32→27)")        print(f"  输入特征维度: {features.shape}")        print(f"  输出向量: {ascii_codes}")        print("n[步骤3] ASCII解码")        print(f"  ASCII码: {ascii_codes}")        print(f"  对应字符: {[chr(c) for c in ascii_codes]}")        print("n" + "=" * 70)        print(f"  ✅ FLAG: {flag}")        print("=" * 70)    
except FileNotFoundError as e:        print(f"❌ 文件未找到: {e}")    
except Exception as e:        print(f"❌ 错误: {e}")        import traceback        traceback.print_exc()
```


---
## 附图

[图片已移除]