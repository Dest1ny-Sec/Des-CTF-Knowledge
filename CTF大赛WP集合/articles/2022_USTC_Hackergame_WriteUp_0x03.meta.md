---
title: 2022 USTC Hackergame WriteUp 0x03 (Linux VM pwn)
contest: 2022 USTC Hackergame
year: 2022
difficulty: hard
vuln_type: [pwn_unknown, auth_bypass, reverse, web_unknown]
tags: [USTC-Hackergame, iPXE, SeaBIOS, qemu-VM, busybox, init, suid-setuid, flag2-uid-1337, kernel-pwn, qemu, x86, container-escape]
attack_chain: ["nc 202.38.93.111 10338 → iPXE → SeaBIOS → Linux 5.19.9 启动", "/challenge 是 setuid 0 → 普通用户跑", "cat /flag2 权限 -r-------- 1 1337 1337 → 只有 uid 1337 能读", "env 收集：kernel cmdline / uname / mount / df / ps", "/tmp 共享可写（tmpfs）", "chall 有 SUID 标志 + 路径 + 大小 20352 → static-linked", "pwndbg / ROPgadget / objdump 分析 chall 找漏洞", "exploit: 提权到 uid 1337 读 flag2 / 继续提权到 root 读 /flag"]
key_payload: "/challenge setuid 0 + uid 1337 owner of /flag2"
one_liner: USTC Hackergame 真机 Linux VM pwn：iPXE 启动 → busybox shell → SUID 提权链
lesson: iPXE + SeaBIOS 模拟远程固件启动是 CTF 高端考法；多层提权是 Linux pwn 实战
quality: high
---

# 2022 USTC Hackergame WriteUp 0x03 (Linux VM pwn)

原文 https://www.ctfiot.com/71369.html

## 远程启动流程
```bash
$ stty raw -echo; nc 202.38.93.111 10338; stty sane
Please input your token:
SeaBIOS (version 1.14.0-2)
iPXE (http://ipxe.org) 00:03.0 CA00 PCI2.10 PnP PMM+0FF8F360+0FECF360 CA00
Booting from ROM...
[    5.616162] Dev sda: unable to read RDB block 1
[    5.621327] Dev sda: unable to read RDB block 1
/ $ ls -al
total 32
-rw-------    1 1000     1000             8 Oct 25 09:07 .ash_history
---s--x--x    1 0        0            20352 Oct 15 18:20 chall    ← SUID root
-r--------    1 1337     1337           512 Oct 25 09:07 flag2     ← uid 1337 才能读
-rwxr-xr-x    1 1000     1000            27 Oct  5 17:13 init
```

## 环境
- Linux 5.19.9 x86_64
- busybox 静态链接
- 文件系统：rootfs + tmpfs /tmp
- init 启动 /challenge
- 内存 219 MB

## 攻击
```bash
/ $ mount
rootfs on / type rootfs (rw)
none on /proc type proc (rw,relatime)
none on /sys type sysfs (rw,relatime)
none on /sys/kernel/debug type debugfs (rw,relatime)
devtmpfs on /dev type devtmpfs (rw,relatime,size=89988k,nr_inodes=22497,mode=755,inode64)
none on /tmp type tmpfs (rw,relatime,inode64)

/ $ free -h
              total        used        free      shared  buff/cache   available
Mem:         219.3M       16.2M       76.2M           0      126.9M       86.2M
Swap:             0           0           0
```

## 多层提权链
1. **uid 1000 (普通)** → 找漏洞提权到 **uid 1337** 读 `/flag2`
2. **uid 1337** → 找漏洞提权到 **uid 0 (root)** 读 `/flag`（如果有）
3. **chall 是 SUID root** → 漏洞可拿 root

## 工具
- pwndbg / gdb-multiarch
- ROPgadget / ropper
- objdump
- qemu 用户态模拟（先本地跑）

## 教学价值
- **iPXE + SeaBIOS** 模拟远程固件启动
- **多层 SUID 提权** 实战链
- **uid 1337** 经典 CTF 用户 ID
- **busybox 静态链接** 体积小但反编译难度大
- **真机 Linux VM 调试** 实战经验

## 关联
- 同一批还有 #58 USTC Hackergame 0x01（rclone 密码）

## 备注
- iPXE 网络启动 + SeaBIOS 模拟 = 类似真实服务器运维
- /tmp tmpfs 可写 → 可放 exploit 二进制
- 内核 /proc /sys 可访问 → 可读环境信息
- nc 直连，stty raw 模式避免回显
