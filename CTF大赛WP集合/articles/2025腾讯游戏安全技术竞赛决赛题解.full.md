---
title: 2025 腾讯游戏安全技术竞赛 - 决赛题解
contest: 腾讯游戏安全
year: 2025
difficulty: hard
vuln_type: reverse
tags:
- VT抗分析
- KdDisableDebugger
- kdcom.dll检测
- MSR hook
- 单表替换
- VT hook TEA
- rdmsr(0xE8)
- 异或key依赖flag长度
- Unicorn模拟
- NtQuerySystemInformation
- 栈回溯检测
- RtlWalkFrameChain
- dfs变种+记忆化
attack_chain:
- kdcom.dll 模块存在性检测 → hook NtQuerySystemInformation 把 Name[0] 改 'x' 隐藏
- KdDisableDebugger 后台线程调用 → 驱动层直接 return 阻断
- 读 flag 后做单表替换 (VT 实现, hook+0x95DF)
- 用 key XOR flag 加密
- 启用 VT 用 hook 过的 TEA 加密上一步密文
- 改 rdmsr(0xE8) 行为, 在 check 前 XOR 一个由 flag 长度决定的 key
- 'XSafe 驱动+二次加载: 用 XSafe.sys 加载, XSafe2.sys 用于定位 TEA 函数 dump enc.bin'
- 'VT-Detection1: MSR 检测源码'
- 'VT-Detection2: 真机专属检测'
- 'exp.py 还原 TEA 加密: Unicorn 跑 0xFFFFF806FF8D9F0C..0xFFFFF806FF8DA05C 提取栈明文'
- 'dfs 变种: f[x][y] = x%5 + dfs(x-1,y) + dfs(x-1,y-1); dfs(44,22)=7039739125714'
key_payload: '''kdcom.dll 检测 + KdDisableDebugger + VT hook TEA + rdmsr(0xE8) 异或 + Unicorn 模拟还原明文'''
one_liner: Windows 内核 VT 抗分析 — kdcom.dll 检测 + KdDisableDebugger + VT hook TEA + MSR(0xE8) 异或 + Unicorn 模拟还原 + dfs(44,22) 记忆化变种。
lesson: 抗分析是分层叠加：模块名检测 + 调试 API 检测 + VT 虚拟化 + 硬件断点检测；XSafe 双驱动配合可定位+dump 被保护函数 enc.bin；Unicorn 模拟内核函数可旁过 anti-dump。
quality: high
full_path: 2025腾讯游戏安全技术竞赛决赛题解.full.md
meta_path: 2025腾讯游戏安全技术竞赛决赛题解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2025 腾讯游戏安全技术竞赛 - 决赛题解。Windows 内核 VT 抗分析 — kdcom.dll 检测 + KdDisableDebugger + VT hook TEA + MSR(0xE8) 异或 + Unicorn 模拟还原 + dfs(44,22) 记忆化变种。。关键路径：kdcom.dll 模块存在性检测 → hook NtQuerySystemInformation 把 ...
category: reverse
subcategory: reverse
tools_used:
- Python
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/239238.html
reasoning_chain:
- 触发点：kdcom.dll 模块存在性检测 → 假设：检测到 kdcom 就 'ACE' 蓝屏 → 动作：hook NtQuerySystemInformation 把 kdcom.Name[0] 改 'x' 隐藏
- 观察：kdcom 检测绕过 → 下一步：后台线程 KdDisableDebugger → 假设：驱动层直接 return 阻断
- 动作：驱动 hook KdDisableDebugger → 下一步：读 flag → VT hook +0x95DF 做单表替换
- 下一步：用 key XOR flag 单表替换 → 假设：输入 key + 已 hook 过的 TEA 加密上一步密文
- 触发点：VT hook rdmsr(0xE8) → 在 check 前 XOR 一个 key → 观察：key 由 flag 长度决定 → 假设：未 hook 直接动态改行为
- 触发点：XSafe.sys + XSafe2.sys 双驱动 → 假设：XSafe 后加载 + XSafe2.sys 定位 TEA 函数 dump enc.bin → 下一步：exp.py Unicorn 模拟
- 下一步：Unicorn 跑 0xFFFFF806FF8D9F0C..0xFFFFF806FF8DA05C → hook 0xA05C 处读 RSP+0xE0 栈明文
- 触发点：dfs 变种 f[x][y] = x%5 + dfs(x-1,y) + dfs(x-1,y-1) → 假设：dfs(44,22) 记忆化 → 动作：结果 = 7039739125714
failed_attempts:
- 试图在 R3 用 IDA 直接调内核函数 → 失败：必须 Unicorn 模拟或 XSafe 双驱动配合
- 试图放弃 hook kdcom 检测 → 失败：原程序读到 kdcom 直接蓝屏
- 试图手解 TEA 算法 → 失败：必须 Unicorn 跑原函数 dump 栈
key_observations:
- 抗分析分层叠加：模块名检测 + 调试 API 检测 + VT 虚拟化 + 硬件断点检测
- XSafe 双驱动配合可定位+dump 被保护函数 enc.bin
- Unicorn 模拟内核函数可旁过 anti-dump
- RtlWalkFrameChain 栈回溯检测 Hook 范围内地址是高级反 hook
- dfs 变种记忆化：f[x][y] = x%5 + dfs(x-1,y) + dfs(x-1,y-1)
prerequisites:
- Windows 内核 VT 抗分析原理
- kdcom.dll + KdDisableDebugger 调试 API
- XSafe 双驱动设计 + IOCTL
- Unicorn CPU 模拟器使用
---
# 2025腾讯游戏安全技术竞赛决赛题解

