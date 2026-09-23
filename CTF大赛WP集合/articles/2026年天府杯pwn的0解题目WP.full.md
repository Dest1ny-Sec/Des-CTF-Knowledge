---
title: 2026 天府杯 pwn 0 解题目 WP（libc-2.27 菜单+）
contest: 2026 天府杯
year: 2026
difficulty: hard
vuln_type:
- heap_exploit
- ret2libc
- rop
tags:
- 天府杯 2026 pwn 0 解
- libc-2.27 经典堆利用
- setvbuf 关闭缓冲
- 菜单 mean()+input()+add()+show() 子函数 0x400b7f/0x400bea/0x400ccd
- result 全局标志 0/1 二次进入
- while(true) 循环
- pwndbg fork 跟踪
- tcache 攻击
attack_chain:
- libc-2.27 经典堆版本
- setvbuf 关闭 stdout/stderr/stdin 缓冲
- 菜单：mean() + input() 选 1/2/1337
- add(0x400b7f) / show(0x400bea) / show(0x400ccd) 二次入口
- result 全局变量 = 0 → 1337 显示一次后置 1
- 下次进 1337 → result 返 0 直接退出
- 0 解：题目难度大，48h 比赛 0 队伍提交
key_payload: result=1 后 1337 失效，要重置触发两次入口
one_liner: 2026 天府杯 pwn 0 解题目：libc-2.27 菜单题 add+show+0x400b7f/bea/ccd 子函数+result 全局标志 0/1，二次入口切换。
lesson: 天府杯是国内顶级线下 CTF，2026 pwn 出现 0 解题目说明难度极高；libc-2.27 经典堆漏洞是 tcache 时代代表，House of Apple 2 + tcache 攻击仍是主流。
quality: medium
full_path: 2026年天府杯pwn的0解题目WP.full.md
meta_path: 2026年天府杯pwn的0解题目WP.meta.md
images_removed: true
images_removed_count: 8
schema_version: v3.0.0-P0
summary: 2026 天府杯 pwn 0 解题目 WP（libc-2.27 菜单+）。2026 天府杯 pwn 0 解题目：libc-2.27 菜单题 add+show+0x400b7f/bea/ccd 子函数+result 全局标志 0/1，二次入口切换。。关键路径：libc-2.27 经典堆版本 → setvbuf 关闭 stdout/stderr/stdin 缓冲 → 菜单：mean() + in...
category: pwn
subcategory: heap_exploitation
subcategories:
- heap_exploitation
- stack_overflow
- rop
tools_used:
- GDB
time_required: long
difficulty_score: 4
code_blocks_count: 0
images_count: 8
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/296847.html
reasoning_chain:
- libc-2.27 经典堆版本 + setvbuf 关缓冲 → 触发点：菜单题 add/show/0x400b7f/bea/ccd
- 菜单 mean()+input() 选 1/2/1337 → 假设：result 全局标志 0/1 切换二次入口
- add(0x400b7f) / show(0x400bea) / show(0x400ccd) → 观察：sub function 偏移
- 假设：result=0 → 1337 显示一次 → 动作：触发后置 1 → 下次返 0 直接退出
- 假设：要重置触发两次入口 → 动作：找 result 写入路径
- 0 解：48h 比赛 0 队伍提交 → 触发点：题目难度极高
- 假设：House of Apple 2 + tcache 攻击 → 动作：pwndbg fork 跟踪堆分配
failed_attempts:
- 试图普通 tcache 攻击 → 失败：result 全局标志限制二次入口
- setvbuf 关闭缓冲后 IO 报错 → 失败：需 pwntools context.log_level = 'debug' 调试
- 整数溢出绕过 → 失败：菜单长度有限制
key_observations:
- libc-2.27 经典堆漏洞 = tcache 时代代表，House of Apple 2 + tcache 仍是主流
- result 全局变量 0/1 切换二次入口是菜单题反自动化套路
- 天府杯是国内顶级线下 CTF，2026 pwn 出现 0 解说明难度极高
- setvbuf 关闭缓冲是为了绕过 stdout 探测延迟
- sub function 偏移 0x400b7f/bea/ccd 三入口是分阶段调试触发点
prerequisites:
- libc-2.27 堆漏洞（tcache / House of Apple 2）
- GDB/pwndbg fork 跟踪
- 菜单题逆向 + 全局状态机分析
- setvbuf/printf 缓冲控制
---
# 2026年天府杯pwn的0解题目WP

