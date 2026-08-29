---
title: 【Volatility3】护网杯 Easy_dump
contest: 护网杯
year: 2024
difficulty: medium
vuln_type: forensic_memory
tags: [Volatility3, vigenere-cipher, file-recovery, memmap, strings-unicode, hint-plot, matplotlib]
attack_chain: vol.py info.Info + windows.pslist + windows.memmap --pid 2616 --dump + strings -e l pid.2616.dmp | grep flag + windows.filescan + windows.dumpfiles --physaddr 0x2408c460 恢复加密信息/维吉尼亚密码解密 (key=aeolus)/matplotlib 绘制 hint.txt 散点图
key_payload: vol.py windows.memmap --pid 2616 --dump  维吉尼亚密钥 aeolus  physaddr=0x2408c460
one_liner: 护网杯 Easy_dump，Volatility3 内存取证 + 维吉尼亚密码解密 + hint 散点图绘制。
lesson: Volatility3 命令格式 windows.<plugin> 与 v2 差异大；memmap --pid --dump 提取进程内存；strings -e l 处理 UTF-16 LE 字符串；维吉尼亚密码 key=aeolus 即可解。
quality: high
---

# 【Volatility3】护网杯 Easy_dump

## 概览
护网杯 Easy_dump 内存取证题，Volatility3 工具链 + 维吉尼亚密码 + hint 散点图。

## Volatility3 命令
```bash
# 镜像信息
python vol.py -f easy_dump.img info.Info

# 进程列表
python vol.py -f easy_dump.img windows.pslist

# 进程内存 dump
python vol.py -o ./outputdir/ -f easy_dump.img windows.memmap --pid 2616 --dump

# 进程内字符串搜索
strings -e l pid.2616.dmp | grep "flag"

# 文件扫描
python vol.py -f easy_dump.img windows.filescan

# 物理地址提取文件
python vol.py -o .outputdir -f easy_dump.img windows.dumpfiles --physaddr 0x2408c460
```

## 关键步骤

### 1. 进程内存 dump
- PID 2616 是关键进程
- `windows.memmap --pid 2616 --dump` 输出 pid.2616.dmp

### 2. 字符串搜索
- `strings -e l` 处理 UTF-16 LE（Windows 默认编码）
- 找 "flag" 关键字

### 3. 文件恢复
- 物理地址 0x2408c460 是被删除的 hint.txt
- `windows.dumpfiles --physaddr` 恢复

### 4. 维吉尼亚密码
- 加密信息 key = `aeolus`
- 在线工具或 Python 实现解密

### 5. hint 散点图
```python
import matplotlib.pyplot as plt
import numpy as np

x = []
y = []
with open('hint.txt', 'r') as f:
    datas = f.readlines()
    for data in datas:
        arr = data.split(' ')
        x.append(int(arr[0]))
        y.append(int(arr[1]))

plt.plot(x, y, 'ks', ms=1)
plt.show()
```

## 经验提炼
- Volatility3 命令格式 `windows.<plugin>` 与 v2 差异大
- `memmap --pid --dump` 提取进程内存
- `strings -e l` 处理 UTF-16 LE 字符串
- 维吉尼亚密码 key=aeolus 即可解
- 被删除文件通过 filescan + dumpfiles 恢复（physaddr 锚点）
- matplotlib `plt.plot(x, y, 'ks', ms=1)` 散点图绘制是 CTF 经典
- info.Info 提供 KDBG 等基础信息
