---
title: 2025 第三届京麒 CTF 挑战赛 writeup by Mini-Venom
contest: 京麒 CTF
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [SSTI, 删disable, FastJson1.2.80, CVE-2022-25845, JsonGenerationException, FilterFileOutputStream, MarshalOutputStream, InflaterOutputStream, /etc/crontab, Frida hook, XXTEA, libre0.so]
attack_chain:
  - 计算器题: 删 disable 后 ''.__class__.__mro__[1].__subclasses__()[80].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("env").read()') 拿 flag
  - FastJ 题 step1: 双 @type 触发 JsonGenerationException 缓存 UTF8JsonGenerator
  - FastJ 题 step2: $ref 二次取 OutputStream 走 MarshalOutputStream+InflaterOutputStream+FilterFileOutputStream 写 /etc/crontab
  - DeflaterOutputStream 把反弹 shell 指令压缩 + base64 作为 array 字段
  - Crontab root 反弹 shell → RCE
  - 安卓题: Frida hook libre0.so+0x184C 的 XXTEA 加密函数观察入参出参
key_payload: '{{+__class__+__mro__+__subclasses__+__init__+__globals__+__builtins__+eval+popen(env).read()}} + FastJson1.2.80 CVE-2022-25845 双 @type 缓存链'
one_liner: 京麒 CTF 三题 — SSTI 绕 disable 直接 RCE + FastJson 1.2.80 CVE-2022-25845 写 /etc/crontab 反弹 + 安卓 XXTEA Frida hook 提取密钥。
lesson: FastJson 1.2.80 黑名单禁了 FileOutputStream 但应用自定义 FilterFileOutputStream 时仍可借 sun.rmi.server.MarshalOutputStream 走 RCE；SSTI 沙箱 disable 删配置即可破。
quality: high
---

# 2025 第三届京麒 CTF 挑战赛 writeup by Mini-Venom

## 速读
ChaMd5 Mini-Venom 团队 — 两道 web + 一道安卓 reverse 复盘。

## Web — 计算器
- SSTI 沙箱过滤了部分关键字但 disable 文件可直接删
- 经典 `''.__class__.__mro__[1].__subclasses__()[80].__init__.__globals__['__builtins__']['eval']('__import__("os").popen("env").read()')` 链
- 读环境变量得 flag

## Web — FastJson 1.2.80
- 应用自定义 `com.app.FilterFileOutputStream` 绕 1.2.80 黑名单
- 利用 CVE-2022-25845 风格双 @type 链：
  - 第一步: `@type=java.lang.Exception` → `com.fasterxml.jackson.core.JsonGenerationException` (缓存 g)
  - 第二步: `@type=com.fasterxml.jackson.core.JsonGenerator` → `com.fasterxml.jackson.core.json.UTF8JsonGenerator` (缓存 out)
  - 通过 `$ref=$.a.a` `$ref=$.c.c` 二次取
- 写文件链: `OutputStream` → `sun.rmi.server.MarshalOutputStream` → `java.util.zip.InflaterOutputStream` → `FilterFileOutputStream`
- 写入 `/etc/crontab` (root 权限) → 反弹 shell
- POC 完整 Java 代码 (RestTemplate + payload1/2)

## 安卓 Reverse
- Frida hook `libre0.so + 0x184C` (XXTEA 加密)
- Interceptor.attach 打印 args[0] args[2] args[3] + hexdump
- 推 XXTEA key + 提取明文

## 评价
技术深度可观 — FastJson 1.2.80 利用链完整但需应用提供 FilterFileOutputStream，CRC 题少了一道；安卓 hook 简短但有可复现性。
