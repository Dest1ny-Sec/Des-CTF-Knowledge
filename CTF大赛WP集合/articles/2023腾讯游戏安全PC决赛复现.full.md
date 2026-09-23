---
title: 2023 腾讯游戏安全 PC 决赛复现 - Detours Hook + TLS 守护
contest: 腾讯游戏安全 PC 决赛
year: 2023
difficulty: hard
vuln_type:
- reverse
- pwn_unknown
tags:
- Windows逆向
- Detours Hook库
- TLS线程局部存储
- DLL注入
- 进程守护
- 游戏反外挂
- WorkingService.exe
- CreateRemoteThread
- VirtualAllocEx
attack_chain: 用 CreateToolhelp32Snapshot 枚举 WorkingService.exe 进程 → OpenProcess + VirtualAllocEx 远程分配 → WriteProcessMemory 写 DLL 路径 → CreateRemoteThread + LoadLibraryA 注入 → DLL 入口 DllMain 用 Detours 库 inline hook CreateFileA → TLS 记录每线程调用次数超 16 次 ExitThread(0) 自杀 → 配合 ntdll.NtProtectVirtualMemory 0xA0990 偏移的 unhook 还原 originBytes 24 字节特征码
key_payload: jmpBytes = { 0xE9, 0xE0, 0x26, 0x16, 0x00 } ; originBytes = { 0x4C, 0x8B, 0xD1, 0xB8, 0x50, 0x00, 0x00, 0x00, 0xF6, 0x04, 0x25, 0x08, 0x03, 0xFE, 0x7F, 0x01, 0x75, 0x03, 0x0F, 0x05, 0xC3, 0xCD, 0x2E, 0xC3 } ; unHookAddr = ntdll_base + 0xA0990
one_liner: Detours inline hook + TLS 计数 + CreateRemoteThread 远程注入的游戏反外挂守护。
lesson: Windows Hook 反外挂关键在 ntdll 自身也被 hook 时需要 unhook 后再注入，特征码恢复靠写死 24 字节 syscall 入口。
quality: high
full_path: 2023腾讯游戏安全PC决赛复现.full.md
meta_path: 2023腾讯游戏安全PC决赛复现.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 2023 腾讯游戏安全 PC 决赛复现 - Detours Hook + TLS 守护。Detours inline hook + TLS 计数 + CreateRemoteThread 远程注入的游戏反外挂守护。。经验：Windows Hook 反外挂关键在 ntdll 自身也被 hook 时需要 unhook 后再注入，特征码恢复靠写死...
category: reverse
subcategory: reverse
subcategories:
- reverse
- pwn_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/199546.html
reasoning_chain:
- 触发点：CreateToolhelp32Snapshot 枚举 WorkingService.exe → 假设 OpenProcess + VirtualAllocEx 远程分配
- actor WriteProcessMemory 写 DLL 路径 → 假设 CreateRemoteThread + LoadLibraryA 注入 → 观察：DLL 注入
- actor DLL 入口 DllMain Detours inline hook CreateFileA → 假设：jmpBytes 24 字节改5 字节
- actor TLS 记录每线程调用次数超 16 次 ExitThread(0) 自杀 → 假设：进程守护
- actor ntdll.NtProtectVirtualMemory 0xA0990 偏移 unhook → 假设：还原 originBytes 24 字节
- actor 特征码恢复靠写死 24 字节 syscall 入口 → 观察：成功注入 WorkingService
- actor CreateRemoteThread 远程注入 + Detours hook → 假设：游戏反外挂守护
failed_attempts:
- 试图直接远程线程 LoadLibraryA → 失败：ntdll 自身被 hook 需 unhook 后再注入
- 试图不解 originBytes 24 字节 → 失败：必须还原 syscall 入口
key_observations:
- Windows Hook 反外挂关键在 ntdll 自身也被 hook 时需要 unhook 后再注入
- 特征码恢复靠写死 24 字节 syscall 入口
- Detours inline hook 用 5 字节 jmpBytes 替换
- TLS 线程局部存储守护每线程计数
prerequisites:
- Windows API CreateRemoteThread + VirtualAllocEx 注入
- Detours inline hook 原理
- TLS 线程局部存储
- ntdll syscall 入口恢复
---
# 2023腾讯游戏安全PC决赛复现

