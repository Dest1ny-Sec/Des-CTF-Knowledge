# 强网杯2024 ez_vm 手撕VM + DFA Attack Whitebox AES

> 原文: https://www.ctfiot.com/221672.html
> ID: 221672

一

题目思路

二

题目背景

chal.exe 3766323862633565396633663134393532356365646630626636363036636630
:)

三

剖析bytecode格式

switch ( (char)_RAX )
 {
 case 0:
 __asm { tzcnt eax, ebx; jumptable 000000014009A7F8 case 0 }
 v86 = _RAX;
 switch ( v86 )
 {
 case 0LL:
 v87 = *(unsigned __int8 *)v10;
 v88 = a1;
 goto LABEL_260;
 case 1LL:
 v87 = *(_WORD *)v10;
 v88 = a1;
LABEL_260:
 push_16(v88, v87);
 break;
 case 2LL:
 push_32(a1, *v10);
 break;
 case 3LL:
 push_64(a1, *(_QWORD *)v10);
 break;
 case 4LL:
 JUMPOUT(0x14009A190LL);
 }

__int64 __fastcall sub_14009A6B0(__int64 a1, __int16 a2)
{
 __int64 result; // rax

 result = *(_QWORD *)(a1 + 8); // vrsp
 if ( result == *(_QWORD *)(a1 + 536) )
 BUG();
 *(_QWORD *)(a1 + 8) = result - 2;
 *(_WORD *)(result - 2) = a2; 
 return result;
}

00 08 20 00 00 00 00 00 00 00

四

handler逆向

mov reg, imm

case 1:
 v89 = (__int16 *)pop_64(a1);
 __asm { tzcnt ecx, ebx }
 v91 = _RCX;
 switch ( v91 )
 {
 case 0LL:
 v13 = *(unsigned __int8 *)v89;
 goto LABEL_5;
 case 1LL:
 v13 = *v89;
 v8 = a1;
 goto LABEL_6;
 case 2LL:
 v58 = *(_DWORD *)v89;
 goto LABEL_289;
 case 3LL:
 v138 = *(_QWORD *)v89;
 goto LABEL_317;
 }

mov reg, [reg]

case 5:
 _RAX = (_QWORD *)pop_64(a1);
 v75 = _RAX;
 if ( (_DWORD)_RBX == 4 )
 {
 *_RAX = (unsigned int)pop_32(a1);
 }
 else
 {
 __asm { tzcnt eax, ebx }
 v130 = _RAX;
 switch ( (unsigned __int64)v130 )
 {
 case 0uLL:
LABEL_155:
 *v75 = pop_16(a1);
 break;
 case 1uLL:
LABEL_158:
 *(_WORD *)v75 = pop_16(a1);
 break;
 case 2uLL:
LABEL_156:
 *(_DWORD *)v75 = pop_32(a1);
 break;
 case 3uLL:
LABEL_157:
 *(_QWORD *)v75 = pop_64(a1);
 break;
 }
 }

mov [reg],reg

case 7:
 __asm { tzcnt eax, ebx; jumptable 000000014009A7F8 case 7 }
 v77 = _RAX;
 switch ( v77 )
 {
 case 0LL:
 v78 = pop_16(a1);
 v79 = pop_16(a1);
 v80 = v79 + v78;
 v81 = *(_QWORD *)(a1 + 0x210) & 0x3F77D7LL;
 if ( v79 < 0 )
 {
 if ( v80 < 0 || v78 >= 0 )
 goto LABEL_103;
 }
 else if ( v80 >= 0 || v78 < 0 )
 {
LABEL_103:
 v82 = v81 & 0x3F7F17;
 v83 = v81 | 0x80; //SF
 if ( v80 >= 0 )
 v83 = v82;
 v84 = v83 & 0x3F7F92;
 v85 = v83 | 0x40;// ZF
 if ( v80 )
 v85 = v84;
 *(_QWORD *)(a1 + 0x210) = v85 & 0x3F7FD2 | (unsigned __int64)(unsigned __int8)((4 * !__SETP__(v80, 0)) | ((unsigned __int8)v80 < (unsigned __int8)v79));//PF
 v13 = (unsigned __int8)v80;
 goto LABEL_5;
 }
 LODWORD(v81) = v81 | 0x800; //OF
 goto LABEL_103;
 case 1LL:
 //.....

add reg, reg

case 18:
 __asm { tzcnt eax, ebx; jumptable 000000014009A7F8 case 18 }
 v102 = _RAX;
 switch ( v102 )
 {
 case 0LL:
 v103 = pop_16(a1);
 v104 = pop_16(a1);
 v105 = v104 - v103;
 v106 = *(_QWORD *)(a1 + 528) & 0x3F77D7LL;
 if ( v104 >= 0 )
 {
 if ( v105 >= 0 || v103 < 0 )
 goto LABEL_134;
LABEL_133:
 LODWORD(v106) = v106 | 0x800;
 goto LABEL_134;
 }
 if ( v105 >= 0 && v103 < 0 )
 goto LABEL_133;
LABEL_134:
 v107 = v106 & 0x3F7F17 | v105 & 0x80;
 v108 = v107 + 64;
 if ( v104 != v103 )
 v108 = v107;
 *(_QWORD *)(a1 + 528) = v108 & 0x3F7FD2 | (unsigned __int64)(unsigned __int8)(((unsigned __int8)v104 < (unsigned __int8)v103) | (4 * !__SETP__(v104, v103)));
 goto LABEL_7;
 case 1LL:
 //.....

cmp reg，reg

case 21:
 v224 = *(_QWORD *)(a1 + 0x210);
 switch ( *(_BYTE *)v11 )
 {
 case 0:
 goto ture_jmp; // jmp
 case 1:
 goto LABEL_370;
 case 2:
 goto LABEL_363;
 case 3:
 if ( (v224 & 0x40) == 0 && (v224 & 1) == 0 )// ja
 goto false_jmp; // jbe
 goto ture_jmp;
 case 4:
 if ( (v224 & 0x40) != 0 || (((unsigned __int8)v224 ^ 1) & 1) == 0 )// jbe
 goto false_jmp; // ja
 goto ture_jmp;
 case 5:
 if ( (((unsigned __int8)v224 ^ 1) & 1) == 0 )// jb
 goto false_jmp; // jae
 goto ture_jmp;
 case 6:
 if ( ((v224 & 0x80u) != 0LL) != ((v224 & 0x800) != 0) )// jl
 goto ture_jmp; // jge
 goto LABEL_370;
 case 7:
 if ( ((v224 & 0x80u) != 0LL) != ((v224 & 0x800) == 0) )// jg
 goto LABEL_363; // jle
 goto false_jmp;
 case 8:
 if ( ((v224 & 0x80u) != 0LL) != ((v224 & 0x800) == 0) )// jg
 goto ture_jmp;
LABEL_370:
 if ( (v224 & 0x40) != 0 ) // jz
 goto ture_jmp; // jnz
 goto false_jmp;
 case 9:
 if ( ((v224 & 0x80u) != 0LL) == ((v224 & 0x800) != 0) )
 goto false_jmp;
LABEL_363:
 if ( (v224 & 0x40) != 0 ) // jz
false_jmp:
 *(_QWORD *)a1 = v4 + 11;
 else
ture_jmp:
 *(_QWORD *)a1 = &v4[-*(_QWORD *)(v4 + 3)];
 break;
 default:
 goto LABEL_418;
 }

ture_jmp:
 *(_QWORD *)a1 = &v4[-*(_QWORD *)(v4 + 3)];
false_jmp:
 *(_QWORD *)a1 = v4 + 11;（next bytecode）

case 27:
 v15 = (unsigned __int8)v4[2];
 v16 = v4 + 3;
 *(_QWORD *)a1 = v16;
 v2 = 0LL;
 memset(v443, 0, sizeof(v443));
 v444 = 0LL;
 v17 = 0LL;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0x9000000101uLL, 0);
 LOBYTE(v18) = 1;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0xA000000101uLL, v18);
 LOBYTE(v19) = 2;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0xB000000101uLL, v19);
 LOBYTE(v20) = 3;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0xC000000101uLL, v20);
 LOBYTE(v21) = 4;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0xD000000101uLL, v21);
 LOBYTE(v22) = 5;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0xE000000101uLL, v22);
 LOBYTE(v23) = 6;
 // ....

