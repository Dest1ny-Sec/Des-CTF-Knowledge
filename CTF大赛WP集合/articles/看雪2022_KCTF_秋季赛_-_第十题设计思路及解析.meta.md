---
title: 看雪2022 KCTF 秋季赛 | 第十题设计思路及解析
contest: 看雪2022 KCTF秋季赛
year: 2022
difficulty: hard
vuln_type: reverse
tags: [AES-CBC解密sc1, RSA快速分解, AES前缀枚举, 迷宫生成+验证, shellcode, 两个shellcode]
attack_chain: RSA快速分解n求私钥→AES key后缀AllIsNothing→前4字符暴力枚举(0-9)→python+vc混合枚举133秒得6结果→选能正常执行shellcode的1010→生成10x10迷宫→sc2验证路径30 31 32 33 43 53 52 51 61 71 72 73 74 84 94
key_payload: "AES-CBC IV=ABCDEF0123456789;后缀=AllIsNothing;前4枚举(0-9)横向纵向相加相等;AES key=1010AllIsNothing;迷宫10x10(00=通);路径30 31 32 33 43 53 52 51 61 71 72 73 74 84 94"
one_liner: KCTF2022秋Q10《两袖清风》：AES前4枚举+RSA后缀解+shellcode验证+迷宫路径算法
lesson: python+vc混合枚举速度；AES-CBC shellcode按执行结果筛选key
quality: high
---

# 看雪2022 KCTF 秋季赛 | 第十题设计思路及解析

**赛事**：看雪2022 KCTF秋季赛 Q10《两袖清风》

**难度**：5队攻破

**题目设计**：
- NoLimit CrackMe
- 两段shellcode（sc1生成迷宫+sc2验证迷宫）
- sc1通过AES加密（前4字符枚举+后RSA加密）
- 调试检测会生成错误伪迷宫

**关键步骤**：

**1. RSA分解n**：
- n可快速分解 → RSA私钥
- 解密得到AES后部分秘钥：`AllIsNothing`

**2. AES前4字符枚举**：
- python枚举(0-9)的4个字符
- vc解密sc1并执行（VirtualAlloc + memcpy + 函数指针执行）
- 横向纵向两个字符相加结果全相等
- 枚举133秒得6结果：`['1441', '1010', '2222', '2424', '3773', '4646']`

**3. 筛选能正常执行shellcode的key**：
- 1441: test edi,ebx
- 2222/3773: ret（直接返回）
- 2424: xor cl, [rbx+19]; ret
- 4646: adc ch, al; ret
- **1010: 完整执行call 1D18DAF0004 + 长shellcode** → 选1010

**4. AES key = 1010AllIsNothing**

**5. 迷宫生成**（10x10）：
```
01 01 01 01 01 01 01 01 01 01
01 01 01 01 01 01 01 01 01 01
01 01 01 01 01 01 01 01 01 01
00 00 00 00 01 01 01 01 01 01
01 01 01 00 01 01 01 01 01 01
01 00 00 00 00 00 00 01 01 01
01 00 01 01 01 01 00 01 01 01
01 00 00 00 00 01 00 00 00 01
01 01 01 01 00 01 00 01 01 01
01 01 01 01 00 01 01 01 01 01
```

**6. 路径**：
```
30 31 32 33 43 53 52 51 61 71 72 73 74 84 94
```

**7. 最终key格式**：
- RSA私钥 + AES前4字符 + 路径长度 + 路径坐标

**技术总结**：
- python+vc混合枚举加速（python调度+vc执行）
- AES shellcode解密后按执行结果筛选key
- RSA n快速分解得到后部分AES key
- 10x10迷宫用00=可通过表示

**质量评估**：高（枚举代码+迷宫+路径）