> 原文: https://www.ctfiot.com/199546.html
> ID: 199546

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码 隐藏代码
bool KillProcessByName(const char* processName) {
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(PROCESSENTRY32);
    if (Process32First(hSnapshot, &pe)) {
        do {
            if (strcmp(pe.szExeFile, processName) == 0) {
                HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pe.th32ProcessID);
                if (hProcess) {
                    TerminateProcess(hProcess, 0);
                    CloseHandle(hProcess);
                    Num++;
                    printf("Kill suc:[%d]n", Num);
                }
            }
        } while (Process32Next(hSnapshot, &pe));
    }

    CloseHandle(hSnapshot);
    return true;
}
int main()
{
    while(1)
    {
        KillProcessByName("WorkingService.exe");
    }
    return 0;
}
复制代码 隐藏代码
    #include "pch.h"
    #include <windows.h>
    #include <shellapi.h>
    #include <detours.h>
    #include <tlhelp32.h>
    #pragma comment(lib,"detours.lib")
    #define _DEBUG
    #define DBGMGEBOX(fmt, ...)
    do {
         /* 假设最大长度为1024，根据需要调整大小 */
        wsprintfA(out, fmt, __VA_ARGS__);
        MessageBoxA(NULL, out, "提示", MB_OK);
    } while(0)
char out[100];
DWORD tlsIndex;//tls索引
type
def BOOL(WINAPI* ShellExecuteExA_t)(SHELLEXECUTEINFOA*);
typedef HANDLE (WINAPI* CreateFileA_t)(
    LPCSTR                lpFileName,
    DWORD                 dwDesiredAccess,
    DWORD                 dwShareMode,
    LPSECURITY_ATTRIBUTES lpSecurityAttributes,
    DWORD                 dwCreationDisposition,
    DWORD                 dwFlagsAndAttributes,
    HANDLE                hTemplateFile
);

ShellExecuteExA_t TrueShellExecuteExA = NULL;
CreateFileA_t TrueCreateFileA = NULL;

