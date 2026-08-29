---
title: CCB 决赛有感 (附 RE/AI 题目附件)
contest: CCB
year: 2026
difficulty: medium
vuln_type: web_unknown
tags: [实网渗透, schema.sql, 文件上传改后缀PHP, find -perm -4000 提权, fscan扫描, DokiLogic Renpy rpyc, unrpyc解密, 1.exe XOR 35, app.java邮件网关]
attack_chain:
  - 实网渗透: 扫目录 → schema.sql → 账号密码 → 后台文件上传 → 改后缀 PHP
  - 上线 supershell → find SUID 提权
  - /usr/bin/find . -exec /bin/bash -p ; -quit
  - fscan 扫到 app.java + protokms 邮件网关 → 触及盲区
  - DokiLogic: Renpy 游戏, script.rpyc → unrpyc 解
  - 主程序释放 1.exe, 捕获其输出
  - 输入字符串 XOR 35 与 exe 输出比较
  - flag = 1.exe 输出 XOR 35
key_payload: 'schema.sql / 后台 PHP 改后缀 / find SUID 提权 / unrpyc / 1.exe XOR 35 / protokms 邮件网关'
one_liner: CCB 决赛有感 — 实网渗透 schema.sql + 后台 PHP 改后缀 + find SUID 提权 + DokiLogic Renpy 1.exe XOR 35 还原 flag。
lesson: 实网渗透 4 步曲:目录扫 → 凭据/源码 → 上传 RCE → SUID 提权;Renpy .rpyc 必用 unrpyc 解;1.exe 硬编码可在 rpy 中提取后 python 调执行再 XOR。
quality: medium
---

# CCB 决赛有感 (附 RE/AI 题目附件)

## 速读
CCB 决赛复盘 — 实网渗透 + RE DokiLogic 复现。

## 实网渗透
1. 扫目录 → 找到 `schema.sql`
2. 找到账号密码
3. 后台文件上传点 → 抓包改后缀为 .php
4. 上线 supershell
5. `find / -perm -4000 -type f -exec ls -la {} 2>/dev/null` 找 SUID
6. `/usr/bin/find . -exec /bin/bash -p ; -quit` 提权
7. fscan 扫到 app.java + protokms (邮件网关软件)
8. 触及盲区, 潦草退场

## DokiLogic (RE)
- Renpy 游戏, 输入 answer
- 找到 `script.rpyc` → unrpyc 解 (https://github.com/CensoredUsername/unrpyc)
- 主程序释放 1.exe, 捕获其输出
- 输入字符串每字符 XOR 35, 与 exe 输出比较
- flag = exe 输出 XOR 35

## EXP
```python
import subprocess
import os

_f = b'MZ\x90\x00...'  # rpy 里的 _f (1.exe 硬编码)

with open('temp.exe', 'wb') as f:
    f.write(_f)

output = subprocess.run('temp.exe', stdout=subprocess.PIPE).stdout.decode('latin-1')
os.remove('temp.exe')

flag_input = "".join(chr(ord(c) ^ 35) for c in output)
print(f'flag{{{flag_input}}}')
```
