---
title: 2025 LitCTF ez_math - 2×2 矩阵幂 Cayley-Hamilton 攻击
contest: LitCTF
year: 2025
difficulty: hard
vuln_type: crypto_rsa
tags:
- matrix-power
- Cayley-Hamilton
- finite-field
- quadratic-extension
- GF-p2
- quotient-ring
- RSA-matrix
- modular-inverse
- characteristic-polynomial
attack_chain:
- '加密: A = [[flag, getPrime], [getPrime, getPrime]]; B = A^e mod p (e=65537, p 512-bit 素数)'
- '关键: flag 在 A[0][0]'
- 'Cayley-Hamilton: M² - (tr M)·M + (det M)·I = 0 → M^n = p_n·M - (det M)·p_{n-1}·I'
- '特征多项式: χ_A(x) = x² - (tr A)x + det A'
- '特征值: B 的特征值 = A 特征值的 e 次方'
- 在 GF(p²)* 中, gcd(e, p²-1) = 1 → 映射 x → x^e 是双射
- '计算私钥: d = inverse_mod(e, p²-1)'
- '商环: R = F_p[X]/(X² - s1·X + s2), X 模拟 B 的特征值'
- 计算 X^d = β + α·X (商环中快速幂)
- '恢复 A: A = α·B + β·I'
- flag = A[0][0] = LitCTF{13dd217e-9a67-4093-8a1b-d2592c45ba82}
key_payload: '''A = α·B + β·I + 商环 mul + pow_poly + d = inverse_mod(e, p²-1)'''
one_liner: LitCTF 2025 ez_math：2×2 矩阵 A^e mod p 的 Cayley-Hamilton 攻击，把高次幂降维到商环多项式求逆。
lesson: Cayley-Hamilton 定理 + 二次扩域是矩阵密码的通用解法；商环运算避开了复杂特征值计算。
quality: high
full_path: 解析2025LitCTF_ez_math.full.md
meta_path: 解析2025LitCTF_ez_math.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '2025 LitCTF ez_math - 2×2 矩阵幂 Cayley-Hamilton 攻击。LitCTF 2025 ez_math：2×2 矩阵 A^e mod p 的 Cayley-Hamilton 攻击，把高次幂降维到商环多项式求逆。。关键路径：加密: A = [[flag, getPrime], [getPrime, getPrime]]; B = A^e mod p (e=65...'
category: crypto
subcategory: rsa
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/278432.html
reasoning_chain:
- 题目B=A^e mod p, A[0][0]=flag → e=65537, p 512-bit 素数 → 触发点：矩阵幂加密
- 假设：Cayley-Hamilton定理 M²-(tr M)M+(det M)I=0 → 动作：把高次幂降维到线性
- B的特征值μ=A特征值λ的e次方 → 在GF(p²)中阶p²-1 → gcd(e,p²-1)=1 → 双射
- 动作：d=inverse_mod(e, p²-1) → 假设：可在特征值空间求逆
- 动作：构造商环R=F_p[X]/(X²-s1*X+s2), X模拟B特征值 → 触发点：商环多项式求幂
- X^d=β+α*X(pow_poly in商环) → A=α·B+β·I → 假设：恢复原始矩阵
- 观察：flag=A_recovered[0,0] → LitCTF{13dd217e-9a67-4093-8a1b-d2592c45ba82}
failed_attempts:
- 试图直接在GF(p)中求B^(1/e) → 失败：p阶为p-1不含B的e次根需要扩域
- 试图求A特征值再开e次方 → 失败：特征值可能在GF(p²)内,GF(p)中无解
- 试图用numpy矩阵求逆 → 失败：模p下无浮点,需用商环多项式
key_observations:
- Cayley-Hamilton定理把M^n降维成p_n·M - det·p_{n-1}·I的线性组合
- 二次扩域GF(p²)是处理矩阵特征值的最低成本
- 商环F_p[X]/(X²-s1·X+s2)避开显式特征值计算
- gcd(e, p²-1)=1 时 x→x^e 是双射,这是 e 不可约的判定
prerequisites:
- Cayley-Hamilton定理
- 二次扩域GF(p²)运算
- 商环F_p[X]/(X²-s1·X+s2)
- 矩阵模幂基础
---
# 解析2025LitCTF ez_math

> 原文: https://www.ctfiot.com/278432.html
> ID: 278432

2×2矩阵”取e次幂”的逆向

从 Cayley–Hamilton 到二次扩域一把通关（附完整Python代码）

题目概述

今天我们来分析一道极具挑战性的CTF密码学题目。这道题目基于2×2矩阵的高次幂运算，要求我们逆向破解加密过程。题目看似简单——已知B=A^e mod p，求A——但背后涉及了深刻的数学理论：Cayley-Hamilton定理、有限域扩域和矩阵群理论。

本文将通过完整的理论推导和实际复现，带你从数学原理到代码实现，彻底掌握这类矩阵密码题的解题精髓。

题目分析

首先，让我们看看题目给出的加密代码：

