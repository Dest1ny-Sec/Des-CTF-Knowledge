---
title: 腾讯游戏安全大赛初赛题解
contest: 腾讯游戏安全
year: 2023
difficulty: medium
vuln_type: reverse
tags:
- Base64
- contest-txt
- plaintext-extraction
- CE-Memory-View
- inline-hook
- VirtualProtect
- DLL-inject
- WriteProcessMemory
- T-contest
- unhook-ZwProtectVirtualMemory
attack_chain:
- 'Q1 找明文: 64 位 Windows10 + contest.exe + 写 contest.txt'
- '密文: ImVkImx9JG12OGtlImV+'
- 用 Cheat Engine memory view 找 contest.txt 字符串
- '找 base 表地址 7FF713657190: QRSTUVWXYZabcdefABCDEFGHIJKLMNOPwxyz0123456789+/ghijklmnopqrstuv'
- base64 解密得 catchmeifyoucan (明文)
- 'Q2 改内存让密文改明文:'
- base64 三原文对应四密文规则
- 右移两位查表 = 第一密文 → NOP 掉 contest.exe+BA39~BA41
- and 0x3f = 第四密文 → NOP 掉 contest.exe+B9FD~BA04
- 第三项目 BA5D~BA68 NOP 掉
- mov [r14],al + add r14,0 (不递增 r14) → BA05 起始
- VirtualProtect 被 inline hook → 修复 ZwProtectVirtualMemory
- VirtualProtectEx + WriteProcessMemory PATCH 内存
- 远程线程注入 DLL → LoadLibraryA → DllMain → patch()
key_payload: '''NOP contest.exe+BA39~BA41/B9FD~BA04/BA5D~BA68 + BA05 mov [r14],al + add r14,0 + DLL inject'''
one_liner: 腾讯游戏安全初赛：CE 找 base64 表 + 找明文 + DLL 注入 PATCH 内存让 Base64 密文改明文，NOP 关键指令 + 修复 inline hook。
lesson: Windows inline hook 修复是高级游戏安全技术；DLL 注入 + WriteProcessMemory 是游戏外挂标配。
quality: high
full_path: 腾讯游戏安全大赛初赛题解.full.md
meta_path: 腾讯游戏安全大赛初赛题解.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '腾讯游戏安全大赛初赛题解。腾讯游戏安全初赛：CE 找 base64 表 + 找明文 + DLL 注入 PATCH 内存让 Base64 密文改明文，NOP 关键指令 + 修复 inline hook。。关键路径：Q1 找明文: 64 位 Windows10 + contest.exe + 写 contest.txt → 密文: ImVkImx9JG12OGtlImV+ → 用 Cheat E...'
category: reverse
subcategory: reverse
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/115172.html
reasoning_chain:
- 触发点：contest.exe 写 contest.txt 含 base64 密文 → 假设：找明文 flag
- 动作：CE Memory View 找 contest.txt 明文 → 观察：找到 catchmeifyoucan
- 假设：base64 表被改 → 动作：CE 找访问密文地址 → 观察：找到 base64 表
- 触发点：base64 表 QRSTUVWXYZabcdefABCDEFGHIJKLMNOPwxyz0123456789+/ghijklmnopqrstuv
- 动作：用自定义 base64 表解 ImVkImx9JG12OGtlImV+ → 观察：catchmeifyoucan
- 触发点：WriteProcessMemory 写内存 → 假设：PATCH 内存让密文变明文
- 动作：NOP 三个代码段 BA39-B9FD-BA5D → 观察：contest 输出明文
- 假设：VirtualProtect 被 hook → 动作：先 VirtualProtectEx 远程 + WriteProcessMemory 修复
- 假设：远程线程注入 LoadLibraryA → 动作：OpenProcess + VirtualAllocEx + CreateRemoteThread
failed_attempts:
- 直接改 contest.txt → 失败：exe 重写文件
- 解密 base64 用标准表 → 失败：表被改
- 直接 NOP 关键指令 → 失败：被 anti-cheat 检测
key_observations:
- base64 自定义表 QRSTUVWXYZabcdefAB... 是游戏安全常见混淆
- contest.exe 三段 NOP + add r14,0 = 输出明文
- WriteProcessMemory 远程 + VirtualProtectEx 绕 hook 是注入标配
- cheat engine 找密文访问基址（r14 寄存器）
prerequisites:
- Cheat Engine 内存查看 + 反汇编
- base64 表自定义
- inline hook 修复
- CreateRemoteThread + LoadLibraryA 注入
---
# 腾讯游戏安全大赛初赛题解

