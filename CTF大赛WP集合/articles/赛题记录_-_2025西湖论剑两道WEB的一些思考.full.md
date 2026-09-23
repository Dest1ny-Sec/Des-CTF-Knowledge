---
title: 赛题记录 | 2025西湖论剑两道WEB的一些思考
contest: 2025 西湖论剑
year: 2025
difficulty: medium
vuln_type: ssti
tags:
- Flask-SSTI
- render_template_string
- format-string
- JSON.parse
- URL-encoding
- js-replace
- lastMatch
- sqli
- String-replace-attack
attack_chain:
- '例题1 Flask SSTI: render_template_string + format(phone)拼接用户输入phone触发SSTI'
- 关键词过滤:flag/?/*/-/less/nl/tac/more/tail/od/grep/awd/sed/64//%2f/%2F
- 绕:使用curl目标机器|sh执行命令(也可通过print与进制绕)
- nc回传命令逐点执行
- '例题2 Nodejs SQL注入: 双重关卡'
- 1. URI中不允许逗号 → URL编码绕过
- 2. 用户名/密码过滤'|"/\ → 真正的考题
- 关键:String.replace的lastMatch特性$` (待替换字符前所有字符)
- 构造:$` or 1# 作为username,触发SELECT * FROM userinfo WHERE username='` or 1#' and password='aa
- $` 被替换为待替换字符前的所有字符,or 1#逃逸出单引号外
key_payload: $` or 1# (String.replace lastMatch特性)
one_liner: 2025西湖论剑两道WEB,Flask SSTI双层关键词过滤绕(curl|sh/nc)+Nodejs SQL注入String.replace lastMatch($` or 1#)逃逸单引号外。
lesson: Flask render_template_string配合format()是危险的;Nodejs String.replace的$` $' lastMatch特性常被忽视,可绕SQL注入字符过滤;URL编码是绕URI字符限制的通用方法。
quality: high
full_path: 赛题记录_-_2025西湖论剑两道WEB的一些思考.full.md
meta_path: 赛题记录_-_2025西湖论剑两道WEB的一些思考.meta.md
images_removed: true
images_removed_count: 4
schema_version: v3.0.0-P0
summary: '赛题记录 | 2025西湖论剑两道WEB的一些思考。2025西湖论剑两道WEB,Flask SSTI双层关键词过滤绕(curl|sh/nc)+Nodejs SQL注入String.replace lastMatch($` or 1#)逃逸单引号外。。关键路径：例题1 Flask SSTI: render_template_string + format(phone)拼接用户输入phone触发...'
category: web
subcategory: web_other
tools_used:
- Flask
- curl
- netcat
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 4
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/225011.html
reasoning_chain:
- 例题1 Flask SSTI：render_template_string + format(phone) 拼接用户输入 → 触发点：SSTI 入口
- 关键词黑名单：flag/?/*/-/less/nl/tac/more/tail/od/grep/awd/sed/64//%2f/%2F → 假设：绕黑名单
- 动作：用 'curl 目标|sh' 替代 'cat /flag' → 观察：RCE 成功
- 或通过 print+进制编码（八进制/十六进制）绕 → nc 回传命令逐点执行
- 例题2 Node.js SQL 注入 → 触发点：双重关卡
- 关卡1：URI 中不允许逗号 → 假设：URL 编码可绕过 → 动作：%2C 编码
- 关卡2：过滤 '|\"/ → 假设：需要用其他字符
- 关键洞察：String.replace 的 lastMatch 特性 $`（待替换字符前所有字符）
- 构造：$` or 1# 作为 username → 触发 SELECT * FROM userinfo WHERE username='<原始 or 1#' and password='aa
- $` 替换为单引号前所有字符 → or 1# 逃逸出单引号外 → SQL 注入成功
failed_attempts:
- 用 'cat /flag' → 失败：关键词黑名单过滤
- 用 ?cmd=cat /flag → 失败：? 也被过滤
- 用双写 catcat → 失败：只替换一次仍可能命中
- 关卡2 直接 'or 1# → 失败：' 被过滤
key_observations:
- Flask render_template_string 配合 format() 是危险的 SSTI 模式
- Node.js String.replace 的 $` $' lastMatch 特性常被忽视，可绕 SQL 注入字符过滤
- URL 编码（%2C 等）是绕 URI 字符限制的通用方法
- 命令执行可走 curl+bash/nc 回传，不一定要 cat/flag 关键词
prerequisites:
- Flask SSTI（Jinja2 模板注入）原理与绕过
- Node.js String.replace 替换模式（$` $' $$ $&）
- URL 编码与解码原理
- SQL 注入基础与 WAF 绕过技巧
---
# 赛题记录 | 2025西湖论剑两道WEB的一些思考

> 原文: https://www.ctfiot.com/225011.html
> ID: 225011

赛题记录 | 2025西湖论剑两道WEB的一些思考

例题1: Python SSTI

目标站点存在 SSTI, 通过命令执行, 拿到源码如下:

from flask import Flask, request, render_template, render_template_string, redirect, url_for, abort
from urllib.parse import unquote

app = Flask(__name__)

phone = ''

def is_safe_input(user_input):
    # unsafe_keywords = ['eval', 'exec', 'os', 'system', 'import', '__import__']
    unsafe_keywords = ['flag','?','*','-','less','nl','tac','more','tail','od','grep','awd','sed','64','/','%2f','%2F']
    if any(keyword in user_input for keyword in unsafe_keywords):
    # if user_input in unsafe_keywords:
        return True
    return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    global phone
    phone = request.form.get("phone_number")
    return render_template("login.html")

@app.route("/cpass", methods=["POST"])
def check():
    global phone
    password = request.form.get("password")

    if is_safe_input(phone):
        return redirect(url_for('index'))

    if phone != "1686682318" and password != "Happy_news_admin":
        return render_template_string('<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>login failed</title>
        </head>
        
            <script>alert("{}The number does not exist or the password is incorrect!") </script>
            <script>window.location.href = "/";</script>
        
        </html>'.format(phone))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5005"), debug=True)

实际上只是普通的一道 SSTI 题目, 但比赛时临时想到了一个绕过方法, 将其记载下来:

这是一个普通的 curl 命令拿机器返回值的案例, 绕过比较简单: 使用curl 目标机器 | sh即可 (当然也可以通过print与进制绕过), 具体拿 flag 过程如下:

一点一点使用 nc 回传要执行的命令即可. 对于上图为什么没有伪造 HTTP 响应头即可攻击成功, 可能对 CURL 版本有具体限制, 以后遇到尽量加上 HTTP 响应头.

例题2: Nodejs SQL 注入

比赛给出了代码如下:

var express = require('express');
var router = express.Router();
module.exports = router;

router.get('/',(req,res,next)=>{
    if(req.query.info){
        if(req.url.match(/,/ig)){
            res.end('hacker1!');
        }
        var info = JSON.parse(req.query.info);
        if(info.username&&info.password){
            var username = info.username;
            var password = info.password;
            if(info.username.match(/'|"|\/) || info.password.match(/'|"|\/)){
                res.end('hacker2!');
            }
            var sql = "select * from userinfo where username = '{username}' and password = '{password}'";
            sql = sql.replace("{username}",username);
            sql = sql.replace("{password}",password);
            connection.query(sql,function (err,rs) {
            if (err) {
                res.end('error1');
            }
            else {
                if(rs.length>0){
                res.sendFile('/flag');
                }else {
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

其中有两层关卡, 第一层是不允许URI中存在逗号, 这里使用 URL 编码即可绕过.

第二层关卡才是核心, 实际上考核的是js中对String.replace函数的一个特性.

参考: https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/RegExp/lastMatch

中说明了JavaScript特性, 这里可以利用的只有

$` 与 $'

