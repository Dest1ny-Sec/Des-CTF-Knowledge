---
title: 2024 羊城杯 Crypto AK 篇（DASCTF 套题）
contest: 2024 羊城杯粤港澳大湾区网络安全大赛
year: 2024
difficulty: medium
vuln_type: [lattice, ecdsa, crypto_rsa]
tags: [Hessian curve, EllipticCurve_from_cubic, discrete_log, 自定义曲线离散对数, AES-CBC SHA256, RSA padding, RSA Iroot, bcactf rsa-is-broken]
attack_chain:
  - 识别 Hessian curve ax³+y³+1=dxy 公式还原 d
  - EllipticCurve_from_cubic 升维到 Weierstrass 再 discrete_log
  - 小阶曲线穷举 i ∈ [0,1000] 比对 P 还原乘数
  - 标准 ECC curve 离散对数 P.log(G)
  - k 已知 → SHA256(key)[:16] + AES-CBC(iv) 解密
  - 短密文 m=c^d mod n → 加 n*256 跳到 DASCTF{ 前缀
  - 大整数 n 用 iroot(n,2) 取整 + next_prime 试 p
key_payload: "PR.<d>=PolynomialRing(Zmod(p)); f=a*gx^3+gy^3+1-d*gx*gy; f.roots()"
one_liner: 把 5 道 DASCTF 套题串成一篇——Hessian 曲线、自定义曲线离散对数、ECC log、AES 派生、bcactf 原题搬运、RSA sqrt+CRT，每题一段解题脚本。
lesson: Hessian curve 化简到 Weierstrass 是 SageMath 一行 EllipticCurve_from_cubic 的事；CTF Crypto 真题常把 bcactf / corCTF 等国外比赛原题直接搬来当套题，看 flag 样式就能秒判出处。
quality: high
---

# 2024 羊城杯 Crypto AK 篇

DASCTF 经典套题风格 5 道打包：

1. **TH_Curve** 自定义 Hessian curve `ax³+y³+1 = d·x·y`（a=2、a=46 两种），先用 `f=a*gx^3+gy^3+1-d*gx*gy` 在 Zmod(p) 上解出 d=8817…7200，再用 `R.<x,y,z>=Zmod(p)[]` + `EllipticCurve_from_cubic` 把 cubic 升到 Weierstrass，`P.discrete_log(Q)` 得 m=525729205728344257526560548008783649，转 long_to_bytes 出 flag。
2. **小阶自定义曲线**：a=46 d=20 p1=8261…837，穷举 i ∈ [0,1000] 跑自写 mul_curve 比对 P1/Q1 出乘数。
3. **标准 ECC**：y²=x³-35x+98 在 GF(770311352827455849356512448287) 上 `P.log(G)` 得 k=2951856998192356。
4. **AES 派生**：SHA256(str(k).encode())[:16] 作 key，iv=0xbae1…07d6，AES-CBC 解密得 `DASCTF{THe_C0rv!_1s_Aw3s0me@!!}x01`。
5. **bcactf rsa-is-broken 搬运题**：c 短 + n 给出 p、q，m=pow(c,d,n) 后用 `m%256 != 125`（flag 末位 `}` = 0x7D=125）反复加 n，再用 `b'DASCTF{' + b'0'*` 长度试探 + `jump=n*256` 跳到合法字符集。
6. **大 RSA sqrt**：`p=iroot(n,2)[0]; p=next_prime(n//p);` 直接分解，再 normal RSA 解 `DASCTF{Ot2N63D_n8L6kJt_f40V61m_zS1O8L7}`。

## 关键技巧
- **Hessian → Weierstrass**：SageMath 自带 `EllipticCurve_from_cubic(morphism=True)`，免手撕同构映射。
- **bcactf 原题移植**：crypto 圈常互搬，flag 前缀 `bcactf` 还在但 flag 改 `DASCTF{...}`，识别套路。
- **RSA padding 解码**：已知 m ≡ c^d mod n，加 n 的倍数试探 flag 边界。
