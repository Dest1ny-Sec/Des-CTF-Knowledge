# 第三届古剑山网络安全功防大赛初赛Reverse全解wp

> 原文: https://www.ctfiot.com/284751.html
> ID: 284751

前言：每个题刚放出来没多久就被秒，感觉大家逆向水平都真好，题也不算简单啊🤭easyre题目描述：可能需要动静结合。利用思路：非常简单的签到题。逻辑就是先base64再rc4加异或

关键在于v7的判断来决定这11组加密后的密文每个是否再和0x22222222异或。可以写脚本也可以动调直接得出总体异或的密钥流：00 00 00 00 22 22 22 22 22 22 22 22 22 22 22 22 22 22 22 22 00 00 00 00 00 00 00 00 00 00 00 00 22 22 22 22 22 22 22 22 00 00 00 00Cyberchef逆序解密：异或0x90504956(v12)->异或密钥流->rc4解密->base64解密。

Helloworld题目描述：想办法让程序输出HelloWorld吧。利用思路：IDA反编译得到：int __cdecl main(int argc, const char **argv, const char **envp){ const char *v3; // ebx unsigned int v4; // eax int i; // esi FILE *v6; // eax unsigned int v7; // edi unsigned int v8; // ecx unsigned int v9; // esi int v10; // eax char *v11; // edx unsigned int v12; // eax unsigned int v13; // ecx unsigned int v14; // eax unsigned int v15; // eax unsigned int v16; // eax unsigned int v17; // eax char v18; // al char v19; // dl char v20; // dl char v21; // dl int v22; // eax int v24; // [esp-4h] [ebp-A8h] unsigned int v25; // [esp+14h] [ebp-90h] unsigned int v26; // [esp+1Ch] [ebp-88h] char Buffer[100]; // [esp+20h] [ebp-84h] BYREF char v28[28]; // [esp+84h] [ebp-20h] BYREF v3 = (const char *)malloc(0x64u); v4 = time64(0); srand(v4); for ( i = 0; i < 100; ++i ) v3[i] = rand() % 255; strcpy(v28, “abcdefghijklmnopqrstuvwxyz”); v6 = _acrt_iob_func(0); fgets(Buffer, 100, v6); v7 = 0; v26 = 0; v8 = strlen(Buffer); if ( v8 ) { v9 = v25; v10 = 1 – (_DWORD)Buffer; do { v11 = &Buffer[v7]; if ( (unsigned int)&Buffer[v7 + v10] < v8 ) { v12 = (unsigned __int8)*v11; v13 = v12 & 0xF; v14 = v12 >> 4; if ( v14 == 3 ) v9 = v11[1] & 0x1F; v15 = v14 – 1; if ( !v15 ) { if ( v13 >= strlen(v3) ) goto LABEL_24; v21 = v3[v13]; if ( (unsigned __int8)(v21 – ‘a’) > 0x19u ) goto LABEL_24; v20 = v21 – 32; goto LABEL_23; } v16 = v15 – 1; if ( v16 ) { v17 = v16 – 1; if ( v17 ) { if ( v17 == 1 && v13 < strlen(v3) ) v3[v13] = v18; } else if ( v13 < strlen(v3) && v9 < strlen(v28) ) { v3[v13] = v28[v9]; } goto LABEL_24; } if ( v13 < strlen(v3) ) { v19 = v3[v13]; if ( (unsigned __int8)(v19 – ‘A’) <= 0x19u ) { v20 = v19 + 32;LABEL_23: v3[v13] = v20; } } }LABEL_24: v26 += 2; v7 = v26; v8 = strlen(Buffer); v10 = 1 – (_DWORD)Buffer; } while ( v26 < v8 ); } v22 = sub_8011CE(sub_801348); std::
ostream::
operator<<(v22, v24); return 0;}首先，分析逻辑：输入 Buffer 被解析为操作码，每 2 个字节一个操作一个字节：d1 = Buffer[i]，高 4 位 op = (d1 >> 4) & 0xF，低 4 位 idx = d1 & 0xF只有 op == 3 时使用下一个字节：d2 = Buffer[i+1]，src_idx = d2 & 0x1Fv28 = “abcdefghijklmnopqrstuvwxyz”操作：op == 1：如果 v3[idx] 是小写字母，则 v3[idx] -= 32op == 2：如果 v3[idx] 是大写字母，则 v3[idx] += 32op == 3：v3[idx] = v28[src_idx]op == 4：无效操作，忽略索引 idx 范围 0-15，所以最多控制前 16 字节目标：v3[0:10] = “HelloWorld”H e l l o W o r l d索引：0 1 2 3 4 5 6 7 8 9H (72) = ‘H’e (101) = ‘e’l (108) = ‘l’l (108) = ‘l’o (111) = ‘o’W (87) = ‘W’o (111) = ‘o’r (114) = ‘r’l (108) = ‘l’d (100) = ‘d’v28 = “abcdefghijklmnopqrstuvwxyz”我们需要使用 op==3 来赋值，因为 v3 初始是随机值，只有 op==3 可以精确赋值为已知字符。对于每个字符，我们需要：构造 Buffer[i] = (op << 4) | idx，其中 idx 是目标索引，op=3构造 Buffer[i+1]&0x1F = src_idx，其中 src_idx 是字符在 v28 中的索引所以策略：先用 op==3 设置所有字符为小写然后用 op==1 将索引 0 和 5 的字符转为大写
def generate_helloworld_payload(): “””生成无0x00的HelloWorld字节码””” v28 = “abcdefghijklmnopqrstuvwxyz” target = “HelloWorld” char_to_idx = {c: i for i, c in enumerate(v28)} FILL_BYTE = 0xFF # 无害填充，对应op=0xF（未定义） payload = bytearray() for i, ch in enumerate(target.lower()): # 1. 写入小写字母 (op=3) payload.append((3 << 4) | i) payload.append(char_to_idx[ch]) # 2. 如果原字符是大写，立即转大写 (op=1) if target[i].isupper(): payload.append((1 << 4) | i) payload.append(FILL_BYTE) # 非零填充 return bytes(payload)
# 生成结果payload = generate_helloworld_payload()print(payload.hex())
# 输出: 300710ff3104320b330b340e351610ff360e3711380b3903远程用pwntools去打
from pwn import *context.log_level = “debug”p = remote(‘ ‘, )#ip,portpayload = bytes.fromhex(“300710ff3104320b330b340e351610ff360e3711380b3903”)p.sendline(payload)p.recv()veryez一道简单的vm题

