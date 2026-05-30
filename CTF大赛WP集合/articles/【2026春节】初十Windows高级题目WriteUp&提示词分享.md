# 【2026春节】初十Windows高级题目WriteUp&提示词分享

> 原文: https://www.ctfiot.com/304400.html
> ID: 304400

作者论坛账号：Tokeii

：约 40MB，其中大部分为数据段中嵌入的密码学查找表

：

（位于 RVA0x154E50）：已知白盒密码上下文，约 2.7MB

（位于 RVA0xAD7660）：自定义白盒密码上下文，约 28.8MB（0x1B4F428字节）

：自绘窗口，输入 UID 和 flag 后触发验证函数

：几乎所有关键函数的控制流都被 MBA 表达式混淆，使用n*(n+1)或n*(n-1)等恒偶不透明谓词（opaque predicate）控制状态机跳转

函数 RVA

功能

特点

UID → 32字节哈希

SipHash 变体，纯计算

32字节 → 280字节派生

642行 SSE/MBA，无外部调用

CHIMERA1 blob → 堆上下文

MBA 状态机包裹的 memcpy

验证 “CHIMERA1” 头

逐字节检查 8 字节魔术值

白盒密码核心变换

反编译失败，~95M 指令

白盒分组密码（20轮）

仅适用于 PRISMWB3

64字节内存比较

MBA 混淆的 memcmp

HookD3B20（比较函数），在比较时读取rdx（期望值 m2）

：Frida GUI 自动化无法正确触发按钮点击，无法可靠触发验证流程

：曾捕获一个 m2 值，但无法确认其对应的 UID

将 PE 文件完整映射到 Unicorn 内存空间

设置堆栈、堆、IO 缓冲区等辅助内存区域

逐步执行D11D0→D1BF0→FD790

从输出缓冲区读取 m2

Hook12EBC0入口，直接从 PE 镜像中的原始 CHIMERA1 blob 复制到一个专用的、不重叠的内存区域（CTX_BASE = 0x300000000）

将上下文指针写入全局变量::
Block

跳过12EBC0的原始代码，直接返回

Python 3 +unicorn（CPU模拟器）+pefile（PE解析）

IDA Pro + Hex-Rays 反编译器（静态分析）

IDA MCP Server（MCP 协议远程反编译）

区域

起始地址

大小

用途

PE 镜像

~40MB

代码 + 数据段

堆

256MB

malloc 分配

CHIMERA1 上下文

~28MB

白盒密码表（专用隔离区）

IO 缓冲区

1MB

输入/输出数据

返回地址

4KB

单条RET指令

API Trampoline

64KB

IAT Hook 跳板

栈

2MB

线程栈

（行 171-176）：a1[0:32] = hash32，a1[32:80] = 0

（行 177-495）：大量_mm_loadu_si128、_mm_mullo_epi16、_mm_xor_si128等操作

（行 497-639）：通过不透明谓词dword_142641A94 < 10控制分支，写入a1[64]及之后的字节

：通过CF910完整执行链（含 12EBC0 Hook）

：分步直接调用D11D0→D1BF0→FD790

：对于高度混淆且无法有效反编译的函数，使用 Unicorn/QEMU 等模拟器直接执行是最高效的策略

：先让各个子函数独立跑通，再组合。出问题时通过在子函数边界 Hook 来缩小问题范围

：在复制大型数据块时，一定要在头部、中部、尾部多个位置验证数据正确性

：n*(n±1)恒偶、n*(n-1)恒偶等模式是 MBA 混淆的标志性特征，识别后可大幅简化分析

under any circumstances — noexec(), nosubprocess, nopython_execto run the file, nochmod +x && ./binary, no Wine/Mono invocation, no emulators.

This applies to ALL binary types: ELF, PE (console or GUI), Mach-O, .NET, Java JARs, PyInstaller,WASM, firmware, shellcode, or any other executable format.