fromsage.allimport*fromCrypto.Util.numberimport*fromuuidimportuuid4flag =b'LitCTF{'+ str(uuid4()).encode() +b'}'flag = bytes_to_long(flag)len_flag = flag.bit_length()e =65537p = getPrime(512)P = GF(p)A = [[flag, getPrime(len_flag)], [getPrime(len_flag), getPrime(len_flag)]]A = matrix(P, A)B = A ** eprint(f"e ={e}")print(f"p ={p}")print(f"B ={list(B)}".replace('(','[').replace(')',']'))

加密流程分析

从代码中我们可以看出加密过程：

Flag准备：将flag转换为长整数

密钥生成：选择512位素数p作为模数，e=65537作为公钥指数

矩阵构建：构造2×2矩阵A，其中A[0][0]是flag，其他元素是随机素数

矩阵加密：计算B = A^e mod p

输出版本：给出e、p和B的值

tr M = M[0][0] + M[1][1] 是矩阵的迹

det M 是矩阵的行列式

I 是单位矩阵

p₀ = 0, p₁ = 1

pₙ = (tr M)·pₙ₋₁ – (det M)·pₙ₋₂

A的特征多项式：χ_A(x) = x² – (tr A)x + det A

B的特征值：μ₁ = λ₁^e, μ₂ = λ₂^e

在GF(p²)*（p²阶乘法群）中，当gcd(e, p²-1) = 1时

映射x → x^e是双射，其逆映射为x → x^d，其中d·e ≡ 1 (mod p²-1)

验证可逆性：确认gcd(e, p²-1) = 1

计算私钥：d = e^(-1) mod (p²-1)

构建商环：基于B的特征多项式

多项式幂运算：在商环中计算X^d

提取系数：得到α和β

矩阵重构：A = α·B + β·I

提取flag：从A[0][0]提取结果

商环运算：mul函数实现了商环中的乘法，自动处理X²的降次

快速幂：pow_poly函数在商环中计算多项式的幂次

系数提取：beta, alpha = pow_poly((0, 1), d)得到关键的α和β

矩阵重构：A = α·B + β·I恢复原始矩阵

降维：将高次幂运算降维到一次多项式

线性化：使非线性问题转化为线性问题

结构保持：保持了矩阵的代数结构

特征域模拟：X的行为完全模拟B的特征值

运算封闭：所有运算都在有限域内进行

降次自动：X²自动降次为一次多项式

复杂的特征值计算

数值不稳定性

浮点数精度问题

GF(p²)*的阶是p²-1

2×2矩阵的特征值最多需要二次扩域

当gcd(e, p²-1)=1时，映射x→x^e在GF(p²)*上是双射

存在性：逆映射必定存在

唯一性：解是唯一的

有效性：算法保证收敛

退化情况处理

如果B是数量矩阵（与I成比例），商环退化为1维

此时需要特殊处理，但本题不会出现

大整数运算优化

使用快速幂算法：O(log d)时间复杂度

模运算中间结果，避免溢出

Python的任意精度整数优势明显

数值验证的重要性

验证gcd条件

确认e·d ≡ 1 (mod p²-1)

最终验证A^e = B

理论深度：从Cayley-Hamilton定理到有限域扩域，体现了抽象代数在密码学中的强大应用

方法优雅：商环计算避免了复杂的数值计算，展现了代数方法的简洁和高效

实用性强：纯Python实现让理论知识可以直接应用于实际CTF比赛

启发性大：这种思路可以扩展到更高维度的矩阵和其他代数结构

数学直觉的培养：学会从代数结构的角度思考密码问题

工具的掌握：熟练运用SageMath等数学工具

思维的训练：培养抽象思维和逻辑推理能力

视野的拓展：了解现代密码学研究的前沿方向


