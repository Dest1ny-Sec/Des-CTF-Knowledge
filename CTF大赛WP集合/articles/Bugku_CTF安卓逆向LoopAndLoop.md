# Bugku CTF安卓逆向LoopAndLoop

> 原文: https://www.ctfiot.com/167027.html
> ID: 167027

来自bugku的LoopAndLoop(阿里CTF)（https://ctf.bugku.com/challenges/detail/id/120.html）。

◆JADX 用于解包和分析APK

◆IDA 7.5 SP3 逆向分析so

拿到压缩包解压，看到文件时APK格式，直接拖到夜神模拟器看看。

简单的测试了下如下：

将APK拖到JADX，找到MainActivity,代码如下：

public class MainActivity extends AppCompatActivity {
 public native int chec(int i, int i2);

 public native String stringFromJNI2(int i);

 /* JADX INFO: Access modifiers changed from: protected */
 @Override // android.support.v7.app.AppCompatActivity, android.support.v4.app.FragmentActivity, android.support.v4.app.BaseFragmentActivityDonut, android.app.Activity
 public void onCreate(Bundle savedInstanceState) {
 super.onCreate(savedInstanceState);
 setContentView(R.layout.activity_main);
 Button button = (Button) findViewById(R.id.button);
 final TextView tv1 = (TextView) findViewById(R.id.textView2);
 final TextView tv2 = (TextView) findViewById(R.id.textView3);
 final EditText ed = (EditText) findViewById(R.id.editText);
 button.setOnClickListener(new View.OnClickListener() { // from class: net.bluelotus.tomorrow.easyandroid.MainActivity.1
 @Override // android.view.View.OnClickListener
 public void onClick(View v) {
 String in_str = ed.getText().toString();
 try {
 int in_int = Integer.parseInt(in_str);
 if (MainActivity.this.check(in_int, 99) == 1835996258) {
 tv1.setText("The flag is:");
 tv2.setText("alictf{" + MainActivity.this.stringFromJNI2(in_int) + "}");
 return;
 }
 tv1.setText("Not Right!");
 } catch (NumberFormatException e) {
 tv1.setText("Not a Valid Integer number");
 }
 }
 });
 }

 @Override // android.app.Activity
 public boolean onCreateOptionsMenu(Menu menu) {
 getMenuInflater().inflate(R.menu.menu_main, menu);
 return true;
 }

 @Override // android.app.Activity
 public boolean onOptionsItemSelected(MenuItem item) {
 int id = item.getItemId();
 if (id == R.id.action_settings) {
 return true;
 }
 return super.onOptionsItemSelected(item);
 }

 public String messageMe(String text) {
 return "LoopOk" + text;
 }

 public int check(int input, int s) {
 return chec(input, s);
 }

 public int check1(int input, int s) {
 int t = input;
 for (int i = 1; i < 100; i++) {
 t += i;
 }
 return chec(t, s);
 }

 public int check2(int input, int s) {
 int t = input;
 if (s % 2 == 0) {
 for (int i = 1; i < 1000; i++) {
 t += i;
 }
 return chec(t, s);
 }
 for (int i2 = 1; i2 < 1000; i2++) {
 t -= i2;
 }
 return chec(t, s);
 }

 public int check3(int input, int s) {
 int t = input;
 for (int i = 1; i < 10000; i++) {
 t += i;
 }
 return chec(t, s);
 }

 static {
 System.loadLibrary("lhm");
 }
}

安卓层面主要的逻辑

int in_int = Integer.parseInt(in_str);
if (MainActivity.this.check(in_int, 99) == 1835996258) {
 tv1.setText("The flag is:");
 tv2.setText("alictf{" + MainActivity.this.stringFromJNI2(in_int) + "}");
 return;
}
tv1.setText("Not Right!");

以上代码逻辑：

◆将输入的字符串转int

◆将int传入check函数，得到的int必须等于1835996258

双击check函数，一层层引用可以找到最终调用的是：

public native int chec(int i, int i2);

JADX保存文件到本地，直接将so文件拖入32位IDA7.5版本，其支持arm F5的版本也行。

查看Exports 页面，下面时部分导出函数：

