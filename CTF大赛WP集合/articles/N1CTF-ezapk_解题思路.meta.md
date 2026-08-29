---
title: N1CTF 2024 ezapk 解题思路 (Android + JNI Frida hook)
contest: N1CTF
year: 2024
difficulty: hard
vuln_type: reverse
tags: [Android APK, JNI native1/native2, Frida hook, JNI 字符串转换, 内存读写]
attack_chain: |
  1. 题目: N1CTF 2024 ezapk — Android APK + native1.so + native2.so
  2. MainActivity:
     - binding.CheckButton.onClick: 读 flagText → startsWith("n1ctf{") && endsWith("}")
     - 提取中间部分 substring(6, length-1) → enc("...").equals("iRrL63tve+H72wjr/HHiwlVu5RZU9XDcI7A=")
     - enc 是 native 方法 (native1 + native2)
  3. Frida hook:
     - Java.use("com.n1ctf2024.ezapk.MainActivity")
     - MainActivity.enc.implementation = function(input) { ... return 自定义逻辑 }
  4. JNI 内存模型:
     - JNIEnv *env, jobject obj, jint i, jstring s
     - GetStringUTFChars(env, s, 0) 拿 C 字符串
     - ReleaseStringUTFChars(env, s, str) 释放
  5. 解法: Frida hook 后直接调 enc 试所有可能输入 + 比对 "iRrL63tve+H72wjr/HHiwlVu5RZU9XDcI7A=" → 还原原始 flag
key_payload: |
  // Frida hook:
  Java.perform(() => {
      const MainActivity = Java.use("com.n1ctf2024.ezapk.MainActivity");
      MainActivity.enc.implementation = function(input) {
          // 自定义逻辑或直接观察
          return this.enc(input);
      };
  });
  
  // 验证:
  // n1ctf{<中间部分>} substring(6, length-1) → enc() == "iRrL63tve+H72wjr/HHiwlVu5RZU9XDcI7A="
one_liner: N1CTF 2024 ezapk: Android APK + native1/native2 JNI, Frida hook MainActivity.enc 观察明文/密文对比还原 flag。
lesson: |
  - JNI 标准符号: Java_<package>_<class>_<method>
  - Android loadLibrary("native1") + loadLibrary("native2") 链式加载
  - Frida Java.use + .implementation 拦截 native 方法
  - JNI GetStringUTFChars 拿 jstring, ReleaseStringUTFChars 释放
  - 目标密文 "iRrL63tve+H72wjr/HHiwlVu5RZU9XDcI7A=" 是 base64, 可能是 AES/DES/RSA
quality: medium
---

# N1CTF 2024 ezapk 解题思路

> 来源: ctfiot.com 217460

## MainActivity (Java)

```java
public class MainActivity extends AppCompatActivity {
    private ActivityMainBinding binding;
    public native String enc(String str);
    public native String stringFromJNI();

    public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        ActivityMainBinding inflate = ActivityMainBinding.inflate(getLayoutInflater());
        this.binding = inflate;
        setContentView(inflate.getRoot());
        this.binding.CheckButton.setOnClickListener(view -> {
            String obj = this.binding.flagText.getText().toString();
            if (obj.startsWith("n1ctf{") && obj.endsWith("}")) {
                if (enc(obj.substring(6, obj.length() - 1))
                    .equals("iRrL63tve+H72wjr/HHiwlVu5RZU9XDcI7A=")) {
                    Toast.makeText(this, "Congratulations!", 1).show();
                } else {
                    Toast.makeText(this, "Try again.", 0).show();
                }
            }
        });
    }

    static {
        System.loadLibrary("native2");
        System.loadLibrary("native1");
    }
}
```

## JNI 模板

```c
jdouble Java_pkg_Cls_f__ILjava_lang_String_2 (
    JNIEnv *env, jobject obj, jint i, jstring s) {
    const char *str = (*env)->GetStringUTFChars(env, s, 0);
    // process the string
    (*env)->ReleaseStringUTFChars(env, s, str);
    return ...;
}
```

## Frida Hook

```javascript
Java.perform(() => {
    const MainActivity = Java.use("com.n1ctf2024.ezapk.MainActivity");
    MainActivity.enc.implementation = function(input) {
        // 1. 直接观察密文
        console.log("enc input:", input);
        const out = this.enc(input);
        console.log("enc output:", out);
        return out;
        // 2. 或 hook 返回固定值
        return "iRrL63tve+H72wjr/HHiwlVu5RZU9XDcI7A=";
    };
});
```

## 评价

N1CTF 2024 ezapk 是 **Android + JNI 加密** 入门逆向题，亮点：
- `System.loadLibrary("native2"); System.loadLibrary("native1")` 链式加载
- 目标密文 `"iRrL63tve+H72wjr/HHiwlVu5RZU9XDcI7A="` 是 base64
- Frida hook 是最快解法（hook enc 拿到中间值）
- 也可对 native1/2 反汇编还原算法

适用读者：Android 逆向 / JNI 调通 / Frida hook 实践