BOOL WINAPI HookedShellExecuteExA(SHELLEXECUTEINFOA* pExecInfo) {
    #if 1
    //执行第一个ShellExecuteExA守护进程
    static int Num = 0;
    DBGMGEBOX("ShellExecuteExA 被调用:
Num = %dnhProcess = %p", Num, pExecInfo->hProcess);
    if (Num == 0)
    {
        Num++;
        return TrueShellExecuteExA(pExecInfo);
    }
    else
    {
        return TrueShellExecuteExA(pExecInfo);
    }
    #else
    //执行第二个ShellExecuteExA病毒进程
    static int Num = 0;
    DBGMGEBOX("ShellExecuteExA 被调用:
Num = %d n调用者窗口句柄 = 0x%pn", Num, pExecInfo->hwnd);
    if (Num == 0)
    {
        Num++;
        DBGMGEBOX("[2]:
当前线程ID：%d", GetCurrentThreadId());
        pExecInfo->lpFile = "C:\Users\Administrator\Desktop\自动F8直到call.txt";//修改参数导致重启失败;
        return TrueShellExecuteExA(pExecInfo);

    }
    else
    {

        DBGMGEBOX("[1]:
当前线程ID：%d", GetCurrentThreadId());
        return TrueShellExecuteExA(pExecInfo);
    }
    #endif
}
HANDLE WINAPI HookCreateFileA(
    LPCSTR                lpFileName,
    DWORD                 dwDesiredAccess,
    DWORD                 dwShareMode,
    LPSECURITY_ATTRIBUTES lpSecurityAttributes,
    DWORD                 dwCreationDisposition,
    DWORD                 dwFlagsAndAttributes,
    HANDLE                hTemplateFile
)
{

    //判断线程是否是第一次运行CreateFileA，是的话就放行，不是第一次运行就终止线程
    // 获取当前线程的TLS值
    LPVOID tlsValue = TlsGetValue(tlsIndex);

    if (tlsValue == NULL)
    {
        // 第一次运行，设置TLS值
    #ifdef _DEBUG
        DBGMGEBOX("放行nlpFileName:%sn", lpFileName);
    #endif
        TlsSetValue(tlsIndex, (LPVOID)1);
    }
    else
    {
        // 不是第一次运行，终止线程
    #ifdef _DEBUG
        DBGMGEBOX("终止nlpFileName:%sn", lpFileName);
    #endif
        ExitThread(0);
    }
    return CreateFileA(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
}
BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:

        DetourTransactionBegin();
        DetourUpdateThread(GetCurrentThread());
        /*TrueShellExecuteExA = (ShellExecuteExA_t)DetourFindFunction("shell32.dll", "ShellExecuteExA");
        DetourAttach(&(PVOID&)TrueShellExecuteExA, HookedShellExecuteExA);*/

        tlsIndex = TlsAlloc();//初始化TLS
        TrueCreateFileA = (CreateFileA_t)DetourFindFunction("kernelbase.dll", "CreateFileA");
        DetourAttach(&(PVOID&)TrueCreateFileA, HookCreateFileA);

        DetourTransactionCommit();
        break;
    case DLL_PROCESS_DETACH:
        DetourTransactionBegin();
        DetourUpdateThread(GetCurrentThread());
        DetourDetach(&(PVOID&)TrueShellExecuteExA, HookedShellExecuteExA);
        DetourDetach(&(PVOID&)TrueCreateFileA, HookCreateFileA);
        TlsFree(tlsIndex);//清理TLS
        DetourTransactionCommit();
        break;
    }
    return TRUE;
}
复制代码 隐藏代码
HANDLE CreateFileA(
    LPCSTR lpFileName,    // 文件名
    DWORD dwDesiredAccess, // 访问模式
    DWORD dwShareMode,     // 共享模式
    LPSECURITY_ATTRIBUTES lpSecurityAttributes, // 安全属性
    DWORD dwCreationDisposition, // 创建或打开文件的方式
    DWORD dwFlagsAndAttributes, // 文件属性
    HANDLE hTemplateFile // 模板文件句柄
);
复制代码 隐藏代码
HANDLE WINAPI HookCreateFileA(
    LPCSTR                lpFileName,
    DWORD                 dwDesiredAccess,
    DWORD                 dwShareMode,
    LPSECURITY_ATTRIBUTES lpSecurityAttributes,
    DWORD                 dwCreationDisposition,
    DWORD                 dwFlagsAndAttributes,
    HANDLE                hTemplateFile
)
{
    //缩小每个线程执行CreateFileA的次数，CPU降低到%5以下
    // 获取当前线程的TLS值
    LPVOID tlsValue = TlsGetValue(tlsIndex);

    if ((DWORD_PTR)tlsValue <= 0x10)
    {
    #ifdef _KDEBUG
        DBGMGEBOX("放行nlpFileName:%sn", lpFileName);
    #endif
        dwFlagsAndAttributes = FILE_ATTRIBUTE_NORMAL;
        TlsSetValue(tlsIndex, (LPVOID)((DWORD_PTR)tlsValue + 1));
    }
    else
    {
    #ifdef _KDEBUG
        DBGMGEBOX("终止nlpFileName:%sn", lpFileName);
    #endif
        ExitThread(0);
    }
    return TrueCreateFileA(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
}
复制代码 隐藏代码
int main() {
    while (1)
    {
        int Num = 0;
        ve  = GetPidByProcName("WorkingService.exe");
        if (!ve.empty())
        {
            printf("There are currently %d processesn", ve.size());
            //依次注入并用map标记是否被注入过
            for (auto i : ve)
            {
                auto it = mp.find(i);
                if (it == mp.end())//没有被注入过
                {
                    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, i);
                    if (InjectDll(hProcess, dllPath))
                    {
                        Num++;
                        mp.insert({ i,true });
                        printf("Inject  process Success!n", Num);
                    }
                }
                else //曾经注入过该进程
                {
                    printf("[%d] Has Been Injectedn",i);
                    continue;
                }
            }
        }
        else
        {
            printf("Wating WorkingService.exe ...n");
        }
        system("cls");
        //Sleep(200);
    }
    return 0;
}
复制代码 隐藏代码
//main.cpp
    #include <windows.h>
    #include <tlhelp32.h>
    #include <stdio.h>
    #include <vector>
    #include <map>
char dllPath[] = R"(C:
Users15386DesktoptemphookDll.dll)";
std::
vector<DWORD64>ve;
std::
map<DWORD64, bool>mp;
BYTE jmpBytes[] = {
0xE9, 0xE0, 0x26, 0x16, 0x00
};
BYTE originBytes[] = {
0x4C, 0x8B, 0xD1, 0xB8, 0x50, 0x00, 0x00, 0x00, 0xF6, 0x04, 0x25, 0x08, 0x03, 0xFE, 0x7F, 0x01,
 0x75, 0x03, 0x0F, 0x05, 0xC3, 0xCD, 0x2E, 0xC3
};
std::
vector<DWORD64> GetPidByProcName(const char* processName) {
    HANDLE hProcessSnap = INVALID_HANDLE_VALUE;
    PROCESSENTRY32 pe32 = { 0 };

    std::
vector<DWORD64> vec;
    vec.clear();
    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hProcessSnap == INVALID_HANDLE_VALUE) {
        vec;
    }

    pe32.dwSize = sizeof(PROCESSENTRY32);

    if (Process32First(hProcessSnap, &pe32)) {
        do {
            if (strcmp(pe32.szExeFile, processName) == 0) {
                vec.push_back(pe32.th32ProcessID);
            }
        } while (Process32Next(hProcessSnap, &pe32));
    }
    CloseHandle(hProcessSnap);
    return vec;
}

DWORD64 GetModuleBase(DWORD64 pid,const char* ModuleName)
{
    HANDLE hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid);
    if (hModuleSnap != INVALID_HANDLE_VALUE) {
        MODULEENTRY32 me32;
        me32.dwSize = sizeof(MODULEENTRY32);
        if (Module32First(hModuleSnap, &me32)) {
            do {
                if (_stricmp(me32.szModule, ModuleName) == 0) {
                    return (DWORD64)me32.modBaseAddr;
                }
            } while (Module32Next(hModuleSnap, &me32));
        }
        CloseHandle(hModuleSnap);
    }
    return 0;
}

