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
