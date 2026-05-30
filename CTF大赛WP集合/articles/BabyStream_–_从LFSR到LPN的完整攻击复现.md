# BabyStream – 从LFSR到LPN的完整攻击复现

> 原文: https://www.ctfiot.com/281936.html
> ID: 281936

BabyStream – 从LFSR到LPN的完整攻击复现

0x00 题目概述

这是一道密码学题目,实现了一个基于LFSR的流密码算法。题目提供了加密程序和2048字节的加密输出,要求恢复128位的初始状态。

核心信息:

算法: LFSR + Feedforward函数

状态长度: 128位

输出长度: 16384位 (2048字节)

Flag:flag{ce2980ad9763b8468882f292dbe9f365}

SHA-256校验:825c3637fb99400d7d132f80e379db5982cfaf0eb73b47c1cfdfd9c03aceebac

将128位状态左移1位

根据mask选择特定位进行异或

结果作为新的最低位

这是一个线性变换,可以用转移矩阵表示

线性部分:

x[127]

Σ(x[i] ⊕ x[box[i]])for i in range(63)

覆盖了127个互不重复的比特(缺x[126])

非线性部分:

4次项:x[11] & x[22] & x[33] & x[53]

16次项:x[1] & x[9] & ... & x[59]

63次项:x[0] & x[1] & ... & x[62]

4次项x[11] & x[22] & x[33] & x[53]: 概率 = 1/16 = 0.0625

16次项: 概率 = 1/65536 ≈ 0.0000153

63次项: 概率 ≈ 1/10^19 (几乎为0)

约93.75%的输出位只受线性部分影响

约6.25%的输出位受非线性项干扰(视为”噪声”)

矩阵 A ∈ GF(2)^(m×n)

向量 y ∈ GF(2)^m

秘密向量 s ∈ GF(2)^n

s: 128位初始状态(未知)

a[t]: 第t个系数向量(已知)

y[t]: 第t个输出位(已知)

noise[t]: 非线性项产生的噪声

内存占用: 128×128/8 = 2KB (可接受)

计算开销: 矩阵乘法 O(128^2) (较慢)

代码复杂度高

列向量左移 → 行向量右移

反馈位注入 → 条件异或mask

时间复杂度: O(1)

时间复杂度: O(n) 而不是 O(n · 128^2)

空间复杂度: O(n) 存储结果

无需显式矩阵,仅需位运算

有噪声: 约6.25%的方程是错的

矛盾方程: 直接求解会失败(无解)

随机选择最小子集(128个方程)

用这个子集求解得到候选解s

用候选解预测所有输出,计算准确率

重复多次,取准确率最高的解

全部正确的概率: (1-η)^128 ≈ 0.0001

但只要大部分正确,解就接近真实值

通过准确率筛选,可以找到最优解

方法

适用场景

复杂度

本题效果

代数攻击(Gröbner基)

完全非线性系统

指数级

无法处理噪声

线性化攻击

低次非线性

多项式级

方程组无解

不检查矛盾行(0…0 = 1)

自由元默认设为0

允许子系统有少量错误

trials: 迭代次数(1200-2000)

subset: 子集大小(128-256)

seed: 随机种子(可复现)

理论上限: 93.75% (1 – 1/16)

实际达到: 93.854%

略高于理论值,因为16次和63次项的噪声极低

逐字节完全一致:100% match

SHA-256校验: 完全相同

这是最强的验证!

传统: O(n · 128^2) ≈ 268M次运算

优化: O(n) ≈ 16K次运算

加速比:16,384倍!

行异或:A[r] ^= A[row] (O(1))

检查某位:(A[r] >> col) & 1 (O(1))

设置某位:s |= (1 << col) (O(1))

trials

subset

成功率

平均时间

500

128

60%

2秒

1200

128

85%

4秒

2000

128

95%

7秒

1200

256

90%

6秒

2000

256

98%

10秒

快速测试:trials=1200, subset=128

稳定求解:trials=2000, subset=256

非线性项仍然存在

导致方程组有噪声

直接高斯消元得到”无解”

不是修改代码

而是建模时忽略非线性项

把非线性项当作噪声处理

用鲁棒算法(RANSAC)求解

量子安全: 目前没有有效的量子算法

简单高效: 只需异或和随机数

应用广泛: 认证协议、加密方案

理论基础: 学习理论、复杂性理论

η ≈ 25% ~ 30%

或者n(维度)更大(如n=512)

添加更多低次非线性项(2次、3次)

调整box映射增加非线性

使用多个非线性函数

使用256位或512位LFSR

增加状态空间

提高计算复杂度

LPN + LFSR的非线性组合

多级滤波

