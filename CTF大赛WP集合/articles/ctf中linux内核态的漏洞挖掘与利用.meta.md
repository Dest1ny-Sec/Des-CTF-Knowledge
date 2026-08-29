---
title: ctf 中 linux 内核态的漏洞挖掘与利用
contest: ctf-share
year: 2018
difficulty: hard
vuln_type: pwn_unknown
tags: [kernel-pwn, stack-overflow, smep-bypass, smap-bypass, kallsyms-leak, rop, iretq, kernel-fs, randstruct]
attack_chain:
  - core.ko ioctl 0x6677889C 设置 off 全局变量
  - ioctl 0x6677889B 触发 core_read 泄 canary + ret_addr
  - 写入 0x100 字节到 name
  - ioctl 0x6677889A 传 -0xa000...8 绕过有符号长度检查
  - core_copy_func 栈溢出 0x58 字节
  - 内核 shellcode: commit_creds(prepare_kernel_cred(0))
  - SMEP/SMAP 开启时改 ROP 链
  - swapgs + iretq 返回用户态
  - zerofs 内核文件系统 OOB 读 cred
key_payload: 内核栈溢出 ROP + kallsyms 提权函数
one_liner: V-lab 实验室 CTF 内核漏洞挖掘教程，覆盖 core.ko 栈溢出 + zerofs 内核文件系统越界读写两套思路。
lesson: 内核栈溢出要点：先泄 canary/ret_addr，再 ROP 走 prepare_kernel_cred(0) → commit_creds 提权，最后 iretq 返用户态；SMEP/SMAP 开启必须 ROP。
quality: high
---

V-lab 实验室出品，CTF 内核态漏洞挖掘与利用两套实战：core.ko 栈溢出 + zerofs 内核文件系统 OOB。

**第一题：core.ko 栈溢出**

环境：qemu -m 512M 启动，启 kaslr、kptr_restrict、dmesg_restrict；core.cpio 解包修改 init 关掉 poweroff；core.ko 开了 NX + stack canary。

漏洞函数链：
- `init_module` → `proc_create("core", ...)` + `file_operations` 三个回调
- `core_ioctl(0x6677889b) → core_read(param)`：可控全局变量 off，输出 0x40 字节到用户态
- `core_ioctl(0x6677889c, off)`：设置 off 全局变量
- `core_ioctl(0x6677889a) → core_copy_func(size)`：把 name 拷贝到栈上，但有符号对比 `(long)size < 0x40`，传 `0xf000000000000058` 绕过
- `core_write` 写 name 全局变量

利用：
1. 调 `core_ioctl(0x6677889c, 64)` 设 off
2. 调 `core_ioctl(0x6677889b, buf)` 泄 canary + ret_addr
3. 写 name 为 `[pad*8, canary, 0, &shellcode]`
4. 调 `core_ioctl(0x6677889a, 0xf000000000000058)` 触发栈溢出
5. shellcode 走 `commit_creds(prepare_kernel_cred(0))` + `mov rbp, rsp; pop rbp; jmp ret_addr` 修复栈帧

**SMEP/SMAP 开启版本**

shellcode 不能再跳到用户态代码。改用 ROP 链：
- `pop rdi; ret` (FFFFFFFF81126515)
- `pop rcx; ret` (FFFFFFFF8186EB33)
- `pop rdx; ret` (FFFFFFFF810A0F49)
- `mov rdi, rax; call rcx` (FFFFFFFF81623D0B)
- `commit_creds; swapgs; popfq; ret` (FFFFFFFF81A012DA)
- `iretq` (FFFFFFFF81050AC2)
- iretq 框：`[ret_addr, user_cs, user_rflags, user_sp, user_ss]`

先用 `cat /tmp/kallsyms | grep prepare_kernel_cred/commit_creds` 拿到函数地址；用 `extract-vmlinux bzImage > vmlinux` 提取内核可执行文件，`ropper --file ./vmlinux --nocolor > gadgets` 提取 gadgets。

**第二题：zerofs 内核文件系统 OOB**

环境：smep + smap + kaslr 都开，`zerofs.ko` 文件系统模块，mount 到 /mnt 后读写文件触发回调。

漏洞：zerofs 读函数不检查文件大小为 -1 时的越界读；写函数不检查偏移 + size 造成越界写。

利用：
1. 构造符合 zerofs 格式的 image（参考 simplefs 源码，第 1 块 superblock + 第 2 块 inode 索引 + 数据块）
2. 写文件时偏移调大，触发内核地址越界写
3. 读文件时 size=-1 + 偏移扫描内核内存，匹配连续 3 个 32 位整型 == 1000 来定位当前进程的 cred 结构
4. 越界写 cred 的 uid/gid/suid/sgid/fsgid 等字段为 0，提权
5. 难点：rand_struct 插件改变了部分结构体内部偏移，需要在 `prepare_creds` 内部下断点观测

作者使用 zerofs 思路时绕过了 kallsyms 读取限制（kptr_restrict=2），是内核文件系统类题目的高阶解法。