BOOL InjectDll(HANDLE hProcess, LPCSTR dllPath) {

    LPVOID pRemoteDllPath = VirtualAllocEx(hProcess, NULL, strlen(dllPath) + 1, MEM_COMMIT, PAGE_READWRITE);
    if (pRemoteDllPath == NULL) {
        printf("VirtualAllocEx Failed:[%d]n", GetLastError());
        return FALSE;
    }

    if (!WriteProcessMemory(hProcess, pRemoteDllPath, dllPath, strlen(dllPath) + 1, NULL)) {
        printf("WriteProcessMemory Failed:[%d]n", GetLastError());
        VirtualFreeEx(hProcess, pRemoteDllPath, 0, MEM_RELEASE);
        return FALSE;
    }

    LPTHREAD_START_ROUTINE lpLoadLibrary = (LPTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandleA("kernel32.dll"), "LoadLibraryA");
    if (lpLoadLibrary == NULL) {
        printf("GetProcAddress Failed:[%d]n", GetLastError());
        VirtualFreeEx(hProcess, pRemoteDllPath, 0, MEM_RELEASE);
        return FALSE;
    }

    HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, lpLoadLibrary, pRemoteDllPath, 0, NULL);
    if (hThread == NULL) {
        printf("CreateRemoteThread Failed:[%d]n", GetLastError());
        VirtualFreeEx(hProcess, pRemoteDllPath, 0, MEM_RELEASE);
        return FALSE;
    }

    WaitForSingleObject(hThread, INFINITE);

    DWORD dwExitCode;
    if (GetExitCodeThread(hThread, &dwExitCode) && dwExitCode == 0) {
        printf("LoadLibraryA Failed in remote processn");
        CloseHandle(hThread);
        VirtualFreeEx(hProcess, pRemoteDllPath, 0, MEM_RELEASE);
        return FALSE;
    }

    CloseHandle(hThread);
    VirtualFreeEx(hProcess, pRemoteDllPath, 0, MEM_RELEASE);

    return TRUE;
}

