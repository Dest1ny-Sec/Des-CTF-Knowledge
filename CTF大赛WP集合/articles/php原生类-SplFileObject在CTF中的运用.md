# php原生类-SplFileObject在CTF中的运用

> 原文: https://www.ctfiot.com/67998.html
> ID: 67998

<?phperror_reporting(0);show_source(__FILE__);
$a = $_GET["a"];$b = $_GET["b"];$c = $_GET["c"];$d = $_GET["d"];$e = $_GET["e"];$f = $_GET["f"];$g = $_GET["g"];
if(preg_match("/Error|ArrayIterator|Exception/i", $a)) { die("hello");}
$class = new $a($b);$str1 = substr($class->$c(),$d,$e);$str2 = substr($class->$c(),$f,$g);$str1($str2);?>

$e = new Exception("systemid");
echo $e->getMessage();

public __construct( string $filename, string $mode = "r", bool $useIncludePath = false, ?resource $context = null)

allow_url_fopen ：onallow_url_include：on

$a = "eval";$b = "phpinfo();";
$a($b);


```
<?phperror_reporting(0);show_source(__FILE__);
$a = $_GET["a"];$b = $_GET["b"];$c = $_GET["c"];$d = $_GET["d"];$e = $_GET["e"];$f = $_GET["f"];$g = $_GET["g"];
if(preg_match("/Error|ArrayIterator|Exception/i", $a)) { die("hello");}
$class = new $a($b);$str1 = substr($class->$c(),$d,$e);$str2 = substr($class->$c(),$f,$g);$str1($str2);?>
$e = new Exception("systemid");
echo $e->getMessage();
public __construct( string $filename, string $mode = "r", bool $useIncludePath = false, ?resource $context = null)
allow_url_fopen ：onallow_url_include：on
$a = "eval";$b = "phpinfo();";
$a($b);
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1667054767.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1667054768.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1667054769.png)