时变参数

LPN问题识别– 识别噪声的来源和比例

RANSAC算法– 鲁棒估计的经典方法

GF(2)线性代数– 位运算优化

LFSR数学建模– 转移矩阵的快速计算

噪声可预测: 非线性项激活概率已知

数据充足: 16384个样本 >> 128个未知数

RANSAC鲁棒: 能容忍6.25%的噪声

计算高效: 位运算优化,秒级求解

识别噪声来源– 计算非线性项的激活概率

评估噪声率– 判断是否适合RANSAC

参数调优– trials、subset大小的权衡

验证准确率– 接近理论上限说明解正确

严格校验– 100%复现是最强验证

笔记本i5: 5-7秒

服务器: 2-3秒

密码分析不仅仅是代数攻击

统计方法在处理噪声时的强大能力

LPN问题在密码学中的重要性

优雅的数学建模如何简化复杂问题

位运算优化在密码分析中的价值

严格验证在CTF中的必要性

Blum, A., Kalai, A., & Wasserman, H. (2003). Noise-tolerant learning, the parity problem, and the statistical query model

RANSAC: Random Sample Consensus Algorithm

Learning Parity with Noise (LPN) – Post-Quantum Cryptography

Toyocrypt Algorithm Specification

Python 3.8+ (仅需标准库)

运行时间: 5-10秒


```
deflfsr(R, mask): degree =128 f_skr = (1<< degree) -1 tmp = ((R <<1) & mask) lastbit =0 whiletmp !=0: lastbit ^= (tmp &1) tmp = tmp >>1 return((R <<1) ^ lastbit) & f_skr
```



```
S[t+1] = T · S[t] (mod 2)
```



```
MASK =0x16c9c9a7f51ce6637b0e3f461a8da9b75
```



```
deffeedforward(r): x = [int(i)foriinlist('{0:0b}'.format(r))][::-1] x += [0] * (128- len(x)) box = [78,65,90, ...] # 63个索引 out = x[127] foriinrange(0,63): out ^= (x[i] ^ x[box[i]]) &1 out ^= x[11] & x[22] & x[33] & x[53] &1 # 4次项 out ^= x[1] & x[9] & ... & x[59] &1 # 16次项 tmp =1 foriinrange(0,63): tmp &= x[i] out ^= tmp &1 # 63次项 returnout
```



```
y[i] = <A[i], s> ⊕ noise[i]
```



```
y[t] = <a[t], s> ⊕ noise[t]
```



```
State[t] = T^t · s
```



```
linear_output[t] = c · State[t+1] = c · T^(t+1) · s = <(T^T)^(t+1) · c, s>
```



```
a[t] = (T^T)^(t+1) · c
```



```
c =1<<127# x[127]foriinrange(63): c ^= (1<< i) # x[i] c ^= (1<< box[i]) # x[box[i]]
```



```
FULL = (1<<128) -1MASK_SHIFTED = MASK >>1defapply_Tt(v, mask_shifted): """对行向量v施加一次T^T""" u = (v >>1) & FULL ifv &1: u ^= mask_shifted returnu
```



```
defbuild_c(box): """构造线性部分系数""" c =1<<127 foriinrange(63): c ^= (1<< i) c ^= (1<< box[i]) returncdefgen_rows(n, c_vec, mask_shifted): """生成系数向量序列""" rows = [] v = apply_Tt(c_vec, mask_shifted) # a[0] = T^T · c for_inrange(n): rows.append(v) v = apply_Tt(v, mask_shifted) # a[t+1] = T^T · a[t] returnrows
```



```
defparity(x: int)-> int: """计算奇偶性""" returnx.bit_count() &1defgf2_gauss_solve(A_rows, b_bits, n=128): """GF(2)上的高斯消元(放宽一致性检查)""" A = A_rows[:] b = b_bits[:] m = len(A) row =0 piv = [-1] * n # 前向消元 forcolinrange(n): # 找主元 pivot =None forrinrange(row, m): if(A[r] >> col) &1: pivot = r break ifpivotisNone: continue # 交换行 A[row], A[pivot] = A[pivot], A[row] b[row], b[pivot] = b[pivot], b[row] piv[col] = row # 消元 forrinrange(m): ifr != rowand((A[r] >> col) &1): A[r] ^= A[row] b[r] ^= b[row] row +=1 ifrow == m: break # 回代(自由元设为0) s =0 forcolinrange(n -1,-1,-1): r = piv[col] ifr ==-1: continue above = (A[r] >> (col +1)) & ((1<< (n - col -1)) -1) val = b[r] ^ parity(above & (s >> (col +1))) ifval: s |= (1<< col) return(True, s)
```



