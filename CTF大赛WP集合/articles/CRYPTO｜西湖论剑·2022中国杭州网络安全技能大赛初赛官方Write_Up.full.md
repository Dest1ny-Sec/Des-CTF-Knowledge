---
title: CRYPTO｜西湖论剑 2022 中国杭州网络安全技能大赛初赛官方 Write Up
contest: 西湖论剑
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags:
- MyCurveErrorLearn ECHNP
- MyErrorLearn MIHNP
- MyErrorLearnTwice LLL对角阵
- LockByLock Pollard kangaroo
- MyOracle MT19937 LSB
- 椭圆曲线HNP
- 模逆HNP
- Coppersmith
- Pollard kangaroo e范围爆破
- MT19937 state恢复
attack_chain:
- 'MyCurveErrorLearn: ECHNP(DH) 椭圆曲线 Hidden Number Problem, 输入 0 得 t=0, t 与 oracle 输出多项式关系'
- 'LockByLock: secureProcedure 嵌套加密, A 加密 c1, B 加密 c1 得 c2, A 解 c2 得 c3'
- 两次输入得中间值, Pollard's kangaroo 在 e 范围内求解
- 'MyErrorLearn: MIHNP 模逆 HNP, 二元 Coppersmith 解多项式'
- 'MyErrorLearnTwice: d 组输出, LLL 求对角阵 + 最短格向量恢复 e'
- 'MyOracle: 模是偶数时泄露 r LSB, 构造矩阵恢复 MT19937 全部 state'
key_payload: '''ECHNP(DH) / LockByLock kangaroo / MIHNP Coppersmith / MIHNP LLL 对角阵 / MT19937 LSB state 恢复'''
one_liner: 西湖论剑 2022 CRYPTO 官方 WP — MyCurveErrorLearn ECHNP 椭圆 HNP + LockByLock Pollard kangaroo + MyErrorLearn MIHNP Coppersmith + MyErrorLearnTwice LLL 对角阵 + MyOracle MT19937 LSB state 恢复。
lesson: HNP (Hidden Number Problem) 是密码学隐藏数问题模板;ECHNP/MIHNP/LWE 都基于 LLL;Pollard kangaroo 适合已知 e 范围;MT19937 LSB oracle 是 RNG 恢复经典。
quality: high
full_path: CRYPTO｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write_Up.full.md
meta_path: CRYPTO｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write_Up.meta.md
images_removed: true
images_removed_count: 6
schema_version: v3.0.0-P0
summary: CRYPTO｜西湖论剑 2022 中国杭州网络安全技能大赛初赛官方 Write Up。西湖论剑 2022 CRYPTO 官方 WP — MyCurveErrorLearn ECHNP 椭圆 HNP + LockByLock Pollard kangaroo + MyErrorLearn MIHNP Coppersmith + MyErrorLearnTwice LLL 对角阵 + MyOra...
category: crypto
subcategory: rsa
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 6
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/97733.html
reasoning_chain:
- MyCurveErrorLearn 触发点：oracle 输入 0 给出 t*P 等于 0 → 假设：HNP 椭圆曲线版（ECHNP）
- 动作：读 Oracle(0)/Oracle(t) 求差 → 观察：得到 P + [t]R 的多项式关系 → 下一步：构造线性方程组解 P
- 动作：把 ECHNP 化为系数矩阵 + LLL 求短向量 → 观察：恢复点 P 完成
- LockByLock 触发点：A 加密 c1 + B 加密 c1 得 c2 + A 解 c2 得 c3 三层嵌套 → 假设：经典 common modulus attack
- 动作：两次输入得中间值 + 已知 e 范围 → 下一步：用 Pollard's kangaroo 在 e 区间搜索
- 假设：kangaroo 对 ECDLP 有效但这里是 e 整数 → 动作：pollard_kangaroo(e) 在 [low,high] → 观察：恢复 e 完成
- MyErrorLearn 触发点：mod p + 模逆 oracle + d 对 (r, x) → 假设：MIHNP = Mod Inverse Hidden Number Problem
- 动作：HNP 第 7 章构造 → 观察：得到 (a_i*x + b_i) mod p = c_i 的 d 个方程
- 假设：d 个方程中 x 是变量 → 动作：用二元 Coppersmith 解多项式方程 → 观察：得 e 还原 s
- MyErrorLearnTwice 触发点：d 组输出 → 动作：构造矩阵 + LLL 求对角阵 → 下一步：最短格向量等于 e 未知数
- MyOracle 触发点：mod 是偶数时泄露 r LSB → 假设：MT19937 PRNG state 恢复经典套路
- 动作：构造 GF(2) 矩阵收集 624 个 LSB → 观察：解 19937 维 state → 解密得 flag
failed_attempts:
- MyCurveErrorLearn 用 sage 内置 ec_dlog → 失败：P 是未知点没法独立解 DLP
- LockByLock 用常规 common modulus 直接 gcd → 失败：3 层套娃 e 范围未对齐
- MyErrorLearn 直接 z3 binary coppersmith → 失败：d 个独立同余方程约束不够
- MyOracle 试图从 LSB 直接解出 MT state → 失败：必须凑够 624 个 LSB 方程才能 BF 矩阵逆
key_observations:
- HNP (Hidden Number Problem) 是密码学隐藏数问题标准模板，ECHNP/MIHNP/LWE 三大变体都基于 LLL
- Pollard's kangaroo 在 e 区间已知时比 Pollard rho 更快，因为有界搜索
- MIHNP 二元 Coppersmith 解多项式方程是 Boneh-Durfee 的扩展
- MT19937 LSB oracle 是 RNG state 恢复的经典层（看 cryptography-wiki）
- LLL 算法 + Hermite normal form 对角化是 Hidden Number Problem 的核心
prerequisites:
- SageMath LLL 算法使用
- 椭圆曲线 Hidden Number Problem 基础（Boneh 论文）
- Pollard's kangaroo 实现
- Coppersmith 小根求解（sage small_roots）
- MT19937 PRNG 状态恢复（624 个 32-bit 观察）
---
# CRYPTO｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

