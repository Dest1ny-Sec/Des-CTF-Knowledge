# 2024 强网拟态 CFB_chall

> 原文: https://www.ctfiot.com/211724.html
> ID: 211724

from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import AES
import os
from string import printable
app = Flask(__name__)

# 初始化全局变量
def initialize_globals():
    global key, iv,register_open, login_attempts
    key = os.urandom(16)
    iv  = os.urandom(16)
    register_open = True
    login_attempts = 500

initialize_globals()

def encrypt(data, key):
    #iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    ct_bytes = cipher.encrypt(data.encode('utf-8'))
    return ct_bytes.hex()

def decrypt(ct, key):
    ct_bytes = bytes.fromhex(ct)
    #iv = ct_bytes[:16]
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    data = cipher.decrypt(ct_bytes[:])
    #print("data:",data)
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    global register_open, login_attempts
    message = ""
    
    if request.method in  ['POST']:
        if request.is_json:
            data = request.get_json()
            action = data.get('action')
            
            if action == 'register':
                if not register_open:
                    message = "Registration function is closed"
                else:
                    username = data.get('username')
                    password = data.get('password')
                    if len(password)<8:
                     message = "Registration failed, password too short"
                    elif not set(password+username)<=set(printable):
                        message = "Registration failed, illegal character"
                    elif 'admin' in username:
                        message = "Registration failed, you are not an admin"
                    else:
                        token = encrypt(f"{username}x00{password}x01x02x03", key)
                        register_open = False
                        message = f"Please save your token: {token}"
            
            elif action == 'login':
                if login_attempts <= 0:
                    message = "Too many attempts"
                else:
                    username = data.get('username').encode()
                    password = data.get('password').encode()
                    token = data.get('token')
                    
                    try:
                        decrypted = decrypt(token, key)
                        #print(decrypted)
                        token_username, *_, token_password = decrypted.split(b'x00')
                        #print(token_username,",",token_password)
                        assert(token_password[-3:]==b"x01x02x03")
                        token_password=token_password[:-3]
                        if username == token_username and password == token_password:
                            if username == b'admin':
                                #print(token_password)
                                if password == b'123456':
                                    f=open("./flag","r")
                                    flag=f.read()
                                    #print(flag)
                                    f.close()
                                    message = "You have logged in with admin privileges, here is your flag: "+flag
                                else:
                                    message = "Admin login failed, please try again"
                            else:
                                message = "You have logged in as a regular user"
                        else:
                            message = "Login failed, please try again"
                    
except:
                        message = "Login wrong, please try again"
                    finally:
                        login_attempts -= 1
            
            elif action == 'restart':
                initialize_globals()
                message = "System has been restarted. AES key and function counts have been reset."
        else:
            message = "Unsupported Media Type: Content-Type must be application/json"
    
        return jsonify({'message': message})
    return render_template('index.html', message=message)    

if __name__ == '__main__':
    app.run(host="0.0.0.0")

题目内容

题目是一个简单的注册登录机制。首先是注册，要求用户名不为admin，密码长度超过8位，并且都是可见字符。然后会生成 token = encrypt(f"{username}x00{password}x01x02x03", key)，这里加密用的是 AES_CFB 模式。

获取flag的部分在注册，注册的时候会解密token，然后以 x00 进行分割，分别获取用户名和密码，然后要求密码的最后三个字节是 x01x02x03

如果想要获取flag，还要求用户名是 admin，密码是 123456 登录。

这里的主要矛盾是不能注册admin，密码长度不小于 8 位，与，登录 admin，密码是123456，只有六位之间的矛盾。

所以解题方向显然就是先注册，然后通过篡改 token 来达到绕过限制的效果。

解题步骤

最开始我在网上找到的 CFB 模式是这样子的

