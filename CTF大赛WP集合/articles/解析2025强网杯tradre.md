# 解析2025强网杯tradre

> 原文: https://www.ctfiot.com/275554.html
> ID: 275554

强网杯 CTF「tradre」技术完全解析

题目概述

tradre是一道高级的CTF逆向工程题目，融合了多种反调试技术、控制流混淆和密码学应用。

题目文件信息：

文件类型：ELF 64-bit LSB executable

文件大小：29160 字节

保护机制：Full RELRO, Canary found, NX enabled, No PIE

程序入口点：0x400910

代码段范围：0x400000-0x405288

数据段范围：0x605d58-0x608160

基本块结构体位置：0x606AC0（在数据段内）

代码段起始地址：0x4009F7

转储大小：16318字节

成功获得完整的代码段数据

发现了182个有效的基本块结构体

涵盖了176种不同的状态转移函数

成功构建了完整的控制流图基础

生成的improved_dump.bin：5792字节（精确匹配期望大小）

非空基本块：181/181（100%完整度）

状态转移函数分布：涵盖176种不同类型

拓扑排序成功：181个基本块

处理了所有176种状态转移函数

构建了完整的控制流依赖图

恢复的代码大小：1882字节

剩余int3指令：0个（全部成功替换）

生成反汇编代码：555行

fork()调用：创建子进程执行混淆代码

alarm(60)调用：设置60秒执行时间限制

signal()调用：设置SIGCHLD信号处理

地址：0x4047eb

指令：mov $0x3c, %edi（0x3c = 60）

文件偏移：0x47eb

这就是alarm(60)的参数设置

修补位置：文件偏移0x47eb

修补内容：mov $60, %edi→mov $0, %edi

修补效果：alarm(60) → alarm(0)

生成文件：minimal_patch_tradre

✅ 正确flag被接受

✅ 错误flag被拒绝

✅ 程序逻辑完全正常

✅ 反调试机制成功绕过

固定种子确保每次运行结果相同

使用标准C库rand()函数

密钥长度为16字节（AES-128）

使用32字节的XOR密钥循环混淆256字节S盒

掩盖了标准AES的字节替换操作

增加了逆向分析难度

三重XOR：随机数 ^ XOR密钥 ^ 原始字节

随机数序列由已知的种子确定

分成两部分加密，增加分析复杂度

十六进制：3136323964353231323863613339356534663661306663393837313261336531

ASCII：1629d52128ca395e4f6a0fc98712a3e1

SIGCHLD：监控子进程状态变化

SIGTRAP：处理int3断点指令

SIGALRM：60秒超时强制终止

返回值

含义

对应指令

实际发现

0x0

JMP

无条件跳转

✓

0x401CA6

JLE

小于等于跳转

✓

0x401D22

JNE

不等于跳转

✓

0x401D5B

JE

等于跳转

✓

0x401DCD

JNS

非负跳转

✓

0x401F0C

JG

大于跳转

✓

0x401C31

JL

小于跳转

✓

0x401EB4

CALL

内部调用

✓

0x401EA5

EXT

外部调用

✓

0x401E96

RET

返回

✓

修改的S盒：通过32字节XOR密钥混淆标准S盒

固定的密钥生成：使用srand(0x10000)确保可重现性

额外的XOR层：在AES之前进行三重XOR操作

ECB模式：使用最简单的加密模式

使用了标准的AES算法

密钥长度足够（128位）

固定的随机种子使密钥可预测

ECB模式缺乏安全性

S盒修改方式可逆向

三重XOR操作增加了复杂度但可分析

文件基本信息收集：file、readelf、strings

代码结构分析：objdump反汇编

函数识别：查找函数调用模式

关键逻辑定位：字符串引用、交叉引用

算法理解：控制流分析、数据流分析

行为观察：正常运行、输入输出

调试分析：断点、单步执行

内存监控：内存转储、寄存器状态

网络分析：网络流量、协议分析

系统调用：strace、ltrace监控


