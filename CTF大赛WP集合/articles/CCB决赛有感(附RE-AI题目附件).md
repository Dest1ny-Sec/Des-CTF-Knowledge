# CCB决赛有感(附RE/AI题目附件)

> 原文: https://www.ctfiot.com/306981.html
> ID: 306981

“赛场很大,灯光很亮,茶歇很好吃  Ψ(￣∀￣)Ψ”

真是吃了没有pwn手的亏了,java基础也太薄弱了…..

话说,现场大佬好多，膜拜膜拜….

来张赛场照

实网渗透：

扫目录

找到一个schema.sql文件

找到账号密码,后台文件上传点上传文件，抓包修改后缀为php,成功拿到初步shell

上线 supershell ，发现find有suid权限，直接提权

find / -perm -4000 -type f -exec ls -la {} 2>/dev/null ;

/usr/bin/find . -exec /bin/bash -p ; -quit

拿到flag了,后面fscan扫描拿到一个app.java和一个protokms（一个邮件网关的软件）一下触及到盲区了…潦草退场了。

专项能力赛

DokiLogic

下载题目附件给了一个Renpy的游戏，打开就提示让输出answer,再没什么东西。 在路径下找到一个scrpit.rpyc文件不出意外就是flag的逻辑所在了

但是!我没有解密这个文件的脚本 /(ㄒoㄒ)/~~ ,以下来自赛后复现….

用unrpyc解密rpyc:
https://github.com/CensoredUsername/unrpyc

拿到script.rpy

重点逻辑就是,主程序运行后会释放一个1.exe,然后

捕获其输出，在游戏开始时要求输入一个字符串，将该字符串每个字符与 35 异或后，与之前捕获的 exe 输出比较，若相等则提示用

flag{输入}

格式提交，否则重试。

因此，正确的输入就是 exe 输出与 35 再次异或的结果

直接把硬编码的1.exe粘出来用python脚本直接获取输出然后异或就可以拿到flag了，我就说怎么这么多解…. 还是储备太少了,没有解密脚本。

附上exp

import subprocess
import os

_f = b'MZx90x00...'  # rpy里的_f也就是1.exe的硬编码数据

with open('temp.exe', 'wb') as f:
    f.write(_f)

output = subprocess.run('temp.exe', stdout=subprocess.PIPE).stdout.decode('latin-1')
os.remove('temp.exe')

flag_input = "".join(chr(ord(c) ^ 35) for c in output)
print(f'flag{{{flag_input}}}')

最后的最后,公众号后台回复:
CCB2026拿题目附件(RE/AI)


```
find / -perm -4000 -type f -exec ls -la {} 2>/dev/null ;
/usr/bin/find . -exec /bin/bash -p ; -quit
import subprocess
import os

_f = b'MZx90x00...'  # rpy里的_f也就是1.exe的硬编码数据

with open('temp.exe', 'wb') as f:
    f.write(_f)

output = subprocess.run('temp.exe', stdout=subprocess.PIPE).stdout.decode('latin-1')
os.remove('temp.exe')

flag_input = "".join(chr(ord(c) ^ 35) for c in output)
print(f'flag{{{flag_input}}}')
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865021-wxsync-2026-05-65c81eadbc60f3e30c0524a87aa20729.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865023-wxsync-2026-05-c202e167ddd96f2551e06217010a4924.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865024-wxsync-2026-05-6a1badcbbffd0b831b454ad962848698.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865027-wxsync-2026-05-23cfc9bf3284b028fcf391e9c52865d2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865028-wxsync-2026-05-3b9ada70b909bef753ce94492a68fd55.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865030-wxsync-2026-05-19c4eeeeaeb0366beeba6d73a1994571.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865032-wxsync-2026-05-6a537925d7ded0575c3ce89df7267357.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865033-wxsync-2026-05-5a5f611b882a39855781183c99de31bb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865035-wxsync-2026-05-dbef3af2b8c8727bf1c62fdc26836db8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/05/1777865037-wxsync-2026-05-bc3641d0abf4dd738d65b2b5a6d5301f.png)