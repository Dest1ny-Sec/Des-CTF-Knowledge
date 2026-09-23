---
title: CTF 《2015 移动安全挑战赛》第二题 AliCrackme_2 逆向
contest: 移动安全挑战赛
year: 2015
difficulty: easy
vuln_type: reverse
tags:
- Android so 静态
- while 循环匹配
- aWojiushidaan
- Frida hook fgets
- TracerPid:t0
- hook kill
- mprop ro.debuggable
- AS 64端口12346
- 看雪 行简
- 2015经典
attack_chain:
- 'so 静态: while 循环匹配用户输入 vs 硬编码 aWojiushidaan'
- '反调试: Frida hook fgets 改 TracerPid: 为 TracerPid:t0'
- Frida hook kill 直接返回 0
- 启动 android_server64 -p 12346 root 调试
- mprop 工具 ro.debuggable 1 改属性
key_payload: '''while 循环字符比较 / aWojiushidaan / Frida hook fgets 改 TracerPid / Frida hook kill / mprop ro.debuggable 1 / android_server64 12346'''
one_liner: AliCrackme_2 — Android so 静态分析 while 循环匹配 aWojiushidaan + Frida hook fgets 改 TracerPid:t0 + hook kill + mprop ro.debuggable 1 + android_server64 -p12346 调试。
lesson: Android 经典逆向三件套:静态分析硬编码字符串 + Frida hook 改 TracerPid + mprop 改 ro.debuggable;2015 年风格是 so 字符比较。
quality: medium
full_path: CTF_《2015移动安全挑战赛》第二题_AliCrackme_2_逆向.full.md
meta_path: CTF_《2015移动安全挑战赛》第二题_AliCrackme_2_逆向.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: CTF 《2015 移动安全挑战赛》第二题 AliCrackme_2 逆向。AliCrackme_2 — Android so 静态分析 while 循环匹配 aWojiushidaan + Frida hook fgets 改 TracerPid:t0 + hook kill + mprop ro.debuggable 1 + android_server64 -p12346 调试。。关键...
category: reverse
subcategory: reverse
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/124720.html
reasoning_chain:
- 触发点：apk 文件 + 反编译查看 so 库 + while 循环硬编码字符串比较 → 假设：用户输入与 'aWojiushidaan' 字符匹配
- 动作：IDA 看 libcrackme.so 主函数 → 观察：fgets + 字符串比较 + while 循环 = 静态硬编码
- 假设：硬编码字符串就是密码 → 动作：直接提交 aWojiushidaan → 观察：flag 通过
- 触发点：App 检测是否被调试（TracerPid） → 假设：用 Frida hook TracerPid 改 0
- 动作：Frida hook fgets 在写入时改 TracerPid:t0 → 观察：调试检测不过
- 假设：进程内调 kill 防调试 → 动作：Frida hook kill 直接 return 0 → 观察：调试进程不死
- 下一步：mprop 工具把 ro.debuggable 改 1 → 动作：mprop ro.debuggable 1 → 观察：apk 重新签名能调试
- 动作：启动 android_server64 -p 12346 root 转发端口 → 观察：IDA 远程 attach 调试 → 完成
failed_attempts:
- 试图直接 unzip 看 classes.dex → 失败：关键逻辑在 libcrackme.so 不在 dex
- 试图用 jdb 而非 IDA 调试 → 失败：Native 层必须 IDA + android_server64
- 试图脱壳 dex → 失败：题目无壳，是 2015 年经典 Native 反调试
key_observations:
- 2015 年风格 Android Crackme = so 静态分析 + 反调试三件套（TracerPid/kill/ro.debuggable）
- Frida hook fgets 时改内存 TracerPid 是经典反反调试
- mprop 工具能离线修改 prop，无需重启
- android_server64 (ARM64 调试代理) 必须用 root 权限 + 端口 12346 默认
- 硬编码字符串匹配 = 最简单的 2015 反向题套路
prerequisites:
- IDA 静态分析 so 库（libcrackme.so 反汇编）
- Frida hook fgets/kill 反调试框架
- mprop 工具 + Android prop 修改
- android_server64 启动 + adb forward 12346
- Android 反调试三件套原理（TracerPid/ro.debuggable/kill）
---
# CTF 《2015移动安全挑战赛》第二题 AliCrackme_2 逆向

> 原文: https://www.ctfiot.com/124720.html
> ID: 124720

一

前言

二

入手点定位

三

so 静态分析

v5 = (*env)->GetStringUTFChars(env, password, 0); // v5为用户输入的密码
v6 = off_628C; // off_628C：aWojiushidaan
while ( 1 ) // while循环判断用户输入内容
{
 v7 = *v6; // v6 指针所指向的地址中的字符，赋值给 v7 变量
 if ( v7 != *v5 ) // 检查 v7 和 v5 变量中存储的字符是否相等。如果不相等，则跳出循环。
 break;
 ++v6; // 这两行代码将 v6 和 v5 的值递增，使它们指向下一个字符。
 ++v5;
 v8 = 1;
 if ( !v7 ) // 如果 v7 中的字符为空（即字符串结束符），则返回 v8 的值。
 return v8;
 }
 return 0; // 如果前面的循环没有提前退出并且未返回 v8 的值，则说明字符串不匹配，函数返回 0 表示不相等。
}

