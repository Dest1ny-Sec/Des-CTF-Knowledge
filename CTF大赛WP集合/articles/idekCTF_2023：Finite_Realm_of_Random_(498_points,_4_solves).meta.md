---
title: idekCTF 2023: Finite Realm of Random (498 points, 4 solves)
contest: idekCTF
year: 2023
difficulty: hard
vuln_type: crypto_rsa
tags: [galois-field, finite-field, frobenius, f127, gf32, conjugates, freshmen-dream, sage]
attack_chain:
  - L = F_127^32 (Galois 域)
  - 32 字符分块编码为多项式系数
  - 5 次伽罗瓦共轭变换 f → f^(127^k)
  - 利用 Freshman's Dream 公式 φ(r2) = φ(r1)^(p^k)
  - 32 个共轭尝试还原
  - ASCII 范围验证
  - 找到 4 个相容块拼成 flag
key_payload: Frobenius 幂 + Freshman's Dream + 32 共轭爆破
one_liner: idekCTF 2023 高分密码学题，Galois 域上多项式共轭变换 + Freshman's Dream 还原。
lesson: 有限域上 (a+b)^p = a^p + b^p 的 Freshman's Dream 是处理 Frobenius 幂的关键。
quality: high
---

idekCTF 2023 Black Bauhinia 战队 WP，作者 high-quality 数学密码学解法。

**题面**
> I took a flag, and shuffled it. I took a part, and randomized it. I took the bits and pieces, and scattered them across the field.

**数学模型**
- L = F_127^32
- 32 字节分块编码为多项式：`c = c0 + c1·g + c2·g^2 + ... + c31·g^31`
- 5 次迭代：
  1. 选 r1, r2 共享最小多项式
  2. 找 φ(X) ∈ F_127[X]，deg ≤ 31，φ(r1) = f
  3. 替换 f → φ(r2)
- 输出最终 f

**核心观察**（Lemma）：
r1, r2 共享最小多项式 → r2 = σ(r1)，其中 σ 是 Galois 群元素。
Gal(F_p^n / F_p) = ⟨Frob_p⟩ ≅ Z/nZ
所以 r2 = r1^(p^k) for some 0 ≤ k < 32。

**关键推导**（Claim）：
- φ(r2) = φ(r1)^(p^k) = f^(p^k)
- 因为 di ∈ F_127，di^(p^k) = di（Freshman's Dream）
- 所以 step (2) 实际就是 f → f^(p^k)

**Sage 解法**
```python
L = GF(127)
for i in range(5):
    L = L['x'].irreducible_element(2, algorithm='random').splitting_field(f't{i}')

ct = bytes.fromhex(open('out.txt', 'r').read())
blocks = [L(list(map(int, ct[i:i + L.degree()]))) for i in range(0, len(ct), L.degree())]

def convert(poly):
    return bytes(map(int, poly.polynomial().coefficients()))

for c in blocks:
    for i in range(32):
        r = bytes(vector(c^(127^i)))
        if all(32 <= t < 127 or t == 0 for t in r):
            print(r.decode())
```

**flag**：`idek{4nd_7hu5_5p0k3_G4!015:_7h3_f1n1t3_r34Lm_sh4ll_n07_h4rb0ur_r4nd0mn355,_0n!y_7h3_fr0b3n1u5__}`

整题把"看似随机的 Galois 变换"用代数化成"32 种共轭 + 试错"，思路漂亮。