> 原文: https://www.ctfiot.com/239238.html
> ID: 239238

作者论坛账号：xia0ji233

：还没走过。

：已经往左走过。

：已经往左走过，且已经往左下走过。

题目检测 kdcom.dll 模块，检测到则直接 'ACE' 蓝屏。

题目有个线程一直在调用，KdDisableDebugger

对于第一个检测，把蓝屏函数直接返回即可。

对于第二个检测，把该api直接返回即可。

读取 flag 之后，先做一次单表映射的替换，这里是由 VT 实现的，hook点在（+0x95DF）

用输入的 key 对输入的 flag 进行异或加密。

开启 VT，使用 VT hook 过的 TEA 加密逻辑加密上一步得到的密文。

用VT hook rdmsr，使得 rdmsr(0xE8) 在 check 之前异或了一个密钥，这个密钥由输入的 flag 长度决定。

XSafe：包含驱动的源码，编译之后先加载该驱动，后加载题目给的驱动，配置正确的情况下可以双机调试且成功加载驱动（无法二次加载及卸载）。

XSafe.sys：XSafe编译的二进制文件。

XSafe2：包含爆破 TEA 加密爆破的源码，需要借助驱动 1 找到 TEA 函数的具体位置，并且根据输出的内存地址手动 dump 文件，得到 enc.bin。

XSafe2.sys：XSafe2编译的二进制文件

VT-Detection1：包含方法1所述的MSR检测源码，加载时可以判断当前是否处于题目的 VT hook 环境中，虚拟机和真机均有效。

VT-Detection1.sys：VT-Detection1编译的二进制文件

VT-Detection2：包含方法2所属的检测方法，只在真机有效。

VT-Detection2.exe：VT-Detection2编译的二进制文件

enc.bin：由 XSafe2.sys dump 分配的内存文件。

