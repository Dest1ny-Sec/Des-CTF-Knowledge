---
title: FE-CTF 2022: Cyber Demon – Hug Me, Squeeze Me
contest: FE-CTF 2022
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [pwn, lzma, sqz, libsqz.so, elf-section, fetch-verbose, 彩蛋]
attack_chain:
  - SECTIONS有._STRIP_ELF_BEFORE_CTF_ = 0x1337 彩蛋符号
  - 运行./words.elf (LD_LIBRARY_PATH)
  - 交互: Count/Unique/Ignore case/Verbose/Links/Words/Fetch
  - Fetch https://www.google.com 被Killed（OOM）
  - 改 libsqz.so → touch libsqz.c → gcc -shared 创建空库
  - Fetch https://neverssl.com 不Killed
  - libsqz是 LZMA 压缩库
key_payload: _STRIP_ELF_BEFORE_CTF_ = 0x1337  # ELF彩蛋
one_liner: FE-CTF Hug Me Squeeze Me：ELF彩蛋+libsqz.so LZMA压缩+OOM Kill
lesson: 替换 libsqz.so 为空库可绕过OOM Kill
quality: medium
---

# FE-CTF 2022: Cyber Demon – Hug Me, Squeeze Me

## 题目信息
- 比赛：FE-CTF 2022
- 题目：Cyber Demon – Hug Me, Squeeze Me
- 类型：Reverse / PWN 混合

## 关键攻击链
### 1. ELF 彩蛋
- SECTIONS 段含 `_STRIP_ELF_BEFORE_CTF_ = 0x1337`

### 2. 程序交互
- `./words.elf` 启动 + `LD_LIBRARY_PATH=$PWD`
- 命令：
  - `Count[=yes/no]`
  - `Unique[=yes/no]`
  - `Ignore case[=yes/no]`
  - `Verbose[=yes/no]`
  - `Links[=on/off]`
  - `Words[=on/off]`
  - `Fetch <URL>`

### 3. 内部函数
- `get(char *url, char **contentsout)` 下载 URL 内容
- 调用 `accept@GLIBC_2.2.5`, `__xstat64@GLIBC_2.2.5`

### 4. libsqz.so 替换
- 原始 libsqz 是 LZMA 压缩库
- 替换为 `touch libsqz.c` + `gcc -shared libsqz.c -o libsqz.so`
- 绕过大文件 OOM Kill

### 5. 攻击效果
- `Fetch https://neverssl.com` 不再被 Killed
- 拿到 HTTP 响应内容

## 评分
- quality: medium（ELF 彩蛋 + 库替换绕过 OOM，思路新颖）
