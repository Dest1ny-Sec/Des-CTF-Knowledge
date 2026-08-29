---
title: Social Engineering To Solve A Crypto Challenge – LakeCTF 2022
contest: LakeCTF
year: 2022
difficulty: medium
vuln_type: crypto_rsa
tags: [pgp-rsa, protonmail-lookup, social-engineering, key-recovery]
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
---
# LakeCTF 2022 - Social Engineering PGP

## 背景
- 题目描述：组织者账号被黑后创建新账号
- 攻击者截获 PGP 加密邮件
- 任务是解密该邮件

## 攻击路径

### 1. 公钥获取
```python
import requests
username = "epfl-ctf-admin2"
open("pub", "wb").write(requests.get(
    f"https://api.protonmail.ch/pks/lookup?op=get&search={username}@protonmail.com"
).content)
```

### 2. 公钥解析
```bash
cat pub | gpg --list-packets --verbose
```

解析得到：
- `version 4, algo 1, created 1654083420, expires 0`
- 公钥模数 n (4096-bit RSA 模数, 完整 16 行)
- 公开指数 e = `010001` (65537)
- 密钥 ID: `2461439C55F8627A`

### 3. 攻击方向

#### 方向 A: 分解 n
- 在线查询 FactorDB / yafu 分解
- 若 n 是脆弱生成 (e.g. close primes / Fermat)

#### 方向 B: Social Engineering
- 通过 PGP 公钥服务器可以发现 admin 真实 email
- 邮件转发 / 钓鱼拿到 admin 私钥
- 题目提示是 social engineering → 找社工路径

### 4. 解密
- 用获取的私钥解密 PGP 邮件
- 拿到 flag
