---
title: DefCamp CTF 2025 onigirl 复盘详解
contest: DefCamp CTF 2025
year: 2025
difficulty: hard
vuln_type: stego_image
tags: [pwn, rev, stb_image, pic-format, png, distance-factor, xor, privilege, modification-parameters]
attack_chain:
  - PIE+Full RELRO+Canary+NX
  - 读取图片stbi_load_from_memory
  - 计算像素到中心距离
  - 距离因子distance_factor=1.8*(1.0-d/max_distance)
  - modification_parameters_1[10]应用矩阵非线性变换
  - XOR/NOT像素引入噪声
  - privilege_value*=(R&G)&B&0xF
  - 目标privilege==4919
  - stbi__pic_test Core: 头校验 53 80 f6 34
  - stbi__pic_is4(p_n4096, "PICT") 验证
key_payload: *(double*)&modification_parameters[3*random_index] = rand()/2147483647.0*0.25+0.15
one_liner: DefCamp 2025 onigirl：stb_image魔改+PIC格式+像素距离变换
lesson: stb_image读取+随机扰动+像素距离因子是复杂图像题常见模式
quality: high
---

# DefCamp CTF 2025 onigirl 复盘详解

## 题目信息
- 比赛：DefCamp CTF 2025
- 题目：onigirl
- 类型：Pwn + Rev + Stego 混合
- 保护：Full RELRO + Canary + NX + PIE

## 关键攻击链
### 1. 程序结构
- `srand(time(0))` 随机种子
- `privilege_value = 4` 初始
- `modification_parameters_1[10]` 矩阵参数
- 读取图片大小 + 字节到 `stbi_load_from_memory`
- 计算像素到中心距离
- 距离因子 `distance_factor = 1.8 * (1.0 - d/max_distance)`
- 修改 RGB 分量

### 2. 像素变换
- 行索引奇数 → 220，偶数 → 255
- 距离因子应用到 RGB
- 随机扰动：`rand() / 2147483647.0 * 0.25 + 0.15`
- 某些像素 XOR / NOT 引入噪声

### 3. privilege 计算
```c
privilege = *privilege_pointer != 4919;
*privilege_pointer ^= (unsigned __int8)(pixel_pointer[1] & *pixel_pointer) & (unsigned __int8)pixel_pointer[2] & 0xF;
*privilege_pointer |= 7u;
*privilege_pointer &= 0x1FFFu;
final_privilege_value = *privilege_pointer;
*privilege_pointer = rand() & 0x3F | final_privilege_value;
```

### 4. 关键路径：PIC 格式
- `stbi__pic_test_core`：4 字节头校验 `53 80 f6 34`
- 跳过 0x53 字节
- `stbi__pic_is4(p_n4096, "PICT")` 验证
- 加载为 PIC 格式

### 5. 攻击点
- 修改 `modification_parameters_1[10]` 控制变换
- 注入特定 PIC 图像触发 privilege == 4919

## 评分
- quality: high（stb_image 魔改 + 像素距离因子 + 矩阵非线性 + PIC 格式头）
