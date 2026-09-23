# 内存取证命令速查

> 来源: 内存取证秒杀所有命令.pdf
> 更新日期: 2026-05-21 (从PDF提取整理)

---

## Volatility 2 Windows 插件速查表

### 进程相关

| 插件 | 功能 |
|------|------|
| `pslist` | 按照EPROCESS列表打印所有正在运行的进程 |
| `psscan` | 进程对象池扫描 |
| `pstree` | 以树型方式打印进程列表 |
| `psxview` | 查找带有隐藏进程的所有进程列表 |
| `procdump` | 进程转储到一个可执行文件示例 |
| `memdump` | 转储进程的可寻址内存 |
| `cmdline` | 显示进程命令行参数 |
| `cmdscan` | 提取执行的命令行历史记录（扫描_COMMAND_HISTORY信息） |
| `consoles` | 提取执行的命令行历史记录（扫描_CONSOLE_INFORMATION信息） |
| `privs` | 显示进程权限 |
| `envars` | 显示进程的环境变量 |
| `getsids` | 打印每个进程的SID信息 |
| `handles` | 打印每个进程打开的句柄的列表 |
| `dlllist` | 打印每个进程加载的动态链接库列表 |
| `dlldump` | 从进程地址空间转储动态链接库 |
| `ldrmodules` | 检测未链接的动态链接DLL |

### 内存/镜像信息

| 插件 | 功能 |
|------|------|
| `imageinfo` | 查看/识别镜像信息（**第一步必做**） |
| `imagecopy` | 将物理地址空间导出原生DD镜像文件 |
| `kdbgscan` | 搜索和转储潜在KDBG值 |
| `kpcrscan` | 搜索和转储潜在KPCR值 |
| `raw2dmp` | 将物理内存原生数据转换为WinDbg崩溃转储格式 |
| `screenshot` | 基于GDI Windows的虚拟屏幕截图保存 |

### 文件/注册表

| 插件 | 功能 |
|------|------|
| `filescan` | 提取文件对象池信息 |
| `dumpfiles` | 提取内存中映射或缓存的文件 |
| `hivelist` | 打印注册表配置单元列表 |
| `hivescan` | 注册表配置单元池扫描 |
| `hivedump` | 打印注册表配置单元信息 |
| `dumpregistry` | 转储内存中注册表信息至磁盘 |
| `printkey` | 打印注册表项及其子项和值 |
| `mftparser` | 扫描并解析潜在的MFT条目 |

### 网络

| 插件 | 功能 |
|------|------|
| `connections` | 打印系统打开的网络连接（仅XP/2003） |
| `connscan` | 打印TCP连接信息 |
| `sockets` | 打印已打开套接字列表 |
| `sockscan` | TCP套接字对象池扫描 |
| `netscan` | 网络连接扫描（Win7+） |

### 密码/凭证

| 插件 | 功能 |
|------|------|
| `hashdump` | 转储内存中的Windows账户密码哈希(LM/NTLM) |
| `cachedump` | 获取内存中缓存的域帐号的密码哈希 |
| `lsadump` | 从注册表中提取LSA密钥信息（已解密） |
| `dumpcerts` | 提取RAS私钥及SSL公钥 |

### 恶意代码检测

| 插件 | 功能 |
|------|------|
| `malfind` | 查找隐藏的和插入的代码 |
| `apihooks` | 检测内核及进程的内存空间中的API hook |
| `driverirp` | IRP hook驱动检测 |
| `ssdt` | 显示SSDT条目 |
| `callbacks` | 打印全系统通知例程 |
| `timers` | 打印内核计时器及关联模块的DPC |
| `yarascan` | 以Yara签名扫描进程或内核内存 |

### 驱动/内核

| 插件 | 功能 |
|------|------|
| `modules` | 打印加载模块的列表 |
| `modscan` | 内核模块池扫描 |
| `moddump` | 转储内核驱动程序到可执行文件的示例 |
| `driverscan` | 驱动对象池扫描 |
| `drivermodule` | 关联驱动对象至内核模块 |
| `devicetree` | 显示设备树信息 |
| `unloadedmodules` | 打印卸载的模块信息列表 |

### 用户交互痕迹

| 插件 | 功能 |
|------|------|
| `clipboard` | 提取Windows剪贴板中的内容 |
| `notepad` | 查看记事本当前显示的文本 |
| `iehistory` | 重建IE缓存及访问历史记录 |
| `sessions` | MM_SESSION_SPACE详细信息列表（用户登录会话） |
| `shellbags` | 打印Shellbags信息 |
| `userassist` | 打印注册表中UserAssist相关信息 |

### 其他常用

