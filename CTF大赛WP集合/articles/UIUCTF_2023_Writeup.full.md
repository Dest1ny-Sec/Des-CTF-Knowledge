---
title: UIUCTF 2023 Writeup
contest: UIUCTF
year: 2023
difficulty: medium
vuln_type: reverse
tags:
- custom-vm
- vmwhere
- stack-vm
- byte-swap-reverse
- xorshift64
- gdb-scripting
- sfcta
attack_chain:
- 'vmwhere1: 自定义 VM，22 个 opcode (ADD/SUB/AND/OR/XOR/SHL/SHR/READ/PUTCHAR/PUSH/JNEG/JZ/JMP/POP/DUP/REVERSE/SPLIT_BIT/POP_BITS/CALL/UNKNOWN/DEBUG)'
- opcode 0xa PUSH imm, 0x8 READ flag byte
- 0x10 REVERSE TOP n 反转栈顶 n 字节
- 0x11 SPLIT BYTE TO 8 BITS, 0x12 POP 8 重组字节
- '24 字节 key XOR 链式: a = k ^ key[i+1]; flag[i] = (a>>4)^a'
- key[::-1] 模式找 pattern `\x05\x0f\x0a` 后字节
- ciuctf{ar3_y0u_4_r3al_vm_wh3r3_(gpt_g3n3r4t3d_th1s_f14g)}
- 'vmwhere2: 更复杂栈机 + 47 字节 key'
- 16 进制字符串 hash ('u', 'i', 'u', 'c', 't', 'f', '{') 调 mini-VM
- '每字节 x 计算 SFCTA: result = 0; for bit in 7..0: if (x>>i)&1: result = (result+1)*3; else: result = result*3'
- 47 个 key 字符通过 table 反查
- 输入 flag 任意字节返回 PUTCHAR 验证
- gdb python gdb.parse_and_eval("$al") 单字符爆破
key_payload: '(a>>4) ^ a  # flag 字符链式 XOR'
one_liner: UIUCTF 2023 vmwhere 2 题：自定义字节码 VM + REVERSE TOP N 反转 + 24/47 字节 key 链式 XOR。
lesson: 自研 VM 逆向时先用 Python 写 interpreter 复现 opcode，再分析 flag 校验逻辑。
quality: high
full_path: UIUCTF_2023_Writeup.full.md
meta_path: UIUCTF_2023_Writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'UIUCTF 2023 Writeup。UIUCTF 2023 vmwhere 2 题：自定义字节码 VM + REVERSE TOP N 反转 + 24/47 字节 key 链式 XOR。。关键路径：vmwhere1: 自定义 VM，22 个 opcode (ADD/SUB/AND/OR/XOR/SHL/SHR/READ/PUTCHAR/PUSH/JNEG/JZ/JMP/POP/DUP/R...'
category: reverse
subcategory: reverse
tools_used:
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/123684.html
reasoning_chain:
- vmwhere1 → IDA 看 check 函数 → 触发点：22 个 opcode 的 stack-VM 解释器
- 假设：自研字节码 VM → 动作：Python 写 interpreter 复现 opcode 0-0x15
- 观察：opcode 0x10 REVERSE TOP N 反转栈顶 N 字节 → 假设：字节顺序被打乱
- 动作：还原 REVERSE 顺序 → 观察：得到线性字节流
- 假设：flag 校验逻辑是 24 字节 key 链式 XOR → 动作：写 a = k ^ key[i+1]; flag[i] = (a>>4) ^ a
- 观察：flag = ciuctf{ar3_y0u_4_r3al_vm_wh3r3_(gpt_g3n3r4t3d_th1s_f14g)}
- vmwhere2 → 47 字节 key 更复杂 → 触发点：每字节走 SFCTA 自定义哈希
- 假设：每字节独立，可 47 次单字节爆破 → 动作：gdb 调 gdb.parse_and_eval("$al") PUTCHAR 反馈
- 观察：47 个 key 字符逐一恢复 → flag 还原
failed_attempts:
- 试图直接分析 0x10 REVERSE 后的字节 → 失败：必须先复现完整 VM 执行
- 试图用 angr 自动化符号执行 vmwhere2 → 失败：路径爆炸太深
key_observations:
- 自研 VM 逆向先写 interpreter 比死磕反编译快
- SFCTA 类自定义哈希 + 单字节 PUTCHAR 反馈 = 可逐字节爆破
- gdb python gdb.parse_and_eval("$al") 是拿寄存器返回值的关键
- REVERSE TOP N 字节反序是字节码 VM 混淆常见手法
prerequisites:
- IDA 反编译 stack-VM 字节码阅读
- Python 自定义 VM interpreter 实现
- gdb python scripting API
---
# UIUCTF 2023 Writeup

