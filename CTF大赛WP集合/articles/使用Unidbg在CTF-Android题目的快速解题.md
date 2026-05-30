# 使用Unidbg在CTF-Android题目的快速解题

> 原文: https://www.ctfiot.com/163430.html
> ID: 163430

遇到了一道android题目，最近学了Unidbg，做完这题，发现成了Unidbg的铁杆粉丝，真的是很方便，我再也不用辛辛苦苦动态分析so啦。

aapt dump badging apk名字

int __fastcall Java_an_droid_j_MainActivity_j(JNIEnv *a1)
{
 int i; // r1
 int v2; // r0
 int v3; // r0
 char v5[32]; // [sp-40h] [bp-70h] BYREF
 _BYTE v6[36]; // [sp-20h] [bp-50h] BYREF
 JNIEnv *v7; // [sp+4h] [bp-2Ch]
 int *v8; // [sp+8h] [bp-28h]
 int v9; // [sp+Ch] [bp-24h]
 int v10; // [sp+10h] [bp-20h]
 _BYTE *v11; // [sp+14h] [bp-1Ch]
 int v12; // [sp+1Ch] [bp-14h] BYREF

 v8 = &v12;
 v7 = a1;
 for ( i = -1178200092; ; i = 52119689 )
 {
 do
 {
 v3 = i;
 i = 1445388760;
 }
 while ( v3 == -1178200092 );
 if ( v3 == 52119689 )
 break;
 v11 = v6;
 strcpy(v5, "FlagLostHelpMeGetItBack");
 v10 = 30;
 v9 = 97;
 v5[29] = 0;
 *(_WORD *)&v5[27] = 0;
 v5[24] = 0;
 *(_WORD *)&v5[25] = 0;
 v5[30] = 80;
 qmemcpy(v6, v5, 0x1Eu);
 v2 = (int)(*v7)->NewStringUTF(v7, v6);
 *v8 = v2;
 }
 return *v8;
}

public String func_j(){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object = dvmClass.newObject(null);
 DvmObject<?> object1 = object.callJniMethodObject(emulator, "j()Ljava/lang/String;");
 return object1.getValue().toString();
 }

public int func_p(int args){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object=dvmClass.newObject(null);
 int object1=object.callJniMethodInt(emulator,"p(I)I",args);
 return object1;
 }

jstring __fastcall Java_an_droid_j_MainActivity_init(JNIEnv *a1, jobject a2, int a3)

public int func_p(int args){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object=dvmClass.newObject(null);
 int object1=object.callJniMethodInt(emulator,"p(I)I",args);
 return object1;
 }

int zygote = 1357024680;
 long start =System.currentTimeMillis();
 for(int i=0;i<99999;i++){
 zygote =mylesson4.func_p(zygote);
 }
 System.out.println("99999次后的zygote的值："+zygote);

lesson4 mylesson4=new lesson4(apkFilePath,soFilePath,apkProcessname);
 int temp = 1738911344;
 System.out.println("flag{" + mylesson4.func_init(temp) + "}");

package com.lesson4;

import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;

