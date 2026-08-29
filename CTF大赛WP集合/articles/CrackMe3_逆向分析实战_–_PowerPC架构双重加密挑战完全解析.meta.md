---
title: CrackMe3 逆向分析实战 – PowerPC架构双重加密挑战完全解析
contest: 公众号文章
year: 2024
difficulty: medium
vuln_type: reverse
tags: [rev, powerpc, idea, rc6, dual-cipher, radare2, abiv2, stripped]
attack_chain:
  - file命令识别ELF 64-bit LSB PowerPC abiv2
  - radare2 r2 -q -c 'aaa; iz'列字符串
  - "Bingo!"在0x100024a8
  - fcn.10001740(2528字节)主要加密逻辑
  - fcn.10000c64(1196字节)辅助加密/密钥派生
  - 16字节(128-bit)IDEA标准Key
  - 24字节可能是加密输出
  - 双重加密：IDEA加密→RC6加密→与硬编码比较
key_payload: r2 -q -c 'aaa; iz' ./crackme3  # 找Bingo!和加密数据
one_liner: PowerPC64 CrackMe，IDEA+RC6双重加密逆向
lesson: 非x86架构二进制逆向需用file/readelf先确认，r2跨平台支持好
quality: high
---

# CrackMe3 逆向分析实战 – PowerPC架构双重加密挑战完全解析

## 题目信息
- 文件：13KB ELF 64-bit LSB executable, PowerPC abiv2
- 类型：动态链接 + stripped
- 工具：file / readelf / radare2

## 关键攻击链
1. **架构识别**：
   - `file crackme3` → ELF 64-bit LSB executable, 64-bit PowerPC, dynamically linked, stripped
   - PowerPC 是 RISC 架构，常用于服务器/网络设备/嵌入式
   - ABIv2 调用约定
2. **静态分析**：
   - `r2 -q -c 'aaa; iz' ./crackme3` 找字符串
   - "Bingo!" 在偏移 0x100005d0 + 0x24a8 = 0x100024a8
   - 入口点 0x100005d0
3. **函数识别**：
   - `fcn.10001740` 2528 字节（最大，主加密）
   - `fcn.10000c64` 1196 字节（次大，可能密钥派生）
4. **数据提取**：
   - 16 字节（128 位）= IDEA 标准 Key
   - 24 字节 = 加密输出
   - 用户输入 → IDEA 加密 → RC6 加密 → 与硬编码比较
5. **加密算法**：
   - IDEA（International Data Encryption Algorithm）128-bit key, 64-bit block
   - RC6（Rivest Cipher 6）可变 key/block

## 关键技术点
- 非 x86 架构逆向（PowerPC abiv2）
- IDEA 加密算法识别（128-bit key）
- RC6 加密算法识别
- radare2 跨平台反汇编
- 双重加密还原：先 RC6 解再 IDEA 解

## 评分
- quality: high（架构识别 + 工具使用 + 算法识别完整，附图清晰）