Name	Address	Ordinal
Java_net_bluelotus_tomorrow_easyandroid_MainActivity_chec	00000E8C	
Java_net_bluelotus_tomorrow_easyandroid_MainActivity_stringFromJNI2	00000F18	
....

双击函数Java_net_bluelotus_tomorrow_easyandroid_MainActivity_chec，直接跳转到汇编代码页面，F5就可得到逻辑代码。简单的修改了下第一个参数的数据类型，代码逻辑看着更清晰了。

int __fastcall Java_net_bluelotus_tomorrow_easyandroid_MainActivity_chec(JNIEnv *jenv, int a2, int t, int s)
{
 jclass v5; // r7
 int result; // r0
 int v10[9]; // [sp+1Ch] [bp-24h] BYREF

 v5 = (*jenv)->FindClass(jenv, "net/bluelotus/tomorrow/easyandroid/MainActivity");
 v10[0] = _JNIEnv::GetMethodID(jenv, v5, "check1", "(II)I");
 v10[1] = _JNIEnv::GetMethodID(jenv, v5, "check2", "(II)I");
 v10[2] = _JNIEnv::GetMethodID(jenv, v5, "check3", "(II)I");
 if ( s - 1 <= 0 )
 result = t;
 else
 result = _JNIEnv::CallIntMethod(jenv, a2, v10[2 * s % 3], t, s - 1);// 
 // 99 * 2 % 3 = 0
 // 98 * 2 % 3 = 1
 // 97 * 2 % 3 = 2
 // 96 * 2 % 3 = 0
 return result;
}

可以看到so文件的代码又去调用了UI层的逻辑。

结合MainActivity中的代码和so中的代码，整理chec函数逻辑如下：

int chec(int t, int s);

int check1(int input, int s)
{
 int t = input;
 for (int i = 1; i < 100; i++)
 {
 t += i;
 }
 return chec(t, s);
}

int check2(int input, int s)
{
 int t = input;
 if (s % 2 == 0)
 {
 for (int i = 1; i < 1000; i++)
 {
 t += i;
 }
 return chec(t, s);
 }
 for (int i2 = 1; i2 < 1000; i2++)
 {
 t -= i2;
 }
 return chec(t, s);
}

int check3(int input, int s)
{
 int t = input;
 for (int i = 1; i < 10000; i++)
 {
 t += i;
 }
 return chec(t, s);
}

typedef int (*pfn_check)(int, int);

pfn_check check_fns[3] = {
 check1, check2, check3};

int chec(int t, int s)
{
 if (s - 1 <= 0)
 {
 /* code */
 return t;
 }
 else
 {
 return check_fns[2 * s % 3](t, s - 1);
 }
}

既然是个int值，从0开始穷举就可以了。但是这绝对不是唯一办法。

先看看前0-99的输出吧!

for ( i = 0; i < 100; i++)
 {
 /* code */
 printf("[%08d] chec(%d,99) = %d n",i,i,chec(i,99));
 }

结果

[00000000] chec(0,99) = 1599503850
[00000001] chec(1,99) = 1599503851
[00000002] chec(2,99) = 1599503852
[00000003] chec(3,99) = 1599503853
[00000004] chec(4,99) = 1599503854
[00000005] chec(5,99) = 1599503855
[00000006] chec(6,99) = 1599503856
[00000007] chec(7,99) = 1599503857
[00000008] chec(8,99) = 1599503858
[00000009] chec(9,99) = 1599503859
[00000010] chec(10,99) = 1599503860
[00000011] chec(11,99) = 1599503861
[00000012] chec(12,99) = 1599503862
[00000013] chec(13,99) = 1599503863
[00000014] chec(14,99) = 1599503864
[00000015] chec(15,99) = 1599503865
[00000016] chec(16,99) = 1599503866
[00000017] chec(17,99) = 1599503867
[00000018] chec(18,99) = 1599503868
[00000019] chec(19,99) = 1599503869
[00000020] chec(20,99) = 1599503870
[00000021] chec(21,99) = 1599503871
[00000022] chec(22,99) = 1599503872
[00000023] chec(23,99) = 1599503873
[00000024] chec(24,99) = 1599503874
.....

可以看出是结果是线性的。首先我们会想到2分法。

