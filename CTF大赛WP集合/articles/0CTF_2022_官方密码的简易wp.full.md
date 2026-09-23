---
title: 0CTF 2022 官方密码的简易 WP (官方题解)
contest: 0CTF/TCTF 2022
year: 2022
difficulty: hard
vuln_type:
- crypto_rsa
- lattice
- block_cipher
tags:
- Coppersmith
- smooth-integers
- CRT-decoding
- AEAD
- algebraic-attack
- SBOX
- Gröbner-basis
- partial-key-exposure
- RLWE
- IPFE
- Feistel
- SPN
- Boomerang-attack
- Yoyo-tricks
- Matrix
- LU-decomposition
attack_chain:
- 'real-magic-dlog: Boneh 2000 CRT decoding 在短区间找 smooth 整数 → DLP 60s 限时'
- 'Leopard: 自研 AEAD (基于 Panther)，SBOX = 55/x + 186 over GF(2^8)，差分故障分析恢复密钥'
- 'ezRSA++: CRT-RSA dp/dq 105 bit 已知 55 LSB，Partial Key Exposure Attack'
- 'Login: RLWE-based IPFE，l 维向量编码多项式，但 l=1 → 线性代数恢复 y'
- 'Chimera: Feistel+SPN+perm 混合加密，差分密码 + Yoyo tricks + Boomerang attack 8192 次 oracle'
- 'ezMat: LU 分解 + 线性方程 + sha256 校验恢复 flag 字节'
key_payload: ''
one_liner: 0CTF 2022 五道官方密码题，覆盖 DLP/AEAD/RSA/RLWE/Feistel+SPN
lesson: 顶级 CTF 密码学题都是最新研究 + 论文级攻击；Coppersmith / Gröbner / DFA 是常见方法
quality: high
full_path: 0CTF_2022_官方密码的简易wp.full.md
meta_path: 0CTF_2022_官方密码的简易wp.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '0CTF 2022 官方密码的简易 WP (官方题解)。0CTF 2022 五道官方密码题，覆盖 DLP/AEAD/RSA/RLWE/Feistel+SPN。关键路径：real-magic-dlog: Boneh 2000 CRT decoding 在短区间找 smooth 整数 → DLP 60s 限时 → Leopard: 自研 AEAD (基于 Panther)，SBOX = 55/x...'
category: crypto
subcategory: rsa
subcategories:
- rsa
- lattice
- symmetric
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/58224.html
reasoning_chain:
- 触发点：5 道 0CTF 2022 官方密码题 + 2021 系列 9 道，每题标 ★-★★★★ 难度，覆盖 DLP/AEAD/RSA/RLWE/Feistel-SPN → 假设：每题都是最新论文级攻击
- real-magic-dlog trigger：60s 限时 + HITCON magic dlog 变种 → 假设：Boneh 2000 CRT decoding 在短区间找 smooth → 动作：实现论文 [1] 算法
- 观察：设 S = product of first 45 primes 平滑率最高，剩余大因子 60s 内能 Pohlig-Hellord DLP → 下一步：Leopard
- Leopard trigger：给定 (固定 pt, ct, fault_ct) + 300s → 假设：差分故障分析 DFA 恢复 AEAD 密钥 + IV
- 动作：读 SBOX 源码 → 观察：SBOX[x] = 55/x + 186 在 GF(2^8) 上，线性变换在 GF(2^8) 而非 GF(2)^8（区别于 AES）
- 假设：fault 注入前 state 部分已知（= ct 字节），其余当变量 → 动作：Sage 模拟 state update
- 观察：方程 55/f(x0,...)+186 = ct[i]+pt[i]，Sage 输出分子 → 多变量多项式
- 动作：注入多次 fault 收集足够方程 → Gröbner basis 求根 → 观察：300s 内恢复 key + IV
- ezRSA++ trigger：N ~2000 bits, dp/dq 105 bits, 给 55 LSBs → 假设：Partial Key Exposure Attack 论文 [1] → 动作：实现 May et al al. 算法
- Login trigger：RLWE-IPFE 原方案 l 维向量 → l 多项式，题里 l=1 → 假设：X*Y 系数线性代数恢复 y → 动作：解线性方程组
- Chimera trigger：Feistel+SPN+perm 混合，8192 次 oracle + 300s → 假设：差分密码 + Yoyo tricks + Boomerang 三论文组合 → 动作：构造 differential path
failed_attempts:
- real-magic-dlog 设小 S →失败：平滑率太低，60s 内解不完 DLP
- Leopard 不引入 fault 只看 (pt, ct) → 失败：方程不够解 Gröbner
- ezRSA++ 用 Coppersmith 整体攻击 → 失败：dp/dq 105 bit 太小，整体攻击不如 partial exposure
- Login 当标准 RLWE 设 (2,1) 还原 → 失败：l=1 时安全归零，线性代数是唯一路径
- Chimera 只跑 Feistel 差分 → 失败：单 Feistel 差分不满足 Yoyo 触发条件
key_observations:
- AEAD SBOX 是 GF(2^8) 还是 GF(2)^8 线性变换是 algebraic attack 关键分叉
- 差分故障分析（DFA）=已知 (pt, ct, fault_ct) → 故障前状态作变量 → 多项式方程组
- RSA CRT模式 dp/dq 短且部分 LSB 已知 → Partial Key Exposure Attack 优于整体 Coppersmith
- RLWE-IPFE 在 l=1 时退化为线性加密，X*Y 系数矩阵直接解 y
- Boomerang + Yoyo tricks 是高阶差分密码学的标准武器组合，用于 SPN 加密 oracle 攻击
prerequisites:
- AEAD 对称密码分析（SBOX 差分 + 故障分析）
- Boneh 2000 CRT decoding 论文基础
- RSA Coppersmith / Partial Key Exposure / Lattice
- SageMath Grögröbner basis 与 GF(2^8) 多项式运算
- 差分密码学 + Yoyo tricks + Boomerang attack 文献
---
# 0CTF 2022 官方密码的简易wp

