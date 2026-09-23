---
title: 2022 第六届强网杯青少赛 Misc & Crypto WriteUp
contest: 强网杯青少赛 2022
year: 2022
difficulty: easy
vuln_type: crypto_oracle
tags:
- base64
- 奇偶分离
- 异或32
- 大小写偏移
- NGC660安全实验室
- 入门
attack_chain:
- 读 chuyinweilai.png 文件 Base64 decode
- 字节奇偶分离交换 + zfill(2) 重组 PNG
- XOR 32 还原 FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]
- 大写字母 -31 / 小写字母 -32 解密
- 大写字母 -32 解密反向偏移
key_payload: '''cryher = "FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]"; res = chr(ord(i)^32)'''
one_liner: 入门：Base64 + 字节奇偶互换 + XOR 32 + 大小写 -31/-32 偏移。
lesson: PNG 字节奇偶互换 + zfill(2) 重组是常见 stego 套路；大小写偏移 -31/-32 区分大小写。
quality: medium
full_path: 2022第六届强网杯青少赛_Misc&Crypto-WriteUp.full.md
meta_path: 2022第六届强网杯青少赛_Misc&Crypto-WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2022 第六届强网杯青少赛 Misc & Crypto WriteUp。入门：Base64 + 字节奇偶互换 + XOR 32 + 大小写 -31/-32 偏移。。关键路径：读 chuyinweilai.png 文件 Base64 decode → 字节奇偶分离交换 + zfill(2) 重组 PNG → XOR 32 还原 FLAG[vxpsDqCElwwoClsoColwpuvlqFv...
category: crypto
subcategory: oracle
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/71039.html
reasoning_chain:
- chuyinweilai.png 文件读入 → 触发点：base64 编码字符串伪装图片
- 假设：文件内容是 base64 → 动作：base64.b64decode 还原 PNG → 观察：得到 PNG
- 观察：图片打不开 → 假设：字节被奇偶互换 → 动作：分奇偶 + zfill(2) 重组 hex → 还原 PNG
- 观察：看到 FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss] → 触发点：异或加密
- 假设：XOR 32 是常见位翻转 → 动作：chr(ord(i)^32) → 观察：还原 cryher
- 假设：cryher 还要二次偏移 → 动作：大写 -31 / 小写 -32 → 观察：得到 flag
failed_attempts:
- 试图直接 PIL.Image.open('chuyinweilai.png') → 失败：内容是 base64 文本
- 试图 base64 解码后 PIL 显示 → 失败：图片字节奇偶互换
- 试图直接 XOR 32 还原 → 失败：结果还需要大小写偏移
key_observations:
- PNG 字节奇偶互换 + zfill(2) 是 stego 常见套路
- XOR 32 是大小写翻转的快捷方式
- 大写 -31 / 小写 -32 区分大小写字母偏移
- base64 伪装图片是入门 misc 套路
prerequisites:
- base64 编码原理
- PNG 文件结构 (89 50 4E 47 magic)
- 位运算基础（XOR / >> / <<）
- Python PIL / binascii 库使用
---
# 2022第六届强网杯青少赛 Misc&Crypto-WriteUp

> 原文: https://www.ctfiot.com/71039.html
> ID: 71039

import base64f = open('chuyinweilai.png','r')content = base64.b64decode(f.read())with open('new.png','wb') as f:f.write(content)

import base64import binasciif = open('chuyinweilai.png','r')content = base64.b64decode(f.read())r = ""for i in range(0,len(content),2): #分奇偶写入文件 r += str(hex(content[i+1]))[2:].zfill(2) #这里zfill(2)很重要 一定要填充0 否则结果大相径庭 r += str(hex(content[i]))[2:].zfill(2)content = binascii.unhexlify(r)with open('new.png','wb') as f:f.write(content)

cryher = "FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]"res = ""for i in cryher: res += chr(ord(i)^32)
content = "VXPSdQceLWWOcLSOcOLWPUVLQfVVfRPOPbSS"res = "flag{"for i in content: if i.isupper(): #大写 -31 res += chr(ord(i)-31) else: #小写 -32 res += chr(ord(i)-32)res += "}"print(res.lower())

免责声明

由于传播、利用本公众号NGC660安全实验室所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，公众号NGC600安全实验室及作者不为此承担任何责任，一旦造成后果请自行承担！如有侵权烦请告知，我们会立即删除并致歉。谢谢！


```
import base64f = open('chuyinweilai.png','r')content = base64.b64decode(f.read())with open('new.png','wb') as f:f.write(content)
import base64import binasciif = open('chuyinweilai.png','r')content = base64.b64decode(f.read())r = ""for i in range(0,len(content),2): #分奇偶写入文件 r += str(hex(content[i+1]))[2:].zfill(2) #这里zfill(2)很重要 一定要填充0 否则结果大相径庭 r += str(hex(content[i]))[2:].zfill(2)content = binascii.unhexlify(r)with open('new.png','wb') as f:f.write(content)
cryher = "FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]"res = ""for i in cryher: res += chr(ord(i)^32)
content = "VXPSdQceLWWOcLSOcOLWPUVLQfVVfRPOPbSS"res = "flag{"for i in content: if i.isupper(): #大写 -31 res += chr(ord(i)-31) else: #小写 -32 res += chr(ord(i)-32)res += "}"print(res.lower())
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