---
title: LIT CTF 2024 WriteUp (Web + Python)
contest: LIT CTF
year: 2024
difficulty: easy
vuln_type: web_unknown
tags: [console.log %c, JWT 算法混淆, SSRF, login 逐位比较]
attack_chain: |
  1. anti-inspect: console.log 输出格式 + %c style → 把 %c 删掉就显示 flag
     - LITCTF{your_fOund_teh_fI@g_94932}
  2. JWT1: 没加密部分的校验 → 改 payload 内容即可 (alg=none 攻击或直接改)
  3. JWT2: 程序内 crypto.createHmac('sha256', jwtSecret).update(header + '.' + payload).digest('base64').replace(/=/g, '')
     - jwtSecret 在源码中, jwt.io 解析加密 name 失败 → 本地运行 + 复制 signature
  4. traversed: SSRF / 目录遍历
  5. kirbytime: Flask login 7 字符逐位比较 (timing attack)
     - for i in range(len(password)):
         if password[i] != real[i]:
             message = "incorrect"
             return render_template('login.html', message=message)
         else:  # 阻塞
             time.sleep(0.5)
     - 通过 timing 推断每个字符
key_payload: |
  # anti-inspect console.log 删 %c:
  # console.log("%cLITCTF{your_fOund_teh_fI@g_94932}")
  # → 直接删 %c 看 flag
  
  # JWT1: 改 payload
  # {"alg":"HS256"} → {"alg":"none"} + {"role":"admin"}
  
  # JWT2: 找源码 secret
  expectedSignature = crypto.createHmac('sha256', jwtSecret).update(header + '.' + payload).digest('base64').replace(/=/g, '');
  
  # kirbytime timing attack:
  for i in range(len(password)):
      if password[i] != real[i]:
          message = "incorrect"
          return render_template('login.html', message=message)
      else:
          time.sleep(0.5)  # 阻塞，让 timing 泄露
one_liner: LIT CTF 2024 狼组搬运，5 道 Web 速查 (console.log 样式 / JWT1 改 payload / JWT2 找 secret / 目录遍历 / 7 字符 timing attack)。
lesson: |
  - console.log("%c...") 浏览器才会解释 style flag，但内容已经在 message 里
  - JWT alg=none 是经典攻击: 后端不校验签名直接放行
  - HMAC 签名 jwt.io 解析失败时，本地跑算法生成 signature 再拼 JWT
  - Flask login 7 字符逐位比较 + sleep(0.5) 是经典 timing attack
  - 时序攻击是 login 题的"灰色地带"，现代 CTF 已经少用
quality: low
---

# LIT CTF 2024 WriteUp

> 来源: ctfiot.com 199713 - 狼组安全社区

## anti-inspect

```javascript
// 题目代码:
console.log("%c" + flag)  // %c 是 CSS style
```

**绕过：** 把 `%c` 删掉就显示完整 flag。

`LITCTF{your_fOund_teh_fI@g_94932}`

## JWT1

题目用 JWT 验证，**没加密部分校验**。直接改 payload（如 `role: admin`）即可通过。

```python
# alg=none 攻击:
header = {"alg": "none", "typ": "JWT"}
payload = {"role": "admin"}
token = base64url(header) + "." + base64url(payload) + "."
```

## JWT2

```python
expectedSignature = crypto.createHmac('sha256', jwtSecret) \
    .update(header + '.' + payload).digest('base64').replace(/=/g, '');
```

源码找 `jwtSecret` → 本地运行算法生成 signature → 拼接 JWT。`jwt.io` 解析加密的 name 失败时，用这个方法。

## traversed

SSRF / 目录遍历基础题，flag 藏在 internal endpoint。

## kirbytime (Flask 7 字符 timing attack)

```python
@app.route('/', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        password = request.form['password']
        real = 'REDACTED'
        if len(password) != 7:
            return render_template('login.html', message="you need 7 chars")
        for i in range(len(password)):
            if password[i] != real[i]:
                message = "incorrect"
                return render_template('login.html', message=message)
            else:
                time.sleep(0.5)  # 关键: 阻塞
        # success
```

**Timing attack：** 第一个字符对时阻塞 0.5s → 推断字符 → 第二个字符对时再阻塞 → ... 7 次后穷举出密码。

## 评价

LIT CTF 2024 狼组搬运，5 道 Web 速查。每道都是"工具熟悉度"考试：
- console.log %c 是浏览器渲染 trick
- JWT alg=none 是 2018 经典攻击
- HMAC 签名 jwt.io 失败时本地重算
- Timing attack 是 login 题的灰色地带

整体偏入门，缺深度。
