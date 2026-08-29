---
title: 2025"领航杯"网安赛项教师组决赛 WP（上）- Crypto 修栅栏/RSA + Misc DNS/FTP + Web locallogin
contest: 2025 领航杯网安赛项
year: 2025
difficulty: medium
vuln_type: [crypto_rsa, web_unknown, sqli, ssrf, auth_bypass]
tags: [领航杯 2025 教师组 决赛, Crypto 修栅栏 rail fence cipher, CnHongKe base64 拼接, DNS 二级域名组成有意义语句, FTP 流量 flag.zip + sk.pem + secret.enc, X-Forwarded-For 127.0.0.1 绕过 IP 检测, base64 编码 cookie 替换 user→admin, sqlmap 盲注]
attack_chain:
  - Crypto 修栅栏：三个一组替换，从上往下从左往右拼接 → CnHongKe base64 → 解码
  - Crypto RSA：直接参考 Python 脚本运行
  - DNS 流量：二级域名组成有意义语句 → flag
  - FTP 流量：flag.zip + sk.pem + secret.enc → 还原密文
  - Web locallogin: user/userpass 登录 + X-Forwarded-For: 127.0.0.1 绕 IP 检测
  - cookie base64 编码 user→admin 替换
  - Web sql: sqlmap 脚本爆破
key_payload: "X-Forwarded-For: 127.0.0.1 绕 IP 检测"
one_liner: 2025 领航杯教师组决赛上：Crypto 修栅栏+RSA + Misc DNS/FTP + Web locallogin XFF+cookie 替换+sqlmap。
lesson: 修栅栏密码 = 三组字符按行拼接 → base64 编码；X-Forwarded-For 绕 IP 检测是经典 Web 套路；base64 编码 cookie 替换 user 字段是 admin 鉴权绕过常考点。
quality: medium
---

# 2025"领航杯"网安赛项教师组决赛 WP（上）

## 01-1 Crypto 修栅栏

三个一组进行替换，从上往下从左往右进行拼接 → `CnHongKe` 的 base64 编码  
直接 base64 解码得答案。

## 01-2 Crypto RSA

直接参考 Python 脚本，运行即可。

## 02-1 Misc DNS 流量分析

打开 pcap 发现都是 DNS 流量  
观察传输的**二级域名**可以组成有意义语句  
整合得 flag。

## 02-2 Misc keyfile

分析流量发现 FTP 流量 → 优先查看传输的文件  
发现 flag.zip，但保存出来是加密的 → 结合 `sk.pem` + `secret.enc` 解密数据  
得到密文。

## 03-1 Web locallogin

```bash
# 1. user / userpass 登录
# 2. 登录后抓包，加 X-Forwarded-For: 127.0.0.1 绕 IP 检测
# 3. 查看 cookie 值，base64 编码
# 4. 将 user 替换为 admin，base64 编码替换 cookie
```

## 03-2 Web sql

sqlmap 脚本爆破，写脚本自动化。

## 总结

- **修栅栏密码**：多组字符串按规则拼接 → base64
- **DNS 二级域名**：隐写信息
- **FTP sk.pem + secret.enc**：PKI 解密 flag.zip
- **X-Forwarded-For 127.0.0.1**：绕 IP 黑白名单
- **cookie base64 user 字段替换**：admin 提权