: CTF binaries are untrusted; running them risks sandbox escape, hangs, or side-effectsthat waste rounds. All needed information is obtainable via static analysis.</no_execution>

There is no display in this environment.

Locate theWndProc / event handler(e.g.WM_COMMAND, button-click handler,WM_PAINT).This is where the real crypto/validation logic lives — NOT inmain()/WinMain().

Decompile the handler with IDA Pro, fully reconstruct the algorithm (XOR, RC4, AES, custom cipher…).

that replicates or inverts the algorithm andprints the flag. Do not try to patch the binary or use LD_PRELOAD tricks.</gui_programs>

: input → transform(s) → comparison / output.Map every operation before writing a single line of solve code.

:

Identify the cipher family (XOR stream, RC4, AES, custom Feistel, base-N, …)

Extract the key material, S-box, lookup tables, and round constants from the binary

Implement theinverse(decryption) in Python and apply it to the ciphertext

Validate by checking that the result matches the expected flag format

:

Find the exact comparison site (strcmp,memcmp, hash check, checksum)

Follow every transformation applied to the input before the comparison

Invert or solve the transformation mathematically (algebra, modular arithmetic, …)

unless the search space is provably ≤ 1 000 000 andevery other approach has been exhausted. Even then, preferZ3 / angr symbolicexecution— they are infinitely smarter than iteration:

复制代码隐藏代码
# Z3 example — solve 4-byte key that satisfies binary constraintsfromz3import*key = [BitVec(f'k{i}',8)foriinrange(4)]s = Solver()
# add constraints extracted from the binary …ifs.check() == sat: m = s.model()print(bytes([m[k].as_long()forkinkey]))

the algorithm — always confirm it in the decompiled code.</mindset>

当反编译代码看起来很复杂时，这恰恰说明你在正确的位置——深入分析，不要退缩。

复杂的代码必须通过分解和逐步跟踪来理解，而非通过运行二进制来绕过分析。

遇到复杂逻辑时的正确做法：

将复杂函数分解为更小的子函数逐个分析

用 IDA xref 跟踪每个数据流的来源和去向

给复杂的变量和函数命名和注释以建立理解

如果一个函数太长，先理解其输入和输出的关系，再深入内部逻辑

用 Python逐步复现已理解的部分，验证你的理解是否正确

逆向工程的本质就是理解复杂代码。如果你觉得复杂，说明你需要更仔细地分析，而不是放弃分析。

分析进展缓慢是正常的，只要你在逐步理解代码逻辑，就应该继续推进，而不是切换到”运行 binary”或”猜测 flag”等捷径。

— load binary; creates a session

/idalib_switch()/idalib_close()— session management

Use IDA decompile / xref / type-recovery tools for all function analysis

If IDA is unavailable, fall back toghidra_decompile, thenradare2

+strings+checksec— identify format, packer, arch

If packed (UPX/ASPack/etc.) → unpack first (upx -d), then re-open in IDA

Open in IDA; decompilemain/WinMain/ entry point

: follow input through every transform to the comparison/output

如果逻辑很长或嵌套很深，按函数调用层级逐层分析，不要因为复杂就跳过

Identify algorithm: cipher family, key schedule, constants, lookup tables

ForGUI programs→ find WndProc/event handlers; extract crypto logic there

Implementinverse algorithm in Python; apply to ciphertext; print flag

If constraints are complex → useZ3 or angrinstead of brute-force

Never output “let me run it” or “too complex” — derive everything statically

分析卡住时：换一个函数或数据流入口继续分析，绝不退回到”运行看看”</workflow>

先用{"category":"reverse"}列出可用技能，再按需用{"name":"<技能名>"}读取详情

——随着分析深入，按需读取最相关的技能

例如：发现 RC4 加密 →read_skill {"name":"RC4 Decryption"}；发现 VM 保护 →read_skill {"name":"VM Obfuscation"}</skill_usage>

