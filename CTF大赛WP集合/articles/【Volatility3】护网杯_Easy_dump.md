# 【Volatility3】护网杯_Easy_dump

> 原文: https://www.ctfiot.com/180914.html
> ID: 180914

前言

因为近期有备赛需求，并且比赛强制要求使用 Volatility3 进行取证，故产生这篇文章，这题对刚入门取证的我来说有不小的难度，但整体打下来还是比较轻松，难点主要在于 Volatility3 的文献较少，使用和 Volatility2 版本有较大的差异，整体复盘请看题解部分，希望对之后 Volatility3 上手的师傅提供帮助，另外本文特别感谢 @零溢出 师傅的无私帮助，最后列出一些 Volatility3 有价值的一些材料

Volatility3 使用笔记

Volatility3 使用入门笔记

Volatility3 官方文档

【内存取证】Volatility3 快速上手

使用的是 vigenere（维吉尼亚密码）加密，密钥是 aeolus

加密信息被删除了，需要我们手动恢复，也就是说message.img内有文件被删除


```
python vol.py -f D:
ShenTouvolatility3-developvenveasy_dump.img info.Info
python vol.py -f D:
ShenTouvolatility3-developvenveasy_dump.img windows.pslist
python vol.py -o ./outputdir/ -f D:
ShenTouvolatility3-developvenveasy_dump.img windows.memmap --pid 2616 --dump
strings -e l pid.2616.dmp | grep "flag"
python vol.py -f D:
ShenTouvolatility3-developvenveasy_dump.img windows.filescan
python vol.py -o .outputdir -f D:
ShenTouvolatility3-developvenveasy_dump.img windows.dumpfiles --physaddr 0x2408c460
import matplotlib.pyplot as plt
import numpy as np

x = []
y = []
with open('hint.txt','r') as f:
   datas = f.readlines()
   for data in datas:
        arr = data.split(' ')
        x.append(int(arr[0]))
        y.append(int(arr[1]))
     
plt.plot(x,y,'ks',ms=1)
plt.show()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1715562560.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1715562561.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1715562563.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1715562564.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/9-1715562564.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1715562566.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1715562566.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1715562567.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1715562568.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1715562569.png)