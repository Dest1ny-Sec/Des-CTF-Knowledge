---
title: Android APK 逆向分析：多组件协同漏洞利用链详解
contest: Android 逆向
year: 2025
difficulty: hard
vuln_type: misc_unknown
tags: [APK反编译, WebActivity未导出, CoreService normal权限, AIDL a.Stub, MiscService透传Intent, CLASS_NAME, libWaWaWa.so 娜迦加固, DT_STRTAB损坏, JNI decode, Serializable DTO, DES key/iv]
attack_chain:
  - apktool d Load -o decompiled 反编译
  - WebActivity(未导出) 需走 Intent 跳板
  - CoreService (normal 权限) AIDL a.Stub 提供 Load.getUrl/getToken/getIv + decode
  - MiscService (已导出) 透传 Intent CLASS_NAME + putExtras
  - b implements Serializable { key, iv, status } DTO
  - WebActivity 读 Serializable b 实例, 满足 c()="loading" 调 Load.decode
  - libWaWaWa.so 32 位 ARM, DT_STRTAB 损坏, 娜迦加固特征
  - JNI: Java_com_example_wawawa_Load_decode / getUrl / getToken / getIv
  - 攻击: 通过 MiscService 启动 WebActivity, 传 Serializable b 实例
  - 申请 normal 权限 com.example.wawawa.permission.CORE_SERVICE
key_payload: 'APK 多组件协同 / MiscService Intent 透传 / WebActivity 未导出但可间接启动 / CoreService AIDL a.Stub / 娜迦加固 / Serializable b DTO / JNI decode'
one_liner: Android 多组件协同漏洞链 — APK 反编译 + MiscService (已导出) 透传 Intent CLASS_NAME 启动未导出 WebActivity + CoreService AIDL 远程调 JNI 拿 key/iv + libWaWaWa.so 娜迦加固解密。
lesson: Android normal 权限形同虚设,任何 app 可申请;MiscService 透传 Intent 是常见未导出组件攻击跳板;娜迦加固 DT_STRTAB 损坏是显著特征;Serializable DTO 跨进程传参可携带攻击 payload。
quality: high
---

# Android APK 逆向分析：多组件协同漏洞利用链详解

## 速读
Android 逆向综合题 — 多组件 + AIDL + 娜迦加固 SO 协同利用。

## 组件结构

| 组件 | 状态 | 入口 |
|------|------|------|
| WebActivity | 未导出 | 需 Intent 跳板 |
| CoreService | normal 权限 | AIDL a.Stub |
| MiscService | 已导出 | 透传 Intent |
| libWaWaWa.so | 32 位 ARM | 娜迦加固 |

## WebActivity
- 读 Serializable "KEY" 实例 (类型 b)
- `b.a()` = DES key, `b.b()` = DES iv
- `b.c()=="loading"` 调 `Load.decode(this, key, iv, a.a)`
- 失败降级 `loadUrl("file:///android_asset/666")`

## CoreService
- AIDL `a.Stub` 三个方法:
  - `a()` → 远程 VPS POST 拿 key
  - `b()` → null
  - `c()` → 调 `Load.getIv` 拿本地 iv

## MiscService
- `setClassName(getApplicationContext(), intent.getStringExtra("CLASS_NAME"))`
- `putExtras(arg4)` 透传所有参数
- `setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)` 启动 Activity

## libWaWaWa.so
- 32 位 ARM EABI5
- `DT_STRTAB 0x460cc not located in any PT_LOAD segment` (损坏)
- 无 Section Header (被去除)
- 字符串: "begin decode strtab" / "decode string %s" / "end decode strtab 2"
- 典型娜迦加固

## JNI Exports
- `Java_com_example_wawawa_Load_decode`
- `Java_com_example_wawawa_Load_getUrl`
- `Java_com_example_wavawa_Load_getToken`
- `Java_com_example_wavawa_Load_getIv`
