---
title: CTF学习交流群 第六期writeup大放送
contest: 群赛出题
year: 2017
difficulty: medium
vuln_type: web_unknown
tags: [misc, etl, smb, NTLM, hashcat, reverse, life_or_flag, 群活动]
attack_chain:
  - etl2pcapng转换netsh trace为pcap
  - wireshark看SMB抓flag.zip多次重传
  - 提取Net-NTLM hash format username::domain:challenge:HMAC-MD5:blob
  - hashcat -m 5600爆破administrator密码为flag
  - life_or_flag: 20字符flag读入后deal()分支运算+4字节线性方程组
key_payload: hashcat64 -m 5600 administrator:::8b1ca28f...:1c4d7b10...:010100... flag.txt
one_liner: 群第6期三题，etl+SMB Net-NTLM爆破+逆向flag约束方程
lesson: Net-NTLM从SMB包中提取后hashcat秒破
quality: high
---

# CTF学习交流群 第六期writeup大放送

## 题目信息
- 群号 473831530（已关闭入群）
- 出题人：札克利（BrainOverFlow）、七友（etl）、Processor（life_or_flag）
- 工具：etl2pcapng / wireshark / hashcat

## 关键攻击链
1. **BrainOverFlow（misc）**：仅给 B 站视频链接 wp，无文字
2. **etl 流量分析**：
   - `etl2pcapng.exe ctf.etl ctf.pcap` 转格式
   - wireshark 看 SMB 协议，多次复制 flag.zip
   - 提取 Net-NTLM hash：`administrator:::8b1ca28f73d4de6b:1c4d7b101dabb5d9efccce3d6f9d9075:0101000000000000c6a7b132...`
   - `hashcat64 -m 5600 ... flag.txt` < 1 秒爆破
3. **life_or_flag（reverse）**：
   - 读 20 字符 flag，400AAC 算 MD5 放 V6
   - 402358 + 4024DD 两 check
   - `flag_encode=[204,110,95,51,61,47,118,57,87,50,115,228,86,47,49,37,25,118,31,123]`
   - `deal(a)`: a&3 分别 -2/(a*2)&0xff/a/2/(a+2)
   - 4 字节线性方程组 9v3+6v2+3v4+8v5=1281 等 4 个

## 评分
- quality: high（etl+pcap+NTLM 链路完整，life_or_flag 给出完整求解脚本）
