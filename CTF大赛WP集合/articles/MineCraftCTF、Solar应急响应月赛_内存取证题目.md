# MineCraftCTF、Solar应急响应月赛 内存取证题目

> 原文: https://www.ctfiot.com/265387.html
> ID: 265387

MineCraftCTF 内存取证

Geek团队运营着一个大型的Minecraft多人服务器，拥有超过5000名注册玩家。2025年8月11日下午，服务器管理员收到多名玩家举报，称服务器出现异常行为，技术在排查后发现服务器文件被勒索组织投放了勒索病毒，导致文件被加密，技术将服务器内存镜像打包交给专业网络安全团队极安云科进行排查，请你协助公司方进行排查。用户须知：本题涉及到真实环境勒索病毒，请在隔离环境下进行解题操作，严禁将本题所涉文件与外界互联网接触

第六题不会

1. 请提交攻击者IP

这题建议做完第三题后再做，在第三题中暴搜.php，最后面发现了webshell成功的链接

所以去看看能不能搜到访问这个链接的日志，直接搜http://10.10.0.133/index.php没搜到，所以搜了index.php

第一个就找到了日志，往上翻有REMOTE_ADDR 10.10.0.1

POST /uploads/shell.php HTTP/1.1Host: 10.10.0.133User-Agent: Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Referer: http://10.10.0.133/index.php?msg=文件上传成功！文件名: shell.php, 大小: 0.03 KB&type=successContent-Type: application/x-www-form-urlencodedContent-Length: 4901Connection: closeDOCUMENT_ROOT: C:/phpstudy_pro/WWWSERVER_SOFTWARE: nginx/1.15.11REMOTE_ADDR: 10.10.0.1REMOTE_PORT: 59820SERVER_ADDR: 10.10.0.133SERVER_PORT: 80SERVER_NAME: localhostGATEWAY_INTERFACE: CGI/1.1REQUEST_SCHEME: httpREDIRECT_STATUS: 200

10.10.0.1

2. 请提交攻击者外联IP和端口

首先查看镜像的imageinfo，得到profile=Win7SP1x64

F:
forensicsvolatilityvolatility_2.6_win64_standalone>volatility_2.6_win64_standalone.exe -f memdump.mem imageinfoVolatility Foundation Volatility Framework 2.6INFO    : volatility.debug    : Determining profile based on KDBG search...          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)                     AS Layer2 : FileAddressSpace (F:
forensicsvolatilityvolatility_2.6_win64_standalonememdump.mem)                      PAE type : No PAE                           DTB : 0x187000L                          KDBG : 0xf80003fea120L          Number of Processors : 4     Image Type (Service Pack) : 1                KPCR for CPU 0 : 0xfffff80003fec000L                KPCR for CPU 1 : 0xfffff88004500000L                KPCR for CPU 2 : 0xfffff8800457d000L                KPCR for CPU 3 : 0xfffff880009af000L             KUSER_SHARED_DATA : 0xfffff78000000000L           Image date and time : 2025-08-11 09:22:45 UTC+0000     Image local date and time : 2025-08-11 17:22:45 +0800

其次netscan查看网络连接

