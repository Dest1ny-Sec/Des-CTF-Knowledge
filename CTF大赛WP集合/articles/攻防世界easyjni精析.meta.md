---
title: 攻防世界 easyjni 精析
contest: 攻防世界 (xctf)
year: 2023
difficulty: medium
vuln_type: [reverse, crypto_oracle]
tags: [APK, JNI, native, base64, 自定义编码表, swap, 字符交换, 看雪, xianxiong]
attack_chain: ["APK 反编译定位 JNI native 方法", "JADX/Ghidra 打开 .so 看 JNI_OnLoad 注册函数", "识别自定义 base64 编码表 'i5jLW7S0GX6uf1cv3ny4q8es2Q+bdkYgKOIT/tAxUrFlVPzhmow9BHCMDpEaJRZN'", "用 str.maketrans 映射回标准 base64 字母表", "base64 解码得 flag 字符串", "看 so 函数：先做 16 字节字符表置换 (s1[i] = t_str[i+16])", "再做 32 字节相邻 swap 还原"]
key_payload: "str1.translate(str.maketrans(string1, string2)) → base64.b64decode"
one_liner: 自定义 base64 字母表 + JNI 字符串置换还原
lesson: native 层 base64 经常换字母表防识别；JNI_OnLoad 里 StringUTFChars 读入后做字符表 swap
quality: high
---

# 攻防世界 easyjni 精析

原文 https://www.ctfiot.com/97303.html （看雪论坛 xianxiong）

## 题一：APK 自定义 base64
```python
import base64, string

str1 = "QAoOQMPFks1BsB7cbM3TQsXg30i9g3=="
string1 = 'i5jLW7S0GX6uf1cv3ny4q8es2Q+bdkYgKOIT/tAxUrFlVPzhmow9BHCMDpEaJRZN'  # 自定义表
string2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"  # 标准表

decoded = base64.b64decode(str1.translate(str.maketrans(string1, string2)))
print(decoded)
```

## 题二：SO 字符串置换
```c
// 16 字节字符表交换
do {
    v8 = &s1[i];
    s1[i] = t_str[i + 16];
    v9 = t_str[i++];
    v8[16] = v9;
} while (i != 16);

// 32 字节相邻 swap
do {
    v12 = __OFSUB__(v10, 30);
    v11 = v10 - 30 < 0;
    v16 = s1[v10];
    s1[v10] = s1[v10 + 1];
    s1[v10 + 1] = v16;
    v10 += 2;
} while (v11 ^ v12);
```

## 解码脚本
```c
#include <stdio.h>
int main() {
    int i = 0, j = 0;
    char s1[33] = "s1:abcdefghijklmnopqrstuvwxyz123";
    char t_str[33] = "t_str:ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    // 1) 16 字节字符表交换
    do {
        char v9 = t_str[i + 16];
        s1[i] = v9;
        t_str[i + 16] = s1[i + 1];
        i++;
    } while (i != 16);
    // 2) 32 字节相邻 swap
    i = 0;
    do {
        char v9 = s1[i];
        s1[i] = s1[i + 1];
        s1[i + 1] = v9;
        i += 2;
    } while (i != 32);
    for (j = 0; j < 33; j++) printf("%c", s1[j]);
}
```

## 教学要点
- **JNI 字符串处理**：native 层加密后用 `NewStringUTF` 返回，Java 层只看到密文
- **自定义 base64 字母表** 是入门防识别技术，攻击手法是 str.translate
- **字符表 swap**：用 `OFSUB` 宏做循环退出条件是 IDA 反编译常见坑
- APK + SO 双层加密是 2022+ 移动 CTF 标配
- 看雪论坛 xianxiong 系列教程质量高

## 配套思考题
代码块二（带 OFSUB 的）通常作为思考题，要识别"循环 16 次（i<16 还是 16==i）"的退出条件
