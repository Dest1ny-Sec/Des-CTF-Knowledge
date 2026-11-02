---
title: '2026山东省赛总决赛 Crypto3-投影协议权重攻击'
contest: '2026山东省赛总决赛'
contest_normalized: '2026山东省赛总决赛'
contest_year: 2026
year: 2026
category: crypto
subcategory: 'linear_algebra'
subcategory_guess: 'linear_system'
tags:
- 'linear-algebra'
- 'modular'
- 'oracle'
- 'normalization-bypass'
- 'query-budget'
attack_chain:
- '读 projection.py 发现 w 需满足 sum(w) ≡ 1 (mod p) 且 0<w<p'
- '构造 baseline 向量 (1,...,1, 1-(n-1)) 满足归一化约束'
- '再构造 n-1 个差分向量 (第i项+1, 末项-1)，仍满足约束'
- '收集 n 次响应组成线性方程组，在 mod p 下高斯消元'
- '38 次查询 < 40 预算，解出全部 secret'
one_liner: 'sum(w)≡1 归一化约束可被"差分向量"绕过，用 n 次查询解线性方程组恢复 secret'
lesson: '归一化类约束（sum≡1）并不构成防线：因约束是线性的，差分向量族自动满足，本质是自由度 n-1 的仿射空间。任何"只校验线性约束"的 oracle 都能被 n 次查询完全解出。'
quality: high
last_verified: '2026-11-02'
failed_attempts:
- '试图用单位向量 e_i 逐项取值 → 失败：sum(e_i)=1 但其他项为 0，不满足 0<w<p'
- '试图用差分向量直接求绝对量 → 失败：差分只给 x_i - x_last，还需一次基线查询'
- '直接用未取模的 S1 做消元 → 失败：oracle 返回的是 mod p 后的值'
key_observations:
- 'w 的约束是线性同余，差分向量 (w+e_i-e_last) 仍满足 sum≡1'
- 'n 维秘密 + 1 个线性约束 = 自由度 n-1，n 次查询刚好够'
- '预算 40 > 维度 38，留了 2 次余量用于校验'
---

# 2026山东省赛总决赛 Crypto3-投影协议权重攻击

## 题目

```
projection / tcp

每行一个 JSON。连接后返回 n、p、budget。

请求：{"weights": [整数, ...]}
响应：{"value": 整数}

向量长度 n；各项在 1..p-1；权重之和模 p 等于 1。
每连接最多 budget 次请求。
```

`projection.py`：

```python
P = 65537
N = 38
BUDGET = 40

def project(secret, weights, mask):
    if len(weights) != N: raise ValueError('dimension')
    if any(type(w) is not int or not 0 < w < P for w in weights): raise ValueError('range')
    if sum(weights) % P != 1: raise ValueError('normalization')
    return (sum(w*x for w,x in zip(weights,secret)) + mask) % P
```

## 关键观察

`n=38`，预算是 40 —— **只比维度多 2 次**。这意味着必须做到「维度 + 常数次」而不是「2×维度」。

朴素思路 `w = e_i`（单位向量）会被两个条件卡死：

1. `sum(e_i) = 1` 其实满足归一化，但其他项是 `0`，违反 `0 < w < p`
2. 所以只能凑 `w = e_i + (1 - e_i) 的补偿项`，每次查询只多拿一个坐标

真正的突破口：**归一化约束是线性的，差分向量天然满足它**。

设基线向量

```
b = (1, 1, ..., 1, a),  a = 1 - (n-1) mod p
```

`sum(b) = (n-1) + a = 1 mod p` ✓，且所有分量 `1 ≤ x < p` ✓（`a = 65501`）。

再构造差分向量 `b_i = b + e_i - e_last`，即第 i 项 +1、最后一项 -1：

```
sum(b_i) = sum(b) + 1 - 1 = 1 mod p  ✓ 仍然合法
```

于是

```
S_i - S_0 = x_i - x_last
```

这正是我们想要的**线性方程**，而且构造出的 n 个向量是线性无关的。

## 攻击

取 n 个向量：

```
v_0 = b                      (基线)
v_i = b + e_i - e_last   (i = 1..n-2)
```

（共 n 个，构成满秩矩阵，因为 `v_i - v_0 = e_i - e_last` 张成 `x_i - x_last` 的空间，加上 `v_0` 本身提供绝对尺度）

对每个向量查询得到 `S_i`，组成

```
x = M^{-1} S   (mod p)
```

在 `mod 65537` 下做高斯消元。

### 完整脚本（已本地验证跑通）

```python
P, N, BUDGET = 65537, 38, 40

def attack(ask):
    """ask(w) -> 返回 oracle 的 value；w 必须满足 0<w<p 且 sum(w)%p==1"""
    a = (1 - (N - 1)) % P
    base = [1] * (N - 1) + [a]
    assert sum(base) % P == 1 and all(0 < x < P for x in base)

    vecs = [base]
    for i in range(N - 1):                     # i = 0..N-2
        w = list(base)
        w[i] += 1
        w[-1] -= 1
        assert sum(w) % P == 1 and all(0 < x < P for x in w)
        vecs.append(w)
    assert len(vecs) == N

    S = [ask(v) for v in vecs]                 # N 次查询，38 < 40

    # mod P 高斯消元
    A = [vecs[i][:] + [S[i]] for i in range(N)]
    for col in range(N):
        piv = next(r for r in range(col, N) if A[r][col] % P)
        A[col], A[piv] = A[piv], A[col]
        inv = pow(A[col][col], -1, P)
        A[col] = [(v * inv) % P for v in A[col]]
        for r in range(N):
            if r != col and A[r][col]:
                f = A[r][col]
                A[r] = [(A[r][c] - f * A[col][c]) % P for c in range(N + 1)]
    return [A[i][N] for i in range(N)]
```

### 本地验证结果

```python
secret = [random.randrange(1, P) for _ in range(N)]
got    = attack(lambda w: project(secret, w, mask))

assert got == secret        # ✅ 恢复成功
print("查询次数:", 38, "/ 预算 40")
```

恢复出来 `x[0:3] = [17612, 8272, 33433]`，与 `secret[0:3]` 完全一致。

## 失败路径（踩过的坑）

1. **单位向量** `e_i`：`sum=1` 但其他项是 0，违反 `0<w<p`，直接 rejected。
2. **只用差分求绝对量**：差分只给 `x_i - x_last`，还需要一个基线方程提供绝对尺度，否则整体平移一个常数。
3. **忘记 oracle 返回已取模**：用未取模的 `S1` 做消元会整体错位。

## 出题视角

这题的精妙在于**预算 40 vs 维度 38**：它明示"不可能用 2n 次"，迫使你找线性结构。

任何"只校验线性约束"的 oracle 都等价于一个仿射空间投影 —— 至少 `n` 次查询就能完全解出。防御方式只有两种：

- 非线性约束（如要求 `w` 的某个子集为 0，破坏线性）
- 限制无法构造出互补向量（如要求所有 `w` 必须为正且不允许"负数补偿"）

类似变形：`sum(w) = 0`、`w` 的 L1 范数固定、或要求 `w` 为单位向量 —— 前两个仍可被差分绕过，最后一个才真正安全。
