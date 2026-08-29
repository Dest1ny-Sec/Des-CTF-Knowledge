---
title: Aliyun 2025 easy-cuda-rev - PTX 汇编 + CUDA 加速
contest: AliyunCTF
year: 2025
difficulty: hard
vuln_type: reverse
tags: [CUDA, PTX, sm_52, cuobjdump, AES T-table, ROT循环, mov.u64 %SPL __local_depot0, vprintf, encrypt_kernel, GPU加速, 10M轮异或]
attack_chain:
  - cuobjdump -ptx easy_cuda 提取 PTX 汇编
  - arch=sm_52, code version=[8,0], compressed
  - T[256] AES T-table (S-box + MixColumns)
  - RT[256] 逆 T-table
  - encrypt_kernel 入口 mov.u64 %SPL, __local_depot0 + cvta.local.u64 %SP
  - 字节处理: ld.global.u8 读 input[i], XOR ((i*73 + key) & 0xFF), 4-bit swap (AND 0xF0, SHL 4, SHR 4, OR)
  - 5 段循环每段 10485760 轮查 T-table, 每轮 XOR 轮计数器
  - 最后 st.global.u8 写回, vprintf("gift%d", byte)
  - vprintf 调用 mov.u64 %rd42, $str; cvta.global.u64; call.uni vprintf
  - GPU 加速爆破 5 段独立循环, 倒数逆向
key_payload: 'cuobjdump -ptx / sm_52 / encrypt_kernel / 5x10485760 轮 / T-table 查表 / 4-bit swap / XOR (i*73+key) / vprintf gift'
one_liner: Aliyun 2025 easy-cuda-rev — CUDA PTX 汇编 sm_52 + 5 段 10485760 轮 T-table 查表 + 4-bit swap + XOR 索引 + GPU 加速爆破 + vprintf 逐字节输出。
lesson: CUDA reverse 用 cuobjdump -ptx 提汇编;__local_depot0 是 per-thread local memory;vprintf 调 call.uni 输出来看 gift1/gift2/gift3/gift4/gift5 分段结果。
quality: high
---

# Aliyun 2025 easy-cuda-rev - PTX 汇编 + CUDA 加速

## 速读
AliyunCTF 2025 — easy-cuda-rev GPU 加密逆向题。

## PTX 提取
```bash
cuobjdump -ptx easy_cuda > test.txt
# arch=sm_52 code=[8,0] compressed
```

## 关键 PTX
```ptx
.visible .entry _Z14encrypt_kernelPhh(
.param .u64 _Z14encrypt_kernelPhh_param_0,  ; uint8_t* data
.param .u8 _Z14encrypt_kernelPhh_param_1   ; uint8_t key
)
{
    .local .align 8 .b8 __local_depot0[8];
    .reg .b64 %SP;
    .reg .b64 %SPL;
    
    mov.u64 %SPL, __local_depot0;
    cvta.local.u64 %SP, %SPL;
    ld.param.u8 %rs12, [param_1];  ; key
    ld.param.u64 %rd19, [param_0]; ; data ptr
    
    ; tid = blockIdx.x * blockDim.x + threadIdx.x
    mov.u32 %r1, %ntid.x;
    mov.u32 %r54, %ctaid.x;
    mul.lo.s32 %r2, %r54, %r1;
    mov.u32 %r3, %tid.x;
    add.s32 %r4, %r2, %r3;
    
    ld.global.u8 %rs13, [%rd3];
    cvt.u16.u32 %rs14, %r4;
    mul.lo.s16 %rs15, %rs14, 73;       ; i * 73
    add.s16 %rs16, %rs15, %rs12;       ; (i*73) + key
    xor.b16 %rs17, %rs13, %rs16;       ; byte XOR (i*73+key)
    ; 4-bit swap
    and.b16 %rs18, %rs17, 240;
    shr.u16 %rs19, %rs18, 4;
    shl.b16 %rs20, %rs17, 4;
    or.b16 %rs58, %r19, %r20;
    
    ; 5 段循环查 T[256] 表
    mov.u32 %r242, 0;
loop_1:
    cvt.u64.u16 %rd22, %rs58;
    and.b64 %rd23, %rd22, 255;
    add.s64 %rd25, %rd24, %rd23;
    ld.const.u8 %rs21, [T + %rd23];
    shr.u16 %rs22, %rs21, 4;
    shl.b16 %rs23, %rs21, 4;
    or.b16 %rs24, %r22, %r23;
    cvt.u16.u32 %rs25, %r242;
    xor.b16 %rs58, %r24, %r25;
    add.s32 %r242, %r242, 1;
    setp.lt.u32 %p2, %r242, 10485760;
    @%p2 bra loop_1;
    ; ... 4 more loops
    
    st.global.u8 [%rd3], %rs58;
    
    ; vprintf 输 gift1/gift2/gift3/gift4/gift5
}
```

## 输出
- `$str[8] = "gift1:\n\0"`
- `$str$1[6] = "%02x \0"`
- vprintf "gift1: %02x " 逐字节输出
