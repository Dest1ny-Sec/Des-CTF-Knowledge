---
title: RWCTF 5th Shellfind 复现
contest: RWCTF 5th
year: 2022
difficulty: high
vuln_type: rop
tags: [iot, mips, udp-service, ipfind, base64-decode, stack-overflow, ret2shellcode, qemu, firmadyne, pwn]
attack_chain:
  - 复现 RealWorld CTF 5th IoT PWN 题目 - 基于真实设备固件改编
  - 拿到 .bin 固件包解压获得完整文件系统
  - 下载官方固件 + bindiff 比对找到被修改的 ipfind 二进制
  - MIPS 大端 + 无任何保护
  - 模拟: qemu-system-mips + malta + vmlinux-3.2.0-4-4kc-malta + tap0 网络
  - 启动 chroot squashfs-root + mount /proc + 切换 /etc/rc.d/rcS
  - 启动 ipfind eth0 & 替换默认 br0 (qemu 模拟器用 eth0)
  - 漏洞点: sub_400F50 base64 decode 到栈 → 栈溢出
  - checksec: No RELRO + No canary + NX disabled + No PIE + Has RWX
  - mipsrop 无输出 → 自构 ROP
  - 利用 UDP 协议: FIVI + cmd=2 (Shell) + base64(username:password) 触发
  - sub_4013F4 校验 + sub_400F50 触发 base64 decode 栈溢出
  - s_log_nothing 泄露栈地址 → 改 GOT → ret2shellcode
  - dup2 stdin/stdout/stderr + execve /bin/busybox sh
  - 利用 IPFIND UDP fd 复用作为 RCE
key_payload: base64(b'a'*padding + rop + shellcode)
one_liner: RWCTF 5th Shellfind 复现 WP：qemu malta mips 模拟器 + tap0 网络 + ipfind UDP 62720 + base64 栈溢出 + dup2 busybox sh 回连。
lesson: qemu-system-mips + tap0 桥接 + chroot 启动是 IoT 复现基础；ipfind 启动时指定 eth0 (qemu 模拟器) 而非 br0 (真实设备) 才能 gdbserver 调试；base64 decode 写入栈是经典溢出模式。
quality: high
---