exp.py：TEA 加密的还原脚本

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码 隐藏代码
import idaapi
import idc
from unicorn import *
from unicorn.x86_const import *
import ida_name
import mmap
import sys
import idautils
import struct
base_addr = idaapi.get_imagebase()
fix_function_start=0xFFFFF806FF8D9F0C
fix_function_end=0xFFFFF806FF8DA05F
PAGE_SIZE=0x1000
RSP=0xdead0000
RBP=0xdead0000
map_addr=idaapi.get_imagebase()
offset=base_addr-map_addr
defhook_mem_unmapped(uc, access, address, size, value, user_data):
    aligned_addr = address&0xFFFFFFFFFFFFF000
    try:
        uc.mem_map(aligned_addr, PAGE_SIZE)
        data=idaapi.get_bytes(aligned_addr,PAGE_SIZE)
        uc.mem_write(aligned_addr,data)
        returnTrue
# 表示错误已处理，继续执行
    
except Exception as e:
        print(f"[-] 动态映射内存页失败: {e}")
        returnFalse

instr_count = 0
cnt=0
defhook_code(uc, address, size, user_data):
    global instr_count,cnt
    instr_count += 1
    rax=uc.reg_read(UC_X86_REG_RAX)
    rcx=uc.reg_read(UC_X86_REG_RCX)
    rdx=uc.reg_read(UC_X86_REG_RDX)
    r8=uc.reg_read(UC_X86_REG_R8)
    r9=uc.reg_read(UC_X86_REG_R9)
    r10=uc.reg_read(UC_X86_REG_R10)
    rbp=uc.reg_read(UC_X86_REG_RBP)
    rsp=uc.reg_read(UC_X86_REG_RSP)
    rip=uc.reg_read(UC_X86_REG_RIP)
    if rip==0xFFFFF806FF8DA05C:
        st=b''
        offset=0xE0
        whileTrue:
            if uc.mem_read(rsp+offset,2)==b'x00x00':
                break
            st+=uc.mem_read(rsp+offset,1)
            offset+=2
        print(st)
        #print(uc.mem_read(rsp+offset))

mu = Uc(UC_ARCH_X86, UC_MODE_64)
mu.reg_write(UC_X86_REG_RIP, fix_function_start)  # 设置执行起始地址
mu.reg_write(UC_X86_REG_R13, 0xFF)
mu.reg_write(UC_X86_REG_RSP, RSP)
mu.reg_write(UC_X86_REG_RBP, RBP)
mu.mem_map(RSP-PAGE_SIZE,PAGE_SIZE*2)
mu.hook_add(UC_HOOK_MEM_FETCH_UNMAPPED, hook_mem_unmapped)
mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED, hook_mem_unmapped)
mu.hook_add(UC_HOOK_MEM_WRITE_UNMAPPED, hook_mem_unmapped)
mu.hook_add(UC_HOOK_CODE, hook_code)
instr_count=0
print(hex(mu.reg_read(UC_X86_REG_RIP)))
try:
    mu.emu_start(fix_function_start,fix_function_end)
except UcError as e:
    print(e)
    pass
复制代码 隐藏代码
NTSTATUS gh_NtQuerySystemInformation(...)
{
    unhook();
    auto ret = ((NtQuerySystemInformation_t)(TargetFunction))(...);
    if (SystemInformationLength&& SystemInformationClass== SystemModuleInformation) {
        PSYSTEM_MODULE_INFORMATION pModInfo = (PSYSTEM_MODULE_INFORMATION)SystemInformation;
        for (int i = 0; i < pModInfo->ModulesCount; i++) {
            PSYSTEM_MODULE_INFORMATION_ENTRY pEntry = &pModInfo->Modules[i];
            if (strcmp(pEntry->Name + pEntry->NameOffset, "kdcom.dll")) {
                (pEntry->Name + pEntry->NameOffset)[0] = 'x';
            }
        }
    }
    rehook();
    return ret;
}
复制代码 隐藏代码
struct deque
{
    void *vtable;
    data **map;
    __int64 MAX_SIZE;
    __int64 begin_idx;
    __int64 size;
};
struct data
{
    int x1;
    int y1;
    _QWORD data2;
    _QWORD data3;
    int x4;
    int y4;
};
复制代码 隐藏代码
    #include<stdio.h>
    #include<string.h>