unsigned int low, high, value, cur, t,v,i;

 value = 1835996258;
 low = 0;
 high = 0xffffffff;

 cur = low + (high - low)/2;
 printf("value = %08x n",value);
 i = 0;
 while (1)
 {
 v = chec(cur, 99) ;
 printf("[%08d] cur = %08x v = %08x low = %08x high = %08x n", i, cur,v,low,high);
 i++;
 if (v > value)
 {
 high = cur;
 cur = low + (high - low) / 2;
 continue;
 }

 if (v < value)
 {
 low = cur;
 cur = low + (high - low) / 2;
 continue;
 }

 //printf("chec(low,99) = %d n", chec(low, 99));
 //printf("chec(high,99) = %d n", chec(high, 99));
 printf("value = %d n", value);
 printf("chec(%d,99) = %d n", cur,chec(cur,99));
 flag(cur);
 break;
 }

2分法计算如下：

[00000023] cur = 0e1896ff v = 6d6f14e9 low = 0e1895ff high = 0e1897ff
[00000024] cur = 0e18967f v = 6d6f1469 low = 0e1895ff high = 0e1896ff
[00000025] cur = 0e18963f v = 6d6f1429 low = 0e1895ff high = 0e18967f
[00000026] cur = 0e18965f v = 6d6f1449 low = 0e18963f high = 0e18967f
[00000027] cur = 0e18966f v = 6d6f1459 low = 0e18965f high = 0e18967f
[00000028] cur = 0e189677 v = 6d6f1461 low = 0e18966f high = 0e18967f
[00000029] cur = 0e18967b v = 6d6f1465 low = 0e189677 high = 0e18967f
[00000030] cur = 0e189679 v = 6d6f1463 low = 0e189677 high = 0e18967b
[00000031] cur = 0e189678 v = 6d6f1462 low = 0e189677 high = 0e189679
value = 1835996258
chec(236492408,99) = 1835996258

通过仔细观察也可以看出i增长1，计算结果也增长1。这样可以直接算出想要的i值。

i = 1835996258 - chec(0,99);
printf("%d n",i);

计算结果。

236492408

找到so中函数stringFromJNI2，方法同上。

jstring __fastcall Java_net_bluelotus_tomorrow_easyandroid_MainActivity_stringFromJNI2(JNIEnv *a1, int a2, int a3)
{
 int v3; // r1
 JNIEnv v4; // r2
 char v6; // [sp+8h] [bp-50h]
 char v7; // [sp+Ch] [bp-4Ch]
 char v8; // [sp+10h] [bp-48h]
 int v9; // [sp+24h] [bp-34h]
 char str[12]; // [sp+28h] [bp-30h] BYREF

 v8 = a3 / 1000 % 10;
 v9 = a3 / 10000 % 10;
 v6 = a3 % 10;
 str[0] = v8 + v6 * v9;
 v7 = a3 / 1000000 % 10;
 v3 = a3 / 100 % 10;
 str[1] = v9 * v7 + 10 * v3 + 3;
 str[2] = 10 * (v8 + v9);
 str[3] = v9 * v7;
 str[4] = 19 * (a3 / 100000 % 10) + 2;
 str[5] = v6 * v7 + 1;
 str[6] = v6 * v7;
 str[7] = 12 * v3;
 str[9] = 12 * v3 + 3;
 str[8] = str[2] + v8;
 v4 = *a1;
 str[10] = 2 * (v9 * v7 + 10 * v3 - 37);
 str[11] = 0;
 return v4->NewStringUTF(a1, str);
}

剔除无用参数得到c语言逻辑。

void flag(int a3)
{
 int v3; // r1
 char v6; // [sp+8h] [bp-50h]
 char v7; // [sp+Ch] [bp-4Ch]
 char v8; // [sp+10h] [bp-48h]
 int v9; // [sp+24h] [bp-34h]
 char str[12]; // [sp+28h] [bp-30h] BYREF

 v8 = a3 / 1000 % 10;
 v9 = a3 / 10000 % 10;
 v6 = a3 % 10;
 str[0] = v8 + v6 * v9;
 v7 = a3 / 1000000 % 10;
 v3 = a3 / 100 % 10;
 str[1] = v9 * v7 + 10 * v3 + 3;
 str[2] = 10 * (v8 + v9);
 str[3] = v9 * v7;
 str[4] = 19 * (a3 / 100000 % 10) + 2;
 str[5] = v6 * v7 + 1;
 str[6] = v6 * v7;
 str[7] = 12 * v3;
 str[9] = 12 * v3 + 3;
 str[8] = str[2] + v8;

 str[10] = 2 * (v9 * v7 + 10 * v3 - 37);
 str[11] = 0;
 printf("flag:alictf{%s}", str);
}

