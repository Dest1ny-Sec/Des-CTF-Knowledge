---
title: 2023 强网杯 WriteUp by Arr3stY0u
contest: 强网杯 2023
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [RSA_p5, sage_nth_root, AES-CFB, pyModeS, ADS-B, XTEA, FSB, LD_PRELOAD hook, phoenixAES, ARC4, fpylll, ISIS]
attack_chain:
  - not only rsa: n=p^5, e=641747, sage Mod(c,n).nth_root(e, all=True) 找 flag
  - discrete_log: g=5 mod p, c 走 bsgs+padding 反推
  - babyrsa: p,q 共 100 bit kbits 共享，attack2 LLL 攻击 + 二次丢番图方程
  - Speed up: 2^27! 各位数求和
  - 石头剪刀布: AI 学习模式，固定套路试探
  - QAM 流量: wav 4-ary QAM 解调，2-bit/样点映射
  - rockyou AES-CFB: EVP_BytesToKey 派生 key，密文开 HTTP header 检索
  - pyModeS: 1090ES ADS-B 报文 tell() 解析航班号
  - aes_keyschedule: 末轮 key 反推 AES-128 完整 key schedule
  - rc4_license: ARC4("WelcomeToQWB2023") 解密 License.dat
  - fancy: LD_PRELOAD hook clock_gettime + 4-bit 拆分密文爆破
  - 0xGame QAM: scipy 读 wav, -3/-1/1/3 → 00/01/10/11
  - VMP VM: ida 模拟执行 sar/shl/add/cmp VM 指令
  - XTEA 32 轮加密: pwndbg 搜 key 内存，XOR + bswap 解密
  - 论文题 ISIS: fpylll BKZ + g6k Siever 解 SIS 短向量
key_payload: 'n = p^5, e = 641747, c (qwb RSA)'
one_liner: 12+ 道题：RSA p^5+BSGS+ADS-B+pyModeS+XTEA+VM+LD_PRELOAD+phoenixAES+ARC4+ISIS 论文题。
lesson: RSA p^5 用 sage nth_root 一步搞定；AES 末轮 key 已知反推完整 key schedule；XTEA 32 轮是入门题标配。
quality: high
---

# 2023 强网杯 WriteUp by Arr3stY0u

## 来源
- 原文：ctfiot.com/152049.html
- 作者：Arr3stY0u
- 比赛：强网杯 2023

## 12+ 道题详解

### crypto
1. **discrete_log** - p-1=2q 特殊 DLP，bsgs + padding 反推
2. **not only rsa** - n = p^5，sage `Mod(c, n).nth_root(e, all=True)` 找含 flag
3. **babyrsa** - p,q 共 100 bit 共享 kbits，attack2 LLL 攻击 + 二次丢番图
4. **QAM** - wav 4-ary QAM 解调：-3/-1/1/3 → 00/01/10/11
5. **rockyou** - AES-CFB 加密的 HTTP 流量，rockyou 字典 + EVP_BytesToKey 派生 key
6. **aes_keyschedule** - 已知末轮 key 反推 AES-128 完整 11 轮
7. **RC4 License** - ARC4("WelcomeToQWB2023") 解密 License.dat
8. **fancy** - LD_PRELOAD hook clock_gettime + 4-bit 拆分爆破
9. **XTEA 32 轮** - pwndbg 搜 key 内存，XOR + bswap 解密
10. **论文题 ISIS** - 美密 2023《Finding short integer solutions when the modulus is small》，fpylll BKZ + g6k Siever

### misc
11. **Speed up** - 2^27! 各位数求和
12. **石头剪刀布** - AI 学习模式固定套路
13. **pyModeS ADS-B** - 1090ES 报文 `pyModeS.decoder.tell()` 解析航班号

### reverse
14. **VMP VM** - ida 模拟执行 sar/shl/add/cmp VM 指令
15. **0xGame QAM** - scipy.io.wavfile 读音频解 4-ary QAM

## 关键技巧
- **RSA p^5**：sage nth_root 一步搞定，无需手算开根
- **babyrsa 共享 kbits**：LLL attack2 + 二次丢番图（参考虎符 RRSSAA）
- **AES 末轮 key**：aes_keyschedule 工具反推完整 11 轮 key schedule
- **XTEA 32 轮**：pwndbg search 找 key 内存，XOR + bswap 解密
- **ADS-B 1090ES**：pyModeS 库 `decoder.tell()` 一行解航班号
- **LD_PRELOAD hook**：hook clock_gettime 固定时间戳，4-bit 拆分逐字节爆破
- **phoenixAES**：末轮 AES 密文 + 末轮 key 反推主密钥
- **ISIS small q**：fpylll + g6k 联合 BKZ + sieve 攻击

## 适用场景
- RSA p^k 模数攻击
- AES key schedule 反推
- XTEA 入门
- ADS-B 1090ES 解析
- ISIS lattice