F:
forensicsvolatilityvolatility_2.6_win64_standalone>volatility_2.6_win64_standalone.exe -f memdump.mem --profile=Win7SP1x64 netscanVolatility Foundation Volatility Framework 2.6Offset(P)          Proto    Local Address                  Foreign Address      State            Pid      Owner          Created0x79d4e0           TCPv4    127.0.0.1:
9000                 127.0.0.1:
65026      CLOSED           -10x6455110          TCPv4    0.0.0.0:
3306                   0.0.0.0:0            LISTENING        2716     mysqld.exe0x6455110          TCPv6    :::
3306                        :::0                 LISTENING        2716     mysqld.exe0xfb45260          UDPv6    fe80::
e8fe:
835b:
aef8:
5951:
59954 *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x10480010         UDPv6    fe80::
e8fe:
835b:
aef8:
5951:
1900 *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x110a85a0         UDPv4    10.10.0.133:
59956              *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x11d34010         UDPv4    127.0.0.1:
1900                 *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x1651e5a0         UDPv4    10.10.0.133:
59956              *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x1945b5b0         UDPv4    0.0.0.0:
52018                  *:*                                   384      svchost.exe    2025-08-11 09:22:12 UTC+00000x2ab04010         UDPv4    0.0.0.0:0                      *:*                                   1172     iexplore.exe   2025-08-11 09:22:28 UTC+00000x2ab04010         UDPv6    :::0                           *:*                                   1172     iexplore.exe   2025-08-11 09:22:28 UTC+00000x2ad41010         UDPv4    0.0.0.0:0                      *:*                                   1172     iexplore.exe   2025-08-11 09:22:28 UTC+00000x2ad41010         UDPv6    :::0                           *:*                                   1172     iexplore.exe   2025-08-11 09:22:28 UTC+00000x2eb43ec0         UDPv4    10.10.0.133:
1900               *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x3d66c900         UDPv4    0.0.0.0:0                      *:*                                   3004     phpstudy_pro.e 2025-08-04 05:41:58 UTC+00000x3d66c900         UDPv6    :::0                           *:*                                   3004     phpstudy_pro.e 2025-08-04 05:41:58 UTC+00000x3d716be0         UDPv4    0.0.0.0:
64039                  *:*                                   384      svchost.exe    2025-08-11 09:22:36 UTC+00000x3d716be0         UDPv6    :::
64039                       *:*                                   384      svchost.exe    2025-08-11 09:22:36 UTC+00000x3da05130         UDPv4    0.0.0.0:0                      *:*                                   1504     svchost.exe    2025-08-04 05:02:04 UTC+00000x3da06680         UDPv4    10.10.0.133:68                 *:*                                   3036     svchost.exe    2025-08-11 09:22:06 UTC+00000x3da07840         UDPv4    0.0.0.0:0                      *:*                                   1504     svchost.exe    2025-08-04 05:02:04 UTC+00000x3da07840         UDPv6    :::0                           *:*                                   1504     svchost.exe    2025-08-04 05:02:04 UTC+00000x3daa3480         UDPv4    0.0.0.0:
63384                  *:*                                   384      svchost.exe    2025-08-11 09:22:03 UTC+00000x3dac0a90         UDPv4    0.0.0.0:0                      *:*                                   384      svchost.exe    2025-08-11 09:19:50 UTC+00000x3dac0a90         UDPv6    :::0                           *:*                                   384      svchost.exe    2025-08-11 09:19:50 UTC+00000x3dc2d560         UDPv4    0.0.0.0:
5355                   *:*                                   384      svchost.exe    2025-08-11 09:22:02 UTC+00000x3da299e0         TCPv4    0.0.0.0:
3306                   0.0.0.0:0            LISTENING        2116     mysqld.exe0x3da299e0         TCPv6    :::
3306                        :::0                 LISTENING        2116     mysqld.exe0x3daee160         TCPv4    0.0.0.0:
3306                   0.0.0.0:0            LISTENING        1904     mysqld.exe0x3daee160         TCPv6    :::
3306                        :::0                 LISTENING        1904     mysqld.exe0x3db168e0         TCPv4    0.0.0.0:
49157                  0.0.0.0:0            LISTENING        444      lsass.exe0x3dc094a0         TCPv4    127.0.0.1:
9000                 0.0.0.0:0            LISTENING        1928     xp.cn_cgi.exe0x3dca37a0         TCPv4    0.0.0.0:
3306                   0.0.0.0:0            LISTENING        1904     mysqld.exe0x3dca37a0         TCPv6    :::
3306                        :::0                 LISTENING        1904     mysqld.exe0x3dcf77f0         TCPv4    0.0.0.0:
49155                  0.0.0.0:0            LISTENING        428      services.exe0x3dcf77f0         TCPv6    :::
49155                       :::0                 LISTENING        428      services.exe0x3dd40380         TCPv4    0.0.0.0:
49155                  0.0.0.0:0            LISTENING        428      services.exe0x3ddf4340         TCPv4    0.0.0.0:
49156                  0.0.0.0:0            LISTENING        1504     svchost.exe0x3ddf9ee0         TCPv4    0.0.0.0:
49156                  0.0.0.0:0            LISTENING        1504     svchost.exe0x3ddf9ee0         TCPv6    :::
49156                       :::0                 LISTENING        1504     svchost.exe0x3de65010         UDPv6    ::1:
1900                       *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x3df82bf0         UDPv4    0.0.0.0:0                      *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3df93a50         UDPv4    0.0.0.0:0                      *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3df93a50         UDPv6    :::0                           *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e0c2af0         UDPv6    fe80::
e8fe:
835b:
aef8:
5951:
546  *:*                                   3036     svchost.exe    2025-08-11 09:22:02 UTC+00000x3e13cc70         UDPv4    0.0.0.0:
500                    *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e140a20         UDPv4    0.0.0.0:
4500                   *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e140a20         UDPv6    :::
4500                        *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e147010         UDPv4    0.0.0.0:
4500                   *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e15c010         UDPv4    0.0.0.0:
500                    *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e15c010         UDPv6    :::
500                         *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3deb95f0         TCPv4    0.0.0.0:
49154                  0.0.0.0:0            LISTENING        900      svchost.exe0x3debd450         TCPv4    0.0.0.0:
49154                  0.0.0.0:0            LISTENING        900      svchost.exe0x3debd450         TCPv6    :::
49154                       :::0                 LISTENING        900      svchost.exe0x3dec9680         TCPv4    127.0.0.1:
9000                 0.0.0.0:0            LISTENING        2700     xp.cn_cgi.exe0x3ded6940         TCPv4    10.10.0.133:
139                0.0.0.0:0            LISTENING        4        System0x3df47bd0         TCPv4    0.0.0.0:
49157                  0.0.0.0:0            LISTENING        444      lsass.exe0x3df47bd0         TCPv6    :::
49157                       :::0                 LISTENING        444      lsass.exe0x3df822e0         TCPv4    0.0.0.0:
445                    0.0.0.0:0            LISTENING        4        System0x3df822e0         TCPv6    :::
445                         :::0                 LISTENING        4        System0x3e162930         TCPv4    0.0.0.0:
135                    0.0.0.0:0            LISTENING        692      svchost.exe0x3e1678e0         TCPv4    0.0.0.0:
135                    0.0.0.0:0            LISTENING        692      svchost.exe0x3e1678e0         TCPv6    :::
135                         :::0                 LISTENING        692      svchost.exe0x3e174d00         TCPv4    0.0.0.0:
49152                  0.0.0.0:0            LISTENING        372      wininit.exe0x3e176630         TCPv4    0.0.0.0:
49152                  0.0.0.0:0            LISTENING        372      wininit.exe0x3e176630         TCPv6    :::
49152                       :::0                 LISTENING        372      wininit.exe0x3e1797b0         TCPv4    0.0.0.0:
49153                  0.0.0.0:0            LISTENING        772      svchost.exe0x3e1a4e60         TCPv4    0.0.0.0:
49153                  0.0.0.0:0            LISTENING        772      svchost.exe0x3e1a4e60         TCPv6    :::
49153                       :::0                 LISTENING        772      svchost.exe0x3e1b54f0         TCPv4    127.0.0.1:
65027                127.0.0.1:
443        CLOSED           -10x3ee184c0         UDPv4    127.0.0.1:
59957                *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x3f0d8310         UDPv4    0.0.0.0:
5355                   *:*                                   384      svchost.exe    2025-08-11 09:22:02 UTC+00000x3f0d8310         UDPv6    :::
5355                        *:*                                   384      svchost.exe    2025-08-11 09:22:02 UTC+00000x3f61bc00         UDPv4    10.10.0.133:
137                *:*                                   4        System         2025-08-11 09:19:50 UTC+00000x3f6a8010         UDPv4    10.10.0.133:
138                *:*                                   4        System         2025-08-11 09:19:50 UTC+00000x3f6ba970         UDPv6    ::1:
59955                      *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x3f7be6e0         UDPv4    0.0.0.0:
56365                  *:*                                   384      svchost.exe    2025-08-11 09:22:06 UTC+00000x3f601180         TCPv4    0.0.0.0:
3306                   0.0.0.0:0            LISTENING        1384     dllhost.exe0x3f601180         TCPv6    :::
3306                        :::0                 LISTENING        1384     dllhost.exe0x3f772010         TCPv4    10.10.0.133:80                 10.10.0.1:
64000      CLOSED           -10x3fcb50e0         UDPv4    0.0.0.0:
58363                  *:*                                   384      svchost.exe    2025-08-11 09:22:00 UTC+00000x3fd14110         UDPv4    0.0.0.0:0                      *:*                                   3004     phpstudy_pro.e 2025-08-04 05:41:58 UTC+00000x3fd14110         UDPv6    :::0                           *:*                                   3004     phpstudy_pro.e 2025-08-04 05:41:58 UTC+00000x3fd59230         UDPv4    0.0.0.0:
5355                   *:*                                   384      svchost.exe    2025-08-11 09:22:02 UTC+00000x3fd59230         UDPv6    :::
5355                        *:*                                   384      svchost.exe    2025-08-11 09:22:02 UTC+00000x3fd7d010         UDPv4    0.0.0.0:
49997                  *:*                                   384      svchost.exe    2025-08-11 09:22:29 UTC+00000x3fc827a0         TCPv4    10.10.0.133:
64999              66.240.205.34:
9002   CLOSE_WAIT       -10x3fd7a7e0         TCPv4    10.10.0.133:80                 10.10.0.1:
59820      CLOSED           -1

