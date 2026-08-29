---
title: 看雪2023 KCTF年度赛 | 第五题·争分夺秒-设计思路及解析
contest: 看雪2023 KCTF年度赛
year: 2023
difficulty: medium
vuln_type: reverse
tags: [Windows CrackMe, 计算混淆代码nop, Base64+CRC32, 逆元模逆, 幻方对称加密, Key格式, 模式识别]
attack_chain: patch掉inside_dbg()调试器检测→nop混淆计算代码→求解a*x mod n=1小整数方程得到逆元→生成两个幻方+key1/key2异或→验证key1/key2唯一性
key_payload: "inside_dbg 0x402220调试器检测;nop混淆;a*x%n=1;0x7D45*x%0x346F8717=1逆元;0xD711*x%0x729969FF=1;key格式=4+2+key1+4+2+key2+4校验和;幻方对称加密"
one_liner: KCTF2023年度赛Q5《争分夺秒》Windows CrackMe：模式识别nop混淆+逆元模逆+双幻方对称加密
lesson: 计算混淆代码用模式识别特征+静态nop；逆元小整数方程a*x mod n=1直接枚举
quality: high
---

# 看雪2023 KCTF年度赛 | 第五题·争分夺秒-设计思路及解析

**赛事**：看雪2023 KCTF年度赛 Q5《争分夺秒》

**难度**：9队破解

**题目设计**：
- Windows CrackMe方案一
- 大量计算混淆代码干扰逆向
- 混淆代码有特征，可模式识别

**核心算法**：
- Base64统一输入范围
- **CRC32验证输入有效性**
- **逆元生成两个唯一Key**
- 使用Key生成幻方
- 幻方进行对称加密
- 逆元计算验证加密结果

**Key格式**（字节单位）：
```
| 4 | 2 | ####key1#### | 4 | 2 | ####key2#### | 4 |
| 幻|长 |              | 幻 |长|              |  |
| 方|度|              | 方 |度|              | 校验和|
|key|len|              |key |len|             |    |
```

**验证流程**：
1. base64解码
2. 校验和验证
3. 验证key1/key2长度
4. **通过逆元验证两个幻方key唯一性**
5. 根据两个幻方key分别生成两个幻方，并分别对key1和key2进行异或
6. 通过逆元验证key1和key2的唯一性
7. 通过所有验证返回成功

**赛题解析**：

**Step 1：反调试**
- inside_dbg() 0x402220 调试器检测
- 不管三七二十一，**静态patch使inside_dbg始终返回0**
- 否则触发 `*Block += rand() % 3 + 1` 等暗坑

**Step 2：nop混淆**
- 计算混淆代码有特征
- 模式识别后静态nop
- 看到核心算法

**Step 3：小整数方程逆元**：
```c
n = 0x346F8717; a = 0x7D45; // 求解x使得 a*x % n = 1
// 枚举结果：
A = 0x3153622a, 0x65c2e941, 0x9a327058, 0xcea1f76f  // 4个解

a = 0xD711; n = 0x729969FF; // 另一组
// 枚举结果：
B = 0x4372a49d, 0xb60c0e9c  // 2个解
```

**Step 4：枚举代码**：
```c
unsigned long long n = 0x346F8717i64;
unsigned long long a = 0x7D45i64;
for (unsigned int i = 0; i < -1; ++i) {
    unsigned long long x = i;
    if (a * x % n == 1) printf("0x%x\n", i);
}
```

**Step 5：日志断点 + 动静结合**
- 定位核心算法
- 求解最终key

**核心技术**：
- 计算混淆代码模式识别 + nop
- inside_dbg反调试patch
- 模逆元小整数方程枚举（多解）
- 幻方对称加密
- 校验和验证

**质量评估**：高（混淆模板 + 模逆枚举 + Key格式）
