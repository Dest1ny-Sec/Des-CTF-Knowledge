# 解析一道清朝老题-McEliece

> 原文: https://www.ctfiot.com/282175.html
> ID: 282175

McEliece密码系统攻击：从GRS码到Sidelnikov-Shestakov攻击的完整解析

一、题目背景

本题是一道经典的后量子密码学CTF挑战,涉及McEliece公钥密码系统的安全性分析。题目提供了两个文件:

publickey.sobj: 公钥矩阵(64×128,定义在GF(2^8)上)

ciphertext.sobj: 密文向量(128维,GF(2^8))

选择一个[n, k, d]线性纠错码C,具有高效的解码算法D

选择k×k的可逆矩阵S和n×n的置换矩阵P

计算G’ = S·G·P,其中G是码C的生成矩阵

公钥:G’ (k×n矩阵)

私钥:(S, G, P, D)

明文m是k维向量

随机选择权重为t的错误向量e(n维)

密文 c = m·G’ + e

计算 c’ = c·P^(-1) = m·S·G + e·P^(-1)

使用解码算法D解码c’,得到m·S

计算 m = (m·S)·S^(-1)

码结构隐藏:
经过S和P变换后的G’应当看起来像随机矩阵

译码困难性:
在不知道码结构的情况下,从c恢复m是计算困难的

支撑向量 α = (α₀, α₁, …, α_{n-1}),所有αᵢ互不相同

列乘子向量 v = (v₀, v₁, …, v_{n-1}),所有vᵢ≠0

参数 k < n

范德蒙德结构:
生成矩阵的每一列都是范德蒙向量

列之间的多项式关系:
由于是在有限域上的幂次,列之间存在可识别的代数关系

对偶码也是GRS:
GRS码的对偶码仍然是GRS码

设 a[0] = 0, a[1] = 1 (无损一般性)

构造GRS码对象:

使用Berlekamp-Welch解码器:

解码密文:

总共只需要枚举255个ratio值

对于正确的ratio,所有验证步骤都会成功

攻击在第一个ratio时就成功了,说明α[0]=0的选择是标准的

q = |F| = 256 (有限域大小)

n = 128 (码长度)

需要枚举255个ratio

每个ratio需要进行n次查找和验证

总体可以在秒级完成

二元Goppa码:
目前最安全的选择,是NIST后量子密码标准的候选

参数要求:

码长 n ≥ 2000

错误能力 t ≥ 50

定义在GF(2^m),m ≥ 11

抗量子:
没有已知的量子算法能有效攻击

简单高效:
加密和解密都是线性运算

长期安全:
40多年的密码分析没有发现本质性弱点

McEliece密码系统的工作原理

GRS码的代数结构及其安全弱点

Sidelnikov-Shestakov攻击的实现细节

密码系统实现中参数选择的重要性

McEliece本身是安全的后量子密码系统

使用GRS/Reed-Solomon码实现会导致多项式时间攻击

正确的实现应使用二元Goppa码

在后量子时代,基于编码理论的密码学仍然是重要的研究方向

Sidelnikov, V.M., Shestakov, S.O. (1992). “On insecurity of cryptosystems based on generalized Reed-Solomon codes”

IACR ePrint 2009/452: “Algebraic Cryptanalysis of McEliece Variants with Compact Keys”

NIST Post-Quantum Cryptography Standardization Project

Hack.lu CTF 2017 – McEliece Challenge Writeups


```
G[i,j] = vⱼ · αⱼⁱ (i=0,1,...,k-1; j=0,1,...,n-1)
gpe = gp.echelon_form()
for ratio in F.list()[1:]: # 255个候选值
tar = (gpe[0][i] / gpe[1][i]) / ratio
(x - a[1]) / (x - a[0]) == tar
v0 = gpe[0][k]/gpe[i][k] * (a[k] - a[0])v1 = gpe[0][k+1]/gpe[i][k+1] * (a[k+1] - a[0])
r2 * (a[k] - x) == v0r2 * (a[k+1] - x) == v1
mp = gp.matrix_from_rows_and_columns(range(k), range(k+1))cp = mp.right_kernel().basis()[-1]
C = codes.GeneralizedReedSolomonCode(a, k, cols)
D = codes.decoders.GRSBerlekampWelchDecoder(C)
tmp = D.decode_to_message(cmsg)msg = vector(tmp) * h.inverse()
# Sage提供了丰富的编码理论库sage --version
F = GF(2^8)n, k = 128, 64cmsg = load("ciphertext.sobj")gp = load("publickey.sobj")
(102, 108, 97, 103, 123, 82, 101, 101, 100, 83, 111, 108, ...)
flag{ReedSolomonCodesAreNoGoodIdeaForMcElieceIfYouWantTopCrypto}
    #https://eprint.iacr.org/2009/452.pdf
# Sidelnikov-Shestakov attackF=GF(2^8)n, k = 128, 64cmsg = load("ciphertext.sobj")gp = load("publickey.sobj")gpe = gp.echelon_form()for ratio in F.list()[1:]: a = [0]*n a[1] = 1 succ = True # 恢复支撑向量 for i in range(k, n): tar = gpe[0][i]/gpe[1][i] / ratio res = 0 for x in F.list(): if x!=0 and (x-a[1])/(x-a[0])==tar: if res!=0: succ = False break res = x if res==0: succ = False if not succ: break a[i] = res if not succ: continue # 恢复剩余元素 for i in range(2, k): v0 = gpe[0][k]/gpe[i][k]*(a[k]-a[0]) v1 = gpe[0][k+1]/gpe[i][k+1]*(a[k+1]-a[0]) res = 0 for r2 in F.list()[1:]: for x in F.list()[1:]: if r2*(a[k]-x)==v0 and r2*(a[k+1]-x)==v1: res = x break if res!=0: break if res==0: succ = False if not succ: break a[i] = res if not succ: continue try: # 重构GRS码 mp = gp.matrix_from_rows_and_columns(range(k), range(k+1)) cp = mp.right_kernel().basis()[-1] Ct = codes.GeneralizedReedSolomonCode(a[:k+1], k, cp) Et = codes.encoders.GRSEvaluationVectorEncoder(Ct) gm = Et.generator_matrix() co = gm.right_kernel().basis()[-1] Ct = codes.GeneralizedReedSolomonCode(a[:k+1], k, co) Et = codes.encoders.GRSEvaluationVectorEncoder(Ct) gtmp1 = Et.generator_matrix() gtmp2 = gtmp1.matrix_from_rows_and_columns(range(k), range(k)) mtmp2 = gp.matrix_from_rows_and_columns(range(k), range(k)) h = mtmp2*gtmp2.inverse() g = h.inverse()*gp cols = g[0] # 解码 C = codes.GeneralizedReedSolomonCode(a, k, cols) E = codes.encoders.GRSEvaluationVectorEncoder(C) D = codes.decoders.GRSBerlekampWelchDecoder(C) g = E.generator_matrix() tmp = D.decode_to_message(cmsg) msg = vector(tmp)*h.inverse() # 输出flag msg_bytes = [int(str(x)) for x in msg] print(bytes(msg_bytes)) break 
except: continue
```