1B 08 03 C1 E1 02

case 27:
 v15 = (unsigned __int8)v4[2];// v15 = 3
 v16 = v4 + 3; // v16 -〉c1 e1 02

memcpy_1(v87 + *(_QWORD *)(a1 + 0x230), v16, v15);

case 28:
 return a1;

五

虚拟机parser编写

from capstone import *

md = Cs(CS_ARCH_X86, CS_MODE_64)

with open('chal.exe','rb') as f:
 vm_opcode = f.read()[0x97200:0x97200+0x15b8c]

print(vm_opcode[:16])

pc_max = len(vm_opcode)
pc = 0
reg_index = -1

def get_reg():
 reg_name = [
 # 'rax', used
 # 'rbx',
 # 'rcx',
 # 'rdx',
 'rdi',
 'rsi',
 # 'rsp',
 'rbp',
 'r8',
 'r9',
 'r10',
 'r11',
 'r12',
 'r13',
 'r14',
 'r15',
 ]
 assert reg_index >= 0 , "reg_index_error"
 assert reg_index < len(reg_name) , "reg_index_error"
 return reg_name[reg_index]

def get_reg_size():
 reg_name_size = [
 # ['al','ax','eax','rax'], used
 # ['bl','bx','ebx','rbx'],
 # ['cl','cx','ecx','rcx'],
 # ['dl','dx','edx','rdx'],
 ['dil','di','edi','rdi'],
 ['sil','si','esi','rsi'],
 # ['spl','sp','esp','rsp'],
 ['bpl','bp','ebp','rbp'],
 ['r8b','r8w','r8d','r8'],
 ['r9b','r9w','r9d','r9'],
 ['r10b','r10w','r10d','r10'],
 ['r11b','r11w','r11d','r11'],
 ['r12b','r12w','r12d','r12'],
 ['r13b','r13w','r13d','r13'],
 ['r14b','r14w','r14d','r14'],
 ['r15b','r15w','r15d','r15'],
 ]
 assert reg_index >= 0 , "reg_index_error"
 assert reg_index < len(reg_name_size) , "reg_index_error"
 return reg_name_size[reg_index][opsize.bit_length()-1]

opsize_arr = [1,2,4,8]
x64_asm = []
need_label = set()
pc_infor = []