> 原文: https://www.ctfiot.com/115172.html
> ID: 115172

1.在64位Windows10系统上运行contest.exe, 找到明文的信息，作为答案提交（1分）。

答案：catchmeifyoucan

正常运行会在当前目录下的 contest.txt 去写入一个ImVkImx9JG12OGtlImV+。

CE打开，先通过CE的memory view找到一串一直在变化的内存。

虽然不确定，找到了 contest.txt 这个明文，但是catchmeifyoucan不确定它是不是flag，还得进一步确定，于是查找是谁访问了这个地址。

在第三项中，发现后面有一个读取r10所指示的内存的操作。

同样memory view查找7FF713657190地址，结果找到一串 base 表：

QRSTUVWXYZabcdefABCDEFGHIJKLMNOPwxyz0123456789+/ghijklmnopqrstuv

于是果断拿密文解密，发现得到了正确答案。

2.编写程序，运行时修改尽量少的contest.exe内存，让contest.exe 由写入密文信息变为写入明文信息成功。（满分2分）

Base64编码的一组中，三个原文对应四个密文。第一个密文和第四个密文只会被原文第一个字符和第三个字符影响。第二个字符会被第一个原文和第二个原文字符影响，第三个字符会被第二个原文和第三个原文字符影响。

对 base 表进行访问查询，找到三个地址，对三个地址分析。

查看第一项访问地址

右移两位进行查表，很明显就是对第一个密文的操作，因此把中间的操作全部NOP，只剩读取和写入操作。

再对第二个项目分析，很明显看到了对第四个密文的操作：

这里的and 0x3f就是取得最低的六位，很明显是最后一位，同样也把中间的指令全部NOP掉。

不仅如此，同时注意到赋值的时候，对 r14+1了，并且r14的值在后面+1。这里有一个很头疼的点就是明文密文长度不一致，三个原文对应四个密文，因此这里可以为这个点考虑起来了。如果我 r14 的值不给他 +1，直接给 r14 的值赋值，结果会怎样呢？也就是对应指令修改为：

mov [r14],al
add r14,0

发现输出文件的内容果然变短了。

并且此时，我们再处理中间的一位，就能得到明文输出了。

我们来看第三个项目：

这里同样把 BA5D-BA68的代码段NOP掉，做完之后，发现contest输出明文了。

总结一下：

◆contest.exe+BA39~BA41 全部NOP掉

◆contest.exe+B9FD~BA04 全部NOP掉

◆contest.exe+BA5D~BA68 全部NOP掉

◆contest.exe+BA05开始，把指令变成：

mov [r14],al
add r14,0

编写dll进行一次性修改：

但是在写内存的时候，发现VirtualProtect一直调用失败，拿火绒剑扫了一下，发现VirtualProtect被下了钩子。

尝试修复一下这个钩子，写一个注入器和dll。

DLL不能直接使用 VirtualProtect 去修改内存属性，所以我们需要在注入之前，使用VirtualProtectEx先修改内存权限，再通过WriteProcessMemory函数修复程序在API处下的一个钩子，这里是inline hook，因此直接遍历模块寻找ZwProtectVirtualMemory函数把钩子取消。

取消之后，即可使用远程线程注入的方式去注入dll，远程注入的思路就是开辟一块远程内存，写入dll路径，创建远程线程回调LoadLibraryA函数去加载 DLL。

DLL主要就是作上面分析的一些PATCH内存的操作。

下面是源码：

