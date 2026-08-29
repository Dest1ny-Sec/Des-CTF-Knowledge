---
title: MISC｜西湖论剑 2022 官方 Write Up
contest: 西湖论剑
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [Volatility, VirtualBox VRAM, Rabin 密码, npbk 模拟器, Skred 聊天, Kylin Update Manager, mp3stego, jjencode, 已知明文]
attack_chain: |
  1. (一) Isolated Machine Memory Analysis: ELF core dump (VirtualBox 生成的虚拟机 core) + VRAM 还原桌面 + 聊天窗口 (Python IDLE 加密 flag 方式 + RSA) + 剪贴板 RSA 公钥
     - 512-bit N → factordb 分解 → P/Q
     - E=2 不是 RSA，是 Rabin 密码 → 写 Rabin 解密脚本得 4 个明文 (1 个是 flag)
  2. (二) 机你太美: 夜神模拟器 npbk 文件 + rm /data/system/locksettings.db 绕开机密码 + Skred 聊天工具 + 隐写
     - 1.png alpha 通道 251=0 / 255=1 → 转二进制 → cyberchef → 拿到 XOR key
     - 用 XOR key 异或补发的内容 → flag
  3. (三) KP-Basic: Kylin 系统 ping 工具 + 命令注入 → CNVD-2022-78421 Kylin-Update-Manager 漏洞 + dbus 提权 → fakeadmin:Bb123*** 登录 → sudo su → glzjin + vncserver
     - 文件保险箱 rockyou.txt 爆破 → "maganda" → flag
  4. (四) mp3: mp3 文件尾藏 png + png 二值化 0/255 转 0/1 bit + Python struct.pack → flag.zip
     - mp3stego 空密码解密 → 8750d5109208213f → 解压 flag.zip → 47.txt
     - 47.txt 是 jjencode 变种 (用 'a' 替换 '$') → 浏览器控制台跑出 DASCTF{f8097257d699d7fdba7e97a15c4f94b4}
  5. (五) take_the_zip_easy: 加密 zip 包含另一个 zip → 已知明文攻击 (bkcrack)
     - dasflow.zip 偏移 30 字节处是 dasflow.pcapng → 用 pcapng 作为明文 → bkcrack 爆破
key_payload: |
  # (一) Rabin 密码解密 (E=2, P, Q 已知):
  c = flag_enc
  r = pow(c, (P+1)//4, P)
  s = pow(c, (Q+1)//4, Q)
  # CRT 拼 4 个解
  # yP = P * pow(P, -1, Q) % N
  # yQ = Q * pow(Q, -1, P) % N
  m1 = (r*yP + s*yQ) % N
  m2 = (r*yP - s*yQ) % N
  m3 = (-r*yP + s*yQ) % N
  m4 = (N - m1) % N
  
  # (二) 1.png alpha 转二进制:
  from PIL import Image
  img = Image.open('1.png')
  flag = ''
  for x in range(img.size[0]):
      for y in range(img.size[1]):
          r, g, b, alpha = img.getpixel((x, y))
          if x == 400:
              if alpha == 251: flag += '0'
              elif alpha == 255: flag += '1'
  # cyberchef 转 binary → key
  
  # (四) mp3stego + jjencode:
  # Decode.exe -X -P "" flag.mp3
  # 8750d5109208213f → 解压 → 47.txt (jjencode 变种, 用 'a' 替换 '$')
  # 浏览器控制台运行
one_liner: 西湖论剑 2022 官方 MISC 5 题 (Volatility VRAM + Rabin / npbk 模拟器 + alpha 隐写 / Kylin CNVD-2022-78421 / mp3stego + jjencode / 已知明文 zip 攻击)。
lesson: |
  - VirtualBox ELF core dump 含 VRAM 区域，vol.py strings 搜显存偏移
  - E=2 是 Rabin 密码，不是 RSA (解 4 个明文)
  - 夜神模拟器 npbk 文件 + rm locksettings.db 绕密码
  - PIL alpha 通道 (251/255) 转 0/1 bit
  - mp3stego 空密码仍可解密
  - jjencode 变种: 字符 '$' 换成 'a' 也用同样原理
  - 加密 zip 套加密 zip 时用 bkcrack 已知明文攻击
quality: high
---

# MISC｜西湖论剑 2022 官方 Write Up

> 来源: ctfiot.com 96709

## 比赛概况

2023-02-02 第六届西湖论剑网络安全技能大赛初赛：306 所高校、485 支战队、2733 人参赛。

## （一）Isolated Machine Memory Analysis

- **Volatility 基础分析**：发现 `mstsc.exe` 进程（远程连接）
- **VirtualBox ELF core dump**：含 VRAM 等额外信息
- **VRAM 还原**：4 字节为一单位，估算分辨率 → 还原桌面（含远程连接窗口 + Python IDLE + 聊天窗口）
- **剪贴板取证**：拿到 RSA 公钥
- **512-bit N + E=2** → 实际是 **Rabin 密码**（不是 RSA）
  - factordb 查 P/Q → 写 Rabin 解密 → 4 个明文中 1 个是 flag

## （二）机你太美

- 夜神模拟器 npbk 文件
- `adb shell rm /data/system/locksettings.db` 绕开机密码
- Skred 聊天工具
- 1.png alpha 通道隐写：
  ```python
  from PIL import Image
  img = Image.open('1.png')
  flag = ''
  for x in range(img.size[0]):
      for y in range(img.size[1]):
          r, g, b, alpha = img.getpixel((x, y))
          if x == 400:
              if alpha == 251: flag += '0'
              elif alpha == 255: flag += '1'
  # cyberchef → XOR key
  ```
- XOR 解密聊天补发内容 → flag

## （三）KP-Basic

- Kylin 系统的 ping 工具
- 抓包 + 命令注入 → 反弹 Shell
- **CNVD-2022-78421** Kylin-Update-Manager 漏洞 + dbus 提权
- `fakeadmin:Bb123***` 登录 → `sudo su` → `glzjin` 用户 + `vncserver`
- 文件保险箱 `rockyou.txt` 爆破 → `maganda` → flag

## （四）mp3

1. mp3 文件尾藏 png
2. PNG 二值化 0/255 → 0/1 bit
3. `struct.pack` 拼成 flag.zip
4. `mp3stego -X -P "" flag.mp3` 空密码解密 → `8750d5109208213f`
5. 解压 → 47.txt
6. **jjencode 变种**：把 `$` 换成 `a`，浏览器控制台运行 → `DASCTF{f8097257d699d7fdba7e97a15c4f94b4}`

## （五）take_the_zip_easy

加密 zip 内含另一个 zip → 已知明文攻击：
- `dasflow.zip` 偏移 30 字节处是 `dasflow.pcapng`（已知文件名）
- 用 `bkcrack` 把 `pcapng` 当明文 → 恢复 `dasflow.zip` 加密 key

## 评价

西湖论剑 2022 官方 MISC 5 题，亮点是：
- **VirtualBox ELF core dump + VRAM 还原**（国内首次出现 VRAM 取证）
- **E=2 Rabin 密码**（不是 RSA，常被误判）
- **mp3stego + jjencode 变种**
- **加密 zip 套加密 zip 已知明文攻击**

适用读者：内存取证研究员 / MISC 杂项老手 / 移动安全工程师
