# Aliyun2025 题解：easy-cuda-rev PTX汇编+cuda加速

> 原文: https://www.ctfiot.com/232133.html
> ID: 232133

1

题目描述

2

提取PTX汇编

cuobjdump -ptx .easy_cuda > test.txt

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

}

3

Gork+Deepseek分析

def gift1(data, key=0xac, rounds=1):
 data = list(data) # 复制输入数据，避免修改原数组
 n = len(data) # 数据长度，模拟线程数

 # 阶段 1：初始 XOR + S-box 迭代
 for i in range(n):
 # 初始 XOR
 val = data[i]
 temp = (i * 73 + key) & 0xffff # 模拟 16 位运算
 val ^= temp
 # 高低 4 位交换
 val = ((val & 0xf0) >> 4) | ((val & 0x0f) << 4)
 
 # S-box 迭代（5 次循环合并为一个函数）
 for _ in range(5):
 for r in range(rounds):
 val = SBOX[val]
 val = ((val & 0xf0) >> 4) | ((val & 0x0f) << 4)
 val ^= r & 0xff # 模拟计数器 XOR
 data[i] = val & 0xff

def gift2(data):
 for i in range(256):
 temp = data[i] ^ 0xac
 next_idx = (i + 1) % 256 # 循环取相邻数据
 data[i] = temp ^ data[next_idx]
 return data

def encrypt_exchange(data, num_threads):
 """
 模拟 PTX 代码中的两次交换过程，支持环形交换。
 :param data: 输入数据列表，长度为 num_threads。
 :param num_threads: 线程数。
 :return: 交换后的数据列表。
 """
 # 第一次交换：偶数线程与奇数线程交换
 for thread_id in range(0, num_threads, 2): # 遍历偶数线程
 target_thread_id = (thread_id + 1) % num_threads # 环形回绕
 # 交换数据
 data[thread_id], data[target_thread_id] = data[target_thread_id], data[thread_id]

 # 第二次交换：奇数线程与偶数线程交换
 for thread_id in range(1, num_threads, 2): # 遍历奇数线程
 target_thread_id = (thread_id + 1) % num_threads # 环形回绕
 # 交换数据
 data[thread_id], data[target_thread_id] = data[target_thread_id], data[thread_id]

 return data

def tea_encrypt(plain_text, key,delta = 0x9E3779B9,sum = 0):
 """TEA 加密函数
 plain_text: 待加密的 2 元素列表，每个元素为 32 位整数
 key: 4 元素列表，每个元素为 32 位整数
 """
 v0, v1 = plain_text
 k0, k1, k2, k3 = key
 
 for _ in range(8): # 32轮加密
 sum = (sum + delta) & 0xFFFFFFFF
 v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
 v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
 

 return [v0, v1]