四

反调试方式确认

root@phone:/data/local/tmp # ./as_64 -p12346

function Tracepid() {
 console.warn(".............")
 var fgetsPtr = Module.findExportByName("libc.so", "fgets");
 var fgets = new NativeFunction(fgetsPtr, 'pointer', ['pointer', 'int', 'pointer']);
 Interceptor.replace(fgetsPtr, new NativeCallback(function (buffer, size, fp) {
 var retval = fgets(buffer, size, fp);
 var bufstr = Memory.readUtf8String(buffer);
 if (bufstr.indexOf("TracerPid:") > -1) {
 Memory.writeUtf8String(buffer, "TracerPid:t0");
 }
 return retval;
 }, 'pointer', ['pointer', 'int', 'pointer']));
 var killptr = Module.findExportByName("libc.so", "kill");
 var kill = new NativeFunction(fgetsPtr, 'int', ['int', 'int']);
 Interceptor.replace(killptr, new NativeCallback(function (pid,sig) {
 console.log("kill")
 return 0;
 }, 'int', ['int', 'int']));
}

五

so 动态分析

adb push mprop /data/local/tmp # 将下载好的 mprop 工具放入 /data/local/tmp 当中
adb shell
su
cat default.prop | grep debug # 查看default.prop里面的配置值，此处是 0
getprop ro.debuggable # 获取ro.debuggable 此处应该是 0
cd /data/local/tmp
chmod 777 mprop # 修改权限
./mprop ro.debuggable 1 # 修改 ro.debuggable 1 的值为 1
cat default.prop | grep debug # 查看default.prop里面的配置值，此处是应该还是 0
getprop ro.debuggable # 获取 ro.debuggable 此处应该是 1

看雪ID：行简

https://bbs.kanxue.com/user-home-945390.htm

*本文为看雪论坛优秀文章，由 行简 原创，转载请注明来自看雪社区

# 往期推荐

1、在 Windows下搭建LLVM 使用环境

2、深入学习smali语法

3、安卓加固脱壳分享

4、Flutter 逆向初探

5、一个简单实践理解栈空间转移

6、记一次某盾手游加固的脱壳与修复

球分享

球点赞

球在看


```
一
前言
二
入手点定位
三
so 静态分析
v5 = (*env)->GetStringUTFChars(env, password, 0); // v5为用户输入的密码
v6 = off_628C; // off_628C：aWojiushidaan
while ( 1 ) // while循环判断用户输入内容
{
 v7 = *v6; // v6 指针所指向的地址中的字符，赋值给 v7 变量
 if ( v7 != *v5 ) // 检查 v7 和 v5 变量中存储的字符是否相等。如果不相等，则跳出循环。
 break;
 ++v6; // 这两行代码将 v6 和 v5 的值递增，使它们指向下一个字符。
 ++v5;
 v8 = 1;
 if ( !v7 ) // 如果 v7 中的字符为空（即字符串结束符），则返回 v8 的值。
 return v8;
 }
 return 0; // 如果前面的循环没有提前退出并且未返回 v8 的值，则说明字符串不匹配，函数返回 0 表示不相等。
}
四
反调试方式确认
root@phone:/data/local/tmp # ./as_64 -p12346
function Tracepid() {
 console.warn(".............")
 var fgetsPtr = Module.findExportByName("libc.so", "fgets");
 var fgets = new NativeFunction(fgetsPtr, 'pointer', ['pointer', 'int', 'pointer']);
 Interceptor.replace(fgetsPtr, new NativeCallback(function (buffer, size, fp) {
 var retval = fgets(buffer, size, fp);
 var bufstr = Memory.readUtf8String(buffer);
 if (bufstr.indexOf("TracerPid:") > -1) {
 Memory.writeUtf8String(buffer, "TracerPid:t0");
 }
 return retval;
 }, 'pointer', ['pointer', 'int', 'pointer']));
 var killptr = Module.findExportByName("libc.so", "kill");
 var kill = new NativeFunction(fgetsPtr, 'int', ['int', 'int']);
 Interceptor.replace(killptr, new NativeCallback(function (pid,sig) {
 console.log("kill")
 return 0;
 }, 'int', ['int', 'int']));
}
五
so 动态分析
adb push mprop /data/local/tmp # 将下载好的 mprop 工具放入 /data/local/tmp 当中
adb shell
su
cat default.prop | grep debug # 查看default.prop里面的配置值，此处是 0
getprop ro.debuggable # 获取ro.debuggable 此处应该是 0
cd /data/local/tmp
chmod 777 mprop # 修改权限
./mprop ro.debuggable 1 # 修改 ro.debuggable 1 的值为 1
cat default.prop | grep debug # 查看default.prop里面的配置值，此处是应该还是 0
getprop ro.debuggable # 获取 ro.debuggable 此处应该是 1
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