#include<windows.h>
#include
#include<time.h>
#include<stdlib.h>
#include<TlHelp32.h>
DWORD old;
SIZE_T written;
DWORD FindProcess() {
 HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
 PROCESSENTRY32 pe32;
 pe32 = { sizeof(pe32) };
 BOOL ret = Process32First(hSnap, &pe32);
 while (ret)
 {
 if (!wcsncmp(pe32.szExeFile, L"contest.exe", 11)) {
 printf("Find contest.exe Process %dn", pe32.th32ProcessID);
 return pe32.th32ProcessID;
 }
 ret = Process32Next(hSnap, &pe32);
 }
 return 0;
}
void InjectModule(DWORD ProcessId, const char* szPath)
{
 HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, ProcessId);
 printf("进程句柄:%pn", hProcess);
 LPVOID lpAddress = VirtualAllocEx(hProcess, NULL, 0x100, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
 SIZE_T dwWriteLength = 0;
 WriteProcessMemory(hProcess, lpAddress, szPath, strlen(szPath), &dwWriteLength);
 HANDLE hThread = CreateRemoteThread(hProcess, NULL, NULL, (LPTHREAD_START_ROUTINE)LoadLibraryA, lpAddress, NULL, NULL);
 WaitForSingleObject(hThread, -1);
 VirtualFreeEx(hProcess, lpAddress, 0, MEM_RELEASE);
 CloseHandle(hProcess);
 CloseHandle(hThread);
}
void UNHOOK(DWORD ProcessId) {
 BYTE INS[] = {0x4C,0x8B,0xD1,0xB8,0x50};
 HANDLE ths = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, ProcessId);
 MODULEENTRY32 me;
 me.dwSize = sizeof(me);
 UINT64 addr=0;
 if (Module32First(ths, &me))
 {
 do
 {
 if (addr=(UINT64)GetProcAddress(me.hModule, "ZwProtectVirtualMemory"))
 {
 printf("addr:%pn", addr);
 break;
 }

 } while (Module32Next(ths, &me));
 }
 CloseHandle(ths);
 HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, ProcessId);
 VirtualProtectEx(hProcess, (void *)addr, 0x5, PAGE_EXECUTE_READWRITE, &old);
 WriteProcessMemory(hProcess, (void *)addr, INS, 0x5, &written);
 printf("written:%dn", written);
 VirtualProtectEx(hProcess, (void*)addr, 0x5, old, &old);
 CloseHandle(hProcess);
}
int main() {
 DWORD ProcessId = FindProcess();
 while (!ProcessId) {
 printf("未找到contest程序，等待两秒中再试n");
 Sleep(2000);
 ProcessId = FindProcess();
 }
 printf("尝试去除钩子...n");
 UNHOOK(ProcessId);//去除钩子
 printf("开始注入进程...n");
 InjectModule(ProcessId, "C:\Users\xia0ji233\source\repos\T-contest\x64\Debug\T-contest.dll");
 printf("注入完毕n");
}

#include<Windows.h>
#include<time.h>
#include<stdio.h>
DWORD oldprot,ret;
PROC HookedFunction;
UINT64 Offset[3] = { 0xBA39 ,0xB9FD ,0xBA5D }, Len[3] = { 9,8,12 };//PATCH偏移和PATCH长度，这里皆patch为0x90(NOP)
BYTE Ins[] = {
 0x41,0x88,0x06, //mov [r14],al
 0x90, //nop
 0x49,0x83,0xC6,0x00 //add r14, 0
};

UINT64 InsOffset = 0xBA05,InsLen=sizeof(Ins);
SIZE_T num;
BYTE buf = 0x90;
BYTE NOP[] = { 0x90,0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90 };
void patch() {
 UINT64 Base = (UINT64)GetModuleHandle(nullptr);
 for (int i = 0; i < 3; i++) {
 UINT64 addr = Base + Offset[i];
 VirtualProtect((void *)addr, Len[i], PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void *)addr, NOP, Len[i]);
 VirtualProtect((void*)addr, Len[i], oldprot, &oldprot);
 }
 printf("NOP donen");
 VirtualProtect((void*)(Base + InsOffset), InsLen,PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void *)(Base + InsOffset), Ins, InsLen);
 VirtualProtect((void*)(Base + InsOffset), InsLen, oldprot, &oldprot);
 printf("Instruction Patch Done!n");
}

BOOL APIENTRY DllMain(HMODULE hModule,
 DWORD ul_reason_for_call,
 LPVOID lpReserved
)
{
 switch (ul_reason_for_call)
 {
 case DLL_PROCESS_ATTACH:
 patch();
 case DLL_THREAD_ATTACH:
 case DLL_THREAD_DETACH:
 case DLL_PROCESS_DETACH:
 break;
 }
 return TRUE;
}

