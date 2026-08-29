---
title: 一道关于逆向的实战CTF题目分析
contest: 实战逆向 CTF
year: 2024
difficulty: easy
vuln_type: reverse
tags: [left函数, xor函数, 32轮调度, dword数组, 简单C还原]
attack_chain:
  - IDA 反编译 left(a1,a2): printf("%c", ((a1 ^ a2) >> 8))
  - xors(a1,a2): printf("%c", (((a1 + a2) >> 8) ^ a2))
  - dword_402120[32] 已知 32 个 16 位数
  - temp[32]={1,0,0,1,0,1,1,0,...} 决定每轮调用 left/xor
  - temp[i]=1 调 left(dword[i], 8)
  - temp[i]=0 调 xors(dword[i], 40)
  - 32 轮逐字节打印还原 flag
key_payload: 'flag{(a1^a2)>>8 | ((a1+a2)>>8)^a2}'
one_liner: 自实现 left/xor 双函数 + 32 轮调度 + dword 数组还原 flag。
lesson: IDA 反编译时遇到 `((a2 ^ a1) << 8) - a2` 这种结构要还原原始算术语义；32 轮调度类 VM 用 C 复写比反汇编快 10 倍。
quality: medium
---

# 一道关于逆向的实战CTF题目分析

## 概览
- **来源**: ctfiot 193276
- **类型**: 简单逆向实战

## 核心函数
```c
int sub_401040(char a1, int a2) {
    return ((a2 ^ a1) << 8) - a2;  // left 调度
}
int sub_401080(char a1, int a2) {
    return a2 ^ (a1 << 8);  // xor 调度
}
```

## 还原
```c
#include <stdio.h>

void left(unsigned int a1, unsigned int a2) {
    // (a1>>8)^a2
    printf("%c", ((a1 ^ a2) >> 8));
}

void xors(unsigned int a1, unsigned int a2) {
    // ((a1+a2)>>8)^a2
    printf("%c", (((a1 + a2) >> 8) ^ a2));
}

int main() {
    unsigned int dword_402120[32] = {
        0x00004408, 0x000068D8, 0x00007AD8, 0x00004308, 0x00007BD8, 0x00004608, 0x00007B08, 0x000070D8,
        0x00003308, 0x00007308, 0x000076D8, 0x00005CD8, 0x000076D8, 0x00006608, 0x00006908, 0x00006E08,
        0x00004BD8, 0x000076D8, 0x00003FD8, 0x00006F08, 0x00005ED8, 0x000076D8, 0x00007408, 0x000046D8,
        0x00005F08, 0x00006308, 0x00003408, 0x00007408, 0x000076D8, 0x000044D8, 0x00004CD8, 0x00007D08
    };
    int temp[32] = {1,0,0,1,0,1,1,0,1,1,0,0,0,1,1,1,0,0,0,1,0,0,1,0,1,1,1,1,0,0,0,1};
    
    for (size_t i = 0; i < 32; i++) {
        if (temp[i]) {
            left(dword_402120[i], 8);
        } else {
            xors(dword_402120[i], 40);
        }
    }
    return 0;
}
```

## 教学
- 32 轮调度是 RE 入门常见套路
- `dword_402120` 数组初始值用 IDA Export Data 提取
- `temp` 数组是 IDA 看 cmp/jne 跳转条件汇总
