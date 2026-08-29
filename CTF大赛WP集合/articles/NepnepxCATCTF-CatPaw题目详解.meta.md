---
title: NepnepxCATCTF CatPaw 题目详解 (Android 小米备份 + 触摸事件)
contest: NepnepxCATCTF
year: 2023
difficulty: hard
vuln_type: reverse
tags: [Android 小米备份, 7zip, /dev/input/event1 触摸事件, Frida hook LoginDataSource, X/Y 03003500/03003600]
attack_chain: |
  1. 题目: NepnepxCATCTF CatPaw — Android 小米备份
  2. 解压:
     - 7zip 打开小米备份 → apk
     - jadx 打开 apk → 看 java 层
  3. 验证:
     - md5 == "8b9b0ad9c324204fac87ae0fc2c630bd"
     - password > 5 位
     - Frida hook LoginDataSource.login() 绕验证
  4. 关键: so 读 /dev/input/event1 保存到应用目录
     - getevent -lt /dev/input/event1 抓坐标
     - cat 1666666666 >> /dev/input/event1 重放触摸事件
  5. 触摸事件分析:
     - 03003500: X 轴
     - 03003600: Y 轴
     - 16 字节事件记录: type(2) + code(2) + value(4) + timestamp(8)
  6. 还原触摸坐标 → 画图
  7. 把画的图转 flag
key_payload: |
  # Frida hook LoginDataSource:
  setImmediate(function() {
      Java.perform(function() {
          var targetClass = 'nep.zxc.catpaw.data.LoginDataSource';
          var methodName = 'login';
          var gclass = Java.use(targetClass);
          gclass[methodName].overload("java.lang.String").implementation = function(arg0) {
              var loginUser = Java.use("nep.zxc.catpaw.data.model.LoggedInUser").$new("12345", "admin");
              var resultClass = Java.use("nep.zxc.catpaw.data.Result$Success");
              var ret = resultClass.$new(loginUser);
              return ret;
          }
      });
  });
  
  # 触摸事件还原:
  def get_x(v):
      x = []
      for i in range(4):
          tmp = str(hex(v[i+4]))[2:]
          if len(tmp) == 1: tmp = "0" + tmp
          x.append(tmp)
      x.reverse()
      return int("".join(x), 16)
  
  def get_y(v):
      y = []
      for i in range(4):
          tmp = str(hex(v[i+4]))[2:]
          if len(tmp) == 1: tmp = "0" + tmp
          y.append(tmp)
      y.reverse()
      return int("".join(y), 16)
  
  def is_x(v):
      return v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x35 and v[3] == 0x00
  
  def is_y(v):
      return v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x36 and v[3] == 0x00
  
  with open("1666666666", "rb") as fr:
      rd = fr.read()
  
  for i in range(16, len(rd), 24):
      v = rd[i:i+8]
      if is_x(v): print(get_x(v), end=",")
      if is_y(v): print(get_y(v))
one_liner: NepnepxCATCTF CatPaw: Android 小米备份 + Frida hook 绕 login + /dev/input/event1 触摸事件还原画图。
lesson: |
  - 小米备份 = 7zip 压缩包, 内部含 apk + /data/data 应用数据
  - Frida hook LoginDataSource.login 绕密码验证
  - /dev/input/event1 是 Linux input 子系统, 16 字节 / event (type/code/value/timestamp)
  - 03003500 = EV_ABS ABS_MT_POSITION_X, 03003600 = EV_ABS ABS_MT_POSITION_Y
  - 触摸事件还原: 大端 4 字节 value 字段 → 像素坐标
  - flag 藏在画图里 (CatCTF{...})
quality: high
---

# NepnepxCATCTF CatPaw 题目详解

> 来源: ctfiot.com 89529

## 题目分析

小米备份文件，7zip 解压得到 apk。

```bash
7z x catpaw.ab
# 得到 apk
```

## Frida Hook 绕验证

```javascript
setImmediate(function() {
    Java.perform(function() {
        var targetClass = 'nep.zxc.catpaw.data.LoginDataSource';
        var methodName = 'login';
        var gclass = Java.use(targetClass);
        gclass[methodName].overload("java.lang.String").implementation = function(arg0) {
            var loginUser = Java.use("nep.zxc.catpaw.data.model.LoggedInUser").$new("12345", "admin");
            var resultClass = Java.use("nep.zxc.catpaw.data.Result$Success");
            var ret = resultClass.$new(loginUser);
            return ret;
        }
    });
});
```

> hook 之后直接显示通过，并没有给出 flag

## /dev/input/event1 触摸事件

so 库读 `/dev/input/event1` 并保存到应用目录（如 `1666666666`）：

```bash
# 抓取触摸事件
getevent -lt /dev/input/event1

# 重放触摸事件
cat 1666666666 >> /dev/input/event1
```

## 触摸事件格式

每个 event 16 字节：
- type(2) + code(2) + value(4) + timestamp(8)

```
03003500 = EV_ABS ABS_MT_POSITION_X (X 轴)
03003600 = EV_ABS ABS_MT_POSITION_Y (Y 轴)
```

## 还原坐标

```python
def get_x(v):
    x = []
    for i in range(4):
        tmp = str(hex(v[i+4]))[2:].zfill(2)
        x.append(tmp)
    x.reverse()
    return int("".join(x), 16)

def is_x(v):
    return v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x35 and v[3] == 0x00

def is_y(v):
    return v[0] == 0x03 and v[1] == 0x00 and v[2] == 0x36 and v[3] == 0x00

with open("1666666666", "rb") as fr:
    rd = fr.read()

for i in range(16, len(rd), 24):
    v = rd[i:i+8]
    if is_x(v): print(get_x(v), end=",")
    if is_y(v): print(get_y(v))
```

## 评价

NepnepxCATCTF CatPaw 高难度 Android 逆向题：
- **小米备份** 7zip 解压
- **Frida hook** 绕 LoginDataSource.login
- **/dev/input/event1** 触摸事件还原
- **EV_ABS** type=3 + code=53/54 (X/Y) 格式

适用读者：Android 逆向 / 触摸事件分析 / Frida hook
