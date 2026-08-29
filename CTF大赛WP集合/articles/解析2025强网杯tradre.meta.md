---
title: 解析2025强网杯tradre
contest: 强网杯 2025 tradre
year: 2025
difficulty: hard
vuln_type: reverse
tags: [control-flow-obfuscation, basic-block, state-transition, alarm-bypass, signal-SIGCHLD, AES-modified, S-box-XOR, fork-anti-debug, minimal-patch, dispatcher]
attack_chain:
- ELF 64位LSB+Full RELRO+Canary+NX+No PIE
- 大小:29160字节+入口0x400910+代码段0x400000-0x405288
- 数据段:0x605d58-0x608160
- 基本块结构体:0x606AC0
- 转储大小:16318字节+182个基本块+176种状态转移函数
- improved_dump.bin:5792字节+181/181非空基本块
- 恢复代码大小:1882字节+生成反汇编代码:555行
- 修补位置:文件偏移0x47eb
- 修补内容:mov $60, %edi → mov $0, %edi (alarm(60)→alarm(0))
- 生成:minimal_patch_tradre
- 反调试:fork()+alarm(60)+signal(SIGCHLD)
- 加密:固定seed+rand()+AES-128(16字节密钥)+32字节XOR密钥循环混淆256字节S盒
- 三重XOR:随机数 ^ XOR密钥 ^ 原始字节
- 密文:3136323964353231323863613339356534663661306663393837313261336531 / ASCII:1629d52128ca395e4f6a0fc98712a3e1
- 信号:SIGCHLD(监控子进程)+SIGTRAP(处理int3断点)+SIGALRM(60秒超时)
- 状态转移:0x0(JMP)+0x401CA6(JLE)+0x401D22(JNE)+0x401D5B(JE)+0x401DCD(JNS)+0x401F0C(JG)+0x401C31(JL)+0x401EB4(CALL)+0x401EA5(EXT)+0x401E96(RET)
key_payload: minimal_patch_tradre (alarm(60)→alarm(0))
one_liner: 强网杯2025 tradre逆向,Full RELRO+Canary+NX+No PIE+控制流平坦化(182基本块+176状态转移)+fork()反调试+alarm(60)修补(mod $60, %edi→$0, %edi)+AES-128(固定seed+32字节XOR密钥循环混淆S盒)。
lesson: tradre是2025强网杯控制流混淆+多反调试+魔改AES的高级题;alarm(60)单点patch是绕过60秒超时的标准方法;S盒三重XOR(随机数^XOR密钥^原始字节)需要从已知seed爆破。
quality: high
---

## 题目列表

1道Reverse:tradre(强网杯2025)

## 关键考点

### 文件信息
- ELF 64位LSB+大小29160字节
- 保护:Full RELRO+Canary+NX+No PIE
- 入口:0x400910
- 代码段:0x400000-0x405288
- 数据段:0x605d58-0x608160
- 基本块结构体:0x606AC0

### 控制流平坦化
- 代码段起始:0x4009F7
- 转储大小:16318字节
- 182个有效基本块+176种状态转移函数
- improved_dump.bin:5792字节(精确匹配期望大小)
- 非空基本块:181/181(100%完整度)
- 状态转移函数分布:涵盖176种不同类型
- 拓扑排序成功:181个基本块
- 恢复代码大小:1882字节
- 生成反汇编代码:555行

### 反调试
- fork():创建子进程执行混淆代码
- alarm(60):60秒执行时间限制
- signal():SIGCHLD信号处理
- 地址:0x4047eb
- 指令:mov $0x3c, %edi(0x3c=60)

### 修补
- 修补位置:文件偏移0x47eb
- 修补内容:mov $60, %edi → mov $0, %edi
- 修补效果:alarm(60) → alarm(0)
- 生成文件:minimal_patch_tradre

### 加密算法
- 固定seed:确保每次运行结果相同
- 使用标准C库rand()函数
- 密钥长度:16字节(AES-128)
- 使用32字节XOR密钥循环混淆256字节S盒
- 掩盖了标准AES的字节替换操作
- 三重XOR:随机数 ^ XOR密钥 ^ 原始字节
- 随机数序列由已知的种子确定
- 分成两部分加密,增加分析复杂度

### 密文
- 十六进制:3136323964353231323863613339356534663661306663393837313261336531
- ASCII:1629d52128ca395e4f6a0fc98712a3e1

### 信号
- SIGCHLD:监控子进程状态变化
- SIGTRAP:处理int3断点指令
- SIGALRM:60秒超时强制终止

### 状态转移函数
- 0x0 JMP 无条件跳转 ✓
- 0x401CA6 JLE 小于等于跳转 ✓
- 0x401D22 JNE 不等于跳转 ✓
- 0x401D5B JE 等于跳转 ✓
- 0x401DCD JNS 非负跳转 ✓
- 0x401F0C JG 大于跳转 ✓
- 0x401C31 JL 小于跳转 ✓
- 0x401EB4 CALL 内部调用 ✓
- 0x401EA5 EXT 外部调用 ✓
- 0x401E96 RET 返回

## 实战价值
- tradre是2025强网杯控制流混淆+多反调试+魔改AES的高级题
- alarm(60)单点patch是绕过60秒超时的标准方法
- S盒三重XOR(随机数^XOR密钥^原始字节)需要从已知seed爆破
- 控制流平坦化的176种状态转移函数是2025新高度
- 最小化patch(minimal_patch)是CTF逆向的高效策略