```
defpredict(rows, s): """预测输出""" return[parity(r & s)forrinrows]defransac_solve(rows, y_bits, trials=2000, subset=128, seed=2): """RANSAC求解LPN问题""" rnd = random.Random(seed) N = len(rows) best_s, best_acc =0,-1.0 idx_all = list(range(N)) for_inrange(trials): # 1. 随机抽取subset个方程 idx = rnd.sample(idx_all, subset) A = [rows[i]foriinidx] b = [y_bits[i]foriinidx] # 2. GF(2)高斯消元求解 ok, s = gf2_gauss_solve(A, b) ifnotok: continue # 3. 用全体样本验证 yp = predict(rows, s) hits = sum(1- (a ^ b)fora, binzip(yp, y_bits)) acc = hits / N # 4. 更新最优解 ifacc > best_acc: best_acc, best_s = acc, s ifacc >0.92: # 93.75%理论上限 break returnbest_s, best_acc
```



```
[1] 读取output文件 → 16384个输出比特[2] 从babystream.py解析mask和box[3] 计算线性部分系数向量c[4] 生成系数矩阵: a[t] = (T^T)^(t+1) · c[5] RANSAC求解: - 2000次迭代 - 每次随机选128个方程 - 高斯消元求解 - 全局验证打分[6] 获得准确率93.854%的解[7] 输出flag{ce2980ad9763b8468882f292dbe9f365}
```



```
defbits_be(bs): """字节序列 → 比特(高位在前)""" out = [] forbinbs: forjinrange(7,-1,-1): out.append((b >> j) &1) returnout
```



```
$ python3 solve.py[+] Loaded output: 2048 bytes (16384 bits)[+] Parsed mask: 0x16c9c9a7f51ce6637b0e3f461a8da9b75[+] Parsed box[63] from babystream.py[+] RANSAC accuracy: 93.854%flag{ce2980ad9763b8468882f292dbe9f365}
```



```
deflfsr_step(R): """LFSR单步演化""" degree =128 f_skr = (1<< degree) -1 tmp = ((R <<1) & MASK) lastbit = parity(tmp) return((R <<1) ^ lastbit) & f_skrdeffeedforward_bit(r): """完整的feedforward函数(含非线性项)""" x = [(r >> i) &1foriinrange(128)] # 线性部分 out = x[127] foriinrange(63): out ^= (x[i] ^ x[BOX[i]]) &1 # 非线性部分 out ^= x[11] & x[22] & x[33] & x[53] &1 out ^= x[1] & x[9] & x[12] & x[18] & x[20] & x[23] & x[25] & x[26] & x[28] & x[33] & x[38] & x[41] & x[42] & x[51] & x[53] & x[59] &1 tmp =1 foriinrange(63): tmp &= x[i] out ^= tmp &1 returnout &1defregenerate(r0, nbytes): """重新生成密钥流""" r = r0 out = bytearray() for_inrange(nbytes): byte_val =0 for_inrange(8): r = lfsr_step(r) bit = feedforward_bit(r) byte_val = (byte_val <<1) ^ bit out.append(byte_val) returnbytes(out)# 验证r =0xce2980ad9763b8468882f292dbe9f365regenerated = regenerate(r,2048)withopen("output","rb")asf: original = f.read()print(f"验证:{regenerated == original}") # Trueprint(f"匹配率:{sum(a==bfora,binzip(regenerated, original))}/2048") # 2048/2048
```



```
# 显式构造128×128矩阵T = np.zeros((128,128), dtype=int)# ... 填充矩阵 ...# 矩阵乘法: O(128^2)
```



```
# 位运算 O(1) 计算defapply_Tt(v): u = (v >>1) & FULL ifv &1: u ^= MASK_SHIFTED returnu
```



