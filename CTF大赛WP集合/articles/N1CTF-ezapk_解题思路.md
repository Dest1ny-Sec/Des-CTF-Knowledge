# N1CTF-ezapk 解题思路

> 原文: https://www.ctfiot.com/217460.html
> ID: 217460

public class MainActivity extends AppCompatActivity {
 private ActivityMainBinding binding;

 public native String enc(String str);

 public native String stringFromJNI();

 /* JADX INFO: Access modifiers changed from: protected */
 @Override // androidx.fragment.app.FragmentActivity, androidx.activity.ComponentActivity, androidx.core.app.ComponentActivity, android.app.Activity
 public void onCreate(Bundle bundle) {
 super.onCreate(bundle);
 ActivityMainBinding inflate = ActivityMainBinding.inflate(getLayoutInflater());
 this.binding = inflate;
 setContentView(inflate.getRoot());
 this.binding.CheckButton.setOnClickListener(new View.OnClickListener() { // from class: com.n1ctf2024.ezapk.MainActivity$$ExternalSyntheticLambda0
 @Override // android.view.View.OnClickListener
 public final void onClick(View view) {
 MainActivity.this.m157lambda$onCreate$0$comn1ctf2024ezapkMainActivity(view);
 }
 });
 }

 /* JADX INFO: Access modifiers changed from: package-private */
 /* renamed from: lambda$onCreate$0$com-n1ctf2024-ezapk-MainActivity, reason: not valid java name */
 public /* synthetic */ void m157lambda$onCreate$0$comn1ctf2024ezapkMainActivity(View view) {
 String obj = this.binding.flagText.getText().toString();
 if (obj.startsWith("n1ctf{") && obj.endsWith("}")) {
 if (enc(obj.substring(6, obj.length() - 1)).equals("iRrL63tve+H72wjr/HHiwlVu5RZU9XDcI7A=")) {
 Toast.makeText(this, "Congratulations!", 1).show();
 return;
 } else {
 Toast.makeText(this, "Try again.", 0).show();
 return;
 }
 }
 Toast.makeText(this, "Try again.", 0).show();
 }

 static {
 System.loadLibrary("native2");
 System.loadLibrary("native1");
 }
}

package pkg; 

class Cls { 

 native double f(int i, String s); 

 ... 

}

jdouble Java_pkg_Cls_f__ILjava_lang_String_2 (
 JNIEnv *env, /* interface pointer */
 jobject obj, /* "this" pointer */
 jint i, /* argument #1 */
 jstring s) /* argument #2 */
{
 /* Obtain a C-copy of the Java string */
 const char *str = (*env)->GetStringUTFChars(env, s, 0);

 /* process the string */
 ...

 /* Now we are done with str */
 (*env)->ReleaseStringUTFChars(env, s, str);

 return ...
}

const struct JNINativeInterface ... = {

 NULL,
 NULL,
 NULL,
 NULL,
 GetVersion,

 DefineClass,
 //... 太长省略
 
 GetJavaVM,

 GetStringRegion,
 GetStringUTFRegion,
 //...
 GetObjectRefType
 };

Java.perform(() => {
 const MainActivity = Java.use("com.n1ctf2024.ezapk.MainActivity"); 
 
 MainActivity.enc.implementation = function(input) {
 console.log("enc called with input:", input);
 const result = this.enc(input);
 startHook();
 // startHooklib();
 console.log("enc returned:", result);

 return result;
 };
});

function startHook(){
 const lib_art = Process.findModuleByName('libart.so');
 const symbols = lib_art.enumerateSymbols();
 for (let symbol of symbols) {
 var name = symbol.name;
 if (name.indexOf("art") >= 0) {
 if ((name.indexOf("CheckJNI") == -1) && (name.indexOf("JNI") >= 0)) {
 if (name.indexOf("GetStringUTFChars") >= 0) {
 console.log('start hook', symbol.name);
 Interceptor.attach(symbol.address, {
 onEnter: function (arg) {
 console.log('GetStringUTFChars called from:n' + Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('n') + 'n');
 },
 onLeave: function (retval) {
 console.log('onLeave GetStringUTFChars:', ptr(retval).readCString())
 }
 })
 }
 }
 }
 }
}

// frida -U -f com.n1ctf2024.ezapk -l hook.js
GetStringUTFChars called from:
0x6d55c7117c libnative1.so!0x1b17c
//没有 多点几次 hook和输出在一起 所有你需要hook了 再点几次

