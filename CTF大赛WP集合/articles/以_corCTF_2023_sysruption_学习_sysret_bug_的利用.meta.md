---
title: corCTF 2023 sysruption SYSRET bug 利用学习
contest: corCTF
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [Linux-Kernel, SYSRET, canonical-address, EntryBleed, KASLR-bypass, side-channel, qemu-host-cpu, x86_64, FizzBuzz101, Crusaders-of-Rust]
attack_chain:
  - qemu-system-x86_64 -cpu host -enable-kvm + Linux 6.3.4
  - -cpu host 触发 EntryBleed 侧信道，绕过 KASLR
  - Patch entry_64.S: 删除 SYSRET 前的 canonical address check
  - shl $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx + sar + cmpq %rcx, %r11 + jne slow_exit
  - 删除后, SYSRET 返回 non-canonical RCX/RIP 在内核态 #GP
  - 本质让用户接管内核，因为用户态控制 RSP
  - 用户态 syscall → 内核态处理 → SYSRET 跳 non-canonical → #GP 异常
  - #GP 处理路径用户可控 → 内核代码执行
  - 利用：构造特定 non-canonical 地址 + 准备 #GP handler
key_payload: 'qemu -cpu host + EntryBleed + 删除 canonical check + SYSRET non-canonical RCX/RIP + #GP 用户态控制'
one_liner: corCTF 2023 sysruption：Linux Kernel 6.3.4 删除 SYSRET canonical 检查 + EntryBleed 侧信道绕过 KASLR，内核 RCE。
lesson: SYSRET canonical check 是 Intel/AMD 长期存在的硬件 bug 缓解措施，删除后用户态可控制内核 RSP 触发内核执行。
quality: high
---

# corCTF 2023 sysruption - SYSRET bug 利用学习

**来源**: ctfiot.com ID 166547
**作者**: 来自 Crusaders-of-Rust 战队
**出题人**: FizzBuzz101
**仓库**: https://github.com/Crusaders-of-Rust/corCTF-2023-public-challenge-archive/tree/master/pwn/sysruption

## 题目环境
```bash
#!/bin/sh
qemu-system-x86_64 \
    -m 4096M \
    -smp 1 \
    -nographic \
    -kernel "./bzImage" \
    -append "console=ttyS0 loglevel=3 panic=-1 pti=off kaslr" \
    -no-reboot \
    -monitor /dev/null \
    -cpu host \
    -netdev user,id=net \
    -device e1000,netdev=net \
    -initrd "./initramfs.cpio.gz" \
    -enable-kvm
```

## 漏洞

### Patch
```diff
--- orig_entry_64.S
+++ linux-6.3.4/arch/x86/entry/entry_64.S
@@ -150,13 +150,13 @@
        ALTERNATIVE "shl $(64 - 48), %rcx; sar $(64 - 48), %rcx",
                "shl $(64 - 57), %rcx; sar $(64 - 57), %rcx", X86_FEATURE_LA57
 #else
-       shl     $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
-       sar     $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
+       # shl   $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
+       # sar   $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
 #endif
 
        /* If this changed %rcx, it was not canonical */
-       cmpq    %rcx, %r11
-       jne     swapgs_restore_regs_and_return_to_usermode
+       # cmpq  %rcx, %r11
+       # jne   swapgs_restore_regs_and_return_to_usermode
```

### 删除的检查
- 原意：%rcx 是 non-canonical 地址时，跳到 slow exit path
- 删除后：fast exit path 走 SYSRET，但 RCX 是 non-canonical

### Canonical Address
- 高 17 bit 必须相同（48-bit 寻址）
- 范围: 0~0x7fffffffffff（用户态）+ 0xffff800000000000~0xffffffffffffffff（内核态）
- 48-bit 寻址 + 4 级页表

## EntryBleed 侧信道
- `-cpu host` 触发 EntryBleed（CVE-2022-4543 等）
- 类似 MDS / TAA 攻击
- 此前 SCTF 考过
- 利用侧信道绕过 KASLR

## entry_SYSCALL_64 分析

### 关键指令
```asm
SYM_CODE_START(entry_SYSCALL_64)
    UNWIND_HINT_ENTRY
    ENDBR
    swapgs
    movq %rsp, PER_CPU_VAR(cpu_tss_rw + TSS_sp2)
    SWITCH_TO_KERNEL_CR3 scratch_reg=%rsp
    movq PER_CPU_VAR(pcpu_hot + X86_top_of_stack), %rsp
    
    /* Construct struct pt_regs on stack */
    pushq $__USER_DS            /* pt_regs->ss */
    pushq PER_CPU_VAR(cpu_tss_rw + TSS_sp2)  /* pt_regs->sp */
    pushq %r11                  /* pt_regs->flags */
    pushq $__USER_CS            /* pt_regs->cs */
    pushq %rcx                  /* pt_regs->ip */
    pushq %rax                  /* pt_regs->orig_ax */
    PUSH_AND_CLEAR_REGS rax=$-ENOSYS
    
    movq %rsp, %rdi             /* pt_regs addr */
    movslq %eax, %rsi           /* syscall number */
    call do_syscall_64
    
    /* Try SYSRET */
    movq RCX(%rsp), %rcx
    movq RIP(%rsp), %r11
    cmpq %rcx, %r11             /* SYSRET requires RCX == RIP */
    jne swapgs_restore_regs_and_return_to_usermode
    
    /* Canonical address check 删除！ */
    shl $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
    sar $(64 - (__VIRTUAL_MASK_SHIFT+1)), %rcx
    /* If this changed %rcx, it was not canonical */
    cmpq %rcx, %r11
    jne swapgs_restore_regs_and_return_to_usermode
    /* (删除后) */
    
    cmpq $__USER_CS, CS(%rsp)
    jne swapgs_restore_regs_and_return_to_usermode
    
    /* 真正 SYSRET */
    popq %rdi
    ...
    sysretq
```

## 攻击流程
1. 用户态 syscall 进入 entry_SYSCALL_64
2. 内核态处理 syscall
3. 准备 SYSRET 弹出 pt_regs 到 RCX/R11
4. RCX 是 non-canonical 地址
5. SYSRET → 用户态跳到 non-canonical 地址 → #GP
6. #GP handler 在用户态注册 → 内核态执行
7. 用户态控制 RSP → 内核栈劫持

## 关键技术
- **SYSRET 硬件 bug**：Intel/AMD SYSRET 遇到 non-canonical RCX/RIP 在内核 #GP
- **canonical address check 缓解**：删除后恢复漏洞
- **EntryBleed**：侧信道通过 -cpu host 绕过 KASLR
- **#GP handler 用户态注册**：通过修改 IDT/GDT 接管异常处理
- **RSP 用户态控制**：用户栈指针在内核态有效

## 评价
corCTF 2023 sysruption 顶级 Linux Kernel PWN 题：
- 深入理解 SYSRET 微架构行为
- canonical address 与 48-bit 寻址
- EntryBleed 侧信道绕过 KASLR
- 内核态 #GP handler 用户劫持

是 Linux Kernel 高级研究案例。
