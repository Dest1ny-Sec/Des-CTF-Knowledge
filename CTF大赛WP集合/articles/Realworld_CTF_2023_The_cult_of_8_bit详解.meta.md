---
title: Realworld CTF 2023 The_cult_of_8_bit 详解
contest: Realworld CTF 2023
year: 2023
difficulty: high
vuln_type: xss
tags: [jsonp, same-origin-method-execution, iframe-focus, post-id-leak, csrf, char-by-char-extract, opensearch-opener]
attack_chain:
  - 博客系统: /login /register /report /post / 五个路由
  - admin 用户密码 sha256(ADMIN_PASSWORD || "password") + Object.freeze
  - 初始 flag post: crypto.randomUUID() 作 id, body=FLAG env
  - admin 不可创建 todo (Nice try redirect)
  - 漏洞 1: XSS todo 注入 - new URL(text) 检测 + javascript: 黑名单
  - 漏洞 2: JSONP callback 跨域调用 load_post({success, name, body})
  - 漏洞 3: URLSearchParams.get('id') 不 url-decode → null byte 注入
  - 攻击: %00 截断 + %3F 替换 ? + callback=alert%23
  - 完整链: post/?id=UUID%3Fcallback=alert%23%00 → innerHTML 渲染 callback
  - admin 通过 report URL 访问 → callback 触发 → opener 跨窗口调用
  - 技巧: opener.opener.document.body...text[i] 逐字符提取 post id
  - iframe focus 监听: charList="0123456789abcdef-" + createIframe(name)
  - document.activeElement.name 获焦点 iframe name → 还原 36 字符 UUID
  - feature policy allow="sync-xhr 'none'" 阻止 sync-xhr
  - 完整利用: open /b.html + location=/(admin home) + listenFocus + exploit 36 次
  - 36 次循环: for i=0..35 { challenge.location = /post/?id=...%3Fcallback=...+text[i]+.focus }
key_payload: opener[opener.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].text[${i}]].focus
one_liner: Realworld CTF 2023 The_cult_of_8_bit：JSONP callback + URL %00 截断 + opener opener 跨窗口访问 admin home + iframe focus 监听逐字符提取 UUID 拿到 flag post。
lesson: JSONP + URLSearchParams.get 不解码是 web 高阶绕过；opener.opener 跨窗口读取同源页面内容是经典 XSS 提权；iframe name + focus + activeElement 是逐字符提取 UUID 的盲注技巧。
quality: high
---
