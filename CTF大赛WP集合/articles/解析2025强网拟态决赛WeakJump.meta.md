---
title: 解析2025强网拟态决赛WeakJump
contest: 强网拟态 2025 决赛 WeakJump
year: 2025
difficulty: hard
vuln_type: reverse
tags: [statically-linked, stripped, ptrace-anti-debug, control-flow-flatten, TEA, feistel-cipher, dispatcher-block, dynamic-analysis, black-box, switch-case]
attack_chain:
- ELF 64位LSB+statically linked+stripped+BuildID
- 工具链:radare2/binutils/gdb/strace
- ptrace(PTRACE_TRACEME, 0, 0, 0)反调试
- 绕反调试:GDB的`catch syscall ptrace` + `commands ... end` + `set $rax = 0` + continue
- 关键字符串:Provide the flag for WeakJump / WeakJump clear / Nope, WeakJump resists you
- 算法:TEA (Tiny Encryption Algorithm) Feistel结构
- 数据块:8字节64位,左右各4字节32位,8轮,4组(共32字节)
- delta=0x9E3779B9(黄金分割),sum初值=delta*32=0xC6EF3720
- delta补码0x61C88647
- 控制流平坦化:switch-case+dispatcher+大量跳转+看似无意义计算
- 策略:不要深入分析混淆细节,将函数视为黑盒+动态分析
- axt @0x401639 查找字符串引用
key_payload: ptrace=$rax=0 + TEA Feistel
one_liner: 强网拟态2025决赛WeakJump逆向,静态链接+stripped+ptrace反调试(用GDB catch syscall ptrace改$rax=0绕过)+控制流平坦化(将函数视为黑盒+动态分析)+TEA Feistel(8字节块+4组+8轮+delta=0x9E3779B9)。
lesson: ptrace反调试用GDB catch syscall+set $rax=0绕过;TEA特征常量0x9E3779B9+0xC6EF3720+0x61C88647是快速识别;控制流平坦化不要深入分析,黑盒动态分析更高效。
quality: high
---

## 题目列表

1道Reverse:WeakJump决赛

## 关键考点

### 文件信息
- ELF 64位LSB+x86-64+statically linked+stripped+BuildID 0adf2873eac656282618b5479e72ec35e4f33ec9
- 工具:radare2/binutils/gdb/strace

### ptrace反调试
```c
ptrace(PTRACE_TRACEME, 0, 0, 0);  // 表示该进程请求被追踪
```
- 进程已被gdb追踪,再次调用失败
- 绕方法:GDB的catch syscall ptrace + commands + set $rax = 0 + continue
- 强制将ptrace返回值改为0(成功),程序认为ptrace调用成功

### 控制流平坦化
- 大量跳转指令+switch-case结构
- 看似无意义的计算
- 正常的顺序执行被打乱
- 通过分发器(dispatcher)控制执行顺序
- 代码块之间的逻辑关系被隐藏
- 防止算法被快速识别和提取
- 模拟真实恶意软件的保护手段

### 应对策略
- 不要深入分析混淆细节(会陷入细节消耗大量时间)
- 动态分析:将函数视为黑盒,只关注输入和输出
- 使用调试器获取运行时数据
- 符号执行(angr/Triton)
- 去混淆工具(D810 IDA插件)
- 二进制模拟器(Unicorn/Qiling)

### TEA算法
- 全称:Tiny Encryption Algorithm
- 数据块:8字节(64位)
- 左右各4字节(32位)
- 8轮迭代
- 4组数据(32字节输入)
- delta=0x9E3779B9(黄金分割比例*2^32)
- sum初值=delta*32=0xC6EF3720
- 加密/解密对称,只需反向使用密钥序列

### Feistel结构
- L[i+1] = R[i]
- R[i+1] = L[i] ⊕ F(R[i], K[i])
- F函数可以任意复杂单向函数
- 即使F不可逆,整个密码也可逆
- 安全性经过验证(DES使用了Feistel结构)
- 理论基础扎实
- 加密/解密使用相同的结构

### radare2命令
- r2 -q + aaa + iz:列出所有字符串
- axt @地址:查找引用指定地址的代码

## 实战价值
- ptrace反调试用GDB catch syscall+set $rax=0绕过
- TEA特征常量0x9E3779B9+0xC6EF3720+0x61C88647是快速识别
- 控制流平坦化不要深入分析,黑盒动态分析更高效
- 静态链接+stripped的逆向需要更强的控制流分析能力
- 符号执行(angr/Triton)和二进制模拟器(Unicorn/Qiling)是高级武器