外联地址中，只有66.240.205.34:
9002为外网ip

66.240.205.34:
9002

3. 请提交该服务器皮肤上传系统中发现的webshell绝对路径（含文件名）

flag格式：MCCTF{D:/xxx/xxx.php}

使用暴力搜索，已经提示是php文件，直接搜 .php

F:
forensicsvolatilityvolatility_2.6_win64_standalone>strings memdump.mem | findstr /i .php > php_found.txt

C:/phpstudy_pro/WWW/uploads/shell.php

4. 请提交该服务器勒索病毒名称

这题也是暴搜，让AI给出了常见的病毒名

LockBit 3.0

5. 请提提交该勒索组织留下的浏览器地址的顶级域名，如：.com

上题找到了勒索信，就直接看具体内容 如果你不支付赎金，这些数据将在TOR网站上公布

.onion

Solar月赛-VOL_EASY

某企业服务器近日遭受隐秘入侵。安全团队通过日志溯源发现，黑客利用Web应用漏洞植入恶意后门，根据溯源的信息配合警方逮捕了黑客，安全团队已经紧急保存了黑客电脑的内存转储文件，请你开始取证以便固定证据。请根据题目文件，找出下面10条证据让罪犯服软吧！解压密码：0f6941beab90bc8be5bc25b6c56ee849