有点类似于流密码，那题目不是很简单么？我们注册一个admi，然后密码设置成aa123456，此时我们的token明文是 admi x00 aa123456x01x02x03 ，刚好十六个字节。然后会获得对应的十六字节密文，我们只需要在密文的对应位置（第5，6，7个字节）做一下修改，让他把原来是 x00 aa的解密成 nx00 x00 就好了。

因为以 x00 进行分割用的代码是token_username, *_, token_password = decrypted.split(b'x00')，这表示如果用 x00 分出超过两段的话，中间多余的部分会全部传给变量_

那么好像，这题就简单的结束了？

事实并非如此。在使用代码测试的时候，发现 python 实现的 AES CFB 模式其实是这样的

其中，n = 1，也就是每次只加密一个字节。

因此当修改一个字节的时候，极大概率会影响后面 16 字节的解密（参考上图，因为进入下一组的“加密器“的输入变了，于是K就整个变了，K的最高位有极大概率和原来不同）。

测试代码

from Crypto.Cipher import AES

def encrypt(data):
    #iv = os.urandom(16)
    #key = os.urandom(16)
    iv = b"a"*16
    key = b"a"*16
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    ct_bytes = cipher.encrypt(data.encode('utf-8'))
    return ct_bytes.hex()

def decrypt(ct):
    iv = b"a"*16
    key = b"a"*16
    ct_bytes = bytes.fromhex(ct)
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    data = cipher.decrypt(ct_bytes[:])
    #print("data:",data)
    return data

res = encrypt("adminx00123456x01x02x03abcdefg")
print(res)
print(decrypt(res))

# 修改第一个字节，解密为b
print(decrypt(hex(0x30^ord('a')^ord('b'))[2:].rjust(2,'0')+"74fd4ec3277a06ad2e91ba41d043b40adf38a3333e"))

测试结果

可以看到虽然第一个字节被成功篡改为了b，但是连着后面十六个字节也都被影响了。

于是我们要调整一下注册策略。

这里我选择注册 admim，密码为 'a'*15+'11123456'，这样修改第五个 m 为n 时，只会影响后面十五个a和第一个1 的解密，然后为了把 admin 隔离出来，我们还要修改第六个字节，使得 n 后面跟一个 x00。但是前面说了，由于对第五个字节 m 的修改，会影响到第六个的解密，并且我们也不知道会解密后的明文是什么，所以这里我们只能选择爆破，需要用掉 256 次登录机会。

不过即使 admin 可以分割出来，123456 怎么处理呢？

我们注册的密码时 11123456，对 m 的修改，会同时影响第 22 字节的 1 。但是不碍事，我们是需要对第 23 字节的 1 进行篡改，如果改成 x00，那么就能把后面的 123456x01x02x03 分离出来，就能绕过验证了。

但如果去主动修改这第 23 字节的 1，那同样会导致后面 123456x01x02x03 解密受影响。所以我们只能选择爆破第 7个字节，让他影响到第 23 字节，但又不影响更后面内容的解密。

不过由于登录次数只有500次，两个字节的爆破最多需要65536次机会，这是远远不够的。

我这里的策略是，第七个字节我指定一个值，如果当后面第 23 字节被确定改成 x00后，那么根据分割代码 token_username, *_, token_password = decrypted.split(b'x00')，不管我怎么爆破第六字节，解密后的 token 肯定会至少被分割为两部分，就不会报错，否则就会返回 wrong。如果返回 wrong，我就直接 reset，重置 iv 和 key，再试。

如果前三次的爆破都没有返回 wrong，那基本就成了。此时再继续爆破第 6 个字节就可以了。总共只需要 256 次登录尝试。

import requests

def reset():
        burp0_url = "http://web-dea8c74b17.challenge.xctf.org.cn:80/"
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
131.0) Gecko/20100101 Firefox/131.0", "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest", "Origin": "http://web-dea8c74b17.challenge.xctf.org.cn", "Connection": "keep-alive", "Referer": "http://web-dea8c74b17.challenge.xctf.org.cn/", "Priority": "u=0"}
        burp0_json = {
            "action": "restart",
        }
        r=requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
        return 

