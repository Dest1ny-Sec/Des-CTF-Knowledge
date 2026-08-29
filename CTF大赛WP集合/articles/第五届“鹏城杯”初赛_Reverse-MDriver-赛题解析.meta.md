---
title: 第五届"鹏城杯"初赛 Reverse-MDriver-赛题解析
contest: 鹏城杯
year: 2025
difficulty: hard
vuln_type: reverse
tags: [Windows驱动,WFP,FWPS_CLASSIFY,MSR,KiSystemCall64,KUSER_SHARED_DATA,ICMP,RC4-XOR]
attack_chain: 1. 识别ClassifyFn为WFP callout驱动函数→rdmsr C0000082获取MSR_LSTAR=fffff801`0c211900→KiSystemCall64前4字节0f 01 f8 65作key1(4字节循环)|2. 读取KUSER_SHARED_DATA.NtSystemRoot="C:\WINDOWS" UTF-16LE 20字节→v4[i]^=(~i)&0xFF 256次异或生成key2|3. 密文v41 20字节cipher=payload[i]=cipher[i]^key2[i]^key1[i%4]|4. 触发: Python socket SOCK_RAW IPPROTO_ICMP发包payload=go_to_find_the_flag!→驱动ICMP包匹配触发
key_payload: msr[c0000082] = fffff801`0c211900|0f 01 f8 65(key1)|seed_str="C:\WINDOWS" seed_bytes=seed_str.encode('utf-16le')[:0x14]|v4[i] ^= (~i) & 0xFF for i in range(256)|cipher=[0xD4,0x90,0x60,0xED,...]|key2=[0xBC,0xFE,0xC7,0xFC,...]|p=c^k2^k1|socket.SOCK_RAW socket.IPPROTO_ICMP|flag{Y0r_Ar3_W1nKern3l_Mas7er!*}
one_liner: 鹏城杯2025 WFP callout驱动逆向,ClassifyFn识别WFP过滤ICMP,MSR_LSTAR读KiSystemCall64前4字节作Key1,KUSER_SHARED_DATA.NtSystemRoot="C:\WINDOWS" UTF-16LE异或(~i)生成Key2,密文双key异或解flag,Python SOCK_RAW发ICMP包触发驱动
lesson: 1) WFP驱动ClassifyFn签名识别:(const FWPS_INCOMING_VALUES0*, const FWPS_INCOMING_METADATA_VALUES0*, void*, const void*, const FWPS_FILTER1*, UINT64, FWPS_CLASSIFY_OUT0*); 2) MSR C0000082(MSR_LSTAR)读KiSystemCall64前4字节作为密码key1; 3) KUSER_SHARED_DATA.NtSystemRoot(0x30偏移)固定存系统目录"C:\WINDOWS" UTF-16LE格式,加密key素材; 4) Python socket SOCK_RAW IPPROTO_ICMP直接发ICMP包触发驱动callout; 5) 驱动级逆向思路:从filter/classify函数入手定位算法,MSR+共享数据是常见数据源
quality: high
---

## 备注

原文(https://www.ctfiot.com/291134.html)2026年1月发布,作者看雪ID:relost。Windows驱动逆向+密码学融合题。

### 题目详情

**驱动分析** — WFP(Windows Filtering Platform)callout驱动
- 入口函数`ClassifyFn`签名匹配WFP v1 callout
- 在IDA中a6被识别为`_DWORD*`(实际是UINT64 flowContext)
- 函数功能:对ICMP包进行过滤匹配

**Key1获取** — MSR寄存器
- `rdmsr C0000082`读取MSR_LSTAR(Long System Target Address Register)
- 指向`KiSystemCall64`函数入口
- 入口前4字节:`0f 01 f8 65`(swapgs指令的机器码)
- Key1=[0x0F, 0x01, 0xF8, 0x65] 循环使用

**Key2生成** — KUSER_SHARED_DATA
- KUSER_SHARED_DATA位于0xFFFFF78000000000
- 0x30偏移处为NtSystemRoot(系统目录,固定"C:\WINDOWS")
- seed_str="C:\WINDOWS" UTF-16LE 编码(seed_bytes[:0x20])
- v4=bytearray(256)初始化,前20字节填seed_bytes
- `for i in range(256): v4[i] ^= (~i) & 0xFF`异或处理
- Key2取v4前20字节:[0xBC, 0xFE, 0xC7, 0xFC, 0xA7, 0xFA, 0xAE, 0xF8, 0xBE, 0xF6, 0xBB, 0xF4, 0xB7, 0xF2, 0xBE, 0xF0, 0xB8, 0xEE, 0xBE, 0xEC]

**密文解密**
- cipher 20字节:[0xD4, 0x90, 0x60, 0xED, 0xC7, 0xA4, 0x30, 0xF4, 0xDF, 0x93, 0x1C, 0xE5, 0xD0, 0x96, 0x19, 0xF3, 0xDB, 0x8E, 0x21, 0xA8]
- 解密:p = c ^ k2 ^ k1
- 结果:`go_to_find_the_flag!`

**触发EXP**
- Python socket SOCK_RAW IPPROTO_ICMP
- ICMP type=8 (echo request), code=0
- payload=`go_to_find_the_flag!`
- checksum计算(标准IP checksum)
- 发往127.0.0.1驱动触发

**Flag**
- `flag{Y0r_Ar3_W1nKern3l_Mas7er!*}`

## 评级

- **quality: high** — 完整驱动逆向+MSR+共享数据双key异或密码学链,Python socket发包exp齐全,作者是看雪relost(高质WP)
- **vuln_type: reverse** — 驱动逆向+密码学
- 实战价值:Windows驱动callout逆向是内核安全高阶技术,MSR_LSTAR+KUSER_SHARED_DATA是常见攻击面