// 导入通用且标准的类库
import com.github.unidbg.linux.android.dvm.AbstractJni;
import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.array.ByteArray;
import com.github.unidbg.linux.android.dvm.jni.ProxyDvmObject;
import com.github.unidbg.memory.Memory;
import com.lession1.oasis;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class lesson4 extends AbstractJni{
 private final AndroidEmulator emulator; //android模拟器
 private final VM vm;//vm虚拟机
 private final Module module;
 private final Memory memory;
 private final DalvikModule dm;
 //将该类封装起来，以后直接套用模板
 public lesson4(String apkFilePath,String soFilePath,String apkProcessname) throws IOException {
 // 创建模拟器实例,进程名建议依照实际进程名填写，可以规避针对进程名的校验
 emulator = AndroidEmulatorBuilder.for32Bit().setProcessName(apkProcessname).build();

 //.addBackendFactory(new DynarmicFactory((true))) 下面会创建一个快速模拟器实例，加载速度快，但是某些特性不支持
 //.setProcessName()设置进程名，避免原进程对进程名进行检验

 // 获取模拟器的内存操作接口
 memory = emulator.getMemory();
 // 设置系统类库解析 支持19和23，因为在main/resources/android只集成了两个版本
 memory.setLibraryResolver(new AndroidResolver(23));

 // 创建Android虚拟机,传入APK,可以过掉签名校验，路径比如："unidbg-android\src\test\java\com\lesson1\123.apk"
 vm = emulator.createDalvikVM(new File(apkFilePath));
 vm.setVerbose(false); // 打印日志，会在调用初始化JNI_onload打印一些信息，默认：false

 // 加载目标SO
 dm = vm.loadLibrary(new File(soFilePath), true); // 加载so到虚拟内存，第二个参数：是否需要初始化
 //获取本SO模块的句柄
 module = dm.getModule();

 vm.setJni(this); //设置Jni，防止报错
 //创建完后，需要调用JNI_onload函数
 //dm.callJNI_OnLoad(emulator); // 调用JNI OnLoad，进行动态注册某些函数。如果都是静态注册，那就不用调用这个函数

 //本次样本连个 JNI_onLoad都没有

 }

 //这个是模拟 bak_libj.so的j方法
 public String func_j(String method,double args){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object=dvmClass.newObject(null);
 //获得一个DvmObject对象
 //DvmObject object= ProxyDvmObject.createObject(vm,"an.droid.j"); //因为我创建的类全包名和原app不一样，所以换一种方式来寻找到对应的类对象
 DvmObject object1=object.callJniMethodObject(emulator,method,args);
 String return_value=object1.getValue().toString();
 return return_value;

 }

 //下面两个是模拟 libj.so的init、p和j方法
 //均使用了动态获得dvmclass的方式
 public int func_p(int args){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object=dvmClass.newObject(null);
 int object1=object.callJniMethodInt(emulator,"p(I)I",args);
 return object1;
 }

 public String func_init(int args){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object=dvmClass.newObject(null);
 //方法签名在对应的so文件中推导出，其实不难的，看参数和看返回值
 DvmObject<?> object1 = object.callJniMethodObject(emulator, "init(I)Ljava/lang/String;", args);
 return object1.getValue().toString();
 }
 public String func_j(){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object = dvmClass.newObject(null);
 DvmObject<?> object1 = object.callJniMethodObject(emulator, "j()Ljava/lang/String;");
 return object1.getValue().toString();
 }

 //创建一个main函数
 public static void main(String[] args) throws IOException {
 // 1、需要调用的so文件所在路径
 String soFilePath = "unidbg-android/src/test/java/com/lesson4/libj.so";
 // 2、APK的路径
 String apkFilePath="unidbg-android/src/test/java/com/lesson4/a.apk";
 // 3、apk进程名
 String apkProcessname="an.droid.j";

 lesson4 mylesson4=new lesson4(apkFilePath,soFilePath,apkProcessname);
 int temp = 1738911344;
 System.out.println("flag{" + mylesson4.func_init(temp) + "}");

// int zygote = 1357024680;
// long start =System.currentTimeMillis();
// for(int i=0;i<99999;i++){
// zygote =mylesson4.func_p(zygote);
// }
// System.out.println("99999次后的zygote的值："+zygote);

 }

}

看雪ID：NYSECbao

https://bbs.kanxue.com/user-home-971547.htm

*本文为看雪论坛优秀文章，由 NYSECbao 原创，转载请注明来自看雪社区

# 往期推荐

1、区块链智能合约逆向-合约创建-调用执行流程分析

2、在Windows平台使用VS2022的MSVC编译LLVM16

3、神挡杀神——揭开世界第一手游保护nProtect的神秘面纱

4、为什么在ASLR机制下DLL文件在不同进程中加载的基址相同

5、2022QWB final RDP

6、华为杯研究生国赛 adv_lua

球分享

球点赞

球在看


