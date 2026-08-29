---
title: 记一次某部内存取证比赛writeup
contest: 某部内存取证比赛
year: 2023
difficulty: medium
vuln_type: forensic_memory
tags: [volatility, winxp, imageinfo, pstree, pslist, memdump, dlllist, malfind, hivelist, hashdump, TrueCrypt, matplotlib, hint-plot]
attack_chain:
- volatility2 imageinfo确认winxp.raw为WinXPSP3x86
- pstree/pslist查运行进程
- memdump/procdump/dlldump导出PID=324进程及所有DLL
- getsids/dlllist/threads/malfind深挖进程痕迹
- hivelist查注册表蜂巢位置
- hivedump导出SAM,hashdump -y system -s SAM取账号Hash
- printkey查SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon最后登录用户
- 拿到key=Th1s_1s_K3y00000+iv=1234567890123456
- AES/CBC解密jfXvUoypb8p3zvmPks8kJ5Kt0vmEw0xUZyRGOicraY4=得flag
- hint.txt数据用matplotlib作图显示图像(可能是字符画或图片)
key_payload: key=Th1s_1s_K3y00000 iv=1234567890123456
one_liner: 某部内存取证比赛WP,volatility2全套命令实战:WinXPSP3x86镜像+进程树+进程dump+注册表蜂巢+SAM hashdump+Winlogon最后登录用户+AES解密+matplotlib数据绘图。
lesson: volatility2是Windows内存取证必备工具,常用命令组合:imageinfo→pstree→pslist→memdump→hivelist→hashdump→printkey,matplotlib散点图作图是hint可视化的简单方法。
quality: medium
---

## 题目列表

内存取证综合:WinXPSP3x86镜像+多检材分析

## 关键考点

### volatility2常用命令

```bash
# 基础信息
volatility -f winxp.raw imageinfo

# 进程分析
volatility -f winxp.raw --profile=WinXPSP3x86 pstree
volatility -f winxp.raw --profile=WinXPSP3x86 pslist

# 进程导出
volatility -f winxp.raw --profile=WinXPSP3x86 memdump -p 324 --dump-dir=/home/lyshark
volatility -f winxp.raw --profile=WinXPSP3x86 procdump -p 324 --dump-dir=/home/lyshark
volatility -f winxp.raw --profile=WinXPSP3x86 dlldump -p 324 --dump-dir=/home/lyshark

# 进程详细信息
volatility -f winxp.raw --profile=WinXPSP3x86 getsids -p 324
volatility -f winxp.raw --profile=WinXPSP3x86 dlllist -p 324
volatility -f winxp.raw --profile=WinXPSP3x86 threads -p 324
volatility -f winxp.raw --profile=WinXPSP3x86 drivermodule
volatility -f winxp.raw --profile=WinXPSP3x86 malfind -p 324 -D /home/lyshark

# 浏览器/任务/历史
volatility -f winxp.raw --profile=WinXPSP3x86 iehistory
volatility -f winxp.raw --profile=WinXPSP3x86 joblinks
volatility -f winxp.raw --profile=WinXPSP3x86 cmdscan
volatility -f winxp.raw --profile=WinXPSP3x86 consoles
volatility -f winxp.raw --profile=WinXPSP3x86 cmdline
volatility -f winxp.raw --profile=WinXPSP3x86 filescan

# 网络
volatility -f winxp.raw --profile=WinXPSP3x86 connscan
volatility -f winxp.raw --profile=WinXPSP3x86 connections
volatility -f winxp.raw --profile=WinXPSP3x86 netscan
volatility -f winxp.raw --profile=WinXPSP3x86 sockscan

# 时间线
volatility -f winxp.raw --profile=WinXPSP3x86 timeliner

# 注册表
volatility -f winxp.raw --profile=WinXPSP3x86 hivelist
volatility -f winxp.raw --profile=WinXPSP3x86 hivedump -o 0xe144f758
volatility -f winxp.raw --profile=WinXPSP3x86 printkey -K "SAM\Domains\Account\Users\Names"
volatility -f winxp.raw --profile=WinXPSP3x86 hashdump -y system地址 -s SAM地址
volatility -f winxp.raw --profile=WinXPSP3x86 printkey -K "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
```

### 关键数据
- 镜像:winxp.raw
- 进程:PID=324
- 注册表:SAM/SYSTEM/SECURITY
- Winlogon最后登录用户(从注册表)
- key: `Th1s_1s_K3y00000`
- iv: `1234567890123456`
- 密文: `jfXvUoypb8p3zvmPks8kJ5Kt0vmEw0xUZyRGOicraY4=` (base64)

### AES解密
- key=16字节 Th1s_1s_K3y00000
- iv=16字节 1234567890123456
- 密文base64
- 模式:CBC(默认)
- 解密得flag

### matplotlib散点图
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

## 实战价值
- volatility2是Windows内存取证必备工具(volatility3已发布)
- 常用检材提取路径:进程→DLL→注册表→SAM→最后登录用户
- matplotlib散点图作图是hint可视化的简单方法(可显示二维码/字符画)
- AES/CBC在CTF和取证中是常见加密模式