在一开始的时候我们在内存看到了contest.txt，于是尝试直接修改，发现可以成功更改写入的文件，因此为了达到目的我们可以直接修改这里的内存，但是因为它一直在变化，因此可以查看什么写了这个内存。

主要是做了一个异或运算，直接 NOP即可。

需要注意在把指令patch掉之后，一定要写一下这里存储 Name 的地方，把 Name 替换为自己想要的名字即可。

但是发现 flag 写进去时而变化，究其原因还是因为flag内存一直在变化，因此patch修改flag的内存让它也不再变化即可。

注入器不变，DLL 需要稍微改变一下。

#include<Windows.h>
#include<time.h>
#include<stdio.h>
DWORD oldprot,ret;
PROC HookedFunction;
UINT64 Offset[3] = { 0xBA39 ,0xB9FD ,0xBA5D }, Len[3] = { 9,8,12 };//PATCH偏移和PATCH长度，这里皆patch为0x90(NOP)
BYTE Ins[] = {
 0x41,0x88,0x06, //mov [r14],al
 0x90, //nop
 0x49,0x83,0xC6,0x00 //add r14, 0
};

UINT64 InsOffset = 0xBA05,InsLen=sizeof(Ins);
SIZE_T num;
BYTE buf = 0x90;
BYTE NOP[] = { 0x90,0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90 };
void patch() {
 UINT64 Base = (UINT64)GetModuleHandle(nullptr);
 for (int i = 0; i < 3; i++) {//把三个点位的指令NOP掉
 UINT64 addr = Base + Offset[i];
 VirtualProtect((void *)addr, Len[i], PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void *)addr, NOP, Len[i]);
 VirtualProtect((void*)addr, Len[i], oldprot, &oldprot);
 }
 printf("NOP donen");
 VirtualProtect((void*)(Base + InsOffset), InsLen,PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void *)(Base + InsOffset), Ins, InsLen);//替换对应的指令
 VirtualProtect((void*)(Base + InsOffset), InsLen, oldprot, &oldprot);
 printf("Instruction Patch Done!n");
}

void patchname() {
 UINT64 Base = (UINT64)GetModuleHandle(nullptr);
 UINT64 Offset1 = 0xC8F3,Offset2=0xC5C6,NameOffset=0x772FA,Len1=4,Len2=5,flagOffset = 0x772E9;
 char NewName[] = "test.txt";//新文件名
 char flag[] = "catchmeifyoucan";
 VirtualProtect((void*)(Base + Offset1), Len1, PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void*)(Base + Offset1), NOP, Len1);//指令Nop掉防止写的时机不对发生变化
 VirtualProtect((void*)(Base + Offset1), Len1, oldprot, &oldprot);

 VirtualProtect((void*)(Base + Offset2), Len2, PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void*)(Base + Offset2), NOP, Len2);//指令Nop掉防止写的时机不对发生变化
 VirtualProtect((void*)(Base + Offset2), Len2, oldprot, &oldprot);

 VirtualProtect((void*)(Base + NameOffset), sizeof(NewName), PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void*)(Base + NameOffset), NewName, sizeof(NewName));//把名字写到内存中
 VirtualProtect((void*)(Base + NameOffset), sizeof(NewName), oldprot, &oldprot);

 VirtualProtect((void*)(Base + flagOffset), sizeof(flag), PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void*)(Base + flagOffset), flag, sizeof(flag));//把flag写到内存中
 VirtualProtect((void*)(Base + flagOffset), sizeof(flag), oldprot, &oldprot);

 printf("Change Name Successn");
}

BOOL APIENTRY DllMain(HMODULE hModule,
 DWORD ul_reason_for_call,
 LPVOID lpReserved
)
{
 switch (ul_reason_for_call)
 {
 case DLL_PROCESS_ATTACH:
 patch();
 patchname();
 case DLL_THREAD_ATTACH:
 case DLL_THREAD_DETACH:
 case DLL_PROCESS_DETACH:
 break;
 }
 return TRUE;
}

看雪ID：xi@0ji233

https://bbs.kanxue.com/user-home-919002.htm

*本文由看雪论坛 xi@0ji233 原创，转载请注明来自看雪社区

# 往期推荐

1、在 Windows下搭建LLVM 使用环境

2、深入学习smali语法

