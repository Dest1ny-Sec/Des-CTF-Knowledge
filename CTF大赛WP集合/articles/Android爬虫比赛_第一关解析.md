# Android爬虫比赛  第一关解析

> 原文: https://www.ctfiot.com/92066.html
> ID: 92066

一

环境

frida 12.8.20

python 3.8.10

jadx-gui-1.2.0

fiddler

二

实战步骤

1、安装APP，来到第一关，翻页时抓包。

jadx打开APP ，根据page= 查找到 com.yuanrenxue.match2022.fragment.challenge.ChallengeOneFragment 类。

此处有sign函数，很大几率为翻页调用函数，hook当前函数查看 this.page 和 oooOO0O.OooO00o().longValue()的值：

function hook_ChallengeOneFragment(){ //访问内部类函数 Java.perform(function(){ var InnerClasses = Java.use("com.yuanrenxue.match2022.fragment.challenge.ChallengeOneFragment"); // console.log(InnerClasses); InnerClasses.lambda$initListeners$2.overload('o00O000.OooOO0O').implementation = function(age){ console.log("this.page.value:",this.page.value);//查看page的值 console.log("age.OooO00o().longValue() :",age.OooO00o().longValue());//查看值 console.log("age:",age)//查看参数 var res = this.lambda$initListeners$2(age)//运行函数 console.log("res:",res,"type:",res.$className);//返回值和返回值类型 var Map = Java.use('retrofit2.adapter.rxjava2.BodyObservable');//根据返回值类型创建对象 var NewP = Java.cast(res, Map); //将返回值转成相应类型 console.log("NewP:",NewP.toString());//输出返回值 return res; }; });}

分析代码：

StringBuilder 为可变字符串。

根据代码得出 sb的值为页码+时间戳 “page=21652931584″。

再次hook Sign函数查看参数和返回值并与fiddler对比。

function hook_SignClass(){ //访问内部类函数 Java.perform(function(){ // 访问内部类时，在当前类后加$符号，后跟内部类名 var InnerClasses = Java.use("com.yuanrenxue.match2022.security.Sign"); // console.log(InnerClasses); InnerClasses.sign.overload('[B').implementation = function(arge1){ console.log("参数和参数类型:",arge1,arge1.$className);//数组类型一般会返回null console.log("数组类型转码：",JSON.stringify(arge1));//数组类型可尝试使用json解析 var res = this.sign(arge1);//运行函数 // return true; console.log("res",res);//返回值 return res; }; });}

此时已经可以断定，这个Sign就是翻页的加密函数 。

根据jadx反汇编代码：

new Sign().sign(sb.toString().getBytes(StandardCharsets.UTF_8))

我们用python实现一下。

time_ = '1652932157's = 'page=1' + time_print("s:",s)bArr = [x for x in bytearray(s,'utf_8')]print("bArr:",bArr) #s: page=11652932157#bArr: [112, 97, 103, 101, 61, 49, 49, 54, 53, 50, 57, 51, 50, 49, 53, 55]

此时直接调用sign生成加密参数，抓取100页的值相加得出flag：

#!/usr/bin/env python# -*- coding: utf-8 -*- import fridaimport requestsimport time #发送接收frida_js信息def on_message(message, data): if message['type'] == 'send': print("[*] {0}".format(message['payload'])) else: print(message) js = open('hook.js', 'r', encoding='utf8').read() #读取frida脚本 session = frida.get_remote_device().attach('com.yuanrenxue.match2022')#根据包名启动APP script = session.create_script(js)script.on('message', on_message)script.load()#加载frida脚本 if __name__ == '__main__': time_ = int(time.time())#获取世家戳 header2 = { 'Accept-Language':'zh-CN,zh;q=0.8', 'User-Agent':'Mozilla/5.0 (Linux; U; Android 10; zh-cn; Mi9 Pro 5G Build/QKQ1.190825.002) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1', 'Content-Type':'application/x-www-form-urlencoded', 'Content-Length':'57', 'Host':'appmatch.yuanrenxue.com', 'Connection':'Keep-Alive', 'Accept-Encoding':'gzip', 'Cache-Control':'no-cache', } count = 0 #记数 for i in range(1,101): s = f'page={i}' + str(time_) bArr = [x for x in bytearray(s,'utf_8')] res = script.exports.callsecretfunctionedy(bArr) #调用frida_js函数获取加密参数 payload = { 'page': str(i), 'sign': res, 't': time_, } r = requests.post("https://appmatch.yuanrenxue.com/app1", data=payload, headers = header2, verify = False ) data = r.json()['data'] for v in data: count += int(v['value']) print("flag count:",count)

var result;function callDYFun(bArr) { //定义导出函数 Java.perform(function () { console.log("bArr:",bArr); var ss = Java.use('com.yuanrenxue.match2022.security.Sign'); var str = Java.use("java.lang.String"); var res = str.$new(ss.$new().sign(bArr)); result = str.valueOf(res) console.log("result:",result); }); return result;//返回值给python}rpc.exports = { callsecretfunctionedy: callDYFun,};

类中有两个函数一模一样lambda$initListeners$2和lambda$initListeners$0 。

经测试调用的是 lambda$initListeners$2。

看雪ID：网络枭红

https://bbs.pediy.com/user-home-385739.htm

*本文由看雪论坛 网络枭红 原创，转载请注明来自看雪社区

https://www.kanxue.com/book-leaflet-85.htm

# 往期推荐

1.CVE-2022-21882提权漏洞学习笔记

2.wibu证书 – 初探

3.win10 1909逆向之APIC中断和实验

4.EMET下EAF机制分析以及模拟实现

5.sql注入学习分享

6.V8 Array.prototype.concat函数出现过的issues和他们的POC们

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
一
环境
```



```
二
实战步骤
```



```
function hook_ChallengeOneFragment(){ //访问内部类函数 Java.perform(function(){ var InnerClasses = Java.use("com.yuanrenxue.match2022.fragment.challenge.ChallengeOneFragment"); // console.log(InnerClasses); InnerClasses.lambda$initListeners$2.overload('o00O000.OooOO0O').implementation = function(age){ console.log("this.page.value:",this.page.value);//查看page的值 console.log("age.OooO00o().longValue() :",age.OooO00o().longValue());//查看值 console.log("age:",age)//查看参数 var res = this.lambda$initListeners$2(age)//运行函数 console.log("res:",res,"type:",res.$className);//返回值和返回值类型 var Map = Java.use('retrofit2.adapter.rxjava2.BodyObservable');//根据返回值类型创建对象 var NewP = Java.cast(res, Map); //将返回值转成相应类型 console.log("NewP:",NewP.toString());//输出返回值 return res; }; });}
```



```
function hook_SignClass(){ //访问内部类函数 Java.perform(function(){ // 访问内部类时，在当前类后加$符号，后跟内部类名 var InnerClasses = Java.use("com.yuanrenxue.match2022.security.Sign"); // console.log(InnerClasses); InnerClasses.sign.overload('[B').implementation = function(arge1){ console.log("参数和参数类型:",arge1,arge1.$className);//数组类型一般会返回null console.log("数组类型转码：",JSON.stringify(arge1));//数组类型可尝试使用json解析 var res = this.sign(arge1);//运行函数 // return true; console.log("res",res);//返回值 return res; }; });}
```



```
new Sign().sign(sb.toString().getBytes(StandardCharsets.UTF_8))
```



```
time_ = '1652932157's = 'page=1' + time_print("s:",s)bArr = [x for x in bytearray(s,'utf_8')]print("bArr:",bArr) #s: page=11652932157#bArr: [112, 97, 103, 101, 61, 49, 49, 54, 53, 50, 57, 51, 50, 49, 53, 55]
```



```
#!/usr/bin/env python# -*- coding: utf-8 -*- import fridaimport requestsimport time #发送接收frida_js信息def on_message(message, data): if message['type'] == 'send': print("[*] {0}".format(message['payload'])) else: print(message) js = open('hook.js', 'r', encoding='utf8').read() #读取frida脚本 session = frida.get_remote_device().attach('com.yuanrenxue.match2022')#根据包名启动APP script = session.create_script(js)script.on('message', on_message)script.load()#加载frida脚本 if __name__ == '__main__': time_ = int(time.time())#获取世家戳 header2 = { 'Accept-Language':'zh-CN,zh;q=0.8', 'User-Agent':'Mozilla/5.0 (Linux; U; Android 10; zh-cn; Mi9 Pro 5G Build/QKQ1.190825.002) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1', 'Content-Type':'application/x-www-form-urlencoded', 'Content-Length':'57', 'Host':'appmatch.yuanrenxue.com', 'Connection':'Keep-Alive', 'Accept-Encoding':'gzip', 'Cache-Control':'no-cache', } count = 0 #记数 for i in range(1,101): s = f'page={i}' + str(time_) bArr = [x for x in bytearray(s,'utf_8')] res = script.exports.callsecretfunctionedy(bArr) #调用frida_js函数获取加密参数 payload = { 'page': str(i), 'sign': res, 't': time_, } r = requests.post("https://appmatch.yuanrenxue.com/app1", data=payload, headers = header2, verify = False ) data = r.json()['data'] for v in data: count += int(v['value']) print("flag count:",count)
```



```
var result;function callDYFun(bArr) { //定义导出函数 Java.perform(function () { console.log("bArr:",bArr); var ss = Java.use('com.yuanrenxue.match2022.security.Sign'); var str = Java.use("java.lang.String"); var res = str.$new(ss.$new().sign(bArr)); result = str.valueOf(res) console.log("result:",result); }); return result;//返回值给python}rpc.exports = { callsecretfunctionedy: callDYFun,};
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673662910.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1673662911.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673662912.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673662912.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673662912.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1673662913.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673662913.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1673662913.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1673662913.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673662914.jpeg)