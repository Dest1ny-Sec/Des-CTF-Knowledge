# 有趣的Hack-A-Sat黑掉卫星挑战赛——被破坏的阿波罗计算机（解法一）

> 原文: https://www.ctfiot.com/97721.html
> ID: 97721

国家太空安全是国家安全在空间领域的表现。随着太空技术在政治、经济、军事、文化等各个领域的应用不断增加，太空已经成为国家赖以生存与发展的命脉之一，凝聚着巨大的国家利益，太空安全的重要性日益凸显[1]。而在信息化时代，太空安全与信息安全紧密地结合在一起。

2020年9月4日,美国白宫发布了首份针对太空网络空间安全的指令——《航天政策第5号令》，其为美国首个关于卫星和相关系统网络安全的综合性政策，标志着美国对太空网络安全的重视程度达到新的高度。在此背景下，美国自2020年起，连续两年举办太空信息安全大赛“黑掉卫星（Hack-A-Sat）”，在《Hack-A-Sat太空信息安全挑战赛深度解析》一书中有详细介绍，本文介绍了Hack-A-Sat黑掉卫星挑战赛的

寻找阿波罗导航计算机中被修改的PI（apollo_gcm）这道赛题的解题过程。

题目介绍

Step right up, here’s one pulled straight from the history books. See if you can DSKY your way through this challenge! (Thank goodness VirtualAGC is a thing…)

从上述题目介绍可知，这道题目需要比较旧的知识，与阿波罗导航计算机（Apollo Guidance Computer，AGC）相关，并且要用到DSKY。DSKY是AGC的输入/输出，类似于现代计算机的显示器、键盘。

主办方给出了一个链接地址，使用netcat打开该链接后，会获得一段提示信息，如下：

The rope memory in the Apollo Guidance Computer experienced an unintended ‘tangle’ just prior to launch. While Buzz Aldrin was messing around with the docking radar and making Neil nervous; he noticed the value of PI was slightly off but wasn’t exactly sure by how much. It seems that it was changed to something slightly off 3.14 although still 3 point something.

The Commanche055 software on the AGC stored the value of PI under the name “PI/16”, and

although it has always been stored in a list of constants, the exact number of constants in that memory region has changed with time.

Help Buzz tell ground control the floating point value PI by connecting your DSKY to the AGC Commanche055 instance that is listening at 172.17.0.1:
19008

What is the floating point value of PI?:

通过分析，主要给出如下信息：

阿波罗飞船就要发射，但是飞船上的AGC出现了一点状况，其中圆周率PI的值发生了变化，不再是14，而是有一点点变化，但是还是3点几。

PI值是通过AGC上的Commanche055软件存储的，存储的名称是“PI/16”。

PI与其他常数存储在一起，因为常数的数量会有变化，所以存储位置不固定。

AGC上的存储器是线存储器（Rope Memory）。

使用DSKY通过地址17.0.1:
19008可以连接到AGC的Commanche055软件。

要求参赛者找到当前PI的值。

编译及测试

这个挑战题的代码位于apollo目录下，查看challenge、solver目录下的Dockerfile，发现其中用到的是python:3.7-slim，为了加快题目的编译进度，在apollo目录下新建一个文件sources.list，内容如下：

deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib

deb-src https://mirrors.aliyun.com/debian/ bullseye main non-free contrib

deb https://mirrors.aliyun.com/debian-security/ bullseye-security main

deb-src https://mirrors.aliyun.com/debian-security/ bullseye-security main

deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib

deb-src https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib

deb https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib

deb-src https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib

将sources.list复制到apollo、challenge、solver目录下，修改challenge、solver目录下的Dockerfile，在所有的FROM python:3.7-slim下方添加：

ADD sources.list /etc/apt/sources.list

打开终端，进入apollo所在目录，执行命令：

sudo make build

