---
title: 2024 第四届"网鼎杯"白虎组 writeup（GTP TEID + AES-ECB + SPN 仿射）
contest: 2024 第四届网鼎杯
year: 2024
difficulty: hard
vuln_type: [block_cipher, lattice, ssrf, crypto_rsa, ssti, web_unknown]
tags: [白虎 misc01 GTP TEID 统计排序, tshark gtp.teid, tshark e GTP 流, misc02 AES-ECB TEID 当 key, misc03 php filter 侧信道, misc04 三个文件合并 zip 伪加密, CRYPTO01 SPN P(x) 仿射变换, S 看作 chips 线性变换, 对 S 求 LLL 还原 keys, flag 头 wdflag{ 爆破 1 字节]
attack_chain:
  - misc01: tshark -r UPF.cap -e "gtp.teid" 统计排序两处异常 TEID 拼接
  - misc02: TEID 作 AES-ECB key 解密加密流量
  - misc03: php filter convert.quoted-printable-encode 3000 次侧信道 (DownUnderCTF 2022 minimal-php 同款)
  - misc04: cat 1 2 3 > 1.zip binwalk 看 2.png 伪加密 + !@#QQQ0010flag**** 掩码爆破
  - CRYPTO01: P(x) = P*x, S(x) = A*x + b，T = P^{-1}AP, U = P^{-1}b
  - r = T^{14} x + (T^{13}+...+I) U + (T^{13}+...+I) P^{-1} k
  - flag 头 "wdflag{" 7 字符，爆破 1 字节解方程组，得 keys 列表
  - chips 只有 1 和 -1 → 对 S 求 LLL
key_payload: "S = chips 线性变换；S = LLL(chips) 还原 keys"
one_liner: 白虎组四题：GTP TEID 统计 + AES-ECB + php filter 侧信道 + zip 伪加密 + SPN 仿射 LLL 还原 keys。
lesson: GTP 协议 TEID 是 5G 核心网隧道标识，tshark -e gtp.teid 提取；SPN 密码里 S 看作 chips 线性变换（chips ∈ {1,-1}）时，直接对 S 求 LLL 即可还原 key 比特。
quality: high
---

# 2024 第四届"网鼎杯"白虎组

## Misc 01-04

### misc01: GTP TEID 流量分析
```bash
tshark -r UPF.cap -e "gtp.teid" -T fields | sed '/^\s*$/d' > upf.txt
```
统计排序 TEID 找两处异常报文 → 拼接得 `wdflag{18xxx23xxx}`。

### misc02: AES-ECB TEID 作 key
观察 GTP 协议后续数据是加密的 AES-ECB 流量，**TEID 直接当 key** 解密请求/响应包。

### misc03: PHP filter 侧信道
参考 DownUnderCTF 2022 minimal-php：
```python
blow_up_enc = join(*['convert.quoted-printable-encode'] * 3000)
req(f'convert.base64-encode|convert.iconv..CSISO2022KR|convert.base64-encode|{blow_up_enc}|{trailer}')
```
tshark 提取 value 和状态码，替换原脚本请求。

### misc04: 三文件合并 + zip 伪加密
```bash
cat 1 2 3 > 1.zip
binwalk 1.zip  # 看到两个压缩包
```
- `2.png` 伪加密，去掉伪加密位解压得后一半 flag  
- 另一压缩包用 `!@#QQQ0010flag****` 掩码爆破后 4 位数字 → jpg  
- 分离出 png，爆破宽高 → 前一半 flag

## CRYPTO01：SPN 仿射 + LLL 还原 keys

```python
# SPN: P(x) = P * x, S(x) = A * x + b
# T = P^{-1} * A * P, U = P^{-1} * b
# r = T^{14} x + (T^{13} + ... + I) U + (T^{13} + ... + I) P^{-1} k
# flag 头 "wdflag{" 7 字符，爆破 1 字节解方程组
# S 看作 chips 线性变换，chips ∈ {1, -1} → 对 S 求 LLL
```

核心思想：S 函数可以用 chips（仅 ±1）表示时，整个加密是线性 + 仿射。  
对 chips 矩阵求 LLL 即可还原 key 比特，遍历 keys 解出 flag。
