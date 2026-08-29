---
title: Bugku CTF 安卓逆向 LoopAndLoop
contest: Bugku
year: 2022
difficulty: hard
vuln_type: reverse
tags: [APK逆向, JNI反弹调用, check1+check2+check3, 100/1000/10000循环累加, 1835996258校验, alictf{}, JNI FindClass GetMethodID CallIntMethod, IDA F5, ARM F5]
attack_chain:
  - APK jadx 看 MainActivity: input → check(input, 99) == 1835996258 触发
  - check 调 chec(input, s) JNI native
  - so chec 用 FindClass("net/bluelotus/.../MainActivity") 反射拿 check1/check2/check3 methodID
  - CallIntMethod 调 (a2, v10[2*s%3], t, s-1) 反弹调 Java
  - check1: t += 1..99
  - check2: s%2==0 → t += 1..999; else t -= 1..999
  - check3: t += 1..9999
  - s=99 → v10[2*99%3] = v10[0] = check1; s=98 → check2; s=97 → check3; s=96 → check1
  - 循环递归直到 s=1 返回 t
  - flag: alictf{stringFromJNI2(in_int)}
key_payload: 'check(input,99) == 1835996258 / JNI chec FindClass GetMethodID CallIntMethod 反射 / check1+check2+check3 三函数累加 / 2*s%3 索引 / stringFromJNI2 flag'
one_liner: Bugku 安卓逆向 LoopAndLoop — JNI chec 反射调 check1+check2+check3 三函数累加 + check(input,99)==1835996258 + stringFromJNI2 还原 alictf{} flag。
lesson: JNI 反弹调 Java 函数是 Android 逆向难点;2*s%3 索引巧妙选函数;stringFromJNI2(in_int) 是 flag 生成函数。
quality: high
---

# Bugku CTF 安卓逆向 LoopAndLoop

## 速读
Bugku LoopAndLoop (阿里 CTF) — JNI 反弹调 Java 的循环累加题。

## 入口逻辑
```java
int in_int = Integer.parseInt(in_str);
if (MainActivity.this.check(in_int, 99) == 1835996258) {
    tv1.setText("The flag is:");
    tv2.setText("alictf{" + MainActivity.this.stringFromJNI2(in_int) + "}");
    return;
}
```

## so chec 函数
```c
int __fastcall Java_..._chec(JNIEnv *jenv, int a2, int t, int s) {
    v5 = (*jenv)->FindClass(jenv, "net/bluelotus/tomorrow/easyandroid/MainActivity");
    v10[0] = _JNIEnv::GetMethodID(jenv, v5, "check1", "(II)I");
    v10[1] = _JNIEnv::GetMethodID(jenv, v5, "check2", "(II)I");
    v10[2] = _JNIEnv::GetMethodID(jenv, v5, "check3", "(II)I");
    if (s - 1 <= 0)
        result = t;
    else
        result = _JNIEnv::CallIntMethod(jenv, a2, v10[2 * s % 3], t, s - 1);
    return result;
}
```

## 三个 Java check
- `check1(input, s)`: t += 1..99, return chec(t, s)
- `check2(input, s)`: s%2==0 → t += 1..999; else t -= 1..999
- `check3(input, s)`: t += 1..9999, return chec(t, s)

## s→函数映射 (2*s%3)
- 99*2%3=0 → check1
- 98*2%3=1 → check2
- 97*2%3=2 → check3
- 96*2%3=0 → check1

## 求解
- 倒推: 从 s=1 算到 s=99
- 满足 check(in_int, 99) == 1835996258 的 in_int
- stringFromJNI2(in_int) 得 alictf flag
