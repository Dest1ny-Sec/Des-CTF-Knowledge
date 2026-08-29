---
title: NKCTF 2024 re VM?VM! WP (Wireworld 元胞自动机)
contest: NKCTF
year: 2024
difficulty: hard
vuln_type: reverse
tags: [Wireworld 元胞自动机, 2324x2324 像素图, IDA 数据提取, PIL 绘图, decode XOR bit 流]
attack_chain: |
  1. 题目: NKCTF 2024 re VM?VM! — 2324x2324 像素图模拟 Wireworld 元胞自动机
  2. sub_1570 是加密主逻辑, 加载不出但需输出 1
  3. Wireworld 元胞自动机规则:
     - 空 → 空
     - 电子头 → 电子尾
     - 电子尾 → 导体
     - 当仅有一个或仅有两个电子头的邻居是导体时, 导体 → 电子头
  4. 1 是终点, 到达就返回 1
  5. 数据提取: IDA api 读 0x4018-0x535D93 字节
  6. PIL 渲染: 0x914x0x914 像素图, 5 颜色:
     - 0x01 红 (电子头)
     - 0xEC 蓝
     - 0x11 绿 (导体)
     - 0xCD 黑
     - 0x80 黄
     - 0xEA 青
  7. Wireworld Simulator 在线模拟: 信号消失 = 异或 (XOR) 逻辑门
  8. decode XOR: key bit 流 (key0/1/2/3) 还原 res 序列 → long_to_bytes 转 flag
key_payload: |
  # 数据提取 (IDA):
  START_ADDR = 0x4018
  END_ADDR = 0x535D93
  BYTES_PER_LINE = 16
  for ea in range(START_ADDR, END_ADDR + 1):
      byte_value = idaapi.get_byte(ea)
      hex_string = '0x{:02X}'.format(byte_value)
      f.write(hex_string + (',' if bytes_written % BYTES_PER_LINE else ',\n'))
  
  # PIL 渲染:
  from PIL import Image
  s = [...]  # 字节流
  img = Image.new('RGB', (0x914, 0x914), (255, 255, 255))
  pixels = img.load()
  for i in range(len(s)):
      i_row = i // 0x914
      i_col = i % 0x914
      if s[i] == 0x1: pixels[i_row, i_col] = (255, 0, 0)    # 红
      elif s[i] == 0xEC: pixels[i_row, i_col] = (0, 0, 255)   # 蓝
      elif s[i] == 0x11: pixels[i_row, i_col] = (0, 255, 0)   # 绿
      elif s[i] == 0xCD: pixels[i_row, i_col] = (0, 0, 0)     # 黑
      elif s[i] == 0x80: pixels[i_row, i_col] = (255, 255, 0) # 黄
      elif s[i] == 0xEA: pixels[i_row, i_col] = (0, 255, 255) # 青
  img.save('image.png')
  
  # decode XOR bit 流:
  from Crypto.Util.number import long_to_bytes
  def decode(key):
      key_string = long_to_bytes(int("".join([str(i) for i in key]), 2))
      res = [0]
      for i in range(len(key)-1):
          res.append(res[i] ^ key[i])
      flag = long_to_bytes(int("".join([str(i) for i in res]), 2))
      print(flag)
  
  key0 = [1, 0, 1, 1, 0, 0, 1, 0]
  key1 = [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, ...]  # 100+ bit
  decode(key0)
  decode(key1)
one_liner: NKCTF 2024 re VM?VM! — 2324x2324 Wireworld 元胞自动机 (0x914 像素) + XOR bit 流解码还原 flag。
lesson: |
  - Wireworld 元胞自动机 4 状态: 空/导体/电子头/电子尾 + 状态转换规则
  - 1 个或 2 个电子头邻居是导体 → 导体变电子头 (异或逻辑门)
  - PIL 渲染 0x914x0x914 像素图是标准逆向技巧
  - IDA api.get_byte 大量地址提取数据
  - decode XOR bit 流: res = [0]; res[i+1] = res[i] ^ key[i]
  - Wireworld Simulator 在线工具: https://danprince.github.io/wireworld/
