---
title: 2026 丹麦国情局 FE – 恶猿行动 Writeup（OPERATION BAD PRIMATE 渗透）
contest: 2026 丹麦国情局 FE
year: 2026
difficulty: hard
vuln_type: [sqli, lfi, pwn_unknown, ssh, web_unknown]
tags: [丹麦国情局 FE 恶猿行动 2026, MonkEZ/EDO 公司服务器, OPERATION BAD PRIMATE, vmdk 虚拟机, 仅主机模式, nmap 三个 ssh + 一个 http, sqlite 登录 SQLMap, robots.txt 目录扫描, 路径穿越 + AES 加密 SSH 私钥, docker 逃逸 bash_history, TLS 客户端证书密钥被删, root@printserver, root access]
attack_chain:
  - 部署: 下载 vmdk → VM 仅主机模式（避免 NAT 暴露）
  - 外部侦察: nmap 三个 ssh + 一个 http
  - 初始访问: 登录框随便输 → sqlmap dump users → 拿 ssh 凭据
  - docker 登录 → html 注释提示至少 2 个漏洞
  - robots.txt 目录扫描 → 路径穿越
  - 路径穿越拿 AES 加密的 SSH 私钥
  - docker 逃逸: bash_history 查 docker 命令 → 需 TLS 客户端证书
  - 证书密钥已被删 → 需从备份/历史恢复
  - 最终: root@printserver
key_payload: "robots.txt → 路径穿越 → AES SSH 私钥"
one_liner: 2026 丹麦国情局 FE 恶猿行动：MonkEZ/EDO 服务器渗透 - sqlmap + robots 路径穿越 + AES SSH 私钥 + docker 逃逸 + TLS 客户端证书恢复。
lesson: 丹麦国情局 FE 是面向计算机网络利用部 (CNE) 培训的高仿真 APT 渗透靶场，核心是 docker 逃逸 + TLS 客户端证书恢复；用 vmdk 部署 + 仅主机模式 防 VM 反弹。
quality: high
---

# 2026 丹麦国情局 FE – 恶猿行动 Writeup（OPERATION BAD PRIMATE）

## 背景

> 战略关注与考量部 → 计算机网络利用部（CNE）培训  
> 截止日期：2026-02-30  
> 目标公司：**MonkEZ/EDO**（掩护非法活动）  
> 任务：从旧备份服务器中找漏洞，识别即使密码改了也能用的访问路径 → **root@printserver**

## 虚拟机部署

下载 vmdk → VM 新建虚拟机用这个 vmdk  
**重要**：不确定 VM 是否 200% 安全前，**不要设置为 NAT**！  
建议 **"仅主机模式"**（避免 VM 访问你的本地网络/互联网）。

## 攻击链

### 1. 外部侦察
```bash
nmap -p- 192.168.x.x
# 三个 ssh + 一个 http
```

### 2. 初始访问（sqlmap + sqlmap dump users）
- http 登录框随便输 → 提示 sqlite
- `sqlmap -u "http://target/login" --data="user=admin&pass=admin" --dump -T users`
- dump users 表 → 拿到 ssh 凭据
- ssh 登录发现是 docker 容器
- html 注释提示"至少 2 个漏洞"

### 3. 路径穿越 + AES SSH 私钥
- `robots.txt` 目录扫描发现隐藏路径
- 路径穿越漏洞（`../` 遍历）
- 拿到 **AES 加密的 SSH 私钥**

### 4. docker 逃逸
- 查 `.bash_history`
- docker 远程访问需 **TLS 客户端证书+密钥**
- 但证书密钥已被删 → 需从备份/历史恢复

### 5. 终极目标
- `root@printserver` 拿到 root 访问

## 战队经验

> vpn network 还差最后两个二进制 → 提示要补二进制
> 二进制始终要面对 → 春节后协调进大师计划
