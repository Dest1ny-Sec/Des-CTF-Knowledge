---
title: bi0sCTF 2024 Tallocator (未翻译)
contest: bi0sCTF
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [android-native, custom-allocator, talloc, jni, anti-debug, key-xor]
attack_chain:
  - Java_bi0sctf_android_challenge_MainActivity_talloc 入口
  - 自定义分配器 mmap(0x41410000) + sbrk
  - is_talloc_inited 单次初始化
  - 调试器检测 v8 = v7[5] 调用
  - size 范围 0x150-0xFFF 走 sbrk_ed wilderness
  - 0x30 + 0xFC8 + 0x3A63 三个魔数
  - key = "50133tbd5mrt1769" XOR
key_payload: 自定义 talloc + anti-debug 回调 + wilderness 分配器
one_liner: bi0sCTF 2024 Android JNI 自定义分配器 Tallocator 题，未翻译版本（中文 WP 暂未覆盖）。
lesson: Android 逆向链 = Java → JNI → native lib（libtallocator.so），必须结合三层。
quality: high
---

bi0sCTF 2024 Tallocator 完整复现（**未翻译**版本，作者 ctfiot 转存的印度战队原版英文 WP）。

**题目结构**
```
app.apk
├── arm64-v8a/libnative.so + libtallocator.so
├── armeabi-v7a/libnative.so + libtallocator.so
├── x86/libnative.so + libtallocator.so
└── x86_64/libnative.so + libtallocator.so
```

**关键发现**
- `const key = "50133tbd5mrt1769"`（硬编码 key）
- `Java_bi0sctf_android_challenge_MainActivity_talloc` 入口
- 自定义分配器 `talloc`：
  - 首次调用 `mmap(0x41410000, 0x1000, 7, 34, -1, 0)` + `sbrk(4096)`
  - 三个魔数：`v7[1] = 0x30, v7[7] = 0xFC8, v7[4] = 0x3A63`
  - `wilderness_s = v7 + 7`
- **调试器检测**：`v8 = v7[5]; if (v8) v8(a1, a2); perror("Debugger called !!");`
- **大小分类**：`size = (data_size + 0x17) & 0xFFF0`：
  - `size > 0x150` 且 `size - 0x151 <= 0xEAE` 走 sbrk_ed wilderness
  - 其他走 mmap 区域 0x41410000

**反调试绕过**：patch `v7[5] = NULL` 即可；或 hook libc `sbrk` 让其返回 NULL 区域。

**攻击思路**：
- 写 native 客户端 JNI 调用 `talloc/free` 触发 UAF
- 配合 libc malloc bin 攻击
- key XOR 解密 flag

**未翻译说明**：ctfiot 缓存的 bi0sCTF 2024 官方 WP 是英文原文，本 meta 仅作概要索引。完整 WP 建议读 https://github.com/bi0s-Recruitment/ 或 bi0s 官方博客。
