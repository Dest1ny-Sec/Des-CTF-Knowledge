---
title: 【CyberDefenders】TeamSpy【Walkthrough】
contest: CyberDefenders
year: 2024
difficulty: medium
vuln_type: forensic_disk
tags: [volatility-2, imageinfo, malfind, Win7SP1x64, vmem, mimikatz, lsadump, svchost-injection, explorer-process]
attack_chain: vol.py imageinfo 识 Win7SP1x64 + malfind 找 svchost.exe 0x5c40000 PAGE_EXECUTE_READWRITE 注入 + explorer.exe 0x49f0000 注入（mov rax 0xfe2d7cf8 跳转）+ hashdump + lsadump + mimikatz
key_payload: Win7SP1x64 profile  DTB=0x187000  KDBG=0xf800029ed070
one_liner: CyberDefenders TeamSpy 内存取证 WP，Win7SP1x64 镜像 + svchost/explorer 进程注入 + mimikatz 凭据提取。
lesson: volatility 2 imageinfo 优先 Win7SP1x64 候选；malfind 找 PAGE_EXECUTE_READWRITE + VadS 进程注入点；mimikatz 配合 lsadump 提取 Windows 凭据。
quality: high
---

# 【CyberDefenders】TeamSpy【Walkthrough】

## 概览
CyberDefenders TeamSpy 内存取证 Walkthrough，使用 Volatility 2 分析 Win7SP1x64 镜像。

## 镜像信息
- 文件: `win7ecorpoffice2010-36b02ed3.vmem` / `ecorpwin7-e73257c4.vmem`
- Profile: `Win7SP1x64`
- DTB: `0x187000`
- KDBG: `0xf800029ed070`
- 处理器: 1-2 核
- 镜像时间: 2016-10-05 03:05:11 UTC

## 进程注入分析（malfind）

### svchost.exe Pid 2232 @ 0x5c40000
- Vad Tag: `VadS`
- Protection: `PAGE_EXECUTE_READWRITE`
- Flags: `CommitCharge: 128, MemCommit: 1, PrivateMemory: 1, Protection: 6`
- 注入代码片段（x86-64）：
  ```
  48 8b 45 20    mov rax, [rbp+0x20]
  48 89 c2       mov rdx, rax
  48 8b 45 18    mov rax, [rbp+0x18]
  48 8b 00       mov rax, [rax]
  48 89 02       mov [rdx], rax
  48 8b 45 20    mov rax, [rbp+0x20]
  ```
- 模式：函数指针拷贝到 [rdx]，[rax] 是 PE 文件某表

### explorer.exe Pid 2492 @ 0x49f0000
- 注入特征：
  ```
  41 ba 80 00 00 00       mov r10d, 0x80
  48 b8 f8 7c 2d ff fe 07 00 00  mov rax, 0x7feff2d7cf8
  48 ff 20                 jmp [rax]
  ```
- 0x7feff2d7cf8 是 Windows 7 内核回调地址（典型 ntdll 钩子）
- 钩子跳到用户态注入区

## 推荐插件组合
1. `imageinfo` 识 profile
2. `malfind` 找注入
3. `pslist / pstree` 列进程
4. `hashdump` 提 NTLM hash
5. `lsadump` 提 LSA secret
6. `mimikatz`（volatility 插件）提明文密码
7. `filescan / dumpfiles` 找可疑文件
8. `netscan` 看网络连接

## 经验提炼
- volatility 2 imageinfo 优先 Win7SP1x64 候选
- malfind 关键标志：PAGE_EXECUTE_READWRITE + VadS 标签
- svchost.exe 注入是 TeamSpy 木马典型特征
- explorer.exe 跳到 0x7feff... 内核回调地址是 rootkit 钩子
- mimikatz 配合 lsadump 提取 Windows 凭据（明文密码）
- DTB/KDBG 是 Win 内存取证的锚点
