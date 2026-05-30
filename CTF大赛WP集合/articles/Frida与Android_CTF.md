# Frida与Android CTF

> 原文: https://www.ctfiot.com/31515.html
> ID: 31515

E

N

D

关

于

我

们

Tide安全团队正式成立于2019年1月，是新潮信息旗下以互联网攻防技术研究为目标的安全团队，团队致力于分享高质量原创文章、开源安全工具、交流安全技术，研究方向覆盖网络攻防、系统安全、Web安全、移动终端、安全开发、物联网/工控安全/AI安全等多个领域。

团队作为“省级等保关键技术实验室”先后与哈工大、齐鲁银行、聊城大学、交通学院等多个高校名企建立联合技术实验室。团队公众号自创建以来，共发布原创文章370余篇，自研平台达到26个，目有15个平台已开源。此外积极参加各类线上、线下CTF比赛并取得了优异的成绩。如有对安全行业感兴趣的小伙伴可以踊跃加入或关注我们。


```
var CONTEXT = null;

function getObjClassName(obj) {
 if (!jclazz) {
 var jclazz = Java.use("java.lang.Class");
 }
 if (!jobj) {
 var jobj = Java.use("java.lang.Object");
 }
 return jclazz.getName.call(jobj.getClass.call(obj));
}

function hookReturn() {
 Java.perform(function () {
 Java.use("com.kanxue.pediy1.VVVVV").VVVV.implementation = function (context, str) {
 var result = this.VVVV(context, str)
 console.log("context,str,result => ", context, str, result);
 console.log("context className is => ", getObjClassName(context));
 CONTEXT = context;
 return true;
 }
 })
}
function invoke() {
 Java.perform(function () {
 //console.log("CONTEXT IS => ",CONTEXT)
 var MainActivity = null;
 Java.choose("com.kanxue.pediy1.MainActivity", {
 onMatch: function (instance) {
 MainActivity = instance;
 },
 onComplete: function () { }
 })
 var CONTEXT2 = Java.use("com.kanxue.pediy1.MainActivity$1").$new(MainActivity);
 var javaString = Java.use("java.lang.String").$new("12345");
 for (var x = 0; x < (99999 + 1); x++) {
 var result = Java.use("com.kanxue.pediy1.VVVVV").VVVV(CONTEXT2, String(x));
 console.log("now x is => ", String(x))
 if (result) {
 console.log("found result is => ", String(x))
 break;
 }
 }
 })

}

function main() {
 hookReturn()
}
```



```
function invoke2() {
 Java.perform(function () {
 Java.enumerateClassLoaders({
 onMatch: function (loader) {
 try {
 if (loader.findClass("com.kanxue.pediy1.VVVVV")) {
 console.log("Successfully found loader")
 console.log(loader);
 Java.classFactory.loader = loader;
 }
 }
 catch (error) {
 console.log("find error:" + error)
 }
 },
 onComplete: function () {
 console.log("end1")
 }
 })
 var javaString = Java.use("java.lang.String").$new("12345");
 for (var x = 0; x < (99999 + 1); x++) {
 var result = Java.use("com.kanxue.pediy1.VVVVV").VVVV(String(x)); 
 console.log("now x is => ", String(x))
 if (result) {
 console.log("found result is => ", String(x))
 break;
 }
 }
 })
}

function main() {

}
setImmediate(main)
```



```
function invoke2() {
 Java.perform(function () {
 var MainActivity = null;
 Java.choose("com.kanxue.pediy1.MainActivity",{
 onMatch:function(instance){
 MainActivity = instance;
 },
 onComplete:function(){}
 })
 var loader1 = null;
 var loader2 = null;
 Java.enumerateClassLoaders({
 onMatch: function (loader) {
 try {
 if (loader.findClass("com.kanxue.pediy1.VVVVV")) {
 console.log("Successfully found loader")
 console.log(loader);
 loader2 = loader;
 Java.classFactory.loader = loader2;
 }else if(loader.findClass("com.kanxue.pediy1.MainActivity")){console.log("Successfully found loader")
 console.log(loader);
 loader1 = loader;
 }else{
 }
 }
 catch (error) {
 console.log("find error:" + error)
 }
 },
 onComplete: function () {
 console.log("end1")
 }
 })
 var javaString = Java.use("java.lang.String").$new("12345");
 for (var x = 0; x < (99999 + 1); x++) {
 var result1 = MainActivity.stringFromJNI(String(100000 - x));
 var result2 = Java.use("com.kanxue.pediy1.VVVVV").VVVV(String(result1)); 
 console.log("now x is => ", String(x))
 if (result2) {
 console.log("found result2 is => ", String(100000 - x))
 break;
 }
 }
 })
}
function main() {
}
setImmediate(main)
```



```
frida -U -f com.kanxue.pediy1 -l /Users/tale/Downloads/20220317/111.js --no-pause
```



```
function replaceKill(){
 var kill_addr = Module.findExportByName("libc.so", "kill");
 Interceptor.replace(kill_addr,new NativeCallback(function(arg0,arg1){
 console.log("arg0=> ",arg0)
 console.log("arg1=> ",arg1)
 },"int",['int','int']))
}

function main() {
 replaceKill();
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/3-1647911921.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/8-1647911922.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/10-1647911923.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/5-1647911924.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/6-1647911924.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/6-1647911925.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/0-1647911925.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/8-1647911926.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/10-1647911926.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/0-1647911927.jpeg)