---
title: 从零开始的工控固件逆向之旅 – VxWorks密码哈希破解实战
contest: VxWorks 密码哈希 CTF
year: 2024
difficulty: medium
vuln_type: crypto_oracle
tags: [VxWorks, PowerPC, loginDefaultEncrypt, 魔数乘法, 字符变换, 碰撞攻击, 施耐德Quantum, 弱哈希]
attack_chain:
  - key.bin 973KB 固件 + extracted 4.6MB → VxWorks 6.40 RTOS PowerPC 施耐德 Quantum PLC
  - file/hexdump 提取元数据 (140-NOE-771-01 设备型号)
  - strings 搜 loginDefaultEncrypt @ 0x22F124
  - IDA Pro 反编译 PowerPC 汇编还原 C 算法
  - 加权求和: passwdInt += ASCII(char[i]) * (i+2) ^ (i+1)
  - 乘魔数 31695317 (0x1E3A1D5) & 0xFFFFFFFF 掩码
  - 字符变换: <'3'+33 / <'7'+47 / <'9'+65
  - 字典攻击 + 智能暴力破解 (FLAG+4字符, A-Z+0-9 36^4=1,679,616)
  - 0.07 秒 / 403,259 次/秒 找到 FLAGAWYZ
  - 32 位掩码丢弃高 5 位 → 434 个碰撞密码
key_payload: 'vx_hash(FLAGAWYZ) = cQwwddSRxS + 32 位掩码碰撞 434 个'
one_liner: VxWorks loginDefaultEncrypt 加权求和+魔数+32 位掩码导致大量碰撞，FLAG+4 字符 0.07 秒爆破。
lesson: VxWorks CVE-2010-2965 弱密码哈希无盐值 + 32 位掩码 (丢失 5 位) = 大量碰撞；防御要用 bcrypt/Argon2 + 随机盐值 + 多迭代 + 2FA。
quality: high
---

# 从零开始的工控固件逆向之旅 – VxWorks密码哈希破解实战

## 概览
- **来源**: ctfiot 283309
- **题目**: VxWorks 密码哈希破解 CTF
- **目标**: 找到生成 cQwwddSRxS 的密码
- **难度**: ⭐⭐⭐

## 固件识别
- `key.bin` 973KB + `_key.bin.extracted/385` 4.6MB
- `hexdump` 偏移 0x20: 设备型号 "140-NOE-771-01"
- 偏移 0x30: 编译时间 "Nov 21 14 12:03"
- 偏移 0x40: 固件描述 "Quantum Ethernet Executive firmware Ver. 6.40"
- 设备: 施耐德 Quantum PLC (VxWorks 6.40 RTOS + PowerPC)

## 算法还原
```c
STATUS loginDefaultEncrypt(char* in, char* out) {
    unsigned long magic = 31695317;  // 0x1E3A1D5
    unsigned long passwdInt = 0;
    if (strlen(in) < 8 || strlen(in) > 40) return ERROR;
    
    // Step 1: 加权求和
    for (ix = 0; ix < strlen(in); ix++) {
        passwdInt += (in[ix]) * (ix + 2) ^ (ix + 1);
    }
    
    // Step 2: 魔数乘法 + 32 位掩码
    sprintf(out, "%u", (long)(passwdInt * magic) & 0xFFFFFFFF);
    
    // Step 3: 字符变换
    for (ix = 0; ix < strlen(out); ix++) {
        if (out[ix] < '3') out[ix] += '!';   // +33
        if (out[ix] < '7') out[ix] += '/';   // +47
        if (out[ix] < '9') out[ix] += 'B';   // +65
    }
    return OK;
}
```

## Python 实现
```python
def vx_hash(password):
    if len(password) < 8 or len(password) > 40: return None
    magic = 0x1E3A1D5
    password_int = 0
    for i in range(len(password)):
        password_int += int(ord(password[i]) * (i + 2) ^ (i + 1))
    temp = str((int(password_int * magic) & 0xffffffff))
    output = ""
    for c in temp:
        if c < '3': output += chr(ord(c) + 33)
        elif c < '6': output += chr(ord(c) + 47)
        elif c < '9': output += chr(ord(c) + 65)
        else: output += c
    return output
```

## 破解过程
| 测试 | 密码 | 哈希 |
|---|---|---|
| 默认 | fdrusers | ycwxQxSS9 |
| 常见 | targettarget | Sxddcd9cSQ |
| **目标** | **FLAGAWYZ** | **cQwwddSRxS** ✓ |

- 字典攻击失败 → 智能暴力破解 FLAG+4 字符 (A-Z+0-9)
- 搜索空间 1,679,616 → 29,402 次找到 (1.75% 空间)
- 速度 403,259 次/秒, 耗时 0.07 秒

## 碰撞分析
- 32 位掩码丢弃高 5 位 (11001) → 大量碰撞
- 仅 FLAG**** 大写模式就有 **434 个碰撞**
- 真实密码 FLAGKNXY 与 FLAGAWYZ/FLAGAZWY 都能登录

## 防御措施
- **VxWorks**: 无盐值, 1 次迭代, 10^10 种, 弱
- **bcrypt**: 随机盐值, 2^12 迭代, 2^184 种, 强
- 使用 bcrypt/scrypt/Argon2 + 2FA

## CVE
- CVE-2010-2965: VxWorks weak password hashing
- CERT VU#840249
- CISA ICS-ALERT-10-214-01
