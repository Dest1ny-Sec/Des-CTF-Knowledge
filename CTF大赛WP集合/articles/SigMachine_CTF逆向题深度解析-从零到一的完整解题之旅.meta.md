---
title: SigMachine CTF 逆向题深度解析
contest: 自制 CTF 教学题
year: 2025
difficulty: hard
vuln_type: [reverse, misc_math]
tags: [ELF, x86-64, statically-linked, stripped, Linux-signal, sigaction, OLLVM, signal-handler, 反调试, SROP, 自定义加密, IDA]
attack_chain: ["file 命令识别 ELF 64-bit LSB 静态链接 stripped", "字符串定位: 0x47c093 'wrong!' 0x47c09a 'right!' 0x47c0a1 'password:'", "查 signal/sigaction 函数引用 → 注册信号处理器", "signal handler 里藏 flag 校验逻辑（保护主函数不让单步）", "反反调试: 用 ptrace 接管 / 改 signal handler 跳过", "静态链接 + stripped → 手工定位关键函数（搜索 0x400a70 等候选）", "OLLVM 混淆（控制流平坦化 + 虚假控制流）→ 用 D-810 反混淆插件", "还原加密函数: 输入 password → state machine → 比较 right! 决定输出"]
key_payload: "0x47c093 'wrong!' / 0x47c09a 'right!' / 0x47c0a1 'password:'"
one_liner: ELF+signal handler+OLLVM 三合一逆向入门
lesson: signal handler 是反调试常用手段；OLLVM 是工业级混淆；静态链接二进制要手动定位
quality: high
---

# SigMachine CTF 逆向题深度解析

原文 https://www.ctfiot.com/283400.html

## 题目概览
- ELF 64-bit LSB executable, x86-64
- statically linked（678KB）
- stripped（无符号）
- 融合：ELF 格式 / Linux signal / 自定义加密 / OLLVM 混淆

## 攻击链
### Step 1: file 命令
```bash
$ file sigmachine
sigmachine: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, stripped
```

### Step 2: 字符串定位
- `0x47c093` "wrong!"
- `0x47c09a` "right!"
- `0x47c0a1` "password: "

### Step 3: 信号处理器
- `sigaction(SIGUSR1, ...)` / `signal(SIGSEGV, ...)` 等
- 信号处理器内藏**反调试逻辑**：
  - 检测到 ptrace 跟踪时改变执行流
  - 校验 input 决定 "right!" / "wrong!"
- 主函数流程：注册信号 → 输入 password → 触发信号

### Step 4: 函数地址候选
| 字节（小端） | 反转后 | 函数地址 |
|------|------|------|
| 700a4000 00000000 | 0x00000000 00400a70 | 0x400a70 |
| 50194000 00000000 | 0x00000000 00401950 | 0x401950 |
| 90194000 00000000 | 0x00000000 00401990 | 0x401990 |
| f0194000 00000000 | 0x00000000 004019f0 | 0x4019f0 |

### Step 5: OLLVM 反混淆
- 使用 **D-810** IDA 插件
- 或用 **OLLVM-Unflattener**
- 控制流平坦化 + 虚假控制流 + 指令替换

## 教学价值
- **ELF 64-bit 文件结构** 入门
- **statically linked stripped** = 全靠逆向
- **Linux signal** = 反调试 / 隐蔽通信
- **OLLVM** = 工业级代码保护
- **IDA Pro + D-810** 反混淆
- **GDB / ptrace** 调试

## 工具
- IDA Pro + D-810
- Ghidra + OLLVM 反混淆
- pwntools
- file / readelf / objdump
- GDB + pwndbg
- unicorn engine
