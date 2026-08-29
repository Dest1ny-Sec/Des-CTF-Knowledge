---
title: DATALOG 魔幻之力，N1CTF 2023 guess writeup
contest: N1CTF
year: 2023
difficulty: hard
vuln_type: misc_math
tags: [souffle, datalog, symbol-table, ordinal, 静态分析, 推理规则]
attack_chain:
  - 阅读 Soufflé 文档了解符号表机制
  - 理解 ordinal number 表示法
  - 利用 ord(@GETFLAG()) 推理规则
  - HINT(_) 触发 FLAG 关系防止被优化
  - __LINE__ 计算 salt 个数推算 flag 序号
  - as(序号, symbol) 反查
  - 36 轮不重置规则
key_payload: ord() 推 symbol table 序号 + __LINE__ 动态调整
one_liner: N1CTF 2023 guess 题用 Soufflé 静态分析引擎 + Datalog 推理规则恢复 flag 序号。
lesson: Soufflé 等静态分析引擎的 symbol table + 推理规则是新型 CTF 出题方向。
quality: high
---

N1CTF 2023 出题人 cscat + cyberutopian 联合出品的"guess"题完整解析。

**题目设计理念**
静态分析相关 CTF 题难以兼顾相关性与选手体验。Soufflé 是类似 Datalog 的逻辑编程语言执行引擎，广泛用于静态分析。题目让选手阅读 Soufflé 文档理解执行原理，用技巧获得 flag。

**Soufflé 源文件**
```souffle
.functor hash1(x: symbol): number
.functor hash2(x: symbol): number
.functor GETFLAG(): symbol

.decl SALT(x: symbol)
.output SALT
.decl FLAG(x: symbol)
FLAG(@GETFLAG()).
.decl HINT(x: symbol)
HINT(substr(x,0,4)) :- FLAG(x).
.decl HASH(x: number)
HASH(@hash1(x)) :- FLAG(x).
.decl SALT_HASH1(h: number, s: symbol)
SALT_HASH1(h,s) :- h=@hash1(cat(flg,s)), FLAG(flg), SALT(s).
.decl SALT_HASH2(h: number, s: symbol)
SALT_HASH2(h,s) :- h=@hash2(cat(flg,s)), FLAG(flg), SALT(s).
.decl GUESS(x: symbol)
.output GUESS(attributeNames="ans")
```

**约束**：
- GUESS 推理规则 < 300 字符
- 禁用 `Ff.` 三个字符
- 36 轮通过即拿 flag

**关键洞察**
在 Soufflé 中，字符串都存储在全局 symbol table 中，推理产生新字符串时插入获得序号。需要猜测的 flag 是 functor GETFLAG 产生的字符串，**会插入到 symbol table 中**。无法直接访问 flag，但可以猜测 symbol table 序号。

`x=as(序号, symbol)` 可以反查字符串；`ord(@GETFLAG())` 可得到 flag 字符串的序号。

**两大坑**：
1. 直接 `x=as(__LINE__-..., symbol)` 失败 — 关系 FLAG 没有被任何输出引用，Soufflé 优化器会删除 FLAG 关系，flag 也不再在 symbol table 中。解：添加 `HINT(_)` 触发对 FLAG 的依赖。
2. 如果规则用到了 SALT，会导致 Soufflé 先输出 SALT 再输出 GUESS。解：避免 SALT 依赖。

**最终解法**
用 __LINE__ 算 salt 个数，用 GUESS 行号偏移推算 flag 序号。

出题人是寻臻科技 cscat + 开放式代码分析 cyberutopian，关联 CodeQL/Doop/Soufflé 等静态分析框架。