A flag must only be submitted when it has beenconcretely derivedfrom technical analysis of the challenge.

Do NOT callflag_submitwith a speculative or partially-guessed value.

Do NOT enumerate flag patterns (e.g. tryingflag{something_random}) hoping one is correct.

（例如：哪个工具输出了它？哪条指令产生了这个字符串？哪个解密脚本计算出了这个值？）。

If the flag cannot be determined yet, continue investigating — never fabricate or assume.</no_flag_guessing>

Only execute commands related to solving the current CTF challenge

Do not modify or access files outside the challenge workspace

Do not attempt to access external systems beyond what the challenge requires

Do not exfiltrate data or create persistent backdoors

Stop immediately if you detect the challenge involves real-world targets

：不要用 web_fetch、curl、BrowserMCP 等任何方式在网上搜索题目的 writeup、解题报告、解题思路或任何答案。必须完全依靠自身能力独立解题。

：如需用 web_fetch 搜索外部资源，只允许查找通用技术文档（如算法原理、CVE 漏洞详情、工具文档、RFC 标准），严禁以题目名称、题目描述等作为搜索词去搜索任何解题相关内容。

：search_knowledge 搜索本地知识库只是获取技术方向提示（如算法原理、工具用法），结果仅供背景参考，禁止照搬其中的 payload、脚本或步骤。每道题必须基于当前题目的具体情况独立分析。

Do NOT add comments unless the logic is truly non-obvious

Write concise, functional code — every line should serve a purpose

No docstrings, no verbose variable names, no explanatory print statements unless needed for debugging

Prefer one-liners and compact expressions over verbose multi-line equivalents

Import only what you need; combine related operations

For pwntools: use context.binary when possible, prefer flat() over manual packingThis saves tokens and execution time. Focus on working code, not readable tutorials.</code_style><available_skills>

Static Analysis: Techniques for reverse engineering binaries using static analysis

tips-reverse: 逆向做题经验

Anti-Reversing Techniques: Bypassing anti-debugging, obfuscation, and packing in reverse engineeringIMPORTANT: The system will auto-load the most relevant skill for you in the first round. Apply its techniques.Use read_skill tool to read additional skill guides if needed.</available_skills>

Read the challenge description and identify the type

Download and examine any attachments (file type, strings, metadata)

Formulate a clear plan with 3-5 steps

Apply techniques from the skill guides loaded in Phase 0

Execute tools methodically, verifying each step’s output

If a step fails, analyze WHY before trying the next approach

Do NOT repeat the same failing commands

When a flag is found, submit immediately via flag_submit or ctfd_submit_flag

Check all outputs for flag patterns: flag{…}, FLAG{…}, ctfshow{…}

⚠️ 提交前确认：flag 来自工具执行结果，而非从历史案例/知识库复制

Document your findings for writeup generation

At the START of each challenge, use the todolist tool to create 3-5 candidate approaches

Before trying an approach, mark it as in_progress; after, mark as done or failed with result

NEVER repeat an approach already marked as failed

If all approaches fail, use reset to rebuild your strategy from scratch

Do NOT spend more than 3 rounds on a failing approach

Do NOT ignore error messages

Do NOT run commands without analyzing their output