> 原文: https://www.ctfiot.com/123684.html
> ID: 123684


```
undefined8 check(byte *param_1,int param_2)

{
 byte *pbVar1;
 byte bVar2;
 byte bVar3;
 int iVar4;
 byte *pbVar5;
 uint local_24;
 byte *local_20;
 byte *local_18;

 pbVar5 = (byte *)malloc(0x1000);
 local_20 = param_1;
 local_18 = pbVar5;
 while( true ) {
 if ((local_20 < param_1) || (param_1 + param_2 <= local_20)) {
 printf("Program terminated unexpectedly. Last instruction: 0x%04lx\n",
 (long)local_20 - (long)param_1);
 return 1;
 }
 pbVar1 = local_20 + 1;
 switch(*local_20) {
 case 0:
 return 0;
 case 1:
 local_18[-2] = local_18[-2] + local_18[-1];
 local_18 = local_18 + -1;
 local_20 = pbVar1;
 break;
 case 2:
 local_18[-2] = local_18[-2] - local_18[-1];
 local_18 = local_18 + -1;
 local_20 = pbVar1;
 break;
 case 3:
 local_18[-2] = local_18[-2] & local_18[-1];
 local_18 = local_18 + -1;
 local_20 = pbVar1;
 break;
 case 4:
 local_18[-2] = local_18[-2] | local_18[-1];
 local_18 = local_18 + -1;
 local_20 = pbVar1;
 break;
 case 5:
 local_18[-2] = local_18[-2] ^ local_18[-1];
 local_18 = local_18 + -1;
 local_20 = pbVar1;
 break;
 case 6:
 local_18[-2] = local_18[-2] << (local_18[-1] & 0x1f);
 local_18 = local_18 + -1;
 local_20 = pbVar1;
 break;
 case 7:
 local_18[-2] = (byte)((int)(uint)local_18[-2] >> (local_18[-1] & 0x1f));
 local_18 = local_18 + -1;
 local_20 = pbVar1;
 break;
 case 8:
 iVar4 = getchar();
 *local_18 = (byte)iVar4;
 local_18 = local_18 + 1;
 local_20 = pbVar1;
 break;
 case 9:
 local_18 = local_18 + -1;
 putchar((uint)*local_18);
 local_20 = pbVar1;
 break;
 case 10:
 *local_18 = *pbVar1;
 local_18 = local_18 + 1;
 local_20 = local_20 + 2;
 break;
 case 0xb:
 if ((char)local_18[-1] < '\0') {
 pbVar1 = pbVar1 + CONCAT11(*pbVar1,local_20[2]);
 }
 local_20 = pbVar1;
 local_20 = local_20 + 2;
 break;
 case 0xc:
 if (local_18[-1] == 0) {
 pbVar1 = pbVar1 + CONCAT11(*pbVar1,local_20[2]);
 }
 local_20 = pbVar1;
 local_20 = local_20 + 2;
 break;
 case 0xd:
 local_20 = pbVar1 + (long)CONCAT11(*pbVar1,local_20[2]) + 2;
 break;
 case 0xe:
 local_18 = local_18 + -1;
 local_20 = pbVar1;
 break;
 case 0xf:
 *local_18 = local_18[-1];
 local_18 = local_18 + 1;
 local_20 = pbVar1;
 break;
 case 0x10:
 local_20 = local_20 + 2;
 bVar2 = *pbVar1;
 if ((long)local_18 - (long)pbVar5 < (long)(ulong)bVar2) {
 printf("Stack underflow in reverse at 0x%04lx\n",(long)local_20 - (long)param_1);
 }
 for (local_24 = 0; (int)local_24 < (int)(uint)(bVar2 >> 1); local_24 = local_24 + 1) {
 bVar3 = local_18[(int)(local_24 - bVar2)];
 local_18[(int)(local_24 - bVar2)] = local_18[(int)~local_24];
 local_18[(int)~local_24] = bVar3;
 }
 break;
 default:
 printf("Unknown opcode: 0x%02x at 0x%04lx\n",(ulong)*local_20,(long)local_20 - (long)param_1);
 return 1;
 case 0x28:
 FUN_00101370(param_1,pbVar5,local_18,(long)pbVar1 - (long)param_1);
 local_20 = pbVar1;
 }
 if (local_18 < pbVar5) break;
 if (pbVar5 + 0x1000 < local_18) {
 printf("Stack overflow at 0x%04lx\n",(long)local_20 - (long)param_1);
 return 1;
 }
 }
 printf("Stack underflow at 0x%04lx\n",(long)local_20 - (long)param_1);
 return 1;
}
# gdb -x solver.py
import gdb
from pprint import pprint

# pprint(dir(gdb))
BINDIR = "/home/ubuntu/Hacking/CTF/2023/UIUCTF/Rev/vmwhere1/"
BIN = "chal"

gdb.execute('file {}/{}'.format(BINDIR, BIN))
# gdb.execute('b *{}'.format(0x555555555587))
gdb.execute('b *{}'.format(0x55555555569f))

flag = "uiuctf{" + "A"*150
for i in range(150):
 for j in range(0x21,0x126):
 flag = flag[:i] + chr(j) + "A"*(30-i)
 with open("in.txt", "w") as f:
 f.write(flag)

 gdb.execute("run program < in.txt")
 gdb.execute("continue {}".format(51+i))
 res = int(gdb.parse_and_eval("$al"))
 if res == 0:
 print(flag)
 print(chr(j),flag)
 break
 else:
 continue

print(flag)
gdb.execute('quit')
void FUN_00101370(undefined8 param_1,long param_2,long param_3,undefined8 param_4)
{
 int local_c;

 param_3 = param_3 + -1;
 printf("Program counter: 0x%04lx\n",param_4);
 printf("Stack pointer: 0x%04lx\n",param_3 - param_2);
 puts("Stack:");
 for (local_c = 0; local_c < 0x10; local_c = local_c + 1) {
 if (-1 < (param_3 - param_2) - (long)local_c) {
 printf("0x%04lx: 0x%04x\n",(param_3 - param_2) - (long)local_c,
 (ulong)*(byte *)(param_3 - local_c));
 }
 }
 return;
}
echo -n -e "\x0a\x21\x0a\x22\x0a\x23\x0a\x24\x28" > test
./chal test
>
Program counter: 0x0009
Stack pointer: 0x0003
Stack:
0x0003: 0x0024
0x0002: 0x0023
0x0001: 0x0022
0x0000: 0x0021
Program terminated unexpectedly. Last instruction: 0x0009
08 0f 0a 04 07 05 05 0f 0a 72 05 0c 00 03 0d 04 0d 0e
op = prog[pic]

if op == 1:
 a = stack.pop()
 b = stack.pop()
 stack.append(a+b)
 pic += 1

if op == 5:
 a = stack.pop()
 b = stack.pop()
 n = a ^ b
 stack.append(n)
 pic += 1

if op == 7:
 a = stack.pop()
 b = stack.pop()
 n = b >> (a & 0x1f)
 stack.append(n)
 pic += 1

if op == 8:
 c = flag[seek]
 seek += 1
 stack.append(c)
 pic += 1

if op == 0xa:
 data = prog[pic+1]
 stack.append(data)
 pic += 2

if op == 0xf:
 stack.append(stack[-1])
 pic += 1
with open("program", "rb") as f:
 prog = f.read()

pattern = b"\x05\x0f\x0a"
key = []
for i in range(3, len(prog)):
 if prog[i-3:i] == pattern:
 key.append(prog[i])

print(key)
with open("program", "rb") as f:
 prog = f.read()

pattern = b"\x05\x0f\x0a"
key = []
for i in range(3, len(prog)):
 if prog[i-3:i] == pattern:
 key.append(prog[i])

# print([hex(i) for i in key])

flag = ""
key = key[::-1]
for i in range(len(key)-1):
 k = key[i]
 a = k ^ key[i+1]
 flag += chr((a>>4)^a)
print("c" + flag[::-1])

# ciuctf{ar3_y0u_4_r3al_vm_wh3r3_(gpt_g3n3r4t3d_th1s_f14g)}
case 0x11:
 local_30 = sp[-1];
 for (j = 0; j < 8; j = j + 1) {
 (sp + -1)[j] = local_30 & 1;
 local_30 = local_30 >> 1;
 }
 sp = sp + 7;
 current_pic = next_pic;
 break;

case 0x12:
 local_2f = 0;
 for (k = 7; -1 < k; k = k + -1) {
 local_2f = local_2f << 1 | (sp + -8)[k] & 1;
 }
 sp[-8] = local_2f;
 sp = sp + -7;
 current_pic = next_pic;
 break;
08 11 0a ff 10 09 10 08 0a 00 10 02 0f 0a ff 05 0c 00 04 0e 0d 00 04 0e 0d 00 16 10 02 10 02 0c 00 07 0e 0a 01 01 0d 00 01 0e 0f 0f 01 01 0d ff d9 0e
08
11
0a ff
10 09
10 08
0a 00
10 02
0f
0a ff
05
0c 00 04
0e
0d 00 04
0e 0d 00 16
10 02
10 02
0c 00 07 0e 0a 01 01 0d 00 01
0e
0f
0f
01
01
0d ff d9
0e
    #include <stdio.h>
    #include <stdlib.h>

void main()
{
 char bVar1;
 char bVar2;
 int iVar3;
 char *stack;
 char local_30;
 char local_2f;
 uint i;
 int j;
 int k;
 char *current_pic;
 char *sp;
 char *next_pic;

 FILE *f;
 void *prog;
 long f_size;

 // Read file
 f = fopen("program","r");
 if (f == (FILE *)0x0) {
 prog = (void *)0x0;
 }
 else {
 fseek(f,0,2);
 f_size = ftell(f);
 rewind(f);
 prog = malloc(f_size);
 if (prog == (void *)0x0) {
 prog = (void *)0x0;
 }
 else {
 fread(prog,1,f_size,f);
 fclose(f);
 }
 }

 // Run program
 stack = (char *)malloc(0x1000);
 current_pic = prog;
 int start = (int)current_pic;
 sp = stack;
 while(1) {
 if ((current_pic < prog) || (prog + f_size <= current_pic)) {
 printf("Program terminated unexpectedly. Last instruction: 0x%04lx\n",
 (long)current_pic - (long)prog);
 return 1;
 }
 printf("[0x%x] OP:0x%x ", current_pic - start, *current_pic);
 next_pic = current_pic + 1;
 switch(*current_pic) {
 case 0:
 return 0;
 case 1:
 printf("ADD %x, %x = %x\n", sp[-2], sp[-1], sp[-2] + sp[-1]);
 sp[-2] = sp[-2] + sp[-1];
 sp = sp + -1;
 current_pic = next_pic;
 break;
 case 2:
 printf("SUB %x, %x = %x\n", sp[-2], sp[-1], sp[-2] - sp[-1]);
 sp[-2] = sp[-2] - sp[-1];
 sp = sp + -1;
 current_pic = next_pic;
 break;
 case 3:
 printf("AND %x, %x = %x\n", sp[-2], sp[-1], sp[-2] & sp[-1]);
 sp[-2] = sp[-2] & sp[-1];
 sp = sp + -1;
 current_pic = next_pic;
 break;
 case 4:
 printf("OR %x, %x = %x\n", sp[-2], sp[-1], sp[-2] | sp[-1]);
 sp[-2] = sp[-2] | sp[-1];
 sp = sp + -1;
 current_pic = next_pic;
 break;
 case 5:
 printf("XOR %x, %x = %x\n", sp[-2], sp[-1], sp[-2] ^ sp[-1]);
 sp[-2] = sp[-2] ^ sp[-1];
 sp = sp + -1;
 current_pic = next_pic;
 break;
 case 6:
 printf("LSH %x, %x = %x\n", sp[-2], (sp[-1] & 0x1f), sp[-2] >> (sp[-1] & 0x1f));
 sp[-2] = sp[-2] << (sp[-1] & 0x1f);
 sp = sp + -1;
 current_pic = next_pic;
 break;
 case 7:
 printf("RSH %x, %x = %x\n", sp[-2], (sp[-1] & 0x1f), sp[-2] << (sp[-1] & 0x1f));
 sp[-2] = (char)((int)(uint)sp[-2] >> (sp[-1] & 0x1f));
 sp = sp + -1;
 current_pic = next_pic;
 break;
 case 8:
 iVar3 = getchar();
 *sp = (char)iVar3;
 printf("READ %c\n", *sp);
 sp = sp + 1;
 current_pic = next_pic;
 break;
 case 9:
 sp = sp + -1;
 printf("PUTCHAR %c\n", *sp);
 // putchar((uint)*sp);
 current_pic = next_pic;
 break;
 case 10:
 printf("PUSH %x\n", *next_pic);
 *sp = *next_pic;
 sp = sp + 1;
 current_pic = current_pic + 2;
 break;
 case 0xb:
 if ((char)sp[-1] < '\0') {
 next_pic = next_pic + (*next_pic << 8 | current_pic[2]);
 }
 current_pic = next_pic;
 current_pic = current_pic + 2;
 printf("JPM %x\n", current_pic);
 break;
 case 0xc:
 if (sp[-1] == 0) {
 next_pic = next_pic + (*next_pic << 8 | current_pic[2]);
 }
 current_pic = next_pic;
 current_pic = current_pic + 2;
 printf("JPM %x\n", current_pic);
 break;
 case 0xd:
 current_pic = next_pic + (*next_pic << 8 | current_pic[2]) + 2;
 printf("JPM %x\n", current_pic);
 break;
 case 0xe:
 printf("POP\n");
 sp = sp + -1;
 current_pic = next_pic;
 break;
 case 0xf:
 printf("DUP %x\n", sp[-1]);
 *sp = sp[-1];
 sp = sp + 1;
 current_pic = next_pic;
 break;
 case 0x10:
 printf("REVERSE TOP %x\n", *next_pic);
 current_pic = current_pic + 2;
 bVar1 = *next_pic;
 if ((long)sp - (long)stack < (long)(ulong)bVar1) {
 printf("Stack underflow in reverse at 0x%04lx\n",(long)current_pic - (long)prog);
 }
 for (i = 0; (int)i < (int)(uint)(bVar1 >> 1); i = i + 1) {
 bVar2 = sp[(int)(i - bVar1)];
 sp[(int)(i - bVar1)] = sp[(int)~i];
 sp[(int)~i] = bVar2;
 }
 break;
 case 0x11:
 printf("SPLIT BYTE TO BITS\n");
 local_30 = sp[-1];
 for (j = 0; j < 8; j = j + 1) {
 (sp + -1)[j] = local_30 & 1;
 local_30 = local_30 >> 1;
 }
 sp = sp + 7;
 current_pic = next_pic;
 break;
 case 0x12:
 printf("POP 8 VALUES, NEW VALUE = LSB OF LAST 8\n");
 local_2f = 0;
 for (k = 7; -1 < k; k = k + -1) {
 local_2f = local_2f << 1 | (sp + -8)[k] & 1;
 }
 sp[-8] = local_2f;
 sp = sp + -7;
 current_pic = next_pic;
 break;
 default:
 printf("Unknown opcode: 0x%02x at 0x%04lx\n",(ulong)*current_pic,
 (long)current_pic - (long)prog);
 return 1;
 }
 if (sp < stack) break;
 if (stack + 0x1000 < sp) {
 printf("Stack overflow at 0x%04lx\n",(long)current_pic - (long)prog);
 return 1;
 }
 }
 printf("Stack underflow at 0x%04lx\n",(long)current_pic - (long)prog);
 return 1;
}
[0x74] OP:
0xa PUSH 0
[0x76] OP:
0x8 READ u
[0x77] OP:
0x11 SPLIT BYTE TO BITS
[0x78] OP:
0xa PUSH ffffffff
[0x7a] OP:
0x10 REVERSE TOP 9
[0x7c] OP:
0x10 REVERSE TOP 8
[0x7e] OP:
0xa PUSH 0
[0x80] OP:
0x10 REVERSE TOP 2
[0x82] OP:
0xf DUP 0
[0x83] OP:
0xa PUSH ffffffff
[0x85] OP:
0x5 XOR 0, ffffffff = ffffffff
[0x86] OP:
0xc JPM f117f519
[0x89] OP:
0xe POP
[0x8a] OP:
0xd JPM f117f521
[0x91] OP:
0x10 REVERSE TOP 2
[0x93] OP:
0x10 REVERSE TOP 2
[0x95] OP:
0xc JPM f117f52f
[0x9f] OP:
0xe POP
[0xa0] OP:
0xf DUP 0
[0xa1] OP:
0xf DUP 0
[0xa2] OP:
0x1 ADD 0, 0 = 0
[0xa3] OP:
0x1 ADD 0, 0 = 0
[0xa4] OP:
0xd JPM f117f510
[0x80] OP:
0x10 REVERSE TOP 2
[0x82] OP:
0xf DUP 1
[0x83] OP:
0xa PUSH ffffffff
[0x85] OP:
0x5 XOR 1, ffffffff = fffffffe
[0x86] OP:
0xc JPM f117f519
[0x89] OP:
0xe POP
[0x8a] OP:
0xd JPM f117f521
[0x91] OP:
0x10 REVERSE TOP 2
[0x93] OP:
0x10 REVERSE TOP 2
[0x95] OP:
0xc JPM f117f528
[0x98] OP:
0xe POP
[0x99] OP:
0xa PUSH 1
[0x9b] OP:
0x1 ADD 0, 1 = 1
[0x9c] OP:
0xd JPM f117f530
[0xa0] OP:
0xf DUP 1
[0xa1] OP:
0xf DUP 1
[0xa2] OP:
0x1 ADD 1, 1 = 2
[0xa3] OP:
0x1 ADD 1, 2 = 3
[0xa4] OP:
0xd JPM f117f510
[0x80] OP:
0x10 REVERSE TOP 2
[0x82] OP:
0xf DUP 1
[0x83] OP:
0xa PUSH ffffffff
[0x85] OP:
0x5 XOR 1, ffffffff = fffffffe
[0x86] OP:
0xc JPM f117f519
[0x89] OP:
0xe POP
[0x8a] OP:
0xd JPM f117f521
[0x91] OP:
0x10 REVERSE TOP 2
[0x93] OP:
0x10 REVERSE TOP 2
[0x95] OP:
0xc JPM f117f528
[0x98] OP:
0xe POP
[0x99] OP:
0xa PUSH 1
[0x9b] OP:
0x1 ADD 3, 1 = 4
[0x9c] OP:
0xd JPM f117f530
[0xa0] OP:
0xf DUP 4
[0xa1] OP:
0xf DUP 4
[0xa2] OP:
0x1 ADD 4, 4 = 8
[0xa3] OP:
0x1 ADD 4, 8 = c
[0xa4] OP:
0xd JPM f117f510
[0x80] OP:
0x10 REVERSE TOP 2
[0x82] OP:
0xf DUP 1
[0x83] OP:
0xa PUSH ffffffff
[0x85] OP:
0x5 XOR 1, ffffffff = fffffffe
[0x86] OP:
0xc JPM f117f519
[0x89] OP:
0xe POP
[0x8a] OP:
0xd JPM f117f521
[0x91] OP:
0x10 REVERSE TOP 2
[0x93] OP:
0x10 REVERSE TOP 2
[0x95] OP:
0xc JPM f117f528
[0x98] OP:
0xe POP
[0x99] OP:
0xa PUSH 1
[0x9b] OP:
0x1 ADD c, 1 = d
[0x9c] OP:
0xd JPM f117f530
[0xa0] OP:
0xf DUP d
[0xa1] OP:
0xf DUP d
[0xa2] OP:
0x1 ADD d, d = 1a
[0xa3] OP:
0x1 ADD d, 1a = 27
[0xa4] OP:
0xd JPM f117f510
[0x80] OP:
0x10 REVERSE TOP 2
[0x82] OP:
0xf DUP 0
[0x83] OP:
0xa PUSH ffffffff
[0x85] OP:
0x5 XOR 0, ffffffff = ffffffff
[0x86] OP:
0xc JPM f117f519
[0x89] OP:
0xe POP
[0x8a] OP:
0xd JPM f117f521
[0x91] OP:
0x10 REVERSE TOP 2
[0x93] OP:
0x10 REVERSE TOP 2
[0x95] OP:
0xc JPM f117f52f
[0x9f] OP:
0xe POP
[0xa0] OP:
0xf DUP 27
[0xa1] OP:
0xf DUP 27
[0xa2] OP:
0x1 ADD 27, 27 = 4e
[0xa3] OP:
0x1 ADD 27, 4e = 75
[0xa4] OP:
0xd JPM f117f510
[0x80] OP:
0x10 REVERSE TOP 2
[0x82] OP:
0xf DUP 1
[0x83] OP:
0xa PUSH ffffffff
[0x85] OP:
0x5 XOR 1, ffffffff = fffffffe
[0x86] OP:
0xc JPM f117f519
[0x89] OP:
0xe POP
[0x8a] OP:
0xd JPM f117f521
[0x91] OP:
0x10 REVERSE TOP 2
[0x93] OP:
0x10 REVERSE TOP 2
[0x95] OP:
0xc JPM f117f528
[0x98] OP:
0xe POP
[0x99] OP:
0xa PUSH 1
[0x9b] OP:
0x1 ADD 75, 1 = 76
[0x9c] OP:
0xd JPM f117f530
[0xa0] OP:
0xf DUP 76
[0xa1] OP:
0xf DUP 76
[0xa2] OP:
0x1 ADD 76, 76 = ec
[0xa3] OP:
0x1 ADD 76, ffffffec = 62
[0xa4] OP:
0xd JPM f117f510
[0x80] OP:
0x10 REVERSE TOP 2
[0x82] OP:
0xf DUP 0
[0x83] OP:
0xa PUSH ffffffff
[0x85] OP:
0x5 XOR 0, ffffffff = ffffffff
[0x86] OP:
0xc JPM f117f519
[0x89] OP:
0xe POP
[0x8a] OP:
0xd JPM f117f521
[0x91] OP:
0x10 REVERSE TOP 2
[0x93] OP:
0x10 REVERSE TOP 2
[0x95] OP:
0xc JPM f117f52f
[0x9f] OP:
0xe POP
[0xa0] OP:
0xf DUP 62
[0xa1] OP:
0xf DUP 62
[0xa2] OP:
0x1 ADD 62, 62 = c4
[0xa3] OP:
0x1 ADD 62, ffffffc4 = 26
[0xa4] OP:
0xd JPM f117f510
[0x80] OP:
0x10 REVERSE TOP 2
[0x82] OP:
0xf DUP 1
[0x83] OP:
0xa PUSH ffffffff
[0x85] OP:
0x5 XOR 1, ffffffff = fffffffe
[0x86] OP:
0xc JPM f117f519
[0x89] OP:
0xe POP
[0x8a] OP:
0xd JPM f117f521
[0x91] OP:
0x10 REVERSE TOP 2
[0x93] OP:
0x10 REVERSE TOP 2
[0x95] OP:
0xc JPM f117f528
[0x98] OP:
0xe POP
[0x99] OP:
0xa PUSH 1
[0x9b] OP:
0x1 ADD 26, 1 = 27
[0x9c] OP:
0xd JPM f117f530
[0xa0] OP:
0xf DUP 27
[0xa1] OP:
0xf DUP 27
[0xa2] OP:
0x1 ADD 27, 27 = 4e
[0xa3] OP:
0x1 ADD 27, 4e = 75
[0xa4] OP:
0xd JPM f117f510
[0x80] OP:
0x10 REVERSE TOP 2
[0x82] OP:
0xf DUP ffffffff
[0x83] OP:
0xa PUSH ffffffff
[0x85] OP:
0x5 XOR ffffffff, ffffffff = 0
[0x86] OP:
0xc JPM f117f51d
[0x8d] OP:
0xe POP
[0x8e] OP:
0xd JPM f117f537
[0xa7] OP:
0xe POP
[0xa8] OP:
0x8 READ i
result = 0
for i in range(7, -1, -1):
	if (x >> i) & 1 == 1:
 result = (result + 1) * 3
	else:
 result = result * 3
	result = result % 256
return result
[0xa0] OP:
0xf DUP 1
[0xa1] OP:
0xf DUP 1
[0xa2] OP:
0x1 ADD 1, 1 = 2
[0xa3] OP:
0x1 ADD 1, 2 = 3
[0xa4] OP:
0xd JPM f117f510

[0x80] OP:
0x10 REVERSE TOP 2
[0x82] OP:
0xf DUP 1
[0x83] OP:
0xa PUSH ffffffff
[0x85] OP:
0x5 XOR 1, ffffffff = fffffffe
[0x86] OP:
0xc JPM f117f519
[0x89] OP:
0xe POP
[0x8a] OP:
0xd JPM f117f521

[0x91] OP:
0x10 REVERSE TOP 2
[0x93] OP:
0x10 REVERSE TOP 2
[0x95] OP:
0xc JPM f117f528

[0x98] OP:
0xe POP
[0x99] OP:
0xa PUSH 1
[0x9b] OP:
0x1 ADD 3, 1 = 4
[0x9c] OP:
0xd JPM f117f530
import subprocess

key = [0xc6,0x8b,0xd9,0xcf,0x63,0x60,0xd8,0x7b,0xd8,0x60,0xf6,0xd3,0x7b,0xf6,0xd8,0xc1,0xcf,0xd0,0xf6,0x72,0x63,0x75,0xbe,0xf6,0x7f,0xd8,0x63,0xe7,0x6d,0xf6,0x63,0xcf,0xf6,0xd8,0xf6,0xd8,0x63,0xe7,0x6d,0xb4,0x88,0x72,0x70,0x75,0xb8,0x75]
key = key[::-1]
table = {}

for i in range(0x21, 0xfd):
 cmd = 'echo "{}" | ./a.out | grep 0xb90 | cut -d " " -f 5'.format(chr(i))
 result = subprocess.run(cmd, capture_output=True, shell=True)
 table[result.stdout.decode().replace(",\n", "")] = chr(i)

for k in key:
 print(table[hex(k).replace("0x", "")], end="")
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