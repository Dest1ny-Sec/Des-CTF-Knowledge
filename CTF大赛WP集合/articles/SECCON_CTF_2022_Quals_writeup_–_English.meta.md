---
title: SECCON CTF 2022 Quals writeup - English
contest: SECCON CTF 2022 Quals
year: 2022
difficulty: high
vuln_type: ssrf
tags: [qs-parameter-limit, http-param-pollution, ssrf, flask-template, lfi, smuggled-cookie, xss, dompurify-trusted-types, regexp-rightContext, deno-prototype-pollution, prototype-proxy]
attack_chain:
  - 题目 1 skipinx: nginx 注入 &proxy=nginx + Express 限制
  - nginx.conf: set $args "${args}&proxy=nginx" + proxy_pass
  - Express: req.query.proxy.includes("nginx") → 400 error
  - qs (Node query string) parameterLimit=1000 默认值
  - 1000 个 & 拼参数耗尽 limit → 第一个 proxy=nginx 被丢弃
  - flag: SECCON{sometimes_deFault_options_are_useful_to_bypa55}
  - 题目 2 easylfi: Flask + curl file:// + WAF (SECCON) + template replace
  - curl file://{os.getcwd()}/public/{filename} 路径可控
  - 拦 '..' 和 '%' 防 LFI
  - 绕过: filename='.{.}./.{.}./flag.txt' + params="{name}":"{"
  - WAF 检查 SECCON 字符串 → 用 "{!" 吃掉 SECCON{
  - 完整 payload: /{.}./{.}./{app/public/hello.html,flag.txt} + params={name}→{, → →}{, → {SECCON}清
  - 还原 flag = "SECCON{real_flag}" 跳过 WAF
  - flag: SECCON{i_lik3_fe4ture_of_copy_aS_cur1_in_br0wser}
  - 题目 3 ldx: HTTP request smuggling + cookie 窃取
  - 4 服务: nginx (3000) + bff (Python waitress) + backend (3000) + bot (puppeteer) + report
  - waitress parser 接受第一个 HTTP/1.1 line
  - bff: proxy backend 转发原始 payload
  - evilHeader = encode(`bbb\r\nContent-Length: ${contentLength}\r\n`) q-encoded
  - bot 触发 fetch + xss 攻击者服务器 + cookie=/?a=b HTTP/1.1 注入
  - 内容长度 = 24 = 0x18 控制请求边界
  - 完整 XSS 链: 攻击者服务器弹 cookie 到 ?text=...
  - flag: SECCON{i5_1t_p0ssible_tO_s7eal_http_only_cooki3_fr0m_XSS}
  - 题目 4 DOMClobber: DOMPurify trustedTypes + RegExp.rightContext bypass
  - createHTML: unsafe → DOMPurify.sanitize + .replace(/SECCON{.+}/g, REDACTED)
  - 利用 "".match(/^$/) 设置 RegExp.input = matched string
  - document.all["0"]/ownerDocument/defaultView/RegExp/rightContext 泄露
  - emoji="0/ownerDocument/defaultView/RegExp/rightContext"
  - message = `{{emoji}} S{{emoji}}<script><`
  - bot 访问 /result?emoji&message 触发 RegExp.rightContext 拿 flag
  - flag: SECCON{w0w_yoU_div3d_deeeeeep_iNto_DOMPurify}
  - 题目 5 Deno prototype pollution: validate_identifier 限制 input/output
  - crypto.randomUUID().replaceAll 写文件
  - prototype pollution: "".constructor.prototype.replaceAll = "".constructor.raw
  - input.filename 覆盖 → {{FLAG}} 删除绕过
  - Reflect.has + Object.setPrototypeOf Proxy 链
  - 完整利用: input.filename 注入 + Proxy has trap 泄露 + prototype pollution 写文件
key_payload: SECCON_BASE_URL=/report POST {expr: xssPayload} + contentLength=24 evilHeader q-encoded
one_liner: SECCON CTF 2022 Quals 5 题：qs 1000 参数 limit 绕过 + Flask curl file:// LFI WAF 绕过 + HTTP 请求走私偷 HttpOnly cookie + DOMPurify trustedTypes RegExp.rightContext 泄露 + Deno 原型链污染。
lesson: Express qs 默认 parameterLimit=1000 是经典 HTTP 参数污染绕过；DOMPurify + trustedTypes 仍可通过 RegExp.input/rightContext 泄露过滤前内容；Deno 原型链污染限制 input/output 仍可 Reflect.has 触发 Proxy。
quality: high
---
