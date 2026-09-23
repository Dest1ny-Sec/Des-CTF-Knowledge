---
title: 第四届"长安杯"电子数据取证竞赛 WriteUp
contest: 长安杯
year: 2022
difficulty: medium
vuln_type: forensic_disk
tags:
- 取证
- Java后台
- nohup
- mysql
- Frida-Hook
- Android脱壳
- Java扩展欧几里得逆向
- 4字符爆破
attack_chain: '计算机取证: ens33网卡配置+5个java jar后台(admin-api/cloud/market/ucenter-api/exchange)+npm run dev|服务器取证: powershell历史+%USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt+ wsl+service mysql start|SHOW VARIABLES LIKE ''gen%'' 显示生成列|Frida-Hook: Java.perform attach()改写java.lang.String.equals打印所有比较|手机取证: Android加固脱壳|Java逆向: OooO扩展欧几里得函数+4字符4重for爆破flag (iArr[6]={1197727043,1106668192,...}+objArr[6]={''x'',''1'','':'',''A'',''z'',''}''})'
key_payload: 'nohup java -jar admin-api.jar > admin-api.file 2>&1 &|SHOW VARIABLES LIKE ''gen%'';|Frida hook: HookClass = Java.classFactory.use(''java.lang.String''); HookClass.equals.implementation = function(obj){ console.log(this + '' equals '' + obj); return ret; }|private long[] OooO(long j, long j2): if j==0 return {0,1}; return {((j2/j)*OooO[0])+OooO[1], OooO[0]}; (扩展欧几里得)|int j = str.charAt(0) << 16; j = j | (str.charAt(1) << ''b''); j = j | (str.charAt(2) << 24); j = str.charAt(3) | j;|for ig1,ig2,ig3,ig4 in 33..127: 4字符爆破 OooO0O0(subStr, 5) → 验证iArr[num] - j == ((Integer)objArr[num]).intValue()'
one_liner: 第四届长安杯电子数据取证(虚拟币交易诈骗+USTD币+HT币+勒索+Java 5服务后台+nohup日志+Frida Hook java.lang.String.equals+扩展欧几里得逆向+4字符4重爆破)
lesson: 1) Java后台取证:nohup java -jar xxx.jar启动5个微服务; 2) MySQL生成列:SHOW VARIABLES LIKE 'gen%'; 3) PSReadLine历史记录取证:ConsoleHost_history.txt路径固定; 4) Frida-Hook Java类:Java.classFactory.use+equals.implementation打印所有比较; 5) 扩展欧几里得Java逆向:OooO(j, j2)递归实现; 6) 4字符爆破:33-127 ASCII范围+扩展欧几里得比较验证
quality: high
full_path: 第四届“长安杯”电子数据取证竞赛_WriteUp.full.md
meta_path: 第四届“长安杯”电子数据取证竞赛_WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 第四届"长安杯"电子数据取证竞赛 WriteUp。第四届长安杯电子数据取证(虚拟币交易诈骗+USTD币+HT币+勒索+Java 5服务后台+nohup日志+Frida Hook java.lang.String.equals+扩展欧几里得逆向+4字符4重爆破)。经验：1) Java后台取证:nohup java -jar xxx.jar启动5个微服务; 2) MySQL生成列:SHOW...
category: forensic
subcategory: disk_forensics
tools_used:
- Java
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/76314.html
reasoning_chain:
- 触发点：USTD 币诈骗案 + 服务器镜像 + 5 个 Java 后台服务 → 假设：分析 Java jar
- 动作：nohup java -jar admin-api.jar/cloud.jar/market.jar/ucenter-api.jar/exchange.jar → 观察：5 服务目录
- 触发点：MySQL 数据存放点 → 假设：show global variables like '%datadir%' 找 datadir
- 动作：SHOW VARIABLES → 观察：datadir 在 /var/lib/mysql
- 触发点：Frida Hook java.lang.String.equals → 假设：拦截加密/比较逻辑
- 动作：Java.perform + Java.use('java.lang.String').equals.implementation → 观察：拿到加密前后比较
- 触发点：扩展欧几里得逆推 RSA 参数 → 假设：RSA 4 字符验证
- 动作：OooO(j, 4294967296L) 计算 32-bit 同余 → 观察：还原 flag
- 触发点：PowerShell 历史记录 → 假设：ConsoleHost_history.txt 含密码
failed_attempts:
- Frida 启动直接 hook → 失败：需要绕过加固
- MySQL 数据硬读 → 失败：未启动服务
- RSA 单字符爆破 → 失败：算法是 4 字符一块
key_observations:
- 电子数据取证竞赛常见 5 服务：admin-api/cloud/market/ucenter-api/exchange
- Frida Hook String.equals 可拦截密码比较逻辑
- RSA 4 字符小块验证可单组爆破
- PowerShell 历史记录 (.ConsoleHost_history.txt) 是 Windows 取证常考点
prerequisites:
- Java jar 后台服务分析
- Frida Java.perform API
- 扩展欧几里得算法
- Windows PowerShell 历史取证
---
# 第四届“长安杯”电子数据取证竞赛 WriteUp

