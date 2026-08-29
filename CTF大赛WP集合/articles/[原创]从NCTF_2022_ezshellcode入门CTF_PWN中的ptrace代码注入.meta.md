---
title: [原创] 从 NCTF 2022 ezshellcode 入门 CTF PWN 中的 ptrace 代码注入
contest: NCTF 2022
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [ptrace_attach, ptrace_scope_disabled, shellcode_two_process, seccomp_sandbox_bypass, mmap_rwx_0x401000, getregs_setregs_rip_modify, ptrace_peekdata_pokedata, fork_parent_child_pwn, pwn_shellcode_codegen]
attack_chain: 程序 mmap(0x401000, 0x1000) rwx + 读 shellcode + seccomp 禁 socket + close(0/1/2) → fork 父子进程 → 子进程 0x401000 跳 shellcode (此时未 close 0/1/2) → 父进程 ptrace(PTRACE_ATTACH, pid) + ptrace(PTRACE_SYSCALL) + wait4 → rax==0 持续 (防 read 被打断) → rax!=0 时 setregs rip=0x401000 → detach → 子进程执行 shellcraft.sh() → /bin/sh
key_payload: echo 0 > /proc/sys/kernel/yama/ptrace_scope / shellcode = shellcraft.ptrace(0x10,PTRACE_ATTACH)+ptrace(0x18,DETACH)+wait4+ptrace(12,GETREGS)+setregs rip=0x401000+ptrace(13,SETREGS)+ptrace(17,DETACH) / 跳过 close(0/1/2)
one_liner: NCTF 2022 ezshellcode：父子进程 ptrace 注入绕过 close(0/1/2) + seccomp 沙箱，父进程 PTRACE_ATTACH+SYSCALL+GETREGS+SETREGS rip=0x401000 控制子进程直接 shellcraft.sh()。
lesson: ptrace_scope = 0 是 Linux 容器 CTF 标配；父子进程 ptrace 注入跳过 sandbox 限制是 2022 流行 pwn 技巧；PTRACE_GETREGS 改 RIP 是控制子进程 PC 指针的通用方法。
quality: high
---