```
fromsage.allimport*fromCrypto.Util.numberimport*fromuuidimportuuid4flag =b'LitCTF{'+ str(uuid4()).encode() +b'}'flag = bytes_to_long(flag)len_flag = flag.bit_length()e =65537p = getPrime(512)P = GF(p)A = [[flag, getPrime(len_flag)], [getPrime(len_flag), getPrime(len_flag)]]A = matrix(P, A)B = A ** eprint(f"e ={e}")print(f"p ={p}")print(f"B ={list(B)}".replace('(','[').replace(')',']'))
e = 65537p = 8147594556101158967571180945694180896742294483544853070485096002084187305007965554901340220135102394516080775084644243545680089670612459698730714507241869B = [[2155477851953408309667286450183162647077775173298899672730310990871751073331268840697064969968224381692698267285466913831393859280698670494293432275120170, 4113196339199671283644050914377933292797783829068402678379946926727565560805246629977929420627263995348168282358929186302526949449679561299204123214741547], [3652128051559825585352835887172797117251184204957364197630337114276860638429451378581133662832585442502338145987792778148110514594776496633267082169998598, 2475627430652911131017666156879485088601207383028954405788583206976605890994185119936790889665919339591067412273564551745588770370229650653217822472440992]]
M² - (tr M)·M + (det M)·I = 0
Mⁿ = pₙ·M - (det M)·pₙ₋₁·I
B = u·A + v·I
A = α·B + β·I
gcd(65537, p²-1) = 1 ✓
μ^d = λ
X² - (tr B)·X + det B = 0
X^d = β + α·X
A = α·B + β·I
fromsage.allimport*fromCrypto.Util.numberimport*# 题目参数e =65537p =8147594556101158967571180945694180896742294483544853070485096002084187305007965554901340220135102394516080775084644243545680089670612459698730714507241869B_data = [[2155477851953408309667286450183162647077775173298899672730310990871751073331268840697064969968224381692698267285466913831393859280698670494293432275120170,4113196339199671283644050914377933292797783829068402678379946926727565560805246629977929420627263995348168282358929186302526949449679561299204123214741547], [3652128051559825585352835887172797117251184204957364197630337114276860638429451378581133662832585442502338145987792778148110514594776496633267082169998598,2475627430652911131017666156879485088601207383028954405788583206976605890994185119936790889665919339591067412273564551745588770370229650653217822472440992]]# 构建有限域和矩阵P = GF(p)B = matrix(P, B_data)
# 计算群阶和私钥phi = p^2-1d = inverse_mod(e, phi)
# 解密A_recovered = B^dflag = long_to_bytes(int(A_recovered[0,0]))print(flag) # b'LitCTF{13dd217e-9a67-4093-8a1b-d2592c45ba82}'
# Python 3.x - 完整解题代码e =65537p =8147594556101158967571180945694180896742294483544853070485096002084187305007965554901340220135102394516080775084644243545680089670612459698730714507241869B11 =2155477851953408309667286450183162647077775173298899672730310990871751073331268840697064969968224381692698267285466913831393859280698670494293432275120170B12 =4113196339199671283644050914377933292797783829068402678379946926727565560805246629977929420627263995348168282358929186302526949449679561299204123214741547B21 =3652128051559825585352835887172797117251184204957364197630337114276860638429451378581133662832585442502338145987792778148110514594776496633267082169998598B22 =2475627430652911131017666156879485088601207383028954405788583206976605890994185119936790889665919339591067412273564551745588770370229650653217822472440992mod = p
# 计算 B 的迹和行列式s1 = (B11 + B22) % mod # tr(B)s2 = (B11 * B22 - B12 * B21) % mod # det(B)
# 商环 R = F_p[X]/(X^2 - s1*X + s2) 中的运算defmul(u, v): a, b = u c, d = v const = (a*c - (b*d % mod) * s2) % mod # X^2 ≡ s1*X - s2 xcoef = (a*d + b*c + (b*d % mod) * s1) % mod return(const, xcoef)defpow_poly(base, exp): res = (1,0) # 1 b = base eexp = exp whileeexp >0: ifeexp &1: res = mul(res, b) b = mul(b, b) eexp >>=1 returnres
# 验证可逆性并计算私钥frommathimportgcdassertgcd(e, p*p -1) ==1d = pow(e,-1, p*p -1)
# 计算 X^d = beta + alpha*Xbeta, alpha = pow_poly((0,1), d)
# 恢复矩阵 A = alpha*B + beta*IA11 = (alpha * B11 + beta) % modA12 = (alpha * B12) % modA21 = (alpha * B21) % modA22 = (alpha * B22 + beta) % mod
# 提取flagdeflong_to_bytes(n): bl = (n.bit_length() +7) //8 returnn.to_bytes(bl,'big')flag = long_to_bytes(A11).decode()print(flag) # LitCTF{13dd217e-9a67-4093-8a1b-d2592c45ba82}
LitCTF{13dd217e-9a67-4093-8a1b-d2592c45ba82}
# 正确性验证（可选）defmat_mul(M, N, mod): return[ [(M[0][0]*N[0][0] + M[0][1]*N[1][0]) % mod, (M[0][0]*N[0][1] + M[0][1]*N[1][1]) % mod], [(M[1][0]*N[0][0] + M[1][1]*N[1][0]) % mod, (M[1][0]*N[0][1] + M[1][1]*N[1][1]) % mod], ]defmat_pow(M, e, mod): R = [[1,0],[0,1]] A = [[M[0][0], M[0][1]],[M[1][0], M[1][1]]] whilee >0: ife &1: R = mat_mul(R, A, mod) A = mat_mul(A, A, mod) e >>=1 returnR
# 验证 A^e = BA = [[A11, A12],[A21, A22]]B_recomputed = mat_pow(A, e, p)assertB_recomputed[0][0] == B11andB_recomputed[0][1] == B12assertB_recomputed[1][0] == B21andB_recomputed[1][1] == B22
私钥d正确计算：e·d ≡ 1 (mod p²-1)矩阵重构成功：A = α·B + β·IFlag正确提取：A[0][0] = 2738291505...验证通过：A^e = B
A² = (tr A)·A - (det A)·I
LitCTF{13dd217e-9a67-4093-8a1b-d2592c45ba82}
```
