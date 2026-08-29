---
title: 解析2025LitCTF-math
contest: LitCTF 2025
year: 2025
difficulty: medium
vuln_type: crypto_rsa
tags: [RSA, hint-leak, noise-factor, p-plus-q, Vieta, Pollard-Rho, Miller-Rabin, isqrt, wiener-attack, math-model]
attack_chain:
- 识别hint异常:hint=p*q+noise*p+noise*q+noise² = n + noise*(p+q+noise)
- 计算hint_minus_n = hint - n,寻找40位左右素因子noise
- Pollard-Rho因数分解,验证(noise, d//noise)是否满足isqrt判别式为完全平方
- 命中noise=942430120937
- 由hint-n = noise*(p+q+noise)推导S = (hint-n)//noise,p+q = S - noise
- (p-q)² = (p+q)² - 4n,p-q = isqrt(...)求得
- p = ((p+q) + (p-q))/2,q = ((p+q) - (p-q))/2
- 验证p*q == n,计算phi=(p-1)(q-1),d=e⁻¹ mod phi
- m=c^d mod n,long_to_bytes得flag
key_payload: LitCTF{db6f52b9265971910b306754b9df8b76}
one_liner: LitCTF 2025 math方向RSA带噪声hint泄露攻击链,标准hint = n + noise*(p+q+noise)形式,40位小素数Pollard-Rho分解+韦达定理还原p,q。
lesson: 任何hint都要先转成数学表达式: hint = n + noise*(p+q+noise) 是关键;小素数因子必用Pollard-Rho;已知p+q和pq用韦达定理。
quality: high
---

## 题目列表

1道密码学:RSA带噪声hint攻击

## 关键考点

### 数学建模
- 加密代码:
  ```python
  p, q = getPrime(1024), getPrime(1024)
  n = p*q
  noise = getPrime(40)  # 关键:40位小素数
  tmp1 = noise*p + noise*q
  tmp2 = noise*noise
  hint = p*q + tmp1 + tmp2
  c = pow(m, e, n)
  ```

### 关键关系推导
- hint = p*q + noise*p + noise*q + noise²
- hint = n + noise*(p + q + noise)
- **hint - n = noise × (p + q + noise)**
- 因noise仅40位,可用Pollard-Rho分解大整数hint-n找到noise因子

### 攻击步骤
1. 计算d = hint - n
2. Pollard-Rho找40位素因子,候选30≤bit_length≤60+is_prime
3. 验证`is_square((S - noise)² - 4*n)` (判别式为完全平方)
4. 命中noise=942430120937
5. S = (hint - n) // noise
6. spq = S - noise (p+q)
7. D = spq² - 4n (判别式)
8. t = isqrt(D)
9. p = (spq + t) // 2
10. q = (spq - t) // 2
11. 验证p*q == n
12. phi = (p-1)*(q-1),d = e⁻¹ mod phi
13. m = c^d mod n
14. long_to_bytes(m) → flag

### flag
- LitCTF{db6f52b9265971910b306754b9df8b76}

## 实战价值
- 任何hint先转成数学表达式,识别未知量
- 小素数因子必用Pollard-Rho(不是直接除)
- p+q已知 + pq已知 → 韦达定理 → p,q
- Miller-Rabin + isqrt + egcd 三大工具是RSA攻击的底层依赖
