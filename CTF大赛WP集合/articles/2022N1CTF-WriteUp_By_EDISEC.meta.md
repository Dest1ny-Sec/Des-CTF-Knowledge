---
title: 2022 N1CTF WriteUp By EDISEC
contest: N1CTF 2022
year: 2022
difficulty: hard
vuln_type: [lfi, web_unknown, lattice, crypto_rsa, forensic_disk]
tags: [N1CTF, struts2, WEB-INF, mtime, md5, cmd-trace, WallPaper, knapsack-LLL, discrete_log, GF(q), ECDLP, DLP]
attack_chain: ["Web Easy_S2: struts2 WEB-INF/classes/com.mycompany.helloword.action/struts.xml + .do 后缀", "Misc just_find_flag: cmd 痕迹 'C:\\\\Program Files (x86)\\\\Windows NT\\\\Accessories\\\\flag.zip' → md5(0d3ba7db468bdbd4f93a88c97ba7bef1) 是密码", "Crypto Ezdlp: knapsack lattice 攻击 m = matrix(ZZ, len(l), len(l)+1) → LLL 短向量 → GCD 找 n 因子", "q = 12980311456459934558628309999285260982188754011593109633858685687007370476504059552729490523256867881534711749584157463076269599380216374688443704196597025947 (130-bit)", "ECDLP: F=GF(q), g=F(0x10001), y 已知 → discrete_log(y, g) 还原 a → flag"]
key_payload: "md5('C:\\\\Program Files (x86)\\\\Windows NT\\\\Accessories\\\\flag.zip') = 0d3ba7db468bdbd4f93a88c97ba7bef1"
one_liner: N1CTF 2022：struts2 LFI + cmd 痕迹 md5 + knapsack lattice + ECDLP
lesson: cmd 痕迹 = 取证金矿；knapsack lattice 是经典格密码；ECDLP 130-bit 可用 Pohlig-Hellman
quality: high
---

# 2022 N1CTF WriteUp By EDISEC

原文 https://www.ctfiot.com/71976.html

## Web

### Easy_S2
```bash
# Struts2 经典 LFI
# 看 WEB-INF/classes/com.mycompany.helloword.action 下的 struts.xml
# 后缀是 .do 不是 .action
# https://openhome.cc/Gossip/ServletJSP/DeclarativeSecurityBasic.html
```

## Misc

### just find flag
```bash
# cmd 痕迹：
# echo "Stucked? You can ask WallPaper god for help."
# "C:\Program Files (x86)\Windows NT\Accessories\flag.zip"
from hashlib import md5
a = 'C:\\Program Files (x86)\\Windows NT\\Accessories\\flag.zip'
a = md5(a.encode('utf-8')).hexdigest()
print(a)
# 0d3ba7db468bdbd4f93a88c97ba7bef1
```
- 还原 cmd 历史记录
- 把路径字符串 md5 当 zip 密码

## Crypto

### Ezdlp (knapsack lattice)
```python
l = [...]  # 20 个长整数
m = matrix(ZZ, len(l), len(l) + 1)
for i in range(len(l)):
    m[i, i] = 1
    m[i, len(l)] = l[i]
r = m.LLL()

def get_kn(s, c):
    cc = c[:-1]
    l = [i for i in s]
    l[-1] = -l[-1]
    u, v = 1, pow(e, abs(s[-1]))
    if s[-1] < 0: u, v = v, u
    for i in range(len(cc)):
        if s[i] > 0: u *= pow(cc[i], s[i])
        if s[i] < 0: v *= pow(cc[i], -s[i])
    return u - v

nl = [get_kn(i, c) for i in r]
print(GCD(nl))
```

### ECDLP
```python
# 130-bit 素数域上的 ECDLP
q = 12980311456459934558628309999285260982188754011593109633858685687007370476504059552729490523256867881534711749584157463076269599380216374688443704196597025947
F = GF(q)
g = F(0x10001)
y = F(91561944814950778736488535643520052714900101756544637483800925876319855838327993556442983654484996766433049736153189800056457912285338408230393372558184963346036063617106521919740962726456954911219888157214487326900658606650604294547947205051640436119495039170478782141363198165616660075024383933961325219072058)
a = int(discrete_log(y, g))
print(bytes.fromhex(hex(a)[2:]))
```

### DLP
```python
# a, b = 随机素数
a = primes(2^24, 2^25)
b = primes(2^31, 2^32)
g = pow(2, 2, n)  # g=2^2
# Pohlig-Hellman
D = pow(g, 2^16, n)
V = pow(g, -1, n)
l = [pow(D, u, n) for u in range(2^16)]
for v in range(1, 2^16, 2):
    vv = pow(V, v, n)
    for j in l:
        if 1 < GCD(j - vv, n):
            print(GCD(j - vv, n))
```

## 教学价值
- **cmd 痕迹** = 取证金矿（Windows 用户行为）
- **md5(路径) 当密码** 是常见 MISC 套路
- **Struts2** LFI 看 .xml 是经典 web 入门
- **knapsack lattice** 是格密码标准问题
- **ECDLP** 130-bit 域上 Pohlig-Hellman 可破
- **discrete_log** 是 SageMath 内置

## 工具
- md5sum
- struts2 scan
- SageMath (LLL / discrete_log)
- adb / fastboot（提取 mtime）

## 关联
- #20 N1CTF Junior 2026 pwn（rop/srop）
- #38 N1CTF 2023 pwn1OS (iOS pwn)
