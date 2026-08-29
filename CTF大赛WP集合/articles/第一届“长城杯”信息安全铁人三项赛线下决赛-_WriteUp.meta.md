---
title: 第一届“长城杯”信息安全铁人三项赛线下决赛- WriteUp
contest: 第一届长城杯信息安全铁人三项赛
year: 2024
difficulty: mixed
vuln_type: misc_unknown
tags: [长城杯, 铁人三项, EDI安全, 企业环境渗透, 取证溯源, php://filter读源码, 综合靶场]
attack_chain: 12+个flag(flag1-14)→企业环境渗透(202.0.6.195/194/193)→php://filter读flag.php→取证溯源(data2024.zip+SSH+VNC)
key_payload: "flag1-14多flag;php://filter/read=convert.base64-encode/resource=flag.php;202.0.5.236 root:Szivfn4bLZ;data2024.zip"
one_liner: 第一届长城杯信息安全铁人三项赛线下决赛：12+flag企业环境渗透+取证溯源综合WP
lesson: 铁人三项赛综合渗透：企业环境+移动应用+取证溯源
quality: medium
---

# 第一届"长城杯"信息安全铁人三项赛线下决赛- WriteUp

**赛事**：第一届"长城杯"信息安全铁人三项赛线下决赛（2024，EDI安全战队WP）

**题型**：企业环境渗透 + 取证溯源综合

**第一阶段：企业环境渗透**

**获取的flag**：
```
flag1{9a0fe27c8bcc9aad51eda55e1b735eb5}
flag2{5399019c4053e1a5e756522fe94cdefe}
flag3{21db4fb5e7cd1d14f041436c4f50ce8c}
flag4{efba34b4991857a0c3639a0a31424041}
flag5{a40310f194e1abfec9581d026e29832c}
flag6{bf2bbf3cf5bf7fa02fcfd1f649a03a78}
flag7{cb8650fe07e6f4da7d9f1817b82eb019}
flag8{912ec803b2ce49e4a541068d495ab570}
flag9{ab67b0ec5c2d29c248e3aa9c7d31d620}
flag12{76e24b847fdf0208195fffba98731234}
flag14{8f552743a81f9bc517a35a5421e76764}
```

**三台靶机**：
- 202.0.6.195
- 202.0.6.194
- 202.0.6.193

**关键payload**：
```
http://202.0.6.194:8080/index.php?file=php://filter/read=convert.base64-encode/resource=flag.php
```

**端口扫描结果**（202.0.6.193）：
```
22/tcp   open  ssh
80/tcp   open  http
3306/tcp open  mysql
3389/tcp open  ms-wbt-server
```

**第二阶段：取证溯源**

**题目背景**：
- 同事李白运维Linux服务器发现异常
- 移动应用服务端可能被攻击
- 提供SSH和VNC访问
- data2024.zip流量包

**环境**：
- 用户名：root
- 密码：Szivfn4bLZ
- 虚机IP：202.0.5.236

**关卡1**：黑客攻击此服务器所使用的2个IP（ascii码从小到大排列，空格分隔）

**质量评估**：中（多flag结果 + 关键payload + 取证环境）