Dword_408254处就是存的操作码vm code

void __cdecl __noreturn sub_401030(int a1, int a2){ unsigned int v2; // eax int v3; // ecx int v4; // eax int v5; // eax int v6; // eax int v7; // eax int v8; // eax int v9; // eax unsigned int v10; // eax unsigned int v11; // eax unsigned int v12; // esi int v13; // eax int v14; // eax unsigned int v15; // esi int v16; // esi int v17; // eax int v18; // esi int v19; // [esp+Ch] [ebp-4h] BYREF sub_401390(); dword_40AC60 = 0; while ( 1 ) { while ( 1 ) { while ( 1 ) {LABEL_2: while ( 1 ) { v2 = *(_DWORD *)(a1 + 4 * dword_40AC60); v3 = ++dword_40AC60; if ( v2 > 0x201 ) break; if ( v2 == 0x201 ) { v19 = sub_4013E0(); v7 = sub_4013E0(); sub_4013A0(v19 – v7); } else { switch ( v2 ) { case 0x101u: v19 = sub_4013E0(); v4 = sub_4013E0(); sub_4013A0(v19 + v4); break; case 0x102u: v19 = sub_4013E0(); v5 = sub_4013E0(); sub_4013A0(v19 & v5); break; case 0x103u: sub_401370(); case 0x104u: v6 = *(_DWORD *)(a1 + 4 * v3); dword_40AC60 = v3 + 1; sub_4013A0(v6); break; case 0x105u: printf(“Enter integer: “); scanf(“%d”, &v19); fflush(&Stream); sub_4013A0(v19); break; default: continue; } } } if ( v2 > 0x305 ) break; if ( v2 == 773 ) { v13 = sub_4013E0(); gets(a2 + v13); } else if ( v2 > 0x301 ) { v10 = v2 – 770; if ( v10 ) { v11 = v10 – 1; if ( v11 ) { if ( v11 == 1 ) { v19 = *(_DWORD *)(sub_4013E0() + a2); sub_4013A0(v19); } } else { v12 = *(_DWORD *)(a1 + 4 * v3); dword_40AC60 = v3 + 1; if ( !sub_4013E0() ) dword_40AC60 = v12 >> 2; } } else { v19 = sub_4013E0(); sub_4013A0(~v19); } } else if ( v2 == 769 ) { v19 = sub_4013E0() + 1; sub_4013A0(v19); } else { switch ( v2 ) { case 0x202u: v19 = sub_4013E0(); v8 = sub_4013E0(); sub_4013A0(v19 | v8); break; case 0x203u: dword_40AC60 = *(_DWORD *)(a1 + 4 * v3) >> 2; break; case 0x204u: sub_4013E0(); break; case 0x205u: v9 = sub_4013E0(); printf(“%dn”, v9); break; default: continue; } } } if ( v2 > 0x504 ) break; if ( v2 == 1284 ) { v19 = *(unsigned __int8 *)(sub_4013E0() + a2); sub_4013A0(v19); } else { switch ( v2 ) { case 0x401u: v19 = sub_4013E0() – 1; sub_4013A0(v19); break; case 0x402u: v19 = sub_4013E0(); v14 = sub_4013E0(); sub_4013A0(v19 ^ v14); break; case 0x403u: v15 = *(_DWORD *)(a1 + 4 * v3); dword_40AC60 = v3 + 1; if ( sub_4013E0() ) dword_40AC60 = v15 >> 2; break; case 0x404u: v16 = sub_4013E0(); *(_DWORD *)(v16 + a2) = sub_4013E0(); break; case 0x405u: v17 = sub_4013E0(); puts((const char *)(a2 + v17)); break; default: goto LABEL_2; } } } if ( v2 == 1540 ) { v18 = sub_4013E0(); *(_BYTE *)(v18 + a2) = sub_4013E0(); } }}上面就是主要的解析函数，可以看到操作码类型很少，经过调试或者简单手撕就可得到逻辑为异或，我这里通过调试大概理解出来就是input^key[i&7]，思路就不详细展开了。

Key是viryualM，后面是加密后的密文，直接cyberchef解密就行。

babyre题目描述：just re.利用思路：此题考察的就是逆向基本功底，过反调试跟踪程序加密逻辑。直接调试程序会发现程序会退出，那么应该是有反调试，在这里

是sys_ptrace反调试，我的做法是直接运行后patch掉qword_6D1D60的值就绕过了反调试不会退出。然后继续往下跟踪，找到函数对于输入的加密逻辑。

就是一个rc4，flag的后半段就是直接明文比较”is_good}”，然后把这个作为rc4加密的key对flag整体进行加密，和加密后的密文进行比对。那么cyberchef解密就得到了最终flag。

