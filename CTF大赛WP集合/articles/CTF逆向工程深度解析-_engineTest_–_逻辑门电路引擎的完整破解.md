# CTF逆向工程深度解析: engineTest – 逻辑门电路引擎的完整破解

> 原文: https://www.ctfiot.com/284044.html
> ID: 284044

CTF逆向工程深度解析: engineTest – 逻辑门电路引擎的完整破解

前言

本文将详细解析一道经典的CTF逆向工程题目engineTest。这道题目的设计非常精妙,它将传统的flag验证问题转化为一个基于逻辑门电路的计算引擎。通过本文的学习,读者将掌握以下技能:

ELF二进制文件的静态分析方法

数据结构的逆向重建技术

位运算和坐标编码机制的理解

布尔可满足性问题(SAT)的建模与求解

Z3约束求解器的实际应用

文件名

大小

描述

engineTest

22,928字节

64位ELF可执行文件(主程序)

cp

1,383,336字节

电路配置数据文件

ip

2,184字节

输入坐标映射文件

op

520字节

输出坐标映射文件

go.sh

–

执行脚本

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line$ cat go.sh#!/bin/shecho "input the flag:"exec ./engineTest ./cp ./ip /dev/stdin ./op$ echo "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" | ./engineTest ./cp ./ip /dev/stdin ./opWrong!

