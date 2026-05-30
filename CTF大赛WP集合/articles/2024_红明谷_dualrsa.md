# 2024 红明谷 dualrsa

> 原文: https://www.ctfiot.com/172261.html
> ID: 172261

这道赛题比赛的时候没有做出来，赛后复现的时候和 1997 的群友”集思广益“后发现其实也不是很难，主要是构造字符串利用 eval 那里限制的太死了，粗略测了一下发现只有一个值是满足的，出题人真会卡啊。另外整个流程由于在换着 RSA 的参数用，所以乍一眼看过去还是有点绕的，再加上比赛时间也不多，所以最后遗憾败北。

题面

题目源代码：

from libnum import n2s, s2n, xgcd
import socketserver
from secret import flag
from Crypto.Util.number import getPrime

hint = s2n(flag)

class RSASystem:
    def __init__(self, nbits, e, inherit=None):
        self.nbits = nbits
        self.e = e
        if inherit:
            self.__pri_key = inherit.__pri_key
        else:
            self.__pri_key = self.gen_key()
            self.n = self.__pri_key[0] * self.__pri_key[1]

    def gen_key(self):
        p = getPrime(self.nbits)
        q = getPrime(self.nbits)
        phi = (p - 1) * (q - 1)
        d = xgcd(self.e, phi)[0] % phi
        return p, q, d

    def encrypt(self, m):
        if not isinstance(m, str):
            return ""
        try:
            return pow(eval(m), self.e, self.n)

        
except:
            return pow(s2n(m), self.e, self.n)

    def decrypt(self, c):
        if not isinstance(c, str):
            return None
        try:
            return pow(eval(c), self.__pri_key[2], self.n)
        
except:
            return pow(s2n(c), self.__pri_key[2], self.n)

    def restore(self, sig):
        return self.encrypt(sig)

class OuterServer:
    def __init__(self, rsa: RSASystem, inner_server):
        self.rsa = rsa
        self.inner_server = inner_server

    def get_enc(self, m):
        return str(self.inner_server.rsa.encrypt(m))

    def get_dec(self, c):
        cur = self.inner_server.rsa.decrypt(c)
        return cur % 256

    def enc(self, m):
        return str(self.rsa.encrypt(m))

    def sig(self, m):
        return self.rsa.decrypt(m)

    def restore_sig(self, cur_sig):
        return n2s(eval(self.enc(str(cur_sig)))).decode('latin')

class InnerServer:
    def __init__(self, rsa):
        self.rsa = rsa

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class EncHandler(socketserver.BaseRequestHandler):
    def handle(self):
        inner_server = InnerServer(rsa1)
        outer_server = OuterServer(rsa2, inner_server)
        flag_enc = outer_server.enc(flag)
        
        self.sendline(f"The public keys are: {outer_server.rsa.n}, {inner_server.rsa.n}")
        self.sendline("menu:n1. getFlagn2. encrypt your messagen3. decrypt your message")
        for _ in range(600):
            self.send("Please choose your option![+]")
            choice = eval(self.recv(1))
            if choice == 1:
                self.sendline(flag_enc)
            elif choice == 2:
                self.send("Input your message's sig![+]")
                cur_sig = int(self.recv())
                stored_sig = outer_server.restore_sig(cur_sig)
                message_enc = outer_server.get_enc(stored_sig)
                self.sendline(message_enc)
            elif choice == 3:
                self.send("Input your ciphertext![+]")
                cur_cipher = int(self.recv())
                cur_ans = outer_server.enc(str(outer_server.get_dec(str(cur_cipher))))
                self.sendline(cur_ans)

    def sendline(self, msg):
        self.request.sendall((msg + 'n').encode())

    def send(self, msg):
        self.request.send((msg + 'n').encode())

    def recv(self, byte=2048):
        message = self.request.recv(2048).strip().decode()
        return message[0: min(len(message), byte)]

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1213
    rsa1 = RSASystem(2048, 65537)
    rsa2 = RSASystem(2049, 83)
    print('Start serving...')
    server = ThreadedTCPServer((HOST, PORT), EncHandler)
    server.serve_forever()

题目首先给出两个模数

，对应两份 RSA： InnerServer（

