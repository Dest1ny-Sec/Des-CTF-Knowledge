---
title: SANS Offensive CTF - Taskist 01-04
contest: SANS Offensive CTF
year: 2025
difficulty: medium
vuln_type: ssrf
tags: [idor, privilege-escalation, ssrf, lfi, file-read, proc-self-environ, burp-intruder, file-protocol, jwt]
attack_chain:
  - Taskist::01 IDOR: /api/tasks/64 越权访问 admin task 拿到 flag-1
  - 攻击: Burp Intruder 遍历 1-100 数字 payload
  - Taskist::02 权限提升: update password 接口 user_id 参数可改
  - 改 user_id 为 admin 的 user_id → 改 admin 密码 → 拿 flag-2
  - Taskist::03 SSRF: site_config 导入功能 url 参数可改
  - 攻击: 上传 dummy 文件 + Burp 拦截 + 改 url=http://attacker.com → SSRF confirmed
  - 利用 /proc/self/environ + /app/index.js 读源码
  - 提示: admin 还有 2/3 task pending, 提示 /app 目录
  - Brute force LFI 常见 payloads → /proc/*/* 敏感端点
  - 拿到 flag-3
  - Taskist::04 SSRF 链根目录: 文件上传触发 file:///
  - file:///etc/* 测根目录 → file:///root/flag.txt 读 root flag
  - 拿到 flag-4
  - 全程工具: Burp Suite Intruder / Collaborator
key_payload: file:///root/flag.txt
one_liner: SANS Offensive CTF Taskist 4 题：IDOR 遍历 tasks/64 拿 flag1 + 改 user_id 改 admin 密码 + SSRF 测 LFI 读源码 + file:///root/flag.txt 读根目录。
lesson: IDOR + 权限提升 + SSRF + LFI 是 OWASP Top 10 经典 4 链；Burp Intruder 数字遍历是 IDOR 探查基础；/proc/self/environ 读环境变量是 SSRF 提权必经之路。
quality: medium
---
