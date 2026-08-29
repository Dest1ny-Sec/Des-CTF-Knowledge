---
title: Frida 与 Android CTF
contest: 看雪/Tide 安全 (kanxue/pediy1)
year: 2022
difficulty: medium
vuln_type: [reverse, misc_unknown]
tags: [Frida, Android, JNI, Java.perform, Java.choose, enumerateClassLoaders, Interceptor.replace, kill, anti-debug]
attack_chain: ["frida -U -f 目标包 spawn 注入", "Java.perform hook 关键方法 VVVV(context, str)", "Java.choose 找 MainActivity 实例注入伪 context", "Java.enumerateClassLoaders 找正确 classloader", "枚举 0-99999 爆破正确输入拿 true 返回", "Interceptor.replace(libc.so!kill) 绕反调试"]
key_payload: "Java.use(\"com.kanxue.pediy1.VVVVV\").VVVV(CONTEXT2, String(x))"
one_liner: Frida hook + 爆破绕过 Android JNI 校验 + kill 拦截绕反调试
lesson: Android CTF 高频工具是 Frida；自定义 classloader 需 enumerateClassLoaders 切换；JNI 反调试常见用 kill(pid, 0) 检测 tracerpid
quality: high
---

# Frida 与 Android CTF

原文 https://www.ctfiot.com/31515.html （Tide 安全团队 2022）

## 案例：com.kanxue.pediy1.VVVV 校验绕过

**Step 1: hook 关键方法**
```js
Java.perform(function () {
    Java.use("com.kanxue.pediy1.VVVVV").VVVV.implementation = function (context, str) {
        var result = this.VVVV(context, str);
        console.log("context,str,result => ", context, str, result);
        console.log("context className is => ", getObjClassName(context));
        CONTEXT = context;
        return true;  // 强制 true
    }
})
```

**Step 2: 拿真 context 注入爆破**
- 用 `Java.choose("MainActivity")` 拿活实例
- `Java.use("MainActivity$1").$new(MainActivity)` 拿真 context
- 0..99999 枚举找 VVVV 返回 true 的 input

**Step 3: 自定义 classloader 切换**
```js
Java.enumerateClassLoaders({
    onMatch: function (loader) {
        if (loader.findClass("com.kanxue.pediy1.VVVVV")) {
            Java.classFactory.loader = loader;  // 关键
        }
    }
})
```

**Step 4: kill 反调试拦截**
```js
var kill_addr = Module.findExportByName("libc.so", "kill");
Interceptor.replace(kill_addr, new NativeCallback(function (arg0, arg1) {
    console.log("kill called:", arg0, arg1);
    return 0;  // 不真 kill
}, "int", ['int', 'int']));
```

## Frida 工具点回顾
- `Java.perform()` — 进 ART 主线程
- `Java.use(class).method.implementation = fn` — Java 层 hook
- `Java.choose(class, {onMatch, onComplete})` — 找存活实例
- `Java.enumerateClassLoaders` — 切换 classloader
- `Interceptor.replace(addr, NativeCallback)` — native hook
- `Interceptor.attach(addr, {onEnter, onLeave})` — 观察/劫持
- `Module.findExportByName(module, name)` — 找符号

## 教学价值
- Frida 是 Android CTF 必备
- 多 classloader（插件化、MultiDex、动态加载）必须切 loader
- kill(pid, 0) 是经典反调试检测 Frider
- 主动 spawn 注入 (`-f` 标志) 比 attach 更早拿 control