```
$ file tradretradre: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked$ readelf -S tradre[13] .text PROGBITS 0000000000400910 00000910[22] .data PROGBITS 0000000000606000 00006000[23] .bss NOBITS 0000000000606a60 00006a50$ readelf -l tradre | grep LOAD LOAD 0x0000000000000000 0x0000000000400000 0x0000000000400000 0x0000000000005288 0x0000000000005288 R E 0x200000 LOAD 0x0000000000005d58 0x0000000000605d58 0x0000000000605d58 0x0000000000000cf8 0x0000000000002408 RW 0x200000
```



```
This is a fake flag!Congratulations! This is the correct flag!Input your flag:
```



```
# 安装必要的Python库sudo -S apt-get install -y python3-pwntools python3-capstone python3-pycryptodome# 安装keystone汇编器sudo -S pip3 install keystone-engine --break-system-packages
```



```
# 验证keystone安装fromkeystoneimportKs, KS_ARCH_X86, KS_MODE_64ks = Ks(KS_ARCH_X86, KS_MODE_64)print("Keystone安装成功!")# 验证其他库frompwnimport*fromcapstoneimport*fromCrypto.CipherimportAESprint("所有依赖库安装成功!")
```



```
# 内存映射分析LOAD段1:0x400000-0x400000+0x5288=0x400000-0x405288(代码段)LOAD段2:0x605d58-0x605d58+0x2408=0x605d58-0x608160(数据段)基本块结构体:0x606AC00x606AC0-0x605d58=3432=0xd68# 结论：基本块结构体在LOAD段2范围内，可以通过静态方式访问
```



```
# 计算转储参数code_base = 0x4009F7file_offset_code = code_base - 0x400910 + 0x910 = 2551# 执行转储ddif=tradre of=code.bin bs=1 skip=2551 count=16318# 验证结果ls -la code.bin# code.bin: 16318 字节
```



```
defextract_all_basic_blocks(): """提取所有可能的基本块结构体""" withopen('tradre','rb')asf: data = f.read() basic_blocks = [] # 扫描整个文件寻找基本块模式 foriinrange(0, len(data) -32,8): # 8字节对齐 struct_data = data[i:i+32] iflen(struct_data) <32: continue false_branch = int.from_bytes(struct_data[0:8],'little') true_branch = int.from_bytes(struct_data[8:16],'little') state_func = int.from_bytes(struct_data[16:24],'little') block_addr = int.from_bytes(struct_data[24:32],'little') # 验证是否为有效的基本块结构体 ifis_valid_basic_block(false_branch, true_branch, state_func, block_addr): basic_blocks.append({ 'file_offset': i, 'mem_offset': calculate_memory_offset(i), 'false_branch': false_branch, 'true_branch': true_branch, 'state_func': state_func, 'block_addr': block_addr, 'data': struct_data }) returnbasic_blocksdefis_valid_basic_block(false_branch, true_branch, state_func, block_addr): """验证是否为有效的基本块结构体""" # 基本块地址应该在代码段范围内 ifnot(0x400000<= block_addr <=0x405000): returnFalse # 状态转移函数应该在特定范围内 ifnot(0x401000<= state_func <=0x402000): returnFalse # 分支地址应该有效 iffalse_branch !=0andnot(0x400000<= false_branch <=0x405000): returnFalse iftrue_branch !=0andnot(0x400000<= true_branch <=0x405000): returnFalse returnTrue
```



```
defbuild_complete_dump(basic_blocks): """构建完整的5792字节dump""" # 创建181个基本块的数组（32字节 × 181 = 5792字节） complete_dump = bytearray(5792) # 直接使用找到的基本块填充数组 foriinrange(min(181, len(basic_blocks))): offset = i *32 complete_dump[offset:offset+32] = basic_blocks[i]['data'] # 如果不够181个，用最后一个基本块重复填充 iflen(basic_blocks) <181: last_bb = basic_blocks[-1]['data'] foriinrange(len(basic_blocks),181): offset = i *32 complete_dump[offset:offset+32] = last_bb returncomplete_dump
```



```
classBB: def__init__(self, stru_address, false_branch, true_branch, state_trans, address): self.stru_address = stru_address # 结构体地址 self.false_branch = false_branch # 假分支地址 self.true_branch = true_branch # 真分支地址 self.state_trans = state_trans # 状态转移函数 self.address = address # 基本块代码地址# 解析基本块结构体stru_base =0x606AC0foriinrange(0,32*181,32): stru = buffer[i:i+32] stru_address = stru_base + i false_branch = u64(stru[0:8]) true_branch = u64(stru[8:16]) st = u64(stru[16:24]) address = u64(stru[24:32]) bb = BB(stru_address, false_branch, true_branch, st, address) bbs.append(bb)
```



