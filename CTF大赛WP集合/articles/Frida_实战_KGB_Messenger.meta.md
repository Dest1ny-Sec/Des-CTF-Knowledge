---
title: Frida 实战 KGB Messenger
contest: KGB Messenger CTF App
year: 2024
difficulty: medium
vuln_type: reverse
tags: [frida, android, kgb, russia, system-getProperty, base64, login, ctf-app]
attack_chain:
  - 第1关: hook System.getProperty("user.home") 强制返回"Russia"
  - 第2关: hook System.getenv(String) 返回"FLAG{57ERL1NG_4RCH3R}" base64
  - 解码: base64 -d "RkxBR3s1N0VSTDFOR180UkNIM1J9Cg==" → FLAG{57ERL1NG_4RCH3R}
  - 第3关: 用户名codenameduchess登录
  - 第4关: hook LoginActivity.j() 强制true
  - 后续关卡: 算法反推+Frida hook
key_payload: FLAG{57ERL1NG_4RCH3R}
one_liner: Frida闯关KGB Messenger：4关hook俄罗斯判断+base64密码+登录
lesson: Frida实战CTF App：System.getProperty/Environment反俄判断
quality: high
---

# Frida 实战 KGB Messenger

## 题目信息
- 比赛：KGB Messenger CTF App
- 类型：Android Frida 实战

## 关键攻击链
### 第 1 关：俄罗斯设备判断
- 报错：`This app can only run on Russian devices.`
- jadx 反编译：`System.getProperty("user.home") = Russia`
```javascript
var system = Java.use("java.lang.System");
system.getProperty.overload('java.lang.String').implementation = function (str) {
    var re = this.getProperty(str);
    return "Russia";
}
```

### 第 2 关：环境变量
- `System.getenv(String)` 返回 base64 字符串
```javascript
system.getenv.overload('java.lang.String').implementation = function (str) {
    return "RkxBR3s1N0VSTDFOR180UkNIM1J9Cg==";
}
// base64 -d → FLAG{57ERL1NG_4RCH3R}
```

### 第 3 关：登录
- 用户名 = `codenameduchess`（R.string.username）
```bash
adb shell input text 'codenameduchess'
```

### 第 4 关：密码验证
- `LoginActivity.j()` 函数决定登录结果
- 强制返回 true：
```javascript
var LoginActivity = Java.use("com.tlamb96.kgbmessenger.LoginActivity");
LoginActivity["j"].implementation = function () {
    var ret = this.j();
    return true;  // 强制 true
}
```

## 评分
- quality: high（4 关 Frida Hook 实战 + jadx 反编译思路）