3、安卓加固脱壳分享

4、Flutter 逆向初探

5、一个简单实践理解栈空间转移

6、记一次某盾手游加固的脱壳与修复

球分享

球点赞

球在看


```
mov [r14],al
add r14,0
mov [r14],al
add r14,0
    #include<windows.h>
    #include
    #include<time.h>
    #include<stdlib.h>
    #include<TlHelp32.h>
DWORD old;
SIZE_T written;
DWORD FindProcess() {
 HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
 PROCESSENTRY32 pe32;
 pe32 = { sizeof(pe32) };
 BOOL ret = Process32First(hSnap, &pe32);
 while (ret)
 {
 if (!wcsncmp(pe32.szExeFile, L"contest.exe", 11)) {
 printf("Find contest.exe Process %dn", pe32.th32ProcessID);
 return pe32.th32ProcessID;
 }
 ret = Process32Next(hSnap, &pe32);
 }
 return 0;
}
void InjectModule(DWORD ProcessId, const char* szPath)
{
 HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, ProcessId);
 printf("进程句柄:%pn", hProcess);
 LPVOID lpAddress = VirtualAllocEx(hProcess, NULL, 0x100, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
 SIZE_T dwWriteLength = 0;
 WriteProcessMemory(hProcess, lpAddress, szPath, strlen(szPath), &dwWriteLength);
 HANDLE hThread = CreateRemoteThread(hProcess, NULL, NULL, (LPTHREAD_START_ROUTINE)LoadLibraryA, lpAddress, NULL, NULL);
 WaitForSingleObject(hThread, -1);
 VirtualFreeEx(hProcess, lpAddress, 0, MEM_RELEASE);
 CloseHandle(hProcess);
 CloseHandle(hThread);
}
void UNHOOK(DWORD ProcessId) {
 BYTE INS[] = {0x4C,0x8B,0xD1,0xB8,0x50};
 HANDLE ths = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, ProcessId);
 MODULEENTRY32 me;
 me.dwSize = sizeof(me);
 UINT64 addr=0;
 if (Module32First(ths, &me))
 {
 do
 {
 if (addr=(UINT64)GetProcAddress(me.hModule, "ZwProtectVirtualMemory"))
 {
 printf("addr:%pn", addr);
 break;
 }

 } while (Module32Next(ths, &me));
 }
 CloseHandle(ths);
 HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, ProcessId);
 VirtualProtectEx(hProcess, (void *)addr, 0x5, PAGE_EXECUTE_READWRITE, &old);
 WriteProcessMemory(hProcess, (void *)addr, INS, 0x5, &written);
 printf("written:%dn", written);
 VirtualProtectEx(hProcess, (void*)addr, 0x5, old, &old);
 CloseHandle(hProcess);
}
int main() {
 DWORD ProcessId = FindProcess();
 while (!ProcessId) {
 printf("未找到contest程序，等待两秒中再试n");
 Sleep(2000);
 ProcessId = FindProcess();
 }
 printf("尝试去除钩子...n");
 UNHOOK(ProcessId);//去除钩子
 printf("开始注入进程...n");
 InjectModule(ProcessId, "C:\Users\xia0ji233\source\repos\T-contest\x64\Debug\T-contest.dll");
 printf("注入完毕n");
}
    #include<Windows.h>
    #include<time.h>
    #include<stdio.h>
DWORD oldprot,ret;
PROC HookedFunction;
UINT64 Offset[3] = { 0xBA39 ,0xB9FD ,0xBA5D }, Len[3] = { 9,8,12 };//PATCH偏移和PATCH长度，这里皆patch为0x90(NOP)
BYTE Ins[] = {
 0x41,0x88,0x06, //mov [r14],al
 0x90, //nop
 0x49,0x83,0xC6,0x00 //add r14, 0
};

UINT64 InsOffset = 0xBA05,InsLen=sizeof(Ins);
SIZE_T num;
BYTE buf = 0x90;
BYTE NOP[] = { 0x90,0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90 };
void patch() {
 UINT64 Base = (UINT64)GetModuleHandle(nullptr);
 for (int i = 0; i < 3; i++) {
 UINT64 addr = Base + Offset[i];
 VirtualProtect((void *)addr, Len[i], PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void *)addr, NOP, Len[i]);
 VirtualProtect((void*)addr, Len[i], oldprot, &oldprot);
 }
 printf("NOP donen");
 VirtualProtect((void*)(Base + InsOffset), InsLen,PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void *)(Base + InsOffset), Ins, InsLen);
 VirtualProtect((void*)(Base + InsOffset), InsLen, oldprot, &oldprot);
 printf("Instruction Patch Done!n");
}

BOOL APIENTRY DllMain(HMODULE hModule,
 DWORD ul_reason_for_call,
 LPVOID lpReserved
)
{
 switch (ul_reason_for_call)
 {
 case DLL_PROCESS_ATTACH:
 patch();
 case DLL_THREAD_ATTACH:
 case DLL_THREAD_DETACH:
 case DLL_PROCESS_DETACH:
 break;
 }
 return TRUE;
}
    #include<Windows.h>
    #include<time.h>
    #include<stdio.h>
DWORD oldprot,ret;
PROC HookedFunction;
UINT64 Offset[3] = { 0xBA39 ,0xB9FD ,0xBA5D }, Len[3] = { 9,8,12 };//PATCH偏移和PATCH长度，这里皆patch为0x90(NOP)
BYTE Ins[] = {
 0x41,0x88,0x06, //mov [r14],al
 0x90, //nop
 0x49,0x83,0xC6,0x00 //add r14, 0
};

UINT64 InsOffset = 0xBA05,InsLen=sizeof(Ins);
SIZE_T num;
BYTE buf = 0x90;
BYTE NOP[] = { 0x90,0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90 };
void patch() {
 UINT64 Base = (UINT64)GetModuleHandle(nullptr);
 for (int i = 0; i < 3; i++) {//把三个点位的指令NOP掉
 UINT64 addr = Base + Offset[i];
 VirtualProtect((void *)addr, Len[i], PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void *)addr, NOP, Len[i]);
 VirtualProtect((void*)addr, Len[i], oldprot, &oldprot);
 }
 printf("NOP donen");
 VirtualProtect((void*)(Base + InsOffset), InsLen,PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void *)(Base + InsOffset), Ins, InsLen);//替换对应的指令
 VirtualProtect((void*)(Base + InsOffset), InsLen, oldprot, &oldprot);
 printf("Instruction Patch Done!n");
}

void patchname() {
 UINT64 Base = (UINT64)GetModuleHandle(nullptr);
 UINT64 Offset1 = 0xC8F3,Offset2=0xC5C6,NameOffset=0x772FA,Len1=4,Len2=5,flagOffset = 0x772E9;
 char NewName[] = "test.txt";//新文件名
 char flag[] = "catchmeifyoucan";
 VirtualProtect((void*)(Base + Offset1), Len1, PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void*)(Base + Offset1), NOP, Len1);//指令Nop掉防止写的时机不对发生变化
 VirtualProtect((void*)(Base + Offset1), Len1, oldprot, &oldprot);

 VirtualProtect((void*)(Base + Offset2), Len2, PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void*)(Base + Offset2), NOP, Len2);//指令Nop掉防止写的时机不对发生变化
 VirtualProtect((void*)(Base + Offset2), Len2, oldprot, &oldprot);

 VirtualProtect((void*)(Base + NameOffset), sizeof(NewName), PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void*)(Base + NameOffset), NewName, sizeof(NewName));//把名字写到内存中
 VirtualProtect((void*)(Base + NameOffset), sizeof(NewName), oldprot, &oldprot);

 VirtualProtect((void*)(Base + flagOffset), sizeof(flag), PAGE_EXECUTE_READWRITE, &oldprot);
 memcpy((void*)(Base + flagOffset), flag, sizeof(flag));//把flag写到内存中
 VirtualProtect((void*)(Base + flagOffset), sizeof(flag), oldprot, &oldprot);

 printf("Change Name Successn");
}

BOOL APIENTRY DllMain(HMODULE hModule,
 DWORD ul_reason_for_call,
 LPVOID lpReserved
)
{
 switch (ul_reason_for_call)
 {
 case DLL_PROCESS_ATTACH:
 patch();
 patchname();
 case DLL_THREAD_ATTACH:
 case DLL_THREAD_DETACH:
 case DLL_PROCESS_DETACH:
 break;
 }
 return TRUE;
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