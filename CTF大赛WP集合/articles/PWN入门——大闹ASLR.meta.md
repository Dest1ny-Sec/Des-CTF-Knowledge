---
title: PWN入门 - 大闹 ASLR
contest: 看雪论坛 ctfiot 系列
year: 2024
difficulty: high
vuln_type: pwn_unknown
tags: [pwn, 教程, ASLR, linux-kernel, VFS, proc, sysctl, ELF-loader]
attack_chain:
  - 三档 ASLR 控制：0 全关 / 1 部分 / 2 全开 (堆栈 mmap libc)
  - echo xxx | sudo tee -a /proc/sys/kernel/randomize_va_space
  - proc 虚文件系统注册 (file_system_type + super_block)
  - sysctl kern_table.procname=randomize_va_space + proc_dointvec 写
  - load_elf_binary: personality & ADDR_NO_RANDOMIZE + randomize_va_space 设 PF_RANDOMIZE
  - arch_mmap_rnd: get_random_long() & ((1<<rndbits)-1) << PAGE_SHIFT
  - arch_randomize_brk: range=0x02000000 + get_random_long()%range << PAGE_SHIFT
  - randomize_stack_top: get_random_long() & STACK_RND_MASK (0x3fffff) << PAGE_SHIFT
  - 栈分配后 arch_align_stack 再 sp -= prandom_u32_max(8192); sp &= ~0xf
  - 详解 32 位 vs 64 位 mmap_rnd_bits = 32
  - 绕过思路：稳定泄露某元素地址 = 减偏移 = 得 libc 基址
key_payload: (get_random_long() & ((1UL<<32)-1)) << 12 = mmap 随机偏移
one_liner: 从 Linux VFS/proc 虚文件系统、sysctl 接口逐层下钻到 load_elf_binary 内核 ELF 加载器，详解 ASLR 0/1/2 三档随机化原理。
lesson: ASLR 随机化是加载期 (load_elf_binary) 一次性完成，运行期不可改；mmap 32 bit 随机 + 12 bit 页对齐，栈 22 bit 随机 + 12 bit 对齐；只要能稳定泄露一个地址 = 全部可控。
quality: high
---
