---
title: 看雪·2023 KCTF 年度赛 | 第二题设计思路及解析
contest: 看雪2023 KCTF年度赛
year: 2023
difficulty: medium
vuln_type: reverse
tags: [39球称量问题, 测量矩阵(-1/0/1), srand(time(0))随机, IsDebuggerPresent反调试, 称重问题]
attack_chain: IsDebuggerPresent反调试patch→srand(time(0))初始化→读Serial输入→称量矩阵4次测量→向量结果→验证
key_payload: "39球编号1-39;测量矩阵(0不选/1右侧/-1左侧);称量4次得向量;srand(time(0))确定随机;IsDebuggerPresent取反patch"
one_liner: KCTF2023年度赛Q2《CN星际基地》39球称量问题+测量矩阵+IsDebuggerPresent反调试
lesson: 称重问题用测量矩阵(0/-1/1)表示；每次测量结果-1/0/1；最少4次测量得解
quality: medium
---

# 看雪·2023 KCTF 年度赛 | 第二题设计思路及解析

**赛事**：看雪2023 KCTF年度赛 Q2《CN星际基地》

**难度**：围观2500+，11队提交（前3：98k/Nano/qswjjw）

**题目设计**：
- 39球称量问题
- 称量矩阵(0/-1/1)表示球位置
- 称量4次得向量结果

**测量矩阵说明**：
- 球体编号：1, 2, 3, ..., 38, 39
- **0**：不选取
- **1**：放在右侧
- **-1**：放在左侧
- 称量结果：
  - 0：相等
  - -1：左侧重
  - 1：右侧重

**示例**：
```
某一行测量：
1-13球体不参与（值为0）
14-20、22、32、33、37-39 → 右侧（值为1）
21、23-31、34-36 → 左侧（值为-1）
```

**称量4次**：
- 得到4维向量
- 用于反推

**赛题解析**：

**Step 1：反调试**
- IDA打开有反调试
- IsDebuggerPresent 的if判断取反patch

**Step 2：分析main函数**
```c
v3 = 0;
v132 = 0;
v4 = time64(0);
srand(v4);  // 随机种子用当前时间
v5 = sub_7FF6DD8E2F10(std::cout, &unk_7FF6DD8E66E8);
v6 = std::ostream::operator<<(v5, sub_7FF6DD8E30E0);
sub_7FF6DD8E2F10(v6, "Serial:\t\t");
// 提示 Serial:
LOBYTE(Src) = 0;
sub_7FF6DD8E2A90(&Src, &unk_7FF6DD8E6698, 0);
// std::cin 读取用户输入到Src
sub_7FF6DD8E32F0(std::cin, &Src, v8);
```

**Step 3：核心逻辑**
- 4次测量
- 比较结果

**核心技术**：
- 39球称量问题
- 测量矩阵表示（0/-1/1）
- 4次称量确定异常球
- srand(time(0))随机
- IsDebuggerPresent反调试patch

**质量评估**：中（题面清晰但具体SN和完整算法缺）