），OuterServer（

）

然后提供三个功能

给出 flag 的密文

使用  OuterServer 进行加密，然后用 InnerServer 进行加密，输出

使用 InnerServer 进行解密，然后对最后一个字节用 OuterServer 进行加密，输出


```
from libnum import n2s, s2n, xgcd
import socketserver
from secret import flag
from Crypto.Util.number import getPrime

hint = s2n(flag)

class RSASystem:
    def __init__(self, nbits, e, inherit=None):
        self.nbits = nbits
        self.e = e
        if inherit:
            self.__pri_key = inherit.__pri_key
        else:
            self.__pri_key = self.gen_key()
            self.n = self.__pri_key[0] * self.__pri_key[1]

    def gen_key(self):
        p = getPrime(self.nbits)
        q = getPrime(self.nbits)
        phi = (p - 1) * (q - 1)
        d = xgcd(self.e, phi)[0] % phi
        return p, q, d

    def encrypt(self, m):
        if not isinstance(m, str):
            return ""
        try:
            return pow(eval(m), self.e, self.n)

        
except:
            return pow(s2n(m), self.e, self.n)

    def decrypt(self, c):
        if not isinstance(c, str):
            return None
        try:
            return pow(eval(c), self.__pri_key[2], self.n)
        
except:
            return pow(s2n(c), self.__pri_key[2], self.n)

    def restore(self, sig):
        return self.encrypt(sig)

class OuterServer:
    def __init__(self, rsa: RSASystem, inner_server):
        self.rsa = rsa
        self.inner_server = inner_server

    def get_enc(self, m):
        return str(self.inner_server.rsa.encrypt(m))

    def get_dec(self, c):
        cur = self.inner_server.rsa.decrypt(c)
        return cur % 256

    def enc(self, m):
        return str(self.rsa.encrypt(m))

    def sig(self, m):
        return self.rsa.decrypt(m)

    def restore_sig(self, cur_sig):
        return n2s(eval(self.enc(str(cur_sig)))).decode('latin')

class InnerServer:
    def __init__(self, rsa):
        self.rsa = rsa

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class EncHandler(socketserver.BaseRequestHandler):
    def handle(self):
        inner_server = InnerServer(rsa1)
        outer_server = OuterServer(rsa2, inner_server)
        flag_enc = outer_server.enc(flag)
        
        self.sendline(f"The public keys are: {outer_server.rsa.n}, {inner_server.rsa.n}")
        self.sendline("menu:n1. getFlagn2. encrypt your messagen3. decrypt your message")
        for _ in range(600):
            self.send("Please choose your option![+]")
            choice = eval(self.recv(1))
            if choice == 1:
                self.sendline(flag_enc)
            elif choice == 2:
                self.send("Input your message's sig![+]")
                cur_sig = int(self.recv())
                stored_sig = outer_server.restore_sig(cur_sig)
                message_enc = outer_server.get_enc(stored_sig)
                self.sendline(message_enc)
            elif choice == 3:
                self.send("Input your ciphertext![+]")
                cur_cipher = int(self.recv())
                cur_ans = outer_server.enc(str(outer_server.get_dec(str(cur_cipher))))
                self.sendline(cur_ans)

    def sendline(self, msg):
        self.request.sendall((msg + 'n').encode())

    def send(self, msg):
        self.request.send((msg + 'n').encode())

    def recv(self, byte=2048):
        message = self.request.recv(2048).strip().decode()
        return message[0: min(len(message), byte)]

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1213
    rsa1 = RSASystem(2048, 65537)
    rsa2 = RSASystem(2049, 83)
    print('Start serving...')
    server = ThreadedTCPServer((HOST, PORT), EncHandler)
    server.serve_forever()
cur_sig = int(self.recv())
stored_sig = outer_server.restore_sig(cur_sig)

def restore_sig(self, cur_sig):
    return n2s(eval(self.enc(str(cur_sig)))).decode('latin')

def enc(self, m):
    return str(self.rsa.encrypt(m))

def encrypt(self, m):
    if not isinstance(m, str):
        return ""
    try:
        return pow(eval(m), self.e, self.n)

    
except:
        return pow(s2n(m), self.e, self.n)
message_enc = outer_server.get_enc(stored_sig)

def get_enc(self, m):
    return str(self.inner_server.rsa.encrypt(m))

def encrypt(self, m):
    if not isinstance(m, str):
        return ""
    try:
        return pow(eval(m), self.e, self.n)

    
except:
        return pow(s2n(m), self.e, self.n)
from Crypto.Util.number import *
from gmpy2 import *
rce = __import__('os').system("ls") 
rce += 'xff' from Crypto.Util.number import *
from gmpy2 import *
rce = b"__import__('os').system('ls')"
rce += b'xff' * (512 - len(rce))
m = gmpy2.iroot(bytes_to_long(rce),83)[0]
print(m)
print(long_to_bytes(pow(m,83)))* (512 - len(rce))
gmpy2.iroot(bytes_to_long(rce),38)[0]
708732724968359
b'__impnx9b>x8duxa17xb2x10xc5xeauxdax91x07rx8fxd3xfcxb0xfaxf07"x81-oxfex9fx88xf5x1fxf9gxb6xecQx16x89xcb{xa5x80nxccxedxdb:
Yxe9xa5xa3xf7x15cxb4x1erxf9Ex91:
x82x1fx90xa5-8xb2fxe1xb3xa0xbax07~x977xeax0fx02x92xc0mx97xd1Yxb6xe9Hxdfxadx8fx80yxe1bxf6xb2Fxd6x03xe1 jxddxbcx16Rxe12xf2xb4x91xebxbexcfex185x8fxddxd3xdex1bOxda_srRx00xFxe1xadx0cxd3xc478faxc8xa8cxfa<rxaeox0c5xfex1cadx02xbbx11x88xfexd7xeaxf0ixf3uxe9x9ag6itKxe3xcexb2xaexdacxb9Kxaf{xddxe9xa2x16xc8xc9xb2Yxc9xb9'x1axe4xe8xb9xfdx1cxdcxa8xb0x1bx9fMx1enKxaex89x9eNxebrPx16:%xb7zx8axb8Bmx80xeexc8x8dH81#xe8.xd9x07x85xbdx1e-xaaTnxec4xbdx85xeb|x96xb5x1a%xb1*enx06xd7}xaaOxeenx03~oxbdnx03xa3xc9Ixed]SxfexbdwQx83x12Rxbfx15Oxe8xc2Hjxa6Pxfb37x12xx0fxfax9bxe0xf3Dxcbxd8x0c9xb0x08x13xd4#Bxa7x98GCxf9Ekxb6y^xffxe1Itx05xd4lxbdDx8b?Ehx90xa1"P6xdexa4>tx96x11x1ex13x87x88xba^"tx19Qx1a7xed)Mx93"/!xd2x9d Bx07xeevx19kx82xb3xd8xea3xe3xedx18xe3xd7x86fcxfdijx0b1xa0x9bw&tOxafx9bx9aDox9ex12x1bhxe6xf8x17Saxc6_:
fx19xaaxa4xe0xaexaaYx99xf9xba]x04x94xc8:
x1bjx9ckxd7>F{Dx00x9cocxdcxd7xefxd1xe1xdb3xfe?x0cxf5xb8x0cx14xa1x94Gx08x90xe9Eaxe9YW;Px91x05xa1xdaX[xf8xe0xab8Jxa6xcdxc9 xb5xd33=Gxb1xa3xadv$uxee.Bxb7$xb7'
from Crypto.Util.number import *
from gmpy2 import *
hint = 123456
rce = b"hint#"
rce += b'xff' * (512 - len(rce))
m = gmpy2.iroot(bytes_to_long(rce),83)[0]
print(m)
print(long_to_bytes(pow(m,83)))
print(eval(long_to_bytes(pow(m,83))))
709506354616988
b'hint#xfe"1xfbx1f*xb57x85x80xddxf2 Cx81dxc2Zxacxc4xa9x1bx03Yx070xe0xb5x95xee~x9fx13#X+#f|~x88fx85xaex96x89x19fxfex14xab'xb2lx9exd4Vxc3Hm}!xc9IQxf8xb4xe5Djxe3xe9x00pxedxabx1fxe0Yxb2xa5xa1xbfxb5xddx93xac&Txd6%xd7x9ax19xccxfdkGxffxb3xe3x93xf9x8cxcfIx15x01xb5x16x1d:
x92xb0hx9exa3xcfxcdOxa4N:-xa1Axcfxd0x84ixebxffx92x1d"x0cxafx88z[x05<xf06xd1xb4Crx8axbcx9fm8x96gxfb{xfax89ux01xbdx88Axccx87xf3x9a3xe1x04x94xbcxa8x00xe6x81x0exb0xf1Cxc1xb5x9axf7xa1Ox00jx10xbbx94xfb4<x94!x9dx15x96xc2x05xb3x8bxfexa0rn'x0bZxba+?xdcx8fxc9 kxf6x1dJxc3xa0xf8xxdf5xfcx97cx1fxf5xf2xd96{x1exe8Kx0exc6xd1*K2xf1x93xa4xa0x89xf0x8fx86fx1cx88xe32xc7x08&xbb_?,xd3x89xecyx1c?xf1xe5xc8xa5@Kxdccxd77;x01x97:
x8axbd/Bxa1xd8`qx1bx1977x0cxe0xebxa6amExdaxfaxd6xd2xd2xbdxedxb8xcfxa2xa7rxd1x80xe7xe7sWx93K(xd4x1f=4xf9x8exf1xf1x10rx06x89xc2b#xcbxedx96x19xb2x02x0cx01&x96J+xbfr"Axea#xde.Xx00xefxcdxbbhRx81Axc9I1xfaxb3xe6>MGB)x89x1fxc1&xb0xabx8bx1axd3)xb3x94x19Pz.Fvxe6x14xe0xe3xad>Ux0fxe8|Hxb2x85xc0-x06xcexbexa7:
xc23Cxe5x85tx11xc6^xf6xdax06xd3{x03xdfKx03x8cxefxca9Txfexc80gx86_xcax94IWx82q@xd9x07xd6xeaxc8xdbx8e\xd7x9ex88x8dx01xb6xe3,Txacxb0mx1fx1axe6kexed,$x01xf1mxc0x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00'
Traceback (most recent call last):
  File "C:
UsersjkangDesktoptest.py", line 42, in <module>
    print(eval(long_to_bytes(pow(m,83))))
ValueError: source code string cannot contain null bytes
from Crypto.Util.number import *
from gmpy2 import *

hint = 1233444

for j in range(400,507):
 tmp = bytes_to_long(b"hint#"+b'x00'*j)
 tmp2 = bytes_to_long(b"hint$"+b'x00'*j)
 floor = iroot(tmp,83)[0]
 sky = iroot(tmp2,83)[0]
 #print(floor,sky)
 for i in range(floor,sky+1):

  m = long_to_bytes(pow(i,83))
  try:
   eval(m)
   print(m)
   print("[+]",j,i)
  
except:
   pass
b'hint#Bx85xa91xd8x95xedxd4_%x13x1bVxc4xfc8x832k-xc3w"gxcexa5x17nxfexacxbeP`sx17<xb6x9ex9bx87)rkxefxd4xebxaeNEx13xeffx82rQdx06x04x1dxb2Uxd6Ixc4x01xfax1dxb3xde^+-xaex9abdxf2hxe1]4txe6@x07x12xcfx98x93xddx82'xc6xe1x10xcdx87Ex1eMmx93mrxc4xc4xee0xdexbcx1ex15yxd2xdfSj1x80x82x84|xxf0Ux19xd6x84x1bxbeQn`xcdxbbxe87Yxfax1d6x82x17xc6T+xdf.yQb&xdbxb8xa7}>'x0cxefx92xeaAx8a*Qzx8elpCxa0xdfxd8x98xbeHxe1xc4x0e8UM8yuxdb|MRM0xf6xbf0E?xa3xe6xb2x03wx93FAx8d=xfcxd1x06;xa11xa1xc8xd5&xa4xccmxe0xbaoCt#xf3x07x066ct:
x93hx80"xecxc8xf2x85x87x9cxe0-xb5wxe8x88x8ddAx87xacxddxe8xaaxfdxfbxfbx7fxd5xb6,t`x1fx82xa9xc9'pxf8x8exc3xc9xb1x8cc.xc2ifxc7xabvx10xb9"j1xa1`xeex98xf55xa8x94hxa7,Wxd0xb3%*x9cx9cxc5cxb3Xxe6cxdaxf7xdf@\Pxabxdf@xfbxadx16*x04x17b*xf6xf0xecxb1xf2&oxb1xf7xa4xe84Mx0cxcdxc5'iDxd5xbd1^xf7x0fxb0Sx8eqxbcKxf7&txa7xaaxe5xa0x11x2xcdx7fxe8Kx87x08x90Y[x02x90mxbdxabxf4xxf9xadxccYxdfVOixc2$xb69Hxa7xb2xc5xc0xb3xe0@xeexa7xcc'xf2]xe7xc9xe1 xa7xc4xdfxdexfbHxe3x8eA<T )>x97xcbx9cx86px82xb03xa5xccxcdG+dx87xafx11vx14xf5xb4Y`x93/x89`xc7xc0xd3_cBxbc/s7xb85"xfcnxc8x8cxcdxeaxaf\Qx07xf5xfb/xeaBxadxb8xd9x0bx8epm_sW|x80x15'
[+] 501 475189300601805
>> print(long_to_bytes(iroot(1105429575052088912049453038438451145102848046647844017283034044181579750804790663420352960444452892999750053625107156940415372665194489176787584483463433571159839630126953125,83)[0]))
b'}'
from pwn import *
from gmpy2 import iroot
from Crypto.Util.number import *

def lsbOracle(c):
 sh.recvuntil("[+]n")
 sh.sendline("3")
 sh.recvuntil("[+]n")
 sh.sendline(str(c))
 m = int(sh.recvuntil("n")[:-1])
 m = (iroot(m,83)[0])
 m = int(m)
 return m

n = 342252041423688785889282765687710688255177882518369200750856155858905317457669565327799154097080309519902323704731786521119679788331163899712030592725716553131904990426795686126430473254570275940110987683808214438585625423418919468468832148182908455474456550418041742997271433240614952005578253682336437125038102326899911333463929489685779323867218442530395713429260907696832757449156018783902172677312100563325755016411027809771718818171259598563888947753292653500901534384554453984509887806078098349553817530495128573148732706790048315312568413984071196984273100823863183298941823312722426405346171773474664965706357164182619792042434685780148473772921281445129558163823564579979182803128147267240222286783559132333289318029114339721706448992027153246340364373687926229961729995351698989856745823414933965677866527270826729775261069996489981097613639888849956319227010256286532659702270390841901334861070209915452231417437313078329132875528615282343172673650907640567175830218039566101273281917952868441053517106187436348216473297765766898441932333506483172867604029033657893030890966485205568687558845875381058268702680974533364436558170483121677597702156036363994050124492877180934238685246582213926325796426144036106626768520573 # 这个值在靶机启动后就不变了，所以交互一下直接复制

sh = remote("0.0.0.0",1215)
e = 65537
sh.recvuntil("[+]n")
sh.sendline("2")
sh.recvuntil("[+]n")
sh.sendline("475189300601805")
c = int(sh.recvuntil("n")[:-1])

a = 0
plaintext = 0
i = 0
f = 0
mod = 256   # !!!!!!!!!!!!!!!!!!!! 
while True:
    #for i in range(0,400):
 inv = inverse(mod,n) # pow(3,-1)
 c1 = (c * pow(inv,e*i,n)) % n
 p = lsbOracle(c1)
 print(p)
 aa = (p - (a*inv) % n) % mod
 print(aa)
 print("---------round " + str(i) + " ---------")
 if aa == 0:
  f += 1
  if f == 20:
   break
 else:
  f = 0
 a = a*inv + aa
 plaintext = mod**i*aa + plaintext
 print(long_to_bytes(plaintext))
 i += 1
 '''content = long_to_bytes(plaintext)
 if b"flag" in content:
  break''' 
print(long_to_bytes(plaintext))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/9-1712623682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1712623682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/5-1712623683.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/6-1712623685.png)