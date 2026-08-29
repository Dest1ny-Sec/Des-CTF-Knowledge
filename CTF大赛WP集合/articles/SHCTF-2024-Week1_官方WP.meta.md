---
title: SHCTF-2024-Week1 官方WP
contest: SHCTF
year: 2024
difficulty: easy
vuln_type: misc_unknown
tags: [shctf2024-week1, rc4-decrypt, rockyou, png-header, zip-pseudoencrypt, ctfiot]
attack_chain:
- 用 RC4 硬编码 key 解 Windows Defender Quarantine 加密 zip
- rockyou 字典爆破解压密码
- 010editor 补全 PNG 头尾 (89 50 4E 47 0D 0A 1A 0A / AE 42 60 82)
- 修改 PNG 高度 07→08 露出 flag 文本
- zip 伪加密改 09 00 为 00 00 解压
- 注释处读取掩码格式密码 (shctf{})
- airpcap-ng / aircrack-ng + 字典爆破 WiFi
- fastcoll 生成同前缀 MD5 碰撞 (MD5 master!)
- ROP gadget pop rdi + plt puts 泄 got
- 一字节覆写 ret_addr 为 backdoor
- int size 负数绕过 strlen / size 检查
- 0x50f syscall 跳过 check 直接执行 shellcode
- chain 5 链式 PHAR 反序列化 system('cat /f*')
- base64 解密 game.js 0x208 后 alert
- /api?SSHCTFF=cmd RCE 调 os.popen
key_payload: 1zflask /api?SSHCTFF=cat /flag
one_liner: 看雪 ctfiot 招新题库，Week1 全是 8 个类别的签到 + 工具题 (RC4/PNG/zip/MD5 碰撞/WiFi/Java/PHP 链)。
lesson: 真实取证场景里 Quarantine 文件结构 + cuckoo-modified RC4 key 是常见 pattern，rockyou 字典对短密码永远先试。
quality: medium
---
# SHCTF-2024-Week1 官方 WP（ctfiot 209352）

## Misc
- **Quarantine**：RC4 硬编码 key 解密 Windows Defender Quarantine zip → base64 解压 → rockyou 字典爆破
- **拜师之旅①**：010editor 补全 PNG 头尾 (8950 4E47 0D0A 1A0A + AE 42 60 82)，改高度 07→08
- **真真假假遮遮掩掩**：zip 伪加密改 09 00 → 00 00；掩码爆破弱口令 (6 位)
- **Rasterizing Traffic**：光栅流量提取 + 曾哥脚本 `Raster-Terminator` 还原图片
- **有 WiFi 干嘛不用呢？**：合并字典后 `aircrack-ng file -w output` 跑密码

## Web
- **poppopop**：5 链 PHAR 反序列化触发 system('cat /f*')
- **jvav**：Runtime.exec 在线 java 执行 `cat /flag`
- **单身十八年的手速**：定位 0x208 → alert base64 解密
- **1zflask**：robots.txt → /s3recttt 拿源码 → `/api?SSHCTFF=cat /flag`
- **MD5 Master**：`fastcoll` 生成前缀 `MD5 master!` 同 MD5 双文件
- **蛐蛐？蛐蛐！**：check.php 弱校验 6 位数 / 114514a / 科学计数法 + 分号截断

## Pwn
- **签个到吧**：`close(1)` 后 `cat /flag >$2` 重定向 fd
- **指令执行器**：0x50f syscall 跳过 check，写 shellcode 末尾 nop 至 0x50f
- **No_stack_overflow1**：插入 0x00 绕过 strlen → 覆盖 ret_addr = backdoor
- **No_stack_overflow2**：int 负数绕过 size check → pop rdi + puts 泄 got → ret2libc
- **No_stack_overflow2_pro**：静态链接 → pop rax(0x3b) + pop rdi + pop rsi + pop rdx + syscall

## Reverse
- **Ezapk**：enc_char = ord(c)//2 - 6; out ^= key[i%len(key)]
- **ezxor**：i%3 分三组异或 0x90/0x21/0x31 → SHCTF{x0r_N1ce_hxxxoorrr!}
- **ezrc4**：FenKey!! + RC4 + ^102 → SHCTF{rc4_nice_ez!!!}
- **EzDBG**：WinDBG 加载 .pdb → enc 异或 0x66 还原
- **gamegame**：在线数独解出答案包裹 shctf{}

## Crypto
- **factor**：yafu 分解 N → 10 个素数选 7 个排列 → 还原
