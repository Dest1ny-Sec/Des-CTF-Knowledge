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
```



```
nohup java -jar admin-api.jar > admin-api.file 2>&1 &
nohup java -jar cloud.jar > cloud.file 2>&1 &
nohup java -jar market.jar > market.file 2>&1 &
nohup java -jar ucenter-api.jar > xucenter-api.file 2>&1 &
nohup java -jar exchange.jar > exchange.file 2>&1 &
```



```
npm run dev
```



```
%USERPROFILE%AppDataRoamingMicrosoftWindowsPowerShellPSReadLineConsoleHost_history.txt
```



```
wsl -u root
service mysql start
```



```
show global variables like "%datadir%";
```



```
SHOW VARIABLES LIKE 'gen%';
```



```
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
```



```
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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1668774030.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1668774030.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668774030.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668774031.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1668774032.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1668774033.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668774034.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1668774035.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668774036.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1668774037.png)