此时如果使用make test命令进行测试，等待30～60秒，会出现如图7-10所示的结果。可以发现测试中，找到的PI值由两个八进制数组成（AGC采用八进制表示各种数据），具体解释后面会有介绍，找到PI值后，题目给出了flag值。

图7-10  apollo挑战题的测试结果

相关背景知识

1．阿波罗导航计算机AGC

阿波罗计划是美国在1961年—1972年组织实施的一系列载人登月飞行任务，其目的是实现载人登月飞行和人对月球的实地考察，为载人行星飞行和探测进行技术准备。它是世界航天史上具有划时代意义的一项成就。阿波罗计划始于1961年5月，至1972年12月第6次登月成功结束，历时约11年，耗资255亿美元。阿波罗号飞船由指挥舱、服务舱和登月舱3部分组成。

（1）指挥舱：是宇航员在飞行中生活和工作的座舱，也是全飞船的控制中心。指挥舱为圆锥形，高3.2m，重约6吨。指挥舱分前舱、宇航员舱和后舱3部分。前舱内放置着陆部件、回收设备和姿态控制发动机等。宇航员舱为密封舱，存有供宇航员生活14天的必需品和救生设备。后舱内装有10台姿态控制发动机，各种仪器和贮箱，姿态控制、制导导航系统，以及船载计算机和无线电分系统等。

（2）服务舱：其前端与指挥舱对接，后端有推进系统主发动机喷管。舱体为圆筒形，高6.7m，直径4m，重约25吨。主发动机用于轨道转移和变轨机动。姿态控制系统由16台火箭发动机组成，用于飞船与第三级火箭分离、登月舱与指挥舱对接和指挥舱与服务舱分离等。

（3）登月舱：由下降级和上升级组成，地面起飞时重14.7吨，宽4.3m，最大高度约7m。其中下降级由着陆发动机、4根着陆架和4个仪器舱组成，上升级是登月舱主体。宇航员完成月面活动后驾驶上升级返回环月轨道与指挥舱会合。上升级由宇航员座舱、返回发动机、推进剂贮箱、仪器舱和控制系统组成。宇航员座舱可容纳2名宇航员，舱内设有导航、控制、通信、生命保障和电源等设备。

AGC是阿波罗计划中的主要船载计算机，使用在所有的登月任务中。指挥舱和登月舱都有AGC，但是两者运行的软件不同。AGC及其软件是在麻省理工学院仪器实验室（现在称为德雷珀实验室）开发的。性能参数如下：

RAM为2048字，一个字是15bit。

ROM为36864字，一个字是15bit。

每秒最多可执行85 000条指令。

使用28V直流供电，电流为5A。

具备输入输出DSKY。

题目中使用的是VirtualAGC。VirtualAGC是AGC爱好者制作的一个AGC模拟器，是开源软件，可以运行AGC上的程序。此外，AGC普遍使用的是八进制，本书采用Python的写法，数字前加“0o”表示八进制数，还有一种表示方法，就是数字加一个下标“8”。

2．线存储器

线存储器是一种只读存储器（ROM）。利用磁环改变导线上电压的状态，如果导线穿过磁环，导线上的电压就会发生改变。系统检测到这种改变后，就会把这条导线上的数据解释为1，如果导线没有穿过磁环，那么导线上的电压不发生改变，系统就会把这条导线上的数据解释为0。线存储器如图7-11所示。

（a）

（b）

（c）

图7-11  线存储器

AGC上的ROM是以Bank组织的，每个bank为1024字，每个字为15bit，每个Bank中的字的地址是从0o2000（对应十进制1024）开始的，所以给出一个数据的Bank号及Bank中的地址address，可以计算实际地址，方法为：

Bank×20008 + address – 20008

例如，第0o27个Bank中的地址0o3355，对应的实际地址为：

278×20008 + 33558 – 20008 = 573558

3．DSKY