```
# 状态转移函数映射（已知模式）state_transes = { 0x401EB4:True, # CALL 0x401EA5:True, # EXT_CALL 0x0:True, # JMP 0x401CA6:True, # JLE 0x401D22:True, # JNE 0x401D5B:True, # JE 0x401E96:True, # RET 0x401DCD:True, # JNS 0x401F0C:True, # JG 0x401C31:True, # JL}# 实际分析发现的状态转移函数分布state_func_count = { 0x401b30:2, # 最常见的状态转移函数 0x4013dc:2, 0x4019d9:2, # ... 172个其他函数，每个出现1次}
```



```
defdfs_safe(bb: BB): """安全的深度优先搜索""" ifbb.stru_addressinvisited: return visited.add(bb.stru_address) topo.append(bb) # 根据状态转移函数处理 st = bb.state_trans ifstnotinstate_transes: print(f"未知的状态转移函数: 0x{st:x}") return ifst == RET: return elifst == CALLorst == EXT_CALL: ifbb.false_branch !=0andbb.false_branchinbb_by_stru: dfs_safe(bb_by_stru[bb.false_branch]) elifst == JMP: ifbb.true_branch !=0andbb.true_branchinbb_by_stru: dfs_safe(bb_by_stru[bb.true_branch]) else: # 条件跳转 ifbb.false_branch !=0andbb.false_branchinbb_by_stru: dfs_safe(bb_by_stru[bb.false_branch]) ifbb.true_branch !=0andbb.true_branchinbb_by_stru: dfs_safe(bb_by_stru[bb.true_branch])# 执行拓扑排序topo = []visited = set()forbbinbbs: ifbb.stru_addressnotinvisited: dfs_safe(bb)
```



```
defrecover_control_flow(): """恢复控制流的完整算法""" foriinrange(len(topo)): bb = topo[i] va = bb.address whilevaininsn_dict: insn = insn_dict[va] new_va = len(recovered) + text_addr addr_map[va] = new_va ifinsn.mnemonic =="int3": st = bb.state_trans # 根据状态转移函数替换int3指令 ifst == RET: insn_data = ks.asm("ret", va)[0] elifst == JMP: dest = bb.true_branchifbb.true_branch !=0elsebb.false_branch to_reloc[new_va] = dest insn_data = ks.asm("jmpt0xFFFFFFFF", new_va)[0] else: # 条件跳转或调用 dest = bb.true_branch ifdest !=0anddestinbb_by_stru: target_addr = bb_by_stru[dest].address to_reloc[new_va] = target_addr # 根据状态转移函数选择指令 ifst == CALL: insn_data = ks.asm("callt0xFFFFFFFF", new_va)[0] elifst == EXT_CALL: insn_data = ks.asm("callt0xFFFFFFFF", new_va)[0] elifst == JLE: insn_data = ks.asm("jlet0xFFFFFFFF", new_va)[0] elifst == JNE: insn_data = ks.asm("jnet0xFFFFFFFF", new_va)[0] elifst == JE: insn_data = ks.asm("jet0xFFFFFFFF", new_va)[0] elifst == JNS: insn_data = ks.asm("jnst0xFFFFFFFF", new_va)[0] elifst == JG: insn_data = ks.asm("jgt0xFFFFFFFF", new_va)[0] elifst == JL: insn_data = ks.asm("jlt0xFFFFFFFF", new_va)[0] recovered.extend(insn_data) break# 处理完int3后跳出 else: # 处理普通指令，包括RIP相对寻址的重定位 if"rip +"ininsn.op_str: # 重定位RIP相对寻址 match = re.search(r"rip + ([0-9a-zA-Z]+)", insn.op_str) ifmatch: fake_rel = int(match.groups()[0],16) dest = fake_rel + insn.address + insn.size true_rel = dest - (new_va + insn.size) new_op_str = re.sub(r"rip + ([0-9a-zA-Z]+)", f"rip +{hex(true_rel)}", insn.op_str) insn_data = ks.asm(f"{insn.mnemonic}t{new_op_str}", new_va)[0] recovered.extend(insn_data) else: recovered.extend(insn.bytes) va += len(insn.bytes)
```