quality: high
---

# NKCTF 2024 re VM?VM! WP

> 来源: ctfiot.com 197341

## 题目分析

- `sub_1570` 太大，加载不出来
- 是加密主逻辑，目的是需要输出 1
- 实际上是一个 2324x2324 (0x914) 的像素图
- 模拟 **Wireworld 元胞自动机**

## Wireworld 元胞自动机

```
组成:
- 空
- 导体
- 电子头
- 电子尾

每代变化:
- 空 → 空
- 电子头 → 电子尾
- 电子尾 → 导体
- 当仅有一个或仅有两个电子头的邻居是导体时, 导体 → 电子头

1 就是终点，到达就返回 1
```

> 根据资料知道这是在模拟 Wireworld 元胞自动机

## 数据提取 (IDA Python)

```python
import idaapi
import idautils

START_ADDR = 0x4018
END_ADDR = 0x535D93
BYTES_PER_LINE = 16

with open('output.txt', 'w') as f:
    bytes_written = 0
    for ea in range(START_ADDR, END_ADDR + 1):
        byte_value = idaapi.get_byte(ea)
        hex_string = '0x{:02X}'.format(byte_value)
        if bytes_written > 0 and bytes_written % BYTES_PER_LINE != 0:
            f.write(',')
        f.write(hex_string)
        bytes_written += 1
        if bytes_written % BYTES_PER_LINE == 0:
            f.write(',\n')
```

## PIL 渲染

```python
from PIL import Image
s = [...]  # 字节流
img = Image.new('RGB', (0x914, 0x914), (255, 255, 255))
pixels = img.load()
for i in range(len(s)):
    i_row = i // 0x914
    i_col = i % 0x914
    if s[i] == 0x1: pixels[i_row, i_col] = (255, 0, 0)    # 红
    elif s[i] == 0xEC: pixels[i_row, i_col] = (0, 0, 255)   # 蓝
    elif s[i] == 0x11: pixels[i_row, i_col] = (0, 255, 0)   # 绿
    elif s[i] == 0xCD: pixels[i_row, i_col] = (0, 0, 0)     # 黑
    elif s[i] == 0x80: pixels[i_row, i_col] = (255, 255, 0) # 黄
    elif s[i] == 0xEA: pixels[i_row, i_col] = (0, 255, 255) # 青
img.save('image.png')
```

## Wireworld Simulator

```url
https://danprince.github.io/wireworld/
```

**关键发现**：信号消失 = 异或 (逻辑门) 原理（电子头"邻居=1 或 2 时传导"等价于 XOR 逻辑）

## decode XOR bit 流

```python
from Crypto.Util.number import long_to_bytes

def decode(key):
    key_string = long_to_bytes(int("".join([str(i) for i in key]), 2))
    res = [0]
    for i in range(len(key)-1):
        tmp = res[i] ^ key[i]
        res.append(tmp)
    flag = long_to_bytes(int("".join([str(i) for i in res]), 2))
    print(flag)

key0 = [1, 0, 1, 1, 0, 0, 1, 0]
key1 = [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, ...]  # 100+ bit
key2 = [0, 1, 1, 1, 0, 1, 1, 1, ...]
key3 = [1, 0, 1, 0, 1, 1, 0, 0, ...]
decode(key0)
decode(key1)
decode(key2)
decode(key3)
```

## 评价

NKCTF 2024 re VM?VM! 高质量 Reverse 题：
- **Wireworld 元胞自动机** 抽象 VM（信号传播 = 逻辑门）
- **0x914x0x914 = 2324x2324 像素图** 渲染技巧
- **5 种颜色编码** 0x01/0xEC/0x11/0xCD/0x80/0xEA
- **decode XOR bit 流** 还原 4 段 flag

适合研究**非传统计算模型**（元胞自动机）和**逆向工程中数据可视化**的同学。
