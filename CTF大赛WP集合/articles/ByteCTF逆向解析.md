# ByteCTF逆向解析

> 原文: https://www.ctfiot.com/208437.html
> ID: 208437

一

babyapk

首先分析了下java层的东西，然后发现和平常做的安卓不太一样，搜索后发现这是使用Flutter框架写的安卓apk，所以从网上找了下资料后发现可以使用blutter工具，具体的使用在此不再详说，网上有很多详细资料，在使用该工具初步解析apk后获得如下文件。

其中的main.dart可以说已经看清了该apk的主要逻辑。

该test函数可以轻易看到和验证有关的大量逻辑。

在下面发现最主要的是调用了 m3N4B5V6()函数进行判断。

右边的注释则说明了该函数所属的package。

进而找到simple.dart。

接着跟进。

在这里我一度思路中断，因为我对Rust以及FFI调用的实现并不了解。

但是我注意到其中大量出现的API和Simple字样，于是在IDA中进行搜索发现该字符。

向上查看交叉引用发现了加密函数。

同时从加密函数这里继续向上查看引用多次最终索引到了这里。

这里是我之前搜索过m3n4b5v6分析过的函数，但是由于其中内部逻辑很多很乱，我实在没有分析下去，才转战dart文件去分析。除去前面这些过程实际上我还对native层的这些函数包括app.so内的一些和交互有关以及可疑的函数进行了多次fridaHOOK，但也成效甚微，不过还好总算找到加密逻辑处了。

然后这里也是因为之前HOOK时发现很多函数没反应于是猜测有长度检测，不断改变长度查看HOOK情况得到长度为0x2d，{}内为36位。

分析加密函数，倒着分析，得到该后半部分大致逻辑，判断为纯纯的z3。

用z3约束后发现约束出的数组都是可显字符，即32e750c8fb214562af22973fb5176b9c，猜测离flag很接近了。

from z3 import * 

# 声明 v58 数组，每个变量为 16 位
for j in range(4):
 v58 = [BitVec(f'v58[{i}]', 32) for i in range(8)] # 假设有8个变量

 # 密文数组
 cmp = [
 0x0001EE59, 0x0000022A, 0x00001415, 0x00040714, 0x000013E0, 0x000008B8, 0xFFFDCEA0, 0x0000313B, 
 0x0003D798, 0xFFFFFE6B, 0x00000C4E, 0x00023884, 0x0000008D, 0x00001DB4, 0xFFFC1328, 0x00001EAC, 
 0x00043C64, 0x0000142B, 0xFFFFF622, 0x00023941, 0xFFFFEF6D, 0x0000120C, 0xFFFBD30F, 0x00001EBE, 
 0x00045158, 0xFFFFEF66, 0x00001D3F, 0x0004C46B, 0xFFFFF97A, 0x00001BFD, 0xFFFBA235, 0x00001ED2
 ]

 # 创建求解器
 s = Solver()

 # 添加变量的范围限制 (0 <= num <= 65535)
 for i in range(8):
 s.add(v58[i] >= 0, v58[i] <= 0x10FFFF)

 # 添加约束条件
 num2 = v58[2]
 num3 = v58[3]
 num0 = v58[0]
 num1 = v58[1]
 num4 = v58[4]
 num5 = v58[5]
 num6 = v58[6]
 num7 = v58[7]

 # 计算公式的约束条件
 s.add(num7 + num1 * num3 * num5 - (num0 + num6 + num2 * num4) == cmp[0+j*8])
 s.add(num3 - num4 - num0 * num5 + num7 * num1 + num2 + num6 == cmp[1+j*8])
 s.add(num0 * num5 - (num4 + num7 * num1) + num2 + num6 * num3 == cmp[2+j*8])
 s.add(num1 + num4 * num0 - (num7 + num2) + num6 * num5 * num3 == cmp[3+j*8])
 s.add(num5 * num3 + num1 + num2 * num4 - (num6 + num7 * num0) == cmp[4+j*8])
 s.add(num0 * num5 + num1 * num3 + num2 - (num6 + num4 * num7) == cmp[5+j*8])
 s.add(num7 - num1 + num2 * num5 + num6 - num0 * num4 * num3 == cmp[6+j*8])

 # 最后一轮的约束
 s.add(num3 - num7 - (num1 + num5) + num4 * num0 + num6 * num2 == cmp[7+j*8])

 # 求解
 if s.check() == sat:
 model = s.model()
 v58_values = [model[v58[i]].as_long() for i in range(8)]
 print("数组解是：", v58_values)
 else:
 print("没有解。")

