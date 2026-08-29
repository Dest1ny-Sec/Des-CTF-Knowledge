---
title: 羊城杯 2024/chal (Reverse)
contest: 羊城杯
year: 2024
difficulty: hard
vuln_type:
- reverse
tags:
- Cython
- IDA
- Python hook
- IDEA 魔改
- TEA 魔改
- XTEA 魔改
- random.seed 可控
- pkcs5padding
attack_chain:
- 题目给 chal.pyx 编译的二进制 + main.py
- dir(chal) 发现 _p1/_p2/_p3 函数和 _tips/_var1/_var2/_var3 属性
- IDA 打开 chal 二进制，识别 PyObject 操作和 _Pyx_CyFunction_New 系列
- 用 setattr hook chal.chal 的 _p1/_p2/_p3 拦截参数和返回值
- 分析 _p3 流程：XOR 填充 → IDEA 轮 → TEA → XTEA → TEA → XTEA → IDEA 轮
- 关键：random.seed 用 sum([2654435769-len(flag)] + flag ord 列表) 可控
- 关键：self.tips 累加 tmps[i] ^ random.getrandbits(8) 才是真校验
- 关键：self._var3 没用，是干扰项
- 还原随机数生成 → 解 IDEA/TEA/XTEA 魔改密文 → 拿 flag
key_payload: "setattr(chal.chal, '_p1', hook_p1); chal.chal('a'*48)  # 拦截函数调用"
one_liner: Cython 逆向 + Python 函数 hook + random.seed 已知还原魔改 IDEA/TEA/XTEA
lesson: Cython 编译的 Python 库仍可从 .so 中逆向出 PyObject 结构和函数指针；用 setattr hook Python 函数比纯静态逆向快 10 倍；random.seed 用 flag 长度+内容生成时可枚举
quality: high
---

# 羊城杯 2024/chal (Reverse)

**Cython 逆向 + Python 函数 hook + random.seed 已知还原魔改 IDEA/TEA/XTEA**

> 羊城杯 · 2024 · hard · reverse · quality=high
> 思路: 题目给 chal.pyx 编译的二进制 + main.py → dir(chal) 发现 _p1/_p2/_p3 函数和 _tips/_var1/_var2/_var3 属性 → IDA 打开 chal 二进制，识别 PyObject 操作和 _Pyx_CyFunction_New 系列 → 用 setattr hook chal.chal 的 _p1/_p2/_p3 拦截参数和返回值 → 分析 _p3 流程：XOR 填充 → IDEA 轮 → TEA → XTEA → TEA → XTEA → IDEA 轮 → 关键：random.seed 用 sum([2654435769-len(flag)] + flag ord 列表) 可控 → 关键：self.tips 累加 tmps[i] ^ random.getrandbits(8) 才是真校验 → 关键：self._var3 没用，是干扰项 → 还原随机数生成 → 解 IDEA/TEA/XTEA 魔改密文 → 拿 flag
> 套路: Cython 编译的 Python 库仍可从 .so 中逆向出 PyObject 结构和函数指针；用 setattr hook Python 函数比纯静态逆向快 10 倍；random.seed 用 flag 长度+内容生成时可枚举

**关键 payload**:
```python
setattr(chal.chal, '_p1', hook_p1)
chal.chal('a'*48)  # 拦截函数调用
```
