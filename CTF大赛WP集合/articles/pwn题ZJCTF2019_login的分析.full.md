---
title: pwn 题 ZJCTF 2019 login 的分析
contest: ZJCTF
year: 2019
difficulty: hard
vuln_type: pwn_unknown
tags:
- cpp-vtable
- virtual-function
- function-pointer
- two-level-pointer
- asn-stack-overflow
- password-backdoor
- gdb-trace
attack_chain:
- C++ User/Admin 结构体
- 虚函数表 + 虚函数指针
- main 函数 user->read_name 0x49 字节
- 覆盖 password_checker 二级指针
- 写后门函数 0x400e88 地址
- 触发 password 验证流程
- 二级指针调用跳到后门
key_payload: C++ 二级虚函数指针 + 栈平移覆盖
one_liner: ZJCTF 2019 login PWN 复盘，C++ 虚函数表 + 二级指针调用 + 栈子函数复用覆盖。
lesson: '''父子函数栈平移时，子函数栈空间的指针变量可能被父函数新调用破坏。'''
quality: high
full_path: pwn题ZJCTF2019_login的分析.full.md
meta_path: pwn题ZJCTF2019_login的分析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: pwn 题 ZJCTF 2019 login 的分析。ZJCTF 2019 login PWN 复盘，C++ 虚函数表 + 二级指针调用 + 栈子函数复用覆盖。。关键路径：C++ User/Admin 结构体 → 虚函数表 + 虚函数指针 → main 函数 user->read_name 0x49 字节。经验：'父子函数栈平移时，子函数栈空间的指针变量可能被父函数新调用破坏。'
category: pwn
subcategory: pwn_other
tools_used:
- C
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/89970.html
reasoning_chain:
- main 调 read_name 读 0x49 字节到 bss login+1，main 调 password_checker，里面 read_password 读 0x50 字节密码 → 触发点：两个读 + 父子函数栈平行
- 假设：父子函数 ebp 相同，但 esp 不同 → 子函数栈空间会被父函数复用 → 父函数 [rbp-0x18] 处的指针可能被新 read_password 覆盖
- 动作：gdb 单步 password_checker 汇编 → 观察：二级指针 v7 经 v3 调用后，rax=[rbp-0x18] 内地址
- 假设：覆盖 v7 指向的二级指针值 → 动作：read_password 写 '2jctf_pa5sw0rd\x00' + 'a'*0x48 + p64(0x400e88)
- 观察：v7[0] 被覆盖为 0x400e88 后门地址 → 下一步：触发 password_checker 调用 v7() → 跳到后门
- '动作：io.sendlineafter(''username: '',''admin'')；io.sendafter(''password'',payload) → 观察：执行后门 getshell'
failed_attempts:
- 试图用 gets + ROP → 失败：有 canary 保护
- 试图覆盖 magic 变量触发隐藏菜单 → 失败：magic 未初始化路径不可控
- 试图直接覆盖返回地址到 system → 失败：函数末尾有 canary 校验
key_observations:
- 父子函数栈平行时，子函数栈空间可能承载父函数的指针变量，新 read 操作可破坏该指针
- C++ 二级虚函数指针调用：先 std::cout 打印再解引用，gdb follow step 才能看清 rax 链路
- read 接受 0x49 字节 > 用户名 0x50 上限但 < 密码 0x50 → 借 password 函数读窗口溢出更合适
- vtable/二级指针攻击：先看 vtable 是否可写，再看 vtable 内函数指针能否被二级指针间接调用
prerequisites:
- x86_64 函数栈帧（push rbp / sub rsp / leave; ret）
- C++ 虚函数表与二级指针调用
- GDB 多函数调用栈跟踪与 rax 链路追踪
- Pwntools 远程/本地 pwn 基本用法
---
# pwn题ZJCTF2019 login的分析

> 原文: https://www.ctfiot.com/89970.html
> ID: 89970

由于对汇编了解甚少，本不复杂的一题让我学到了很多。

文件一开始需要登录，需要用户名和密码。

先checksec，存在canary。

主函数如下，一眼可以得到密码，下面会慢慢分析。

首先是16行的Admin的构造函数，调用了User的构造函数。

User构建的结构体，包含0x401170处的get_password函数的指针，传入的用户名与密码，它们的上限大小都是0x50。

Admin结构体与User的区别在于指针改为了0x401150，但还是get_password指针。

感觉这个Admin结构体意义不明，但数据结构的构思和我们关系不大就是了
后续可能存在函数指针的利用。

接着看主函数25行的User::
read_name，读取输入的0x49个字符，然后赋值给bss段的login+1处，login是一个全局User结构体，实现了名字读入。

接着到了本题的重点，指针v3(实际只被寄存器暂存)存储函数指针main::{lambda(void)#1}::
operator,然后经过password_checker得到二级指针v7。

查看password_checker,3*8的数组v2中，在v2处存储了a1(主函数的v3）指针。

看汇编语言更为直观，rax存储了[rbp-0x18]处的地址。

接着是read_password函数，与read_name函数基本一致。

get_password函数很简单。

在看最后的password_checker()前，我们用正确密码测试文件，显示段错误。

查看password_checker,login与admin的密码比较后，来了个奇葩的有毒打印，接着前面的二级函数终于被调用了。

我们需要知道报错原因，gdb调试发现正好是二级指针调用出错。

此外题目中有现成后门。

因此这题的漏洞基本算是送到脸上了，但对汇编不了解的我硬是做了两天。

经过上面的初步分析，我们知道程序在password_checker中调用一个二级指针失败而段错误终止，考虑到canary的存在，srop不可能短期实现。即使我们无法利用这个二级指针getshell，它的存在也会让程序终止。由于存在后门函数，只要能改变这个二级指针，这题就getshell了。

在网上多位师傅博客的参考下，我学会了用汇编溯源的技巧。c语言代码虽然易懂，但最硬核与直接的还是汇编。

调试前我们要明白一个概念：对于一个函数内调用的函数，他们的栈是平行的：由于push rbp; mov rbp, rsp;sub rsp, x子函数的ebp相同，esp根据位移不同而不同。

因此，子函数的栈空间会存在反复利用的情况；如果父函数中出现了子函数栈空间的指针变量，下一次调用子函数时，这个指针变量指向的值就有可能改变！

回到调试，我们观察main函数的汇编，指针存于[rbp-0x130]，它来自于password_checker的rax。

此处与我们初步调试的结果相同，rax的来源是[rbp-0x18]的地址（我原来不明白lea的意思……想了很久）。在最终二级指针调用时，会获得rbp-0x18的值，再获得[rbp-0x18]内的地址。我们可以覆盖后面子函数中[rbp-0x18]的值。

from pwn import *context.log_level = 'debug' io = process('./login')#io = remote('node4.buuoj.cn',25895)#pause()#gdb.attach(io, 'b *0x400b42') io.sendlineafter('username: ', 'admin')payload = b'2jctf_pa5sw0rdx00'.ljust(0x48, b'x61') + p64(0x400e88)io.sendafter('password', payload)io.interactive()

看雪ID：N1co5in3

https://bbs.pediy.com/user-home-945391.htm

*本文由看雪论坛 N1co5in3 原创，转载请注明来自看雪社区

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
from pwn import *context.log_level = 'debug' io = process('./login')#io = remote('node4.buuoj.cn',25895)#pause()#gdb.attach(io, 'b *0x400b42') io.sendlineafter('username: ', 'admin')payload = b'2jctf_pa5sw0rdx00'.ljust(0x48, b'x61') + p64(0x400e88)io.sendafter('password', payload)io.interactive()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]