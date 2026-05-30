# vol2取证-入门向

> 原文: https://www.ctfiot.com/190333.html
> ID: 190333

后缀
描述

.vmx
虚拟机的配置文件

.vmdk
虚拟机磁盘文件的元数据文件

flat.vmdk
虚拟机的二进制磁盘文件，是虚拟机真正磁盘数据文件

ctk.vmdk
虚拟机磁盘文件的数据块变化追踪文件，保存自从上次快照以来的所发生变化的数据块偏移量信息

.vmem
虚拟机的内存页面文件，存放虚拟机运行时的内存数据，在虚拟机运行或者崩溃时被创建

.vmss
虚拟机挂起时的状态信息文件

.vmsd
虚拟机快照的元数据文件，保存了如快照名、UID(Unique Identifier)、磁盘文件名等信息。在创建快照前，其 size 为 0byte

.vmsn
虚拟机快照的状态信息文件，用于保存创建快照时虚拟机的状态。这个文件的大小取决于创建快照时是否选择保存内存的状态。如果保存的话，那么这个文件会比分配给这个虚拟机的内存大小还要大几兆

.vmtx
虚拟机模板文件

.nvram
虚拟机 bios 文件

.vswp
虚拟机交换文件

.log
虚拟机日志文件

插件名称
功能

amcache
查看AmCache应用程序痕迹信息

apihooks
检测内核及进程的内存空间中的API hook

atoms
列出会话及窗口站atom表

atomscan
Atom表的池扫描(Pool scanner)

auditpol
列出注册表HKLMSECURITYPolicyPolAdtEv的审计策略信息

bigpools
使用BigPagePoolScanner转储大分页池(big page pools)

bioskbd
从实时模式内存中读取键盘缓冲数据(早期电脑可以读取出BIOS开机密码)

cachedump
获取内存中缓存的域帐号的密码哈希

callbacks
打印全系统通知例程

clipboard
提取Windows剪贴板中的内容

cmdline
显示进程命令行参数

cmdscan
提取执行的命令行历史记录（扫描_COMMAND_HISTORY信息）

connections
打印系统打开的网络连接(仅支持Windows XP 和2003)

connscan
打印TCP连接信息

consoles
提取执行的命令行历史记录（扫描_CONSOLE_INFORMATION信息）

crashinfo
提取崩溃转储信息

deskscan
tagDESKTOP池扫描(Poolscaner)

devicetree
显示设备树信息

dlldump
从进程地址空间转储动态链接库

dlllist
打印每个进程加载的动态链接库列表

driverirp
IRP hook驱动检测

drivermodule
关联驱动对象至内核模块

driverscan
驱动对象池扫描

dumpcerts
提取RAS私钥及SSL公钥

dumpfiles
提取内存中映射或缓存的文件

dumpregistry
转储内存中注册表信息至磁盘

editbox
查看Edit编辑控件信息 (Listbox正在实验中)

envars
显示进程的环境变量

eventhooks
打印Windows事件hook详细信息

evtlogs
提取Windows事件日志（仅支持XP/2003)

filescan
提取文件对象（file objects）池信息

gahti
转储用户句柄（handle）类型信息

gditimers
打印已安装的GDI计时器(timers)及回调(callbacks)

gdt
显示全局描述符表(Global Deor Table)

getservicesids
获取注册表中的服务名称并返回SID信息

getsids
打印每个进程的SID信息

handles
打印每个进程打开的句柄的列表

hashdump
转储内存中的Windows帐户密码哈希(LM/NTLM)

hibinfo
转储休眠文件信息

hivedump
打印注册表配置单元信息

hivelist
打印注册表配置单元列表

hivescan
注册表配置单元池扫描

hpakextract
从HPAK文件（Fast Dump格式）提取物理内存数据

hpakinfo
查看HPAK文件属性及相关信息

idt
显示中断描述符表(Interrupt Deor Table)

iehistory
重建IE缓存及访问历史记录

imagecopy
将物理地址空间导出原生DD镜像文件

imageinfo
查看/识别镜像信息

impscan
扫描对导入函数的调用

joblinks
打印进程任务链接信息

kdbgscan
搜索和转储潜在KDBG值

kpcrscan
搜索和转储潜在KPCR值

ldrmodules
检测未链接的动态链接DLL

lsadump
从注册表中提取LSA密钥信息（已解密）

machoinfo
转储Mach-O 文件格式信息

malfind
查找隐藏的和插入的代码

mbrparser
扫描并解析潜在的主引导记录(MBR)

memdump
转储进程的可寻址内存

memmap
打印内存映射

messagehooks
桌面和窗口消息钩子的线程列表

mftparser
扫描并解析潜在的MFT条目

moddump
转储内核驱动程序到可执行文件的示例

modscan
内核模块池扫描

modules
打印加载模块的列表

multiscan
批量扫描各种对象

mutantscan
对互斥对象池扫描

netscan
查看ip地址，连接过的网络

notepad
查看记事本当前显示的文本

objtypescan
扫描窗口对象类型对象

patcher
基于页面扫描的补丁程序内存

