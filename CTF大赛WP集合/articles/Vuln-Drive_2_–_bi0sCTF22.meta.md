---
title: Vuln-Drive 2 – bi0sCTF22
contest: bi0sCTF 2022
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [smuggling_path, http_request_split, waf_bypass, sqlite_sqli, ssrf_internal, flag_header_xprohacker, file_get_contents, custom_http_in_post]
attack_chain: docker-compose 三层架构 frontend/waf/app → view.php?file=chdir 后 file_get_contents 读文件 (txt 后缀限制) → upload path= 路径穿越 + file content 是构造的 HTTP 请求 (含 X-pro-hacker: Pro-hacker + flag: gimme + Token header) → 通过 smuggling 绕过 waf 直达 app → SQLite SQL 注入 user=a',substr((select*from flag),{},1));-- → 盲注爆破 flag
key_payload: X-pro-hacker: Pro-hacker + flag: gimme + Content-Type: application/x-www-form-urlencoded + user=a',substr((select*from flag),{},1));-- + Token: 16 字符
one_liner: bi0sCTF 2022 Vuln-Drive 2 WAF 绕过，HTTP smuggling 把含 SQL 注入的 HTTP 请求塞进 multipart 上传，绕过 waf 直达内网 app。
lesson: 经典 "HTTP smuggling via POST body"：上传文件内容实际是合法 HTTP 请求，被后端 view.php 转发到内网 app，绕开 WAF 检查。
quality: high
---
