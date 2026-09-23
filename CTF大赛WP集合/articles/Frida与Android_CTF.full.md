---
title: Frida 与 Android CTF
contest: 看雪/Tide 安全 (kanxue/pediy1)
year: 2022
difficulty: medium
vuln_type:
- reverse
- misc_unknown
tags:
- Frida
- Android
- JNI
- Java.perform
- Java.choose
- enumerateClassLoaders
- Interceptor.replace
- kill
- anti-debug
attack_chain:
- frida -U -f 目标包 spawn 注入
- Java.perform hook 关键方法 VVVV(context, str)
- Java.choose 找 MainActivity 实例注入伪 context
- Java.enumerateClassLoaders 找正确 classloader
- 枚举 0-99999 爆破正确输入拿 true 返回
- Interceptor.replace(libc.so!kill) 绕反调试
key_payload: Java.use("com.kanxue.pediy1.VVVVV").VVVV(CONTEXT2, String(x))
one_liner: Frida hook + 爆破绕过 Android JNI 校验 + kill 拦截绕反调试
lesson: Android CTF 高频工具是 Frida；自定义 classloader 需 enumerateClassLoaders 切换；JNI 反调试常见用 kill(pid, 0) 检测 tracerpid
quality: high
full_path: Frida与Android_CTF.full.md
meta_path: Frida与Android_CTF.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: Frida 与 Android CTF。Frida hook + 爆破绕过 Android JNI 校验 + kill 拦截绕反调试。关键路径：frida -U -f 目标包 spawn 注入 → Java.perform hook 关键方法 VVVV(context, str) → Java.choose 找 MainActivity 实例注入伪 context。经验：Android CT...
category: reverse
subcategory: reverse
subcategories:
- reverse
- misc_other
tools_used:
- Frida
- Java
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/31515.html
reasoning_chain:
- 触发点：frida -U -f 目标包 spawn 注入 → 假设：必须 Java.perform 注入
- 动作：Java.use('com.kanxue.pediy1.VVVVV').VVVV(CONTEXT, str) → 触发点：关键方法 hook
- 假设：VVVV 返回 bool → 假设：必须爆破正确输入 → 动作：0-99999 枚举
- 假设：MainActivity 实例获取真 context → 动作：Java.choose('com.kanxue.pediy1.MainActivity')
- 假设：自定义 classloader → 动作：Java.enumerateClassLoaders() 找正确
- 假设：JNI 反调试用 kill(pid, 0) 检测 tracerpid → 动作：Interceptor.replace(libc.so!kill)
- 假设：返回 0 绕过 → 动作：var kill_func = new NativeFunction(Module.findExportByName('libc.so','kill'),'int',['int','int']);
- Interceptor.replace(kill_func, new NativeCallback(function(pid, sig){ return 0; },'int',['int','int']));
- 观察：tracerpid 检测失效 → 反调试绕过 → 完成
failed_attempts:
- 试图直接 frida --attach 注入 → 失败：必须 spawn 早注入
- 试图用 Frida 直接改 process tracerpid → 失败：必须 hook kill 系统调用
- 试图 attach debugger 调试 → 失败：触发反调试
key_observations:
- frida -U -f 是 spawn 模式最早 hook 时机
- Java.choose 找实例 + Java.enumerateClassLoaders 找正确 loader 是自定 classloader 关键
- Interceptor.replace(NativeFunction) 是 hook native 函数核心
- kill(pid, 0) 检测 tracerpid 是 Android 反调试经典手法
- 0-99999 爆破常见于简单校验函数
prerequisites:
- Frida spawn / attach 模式区别
- Java.use / Java.choose / Java.enumerateClassLoaders
- NativeFunction / Interceptor.replace
- Android JNI 反调试原理（kill tracerpid）
---
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
function invoke2() {
 Java.perform(function () {
 var MainActivity = null;
 Java.choose("com.kanxue.pediy1.MainActivity",{
 onMatch:
function(instance){
 MainActivity = instance;
 },
 onComplete:
function(){}
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
frida -U -f com.kanxue.pediy1 -l /Users/tale/Downloads/20220317/111.js --no-pause
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