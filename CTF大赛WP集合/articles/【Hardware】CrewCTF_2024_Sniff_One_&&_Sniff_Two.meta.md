---
title: 【Hardware】CrewCTF 2024 Sniff One && Sniff Two
contest: CrewCTF
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [hardware, logic-analyzer, Saleae, SPI-sniff, RGB-encoding, two-bit-plane, color-decode, numpy-packbits, PIL-Image]
attack_chain: Saleae 逻辑分析仪抓 SPI/MOSI 信号 + 解析时钟 + 双 bit 平面 (黑/红) numpy 重组 + 136x249 RGB 图像还原 + 隐藏 flag 在色块内容中
key_payload: width=136 height=249  buf_a 黑平面 buf_b 红平面  color_mapping = {0: 白, 1: 黑, 2: 红}
one_liner: CrewCTF 2024 硬件题 Sniff One/Two，逻辑分析仪抓 SPI 信号 + numpy 双 bit 平面重组 136x249 RGB 图像。
lesson: Saleae Logic 2 导出 raw binary 后用 numpy packbits/unpackbits 重组位平面；RGB 双通道编码（黑/红）是硬件 LCD 显示常见方案；136x249 是常见电子墨水屏分辨率。
quality: high
---

# 【Hardware】CrewCTF 2024 Sniff One && Sniff Two

## 概览
CrewCTF 2024 硬件题，使用 Saleae 逻辑分析仪抓 SPI 信号，通过 numpy 双 bit 平面重组 136x249 RGB 图像。

## 工具链
- **Saleae Logic 2**: 逻辑分析仪软件（抓 SPI/I2C/UART）
- **numpy**: packbits / unpackbits 位平面操作
- **PIL**: Image.fromarray 重建图像
- **逻辑分析仪硬件**: Saleae Logic Pro / 兼容

## 关键脚本
```python
import numpy as np
from PIL import Image

def display(buf_a, buf_b):
    width = 136
    height = 249
    color_mapping = {
        0: (255, 255, 255),  # 白色
        1: (0, 0, 0),        # 黑色
        2: (255, 0, 0)       # 红色
    }
    buf_a_unpacked = np.unpackbits(np.array(buf_a, dtype=np.uint8))
    buf_b_unpacked = np.unpackbits(np.array(buf_b, dtype=np.uint8))
    
    buf_a = buf_a_unpacked[:height*width].reshape((height, width))
    buf_b = buf_b_unpacked[:height*width].reshape((height, width))
    
    buf = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            if buf_a[i, j] == 0:
                buf[i, j] = 1       # 黑色
            elif buf_b[i, j] == 1:
                buf[i, j] = 2       # 红色
            else:
                buf[i, j] = 0       # 白色
    
    image_array = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            image_array[y, x] = color_mapping[buf[y, x]]
    
    image = Image.fromarray(image_array, 'RGB')
    image.show()
```

## 攻击链

### Stage 1: 抓信号
- 用 Saleae 抓 SPI 4 根线：CLK, MOSI, MISO, CS
- 导出 raw binary 或 CSV

### Stage 2: 解析双 bit 平面
- `buf_a = numpy.where(region == BLACK, 0, 1).tolist()` 黑平面
- `buf_b = numpy.where(region == RED, 1, 0).tolist()` 红平面
- `numpy.packbits` / `unpackbits` 在字节和位之间转换

### Stage 3: 重组 RGB
- 136x249 分辨率（电子墨水屏常见）
- 三色编码：白(00) / 黑(01) / 红(10)
- `Image.fromarray(image_array, 'RGB')` 显示

## 参考链接
- https://mwlik.github.io/2024-08-05-crewctf-2024-sniff-challenge/
- https://xz.aliyun.com/t/15357

## 经验提炼
- Saleae Logic 2 导出 raw binary 后用 numpy 解析
- 双 bit 平面 (黑/红) 是硬件 LCD 显示常见方案
- `numpy.packbits` 把 8 位布尔数组压缩为字节
- `numpy.unpackbits` 反向解压
- 136x249 是电子墨水屏常见分辨率
- SPI 抓包要同时抓 CLK + MOSI + CS 解析协议
- 颜色映射 `{0:白, 1:黑, 2:红}` 是三色 e-ink 屏标准
