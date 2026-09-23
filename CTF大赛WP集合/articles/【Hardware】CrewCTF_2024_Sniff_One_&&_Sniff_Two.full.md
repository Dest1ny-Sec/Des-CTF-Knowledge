---
title: 【Hardware】CrewCTF 2024 Sniff One && Sniff Two
contest: CrewCTF
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags:
- hardware
- logic-analyzer
- Saleae
- SPI-sniff
- RGB-encoding
- two-bit-plane
- color-decode
- numpy-packbits
- PIL-Image
attack_chain: Saleae 逻辑分析仪抓 SPI/MOSI 信号 + 解析时钟 + 双 bit 平面 (黑/红) numpy 重组 + 136x249 RGB 图像还原 + 隐藏 flag 在色块内容中
key_payload: 'width=136 height=249  buf_a 黑平面 buf_b 红平面  color_mapping = {0: 白, 1: 黑, 2: 红}'
one_liner: CrewCTF 2024 硬件题 Sniff One/Two，逻辑分析仪抓 SPI 信号 + numpy 双 bit 平面重组 136x249 RGB 图像。
lesson: Saleae Logic 2 导出 raw binary 后用 numpy packbits/unpackbits 重组位平面；RGB 双通道编码（黑/红）是硬件 LCD 显示常见方案；136x249 是常见电子墨水屏分辨率。
quality: high
full_path: 【Hardware】CrewCTF_2024_Sniff_One_&&_Sniff_Two.full.md
meta_path: 【Hardware】CrewCTF_2024_Sniff_One_&&_Sniff_Two.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【Hardware】CrewCTF 2024 Sniff One && Sniff Two。CrewCTF 2024 硬件题 Sniff One/Two，逻辑分析仪抓 SPI 信号 + numpy 双 bit 平面重组 136x249 RGB 图像。。经验：Saleae Logic 2 导出 raw binary 后用 numpy packbits/unpackbits 重组...
category: misc
subcategory: misc_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/213017.html
reasoning_chain:
- 拿到 Saleae Logic 2 抓的 .sal 录制 → 触发点：SPI 协议 MOSI/MISO/CLK
- 解析 SPI clock 频率 + 采样 MOSI 数据 → 假设：电子墨水屏刷新
- 识别屏幕分辨率 136×249 → 假设：黑白+红三色电子纸
- 双 bit plane 重组：buf_a 黑/​buf_b 红 + color_mapping {0:白,1:黑,2:红}
- numpy packbits/unpackbits reshape (249,136) → PIL.Image → 动作：输出 PNG
- 查看图像 → flag 在色块内容中
failed_attempts:
- 试图单 bit plane 显示 → 黑红叠加丢色
- 试图 240×320 LCD 分辨率 → 不匹配电子墨水屏
- 试图 Saleae Analyzer 协议解码 → 太慢，直接 numpy
key_observations:
- 电子墨水屏双 bit 平面是常见方案（黑白+红/黄）
- 136×249 = 常见电子墨水屏分辨率
- numpy packbits/unpackbits 是位图重组最常用
- 颜色映射 {0:白,1:黑,2:红} 是嵌入式显示惯例
prerequisites:
- Saleae Logic 2 逻辑分析仪使用
- SPI 协议 MOSI/CLK 抓取
- numpy packbits/unpackbits
- PIL.Image 图像构造
---
# 【Hardware】CrewCTF 2024 Sniff One && Sniff Two

> 原文: https://www.ctfiot.com/213017.html
> ID: 213017

CrewCTF 2024 硬件题目

Sniff One

Sniff Two

buf_a = numpy.packbits(numpy.where(region == BLACK, 0, 1)).tolist()
buf_b = numpy.packbits(numpy.where(region == RED, 1, 0)).tolist()

buf_a_unpacked = np.unpackbits(np.array(buf_a, dtype=np.uint8))
buf_b_unpacked = np.unpackbits(np.array(buf_b, dtype=np.uint8))

width = 136
height = 249
buf_a = buf_a_unpacked[:
height * width].reshape((height, width))
buf_b = buf_b_unpacked[:
height * width].reshape((height, width))

color_mapping = {
 0:(255,255,255), # 白色
 1:(0,0,0),       # 黑色
 2:(255,0,0)      # 红色  
}

buf = np.zeros((height,width), dtype=np.uint8)

for i in range(height):
 for j in range(width):
  if buf_a[i,j] == 0:   # 黑色
   buf[i,j] = 1
  elif buf_b[i,j] == 1: # 红色
   buf[i,j] = 2
  else:
   buf[i,j] = 0      # 白色

image_array = np.zeros((height, width, 3), dtype=np.uint8)

for y in range(height):
 for x in range(width):
  image_array[y,x] = color_mapping[buf[y,x]] # 修改对应位置的颜色

image = Image.fromarray(image_array,'RGB')
image.show()

参

考

https://mwlik.github.io/2024-08-05-crewctf-2024-sniff-challenge/

https://xz.aliyun.com/t/15357

完整脚本：

import csv
import time
import numpy as np
from PIL import Image

def display(buf_a, buf_b):
 width = 136
 height = 249

 color_mapping = {
  0:(255,255,255), # 白色
  1:(0,0,0),       # 黑色
  2:(255,0,0)      # 红色  
 }
 buf_a_unpacked = np.unpackbits(np.array(buf_a, dtype=np.uint8))
 buf_b_unpacked = np.unpackbits(np.array(buf_b, dtype=np.uint8))

 buf_a = buf_a_unpacked[:
height*width].reshape((height,width))
 buf_b = buf_b_unpacked[:
height*width].reshape((height,width))

 buf = np.zeros((height,width), dtype=np.uint8)

 for i in range(height):
  for j in range(width):
   if buf_a[i,j] == 0:
    buf[i,j] = 1
   elif buf_b[i,j] == 1:
    buf[i,j] = 2
   else:
    buf[i,j] = 0

 image_array = np.zeros((height, width, 3), dtype=np.uint8)

 for y in range(height):
  for x in range(width):
   image_array[y,x] = color_mapping[buf[y,x]]

 image = Image.fromarray(image_array,'RGB')
 image.show()

