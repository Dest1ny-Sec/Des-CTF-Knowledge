---
title: CTF 《2015 移动安全挑战赛》第二题 AliCrackme_2 逆向
contest: 移动安全挑战赛
year: 2015
difficulty: easy
vuln_type: reverse
tags: [Android so 静态, while 循环匹配, aWojiushidaan, Frida hook fgets, TracerPid:t0, hook kill, mprop ro.debuggable, AS 64端口12346, 看雪 行简, 2015经典]
attack_chain:
  - so 静态: while 循环匹配用户输入 vs 硬编码 aWojiushidaan
  - 反调试: Frida hook fgets 改 TracerPid: 为 TracerPid:t0
  - Frida hook kill 直接返回 0
  - 启动 android_server64 -p 12346 root 调试
  - mprop 工具 ro.debuggable 1 改属性
key_payload: 'while 循环字符比较 / aWojiushidaan / Frida hook fgets 改 TracerPid / Frida hook kill / mprop ro.debuggable 1 / android_server64 12346'
one_liner: AliCrackme_2 — Android so 静态分析 while 循环匹配 aWojiushidaan + Frida hook fgets 改 TracerPid:t0 + hook kill + mprop ro.debuggable 1 + android_server64 -p12346 调试。
lesson: Android 经典逆向三件套:静态分析硬编码字符串 + Frida hook 改 TracerPid + mprop 改 ro.debuggable;2015 年风格是 so 字符比较。
quality: medium
---

# CTF 《2015 移动安全挑战赛》第二题 AliCrackme_2 逆向

## 速读
2015 移动安全挑战赛 AliCrackme_2 — Android so 字符串匹配 + Frida 反调试。

## 静态分析

### 校验函数
```c
v5 = (*env)->GetStringUTFChars(env, password, 0);
v6 = off_628C;  // aWojiushidaan
while (1) {
    v7 = *v6;
    if (v7 != *v5) break;
    ++v6; ++v5;
    v8 = 1;
    if (!v7) return v8;
}
return 0;
```

- 用户输入 vs `aWojiushidaan` 逐字符比较
- 全部相等返回 1, 否则 0

## 反调试

### Frida hook fgets
```javascript
function Tracepid() {
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
}
```

### Frida hook kill
```javascript
var killptr = Module.findExportByName("libc.so", "kill");
Interceptor.replace(killptr, new NativeCallback(function (pid, sig) {
    return 0;
}, 'int', ['int', 'int']));
```

## 动态分析
```bash
./mprop ro.debuggable 1  # 改属性
./as_64 -p 12346         # 启动调试 server
```