poolpeek
可配置的池扫描器插件

printkey
打印注册表项及其子项和值

privs
显示进程权限

procdump
进程转储到一个可执行文件示例

pslist
按照EPROCESS列表打印所有正在运行的进程

psscan
进程对象池扫描

pstree
以树型方式打印进程列表

psxview
查找带有隐藏进程的所有进程列表

qemuinfo
转储Qemu 信息

raw2dmp
将物理内存原生数据转换为windbg崩溃转储格式

screenshot
基于GDI Windows的虚拟屏幕截图保存

servicediff
Windows服务列表(ala Plugx)

sessions
_MM_SESSION_SPACE的详细信息列表(用户登录会话)

shellbags
打印Shellbags信息

shimcache
解析应用程序兼容性Shim缓存注册表项

shutdowntime
从内存中的注册表信息获取机器关机时间

sockets
打印已打开套接字列表

sockscan
TCP套接字对象池扫描

ssdt
显示SSDT条目

strings
物理到虚拟地址的偏移匹配(需要一些时间，带详细信息)

svcscan
Windows服务列表扫描

symlinkscan
符号链接对象池扫描

thrdscan
线程对象池扫描

threads
调查_ETHREAD 和_KTHREADs

timeliner
创建内存中的各种痕迹信息的时间线

timers
打印内核计时器及关联模块的DPC

truecryptmaster
恢复TrueCrypt 7.1a主密钥

truecryptpassphrase
查找并提取TrueCrypt密码

truecryptsummary
TrueCrypt摘要信息

unloadedmodules
打印卸载的模块信息列表

userassist
打印注册表中UserAssist相关信息

userhandles
转储用户句柄表

vaddump
转储VAD数据为文件

vadinfo
转储VAD信息

vadtree
以树形方式显示VAD树信息

vadwalk
显示遍历VAD树

vboxinfo
转储Virtualbox信息（虚拟机）

verinfo
打印PE镜像中的版本信息

vmwareinfo
转储VMware VMSS/VMSN 信息

volshell
内存镜像中的shell

windows
打印桌面窗口(详细信息)

wintree
Z顺序打印桌面窗口树

wndscan
池扫描窗口站

yarascan
以Yara签名扫描进程或内核内存

往期精选

DASCTF X HDCTF 2024｜生而无畏战

2024-05-22

安恒书院首场！2024年嘉兴市职业技能竞赛—网络安全技能竞赛顺利举办

2024-05-24

安恒培训｜六月认证培训开课了！热门课程火热报名中～

2024-05-23


```
f1=open('secret.jpg','rb')
f2=open('1.zip','wb')
f2.write(f1.read()[::-1])
f1.close()
f2.close()
vol.py --plugins=/root/桌面/volatility/volatility/plugins/ -f /root/桌面/WIN-DOOJTVIN21M-20231005-091206.raw --profile=Win7SP1x64 mimikatz
*** Failed to import volatility.plugins.mimikatz (AttributeError: 'module' object has no attribute 'ULInt32')
sudo pip uninstall construct
sudo pip install construct==2.5.5-reupload
filescan | grep -E "jpg|png|bmp|gif|zip|rar|7z|pdf|txt|rtf|doc|ccx|kdbx|vera|py|dmp"
filescan | grep "Desktop"
filescan | grep -iE "flag|ctf"
filescan | grep -iE "flag|.zip$|.rar$|.7z$|.txt$|.png$|.jpg$|.gif$|.pdf$|.doc$|.docx$|.pcapng$|.raw$|.kdbx$"
volatility -f example.raw --profile=版本号 hivelist
volatility -f example.raw --profile=Win7SP1x64 printkey -o 0xfffff8a000024010 -K "ControlSet001ControlComputerNameComputerName"
volatility -f example.raw --profile=Win7SP1x64 printkey -o 0xfffff8a000024010 -K "ControlSet001ServicesTcpipParameters"
volatility -f example.raw --profile=版本号 printkey -K "SAMDomainsAccountUsersNames"
volatility -f example.raw --profile=版本号 dumpfiles -Q 偏移量 --dump-dir=保存路径
volatility -f example.raw --profile=版本号 memdump -p PID --dump-dir=保存路径
volatility -f example.raw --profile=版本号 netscan
volatility -f example.raw --profile=版本号 screenshot --dump-dir=保存路径
volatility -f example.raw --profile=版本号 cmdscan
volatility -f example.raw --profile=版本号 cmdline
volatility -f example.raw --profile=版本号 mimikatz
volatility -f example.raw --profile=版本号 lsadump
volatility -f 1.raw  --profile=版本号 printkey -K "SOFTWAREMicrosoftWindows NTCurrentVersionWinlogon"
volatility -f 1.raw  --profile=版本号 evtlogs --dump-dir logs/
volatility -f windows.vmem --profile=版本号 dumpregistry -o 偏移量 -D 保存路径
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/5-1719578172.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/6-1719578172.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/0-1719578173.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/0-1719578174.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/2-1719578174.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/4-1719578175.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/2-1719578175.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/9-1719578176.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/3-1719578177.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/6-1719578177.png)