这种逻辑的似乎涉及到编码转化，不影响flag的值。

这里发现了对-的约束，于是再根据很可显的字符串的长度为32，立马想到有四个-插在中间。

思考后感觉z3不好写而且情况也不多，于是直接写了穷举的爆破脚本。

from itertools import combinations

# 原始字符串
original_string = "32e750c8fb214562af22973fb5176b9c"

# 定义用于验证的 byte 数组（byte_18E46）
byte_18E46 = [ 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
 0x00, 0x00, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 
 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 
 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 
 0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
# 验证逻辑函数
def validate_hyphen_positions(input_str):
 byte = byte_18E46
 input_bytes = [ord(c) for c in input_str]
 
 # 模拟你提供的验证逻辑
 v2 = byte[input_bytes[0]]
 if v2 == 36:
 return False
 v3 = byte[input_bytes[v2]] + v2
 if v3 == 36:
 return False
 v4 = v3 + byte[input_bytes[v3]]
 if v4 == 36:
 return False
 v5 = v4 + byte[input_bytes[v4]]
 if v5 == 36:
 return False
 v6 = v5 + byte[input_bytes[v5]]
 if v6 == 36:
 return False
 v7 = v6 + byte[input_bytes[v6]]
 if v7 == 36:
 return False
 v8 = v7 + byte[input_bytes[v7]]
 if v8 == 36:
 return False
 v9 = v8 + byte[input_bytes[v8]]
 if v9 == 36:
 return False
 v10 = input_bytes[v9]
 if v10 != ord('-'):
 return False
 v12 = v9 + byte[input_bytes[v9]]
 if v12 == 36:
 return False
 v13 = v12 + byte[input_bytes[v12]]
 if v13 == 36:
 return False
 v14 = v13 + byte[input_bytes[v13]]
 if v14 == 36:
 return False
 v15 = v14 + byte[input_bytes[v14]]
 if v15 == 36:
 return False
 v16 = v15 + byte[input_bytes[v15]]
 if v16 == 36:
 return False
 v18 = input_bytes[v16]
 if v18 != ord('-'):
 return False
 v20 = v16 + byte[input_bytes[v16]]
 if v20 == 36:
 return False
 v21 = v20 + byte[input_bytes[v20]]
 if v21 == 36:
 return False
 v22 = v21 + byte[input_bytes[v21]]
 if v22 == 36:
 return False
 v23 = v22 + byte[input_bytes[v22]]
 if v23 == 36:
 return False
 v24 = v23 + byte[input_bytes[v23]]
 if v24 == 36:
 return False
 v25 = input_bytes[v24]
 if v25 != ord('-'):
 return False
 v27 = v24 + byte[input_bytes[v24]]
 if v27 == 36:
 return False
 v28 = v27 + byte[input_bytes[v27]]
 if v28 == 36:
 return False
 v29 = v28 + byte[input_bytes[v28]]
 if v29 == 36:
 return False
 v30 = v29 + byte[input_bytes[v29]]
 if v30 == 36:
 return False
 v31 = v30 + byte[input_bytes[v30]]
 if v31 == 36:
 return False
 v32 = input_bytes[v31]
 if v32 != ord('-'):
 return False
 
 return True

# 生成插入 '-' 的位置的组合
positions = list(combinations(range(len(original_string) + 1), 4)) # 选择 4 个插入位置

# 计数器
count = 0
valid_count = 0 # 成功验证的组合计数器

# 遍历所有组合
for pos in positions:
 temp_str = original_string
 # 插入时要注意位置的偏移，每次插入后，字符串长度增加
 for i, p in enumerate(pos):
 temp_str = temp_str[:p + i] + '-' + temp_str[p + i:] # 插入 '-' 并调整位置索引
 
 # 验证插入的 '-' 是否符合条件
 if validate_hyphen_positions(temp_str):
 print(f"Valid combination: {temp_str}")
 valid_count += 1 # 计数通过验证的组合
 
 # 计数
 count += 1

# 打印总次数
print(f"Total combinations: {count}")
print(f"Total valid combinations: {valid_count}")

最终Flag：ByteCTF{32e750c8-fb21-4562-af22-973fb5176b9c}

二

ByteBuffer

根据题目提示了解了下flatbuffer，大致明白就是把数据以某种形式序列化那种？转化为一维的数组这样子。

然后用010打开。

发现有很多的Edge，Dot字样。

所以大致能猜到这些线和点能画出来Flag。

于是将dot和Edge的数据分别提取一份喂给Gpt，然后它成功猜测到可能的数据结构：进而提取了所有的数据。

一开始Edge的分析成了两个坐标，后来才发现它的分析的起始坐标很有规律，于是猜到了是代表的下面的点的序号及之间的连接。

遂训练AI写出脚本解出。

import matplotlib.pyplot as plt

# 点的坐标数据
dot_coordinates = [
 (75, 75),(25, 75),(75, 25),(25, 25),(25, 125),(75, 125),(100, 75),(100, 25),(150, 25),(150, 75),
 (100, 125),(150, 125),(175, 75),(175, 25),(225, 25),(225, 75),(225, 125),(250, 75),(250, 25),(300, 25),
 (300, 75),(250, 125),(300, 125),(325, 75),(325, 25),(375, 75),(375, 25),(375, 125),(400, 75),(400, 25),
 (450, 25),(450, 75),(400, 125),(450, 125),(475, 75),(475, 25),(475, 125),(525, 75),(550, 75),(550, 25),
 (600, 25),(600, 75),(550, 125),(600, 125),(625, 75),(625, 25),(675, 25),(675, 75),(625, 125),(675, 125),
 (700, 75),(700, 25),(750, 25),(750, 75),(750, 125),(700, 125),(775, 75),(775, 25),(825, 25),(825, 75),
 (775, 125),(825, 125),(850, 75),(850, 25),(900, 25),(900, 75),(850, 125),(900, 125),(925, 75),(925, 25),
 (975, 25),(975, 75),(925, 125),(975, 125),(1000, 75),(1000, 25),(1050, 25),(1050, 75),(1000, 125),(1050, 125),
 (1075, 75),(1075, 25),(1125, 25),(1125, 75),(1125, 125),(1075, 125),(1150, 75),(1150, 25),(1200, 25),(1200, 75),
 (1200, 125),(1225, 75),(1225, 25),(1225, 125),(1275, 75),(1300, 75),(1300, 25),(1350, 25),(1350, 75),(1300, 125),
 (1350, 125),(1375, 75),(1375, 25),(1425, 25),(1425, 75),(1375, 125),(1425, 125),(1450, 75),(1450, 25),(1500, 25),
 (1500, 75),(1450, 125),(1500, 125),(1525, 75),(1525, 25),(1575, 25),(1575, 75),(1525, 125),(1575, 125),(1600, 75)
]

# 边的连接关系 (基于点的序号，序号从0开始)
edges = [
 (119, 117), (119, 118), (117, 114), (116, 115), (115, 114),
 (113, 111), (113, 112), (112, 108), (111, 108), (110, 109),
 (109, 108), (107, 105), (107, 106), (106, 102), (105, 102),
 (105, 104), (104, 103), (103, 102), (101, 99), (101, 100),
 (99, 96), (98, 97), (97, 96), (94, 92), (93, 92), (91, 90),
 (90, 89), (89, 88), (86, 81), (86, 85), (85, 84), (84, 83),
 (83, 82), (82, 81), (80, 78), (80, 79), (78, 75), (78, 77),
 (77, 76), (76, 75), (74, 73), (73, 69), (72, 69), (72, 71),
 (71, 70), (68, 66), (68, 67), (66, 63), (66, 65), (65, 64),
 (64, 63), (62, 60), (62, 61), (61, 57), (60, 57), (59, 58),
 (58, 57), (56, 51), (56, 55), (55, 54), (54, 53), (53, 52),
 (52, 51), (50, 48), (50, 49), (48, 45), (47, 46), (46, 45),
 (44, 42), (44, 43), (43, 39), (42, 39), (42, 41), (41, 40),
 (40, 39), (37, 35), (36, 35), (34, 33), (33, 29), (32, 29),
 (32, 31), (31, 30), (28, 26), (27, 26), (26, 24), (25, 24),
 (23, 21), (23, 22), (21, 18), (20, 19), (19, 18), (17, 16),
 (16, 15), (15, 14), (12, 11), (11, 7), (10, 7), (10, 9),
 (9, 8), (6, 1), (6, 5), (4, 3), (3, 1), (2, 1)
]

# 创建图形
plt.figure(figsize=(12, 12))

# 绘制点
for i, (x, y) in enumerate(dot_coordinates):
 plt.scatter(x, y, c='blue', zorder=2)
 plt.text(x, y, f"{i+1}", fontsize=8, ha='right', zorder=3)

# 绘制连接关系
for start, end in edges:
 x_values = [dot_coordinates[start-1][0], dot_coordinates[end-1][0]]
 y_values = [dot_coordinates[start-1][1], dot_coordinates[end-1][1]]
 plt.plot(x_values, y_values, 'k-', zorder=1)

# 优化显示
plt.title("Optimized Dot and Edge Connections")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.grid(True)
plt.axis('equal') # 保持比例相同
plt.show()

发现图还有点问题，第三个一看就很有特点，是7，于是镜像翻转。

flag：ByteCTF{327542185069230715865}

看雪ID：螺丝兔

https://bbs.kanxue.com/user-home-992277.htm

*本文为看雪论坛优秀文章，由 螺丝兔 原创，转载请注明来自看雪社区

# 往期推荐

1、Alt-Tab Terminator注册算法逆向

2、恶意木马历险记

3、VMP源码分析：反调试与绕过方法

4、Chrome V8 issue 1486342浅析

5、Cython逆向-语言特性分析

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
babyapk
```



```
from z3 import * 

# 声明 v58 数组，每个变量为 16 位
for j in range(4):
 v58 = [BitVec(f'v58[{i}]', 32) for i in range(8)] # 假设有8个变量

 # 密文数组
 cmp = [
 0x0001EE59, 0x0000022A, 0x00001415, 0x00040714, 0x000013E0, 0x000008B8, 0xFFFDCEA0, 0x0000313B, 
 0x0003D798, 0xFFFFFE6B, 0x00000C4E, 0x00023884, 0x0000008D, 0x00001DB4, 0xFFFC1328, 0x00001EAC, 
 0x00043C64, 0x0000142B, 0xFFFFF622, 0x00023941, 0xFFFFEF6D, 0x0000120C, 0xFFFBD30F, 0x00001EBE, 
 0x00045158, 0xFFFFEF66, 0x00001D3F, 0x0004C46B, 0xFFFFF97A, 0x00001BFD, 0xFFFBA235, 0x00001ED2
 ]

 # 创建求解器
 s = Solver()

 # 添加变量的范围限制 (0 <= num <= 65535)
 for i in range(8):
 s.add(v58[i] >= 0, v58[i] <= 0x10FFFF)

 # 添加约束条件
 num2 = v58[2]
 num3 = v58[3]
 num0 = v58[0]
 num1 = v58[1]
 num4 = v58[4]
 num5 = v58[5]
 num6 = v58[6]
 num7 = v58[7]

 # 计算公式的约束条件
 s.add(num7 + num1 * num3 * num5 - (num0 + num6 + num2 * num4) == cmp[0+j*8])
 s.add(num3 - num4 - num0 * num5 + num7 * num1 + num2 + num6 == cmp[1+j*8])
 s.add(num0 * num5 - (num4 + num7 * num1) + num2 + num6 * num3 == cmp[2+j*8])
 s.add(num1 + num4 * num0 - (num7 + num2) + num6 * num5 * num3 == cmp[3+j*8])
 s.add(num5 * num3 + num1 + num2 * num4 - (num6 + num7 * num0) == cmp[4+j*8])
 s.add(num0 * num5 + num1 * num3 + num2 - (num6 + num4 * num7) == cmp[5+j*8])
 s.add(num7 - num1 + num2 * num5 + num6 - num0 * num4 * num3 == cmp[6+j*8])

 # 最后一轮的约束
 s.add(num3 - num7 - (num1 + num5) + num4 * num0 + num6 * num2 == cmp[7+j*8])

 # 求解
 if s.check() == sat:
 model = s.model()
 v58_values = [model[v58[i]].as_long() for i in range(8)]
 print("数组解是：", v58_values)
 else:
 print("没有解。")
```



```
from itertools import combinations

# 原始字符串
original_string = "32e750c8fb214562af22973fb5176b9c"

# 定义用于验证的 byte 数组（byte_18E46）
byte_18E46 = [ 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 
 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
 0x00, 0x00, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 
 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 
 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 
 0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
# 验证逻辑函数
def validate_hyphen_positions(input_str):
 byte = byte_18E46
 input_bytes = [ord(c) for c in input_str]
 
 # 模拟你提供的验证逻辑
 v2 = byte[input_bytes[0]]
 if v2 == 36:
 return False
 v3 = byte[input_bytes[v2]] + v2
 if v3 == 36:
 return False
 v4 = v3 + byte[input_bytes[v3]]
 if v4 == 36:
 return False
 v5 = v4 + byte[input_bytes[v4]]
 if v5 == 36:
 return False
 v6 = v5 + byte[input_bytes[v5]]
 if v6 == 36:
 return False
 v7 = v6 + byte[input_bytes[v6]]
 if v7 == 36:
 return False
 v8 = v7 + byte[input_bytes[v7]]
 if v8 == 36:
 return False
 v9 = v8 + byte[input_bytes[v8]]
 if v9 == 36:
 return False
 v10 = input_bytes[v9]
 if v10 != ord('-'):
 return False
 v12 = v9 + byte[input_bytes[v9]]
 if v12 == 36:
 return False
 v13 = v12 + byte[input_bytes[v12]]
 if v13 == 36:
 return False
 v14 = v13 + byte[input_bytes[v13]]
 if v14 == 36:
 return False
 v15 = v14 + byte[input_bytes[v14]]
 if v15 == 36:
 return False
 v16 = v15 + byte[input_bytes[v15]]
 if v16 == 36:
 return False
 v18 = input_bytes[v16]
 if v18 != ord('-'):
 return False
 v20 = v16 + byte[input_bytes[v16]]
 if v20 == 36:
 return False
 v21 = v20 + byte[input_bytes[v20]]
 if v21 == 36:
 return False
 v22 = v21 + byte[input_bytes[v21]]
 if v22 == 36:
 return False
 v23 = v22 + byte[input_bytes[v22]]
 if v23 == 36:
 return False
 v24 = v23 + byte[input_bytes[v23]]
 if v24 == 36:
 return False
 v25 = input_bytes[v24]
 if v25 != ord('-'):
 return False
 v27 = v24 + byte[input_bytes[v24]]
 if v27 == 36:
 return False
 v28 = v27 + byte[input_bytes[v27]]
 if v28 == 36:
 return False
 v29 = v28 + byte[input_bytes[v28]]
 if v29 == 36:
 return False
 v30 = v29 + byte[input_bytes[v29]]
 if v30 == 36:
 return False
 v31 = v30 + byte[input_bytes[v30]]
 if v31 == 36:
 return False
 v32 = input_bytes[v31]
 if v32 != ord('-'):
 return False
 
 return True

# 生成插入 '-' 的位置的组合
positions = list(combinations(range(len(original_string) + 1), 4)) # 选择 4 个插入位置

# 计数器
count = 0
valid_count = 0 # 成功验证的组合计数器

# 遍历所有组合
for pos in positions:
 temp_str = original_string
 # 插入时要注意位置的偏移，每次插入后，字符串长度增加
 for i, p in enumerate(pos):
 temp_str = temp_str[:p + i] + '-' + temp_str[p + i:] # 插入 '-' 并调整位置索引
 
 # 验证插入的 '-' 是否符合条件
 if validate_hyphen_positions(temp_str):
 print(f"Valid combination: {temp_str}")
 valid_count += 1 # 计数通过验证的组合
 
 # 计数
 count += 1

# 打印总次数
print(f"Total combinations: {count}")
print(f"Total valid combinations: {valid_count}")
```



```
二
ByteBuffer
```



```
import matplotlib.pyplot as plt

# 点的坐标数据
dot_coordinates = [
 (75, 75),(25, 75),(75, 25),(25, 25),(25, 125),(75, 125),(100, 75),(100, 25),(150, 25),(150, 75),
 (100, 125),(150, 125),(175, 75),(175, 25),(225, 25),(225, 75),(225, 125),(250, 75),(250, 25),(300, 25),
 (300, 75),(250, 125),(300, 125),(325, 75),(325, 25),(375, 75),(375, 25),(375, 125),(400, 75),(400, 25),
 (450, 25),(450, 75),(400, 125),(450, 125),(475, 75),(475, 25),(475, 125),(525, 75),(550, 75),(550, 25),
 (600, 25),(600, 75),(550, 125),(600, 125),(625, 75),(625, 25),(675, 25),(675, 75),(625, 125),(675, 125),
 (700, 75),(700, 25),(750, 25),(750, 75),(750, 125),(700, 125),(775, 75),(775, 25),(825, 25),(825, 75),
 (775, 125),(825, 125),(850, 75),(850, 25),(900, 25),(900, 75),(850, 125),(900, 125),(925, 75),(925, 25),
 (975, 25),(975, 75),(925, 125),(975, 125),(1000, 75),(1000, 25),(1050, 25),(1050, 75),(1000, 125),(1050, 125),
 (1075, 75),(1075, 25),(1125, 25),(1125, 75),(1125, 125),(1075, 125),(1150, 75),(1150, 25),(1200, 25),(1200, 75),
 (1200, 125),(1225, 75),(1225, 25),(1225, 125),(1275, 75),(1300, 75),(1300, 25),(1350, 25),(1350, 75),(1300, 125),
 (1350, 125),(1375, 75),(1375, 25),(1425, 25),(1425, 75),(1375, 125),(1425, 125),(1450, 75),(1450, 25),(1500, 25),
 (1500, 75),(1450, 125),(1500, 125),(1525, 75),(1525, 25),(1575, 25),(1575, 75),(1525, 125),(1575, 125),(1600, 75)
]

# 边的连接关系 (基于点的序号，序号从0开始)
edges = [
 (119, 117), (119, 118), (117, 114), (116, 115), (115, 114),
 (113, 111), (113, 112), (112, 108), (111, 108), (110, 109),
 (109, 108), (107, 105), (107, 106), (106, 102), (105, 102),
 (105, 104), (104, 103), (103, 102), (101, 99), (101, 100),
 (99, 96), (98, 97), (97, 96), (94, 92), (93, 92), (91, 90),
 (90, 89), (89, 88), (86, 81), (86, 85), (85, 84), (84, 83),
 (83, 82), (82, 81), (80, 78), (80, 79), (78, 75), (78, 77),
 (77, 76), (76, 75), (74, 73), (73, 69), (72, 69), (72, 71),
 (71, 70), (68, 66), (68, 67), (66, 63), (66, 65), (65, 64),
 (64, 63), (62, 60), (62, 61), (61, 57), (60, 57), (59, 58),
 (58, 57), (56, 51), (56, 55), (55, 54), (54, 53), (53, 52),
 (52, 51), (50, 48), (50, 49), (48, 45), (47, 46), (46, 45),
 (44, 42), (44, 43), (43, 39), (42, 39), (42, 41), (41, 40),
 (40, 39), (37, 35), (36, 35), (34, 33), (33, 29), (32, 29),
 (32, 31), (31, 30), (28, 26), (27, 26), (26, 24), (25, 24),
 (23, 21), (23, 22), (21, 18), (20, 19), (19, 18), (17, 16),
 (16, 15), (15, 14), (12, 11), (11, 7), (10, 7), (10, 9),
 (9, 8), (6, 1), (6, 5), (4, 3), (3, 1), (2, 1)
]

# 创建图形
plt.figure(figsize=(12, 12))

# 绘制点
for i, (x, y) in enumerate(dot_coordinates):
 plt.scatter(x, y, c='blue', zorder=2)
 plt.text(x, y, f"{i+1}", fontsize=8, ha='right', zorder=3)

# 绘制连接关系
for start, end in edges:
 x_values = [dot_coordinates[start-1][0], dot_coordinates[end-1][0]]
 y_values = [dot_coordinates[start-1][1], dot_coordinates[end-1][1]]
 plt.plot(x_values, y_values, 'k-', zorder=1)

# 优化显示
plt.title("Optimized Dot and Edge Connections")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.grid(True)
plt.axis('equal') # 保持比例相同
plt.show()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/6-1728388809.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/10-1728388810.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/3-1728388810.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/7-1728388812.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/6-1728388812.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1728388813.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/5-1728388814.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1728388814.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/5-1728388815.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/10-1728388815.png)