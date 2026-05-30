# 【WP】第七届“湖湘杯” leaker|设计思路与解析

> 原文: https://www.ctfiot.com/15097.html
> ID: 15097

本题由NanoApe师傅提供，赛后将该题的设计思路公开，供大家学习交流。

本题的 idea 来源于互联网公司内部的用于防泄密的数字水印。

数字水印

“数字水印”一词是由Andrew Tirkel和Charles Osborne于1992年12月提出，并于次年与Gerard Rankin一起成功地嵌入、提取了扩频掩密水印。

数字水印是一种隐蔽地嵌入到音频、视频或图像数据等信号的标记，这个标记并不影响原有的信号，它通常用于验证数据的真实性、完整性，或者标识其所有者的信息，起到版权保护的作用。

与传统的物理水印一样，数字水印通常只能在特定条件下（如在使用了一些算法后）才能被感知。传统水印可以应用于可见媒体（如图像或视频），而数字水印的信号可以是音频、图片、视频、文本或者3D模型，一个信号也可能携带几个不同的数字水印。

隐写术和数字水印都是采用隐写技术将数据隐蔽地嵌入到信号中，但前者旨在实现人类感官上的不可感知性，而数字水印的重心在于鲁棒控制。

数字水印的一种应用是追踪溯源。水印被嵌入到每个分布点的数字信号中，如果找到作品的副本，则可以从副本中检索水印，从而得知分发的来源。

writeup

解压题目附件，得到一张截图。

我们先用 Stegsolve 读取图片，看一下图片各个层面的信息。我们发现图片是 RGBA 模式，而 Alpha 通道只有 255 和 254 两种取值，说明最低位有问题。

很容易发现像素分布存在一定规律，那么我们后面研究的重点就从这里展开。

先单独提取出来得到 01 矩阵。对于水印题，我们要做的事情就是找规律。一般来说，为了做到随机截取图片任意一块还能完整读取水印包含的信息，水印会将想要隐藏的信息重复填写，达到抗修改的效果，所以可以尝试先寻找数据的规律。

首先可以发现，行存在重复出现的规律，周期是 76 行，也就是说第 1 行的数据和第 77 行的数据是一样的。
看起来行与行之间还是有点重复的规律，于是我们取出第 1 行所代表的 01 序列的前缀，大概取前 40 个 01 数据就好，然后在图中查找，发现这串 01 序列前缀同样出现在了第 3,5,7… 行中。

通过分析我们可以发现数据隔两行就会重复一次，因此我们可以将分析数据的范围缩小成两行。

然后我们再尝试查找这两行有没有什么重复的模式，发现这两行内出现了很多次 2×4 的 0 矩阵，而每两个 0 矩阵之间的信息都是一样的，这让我们又可以将范围缩小。到这里我们就得到了完整的一份信息经过加密后的结果。

接着我们发现第一行每隔 4 位都为 0，可以猜测是 ASCII 码的最高位，于是猜测每 2×4 个矩阵代表一个字符的 ASCII 码。

通过分析 ASCII 码的 01 分布规律，我们发现第二行第二列的格子上的 01 分布是不均匀的，因此我们可以猜测该地方为 ASCII 的第 4 位， 再根据第二行第一列以及第一行第二列的 01 分布情况，结合 [0-9a-zA-Z] 的 ASCII 码在各个二进制位上的 01 分布情况，进行一一对应，最后推测出解读方法：

1
3
5
7

2
4
6
8

END

春秋GAME伽玛实验室

会定期分享赛题赛制设计、解题思路……

如果你日常有一些技术研究和好的设计思路

或在赛后对某道题有另辟蹊径的想法

欢迎找到春秋GAME投稿哦～

联系vx:cium0309


```
from PIL import Image
import numpy as np
import random
import base64

im = Image.open('leaker.png')
im = np.asarray(im)
x, y, z = im.shape

print(im.shape)

c = []
for j in range(y):
    c.append(1 - im[0, j, 3] // 255)
    c.append(1 - im[1, j, 3] // 255)

c = ''.join([str(x) for x in c])
c = c[:c.find('00000000')]
flag = ''.join([chr(int(c[i:i+8], 2)) for i in range(0, len(c), 8)])

print(flag)
print(base64.b64decode(flag.encode()))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/0-1638445626.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/4-1638445627.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/7-1638445628.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/1-1638445629.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/6-1638445629.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/4-1638445630.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/9-1638445630.png)