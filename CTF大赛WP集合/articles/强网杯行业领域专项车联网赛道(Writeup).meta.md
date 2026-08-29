---
title: 强网杯行业领域专项车联网赛道 WriteUp - AES-CPA侧信道+VIN_RC4+CAN数据
contest: 强网杯行业领域专项车联网赛道
year: 2024
difficulty: hard
vuln_type: crypto_rsa
tags: [CPA侧信道, AES-128, TRS文件, 功耗分析, First_round_SubBytes, Hamming_Weight, 相关性, RC4_变种, VIN_加密, KSA+3, CAN总线, signal_map, can_id, 字节频率, Z1X3Y4E5Z8V2A6H6, 7AF2C74EAD5C2D4505E94B820275CA8C52]
attack_chain: AES侧信道:TRS文件解析ntraces/nsamples/dlen=32(16B PT+16B CT) → 标准化traces(去均值+单位方差) → CPA循环16字节:猜测0-255,计算SubBytes(p^b)+Hamming_Weight,与trace相关性,选argmax → flag{UPPERCASE_HEX} → VIN_RC4:variantRC4Encrypt(双KSA+反向KSA+3常数+K生成S流+K^k%256) + correctEncrypted=7AF2C74EAD5C2D4505E94B820275CA8C52+key=Z1X3Y4E5Z8V2A6H6 → 密文 ^ K ^ (k%256)得VIN → CAN数据:CAN_LINE_RE解析can0 + signal_map映射+Counter统计每信号最频值
key_payload: AES-128 CPA HW模型 + variantRC4 S流+K^(k%256) + CAN帧最频值
one_liner: 强网杯车联网赛道:AES-CPA侧信道攻击+变种RC4 VIN加密+CAN总线数据最频值提取。
lesson: AES-128 CPA侧信道:TRS文件ntraces/nsamples/dlen=32(16B PT+16B CT) → trace标准化(去均值+单位方差) → 16字节独立猜测+argmax(SubBytes(p^b)+HW与trace相关性);variantRC4:KSA正向+反向+S流生成+ciphertext^K^(k%256)双异或;CAN数据:CSV signal_map(can_id+byte+len)解析CAN帧+Counter统计每信号最频值;KSA常数+3(变种)。
quality: high
---
