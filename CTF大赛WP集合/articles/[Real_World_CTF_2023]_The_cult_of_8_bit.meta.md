---
title: [Real World CTF 2023] The cult of 8 bit
contest: Real World CTF 2023
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [nodejs_ejs, jsonp_xss, callback_proto_pollution, win_open_opener, focus_iframe_alphabet, xs_leak_href_one_byte, real_world_ctf_challenge, javascript_url_filter_bypass, real_world_8bit_exploit]
attack_chain: 1) Node.js EJS 模板 <%= todo.text %> 不转义 (URL 模式 href 直接输出) + isURL = !text.toLowerCase().trim().startsWith("javascript:") 弱过滤 → javascript:alert() 嵌 [ 开括号 → [javascript:alert()] / 2) window.open opener + opener.opener 跨窗口访问 → JSONP callback=our_function%23%00 切断原 callback → 4 字符的 opaener 标识泄漏 / 3) 16 个 iframe name=alphabet 中 0-9a-f- 检测 onfocus event → setInterval 检测 document.activeElement.name → 字符级泄漏 / 4) 长度 36 的 post id 逐字符访问 opener.opener.document.body.children[1].childNodes[1].children[0].children[0].children[3].children[0].children[0].children[0].href[32+i].focus
key_payload: text = "[](javascript:alert())" / JSONP /api/post/{id}?callback=our_function%23%00 / alphabet = "0123456789abcdef-" / 16 iframes with name=alphabet[i] / document.activeElement.name
one_liner: Real World CTF 2023 The cult of 8 bit：Node EJS URL 弱过滤 + JSONP callback %23%00 切断 + 16 iframe focus 事件字符级 href 泄漏，opener 跨窗口访问实现 8-bit 单字符 XS-Leak。
lesson: 现代浏览器已经屏蔽 opener.document 跨域访问，但通过 open() + 多次 redirect + target 锚点 + iframe focus 事件仍可单字符泄漏；alphabet iframe 是字符级盲注标配。
quality: high
---
