---
title: 第三届"陇剑杯"网络安全大赛初赛-夺旗闯关赛WriteUp
contest: 第三届陇剑杯初赛
year: 2025
difficulty: hard
vuln_type: crypto_rsa
tags: [陇剑杯, Weil配对vs Tate, F_{p^2}扩域, j=0椭圆曲线y^2=x^3+1, r-子群基, 离散对数映射表, Miller loop, 国产密码学]
attack_chain: 解析output.txt得a/r/P/Q/gift/n/c→构造F_{p^2}扩域→E0:y^2=x^3+1 (j=0)→r-子群P_r/Q_r→Weil配对(w_base)→预计算j映射表→每个gift点对还原E'→Weil配对w1→查表得j→x_byte = j*inv(2^a) mod r→pp=n/pp→RSA解密
key_payload: "Weil配对 vs Tate配对;F_{p^2} y^2=x^3+1;j=0 E0;r-子群基co_r=(p+1)/r;Miller loop;deg φ=2^a*x;x_byte=j*inv(2^a) mod r;flag{S1mple_Is0geNy_7r1ck_t0_Recov3r_Fla9}"
one_liner: 第三届陇剑杯初赛夺旗闯关：F_{p^2}扩域Weil配对+RSA双线性对密码学难题
lesson: Weil配对比Tale配对值会抵消规范化常数；r-子群基co_r=(p+1)/r；预计算j映射表
quality: high
---

# 第三届"陇剑杯"网络安全大赛初赛-夺旗闯关赛WriteUp

**赛事**：第三届陇剑杯初赛-夺旗闯关赛（2025）

**平凉关卡-RSA.ios（密码学）**：

**核心**：**Weil 配对 vs Tate 配对**（F_{p^2}扩域）

**思路要点**：
1. 从 output.txt 解析 a, r, P, Q, gift[], n, c
2. 构造 **F_{p^2}**（i^2 = -1）与 E0: y^2 = x^3 + 1 (j=0)
3. 取r-子群：P_r = ((p+1)/r)*P, Q_r = ((p+1)/r)*Q
4. 用 **Weil 配对**而不是 Tate 配对：
   - e'_r(φ(P_r), φ(Q_r)) = e_r(P_r, Q_r)^{deg φ}
   - **deg φ = 2^a * x**（x 是待求字节）
   - Weil 配对比值会抵消规范化常数
5. 对每个 gift 的 (φ(P), φ(Q)) 还原出 E': y^2 = x^3 + A'x + B'
6. 计算 e'_r，做离散对数求 deg φ (mod r)
7. x = deg φ * inv(2^a, r) (mod r)，且 1..255
8. 拼回小端得到 pp = p
9. 分解 n = p*q 并 RSA 解密得到 flag

**核心代码**：
```python
class Fp2:
    """表示 a*i + b"""
    def __init__(self, a, b):
        self.a = a % MOD; self.b = b % MOD
    def __mul__(self, other):
        ai = (self.a*other.b + self.b*other.a) % MOD
        br = (self.b*other.b - self.a*other.a) % MOD
        return Fp2(ai, br)
    def inv(self):
        den = (self.a*self.a + self.b*self.b) % MOD
        invden = pow(den, -1, MOD)
        return Fp2(-self.a*invden, self.b*invden)
    def __pow__(self, e):
        # 快速幂
        ...

def weil_pairing_red(self, P, Q, r):
    # e_r(P,Q) = (-1)^r * f_{r,P}(Q) / f_{r,Q}(P)
    fPQ = self.miller_raw(P, Q, r)
    fQP = self.miller_raw(Q, P, r)
    val = fPQ / fQP
    if r % 2 == 1: val = val * Fp2(0, -1)  # 乘(-1)
    return val ** ((MOD*MOD - 1) // r)

# 主循环
E0 = EllipticCurve(0, 1)  # y^2 = x^3 + 1
co_r = (p + 1) // r
P_r = E0.mul(P0, co_r)
Q_r = E0.mul(Q0, co_r)
w_base = E0.weil_pairing_red(P_r, Q_r, r)  # 基准配对

# 预计算j映射表
table = {}
val = Fp2(0, 1)
for j in range(r):
    table[(val.a, val.b)] = j
    val = val * w_base

# 逐 gift 还原
for (phiP_xy, phiQ_xy) in gift_points:
    # 由两点解 E': y^2 = x^3 + A'x + B'
    S1 = y1*y1 - x1*x1*x1
    S2 = y2*y2 - x2*x2*x2
    A1 = (S1 - S2) / (x1 - x2)
    B1 = S1 - A1*x1
    E1 = EllipticCurve(A1, B1)
    # 还原r-子群并配对
    phiP_r = E1.mul(phiP, co_r)
    phiQ_r = E1.mul(phiQ, co_r)
    w1 = E1.weil_pairing_red(phiP_r, phiQ_r, r)
    j = table.get((w1.a % MOD, w1.b % MOD))
    # 求解 x_byte
    x_byte = (j * inv_mod(pow(2, a, r), r)) % r
    xs_le.append(x_byte)

# 拼回 pp
pp = 0
for i, b in enumerate(xs_le):
    pp |= (b << (8*i))
qq = n // pp
phi_n = (pp - 1) * (qq - 1)
d = inv_mod(e, phi_n)
m = pow(c, d, n)
flag = long_to_bytes(m)
```

**flag**：`flag{S1mple_Is0geNy_7r1ck_t0_Recov3r_Fla9}`

**核心技术**：
- F_{p^2} 扩域（i^2 = -1）
- 椭圆曲线 y^2 = x^3 + 1 (j=0)
- **Weil 配对 vs Tate 配对**（抵消规范化常数）
- r-子群基 co_r = (p+1)/r
- Miller loop + 最终指数
- 预计算 j 映射表 → 离散对数
- deg φ = 2^a * x
- x_byte = j * inv(2^a, r) mod r

**质量评估**：高（前沿密码学 + Weil配对 + RSA联用）