def login(token):
        username = "admin"
        password = '123456'
        # password = '12345678'
        burp0_url = "http://web-dea8c74b17.challenge.xctf.org.cn:80/"
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
131.0) Gecko/20100101 Firefox/131.0", "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest", "Origin": "http://web-dea8c74b17.challenge.xctf.org.cn", "Connection": "keep-alive", "Referer": "http://web-dea8c74b17.challenge.xctf.org.cn/", "Priority": "u=0"}
        burp0_json = {
            "action": "login",
            "password": password,
            "token": token,
            "username": username
        }
        r=requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
        return(r.text)

def reg():
        username = "admim"
        password = 'a'*15+'11123456'
        # password = '12345678'
        burp0_url = "http://web-dea8c74b17.challenge.xctf.org.cn:80/"
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
131.0) Gecko/20100101 Firefox/131.0", "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest", "Origin": "http://web-dea8c74b17.challenge.xctf.org.cn", "Connection": "keep-alive", "Referer": "http://web-dea8c74b17.challenge.xctf.org.cn/", "Priority": "u=0"}
        burp0_json = {
            "action": "register",
            "password": password,
            "username": username
        }
        r=requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
        return (r.text)

while True:

        reset()
        r = reg()
        # print(r)
        token = (r[r.index(": ")+2:-3])
        print(token)
        with open("token","w") as f:
                f.write(token)

        from tqdm import *
        for i in range(256):
            print(i)

            s = ((token[:8]+(hex(int(token[8:10],16)^(ord('m')^ord('n')))[2:]).rjust(2,'0')+hex(i)[2:].rjust(2,'0')+'01'+token[14:]))             
            print(s)
            r = login(s)
            if "wrong" in r:
                    print("next")
                    break
            if i==2:
                    print("maybe in ")
            if 'flag' in r:
                    print(r)

理论上我们这种做法的成功率是 1/512。

通过 reset 随机碰撞出第 23 字节的 x00，这里的概率是 1/256，但实际运行次数要看运气。

没有报错表示进入第二阶段，通过 login 遍历出第 6 字节的 x00 。这里的概率也是 1/256，但实际运行次数不超过256次。

CFB chall revenge

赛后春哥觉得我这种做法还是不太优雅，还搞了一个 revenge 在 NSSCTF ：[ZMJ4396]CFBChall_revenge | NSSCTF

from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import AES
import os
from string import printable
app = Flask(__name__)

# 初始化全局变量
def initialize_globals():
    global key, iv,register_open, login_attempts
    key = os.urandom(16)
    iv  = os.urandom(16)
    register_open = True
    login_attempts = 777

initialize_globals()

def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    ct_bytes = cipher.encrypt(data.encode('utf-8'))
    return ct_bytes.hex()

def decrypt(ct, key):
    ct_bytes = bytes.fromhex(ct)
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    data = cipher.decrypt(ct_bytes[:])
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    global register_open, login_attempts
    message = ""
    
    if request.method in  ['POST']:
        if request.is_json:
            data = request.get_json()
            action = data.get('action')
            
            if action == 'register':
                if not register_open:
                    message = "Registration function is closed"
                else:
                    username = data.get('username')
                    password = data.get('password')
                    if len(password)<8:
                        message = "Registration failed, password too short"
                    elif not set(password+username)<=set(printable):
                        message = "Registration failed, illegal character"
                    elif 'admin' in username:
                        message = "Registration failed, you are not an admin"
                    else:
                        token = encrypt(f"{username}x00{password}x01x02x03", key)
                        register_open = False
                        message = f"Please save your token: {token}"
            
            elif action == 'login':
                if login_attempts <= 0:
                    message = "Too many attempts"
                else:
                    username = data.get('username').encode()
                    password = data.get('password').encode()
                    token = data.get('token')
                    
                    try:
                        decrypted = decrypt(token, key)
                        #print(decrypted)
                        token_username, *_, token_password = decrypted.split(b'x00')
                        #print(token_username,",",token_password)
                        assert(token_password[-3:]==b"x01x02x03")
                        token_password=token_password[:-3]
                        if username == token_username and password == token_password:
                            if username == b'admin':
                                #print(token_password)
                                if password == b'123456':
                                    f=open("./flag.txt","r")
                                    flag=f.read()
                                    f.close()
                                    message = "You have logged in with admin privileges, here is your flag: "+flag
                                else:
                                    message = "Admin login failed, please try again"
                            else:
                                message = "You have logged in as a regular user"
                        else:
                            message = "Login failed, please try again"
                    