final题目描述：CVE-2010-2967，本题对加密算法进行了局部修改。需要对固件进行分析，成功找到存在漏洞的hash算法。已知字符串“SimpleXue”，请计算此字符串经过hash算法加密过的哈希值，并放在flag{}中提交。利用思路：很明显题目考察的是固件分析，给了一个pacth.bin文件，直接binwalk -e patch.bin提取出名为385的二进制文件，再对它进行binwalk文件分离分析，可以看到如下内容。

可以看出，固件是基于VxWorks 2.5的，加载基址一般为0x10000。（经过分析也可确定基地址确实为0x10000）查看固件中指令特征：用hexdump -C 385 | head -20观察指令码

指令多以0x7C开头，确定固件为PowerPC结构。结合题目，CVE-2010-2967，得知漏洞函数在于loginDefaultEncrypt()函数。根据上图最后一行得知文件也存在符号表信息，位于文件偏移0x301E74中，且告诉了我们格式VxWorks symbol table, big endian, first en
try: [type: function, code address: 0x1FF058, symbol address: 0x27655C]也就是说，大端序存储，前4字节是符号名偏移地址，5-8字节是代码偏移地址，9-12字节是类型，后4字节基本全为0应该就是保留字段。

手动分析得到我们需要的函数类型对应的应该就是0x500确定好以上信息之后，我们就可以把固件载入ida9.0当中，选择PowerPC架构，大端序，后面默认选项，进入ida反编译发现左侧是没有符号信息的。需要进行符号恢复。

写python脚本把对应的符号表信息提取计算得到对应偏移处函数的真实函数名。

