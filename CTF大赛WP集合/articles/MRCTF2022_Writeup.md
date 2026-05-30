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
 # print(bits[:100])
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
```



```
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