下面看一下具体利用方案:

var str = "Hello, my name is Heihu577.";
var regex = /my name/;
var result = str.replace(regex, "A $` B");
console.log(result);

而最终的运行结果为:

$` 的位置被替换成了 待替换字符前的所有字符, 所以这里Hello被挤出来, 那么根据这个场景, 我们可以模拟一个与比赛相同的环境:

var str = "SELECT * FROM userinfo WHERE username='{username}' and password='{password}'";
str = str.replace('{username}', '$` or 1#'); // 可控点
str = str.replace('{password}', 'aa'); // 可控点
console.log(str);

最终运行结果:

这里成功将or 1#逃逸出来, 从而导致了绕过.


```
from flask import Flask, request, render_template, render_template_string, redirect, url_for, abort
from urllib.parse import unquote

app = Flask(__name__)

phone = ''

def is_safe_input(user_input):
    # unsafe_keywords = ['eval', 'exec', 'os', 'system', 'import', '__import__']
    unsafe_keywords = ['flag','?','*','-','less','nl','tac','more','tail','od','grep','awd','sed','64','/','%2f','%2F']
    if any(keyword in user_input for keyword in unsafe_keywords):
    # if user_input in unsafe_keywords:
        return True
    return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    global phone
    phone = request.form.get("phone_number")
    return render_template("login.html")

@app.route("/cpass", methods=["POST"])
def check():
    global phone
    password = request.form.get("password")

    if is_safe_input(phone):
        return redirect(url_for('index'))

    if phone != "1686682318" and password != "Happy_news_admin":
        return render_template_string('<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>login failed</title>
        </head>
        
            <script>alert("{}The number does not exist or the password is incorrect!") </script>
            <script>window.location.href = "/";</script>
        
        </html>'.format(phone))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5005"), debug=True)
var express = require('express');
var router = express.Router();
module.exports = router;

router.get('/',(req,res,next)=>{
    if(req.query.info){
        if(req.url.match(/,/ig)){
            res.end('hacker1!');
        }
        var info = JSON.parse(req.query.info);
        if(info.username&&info.password){
            var username = info.username;
            var password = info.password;
            if(info.username.match(/'|"|\/) || info.password.match(/'|"|\/)){
                res.end('hacker2!');
            }
            var sql = "select * from userinfo where username = '{username}' and password = '{password}'";
            sql = sql.replace("{username}",username);
            sql = sql.replace("{password}",password);
            connection.query(sql,function (err,rs) {
            if (err) {
                res.end('error1');
            }
            else {
                if(rs.length>0){
                res.sendFile('/flag');
                }else {
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
$` 与 $'
var str = "Hello, my name is Heihu577.";
var regex = /my name/;
var result = str.replace(regex, "A $` B");
console.log(result);
var str = "SELECT * FROM userinfo WHERE username='{username}' and password='{password}'";
str = str.replace('{username}', '$` or 1#'); // 可控点
str = str.replace('{password}', 'aa'); // 可控点
console.log(str);
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]