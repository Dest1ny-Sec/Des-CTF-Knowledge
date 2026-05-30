# 解析2025强网拟态HyperJump

> 原文: https://www.ctfiot.com/276936.html
> ID: 276936

CTF逆向题目：HyperJump 深度技术解析

一、题目背景与初步分析

1.1 题目描述

组织使用了一个定制的虚拟机程序来保护他们的秘密。你需要找到能够通过验证的口令。有时候，最复杂的迷宫也有它的规律…

这是一道典型的逆向工程题目，涉及到自定义虚拟机和口令验证机制。题目提示”最复杂的迷宫也有它的规律”，暗示我们需要找到验证逻辑中的模式。

1.2 环境准备

在开始分析之前，我们需要准备以下工具：

radare2或IDA Pro/Ghidra：用于反汇编和反编译

objdump：快速查看汇编代码

Python 3：编写自动化脚本

Linux环境：题目程序为ELF格式

64位ELF可执行文件：需要在Linux x64环境下运行

PIE (Position Independent Executable)：地址随机化，增加分析难度

stripped：符号信息已被去除，无法直接看到函数名

使用反反调试技术（如修改ptrace返回值）

纯静态分析（本文采用的方法）

Patch掉反调试代码

查找表访问：从预设的数据表中读取值

多种位运算：XOR、ROL、ROR等

SIMD指令：使用SSE指令（movd, punpckldq等）

最终比较：将计算结果与预期值（存储在地址0x5420+r15处）比较

增加静态分析难度

防止简单的字符串搜索找到答案

实现类似虚拟机的字节码解释执行

r15递增1，指向下一个字符

检查是否已验证24个字符

全部通过则打印成功消息，返回0

打印”Nope, try again.”

设置返回码为1

直接返回（不继续验证后续字符）

程序逐字符验证flag

一旦某个字符错误，立即返回失败

r15寄存器保存了当前验证到第几个字符

尝试每个位置的所有可能字符（0-9, a-z, A-Z, 符号等）

观察返回码（即r15的值）

返回码最大的字符就是正确的字符

重复步骤1-3直到找到完整的24字符flag

mov eax, 0x1的机器码是：b8 01 00 00 00(5字节)

b8：mov eax, imm32 的opcode

01 00 00 00：立即数1（小端序）

mov eax, r15d的机器码是：44 89 f8(3字节)

44：REX前缀，表示使用扩展寄存器r15

89：mov r/m32, r32 的opcode

f8：ModR/M字节，指定 eax ← r15d

r15的值在失败时仍然保留：虽然跳转到了0x1440，但r15寄存器的值没有被修改，它仍然保存着验证失败的位置。

修改返回值不影响程序逻辑：我们只是改变了返回给操作系统的退出码，程序的其他逻辑完全不变。

技术上合理：返回码是程序与外界通信的标准方式，通过$?或subprocess的returncode可以读取。

第1个字符’f’正确 → 返回码从0变为1

前2个字符”fl”正确 → 返回码变为3（注意不是2！）

前4个字符”flag”正确 → 返回码为4