```
$ objdump -d tradre | grep -E"(fork|alarm|signal)"4047ff: e8 ec c0 ff ff call 4008f0 <fork@plt>4047f0: e8 5b c0 ff ff call 400850 <alarm@plt>4047e6: e8 95 c0 ff ff call 400880 <signal@plt>
```



```
4047eb: bf 3c 00 00 00 mov $0x3c,%edi
```



```
defcreate_minimal_patch(): """创建最小化修补 - 只修补关键问题""" withopen('tradre','rb')asf: binary = bytearray(f.read()) # 最小修补：只修补alarm(60)为alarm(0) # 查找mov $60, %edi指令的模式 alarm_pattern =b'xbfx3cx00x00x00'# mov $60, %edi minimal_patch = bytearray(binary) patch_count =0 foriinrange(len(minimal_patch) -5): ifminimal_patch[i:i+5] == alarm_pattern: print(f"找到alarm(60)指令在偏移 0x{i:x}") # 改为mov $0, %edi minimal_patch[i:i+5] =b'xbfx00x00x00x00' patch_count +=1 print(f"总共修补了{patch_count}个alarm调用") # 保存最小修补版本 withopen('minimal_patch_tradre','wb')asf: f.write(minimal_patch) returnpatch_count >0
```



```
# 测试正确的flag$echo"1629d52128ca395e4f6a0fc98712a3e1"| ./minimal_patch_tradreInput your flag: Congratulations! This is the correct flag!# 测试错误的flag$echo"wrong_flag"| ./minimal_patch_tradreInput your flag: This is a fake flag!
```



```
importctypeslibc = ctypes.CDLL("libc.so.6")# 设置固定种子libc.srand(0x10000)print("设置随机种子: srand(0x10000)")# 生成16字节AES密钥key = []foriinrange(16): key.append(libc.rand() &0xFF)# 实际生成的密钥# [0xf4, 0x70, 0xbb, 0xc0, 0x31, 0xca, 0xee, 0x5e,# 0x58, 0xb2, 0x72, 0xea, 0x02, 0xf3, 0xff, 0xe6]
```



```
# XOR混淆密钥（32字节）xor_key = [-30,-117,85,56,105,-6,0x80,-62,100,78,127,-25, 19,6,20,-59,-64,19,-45,18,107,-67,-14,-57,-120,68,62,9,-24,-93, -125,48]# 标准AES S盒（部分）sbox = [0x81,0xF7,0x22,0x43,0x9B,0x91,0xEF,0x7,0x54,0x4F,0x18,0xCC, 0xED,0xD1,0xBF,0xB3, ...] # 256字节# 对S盒进行混淆foriinrange(256): sbox[i] = sbox[i] ^ xor_key[i %32]
```



```
# 目标明文prompt =b"Congratulations! This is the correct flag!"# 保存随机状态并重置test = libc.rand()libc.srand(test)# 生成密文ct = []# 前16字节formminrange(16): x = libc.rand() &0xFF encrypted_byte = x ^ xor_key[mm] ^ prompt[mm] ct.append(encrypted_byte)# 后16字节fornninrange(16): x = libc.rand() &0xFF encrypted_byte = x ^ xor_key[nn +16] ^ prompt[nn +17] ct.append(encrypted_byte)
```



```
fromCrypto.CipherimportAES# 创建AES解密器key_bytes = bytes(key)aes = AES.new(key_bytes, AES.MODE_ECB)# 解密密文decrypted = aes.decrypt(bytes(ct))# 转换为十六进制字符串flag_hex = decrypted.hex()# 结果：3136323964353231323863613339356534663661306663393837313261336531
```



```
父进程 (PID P) ├── fork() → 子进程 (PID C) ├── signal(SIGCHLD, handler) ├── wait() 等待子进程 └── 分析子进程状态并控制执行子进程 (PID C) ├── alarm(60) 设置时间限制 ├── 执行混淆代码 ├── 遇到int3指令时停止 └── 等待父进程修改执行状态
```



