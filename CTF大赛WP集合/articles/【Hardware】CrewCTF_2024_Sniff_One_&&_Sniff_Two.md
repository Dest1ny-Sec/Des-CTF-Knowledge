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
buf_a = buf_a_unpacked[:height * width].reshape((height, width))
buf_b = buf_b_unpacked[:height * width].reshape((height, width))

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

 buf_a = buf_a_unpacked[:height*width].reshape((height,width))
 buf_b = buf_b_unpacked[:height*width].reshape((height,width))

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
```



```
buf_a_unpacked = np.unpackbits(np.array(buf_a, dtype=np.uint8))
buf_b_unpacked = np.unpackbits(np.array(buf_b, dtype=np.uint8))
```



```
width = 136
height = 249
buf_a = buf_a_unpacked[:height * width].reshape((height, width))
buf_b = buf_b_unpacked[:height * width].reshape((height, width))
```



```
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
```



```
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

 buf_a = buf_a_unpacked[:height*width].reshape((height,width))
 buf_b = buf_b_unpacked[:height*width].reshape((height,width))

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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/4-1730541744.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1730541745.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1730541745.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/4-1730541746.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1730541746.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1730541747.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1730541747.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1730541748.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1730541748.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1730541749.png)