while pc < pc_max:
 opcode = vm_opcode[pc]
 opsize = vm_opcode[pc+1]
 pc_infor.append(pc)
 x64_asm.append(f'lable_{hex(pc)}:')
 assert opsize in opsize_arr, "opsize error"
 if opcode == 0:
 imm = int.from_bytes(vm_opcode[pc+2:pc+2+opsize],'little')
 if opsize == 1:
 print(f"push16 {imm}")
 if opsize == 2:
 print(f"push16 {imm}")
 if opsize == 4:
 print(f"push32 {imm}")
 if opsize == 8:
 print(f"push64 {imm}")
 pc += 2+opsize
 reg_index += 1
 dst_reg = get_reg()
 asm = f'mov %s, {imm}' % (dst_reg)
 x64_asm.append(asm)

 elif opcode == 1:
 if opsize == 1:
 print(f"load16")
 if opsize == 2:
 print(f"load16")
 if opsize == 4:
 print(f"load32")
 if opsize == 8:
 print(f"load64")
 pc += 2
 src_reg = get_reg()
 dst_reg = get_reg_size()
 asm = 'mov %s, [%s]' % (dst_reg, src_reg)
 if opsize < 4: #not support 32->64
 asm += 'nmovzx %s, %s' % (src_reg, dst_reg)
 x64_asm.append(asm)

 elif opcode == 2:
 print(f"{opcode} not impl")
 break

 elif opcode == 3:
 if opsize == 1:
 print(f"store16")
 if opsize == 2:
 print(f"store16")
 if opsize == 4:
 print(f"store32")
 if opsize == 8:
 print(f"store64")
 pc += 2
 dst_reg = get_reg()
 reg_index -= 1
 src_reg = get_reg_size()
 reg_index -= 1 
 asm = "mov [%s], %s" % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 4:
 print(f"{opcode} not impl")
 break

 elif opcode == 5:
 if opsize == 1:
 print(f"store8")
 if opsize == 2:
 print(f"store16")
 if opsize == 4:
 print(f"store32u")
 if opsize == 8:
 print(f"store64")
 pc += 2
 dst_reg = get_reg()
 reg_index -= 1
 src_reg = get_reg_size()
 reg_index -= 1 
 asm = "mov [%s], %s" % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 6:
 if opsize == 1:
 print(f"store8")
 if opsize == 2:
 print(f"store16")
 pc += 2
 dst_reg = get_reg()
 reg_index -= 1
 src_reg = get_reg_size()
 reg_index -= 1 
 asm = "mov [%s], %s" % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 7:
 if opsize == 1:
 print(f"add16")
 if opsize == 2:
 print(f"add16")
 if opsize == 4:
 print(f"add32")
 if opsize == 8:
 print(f"add64")
 pc += 2
 src_reg = get_reg_size()
 reg_index -= 1
 dst_reg = get_reg_size()
 asm = 'add %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)
 

 elif opcode == 8:
 if opsize == 1:
 print(f"sub16")
 if opsize == 2:
 print(f"sub16")
 if opsize == 4:
 print(f"sub32")
 if opsize == 8:
 print(f"sub64")
 pc += 2
 src_reg = get_reg_size()
 reg_index -= 1
 dst_reg = get_reg_size()
 asm = 'sub %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 9 or opcode == 0xa:
 print(f"{opcode} not impl")
 break

 elif opcode == 0x0b:
 if opsize == 1:
 print(f"div16")
 if opsize == 2:
 print(f"div16")
 if opsize == 4:
 print(f"div32")
 if opsize == 8:
 print(f"div64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'xor rdx, rdx'
 asm += 'nmov rax, %s' % dst_reg
 asm += 'nmov rcx, %s' % src_reg
 asm += 'ndiv rcx'
 asm += 'nmov %s, rax'% dst_reg 
 x64_asm.append(asm)

 elif opcode == 0x0c:
 print(f"{opcode} not impl")
 break

 elif opcode == 0x0d:
 if opsize == 1:
 print(f"imul16")
 if opsize == 2:
 print(f"imul16")
 if opsize == 4:
 print(f"imul32")
 if opsize == 8:
 print(f"imul64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'imul %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x0e:
 if opsize == 1:
 print(f"and16")
 if opsize == 2:
 print(f"and16")
 if opsize == 4:
 print(f"and32")
 if opsize == 8:
 print(f"and64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'and %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x0f:
 if opsize == 1:
 print(f"or16")
 if opsize == 2:
 print(f"or16")
 if opsize == 4:
 print(f"or32")
 if opsize == 8:
 print(f"or64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'or %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x10:
 if opsize == 1:
 print(f"xor16")
 if opsize == 2:
 print(f"xor16")
 if opsize == 4:
 print(f"xor32")
 if opsize == 8:
 print(f"xor64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'xor %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x11:
 if opsize == 1:
 print(f"~16")
 if opsize == 2:
 print(f"~16")
 if opsize == 4:
 print(f"~32")
 if opsize == 8:
 print(f"~64")
 pc += 2
 src_reg = get_reg()
 asm = 'not %s' % (src_reg)
 x64_asm.append(asm)

 elif opcode == 0x12:
 if opsize == 1:
 print(f"CMP16")
 if opsize == 2:
 print(f"CMP16")
 if opsize == 4:
 print(f"CMP32")
 if opsize == 8:
 print(f"CMP64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 reg_index -= 1
 asm = 'cmp %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x13 | opcode == 0x14:
 print(f"{opcode} not impl")
 break

 elif opcode == 0x15:
 jmp_condition = vm_opcode[pc+2]
 offset = int.from_bytes(vm_opcode[pc+3:pc+3+8],'little')
 jmp_pc = pc - offset & 2**64 - 1
 target = hex(jmp_pc)
 lable = "lable_%s" % target
 if jmp_condition == 0:
 print("jmp")
 asm = f'jmp {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 1:
 print("jz")
 asm = f'jz {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 2:
 print("jnz")
 asm = f'jnz {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 3:
 print("jbe")
 asm = f'jbe {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 4:
 print("ja")
 asm = f'ja {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 5:
 print("jae")
 asm = f'jae {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 6:
 print("jle")
 asm = f'jle {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 7:
 print("jg")
 asm = f'jg {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 8:
 print("jg") 
 asm = f'jg {lable}'
 need_label.add(jmp_pc) 
 pc += 11
 x64_asm.append(asm)

 elif opcode == 0x16:
 print("pushVM")
 reg_index += 1
 dst_reg = get_reg()
 asm = "mov %s ,rbx" % dst_reg
 pc += 2 
 x64_asm.append(asm)

 elif opcode == 0x17:
 print("add64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'add %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x18:
 print("imul64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'imul %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x19:
 print("sub64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'sub %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x1a:
 base = hex(int.from_bytes(vm_opcode[pc+2:pc+2+opsize],'little'))
 print(f"rebase {base}")
 pc += 2 + opsize
 x64_asm.append('nop')

 elif opcode == 0x1b:
 shellcode_len = vm_opcode[pc+2]
 print("JIT")
 print(f"shellcode {shellcode_len}")
 shellcode_byte = vm_opcode[pc+3:pc+3+shellcode_len]
 asm = f'JIT_{pc}:n'
 for i in md.disasm(shellcode_byte,0):
 asm += f"{i.mnemonic} {i.op_str}n"
 print(asm)
 pc += 3 + shellcode_len
 x64_asm.append(asm)

 elif opcode == 0x1c:
 print('return')
 asm = 'mov rax, rbxnret'
 x64_asm.append(asm)
 break

with open("parse.s",'w') as f:
 f.write('''
.intel_syntax noprefix
.code64
.section .text
 .global _start
_start:
''')
 f.write('mov rbx, rcxn')
 # for index,asm in enumerate(x64_asm):
 # # if pc_infor[index] in need_label:
 # lable = 'lable_' + hex(pc_infor[index])+":"
 # f.write(lable)
 f.write('n'.join(x64_asm))

六

初探witheBox 逆向

VmContext *__fastcall start(VmContext *a1)
{
 *((_QWORD *)a1->rsp + 2) = a1->rdx;
 *((_QWORD *)a1->rsp + 1) = a1->rcx;
 a1->rsp = (char *)a1->rsp - 8;
 *(_QWORD *)a1->rsp = a1->rbp;
 a1->rsp = (char *)a1->rsp - 192;
 a1->rbp = (char *)a1->rsp + 32;
 a1->rcx = (void *)0x140097017LL;
 ((void (*)(void))((char *)NtCurrentPeb()->ImageBaseAddress + 12048))();
 //shiftRow tables
 *((_BYTE *)a1->rbp + 16) = 0;
 *((_BYTE *)a1->rbp + 17) = 5;
 *((_BYTE *)a1->rbp + 18) = 10;
 *((_BYTE *)a1->rbp + 19) = 15;
 *((_BYTE *)a1->rbp + 20) = 4;
 *((_BYTE *)a1->rbp + 21) = 9;
 *((_BYTE *)a1->rbp + 22) = 14;
 *((_BYTE *)a1->rbp + 23) = 3;
 *((_BYTE *)a1->rbp + 24) = 8;
 *((_BYTE *)a1->rbp + 25) = 13;
 *((_BYTE *)a1->rbp + 26) = 2;
 *((_BYTE *)a1->rbp + 27) = 7;
 *((_BYTE *)a1->rbp + 28) = 12;
 *((_BYTE *)a1->rbp + 29) = 1;
 *((_BYTE *)a1->rbp + 30) = 6;
 *((_BYTE *)a1->rbp + 31) = 11;
 for ( *((_DWORD *)a1->rbp + 16) = 0; *((unsigned int *)a1->rbp + 16) < 9uLL; *((_DWORD *)a1->rbp + 16) = a1->rax )
 {
 //shift_rows
 for ( *((_DWORD *)a1->rbp + 17) = 0; *((unsigned int *)a1->rbp + 17) < 0x10uLL; *((_DWORD *)a1->rbp + 17) = a1->rax )
 {
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 17);
 LOBYTE(a1->rax) = *((_BYTE *)a1->rax + (unsigned __int64)a1->rbp + 16);
 LODWORD(a1->rcx) = *((_DWORD *)a1->rbp + 17);
 a1->rdx = (void *)*((_QWORD *)a1->rbp + 22);
 LOBYTE(a1->rax) = *((_BYTE *)a1->rax + (unsigned __int64)a1->rdx);
 *((_BYTE *)a1->rcx + (unsigned __int64)a1->rbp) = a1->rax;
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 17);
 ++LODWORD(a1->rax);
 // tmp[i] = state[order[i]]
 }
 for ( *((_DWORD *)a1->rbp + 18) = 0; *((unsigned int *)a1->rbp + 18) < 0x10uLL; *((_DWORD *)a1->rbp + 18) = a1->rax )
 {
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 18);
 LODWORD(a1->rcx) = *((_DWORD *)a1->rbp + 18);
 a1->rdx = (void *)*((_QWORD *)a1->rbp + 22);
 LOBYTE(a1->rax) = *((_BYTE *)a1->rax + (unsigned __int64)a1->rbp);
 *((_BYTE *)a1->rcx + (unsigned __int64)a1->rdx) = a1->rax;
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 18);
 ++LODWORD(a1->rax);
 //state[i] = tmp[i]
 }
 for ( *((_DWORD *)a1->rbp + 19) = 0; *((unsigned int *)a1->rbp + 19) < 4uLL; *((_DWORD *)a1->rbp + 19) = a1->rax )
 {
 //too long to show
 }
 }
 //memcpy
 for ( *((_DWORD *)a1->rbp + 23) = 0; *((unsigned int *)a1->rbp + 23) < 0x10uLL; *((_DWORD *)a1->rbp + 23) = a1->rax )
 {
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 23);
 LODWORD(a1->rcx) = *((_DWORD *)a1->rbp + 23);
 a1->rdx = (void *)*((_QWORD *)a1->rbp + 23);
 a1->r8 = (void *)*((_QWORD *)a1->rbp + 22);
 LOBYTE(a1->rax) = *((_BYTE *)a1->rax + (unsigned __int64)a1->r8);
 *((_BYTE *)a1->rcx + (unsigned __int64)a1->rdx) = a1->rax;
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 23);
 ++LODWORD(a1->rax);
 }
 a1->rsp = (char *)a1->rbp + 160;
 a1->rbp = *(void **)a1->rsp;
 a1->rsp = (char *)a1->rsp + 8;
 return a1;
}

八

DFA攻击

a1->rdx = (void *)*((_QWORD *)a1->rbp + 22); // state[] = a1->rbp + 22

lable_0x7ed:
mov rdi, [rdi]

rdi == 0x00007FF68C2DE7ed

lable_0x427:
cmp rdi, rsi

rdi == 0x00007FF68C2DE427

212717A58241E17212C9926E0D67F45C
232717A58241E1A312C9956E0DFBF45C // 1 8 11 14 
E92717A58241E18C12C9F76E0D69F45C
212717EE82412C7212FA926E9C67F45C // 4 7 10 13 
212717898241DC721220926E1D67F45C
212721A582CEE1722FC9926E0D67F422 // 3 6 9 16
212772A5823CE1727FC9926E0D67F484
21BA17A57241E17212C992350D67A05C // 2 5 12 15 
21FB17A53A41E17212C992A00D67C65C

import phoenixAES

data = """212717A58241E17212C9926E0D67F45C
232717A58241E1A312C9956E0DFBF45C
E92717A58241E18C12C9F76E0D69F45C
212717EE82412C7212FA926E9C67F45C
212717898241DC721220926E1D67F45C
212721A582CEE1722FC9926E0D67F422
212772A5823CE1727FC9926E0D67F484
21BA17A57241E17212C992350D67A05C
21FB17A53A41E17212C992A00D67C65C
"""

with open('crackfile','wb') as fp:
 fp.write(data.encode('utf-8'))

phoenixAES.crack_file('crackfile',[],True,False,verbose=3)
#Last round key #N found:
#BF2256727EF09577C7F720C7D84D697A

from aeskeyschedule import *
base_key = reverse_key_schedule(bytes.fromhex('BF2256727EF09577C7F720C7D84D697A'),10)
print(base_key)
# b'welcometoqwb2024'

九

AES 解密

from Crypto.Cipher import AES

enc = bytes.fromhex('C40CC020FC48F6D26CD2FC2B5CA72E6541FE0E64056ED59CCC411D10BEA0F509')

key = b'welcometoqwb2024'

aes = AES.new(key=key,mode=AES.MODE_ECB)

flag = int.from_bytes(aes.decrypt(enc),'big')

print(hex(flag)[2:])
# print(aes.decrypt(enc))
#3766323862633565396633663134393532356365646630626636363036636630

看雪ID：SleepAlone

https://bbs.kanxue.com/user-home-950548.htm

*本文为看雪论坛优秀文章，由 SleepAlone 原创，转载请注明来自看雪社区

# 往期推荐

1、Frida 逆向一个 APP

2、强网杯S8 Rust Pwn chat-with-me出题思路分享

3、浅析libc2.38版本及以前tcache安全机制演进过程与绕过手法

4、购物APP设备风控SDK-mtop简单分析

5、PWN入门：偷吃特权-SetUID

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
题目思路
```



```
二
题目背景
```



```
chal.exe 3766323862633565396633663134393532356365646630626636363036636630
:)
```



```
三
剖析bytecode格式
```



```
switch ( (char)_RAX )
 {
 case 0:
 __asm { tzcnt eax, ebx; jumptable 000000014009A7F8 case 0 }
 v86 = _RAX;
 switch ( v86 )
 {
 case 0LL:
 v87 = *(unsigned __int8 *)v10;
 v88 = a1;
 goto LABEL_260;
 case 1LL:
 v87 = *(_WORD *)v10;
 v88 = a1;
LABEL_260:
 push_16(v88, v87);
 break;
 case 2LL:
 push_32(a1, *v10);
 break;
 case 3LL:
 push_64(a1, *(_QWORD *)v10);
 break;
 case 4LL:
 JUMPOUT(0x14009A190LL);
 }
```



```
__int64 __fastcall sub_14009A6B0(__int64 a1, __int16 a2)
{
 __int64 result; // rax

 result = *(_QWORD *)(a1 + 8); // vrsp
 if ( result == *(_QWORD *)(a1 + 536) )
 BUG();
 *(_QWORD *)(a1 + 8) = result - 2;
 *(_WORD *)(result - 2) = a2; 
 return result;
}
```



```
00 08 20 00 00 00 00 00 00 00
```



```
四
handler逆向
```



```
mov reg, imm
```



```
case 1:
 v89 = (__int16 *)pop_64(a1);
 __asm { tzcnt ecx, ebx }
 v91 = _RCX;
 switch ( v91 )
 {
 case 0LL:
 v13 = *(unsigned __int8 *)v89;
 goto LABEL_5;
 case 1LL:
 v13 = *v89;
 v8 = a1;
 goto LABEL_6;
 case 2LL:
 v58 = *(_DWORD *)v89;
 goto LABEL_289;
 case 3LL:
 v138 = *(_QWORD *)v89;
 goto LABEL_317;
 }
```



```
mov reg, [reg]
```



```
case 5:
 _RAX = (_QWORD *)pop_64(a1);
 v75 = _RAX;
 if ( (_DWORD)_RBX == 4 )
 {
 *_RAX = (unsigned int)pop_32(a1);
 }
 else
 {
 __asm { tzcnt eax, ebx }
 v130 = _RAX;
 switch ( (unsigned __int64)v130 )
 {
 case 0uLL:
LABEL_155:
 *v75 = pop_16(a1);
 break;
 case 1uLL:
LABEL_158:
 *(_WORD *)v75 = pop_16(a1);
 break;
 case 2uLL:
LABEL_156:
 *(_DWORD *)v75 = pop_32(a1);
 break;
 case 3uLL:
LABEL_157:
 *(_QWORD *)v75 = pop_64(a1);
 break;
 }
 }
```



```
mov [reg],reg
```



```
case 7:
 __asm { tzcnt eax, ebx; jumptable 000000014009A7F8 case 7 }
 v77 = _RAX;
 switch ( v77 )
 {
 case 0LL:
 v78 = pop_16(a1);
 v79 = pop_16(a1);
 v80 = v79 + v78;
 v81 = *(_QWORD *)(a1 + 0x210) & 0x3F77D7LL;
 if ( v79 < 0 )
 {
 if ( v80 < 0 || v78 >= 0 )
 goto LABEL_103;
 }
 else if ( v80 >= 0 || v78 < 0 )
 {
LABEL_103:
 v82 = v81 & 0x3F7F17;
 v83 = v81 | 0x80; //SF
 if ( v80 >= 0 )
 v83 = v82;
 v84 = v83 & 0x3F7F92;
 v85 = v83 | 0x40;// ZF
 if ( v80 )
 v85 = v84;
 *(_QWORD *)(a1 + 0x210) = v85 & 0x3F7FD2 | (unsigned __int64)(unsigned __int8)((4 * !__SETP__(v80, 0)) | ((unsigned __int8)v80 < (unsigned __int8)v79));//PF
 v13 = (unsigned __int8)v80;
 goto LABEL_5;
 }
 LODWORD(v81) = v81 | 0x800; //OF
 goto LABEL_103;
 case 1LL:
 //.....
```



```
add reg, reg
```



```
case 18:
 __asm { tzcnt eax, ebx; jumptable 000000014009A7F8 case 18 }
 v102 = _RAX;
 switch ( v102 )
 {
 case 0LL:
 v103 = pop_16(a1);
 v104 = pop_16(a1);
 v105 = v104 - v103;
 v106 = *(_QWORD *)(a1 + 528) & 0x3F77D7LL;
 if ( v104 >= 0 )
 {
 if ( v105 >= 0 || v103 < 0 )
 goto LABEL_134;
LABEL_133:
 LODWORD(v106) = v106 | 0x800;
 goto LABEL_134;
 }
 if ( v105 >= 0 && v103 < 0 )
 goto LABEL_133;
LABEL_134:
 v107 = v106 & 0x3F7F17 | v105 & 0x80;
 v108 = v107 + 64;
 if ( v104 != v103 )
 v108 = v107;
 *(_QWORD *)(a1 + 528) = v108 & 0x3F7FD2 | (unsigned __int64)(unsigned __int8)(((unsigned __int8)v104 < (unsigned __int8)v103) | (4 * !__SETP__(v104, v103)));
 goto LABEL_7;
 case 1LL:
 //.....
```



```
cmp reg，reg
```



```
case 21:
 v224 = *(_QWORD *)(a1 + 0x210);
 switch ( *(_BYTE *)v11 )
 {
 case 0:
 goto ture_jmp; // jmp
 case 1:
 goto LABEL_370;
 case 2:
 goto LABEL_363;
 case 3:
 if ( (v224 & 0x40) == 0 && (v224 & 1) == 0 )// ja
 goto false_jmp; // jbe
 goto ture_jmp;
 case 4:
 if ( (v224 & 0x40) != 0 || (((unsigned __int8)v224 ^ 1) & 1) == 0 )// jbe
 goto false_jmp; // ja
 goto ture_jmp;
 case 5:
 if ( (((unsigned __int8)v224 ^ 1) & 1) == 0 )// jb
 goto false_jmp; // jae
 goto ture_jmp;
 case 6:
 if ( ((v224 & 0x80u) != 0LL) != ((v224 & 0x800) != 0) )// jl
 goto ture_jmp; // jge
 goto LABEL_370;
 case 7:
 if ( ((v224 & 0x80u) != 0LL) != ((v224 & 0x800) == 0) )// jg
 goto LABEL_363; // jle
 goto false_jmp;
 case 8:
 if ( ((v224 & 0x80u) != 0LL) != ((v224 & 0x800) == 0) )// jg
 goto ture_jmp;
LABEL_370:
 if ( (v224 & 0x40) != 0 ) // jz
 goto ture_jmp; // jnz
 goto false_jmp;
 case 9:
 if ( ((v224 & 0x80u) != 0LL) == ((v224 & 0x800) != 0) )
 goto false_jmp;
LABEL_363:
 if ( (v224 & 0x40) != 0 ) // jz
false_jmp:
 *(_QWORD *)a1 = v4 + 11;
 else
ture_jmp:
 *(_QWORD *)a1 = &v4[-*(_QWORD *)(v4 + 3)];
 break;
 default:
 goto LABEL_418;
 }
```



```
ture_jmp:
 *(_QWORD *)a1 = &v4[-*(_QWORD *)(v4 + 3)];
false_jmp:
 *(_QWORD *)a1 = v4 + 11;（next bytecode）
```



```
case 27:
 v15 = (unsigned __int8)v4[2];
 v16 = v4 + 3;
 *(_QWORD *)a1 = v16;
 v2 = 0LL;
 memset(v443, 0, sizeof(v443));
 v444 = 0LL;
 v17 = 0LL;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0x9000000101uLL, 0);
 LOBYTE(v18) = 1;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0xA000000101uLL, v18);
 LOBYTE(v19) = 2;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0xB000000101uLL, v19);
 LOBYTE(v20) = 3;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0xC000000101uLL, v20);
 LOBYTE(v21) = 4;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0xD000000101uLL, v21);
 LOBYTE(v22) = 5;
 sub_7FF68C2DCEF0(v7, byte_7FF68C2DA000, 0xE000000101uLL, v22);
 LOBYTE(v23) = 6;
 // ....