> 原文: https://www.ctfiot.com/58224.html
> ID: 58224

My-Public-CTF-Challenges

This is the repository of some CTF challenges I made, maybe including the source code and solution.

ToC

0CTF/TCTF 2022

real magic dlog

Leopard

ezRSA++

Login

Chimera

0CTF/TCTF 2021 Finals

ezMat

ezHash

ezRSA

ezRSA+

halfhalf

0CTF/TCTF 2021 Quals

zer0lfsr-

zer0lfsr+

zer0lfsr++

0CTF/TCTF 2022

real-magic-dlog

Category: Crypto

Difficulty: ★

Solved: 66 / 158

Tag: Smoothness, Coppersmith

Details

Source

This challenge is based on HITCON CTF 2021 magic dlog, but we add a 60-seconds limit this time. According to its author @lyc, the intended solution is [1]. But many players solved it with simple brute-force attack, i.e., randomly generating numbers and hope it is smooth enough.

Solution

I underestimate the success rate of the original brute-force method, so it also works for this challenge. The intended solution is to implement the algorithm in [1]. But in our case, it can not guarantee the full smoothness of the output number, the number always contains one or two large factors. So, we hope these factors are not too large, then the DLP can be solved within 1 minute. Another trick is the parameter setting, the algorithm works better if we set S (for details, see [1]) as the product of first 45 primes, I don’t know why.

Reference

[1] Boneh, Dan. “Finding smooth integers in short intervals using CRT decoding.” Proceedings of the thirty-second annual ACM symposium on Theory of computing. 2000.

Leopard

Category: Crypto

Difficulty: ★★☆

Solved: 6 / 158

Tag: AEAD, Algebraic Attack

Details

Source

This challenge implements a homemade AEAD scheme named Leopard, which is inspired from an AEAD scheme called Panther [1]. Note that Panther suffers from a straightforward attack [2], while Leopard has been patched. And in this challenge, we are asked to apply the differential fault analysis on Leopard. Specifically, given a fixed plaintext, its ciphertext as well as a fault ciphertext, one should recover the secret key and IV within 300s.

Solution

There are at least three methods to solve this task.

