---
title: 'HKCERT CTF 2022 Postmortem (III): The Remaining Challenges'
contest: HKCERT CTF 2022
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags:
- misc
- z3-solver
- mycraft
- java
- weighted-baked-model
- getRotation
- random-seed
attack_chain:
- '序列: ? 1 37 37 97 / ? 33'
- '序列: ? 1 85 85 97 / ? 85 / ? 2 2 26 97 / ? 24'
- 'z3求解: xs[0..m-1]整数数组'
- '约束: 严格递增+不重复+<q'
- sum[0]=xs[0], sum[i+1]=sum[i]+(i+2)*xs[i+1]
- product[0]=xs[0], product[i+1]=product[i]*(i+2)*xs[i+1]
- sum[m-1] % q == s, product[m-1] % q == p
- 'Java getRotation: x*3129871 ^ z*116129781 ^ y'
- seed = (l*l*42317861 + l*11) >> 16
- Random.nextLong() % 4
key_payload: z3.Solver + xorshift seed + weighted-baked-model
one_liner: HKCERT 2022 Misc：z3求解Minecraft mycraft+getRotation种子
lesson: Java Random种子可由x,y,z坐标异或重建
quality: high
full_path: HKCERT_CTF_2022_Postmortem_(III)-_The_Remaining_Challenges.full.md
meta_path: HKCERT_CTF_2022_Postmortem_(III)-_The_Remaining_Challenges.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'HKCERT CTF 2022 Postmortem (III): The Remaining Challenges。HKCERT 2022 Misc：z3求解Minecraft mycraft+getRotation种子。关键路径：序列: ? 1 37 37 97 / ? 33 → 序列: ? 1 85 85 97 / ? 85 / ? 2 2 26 97 / ? 24 → z3求解: x...'
category: misc
subcategory: misc_other
tools_used:
- Java
- Z3
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/87574.html
reasoning_chain:
- 触发点：题目交互序列 '? m s p q' + 每次返回整数序列 xs[0..m-1] → 假设：约束 sum[i+1] = sum[i] + (i+2)*xs[i+1], product 同理，且 sum[m-1] % q == s, product[m-1] % q == p → 动作：用 z3 求解
- 观察：z3.Int 数组 + 严格递增约束 + 不重复约束 → 下一步：循环 100 次 track 跑 z3.solve → 观察：xs 解出后 sendline 提交
- 触发点：Minecraft getRotation 源码 l = x*3129871 ^ z*116129781 ^ y → 假设：seed 是 (l*l*42317861 + l*11) >> 16 + Java Random.nextLong()%4 → 动作：对 -20000≤x≤20000, 0≤y≤256 暴力枚举
- 观察：每个坐标 (x,y,z) 对应确定旋转 → 下一步：拿题目给的 10 组坐标 (x0..x9, y0..y9, z0..z9) 反推 seed
- 假设：rotation 值与种子一一对应 → 动作：枚举 x∈[-20000,20000], y∈[0,256], z∈[-20000,20000]，匹配全部 rotation → 观察：得到 (x0,y0,z0)
failed_attempts:
- 试图直接对 16 个维度建立 z3 整数约束 → 失败：z3 对单纯 mod q 约束在大整数下求解慢
- 试图用 Sage discrete_log 还原 Minecraft Random → 失败：Java Random 是 LCG+位运算，需从坐标枚举种子
key_observations:
- Java Random 种子可由 x*3129871 ^ z*116129781 ^ y 三个坐标线性异或还原，是 Minecraft 等 voxel 游戏题目的常见考点
- z3 求解 sum/product 链式约束 + 严格递增是 CTF Crypto 难题通用思路
- rotations 0-3 + Java nextLong() % 4 把 LCG 输出映射到 4 个值，暴力枚举坐标范围即可逆推
- Minecraft WeightedBakedModel.getQuads 内部调用 Random.nextLong() 是已知热点
prerequisites:
- z3 Solver Python 绑定 + Implies/Not/Int 约束建模
- Java Random (LCG + next(32)) 内部实现
- Minecraft getRotation / WeightedBakedModel 源码
- Python itertools + rich.progress track 进度条
---
# HKCERT CTF 2022 Postmortem (III): The Remaining Challenges

