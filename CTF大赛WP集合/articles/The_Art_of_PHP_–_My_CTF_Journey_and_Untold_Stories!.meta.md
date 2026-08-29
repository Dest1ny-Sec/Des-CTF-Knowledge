---
title: The Art of PHP – My CTF Journey and Untold Stories! (Orange Tsai)
contest: 多个
year: 2024
author: Orange Tsai
difficulty: hard
vuln_type: web_unknown
tags: [orange-tsai, php-internals, fsop, csp-bypass, max_input_vars, lfi2rce, phar, laravel-mpdf, scoreboard-hack, real-world-cve]
attack_chain:
- PHP 7.0 Throwable 格式串 bug #71105 配合 new $model() 触发 RCE
- max_input_vars 触发 warning 破坏 header 输出 → CSP 失效
- WordPress maybe_unserialize 自动反序列化 DB 字符串 (Column Truncation 攻击)
- LFI to RCE 二十年进化史 (filter chain → AFR → base64)
- PHAR 反序列化 (Laravel + mPDF 链)
- Hack the Scoreboard: 0day 改 CTF 排行榜
- 多个真实 CVE 复盘 (Microsoft Exchange / SSL VPN / Apache HTTP)
- XCTF / SECCON / DEFCON / cLEMENCy middle-endian 9-bit byte
- One-Gadget / Return-to-CSU / House of Orange / FreeBSD 0day "God Mode"
- Wireshark bug / ELF parser bug 干扰对手
key_payload: new $model() + Throwable $name
one_liner: Orange Tsai 大佬回忆录：PHP 内核 + CTF 二十年 + 真实 CVE + FSOP + LFI 进化 + PHAR 反序列化 + Scoreboard 0day。
lesson: CTF 不只是比赛，是研究交流的社区；Orange Tsai 真实 0day 经验 (Exchange/SSL VPN/Apache) 与 CTF 一脉相承。
quality: high
---
# The Art of PHP – My CTF Journey and Untold Stories! (Orange Tsai)

## 目录
- Prologue: About Me / Hacking Competitions / Being a Pro CTF Gamer / How About PHP Security?
- Main:
  1. Reviving Forgotten Bugs Through CTF
     - 1.1 Formatting Objects for Fun and Profit! (PHP Bug #71105)
     - 1.2 When Security Features Make You Less Secure (CSP + max_input_vars)
  2. One `unserialize()` to Rule Them All
     - 2.1 The "Serialize-Then-Replace" Pattern
     - 2.2 Sleepy Cats Catch No Mice
     - 2.3 The "Holy Grail" of Deserialization Attacks
  3. When Windows Breaks...
     - 3.1 Windows Path Madness
     - 3.2 Let's Make Windows Defender Angry!
  4. New Attacks and Techniques Born in CTFs
     - 4.1 Twenty Years of Evolving LFI to RCE (Level 0/Max/Filter Chain)
     - 4.2 PHAR Deserialization (Laravel + mPDF Kill Chain)
  5. Participants Also Popped 0days
     - 5.1 Hack the Scoreboard!
     - 5.2 From CTF to Real World!

## 关键洞见

### 1. PHP 7.0 Throwable + new $model() = RCE
```php
$model = $_GET['model'];
$object = new $model();
// PHP Bug #71105: $name = "%n%n%n"; $name::doSomething();
```
- 任意对象实例化 + 格式串 = Format-String Oriented Programming (FSOP)
- 1. leak address through PHP errors
- 2. 移动堆指针到 GOT(free)-2
- 3. 部分覆写 GOT[free] → system()

### 2. max_input_vars 破坏 CSP
- `header("Content-Security-Policy: default-src 'none';");`
- `echo $_GET["xss"];` 之前 warning 触发
- 1000+ A=B 参数 → "Warning: Request Startup: Input variables exceeded 1000"
- 警告输出导致 header 已发送 → CSP 失效 → XSS

### 3. WordPress maybe_unserialize 自动反序列化
```php
function maybe_unserialize( $original ) {
    if ( is_serialized( $original ) ) return @unserialize( $original );
    return $original;
}
```
- DB 存字符串自动反序列化
- Column Truncation 攻击 (💩 emoji U+1F4A9) 截断字符串
- 0CTF 2016 "Serialize-Then-Replace" pattern

### 4. LFI to RCE 二十年进化
- Level 0: LFI 经典
- Level 1: AFR (Access File Read)
- Level 2: filter chain (用 base64 编码链)
- Level Max: filter chain ~After Story~ (php://filter 多重编码)

### 5. PHAR 反序列化
- PHAR 文件的 metadata 是序列化对象
- fopen("phar://...") 触发 __destruct
- Laravel + mPDF 链子 kill chain

### 6. Hack the Scoreboard
- 利用 scoreboard 自身的 0day
- 真实 0day: Microsoft Exchange ProxyLogon, SSL VPN, Apache HTTP

## 重要里程碑
- cLEMENCy: 9-bit middle-endian (LegitBS DEFCON Finals)
- House of Orange, Return-to-CSU, One-Gadget
- FreeBSD 0day "God Mode"
- Wireshark bug 干扰对手流量分析
- ELF parser bug 欺骗反汇编工具

## 感想
> "Just learn, hack, enjoy - then repeat!"
> CTF 不仅是比赛，更是推动 PHP/Web 安全的真正动力。