```
#!/usr/bin/env python3# -*- coding: utf-8 -*-"""BabyStream LPN/RANSAC 完整求解器"""importrandomDEG =128FULL = (1<< DEG) -1MASK =0x16c9c9a7f51ce6637b0e3f461a8da9b75MASK_SHIFTED = MASK >>1BOX = [78,65,90,99,117,113,87,119,64,69,114,86,72,123,91,103, 124,93,79,82,76,84,106,73,110,92,118,63,109,101,67,122, 98,111,80,105,108,107,100,81,125,71,96,83,75,68,95,74, 104,112,121,115,77,89,85,97,70,120,88,66,94,102,116]defparity(x: int)-> int: """计算奇偶性""" returnx.bit_count() &1defbits_be(bs): """字节序列 → 比特(高位在前)""" out = [] forbinbs: forjinrange(7,-1,-1): out.append((b >> j) &1) returnoutdefapply_Tt(v): """施加转移矩阵T^T""" u = (v >>1) & FULL ifv &1: u ^= MASK_SHIFTED returnudefbuild_c(): """构造线性部分系数""" c =1<<127 foriinrange(63): c ^= (1<< i) c ^= (1<< BOX[i]) returncdefgen_rows(n): """生成系数向量序列""" rows = [] v = apply_Tt(build_c()) for_inrange(n): rows.append(v) v = apply_Tt(v) returnrowsdefgf2_gauss_solve(A_rows, b_bits, n=128): """GF(2)高斯消元""" A = A_rows[:] b = b_bits[:] m = len(A) row =0 piv = [-1] * n forcolinrange(n): pivot =None forrinrange(row, m): if(A[r] >> col) &1: pivot = r break ifpivotisNone: continue A[row], A[pivot] = A[pivot], A[row] b[row], b[pivot] = b[pivot], b[row] piv[col] = row forrinrange(m): ifr != rowand((A[r] >> col) &1): A[r] ^= A[row] b[r] ^= b[row] row +=1 ifrow == m: break s =0 forcolinrange(n -1,-1,-1): r = piv[col] ifr ==-1: continue above = (A[r] >> (col +1)) & ((1<< (n - col -1)) -1) val = b[r] ^ parity(above & (s >> (col +1))) ifval: s |= (1<< col) return(True, s)defpredict(rows, s): """预测输出""" return[parity(r & s)forrinrows]defransac_solve(rows, y_bits, trials=2000, subset=128, seed=2): """RANSAC求解""" rnd = random.Random(seed) N = len(rows) best_s, best_acc =0,-1.0 idx_all = list(range(N)) for_inrange(trials): idx = rnd.sample(idx_all, subset) A = [rows[i]foriinidx] b = [y_bits[i]foriinidx] ok, s = gf2_gauss_solve(A, b) ifnotok: continue yp = predict(rows, s) hits = sum(1- (a ^ b)fora, binzip(yp, y_bits)) acc = hits / N ifacc > best_acc: best_acc, best_s = acc, s ifacc >0.92: break returnbest_s, best_acc# 验证函数deflfsr_step(R): tmp = ((R <<1) & MASK) lastbit = parity(tmp) return((R <<1) ^ lastbit) & FULLdeffeedforward_bit(r): x = [(r >> i) &1foriinrange(128)] out = x[127] foriinrange(63): out ^= (x[i] ^ x[BOX[i]]) &1 out ^= x[11] & x[22] & x[33] & x[53] idx2 = [1,9,12,18,20,23,25,26,28,33,38,41,42,51,53,59] t =1 forkinidx2: t &= x[k] out ^= t t =1 foriinrange(63): t &= x[i] out ^= t &1 returnout &1defregenerate(r0, nbytes): r = r0 out = bytearray() for_inrange(nbytes): byte_val =0 for_inrange(8): r = lfsr_step(r) bit = feedforward_bit(r) byte_val = (byte_val <<1) ^ bit out.append(byte_val) returnbytes(out)defmain(): print("="*60) print("BabyStream - LPN/RANSAC 求解器") print("="*60) # 读取output withopen("output","rb")asf: raw = f.read() y_bits = bits_be(raw) print(f"[+] 加载输出:{len(raw)}字节 ({len(y_bits)}比特)") # 生成系数矩阵 rows = gen_rows(len(y_bits)) print(f"[+] 生成系数矩阵:{len(rows)}行") # RANSAC求解 print("[*] 开始RANSAC求解...") best_s, best_acc = ransac_solve(rows, y_bits, trials=2000, subset=128) print(f"[+] RANSAC准确率:{best_acc:.3%}") # 输出flag flag =f"flag{{{best_s:032x}}}" print(f"[+] Flag:{flag}") # 严格验证 print("[*] 验证中...") regenerated = regenerate(best_s, len(raw)) match = (regenerated == raw) print(f"[+] 完整复现匹配:{match}") ifmatch: print("="*60) print("验证通过! 成功恢复初始状态!") print("="*60) else: print("警告: 验证未通过,请检查参数")if__name__ =="__main__": main()
```



```
变量数量: C(128,1) + C(128,2) + C(128,3) ≈ 350,000结果: 变量爆炸,无法求解
```



```
假设: 所有AND替换为XOR结果: 方程组无解(与真实output不匹配)
```



```
变量数量: 128噪声率: 6.25%结果: RANSAC成功求解
```



```
行向量生成: O(N) N = 16384单次消元: O(subset^3) subset = 128RANSAC: O(trials × subset^3)总计: O(trials × 128^3) ≈ 4M次运算
```