except:
                        message = "Login wrong, please try again"
                    finally:
                        login_attempts -= 1
            
            elif action == 'restart':
                message = "Uh-oh, this function is no longer available :("
        else:
            message = "Unsupported Media Type: Content-Type must be application/json"
    
        return jsonify({'message': message})
    return render_template('index.html', message=message)    

if __name__ == '__main__':
    app.run(host="0.0.0.0")

主要是把函数 restart 给 ban 了，也就是把我上面看运气的这部分路给断了。（当然重启靶机还是可以达到同样的效果，不过这就更加不优雅了）

那么我们注意到代码中另一个做的比较危险的地方，就是对于不同的错误，有不同的报错内容返回（没记错的话，当初 openssl 代码中就是因为不同的报错返回，才让 RSA PKCSv1.5 挨打了）

回顾一下我们上一题的token:'admim'+'x00'+'a'*15+'11123456'+'x01x02x03'

由于 username 和 password 我们都可控，这一次我们选择把这个 x00 后移

我们设 username 为 'admim' + 'a'*17，password 为 11123456

于是 token: 'admim'+'a'*17+'x00'+'11123456'+'x01x02x03'

第一步跟之前一样，我们修改 m 为 n，然后爆破第六个字节，

当第六个字节被篡改，解密后为 x00 时，我们就可以以 admin 和 11123456 登录，不过由于题目代码

if username == b'admin':
    #print(token_password)
    if password == b'123456':
        f=open("./flag.txt","r")
        flag=f.read()
        f.close()
        message = "You have logged in with admin privileges, here is your flag: "+flag
    else:
        message = "Admin login failed, please try again"
else:
    message = "You have logged in as a regular 

此时会返回报错 Admin login failed, please try again

这个时候我们就根据报错，确定了第 6 个字节，我们以此为基础，然后再爆破密文第 9 个字节，让明文第 25 个字节解密为 x00，这个时候我们就能以 admin 和 123456 登录，拿到 flag 了。

理论上两次遍历，最多只需要交互 512 次。题目给了 777 次，是完全足够的。