ava.perform(() => {
 const MainActivity = Java.use("com.n1ctf2024.ezapk.MainActivity"); 
 
 MainActivity.enc.implementation = function(input) {
 console.log("enc called with input:", input);
 const result = this.enc(input);
 //startHook();
 startHooklib();
 console.log("enc returned:", result);

 return result;
 };
});

function startHooklib(){

 var functions_lib1 = Module.enumerateExports("libnative1.so");
 functions_lib1 = []
 var functions_lib2 = Module.enumerateExports("libnative2.so");
 
 functions_lib1 = functions_lib1.map(item => {
 return { ...item, module: "libnative1.so" }; 
 })

 functions_lib2 = functions_lib2.map(item => {
 return { ...item, module: "libnative2.so" }; 
 })

 var functions = [...functions_lib1,...functions_lib2];

 // {
 // "address": "0x6d56602ca8",
 // "name": "aE7KMLpKuUbB",
 // "type": "function"
 // }
 
 
 functions.forEach(function(func) {
 var moduleBase_lib1 = Module.findBaseAddress(func.module);
 var moduleBase_lib2 = Module.findBaseAddress(func.module);
 if ( moduleBase_lib1 && moduleBase_lib2) {
 var address = func.address
 // console.log("Attaching to function at " + func.module + "!" + func.addr);
 Interceptor.attach(address, {
 onEnter: function(args) {
 console.log(func.module + " function called at " + func.address + " " + func.name);
 },
 onLeave: function(retval) {
 console.log(func.module + " function returned at "+ func.address + " " + func.name);
 }
 });
 } else {
 console.log("Module " + func.module + " not found!");
 }
 });
}

libnative2.so function called at 0x6d55c0306c iusp9aVAyoMI
libnative2.so function returned at 0x6d55c0306c iusp9aVAyoMI
libnative2.so function called at 0x6d55c032c0 SZ3pMtlDTA7Q
libnative2.so function returned at 0x6d55c032c0 SZ3pMtlDTA7Q
libnative2.so function called at 0x6d55c03ab0 UqhYy0F049n5
libnative2.so function returned at 0x6d55c03ab0 UqhYy0F049n5

_BYTE *__fastcall iusp9aVAyoMI(__int64 a1, size_t a2)
{
 size_t i; // [xsp+0h] [xbp-40h]
 _BYTE *v4; // [xsp+8h] [xbp-38h]

 v4 = malloc(a2);
 __memcpy_chk(v4, a1, a2, -1LL);
 for ( i = 0LL; i < a2; ++i )
 v4[i] ^= rand();
 return v4;
}
_BYTE *__fastcall SZ3pMtlDTA7Q(__int64 a1, int a2)
{
 v20[2] = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
 v16 = malloc(a2);
 __memcpy_chk(v16, a1, a2, -1LL);
 v20[1] = 0LL;
 v20[0] = 0LL;
 for ( i = 0; i < 16; ++i )
 *((_BYTE *)v20 + i) = rand();
 // .... 
}

void init()
{
 srand(0x134DAD5u);
}

__int64 sub_1B540()
{
 FILE *v0; // x20
 char *v1; // x0
 unsigned __int64 v2; // x19
 __int64 v3; // x24
 __int64 v4; // x22
 __int64 v5; // x23
 __int64 v6; // x25
 __int64 v7; // x8
 __int64 (**v8)(); // x19
 __int64 result; // x0
 char filename[4096]; // [xsp+8h] [xbp-1008h] BYREF
 __int64 v11; // [xsp+1008h] [xbp-8h]

 v11 = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
 sub_1B6C4(filename);
 v0 = fopen(filename, "r");
 if ( v0 )
 {
 while ( fgets(filename, 4096, v0) )
 {
 if ( strstr(filename, "libnative2.so") )
 {
 v1 = strtok(filename, "-");
 v2 = strtoull(v1, 0LL, 16);
 goto LABEL_6;
 }
 }
 }
 v2 = 0LL;
LABEL_6:
 fclose(v0);
 sub_1B000(v2, &qword_40F70);
 if ( (int)(qword_40FC8 / 0x18uLL) < 1 )
 {
LABEL_10:
 v7 = 0LL;
 }
 else
 {
 v3 = (unsigned int)(qword_40FC8 / 0x18uLL);
 v4 = qword_40F78;
 v5 = unk_40F80;
 v6 = qword_40FC0 + 8;
 while ( strcmp((const char *)(v5 + *(unsigned int *)(v4 + 24LL * *(unsigned int *)(v6 + 4))), "rand") )
 {
 v6 += 24LL;
 if ( !--v3 )
 goto LABEL_10;
 }
 v7 = *(_QWORD *)(v6 - 8);
 }
 v8 = (__int64 (**)())(v7 + v2);
 result = mprotect(v8, 8uLL, 3);
 *v8 = sub_1B140;
 return result;
}