import struct
# 固件路径FIRMWARE_FILE = “C:\Users\031225\Desktop\385″SYMTAB_OFFSET = 0x301E74 # 符号表起始偏移ENTRY_SIZE = 16 # 每个符号条目长度FIRMWARE_BASE = 0x10000 # IDA加载基址
# 读取固件with open(FIRMWARE_FILE, “rb”) as f: firmware = f.read()
# 提取符号表symtab = firmware[SYMTAB_OFFSET:]offset = 0symbols = []while offset + ENTRY_SIZE <= len(symtab): try: # 解析符号表条目：符号名偏移 → 函数偏移 → 类型 → 保留 name_offset = struct.unpack(“>I”, symtab[offset:
offset+4])[0] – FIRMWARE_BASE func_offset = struct.unpack(“>I”, symtab[offset+4:
offset+8])[0] sym_type = struct.unpack(“>I”, symtab[offset+8:
offset+12])[0] 
except struct.error: break # 读取函数名（从name_offset位置） if name_offset < len(firmware): name = “” for i in range(100): c = firmware[name_offset + i] if c == 0: break if 0x20 <= c <= 0x7E: name += chr(c) # 仅保留函数类型条目 if func_offset != 0 and sym_type == 0x0500 and name: func_ea = func_offset # IDA中的实际地址 symbols.append((func_ea, name)) offset += ENTRY_SIZE
# 保存符号到文本文件with open(“symbols.txt”, “w”, encoding=”utf-8″) as f: for ea, name in symbols: f.write(f”{ea:
08X} {name}n”)print(f”提取到{len(symbols)}个符号！”)

然后用ida python 进行函数名重命名恢复符号。import idaapiimport idautilsimport ida_name # 导入ida_name模块获取常量
# 直接读取符号表并重命名symbol_file = “C:\Users\031225\Desktop\symbols.txt”symbol_map = {}with open(symbol_file, “r”) as f: for line in f: if not line.strip(): continue addr_str, name = line.strip().split(” “, 1) addr = int(addr_str, 16) symbol_map[addr] = namerenamed = 0for addr, name in symbol_map.items(): if idaapi.get_func(addr) is None: idaapi.add_func(addr) # 使用ida_name.SN_FORCE或直接用0x40 if ida_name.set_name(addr, name, ida_name.SN_FORCE): renamed += 1print(f”完成！重命名{renamed}个函数”)恢复后的函数效果

找到loginDefaultEncrypt()函数

那么上面的算法就是有缺陷的被改动的hash算法，根据反编译的逻辑写一个python脚本计算字符串“SimpleXue”最终的加密哈希值。def loginDefaultEncrypt(input_str): if len(input_str) <= 7 or len(input_str) > 40: return None # 计算 v4 v4 = 0 for i, ch in enumerate(input_str): v7 = ord(ch) * (i + 2) v4 += (v7 ^ (i + 1)) & 0xFFFFFFFF # 乘法 num = (31695317 * (v4 & 0xFFFFFFFF)) & 0xFFFFFFFF # 字符替换 result = “” for c in str(num): ascii_val = ord(c) if ascii_val <= 0x32: # 0-2 ascii_val += 33 if ascii_val <= 0x35: # 3-5 ascii_val += 47 if ascii_val <= 0x38: # 6-8 ascii_val += 65 # 9 不变 result += chr(ascii_val) return result
# 测试print(loginDefaultEncrypt(“SimpleXue”)) # 输出: SQbcQSScQc

本篇文章来源于微信公众号: Laopo安全

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1764668611-wxsync-2025-12-5f7b868aec1e5da8ea20e1d8e7f437b8.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1764668613-wxsync-2025-12-fb1fa80c04104466534740c708921947.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1764668615-wxsync-2025-12-c1ff9b60ea0ca1d5174108005359e549.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1764668618-wxsync-2025-12-44b543c99310e91c29d87341559b6ba9.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1764668620-wxsync-2025-12-ee3d698e90ffe794f861ccba575fea8f.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1764668621-wxsync-2025-12-ca1b92bfcd576adae2ad555b49b3da36.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1764668623-wxsync-2025-12-07a025ccebe10e5176bdf04f08345c33.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1764668625-wxsync-2025-12-f2bad707c42daad1e5643bbefce69537.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1764668627-wxsync-2025-12-5ab9b575715d4dfe3523ac09aec98f89.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1764668629-wxsync-2025-12-1f0d4711ad5c045e3bc10bf4cce0b841.jpg)