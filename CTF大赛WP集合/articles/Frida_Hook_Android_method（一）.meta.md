---
title: Frida Hook Android method（一）
contest: ad2001 Frida 系列
year: 2023
difficulty: easy
vuln_type: reverse
tags: [frida, android, hook, java.perform, caesar-cipher, get_random, check]
attack_chain:
  - get_random返回0-99随机整数
  - check(i, i2) 验证 (i*2)+4==i2
  - 成功返回"AMDYV{WVWT_CJJF_0s1}"的Caesar变种
  - charAt-21取模26+26
  - Frida hook get_random返回真实值
  - Frida hook check(int, int)强制参数8, 20
key_payload: AMDYV{WVWT_CJJF_0s1}  # Caesar-21后flag
one_liner: Frida Hook Android：get_random+check函数hook+Caesar-21解flag
lesson: Frida可用Java.use+"implementation"覆盖Java方法
quality: high
---

# Frida_Hook_Android_method（一）

## 题目信息
- 比赛：ad2001 Frida 教学系列
- 题目：frida0x1（Hook Android method）
- 工具：Frida

## 关键攻击链
### 1. 原 Java 代码
```java
final int i = get_random();
int get_random() { return new Random().nextInt(100); }
void check(int i, int i2) {
    if ((i * 2) + 4 == i2) {
        // 显示 flag
        StringBuilder sb = new StringBuilder();
        for (int i3 = 0; i3 < 20; i3++) {
            char charAt = "AMDYV{WVWT_CJJF_0s1}".charAt(i3);
            if (charAt < 'a' || charAt > 'z') {
                if (charAt >= 'A' && charAt <= 'Z') {
                    charAt = (char) (charAt - 21);
                    if (charAt >= 'A') { ... }
                    charAt = (char) (charAt + 26);
                }
                sb.append(charAt);
            } else {
                charAt = (char) (charAt - 21);
                if (charAt >= 'a') sb.append(charAt);
                charAt = (char) (charAt + 26);
                sb.append(charAt);
            }
        }
    }
}
```

### 2. Caesar-21 解码
- 每个字符 - 21，若结果 < 0 则 +26
- "AMDYV{WVWT_CJJF_0s1}" 解后得 flag

### 3. Frida Hook
```javascript
// Hook 1: get_random 读取值
Java.perform(function() {
    var a = Java.use("com.ad2001.frida0x1.MainActivity");
    a.get_random.implementation = function() {
        var ret_val = this.get_random();
        console.log("随机数：" + ret_val);
        console.log("答案：" + (ret_val * 2 + 4));
        return ret_val;
    };
});

// Hook 2: check 强制参数
Java.perform(function() {
    var a = Java.use("com.ad2001.frida0x1.MainActivity");
    a.check.overload('int', 'int').implementation = function(a, b) {
        console.log("你输入的是：" + b);
        this.check(8, 20);  // 强制 (8*2)+4 == 20
    };
});
```

## 评分
- quality: high（Frida Hook 完整 + Caesar-21 解码）
