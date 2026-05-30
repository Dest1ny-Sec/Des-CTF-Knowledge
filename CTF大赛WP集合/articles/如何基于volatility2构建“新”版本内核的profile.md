# 如何基于volatility2构建“新”版本内核的profile

> 原文: https://www.ctfiot.com/70385.html
> ID: 70385

推荐阅读：

2022蓝帽杯遇见的 SUID 提权 总结篇

CobaltStrike beacon二开指南

Edge浏览器-通过XSS获取高权限从而RCE

The End of AFR?

java免杀合集

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
strings 1.mem | grep -i 'Linux version' | uniq

Linux version 5.4.0-84-generic (buildd@lcy01-amd64-007) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #94~18.04.1-Ubuntu SMP Thu Aug 26 23:17:46 UTC 2021 (Ubuntu 5.4.0-84.94~18.04.1-generic 5.4.133)
python2 vol.py -f 1.mem banners.Banners
sudo apt-get install linux-headers-$(uname -r)
sudo apt install build-essential dwarfdump

cd volatility/tools/linux

make

sudo zip Ubuntu1804.zip volatility/tools/linux/module.dwarf /boot/System.map-x.x.x-xx-lowlatency

mv Ubuntu1804.zip volatility/volatility/plugins/linux/
vol2 -f 1.mem --profile=LinuxUbuntu1804-5_4_0-84x64 linux_enumerate_files | grep "/etc/shadow"
vol2 -f 1.mem --profile=LinuxUbuntu1804-5_4_0-84x64 linux_find_file -i 0xffff97ce7444b448

-O shadow.txt
strings 1.mem | grep -i "flag3"
linux_apihooks - 检查用户名apihooks

linux_arp - 打印ARP表

linux_aslr_shift - 自动检测Linux aslr改变

linux_banner - 打印Linux Banner信息

linux_bash - 从bash进程内存中恢复bash历史记录

linux_bash_env - 恢复一个进程的动态环境变量

linux_bash_hash - 从bash进程内存中恢复bash哈希表

linux_check_afinfo - 验证网络协议的操作函数指针

linux_check_creds - 检查是否有任何进程正在共享凭证结构

linux_check_evt_arm - 检查异常向量表以查找系统调用表钩子

linux_check_fop - 检查rootkit修改的文件操作结构

linux_check_idt - 检查IDT是否被更改

linux_check_inline_kernel - 检查内联内核挂钩

linux_check_modules - 将模块列表与sysfs信息进行比较

linux_check_syscall - 检查系统调用表是否已被更改

linux_check_tty - 检查tty的钩子

linux_cpuinfo - 打印有关每个活动处理器的信息

linux_dentry_cache - 从dentry缓存收集文件

linux_dmesg - 收集dmesg buffer

linux_dump_map - 将选定的内存映射写入到磁盘

linux_dynamic_env - 恢复进程的动态环境变量

linux_elfs - 在进程映射中找ELF二进制文件

linux_enumerate_files - 列出文件系统缓存引用的文件

linux_find_file - 列出并从内存中恢复文件

linux_getcwd - 列出每个进程的当前工作目录

linux_hidden_modules - Carves内存寻找隐藏的内核模块

linux_ifconfig - 收集活动接口

linux_info_regs - GDB中的“info寄存器”。它打印出所有的输出

linux_iomem - 提供与/proc/iomem相似的输出

linux_kernel_opened_files - 列出从内核中打开的文件

linux_keyboard_notifiers - 解析键盘通知调用链

linux_ldrmodules - 将proc映射的输出与libdl中的库列表进行比较

linux_library_list - 将库加载到一个进程中

linux_librarydump - 将进程内存中的共享库转储到磁盘

linux_list_raw - 列出应用程序与混杂的套接字

linux_lsmod - 收集加载内核模块

linux_lsof - 列出文件描述符及其路径

linux_malfind - 查找可疑的过程映射

linux_memmap - 转储用于linux任务的内存映射

linux_moddump - 提取加载内核模块

linux_mount - 收集挂载的fs/devices

linux_mount_cache - 收集从kmem_cache安装的fs/设备。

linux_netfilter - 列出Netfilter钩子

linux_netscan - 刻画网络连接结构

linux_netstat - 列表打开的套接字

linux_pidhashtable - 通过PID哈希表枚举进程

linux_pkt_queues - 将每个进程的数据包队列写入磁盘

linux_plthook - 扫描ELF二进制文件' PLT hooks

linux_proc_maps - 收集进程内存映射

linux_proc_maps_rb - 通过映射红黑树收集linux的进程映射

linux_procdump - 将进程的可执行映像转储到磁盘

linux_process_hollow - 检查是否有进程被挖空的迹象

linux_psaux - 收集进程和完整的命令行和开始时间

linux_psenv - 收集进程及其静态环境变量

linux_pslist - 收集活动任务通过task_struct->task list

linux_pslist_cache - 从kmem_cache中收集计划任务

linux_psscan - 扫描进程的物理内存

linux_pstree - 显示进程之间的父/子关系

linux_psxview - 查找隐藏进程与各种各样的进程列表

linux_recover_filesystem - 从内存中恢复整个缓存的文件系统

linux_route_cache - 从内存中恢复路由缓存

linux_sk_buff_cache - 从sk_buff kmem_cache中恢复数据包

linux_slabinfo - 在一台正在运行的机器上模拟/proc/slabinfo。

linux_strings - 将物理偏移量匹配到虚拟地址(可能需要一段时间，非常详细)

linux_threads - 打印进程的线程

linux_tmpfs - 从内存中恢复tmpfs文件系统。

linux_truecrypt_passphrase - 恢复缓存Truecrypt口令

linux_vma_cache - 从vm_area_struct 缓存中收集VMAs

linux_volshell - 内存映像中的shell

linux_yarascan - Linux内存映像中的一个shell
vol -f 1.mem --profile=LinuxUbuntu1804-5_4_0-84x64 linux_enumerate_files
vol -f 1.mem --profile=LinuxUbuntu1804-5_4_0-84x64 linux_find_file -i 0xf5a4e568 -O file.txt
vol -f 1.mem --profile=LinuxUbuntu1804-5_4_0-84x64 linux_bash
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1667540601.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667540601.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1667540602.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667540602.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1667540602.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1667540603.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667540603.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/3-1667540604.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1667540605.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1667540605.png)