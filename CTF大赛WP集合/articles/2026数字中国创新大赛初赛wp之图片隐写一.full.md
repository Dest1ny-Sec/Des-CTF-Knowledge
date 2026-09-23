---
title: 2026 数字中国创新大赛初赛 wp 之图片隐写一（LSB 多通道爆破）
contest: 2026 数字中国创新大赛
year: 2026
difficulty: easy
vuln_type:
- stego_image
- misc_unknown
tags:
- 数字中国 2026 初赛
- 图片隐写一
- LSB 最低位 steg
- zsteg --lsb1.png
- G 通道 stride [1::3]
- start 0-7 step 1..len/256 爆破
- msb 拼字节
- isprintable 过滤
- 5 张图片轮试
attack_chain:
- '5 张图轮试: zsteg -a --lsb1.png'
- '自写爆破脚本: 假设 G 通道 [1::3] (单色)'
- '三层循环: start 0-7 (起始位) × step 1..len//(L*8) (间隔) × msb/lsb 拼字节'
- 答案 32 字符 → 至少 256 bit → 爆破到正确 G 通道偏移
- decoded.isprintable() 过滤
key_payload: G = rgb[1::3]; bits = [G[start + i*step] & 1 for i in range(L*8)]
one_liner: 2026 数字中国图片隐写一：zsteg + LSB 1 比特 + G 通道 + start/step 爆破 + msb 拼字节 + isprintable 过滤。
lesson: LSB 隐写爆破套路：start=起始位 0-7，step=间隔 1..len/(L*8)，msb/lsb 两种拼接，isprintable 过滤；zsteg 是 1.8 步完成 90% 情况。
quality: medium
full_path: 2026数字中国创新大赛初赛wp之图片隐写一.full.md
meta_path: 2026数字中国创新大赛初赛wp之图片隐写一.meta.md
images_removed: true
images_removed_count: 5
schema_version: v3.0.0-P0
summary: '2026 数字中国创新大赛初赛 wp 之图片隐写一（LSB 多通道爆破）。2026 数字中国图片隐写一：zsteg + LSB 1 比特 + G 通道 + start/step 爆破 + msb 拼字节 + isprintable 过滤。。关键路径：5 张图轮试: zsteg -a --lsb1.png → 自写爆破脚本: 假设 G 通道 [1::3] (单色) → 三层循环: start ...'
category: misc
subcategory: stego
subcategories:
- stego
- misc_other
tools_used:
- zsteg
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 5
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/307065.html
reasoning_chain:
- 5 张图轮试 zsteg -a --lsb1.png → 触发点：LSB 最低位隐写
- 假设：G 通道 [1::3] 单色 → 动作：自写爆破脚本 → 观察：候选 start/step 组合
- '三层循环: start 0-7 (起始位) × step 1..len//(L*8) (间隔) × msb/lsb 拼字节'
- 假设：答案 32 字符 → 至少 256 bit → 动作：爆破到正确 G 通道偏移
- decoded.isprintable() 过滤 → 观察：拿到 flag 字符串
failed_attempts:
- zsteg 默认参数 → 失败：start/step 不在 zsteg 默认枚举范围
- 只测 R 通道 → 失败：本题藏在 G 通道 stride [1::3]
- 手工拼字节 → 失败：32 字符需 256 bit，自动化爆破更快
key_observations:
- LSB 隐写爆破套路：start=起始位 0-7，step=间隔 1..len/(L*8)，msb/lsb 两种拼接，isprintable 过滤
- zsteg 是 1.8 步完成 90% 情况的瑞士军刀
- G 通道 [1::3] 单色提取是特殊隐写模式
- 5 张图轮试 + 多通道枚举是 LSB 通用解法
- isprintable() 过滤 = 减少假阳性的关键
prerequisites:
- zsteg LSB 隐写工具
- PIL/numpy 像素操作（RGB 通道分离）
- Python 字节拼接（msb/lsb 两种顺序）
- isprintable() 字符串验证
---
# 2026数字中国创新大赛初赛wp之图片隐写一

> 原文: https://www.ctfiot.com/307065.html
> ID: 307065

2026数字中国创新大赛初赛wp之图片隐写一

缘起

我最喜欢的就是杂项了，很有意思，尤其是隐写，可是这道题确实有点料，浪费不少时间，不过还好，最后还是做出来了。

题目

题目附件我放在网盘：

https://cloud.189.cn/t/ymEby2uQRn6b（访问码：4zlr）

分析

题目看起来很简单：

虽然图片很多，但是实际就5张，就算每个都试试也不是问题

已经明确说了是lsb，而且是最后一位，范围以及限制死了

zsteg--lsb1.png

zsteg -a--lsb1.png

图片是lsb隐写

最后一位

假设是平均间隔，前面可以空几位

假设他给的答案例子，格式是一样的，就是32位的（题目答案例子）

组合1： 颜色，就是可能是单色（r,g,b）,或者三色都有（rgb）

组合2： 排列：lsb或者msb

从第几位开始存储

每隔多少位存储

img= Image.open("5.png")rgb= img.convert("RGB").tobytes()G= rgb[1::3]L=32 #1forstart in range(0,8): #2 forstep in range(1,(len(G)//(L*8))+1): #3 bits=[G[start + i * step] & 1 for i in range(L * 8)] result=[] fori in range(0, len(bits),8): b=0 forbit in bits[i:i+8]: b=(b<<1) | bit # msb 4 result.append(b) decoded_string= bytes(result).decode(errors='ignore') ifdecoded_string.isprintable(): #5 print(decoded_string)

前面分析的结果设置，G通道是试到第二个试出来的

第一层循环，假设隐藏数据开头从第几位开始，先爆一个字节试试

第二层循环，平均间隔：总长度除以答案长度，就表示最长间隔，所以从1到这个数，爆破

然后按照8个bit组成一个字节，这里有2种可能，lsb或者msb，就是高低位，这个是试出来的，2次就行

答案应该是可打印的，所以加了个过滤，方便人眼看，其实可以按照答案模板更多的过滤一些，不过就此也够一眼出结果了

2026数字中国创新大赛初赛wp之俩签到题

2026数字中国创新大赛数字安全赛道writeup之web题目一


```
zsteg--lsb1.png
zsteg -a--lsb1.png
img= Image.open("5.png")rgb= img.convert("RGB").tobytes()G= rgb[1::3]L=32 #1forstart in range(0,8): #2 forstep in range(1,(len(G)//(L*8))+1): #3 bits=[G[start + i * step] & 1 for i in range(L * 8)] result=[] fori in range(0, len(bits),8): b=0 forbit in bits[i:i+8]: b=(b<<1) | bit # msb 4 result.append(b) decoded_string= bytes(result).decode(errors='ignore') ifdecoded_string.isprintable(): #5 print(decoded_string)
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]