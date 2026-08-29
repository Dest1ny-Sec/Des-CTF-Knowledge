---
title: 2024 CISCN x 长城杯 威胁检测与流量分析 WP（zeroshell + WinFT）
contest: CISCN x 长城杯
year: 2024
difficulty: medium
vuln_type: [stego_traffic, rce, forensic_disk, misc_unknown]
tags: [zeroshell防火墙, CVE-2019-12725, x509view命令注入, Wireshark追踪TCP流, Referer base64, WinFT exe分析, 火绒剑, PCHunter启动项, CTF-NetA 压缩包]
attack_chain: Wireshark 打开 pcap → 搜 "exec" 关键字 → 定位 HTTP 包 → 追踪 TCP 流 → 解码 Referer base64 拿 flag → 找 zeroshell 漏洞 CVE-2019-12725 /cgi-bin/kerbynet?Action=x509view&x509type='%0Aid%0A' 命令注入 → 读 /DB/_DB.001/flag 与 /Database/flag → netstat 查外联 IP 202.115.89.103 → 找 /tmp/.nginx 木马 → IDA 找密钥 11223344qweasdzxc → 启动项 /var/register/system/startup/scripts/nat/File → WinFT 流量分析: 微步云沙箱判 exe 木马 + 火绒剑查外联 IP:PORT + PCHunter 启动项最后一行 flag + cyberchef 解密 + CTF-NetA 梭出分片压缩包
key_payload: /cgi-bin/kerbynet?Action=x509view&Section=NoAuthREQ&x509type='%0Aid%0A' ; flag{c6045425-6e6e-41d0-be09-95682a4f65c4} ; flag{202.115.89.103} ; flag{.nginx} ; flag{11223344qweasdzxc} ; flag{/var/register/system/startup/scripts/nat/File}
one_liner: Wireshark 追踪 Referer base64 + CVE-2019-12725 命令注入 + WinFT 火绒剑 PCHunter。
lesson: zeroshell 防火墙 x509view 接口 %0A 注入 16 年漏洞至今野外仍常见，防火墙类取证要查启动项。
quality: high
---
# 2024 CISCN x 长城杯 威胁检测与流量分析 WP

## 一、zeroshell 流量分析 + 取证

**zeroshell_1**：从攻击者执行命令的 HTTP 数据包定位 flag
- Wireshark 搜 "exec" 关键字
- 追踪 TCP 流，看到 Referer 字段有 `base64(flag{...})`

**zeroshell_2**：漏洞复现拿 flag
- zeroshell 防火墙 CVE-2019-12725 远程命令执行
- Payload: `GET /cgi-bin/kerbynet?Action=x509view&Section=NoAuthREQ&x509type='%0Aid%0A'`
- 注入点在 `x509type` 参数，`%0A` 是换行 → 截断引号闭合
- 在 `/DB/_DB.001/flag` 和 `/Database/flag` 找到
- flag = `flag{c6045425-6e6e-41d0-be09-95682a4f65c4}`

**zeroshell_3**：木马外联 IP
- `netstat -ano` 找异常外部地址
- flag = `flag{202.115.89.103}`

**zeroshell_4**：木马本体文件名
- 找 `/tmp/.nginx`（伪装成 nginx 进程）
- flag = `flag{.nginx}`

**zeroshell_5**：逆向 .nginx 找密钥
- IDA 搜反联 IP 字符串，关键字附近有可疑 16 字节
- flag = `flag{11223344qweasdzxc}`

**zeroshell_6**：启动项
- flag = `flag{/var/register/system/startup/scripts/nat/File}`

## 二、WinFT 流量分析

**WinFT_1**：找可疑 exe
- 微步云沙箱判为木马
- 火绒剑查进程 + 网络连接 → 拿到外联 IP:PORT

**WinFT_2**：PCHunter 取证
- 启动项第 3 个选项最后一行就是 flag
- cyberchef 解密 base64 密文

**WinFT_5**：CTF-NetA 流量拼包
- 流量被切成两部分：client + server
- 拼接后是 zip，含 flag.txt 和时间线注释
- 直接打开拿 flag

**攻击链总览**

| 阶段 | 工具 | 关键产物 |
|------|------|----------|
| 流量定位 | Wireshark | Referer base64 → flag |
| 漏洞复现 | CVE-2019-12725 exp | 命令执行读 /DB/_DB.001/flag |
| 驻留分析 | netstat / find | 外联 IP / .nginx |
| 逆向 | IDA | 密钥字符串 |
| 启动项 | ls /var/register | 启动脚本 |
| Windows 取证 | 火绒剑 / PCHunter | 进程 + 启动项 + 流量拼包 |
