---
title: MRCTF 2022 Writeup (JPEG Huffman + AI 口罩攻击)
contest: MRCTF
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags:
- JPEG Huffman 表
- 哈夫曼解码
- AI 口罩
- Keras 机器学习
- mutation 扰动
attack_chain: '|'
key_payload: '|'
one_liner: 'MRCTF 2022 Writeup: JPEG Huffman 手动解码 + 4-bit flag 提取 + AI 口罩对抗样本扰动 (checkSkin + checkMask 双重绕过)。'
lesson: '|'
quality: high
full_path: MRCTF2022_Writeup.full.md
meta_path: MRCTF2022_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'MRCTF 2022 Writeup (JPEG Huffman + AI 口罩攻击)。MRCTF 2022 Writeup: JPEG Huffman 手动解码 + 4-bit flag 提取 + AI 口罩对抗样本扰动 (checkSkin + checkMask 双重绕过)。。经验：|'
category: misc
subcategory: misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/37642.html
reasoning_chain:
- 触发点：JPEG 文件 + Huffman 表 + AI 口罩 → 假设：JPEG 字节级修复 + 对抗样本生成双阶段
- 动作：解析 JPEG Huffman 表 ST=0x6a，L=int.from_bytes(d[ST-2:ST], 'big')-2 → B=d[ST:ST+L][1:][:16]（16 个码长）+ C=d[ST:ST+L][1:][16:]（码字）
- number(x) 函数：0→. → .→1 → 1→0 → int(x,2) → 假设：把 Huffman 码长 (B) 转成实际码字数值 → 动作：构造 DC/AC 表
- JPEG 数据流还原：0xFF00 → 0xFF（去字节填充）→ bits = ''.join(bin(x)[2:].zfill(8) for x in data) → 假设：拿到 Huffman 比特流
- 动作：DC.get(bits[st:ed]) 拿码长 + AC.get(...) >> 4 是 0 的游程, & 0b1111 是码长 → 假设：解码出 DC/AC 系数差值
- 触发点：'最后一字节 4-bit 拼成 flag' + assert diff[0][:-4] in ['0', '00', '000', '0000'] → 动作：取 diff[0][-4:] 拼字节 → 8 字符 × 4 bit = 1 字节
- AI 口罩攻击：checkSkin(img1,img2) 检 skin 差异 + checkMask(img) Keras 预测 mask 概率 → 假设：对抗样本绕过 skin 差异检测
- '动作：mutation() 单像素随机扰动 [-10,10] + while best_score <= 0.999: 迭代 → 观察：checkSkin=0 + mask 概率高 → 通过'
failed_attempts:
- 试图直接 cat JPEG 末尾 → 失败：flag 藏在 Huffman 解码后的 DC 系数差值最后一字节 4 bit
- 试图用 JPEG 标准库解码 → 失败：JPEG 文件结构被改造，标准库直接抛异常
- 试图训练 CNN 模型做 mask 检测 → 失败：题给 Keras 模型是黑盒，只能靠 mutation 扰动盲猜
key_observations:
- JPEG Huffman 表结构：ST-2 位置存长度大端序，ST 后跳过 1 字节类别，16 字节是码长 B[i]，剩余是码字 C
- DC_len = DC.get(bits[st:ed]) 是 Huffman 表反查码长的标准范式，AC.get(...) >> 4 / & 0xf 解析游程/码长
- JPEG 0xFF00 → 0xFF 是字节填充规则，bytes 流解码必先做反向替换
- 对抗样本 + Keras 黑盒 = 只能靠 mutation 单像素扰动循环爆破 score
- 8 字符 × 4 bit = 32 bit = 1 字节是位流拼接 flag 的固定套路
prerequisites:
- JPEG 文件结构（SOI/APP0/DQT/DHT/SOS/EOI marker 含义）
- Huffman 编码原理（变长码表 + 码长数组 + 码字数组）
- Keras/Python 图像处理（PIL + numpy pixel 操作）
- 对抗样本基础（mutation / FGSM / 黑盒 score 爆破）
---
# MRCTF2022 Writeup

> 原文: https://www.ctfiot.com/37642.html
> ID: 37642


