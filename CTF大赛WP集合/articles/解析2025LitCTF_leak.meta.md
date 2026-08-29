---
title: 解析2025LitCTF leak
contest: LitCTF 2025
year: 2025
difficulty: hard
vuln_type: crypto_rsa
tags: [RSA-dp-leak, partial-key-exposure, Coppersmith, LLL, lattice-attack, bivariate, small-root, CRT-RSA, side-channel]
attack_chain:
- 题目生成2048位RSA,e=101位素数,泄露dp的高841位,hint=dp>>180
- 未知部分:0≤x<2^180 (约1.5×10^54种可能),1≤k<e (约10^30种可能)
- 数学建模:F(x,k) = A + e*x + k能被p整除,x≪p,k≪p
- 构造bivariate多项式F(x,k)=A+e*x+k,使用Coppersmith寻找小根
- LLL算法寻找格中的短向量
- 从短向量中恢复x和k,得完整dp
- 验证dp*p在[p+1,p+0x100]范围,反推p,q
- 标准RSA解密得m
key_payload: LitCTF{...}
one_liner: LitCTF 2025 leak方向RSA dp高位泄露攻击深度解析,180位dp低位+LLL/Coppersmith寻找小根恢复完整dp,侧信道+实现漏洞双重视角。
lesson: RSA-CRT实现中泄露dp高位是致命的;Coppersmith小根攻击对(x≪n)的多项式F(x)有效;实际部署中应避免计算和存储dp。
quality: high
---

## 题目列表

1道密码学:RSA dp高位泄露

## 关键考点

### 数学建模
- 题目代码:
  ```python
  p, q, e = getPrime(1024), getPrime(1024), getPrime(101)
  n = p*q
  temp = gmpy2.invert(e, p-1)  # 计算dp = e^(-1) mod (p-1)
  c = pow(m, e, n)
  hint = temp >> 180  # 泄露dp的高841位
  ```

### 攻击原理
- dp = e^(-1) mod (p-1),即e*dp ≡ 1 (mod p-1)
- 存在k使得e*dp = k*(p-1) + 1
- 已知dp高位dp_high = dp >> 180
- 完整dp = dp_high * 2^180 + x (其中x是未知低180位)
- 代入:e*(dp_high * 2^180 + x) = k*(p-1) + 1
- 重排:e*dp_high*2^180 + e*x = k*p - k + 1
- 关键:bivariate多项式F(x,k) = A + e*x + k (mod p),其中A = e*dp_high*2^180 + k - 1
- 因x<2^180≪2^1024≈p,k<e≪p,使用Coppersmith方法找小根

### 攻击工具
- sage小根:`f = ...; f.monic(); f.small_roots(X=2^180, beta=0.4)`
- LLL格基规约
- 还原p后:q=n//p,标准RSA解密m=pow(c, d, n)

### 防护启示
- 避免计算/存储dp、dq等CRT参数
- 实施严格内存保护
- 及时清理敏感数据
- HSM硬件保护密钥
- 定期密钥轮换
- 经典案例:
  - 2008 OpenSSL Debian伪随机数(32768种可能)
  - 2013 Android Bitcoin钱包SecureRandom缺陷ECDSA签名可预测
  - 2010 PS3 ECDSA签名k重用导致私钥计算

## 实战价值
- RSA-CRT实现的安全性是密码学工程实践的核心
- 任何"小泄露"都要认真对待,小根攻击对2048位RSA也只需180位低位
- sage的small_roots是必备工具
- 部署侧:实施constant-time算法+内存保护+HSM
