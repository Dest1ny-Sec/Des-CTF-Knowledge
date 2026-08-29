---
title: 强网杯青少年专项赛 线上赛 WP
contest: 强网杯青少年
year: 2024
difficulty: medium
vuln_type: misc_unknown
tags: [QR-code-combine, backdoor-user-kill, GIF-multi-frame, multi-encode, AES-CBC, DP-state-count, ret2libc, fgets-overflow, 隼目安全]
attack_chain:
  - MISC 签到漫画: 多页漫画末有二维码拼图 → 桌面 qq 钉 → 解析 → flag{youthful_and_upward}
  - MISC 删除后门用户: backdoor 用户 5 秒复活, kill 父进程 Pid22 → userdel -f backdoor → flag{943f9194-97a1-497f-80ef-0fbe530acfa9}
  - MISC white: GIF 多帧 → flag{passion_is_the_greatest_teacher}
  - Crypto Classics: base32+base64+rot13(回转 23 位)+Atbash+Vigenère(key=GAMELAB) → flag{2834d185-a1da-4fb1-8bac-59076eb6a634}
  - Crypto AliceAES: AES-CBC + 8995bee3173bb5ede17be5cfc58d762c → flag{6e80563b-21b2-4a70-a809-ec0893c18ccb}
  - Crypto easymath: DP 状态计数 + next_prime
  - PWN clock_in: fgets 缓冲区溢出 + ret2libc + puts@plt 泄 libc + system("/bin/sh")
key_payload: 'QR 拼图 + kill 父进程 + GIF 多帧 + base32/64/rot13/Atbash/Vigenère + AES-CBC + DP 计数 + ret2libc'
one_liner: 强网青少年 6+ 题：QR 拼图 + 后门用户删除 + GIF + 5 重编码 + AES-CBC + DP 计数 + ret2libc。
lesson: 强网青少年题覆盖 Misc 多技能 + Crypto 多重编码 + PWN 基础栈溢出；适合青少年入门。
quality: high
---

# 强网杯青少年专项赛 线上赛 WP

**来源**: ctfiot.com ID 217894
**主办**: 隼目安全

## MISC

### 签到漫画
- 多页漫画末有二维码拼图
- 用 qq 钉在桌面
- 解析二维码: `http://weixin.qq.com/r/4BIrMz7ES2M0rXpQ90fy?flag{youthful_and_upward}`
- flag: `flag{youthful_and_upward}`

### 删除后门用户 2
- 容器中读取 /etc/passwd
- 发现 backdoor:x:0:1000::/home/backdoor:/sbin/nologin
- backdoor 用户每 5 秒复活
- 找父进程 Pid 22 sleep 5
- userdel -f backdoor
- flag: `flag{943f9194-97a1-497f-80ef-0fbe530acfa9}`

### white
- 010 打开, GIF 头
- 改后缀名, 第二帧 flag
- flag: `flag{passion_is_the_greatest_teacher}`

## Crypto

### Classics
- 5 重编码: base32 + base64 + rot13(回转 3 位, 解密回转 23 位) + Atbash + Vigenère(key=GAMELAB)
- flag: `flag{2834d185-a1da-4fb1-8bac-59076eb6a634}`

### AliceAES
- AES-CBC 加密, hex 输出
- 计算 key + iv + 加密 = `8995bee3173bb5ede17be5cfc58d762c`
- flag: `flag{6e80563b-21b2-4a70-a809-ec0893c18ccb}`

### easymath
- DP 状态计数: `dp[i][state]` = 长度为 i 状态为 state 的序列数
- 跳过 0b1111 和 0b0000 状态
- 计算有效序列数 key = count_valid_sequences(2331)
- p = next_prime(key)
- flag: `flag{77310934-21fa-4ee4-a783-dc1865ebab28}`

## PWN

### clock_in
- fgets 缓冲区溢出
- ret2libc
- puts@plt 泄 libc
- system("/bin/sh")
- payload: `cyclic(72) + pop_rdi + puts_got + puts_plt + 0x401090`

## 评价
强网杯青少年专项赛 6+ 题：
- Misc: QR 拼图 + 父进程查找 + GIF 多帧
- Crypto: 多重编码 + AES-CBC + DP 计数
- PWN: 基础栈溢出 + ret2libc

是青少年入门 CTF 的好材料。
