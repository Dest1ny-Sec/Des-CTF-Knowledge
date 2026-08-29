---
title: 1337UP LIVE CTF WriteUp
contest: 1337UP LIVE CTF 2023
year: 2023
difficulty: medium
vuln_type: [stego_image, sqli, lfi, web_unknown, misc_unknown, reverse]
tags: [Intigriti, jpg-zip-concat, stegsolve, sha256-crack, X-Forwarded-For, BioCorp, XOR-reversible, wifi-pcap, knight-knight, escargot-esolang]
attack_chain: ["Q1 Sanity Check: 直接看题面 INTIGRITI{1f_y0u_l34v3_7h3_fl46_w1ll_b3_r3v0k3d}", "Q2 In Plain Sight: jpg 尾接 zip（FFD9 + 504B 中间是 zip），解压后 stegsolve 出 flag", "Q3 Socials: Twitter h0p3_y0u + youtube _3nj0y_ + reddit d4_c7f → INTIGRITI{h0p3_y0u_3nj0y_d4_c7f}", "Q4 irrOReversible: 按位或运算 → 传 256 个 x00 还原 → INTIGRITI{b451c_x0r_wh47?}", "Q5 Pizza Paradise: robots.txt → js 登录 sha256 爆破 → 任意文件读", "Q6 BioCorp: PHP $_SERVER 超全局 → X-Forwarded-For / X-Biocorp-VPN 等头变 HTTP_* 访问内部资源", "Q7 Knight: 两层 knight escargot esolang → INTIGRITI{}", "Q8 WIFI: pcap 解 WPA2 → 拿 SSID/密码"]
key_payload: "INTIGRITI{1f_y0u_l34v3_7h3_fl46_w1ll_b3_r3v0k3d}"
one_liner: 1337UP LIVE CTF 8 大题：sanity + stego + XOR + web + bio + wifi + esolang
lesson: jpg 后接 zip 是经典 MISC 套路；XOR 全 0 还原是 reverse 入门；escargot esolang 是字符画
quality: high
---

# 1337UP LIVE CTF WriteUp

原文 https://www.ctfiot.com/216053.html （WgpSec 狼组安全团队）

## WARMUP

### Sanity Check
直接看题面：
```
INTIGRITI{1f_y0u_l34v3_7h3_fl46_w1ll_b3_r3v0k3d}
```

### In Plain Sight
- jpg 尾接 zip（FFD9 + 504B 中间是 zip 文件）
- 手动提取 → 解压 → stegsolve
- 拿 flag

### Socials
- Twitter: `h0p3_y0u`
- YouTube: `_3nj0y_`
- Reddit: `d4_c7f`
- **Total: `INTIGRITI{h0p3_y0u_3nj0y_d4_c7f}`**

### irrOReversible
- 按位或运算
- 直接传 256 个 `\x00` 还原
- hex 转 → `INTIGRITI{b451c_x0r_wh47?}`

## WEB

### Pizza Paradise
- 扫目录 → robots.txt
- js 登录逻辑 → sha256 爆破
- 任意文件读拿 flag

### BioCorp
- PHP `$_SERVER` 超全局
- 请求头加 `HTTP_` 前缀，`-` 变 `_`
- `X-Forwarded-For` → `HTTP_X_FORWARDED_FOR`
- `X-Biocorp-VPN` → `HTTP_X_BIOCORP_VPN`
- 用伪造头访问内部 VPN 资源

## REVERSE
### Knight
- Knight esolang（骑士旅游 / 字符画）
- 两层嵌套解出 `INTIGRITI{}`

## CRYPTO
### XOR
- 异或操作 → 已知 plaintext 还原
- 256 字节 0 是 universal XOR key

## FORENSIC
### WIFI
- pcap 抓 WPA2 握手
- aircrack-ng 跑字典爆破
- 拿 SSID + 密码

## 教学价值
- **jpg 尾接 zip** 是经典 MISC
- **FFD9 + 504B 边界** 是 MISC 入门
- **XOR 0** 还原是 reverse 基础
- **PHP $_SERVER** 头转换规则
- **Knight / Escargot** esolang 是字符画语言
- **WPA2 破解** 是 forensic 入门
- 1337UP 是 Intigriti 漏洞平台办的 CTF

## flag 汇总
- Sanity: `INTIGRITI{1f_y0u_l34v3_7h3_fl46_w1ll_b3_r3v0k3d}`
- Socials: `INTIGRITI{h0p3_y0u_3nj0y_d4_c7f}`
- XOR: `INTIGRITI{b451c_x0r_wh47?}`