Interceptor.attach(Module.findExportByName('libc.so', 'android_dlopen_ext'), {
 onEnter: function(args) {
 var libraryPath = Memory.readUtf8String(args[0]); // 第一个参数是库路径
 console.log('android_dlopen_ext called to load library: ' + libraryPath);
 if (libraryPath.indexOf('native1.so') !== -1) {
 console.log('Pausing for 10 seconds before loading native1.so...');
 // 暂停 10 秒
 var sleep_string = Module.findExportByName('libc.so', 'sleep');
 var sleep_address = parseInt(sleep_string, 16);
 new NativeFunction(ptr(sleep_address), 'void', ['int'])(20);
 }
 },
 onLeave: function(retval) {
 // 你可以在此修改返回值，或输出其他信息
 console.log('android_dlopen_ext returned: ' + retval);
 }
 });

hook_mprotect()
 var module = Process.findModuleByName('libnative2.so');
 console.log('libnative2.so loaded at: ' + module.base);

function hook_mprotect(){
 // 使用 Frida 钩取 mprotect 函数
Interceptor.attach(Module.findExportByName("libc.so", 'mprotect'), {
 onEnter: function(args) {
 // 获取函数参数
 this.addr = args[0]; // addr 参数：指向内存区域的指针
 this.len = args[1]; // len 参数：内存区域的长度
 this.prot = args[2]; // prot 参数：内存保护标志

 // console.log(this.len.toString());

 // if(this.len.toString() === '0x8'){
 console.log('mprotect called');
 console.log('Address: ' + this.addr,'Length: ' + this.len + 'Protection: ' + this.prot);
 // }
 
 },
 onLeave: function(retval) {
 // 你可以在此修改函数的返回值，或者在返回时打印一些信息
 // console.log('mprotect return value: ' + retval);
 }
});

}

mprotect called
Address: 0x6d55c3c3f8 Length: 0x8Protection: 0x3

看雪ID：SleepAlone

https://bbs.kanxue.com/user-home-9950548.htm

*本文为看雪论坛优秀文章，由 SleepAlone 原创，转载请注明来自看雪社区

# 往期推荐

1、PWN入门-SROP拜师

2、一种apc注入型的Gamarue病毒的变种

3、野蛮fuzz：提升性能

4、关于安卓注入几种方式的讨论，开源注入模块实现

5、2024年KCTF水泊梁山-反混淆

球分享

球点赞

球在看

点击阅读原文查看更多


```
public class MainActivity extends AppCompatActivity {
 private ActivityMainBinding binding;

 public native String enc(String str);

 public native String stringFromJNI();

 /* JADX INFO: Access modifiers changed from: protected */
 @Override // androidx.fragment.app.FragmentActivity, androidx.activity.ComponentActivity, androidx.core.app.ComponentActivity, android.app.Activity
 public void onCreate(Bundle bundle) {
 super.onCreate(bundle);
 ActivityMainBinding inflate = ActivityMainBinding.inflate(getLayoutInflater());
 this.binding = inflate;
 setContentView(inflate.getRoot());
 this.binding.CheckButton.setOnClickListener(new View.OnClickListener() { // from class: com.n1ctf2024.ezapk.MainActivity$$ExternalSyntheticLambda0
 @Override // android.view.View.OnClickListener
 public final void onClick(View view) {
 MainActivity.this.m157lambda$onCreate$0$comn1ctf2024ezapkMainActivity(view);
 }
 });
 }

 /* JADX INFO: Access modifiers changed from: package-private */
 /* renamed from: lambda$onCreate$0$com-n1ctf2024-ezapk-MainActivity, reason: not valid java name */
 public /* synthetic */ void m157lambda$onCreate$0$comn1ctf2024ezapkMainActivity(View view) {
 String obj = this.binding.flagText.getText().toString();
 if (obj.startsWith("n1ctf{") && obj.endsWith("}")) {
 if (enc(obj.substring(6, obj.length() - 1)).equals("iRrL63tve+H72wjr/HHiwlVu5RZU9XDcI7A=")) {
 Toast.makeText(this, "Congratulations!", 1).show();
 return;
 } else {
 Toast.makeText(this, "Try again.", 0).show();
 return;
 }
 }
 Toast.makeText(this, "Try again.", 0).show();
 }

 static {
 System.loadLibrary("native2");
 System.loadLibrary("native1");
 }
}
```



```
package pkg; 

class Cls { 

 native double f(int i, String s); 

 ... 

}
```