> 原文: https://www.ctfiot.com/87574.html
> ID: 87574


```
nc HOST PORT
? 1 37 37 97
? 33
?
nc HOST PORT
? 1 85 85 97
? 85
? 2 2 26 97
? 24
?
from pwn import *
from z3 import *
from operator import add, mul
from functools import reduce
from rich.progress import track
import itertools

# TODO: change this to the remote service
r = process('./chall')

for _ in track(range(100)):
 r.recvuntil('? '.encode())

 m, s, p, q = map(int, r.recvline().decode().split())

 _s = Solver()
 xs = [Int(f'x_{i}') for i in range(m)]

 subss = [Int(f'ss_{i}') for i in range(m)]
 subps = [Int(f'ps_{i}') for i in range(m)]

 # The base conditions
 for i in range(1, m):
 _s.add(xs[i-1] <= xs[i])
 for i in range(0, m):
 _s.add(Not(xs[i] <= 0))
 for i in range(0, m):
 _s.add(xs[i] < q)
 for i, j in itertools.product(range(0, m), repeat=2):
 _s.add(Implies(i != j, xs[i] != xs[j]))

 # The "s" and "p" requirements
 _s.add(subss[0] == xs[0])
 _s.add(subps[0] == xs[0])
 for i in range(m-1):
 _s.add(subss[i+1] == subss[i] + (i+2)*xs[i+1])
 _s.add(subps[i+1] == subps[i] * (i+2)*xs[i+1])
 _s.add(subss[m-1] % q == s)
 _s.add(subps[m-1] % q == p)

 assert _s.check() == sat
 md = _s.model()
 x0s = [md.evaluate(xs[i]) for i in range(m)]
 r.sendlineafter('? '.encode(), ' '.join(map(str, x0s)).encode())

print(r.recvline().strip().decode())
From above, we know (x0+0, y0+0, z0+0) is pointing rightwards and
 (x0+0, y0+0, z0+1) is pointing leftwards and ... and
 (x0+1, y0-2, z0+9) is pointing rightwards
for some (x0, y0, z0).

For each -20000 <= x <= 20000, 0 <= y <= 256, -20000 <= z <= 20000:
 If (x+0, y+0, z+0) is pointing rightwards and
 (x+0, y+0, z+1) is pointing leftwards and ... and
 (x+1, y-2, z+9) is pointing rightwards, then:
 (x, y, z) are the coordinates we want!
// An Java implementation of the `getRotation`
public static long getRotation(int x, int y, int z) {
 // Math#getSeed
 long l = (long)(x * 3129871) ^ (long)z * 116129781L ^ (long)y;
 l = l * l * 42317861L + l * 11L;
 long seed = l >> 16;

 // ModelBlockRenderer#tesselateWithAO
 Random random = new Random(seed);

 // WeightedBakedModel#getQuads
 return Math.abs(random.nextLong()) % 4;
}
public long nextLong() {
 return ((long)(next(32)) << 32) + next(32);
}
func getRotation(x, y, z int) int32 {
	/*
 long l = (long)(x * 3129871) ^ (long)z * 116129781L ^ (long)y;
 l = l * l * 42317861L + l * 11L;
 long seed = l >> 16;
	*/
	x2 := int(int32(x * 3129871))
	z2 := z * 116129781

	l := x2 ^ y ^ z2
	l = l * (l*42317861 + 11) // l = l*l*42317861 + l*11

	seed := l >> 16

	/*
 Random random = new Random(seed);
	*/
	seed ^= 0x5DEECE66D

	/*
 return Math.abs(random.nextLong()) % 4;
	*/
	v := int32((seed*0xBB20B4600A69 + 0x40942DE6BA) >> 16)
	if v < 0 {
 v = -v
	}
	return v & 3
}
```