Approach 1 (team More Smoked Leet Chicken): This is an algebraic attack, and it is the intended solution. The SBOX of Leopard is not generated in the same way as the SBOX of AES. One can check this wiki page, note that the linear transform is done over $\mathbb{F}{2}^8$. But in this challenge, one can figure out the linear transform is actually done over $\mathbb{F}{2^8}$, it can be represented as SBOX[x]=55/x+186. Now consider the internal state of the cipher just before the fault will be injected, partial state are known to us since they are equal to the ciphertext bytes, so we can treat the remaining unknown state bytes as variables over F28, then simulate the state update function locally. And we can get several equations in the form as 55/f(x_0,x_1,...)+186=ct[i]+pt[i], SageMath keeps these equations in fraction form, but we can extract the numerator part of the fraction, which yields a multivariate equation. After collecting enough equations, we can find the roots with Gröbner basis. The fault is used to providing more equations.

Approach 2 (team perfect r00t): This is a SAT-based solution, one can check here.

Approach 3 (other teams): This is a guess-and-determine attack, which exploits the internal state update function. Several players shared their codes in Discord channel, but there are no detailed writeups now. If you have a detailed analysis, please contact me 🙂

Reference

[1] Bhargavi, K. V. L., Chungath Srinivasan, and K. V. Lakshmy. “Panther: A Sponge Based Lightweight Authenticated Encryption Scheme.” International Conference on Cryptology in India. Springer, Cham, 2021.

[2] Boura, Christina, Rachelle Heim Boissier, and Yann Rotella. “Breaking Panther.” Cryptology ePrint Archive (2022).

ezRSA++

Category: Crypto

Difficulty: ★★★☆

Solved: 4 / 158

Tag: RSA, Coppersmith

Details

Source

This challenge is based on 0CTF/TCTF 2021 Finals ezRSA+. We are given an CRT-RSA public key where N and eare around 2000 bits. We also know both dp and dq are 105 bits, and we are given 55 LSBs of them.

Solution

