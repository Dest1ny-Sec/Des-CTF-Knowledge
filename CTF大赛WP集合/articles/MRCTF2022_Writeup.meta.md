---
title: MRCTF 2022 Writeup (JPEG Huffman + AI 口罩攻击)
contest: MRCTF
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [JPEG Huffman 表, 哈夫曼解码, AI 口罩, Keras 机器学习, mutation 扰动]
attack_chain: |
  1. JPEG Huffman 表解析: ST=0x6a, L=int.from_bytes(d[ST-2:ST], 'big')-2, B=d[ST:ST+L][1:][:16] (16 个长度的码长), C=d[ST:ST+L][1:][16:] (码字)
  2. number(x) 函数: 0 替换为 . → . 替换为 1 → 1 替换为 0 → int(x, 2) 二进制转换
     - 用于把 Huffman 码长 (B) 转成实际数值
  3. DC Huffman 表 + AC Huffman 表分别解析 → DC.get(bits[st:ed]) 返回码长
  4. JPEG 数据流: 0xFF00 → 0xFF 还原 (JPEG 字节填充)
  5. bits = ''.join([bin(x)[2:].zfill(8) for x in d[ST:-2].replace(b'\xFF\x00', b'\xFF')])
  6. 完整 Huffman 解码: DC_len = DC.get(bits[st:ed]) → st, ed = ed, ed+DC_len
  7. AC 解码: m < 63, AC.get(bits[st:ed]) >> 4 是 0 的游程, & 0b1111 是码长
  8. 最后一字节 4-bit 拼成 flag: assert diff[0][:-4] in ['0', '00', '000', '0000'] → diff[0][-4:] 拼出
  9. 8 字符 (4 bit × 8) = 1 字节
 10. AI 口罩攻击 (对抗样本):
     - checkSkin(img1, img2) 检测 skin 差异
     - checkMask(img) Keras 预测 mask 概率
     - mutation() 随机扰动单像素 [-10, 10]
     - while best_score <= 0.999: 迭代找 score 更高的扰动
     - checkSkin 返回 0 → 通过
key_payload: |
  # JPEG Huffman 表解析:
  ST = 0x6a
  L = int.from_bytes(d[ST-2:ST], 'big') - 2
  B = d[ST:ST+L][1:][:16]  # 16 个码长
  C = d[ST:ST+L][1:][16:]  # 码字
  DC, AC = {}, {}
  v, n = 0, 0
  for i in range(1, 16):
      v <<= 1
      for _ in range(B[i]):
          DC[f'{v:b}'.zfill(i+1)] = C[n]
          n += 1
          v += 1
  
  # Huffman 解码:
  bits = ''.join([bin(x)[2:].zfill(8) for x in d[ST:-2].replace(b'\xFF\x00', b'\xFF')])
  st, ed = 0, 0
  while True:
      while DC.get(bits[st:ed]) is None and ed <= len(bits):
          ed += 1
      if ed > len(bits): break
      DC_len = DC.get(bits[st:ed])
      st, ed = ed, ed + DC_len
      if DC_len:
          G_0_0 = number(bits[st:ed])
          st = ed
          m = 0
          while m < 63:
              while AC.get(bits[st:ed]) is None:
                  ed += 1
              G_SET.add(bits[st:ed])
              if AC.get(bits[st:ed]) == 0:
                  st = ed
                  break
              m += AC.get(bits[st:ed]) >> 4
              AC_len = AC.get(bits[st:ed]) & 0b1111
              st = ed = ed + AC_len
              m += 1
  
  # AI 口罩扰动:
  while best_score <= 0.999:
      img = mutation(deepcopy(best_img))
      img_f = img.astype(np.float32) / 255.
      score = checkMask(img_f)
      if score > best_score:
          best_img = img
          best_score = score
one_liner: MRCTF 2022 Writeup: JPEG Huffman 手动解码 + 4-bit flag 提取 + AI 口罩对抗样本扰动 (checkSkin + checkMask 双重绕过)。
lesson: |
  - JPEG Huffman 表格式: 0xFF 0xC4 + 长度 + 表 ID + 16 字节码长 + 码字
  - 0xFF 0x00 字节填充 → 0xFF 还原 (JPEG 数据流)
  - 0xFF + 16 个码长 → v <<= 1 顺序分配码字
  - DC 表 + AC 表分别解析
  - AI 对抗样本: 随机单像素扰动 [-10, 10] + 迭代提升 score
  - checkSkin 颜色差异 < 10 → 通过
  - checkMask Keras 预测 > 0.999 → 戴口罩
