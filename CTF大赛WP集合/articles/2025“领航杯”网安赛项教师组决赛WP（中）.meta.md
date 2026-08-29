---
title: 2025"领航杯"网安赛项教师组决赛 WP（中）
contest: 领航杯
year: 2025
difficulty: medium
vuln_type: crypto_rsa
tags: [MT19937, AES-ECB, 状态逆推, Xorshift, 32-bit-twist, 多线程爆破, 公众号引流文]
attack_chain:
  - 拆解 Xorshift32 4 段位移掩码 (>>18/<<15/<<7/>>11)
  - 用 inv_number 还原 update_state 前置 MT-like 状态
  - gen_rand_number 模拟末端正向
  - 多进程分片穷举 S 状态 0..2^32
  - AES-ECB 解密 ciphertext 验证 "CnHongKe" 前缀
key_payload: 'MT19937 逆运算 + multiprocessing 32-bit 状态分片爆破'
one_liner: 公众号风格的两题展示 — Crypto-randError 现场无人解，MT19937 逆推 + AES-ECB 明文前缀爆破；Misc-VC&EZ 提示恶意 docx + 符号链接 + PHP filter 链读 flag。
lesson: 完整 EXP 被作者隐藏成引流钩子；MT19937 状态可逆可爆破前提是 update_state 是仿射的且 y*X 段可枚举。
quality: medium
---

# 2025"领航杯"网安赛项教师组决赛 WP（中）

## 速读
ChaMd5 数字人才创研院公众号风格输出 — 题面+思路点+完整 EXP 隐藏在"关注私信"。

## Crypto-randError
- 现场 0 解；EXP 给出 32-bit 状态 Xorshift/MT 混合生成器
- 通过 inv_number 还原 4 段位移 + gen_rand_number 正向模拟
- multiprocessing.Pool 分片 task_range 暴力 S 候选
- AES-ECB 解密判定明文前缀 "CnHongKe"

## Misc-VC&EZ
- 构造恶意 docx，word/_rels/document.xml.rels 指向 media/php://filter/read=zlib.deflate/resource=flag.txt
- word/media 软链接到 / 触发任意文件读
- 路径用 &#N; HTML 实体编码绕过字符串检测
- ZIP_DEFLATED + ZipInfo(create_system=3, external_attr=0xA1ED0000) 保留 Unix 软链接属性

## 评价
公众号引流文 — EXP 主体藏在 "关注私信" 后，文中只露思路骨架。Crypto 思路完整，Misc EXP 给出可执行 Python 但未提供触发结果。
