---
title: 记一次某部内存取证比赛writeup
contest: 某部内存取证比赛
year: 2023
difficulty: medium
vuln_type: forensic_memory
tags:
- volatility
- winxp
- imageinfo
- pstree
- pslist
- memdump
- dlllist
- malfind
- hivelist
- hashdump
- TrueCrypt
- matplotlib
- hint-plot
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
full_path: 记一次某部内存取证比赛writeup.full.md
meta_path: 记一次某部内存取证比赛writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 记一次某部内存取证比赛writeup。某部内存取证比赛WP,volatility2全套命令实战:WinXPSP3x86镜像+进程树+进程dump+注册表蜂巢+SAM hashdump+Winlogon最后登录用户+AES解密+matplotlib数据绘图。。关键路径：volatility2 imageinfo确认winxp.raw为WinXPSP3x86 → pstree/pslist查运行...
category: forensic
subcategory: memory_forensics
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/131729.html
reasoning_chain:
- winxp.raw 内存镜像 → 触发点：volatility2 imageinfo 确认 Profile=WinXPSP3x86
- 动作：pstree/pslist 查运行进程 → 观察：PID=324 进程可疑 (TrueCrypt痕迹)
- 动作：memdump -p 324 + procdump + dlldump 导出进程及其所有 DLL
- getsids/dlllist/threads/malfind 深挖 → 观察：TrueCrypt 加载
- 动作：hivelist 查注册表蜂巢地址 → hivedump 导出 SAM
- hashdump -y system_addr -s SAM_addr 取账号 NTLM Hash → 观察：用户口令 hash
- printkey -K 'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon' → 观察：最后登录用户
- 关键：在密码处理脚本等位置发现 key=Th1s_1s_K3y00000 iv=1234567890123456
- 动作：AES-CBC 解密 jfXvUoypb8p3zvmPks8kJ5Kt0vmEw0xUZyRGOicraY4= → flag
- hint.txt 是坐标数据 → 动作：matplotlib.pyplot(x,y,'ks',ms=1) 散点图 → 提示字符
failed_attempts:
- 试图直接 strings 内存镜像找 flag → 失败：flag 被加密藏在内存密文
- 仅靠 pslist 跳过 malfind → 失败：注入代码在未授权页面，malfind 才能识别
- 不解密直接 dump TrueCrypt 卷 → 失败：缺 key/iv
key_observations:
- volatility2 标准命令链：imageinfo→pstree→pslist→memdump→hivelist→hashdump→printkey 是 Windows 内存取证 SOP
- printkey Winlogon 最后登录用户是从注册表痕迹取证的金钥匙
- matplotlib 散点图作图(ms=1)是 hint.txt 坐标型数据可视化的最简方法
- AES/CBC/PKCS7 解密要 key+iv 都到位，缺一不可
prerequisites:
- volatility2 命令行使用（imageinfo/pstree/hashdump/printkey 等）
- Windows 注册表蜂巢（SAM/SYSTEM/SOFTWARE）结构
- AES-CBC 解密与 PKCS7 padding
- Python matplotlib 基础绘图
---
# 记一次某部内存取证比赛writeup

> 原文: https://www.ctfiot.com/131729.html
> ID: 131729


```
https://github.com/volatilityfoundation/volatility3/releases/tag/v2.0.1
python3 setup.py build
python3 setup.py install
pip3 install -r requirements.txt
volatility -f winxp.raw imageinfo                     # 查询镜像基本信息
volatility -f winxp.raw --profile=WinXPSP3x86 pstree   # 查运行进程进程树
volatility -f winxp.raw --profile=WinXPSP3x86 pslist   # 查正在运行的进程
volatility -f winxp.raw --profile=WinXPSP3x86 memdump -p 324 --dump-dir=/home/lyshark   # 将PID=324的进程dump出来
volatility -f winxp.raw --profile=WinXPSP3x86 procdump -p 324 --dump-dir=/home/lyshark   # 将PID=324进程导出为exe
volatility -f winxp.raw --profile=WinXPSP3x86 dlldump -p 324 --dump-dir=/home/lyshark   # 将PID=324进程的所有DLL导出volatility -f winxp.raw --profile=WinXPSP3x86 getsids -p 324 # 查询指定进程的SID
volatility -f winxp.raw --profile=WinXPSP3x86 dlllist -p 324 # 查询指定进程加载过的DLL
volatility -f winxp.raw --profile=WinXPSP3x86 threads -p 324 # 列出当前进程中活跃的线程
volatility -f winxp.raw --profile=WinXPSP3x86 drivermodule   # 列出目标中驱动加载情况
volatility -f winxp.raw --profile=WinXPSP3x86 malfind -p 324 -D /home/lyshark   # 检索内存读写执行页volatility -f winxp.raw --profile=WinXPSP3x86 iehistory # 检索IE浏览器历史记录
volatility -f winxp.raw --profile=WinXPSP3x86 joblinks # 检索计划任务
volatility -f winxp.raw --profile=WinXPSP3x86 cmdscan   # 只能检索命令行历史
volatility -f winxp.raw --profile=WinXPSP3x86 consoles # 抓取控制台下执行的命令以及回显数据
volatility -f winxp.raw --profile=WinXPSP3x86 cmdline   # 列出所有命令行下运行的程序
volatility -f winxp.raw --profile=WinXPSP3x86 filescan # 列出文件volatility -f winxp.raw --profile=WinXPSP3x86 connscan   # 检索已经建立的网络链接
volatility -f winxp.raw --profile=WinXPSP3x86 connections # 检索已经建立的网络链接
volatility -f winxp.raw --profile=WinXPSP3x86 netscan     # 检索所有网络连接情况
volatility -f winxp.raw --profile=WinXPSP3x86 sockscan   # TrueCrypt摘要TrueCrypt摘要volatility -f winxp.raw --profile=WinXPSP3x86 timeliner # 尽可能多的发现目标主机痕迹volatility -f winxp.raw --profile=WinXPSP3x86 hivelist                                       # 检索所有注册表蜂巢
volatility -f winxp.raw --profile=WinXPSP3x86 hivedump -o 0xe144f758                         # 检索SAM注册表键值对
volatility -f winxp.raw --profile=WinXPSP3x86 printkey -K "SAM\Domains\Account\Users\Names" # 检索注册表中账号密码
volatility -f winxp.raw --profile=WinXPSP3x86 hashdump -y system地址 -s SAM地址               # dump目标账号Hash值
volatility -f winxp.raw --profile=WinXPSP3x86 printkey -K "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" # 查最后登录的用户
key: Th1s_1s_K3y00000
iv: 1234567890123456
jfXvUoypb8p3zvmPks8kJ5Kt0vmEw0xUZyRGOicraY4=
import matplotlib.pyplot as plt
import numpy as np

x = []
y = []
with open('hint.txt','r') as f:
   datas = f.readlines()
   for data in datas:
       arr = data.split(' ')
       x.append(int(arr[0]))
       y.append(int(arr[1]))
    
plt.plot(x,y,'ks',ms=1)
plt.show()
```
