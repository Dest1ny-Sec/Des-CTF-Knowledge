---
title: 使用Unidbg在CTF-Android题目的快速解题
contest: Unidbg Android CTF
year: 2024
difficulty: medium
vuln_type: reverse
tags: [Unidbg, Android, JNI, libj.so, AbstractJni, DvmClass, JNIEnv, callJniMethodObject, 模拟执行]
attack_chain:
  - aapt dump badging apk 看包名 + Activity
  - IDA 反编译 libj.so 看 JNI 函数 Java_an_droid_j_MainActivity_j/init/p
  - j() 返回 "FlagLostHelpMeGetItBack" 字符串 (内置常量, 长度 30 字节)
  - init(I) 接收 1738911344 返回 flag 字符串
  - p(I) 循环 99999 次混淆控制流
  - 用 Unidbg AndroidEmulatorBuilder.for32Bit() 创建模拟器
  - setProcessName("an.droid.j") 避免进程名校验
  - memory.setLibraryResolver(new AndroidResolver(23))
  - vm.createDalvikVM(File(apkFilePath)) 加载 APK
  - vm.loadLibrary(File(soFilePath), true) 加载 so
  - vm.setJni(this) 设置 AbstractJni
  - dvmClass.newObject(null).callJniMethodObject(emulator, "init(I)Ljava/lang/String;", temp)
  - System.out.println("flag{" + result + "}")
key_payload: 'lesson4 + AndroidEmulatorBuilder + callJniMethodObject init(I)'
one_liner: Unidbg 模拟 Android JNI 调用 libj.so 绕过动态分析，无需真机直接拿到 flag。
lesson: Unidbg 是 Android RE 的金钥匙：AndroidEmulatorBuilder + setProcessName + AndroidResolver + createDalvikVM + loadLibrary 五步走，setJni(this) 必加防报错。
quality: high
---

# 使用Unidbg在CTF-Android题目的快速解题

## 概览
- **来源**: 看雪 NYSECbao
- **类型**: Unidbg Android JNI 模拟
- **难度**: ⭐⭐⭐

## APK 静态分析
- `aapt dump badging <apk>` 看包名/Activity
- IDA 打开 libj.so 反编译 JNI 函数:
  - `Java_an_droid_j_MainActivity_j()` - 返回 "FlagLostHelpMeGetItBack" (内置常量)
  - `Java_an_droid_j_MainActivity_init(int)` - 接收 int 返回 flag 字符串
  - `Java_an_droid_j_MainActivity_p(int)` - 循环混淆控制流

## Unidbg EXP
```java
package com.lesson4;

import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.AbstractJni;
import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;

public class lesson4 extends AbstractJni {
    private final AndroidEmulator emulator;
    private final VM vm;
    private final Module module;
    private final Memory memory;
    private final DalvikModule dm;

    public lesson4(String apkFilePath, String soFilePath, String apkProcessname) throws IOException {
        // 1. 创建 32 位模拟器
        emulator = AndroidEmulatorBuilder.for32Bit()
            .setProcessName(apkProcessname)  // 进程名防校验
            .build();
        
        // 2. 设置系统库解析
        memory = emulator.getMemory();
        memory.setLibraryResolver(new AndroidResolver(23));
        
        // 3. 创建 Dalvik VM 加载 APK
        vm = emulator.createDalvikVM(new File(apkFilePath));
        vm.setVerbose(false);
        
        // 4. 加载 SO
        dm = vm.loadLibrary(new File(soFilePath), true);
        module = dm.getModule();
        
        // 5. 设置 Jni 上下文
        vm.setJni(this);
    }

    public int func_p(int args) {
        DvmClass dvmClass = vm.resolveClass("an.droid.j.MainActivity");
        DvmObject<?> object = dvmClass.newObject(null);
        return object.callJniMethodInt(emulator, "p(I)I", args);
    }

    public String func_init(int args) {
        DvmClass dvmClass = vm.resolveClass("an.droid.j.MainActivity");
        DvmObject<?> object = dvmClass.newObject(null);
        DvmObject<?> object1 = object.callJniMethodObject(
            emulator, "init(I)Ljava/lang/String;", args);
        return object1.getValue().toString();
    }

    public static void main(String[] args) throws IOException {
        String soFilePath = "unidbg-android/src/test/java/com/lesson4/libj.so";
        String apkFilePath = "unidbg-android/src/test/java/com/lesson4/a.apk";
        String apkProcessname = "an.droid.j";

        lesson4 mylesson4 = new lesson4(apkFilePath, soFilePath, apkProcessname);
        int temp = 1738911344;
        System.out.println("flag{" + mylesson4.func_init(temp) + "}");
    }
}
```

## 关键 API
- `callJniMethodInt(emulator, "p(I)I", args)` - 调用返回 int 的 JNI 方法
- `callJniMethodObject(emulator, "init(I)Ljava/lang/String;", args)` - 调用返回 String 的 JNI 方法
- `dvmClass.newObject(null)` - 创建 Dalvik 对象实例
- `vm.resolveClass("an.droid.j.MainActivity")` - 解析类

## 优势
- 不用真机/模拟器
- 不用 Frida hook 动态调试
- Java 一键模拟整个 Android JNI 调用链
