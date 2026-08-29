---
title: 2023 SCTF Syclang 关于中间指令的分析
contest: SCTF 2023
year: 2023
difficulty: medium
vuln_type: reverse
tags: [Syclang IR, 自定义中间指令, 差分加密, 索引置乱, 数组加减, 看雪论坛]
attack_chain:
  - 解析 Syclang 自定义 IR 中间指令语法
  - 识别 4 个 exp 结构体 (var22/var23/var24/var25)
  - var22.L/R/X 8 组索引+偏移量硬编码
  - var23.key[0..23] 24 字节密文硬编码
  - 循环 1：exp.key[23-i] = input[i] 反序写入
  - 循环 2：差分 var22.key[i] -= var22.key[i-1]
  - 循环 3：8 组加减 var22.key[L[i]] += X[i] / var22.key[R[i]] -= X[i]
  - 循环 4：累加 var22.key[i] += var22.key[i-1]
  - 对 var23 做同样差分 + 减/加 var22.key[i*3] + 累加
  - 比较 var22 == var23
key_payload: 'var23.key[0..23] = {252, 352, 484, 470, 496, 487, 539, 585, 447, 474, 577, 454, 466, 345, 344, 486, 501, 423, 490, 375, 257, 203, 265, 125}'
one_liner: Syclang 自定义 IR 逆向：4 轮差分/加减/累加/索引置乱混合加密。
lesson: 自定义 IR 逆向关键是识别循环结构 + 操作类型，差分加密逆向就是反向累加。
quality: medium
---

# 2023 SCTF Syclang 关于中间指令的分析

## 来源
- 原文：ctfiot.com/125684.html
- 作者：NYSECbao（看雪 ID），感谢 s0rry 师傅帮助
- 平台：看雪论坛

## 题目描述
CTF 题给了一段 800 多行的 Syclang 自定义 IR 中间代码（作者感觉像 Go 语言风格）。

## 关键 IR 语法
```syclang
STRUCT exp :
 ARRAY .key(int)[24]<+0>      // 8 字节 * 24
 ARRAY .L(int)[8]<+192>
 ARRAY .R(int)[8]<+256>
 ARRAY .X(int)[8]<+320>

LABEL label4 :                  // 循环
 temp4 := #24
 IF var15<+56> < temp4 GOTO label3
 GOTO label2
LABEL label3 :
 ...
 GOTO label4
```

## 翻译后的 C 伪代码
```c
typedef struct { long long key[24]; long long L[8]; long long R[8]; long long X[8]; } exp;

int main() {
    exp var22, var23, var24, var25;
    
    // 索引硬编码
    var22.L[0]=0; var22.R[0]=8; var22.X[0]=11;
    var22.L[1]=15; var22.R[1]=23; var22.X[1]=-13;
    var22.L[2]=2; var22.R[2]=11; var22.X[2]=17;
    var22.L[3]=10; var22.R[3]=20; var22.X[3]=-19;
    var22.L[4]=6; var22.R[4]=13; var22.X[4]=23;
    var22.L[5]=9; var22.R[5]=21; var22.X[5]=-29;
    var22.L[6]=1; var22.R[6]=19; var22.X[6]=31;
    var22.L[7]=4; var22.R[7]=17; var22.X[7]=-37;
    
    // 密文硬编码
    var23.key[0..23] = {252,352,484,470,496,487,539,585,447,474,577,454,466,345,344,486,501,423,490,375,257,203,265,125};
    
    // 1. 反序写入
    for (i=0; i<24; i++) var22.key[23-i] = input[i];
    
    // 2. 差分
    for (i=23; i>0; i--) var22.key[i] -= var22.key[i-1];
    
    // 3. 索引置乱 + 加减
    for (i=0; i<8; i++) {
        var22.key[L[i]] += X[i];
        var22.key[R[i]] -= X[i];
    }
    
    // 4. 累加
    for (i=1; i<24; i++) var22.key[i] += var22.key[i-1];
    
    // 5. 对 var23 做同样处理 + 减 var22.key[i*3]
    for (i=23; i>0; i--) var23.key[i] -= var23.key[i-1];
    for (i=0; i<8; i++) {
        var23.key[L[i]] -= var22.key[i*3];
        var23.key[R[i]] += var22.key[i*3];
    }
    for (i=1; i<24; i++) var23.key[i] += var23.key[i-1];
    
    // 6. 比较
    for (i=0; i<24; i++) if (var22.key[i] != var23.key[i]) exit;
}
```

## 解题思路
- 把 IR 一行行翻译成 C 表达式
- 找到 4 个关键循环 + 1 个索引数组
- 差分加密的逆向就是反向累加
- 索引置乱逆向就是反向索引置乱

## 关键技巧
- **IR 模式识别**：循环结构 = LABEL + IF + GOTO
- **数组偏移**：`<+n>` 表示栈帧偏移，理解为结构体字段位置
- **结构体打包**：4 个 exp 共用同一份 L/R/X 索引表

## 适用场景
- 自定义 IR 字节码逆向
- 差分 + 索引置乱混合加密
- 看雪论坛中级 RE 题
