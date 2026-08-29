---
title: 看雪·众安 2021 KCTF 秋季赛 第四题 偶遇棋痴
contest: KCTF秋季赛
year: 2021
difficulty: hard
vuln_type: reverse
tags: [Lambda-Calculus, Church-Numeral, Boost-serialize, JNI, Android, z3, Syclover, ARM, unidbg, binary-tree]
attack_chain:
  - 出题方用 Lambda 演算（Church Numeral + ADD/SUB/MULT/IF/XOR/ABSDIFF）编码 flag 校验逻辑
  - 程序把 Lambda 表达式预编译后用 Boost text_oarchive 序列化到 C 字符串数组
  - 运行时反序列化回 Lambda 语法树
  - 用户输入 14 字符按 4bit 拆成 28 个 ipt
  - 把 28 个 ipt 插入预编译树的 28 个分支点
  - 调用 sub_39614 对整棵树做删减
  - 最终树只剩 3 个特定节点即通过
  - 关键：用户每个 4bit 输入对其他输入独立，可分 28 个独立 4bit 暴力（实际先低 4bit 后高 4bit）
key_payload: 'flag = (high4bit << 4) | low4bit, 28 个方程 z3 解 + 暴力枚举'
one_liner: 把 flag 验证逻辑用 Lambda 演算写出来序列化到 Android JNI，逆向时要还原 Lambda 语法树并独立爆破每个 4bit 输入。
lesson: Lambda 演算 + 序列化是隐蔽的"代码即数据"反模式，逆向者要么反序列化还原 AST（方式 1），要么爆破每个独立分支（方式 2）。
quality: high
---

# 看雪·众安 2021 KCTF 秋季赛 | 第四题 偶遇棋痴 出题方 Syclover 战队

**来源**: ctfiot.com ID 13578
**战队**: 辣鸡战队一血用时 108677 秒
**专家点评**: kkHAIKE（"题主立题新颖，让 lambda 演算有了新使用领域"）

## 题目立意
参赛题目叫"神秘的数学 (Android)"。设计思路：把 flag 验证逻辑用 **Lambda Calculus**（Church Numeral + Lambda 演算）实现，选手需要学习 λ 演算如何做数值/逻辑计算、currying、α-conversion、Beta Reduction、Church Boolean 等基础。

## 技术架构
- 提前用 Python 脚本生成 Lambda 表达式（28 个 ABSDIFF 方程）
- 通过 Boost 序列化组件将预编译的 Lambda 表达式序列化到 C 字符串数组
- 运行时反序列化得到 Lambda 语法树
- 用户输入 14 字符按 4bit 拆 28 个 ipt
- 把 ipt 插入语法树分支点
- 用 `sub_39614` 对整棵树做删减
- 最终只剩 3 个节点即成功

## 赛题解析（方式 1：还原 AST + z3）
1. IDA 看 sub_39998，输入字符串长度 14 时初始化一张表（无用）
2. 把每 4bit 转 dword，成长度 28 的数组
3. `sub_39658` 处理固定字符串 = boost::text_iarchive 反序列化
4. 反序列化出 v13（二叉树结构，每个节点 16 字节）
5. `sub_39910` 把 28 个 ipt 转 16 棵小树中的一颗插入二叉树
6. `sub_39614` 删减
7. 把树转为 Python 表达式：P = PP 结合双目运算；A = ADD；S = SUB；M = MULT；I = INC
8. z3 求解 28 个 IntVector 变量让最终结果 == 0
9. flag = `chr((high4bit << 4) | low4bit)` × 14

## 赛题解析（方式 2：独立分支爆破）
作者定制了一棵非常大的二叉树，用户每个 4bit 输入相对其他输入是独立的，可以拆为 28 道独立小题：
- 在保持 27 个输入不变时，求剩下那个输入使最终节点数最少的值
- unidbg 在 UXTB16 指令报错，改用 ARM 汇编转 C 代码暴力
- 第一次暴所有低 4bit，第二次暴高 4bit（可见字符最高位 0，仅 3bit）
- 指标改为"二叉树层数最少"

## Lambda 演算核心
```python
L_NUM(n): SUCC SUCC SUCC ... SUCC ZERO  # 嵌套 n 次
L_ADD(): \m\n\f\x m f (n f x)         # Church 加法
L_SUB(): \m\n n PRE m                  # 减法 = m 减 1 共 n 次
L_XOR(): \a\b a (NOT b) b              # 异或（仅 bool）
L_ABSDIFF(l, r): ADD(SUB(l,r), SUB(r,l))
```

## 28 个方程示例
```python
data = [(1, 2, 2), (2, 6, 20), (3, 5, 20), (5, 10, 40), ...]
# 28 组 (l1, d2, target) 即 |x_i * l1 + d2 - target| 的累加
flag_l[i] = (data[i][2] - data[i][1]) // data[i][0]
flag += chr((flag_l[2i+1] << 4) | flag_l[2i])
```

## 评价
学术+实战结合的精品题。Lambda 演算 + Boost 序列化 + JNI + 二叉树 4 重抽象，逆向路径有 2 条（AST 还原 vs 独立爆破）。是函数式编程与 CTF 结合的优秀范例。