DSKY类似于现代的显示器和键盘，但是那时候的显示器和键盘比较简单，如图7-12、图7-13所示。可以发现，上半部分是两个显示屏，下半部分是一个键盘，可以用于输入。

图7-12  DSKY

图7-13  飞船舱内操作面板，其中中间偏左有DSKY

为了更加清晰地了解DSKY，这里以VirtualAGC中实现的yaDSKY（yet another DSKY）为例进行介绍，其界面如图7-14所示。yaDSKY就是DSKY的模拟器，其界面和功能是完全一致的。

先介绍上半部分的显示屏，需要关注的是右半边，都是使用7段数码管来实现的，第二行有一个VERB，下方对应两个7段数码管，第二行还有一个NOUN，下方也对应两个7段数码管，接下来是三行连续的显示，每一行都是5个7段数码管，而且每一行最前方有一个类似加号的显示，显示的是正、负。

再介绍下半部分的键盘，需要关注的是，最左边一个按键名称是VERB，另一个是NOUN，与上半部分的显示刚好对应。在最右边有一个按键名称是ENTR，应该就是类似于现代键盘的回车键。

图7-14  yaDSKY的界面

这里就涉及DSKY的操作方法了，DSKY采用动词VERB（简称V）+名词NOUN（简称N）的方式进行控制操作，其中V、N的部分取值及其作用如图7-15所示。

（a）V的取值

（b）N的取值

图7-15  DSKY的V、N的部分取值（续）

注意到其中V的取值最下面的0o27，可以用来显示存储器中的数据，所以使用DSKY查询存储器特定地址的方式为：依次输入V27N02E，然后会发现DSKY上27、02两个数字会闪，此时输入57355，按ENTR键，即可得到地址为57355的数字，并在下面3行的第1行显示。此时再次按ENTR键，又可以输入一个地址，再按ENTR键，就会显示存储器中这个新地址存储的数据，如图7-16所示。

图7-16  使用DSKY读取ROM指定地址存储的数据

4．AGC中浮点数表示

AGC中字有15位，还带1个奇偶校验位，但是这个奇偶校验位只供硬件使用，软件访问不了。一个字采用MSB的方式，最高位是第15位，最低位是第1位，如图7-17所示，最后一个P是奇偶校验位。

图7-17  AGC中字的格式

1）单精度浮点数（Single-Precision，SP）的格式

SP使用一个15位的字表示，第15位是符号位，为1表示负数，为0表示正数。第14～第1位构成SP的小数部分。如果是正数，那么SP的值就是：

如果是负数，那么SP的值就是：

比如：

+0 在AGC中使用SP表示，就是000000000000000；

-0 在AGC中使用SP表示，就是111111111111111；

1/2 在AGC中使用SP表示，就是01000000000000；

-1/2 在AGC中使用SP表示，就是101111111111111；

1/4 在AGC中使用SP表示，就是001000000000000；

3/4 在AGC中使用SP表示，就是011000000000000。

2）双精度浮点数（Double-Precision，DP）的格式

为了提高精度，使用两个连续的15位的字表示一个DP。前一个字称为字1，后一个字称为字0，字1的第14位～第1位表示较高的有效位，字0的第14位～1位表示较低的有效位，并且字1的第15位是符号位，如图7-18所示。

图7-18  DP格式

一般而言，这两个字的第15位是一致的，但是也有不一致的情况，这里只考虑一致的情况。如果是正数，那么DP的值就是：

如果是负数，那么DP的值就是：

现在，回头检查一下前文在进行测试时，显示的PI/16的结果，如图7-10所示，为0o6413 0o11416，这是一个DP，按照DP的定义，其对应的十进制数为：

这个就是PI/16的值，将其乘以16，得到PI的值为3.26103293895721435546875，可见确实是偏了一点。

解法一