with open("./capture.csv") as file:
 buf_a = []
 buf_b = []
 in_packet = False
 in_buf_a = False
 in_buf_b = False
 my_table = csv.reader(file) 
 header = next(my_table) # 跳过第一行的标题
 for line in my_table:
  MOSI = int(line[2],16)
  D_C = int(line[3],16)
  if D_C == 0x00:    # 如果是command
   if MOSI == 0x01: # command 是 0x01 的话表示是数据包
    in_packet = True # 表示这是一张图片
   elif MOSI == 0x20:  # command 是 0x20 的话表示是图片传输完了
    in_packet = False
    display(buf_a, buf_b) # 展示图片
    buf_a = []
    buf_b = []
   elif MOSI == 0x24:  # 如果是 0x24 的话表示的 buf_a 的内容
    in_buf_a = True
   elif MOSI == 0x26:  # 如果是 0x24 的话表示的 buf_b 的内容
    in_buf_b = True
    in_buf_a = False

  elif D_C == 0Xff:  # 如果是 data
   if in_packet:  # 先判断是不是数据包
    if in_buf_a:  # 是 buf_a 的内容的话就往 buf_a 里面添加
     buf_a.append(MOSI)
    elif in_buf_b: # 否则是 buf_b 的内容的话就往 buf_b 里面添加
     buf_b.append(MOSI)


```
buf_a = numpy.packbits(numpy.where(region == BLACK, 0, 1)).tolist()
buf_b = numpy.packbits(numpy.where(region == RED, 1, 0)).tolist()
buf_a_unpacked = np.unpackbits(np.array(buf_a, dtype=np.uint8))
buf_b_unpacked = np.unpackbits(np.array(buf_b, dtype=np.uint8))
width = 136
height = 249
buf_a = buf_a_unpacked[:
height * width].reshape((height, width))
buf_b = buf_b_unpacked[:
height * width].reshape((height, width))
color_mapping = {
 0:(255,255,255), # 白色
 1:(0,0,0),       # 黑色
 2:(255,0,0)      # 红色  
}

buf = np.zeros((height,width), dtype=np.uint8)

for i in range(height):
 for j in range(width):
  if buf_a[i,j] == 0:   # 黑色
   buf[i,j] = 1
  elif buf_b[i,j] == 1: # 红色
   buf[i,j] = 2
  else:
   buf[i,j] = 0      # 白色

image_array = np.zeros((height, width, 3), dtype=np.uint8)

for y in range(height):
 for x in range(width):
  image_array[y,x] = color_mapping[buf[y,x]] # 修改对应位置的颜色

image = Image.fromarray(image_array,'RGB')
image.show()
import csv
import time
import numpy as np
from PIL import Image

def display(buf_a, buf_b):
 width = 136
 height = 249

 color_mapping = {
  0:(255,255,255), # 白色
  1:(0,0,0),       # 黑色
  2:(255,0,0)      # 红色  
 }
 buf_a_unpacked = np.unpackbits(np.array(buf_a, dtype=np.uint8))
 buf_b_unpacked = np.unpackbits(np.array(buf_b, dtype=np.uint8))

 buf_a = buf_a_unpacked[:
height*width].reshape((height,width))
 buf_b = buf_b_unpacked[:
height*width].reshape((height,width))

 buf = np.zeros((height,width), dtype=np.uint8)

 for i in range(height):
  for j in range(width):
   if buf_a[i,j] == 0:
    buf[i,j] = 1
   elif buf_b[i,j] == 1:
    buf[i,j] = 2
   else:
    buf[i,j] = 0

 image_array = np.zeros((height, width, 3), dtype=np.uint8)

 for y in range(height):
  for x in range(width):
   image_array[y,x] = color_mapping[buf[y,x]]

 image = Image.fromarray(image_array,'RGB')
 image.show()

with open("./capture.csv") as file:
 buf_a = []
 buf_b = []
 in_packet = False
 in_buf_a = False
 in_buf_b = False
 my_table = csv.reader(file) 
 header = next(my_table) # 跳过第一行的标题
 for line in my_table:
  MOSI = int(line[2],16)
  D_C = int(line[3],16)
  if D_C == 0x00:    # 如果是command
   if MOSI == 0x01: # command 是 0x01 的话表示是数据包
    in_packet = True # 表示这是一张图片
   elif MOSI == 0x20:  # command 是 0x20 的话表示是图片传输完了
    in_packet = False
    display(buf_a, buf_b) # 展示图片
    buf_a = []
    buf_b = []
   elif MOSI == 0x24:  # 如果是 0x24 的话表示的 buf_a 的内容
    in_buf_a = True
   elif MOSI == 0x26:  # 如果是 0x24 的话表示的 buf_b 的内容
    in_buf_b = True
    in_buf_a = False

  elif D_C == 0Xff:  # 如果是 data
   if in_packet:  # 先判断是不是数据包
    if in_buf_a:  # 是 buf_a 的内容的话就往 buf_a 里面添加
     buf_a.append(MOSI)
    elif in_buf_b: # 否则是 buf_b 的内容的话就往 buf_b 里面添加
     buf_b.append(MOSI)
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