> 原文: https://www.ctfiot.com/296847.html
> ID: 296847

2026年天府杯pwn的0解题目WP

libc版本为2.27

整体代码逻辑如下：

extern FILE *stderr;

extern FILE *stdin;

extern FILE *stdout;

unsignedintmain(unsignedinta0, unsignedlonglonga1)

{

unsignedlonglong v0;  // [bp-0x28]

unsignedint v1;  // [bp-0x1c]

char result;  // [bp-0x11]

unsignedlonglong v3;  // [bp-0x10]

v1= a0;

v0= a1;

setvbuf(stdout, NULL, 2, 0);

setvbuf(stderr, NULL, 2, 0);

setvbuf(stdin, NULL, 2, 0);

result =0;

while (true)

{

mean();

v3 =input();

if (v3 ==1)

{

add(sub_400b7f);

}

elseif (v3 >=1)

{

if (v3 ==2)

{

show(sub_400bea);

}

elseif (v3 ==1337)

{

if (result)

return0;

show(sub_400ccd);

result =1;

}

else

{

return0;

}

}

}

}

intmean()

{

puts(“1. malloc”);

puts(“2. delete”);

puts(“3. exit”);

returnprintf(“>> “);

}

longlonginput()

{

unsignedlonglong v0;  // [bp-0x30]

char v1;  // [bp-0x28]

v0=16;

memset(&v1, 0, 16);

shuru(&v1, 15);

returnstrtol(&v1, NULL, 10);

}

longlongshuru(char*a0, longlonga1)

{

char v0;  // [bp-0x21]

void* i;  // [bp-0x20]

unsignedlonglong count;  // [bp-0x18]

for (i =0; i < a1; i +=1)

{

count =read(0, &v0, 1);

if (count !=1)

exit(–1); /* do not return */

if (v0 ==10)

return i;

*((char*)(a0 + i)) = v0;

}

return i;

}

typedefstruct struct_0 {

struct struct_0 *field_0;

} struct_0;

externunsignedlonglongg_602060[4];

externunsignedlonglong g_602160;

void*sub_400ec0(struct_0 **a0)

{

char v0;  // [bp-0x29]

void* idx;  // [bp-0x28]

void* j;  // [bp-0x20]

unsignedlonglong v3;  // [bp-0x18]

unsignedlonglong v4;  // [bp-0x10]

puts(“Length: “);

v3=input();

if (v3 >640)

exit(–1); /* do not return */

v4= v3 +15>>4;

for (idx =0; idx <=31&&*((longlong*)(0x8* idx + (char*)&g_602060[0])); idx +=1);

if (idx ==32)

exit(–1); /* do not return */

*((unsignedlonglong*)(0x8* idx + (char*)&g_602060[0])) =a0(v4);

*((unsignedlonglong*)(0x8* idx + (char*)&g_602160)) = v4;

puts(“Data: “);

for (j =0; j < v4; j +=1)

{

v0 =sub_40108a(j *24+*((longlong*)(0x8* idx + (char*)&g_602060[0])));

if (v0 !=1)

return v0 ^1;

}

return j;

}

typedefstruct struct_0 {

charpadding_0[16];

unsignedlonglong field_10;

} struct_0;

unsignedlonglongsub_40108a(struct_0 *ptr)

{

ptr->field_10=shuru(ptr, 16);

returnptr->field_10&0xffffffffffffff00|ptr->field_10==16;

}

unsignedlonglongsub_400b7f(unsignedlonga0)

{

void* i;  // [bp-0x18]

unsignedlonglong ptr;  // [bp-0x10]

ptr =malloc(a0 *24);

for (i =0; i < a0; i +=1)

{

sub_400e4a(ptr + i *24);

}

return ptr;

}

typedefstruct struct_0 {

charpadding_0[16];

void* field_10;

} struct_0;

longlongsub_400e4a(struct_0 *ptr)

{

ptr->field_10=0;

returnsub_401062(ptr);

}

longlongsub_401062(struct_0 *a0)

{

returnmemset(a0, 0, a0->field_10);

}

typedefstruct struct_0 {

struct struct_0 *field_0;

} struct_0;