因为VirtualAGC是开源软件，所以可以得到其源代码，检索VirtualAGC上Commanche055的代码，可以知道PI/16的存储位置，如图7-19所示，位于0o27 Bank，0o3355 address。通过前面的介绍，可以知道如果使用DSKY查询，那么地址应该就是 0o57355，并且知道在PI/16下一个位置存储的值是0o37777，所以解法一的思路就是使用DSKY从理论上PI/16的存储位置0o57355处开始读取线存储器中的数据，直到读取到的数据是0o37777为止，此时再回头读出前两个位置的数据，就是PI/16的值。

为此，需要先安装Virtual AGC，以使用其中的yaDSKY。需要使用32位的Linux系统，此处使用的Ubuntu14.04 32位版本。在Ubuntu14.04 32位版本上，Virtual AGC安装步骤如下：

（1）从ibiblio下载Ubuntu上的Virtual AGC的安装包。

（2）安装tk、libsdl1.2、libncurses5、liballegro4.4、libgtk2.0、libwxgtk2.8，如果安装libsdl1.2提示找不到对应的包，可以安装libsdl1.2-dev。

（3）在根目录下使用sudo find / -name “libwx_gtk2u_core-2.8.so.0″寻找库文件，发现在目录/usr/lib/x86_64-linux-gnu/下，于是使用命令edit ~/.bashrc编辑环境变量，添加如下语句：

export LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

图7-19  检索Commanche055代码，得到PI/16的存储位置

（4）执行命令source ~/.bashrc，更新环境变量。

（5）解压缩下载的VirtualAGC安装包，在Resource目录下，执行yaDSKY程序，如图7-20所示。注意不要在bin目录下执行yaDSKY，会提示找不到图片资源。

图7-20  在Resource目录下，执行yaDSKY程序

（6）为了连接到主办方给出的链接地址，还需要在yaDSKY后面添加一些参数，其中IP地址、端口号需要依据实际情况修改：

../bin/./yaDSKY2 –ip=192.168.43.10 –port=31450

本书在本地主机进行测试时，使用虚拟机安装Ubuntu14.04 32位版本运行yaDSKY程序，此时可以使用如下步骤：

（1）在宿主机执行如下命令，运行挑战题的容器。

sudo socat -v tcp-listen:
31450,reuseaddr exec:”docker run –rm -i -e SERVICE_HOST=17192.168.43.10 -e SERVICE_PORT=19008 -p 19008\:
19697 -e SEED=1234 -e FLAG=flag{zulu\:
GG1EnNVMK3} apollo\:
challenge”

（2）在虚拟机中打开一个终端，执行：

nc 192.168.43.10 31450

（3）在虚拟机中再打开一个终端，到Resources目录下，执行：

../bin/./yaDSKY2 –ip=192.168.43.10 –port=31450

这样就可以连接上了。

输入V27N02E后，27、02两个数字会闪，此时输入0o57355，如图7-21所示。

图7-21  输入读取ROM的指令及要读取的ROM地址

按ENTR键，即可得到地址为0o57355的数字，在第一行显示，如图7-22所示。

图7-22  ROM地址0o57355处的数据

此时再次按ENTR键，然后又可以输入一个地址，再按ENTR键，就会显示这个新地址的数据。如此继续，直到读取到的数据为0o37777，如图7-23所示。

图7-23  在地址0o57367处读取的数据是0o37777

所以PI/16的值，应该存储在地址0o57365、0o57366处，如图7-24所示（注意，每次测试时，这两处存储的数据都会变化，所以读者在测试的时候，可能不是图中的值，但是方法是一样的）。按照前文的计算方法，得到PI/16的值为：

从而得到PI的值为3.77239286899566650390625，将该结果输入终端，可以得到flag信息，如图7-25所示。

图7-24  存储在地址0o57365、0o57366处的数据

图7-25  输入读取到的PI值，得到flag

原文始发于Freebuf(hackasat)：有趣的Hack-A-Sat黑掉卫星挑战赛——被破坏的阿波罗计算机（解法一）