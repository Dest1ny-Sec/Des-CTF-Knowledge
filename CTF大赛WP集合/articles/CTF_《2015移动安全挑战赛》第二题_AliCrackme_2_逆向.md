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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/2-1689080731.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/0-1689080731.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/5-1689080732.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/1-1689080732.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/2-1689080733.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/9-1689080733.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/3-1689080733.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/2-1689080734.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/4-1689080734.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/07/3-1689080734.png)