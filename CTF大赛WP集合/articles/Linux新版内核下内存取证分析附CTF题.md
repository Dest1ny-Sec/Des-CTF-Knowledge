# Linux新版内核下内存取证分析附CTF题

> 原文: https://www.ctfiot.com/60876.html
> ID: 60876

推荐阅读：

The End of AFR?

java免杀合集

ATT&CK中的攻与防——T1059

若依(RuoYi)管理系统后台sql注入漏洞分析

利用 PHP-FPM 做内存马的方法

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
Linux version 5.15.0-43-generic (buildd@lcy02-amd64-076) (gcc (Ubuntu 11.2.0-19ubuntu1) 11.2.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #46-Ubuntu SMP Tue Jul 12 10:30:17 UTC 2022 (Ubuntu 5.15.0-43.46-generic 5.15.39)
```



```
由于Volatility2的方案在Ubuntu22.04尚未人成功实现, 需要从vol源码角度和Linux内核方向进行修改.本文不再介绍该种思路.

但是对于指定的系统生成profile, 提供以下使用docker快速生成策略的解决方案. 可应用在其他场景. 如: 可用于出题对互联网尚未发布的策略文件, 使用“较新”系统进行出题.

具体原理, 参照官方说明:[https://github.com/volatilityfoundation/volatility/wiki/Linux](https://github.com/volatilityfoundation/volatility/wiki/Linux)

```bash
# 建立模拟环境
cd ./volatility2/tools/linux
docker run -it --rm -v $PWD:/volatility ubuntu:20.04 /bin/bash
# 安装必须环境
apt update
apt install -y linux-headers-5.15.0-43-generic linux-image-5.15.0-43-generic dwarfdump build-essential vim zip
cd /volatility/tools/linux
/volatility/tools/linux# sed -i 's/$(shell uname -r)/5.15.0-43-generic/g' Makefile
/volatility/tools/linux# echo 'MODULE_LICENSE("GPL");' >> module.c
/volatility/tools/linux# make
/volatility/tools/linux# cd /
/volatility/tools/linux# zip Linux-5.15.0-43-generic.zip volatility/tools/linux/module.dwarf /boot/System.map-5.15.0-43-generic
/volatility/tools/linux# exit
mv Linux-5.15.0-43-generic.zip ./volatility2/volatility/plugins/overlays/linux

```
```



```
./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-4.4.0-137-generic > output.json
```



```
附: 若出现多次错误等问题,可以删除附加源,重新添加即可.

```jsx
# remove old one
rm -f /etc/apt/sources.list.d/ddebs.list
```
```



```
$ git clone <https://github.com/volatilityfoundation/dwarf2json>
$ cd dwarf2json/
$ go build
wget <https://launchpad.net/ubuntu/+archive/primary/+files/linux-image-unsigned-5.15.0-48-generic-dbgsym_5.15.0-48.54_amd64.ddeb>
# 使用能适用该内核的操作系统 (ubuntu 18.04 / 20.04 / etc)
$ docker run -it --rm -v $PWD:/volatility ubuntu:18.04 /bin/bash
/# cd /volatility/
/volatility# dpkg -i linux-image-unsigned-5.15.0-48-generic-dbgsym_5.15.0-48.54_amd64.ddeb
/volatility# dpkg -i linux-image-unsigned-5.15.0-48-generic-dbgsym_5.15.0-48.54_amd64.ddeb
/volatility# ./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-5.15.0-48-generic > linux-image-5.15.0-48-generic.json 

$ cp linux-image-4.15.0-184-generic.json ./volatility3/volatility3/framework/symbols/linux
```



```
banners.Banners     Attempts to identify potential linux banners in an
    linux.bash.Bash     Recovers bash command history from memory.
    linux.check_afinfo.Check_afinfo
    linux.check_creds.Check_creds
    linux.check_idt.Check_idt
    linux.check_modules.Check_modules
    linux.check_syscall.Check_syscall
    linux.elfs.Elfs     Lists all memory mapped ELF files for all processes.
    linux.keyboard_notifiers.Keyboard_notifiers
    linux.kmsg.Kmsg     Kernel log buffer reader
    linux.lsmod.Lsmod   Lists loaded kernel modules.
    linux.lsof.Lsof     Lists all memory maps for all processes.
    linux.malfind.Malfind
    linux.mountinfo.MountInfo
    linux.proc.Maps     Lists all memory maps for all processes.
    linux.psaux.PsAux   Lists processes with their command line arguments
    linux.pslist.PsList
                        Lists the processes present in a particular linux
    linux.pstree.PsTree
    linux.tty_check.tty_check
```



```
python vol.py -f ~/Documents/ctf/sakei/dump.mem  linux.psaux.PsAux
```



```
import sys

try:
    password = sys.argv[1]
except:
    print("Usage: ./wallet password")
    exit()

words = []
with open("bip39list.txt", "r") as f:
    words = f.read().splitlines()

code = 0x26F4036773F33FD1BC4E55616472CD7F65086B670B2DD5B84BB4D16F02730E734F72E500
code = bin(code)[2:]
code = str(code.zfill((len(code)+(12-len(code)%12))))

mnemonic = []

for i in range(0, len(code), 12):
    mnemonic.append(words[int(code[i:(i+12)],2)-1])

print(" ".join(mnemonic))

# output:
evidence leopard solution layer legend danger orient project silver flower wrong path stove throw fortune report nuclear old target exact broom hawk toss paper
```



```
Linux version 4.19.0-21-amd64 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.249-2 (2022-06-30)
```



```
题目具体细节, 本文不详细叙述, 相关文件都是按照原始数据保存在文件中, 可以直接使用010 editor打开后搜索关键信息
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/9-1665204122.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1665204122.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1665204122.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1665204123.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1665204123.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/9-1665204125.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1665204125.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1665204126.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1665204126.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/4-1665204127.png)