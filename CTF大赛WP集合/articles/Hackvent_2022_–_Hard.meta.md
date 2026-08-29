---
title: Hackvent 2022 Hard 全套
contest: Hackvent 2022
year: 2022
difficulty: hard
vuln_type: [reverse, stego_image, block_cipher, pwn_unknown]
tags: [ADCP, base64, haystack, QR, pyzbar, zip2john, hashcat, AES-ECB, bytewise, heap-exploit, UAF]
attack_chain: ["解析 ADCP 频谱找 base64 flag", "切 24800x24800 PNG 网格 pyzbar 扫 QR", "PBKDF2-HMAC zip 碰撞爆破前缀密码", "AES-ECB 字节翻转 oracle 解 flag", "UAF + heap 控制写 present 指针"]
key_payload: "HV22{v-wish-v-g0t-b33r} / HV22{1'm_y0ur_need13.} / HV22{HAVING_FUN_WITH_CHOSEN_PREFIX_PBKDF2_HMAC_COLLISIONS_nzvwuj} / HV22{len()!=len()} / NOPELOS (ASCII art flag)"
one_liner: 五题 Hard 覆盖频谱/图像/密码/AES/pwn
lesson: PBKDF2-HMAC 已知末段可前缀爆破；AES-ECB 配合可控前缀可逐字节 oracle；UAF 后用未清空指针覆盖堆块写任意地址
quality: high
---

# Hackvent 2022 Hard 五题

原文 https://www.ctfiot.com/89723.html

## 1. 频谱隐藏 base64 (Day 16 - HV22{v-wish-v-g0t-b33r})
`message_1msps.cu8` 是 RDI ADCP 声学多普勒流速剖面仪原始格式，字节值集中在 127/128 附近，落在 0xFF 一带的少数字节拼出 `SFYyMnt2LXdpc2gtdi1nMHQtYjMzcn0=`，base64 解码即 flag。

## 2. 大图扫 QR (HV22{1'm_y0ur_need13.})
24800x24800 单色 PNG，绝大多数 QR 是 "Sorry, no flag here!"，少数藏 flag。脚本按 [25, 2, 2, 2, 2, 2] 分块递归裁切，pyzbar 扫每块，~1 分钟扫 85 万子图。

## 3. 已知后缀 PBKDF2 zip 密码碰撞
`SantasSleigh.raw` 字符集 {0,1,2,3}，去重出 `69792b677e3e4c7a6d78545c205c4e5e26` 视为 zip 密码尾部，zip2john + john mask `?A?A?Aiy+g~>LzmxT\ \N^&` 4 秒出 3 字符前缀 `4Lt`；`7z x` 解出 `HV22{HAVING_FUN_WITH_CHOSEN_PREFIX_PBKDF2_HMAC_COLLISIONS_nzvwuj}`。

## 4. AES-ECB 字节 oracle (HV22{len()!=len()})
服务：`input + flag` 拼 16 字节对齐 → AES-ECB 加密。利用 `§` 是 2 字节 UTF-8，控制 16 字节边界位置使 flag 字节落到独立 block，逐字节比对相同前缀 oracle 出 flag。

## 5. heap UAF pwn (NOPELOS)
ELF 64 菜单：看 naughty list / 看 workshop / 偷 present / good deed。
- 选项 1 输入负索引 → 越界读 `present` 指针泄露 PIE
- 选项 3 free workshop
- 选项 4 good deed 写入 48 字节，前 40 字节姓名 + 后 8 字节堆指针 → UAF 重新占位 freed chunk
- 选项 2 触发 `present()` 跳到 `system("sh")` → 读 FLAG

## 质量评估
- ADCP 数据隐写少见、教学价值高
- 大图扫 QR 是经典分治思想
- PBKDF2 已知尾部前缀爆破可作为密码学碰撞范式
- AES-ECB 字节翻转 oracle 教科书级
- pwn 全套 UAF 利用链清晰
