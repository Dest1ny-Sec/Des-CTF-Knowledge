---
title: Understanding Dirty Pagetable – m0leCon Finals 2023 CTF Writeup
contest: m0leCon Finals 2023
year: 2023
difficulty: hard
vuln_type: rop
tags: [linux_kernel, modprobe_path, dirty_pagetable, commit_creds, find_task_by_vpid, switch_task_namespaces, copy_fs_struct, kpti_trampoline, userfaultfd, custom_shellcode, ret2usr_64]
attack_chain: 通过 modprobe_path 触发自定义 shellcode → call a:pop r15 取 kaslr offset → commit_creds(init_cred) → find_task_by_vpid(1) → switch_task_namespaces(task, init_nsproxy) → copy_fs_struct(init_fs) → find_task_by_vpid(getpid()) → 改 current->fs=0x740 → kpti_bypass 跳回用户态
key_payload: lea rdi, [r15 + init_cred] / mov [rsp+0x00], rax (zero) / mov [rsp+0x10], 0x2222222222222222 (win) / mov rax, 0x3333333333333333 (cs)
one_liner: m0leCon Finals 2023 决出的 Linux 内核 PWN 题 Dirty Pagetable 完整 shellcode 复盘，覆盖 kaslr 定位+提权+namespace+fs+KPTI bypass 完整六件套。
lesson: Linux kernel exploit 的 6 步经典链：commit_creds(init_cred) → find_task_by_vpid(1) → switch_task_namespaces → copy_fs_struct → 改 current->fs → kpti_trampoline 跳回。
quality: high
---