```
jdouble Java_pkg_Cls_f__ILjava_lang_String_2 (
 JNIEnv *env, /* interface pointer */
 jobject obj, /* "this" pointer */
 jint i, /* argument #1 */
 jstring s) /* argument #2 */
{
 /* Obtain a C-copy of the Java string */
 const char *str = (*env)->GetStringUTFChars(env, s, 0);

 /* process the string */
 ...

 /* Now we are done with str */
 (*env)->ReleaseStringUTFChars(env, s, str);

 return ...
}
```



```
const struct JNINativeInterface ... = {

 NULL,
 NULL,
 NULL,
 NULL,
 GetVersion,

 DefineClass,
 //... 太长省略
 
 GetJavaVM,

 GetStringRegion,
 GetStringUTFRegion,
 //...
 GetObjectRefType
 };
```



```
Java.perform(() => {
 const MainActivity = Java.use("com.n1ctf2024.ezapk.MainActivity"); 
 
 MainActivity.enc.implementation = function(input) {
 console.log("enc called with input:", input);
 const result = this.enc(input);
 startHook();
 // startHooklib();
 console.log("enc returned:", result);

 return result;
 };
});

function startHook(){
 const lib_art = Process.findModuleByName('libart.so');
 const symbols = lib_art.enumerateSymbols();
 for (let symbol of symbols) {
 var name = symbol.name;
 if (name.indexOf("art") >= 0) {
 if ((name.indexOf("CheckJNI") == -1) && (name.indexOf("JNI") >= 0)) {
 if (name.indexOf("GetStringUTFChars") >= 0) {
 console.log('start hook', symbol.name);
 Interceptor.attach(symbol.address, {
 onEnter: function (arg) {
 console.log('GetStringUTFChars called from:n' + Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('n') + 'n');
 },
 onLeave: function (retval) {
 console.log('onLeave GetStringUTFChars:', ptr(retval).readCString())
 }
 })
 }
 }
 }
 }
}
```



```
// frida -U -f com.n1ctf2024.ezapk -l hook.js
GetStringUTFChars called from:
0x6d55c7117c libnative1.so!0x1b17c
//没有 多点几次 hook和输出在一起 所有你需要hook了 再点几次
```



```
ava.perform(() => {
 const MainActivity = Java.use("com.n1ctf2024.ezapk.MainActivity"); 
 
 MainActivity.enc.implementation = function(input) {
 console.log("enc called with input:", input);
 const result = this.enc(input);
 //startHook();
 startHooklib();
 console.log("enc returned:", result);

 return result;
 };
});

function startHooklib(){

 var functions_lib1 = Module.enumerateExports("libnative1.so");
 functions_lib1 = []
 var functions_lib2 = Module.enumerateExports("libnative2.so");
 
 functions_lib1 = functions_lib1.map(item => {
 return { ...item, module: "libnative1.so" }; 
 })

 functions_lib2 = functions_lib2.map(item => {
 return { ...item, module: "libnative2.so" }; 
 })

 var functions = [...functions_lib1,...functions_lib2];

 // {
 // "address": "0x6d56602ca8",
 // "name": "aE7KMLpKuUbB",
 // "type": "function"
 // }
 
 
 functions.forEach(function(func) {
 var moduleBase_lib1 = Module.findBaseAddress(func.module);
 var moduleBase_lib2 = Module.findBaseAddress(func.module);
 if ( moduleBase_lib1 && moduleBase_lib2) {
 var address = func.address
 // console.log("Attaching to function at " + func.module + "!" + func.addr);
 Interceptor.attach(address, {
 onEnter: function(args) {
 console.log(func.module + " function called at " + func.address + " " + func.name);
 },
 onLeave: function(retval) {
 console.log(func.module + " function returned at "+ func.address + " " + func.name);
 }
 });
 } else {
 console.log("Module " + func.module + " not found!");
 }
 });
}
```



```
libnative2.so function called at 0x6d55c0306c iusp9aVAyoMI
libnative2.so function returned at 0x6d55c0306c iusp9aVAyoMI
libnative2.so function called at 0x6d55c032c0 SZ3pMtlDTA7Q
libnative2.so function returned at 0x6d55c032c0 SZ3pMtlDTA7Q
libnative2.so function called at 0x6d55c03ab0 UqhYy0F049n5
libnative2.so function returned at 0x6d55c03ab0 UqhYy0F049n5
```



