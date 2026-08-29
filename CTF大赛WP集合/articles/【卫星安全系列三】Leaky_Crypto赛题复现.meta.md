---
title: 【卫星安全系列三】Leaky Crypto赛题复现
contest: Hack-A-Sat / Leaky Crypto
year: 2023
difficulty: hard
vuln_type: crypto_oracle
tags: [AES侧信道, T-表Cache碰撞, 时间差分析, 密钥链还原, AES-128-ECB, 卫星载荷, THRESHOLD]
attack_chain:
  - 题目：100000 个 (明文 hex, 加密时间 ns) 数据
  - AES-128-ECB + 密钥前 6 字节 97ca6080f575 已知
  - 密文 96 字节 flag 加密结果
  - AES T-表查表触发 Cache Hit/Miss
  - Cache Miss 慢 (10776), Cache Hit 快 (10704)
  - 公式: p[i] ^ key[i] == p[j] ^ key[j] (T-表同索引)
  - 链: 0→4→8 / 12→5→9→13 / 1→10→14→2 / 6→15→3→7 / 11
  - THRESHOLD=10 过滤弱信号
  - 已知 key[0..5] = 97ca6080f575 推 key[6..15]
  - key[6]={0xe4,0xe5,0xe6,0xe7} 4 候选
  - itertools.product 笛卡尔积 (4^10 = 1048576)
  - AES 解密 + unpad + 'flag' 验证
key_payload: '97ca6080f575e646e557f755bf15685e + flag{uniform54349juliet:...}'
one_liner: AES T-表 Cache 侧信道攻击：100000 (明文, 时间) 数据 + 链式密钥字节还原 + AES 解密。
lesson: AES 软件实现 T-表 (SubBytes+ShiftRows+MixColumns 合并) 会因输入命中同一表项触发 Cache Hit 加速；T-表索引 p[i] ^ key[i] 同值 → Cache Hit → 加密时间短；构造 16 字节链 + THRESHOLD 过滤。
quality: high
---

# 【卫星安全系列三】Leaky Crypto赛题复现

## 概览
- **来源**: ctfiot 151037 (Hack-A-Sat / Leaky Crypto)
- **类型**: AES 侧信道攻击 + Cache 时序
- **难度**: ⭐⭐⭐⭐

## 题目文件
- `Readme.txt`: AES-128-ECB 加密 + 密钥前 6 字节 `97ca6080f575` 已知
- `test.txt`: 100000 个 (明文 hex, 加密时间 ns)
- 密文: `7972c157dad7b858596ecdb798877cc4...`

## AES T-表原理
- AES 4 步: AddRoundKey → SubBytes → ShiftRows → MixColumns
- 软件实现: 合并 SubBytes+ShiftRows+MixColumns 为 4 张 T-表 (T0/T1/T2/T3)
- 索引 = `p[i] ^ key[i]`: 命中同一表项 → Cache Hit (10704ns), Miss → 10776ns

## 攻击算法
```python
THRESHOLD = 10

def check(i, j, ki, kj):
    col, ncol = [], []
    for p, t in data:
        if p[i] ^ ki == p[j] ^ kj:
            col.append(t)  # Cache Hit
        else:
            ncol.append(t)  # Cache Miss
    r = mean(ncol) - mean(col)
    return r if r > THRESHOLD else None

def hack(chains):
    for i, j in chains:
        for ki in list(key[i]):
            for kj in range(256):
                r = check(i, j, ki, kj)
                if r and j > 5:
                    key[j].add(kj)

# 链: 0→4→8 / 12→5→9→13 / 1→10→14→2 / 6→15→3→7 / 11
chains = [(0, 4), (4, 8), (5, 9), (9, 13), (5, 12),
          (1, 10), (2, 14), (10, 14),
          (3, 7), (3, 15), (15, 6)]
```

## 密钥还原
- key[0..5] = `[151, 202, 96, 128, 245, 117]` (已知)
- key[6]={228,229,230,231} 4 候选
- 全部 16 字节笛卡尔积 4^10 = 1,048,576 种
- AES.new(k, MODE_ECB).decrypt(c) + unpad + 'flag' in p

## 答案
- 完整密钥: `97ca6080f575e646e557f755bf15685e`
- flag: `flag{uniform54349juliet:GL2aGs7ys8ygcW0kFBPLbwEdjLbwNltiPdX_ANqtOFbUpEh_ciY8tWZd4y2VblkUhOl-PxXJdJYK86pIHmmwcw0}`