黑客上传的一句话木马密码是多少？

在DeviceHarddiskVolume2Tools文件夹下发现多个异常内容，dump_lass.bat ezshell.php.txt等，全部导出后，ezshell.php.txt中找到一句话木马

solar

黑客使用的木马连接工具叫什么（比如xx.exe）？(仅首字母大写)

DeviceHarddiskVolume2ToolsAntSword-Loader-v4.0.3-win32-x64AntSword.exe

黑客使用的木马连接工具的位置在哪里（比如C:
xxxxxx.exe） ？

• 如上题，Tools和Windows文件在一个盘里放着，所以是C盘，加上后面内容即可

• 也可以用cmdline查看

C:
ToolsAntSword-Loader-v4.0.3-win32-x64AntSword.exe

黑客获取到的FLAG是什么？

DeviceHarddiskVolume2Toolsflag.txtratorDesktopflag.txt

正常导出文件即可

黑客入侵的网站地址是多少（只需要http://xxxxx/）？

关于问网站地址的题，大多数都看的是iehistory

F:
forensicsvolatilityvolatility_2.6_win64_standalone>volatility_2.6_win64_standalone.exe -f vol_easy.vmem --profile=Win7SP1x64 iehistoryVolatility Foundation Volatility Framework 2.6**************************************************Process: 1656 explorer.exeCache type "DEST" at 0x6bcb23dLast modified: 2025-07-23 17:37:39 UTC+0000Last accessed: 2025-07-23 09:37:40 UTC+0000URL: Administrator@http://192.168.186.140/uploads/6880ad58e4e88.php**************************************************Process: 1656 explorer.exeCache type "DEST" at 0x6bcb9ddLast modified: 2025-07-23 17:37:28 UTC+0000Last accessed: 2025-07-23 09:37:30 UTC+0000URL: Administrator@file:///C:/Tools/ezshell.php**************************************************Process: 1928 iexplore.exeCache type "DEST" at 0x4768235Last modified: 2025-07-23 17:37:29 UTC+0000Last accessed: 2025-07-23 09:37:30 UTC+0000URL: Administrator@http://192.168.186.140/index.php