最后得到flag如下：

236492408
flag:alictf{Jan6N100p3r}

看雪ID：zhenwo

https://bbs.kanxue.com/user-home-396123.htm

*本文为看雪论坛优秀文章，由 zhenwo 原创，转载请注明来自看雪社区

# 往期推荐

1、ELF文件脱壳纪事

2、Glibc-2.35下对tls_dtor_list的利用详解

3、对旅行APP的检测以及参数计算分析【Simplesign篇】

4、2023强网杯warmup题解

5、Directory Opus 13.2 逆向分析

6、Pwn-oneday题目解析

球分享

球点赞

球在看

点击阅读原文查看更多


```
public class MainActivity extends AppCompatActivity {
 public native int chec(int i, int i2);

 public native String stringFromJNI2(int i);

 /* JADX INFO: Access modifiers changed from: protected */
 @Override // android.support.v7.app.AppCompatActivity, android.support.v4.app.FragmentActivity, android.support.v4.app.BaseFragmentActivityDonut, android.app.Activity
 public void onCreate(Bundle savedInstanceState) {
 super.onCreate(savedInstanceState);
 setContentView(R.layout.activity_main);
 Button button = (Button) findViewById(R.id.button);
 final TextView tv1 = (TextView) findViewById(R.id.textView2);
 final TextView tv2 = (TextView) findViewById(R.id.textView3);
 final EditText ed = (EditText) findViewById(R.id.editText);
 button.setOnClickListener(new View.OnClickListener() { // from class: net.bluelotus.tomorrow.easyandroid.MainActivity.1
 @Override // android.view.View.OnClickListener
 public void onClick(View v) {
 String in_str = ed.getText().toString();
 try {
 int in_int = Integer.parseInt(in_str);
 if (MainActivity.this.check(in_int, 99) == 1835996258) {
 tv1.setText("The flag is:");
 tv2.setText("alictf{" + MainActivity.this.stringFromJNI2(in_int) + "}");
 return;
 }
 tv1.setText("Not Right!");
 } catch (NumberFormatException e) {
 tv1.setText("Not a Valid Integer number");
 }
 }
 });
 }

 @Override // android.app.Activity
 public boolean onCreateOptionsMenu(Menu menu) {
 getMenuInflater().inflate(R.menu.menu_main, menu);
 return true;
 }

 @Override // android.app.Activity
 public boolean onOptionsItemSelected(MenuItem item) {
 int id = item.getItemId();
 if (id == R.id.action_settings) {
 return true;
 }
 return super.onOptionsItemSelected(item);
 }

 public String messageMe(String text) {
 return "LoopOk" + text;
 }

 public int check(int input, int s) {
 return chec(input, s);
 }

 public int check1(int input, int s) {
 int t = input;
 for (int i = 1; i < 100; i++) {
 t += i;
 }
 return chec(t, s);
 }

 public int check2(int input, int s) {
 int t = input;
 if (s % 2 == 0) {
 for (int i = 1; i < 1000; i++) {
 t += i;
 }
 return chec(t, s);
 }
 for (int i2 = 1; i2 < 1000; i2++) {
 t -= i2;
 }
 return chec(t, s);
 }

 public int check3(int input, int s) {
 int t = input;
 for (int i = 1; i < 10000; i++) {
 t += i;
 }
 return chec(t, s);
 }

 static {
 System.loadLibrary("lhm");
 }
}
```



```
int in_int = Integer.parseInt(in_str);
if (MainActivity.this.check(in_int, 99) == 1835996258) {
 tv1.setText("The flag is:");
 tv2.setText("alictf{" + MainActivity.this.stringFromJNI2(in_int) + "}");
 return;
}
tv1.setText("Not Right!");
```



```
public native int chec(int i, int i2);
```