```
aapt dump badging apk名字
int __fastcall Java_an_droid_j_MainActivity_j(JNIEnv *a1)
{
 int i; // r1
 int v2; // r0
 int v3; // r0
 char v5[32]; // [sp-40h] [bp-70h] BYREF
 _BYTE v6[36]; // [sp-20h] [bp-50h] BYREF
 JNIEnv *v7; // [sp+4h] [bp-2Ch]
 int *v8; // [sp+8h] [bp-28h]
 int v9; // [sp+Ch] [bp-24h]
 int v10; // [sp+10h] [bp-20h]
 _BYTE *v11; // [sp+14h] [bp-1Ch]
 int v12; // [sp+1Ch] [bp-14h] BYREF

 v8 = &v12;
 v7 = a1;
 for ( i = -1178200092; ; i = 52119689 )
 {
 do
 {
 v3 = i;
 i = 1445388760;
 }
 while ( v3 == -1178200092 );
 if ( v3 == 52119689 )
 break;
 v11 = v6;
 strcpy(v5, "FlagLostHelpMeGetItBack");
 v10 = 30;
 v9 = 97;
 v5[29] = 0;
 *(_WORD *)&v5[27] = 0;
 v5[24] = 0;
 *(_WORD *)&v5[25] = 0;
 v5[30] = 80;
 qmemcpy(v6, v5, 0x1Eu);
 v2 = (int)(*v7)->NewStringUTF(v7, v6);
 *v8 = v2;
 }
 return *v8;
}
public String func_j(){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object = dvmClass.newObject(null);
 DvmObject<?> object1 = object.callJniMethodObject(emulator, "j()Ljava/lang/String;");
 return object1.getValue().toString();
 }
public int func_p(int args){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object=dvmClass.newObject(null);
 int object1=object.callJniMethodInt(emulator,"p(I)I",args);
 return object1;
 }
jstring __fastcall Java_an_droid_j_MainActivity_init(JNIEnv *a1, jobject a2, int a3)
public int func_p(int args){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object=dvmClass.newObject(null);
 int object1=object.callJniMethodInt(emulator,"p(I)I",args);
 return object1;
 }
int zygote = 1357024680;
 long start =System.currentTimeMillis();
 for(int i=0;i<99999;i++){
 zygote =mylesson4.func_p(zygote);
 }
 System.out.println("99999次后的zygote的值："+zygote);
lesson4 mylesson4=new lesson4(apkFilePath,soFilePath,apkProcessname);
 int temp = 1738911344;
 System.out.println("flag{" + mylesson4.func_init(temp) + "}");
package com.lesson4;

import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;

// 导入通用且标准的类库
import com.github.unidbg.linux.android.dvm.AbstractJni;
import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.array.ByteArray;
import com.github.unidbg.linux.android.dvm.jni.ProxyDvmObject;
import com.github.unidbg.memory.Memory;
import com.lession1.oasis;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class lesson4 extends AbstractJni{
 private final AndroidEmulator emulator; //android模拟器
 private final VM vm;//vm虚拟机
 private final Module module;
 private final Memory memory;
 private final DalvikModule dm;
 //将该类封装起来，以后直接套用模板
 public lesson4(String apkFilePath,String soFilePath,String apkProcessname) throws IOException {
 // 创建模拟器实例,进程名建议依照实际进程名填写，可以规避针对进程名的校验
 emulator = AndroidEmulatorBuilder.for32Bit().setProcessName(apkProcessname).build();

 //.addBackendFactory(new DynarmicFactory((true))) 下面会创建一个快速模拟器实例，加载速度快，但是某些特性不支持
 //.setProcessName()设置进程名，避免原进程对进程名进行检验

 // 获取模拟器的内存操作接口
 memory = emulator.getMemory();
 // 设置系统类库解析 支持19和23，因为在main/resources/android只集成了两个版本
 memory.setLibraryResolver(new AndroidResolver(23));

 // 创建Android虚拟机,传入APK,可以过掉签名校验，路径比如："unidbg-android\src\test\java\com\lesson1\123.apk"
 vm = emulator.createDalvikVM(new File(apkFilePath));
 vm.setVerbose(false); // 打印日志，会在调用初始化JNI_onload打印一些信息，默认：false

 // 加载目标SO
 dm = vm.loadLibrary(new File(soFilePath), true); // 加载so到虚拟内存，第二个参数：是否需要初始化
 //获取本SO模块的句柄
 module = dm.getModule();

 vm.setJni(this); //设置Jni，防止报错
 //创建完后，需要调用JNI_onload函数
 //dm.callJNI_OnLoad(emulator); // 调用JNI OnLoad，进行动态注册某些函数。如果都是静态注册，那就不用调用这个函数

 //本次样本连个 JNI_onLoad都没有

 }

 //这个是模拟 bak_libj.so的j方法
 public String func_j(String method,double args){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object=dvmClass.newObject(null);
 //获得一个DvmObject对象
 //DvmObject object= ProxyDvmObject.createObject(vm,"an.droid.j"); //因为我创建的类全包名和原app不一样，所以换一种方式来寻找到对应的类对象
 DvmObject object1=object.callJniMethodObject(emulator,method,args);
 String return_value=object1.getValue().toString();
 return return_value;

 }

 //下面两个是模拟 libj.so的init、p和j方法
 //均使用了动态获得dvmclass的方式
 public int func_p(int args){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object=dvmClass.newObject(null);
 int object1=object.callJniMethodInt(emulator,"p(I)I",args);
 return object1;
 }

 public String func_init(int args){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object=dvmClass.newObject(null);
 //方法签名在对应的so文件中推导出，其实不难的，看参数和看返回值
 DvmObject<?> object1 = object.callJniMethodObject(emulator, "init(I)Ljava/lang/String;", args);
 return object1.getValue().toString();
 }
 public String func_j(){
 DvmClass dvmClass=vm.resolveClass("an.droid.j.MainActivity");
 DvmObject<?> object = dvmClass.newObject(null);
 DvmObject<?> object1 = object.callJniMethodObject(emulator, "j()Ljava/lang/String;");
 return object1.getValue().toString();
 }

 //创建一个main函数
 public static void main(String[] args) throws IOException {
 // 1、需要调用的so文件所在路径
 String soFilePath = "unidbg-android/src/test/java/com/lesson4/libj.so";
 // 2、APK的路径
 String apkFilePath="unidbg-android/src/test/java/com/lesson4/a.apk";
 // 3、apk进程名
 String apkProcessname="an.droid.j";

 lesson4 mylesson4=new lesson4(apkFilePath,soFilePath,apkProcessname);
 int temp = 1738911344;
 System.out.println("flag{" + mylesson4.func_init(temp) + "}");

// int zygote = 1357024680;
// long start =System.currentTimeMillis();
// for(int i=0;i<99999;i++){
// zygote =mylesson4.func_p(zygote);
// }
// System.out.println("99999次后的zygote的值："+zygote);

 }

}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/1-1708596894.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/7-1708596894.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/4-1708596895.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/9-1708596895.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/9-1708596896.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1708596896.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/0-1708596897.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/1-1708596897.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1708596898.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/0-1708596898.jpeg)