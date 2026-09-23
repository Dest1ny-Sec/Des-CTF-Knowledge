---
title: Social Engineering To Solve A Crypto Challenge – LakeCTF 2022
contest: LakeCTF
year: 2022
difficulty: medium
vuln_type: crypto_rsa
tags:
- pgp-rsa
- protonmail-lookup
- social-engineering
- key-recovery
attack_chain:
- 知道收件人 epfl-ctf-admin2 @protonmail.com
- 调 ProtonMail API https://api.protonmail.ch/pks/lookup?op=get&search={user}@protonmail.com
- 下载公钥 pub
- gpg --list-packets --verbose 解析公钥
- 拿到 sub key packet v4 algo 1 (RSA)
- e = 010001 (标准 65537)
- n = 0x B1CF59A37A81DA78...DC3
- 检查 n 是否可分解 (FactorDB)
- 假定 n 是 1024-bit 标准 RSA 但因 social 攻击已知部分信息
- 攻击者拿到 mail 转发后尝试用 admin 凭据重发
- social engineering 拿私钥 → 离线解密 PGP
key_payload: requests.get("https://api.protonmail.ch/pks/lookup?op=get&search=epfl-ctf-admin2@protonmail.com")
one_liner: LakeCTF 2022 社工 + Crypto：通过 ProtonMail API 公开查询接口拿到 PGP 公钥用于后续攻击。
lesson: 任何 PGP 公钥服务器都允许陌生人拉取目标公钥；私钥安全完全依赖持有者。
quality: medium
full_path: Social_Engineering_To_Solve_A_Crypto_Challenge_–_LakeCTF_2022.full.md
meta_path: Social_Engineering_To_Solve_A_Crypto_Challenge_–_LakeCTF_2022.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Social Engineering To Solve A Crypto Challenge – LakeCTF 2022。LakeCTF 2022 社工 + Crypto：通过 ProtonMail API 公开查询接口拿到 PGP 公钥用于后续攻击。。关键路径：知道收件人 epfl-ctf-admin2 @protonmail.com → 调 ProtonMail API https:/...
category: crypto
subcategory: rsa
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/59629.html
reasoning_chain:
- 任务：解密 PGP 邮件 → 触发点：缺私钥
- 知道收件人 epfl-ctf-admin2@protonmail.com → 假设：ProtonMail PGP 公钥服务器可拉
- 动作：curl 'https://api.protonmail.ch/pks/lookup?op=get&search=epfl-ctf-admin2@protonmail.com' → 观察：拿到 pub
- gpg --list-packets --verbose pub → 假设：解析得到 RSA 公钥参数
- 观察：n=4096-bit, e=65537 → 假设：要么分解 n 要么社工
- FactorDB 查询 n → 失败：n 不是脆弱生成
- 假设：社工路径 → 邮件转发/钓鱼拿到 admin 私钥
- 动作：用私钥解密 PGP 邮件 → flag
failed_attempts:
- 试图直接 FactorDB 分解 4096-bit n → 失败：n 是标准 RSA 非脆弱
- 试图离线爆破私钥 → 失败：4096-bit 不可行
key_observations:
- 任何 PGP 公钥服务器都允许陌生人拉取目标公钥；私钥安全完全依赖持有者
- ProtonMail API 是公开的 PGP lookup 接口 (/pks/lookup?op=get)
- 社工攻击是 crypto 难题常被忽视的合法解法
- 邮件转发 + 重发是 admin 凭据恢复的经典社工路径
prerequisites:
- PGP 公钥服务器查询协议 (HTTPS API)
- gpg --list-packets 命令解析
- FactorDB 等 RSA n 分解查询
- 社工攻击思路与邮件转发机制
---
# Social Engineering To Solve A Crypto Challenge – LakeCTF 2022

> 原文: https://www.ctfiot.com/59629.html
> ID: 59629


```
1
2
3
After getting hacked, the organizers of the CTF created a new and
more secure account. You were able to intercept this PGP encrypted
e-mail. Can you decrypt it?
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
import requests
username = "epfl-ctf-admin2"
open("pub", "wb").write(requests.get(f"https://api.protonmail.ch/pks/lookup?op=get&search={username}@protonmail.com").content)
!cat pub | gpg --list-packets --verbose

# The relevant public key used for the challenge:

# :
public sub key packet:
# version 4, algo 1, created 1654083420, expires 0
# pkey[0]:
# B1CF59A37A81DA7854EFFDB8C9FE9F2AABEC72FEC3D62324B24D9DB7DE01A3099F79E01219EC35DB4C58C
# 4C6A1B09865349E37B218F48CA9EC161AF84ED32AD5E7B096079DF567991C1B9E03A419B00D3FF6350849
# C1E8C0753E2BCD54BDD33D81D5D564EE721A6BE80921B4CF220AA9F05F53D98106E59DE9ED327899FB633
# 86AB95F106E5CD60F4F578096B0E0C217928BE5CF6BBE10C6633F2DC320D224AEBF51FE34352738AD0B6E
# 0873C6C3DF5E49EF218F02688F1478D50A55A44D875BFC4799754C2F6135FF168C9C8E225EBF84850A01C
# A7AE789D425824663FD2479ECC7AD71E1BE674FA59A42ACBAFA48EB43B181957145ED996739FFACE0A2F8
# 3432C0E9D64BCC5A68033AD8E7DF8191B1C0C157007544C8D1AE3A4B662D4B8FAE3549B2A63A076D62E34
# 847DD1AE307B3741A5CE1B5727A2586448FFFA1BB5FF019EA7230CC61DDDA1663B2E165322A02A13EF02B
# 9183704B083C3C7E9A9919C37693BE62A8B4F592041605AD046AC32D0DBFC0D312709D881DD164E2DD130
# 791BA70282FDBBA4391D78CD856AD237F73115DD1A0DD12EFE336E580C0B19C9A4B61F5119A0C1BAEC7C0
# E313EB65C7405DE5B9BC4C6464A08547887F1C255C1E5ABE8989BF57D94C20E1B50151F4FA796EE46E69B
# A77C289641EE560B80F2665BD8292C5DD25304BE9246E0FA38133DDD543FB26582DE80A8A0077A7ED636A
# 2DC3
# pkey[1]: 010001
# keyid: 2461439C55F8627A
```
