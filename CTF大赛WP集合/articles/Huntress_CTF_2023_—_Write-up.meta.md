---
title: Huntress CTF 2023 Write-up
contest: Huntress CTF
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [Misc, Forensics, RE, Web, OSINT, 多题合集]
attack_chain: |
  1. Tecuha.exe -pwinfected hot_off_the_press.uha → UHA 解包
  2. Splunk_TA_windows/bin/powershell/nt6-health.ps1 Basic Auth YmFja2Rvb3I6dXNlX3RoaXNfdG9fYXV0aGVudGljYXRlX3dpdGhfdGhlX2RlcGxveWVkX2h0dHBfc2VydmVy
  3. firepwd/firepwd.py -d home/challenge/.mozilla/firefox/bc1m1zlr.default-release/ 读 Firefox 密码库
  4. oledump.py -s a -v word/vbaProject.bin 提取 VBA 宏 (Pears/Strawberries/Almonds/Nuts/Bears/Tragedy + AutoOpen)
  5. Nuts(obf_str) 函数 Pears(b)=Chr(b-17) + Strawberries(s)=Left(s,3) + Almonds(s)=Right(s,Len(s)-3) 拼字符串 → GetObject().Get().Create Water, Tea, Coffee, Napkin
  6. wmie MSAcpi_ThermalZoneTemperature + Resolve-DnsName eventlog.zip TXT → 沙箱检测 + DNS TXT 外带 base64
  7. wget --user=opendir --password=opendir --recursive 目录遍历 + curl -L max-redirs 80 重定向链 awk grep sed
  8. file welcome/.hidden/welcomeToThePark Mach-O 64-bit arm64 + strings ADATA_128GB.lnk -e l 提取 cmd.exe 链
  9. vol3 -f image/image.bin windows.hashdump.Hashdump + impacket-secretsdump LOCAL -ntds ntds.dit -system SYSTEM → 抓 NTLM hash
 10. Bliss_Windows_XP.png ^ Bliss_Windows_XP.encry.png 字节 XOR + Decryptor.DecryptorUtil AESDecryptFile SHA256 链
key_payload: |
  flag{...}    # 各题单独 flag
one_liner: Huntress CTF 2023 多题大杂烩，UHA 压缩包 / Splunk / Firefox 密码 / VBA 宏 / WMI 沙箱检测 / DNS TXT / 文件 XOR 经典套路都有。
lesson: Misc 题考的不是新漏洞，是对常见工具链 (oletools / volatility / impacket / firepwd) 的熟练度；UHA 压缩包 + wmie 沙箱检测 + Resolve-DnsName TXT 记录外带是 Huntress 历年高频考点。
quality: medium
---

# Huntress CTF 2023 Write-up

> 来源: ctfiot.com 147388

## 题型速览

文章是把 Huntress CTF 2023 多道题的核心 payload 拼起来，没有完整复现但每个点都给到 cheat-sheet 程度：

| 类型 | 题目 | 关键点 |
|------|------|------|
| Misc/ZIP | Tecuha.exe + UHA 解包 | gz+b64 拼起来的自定义压缩格式 |
| Misc/Web | Splunk PowerShell Basic Auth | `Authorization: Basic YmFja2Rvb3I6...` |
| Misc/Web | opendir FTP 弱密码 | `--user=opendir --password=opendir --recursive` |
| Misc/Password | firepwd Firefox 密码库 | NSS 解 master password |
| RE/VBA | 文档宏 Nuts() 函数 | `Chr(b-17)` 偏移 + `Left/Right` 切分 + 循环 |
| Misc/Windows | WMI 沙箱检测 | `MSAcpi_ThermalZoneTemperature` + `Resolve-DnsName TXT` |
| Misc/RE | Mach-O arm64 二进制 | `file` 判架构 + `strings .lnk -e l` |
| Forensics | NTDS + SYSTEM 离线 | vol3 hashdump + impacket-secretsdump |
| Crypto/Image | Bliss_Windows_XP.png XOR | 已知原图做 key 流 |

## 评价

把 Huntress 这类"考熟练度"的 CTF 套路都过了一遍：UHA 解包、Splunk 凭证、oletools、Firefox 密码、Volume Shadow Copy 的 NTDS 提取、纯图像 XOR。

内容偏 payload 速查风格，缺独立完整复现链路；很多代码片段只有核心几行（`Attribute VB_Name`、`MSAcpi_ThermalZoneTemperature` 等），但堆得够多，作为备考 cheat sheet 有用。
