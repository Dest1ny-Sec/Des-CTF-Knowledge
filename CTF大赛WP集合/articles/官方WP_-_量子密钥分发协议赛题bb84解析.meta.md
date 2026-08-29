---
title: 量子密钥分发协议赛题bb84官方WP - 第十六届信安国赛
contest: 第十六届全国大学生信息安全竞赛(信安国赛)初赛 + 伽玛实验场
year: 2023
difficulty: hard
vuln_type: crypto_rsa
tags: [量子密钥分发, BB84协议, 偏振编码, 一次一密, 流密码, 异或, UTF-8, 线性同余, 安徽问天量子, 香农熵, 误码率, 100%纠错, EPC1-APD]
attack_chain: 读csv获Alice随机序列EPC1+Bob探测器APD1-APD4 → 有效探测(APD仅1个为1) → 对基成功(EPC1=1/2→APD1/2为1;EPC1=3/4→APD3/4为1) → 误码筛(EPC1=1∧APD2=1等) → 误码率计算 → 100%纠错假设 → 线性同余(A=1709,B=2003,M=keyPool.length,indexBegin=17)索引取安全密钥 → 异或解密hex密文 → UTF-8编码得明文
key_payload: BB84偏振协议 + 100%纠错 + 一次一密 + 流密码异或 + 线性同余(A=1709,B=2003)
one_liner: 安徽问天量子设计信安国赛BB84量子密钥分发赛题:偏振对基+误码筛+线性同余取密钥+流密码异或。
lesson: BB84协议:4种偏振态(0°/45°/90°/135°=H/V/±/+),Alice随机选基+随机比特,选错基时误码;有效探测=仅1个APD响应;对基成功条件:EPC1=1/2用APD1/2,EPC1=3/4用APD3/4;100%纠错假设简化算法;一次一密=密钥长度=明文长度;流密码=异或;线性同余公式res=(A*index+B) % M;UTF-8编码最终明文。
quality: high
---