```
Name	Address	Ordinal
Java_net_bluelotus_tomorrow_easyandroid_MainActivity_chec	00000E8C	
Java_net_bluelotus_tomorrow_easyandroid_MainActivity_stringFromJNI2	00000F18	
....
```



```
int __fastcall Java_net_bluelotus_tomorrow_easyandroid_MainActivity_chec(JNIEnv *jenv, int a2, int t, int s)
{
 jclass v5; // r7
 int result; // r0
 int v10[9]; // [sp+1Ch] [bp-24h] BYREF

 v5 = (*jenv)->FindClass(jenv, "net/bluelotus/tomorrow/easyandroid/MainActivity");
 v10[0] = _JNIEnv::GetMethodID(jenv, v5, "check1", "(II)I");
 v10[1] = _JNIEnv::GetMethodID(jenv, v5, "check2", "(II)I");
 v10[2] = _JNIEnv::GetMethodID(jenv, v5, "check3", "(II)I");
 if ( s - 1 <= 0 )
 result = t;
 else
 result = _JNIEnv::CallIntMethod(jenv, a2, v10[2 * s % 3], t, s - 1);// 
 // 99 * 2 % 3 = 0
 // 98 * 2 % 3 = 1
 // 97 * 2 % 3 = 2
 // 96 * 2 % 3 = 0
 return result;
}
```



```
int chec(int t, int s);

int check1(int input, int s)
{
 int t = input;
 for (int i = 1; i < 100; i++)
 {
 t += i;
 }
 return chec(t, s);
}

int check2(int input, int s)
{
 int t = input;
 if (s % 2 == 0)
 {
 for (int i = 1; i < 1000; i++)
 {
 t += i;
 }
 return chec(t, s);
 }
 for (int i2 = 1; i2 < 1000; i2++)
 {
 t -= i2;
 }
 return chec(t, s);
}

int check3(int input, int s)
{
 int t = input;
 for (int i = 1; i < 10000; i++)
 {
 t += i;
 }
 return chec(t, s);
}

typedef int (*pfn_check)(int, int);

pfn_check check_fns[3] = {
 check1, check2, check3};

int chec(int t, int s)
{
 if (s - 1 <= 0)
 {
 /* code */
 return t;
 }
 else
 {
 return check_fns[2 * s % 3](t, s - 1);
 }
}
```



```
for ( i = 0; i < 100; i++)
 {
 /* code */
 printf("[%08d] chec(%d,99) = %d n",i,i,chec(i,99));
 }
```



```
[00000000] chec(0,99) = 1599503850
[00000001] chec(1,99) = 1599503851
[00000002] chec(2,99) = 1599503852
[00000003] chec(3,99) = 1599503853
[00000004] chec(4,99) = 1599503854
[00000005] chec(5,99) = 1599503855
[00000006] chec(6,99) = 1599503856
[00000007] chec(7,99) = 1599503857
[00000008] chec(8,99) = 1599503858
[00000009] chec(9,99) = 1599503859
[00000010] chec(10,99) = 1599503860
[00000011] chec(11,99) = 1599503861
[00000012] chec(12,99) = 1599503862
[00000013] chec(13,99) = 1599503863
[00000014] chec(14,99) = 1599503864
[00000015] chec(15,99) = 1599503865
[00000016] chec(16,99) = 1599503866
[00000017] chec(17,99) = 1599503867
[00000018] chec(18,99) = 1599503868
[00000019] chec(19,99) = 1599503869
[00000020] chec(20,99) = 1599503870
[00000021] chec(21,99) = 1599503871
[00000022] chec(22,99) = 1599503872
[00000023] chec(23,99) = 1599503873
[00000024] chec(24,99) = 1599503874
.....
```



```
unsigned int low, high, value, cur, t,v,i;

 value = 1835996258;
 low = 0;
 high = 0xffffffff;

 cur = low + (high - low)/2;
 printf("value = %08x n",value);
 i = 0;
 while (1)
 {
 v = chec(cur, 99) ;
 printf("[%08d] cur = %08x v = %08x low = %08x high = %08x n", i, cur,v,low,high);
 i++;
 if (v > value)
 {
 high = cur;
 cur = low + (high - low) / 2;
 continue;
 }

 if (v < value)
 {
 low = cur;
 cur = low + (high - low) / 2;
 continue;
 }

 //printf("chec(low,99) = %d n", chec(low, 99));
 //printf("chec(high,99) = %d n", chec(high, 99));
 printf("value = %d n", value);
 printf("chec(%d,99) = %d n", cur,chec(cur,99));
 flag(cur);
 break;
 }
```



