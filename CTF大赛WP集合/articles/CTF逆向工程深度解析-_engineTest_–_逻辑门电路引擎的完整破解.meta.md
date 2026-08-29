---
title: CTF逆向工程深度解析: engineTest – 逻辑门电路引擎的完整破解
contest: 公众号文章
year: 2024
difficulty: hard
vuln_type: reverse
tags: [reverse, ELF, Z3, SAT, 逻辑门, 电路模拟, 符号执行]
attack_chain:
  - 静态分析ELF64 stripped二进制r2 aaa; s main; pdf
  - 解析cp/ip/op三个文件结构：电路配置+输入映射+输出映射
  - 提取门电路节点表+坐标编码
  - Z3建模为布尔可满足性问题求解flag
  - stdin输入36字符flag走完整电路验证
key_payload: r2 -q -c 'aaa; s main; pdf' ./engineTest; Solver().add(...)
one_liner: 逻辑门电路模拟flag验证，Z3建模为SAT求解
lesson: 复杂flag验证可降为SAT/Z3约束求解
quality: high
---

# CTF逆向工程深度解析: engineTest – 逻辑门电路引擎的完整破解

## 题目信息
- 文件：engineTest (22928 字节) / cp (1.3MB 电路配置) / ip (2184 字节) / op (520 字节) / go.sh
- 类型：64位 ELF stripped
- 输入：stdin 36 字符 flag
- 验证：通过 cp+ip+op 定义的电路模拟计算

## 关键攻击链
1. **静态分析**：`r2 -q -c 'aaa; s main; pdf'` 反汇编 main 函数，发现 5 个 argv 参数（程序名+cp+ip+stdin+op）
2. **文件结构解析**：
   - `cp` 电路配置：1383336 字节，定义门节点表
   - `ip` 输入映射：2184 字节，定义输入 bit → 电路输入线
   - `op` 输出映射：520 字节，定义电路输出线 → 验证位
3. **位运算坐标编码**：每个门节点用坐标 (x, y) 编码，bit 级运算
4. **Z3 SAT 建模**：用 `z3.Bool` 表示每条线状态，添加所有门约束（AND/OR/NOT/XOR），求解 flag 的 36*8=288 bit
5. **Solver 求解**：flag 一旦确定，电路输出应与 op 中的目标值匹配

## 关键技术点
- radare2 静态分析（替代 IDA 的开源选项）
- 电路模拟器反编译为 SAT 问题
- 布尔逻辑 → Z3 BitVec / Bool 求解
- 输入文件格式自定义：cp/ip/op 三件套

## 评分
- quality: high（思路新颖，把 flag 验证抽象为 SAT 问题，配 r2 截图）