> 原文: https://www.ctfiot.com/76314.html
> ID: 76314

第四届“长安杯”电子数据取证竞赛 WriteUp

竞赛案情

案件情况

某地警方接到受害人报案称其在某虚拟币交易网站遭遇诈骗，该网站号称使用“USTD 币”购买所谓的“HT 币”，受害人充值后不但“HT 币”无法提现、交易，而且手机还被恶意软件锁定勒索。警方根据受害人提供的虚拟币交易网站调取了对应的服务器镜像并对案件展开侦查。

考试方向

计算机取证分析；

服务器/网站取证分析；

手机取证分析；

程序功能分析。


```
vi /etc/sysconfig/network-scripts/ifcfg-ens33
nohup java -jar admin-api.jar > admin-api.file 2>&1 &
nohup java -jar cloud.jar > cloud.file 2>&1 &
nohup java -jar market.jar > market.file 2>&1 &
nohup java -jar ucenter-api.jar > xucenter-api.file 2>&1 &
nohup java -jar exchange.jar > exchange.file 2>&1 &
npm run dev
%USERPROFILE%AppDataRoamingMicrosoftWindowsPowerShellPSReadLineConsoleHost_history.txt
wsl -u root
service mysql start
show global variables like "%datadir%";
SHOW VARIABLES LIKE 'gen%';
Java.perform(function () {
    var application = Java.use('android.app.Application');
    application.attach.overload('android.content.Context').implementation = function(context){
        var result = this.attach(context);
        var classloader = context.getClassLoader();
        Java.classFactory.loader = classloader;
        // 加固方法用classloader找到被加固的类
        var HookClass = Java.classFactory.use('java.lang.String');
        HookClass.equals.implementation = function(obj){
            var ret = this.equals(obj)
            console.log(this + ' equals ' + obj);
            return ret;
        }
    }
});
package src.an;

import org.junit.Test;

public class Boom {
    private int[] OooO0oO = {1197727163, 1106668241, 312918615, 1828680913, 1668105995, 1728985987};

    private long[] OooO(long j, long j2) {
        if (j == 0) {
            return new long[]{0, 1};
        }
        long[] OooO = OooO(j2 % j, j);
        return new long[]{((j2 / j) * OooO[0]) + OooO[1], OooO[0]};
    }

    public boolean OooO0O0(String str, int num) {
        // 改成单次的！，每次传入四个字符，num从0开始
        int j = str.charAt(0) << 16;
        j = j | (str.charAt(1) << 'b');
        j = j | (str.charAt(2) << 24);
        j = str.charAt(3) | j;
        try {
            int[] iArr = {1197727043, 1106668192, 312918557, 1828680848, 1668105873, 1728985862};
            Object[] objArr = {'x', '1', ':', 'A', 'z', '}'};
            if (iArr[num] - j != ((Integer) objArr[num]).intValue()) {
                return false;
            }
            return true;
        } catch (Exception unused) {
            if (((OooO(j, 4294967296L)[0] % 4294967296L) + 4294967296L) % 4294967296L != this.OooO0oO[num]) {
                return false;
            }
            return true;
        }
    }

    @Test
    public void tryBoom() {
        String allStrings = new String();
        int j = 0;
        for (int i = 33; i < 127; i++) {
            char c = (char) i;
            allStrings += String.valueOf(c);
        }
        for (int ig1 = 0; ig1 < allStrings.length(); ig1++) {
            String subStr1 = allStrings.substring(ig1, ig1 + 1);
            for (int ig2 = 0; ig2 < allStrings.length(); ig2++) {
                String subStr2 = allStrings.substring(ig2, ig2 + 1);
                for (int ig3 = 0; ig3 < allStrings.length(); ig3++) {
                    String subStr3 = allStrings.substring(ig3, ig3 + 1);
                    for (int ig4 = 0; ig4 < allStrings.length(); ig4++) {
                        String subStr4 = allStrings.substring(ig4, ig4 + 1);
                        String subStr = subStr1 + subStr2 + subStr3 + subStr4;
                        if (OooO0O0(subStr, 5)) {
                            System.out.println(subStr);
                        }
                    }
                }
            }

        }

    }

}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]