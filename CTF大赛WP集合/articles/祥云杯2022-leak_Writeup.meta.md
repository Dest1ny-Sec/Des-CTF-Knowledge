---
title: 祥云杯2022-leak Writeup
contest: 祥云杯2022
year: 2022
difficulty: hard
vuln_type: heap_exploit
tags: [glibc 2.27-1.6, UAF, IO结构体伪造, _IO_write_base泄露, fastbin reverse into tcache, tcache双链表, 堆地址泄露, 0xfbad1800]
attack_chain: 入口读flag到堆→add/delete/edit有UAF无show→fastbin reverse into tcache写堆地址到IO结构体→修改stdout._flags=0xfbad1800 + _IO_write_base=堆地址→exit时泄露堆内容→堆地址已知→改stdout写指针到libc→获取system
key_payload: "stdout._flags=0xfbad1800;_IO_write_base=heap_addr;fastbin->bk=&tcache[size];tcache双链表fd/bk;glibc 2.27-1.6;flag在堆上"
one_liner: 祥云杯2022 leak：glibc 2.27堆题+IO结构体泄露+fastbin reverse into tcache
lesson: 无show的2.27堆题：IO结构体伪造 + fastbin reverse into tcache利用堆地址
quality: high
---

# 祥云杯2022-leak Writeup

**赛事**：祥云杯2022

**难度**：高质量堆题

**题目特征**：
- glibc **2.27 1.6版本**（tcache双链表）
- 实现增删改功能
- 没有查（4、5选项目测是摆设）
- 入口把flag内容读到堆上
- delete操作存在 **UAF漏洞**

**核心思路**：

**Step 1：IO结构体泄露原理**
- 题目没有IO函数 → IO结构体未初始化
- **关键知识点**：设置 stdout._flags = 0xfbad1800 + exit
- exit时输出 _IO_write_base 到 _IO_write_ptr 之间的内容
- 逐字节打印，只有不可读内存才崩溃
- _IO_write_base 改成堆地址 → 泄露堆内容（flag）

**Step 2：写堆地址到IO结构体**
- 没有泄漏堆地址 → 用 **fastbin reverse into tcache**

**fastbin reverse into tcache 原理**（2.27 1.4+ 双链表）：
- 2.27 1.4版本前：tcache没有bk指针
- 2.27 1.4+：tcache有 fd + bk
- glibc 在 fastbin 链入 tcache 时执行：
  ```
  fastbin->fd = tcache[size]->fd
  fastbin->bk = &tcache[size]
  tcache[size]->fd = fastbin
  ```
- → **任意写一个堆地址**

**Step 3：UAF利用**
- 2.27 1.6开始检测double free
- 不能直接double free（遍历tcache检测相同指针）
- 需要堆重叠思路

**Step 4：布局策略**
- 0、1两个chunk互刷填满tcache
- 1、2两个chunk free得到两个fastbin
- 利用fastbin构造fd指向target
- 改tcache对应size数量 < 7
- 再申请该大小fastbin → 写堆地址到 target + 0x18

**交互函数**：
```python
def choice(ch): p.sendlineafter(b'Your choice: ', str(ch))
def add(index, size):
    choice(1); p.sendlineafter(b'Index: ', str(index))
    p.sendlineafter(b'Size: ', str(size))
def edit(index, content):
    choice(2); p.sendlineafter(b'Index: ', str(index))
    p.sendafter(b'Content: ', content)
def free(index):
    choice(3); p.sendlineafter(b'Index: ', str(index))
```

**关键payload**：
- `add(1, 0x30)` 
- `add(4, 0x20)`
- `add(2, 0x30)`
- 构造 unsorted bin + tcache + fastbin

**核心技术**：
- glibc 2.27 1.6 tcache双链表
- IO结构体伪造 _flags=0xfbad1800
- _IO_write_base 改堆地址泄露
- fastbin reverse into tcache 写堆地址
- UAF + 堆重叠

**质量评估**：高（2.27-1.6最新特性 + 完整思路分析）
