---
title: HECTF-2023 WriteUp
contest: HECTF 2023
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [osint, ntlm, baidu-pan, 拼图, dou-di-zhu, bilibili, gif, 视频]
attack_chain:
  - 第1关: Welcome HECTF{Welcome_To_HECTF_2023}
  - Osint: 河北省邯郸市永年区永年太极广场
  - 牌型密码: 黑桃s 红桃h 梅花c 红尖d
  - small joker=kaf, big joker=wi1
  - B站视频: https://www.bilibili.com/video/BV1Lj41187kx/
  - 农民牌得flag: HECTF{Dou_di_Zhu_uhZ_id_uoD_hEccctf_TY6d145A57R7WVz}
  - 百度网盘: 二维码拼图24张
  - flag: HECTF{java_ca_fei_bao_bei}
  - NTLM流量: ntlmssp过滤+NTProofStr提取
key_payload: HECTF{Dou_di_Zhu_uhZ_id_uoD_hEccctf_TY6d145A57R7WVz}
one_liner: HECTF 2023 多关MISC：OSINT+牌型密码+拼图+NTLM
lesson: 综合MISC题常结合OSINT+牌型+拼图+NTLM
quality: high
---

# HECTF-2023 WriteUp

## 题目信息
- 比赛：HECTF 2023
- 类别：MISC + OSINT 综合

## 关键攻击链
### 1. 欢迎
- `HECTF{Welcome_To_HECTF_2023}`

### 2. OSINT
- 答案：`HECTF{河北省邯郸市永年区永年太极广场}`

### 3. 牌型密码
- 黑桃 → s
- 红桃 → h
- 梅花 → c
- 红尖 → d
- small joker → kaf
- big joker → wi1
- B 站视频：https://www.bilibili.com/video/BV1Lj41187kx/
- 农民牌型获得 flag：
  - `HECTF{Dou_di_Zhu_uhZ_id_uoD_hEccctf_TY6d145A57R7WVz}`

### 4. 百度网盘拼图
- 24 张二维码拼图
- 拼出后下载
- `HECTF{java_ca_fei_bao_bei}`

### 5. NTLM 流量
- Wireshark 过滤 `ntlmssp`
- 提取 NTProofStr
- 复制域名 + 用户名 + NTLMv2 响应
- 进一步破解

## 评分
- quality: high（多形式 MISC 综合：OSINT + 牌型 + 拼图 + NTLM）