```
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

 ST = 0x6a
 L = int.from_bytes(d[ST-2:ST], 'big')-2
 B = d[ST:ST+L][1:][:16]
 C = d[ST:ST+L][1:][16:]
 v, n = 0, 0
 for i in range(1, 16):
 v <<= 1
 for _ in range(B[i]):
 DC[f'{v:b}'.zfill(i+1)] = C[n]
 n += 1
 v += 1

 ST = 0x6a+L+4
 L = int.from_bytes(d[ST-2:ST], 'big')-2
 B = d[ST:ST+L][1:][:16]
 C = d[ST:ST+L][1:][16:]
 v, n = 0, 0
 for i in range(1, 16):
 v <<= 1
 for _ in range(B[i]):
 AC[f'{v:b}'.zfill(i+1)] = C[n]
 n += 1
 v += 1

 # print(DC, AC)
 ST = ST + L + 0xa
 bits = ''.join([bin(x)[2:].zfill(8)
 for x in d[ST:-2].replace(b'\xFF\x00', b'\xFF')])
 st, ed = 0, 0
 # print(bits[:
100])
 G_SET = set()
 while True:
 # print(ed, len(bits))
 while DC.get(bits[st: ed]) is None and ed <= len(bits):
 ed += 1
 # print('debug', bits[st: ed])
 if ed > len(bits):
 break
 DC_len = DC.get(bits[st: ed])
 # print(DC_len, st, ed)
 st, ed = ed, ed + DC_len
 if DC_len:
 G_0_0 = number(bits[st: ed])
 st = ed
 m = 0
 while m < 63:
 while AC.get(bits[st: ed]) is None:
 ed += 1
 # print(AC.get(bits[st: ed]), AC.get(bits[st: ed]) & 0b1111, AC.get(bits[st: ed]) >> 4)
 G_SET.add(bits[st: ed])
 if AC.get(bits[st: ed]) == 0:
 st = ed
 break
 # 0
 m += AC.get(bits[st: ed]) >> 4

 # > 0
 AC_len = AC.get(bits[st: ed]) & 0b1111
 st = ed = ed + AC_len
 m += 1
 # print(bits[st: st+100])
 diff = list(set(list(AC.keys())) - G_SET)
 assert len(diff) == 1
 assert diff[0][:-4] in ['0', '00', '000', '0000']
 __flag += diff[0][-4:]
 if len(__flag) == 8:
 flag += chr(int(__flag, 2))
 __flag = ''
 print(flag)

print(flag)
import base64
import cv2
import random
import numpy as np
from keras.models import load_model
from copy import deepcopy

model = load_model('simplenn.model')

def checkSkin(img1, img2):
 output = []
 for i in range(0, len(img1)):
 for j in range(0, len(img1[i])):
 output.append(img2[i][j]-img1[i][j])
 maxnum = 0
 for i in output:
 num = 0
 for j in i:
 if j >= 200:
 j = 255 - j
 num = j
 if num >= maxnum:
 maxnum = num
 index = i
 # print(index)
 # print(maxnum)
 if maxnum > 10:
 return 0
 else:
 return 1

def checkMask(img):
 predict = model.predict(img)
 return predict[0][1]

origin = cv2.imread('dog.bmp')
origin = np.expand_dims(origin, axis=0)
origin_f = origin.astype(np.float32) / 255.

best_img = cv2.imread('best.bmp')
best_img = np.expand_dims(best_img, axis=0)
best_score = checkMask(best_img.astype(np.float32) / 255.)

def mutation(img):
 for _ in range(1):
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
 # assert checkSkin(img[0], origin[0]) == 1
 best_img = img
 best_score = score
 print(best_score, score)
 cv2.imwrite('best.bmp', best_img[0])

# img = deepcopy(origin)

# while True:
# score = checkSkin(img, cv2.imread('dog.bmp'))
# img = cv2.resize(img, (128, 128))
# img_tensor = np.expand_dims(img, axis=0)
# img_tensor = img_tensor.astype(np.float32)
# img_tensor /= 255.
# score += checkMask(img_tensor)
# print(score)

# from pwn import *
# context(log_level='debug', os='linux')
# r = remote('82.156.190.31', 17271)

# r.sendafter(b'>', b'2')
# r.recvuntil(b'looks like\n')
# img_base64 = r.recvline()
# print(img_base64)

# r.interactive()
```