```
_BYTE *__fastcall iusp9aVAyoMI(__int64 a1, size_t a2)
{
 size_t i; // [xsp+0h] [xbp-40h]
 _BYTE *v4; // [xsp+8h] [xbp-38h]

 v4 = malloc(a2);
 __memcpy_chk(v4, a1, a2, -1LL);
 for ( i = 0LL; i < a2; ++i )
 v4[i] ^= rand();
 return v4;
}
_BYTE *__fastcall SZ3pMtlDTA7Q(__int64 a1, int a2)
{
 v20[2] = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
 v16 = malloc(a2);
 __memcpy_chk(v16, a1, a2, -1LL);
 v20[1] = 0LL;
 v20[0] = 0LL;
 for ( i = 0; i < 16; ++i )
 *((_BYTE *)v20 + i) = rand();
 // .... 
}
```



```
void init()
{
 srand(0x134DAD5u);
}
```



```
__int64 sub_1B540()
{
 FILE *v0; // x20
 char *v1; // x0
 unsigned __int64 v2; // x19
 __int64 v3; // x24
 __int64 v4; // x22
 __int64 v5; // x23
 __int64 v6; // x25
 __int64 v7; // x8
 __int64 (**v8)(); // x19
 __int64 result; // x0
 char filename[4096]; // [xsp+8h] [xbp-1008h] BYREF
 __int64 v11; // [xsp+1008h] [xbp-8h]

 v11 = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
 sub_1B6C4(filename);
 v0 = fopen(filename, "r");
 if ( v0 )
 {
 while ( fgets(filename, 4096, v0) )
 {
 if ( strstr(filename, "libnative2.so") )
 {
 v1 = strtok(filename, "-");
 v2 = strtoull(v1, 0LL, 16);
 goto LABEL_6;
 }
 }
 }
 v2 = 0LL;
LABEL_6:
 fclose(v0);
 sub_1B000(v2, &qword_40F70);
 if ( (int)(qword_40FC8 / 0x18uLL) < 1 )
 {
LABEL_10:
 v7 = 0LL;
 }
 else
 {
 v3 = (unsigned int)(qword_40FC8 / 0x18uLL);
 v4 = qword_40F78;
 v5 = unk_40F80;
 v6 = qword_40FC0 + 8;
 while ( strcmp((const char *)(v5 + *(unsigned int *)(v4 + 24LL * *(unsigned int *)(v6 + 4))), "rand") )
 {
 v6 += 24LL;
 if ( !--v3 )
 goto LABEL_10;
 }
 v7 = *(_QWORD *)(v6 - 8);
 }
 v8 = (__int64 (**)())(v7 + v2);
 result = mprotect(v8, 8uLL, 3);
 *v8 = sub_1B140;
 return result;
}
```



```
Interceptor.attach(Module.findExportByName('libc.so', 'android_dlopen_ext'), {
 onEnter: function(args) {
 var libraryPath = Memory.readUtf8String(args[0]); // 第一个参数是库路径
 console.log('android_dlopen_ext called to load library: ' + libraryPath);
 if (libraryPath.indexOf('native1.so') !== -1) {
 console.log('Pausing for 10 seconds before loading native1.so...');
 // 暂停 10 秒
 var sleep_string = Module.findExportByName('libc.so', 'sleep');
 var sleep_address = parseInt(sleep_string, 16);
 new NativeFunction(ptr(sleep_address), 'void', ['int'])(20);
 }
 },
 onLeave: function(retval) {
 // 你可以在此修改返回值，或输出其他信息
 console.log('android_dlopen_ext returned: ' + retval);
 }
 });
```



```
hook_mprotect()
 var module = Process.findModuleByName('libnative2.so');
 console.log('libnative2.so loaded at: ' + module.base);

function hook_mprotect(){
 // 使用 Frida 钩取 mprotect 函数
Interceptor.attach(Module.findExportByName("libc.so", 'mprotect'), {
 onEnter: function(args) {
 // 获取函数参数
 this.addr = args[0]; // addr 参数：指向内存区域的指针
 this.len = args[1]; // len 参数：内存区域的长度
 this.prot = args[2]; // prot 参数：内存保护标志

 // console.log(this.len.toString());

 // if(this.len.toString() === '0x8'){
 console.log('mprotect called');
 console.log('Address: ' + this.addr,'Length: ' + this.len + 'Protection: ' + this.prot);
 // }
 
 },
 onLeave: function(retval) {
 // 你可以在此修改函数的返回值，或者在返回时打印一些信息
 // console.log('mprotect return value: ' + retval);
 }
});

}
```



```
mprotect called
Address: 0x6d55c3c3f8 Length: 0x8Protection: 0x3
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1732807489.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1732807490.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1732807491.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1732807492.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1732807493.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1732807494.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1732807496.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1732807496.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1732807497.gif)