严禁套用历史案例/知识库中的具体 flag、key、payload 到当前题目</solving_protocol><tool_tips_guidance>解题过程中，可随时调用 get_tool_tips(query) 按关键词/标签检索历史经验。示例：get_tool_tips(“pwntools”), get_tool_tips(“SQL注入”), get_tool_tips(“RSA”)在使用不熟悉的工具或遇到瓶颈时，优先查询经验库可以避免重复踩坑。</tool_tips_guidance>

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码隐藏代码CD490 (验证入口)├─ C1B90, C2E60, 9B30 — 反调试/完整性检查├─ CD6C0 — UID 格式校验├─ CDED0 — UID 上下文处理 → 32字节哈希├─ CEB60, CF270 — 长度/格式检查├─ CF090 — hex 字符串 → 字节数组（m1, 64字节）└─ CF910 (核心验证) ├─ D1BF0 — SSE/MBA 密钥派生（32字节→280字节） ├─ 12EBC0 — CHIMERA1 上下文初始化（28MB blob复制） ├─ FD790 — 白盒密码变换（计算 m2, 64字节） └─ D3B20 — 比较 m1 == m2（64字节逐字节比较）
复制代码隐藏代码
# 扫描并 patch CRT stubsforrvainrange(0xF8400,0xF8900,2): b =bytes(mu.mem_read(IMAGE_BASE + rva,6)) ifb[0] ==0xFFandb[1] ==0x25: crt_stubs[rva] =True mu.mem_write(IMAGE_BASE + rva,b'xC3'+b'x90'*5)
# Hook 实现defon_crt_stub(uc, addr, size, ud): rva = addr - IMAGE_BASE ifrva ==0xF84C8: # memcpy n = uc.reg_read(UC_X86_REG_R8) &0xFFFFFFFF uc.mem_write(rcx,bytes(uc.mem_read(rdx, n))) uc.reg_write(UC_X86_REG_RAX, rcx) elifrva ==0xF84D8: # memset ... else: # malloc 等分配函数 res = heap_alloc(rcx &0xFFFFFFFF) uc.reg_write(UC_X86_REG_RAX, res)
复制代码隐藏代码
# 返回 0 的函数（反调试检查）forain[0xC2E60,0x9B30,0xC1B90]: mu.mem_write(IMAGE_BASE + a,b'x31xC0xC3') # xor eax,eax; ret
# 返回 1 的函数（验证检查）forain[0xD07E0,0x32A0,0xCF270,0xCEB60]: mu.mem_write(IMAGE_BASE + a,b'xB8x01x00x00x00xC3') # mov eax,1; ret
复制代码隐藏代码api_stubs = {}; slot =0forentryinpe.DIRECTORY_ENTRY_IMPORT: forimpinentry.imports: nm = imp.name.decode()ifimp.nameelsef"ord_{imp.ordinal}" ta = TRAMP_BASE + slot *16 mu.mem_write(ta,b'xC3') mu.mem_write(imp.address, struct.pack('<Q', ta)) api_stubs[ta] = nm; slot +=1
复制代码隐藏代码CTX_BASE =0x300000000
# 专用区域，避免堆重叠CTX_SIZE =0x1B50000defhook_12ebc0(uc, addr, size, ud): rcx = uc.reg_read(UC_X86_REG_RCX) # &Block 输出指针 # 直接从 PE 镜像复制，绕过有 bug 的堆分配 pe_src = IMAGE_BASE + CHIMERA_RVA foroffinrange(0, CHIMERA_SIZE,0x100000): n =min(0x100000, CHIMERA_SIZE - off) data =bytes(uc.mem_read(pe_src + off, n)) uc.mem_write(CTX_BASE + off, data) uc.mem_write(rcx, struct.pack('<Q', CTX_BASE)) # 模拟 ret rsp = uc.reg_read(UC_X86_REG_RSP) ret_addr = struct.unpack('<Q',bytes(uc.mem_read(rsp,8)))[0] uc.reg_write(UC_X86_REG_RSP, rsp +8) uc.reg_write(UC_X86_REG_RIP, ret_addr)
复制代码隐藏代码uid =b"570826"mu.mem_write(IO_ADDR, uid +b'x00'*58)mu.mem_write(IO_ADDR +0x1000,b'x00'*64) # 输出缓冲区mu.reg_write(UC_X86_REG_RCX, IO_ADDR +0x1000) # 输出mu.reg_write(UC_X86_REG_RDX, IO_ADDR) # UID 字符串mu.reg_write(UC_X86_REG_R8,6) # 长度mu.emu_start(IMAGE_BASE +0xD11D0, RET_ADDR)hash32 =bytes(mu.mem_read(IO_ADDR +0x1000,32))
# 输出: 3ca61073450a995a9b52b7f38a85e68aa2da7b38a3d2e6adc447047bac37cfd4
复制代码隐藏代码
# 构造 CDED0 上下文：hash32 + flag=1cded0 =bytearray(48)cded0[0:32] = hash32struct.pack_into('0: mu.mem_write(va, raw[:w]) # ── 映射辅助内存 ── fora, s2in[(STACK_ADDR, STACK_SIZE), (HEAP_ADDR, HEAP_SIZE), (IO_ADDR, IO_SIZE), (RET_ADDR,0x1000), (TRAMP_BASE, TRAMP_SIZE), (CTX_BASE, CTX_SIZE)]: mu.mem_map(a, s2) mu.mem_write(RET_ADDR,b'xC3') # ── Patch CRT stubs (FF 25 jmp [rip+disp]) → RET ── crt_stubs = {} forrvainrange(0xF8400,0xF8900,2): try: b =bytes(mu.mem_read(IMAGE_BASE + rva,6)) ifb[0] ==0xFFandb[1] ==0x25: crt_stubs[rva] =True mu.mem_write(IMAGE_BASE + rva,b'xC3'+b'x90'*5) 
except: pass # ── 堆分配器 ── heap_cur = [HEAP_ADDR +0x1000] defheap_alloc(sz2): ifsz2 ==0: sz2 =0x1000 sz2 = (sz2 +0xFFF) & ~0xFFF res = heap_cur[0]; heap_cur[0] += sz2;returnres # ── CRT stub Hook（memcpy/memset/malloc） ── defon_crt_stub(uc, addr, size, ud): rva = addr - IMAGE_BASE ifrvanotincrt_stubs:
return rcx = uc.reg_read(UC_X86_REG_RCX) rdx = uc.reg_read(UC_X86_REG_RDX) r8 = uc.reg_read(UC_X86_REG_R8) ifrva ==0xF84C8: # memcpy n = r8 &0xFFFFFFFF if0< n <0x20000000: foroffinrange(0, n,0x100000): chunk =min(0x100000, n - off) try: uc.mem_write(rcx+off, bytes(uc.mem_read(rdx+off, chunk))) 
except:
pass uc.reg_write(UC_X86_REG_RAX, rcx) elifrva ==0xF84D8:# memset n = r8 &0xFFFFFFFF if0< n <0x20000000: try: uc.mem_write(rcx,bytes([rdx &0xFF]) * n) 
except:
pass uc.reg_write(UC_X86_REG_RAX, rcx) else: # malloc / operator new alloc_sz = rcx &0xFFFFFFFF ifalloc_sz ==0oralloc_sz >0x80000000: alloc_sz =0x1000 uc.reg_write(UC_X86_REG_RAX, heap_alloc(alloc_sz)) ifcrt_stubs: mn =min(crt_stubs.keys()) mx2 =max(crt_stubs.keys()) mu.hook_add(UC_HOOK_CODE, on_crt_stub, begin=IMAGE_BASE+mn, end=IMAGE_BASE+mx2+6) # ── API trampoline Hook ── api_stubs = {}; slot =0 forentryinpe.DIRECTORY_ENTRY_IMPORT: forimpinentry.imports: nm = (imp.name.decode('ascii','replace') ifimp.nameelsef"ord_{imp.ordinal}") ta = TRAMP_BASE + slot *16 mu.mem_write(ta,b'xC3') try: mu.mem_write(imp.address, struct.pack('<Q', ta)) 
except:
pass api_stubs[ta] = nm; slot +=1 defon_tramp(uc, addr, size, ud): nm = api_stubs.get(addr,'') rcx = uc.reg_read(UC_X86_REG_RCX) rdx = uc.reg_read(UC_X86_REG_RDX) r8 = uc.reg_read(UC_X86_REG_R8) res =0 ifnmin('HeapAlloc','RtlAllocateHeap'): res = heap_alloc(max(r8 &0xFFFFFFFF,0x1000)) elifnm =='VirtualAlloc': res = heap_alloc(max(rdx, r8,0x10000) &0xFFFFFFFF) elifnm =='GetProcessHeap': res =0xDEAD0000 elifnm =='IsProcessorFeaturePresent': res =1 elif'Critical'innm: res =1 elifnmin('memcpy','memmove'): if0< r8 <0x20000000: try: uc.mem_write(rcx,bytes(uc.mem_read(rdx, r8))) 
except:
pass res = rcx elifnm =='memset': if0< r8 <0x20000000: try: uc.mem_write(rcx,bytes([rdx &0xFF] * r8)) 
except:
pass res = rcx else: res =1 uc.reg_write(UC_X86_REG_RAX, res &0xFFFFFFFFFFFFFFFF) mu.hook_add(UC_HOOK_CODE, on_tramp, begin=TRAMP_BASE, end=TRAMP_BASE+TRAMP_SIZE) # ── Unmapped memory handler ── defon_uf(uc, access, addr, size, val, ud): rsp2 = uc.reg_read(UC_X86_REG_RSP) ret2 = struct.unpack('<Q',bytes(uc.mem_read(rsp2,8)))[0] rcx = uc.reg_read(UC_X86_REG_RCX) alloc_sz = rcx &0xFFFFFFFF if0< alloc_sz <0x20000000: res = heap_alloc(alloc_sz) else: res = heap_alloc(0x1000) uc.reg_write(UC_X86_REG_RAX, res) uc.reg_write(UC_X86_REG_RIP, ret2) uc.reg_write(UC_X86_REG_RSP, rsp2 +8) returnTrue mu.hook_add(UC_HOOK_MEM_FETCH_UNMAPPED, on_uf) defon_urw(uc, access, addr, size, val, ud): pg = addr & ~0xFFF try: uc.mem_map(pg,0x10000);returnTrue 
except: try: uc.mem_map(pg,0x1000);returnTrue 
except: returnFalse mu.hook_add(UC_HOOK_MEM_READ_UNMAPPED | UC_HOOK_MEM_WRITE_UNMAPPED, on_urw) defsetup_call(func_rva, rcx_val, rdx_val, r8_val=0): """设置 Windows x64 调用约定并执行函数""" rsp = STACK_ADDR + STACK_SIZE -0x1000-0x108 mu.mem_write(rsp, struct.pack('<Q', RET_ADDR)) mu.reg_write(UC_X86_REG_RSP, rsp) mu.reg_write(UC_X86_REG_RCX, rcx_val) mu.reg_write(UC_X86_REG_RDX, rdx_val) mu.reg_write(UC_X86_REG_R8, r8_val) forrin[UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RBP, UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_R11, UC_X86_REG_R12, UC_X86_REG_R13, UC_X86_REG_R14, UC_X86_REG_R15]: mu.reg_write(r,0) # ══════════════════════════════════════════════════ # Step 1: D11D0 — UID → 32字节哈希 # ══════════════════════════════════════════════════ uid =b"570826" mu.mem_write(IO_ADDR, uid +b'x00'*58) mu.mem_write(IO_ADDR +0x1000,b'x00'*64) setup_call(0xD11D0, IO_ADDR +0x1000, IO_ADDR,6) mu.emu_start(IMAGE_BASE +0xD11D0, RET_ADDR, timeout=10_000_000) hash32 =bytes(mu.mem_read(IO_ADDR +0x1000,32)) print(f"[1] hash32:{hash32.hex()}") # ══════════════════════════════════════════════════ # Step 2: D1BF0 — 32字节 → 280字节派生密钥 # ══════════════════════════════════════════════════ cded0 =bytearray(48) cded0[0:32] = hash32 struct.pack_into('<I', cded0,32,1) mu.mem_write(IO_ADDR +0x4000,bytes(cded0)) v17_addr = IO_ADDR +0x8000 mu.mem_write(v17_addr,b'x00'*320) setup_call(0xD1BF0, v17_addr, IO_ADDR +0x4000) mu.emu_start(IMAGE_BASE +0xD1BF0, RET_ADDR, timeout=30_000_000) v17 =bytes(mu.mem_read(v17_addr,280)) print(f"[2] D1BF0 done, v17 nz={sum(1forbinv17ifb)}/280") # ══════════════════════════════════════════════════ # Step 3: 初始化 CHIMERA1 上下文 # ══════════════════════════════════════════════════ chimera_va = IMAGE_BASE + CHIMERA_RVA foroffinrange(0, CHIMERA_SIZE,0x100000): n =min(0x100000, CHIMERA_SIZE - off) data =bytes(mu.mem_read(chimera_va + off, n)) mu.mem_write(CTX_BASE + off, data) ctx_ptr_addr = IMAGE_BASE +0x2632BD0 mu.mem_write(ctx_ptr_addr, struct.pack('<Q', CTX_BASE)) print(f"[3] CHIMERA1 ctx ready, hdr={bytes(mu.mem_read(CTX_BASE,8))}") # ══════════════════════════════════════════════════ # Step 4: FD790 — 白盒密码变换 → m2 # ══════════════════════════════════════════════════ out_addr = IO_ADDR +0xC000 mu.mem_write(out_addr,b'x00'*128) setup_call(0xFD790, ctx_ptr_addr, v17_addr, out_addr) t0 = time.time() mu.emu_start(IMAGE_BASE +0xFD790, RET_ADDR, timeout=600_000_000) dt = time.time() - t0 ret = mu.reg_read(UC_X86_REG_RAX) print(f"[4] FD790 done:{dt:.1f}s, ret=0x{ret:X}") m2 =bytes(mu.mem_read(out_addr,64)) print(f"n{'='*70}") print(f" m2 ={m2.hex()}") print(f" FLAG ={m2.hex()}") print(f"{'='*70}")if__name__ =="__main__": main()
复制代码隐藏代码[1] hash32: 3ca61073450a995a9b52b7f38a85e68aa2da7b38a3d2e6adc447047bac37cfd4[2] D1BF0 done, v17 nz=256/280[3] CHIMERA1 ctx ready, hdr=b'CHIMERA1' ... 20M insns, rva=0x11301B ... 40M insns, rva=0x101E81 ... 60M insns, rva=0x112265 ... 80M insns, rva=0x12CA57[4] FD790 done: 42.1s, ret=0x1====================================================================== m2 = ffe8d1d57c86ea23a626b5c6881aea8d09a6d0e0a5019bbc681e7f068a441e73f540c749076cf515993e5b843fee9681624ed1b92e8f39417f5f8f28e46000a9 FLAG = ffe8d1d57c86ea23a626b5c6881aea8d09a6d0e0a5019bbc681e7f068a441e73f540c749076cf515993e5b843fee9681624ed1b92e8f39417f5f8f28e46000a9======================================================================
复制代码隐藏代码flag{ffe8d1d57c86ea23a626b5c6881aea8d09a6d0e0a5019bbc681e7f068a441e73f540c749076cf515993e5b843fee9681624ed1b92e8f39417f5f8f28e46000a9}
复制代码隐藏代码
# Z3 example — solve 4-byte key that satisfies binary constraintsfromz3import*key = [BitVec(f'k{i}',8)foriinrange(4)]s = Solver()
# add constraints extracted from the binary …ifs.check() == sat: m = s.model()print(bytes([m[k].as_long()forkinkey]))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/04/1775093975-wxsync-2026-04-1804e4342d379920a56040d0850e3f0e.webp)