ounter(lineounter(lineounter(lineounter(line$ file engineTestengineTest: ELF 64-bit LSB executable, x86-64, version 1 (SYSV),dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,for GNU/Linux 2.6.32, stripped

64位ELF可执行文件

小端序(LSB)

动态链接

已stripped(符号表被移除,增加逆向难度)

ounter(line$ r2 -q -c 'aaa; s main; pdf' ./engineTest

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineif (argc != 5){ fwrite("[ERROR]n", 1, 8, stderr); fflush(stderr); _exit(1);}

argv[0]: 程序名

argv[1]: cp文件路径

argv[2]: ip文件路径

argv[3]: 输入文件路径(/dev/stdin)

argv[4]: op文件路径

ounter(lineounter(lineounter(lineounter(lineif (!strcmp(argv[1], "none")) f_cp = 0;else f_cp = open(argv[1], 0);

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linestruct description{ __int64 m_size; // 偏移+0x00: 位数组大小 __int64 records_count; // 偏移+0x08: 记录数量 record *records; // 偏移+0x10: 记录数组指针 __int64 *m; // 偏移+0x18: 位存储数组 __int64 *generated; // 偏移+0x20: 生成的索引数组 __int64 record_pos; // 偏移+0x28: 当前记录位置};

ounter(lineounter(lineounter(lineounter(lineounter(line; 地址0x402ac6处的关键初始化mov qword [rax + 0x18], rdx ; descr->m = allocated_memorymov rax, qword [var_18h]mov rax, qword [rax + 0x18]mov qword [rax], 2 ; *descr->m = 2

位0 = 0

位1 = 1

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linestruct record{ __int64 type; // 偏移+0x00: 操作类型 __int64 q1; // 偏移+0x08: 第一个操作数坐标 __int64 q2; // 偏移+0x10: 第二个操作数坐标 __int64 q3; // 偏移+0x18: 第三个操作数坐标(仅type=4时使用) __int64 q4; // 偏移+0x20: 结果存储坐标};

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineimport structwith open('cp', 'rb') as f: data = f.read()m_size = struct.unpack('<Q', data[0:8])[0]records_count = struct.unpack('<Q', data[8:16])[0]print(f"m_size: {m_size} (0x{m_size:x})")print(f"records_count: {records_count} (0x{records_count:x})")print(f"预期文件大小: {16 + records_count * 40}")print(f"实际文件大小: {len(data)}")

ounter(lineounter(lineounter(lineounter(linem_size: 34857 (0x8829)records_count: 34583 (0x8717)预期文件大小: 1383336实际文件大小: 1383336

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linetype_count = {1: 0, 2: 0, 3: 0, 4: 0}
for i in range(records_count): offset = 16 + i * 40 rec = struct.unpack('<QQQQQ', data[offset:
offset+40]) op_type = rec[0] if op_type in type_count: type_count[op_type] += 1print(f"Type 1 (AND门): {type_count[1]}")print(f"Type 2 (OR门): {type_count[2]}")print(f"Type 3 (XOR门): {type_count[3]}")print(f"Type 4 (MUX门): {type_count[4]}")

ounter(lineounter(lineounter(lineounter(lineounter(lineType 1 (AND门): 12887Type 2 (OR门): 8352Type 3 (XOR门): 9184Type 4 (MUX门): 4160总计: 34583

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linevoid set_bit(description *descr, unsigned __int64 coord, __int64 bit){ unsigned __int64 v3 = descr->m[coord >> 6]; signed __int64 v4; if (bit) v4 = (1LL << (coord & 0x3F)) | v3; else v4 = ~(1LL << (coord & 0x3F)) & v3; descr->m[coord >> 6] = v4;}

ounter(lineounter(lineounter(lineounter(lineunsigned __int64 get_bit(description *descr, unsigned __int64 coord){ return (descr->m[coord >> 6] >> (coord & 0x3F)) & 1;}

高58位(coord >> 6): m数组的索引

低6位(coord & 0x3F): 该64位整数中的位位置(0-63)

数组索引: 130 >> 6 = 2

位位置: 130 & 0x3F = 2

即m[2]的第2位

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linewith open('ip', 'rb') as f: data = f.read()ip_count = struct.unpack('<Q', data[0:8])[0]coords = []for i in range(ip_count): coord = struct.unpack('<Q', data[8 + i*8:16 + i*8])[0] coords.append(coord)print(f"坐标数量: {ip_count}")print(f"输入字节数: {ip_count // 8}")print(f"坐标范围: {min(coords)} ~ {max(coords)}")print(f"前8个坐标: {coords[:8]}")

ounter(lineounter(lineounter(lineounter(line坐标数量: 272 (0x110)输入字节数: 34坐标范围: 2 ~ 273前8个坐标: [2, 3, 4, 5, 6, 7, 8, 9]

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linefor (j = 0; j < ip_count; ++j){ if (!(j & 7)) // 每8位读取一个新字节 read_file(f_stdin, &c, 1); set_bit(&cp_descr, ip_coord[j], c & 1); // 取最低位写入 c = c >> 1; // 右移准备下一位}

272个坐标意味着需要272位输入,即34字节

坐标从2开始到273,跳过了位0和位1(预设的常量值)

输入数据按位展开后依次写入这些坐标

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineif (get_bit(descr, 0) || !get_bit(descr, 1)){ fwrite("[ERROR]n", 1, 8, stderr); fflush(stderr); _exit(1);}

ounter(lineres_bit = (get_bit(descr, q1) & get_bit(descr, q2)) != 0;

ounter(lineres_bit = (get_bit(descr, q1) | get_bit(descr, q2)) != 0;

ounter(lineres_bit = get_bit(descr, q1) != get_bit(descr, q2);

ounter(lineounter(lineounter(lineounter(lineif (get_bit(descr, q1) != 0) res_bit = get_bit(descr, q2) != 0;else res_bit = get_bit(descr, q3) != 0;

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linewith open('op', 'rb') as f: data = f.read()op_count = struct.unpack('<Q', data[0:8])[0]coords = [struct.unpack('<Q', data[8+i*8:16+i*8])[0] for i in range(op_count)]print(f"输出坐标数量: {op_count}")print(f"输出字节数: {op_count // 8}")print(f"坐标范围: {min(coords)} ~ {max(coords)}")

ounter(lineounter(lineounter(line输出坐标数量: 64 (0x40)输出字节数: 8坐标范围: 34793 (0x87e9) ~ 34856 (0x8828)

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
# 查找每个输出坐标对应的MUX门记录for out_coord in op_coords: for rec in records: t, q1, q2, q3, q4 = rec if q4 == out_coord: print(f"输出位{out_coord}: type={t}, q1={q1}, q2={q2}, q3={q3}") break

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line输出位34793: type=4, q1=34792, q2=1, q3=0输出位34794: type=4, q1=34792, q2=1, q3=0输出位34795: type=4, q1=34792, q2=0, q3=0输出位34796: type=4, q1=34792, q2=0, q3=0输出位34797: type=4, q1=34792, q2=0, q3=0输出位34798: type=4, q1=34792, q2=0, q3=1输出位34799: type=4, q1=34792, q2=1, q3=0输出位34800: type=4, q1=34792, q2=0, q3=0...

所有64个MUX门的q1都指向位34792– 这是验证位

q2的值直接编码了”Correct!”的各个位

q3的值直接编码了” Wrong! “的各个位

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
def bits_to_string(bits, length=8): s = '' for byte_idx in range(length): char_val = 0 for bit_idx in range(8): bit_pos = byte_idx * 8 + bit_idx if bit_pos < len(bits): char_val |= (bits[bit_pos] << bit_idx) s += chr(char_val) return sq2_string = bits_to_string(q2_bits) # 结果: "Correct!"q3_string = bits_to_string(q3_bits) # 结果: " Wrong! "

当验证位34792为1时,每个MUX门选择q2值,组装成”Correct!”

当验证位34792为0时,每个MUX门选择q3值,组装成” Wrong! “

程序维护一个34857位的位数组m

位0固定为0,位1固定为1

位2-273存储用户输入的34字节flag(272位)

通过34583条逻辑门记录,计算出剩余位的值

位34792是关键验证位,必须为1才表示flag正确

位34793-34856存储输出结果(64位,8字节)

为每个位创建一个布尔变量

添加初始位约束

添加验证位约束

添加所有逻辑门约束

让Z3自动搜索满足所有约束的解

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3
# -*- coding: utf-8 -*-from z3 import BitVec, Solver, Or, And, satimport struct
def get_records(filename='cp'): """从cp文件解析所有记录""" with open(filename, 'rb') as f: cp = f.read() m_size, count = struct.unpack('<QQ', cp[0:16]) print(f"[+] 正在解析CP文件...") print(f" 位数组大小: {m_size}") print(f" 记录数量: {count}") res = [] for i in range(count): record = struct.unpack('<QQQQQ', cp[i * 40 + 16:i * 40 + 56]) res.append(record) return m_size, res
def solve(m_size, records): """使用Z3求解器求解""" print(f"n[+] 开始构建Z3约束...") # 创建位向量数组 B = [BitVec(str(i), 1) for i in range(m_size)] s = Solver() # 约束1: 每个变量只能是0或1 print(f" 添加位值约束 (0或1)...") for b in B: s.add(Or(b == 0, b == 1)) # 约束2: 初始位的固定值 (来自*descr->m = 2) print(f" 添加初始位约束 (bit0=0, bit1=1)...") s.add(B[0] == 0) s.add(B[1] == 1) # 约束3: 关键验证位必须为1 print(f" 添加验证位约束 (bit34792=1)...") s.add(B[34792] == 1) # 约束4: 输入字符的最高位为0 (ASCII可打印字符) print(f" 添加ASCII字符约束 (34个字符的最高位为0)...") for i in range(34): s.add(B[2 + i * 8 + 7] == 0) # 约束5: 添加所有逻辑门约束 print(f" 添加逻辑门约束 ({len(records)} 条记录)...") for i, (op_type, q1, q2, q3, q4) in enumerate(records): if op_type == 1: # AND门: q4 = q1 & q2 s.add(B[q1] & B[q2] == B[q4]) elif op_type == 2: # OR门: q4 = q1 | q2 s.add(B[q1] | B[q2] == B[q4]) elif op_type == 3: # XOR门: q4 = q1 ^ q2 s.add(B[q1] ^ B[q2] == B[q4]) elif op_type == 4: # MUX门: q4 = q1 ? q2 : q3 s.add(Or(And(B[q1] == 1, B[q2] == B[q4]), And(B[q1] == 0, B[q3] == B[q4]))) if (i + 1) % 10000 == 0: print(f" 处理进度: {i+1}/{len(records)}") # 开始求解 print(f"n[+] 开始求解 (这可能需要一些时间)...") if s.check() == sat: print(f"[+] 求解成功!") model = s.model() return [model[B[i]].as_long() for i in range(m_size)] else: print(f"[-] 求解失败: 无解") return None
def extract_string(bits, offset, length): """从位数组提取字符串""" s = '' for byte_idx in range(length): char_val = 0 for bit_idx in range(8): bit_pos = offset + byte_idx * 8 + bit_idx char_val |= (bits[bit_pos] << bit_idx) s += chr(char_val) return s
def main(): print("=" * 60) print("engineTest Z3求解器") print("=" * 60) # 解析记录 m_size, records = get_records() # 求解 bits = solve(m_size, records) if bits: # 提取flag (从位2开始的34字节) flag = extract_string(bits, 2, 34) print(f"n{'=' * 60}") print(f"FLAG: {flag}") print(f"{'=' * 60}") # 提取验证成功后的输出 (从位34793开始的8字节) output = extract_string(bits, 34793, 8) print(f"预期输出: {output}")if __name__ == '__main__': main()

位值约束: 每个位只能是0或1,这是布尔变量的基本约束

初始位约束:B[0] == 0和B[1] == 1对应程序中*descr->m = 2的初始化

验证位约束:B[34792] == 1强制要求验证通过

ASCII约束: 每个输入字符的最高位为0,因为flag是可打印ASCII字符(0x00-0x7F)

逻辑门约束: 将34583条记录转换为Z3约束,确保逻辑电路的正确性

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line============================================================engineTest Z3求解器============================================================[+] 正在解析CP文件... 位数组大小: 34857 记录数量: 34583[+] 开始构建Z3约束... 添加位值约束 (0或1)... 添加初始位约束 (bit0=0, bit1=1)... 添加验证位约束 (bit34792=1)... 添加ASCII字符约束 (34个字符的最高位为0)... 添加逻辑门约束 (34583 条记录)... 处理进度: 10000/34583 处理进度: 20000/34583 处理进度: 30000/34583[+] 开始求解 (这可能需要一些时间)...[+] 求解成功!============================================================FLAG: flag{wind*w(s)_*f_B1ll(ion)_g@t5s}============================================================预期输出: Correct!

ounter(lineounter(line$ echo -n "flag{wind*w(s)_*f_B1ll(ion)_g@t5s}" | ./engineTest ./cp ./ip /dev/stdin ./opCorrect!

使用64位整数数组存储大量位数据

坐标编码:
index = coord >> 6,bit_pos = coord & 0x3F

位操作:
value = (array[index] >> bit_pos) & 1

基本逻辑门: AND、OR、XOR、MUX

通过记录数组定义电路拓扑

按依赖顺序执行计算

cp文件: 电路定义(门类型和连接关系)

ip文件: 输入映射(用户数据写入位置)

op文件: 输出映射(结果读取位置)

将验证问题转化为布尔约束求解

利用Z3求解器自动搜索解空间

添加合理约束缩小搜索范围(如ASCII字符约束)

理解程序的整体架构和数据流

逆向各个数据文件的格式

重建核心数据结构

理解位运算和坐标编码机制

识别问题本质(SAT问题)

应用合适的工具(Z3求解器)

可以将验证逻辑编译成复杂的门电路网络

增加逆向分析的难度

隐藏真正的验证算法

熟练掌握IDA Pro、Ghidra、radare2等逆向工具的使用

深入理解计算机底层的位运算和内存布局

学习数据结构重建技巧

了解常见的代码保护和混淆技术

掌握符号执行和约束求解工具(如Z3、angr)

培养将复杂问题抽象为数学模型的能力

ounter(lineflag{wind*w(s)_*f_B1ll(ion)_g@t5s}

ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""engineTest 完整分析脚本从二进制逆向到约束求解的完整实现"""import structimport os
def analyze_binary(): """分析二进制文件基本信息""" print("=" * 70) print("STEP 1: 二进制文件基本分析") print("=" * 70) with open('engineTest', 'rb') as f: header = f.read(64) if header[:4] == b'x7fELF': print("[+] 文件类型: ELF可执行文件") ei_class = header[4] print(f" 架构: {'64-bit' if ei_class == 2 else '32-bit'}") ei_data = header[5] print(f" 字节序: {'Little Endian' if ei_data == 1 else 'Big Endian'}") file_size = os.path.getsize('engineTest') print(f" 文件大小: {file_size} bytes")def analyze_cp_file(): """分析cp文件结构""" print("n" + "=" * 70) print("STEP 2: CP文件结构分析") print("=" * 70) with open('cp', 'rb') as f: data = f.read() m_size = struct.unpack('<Q', data[0:8])[0] records_count = struct.unpack('<Q', data[8:16])[0] print(f"[+] m_size (位数组大小): {m_size}") print(f"[+] records_count (记录数): {records_count}") # 解析记录 records = [] type_count = {1: 0, 2: 0, 3: 0, 4: 0} for i in range(records_count): offset = 16 + i * 40 rec = struct.unpack('<QQQQQ', data[offset:
offset+40]) records.append(rec) if rec[0] in type_count: type_count[rec[0]] += 1 print(f"n[+] 记录类型统计:") print(f" Type 1 (AND门): {type_count[1]}") print(f" Type 2 (OR门): {type_count[2]}") print(f" Type 3 (XOR门): {type_count[3]}") print(f" Type 4 (MUX门): {type_count[4]}") return m_size, records_count, records
def analyze_ip_file(): """分析ip文件结构""" print("n" + "=" * 70) print("STEP 3: IP文件结构分析") print("=" * 70) with open('ip', 'rb') as f: data = f.read() ip_count = struct.unpack('<Q', data[0:8])[0] coords = [struct.unpack('<Q', data[8 + i*8:16 + i*8])[0] for i in range(ip_count)] print(f"[+] 坐标数量: {ip_count}") print(f"[+] 输入字节数: {ip_count // 8}") print(f"[+] 坐标范围: {min(coords)} ~ {max(coords)}") return ip_count, coords
def analyze_op_file(): """分析op文件结构""" print("n" + "=" * 70) print("STEP 4: OP文件结构分析") print("=" * 70) with open('op', 'rb') as f: data = f.read() op_count = struct.unpack('<Q', data[0:8])[0] coords = [struct.unpack('<Q', data[8 + i*8:16 + i*8])[0] for i in range(op_count)] print(f"[+] 坐标数量: {op_count}") print(f"[+] 输出字节数: {op_count // 8}") print(f"[+] 坐标范围: {min(coords)} ~ {max(coords)}") return op_count, coords
def find_verification_bit(records, op_coords): """查找验证位""" print("n" + "=" * 70) print("STEP 5: 验证位分析") print("=" * 70) verification_bit = None q2_bits = [] q3_bits = [] for out_coord in op_coords: for rec in records: t, q1, q2, q3, q4 = rec if q4 == out_coord: if verification_bit is None: verification_bit = q1 q2_bits.append(q2) q3_bits.append(q3) break # 组装字符串 def bits_to_string(bits, length=8): s = '' for byte_idx in range(length): char_val = 0 for bit_idx in range(8): bit_pos = byte_idx * 8 + bit_idx if bit_pos < len(bits): char_val |= (bits[bit_pos] << bit_idx) s += chr(char_val) return s q2_string = bits_to_string(q2_bits) q3_string = bits_to_string(q3_bits) print(f"[+] 验证位位置: {verification_bit}") print(f"[+] 当验证位=1时输出: '{q2_string}'") print(f"[+] 当验证位=0时输出: '{q3_string}'") return verification_bit
def z3_solve(m_size, records, verification_bit): """使用Z3求解""" print("n" + "=" * 70) print("STEP 6: Z3约束求解") print("=" * 70) from z3 import BitVec, Solver, Or, And, sat print(f"[+] 创建 {m_size} 个位变量...") B = [BitVec(str(i), 1) for i in range(m_size)] s = Solver() print("[+] 添加约束...") for b in B: s.add(Or(b == 0, b == 1)) s.add(B[0] == 0) s.add(B[1] == 1) s.add(B[verification_bit] == 1) for i in range(34): s.add(B[2 + i * 8 + 7] == 0) for op_type, q1, q2, q3, q4 in records: if op_type == 1: s.add(B[q1] & B[q2] == B[q4]) elif op_type == 2: s.add(B[q1] | B[q2] == B[q4]) elif op_type == 3: s.add(B[q1] ^ B[q2] == B[q4]) elif op_type == 4: s.add(Or(And(B[q1] == 1, B[q2] == B[q4]), And(B[q1] == 0, B[q3] == B[q4]))) print("[+] 开始求解...") if s.check() == sat: print("[+] 求解成功!") model = s.model() return [model[B[i]].as_long() for i in range(m_size)] else: print("[-] 无解") return None
def extract_flag(bits): """提取flag""" print("n" + "=" * 70) print("STEP 7: 提取Flag") print("=" * 70) flag = '' for byte_idx in range(34): char_val = 0 for bit_idx in range(8): bit_pos = 2 + byte_idx * 8 + bit_idx char_val |= (bits[bit_pos] << bit_idx) flag += chr(char_val) print(f"[+] FLAG: {flag}") return flag
def main(): print("=" * 70) print(" engineTest 完整分析") print("=" * 70) analyze_binary() m_size, records_count, records = analyze_cp_file() ip_count, ip_coords = analyze_ip_file() op_count, op_coords = analyze_op_file() verification_bit = find_verification_bit(records, op_coords) bits = z3_solve(m_size, records, verification_bit) if bits: flag = extract_flag(bits) return flag return Noneif __name__ == '__main__': main()


```
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line$ cat go.sh#!/bin/shecho "input the flag:"exec ./engineTest ./cp ./ip /dev/stdin ./op$ echo "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" | ./engineTest ./cp ./ip /dev/stdin ./opWrong!
ounter(lineounter(lineounter(lineounter(line$ file engineTestengineTest: ELF 64-bit LSB executable, x86-64, version 1 (SYSV),dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,for GNU/Linux 2.6.32, stripped
ounter(line$ r2 -q -c 'aaa; s main; pdf' ./engineTest
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineif (argc != 5){ fwrite("[ERROR]n", 1, 8, stderr); fflush(stderr); _exit(1);}
ounter(lineounter(lineounter(lineounter(lineif (!strcmp(argv[1], "none")) f_cp = 0;else f_cp = open(argv[1], 0);
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linestruct description{ __int64 m_size; // 偏移+0x00: 位数组大小 __int64 records_count; // 偏移+0x08: 记录数量 record *records; // 偏移+0x10: 记录数组指针 __int64 *m; // 偏移+0x18: 位存储数组 __int64 *generated; // 偏移+0x20: 生成的索引数组 __int64 record_pos; // 偏移+0x28: 当前记录位置};
ounter(lineounter(lineounter(lineounter(lineounter(line; 地址0x402ac6处的关键初始化mov qword [rax + 0x18], rdx ; descr->m = allocated_memorymov rax, qword [var_18h]mov rax, qword [rax + 0x18]mov qword [rax], 2 ; *descr->m = 2
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linestruct record{ __int64 type; // 偏移+0x00: 操作类型 __int64 q1; // 偏移+0x08: 第一个操作数坐标 __int64 q2; // 偏移+0x10: 第二个操作数坐标 __int64 q3; // 偏移+0x18: 第三个操作数坐标(仅type=4时使用) __int64 q4; // 偏移+0x20: 结果存储坐标};
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineimport structwith open('cp', 'rb') as f: data = f.read()m_size = struct.unpack('<Q', data[0:8])[0]records_count = struct.unpack('<Q', data[8:16])[0]print(f"m_size: {m_size} (0x{m_size:x})")print(f"records_count: {records_count} (0x{records_count:x})")print(f"预期文件大小: {16 + records_count * 40}")print(f"实际文件大小: {len(data)}")
ounter(lineounter(lineounter(lineounter(linem_size: 34857 (0x8829)records_count: 34583 (0x8717)预期文件大小: 1383336实际文件大小: 1383336
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linetype_count = {1: 0, 2: 0, 3: 0, 4: 0}
for i in range(records_count): offset = 16 + i * 40 rec = struct.unpack('<QQQQQ', data[offset:
offset+40]) op_type = rec[0] if op_type in type_count: type_count[op_type] += 1print(f"Type 1 (AND门): {type_count[1]}")print(f"Type 2 (OR门): {type_count[2]}")print(f"Type 3 (XOR门): {type_count[3]}")print(f"Type 4 (MUX门): {type_count[4]}")
ounter(lineounter(lineounter(lineounter(lineounter(lineType 1 (AND门): 12887Type 2 (OR门): 8352Type 3 (XOR门): 9184Type 4 (MUX门): 4160总计: 34583
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linevoid set_bit(description *descr, unsigned __int64 coord, __int64 bit){ unsigned __int64 v3 = descr->m[coord >> 6]; signed __int64 v4; if (bit) v4 = (1LL << (coord & 0x3F)) | v3; else v4 = ~(1LL << (coord & 0x3F)) & v3; descr->m[coord >> 6] = v4;}
ounter(lineounter(lineounter(lineounter(lineunsigned __int64 get_bit(description *descr, unsigned __int64 coord){ return (descr->m[coord >> 6] >> (coord & 0x3F)) & 1;}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linewith open('ip', 'rb') as f: data = f.read()ip_count = struct.unpack('<Q', data[0:8])[0]coords = []for i in range(ip_count): coord = struct.unpack('<Q', data[8 + i*8:16 + i*8])[0] coords.append(coord)print(f"坐标数量: {ip_count}")print(f"输入字节数: {ip_count // 8}")print(f"坐标范围: {min(coords)} ~ {max(coords)}")print(f"前8个坐标: {coords[:8]}")
ounter(lineounter(lineounter(lineounter(line坐标数量: 272 (0x110)输入字节数: 34坐标范围: 2 ~ 273前8个坐标: [2, 3, 4, 5, 6, 7, 8, 9]
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linefor (j = 0; j < ip_count; ++j){ if (!(j & 7)) // 每8位读取一个新字节 read_file(f_stdin, &c, 1); set_bit(&cp_descr, ip_coord[j], c & 1); // 取最低位写入 c = c >> 1; // 右移准备下一位}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineif (get_bit(descr, 0) || !get_bit(descr, 1)){ fwrite("[ERROR]n", 1, 8, stderr); fflush(stderr); _exit(1);}
ounter(lineres_bit = (get_bit(descr, q1) & get_bit(descr, q2)) != 0;
ounter(lineres_bit = (get_bit(descr, q1) | get_bit(descr, q2)) != 0;
ounter(lineres_bit = get_bit(descr, q1) != get_bit(descr, q2);
ounter(lineounter(lineounter(lineounter(lineif (get_bit(descr, q1) != 0) res_bit = get_bit(descr, q2) != 0;else res_bit = get_bit(descr, q3) != 0;
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(linewith open('op', 'rb') as f: data = f.read()op_count = struct.unpack('<Q', data[0:8])[0]coords = [struct.unpack('<Q', data[8+i*8:16+i*8])[0] for i in range(op_count)]print(f"输出坐标数量: {op_count}")print(f"输出字节数: {op_count // 8}")print(f"坐标范围: {min(coords)} ~ {max(coords)}")
ounter(lineounter(lineounter(line输出坐标数量: 64 (0x40)输出字节数: 8坐标范围: 34793 (0x87e9) ~ 34856 (0x8828)
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
# 查找每个输出坐标对应的MUX门记录for out_coord in op_coords: for rec in records: t, q1, q2, q3, q4 = rec if q4 == out_coord: print(f"输出位{out_coord}: type={t}, q1={q1}, q2={q2}, q3={q3}") break
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line输出位34793: type=4, q1=34792, q2=1, q3=0输出位34794: type=4, q1=34792, q2=1, q3=0输出位34795: type=4, q1=34792, q2=0, q3=0输出位34796: type=4, q1=34792, q2=0, q3=0输出位34797: type=4, q1=34792, q2=0, q3=0输出位34798: type=4, q1=34792, q2=0, q3=1输出位34799: type=4, q1=34792, q2=1, q3=0输出位34800: type=4, q1=34792, q2=0, q3=0...
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line
def bits_to_string(bits, length=8): s = '' for byte_idx in range(length): char_val = 0 for bit_idx in range(8): bit_pos = byte_idx * 8 + bit_idx if bit_pos < len(bits): char_val |= (bits[bit_pos] << bit_idx) s += chr(char_val) return sq2_string = bits_to_string(q2_bits) # 结果: "Correct!"q3_string = bits_to_string(q3_bits) # 结果: " Wrong! "
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3
# -*- coding: utf-8 -*-from z3 import BitVec, Solver, Or, And, satimport struct
def get_records(filename='cp'): """从cp文件解析所有记录""" with open(filename, 'rb') as f: cp = f.read() m_size, count = struct.unpack('<QQ', cp[0:16]) print(f"[+] 正在解析CP文件...") print(f" 位数组大小: {m_size}") print(f" 记录数量: {count}") res = [] for i in range(count): record = struct.unpack('<QQQQQ', cp[i * 40 + 16:i * 40 + 56]) res.append(record) return m_size, res
def solve(m_size, records): """使用Z3求解器求解""" print(f"n[+] 开始构建Z3约束...") # 创建位向量数组 B = [BitVec(str(i), 1) for i in range(m_size)] s = Solver() # 约束1: 每个变量只能是0或1 print(f" 添加位值约束 (0或1)...") for b in B: s.add(Or(b == 0, b == 1)) # 约束2: 初始位的固定值 (来自*descr->m = 2) print(f" 添加初始位约束 (bit0=0, bit1=1)...") s.add(B[0] == 0) s.add(B[1] == 1) # 约束3: 关键验证位必须为1 print(f" 添加验证位约束 (bit34792=1)...") s.add(B[34792] == 1) # 约束4: 输入字符的最高位为0 (ASCII可打印字符) print(f" 添加ASCII字符约束 (34个字符的最高位为0)...") for i in range(34): s.add(B[2 + i * 8 + 7] == 0) # 约束5: 添加所有逻辑门约束 print(f" 添加逻辑门约束 ({len(records)} 条记录)...") for i, (op_type, q1, q2, q3, q4) in enumerate(records): if op_type == 1: # AND门: q4 = q1 & q2 s.add(B[q1] & B[q2] == B[q4]) elif op_type == 2: # OR门: q4 = q1 | q2 s.add(B[q1] | B[q2] == B[q4]) elif op_type == 3: # XOR门: q4 = q1 ^ q2 s.add(B[q1] ^ B[q2] == B[q4]) elif op_type == 4: # MUX门: q4 = q1 ? q2 : q3 s.add(Or(And(B[q1] == 1, B[q2] == B[q4]), And(B[q1] == 0, B[q3] == B[q4]))) if (i + 1) % 10000 == 0: print(f" 处理进度: {i+1}/{len(records)}") # 开始求解 print(f"n[+] 开始求解 (这可能需要一些时间)...") if s.check() == sat: print(f"[+] 求解成功!") model = s.model() return [model[B[i]].as_long() for i in range(m_size)] else: print(f"[-] 求解失败: 无解") return None
def extract_string(bits, offset, length): """从位数组提取字符串""" s = '' for byte_idx in range(length): char_val = 0 for bit_idx in range(8): bit_pos = offset + byte_idx * 8 + bit_idx char_val |= (bits[bit_pos] << bit_idx) s += chr(char_val) return s
def main(): print("=" * 60) print("engineTest Z3求解器") print("=" * 60) # 解析记录 m_size, records = get_records() # 求解 bits = solve(m_size, records) if bits: # 提取flag (从位2开始的34字节) flag = extract_string(bits, 2, 34) print(f"n{'=' * 60}") print(f"FLAG: {flag}") print(f"{'=' * 60}") # 提取验证成功后的输出 (从位34793开始的8字节) output = extract_string(bits, 34793, 8) print(f"预期输出: {output}")if __name__ == '__main__': main()
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line============================================================engineTest Z3求解器============================================================[+] 正在解析CP文件... 位数组大小: 34857 记录数量: 34583[+] 开始构建Z3约束... 添加位值约束 (0或1)... 添加初始位约束 (bit0=0, bit1=1)... 添加验证位约束 (bit34792=1)... 添加ASCII字符约束 (34个字符的最高位为0)... 添加逻辑门约束 (34583 条记录)... 处理进度: 10000/34583 处理进度: 20000/34583 处理进度: 30000/34583[+] 开始求解 (这可能需要一些时间)...[+] 求解成功!============================================================FLAG: flag{wind*w(s)_*f_B1ll(ion)_g@t5s}============================================================预期输出: Correct!
ounter(lineounter(line$ echo -n "flag{wind*w(s)_*f_B1ll(ion)_g@t5s}" | ./engineTest ./cp ./ip /dev/stdin ./opCorrect!
ounter(lineflag{wind*w(s)_*f_B1ll(ion)_g@t5s}
ounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(lineounter(line#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""engineTest 完整分析脚本从二进制逆向到约束求解的完整实现"""import structimport os
def analyze_binary(): """分析二进制文件基本信息""" print("=" * 70) print("STEP 1: 二进制文件基本分析") print("=" * 70) with open('engineTest', 'rb') as f: header = f.read(64) if header[:4] == b'x7fELF': print("[+] 文件类型: ELF可执行文件") ei_class = header[4] print(f" 架构: {'64-bit' if ei_class == 2 else '32-bit'}") ei_data = header[5] print(f" 字节序: {'Little Endian' if ei_data == 1 else 'Big Endian'}") file_size = os.path.getsize('engineTest') print(f" 文件大小: {file_size} bytes")def analyze_cp_file(): """分析cp文件结构""" print("n" + "=" * 70) print("STEP 2: CP文件结构分析") print("=" * 70) with open('cp', 'rb') as f: data = f.read() m_size = struct.unpack('<Q', data[0:8])[0] records_count = struct.unpack('<Q', data[8:16])[0] print(f"[+] m_size (位数组大小): {m_size}") print(f"[+] records_count (记录数): {records_count}") # 解析记录 records = [] type_count = {1: 0, 2: 0, 3: 0, 4: 0} for i in range(records_count): offset = 16 + i * 40 rec = struct.unpack('<QQQQQ', data[offset:
offset+40]) records.append(rec) if rec[0] in type_count: type_count[rec[0]] += 1 print(f"n[+] 记录类型统计:") print(f" Type 1 (AND门): {type_count[1]}") print(f" Type 2 (OR门): {type_count[2]}") print(f" Type 3 (XOR门): {type_count[3]}") print(f" Type 4 (MUX门): {type_count[4]}") return m_size, records_count, records
def analyze_ip_file(): """分析ip文件结构""" print("n" + "=" * 70) print("STEP 3: IP文件结构分析") print("=" * 70) with open('ip', 'rb') as f: data = f.read() ip_count = struct.unpack('<Q', data[0:8])[0] coords = [struct.unpack('<Q', data[8 + i*8:16 + i*8])[0] for i in range(ip_count)] print(f"[+] 坐标数量: {ip_count}") print(f"[+] 输入字节数: {ip_count // 8}") print(f"[+] 坐标范围: {min(coords)} ~ {max(coords)}") return ip_count, coords
def analyze_op_file(): """分析op文件结构""" print("n" + "=" * 70) print("STEP 4: OP文件结构分析") print("=" * 70) with open('op', 'rb') as f: data = f.read() op_count = struct.unpack('<Q', data[0:8])[0] coords = [struct.unpack('<Q', data[8 + i*8:16 + i*8])[0] for i in range(op_count)] print(f"[+] 坐标数量: {op_count}") print(f"[+] 输出字节数: {op_count // 8}") print(f"[+] 坐标范围: {min(coords)} ~ {max(coords)}") return op_count, coords
def find_verification_bit(records, op_coords): """查找验证位""" print("n" + "=" * 70) print("STEP 5: 验证位分析") print("=" * 70) verification_bit = None q2_bits = [] q3_bits = [] for out_coord in op_coords: for rec in records: t, q1, q2, q3, q4 = rec if q4 == out_coord: if verification_bit is None: verification_bit = q1 q2_bits.append(q2) q3_bits.append(q3) break # 组装字符串 def bits_to_string(bits, length=8): s = '' for byte_idx in range(length): char_val = 0 for bit_idx in range(8): bit_pos = byte_idx * 8 + bit_idx if bit_pos < len(bits): char_val |= (bits[bit_pos] << bit_idx) s += chr(char_val) return s q2_string = bits_to_string(q2_bits) q3_string = bits_to_string(q3_bits) print(f"[+] 验证位位置: {verification_bit}") print(f"[+] 当验证位=1时输出: '{q2_string}'") print(f"[+] 当验证位=0时输出: '{q3_string}'") return verification_bit
def z3_solve(m_size, records, verification_bit): """使用Z3求解""" print("n" + "=" * 70) print("STEP 6: Z3约束求解") print("=" * 70) from z3 import BitVec, Solver, Or, And, sat print(f"[+] 创建 {m_size} 个位变量...") B = [BitVec(str(i), 1) for i in range(m_size)] s = Solver() print("[+] 添加约束...") for b in B: s.add(Or(b == 0, b == 1)) s.add(B[0] == 0) s.add(B[1] == 1) s.add(B[verification_bit] == 1) for i in range(34): s.add(B[2 + i * 8 + 7] == 0) for op_type, q1, q2, q3, q4 in records: if op_type == 1: s.add(B[q1] & B[q2] == B[q4]) elif op_type == 2: s.add(B[q1] | B[q2] == B[q4]) elif op_type == 3: s.add(B[q1] ^ B[q2] == B[q4]) elif op_type == 4: s.add(Or(And(B[q1] == 1, B[q2] == B[q4]), And(B[q1] == 0, B[q3] == B[q4]))) print("[+] 开始求解...") if s.check() == sat: print("[+] 求解成功!") model = s.model() return [model[B[i]].as_long() for i in range(m_size)] else: print("[-] 无解") return None
def extract_flag(bits): """提取flag""" print("n" + "=" * 70) print("STEP 7: 提取Flag") print("=" * 70) flag = '' for byte_idx in range(34): char_val = 0 for bit_idx in range(8): bit_pos = 2 + byte_idx * 8 + bit_idx char_val |= (bits[bit_pos] << bit_idx) flag += chr(char_val) print(f"[+] FLAG: {flag}") return flag
def main(): print("=" * 70) print(" engineTest 完整分析") print("=" * 70) analyze_binary() m_size, records_count, records = analyze_cp_file() ip_count, ip_coords = analyze_ip_file() op_count, op_coords = analyze_op_file() verification_bit = find_verification_bit(records, op_coords) bits = z3_solve(m_size, records, verification_bit) if bits: flag = extract_flag(bits) return flag return Noneif __name__ == '__main__': main()
```