```



```
1B 08 03 C1 E1 02
```



```
case 27:
 v15 = (unsigned __int8)v4[2];// v15 = 3
 v16 = v4 + 3; // v16 -〉c1 e1 02
```



```
memcpy_1(v87 + *(_QWORD *)(a1 + 0x230), v16, v15);
```



```
case 28:
 return a1;
```



```
五
虚拟机parser编写
```



```
from capstone import *

md = Cs(CS_ARCH_X86, CS_MODE_64)

with open('chal.exe','rb') as f:
 vm_opcode = f.read()[0x97200:0x97200+0x15b8c]

print(vm_opcode[:16])

pc_max = len(vm_opcode)
pc = 0
reg_index = -1

def get_reg():
 reg_name = [
 # 'rax', used
 # 'rbx',
 # 'rcx',
 # 'rdx',
 'rdi',
 'rsi',
 # 'rsp',
 'rbp',
 'r8',
 'r9',
 'r10',
 'r11',
 'r12',
 'r13',
 'r14',
 'r15',
 ]
 assert reg_index >= 0 , "reg_index_error"
 assert reg_index < len(reg_name) , "reg_index_error"
 return reg_name[reg_index]

def get_reg_size():
 reg_name_size = [
 # ['al','ax','eax','rax'], used
 # ['bl','bx','ebx','rbx'],
 # ['cl','cx','ecx','rcx'],
 # ['dl','dx','edx','rdx'],
 ['dil','di','edi','rdi'],
 ['sil','si','esi','rsi'],
 # ['spl','sp','esp','rsp'],
 ['bpl','bp','ebp','rbp'],
 ['r8b','r8w','r8d','r8'],
 ['r9b','r9w','r9d','r9'],
 ['r10b','r10w','r10d','r10'],
 ['r11b','r11w','r11d','r11'],
 ['r12b','r12w','r12d','r12'],
 ['r13b','r13w','r13d','r13'],
 ['r14b','r14w','r14d','r14'],
 ['r15b','r15w','r15d','r15'],
 ]
 assert reg_index >= 0 , "reg_index_error"
 assert reg_index < len(reg_name_size) , "reg_index_error"
 return reg_name_size[reg_index][opsize.bit_length()-1]

