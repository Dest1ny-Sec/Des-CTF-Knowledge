---
title: 【Android CTF】鸿蒙逆向 - SHCTF - Android？Harmony！题解
contest: SHCTF
year: 2024
difficulty: medium
vuln_type: reverse
tags: [HarmonyOS, ArkTS, ETS-bytecode, encode-114514, mod-95, ASCII-shift, maze-create, promptAction]
attack_chain: 鸿蒙 ArkTS/ETS 字节码反编译 Index 构造函数初始化 secretKey + __userInput/validateAndCreateMaze 用 encode(arg0) 与 secretKey 比较 + 调 maze.CreateMaze 生成迷宫写 /What 文件/encode 函数 (114514 * (ord - 32) + 1919810) % 95 + 32 字符编码/逆运算 ((y - 32) * 95^(-1) - 1919810) / 114514 + 32 还原
key_payload: secretKey = "[f#fLw)??Pz?#9w)Du[ks[q[#w4D?4P4UJf,kU[f.rDkfwrDtq...)?J.#rP4[qrPDJkkJ|.9J|qffU?k|D4P4P[wkk.)k?JUJ[k#9kww[r??wUfw|PkrPUf.P#f.P#.PwJ4f4q.PU4UPDr9.[9fJ#PqP)cDDffJPDrJ.J4qPP[r[.JfJ4f|?U9#"
one_liner: SHCTF 2024 鸿蒙 ArkTS 逆向，secretKey + encode 字符编码 (114514*x + 1919810) % 95 + 32 还原 + 迷宫生成。
lesson: 鸿蒙 ArkTS 编译为 ETS 字节码，可用 HarmonyOS 反编译工具还原；简单模运算 (a*x + b) % m + offset 可通过 mod 逆元还原输入；迷宫生成函数 CreateMaze(arg0) 把 flag 转迷宫。
quality: medium
---

# 【Android CTF】鸿蒙逆向 - SHCTF - Android？Harmony！题解

## 概览
SHCTF 2024 鸿蒙 HarmonyOS ArkTS 逆向实战，覆盖 ETS 字节码 + 字符编码还原 + 迷宫生成。

## ArkTS 字节码反编译

### Index 构造函数
```javascript
public Object Index(...) {
    if ((0 == arg3 ? 1 : 0) != 0) { arg3 = -1; }
    if ((0 == arg4 ? 1 : 0) != 0) { arg4 = null; }
    Object obj = super(arg0, arg2, arg3, arg5);
    if (("function" == typeof(arg4) ? 1 : 0) != 0) {
        obj.paramsGenerator_ = arg4;
    }
    obj.__userInput = ObservedPropertySimplePU("", obj, "userInput");
    obj.secretKey = "[f#fLw)??Pz?#9w)Du[ks[q[#w4D?4P4UJf,kU[f.rDkfwrDtq...)?J.#rP4[qrPDJkkJ|.9J|qffU?k|D4P4P[wkk.)k?JUJ[k#9kww[r??wUfw|PkrPUf.P#f.P#.PwJ4f4q.PU4UPDr9.[9fJ#PqP)cDDffJPDrJ.J4qPP[r[.JfJ4f|?U9#";
    obj.setInitiallyProvidedValue(arg1);
    obj.finalizeConstruction();
    return obj;
}
```

### validateAndCreateMaze 函数
- `secretKey == newobjrange.encode(arg0)` 比较
- 正确时调 `maze.CreateMaze(arg0)` 生成迷宫
- 写文件到 `filesDir + "/What"`
- 弹 toast "口令正确！\n等下！好像创建了什么东西？"

### encode 函数
- 关键公式：`String.fromCharCode((((114514 * (ord - 32)) + 1919810) % 95) + 32)`
- 对每个字符 x：`y = (114514 * (x - 32) + 1919810) % 95 + 32`

## 还原输入
- 逆运算：`x = ((y - 32) * pow(95, -1, 114514) - 1919810) * pow(114514, -1, 95) + 32`
- 模运算下需要先求 95 关于 114514 的逆元
- 逐字符还原 secretKey 对应的原始口令

## 经验提炼
- 鸿蒙 ArkTS 编译为 ETS 字节码，结构类似 .class
- 鸿蒙特有 API：`@ohos:promptAction`、`@ohos:file.fs`、`@bundle:com.welcome.shctf/entry/ets/model/...`
- `(a*x + b) % m + offset` 字符编码可通过扩展欧几里得求逆元还原
- 模运算下求 `gcd(a, m) = 1` 才有解，否则需要单独处理
- 迷宫生成函数 CreateMaze(arg0) 把 flag 转迷宫是常见 Android 比赛套路
- 114514 / 1919810 是日本 ACG 文化梗数字（"野獣先輩" 和"田所浩二"）
