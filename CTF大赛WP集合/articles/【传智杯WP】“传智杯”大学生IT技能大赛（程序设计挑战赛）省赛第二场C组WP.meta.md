---
title: 【传智杯WP】"传智杯"大学生IT技能大赛（程序设计挑战赛）省赛第二场C组WP
contest: 传智杯
year: 2026
difficulty: easy
vuln_type: misc_unknown
tags: [算法竞赛, 数论整除, 位运算OR, 平方数判定, DP-ovo, 二分查找, LCA, 树上差分]
attack_chain: 6 道算法题：A 整除判断 (l+2)/3 <= r/3 / B n*m 矩阵 OR 找 mask / C 偶数 + 奇数平方数 前缀和 / D 字符串"ovo" DP / E 二分 + 前缀和 k+m / F LCA + 树上差分
key_payload: mask = (1<<30) - 1  math.isqrt(x) % 2 == 1  up[k][v] 二分 LCA
one_liner: 传智杯 6 道算法题程序设计挑战赛 WP，整除判断 + 位运算 OR + 平方数 + DP + 二分 + LCA。
lesson: 程序设计挑战赛考察算法实现能力；(l+2)//3 <= r//3 整除判断；mask = (1<<30)-1 位运算 OR；math.isqrt(x) 平方数判定；树上差分是 LCA 类题标准解法。
quality: medium
---

# 【传智杯WP】"传智杯"大学生IT技能大赛（程序设计挑战赛）省赛第二场C组WP

## 概览
传智杯 6 道算法题程序设计挑战赛 WP，覆盖整除/位运算/平方数/DP/二分/LCA。

## A — 小苯点兵点将（整除判断）
```python
T = int(input())
for _ in range(T):
    l, r = map(int, input().split())
    print("YES" if (l + 2) // 3 <= r // 3 else "NO")
```

## B — 小苯的迷宫行走（位运算 OR）
```python
data = list(map(int, sys.stdin.read().split()))
ptr = 0
t = data[ptr]; ptr += 1
mask = (1 << 30) - 1
for _ in range(t):
    n = data[ptr]; m = data[ptr+1]; ptr += 2
    total = n * m
    end = ptr + total
    ans = 0
    while ptr < end:
        ans |= data[ptr]
        if ans == mask:
            ptr = end
            break
        ptr += 1
    ptr = end
    print(ans)
```

## C — 小苯的好数（前缀和 + 平方数）
```python
for _ in range(T):
    n = data[ptr]; q = data[ptr+1]; ptr += 2
    a = data[ptr:ptr+n]; ptr += n
    prefix = [0] * (n+1)
    for i in range(n):
        x = a[i]
        if x % 2 == 0:
            prefix[i+1] = prefix[i] + 1
        else:
            s = math.isqrt(x)
            if s % 2 == 1 and s * s == x:
                prefix[i+1] = prefix[i] + 1
            else:
                prefix[i+1] = prefix[i]
    for _ in range(q):
        l = data[ptr]; r = data[ptr+1]; ptr += 2
        print(prefix[r] - prefix[l-1])
```

## D — 小苯的ovo（DP）
- 在字符串中找最多 m 个 "ovo" 子序列
- 每次修改 cost[i] = "ovo" 三字符需修改数
- DP 状态: dp[i][m] = 前 i 字符选 m 个 "ovo" 最小 cost
- 转移: dp[i][m] = min(dp[i-1][m], dp[i-3][m-1] + cost[i-3])

## E — 小苯的水瓶（二分）
- 数组 + k + m，求最大可能水位
- 二分水位 + 前缀和

## F — 小苯的旅行计划（LCA + 树上差分）
- 树 n 节点 m 路径查询
- LCA 算总路径长度
- 树上差分统计边使用次数
- 找最大减少 = max(weight[v] * diff[v])

## 经验提炼
- 程序设计挑战赛考察算法实现能力
- (l+2)//3 <= r//3 整除判断
- mask = (1<<30)-1 位运算 OR
- math.isqrt(x) 平方数判定
- 树上差分是 LCA 类题标准解法
- DP 状态机：dp[i][m] = 选 m 个的成本最小值
- 二分 + 前缀和 双 log 复杂度
- LCA 倍增 up[k][v]
- "ovo" 字符串题 cost 计算三字符不等数
- BFS 构图 + 树重建
