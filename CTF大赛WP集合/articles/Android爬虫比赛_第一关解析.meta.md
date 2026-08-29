---
title: Android 爬虫比赛 第一关解析
contest: 爬虫 CTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [yuanrenxue match2022, frida hook, Sign.sign, page+timestamp, retrofit2, BodyObservable, lambda$initListeners$2, Python累加, 看雪论坛]
attack_chain:
  - jadx 反编译 com.yuanrenxue.match2022
  - 翻页时抓包, 发现 page + t + sign 三个参数
  - frida hook ChallengeOneFragment.lambda$initListeners$2(OooOO0O) 看 this.page.value
  - sb = "page=" + page + timestamp → bArr = bytearray utf8
  - frida hook Sign.sign(byte[]) 拿加密结果
  - Python rpc.exports.callsecretfunctionedy(bArr) 调 Java Sign.sign
  - 100 页累加 value 即 flag count
key_payload: 'page + timestamp 拼接 / Sign.sign(bArr) 加密 / retrofit2 BodyObservable 返回值 / 100 页累加 / frida rpc.exports'
one_liner: 猿人学 Android 爬虫第一关 — frida hook ChallengeOneFragment + Sign.sign + Python rpc.exports.callsecretfunctionedy + 100 页 value 累加得 flag count。
lesson: frida + rpc.exports 是 Java <-> Python 跨语言调标准做法;byte[] 参数先 bytearray('utf-8') 再传;sign 加密是 page+timestamp 拼接后单函数。
quality: high
---

# Android 爬虫比赛 第一关解析

## 速读
猿人学 match2022 Android 爬虫第一关 — frida + Python 联合解题。

## 环境
- frida 12.8.20
- Python 3.8.10
- jadx-gui 1.2.0
- fiddler

## 步骤
1. jadx 反编译 → `ChallengeOneFragment` 内部类 `lambda$initListeners$2`
2. 抓包看 `page=`, `sign=`, `t=timestamp`
3. frida hook `lambda$initListeners$2(OooOO0O)` 看 `this.page.value` + 返回 `BodyObservable`
4. sb = `page=` + page + timestamp → bArr
5. frida hook `Sign.sign(byte[])` 拿加密结果
6. Python 通过 `rpc.exports.callsecretfunctionedy(bArr)` 调 Java 加密
7. POST `https://appmatch.yuanrenxue.com/app1` 拿 data
8. 100 页累加 value → flag count

## frida rpc 脚本
```javascript
var result;
function callDYFun(bArr) {
    Java.perform(function () {
        var ss = Java.use('com.yuanrenxue.match2022.security.Sign');
        var str = Java.use("java.lang.String");
        var res = str.$new(ss.$new().sign(bArr));
        result = str.valueOf(res);
    });
    return result;
}
rpc.exports = {
    callsecretfunctionedy: callDYFun,
};
```

## Python 累加
```python
for i in range(1, 101):
    s = f'page={i}' + str(time_)
    bArr = [x for x in bytearray(s, 'utf-8')]
    res = script.exports.callsecretfunctionedy(bArr)
    payload = {'page': str(i), 'sign': res, 't': time_}
    r = requests.post("https://appmatch.yuanrenxue.com/app1", data=payload, headers=header2, verify=False)
    for v in r.json()['data']:
        count += int(v['value'])
print("flag count:", count)
```
