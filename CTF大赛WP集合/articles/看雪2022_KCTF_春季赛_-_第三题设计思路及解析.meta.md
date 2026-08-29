---
title: 看雪2022 KCTF 春季赛 | 第三题设计思路及解析
contest: 看雪2022 KCTF春季赛
year: 2022
difficulty: hard
vuln_type: reverse
tags: [魔改AES, MD5作为AES key, S盒交换, shiftRow反向, 异常处理藏逻辑, 静态硬刚]
attack_chain: MD5(已知字符串)作AES密钥→k[42]=0xD4AF3085魔改→AES keyExpansion调swap_aes_sbox交换S[113]/S[163]→invShiftRows方向魔改→AES加密与已知数组对比→AES_DE_402070解出flag
key_payload: "k[42]=0xD4AF3085;swap_aes_sbox:inv_S[S[113]]与inv_S[S[163]]交换;invShiftRows ROF32(block, 8*i);byte_41C200[16]=244 byte_41C200[17]=242;flag{db5c6a8dfec4d0ec5569899640}"
one_liner: KCTF2022春Q3《石像病毒》：MD5作AES key+S盒交换+shiftRow方向魔改+异常处理藏逻辑
lesson: 魔改AES常见点：S盒交换/swaps、ShiftRows方向、keyExpansion、对比数组
quality: high
---

# 看雪2022 KCTF 春季赛 | 第三题设计思路及解析

**赛事**：看雪2022 KCTF春季赛 Q3《石像病毒》

**难度**：围观2253人，27队破解，一血2h13min（mininepRe战队）

**题目设计**：
- 已知字符串的MD5值作AES密钥
- 加密输入，与已知数组对比
- **异常处理藏魔改逻辑**（需细看汇编）
- 4个魔改点：
  1. **MD5魔改**：除0异常 → `exception_md5_change45` 改k[42] = 0xD4AF3085
  2. **AES S盒交换**：未知指令异常 → `exception_aes_sbox` 交换S[113]和S[163]
  3. **AES shiftRow方向**：未知指令异常 → 魔改移动方向
  4. **AES GMul**：除0异常 → 魔改比较密文字节

**破解思路**：
- patch掉异常处理调试 或 静态硬刚
- 编写exp对应魔改

**关键exp**：
```c
// 1. k[42] = 0xD4AF3085;
// 2. S盒交换
void swap_aes_sbox() {
    inv_S[S[113]] ^= inv_S[S[163]];
    inv_S[S[163]] ^= inv_S[S[113]];
    inv_S[S[113]] ^= inv_S[S[163]];
    return;
}

// 3. shiftRow魔改（方向反向）
int invShiftRows(uint8_t (*state)[4]) {
    uint32_t block[4] = {0};
    for (int i = 0; i < 4; ++i) {
        LOAD32H(block[i], state[i]);
        block[i] = ROF32(block[i], 8*i);  // 改为 ROR 或不同方向
        STORE32H(block[i], state[i]);
    }
    return 0;
}

// 4. 已知密文魔改
byte_41C200[16] = 244;
byte_41C200[17] = 242;
```

**AES解密**：
```c
char target[] = {0x57, 0x7C, 0xF5, 0x6D, ..., 0xE6, 0xCB};  // 32字节密文
char key[] = {0x2F, 0x65, 0xB1, 0xFF, ..., 0x05, 0x9D};  // 16字节AES key
char flag[33] = {0};
AES_DE_402070(key, 16, target, flag, 32);
```

**flag**：`flag{db5c6a8dfec4d0ec5569899640}`

**技术总结**：
- 魔改AES常见点：S盒swap、ShiftRows方向、keyExpansion、比较数组
- 异常处理（除0、未知指令）可隐藏逻辑流
- 静态硬刚：看汇编找异常handler
- patch异常绕过调试干扰

**质量评估**：高（4个魔改点详解 + flag）
