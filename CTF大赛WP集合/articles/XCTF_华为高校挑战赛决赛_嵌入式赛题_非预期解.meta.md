---
title: XCTF 华为高校挑战赛决赛/嵌入式非预期解
contest: XCTF
year: null
difficulty: hard
vuln_type:
- pwn_unknown
- reverse
tags:
- 嵌入式
- LiteOS
- Hi3518
- qemu-system-arm
- migrate exec
- ARM shellcode
- syscall 0x206
- readreg
- HarmonyOS
- pwntools ARM
attack_chain:
- 题目用 qemu-system-arm -M hi3518 模拟 LiteOS（HarmonyOS 内核）
- 拿 qemu monitor 的 migrate "exec: cmd" 注入命令
- 直接 strings /rootfs.img | grep flag 找 flag
- 或 migrate "exec: base64 rootfs.img" 整盘 dump
- 非预期：通过 qemu monitor 注入 ARM shellcode (svc 0 + readreg 系统调用) 读任意内存
- 构造 shellcode：mov r7, 0x206; adr r0, "readreg"; adr r1, cmd_str; svc 0
- 把 shellcode patch 进 camera_app 二进制
- 通过串口发到 qemu，触发后读 flag 字符串内存
- 提取 hex 字符串，反转拼接得 flag
key_payload: "io.sendlineafter('finish', shellcode.hex())  # ARM shellcode 注入 qemu"
one_liner: qemu-system-arm LiteOS 模拟器 migrate exec 注入命令 + ARM shellcode readreg 系统调用
lesson: qemu-monitor 的 migrate "exec: cmd" 可作为嵌入式题的非预期入口；LiteOS 系统调用 0x206 是 readreg 任意内存读
quality: high
---

# XCTF 华为高校挑战赛决赛/嵌入式非预期解

**qemu-system-arm LiteOS 模拟器 + migrate exec 注入 + ARM shellcode**

> XCTF · ? · hard · pwn/reverse · quality=high
> 思路: qemu-system-arm -M hi3518 跑 LiteOS → qemu monitor migrate "exec: cmd" 注入命令 → 整盘 dump → 找 flag
> 套路: qemu-monitor 的 migrate "exec: cmd" 可作为嵌入式题的非预期入口；LiteOS 系统调用 0x206 是 readreg 任意内存读

**关键 payload**:
```python
io.sendlineafter('finish', shellcode.hex())  # ARM shellcode 注入 qemu
```
