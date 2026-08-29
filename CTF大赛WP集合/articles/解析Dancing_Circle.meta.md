---
title: 解析Dancing Circle
contest: Dancing Circle
year: 2024
difficulty: hard
vuln_type: reverse
tags: [sudoku, dancing-links, DLX, exact-cover, x64dbg, dynamic-analysis, byte-rotation, table-composition, anti-disassembly]
attack_chain:
- 双处数据校验→生成大数Num1,Num1×Num2得数独初盘Data1
- 解析Data1→初始化DLX(Dancing Links)精确覆盖问题
- 中心格不由用户输入,由9个调试检查函数返回推得必须=7
- 用户输入80位十六进制字符在cover()中分5小步做"交换+移位"
- 每60次交换得到一次向右90°旋转,共执行4次旋转回原位
- 5×60×4=1200次cover()调用,每格经历6次字节级查表变换
- 合成净变换T_net[0-9]=[11,181,163,154,228,232,129,94,134,151]
- L[T_net(D_i)]==S_i (∀i≠center)对UserData2查表后与DLX解逐位比较
- 匹配计数cnt=79(比较中心时cnt--)为通过条件
- 动态抓初盘与查表→合成T_net→DLX解数独→逐格穷举逆向80位hex输入→自检cnt
key_payload: 32415867057146038208672345171508423626351804840632517408215763137846025652307148
one_liner: Dancing Circle把"加密题"藏回数独与DLX,大整数生成数独初盘+DLX精确覆盖求解+5步×60次×4旋转=1200次cover+6次字节查表合成净变换T_net,IDA+Python复现全流程。
lesson: 复杂加密题常包装经典算法(数独+DLX),动态分析(x64dbg/IDA)比静态分析更有效;字节级查表合成T_net是经典混淆手段;精确覆盖建模是数独问题的本质。
quality: high
---

## 题目列表

1道逆向:Dancing Circle(数独+DLX伪装加密题)

## 关键考点

### 题目骨架
1. 双处数据校验 → 大数Num1
2. Num1 × Num2 → Data1(数独初盘)
3. DLX解数独 + 9个调试检查函数
4. 用户80位hex输入在DLX的cover()中分步交换+旋转+查表
5. 与DLX解逐位比较,cnt=79(中心-1)通过

### 核心机制
- 9×9=81个候选
- 4种约束:格子/行/列/宫
- 共324列约束矩阵
- DLX递归cover()/uncover()实现高效回溯
- 旋转:5小步×60次交换=1次90°右转,共4次转回原位
- 6张256字节表T1-T6合成净变换T_net

### 关键参数
- 数独初盘:标准9×9数独(展示在文中)
- 中心格固定=7
- T_net[0-9] = [11, 181, 163, 154, 228, 232, 129, 94, 134, 151]
- L[T_net(D_i)] == S_i(∀i≠center)
- 匹配阈值:79/80

### 数据
- 验证flag:32415867057146038208672345171508423626351804840632517408215763137846025652307148

### 复现策略
1. 动态断点抓数独初盘(在DLX矩阵填充前)
2. 导出6张变换表(严格按调用顺序)
3. 合成T_net
4. DLX解数独得S_i
5. 逐格穷举x∈[0..15]使L[T_net(x)]==S_i
6. 自检cnt==79

### 经验教训
- 多解情况:单格可能多于一个x使L[T_net(x)]==S_i,任选其一
- 中心位:脚本与程序都把中心格固定为7
- 编码:Windows运行注意Unicode

## 实战价值
- 复杂加密题常包装经典算法,识别算法本质是关键
- DLX(Dancing Links)是数独/精确覆盖问题的高效解法
- 动态分析比静态分析在字节级查表场景更有效
- 严格按调用顺序导出变换表才能合成正确T_net
