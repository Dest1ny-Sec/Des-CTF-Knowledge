---
title: GDG Algiers CTF两道矩阵题wp
contest: GDG Algiers CTF
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [matrix, diagonalization, sagemath, discrete-log, poly, rsa, aes-cbc, lwe]
attack_chain:
  - 第1题 the_matrix: 12x12矩阵GF(p)对角化
  - D.diagonalization() + A.inverse() * P * A
  - 取对角元素 vD=[37,31,29,...,3,2] vP=[大数...]
  - discrete_log(vP[11], vD[11]) = K
  - SHA256(K)[:256] 作AES key解iv+ciphertext
  - flag: CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}
  - 第2题 franklin-last-words: 多项式3*num^3, 3*num^6
  - v2polyv/v2poly2v映射
  - poly_C*V1[0][0] + poly_y*V1[0][1]
  - 爆破字符32-126
  - flag: CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}
key_payload: K = discrete_log(G(vP[11]), G(vD[11]))
one_liner: GDG Algiers CTF 2题：矩阵对角化DLP+多项式LWE
lesson: 矩阵对角化可破解特征值加密；多项式+线性方程组可恢复字符
quality: high
---

# GDG Algiers CTF两道矩阵题wp

## 题目信息
- 比赛：GDG Algiers CTF
- 作者：狗敦子（看雪论坛）
- 类别：Crypto（2 题矩阵）

## 关键攻击链
### 题 1：the_matrix
```python
from sage.all import *
p = 12143520799543738643
D = read_matrix('matrix.txt')  # 12x12
P = read_matrix('public_key.txt')
digD, A = D.diagonalization()
digP = A.inverse() * P * A
vD = [digD[i][i] for i in range(12)]
vP = [digP[i][i] for i in range(12)]
# vD = [37, 31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 2]
# vP = [6751925379844785295, 11256715989719283883, ...]
G = GF(p)
K = discrete_log(G(vP[11]), G(vD[11]))
# K = 7619698002081645976
key = SHA256.new(data=str(K).encode()).digest()[:2**8]
cipher = AES.new(key, AES.MODE_CBC, iv)
flag = cipher.decrypt(ciphertext).decode()[:46]
# flag: CyberErudites{Di4g0n4l1zabl3_M4tric3s_d4_b3st}
```

### 题 2：franklin-last-words
```python
from sage.all import Matrix, IntegerModRing
from message import N, e, ct
def poly(num):
    return [(3*pow(num, 3, N)) % N, (3*pow(num, 6, N)) % N]
def v2polyv(v, num):
    return (v - R_3 - pow(num, 9, N)) % N
def polyv2v(v, num):
    return (v + R_3 + pow(num, 9, N)) % N
def gen(num):
    V2 = Matrix(IntegerModRing(N), [poly(num)])
    V1 = V2 * T_
    v = (poly_C*V1[0][0] + poly_y*V1[0][1]) % N
    table[polyv2v(v, num)] = chr(num)
table = {}
R_3 = ct[0]
prefix = b"CyberErudites{}"
T = Matrix(IntegerModRing(N), [poly(int(prefix[0])), poly(int(prefix[1]))])
T_ = T.inverse()
poly_C = v2polyv(ct[1], ord('C'))
poly_y = v2polyv(ct[2], ord('y'))
for num in range(32, 126):
    gen(num)
# flag: CyberErudites{Fr4nkl1n_W3_n33d_an0th3R_S3450N_A54P}
```

## 评分
- quality: high（sagemath 矩阵对角化 + DLP + 多项式 LWE 双题）
