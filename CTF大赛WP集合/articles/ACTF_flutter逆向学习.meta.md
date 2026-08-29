---
title: ACTF flutter 逆向学习
contest: ACTF
year: 2023
difficulty: medium
vuln_type: reverse
tags: [Flutter, DartVM, libapp.so, blutter, objs.txt, blutter_frida.js, ida_script, asm, frida hook, IDA动态调试, root真机, AndroidKiller, debuggable, targetSdkVersion, adb push, onChanged, onSubmitted, 按钮交互]
attack_chain:
  - apk 改后缀 .zip 解压得 libapp.so (DartVM 快照)
  - reflutter/flutter 逆向助手对新 SDK 无效
  - 用 blutter 解析 libapp.so (pyelftools + capstone + libicu-dev)
  - 产物: objs.txt 对象池、blutter_frida.js、ida_script 符号还原、asm 反编译
  - AndroidKiller 改 AndroidManifest.xml 加 android:debuggable="true" + targetSdkVersion 27/28
  - adb install 重打包
  - adb push android_server64 /data/local/tmp/as + chmod 777
  - adb forward tcp:12345 tcp:12345
  - IDA 启动, 加载 libapp.so, run addName.py 还原符号
  - 看 main.dart 找按钮回调 (onChanged/onSubmitted)
  - Frida hook 输入/输出函数
key_payload: 'blutter / IDA + addName.py / Frida hook 按钮回调 / targetSdkVersion 27/28 + debuggable=true / android_server64 root 真机'
one_liner: ACTF Flutter 逆向学习 — blutter 解析 DartVM 快照 + IDA 符号还原 + Frida hook 按钮回调 + 真机 root 动态调试。
lesson: Flutter 逆向核心是 DartVM 快照 (libapp.so);blutter 是开源首选工具;高 SDK 版本需降 targetSdkVersion 才能重签名;真机动态调试需 root + adb + android_server。
quality: high
---

# ACTF flutter 逆向学习

## 速读
ACTF Flutter APK 逆向完整教程 — 介绍 blutter + IDA + Frida 全流程。

## 步骤
1. **APK 改后缀 .zip 解压** — 得 libapp.so (DartVM 快照)
2. **安装 blutter** — `apt install python3-pyelftools libicu-dev libcapstone-dev`
3. **blutter 解析** — 产物 5 类:
   - objs.txt: 对象池完整转储
   - blutter_frida.js: Frida hook 脚本
   - ida_script: 符号还原脚本
   - asm: Dart 反编译结果
4. **AndroidKiller 改 manifest** — `android:debuggable="true"` + `targetSdkVersion=27/28`
5. **adb 安装** — `adb install chall_killer.apk`
6. **真机 root** — adb push android_server64 + chmod 777
7. **IDA 动态调试** — adb forward + addName.py 还原符号
8. **Frida hook** — `Interceptor.attach` 监听 onChanged/onSubmitted
