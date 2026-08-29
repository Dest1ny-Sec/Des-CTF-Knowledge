---
title: SSCTF-pwn450 win kernel 漏洞分析 (三)
contest: SSCTF
year: 2014
difficulty: hard
vuln_type: misc_unknown
tags: [windows-kernel, gdi-bug, bitmap-surfobj, kmdf-driver, win32k-bsod]
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
---
# SSCTF pwn450 win kernel BSoD 分析 (三)

bee13oy / CloverSec Labs 旧文，演示 Windows 7 SP1 x86 + Windows 10 x86 上 win32k!EngPaint 的 BSoD 利用。

## 漏洞链
- `demo_CreateBitmapIndirect` 创建 8×8 灰度 HBITMAP (bits[8][2] = 0xFF / 0x0C / 0xC0)
- `NtGdiSetBitmapAttributes` 系统调用 0x1110 设置特殊属性
- `CreateRectRgnIndirect({left=0x368c, top=0x400000})` 创建巨型 region
- `CreateCompatibleDC(0)` 拿到与默认设备兼容的 HDC
- `SelectObject(HDC, hBitmap2)` 选入 HDC
- `CreateSolidBrush(0x00edfc13)` 制造填充刷
- `FillRgn(HDC, hRgn, hBrush)` 触发 `EngPaint` 路径

## 调试细节
- 双机 NTSD 调试：`ntsd.exe -ddefer -y ... pwn450.exe`
- `kd> g` 命中 `win32k!EngPaint` (9aacb697 8bff mov edi,edi)
- 栈回溯：`EngPaint → NtGdiFillRgn+0x339 → nt!KiFastCallEntry+0x12a`
- `fe723018` 即 SURFOBJ，结构体偏移：
  - `+0x00 dhsurf`
  - `+0x04 hsurf`
  - `+0x08 dhpdev`
  - `+0x0c hdev`
  - `+0x10 sizlBitmap`
  - `+0x18 pvBits`
  - `+0x1c pvScan0`
  - `+0x20 lDelta`
  - `+0x24 iBitmapFormat`
- 第二次 `kd> g` 命中 `bGetRealizedBrush+0x38` 访问 `test byte ptr [eax+24h],1` 时崩溃
- Win7 SP1 x86 上可 EoP 到 SYSTEM；Win10 x86 仅 BSoD

## 经验
- 需要 IDA 给 KMDF 驱动加符号表
- Vergilius 网站查询 EPROCESS 偏移随 Windows 版本变化
- 推荐 OpenSecurityTraining2 高级 Windbg 课程
- OSRLoader 加载驱动
