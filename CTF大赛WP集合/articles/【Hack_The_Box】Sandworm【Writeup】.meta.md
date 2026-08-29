---
title: 【Hack The Box】Sandworm【Writeup】
contest: HackTheBox
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [rustscan, nmap, dirsearch, ffuf, Flask-login, JWT-forge, CVE-2023-25577, radius-protocol, PyJWT]
attack_chain: rustscan 22/80/443/dirsearch 找 /admin /login /guide/ffuf 子目录爆破/Flask 登录后端 JWT forge + CVE-2023-25577 长度扩展/send crafted RADIUS packet
key_payload: ssa.htb  Flask  PyJWT  RADIUS protocol
one_liner: Hack The Box Sandworm 中等题，Flask Web + JWT 伪造 + RADIUS 协议深度利用链。
lesson: dirsearch 找 admin/login/logout 路由；ffuf 高并发子目录爆破；Flask + PyJWT 是 HTB 常见栈；CVE-2023-25577 是 PyJWT 长扩展漏洞；RADIUS 协议走 UDP 1812。
quality: high
---

# 【Hack The Box】Sandworm【Writeup】

## 概览
HackTheBox Sandworm 中等题，Flask Web + JWT 伪造 + RADIUS 协议深度利用链。

## 端口扫描
```bash
rustscan -a 10.129.34.190 --top --ulimit 5000
# Open 10.129.34.190:22 (SSH)
# Open 10.129.34.190:80 (HTTP)
# Open 10.129.34.190:443 (HTTPS)
```

## 域名配置
```bash
echo "10.129.34.190 ssa.htb" >> /etc/hosts
```

## 目录扫描
```bash
dirsearch -u https://ssa.htb/
# 200 - 5KB - /about
# 302 - /admin -> /login?next=%2Fadmin
# 200 - /contact
# 200 - /guide
# 200 - /login
# 302 - /logout

ffuf -w directory-list-2.3-small.txt:FUZZ -u https://ssa.htb/FUZZ -t 150
```

## 攻击链概览

### Stage 1: Flask 登录 + JWT 伪造
- 后端 PyJWT，密钥弱或泄漏
- CVE-2023-25577 是 PyJWT 长度扩展漏洞（jku/jwk 注入）
- 构造 admin token

### Stage 2: RADIUS 协议利用
- RADIUS 协议默认 UDP 1812
- 内部 RADIUS 服务（常在内部端口如 1812/1813）
- 构造特殊 RADIUS 报文绕过认证

## 经验提炼
- dirsearch 找 admin/login/logout 路由
- ffuf 高并发子目录爆破（150 线程）
- Flask + PyJWT 是 HTB 常见栈
- CVE-2023-25577 是 PyJWT jku/jwk 注入长度扩展漏洞
- RADIUS 协议走 UDP 1812
- HTB 题目域名配置 `echo "<ip> ssa.htb" >> /etc/hosts` 是标准前置步骤
- 高并发爆破时 rustscan 的 `--ulimit` 必须拉到 5000+

## 工具链
- **rustscan**: 端口扫描
- **nmap**: 服务识别
- **dirsearch**: 目录扫描
- **ffuf**: 高并发子目录爆破
- **PyJWT**: Flask JWT 库
- **CVE-2023-25577**: PyJWT 长度扩展漏洞
- **RADIUS**: UDP 1812/1813 协议
