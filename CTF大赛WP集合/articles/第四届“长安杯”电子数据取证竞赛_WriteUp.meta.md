---
title: 第四届"长安杯"电子数据取证竞赛 WriteUp
contest: 长安杯
year: 2022
difficulty: medium
vuln_type: forensic_disk
tags: [取证,Java后台,nohup,mysql,Frida-Hook,Android脱壳,Java扩展欧几里得逆向,4字符爆破]
attack_chain: 计算机取证: ens33网卡配置+5个java jar后台(admin-api/cloud/market/ucenter-api/exchange)+npm run dev|服务器取证: powershell历史+%USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt+ wsl+service mysql start|SHOW VARIABLES LIKE 'gen%' 显示生成列|Frida-Hook: Java.perform attach()改写java.lang.String.equals打印所有比较|手机取证: Android加固脱壳|Java逆向: OooO扩展欧几里得函数+4字符4重for爆破flag (iArr[6]={1197727043,1106668192,...}+objArr[6]={'x','1',':','A','z','}'})
key_payload: nohup java -jar admin-api.jar > admin-api.file 2>&1 &|SHOW VARIABLES LIKE 'gen%';|Frida hook: HookClass = Java.classFactory.use('java.lang.String'); HookClass.equals.implementation = function(obj){ console.log(this + ' equals ' + obj); return ret; }|private long[] OooO(long j, long j2): if j==0 return {0,1}; return {((j2/j)*OooO[0])+OooO[1], OooO[0]}; (扩展欧几里得)|int j = str.charAt(0) << 16; j = j | (str.charAt(1) << 'b'); j = j | (str.charAt(2) << 24); j = str.charAt(3) | j;|for ig1,ig2,ig3,ig4 in 33..127: 4字符爆破 OooO0O0(subStr, 5) → 验证iArr[num] - j == ((Integer)objArr[num]).intValue()
one_liner: 第四届长安杯电子数据取证(虚拟币交易诈骗+USTD币+HT币+勒索+Java 5服务后台+nohup日志+Frida Hook java.lang.String.equals+扩展欧几里得逆向+4字符4重爆破)
lesson: 1) Java后台取证:nohup java -jar xxx.jar启动5个微服务; 2) MySQL生成列:SHOW VARIABLES LIKE 'gen%'; 3) PSReadLine历史记录取证:ConsoleHost_history.txt路径固定; 4) Frida-Hook Java类:Java.classFactory.use+equals.implementation打印所有比较; 5) 扩展欧几里得Java逆向:OooO(j, j2)递归实现; 6) 4字符爆破:33-127 ASCII范围+扩展欧几里得比较验证
quality: high
---

## 备注

原文(https://www.ctfiot.com/76314.html)2022年11月第四届长安杯电子数据取证竞赛,案情:某地警方接到虚拟币交易网站诈骗案,USDT币购买HT币,充值后无法提现,手机被恶意软件锁定勒索。

### 题目详情

**服务器取证**
- 后台:`nohup java -jar admin-api.jar/cloud.jar/market.jar/ucenter-api.jar/exchange.jar` + `npm run dev`
- 网卡:`/etc/sysconfig/network-scripts/ifcfg-ens33`
- 历史:`%USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`
- WSL: `wsl -u root` + `service mysql start`
- MySQL生成列:`SHOW VARIABLES LIKE 'gen%';`

**程序功能分析 - Frida-Hook**
```js
Java.perform(function () {
    var application = Java.use('android.app.Application');
    application.attach.overload('android.content.Context').implementation = function(context){
        var result = this.attach(context);
        var classloader = context.getClassLoader();
        Java.classFactory.loader = classloader;
        var HookClass = Java.classFactory.use('java.lang.String');
        HookClass.equals.implementation = function(obj){
            var ret = this.equals(obj);
            console.log(this + ' equals ' + obj);
            return ret;
        }
    }
});
```

**Java逆向 - 扩展欧几里得**
```java
private long[] OooO(long j, long j2) {
    if (j == 0) return new long[]{0, 1};
    long[] OooO = OooO(j2 % j, j);
    return new long[]{((j2 / j) * OooO[0]) + OooO[1], OooO[0]};
}
```

**4字符爆破**
```java
public boolean OooO0O0(String str, int num) {
    int j = str.charAt(0) << 16;
    j = j | (str.charAt(1) << 'b');  // 'b' = 0x62
    j = j | (str.charAt(2) << 24);
    j = str.charAt(3) | j;
    int[] iArr = {1197727043, 1106668192, 312918557, 1828680848, 1668105873, 1728985862};
    Object[] objArr = {'x', '1', ':', 'A', 'z', '}'};
    if (iArr[num] - j != ((Integer) objArr[num]).intValue()) return false;
    return true;
}
```
- 4字符每段比较 `iArr[num] - j == (char)objArr[num]`
- 4重for循环33-127爆破

## 评级

- **quality: high** — 完整电子数据取证流程(计算机+服务器+手机+程序分析),Frida Hook+Java扩展欧几里得逆向+4字符爆破都是实战高阶技术
- **vuln_type: forensic_disk** — 主分类取证(电子数据)
- 实战价值:长安杯是国内最大电子数据取证赛事,题型涵盖服务端日志+手机脱壳+逆向+反编译
