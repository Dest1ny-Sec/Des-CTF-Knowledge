---
title: RWCTF 5th ShellFind Write-up
contest: RWCTF 5th
year: 2022
difficulty: high
vuln_type: rop
tags: [iot, mips, udp-service, ipfind, base64-decode, stack-overflow, ret2shellcode, qemu, firmadyne, pwn, f5-bigip]
attack_chain:
  - 出题背景：IoT 安全 (Pink 僵尸网络) - 模拟 IoT 设备调试接口
  - 题目类型 PWN (Normal) - Hello Hacker 提示 only one UDP service to shell
  - FIRMADYNE 仿真 + FIRMae 自动化 + TAP 虚拟网络
  - netstat 发现 ddp 62976 + ipfind 62720 + tcp 31338 + http 80
  - ipfind 监听 UDP 0xF580 (62720) - 目标服务
  - UDP 协议 27 字节：4 magic "FIVI" + 4 pad + 1 type=10 + 2 cmd + ...
  - sub_4013F4 进入 sub_400F50 base64 decode 到栈上 → 栈溢出
  - checksec: No RELRO + No canary + NX disabled + No PIE + Has RWX
  - qemu 中开启 ASLR, mipsrop 无输出需自构造
  - 漏洞点: s_log_nothing addiu $v0,$sp,0x10+arg_4 → 栈地址 leak
  - 改 GOT: 0x00400c9c lw $gp, 0x10($sp) ; lw $ra, 0x1c($sp) ; jr $ra ; addiu $sp, $sp, 0x20
  - 单命令受限 (几百字符)，busybox nc 被改 nx 不能反弹 shell
  - 多次利用: rm /var/run/ipfind-br0.pid; ipfind br0 & 重启服务
  - ret2shellcode: dup2 → busybox sh → connect back to attacker
  - 利用 dup2(2) + execve /bin/busybox sh sys 0xfdf/0xfab
  - 出题总结: 固件模拟 (QEMU+FIRMADYNE) + 网络服务发现 + 漏洞挖掘 + 利用
key_payload: rop_chain = 0x3C1C0042 (lui $gp) + 0x279CB030 (addiu $gp) + lw $v0 server_sockfd + lw $a0 (fd) + dup2 loop + execve /bin/busybox sh
one_liner: RWCTF 5th ShellFind 长亭科技官方 WP：IoT 固件模拟 + UDP ipfind base64 解码栈溢出 + mips 无防护 ROP 改 GOT + dup2 busybox sh 回连。
lesson: IoT 攻防人员需掌握 FIRMADYNE/FIRMae 自动化仿真；mips 自构 ROP 关键是找 jr $ra + lw $gp gadget；UDP 服务复用 fd 是反连 RCE 唯一路径；s_log_nothing 类函数常常会泄露栈地址。
quality: high
---