BOOL RemoveHook(HANDLE hProcess,PVOID unHookAddr, BYTE* originBytes)
{
   PDWORD oldProtect = 0;
   if (!WriteProcessMemory(hProcess, (PVOID)unHookAddr, originBytes, sizeof(originBytes), 0))
   {
       printf("RemoveHook Failed!!!: [%d]n", GetLastError());
       return FALSE;
   }
}
int main() {
    while (1)
    {
        int Num = 0;
        ve  = GetPidByProcName("WorkingService.exe");//获取所有进程pid
        if (!ve.empty())
        {
            printf("There are currently %d processesn", ve.size());
            //依次注入并用map标记是否被注入过
            for (auto i : ve)
            {
                auto it = mp.find(i);
                if (it == mp.end())//没有被注入过
                {
                    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, i);//要用管理员权限运行，要不然为返回空
                    if (!hProcess) printf("OpenProcess Error:[%d]", GetLastError());
                    DWORD64 unHookAddr = GetModuleBase(i,"ntdll.dll") + 0xA0990;//NtProtectVirtualMemory地址，ntdll + 0xA0990
                    if (RemoveHook(hProcess, (PVOID)unHookAddr, originBytes))//先取消NtProtectVirtualMemory钩子再注入
                    {
                        if (InjectDll(hProcess, dllPath))
                        {
                            Num++;
                            mp.insert({ i,true });//注入成功后进行标记
                            printf("Inject  process Success!n", Num);
                        }
                    }

                }
                else  continue;//曾经注入过该进程
            }
        }
        else printf("Wating WorkingService.exe ...n");
        Sleep(1000);
        system("cls");

    }
    return 0;
}
复制代码 隐藏代码
//dllmain.cpp
    #include "pch.h"
    #include <windows.h>
    #include <shellapi.h>
    #include <detours.h>
    #include <tlhelp32.h>
    #include <stdlib.h>
    #pragma comment(lib,"detours.lib")
    #define _KDEBUG
    #define DBGMGEBOX(fmt, ...)
    do {
         /* 假设最大长度为1024，根据需要调整大小 */
        wsprintfA(out, fmt, __VA_ARGS__);
        MessageBoxA(NULL, out, "提示", MB_OK);
    } while(0)