quality: high
---

# MRCTF 2022 Writeup

> 来源: ctfiot.com 37642

## JPEG Huffman 手动解码

```python
def number(x):
    if x[0] == '0':
        x = x.replace('0', '.').replace('1', '0').replace('.', '1')
    return int(x, 2)

flag = ''
__flag = ''

for id in range(78):
    filename = f'pic/{id}.jpg'
    with open(filename, 'rb') as f:
        d = f.read()
    DC, AC = {}, {}
    
    # DC Huffman 表
    ST = 0x6a
    L = int.from_bytes(d[ST-2:ST], 'big') - 2
    B = d[ST:ST+L][1:][:16]
    C = d[ST:ST+L][1:][16:]
    v, n = 0, 0
    for i in range(1, 16):
        v <<= 1
        for _ in range(B[i]):
            DC[f'{v:b}'.zfill(i+1)] = C[n]
            n += 1
            v += 1
    
    # AC Huffman 表
    ST = 0x6a + L + 4
    L = int.from_bytes(d[ST-2:ST], 'big') - 2
    B = d[ST:ST+L][1:][:16]
    C = d[ST:ST+L][1:][16:]
    v, n = 0, 0
    for i in range(1, 16):
        v <<= 1
        for _ in range(B[i]):
            AC[f'{v:b}'.zfill(i+1)] = C[n]
            n += 1
            v += 1
    
    # JPEG 数据流 + 0xFF00 还原
    ST = ST + L + 0xa
    bits = ''.join([bin(x)[2:].zfill(8) for x in d[ST:-2].replace(b'\xFF\x00', b'\xFF')])
    st, ed = 0, 0
    G_SET = set()
    while True:
        while DC.get(bits[st:ed]) is None and ed <= len(bits):
            ed += 1
        if ed > len(bits): break
        DC_len = DC.get(bits[st:ed])
        st, ed = ed, ed + DC_len
        if DC_len:
            G_0_0 = number(bits[st:ed])
            st = ed
            m = 0
            while m < 63:
                while AC.get(bits[st:ed]) is None:
                    ed += 1
                G_SET.add(bits[st:ed])
                if AC.get(bits[st:ed]) == 0:
                    st = ed
                    break
                m += AC.get(bits[st:ed]) >> 4
                AC_len = AC.get(bits[st:ed]) & 0b1111
                st = ed = ed + AC_len
                m += 1
    
    # 最后一字节 4-bit 拼成 flag
    diff = list(set(list(AC.keys())) - G_SET)
    assert len(diff) == 1
    assert diff[0][:-4] in ['0', '00', '000', '0000']
    __flag += diff[0][-4:]
    if len(__flag) == 8:
        flag += chr(int(__flag, 2))
        __flag = ''
print(flag)
```

## AI 口罩攻击

```python
import cv2, numpy as np
from keras.models import load_model

model = load_model('simplenn.model')

def checkSkin(img1, img2):
    output = []
    for i in range(len(img1)):
        for j in range(len(img1[i])):
            output.append(img2[i][j] - img1[i][j])
    maxnum = 0
    for i in output:
        num = 0
        for j in i:
            if j >= 200: j = 255 - j
            num = j
        if num >= maxnum: maxnum = num
    return 0 if maxnum > 10 else 1

def checkMask(img):
    predict = model.predict(img)
    return predict[0][1]

def mutation(img):
    x = random.randint(0, 127)
    y = random.randint(0, 127)
    z = random.randint(0, 2)
    d = random.randint(-10, 10)
    img[0, x, y, z] = origin[0, x, y, z] + d
    return img

while best_score <= 0.999:
    img = mutation(deepcopy(best_img))
    img_f = img.astype(np.float32) / 255.
    score = checkMask(img_f)
    if score > best_score:
        best_img = img
        best_score = score
```

## 评价

MRCTF 2022 混合题型 writeup:
1. **JPEG Huffman 手动解码**：78 张图，每张隐藏 1 字节 flag
2. **AI 口罩攻击**：对抗样本扰动，绕过 checkSkin (颜色差 < 10) + checkMask (Keras 预测 > 0.999)

两个都是高难度题，亮点是 **JPEG 字节级手工解码** 和 **对抗样本 FGSM 简化版**（随机单像素扰动）。