| 插件 | 功能 |
|------|------|
| `amcache` | 查看AmCache应用程序痕迹信息 |
| `shimcache` | 解析应用程序兼容性Shim缓存注册表项 |
| `shutdowntime` | 从内存中的注册表信息获取机器关机时间 |
| `verinfo` | 打印PE镜像中的版本信息 |
| `timeliner` | 创建内存中的各种痕迹信息的时间线 |
| `strings` | 物理到虚拟地址的偏移匹配 |
| `mbrparser` | 扫描并解析潜在的主引导记录(MBR) |
| `svcscan` | Windows服务列表扫描 |
| `mutantscan` | 互斥对象池扫描 |
| `symlinkscan` | 符号链接对象池扫描 |
| `thrdscan` | 线程对象池扫描 |
| `editbox` | 查看Edit编辑控件信息 |
| `deskscan` | tagDESKTOP池扫描 |
| `clipboard` | 提取Windows剪贴板内容 |
| `auditpol` | 列出审计策略信息 |
| `bioskbd` | 从实时模式内存中读取键盘缓冲数据 |
| `crashinfo` | 提取崩溃转储信息 |
| `evtlogs` | 提取Windows事件日志（仅XP/2003） |
| `gdt` | 显示全局描述符表 |
| `idt` | 显示中断描述符表 |
| `hibinfo` | 转储休眠文件信息 |
| `machoinfo` | 转储Mach-O文件格式信息 |
| `multiscan` | 批量扫描各种对象 |
| `poolpeek` | 可配置的池扫描器插件 |
| `qemuinfo` | 转储Qemu信息 |
| `vboxinfo` | 转储Virtualbox信息 |
| `vmwareinfo` | 转储VMware VMSS/VMSN信息 |
| `volshell` | 内存镜像中的shell |
| `windows` | 打印桌面窗口详细信息 |
| `wintree` | Z顺序打印桌面窗口树 |
| `wndscan` | 池扫描窗口站 |
| `truecryptmaster` | 恢复TrueCrypt 7.1a主密钥 |
| `truecryptpassphrase` | 查找并提取TrueCrypt密码 |

---

## Volatility 2 Windows 常用操作流程

### 第一步：识别镜像

```bash
volatility -f file.raw imageinfo
```

### 第二步：查看进程

```bash
volatility -f file.raw --profile=Win7SP1x86 pslist
volatility -f file.raw --profile=Win7SP1x86 psscan     # 更全面
volatility -f file.raw --profile=Win7SP1x86 pstree     # 树形
```

### 第三步：查找文件

```bash
# 查找图片/压缩包/文档
volatility -f file.raw --profile=Win7SP1x86 filescan | grep -v Temporary | grep -E 'png|jpg|gif|zip|rar|7z|pdf|txt|.snt'

# 导出文件
volatility -f file.raw --profile=Win7SP1x64 dumpfiles -Q 0x000000003ee15c70 --dump-dir=./
```

### 第四步：导出进程内存

```bash
volatility -f file.raw --profile=Win7SP1x86 memdump -p 3380 -D ~/CTF
```

### 第五步：截图/其他

```bash
volatility screenshot -f file.raw --profile=WinXPSP2x86 --dump-dir=./
volatility -f file.raw --profile=Win7SP1x86 hashdump   # dump密码哈希
```

---

## Volatility 2 Linux 常用命令

### 基本信息

```bash
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_pslist        # 查看进程
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_psaux         # 保存进程
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_pstree        # 进程树
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_procdump 2187 --dump-dir=./dump  # 导出进程
```

### 网络信息

```bash
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_netstat       # 网络连接状态
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_netscan       # 网络连接扫描
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_netstat -p <PID>   # 指定进程网络连接
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_netstat | grep -E 'LISTEN|ESTABLISHED'  # 活跃连接
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_arp           # ARP表
```

### Bash/环境

```bash
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_bash          # bash历史记录
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_bash_env      # bash环境变量
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_getcwd        # 进程工作目录
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_dynamic_env   # 动态环境变量
```

### 文件查找/恢复

```bash
# 查找特定文件
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_enumerate_files | grep '文件名'

# 查找Firefox历史记录
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_enumerate_files | grep 'mozilla/firefox'
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_enumerate_files | grep 'places.sqlite'

# 导出文件（-i 为文件inode地址）
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_find_file -i 0xffff9760a8731a98 -O places.sqlite
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_find_file -i 0xffff997931585c00 -O output.7z.part

# 查看openssh
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_lsof      # 打开的文件和网络连接
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_ifconfig   # 网络接口
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_sshkeys    # SSH密钥
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_mount      # 挂载设备
volatility -f out.mem --profile=LinuxUbuntu16x64 linux_dmesg      # 内核消息
```

---

## Volatility 3 常用命令

```bash
# 镜像信息
vol3 -f file.raw windows.info

# 进程列表
vol3 -f file.raw windows.pslist
vol3 -f file.raw windows.psscan
vol3 -f file.raw windows.pstree

# 文件扫描
vol3 -f file.raw windows.filescan

# 命令行
vol3 -f file.raw windows.cmdline

# 网络
vol3 -f file.raw windows.netstat

# 注册表
vol3 -f file.raw windows.registry.hivelist

# 导出文件
vol3 -f file.raw windows.dumpfiles --virtaddr 0x...

# hash dump
vol3 -f file.raw windows.hashdump

# 恶意代码检测
vol3 -f file.raw windows.malfind
```

---

## 相关资源

- [Volatility官方Wiki](https://github.com/volatilityfoundation/volatility/wiki)
- [Volatility3官方文档](https://volatility3.readthedocs.io/)
- 工具使用: 配合 [Wireshark使用.md](Wireshark使用.md) — 流量+内存联合分析
