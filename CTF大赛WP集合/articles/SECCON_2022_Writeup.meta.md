---
title: SECCON 2022 Writeup
contest: SECCON 2022
year: 2022
difficulty: high
vuln_type: rop
tags: [pwn, ret2libc, libc-leak, name-format, babyfile, io-file, fsop, _IO_read_base, vtable-overflow, free-hook]
attack_chain:
  - 题目 1 koncha: scanf 栈溢出 + libc 地址泄露
  - name[0x30] + country[0x20] + scanf("%[^\n]s") 绕过 \n 截断
  - printf("Nice to meet you, %s!\n", name) 泄露栈地址
  - 攻击: 跳过 name → country cyclic(88) + p64(libc_base+one_gadget 0xe3b01)
  - 题目 2 babyfile: FILE 结构 + trick(offset, value) 改 fp->xx
  - menu: 1=Flush 2=Trick 0=Exit
  - _IO_FILE _flags + _IO_read_ptr/end/base + _IO_write_ptr + _chain
  - 改 _mode=0x1 + vtable=0xa8 触发 _IO_doallocbuf + 分配 buffer
  - 改 vtable=0x60 触发 _IO_underflow 设置 read_base
  - getheap 16 次爆破 heap/libc leak
  - 攻击: trick(_fileno, 0x04) + trick(vtable, 0x50) 触发 _IO_finish
  - finish → puts(fp->_IO_read_ptr) 调 system
  - free_space 写 system 8 字节 + binsh 8 字节
  - _IO_save_base 写 target (system 参数 "/bin/sh")
  - _IO_write_base FROM + _IO_buf_base/__free_hook TO 触发任意地址写
  - flush 触发 system(binsh) shell
key_payload: trick(free_speace+i, system_byte) + trick(free_speace+8+i, binsh_byte) + trick(_IO_save_base+i, heap_arg)
one_liner: SECCON 2022 koncha (scanf 栈溢出 + one_gadget) + babyfile (FILE 结构 _IO_read_base/vtable 偏移 trick 任意改 → _IO_finish 触发 system(binsh))。
lesson: scanf("%[^\n]s") 格式串保留换行前内容；FILE 结构 vtable 偏移可触发任意 _IO_xxx 函数 (如 _IO_finish 调 puts)；trick(offset, value) 任意改 FILE 字段是 FILE 攻击经典模式。
quality: high
---