int v[50][50];
longlong f[50][50];
longlongdfs(int x, int y) {
    if (x == y || !y)return1;
    if (f[x][y] != -1)return f[x][y];
    return f[x][y] = x%5+dfs(x-1,y)+dfs(x-1,y-1);
}

intmain() {
    memset(f, -1, sizeof(f));
    printf("%lldn", dfs(44,22));
}
//7039739125714
复制代码 隐藏代码
NTSTATUS gh_NtQuerySystemInformation(...)
{
    unhook();
    //...
    PVOID stack[MAX_BACKTRACE_DEPTH+1] = { 0 };
    RtlWalkFrameChain(stack, MAX_BACKTRACE_DEPTH,0);
    bool flag = 0;
    staticint cnt = 0;
    for(int i = 0; i < MAX_BACKTRACE_DEPTH; i++) {
        if(stack[i]>= Hooks::
Base && stack[i] <= (PVOID)((UINT64)Hooks::
Base + Hooks::
Size)) {
            flag = 1;
            break;
        }
    }
    if (flag) {
        char code = 0xC3;
        cnt += 1;
        if (cnt == 3) {
            DriverUtil::
MDLWriteMemory((PVOID)((UINT64)Hooks::
Base + 0x74f0), &code, 1);
            DriverUtil::
MDLWriteMemory((PVOID)(KdDisableDebugger), &code, 1);
            return ret;
        }
    }
    rehook();
    return ret;
}
复制代码 隐藏代码
typedef VOID(*TEAEnc)(unsigned int*, unsigned int*);
extern"C" NTSTATUS DriverEntry(
    _In_ PDRIVER_OBJECT  DriverObject,
    _In_ PUNICODE_STRING RegistryPath
) {
    DriverObject->DriverUnload = DriverUnload;

    TEAEnc teaEnc = (TEAEnc)0xFFFFF8032AC51560;
    unsignedint key[4] = { 0x00000089, 0x000000FE, 0x00000076, 0x000000A0 };
    unsignedint data[2] = { 0x00000000, 0x00000000 };
    teaEnc((unsignedint*)data, (unsignedint*)key);
    for(int i = 0; i < 8; i++) {
        DBG_PRINT("data[%d]=%02xn", i,((unsignedchar*)data)[i]);
    }
    return STATUS_SUCCESS;
}
复制代码 隐藏代码
target=b'xc0x6dxdax3fxc9x8dx05xffx56x62x69x55x6cxbbxa4x90x57xa0xa6x82xfbxa7x8exe7x69x52xf3xc9xf1xd7x1ax88xfdx7bxeaxa9x91x95xe4x02xc5xddxe7xf6x64xcbx0ex88xd9xd2x4ex1ex3bxaex27x64x2dxfdxcax5cx1cx7bxccxd0xe7x40x6ex5exefxa9x5dx8axd3x5dx42xfax72x9ax1bx30x2fxddx72xc2xe5xf3x1cx9bxa4xf0x3bx91xe8x3bxc8x4ex1fx8ax40x09xf8x6bx7bxb4x8bx42x1dx71x81x43xacxb9x76x42x56x05x5fxf1xeex5dx7ax2cxfex48x92x7dx5ax41x93xd1x4ax47x32xb8x98xa1'
table=open("./enc.bin","rb").read()
for i in range(0,136,8):
    num = table.find(target[i:i+8])//8
    x=num//256
    y=num%256
    print(f"{x:
02x} {y:
02x}",end=" ")
复制代码 隐藏代码
f6 59 ab d7 ea 1894 ab d457 b1 d484c6f0d4534e 3281 bc 86c3321b 5b f56784c30596c6 01
复制代码 隐藏代码
bool is_vt_enabled1()
{
    constunsignedint IA32_FEATURE_CONTROL = 0x3A;
    unsignedlonglong msr_val = __readmsr(IA32_FEATURE_CONTROL);
    return (msr_val & (1 << 2)) != 0; // VMX outside SMX enabled
}
if (is_vt_enabled1()) {
    DBG_PRINT("VT1 is enabledn");
}
else {
    DBG_PRINT("VT1 is not enabledn");
}
复制代码 隐藏代码
bool is_vt_enabled1()
{
    LARGE_INTEGER freq; // 获取频率
    LARGE_INTEGER start = KeQueryPerformanceCounter(&freq);
    constunsignedint IA32_FEATURE_CONTROL = 0x3A;
    unsignedlonglong msr_val;
    for (int i = 0; i < 100000; i++){
        msr_val = __readmsr(IA32_FEATURE_CONTROL);
    }
    LARGE_INTEGER end = KeQueryPerformanceCounter(NULL);
    LONGLONG delta = end.QuadPart - start.QuadPart;
    LONGLONG elapsed_us = (delta * 1000) / freq.QuadPart;
    DBG_PRINT("Elapsed time: %lld msn", elapsed_us); // 打印经过的时间
    return (msr_val & (1 << 2)) != 0; // VMX outside SMX enabled
}
复制代码 隐藏代码
start = KeQueryPerformanceCounter(NULL);
int a = 1;
int* k = &a;
for (int i = 0; i < 100000000; i++) {
    *k *= 3;
}
end = KeQueryPerformanceCounter(NULL);
delta = end.QuadPart - start.QuadPart;
LONGLONG elapsed_us2 = (delta * 1000) / freq.QuadPart;
DBG_PRINT("Elapsed time: %lld msn", elapsed_us2); // 打印经过的时间
复制代码 隐藏代码
bool is_vt_enabled1()
{
    LARGE_INTEGER freq; // 获取频率
    LARGE_INTEGER start = KeQueryPerformanceCounter(&freq);
    constunsignedint IA32_FEATURE_CONTROL = 0x3A;
    unsignedlonglong msr_val;
    for (int i = 0; i < 100000; i++){
        msr_val = __readmsr(IA32_FEATURE_CONTROL);
    }
    LARGE_INTEGER end = KeQueryPerformanceCounter(NULL);
    LONGLONG delta = end.QuadPart - start.QuadPart;
    LONGLONG elapsed_us1 = (delta * 1000) / freq.QuadPart;
    DBG_PRINT("Elapsed time: %lld msn", elapsed_us1); // 打印经过的时间
    start = KeQueryPerformanceCounter(NULL);
    int a = 1;
    int* k = &a;
    for (int i = 0; i < 100000000; i++) {
        *k *= 3;
    }
    end = KeQueryPerformanceCounter(NULL);
    delta = end.QuadPart - start.QuadPart;
    LONGLONG elapsed_us2 = (delta * 1000) / freq.QuadPart;
    DBG_PRINT("Elapsed time: %lld msn", elapsed_us2); // 打印经过的时间
    return elapsed_us1 / elapsed_us2 > 5;
}
复制代码 隐藏代码
bool check_invalid_leaf()
{
    constexprunsignedint invalid_leaf = 0x04201337;
    constexprunsignedint valid_leaf   = 0x40000000;

    _cpuid_buffer_t InvalidLeafResponse = {};
    _cpuid_buffer_t ValidLeafResponse   = {};

    __cpuid(reinterpret_cast(&InvalidLeafResponse), invalid_leaf);
    __cpuid(reinterpret_cast(&ValidLeafResponse), valid_leaf);

    if ((InvalidLeafResponse.EAX != ValidLeafResponse.EAX) ||
        (InvalidLeafResponse.EBX != ValidLeafResponse.EBX) ||
        (InvalidLeafResponse.ECX != ValidLeafResponse.ECX) ||
        (InvalidLeafResponse.EDX != ValidLeafResponse.EDX))
        returntrue;

    returnfalse;
}
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