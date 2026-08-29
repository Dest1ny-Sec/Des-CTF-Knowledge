---
title: ナゾトキ x CTF? - 虹色の研究 - WriteUp
contest: ナゾトキ
year: 2023
difficulty: easy
vuln_type: reverse
tags: [虹色の研究, MineNumber-7, reversing, decompile, ASCII-sum, 0x309, 7 color, 日语]
attack_chain: 1. nc 12345 启动 MineNumber Search Engine /2. 输入名字生成 MineNumber /3. strings + grep flag/4. 反编译：local_58 字符串 ASCII 求和 /5. 输入名字 ASCII 和 = 0x309 (777) 触发 flag
key_payload: local_64 == 0x309  name ASCII sum = 777  flag.txt
one_liner: ナゾトキ x CTF 虹色の研究（日语 CTF 入门题），MineNumber=777 触发 flag 字符串输出。
lesson: 日语 CTF 入场题；ASCII 字符求和触发 flag 是入门级；strings + grep 找 flag 字符串；反编译看比较常量 0x309。
quality: medium
---

# ナゾトキ x CTF? - 虹色の研究 - WriteUp

## 概览
日语 CTF 入门题 ナゾトキ x CTF 之虹色の研究，MineNumber Search Engine。

## 攻击步骤
```bash
nc xxx.xxx.xxx.xxx 12345
```

```
************************
MineNumber Search Engine
************************
Enter your name:
DonGury
Your MineNumber is : 712
Don't mind. I'm looking for the 777.
```

## 反编译分析
```c
while ((local_60 < 0x40 && (local_58[(int)local_60] != 10))) {
    local_64 = local_64 + (int)local_58[(int)local_60];
    local_60 = local_60 + 1;
}
printf("Your MineNumber is : %d\n", (ulong)local_64);
if (local_64 == 0x309) {
    puts(flag);
    puts("You are the luckiest!");
}
```

- local_58 字符数组
- local_64 求 ASCII 字符和
- 比较 0x309 = 777

## strings 找 flag
```bash
strings 1_Reversing | grep -E "((nazo)|(777)|(flag))"
flag.txt
```

## 经验提炼
- 日语 CTF 入场题
- ASCII 字符求和触发 flag 是入门级
- strings + grep 找 flag 字符串
- 反编译看比较常量 0x309
- 0x309 = 777 是 MineNumber 目标
- ナゾトキ = 谜题
- 虹色 = 7 颜色（红橙黄绿青蓝紫）
- local_58 是栈上字符串
- while 循环 + != 10 终止（换行符）
- printf %d 输出十进制