char out[100];
DWORD tlsIndex;//tls索引
type
def BOOL(WINAPI* ShellExecuteExA_t)(SHELLEXECUTEINFOA*);
typedef HANDLE (WINAPI* CreateFileA_t)(
    LPCSTR                lpFileName,
    DWORD                 dwDesiredAccess,
    DWORD                 dwShareMode,
    LPSECURITY_ATTRIBUTES lpSecurityAttributes,
    DWORD                 dwCreationDisposition,
    DWORD                 dwFlagsAndAttributes,
    HANDLE                hTemplateFile
);
ShellExecuteExA_t TrueShellExecuteExA = NULL;
CreateFileA_t TrueCreateFileA = NULL;
BOOL WINAPI HookedShellExecuteExA(SHELLEXECUTEINFOA* pExecInfo) {
    #if 1
    //执行第一个ShellExecuteExA守护进程
    static int Num = 0;
    DBGMGEBOX("ShellExecuteExA 被调用:
Num = %dnhProcess = %p", Num, pExecInfo->hProcess);
    if (Num == 0)
    {
        Num++;
        return TrueShellExecuteExA(pExecInfo);
    }
    else
    {
        return TrueShellExecuteExA(pExecInfo);
    }
    #else
    //执行第二个ShellExecuteExA病毒进程
    static int Num = 0;
    DBGMGEBOX("ShellExecuteExA 被调用:
Num = %d n调用者窗口句柄 = 0x%pn", Num, pExecInfo->hwnd);
    if (Num == 0)
    {
        Num++;
        DBGMGEBOX("[2]:
当前线程ID：%d", GetCurrentThreadId());
        pExecInfo->lpFile = "C:\Users\Administrator\Desktop\自动F8直到call.txt";//修改参数导致重启失败;
        return TrueShellExecuteExA(pExecInfo);

    }
    else
    {

        DBGMGEBOX("[1]:
当前线程ID：%d", GetCurrentThreadId());
        return TrueShellExecuteExA(pExecInfo);
    }
    #endif
}
HANDLE WINAPI HookCreateFileA(
    LPCSTR                lpFileName,
    DWORD                 dwDesiredAccess,
    DWORD                 dwShareMode,
    LPSECURITY_ATTRIBUTES lpSecurityAttributes,
    DWORD                 dwCreationDisposition,
    DWORD                 dwFlagsAndAttributes,
    HANDLE                hTemplateFile
)
{

    //判断线程是否是第一次运行CreateFileA，是的话就放行，不是第一次运行就终止线程
    // 获取当前线程的TLS值
    LPVOID tlsValue = TlsGetValue(tlsIndex);
    if ((DWORD_PTR)tlsValue <= 0x10)
    {
        //
    #ifdef _KDEBUG
        DBGMGEBOX("放行nlpFileName:%sn", lpFileName);
    #endif
        dwFlagsAndAttributes = FILE_ATTRIBUTE_NORMAL;
        TlsSetValue(tlsIndex, (LPVOID)((DWORD_PTR)tlsValue + 1));
    }
    else
    {
        static int Num = 0;//如果终止了十六个线程，再终止进程，使得守护线程再生工作进程
        // 不是第一次运行，终止线程
    #ifdef _KDEBUG
        DBGMGEBOX("终止nlpFileName:%sn", lpFileName);
    #endif
        Num++;
        ExitThread(0);
        if (Num == 16) exit(0);
    }
    return TrueCreateFileA(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:

        DetourTransactionBegin();
        DetourUpdateThread(GetCurrentThread());

        //ShellExecuteExA hook
        /*TrueShellExecuteExA = (ShellExecuteExA_t)DetourFindFunction("shell32.dll", "ShellExecuteExA");
        DetourAttach(&(PVOID&)TrueShellExecuteExA, HookedShellExecuteExA);*/

        tlsIndex = TlsAlloc();//初始化TLS
        TrueCreateFileA = (CreateFileA_t)DetourFindFunction("kernelbase.dll", "CreateFileA");
        DetourAttach(&(PVOID&)TrueCreateFileA, HookCreateFileA);

        DetourTransactionCommit();
        break;
    case DLL_PROCESS_DETACH:
        DetourTransactionBegin();
        DetourUpdateThread(GetCurrentThread());
        DetourDetach(&(PVOID&)TrueShellExecuteExA, HookedShellExecuteExA);
        DetourDetach(&(PVOID&)TrueCreateFileA, HookCreateFileA);
        TlsFree(tlsIndex);//清理TLS

        DetourTransactionCommit();
        break;
    }
    return TRUE;
}
复制代码 隐藏代码
1 F2FU4Wht52lm+2dV4WFu 6128
2 4WECF2ht52lm+2dV4WFu 20512
2 4WECF2ht52lm+2dV4WFu 22060
3 Fx9U4RY7ERcwDRkDFx84 22708
4 Fx8CFxY7ERcwDRkD4WFu 25296
5 Fx9U4RZt5xcwDRkDFx84 25376
6 Fx8CFxY7ERcwDRkDFx84 25620
3 Fx9U4RY7ERcwDRkDFx84 25756
2 4WECF2ht52lm+2dV4WFu 26136
3 Fx9U4RY7ERcwDRkDFx84 27704
7 4R9U4RY7ERcwDWdV4WE4 27976
8 4WECF2ht5xcwDRkDFx84 28380
3 Fx9U4RY7ERcwDRkDFx84 28624
9 Fx9U4RY7EWlm+xkDFx84 28764
10 4WECFxY7ERcwDWdV4WFu 29904
11 Fx9U4RY7ERcwDWdV4WE4 31648
复制代码 隐藏代码
明文：0x15, 0x61, 0x02, 0x15, 0x68, 0x1B, 0x13, 0x69, 0x66, 0x79, 0x6F, 0x75, 0x63, 0x17, 0x18
实际密文：F2ECF2g7EWlm+2dV4R84
正常base64密文：F2ECF2g7EWlm+2dV4R84
明文：0x63, 0x17, 0x74, 0x63, 0x1E, 0x6D, 0x65, 0x1F, 0x10, 0x0F, 0x19, 0x03, 0x15, 0x61, 0x6E
实际密文：4R9U4RZt5xcwDRkDF2Fu
正常base64密文：4R9U4RZt5xcwDRkDF2Fu
复制代码 隐藏代码
//34288线程
文件密文：4WFU4Wht52lm+2dV4WFu
密文1   ：Fx8C4Wg7ERcwDWdV4WE4
密文2   ：4WFUFxZt52lm+xkDFx9u
复制代码 隐藏代码
//14032 线程
文件密文：Fx8CFxY7ERcwDRkDFx84
密文1   ：Fx8C4Wg7ERcwDWdV4WE4
密文2   ：4WFUFxZt52lm+xkDFx9u
复制代码 隐藏代码
{
0x15, 0x17, 0x02, 0x15, 0x1E, 0x1B, 0x13, 0x1F, 0x10, 0x0F, 0x19, 0x03, 0x15, 0x17, 0x18
};
复制代码 隐藏代码
mov r8, qword ptr ds:[rdi]
mov r9b, byte ptr ds:[rdi+0x8]
mov byte ptr ds:[r8], r9b
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