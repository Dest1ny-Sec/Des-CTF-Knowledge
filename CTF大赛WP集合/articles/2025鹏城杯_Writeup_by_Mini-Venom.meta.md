---
title: 2025 鹏城杯 Writeup by Mini-Venom
contest: 鹏城杯
year: 2025
difficulty: hard
vuln_type: web_unknown
tags: [myZoo菜单pwn, Heartbeat_Out_of_Bounds, MQTT hash31 auth, Pivoting栈迁移, ez_java JWT HS512, /download path=uploads/..%2fWEB-INF, tar路径穿越, web.xml覆盖jsp-file, ez_php Session+file包含, Uplssse spl_autoload .inc 0.5s竞争, ezDjango pickle反序列化, true_or_false LCG, lcg反推seed]
attack_chain:
  - myZoo: 菜单 1/2/3 选项, payload b'a'*4+p64(0x1FB9) 触发后门, %23$p 泄栈拿 libc/heap/stack
  - Heartbeat_Out_of_Bounds: MQTT hash31 算 auth, set_vin TOCTOU 竞态 sleep(2) 期间改合法 vin
  - Pivoting: 拿到 libc 但栈低, 调高栈 + leave_ret 二次栈迁移
  - ez_java: /download?path=uploads/..%2fWEB-INF 绕, JwtUtil.class 拿 secret-secret-secret-secret-secret-secret-secret-secret-secret-secret-secret
  - jwt.encode HS512 sub=admin exp=1999999999
  - admin/upload 上传 tar, entry.getName()="/../WEB-INF/shell.xml" 写 jsp
  - 再传 web.xml 加 jsp-file 映射, 访问 /shell RCE
  - ez_php: Cookie: identification=Tzo...Session\User 走 dashboard.php?filename= 绕后缀
  - Uplssse: 恶 .inc 上传, Cookie O:4:Evil 触发 spl_autoload, 0.5s 竞争写 shell.php
  - ezDjango: str.format ssti + copy_file 写恶意 pickle 到 cache, pickle.load() RCE
  - true_or_false: LCG (A=1103515245, B=12345, MOD=2^31) 8字节块反推 seed
key_payload: 'JWT HS512 secret-secret-secret-secret-secret-secret-secret-secret-secret-secret-secret / MQTT hash31 auth TOCTOU / tar /../WEB-INF 路径穿越写 shell.xml / 0.5s 竞争 .inc autoload / pickle.copy_file RCE / LCG 反推 seed'
one_liner: 鹏城杯 2025 7 题 — myZoo 菜单 pwn + MQTT Heartbeat TOCTOU + Pivoting 栈迁移 + ez_java JWT HS512+tar 写 shell.xml + ez_php Session LFI + Uplssse spl_autoload 0.5s 竞争 + ezDjango pickle RCE + LCG 逆推。
lesson: JWT 密钥在 .class 文件中是字符串常量 (strings 命令可读)；tar 路径穿越 + JSP 映射 web.xml 的 servlet 元素是关键链；MQTT hash31 是 (31*x+ord) 累加;LCG 单块反推 seed 需先解 lcg.
quality: high
---

# 2025 鹏城杯 Writeup by Mini-Venom

## 速读
ChaMd5 Mini-Venom 团队 — 7 题 WP 集合（5 Web + 2 Pwn + 1 Crypto）。

## Pwn

### myZoo
- 菜单选项 1/2/3
- payload `b'a'*4+p64(0x1FB9) + 填充 + p64(0x11E0)` 触发后门
- 选项 2 触发 `%23$p--%7$p--%6$p` 泄栈拿 libc/heap/stack
- 选项 1 触发 system("/bin/sh")

### Heartbeat_Out_of_Bounds
- MQTT `hash31(vin)` 算 auth
- 订阅 `#` 等心跳
- `set_vin TOCTOU`: 合法 VIN 触发 sleep(2) 期间改 vin

### Pivoting
- 拿 libc 但栈低, 调高栈
- 二次 leave_ret 栈迁移

## Web

### ez_java
- `/download?path=uploads/..%2fWEB-INF%2fclasses%2fcom%2fctf%2fJwtUtil.class` 读类
- JWT 密钥: `secret-secret-secret-secret-secret-secret-secret-secret-secret-secret-secret` (HS512)
- admin JWT 伪造 `sub=admin exp=1999999999`
- tar `/../WEB-INF/shell.xml` 路径穿越 + 改 web.xml 加 jsp-file 映射

### ez_php
- Cookie `identification` base64 Session\User
- dashboard.php?filename=….//flag.php/ 后缀绕

### Uplssse
- `spl_autoload_register` 加载 `tmp_directory=./tmp/类名.inc`
- 上传恶意 .inc → 0.5s 竞争 Cookie O:4:Evil 触发

### ezDjango
- str.format ssti
- copy_file 写恶意 pickle 到 django cache
- 触发 `cache.get('pwn')` → pickle.load() RCE

## Crypto: true_or_false
- LCG `s = (1103515245*s + 12345) % 2^31`
- 8 字节块反推 seed
