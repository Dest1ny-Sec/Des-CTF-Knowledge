---
title: rwctf 2023 ASTLIBRA
contest: RWCTF
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [c-cgi, constructor-attribute, exp, curl, system-rce, source-leak]
attack_chain:
  - 找到 `__attribute__((constructor))` 自动执行函数
  - 调 system("xxx")
  - 拿 exp curl 反弹 shell
  - 源码泄露路径
key_payload: __attribute__((constructor)) 自动执行
one_liner: rwctf 2023 ASTLIBRA C-CGI 题目，constructor 属性自动执行。
lesson: '`__attribute__((constructor))` 在 main 前自动执行，是 C/C++ 隐藏代码常用技巧。'
quality: medium
---

rwctf 2023 ASTLIBRA 题 WP（来源 ctfiot，仅给部分代码片段）。

**核心代码**
```c
http\");}  // ???
__attribute__((constructor)) void exp() {
    ...
    system(xxx);
    ...
}
function tmp(){
    var ch = curl_init();
}
```

**关键发现**：
- `__attribute__((constructor))` 修饰的函数 `exp()` 在 main 之前自动执行
- 不需要主动调用，反编译时容易漏掉
- 函数内调 `system("xxx")` 反弹 shell

**`__attribute__((constructor))` 用途**：
- C/C++ ELF 加载时优先于 main 执行
- 类似 Java static initializer / Python module-level code
- CTF 出题人常用：藏 RCE 后门

**质量评估**：题目残缺（只给部分代码），标 medium。
