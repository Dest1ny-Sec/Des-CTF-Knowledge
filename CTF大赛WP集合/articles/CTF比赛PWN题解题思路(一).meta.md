---
title: CTF比赛PWN题解题思路(一)
contest: 公众号文章（小话安全）
year: 2024
difficulty: easy
vuln_type: rop
tags: [pwn, 栈溢出, ret2shell, IDA, 入门]
attack_chain:
  - 题1：栈溢出admin+51字符+0x405D36覆盖返回地址shell函数
  - 题2：data输入0xc0字节覆盖v7变量与v5比较触发shell
  - 题3：gets栈溢出+RDI指向/bin/sh+调用system
  - 题4：gets栈溢出+vmmap找可写地址注入/bin/sh再system
key_payload: payload = b"a"*32+b"b"*8+rop()  # 含add rax,1;ret 循环
one_liner: 4道PWN入门题，栈溢出+返回地址覆盖+ROP思路
lesson: 栈溢出三要素：覆盖长度+目标地址+payload构造
quality: medium
---

# CTF比赛PWN题解题思路(一)

## 题目信息
- 来源：微信公众号「小话安全」4 道 PWN 题合集
- 类型：均为 Linux x86_64 入门栈溢出
- 工具：IDA / GDB / pwntools

## 关键攻击链
1. **题1 栈溢出基础**：输入 admin 触发分支，func 函数内 gets 栈溢出，0x405D36 为 shell() 函数入口，payload = admin + 51 字符 + 0x365D40
2. **题2 变量覆盖**：data 缓冲区 0xc0 字节溢出覆盖下方 v7 比较变量，输入已知数据绕过相等判断
3. **题3 ret2system**：gets 栈溢出，binary 自带 /bin/sh 字符串 + system 函数，RDI=/bin/sh 后 ret2system
4. **题4 注入 /bin/sh**：gets 栈溢出但无 /bin/sh 字符串，gdb vmmap 找可写地址（如 bss），先写 /bin/sh 再 system

## 关键技术点
- IDA 查找危险函数（system/shell/gets）
- gdb vmmap 寻找可写段
- 栈帧布局：buffer + saved_rbp + return_addr
- 小端序存储：地址需要倒序写入
- 计算 padding 长度（含 / 不含 admin 字符串）

## 评分
- quality: medium（讲解清晰，但无具体 exp 完整 payload，只有方法一/二的思路）