http://192.168.186.140/

黑客入侵时，使用的系统用户名是什么？

查看用户列表

Administrator:
500:
aad3b435b51404eeaad3b435b51404ee:
3b397b08d3203ddb1aae4a687651a310:::
Guest:
501:
aad3b435b51404eeaad3b435b51404ee:
31d6cfe0d16ae931b73c59d7e0c089c0:::

Administrator

黑客创建隐藏账户的密码是多少？

Tools文件夹下还有一张截屏

DeviceHarddiskVolume2Toolsscreenshot-20250723-171834.png

使用了net user solar$ solar2025 /add这是隐藏账户创建，正常情况下net user查看不到此用户，但使用wmic命令

solar2025

黑客首次操作靶机的关键程序是什么？

如上图所示

C:
phpstudy_prowww> dump_lass.bat[*]正在获取 lsass.exe PID..

lsass.exe

该关键程序的PID是多少？

同上

[*]PID:
456

该关键程序的内存文件保存到了什么地方？

同上

[*]正在尝试导出内存转储.[√]成功导出1sass内存？C:
phpstudy_proWwwlsass.dmp

C:
phpstudy_proWWWlsass.dmp


```
POST /uploads/shell.php HTTP/1.1Host: 10.10.0.133User-Agent: Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflateAccept-Language: zh-CN,zh;q=0.9Referer: http://10.10.0.133/index.php?msg=文件上传成功！文件名: shell.php, 大小: 0.03 KB&type=successContent-Type: application/x-www-form-urlencodedContent-Length: 4901Connection: closeDOCUMENT_ROOT: C:/phpstudy_pro/WWWSERVER_SOFTWARE: nginx/1.15.11REMOTE_ADDR: 10.10.0.1REMOTE_PORT: 59820SERVER_ADDR: 10.10.0.133SERVER_PORT: 80SERVER_NAME: localhostGATEWAY_INTERFACE: CGI/1.1REQUEST_SCHEME: httpREDIRECT_STATUS: 200
F:
forensicsvolatilityvolatility_2.6_win64_standalone>volatility_2.6_win64_standalone.exe -f memdump.mem imageinfoVolatility Foundation Volatility Framework 2.6INFO    : volatility.debug    : Determining profile based on KDBG search...          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)                     AS Layer2 : FileAddressSpace (F:
forensicsvolatilityvolatility_2.6_win64_standalonememdump.mem)                      PAE type : No PAE                           DTB : 0x187000L                          KDBG : 0xf80003fea120L          Number of Processors : 4     Image Type (Service Pack) : 1                KPCR for CPU 0 : 0xfffff80003fec000L                KPCR for CPU 1 : 0xfffff88004500000L                KPCR for CPU 2 : 0xfffff8800457d000L                KPCR for CPU 3 : 0xfffff880009af000L             KUSER_SHARED_DATA : 0xfffff78000000000L           Image date and time : 2025-08-11 09:22:45 UTC+0000     Image local date and time : 2025-08-11 17:22:45 +0800
F:
forensicsvolatilityvolatility_2.6_win64_standalone>volatility_2.6_win64_standalone.exe -f memdump.mem --profile=Win7SP1x64 netscanVolatility Foundation Volatility Framework 2.6Offset(P)          Proto    Local Address                  Foreign Address      State            Pid      Owner          Created0x79d4e0           TCPv4    127.0.0.1:
9000                 127.0.0.1:
65026      CLOSED           -10x6455110          TCPv4    0.0.0.0:
3306                   0.0.0.0:0            LISTENING        2716     mysqld.exe0x6455110          TCPv6    :::
3306                        :::0                 LISTENING        2716     mysqld.exe0xfb45260          UDPv6    fe80::
e8fe:
835b:
aef8:
5951:
59954 *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x10480010         UDPv6    fe80::
e8fe:
835b:
aef8:
5951:
1900 *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x110a85a0         UDPv4    10.10.0.133:
59956              *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x11d34010         UDPv4    127.0.0.1:
1900                 *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x1651e5a0         UDPv4    10.10.0.133:
59956              *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x1945b5b0         UDPv4    0.0.0.0:
52018                  *:*                                   384      svchost.exe    2025-08-11 09:22:12 UTC+00000x2ab04010         UDPv4    0.0.0.0:0                      *:*                                   1172     iexplore.exe   2025-08-11 09:22:28 UTC+00000x2ab04010         UDPv6    :::0                           *:*                                   1172     iexplore.exe   2025-08-11 09:22:28 UTC+00000x2ad41010         UDPv4    0.0.0.0:0                      *:*                                   1172     iexplore.exe   2025-08-11 09:22:28 UTC+00000x2ad41010         UDPv6    :::0                           *:*                                   1172     iexplore.exe   2025-08-11 09:22:28 UTC+00000x2eb43ec0         UDPv4    10.10.0.133:
1900               *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x3d66c900         UDPv4    0.0.0.0:0                      *:*                                   3004     phpstudy_pro.e 2025-08-04 05:41:58 UTC+00000x3d66c900         UDPv6    :::0                           *:*                                   3004     phpstudy_pro.e 2025-08-04 05:41:58 UTC+00000x3d716be0         UDPv4    0.0.0.0:
64039                  *:*                                   384      svchost.exe    2025-08-11 09:22:36 UTC+00000x3d716be0         UDPv6    :::
64039                       *:*                                   384      svchost.exe    2025-08-11 09:22:36 UTC+00000x3da05130         UDPv4    0.0.0.0:0                      *:*                                   1504     svchost.exe    2025-08-04 05:02:04 UTC+00000x3da06680         UDPv4    10.10.0.133:68                 *:*                                   3036     svchost.exe    2025-08-11 09:22:06 UTC+00000x3da07840         UDPv4    0.0.0.0:0                      *:*                                   1504     svchost.exe    2025-08-04 05:02:04 UTC+00000x3da07840         UDPv6    :::0                           *:*                                   1504     svchost.exe    2025-08-04 05:02:04 UTC+00000x3daa3480         UDPv4    0.0.0.0:
63384                  *:*                                   384      svchost.exe    2025-08-11 09:22:03 UTC+00000x3dac0a90         UDPv4    0.0.0.0:0                      *:*                                   384      svchost.exe    2025-08-11 09:19:50 UTC+00000x3dac0a90         UDPv6    :::0                           *:*                                   384      svchost.exe    2025-08-11 09:19:50 UTC+00000x3dc2d560         UDPv4    0.0.0.0:
5355                   *:*                                   384      svchost.exe    2025-08-11 09:22:02 UTC+00000x3da299e0         TCPv4    0.0.0.0:
3306                   0.0.0.0:0            LISTENING        2116     mysqld.exe0x3da299e0         TCPv6    :::
3306                        :::0                 LISTENING        2116     mysqld.exe0x3daee160         TCPv4    0.0.0.0:
3306                   0.0.0.0:0            LISTENING        1904     mysqld.exe0x3daee160         TCPv6    :::
3306                        :::0                 LISTENING        1904     mysqld.exe0x3db168e0         TCPv4    0.0.0.0:
49157                  0.0.0.0:0            LISTENING        444      lsass.exe0x3dc094a0         TCPv4    127.0.0.1:
9000                 0.0.0.0:0            LISTENING        1928     xp.cn_cgi.exe0x3dca37a0         TCPv4    0.0.0.0:
3306                   0.0.0.0:0            LISTENING        1904     mysqld.exe0x3dca37a0         TCPv6    :::
3306                        :::0                 LISTENING        1904     mysqld.exe0x3dcf77f0         TCPv4    0.0.0.0:
49155                  0.0.0.0:0            LISTENING        428      services.exe0x3dcf77f0         TCPv6    :::
49155                       :::0                 LISTENING        428      services.exe0x3dd40380         TCPv4    0.0.0.0:
49155                  0.0.0.0:0            LISTENING        428      services.exe0x3ddf4340         TCPv4    0.0.0.0:
49156                  0.0.0.0:0            LISTENING        1504     svchost.exe0x3ddf9ee0         TCPv4    0.0.0.0:
49156                  0.0.0.0:0            LISTENING        1504     svchost.exe0x3ddf9ee0         TCPv6    :::
49156                       :::0                 LISTENING        1504     svchost.exe0x3de65010         UDPv6    ::1:
1900                       *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x3df82bf0         UDPv4    0.0.0.0:0                      *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3df93a50         UDPv4    0.0.0.0:0                      *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3df93a50         UDPv6    :::0                           *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e0c2af0         UDPv6    fe80::
e8fe:
835b:
aef8:
5951:
546  *:*                                   3036     svchost.exe    2025-08-11 09:22:02 UTC+00000x3e13cc70         UDPv4    0.0.0.0:
500                    *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e140a20         UDPv4    0.0.0.0:
4500                   *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e140a20         UDPv6    :::
4500                        *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e147010         UDPv4    0.0.0.0:
4500                   *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e15c010         UDPv4    0.0.0.0:
500                    *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3e15c010         UDPv6    :::
500                         *:*                                   900      svchost.exe    2025-08-04 05:02:03 UTC+00000x3deb95f0         TCPv4    0.0.0.0:
49154                  0.0.0.0:0            LISTENING        900      svchost.exe0x3debd450         TCPv4    0.0.0.0:
49154                  0.0.0.0:0            LISTENING        900      svchost.exe0x3debd450         TCPv6    :::
49154                       :::0                 LISTENING        900      svchost.exe0x3dec9680         TCPv4    127.0.0.1:
9000                 0.0.0.0:0            LISTENING        2700     xp.cn_cgi.exe0x3ded6940         TCPv4    10.10.0.133:
139                0.0.0.0:0            LISTENING        4        System0x3df47bd0         TCPv4    0.0.0.0:
49157                  0.0.0.0:0            LISTENING        444      lsass.exe0x3df47bd0         TCPv6    :::
49157                       :::0                 LISTENING        444      lsass.exe0x3df822e0         TCPv4    0.0.0.0:
445                    0.0.0.0:0            LISTENING        4        System0x3df822e0         TCPv6    :::
445                         :::0                 LISTENING        4        System0x3e162930         TCPv4    0.0.0.0:
135                    0.0.0.0:0            LISTENING        692      svchost.exe0x3e1678e0         TCPv4    0.0.0.0:
135                    0.0.0.0:0            LISTENING        692      svchost.exe0x3e1678e0         TCPv6    :::
135                         :::0                 LISTENING        692      svchost.exe0x3e174d00         TCPv4    0.0.0.0:
49152                  0.0.0.0:0            LISTENING        372      wininit.exe0x3e176630         TCPv4    0.0.0.0:
49152                  0.0.0.0:0            LISTENING        372      wininit.exe0x3e176630         TCPv6    :::
49152                       :::0                 LISTENING        372      wininit.exe0x3e1797b0         TCPv4    0.0.0.0:
49153                  0.0.0.0:0            LISTENING        772      svchost.exe0x3e1a4e60         TCPv4    0.0.0.0:
49153                  0.0.0.0:0            LISTENING        772      svchost.exe0x3e1a4e60         TCPv6    :::
49153                       :::0                 LISTENING        772      svchost.exe0x3e1b54f0         TCPv4    127.0.0.1:
65027                127.0.0.1:
443        CLOSED           -10x3ee184c0         UDPv4    127.0.0.1:
59957                *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x3f0d8310         UDPv4    0.0.0.0:
5355                   *:*                                   384      svchost.exe    2025-08-11 09:22:02 UTC+00000x3f0d8310         UDPv6    :::
5355                        *:*                                   384      svchost.exe    2025-08-11 09:22:02 UTC+00000x3f61bc00         UDPv4    10.10.0.133:
137                *:*                                   4        System         2025-08-11 09:19:50 UTC+00000x3f6a8010         UDPv4    10.10.0.133:
138                *:*                                   4        System         2025-08-11 09:19:50 UTC+00000x3f6ba970         UDPv6    ::1:
59955                      *:*                                   2628     svchost.exe    2025-08-11 09:19:50 UTC+00000x3f7be6e0         UDPv4    0.0.0.0:
56365                  *:*                                   384      svchost.exe    2025-08-11 09:22:06 UTC+00000x3f601180         TCPv4    0.0.0.0:
3306                   0.0.0.0:0            LISTENING        1384     dllhost.exe0x3f601180         TCPv6    :::
3306                        :::0                 LISTENING        1384     dllhost.exe0x3f772010         TCPv4    10.10.0.133:80                 10.10.0.1:
64000      CLOSED           -10x3fcb50e0         UDPv4    0.0.0.0:
58363                  *:*                                   384      svchost.exe    2025-08-11 09:22:00 UTC+00000x3fd14110         UDPv4    0.0.0.0:0                      *:*                                   3004     phpstudy_pro.e 2025-08-04 05:41:58 UTC+00000x3fd14110         UDPv6    :::0                           *:*                                   3004     phpstudy_pro.e 2025-08-04 05:41:58 UTC+00000x3fd59230         UDPv4    0.0.0.0:
5355                   *:*                                   384      svchost.exe    2025-08-11 09:22:02 UTC+00000x3fd59230         UDPv6    :::
5355                        *:*                                   384      svchost.exe    2025-08-11 09:22:02 UTC+00000x3fd7d010         UDPv4    0.0.0.0:
49997                  *:*                                   384      svchost.exe    2025-08-11 09:22:29 UTC+00000x3fc827a0         TCPv4    10.10.0.133:
64999              66.240.205.34:
9002   CLOSE_WAIT       -10x3fd7a7e0         TCPv4    10.10.0.133:80                 10.10.0.1:
59820      CLOSED           -1
F:
forensicsvolatilityvolatility_2.6_win64_standalone>strings memdump.mem | findstr /i .php > php_found.txt
DeviceHarddiskVolume2ToolsAntSword-Loader-v4.0.3-win32-x64AntSword.exe
DeviceHarddiskVolume2Toolsflag.txtratorDesktopflag.txt
F:
forensicsvolatilityvolatility_2.6_win64_standalone>volatility_2.6_win64_standalone.exe -f vol_easy.vmem --profile=Win7SP1x64 iehistoryVolatility Foundation Volatility Framework 2.6**************************************************Process: 1656 explorer.exeCache type "DEST" at 0x6bcb23dLast modified: 2025-07-23 17:37:39 UTC+0000Last accessed: 2025-07-23 09:37:40 UTC+0000URL: Administrator@http://192.168.186.140/uploads/6880ad58e4e88.php**************************************************Process: 1656 explorer.exeCache type "DEST" at 0x6bcb9ddLast modified: 2025-07-23 17:37:28 UTC+0000Last accessed: 2025-07-23 09:37:30 UTC+0000URL: Administrator@file:///C:/Tools/ezshell.php**************************************************Process: 1928 iexplore.exeCache type "DEST" at 0x4768235Last modified: 2025-07-23 17:37:29 UTC+0000Last accessed: 2025-07-23 09:37:30 UTC+0000URL: Administrator@http://192.168.186.140/index.php
Administrator:
500:
aad3b435b51404eeaad3b435b51404ee:
3b397b08d3203ddb1aae4a687651a310:::
Guest:
501:
aad3b435b51404eeaad3b435b51404ee:
31d6cfe0d16ae931b73c59d7e0c089c0:::
DeviceHarddiskVolume2Toolsscreenshot-20250723-171834.png
C:
phpstudy_prowww> dump_lass.bat[*]正在获取 lsass.exe PID..
[*]PID:
456
[*]正在尝试导出内存转储.[√]成功导出1sass内存？C:
phpstudy_proWwwlsass.dmp
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755480013-wxsync-2025-08-19f4a79fef72b87141bc5e667afe5c6e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755480015-wxsync-2025-08-a0eaf5c3c21f1899a7e5bcb2f749b7e5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755480017-wxsync-2025-08-922e3dd60264d9e9b1db1f149ab5c2bd.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755480019-wxsync-2025-08-c83933103ed53a6373523c135ba906d0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755480021-wxsync-2025-08-26e8da98ac809ac61393111ebf542902.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755480023-wxsync-2025-08-5df5cc23c9e98e7a5fe231b18e2dcde0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755480025-wxsync-2025-08-c88e18e9a8f4f90e8dd9db61f0040925.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755480027-wxsync-2025-08-cac6bfd31089a031683d6f5d04b9631a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755480028-wxsync-2025-08-a799fa4a386a0a91a4f4cfcb772a9602.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755480030-wxsync-2025-08-c35c6aa922b75ba53926509bf83f44da.png)