---
title: CTFSHOW 第三届愚人杯 WP
contest: CTFShow
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [PNG CRC32反推宽高, Ook语言, PHP base64任意文件读, 反序列化链 w_wuw_w+gBoBg, Caesar字符移位, Flask SSTI cycler, RSA链式加密+IP尾, s_box+encrypt1+encrypt2, 矩阵异或+线性代数, 异或递推, PNG矩阵成图]
attack_chain:
  - Misc: PNG CRC32 反推 width/height (for w/h in 4096)
  - Ook 语言: !替换！, .替换。, ?替换？
  - Web PHP: ?img=base64(file) 任意文件读
  - 反序列化: w_wuw_w __destruct → gBoBg __toString → w_wuw_w __invoke → EeE __clone → cycycycy.aaa
  - Caesar 字符移位 4 + qwertyuiopasdfghjklzxcvbnm123456789
  - Flask SSTI: g.pop.__globals__.__builtins__.__import__('os').popen('ls').read()
  - Crypto: RSA PKCS1_v1_5 链式加密 (密文1+IP2 → 密文2+IP3 → 明文+IP用户B)
  - encrypt1: 块内 16 字节 7 倍位置交换
  - encrypt2: S_BOX 置换 16 次
  - Reverse: 矩阵加密 (300*300 异或表) + 矩阵成图
  - flag 不在题面, 在加密矩阵本身
key_payload: 'PNG CRC32 反推 / Ook 语言 / PHP base64 任意文件读 / 反序列化 4 步链 / Caesar 移位 4 / Flask SSTI / RSA PKCS1 链式加密 / S_BOX 置换 / 300x300 矩阵异或 / 矩阵成图'
one_liner: CTFSHOW 第三届愚人杯 — 12+ 题合集: PNG CRC32 反推 + Ook 语言 + PHP base64 任意文件读 + 反序列化 4 步链 + Caesar + Flask SSTI + RSA 链式 + S_BOX 置换 + 矩阵异或。
lesson: 愚人杯风格是 1 道题多种 trick 混合;PNG CRC32 反推宽高是经典;反序列化 4 步链 (destruct → toString → invoke → clone) 是 PHP 模板;S_BOX 置换 + 16 轮 encrypt1 块内交换是常见加密。
quality: high
---

# CTFSHOW 第三届愚人杯 WP

## 速读
CTFSHOW 愚人杯 多题合集 — 12+ 题涵盖 Misc/Web/Reverse/Crypto。

## 题目列表

### Misc
- **PNG 宽高反推**: CRC32 暴力 w/h 0..4096
- **Ook 语言**: 中文标点替换 (!→！ .→。 ?→？)

### Web
- **PHP base64 任意文件读**: `?img=base64(file_get_contents(...))`
- **反序列化 4 步链**: `w_wuw_w.__destruct → gBoBg.__toString → w_wuw_w.__invoke → EeE.__clone → cycycycy.aaa`
- **Caesar 移位 4**: `qwertyuiopasdfghjklzxcvbnm123456789`
- **Flask SSTI**: `g.pop.__globals__.__builtins__.__import__('os').popen('ls').read()`

### Crypto
- **RSA 链式加密**: PKCS1_v1_5 加密 (密文1+IP2 → 密文2+IP3 → 明文+IP用户B)
- **S_BOX + encrypt1**: 16 轮 S_BOX 置换 + 块内 16 字节 7 倍位置交换 (BLOCK=16, j*7%BLOCK)
- **矩阵加密**: 300x300 异或表 + 已知部分明文反推 index + 矩阵成图 (PIL.Image)

### Reverse
- **加密矩阵 0x28A0..0x5A6E0**: 提取成 PIL Image 看 flag
- **异或递推**: code[i] ^ code[i+1] 反推原 flag
- **flask 模版注入**: `render_template_string('hello %s' % name)` + 'ge' in name 黑名单
- **RSA 加密 +10 字节 IP**: `data = decrypt(data1, key.export_key())`

## 关键
- 矩阵是 flag 的图, 加密矩阵 (300*300) 是关键
- 反序列化 4 步链是 PHP 经典
- S_BOX 置换 + 块内 7 倍交换是常见加密