Approach 1 (team idek): This is the intended solution, just implement the algorithm in the paper [1]. @gripingberry has released his neat [code] (https://gist.github.com/willfisher/79292934bf2a08cc41174619ae69a70c).

Approach 2 (team Super Guesser and team Straw Hat): Please read rkm’s writeup.

Reference

[1] May, Alexander, Julian Nowakowski, and Santanu Sarkar. “Partial Key Exposure Attack on Short Secret Exponent CRT-RSA.

Login

Category: Crypto

Difficulty: ★★☆

Solved: 2 / 158

Tag: Lattice, RLWE, IPFE

Details

Source

This challenge implements an RLWE-based inner-product functional encryption scheme. You have to login as player at first then login as admin to get flag. The scheme is modified from [1].

Solution

The original scheme encodes a l-dimension vector to l polynomials, and this is provably secure. But in this task, both the vectors x and y are treated as one polynomial X and Y, it is possible to recover y from the coefficients of the result X*Y with some linear algebra when x is known. One may refer to perfect r00t ‘s writeupfor detials

Reference

[1] Mera, Jose Maria Bermudo, et al. “Efficient lattice-based inner-product functional encryption.” IACR International Conference on Public-Key Cryptography. Springer, Cham, 2022.

Chimera

Category: Crypto

Difficulty: ★★★★☆

Solved: 0 / 158

Tag: Feistel, SPN, Boomerang Attack

Details

Source

This challenge implements a homemade block cipher named Chimera. The 16-bytes plain text will be encrypted by two parallel 4-rounds DES-like cipher, then permutated, and finally encrypted by a 4-rounds (without shift rows in first round) AES-like cipher. One can set one byte among the master keys of three components to a specified byte of flag. And the server provide an encryption oracle as well as a decryption oracle. The time limit is 300 seconds, and one can call encryption/decryption oracles for 16-bytes input plaintext at most 8192 times.

Solution

The intended solution is a combination of differential cryptanalysis of the Feistel cipher [1] and Yoyo tricks with the SPN [2], which can be regarded as a retracing boomerang attack [3]. The basic idea is to find a differential path of one of the Feistel cipher such that the non-zero bytes in the output differential after the permutation are placed in one column of the input to SPN, then the condition of Yoyo tricks will be satisfied. And one may hope when decryption, the input difference of another Feistel cipher are exactly zero, thus the right half of two plaintexts are the same. Once this happens, the differential path of the first Feistel cipher is likely activated, and we can extract some bytes of the first round key, since the input as well as the difference of the output of first round function are known. Detailed writeup is coming soon…

Reference

[1] Biham, Eli, and Adi Shamir. Differential cryptanalysis of the data encryption standard. Springer Science & Business Media, 2012.

[2] Rønjom, Sondre, Navid Ghaedi Bardeh, and Tor Helleseth. “Yoyo tricks with AES.” International Conference on the Theory and Application of Cryptology and Information Security. Springer, Cham, 2017.

[3] Dunkelman, Orr, et al. “The retracing boomerang attack.” Annual International Conference on the Theory and Applications of Cryptographic Techniques. Springer, Cham, 2020.

0CTF/TCTF 2021 Finals

ezMat

Category: Crypto

Difficulty: ★

Solved: 12 / 12

Tag: Matrix, Linear Algebra

Details

Source

This task is inspired from the challenge Onclude in Crypto CTF 2021. The ciphertext computes as E = L_inv * S * X = U * X = U * (A + R), we know E and R, need to recover A. And U is the LU decomposition of a secret matrix, A is a matrix which contains most of zero and flag bytes. We are also given a sha256 digest of flag.

Solution

Notice that U is a triangular matrix, and there are lots of zero elements in A, thus we may solve linear equations to recover most elements in A, then bruteforce the remaining bytes according to the given sha256 digest.

ezHash

Category: Crypto

Difficulty: ★★★☆

Solved: 3 / 12

Tag: Matrix, LPS Graph

Details

Source

The script implements an algorithm involves 2×2 matrix multiplication over Fp. Our input will be converted to base 5 sequence, then each time choose one of the six generator matrix multiple to the result according to the sequence. The server will generate a random matrix X per connection, we have 10 seconds to find an input which yields a matrix Y, where Y ≡ aX (mod p) for some a ∈ Fp.

Solution

In fact, the algorithm is a hash function based on LPS graph. This paper [1] describes a preimage attack, just implement it.

Reference

[1] Petit, Christophe, Kristin Lauter, and Jean-Jacques Quisquater. “Full cryptanalysis of LPS and Morgenstern hash functions.” International Conference on Security and Cryptography for Networks. Springer, Berlin, Heidelberg, 2008.

ezRSA

Category: Crypto

Difficulty: ★★

Solved: 11 / 12

Tag: RSA, Hint

Details

Source

The script generates a CRT-RSA key pair, where n is 2000 bits, e is 1000 bits, dp, dq, k, l are only 60 bits, then encrypt the flag. We are given the public key, encrypted flag and the lowest 10 bits of both dp dq as well as a magic number m = 1337 * k ** 4 + 7331 * l ** 3 + 73331 * k ** 2 + 13337 * l ** 2 + 7 * k * l + 2 * k + l.

Solution

Take 4th root of m // 1337 may get an approximation of k, then search in a small range, for each candidate k_bar, take 3th root of (m - 1337 * k_bar ** 4) // 7331 to get an approximation of l, then search again and use m to determine l and k. As k * p - k = e * dp - 1, we can recover p, then decrypt flag.

ezRSA+

Category: Crypto

Difficulty: ★★☆

Solved: 6 / 12

Tag: RSA, Lattice, Continued Fraction

Details

Source

Same as ezRSA, but no magic numebr m, and we get the lowest 12 bits of both dp dq.

Solution

Approach 1: After some arithmetic, we have e * e * X + e * Y + Z = W * n, where X = dp * dq,Y = dp * (l - 1) + dq * (k - 1), Z = (k - 1) * (l - 1), W = k * l. Notice that X, Y, Z, W are small enough, so we can construct a lattice where the first column is [n, -e^2, -e], then apply LLL to get k and l, which leads to factor n.

Approach 2: Notice dp and dq are small enough, we may apply Wiener’s attack, to get X = dp * dq (for data in this task, X = dp * dq // 3) from the continued fraction of e * e / N. Then we may guess dpfrom the factors of X, and recover p via GCD(pow(pow(2, e, n), dp, n) - 2, n) .

Approach 3: Both the above methods are unintended, intended solution involves a Partial Key Exposure attack on CRT-RSA [1] or a small CRT-Exponent attack (slower) [2].

Reference

[1] May, Alexander, Julian Nowakowski, and Santanu Sarkar. “Partial Key Exposure Attack on Short Secret Exponent CRT-RSA.

[2] Takayasu, Atsushi, Yao Lu, and Liqiang Peng. “Small CRT-exponent RSA revisited.” Journal of Cryptology 32.4 (2019): 1337-1382.

halfhalf

Category: Reverse

Difficulty: ★★☆

Solved: 7 / 12

Tag: Rust, Jacobi Symbol

Details

Source

We are given a Rust ELF file. It requires you solve a PoW, then input a magic word, next the server will generate a RSA key and a secret number. You can interact with server, there are five options: Get the RSA modulus; Guess the secret; Reset secret; Get flag; Exit. Each time you input a guess, the server may encrypt9x^2 or 18x^2 for some random x, which depends whether your guess is greater than the secret. And if your guess is same as the secret you may get the flag. Note that all the number should be encoded with emoji.

Solution

The PoW requires us to find a 4-byte phrase whose sha256 digest match the given value for the last 3 bytes. And it is easy to find the magic word, which are a series of emoji. To distinguish 9x^2 and 18x^2, we can compute its Jacobi symbol, so a binary search can determine the secret and get the flag.

Issues

I deployed this challenge with xinetd, due to a mistake in the wrapper, the program is executed under root directory, so it can’t read the flag from file. Thanks @FORMALIN for pointing out this.

@RBTree tells me the 60s time limitation is too tight, and he asks to increase it. But the source code of this challenge is lost, due to a VM broken, so the only way is to patch the binary. And he quickly finds the location of the corresponding parameters, then I patch it from 60s to 200s. Thanks RBTree’s help.

0CTF/TCTF 2021 Quals

zer0lfsr-

Category: Crypto

Difficulty: ★★

Solved: 35 / 198

Tag: LFSR, NFSR, Z3

Details

Source

There are three generators composed of LFSR or NFSR.

Generator1 contains a 48-bit NFSR and a 16-bit LFSR

Generator2 contains a 16-bit NFSR and a 48-bit LFSR

Generator3 contains a 64-bit LFSR

The output functions of each generator are filted, which are not linear from its internal state. We are asked to recover the initial state of any two generators within 50 seconds after obtained its consecutive 5000-byte output and the hash digest of its initial state.

Solution

Most teams choose to attack Generator1 and Generator3.

Approach 1: Use z3

Approach 2: See rkm’s writeup for details

zer0lfsr+

Category: Crypto

Difficulty: ★★★★

Solved: 2 / 198

Tag: LFSR, NFSR, FCA

Details

Source

The three generators remain unchanged. But we are given 20000 bytes from the majority function of the output of three generators, and are required to recover all the initial states within 100s. The initial state of Generator2 is derived from Generator1 with KDF function, the initial state of Generator3 is derived from Generator2 with KDF function.

Solution

Please check rkm’s writeup for details.

zer0lfsr++

Category: Crypto

Difficulty: ★★★★★

Solved: 1 / 198

Tag: LFSR, NFSR, FCA

Details

Source

Same as zer0lfsr+, but there are no KDF, three initial states are independent. And we have a hint, can get the highest 16 bits of one of the three state.

Solution

FCA attack recover full state of Generator3.

FCA attack recover the LFSR state of Generator2 and use the hint to get the NFSR state of Generator2.

Similar attack in [1] to recover full state of Generator1.

Reference

[1] Berbain, Côme, Henri Gilbert, and Alexander Maximov. “Cryptanalysis of grain.” International Workshop on Fast Software Encryption. Springer, Berlin, Heidelberg, 2006.

原文始发于GitHub：0CTF 2022 官方密码的简易wp