def gift5(data):
 tea_key = [-1556008596 & 0xffffffff , -939442524 & 0xffffffff, 1013904242 & 0xffffffff, 338241895 & 0xffffffff]
 enc = b''
 for i in range(0,len(data),8):
 v0 = int.from_bytes(data[i:i+4], 'little')
 v1 = int.from_bytes(data[i+4:i+8], 'little')
 sum = 0
 for j in range(10485760 // 8):
 v0, v1 = tea_encrypt([v0,v1],tea_key,sum=sum)
 sum = (sum - 239350328) & 2 ** 32 -1
 
 
 enc += v0.to_bytes(4, 'little') + v1.to_bytes(4, 'little')
 print(v0.to_bytes(4, 'little').hex(), v1.to_bytes(4, 'little').hex())
 exit()
 return enc

import numpy as np
from numba import cuda

# S-box 表 (T[256])
SBOX = np.array([
 99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22
], dtype=np.uint8)

ISBOX = np.array([82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]
, dtype=np.uint8)

# 将 SBOX 传输到全局 GPU 内存
SBOX_global = cuda.to_device(SBOX)
ISBOX_global = cuda.to_device(ISBOX)

@cuda.jit
def encrypt_stage1_cuda(SBOX_global ,data, key, rounds, output):
 """
 CUDA 核函数：实现 PTX 第一阶段的加密逻辑。
 :param data: 输入字节数组 (uint8)
 :param key: 密钥 (uint8)
 :param rounds: S-box 迭代轮数
 :param output: 输出数组 (uint8)
 """
 idx = cuda.grid(1) # 全局线程索引，等价于 PTX 的 %r4
 if idx < data.size: # 等价于 PTX 的 %p1 检查
 # 初始 XOR 和高低位交换
 val = data[idx]
 temp = (idx * 73 + key) & 0xffff # 16 位运算
 val ^= temp
 val = ((val & 0xf0) >> 4) | ((val & 0x0f) << 4) # 高低位交换

 # 5 次 S-box 迭代
 for _ in range(5):
 for r in range(rounds):
 val = SBOX_global[val] # S-box 替换
 val = ((val & 0xf0) >> 4) | ((val & 0x0f) << 4) # 高低位交换
 val ^= r & 0xff # XOR 计数器
 val &= 0xff # 确保 8 位

 output[idx] = val

@cuda.jit
def decrypt_stage1_cuda(ISBOX_global, data, key, rounds, output):
 idx = cuda.grid(1)
 if idx < data.size:
 val = np.uint8(data[idx])

 for _ in range(5):
 for r in range(rounds - 1, -1, -1):
 val ^= np.uint8(r & 0xff)
 val = np.uint8(((val & 0xf0) >> 4) | ((val & 0x0f) << 4))
 val = ISBOX_global[val] # 直接赋值，不用 np.uint8()

 val = np.uint8(((val & 0xf0) >> 4) | ((val & 0x0f) << 4))
 temp = np.uint16(idx * 73 + key) & np.uint16(0xffff)
 val ^= temp

 output[idx] = val

def encrypt_stage1(data, key=0xac, rounds=10485760, threads_per_block=256):
 """
 使用 CUDA 加速的第一阶段加密。
 :param data: 输入字节数组 (list of int, 0-255)
 :param key: 密钥 (默认 0xac)
 :param rounds: S-box 迭代轮数 (默认 10485760)
 :param threads_per_block: 每个块的线程数
 :return: 加密后的字节数组
 """
 # 转换为 NumPy 数组并传输到 GPU
 data_np = np.frombuffer(data, dtype=np.uint8)
 data_device = cuda.to_device(data_np)
 output_device = cuda.device_array_like(data_np)

 # 计算网格和块配置
 n = len(data)
 blocks = (n + threads_per_block - 1) // threads_per_block # 向上取整

 # 调用 CUDA 核函数
 encrypt_stage1_cuda[blocks, threads_per_block](SBOX_global ,data_device, key, rounds, output_device)

 # 将结果从 GPU 拷贝回 CPU
 result = output_device.copy_to_host() # 直接拷贝为 NumPy 数组
 return result.tolist() # 转换为 Python 列表

def decrypt_stage1(data, key=0xac, rounds=10485760, threads_per_block=256):
 data_np = np.frombuffer(data, dtype=np.uint8)
 data_device = cuda.to_device(data_np)
 output_device = cuda.device_array_like(data_np)

 n = len(data)
 blocks = (n + threads_per_block - 1) // threads_per_block # 向上取整
 decrypt_stage1_cuda[blocks, threads_per_block](ISBOX_global,data_device,key,rounds,output_device)

 result = output_device.copy_to_host() # 直接拷贝为 NumPy 数组
 return result.tolist() # 转换为 Python 列表

# 测试代码
if __name__ == "__main__":
 # 示例输入
 with open("flag",'rb') as f:
 input_data = f.read()
 # print("Original:", input_data)
 
 # CUDA 加速加密
 encrypted = encrypt_stage1(input_data, key=0xac) # 为了测试，使用较小的 rounds
 for num in encrypted:
 print(f'{num:02x}',end=' ')
 print(encrypted[:256])
 dec = decrypt_stage1(bytes(encrypted))
 print(dec)

def rev_gift2(data_):
 res = []
 for index in range(0,len(data_),256):
 data = data_[index:index+256]
 for i in range(255,-1,-1):
 next_idx = (i + 1) % 256 # 循环取相邻数据
 temp = data[next_idx] ^ data[i]
 data[i] = temp^ 0xac
 res = res + data
 return res

def decrypt_exchange(data_, num_threads=256):
 res = []
 for i in range(0,len(data_),256):
 data = data_[i:i+256]
 for thread_id in range(1, num_threads, 2): # 遍历奇数线程
 target_thread_id = (thread_id + 1) % num_threads # 环形回绕
 # 交换数据
 data[thread_id], data[target_thread_id] = data[target_thread_id], data[thread_id]

 for thread_id in range(0, num_threads, 2): # 遍历偶数线程
 target_thread_id = (thread_id + 1) % num_threads # 环形回绕
 # 交换数据
 data[thread_id], data[target_thread_id] = data[target_thread_id], data[thread_id]
 res = res + data
 return res

import numpy as np
from numba import cuda

# TEA 常量
DELTA = np.uint32(0x9E3779B9)
TEA_KEY = np.array([-1556008596 & 0xffffffff, -939442524 & 0xffffffff,
 1013904242 & 0xffffffff, 338241895 & 0xffffffff], dtype=np.uint32)
TEA_KEY_GLOBAL = cuda.to_device(TEA_KEY)

@cuda.jit
def tea_encrypt_cuda(TEA_KEY_GLOBAL, data, output, rounds):
 """
 CUDA 核函数：TEA 加密变种。
 :param data: 输入字节数组 (uint8, 256 字节)
 :param output: 输出字节数组 (uint8, 256 字节)
 :param rounds: 总轮数
 """
 idx = cuda.grid(1) # 全局线程索引
 if idx < 32: # 32 个 8 字节块
 # 计算每个线程的偏移
 start = idx * 8

 # 加载 v0 和 v1 (小端序)
 v0 = np.uint32(data[start] | (data[start + 1] << 8) | 
 (data[start + 2] << 16) | (data[start + 3] << 24))
 v1 = np.uint32(data[start + 4] | (data[start + 5] << 8) | 
 (data[start + 6] << 16) | (data[start + 7] << 24))

 # 初始化 sum 为 uint32
 sum_val = np.uint32(0)

 # 主循环：每次 8 轮
 for _ in range(rounds // 8):
 for _ in range(8): # 模拟 tea_encrypt 的 8 轮
 sum_val = np.uint32(sum_val + 0x9E3779B9) & np.uint32(0xffffffff)
 v0 = np.uint32(v0 + (((v1 << 4) + TEA_KEY_GLOBAL[0]) ^ 
 (v1 + sum_val) ^ ((v1 >> 5) + TEA_KEY_GLOBAL[1]))) & np.uint32(0xffffffff)
 v1 = np.uint32(v1 + (((v0 << 4) + TEA_KEY_GLOBAL[2]) ^ 
 (v0 + sum_val) ^ ((v0 >> 5) + TEA_KEY_GLOBAL[3]))) & np.uint32(0xffffffff)
 
 if idx == 0:
 print(v0,v1)
 
 sum_val = np.uint32(sum_val - 239350328) & np.uint32(0xffffffff)

 # 存储结果到输出数组
 output[start] = v0 & 0xff
 output[start + 1] = (v0 >> 8) & 0xff
 output[start + 2] = (v0 >> 16) & 0xff
 output[start + 3] = (v0 >> 24) & 0xff
 output[start + 4] = v1 & 0xff
 output[start + 5] = (v1 >> 8) & 0xff
 output[start + 6] = (v1 >> 16) & 0xff
 output[start + 7] = (v1 >> 24) & 0xff
 

@cuda.jit
def tea_decrypt_cuda(TEA_KEY_GLOBAL, data, output, rounds):
 idx = cuda.grid(1) # 全局线程索引
 if idx < 32: # 32 个 8 字节块
 # 计算每个线程的偏移
 start = idx * 8

 # 加载 v0 和 v1 (小端序)
 v0 = np.uint32(data[start] | (data[start + 1] << 8) | 
 (data[start + 2] << 16) | (data[start + 3] << 24))
 v1 = np.uint32(data[start + 4] | (data[start + 5] << 8) | 
 (data[start + 6] << 16) | (data[start + 7] << 24))

 # 初始化 sum 为 uint32
 sum_val = np.uint32(((-239350328 * (10485760 // 8))) & 2 ** 32 -1)

 # 主循环：每次 8 轮
 for _ in range(rounds // 8):
 for _ in range(8): # 模拟 tea_encrypt 的 8 轮
 v1 = np.uint32(v1 - (((v0 << 4) + TEA_KEY_GLOBAL[2]) ^ 
 (v0 + sum_val) ^ ((v0 >> 5) + TEA_KEY_GLOBAL[3]))) & np.uint32(0xffffffff)
 v0 = np.uint32(v0 - (((v1 << 4) + TEA_KEY_GLOBAL[0]) ^ 
 (v1 + sum_val) ^ ((v1 >> 5) + TEA_KEY_GLOBAL[1]))) & np.uint32(0xffffffff)
 
 sum_val = np.uint32(sum_val - 0x9E3779B9) & np.uint32(0xffffffff)
 if idx == 0:
 print(v0,v1)
 
 sum_val = np.uint32(sum_val + 239350328) & np.uint32(0xffffffff)

 # 存储结果到输出数组
 output[start] = v0 & 0xff
 output[start + 1] = (v0 >> 8) & 0xff
 output[start + 2] = (v0 >> 16) & 0xff
 output[start + 3] = (v0 >> 24) & 0xff
 output[start + 4] = v1 & 0xff
 output[start + 5] = (v1 >> 8) & 0xff
 output[start + 6] = (v1 >> 16) & 0xff
 output[start + 7] = (v1 >> 24) & 0xff

def tea_encrypt_cuda_host(data, rounds=10485760, threads_per_block=32):
 """
 使用 CUDA 加速的 TEA 加密。
 :param data: 输入字节数组 (256 字节)
 :param rounds: 总轮数 (默认 10485760)
 :param threads_per_block: 每个块的线程数
 :return: 加密后的字节数组
 """
 # if len(data) != 256:
 # raise ValueError("Data must be exactly 256 bytes")

 # 转换为 NumPy 数组并传输到 GPU
 data_np = np.array(list(data), dtype=np.uint8)
 data_device = cuda.to_device(data_np)
 output_device = cuda.device_array_like(data_np)

 # 计算网格和块配置
 blocks = 1 # 固定 32 个线程，1 个块足够
 tea_encrypt_cuda[blocks, threads_per_block](TEA_KEY_GLOBAL, data_device, output_device, rounds)

 # 将结果拷贝回 CPU
 result = output_device.copy_to_host()
 return bytes(result)

def tea_decrypt_cuda_host(data_, rounds=10485760, threads_per_block=32):
 """
 使用 CUDA 加速的 TEA 加密。
 :param data: 输入字节数组 (256 字节)
 :param rounds: 总轮数 (默认 10485760)
 :param threads_per_block: 每个块的线程数
 :return: 加密后的字节数组
 """
 print("data_:",len(data_))
 res = b''
 for index in range(0,len(data_),256):
 # print(index)
 data = data_[index:index+256]
 # print(len(data))
 if len(data) != 256:
 raise ValueError("Data must be exactly 256 bytes")

 # 转换为 NumPy 数组并传输到 GPU
 data_np = np.array(list(data), dtype=np.uint8)
 data_device = cuda.to_device(data_np)
 output_device = cuda.device_array_like(data_np)

 # 计算网格和块配置
 blocks = 1 # 固定 32 个线程，1 个块足够
 tea_decrypt_cuda[blocks, threads_per_block](TEA_KEY_GLOBAL, data_device, output_device, rounds)

 # 将结果拷贝回 CPU
 result = output_device.copy_to_host()
 res += bytes(result)
 return res

# 测试代码
if __name__ == "__main__":
 data = bytes([150, 4, 235, 182, 108, 114, 166, 121, 74, 204, 139, 106, 35, 137, 56, 11, 217, 104, 176, 195, 147, 190, 119, 62, 37, 23, 23, 196, 174, 33, 65, 64, 190, 149, 92, 135, 185, 41, 15, 137, 3, 0, 216, 54, 119, 105, 150, 80, 15, 82, 236, 171, 254, 251, 74, 47, 141, 246, 159, 206, 226, 2, 67, 177, 82, 3, 1, 248, 111, 207, 190, 158, 6, 98, 248, 144, 237, 201, 249, 159, 139, 115, 242, 169, 7, 175, 67, 189, 67, 181, 203, 232, 20, 38, 5, 51, 117, 8, 113, 113, 30, 117, 148, 167, 77, 18, 132, 68, 104, 105, 97, 6, 186, 137, 70, 190, 105, 4, 183, 136, 113, 11, 170, 151, 58, 152, 114, 55, 78, 128, 86, 82, 17, 239, 59, 145, 109, 224, 85, 158, 187, 215, 122, 153, 25, 137, 188, 161, 126, 51, 168, 103, 155, 54, 86, 46, 76, 230, 182, 30, 0, 151, 188, 48, 66, 13, 217, 209, 37, 70, 204, 53, 135, 132, 213, 253, 23, 11, 29, 96, 86, 18, 49, 76, 215, 94, 99, 127, 133, 165, 176, 189, 253, 238, 221, 55, 110, 147, 9, 153, 48, 126, 37, 142, 242, 60, 109, 205, 93, 67, 94, 75, 53, 137, 22, 147, 160, 171, 234, 145, 173, 169, 161, 142, 152, 120, 122, 170, 192, 70, 99, 82, 239, 149, 74, 209, 38, 155, 245, 228, 188, 53, 14, 68, 104, 240, 5, 57, 139, 112, 36, 215, 222, 101, 73, 65])

 print("Original:", data.hex()[:32], "...")
 encrypted = tea_encrypt_cuda_host(data) 
 # print("Encrypted:", encrypted.hex(), "...")
 # for num in encrypted:
 # print(f'{num:02x}',end=' ')

 dec = tea_decrypt_cuda_host(encrypted)
 for num in dec:
 print(f'{num:02x}',end=' ')
 assert data == dec

from cudagift5 import tea_decrypt_cuda_host
from gift34 import decrypt_exchange
from cuda_gift1 import decrypt_stage1
from gift2 import rev_gift2

with open("flag_enc",'rb') as f:
 enc = f.read()

print(len(enc))
# xor thread id
enc_xor = []
for i in range(len(enc)):
 enc_xor.append(enc[i] ^ (i % 256))
print("gift 6")

# rev gift5
enc = bytes(enc_xor)
dec = tea_decrypt_cuda_host(enc)
print("gift 5")

with open("flag_gift5",'wb') as f:
 f.write(dec)

# with open("flag_gift5",'rb') as f:
# dec = f.read()

# rev gift34
enc = list(dec)
dec = decrypt_exchange(enc)
print("gift 34")

#rev gift2
enc = dec
dec = rev_gift2(enc)
print("gift 2")

# rev gift1
enc = bytes(dec)
dec = decrypt_stage1(enc)
print("gift 1")

with open("flag.dec",'wb') as f:
 f.write(bytes(dec))

看雪ID：SleepAlone

https://bbs.kanxue.com/user-home-950548.htm

*本文为看雪论坛文章，由 SleepAlone 原创，转载请注明来自看雪社区

# 往期推荐

1、一种基于unicorn的寄存器间接跳转混淆去除方式

2、白盒SM4的DFA方案

3、VNCTF-2025-赛后复现

4、IDA Pro 9 SP1 安装和插件配置

5、初探 android crc 检测及绕过

球分享

球点赞

球在看

点击阅读原文查看更多


```
cuobjdump -ptx .easy_cuda > test.txt
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

}
```



```
def gift1(data, key=0xac, rounds=1):
 data = list(data) # 复制输入数据，避免修改原数组
 n = len(data) # 数据长度，模拟线程数

 # 阶段 1：初始 XOR + S-box 迭代
 for i in range(n):
 # 初始 XOR
 val = data[i]
 temp = (i * 73 + key) & 0xffff # 模拟 16 位运算
 val ^= temp
 # 高低 4 位交换
 val = ((val & 0xf0) >> 4) | ((val & 0x0f) << 4)
 
 # S-box 迭代（5 次循环合并为一个函数）
 for _ in range(5):
 for r in range(rounds):
 val = SBOX[val]
 val = ((val & 0xf0) >> 4) | ((val & 0x0f) << 4)
 val ^= r & 0xff # 模拟计数器 XOR
 data[i] = val & 0xff
```



```
def gift2(data):
 for i in range(256):
 temp = data[i] ^ 0xac
 next_idx = (i + 1) % 256 # 循环取相邻数据
 data[i] = temp ^ data[next_idx]
 return data
```



```
def encrypt_exchange(data, num_threads):
 """
 模拟 PTX 代码中的两次交换过程，支持环形交换。
 :param data: 输入数据列表，长度为 num_threads。
 :param num_threads: 线程数。
 :return: 交换后的数据列表。
 """
 # 第一次交换：偶数线程与奇数线程交换
 for thread_id in range(0, num_threads, 2): # 遍历偶数线程
 target_thread_id = (thread_id + 1) % num_threads # 环形回绕
 # 交换数据
 data[thread_id], data[target_thread_id] = data[target_thread_id], data[thread_id]

 # 第二次交换：奇数线程与偶数线程交换
 for thread_id in range(1, num_threads, 2): # 遍历奇数线程
 target_thread_id = (thread_id + 1) % num_threads # 环形回绕
 # 交换数据
 data[thread_id], data[target_thread_id] = data[target_thread_id], data[thread_id]

 return data
```



```
def tea_encrypt(plain_text, key,delta = 0x9E3779B9,sum = 0):
 """TEA 加密函数
 plain_text: 待加密的 2 元素列表，每个元素为 32 位整数
 key: 4 元素列表，每个元素为 32 位整数
 """
 v0, v1 = plain_text
 k0, k1, k2, k3 = key
 
 for _ in range(8): # 32轮加密
 sum = (sum + delta) & 0xFFFFFFFF
 v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
 v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
 

 return [v0, v1]
```



```
def gift5(data):
 tea_key = [-1556008596 & 0xffffffff , -939442524 & 0xffffffff, 1013904242 & 0xffffffff, 338241895 & 0xffffffff]
 enc = b''
 for i in range(0,len(data),8):
 v0 = int.from_bytes(data[i:i+4], 'little')
 v1 = int.from_bytes(data[i+4:i+8], 'little')
 sum = 0
 for j in range(10485760 // 8):
 v0, v1 = tea_encrypt([v0,v1],tea_key,sum=sum)
 sum = (sum - 239350328) & 2 ** 32 -1
 
 
 enc += v0.to_bytes(4, 'little') + v1.to_bytes(4, 'little')
 print(v0.to_bytes(4, 'little').hex(), v1.to_bytes(4, 'little').hex())
 exit()
 return enc
```



```
import numpy as np
from numba import cuda

# S-box 表 (T[256])
SBOX = np.array([
 99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118,
 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192,
 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21,
 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117,
 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132,
 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207,
 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168,
 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210,
 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115,
 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219,
 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121,
 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8,
 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138,
 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158,
 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223,
 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22
], dtype=np.uint8)

ISBOX = np.array([82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]
, dtype=np.uint8)

# 将 SBOX 传输到全局 GPU 内存
SBOX_global = cuda.to_device(SBOX)
ISBOX_global = cuda.to_device(ISBOX)

@cuda.jit
def encrypt_stage1_cuda(SBOX_global ,data, key, rounds, output):
 """
 CUDA 核函数：实现 PTX 第一阶段的加密逻辑。
 :param data: 输入字节数组 (uint8)
 :param key: 密钥 (uint8)
 :param rounds: S-box 迭代轮数
 :param output: 输出数组 (uint8)
 """
 idx = cuda.grid(1) # 全局线程索引，等价于 PTX 的 %r4
 if idx < data.size: # 等价于 PTX 的 %p1 检查
 # 初始 XOR 和高低位交换
 val = data[idx]
 temp = (idx * 73 + key) & 0xffff # 16 位运算
 val ^= temp
 val = ((val & 0xf0) >> 4) | ((val & 0x0f) << 4) # 高低位交换

 # 5 次 S-box 迭代
 for _ in range(5):
 for r in range(rounds):
 val = SBOX_global[val] # S-box 替换
 val = ((val & 0xf0) >> 4) | ((val & 0x0f) << 4) # 高低位交换
 val ^= r & 0xff # XOR 计数器
 val &= 0xff # 确保 8 位

 output[idx] = val

@cuda.jit
def decrypt_stage1_cuda(ISBOX_global, data, key, rounds, output):
 idx = cuda.grid(1)
 if idx < data.size:
 val = np.uint8(data[idx])

 for _ in range(5):
 for r in range(rounds - 1, -1, -1):
 val ^= np.uint8(r & 0xff)
 val = np.uint8(((val & 0xf0) >> 4) | ((val & 0x0f) << 4))
 val = ISBOX_global[val] # 直接赋值，不用 np.uint8()

 val = np.uint8(((val & 0xf0) >> 4) | ((val & 0x0f) << 4))
 temp = np.uint16(idx * 73 + key) & np.uint16(0xffff)
 val ^= temp

 output[idx] = val

def encrypt_stage1(data, key=0xac, rounds=10485760, threads_per_block=256):
 """
 使用 CUDA 加速的第一阶段加密。
 :param data: 输入字节数组 (list of int, 0-255)
 :param key: 密钥 (默认 0xac)
 :param rounds: S-box 迭代轮数 (默认 10485760)
 :param threads_per_block: 每个块的线程数
 :return: 加密后的字节数组
 """
 # 转换为 NumPy 数组并传输到 GPU
 data_np = np.frombuffer(data, dtype=np.uint8)
 data_device = cuda.to_device(data_np)
 output_device = cuda.device_array_like(data_np)

 # 计算网格和块配置
 n = len(data)
 blocks = (n + threads_per_block - 1) // threads_per_block # 向上取整

 # 调用 CUDA 核函数
 encrypt_stage1_cuda[blocks, threads_per_block](SBOX_global ,data_device, key, rounds, output_device)

 # 将结果从 GPU 拷贝回 CPU
 result = output_device.copy_to_host() # 直接拷贝为 NumPy 数组
 return result.tolist() # 转换为 Python 列表

def decrypt_stage1(data, key=0xac, rounds=10485760, threads_per_block=256):
 data_np = np.frombuffer(data, dtype=np.uint8)
 data_device = cuda.to_device(data_np)
 output_device = cuda.device_array_like(data_np)

 n = len(data)
 blocks = (n + threads_per_block - 1) // threads_per_block # 向上取整
 decrypt_stage1_cuda[blocks, threads_per_block](ISBOX_global,data_device,key,rounds,output_device)

 result = output_device.copy_to_host() # 直接拷贝为 NumPy 数组
 return result.tolist() # 转换为 Python 列表

# 测试代码
if __name__ == "__main__":
 # 示例输入
 with open("flag",'rb') as f:
 input_data = f.read()
 # print("Original:", input_data)
 
 # CUDA 加速加密
 encrypted = encrypt_stage1(input_data, key=0xac) # 为了测试，使用较小的 rounds
 for num in encrypted:
 print(f'{num:02x}',end=' ')
 print(encrypted[:256])
 dec = decrypt_stage1(bytes(encrypted))
 print(dec)
```



```
def rev_gift2(data_):
 res = []
 for index in range(0,len(data_),256):
 data = data_[index:index+256]
 for i in range(255,-1,-1):
 next_idx = (i + 1) % 256 # 循环取相邻数据
 temp = data[next_idx] ^ data[i]
 data[i] = temp^ 0xac
 res = res + data
 return res
```



```
def decrypt_exchange(data_, num_threads=256):
 res = []
 for i in range(0,len(data_),256):
 data = data_[i:i+256]
 for thread_id in range(1, num_threads, 2): # 遍历奇数线程
 target_thread_id = (thread_id + 1) % num_threads # 环形回绕
 # 交换数据
 data[thread_id], data[target_thread_id] = data[target_thread_id], data[thread_id]

 for thread_id in range(0, num_threads, 2): # 遍历偶数线程
 target_thread_id = (thread_id + 1) % num_threads # 环形回绕
 # 交换数据
 data[thread_id], data[target_thread_id] = data[target_thread_id], data[thread_id]
 res = res + data
 return res
```



```
import numpy as np
from numba import cuda

# TEA 常量
DELTA = np.uint32(0x9E3779B9)
TEA_KEY = np.array([-1556008596 & 0xffffffff, -939442524 & 0xffffffff,
 1013904242 & 0xffffffff, 338241895 & 0xffffffff], dtype=np.uint32)
TEA_KEY_GLOBAL = cuda.to_device(TEA_KEY)

@cuda.jit
def tea_encrypt_cuda(TEA_KEY_GLOBAL, data, output, rounds):
 """
 CUDA 核函数：TEA 加密变种。
 :param data: 输入字节数组 (uint8, 256 字节)
 :param output: 输出字节数组 (uint8, 256 字节)
 :param rounds: 总轮数
 """
 idx = cuda.grid(1) # 全局线程索引
 if idx < 32: # 32 个 8 字节块
 # 计算每个线程的偏移
 start = idx * 8

 # 加载 v0 和 v1 (小端序)
 v0 = np.uint32(data[start] | (data[start + 1] << 8) | 
 (data[start + 2] << 16) | (data[start + 3] << 24))
 v1 = np.uint32(data[start + 4] | (data[start + 5] << 8) | 
 (data[start + 6] << 16) | (data[start + 7] << 24))

 # 初始化 sum 为 uint32
 sum_val = np.uint32(0)

 # 主循环：每次 8 轮
 for _ in range(rounds // 8):
 for _ in range(8): # 模拟 tea_encrypt 的 8 轮
 sum_val = np.uint32(sum_val + 0x9E3779B9) & np.uint32(0xffffffff)
 v0 = np.uint32(v0 + (((v1 << 4) + TEA_KEY_GLOBAL[0]) ^ 
 (v1 + sum_val) ^ ((v1 >> 5) + TEA_KEY_GLOBAL[1]))) & np.uint32(0xffffffff)
 v1 = np.uint32(v1 + (((v0 << 4) + TEA_KEY_GLOBAL[2]) ^ 
 (v0 + sum_val) ^ ((v0 >> 5) + TEA_KEY_GLOBAL[3]))) & np.uint32(0xffffffff)
 
 if idx == 0:
 print(v0,v1)
 
 sum_val = np.uint32(sum_val - 239350328) & np.uint32(0xffffffff)

 # 存储结果到输出数组
 output[start] = v0 & 0xff
 output[start + 1] = (v0 >> 8) & 0xff
 output[start + 2] = (v0 >> 16) & 0xff
 output[start + 3] = (v0 >> 24) & 0xff
 output[start + 4] = v1 & 0xff
 output[start + 5] = (v1 >> 8) & 0xff
 output[start + 6] = (v1 >> 16) & 0xff
 output[start + 7] = (v1 >> 24) & 0xff
 

@cuda.jit
def tea_decrypt_cuda(TEA_KEY_GLOBAL, data, output, rounds):
 idx = cuda.grid(1) # 全局线程索引
 if idx < 32: # 32 个 8 字节块
 # 计算每个线程的偏移
 start = idx * 8

 # 加载 v0 和 v1 (小端序)
 v0 = np.uint32(data[start] | (data[start + 1] << 8) | 
 (data[start + 2] << 16) | (data[start + 3] << 24))
 v1 = np.uint32(data[start + 4] | (data[start + 5] << 8) | 
 (data[start + 6] << 16) | (data[start + 7] << 24))

 # 初始化 sum 为 uint32
 sum_val = np.uint32(((-239350328 * (10485760 // 8))) & 2 ** 32 -1)

 # 主循环：每次 8 轮
 for _ in range(rounds // 8):
 for _ in range(8): # 模拟 tea_encrypt 的 8 轮
 v1 = np.uint32(v1 - (((v0 << 4) + TEA_KEY_GLOBAL[2]) ^ 
 (v0 + sum_val) ^ ((v0 >> 5) + TEA_KEY_GLOBAL[3]))) & np.uint32(0xffffffff)
 v0 = np.uint32(v0 - (((v1 << 4) + TEA_KEY_GLOBAL[0]) ^ 
 (v1 + sum_val) ^ ((v1 >> 5) + TEA_KEY_GLOBAL[1]))) & np.uint32(0xffffffff)
 
 sum_val = np.uint32(sum_val - 0x9E3779B9) & np.uint32(0xffffffff)
 if idx == 0:
 print(v0,v1)
 
 sum_val = np.uint32(sum_val + 239350328) & np.uint32(0xffffffff)

 # 存储结果到输出数组
 output[start] = v0 & 0xff
 output[start + 1] = (v0 >> 8) & 0xff
 output[start + 2] = (v0 >> 16) & 0xff
 output[start + 3] = (v0 >> 24) & 0xff
 output[start + 4] = v1 & 0xff
 output[start + 5] = (v1 >> 8) & 0xff
 output[start + 6] = (v1 >> 16) & 0xff
 output[start + 7] = (v1 >> 24) & 0xff

def tea_encrypt_cuda_host(data, rounds=10485760, threads_per_block=32):
 """
 使用 CUDA 加速的 TEA 加密。
 :param data: 输入字节数组 (256 字节)
 :param rounds: 总轮数 (默认 10485760)
 :param threads_per_block: 每个块的线程数
 :return: 加密后的字节数组
 """
 # if len(data) != 256:
 # raise ValueError("Data must be exactly 256 bytes")

 # 转换为 NumPy 数组并传输到 GPU
 data_np = np.array(list(data), dtype=np.uint8)
 data_device = cuda.to_device(data_np)
 output_device = cuda.device_array_like(data_np)

 # 计算网格和块配置
 blocks = 1 # 固定 32 个线程，1 个块足够
 tea_encrypt_cuda[blocks, threads_per_block](TEA_KEY_GLOBAL, data_device, output_device, rounds)

 # 将结果拷贝回 CPU
 result = output_device.copy_to_host()
 return bytes(result)

def tea_decrypt_cuda_host(data_, rounds=10485760, threads_per_block=32):
 """
 使用 CUDA 加速的 TEA 加密。
 :param data: 输入字节数组 (256 字节)
 :param rounds: 总轮数 (默认 10485760)
 :param threads_per_block: 每个块的线程数
 :return: 加密后的字节数组
 """
 print("data_:",len(data_))
 res = b''
 for index in range(0,len(data_),256):
 # print(index)
 data = data_[index:index+256]
 # print(len(data))
 if len(data) != 256:
 raise ValueError("Data must be exactly 256 bytes")

 # 转换为 NumPy 数组并传输到 GPU
 data_np = np.array(list(data), dtype=np.uint8)
 data_device = cuda.to_device(data_np)
 output_device = cuda.device_array_like(data_np)

 # 计算网格和块配置
 blocks = 1 # 固定 32 个线程，1 个块足够
 tea_decrypt_cuda[blocks, threads_per_block](TEA_KEY_GLOBAL, data_device, output_device, rounds)

 # 将结果拷贝回 CPU
 result = output_device.copy_to_host()
 res += bytes(result)
 return res

# 测试代码
if __name__ == "__main__":
 data = bytes([150, 4, 235, 182, 108, 114, 166, 121, 74, 204, 139, 106, 35, 137, 56, 11, 217, 104, 176, 195, 147, 190, 119, 62, 37, 23, 23, 196, 174, 33, 65, 64, 190, 149, 92, 135, 185, 41, 15, 137, 3, 0, 216, 54, 119, 105, 150, 80, 15, 82, 236, 171, 254, 251, 74, 47, 141, 246, 159, 206, 226, 2, 67, 177, 82, 3, 1, 248, 111, 207, 190, 158, 6, 98, 248, 144, 237, 201, 249, 159, 139, 115, 242, 169, 7, 175, 67, 189, 67, 181, 203, 232, 20, 38, 5, 51, 117, 8, 113, 113, 30, 117, 148, 167, 77, 18, 132, 68, 104, 105, 97, 6, 186, 137, 70, 190, 105, 4, 183, 136, 113, 11, 170, 151, 58, 152, 114, 55, 78, 128, 86, 82, 17, 239, 59, 145, 109, 224, 85, 158, 187, 215, 122, 153, 25, 137, 188, 161, 126, 51, 168, 103, 155, 54, 86, 46, 76, 230, 182, 30, 0, 151, 188, 48, 66, 13, 217, 209, 37, 70, 204, 53, 135, 132, 213, 253, 23, 11, 29, 96, 86, 18, 49, 76, 215, 94, 99, 127, 133, 165, 176, 189, 253, 238, 221, 55, 110, 147, 9, 153, 48, 126, 37, 142, 242, 60, 109, 205, 93, 67, 94, 75, 53, 137, 22, 147, 160, 171, 234, 145, 173, 169, 161, 142, 152, 120, 122, 170, 192, 70, 99, 82, 239, 149, 74, 209, 38, 155, 245, 228, 188, 53, 14, 68, 104, 240, 5, 57, 139, 112, 36, 215, 222, 101, 73, 65])

 print("Original:", data.hex()[:32], "...")
 encrypted = tea_encrypt_cuda_host(data) 
 # print("Encrypted:", encrypted.hex(), "...")
 # for num in encrypted:
 # print(f'{num:02x}',end=' ')

 dec = tea_decrypt_cuda_host(encrypted)
 for num in dec:
 print(f'{num:02x}',end=' ')
 assert data == dec
```



```
from cudagift5 import tea_decrypt_cuda_host
from gift34 import decrypt_exchange
from cuda_gift1 import decrypt_stage1
from gift2 import rev_gift2

with open("flag_enc",'rb') as f:
 enc = f.read()

print(len(enc))
# xor thread id
enc_xor = []
for i in range(len(enc)):
 enc_xor.append(enc[i] ^ (i % 256))
print("gift 6")

# rev gift5
enc = bytes(enc_xor)
dec = tea_decrypt_cuda_host(enc)
print("gift 5")

with open("flag_gift5",'wb') as f:
 f.write(dec)

# with open("flag_gift5",'rb') as f:
# dec = f.read()

# rev gift34
enc = list(dec)
dec = decrypt_exchange(enc)
print("gift 34")

#rev gift2
enc = dec
dec = rev_gift2(enc)
print("gift 2")

# rev gift1
enc = bytes(dec)
dec = decrypt_stage1(enc)
print("gift 1")

with open("flag.dec",'wb') as f:
 f.write(bytes(dec))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-5d75510a3f605e1cf3862d52a0dbde36.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-5d75510a3f605e1cf3862d52a0dbde36.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-5f2ca628d0031306ca2173d8af29e181.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-71612baea187590d75a96ee2368782fc.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-7b3fd9ae39f478f9de03e8b5700c3f91.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-7b3fd9ae39f478f9de03e8b5700c3f91.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-7b3fd9ae39f478f9de03e8b5700c3f91.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-5d80cff1be9ef61d0df3aa0fbe25c7e3.gif)