> 原文: https://www.ctfiot.com/97733.html
> ID: 97733

2023年2月2日，第六届西湖论剑网络安全技能大赛初赛落下帷幕！来自全国306所高校、485支战队、2733人集结线上初赛！

以下为本届西湖论剑大赛初赛CRYPTO题目的Write Up

CRYPTO

2022西湖论剑大赛官方WP

（一）

MyCurveErrorLearn

题目定义的问题可以被描述为ECHNP(DH)

ECHNP(DH)：指定素数p、正整数m，以及

上的椭圆曲线
。点$Q in E, Rin 。定义E上的函数f，未知数Pin E，存在预言机mathcal{O}_{P,R}(t)=f(P+[t]R)。通过预言机mathcal{O}_{P,R}恢复P$。

参考文献HNP第7.1节 Elliptic Curve Hidden Number Problem中的构造，考虑输入0，则可以得到

，此时分别输入

，则可以得到多项式

（二）

LockByLock

由附件可知在secureProcedure中得到了A加密flag的密文c1，B加密c1的密文c2，A解密c2的密文c3.

我们可以做两次输入让A，B来重复上述步骤并且得到中间值。

有

显然可以构造

然后已知e的范围，所以我们使用Pollard’s kangaroo求即可。求完之后带入secureProcedure中得到的结果取一次共模即可。

（三）

MyErrorLearn

题目定义的问题可以被描述为MIHNP

MIHNP：指定素数p以及正整数k，d，未知数

，令

为独立随机乘数。从d对

中恢复
。

其中

参考文献HNP第7章The Modular Inversion Hidden Number Problem中的构造，有

有

。

使用二元coppersmith求解此多项式方程，即可得到e。从而恢复s。

（四）

MyErrorLearnTwice

题目定义的问题可以被描述为MIHNP

MIHNP：指定素数p以及正整数k，d，未知数

，令

为独立随机乘数。从d对

中恢复
。

其中

参考文献HNP第7章The Modular Inversion Hidden Number Problem中的构造，有

有

。设

，所以我们可以利用d组输出得到
项方程

则
为
的
维对角线方阵。
为

维矩阵，由上述多项式方程构造得到每一列。

考虑向量

为最短格向量。使用LLL算法即可求解e，从而得到s。

（五）

MyOracle

题目的关键点是找到Oracle泄露的有用信息，构造模型，很显然，mod是随机的，则当mod为偶数时，会泄露r的LSB，由此我们可以构造矩阵来恢复MT的全部state，从而预测随机数。

具体矩阵构造方式参考cryptography-wiki MT19937.

— 往期回顾 —

MISC｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

WEB｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]