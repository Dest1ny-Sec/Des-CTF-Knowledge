---
title: 2026 阿里 CTF Writeup by Mini-Venom
contest: 阿里CTF
year: 2026
difficulty: hard
vuln_type: web_unknown
tags: [heartbeat代理, Content-Type覆盖, format string, {0.config}, SSTI, .webp伪装.class, CAFEBABE, DexClassLoader动态加载, C0003L扫描器, Runner.encrypt虚拟机, LZRR压缩, 4C5A5252头, CRC32 0xEDB88320, RSA-2048 SessionKey, 89ali魔数, XOR 233文件名, BackupExec RPC NDR, OpenRemoteFile, 16字节XOR]
attack_chain:
  - Web: heartbeat 代理 action 部分, client Content-Type + token multipart/form-data 注入
  - 用 {0.view_functions[index].__globals__[API_KEY]} format string 泄 API_KEY
  - admin 读模板 SSTI: {config.__class__.__init__.__globals__['os'].popen('cat /flag*').read()}
  - 伪装: res/mipmap 数字命 .webp 头是 CAFEBABE 实际是 .class
  - DexClassLoader 动态加载 .webp 中的代码
  - C0003L 扫描器遍历目录找 .java 源文件
  - Runner.encrypt: 8字节 Key + IV + Base64 指令 → 置换移位变换（对称算法）
  - Il1.LZRR 自定义 LZ77 压缩 (头 4C 5A 52 52, version/mode/origLen/crc32, mode=15 走 RLE)
  - 协议: 8 字节 Session Key 用 RSA-2048 公钥加密 + XOR 233 文件名 + LZRR 压缩 payload + 89 61 6C 69 头
  - 流量包 data0/data1/data2 = 3 batch
  - 奇数 batch algo3 keyless（rank=0）, 偶数 batch algo2 依赖 key 需已知明文恢复 keystream
  - BackupExec RPC OpenRemoteFile NDR 16字节 XOR 解密读 flag
key_payload: 'heartbeat 代理 + format string + SSTI / .webp=.class DexClassLoader / LZRR 4C5A5252 / 89ali 头 + RSA-2048 SessionKey + XOR 233 / BackupExec RPC OpenRemoteFile + 16字节 XOR'
one_liner: 阿里CTF 2026 — Web heartbeat 代理 + format string + SSTI + Android .webp 伪装 .class DexClassLoader + 3 batch 流量 (RSA-2048+LZRR+89ali) + BackupExec RPC NDR 16字节XOR。
lesson: 伪装 .webp/.png/.jpg 是反检测常规手段（CAFEBABE 头 magic number 直接暴露 .class）；加密协议魔数 + RSA 会话密钥 + LZRR 自定义压缩是常见样本偷数据模式；BackupExec RPC 是历史漏洞重灾区。
quality: high
---

# 2026 阿里 CTF Writeup by Mini-Venom

## 速读
ChaMd5 Mini-Venom 团队 — 4 道大题混合(Web+Android+流量+BackupExec RPC)。

## Web
- heartbeat 代理注入
- format string `{0.view_functions[index].__globals__[API_KEY]}` 泄 API_KEY
- admin SSTI 读 flag

## Android 木马 (anti-VM)
- res/mipmap/*.webp 头是 `CAFEBABE` 实际是 .class
- DexClassLoader 动态加载
- C0003L 扫描器找 .java 源文件
- Runner.encrypt 8字节 Key + IV + 指令 → 置换移位
- Il1.LZRR 自定义 LZ77 (头 `4C 5A 52 52`, mode=15+RLE, CRC32 0xEDB88320)

## 协议封装
- 8 字节 Session Key 用 RSA-2048 加密
- 文件名 XOR 233
- LZRR 压缩 payload
- 头 `89 61 6C 69` ("\x89ali")
- 流量包 3 batch，奇数 keyless，偶数 key 依赖

## BackupExec RPC
- NDR OpenRemoteFile
- 16 字节 XOR 解密
- imacket transport + rpcrt