```
from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import AES
import os
from string import printable
app = Flask(__name__)

# 初始化全局变量
def initialize_globals():
    global key, iv,register_open, login_attempts
    key = os.urandom(16)
    iv  = os.urandom(16)
    register_open = True
    login_attempts = 500

initialize_globals()

def encrypt(data, key):
    #iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    ct_bytes = cipher.encrypt(data.encode('utf-8'))
    return ct_bytes.hex()

def decrypt(ct, key):
    ct_bytes = bytes.fromhex(ct)
    #iv = ct_bytes[:16]
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    data = cipher.decrypt(ct_bytes[:])
    #print("data:",data)
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    global register_open, login_attempts
    message = ""
    
    if request.method in  ['POST']:
        if request.is_json:
            data = request.get_json()
            action = data.get('action')
            
            if action == 'register':
                if not register_open:
                    message = "Registration function is closed"
                else:
                    username = data.get('username')
                    password = data.get('password')
                    if len(password)<8:
                     message = "Registration failed, password too short"
                    elif not set(password+username)<=set(printable):
                        message = "Registration failed, illegal character"
                    elif 'admin' in username:
                        message = "Registration failed, you are not an admin"
                    else:
                        token = encrypt(f"{username}x00{password}x01x02x03", key)
                        register_open = False
                        message = f"Please save your token: {token}"
            
            elif action == 'login':
                if login_attempts <= 0:
                    message = "Too many attempts"
                else:
                    username = data.get('username').encode()
                    password = data.get('password').encode()
                    token = data.get('token')
                    
                    try:
                        decrypted = decrypt(token, key)
                        #print(decrypted)
                        token_username, *_, token_password = decrypted.split(b'x00')
                        #print(token_username,",",token_password)
                        assert(token_password[-3:]==b"x01x02x03")
                        token_password=token_password[:-3]
                        if username == token_username and password == token_password:
                            if username == b'admin':
                                #print(token_password)
                                if password == b'123456':
                                    f=open("./flag","r")
                                    flag=f.read()
                                    #print(flag)
                                    f.close()
                                    message = "You have logged in with admin privileges, here is your flag: "+flag
                                else:
                                    message = "Admin login failed, please try again"
                            else:
                                message = "You have logged in as a regular user"
                        else:
                            message = "Login failed, please try again"
                    
except:
                        message = "Login wrong, please try again"
                    finally:
                        login_attempts -= 1
            
            elif action == 'restart':
                initialize_globals()
                message = "System has been restarted. AES key and function counts have been reset."
        else:
            message = "Unsupported Media Type: Content-Type must be application/json"
    
        return jsonify({'message': message})
    return render_template('index.html', message=message)    

if __name__ == '__main__':
    app.run(host="0.0.0.0")
from Crypto.Cipher import AES

def encrypt(data):
    #iv = os.urandom(16)
    #key = os.urandom(16)
    iv = b"a"*16
    key = b"a"*16
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    ct_bytes = cipher.encrypt(data.encode('utf-8'))
    return ct_bytes.hex()

def decrypt(ct):
    iv = b"a"*16
    key = b"a"*16
    ct_bytes = bytes.fromhex(ct)
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    data = cipher.decrypt(ct_bytes[:])
    #print("data:",data)
    return data

res = encrypt("adminx00123456x01x02x03abcdefg")
print(res)
print(decrypt(res))

# 修改第一个字节，解密为b
print(decrypt(hex(0x30^ord('a')^ord('b'))[2:].rjust(2,'0')+"74fd4ec3277a06ad2e91ba41d043b40adf38a3333e"))
import requests

def reset():
        burp0_url = "http://web-dea8c74b17.challenge.xctf.org.cn:80/"
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
131.0) Gecko/20100101 Firefox/131.0", "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest", "Origin": "http://web-dea8c74b17.challenge.xctf.org.cn", "Connection": "keep-alive", "Referer": "http://web-dea8c74b17.challenge.xctf.org.cn/", "Priority": "u=0"}
        burp0_json = {
            "action": "restart",
        }
        r=requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
        return 

def login(token):
        username = "admin"
        password = '123456'
        # password = '12345678'
        burp0_url = "http://web-dea8c74b17.challenge.xctf.org.cn:80/"
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
131.0) Gecko/20100101 Firefox/131.0", "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest", "Origin": "http://web-dea8c74b17.challenge.xctf.org.cn", "Connection": "keep-alive", "Referer": "http://web-dea8c74b17.challenge.xctf.org.cn/", "Priority": "u=0"}
        burp0_json = {
            "action": "login",
            "password": password,
            "token": token,
            "username": username
        }
        r=requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
        return(r.text)

def reg():
        username = "admim"
        password = 'a'*15+'11123456'
        # password = '12345678'
        burp0_url = "http://web-dea8c74b17.challenge.xctf.org.cn:80/"
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
131.0) Gecko/20100101 Firefox/131.0", "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest", "Origin": "http://web-dea8c74b17.challenge.xctf.org.cn", "Connection": "keep-alive", "Referer": "http://web-dea8c74b17.challenge.xctf.org.cn/", "Priority": "u=0"}
        burp0_json = {
            "action": "register",
            "password": password,
            "username": username
        }
        r=requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
        return (r.text)

while True:

        reset()
        r = reg()
        # print(r)
        token = (r[r.index(": ")+2:-3])
        print(token)
        with open("token","w") as f:
                f.write(token)

        from tqdm import *
        for i in range(256):
            print(i)

            s = ((token[:8]+(hex(int(token[8:10],16)^(ord('m')^ord('n')))[2:]).rjust(2,'0')+hex(i)[2:].rjust(2,'0')+'01'+token[14:]))             
            print(s)
            r = login(s)
            if "wrong" in r:
                    print("next")
                    break
            if i==2:
                    print("maybe in ")
            if 'flag' in r:
                    print(r)
from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import AES
import os
from string import printable
app = Flask(__name__)

# 初始化全局变量
def initialize_globals():
    global key, iv,register_open, login_attempts
    key = os.urandom(16)
    iv  = os.urandom(16)
    register_open = True
    login_attempts = 777

initialize_globals()

def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    ct_bytes = cipher.encrypt(data.encode('utf-8'))
    return ct_bytes.hex()

def decrypt(ct, key):
    ct_bytes = bytes.fromhex(ct)
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    data = cipher.decrypt(ct_bytes[:])
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    global register_open, login_attempts
    message = ""
    
    if request.method in  ['POST']:
        if request.is_json:
            data = request.get_json()
            action = data.get('action')
            
            if action == 'register':
                if not register_open:
                    message = "Registration function is closed"
                else:
                    username = data.get('username')
                    password = data.get('password')
                    if len(password)<8:
                        message = "Registration failed, password too short"
                    elif not set(password+username)<=set(printable):
                        message = "Registration failed, illegal character"
                    elif 'admin' in username:
                        message = "Registration failed, you are not an admin"
                    else:
                        token = encrypt(f"{username}x00{password}x01x02x03", key)
                        register_open = False
                        message = f"Please save your token: {token}"
            
            elif action == 'login':
                if login_attempts <= 0:
                    message = "Too many attempts"
                else:
                    username = data.get('username').encode()
                    password = data.get('password').encode()
                    token = data.get('token')
                    
                    try:
                        decrypted = decrypt(token, key)
                        #print(decrypted)
                        token_username, *_, token_password = decrypted.split(b'x00')
                        #print(token_username,",",token_password)
                        assert(token_password[-3:]==b"x01x02x03")
                        token_password=token_password[:-3]
                        if username == token_username and password == token_password:
                            if username == b'admin':
                                #print(token_password)
                                if password == b'123456':
                                    f=open("./flag.txt","r")
                                    flag=f.read()
                                    f.close()
                                    message = "You have logged in with admin privileges, here is your flag: "+flag
                                else:
                                    message = "Admin login failed, please try again"
                            else:
                                message = "You have logged in as a regular user"
                        else:
                            message = "Login failed, please try again"
                    
except:
                        message = "Login wrong, please try again"
                    finally:
                        login_attempts -= 1
            
            elif action == 'restart':
                message = "Uh-oh, this function is no longer available :("
        else:
            message = "Unsupported Media Type: Content-Type must be application/json"
    
        return jsonify({'message': message})
    return render_template('index.html', message=message)    

if __name__ == '__main__':
    app.run(host="0.0.0.0")
if username == b'admin':
    #print(token_password)
    if password == b'123456':
        f=open("./flag.txt","r")
        flag=f.read()
        f.close()
        message = "You have logged in with admin privileges, here is your flag: "+flag
    else:
        message = "Admin login failed, please try again"
else:
    message = "You have logged in as a regular
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1729849277.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1729849277.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/10-1729849278.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/3-1729849278.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1729849279.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1729849279.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/2-1729849280.png)