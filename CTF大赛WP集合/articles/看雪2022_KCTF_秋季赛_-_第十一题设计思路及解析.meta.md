---
title: 看雪2022 KCTF 秋季赛 | 第十一题设计思路及解析
contest: 看雪2022 KCTF秋季赛
year: 2022
difficulty: hard
vuln_type: reverse
tags: [魔改DES, RSHash内存完整性, 22次正向迭代, 0x5B6364断点, 修正函数签名, KCTF作为name, non-pwn预期解]
attack_chain: IDA打开main函数无混淆→修正混淆函数签名→v70迭代变量贯穿→输入KCTF作name→0x5B6364断点→正向迭代22次后v391=correct serial→6FB1CE80914403C4
key_payload: "修正函数签名按push数确定参数个数;v70变量贯穿;0x5B6364断点;v391=correct serial;name=KCTF;serial=6FB1CE80914403C4"
one_liner: KCTF2022秋Q11《衣锦昼行》：魔改DES+RSHash+正向迭代22次+断点取serial的非预期解
lesson: IDA混淆函数按汇编push个数修正签名；正向迭代变量贯穿时中途断点取结果
quality: high
---

# 看雪2022 KCTF 秋季赛 | 第十一题设计思路及解析

**赛事**：看雪2022 KCTF秋季赛 Q11《衣锦昼行》

**难度**：4队提交（最终题）

**题目设计**：
- 修改过的DES算法
- RSHash保护算法部分内存完整性
- 未加壳无反调试
- 修改中间值1 bit也会对结果产生巨大影响（只能算法逆推）

**赛题解析（非预期解）**：

1. IDA打开，main函数（sub_5B4270）无混淆
2. main调用的其他函数都加了混淆（push个数识别参数）
3. main函数F5伪代码观感差
4. **修正所有函数类型**：根据汇编里调用函数前的push个数确定参数个数
5. 修正后main函数清爽

**核心算法**：
- 输入name → 计算出v365
- 输入serial → 计算出v395
- v365 == v395时登录成功
- v70变量贯穿大部分代码
- 输入serial前以v365为初值正向遍历v70迭代22次得到v391
- 输入serial后以serial为初值反向遍历v70迭代22次得到v395
- **正向反向计算互逆**

**非预期解**：
- 输入KCTF作name
- 在0x5B6364下断点查看正向迭代22次后的v391
- v391正好就是公开的serial

**答案**：
```
name: KCTF
serial: 6FB1CE80914403C4
```

**技术总结**：
- 混淆函数修复：根据汇编中调用函数前的push个数确定参数个数
- v70变量贯穿迭代 + 0x5B6364断点取中途结果
- 修正函数签名后交叉引用更准
- 修改中间值1bit结果巨变 → 需算法逆推

**质量评估**：高（非预期解法+答案+flag）