```
[00000023] cur = 0e1896ff v = 6d6f14e9 low = 0e1895ff high = 0e1897ff
[00000024] cur = 0e18967f v = 6d6f1469 low = 0e1895ff high = 0e1896ff
[00000025] cur = 0e18963f v = 6d6f1429 low = 0e1895ff high = 0e18967f
[00000026] cur = 0e18965f v = 6d6f1449 low = 0e18963f high = 0e18967f
[00000027] cur = 0e18966f v = 6d6f1459 low = 0e18965f high = 0e18967f
[00000028] cur = 0e189677 v = 6d6f1461 low = 0e18966f high = 0e18967f
[00000029] cur = 0e18967b v = 6d6f1465 low = 0e189677 high = 0e18967f
[00000030] cur = 0e189679 v = 6d6f1463 low = 0e189677 high = 0e18967b
[00000031] cur = 0e189678 v = 6d6f1462 low = 0e189677 high = 0e189679
value = 1835996258
chec(236492408,99) = 1835996258
```



```
i = 1835996258 - chec(0,99);
printf("%d n",i);
```



```
236492408
```



```
jstring __fastcall Java_net_bluelotus_tomorrow_easyandroid_MainActivity_stringFromJNI2(JNIEnv *a1, int a2, int a3)
{
 int v3; // r1
 JNIEnv v4; // r2
 char v6; // [sp+8h] [bp-50h]
 char v7; // [sp+Ch] [bp-4Ch]
 char v8; // [sp+10h] [bp-48h]
 int v9; // [sp+24h] [bp-34h]
 char str[12]; // [sp+28h] [bp-30h] BYREF

 v8 = a3 / 1000 % 10;
 v9 = a3 / 10000 % 10;
 v6 = a3 % 10;
 str[0] = v8 + v6 * v9;
 v7 = a3 / 1000000 % 10;
 v3 = a3 / 100 % 10;
 str[1] = v9 * v7 + 10 * v3 + 3;
 str[2] = 10 * (v8 + v9);
 str[3] = v9 * v7;
 str[4] = 19 * (a3 / 100000 % 10) + 2;
 str[5] = v6 * v7 + 1;
 str[6] = v6 * v7;
 str[7] = 12 * v3;
 str[9] = 12 * v3 + 3;
 str[8] = str[2] + v8;
 v4 = *a1;
 str[10] = 2 * (v9 * v7 + 10 * v3 - 37);
 str[11] = 0;
 return v4->NewStringUTF(a1, str);
}
```



```
void flag(int a3)
{
 int v3; // r1
 char v6; // [sp+8h] [bp-50h]
 char v7; // [sp+Ch] [bp-4Ch]
 char v8; // [sp+10h] [bp-48h]
 int v9; // [sp+24h] [bp-34h]
 char str[12]; // [sp+28h] [bp-30h] BYREF

 v8 = a3 / 1000 % 10;
 v9 = a3 / 10000 % 10;
 v6 = a3 % 10;
 str[0] = v8 + v6 * v9;
 v7 = a3 / 1000000 % 10;
 v3 = a3 / 100 % 10;
 str[1] = v9 * v7 + 10 * v3 + 3;
 str[2] = 10 * (v8 + v9);
 str[3] = v9 * v7;
 str[4] = 19 * (a3 / 100000 % 10) + 2;
 str[5] = v6 * v7 + 1;
 str[6] = v6 * v7;
 str[7] = 12 * v3;
 str[9] = 12 * v3 + 3;
 str[8] = str[2] + v8;

 str[10] = 2 * (v9 * v7 + 10 * v3 - 37);
 str[11] = 0;
 printf("flag:alictf{%s}", str);
}
```



```
236492408
flag:alictf{Jan6N100p3r}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/7-1710205167.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1710205168.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/2-1710205168.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1710205169.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/2-1710205170.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1710205170.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/3-1710205171.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/10-1710205171.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/3-1710205172.gif)