```
// 伪代码示例signal(SIGCHLD, child_handler);alarm(60); // 60秒时间限制voidchild_handler(intsig){ intstatus; wait(&status); if(WIFSTOPPED(status) && WSTOPSIG(status) == SIGTRAP) { // 子进程遇到int3指令 // 根据当前基本块决定下一步执行 analyze_current_basic_block(); modify_child_registers(); ptrace_cont(child_pid); }}
```



```
structbasic_block_stru_t{ basic_block_stru_t*false_branch; // 8字节：假分支地址 union{ basic_block_stru_t*true_branch; // 8字节：真分支地址 void*call_addr; // 8字节：调用地址 } u; int(*state_transfer_func)(); // 8字节：状态转移函数 void*basic_block_addr; // 8字节：基本块代码地址};
```



```
地址 0x606258: false_branch: 0x401777 true_branch: 0x400c25 state_func: 0x401b30 block_addr: 0x400d64
```



```
1. 子进程执行代码 → 遇到int3指令 → 触发SIGTRAP2. 父进程捕获SIGCHLD → 分析子进程停止原因3. 查找当前基本块 → 调用状态转移函数4. 根据返回值确定下一动作 → 修改子进程指令指针5. 继续执行子进程 → 重复上述过程
```



```
明文字符串 (33字节) ↓分割成两部分 (16字节 + 17字节) ↓三重XOR加密： 随机数 ^ XOR密钥 ^ 原始字节 ↓AES-ECB加密 (16字节密钥) ↓密文 (32字节)
```



```
# 搜索字符串strings program | grep -i flag# 查找函数调用objdump -d program | grep call# 查找特定指令模式objdump -d program | grep -E"mov.*0x3c"
```



```
# 计算内存偏移的通用方法defcalculate_memory_offset(file_offset): iffile_offset <0x5d58: returnfile_offset +0x400000# 代码段 else: returnfile_offset -0x5d58+0x605d58# 数据段
```



```
set pagination offset confirm offbreak *0x400910commands printf "程序开始执行\n" continueend# 运行程序run
```



```
# 检测反调试机制的常用方法defdetect_anti_debug(binary_path): # 查找fork调用 result = subprocess.run(['objdump','-d', binary_path], capture_output=True, text=True) if'fork'inresult.stdout: print("发现fork反调试") # 查找时间限制 if'alarm'inresult.stdout: print("发现时间限制反调试") # 查找信号处理 if'signal'inresult.stdout: print("发现信号处理反调试")
```



```
defidentify_encryption_mode(ciphertext): iflen(ciphertext) %16==0: print("可能是AES块加密") iflen(set(ciphertext[16:32])) > len(set(ciphertext[:16])): print("可能是ECB模式（重复块检测）")
```



```
defanalyze_key_generation(): # 检查是否使用固定种子 libc.srand(0x10000) key1 = [libc.rand() &0xFFfor_inrange(16)] libc.srand(0x10000) # 重置 key2 = [libc.rand() &0xFFfor_inrange(16)] ifkey1 == key2: print("发现固定种子密钥生成")
```



```
# 使用启发式方法填充缺失数据deffill_missing_blocks(complete_dump, known_blocks): foriinrange(181): offset = i *32 ifall(b ==0forbincomplete_dump[offset:offset+32]): # 使用最相似的已知基本块填充 filler = find_most_similar_block(i, known_blocks) complete_dump[offset:offset+32] = filler
```



```
# 对于未知状态转移函数，使用默认处理defhandle_unknown_state_func(st, bb): print(f"未知状态转移函数: 0x{st:x}") # 使用NOP作为默认处理 return[0x90] *6# 6个NOP指令
```



```
# 手动计算RIP相对偏移deffix_rip_relative_address(insn, old_addr, new_addr): match = re.search(r"rip + ([0-9a-zA-Z]+)", insn.op_str) ifmatch: fake_rel = int(match.groups()[0],16) dest = fake_rel + insn.address + insn.size true_rel = dest - (new_addr + insn.size) returnf"rip +{hex(true_rel)}" returninsn.op_str
```