前5个字符”flag{“正确 → 返回码为5

跳跃式验证（类似虚拟机的跳转指令）

多字节一组的验证

某些字符被多次验证

时间复杂度：O(n × m)，其中n是flag长度（24），m是字符集大小（约95个可打印ASCII字符）

最坏情况：24 × 95 = 2,280次程序执行

实际情况：由于验证可能跳跃，可能更快

文件格式识别：使用file命令判断架构和链接方式

反汇编技术：使用objdump、radare2等工具

符号剥离处理：手动定位main函数（通过__libc_start_main调用）

PIE程序分析：理解位置无关代码的地址计算

函数调用约定：参数传递（rdi, rsi, rdx等）、返回值（rax）

寄存器用途：

r15：本题中用作循环索引

rax,rbx,rcx,rdx：通用寄存器，用于各种计算

rdi,rsi：函数参数寄存器

控制流指令：

cmp+jne：条件跳转

call/ret：函数调用

SIMD指令：movd,punpckldq等SSE指令用于数据处理

指令编码：理解x86-64机器码格式

Opcode（操作码）

ModR/M字节（指定操作数）

REX前缀（访问扩展寄存器r8-r15）

Patch策略：

同长度替换（最简单）

短指令+NOP填充（本题方法）

长指令需要跳转表（复杂场景）

工具选择：

Python脚本：适合简单patch

专业工具：IDA Pro的Keypatch插件、Binary Ninja等

泄露信息：程序失败时r15寄存器的值

利用方式：通过修改程序返回该值

攻击效果：将指数级爆破（95^24）降低到线性级（95×24）

时序攻击：通过响应时间差异判断（如strcmp提前退出）

缓存攻击：Spectre/Meltdown等CPU漏洞

功耗分析：智能卡密码学攻击

subprocess模块：Python中运行外部程序并获取返回码

贪心算法：逐位选择最优解

字符集遍历：使用string.printable覆盖所有可打印字符

限制尝试次数：lockout机制

添加延时：每次验证失败后sleep

组合验证：不单独验证每个字符，而是验证整体hash

完整性检查：程序自检测代码段hash

虚拟化保护：使用商业壳（VMProtect等）

代码混淆：增加静态分析难度（本题已使用）

先动后静：先运行程序了解行为，再静态分析

字符串搜索：快速定位关键代码

模式识别：识别常见算法（Base64/AES/TEA等）

脚本自动化：重复性工作必须自动化

多工具结合：不同工具有各自优势

复杂的代码混淆可以增加分析难度

但如果验证逻辑本身存在缺陷（如侧信道泄露），再复杂的混淆也无济于事

安全的本质在于算法和架构，而非复杂度

x86-64 ABI规范：理解函数调用约定

Intel开发者手册：指令集参考

CTF Wiki：逆向工程技巧总结

《Reverse Engineering for Beginners》：Dennis Yurichev著，免费电子书

《Practical Binary Analysis》：实用二进制分析指南


```
$ file hyperjumphyperjump: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV),dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,forGNU/Linux 3.2.0, stripped
```



```
$ ./hyperjumpProvide the flag:testNope, try again.
```



```
importsubprocessp = subprocess.Popen('./hyperjump', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)stdout, stderr = p.communicate(input='test')print(f"Return code:{p.returncode}") # 输出: Return code: 1
```



```
$ strings hyperjump | grep -E"(flag|Flag|congratulations|Congratulations|Nope|Provide)"Provide the flag:Nope, try again.Correct flag, congratulations!
```



```
$ objdump -d hyperjump -M intel | grep -A 15"entry0"
```



```
1484: 48 8d 3d 75 fc ff ff lea rdi,[rip+0xfffffffffffffc75]148b: ff 15 2f 6b 00 00 call QWORD PTR [rip+0x6b2f]
```



```
$ objdump -d hyperjump -M intel | grep -A 100"1100 <"
```



```
1119: lea rdi,[rip+0x451d] # "Provide the flag:"1120: call 1050 <puts@plt> # 打印提示信息1125: lea rax,[rbp-0xb0] # 输入缓冲区地址112c: mov esi,0x80 # 缓冲区大小128字节1131: mov rdx,QWORD PTR [rip+0x6f38] # stdin1138: mov rdi,rax1142: call 1090 <fgets@plt> # 读取输入1157: call 1080 <strlen@plt> # 获取输入长度
```



```
1165: cmp BYTE PTR [rbp+rax*1-0xb1],0xa # 检查是否有换行符116d: lea rdx,[rax-0x1] # 去除换行符1171: je 11761173: mov rdx,rax # 保留原长度1176: cmp rdx,0x18 # 比较长度是否为24 (0x18)117a: jne 1440 # 长度不对跳转到失败处理
```



```
1180: xor eax,eax # eax = 01182: mov r15d,0xb # r15 = 11 (临时值)1188: xor edi,edi # edi = 0...11b2: mov QWORD PTR [rbp-0xe8],r15 # 保存r1511b9: mov r15,rdi # r15 = 0 (作为循环索引)
```



```
11c0: mov rax,QWORD PTR [rbp-0x100] # 获取输入字符串地址11c7: movzx ebx,BYTE PTR [rax+r15*1] # 读取第r15个字符到ebx11cc: call 4350 # 调用反调试函数
```



```
11d1: lea rcx,[rip+0x43c8] # 加载查找表1地址11d8: lea rdx,[r15+r15*2+0x5] # rdx = r15*3 + 511e4: mov eax,DWORD PTR [rcx+r15*4] # 从查找表读取值11e8: movzx esi,bl # esi = 当前输入字符11fc: xor eax,esi # 异或运算...[省略中间大量运算指令]...13f3: cmp BYTE PTR [rdi+r15*1],al # 比较计算结果与预期值13f7: jne 1440 # 不相等跳转到失败处理
```



```
13f9: add r15,0x1 # r15++ (索引递增)1416: cmp r15,0x18 # 检查是否验证了24个字符141a: jne 11c0 # 未完成继续循环1420: lea rdi,[rip+0x4249] # "Correct flag, congratulations!"1427: call 1050 <puts@plt> # 打印成功消息142c: xor eax,eax # eax = 0 (返回码)142e: [函数清理和返回]
```



```
1440: lea rdi,[rip+0x4214] # "Nope, try again."1447: call 1050 <puts@plt> # 打印失败消息144c: mov eax,0x1 # eax = 1 (返回码)1451: jmp 142e # 跳转到函数返回
```



```
144c: mov eax,0x1 # 原始：返回固定值1
```



```
144c: mov eax,r15d # 修改：返回r15的值（验证通过的字符数）
```



```
#!/usr/bin/env python3"""Patch hyperjump binary to return the number of correctly verified charactersinstead of just returning 1 on failure."""importsysdefpatch_binary(input_file, output_file): """Patch the hyperjump binary to return verification position on failure.""" # Read the original binary withopen(input_file,'rb')asf: data = bytearray(f.read()) # Search for the pattern: b8 01 00 00 00 eb db (mov eax,0x1; jmp ...) pattern =b'xb8x01x00x00x00xebxdb' offset = data.find(pattern) ifoffset ==-1: print("Error: Could not find the pattern to patch!") returnFalse print(f"Found pattern at file offset: 0x{offset:x}") # Patch: Replace 'mov eax, 0x1' with 'mov eax, r15d; nop; nop' # b8 01 00 00 00 -> 44 89 f8 90 90 data[offset:offset+5] =b'x44x89xf8x90x90' # Write the patched binary withopen(output_file,'wb')asf: f.write(data) print(f"Successfully patched! Output:{output_file}") print("The binary will now return the number of correctly verified characters.") returnTrueif__name__ =='__main__': input_file ='hyperjump' output_file ='hyperjump_patched' ifpatch_binary(input_file, output_file): importos importstat # Make the patched file executable os.chmod(output_file, os.stat(output_file).st_mode | stat.S_IEXEC) print(f"nPatched binary is ready:{output_file}") else: sys.exit(1)
```



```
$ python3 patch_hyperjump.pyFound pattern at file offset: 0x144cSuccessfully patched! Output: hyperjump_patchedThe binary will nowreturnthe number of correctly verified characters.Patched binary is ready: hyperjump_patched
```



```
importsubprocesstest_cases = [ "aaaaaaaaaaaaaaaaaaaaaaaa", # 24个a "faaaaaaaaaaaaaaaaaaaaaaa", # f + 23个a "flaaaaaaaaaaaaaaaaaaaaaa", # fl + 22个a "flagaaaaaaaaaaaaaaaaaaaa", # flag + 20个a "flag{aaaaaaaaaaaaaaaaaaa", # flag{ + 19个a]fortest_inputintest_cases: p = subprocess.Popen('./hyperjump_patched', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) stdout, stderr = p.communicate(input=test_input) print(f"Input:{test_input[:10]:10s}... | Len:{len(test_input):2d}| RC:{p.returncode:3d}")
```



```
Input: aaaaaaaaaa... | Len: 24 | RC: 0Input: faaaaaaaaa... | Len: 24 | RC: 1Input: flaaaaaaaa... | Len: 24 | RC: 3Input: flagaaaaaa... | Len: 24 | RC: 4Input: flag{aaaaa... | Len: 24 | RC: 5
```



```
算法：逐位贪心爆破输入：patched程序路径，初始猜测（如"flag{111111111111111111}"）输出：正确的flag1. 初始化 current_flag = "flag{111111111111111111}"2. 初始化 best_rc = 03. 对于每个位置 i (0 到 23): 4. 对于每个可能的字符 c (0-9, a-z, A-Z, 特殊符号): 5. 构造测试字符串：test = current_flag[:i] + c + current_flag[i+1:] 6. 运行 patched程序，输入test，获取返回码 rc 7. 如果 rc > best_rc: 8. current_flag[i] = c 9. best_rc = rc 10. 如果输出包含 "Congratulations"： 11. 返回 test （找到完整flag）12. 返回 current_flag
```



```
#!/usr/bin/env python3"""Brute force script to find the correct flag for hyperjump challenge."""importstringimportsubprocess# All printable ASCII charactersalp = string.printable.strip()# Start with a known format (based on CTF flag format)input_data ="flag{111111111111111111}"exe_file_path ="./hyperjump_patched"print("Starting brute force...")print(f"Initial input:{input_data}")print(f"Target length:{len(input_data)}")print("="*60)# Track the best return code seen so farbest_returncode =0# Brute force each positionforiinrange(len(input_data)): print(f"n[*] Trying position{i}...") best_char = input_data[i] position_best_rc =0 # Try all possible characters for this position forcharinalp: # Create modified input with this character at position i modified_data = input_data[:i] + char + input_data[i+1:] # Run the binary process = subprocess.Popen( exe_file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True ) stdout, stderr = process.communicate(input=modified_data) # Check if we found a better character ifprocess.returncode > position_best_rc: position_best_rc = process.returncode best_char = char print(f" [+] Better char found: '{char}' (return code:{process.returncode})") # Check for success if"Congratulations"instdoutor"Correct"instdout: print(f"n{'='*60}") print(f"[SUCCESS] Flag found:{modified_data}") print(f"{'='*60}") exit(0) # Update the input with the best character found for this position ifbest_char != input_data[i]: input_data = input_data[:i] + best_char + input_data[i+1:] print(f" [*] Updated position{i}to '{best_char}'") print(f" [*] Current input:{input_data}")print(f"n{'='*60}")print(f"[*] Final input:{input_data}")print(f"{'='*60}")# Verify the final resultprocess = subprocess.Popen( exe_file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)stdout, stderr = process.communicate(input=input_data)print(f"Final output:n{stdout}")
```



```
$ python3 solve.pyStarting brute force...Initial input: flag{111111111111111111}Target length: 24============================================================[*] Trying position 0... [+] Better char found:'f'(returncode: 5)[*] Trying position 1... [+] Better char found:'0'(returncode: 1) [+] Better char found:'l'(returncode: 5)[*] Trying position 2... [+] Better char found:'0'(returncode: 2) [+] Better char found:'a'(returncode: 5)[*] Trying position 3... [+] Better char found:'0'(returncode: 3) [+] Better char found:'g'(returncode: 5)[*] Trying position 4... [+] Better char found:'0'(returncode: 4) [+] Better char found:'{'(returncode: 5)[*] Trying position 5... [+] Better char found:'0'(returncode: 5) [+] Better char found:'m'(returncode: 6) [*] Updated position 5 to'm' [*] Current input: flag{m11111111111111111}[*] Trying position 6... [+] Better char found:'0'(returncode: 6) [+] Better char found:'4'(returncode: 7) [*] Updated position 6 to'4' [*] Current input: flag{m41111111111111111}... (中间省略) ...[*] Trying position 22... [+] Better char found:'0'(returncode: 22)============================================================[SUCCESS] Flag found: flag{m4z3d_vm_jump5__42}============================================================
```



```
$echo"flag{m4z3d_vm_jump5__42}"| ./hyperjumpProvide the flag:Correct flag, congratulations!
```



```
// 不安全：提前退出泄露信息for(inti =0; i < len; i++) { if(input[i] != expected[i]) return0; // 泄露了i的值}// 安全：固定时间比较intresult =0;for(inti =0; i < len; i++) { result |= (input[i] ^ expected[i]);}return(result ==0); // 总是执行完所有比较
```



```
1. 文件分析 ├─ file命令：确认ELF 64位、PIE、stripped └─ strings命令：找到关键字符串2. 静态分析 ├─ 定位main函数：通过entry0和__libc_start_main ├─ 分析输入处理：fgets读取、strlen检查 ├─ 发现长度约束：必须24字符 └─ 理解验证循环：r15作为索引，逐字符处理3. 漏洞识别 ├─ 发现侧信道：r15保存验证进度 ├─ 提前退出问题：失败时r15未清零 └─ 可利用性评估：可通过patch暴露r154. Binary Patching ├─ 定位patch点：0x144c处的mov eax,0x1 ├─ 编写patch脚本：替换为mov eax,r15d └─ 验证patch效果：观察返回码变化5. 自动化爆破 ├─ 设计算法：贪心逐位搜索 ├─ 实现脚本：Python+subprocess └─ 执行攻击：2000+次尝试找到flag6. 结果验证 └─ 使用原始程序验证flag正确性
```
