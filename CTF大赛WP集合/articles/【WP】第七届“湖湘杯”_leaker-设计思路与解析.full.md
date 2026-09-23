---
title: 【WP】第七届"湖湘杯" leaker 设计思路与解析
contest: 湖湘杯
year: 2021
difficulty: medium
vuln_type: stego_image
tags:
- digital-watermark
- RGBA-alpha-LSB
- 01-matrix-pattern
- period-76-rows
- 2x4-block-ASCII
- leaker-source
- frequency-anti-trim
attack_chain: 1. Stegsolve 读 RGBA 模式 + Alpha 通道只有 255/254 → 最低位藏数据/2. 行重复周期 76 行 + 隔两行重复 → 缩小分析范围/3. 2x4 0 矩阵之间是相同信息 + 每隔 4 位为 0（ASCII 最高位）/4. 解读：1,3,5,7 行 + 2,4,6,8 列 + END 结束
key_payload: Alpha LSB 255/254  周期 76 行  2x4 矩阵 ASCII 编码
one_liner: 第七届湖湘杯 leaker 数字水印题，RGBA Alpha LSB 提取 01 矩阵 + 2x4 块 ASCII 编码还原。
lesson: 数字水印 = 抗修改隐写术，重复填充实现任意位置可读；RGBA Alpha 通道 255/254 区分是 LSB 隐写信号；2x4 0 矩阵作为分隔符是常见水印编码方式。
quality: high
full_path: 【WP】第七届“湖湘杯”_leaker-设计思路与解析.full.md
meta_path: 【WP】第七届“湖湘杯”_leaker-设计思路与解析.meta.md
images_removed: true
images_removed_count: 7
schema_version: v3.0.0-P0
summary: 【WP】第七届"湖湘杯" leaker 设计思路与解析。第七届湖湘杯 leaker 数字水印题，RGBA Alpha LSB 提取 01 矩阵 + 2x4 块 ASCII 编码还原。。经验：数字水印 = 抗修改隐写术，重复填充实现任意位置可读；RGBA Alpha 通道 255/254 区分是 LSB 隐写信...
category: misc
subcategory: stego
tools_used:
- Stegsolve
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 7
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/15097.html
reasoning_chain:
- 拿到 leaker.png → 触发点：题目名 'leaker' + 数字水印 → 动作：Stegsolve 读 RGBA 通道
- 观察：Alpha 通道只有 255 和 254 两种值 → 假设：最低位藏数据 → 动作：提取 alpha%2 序列
- 像素有规律重复 → 假设：数字水印抗截取用周期填充 → 动作：按行找重复周期
- 观察：周期 76 行 → 假设：水印每隔两行重复一次 → 动作：取第 1 行 + 第 3 行做分析
- 两行内发现大量 2×4 全 0 矩阵 → 假设：每个 2×4 块代表一个字符 → 动作：看块间 01 分布
- 第一行每隔 4 位为 0 → 假设：是 ASCII 最高位 → 动作：尝试 2 行 8 列 ASCII 编码
- ASCII 推导：行 1,3,5,7 给高 4 位 + 行 2,4,6,8 给低 4 位 → 观察：还原 base64 串
- 动作：base64 解码 → 观察：得到 flag
failed_attempts:
- 试图用 zsteg/steghide 跑全部通道 → 失败：水印是抗修改隐写，不在常规 stego 工具范围
- 试图 LSB 提取 RGB 而非 Alpha → 失败：RGB 是真实颜色，没藏数据
- 试图直接拼接第 1 行所有 01 → 失败：周期没找对，混入了重复块
key_observations:
- 数字水印 = 抗截取隐写，核心特征是周期重复填充
- RGBA Alpha 通道只有 255/254 是 LSB 隐写的最强信号
- 2×4 0 矩阵作为分隔符是常见水印编码边界
- 水印解码要先识别周期，再缩范围到最小重复单元
- base64 是 flag 在水印里再包一层编码的常用招
prerequisites:
- Stegsolve 通道分析与 LSB 原理
- 数字水印抗修改特性理解
- Python PIL/numpy 像素处理
- base64/ASCII 编码基础
---
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

联系vx:
cium0309


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

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]