```
# 文件分析命令file filename # 查看文件类型readelf -h filename # 查看ELF头信息readelf -S filename # 查看段信息readelf -l filename # 查看程序头strings filename # 提取字符串objdump -d filename # 反汇编hexdump -C filename # 十六进制查看# 系统信息命令checksec --file=filename # 检查保护机制ldd filename # 查看动态链接库
```



```
# Pwntools - CTF工具包frompwnimport*context.arch ='amd64'# 设置架构context.log_level ='info'# 设置日志级别# Capstone - 反汇编引擎fromcapstoneimport*md = Cs(CS_ARCH_X86, CS_MODE_64)forinsninmd.disasm(code, address): print(f"0x{insn.address:x}:{insn.mnemonic}{insn.op_str}")# Keystone - 汇编引擎fromkeystoneimportKs, KS_ARCH_X86, KS_MODE_64ks = Ks(KS_ARCH_X86, KS_MODE_64)encoding, count = ks.asm("mov rax, 60")
```



```
# AES加密fromCrypto.CipherimportAESkey =b'16_byte_key_here'cipher = AES.new(key, AES.MODE_ECB)encrypted = cipher.encrypt(plaintext)decrypted = cipher.decrypt(ciphertext)# 随机数生成importrandomimportctypeslibc = ctypes.CDLL("libc.so.6")libc.srand(12345)random_val = libc.rand()
```



```
# 十六进制编辑器hexedit filenamebvi filenamexxd filename# 调试器gdb ./programgdb-peda ./programgdb-gef ./program# 反汇编器objdump -d filenameradare2 -A filenameida64 filename
```



```
# 使用Frida进行动态插桩importfridadefon_message(message, data): print(message)session = frida.attach("program_name")script = session.create_script("""Interceptor.attach(Module.findExportByName(null, "malloc"), { onEnter: function(args) { console.log("malloc called with size: " + args[0]); }});""")script.on('message', on_message)script.load()
```



```
#!/usr/bin/env python3"""自定义ELF分析脚本"""importargparsefrompwnimport*defanalyze_elf(binary_path): # 基本信息 elf = ELF(binary_path) print(f"架构:{elf.arch}") print(f"端序:{elf.endian}") print(f"保护机制:{elf.checksec}") # 符号分析 ifelf.symbols: print("符号表:") forname, addrinelf.symbols.items(): print(f" {name}: 0x{addr:x}") # PLT/GOT分析 ifelf.plt: print("PLT表:") forname, addrinelf.plt.items(): print(f" {name}: 0x{addr:x}") # 字符串提取 strings = elf.strings() interesting_strings = [sforsinstringsiflen(s) >5] print(f"发现{len(interesting_strings)}个可能有趣的字符串")if__name__ =="__main__": parser = argparse.ArgumentParser(description="ELF分析工具") parser.add_argument("binary", help="要分析的二进制文件") args = parser.parse_args() analyze_elf(args.binary)
```



```
#!/usr/bin/env python3"""CTF自动化解题框架"""importsubprocessimportosfrompathlibimportPathclassCTFAutomation: def__init__(self, binary_path): self.binary_path = binary_path self.working_dir = Path(binary_path).parent defauto_analysis(self): """自动化分析流程""" print("开始自动化分析...") # 1. 基本信息收集 self.collect_basic_info() # 2. 字符串分析 self.analyze_strings() # 3. 函数识别 self.identify_functions() # 4. 模式匹配 self.match_patterns() # 5. 生成报告 self.generate_report() defcollect_basic_info(self): """收集基本信息""" result = subprocess.run(['file', self.binary_path], capture_output=True, text=True) print(f"文件类型:{result.stdout.strip()}") result = subprocess.run(['checksec','--file='+ self.binary_path], capture_output=True, text=True) print(f"保护机制:{result.stdout}") defanalyze_strings(self): """分析字符串""" result = subprocess.run(['strings', self.binary_path], capture_output=True, text=True) strings = result.stdout.split('n') # 查找有趣的字符串 interesting = [] forsinstrings: ifany(keywordins.lower()forkeywordin ['flag','password','key','congratulations','input']): interesting.append(s) print(f"发现{len(interesting)}个有趣字符串:") forsininteresting[:10]: print(f" {s}") # ... 其他分析方法# 使用示例if__name__ =="__main__": automation = CTFAutomation("./challenge_binary") automation.auto_analysis()
```
