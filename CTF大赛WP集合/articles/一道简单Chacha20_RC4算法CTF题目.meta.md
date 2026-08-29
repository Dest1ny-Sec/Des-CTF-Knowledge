---
title: 一道简单 Chacha20 + RC4 算法 CTF 题目
contest: CTF练习
year: 2022
difficulty: medium
vuln_type: reverse
tags: [Chacha20, RC4, flower-instructions, anti-debug, IDA, srand-time-pid, time-brute-force, newu, 看雪]
attack_chain:
  - 32 位 VC++ 程序，无壳
  - IDA F5 反编译 main 函数：读 flag → 3 个未识别函数 → 输出 flag.enc
  - 关键: sub_401450 是 Chacha20（特征字符串 "expand 32-byte k"）
  - 花指令: 0x401468~0x40146C 红色未识别，0x40146A 强制跳转到 0x40146F
  - 去花: 0x40146E 按 D 转数据 + 0x40146F 按 C 转代码 + 0x40146A~0x40146E 改 0x90 (NOP) + 0x401450~0x401566 按 P 重定义函数
  - loc_401940 和 loc_401AA0 同样处理
  - 三个函数：Chacha20 + RC4 + PRNG seed
  - sub_401610 是 PRNG seed 生成器，srand(time(0) ^ pid)
  - RC4 key = "Encrypted!!" (12 字节)
  - Chacha20 key 由 PRNG 生成 32 字节
  - 爆破: timestamp [1662909722, 1662973302] × pid [1, 9000]
  - 判定: 解密后前 3 字符 == "fla"
key_payload: 'time(0) ^ pid 爆破 + ChaCha20XOR + RC4 + hexData[0:3] == "fla"'
one_liner: Reverse 32 位题：花指令 0x40146A 跳 0x40146F + Chacha20 + RC4 + srand(time^pid) 爆破。
lesson: 花指令去花三步走 (D 转数据 + C 转代码 + NOP 填充)；Chacha20 特征 "expand 32-byte k"；srand(time) 爆破时间窗口。
quality: high
---

# 一道简单 Chacha20 + RC4 算法 CTF 题目

**来源**: ctfiot.com ID 89178
**作者**: 看雪 ID `newu`

## 题目概述
- 32 位 VC++ 程序，无壳
- main 函数读 flag → 三个函数处理 → 输出 flag.enc
- flag.enc 48 字节

## 花指令处理
```text
0x401468 ~ 0x40146C 红色未识别
0x40146A 处跳转强制跳转到 0x40146F
破坏 IDA 栈帧识别
```

### 三步去花
1. 0x40146E 按 `D` 转数据
2. 0x40146F 按 `C` 转代码
3. 0x40146A ~ 0x40146E 改 `0x90` (NOP)
4. 0x401450 ~ 0x401566 按 `P` 重定义函数

loc_401940 和 loc_401AA0 同样处理。

## 三个核心函数

### sub_401450 = Chacha20
- 特征字符串 `"expand 32-byte k"`
- 20 轮 quarter round
- counter + nonce 12 字节

```c
void ChaCha20XOR(uint8_t key[32], uint32_t counter, uint8_t nonce[12],
                 uint8_t *in, uint8_t *out, int inlen) {
    int i, j;
    uint32_t s[16];
    uint8_t block[64];
    chacha20_init_state(s, key, counter, nonce);
    for (i = 0; i < inlen; i += 64) {
        chacha20_block(s, block, 20);
        s[12]++;
        for (j = i; j < i + 64; j++) {
            if (j >= inlen) break;
            out[j] = in[j] ^ block[j - i];
        }
    }
}
```

### loc_401940 = RC4
- S 盒 256 字节初始化
- 加密/解密同算法

### sub_401610 = PRNG seed
- `srand(time(0) ^ pid)`
- 32 字节 key 由 rand() 生成

## 解题脚本
```c
void get_flag(unsigned char *mykey, int v0, int pid) {
    unsigned char s[256] = {0};
    unsigned char key[12] = "Encrypted!!";
    char hexData[48] = {
        0xFC, 0xD4, 0x19, 0x74, 0x51, 0x67, 0xED, 0x4B, 0x9C, 0x48,
        0xC6, 0x5F, 0x9B, 0x5D, 0xB4, 0xF0, 0x44, 0x02, 0xAF, 0xAC,
        0x66, 0x01, 0x06, 0xA5, 0xBE, 0xBC, 0xD0, 0x77, 0x29, 0x64,
        0x8D, 0x5E, 0x41, 0xD4, 0x77, 0x31, 0x40, 0xB4, 0x92, 0x22,
        0xF9, 0x9F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    };
    int enc_len = strlen(hexData);
    rc4_init(s, key, strlen((const char *)key));
    rc4_crypt(s, (uint8_t *)hexData, enc_len);
    ChaCha20XOR((uint8_t *)mykey, 1, key, (uint8_t *)hexData, strlen(hexData));
    if (hexData[0] == 'f' && hexData[1] == 'l' && hexData[2] == 'a') {
        printf("timestamp:%d, pid:%d ", v0, pid);
        for (int i = 0; i < 48; i++) printf("%c", hexData[i]);
        printf("\n");
        exit(0);
    }
}

int main() {
    unsigned char mykey[32];
    int timestamp;
    DWORD Seed;
    for (int pid = 1; pid < 9000; pid++) {
        for (timestamp = 1662909722; timestamp <= 1662973302; timestamp++) {
            Seed = timestamp ^ pid;
            srand(Seed);
            for (int i = 0; i < 32; ++i)
                mykey[i] = (unsigned __int16)rand() >> 8;
            get_flag(mykey, timestamp, pid);
        }
    }
    return 0;
}
```

## 爆破参数
- **timestamp 范围**: 1662909722 (2022-09-11 23:22:02) ~ 1662973302 (2022-09-12 17:01:42)
- **pid 范围**: 1 ~ 9000
- **关键**: 时间要从出题时间点开始算，不是当前时间

## 评价
一道标准的 Reverse 入门提升题：
- **花指令识别与去花**（IDA 三步操作）
- **Chacha20 + RC4 双层流密码**（关键看 "expand 32-byte k"）
- **srand(time^pid) 爆破**（流密码速度极快）
- **反调试**（题目未深入利用，静态分析即可）