opsize_arr = [1,2,4,8]
x64_asm = []
need_label = set()
pc_infor = []

while pc < pc_max:
 opcode = vm_opcode[pc]
 opsize = vm_opcode[pc+1]
 pc_infor.append(pc)
 x64_asm.append(f'lable_{hex(pc)}:')
 assert opsize in opsize_arr, "opsize error"
 if opcode == 0:
 imm = int.from_bytes(vm_opcode[pc+2:pc+2+opsize],'little')
 if opsize == 1:
 print(f"push16 {imm}")
 if opsize == 2:
 print(f"push16 {imm}")
 if opsize == 4:
 print(f"push32 {imm}")
 if opsize == 8:
 print(f"push64 {imm}")
 pc += 2+opsize
 reg_index += 1
 dst_reg = get_reg()
 asm = f'mov %s, {imm}' % (dst_reg)
 x64_asm.append(asm)

 elif opcode == 1:
 if opsize == 1:
 print(f"load16")
 if opsize == 2:
 print(f"load16")
 if opsize == 4:
 print(f"load32")
 if opsize == 8:
 print(f"load64")
 pc += 2
 src_reg = get_reg()
 dst_reg = get_reg_size()
 asm = 'mov %s, [%s]' % (dst_reg, src_reg)
 if opsize < 4: #not support 32->64
 asm += 'nmovzx %s, %s' % (src_reg, dst_reg)
 x64_asm.append(asm)

 elif opcode == 2:
 print(f"{opcode} not impl")
 break

 elif opcode == 3:
 if opsize == 1:
 print(f"store16")
 if opsize == 2:
 print(f"store16")
 if opsize == 4:
 print(f"store32")
 if opsize == 8:
 print(f"store64")
 pc += 2
 dst_reg = get_reg()
 reg_index -= 1
 src_reg = get_reg_size()
 reg_index -= 1 
 asm = "mov [%s], %s" % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 4:
 print(f"{opcode} not impl")
 break

 elif opcode == 5:
 if opsize == 1:
 print(f"store8")
 if opsize == 2:
 print(f"store16")
 if opsize == 4:
 print(f"store32u")
 if opsize == 8:
 print(f"store64")
 pc += 2
 dst_reg = get_reg()
 reg_index -= 1
 src_reg = get_reg_size()
 reg_index -= 1 
 asm = "mov [%s], %s" % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 6:
 if opsize == 1:
 print(f"store8")
 if opsize == 2:
 print(f"store16")
 pc += 2
 dst_reg = get_reg()
 reg_index -= 1
 src_reg = get_reg_size()
 reg_index -= 1 
 asm = "mov [%s], %s" % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 7:
 if opsize == 1:
 print(f"add16")
 if opsize == 2:
 print(f"add16")
 if opsize == 4:
 print(f"add32")
 if opsize == 8:
 print(f"add64")
 pc += 2
 src_reg = get_reg_size()
 reg_index -= 1
 dst_reg = get_reg_size()
 asm = 'add %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)
 

 elif opcode == 8:
 if opsize == 1:
 print(f"sub16")
 if opsize == 2:
 print(f"sub16")
 if opsize == 4:
 print(f"sub32")
 if opsize == 8:
 print(f"sub64")
 pc += 2
 src_reg = get_reg_size()
 reg_index -= 1
 dst_reg = get_reg_size()
 asm = 'sub %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 9 or opcode == 0xa:
 print(f"{opcode} not impl")
 break

 elif opcode == 0x0b:
 if opsize == 1:
 print(f"div16")
 if opsize == 2:
 print(f"div16")
 if opsize == 4:
 print(f"div32")
 if opsize == 8:
 print(f"div64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'xor rdx, rdx'
 asm += 'nmov rax, %s' % dst_reg
 asm += 'nmov rcx, %s' % src_reg
 asm += 'ndiv rcx'
 asm += 'nmov %s, rax'% dst_reg 
 x64_asm.append(asm)

 elif opcode == 0x0c:
 print(f"{opcode} not impl")
 break

 elif opcode == 0x0d:
 if opsize == 1:
 print(f"imul16")
 if opsize == 2:
 print(f"imul16")
 if opsize == 4:
 print(f"imul32")
 if opsize == 8:
 print(f"imul64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'imul %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x0e:
 if opsize == 1:
 print(f"and16")
 if opsize == 2:
 print(f"and16")
 if opsize == 4:
 print(f"and32")
 if opsize == 8:
 print(f"and64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'and %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x0f:
 if opsize == 1:
 print(f"or16")
 if opsize == 2:
 print(f"or16")
 if opsize == 4:
 print(f"or32")
 if opsize == 8:
 print(f"or64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'or %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x10:
 if opsize == 1:
 print(f"xor16")
 if opsize == 2:
 print(f"xor16")
 if opsize == 4:
 print(f"xor32")
 if opsize == 8:
 print(f"xor64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'xor %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x11:
 if opsize == 1:
 print(f"~16")
 if opsize == 2:
 print(f"~16")
 if opsize == 4:
 print(f"~32")
 if opsize == 8:
 print(f"~64")
 pc += 2
 src_reg = get_reg()
 asm = 'not %s' % (src_reg)
 x64_asm.append(asm)

 elif opcode == 0x12:
 if opsize == 1:
 print(f"CMP16")
 if opsize == 2:
 print(f"CMP16")
 if opsize == 4:
 print(f"CMP32")
 if opsize == 8:
 print(f"CMP64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 reg_index -= 1
 asm = 'cmp %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x13 | opcode == 0x14:
 print(f"{opcode} not impl")
 break

 elif opcode == 0x15:
 jmp_condition = vm_opcode[pc+2]
 offset = int.from_bytes(vm_opcode[pc+3:pc+3+8],'little')
 jmp_pc = pc - offset & 2**64 - 1
 target = hex(jmp_pc)
 lable = "lable_%s" % target
 if jmp_condition == 0:
 print("jmp")
 asm = f'jmp {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 1:
 print("jz")
 asm = f'jz {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 2:
 print("jnz")
 asm = f'jnz {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 3:
 print("jbe")
 asm = f'jbe {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 4:
 print("ja")
 asm = f'ja {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 5:
 print("jae")
 asm = f'jae {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 6:
 print("jle")
 asm = f'jle {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 7:
 print("jg")
 asm = f'jg {lable}'
 need_label.add(jmp_pc)
 if jmp_condition == 8:
 print("jg") 
 asm = f'jg {lable}'
 need_label.add(jmp_pc) 
 pc += 11
 x64_asm.append(asm)

 elif opcode == 0x16:
 print("pushVM")
 reg_index += 1
 dst_reg = get_reg()
 asm = "mov %s ,rbx" % dst_reg
 pc += 2 
 x64_asm.append(asm)

 elif opcode == 0x17:
 print("add64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'add %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x18:
 print("imul64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'imul %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x19:
 print("sub64")
 pc += 2
 src_reg = get_reg()
 reg_index -= 1
 dst_reg = get_reg()
 asm = 'sub %s, %s' % (dst_reg, src_reg)
 x64_asm.append(asm)

 elif opcode == 0x1a:
 base = hex(int.from_bytes(vm_opcode[pc+2:pc+2+opsize],'little'))
 print(f"rebase {base}")
 pc += 2 + opsize
 x64_asm.append('nop')

 elif opcode == 0x1b:
 shellcode_len = vm_opcode[pc+2]
 print("JIT")
 print(f"shellcode {shellcode_len}")
 shellcode_byte = vm_opcode[pc+3:pc+3+shellcode_len]
 asm = f'JIT_{pc}:n'
 for i in md.disasm(shellcode_byte,0):
 asm += f"{i.mnemonic} {i.op_str}n"
 print(asm)
 pc += 3 + shellcode_len
 x64_asm.append(asm)

 elif opcode == 0x1c:
 print('return')
 asm = 'mov rax, rbxnret'
 x64_asm.append(asm)
 break

with open("parse.s",'w') as f:
 f.write('''
.intel_syntax noprefix
.code64
.section .text
 .global _start
_start:
''')
 f.write('mov rbx, rcxn')
 # for index,asm in enumerate(x64_asm):
 # # if pc_infor[index] in need_label:
 # lable = 'lable_' + hex(pc_infor[index])+":"
 # f.write(lable)
 f.write('n'.join(x64_asm))
```



```
六
初探witheBox 逆向
```



```
VmContext *__fastcall start(VmContext *a1)
{
 *((_QWORD *)a1->rsp + 2) = a1->rdx;
 *((_QWORD *)a1->rsp + 1) = a1->rcx;
 a1->rsp = (char *)a1->rsp - 8;
 *(_QWORD *)a1->rsp = a1->rbp;
 a1->rsp = (char *)a1->rsp - 192;
 a1->rbp = (char *)a1->rsp + 32;
 a1->rcx = (void *)0x140097017LL;
 ((void (*)(void))((char *)NtCurrentPeb()->ImageBaseAddress + 12048))();
 //shiftRow tables
 *((_BYTE *)a1->rbp + 16) = 0;
 *((_BYTE *)a1->rbp + 17) = 5;
 *((_BYTE *)a1->rbp + 18) = 10;
 *((_BYTE *)a1->rbp + 19) = 15;
 *((_BYTE *)a1->rbp + 20) = 4;
 *((_BYTE *)a1->rbp + 21) = 9;
 *((_BYTE *)a1->rbp + 22) = 14;
 *((_BYTE *)a1->rbp + 23) = 3;
 *((_BYTE *)a1->rbp + 24) = 8;
 *((_BYTE *)a1->rbp + 25) = 13;
 *((_BYTE *)a1->rbp + 26) = 2;
 *((_BYTE *)a1->rbp + 27) = 7;
 *((_BYTE *)a1->rbp + 28) = 12;
 *((_BYTE *)a1->rbp + 29) = 1;
 *((_BYTE *)a1->rbp + 30) = 6;
 *((_BYTE *)a1->rbp + 31) = 11;
 for ( *((_DWORD *)a1->rbp + 16) = 0; *((unsigned int *)a1->rbp + 16) < 9uLL; *((_DWORD *)a1->rbp + 16) = a1->rax )
 {
 //shift_rows
 for ( *((_DWORD *)a1->rbp + 17) = 0; *((unsigned int *)a1->rbp + 17) < 0x10uLL; *((_DWORD *)a1->rbp + 17) = a1->rax )
 {
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 17);
 LOBYTE(a1->rax) = *((_BYTE *)a1->rax + (unsigned __int64)a1->rbp + 16);
 LODWORD(a1->rcx) = *((_DWORD *)a1->rbp + 17);
 a1->rdx = (void *)*((_QWORD *)a1->rbp + 22);
 LOBYTE(a1->rax) = *((_BYTE *)a1->rax + (unsigned __int64)a1->rdx);
 *((_BYTE *)a1->rcx + (unsigned __int64)a1->rbp) = a1->rax;
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 17);
 ++LODWORD(a1->rax);
 // tmp[i] = state[order[i]]
 }
 for ( *((_DWORD *)a1->rbp + 18) = 0; *((unsigned int *)a1->rbp + 18) < 0x10uLL; *((_DWORD *)a1->rbp + 18) = a1->rax )
 {
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 18);
 LODWORD(a1->rcx) = *((_DWORD *)a1->rbp + 18);
 a1->rdx = (void *)*((_QWORD *)a1->rbp + 22);
 LOBYTE(a1->rax) = *((_BYTE *)a1->rax + (unsigned __int64)a1->rbp);
 *((_BYTE *)a1->rcx + (unsigned __int64)a1->rdx) = a1->rax;
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 18);
 ++LODWORD(a1->rax);
 //state[i] = tmp[i]
 }
 for ( *((_DWORD *)a1->rbp + 19) = 0; *((unsigned int *)a1->rbp + 19) < 4uLL; *((_DWORD *)a1->rbp + 19) = a1->rax )
 {
 //too long to show
 }
 }
 //memcpy
 for ( *((_DWORD *)a1->rbp + 23) = 0; *((unsigned int *)a1->rbp + 23) < 0x10uLL; *((_DWORD *)a1->rbp + 23) = a1->rax )
 {
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 23);
 LODWORD(a1->rcx) = *((_DWORD *)a1->rbp + 23);
 a1->rdx = (void *)*((_QWORD *)a1->rbp + 23);
 a1->r8 = (void *)*((_QWORD *)a1->rbp + 22);
 LOBYTE(a1->rax) = *((_BYTE *)a1->rax + (unsigned __int64)a1->r8);
 *((_BYTE *)a1->rcx + (unsigned __int64)a1->rdx) = a1->rax;
 LODWORD(a1->rax) = *((_DWORD *)a1->rbp + 23);
 ++LODWORD(a1->rax);
 }
 a1->rsp = (char *)a1->rbp + 160;
 a1->rbp = *(void **)a1->rsp;
 a1->rsp = (char *)a1->rsp + 8;
 return a1;
}
```



```
八
DFA攻击
```



```
a1->rdx = (void *)*((_QWORD *)a1->rbp + 22); // state[] = a1->rbp + 22
```



```
lable_0x7ed:
mov rdi, [rdi]
```



```
rdi == 0x00007FF68C2DE7ed
```



```
lable_0x427:
cmp rdi, rsi
```



```
rdi == 0x00007FF68C2DE427
```



```
212717A58241E17212C9926E0D67F45C
232717A58241E1A312C9956E0DFBF45C // 1 8 11 14 
E92717A58241E18C12C9F76E0D69F45C
212717EE82412C7212FA926E9C67F45C // 4 7 10 13 
212717898241DC721220926E1D67F45C
212721A582CEE1722FC9926E0D67F422 // 3 6 9 16
212772A5823CE1727FC9926E0D67F484
21BA17A57241E17212C992350D67A05C // 2 5 12 15 
21FB17A53A41E17212C992A00D67C65C
```



```
import phoenixAES

data = """212717A58241E17212C9926E0D67F45C
232717A58241E1A312C9956E0DFBF45C
E92717A58241E18C12C9F76E0D69F45C
212717EE82412C7212FA926E9C67F45C
212717898241DC721220926E1D67F45C
212721A582CEE1722FC9926E0D67F422
212772A5823CE1727FC9926E0D67F484
21BA17A57241E17212C992350D67A05C
21FB17A53A41E17212C992A00D67C65C
"""

with open('crackfile','wb') as fp:
 fp.write(data.encode('utf-8'))

phoenixAES.crack_file('crackfile',[],True,False,verbose=3)
#Last round key #N found:
#BF2256727EF09577C7F720C7D84D697A
```



```
from aeskeyschedule import *
base_key = reverse_key_schedule(bytes.fromhex('BF2256727EF09577C7F720C7D84D697A'),10)
print(base_key)
# b'welcometoqwb2024'
```



```
九
AES 解密
```



```
from Crypto.Cipher import AES

enc = bytes.fromhex('C40CC020FC48F6D26CD2FC2B5CA72E6541FE0E64056ED59CCC411D10BEA0F509')

key = b'welcometoqwb2024'

aes = AES.new(key=key,mode=AES.MODE_ECB)

flag = int.from_bytes(aes.decrypt(enc),'big')

print(hex(flag)[2:])
# print(aes.decrypt(enc))
#3766323862633565396633663134393532356365646630626636363036636630
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/3-1735548662.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/0-1735548663.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/7-1735548664.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/3-1735548666.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/1-1735548667.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/12/6-1735548669.gif)