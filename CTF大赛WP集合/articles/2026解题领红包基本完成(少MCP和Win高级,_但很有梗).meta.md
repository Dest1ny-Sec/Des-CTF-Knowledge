---
title: 2026 解题领红包基本完成（CrackMe v2.5 假码+真码+校验和+AES点阵图+Android 拼图）
contest: 2026 解题领红包
year: 2026
difficulty: hard
vuln_type: [reverse, misc_unknown, pwn_unknown]
tags: [解题领红包 2026, CrackMe v2.5, 假码 53+byte_D63032 16 字符, 真码长度 31, 校验和 44709 sum(Str[i]*(i+1)), JNI 环境异常 v152, /proc/self/maps 首次读取 v161, Frida/Xposed inline hook, readlink+readlinkat 模拟器, maps 黑名单 frida/magisk, AES 解密点阵图 flag, Android Compose w1.g.d F.C.C case 25, key=[54,1,22,28] XOR, 30 字符总长度, Frida Java.perform u1.m f7612q]
attack_chain:
  - 假码：53 + byte_D63032[] = 16 字符 "53..." 假码比对
  - 真码长度 31
  - 校验和 sum(Str[i] * (i+1)) = 44709
  - AES 解密点阵图：用户输入渲染与点阵图比较
  - JNI 环境异常检测 (FindClass/GetMethodID/NewStringUTF/GetObjectRefType)
  - /proc/self/maps 首次读取检测 v161
  - Frida/Xposed inline hook 检测
  - readlink+readlinkat 模拟器检测
  - Android Compose: u1.m 类构造参数 f7612q 读 flag
  - 拼图解密 key=[54,1,22,28] XOR cipher_blocks 6 块
  - 30 字符总长度
key_payload: "校验和 sum(Str[i] * (i+1)) = 44709"
one_liner: 2026 解题领红包 CrackMe v2.5：假码 16 + 真码 31 校验和 44709 + AES 点阵图 + JNI/Frida/模拟器多层检测 + Android 拼图 6 块 XOR。
lesson: CrackMe 真码 = 假码外+真码（长度+校验和+子函数动态生成）三层防御；JNI/Frida/模拟器检测是真机脱壳关键；Android Compose 拼图解密在 F.C 类 case 25 完成。
quality: high
---

# 2026 解题领红包基本完成（少 MCP 和 Win 高级，但很有梗）

## 第一部分：CrackMe v2.5 桌面端

```c
int __cdecl sub_D5D130(char a1) {
    // 假码检测
    if (!v5) {
        while (Str[v6] == v4) {
            if (++v6 == 16) {  // 假码长度 16
                v16 = 1;
                puts("Nice try, but not quite right...");
                goto LABEL_9;
            }
            v4 = byte_D63032[v6];
        }
    }
    // 真码长度检测
    if (strlen(Str) != 31) {  // 真码长度 31
        puts("Hint: The length is your first real challenge.");
        goto LABEL_9;
    }
    // 校验和
    if (sub_C916D0((int)Str, 31)) {
        Str = 0;
        v8 = *v22;
        do { Str += ++v9 * v8; v8 = v22[v9]; } while (v8);
        if (Str != 44709) {
            puts("Checksum failed!");
            // Expected: 44709
        }
    }
}

bool __cdecl sub_C916D0(int a1, int a2) {
    unsigned __int8 *Block = (unsigned __int8 *)sub_D5B710(0x64u);
    sub_C91620(Block);  // 动态生成 Flag
    // 字节比较 Str[i] == Block[i]
    if (a2 == v4) return true;
}
```

## 三层防御

1. **假码**：长度 16，53+byte_D63032[] 直接 return "Nice try"
2. **真码长度**：31
3. **校验和**：`sum(Str[i] * (i+1)) = 44709`（下断点直接看 Block）

## 环境检测（12 项）

| 检测 | 干净环境值 | 含义 |
|------|----------|------|
| JNI 异常（FindClass 等） | v152 | JNI 全部正常 |
| /proc/self/maps 首次读取 | v161 | 异常检测 |
| Frida/Xposed inline hook | 无 hook | 可执行库 hook |
| readlink+readlinkat 模拟器 | 不触发 | 真机一致 |
| maps 黑名单字符串 | frida/magisk | 检测反调试 |
| 设备指纹 | v263=1 | 模拟器列表 |
| /sys/cpu access 失败 | 不触发 | 真机可访问 |
| 首次 maps 解析 v114 | = 0 | 干净环境无命中 |

## AES 解密点阵图 flag

> 使用 AES(大概是)解密输入文件，解密后得到文字点阵图（图片内容就是 Flag）  
> 将用户输入进行渲染，并与点阵图比较

## Android 拼图 flag（F.C 类 case 25）

```python
key = [54, 1, 22, 28]
cipher_blocks = [
    [80, 109, 119, 123, 77],
    [97, 116, 34, 45, 105],
    [ord('f'), ord('1'), ord('|'), ord('-'), 5, ord('^')],
    [4, 49, 36, 42, 105],
    [ord('e'), ord('q'), ord('d'), ord('-'), ord('X'), ord('f'), ord('I')],
    [ord('p'), ord('2'), ord('e'), ord('h'), 7, ord('w'), ord('"'), ord('p'), ord('K')]
]

flag = ""
for block in cipher_blocks:
    for i in range(len(block)):
        current_key = key[i % len(key)]
        char_code = block[i] ^ current_key
        flag += chr(char_code)
print(flag)
```
30 字符总长度（`_total_len: 30`）。

## Frida Hook Java.perform

```javascript
Java.perform(function() {
    let m = Java.use("u1.m");
    m["$init"].implementation = function(...) {
        console.log(`m.$init is called: ...`);
        this["$init"](...);
    };
});
```
Hook `u1.m` 构造函数的 `f7612q`（flag 字符串）参数。