externunsignedlonglongg_602060[4];

unsignedlonglongshow(struct_0 **a0)

{

unsignedlonglong v0;  // [bp-0x10]

puts(“Index: “);

v0=input();

if (v0 <=31)

return (!g_602060[v0] ?puts(“Nope”) :a0(v0));

exit(–1); /* do not return */

}

externvoid g_602060;

void*sub_400bea(unsignedlongidx)

{

void* i;  // rbx

if (*((longlong*)&(&g_602060)[8* idx]))

{

i =*((longlong*)&(&g_602060)[8* idx]) +*((longlong*)(*((longlong*)&(&g_602060)[8* idx]) –8)) *24;

while (i !=*((longlong*)&(&g_602060)[8* idx]))

{

sub_400e72(i –24);

}

sub_400d45(*((longlong*)&(&g_602060)[8* idx]) –8);

}

*((unsignedlonglong*)&(&g_602060)[8* idx]) =0;

return&g_602060;

}

longlongsub_400e72(void*a0)

{

returnsub_401062(a0);

}

longlongsub_401062(struct_0 *a0)

{

returnmemset(a0, 0, a0->field_10);

}

longlongsub_400d45(unsignedlonga0)

{

return (unsignedlonglong)free(a0 +15&0xfffffffffffffff0);

}

externunsignedlonglongg_602060[4];

externunsignedlonglongg_602160[4];

intsub_400ccd(unsignedlonga0)

{

void* i;  // [bp-0x10]

for (i =0; i <g_602160[a0]; i +=1)

{

sub_400e8e(i *24+g_602060[a0]);

}

returnputchar(10);

}

typedefstruct struct_0 {

charpadding_0[16];

char field_10;

} struct_0;

extern FILE *stdout;

longlongsub_400e8e(struct_0 *a0)

{

returnfwrite(a0, *((longlong*)&a0->field_10), 1, stdout);

}

保护机制、ROP链、gadget、sh：

详细分析：

这里需要注意绕过，我们输入的size经过了运算和移位

然后就是注意对齐，清空 field_10的最低字节，然后设置其值为 0x10

注意用户实际输入的计算：

1. 用户输入size = v3 (比如0x60 = 96)

2. 计算结构体数量：v4 = (v3 + 15) / 16

3. 实际malloc：malloc(v4 * 24)

举个例子：

– 用户输入：0x60 = 96字节

– 结构体数量：(96 + 15) / 16 = 111 / 16 = 6 (整数除法)

– 实际malloc：6 * 24 = 144字节

– malloc对齐后：0x90字节，但堆头占0x10，所以用户看到0x80

但是也可以不用纠结这个问题，直接按照常规来写脚本就可以，就是注意分配的地址大小

然后有一个隐藏的show函数，当输入1337时候出现，但是只有一次机会

运行之后result = 1，就不能第二次进去了

然后是delete，就是free之后把指针清零（因为这个程序不是多线程程序所以不存在UAF，如果是多线程就得分情况导致潜在UAF漏洞的核心问题在于，释放内存和清空全局表指针的操作不是原子性的，在这之间存在一个时间窗口，并且代码逻辑可能创建了指向已释放内存的“悬垂指针”）

但是要注意delete内存对齐问题函数中存在堆操作越界 / 非法内存访问，正确的对齐计算：free((void*)((a0 + 15) & ~0xF))，否则，错误的地址导致破坏glibc的堆管理结构程序会退出

所以：先申请了 17 个堆块（索引0-16），free  10/7/6/2——这些索引在show()的检查范围内（v0<=31），且先通过add操作把g_602060的对应位置写入了合法的堆地址（而非随机值），避免了puts("Nope")后触发的非法访问。先大量add不同大小的堆块（0x70/0x10/0xb0/0xd0等），让g_602060中对应索引的位置被写入malloc返回的合法堆地址（而非越界的随机值），此时sub_400bea中*((long long *)&(&g_602060)[8 * idx])是合法地址，暂时不会触发段错误。通过add(0x10, pld(0,0x441 + 0x20*3 + 0x60))等操作，伪造了a0的值，让a0+15&~0xf恰好等于一个合法的堆地址（而非野指针），规避了free非法地址触发的崩溃。

Exp攻击如下：

本篇文章来源于微信公众号: 由由学习吧

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