---
title: 春秋杯WP｜2023春秋杯春季赛之crypto篇
contest: 春秋杯2023春季赛
year: 2023
difficulty: hard
vuln_type: crypto_rsa
tags: [Pell方程, 连分数, 二项式定理, 恶意ECDH, 超椭圆曲线, 双线性对, 离散对数]
attack_chain: 佩尔Pell方程连分数求特解→二项式定理逆推离散对数flag1→ECDHE参数w/a/b/x已知+线性组合z=k1*G-a*k1*Y-wt*G-bY逆推k2→AES-ECB解密flag2→超椭圆曲线Jacobian离散对数求r→AES-ECB解密flag3
key_payload: "continued_fraction(sqrt(1117));flag1=(enc1-1)//n^2*inverse(233,n)%n;z = M1 - w*t*G - a*x*M1 - b*x*G;k2 = sha256(str(z[0]).encode()).digest()[:6];D2=r*D1;J(HC((sx,sy)))"
one_liner: 春秋杯2023春季赛crypto三题：Pell方程+恶意ECDH+超椭圆曲线Jacobian
lesson: Pell方程连分数+ECDHE参数已知时逆推k2+超椭圆曲线Jacobian是近年crypto难点
quality: high
---

# 春秋杯WP｜2023春秋杯春季赛之crypto篇

**赛事**：春秋杯2023春季赛 crypto方向

**三题详解**：

**1. Pell方程（佩尔方程 + 二项式定理逆推离散对数）**
- enc1 = pow(233*n^2+1, part1, n^3)
- enc2 = pow(y*n+1, part2, n^3)
- n为2048bit大整数，直接求离散对数不可行
- 用二项式定理在模n^2/n下分析
- **D=1117, x^2 - D*y^2 = 1**：用连分数求小特解，线性迭代求所有解
- flag1: `(enc1-1) // n^2 * inverse(233, n) % n`
- flag2: `(enc2%n^2 - 1) // n * inverse(yi, n) % n`
- flag: `flag{11e89e28-4e27-47f0-a7c7-8e66c18881be}`

**2. 恶意ECDH**
- w/a/b/x生成参数：`(31889563, 31153, 28517, 763220531)`
- 椭圆曲线E: y^2 = x^3 + Ax + B (A=1064988096, B=802063264240, P=12565...)
- 已知w/a/b/x/Y/M1/M2/B_ + t=1
- **z = (k1 - w*t)*G + (-a*k1 - b)*Y** 展开
  - z = M1 - a*x*M1 + (-w*t*G - b*Y)
  - 全部已知 → 计算k2
- k2 = sha256(str(z[0]).encode()).digest()[:6]
- 共享密钥 = k_rec * M2
- AES-ECB解密
- flag: `flag{63259ab8-4916-4095-8888-d92c2b003e18}`

**3. 超椭圆曲线（Hyperelliptic Curve）**
- p = 2^256随机素数
- g=3, sx随机
- 多项式f生成超椭圆曲线HC, sy = f(sx).nth_root(2)
- Jacobian群 J = HC.jacobian()(GF(p))
- D1 = randint * J((sx, sy))
- D2 = r * D1
- 已知D1, D2, 求r（Jacobian上的离散对数）
- key = sha256(str(r))
- AES-ECB解密
- 难点：超椭圆曲线Jacobian上的DLP非常规ECC DLP

**核心知识点**：
- Pell方程 x^2 - Dy^2 = 1 连分数+线性迭代
- 椭圆曲线参数已知时逆推私有标量
- 超椭圆曲线Jacobian的DLP（Hyperelliptic Curve Cryptography）

**质量评估**：高（三题payload + flag完整）
